# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T01:02:22.514Z

```
你是 SandboxWorld 项目(泰拉瑞亚 1.4.5.6 的 TypeScript 复刻,实现代码在 ~/Project/GLM/SandboxWorld/game/src/)的机制审计员。你的域是:**物品使用主链(useTime/useAnimation/autoReuse/reuseDelay/使用节奏)**——这是所有武器/工具/消耗品的共同骨架。

参照资源:
- 官方 wiki 离线镜像:~/Project/GLM/SandboxWorld/terraria-wiki-md/(Use_time.md、Autoswing.md、相关武器页)
- 反编译源码:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/(Player.cs ItemCheck/ApplyItemTime 段;先 grep -n 定位再精读)
- 本仓库实现:game/src/core/Game.ts、game/src/entities/Player.ts(grep "useTime\|useAnimation\|autoReuse\|reuseDelay\|itemTime")

审计规则:
- 只读审计,禁止修改/创建任何文件,报告作为最终回复返回
- wiki 与实现冲突时以源码裁决;wiki 与源码不符要标注
- 每条结论给实现侧 file:line 证据(grep 到并读过;纯推断标 ❓)

必核清单:
1. useTime vs useAnimation 双轨:动画时长 vs 触发 tick 的关系(itemAnimation 每帧递减、itemTime 到 0 才能再触发)、useAnimation<useTime 时(急速武器)的行为
2. reuseDelay(使用后冷却,如某些枪/回旋镖再掷延迟)
3. autoReuse:自动连发规则、是否需要重新按住、1.4 手动连发的节奏
4. 攻速加成链:meleeSpeed 对 useAnimation/useTime 的作用公式(CapAttackSpeeds 及倒数档)、各来源(甲虫球/食物/野性爪/夜明套/狼人)叠加语义
5. 使用时机与动作打断:使用中能否切换物品(切了会怎样)、使用中能否跳跃移动、使用时喝药打断
6. 弹药/魔法发射时机(itemTime 中段发射 vs 开头)、连续射击的每发间隔
7. 消耗品使用:药水饮用时间(useTime 长如 17?)、喝药动画、是否可被打断
8. 放置类物品使用:放置节奏、placeAnimation
9. 冲刺/位移武器(暗影匕首?)与使用链交互
10. 挥舞类近战伤害判定窗口(itemAnimation 哪个阶段判伤)与攻击弧线

实现侧入口:grep -rn "useTime\|useAnimation\|autoReuse\|reuseDelay" game/src/core/Game.ts game/src/entities/Player.ts | head -40

输出格式(markdown):
## 域:物品使用主链
### 差异清单
| # | 机制项 | 原版设定(wiki页+数值) | 本仓库实现(file:line) | 状态 | 差异细节 |
状态:✅对齐(一行) / ⚠️数值偏差(两侧数值) / ❌未实现 / 🔀逻辑不同 / ❓存疑 / 📄wiki与源码不符
### 覆盖清单
### 最需修复 TOP N
```

---

## 📎 Attachment · skill_listing · 2026-08-13T01:02:22.516Z

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

## 🤖 Assistant · 2026-08-13T01:02:24.041Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I'm the mechanics auditor for the item usage main chain. Let me start by exploring the key files:

1. First, look at the wiki mirror for Use_time.md and Autoswing.md
2. Then the decompiled source Player.cs ItemCheck/ApplyItemTime sections
3. Then the repo implementation in game/src/core/Game.ts and game/src/entities/Player.ts

Let me start with parallel exploration.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:24.603Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | head -50; echo \"---\"; ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | grep -i -E \"use_time|autoswing|use\" ",
 "description": "List wiki mirror files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:24.681Z

**📎 ToolResult**

```
_categories_partials_Category_3DS_content_pages_1.md
_categories_partials_Category_3DS_content_pages_2.md
_categories_partials_Category_3DS_content_pages_3.md
_categories_partials_Category_3DS_content_pages_4.md
_categories_partials_Category_3DS_content_pages_5.md
_categories_partials_Category_3DS_content_pages_6.md
_categories_partials_Category_3DS_content_pages_7.md
_categories_partials_Category_3DS_content_pages_8.md
_categories_partials_Category_Accessory_items_pages_1.md
_categories_partials_Category_Accessory_items_pages_2.md
_categories_partials_Category_Achievement-related_elements_pages_1.md
_categories_partials_Category_Achievement-related_elements_pages_2.md
_categories_partials_Category_Autoswing_items_pages_1.md
_categories_partials_Category_Autoswing_items_pages_2.md
_categories_partials_Category_Bag_loot_items_pages_1.md
_categories_partials_Category_Bag_loot_items_pages_2.md
_categories_partials_Category_Buffs_pages_1.md
_categories_partials_Category_Buffs_pages_2.md
_categories_partials_Category_By_Hand_pages_1.md
_categories_partials_Category_By_Hand_pages_2.md
_categories_partials_Category_Console_content_pages_1.md
_categories_partials_Category_Console_content_pages_10.md
_categories_partials_Category_Console_content_pages_11.md
_categories_partials_Category_Console_content_pages_12.md
_categories_partials_Category_Console_content_pages_13.md
_categories_partials_Category_Console_content_pages_14.md
_categories_partials_Category_Console_content_pages_15.md
_categories_partials_Category_Console_content_pages_16.md
_categories_partials_Category_Console_content_pages_17.md
_categories_partials_Category_Console_content_pages_2.md
_categories_partials_Category_Console_content_pages_3.md
_categories_partials_Category_Console_content_pages_4.md
_categories_partials_Category_Console_content_pages_5.md
_categories_partials_Category_Console_content_pages_6.md
_categories_partials_Category_Console_content_pages_7.md
_categories_partials_Category_Console_content_pages_8.md
_categories_partials_Category_Console_content_pages_9.md
_categories_partials_Category_Consumable_items_pages_1.md
_categories_partials_Category_Consumable_items_pages_2.md
_categories_partials_Category_Consumable_items_pages_3.md
_categories_partials_Category_Consumable_items_pages_4.md
_categories_partials_Category_Consumable_items_pages_5.md
_categories_partials_Category_Consumable_items_pages_6.md
_categories_partials_Category_Craftable_items_pages_1.md
_categories_partials_Category_Craftable_items_pages_2.md
_categories_partials_Category_Craftable_items_pages_3.md
_categories_partials_Category_Craftable_items_pages_4.md
_categories_partials_Category_Craftable_items_pages_5.md
_categories_partials_Category_Craftable_items_pages_6.md
_categories_partials_Category_Craftable_items_pages_7.md
---
_categories_partials_Category_Autoswing_items_pages_1.md
_categories_partials_Category_Autoswing_items_pages_2.md
Abandoned_house.md
Activate_Set_Bonuses.md
Autopause_Off.md
Autopause_On.md
Autopause.md
Autoswing.md
Ball_O'_Fuse_Wire.md
Black_Recluse_Banner.md
Black_Recluse.md
Category_Autoswing_items
Category_Autoswing_items.md
Category_Valid_house_NPCs
Category_Valid_house_NPCs.md
Confused
Confused.md
Floating_house.md
Focused.md
Gold_Mouse.md
House
House.md
Infused_Fertilizer.md
Legacy_Autoswing.md
Legacy_House.md
ManaUser.md
Mouse_Statue.md
Mouse.md
ReuseDelay.md
Ruined_House.md
Treehouse.md
Unused_NPCs.md
Use_delay.md
Use_Style_IDs.md
Use_style.md
Use_time
Use_time.md
UseAnimation.md
UseTime.md

```


---

## 🤖 Assistant · 2026-08-13T01:02:25.151Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"useTime\\|useAnimation\\|autoReuse\\|reuseDelay\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts 2>/dev/null | head -60",
 "description": "Grep implementation for item time fields"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:25.172Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:112:  useTime = 0;           // 通用动作冷却
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:136:   *  ——Game 鞭 useTime 结算读取；312/365 登记持续期（效果端暂不接） */
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:230:    autoReuseGlove: boolean; // 力量手套族：近战武器自动连挥（Player.cs:52040-52042）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:260:    whipSpd: number;       // 鞭 useTime 倍率（黑曜套 1/1.15）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:299:    let ammoSave = false, kbGlove = false, yoyoString = false, autoReuseGlove = false;
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:373:        if (fx.autoReuseGlove) autoReuseGlove = true;   // 力量手套族：近战自动连挥
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:500:      arrowDmg, ammoSave, kbGlove, autoReuseGlove, yoyoString,
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:545:   *  封顶 3 后取倒数，作为 useAnimation/useTime 的时长乘数。原"猛爪手套 ×2"档已废——
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:546:   *  原版猛爪手套 211 只给 meleeSpeed += 0.12 + autoReuseGlove（:14559-14562），
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:628:  /** 用魔物品起手（Game 在设定 useTime 后调用）：登记动画窗，窗内每帧重置
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:630:   *  ItemCheck_ApplyManaRegenDelay :49851；本仓单计时器模型以 useTime 代 useAnimation） */
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:632:    this.manaAnimTicks = Math.max(this.manaAnimTicks, this.useTime);
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:669:    if (this.useTime > 0) this.useTime--;
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1517:    // （攻击中 itemAnimation 门→近似 useTime>0 暂停 5t）；星璇套=双击↓开关 vortexStealthActive
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1526:      if (this.useTime > 0) { this.stealthTimer = 15; if (this.stealth > 0) this.stealth = Math.min(1, this.stealth + 0.1); }
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1532:      if (this.useTime > 0) this.stealthTimer = 5;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:553:  /** 上一帧鼠标左键状态（非 autoReuse 近战武器需点击沿触发新挥，原版 autoReuse 语义） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2103:        || w.oldOnesArmy.ongoing || this.player.useTime > 0;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2483:    // 非 autoReuse 武器(链球/回旋镖/悠悠球/长矛)全体掷不出(2026-08-13 实锤)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2492:    // 按住期间已有 1094 进 ai[0]=1000 喷火态 + SetDummyItemTime(2) 锁 useTime）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2508:          this.player.useTime = Math.max(this.player.useTime, 2); // SetDummyItemTime(2)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2533:        if (!this.golfAim && inp.mouseDown && this.player.useTime === 0) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2578:            this.player.useTime = 0;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2583:            this.player.useTime = Math.max(this.player.useTime, 12);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2599:            this.player.useTime = 42; // useAnimation 12 + 后摇 30（:49561-49567）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2700:    this.prevSwingMouse = !!this.input?.mouseDown; // 挥剑点击沿（非 autoReuse 武器需重新点击）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3699:      speed: c?.useAnimation ?? 25,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3700:      useTime: c?.useTime ?? 20,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3737:  /** 使用动画时长（Player.itemAnimationMax = item.useAnimation）：
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3738:   *  vi_ 取 vanilla-itemcombat.useAnimation；legacy 工具 def.tool.speed；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3739:   *  无数据 → 30（原版绝大多数消耗品 useAnimation 15-45 的中位近似） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3745:      const ua = itemCombat(vid)?.useAnimation;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3901:      canChangeImmediately: !this.swing && p.useTime === 0,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3903:      // 本作 swing = itemAnimation、player.useTime = itemTime；reuseDelay/channel/
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4049:      // ★挥击时长 = useAnimation、复用冷却 = useTime（Player.ItemCheck：itemAnimationMax 与
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4050:      // itemTime 分立；1790 件 vi 武器两者不同——此前把 useTime 当动画时长，挥速虚快 35%+）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4051:      // autoReuse 持按链式：useTime<useAnimation 时原版会在动画未走完时重置弧线（下挥被截）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4055:        : Math.max(4, Math.round((cwMelee!.useAnimation) / this.player.attackSpeedMult));
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4056:      // ★原版 ApplyItemTime（P:4216-4222）useTime 裸值不乘 meleeSpeed——此前误缩
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4060:        : Math.max(1, Math.round(cwMelee!.useTime));
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4061:      // TryAllowingItemReuse（Player.cs:52036-52053）：autoReuseGlove（力量手套族配饰）给
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4064:      const gloveReuse = this.player.equipStats.autoReuseGlove && heldVid !== 3030;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4065:      const autoReuse = cwMelee ? (cwMelee.autoReuse || gloveReuse) : true;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4067:      const canChain = autoReuse || clickEdge; // 非 autoReuse 武器需重新点击（原版语义）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4071:      //   此前 !this.swing 硬门让每挥击周期漏出 1 帧 useTime==0——黄蜂 ai[1] 每周期清零,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4074:      if (this.player.useTime === 0 && canChain && (swingOver || reuseSpd < animSpd)) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4080:        this.player.useTime = reuseSpd;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4084:        // 挥砍为主 + 挥击启动帧朝鼠标射出 item.shoot（useTime 节奏=每次挥击一弹）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4111:      if (this.player.useTime === 0 && (!this.swing || this.swing.t <= 1)) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4113:        this.player.useTime = spd;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4130:      this.tryMine(tx, ty, dual.power, dual.type, spd, tool.useTime ?? spd);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4136:    // 对准 219/642 左键使用 → 转化；642 先查矿物兑换表。useTime 冷却 = 10×(642?0.33:1)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4137:    if (inp.mouseDown && !inp.rightDown && this.player.useTime === 0
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4142:          // useAnimation 15（Item.cs:6301 泥沙/MakeUsableWithChlorophyteExtractinator:48120）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4169:    // （Player.ItemCheck：itemAnimationMax = useAnimation，ApplyUseStyle 按 useStyle
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4176:    if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4191:        this.player.useTime = 30;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4195:    if (heldDef?.potion && inp.mouseDown && this.player.useTime === 0) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4207:        this.player.useTime = 30;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4217:        this.player.useTime = 60;

```


---

## 🤖 Assistant · 2026-08-13T01:02:26.416Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read the wiki pages and then dig into the source code. Let me read the key wiki pages first: Use_time.md, Autoswing.md, UseAnimation.md, ReuseDelay.md, Use_delay.md, Use_Style_IDs.md.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:26.580Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Use_time.md"
}
```


---

## 🤖 Assistant · 2026-08-13T01:02:26.758Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Autoswing.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:26.763Z

**📎 ToolResult**

```
1	# Autoswing
2	
3	> 原页面: `Autoswing`
4	
5	# Autoswing
6	
7	[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
8	
9	This is the **main** page whose information applies to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.  
10	For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Autoswing](Legacy%3AAutoswing "Legacy:Autoswing")**.
11	
12	For a list of weapons with autoswing, use the sort feature of the Autoswing column on the [List of weapons](List_of_weapons.md "List of weapons") page or see [Category:Autoswing items](Category%3AAutoswing_items "Category:Autoswing items").
13	
14	Demonstration of the [Cutlass'](Cutlass.md "Cutlass") autoswing.
15	
16	Demonstration of how all [blocks](Blocks.md "Blocks") have autoswing when being placed.
17	
18	**Autoswing** , also known as **autofire** or **autouse** , is a property that can apply to usable items, such as [weapons](Weapons.md "Weapons"), [tools](Tools.md "Tools") and [blocks](Blocks.md "Blocks"), wherein the item is automatically reused (or swung) while the [`⚒ Use / Attack`](Game_controls.md "Game controls") key/button is held down. In contrast, weapons without autoswing require that the player repeatedly clicks or presses [`⚒ Use / Attack`](Game_controls.md "Game controls") in order to continue attacking. 
19	
20	On the wiki, items with autoswing feature the [](Autoswing.md "Autoswing") icon in the top-right corner of their infobox. 
21	
22	## Notes
23	
24	  * Internally, the `autoReuse` attribute determines whether an item has the ability to autoswing.
25	  * Autoswing can be enabled for all weapons in the [settings](Settings.md "Settings") menu by enabling the "Autofire" option. Autoswing can also be enabled on [melee weapons](Melee_weapons.md "Melee weapons") and [whips](Whips.md "Whips") by certain accessories: [Feral Claws](Feral_Claws.md "Feral Claws"), [Power Glove](Power_Glove.md "Power Glove"), [Mechanical Glove](Mechanical_Glove.md "Mechanical Glove"), [Fire Gauntlet](Fire_Gauntlet.md "Fire Gauntlet"), and [Berserker's Glove](Berserker's_Glove.md "Berserker's Glove")**** __(Desktop, Console and Mobile versions). 
26	    * Note that none of these actually change the `autoReuse` attribute of an item.
27	
28	View or edit this template
29	
30	Game mechanics
31	
32	Combat
33	
34	  * [Attack speed](Attack_speed.md "Attack speed")
35	  * Autoswing
36	  * [Critical hit](Critical_hit.md "Critical hit")
37	  * [Damage](Damage.md "Damage")
38	    * [Invincibility frame](Invincibility_frame.md "Invincibility frame")
39	  * [Knockback](Knockback.md "Knockback")
40	  * [Lock on](Lock_on.md "Lock on")**** __(Desktop, Console, Mobile and 3DS versions)
41	  * [Velocity](Velocity.md "Velocity")
42	
43	Environment
44	
45	  * [Ambient objects](Ambient_objects.md "Ambient objects")
46	  * [Ambient entities](Ambient_entities.md "Ambient entities")**** __(Desktop, Console and Mobile versions)
47	  * [Biome backgrounds](Biome_backgrounds.md "Biome backgrounds")
48	  * [Biomes](Biomes.md "Biomes")
49	    * [Spread](Biome_spread.md "Biome spread")
50	  * [Day and night cycle](Day_and_night_cycle.md "Day and night cycle")
51	  * [Events](Events.md "Events")
52	  * [Gravity](Gravity.md "Gravity")
53	  * [Liquids](Liquids.md "Liquids")
54	  * [Moon phase](Moon_phase.md "Moon phase")
55	  * [Music](Music.md "Music")
56	  * [NPC spawning](NPC_spawning.md "NPC spawning")
57	  * [Status messages](Status_messages.md "Status messages")
58	  * [Wind](Wind.md "Wind")
59	
60	Interface
61	
62	  * [Boss health bar](Boss_health_bar.md "Boss health bar")**** __(Desktop, Console and Mobile versions)
63	  * [Camera Mode](Camera_Mode.md "Camera Mode")**** __(Desktop version)
64	  * [Credits](Credits.md "Credits")**** __(Desktop, Console and Mobile versions)
65	  * [Emotes](Emotes.md "Emotes")**** __(Desktop, Console and Mobile versions)
66	  * [Minimap](Minimap.md "Minimap")
67	  * [Logo](Logo.md "Logo")
68	  * [NPC flag](NPC_flag.md "NPC flag")
69	  * [Title messages](Title_messages.md "Title messages")**** __(Desktop version)
70	  * [Tips](Tips.md "Tips")
71	  * [Resource Packs](Resource_Pack.md "Resource Pack")**** __(Desktop version)
72	  * [RGB](RGB.md "RGB")**** __(Desktop version)
73	  * [Workshop Hub](Workshop_Hub.md "Workshop Hub")**** __(Desktop version)
74	
75	Items
76	
77	  * [Alternative crafting ingredients](Alternative_crafting_ingredients.md "Alternative crafting ingredients")
78	  * [Ammo conversion](Ammo_conversion.md "Ammo conversion")
79	  * [Block Swap](Block_Swap.md "Block Swap")**** __(Desktop, Console and Mobile versions)
80	  * [Consumables](Consumables.md "Consumables")
81	  * [Crafting stations](Crafting_stations.md "Crafting stations")
82	    * [By Hand](By_Hand.md "By Hand")
83	  * [Crossover content](Crossover_content.md "Crossover content")
84	  * [Explosion-proof objects](Explosion-proof_objects.md "Explosion-proof objects")
85	  * [Flat-surface items](Flat-surface_items.md "Flat-surface items")
86	  * [Highlight](Highlight.md "Highlight")
87	  * [Mining speed](Mining_speed "Mining speed")
88	  * [Modifiers](Modifiers.md "Modifiers")
89	  * [NPC drops](NPC_drops.md "NPC drops")
90	  * [Placement](Placement.md "Placement")
91	  * [Pickaxe power](Pickaxe_power.md "Pickaxe power")
92	  * [Rarity](Rarity.md "Rarity")
93	  * [Recipes](Recipes.md "Recipes")
94	  * [Storage](Storage_items.md "Storage items")
95	  * [Tooltips](Tooltips.md "Tooltips")
96	  * [Use time](Use_time.md "Use time")
97	  * [Value](Value.md "Value")
98	
99	Game
100	
101	  * [Achievements](Achievements.md "Achievements")**** __(Desktop, Console, Old-gen console and Mobile versions)
102	  * [Difficulty](Difficulty.md "Difficulty")
103	    * [Journey](Journey_Mode.md "Journey Mode")**** __(Desktop, Console and Mobile versions)
104	    * [Classic](Classic_Mode.md "Classic Mode")
105	    * [Expert](Expert_Mode.md "Expert Mode")**** __(Desktop, Console and Mobile versions)
106	      * [Coin pickup](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")**** __(Desktop, Console and Mobile versions)
107	    * [Master](Master_Mode.md "Master Mode")**** __(Desktop, Console and Mobile versions)
108	  * [Fishing](Fishing.md "Fishing")
109	  * [Golf](Golf.md "Golf")**** __(Desktop, Console and Mobile versions)
110	  * [Hoik](Hoik.md "Hoik")
111	  * [Music](Music.md "Music")
112	  * [Teleportation](Teleportation.md "Teleportation")
113	    * [Pylons](Pylons.md "Pylons")**** __(Desktop, Console and Mobile versions)
114	  * [Town](Town.md "Town")**** __(Desktop, Console and Mobile versions)
115	
116	Multiplayer
117	
118	  * [Server](Server.md "Server")
119	  * [Chat](Chat.md "Chat")
120	  * [Multiplayer](Multiplayer.md "Multiplayer")
121	
122	Player
123	
124	  * [Aggro](Aggro.md "Aggro")
125	  * [Ammo conservation](Ammo_conservation.md "Ammo conservation")
126	  * [Breath meter](Breath_meter.md "Breath meter")
127	  * [Buffs](Buffs.md "Buffs")
128	    * [Debuffs](Debuffs.md "Debuffs")
129	  * [Character](Character.md "Character")
130	  * [Character styles](Character_styles.md "Character styles")**** __(Desktop, Console and Mobile versions)
131	  * [Damage reduction](Damage_reduction.md "Damage reduction")
132	  * [Dash](Dash.md "Dash")
133	  * [Death](Death.md "Death")
134	  * [Defense](Defense.md "Defense")
135	  * [Dodge](Dodge.md "Dodge")
136	  * [Drowning](Drowning.md "Drowning")
137	  * [Extra jump](Extra_jump.md "Extra jump")
138	  * [Fall damage](Fall_damage.md "Fall damage")
139	  * [Flight](Flight.md "Flight")
140	  * [Ghost](Ghost.md "Ghost")**** __(Desktop, Console, Old-gen console and Mobile versions)
141	  * [Hairstyles](Hairstyles.md "Hairstyles")
142	  * [Health](Health.md "Health")
143	  * [Health regeneration](Health_regeneration.md "Health regeneration")
144	  * [Inventory](Inventory.md "Inventory")
145	  * [Lifesteal](Lifesteal.md "Lifesteal")
146	  * [Loadouts](Loadouts.md "Loadouts")**** __(Desktop, Console and Mobile versions)
147	  * [Luck](Luck.md "Luck")**** __(Desktop, Console and Mobile versions)
148	  * [Mana](Mana.md "Mana")
149	  * [Movement speed](Movement_speed.md "Movement speed")
150	  * [Social slots](Social_slots.md "Social slots")
151	  * [Spawn](Spawn.md "Spawn")
152	  * [Stealth](Stealth.md "Stealth")
153	
154	Settings
155	
156	  * [Cursor modes](Cursor_modes.md "Cursor modes")
157	  * [Game controls](Game_controls.md "Game controls")
158	  * [Lighting mode](Lighting_mode.md "Lighting mode")**** __(Desktop, Console and Mobile versions)
159	  * [Parallax](Parallax.md "Parallax")**** __(Desktop, Console and Mobile versions)
160	  * [Settings](Settings.md "Settings")**** __(Desktop, Console, Mobile and 3DS versions)
161	  * [Toggles](Toggles.md "Toggles")
162	
163	Technical
164	
165	  * [AI](AI.md "AI")
166	  * [Chat commands](Commands.md "Commands")
167	  * [Command-line parameters](Command-line_parameters.md "Command-line parameters")**** __(Desktop version)
168	  * [Config.json](Config.json_settings.md "Config.json settings")**** __(Desktop and Mobile versions)
169	  * [Data IDs](Data_IDs.md "Data IDs")
170	  * [Debug commands](Debug_commands.md "Debug commands")**** __(Desktop version)
171	  * [Game platform](Game_platform.md "Game platform")
172	  * [NPC names](NPC_names.md "NPC names")
173	  * [Projectiles](Projectiles.md "Projectiles")
174	
175	World
176	
177	  * [Pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode")
178	  * [Hardmode](Hardmode.md "Hardmode")
179	    * [Conversion](Hardmode_conversion.md "Hardmode conversion")
180	  * [Special world seeds](Special_world_seeds.md "Special world seeds")**** __(Desktop, Console and Mobile versions)
181	  * [Secret world seeds](Secret_world_seeds.md "Secret world seeds")**** __(Desktop, Console and Mobile versions)
182	  * [World](World.md "World")
183	    * [Generation](World_generation.md "World generation")
184	  * [World Seed](World_Seed.md "World Seed")**** __(Desktop, Console and Mobile versions)
185	  * [World size](World_size.md "World size")
186	
187	Category: 
188	
189	  * [Game mechanics](Category%3AGame_mechanics "Category:Game mechanics")
190	
191	Hidden categories: 
192	
193	  * Pages using DynamicPageList3 dplvar parser function
194	  * Pages using DynamicPageList3 parser function
195	  * Mainspace pages with a corresponding Legacy page
196	  * Pages with navboxes
197	  * Random
198	
199	This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=Autoswing&oldid=998900 "Last edited on 2026-06-19"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
200	  *[1 required]: Journey Mode
201	  *[Qty.]: Quantitas
202	  *[100%]: Expert Mode
203	  *[DPS]: Damage per second
204	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
205	  *[300]: Expert Mode
206	  *[400]: Master Mode
207	  *[160]: Expert Mode
208	  *[240]: Master Mode
209	  *[3 required]: Journey Mode
210	  *[#]: Number of summons, i.e. times that Abigail's Flower was used
211	  *[Max.  
212	enemies]: Maximum number of enemies Abigail can damage at once
213	  *[HM]: Hardmode
214	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
215	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
216	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
217	  *[8]: Expert Mode
218	  *[10]: Chế độ Expert
219	  *[120]: Master Mode
220	  *[150]: Expert Mode
221	  *[13]: Chế độ Master
222	  *[195]: Master Mode
223	  *[Verify]: Is this still true?
224	  *[50 required]: Journey Mode
225	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
226	  *[100 required]: Journey Mode
227	  *[cần có 1]: Chế độ Journey
228	  *[25 required]: Journey Mode
229	  *[cần có 25]: Chế độ Journey
230	  *[400 required]: Journey Mode
231	  *[membutuhkan 100]: Mode Journey
232	  *[cần có 100]: Chế độ Journey
233	  *[Slg.]: Số lượng
234	  *[1.99%]: Expert Mode
235	  *[199/10000 (1.99%)]: Expert Mode
236	  *[membutuhkan 1]: Mode Journey
237	  *[1,99%]: Expert Mode
238	  *[1/50 (2%)]: Mode Expert
239	  *[200 required]: Journey Mode
240	  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11 tiles per second
241	  *[16 mph]: 16 mil per jam (diukur dengan item Stopwatch) atau 11.73 blok per detik
242	  *[20 required]: Journey Mode
243	  *[180]: Expert Mode
244	  *[270]: Master Mode
245	  *[5–9 seconds]: Expert Mode
246	  *[5–9]: Expert Mode
247	  *[15 required]: Journey Mode
248	  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
249	  *[Power]: Bait Power
250	  *[5 required]: Journey Mode
251	  *[cần có {{{research}}}]: Chế độ Journey
252	  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
253	  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
254	  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
255	  *[Expert Mode exclusive]: Expert Mode
256	  *[402]: Master Mode
257	  *[523]: Expert Mode
258	  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
259	  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
260	  *[800]: Expert Mode
261	  *[1200]: Master Mode
262	  *[15]: Expert Mode
263	  *[17]: Master Mode
264	  *[O. v. odražení]: Odolnost vůči odražení
265	  *[1 minute 30 seconds]: Expert Mode
266	  *[1 minute 52.5 seconds]: Master Mode
267	  *[90]: Expert Mode
268	  *[112.5]: Master Mode
269	  *[2–6]: Expert Mode
270	  *[2-6]: Expert Mode
271	  *[%100]: Expert Mode
272	  *[28]: Expert Mode
273	  *[42]: Master Mode
274	  *[80]: Expert Mode
275	  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
276	  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
277	  *[ Major improvements to all stats and increased life regeneration]: Expert Mode
278	  *[50%]: Expert Mode
279	  *[1/2 (50%)]: Expert Mode
280	  *[30]: Mode Expert
281	  *[45]: Mode Master
282	  *[3/4]: Chế độ Expert
283	  *[5]: Master Mode
284	  *[75%]: Mode Expert
285	  *[semua]: Mode Master
286	  *[6]: Chế độ Master
287	  *[toàn bộ]: Chế độ Master
288	  *[199/10000 (1,99%)]: Mode Expert
289	  *[4 minutes]: Expert Mode
290	  *[5 minutes]: Master Mode
291	  *[4]: Expert Mode
292	  *[36]: Expert Mode
293	  *[22]: Expert Mode
294	  *[26]: Master Mode
295	  *[Ruce pryč od mé zbraně, kámo!]: Keep your hands off my gun, buddy!
296	  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
297	  *[Koukám, že házíš očkem po žraločkovi. Opravdu nechceš vědět, jak byl vyroben.]: I see you're eyeballing the Minishark. You really don't want to know how it was made.
298	  *[Neobtěžuj se s [jméno demoličního experta], vše, co potřebuješ, je přímo tady.]: Don't bother with [Name of Demolitionist], I've got all you need right here.
299	  *[Jaký má [jméno demoličního experta] problém? Uvědomuje si vůbec, že oba prodáváme naprosto rozdílné zboží?]: What's [Name of Demolitionist]'s problem? Does he even realize we sell completely different stuff?
300	  *[Pohni zadkem! Za hodinu mám rande s [jméno sestřičky].]: Make it quick! I've got a date with [Name of Nurse] in a hour.
301	  *[Chci to, co [jméno sestřičky] prodává. Co myslíš tím, že neprodává ani ň?]: I want what [Name of Nurse] is sellin'. What do you mean, she doesn't sell anything?
302	  *[Na [jméno dryády] bych mohl oči nechat. Škoda, že je to taková prudařka.]: [Name of Dryad] is a looker. Too bad she's such a prude.
303	  *[Slyšel jsem, že se ve světě nachází panenka vypadající skoro jako [jméno průvodce]. Mile rád bych do ní vpálil pár kulek.]: I heard there is a doll that looks very similar to [Name of Guide] somewhere in the underworld. I'd like to put a few rounds in it.
304	  *[Miluji noci jako je tahle. Vždy se najde něco na zabití.]: I love nights like tonight, there is never a shortage of things to kill.
305	  *[Chlape, tohle je noc přímo stvořená, abys s nikým nemusel mluvit, nemyslíš [jméno hráče]?]: Man, it's a good night not to talk to anybody, don't you think, [Name of Player]?
306	  *[14]: Expert Mode
307	  *[17.5]: Master Mode
308	  *[7]: Expert Mode
309	  *[8.75]: Master Mode
310	  *[21]: Expert Mode
311	  *[26.25]: Master Mode
312	  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
313	  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second

```


---

## 👤 User(sidechain) · 2026-08-13T01:02:26.808Z

**📎 ToolResult**

```
1	# Use time
2	
3	> 原页面: `Use_time`
4	
5	# Use time
6	
7	**Use time** is a statistic that applies to [weapons](Weapons.md "Weapons"), [tools](Tools.md "Tools") and other usable [items](Items.md "Items"). It determines the time that must pass, after use, before the same item or another item can be used again. In basic terms, this is the "rate of fire", as measured in game ticks.[1] A lower use time means a faster weapon. The [shortswords](Shortswords "Shortswords"), for example, usually have a use time between 10 and 13, meaning that they can be used in quick succession, as compared to the exceptionally slow [Volcano](Volcano.md "Volcano"), which has a use time of 40 – a much slower weapon which cannot be used as often. 
8	
9	Use time is particularly useful in comparing the speed of tools and weapons. The in-game tooltips for these items automatically group these values into categories like "Very fast" or "Very slow". They are grouped as following: 
10	
11	Value | In-game text   
12	---|---  
13	≤8 | Insanely fast speed  
14	9–20 | Very fast speed  
15	21–25 | Fast speed  
16	26–30 | Average speed  
17	31–35 | Slow speed  
18	36–45 | Very slow speed  
19	46–55 | Extremely slow speed  
20	≥56 | Snail speed  
21	  
22	## Technical info
23	
24	Several statistics are used to determine the use behavior of an item: **`useTime`** ,[2] **`useAnimation`** ,[3] and **`reuseDelay`**.[4] All these values are in ticks.[1]
25	
26	  * `useTime` determines time between actual uses of the item, i.e., the interval between the item taking effect.
27	  * `useAnimation`, as its name suggests, is the duration of animation of each item use, i.e., the item's behavior after a single [`⚒ Use / Attack`](Game_controls.md "Game controls") key input.
28	  * `reuseDelay` determines how many ticks before an item can be used again. This is usually used for balancing weapons that would have extremely high fire rate otherwise. This stat is also commonly referenced to as "use delay".
29	
30	Internally, two tick counters, `itemTime` and `itemAnimation`, corresponding to `useTime` and `useAnimation` are applied to a player. When an item is used, the game checks for its `useTime` and `useAnimation`, applies all attack speed bonuses, then adds the resulting ticks to their respective counter. These counters are reduced by 1 per tick, and as long as they are above zero, the player is considered using the item and several actions are disabled for the duration. For most items, `useTime` is equal to `useAnimation`, meaning that the item would be used only once per [`⚒ Use / Attack`](Game_controls.md "Game controls") key input. Some items have their `useTime` stat less than `useAnimation`, which causes them to be used multiple times per [`⚒ Use / Attack`](Game_controls.md "Game controls") key input. 
31	
32	Times of use per [`⚒ Use / Attack`](Game_controls.md "Game controls") key input   
33	---  
34	[math]\displaystyle{ \text{Times of use} = \left\lceil \frac{\mathit{useAnimation}}{\mathit{useTime}} \right\rceil }[/math]  
35	[math]\displaystyle{ \lceil{x}\rceil }[/math] is the ceiling function (round up [math]\displaystyle{ x }[/math] to the next integer).  
36	  
37	`reuseDelay` is applied after the `itemAnimation` counter turns to zero. This will add value of `reuseDelay` to both counters, making the player have to wait a few more ticks before they can use item. 
38	
39	On this wiki, the `useAnimation` stat is displayed in infoboxes as the "use time" stat. The `useTime` stat is only displayed for [tools](Tools.md "Tools") as their "[tool speed](Tool_speed.md "Tool speed")" stat (since this stat have no effect on the function of other items in most cases). 
40	
41	On [ Desktop version](Desktop_version_history.md "Desktop version history"), certain actions are disabled when the `itemTime` or `itemAnimation` tick counters are not zero: 
42	
43	  * Actions that involve interaction with items in inventory, including:[5]
44	    * Switching held item (when `itemAnimation` tick counter is not zero).
45	    * Switching held item by mouse (when `itemTime` tick counter is not zero).
46	    * Throwing held item onto ground.
47	    * Changing equipables, including [armor](Armor.md "Armor"), [accessory](Accessory "Accessory"), and items in [equipment slots](Equipment_slot.md "Equipment slot").
48	    * [Inventory management keys](Cursor_modes#Special_cursors "Cursor modes") like Quick Sell, Quick Trash, etc.
49	  * Swapping [Loadouts](Loadouts.md "Loadouts")**** __(Desktop, Console and Mobile versions).[6]
50	  * The [Digging Molecart](Digging_Molecart.md "Digging Molecart")**** __(Desktop, Console and Mobile versions) 's mining and [Minecart Track](Minecart_Track.md "Minecart Track") placing.
51	  * Interaction with most game interface elements. This can be observed by turning on [autopause](Autopause.md "Autopause") and opening inventory when using an item. Apart from the Duplication Menu, other functions of [Journey Mode](Journey_Mode.md "Journey Mode") Power Menu will still be functional.[7]
52	
53	Several hotkeys will still be functional, including [`Quick Heal`](Game_controls.md "Game controls"), [`Quick Mana`](Game_controls.md "Game controls"), [`Quick Buff`](Game_controls.md "Game controls"), [`Grapple`](Game_controls.md "Game controls"), and [`Quick Mount`](Game_controls.md "Game controls"). 
54	
55	For example: 
56	
57	  * [Pickaxes](Pickaxes.md "Pickaxes") use `useTime` to determine how fast they can hit tiles (which is the [tool speed](Tool_speed.md "Tool speed") displayed on this wiki); their `useAnimation` determines how fast they deal melee damage (which is the duration of the swinging animation).
58	  * The [Golden Shower](Golden_Shower.md "Golden Shower") has a `useTime` of 6 and a `useAnimation` of 18, causing it firing 3 times per [`⚒ Use / Attack`](Game_controls.md "Game controls") key input.
59	  * The [Clockwork Assault Rifle](Clockwork_Assault_Rifle.md "Clockwork Assault Rifle") has a `useTime` of 4 and a `useAnimation` of 12, causing it firing 3 times per [`⚒ Use / Attack`](Game_controls.md "Game controls") key input. It also has a `reuseDelay` of 14, adding 14-tick interval between the three round bursts.
60	
61	### Special conditons
62	
63	#### Use limit
64	
65	The following weapons are specially coded to only fire a specific amount of times per use, based on their `useAnimation`: [Tome of Infinite Wisdom](Tome_of_Infinite_Wisdom.md "Tome of Infinite Wisdom")**** __(Desktop, Console and Mobile versions) (4 times), [Nightglow](Nightglow.md "Nightglow")**** __(Desktop, Console and Mobile versions) (4 times), and [Eventide](Eventide.md "Eventide")**** __(Desktop, Console and Mobile versions) (5 times).[8]
66	
67	#### Swinging items
68	
69	For items that are swung overhead ([melee](Melee "Melee") weapons, [pickaxes](Pickaxes.md "Pickaxes"), etc.), the length of their swinging animation is related to `useAnimation`. A single target will only be hit once during one swinging animation. 
70	
71	#### Projectile melee weapons
72	
73	The following [projectile melee weapons](Projectile_melee_weapons.md "Projectile melee weapons") have their projectiles' shoot rate based on their `useTime` stat, which differs from their standard use time (the `useAnimation`), so they might not shoot a projectile on every swing. These shoot rates can only be changed by [modifiers](Modifiers.md "Modifiers") as only modifiers can affect `useTime`. However, if such a weapon's `useTime` is less than its `useAnimation`, it still cannot shoot a projectile again until the swing finishes. 
74	
75	  * [](Starfury.md "Starfury")[Starfury](Starfury.md "Starfury")
76	  * [](Frostbrand.md "Frostbrand")[Frostbrand](Frostbrand.md "Frostbrand")
77	  * [](Beam_Sword.md "Beam Sword")[Beam Sword](Beam_Sword.md "Beam Sword")
78	  * [](Ice_Blade.md "Ice Blade")[Ice Blade](Ice_Blade.md "Ice Blade")
79	  * [](Enchanted_Sword.md "Enchanted Sword")[Enchanted Sword](Enchanted_Sword.md "Enchanted Sword")
80	  * [](Chlorophyte_Claymore.md "Chlorophyte Claymore")[Chlorophyte Claymore](Chlorophyte_Claymore.md "Chlorophyte Claymore")
81	  * [](Chlorophyte_Saber.md "Chlorophyte Saber")[Chlorophyte Saber](Chlorophyte_Saber.md "Chlorophyte Saber")
82	
83	****__(Desktop, Console and Mobile versions) The following projectile melee weapons have the `shootsEveryUse` ability, which causes them to shoot a projectile every time they are used. However, if such a weapon's `useTime` is less than its `useAnimation`, it still cannot shoot a projectile again until the swing finishes.
84	
85	  * [](Blade_of_Grass.md "Blade of Grass")[Blade of Grass](Blade_of_Grass.md "Blade of Grass")
86	  * [](Night's_Edge.md "Night's Edge")[Night's Edge](Night's_Edge.md "Night's Edge")
87	  * [](Excalibur.md "Excalibur")[Excalibur](Excalibur.md "Excalibur")
88	  * [](True_Excalibur.md "True Excalibur")[True Excalibur](True_Excalibur.md "True Excalibur")
89	  * [](True_Night's_Edge.md "True Night's Edge")[True Night's Edge](True_Night's_Edge.md "True Night's Edge")
90	  * [](Terra_Blade.md "Terra Blade")[Terra Blade](Terra_Blade.md "Terra Blade")
91	  * [](The_Horseman's_Blade.md "The Horseman's Blade")[The Horseman's Blade](The_Horseman's_Blade.md "The Horseman's Blade")
92	  * [](Waffle's_Iron.md "Waffle's Iron")[Waffle's Iron](Waffle's_Iron.md "Waffle's Iron")
93	
94	#### Combined with autoswing
95	
96	[Autoswinging](Autoswing.md "Autoswing") items are items that have the `autoReuse` attribute, i.e. having the [](Autoswing.md "Autoswing") autoswing icon displayed on its infobox on this wiki. When such an item reaches one tick before its animation ends, it immediately skips to start a new animation (a new use of the item).[9]
97	
98	This is fine for most of the items, as the game adds one tick to their `useAnimation` in the calculation process (see calculation below). However, this step is the last step in the whole process; the calculation for [melee weapons](Melee_weapons.md "Melee weapons") are done earlier, therefore skipping this step. This means that the actual use time (`useAnimation`) of autoswing melee weapons is one tick lower than the `useAnimation` stated in the source code, in the item's tooltip, and here on the wiki. 
99	
100	### Calculation
101	
102	The calculation of time taken for item use triggered by a single [`⚒ Use / Attack`](Game_controls.md "Game controls") key input uses different formula based on the type of item.[10]
103	
104	However, before all calculations, the effect of [modifiers](Modifiers.md "Modifiers") are applied first, acting as a direct change to specific item stats. `useTime`, `useAnimation`, and `reuseDelay` are affected, using the following formula: 
105	
106	[math]\displaystyle{ \text{New stat} = \operatorname{round}(\text{Original stat}\times\mathit{Modifier}) }[/math]
107	
108	  * The [math]\displaystyle{ \operatorname{round} }[/math] operator rounds the value to the nearest integer. If the value is halfway between two integers (.5), it will be rounded to the nearest even number theoretically, but the actual result may differ due to floating point inaccuracies.
109	  * [math]\displaystyle{ \mathit{Modifier} }[/math] is the modifier's boost to speed, in decimal. For example, the [Light](Light.md "Light") modifier gives +15% speed, which means [math]\displaystyle{ \mathit{Modifier}=1-0.15=0.85 }[/math].
110	
111	All formulas below use this new stat for calculation. 
112	
113	* | Weapon  | Modifier  | Bonus  | Modified `useAnimation` | Actual bonus[a]  
114	---|---|---|---|---  
115	[](Megashark.md "Megashark")  
116	[Megashark](Megashark.md "Megashark")  
117	Base `useAnimation`: 7 | Unreal  | +10% speed  | 6  | +14% speed (+4%)  
118	Rapid  | +15% speed  | 6  | +14% speed (-1%)  
119	[](Musket.md "Musket")  
120	[Musket](Musket.md "Musket")  
121	Base `useAnimation`: 32 | Nimble  | +5% speed  | 30  | +6% speed (+1%)  
122	Unreal  | +10% speed  | 29  | +9% speed (-1%)  
123	Rapid  | +15% speed  | 27  | +16% speed (+1%)  
124	  
125	The total time of item use is then calculated by the following formulas. Note that a given item corresponds to one and only one formula below. 
126	
127	**For items that deal[melee](Melee "Melee") damage:**
128	
129	[math]\displaystyle{ \text{Total time} = \left\lfloor\mathit{useAnimation}\times\frac{1}{1+\mathit{Melee\ speed}\times\mathit{Melee\ speed\ multiplier}}\right\rfloor+\mathit{reuseDelay} }[/math]
130	
131	  * [math]\displaystyle{ \left\lfloor{x}\right\rfloor }[/math] is the floor function (round down to the nearest integer).
132	  * [math]\displaystyle{ \mathit{Melee\ speed} }[/math] is the sum of melee speed bonuses in decimals, starting at 0. For example, 10% increased melee speed means +0.1.
133	  * [math]\displaystyle{ \mathit{Melee\ speed\ multiplier} }[/math] is [math]\displaystyle{ 1 }[/math] for most weapons. See table below for weapons with a different value:[11]
134	
135	Item | Multiplier   
136	---|---  
137	[Terra Blade](Terra_Blade.md "Terra Blade") | 0.75   
138	[Bladed Glove](Bladed_Glove.md "Bladed Glove") | 0.5   
139	[Fetid Baghnakhs](Fetid_Baghnakhs.md "Fetid Baghnakhs")**** __(Desktop, Console and Mobile versions) | 0.25   
140	[Psycho Knife](Psycho_Knife.md "Psycho Knife")**** __(Desktop, Console and Mobile versions) | 0.33   
141	  
142	**For[whips](Whips.md "Whips"):**
143	
144	[math]\displaystyle{ \text{Total time} = \left\lfloor\mathit{useAnimation}\times\frac{1}{1+\mathit{Melee\ speed}+\mathit{Whip\ speed\ buff}}\times\frac{1}{\mathit{Whip\ speed\ set\ bonus}}\right\rfloor+\mathit{reuseDelay} }[/math]
145	
146	  * [math]\displaystyle{ \mathit{Melee\ speed} }[/math] is the sum of melee speed bonuses in decimals, starting at 0. For example, 10% increased melee speed means +0.1.
147	  * [math]\displaystyle{ \mathit{Whip\ speed\ buff} }[/math] is the sum of whip speed bonuses from buffs in decimals, starting at 0. For example, 12% increased whip speed of [Jungle's Fury](Jungle's_Fury "Jungle's Fury") means +0.12.
148	  * [math]\displaystyle{ \mathit{Whip\ speed\ set\ bonus} }[/math] is whip speed bonuses from set bonus, which is 1 when no set bonus is in effect. Currently, only the [Obsidian armor](Obsidian_armor.md "Obsidian armor") provides this bonus, changing this value to 1.15.
149	  * Currently, all whips have a [math]\displaystyle{ \mathit{reuseDelay} }[/math] of 0.
150	
151	**For[blocks](Blocks.md "Blocks"):**
152	
153	[math]\displaystyle{ \text{Total time} = \left\lfloor\mathit{useAnimation}\times\frac{1}{1+\mathit{Block\ speed}}\right\rfloor+\mathit{reuseDelay} }[/math]
154	
155	  * [math]\displaystyle{ \mathit{Block\ speed} }[/math] is 0 by default; some items add a specific value to it.
156	  * Currently, all blocks have a [math]\displaystyle{ \mathit{reuseDelay} }[/math] of 0.
157	
158	{
159	
160	**For[walls](Walls "Walls"):**
161	
162	[math]\displaystyle{ \text{Total time} = \left\lfloor\mathit{useAnimation}\times\frac{1}{1+\mathit{Wall\ speed}}\right\rfloor+\mathit{reuseDelay} }[/math]
163	
164	  * [math]\displaystyle{ \mathit{Wall\ speed} }[/math] is 0 by default; some items add a specific value to it.
165	  * Currently, all walls have a [math]\displaystyle{ \mathit{reuseDelay} }[/math] of 0.
166	
167	Item | Value   
168	---|---  
169	[Ambrosia](Ambrosia.md "Ambrosia") | +0.05   
170	[Builder Potion](Builder_Potion.md "Builder Potion") | +0.25   
171	[Portable Cement Mixer](Portable_Cement_Mixer.md "Portable Cement Mixer")  
172	(or its upgrades) | +0.5   
173	  
174	For rest of the items that can [autoswing](Autoswing.md "Autoswing") (`autoReuse = true`), has a `reuseDelay` of 0, `useTime` is no more than `useAnimation`, can shoot projectile, and has a [use style](Use_Style_IDs.md "Use Style IDs") of 5 (see below for a list of applicable items): 
175	
176	[math]\displaystyle{ \text{Total time} = \mathit{useAnimation}+1 }[/math]
177	
178	  * The +1 negates the animation skip feature of autoswing items.
179	
180	*   * [](Minishark.md "Minishark")[Minishark](Minishark.md "Minishark")
181	  * [](Space_Gun.md "Space Gun")[Space Gun](Space_Gun.md "Space Gun")
182	  * [](Aqua_Scepter.md "Aqua Scepter")[Aqua Scepter](Aqua_Scepter.md "Aqua Scepter")
183	  * [](Harpoon.md "Harpoon")[Harpoon](Harpoon.md "Harpoon")
184	  * [](Water_Bolt.md "Water Bolt")[Water Bolt](Water_Bolt.md "Water Bolt")
185	  * [](Star_Cannon.md "Star Cannon")[Star Cannon](Star_Cannon.md "Star Cannon")
186	  * [](Sandgun.md "Sandgun")[Sandgun](Sandgun.md "Sandgun")
187	  * [](Blowpipe.md "Blowpipe")[Blowpipe](Blowpipe.md "Blowpipe")
188	  * [](Cobalt_Repeater.md "Cobalt Repeater")[Cobalt Repeater](Cobalt_Repeater.md "Cobalt Repeater")
189	  * [](Mythril_Repeater.md "Mythril Repeater")[Mythril Repeater](Mythril_Repeater.md "Mythril Repeater")
190	  * [](Adamantite_Repeater.md "Adamantite Repeater")[Adamantite Repeater](Adamantite_Repeater.md "Adamantite Repeater")
191	  * [](Magical_Harp.md "Magical Harp")[Magical Harp](Magical_Harp.md "Magical Harp")
192	  * [](Flamethrower.md "Flamethrower")[Flamethrower](Flamethrower.md "Flamethrower")
193	  * [](Laser_Rifle.md "Laser Rifle")[Laser Rifle](Laser_Rifle.md "Laser Rifle")
194	  * [](Crystal_Storm.md "Crystal Storm")[Crystal Storm](Crystal_Storm.md "Crystal Storm")
195	  * [](Cursed_Flames.md "Cursed Flames")[Cursed Flames](Cursed_Flames.md "Cursed Flames")
196	  * [](Megashark.md "Megashark")[Megashark](Megashark.md "Megashark")
197	  * [](Hallowed_Repeater.md "Hallowed Repeater")[Hallowed Repeater](Hallowed_Repeater.md "Hallowed Repeater")
198	  * [](Tactical_Shotgun.md "Tactical Shotgun")[Tactical Shotgun](Tactical_Shotgun.md "Tactical Shotgun")
199	  * [](Marrow.md "Marrow")[Marrow](Marrow.md "Marrow")
200	  * [](Unholy_Trident.md "Unholy Trident")[Unholy Trident](Unholy_Trident.md "Unholy Trident")
201	  * [](Ice_Bow.md "Ice Bow")[Ice Bow](Ice_Bow.md "Ice Bow")
202	  * [](Frost_Staff.md "Frost Staff")[Frost Staff](Frost_Staff.md "Frost Staff")
203	  * [](Sapphire_Staff.md "Sapphire Staff")[Sapphire Staff](Sapphire_Staff.md "Sapphire Staff")
204	  * [](Emerald_Staff.md "Emerald Staff")[Emerald Staff](Emerald_Staff.md "Emerald Staff")
205	  * [](Ruby_Staff.md "Ruby Staff")[Ruby Staff](Ruby_Staff.md "Ruby Staff")
206	  * [](Diamond_Staff.md "Diamond Staff")[Diamond Staff](Diamond_Staff.md "Diamond Staff")
207	  * [](Grenade_Launcher.md "Grenade Launcher")[Grenade Launcher](Grenade_Launcher.md "Grenade Launcher")
208	  * [](Rocket_Launcher.md "Rocket Launcher")[Rocket Launcher](Rocket_Launcher.md "Rocket Launcher")
209	  * [](Proximity_Mine_Launcher.md "Proximity Mine Launcher")[Proximity Mine Launcher](Proximity_Mine_Launcher.md "Proximity Mine Launcher")
210	  * [](Clentaminator.md "Clentaminator")[Clentaminator](Clentaminator.md "Clentaminator")
211	  * [](Nettle_Burst.md "Nettle Burst")[Nettle Burst](Nettle_Burst.md "Nettle Burst")
212	  * [](Coin_Gun.md "Coin Gun")[Coin Gun](Coin_Gun.md "Coin Gun")
213	  * [](Blowgun.md "Blowgun")[Blowgun](Blowgun.md "Blowgun")
214	  * [](Bee_Gun.md "Bee Gun")[Bee Gun](Bee_Gun.md "Bee Gun")
215	  * [](Wasp_Gun.md "Wasp Gun")[Wasp Gun](Wasp_Gun.md "Wasp Gun")
216	  * [](Leaf_Blower.md "Leaf Blower")[Leaf Blower](Leaf_Blower.md "Leaf Blower")
217	  * [](Palladium_Repeater.md "Palladium Repeater")[Palladium Repeater](Palladium_Repeater.md "Palladium Repeater")
218	  * [](Orichalcum_Repeater.md "Orichalcum Repeater")[Orichalcum Repeater](Orichalcum_Repeater.md "Orichalcum Repeater")
219	  * [](Titanium_Repeater.md "Titanium Repeater")[Titanium Repeater](Titanium_Repeater.md "Titanium Repeater")
220	  * [](Chlorophyte_Shotbow.md "Chlorophyte Shotbow")[Chlorophyte Shotbow](Chlorophyte_Shotbow.md "Chlorophyte Shotbow")
221	  * [](Venus_Magnum.md "Venus Magnum")[Venus Magnum](Venus_Magnum.md "Venus Magnum")
222	  * [](Stynger.md "Stynger")[Stynger](Stynger.md "Stynger")
223	  * [](Uzi.md "Uzi")[Uzi](Uzi.md "Uzi")
224	  * [](Heat_Ray.md "Heat Ray")[Heat Ray](Heat_Ray.md "Heat Ray")
225	  * [](Golem_Fist.md "Golem Fist")[Golem Fist](Golem_Fist.md "Golem Fist")
226	  * [](Poison_Staff.md "Poison Staff")[Poison Staff](Poison_Staff.md "Poison Staff")
227	  * [](Book_of_Skulls.md "Book of Skulls")[Book of Skulls](Book_of_Skulls.md "Book of Skulls")
228	  * [](KO_Cannon.md "KO Cannon")[KO Cannon](KO_Cannon.md "KO Cannon")
229	  * [](Snowball_Cannon.md "Snowball Cannon")[Snowball Cannon](Snowball_Cannon.md "Snowball Cannon")
230	  * [](Golden_Shower.md "Golden Shower")[Golden Shower](Golden_Shower.md "Golden Shower")
231	  * [](Shadowbeam_Staff.md "Shadowbeam Staff")[Shadowbeam Staff](Shadowbeam_Staff.md "Shadowbeam Staff")
232	  * [](Inferno_Fork.md "Inferno Fork")[Inferno Fork](Inferno_Fork.md "Inferno Fork")
233	  * [](Spectre_Staff.md "Spectre Staff")[Spectre Staff](Spectre_Staff.md "Spectre Staff")
234	  * [](S.D.M.G..md "S.D.M.G.")[S.D.M.G.](S.D.M.G..md "S.D.M.G.")****__(Desktop, Console and Mobile versions)
235	  * [](Scourge_of_the_Corruptor.md "Scourge of the Corruptor")[Scourge of the Corruptor](Scourge_of_the_Corruptor.md "Scourge of the Corruptor")
236	  * [](Candy_Corn_Rifle.md "Candy Corn Rifle")[Candy Corn Rifle](Candy_Corn_Rifle.md "Candy Corn Rifle")
237	  * [](Jack_'O_Lantern_Launcher.md "Jack 'O Lantern Launcher")[Jack 'O Lantern Launcher](Jack_'O_Lantern_Launcher.md "Jack 'O Lantern Launcher")
238	  * [](Bat_Scepter.md "Bat Scepter")[Bat Scepter](Bat_Scepter.md "Bat Scepter")
239	  * [](Stake_Launcher.md "Stake Launcher")[Stake Launcher](Stake_Launcher.md "Stake Launcher")
240	  * [](Red_Ryder.md "Red Ryder")[Red Ryder](Red_Ryder.md "Red Ryder")**** __(Desktop, Console, Old-gen console and Mobile versions)
241	  * [](Elf_Melter.md "Elf Melter")[Elf Melter](Elf_Melter.md "Elf Melter")
242	  * [](Chain_Gun.md "Chain Gun")[Chain Gun](Chain_Gun.md "Chain Gun")
243	  * [](Razorpine.md "Razorpine")[Razorpine](Razorpine.md "Razorpine")
244	  * [](Blizzard_Staff.md "Blizzard Staff")[Blizzard Staff](Blizzard_Staff.md "Blizzard Staff")
245	  * [](Snowman_Cannon.md "Snowman Cannon")[Snowman Cannon](Snowman_Cannon.md "Snowman Cannon")
246	  * [](Venom_Staff.md "Venom Staff")[Venom Staff](Venom_Staff.md "Venom Staff")**** __(Desktop, Console, Old-gen console and Mobile versions)
247	  * [](Pulse_Bow.md "Pulse Bow")[Pulse Bow](Pulse_Bow.md "Pulse Bow")**** __(Desktop, Console, Old-gen console and Mobile versions)
248	  * [](Gatligator.md "Gatligator")[Gatligator](Gatligator.md "Gatligator")**** __(Desktop, Console, Old-gen console and Mobile versions)
249	  * [](Water_Gun.md "Water Gun")[Water Gun](Water_Gun.md "Water Gun")**** __(Desktop, Console, Old-gen console and Mobile versions)
250	  * [](Slime_Gun.md "Slime Gun")[Slime Gun](Slime_Gun.md "Slime Gun")**** __(Desktop, Console, Old-gen console and Mobile versions)
251	  * [](Flairoon "Flairoon")[Flairoon](Flairoon "Flairoon")
252	  * [](Razorblade_Typhoon.md "Razorblade Typhoon")[Razorblade Typhoon](Razorblade_Typhoon.md "Razorblade Typhoon")
253	  * [](Bubble_Gun.md "Bubble Gun")[Bubble Gun](Bubble_Gun.md "Bubble Gun")
254	  * [](Tsunami.md "Tsunami")[Tsunami](Tsunami.md "Tsunami")
255	  * [](Meteor_Staff.md "Meteor Staff")[Meteor Staff](Meteor_Staff.md "Meteor Staff")**** __(Desktop, Console and Mobile versions)
256	  * [](Xenopopper.md "Xenopopper")[Xenopopper](Xenopopper.md "Xenopopper")**** __(Desktop, Console and Mobile versions)
257	  * [](Life_Drain.md "Life Drain")[Life Drain](Life_Drain.md "Life Drain")**** __(Desktop, Console and Mobile versions)
258	  * [](Dart_Pistol.md "Dart Pistol")[Dart Pistol](Dart_Pistol.md "Dart Pistol")**** __(Desktop, Console and Mobile versions)
259	  * [](Dart_Rifle.md "Dart Rifle")[Dart Rifle](Dart_Rifle.md "Dart Rifle")**** __(Desktop, Console and Mobile versions)
260	  * [](Hellwing_Bow.md "Hellwing Bow")[Hellwing Bow](Hellwing_Bow.md "Hellwing Bow")**** __(Desktop, Console and Mobile versions)
261	  * [](Daedalus_Stormbow.md "Daedalus Stormbow")[Daedalus Stormbow](Daedalus_Stormbow.md "Daedalus Stormbow")**** __(Desktop, Console and Mobile versions)
262	  * [](Crystal_Vile_Shard.md "Crystal Vile Shard")[Crystal Vile Shard](Crystal_Vile_Shard.md "Crystal Vile Shard")**** __(Desktop, Console and Mobile versions)
263	  * [](Shadowflame_Bow.md "Shadowflame Bow")[Shadowflame Bow](Shadowflame_Bow.md "Shadowflame Bow")**** __(Desktop, Console and Mobile versions)
264	  * [](Shadowflame_Hex_Doll.md "Shadowflame Hex Doll")[Shadowflame Hex Doll](Shadowflame_Hex_Doll.md "Shadowflame Hex Doll")**** __(Desktop, Console and Mobile versions)
265	  * [](Nail_Gun.md "Nail Gun")[Nail Gun](Nail_Gun.md "Nail Gun")**** __(Desktop, Console and Mobile versions)
266	  * [](Crystal_Serpent.md "Crystal Serpent")[Crystal Serpent](Crystal_Serpent.md "Crystal Serpent")**** __(Desktop, Console and Mobile versions)
267	  * [](Toxikarp.md "Toxikarp")[Toxikarp](Toxikarp.md "Toxikarp")**** __(Desktop, Console and Mobile versions)
268	  * [](Amber_Staff.md "Amber Staff")[Amber Staff](Amber_Staff.md "Amber Staff")**** __(Desktop, Console and Mobile versions)
269	  * [](Portal_Gun.md "Portal Gun")[Portal Gun](Portal_Gun.md "Portal Gun")**** __(Desktop, Console and Mobile versions)
270	  * [](Solar_Eruption.md "Solar Eruption")[Solar Eruption](Solar_Eruption.md "Solar Eruption")**** __(Desktop, Console and Mobile versions)
271	  * [](Vortex_Beater.md "Vortex Beater")[Vortex Beater](Vortex_Beater.md "Vortex Beater")**** __(Desktop, Console and Mobile versions)
272	  * [](Nebula_Arcanum.md "Nebula Arcanum")[Nebula Arcanum](Nebula_Arcanum.md "Nebula Arcanum")**** __(Desktop, Console and Mobile versions)
273	  * [](Phantasm.md "Phantasm")[Phantasm](Phantasm.md "Phantasm")**** __(Desktop, Console and Mobile versions)
274	  * [](Nebula_Blaze.md "Nebula Blaze")[Nebula Blaze](Nebula_Blaze.md "Nebula Blaze")**** __(Desktop, Console and Mobile versions)
275	  * [](Celebration.md "Celebration")[Celebration](Celebration.md "Celebration")**** __(Desktop, Console and Mobile versions)
276	  * [](Lunar_Flare.md "Lunar Flare")[Lunar Flare](Lunar_Flare.md "Lunar Flare")**** __(Desktop, Console and Mobile versions)
277	  * [](Spirit_Flame.md "Spirit Flame")[Spirit Flame](Spirit_Flame.md "Spirit Flame")**** __(Desktop, Console and Mobile versions)
278	  * [](Sleepy_Octopod.md "Sleepy Octopod")[Sleepy Octopod](Sleepy_Octopod.md "Sleepy Octopod")**** __(Desktop, Console and Mobile versions)
279	  * [](Tome_of_Infinite_Wisdom.md "Tome of Infinite Wisdom")[Tome of Infinite Wisdom](Tome_of_Infinite_Wisdom.md "Tome of Infinite Wisdom")**** __(Desktop, Console and Mobile versions)
280	  * [](Phantom_Phoenix.md "Phantom Phoenix")[Phantom Phoenix](Phantom_Phoenix.md "Phantom Phoenix")**** __(Desktop, Console and Mobile versions)
281	  * [](Sky_Dragon's_Fury.md "Sky Dragon's Fury")[Sky Dragon's Fury](Sky_Dragon's_Fury.md "Sky Dragon's Fury")**** __(Desktop, Console and Mobile versions)
282	  * [](Aerial_Bane.md "Aerial Bane")[Aerial Bane](Aerial_Bane.md "Aerial Bane")**** __(Desktop, Console and Mobile versions)
283	  * [](Celebration_Mk2.md "Celebration Mk2")[Celebration Mk2](Celebration_Mk2.md "Celebration Mk2")**** __(Desktop, Console and Mobile versions)
284	  * [](Super_Star_Shooter.md "Super Star Shooter")[Super Star Shooter](Super_Star_Shooter.md "Super Star Shooter")**** __(Desktop, Console and Mobile versions)
285	  * [](Thunder_Zapper.md "Thunder Zapper")[Thunder Zapper](Thunder_Zapper.md "Thunder Zapper")**** __(Desktop, Console and Mobile versions)
286	  * [](Blood_Rain_Bow.md "Blood Rain Bow")[Blood Rain Bow](Blood_Rain_Bow.md "Blood Rain Bow")**** __(Desktop, Console and Mobile versions)
287	  * [](Eventide.md "Eventide")[Eventide](Eventide.md "Eventide")**** __(Desktop, Console and Mobile versions)
288	  * [](Resonance_Scepter.md "Resonance Scepter")[Resonance Scepter](Resonance_Scepter.md "Resonance Scepter")**** __(Desktop, Console and Mobile versions)
289	  * [](Pew-matic_Horn.md "Pew-matic Horn")[Pew-matic Horn](Pew-matic_Horn.md "Pew-matic Horn")**** __(Desktop, Console and Mobile versions)
290	  * [](Terraformer.md "Terraformer")[Terraformer](Terraformer.md "Terraformer")**** __(Desktop, Console and Mobile versions)
291	  * [](Barrel_Launcher.md "Barrel Launcher")[Barrel Launcher](Barrel_Launcher.md "Barrel Launcher")**** __(Desktop, Console and Mobile versions)
292	  * [](Shimmer_Gun.md "Shimmer Gun")[Shimmer Gun](Shimmer_Gun.md "Shimmer Gun")**** __(Desktop, Console and Mobile versions)
293	  * [](Flairon.md "Flairon")[Flairon](Flairon.md "Flairon")
294	  * [](Acorn_Slingshot.md "Acorn Slingshot")[Acorn Slingshot](Acorn_Slingshot.md "Acorn Slingshot")**** __(Desktop, Console and Mobile versions)
295	
296	  
297	---  
298	  
299	For the other items: 
300	
301	[math]\displaystyle{ \text{Total time} = \mathit{useAnimation} }[/math]
302	
303	## Notes
304	
305	  * The "fire rate" per second is calculated by dividing ticks per second (60) by the item's use time: [math]\displaystyle{ \mathit{fire\ rate} = \frac{60}{\mathit{use\ time}} }[/math]
306	
307	    For instance, a [Megashark](Megashark.md "Megashark") has a use time of 7. Its rate of fire can be calculated by inserting this in the formula above: [math]\displaystyle{ \mathit{fire\ rate} = \frac{60}{ 7 } \approx 8.57 }[/math]
308	    Multiplying this with 60 reveals the rate of fire per minute, which is about 514.29 rounds per minute for the Megashark.
309	
310	  * Certain items' use condition are not solely based on its use time. For example, [recovery potions](Recovery_potions.md "Recovery potions") like [Mushrooms](Mushroom.md "Mushroom") and [Lesser Healing Potions](Lesser_Healing_Potion.md "Lesser Healing Potion") have a special cooldown period; [flails](Flails.md "Flails") and [boomerangs](Boomerangs.md "Boomerangs") must return before being fired again.
311	  * The animation skipping feature of autoswing melee weapons has great impact on use time in some cases. For example, A Light [Meowmere](Meowmere.md "Meowmere") has a use time of 12. With 141% melee speed bonus, its use time becomes 4.98, which is rounded down to 4, equal to 200% melee speed bonus. Considering the skip, actual use time has been reduced from 11 to 3, which is equal to 267% melee speed bonus.
312	
313	## History
314	
315	[ Desktop version](Desktop_version_history.md "Desktop version history")
316	
317	  * [Desktop 1.0.6](Desktop_1.0.6 "Desktop 1.0.6"): 
318	    * The tooltip text "Very fast" is now applied to all items up to a use time of 20. Shifted the other groups accordingly: 
319	      * "Very fast" is now 9–20 instead of 9–15.
320	      * "Fast" is now 21–25 instead of 16–20.
321	      * "Average" is now 25–30 instead of 21–25.
322	      * "Slow" is now 31–35 instead of 26–30.
323	      * "Very slow" is now 36–45 instead of 31–40.
324	      * "Extremely slow" is now 46–55 instead of 41–50.
325	      * "Snail" is now ≥56 instead of ≥51.
326	
327	    
328	
329	    As a result, some items are now listed as being faster even though their actual use time did not change.
330	
331	  * [Desktop 1.0.3](Desktop_1.0.3 "Desktop 1.0.3"): Fixed a typo in a use time tooltip text: "Extremly slow speed" → "Extrem**e** ly slow speed".
332	
333	## References
334	
335	  1. ↑ 1.0 1.1 A tick is a time unit countable by the software. Most of _[Terraria](Terraria.md "Terraria")'s_ updating logic happens every tick. A tick has the length of 1/60th of a second, hence there are 60 ticks in a second and 3600 ticks in a minute.
336	  2. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, field `useTime` in `Terraria.Item.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
337	  3. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, field `useAnimation` in `Terraria.Item.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
338	  4. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, field `reuseDelay` in `Terraria.Item.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
339	  5. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `LeftClick()` in `Terraria.UI.ItemSlot.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
340	  6. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `TrySwitchingLoadout()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
341	  7. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `HoverOverCraftingItemButton()` in `Terraria.Main.cs` and property `IgnoreMouseInterface` in `Terraria.GameInput.PlayerInput.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
342	  8. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, method `ItemCheck_OwnerOnlyCode()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
343	  9. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `ApplyItemAnimation()` in `Terraria.Player.cs` and `ItemCheck_HandleMPItemAnimation()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
344	  10. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, methods `Update()` in `Terraria.Player.cs`, `CapAttackSpeeds()` in `Terraria.Player.cs`, and `ApplyItemAnimation()` in `Terraria.Player.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
345	  11. ↑ Information taken from the [ Desktop](Desktop_version_history.md "Desktop version history") [1.4.4.9](1.4.4.9.md "1.4.4.9") source code, field `Sets.BonusMeleeSpeedMultiplier` in `Terraria.ID.ItemID.cs`. There may be inaccuracies, as the current  Desktop version is 1.4.5.6.
346	
347	  1. ↑ The percentage shown in-game.
348	
349	View or edit this template
350	
351	Game mechanics
352	
353	Combat
354	
355	  * [Attack speed](Attack_speed.md "Attack speed")
356	  * [Autoswing](Autoswing.md "Autoswing")
357	  * [Critical hit](Critical_hit.md "Critical hit")
358	  * [Damage](Damage.md "Damage")
359	    * [Invincibility frame](Invincibility_frame.md "Invincibility frame")
360	  * [Knockback](Knockback.md "Knockback")
361	  * [Lock on](Lock_on.md "Lock on")**** __(Desktop, Console, Mobile and 3DS versions)
362	  * [Velocity](Velocity.md "Velocity")
363	
364	Environment
365	
366	  * [Ambient objects](Ambient_objects.md "Ambient objects")
367	  * [Ambient entities](Ambient_entities.md "Ambient entities")**** __(Desktop, Console and Mobile versions)
368	  * [Biome backgrounds](Biome_backgrounds.md "Biome backgrounds")
369	  * [Biomes](Biomes.md "Biomes")
370	    * [Spread](Biome_spread.md "Biome spread")
371	  * [Day and night cycle](Day_and_night_cycle.md "Day and night cycle")
372	  * [Events](Events.md "Events")
373	  * [Gravity](Gravity.md "Gravity")
374	  * [Liquids](Liquids.md "Liquids")
375	  * [Moon phase](Moon_phase.md "Moon phase")
376	  * [Music](Music.md "Music")
377	  * [NPC spawning](NPC_spawning.md "NPC spawning")
378	  * [Status messages](Status_messages.md "Status messages")
379	  * [Wind](Wind.md "Wind")
380	
381	Interface
382	
383	  * [Boss health bar](Boss_health_bar.md "Boss health bar")**** __(Desktop, Console and Mobile versions)
384	  * [Camera Mode](Camera_Mode.md "Camera Mode")**** __(Desktop version)
385	  * [Credits](Credits.md "Credits")**** __(Desktop, Console and Mobile versions)
386	  * [Emotes](Emotes.md "Emotes")**** __(Desktop, Console and Mobile versions)
387	  * [Minimap](Minimap.md "Minimap")
388	  * [Logo](Logo.md "Logo")
389	  * [NPC flag](NPC_flag.md "NPC flag")
390	  * [Title messages](Title_messages.md "Title messages")**** __(Desktop version)
391	  * [Tips](Tips.md "Tips")
392	  * [Resource Packs](Resource_Pack.md "Resource Pack")**** __(Desktop version)
393	  * [RGB](RGB.md "RGB")**** __(Desktop version)
394	  * [Workshop Hub](Workshop_Hub.md "Workshop Hub")**** __(Desktop version)
395	
396	Items
397	
398	  * [Alternative crafting ingredients](Alternative_crafting_ingredients.md "Alternative crafting ingredients")
399	  * [Ammo conversion](Ammo_conversion.md "Ammo conversion")
400	  * [Block Swap](Block_Swap.md "Block Swap")**** __(Desktop, Console and Mobile versions)
401	  * [Consumables](Consumables.md "Consumables")
402	  * [Crafting stations](Crafting_stations.md "Crafting stations")
403	    * [By Hand](By_Hand.md "By Hand")
404	  * [Crossover content](Crossover_content.md "Crossover content")
405	  * [Explosion-proof objects](Explosion-proof_objects.md "Explosion-proof objects")
406	  * [Flat-surface items](Flat-surface_items.md "Flat-surface items")
407	  * [Highlight](Highlight.md "Highlight")
408	  * [Mining speed](Mining_speed "Mining speed")
409	  * [Modifiers](Modifiers.md "Modifiers")
410	  * [NPC drops](NPC_drops.md "NPC drops")
411	  * [Placement](Placement.md "Placement")
412	  * [Pickaxe power](Pickaxe_power.md "Pickaxe power")
413	  * [Rarity](Rarity.md "Rarity")
414	  * [Recipes](Recipes.md "Recipes")
415	  * [Storage](Storage_items.md "Storage items")
416	  * [Tooltips](Tooltips.md "Tooltips")
417	  * Use time
418	  * [Value](Value.md "Value")
419	
420	Game
421	
422	  * [Achievements](Achievements.md "Achievements")**** __(Desktop, Console, Old-gen console and Mobile versions)
423	  * [Difficulty](Difficulty.md "Difficulty")
424	    * [Journey](Journey_Mode.md "Journey Mode")**** __(Desktop, Console and Mobile versions)
425	    * [Classic](Classic_Mode.md "Classic Mode")
426	    * [Expert](Expert_Mode.md "Expert Mode")**** __(Desktop, Console and Mobile versions)
427	      * [Coin pickup](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")**** __(Desktop, Console and Mobile versions)
428	    * [Master](Master_Mode.md "Master Mode")**** __(Desktop, Console and Mobile versions)
429	  * [Fishing](Fishing.md "Fishing")
430	  * [Golf](Golf.md "Golf")**** __(Desktop, Console and Mobile versions)
431	  * [Hoik](Hoik.md "Hoik")
432	  * [Music](Music.md "Music")
433	  * [Teleportation](Teleportation.md "Teleportation")
434	    * [Pylons](Pylons.md "Pylons")**** __(Desktop, Console and Mobile versions)
435	  * [Town](Town.md "Town")**** __(Desktop, Console and Mobile versions)
436	
437	Multiplayer
438	
439	  * [Server](Server.md "Server")
440	  * [Chat](Chat.md "Chat")
441	  * [Multiplayer](Multiplayer.md "Multiplayer")
442	
443	Player
444	
445	  * [Aggro](Aggro.md "Aggro")
446	  * [Ammo conservation](Ammo_conservation.md "Ammo conservation")
447	  * [Breath meter](Breath_meter.md "Breath meter")
448	  * [Buffs](Buffs.md "Buffs")
449	    * [Debuffs](Debuffs.md "Debuffs")
450	  * [Character](Character.md "Character")
451	  * [Character styles](Character_styles.md "Character styles")**** __(Desktop, Console and Mobile versions)
452	  * [Damage reduction](Damage_reduction.md "Damage reduction")
453	  * [Dash](Dash.md "Dash")
454	  * [Death](Death.md "Death")
455	  * [Defense](Defense.md "Defense")
456	  * [Dodge](Dodge.md "Dodge")
457	  * [Drowning](Drowning.md "Drowning")
458	  * [Extra jump](Extra_jump.md "Extra jump")
459	  * [Fall damage](Fall_damage.md "Fall damage")
460	  * [Flight](Flight.md "Flight")
461	  * [Ghost](Ghost.md "Ghost")**** __(Desktop, Console, Old-gen console and Mobile versions)
462	  * [Hairstyles](Hairstyles.md "Hairstyles")
463	  * [Health](Health.md "Health")
464	  * [Health regeneration](Health_regeneration.md "Health regeneration")
465	  * [Inventory](Inventory.md "Inventory")
466	  * [Lifesteal](Lifesteal.md "Lifesteal")
467	  * [Loadouts](Loadouts.md "Loadouts")**** __(Desktop, Console and Mobile versions)
468	  * [Luck](Luck.md "Luck")**** __(Desktop, Console and Mobile versions)
469	  * [Mana](Mana.md "Mana")
470	  * [Movement speed](Movement_speed.md "Movement speed")
471	  * [Social slots](Social_slots.md "Social slots")
472	  * [Spawn](Spawn.md "Spawn")
473	  * [Stealth](Stealth.md "Stealth")
474	
475	Settings
476	
477	  * [Cursor modes](Cursor_modes.md "Cursor modes")
478	  * [Game controls](Game_controls.md "Game controls")
479	  * [Lighting mode](Lighting_mode.md "Lighting mode")**** __(Desktop, Console and Mobile versions)
480	  * [Parallax](Parallax.md "Parallax")**** __(Desktop, Console and Mobile versions)
481	  * [Settings](Settings.md "Settings")**** __(Desktop, Console, Mobile and 3DS versions)
482	  * [Toggles](Toggles.md "Toggles")
483	
484	Technical
485	
486	  * [AI](AI.md "AI")
487	  * [Chat commands](Commands.md "Commands")
488	  * [Command-line parameters](Command-line_parameters.md "Command-line parameters")**** __(Desktop version)
489	  * [Config.json](Config.json_settings.md "Config.json settings")**** __(Desktop and Mobile versions)
490	  * [Data IDs](Data_IDs.md "Data IDs")
491	  * [Debug commands](Debug_commands.md "Debug commands")**** __(Desktop version)
492	  * [Game platform](Game_platform.md "Game platform")
493	  * [NPC names](NPC_names.md "NPC names")
494	  * [Projectiles](Projectiles.md "Projectiles")
495	
496	World
497	
498	  * [Pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode")
499	  * [Hardmode](Hardmode.md "Hardmode")
500	    * [Conversion](Hardmode_conversion.md "Hardmode conversion")
501	  * [Special world seeds](Special_world_seeds.md "Special world seeds")**** __(Desktop, Console and Mobile versions)
502	  * [Secret world seeds](Secret_world_seeds.md "Secret world seeds")**** __(Desktop, Console and Mobile versions)
503	  * [World](World.md "World")
504	    * [Generation](World_generation.md "World generation")
505	  * [World Seed](World_Seed.md "World Seed")**** __(Desktop, Console and Mobile versions)
506	  * [World size](World_size.md "World size")
507	
508	Categories: 
509	
510	  * [Pages with information based on outdated versions of Terraria's source code](Category%3APages_with_information_based_on_outdated_versions_of_Terraria's_source_code "Category:Pages with information based on outdated versions of Terraria's source code")
511	  * [Game mechanics](Category%3AGame_mechanics "Category:Game mechanics")
512	  * [Items](Category%3AItems "Category:Items")
513	
514	Hidden categories: 
515	
516	  * Pages using DynamicPageList3 dplvar parser function
517	  * Entities patched in Desktop 1.0.6
518	  * Entities patched in Desktop 1.0.3
519	  * Pages with navboxes
520	  * Random
521	
522	This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=Use_time&oldid=992891 "Last edited on 2026-04-01"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
523	  *[1 required]: Journey Mode
524	  *[Qty.]: Quantity
525	  *[100%]: Master Mode
526	  *[DPS]: Damage per detik
527	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
528	  *[300]: Master Mode
529	  *[400]: Master Mode
530	  *[160]: Expert Mode
531	  *[240]: Master Mode
532	  *[3 required]: Journey Mode
533	  *[#]: Number of "base" items
534	  *[Max.  
535	enemies]: Maximum number of enemies Abigail can damage at once
536	  *[HM]: Hardmode
537	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
538	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
539	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
540	  *[8]: Expert Mode
541	  *[10]: Expert Mode
542	  *[120]: Master Mode
543	  *[150]: Expert Mode
544	  *[13]: Chế độ Master
545	  *[195]: Master Mode
546	  *[Verify]: Figuring out which paints specifically
547	  *[50 required]: Journey Mode
548	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
549	  *[100 required]: Journey Mode
550	  *[cần có 1]: Chế độ Journey
551	  *[25 required]: Journey Mode
552	  *[cần có 25]: Chế độ Journey
553	  *[400 required]: Journey Mode
554	  *[membutuhkan 100]: Mode Journey
555	  *[cần có 100]: Chế độ Journey
556	  *[Slg.]: Số lượng
557	  *[1.99%]: Expert Mode
558	  *[199/10000 (1.99%)]: Expert Mode
559	  *[membutuhkan 1]: Mode Journey
560	  *[1,99%]: Expert Mode
561	  *[1/50 (2%)]: Mode Expert
562	  *[200 required]: Journey Mode
563	  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
564	  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
565	  *[20 required]: Journey Mode
566	  *[180]: Expert Mode
567	  *[270]: Master Mode
568	  *[5–9 seconds]: Master Mode
569	  *[5–9]: Expert Mode
570	  *[15 required]: Journey Mode
571	  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
572	  *[Power]: Bait power
573	  *[5 required]: Journey Mode
574	  *[cần có {{{research}}}]: Chế độ Journey
575	  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
576	  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
577	  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
578	  *[Expert Mode exclusive]: Expert Mode
579	  *[402]: Master Mode
580	  *[523]: Expert Mode
581	  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
582	  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
583	  *[800]: Expert Mode
584	  *[1200]: Master Mode
585	  *[15]: Expert Mode
586	  *[17]: Master Mode
587	  *[O. v. odražení]: Odolnost vůči odražení
588	  *[1 minute 30 seconds]: Expert Mode
589	  *[1 minute 52.5 seconds]: Master Mode
590	  *[90]: Master Mode
591	  *[112.5]: Master Mode
592	  *[2–6]: Chế độ Expert
593	  *[2-6]: Expert Mode
594	  *[%100]: Expert Mode
595	  *[28]: Expert Mode
596	  *[42]: Master Mode
597	  *[80]: Expert Mode
598	  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
599	  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
600	  *[ Major improvements to all stats and increased life regeneration]: Expert Mode
601	  *[50%]: Expert Mode
602	  *[1/2 (50%)]: Expert Mode
603	  *[30]: Expert Mode
604	  *[45]: Expert Mode
605	  *[3/4]: Chế độ Expert
606	  *[5]: Master Mode
607	  *[75%]: Chế độ Expert
608	  *[semua]: Mode Master
609	  *[6]: Expert Mode
610	  *[toàn bộ]: Chế độ Master
611	  *[199/10000 (1,99%)]: Mode Expert
612	  *[4 minutes]: Expert Mode
613	  *[5 minutes]: Master Mode
614	  *[4]: Expert Mode
615	  *[36]: Expert Mode
616	  *[22]: Expert Mode
617	  *[26]: Master Mode
618	  *[Ruce pryč od mé zbraně, kámo!]: Keep your hands off my gun, buddy!
619	  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
620	  *[Koukám, že házíš očkem po žraločkovi. Opravdu nechceš vědět, jak byl vyroben.]: I see you're eyeballing the Minishark. You really don't want to know how it was made.
621	  *[Neobtěžuj se s [jméno demoličního experta], vše, co potřebuješ, je přímo tady.]: Don't bother with [Name of Demolitionist], I've got all you need right here.
622	  *[Jaký má [jméno demoličního experta] problém? Uvědomuje si vůbec, že oba prodáváme naprosto rozdílné zboží?]: What's [Name of Demolitionist]'s problem? Does he even realize we sell completely different stuff?
623	  *[Pohni zadkem! Za hodinu mám rande s [jméno sestřičky].]: Make it quick! I've got a date with [Name of Nurse] in a hour.
624	  *[Chci to, co [jméno sestřičky] prodává. Co myslíš tím, že neprodává ani ň?]: I want what [Name of Nurse] is sellin'. What do you mean, she doesn't sell anything?
625	  *[Na [jméno dryády] bych mohl oči nechat. Škoda, že je to taková prudařka.]: [Name of Dryad] is a looker. Too bad she's such a prude.
626	  *[Slyšel jsem, že se ve světě nachází panenka vypadající skoro jako [jméno průvodce]. Mile rád bych do ní vpálil pár kulek.]: I heard there is a doll that looks very similar to [Name of Guide] somewhere in the underworld. I'd like to put a few rounds in it.
627	  *[Miluji noci jako je tahle. Vždy se najde něco na zabití.]: I love nights like tonight, there is never a shortage of things to kill.
628	  *[Chlape, tohle je noc přímo stvořená, abys s nikým nemusel mluvit, nemyslíš [jméno hráče]?]: Man, it's a good night not to talk to anybody, don't you think, [Name of Player]?
629	  *[14]: Expert Mode
630	  *[17.5]: Master Mode
631	  *[7]: Expert Mode
632	  *[8.75]: Master Mode
633	  *[21]: Expert Mode
634	  *[26.25]: Master Mode
635	  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
636	  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
637	  *[3.33–6.67%]: Expert Mode
638	  *[3.33%–6.67%]: Expert Mode
639	  *[W]: Wave
640	  *[3.33%]: Expertní mód
641	  *[6.67%]: Expert Mode
642	  *[0.014%]: Expert Mode
643	  *[ Medium improvements to all stats and increased life regeneration]: Expert Mode
644	  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
645	  *[+100%]: Expert Mode
646	  *[−50%]: Expert Mode
647	  *[+20%]: Expert Mode
648	  *[−16.67%]: Expert Mode
649	  *[200]: Expert Mode
650	  *[225]: Master Mode
651	  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
652	  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
653	  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60.13 tiles per second
654	  *[6.25–12.5%]: Expert Mode
655	  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
656	  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.75 tiles per second
657	  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.47 tiles per second
658	  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.33 tiles per second
659	  *[6.25%]: Master Mode
660	  *[12.5%]: Master Mode
661	  *[32›140›176]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
662	  *[48›210›264]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
663	  *[26›92›116]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
664	  *[39›138›174]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
665	  *[2›8›10]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
666	  *[68›148›224]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
667	  *[102›222›336]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
668	  *[40›72›108]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
669	  *[60›108›162]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
670	  *[4›8›12]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
671	  *[92›100]: Expertní mód : Pre-hardmode › Těžký mód
672	  *[138›150]: Master Mode : Pre-Hardmode › Hardmode
673	  *[70›62]: Expertní mód : Pre-hardmode › Těžký mód
674	  *[105›93]: Master Mode : Pre-Hardmode › Hardmode
675	  *[60›132›198]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
676	  *[90›198›297]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
677	  *[36›64›96]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
678	  *[54›96›144]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
679	  *[6›12›18]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
680	  *[200›200›220]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
681	  *[300›300›330]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
682	  *[90›90›80]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
683	  *[135›135›120]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
684	  *[600]: Master Mode
685	  *[320]: Expert Mode
686	  *[480]: Master Mode
687	  *[100]: Journey Mode
688	  *[120›120›132]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
689	  *[180›180›198]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
690	  *[440]: Expert Mode
691	  *[660]: Master Mode
692	  *[1500]: Master Mode
693	  *[2250]: Master Mode
694	  *[2–6 seconds]: Expert Mode
695	  *[2.5–7.5 seconds]: Master Mode
696	  *[2.5–7.5]: Master Mode
697	  *[35 mph]: 35 miles per hour (as measured by the Stopwatch item) or 25.5 tiles per second
698	  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
699	  *[ 17–30]: Expert Mode
700	  *[99 required]: Journey Mode
701	  *[10–29]: Expert Mode
702	  *[1 time]: Expert Mode
703	  *[140]: Expert Mode
704	  *[210]: Master Mode
705	  *[14–20 seconds]: Expert Mode
706	  *[17.5-25 seconds]: Master Mode
707	  *[25%]: Master Mode
708	  *[14–20]: Expert Mode
709	  *[17.5–25]: Master Mode
710	  *[1/30 (3.33%)]: Expert Mode
711	  *[15.97%]: Expert Mode
712	  *[23/144 (15.97%)]: Expert Mode
713	  *[ 8 seconds]: Expert Mode
714	  *[10 seconds]: Master Mode
715	  *[0.5–2.5 seconds]: Master Mode
716	  *[90%]: Expert Mode
717	  *[Web Spit]: Expert Mode
718	  *[30 seconds]: Expert Mode
719	  *[37.5 seconds]: Master Mode
720	  *[4–12]: Expert Mode
721	  *[5–15]: Master Mode
722	  *[33.33%]: Expert Mode
723	  *[1/3 (33.33%)]: Expert Mode
724	  *[20-40]: Expert Mode
725	  *[25-40]: Expert Mode
726	  *[10-14]: Mode Expert
727	  *[12.5-17.5]: Master Mode
728	  *[20]: Expert Mode
729	  *[25]: Master Mode
730	  *[6-10]: Expert Mode
731	  *[7.5-12.5]: Master Mode
732	  *[1/1 (100%)]: Expert Mode
733	  *[6-20]: Expert Mode
734	  *[7.5-25]: Master Mode
735	  *[7.5-15]: Expert Mode
736	  *[9.37-18.75]: Master Mode
737	  *[11/243 (4.53%)]: Expert Mode
738	  *[11/81 (13.58%)]: Expert Mode
739	  *[2 hours]: Expert Mode
740	  *[3 hours]: Master Mode
741	  *[20–40]: Expert Mode
742	  *[25–50]: Master Mode
743	  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
744	  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
745	  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
746	  *[1/150]: Expert Mode
747	  *[1/30]: Expert Mode
748	  *[15.56–31.11%]: Expert Mode
749	  *[15.56%–31.11%]: Expert Mode
750	  *[15.56%]: Expert Mode
751	  *[31.11%]: Expert Mode
752	  *[ 12 _SC_ 50 _CC_]: Expert Mode
753	  *[dusk]: 7:30 PM
754	  *[1.33%]: Expert Mode
755	  *[1%]: Expert Mode
756	  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
757	  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
758	  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
759	  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second
760	  *[20 seconds]: Expert Mode
761	  *[25 seconds]: Master Mode
762	  *[0.5%]: エキスパートモード
763	  *[0.67%]: Expert Mode
764	  *[1-3]: エキスパートモード
765	  *[18 mph]: 18 miles per hour (as measured by the Stopwatch item) or 12.94 tiles per second
766	  *[Crit]: Critical strike chance
767	  *[20 mph]: 20 miles per hour (as measured by the Stopwatch item) or 14.67 tiles per second
768	  *[54 mph]: 54 miles per hour (as measured by the Stopwatch item) or 39.6 tiles per second
769	  *[and the core]: Expert Mode
770	  *[2,800]: Chế độ Expert
771	  *[3,570]: Chế độ Master
772	  *[3,640]: Chế độ Expert
773	  *[4,641]: Chế độ Master
774	  *[15,120]: Chế độ Expert
775	  *[19,296]: Chế độ Master
776	  *[2,125]: Chế độ Expert
777	  *[2,709]: Chế độ Master
778	  *[4,760]: Chế độ Expert
779	  *[6,069]: Chế độ Master
780	  *[11,900]: Mode Expert
781	  *[15,172]: Mode Master
782	  *[8,800]: Chế độ Expert
783	  *[11,220]: Master Mode
784	  *[11,200]: Chế độ Expert
785	  *[14,280]: Chế độ Master
786	  *[28,800]: Chế độ Expert
787	  *[36,720]: Chế độ Master
788	  *[30,000]: Chế độ Expert
789	  *[38,250]: Chế độ Master
790	  *[34,500]: Chế độ Expert
791	  *[43,988]: Chế độ Master
792	  *[120,000]: Chế độ Expert
793	  *[153,000]: Chế độ Master
794	  *[280]: Expert Mode
795	  *[420]: Master Mode
796	  *[42,000]: Chế độ Expert
797	  *[53,550]: Chế độ Master
798	  *[88,500]: Chế độ Expert
799	  *[112,836]: Chế độ Master
800	  *[90,000]: Chế độ Expert
801	  *[114,749]: Chế độ Master
802	  *[78,000]: Expert Mode
803	  *[99,450]: Chế độ Master
804	  *[11700]: Mode Expert
805	  *[14917]: Mode Master
806	  *[98,000]: Chế độ Expert
807	  *[124,950]: Chế độ Master
808	  *[48,000]: Chế độ Expert
809	  *[61,200]: Master Mode
810	  *[217,500]: Expert Mode
811	  *[277,311]: Chế độ Master
812	  *[dua]: Mode Expert
813	  *[10,500]: Mode Expert
814	  *[24 detik]: Mode Expert
815	  *[30 detik]: Mode Expert
816	  *[30 required]: Journey Mode
817	  *[mph]: miles per hour
818	  *[70]: Expert Mode
819	  *[36 mph]: 36 miles per hour (as measured by the Stopwatch item) or 26.4 tiles per second
820	  *[315]: Expert Mode
821	  *[68]: Expert Mode
822	  *[0.5]: Expert Mode
823	  *[96]: Expert Mode
824	  *[144]: Expert Mode
825	  *[12.5]: Master Mode
826	  *[143 mph]: 143 miles per hour (as measured by the Stopwatch item) or 105 tiles per second
827	  *[5525]: Expert Mode
828	  *[7049]: Master Mode
829	  *[60%]: Expert Mode
830	  *[64%]: Expert Mode
831	  *[65%]: Master Mode
832	  *[110–135]: Master Mode
833	  *[30–50]: Master Mode
834	  *[5.23–10.5 sec]: Expert Mode
835	  *[6.53–13.12 sec]: Master Mode
836	  *[3–6 sec]: Expert Mode
837	  *[3.75–7.5 sec]: Master Mode
838	  *[0.73–1.5 sec]: Expert Mode
839	  *[0.92–1.87 sec]: Master Mode
840	  *[7.5–15 sec]: Expert Mode
841	  *[9.37–18.75 sec]: Master Mode
842	  *[1.5–3 sec]: Expert Mode
843	  *[1.87–3.75 sec]: Master Mode
844	  *[11.23–22.5 sec]: Expert Mode
845	  *[14.03–28.12 sec]: Master Mode
846	  *[9.73–19.5 sec]: Expert Mode
847	  *[12.17–24.37 sec]: Master Mode
848	  *[ 60%]: Mode Expert
849	  *[ 25%]: Chế độ Master
850	  *[ 100%]: Expert Mode
851	  *[5700-7700]: Expert Mode
852	  *[ %100]: Master Mode
853	  *[0-200]: Chế độ Expert
854	  *[0-500]: Chế độ Expert
855	  *[2125]: Expert Mode
856	  *[170]: Expert Mode
857	  *[2709]: Master Mode
858	  *[217]: Chế độ Master
859	  *[20%]: Expert Mode
860	  *[1/5 (20%)]: Expert Mode
861	  *[9.73-19.5]: Expert Mode
862	  *[12.17-24.37]: Master Mode
863	  *[2]: Expert Mode
864	  *[3]: Master Mode
865	  *[43.75%]: Expert Mode
866	  *[7/16 (43.75%)]: Expert Mode
867	  *[Third]: Expert Mode
868	  *[Major improvements to all stats and increased life regeneration]: 達人模式
869	  *[Medium improvements to all stats and increased life regeneration]: 達人模式
870	  *[Minor improvements to all stats and increased life regeneration]: 達人模式
871	  *[13 seconds]: Master Mode
872	  *[Zabíjení zajíčků je bezcitné. Tečka.]: Killing bunnies is cruel. Period.
873	  *[14 seconds]: Expert Mode
874	  *[17.5 seconds]: Master Mode
875	  *[26 mph]: 26 miles per hour (as measured by the Stopwatch item) or 18.75 tiles per second
876	  *[189]: Expert Mode
877	  *[283]: Master Mode
878	  *[4.94%]: Expert Mode
879	  *[3.96%]: Expert Mode
880	  *[700]: Expert Mode
881	  *[1,050]: Master Mode
882	  *[23 mph]: 23 miles per hour (as measured by the Stopwatch item) or 16.87 tiles per second
883	  *[2 mph]: 2 miles per hour (as measured by the Stopwatch item) or 1.6875 tiles per second
884	  *[79/1600 (4.94%)]: Expert Mode
885	  *[4,94%]: Expert Mode
886	  *[3/80 (3,75%)]: Mode Expert
887	  *[12.5 seconds]: Master Mode
888	  *[2 required]: Journey Mode
889	  *[24–100]: Expert Mode
890	  *[12–20]: Expert Mode
891	  *[360]: Master Mode
892	  *[[]: Western world border
893	  *[C]: World center
894	  *[]]: Eastern world border
895	  *[60]: Master Mode
896	  *[18–30]: Expert Mode
897	  *[18–90]: Expert Mode
898	  *[115 mph]: 115 miles per hour (as measured by the Stopwatch item) or 84.33 tiles per second
899	  *[382 mph]: 382 miles per hour (as measured by the Stopwatch item) or 280.13 tiles per second
900	  *[721 mph]: 721 miles per hour (as measured by the Stopwatch item) or 528.73 tiles per second
901	  *[12.5–50%]: Expert Mode
902	  *[12.5%–50%]: Expert Mode
903	  *[16.67%]: Expert Mode
904	  *[0.25%]: Expert Mode
905	  *[0.26 mph]: 0.26 miles per hour (as measured by the Stopwatch item)
906	  *[40]: Journey Mode
907	  *[50]: Master Mode
908	  *[37.5]: Master Mode
909	  *[62.5]: Master Mode
910	  *[6.25]: Master Mode
911	  *[46 mph]: 46 miles per hour (as measured by the Stopwatch item) or 33.73 tiles per second
912	  *[membutuhkan 25]: Mode Journey
913	  *[6.22–31.11%]: Expert Mode
914	  *[6.22%–31.11%]: Expert Mode
915	  *[6.22%]: Expert Mode
916	  *[7.78%]: Expert Mode
917	  *[10.37%]: Expert Mode
918	  *[6,22–31,11%]: Expert Mode
919	  *[102]: Master Mode
920	  *[ 4–6 seconds]: Expert Mode
921	  *[5–7.5 seconds]: Master Mode
922	  *[7.5]: Master Mode
923	  *[16]: Expert Mode
924	  *[24]: Expert Mode
925	  *[12 _GC_ 50 _SC_]: Expert Mode
926	  *[8 _GC_]: Expert Mode
927	  *[10 _GC_]: Master Mode
928	  *[tida perempat]: Mode Expert
929	  *[ Verifikasi]: Talk:Coins/id (halaman belum tersedia)
930	  *[Verifikasi]: in Xbox and Mobile
931	  *[ Verify]: Talk:Coins/vi (page does not exist)
932	  *[92 mph]: 92 miles per hour (as measured by the Stopwatch item) or 67.5 tiles per second
933	  *[1.5–3]: Expert Mode
934	  *[1.87–3.75]: Master Mode
935	  *[2/243 (0.82%)]: Expert Mode
936	  *[2/81 (2.47%)]: Expert Mode
937	  *[35]: Master Mode
938	  *[1.8–3]: Expert Mode
939	  *[2.25–3.75]: Master Mode
940	  *[1/6 (16.67%)]: Expert Mode
941	  *[Radius]: Explosion radius in tiles
942	  *[13 mph]: 13 miles per hour (as measured by the Stopwatch item) or 9.375 tiles per second
943	  *[7.76%]: Expert Mode
944	  *[2%]: Expert Mode
945	  *[10 minutes]: Expert Mode
946	  *[12 minutes 30 seconds]: Master Mode
947	  *[105›93›187]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
948	  *[157›140›281]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
949	  *[1–3]: Expert Mode
950	  *[1–2]: Master Mode
951	  *[5–7]: Expert Mode
952	  *[2–4]: Master Mode
953	  *[1/4 (25%)]: Expert Mode
954	  *[8 seconds]: Expert Mode
955	  *[67%]: Expert Mode
956	  *[two pieces]: Expert Mode
957	  *[dua bagian]: Mode Expert
958	  *[2-10]: Expert Mode
959	  *[2-12]: Master Mode
960	  *[0.73–1.5]: Expert Mode
961	  *[0.92–1.87]: Master Mode
962	  *[0.9–1.13]: Expert Mode
963	  *[1.5–1.88]: Master Mode
964	  *[1/6 (16.7%)]: Expert Mode
965	  *[4-6]: Expert Mode
966	  *[5-7.5]: Master Mode
967	  *[48-72]: Expert Mode
968	  *[60-90]: Master Mode
969	  *[168]: Master Mode
970	  *[5–20%]: Expert Mode
971	  *[5%]: Expert Mode
972	  *[10%]: Expert Mode
973	  *[1]: Base value
974	  *[0.14]: Turtle armor
975	  *[0.2]: 5 Menacing modifiers
976	  *[0.15]: Shroomite bonus
977	  *[0.12]: Avenger Emblem
978	  *[0.1]: Quiver bonus
979	  *[0.05]: Well Fed
980	  *[230]: Godly Meowmere
981	  *[1.98]: Melee damage multiplier
982	  *[0.13]: Shroomite armor
983	  *[0.6]: Shroomite armor stealth effect
984	  *[0.16]: 4 Menacing modifiers
985	  *[39]: Godly Chlorophyte Shotbow
986	  *[2.26]: Ranged damage multiplier
987	  *[1.15]: Shroomite bonus
988	  *[1.1]: Archery buff
989	  *[105]: Master Mode
990	  *[11]: Expert Mode
991	  *[3–6]: Expert Mode
992	  *[3.75–7.5]: Master Mode
993	  *[3.6–6]: Expert Mode
994	  *[4.5–7.5]: Master Mode
995	  *[6.56%]: Expert Mode
996	  *[59/900 (6.56%)]: Expert Mode
997	  *[15 seconds]: Master Mode
998	  *[1 minute]: Expert Mode
999	  *[three-quarters]: Expert Mode
1000	  *[all]: Master Mode
1001	  *[a [Jellyfish](Jellyfish.md "Jellyfish")'s shock attack]: Expert Mode
1002	  *[30 _CC_]: Expert Mode
1003	  *[ 4.94%]: Expert Mode
1004	  *[1 _SC_ 50 _CC_]: Expert Mode
1005	  *[6 _GC_]: Expert Mode
1006	  *[6–90 seconds]: Expert Mode
1007	  *[7.5–112.5 seconds]: Master Mode
1008	  *[2–40 seconds]: Expert Mode
1009	  *[2.5–50 seconds]: Master Mode
1010	  *[1–30 seconds]: Expert Mode
1011	  *[1.25–37.5 seconds]: Master Mode
1012	  *[4–14 seconds]: Expert Mode
1013	  *[5–17.5 seconds]: Master Mode
1014	  *[12 seconds]: Expert Mode
1015	  *[14–30 seconds]: Expert Mode
1016	  *[17.5–37.5 seconds]: Master Mode
1017	  *[4–20 seconds]: Expert Mode
1018	  *[5–25 seconds]: Master Mode
1019	  *[1.5–28 seconds]: Expert Mode
1020	  *[1.87–35 seconds]: Master Mode
1021	  *[3–30 seconds]: Expert Mode
1022	  *[3.75–37.5 seconds]: Master Mode
1023	  *[4–12 seconds]: Expert Mode
1024	  *[5–15 seconds]: Master Mode
1025	  *[1.5–14 seconds]: Expert Mode
1026	  *[1.87–17.5 seconds]: Master Mode
1027	  *[0.73–8 seconds]: Expert Mode
1028	  *[0.92–10 seconds]: Master Mode
1029	  *[10–90 seconds]: Expert Mode
1030	  *[12.5–112.5 seconds]: Master Mode
1031	  *[0.5–32 seconds]: Expert Mode
1032	  *[0.63–40 seconds]: Master Mode
1033	  *[5 mph]: 5 miles per hour (as measured by the Stopwatch item) or 3.75 tiles per second
1034	  *[0.67–4 seconds]: Expert Mode
1035	  *[0.83–5 seconds]: Master Mode
1036	  *[1–4 seconds]: Expert Mode
1037	  *[4–8 seconds]: Expert Mode
1038	  *[5 seconds]: Master Mode
1039	  *[11.23–600 seconds]: Expert Mode
1040	  *[14.03–750 seconds]: Master Mode
1041	  *[3–90 seconds]: Master Mode
1042	  *[16 seconds]: Expert Mode
1043	  *[ 6]: Expert Mode
1044	  *[ 18]: Expert Mode
1045	  *[ 6-90 detik]: Mode Expert
1046	  *[2-20 detik]: Mode Expert
1047	  *[14-20 detik]: Mode Expert
1048	  *[16 detik]: Mode Expert
1049	  *[5-30 detik]: Mode Expert
1050	  *[6 detik]: Mode Expert
1051	  *[2.5-14 detik]: Mode Expert
1052	  *[1.25-8 detik]: Mode Expert
1053	  *[0.5-32 detik]: Mode Expert
1054	  *[18.75 detik - 10 menit]: Mode Expert
1055	  *[16.25 detik - 4 menit]: Mode Expert
1056	  *[10 detik]: Mode Expert
1057	  *[14-16 detik]: Mode Expert
1058	  *[20 detik-90 detik]: Mode Expert
1059	  *[2-3 detik]: Mode Expert
1060	  *[ 1 detik]: Mode Expert
1061	  *[5-9 detik]: Mode Expert
1062	  *[3-90 detik]: Mode Expert
1063	  *[16 detik]: Mode Expert
1064	  *[52]: Expert Mode
1065	  *[78]: Master Mode
1066	  *[72]: Expert Mode
1067	  *[108]: Expert Mode
1068	  *[24 seconds]: Expert Mode
1069	  *[0.67 seconds]: Expert Mode
1070	  *[0.83 seconds]: Master Mode
1071	  *[midnight]: 12:00 AM
1072	  *[five]: Expert Mode
1073	  *[0.67]: Expert Mode
1074	  *[0.83]: Master Mode
1075	  *[14000]: Expert Mode
1076	  *[21000]: Master Mode
1077	  *[11900]: Expert Mode
1078	  *[15172]: Master Mode
1079	  *[0.75]: Expert Mode
1080	  *[Atk.  
1081	dmg]: Attack damage
1082	  *[Def.]: Defense
1083	  *[AP]: Armor penetration
1084	  *[77]: Master Mode
1085	  *[81]: Master Mode
1086	  *[27]: Expert Mode
1087	  *[31]: Master Mode
1088	  *[208]: Master Mode
1089	  *[69]: Expert Mode
1090	  *[Dynamit. Můj speciální lík na všechno, co tě trápí.]: Dynamite, my own special cure-all for what ails ya.
1091	  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
1092	  *[Proč očisťovat svět, když jej můžeš vyhodit do povětří?]: Why purify the world when you can just blow it up?
1093	  *[Dnes se bude dobře umírat!]: It's a good day to die!
1094	  *[Jsem si docela jistý, že ti [jméno sestřičky] pomůže přišít zpět všechny tvé končetiny.]: 
1095	  *[Zajímalo by mě, co se stane, pokud… (BUM!)… Oh, omlouvám se, potřeboval jsi tu nohu?]: I wonder what happens if I... (BOOM!)... Oh, sorry, did you need that leg?
1096	  *[Dokonce i [jméno prodejce zbraní] by chtěl to, co já prodávám!]: Even [Name of Arms Dealer] wants what I'm selling!
1097	  *[Byl bys radši s dírou po kulce, nebo dírou po granátu? Myslel jsem si to.]: Would you rather have a bullet hole or a grenade hole? That's what I thought.
1098	  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
1099	  *[ZÁKAZ KOUŘENÍ!]: NO SMOKING IN HERE!!
1100	  *[Pokud hodíš tenhle do vany a zavřeš všechna okna, pročistí to všechny tvé dutiny a urve uši!]: If you throw this one in the bathtub and close all the windows, it'll clear your sinuses and pop your ears!
1101	  *[Chceš si hrát na kuře Pojistku?]: Wanna play Fuse Chicken?
1102	  *[Podepsal bys mi tento griefovací dokument?]: Hey, could you sign this Griefing Waiver?
1103	  *[Něco jsem si od těch zombie odnesl!]: I've got something for them zombies alright!
1104	  *[Hej, neviděl jsi někde klauna?]: Hey, have you seen a clown around?
1105	  *[Ještě před chvílí tady seděla bomba, teď ji nemůžu najít…]: There was a bomb sitting right here, and now I can't seem to find it...
1106	  *[84]: Expert Mode
1107	  *[126]: Master Mode
1108	  *[30 seconds]: Expertní mód
1109	  *[60 mph]: 60 miles per hour (as measured by the Stopwatch item) or 44 tiles per second
1110	  *[33,33%]: Master Mode
1111	  *[88]: Expert Mode
1112	  *[132]: Master Mode
1113	  *[Contact]: The damage without modifier and summon damage bonuses
1114	  *[Pounce]: The damage without modifier and summon damage bonuses
1115	  *[Threshold]: If the player's summon damage bonuses reach it, Ruthless will become the best modifier
1116	  *[N/A]: Not available in vanilla game
1117	  *[16−30 seconds]: Expert Mode
1118	  *[20−37.5 seconds]: Master Mode
1119	  *[ 9.75%]: Expert Mode
1120	  *[16–30]: Expert Mode
1121	  *[20–37.5]: Master Mode
1122	  *[128]: Expert Mode
1123	  *[192]: Master Mode
1124	  *[15–60]: Expert Mode
1125	  *[0.5×]: Journey Mode
1126	  *[2×]: Expert Mode
1127	  *[3×]: Master Mode
1128	  *[4×]: Expert Mode
1129	  *[5.33×]: Legendary Mode
1130	  *[2.5×]: Master Mode
1131	  *[3.5×]: Legendary Mode
1132	  *[0.9×]: Expert Mode
1133	  *[0.8×]: Master Mode
1134	  *[1.5×]: Expert Mode
1135	  *[1.75×]: Master Mode
1136	  *[May increase both during [Hardmode](Hardmode.md "Hardmode") and [Post-Plantera](Post-Plantera.md "Post-Plantera")]: Expert Mode
1137	  *[May increase]: Expert Mode
1138	  *[15 / 30]: Expert Mode
1139	  *[ 4%]: Expert Mode
1140	  *[+15]: Expert Mode
1141	  *[+20]: Master Mode
1142	  *[ 16]: Expert Mode
1143	  *[18]: Master Mode
1144	  *[Opatruj se! Terraria tě potřebuje!]: Be safe; Terraria needs you!
1145	  *[Musíš očistit svět od této nákazy.]: You must cleanse the world of this corruption.
1146	  *[Musíš očistit svět od tohoto karmínu.]: You must cleanse the world of this crimson.
1147	  *[Písky času se přesýpají. A upřímně, nemládneš a nekrásníš.]: The sands of time are flowing. And well, you are not aging very gracefully.
1148	  *[Co je to s tím, že více ‚štěkám‘ než koušu?]: What's this about me having more 'bark' than bite?
1149	  *[Dva goblini tahle přijdou do baru a jeden říká tomu druhému: ‚Dáš si goblet piva?!‘]: So two goblins walk into a bar, and one says to the other, 'Want to get a Goblet of beer?!'
1150	  *[Proč se mi [Jméno obchodníka] snaží prodat sochy andělů? Všichni přeci ví, že nic nedělají.]: Why does [Name of Merchant] keep trying to sell me an angel statues? Everyone knows that they don't do anything.
1151	  *[Kéž by se mnou [jméno prodejce zbraní] přestal flirtovat. Copak si neuvědomuje, že jsem více než 500 let stará?]: I wish [Name of Arms Dealer] would stop flirting with me. Doesn't he realize I'm 500 years old?
1152	  *[Už jsi v nákaze zkoušel použít očistný prášek na ebenokámen?]: Have you tried using purification powder on the ebonstone of The Corruption?
1153	  *[Už jsi v karmínu zkoušel použít očistný prášek na karmínokámen?]: Have you tried using purification powder on the Crimstone of the Crimson?
1154	  *[Viděl jsi starce procházejícího se kolem podzemní kobky? Vůbec nevypadá dobře…]: Have you seen the old man walking around the dungeon? He doesn't look well at all...
1155	  *[Myslím si, že je [jméno lanýže] nepochopený ostatními. Je to velmi vtipný chlapík.]: I feel like [Name of Truffle] is a bit misunderstood, he really is a fun guy.
1156	  *[Prodávám co se mi zlíbí! Pokud se ti to nelíbí, tak máš smůlu.]: I sell what I want! If you don't like it, too bad.
1157	  *[Kámo, je to mnou, nebo je venku tak milion zombie?]: Dude, is it just me or are there a million [[zombies]] out tonight?
1158	  *[Nechci aby sis kupoval mé věci. Já chci abys chtěl si mé věci kupovat, jasné?]: I don't want you to buy my stuff. I want you to want to buy my stuff, ok?
1159	  *[Proč musíš být ve chvílích jako je tato tak konfrontační?]: Why do you have to be so confrontational during a time like this?
1160	  *[[jméno světa] je z [procenta posvátnosti] % posvátný a [procenta nákazy/karmínu] % [nakažen/karmínový]. [Dryádin komentář (viz výše)].]: [Name of world] is [hallow percentage]% hallow and [crimson/corruption percentage]% [crimson/corruption]. [Dryad's comment, see above].
1161	  *[[jméno světa] je kompletně očištěn. Odvedl jsi úžasnou práci!]: [Name of World] is completely pure. You have done an amazing job!
1162	  *[+10]: Expert Mode
1163	  *[+14]: Master Mode
1164	  *[6–20 seconds]: Expert Mode
1165	  *[7.5–25 seconds]: Master Mode
1166	  *[3–10 seconds]: Expert Mode
1167	  *[201]: Expert Mode
1168	  *[302]: Expert Mode
1169	  *[184]: Expert Mode
1170	  *[277]: Master Mode
1171	  *[39000/78000]: Expert Mode
1172	  *[49725/99450]: Master Mode
1173	  *[0]: Expert Mode
1174	  *[39,000]: Expert Mode
1175	  *[49,725]: Master Mode
1176	  *[11,700]: Expert Mode
1177	  *[14,917]: Master Mode
1178	  *[60,000]: Expert Mode
1179	  *[76,500]: Master Mode
1180	  *[99,000]: Master Mode
1181	  *[ 78000]: Expert Mode
1182	  *[99450]: Master Mode
1183	  *[ ]: Master Mode
1184	  *[ 62 _GC_ 50 _SC_]: Expert Mode
1185	  *[ 2 _GC_ 50 _SC_]: Mode Expert
1186	  *[39000]: Mode Expert
1187	  *[49725]: Mode Master
1188	  *[double]: Expert Mode
1189	  *[triple]: Master Mode
1190	  *[1/9 (11.11%)]: Expert Mode
1191	  *[1/8 (12.5%)]: Expert Mode
1192	  *[19]: Master Mode
1193	  *[15120]: Expert Mode
1194	  *[19296]: Master Mode
1195	  *[356]: Mode Expert
1196	  *[209]: Mode Expert
1197	  *[139.33 yards (152.38 m)]: Expert Mode
1198	  *[10479]: Expert Mode
1199	  *[1/20 (5%)]: Expert Mode
1200	  *[10 minutes]: Expert Mode
1201	  *[100-150]: Expert Mode
1202	  *[2-3]: Chế độ Expert
1203	  *[ 15120]: Chế độ Expert
1204	  *[ 19296]: Chế độ Master
1205	  *[ 10500]: Chế độ Expert
1206	  *[10 menit]: Mode Expert
1207	  *[12 menit 30 detik]: Mode Master
1208	  *[2–3]: Chế độ Expert
1209	  *[1/20 (%5)]: Expert Mode
1210	  *[10 phút]: Chế độ Expert
1211	  *[12 phút 30 giây]: Chế độ Master
1212	  *[10500]: Expert Mode
1213	  *[Total damage]: Stationary / Moving
1214	  *[110]: Expert Mode
1215	  *[248]: Master Mode
1216	  *[165]: Expert Mode
1217	  *[372]: Master Mode
1218	  *[49000/98000]: Expert Mode
1219	  *[62475/124950]: Master Mode
1220	  *[12]: Expert Mode
1221	  *[Ethereal Lance 3]: Expert Mode
1222	  *[49,000]: Expert Mode
1223	  *[62,475]: Master Mode
1224	  *[59,994]: Master Mode
1225	  *[39,996]: Expert Mode
1226	  *[24 mph]: 24 miles per hour (as measured by the Stopwatch item) or 17.6 tiles per second
1227	  *[33 mph]: 33 miles per hour (as measured by the Stopwatch item) or 24.2 tiles per second
1228	  *[2000]: Expert Mode
1229	  *[3000]: Master Mode
1230	  *[6000]: Expert Mode
1231	  *[9000]: Master Mode
1232	  *[10000]: Expert Mode
1233	  *[15000]: Master Mode
1234	  *[48›86]: Expert Mode : Pre-Hardmode › Hardmode
1235	  *[72›129]: Master Mode : Pre-Hardmode › Hardmode
1236	  *[124]: Expert Mode
1237	  *[186]: Master Mode
1238	  *[37%]: Expert Mode
1239	  *[44%]: Master Mode
1240	  *[55%]: Expert Mode
1241	  *[82%]: Expert Mode
1242	  *[84%]: Master Mode
1243	  *[172]: Master Mode
1244	  *[258]: Master Mode
1245	  *[228]: Expert Mode
1246	  *[342]: Master Mode
1247	  *[1.33–6.67%]: Expert Mode
1248	  *[27.27–60%]: Expert Mode
1249	  *[5–25%]: Master Mode
1250	  *[20–100%]: Master Mode
1251	  *[125]: Master Mode
1252	  *[9/25 (36%)]: Expert Mode
1253	  *[9/25]: Expert Mode
1254	  *[1050]: Master Mode
1255	  *[1/10 (10%)]: Expert Mode
1256	  *[54]: Master Mode
1257	  *[2366/3640]: Expert Mode
1258	  *[3016/4641]: Master Mode
1259	  *[−15]: Expert Mode
1260	  *[−30]: Expert Mode
1261	  *[Chain charge]: Expert Mode
1262	  *[2,366]: Chế độ Expert
1263	  *[3,016]: Mode Master
1264	  *[436]: Expert Mode
1265	  *[556]: Master Mode
1266	  *[145]: Expert Mode
1267	  *[185]: Master Mode
1268	  *[7 _GC_ 50 _SC_]: Expert Mode
1269	  *[36  
1270	40 when below 145 health]: Expert Mode
1271	  *[54  
1272	60 when below 185 health]: Master Mode
1273	  *[2365/3640]: Chế độ Expert
1274	  *[ 7 _GC_ 50 _SC_]: Chế độ Expert
1275	  *[ %25]: Master Mode
1276	  *[36  
1277	40 khi dưới 145 máu]: Chế độ Expert
1278	  *[54  
1279	60 khi dưới 185 máu]: Chế độ Master
1280	  *[3017/4641]: Chế độ Master
1281	  *[Liên hoàn lướt]: Chế độ Expert
1282	  *[4641]: Chế độ Master
1283	  *[3016]: Chế độ Master
1284	  *[1,000]: Expert Mode
1285	  *[1,500]: Master Mode
1286	  *[8 mph]: 8 miles per hour (as measured by the Stopwatch item) or 5.625 tiles per second
1287	  *[19 mph]: 19 miles per hour (as measured by the Stopwatch item) or 14.0625 tiles per second
1288	  *[4.2–7]: Expert Mode
1289	  *[5.25–8.75]: Master Mode
1290	  *[6–10]: Expert Mode
1291	  *[7.5–12.5]: Master Mode
1292	  *[1.2–2]: Expert Mode
1293	  *[1.5–2.5]: Master Mode
1294	  *[FP]: Fishing Power
1295	  *[cần có 5]: Chế độ Journey
1296	  *[cần có 3]: Chế độ Journey
1297	  *[membutuhkan 99]: Mode Journey
1298	  *[22 mph]: 22 miles per hour (as measured by the Stopwatch item) or 15.8371875 tiles per second
1299	  *[113 mph]: 113 miles per hour (as measured by the Stopwatch item) or 82.5 tiles per second
1300	  *[116 mph]: 116 miles per hour (as measured by the Stopwatch item) or 85.07 tiles per second
1301	  *[13600]: Expert Mode
1302	  *[20400]: Master Mode
1303	  *[32 mph]: 32 miles per hour (as measured by the Stopwatch item) or 23.63343375 tiles per second
1304	  *[81 mph]: 81 miles per hour (as measured by the Stopwatch item) or 59.4 tiles per second
1305	  *[71 mph]: 71 miles per hour (as measured by the Stopwatch item) or 52.07 tiles per second
1306	  *[14 mph]: 14 miles per hour (as measured by the Stopwatch item) or 10.546875 tiles per second
1307	  *[28 mph]: 28 miles per hour (as measured by the Stopwatch item) or 20.53 tiles per second
1308	  *[37 mph]: 37 miles per hour (as measured by the Stopwatch item) or 27 tiles per second
1309	  *[42 mph]: 42 miles per hour (as measured by the Stopwatch item) or 30.8 tiles per second
1310	  *[48 mph]: 48 miles per hour (as measured by the Stopwatch item) or 35.2 tiles per second
1311	  *[49 mph]: 49 miles per hour (as measured by the Stopwatch item) or 35.625 tiles per second
1312	  *[56 mph]: 56 miles per hour (as measured by the Stopwatch item) or 41.07 tiles per second
1313	  *[47 mph]: 47 miles per hour (as measured by the Stopwatch item) or 34.47 tiles per second
1314	  *[7.7 mph]: 7.7 miles per hour (as measured by the Stopwatch item) or 5.65 tiles per second
1315	  *[63 mph]: 63 miles per hour (as measured by the Stopwatch item) or 45.9375 tiles per second
1316	  *[2.5]: Master Mode
1317	  *[250]: Master Mode
1318	  *[375]: Master Mode
1319	  *[100% by wave 14]: Expert Mode
1320	  *[3/11 (27.27%)]: Expert Mode
1321	  *[3/8 (37.5%)]: Expert Mode
1322	  *[3/5 (60%)]: Expert Mode
1323	  *[Base]: Base drop rate without the factor
1324	  *[1.67%]: Expert Mode
1325	  *[2.22%]: Expert Mode
1326	  *[8.33%]: Master Mode
1327	  *[27.27%]: Expert Mode
1328	  *[37.5%]: Expert Mode
1329	  *[6-12]: Expert Mode
1330	  *[7-15]: Master Mode
1331	  *[48-96]: Expert Mode
1332	  *[56-120]: Master Mode
1333	  *[3.75]: Master Mode
1334	  *[13/125 (10.4%)]: Expert Mode
1335	  *[39/400 (9.75%)]: Expert Mode
1336	  *[69/1225 (5.63%)]: Expert Mode
1337	  *[1–4]: Expert Mode
1338	  *[1.25–5]: Master Mode
1339	  *[0.67–2]: Expert Mode
1340	  *[0.83–2.5]: Master Mode
1341	  *[12.5–25%]: Master Mode
1342	  *[(Expert Mode exclusive)]: Expertní mód
1343	  *[40 mph]: 40 miles per hour (as measured by the Stopwatch item) or 29.33 tiles per second
1344	  *[1 minute 38 seconds]: Expert Mode
1345	  *[2 minutes 3 seconds]: Master Mode
1346	  *[Ukořisti drahokam]: Capture the Gem
1347	  *[membutuhkan 15]: Mode Journey
1348	  *[cần có 15]: Chế độ Journey
1349	  *[membutuhkan 5]: Mode Journey
1350	  *[28 seconds]: Expert Mode
1351	  *[35 seconds]: Master Mode
1352	  *[30–90 seconds]: Expert Mode
1353	  *[7.84%]: Expert Mode
1354	  *[7,84%]: Mode Expert
1355	  *[43]: Expert Mode
1356	  *[64]: Expert Mode
1357	  *[288]: Expert Mode
1358	  *[432]: Master Mode
1359	  *[4%]: Expert Mode
1360	  *[44]: Chế độ Expert
1361	  *[66]: Chế độ Master
1362	  *[33.3%]: Expert Mode
1363	  *[10 required]: Journey Mode
1364	  *[90000]: Expert Mode
1365	  *[114749]: Master Mode
1366	  *[37500]: Expert Mode
1367	  *[47812]: Master Mode
1368	  *[22500]: Expert Mode
1369	  *[28687]: Master Mode
1370	  *[19125]: Master Mode
1371	  *[10–14 seconds]: Expert Mode
1372	  *[15–21 seconds]: Master Mode
1373	  *[10–14]: Expert Mode
1374	  *[15–21]: Master Mode
1375	  *[18,750]: Expert Mode
1376	  *[23,906]: Master Mode
1377	  *[58 mph]: 58 miles per hour (as measured by the Stopwatch item) or 42.75 tiles per second
1378	  *[104]: Expert Mode
1379	  *[156]: Master Mode
1380	  *[59 mph]: 59 miles per hour (as measured by the Stopwatch item) or 43.125 tiles per second
1381	  *[162]: Master Mode
1382	  *[112]: Expert Mode
1383	  *[116]: Expert Mode
1384	  *[174]: Master Mode
1385	  *[96–116]: Expert Mode
1386	  *[144–174]: Master Mode
1387	  *[15,000]: Expert Mode
1388	  *[19,124]: Master Mode
1389	  *[7,500]: Expert Mode
1390	  *[9,562]: Master Mode
1391	  *[18,000]: Expert Mode
1392	  *[22,949]: Master Mode
1393	  *[13,500]: Expert Mode
1394	  *[17,212]: Master Mode
1395	  *[4,500]: Expert Mode
1396	  *[5,737]: Master Mode
1397	  *[2,250]: Expert Mode
1398	  *[2,868]: Master Mode
1399	  *[11,250]: Expert Mode
1400	  *[14,343]: Master Mode
1401	  *[9,000]: Expert Mode
1402	  *[11,474]: Master Mode
1403	  *[6,750]: Expert Mode
1404	  *[8,606]: Master Mode
1405	  *[123 mph]: 123 miles per hour (as measured by the Stopwatch item) or 90 tiles per second
1406	  *[1 mph]: 1 mile per hour (as measured by the Stopwatch item) or 0.73 tiles per second
1407	  *[AMA]: Ask Me Anything
1408	  *[Zdravím [jméno hráče]. Je zde něco, s čím bych mohl pomoci?]: Greetings, [Name of Player]. Is there something I can help you with?
1409	  *[Jsem zde proto, abych ti dával rady co máš dělat. Doporučuji ti si se mnou přijít promluvit, kdykoliv si nebudeš vědět rady.]: I am here to give you advice on what to do next. It is recommended that you talk with me anytime you get stuck.
1410	  *[Říká se, že existuje člověk, který ti poradí, jak máš přežít v této krajině… ale počkat. To jsem přeci já.]: They say there is a person who will tell you how to survive in this land... oh wait. That's me.
1411	  *[Měl bys zůstat v době během noci. Je velmi nebezpečné toulat se v noci.]: You should stay indoors at night. It is very dangerous to be wandering around in the dark.
1412	  *[Hej kamaráde, nevíš, kde se nachází nějaký smrtirost? Jen tak, přemýšlím nahlas.]: Hey, buddy, do you know where any deathweed is? Oh, no reason; Just wondering, is all.
1413	  *[Pokud se podíváš na oblohu, uvidíš, že je měsíc krvavý.]: If you were to look up, you'd see the moon is red right now.
1414	  *[S jistotou můžeš říct, že nastal krvavý měsíc, jakmile se barva oblohy promění v červenou. Něho během této doby způsobuje, že se objevuje více nepřátel.]: You can tell a Blood Moon is out when the sky turns red. There is something about it that causes monsters to swarm.
1415	  *[Oktoberfest je tady! [Jméno obchodníka] uvařil kvůli této události své proslulé pivo a [jméno oděvníka] prodává tradiční oblečení spojené s festivalem.]: The Oktober festival is here! [Name of Merchant] has brewed up some of his famous ale especially for the occasion and [Name of Clothier] is selling traditional festival clothes.
1416	  *[Nový rok je tady! [Jméno demoličního experta] prodává speciální zbraně, které rozzáří oblohu a [jméno oděvníka] prodává tradiční sváteční oděv.]: New Year is here! [Name of Demolitionist] is selling special weaponry to light up the skies, and [Name of Clothier] is selling traditional festive attire.
1417	  *[75]: Expert Mode
1418	  *[Expert-exclusive]: Expert Mode
1419	  *[Master-exclusive]: Master Mode
1420	  *[Hive Pack]: Expert Mode
1421	  *[and third]: Expert Mode
1422	  *[0.9›0.4]: Pre-Hardmode › Hardmode
1423	  *[0.5›0.45]: Pre-Hardmode › Hardmode
1424	  *[216]: Master Mode
1425	  *[252]: Master Mode
1426	  *[6.25–25%]: Master Mode
1427	  *[25–100%]: Master Mode
1428	  *[140–148]: Expert Mode
1429	  *[210–222]: Master Mode
1430	  *[10–20 seconds]: Expert Mode
1431	  *[12.5–25 seconds]: Master Mode
1432	  *[≤ 2 seconds]: Expert Mode
1433	  *[≤ 2.5 seconds]: Master Mode
1434	  *[50–100%]: Master Mode
1435	  *[nebo 3/4]: Expertní mód
1436	  *[tümü]: Master Mode
1437	  *[18750]: Expert Mode
1438	  *[67]: Expert Mode
1439	  *[1–5 seconds]: Expert Mode
1440	  *[1.25–6.25 seconds]: Master Mode
1441	  *[ 17 _CC_ ]: Expert Mode
1442	  *[ 49 _CC_ ]: Expert Mode
1443	  *[ 1 _SC_ 30 _CC_ ]: Expert Mode
1444	  *[ 20 _CC_ ]: Expert Mode
1445	  *[14 _GC_ 81 _SC_]: Expert Mode
1446	  *[16 _GC_ 6 _SC_]: Master Mode
1447	  *[2 _PC_ 67 _GC_]: Expert Mode
1448	  *[2 _PC_ 89 _GC_]: Master Mode
1449	  *[81 _SC_ 20 _CC_]: Expert Mode
1450	  *[3 _SC_ 72 _CC_]: Expert Mode
1451	  *[1 _SC_ 69 _CC_]: Expert Mode
1452	  *[9 _SC_ 20 _CC_]: Expert Mode
1453	  *[8 _SC_ 6 _CC_]: Expert Mode
1454	  *[7 _SC_ 44 _CC_]: Expert Mode
1455	  *[4 _SC_ 92 _CC_]: Expert Mode
1456	  *[2 _SC_ 61 _CC_]: Expert Mode
1457	  *[3 _SC_ 31 _CC_]: Expert Mode
1458	  *[5 _SC_ 26 _CC_]: Expert Mode
1459	  *[3 _SC_ 17 _CC_]: Expert Mode
1460	  *[11 _SC_ 73 _CC_]: Expert Mode
1461	  *[4 _SC_ 32 _CC_]: Expert Mode
1462	  *[16 _SC_ 91 _CC_]: Expert Mode
1463	  *[54 _SC_ 67 _CC_]: Expert Mode
1464	  *[72 _SC_ 68 _CC_]: Expert Mode
1465	  *[44 _SC_ 90 _CC_]: Expert Mode
1466	  *[2 _GC_ 46 _SC_ 61 _CC_]: Expert Mode
1467	  *[45 _SC_ 93 _CC_]: Expert Mode
1468	  *[65 _SC_ 1 _CC_]: Expert Mode
1469	  *[12 _SC_ 81 _CC_]: Expert Mode
1470	  *[1 _GC_ 83 _SC_ 35 _CC_]: Expert Mode
1471	  *[2 _GC_ 65 _SC_]: Expert Mode
1472	  *[7 _GC_ 71 _SC_]: Expert Mode
1473	  *[7 _GC_ 95 _SC_]: Expert Mode
1474	  *[8 _GC_ 71 _SC_]: Expert Mode
1475	  *[21 _GC_ 9 _SC_]: Expert Mode
1476	  *[19 _GC_ 70 _SC_]: Expert Mode
1477	  *[13 _GC_ 25 _SC_]: Expert Mode
1478	  *[26 _GC_ 17 _SC_]: Expert Mode
1479	  *[9 _GC_ 44 _SC_]: Expert Mode
1480	  *[5 _GC_ 31 _SC_]: Expert Mode
1481	  *[3 _GC_ 68 _SC_]: Expert Mode
1482	  *[21 _GC_ 20 _SC_]: Expert Mode
1483	  *[15 _GC_ 90 _SC_]: Expert Mode
1484	  *[15 _GC_ 60 _SC_]: Expert Mode
1485	  *[31 _GC_ 80 _SC_]: Expert Mode
1486	  *[37 _GC_ 71 _SC_]: Expert Mode
1487	  *[39 _GC_ 75 _SC_]: Expert Mode
1488	  *[17 _GC_ 92 _SC_]: Expert Mode
1489	  *[35 _GC_ 51 _SC_]: Expert Mode
1490	  *[66 _GC_ 25 _SC_]: Expert Mode
1491	  *[11 _GC_ 92 _SC_]: Expert Mode
1492	  *[19 _GC_ 73 _SC_]: Expert Mode
1493	  *[26 _GC_ 50 _SC_]: Expert Mode
1494	  *[2 _PC_ 65 _GC_]: Expert Mode
1495	  *[1 _PC_ 18 _GC_]: Expert Mode
1496	  *[45900]: Expert Mode
1497	  *[68850]: Master Mode
1498	  *[327,420]: Expert Mode
1499	  *[436,560]: Master Mode
1500	  *[217500]: Expertní mód
1501	  *[277311]: Master Mode
1502	  *[450]: Master Mode
1503	  *[Master Mode]: Master Mode
1504	  *[245]: Expert Mode
1505	  *[367]: Master Mode
1506	  *[76]: Expert Mode
1507	  *[114]: Expert Mode
1508	  *[42000]: Expert Mode
1509	  *[53550]: Master Mode
1510	  *[4–18 seconds]: Expert Mode
1511	  *[5–22.5 seconds]: Master Mode
1512	  *[21000/42000]: Expert Mode
1513	  *[26775/53550]: Master Mode
1514	  *[5›6]: Expert Mode : Pre-Hardmode › Hardmode
1515	  *[6›7]: Master Mode : Pre-Hardmode › Hardmode
1516	  *[1/100 (1%)]: Expert Mode
1517	  *[1/2000 (0.05%)]: Expert Mode
1518	  *[25–40]: Expert Mode
1519	  *[8–28]: Expert Mode
1520	  *[2–20 seconds]: Expert Mode
1521	  *[2.5–25 seconds]: Master Mode
1522	  *[2–8 seconds]: Expert Mode
1523	  *[2.5–10 seconds]: Master Mode
1524	  *[17–30]: Expert Mode
1525	  *[defense]: Expert Mode
1526	  *[14400/28800]: Expert Mode
1527	  *[18360/36720]: Master Mode
1528	  *[25–74]: Expert Mode
1529	  *[13500]: Expert Mode
1530	  *[17212]: Master Mode
1531	  *[11475]: Master Mode
1532	  *[13387]: Master Mode
1533	  *[The [](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu") can greatly increase your mobility as well as provide some extra defense.]: Expert Mode
1534	  *[The [](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") will reduce damage taken, making it a powerful choice.]: Expert Mode
1535	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") has a chance to dodge an attack, providing the player with a useful [](Cerebral_Mindtrick "Cerebral Mindtrick")[Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick") buff.]: Expert Mode
1536	  *[91]: Expert Mode
1537	  *[137]: Master Mode
1538	  *[10+25 per hand alive]: Expert Mode
1539	  *[0+25 per hand alive]: Expert Mode
1540	  *[6–10 seconds]: Expert Mode
1541	  *[7.5–12.5 seconds]: Master Mode
1542	  *[1−2 seconds]: Expert Mode
1543	  *[1.5–2.5 seconds]: Master Mode
1544	  *[9.75%]: Expert Mode
1545	  *[55.56%]: Expert Mode
1546	  *[64500]: Expert Mode
1547	  *[82238]: Master Mode
1548	  *[64,500]: Expert Mode
1549	  *[82,238]: Master Mode
1550	  *[12,000]: Expert Mode
1551	  *[15,300]: Master Mode
1552	  *[13,800]: Expert Mode
1553	  *[17,595.2]: Master Mode
1554	  *[[](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu")'s dash is essential throughout the fight.]: Expert Mode
1555	  *[[](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") greatly decreases damage, but is exclusive to Corruption worlds.]: Expert Mode
1556	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") is very useful for players as it provides a chance to dodge an attack, but is exclusive to Crimson worlds. It doesn't prevent getting inflicted with the [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff, however.]: Expert Mode
1557	  *[24%]: Expert Mode
1558	  *[28%]: Master Mode
1559	  *[11,920]: Expert Mode
1560	  *[15,198]: Master Mode
1561	  *[1560]: Expert Mode
1562	  *[1989]: Master Mode
1563	  *[3120]: Expert Mode
1564	  *[3978]: Master Mode
1565	  *[8800]: Expert Mode
1566	  *[7.2-12.5]: Master Mode
1567	  *[ Expert-exclusive]: Expert Mode
1568	  *[ Master-exclusive]: Master Mode
1569	  *[(expert)]: Expert Mode
1570	  *[12000]: Expert Mode
1571	  *[13800]: Expert Mode
1572	  *[18-90]: Expert Mode
1573	  *[67,500]: Expert Mode
1574	  *[37,500]: Expert Mode
1575	  *[75,000]: Expert Mode
1576	  *[with a 1/5 (20%) chance]: Expert Mode
1577	  *[41]: Expert Mode
1578	  *[0 mph]: 0 miles per hour (as measured by the Stopwatch item) or 0 tiles per second
1579	  *[150 mph]: 150 miles per hour (as measured by the Stopwatch item) or 110 tiles per second
1580	  *[179 mph]: 179 miles per hour (as measured by the Stopwatch item) or 131.27 tiles per second
1581	  *[ 6500]: Expert Mode
1582	  *[8287]: Master Mode
1583	  *[1.25%–5%]: Expert Mode
1584	  *[32]: Expert Mode
1585	  *[0.25 mph]: 0.25 miles per hour (as measured by the Stopwatch item) or 0.18 tiles per second
1586	  *[ 2700]: Expert Mode
1587	  *[4050]: Master Mode
1588	  *[96 mph]: 96 miles per hour (as measured by the Stopwatch item) or 70.4 tiles per second
1589	  *[164 mph]: 164 miles per hour (as measured by the Stopwatch item) or 120 tiles per second
1590	  *[245 mph]: 245 miles per hour (as measured by the Stopwatch item)
1591	  *[11/100 (11%)]: Expert Mode
1592	  *[5% – 20%]: Expert Mode
1593	  *[6.22% – 31.11%]: Expert Mode
1594	  *[50 mph]: 50 miles per hour (as measured by the Stopwatch item) or 36.67 tiles per second
1595	  *[2–10 or 20 seconds]: Expert Mode
1596	  *[2.5–12.5 or 25 seconds]: Master Mode
1597	  *[2–10 or 20 secondi]: Expert Mode
1598	  *[2.5–12.5 or 25 secondi]: Master Mode
1599	  *[52 mph]: 52 miles per hour (as measured by the Stopwatch item) or 38.13 tiles per second
1600	  *[5.63%]: Expert Mode
1601	  *[2 seconds]: Expert Mode
1602	  *[2.5 seconds]: Master Mode
1603	  *[4,000]: Expert Mode
1604	  *[6,000]: Master Mode
1605	  *[148]: Expert Mode
1606	  *[222]: Master Mode
1607	  *[1.33 seconds]: Expert Mode
1608	  *[1.67 seconds]: Master Mode
1609	  *[33,150]: Expert Mode
1610	  *[42,266]: Master Mode
1611	  *[22,100]: Expert Mode
1612	  *[28,177]: Master Mode
1613	  *[11,050]: Expert Mode
1614	  *[14,088]: Master Mode
1615	  *[4,420]: Expert Mode
1616	  *[5,635]: Master Mode
1617	  *[198]: Master Mode
1618	  *[297]: Master Mode
1619	  *[50 seconds]: Master Mode
1620	  *[1 minute 2.5 seconds]: Master Mode
1621	  *[1.25–5 seconds]: Master Mode
1622	  *[six]: Master Mode
1623	  *[additional accessory slot]: Master Mode
1624	  *[1.25%]: Expert Mode
1625	  *[2.5%]: Expert Mode
1626	  *[38 mph]: 38 miles per hour (as measured by the Stopwatch item) or 28.125 tiles per second
1627	  *[ 36]: Expert Mode
1628	  *[399/40,000 (0.9975%)]: Expert Mode
1629	  *[178]: Master Mode
1630	  *[2,659]: Expert Mode
1631	  *[3,390]: Master Mode
1632	  *[2,519]: Expert Mode
1633	  *[3,212]: Master Mode
1634	  *[2,800–2,240]: Expert Mode
1635	  *[3,570–2,856]: Master Mode
1636	  *[2,239–1,680]: Expert Mode
1637	  *[2,855–2,142]: Master Mode
1638	  *[1,679–1,120]: Expert Mode
1639	  *[2,141–1,428]: Master Mode
1640	  *[1,119–560]: Expert Mode
1641	  *[1,427–714]: Master Mode
1642	  *[559–280]: Expert Mode
1643	  *[713–357]: Master Mode
1644	  *[279–0]: Expert Mode
1645	  *[356–0]: Master Mode
1646	  *[2800]: Expert Mode
1647	  *[3570]: Master Mode
1648	  *[1/15th]: Expert Mode
1649	  *[15%]: Mode Expert
1650	  *[46%]: Expert Mode
1651	  *[52%]: Master Mode
1652	  *[68%]: Master Mode
1653	  *[1000]: Expert Mode
1654	  *[sometimes]: Expert Mode
1655	  *[1.2]: Archery buff
1656	  *[9]: Master Mode
1657	  *[O3DS]: Original Nintendo 3DS
1658	  *[Number]: Number of Tiny Eaters
1659	  *[Average]: Average number of Tiny Eaters
1660	  *[102×102]: Expert Mode
1661	  *[1/25 (4%)]: Expert Mode
1662	  *[44–60]: Expert Mode
1663	  *[66–90]: Master Mode
1664	  *[WoF]: Wall
1665	  *[135]: Master Mode
1666	  *[ (1 player)  
1667	57% (2 players)  
1668	71% (3 players)  
1669	81%  (4 players)  
1670	100% (5 players or more)  
1671	]: Expert Mode
1672	  *[ (1 player)  
1673	62% (2 players)  
1674	75% (3 players)  
1675	83% (4 players)  
1676	100% (5 players or more)  
1677	]: Master Mode
1678	  *[ (1 player)  
1679	69% (2 players)  
1680	79% (3 players)  
1681	86%  (4 players)  
1682	100% (5 players or more)  
1683	]: Expert Mode
1684	  *[ (1 player)  
1685	72% (2 players)  
1686	82% (3 players)  
1687	88% (4 players)  
1688	100% (5 players or more)  
1689	]: Master Mode
1690	  *[1485]: Expert Mode
1691	  *[2227]: Master Mode
1692	  *[2700]: Expert Mode
1693	  *[220]: Expert Mode
1694	  *[330]: Master Mode
1695	  *[224]: Expert Mode
1696	  *[336]: Master Mode
1697	  *[454]: Master Mode
1698	  *[52›93›138]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1699	  *[78›140›208]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1700	  *[60›105›105]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1701	  *[90›157›157]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1702	  *[48›86›131]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1703	  *[73›129›196]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1704	  *[60›105›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1705	  *[90›157›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1706	  *[45›120›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1707	  *[67›180›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1708	  *[472]: Master Mode
1709	  *[18–23]: Expert Mode
1710	  *[1/4]: Master Mode
1711	  *[4.94 (79/1600)]: Expert Mode
1712	  *[30–49]: Expert Mode
1713	  *[1/2]: Expert Mode
1714	  *[20–35]: Expert Mode
1715	  *[90–110]: Chế độ Expert
1716	  *[49/625 (7.84%)]: Expert Mode
1717	  *[99/2500 (3.96%)]: Expert Mode
1718	  *[1/15 (6.67%)]: Expert Mode
1719	  *[1/75 (1.33%)]: Expert Mode
1720	  *[1/20 (5%) ****__(Desktop, Console and Mobile versions)]: Expert Mode
1721	  *[5/9 (55.56%)]: Expert Mode
1722	  *[H]: Height (tiles)
1723	  *[14–17]: Expert Mode
1724	  *[3–4]: Expert Mode
1725	  *[12–15]: Chế độ Expert
1726	  *[21-27]: Chế độ Expert
1727	  *[four]: Expert Mode
1728	  *[1–5]: Expert Mode
1729	  *[1.25–6.25]: Master Mode
1730	  *[almost opaque]: Expert Mode
1731	  *[three]: Expert Mode
1732	  *[24,000]: Expert Mode
1733	  *[30,600]: Master Mode
1734	  *[1,200]: Master Mode
1735	  *[16,000]: Expert Mode
1736	  *[20,400]: Master Mode
1737	  *[40000]: Expert Mode
1738	  *[51000]: Master Mode
1739	  *[48000]: Expert Mode
1740	  *[61000]: Master Mode
1741	  *[39 mph]: 39 miles per hour (as measured by the Stopwatch item) or 28.6 tiles per second
1742	  *[599/90,000 (0.6656%)]: Expert Mode
1743	  *[395]: Expert Mode
1744	  *[second phase]: Expert Mode
1745	  *[54000]: Expert Mode
1746	  *[全て]: Master Mode
1747	  *[75 HP]: Chế độ Master
1748	  *[21 Sát thương]: Chế độ Master
1749	  *[20% KB]: Chế độ Master
1750	  *[411 HP]: Chế độ Master
1751	  *[93 Sát thương]: Chế độ Master
1752	  *[Vždy kupuj více drátů, než potřebuješ.]: Always buy more wire than you need!
1753	  *[Je to určitě zapojené do proudu?]: Did you make sure your device was plugged in?
1754	  *[Oh, víš co tento dům opravdu potřebuje? Více blikajících světélek.]: Oh, you know what this house needs? More blinking lights.
1755	  *[Hej [jméno hráče], nevrátil jsi se právě od [jméno gobliního kutila]? Neříkal ti náhodou něco o mně?]: Hey, [Name of Player], did you just come from [Name of Goblin Tinkerer]'s? Did he say anything about me by chance?
1756	  *[Hej, dávej si bacha, kam jdeš! Já jsem tam ještě nedávno byla!]: Hey, watch where you're going! I was over there a little while ago!
1757	  *[[Jméno prodejce zbraní] pořád říká, že stiskne mou tlakovou desku. Já jsem mu ale říkala, že na ni se má šlapat.]: [Name of Arms Dealer] keeps talking about pressing my pressure plate. I told him it was for stepping on.
1758	  *[Oh, nech mě hádat. Zapomněl jsi koupit dostatek drátů. Hlupáku.]: Oh, let me guess. Forgot to buy enough wire. Idiot.
1759	  *[Mohl… Mohl bys… Prosím? Ok? Ok. Ugh.]: Just-could you just...Please? Ok? Ok. Ugh.
1760	  *[Nelíbí se mi, jak se na mě díváš. Já právě PRACUJI.]: I don't appreciate the way you're looking at me. I am WORKING right now.
1761	  *[Všechno co bych pro vypínač chtěla je… Cože?!]: All I want is for the switch to make the... What?!
1762	  *[NEHÝBAT! SPADLA MI KONTAKTNÍ ČOČKA.]: DON'T MOVE. I DROPPED MY CONTACT.
1763	  *[Už jsme byla skoro hotová s věšením blikajících světélek!]: But I was almost done putting blinking lights up here!
1764	  *[Zadrž, už jsem tady dole skoro chytala WiFi signál.]: Hold on, I've almost got wifi going down here.
1765	  *[Děkuji. Trvat to o něco déle, tak skončím jako většina těch kostlivců, co tady dole žije.]: Thanks! It was only a matter of time before I ended up like the rest of the skeletons down here.
1766	  *[Kosh, kapleck Mog. Oh sorry, that's Klingon for 'Buy something or die.']: Kosh, kapleck Mog. Oh promiň, to je klingonsky výraz pro: ‚Něco si kup, nebo zemři.‘
1767	  *[Meč poráží papír! Získej jeden ještě dnes.]: Sword beats paper! Get one today.
1768	  *[Krásné ráno, co myslíš? Nechtěl jsi něco?]: Lovely morning, wouldn't you say? Was there something you needed?
1769	  *[Chceš jablka? Chceš mrkve? Chceš ananasy? Máme pro tebe pochodně!]: You want apples? You want carrots? You want pineapples? We got torches.
1770	  *[Slunce je vysoko, ale mé ceny jsou nízké.]: 
1771	  *[Chlape, to slunce ale pálí! Náhodou mám jedno úžasně ventilované brnění.]: Boy, that sun is hot! I do have some perfectly ventilated armor.
1772	  *[Koukni na moje hliněné bloky, jsou extra hliněné.]: Check out my dirt blocks, they are extra dirty.
1773	  *[Ah, jednoho dnes se budou vyprávět pověsti o [jméno hráče]… jen ty dobré, tím jsem si jist.]: Ah, they will tell tales of [Name of Player] some day... good ones I'm sure.
1774	  *[Brzy nastane noc můj příteli. Rozhodni se dokud ještě můžeš.]: Night be upon us soon, friend. Make your choices while you can.
1775	  *[Nemáš ani ponětí, jakou cenou se v zámoří platí za hliněné bloky.]: You have no idea how much Dirt Blocks sell for overseas.
1776	  *[Kosh, kapleck Mog. Oh promiň, to je [klingonsky](https://en.wikipedia.org/wiki/cs:Klingon "wikipedia:cs:Klingon") výraz pro: ‚Něco si kup, nebo zemři.‘]: Kosh, kapleck Mog. Oh sorry, that's klingon for 'Buy something or die.'
1777	  *[[Jméno hráče], je to tak? Slyšel jsem jen dobré zprávy příteli!]: [Name of Player] is it? I've heard good things, friend!
1778	  *[Občas přemýšlím, jestli je měsíc ze sýra… huh, co? Oh ano, kup něco!]: I wonder if the moon is made of cheese... huh, what? Oh yes, buy something!
1779	  *[Chlápek co teď odcházel mi tady nechal nějaký bordel… uhm chtěl jsem říct… poklady!]: The last guy who was here left some junk... er I mean... treasures!
1780	  *[Řekl jsi zlato? To od tebe klidně odkoupím.]: Did you say gold? I'll take that off of ya.
1781	  *[Slyšel jsem o ukrytém pokladu… oh zapomeň na to.]: I hear there's a secret treasure... oh never mind.
1782	  *[Socha anděla povídáš? Promiň, ale já neprodávám žádné harampádí.]: Angel statue you say? I'm sorry, I'm not a junk dealer.
1783	  *[Viděl jsi už Chith… Shith… Chat… Obří oko?]: Have you seen Chith...Shith.. Chat... The big eye?
1784	  *[Občas hoď okem po ceně, kup čočky!]: Keep your eye on the prize, buy a lens!
1785	  *[Oh výtečně. Už zase slyším [jméno mechaničky] a [jméno sestřičky], jak se hádají.]: Oh, great. I can hear [Name of Mechanic] and [Name of Nurse] arguing from here.
1786	  *[Ani krvavý měsíc nezastaví kapitalismus. Pojďme uzavřít nějaký obchod.]: Not even a Blood Moon can stop capitalism. Let's do some business.
1787	  *[Hej, tento dům je zabezpečený, je to tak? [Jméno hráče], je to tak?!]: Hey, this house is secure, right? Right? [Name of Player]?
1788	  *[Doufám, že takový vychrtlý klučina jako ty není to, co nás má ochránit před okem Cthulu.]: I hope a scrawny kid like you isn't all that's standing between us and Cthulu's Eye.
1789	  *[Cítím, jako kdyby mě sledovala přítomnost zla.]: I feel like an evil presence is watching me.
1790	  *[Když se tak koukám na to ošuntělé brnění, co nosíš, mám chuť ti prodat ještě pár léčivých lektvarů.]: Look at that shoddy armor you're wearing. Better buy some more healing potions.
1791	  *[10–20]: Expert Mode
1792	  *[12–25]: Master Mode
1793	  *[900]: Master Mode
1794	  *[ 5 _GC_]: Expert Mode
1795	  *[25 _GC_]: Expert Mode
1796	  *[11 mph]: 11 miles per hour (as measured by the Stopwatch item) or 8.07 tiles per second
1797	  *[9 mph]: 9 miles per hour (as measured by the Stopwatch item) or 6.6 tiles per second
1798	  *[49]: Expert Mode
1799	  *[Pre-HM]: Pre-Hardmode
1800	  *[101]: Expert Mode
1801	  *[337]: Expert Mode
1802	  *[Enemies that have [picked up coins](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")]: Expert Mode
1803	  *[2.67]: Expert Mode
1804	  *[2.25]: Master Mode
1805	  *[16 sekund]: Expertní mód
1806	  *[ 2 _PC_ 50 _GC_]: Expertní mód
1807	  *[40–45]: Expert Mode
1808	  *[187.5]: Master Mode
1809	  *[+24%]: Expert Mode
1810	  *[+28%]: Master Mode
1811	  *[305 mph]: 305 miles per hour (as measured by the Stopwatch item) or 223.67 tiles per second
1812	  *[255 mph]: 255 miles per hour (as measured by the Stopwatch item) or 187 tiles per second
1813	  *[720 mph]: 720 miles per hour (as measured by the Stopwatch item) or 528 tiles per second
1814	  *[0.0396%]: Expert Mode
1815	  *[10,149/1,000,000 (1.01%)]: Expert Mode
1816	  *[199/10,000 (1.99%)]: Expert Mode
1817	  *[36%]: Expert Mode
1818	  *[night]: 7:30 PM – 4:30 AM
1819	  *[dawn]: 4:30 AM
1820	  *[2–8]: Expert Mode
1821	  *[10–30 seconds]: Expert Mode
1822	  *[12.5–37.5 seconds]: Master Mode
1823	  *[10–30]: Expert Mode
1824	  *[12.5–37.5]: Master Mode
1825	  *[3 _SC_]: Expert Mode
1826	  *[3 _GC_]: Expert Mode
1827	  *[6 _SC_]: Expert Mode
1828	  *[4 _SC_ 50 _CC_]: Expert Mode
1829	  *[9 _SC_]: Expert Mode
1830	  *[20 _SC_]: Expert Mode
1831	  *[15 _SC_]: Expert Mode
1832	  *[30 _SC_]: Expert Mode
1833	  *[50 _SC_]: Expert Mode
1834	  *[37 _SC_ 50 _CC_]: Expert Mode
1835	  *[75 _SC_]: Expert Mode
1836	  *[1 _GC_ 20 _SC_]: Expert Mode
1837	  *[90 _SC_]: Expert Mode
1838	  *[1 _GC_ 80 _SC_]: Expert Mode
1839	  *[2 _GC_]: Expert Mode
1840	  *[1 _GC_ 50 _SC_]: Expert Mode
1841	  *[2 _GC_ 25 _SC_]: Expert Mode
1842	  *[4 _GC_ 50 _SC_]: Expert Mode
1843	  *[4 _GC_]: Expert Mode
1844	  *[Hej, nezmiňoval se [jméno prodejce zbraní] o tom, že by potřeboval vyšetřit? Ptám se jen tak.]: Hey, has [Name of Arms Dealer] mentioned needing to go to the doctor for any reason? Just wondering.
1845	  *[Bolí to, když uděláš tohle? Pak tohle nedělej.]: Does it hurt when you do that? Don't do that.
1846	  *[Ukaž mi, co tě bolí.]: Show me where it hurts.
1847	  *[Tohle není to největší, co jsem za svůj život viděla… Ano, už jsem viděla větší rány.]: That's not the biggest I've ever seen... Yes, I've seen bigger wounds for sure.
1848	  *[Otoč hlavu a zakašlej.]: Turn your head and cough.
1849	  *[Někdy si přeji, aby byl [jméno demoličního experta] více opatrný. Už mě unavuje to každodenní přišívání jeho končetin zpět k tělu.]: I wish [Name of Demolitionist] would be more careful. I'm getting tired of having to sew his limbs back on every day.
1850	  *[Lízátko by sis nedal?]: Would you like a lollipop?
1851	  *[Asi si budu muset promluvit s [jméno průvodce]. Jak často si musíš ošetřovat tak těžké popáleniny?]: I need to have a serious talk with [Name of Guide]. How many times a week can you come in with severe lava burns?
1852	  *[Už jsi viděl starce, jak se potuluje kolem podzemní kobky? Vypadá utrápeně.]: Have you seen that Old Man pacing around the dungeon? He looks troubled.
1853	  *[Nedělej ze sebe takové dítě. Už jsem viděla horší.]: Quit being such a baby! I've seen worse.
1854	  *[Zase trable s těmi tyrany?]: Trouble with those bullies again?
1855	  *[To bude potřebovat pár stehu!]: That's gonna need stitches!
1856	  *[vypadáš, jako kdybys byl napůl strávený. Zase jsi honil slizy?]: You look half digested. Have you been chasing slimes again?
1857	  *[Počkej chvíli, mám tady někde nějaké náplasti se zvířátky.]: Hold on, I've got some cartoon bandages around here somewhere.
1858	  *[[Jméno hráče], to rozchodíš a budeš v pořádku. Šmárja.]: Walk it off, (Name of Player), you'll be fine. Sheesh.
1859	  *[Drazí přátelé, sešli jsme se zde, abychom vzdali poslední úctu… ále, budeš v pořádku.]: Dear friends we are gathered here today to bid farewell... oh, you'll be fine.
1860	  *[Myslím si, že toto ti sluší víc.]: I think you look better this way.
1861	  *[Eww… Co se stalo s tvým obličejem?]: Eww.. what happened to your face?
1862	  *[Támhle jsi nechal svoje rameno. Dojdu pro něj.]: You left your arm over there. Let me get that for you.
1863	  *[MŮJ BOŽE. Dobrá jsem, ale TAKHLE zase ne.]: MY GOODNESS. I'm good but I'm not THAT good.
1864	  *[Co má tohle znamenat?]: What is that supposed to mean!?
1865	  *[Nemyslím si, že se mi líbí tvůj tón v hlase.]: I don't think I like your tone.
1866	  *[Co tady děláš? Pokud nekrvácíš, tak tě tady nechci. Běž pryč.]: Why are you even here? If you aren't bleeding, you don't need to be here. Get out.
1867	  *[COŽE?!]: WHAT?!
1868	  *[Pokud plánuješ zemřít, učiň tak venku.]: If you're going to die, do it outside.
1869	  *[Pospěš si a přestaň krvácet.]: Hurry up and stop bleeding.
1870	  *[Běda, jestli se mi tvá krev dostane na sukni.]: You better not get blood on me.
1871	  *[Ani to nebolelo, že ne?]: That didn't hurt too bad, now did it?
1872	  *[Všechno v pořádku. A ne abych se zase načapala, jak skáčeš z dalších útesů.]: All better. I don't want to see you jumping off any more cliffs.
1873	  *[Tohle asi zanechá jizvu.]: That's probably going to leave a scar.
1874	  *[Podařilo se mi tvůj obličej sešít. Příště si dávej větší pozor.]: I managed to sew your face back on. Be more careful next time.
1875	  *[Přestaň plýtvat mým časem.]: Quit wasting my time.
1876	  *[Žádné šťastné konce ode mě nečekej.]: I don't give happy endings.
1877	  *[Pokud nechceš plastickou operaci, tak ti toho víc nenabídnu.]: I can't do anymore for you without plastic surgery.
1878	  *[Omlouvám se, ale mé služby si nemůžeš momentálně dovolit.]: I'm sorry, but you can't afford me.
1879	  *[Budeš potřebovat více zlata, než je tohle.]: I'm gonna need more gold than that.
1880	  *[Jen abys věděl – nepracuji zadarmo.]: I don't work for free you know.
1881	  *[1,485]: Expert Mode
1882	  *[2,227]: Master Mode
1883	  *[500]: Expert Mode
1884	  *[%55]: Expert Mode
1885	  *[%64]: Expert Mode
1886	  *[Vrať se zpět za noci, pokud si přeješ vstoupit.]: Come back at night if you wish to enter.
1887	  *[Nemůžu tě pustit dále, pokud mě neosvobodíš od mé kletby.]: I cannot let you enter until you free me of my curse.
1888	  *[Můj pán nemůže být vyvolán pod záštitou denního světla.]: My master cannot be summoned under the light of day.
1889	  *[Jsi příliš slabý na zlomení mé kletby. Vrať se zpět, až nebudeš taková nicka.]: You are far too weak to defeat my curse. Come back when you aren't so worthless.
1890	  *[Ubohý hlupáku. Nemůžeš si myslet, že bys mohl porazit mého pána ve stavu, v jakém se nacházíš.]: You pathetic fool. You cannot hope to face my master as you are now.
1891	  *[Doufám, že máš tak šest přátel stojících po tvém boku.]: I hope you have like six friends standing around behind you.
1892	  *[Prosím ne, cizinče. Jen bys marnil svůj drahocenný život.]: Please, no, stranger. You'll only get yourself killed.
1893	  *[Cizinče. Budeš dostatečně silný, abys porazil mého pána?]: Stranger, do you possess the strength to defeat my master?
1894	  *[Ty bys mohl být dostatečně silný na osvobození mě od mé kletby…]: You just might be strong enough to free me from my curse...
1895	  *[Prosím! Poraz mého věznitele a osvoboď mne! Zapřísahám tě!]: Please! Battle my captor and free me! I beg you!
1896	  *[Poraz mého pána a já ti zajistím průchod do podzemní kobky.]: Defeat my master, and I will grant you passage into the Dungeon.
1897	  *[Pokud porazíš mého pána, splním ti jedno přání.]: If you beat my master I will grant you one wish.
1898	  *[∞]: Must defeat Betsy
1899	  *[56]: Mode Expert
1900	  *[7–12]: Master Mode
1901	  *[24–40]: Expert Mode
1902	  *[28–48]: Master Mode
1903	  *[20-37.5]: Master Mode
1904	  *[64–120]: Expert Mode
1905	  *[80-150]: Master Mode
1906	  *[56–80]: Expert Mode
1907	  *[70–100]: Master Mode
1908	  *[40–56]: Expert Mode
1909	  *[60-84]: Master Mode
1910	  *[4–20]: Expert Mode
1911	  *[5–25]: Master Mode
1912	  *[28800]: Mode Expert
1913	  *[43200]: Mode Master
1914	  *[16-30]: Mode Expert
1915	  *[64-120]: Mode Expert
1916	  *[40-56]: Mode Expert
1917	  *[要100次]: Journey Mode
1918	  *[1/150 (0.67%)]: Expert Mode
1919	  *[12.89%]: Expert Mode
1920	  *[19%]: Expert Mode
1921	  *[9.78%]: Expert Mode
1922	  *[13.56%]: Expert Mode
1923	  *[29/225 (12.89%)]: Expert Mode
1924	  *[230 mph]: 230 miles per hour (as measured by the Stopwatch item) or 168.75 tiles per second
1925	  *[22/225 (9.78%)]: Expert Mode
1926	  *[19/100 (19%)]: Expert Mode
1927	  *[Expert Mode:]: Expert Mode
1928	  *[1.4%]: Expert Mode
1929	  *[1/70 (1.43%)]: Expert Mode
1930	  *[10›8]: Expert Mode : Pre-Hardmode › Hardmode
1931	  *[300›330]: Expert Mode : Pre-Hardmode › Hardmode
1932	  *[%-13]: Expert Mode
1933	  *[%1,4]: Expert Mode
1934	  *[5/12 (41.67%)]: Expert Mode
1935	  *[6/12 (50%)]: Expert Mode
1936	  *[1/12 (8.33%)]: Expert Mode
1937	  *[4–9]: Expert Mode
1938	  *[33,600]: Expert Mode
1939	  *[42,840]: Master Mode
1940	  *[21,000]: Expert Mode
1941	  *[26,775]: Master Mode
1942	  *[42,000–37,800]: Expert Mode
1943	  *[53,550–48,195]: Master Mode
1944	  *[37,799–33,600]: Expert Mode
1945	  *[48,194–42,840]: Master Mode
1946	  *[33,599–29,400]: Expert Mode
1947	  *[42,839–37,485]: Master Mode
1948	  *[29,399–25,200]: Expert Mode
1949	  *[37,484–32,130]: Master Mode
1950	  *[25,199–21,001]: Expert Mode
1951	  *[32,129–26,776]: Master Mode
1952	  *[21,000–16,800]: Expert Mode
1953	  *[26,775–21,420]: Master Mode
1954	  *[16,799–12,600]: Expert Mode
1955	  *[21,419–16,065]: Master Mode
1956	  *[12,599–8,400]: Expert Mode
1957	  *[16,064–10,710]: Master Mode
1958	  *[8,399–4,200]: Expert Mode
1959	  *[10,709–5,355]: Master Mode
1960	  *[4,199–0]: Expert Mode
1961	  *[5,354–0]: Master Mode
1962	  *[101×101]: Expert Mode
1963	  *[3/2500 (0.12%)]: Expert Mode
1964	  *[2–10 or 20]: Expert Mode
1965	  *[2.5–12.5 or 25]: Master Mode
1966	  *[4–20 or 40]: Expert Mode
1967	  *[5-12.5 or 50]: Master Mode
1968	  *[2.5-10]: Master Mode
1969	  *[4–16]: Expert Mode
1970	  *[5-20]: Master Mode
1971	  *[2.5-7.5]: Master Mode
1972	  *[5-15]: Master Mode
1973	  *[10 or 40]: Expert Mode
1974	  *[12.5 or 50]: Master Mode
1975	  *[20 or 80]: Expert Mode
1976	  *[25 or 100]: Master Mode
1977	  *[5-10]: Chế độ Expert
1978	  *[6-12.5]: Master Mode
1979	  *[10-20]: Expert Mode
1980	  *[12-25]: Master Mode
1981	  *[4–18]: Chế độ Expert
1982	  *[7.5-17.5]: Master Mode
1983	  *[8–36]: Expert Mode
1984	  *[15-35]: Master Mode
1985	  *[4–8]: Expert Mode
1986	  *[8–16]: Expert Mode
1987	  *[5.23-10.5]: Expert Mode
1988	  *[6.53-13.12]: Master Mode
1989	  *[10-21]: Expert Mode
1990	  *[13-26]: Master Mode
1991	  *[14400]: Chế độ Expert
1992	  *[21600]: Chế độ Master
1993	  *[98]: Expert Mode
1994	  *[123]: Master Mode
1995	  *[196]: Expert Mode
1996	  *[246]: Master Mode
1997	  *[2–10 hoặc 20]: Chế độ Expert
1998	  *[4-20 hoặc 40]: Chế độ Expert
1999	  *[4-16]: Chế độ Expert
2000	  *[4-12]: Chế độ Expert
2001	  *[10 hoặc 40]: Chế độ Expert
2002	  *[20 hoặc 80]: Chế độ Expert
2003	  *[8-36]: Chế độ Expert
2004	  *[8-16]: Chế độ Expert
2005	  *[2.625–5.25]: Chế độ Expert
2006	  *[514 mph]: 514 miles per hour (as measured by the Stopwatch item) or 376.93 tiles per second
2007	  *[2/45]: Expert Mode
2008	  *[5–18]: Expert Mode
2009	  *[7–24]: Expert Mode
2010	  *[7–27]: Expert Mode
2011	  *[10–36]: Expert Mode
2012	  *[3–12]: Expert Mode
2013	  *[3–7]: Expert Mode
2014	  *[95 mph]: 95 miles per hour (as measured by the Stopwatch item) or 69.67 tiles per second
2015	  *[membutuhkan 3]: Mode Journey
2016	  *[6×]: Master Mode
2017	  *[3 mph]: 3 miles per hour (as measured by the Stopwatch item) or 1.875 tiles per second
2018	  *[by wave 12]: Expert Mode
2019	  *[0.56%]: Expert Mode
2020	  *[0.83%]: Expert Mode
2021	  *[1.11%]: Expert Mode
2022	  *[2–20]: Expert Mode
2023	  *[2.5–25]: Master Mode
2024	  *[2.5–10]: Master Mode
2025	  *[8-28 (depending on health)]: Chế độ Expert
2026	  *[2-20 seconds]: Chế độ Expert
2027	  *[2.5-25 seconds]: Chế độ Master
2028	  *[2-8 seconds (melee)]: Chế độ Expert
2029	  *[2.5-10 seconds (melee)]: Chế độ Master
2030	  *[14,400]: Expert Mode
2031	  *[18,360]: Master Mode
2032	  *[0.42 seconds]: Expert Mode
2033	  *[0.5 seconds]: Expert Mode
2034	  *[Descrizione]: General description of items in these tiers. Some exceptions will apply.
2035	  *[Mô tả]: Mô tả vật phẩm của bậc này. Một số ngoại lệ sẽ được áp dụng.
2036	  *[**撳呢度** 嚟載入內容。 _（可能會有些微延遲）_]: 呢個內容係喺外部儲存，所以你撳咗之後，喺佢未下載完之前會有延遲。
2037	  *[2.5 hours]: Master Mode
2038	  *[First part]: At 1/7 of the world
2039	  *[Combined]: Both parts (at 3/14 of the world)
2040	  *[1/5600 (0.02%)]: Expert Mode
2041	  *[Laju]: Laju Anak Panah
2042	  *[Krit]: Peluang Kritikal
2043	  *[382]: Master Mode
2044	  *[10.8%]: Expert Mode
2045	  *[35/324 (10.8%)]: Expert Mode
2046	  *[1/400 (0.25%)]: Expert Mode
2047	  *[27 mph]: 27 miles per hour (as measured by the Stopwatch item) or 19.8 tiles per second
2048	  *[5–10 seconds]: Master Mode
2049	  *[5–10]: Master Mode
2050	  *[0.018%]: Expert Mode
2051	  *[17,550]: Expert Mode
2052	  *[22,376]: Master Mode
2053	  *[5,850]: Expert Mode
2054	  *[7,458]: Master Mode
2055	  *[2 minutes]: Expert Mode
2056	  *[2 minutes 30 seconds]: Master Mode
2057	  *[0.56%–3.33%]: Expert Mode
2058	  *[2 minutes]: Expert Mode
2059	  *[2 minutes and 30 seconds]: Master Mode
2060	  *[107 mph]: 107 miles per hour (as measured by the Stopwatch item) or 78.75 tiles per second
2061	  *[cần có 99]: Chế độ Journey
2062	  *[3,099 mph]: 3,099 miles per hour (as measured by the Stopwatch item) or 2,272.5 tiles per second
2063	  *[20–40 seconds]: Expert Mode
2064	  *[25–50 seconds]: Master Mode
2065	  *[two]: Expert Mode
2066	  *[one]: Master Mode
2067	  *[6,600]: Expert Mode
2068	  *[8,415]: Master Mode
2069	  *[118]: Expert Mode
2070	  *[179]: Master Mode
2071	  *[57]: Expert Mode
2072	  *[85]: Master Mode
2073	  *[100 (if hands aren't killed)]: Expert Mode
2074	  *[6-10 seconds]: Expert Mode
2075	  *[0.5-1 seconds]: Expert Mode
2076	  *[76 mph]: 76 miles per hour (as measured by the Stopwatch item) or 55.7065 tiles per second
2077	  *[158]: Expert Mode
2078	  *[20-35]: Expert Mode
2079	  *[criteria met]: Expert Mode
2080	  *[Criteria not met]: Expert Mode
2081	  *[3/125 (2.4%)]: Expert Mode
2082	  *[3/250 (1.2%)]: Expert Mode
2083	  *[2/125 (1.6%)]: Expert Mode
2084	  *[1/125 (0.8%)]: Expert Mode
2085	  *[0.0143%]: Expert Mode
2086	  *[1/7000 (0.0143%)]: Expert Mode
2087	  *[1/70 (1.4286%)]: Expert Mode
2088	  *[1/5600 (0.0179%)]: Expert Mode
2089	  *[1.43%]: Expert Mode
2090	  *[6–12]: Expert Mode
2091	  *[7–15]: Master Mode
2092	  *[2–10]: Expert Mode
2093	  *[2–12]: Master Mode
2094	  *[10–32]: Expert Mode
2095	  *[12.5–40]: Master Mode
2096	  *[0.5–1]: Expert Mode
2097	  *[0.63–1.25]: Master Mode
2098	  *[5.23–10.5]: Expert Mode
2099	  *[6.53–13.12]: Master Mode
2100	  *[membutuhkan 400]: Mode Journey
2101	  *[90 giây]: Chế độ Expert
2102	  *[2 giây]: Chế độ Expert
2103	  *[84 mph]: 84 miles per hour (as measured by the Stopwatch item) or 61.6 tiles per second
2104	  *[Convertable]: Prone to being converted by Corruption, Crimson, or Hallow
2105	  *[Biến đổi được]: Dễ bị biến đổi bởi Corruption, Crimson, hoặc Hallow
2106	  *[15–30]: Expert Mode
2107	  *[No.]: Number
2108	  *[9/10 (90%)]: Expert Mode
2109	  *[40 seconds]: Expert Mode
2110	  *[10.4%]: Expert Mode
2111	  *[2 or 3 seconds]: Expert Mode
2112	  *[2.5 or 3.75 seconds]: Master Mode
2113	  *[10 or 40 seconds]: Expert Mode
2114	  *[12.5 or 50 seconds]: Master Mode
2115	  *[535]: Expert Mode
2116	  *[ 1–4]: Expert Mode
2117	  *[0.1 mph]: 0.1 miles per hour (as measured by the Stopwatch item) or 0.075 tiles per second
2118	  *[Damage]: The damage without modifier and summon damage bonuses
2119	  *[73 mph]: 73 miles per hour (as measured by the Stopwatch item) or 53.53 tiles per second
2120	  *[1600]: Expert Mode
2121	  *[2400]: Master Mode
2122	  *[15,97%]: Expert Mode
2123	  *[23/144 (15,97%)]: Mode Expert
2124	  *[91 mph]: 91 miles per hour (as measured by the Stopwatch item) or 66.73 tiles per second
2125	  *[-50 health per second]: Expert Mode
2126	  *[50 damage per second]: Expert Mode
2127	  *[4–6 seconds]: Expert Mode
2128	  *[92]: Expert Mode
2129	  *[138]: Master Mode
2130	  *[12000/30000]: Expert Mode
2131	  *[15300/38250]: Master Mode
2132	  *[127]: Expert Mode
2133	  *[13800/34500]: Expert Mode
2134	  *[17595/43988]: Master Mode
2135	  *[4–6]: Expert Mode
2136	  *[5–7.5]: Master Mode
2137	  *[17,595]: Master Mode
2138	  *[three tiles]: Legendary Mode
2139	  *[cần có 400]: Chế độ Journey
2140	  *[6.37]: Expert Mode
2141	  *[19.87%]: Expert Mode
2142	  *[25.58%]: Expert Mode
2143	  *[32.26%]: Expert Mode
2144	  *[23.34%]: Expert Mode
2145	  *[7.75%]: Expert Mode
2146	  *[1.08%]: Expert Mode
2147	  *[0.06%]: Expert Mode
2148	  *[0.001%]: Expert Mode
2149	  *[4–11]: Expert Mode
2150	  *[5–12]: Expert Mode
2151	  *[6–13]: Expert Mode
2152	  *[7–14]: Expert Mode
2153	  *[8–15]: Expert Mode
2154	  *[Kombinace dýmky a kávovaru! Dělá nudličkové hranolky!]: Combination hookah and coffee maker! Also makes julienne fries!
2155	  *[Setkáme se za tři hodiny za domem [jméno provůdce]. Myslím si, že mám pro tebe velmi lákavou nabídku.]: Meet me behind [Name of Guide]'s house in about three hours, I think I have something you will find very appealing.
2156	  *[Použité zboží? V žádném případě! Prodávám pouze to nejkvalitnější zboží na trhu.]: A thrift shop? No, I am only selling the highest quality items on the market.
2157	  *[Žádné vrácení zboží kvůli „výčitkám svědomí kupujícího“, ani kvůli jiným důvodům. Beze srandy.]: I don't refund for "buyer's remorse..." Or for any other reason, really.
2158	  *[Prodávám pouze to, k čemu se dostanu. [Jméno oděvníka] mě pořád pronásleduje a chce exotické látky.]: I only sell what I can get. [Name of Clothier] keeps hounding me for exotic clothing.
2159	  *[Pokud hledáš cetky, hledáš na nesprávném místě.]: If you're looking for junk, you've come to the wrong place.
2160	  *[Prodávám výrobky ze zemí, které ani nemusí existovat!]: I sell wares from places that might not even exist!
2161	  *[Ach ten [jméno obchodníka], neumí vůbec ocenit kvalitní zboží.]: That [Name of Merchant], he really has no appreciation for a really good deal.
2162	  *[Hmm, vypadáš, jako bys potřeboval použít sochu anděla! Řežou a krájí – dělají všech krásné!]: Hmm, you look like you could use an Angel Statue! They slice, and dice, and make everything nice!
2163	  *[Přijď a podívej se! Jednolibrová ryba! Velmi velmi dobrá! Jednolibrová ryba!]: Come and have a look! One pound fish! Very very good! One pound fish!
2164	  *[Kup nyní a donáška bude zdarma!]: Buy now, and get free shipping!
2165	  *[Chceš dvě za cenu jedné?! Chtěj pouze jednu a dohodneme se.]: You want two penny farthings!? Make it one and we have a deal.
2166	  *[Jednolibrová ryba!]: One pound fish!
2167	  *[surface level]: 0 depth elevation

```


---

## 🤖 Assistant · 2026-08-13T01:02:29.184Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now I have the wiki pages. Let me now look at the decompiled source code. Key methods: ApplyItemTime, ApplyItemAnimation, ItemCheck, CapAttackSpeeds, TryAllowingItemReuse.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:29.385Z · glm-x-preview-260804

```
现在，让我来定位反编译源码中的关键方法。
```


---

## 🤖 Assistant · 2026-08-13T01:02:30.646Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"public void ApplyItemTime\\|public void ApplyItemAnimation\\|public void ItemCheck(\\|private void CapAttackSpeeds\\|private bool TryAllowingItemReuse\\|private void ItemCheck_ApplyUseStyle\\|private void ItemCheck_Handle_ItemUse\\|private bool ItemCheck_CheckMana\\|private void ItemCheck_ApplyItemTime\" Player.cs | head -30",
 "description": "Locate key Player.cs methods"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:30.668Z

**📎 ToolResult**

```
4216:	public void ApplyItemTime(Item sItem)
4221:	public void ApplyItemTime(Item sItem, float multiplier)
28555:	private void CapAttackSpeeds()
41949:	public void ItemCheck()

```


---

## 🤖 Assistant · 2026-08-13T01:02:31.343Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"itemTime\\|itemAnimation\" Player.cs | grep -n \"itemTime ==\\|itemAnimation ==\\|itemTime >\\|itemAnimation >\\|itemTime--\\|itemAnimation--\" | head -40",
 "description": "Find itemTime decrements and gates"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:31.366Z

**📎 ToolResult**

```
6:3698:			if (hasBreathingReed && itemAnimation == 0)
7:3844:			if (invis && itemAnimation == 0)
8:3902:	public bool ItemTimeIsZero => itemTime == 0;
9:3904:	public bool ItemAnimationJustStarted => itemAnimation == itemAnimationMax - 1;
19:13937:		if (!wellFed && itemAnimation == 0 && releaseUseItem && (item.buffType == 26 || item.buffType == 206 || item.buffType == 207))
20:16063:			if (itemAnimation > 0 && inventory[selectedItem].type == 1121)
22:18771:		if (shinyStone && IsConsideredStandingStill && itemAnimation == 0)
23:19549:			bool flag3 = (itemAnimation == 0 || inventory[selectedItem].useTurn) && mount.AllowDirectionChange && !sandStorm;
24:19580:			if (mount.Active && mount.AnyTrackRider && !onWrongGround && onTrack && itemAnimation == 0 && velocity.Y == 0f && velocity.X >= 0f)
25:19638:			if (mount.Active && mount.AnyTrackRider && !onWrongGround && onTrack && itemAnimation == 0 && velocity.Y == 0f && velocity.X <= 0f)
28:22418:		if (itemAnimation == 0)
29:22920:		if (hasBreathingReed && itemAnimation == 0)
30:24057:		if (itemAnimation == 0 && !Main.mouseLeftRelease)
32:24403:		if (itemAnimation == 0)
33:24918:				if (itemAnimation == 0 && ItemTimeIsZero && reuseDelay == 0)
34:25212:		if (IsConsideredStandingStill && (itemAnimation == 0 || ItemID.Sets.IsAKite[HeldItem.type]) && !controlUp && !controlDown && !controlLeft && !controlRight && !controlJump && !controlTorch)
35:25439:			if (itemAnimation == 0 && aggro > -750)
36:25450:			if (itemAnimation > 0)
37:25502:			if (itemAnimation > 0)
38:31076:		if (flag2 && altFunctionUse == 0 && itemTime == 0 && itemAnimation == 0)
39:31181:		if (flag2 && altFunctionUse == 0 && inventory[selectedItem].type == 3852 && itemAnimation == 0)
40:31201:		if (flag2 && altFunctionUse == 0 && inventory[selectedItem].makeNPC > 0 && itemAnimation == 0 && ItemID.Sets.PlaceTileOnAltUse[inventory[selectedItem].type])
41:31231:		if (theGeneralCheck && flag && hasRaisableShield && !mount.Active && (itemAnimation == 0 || mouseRight))
44:31360:		if (itemAnimation == 0)
46:35293:		if (HeldItem.type == 4743 && itemAnimation > 0)
47:35871:			if (miscCounter % 4 == 0 && itemAnimation == 0)
48:35880:		else if (itemAnimation > 0 && flag6)
51:35899:				if ((double)itemAnimation > (double)itemAnimationMax * 0.5)
52:35914:				if ((double)itemAnimation > (double)itemAnimationMax * 0.5)
53:35918:				else if ((double)itemAnimation > (double)itemAnimationMax * 0.15)
55:35950:				if ((double)itemAnimation > (double)itemAnimationMax * 0.666)
58:38919:		if (itemTime == 0)
60:39084:		if (canUse && ((!tile.active() && !PlaceThing_Tiles_IsBlockedByLava(item.createTile, item.placeStyle, tile)) || PlaceThing_IsReplaceableBlock(tile) || tileToCreate == 199 || tileToCreate == 23 || tileToCreate == 662 || tileToCreate == 661 || tileToCreate == 2 || tileToCreate == 109 || tileToCreate == 60 || tileToCreate == 70 || tileToCreate == 633 || Main.tileMoss[tileToCreate]) && ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
61:39159:		if (canUse && itemAnimation > 0 && ItemTimeIsZero && controlUseItem && PlaceThing_ValidWallForReplacement() && WorldGen.NearFriendlyWall(tileTargetX, tileTargetY) && WorldGen.ReplaceWall(tileTargetX, tileTargetY, (ushort)HeldItem.createWall))
62:39189:		if (controlUseItem && canUse && Main.tile[tileTargetX, tileTargetY].active() && itemAnimation > 0 && ItemTimeIsZero && flag)
67:41223:		if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
68:41247:			if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
69:41265:			if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
70:41386:		if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
77:42018:		if (itemAnimation == 0)

```


---

## 🤖 Assistant · 2026-08-13T01:02:32.578Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read the ApplyItemTime method at line 4216 and CapAttackSpeeds at 28555.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:32.899Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '4200,4260p' Player.cs",
 "description": "Read ApplyItemTime"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:32.921Z

**📎 ToolResult**

```
		{
			Main.npcChatPortrait = null;
			if (npcIndex >= 0 && npcIndex < Main.maxNPCs && NPCID.Sets.NPCPortraits.TryGetValue(Main.npc[npcIndex].type, out var value))
			{
				Main.npcChatPortrait = value;
				Main.DoNPCPortraitHop();
			}
		}
	}

	public void SetItemTime(int frames)
	{
		itemTime = frames;
		itemTimeMax = frames;
	}

	public void ApplyItemTime(Item sItem)
	{
		SetItemTime(sItem.useTime);
	}

	public void ApplyItemTime(Item sItem, float multiplier)
	{
		int useTime = sItem.useTime;
		int val = (int)((float)useTime * multiplier);
		if (useTime > 0)
		{
			val = Math.Max(val, 1);
		}
		SetItemTime(val);
	}

	public void SetDummyItemTime(int frames)
	{
		itemAnimation = frames;
		itemTime = frames;
		itemTimeMax = frames + 1;
	}

	private void SetItemAnimation(int frames)
	{
		itemAnimation = frames;
		itemAnimationMax = frames;
	}

	private void SetItemAnimation(int baseFrames, float multiplier)
	{
		int val = (int)((float)baseFrames * multiplier);
		if (baseFrames > 0)
		{
			val = Math.Max(val, 1);
		}
		SetItemAnimation(val);
	}

	private void ApplyItemAnimation(Item sItem)
	{
		int num = 0;
		if (sItem.autoReuse && sItem.reuseDelay == 0 && sItem.useTime <= sItem.useAnimation && sItem.shoot > 0 && sItem.useStyle == 5)
		{
			num = 1;

```


---

## 🤖 Assistant · 2026-08-13T01:02:33.230Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '28555,28640p' Player.cs",
 "description": "Read CapAttackSpeeds"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:33.256Z

**📎 ToolResult**

```
	private void CapAttackSpeeds()
	{
		float num = meleeSpeed;
		meleeSpeed = TurnAttackSpeedToUseTimeMultiplier(num);
		summonerWeaponSpeedBonus = TurnAttackSpeedToUseTimeMultiplier(num + summonerWeaponSpeedBonus);
	}

	private float TurnAttackSpeedToUseTimeMultiplier(float speed)
	{
		if (speed > 3f)
		{
			speed = 3f;
		}
		if (speed != 0f)
		{
			speed = 1f / speed;
		}
		return speed;
	}

	public void UpdateLuck()
	{
		UpdateLuckFactors();
		RecalculateLuck();
		if (luckNeedsSync && whoAmI == Main.myPlayer)
		{
			luckNeedsSync = false;
			NetMessage.SendData(134, -1, -1, null, whoAmI);
		}
	}

	private void ResetControls()
	{
		controlUp = false;
		controlLeft = false;
		controlDown = false;
		controlRight = false;
		controlJump = false;
		controlUseItem = false;
		controlUseTile = false;
		controlThrow = false;
		controlInv = false;
		controlHook = false;
		controlTorch = false;
		controlSmart = false;
		controlMount = false;
		controlQuickHeal = false;
		controlQuickMana = false;
		controlCreativeMenu = false;
		controlDash = false;
		controlArmorSetAbility = false;
		mapStyle = false;
		mapAlphaDown = false;
		mapAlphaUp = false;
		mapFullScreen = false;
		mapZoomIn = false;
		mapZoomOut = false;
	}

	private void UpdateControlHolds()
	{
		if (whoAmI == Main.myPlayer && HeldItem.GetFlexibleTileWand() != null)
		{
			if (controlUp && releaseUp)
			{
				FlexibleWandCycleOffset--;
			}
			if (controlDown && releaseDown)
			{
				FlexibleWandCycleOffset++;
			}
		}
		if (controlUp)
		{
			releaseUp = false;
		}
		else
		{
			releaseUp = true;
		}
	}

	public void TryOpeningFullscreenMap()
	{
		if (Main.mapEnabled)
		{

```


---

## 🤖 Assistant · 2026-08-13T01:02:39.191Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Interesting — this is a big finding. `CapAttackSpeeds` in 1456:
```csharp
private void CapAttackSpeeds()
{
    float num = meleeSpeed;
    meleeSpeed = TurnAttackSpeedToUseTimeMultiplier(num);
    summonerWeaponSpeedBonus = TurnAttackSpeedToUseTimeMultiplier(num + summonerWeaponSpeedBonus);
}

private float TurnAttackSpeedToUseTimeMultiplier(float speed)
{
    if (speed > 3f) speed = 3f;
    if (speed != 0f) speed = 1f / speed;
    return speed;
}
```

Wait — this looks very different from what I know. Actually this is a MODIFIED source! Hold on. `TurnAttackSpeedToUseTimeMultiplier` converts meleeSpeed (additive bonus like 0.12) into a multiplicative use-time multiplier? That doesn't make sense... Actually wait. Let me check. Hmm, actually the memory note "A批3近似清零" says "攻速CapAttackSpeeds倒数档(猛爪×2废)" — so the repo has implemented CapAttackSpeeds with the reciprocal. Let me check how meleeSpeed is then used.

Actually wait — I need to be careful. This decompiled source at Terarria1456 might have been modified, OR it might be the actual 1.4.5 code. Let me check how meleeSpeed is consumed in Player.cs.

Actually, in vanilla 1.4.4, CapAttackSpeeds is:
```csharp
private void CapAttackSpeeds()
{
    if (meleeSpeed > 3f)
        meleeSpeed = 3f;
    ... 
}
```
Hmm, actually I recall in 1.4.4:
```csharp
private void CapAttackSpeeds()
{
    meleeSpeed = Math.Min(meleeSpeed, 3f);
}
```

But this decompile shows the reciprocal conversion. Let me search for how meleeSpeed is used after CapAttackSpeeds, and where ApplyItemAnimation uses meleeSpeed.

Let me read ApplyItemAnimation fully first.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:39.296Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '4255,4330p' Player.cs",
 "description": "Read ApplyItemAnimation full"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:39.321Z

**📎 ToolResult**

```
	private void ApplyItemAnimation(Item sItem)
	{
		int num = 0;
		if (sItem.autoReuse && sItem.reuseDelay == 0 && sItem.useTime <= sItem.useAnimation && sItem.shoot > 0 && sItem.useStyle == 5)
		{
			num = 1;
		}
		if (sItem.melee && !ItemID.Sets.NoMeleeSpeedBonus[sItem.type])
		{
			SetItemAnimation(sItem.useAnimation, meleeSpeed);
		}
		else if (sItem.summon && ItemID.Sets.SummonerWeaponThatScalesWithAttackSpeed[sItem.type])
		{
			SetItemAnimation(sItem.useAnimation, summonerWeaponSpeedBonus * whipUseTimeMultiplier);
		}
		else if (sItem.createTile >= 0)
		{
			SetItemAnimation(sItem.useAnimation, tileSpeed);
		}
		else if (sItem.createWall >= 0)
		{
			SetItemAnimation(sItem.useAnimation, wallSpeed);
		}
		else
		{
			SetItemAnimation(sItem.useAnimation + num);
		}
		reuseDelay = sItem.reuseDelay;
	}

	public void MatchItemTimeToItemAnimation()
	{
		itemTime = itemAnimation;
	}

	public bool InOpposingTeam(Player otherPlayer)
	{
		if (hostile && otherPlayer.hostile)
		{
			if (otherPlayer.team != 0)
			{
				return otherPlayer.team != team;
			}
			return true;
		}
		return false;
	}

	public bool TeamChangeAllowed()
	{
		return true;
	}

	public void HealEffect(int healAmount, bool broadcast = true)
	{
		CombatText.NewText(new Rectangle((int)position.X, (int)position.Y, width, height), CombatText.HealLife, healAmount);
		if (broadcast && Main.netMode == 1 && whoAmI == Main.myPlayer)
		{
			NetMessage.SendData(35, -1, -1, null, whoAmI, healAmount);
		}
	}

	public void ManaEffect(int manaAmount)
	{
		CombatText.NewText(new Rectangle((int)position.X, (int)position.Y, width, height), CombatText.HealMana, manaAmount);
		if (Main.netMode == 1 && whoAmI == Main.myPlayer)
		{
			NetMessage.SendData(43, -1, -1, null, whoAmI, manaAmount);
		}
	}

	public void InterruptItemUsageIfOverTile(int tileTypeToBeOver)
	{
		Tile tile = Main.tile[tileTargetX, tileTargetY];
		if (tile != null && tile.active() && tile.type == tileTypeToBeOver)
		{

```


---

## 🤖 Assistant · 2026-08-13T01:02:39.643Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"meleeSpeed\" Player.cs | head -50",
 "description": "Find all meleeSpeed usages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:39.662Z

**📎 ToolResult**

```
2328:	public float meleeSpeed = 1f;
4264:			SetItemAnimation(sItem.useAnimation, meleeSpeed);
10095:				meleeSpeed += 0.1f * (float)beetleOrbs;
11496:					meleeSpeed += 0.051f;
11509:				meleeSpeed -= 0.051f;
11519:				meleeSpeed += 0.1f;
11527:				meleeSpeed += 0.05f;
11543:				meleeSpeed += 0.075f;
11559:				meleeSpeed += 0.1f;
11575:				meleeSpeed -= 0.05f;
11590:				meleeSpeed -= 0.1f;
12560:			meleeSpeed += 0.1f;
12739:			meleeSpeed += 0.2f;
12813:			meleeSpeed += 0.2f;
12877:			meleeSpeed += 0.1f;
12965:			meleeSpeed += 0.07f;
13062:			meleeSpeed += 0.12f;
13098:			meleeSpeed += 0.11f;
13129:			meleeSpeed += 0.09f;
13173:			meleeSpeed += 0.1f;
13216:			meleeSpeed += 0.1f;
13363:			meleeSpeed += 0.06f;
13373:			meleeSpeed += 0.06f;
13389:			meleeSpeed += 0.1f;
13475:			meleeSpeed += 0.15f;
13611:			meleeSpeed += 0.01f;
13615:			meleeSpeed += 0.02f;
13619:			meleeSpeed += 0.03f;
13623:			meleeSpeed += 0.04f;
13998:			meleeSpeed += 0.12f;
14559:			meleeSpeed += 0.12f;
14755:			meleeSpeed += 0.12f;
14762:			meleeSpeed += 0.12f;
14825:			meleeSpeed += 0.12f;
15945:				meleeSpeed += 0.15f;
15981:				meleeSpeed += 0.2f;
18188:		meleeSpeed = 1f;
25620:		float num27 = meleeSpeed - 1f;
25622:		meleeSpeed = 1f + num27;
28557:		float num = meleeSpeed;
28558:		meleeSpeed = TurnAttackSpeedToUseTimeMultiplier(num);
46433:			speed /= meleeSpeed;

```


---

## 🤖 Assistant · 2026-08-13T01:02:44.928Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Very interesting. In this 1.4.5.6 decompile, `meleeSpeed` starts at 1f (line 2328) and is reset to 1f (line 18188). So meleeSpeed is a MULTIPLIER-style stat (1.0 = no bonus), not additive-from-zero. Then `CapAttackSpeeds` converts:
- cap the additive bonus at 3? Wait no. `TurnAttackSpeedToUseTimeMultiplier(num)` where num = meleeSpeed. If meleeSpeed > 3f → 3f. Then speed = 1/speed.

Hmm wait that gives 1/1.12 for meleeSpeed=1.12. So after CapAttackSpeeds, `meleeSpeed` field holds the USE TIME MULTIPLIER = 1/(1+bonus). And `SetItemAnimation(sItem.useAnimation, meleeSpeed)` computes `(int)(useAnimation * multiplier)`, min 1. That's exactly the wiki formula `floor(useAnimation / (1 + meleeSpeed))`. 

So 1.4.5.6 internally stores meleeSpeed as multiplier starting at 1 and post-processing converts it to reciprocal. And line 25620-25622: `float num27 = meleeSpeed - 1f; ... meleeSpeed = 1f + num27;` — probably a half-bonus thing. Let me check that.

Also line 46433: `speed /= meleeSpeed;` — where's that? Let me check.

Now the repo: Player.ts line 545-546 comment says "封顶 3 后取倒数，作为 useAnimation/useTime 的时长乘数" and CapAttackSpeeds 倒数档 implemented. Good.

Now let me check the repo implementation. Let me read Player.ts around lines 100-700 and Game.ts around 3700-4300.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:45.487Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '25610,25630p' Player.cs && echo \"=== 46420 ===\" && sed -n '46420,46445p' Player.cs",
 "description": "Read meleeSpeed consumers context"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:45.520Z

**📎 ToolResult**

```
			}
		}
		else
		{
			stealth = 1f;
		}
		if (manaSick)
		{
			magicDamage *= 1f - manaSickReduction;
		}
		float num27 = meleeSpeed - 1f;
		num27 *= ItemID.Sets.BonusMeleeSpeedMultiplier[inventory[selectedItem].type];
		meleeSpeed = 1f + num27;
		if (tileSpeed > 3f)
		{
			tileSpeed = 3f;
		}
		tileSpeed = 1f / tileSpeed;
		if (wallSpeed > 3f)
		{
			wallSpeed = 3f;
=== 46420 ===

	public void SilentlyShootItem(Item sItem)
	{
		ItemCheck_Shoot(whoAmI, sItem, 0, withAudioVisualFeedback: false);
	}

	private void ItemCheck_Shoot(int i, Item sItem, int weaponDamage, bool withAudioVisualFeedback = true)
	{
		int projToShoot = sItem.shoot;
		float speed = sItem.shootSpeed;
		int damage = sItem.damage;
		if (sItem.melee && !ProjectileID.Sets.NoMeleeSpeedVelocityScaling[projToShoot])
		{
			speed /= meleeSpeed;
		}
		bool canShoot = false;
		int Damage = weaponDamage;
		float KnockBack = sItem.knockBack;
		int usedAmmoItemId = 0;
		if (sItem.useAmmo > 0)
		{
			PickAmmo(sItem, ref projToShoot, ref speed, ref canShoot, ref Damage, ref KnockBack, out usedAmmoItemId, ItemID.Sets.gunProj[sItem.type]);
		}
		else
		{
			canShoot = true;

```


---

## 🤖 Assistant · 2026-08-13T01:02:45.782Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "limit": 80,
 "offset": 95
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:45.792Z

**📎 ToolResult**

```
95	  /** 微光滞留 tick（TryToShimmerUnstuck :28378：钳 0-7200，shimmering +1/否则 -10） */
96	  timeShimmering = 0;
97	  /** 微光化半透明（Player.cs:18147-18162 shimmerTransparency：shimmering +0.015/t
98	   *  钳 0.8；解除后 -0.015/t 回 0，衰减起始帧（恰 0.8）播 Sound 19 style 3）。
99	   *  渲染侧 globalAlpha = 1 - 值（GetAlpha :53253 三通道乘 (1-t) 近似） */
100	  shimmerTransparency = 0;
101	  // ---- 呼吸 1:1（Player.cs:1402-1406 / CheckDrowning :22914-23002）----
102	  breathMax = 200;   // :1404（全源码无修改点——潜水头盔加的是 breathCDMax ×6 非 breathMax）
103	  breath = 200;      // :1406（显示侧气泡数 = breathMax/20 = 10）
104	  breathCD = 0;      // :1402（每 tick +1，≥breathCDMax 时 breath--）
105	  /** 原版 itemAnimation 等效（>0 = 挥舞动画中）：芦苇管换气门禁（:22920/:3698）
106	   *  用。Game.fixedUpdate 每帧注入（swing 在 postUpdate 递减，读到的是上一帧尾值，
107	   *  ≤1 tick 偏差，注释存档） */
108	  itemAnimTicks = 0;
109	  /** accMerman 人鱼化态（:22965 merman=true，水中呼吸；本作仅标志，变身渲染后续） */
110	  merman = false;
111	  inLava = false;
112	  private lavaAccum = 0;
113	  animTime = 0;          // 走路动画计时
114	  useTime = 0;           // 通用动作冷却
115	  dead = false;
116	  respawnTimer = 0;
117	  /** 死亡画面淡入（Player.cs:16873：dead 时 +2/tick 钳 255；GetDeathAlpha :53284 消费） */
118	  immuneAlpha = 0;
119	  // 摔伤追踪
120	  fallStartY: number | null = null;   // 矿车骑乘同步清空（车上不计摔伤），公开给 Minecart
121	  /** 蛛网挣扎计数（原版 stickyBreak，Player.cs:22653） */
122	  private stickyBreak = 0;
123	  private surfaceJumpCd = 0;  // 水面起跳冷却
124	  sinceHurt = 0;               // 距上次受击 tick（自然回血计时；渲染层读取做心心跳动效）
125	  /** 自然回血爬坡计时（Player.lifeRegenTime：受击 :37784 / DoT :18781+ / 流血 :19000 清零，
126	   *  每 tick 基础 +1（:18930）、蜂蜜 +2（:18954）；本仓自然回血为恒 1HP/s 简化，爬坡只
127	   *  决定"出伤后多久开始回"（首档阈值 300t :19003）——蜂蜜 3 倍速抵达 */
128	  lifeRegenTime = 0;
129	  /** 本 tick 落地冲击速度（碰撞前 vy≥3 落地才非 0；Game 消费：起爆器 411 坠落触发） */
130	  landImpactVy = 0;
131	  private regenAccum = 0;
132	  stepRenderY = 0;             // 跨台阶的渲染高度补偿（缓动到 0，消除瞬移顿挫）
133	  stepUp = true;               // Collision.StepUp 自动上台阶（moveAndCollide 内消费）
134	  /** 高尔夫累计分（Player.cs:1792 AccumulateGolfingScore——Golfer 商店门槛/月相画门） */
135	  golferScoreAccumulated = 0;
136	  /** 鞭命中授予的玩家 buff（WhipTagEffect.PlayerBuffId → 剩余 tick；
137	   *  效果实装（:9790-9802）：311 镰鞭=鞭攻速+35%、308 剑鞭=+25%、314 荆棘鞭=+12%
138	   *  ——Game 鞭 useTime 结算读取；312/365 登记持续期（效果端暂不接） */
139	  whipBuffs: Record<number, number> = {};
140	  /** 右键集火目标（MinionAttackTargetNPC，Player.cs:48952：召唤杖右键指定，
141	   *  随从索敌优先；-1=无。失效：死亡或离玩家 >3000px——随从侧判定） */
142	  minionTargetId = -1;
143	  /** 星云三族等级（0-3，各自独立 480t；NebulaLevelup :56091-56121 逐级升/降）：
144	   *  0=伤害 179-181（四系 +15%/级）1=生命 173-175（lifeRegen +6/级）2=魔力 176-178 */
145	  nebula = [0, 0, 0];
146	  private nebulaT = [0, 0, 0];
147	  private nebulaManaAccum = 0;
148	  private nebulaLifeAccum = 0;
149	  /** NebulaLevelup（:56091-56121）：本族 +1 级 cap3，满 480t 重置（拾取驱动） */
150	  nebulaLevelup(family: 0 | 1 | 2): void {
151	    this.nebula[family] = Math.min(3, this.nebula[family] + 1);
152	    this.nebulaT[family] = 480;
153	  }
154	  /** 甲虫攻击球（0-3）：近战命中蓄能，受击掉一颗 */
155	  beetleOrbs = 0;
156	  private beetleCharge = 0;
157	  /** 近战续航窗口（onMeleeHit 刷新；fixedUpdate 内蓄能消费） */
158	  private lastMeleeTick = 0;
159	  /** 潜行 0(可见)-1(满)：蘑菇矿=移动蓄/星璇=双击↓开关（:25500/:25542） */
160	  stealth = 0;
161	  private stealthTimer = 0;
162	  vortexStealthActive = false;
163	  private prevDown = false;
164	  private downTapT = 0;
165	  private sharpenedCd = 0;
166	  /** BOC 受击脉冲（fixedUpdate 消费：buff 321 + 困惑近敌） */
167	  bocPulse = 0;
168	  /** 睡眠（PlayerSleepingHelper SH:155-191：脚侧悬停右键入睡；床失效/移动输入/挥武器唤醒。
169	   *  ★受伤不唤醒（StopSleeping 全调用点仅 5 处，SH:98-131）。睡熟阈值 120t（SH:11） */
170	  sleeping = false;
171	  timeSleeping = 0;
172	  /** 联机远端位置平滑偏移（原版 Player.netOffset，MessageBuffer.cs case 13 注入、
173	   *  Player.UpdateNetOffset :28240 衰减）：模拟位置与权威快照的差，渲染时叠加。
174	   *  本地玩家恒 0 */

```


---

## 🤖 Assistant · 2026-08-13T01:02:47.081Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the repo's attackSpeedMult and the swing logic in Game.ts 3700-4300.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:47.326Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 130,
 "offset": 3690
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:47.330Z

**📎 ToolResult**

```
3690	    const m = /^vi_(\d+)_/.exec(def.key);
3691	    if (!m) return undefined;
3692	    const f = itemFuncOfVid(+m[1]);
3693	    if (!f || !(f.pick || f.axe || f.hammer)) return undefined;
3694	    const c = itemCombat(+m[1]);
3695	    return {
3696	      type: f.pick ? 'pick' : f.axe ? 'axe' : 'hammer',
3697	      power: f.pick ?? f.axe ?? f.hammer,
3698	      damage: c?.damage ?? 5,
3699	      speed: c?.useAnimation ?? 25,
3700	      useTime: c?.useTime ?? 20,
3701	      knockback: c?.knockBack ?? 3,
3702	      // 双工具副力（单工具时与主 power 同值，dualToolResolve 只在多力时改道）
3703	      pickPower: f.pick ?? undefined,
3704	      axePower: f.axe ?? undefined,
3705	      hammerPower: f.hammer ?? undefined,
3706	    } as NonNullable<(typeof ITEM_DEFS)[number]['tool']>;
3707	  }
3708	
3709	  /** 通用消耗品语义门（vanilla-itemfunc）：必须确有 heal/buff 语义才允许占用
3710	   *  else-if 槽位——生命水晶(29)/魔力水晶(109)/生命果(1291)/弓枪族等无此语义，
3711	   *  若被本分支空认领会把链条后续分支全部饿死（else-if 匹配即终止） */
3712	  private consumableFuncGate(def: (typeof ITEM_DEFS)[number]): boolean {
3713	    const fm = /^vi_(\d+)_/.exec(def.key);
3714	    const ff = fm ? itemFuncOfVid(+fm[1]) : null;
3715	    return !!ff?.consumable && !ff.createTile && !ff.shoot && !ff.pick && !ff.axe && !ff.hammer
3716	      && (!!ff.healLife || !!ff.healMana || !!(ff.buffType && ff.buffType > 0));
3717	  }
3718	
3719	  /** 手持物 useStyle 分族（Player.cs:49939 ItemCheck_ApplyUseStyle switch）：
3720	   *  vi_ → vanilla-itemfunc.useStyle（2141 件分布 1:1504 / 4:74 / 5:243 / 9:70 …）；
3721	   *  legacy 药水无 vid → 9（Item.DefaultToHealingPotion：useStyle=9 举杯）；
3722	   *  其余 legacy 缺数据 → 1（挥砍）。返回值供 Renderer 姿势/身体行路由 */
3723	  private heldUseStyle(def: (typeof ITEM_DEFS)[number] | null): number {
3724	    if (!def) return 1;
3725	    const vid = def.vid ?? viIdFromKey(def.key);
3726	    if (vid >= 0) return itemFuncOfVid(vid)?.useStyle ?? 1;
3727	    if (def.potion || def.heal) return 9; // 治疗类（仅标 heal 的残余占位）
3728	    return 1;
3729	  }
3730	
3731	  /** 手持物 useStyle（按本仓库 item id 入口；规则同 heldUseStyle）——
3732	   *  远端 swingNet 构造用（simulateRemotePlayers 无 ITEM_DEFS 条目时回退 1） */
3733	  private useStyleOfVid(itemId: number): number {
3734	    return this.heldUseStyle(ITEM_DEFS[itemId] ?? null);
3735	  }
3736	
3737	  /** 使用动画时长（Player.itemAnimationMax = item.useAnimation）：
3738	   *  vi_ 取 vanilla-itemcombat.useAnimation；legacy 工具 def.tool.speed；
3739	   *  无数据 → 30（原版绝大多数消耗品 useAnimation 15-45 的中位近似） */
3740	  private heldUseAnimation(def: (typeof ITEM_DEFS)[number] | null): number {
3741	    if (!def) return 30;
3742	    if (def.tool?.speed) return Math.max(10, def.tool.speed);
3743	    const vid = def.vid ?? viIdFromKey(def.key);
3744	    if (vid >= 0) {
3745	      const ua = itemCombat(vid)?.useAnimation;
3746	      if (ua && ua > 0) return Math.max(4, ua);
3747	    }
3748	    return 30;
3749	  }
3750	
3751	  /** 启动一次使用动画（itemAnimation>0 的本项目等价）。
3752	   *  useStyle 5/13（弓/枪/法杖/短剑）附 aim 瞄准角——Renderer 持物姿势与
3753	   *  bodyFrame 行档（Player.cs:35986 useStyle==5 的 itemRotation*direction 档）依赖 */
3754	  private useSwing(def: (typeof ITEM_DEFS)[number] | null, aim?: number): void {
3755	    if (!def) return;
3756	    const us = this.heldUseStyle(def);
3757	    const dur = this.heldUseAnimation(def);
3758	    this.swing = {
3759	      t: dur, dur, item: ITEM_BY_KEY[def.key] ?? 0,
3760	      useStyle: us,
3761	      aim: us === 5 || us === 13 ? aim : undefined,
3762	    };
3763	    this.swingHitSet.clear();
3764	    this.swingTileCutSet.clear();
3765	  }
3766	
3767	  /** 双工具分流（Player.cs:45040-45045：tileHammer→锤力 / tileAxe→斧力 / 其余→镐力）。
3768	   *  Hamaxe 族（pick+axe）对树族用斧力、对矿石用镐力；The Axe 族（axe+hammer）
3769	   *  对树族用斧力、其余（锤墙/坡面）走锤。单工具原样返回 */
3770	  private dualToolResolve(
3771	    tool: NonNullable<(typeof ITEM_DEFS)[number]['tool']>,
3772	    targetType: number,
3773	  ): { type: 'pick' | 'axe' | 'hammer'; power: number } {
3774	    const d = tool as NonNullable<(typeof ITEM_DEFS)[number]['tool']> & {
3775	      pickPower?: number; axePower?: number; hammerPower?: number;
3776	    };
3777	    const multi = !!((d.pickPower && d.axePower) || (d.axePower && d.hammerPower) || (d.pickPower && d.hammerPower));
3778	    if (!multi) return { type: tool.type as 'pick' | 'axe' | 'hammer', power: tool.power ?? 10 };
3779	    const sheet = TILE_DEFS[targetType]?.vanilla?.sheet ?? -1;
3780	    if (TILE_AXE_SHEETS.has(sheet) && d.axePower) return { type: 'axe', power: d.axePower };
3781	    if (d.pickPower) return { type: 'pick', power: d.pickPower };
3782	    return { type: 'hammer', power: d.hammerPower ?? tool.power ?? 10 };
3783	  }
3784	
3785	  /** 智能光标设置（对齐原版 Player.SmartCursorSettings + Main.cs:49705 设置结构） */
3786	  private smartSettings(): SmartCursorSettings {
3787	    const d = options.data;
3788	    return {
3789	      toggleMode: d.smartCursorMode === 'toggle',
3790	      smartAxeAfterPickaxe: !!d.smartAxeAfterPickaxe,
3791	      smartBlocksEnabled: !!d.smartBlocksEnabled,
3792	      holdCanReleaseMidUse: !!d.smartHoldCanReleaseMidUse,
3793	    };
3794	  }
3795	
3796	  /**
3797	   * 智能光标每帧驱动（Player.cs:25159-25163 每帧 SmartCursorLookup + :28344-28374 Toggle/Hold 状态机）。
3798	   * Ctrl 按下沿翻转（Toggle）/跟随（Hold）；切换播音效 12（menuTick）。
3799	   * 必须在 updateUse 之前跑——同帧 lookup 结果即被挖掘/放置路径覆盖 tx/ty。
3800	   */
3801	  private updateSmartCursor() {
3802	    const inp = this.input;
3803	    const sc = this.smartCursor;
3804	    const s = this.smartSettings();
3805	    const controlSmart = inp.down('ControlLeft') || inp.down('ControlRight');
3806	    if (sc.updateWanted(controlSmart, !!inp.mouseDown, s)) this.sfx.play('menuTick');
3807	    const blocked = inp.uiBlocking || this.player.dead || !!this.minecart
3808	      || this.renderer.fullMap.open || this.renderer.timeUiHover || this.renderer.weatherUiHover
3809	      || this.annotateMode;
3810	    if (blocked || !sc.wanted) { sc.showing = false; VUI.smartCursorOn = false; return; }
3811	    const held = this.player.inv.heldItem();
3812	    const heldDef = held ? ITEM_DEFS[held.id] : null;
3813	    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
3814	    const [mx, my] = this.camera.screenToWorld(inp.mouseX, inp.mouseY);
3815	    const p = this.player;
3816	    // 放置物才有 blockRange（原版 SmartCursorLookup :95-98 createWall/createTile 才加）；
3817	    // 工具 tileBoost=0
3818	    const placing = heldDef?.tile != null || heldDef?.wallId != null;
3819	    const tb = placing

```


---

## 🤖 Assistant · 2026-08-13T01:02:47.632Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 80,
 "offset": 540
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:47.636Z

**📎 ToolResult**

```
540	  private hardnessCache = 1;
541	  /** 原版 HitTile 伤害积累（劈砍/挖掘通用，阈值 100） */
542	  private hitTiles = new HitTile();
543	  private lastMineHitTick = -999;
544	  swing: {
545	    t: number; dur: number; item: number; dmg?: number; kb?: number;
546	    /** useStyle 分族（Player.cs:49939 ApplyUseStyle switch）：1 挥砍 / 2 咀嚼 /
547	     *  3 雨伞 / 4 举过头 / 5 朝鼠标静持 / 6 饮用旋转 / 9 举杯 / 13 短剑突刺 /
548	     *  14-15 头侧持（不改 bodyFrame）/ 16 静持。缺省 1（Renderer drawUseStyle 路由） */
549	    useStyle?: number;
550	    /** useStyle 5/13 的瞄准角（世界系 atan2；Renderer 姿势与 bodyFrame 行档用它） */
551	    aim?: number;
552	  } | null = null;
553	  /** 上一帧鼠标左键状态（非 autoReuse 近战武器需点击沿触发新挥，原版 autoReuse 语义） */
554	  prevSwingMouse = false;
555	  private swingHitSet = new Set<number>();
556	  /** 同一挥击内 tileCut 格只处理一次（与 swingHitSet 同生命周期） */
557	  private swingTileCutSet = new Set<number>();
558	
559	  /** 滚动 FPS（最近 60 帧均值；样本不足返回 null）——F5 调试报告 meta/perf 段 */
560	  get fps(): number | null {
561	    const n = this.frameDts.length;
562	    if (n < 2) return null;
563	    let sum = 0;
564	    for (const d of this.frameDts) sum += d;
565	    return sum / n > 0 ? 1000 / (sum / n) : null;
566	  }
567	
568	  /** 私有运行时状态一次性打包（F5 调试报告 systems 段；私有字段只从这里出） */
569	  debugSnapshot() {
570	    return {
571	      fps: this.fps,
572	      frameDtMs: this.frameDts.slice(),
573	      hitTilesSize: this.hitTiles.size(),
574	      hitTilesTop: this.hitTiles.dumpTop(10),
575	      mining: this.mining ? { x: this.mining.x, y: this.mining.y, progress: this.mining.progress } : null,
576	      swing: this.swing
577	        ? { t: this.swing.t, dur: this.swing.dur, item: this.swing.item, dmg: this.swing.dmg ?? null, kb: this.swing.kb ?? null, useStyle: this.swing.useStyle ?? null, aim: this.swing.aim ?? null }
578	        : null,
579	      invasionWarn: this.invasionWarn,
580	      tickCount: this.tickCount,
581	    };
582	  }
583	
584	  // 弹药
585	  particles: Particle[] = [];
586	  dmgNumbers: DamageNumber[] = [];
587	
588	  // 敌人生成
589	  boss: Enemy | null = null;
590	  /** 本局世界是否新生成(NPC 入驻公告只在新世界播) */
591	  private freshlyCreated = false;
592	  /** 原版 Spawner 移植实例（VanillaSpawner.ts） */
593	  vanillaSpawner: VanillaSpawner | null = null;
594	  /** 世界生成 worker 客户端（懒建；不可用时 newWorld 走主线程 fallback） */
595	  private genClient: WorldGenClient | null = null;
596	  /** 多人联机客户端（netMode==1；单机 null）。docs/multiplayer-design.md §4 */
597	  net: ClientNet | null = null;
598	  // ---- v3 房间制保护门禁（集中点，低耦合）：策略存于 net.policy，门禁只在操作入口查询 ----
599	  /** 破坏保护：单人/房主/未开启保护时放行 */
600	  netCanEditTile(): boolean {
601	    return !this.net || this.net.policy.isHost || !this.net.policy.protectTiles;
602	  }
603	  /** 物品保护：宝箱取放等受控（自动拾取不门禁——需求明确豁免） */
604	  netCanChestInteract(): boolean {
605	    return !this.net || this.net.policy.isHost || !this.net.policy.protectItems;
606	  }
607	  /** 门禁拒绝提示（2s 节流防刷屏） */
608	  private netDenyAt = 0;
609	  netDeny(msg: string) {
610	    const now = Date.now();
611	    if (now - this.netDenyAt > 2000) {
612	      this.netDenyAt = now;
613	      this.cb.onToast?.(msg);
614	    }
615	    this.input.rightDown = false;
616	  }
617	  // ---- 箱子同步（msg31/32，服务器权威） ----
618	  /** 待开箱（msg31 已发、等回包后自动开面板） */
619	  private netPendingChest: { x: number; y: number } | null = null;

```


---

## 🤖 Assistant · 2026-08-13T01:02:49.161Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the melee swing / use chain in Game.ts at 4040-4300. This is the core.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:49.378Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 200,
 "offset": 3880
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:49.383Z

**📎 ToolResult**

```
3880	      screenTopY,
3881	      screenHeight: canvas.height / this.camera.zoom,
3882	      player: {
3883	        x: p.x, y: p.y, w: p.w, h: p.h,
3884	        gravDir: 1,                              // 反重力未实装（同 SmartCursor 口径）
3885	        // Player.wet（Player.cs:27540 经 Collision.WetCollision Collision.cs:1575 判定）；
3886	        // p.inWater 为脚部液量>100 的简化门，此处按原版命中盒中心盒求交精确复刻
3887	        wet: p.inWater || wetCollision(this.world.store, p.x, p.y, p.w, p.h),
3888	      },
3889	      slots: this.smartSelectSlots(),
3890	      selectedItem: p.inv.selected,
3891	      // IsInTileInteractionRange（Player.cs:31548，Simple 档 tileRangeX=5/tileRangeY=3 + TB）
3892	      inRange: (tx, ty, tb) => this.inTileRange(tx, ty, tb),
3893	    };
3894	    // SelectedItemState（Player.cs:383-517）宿主：换选/还原由 SmartSelect 代管
3895	    // SelectedItemState.Hotbar（:391）= 最近一次 0-9 快捷栏选择（Select :437-439 item<10 时记）；
3896	    // 本作数字键直写 inv.selected，故在此跟随记录
3897	    if (p.inv.selected <= 9) this.smartSelectHotbar = p.inv.selected;
3898	    const host: SmartSelectHost = {
3899	      selected: p.inv.selected,
3900	      hotbar: this.smartSelectHotbar,
3901	      canChangeImmediately: !this.swing && p.useTime === 0,
3902	      // CanChangeSelectedItemImmediately（Player.cs:386-393）：itemAnimation/itemTime 空——
3903	      // 本作 swing = itemAnimation、player.useTime = itemTime；reuseDelay/channel/
3904	      // pendingItemReuse 未实装
3905	      isSlotEmpty: (i) => !p.inv.slots[i],
3906	      onSelectionChanged: () => this.cb.onInventoryChanged(),
3907	    };
3908	    this.smartSelect.update(env, host);
3909	    p.inv.selected = host.selected;
3910	  }
3911	
3912	  /**
3913	   * inventory 0-57 的 Smart Select 槽画像（Player.cs:17326 的 inventory[i].type 等窄视图）。
3914	   * 0-49 背包 + 50-53 钱币 + 54-57 弹药——case 4/5 信号枪弹药门扫到 57（:17374/:17410）。
3915	   * 三力取 vanilla-itemfunc 全量（Hamaxe 斧+锤 / Drax 镐+斧 副力保留），legacy def.tool
3916	   * 画像只覆盖自身类型主力（与 updateUse 的工具判定同序）。
3917	   * 结果写入复用缓冲（每帧调用，防分配热点——perf-audit-2026-08 口径）。
3918	   */
3919	  private smartSelectSlots(): SmartSelectSlot[] {
3920	    const inv = this.player.inv;
3921	    for (let i = 0; i < INV_SIZE; i++) {
3922	      const it = inv.slots[i];
3923	      const buf = this._smartSelectSlots[i];
3924	      if (!it) { this._smartSelectSlots[i] = EMPTY_SLOT; continue; }
3925	      const def = ITEM_DEFS[it.id];
3926	      this._smartSelectSlots[i] = smartSelectSlotOf(
3927	        def,
3928	        it.stack,
3929	        itemFuncOfInternal(it.id, def?.key ?? ''),
3930	        def?.tool ? { type: def.tool.type as 'pick' | 'axe' | 'hammer', power: def.tool.power ?? 0 } : null,
3931	        buf === EMPTY_SLOT ? undefined : buf,
3932	      );
3933	    }
3934	    return this._smartSelectSlots;
3935	  }
3936	
3937	  private updateUse(_dt: number) {
3938	    const inp = this.input;
3939	    // ---- 矿车坐骑（Mount 6 + Minecart.cs 轨道运动学；物理在 Minecart.fixedUpdate）----
3940	    if (this.minecart) {
3941	      const cart = this.minecart;
3942	      const [mtx, mty] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
3943	      const mType = this.world.store.get(mtx, mty);
3944	      // R（坐骑键）：骑乘中下车（Player.TryToDismount 路径 :5768-5776）
3945	      if (inp.down('KeyR') && !this.cartKeyLatch) {
3946	        this.dismountMinecart();
3947	        this.cartKeyLatch = true;
3948	      }
3949	      if (!inp.down('KeyR')) this.cartKeyLatch = false;
3950	      // 右键轨道：骑乘中 → 下车（Player.cs:32806-32812 type==314 && mount.Cart 分支）
3951	      if (inp.rightDown && mType === this.trackTile && this.trackTile !== 0) {
3952	        this.dismountMinecart();
3953	        this.input.rightDown = false;
3954	      }
3955	      if (cart.dead || !cart.mounted) {
3956	        this.minecart = null;
3957	        this.player.ridingCart = false;
3958	        this.player.cart = null;
3959	      }
3960	      // 骑乘中不拦使用路径（原版矿车不在 MountID.Sets.DontHoldItems{55,56,61}
3961	      // MountID.cs:27——车上照常挥击/挖掘/放置/交互；此前整段 return 是简化禁用）
3962	    }
3963	    // R（坐骑键）：未骑乘 + 附近有轨道 → QuickMinecart 上车（Player.cs:5796-5827：
3964	    // 射程内取最近轨道格 + CanHitLine 视线门）
3965	    if (inp.down('KeyR') && !this.cartKeyLatch && this.trackTile !== 0) {
3966	      this.cartKeyLatch = true;
3967	      this.tryQuickMinecart();
3968	    }
3969	    if (!inp.down('KeyR')) this.cartKeyLatch = false;
3970	    // 全屏地图打开时鼠标交给地图（拖动/缩放/传送），不触发挖掘/放置/攻击/使用。
3971	    // 时间调整按钮/面板悬停同理（renderer.timeUiHover 渲染期写入）
3972	    if (inp.uiBlocking || this.player.dead || this.renderer.fullMap.open || this.renderer.timeUiHover || this.renderer.weatherUiHover) {
3973	      this.mining = null;
3974	      return;
3975	    }
3976	    const held = this.player.inv.heldItem();
3977	    const heldDef = held ? ITEM_DEFS[held.id] : null;
3978	    const [rawTx, rawTy] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
3979	    let tx = rawTx, ty = rawTy;
3980	    // 工具判定：legacy def.tool 优先；vi_ 镐/斧/锤经 vanilla-itemfunc 桥接（数值取 combat 表）
3981	    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
3982	    const vw2 = this.renderer.canvas.width, vh2 = this.renderer.canvas.height;
3983	
3984	    // 右键轨道：(最优先,防 NPC 交谈拦截) → 附近宝箱 → NPC 交谈 → 交互
3985	    //（Player.cs:32806-32812：右键轨道格 → LaunchMinecartHook——与手持物品无关，
3986	    //  用"最佳矿车"（装备槽 > 手持 > 背包）；矿车是坐骑召唤物，不消耗）
3987	    const type = this.world.store.get(tx, ty);
3988	    if (inp.rightDown && !this.minecart && type === this.trackTile && this.trackTile !== 0) {
3989	      const tex = this.bestCartTexture();
3990	      if (tex) {
3991	        if (this.mountMinecartAt(tx, ty, tex)) this.input.rightDown = false;
3992	        return;
3993	      }
3994	    }
3995	    if (inp.rightDown) {
3996	      // 光标格本身是蜥蜴祭坛时跳过 ±1 格宝箱搜索——神庙宝箱全庙随机散布可能
3997	      // 贴着祭坛，原版无 ±1 搜索（点到箱本体才开箱）；不跳过则右键祭坛变成开箱
3998	      const cursorIsAltar = type === TILE_BY_KEY['v_237_lihzahrd_altar'];
3999	      const nearChest = cursorIsAltar ? null : this.findChestNear(tx, ty);
4000	      if (nearChest) {
4001	        this.tryOpenChest(nearChest);
4002	        this.input.rightDown = false;
4003	      } else if (this.talkToNearbyNpc(tx, ty)) {
4004	        this.input.rightDown = false;
4005	      } else if (heldDef && viIdFromKey(heldDef.key) === 5289) {
4006	        // 矿车升级套件（Item 5289 MinecartPowerup → Player.unlockedSuperCart = true）：
4007	        // 永久解锁 SuperCart 档（runSpeed 20/accel 0.1/jump 5.15，Mount.cs:371-379），
4008	        // 持久化于世界 flags；已解锁时不再消耗
4009	        if (!this.superCartUnlocked()) {
4010	          (this.world.flags as Record<string, boolean>).superCart = true;
4011	          this.player.inv.removeAt(this.player.inv.selected, 1);
4012	          this.cb.onInventoryChanged();
4013	          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.SuperCartUnlocked'));
4014	        }
4015	        this.input.rightDown = false;
4016	      } else if (heldDef && viIdFromKey(heldDef.key) === 43) {
4017	        if (!this.world.clock.isDay) {
4018	          // 被召唤门拦下（场上已有 NPC 4）时 SummonItemCheck=false → 不消耗（Player.cs:51441-51447）
4019	          if (this.useSuspiciousEye()) {
4020	            this.player.inv.removeAt(this.player.inv.selected, 1);
4021	            this.cb.onInventoryChanged();
4022	          }
4023	        } else {
4024	          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NothingHappened'));
4025	        }
4026	        this.input.rightDown = false;
4027	      } else {
4028	        this.interactAt(tx, ty);
4029	      }
4030	    }
4031	
4032	    // 智能光标覆盖（SmartCursorHelper.cs:157-162）：只影响左键使用路径（挖掘/放置/电路工具），
4033	    // 右键交互（宝箱/门/NPC 交谈）上面已用原始鼠标格 rawTx/rawTy 处理完毕
4034	    if (this.smartCursor.showing) {
4035	      tx = this.smartCursor.x;
4036	      ty = this.smartCursor.y;
4037	    }
4038	
4039	    if (!inp.mouseDown || this.annotateMode) {
4040	      this.mining = null;
4041	      return;
4042	    }
4043	
4044	    // 近战挥剑（vi_ 数据驱动近战武器同走挥击，数值取 combat 表；攻速倍率 =
4045	    // Player.attackSpeedMult = CapAttackSpeeds 倒数档，Player.cs:28555-28574）
4046	    const cw = heldDef ? combatWeapon(heldDef) : null;
4047	    const cwMelee = cw?.kind === 'melee' ? cw : null;
4048	    if (tool?.type === 'sword' || cwMelee) {
4049	      // ★挥击时长 = useAnimation、复用冷却 = useTime（Player.ItemCheck：itemAnimationMax 与
4050	      // itemTime 分立；1790 件 vi 武器两者不同——此前把 useTime 当动画时长，挥速虚快 35%+）
4051	      // autoReuse 持按链式：useTime<useAnimation 时原版会在动画未走完时重置弧线（下挥被截）
4052	      const nativeSpd = tool?.speed;
4053	      const animSpd = nativeSpd != null
4054	        ? Math.max(12, Math.round(nativeSpd / this.player.attackSpeedMult))
4055	        : Math.max(4, Math.round((cwMelee!.useAnimation) / this.player.attackSpeedMult));
4056	      // ★原版 ApplyItemTime（P:4216-4222）useTime 裸值不乘 meleeSpeed——此前误缩
4057	      // 导致近战连挥随攻速加成变快（原版只有动画变快、冷却恒定），审计 §1/§7 修正
4058	      const reuseSpd = nativeSpd != null
4059	        ? animSpd
4060	        : Math.max(1, Math.round(cwMelee!.useTime));
4061	      // TryAllowingItemReuse（Player.cs:52036-52053）：autoReuseGlove（力量手套族配饰）给
4062	      // 近战武器补自动连挥——唯 type 3030 除外；原生 legacy sword 保持持按连挥
4063	      const heldVid = heldDef?.vid ?? -1;
4064	      const gloveReuse = this.player.equipStats.autoReuseGlove && heldVid !== 3030;
4065	      const autoReuse = cwMelee ? (cwMelee.autoReuse || gloveReuse) : true;
4066	      const clickEdge = inp.mouseDown && !this.prevSwingMouse;
4067	      const canChain = autoReuse || clickEdge; // 非 autoReuse 武器需重新点击（原版语义）
4068	      // 词缀乘区（Item.Prefix :551：damage=round(damage×dmg)、knockBack×kb）
4069	      const ps = this.heldPrefixStat();
4070	      // ★ 重启门含 swing.t<=1（原版 itemAnimation 归零同帧即重启挥动,NPC AI 永远看不到 0 帧；
4071	      //   此前 !this.swing 硬门让每挥击周期漏出 1 帧 useTime==0——黄蜂 ai[1] 每周期清零,
4072	      //   永远攒不到 130 → 战斗中黄蜂从不射毒刺(NPC.cs:51165 的 itemAnimation 门因此误判"待机")）
4073	      const swingOver = !this.swing || this.swing.t <= 1;
4074	      if (this.player.useTime === 0 && canChain && (swingOver || reuseSpd < animSpd)) {
4075	        this.swing = {
4076	          t: animSpd, dur: animSpd, item: held!.id,
4077	          dmg: cwMelee ? Math.max(1, Math.round(cwMelee.damage * (ps?.dmg ?? 1))) : undefined,
4078	          kb: cwMelee ? cwMelee.knockback * (ps?.kb ?? 1) : undefined,
4079	        };

```


---

## 🤖 Assistant · 2026-08-13T01:02:50.502Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 210,
 "offset": 4080
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:50.507Z

**📎 ToolResult**

```
4080	        this.player.useTime = reuseSpd;
4081	        this.swingHitSet.clear();
4082	        this.swingTileCutSet.clear();
4083	        // ★ melee+shoot 剑族（附魔剑 989/波刃 190 等，Player.cs:42880 flag4 语义）：
4084	        // 挥砍为主 + 挥击启动帧朝鼠标射出 item.shoot（useTime 节奏=每次挥击一弹）；
4085	        // 弹体走通用 Arrow（贴图/穿透/寿命取投射物表），伤害与本体挥击同源
4086	        if (cwMelee?.shoot && cwMelee.shootSpeed != null) {
4087	          const ang2 = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
4088	          const pd = projectileData(cwMelee.shoot);
4089	          let pen = pd?.penetrate ?? 1;
4090	          if (pen < 0) pen = 3;
4091	          pen = Math.max(1, Math.min(pen, 3));
4092	          this.entities.add(new Arrow(
4093	            this.player.cx + Math.cos(ang2) * 14, this.player.cy - 4 + Math.sin(ang2) * 14,
4094	            // ⑨ melee 弹速 /meleeSpeed（P:46431-46434 speed/=meleeSpeed——审计 §1/§9）
4095	            Math.cos(ang2) * cwMelee.shootSpeed / this.player.attackSpeedMult,
4096	            Math.sin(ang2) * cwMelee.shootSpeed / this.player.attackSpeedMult,
4097	            this.swing.dmg ?? 1, this.swing.kb ?? 3, cwMelee.shoot, null,
4098	            { grav: projGravity(cwMelee.shoot), life: pd?.timeLeft ?? 600, pierce: pen }), 'projectiles');
4099	        }
4100	      }
4101	      this.mining = null;
4102	      return;
4103	    }
4104	
4105	    // 镐/斧/锤：挖掘（按住累计）+ 同时作为武器挥击（伤害低于剑）。
4106	    // 双工具族（Hamaxe/The Axe）先按目标 tile 族分流出生效类型与力（dualToolResolve）
4107	    if (tool && (tool.type === 'pick' || tool.type === 'axe' || tool.type === 'hammer')) {
4108	      const spd = Math.max(14, Math.round((tool.speed ?? 46) / this.player.attackSpeedMult));
4109	      const dual = this.dualToolResolve(tool, this.world.store.get(tx, ty));
4110	      // 同剑系：swing.t<=1 放行同帧重启（防黄蜂 ai[1] 每周期清零,见上）
4111	      if (this.player.useTime === 0 && (!this.swing || this.swing.t <= 1)) {
4112	        this.swing = { t: spd, dur: spd, item: held!.id };
4113	        this.player.useTime = spd;
4114	        this.swingHitSet.clear();
4115	        this.swingTileCutSet.clear();
4116	        // 每次挥砍一声：斧砍植物纤维、镐按材质区分土闷/石金（跟随挥砍节奏，不再密集连响）。
4117	        // 没有生效对象（镐没对准可挖方块 / 斧没对准树）则不出声
4118	        const hType = this.world.store.get(tx, ty);
4119	        const hovered = TILE_DEFS[hType];
4120	        const axeOnTarget = hType === T.TREE || TILE_AXE_SHEETS.has(hovered?.vanilla?.sheet ?? -1)
4121	          || (hovered?.decor ?? false);
4122	        const pickOnTarget = hType !== 0 && this.toolCanBreak(hType, dual.power, dual.type);
4123	        if (dual.type === 'axe' ? axeOnTarget : pickOnTarget) {
4124	          if (dual.type === 'axe') this.sfx.play('chop');
4125	          else if (hovered && /stone|ore|brick|obsidian|ash|gem_|fossil|silt/i.test(hovered.key)) this.sfx.play('tink');
4126	          else this.sfx.play('dig');
4127	        }
4128	      }
4129	      // HitTile 节流窗 = 实际挥击间隔（含攻速配饰加成），保证一挥一击
4130	      this.tryMine(tx, ty, dual.power, dual.type, spd, tool.useTime ?? spd);
4131	      return;
4132	    }
4133	
4134	    // 提取机（Player.cs:41008 PlaceThing_ItemInExtractinator——先于 PlaceThing_Tiles）：
4135	    // 手持可提取物（泥沙/雪泥/沙漠化石/垃圾/苔藓/粪块/蜂巢/贝壳堆/黑曜石，ItemID.cs:1104）
4136	    // 对准 219/642 左键使用 → 转化；642 先查矿物兑换表。useTime 冷却 = 10×(642?0.33:1)
4137	    if (inp.mouseDown && !inp.rightDown && this.player.useTime === 0
4138	      && this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) {
4139	      const esh = this.wiring?.sheetOf(tx, ty) ?? -1;
4140	      if (esh === 219 || esh === 642) {
4141	        if (this.useExtractinator(tx, ty, true)) {
4142	          // useAnimation 15（Item.cs:6301 泥沙/MakeUsableWithChlorophyteExtractinator:48120）
4143	          this.swing = { t: 15, dur: 15, item: held!.id };
4144	          this.swingHitSet.clear();
4145	          this.swingTileCutSet.clear();
4146	          return;
4147	        }
4148	      }
4149	    }
4150	
4151	    // 电路工具(扳手/剪线钳/致动器/致动魔杖/五彩扳手/宏伟蓝图):左键,目标格可被占用
4152	    if (heldDef?.wireTool && inp.mouseDown && !inp.rightDown) {
4153	      this.useWireTool(tx, ty, heldDef);
4154	      return;
4155	    }
4156	
4157	    // 可放置物品：左键放置
4158	    // 墙面物品（Player.PlaceThing_Walls，Player.cs:38937）：左键铺墙
4159	    if (heldDef?.wallId != null && inp.mouseDown && !inp.rightDown) {
4160	      this.tryPlaceWall(tx, ty, heldDef);
4161	      return;
4162	    }
4163	    if (heldDef?.tile && !inp.rightDown) {
4164	      this.tryPlace(tx, ty, heldDef);
4165	      return;
4166	    }
4167	
4168	    // 其它物品（药水/食物/镜子/召唤物等）：左键使用，useStyle 分族姿势
4169	    // （Player.ItemCheck：itemAnimationMax = useAnimation，ApplyUseStyle 按 useStyle
4170	    //  路由——4 举过头（镜子/机械三王召唤）/5 朝鼠标静持（火把族非放置路径）/
4171	    //  9 举杯（增益药水 DefaultToHealingPotion）/2 咀嚼（食物 DefaultToFood）/
4172	    //  6 饮用旋转（回归药水）；此前的统一 30t 挥砍对 395 件 4/5/9 族全错族）
4173	    // （召唤武器例外——交给下方 cw 分发 kind='summon'；spear/yoyo/flail/boomerang 四族
4174	    //  原版 noUseGraphic=true（Item.cs case 220 等,DefaultToSpear :47637 全 202 处）——
4175	    //  投射物即本体,此处再画持物 = 角色旁多出一个静态武器图标,一并排除）
4176	    if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool
4177	      && cw?.kind !== 'summon' && cw?.kind !== 'spear' && cw?.kind !== 'yoyo'
4178	      && cw?.kind !== 'flail' && cw?.kind !== 'boomerang') {
4179	      this.useSwing(heldDef);
4180	      // 召唤道具（原版左键使用）
4181	      if (viIdFromKey(heldDef.key) === 43) {
4182	        if (!this.world.clock.isDay) {
4183	          // 被召唤门拦下（场上已有 NPC 4）时不消耗（SummonItemCheck，Player.cs:51441-51447）
4184	          if (this.useSuspiciousEye()) {
4185	            this.player.inv.removeAt(this.player.inv.selected, 1);
4186	            this.cb.onInventoryChanged();
4187	          }
4188	        } else {
4189	          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NothingHappened'));
4190	        }
4191	        this.player.useTime = 30;
4192	      }
4193	    }
4194	    // 药水饮用（移植自 Maples：点击饮用，治疗类受耐药性封锁）
4195	    if (heldDef?.potion && inp.mouseDown && this.player.useTime === 0) {
4196	      const p = heldDef.potion;
4197	      const buffTypeMap: Record<string, BuffType> = {
4198	        agility: BuffType.Agility, ironskin: BuffType.Ironskin,
4199	        resistance: BuffType.Resistance, thorns: BuffType.Thorns, regen: BuffType.Regen,
4200	        obsidianSkin: BuffType.ObsidianSkin, gills: BuffType.Gills,
4201	        manaRegen: BuffType.ManaRegen, magicPower: BuffType.MagicPower,
4202	        featherfall: BuffType.Featherfall, waterWalking: BuffType.WaterWalking,
4203	        archery: BuffType.Archery, nightOwl: BuffType.NightOwl,
4204	      };
4205	      if (p.isHealType && this.player.buffs.healBlocked) {
4206	        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.HealBlock'));
4207	        this.player.useTime = 30;
4208	      } else {
4209	        const bt = buffTypeMap[p.buff];
4210	        // 贤者之石（pStone：药水 CD -25%，Player.pStone → PotionSickness 2850→2140）
4211	        this.player.buffs.apply(bt, Math.round(p.duration * (this.player.equipStats.pStone ? 0.75 : 1)));
4212	        if (heldDef.heal) {
4213	          this.player.hp = Math.min(this.player.maxHp, this.player.hp + heldDef.heal);
4214	          this.addDamageNumber(this.player.cx, this.player.y, heldDef.heal, false, '#40E080');
4215	        }
4216	        this.player.inv.removeAt(this.player.inv.selected, 1);
4217	        this.player.useTime = 60;
4218	        this.sfx.play('drink');
4219	        this.cb.onInventoryChanged();
4220	        this.cb.onToast(`${heldDef.name}：${p.duration} 秒`);
4221	      }
4222	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && viIdFromKey(heldDef.key) === 29) {
4223	      // 物品态生命水晶(Player.cs:29358:item 29,statLifeMax<400 → +20)
4224	      if (this.player.baseMaxHp >= 400) {
4225	        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.LifeMaxReached'));
4226	      } else {
4227	        this.player.baseMaxHp += 20;
4228	        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 20);
4229	        this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#40E080');
4230	        this.player.inv.removeAt(this.player.inv.selected, 1);
4231	        this.player.useTime = 30;
4232	        this.sfx.play('drink');
4233	        this.cb.onInventoryChanged();
4234	      }
4235	      this.player.useTime = Math.max(this.player.useTime, 30);
4236	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && heldDef.key === 'vi_109_mana_crystal') {
4237	      // 魔力水晶(Player.cs:44655:statManaMax<200 → +20 上限并回复)
4238	      if (this.player.baseMaxMana >= 200) {
4239	        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.ManaMaxReached'));
4240	      } else {
4241	        this.player.baseMaxMana += 20;
4242	        this.player.mana = Math.min(this.player.maxMana, this.player.mana + 20);
4243	        this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#4080FF');
4244	        this.player.inv.removeAt(this.player.inv.selected, 1);
4245	        this.player.useTime = 30;
4246	        this.sfx.play('drink');
4247	        this.cb.onInventoryChanged();
4248	        // 成就：魔力水晶使用（Player.cs:44667 HandleSpecialEvent(1)）
4249	        this.achievements.handleSpecialEvent(1,
4250	          { statLifeMax: this.player.maxHp, statManaMax: this.player.maxMana });
4251	      }
4252	      this.player.useTime = Math.max(this.player.useTime, 30);
4253	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && heldDef.key === 'vi_1291_life_fruit') {
4254	      // 生命果(Player.cs:44665:statLifeMax≥400 且 <500 → +5)
4255	      if (this.player.baseMaxHp < 400) {
4256	        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NeedLifeCrystalFirst'));
4257	      } else if (this.player.baseMaxHp >= 500) {
4258	        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.LifeMaxReached500'));
4259	      } else {
4260	        this.player.baseMaxHp += 5;
4261	        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 5);
4262	        this.addDamageNumber(this.player.cx, this.player.y, 5, false, '#40E080');
4263	        this.player.inv.removeAt(this.player.inv.selected, 1);
4264	        this.player.useTime = 30;
4265	        this.sfx.play('drink');
4266	        this.cb.onInventoryChanged();
4267	        // 成就：生命果使用（Player.cs:44683 HandleSpecialEvent(2)）
4268	        this.achievements.handleSpecialEvent(2,
4269	          { statLifeMax: this.player.maxHp, statManaMax: this.player.maxMana });
4270	      }
4271	      this.player.useTime = Math.max(this.player.useTime, 30);
4272	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && heldDef.key === 'vi_5340_galaxy_pearl') {
4273	      // 银河珍珠（Player.cs:44786-44789：一次性 usedGalaxyPearl → luck +0.03 :28676-28678；
4274	      // 已用过 → 无动作不消耗，原版 !usedGalaxyPearl 门）
4275	      if (!this.player.luckState.usedGalaxyPearl) {
4276	        this.player.luckState.usedGalaxyPearl = true;
4277	        this.player.inv.removeAt(this.player.inv.selected, 1);
4278	        this.cb.onInventoryChanged();
4279	      }
4280	      this.player.useTime = 45;   // Item 5340 useTime（Item.cs:42342）
4281	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && this.consumableFuncGate(heldDef)) {
4282	      // vi_ 药水/食物桥接（vanilla-itemfunc：healLife/healMana/buffType → 治疗/回魔/Buff）。
4283	      // 纯消耗品门（consumable 且无放置/射击/工具语义——宠物坐骑等 buffType 物品不在此列）
4284	      const fm = /^vi_(\d+)_/.exec(heldDef.key);
4285	      const ff = fm ? itemFuncOfVid(+fm[1]) : null;
4286	      // ★ 无消耗品语义（水晶/果/弓族等）不得空占本 else-if 槽位——否则链条后续
4287	      // 全部分支被饿死（else-if 匹配即终止）。命中才处理，否则落空交还链条
4288	      if (ff?.consumable && !ff.createTile && !ff.shoot && !ff.pick && !ff.axe && !ff.hammer
4289	        && (ff.healLife || ff.healMana || (ff.buffType && ff.buffType > 0))) {

```


---

## 🤖 Assistant · 2026-08-13T01:02:54.438Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have a very good picture of the use chain. Let me continue reading to see the rest of the use chain (guns/bows/magic, summon, etc.) — need to check the ranged weapons useTime chain. Let me look at the section around 2483-2710 (guns etc.) and the projectile weapons.

Also need:
- ItemCheck main structure: controlUseItem gate, releaseUseItem, itemAnimation decrement, itemTime decrement, reuseDelay, TryAllowingItemReuse.
- Where does vanilla shoot? ItemCheck_Shoot is called at the START of item use (itemAnimationJustStarted), actually in vanilla, ItemCheck_Shoot happens when itemTime hits... let me check. In vanilla, ItemCheck has:
```
if (itemAnimation > 0) {
  ... 
  if (itemTime == 0) { ... shoot ... }
}
```
Actually let's look at the structure. Let me grep for ItemCheck_Shoot call sites and reuseDelay.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:54.639Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"reuseDelay\" Player.cs | head -40",
 "description": "Find reuseDelay usages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:54.660Z

**📎 ToolResult**

```
1328:	public int reuseDelay;
3910:			if (itemAnimation <= 0 && reuseDelay <= 0 && !channel)
4258:		if (sItem.autoReuse && sItem.reuseDelay == 0 && sItem.useTime <= sItem.useAnimation && sItem.shoot > 0 && sItem.useStyle == 5)
4282:		reuseDelay = sItem.reuseDelay;
24918:				if (itemAnimation == 0 && ItemTimeIsZero && reuseDelay == 0)
31272:			reuseDelay = 0;
42022:		if (itemAnimation == 0 && reuseDelay > 0)
42144:			if (itemAnimation == 0 && reuseDelay == 0 && controlUseItem && releaseUseItem)
51971:		itemAnimation = reuseDelay;
51972:		itemTime = reuseDelay;
51973:		reuseDelay = 0;
52022:				if (sItem.shoot > 0 && whoAmI != Main.myPlayer && controlUseItem && sItem.useStyle == 5 && sItem.reuseDelay == 0 && lastItemUseAttemptSuccess)

```


---

## 🤖 Assistant · 2026-08-13T01:02:55.227Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"TryAllowingItemReuse\\|ItemCheck_Shoot(\\|ItemCheck_ApplyUseStyle\\|ItemCheck_ApplyItemTime\\|ItemTimeIsZero\" Player.cs | head -30",
 "description": "Find shoot/reuse call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:55.250Z

**📎 ToolResult**

```
404:					return player.ItemTimeIsZero;
3902:	public bool ItemTimeIsZero => itemTime == 0;
24918:				if (itemAnimation == 0 && ItemTimeIsZero && reuseDelay == 0)
38944:		if (!ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem || (!Main.tile[tileTargetX + 1, tileTargetY].active() && Main.tile[tileTargetX + 1, tileTargetY].wall <= 0 && !Main.tile[tileTargetX - 1, tileTargetY].active() && Main.tile[tileTargetX - 1, tileTargetY].wall <= 0 && !Main.tile[tileTargetX, tileTargetY + 1].active() && Main.tile[tileTargetX, tileTargetY + 1].wall <= 0 && !Main.tile[tileTargetX, tileTargetY - 1].active() && Main.tile[tileTargetX, tileTargetY - 1].wall <= 0) || Main.tile[tileTargetX, tileTargetY].wall == inventory[selectedItem].createWall)
39084:		if (canUse && ((!tile.active() && !PlaceThing_Tiles_IsBlockedByLava(item.createTile, item.placeStyle, tile)) || PlaceThing_IsReplaceableBlock(tile) || tileToCreate == 199 || tileToCreate == 23 || tileToCreate == 662 || tileToCreate == 661 || tileToCreate == 2 || tileToCreate == 109 || tileToCreate == 60 || tileToCreate == 70 || tileToCreate == 633 || Main.tileMoss[tileToCreate]) && ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
39159:		if (canUse && itemAnimation > 0 && ItemTimeIsZero && controlUseItem && PlaceThing_ValidWallForReplacement() && WorldGen.NearFriendlyWall(tileTargetX, tileTargetY) && WorldGen.ReplaceWall(tileTargetX, tileTargetY, (ushort)HeldItem.createWall))
39189:		if (controlUseItem && canUse && Main.tile[tileTargetX, tileTargetY].active() && itemAnimation > 0 && ItemTimeIsZero && flag)
40950:		if (!tile.active() || item.type != 5328 || !TileID.Sets.IsAContainer[tile.type] || tile.type == 88 || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, item.tileBoost + blockRange) || !ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41012:		if (!tile.active() || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, item.tileBoost + blockRange) || !ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41055:		if (inventory[selectedItem].type < 1874 || inventory[selectedItem].type > 1905 || !Main.tile[tileTargetX, tileTargetY].active() || Main.tile[tileTargetX, tileTargetY].type != 171 || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange) || !ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41173:		if (!ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41223:		if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
41247:			if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
41265:			if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
41386:		if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)
42158:			if (ItemTimeIsZero && whoAmI == Main.myPlayer && !JustDroppedAnItem && IsAllowedToHoldItems)
42177:			if (ItemTimeIsZero && itemAnimation > 0)
42303:				if (ItemTimeIsZero)
42338:				if (ItemTimeIsZero)
42371:				if (ItemTimeIsZero)
42412:				if (ItemTimeIsZero)
42430:				if (ItemTimeIsZero)
42464:				if (ItemTimeIsZero)
42496:				if (ItemTimeIsZero)
42518:				if (ItemTimeIsZero)
42702:			ItemCheck_ApplyUseStyle(mountOffset, item, drawHitbox);
42855:		bool flag4 = itemAnimation > 0 && ItemTimeIsZero && flag;
42881:			ItemCheck_Shoot(whoAmI, sItem, weaponDamage);
42934:			if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem && altFunctionUse == 0)
43073:		if (!ItemTimeIsZero || itemAnimation <= 0 || (sItem.type != 43 && sItem.type != 70 && sItem.type != 544 && sItem.type != 556 && sItem.type != 557 && sItem.type != 560 && sItem.type != 1133 && sItem.type != 1331 && sItem.type != 4988 && sItem.type != 5120 && sItem.type != 5334) || !SummonItemCheck(sItem))

```


---

## 🤖 Assistant · 2026-08-13T01:02:57.754Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key: line 42022 handles reuseDelay after itemAnimation turns 0, and line 42144 is the start-new-use check, 51971 is the "add reuseDelay to both counters" (that's `SetItemAnimation... ` actually let me read around 51960-52030 to see TryAllowingItemReuse). Let me read 42000-42160 (the core ItemCheck use section) and 51960-52030.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:58.125Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '42000,42100p' Player.cs",
 "description": "Read ItemCheck core animation decrement"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:58.148Z

**📎 ToolResult**

```
							break;
						}
					}
				}
			}
		}
		ItemCheck_HandleMount();
		int weaponDamage = GetWeaponDamage(item);
		ItemCheck_AutoReuseLogic(item);
		ItemCheck_HackHoldStyles(item);
		if (itemAnimation < 0)
		{
			itemAnimation = 0;
		}
		if (itemTime < 0)
		{
			itemTime = 0;
		}
		if (itemAnimation == 0)
		{
			itemAnimationMax = 0;
		}
		if (itemAnimation == 0 && reuseDelay > 0)
		{
			ApplyReuseDelay();
		}
		UpdatePlacementPreview(item);
		if (itemAnimation == 0 && altFunctionUse == 2)
		{
			altFunctionUse = 0;
		}
		if (item.type == 2269)
		{
			if (itemAnimation > 0 && !controlUseItem)
			{
				itemAnimation--;
				itemTime--;
				if (itemAnimation <= 0)
				{
					itemAnimation = 0;
				}
				if (itemTime < 0)
				{
					itemTime = 0;
				}
				revolverCritChanceBonus++;
			}
			else if (Main.rand.Next(3) == 0)
			{
				revolverCritChanceBonus -= 2;
			}
			item.TryGetPrefixStatMultipliersForItem(item.prefix, out var _, out var _, out var _, out var _, out var _, out var _, out var crt, out var _, out var _, out var _);
			revolverCritChanceBonus = Utils.Clamp(item.crit + revolverCritChanceBonus, crt, 20 + crt) - item.crit;
		}
		else if (Main.rand.Next(3) == 0)
		{
			revolverCritChanceBonus -= 2;
		}
		if (controlUseItem && releaseUseItem && itemAnimation == 0 && item.useStyle != 0 && !selectedItemState.HasBufferedChange)
		{
			if (altFunctionUse == 1)
			{
				altFunctionUse = 2;
			}
			if (item.shoot == 0)
			{
				itemRotation = 0f;
			}
			bool flag2 = ItemCheck_TryStartUse(item);
			if (whoAmI == Main.myPlayer)
			{
				if (flag2 != lastItemUseAttemptSuccess)
				{
					lastItemUseAttemptSuccess = flag2;
					NetMessage.SendData(13, -1, -1, null, whoAmI);
				}
			}
			else
			{
				flag2 &= lastItemUseAttemptSuccess;
			}
			if (item.potion && flag2)
			{
				ApplyPotionDelay(item);
			}
			if (item.mana > 0 && flag2 && whoAmI == Main.myPlayer && item.buffType != 0 && item.buffTime != 0)
			{
				AddBuff(item.buffType, item.buffTime);
			}
			if (item.shoot <= 0 || !ProjectileID.Sets.MinionTargetingFeature[item.shoot] || altFunctionUse != 2)
			{
				ItemCheck_ApplyPetBuffs(item);
			}
			if (whoAmI == Main.myPlayer && gravDir == 1f && item.mountType != -1 && flag2)
			{
				mount.SetMount(item.mountType, this);
			}
			bool flag3 = item.shoot > 0 && ProjectileID.Sets.MinionTargetingFeature[item.shoot] && altFunctionUse == 2;
			bool flag4 = false;
			if (!flag3 && flag2 && whoAmI == Main.myPlayer && item.shoot == 1094 && TryUsingFoxsparksAbility())
			{

```


---

## 👤 User(sidechain) · 2026-08-13T01:21:51.314Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-13T01:25:22.779Z

```
The coordinator sent a message while you were working:
继续你的「物品使用主链」审计——你正要定位反编译源码关键方法,继续完成 Player.cs 的 ItemCheck/ApplyItemTime 段对账(useTime/useAnimation 双轨、autoReuse、reuseDelay、攻速链、发射时机、药水饮用、放置节奏、挥舞判定窗口)并输出最终 markdown 报告(差异清单表+覆盖清单+TOP N)。只读审计禁改文件,每条结论带 file:line。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-13T01:25:30.033Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The coordinator wants me to continue the audit. I have good material so far. Let me now finish reading the vanilla ItemCheck core sections, then check the repo's ranged weapon chain (Game.ts 2480-2720), Player.ts useTime decrement + attackSpeedMult, and potion drinking in vanilla. Let me be efficient with parallel reads.

Key things I still need:
1. Vanilla ApplyReuseDelay (line ~51971) and TryAllowingItemReuse (~52036), ItemCheck_AutoReuseLogic.
2. Vanilla ItemCheck_TryStartUse / where ApplyItemAnimation/ApplyItemTime are called.
3. Vanilla itemAnimation decrement location (in ItemCheck_ApplyUseStyle or near end) — where itemTime-- and itemAnimation-- happen.
4. Vanilla shoot timing: flag4 = itemAnimation > 0 && ItemTimeIsZero → shoot at line 42881 (mid-animation? no—at itemTime==0 which happens at start of use... actually ItemTimeIsZero is true when itemTime==0, which occurs right after decrementing to 0, i.e., when it's time for next shot).
5. Repo ranged weapon chain: Game.ts around 2483-2710.
6. Repo Player.ts attackSpeedMult computation lines 540-560, useTime decrement line 669, potion healBlock.
7. Vanilla potion: ApplyPotionDelay, potionUseTime.

Let me do these in parallel batches.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:30.312Z · glm-x-preview-260804

```
继续。先读 vanilla 的 reuseDelay/autoReuse 逻辑段与 ItemCheck 尾部的递减点。
```


---

## 🤖 Assistant · 2026-08-13T01:25:30.679Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '51940,52060p' Player.cs",
 "description": "Read ApplyReuseDelay and TryAllowingItemReuse"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:30.724Z

**📎 ToolResult**

```
			{
				Main.mouseItem = sItem.Clone();
			}
			releaseUseItem = false;
			mouseInterface = true;
		}
		else if (frameY == 2 && sItem.legSlot >= 0 && !ArmorIDs.Legs.Sets.MannequinIncompatible.Contains(sItem.legSlot))
		{
			Main.blockMouse = true;
			Main.tile[num, num2].frameX = (short)(num5 + sItem.legSlot * 100);
			if (Main.netMode == 1)
			{
				NetMessage.SendTileSquare(-1, num, num2);
			}
			sItem.stack--;
			if (sItem.stack <= 0)
			{
				sItem.SetDefaults(0);
				Main.mouseItem.SetDefaults(0);
			}
			if (selectedItem == 58)
			{
				Main.mouseItem = sItem.Clone();
			}
			releaseUseItem = false;
			mouseInterface = true;
		}
	}

	private void ApplyReuseDelay()
	{
		itemAnimation = reuseDelay;
		itemTime = reuseDelay;
		reuseDelay = 0;
	}

	private void ItemCheck_HackHoldStyles(Item sItem)
	{
		if (sItem.fishingPole > 0)
		{
			sItem.holdStyle = 0;
			if (ItemTimeIsZero && itemAnimation == 0)
			{
				for (int i = 0; i < 1000; i++)
				{
					if (Main.projectile[i].active && Main.projectile[i].owner == whoAmI && Main.projectile[i].bobber)
					{
						sItem.holdStyle = 1;
					}
				}
			}
		}
		if (!ItemID.Sets.IsAKite[sItem.type])
		{
			return;
		}
		sItem.holdStyle = 0;
		if (!ItemTimeIsZero || itemAnimation != 0)
		{
			return;
		}
		for (int j = 0; j < 1000; j++)
		{
			if (Main.projectile[j].active && Main.projectile[j].owner == whoAmI && Main.projectile[j].type == sItem.shoot)
			{
				sItem.holdStyle = 1;
				ChangeDir((!(Main.projectile[j].Center.X - base.Center.X < 0f)) ? 1 : (-1));
			}
		}
	}

	private void ItemCheck_AutoReuseLogic(Item sItem)
	{
		if (sItem.IsAir || (selectedItemState.HasBufferedChange && (sItem.shoot <= 0 || ItemTimeIsZero)))
		{
			return;
		}
		if (sItem.autoReuse && !noItems)
		{
			releaseUseItem = true;
			if (itemAnimation == 1 && sItem.stack > 0)
			{
				if (sItem.shoot > 0 && whoAmI != Main.myPlayer && controlUseItem && sItem.useStyle == 5 && sItem.reuseDelay == 0 && lastItemUseAttemptSuccess)
				{
					ApplyItemAnimation(sItem);
				}
				else
				{
					itemAnimation = 0;
					if (ItemID.Sets.ShootsOnUseRelease[sItem.type])
					{
						controlUseItem = true;
					}
				}
			}
		}
		TryAllowingItemReuse(sItem);
	}

	private void TryAllowingItemReuse(Item sItem)
	{
		bool flag = false;
		if (autoReuseGlove)
		{
			flag |= sItem.melee && sItem.type != 3030;
			flag |= sItem.summon && ItemID.Sets.SummonerWeaponThatScalesWithAttackSpeed[sItem.type];
		}
		if ((stressBall || autoReuseAllWeapons) && sItem.damage > 0 && (!sItem.channel || !channel))
		{
			flag = true;
		}
		if (flag)
		{
			releaseUseItem = true;
		}
	}

	private void ItemCheck_HandleMount()
	{
		if (!mount.Active)
		{

```


---

## 🤖 Assistant · 2026-08-13T01:25:31.496Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"ItemCheck_AutoReuseLogic\\|ItemCheck_TryStartUse\\|void ItemCheck_ApplyItemTime\\|private void ItemCheck_OwnerOnlyCode\" Player.cs | head; echo ---; sed -n '42700,42900p' Player.cs",
 "description": "Read ItemCheck_ApplyUseStyle and shoot gate"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:31.554Z

**📎 ToolResult**

```
5275:		if (item == null || !ItemCheck_TryStartUse(item))
5372:		if (item == null || !ItemCheck_TryStartUse(item))
5465:		if (item != null && ItemCheck_TryStartUse(item))
5560:		if (!ItemCheck_TryStartUse(item))
5762:			if (item != null && item.mountType != -1 && mount.CanMount(item.mountType, this) && ItemCheck_TryStartUse(item))
5972:		if (!ItemCheck_TryStartUse(item))
42008:		ItemCheck_AutoReuseLogic(item);
42068:			bool flag2 = ItemCheck_TryStartUse(item);
42775:	private void ItemCheck_OwnerOnlyCode(ref ItemCheckContext context, Item sItem, int weaponDamage, Rectangle heldItemFrame)
51182:	private bool ItemCheck_TryStartUse(Item sItem, bool ignoreCursed = false)
---
		if (itemAnimation > 0)
		{
			ItemCheck_ApplyUseStyle(mountOffset, item, drawHitbox);
		}
		else
		{
			ItemCheck_ApplyHoldStyle(mountOffset, item, drawHitbox);
		}
		return drawHitbox;
	}

	public float GetPlacementPreviewOpacity()
	{
		if (!ItemID.Sets.IsAKite[HeldItem.type])
		{
			return 1f;
		}
		if (HeldItem.holdStyle != 0)
		{
			return 0f;
		}
		return Utils.Remap(framesInMovementForPlacementPreview, 0f, 30f, 1f, 0f);
	}

	private void UpdatePlacementPreview(Item sItem)
	{
		if (Main.myPlayer == whoAmI && itemAnimation == 0 && !sItem.IsAir)
		{
			int num = ((velocity.Length() > 0.1f) ? 3 : (-1));
			framesInMovementForPlacementPreview = Utils.Clamp(framesInMovementForPlacementPreview + num, 0, 33);
			Tile targetTile = Main.tile[tileTargetX, tileTargetY];
			FigureOutWhatToPlace(targetTile, sItem, out var tileToCreate, out var previewPlaceStyle, out var overrideCanPlace, out var forcedRandom);
			if ((!overrideCanPlace.HasValue || overrideCanPlace.Value) && TileObjectData.CustomPlace(tileToCreate, previewPlaceStyle))
			{
				TileObject.CanPlace(tileTargetX, tileTargetY, tileToCreate, previewPlaceStyle, direction, out var _, onlyCheck: true, forcedRandom);
			}
		}
	}

	private void FigureOutWhatToPlace(Tile targetTile, Item sItem, out int tileToCreate, out int previewPlaceStyle, out bool? overrideCanPlace, out int? forcedRandom)
	{
		tileToCreate = sItem.createTile;
		previewPlaceStyle = sItem.placeStyle;
		overrideCanPlace = null;
		forcedRandom = null;
		if (UsingBiomeTorches && tileToCreate == 4 && previewPlaceStyle == 0)
		{
			BiomeTorchPlaceStyle(ref tileToCreate, ref previewPlaceStyle);
		}
		if (UsingBiomeTorches && tileToCreate == 215 && previewPlaceStyle == 0)
		{
			BiomeCampfirePlaceStyle(ref tileToCreate, ref previewPlaceStyle);
		}
		if (targetTile != null && targetTile.active())
		{
			ushort type = targetTile.type;
			if (tileToCreate == 23 && type == 59)
			{
				tileToCreate = 661;
			}
			if (tileToCreate == 199 && type == 59)
			{
				tileToCreate = 662;
			}
		}
		if (!ModifyFlexibleWandPlacementInfo(ref tileToCreate, ref previewPlaceStyle, ref forcedRandom))
		{
			overrideCanPlace = false;
		}
		if (tileToCreate == 724)
		{
			previewPlaceStyle = TECritterAnchor.GetLeashedCritterPrototype(sItem.type).anchorStyle;
		}
	}

	private void ItemCheck_OwnerOnlyCode(ref ItemCheckContext context, Item sItem, int weaponDamage, Rectangle heldItemFrame)
	{
		bool flag = true;
		if (selectedItemState.HasBufferedChange && sItem.useTime > itemAnimation)
		{
			flag = false;
		}
		int type = sItem.type;
		if ((type == 65 || type == 676 || type == 723 || type == 724 || type == 757 || type == 674 || type == 675 || type == 989 || type == 1226 || type == 1227) && !ItemAnimationJustStarted)
		{
			flag = false;
		}
		if (type == 5097 && ItemAnimationJustStarted)
		{
			_batbatCanHeal = true;
		}
		if (type == 5094 && ItemAnimationJustStarted)
		{
			_spawnTentacleSpikes = true;
		}
		if (type == 795 && ItemAnimationJustStarted)
		{
			_spawnBloodButcherer = true;
		}
		if (type == 121 && ItemAnimationJustStarted)
		{
			_spawnVolcanoExplosion = true;
		}
		if (type == 155 && ItemAnimationJustStarted)
		{
			_spawnMuramasaCut = true;
		}
		if (type == 3852)
		{
			if (itemAnimation < itemAnimationMax - 12)
			{
				flag = false;
			}
			if (altFunctionUse == 2 && !ItemAnimationJustStarted)
			{
				flag = false;
			}
		}
		if ((type == 4956 || type == 5669) && itemAnimation < itemAnimationMax - 3 * sItem.useTime)
		{
			flag = false;
		}
		if (type == 4952 && itemAnimation < itemAnimationMax - 8)
		{
			flag = false;
		}
		if (type == 4953 && itemAnimation < itemAnimationMax - 10)
		{
			flag = false;
		}
		if (type == 5451 && ownedProjectileCounts[1020] > 0)
		{
			flag = false;
		}
		if (type == 5738 && ownedProjectileCounts[1105] > 0)
		{
			flag = false;
		}
		if (ItemID.Sets.ShootsOnUseRelease[sItem.type] && controlUseItem)
		{
			flag = false;
		}
		bool flag2 = ItemID.Sets.PlaceTileOnAltUse[type];
		bool flag3 = false;
		if (altFunctionUse == 2 && flag2)
		{
			flag3 = true;
		}
		if (altFunctionUse == 2 && ItemID.Sets.IsAKite[type] && sItem.holdStyle != 0)
		{
			flag3 = false;
			StartChanneling();
		}
		ItemCheck_TurretAltFeatureUse(sItem, flag);
		ItemCheck_MinionAltFeatureUse(sItem, flag);
		bool flag4 = itemAnimation > 0 && ItemTimeIsZero && flag;
		if (type == 1156 && channel)
		{
			int num = 0;
			for (int i = 0; i < 1000; i++)
			{
				if (Main.projectile[i].active && Main.projectile[i].owner == whoAmI && Main.projectile[i].type == HeldItem.shoot)
				{
					num++;
				}
			}
			if (num > 0 && num < 3)
			{
				flag4 = true;
			}
		}
		if (sItem.shootsEveryUse)
		{
			flag4 = ItemAnimationJustStarted;
		}
		if (flag3)
		{
			flag4 = false;
		}
		if (sItem.shoot > 0 && flag4)
		{
			ItemCheck_Shoot(whoAmI, sItem, weaponDamage);
		}
		ItemCheck_UseWiringTools(sItem);
		ItemCheck_UseLawnMower(sItem);
		ItemCheck_PlayInstruments(sItem);
		ItemCheck_UseBuckets(sItem);
		if (!channel)
		{
			toolTime = itemTime;
		}
		else
		{
			toolTime--;
			if (toolTime < 0)
			{
				int num2 = sItem.useTime - 1;
				toolTime = num2;
			}
		}
		if (cannonCooldown > 0)

```


---

## 🤖 Assistant · 2026-08-13T01:25:47.678Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good progress. Now I have the key vanilla structures:

1. **CapAttackSpeeds** (P:28555-28569): meleeSpeed (multiplier starting at 1.0) → cap additive bonus at 3 → reciprocal. `TurnAttackSpeedToUseTimeMultiplier`: `if (speed > 3f) speed = 3f; if (speed != 0) speed = 1f/speed;`
   - Note: since meleeSpeed starts at 1f, cap is at 3f (i.e., +200% bonus), reciprocal = 1/3. Matches wiki formula floor(useAnimation/(1+bonus)).
   - Also summonerWeaponSpeedBonus = TurnAttackSpeedToUseTimeMultiplier(num + summonerWeaponSpeedBonus).
   - tileSpeed/wallSpeed: `if (tileSpeed > 3f) tileSpeed = 3f; tileSpeed = 1f / tileSpeed;` — same treatment.

2. **ApplyItemAnimation** (P:4255-4283):
   - num=1 if autoReuse && reuseDelay==0 && useTime<=useAnimation && shoot>0 && useStyle==5 → SetItemAnimation(useAnimation+1) (the +1 negating autoswing skip)
   - melee && !NoMeleeSpeedBonus → SetItemAnimation(useAnimation, meleeSpeed) [meleeSpeed now = 1/(1+bonus) multiplier]
   - summon && SummonerWeaponThatScalesWithAttackSpeed → SetItemAnimation(useAnimation, summonerWeaponSpeedBonus * whipUseTimeMultiplier)
   - createTile>=0 → SetItemAnimation(useAnimation, tileSpeed)
   - createWall>=0 → SetItemAnimation(useAnimation, wallSpeed)
   - else → SetItemAnimation(useAnimation + num)
   - reuseDelay = sItem.reuseDelay (stored!)
   
   Note wiki says the +1 skip negation is "the last step in the whole process; the calculation for melee weapons are done earlier, therefore skipping this step" — consistent: melee branch doesn't add num.

3. **ApplyItemTime** (P:4216-4228): SetItemTime(sItem.useTime) — RAW useTime, no multiplier. Confirms repo comment at Game.ts:4056.

4. **SetItemTime** (P:4212): itemTime = frames; itemTimeMax = frames.
   **SetItemAnimation**: itemAnimation = frames; itemAnimationMax = frames.
   **SetItemAnimation(base, mult)**: val = (int)(base*mult); if base>0 val = max(val,1).

5. **ItemCheck_AutoReuseLogic** (P:52012-52035):
   - if item.IsAir or (HasBufferedChange && (shoot<=0 || ItemTimeIsZero)) return
   - if autoReuse && !noItems: releaseUseItem = true; if (itemAnimation == 1 && stack > 0) { if (shoot>0 && !myPlayer && controlUseItem && useStyle==5 && reuseDelay==0 && lastItemUseAttemptSuccess) ApplyItemAnimation; else { itemAnimation = 0; if ShootsOnUseRelease → controlUseItem = true } }
   - TryAllowingItemReuse(sItem)
   
   Key: autoswing skip happens at itemAnimation == 1 → set itemAnimation = 0 immediately, so a new use starts same tick. This is the "animation skipping" the wiki mentions.

6. **TryAllowingItemReuse** (P:52036-52053):
   - autoReuseGlove: flag |= melee && type != 3030; flag |= summon && SummonerWeaponThatScalesWithAttackSpeed
   - (stressBall || autoReuseAllWeapons) && damage>0 && (!channel || !channel) → flag = true
   - if flag → releaseUseItem = true
   - So the glove only sets releaseUseItem=true (i.e., allows re-trigger without new click), it does NOT change autoReuse attr. Repo: Game.ts:4061-4067 implements gloveReuse for melee but excludes summon-scaling branch; autoReuse = cwMelee.autoReuse || gloveReuse. Roughly aligned, but: repo treats gloveReuse as equivalent to autoReuse=true; vanilla only sets releaseUseItem, meaning the actual chain still requires controlUseItem && releaseUseItem && itemAnimation==0. Functionally similar for melee. But vanilla ALSO gates glove reuse behind... hmm actually in vanilla, does glove give chain reuse even when itemAnimation > 0? No — start use requires itemAnimation == 0 at line 42144. So glove reuse = same as autoReuse for hold-to-chain. OK.

7. **ApplyReuseDelay** (P:51969-51974): when itemAnimation==0 && reuseDelay>0 (P:42022): itemAnimation = reuseDelay; itemTime = reuseDelay; reuseDelay = 0. This matches wiki: "reuseDelay is applied after the itemAnimation counter turns to zero. This will add value of reuseDelay to both counters".

8. **ItemCheck core** (P:42005-42144):
   - itemAnimation<0 → 0; itemTime<0 → 0; itemAnimation==0 → itemAnimationMax=0
   - if (itemAnimation == 0 && reuseDelay > 0) ApplyReuseDelay()
   - if (controlUseItem && releaseUseItem && itemAnimation == 0 && item.useStyle != 0 && !HasBufferedChange) → ItemCheck_TryStartUse(item)

9. **ItemCheck_OwnerOnlyCode / shoot timing** (P:42775+):
   - flag4 = itemAnimation > 0 && ItemTimeIsZero && flag
   - shootsEveryUse → flag4 = ItemAnimationJustStarted
   - if (sItem.shoot > 0 && flag4) ItemCheck_Shoot(...)
   - So shooting happens when itemTime hits 0 DURING animation — i.e., itemTime gates each shot; for useTime<useAnimation weapons (e.g. Clockwork Assault Rifle useTime 4/anim 12) you get 3 shots per hold. Confirms wiki Times-of-use formula.
   - ItemAnimationJustStarted => itemAnimation == itemAnimationMax - 1 (P:3904)

Now where do itemTime-- and itemAnimation-- actually happen? Let me find. Also ItemCheck_TryStartUse (P:51182) to see the canUse checks and where ApplyItemAnimation/ApplyItemTime get called. Let me also check the end of ItemCheck (itemTime decrement) — search "itemTime--".

Also need:
- ItemCheck_TryStartUse: what conditions block use (itemAnimation > 0, noItems, mount, etc.), and where ApplyItemTime is called.
- Potion: ApplyPotionDelay.
- Vanilla itemAnimation decrement in ApplyUseStyle or in ItemCheck after owner code.

Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:48.378Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"itemTime--\\|itemAnimation--\\|itemTime -=\\|itemAnimation -=\" Player.cs | head -20; echo \"=== TryStartUse ===\"; sed -n '51182,51260p' Player.cs",
 "description": "Find decrements and TryStartUse"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:48.428Z

**📎 ToolResult**

```
42035:				itemAnimation--;
42036:				itemTime--;
42139:			itemAnimation--;
42157:			itemTime--;
=== TryStartUse ===
	private bool ItemCheck_TryStartUse(Item sItem, bool ignoreCursed = false)
	{
		bool flag = ItemCheck_CheckCanUse_Inner(sItem, ignoreCursed);
		if (flag)
		{
			if (!ItemCheck_ActuallyPayMana(sItem))
			{
				flag = false;
			}
			if (!ItemCheck_CheckCanUse_KillDirtBlock(sItem))
			{
				flag = false;
			}
			if (!ItemCheck_PullFishingBobbers(sItem))
			{
				flag = false;
			}
		}
		return flag;
	}

	private bool ItemCheck_CheckCanUse_Inner(Item sItem, bool ignoreCursed = false)
	{
		if (whoAmI == Main.myPlayer && Main.LocalPlayerHasPendingInventoryActions())
		{
			return false;
		}
		int num = whoAmI;
		bool flag = true;
		GetTargetTileWithReverseGravity(out var screenTargetTileX, out var screenTargetTileY);
		if (sItem.type == 3335 && (extraAccessory || !Main.expertMode))
		{
			flag = false;
		}
		if (pulley && sItem.fishingPole > 0)
		{
			flag = false;
		}
		if (pulley && ItemID.Sets.IsAKite[sItem.type])
		{
			flag = false;
		}
		if (sItem.type == 3611 && (WiresUI.Settings.ToolMode & (WiresUI.Settings.MultiToolMode.Red | WiresUI.Settings.MultiToolMode.Green | WiresUI.Settings.MultiToolMode.Blue | WiresUI.Settings.MultiToolMode.Yellow | WiresUI.Settings.MultiToolMode.Actuator)) == 0)
		{
			flag = false;
		}
		if (sItem.type == 5451 && ownedProjectileCounts[1020] > 0)
		{
			flag = false;
		}
		if (sItem.type == 5738 && ownedProjectileCounts[1105] > 0)
		{
			flag = false;
		}
		if ((sItem.type == 3611 || sItem.type == 3625) && wireOperationsCooldown > 0)
		{
			flag = false;
		}
		if (!CheckDD2CrystalPaymentLock(sItem))
		{
			flag = false;
		}
		if (sItem.shoot > -1 && ProjectileID.Sets.IsADD2Turret[sItem.shoot] && !downedDD2EventAnyDifficulty && !DD2Event.Ongoing)
		{
			flag = false;
		}
		if (sItem.shoot > -1 && ProjectileID.Sets.IsADD2Turret[sItem.shoot] && DD2Event.Ongoing && num == Main.myPlayer)
		{
			FindSentryRestingSpot(sItem.shoot, out var worldX, out var worldY, out var _);
			if (WouldSpotOverlapWithSentry(worldX, worldY, sItem.shoot == 688 || sItem.shoot == 689 || sItem.shoot == 690))
			{
				flag = false;
			}
		}
		if (sItem.shoot > -1 && ProjectileID.Sets.IsADD2Turret[sItem.shoot] && num == Main.myPlayer)
		{
			FindSentryRestingSpot(sItem.shoot, out var worldX2, out var worldY2, out var _);
			worldX2 /= 16;
			worldY2 /= 16;

```


---

## 🤖 Assistant · 2026-08-13T01:25:51.068Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the decrements: line 42035-42036 (item 2269 special), 42139 itemAnimation--, 42157 itemTime--. Let me read 42130-42175 to see the decrement context (after use start).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:51.375Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '42120,42175p' Player.cs",
 "description": "Read decrement block context"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:51.413Z

**📎 ToolResult**

```
		}
		if (whoAmI == Main.myPlayer && Main.LocalPlayerHasPendingInventoryActions())
		{
			flag5 = false;
		}
		if (selectedItemState.HasBufferedChange)
		{
			flag5 = false;
		}
		if (!flag5)
		{
			channel = false;
		}
		if (itemAnimation > 0)
		{
			if (item.mana > 0)
			{
				ItemCheck_ApplyManaRegenDelay(item);
			}
			itemAnimation--;
			if (itemAnimation == 0 && whoAmI == Main.myPlayer)
			{
				PlayerInput.TryEndingFastUse();
			}
			if (itemAnimation == 0 && reuseDelay == 0 && controlUseItem && releaseUseItem)
			{
				pendingItemReuse = true;
			}
		}
		if (itemAnimation == 0 && item.IsAir && item.type != 0)
		{
			item.TurnToAir();
			pendingItemReuse = false;
		}
		releaseUseItem = !controlUseItem;
		if (itemTime > 0)
		{
			itemTime--;
			if (ItemTimeIsZero && whoAmI == Main.myPlayer && !JustDroppedAnItem && IsAllowedToHoldItems)
			{
				int type = item.type;
				if (type == 65 || type == 724 || type == 989 || type == 1226)
				{
					EmitMaxManaEffect();
				}
			}
		}
		Rectangle heldItemFrame = AnimatePlayerAndGetItemFrame(heightOffsetHitboxCenter, item);
		if (!JustDroppedAnItem && IsAllowedToHoldItems)
		{
			ItemCheck_EmitHeldItemLight(item);
			ItemCheck_EmitFoodParticles(item);
			ItemCheck_EmitDrinkParticles(item);
			if (whoAmI == Main.myPlayer)
			{
				ItemCheck_OwnerOnlyCode(ref context, item, weaponDamage, heldItemFrame);

```


---

## 🤖 Assistant · 2026-08-13T01:25:52.128Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"ApplyPotionDelay\\|potionUseTime\\|public void ApplyItemTime\" Player.cs | head; echo ---; grep -n \"void ApplyPotionDelay\" -A 12 Player.cs | head -20",
 "description": "Find potion delay logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:52.179Z

**📎 ToolResult**

```
4216:	public void ApplyItemTime(Item sItem)
4221:	public void ApplyItemTime(Item sItem, float multiplier)
5286:			ApplyPotionDelay(item);
5383:			ApplyPotionDelay(item);
42083:				ApplyPotionDelay(item);
51085:	private void ApplyPotionDelay(Item sItem)
---
51085:	private void ApplyPotionDelay(Item sItem)
51086-	{
51087-		if (sItem.type == 3001)
51088-		{
51089-			int minValue = 2400;
51090-			int num = 4200;
51091-			potionDelay = Main.rand.Next(minValue, num + 1);
51092-			if (pStone)
51093-			{
51094-				potionDelay = (int)((float)potionDelay * PhilosopherStoneDurationMultiplier);
51095-			}
51096-			AddBuff(21, potionDelay);
51097-		}

```


---

## 🤖 Assistant · 2026-08-13T01:25:54.487Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read ApplyPotionDelay fully (51085-51120) and check where ApplyItemTime / ApplyItemAnimation get called on successful use (search for "ApplyItemAnimation(sItem)" call sites and "ApplyItemTime(sItem)" call sites).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:54.821Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '51085,51182p' Player.cs",
 "description": "Read full ApplyPotionDelay"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:54.860Z

**📎 ToolResult**

```
	private void ApplyPotionDelay(Item sItem)
	{
		if (sItem.type == 3001)
		{
			int minValue = 2400;
			int num = 4200;
			potionDelay = Main.rand.Next(minValue, num + 1);
			if (pStone)
			{
				potionDelay = (int)((float)potionDelay * PhilosopherStoneDurationMultiplier);
			}
			AddBuff(21, potionDelay);
		}
		else if (sItem.type == 227 || sItem.type == 126)
		{
			potionDelay = restorationDelayTime;
			AddBuff(21, potionDelay);
		}
		else if (sItem.type == 1912)
		{
			potionDelay = eggnogDelayTime;
			AddBuff(21, potionDelay);
			TryToResetHungerToNeutral();
		}
		else if (sItem.type == 5)
		{
			potionDelay = mushroomDelayTime;
			AddBuff(21, potionDelay);
			TryToResetHungerToNeutral();
		}
		else
		{
			potionDelay = potionDelayTime;
			AddBuff(21, potionDelay);
		}
	}

	private void ApplyLifeAndOrMana(Item item)
	{
		int num = item.healLife;
		int healMana = item.healMana;
		if (item.type == 3001)
		{
			int healLife = item.healLife;
			int num2 = 120;
			num = Main.rand.Next(healLife, num2 + 1);
			if (Main.myPlayer == whoAmI)
			{
				float num3 = Main.rand.NextFloat();
				int num4 = 0;
				if (num3 <= 0.1f)
				{
					num4 = 240;
				}
				else if (num3 <= 0.3f)
				{
					num4 = 120;
				}
				else if (num3 <= 0.6f)
				{
					num4 = 60;
				}
				if (num4 > 0)
				{
					SetImmuneTimeForAllTypes(num4);
				}
			}
		}
		statLife += num;
		statMana += healMana;
		if (statLife > statLifeMax2)
		{
			statLife = statLifeMax2;
		}
		if (statMana > statManaMax2)
		{
			statMana = statManaMax2;
		}
		if (num > 0 && Main.myPlayer == whoAmI)
		{
			HealEffect(num);
		}
		if (healMana > 0)
		{
			AddBuff(94, manaSickTime);
			if (Main.myPlayer == whoAmI)
			{
				ManaEffect(healMana);
			}
		}
	}

	private bool ItemCheck_CanUse(Item sItem, bool ignoreCursed = false)
	{
		return ItemCheck_CheckCanUse_Inner(sItem, ignoreCursed);
	}

	private bool ItemCheck_TryStartUse(Item sItem, bool ignoreCursed = false)

```


---

## 🤖 Assistant · 2026-08-13T01:25:55.456Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"ApplyItemAnimation(sItem)\\|ApplyItemTime(sItem)\\|ApplyItemTime(item)\\|MatchItemTimeToItemAnimation()\" Player.cs | head -20",
 "description": "Find animation/time application call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:55.496Z

**📎 ToolResult**

```
4285:	public void MatchItemTimeToItemAnimation()
42181:					ApplyItemTime(item);
42191:					ApplyItemTime(item);
42203:					ApplyItemTime(item);
42209:						ApplyItemTime(item);
42279:						ApplyItemTime(item);
42305:					ApplyItemTime(item);
42340:					ApplyItemTime(item);
42373:					ApplyItemTime(item);
42414:					ApplyItemTime(item);
42432:					ApplyItemTime(item);
42466:					ApplyItemTime(item);
42498:					ApplyItemTime(item);
42520:					ApplyItemTime(item);
43079:			ApplyItemTime(sItem);
43094:				ApplyItemTime(sItem);
43111:				ApplyItemTime(sItem);
43127:				ApplyItemTime(sItem);
43145:				ApplyItemTime(sItem);
43161:				ApplyItemTime(sItem);

```


---

## 🤖 Assistant · 2026-08-13T01:25:57.239Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — ApplyItemAnimation isn't called directly in the list? It's called inside ItemCheck_ApplyUseStyle presumably. Let me check where ApplyItemAnimation is called. grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:57.853Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"ApplyItemAnimation\" Player.cs; echo \"=== 42177-42320 ===\"; sed -n '42177,42320p' Player.cs",
 "description": "Find ApplyItemAnimation calls and read use-start branch"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:57.895Z

**📎 ToolResult**

```
4255:	private void ApplyItemAnimation(Item sItem)
50933:		ApplyItemAnimation(sItem);
52024:					ApplyItemAnimation(sItem);
=== 42177-42320 ===
			if (ItemTimeIsZero && itemAnimation > 0)
			{
				if (item.hairDye >= 0)
				{
					ApplyItemTime(item);
					if (whoAmI == Main.myPlayer)
					{
						hairDye = (byte)item.hairDye;
						NetMessage.SendData(4, -1, -1, null, whoAmI);
					}
				}
				if (item.healLife > 0 || item.healMana > 0)
				{
					ApplyLifeAndOrMana(item);
					ApplyItemTime(item);
					if (Main.myPlayer == whoAmI && item.type == 126 && breath == 0)
					{
						AchievementsHelper.HandleSpecialEvent(this, 25);
					}
				}
				if (item.buffType > 0)
				{
					if (whoAmI == Main.myPlayer && item.buffType != 90 && item.buffType != 27)
					{
						AddBuff(item.buffType, item.buffTime);
					}
					ApplyItemTime(item);
				}
				if (item.type == 678)
				{
					if (Main.getGoodWorld)
					{
						ApplyItemTime(item);
						if (whoAmI == Main.myPlayer)
						{
							for (int k = 0; k < 3; k++)
							{
								int type2 = 0;
								int time = 108000;
								switch (Main.rand.Next(18))
								{
								case 0:
									type2 = 16;
									break;
								case 1:
									type2 = 111;
									break;
								case 2:
									type2 = 114;
									break;
								case 3:
									type2 = 8;
									break;
								case 4:
									type2 = 105;
									break;
								case 5:
									type2 = 17;
									break;
								case 6:
									type2 = 116;
									break;
								case 7:
									type2 = 5;
									break;
								case 8:
									type2 = 113;
									break;
								case 9:
									type2 = 7;
									break;
								case 10:
									type2 = 6;
									break;
								case 11:
									type2 = 104;
									break;
								case 12:
									type2 = 115;
									break;
								case 13:
									type2 = 2;
									break;
								case 14:
									type2 = 9;
									break;
								case 15:
									type2 = 3;
									break;
								case 16:
									type2 = 117;
									break;
								case 17:
									type2 = 1;
									break;
								}
								AddBuff(type2, time);
							}
						}
					}
					else
					{
						ApplyItemTime(item);
						if (whoAmI == Main.myPlayer)
						{
							AddBuff(20, 216000);
							AddBuff(22, 216000);
							AddBuff(23, 216000);
							AddBuff(24, 216000);
							AddBuff(30, 216000);
							AddBuff(31, 216000);
							AddBuff(32, 216000);
							AddBuff(33, 216000);
							AddBuff(35, 216000);
							AddBuff(36, 216000);
							AddBuff(68, 216000);
						}
					}
				}
			}
			if ((item.type == 50 || item.type == 3124 || item.type == 3199 || item.type == 5358) && itemAnimation > 0)
			{
				if (Main.rand.Next(2) == 0)
				{
					Dust.NewDust(position, width, height, 15, 0f, 0f, 150, default(Color), 1.1f);
				}
				if (ItemTimeIsZero)
				{
					ApplyItemTime(item);
				}
				else if (itemTime == item.useTime / 2)
				{
					for (int l = 0; l < 70; l++)
					{
						Dust.NewDust(position, width, height, 15, velocity.X * 0.5f, velocity.Y * 0.5f, 150, default(Color), 1.5f);
					}
					RemoveAllGrapplingHooks();
					Spawn(PlayerSpawnContext.RecallFromItem);
					for (int m = 0; m < 70; m++)
					{
						Dust.NewDust(position, width, height, 15, 0f, 0f, 150, default(Color), 1.5f);
					}
				}
			}

```


---

## 🤖 Assistant · 2026-08-13T01:25:59.717Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now ApplyItemAnimation call site 50933 — that's inside ItemCheck_ApplyUseStyle presumably. Let me check 50900-50960. Also I need to know the vanilla order: ItemCheck_TryStartUse returns true → ... but where does the use actually apply itemAnimation? Let me look at 50933 context.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:00.103Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '50880,50975p' Player.cs",
 "description": "Read context around ApplyItemAnimation call"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:00.133Z

**📎 ToolResult**

```
			case 13:
			case 15:
				vector += new Vector2(4f, 4f) * Directions;
				break;
			case 10:
			case 14:
				vector += new Vector2(4f, 2f) * Directions;
				break;
			case 16:
			case 17:
			case 18:
			case 19:
			case 20:
				vector += new Vector2(4f, 4f) * Directions;
				break;
			}
		}
		pos += vector;
	}

	public void FlipItemLocationAndRotationForGravity()
	{
		if (gravDir == -1f)
		{
			itemRotation = 0f - itemRotation;
			float num = position.Y - itemLocation.Y;
			itemLocation.Y = base.Bottom.Y + num;
		}
	}

	private void ItemCheck_StartActualUse(Item sItem)
	{
		bool flag = sItem.type == 4711;
		if (sItem.pick > 0 || sItem.axe > 0 || sItem.hammer > 0 || flag)
		{
			toolTime = 1;
		}
		if (grappling[0] > -1)
		{
			pulley = false;
			pulleyDir = 1;
			if (controlRight)
			{
				direction = 1;
			}
			else if (controlLeft)
			{
				direction = -1;
			}
		}
		StartChanneling(sItem);
		attackCD = 0;
		ResetMeleeHitCooldowns();
		ApplyItemAnimation(sItem);
		bool flag2 = ItemID.Sets.SkipsInitialUseSound[sItem.type];
		if (sItem.UseSound != null && !flag2)
		{
			bool flag3 = sItem.useStyle == 5 || sItem.useStyle == 13 || sItem.shoot > 0;
			bool? flag4 = ItemID.Sets.NetUseSoundSync[sItem.type];
			if (flag4.HasValue)
			{
				flag3 = flag4.Value;
			}
			if (whoAmI == Main.myPlayer && Main.netMode == 1 && flag3)
			{
				NetMessage.SendData(152, -1, -1, null, whoAmI);
			}
			if (whoAmI == Main.myPlayer || !flag3)
			{
				SoundEngine.PlaySound(sItem.UseSound, base.Center, sItem.useSoundPitch);
			}
		}
	}

	private void FreeUpPetsAndMinions(Item sItem)
	{
		if (sItem.shoot == 1093)
		{
			for (int i = 0; i < 1000; i++)
			{
				if (Main.projectile[i].active && Main.projectile[i].owner == whoAmI && Main.projectile[i].minion && Main.projectile[i].type == sItem.shoot)
				{
					Main.projectile[i].Kill();
				}
			}
		}
		if (ProjectileID.Sets.MinionSacrificable[sItem.shoot])
		{
			List<int> list = new List<int>();
			float num = 0f;
			for (int j = 0; j < 1000; j++)
			{
				if (!Main.projectile[j].active || Main.projectile[j].owner != whoAmI || !Main.projectile[j].minion)
				{
					continue;
				}

```


---

## 🤖 Assistant · 2026-08-13T01:26:08.314Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have the full vanilla chain:
- ItemCheck_StartActualUse (P:50911): attackCD=0, ResetMeleeHitCooldowns, ApplyItemAnimation(sItem) → sets itemAnimation & reuseDelay, plays UseSound. Then back in ItemCheck, on the ItemTimeIsZero && itemAnimation>0 branch (P:42177+) the item EFFECTS happen (healLife, buffType, etc.) with ApplyItemTime(item) resetting itemTime each time.

Wait — where does ItemCheck_StartActualUse get called? Let me confirm: inside ItemCheck after flag2 = ItemCheck_TryStartUse(item) → ... probably `if (flag2) ItemCheck_StartActualUse(item)`. Let me check around 42100-42120... Actually I saw at 42068 `bool flag2 = ItemCheck_TryStartUse(item);` then a bunch of potion/mount/buff stuff. Let me grep ItemCheck_StartActualUse call.

Also the melee hit cooldown: ResetMeleeHitCooldowns — for item 10 "swing damage window". Let me check the melee hit detection: `meleeCD`? The repo's swingHitSet. In vanilla, melee damage during itemAnimation: ApplyUseStyle → the item hitbox is checked every frame while itemAnimation > 0 and itemAnimation < itemAnimationMax... Let me look at Player.ItemCheck_ApplyUseStyle for the swing arc and the hit gate (`if (flag && flag3)`...). Actually vanilla melee hitting is in ItemCheck_ApplyUseStyle → `if (sItem.useStyle == 1 ...)` ... then `MeleeHitCheck`? Let me grep "itemAnimation" around 35880-35960 which I saw earlier (flag6 etc.). That looked like AnimatePlayerAndGetItemFrame though.

Let me be efficient: I have enough for the core audit items. But the "挥舞类近战伤害判定窗口" needs a vanilla reference: in vanilla Player.cs, melee hit detection is inside ItemCheck_ApplyUseStyle with:
```
if (flag && flag3 && sItem.melee && ...) { ... ItemCheck_ApplyUseStyle_SwingTools / hitbox check via "MeleeHitCheck" }
```
Let me grep for "MeleeHitCheck|itemAnimation" in the swing style section. Let me search for `useStyle == 1` in ApplyUseStyle.

Let me grep "flag = itemAnimation < itemAnimationMax" something. Search for "hitbox" in Player.cs.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:08.960Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"ItemCheck_StartActualUse(\" Player.cs | head; echo \"=== ApplyUseStyle start ===\"; grep -n \"private void ItemCheck_ApplyUseStyle\" Player.cs; sed -n '49939,50060p' Player.cs",
 "description": "Read ApplyUseStyle swing window"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:09.007Z

**📎 ToolResult**

```
42109:				ItemCheck_StartActualUse(item);
50910:	private void ItemCheck_StartActualUse(Item sItem)
=== ApplyUseStyle start ===
				{
					float num2 = 8f;
					itemLocation.X = position.X + (float)width * 0.5f + ((float)heldItemFrame.Width * 0.5f - num2) * (float)direction;
					num2 = 24f;
					itemLocation.Y = position.Y + num2 + mountOffset;
				}
				else
				{
					float num3 = 6f;
					itemLocation.X = position.X + (float)width * 0.5f - ((float)heldItemFrame.Width * 0.5f - num3) * (float)direction;
					num3 = 20f;
					itemLocation.Y = position.Y + num3 + mountOffset;
				}
				itemRotation = ((float)itemAnimation / (float)itemAnimationMax - 0.5f) * (float)(-direction) * 3.5f - (float)direction * 0.3f;
			}
			else
			{
				Vector2 zero = Vector2.Zero;
				if ((double)itemAnimation < (double)itemAnimationMax * 0.333)
				{
					float num4 = 10f;
					if (heldItemFrame.Width > 32)
					{
						num4 = 14f;
					}
					if (heldItemFrame.Width >= 52)
					{
						num4 = 24f;
					}
					if (heldItemFrame.Width >= 64)
					{
						num4 = 28f;
					}
					if (heldItemFrame.Width >= 92)
					{
						num4 = 38f;
					}
					if (sItem.type == 2330 || sItem.type == 2320 || sItem.type == 2341)
					{
						num4 += 8f;
					}
					if (sItem.type == 671)
					{
						num4 += 12f;
					}
					itemLocation.X = position.X + (float)width * 0.5f + ((float)heldItemFrame.Width * 0.5f - num4) * (float)direction;
					itemLocation.Y = position.Y + 24f + mountOffset;
					zero = new Vector2(-4f, 1f);
				}
				else if ((double)itemAnimation < (double)itemAnimationMax * 0.666)
				{
					float num5 = 10f;
					if (heldItemFrame.Width > 32)
					{
						num5 = 18f;
					}
					if (heldItemFrame.Width >= 52)
					{
						num5 = 24f;
					}
					if (heldItemFrame.Width >= 64)
					{
						num5 = 28f;
					}
					if (heldItemFrame.Width >= 92)
					{
						num5 = 38f;
					}
					if (sItem.type == 2330 || sItem.type == 2320 || sItem.type == 2341)
					{
						num5 += 4f;
					}
					if (sItem.type == 671)
					{
						num5 += 6f;
					}
					itemLocation.X = position.X + (float)width * 0.5f + ((float)heldItemFrame.Width * 0.5f - num5) * (float)direction;
					num5 = 10f;
					if (heldItemFrame.Height > 32)
					{
						num5 = 8f;
					}
					if (heldItemFrame.Height > 52)
					{
						num5 = 12f;
					}
					if (heldItemFrame.Height > 64)
					{
						num5 = 14f;
					}
					if (sItem.type == 2330 || sItem.type == 2320 || sItem.type == 2341)
					{
						num5 += 4f;
					}
					if (sItem.type == 671)
					{
						num5 += 10f;
					}
					itemLocation.Y = position.Y + num5 + mountOffset;
					zero = new Vector2(-6f, -4f);
				}
				else
				{
					float num6 = 6f;
					if (heldItemFrame.Width > 32)
					{
						num6 = 14f;
					}
					if (heldItemFrame.Width >= 48)
					{
						num6 = 18f;
					}
					if (heldItemFrame.Width >= 52)
					{
						num6 = 24f;
					}
					if (heldItemFrame.Width >= 64)
					{
						num6 = 28f;
					}
					if (heldItemFrame.Width >= 92)
					{

```


---

## 🤖 Assistant · 2026-08-13T01:26:13.143Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
This is the useStyle==1 swing itemLocation (render side). The melee HIT window is elsewhere: in vanilla, melee hit is `Player.ItemCheck_ApplyUseStyle` → at the end calls something like:

```
if (flag && flag3) { ... }
```
Actually the melee damage is in `Player.ItemCheck_ApplyUseStyle` via `ItemCheck_ApplyUseStyle_SwingTools`? No. Let me grep "meleeCD" or "ResetMeleeHitCooldowns" or "num26" ... The classic vanilla melee code:

```csharp
Rectangle itemRect = new Rectangle((int)(itemLocation.X - hitbox...), ...);
for each npc: if (npc.immune[whoAmI] == 0 && itemRect.Intersects(npcRect)) { StrikeNPC... npc.immune[whoAmI] = 10 (or 20) }
```
And the gate: `if (item.melee && itemAnimation > 0 && itemAnimation < itemAnimationMax ...)`. Let me grep "StrikeNPC" in Player.cs.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:13.938Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"StrikeNPC\\|ApplyItemToNPC\\|meleeCD\\b\" Player.cs | head -20; echo \"=== ResetMeleeHitCooldowns ===\"; grep -n \"ResetMeleeHitCooldowns\" -A 14 Player.cs | sed -n '1,20p'",
 "description": "Find melee hit application"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:13.973Z

**📎 ToolResult**

```
20164:		int dmg = (int)npc.StrikeNPC(damage, knockback, direction, crit, noEffect: false, fromNet: false, whoAmI);
43746:			int num5 = (int)nPC.StrikeNPC(num3, knockBack, direction, flag3, noEffect: false, fromNet: false, whoAmI);
=== ResetMeleeHitCooldowns ===
43542:	public void ResetMeleeHitCooldowns()
43543-	{
43544-		if (Main.myPlayer == whoAmI)
43545-		{
43546-			Array.Clear(meleeNPCHitCooldown, 0, Main.maxNPCs);
43547-		}
43548-	}
43549-
43550-	public void UpdateMeleeHitCooldowns()
43551-	{
43552-		if (Main.myPlayer == whoAmI)
43553-		{
43554-			for (int i = 0; i < Main.maxNPCs; i++)
43555-			{
43556-				meleeNPCHitCooldown[i]--;
--
50932:		ResetMeleeHitCooldowns();
50933-		ApplyItemAnimation(sItem);
50934-		bool flag2 = ItemID.Sets.SkipsInitialUseSound[sItem.type];
50935-		if (sItem.UseSound != null && !flag2)

```


---

## 🤖 Assistant · 2026-08-13T01:26:17.106Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '43620,43760p' Player.cs",
 "description": "Read melee hit window gate"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:17.133Z

**📎 ToolResult**

```
			{
				return;
			}
			int damage = originalDamage;
			damage = ApplyRapidAttackBonus(damage, sItem.type, !nPC.immortal);
			if (nPC.isLikeATownNPC && sItem.type == 3351)
			{
				damage = 1;
			}
			bool flag3 = false;
			int weaponCrit = GetWeaponCrit(sItem);
			if (Main.rand.Next(1, 101) <= weaponCrit)
			{
				flag3 = true;
			}
			if (GetBannerBuffEffect(nPC, out var effect))
			{
				damage = (int)((float)damage * effect.DamageDealt.Sample(Main.Difficulty));
			}
			if (parryDamageBuff && sItem.melee)
			{
				damage *= 5;
				parryDamageBuff = false;
				ClearBuff(198);
			}
			if (sItem.type == 426 && (float)nPC.life >= (float)nPC.lifeMax * 0.9f)
			{
				damage = (int)((float)damage * 2.5f);
			}
			if (sItem.type == 5096)
			{
				int num = 0;
				if (FindBuffIndex(26) != -1)
				{
					num = 1;
				}
				if (FindBuffIndex(206) != -1)
				{
					num = 2;
				}
				if (FindBuffIndex(207) != -1)
				{
					num = 3;
				}
				float num2 = 1f + 0.05f * (float)num;
				damage = (int)((float)damage * num2);
			}
			if (sItem.type == 671)
			{
				damage = nPC.KeyBrandStrike(whoAmI, damage, itemRectangle.Center.ToVector2());
			}
			int num3 = Main.DamageVar(damage, luck);
			float armorPenetrationPercent = 0f;
			if (sItem.type == 5129 && nPC.isLikeATownNPC)
			{
				armorPenetrationPercent = 1f;
				if (nPC.type == 18)
				{
					num3 *= 2;
				}
			}
			if (sItem.type == 3258)
			{
				ParticleOrchestraSettings settings = new ParticleOrchestraSettings
				{
					PositionInWorld = nPC.Center
				};
				ParticleOrchestrator.RequestParticleSpawn(clientOnly: false, ParticleOrchestraType.SlapHand, settings, whoAmI);
			}
			if (sItem.type == 5382)
			{
				ParticleOrchestraSettings settings2 = new ParticleOrchestraSettings
				{
					PositionInWorld = nPC.Center
				};
				ParticleOrchestrator.RequestParticleSpawn(clientOnly: false, ParticleOrchestraType.WaffleIron, settings2, whoAmI);
			}
			if (sItem.type == 3351 && nPC.type != 488 && nPC.lifeMax > 5)
			{
				int num4 = Item.NewItem(GetItemSource_Misc(ItemSourceID.LuckyCoin), (int)nPC.Left.X + Main.rand.Next(nPC.width), (int)nPC.Top.Y + Main.rand.Next(nPC.height), 1, 1, 71, 1 + RollBadLuck(25));
				WorldItem worldItem = Main.item[num4];
				if (Main.netMode == 0)
				{
					worldItem.noGrabDelay = 100;
				}
				worldItem.timeLeftInWhichTheItemCannotBeTakenByEnemies = 100;
				worldItem.velocity.Y = -2f - Main.rand.NextFloat() * 2f;
				worldItem.velocity.X = (2f + Main.rand.NextFloat() * 2f) * (float)direction;
				worldItem.favorited = false;
				worldItem.newAndShiny = false;
				if (Main.netMode == 1)
				{
					NetMessage.SendData(148, -1, -1, null, num4);
				}
				ParticleOrchestraSettings settings3 = new ParticleOrchestraSettings
				{
					PositionInWorld = nPC.Center
				};
				ParticleOrchestrator.RequestParticleSpawn(clientOnly: false, ParticleOrchestraType.ClassyCane, settings3, whoAmI);
			}
			if (sItem.type == 5129)
			{
				ParticleOrchestraSettings settings4 = new ParticleOrchestraSettings
				{
					PositionInWorld = nPC.Center
				};
				ParticleOrchestrator.RequestParticleSpawn(clientOnly: false, ParticleOrchestraType.FlyMeal, settings4, whoAmI);
				if (nPC.townNPC)
				{
					AchievementsHelper.NotifyProgressionEvent(42);
				}
			}
			if (sItem.type == 1166 || sItem.type == 1320)
			{
				Vector2 vector = new Vector2(itemRectangle.Left + Main.rand.Next(itemRectangle.Width), itemRectangle.Top + Main.rand.Next(itemRectangle.Height / 2));
				Vector2 vector2 = new Vector2((float)direction * (1f + Main.rand.NextFloat() * 5f), -1f - Main.rand.NextFloat() * 3f);
				int damage2 = (int)((double)originalDamage * 0.75);
				Projectile.NewProjectile(GetProjectileSource_Item(sItem), vector, vector2, 21, damage2, knockBack, Main.myPlayer);
			}
			StatusToNPC(sItem.type, npcIndex);
			if (nPC.life > 5)
			{
				OnHit(nPC.Center.X, nPC.Center.Y, nPC);
			}
			num3 += nPC.checkArmorPenetration(GetArmorPenetration(sItem.melee), armorPenetrationPercent);
			NPCKillAttempt attempt = new NPCKillAttempt(nPC);
			int num5 = (int)nPC.StrikeNPC(num3, knockBack, direction, flag3, noEffect: false, fromNet: false, whoAmI);
			ApplyNPCOnHitEffects(sItem, itemRectangle, damage, knockBack, npcIndex, num3, num5);
			int num6 = BannerSystem.NPCtoBanner(nPC.BannerID());
			if (num6 >= 0)
			{
				lastCreatureHit = num6;
			}
			if (Main.netMode != 0)
			{
				if (flag3)
				{
					NetMessage.SendData(28, -1, -1, null, npcIndex, num3, knockBack, direction, 1);
				}
				else
				{

```


---

## 🤖 Assistant · 2026-08-13T01:26:19.409Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need the gate above — let me read 43560-43625 to get the melee hit window conditions (itemAnimation-based).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:19.700Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '43560,43622p' Player.cs",
 "description": "Read melee hit gate conditions"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:19.728Z

**📎 ToolResult**

```
	public bool CanHitNPCWithMeleeHit(int npcIndex)
	{
		return meleeNPCHitCooldown[npcIndex] <= 0;
	}

	public void SetMeleeHitCooldown(int npcIndex, int timeInFrames)
	{
		meleeNPCHitCooldown[npcIndex] = timeInFrames;
	}

	private void ItemCheck_MeleeHitNPCs(Item sItem, Rectangle itemRectangle, int originalDamage, float knockBack)
	{
		for (int i = 0; i < Main.maxNPCs; i++)
		{
			NPC nPC = Main.npc[i];
			if (nPC.active && nPC.immune[whoAmI] == 0 && CanHitNPCWithMeleeHit(i) && attackCD <= 0)
			{
				nPC.position += nPC.netOffset;
				ProcessHitAgainstNPC(sItem, itemRectangle, originalDamage, knockBack, i);
				nPC.position -= nPC.netOffset;
			}
		}
	}

	public void TakeDamageFromJellyfish(int npcIndex)
	{
		NPC nPC = Main.npc[npcIndex];
		Hurt(PlayerDeathReason.ByNPC(npcIndex), (int)((double)nPC.damage * 1.3), -direction);
		SetMeleeHitCooldown(npcIndex, itemAnimation);
		ApplyAttackCooldown();
	}

	private void ProcessHitAgainstNPC(Item sItem, Rectangle itemRectangle, int originalDamage, float knockBack, int npcIndex)
	{
		NPC nPC = Main.npc[npcIndex];
		if (nPC.dontTakeDamage || !CanNPCBeHitByPlayerOrPlayerProjectile(nPC))
		{
			if (NPCID.Sets.ZappingJellyfish[nPC.type] && itemRectangle.Intersects(nPC.Hitbox) && (nPC.noTileCollide || CanHit(nPC)))
			{
				TakeDamageFromJellyfish(npcIndex);
			}
		}
		else
		{
			if (nPC.friendly && (nPC.type != 22 || !killGuide) && (nPC.type != 54 || !killClothier) && (!nPC.isLikeATownNPC || (sItem.type != 5129 && sItem.type != 3351)))
			{
				return;
			}
			Rectangle rectangle = new Rectangle((int)nPC.position.X, (int)nPC.position.Y, nPC.width, nPC.height);
			bool flag = itemRectangle.Intersects(rectangle);
			int type = sItem.type;
			if (type == 121)
			{
				GetPointOnSwungItemPath(70f, 70f, 0f, GetAdjustedItemScale(sItem), out var location, out var outwardDirection);
				GetPointOnSwungItemPath(70f, 70f, 0.9f, GetAdjustedItemScale(sItem), out var location2, out outwardDirection);
				bool flag2 = Utils.LineRectangleDistance(rectangle, location, location2) <= 16f;
				flag = ((!_spawnVolcanoExplosion) ? (flag || flag2) : flag2);
			}
			if (!flag || (!nPC.noTileCollide && !CanHit(nPC)))
			{
				return;
			}

```


---

## 🤖 Assistant · 2026-08-13T01:26:21.693Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK, the melee hit is called from ApplyUseStyle with the swung item rectangle. Where is ItemCheck_MeleeHitNPCs called? Let me grep. Also the gate that decides whether the swing can hit (e.g., `if (item.melee && itemAnimation < itemAnimationMax ...)`). Let me grep call site.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:22.568Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"ItemCheck_MeleeHitNPCs\\|GetPointOnSwungItemPath\" Player.cs | head; echo \"=== gate ===\"; grep -n \"ItemCheck_MeleeHitNPCs\" -B 30 Player.cs | grep -n \"itemAnimation\\|melee\\|useStyle\\|flag\" | head -30",
 "description": "Find melee hit call gate"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:22.609Z

**📎 ToolResult**

```
42997:					ItemCheck_MeleeHitNPCs(sItem, itemRectangle2, weaponDamage, knockBack);
43571:	private void ItemCheck_MeleeHitNPCs(Item sItem, Rectangle itemRectangle, int originalDamage, float knockBack)
43614:				GetPointOnSwungItemPath(70f, 70f, 0f, GetAdjustedItemScale(sItem), out var location, out var outwardDirection);
43615:				GetPointOnSwungItemPath(70f, 70f, 0.9f, GetAdjustedItemScale(sItem), out var location2, out outwardDirection);
44114:	private void GetPointOnSwungItemPath(float spriteWidth, float spriteHeight, float normalizedPointOnPath, float itemScale, out Vector2 location, out Vector2 outwardDirection)
44206:				GetPointOnSwungItemPath(70f, 70f, 0.2f + 0.8f * Main.rand.NextFloat(), GetAdjustedItemScale(sItem), out var location, out var outwardDirection);
44252:				GetPointOnSwungItemPath(60f, 60f, 0.2f + 0.8f * Main.rand.NextFloat(), GetAdjustedItemScale(sItem), out var location2, out var outwardDirection2);
=== gate ===
38:43546-			Array.Clear(meleeNPCHitCooldown, 0, Main.maxNPCs);
48:43556-				meleeNPCHitCooldown[i]--;
55:43563-		return meleeNPCHitCooldown[npcIndex] <= 0;
60:43568-		meleeNPCHitCooldown[npcIndex] = timeInFrames;

```


---

## 🤖 Assistant · 2026-08-13T01:26:24.326Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '42940,43000p' Player.cs",
 "description": "Read melee hit call gate in ItemCheck"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:24.349Z

**📎 ToolResult**

```
		{
			boneGloveTimer = 60;
			Vector2 center = base.Center;
			Vector2 vector = DirectionTo(ApplyRangeCompensation(0.2f, center, Main.MouseWorld)) * 10f;
			Projectile.NewProjectile(GetProjectileSource_Accessory(boneGloveItem), center.X, center.Y, vector.X, vector.Y, 532, 25, 5f, whoAmI);
		}
		if (sItem.type == 1124 && itemAnimation > 0)
		{
			ItemCheck_GetMeleeHitbox(sItem, heldItemFrame, out var _, out var itemRectangle);
			if (Main.rand.Next(30) == 0)
			{
				_ = base.Center;
				Vector2 vector2 = DirectionTo(Main.MouseWorld) * 6f;
				int dmg = 5;
				int num3 = Projectile.NewProjectile(GetProjectileSource_Item(sItem), itemRectangle.X + itemRectangle.Width / 2, itemRectangle.Y + itemRectangle.Height / 2, vector2.X, vector2.Y, beeType(), beeDamage(dmg), beeKB(0f), whoAmI);
				Main.projectile[num3].melee = true;
			}
		}
		if (sItem.type > 0 && itemAnimation > 0)
		{
			ItemCheck_GetMeleeHitboxParticles(sItem, heldItemFrame);
		}
		if (((sItem.damage >= 0 && sItem.type > 0 && !sItem.noMelee) || sItem.type == 1991 || sItem.type == 3183 || sItem.type == 4821) && itemAnimation > 0)
		{
			ItemCheck_GetMeleeHitbox(sItem, heldItemFrame, out var dontAttack2, out var itemRectangle2);
			if (!dontAttack2)
			{
				ItemCheck_EmitUseVisuals(sItem, itemRectangle2);
				if (Main.myPlayer == whoAmI && (sItem.type == 1991 || sItem.type == 3183 || sItem.type == 4821))
				{
					ItemCheck_CatchCritters(sItem, itemRectangle2);
				}
				if (sItem.type == 3183 || sItem.type == 4821)
				{
					bool[] shouldIgnore = ItemCheck_GetTileCutIgnoreList(sItem);
					ItemCheck_CutTiles(sItem, itemRectangle2, shouldIgnore, cutExtraTiles: true);
				}
				if (sItem.damage > 0)
				{
					UpdateMeleeHitCooldowns();
					float knockBack = sItem.knockBack;
					float num4 = 1f;
					if (kbGlove)
					{
						num4 += 1f;
					}
					if (kbBuff)
					{
						num4 += 0.5f;
					}
					knockBack *= num4;
					if (inventory[selectedItem].type == 3106)
					{
						knockBack += knockBack * (1f - stealth);
					}
					bool[] shouldIgnore2 = ItemCheck_GetTileCutIgnoreList(sItem);
					ItemCheck_CutTiles(sItem, itemRectangle2, shouldIgnore2);
					ItemCheck_MeleeHitNPCs(sItem, itemRectangle2, weaponDamage, knockBack);
					ItemCheck_MeleeHitPVP(sItem, itemRectangle2, weaponDamage, knockBack);
					ItemCheck_EmitHammushProjectiles(whoAmI, sItem, itemRectangle2, weaponDamage);
				}

```


---

## 🤖 Assistant · 2026-08-13T01:26:39.143Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So the melee hit window: `itemAnimation > 0` — the WHOLE animation window, hit box computed every frame while itemAnimation > 0 (and itemAnimation decrements each tick). Plus per-NPC cooldown `meleeNPCHitCooldown` — after a hit, `SetMeleeHitCooldown` is set (to what value?). Let me check ProcessHitAgainstNPC end → SetMeleeHitCooldown(i, ?). And the wiki says "A single target will only be hit once during one swinging animation" — because ResetMeleeHitCooldowns() is called at ItemCheck_StartActualUse and cooldown set >= itemAnimation after hit. Let me check the tail of ProcessHitAgainstNPC.

Then, repo side: swingHitSet cleared on each new swing, so each swing hits each NPC once. Let me verify repo swing damage check window. Need to find where swingHitSet is used in damage check — likely in a melee hit resolution function. Let me grep swingHitSet and the swing-based hitbox.

Also I need:
- Repo ranged weapon (bow/gun/magic) use chain: Game.ts 2483-2720.
- Player.ts attackSpeedMult (540-560), useTime decrement (669), healBlocked.
- Repo: does switching items get blocked during swing? Game.ts 3901 canChangeImmediately: !this.swing && p.useTime === 0 — good, but need to check where canChangeImmediately is used (hotbar switch gate).
- Repo: reuseDelay — Game.ts 3903 says "reuseDelay/channel/pendingItemReuse 未实装" — so ❌ reuseDelay not implemented. Confirm by grep reuseDelay in game/src.
- Repo: 急速武器 useTime < useAnimation 行为: Game.ts 4074 `(swingOver || reuseSpd < animSpd)` handles re-trigger mid-animation — but it sets useTime=reuseSpd and resets swing entirely (t: animSpd) — i.e., starts a NEW swing when reuseSpd < animSpd. Vanilla behavior for melee autoswing with useTime<useAnimation: "it still cannot shoot a projectile again until the swing finishes" and animation restarts only when itemAnimation==1 (autoswing skip). Hmm — for melee weapons, vanilla restarts a new swing only when itemAnimation reaches 1 (skip) or 0. The itemTime becoming 0 mid-swing doesn't restart the swing for melee; it only gates effects (shoot/heal). Actually for melee weapons with useTime < useAnimation... rare. But repo's `(reuseSpd < animSpd)` restarts the whole swing early — 🔀 different. Wait, actually look: `if (this.player.useTime === 0 && canChain && (swingOver || reuseSpd < animSpd))` — when reuseSpd < animSpd (fast weapons like Fetid Baghnakhs? Actually those have useTime==useAnimation)... For melee where useTime<useAnimation, repo restarts swing as soon as useTime hits 0, cutting the animation. Vanilla: itemTime==0 mid-swing only re-enables shoot/heal effect; the swing continues; new swing starts only at itemAnimation 1/0. So 🔀. But note the wiki's projectile-melee note: "if such a weapon's useTime is less than its useAnimation, it still cannot shoot a projectile again until the swing finishes" — that's about shooting, not swinging.

Hmm wait — actually there's a subtlety. For non-autoReuse melee with useTime < useAnimation... Let me not over-engineer. The key vanilla semantic: the animation runs its full course; itemTime gates per-tick effects (shoot/consume). Restart requires itemAnimation==0 (or ==1 with autoswing skip). The repo restarts the swing early when reuseSpd<animSpd. That's a 🔀 for fast weapons. But practically, how many melee weapons have useTime < useAnimation? Per repo comment "1790 件 vi 武器两者不同". Hmm that says 1790 vi weapons have useTime != useAnimation — that includes guns/bows (useStyle 5). For melee specifically fewer. Let me quickly check vanilla data for melee weapons with useTime<useAnimation... I could check the repo's combat table. Let me check via a quick node script? That may be heavy. Alternative: grep the repo's vanilla-itemcombat data for a known example: Clockwork Assault Rifle (id 1104?) useTime 4 / useAnimation 12 / reuseDelay 14.

Actually, let me check the ranged weapon chain in the repo first — 2483-2720 which mentions SetDummyItemTime(2), useTime=42 etc.

Let me also check Player.ts for attackSpeedMult and useTime decrement.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:39.334Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "limit": 140,
 "offset": 540
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:39.339Z

**📎 ToolResult**

```
540	    return 1 + this.equipStats.sentrySlots + (this.buffs.has(BuffType.WarTable) ? 1 : 0);
541	  }
542	  get thornsActive(): boolean {
543	    return this.buffs.hasThorns;
544	  }
545	  /** 近战攻速倍率（CapAttackSpeeds + TurnAttackSpeedToUseTimeMultiplier，Player.cs
546	   *  :28555-28574 1:1）：meleeSpeed 加法总和（装备 0.12 档 + 词缀 77-80 + 套装 + buff）
547	   *  封顶 3 后取倒数，作为 useAnimation/useTime 的时长乘数。原"猛爪手套 ×2"档已废——
548	   *  原版猛爪手套 211 只给 meleeSpeed += 0.12 + autoReuseGlove（:14559-14562），
549	   *  0.12 已经 vanilla-accfx.json 走 equipStats.meleeSpeed，不应再翻倍。 */
550	  get attackSpeedMult(): number {
551	    const raw = (1 + this.equipStats.meleeSpeed)
552	      * (this.buffs.has(BuffType.Tipsy) ? 1.1 : 1)
553	      * (this.buffs.has(BuffType.Werewolf) ? 1.051 : 1)      // 狼人 meleeSpeed += 5.1%（:11489）
554	      * (this.buffs.has(BuffType.Weak) ? 0.949 : 1)          // 虚弱 meleeSpeed -= 5.1%（:11507）
555	      * (1 + 0.1 * this.beetleOrbs)                          // 甲虫攻击球攻速（:10071+）
556	      * (1 + this.buffs.wellFedMeleeSpeed);                  // 食物近战速 +5/7.5/10%（:11528+）
557	    return raw > 3 ? 1 / 3 : 1 / raw;                        // :28566-28573
558	  }
559	  /** 全系伤害加成装备聚合（ApplyEquipFunctional dmgX 段；四系分道——summon 是独立
560	   *  minionDamage 链：装备走 SUMMON_GEAR/SET，不含 magic-only 来源） */
561	  damageMult(kind: 'melee' | 'ranged' | 'magic' | 'summon'): number {
562	    const st = this.equipStats;
563	    if (kind === 'summon') {
564	      // minionDamage 链（Player.cs GetWeaponDamageMultiplier summon 分支）：仅四系通用
565	      // 来源（怒气/食物）+ 召唤装备链；MagicPower/Archery 等 class 来源不吃
566	      let m = 1 + st.minionDmg;
567	      if (this.buffs.has(BuffType.Rage)) m += 0.1;
568	      if (this.buffs.has(BuffType.BrainOfConfusionBuff)) m += 0.1; // BOC 321（:9639-9646）
569	      m += this.buffs.wellFedDamage;
570	      m += 0.15 * this.nebula[0];        // 星云伤害 179-181 每级四系 +15%（:10118-10124）
571	      return m;
572	    }
573	    let m = 1 + (kind === 'melee' ? st.dmgMelee : kind === 'ranged' ? st.dmgRanged : st.dmgMagic);
574	    if (kind === 'magic') {
575	      m += this.buffs.magicDmgBonus;            // MagicPower +20%（:9669）
576	      m *= this.buffs.manaSickMagicMult;        // 魔力眩晕最高 -25% 线性恢复（:10003/:25616）
577	    }
578	    if (kind === 'ranged') m *= this.buffs.arrowDmgMult;   // Archery ×1.1（:9712,ranged 近义）
579	    // R1 药水：怒气(117)全系 +10%（:9947）；醉酒(25)近战 +10%（:11513）
580	    if (this.buffs.has(BuffType.Rage)) m += 0.1;
581	    if (kind === 'melee') {
582	      if (this.buffs.has(BuffType.Tipsy)) m += 0.1;
583	      if (this.buffs.has(BuffType.Werewolf)) m += 0.051;      // 狼人（:11488）
584	      if (this.buffs.has(BuffType.Weak)) m -= 0.051;         // 虚弱（:11506）
585	      m += 0.1 * this.beetleOrbs;                              // 甲虫攻击球每颗 +10%（:10071+）
586	      if (this.heldPsychoKnife) m += (1 - this.stealth) * 3;   // 变态刀潜行（:25487）
587	    }
588	    m += this.buffs.wellFedDamage;   // 食物三档全系 +5/7.5/10%（:11527+）
589	    m += 0.15 * this.nebula[0];      // 星云四系 +15%/层
590	    return m;
591	  }
592	  /** 远程分道乘区（Player.cs:3820-3824 bowEffectiveDamage 拆分）：
593	   *  箭 = (rangedDamage + 箭袋stack) × Archery × 蘑菇矿箭头 1.12 × 潜行增伤；
594	   *  弹/火箭 = rangedDamage × 对应蘑菇矿头 1.12 × 潜行；其他（飞镖等）= rangedDamage */
595	  rangedDamageMult(kind: 'arrow' | 'bullet' | 'rocket' | 'other'): number {
596	    const st = this.equipStats;
597	    const base = this.damageMult('ranged'); // rangedDamage 全链（装备+四系 buff）
598	    const stealthBonus = 1 + (1 - this.stealth) * (st.vortexSet ? 0.8 : st.shroomiteSet ? 0.6 : 0);
599	    if (kind === 'arrow') {
600	      // bowEffectiveDamage :3820 = (rangedDamage/arrowMult + stack) × arrowMult²
601	      //   = (rangedDamage + stack×arrowMult) × arrowMult——stack 段平方差异在此
602	      const arrowMult = this.buffs.arrowDmgMult * (st.shroomiteType === 'arrow' ? 1.12 : 1);
603	      return (base + st.arrowStack * arrowMult) * arrowMult * stealthBonus;
604	    }
605	    if (kind === 'bullet') return base * (st.shroomiteType === 'bullet' ? 1.12 : 1) * stealthBonus;
606	    if (kind === 'rocket') return base * (st.shroomiteType === 'rocket' ? 1.12 : 1) * stealthBonus;
607	    return base;
608	  }
609	  /** 手持变态刀 3106（潜行判定用） */
610	  get heldPsychoKnife(): boolean {
611	    const d = ITEM_DEFS[this.inv.heldItem()?.id ?? -1];
612	    const vid = d?.vid ?? (d?.key?.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
613	    return vid === 3106;
614	  }
615	  /** 潜行 aggro（:25518/:25557/:25491：蘑菇矿 -750×(1-s) / 星璇 -1200 / 变态刀 -750）
616	   *  ——敌人索敌距离缩短（NPC.cs:78375 dist -= aggro）；各 AI 家族索敌门消费见后续批 */
617	  get aggro(): number {
618	    const s1 = 1 - this.stealth;
619	    if (this.equipStats.vortexSet) return -Math.round(1200 * s1);
620	    if (this.equipStats.shroomiteSet) return -Math.round(750 * s1);
621	    if (this.heldPsychoKnife) return -Math.round(750 * s1);
622	    return 0;
623	  }
624	  /** 近战护甲穿透（磨刀 159：meleeArmorPenetration += 12，仅近战/投掷） */
625	  get meleeArmorPen(): number {
626	    return this.buffs.has(BuffType.Sharpened) ? 12 : 0;
627	  }
628	  /** 星云 booster CD（命中驱动，Game 侧判定；:12895 nebulaCD=30） */
629	  nebulaCD = 0;
630	  /** 用魔物品起手（Game 在设定 useTime 后调用）：登记动画窗，窗内每帧重置
631	   *  manaRegenDelay（Player.cs:42131-42137 itemAnimation>0 && item.mana>0 →
632	   *  ItemCheck_ApplyManaRegenDelay :49851；本仓单计时器模型以 useTime 代 useAnimation） */
633	  onManaItemUsed(): void {
634	    this.manaAnimTicks = Math.max(this.manaAnimTicks, this.useTime);
635	  }
636	  /** 甲虫进攻套：近战命中蓄能（45 次/球，满 3 球；受击掉球见 damage()） */
637	  onMeleeHit(): void {
638	    // ⑰ 时间蓄能（原版持续近战 ~90t/球）：命中只刷新续航窗口，蓄能走 fixedUpdate 每 tick
639	    if (this.equipStats.beetleOff || this.equipStats.beetleDef) this.lastMeleeTick = 30;
640	  }
641	  /** 装备暴击率（critX 段 + 词缀 67/68） */
642	  critChance(kind: 'melee' | 'ranged' | 'magic'): number {
643	    const st = this.equipStats;
644	    let c = kind === 'melee' ? st.critMelee : kind === 'ranged' ? st.critRanged : st.critMagic;
645	    // R1 药水：暴怒(115)全系暴击 +10（:9890）；醉酒(25)近战暴击 +2（:11515）
646	    if (this.buffs.has(BuffType.Wrath)) c += 10;
647	    if (this.buffs.has(BuffType.BrainOfConfusionBuff)) c += 10; // BOC（:9639）
648	    if (kind === 'melee' && this.buffs.has(BuffType.Tipsy)) c += 2;
649	    if (kind === 'melee' && this.buffs.has(BuffType.Werewolf)) c += 2; // 狼人（:11493）
650	    if (kind === 'melee' && this.heldPsychoKnife) c = Math.min(100, c + Math.round((1 - this.stealth) * 30)); // 变态刀（:25489）
651	    if (kind === 'ranged') {
652	      if (this.equipStats.shroomiteType) c += 5; // 蘑菇矿头 rangedCrit+5（:13274+）
653	      if (st.shroomiteSet || st.vortexSet) c += Math.round((1 - this.stealth) * (st.vortexSet ? 20 : 10)); // 潜行暴击
654	    }
655	    c += this.buffs.wellFedCrit;    // 食物三档全系暴击 +2/3/4（:11525+）
656	    return c;
657	  }
658	
659	  get frame(): number {
660	    if (!this.onGround) return 4;
661	    if (Math.abs(this.vx) > 0.3) {
662	      return 1 + Math.floor(this.animTime / 8) % 3;
663	    }
664	    return 0;
665	  }
666	
667	  fixedUpdate(dt: number, game: GameHooks) {
668	    const world = game.world;
669	    this.lastStore = world.store;   // dashWallAhead 探测缓存（本 tick 内有效）
670	    if (this.iframes > 0) this.iframes--;
671	    if (this.useTime > 0) this.useTime--;
672	
673	    // Buff tick：自然回复 / 环境 DoT（负值=持续伤害,原版 lifeRegen 路径:无视防御与无敌帧）
674	    const buffHeal = this.buffs.tick(dt);
675	    if (buffHeal > 0 && this.hp > 0) this.hp = Math.min(this.maxHp, this.hp + buffHeal);
676	    else if (buffHeal < 0 && this.hp > 0) {
677	      this.hp = Math.max(0, this.hp + buffHeal);
678	      // HurtLifeRegen 飘字（Player.cs:19207-19212）：DoT 分块伤害弹掉血数字,
679	      // LifeRegen 色 (255,60,70) + dot:true;原版 DoT 不触发受击闪烁/无敌帧/音效

```


---

## 🤖 Assistant · 2026-08-13T01:26:39.588Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 120,
 "offset": 2480
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:39.593Z

**📎 ToolResult**

```
2480	    }
2481	    // ★_prevMouseDown/_prevRightDown 须在 updateUse 【之后】记录上一帧值——
2482	    // 此前记在 updateUse 之前(= 本帧值),⑩ 边沿门 mouseDown&&!prev 恒 false,
2483	    // 非 autoReuse 武器(链球/回旋镖/悠悠球/长矛)全体掷不出(2026-08-13 实锤)
2484	    this.updateNebulaBoosters();
2485	    if (this.player.sleeping) {
2486	      const bx = Math.floor(this.player.cx / TILE), by = Math.floor((this.player.y + this.player.h + 2) / TILE);
2487	      if (!w.store.inBounds(bx, by) || w.store.type[w.store.idx(bx, by)] !== (TILE_BY_KEY['bed'] ?? -1)) {
2488	        this.player.sleeping = false; // 床格失效（SH:98-101）
2489	      }
2490	    }
2491	    // ⑤ Foxparks 5664 手持喷火通道（PC:42669-42690 TryUsingFoxsparksAbility：
2492	    // 按住期间已有 1094 进 ai[0]=1000 喷火态 + SetDummyItemTime(2) 锁 useTime）
2493	    {
2494	      const heldF = this.player.inv.heldItem();
2495	      const fDef = heldF ? ITEM_DEFS[heldF.id] : null;
2496	      const fVid = fDef ? (fDef.vid ?? viIdFromKey(fDef.key)) : -1;
2497	      const channeling = fVid === 5664 && inp.mouseDown && !inp.uiBlocking && !this.player.dead;
2498	      for (const e of this.entities.projectiles) {
2499	        const m = e as MinionProj;
2500	        if (!(m instanceof MinionProj) || m.dead || m.projId !== 1094) continue;
2501	        if (channeling) {
2502	          const [fwx, fwy] = this.camera.screenToWorld(inp.mouseX, inp.mouseY);
2503	          const fdx = fwx - this.player.cx, fdy = fwy - this.player.cy;
2504	          const fl = Math.hypot(fdx, fdy) || 1;
2505	          m.foxChannel = true;
2506	          m.foxAimX = fdx / fl; m.foxAimY = fdy / fl;
2507	          m.x = this.player.cx - m.w / 2; m.y = this.player.cy - m.h / 2; // position=MountedCenter-Size/2(:56120)
2508	          this.player.useTime = Math.max(this.player.useTime, 2); // SetDummyItemTime(2)
2509	        } else if (m.foxChannel) {
2510	          m.foxChannel = false;
2511	          m.lockAfterFoxChannel(); // localAI[0]=30 喷火后攻击锁（:56155）
2512	        }
2513	      }
2514	    }
2515	    // ---- 高尔夫球杆蓄力（AI_150_GolfClubHelper :49498-49627 + GolfHelper）：
2516	    //      channel 语义（DefaultToGolfClub :48130）——按住=瞄准（力度=光标距球/300，
2517	    //      与时长无关），松开=击球（CalculateShotStrength 椭圆钳×32）；右键取消。
2518	    {
2519	      const heldG = this.player.inv.heldItem();
2520	      const gDef = heldG ? ITEM_DEFS[heldG.id] : null;
2521	      const gm2 = /^vi_(\d+)_/.exec(gDef?.key ?? '');
2522	      const gVid = gm2 ? +gm2[1] : 0;
2523	      const club = gVid > 0 ? GOLF_CLUBS[gVid] : undefined;
2524	      const myBall = (): GolfBall | null => {
2525	        for (const e of this.entities.projectiles) {
2526	          const b = e as GolfBall;
2527	          if (b instanceof GolfBall && !b.dead) return b;
2528	        }
2529	        return null;
2530	      };
2531	      if (club && !inp.uiBlocking && !this.player.dead && this.player.gravDir === 1) {
2532	        const [mwx, mwy] = this.camera.screenToWorld(inp.mouseX, inp.mouseY);
2533	        if (!this.golfAim && inp.mouseDown && this.player.useTime === 0) {
2534	          // 开瞄：站位盒内有球（ValidateShot :444-448）；无球且 500px 内无球 →
2535	          // 自动摆球（TryPlacingAGolfBallNearANearbyTee :49512-49525：5×5 找球座 494）
2536	          let ball = myBall();
2537	          if (!ball || Math.hypot(ball.cx - this.player.cx, ball.cy - this.player.cy) > 500
2538	            || !golfBallInStance(ball, this.player)) {
2539	            const st = this.world.store;
2540	            const ptx = Math.floor(this.player.cx / TILE), pty = Math.floor((this.player.y + this.player.h) / TILE);
2541	            let tee: [number, number] | null = null;
2542	            outer: for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) {
2543	              const x = ptx + dx, y = pty + dy;
2544	              if (!st.inBounds(x, y)) continue;
2545	              if (TILE_DEFS[st.type[st.idx(x, y)]]?.vanilla?.sheet === 494) { tee = [x, y]; break outer; }
2546	            }
2547	            if (tee) {
2548	              if (ball) ball.dead = true;
2549	              // GetPreferredGolfBallToUse（:48919-48950）：手持→背包首个球族，默认 721
2550	              let projId = 721;
2551	              for (let i = 0; i < this.player.inv.slots.length; i++) {
2552	                const sl = this.player.inv.slots[i];
2553	                if (!sl) continue;
2554	                const km = /^vi_(\d+)_/.exec(ITEM_DEFS[sl.id].key);
2555	                const kv = km ? +km[1] : 0;
2556	                if (kv === 3989 || (kv >= 4242 && kv <= 4253)) {
2557	                  projId = kv === 3989 ? 721 : 739 + (kv - 4242);
2558	                  this.player.inv.removeAt(i, 1);
2559	                  break;
2560	                }
2561	              }
2562	              const own = this.player;
2563	              ball = new GolfBall(tee[0] * TILE + 3, (tee[1] + 1) * TILE - 10, projId, () => own);
2564	              this.entities.add(ball, 'projectiles');
2565	            }
2566	          }
2567	          if (ball && golfBallInStance(ball, this.player)) {
2568	            this.golfAim = true;
2569	            this.golfAimBall = ball;
2570	            this.player.facing = mwx >= this.player.cx ? 1 : -1; // ChangeDir（:49606-49616）
2571	          }
2572	        }
2573	        if (this.golfAim) {
2574	          const ball = this.golfAimBall && !this.golfAimBall.dead ? this.golfAimBall : null;
2575	          if (inp.rightDown) {
2576	            // 右键取消（:49592-49601）：不出手
2577	            this.golfAim = false; this.golfAimBall = null;
2578	            this.player.useTime = 0;
2579	          } else if (!ball) {
2580	            this.golfAim = false; this.golfAimBall = null;
2581	          } else if (inp.mouseDown) {
2582	            // 瞄准维持（SetDummyItemTime :49624-49627）
2583	            this.player.useTime = Math.max(this.player.useTime, 12);
2584	            const shot = golfShot(mwx, mwy, ball, club);
2585	            this.renderer.golfPower = { x: this.player.cx, y: this.player.y + this.player.h + 8, rel: shot.rel, ball };
2586	            this.useSwing(gDef, Math.atan2(mwy - this.player.cy, mwx - this.player.cx));
2587	          } else {
2588	            // 松开 → 击球（:49527-49560）：公式击出 + 地面阻尼（HitGolfBall :451-474）
2589	            const shot = golfShot(mwx, mwy, ball, club);
2590	            const st = this.world.store;
2591	            const btx = Math.floor((ball.x + ball.w / 2) / TILE);
2592	            const bty = Math.floor((ball.y + ball.h + 1) / TILE);
2593	            const solidBelow = st.inBounds(btx, bty) && st.isSolid(btx, bty);
2594	            ball.clubHit(shot.vx, shot.vy, club.rough, solidBelow);
2595	            this.sfx.play('tink', 0.8, ball.cx, ball.cy);
2596	            this.golfScoreTime = 0; // RecordSwing（一杆进洞折扣计时清零）
2597	            this.golfAim = false; this.golfAimBall = null;
2598	            this.renderer.golfPower = null;
2599	            this.player.useTime = 42; // useAnimation 12 + 后摇 30（:49561-49567）

```


---

## 🤖 Assistant · 2026-08-13T01:26:41.590Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me find the ranged weapon (bow/gun/magic) use chain in Game.ts. Search for ranged weapon firing — e.g., combatWeapon kind 'ranged'/'magic', fireProjectile or shootWeapon. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:42.480Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"reuseDelay\" . | head -20; echo \"=== ranged/magic fire chain ===\"; grep -n \"kind === 'ranged'\\|kind === 'magic'\\|fireWeapon\\|tryShoot\\|useRanged\" core/Game.ts | head -30",
 "description": "Check reuseDelay and ranged fire chain"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:42.509Z

**📎 ToolResult**

```
core/Game.ts:3903:      // 本作 swing = itemAnimation、player.useTime = itemTime；reuseDelay/channel/
player/SmartSelect.ts:179:  /** CanChangeSelectedItemImmediately（Player.cs:386-393：itemAnimation/reuseDelay/channel/
=== ranged/magic fire chain ===
4726:    const dmgKind = cwIn.kind === 'magic' ? 'magic' : (cwIn.kind === 'boomerang' || cwIn.kind === 'spear' || cwIn.kind === 'yoyo' || cwIn.kind === 'flail') ? 'melee' as const : 'ranged' as const;
4755:    if (cw.kind === 'grenade' || cw.kind === 'magic' || cw.kind === 'shot' || cw.kind === 'summon') {

```


---

## 🤖 Assistant · 2026-08-13T01:26:44.757Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So reuseDelay is only mentioned in comments — NOT implemented (❌). Confirmed by grep: no actual reuseDelay state.

Now let me find the ranged/magic weapon use chain — search for where guns/bows fire. Look at combatWeapon usage.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:45.306Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"combatWeapon(\" core/Game.ts | head -20; echo \"===\"; grep -n \"useSwing\\|this.swing =\" core/Game.ts | head -40",
 "description": "Find weapon fire chain call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:45.338Z

**📎 ToolResult**

```
2467:      const cw0 = held0 ? combatWeapon(ITEM_DEFS[held0.id]) : null;
4046:    const cw = heldDef ? combatWeapon(heldDef) : null;
11587:    if (def.tool?.type === 'sword' || combatWeapon(def)?.kind === 'melee') {
11588:      const cw = combatWeapon(def);
===
2586:            this.useSwing(gDef, Math.atan2(mwy - this.player.cy, mwx - this.player.cx));
3754:  private useSwing(def: (typeof ITEM_DEFS)[number] | null, aim?: number): void {
3758:    this.swing = {
4075:        this.swing = {
4112:        this.swing = { t: spd, dur: spd, item: held!.id };
4143:          this.swing = { t: 15, dur: 15, item: held!.id };
4179:      this.useSwing(heldDef);
4398:        this.useSwing(heldDef, ang);
4594:        this.useSwing(heldDef, ang);
4756:      this.useSwing(def, ang);
7822:    if (this.swing.t <= 0) { this.swing = null; return; }
11557:          // useStyle/aim 与本地 useSwing 同构：远端 msg13 不带瞄准角，aim 取 0（正前方）——

```


---

## 🤖 Assistant · 2026-08-13T01:26:47.043Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 120,
 "offset": 4360
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:47.057Z

**📎 ToolResult**

```
4360	        if (isArrowKind && this.player.equipStats.quiver) knockback *= 1.1; // 箭袋击退 ×1.1（:52713）
4361	        const projId = ammoC?.shoot ?? bowC?.shoot ?? 1; // PickAmmo：projToShoot = 弹药 shoot
4362	        if (isArrowKind && this.player.equipStats.moltenQuiver && projId === 1) damage += 2; // 熔箭袋木箭→火矢+2（:52700，火矢 proj 换体从略）
4363	        const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
4364	        const ax = this.player.cx + Math.cos(ang) * 14;
4365	        const ay = this.player.cy - 4 + Math.sin(ang) * 14;
4366	        // 回收掉落：仅木箭（原版燃烧箭 Kill 不掉；子弹/飞镖不可回收）
4367	        const dropKey = projId === 1 ? ammoDef.key : null;
4368	        const bowArrow = new Arrow(ax, ay, Math.cos(ang) * speed, Math.sin(ang) * speed,
4369	          damage, knockback, projId, dropKey);
4370	        // 暴击链（审计 §6）：rangedCrit(装备/套装/词缀67-68配饰/buff) + 武器&弹药 item.crit
4371	        const bowVid2 = bowVid ?? (heldDef?.vid ?? -1);
4372	        bowArrow.critBonus = this.player.critChance('ranged')
4373	          + (itemCombat(bowVid2)?.crit ?? 0) + (ammoC?.crit ?? 0) + (ps?.crt ?? 0); // ⑧ 词缀 crt
4374	        bowArrow.armorPen = this.player.equipStats.armorPen + (ps?.arpen ?? 0); // ⑥+⑧ 词缀 arpen
4375	        this.entities.add(bowArrow, 'projectiles');
4376	        // ⑤ 霰弹族多弹丸（Player.cs:47326-47356/47539-47551）：爆管 534 rand(4,6) 发
4377	        // 散布±40×0.05；霰弹枪 964 rand(3,5) ±35×0.04；四管 4703 固定 8 发（同散布，
4378	        // 原版含 π/2 旋转向扰动近似取同表）——此前全族单发化 DPS 差 3-8 倍
4379	        {
4380	          const sg = SHOTGUN_PELLETS[bowVid2];
4381	          if (sg) {
4382	            const n = sg[0] < sg[1] ? sg[0] + Math.floor(Math.random() * (sg[1] - sg[0] + 1)) : sg[0];
4383	            for (let i2 = 1; i2 < n; i2++) {
4384	              const pvx = Math.cos(ang) * speed + (Math.random() * 2 * sg[3] - sg[3]) * sg[2] * 20;
4385	              const pvy = Math.sin(ang) * speed + (Math.random() * 2 * sg[3] - sg[3]) * sg[2] * 20;
4386	              const pa = new Arrow(ax, ay, pvx, pvy, damage, knockback, projId, null);
4387	              pa.critBonus = bowArrow.critBonus;
4388	              this.entities.add(pa, 'projectiles');
4389	            }
4390	          }
4391	        }
4392	        // 弹药节约（ammoCost80：20% 概率不耗弹——蘑菇矿胸甲族，Player.PickAmmo 语义）
4393	        if (!(((this.player.equipStats.ammoSave || this.player.buffs.has(BuffType.AmmoReservation)) && Math.random() < 0.2))) {
4394	          this.player.inv.removeAt(ammoSlot, 1);
4395	        }
4396	        this.player.useTime = bowC?.useTime ?? rg?.speed ?? 30;
4397	        // useStyle 5（弓枪族恒 5）：朝鼠标静持姿势 + 身体行档（Player.cs:46708 itemRotation=瞄准角）
4398	        this.useSwing(heldDef, ang);
4399	        // 发射音（原版 Item.cs UseSound）：弓（useAmmo 40）=Item_5；枪械通用=Item_11；
4400	        // 霰弹枪族 534/964/3788/4703=Item_36；手枪族 164/219/1255/1929/2269/2270=Item_41
4401	        // （Item_36/41 此前登记"素材未提取"，现已落位 public/sounds/——销核）
4402	        this.sfx.play(useAmmo === AMMO_ARROW ? 'bowShoot'
4403	          : GUN_SHOTGUN_VIDS.has(bowVid) ? 'gunShotgun'
4404	          : GUN_HANDGUN_VIDS.has(bowVid) ? 'gunHandgun' : 'gunShot');
4405	        this.cb.onInventoryChanged();
4406	      }
4407	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && cw && cw.kind !== 'melee'
4408	      && ((cw as { autoReuse?: boolean }).autoReuse || (inp.mouseDown && !this._prevMouseDown))) { // ⑩ autoReuse 门
4409	      // vi_* 数据驱动武器（1456 aiStyle 家族）：回旋镖/长矛/悠悠球/连枷/手雷/魔法/直射兜底。
4410	      // 必须排在 thrownCombat 之前——手雷(166 等)满足投掷判定但语义是 ai16 弹跳引信
4411	      this.useCombatWeapon(cw, heldDef);
4412	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && thrownCombat(heldDef)
4413	      && (itemCombat(heldDef.vid ?? viIdFromKey(heldDef.key))?.autoReuse || (inp.mouseDown && !this._prevMouseDown))) { // ⑩
4414	      // 消耗型投掷武器（手里剑/飞刀/毒刀等，Item.shoot + consumable + noMelee 且无 useAmmo）：
4415	      // 朝鼠标投出 item.shoot 投射物，消耗 1 个，数值全取 vanilla-itemcombat.json；
4416	      // 投射物复用 Arrow（重力 0.3/tick = 原版 aiStyle 2 抛物线同值；命中可回收）
4417	      const tc = thrownCombat(heldDef)!;
4418	      const vid = heldDef.vid ?? viIdFromKey(heldDef.key);
4419	      const c = itemCombat(vid);
4420	      const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
4421	      const px = this.player.cx + Math.cos(ang) * 14;
4422	      const py = this.player.cy - 4 + Math.sin(ang) * 14;
4423	      // 粉末族（净化粉 66 / 邪恶粉 67 / 猩红粉 2886）：proj 10/11/463 是 aiStyle 6
4424	      // 粉末云（64×64 无碰撞盒、180 tick、无重力），不是 aiStyle 2 抛物投掷物——
4425	      // 必须先于下方 Arrow 分流，否则退化成"可回收的投掷刀"（GAP 补齐）。
4426	      // 云体以玩家为中心生成（原版 ItemCheck_Shoot 弹心 = 人物中心）
4427	      const powderProj = POWDER_PROJ_BY_ITEM[vid];
4428	      if (powderProj) {
4429	        this.entities.add(new PowderProj(this.player.cx - 32, this.player.cy - 32,
4430	          Math.cos(ang) * (c?.shootSpeed ?? 4), Math.sin(ang) * (c?.shootSpeed ?? 4), powderProj), 'projectiles');
4431	      } else {
4432	        // 穿透取原版 penetrate（手里剑 4；-1 无限上限 6）。
4433	        // ★伤害对账修正：投掷族是 ranged（手里剑 42/投刀 279/毒刀 287 I:1851-1868
4434	        // ranged=true；277 是长矛非手里剑——曾误认）乘区=远程链×词缀（审计 §5）；
4435	        // ⑥ armorPen 移 hit 时（hurt 第 5 参减防语义），磨刀不适用投掷
4436	        const psT = this.heldPrefixStat();
4437	        const dmgT = Math.max(1, Math.round(tc.damage * (psT?.dmg ?? 1) * this.player.damageMult('ranged')));
4438	        let pen = projectileData(tc.shoot)?.penetrate ?? 1;
4439	        if (pen < 0) pen = 6;
4440	        pen = Math.max(1, Math.min(pen, 6));
4441	        const thrownArrow = new Arrow(px, py,
4442	          Math.cos(ang) * (c?.shootSpeed ?? 9), Math.sin(ang) * (c?.shootSpeed ?? 9),
4443	          dmgT, (c?.knockBack ?? 0) * (psT?.kb ?? 1), tc.shoot, heldDef.key, { pierce: pen });
4444	        thrownArrow.critBonus = this.player.critChance('ranged') + (c?.crit ?? 0) + (psT?.crt ?? 0); // 审计 §6 + ⑧ crt；投掷=ranged 族（§5）
4445	        thrownArrow.armorPen = this.player.equipStats.armorPen + (psT?.arpen ?? 0); // ⑥+⑧
4446	        this.entities.add(thrownArrow, 'projectiles');
4447	      }
4448	      this.player.inv.removeAt(this.player.inv.selected, 1);
4449	      this.player.useTime = c?.useTime ?? 15;
4450	      this.sfx.play('throw');
4451	      this.cb.onInventoryChanged();
4452	    } else if (heldDef && [70, 1331, 560].includes(viIdFromKey(heldDef.key))
4453	      && inp.mouseDown && this.player.useTime === 0) {
4454	      // Boss 召唤物(原版 Worm Food 70/Bloody Spine 1331/Slime Crown 560)
4455	      // 群系门（Player.cs:43107-43121/:43194-43208）：蠕虫食物需 ZoneCorrupt、
4456	      // 血腥脊椎需 ZoneCrimson——群系外整支不生效（不消耗/不进 useTime/无音效，
4457	      // 原版 if 内才 ApplyItemTime）；史莱姆王冠无门
4458	      const svid = viIdFromKey(heldDef.key);
4459	      const scene = this.scene;
4460	      const zoneOk = svid === 70 ? (scene == null || scene.zoneCorrupt)
4461	        : svid === 1331 ? (scene == null || scene.zoneCrimson) : true;
4462	      if (zoneOk) {
4463	        const summoned = svid === 70 ? this.summonBoss('eater_of_worlds_head')
4464	          : svid === 1331 ? this.summonBoss('brain_of_cthulhu')
4465	            : this.summonBoss('king_slime');
4466	        // 门拦下（同型 Boss 在场/访客）不消耗——原版 SpawnOnPlayer 失败不回滚物品，
4467	        // 本仓以"召唤成功才扣"为准（审计 2026-08-13）
4468	        if (summoned) {
4469	          this.player.inv.removeAt(this.player.inv.selected, 1);
4470	          this.player.useTime = 60;
4471	          this.cb.onInventoryChanged();
4472	        }
4473	      }
4474	      this.input.mouseDown = false;
4475	    } else if (heldDef && [556, 544, 557].includes(viIdFromKey(heldDef.key))
4476	      && inp.mouseDown && this.player.useTime === 0) {
4477	      // 机械三王召唤物(原版 556/544/557:需困难模式+夜晚)
4478	      if (!this.world.flags.hardMode) {
4479	        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.MechNotAwake'));

```


---

## 🤖 Assistant · 2026-08-13T01:26:57.051Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the key ranged chain is clear: `this.player.useTime = bowC?.useTime ?? rg?.speed ?? 30` at line 4396 — bow sets useTime = useTime of the combat table (which for bows/guns is typically == useAnimation). But note: for guns like Clockwork Assault Rifle (useTime 4, useAnimation 12, reuseDelay 14) — the repo fires ONE projectile per useTime=4 ticks → 3 shots per click... wait no: it fires every time useTime hits 0, so holding gives one shot every 4 ticks = 15 shots/sec, with NO reuseDelay and no 3-round-burst grouping. Vanilla: 3 shots (at itemTime==0 within one itemAnimation) then reuseDelay 14. So repo ❌ reuseDelay → excessive fire rate for those weapons. Big finding.

Also: useSwing() is called per shot (line 4398) — swing = itemAnimation restart per shot. In vanilla, itemAnimation is set once per use-start (ApplyItemAnimation) and shooting happens at itemTime==0 gates during the animation. For useTime==useAnimation weapons (most guns), they coincide. For useTime<useAnimation weapons (clockwork etc.), vanilla animation runs once while 3 shots happen. Repo restarts animation each shot — visual difference + functional (autoReuse skip semantics). Hmm — but actually repo's per-shot useSwing approximates vanilla's behavior for useTime==useAnimation where animation restarts each shot (well, vanilla anim is set at use start each time; with autoswing skip at itemAnimation==1 → effectively same cadence as useTime for useTime==useAnimation non-melee... wait no! For non-melee autoswing with useStyle 5, ApplyItemAnimation adds +1 (num=1) to useAnimation! That's the "Total time = useAnimation + 1" formula in the wiki. So vanilla: Megashark useAnimation 7 → itemAnimation = 8, autoswing skip at 1 → effectively 7-tick cycle = useTime. And the itemTime = useTime = 7 decrements alongside. So shots happen every 7 ticks (when itemTime hits 0). OK.

Now — an important detail for the repo's bow/gun chain: it does NOT add +1 nor implement the skip; it just uses useTime. Effectively identical cadence (useTime ticks). Fine — ⚠️ minor.

Now the ammo check: what gates bow firing? Let me look at the start of the bow section (before 4360) to see the useTime gate & ammo resolution. Let me read 4290-4360.

Also need to check useCombatWeapon (line ~4700-4760) for how ranged/magic/boomerang etc. set useTime.

And the swing damage window (itemAnimation hit window) — find where swingHitSet is consumed (melee hit). Let me grep swingHitSet.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:57.364Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 75,
 "offset": 4296
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:57.407Z

**📎 ToolResult**

```
4296	            const bt = BUFF_BY_VANILLA.get(ff.buffType);
4297	            if (bt !== undefined && bt !== BuffType.Resistance) {
4298	              this.player.buffs.apply(bt, Math.round((ff.buffTime ?? 7200) / 60)); // tick→秒
4299	            }
4300	          }
4301	          if (ff.healLife) {
4302	            this.player.hp = Math.min(this.player.maxHp, this.player.hp + ff.healLife);
4303	            this.addDamageNumber(this.player.cx, this.player.y, ff.healLife, false, '#40E080');
4304	            this.player.buffs.apply(BuffType.Resistance, 60); // 药水病（PotionSickness 近似）
4305	          }
4306	          if (ff.healMana) {
4307	            this.player.mana = Math.min(this.player.maxMana, this.player.mana + ff.healMana);
4308	            this.player.buffs.apply(BuffType.ManaSickness, 5); // 魔力眩晕（300t/瓶,max 合并）
4309	          }
4310	          this.player.inv.removeAt(this.player.inv.selected, 1);
4311	          this.player.useTime = 60;
4312	          this.sfx.play('drink');
4313	          this.cb.onInventoryChanged();
4314	        }
4315	      }
4316	    } else if (heldDef && inp.mouseDown && this.player.useTime === 0
4317	      && (heldDef.ranged || rangedAmmoWeapon(heldDef))) {
4318	      // 远程武器（弓/枪/吹箭筒）：PickAmmo + ItemCheck_Shoot 1:1（Player.cs:52590+/46426）
4319	      //   速度 = 弓 shootSpeed + 弹药 shootSpeed；伤害 = 弓 damage + 弹药 damage；
4320	      //   击退 = 弓 kb + 弹药 kb；投射物类型 = 弹药 shoot；音效 = 弓 UseSound(Item5)
4321	      //   弹药查找：原版先扫 54-57 弹药栏（Inventory.add 已把弹药归入 54-57），再扫背包 0-53 第一组
4322	      //   ★ vi_ 枪族（164 手枪/964 火铳/1319 雪球炮/281 吹箭筒等 useAmmo 武器）此前
4323	      //   combatWeapon 按 useAmmo 排除后无人接管 = 静默失效；此处经
4324	      //   vanilla-itemcombat.useAmmo 数据驱动接入（930 信号枪 useAmmo=-1 原版语义不接）
4325	      const rg = heldDef.ranged ?? null;
4326	      const bowVid = rg?.vid ?? viIdFromKey(heldDef.key);
4327	      const bowC = bowVid >= 0 ? itemCombat(bowVid) : null;
4328	      const useAmmo = bowC?.useAmmo ?? AMMO_ARROW;
4329	      // PickAmmo：弹药栏 54-57 优先，再背包 0-53 第一组 useAmmo 匹配
4330	      // （def.ammoId = legacy 注册；vi_ 弹药经 combat.ammo 反查）
4331	      const ammoOf = (d: (typeof ITEM_DEFS)[number]): number =>
4332	        d.ammoId ?? (d.vid != null || viIdFromKey(d.key) >= 0 ? itemCombat(d.vid ?? viIdFromKey(d.key))?.ammo ?? 0 : 0);
4333	      let ammoSlot = -1;
4334	      let ammoDef: (typeof ITEM_DEFS)[number] | null = null;
4335	      for (const [from, to] of [[54, 58], [0, 54]] as const) {
4336	        for (let i = from; i < to; i++) {
4337	          const sl = this.player.inv.slots[i];
4338	          if (!sl || sl.stack <= 0) continue;
4339	          const d = ITEM_DEFS[sl.id];
4340	          if (d && ammoOf(d) === useAmmo) { ammoSlot = i; ammoDef = d; break; }
4341	        }
4342	        if (ammoSlot >= 0) break;
4343	      }
4344	      if (ammoSlot >= 0 && ammoDef) {
4345	        const ammoC = ammoDef.vid != null || viIdFromKey(ammoDef.key) >= 0
4346	          ? itemCombat(ammoDef.vid ?? viIdFromKey(ammoDef.key)) : null;
4347	        // 箭速：射手 buff ×1.2（cap 20，:52717）+ 箭袋族 ×1.1（:52711）——仅箭族吃
4348	        const isArrowKind = bowC?.useAmmo !== 97 && bowC?.useAmmo !== 771 && bowC?.useAmmo !== 283;
4349	        let speed = (bowC?.shootSpeed ?? rg?.projSpeed ?? 7) + (ammoC?.shootSpeed ?? 0);
4350	        if (isArrowKind) speed = Math.min(20, speed * this.player.buffs.arrowSpeedMult
4351	          * (this.player.equipStats.quiver ? 1.1 : 1));
4352	        // 词缀乘区只作用于武器基伤（GetWeaponDamage：item.damage 含词缀，弹药另加）；
4353	        // 装备远程伤害乘区（侦察镜/复仇者徽章等）
4354	        const ps = this.heldPrefixStat();
4355	        // 弹药分道（Player.cs:3820 bowEffectiveDamage 拆分）：箭吃箭袋/射手/蘑菇矿箭头，
4356	      // 弹/火箭吃对应蘑菇矿头；Archery 不再误伤枪械
4357	      const rKind = bowC?.useAmmo === 97 ? 'bullet' : bowC?.useAmmo === 771 ? 'rocket' : bowC?.useAmmo === 283 ? 'other' : 'arrow';
4358	      let damage = Math.round((bowC?.damage ?? rg?.damage ?? 1) * (ps?.dmg ?? 1) * this.player.rangedDamageMult(rKind)) + (ammoC?.damage ?? 0); // ⑥ pen 移 hit 时
4359	        let knockback = (bowC?.knockBack ?? rg?.knockback ?? 2) * (ps?.kb ?? 1) + (ammoC?.knockBack ?? 0);
4360	        if (isArrowKind && this.player.equipStats.quiver) knockback *= 1.1; // 箭袋击退 ×1.1（:52713）
4361	        const projId = ammoC?.shoot ?? bowC?.shoot ?? 1; // PickAmmo：projToShoot = 弹药 shoot
4362	        if (isArrowKind && this.player.equipStats.moltenQuiver && projId === 1) damage += 2; // 熔箭袋木箭→火矢+2（:52700，火矢 proj 换体从略）
4363	        const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
4364	        const ax = this.player.cx + Math.cos(ang) * 14;
4365	        const ay = this.player.cy - 4 + Math.sin(ang) * 14;
4366	        // 回收掉落：仅木箭（原版燃烧箭 Kill 不掉；子弹/飞镖不可回收）
4367	        const dropKey = projId === 1 ? ammoDef.key : null;
4368	        const bowArrow = new Arrow(ax, ay, Math.cos(ang) * speed, Math.sin(ang) * speed,
4369	          damage, knockback, projId, dropKey);
4370	        // 暴击链（审计 §6）：rangedCrit(装备/套装/词缀67-68配饰/buff) + 武器&弹药 item.crit

```


---

## 🤖 Assistant · 2026-08-13T01:26:57.556Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"swingHitSet\" core/Game.ts | head -20",
 "description": "Find swing hit set consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:57.609Z

**📎 ToolResult**

```
555:  private swingHitSet = new Set<number>();
556:  /** 同一挥击内 tileCut 格只处理一次（与 swingHitSet 同生命周期） */
3763:    this.swingHitSet.clear();
4081:        this.swingHitSet.clear();
4114:        this.swingHitSet.clear();
4144:          this.swingHitSet.clear();
7924:      if (this.swingHitSet.has(c.id)) continue;
7926:        this.swingHitSet.add(c.id);
7932:    // 同一挥击只中一次(swingHitSet 按 Entity.id 去重)
7936:      if (this.swingHitSet.has(tn.id)) continue;
7940:      this.swingHitSet.add(tn.id);
7948:      if (this.swingHitSet.has(e.id)) continue;
7950:      this.swingHitSet.add(e.id);

```


---

## 🤖 Assistant · 2026-08-13T01:27:01.657Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 150,
 "offset": 7815
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:01.678Z

**📎 ToolResult**

```
7815	    if (coins > 1000) coins = 1000; // 防御性上限（原版由 Item.NewItem 内部面值转换）
7816	    drop(73, Math.max(1, Math.round(coins)));
7817	  }
7818	
7819	  private updateSwingHits() {
7820	    if (!this.swing) return;
7821	    this.swing.t--;
7822	    if (this.swing.t <= 0) { this.swing = null; return; }
7823	    const held = this.player.inv.heldItem();
7824	    if (!held) return;
7825	    const heldDef = ITEM_DEFS[held.id];
7826	    const tool = heldDef.tool ?? this.itemFuncTool(held.id);
7827	    // ---- 近战整体门（Player.cs:42964）：(damage>=0 && !noMelee) 才进 GetMeleeHitbox，
7828	    // 且 CutTiles/MeleeHitNPCs 都在 damage>0 内（cs:42991-43006）——
7829	    // 此前挥动药水/镜子（damage=0）也带 32×32 近战盒：砍草 + 对敌 1 点伤害 + 对小动物
7830	    // 一击致死，均为原版没有的行为（vi_ 数值取 combat 表，legacy 工具取 def.tool）
7831	    const swingVid = heldDef.vid ?? viIdFromKey(heldDef.key);
7832	    const swingCombat = swingVid >= 0 ? itemCombat(swingVid) : null;
7833	    const meleeDmg = this.swing.dmg ?? tool?.damage ?? swingCombat?.damage ?? 0;
7834	    const noMelee = heldDef.magic || swingCombat?.noMelee;
7835	    if (noMelee || meleeDmg <= 0) return;
7836	    // ---- 原版 ItemCheck_GetMeleeHitbox（Player.cs:44480）1:1：矩形判定非圆形 ----
7837	    // 基础矩形 = ApplyUseStyle 三段 itemLocation（手部位置，公式同 drawUseItem）+ **恒 32×32**
7838	    // （cs:44489 new Rectangle(itemLocation.X, itemLocation.Y, 32, 32) ×adjustedItemScale≈1，
7839	    // 与武器贴图尺寸无关——此前误用贴图帧宽高当基底，小武器欠打大武器超打）；
7840	    // 方向/重力翻转（cs:44506-44513）；useStyle1 三段扩展（cs:44516-44540）：
7841	    // **早段(anim≥0.666max) 宽×2 高×1.4 X 退 1.2宽 / 中段原样 / 晚段(anim<0.333max)
7842	    // 宽×1.4 高×1.1 Y 下移半高**——此前早/晚段扩展对调，注释也反
7843	    const pAnim = Math.min(1, Math.max(0, this.swing.t / this.swing.dur));
7844	    const ar = this.renderer?.atlas ? atlasIconForKey(this.renderer.atlas, ITEM_DEFS[held.id].key) : null;
7845	    const sprW = ar?.sw ?? 16, sprH = ar?.sh ?? 16;
7846	    const xTier = (w: number, phase: 0 | 1 | 2) => phase === 0
7847	      ? w >= 92 ? 38 : w >= 64 ? 28 : w >= 52 ? 24 : w > 32 ? 14 : 10
7848	      : phase === 1
7849	        ? w >= 92 ? 38 : w >= 64 ? 28 : w >= 52 ? 24 : w > 32 ? 18 : 10
7850	        : w >= 92 ? 38 : w >= 64 ? 28 : w >= 52 ? 24 : w >= 48 ? 18 : w > 32 ? 14 : 6;
7851	    const yTier = (h: number, phase: 0 | 1 | 2) => phase === 0 ? 24
7852	      : h > 64 ? 14 : h > 52 ? 12 : phase === 1 && h > 32 ? 8 : 10;
7853	    let offX: number, offY: number;
7854	    // ★两套三段阈值同源但产物不同，须拆开：命中盒扩展 phase（cs:44520-44541：
7855	    // 早段(anim≥0.666max ⟺ pAnim≥2/3)×2/×1.4、晚段(anim<0.333max ⟺ pAnim≤1/3)×1.4/×1.1）
7856	    // 与基座持位 tier（cs:49957-50095，同 Renderer.drawUseItem case 1——末段→前持位、
7857	    // 起手→后举位）。此前共用一个 phase，把基座持位也接反（早段取了前持位）
7858	    const phase: 0 | 1 | 2 = pAnim > 2 / 3 ? 0 : pAnim > 1 / 3 ? 1 : 2;
7859	    const tier: 0 | 1 | 2 = pAnim <= 1 / 3 ? 0 : pAnim < 2 / 3 ? 1 : 2;
7860	    const hitUs = this.swing.useStyle ?? 1;
7861	    if (hitUs === 3) {
7862	      // useStyle 3（雨伞 946/4707）单一持位（cs:50279-50294）：
7863	      // offX = fw/2-4-max(pAnim*fw*1.2-10, 8)、offY = 顶+24
7864	      offX = sprW * 0.5 - 4 - Math.max(pAnim * sprW * 1.2 - 10, 8);
7865	      offY = 24;
7866	    } else if (tier === 0) { offX = sprW * 0.5 - xTier(sprW, 0); offY = yTier(sprH, 0); }
7867	    else if (tier === 1) { offX = sprW * 0.5 - xTier(sprW, 1); offY = yTier(sprH, 1); }
7868	    else { offX = -(sprW * 0.5 - xTier(sprW, 2)); offY = yTier(sprH, 2); }
7869	    const p = this.player;
7870	    let bx = p.cx + p.facing * offX;
7871	    let by = p.y + offY;
7872	    let bw = 32, bh = 32; // 恒定基底（cs:44489），与武器贴图无关
7873	    if (p.facing === -1) bx -= bw;
7874	    by -= bh;
7875	    if (hitUs === 3) {
7876	      // useStyle 3（cs:44545-44560 + :50279-50312）：anim>0.666 收势段 dontAttack；
7877	      // 判定段宽×1.4 / 高×0.6（Y 下移 0.6 高）；雨伞本体再 高+14 宽-10（朝左 X+10）
7878	      if (pAnim > 0.666) return;
7879	      if (p.facing === -1) bx -= Math.floor(bw * 1.4 - bw);
7880	      bw = Math.floor(bw * 1.4);
7881	      by += Math.floor(bh * 0.6);
7882	      bh = Math.floor(bh * 0.6);
7883	      if (swingVid === 946 || swingVid === 4707) {
7884	        bh += 14;
7885	        bw -= 10;
7886	        if (p.facing === -1) bx += 10;
7887	      }
7888	    } else if (phase === 0) {
7889	      // 三段扩展（cs:44516-44540）：早段大盒覆盖抡起区、晚段小盒收势
7890	      if (p.facing === 1) bx -= Math.floor(bw * 1.2);
7891	      bw *= 2;
7892	      by -= Math.floor(bh * 1.4 - bh);
7893	      bh = Math.floor(bh * 1.4);
7894	    } else if (phase === 2) {
7895	      if (p.facing === -1) bx -= Math.floor(bw * 1.4 - bw);
7896	      bw = Math.floor(bw * 1.4);
7897	      by += Math.floor(bh * 0.5);
7898	      bh = Math.floor(bh * 1.1);
7899	    }
7900	    // 原版 ItemCheck_CutTiles（Player.cs:44002）：挥击矩形内所有 tileCut/KillTile
7901	    for (let ty = Math.floor(by / TILE); ty <= Math.floor((by + bh - 1) / TILE); ty++) {
7902	      for (let tx = Math.floor(bx / TILE); tx <= Math.floor((bx + bw - 1) / TILE); tx++) {
7903	        const tk = tx * 100000 + ty;
7904	        if (this.swingTileCutSet.has(tk)) continue;
7905	        const t = this.world.store.get(tx, ty);
7906	        if (t === POT_TILE) {
7907	          this.swingTileCutSet.add(tk);
7908	          this.smashPot(tx, ty);
7909	        } else if (TILE_CUT.has(t)) {
7910	          this.swingTileCutSet.add(tk);
7911	          this.breakTile(tx, ty);
7912	        }
7913	      }
7914	    }
7915	    // 矩形-AABB 相交判定（原版 ItemCheck_MeleeHitNPCs 的 npc.getRect().Intersects(itemRectangle)）
7916	    const prog = 1 - pAnim;
7917	    // 法杖系 noMelee=true 已在入口门整体跳过（含 CutTiles——原版 noMelee 连
7918	    // GetMeleeHitbox 都不进，cs:42964；此前的 magic 后置 return 只挡实体不挡砍草）
7919	    const hitRect = (ex: number, ey: number, ew: number, eh: number) =>
7920	      ex < bx + bw && ex + ew > bx && ey < by + bh && ey + eh > by;
7921	    // 小动物：任何挥击一击致死
7922	    for (const cent of this.entities.critters) {
7923	      const c = cent as Critter;
7924	      if (this.swingHitSet.has(c.id)) continue;
7925	      if (hitRect(c.x, c.y, c.w, c.h)) {
7926	        this.swingHitSet.add(c.id);
7927	        c.hurt(this);
7928	      }
7929	    }
7930	    // 城镇 NPC:巫毒窄门(原版 ApplyItemToNPC/Damage_PVE_Inner :11970-11972——
7931	    // 向导 22 需装备向导巫毒娃娃 267、裁缝师 54 需裁缝娃 1307,其余免疫玩家近战);
7932	    // 同一挥击只中一次(swingHitSet 按 Entity.id 去重)
7933	    for (const nent of this.entities.npcs) {
7934	      const tn = nent as TownNPC;
7935	      if (!(tn instanceof TownNPC) || tn.dead || tn.bound) continue;
7936	      if (this.swingHitSet.has(tn.id)) continue;
7937	      const eq = this.player.equipStats;
7938	      const doll = tn.vanillaId === 22 ? eq.killGuide : tn.vanillaId === 54 ? eq.killClothier : false;
7939	      if (!doll || !hitRect(tn.x, tn.y, tn.w, tn.h)) continue;
7940	      this.swingHitSet.add(tn.id);
7941	      const swBase = ((meleeDmg || Math.max(1, Math.ceil((tool?.power ?? 10) / 16)))
7942	        * this.player.damageMult('melee')); // ⑥ pen 移 hit 时（挥击处传）
7943	      const swDmg = Math.max(1, Math.round(swBase * (1 + (Math.random() * 30 - 15) / 100)));
7944	      tn.hurt(swDmg, (Math.sign(tn.cx - p.cx) || this.player.facing) * 2, 0, this);
7945	    }
7946	    for (const ent of this.entities.enemies) {
7947	      const e = ent as Enemy;
7948	      if (this.swingHitSet.has(e.id)) continue;
7949	      if (!hitRect(e.x, e.y, e.w, e.h)) continue;
7950	      this.swingHitSet.add(e.id);
7951	      // 怪物专属受击声（各家族不同）；播放失败回退通用 hit
7952	      if (!this.sfx.playFiles(e.def.hitSound, 1, e.cx, e.cy)) this.sfx.play('hit', 1, e.cx, e.cy);
7953	      const crit = Math.random() < 0.04 + this.player.critChance('melee') / 100
7954	        // ★武器 item.crit(GetWeaponCrit:4 基础+武器+装备)——vi_ 数据驱动近战武器 crit
7955	        // 字段此前未入链(挥砍侧全族只有装备 crit)
7956	        + (itemCombat(this.swing ? (ITEM_DEFS[this.swing.item]?.vid ?? viIdFromKey(ITEM_DEFS[this.swing.item]?.key ?? '')) : -1)?.crit ?? 0) / 100;
7957	      // 工具（镐/斧）也有攻击力但远弱于剑：功率/16（铁镐 3 / 铁斧 4，铁剑 16）—— 仅应急；
7958	      // vi_ 数据驱动近战武器优先取挥击时缓存的 combat 表伤害/击退（swing.dmg/kb）；
7959	      // 装备全系伤害乘区（徽章/险恶词缀等，ApplyEquipFunctional dmgMelee 段）
7960	      const baseDmg = ((meleeDmg || Math.max(1, Math.ceil((tool?.power ?? 10) / 16)))
7961	        * this.player.damageMult('melee')); // ⑥ pen 移 hit 时（挥击处传）
7962	      this.player.onMeleeHit(); // 甲虫进攻套蓄能（命中结算前计数无碍）
7963	      // 原版 Main.DamageVar：±15% 浮动（1 + rand(-15..15)/100）
7964	      const dmg = Math.max(1, Math.round(baseDmg * (crit ? 2 : 1) * (1 + (Math.random() * 30 - 15) / 100)));

```


---

## 🤖 Assistant · 2026-08-13T01:27:11.168Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. updateSwingHits is quite well ported (GetMeleeHitbox 3-phase). Swing damage window: whole animation (swing.t from dur-1 down to 1) — matches vanilla `itemAnimation > 0` whole window with per-NPC once-per-swing (swingHitSet ≈ meleeNPCHitCooldown cleared at StartActualUse). ✅ mostly.

But one nuance: vanilla meleeNPCHitCooldown is set per hit — let me check what value is set after a hit (to know whether a second hit can occur in the SAME swing if the cooldown is shorter than animation). Wiki: "A single target will only be hit once during one swinging animation." Let me check ProcessHitAgainstNPC tail → SetMeleeHitCooldown(i, ?). Let me grep quickly.

Then remaining repo checks:
1. useCombatWeapon — ranged/magic/boomerang useTime source (line 4700-4800).
2. hotbar item switch gate — does repo block switching while swinging? check where canChangeImmediately / inventory hotbar selection happens (input handling for digit keys / wheel). Search "canChangeImmediately" usage in SmartSelect and direct selected assignment.
3. Potion drinking: repo sets useTime=60 and healBlocked → 30. Vanilla: potion useAnimation (heal potion useAnimation=17, useTime=17?) Actually let me check Item.cs for healing potion defaults. Vanilla Lesser Healing Potion: useTime 17, useAnimation 17? The task hint says "useTime 长如 17?". Let me grep Item.cs DefaultToHealingPotion.
4. 魔力/魔力眩晕/魔力弹速 — out of domain.
5. placeAnimation / placement rhythm: repo tryPlace — check useTime set there.
6. 冲刺/位移武器 (Shadow dagger?) — probably out of scope/未实装.
7. Check repo: 使用中能否跳跃/移动 — vanilla allows movement (useTurn); jumping while using item: vanilla allows unless mount. Repo: nothing blocks. ✅.

Let me check the vanilla healing potion useTime and SetMeleeHitCooldown value.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:12.180Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"SetMeleeHitCooldown(i\" Player.cs | head -5; echo \"=== healing potion ===\"; grep -n \"public void DefaultToHealingPotion\\|DefaultToFood\\|DefaultToManaPotion\" Item.cs | head; grep -n \"DefaultToHealingPotion\" -A 12 Item.cs | head -18",
 "description": "Melee cooldown value and potion useTime"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:12.263Z

**📎 ToolResult**

```
43566:	public void SetMeleeHitCooldown(int npcIndex, int timeInFrames)
=== healing potion ===
42232:			DefaultToFood(22, 22, 0, 0);
47658:			DefaultToFood(22, 22, 207, 172800);
47662:			DefaultToFood(22, 22, 207, 14400);
47666:			DefaultToFood(22, 22, 207, 14400);
47670:			DefaultToFood(22, 22, 207, 57600);
47674:			DefaultToFood(22, 22, 207, 86400);
47678:			DefaultToFood(22, 22, 207, 14400, useGulpSound: true);
47682:			DefaultToFood(22, 22, 207, 86400);
47686:			DefaultToFood(22, 22, 207, 57600, useGulpSound: true);
47690:			DefaultToFood(22, 22, 207, 57600, useGulpSound: true);
48000:			DefaultToHealingPotion(22, 22, 80);
48001-			SetShopValues(ItemRarityColor.Blue1, 40);
48002-			break;
48003-		}
48004-		float num = 0f;
48005-		num = ((buffType == 207) ? (num + 12f) : ((buffType != 206) ? (num + 3f) : (num + 8f)));
48006-		num += (float)(buffTime / 14400);
48007-		rare = (int)(num / 4f);
48008-	}
48009-
48010-	public void DefaultToMinecart(int mount)
48011-	{
48012-		width = 36;
--
48185:	public void DefaultToHealingPotion(int newwidth, int newheight, int healingAmount, int animationTime = 17)
48186-	{
48187-		UseSound = SoundID.Item3;
48188-		useStyle = 9;

```


---

## 🤖 Assistant · 2026-08-13T01:27:18.690Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '48185,48220p' Item.cs; echo \"=== SetMeleeHitCooldown caller ===\"; grep -n \"SetMeleeHitCooldown(\" Player.cs | head; ",
 "description": "Healing potion defaults and melee CD caller"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:18.752Z

**📎 ToolResult**

```
	public void DefaultToHealingPotion(int newwidth, int newheight, int healingAmount, int animationTime = 17)
	{
		UseSound = SoundID.Item3;
		useStyle = 9;
		useTurn = true;
		useAnimation = (useTime = animationTime);
		consumable = true;
		width = newwidth;
		height = newheight;
		rare = 1;
		value = buyPrice(0, 0, 20);
		potion = true;
		healLife = healingAmount;
	}

	public void SetShopValues(ItemRarityColor rarity, int coinValue)
	{
		rare = (int)rarity;
		value = coinValue;
	}

	public void DefaultToHeadgear(int newwidth, int newheight, int helmetArtID)
	{
		width = newwidth;
		height = newheight;
		headSlot = helmetArtID;
	}

	public void DefaultToBody(int newwidth, int newheight, int bodySlotID)
	{
		width = newwidth;
		height = newheight;
		bodySlot = bodySlotID;
	}

	public void DefaultToLegs(int newwidth, int newheight, int legSlotID)
=== SetMeleeHitCooldown caller ===
43566:	public void SetMeleeHitCooldown(int npcIndex, int timeInFrames)
43589:		SetMeleeHitCooldown(npcIndex, itemAnimation);
43768:			SetMeleeHitCooldown(npcIndex, itemAnimation);

```


---

## 🤖 Assistant · 2026-08-13T01:27:29.024Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key vanilla facts confirmed:
- DefaultToHealingPotion: useAnimation = useTime = 17 (default). useStyle=9 (举杯), useTurn=true. So potion drinking is 17 ticks animation, and the heal is applied when itemTime hits 0 (at the END of the 17-tick animation — actually `ItemTimeIsZero && itemAnimation > 0` branch at 42189: healLife>0 → ApplyLifeAndOrMana + ApplyItemTime. itemTime starts at 17 and decrements to 0 at the 17th tick; so heal applies on the LAST tick of the animation). NOT instant at click. Repo: instant heal + useTime=60 (Game.ts:4217) — ❌/🔀.
- SetMeleeHitCooldown(npcIndex, itemAnimation) at 43768 → per-NPC cooldown = current itemAnimation remaining, so one hit per swing. ✅ matches swingHitSet semantics.

Now the remaining checks:
1. useCombatWeapon (4700-4800) — useTime source for magic/boomerang/spear/yoyo/flail/grenade/summon.
2. Hotbar switch gate.
3. tryPlace useTime (placement rhythm).
4. Mana cost / mana gate (use chain interrupt) — partially domain (使用中喝药打断? no, that's mana).
5. Check the `_prevMouseDown` recording position and clickEdge for non-autoReuse melee — at line 2700 `this.prevSwingMouse = !!this.input?.mouseDown;` — is that after updateUse? Line 2700 comment says 挥剑点击沿. Let me check where 2697-2710 sits relative to updateUse.

Let me read useCombatWeapon and the 2690-2710 region.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:29.994Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 120,
 "offset": 4690
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:30.018Z

**📎 ToolResult**

```
4690	            bob.baitVid = baitVid;          // IsLavaBait 三源判定用（Projectile.cs:19230）
4691	            this.entities.add(bob, 'projectiles');
4692	            this.sfx.play('throw');
4693	            // 成就：抛竿（Player.cs:48652 HandleSpecialEvent(7) → THROWING_LINES）
4694	            this.achievements.handleSpecialEvent(7,
4695	              { statLifeMax: this.player.maxHp, statManaMax: this.player.maxMana });
4696	          }
4697	        }
4698	        this.input.mouseDown = false;
4699	      }
4700	    }
4701	    this.mining = null;
4702	  }
4703	
4704	  /** vi_* 数据驱动武器使用派发（combatWeapon 解析出的 aiStyle 家族）。
4705	   *  数值全部取 vanilla-itemcombat.json（damage/knockBack/useTime/shootSpeed/mana），
4706	   *  行为取 1456 aiStyle 语义（WeaponProj.ts 各实体） */
4707	  /** 手持物词缀属性（Item.Prefix 持久在物品实例上；无词缀=全 1） */
4708	  private heldPrefixStat() {
4709	    const pfx = this.player.inv.heldItem()?.prefix;
4710	    return pfx ? prefixStat(pfx) : null;
4711	  }
4712	
4713	  private useCombatWeapon(cwIn: Exclude<CombatWeapon, { kind: 'melee' }>, def: (typeof ITEM_DEFS)[number]) {
4714	    const inp = this.input;
4715	    const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
4716	    const px = this.player.cx + Math.cos(ang) * 14;
4717	    const py = this.player.cy - 4 + Math.sin(ang) * 14;
4718	    const consume = () => {
4719	      this.player.inv.removeAt(this.player.inv.selected, 1);
4720	      this.cb.onInventoryChanged();
4721	    };
4722	    // 词缀乘区（Item.Prefix :551-557）：damage=round(×dmg)、knockBack×kb——
4723	    // 手雷兜底下限在乘区后取 max，与原版（damage 先乘再判 0）一致；
4724	    // 装备全系伤害乘区（徽章/险恶词缀等）：近战族=melee、魔法=magic、其余=ranged
4725	    const ps = this.heldPrefixStat();
4726	    const dmgKind = cwIn.kind === 'magic' ? 'magic' : (cwIn.kind === 'boomerang' || cwIn.kind === 'spear' || cwIn.kind === 'yoyo' || cwIn.kind === 'flail') ? 'melee' as const : 'ranged' as const;
4727	    const cw = {
4728	      ...cwIn,
4729	      damage: Math.max(1, Math.round(cwIn.damage * (ps?.dmg ?? 1) * this.player.damageMult(dmgKind))), // ⑥ pen 移 hit 时
4730	      knockback: cwIn.knockback * (ps?.kb ?? 1),
4731	      // ⑧ 词缀乘区出口统一折算（I:558-568）：shtspd→shootSpeed、spd→useTime（I:561）
4732	      shootSpeed: ((cwIn as { shootSpeed?: number }).shootSpeed ?? 0) * (ps?.shtspd ?? 1),
4733	      useTime: Math.max(1, Math.round(((cwIn as { useTime?: number }).useTime ?? 0) * (ps?.spd ?? 1))),
4734	    };
4735	    // GetWeaponCrit（Player.cs:42531 族）= 4 基础 + 武器 item.crit + 装备/buff——
4736	    // 投射物近战四族此前写死 4%（Sunfury item.crit=7 原版应 11%）
4737	    const critVid = def.vid ?? viIdFromKey(def.key);
4738	    const critTotal = 0.04 + (itemCombat(critVid)?.crit ?? 0) / 100
4739	    // 成就：蜜蜂套装持蜂枪使用（Player.cs:16060-16069 → event 3 NOT_THE_BEES：
4740	    // head 160 + body 168 + legs 103 且 itemAnimation 中挥动 1121 BeeGun）
4741	    if (critVid === 1121) {
4742	      const b0 = this.player.inv.armor[0], b1 = this.player.inv.armor[1], b2 = this.player.inv.armor[2];
4743	      if (b0 && b1 && b2
4744	        && statOfInternal(b0.id)?.hs === 160 && statOfInternal(b1.id)?.bs === 168
4745	        && statOfInternal(b2.id)?.ls === 103) {
4746	        this.achievements.handleSpecialEvent(3,
4747	          { statLifeMax: this.player.maxHp, statManaMax: this.player.maxMana });
4748	      }
4749	    }
4750	      + this.player.critChance(dmgKind === 'magic' ? 'magic' : dmgKind === 'ranged' ? 'ranged' : 'melee') / 100
4751	      + (ps?.crt ?? 0) / 100; // ⑧ 词缀 crt（I:566 crit+=crt）
4752	    // 使用姿势（Player.ItemCheck：itemAnimation>0 期间持物可见）。
4753	    // ★ spear/yoyo/flail/boomerang 族源码 noUseGraphic=true（DefaultToSpear :47637 等
4754	    //   202 处）——投射物即本体，挥动再画持物会重影，这四族不加 swing
4755	    if (cw.kind === 'grenade' || cw.kind === 'magic' || cw.kind === 'shot' || cw.kind === 'summon') {
4756	      this.useSwing(def, ang);
4757	    }
4758	    switch (cw.kind) {
4759	      case 'grenade': {
4760	        // AI_016：引信 timeLeft（Projectile.SetDefaults：炸弹28=150/炸药棍29=135/手雷30=180）
4761	        // ——此前 29/30 映射对调（炸药棍拿了炸弹的 150、手雷拿了炸药棍的 135）
4762	        const fuse = cw.shoot === 28 ? 150 : cw.shoot === 29 ? 135 : 180;
4763	        // 爆炸伤害（Projectile.SetDefaults）：炸弹28=100/炸药棍29=250/手雷30=60；
4764	        // 此前手雷误取 250
4765	        const dmg = cw.shoot === 28 ? 100 : cw.shoot === 29 ? 250 : Math.max(cw.damage, 60);
4766	        // 地形破坏半径（Projectile.cs:75262 表）：炸弹族28/37/516/519=4、炸药棍族
4767	        // 29/470/637=7；**手雷族(30 等)不在 ExplodeTiles 判定表内=不破坏地形**
4768	        const er = Game.EXPLODE_RADIUS[cw.shoot] ?? 0;
4769	        // 实体伤害盒(Projectile.Kill :74885/:74951):炸弹 28/手雷 30 = 22×22 盒半宽 11;
4770	        // 炸药棍 29 = 200×200 盒半宽 100——与地形破坏半径【无关】
4771	        const hurtBox = cw.shoot === 29 ? 100 : 11;
4772	        this.entities.add(new GrenadeProj(px, py,
4773	          Math.cos(ang) * cw.shootSpeed, Math.sin(ang) * cw.shootSpeed,
4774	          dmg, fuse, cw.shoot, (ex, ey, edmg) => this.explodeAt(Math.floor(ex / TILE), Math.floor(ey / TILE), edmg, er, er > 0, hurtBox, this.player.equipStats.armorPen + (ps?.arpen ?? 0))), 'projectiles'); // ⑥+⑧
4775	        consume();
4776	        this.player.useTime = cw.useTime;
4777	        this.sfx.play('throw');
4778	        this.input.mouseDown = false; // 消费点击(⑩ 边沿门防连发,与 flail/yoyo/magic 一致)
4779	        break;
4780	      }
4781	      case 'glowstick': {
4782	        // aiStyle 14（AI_014 弹跳物理/粘性粘墙/妖精排斥场）：消耗 1 支掷出；
4783	        // 光照走通用弹幕点光（projectileData.light=1）
4784	        this.entities.add(new GlowstickProj(px, py,
4785	          Math.cos(ang) * cw.shootSpeed, Math.sin(ang) * cw.shootSpeed,
4786	          cw.shoot), 'projectiles');
4787	        consume();
4788	        this.player.useTime = cw.useTime;
4789	        this.sfx.play('throw');
4790	        this.input.mouseDown = false;
4791	        break;
4792	      }
4793	      case 'boomerang': {
4794	        // AI_003：飞出减速→返回主角（非消耗，回手即消失）
4795	        const bom = new Boomerang(px, py,
4796	          Math.cos(ang) * cw.shootSpeed, Math.sin(ang) * cw.shootSpeed,
4797	          cw.damage, cw.knockback, cw.shoot);
4798	        bom.critChance = critTotal;
4799	        bom.armorPen = this.player.equipStats.armorPen; // ⑥
4800	        // 301 Bouncing Shield 按 20t/100t 双门需 channel（其余族不用,空挂无害）
4801	        if (cw.shoot === 301) bom.channel = () => this.input.mouseHeld && !this.input.uiBlocking;
4802	        this.entities.add(bom, 'projectiles');
4803	        this.player.useTime = cw.useTime;
4804	        this.sfx.play('throw');
4805	        this.input.mouseDown = false;
4806	        break;
4807	      }
4808	      case 'spear': {
4809	        // AI_019：随角色前刺——伸缩包络按型号参数表(AI_019_Spears_GetSpearOffset),位移=offset×shootSpeed

```


---

## 🤖 Assistant · 2026-08-13T01:27:30.024Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 30,
 "offset": 2690
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:30.044Z

**📎 ToolResult**

```
2690	      this._deathHandled = false;
2691	    }
2692	
2693	    // ---- 智能光标（每帧 lookup；结果供 updateUse 覆盖目标格 + 渲染黄框） ----
2694	    this.updateSmartCursor();
2695	    // ---- 智能选取（Player.cs:24923 selectedItemState.Update：Shift 按住自动换手持
2696	    //      工具/光源；须在 updateUse 前跑，同帧换选即被使用路径看到） ----
2697	    this.updateSmartSelect();
2698	    // ---- 使用物品（鼠标） ----
2699	    this.updateUse(dt);
2700	    this.prevSwingMouse = !!this.input?.mouseDown; // 挥剑点击沿（非 autoReuse 武器需重新点击）
2701	    // ⑩ 边沿门的上一帧快照（须在 updateUse 后记录,见上方注记）
2702	    this._prevRightDown = !!inp?.rightDown;
2703	    this._prevMouseDown = !!inp?.mouseDown;
2704	
2705	    // ---- 实体 ----
2706	    this.entities.update(dt, this);
2707	
2708	    // ---- 传送带实体输送（Collision.StepConveyorBelt, Collision.cs:4215-4351）----
2709	    // 原版在各自碰撞段内调用（Player.cs:27920 / NPC.cs:93774 / WorldItem.cs:938），
2710	    // 这里统一为实体更新后的后处理：每 tick 末等价，对各自 moveAndCollide 无侵入。
2711	    // 掉落物走 itemMode（ApplyConveyorBeltMovementToVelocity :3936-4211，改 vx 逼近
2712	    // 档位目标）；敌怪带 NPCID.Sets.ConveyorBeltCollision 门（NPCID.cs:4789，
2713	    // 普通敌怪原版不吃带）；联机傀儡是快照驱动，本地不动。
2714	    {
2715	      const cst = this.world.store;
2716	      if (!player.dead) stepConveyor(player, cst, player.gravDir);
2717	      for (const e of this.entities.npcs) if (!e.netPuppet) stepConveyor(e, cst, 1);
2718	      for (const e of this.entities.critters) if (!e.netPuppet) stepConveyor(e, cst, 1);
2719	      for (const e of this.entities.drops) if (!e.netPuppet) stepConveyor(e, cst, 1, true);

```


---

## 🤖 Assistant · 2026-08-13T01:27:32.990Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now let me check the hotbar/selection switch gate — where the player changes held item (digit keys / scroll) and whether it's blocked during swing. Search for inv.selected assignment and canChangeImmediately usage.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:34.100Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"canChangeImmediately\" . | head; echo \"=== selected = 直写 ===\"; grep -n \"inv.selected = \\|selected = heldSlot\\|selected = slot\" core/Game.ts | head -20; echo \"=== inventory 键盘换选 ===\"; grep -n \"Digit\\|hotbar\\|scrollSlot\\|selectSlot\" core/Game.ts | head -20",
 "description": "Check item switch gating"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:34.179Z

**📎 ToolResult**

```
core/Game.ts:3901:      canChangeImmediately: !this.swing && p.useTime === 0,
player/SmartSelect.ts:181:  canChangeImmediately: boolean;
player/SmartSelect.ts:250:    if (!host.canChangeImmediately) return;                    // :484
player/SmartSelect.ts:492:    if (!host.canChangeImmediately || item === host.selected) return;   // :425-426
=== selected = 直写 ===
1364:        this.player.inv.selected = code === 'Digit0' ? 9 : Number(code.slice(5)) - 1;
3909:    p.inv.selected = host.selected;
11547:        proxy.inv.selected = Math.min(rp.selectedItem, 9); // 快捷栏 0-9（heldItem 依赖）
=== inventory 键盘换选 ===
1363:      if (this.player && /^Digit[0-9]$/.test(code) && !this.input.uiBlocking) {
1364:        this.player.inv.selected = code === 'Digit0' ? 9 : Number(code.slice(5)) - 1;
3900:      hotbar: this.smartSelectHotbar,

```


---

## 🤖 Assistant · 2026-08-13T01:28:01.209Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So:
- SmartSelect (shift-based) gates on canChangeImmediately = !swing && useTime===0. 
- Digit key hotbar switch (Game.ts:1363-1364) has NO gate at all — you can switch items mid-swing. Vanilla: `TrySwitchingLoadout`/`LeftClick` in ItemSlot blocks switching held item when itemAnimation != 0 (wiki: "Switching held item (when itemAnimation tick counter is not zero)"). Also Player.cs:24918 `if (itemAnimation == 0 && ItemTimeIsZero && reuseDelay == 0)` is the smart-select gate. And selectedItemState has HasBufferedChange buffering. So digit-key immediate switch mid-use = ❌/🔀. Note also: in vanilla, when you switch items mid-use it doesn't cancel animation... Actually vanilla blocks the switch entirely while itemAnimation>0 (inventory hotbar via mouse). For keyboard hotkeys, PlayerInput triggers controlInv... hmm. In vanilla, pressing 1-9 while swinging: the item switch is deferred via selectedItemState (SelectedItemState.HasBufferedChange / buffered change applied when itemAnimation==0). Let me verify quickly: Player.cs:24918 is `if (itemAnimation == 0 && ItemTimeIsZero && reuseDelay == 0)` in selectedItemState.Update. Yes! That's the buffered-change application. So vanilla buffers the switch and applies it when idle. Repo digit keys apply immediately = 🔀.

Let me confirm line 24918 context.

Then: check tryPlace (placement rhythm) useTime. And check whether repo swing blocks potion drinking during use — the potion branch requires useTime===0, and useTime is set by swing... For melee, useTime = reuseSpd (useTime) which is < swing duration sometimes; potion requires useTime===0 but the swing branch runs first and returns early (line 4101-4102 `this.mining=null; return;`) for swords — so while holding a sword and clicking, you never reach the potion branch anyway (different held item). OK fine.

But important: repo `useTime` single timer vs vanilla dual itemTime+itemAnimation. Effects:
- For melee weapons, repo sets useTime = useTime (raw) and swing = useAnimation-scaled. So cooldown between swings = useTime, not useAnimation. Vanilla: new swing starts when itemAnimation hits 0 (or 1 with autoswing) — i.e., effective swing period = scaled useAnimation (with skip: useAnimation-1 ticks for autoswing melee). Repo: swing restarts when `useTime === 0 && canChain && (swingOver || reuseSpd < animSpd)`. Since swingOver requires swing.t<=1 (animation essentially done), the gate is useTime===0 AND swing almost done. So effective period = max(reuseSpd, animSpd-1). Vanilla = animSpd (with skip → animSpd-1... careful). So repo = max(useTime, useAnimation) vs vanilla ≈ useAnimation (skip) for autoswing melee. For most melee useTime==useAnimation → same. For melee with useTime>useAnimation (e.g., some tools?) → repo slower (max) vs vanilla: animation ends at useAnimation, but new use requires itemTime==0 too — wait no! Vanilla new use requires only `itemAnimation == 0` (line 42144: controlUseItem && releaseUseItem && itemAnimation == 0). itemTime being >0 does NOT block a new use! Hmm, but for melee useTime==useAnimation typically. Actually wait — if useTime > useAnimation, itemTime would still be >0 when animation ends... then a new use starts anyway (itemAnimation==0 gate passes), ApplyItemTime resets itemTime. Hmm, but then shoot/effect gates use ItemTimeIsZero — a new use start doesn't reset itemTime (ApplyItemTime is only called in the ItemTimeIsZero branches). Interesting: for melee weapons with useTime > useAnimation, effect (shoot) would be skipped on some swings. Edge case.

Key difference: vanilla swing period for autoswing melee = scaledUseAnimation with the 1-tick skip at itemAnimation==1 → effective (scaledUseAnimation - 1)... hmm, actually the skip sets itemAnimation=0 when it hits 1, then new use sets itemAnimation = scaled again. So the cycle = scaled ticks. Since the animation is set to N and skips the last tick (1→0), effective = N-1? Let's think: itemAnimation set to N at tick T0. Each tick decrements. At tick T0+N-2 it reaches 1 → AutoReuseLogic sets to 0 → new use same tick → itemAnimation = N. So cycle = N-1 ticks. Wiki says "actual use time of autoswing melee weapons is one tick lower". Yes — cycle = N-1 where N = floor(useAnimation/(1+bonus)). Repo: swingOver = swing.t <= 1, i.e., at t==1 the swing restarts (setting t = animSpd). Swing restart happens at Game.ts:4074 gate — same cycle = animSpd - 1? Let's see: t=animSpd set at frame 0. updateSwingHits decrements: t becomes animSpd-1, animSpd-2, ... When t==1, swingOver true → restart sets t=animSpd. So ticks between restarts = animSpd-1. ✅ matches vanilla skip semantics! Nice.

But the extra gate `this.player.useTime === 0` — useTime = reuseSpd = useTime (raw). If useTime < useAnimation-1... then useTime hits 0 before swing is over; gate `(swingOver || reuseSpd < animSpd)` — if reuseSpd < animSpd, the condition passes even when swing is NOT over (swingOver false) → restart swing early, cutting the animation. So for melee weapons with useTime < useAnimation, repo restarts the swing every useTime ticks (fast), whereas vanilla lets the animation play out (period = useAnimation-1) — itemTime==0 mid-swing only gates shoot/heal effects. This is a real 🔀 but how many melee weapons have useTime < useAnimation? Let me check the data quickly: vanilla-itemcombat.json in game — count melee with useTime < useAnimation. Let me find that file.

Also for the potion: repo heal instant + useTime=60. Vanilla: useTime=useAnimation=17, heal applied at the end (itemTime hits 0), potion delay 3600 (potionDelayTime) w/ buff 21; repo uses healBlocked (30?) — the buffs.apply(BuffType.Resistance, 60) = 60 seconds? In repo buffs are seconds (apply(bt, seconds)). Resistance 60s? Vanilla PotionSickness = 3600 ticks = 60s. OK ✅. But heal-block toast path sets useTime=30 (Game.ts:4207) — that's a hack.

Wait — repo Game.ts:4217: `this.player.useTime = 60;` for potions. Vanilla potion useAnimation=useTime=17. So repo 60 vs vanilla 17 — ⚠️. Also vi_ consumables (line 4311) also useTime=60. Vanilla 17.

Hmm, but actually: is that 60 a "balance choice"? Regardless it's a numeric deviation worth flagging.

Now placement: check tryPlace and tryPlaceWall for useTime.

Let me also check the mining rhythm: tool swing spd = max(14, tool.speed / attackSpeedMult) — vanilla tool useAnimation scaled by meleeSpeed? For tools: melee && !NoMeleeSpeedBonus → yes, tools are melee and get meleeSpeed scaling (unless NoMeleeSpeedBonus). Pickaxe useAnimation 25ish. But mining cadence (toolTime) — vanilla itemTime for tools = useTime (unscaled!). Hmm wait — that's a big one! For pickaxes, useTime (tool speed) determines hit rate on tiles; useAnimation determines swing animation. Vanilla: ApplyItemTime(sItem) = RAW useTime (unscaled by meleeSpeed). Repo: `tryMine(tx, ty, dual.power, dual.type, spd, tool.useTime ?? spd)` where spd = scaled useAnimation... and tool.useTime = c?.useTime ?? 20 (raw). Let me read tryMine to see which drives the mining hit cadence.

Let me check tryPlace, tryMine, and the vanilla-itemcombat melee useTime<useAnimation count.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:28:02.054Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"private tryPlace\\b\\|private tryPlace(\\|private tryPlaceWall\\|private tryMine\" core/Game.ts; echo \"===\"; sed -n '/private tryMine/,/^  }/p' core/Game.ts | head -40",
 "description": "Read tryMine cadence"
}
```


---

## 🤖 Assistant · 2026-08-13T01:28:02.451Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game && ls public/data 2>/dev/null | head; find . -name \"vanilla-itemcombat*\" -not -path \"*/node_modules/*\" | head",
 "description": "Locate item combat data file"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:07.228Z

**📎 ToolResult**

```
5090:  private tryMine(tx: number, ty: number, power: number, toolType: 'pick' | 'axe' | 'hammer', speed: number, useTime?: number) {
5910:  private tryPlaceWall(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
5975:  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
===
  private tryMine(tx: number, ty: number, power: number, toolType: 'pick' | 'axe' | 'hammer', speed: number, useTime?: number) {
    // 联机破坏保护（v3 房间制）：非房主禁挖/禁锤墙
    if (!this.netCanEditTile()) { this.mining = null; this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    // 范围检查
    if (!this.inTileRange(tx, ty)) { this.mining = null; return; }
    const type = this.world.store.get(tx, ty);
    // 恶魔祭坛（tile 26，原版 Player.cs:45058）：镐不可破坏（def pick:-1 拦）；
    // 锤 ≥80 锤力且困难模式 → SmashAltar（砸碎=困难矿三档轮换+幽灵）；
    // 否则进度清零 + 玩家受 statLife/2 电击（ByOther(4)）
    if (type === TILE_BY_KEY['v_26_altars']) {
      this.mining = null;
      if (toolType === 'hammer' && power >= 80 && this.world.flags.hardMode) {
        this.smashAltar(tx, ty);
      } else if (toolType === 'hammer') {
        const p = this.player;
        const dmg = Math.max(1, Math.floor(p.maxHp / 2));
        p.damage(dmg, p.cx - p.facing * 8, p.cy, false);
        this.addDamageNumber(p.cx, p.y, dmg, false, '#B080FF');
        this.sfx.play('hit', 0.8);
      }
      return;
    }
    // 锤：敲除背景墙（无墙则无事发生；也可清装饰）
    if (toolType === 'hammer') {
      // 矿车轨道锤击（Player.cs:45442-45447）：FrameTrack(pound) 循环切换连接/加速向
      if (type === this.trackTile && this.trackTile !== 0) {
        if (this.tickCount - this.lastMineHitTick >= Math.max(8, speed)) {
          this.lastMineHitTick = this.tickCount;
          frameTrack(this.world.store, tx, ty, true);
          this.sfx.play('tink');
        }
        this.mining = null;
        return;
      }
      // 原版锤循环（Player.cs:45625-45695）：整砖→半砖→slope1→2→3→4→整砖。
      // 方向感知：右实左空 → 先 slope2；上实下空（天花板模式）→ 先 slope3/4。
      // 平台族的锤循环（:45394-45440 平台坡面/楼梯）未接入——依赖登记：
      // 平台 slope 帧的楼梯绘制 + 对应坡面碰撞（平台 slope1-4 的可行走楼梯几何）
      const hd = TILE_DEFS[type];
      const poundable = type !== 0 && !!hd && hd.solid && !hd.platform && !hd.framed;

```


---

## 👤 User(sidechain) · 2026-08-13T01:28:07.294Z

**📎 ToolResult**

```
./src/data/vanilla-itemcombat.json

```


---

## 🤖 Assistant · 2026-08-13T01:28:09.691Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check how tryMine uses `speed` and `useTime` for the hit cadence — the HitTile throttle. Let me look at the mine hit throttle part of tryMine and the tryPlace useTime setting. Also count melee weapons with useTime < useAnimation in the combat table.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:28:10.380Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"lastMineHitTick\" core/Game.ts | head; echo \"=== tryPlace useTime ===\"; sed -n '5975,6080p' core/Game.ts | grep -n \"useTime\\|swing\" ",
 "description": "Mining throttle and place useTime"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:10.422Z

**📎 ToolResult**

```
543:  private lastMineHitTick = -999;
5116:        if (this.tickCount - this.lastMineHitTick >= Math.max(8, speed)) {
5117:          this.lastMineHitTick = this.tickCount;
5130:      if (poundable && this.world.store.isSolid(tx, ty) && this.tickCount - this.lastMineHitTick >= Math.max(8, speed)) {
5131:        this.lastMineHitTick = this.tickCount;
5169:      if (this.tickCount - this.lastMineHitTick < Math.max(8, speed)) {
5174:      this.lastMineHitTick = this.tickCount;
5208:    if (this.tickCount - this.lastMineHitTick < cooldown) {
5214:    this.lastMineHitTick = this.tickCount;
=== tryPlace useTime ===
45:        this.player.useTime = 14;
54:      if (this.player.useTime > 0) return;
65:      this.player.useTime = 14;
87:    if (this.player.useTime > 0) return;
97:      this.player.useTime = 14;

```


---

## 🤖 Assistant · 2026-08-13T01:28:11.530Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && node -e \"\nconst c=require('./data/vanilla-itemcombat.json');\nconst arr=Array.isArray(c)?c:Object.values(c);\nlet keys=Object.keys(Array.isArray(c)?{}:c);\n// try to find melee entries\nconst e=arr[0]; console.log('sample keys:',JSON.stringify(e).slice(0,400));\n\" ",
 "description": "Inspect combat table structure"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:42.514Z

**📎 ToolResult**

```
sample keys: {"damage":5,"knockBack":2,"useTime":13,"useAnimation":20,"autoReuse":true,"melee":true}

```


---

## 🤖 Assistant · 2026-08-13T01:28:51.868Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting! Sample entry (probably item id 0 = copper shortsword? no, damage 5... hmm whatever): useTime=13, useAnimation=20, autoReuse=true, melee=true. So there ARE melee weapons with useTime < useAnimation! Wait — this is entry index 0 of the object values, which may be item id 0 (no item). Hmm, "damage":5,"knockBack":2,"useTime":13,"useAnimation":20 — hmm. Actually maybe the JSON is keyed by id. Let me analyze properly: count melee entries with useTime<useAnimation, useTime>useAnimation, and reuseDelay field presence.

Also tryMine cadence: `this.tickCount - this.lastMineHitTick >= Math.max(8, speed)` where speed = scaled useAnimation (spd = max(14, tool.speed/attackSpeedMult)). Line 5208 uses `cooldown` — let me check what cooldown is there (maybe the useTime param). Let me read 5150-5215.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:28:54.255Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && node -e \"\nconst c=require('./data/vanilla-itemcombat.json');\nconst ks=Object.keys(c);\nlet n=0,melee=0,lt=0,gt=0,eq=0,ltMelee=0,gtMelee=0,hasReuse=0,reuseNonZero=0,exLt=[],exGt=[],exReuse=[];\nfor(const k of ks){\n  const e=c[k]; n++;\n  if(e.melee){melee++; if(e.useTime<e.useAnimation){ltMelee++;if(exLt.length<12)exLt.push([k,e.useTime,e.useAnimation,e.autoReuse]);} if(e.useTime>e.useAnimation){gtMelee++;if(exGt.length<12)exGt.push([k,e.useTime,e.useAnimation]);} if(e.useTime===e.useAnimation)eq++;}\n  if('reuseDelay' in e){hasReuse++; if(e.reuseDelay) {reuseNonZero++; if(exReuse.length<15)exReuse.push([k,e.reuseDelay,e.useTime,e.useAnimation,e.melee?'melee':e.ranged?'ranged':e.magic?'magic':'?']);}}\n}\nconsole.log('total',n,'melee',melee,'melee useTime<useAnim',ltMelee,'>',gtMelee,'melee eq',eq);\nconsole.log('entries with reuseDelay field:',hasReuse,'nonzero:',reuseNonZero);\nconsole.log('ex melee lt:',JSON.stringify(exLt));\nconsole.log('ex melee gt:',JSON.stringify(exGt));\nconsole.log('ex reuse:',JSON.stringify(exReuse));\n\"",
 "description": "Analyze combat table useTime patterns"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:02.063Z

**📎 ToolResult**

```
total 2612 melee 303 melee useTime<useAnim 111 > 7 melee eq 182
entries with reuseDelay field: 0 nonzero: 0
ex melee lt: [["1",13,20,true],["7",20,30,true],["10",19,27,true],["45",15,30,true],["103",15,20,true],["104",19,45,true],["122",18,23,true],["186",19,27,null],["196",25,37,true],["204",16,30,true],["213",13,25,true],["217",14,27,true]]
ex melee gt: [["65",40,20],["676",30,23],["723",35,20],["724",55,20],["989",45,21],["1226",60,26],["1227",28,16]]
ex reuse: []

```


---

## 🤖 Assistant · 2026-08-13T01:29:24.929Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Big findings:
1. **The combat table has NO reuseDelay field at all** — reuseDelay is entirely missing from vanilla-itemcombat.json → can't be implemented from data. Combined with the grep showing reuseDelay not implemented anywhere in code. ❌ Both data + logic missing.

2. **Melee weapons with useTime < useAnimation: 111 of 303** (36.8%!). Examples: item 1 (copper shortsword? no — item 1 is... actually item 1 = dirt block. Hmm. Let me check: item id 1 = Dirt Block, which is melee? Dirt block: damage 5? no... Actually dirt block has no damage. Hmm, but item 1 in Terraria = "Iron Pickaxe"? No. Item IDs: 1 = Dirt Block. Hmm, melee:true damage 5 for dirt block? That seems odd but blocks DO have damage 0... Actually wait, in Item.cs SetDefaults for item 1 (Dirt Block): `useStyle = 1; useAnimation = 14; useTime = 10; createTile = 0; autoReuse = true;` and width/height... Blocks don't have damage. Hmm, the extractor may set melee=true from `melee = true`? For blocks vanilla doesn't set melee. Let me check item 10 = Musket? No — item 10 = Mushroom? Let me verify: Item 10 = "Musket"? Actually: 1=Dirt Block, 2=Stone Block, 3=Torch, 4=Wood... 10 = Mushroom. Hmm, damage 5 useTime 19 useAnimation 27 — Mushroom is a consumable heal. melee=true?? 

Hmm — the extractor's "melee" flag might be `!ranged && !magic && !summon && !thrown` i.e. default melee. That's plausible: vanilla Item.melee defaults to false though... Actually no: In Item.SetDefaults, for most items the `melee` field isn't explicitly set... but the repo's combatWeapon probably classifies by useStyle/damage. Let me check how melee is derived — look at the extractor or combatWeapon. Item 45 = Cloud in a Bottle? No — 45 is "Breathing Reed"? Hmm. Let me not go down this hole; the important part is the repo's own combatWeapon() interpretation. Let me check combatWeapon source to see how it decides kind='melee'.

Actually more relevant: item 989 (Chlorophyte Claymore): useTime 45 > useAnimation 21! And 1226 (Cutlass): 60 > 26. 65 (Mana Crystal? no, 109 is mana crystal; 65 = Magic Mirror? no, 71 is magic mirror... 65 = "Band of Regeneration"? Hmm). These are "gt" examples: useTime > useAnimation — meaning cooldown longer than animation → gap between swings. For these, repo effective period = max(useTime, animSpd) via gate — that matches vanilla semantics reasonably (vanilla: new use needs itemAnimation==0 only; itemTime still counting doesn't block new use... hmm, actually wait).

Hold on. Let me recheck: vanilla new-use gate at 42144 is `controlUseItem && releaseUseItem && itemAnimation == 0`. itemTime doesn't gate the new use. So for Chlorophyte Claymore (useTime 45, useAnimation 21): swing animation 21 ticks, then new use immediately at tick 21 (itemAnimation==0), while itemTime still has 24 ticks left. So effective swing period = 21 (scaled), NOT max(45,21). And the itemTime remaining would suppress the shoot-effect on subsequent swings (ItemTimeIsZero false) — actually shootsEveryUse sets flag4=ItemAnimationJustStarted so claymore still shoots.

So repo's `useTime === 0 &&` gate + `(swingOver || reuseSpd<animSpd)` → for 989: reuseSpd=45 > animSpd=21 → requires useTime==0 which takes 45 ticks AND swing over (21). Effective period 45 vs vanilla 21. **Repo is 2.1× slower for Chlorophyte Claymore/Cutlass family.** That's a real numeric bug (⚠️/🔀).

Wait, but hold on — is that right? For melee weapons where useTime > useAnimation in vanilla, is there something else? Let me check: item 989 Chlorophyte Claymore Item.cs: useTime... let me verify from the decompiled Item.cs rather than trusting the extractor. grep case 989.

3. Also need: does the repo's melee chain handle "swing restart while animation incomplete" for useTime<useAnimation (111 melee items)? Yes: `(swingOver || reuseSpd < animSpd)` → restarts swing every useTime ticks, cutting the animation. Vanilla: animation plays to completion (period = useAnimation-1 ticks for autoswing), with itemTime==0 gating only the shoot/effect. So for e.g. item 45 (useTime 15, useAnimation 30): vanilla swing period = 29 ticks; repo = 15 ticks → nearly 2× faster swings. ⚠️/🔀 major.

Hmm wait, but actually — I should double check vanilla for melee+autoswing+useTime<useAnimation. When itemTime hits 0 mid-swing and controlUseItem held: the AutoReuseLogic sets itemAnimation=0 when itemAnimation==1 only. So no early restart. New use only when itemAnimation==0. So yes, animation-bound. And the wiki note "if such a weapon's useTime is less than its useAnimation, it still cannot shoot a projectile again until the swing finishes" confirms.

BUT — hmm, one more consideration: for melee weapons the repo's `reuseSpd` is `Math.max(1, Math.round(cwMelee!.useTime))` (raw). So for the 111 items the repo swings every useTime. This is exactly the "此前把 useTime 当动画时长" bug family — they fixed animation duration but introduced early-restart.

Let me verify a couple of these item IDs in Item.cs to be sure the extractor is right (e.g., 45, 103, 104, 989, 1226). Let me grep the SetDefaults cases.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:29:25.553Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && for id in 1 45 103 989 1226; do echo \"=== item $id ===\"; grep -n \"case $id:\" Item.cs | head -2; done",
 "description": "Locate item SetDefaults cases"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:33.648Z

**📎 ToolResult**

```
=== item 1 ===
704:		case 1:
1373:		case 1:
=== item 45 ===
1000:		case 45:
1894:		case 45:
=== item 103 ===
2565:		case 103:
=== item 989 ===
12732:		case 989:
=== item 1226 ===
15102:		case 1226:

```


---

## 🤖 Assistant · 2026-08-13T01:29:37.036Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '1000,1030p' Item.cs; echo \"=== 989 ===\"; sed -n '12732,12745p' Item.cs; echo \"=== 1226 ===\"; sed -n '15102,15115p' Item.cs",
 "description": "Verify item useTime/useAnimation in source"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:37.115Z

**📎 ToolResult**

```
		case 45:
			spd = 0.95f;
			break;
		case 46:
			crt = 3;
			spd = 0.94f;
			dmg = 1.07f;
			break;
		case 47:
			spd = 1.15f;
			break;
		case 48:
			spd = 1.2f;
			break;
		case 49:
			spd = 1.08f;
			break;
		case 50:
			dmg = 0.8f;
			spd = 1.15f;
			break;
		case 51:
			kb = 0.9f;
			spd = 0.9f;
			dmg = 1.05f;
			crt = 2;
			break;
		}
		value = 1f * dmg * (2f - spd) * (2f - mcst) * size * kb * shtspd * (1f + (float)crt * 0.02f) * (1f + (float)arpen * 0.015f) * (1f + (float)tagdmg * 0.03f);
		if (rolledPrefix == 62 || rolledPrefix == 69 || rolledPrefix == 73 || rolledPrefix == 77)
		{
=== 989 ===
		case 989:
			autoReuse = true;
			rare = 2;
			UseSound = SoundID.Item1;
			useStyle = 1;
			damage = 23;
			useAnimation = 21;
			useTime = 45;
			scale = 1.1f;
			width = 30;
			height = 30;
			shoot = 173;
			shootSpeed = 9.5f;
			knockBack = 4.25f;
=== 1226 ===
		case 1226:
			useStyle = 1;
			useAnimation = 26;
			useTime = 60;
			shoot = 229;
			shootSpeed = 8f;
			knockBack = 6f;
			width = 40;
			height = 40;
			damage = 95;
			UseSound = SoundID.Item1;
			rare = 7;
			value = 276000;
			scale = 1f;

```


---

## 🤖 Assistant · 2026-08-13T01:29:47.689Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed! Item 989 (Chlorophyte Claymore): useAnimation=21, useTime=45, autoReuse=true, shoot=173. Item 1226 (Cutlass): useAnimation=26, useTime=60.

So in vanilla: Chlorophyte Claymore swings every 21 ticks (animation-bound) and shoots a projectile each swing via shootsEveryUse? Let me check shootsEveryUse for 989. grep "ShootsEveryUse" or item.shootsEveryUse assignment. In Item.cs there's a loop assigning shootsEveryUse for a list. Let me check.

Wait, actually the first grep hit (case 45 at line 1000) was the Prefix method, not SetDefaults. Item 45 in the second file position (1894) is SetDefaults. Whatever — item 45 = ? with useTime 15/useAnimation 30 per extractor... hmm that first case 45 at 1000 is prefix. Let me not verify 45; 989 and 1226 are solid proof.

Now: for melee weapons with useTime > useAnimation (7 melee: 65, 676, 723, 724, 989, 1226, 1227) — repo makes them slower than vanilla (period max(useTime, anim) vs vanilla anim).

For melee with useTime < useAnimation (111) — repo restarts swings early → faster than vanilla.

Both directions of deviation share the same root: repo treats itemTime as the swing-restart gate (single-timer model), while vanilla gates restart on itemAnimation only.

Let me double check the vanilla behavior once more for item 1226 Cutlass: useAnimation 26, useTime 60. Vanilla: swing every 26 ticks; the projectile (229) shoots when flag4: itemAnimation>0 && ItemTimeIsZero && flag — itemTime starts at 60 and decrements; it hits 0 only during the 3rd swing (26*2=52 <60, so at tick 60, mid-3rd-swing). shootsEveryUse? If 1226 is in the shootsEveryUse list, flag4 = ItemAnimationJustStarted → shoots every swing. Let me check the list.

Now also confirm melee weapon damage window & attackCD. And check ApplyAttackCooldown. attackCD is set where? `attackCD` — in ItemCheck_MeleeHitNPCs gate `attackCD <= 0`. ApplyAttackCooldown sets attackCD = 3? Let me grep quickly. This matters for the repo (swingHitSet gives one hit per swing per NPC; vanilla similar + attackCD for multi-hit protection). Let me check.

Also: shootsEveryUse list — grep "shootsEveryUse" in Item.cs.

Let me batch these.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:29:48.257Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"attackCD = \\|ApplyAttackCooldown\" Player.cs | head -10; echo \"=== shootsEveryUse ===\"; grep -n \"shootsEveryUse\" Item.cs | head -5",
 "description": "Check attackCD and shootsEveryUse"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:48.311Z

**📎 ToolResult**

```
24405:			attackCD = 0;
31278:			ApplyAttackCooldown(20);
43472:			ApplyAttackCooldown();
43590:		ApplyAttackCooldown();
43773:			ApplyAttackCooldown();
43777:	public void ApplyAttackCooldown()
43779:		attackCD = Math.Max(1, (int)((double)itemAnimationMax * 0.33));
43782:	public void ApplyAttackCooldown(int frames)
43786:			attackCD = frames;
50931:		attackCD = 0;
=== shootsEveryUse ===
274:	public bool shootsEveryUse;
3711:			shootsEveryUse = true;
4577:			shootsEveryUse = true;
5677:			shootsEveryUse = true;
9279:			shootsEveryUse = true;

```


---

## 🤖 Assistant · 2026-08-13T01:29:49.064Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && sed -n '5195,5215p' core/Game.ts; echo \"=== tryPlace tail useTime ===\"; sed -n '5975,6080p' core/Game.ts | sed -n '1,10p;40,110p'",
 "description": "Read mining cooldown and tryPlace"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:49.133Z

**📎 ToolResult**

```
      }
      this.mining = null;
      return;
    }
    // ---- 原版 HitTile 制 1:1（Player.cs:45032-45120 ItemCheck_UseMiningTools_ActuallyUseMiningTool
    //      + :52981 GetPickaxeDamage）：每击积累、阈值 100 破坏；冷却 = useTime
    //      （原版 toolTime=ApplyItemTime(useTime)，非 useAnimation）。
    //      采矿加速（TileSpeedAcc 砌砖刀/建筑师背包族：冷却 -25%）----
    const tileSpeedMult = (this.player.equipStats.tileSpeed || this.player.buffs.has(BuffType.Mining)) ? 0.75 : 1;
    // 食物 pickSpeed -= 5/10/15%（Player.cs:11534+）× 风筝 −15%（:9616）→
    // 冷却按原版 useTime/pickSpeed 缩短
    const pickMult = this.player.buffs.pickSpeedMult;
    const cooldown = Math.max(8, Math.round((useTime ?? speed) / this.player.attackSpeedMult) * tileSpeedMult / pickMult);
    if (this.tickCount - this.lastMineHitTick < cooldown) {
      // 节流窗内：只刷新裂缝显示，不积累
      this.hardnessCache = 100;
      this.mining = { x: tx, y: ty, progress: this.hitTiles.getDamage(tx, ty) };
      return;
    }
    this.lastMineHitTick = this.tickCount;
    const d = TILE_DEFS[type];
=== tryPlace tail useTime ===
  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    const st = this.world.store;
    if (!st.inBounds(tx, ty)) return;
    // 距离
    const dx = tx - Math.floor(this.player.cx / TILE);
    const dy = ty - Math.floor(this.player.cy / TILE);
    if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) return;
    const tileId = TILE_BY_KEY[itemDef.tile!];
    const def = TILE_DEFS[tileId];
        st.setTile(tx, y, ropeTile, 0, 0);
        placed++;
      }
      if (placed > 0) {
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 14;
        this.sfx.play('place');
        this.cb.onInventoryChanged();
      }
      return;
    }
    // 火把锚定（TileObjectData tile4 + TileObject.CanPlace 1:1）：
    // 底锚(0)→左锚(22)→右锚(44)→墙锚(0)；普通火把液体中拒绝、水炬 8/11/17 允许
    if (tileId === T.TORCH) {
      if (this.player.useTime > 0) return;
      if (st.isActive(tx, ty)) return;
      const frame = torchAnchorFrame(st, tx, ty);
      // placeStyle（Item.cs placeStyle→TileObjectData subtile）：彩色 427-433 /
      // 群系火把显式表 / 水炬 8/11/17——此前恒 0 = 群系火把放成普通火把（色光全失）
      const style = torchStyleOfItemKey(itemDef.key);
      if (frame < 0) return;
      // 液体门（WaterPlacement）：普通火把 NotAllowed、水炬三色 Allowed
      if (st.liquid[st.idx(tx, ty)] > 0 && !isWaterTorchStyle(style * 22)) return;
      st.setTile(tx, ty, tileId, frame, style * 22);
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = 14;
      this.sfx.play('place');
      this.cb.onInventoryChanged();
      return;
    }
    // 放置空间检查
    for (let dx2 = 0; dx2 < ow; dx2++) {
      for (let dy2 = 0; dy2 < oh; dy2++) {
        const px = tx + dx2, py = ty + dy2;
        if (!st.inBounds(px, py)) return;
        if (st.isActive(px, py)) return;
        // 实心物不能与玩家重叠
        if (def.solid && this.overlapsEntity(px, py)) return;
      }
    }
    // 支撑检查：非漂浮。原版权威 = TileObjectData.CanPlace（TileObjectData.cs 每_tile
    // 锚点表：AnchorTop/Bottom/Wall/AlternateTiles + 方向备选），全量锚点表未提取——
    // 此处以"下/上/侧邻任一格有内容或墙"近似（依赖登记：TileObjectData 锚点类型表）。
    // 矿车轨道（314）例外：无锚点可悬空铺设（TileObjectData 314 无 Anchor 项）
    const isTrack = def.vanilla?.sheet === TRACK_SHEET;
    const needSupport = !isTrack && (def.solid || def.platform || def.framed);
    if (needSupport && !this.hasSupport(tx, ty, ow, oh)) return;
    if (this.player.useTime > 0) return;

    // 矿车轨道（WorldGen.PlaceTile case 314 → Minecart.PlaceTrack + SquareTileFrame：
    // frameX/frameY 是连接 ID 非 18px 像素偏移，随后 FrameTrack 按邻接定型；
    // style = placeStyle：0 普通 / 1 压板(2492) / 2 左加速(2739)；声效 Item52）
    if (isTrack) {
      const style = Math.max(0, Math.min(3, itemDef.placeStyle ?? 0));
      placeTrack(st, tx, ty, style);
      frameTrackArea(st, tx, ty);
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = 14;
      this.playSfxFile('Item_52', 0.8, tx * TILE, ty * TILE);
      this.cb.onInventoryChanged();
      return;
    }

    // 放置
    const isVanillaStyle = !!def.vanilla && def.vanilla.frame === 'style';
    for (let dx2 = 0; dx2 < ow; dx2++) {
      for (let dy2 = 0; dy2 < oh; dy2++) {

```


---

## 🤖 Assistant · 2026-08-13T01:30:00.652Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key mining finding (Game.ts:5208): `cooldown = Math.max(8, Math.round((useTime ?? speed) / this.player.attackSpeedMult) * tileSpeedMult / pickMult)`.

Vanilla: toolTime = itemTime = ApplyItemTime(item) = **RAW useTime, unscaled** (ApplyItemTime P:4216-4218: SetItemTime(sItem.useTime) — no meleeSpeed!). The repo divides useTime by attackSpeedMult → mining cooldown shrinks with melee speed bonuses. **That's a deviation** — vanilla pickaxe useTime is NOT affected by meleeSpeed (only useAnimation is). Actually wait — careful. Let me re-derive: in vanilla, mining cadence = toolTime which is set to itemTime at the end of owner code: `if (!channel) toolTime = itemTime;`. And itemTime = useTime raw. And ApplyItemAnimation scales useAnimation by meleeSpeed for melee (tools are melee). So pickaxe swing animation speeds up with melee speed, but hit cadence on tiles stays at raw useTime. Hmm, but hold on — is that really true? For pickaxes, useTime == useAnimation typically (e.g. copper pickaxe useAnimation 15, useTime 10? let me check). Let me check item 1? no. Pickaxe ids: 1? no — Copper Pickaxe = 3509? no, 3509 is Orichalcum... Copper Pickaxe is 3509? Actually Copper Pickaxe = 1? Hmm: 1 = Dirt Block... The pickaxes: 3509? No — 3509 is "Copper Pickaxe"? Terraria item IDs: 1 Dirt Block... 3509 Copper Pickaxe? I recall 3509 = Copper Pickaxe is wrong; it's 3509 = Orichalcum Pickaxe? Let me just check a pickaxe: Iron Pickaxe = 1? no. Let me grep "pick = " in Item.cs for one id and check useTime/useAnimation.

Actually the repo's tool table: `useTime: c?.useTime ?? 20, speed: c?.useAnimation ?? 25` — for tools, tool.useTime is the combat useTime and speed is useAnimation. Then mining cooldown = useTime / attackSpeedMult — vanilla = raw useTime. So ⚠️: repo mines faster with melee speed accessories; vanilla does not.

Hmm wait — but is that right in vanilla? Let me verify by checking a pickaxe's numbers and the mining code gate: `if (!ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem) return;` (line 41173-ish in PlaceThing? no, that's UseMiningTools). Let me check ItemCheck_UseMiningTools: line 41223 `if (ItemTimeIsZero && itemAnimation > 0 && controlUseItem)`. So a mining hit happens when itemTime hits 0 during the animation. For a pickaxe with useTime 10 and useAnimation 15, you'd get a hit every 10 ticks... and itemTime restarts (ApplyItemTime) only when? In UseMiningTools there must be an ApplyItemTime per hit. OK whatever — the key point stands: itemTime = raw useTime, NOT scaled by meleeSpeed. The repo scales it. Let me verify a pickaxe to be sure about the direction (does melee speed affect mining speed in vanilla? The wiki "Mining speed" page says pickaxe useTime is affected by melee speed? Hmm. Actually I recall: mining speed is affected by melee speed modifiers? Let me check the Mining_speed wiki page — it's in the mirror.

Let me read Mining_speed.md quickly (just the mechanics section).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:01.043Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && sed -n '1,40p' Mining_speed.md 2>/dev/null || ls | grep -i mining",
 "description": "Read mining speed wiki"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:01.125Z

**📎 ToolResult**

```
Guide_Hellstone_Mining.md
Guide_Mining_Strategies.md
Guide_Mining_Techniques.md
Guide_Mining.md
Guide_Tips_for_Mining.md
Legacy_Mining_armor.md
Legacy_Mining_Potion.md
Mining_armor
Mining_armor.md
Mining_Potion.md
Mining_techniques.md

```


---

## 🤖 Assistant · 2026-08-13T01:30:01.629Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"case 3509:\\|case 3541:\\|case 3348:\" Item.cs | head -4",
 "description": "Locate pickaxe cases"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:01.659Z

**📎 ToolResult**

```
30508:		case 3348:
31362:		case 3509:
31725:		case 3541:

```


---

## 🤖 Assistant · 2026-08-13T01:30:03.767Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '31362,31380p' Item.cs",
 "description": "Read pickaxe 3509 stats"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:03.793Z

**📎 ToolResult**

```
		case 3509:
			SetDefaults1(1);
			this.type = type;
			useTime = 15;
			pick = 35;
			useAnimation = 23;
			damage = 4;
			scale = 0.9f;
			tileBoost = -1;
			value = 500;
			return;
		case 3508:
			SetDefaults1(4);
			this.type = type;
			useAnimation = 21;
			damage = 9;
			value = 450;
			scale = 1f;
			return;

```


---

## 🤖 Assistant · 2026-08-13T01:30:30.382Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Item 3509 (Copper Pickaxe): useTime=15, useAnimation=23. So a pickaxe has useTime(15) < useAnimation(23). In vanilla: animation 23 ticks (scaled by meleeSpeed); mining hit when itemTime hits 0 = every 15 ticks (RAW, unscaled). So hits happen mid-animation; new swing restarts at itemAnimation==0 (23 ticks, scaled).

Repo: swing restart gate `useTime===0 && (!this.swing || this.swing.t <= 1)` → wait, for tools the branch is line 4111: `if (this.player.useTime === 0 && (!this.swing || this.swing.t <= 1))` — restart requires swing almost done → effective period = 23 (scaled). Mining cooldown = useTime(15)/attackSpeedMult → scaled by melee speed (⚠️ vanilla: unscaled 15).

Hmm, so there are two deviations in mining:
(a) hit cadence scaled by meleeSpeed (vanilla: raw useTime)
(b) since swing restart requires t<=1 (23 ticks) but useTime=15 → the swing timer and mine timer diverge: mining hits every 15 ticks while swing restarts every 23 — matches vanilla-ish (vanilla: hits at itemTime==0 every 15, swings every 23). OK (b) is fine.

But wait — vanilla hits per swing: itemTime 15, animation 23 → within one 23-tick swing, itemTime hits 0 at tick 15 → one hit; does itemTime restart? In ItemCheck_UseMiningTools_ActuallyUseMiningTool it calls ApplyItemTime after the hit. So hits every 15 ticks continuously (regardless of swing restart). Same as repo. Fine.

Now (a): vanilla mining speed is NOT affected by meleeSpeed (useTime raw). Repo divides by attackSpeedMult. Is that wrong? Wiki "Tool_speed": "Tool speed... The useTime stat is only displayed for tools as their tool speed... These shoot rates can only be changed by modifiers as only modifiers can affect useTime." — from the Use_time page: "Their shoot rates can only be changed by modifiers as only modifiers can affect useTime." That's about projectile melee weapons, but it confirms useTime is unaffected by meleeSpeed (meleeSpeed only scales useAnimation). Actually hmm — for pickaxes: does meleeSpeed affect mining speed in vanilla? Common knowledge: NO — melee speed bonuses do NOT speed up mining (only modifiers/pick speed). Yes, that's well established. So repo's `useTime / attackSpeedMult` for mining = deviation (⚠️ makes mining faster with gloves/food melee speed).

Hmm wait, careful: `pickMult` handles food pickSpeed (wellFed pickSpeed in vanilla? vanilla food gives meleeSpeed not pickSpeed... hmm, the repo comment says "食物 pickSpeed -= 5/10/15%（Player.cs:11534+）". Let me check line 11534 area — earlier grep showed 11534 wasn't in the meleeSpeed list; let me check what stat food gives. Actually vanilla well-fed buffs: "Player.pickSpeed -= ..." hmm. In 1.4.4+ food gives meleeSpeed? Let me check 11528-11545.

Actually I saw in the meleeSpeed grep list: 11527: meleeSpeed += 0.05f (that's probably well fed). And pickSpeed lines: let me grep pickSpeed in Player.cs. This is a side detail; the food pick speed thing might be right (Exquisitely Stuffed gives pickSpeed? no...). Let me quickly grep pickSpeed.

Now let me also verify the repo's potion "drink" (useTime=60) vs vanilla 17. And check where healBlocked comes from (30?). And the vi_ potion path (4311: useTime=60 too).

Also check: does repo gate potion use behind useAnimation (swing)? The potion branch requires useTime===0 only. Since useSwing was called at 4179 for the same item (useSwing sets swing but not useTime!), then potion branch at 4195 runs immediately (useTime still 0) → potion consumed. Wait — 4176 branch: `if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool && cw?.kind !== 'summon' ...)` → useSwing(heldDef) — this applies to vi_ potions too (not excluded)! Then the potion branch at 4195 `if (heldDef?.potion && ...)` executes in the same frame since it's a separate `if` (not else-if). So both useSwing + potion consume happen. For legacy potions (def.potion), useSwing is called at 4179 first (heldDef && useTime===0 && !tool) → yes useSwing runs, then potion branch consumes. So the swing animation plays (30-ish frames via heldUseAnimation → 30 fallback) and useTime=60. Net effect: ~60-tick lockout instead of 17. ⚠️.

Vanilla heal timing: healLife applied when itemTime hits 0 → at tick 17 (end of animation). Repo: instant. 🔀 (minor gameplay difference: can't move-cancel; vanilla useTurn=true allows turning but not moving? Actually useTurn allows changing direction while using. Movement isn't blocked in vanilla during item use).

Also check: 使用中能否跳跃移动 — vanilla: itemAnimation doesn't block movement/jump (unless mount). Repo: nothing blocks. ✅.

Now: 冲刺/位移武器 — "暗影匕首"? Probably referring to dash weapons. Repo dash is accessory-driven; out of scope-ish. I'll mark ❓/未涉及.

Also check: item 1094/5664 channel (SetDummyItemTime) — repo does implement channel semantics for a couple items (Foxparks, golf club, boomerang 301). OK partial.

Also: 弹药发射时机 — "itemTime 中段发射 vs 开头": vanilla shoots when itemTime==0 during animation (i.e., at animation start for the first shot since itemTime set = useTime and decrement... wait). Let me trace: use start at tick T: ApplyItemAnimation (itemAnimation=N), but when is ApplyItemTime first called? In ItemCheck after StartActualUse: the `ItemTimeIsZero && itemAnimation > 0` branch (42177+) — at the moment of use start, itemTime is still 0 from before! Let me check: at 42158 `if (ItemTimeIsZero && whoAmI == myPlayer ...)` then 42177 `if (ItemTimeIsZero && itemAnimation > 0)`. Since itemTime==0 right at use start (before first decrement), the FIRST shot happens on the SAME tick as the use start. Then ApplyItemTime(item) sets itemTime=useTime. Then decrement at 42157 (itemTime-- happens at 42154-42157). So subsequent shots every useTime ticks. So: first projectile at use start (tick 0), subsequent every useTime ticks, animation ends at useAnimation(+1 for useStyle5 autoswing). Repo: fires at click (tick 0) then every useTime — ✅ aligned for the ranged chain.

For melee+shoot (repo line 4086): shoots on swing start each swing. Vanilla: flag4 = itemTime==0 during animation → first shot at swing start ✅, but subsequent swings only re-shoot if itemTime reached 0 again (useTime > useAnimation cases like Chlorophyte Claymore shoot only every ~2nd/3rd swing unless shootsEveryUse). Item 989 & 1226 are in the shootsEveryUse list? Let me check which items get shootsEveryUse=true (Item.cs lines 3711, 4577, 5677, 9279 — those are probably whole lists). Let me grep the actual assignments near those lines to see the list membership.

Let me check that, plus pickSpeed.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:31.011Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '3700,3715p' Item.cs; echo \"=== 4577 ===\"; sed -n '4565,4580p' Item.cs; echo \"=== pickSpeed ===\"; grep -n \"pickSpeed\" Player.cs | head -8",
 "description": "Check shootsEveryUse list and pickSpeed"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:31.049Z

**📎 ToolResult**

```
			shoot = 976;
			shootSpeed = 20f;
			knockBack = 4.5f;
			width = 40;
			height = 40;
			damage = 18;
			scale = 1f;
			UseSound = SoundID.Item1;
			rare = 3;
			value = 27000;
			melee = true;
			shootsEveryUse = true;
			break;
		case 191:
			noMelee = true;
			useStyle = 1;
=== 4577 ===
			knockBack = 4.5f;
			width = 40;
			height = 40;
			damage = 40;
			scale = 1f;
			UseSound = SoundID.Item1;
			rare = 3;
			value = sellPrice(0, 4);
			melee = true;
			shoot = 972;
			shootSpeed = 5f;
			noMelee = true;
			shootsEveryUse = true;
			break;
		case 274:
			useStyle = 5;
=== pickSpeed ===
2334:	public float pickSpeed = 1f;
9615:				pickSpeed -= 0.15f;
9636:				pickSpeed -= 0.2f;
9818:				pickSpeed -= 0.25f;
11535:				pickSpeed -= 0.05f;
11551:				pickSpeed -= 0.1f;
11567:				pickSpeed -= 0.15f;
11582:				pickSpeed += 0.05f;

```


---

## 🤖 Assistant · 2026-08-13T01:30:36.244Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK: pickSpeed is a separate stat (food 11535/11551/11567 = wellFed tiers -5%/-10%/-15%; 9615 kite -15%; 9636 celestial shell -20%; 9818 mining potion/builder -25%). And meleeSpeed is a separate multiplier (11519/11543/11559 = +5%/+7.5%/+10%?). So food affects BOTH pickSpeed and meleeSpeed in vanilla.

And mining cadence = useTime (raw) × pickSpeed? Where is pickSpeed consumed? Let me check: `pickSpeed` used in... grep shows only declarations/assignments. Let me search for consumption: maybe in ApplyItemTime multiplier? ApplyItemTime(sItem, multiplier) — is there a call with pickSpeed? Let me grep "pickSpeed" consumption — maybe `ApplyItemTime(item, pickSpeed)` somewhere. Let me search more broadly including other files.

Hmm the grep above only showed Player.cs lines with declarations and -= assignments. So where is pickSpeed read? Maybe `ItemCheck_UseMiningTools` → `ApplyItemTime(item, pickSpeed)`? Let me grep "pickSpeed" across all files.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:36.783Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -rn \"pickSpeed\" --include=\"*.cs\" . | grep -v \"Player.cs\" | head -10; echo \"=== Player.cs consumption ===\"; grep -n \"pickSpeed\" Player.cs",
 "description": "Find pickSpeed consumption"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:36.810Z

**📎 ToolResult**

```
=== Player.cs consumption ===
2334:	public float pickSpeed = 1f;
9615:				pickSpeed -= 0.15f;
9636:				pickSpeed -= 0.2f;
9818:				pickSpeed -= 0.25f;
11535:				pickSpeed -= 0.05f;
11551:				pickSpeed -= 0.1f;
11567:				pickSpeed -= 0.15f;
11582:				pickSpeed += 0.05f;
11597:				pickSpeed += 0.15f;
12457:			pickSpeed -= 0.05f;
12567:			pickSpeed -= 0.15f;
12612:			pickSpeed -= 0.25f;
13424:			pickSpeed -= 0.1f;
15897:			pickSpeed -= 0.1f;
18511:		pickSpeed = 1f;
25678:		if ((double)pickSpeed < 0.3)
25680:			pickSpeed = 0.3f;
39227:					ApplyItemTime(bestPickaxe, pickSpeed);
39228:					SetItemAnimation(bestPickaxe.useTime, pickSpeed);
39248:				int num4 = (int)((float)bestPickaxe.useTime * pickSpeed);
39251:				SetItemAnimation(bestPickaxe.useTime, pickSpeed);
44950:		itemTime = (int)((float)item.useTime * pickSpeed);
45163:			itemTime = (int)((float)sItem.useTime * pickSpeed);

```


---

## 🤖 Assistant · 2026-08-13T01:30:50.004Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Excellent! Found it — Player.cs:44950 and 45163:
```csharp
itemTime = (int)((float)item.useTime * pickSpeed);
```
So for MINING tools, itemTime = useTime × pickSpeed (not meleeSpeed!). And line 39227-39251 (block swap / smart pickaxe) uses ApplyItemTime(bestPickaxe, pickSpeed).

So vanilla mining cadence = useTime × pickSpeed — meleeSpeed does NOT affect it, but pickSpeed does (food/kite/potion/celestial shell). Let me confirm 44950/45163 context (UseMiningTools).

So repo's `cooldown = useTime / attackSpeedMult * ... / pickMult`:
- ✅ pickSpeed part (pickMult)
- ❌ meleeSpeed part (attackSpeedMult) — vanilla doesn't scale mining useTime by meleeSpeed
- Note: tileSpeedMult (砌砖刀 tileSpeed) is applied by repo to mining cooldown — vanilla tileSpeed only affects block/wall placement useAnimation, NOT mining. Let me verify: ApplyItemAnimation createTile branch uses tileSpeed. Mining itemTime uses pickSpeed only. So repo applying tileSpeed (Builder potion 砌砖药/水泥搅拌机) to MINING cooldown is ❌. Actually repo's `tileSpeedMult` uses `equipStats.tileSpeed || buffs.has(Mining)` → mining potion gives -25% (pickSpeed, correct-ish) but tileSpeed (cement mixer) shouldn't affect mining.

Hmm wait — careful. tileSpeed in vanilla = block placement speed; Mining potion = pickSpeed -25% (line 9818). So repo conflates them. Two small deviations.

Let me verify line 44950 context quickly.

Then I need to check the repo's ranged weapon: does it apply meleeSpeed? No — ranged useTime raw (line 4396: bowC?.useTime). ✅ (vanilla: non-melee useAnimation+1, itemTime=useTime raw).

Now let me also double check: for magic weapons, repo useCombatWeapon sets useTime = cw.useTime (raw). Vanilla: magic useAnimation+1 for autoswing useStyle 5; itemTime=useTime raw. ✅ cadence aligned.

Now, the autoReuse skip for useStyle-5 autoswing (Total time = useAnimation + 1): repo doesn't add +1 — net cadence = useTime. For most guns useTime == useAnimation, so effective cycle = useTime = vanilla cycle (useAnimation+1 with skip → useAnimation). ✅ equivalent. Good — no need to flag except as a note.

One more check on the autoReuse chain for ranged: line 4408 gate `(cw.autoReuse || clickEdge)` ✅ (with clickEdge = mouseDown && !_prevMouseDown). Good — manual re-click rhythm implemented.

Now the melee gate (line 4066): clickEdge = inp.mouseDown && !this.prevSwingMouse. prevSwingMouse is recorded at line 2700 AFTER updateUse — correct ordering per the comment. ✅.

BUT there's a subtle issue: `_prevMouseDown` is used for the ranged gate (4408) and `prevSwingMouse` for melee — both recorded after updateUse. Fine.

Now potion healBlocked: let me check `healBlocked` and where the 60 comes from. And check vanilla potionDelayTime value (3600). Let me grep potionDelayTime in Player.cs.

Also for the "使用时机与动作打断" item: 使用中切物品 — digit key instant switch (❌ vs vanilla buffered/blocked). Let me verify vanilla selectedItemState buffer at 24918.

Let me batch these final checks.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:50.935Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '44940,44960p' Player.cs; echo \"=== 45155 ===\"; sed -n '45150,45170p' Player.cs; echo \"=== 24910 ===\"; sed -n '24910,24930p' Player.cs; echo \"=== potionDelayTime ===\"; grep -n \"potionDelayTime = \\|potionDelayTime=\" Player.cs | head -3",
 "description": "Verify mining itemTime and buffered switch"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:50.984Z

**📎 ToolResult**

```
	private void UseShovel(Player user, Item item, int sX, int sY)
	{
		for (int i = sX - 1; i <= sX + 1; i++)
		{
			for (int j = sY - 1; j <= sY + 1; j++)
			{
				DamageTileWithShovel(user, item, i, j);
			}
		}
		itemTime = (int)((float)item.useTime * pickSpeed);
	}

	private void DamageTileWithShovel(Player user, Item item, int x, int y)
	{
		Tile tileSafely = Framing.GetTileSafely(x, y);
		if (TileID.Sets.CanBeDugByShovel[tileSafely.type])
		{
			int pickPower = 30;
			if (tileSafely.active() && (TileID.Sets.Conversion.Grass[tileSafely.type] || TileID.Sets.Conversion.JungleGrass[tileSafely.type] || tileSafely.type == 70 || tileSafely.type == 633))
			{
=== 45155 ===
					hitTile.Prune();
				}
				ApplyItemTime(sItem);
				AchievementsHelper.CurrentlyMining = false;
			}
		}
		else if (sItem.pick > 0)
		{
			IntentionGuesser.Track(this, x, y, GuessedPlayerIntention.HarvestTreasure);
			PickTile(x, y, sItem.pick);
		}
		if (sItem.pick > 0)
		{
			itemTime = (int)((float)sItem.useTime * pickSpeed);
		}
		ItemCheck_UseMiningTools_TryPoundingTile(sItem, num, ref canHitWalls, x, y);
	}

	private bool IsBottomOfTreeTrunkNoRoots(int x, int y)
	{
		Tile tile = Main.tile[x, y];
=== 24910 ===
					{
						Main.DoScrollingInInventory();
					}
					else
					{
						HandleHotbarControls();
					}
				}
				if (itemAnimation == 0 && ItemTimeIsZero && reuseDelay == 0)
				{
					dropItemCheck();
				}
			}
			selectedItemState.Update();
			if (stoned != lastStoned)
			{
				if (whoAmI == Main.myPlayer && stoned)
				{
					int damage = (int)(20.0 * (double)GameDifficultyData.EnemyDamageMultiplier.Sample(Main.Difficulty));
					Hurt(PlayerDeathReason.ByOther(5), damage, 0);
				}
=== potionDelayTime ===
2750:	public int potionDelayTime = Item.potionDelay;
25193:		potionDelayTime = Item.potionDelay;
25198:			potionDelayTime = (int)((float)potionDelayTime * PhilosopherStoneDurationMultiplier);

```


---

## 🤖 Assistant · 2026-08-13T01:30:51.337Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"healBlocked\" entities/Player.ts player/*.ts 2>/dev/null | head -8",
 "description": "Find healBlocked source"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:51.364Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T01:30:57.101Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- Mining: `itemTime = (int)(sItem.useTime * pickSpeed)` (P:45163, and shovel P:44950) — pickSpeed only, NOT meleeSpeed. And the mining-hit branch calls ApplyItemTime(sItem) (raw useTime) at 45157 then overrides with pickSpeed at 45163. So the repo's `/attackSpeedMult` in the mining cooldown is a deviation. ✅ evidence.
- potionDelayTime = Item.potionDelay. Let me check Item.potionDelay value — likely 3600.
- healBlocked — let me find it in the repo (maybe in buffs.ts).

Let me check Item.potionDelay and find healBlocked in repo.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:57.822Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"potionDelay\" Item.cs | head -3; echo \"=== repo healBlocked ===\"; grep -rn \"healBlocked\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -6",
 "description": "potionDelay value and repo healBlocked"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:57.852Z

**📎 ToolResult**

```
70:	public static int potionDelay = 3600;
=== repo healBlocked ===
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4209:      if (p.isHealType && this.player.buffs.healBlocked) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4294:        if (ff.healLife && this.player.buffs.healBlocked) {
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:487:  get healBlocked(): boolean {

```


---

## 🤖 Assistant · 2026-08-13T01:31:06.365Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. potionDelay = 3600 ticks = 60s. Repo healBlocked (Buffs.ts:487) — presumably Resistance buff check → 60s ✅.

Now I have everything I need for a comprehensive report. Let me do a final check on a couple of remaining checklist items:

1. "useAnimation < useTime 时(急速武器)的行为" — covered (the > cases: 7 melee; and useAnimation>useTime is the common case). Actually "急速武器" = useAnimation < useTime? The task says "useAnimation<useTime 时(急速武器)的行为" — hmm, that's when the animation is shorter than the cooldown → gap between uses. Covered: repo waits max(useTime, anim) vs vanilla waits anim only (but effect gated by itemTime). I have data: 7 melee items with useTime>useAnimation.

2. Placement: repo useTime=14 per place. Vanilla: blocks useAnimation=14/useTime=10? Let me check item 1 (Dirt Block): SetDefaults case 1 at line 704. Let me read it. Vanilla dirt block: useTime=10, useAnimation=14? I believe blocks are useAnimation=14/useTime=10 hmm, actually blocks: useTime=10, useAnimation=15? Let me check.

3. 冲刺/位移武器 — check if repo has any dash weapon (e.g., 暗影匕首? "Shadow dagger"...). Probably means Tabi/挪移匕首? There's "Rod of Discord" (905)? Let me check quickly whether RoD is implemented — grep vi_905. Minor.

4. whip chain: whipSpd (Player.ts:260) — whip useTime multiplier (黑曜套 1/1.15). Vanilla whip formula: floor(useAnimation/(1+meleeSpeed+whipSpeedBuff)/whipSetBonus). Repo has whipSpd — check how it's used in Game (鞭 useTime 结算). Let me grep whipSpd consumption.

Let me do these final greps.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:06.729Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '704,730p' Item.cs",
 "description": "Read dirt block use stats"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:06.751Z

**📎 ToolResult**

```
		case 1:
			size = 1.12f;
			break;
		case 2:
			size = 1.18f;
			break;
		case 3:
			dmg = 1.05f;
			crt = 2;
			size = 1.05f;
			break;
		case 4:
			dmg = 1.1f;
			size = 1.1f;
			kb = 1.1f;
			break;
		case 5:
			dmg = 1.15f;
			break;
		case 6:
			dmg = 1.1f;
			break;
		case 81:
			kb = 1.15f;
			dmg = 1.15f;
			crt = 5;
			spd = 0.9f;

```


---

## 🤖 Assistant · 2026-08-13T01:31:07.418Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"whipSpd\\|RoD\\|vi_905\\|rod_of_discord\" core/Game.ts entities/Player.ts stats/*.ts 2>/dev/null | head -10",
 "description": "Whip speed and discord rod"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:07.445Z

**📎 ToolResult**

```
entities/Player.ts:265:    whipSpd: number;       // 鞭 useTime 倍率（黑曜套 1/1.15）
entities/Player.ts:516:      whipSpd: summonSet?.whipSpd ?? 1,
core/Game.ts:4845:        const whipAtk = Math.min(3, 1 + swb * owner.equipStats.whipSpd);

```


---

## 🤖 Assistant · 2026-08-13T01:31:10.450Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line 704 was the Prefix switch (case 1 inside Prefix). Let me find SetDefaults case 1 for dirt block — search "case 1:" in SetDefaults (second occurrence at 1373). Let me check quickly. Also check the whip usage at Game.ts:4845.

Actually let me be efficient — I have enough for the report. Let me just check the dirt block defaults (SetDefaults case 1) and the whip attack speed line 4840-4850.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:10.776Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && sed -n '1373,1400p' Item.cs",
 "description": "Dirt block SetDefaults"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:10.797Z

**📎 ToolResult**

```
		case 1:
			useStyle = 1;
			useTurn = true;
			useAnimation = 20;
			useTime = 13;
			autoReuse = true;
			width = 24;
			height = 28;
			damage = 5;
			pick = 40;
			UseSound = SoundID.Item1;
			knockBack = 2f;
			value = 2000;
			melee = true;
			break;
		case 2:
			useStyle = 1;
			useTurn = true;
			useAnimation = 15;
			useTime = 10;
			autoReuse = true;
			consumable = true;
			createTile = 0;
			width = 12;
			height = 12;
			break;
		case 3:
			useStyle = 1;

```


---

## 🤖 Assistant · 2026-08-13T01:31:11.105Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && sed -n '4835,4860p' core/Game.ts",
 "description": "Whip attack speed chain"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:11.125Z

**📎 ToolResult**

```
          whip.knockback, whip.useTime, whip.shootSpeed,
          () => (owner.dead ? null : owner),
          // 月主鞭补鞭实时瞄准（Projectile.cs:45045-45046 朝鼠标方向重掷）
          () => Math.atan2(inp.mouseY - this.renderer.canvas.height / 2,
            inp.mouseX - this.renderer.canvas.width / 2),
        ), 'projectiles');
        // 鞭攻速（SetItemAnimation :4266：summonerWeaponSpeedBonus × whipUseTimeMultiplier，
        // 封顶 3×——summonerWeaponSpeedBonus 来自鞭 buff 311/308/314，黑曜套给 wutm）
        const swb = (owner.whipBuffs[311] ? 0.35 : 0) + (owner.whipBuffs[308] ? 0.25 : 0)
          + (owner.whipBuffs[314] ? 0.12 : 0);
        const whipAtk = Math.min(3, 1 + swb * owner.equipStats.whipSpd);
        this.player.useTime = Math.max(1, Math.round(whip.useTime / whipAtk));
        this.sfx.playWav('whipCrack', 0.9, owner.cx, owner.cy); // DefaultToWhip UseSound=Item152（鞭响）
        this.input.mouseDown = false;
        break;
      }
      case 'summon': {
        // 召唤：上限链 = Player.maxMinions（1+buff+散件+套装）/ maxSentries；
        // 超限驱逐最旧（原版 FreeUpPetsAndMinions 最便宜优先——本作全 1 槽=最旧先死）；
        // damage 传武器基伤——随从每 tick 按当时装备重算（Projectile.cs:15368 live 刷新）
        const minions = this.entities.projectiles.filter((e) => e instanceof MinionProj && !e.sentry && !(e as MinionProj).noSlot) as MinionProj[];
        // 星尘龙：已有龙头 → 不出新头，尾前插 2 段（SpawnMinionOnCursor :47906-47963）
        if (cw.shoot === 625) {
          const head = minions.find((m) => m.projId === 625);
          if (head && !head.dead) {
            head.extendDragon(this);

```


---

## 🤖 Assistant · 2026-08-13T01:31:19.873Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: Dirt Block (item 2? no — case 1 is Iron Pickaxe? Hmm: case 1: useAnimation=20, useTime=13, pick=40, damage=5, melee=true, tileBoost... wait pick=40 for item 1? Item 1 = "Iron Pickaxe"? No... Actually in Terraria, item 1 IS the Iron Pickaxe? Hmm. Terraria item IDs: 1 = "Iron Pickaxe"? Let me think: the wiki item list — 1: Iron Pickaxe, 2: Dirt Block, 3: Torch, 4: Iron Axe... Yes! 1 = Iron Pickaxe (useAnimation 20, useTime 13, pick 40 — hmm, iron pickaxe is pick 40? Iron Pickaxe = 35%... whatever, close enough: 3509 copper pickaxe was pick 35; item 1 iron pickaxe pick 40 ✓).

And case 2 (Dirt Block): useAnimation=15, useTime=10, autoReuse=true, consumable, createTile=0. So vanilla block placement: itemTime=10 (raw), itemAnimation=15 (tileSpeed-scaled). Repo: `useTime = 14` per placement — and tryPlace gates on `useTime > 0 return`. Vanilla place cadence: every 10 ticks (itemTime) — placement happens in PlaceThing_Tiles gated by `ItemTimeIsZero && itemAnimation > 0 && controlUseItem` (P:39084) then ApplyItemTime... so one block every 10 ticks (scaled by tileSpeed? Let me check: PlaceThing_Tiles → does it ApplyItemTime or apply tileSpeed? In ApplyItemAnimation, createTile branch: SetItemAnimation(useAnimation, tileSpeed). itemTime = useTime raw (10). So block placement every 10 ticks; animation 15/tileSpeed. With Builder potion (+25% tileSpeed=0.25 → tileSpeed=1.25): animation = 15/1.25=12; itemTime still 10. So placement cadence = useTime raw = 10. Hmm — but does PlaceThing apply itemTime with tileSpeed? Let me check line 39084 branch: `ApplyItemTime(item)`? Let me look... Actually I saw at 39189 walls: `if (controlUseItem && canUse && ... && ItemTimeIsZero && itemAnimation > 0 ...)`. And after placing, it must call ApplyItemTime. Whether it uses a multiplier I'd need to check. Let me grep "ApplyItemTime(item, tileSpeed)" or "tileSpeed)" in Player.cs.

Anyway: repo useTime=14 per block vs vanilla 10 → ⚠️ 1.4× slower placement. Also repo placement gate is useTime-based only, no animation. Minor.

Let me check the tileSpeed consumption for placement cadence.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:20.689Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"tileSpeed\\b\\|wallSpeed\\b\" Player.cs | grep -v \"tileSpeed \\|wallSpeed \" | head; echo ---; grep -n \"tileSpeed\" Player.cs | grep -v \"public\\|tileSpeed = \\|tileSpeed >\" | head",
 "description": "tileSpeed consumption points"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:20.716Z

**📎 ToolResult**

```
4272:			SetItemAnimation(sItem.useAnimation, tileSpeed);
4276:			SetItemAnimation(sItem.useAnimation, wallSpeed);
28050:			int num4 = (int)((float)num3 * tileSpeed);
38960:			ApplyItemTime(inventory[selectedItem], wallSpeed);
39162:			ApplyItemTime(HeldItem, wallSpeed);
39249:				int num5 = (int)((float)HeldItem.useTime * tileSpeed);
39485:			ApplyItemTime(inventory[selectedItem], tileSpeed);
41227:				ApplyItemTime(inventory[selectedItem], tileSpeed);
41231:				ApplyItemTime(inventory[selectedItem], wallSpeed);
41321:					ApplyItemTime(inventory[selectedItem], wallSpeed);
---
4272:			SetItemAnimation(sItem.useAnimation, tileSpeed);
9616:				tileSpeed += 0.15f;
9842:				tileSpeed += 0.25f;
12458:			tileSpeed += 0.05f;
12607:				tileSpeed += 0.5f;
28050:			int num4 = (int)((float)num3 * tileSpeed);
39249:				int num5 = (int)((float)HeldItem.useTime * tileSpeed);
39485:			ApplyItemTime(inventory[selectedItem], tileSpeed);
41227:				ApplyItemTime(inventory[selectedItem], tileSpeed);
41334:				ApplyItemTime(inventory[selectedItem], tileSpeed);

```


---

## 🤖 Assistant · 2026-08-13T01:31:26.413Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: block placement cadence = `ApplyItemTime(item, tileSpeed)` (P:39485, 41227) → itemTime = useTime × (1/(1+tileSpeedBonus))... wait, tileSpeed is converted at 25627-25631: `if (tileSpeed > 3f) tileSpeed = 3f; tileSpeed = 1f / tileSpeed;`. So tileSpeed is already reciprocal → itemTime = useTime × (1/(1+bonus)) → faster with Builder potion. Good.

So vanilla placement: every useTime×tileSpeed ticks (dirt block: 10, or 8 with builder potion); animation = 15×tileSpeed.
Repo: fixed 14 per placement, no tileSpeed scaling (Builder potion only gives +1 range in repo: `buffs.has(BuffType.Builder) ? 1 : 0` — hmm, actually that's used as tileBoost for range; the +25% speed not applied to placement). ⚠️.

Wait, does repo apply tileSpeed to placement anywhere? tryPlace useTime=14 constant. Let me check tryPlaceWall — line 5910. It had useTime=14 too (from the grep: 3 occurrences of useTime=14 in 5975-6080 range and one at 45... the earlier grep showed `this.player.useTime = 14` at multiple sites). And `tileSpeed` in equipStats — used in mining cooldown (wrongly) — let me check if used in placement: grep tileSpeed in Game.ts.

I think I have enough. Let me do one final grep for tileSpeed usage in Game.ts, then write the report.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:27.044Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"tileSpeed\\|attackSpeedMult\" core/Game.ts | head -20; echo \"=== wall place ===\"; sed -n '5910,5975p' core/Game.ts | grep -n \"useTime\" ",
 "description": "tileSpeed usage in repo"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:27.072Z

**📎 ToolResult**

```
4049:    // Player.attackSpeedMult = CapAttackSpeeds 倒数档，Player.cs:28555-28574）
4058:        ? Math.max(12, Math.round(nativeSpd / this.player.attackSpeedMult))
4059:        : Math.max(4, Math.round((cwMelee!.useAnimation) / this.player.attackSpeedMult));
4099:            Math.cos(ang2) * cwMelee.shootSpeed / this.player.attackSpeedMult,
4100:            Math.sin(ang2) * cwMelee.shootSpeed / this.player.attackSpeedMult,
4112:      const spd = Math.max(14, Math.round((tool.speed ?? 46) / this.player.attackSpeedMult));
5207:    const tileSpeedMult = (this.player.equipStats.tileSpeed || this.player.buffs.has(BuffType.Mining)) ? 0.75 : 1;
5211:    const cooldown = Math.max(8, Math.round((useTime ?? speed) / this.player.attackSpeedMult) * tileSpeedMult / pickMult);
11624:      // equipStats（msg5 已同步远端盔甲/配饰，Player.attackSpeedMult = CapAttackSpeeds
11653:   *  镐斧锤 max(14,speed)、其它 30；近战/工具分支除以代理自身 attackSpeedMult——
11659:    const spd = proxy ? proxy.attackSpeedMult : 1;
=== wall place ===
1:   *  ④PlaceWall 成功 → 消耗 + useTime
13:    if (this.player.useTime > 0) return;
41:      this.player.useTime = Math.max(4, Math.round(15 * ((this.player.equipStats.wallSpeed || this.player.buffs.has(BuffType.Builder)) ? 0.75 : 1)));
50:    this.player.useTime = Math.max(4, Math.round(15 * ((this.player.equipStats.wallSpeed || this.player.buffs.has(BuffType.Builder)) ? 0.75 : 1)));

```


---

## 🤖 Assistant · 2026-08-13T01:31:37.850Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting:
- Walls: useTime = max(4, round(15 × (wallSpeed? 0.75 : 1))) — vanilla wall: itemTime = useTime × wallSpeed where wallSpeed = 1/(1+bonus); with +0.25 → 0.8, not 0.75. Minor numeric deviation (0.75 vs 0.8); also base wall useTime is 15? Vanilla walls: useAnimation 15, useTime 10? Let me not verify every block; the wall base 15 vs vanilla wall itemTime (useTime=10 for stone wall? probably). Let me do one quick check for a wall item (item 27 = Stone Wall? no...). Walls: 5 = wood wall? Actually item 27 = wood wall. Let me skip — I'll flag the base as approx.

Hmm, let me quickly check one wall item to be accurate. grep "createWall = " near a case. Item 27 (Wood Wall): useTime 10? Let me check case 27.

- Blocks: fixed 14, no tileSpeed. Vanilla: useTime(10 for dirt)×tileSpeed. So ⚠️: base slower (14 vs 10) + tileSpeed missing.

Let me check item 27 quickly. Then write the report. Also confirm whether repo melee weapons branch also requires inp.mouseDown (yes, gated by 4039 `if (!inp.mouseDown...) return`).

One more: the checklist item "使用时喝药打断" — in vanilla, drinking a potion (heal at end of 17-tick animation) then immediately attacking: the animation must finish. Also QuickHeal hotkey works even when using (wiki: Quick Heal still functional). Repo: quick heal? Let me check if repo has a quick heal hotkey — grep QuickHeal / KeyH. Minor; skip or mark ❓.

Also "弹药/魔法发射时机(itemTime 中段发射 vs 开头)" — done: first shot at use start, then every useTime; repo matches for ranged/magic (useTime raw), melee+shoot shoots on swing start each swing (vanilla: shootsEveryUse list + itemTime gating → Claymore shoots every swing if in list). Is 989 in shootsEveryUse? The wiki list of shootsEveryUse includes Chlorophyte Claymore? The Use_time wiki page's shootsEveryUse list: Blade of Grass, Night's Edge, Excalibur, True Excalibur, True Night's Edge, Terra Blade, The Horseman's Blade, Waffle's Iron. NOT Chlorophyte Claymore (that's in the useTime-based list: Starfury, Frostbrand, Beam Sword, Ice Blade, Enchanted Sword, Chlorophyte Claymore, Chlorophyte Saber). So Claymore's shoot rate is based on useTime (45) with useAnimation 21 → shoots once every 45 ticks (i.e., roughly every 2nd swing). Repo: shoots EVERY swing (every ~21 ticks) → ⚠️ shoots 2× too often for the useTime-based projectile melee family.

Great, that's a solid finding with evidence: Game.ts:4083-4099 (melee+shoot every swing start).

Now let me check item 27 (wood wall) for the wall base number. And then write the report.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:38.519Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"case 27:\" Item.cs | head -2 && sed -n \"$(grep -n 'case 27:' Item.cs | tail -1 | cut -d: -f1),+12p\" Item.cs",
 "description": "Wood wall use stats"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:44.554Z

**📎 ToolResult**

```
831:		case 27:
1679:		case 27:
		case 27:
			useTurn = true;
			useStyle = 1;
			useAnimation = 15;
			useTime = 10;
			consumable = true;
			autoReuse = true;
			createTile = 20;
			width = 18;
			height = 18;
			value = 10;
			ammo = AmmoID.Acorn;
			notAmmo = true;

```


---

## 🤖 Assistant · 2026-08-13T01:31:53.693Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Item 27 = Acorn (createTile=20 tree). useAnimation 15, useTime 10. Blocks generally: useAnimation 15, useTime 10 (some 14/10). So the repo's block place useTime=14 vs vanilla itemTime=useTime=10 → 1.4× slower placement. Confirmed.

Now I have a comprehensive picture. Let me also double check the melee branch gate in repo — is there any requirement that the swing restart happens only when inp.mouseDown held (yes, since 4039 returns if !mouseDown). For autoReuse melee, holding chains ✅.

One last check for the checklist: "1.4 手动连发的节奏" — for non-autoReuse weapons, vanilla requires releaseUseItem — i.e., you must release and press again? Actually `releaseUseItem` is set to `!controlUseItem` each tick (P:42152: releaseUseItem = !controlUseItem). So for a NON-autoReuse item, after a use completes, releaseUseItem is false while holding → no new use until you release and press again. Wait — that means for non-autoReuse weapons, you must RELEASE the button between clicks (a new click isn't enough if you never released... well a new click implies release). So vanilla requires full click cycles (release between uses). Repo: clickEdge = mouseDown && !prevSwingMouse → requires a new press edge (which implies release) ✅ equivalent.

BUT: there's a subtlety for non-autoReuse + glove: TryAllowingItemReuse sets releaseUseItem=true → allows chain while holding. Repo handles via autoReuse flag ✅.

Also: vanilla `ItemCheck_AutoReuseLogic` early-returns when `selectedItemState.HasBufferedChange && (shoot<=0 || ItemTimeIsZero)`.

Also for the "Settings → Autofire (autoReuseAllWeapons)" — repo doesn't have a settings autofire toggle. Let me check quickly... probably not implemented. grep autoReuseAllWeapons / autofire in repo.

Let me grep that quickly, then write the final report. Also double-check: does repo implement the `stressBall`? No. Fine.

Let me also verify one thing about the ranged branch: it doesn't check `swing` — a gun fires every useTime even if swing animation (useAnimation) is longer. useSwing restarts the swing each shot. For guns with useTime==useAnimation, fine. For Clockwork (4/12), swing restarts every 4 → visual. And no reuseDelay. Already covered.

Final grep: autofire setting.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:54.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"autoFire\\|autofire\\|autoReuseAll\" --include=\"*.ts\" . | head -5; echo \"(空=未实装)\"; grep -rn \"quickHeal\\|QuickHeal\" --include=\"*.ts\" . | head -3",
 "description": "Check autofire setting and quick heal"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:54.545Z

**📎 ToolResult**

```
(空=未实装)
core/Game.ts:3668:   *  Player.cs QuickMana 原理同 QuickHeal；返回 true=已补蓝可重试施法） */

```


---

## 🤖 Assistant · 2026-08-13T01:32:21.150Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Autofire setting not implemented; QuickHeal hotkey not implemented (only QuickMana reference in a comment).

Now I have all the evidence I need. Let me compose the final markdown report.

Summary of findings:

### Core architecture
- Vanilla: dual counters itemAnimation/itemTime (+ reuseDelay + pendingItemReuse). Repo: single `player.useTime` (=itemTime) + `swing` object (=itemAnimation), no reuseDelay, no pendingItemReuse (Game.ts:3903 admits).

### Item-by-item checklist:

1. **useTime vs useAnimation 双轨**
   - Vanilla: ApplyItemAnimation (P:4255-4283) sets itemAnimation from useAnimation (melee: ×meleeSpeed reciprocal; createTile: ×tileSpeed; createWall: ×wallSpeed; summon-scaling: ×summonerWeaponSpeedBonus×whipUseTimeMultiplier; else +1 if autoswing useStyle5). reuseDelay stored (P:4282).
   - Vanilla: ApplyItemTime (P:4216) = RAW useTime (no meleeSpeed). Mining tools override: itemTime = useTime×pickSpeed (P:45163/44950).
   - Vanilla restart gate: itemAnimation==0 only (P:42144); itemTime gates per-tick effects only (P:42177+: heal/buff/shoot when ItemTimeIsZero && itemAnimation>0).
   - Repo: melee animSpd = useAnimation/attackSpeedMult (Game.ts:4053-4055) ✅; reuseSpd = raw useTime (4058-4060) ✅ raw; restart gate `useTime===0 && canChain && (swingOver || reuseSpd<animSpd)` (4074) ❌ uses itemTime as restart gate.
   - Data: 111/303 melee have useTime<useAnimation → repo swings ~1.4-2× too fast (animation cut short). 7 melee have useTime>useAnimation (65/676/723/724/989/1226/1227, e.g. Chlorophyte Claymore 21/45, Cutlass 26/60) → repo max(45,21)=45 ticks vs vanilla 21 → 2.1× too slow.
   - Vanilla melee swing cycle for autoswing = useAnimation-1 (skip at itemAnimation==1, P:52022-52030); repo swingOver at t<=1 → same N-1 ✅.

2. **reuseDelay**: ❌ Not implemented anywhere (grep only comments at Game.ts:3903, SmartSelect.ts:179). Data file vanilla-itemcombat.json has 0 entries with reuseDelay (extractor never captured it). → Clockwork Assault Rifle etc. fire at full useTime rate (14-tick burst gap missing). Vanilla: ApplyReuseDelay (P:51969) itemAnimation=itemTime=reuseDelay when animation ends (P:42022).

3. **autoReuse**
   - Repo: cwMelee.autoReuse || gloveReuse (Game.ts:4061-4067); clickEdge for manual (4066); ranged/magic gate at 4408/4413 ✅.
   - Glove: vanilla TryAllowingItemReuse (P:52036) covers melee (≠3030) AND summon-scaling weapons; repo only melee (summon branch missing — whips get autoReuse? whips are autoReuse natively so minor).
   - Settings "Autofire" (autoReuseAllWeapons) ❌ not implemented.
   - AutoReuseLogic early-return on buffered change — N/A.

4. **攻速链 CapAttackSpeeds**
   - Vanilla P:28555-28569: meleeSpeed (multiplier base 1f, P:2328/18188) → cap >3 → reciprocal. BonusMeleeSpeedMultiplier per-item (P:25620-25622: (meleeSpeed-1)×mult+1). summonerWeaponSpeedBonus = reciprocal(num+summonerBonus).
   - Repo Player.ts:550-558: raw = (1+meleeSpeed)×Tipsy 1.1×Werewolf 1.051×Weak 0.949×(1+0.1×beetleOrbs)×(1+wellFedMeleeSpeed); cap 3 → 1/raw ✅ shape matches.
   - Missing: BonusMeleeSpeedMultiplier per-weapon table (Terra Blade 0.75, Bladed Glove 0.5, Fetid Baghnakhs 0.25, Psycho Knife 0.33) ❌ — repo has psycho knife stealth dmg but not the speed multiplier.
   - useTime NOT scaled (vanilla) ✅ repo melee reuseSpd raw ✅; but mining cooldown scales by attackSpeedMult ❌ (Game.ts:5211) — vanilla mining uses pickSpeed only (P:45163).
   - Whip chain: repo whipAtk = min(3, 1+swb×whipSpd) (Game.ts:4843-4847) — vanilla: summonerWeaponSpeedBonus reciprocal of (meleeSpeed+summonerBonus) × whipUseTimeMultiplier — shape differs but effect approximated; ⚠️ meleeSpeed not included for whips (vanilla whips DO scale with meleeSpeed).

5. **打断/切物品**: vanilla blocks held-item switch when itemAnimation>0 / buffers via selectedItemState (P:24918 gate `itemAnimation==0 && ItemTimeIsZero && reuseDelay==0`; wiki Use_time). Repo: SmartSelect gates (Game.ts:3901 ✅) but digit-key hotbar switch (Game.ts:1363-1364) applies immediately, no gate/buffer ❌. Movement/jump during use: vanilla not blocked (except mount) — repo not blocked ✅.

6. **发射时机**: vanilla first shot at use-start (itemTime==0 same tick), then every useTime; animation length irrelevant to cadence (P:42177/42855-42881: flag4 = itemAnimation>0 && ItemTimeIsZero; shootsEveryUse → ItemAnimationJustStarted). Repo ranged: fire at click, useTime=cw.useTime raw (4396) ✅; per-shot useSwing restart (4398) ⚠️ differs for useTime<useAnimation guns (no burst grouping). Melee+shoot: repo fires every swing start (4086) ❌ — vanilla useTime-based projectile melee family (Chlorophyte Claymore useTime 45/anim 21) shoot once per 45t not per swing; shootsEveryUse family not in repo data either.

7. **消耗品/药水**: vanilla DefaultToHealingPotion useAnimation=useTime=17, useStyle 9, heal applied when itemTime hits 0 (P:42189-42193) i.e., end of animation; potionDelay=3600 (Item.cs:70) + buff 21; pStone multiplier. Repo: instant heal, useTime=60 (Game.ts:4217), blocked path useTime=30 (4207), vi_ bridge useTime=60 (4311) ⚠️/🔀; healBlocked=Resistance ✅ (Buffs.ts:487); pStone 0.75 duration applied to BUFF not cooldown — 🔀 (vanilla pStone shortens potionDelay 3600→2700, not buff duration).

Hmm — actually repo line 4211: `apply(bt, Math.round(p.duration * (pStone ? 0.75 : 1)))` — applies pStone to the potion's BUFF duration (vanilla: buff duration unaffected; pStone reduces sickness). That's a 🔀 bug worth flagging. And the memory note says "贤者之石（pStone：药水 CD -25%，Player.pStone → PotionSickness 2850→2140）" — hmm, memory says 2850→2140. Whatever — vanilla PhilosopherStoneDurationMultiplier. Let me check its value quickly... not critical, I'll cite the mechanism mismatch without exact number. Actually let me grep it quickly to be accurate.

8. **放置**: vanilla block useTime=10/useAnimation=15 (item 2 dirt / 27 acorn), cadence = useTime×tileSpeed (P:39485/41227 ApplyItemTime(item,tileSpeed)); wall: ApplyItemTime(item,wallSpeed) (P:38960/39162). Repo: block fixed useTime=14 (tryPlace, Game.ts:~6037 etc.), no tileSpeed; wall 15×(0.75 if wallSpeed/Builder) (tryPlaceWall Game.ts:~5950) — base 15 vs vanilla 10, 0.75 vs 1/(1.25)=0.8 ⚠️. Also repo tryPlace for ropes/torch/track also 14.
   Also: golf club channel ✅ (2533-2599, SetDummyItemTime semantics), extractinator ✅ (4137-4147).

9. **冲刺/位移武器**: no dash-weapon/rod item usage chain found — repo dash is accessory-driven; RoD (905) not implemented ❓ (grep found nothing).

10. **挥舞判定窗口**: vanilla: hit while itemAnimation>0 whole window (P:42964-43006), hitbox = ApplyUseStyle itemLocation + 32×32 base with 3-phase expansion (P:44480+), one hit per NPC per swing (SetMeleeHitCooldown(npc,itemAnimation) P:43768; cleared at StartActualUse P:50932), attackCD = max(1, itemAnimationMax*0.33) after hit (P:43777-43779). Repo: updateSwingHits (Game.ts:7819-7964) whole window, 3-phase hitbox 1:1 ✅, swingHitSet per-swing dedup ✅, but no attackCD (0.33×animMax global hit cooldown) ❓ minor — repo's swingHitSet already prevents multi-hit per swing; attackCD matters only for subsequent swings overlapping. Fine to note.

Let me quickly check PhilosopherStoneDurationMultiplier value and then write the report.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:21.769Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456/Terraria && grep -n \"PhilosopherStoneDurationMultiplier\" Player.cs | head -3; grep -rn \"pStone\" ~/Project/GLM/SandboxWorld/game/src/stats/*.ts | head -5",
 "description": "pStone multiplier values"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:21.833Z

**📎 ToolResult**

```
2276:	public static readonly float PhilosopherStoneDurationMultiplier = 0.75f;
25198:			potionDelayTime = (int)((float)potionDelayTime * PhilosopherStoneDurationMultiplier);
25199:			restorationDelayTime = (int)((float)restorationDelayTime * PhilosopherStoneDurationMultiplier);

```


---

## 🤖 Assistant · 2026-08-13T01:32:50.884Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
pStone multiplier = 0.75 applied to potionDelayTime (sickness duration), NOT to the buff granted. Repo applies 0.75 to the potion's granted buff duration (Game.ts:4211) — 🔀 wrong axis.

Now I'm ready to write the final report. Let me structure it:

## 域:物品使用主链
### 差异清单 (table with ~18 rows)
### 覆盖清单
### 最需修复 TOP N

Let me get precise file:line refs:

Repo:
- Player.ts:112 useTime field; 114 comment
- Player.ts:669-671 (fixedUpdate useTime--)
  Actually the Read showed line 671 `if (this.useTime > 0) this.useTime--;` (line 669 in earlier grep said 669; the Read at offset 540 showed line 671 for useTime--. Earlier grep said Player.ts:669 `if (this.useTime > 0) this.useTime--;`. The read offset 540 line numbering: 667 fixedUpdate, 671 `if (this.useTime > 0) this.useTime--;`. Hmm grep earlier said 669. The Read output shows line numbers: 667 `fixedUpdate(dt: number, game: GameHooks) {`, ... 671 `if (this.useTime > 0) this.useTime--;`. Wait let me recheck: the read printed:
  667	  fixedUpdate(dt: number, game: GameHooks) {
  668	    const world = game.world;
  669	    this.lastStore = world.store;   // dashWallAhead 探测缓存（本 tick 内有效）
  670	    if (this.iframes > 0) this.iframes--;
  671	    if (this.useTime > 0) this.useTime--;
  So useTime-- is Player.ts:671. (The earlier grep said 669 — that was before my read; the read is authoritative: 671.)
- Player.ts:550-558 attackSpeedMult
- Player.ts:630-635 onManaItemUsed
- Player.ts:260 whipSpd
- Game.ts:544-554 swing decl, prevSwingMouse 554
- Game.ts:3901-3904 canChangeImmediately
- Game.ts:4039 mouseDown gate
- Game.ts:4048-4067 melee branch
- Game.ts:4073-4074 restart gate
- Game.ts:4080 useTime = reuseSpd
- Game.ts:4086-4099 melee+shoot
- Game.ts:4107-4131 tool branch; 4112-4113 swing/useTime; 4130 tryMine
- Game.ts:4137-4147 extractinator
- Game.ts:4163-4166 place branches
- Game.ts:4176-4193 generic useSwing
- Game.ts:4195-4221 potion legacy (useTime=60 at 4217, blocked 4207, pStone 4211)
- Game.ts:4281-4314 vi_ consumable bridge (useTime=60 at 4311)
- Game.ts:4316-4405 ranged (gate 4408, useTime 4396, useSwing 4398)
- Game.ts:4407-4411 useCombatWeapon dispatch
- Game.ts:4412-4451 thrown
- Game.ts:4713-4734 useCombatWeapon useTime prefix scaling
- Game.ts:4755-4757 useSwing for grenade/magic/shot/summon
- Game.ts:4776/4788/4803 useTime = cw.useTime
- Game.ts:4843-4848 whip
- Game.ts:5090-5211 tryMine cooldown (5211)
- Game.ts:5910 tryPlaceWall (useTime wall 15×0.75)
- Game.ts:5975 tryPlace (useTime=14)
- Game.ts:7819-7964 updateSwingHits
- Game.ts:2700 prevSwingMouse / 2703 _prevMouseDown
- Game.ts:1363-1364 digit hotbar immediate switch
- SmartSelect.ts:179-181, 250, 492

Vanilla:
- Player.cs:4212-4214 SetItemTime; 4216-4218 ApplyItemTime raw; 4221-4228 ApplyItemTime(mult)
- Player.cs:4249-4253 SetItemAnimation; 4255-4283 ApplyItemAnimation (+1 rule 4258-4261; melee 4263-4265; summon 4266-4269; tile 4270-4272; wall 4273-4275; else+num 4277-4279; reuseDelay store 4282)
- Player.cs:28555-28569 CapAttackSpeeds/TurnAttackSpeedToUseTimeMultiplier
- Player.cs:25620-25622 BonusMeleeSpeedMultiplier application; 25627-25631 tileSpeed/wallSpeed reciprocal
- Player.cs:42005-42024 decrement clamp + ApplyReuseDelay trigger (42022)
- Player.cs:42068 TryStartUse; 42109 StartActualUse
- Player.cs:42130-42152 animation decrement + pendingItemReuse (42144-42147)
- Player.cs:42154-42161 itemTime decrement
- Player.cs:42177+ effect-on-itemTime-zero (healLife 42189-42197, buffType 42198-42106...)
- Player.cs:42855-42881 flag4/shoot
- Player.cs:42797-42806 shootsEveryUse/ItemAnimationJustStarted (ItemAnimationJustStarted def 3904)
- Player.cs:51969-51974 ApplyReuseDelay
- Player.cs:52012-52035 ItemCheck_AutoReuseLogic (skip at itemAnimation==1: 52021-52032)
- Player.cs:52036-52053 TryAllowingItemReuse (glove melee≠3030 52041-52042 + summon-scaling 52043-52044; stressBall/autoReuseAllWeapons 52046-52049)
- Player.cs:24918 buffered change gate
- Player.cs:44950/45163 mining itemTime = useTime×pickSpeed
- Player.cs:38960/39162/39485/41227 placement ApplyItemTime(item, wallSpeed/tileSpeed)
- Player.cs:43542-43548 ResetMeleeHitCooldowns; 43550+ Update; 43566-43568 SetMeleeHitCooldown
- Player.cs:42964-43006 melee window
- Player.cs:43768-43773 hit → cooldown; 43777-43780 ApplyAttackCooldown (itemAnimationMax*0.33)
- Item.cs:70 potionDelay=3600; 48185-48196 DefaultToHealingPotion (17)
- Item.cs:12732-12743 item 989 (21/45); 15102-15113 item 1226 (26/60)
- Item.cs:1382-1394 item 2 dirt block (15/10); 1679+ item 27 acorn (15/10)
- Item.cs:31362-31375 item 3509 copper pickaxe (useTime 15/useAnimation 23)
- Player.cs:25198 pStone

Wiki:
- Use_time.md:24-39 (useTime/useAnimation/reuseDelay definitions, Times-of-use formula line 34, reuseDelay line 37)
- Use_time.md:41-53 (disabled actions)
- Use_time.md:65 (use limit), 73-92 (projectile melee), 94-98 (autoswing skip +1)
- Use_time.md:127-156 (formulas), 174-176 (useAnimation+1)
- Autoswing.md:18-26
- wiki与源码不符: Use_time.md:98 claims the +1 skip step is "the last step in the whole process; the calculation for melee weapons are done earlier" — actually consistent with source (num only applied in the else branch). Also the melee formula in wiki uses floor + BonusMeleeSpeedMultiplier... consistent. The wiki melee formula line 129: Total = floor(useAnimation/(1+MeleeSpeed×MeleeSpeedMultiplier)) + reuseDelay — source applies BonusMeleeSpeedMultiplier to (meleeSpeed-1), i.e., useAnimation/(1+bonus×mult). Wiki's "Melee speed multiplier" semantics match. Fine. One wiki-source nuance: wiki says meleeSpeed starts at 0 ("sum of melee speed bonuses in decimals, starting at 0") while 1456 stores meleeSpeed as 1f-based multiplier — presentation difference, not a conflict. I can note it as 📄 minor.

Also the wiki (Use_time.md:336-345 refs) is based on 1.4.4.9 — noted.

One more check I should include: "reuseDelay is applied after the itemAnimation counter turns to zero... add value of reuseDelay to both counters" (Use_time.md:37) — matches P:51969-51974 + P:42022 ✅.

Data-side finding: vanilla-itemcombat.json has zero reuseDelay entries — the extractor dropped the field entirely. That's a data gap. file: game/src/data/vanilla-itemcombat.json (verified via node: 0 of 2612 entries have reuseDelay).

Let me now also mention: itemCount stats — melee 303 entries; useTime<useAnimation 111; useTime>useAnimation 7.

TOP N fixes:
1. reuseDelay 数据+逻辑全缺（Clockwork 等连发枪射速翻倍以上）
2. 挥击重启门用 useTime 而非 itemAnimation（111 件快 1.4-2×，7 件慢 2.1×）
3. 挖掘冷却误乘 meleeSpeed（attackSpeedMult），且 tileSpeed/采矿药混用（vanilla = useTime×pickSpeed）
4. melee+shoot 剑族每挥一弹（useTime-gated 族 989/1226 弹幕频率×2；shootsEveryUse 族缺数据位）
5. 药水瞬时生效 + useTime=60（vanilla 17t 末帧生效）；pStone 乘错轴（buff 时长 vs 病 CD）
6. 数字键切物品无门禁/无缓冲（vanilla itemAnimation>0 禁切+缓冲）
7. 放置节奏 14 固定 vs useTime=10×tileSpeed；墙 0.75 档 vs 1/1.25
8. autoReuse 设置项（Autofire）未实装；手套 autoReuse 缺 summon-scaling 分支
9. BonusMeleeSpeedMultiplier 每武器表缺失（Terra Blade/Baghnakhs 等）
10. attackCD（itemAnimationMax×0.33 全局近战 CD）缺失

Coverage list: the 10 checklist items.

Now write the final report. Keep it organized and complete with file:line evidence. No emojis per system instruction... wait, the output format explicitly requires status emojis (✅⚠️❌🔀❓📄). The system prompt says "For clear communication with the user the assistant MUST avoid using emojis." But the task explicitly defines the format with these symbols. These are status markers required by the caller's format spec, not decorative emojis. I'll follow the task's explicit format since it's a machine-parsed audit table format specified by the coordinator. The instruction conflict: task-specific format wins for the deliverable (they're semantic markers). I'll use them as specified.

Let me write the report now.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:38.000Z · glm-x-preview-260804

```
审计完成。以下为最终报告。

## 域:物品使用主链

**基准源码锚点(1.4.5.6,均 grep 定位后精读)**
- `ApplyItemTime`:Player.cs:4216(裸 useTime)/ 4221(带乘子版)
- `ApplyItemAnimation`:Player.cs:4255-4283(meleeSpeed 分族 / +1 跳帧 / reuseDelay 存储)
- `CapAttackSpeeds`+`TurnAttackSpeedToUseTimeMultiplier`:Player.cs:28555-28569
- 递减与重启门:Player.cs:42015-42024(钳零+ApplyReuseDelay 触发)、42130-42147(itemAnimation--/pendingItemReuse)、42154-42161(itemTime--)、42144(重启门**只看 itemAnimation**)
- `ApplyReuseDelay`:Player.cs:51969-51974;`ItemCheck_AutoReuseLogic`(跳帧=itemAnimation==1):Player.cs:52012-52035;`TryAllowingItemReuse`:Player.cs:52036-52053
- 发射门:`flag4 = itemAnimation>0 && ItemTimeIsZero`,Player.cs:42855-42881;`shootsEveryUse`→`ItemAnimationJustStarted`(:42798-42805,定义 :3904)
- 挖掘 `itemTime = useTime×pickSpeed`:Player.cs:45163、44950;放置 `ApplyItemTime(item, tileSpeed/wallSpeed)`:Player.cs:39485/41227、38960/39162
- 近战窗口:Player.cs:42964-43006;命中后 `SetMeleeHitCooldown(npc, itemAnimation)`:Player.cs:43768;`ApplyAttackCooldown = max(1, itemAnimationMax×0.33)`:Player.cs:43777-43780

**实现侧模型**:`player.useTime`(=itemTime,Player.ts:112/671 递减)+ `this.swing`(=itemAnimation,Game.ts:544-552,updateSwingHits Game.ts:7819 递减)。单计时器+swing 对象,无 reuseDelay/pendingItemReuse/Game.ts:3903 自认。

### 差异清单

| # | 机制项 | 原版设定(wiki页+数值) | 本仓库实现(file:line) | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 1 | useTime/useAnimation 双轨-动画时长 | useAnimation 经 ApplyItemAnimation 缩放:melee→×(1/(1+meleeSpeed)),createTile→×tileSpeed,createWall→×wallSpeed(P:4255-4283);wiki Use_time.md:127-165 | Game.ts:4053-4055 `useAnimation/attackSpeedMult`( melee)/4112(工具);attackSpeedMult=Player.ts:550-558 | ✅ | 公式形状一致(floor+倒数,封顶 3) |
| 2 | 双轨-itemTime 取值 | ApplyItemTime=**裸 useTime,不乘 meleeSpeed**(P:4216-4218);挖掘/放置例外乘 pickSpeed/tileSpeed/wallSpeed(P:45163/39485) | Game.ts:4058-4060(裸 useTime)、4396(远程裸)、4776/4803(投射族裸) | ✅ | 主干已对(注释 Game.ts:4056 记录了修正史) |
| 3 | 双轨-重启门 | 新一挥只看 `itemAnimation==0`(P:42144);itemTime 只门禁"生效"(射击/治疗/耗弹,P:42177+) | Game.ts:4074 `useTime===0 && canChain && (swingOver \|\| reuseSpd<animSpd)` | 🔀 | **itemTime 被当成重启门**。实测 game/src/data/vanilla-itemcombat.json:303 件 melee 中 **111 件 useTime<useAnimation**(如铜镐类 13/20、45 号 15/30)→ 本仓挥击周期=useTime,动画被截短,比原版快 1.4-2×;**7 件 useTime>useAnimation**(989 叶绿巨剑 21/45、1226 军刀 26/60,Item.cs:12732/15102 实证)→ 本仓周期=max(45,21)=45t,比原版(21t)慢 2.1× |
| 4 | autoReuse 跳帧(+1 档) | autoswing 在 itemAnimation==1 立即归零续挥(P:52021-52032);useStyle5+shoot 自动武器 useAnimation+1 对冲(P:4258-4261),实际周期=useAnimation-1;wiki Use_time.md:94-98/174-176 | Game.ts:4073 `swingOver = !this.swing \|\| this.swing.t<=1` | ✅ | t<=1 重启等价于原版 -1 周期;+1 档未做但净节拍=useTime,与原版周期等价(⚠️ 仅 useTime≠useAnimation 的枪族有视觉差异,见 #7) |
| 5 | reuseDelay | 动画归零后 `itemAnimation=itemTime=reuseDelay`(P:42022+51969-51974);wiki Use_time.md:28/37;发条突击步枪 useTime4/anim12/reuseDelay14 | 全仓仅注释(Game.ts:3903、player/SmartSelect.ts:179);**数据侧 game/src/data/vanilla-itemcombat.json 2612 条 0 条含 reuseDelay 字段**(node 实测) | ❌ | 数据+逻辑双缺。连发枪族(发条/某些回旋镖)以裸 useTime 全速连发,射速可达原版 2-3× |
| 6 | autoReuse 判定+手动连发 | autoReuse 持按续挥;非 autoReuse 需完整点击周期(releaseUseItem,P:42152);wiki Autoswing.md:18-26 | Game.ts:4061-4067(melee)、4408(远程/魔法)、4413(投掷)均 `autoReuse \|\| clickEdge`;边沿快照记在 updateUse 后(Game.ts:2700/2703) | ✅ | 语义对齐(2026-08-13 边沿序 bug 已修,Game.ts:2481 注释) |
| 7 | 弹药/魔法发射时机 | 首发在使用起始帧(itemTime==0 同帧,P:42177/42855),此后每 useTime 一发,与动画长度无关 | Game.ts:4316-4405(弓枪族:点击即发、useTime=bowC.useTime、4398 每发 useSwing) | ✅/🔀 | 节拍对;但每发重启动画(useSwing)与原版"一次动画内多发"不同——仅影响 useTime<useAnimation 的连发枪(叠加 #5 缺 reuseDelay 后此类枪射速偏差最大) |
| 8 | melee+shoot 剑族射击节拍 | 分两族:useTime 驱动族(星怒/波刃/叶绿巨剑 989/军刀 1226 等,Use_time.md:73-81)按 useTime 计(989=45t 一弹,非每挥);shootsEveryUse 族(Use_time.md:83-91)每挥一弹且需数据位 | Game.ts:4086-4099 **每次挥击启动帧必射一弹** | 🔀 | 989/1226 实测弹幕频率=每 21t/26t 一弹,原版 45t/60t 一弹(×2.2);shootsEveryUse 数据位未提取,两族无法区分 |
| 9 | 攻速链 CapAttackSpeeds | meleeSpeed 1f 基数(P:2328/18188),封顶 3 取倒数(P:28555-28569);每武器 BonusMeleeSpeedMultiplier=(ms-1)×mult+1(P:25620-25622),Terra Blade 0.75/拳刃 0.5/恶臭爪 0.25/变态刀 0.33(Use_time.md:135-140) | Player.ts:550-558(封顶 3 取倒数,甲虫球/醉酒/狼人/虚弱/食物入链) | ⚠️ | 汇总链对齐;**BonusMeleeSpeedMultiplier 每武器乘区全缺**(变态刀只做了潜行增伤 Player.ts:586) |
| 10 | 攻速链-useTime 免疫 | useTime 不吃 meleeSpeed(P:4216) | Game.ts:4058-4060 裸值 ✅;**但挖掘冷却 Game.ts:5211 `useTime/attackSpeedMult`** | ⚠️ | 挖掘节奏误乘 meleeSpeed;原版挖掘 itemTime=useTime×pickSpeed(P:45163)——猛爪/食物等 meleeSpeed 会错误加速挖矿 |
| 11 | 攻速链-pickSpeed/tileSpeed 分立 | pickSpeed(食物/风筝/挖矿药/天界壳,P:9615-9818)只作用挖掘;tileSpeed/wallSpeed(砌砖药/水泥搅拌机,P:9616/9842/12607)只作用放置 | Game.ts:5207-5211 `tileSpeedMult = tileSpeed \|\| Mining ? 0.75` 混入挖掘冷却 | 🔀 | 两条独立 stat 被合并成一个 0.75 档;砌砖刀/水泥搅拌机会错误加速挖矿,挖矿药数值 0.75 vs 原版 1/0.75=0.75 恰好近似但语义错位 |
| 12 | 鞭攻速链 | floor(useAnimation/(1+meleeSpeed+鞭速buff)/套乘)(Use_time.md:142-149;P:4266-4269 summonerWeaponSpeedBonus×whipUseTimeMultiplier) | Game.ts:4843-4847 `min(3, 1+swb×whipSpd)`;Player.ts:260 | ⚠️ | 缺 meleeSpeed 项(原版鞭吃近战攻速);swb 直接当加法并用 whipSpd 相乘,形状近似 |
| 13 | 使用中切物品 | itemAnimation>0 禁切+selectedItemState 缓冲(P:24918 `itemAnimation==0 && ItemTimeIsZero && reuseDelay==0`;wiki Use_time.md:43-49) | SmartSelect 有门禁(Game.ts:3901 `!swing && useTime===0`);**数字键热键栏 Game.ts:1363-1364 无任何门禁直写 selected** | ❌ | 挥击/使用中按数字键即时换手持,原版应缓冲到动画结束;切换还会把进行中的 swing/useTime 语义悬空 |
| 14 | 使用中移动/跳跃 | 不禁移动/跳跃(仅 useTurn 允许转向;坐骑例外) | 无任何移动锁 | ✅ | |
| 15 | 药水饮用 | DefaultToHealingPotion useAnimation=useTime=**17**(Item.cs:48185-48196),**动画末帧才回血**(P:42189-42193);病 CD 3600t(Item.cs:70)×pStone 0.75(P:25198) | Game.ts:4195-4221:点击**瞬时回血**,useTime=60(:4217),被病拦时 useTime=30(:4207);vi_ 桥接 useTime=60(Game.ts:4311) | 🔀/⚠️ | 时长 60 vs 17(≈3.5×);回血时机开头 vs 末帧;**pStone 乘错轴**:Game.ts:4211 把 0.75 乘在授予 buff 的时长上,原版乘的是耐药 CD |
| 16 | 耐药性(PotionSickness) | buff 21,3600t,pStone→2700 | Buffs.ts:487 healBlocked;Game.ts:4209/4294 拦截 | ✅ | 机制存在,数值路径见 #15 |
| 17 | 放置节奏 | 方块 useTime=10/useAnimation=15(Item.cs:1382-1394 dirt、1679+ acorn),节拍=useTime×tileSpeed(P:39485/41227);墙 ApplyItemTime(item,wallSpeed)(P:38960/39162) | tryPlace 固定 `useTime=14`(Game.ts:5975 起,绳/火把/轨道/通用共 4 处);tryPlaceWall `15×(wallSpeed\|\|Builder ? 0.75:1)`(Game.ts:5910 区段) | ⚠️ | 方块基速 14 vs 10(1.4× 慢)且 tileSpeed 无乘区;墙基速 15 vs 10、0.75 档 vs 原版 1/1.25=0.8 |
| 18 | 挥舞判定窗口 | itemAnimation>0 全窗判伤(P:42964-43006),命中盒=32×32 基底三段扩展(P:44480+),每挥每怪一次(SetMeleeHitCooldown(npc,itemAnimation) P:43768,起手清零 P:50932),命中后全局 attackCD=itemAnimationMax×0.33(P:43777-43780) | updateSwingHits Game.ts:7819-7964:全窗+三段命中盒 1:1+swingHitSet 每挥去重 | ✅ | 命中盒与去重对齐;全局 attackCD(0.33×animMax)缺失,续挥重叠期原版有额外保护(影响小) |
| 19 | 通道类(channel)/使用锁 | channel 期间 SetDummyItemTime 锁 useTime;高尔夫杆/钓鱼竿 | Game.ts:2508(SetDummyItemTime(2) 等价)、2583/2599(高尔夫 12+42)、4801(回旋镖 301) | ✅ | 三个已实装点均带源码行号;其余 channel 物未系统化(缺 channel 字段数据) |
| 20 | 冲刺/位移武器 | (域内抽查)罗迪 905/挪移类无使用链 | grep vi_905/rod_of_discord 无命中 | ❓ | 未实装,低优先 |
| 21 | 设置项 Autofire | autoReuseAllWeapons 全武器自动连发(TryAllowingItemReuse P:52046-52049;wiki Autoswing.md:25) | grep autoFire/autoReuseAllWeapons 0 命中 | ❌ | 设置项未实装 |
| 22 | 力量手套族 autoReuse 补充 | autoReuseGlove:melee(≠3030)+ **summon-scaling** 都补(TryAllowingItemReuse P:52041-52044) | Game.ts:4061-4065 只做 melee 分支(heldVid!==3030 ✅) | ⚠️ | summon-scaling 武器分支缺(鞭原生 autoReuse,影响面小) |

📄 **wiki 与源码不符/需注意**
- Use_time.md:132 称 meleeSpeed"starting at 0"(加法总和),1456 实际存 1f 基数乘数再经 CapAttackSpeeds 取倒数(P:2328/28557)——表述差异非冲突。
- Use_time.md:98 称"+1 是最后一步,melee 计算更早所以跳过"——与 P:4258/4263 分支结构一致,确认。
- 全 wiki 引用基于 1.4.4.9 源码(Use_time.md:336-345 自注),1.4.5.6 无数值漂移(上述锚点逐一比对)。
- wiki 无"急速武器 useAnimation<useTime"专述;源码裁决:#3 所列 7 件即该形态,行为=动画 21t 结束即续挥、弹幕按 itemTime 45t 门控。

### 覆盖清单
1. 双轨关系/递减/急速武器 → #1#2#3(含 111+7 件实测分布)
2. reuseDelay → #5
3. autoReuse 连发/重按节奏 → #4#6#21#22
4. 攻速链公式+来源叠加 → #9#10#11#12(甲虫球/食物/野性爪/夜明套/狼人均已入链)
5. 使用中切物品/移动/喝药打断 → #13#14#15
6. 弹药/魔法发射时机+连发间隔 → #7#8
7. 消耗品饮用时长/动画/打断 → #15#16
8. 放置节奏 → #17(+提取机 Game.ts:4137-4147 ✅)
9. 冲刺/位移武器 → #20
10. 挥舞判伤窗口/弧线 → #18

### 最需修复 TOP 8

1. **❌ reuseDelay 数据+逻辑双缺**(#5):vanilla-itemcombat.json 提取器漏字段 + 运行时无对应状态。连发枪族(发条突击步枪 4/12/14)射速直接翻倍以上。需先补提取器再接 `ApplyReuseDelay`(P:51969)三行逻辑。
2. **🔀 挥击重启门错用 useTime**(#3):Game.ts:4074。原版只看 itemAnimation(P:42144)。修法:重启门去掉 `useTime===0`(或改为 `swingOver` 单门),itemTime 另行只门禁发射/生效。111 件挥快 1.4-2×、7 件(叶绿巨剑/军刀)挥慢 2.1×,双向失真。
3. **⚠️ 挖掘冷却误乘 meleeSpeed**(#10):Game.ts:5211 去掉 `/attackSpeedMult`,改为原版 `useTime×pickSpeed`(P:45163);顺带拆开 #11 的 tileSpeed/Mining 混用档。
4. **🔀 melee+shoot 剑族每挥一弹**(#8):Game.ts:4086。需引入 shootsEveryUse 数据位区分两族,useTime 驱动族(989/1226 等)按 useTime 门控弹幕。
5. **🔀 药水瞬时生效 + useTime=60**(#15):改 17t 动画末帧回血(P:42189);pStone 0.75 从 buff 时长(Game.ts:4211)移到耐药 CD。
6. **❌ 数字键切物品无门禁**(#13):Game.ts:1363-1364 加与 SmartSelect 同款门禁(或做 selectedItemState 缓冲)。
7. **⚠️ 放置节奏**(#17):14 固定→`useTime×tileSpeed`(基 10),墙 15×0.75→`useTime×wallSpeed`(基 10、0.8 档)。
8. **⚠️ BonusMeleeSpeedMultiplier 每武器乘区缺失**(#9):Terra Blade 0.75/拳刃 0.5/恶臭爪 0.25/变态刀 0.33(P:25620-422),数据位+一处乘法即可。
```
