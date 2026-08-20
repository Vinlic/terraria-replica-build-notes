# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-18T03:31:27.168Z

```
在 ~/Project/GLM/SandboxWorld/game/src 下扫描所有 .ts 文件中的"未完成工作标记"。用 grep 找出包含以下关键词的**注释**行（注意排除历史叙述如"曾""旧""已废""自创近似已废"——只关心当前仍生效的缺口）：

关键词组：
1. 近似（且语境是"当前实现是近似"而非"曾用近似"）
2. 登记后续 / 登记另批 / 登记未接 / 登记 / 备案 / deferred / 另案 / 待办 / 留待
3. 暂不 / 暂略 / 未接 / 未实装 / 未实现 / 未建 / 未做 / 无此 / 缺口 / GAP
4. TODO / FIXME / XXX / HACK
5. 等价边界 / 等价声明 / C 级 / B 级

输出格式：按文件分组，每条给：文件:行号 | 标记类型 | 一句话内容摘要（保留关键 id/行号引用）。重点标注哪些是：
- A. 功能完全缺失（玩家可感知）
- B. 行为简化/数值近似
- C. 纯视觉/音效
- D. 多人/存档等边角

不要读整文件，grep -n 拿到行+上下文一行即可。最后给一个总数统计（A/B/C/D 各多少条）。控制在 200 条以内（按重要性优先：src/core src/entities src/world src/render 顺序）。
```

---

## 📎 Attachment · skill_listing · 2026-08-18T03:31:27.173Z

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

## 🤖 Assistant · 2026-08-18T03:31:39.990Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to scan all .ts files in ~/Project/GLM/SandboxWorld/game/src for "unfinished work markers" in comments. I need to grep for specific keyword groups.

Let me start by exploring the directory structure and then running greps for the keyword groups.

Let me first get a sense of the directory structure, then run parallel greps for the different keyword groups.

Keywords:
1. 近似 (approximation, current context not historical)
2. 登记 (register/deferred), 备案, deferred, 另案, 待办, 留待
3. 暂不, 暂略, 未接, 未实装, 未实现, 未建, 未做, 无此, 缺口, GAP
4. TODO, FIXME, XXX, HACK
5. 等价边界, 等价声明, C 级, B 级

Let me run these greps in parallel. Note the instruction: grep -n to get line + one line of context. Actually "不要读整文件，grep -n 拿到行+上下文一行即可" - don't read whole files, use grep -n to get line + one line of context.

Let me first check the directory structure.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:31:40.368Z · glm-x-preview-260804

```
我先了解目录结构，再并行执行各组关键词的 grep。
```


---

## 🤖 Assistant · 2026-08-18T03:31:40.855Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -type d | head -50",
 "description": "List directory structure under src"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:31:40.910Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src
~/Project/GLM/SandboxWorld/game/src/ui
~/Project/GLM/SandboxWorld/game/src/net
~/Project/GLM/SandboxWorld/game/src/core
~/Project/GLM/SandboxWorld/game/src/wld
~/Project/GLM/SandboxWorld/game/src/fx
~/Project/GLM/SandboxWorld/game/src/drops
~/Project/GLM/SandboxWorld/game/src/render
~/Project/GLM/SandboxWorld/game/src/world
~/Project/GLM/SandboxWorld/game/src/dev
~/Project/GLM/SandboxWorld/game/src/workers
~/Project/GLM/SandboxWorld/game/src/lighting
~/Project/GLM/SandboxWorld/game/src/physics
~/Project/GLM/SandboxWorld/game/src/vui
~/Project/GLM/SandboxWorld/game/src/items
~/Project/GLM/SandboxWorld/game/src/i18n
~/Project/GLM/SandboxWorld/game/src/save
~/Project/GLM/SandboxWorld/game/src/data
~/Project/GLM/SandboxWorld/game/src/assets
~/Project/GLM/SandboxWorld/game/src/stats
~/Project/GLM/SandboxWorld/game/src/entities
~/Project/GLM/SandboxWorld/game/src/debug
~/Project/GLM/SandboxWorld/game/src/player
~/Project/GLM/SandboxWorld/game/src/world/golf
~/Project/GLM/SandboxWorld/game/src/world/liquid
~/Project/GLM/SandboxWorld/game/src/world/gen
~/Project/GLM/SandboxWorld/game/src/world/wiring
~/Project/GLM/SandboxWorld/game/src/world/audit
~/Project/GLM/SandboxWorld/game/src/world/evolution
~/Project/GLM/SandboxWorld/game/src/world/weather
~/Project/GLM/SandboxWorld/game/src/world/spawn
~/Project/GLM/SandboxWorld/game/src/vui/core
~/Project/GLM/SandboxWorld/game/src/vui/elements
~/Project/GLM/SandboxWorld/game/src/vui/states
~/Project/GLM/SandboxWorld/game/src/vui/assets
~/Project/GLM/SandboxWorld/game/src/vui/draw
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla

```


---

## 🤖 Assistant · 2026-08-18T03:31:41.429Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -name \"*.ts\" | wc -l",
 "description": "Count .ts files under src"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:31:41.485Z

**📎 ToolResult**

```
     365

```


---

## 🤖 Assistant · 2026-08-18T03:31:47.008Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
365 .ts files. Now let me run the greps in parallel. I'll do one big grep per keyword group. Let me be careful with the exclusion of historical narrative (曾, 旧, 已废, 自创近似已废).

Let me run these greps.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:31:47.285Z · glm-x-preview-260804

```
共 365 个 .ts 文件。现在并行执行各组关键词 grep。
```


---

## 🤖 Assistant · 2026-08-18T03:31:48.798Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"近似\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v \"曾用近似\\|已废\\|旧的近似\\|曾以近似\\|旧近似\" | head -120",
 "description": "Grep for approximation markers excluding historical mentions"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:31:48.867Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/ui/HousingPanel.ts:43:  private readonly scale: number;   // inventoryScale 近似(1.0;UIScale 影响下的 DOM canvas 走 1:1 像素)
~/Project/GLM/SandboxWorld/game/src/ui/HousingPanel.ts:124:    // 行高 56×scale;列 = floor(mx / 48)(第 0 列宽 56,后续列 48 间隔换算近似——
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:11://     掉落表 = vanilla-npcdrops.json 规则树展平（ItemDropBestiaryInfoElement 近似）
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:310:// ============ 掉落表展平（ItemDropBestiaryInfoElement 近似） ============
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:1181:      // 此处以文本星近似并按星数着色 1-5 灰→金）
~/Project/GLM/SandboxWorld/game/src/ui/AchievementsUI.ts:53:/* ---- 背包提示牌（AchievementAdvisor.DrawOneAchievement 小卡 0.35 缩放近似） ---- */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:217: *  CSS 近似：色层 alpha 沿二次曲线 0.5→0 衰减，5s（300 tick） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:445:   *  DOM 近似为文本域 + 保存按钮）。保存写回 Sign 登记（Sign.TextSign） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:831:  /** 一键装备（ItemSlot.SwapEquip/ArmorSwap :3022-3346 近似）：部位→armor[0-2]（时装→[10-12]），
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:1261:    //（tools/extract-itemrare.mjs 从 Item.cs case 块提取 1643 条）；缺条目 fallback value 近似
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2094:   *  0.8 倍字号）、悬停提亮（原版 buffAlpha 0.4↔1.0 的 CSS 近似）、右键取消
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2125:    // 悬停提亮（原版 buffAlpha 悬停 +0.1/t 至 1、离开 -0.05/t 至 0.4 的 CSS 近似）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2416:   *  hslToRgb(hue,1,0.5) 色层 (time/300)²/2 衰减 5s；CSS 动画近似二次曲线） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2621:      // 专家/大师叠辉光行(静态 α0.45 近似原版脉动;大师红绿脉冲未做,偏差记录)
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2658:  /** 原版配方列表（数据驱动 1456 全量；鱼眼缩放 = 100/(|Δ|+100) 下限 0.75，CraftingUI.cs:184-192 DOM 近似） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3013:      // 环境 debuff(原版用专属 buff 贴图,此处以近义物品图标近似)
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3028:      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3030:      // 食物三档（以已注册食物贴图为图标近似）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3033:      // 微光化 353：银河珍珠 5340 近似（原版 Buff 353 无独立物品图标，debuff 显示
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3170:      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3172:      // 食物三档（以已注册食物贴图为图标近似）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3175:      // 微光化 353：银河珍珠 5340 近似（与上方 init 全量路径的 map 保持同步）
~/Project/GLM/SandboxWorld/game/src/ui/JourneyPowersUI.ts:20:/** 背包内物品点击给 1 / shift 给整堆（原版 UIItemSlot 抓取语义的 UI 近似） */
~/Project/GLM/SandboxWorld/game/src/core/HitTile.ts:64:   *  Prune 仅在 Clear 时调用）——此前"分档衰减 damage"是自创近似还错误归因为原版
~/Project/GLM/SandboxWorld/game/src/ui/ResearchUI.ts:1:// Journey 研究献祭面板（CreativePowers ItemSacrifices 的 DOM 近似入口）。
~/Project/GLM/SandboxWorld/game/src/ui/ResearchUI.ts:7:// ItemSacrificesUITab），此处为整包列表近似——献祭语义与计数 1:1，布局近似。
~/Project/GLM/SandboxWorld/game/src/core/csCompat.ts:3:// 移植 C# 源码时凡涉及以下语义一律用本模块，不要手写近似：
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts:541:        // 召唤杖 UseSound(Item_44)近似:短促"噗"——高频下扫正弦 + 一撮噪声气声
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts:547:        // 鞭响(Item_152)近似:高频噪声急促炸开 + 快速衰减
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts:564:        // 噪声爆发近似(原版 Item_14):一次性白噪 buffer + 低频 thump。
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:18://   多人 closestPlayer 近似为本地玩家（原版 FindClosest,Enemy 侧注入点）。
~/Project/GLM/SandboxWorld/game/src/render/EmoteBubble.ts:28:  if (bubbles.some((b) => b.npc === npc)) return; // 同一实体一次一个（原版 byID 近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:296: *  4703 四管 固定 8（1 主 + 7，原版 π/2 旋转扰动近似同表） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1338:        // 近似收紧②：tag=`${big},${ai1},${ai0}`——中途入视野的龙卷按快照恢复生长态
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1410:    // 不吃常规无敌帧；死因 ByOther(20) teamTank。冷却/减伤以独立字段近似（计划备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1593:   *  失败的 NoMoreTargets 相机推挤未实装（屏震近似暂略）。观战期间本方法吞掉
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1945:   * 门+此处 dead 门近似。返回是否找到并上坐（false → 调用方落 QuickMinecart） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2065:      //  原版只认装备槽；后备两档为本仓无装备槽 UI 时的近似）；全无 → 木质车 13
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2119:  /** 热喷泉 443 登记（原版岩浆流过自动喷发——Main 逐帧扫描上方格；此处 15 tick 采样近似） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2267:      //（原版 lastMouseInterface/inventory 门近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2629:        // EmitDust :171-178 四色按【格数】加权（曾用区旗近似）——沙漠沙景
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3263:    // DoesPlayerHaveReasonToActUpInBed :44-59 的危险/血月夜/日食昼门在此近似重置）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3330:      // oceanDepths 以 zoneBeach 同式近似。手持火把 placeStyle 计入 nearbyTorch（:17775-17778）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3366:      //  ⑤ num3==0 skip;盒 = NPC 中心对屏盒求交（:12297-12302,cx/cy 对玩家中心近似）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4093:    // 作为滤镜强度（激活点 = 玩家位置）；归零/无倒计时自动解除（renderer 侧脉冲近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4357:          // 此处对全组号 -1/-2 近似，交由各自 despawn 倒数收尾）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4559:    //      → 玩家±640px——单机用 luck 字段近似）----
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4786:    // （需右键+狙击镜配饰门）未接（登记）；lastMouseInterface 门以 uiBlocking 近似。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4864:    // （附 4.5 格泛光近似省略）；5643 彩虹 = Disco 轮转
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4872:        // :49390-49410：r/g/b = Main.DiscoR/G/B ÷255（连续渐变）——曾近似 6 档
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4925:            // 与 TileLightScanner 火把 style 7/14/23 同源——曾为静态近似/六色跳变
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5090:    // 亮晶簇/矿族 ×jitter、四柱魂 ×essScale（本仓未跟踪 essScale，取 1 近似——登记）、
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5278:    //  旧 0.5/t+0.8 封顶是 monospace 时代自造近似,位图字体对齐时一并归位）→
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5412:   *  无数据 → 30（原版绝大多数消耗品 useAnimation 15-45 的中位近似） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5654:  /** KillTile_PlaySounds 四档近似（WorldGen.cs:66483-66631）：蛛网 127 → Item27
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6036:          this.spawnParticles(pet.cx, pet.y, '#FF90B0', 4, 1.2, { life: 40 }); // 爱心尘近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6360:          // 钳成 3 违背原版；-1（无限）沿用 3 近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6930:        case 4870: // 回归药水(:42462):传送出生点(床/回归点 stash 未实装→出生点近似,偏差记录)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6972:          // 门（:44878-44892）——teleportToMouse 用就近落点 BFS（既有近似,传送药水等共用）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7029:              // 公告"换装失败"语义近似（原版换皮成功/失败二掷——备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7307:        // 原版含 π/2 旋转向扰动近似取同表）——此前全族单发化 DPS 差 3-8 倍
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7511:      this.useSwing(heldDef, ang);                          // useStyle5 静持（原版由 600 holdout 画枪，持物近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7962:              if (painted > 0) this.sfxAt('splash', ex, ey); // delegate 成功格尘/音近似（:74063-74100 族）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8051:        // cheapest-first，本作插入序近似——双子对自然成对死，与原版常态一致）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8090:            false, // 地面型判定省略：统一飞行（地面 3 件的 walk 近似后续按 aiStyle 细分）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8186:        // 配重球（counterWeight：悠悠球命中时落配重投射物，原版环绕弹的直线坠落近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8190:              // 配重球 = 环绕实体（AI_099_1 :64472-64610 1:1——曾直线坠落 Arrow 近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8554:        // 下一挥须等旋完 + reuseDelay2 = useTime 52 近似；t=25 松手提前收剑时
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9027:    // killTileBreakSound 四档近似）。砍树即此来的"咚咚"声（树干落 dig 档）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9096:        // TreeGrowFX_AshShake :29796-29822 尘 31×~10 + 尘 6×~16 的粒子近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10214:      this.spawnParticles(tx * TILE + 8, ty * TILE + 8, '#5C4436', 6, 1.5); // KillWall_MakeWallDust×10 近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10488:        // tileCut 族(草类)由 decor 近似覆盖;framed 家具不换;solid!==false 排除非实心
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10613:    // 此处以"下/上/侧邻任一格有内容或墙"近似（依赖登记：TileObjectData 锚点类型表）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11009:   *  5395——物品未注册，粒子近似 + 登记引擎级缺口） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11215:        // （床下地面行,本仓 spawnY=落脚格行约定一致;曾 (tx+1, ty−1) 帧盲近似）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11265:      // 非"直线可见"近似（旧注释已过期，电路系统全量移植后语义为导线连通）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11933:   *  小动物族触发压板 135(NPC.cs:47613 白名单由 critters 桶近似);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11980:   *  atmo = 玩家深度线性近似（worldSurface 以上 1 / rockLevel 以下 0）；雷声按距离衰减；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12134:        // 原版 SoundID 43：thunderDistance×15px 处发声——按距离衰减近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12153:    // 直伤 20（不绕 iframes）；视觉光效由粒子近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12345:        // 发射音：陷阱族=敲石近似；炮弹族由 TrapShot 首帧按原版播 Item14（Projectile.cs:21542/26830）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12789:    // 倾倒实心门（:45813 nactive && tileSolid && !tileSolidTop && type!=546 的仓库近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12880:  /** 传送族青尘（回忆药水 Cyan / 魔镜族白尘 dust 15，:42299/:42434 近似） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12921:      // MagicConch：对侧海滩带（beachDistance-100；近似取世界两缘 380 格带内找地表落点）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13276:    const mx = p.cx + p.facing * 8, my = p.cy - 4;          // MouthPosition 近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13305:   *    （:49609-49610——heldItemFrame 取贴图帧，此处 18×18 近似 marshmallow 串贴图）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13483:    if (isNet) return;   // 网不砍草不打怪（金/防火网的 cutExtraTiles 登记近似省略）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13543:      // stack = rand.Next(1, 11)（1-10，旧"1-5 铜"近似已退役）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13578:        // ①甲虫进攻套窗口刷新（beetleCounter+=num2 :43434——本仓时间蓄能模型近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13580:        // ②派对浸剂（enchant 7）彩纸（原版 spawn 弹 289——纯视觉,粒子近似,同敌怪侧）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13625:   *  近似；同 453 模式转桶；VanillaSpawner.spawnBound 只交付占位体——589/685
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13693:    // 类型，AnyNPCs 直接可见；本仓 bound 态以 TownNPC 近似 → 反查登记，使三人组链的
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13755:    // 旧 zoneDesert&&<groundLevel+30 近似退役）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14067:    // ①'' 睡渔夫补放（原版 SpawnNPC 海洋/沙滩分支每轮掷——补放近似其"未解救则持续在场"）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14373:  /** bound TownNPC npcKey → 绑缚态原版 NPC id（本仓 bound 近似的反查表）：
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14516:   *  射程门 = 各站点 IsWithinSnappngRangeToTile 近似统一 inTileRange。 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15504:      // + 入场怪近似为「Boss 槽在场或世吞体节/爬行者在场」
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15533:      // DangerThatPreventsOtherDangers 小集合未跟踪（近似面，登记 RuntimeEvents.ts）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15548:      // WorldGen.PlayerLOS 近似（WorldEvolution.playerLOS 同款：50 格内视为可见）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16123:  /** PunchCameraModifier 近似（GameHooks.punchCamera）：鹿角怪震屏源——
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16360:    // 150×meleeDamage + kb15 朝攻击者——608 追踪弹未实装,直伤近似,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16433:      //   初速 = Next(-35,36)*0.02（aiStyle 36 追踪 AI 未建模，以下方瞄敌近似，登记）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16525:        // 才走 gemsOnly=true 只掉宝石——本仓无背包宝石，近似为不掉）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16575:   *  叠加（原版 ±W/2,±H/2,此处取 ±8/±6 近似） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16664:    // 门（雕像产怪无玩家交互不计）——本仓 hurt 无伤害源参数，近似为全部计入，仅环境击杀的
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16697:    // claimable+对话领取,本仓自动授予近似,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16712:    // 气球碎块 Gore 1143-1145×3 + 1146（近似粒子）→ position = Bottom+(0,48)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16900:   *  光宠点光（Projectile light 族：Fairy 等 7 款照明宠物恒发光——近似暖光 1.1/1.0/0.85；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16968:    const dy = dirY ?? -0.35;                          // 摇杆无纵轴时略朝上（移动端近似）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:17630:  /** TreeGrowFXCheck（:29501-29540 + PlayerLOS 门）：视野内成树 → 绿叶爆散近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:17634:    if (px > this.camera.viewW / 2 + 80 || py > this.camera.viewH / 2 + 80) return;  // PlayerLOS 近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:17638:    this.sfx.play('chop', 0.8, x * TILE + 8, y * TILE);   // 成树沙沙声近似
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:17793:   *  门槛近似（挖掘模型 1:1 的 d.pick 即原版逐型门槛） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:18210:          // 非近似。消费点 Player.cs AdjTiles :35230-35232 → adjWaterSource）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:19013:    // Main.netMode != 0 近似（DyeInitializer.cs:334 队伍发色剂单机恒白）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:19257:      // PvP 冷却递减（圣骑士盾独立槽近似 + 狱火光环 per-owner）
~/Project/GLM/SandboxWorld/game/src/render/MapColors.ts:67:const SKY_FALLBACK = 0x91b9ff; // vanillaSkyColor(浅 y) 近似（生成预览无世界面时的兜底）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:15://     **全体尘都会评估**（含 ① 已命中者）。本引擎沿用既有近似——链 A 命中者不乘
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:26://  既有链 A 单段近似（其后通用重力照旧——扩表时勿动）。
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:184:      //  照常评估，:2136 vx×0.99 显式乘（链 A 命中型的 0.99 沿用既有近似不乘，

```


---

## 🤖 Assistant · 2026-08-18T03:31:49.706Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"登记后续|登记另批|登记未接|登记|备案|deferred|另案|待办|留待\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -150",
 "description": "Grep for deferred/registration markers"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:31:49.756Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:425:      // 登记世界槽位并持久化：导入不再是一次性的，重进游戏可在世界列表中看到并继续游玩
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:639:    // onWorldReady 已进游戏；登记世界槽位并保存初始数据
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:789:      // 多世界槽位（M3）：登记到 WorldStore
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:14:// 已闭合登记（数据层 → UI 消费）：
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:19:// 登记缺口（后续批次）：
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:571: * 解码(pending 去重只挡并发不挡串行)——登记终态,不再重发 */
~/Project/GLM/SandboxWorld/game/src/ui/JourneyPowersUI.ts:7:// 视觉为本仓面板风格（横滑杆代原版竖滑杆，偏差登记）。
~/Project/GLM/SandboxWorld/game/src/ui/ResearchUI.ts:6:// 偏差登记：原版是背包内每物品的研究按钮（CreativeUIState UISacrificeDialog /
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:445:   *  DOM 近似为文本域 + 保存按钮）。保存写回 Sign 登记（Sign.TextSign） */
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts:174:                      //   sub0=Remove——仅房主上行，服务器登记后按条带定向补发（见 net/leashedSync.ts）
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:94:  /** 箱子内容到达/被纠正（服务器权威；Game 负责登记 world.chests 与开面板） */
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:723:  /** 本地登记的箱子 → 同步槽位号（Game 注册；diff 轮询用） */
~/Project/GLM/SandboxWorld/game/src/net/leashedSync.ts:7://     :369-372 / section 激活       服务器登记后按条带向**新收到该条带**的客户端定向补发
~/Project/GLM/SandboxWorld/game/src/net/leashedSync.ts:12://                                    见 Game.netLeashedHostSweep 差异备案）
~/Project/GLM/SandboxWorld/game/src/net/leashedSync.ts:51: *  线序差异备案：锚格 (ax,ay) 在 kind 之前（原版 Type 在锚格前）；kind 为 0/1
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts:48:  | 'sandstormWind';    // ★登记缺失：原版沙暴无专属 wav（Sandstorm 只有视觉 shader + 风场 BGM），
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts:150: *  全路径自动生效。未登记 = 1.0（绝大多数 case 无专属修正，调用方传 1 即原版语义）。 */
~/Project/GLM/SandboxWorld/game/src/core/constants.ts:7:// ★GRAVITY 偏差登记（水体交互批结论：维持 0.4，不改 0.3）：
~/Project/GLM/SandboxWorld/game/src/core/constants.ts:18://   半对齐；全套移植需 NPC_GRAVITY 新常量+逐点替换，留待重力专项。
~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts:28:/** sheet 兜底索引：TILE_MAP 未显式登记的 wld tile id → 注册表中首个同 sheet 的 def。
~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts:462:        // 未显式登记 → sheet 兜底（全量补齐后 753 sheet 全覆盖，正常不再走到降级）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:243:            d.x += playerDx; d.y += playerDy;             //  本仓无消费方——备案不建）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:260:            d.vx *= 1.02; d.vy *= 1.02;                   //  两档本仓无消费方——备案不建）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:285:            && solidTileAt(Math.floor(d.x / 16), Math.floor(d.y / 16))) {  //  10×10 盒≈本格，备案）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:289:          // :1812 Main.snowDust++ 是全屏雪密度计数（无本仓等价物）——备案不建
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:297:          d.vx *= 0.99;   // 均不设——备案）；其余同 217 走兜底
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:441:      case 229: return { rgb: 1, a: 25 / 255 };   // :2659-2663（Lerp(lighting,White,0.6) 近似为全亮基底，备案）
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:16://   rollCoins 双轮极值/rollHeartsAndStars）。遗留登记（非 luck 链缺口）：
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:290:    // 备案（无法精确实现，当前 JSON 也未用到）：IsUsingSpecificAIValues(Conditions.cs:27)
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:368:      // _unresolved 备案），防御性兜底防 ids.length-1 为负
~/Project/GLM/SandboxWorld/game/src/render/CursorItemIcon.ts:95: *  (碎块魔杖族 5324/5329/5330 放置系统缺,引擎级缺口登记) */
~/Project/GLM/SandboxWorld/game/src/render/CritterCage.ts:20:// GAP 登记：
~/Project/GLM/SandboxWorld/game/src/render/CritterCage.ts:45://      残余 GAP（KiteLogic/DrawKite 近似、DrawBubble、逐型 FindFrame）登记在该文件尾。
~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts:58:    // 视口外起点的长瀑也要登记（水柱会流进画面）
~/Project/GLM/SandboxWorld/game/src/render/TileParticles.ts:85: *  src/core（禁区），暂以 lightGate=20 二值门近似——登记。 */
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:1263: *  227 仙人掌走 drawCactusCell 专属路径不在此表;518 按水位动态偏移未移植(备案)。 */
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:146:  /** 晚到贴图 → 去抖合批 → 只重烘登记过该文件的 chunk。
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:147:   *  全程无登记(所有烘焙时已就位)= 无 fallback 可修 → no-op(绝不能 invalidateAll
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:183:    this.chunkSheets.delete(k);  // 重建时会重新登记缺表
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:324:    this.chunkSheets.delete(this._bakingKey); // 重烘焙 = 重新登记
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:360:            // 动画墙（DoUpdate_AnimateWalls 换带 + 星彩玻璃逐格错相）：登记进换带
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:426:            // 动画家具换帧行：此处只登记重烘焙——帧带偏移由 drawVanillaCell 在
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:512:    //   本实现按 16×16 格区域着色——涂多格家具/树只有被涂格区域显色（登记）
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:40:/** loadTex 返回的 Image → bitmap 就绪回调登记(持有方替换自身引用) */
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:1106:   *  【依赖登记】柱背景天空贴图（VortexSky/NebulaSky/StardustSky/SolarSky/MoonLordSky）
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:1118:   *  视觉近似点登记 */
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:1763:    // GetColor 的 bgColor = Main.ColorOfTheSkies；以本帧天空底色近似（登记）
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:2134:   *  （Main.cs:61763，几乎最末）；本仓在世界变换段以恒等变换近似（登记：位置偏早） */
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:2228:   *  绘制，遮挡调制以 sunVisibility 乘 intensity（登记：层级偏早）。 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:340: *  单 tick 期望 = gemP/(K×300) 与原版逐点相等——数值等价实现（等价推导登记于
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:591: *  引擎级缺口登记），按缺席等价为不掉。 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:875:  /** 已登记箱子差分基准（postUpdate 轮询 → msg32 槽位编辑上报） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:878:  /** msg32 回包：登记/更新 world.chests（服务器权威），待开箱自动开面板 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1091:   *  与原版的差异（备案）：a. 原版 TE OnRemoved 由服务器 tile 落格即时触发，本仓
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1163:   *  右键取回是本仓扩展交互——备案。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1410:    // 不吃常规无敌帧；死因 ByOther(20) teamTank。冷却/减伤以独立字段近似（计划备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1420:      // 消耗/甲虫壳等 Hurt 内副作用未模拟（极端叠装场景，登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1510:   *  代理 equipStats 现成；熔岩石 accfx 未登记,直接扫配饰槽 vid） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2117:  /** 触发源登记(idx):428 测重板 / 423 感应器 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2119:  /** 热喷泉 443 登记（原版岩浆流过自动喷发——Main 逐帧扫描上方格；此处 15 tick 采样近似） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2566:    // Mechdusa queen 登记复位（WorldGen.clearWorld :6907 NPC.mechQueen=-1）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2651:    // 烘焙期缺表登记(file→chunks 反查,ChunkCache.onBakeAssetArrived):只重烘
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2695:    // 电路系统(Wiring.cs 移植):器件表 + 触发源登记(测重板 428/感应器 423)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2761:    // public/sounds/——登记销核）；Shimmer×3{微光,水/岩浆/蜜} 原版即 PlaySound(19,…,4)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3007:   *  → 走 freeBoundNpc 转正。687 城镇史莱姆黄 → 683 链无对应实体（未实装，登记）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3008:   *  11/463 的 AttemptToConvertNPCToEvil（兔/企鹅击杀等）未接（登记） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3569:    // 武器 false）。combat 表无 useTurn 列（提取器回填登记遗留）——按 itemfunc
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4786:    // （需右键+狙击镜配饰门）未接（登记）；lastMouseInterface 门以 uiBlocking 近似。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5090:    // 亮晶簇/矿族 ×jitter、四柱魂 ×essScale（本仓未跟踪 essScale，取 1 近似——登记）、
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5505:  // stack--。虚空袋 bank4 路径无载体（登记）；CanConsumeConsumableItem 的硬核不消耗
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5550:   *  值得用的增益药水。CountBuffs()==maxBuffs 门本仓 buffs 无槽上限（登记偏离，
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5551:   *  增益药水可全上）；光宠/ vanityPet 互斥与 603 收藏版门未接（登记） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5636:    p.inv.removeAt(slot, 1);                                  // CanConsume 消耗（硬核档登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5658:   *  （全表 1:1 登记遗留）。专用分支（树/罐/裂砖/轨道/锚桩）各有其音不经过此 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6074:        // doPlacementAction）：捕获小动物 → 锚桩 724（tryPlace 内登记 TECritterAnchor
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7012:          // ②已购且宠物在场 → RerollVariation 换外观变体（变体系统未实装，公告备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7029:              // 公告"换装失败"语义近似（原版换皮成功/失败二掷——备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7335:        // （Item_36/41 此前登记"素材未提取"，现已落位 public/sounds/——销核）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8798:          if (!c) return true;   // 无登记 = 可毁（Chest.cs:594-597）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8869:      // 平台族的锤循环（:45394-45440 平台坡面/楼梯）未接入——依赖登记：
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9092:      // 弹 655 蜂巢（AI_016 蜂巢裂蜂）未实装——登记跳过（见摇树报告跳过清单）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9518:      // 牌面文本登记（WorldGen.cs:43733 Sign.KillSign，帧检分支）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9522:      // 宝箱内容物掉出（BasicChest {21,467}——TileID.cs:315：两表都有战利品登记，
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9825:    // 登记表：砍到基座（整棵倒）→ 移除；拦腰砍 → 收缩为树桩段（y=切口下格起）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9837:   *  首击即倒（不做倒树动画——动画实体绑定自有树的登记表结构） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10202:    // 旧墙物品不掉，登记依赖）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10474:    //  绳一律不换)。平台/火把/篝火/箱/柜 style 族分支(:39299-39349)登记未接。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10613:    // 此处以"下/上/侧邻任一格有内容或墙"近似（依赖登记：TileObjectData 锚点类型表）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10675:    // 容器族放置登记（PlaceChest → Chest.CreateChest :57840-57842;梳妆台
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10682:    // 挂物族放置登记（原版 TileLoader.PlaceTile → TE*.Hook_AfterPlacement：
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10685:    //  记录在放置点(=锚点左上格)登记；空记录等价于无物，交互侧取用时也会按需补建
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10791:    // （开关 UI 未实装，登记 GAP）；无线/同色不耗；上漆在冷却前、成败不影响放置
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11009:   *  5395——物品未注册，粒子近似 + 登记引擎级缺口） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11027:    //  killClothier 旗标未持久化，登记；马桶消化 :19058-19060）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11033:        // （原版 ParticleOrchestra.Digestion；屎堆 5395 vi_ 未注册——物品侧缺口登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11074:    //  右键取回为本仓新增，见 net/leashedSync.ts applyLeashedRetrieve 备案）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11143:        // onChestSync 回包后登记 world.chests 并自动开面板
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11156:      // 墓碑：读碑文（原版 Sign 阅读；碑文在 2×2 锚点登记，点任意一格都能读到）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11186:          //  CanSnapToPosition 目标格畅通检查未移植（床位放置链已保证非实心,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11216:        // 再点移除（RemoveSpawn）未移植——本仓无原始出生点存档,登记
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11874:   *  触发源由 scanTriggerTiles 登记,onTileChanged 增量维护 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12207:   *  sandstorm → playLoop 恒 null（素材缺失登记，wav 入库后自动生效）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12231:        if (!h) { this.weatherLoopVol[name] = vol; continue; }  // sandstormWind 无素材 → null（登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12253:  /** 全图扫描测重板/感应器/间歇泉登记(读档/生成后一次);增量维护见 onTileChanged */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12415:      // ——锚点精确匹配，无登记/空文本静默；命中 → NewTextMultiline(text, pink, 460)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12431:   *  ——锚点无登记则懒建空牌项（Sign.cs:45-59），再开文本编辑面板 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12441:  /** 编辑面板保存（Sign.TextSign :63-77：按登记下标写回文本） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13309:   *    档本仓无手持槽，登记 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13483:    if (isNet) return;   // 网不砍草不打怪（金/防火网的 cutExtraTiles 登记近似省略）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13635:   *  已在场则跳过——activeIds 的反查登记（BOUND_TOWN_NPC_ID）通常已在上游拦下，
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13692:    // bound TownNPC → 绑缚原版 id 登记（原版被缚 NPC 本体就是 105/106/123/354/589/685
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13693:    // 类型，AnyNPCs 直接可见；本仓 bound 态以 TownNPC 近似 → 反查登记，使三人组链的
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14146:      //  兔 656/猫 637/狗 638 的 bought* 旗依赖许可证商店未实装，登记缺失）----
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14198:    // MushroomTileThreshold(=100)——此前按全域找房（备案），现 1:1；不满足则本轮跳过
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14376:   *  685 BoundTownSlimeOld(:12435)。trySpawnEnemy 把 bound TownNPC 登记进 activeIds，
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15533:      // DangerThatPreventsOtherDangers 小集合未跟踪（近似面，登记 RuntimeEvents.ts）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16170:   *  EoC 3）× 专家 2 ×（折扣 0.8 未实装——discountAvailable 恒 false，登记） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16176:    // 全部可移除（该排除表多为 boss 专属 debuff，未实装，登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16360:    // 150×meleeDamage + kb15 朝攻击者——608 追踪弹未实装,直伤近似,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16407:      // FallingStar 落地判定）——Arrow 无 ai 槽，登记依赖。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16433:      //   初速 = Next(-35,36)*0.02（aiStyle 36 追踪 AI 未建模，以下方瞄敌近似，登记）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16697:    // claimable+对话领取,本仓自动授予近似,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16793:        // 小妖精三档死亡登记尸点（黑暗魔法师 RaiseGoblins 的复活源，NPC.cs:80040-80052
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16794:        // switch case 552/553/554——仅 Goblin T1/T2/T3；555+ 与 551 不登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16874:   *  杀/遇/对话三处登记后调用） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16901:   *  逐款色差登记二期） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:17589:    const gs = { genTrees: this.world.trees } as unknown as GenState;   // 生长登记进 world.trees
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:18612:    // SpawnWOF 专用链（舌头/推进方向多实体联动）暂不支持意图，维持访客拦截（备案）
~/Project/GLM/SandboxWorld/game/src/render/InfoAccsLayer.ts:8:// 字体偏差登记:原版 FontAssets.MouseText;本仓 canvas 常规字体+strokeText 四向描边。
~/Project/GLM/SandboxWorld/game/src/render/TileFlames.ts:17:// 【简化登记】
~/Project/GLM/SandboxWorld/game/src/render/TileFlames.ts:124:// 逐 style 火苗参数表（原 S1 简化登记核销）。
~/Project/GLM/SandboxWorld/game/src/render/TileFlames.ts:545:// 手持火苗（原 S3 简化登记核销；PlayerDrawLayers.cs:3519-3561）。
~/Project/GLM/SandboxWorld/game/src/render/VanillaLiquidRenderer.ts:597:// 玩家可见结果（液体贴合坡面斜边）。【简化登记】坡面格与玻璃族的双 pass 差异
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:673:   *  依赖容器内容与门锁系统，未接入——恒按"可杀"处理（注释登记） */
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:516://   登记进 rotationDriven 以禁用通用 facing 镜像)、125/126=双子、127-131=Prime 头+四部件、
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:522:// 18 步循环、/6 换帧 = 3 帧各 6 步；gamePaused 冻结语义本仓无暂停态，恒推进（差异登记）
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:650:  // 差异登记：113 的 ai[2] 是 Leech 放虫轮(bossAI_wof)，放虫期间嘴部定帧=原版吐虫姿势）
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:708:  // 蓄力起点；传送置 5 的 5t 内会错取带内高帧，差异登记——彼时被 50 颗传送尘遮挡）
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1479:      // 代码**（1.4.5.6 实测不渲染任何火苗），无物可移植，勿再登记
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1699:    // heldProj 账本:帧首清账,实体自带 draw 分支登记活体投射物中心;
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1712:        noteHeldProjEntity(e);   // heldProj 账本登记(非目标弹型静默跳过)
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1742:    // PvP 头顶血条（备案偏差：原版无玩家头顶名/血条——仅悬停提示与地图头像边框；
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:2681:        // halfBrick 贴地从略——备案）；DrawBubble 判定与其余族共用
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3442:        // （噬魂怪 aiStyle5 实踩）。新增旋转族 AI 时必须登记在此，旋转与镜像共用本判定。
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3752:  // 第二批已接（原"未接登记"销核）：Glow_100/101+Extra_20（399 探测器 :24564-24575）、
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3890:    // 光染色管线，按全亮叠（差异登记，与全 Glow 表同口径）----
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4270:      // 【登记】本仓 AI_003 无 425 ai3 瞄准蓄力（NPC.cs:58986-59006），ai3 撞的是
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4301:      // 【登记】AI_003 未写 lai3 → 旋转恒 0（原版为指示灯自旋角）。
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:5014:        // 瞳孔静态居中（登记），容器 Extra_17/19 位置与镜像仍 1:1
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:5039:   *  未映射 frameCounter）；破体帧行缺 localAI[2]/[3]，取行 0（登记） */

```


---

## 🤖 Assistant · 2026-08-18T03:31:58.491Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
There are a lot of hits. The output is large. I need to be selective — only "current still-in-effect gaps", exclude historical narrative (曾/旧/已废/退役/销核/已闭合/已接). Also many "登记" hits are just describing registration tables (登记表, 登记箱子) which are actual feature names, not gaps. I need to filter carefully.

Let me now run the remaining keyword groups: group 3 (暂不/暂略/未接/未实装/未实现/未建/未做/无此/缺口/GAP), group 4 (TODO/FIXME/XXX/HACK), group 5 (等价边界/等价声明/C 级/B 级).

Given the constraint of 200 items max and priority order src/core, src/entities, src/world, src/render — I should focus. Let me run the remaining greps.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:31:58.811Z · glm-x-preview-260804

```
命中很多。继续跑第 3、4、5 组关键词。
```


---

## 🤖 Assistant · 2026-08-18T03:32:00.552Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"暂不|暂略|未接|未实装|未实现|未建|未做|无此|缺口|GAP\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -vE \"已废|销核|退役|已接\\)|已闭合|旧.未接\" | wc -l",
 "description": "Count group-3 keyword hits"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:32:00.633Z

**📎 ToolResult**

```
     365

```


---

## 🤖 Assistant · 2026-08-18T03:32:01.199Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"TODO|FIXME|XXX|HACK\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -40",
 "description": "Grep TODO/FIXME/XXX/HACK markers"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:32:01.264Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts:10:// aiStyle 与 AI_XXX 方法的对应见 NPC.cs AI() 分发；此处先覆盖高频家族，
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:630:/** 朝 (tx,ty) 以速度 spd/加速度 acc 追赶(vanilla numXXX = spd/dist 归一后 accelTo) */

```


---

## 🤖 Assistant · 2026-08-18T03:32:02.125Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"等价边界|等价声明|C 级|B 级|C级|B级\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -60",
 "description": "Grep equivalence-boundary and grade markers"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:32:02.199Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Audio.ts:19:  /** 解码 PCM 常驻上限:每首 mp3 解码后 30-45MB,104 首全驻 = GB 级;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4659:      this.golfState.update(golfing, false);   // 3611 高尔夫球车坐骑未实装（等价边界）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11622:    if (!this.boss) this.boss = head;   // 等价边界：单 Boss 槽（见报告）
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:945:  /** deferBuild：跳过构造期同步全量重建（大世界 80MB 级，见 buildStriped），
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:511:    // ★ 等价边界：原版按"绘制调用"着色（多格物件整张贴图随锚格上色）；
~/Project/GLM/SandboxWorld/game/src/world/Paint.ts:126: * ★ 等价边界（登记）：深层漆 13-24 与浅层 1-12 在 WorldGen.paintColor（:43948-44061）
~/Project/GLM/SandboxWorld/game/src/world/golf/GolfState.ts:144:   *  本作单人镜头语义未接（等价边界），保留门条件，无计分副作用。 */
~/Project/GLM/SandboxWorld/game/src/world/OldOnesArmy.ts:23:// 等价边界（备案原版行号）：
~/Project/GLM/SandboxWorld/game/src/entities/GrappleProj.ts:13:// 等价边界（与原版差异，见 tests/grapple.test.ts 头注）：
~/Project/GLM/SandboxWorld/game/src/entities/GrappleProj.ts:117:    // 等价边界：本仓 Buff 系无 Stoned(156)/Webbed(149)——该两门恒 false（原版无此 buff 时同）

```


---

## 🤖 Assistant · 2026-08-18T03:32:22.051Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting. The first count command output "365" — wait, that's suspicious. Actually it returned 365 which matches the file count... no wait, the first tool result shows "365" but that was supposed to be the count of grep hits for group 3. Hmm, actually looking at the results: the first result shows "365" — that seems to be a coincidence? Actually no — it's likely the actual hit count is 365. That's a big coincidence with the file count. Let me verify.

Actually wait, the order of results: result 1 = the wc -l of group 3 = 365 hits. Result 2 = TODO grep = 2 hits (both false positives — "此处先覆盖" contains XXX in "aiXXX"? No... "numXXX" yes). Result 3 = group 5.

365 hits for group 3 is a lot. I need to be selective. The task says: control within 200 items, priority order src/core, src/entities, src/world, src/render.

Given the enormous volume, I should focus on the high-signal markers: 登记缺口, 未实装, 未接, GAP, 备案, 留待, 等价边界, plus 近似 that are current. Many "近似" hits are actually informational ("X 近似" describing an approximation that IS in effect — those count as B or C category).

Strategy: I'll gather hits per directory in priority order, filter out:
- Historical: 曾, 已废, 旧, 退役, 销核, 已闭合, 已接, 已落位, 已退役
- Descriptive "登记表/登记箱子/登记进" which are actual code registrations (not gaps)
- Keep: 登记缺口/未实装/未接/GAP/备案/留待/暂不/暂略/未移植/未做/未建模/未跟踪/未持久化/无素材/缺表

Let me run targeted greps per directory with a focus on gap language. Let me do:

1. core: grep for gap-ish terms
2. entities
3. world
4. render
5. others (ui, fx, drops, net, save, player, etc.) — briefly

Let me define a strong "gap" pattern: 未实装|未接|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未覆盖|未支持|未落地|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂以|暂缺|缺表|缺素材|无素材|无载体|无此|未做|未建

That's still a lot. Let me count per directory first, then fetch in chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:32:23.210Z · glm-x-preview-260804

```
TODO/FIXME 组基本无命中（仅 2 条误报 numXXX/aiXXX）。第 3 组命中 365 行，量太大，我按优先目录分块拉取并过滤。
```


---

## 🤖 Assistant · 2026-08-18T03:32:26.240Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for d in core entities world render; do echo \"== $d ==\"; grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未覆盖|未支持|未接入|未落地|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂以|暂缺|未做|未建|未接\" ~/Project/GLM/SandboxWorld/game/src/$d --include=\"*.ts\" 2>/dev/null | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植\" | wc -l; done",
 "description": "Count gap-marker hits per priority directory"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:32:26.328Z

**📎 ToolResult**

```
== core ==
      75
== entities ==
     121
== world ==
     127
== render ==
      39

```


---

## 🤖 Assistant · 2026-08-18T03:32:46.329Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Total 362 in the four priority dirs alone. I need to be more selective. The user wants up to 200 items total, prioritized. Many hits are informational about "近似" or "登记" as registration (not gap).

Let me use a tighter pattern focused on explicit gaps: 未实装|未接|未实现|未移植|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建

And then a second pass for "近似" that includes 登记偏差/偏差.

Actually let me look at what the marker types mean in this codebase convention. The comments use "登记" (register in a ledger) = recorded known gap, "备案" = filed for record, "销核" = closed/resolved. So active gaps = those with 登记/备案/GAP/未实装/未接 etc. that are NOT 销核/退役/已闭合.

Given 200-item budget across 365 files, and core/entities/world/render having 362 hits with the loose pattern, I need the tightest signal. Let me pull the full lists for each priority dir with a moderately tight pattern, review, and curate.

Plan:
- core: pull all ~75 with tight filter, review all.
- entities: pull 121, review.
- world: pull 127, review.
- render: pull 39, review all.
- others: quick scan with the same tight pattern for remaining dirs (ui, fx, drops, net, save, player, physics, lighting, items, stats, etc.) — but budget. Priority says focus core/entities/world/render order; others can get a brief mention.

Let me pull per-directory lists. I'll use a tight regex: 未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建|未接

Note "登记" alone is too noisy (registration tables). But "登记" + 缺口/偏差 nearby matters. I'll catch those via other terms mostly. Also "近似——登记" style. For B-category approximations, the 近似 grep from earlier already gives many.

Actually, the deliverable: list with file:line | marker type | one-line summary, classified A/B/C/D, plus totals. With ~200 max. Let me gather data now. Start with core and render (smaller), then entities, world.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:32:46.645Z · glm-x-preview-260804

```
按目录分块拉取（先 core 和 render）。
```


---

## 🤖 Assistant · 2026-08-18T03:32:48.392Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建|未接\" ~/Project/GLM/SandboxWorld/game/src/core --include=\"*.ts\" | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植\"",
 "description": "List gap markers in src/core"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:32:48.465Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/constants.ts:14://   修正未移植——深度缩放（gravity×clamp((y/16-(60+10k))/(worldSurface/6),0.25,1)，
~/Project/GLM/SandboxWorld/game/src/core/constants.ts:18://   半对齐；全套移植需 NPC_GRAVITY 新常量+逐点替换，留待重力专项。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:590: *  3643 大琥珀=夺旗 CTF 旗物，非普通宝石）——该族物品本仓未注册（CTF 模式未实装，
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:591: *  引擎级缺口登记），按缺席等价为不掉。 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1091:   *  与原版的差异（备案）：a. 原版 TE OnRemoved 由服务器 tile 落格即时触发，本仓
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1163:   *  右键取回是本仓扩展交互——备案。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1229:        if (!e) continue; // review C2：未知 vanillaId（数据表缺口）只丢这一条，勿中止整批（否则同帧其余傀儡饿死被误清）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1410:    // 不吃常规无敌帧；死因 ByOther(20) teamTank。冷却/减伤以独立字段近似（计划备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1550:   *  观战 slot；单机恒 false（:17044）。includeSelf 仅死亡观战自机用（本仓未接） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1580:   *  目标代理 Bottom + (0, gfxOffY−21) + netOffset（gfxOffY 未建模，取 0） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1593:   *  失败的 NoMoreTargets 相机推挤未实装（屏震近似暂略）。观战期间本方法吞掉
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1838:  // ---- 运行时审计台账六缺口的新增运行时位 ----
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3007:   *  → 走 freeBoundNpc 转正。687 城镇史莱姆黄 → 683 链无对应实体（未实装，登记）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3008:   *  11/463 的 AttemptToConvertNPCToEvil（兔/企鹅击杀等）未接（登记） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3427:        if (recId === undefined) continue;   // 曲目无映射（如 50 TitleIntro）/唱片未注册
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4484:        // 台账「陨石落地系统未实装」已过期:落地 1:1 已接(本文件下方
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4659:      this.golfState.update(golfing, false);   // 3611 高尔夫球车坐骑未实装（等价边界）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4779:    // 原版相机切换平滑；目标代理未建（刚切换）退回自身不跳变）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4786:    // （需右键+狙击镜配饰门）未接（登记）；lastMouseInterface 门以 uiBlocking 近似。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4896:    //   （pulley=滑轨乘坐本仓未跟踪，petting 同；dust 172/萤火纯装饰从略）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5090:    // 亮晶簇/矿族 ×jitter、四柱魂 ×essScale（本仓未跟踪 essScale，取 1 近似——登记）、
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5394:      // itemfunc 提取缺口推断:细剑/短剑族(shoot→aiStyle 161)useStyle=13
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5506:  // 档未接（QuickHeal :5300 中核掉钱链已由死亡惩罚批承载，此取最小实现）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5509:   *  选药（QuickHeal_GetItemToUse :5310-5335）：healLife 与缺口差最小（过量最小）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5551:   *  增益药水可全上）；光宠/ vanityPet 互斥与 603 收藏版门未接（登记） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5667:   *  帧语义=style 帧（frame 'style'）；CopyPaintAndCoating 涂料复制未建模（涂装系统缺席） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5860:        gravDir: 1,                              // 反重力未实装（同 SmartCursor 口径）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5880:      // pendingItemReuse 未实装
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6930:        case 4870: // 回归药水(:42462):传送出生点(床/回归点 stash 未实装→出生点近似,偏差记录)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6971:          // 未移植注：LimitPointToPlayerReachable/AnyWallOfTypeOnLine(350)/丛林蜥蜴墙 87
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7012:          // ②已购且宠物在场 → RerollVariation 换外观变体（变体系统未实装，公告备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7029:              // 公告"换装失败"语义近似（原版换皮成功/失败二掷——备案）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7363:      // 必须先于下方 Arrow 分流，否则退化成"可回收的投掷刀"（GAP 补齐）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8144:        //   248 aiStyle1 箭物理(grav 0.3,射出音 Item17 未提取 GAP);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8475:        // ★食人鱼枪 1156 → 弹 190（aiStyle 39，GAP G3 行为层）：直飞 Arrow 表达不了
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8869:      // 平台族的锤循环（:45394-45440 平台坡面/楼梯）未接入——依赖登记：
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9092:      // 弹 655 蜂巢（AI_016 蜂巢裂蜂）未实装——登记跳过（见摇树报告跳过清单）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9114:    if (!e) return;   // NPC 数据表缺口（见跳过清单）静默丢弃，与生成器同策略
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10201:    // + 墙 ≠ 350。成功：旧墙尘 + 换墙 + 消耗（KillWall_DropItems 墙掉落表未移植——
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10259:   *  涂层（paintCoating 4668/5344）系统未建——涂层物品不在 FindPaintSlot 判定内，惰性。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10474:    //  绳一律不换)。平台/火把/篝火/箱/柜 style 族分支(:39299-39349)登记未接。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10612:    // 锚点表：AnchorTop/Bottom/Wall/AlternateTiles + 方向备选），全量锚点表未提取——
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10791:    // （开关 UI 未实装，登记 GAP）；无线/同色不耗；上漆在冷却前、成败不影响放置
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11009:   *  5395——物品未注册，粒子近似 + 登记引擎级缺口） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11027:    //  killClothier 旗标未持久化，登记；马桶消化 :19058-19060）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11033:        // （原版 ParticleOrchestra.Digestion；屎堆 5395 vi_ 未注册——物品侧缺口登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11074:    //  右键取回为本仓新增，见 net/leashedSync.ts applyLeashedRetrieve 备案）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11186:          //  CanSnapToPosition 目标格畅通检查未移植（床位放置链已保证非实心,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11216:        // 再点移除（RemoveSpawn）未移植——本仓无原始出生点存档,登记
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13121:    // isGeneratingOrLoadingWorld 门（:57187）：载入期 player 未建→跳过（原版直接 return）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13403:    // meleeScaleGlove ×1.1(泰坦手套未实装)不涉及,scale 恒 1)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:13997:        // 总条目；数据层 data/Bestiary.ts。原版另有 vampireSeed 世界分支——种子系统未实装）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14146:      //  兔 656/猫 637/狗 638 的 bought* 旗依赖许可证商店未实装，登记缺失）----
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14198:    // MushroomTileThreshold(=100)——此前按全域找房（备案），现 1:1；不满足则本轮跳过
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14386:   *  墓园（ZoneGraveyard）→ 派对（PartyIsUp；HasNoPartyText 表未移植——本表 NPC
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14718:      // 常规池 66-68(血月 64/65 未实现)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14753:      // (血月 111 / 玩家头部时装 113 未实现跳过)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14772:      // 夜 148-150 / 昼 151-155(幸运/DD2 文本未实现跳过)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14839:      // 巫医(cs:95660-95682):护士在场 263;常规 261/262/264(DD2 专项文本未实现,档位 3 回落 261)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14912:    // 其余类型(旅行商人368/骷髅商453/钓鱼娃369 等非房屋 NPC 未注册,不可达)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:14934:      .replace(/\{Bartender\}/g, Lang.npcName(550) ?? 'Bartender') // 酒馆老板未实装,恒用类型名
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15105:   *  level = ⌊(饵+竿+skill+Tipsy5+漂浮5) × 乘区⌋(坐姿 +5 未跟踪) */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15320:    // extract-shops.mjs 未捕获该 if 门——与 moonPhase 同类缺口，此处直接补）。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15325:    // 与 4702/moonPhase 同类提取缺口，此处按原版循环直补；价格 25 = Item.value（Item.cs:13374））
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15433:  /** 商店上架门（Chest.SetupShop if 门 → 本作状态映射；未实现事件门不上架） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:15533:      // DangerThatPreventsOtherDangers 小集合未跟踪（近似面，登记 RuntimeEvents.ts）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16021:   *  peddlersSatchelWasUsed（:1271 货郎背包 +1）/十周年世界（:1274-1280）未实装 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16170:   *  EoC 3）× 专家 2 ×（折扣 0.8 未实装——discountAvailable 恒 false，登记） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16176:    // 全部可移除（该排除表多为 boss 专属 debuff，未实装，登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16360:    // 150×meleeDamage + kb15 朝攻击者——608 追踪弹未实装,直伤近似,登记）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16433:      //   初速 = Next(-35,36)*0.02（aiStyle 36 追踪 AI 未建模，以下方瞄敌近似，登记）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16624:   *  ghostHurt 未接 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:16931:   *  的 hideMisc 翻转语义；移动端坐骑/宠物键入口。坐骑引擎未实装——槽 3 装备
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:18332:    this.sfx.play('tink'); // SoundID.Item37（非最优档）；最优档音效未接
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:18612:    // SpawnWOF 专用链（舌头/推进方向多实体联动）暂不支持意图，维持访客拦截（备案）

```


---

## 🤖 Assistant · 2026-08-18T03:32:50.248Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建|未接\" ~/Project/GLM/SandboxWorld/game/src/render --include=\"*.ts\" | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植\"",
 "description": "List gap markers in src/render"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:32:50.317Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/CursorItemIcon.ts:94: *  offset 刷 (22,22) / 滚 (28,28),scale 0.8。FlexibleTileWand 分支未实装
~/Project/GLM/SandboxWorld/game/src/render/CursorItemIcon.ts:95: *  (碎块魔杖族 5324/5329/5330 放置系统缺,引擎级缺口登记) */
~/Project/GLM/SandboxWorld/game/src/render/CursorItemIcon.ts:108: *  且无重命名链,该支恒不进（引擎级缺口,勿误当悬停侧缺陷） */
~/Project/GLM/SandboxWorld/game/src/render/CritterCage.ts:20:// GAP 登记：
~/Project/GLM/SandboxWorld/game/src/render/CritterCage.ts:45://      残余 GAP（KiteLogic/DrawKite 近似、DrawBubble、逐型 FindFrame）登记在该文件尾。
~/Project/GLM/SandboxWorld/game/src/render/TileAnim.ts:42:           //   ★原版逐列错相（TileDrawing.cs:6007-6014 addFrY=(frame+x%6)%6*72）未接——
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:36:// 注:原版 :84986-85129 的坡面圆角带((18+n)*18 列)超出 16 列表宽,未移植(平块不受影响)。
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:1263: *  227 仙人掌走 drawCactusCell 专属路径不在此表;518 按水位动态偏移未移植(备案)。 */
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:1335:    case 751: return [11, -8];           // :1034-1041(锚点帧;非锚点帧原版跳过绘制,未移植)
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:1398: *  (AllowsWind 墙集合未提取,任何墙挡风为保守近似) */
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:1475:    case 593:   // :5547-5579:fx>=18 → -18;fx<18 时帧行动画(临时帧未移植)
~/Project/GLM/SandboxWorld/game/src/render/BiomeBackground.ts:377:      // (naturalWidth×1.25)下,相邻背景图独立光栅化在接缝处留 1px 缺口(发丝缝),
~/Project/GLM/SandboxWorld/game/src/render/BiomeBackground.ts:478:  //  · 逐 16px 切片光照（暗洞挖空/贴墙裁剪）未实装——整行绘制近似,几何与原版一致。
~/Project/GLM/SandboxWorld/game/src/render/heldProj.ts:29: *     几族的"不转"恰好一致,非缺口。
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:465:          // 草皮覆盖件：保持原生透明（缺口露出背后的墙/天空），不做任何垫底/填充
~/Project/GLM/SandboxWorld/game/src/render/AutoTiler.ts:152:   * 原版架构：草皮 = 不透明泥土内格底 + 带透明缺口的草皮覆盖。
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:1107:   *  与 FilterMoonLord 专用 shader 未接入——此处只有滤镜层 */
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts:2191:  /** 【未接·原版死代码】DrawSun（:171-184）的 flare1/flare2 两张贴图在原版以
~/Project/GLM/SandboxWorld/game/src/render/BreathMeter.ts:17:// 偏差记录：gfxOffY 恒 0（gfxOffY 非零仅来自坐骑绘制偏移——坐骑系统未实装，
~/Project/GLM/SandboxWorld/game/src/render/BreathMeter.ts:18:// 恒 0 与无坐骑的原版语义一致）；ingameOptionsWindow/InGameUI 分支未移植
~/Project/GLM/SandboxWorld/game/src/render/MonolithFilters.ts:323:    // —— dontStarveShader 是药水 buff（perspectivePlayer），引擎未接，恒 false
~/Project/GLM/SandboxWorld/game/src/render/WallTiler.ts:99:  // 圆角/缺口互相咬合形成双轴交错的梅花格。合成 64×64 可平铺图案后按世界坐标连续取样。
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:873: *  默认：vy>0（或 localAI[0]==1，未移植略）→ 帧 1；vx==0 → 帧 0；
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1542:    // chunk 各自独立光栅化会在接缝处产生 1px 缺口(每 256 世界 px 一条发丝缝,
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1742:    // PvP 头顶血条（备案偏差：原版无玩家头顶名/血条——仅悬停提示与地图头像边框；
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:2681:        // halfBrick 贴地从略——备案）；DrawBubble 判定与其余族共用
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4496:    const fade = Math.max(0, Math.min(1, n291));          // ai2 恒 0（计时未接）时 = 1
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4716:   *  未实装（素材/系统缺）：QueenSlime shader 残影(ai0==4&&vy!=0)、Extra_186 水晶、
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4737:   *  未实装：localAI[3]<60 出生紫雾 3 层叠画（事件出生特效，走 spawnAlpha 渐显替代） */
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4751:   *  投影层：同列 row+18 半透明重绘（:23359-23367）；ai0==2 表情气泡未实装 */
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:4766:   *  未实装：localAI[3]<60 出生旋转紫雾、四向呼吸 sway 叠层（spawnAlpha 渐显替代） */
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:6155:  /** bound NPC 姿态帧（各表帧 0）。589 在 vanilla-npcs.json 缺登记（json 缺口族，同 588/633/663）
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:6346:        // ---- 160/209 Glow 变体档（Main.cs:25769-25799，S 备案 npcGlowVariantTex 接通）----
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:6640:   *  归一化伪法线；bodyRotation 本仓未建模取 0，登记）。lightAt 语域 0-255 → /255 */
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:6658:    // spinningpoint.RotatedBy(-rotation)：bodyRotation 未建模恒 0
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:7864:        //      差 ≈4px（yOffset 4 + playerOffset），备案已核销）。旋转零角时
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:8463:  /** 原版物品 vid → 内部 item id（atlasIcon 键）;未注册返回 -1 */
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:9156:   *    世吞 134 的多段质心平均(:55575-55589)未接,画头段位置

```


---

## 🤖 Assistant · 2026-08-18T03:33:00.470Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now I have core (~75) and render (~39). Let me get entities and world with the same filter. Note some hits are false positives (缺口 used as "gap" in a geometric/pixel sense — e.g. BiomeBackground.ts:377 "1px 缺口(发丝缝)", ChunkCache.ts:465 "缺口露出背后的墙", AutoTiler.ts:152, WallTiler.ts:99, Renderer.ts:1542). I'll exclude those.

Also core/Game.ts:4484 is "已过期" (stale ledger note) — exclude. Game.ts:5394/5509 "缺口" used as "difference gap" for item stats (QuickHeal) — that's describing algorithm not a gap marker; 5394 is "提取缺口推断" = extraction gap inferred... that's actually a data gap marker, keep as B maybe. Let me review at curation.

Now entities and world.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:33:02.077Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建|未接\" ~/Project/GLM/SandboxWorld/game/src/entities --include=\"*.ts\" | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植\"",
 "description": "List gap markers in src/entities"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:33:02.141Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/MinionProj.ts:908:          const centerY = groundY * TILE; // result.ToWorldCoordinates(8f, num6)（半砖 +8 未实装）
~/Project/GLM/SandboxWorld/game/src/entities/MinionProj.ts:929:            // AI_137_CanHit（:67170-67195）：塔顶+20 到敌中心的视线（两次弧线绕行未实装）
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:145: *  两 AI 族未移植（登记：CultistDragonHead/AncientCultistSquidhead），此处不召，
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:190:    // :31282-31292 age==300 召 454/521——两 AI 族未移植（登记），跳过
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:251:  // 闪电 num80−20(expert 基线未实装,g 照原文在经典值上调整)
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts:541:      // 瞄准帧（8 向索引,:36054-36070 的 ai[2] 语义;渲染未接,仅保状态）
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:51:  /** 已被微光转化（上浮漂浮、暂不可拾取，:34466 速度 <0.2 才可拾） */
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:349:      // WorldGen.CheckAchievement_RealEstateAndTownSlimes(:1831)——成就项未接，登记
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:206: *  落地砸出小史莱姆(30% 概率)。经典模式无传送(专家专属),暂不移植传送。 */
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:375:    //   （ZombieMoan wav 未提取 → 略，登记）
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:622:// 基线行为(空中横移 num7=3、跳跃 num2 缩放)本仓未建模,无可挂载点,登记跳过。
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:138: *  未移植时 ai0 恒 0 = 永远休眠，离屏不消散与原版休眠态一致 */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:329:    // 孵化标记 → 星尘生物链——本仓无弹 540 孵化 AI，登记缺口）；≥600 ai[2] 归零
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:353:        // 依赖弹 540 星尘标记孵化链——未移植，登记
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:543:      // （eow_dig 音轨未提取，Dig_0/1/2 近似）+ 穿块碎屑（:51985-51988 KillTile
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:729:    // （染色门 :92026 / 鞭标 VFX 门 :92135）本仓均未移植——字段先行保数据链一致
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:841:   *  UpdateNPC_SoulDrainDebuff :91952-91979)依赖魂镰实装,登记 GAP */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:948:   *  AdjustmentsEnabled :67282 消费）。本仓 Chippy 沙发召唤链未实装 → 恒 false，
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:972:   *  本仓未移植（debuff 自发光 :92181+ 段不受此门），字段落地保数据链一致（批次B） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1011:   *  ReflectProjectile cs:67036 反向归属玩家管线未接，登记依赖） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1328:    // :92484-92500 一并 1:1（见下），视觉渐隐侧未接（GAP：shimmerTransparency
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1604:   *    :60806/:60813/:60822/:60827/:60859/:60892）——天空盒世界未实装恒 false
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1624:    // ——天空盒世界未实装，跳过
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1638:        //   ——天空盒未实装跳过
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1643:        // Skyblock.noFossils && Next(5)==0 → 3347 沙漠化石（:60813-60816）：天空盒未实装跳过
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1651:        //   Next(200)==0 → 29 生命水晶（:60822-60826）：天空盒未实装跳过
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1664:            // Skyblock.lowTiles 表层分支（:60859-60876：194/195/62/27）：天空盒未实装跳过
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1672:            // Skyblock.lowTiles && hardMode 矿桶（:60892-60902）：天空盒未实装跳过
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1854:    // （1/12 帧闪烁上飘）未接——repo 粒子桶无 dust 228 语义，登记
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1866:      // :61289 草药史莱姆 (0.4,0.9,1) @ 中心格（尘 41 每帧闪烁 :61285 未接，登记）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3316:   *  同型个体分离（cs:31108）与穿平台（cs:94137）未移植（注释备案） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3502:    if (this.vanillaId === 43) range = 250;          // 食人怪（getGoodWorld 350 未接入）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:4360:   *  未接，登记。 */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:4755:   *  白天不消失只不发光（发光在 cs:34416 由 !dayTime 门——光照层未接入小动物，备案） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:4869:   *  cs:34646-34666）。速度：普通 0.3、发光/岩浆 0.6。（四象限 rotation 视觉未接，备案） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:4995:   *  （状态 2-7 宝箱引导链需要宝箱搜索基建，未移植备案） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:5912:    // 帧侧整带 +3、计时双倍）。本仓红帽召唤链未实装（Enemy.redHat 恒 false）→ 恒 0
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:5913:    // （enemies 可选访问：测试桩 hooks 可能未实现）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:5962:      // （getGood+24+血肉墙在场的同型双倍档 :21029-21032 未接，FTW 种子消费登记）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:6084:        // Center−(10,20) 起 20×30 窗随机一本，:2684-2741）——本仓 tile 50 未注册（放书
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:6085:        // 系统缺失，引擎级缺口登记），扫描恒空 → 走原版无书兜底 Center+NextVector2Circular
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:6821:      // 支线 a（:41336-41361）：3240px 内（原版还要求 !CanHitLine 视线阻隔——未接，省略）→
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:6906:    //         近似;弹型覆写 1-8 表 :13032 未接,登记）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:7046:    // （693 的 localAI[1]/[2] 受击段 :82083-82087 未接，登记）
~/Project/GLM/SandboxWorld/game/src/entities/TownShot.ts:75:  950: { rot: 'upright', cols: 0, spinRate: 0 },        // AI_186(rotation 0;四层脉冲叠画未接,登记)
~/Project/GLM/SandboxWorld/game/src/entities/GorePiece.ts:575:    // :864-880 玩家矩形相交 → 爆（联机远端玩家不在 GameHooks 面，仅主角，备案）
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts:56:// 438 MuonBlast(骑手弹) / 447 MartianDeathray(死光电报,自带 proj AI 未实装→直飞代) /
~/Project/GLM/SandboxWorld/game/src/entities/projStatus.ts:8://   · 'remixWorld→N'(15/954/979)/'ai0==1→N'(85)——秘密种子/附着态未跟踪,
~/Project/GLM/SandboxWorld/game/src/entities/projStatus.ts:51:  151: 'soulDrainT',   // SoulDrain:25 HP/s(:92927-92935,-50;魂镰 3006 联动登记 GAP)
~/Project/GLM/SandboxWorld/game/src/entities/projStatus.ts:98:    if (!field) continue; // 未实装 buff,登记见上
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:362:    // 301 的 -0.33 变调未建模（playSfxFiles 无 pitch 参数）
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:378:      //   releaseUseItem 输入语义,本引擎未建模（GAP,登记 docs/weapon-proj-audit）
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:562:      // 383 ≥10 的 HitTilesInACircle(300)+Item14 / 301 冲击波粒（:18115-18138）未建模
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:1332:        // 方向,X>0 → 1 / 否则 -1——角色朝鼠标侧转面(GAP#8 ①)。
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:1478:      // 掷出态撞墙 → 坠落态(:41014-41024):位移回卷 + num2 强制 2 + 冲击波(GAP#8 ④)
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:1609:  /** 掷出态撞墙冲击波(GAP#8 ④)。原版两连(:41031-41034):
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:1725:        // Kill 爆尘(:69686-69700):20 颗火尘向外喷(音效 Item54 未提取,登记 GAP)
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:2282: *  ai0=尘色/ai1=射程——尘迹省略（粒子钩子未接），伤害/碰撞 1:1 */
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:2369:  /** 近战系标记（SetDefaults melee=true :6565；浸剂链未接，登记偏差） */
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:2376:   *  vanilla-projectiles.json 未提取该字段，按源码常量 */
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:2499:    // Kill 尘爆近似（:68886-68897）；伴生 953 DaybreakExplosion 未实装——登记偏差
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts:781:    const gravDir = 1;   // 矿车无重力翻转（本仓未实装 gravDir 翻转坐骑）
~/Project/GLM/SandboxWorld/game/src/entities/projTargets.ts:195: *  flag6 = targetNPC.reflectsProjectiles（getGoodWorld 星弹特例未接入——运行时
~/Project/GLM/SandboxWorld/game/src/entities/projTargets.ts:256: *  GAP：ApplyBuffTo 的 trap&&deadMansSweater 减半(:11729-11733)——"死人毛衣"
~/Project/GLM/SandboxWorld/game/src/entities/projTargets.ts:257: *  配件未移植；creativeGodMode 入口门(:11452-11454)——创意上帝模式字段未建模。
~/Project/GLM/SandboxWorld/game/src/entities/projTargets.ts:259: *  独立缺口登记(Player.AddBuff :5088-5092 buffImmune 早退)。 */
~/Project/GLM/SandboxWorld/game/src/entities/projTargets.ts:316: *  未实装 buff（buffTypeByVanilla 查无）静默跳过——登记见 Buffs.ts 枚举注释 */
~/Project/GLM/SandboxWorld/game/src/entities/MissileProj.ts:18://     AI_009_MagicMissiles_Old :40753 回旋语义，另案登记）。
~/Project/GLM/SandboxWorld/game/src/entities/MissileProj.ts:572:   *  （:40770）未建模——仅影响 <100px 近距档的进入判定，登记偏差 */
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:547:   *  TownNPCs/Shimmered 档（Profiles.StackedNPCProfile 档位 1），对话差分登记 GAP */
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:916:    //      （:92562-92568，摘 buff 353 :92570-92573——城镇 buff 系统未建，无载体）。
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:919:    //      变体贴图走 townSheet getter（已接），对话差分未接（GAP）。
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:953:    //      的变身尘/烟粒子（:91277-91309）未接（登记） ----
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:1428:   *  550 扔麦酒(1/600)/229 海盗(1/600) 表演未接（登记）。禁触 = flag30：
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:1595:   *  登记未接 */
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:1985:   *    dryadWard 荆棘反伤(num5/3)与 HurtingBees 未接,略
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:2179:   *  登记未接:挥击态逐 tick 弧形判定(GetSwingStats/TweakSwingStats,近似中段
~/Project/GLM/SandboxWorld/game/src/entities/WhipProj.ts:57: *  依赖 TagEffectState 5478 计数——链机制整块登记 GAP）、310=markedByScytheWhip
~/Project/GLM/SandboxWorld/game/src/entities/Mounts.ts:274: *  地表高度以上 + 命中盒每格无液体且无墙（AllowsWind 墙表白名单未实装，有墙即挡风） */
~/Project/GLM/SandboxWorld/game/src/entities/Mounts.ts:279:  // DoesWindBlowAtThisHeight：tileY < worldSurface（remix 世界反转未实装）
~/Project/GLM/SandboxWorld/game/src/entities/Mounts.ts:790: *  其余坐骑 0（55 爬墙族走 UpdateAfterEquips :2967-2997，未实装登记） */
~/Project/GLM/SandboxWorld/game/src/entities/Mounts.ts:1891: *  未建模登记：mount 61 仙灵武库色光（:3624，纯装饰） */
~/Project/GLM/SandboxWorld/game/src/entities/Mounts.ts:1917:      num2 *= 0.5;   // InAPlaceWithWind 未建模：恒取非露天 0.5 档（登记）
~/Project/GLM/SandboxWorld/game/src/entities/Mounts.ts:2003: *  - 命中敌怪或实心 tile 即消散（penetrate 1 近似；930 穿透 -1 的弹跳/引信未实装——
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:432:    // expert justHit 1/2 蓄力越过视线(:32061-32064/:32077-32081)——justHit 未建模,登记
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:1026:  //    同段 rotation 改自旋 ±0.5/更新（纯视觉,本表 rot 单模未接——登记）
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:126:  /** 食人鱼 190（aiStyle 39，1156 食人鱼枪，GAP G3 行为层）：非空 = 走
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:182: *  （1.4.5 已无武器射出，未移植登记） */
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:197: *  num327=0 直立（另带按 12 帧前位移的 scale 渐缩——scale 通道登记未接） */
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:837:        // 近似——雕像产怪 flag 未实装）。ghostHurt（幽灵伤害头 156）未接，登记。
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:991:    // :26078-26087 淡入完成后每帧面向食人鱼（SetDummyItemTime 持物锁未接，登记 GAP）
~/Project/GLM/SandboxWorld/game/src/entities/PetFollower.ts:22:// 61 款全覆盖；表外 proj id（未来新增/数据缺口）回退旧"肩后悬停近似"
~/Project/GLM/SandboxWorld/game/src/entities/PetFollower.ts:558:  // 登记缺口（本次升级后残留的近似项）：
~/Project/GLM/SandboxWorld/game/src/entities/PetFollower.ts:560:  //    ±120）——ownerRef 无输入态，未建模；
~/Project/GLM/SandboxWorld/game/src/entities/PetFollower.ts:562:  //    尖叫/黑暗戳人、1090 彩虹巨石微光粒子——纯视觉/彩蛋，未移植；
~/Project/GLM/SandboxWorld/game/src/entities/PetFollower.ts:565:  //  ④ AI_026 抚摸(petting)交互帧、尘/Gore 特效未移植。
~/Project/GLM/SandboxWorld/game/src/entities/Portal.ts:57: *  细分集合未接入，实心即挡——装饰非实心天然放行） */
~/Project/GLM/SandboxWorld/game/src/entities/fighterFamilies.ts:353:  // （enemies 可选访问：测试桩 hooks 可能未实现）
~/Project/GLM/SandboxWorld/game/src/entities/LeashedCritter.ts:665:   *  manager 注入以保测试确定性（备案偏差）
~/Project/GLM/SandboxWorld/game/src/entities/LeashedCritter.ts:690:   *  与原版编码差异（备案）：7bit→u16、Size f32×2→u16×2（尺寸恒整像素）、
~/Project/GLM/SandboxWorld/game/src/entities/LeashedCritter.ts:1833:   *  侧 drawLeashedKite 叠加（本仓渲染层暂未接，登记为遗留项，见 GAP 台账⑤） */
~/Project/GLM/SandboxWorld/game/src/entities/LeashedCritter.ts:2163:   *  坡面贴合段从略（本仓生成期坡面罕见，登记备案）
~/Project/GLM/SandboxWorld/game/src/entities/LeashedCritter.ts:2551:// GAP 处置台账（2026-08-13 尾项清零批）
~/Project/GLM/SandboxWorld/game/src/entities/Bobber.ts:125:   *  跟踪，对应 +5 未接（登记）；Tipsy +5 已接（:41542-41545）。 */
~/Project/GLM/SandboxWorld/game/src/entities/Bobber.ts:413:    // 钓具箱族（accfx 未提取该字段——经装备名快速判定，渔夫耳环 2374/渔具袋 3721/钓具箱 2375）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:82: *  未建模 → 墙 350 即命中（备案：分层色阶不区分，越界判定略偏宽，外部
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:280:   *  ——Game 鞭 useTime 结算读取；312/365 登记持续期（效果端暂不接） */
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:976:  /** 哨兵上限（maxTurrets 链 :9863 War Table buff 未实装暂缺 + 散件/套装） */
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1381:      // (RT-3000)/300 连续加成 [:19022-19033] 未实装,登记）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1394:      // 专家且未进食 /2（:19060;闪亮石 0.75 档 skip;坐/睡 ×1.3 未实装）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1484:    // shimmerImmune（:14981 原版旗标来源未移植）恒 false；地狱层内不授予
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1583:    // （十字盾族 :27692 第 6 门）本作未实装 → 恒 0 语义
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:1666:    // 浅蓝近似 dust 34 视觉(sprite 粒子系统未实装)
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:2253:        const glide = !flying && this.inputJump && this.vy > 0;   // :26718（downDash 未建模恒 false）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:2265:          downDash: false,          // isPerformingJump_DownDash 未建模
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:2759:        // LUCKY_BREAK；stoned 摔伤分支 :25071-25076 同门——stoned 态本仓未实装）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:3148:    //    系统未实装，aiStyle 7 弹 Kill 段 :22036-22041 登记不适用）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:3167:      // KillMe 绕无敌帧直死（原版 ByOther(11)/(12) 文案包未移植 → npc 归因）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:3960:    // 本仓 damage 以 false 表示完全免伤——Boss 专属弹幕 371 等不可闪避源未移植）
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:3975:    // 反击 608 弹/冲撞命中消耗登记未接）
~/Project/GLM/SandboxWorld/game/src/entities/SolarEruption.ts:10://     （本仓单层近似，双层视觉差异小备案）。

```


---

## 🤖 Assistant · 2026-08-18T03:33:03.733Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建|未接\" ~/Project/GLM/SandboxWorld/game/src/world --include=\"*.ts\" | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植\"",
 "description": "List gap markers in src/world"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:33:03.805Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/SceneMetrics.ts:10:/** vanilla tile sheet id → 本仓库内部 tile id（TILE_DEFS 下标即内部 id；未注册的 sheet 缺席=计数 0） */
~/Project/GLM/SandboxWorld/game/src/world/SceneMetrics.ts:139:   *  本仓尚无消费端（登记：bestiary/刷怪上下文未接） */
~/Project/GLM/SandboxWorld/game/src/world/SceneMetrics.ts:145:   *  室外天气效应强度 ±0.005/t 逼近（BehindBackwall → -0.1），本仓天气渲染未接（登记） */
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:673:   *  依赖容器内容与门锁系统，未接入——恒按"可杀"处理（注释登记） */
~/Project/GLM/SandboxWorld/game/src/world/MinecartTrack.ts:15:/** 本仓库内部 tile id（v_314_minecart_track）；未注册时 -1 使全部判定安全失败 */
~/Project/GLM/SandboxWorld/game/src/world/FurnitureItems.ts:18://        故一并移植（决策：移植，不备案跳过）
~/Project/GLM/SandboxWorld/game/src/world/FurnitureItems.ts:181:/** useStyle 提取缺口补丁：45 个金属工具/武器族（3480-3521 铜镐族 + 3349/3351/3352）
~/Project/GLM/SandboxWorld/game/src/world/LunarEvent.ts:132: * 偏差：remix/getGood 深层支省略；PlayerLOS（与玩家视线）未接入 → 只按 SolidTiles 判窗
~/Project/GLM/SandboxWorld/game/src/world/Paint.ts:19://   本仓未建涂层存储/渲染链——涂层物品惰性（购买后无效果），登记依赖；油漆域 1-30 全量生效。
~/Project/GLM/SandboxWorld/game/src/world/Paint.ts:104: *  涂层系统未建（见文件头），仅涂刷尘/UI 可能消费 */
~/Project/GLM/SandboxWorld/game/src/world/Paint.ts:129: *   涂层（paintCoating 1/2 → fullbright/invisible 位）系统未建，另行登记。
~/Project/GLM/SandboxWorld/game/src/world/FurnitureStyle.ts:55:    // ★备案（未加专属 case，勿一刀切）：388/389 高门（TallGate）与 617 遗物座的
~/Project/GLM/SandboxWorld/game/src/world/OldOnesArmy.ts:23:// 等价边界（备案原版行号）：
~/Project/GLM/SandboxWorld/game/src/world/JourneyPowers.ts:63:// 写入顺序；本仓实现状态见各条注释（登记 = 引擎级缺口，见报告）
~/Project/GLM/SandboxWorld/game/src/world/golf/GolfState.ts:144:   *  本作单人镜头语义未接（等价边界），保留门条件，无计分副作用。 */
~/Project/GLM/SandboxWorld/game/src/world/golf/GolfState.ts:147:      /* 镜头跟随缓存未接（单人语义：分数记录 + Golfer 台词/商店消费） */
~/Project/GLM/SandboxWorld/game/src/world/liquid/settle.ts:36:    // ★落水越 waterLine 转岩浆（Liquid.cs:177-190，H 批备案的缺口）：非蜜/微光液体
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts:20://    （killTile=掉落+帧刷新；liquidChangeSound=音效；NetMessage 广播=多人层未接）
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts:263:   *  为地牢墙族 → 保持水）。QuickWater 调用方按需接线；未接线=null 不豁免 */
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts:296:    // 解析按 0 档——这些格仍按 style0 档判定（备案，见报告 2-C 节）。
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts:628:        // 原版边界特性：缺口 1 且本格满格时不扣源（Liquid.cs:381-384）
~/Project/GLM/SandboxWorld/game/src/world/World.ts:107:  /** 旗帜击杀计数（BannerSystem.killCount:bannerId→数;随会话,存档登记未接） */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileCleanupPass.ts:41:/** sheet(=原版 tile id)→ 内部 id;未实装时 0(空格)安全退化 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileCleanupPass.ts:189:      // ⑥ 墙 87(cs:21441-21458):extraLiquid 特殊种子分支未实装(SeedFlags 无该旗标),
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenSolid.ts:23:// ★翻转时间线（普通种子，1456 逐行核实；特殊种子专属翻转见文末备案）：
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenSolid.ts:43://   cs:17956  UndergroundJungleTrees 头 379=true（本仓缺该 pass,备案）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenSolid.ts:44://   cs:17997  QuickCleanup 头 137/130=false / 尾 cs:18104-05 还原 true（本仓缺,备案）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenSolid.ts:55:// ★特殊种子专属翻转（不接线,备案）：Pots cs:18123/18184、Traps cs:18894、
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:14:// 下游联动（本轮不实现，备案）：pass 96 CactusPalmTreesAndCoral 头段
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:197: *  skyblock 与 notTheBees（roundLandmasses/noSurface 未建模）。 */
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:207:    // SpawnStarterNPCs(19830，十周年专属→普通种子 no-op，备案跳过) → 本 pass →
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:267:    // 帧规范化族由放置端保证,备案）——注册序本 pass(21327) < MicroBiomes(21785)
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:293:    // 金币堆补底/地表散水清除/画作继承邻墙；FillWallHoles 与彩蛋备案）。零掷骰
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:728://   → 24 DirtToMud → 25 Silt → 26 OresAndShinies → 27 Webs(未移植) → 28 Underworld
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:731:// 本函数内对齐到 16-35 段（Underworld 28 在管线末"地狱"槽、Webs 27 后置——既有偏差另案）。
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:779:  //   还原点 = SmoothWorld 头 cs:16510 翻 true（本仓数据无法表达该窗口,备案）→
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrackPass.ts:17://  - SecretSeed.dualDungeons / errorWorld / notTheBees(225 豁免)分支未接
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrackPass.ts:377:    // dualDungeons 分支未接(无 DungeonUtils)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:10://      备案跳过(FillWallHoles 我方未实装;特殊种子分支不适用普通世界)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:25://   ⑭ DirtiestBlock 彩蛋(cs:22546+)——备案跳过(审计裁决)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:39:/** sheet(=原版 tile id)→ 内部 id;未实装时 0(空格)安全退化 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:68:  if (PC_PLATFORMS.has(sheet)) return !PC_CHEST_ANCH_INVALID.has(sheet) && st.half[i] === 0;  // !halfBrick（properTopFrame 帧位不建模，备案）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:100:/** 原版物品 id → 本仓库物品 id;未注册返回 -1。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:33://    债务期个别箱位/缺箱仍会错位,见 docs 尾批 2-A 备案)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:38://    未移植(帧落 0;四通道无帧,dump 对拍不受影响,渲染端帧备案)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:135:  //   protectedRects 近似（文件头备案的"无全局 StructureMap"已由 GenState 落地）,
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:188:  //   (普通世界行为一致);errorWorld 分支(cs:21879-21882/21890)未建模。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:762:    st.type[i] = LIVING_MAHOGANY; st.flags[i] = 1;       // SetFrames 帧写入备案:帧 0
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:770:    st.wall[i] = 78;                                     // PlaceWall(78)(SquareWallFrame 帧备案)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:1382:  // 行为（薄冰斑挡后续野营地/矿爆点/剑冢）不回归,仍登记进全局保护图,备案。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:1446: *  逐格结果可能分叉,掷骰总数一致,已在文件头备案 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts:332:  //   作上界,该遍下半区几乎空转,封壳出现单侧缺口
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts:12:// RNG 备案：原版 initializeHardMode 走 genRand（世界种子的独立生成流中段状态），
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:199: *  微光避让门：本管线微光 pass(cs:15256) 仍整体排在 vanillaBiomes 之后（顺序偏差另案），
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BrokenTrapCleanupPass.ts:29:/** sheet(=原版 tile id)→ 内部 id;未实装时 0(空格)安全退化 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts:197:  const van = st.w / 4200;                          // num3 缩放(cs:80567;FTW ×1.5 未接)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TreePass.ts:223:  // 面，棕榈不毁沙），K 事件链实证零击杀——备案省略。其余类型帧为渲染态。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/JungleShrinePass.ts:156:  //   未放置 137（原版神龛内含飞镖陷阱,缺件备案）,此翻转当前无消费面,仅存档时间线。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/UndergroundJungleTreesPass.ts:3:// 备案「cs:17956 头 379=true 本仓缺该 pass」），世界状态缺丛林地下树。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/UndergroundJungleTreesPass.ts:25:/** sheet(=原版 tile id)→ 内部 id;未实装时 0（空格）安全退化 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/QuickCleanupPass.ts:2:// 整 pass 缺失（GenSolid.ts 备案「cs:17997 头 137/130=false 本仓缺,备案」）。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/QuickCleanupPass.ts:32:/** sheet(=原版 tile id)→ 内部 id;未实装时 0（空格）安全退化 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/QuickCleanupPass.ts:107:          // setTileSilent 对非 0 内部 id 不清半砖/坡面（QQ 备案 2026-08-17；不补则
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:70:    // 触板→致动石失活→巨石落下（tile 重力未移植，致动语义数据 1:1）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/PilesPass.ts:119:  //   （cs:18919 SetBoulderSolidity(false) 在 noTrapsWorldGen 门内,普通种子不触发,备案）
~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts:216: *  - AnnouncementBoxDisabled / AnnouncementBoxRange：设置系统未接，恒可用 + 全图
~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts:236: *  【依赖登记】657 回声/658 微光/720 CRT/721 复古/725 黑白/733 收音机柱的屏幕滤镜未接入 */
~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts:871:      // AnnouncementBoxRange 默认 -1 = 全图（设置项，引擎暂未接设置门，恒全图）。
~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts:872:      // 【依赖登记】牌面文字编辑 UI 未接入（现存 signs 只读：墓碑/导入存档）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:15://    CheckDye/CheckLog/PlantCheck/CheckLilyPad 因放置门已保证支撑，恒为 no-op，未移植。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:18://  - 秘密种子分支（notTheBees / remix / frozen / extraLiquid）全部不触发，未移植。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:1260:    // 184 的重帧仅在放置时调用（LongMoss pass）；518 的 CheckLilyPad 恒 no-op 未移植
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:1772: *  （巨型蘑菇树未移植——见 C 组备案，此处尝试恒败零掷骰）；丛林草 60 → 61；
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:1783:        // Tree_Mushroom）未移植，恒败不消耗 RNG；备案见报告
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:1844: *  SquareTileFrame 对完整写入的 2×4 块为恒 no-op，未移植）。 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HellFortPass.ts:127: *  箱登记不在 dump 四通道,备案）。 */
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:18://   - Convert case 0（纯净化墙链）与 case 14-21（1.4.4+ 反转换）无消费方未移植；
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:389:      // 沙族（cs:72275-72309）：海洋贝壳补充 / 内陆仙人掌（绿洲/海藻系统未接）
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:757:        // 蘑菇草（cs:74765-74818）：顶蘑菇草植物 71（1/10）+ 蘑菇树（未接）+ 泥→70
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:771:          void 0; // 蘑菇树再生（TryGrowingTreeByType(5)）——树系统运行时接口未接
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:845:  //  未移植：case 0（纯净化墙链,蘑菇墙 80→15/64 深度带）与 case 14-21（1.4.4+
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:261: *  CheckPile 支撑为恒实心叶不触发；10/15/19/304 无后续破坏写;备案见审计文档）。 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1058:// 且上格空墙 0 → 分支处理。未命中列走海滨燕麦段（见下方备案）。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1060:// 已知近似（备案，接线时评估掷骰流影响）：
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1061://   - pass 头部绿洲消费段（cs:21129-21153：绿洲棕榈 323/海滨燕麦/绿洲植物 530）未实现；
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1062://   - 未命中列的 PlantSeaOat/GrowSeaOat/PlaceOasisPlant 段（cs:21302-21320）未实现；
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1153: *  TileFrameImportant、实心族归 Cosmetic——均无掷骰无格写，备案省略）。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts:9://  - SolidTile 的 tileSolidTop 近似为 !platform；PlaceTile 的 495 特判未移植
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenState.ts:165:   *  21153）消费——绿洲棕榈 323 / 海滨燕麦 / 绿洲植物 530（本仓库未实现，备案） */
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2:// ★简化纪律:任何"未移植/近似/恒X"必须在 docs/spawn-parity-gaps.md 登记(含原版行号+
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:72:    // 164 粉冰(=神圣冰)：key 实为 v_164_pink_ice_block（旧注"未注册→0"有误，已注册）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:629:  /** tileDungeon 集（Main.cs:7941-7946）：41/43/44 主砖（677-679 安全变体未注册缺席=0）。
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:715:   *  仙女 isNearFairy 倍率未实现（:653-656，依赖仙女随从实体），登记。
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:908:    // ★此前未移植:小动物链（SpawnAnNPC :2006 `else if (spawnFriendly)`）恒放行 →
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:963:            this.friendlyHit();   // :826-828 非 ftw 恒友好(专家 1/30 例外未实装)
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1380:    //  （下限 2；活跃玩家数未跟踪 → 单人取 1）。skyblock 的 spawnArmedZombies=false
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1437:      // 场上无 399;flag5 的 skyBehindPlayer/AnyDanger 上下文本仓未跟踪,以 skyMob+带外
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1546:    //      （:5281-5303；skyblock lowTiles 子档未建模备案，remix/2 被链首门短路） ----
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1610:      //  savedGolfer 由 freeBoundNpc 解救时写（"未跟踪恒 false"注释已过时）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1645:    //  ★此前未移植:困难模式丛林湖泊只有食人鱼/垂钓者兜底,原版主体是巨骨舌鱼
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1659:    //  救援链未实装（376 睡渔夫可由本段刷出，但无 376→369 转换、flags 亦无
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1694:      //  依赖链未实装：items.ts 无 Chum 物品注册、无弹体 820 → 恒 10（依赖：
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2057:        // 书架书怪 693/694（AI_FindNearbyBook）：书架实体系统未实现，暂缺
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2116:    //      GetGnomeChance 基档 10[:5281]，skyblock lowTiles 档未建模恒 10）----
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2175:    //  maxValue=65（L1195；remixWorld+地表恶地时 25——remix 未实装恒 65）。
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2438:      //  flag17 的 AnyDanger 压制（有敌对 NPC 面向玩家时关闭）未实装 → 恒放行（登记台账）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2548:        //  SpawnOnPlayer（NPC.cs:81273+，500 次玩家 spawnArea 内选点）未移植，以
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2658:        // :4419-4433 主只后四向各 1/fireFlyMultiple 附加（此前恒单只，备案已核销）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2663:      // L4439：乌鸦 Raven 301——(万圣节 || 墓地) && 1/12（节日未接 → 墓地单门）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2712:      // L4585：skyblock 火把僵尸段省略（skyblock 语义未接；原文本支亦带 !ZoneGraveyard 门）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2723:      // L4634：halloween/xMas 节日僵尸 319-321/331-332 段略（节日未接）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2838:      // 骷髅商 453（L4905-4910）：1/35，非水域（影烛未实现），场内唯一（CountNPCS==0）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2847:      // L4917：深层半段 && 1/200（offensiveToTim 1/50 buff 未接）→ Bound Goblin 45
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:3035:   *  计数 ≥40 通过（remixWorld 阈值 10 未接——本仓无 remix 世界恒 40） */
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:3088:   *  （:4111/:4602），地下恒 -1。万圣/圣诞史莱姆门（节日系统未移植,备案） */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts:578: *  pass 更晚），备案不查。fx=style*54+col*18，fy=0/18。 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts:680:  //   存档时间线——原版由 UndergroundJungleTrees 头（cs:17956,本仓缺该 pass,备案）还原。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts:781:  //   Piles 头翻转 → 229 终态与本仓序偏差联动（生成末态 false,原版 true）,备案。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts:790:          st.flags[i] = 0;                       // active(false)，type 留待幼虫覆写
~/Project/GLM/SandboxWorld/game/src/world/evolution/RuntimeEvents.ts:2:// 六缺口的三个系统落点（调用方 = core/Game.ts）：
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:395:  //   （生成期 G/C 箱腿实测全砖，平台 properTopFrame 未建模备案）；EmptyTile 不在锚类型。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:1296:  //   4→半砖/余→平）。近似备案：CanPound 全门（NO_POUND/BOULDERS/FORBIDS 表）以
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:2524:        // ②平台/solidTop/桌（SolidWithTop|Table 路——本段实测腿全 41/43/44 砖，备案近似）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:3781:  // Dome 体未转录（WorldUtils 形状族+窗/柱特征另案）——precalc 链（掷/位置）照走、
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:3782:  // 入口体暂以 Legacy 城堡近似（备案：Dome 种子 x86 网格不裁决）。
~/Project/GLM/SandboxWorld/game/src/world/audit/exemptions.ts:39://  未接通)、186/187(多带表帧语义)、105 雕像/411 起爆器/103 bowls/crystal_heart。

```


---

## 🤖 Assistant · 2026-08-18T03:33:11.502Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have substantial data. There's a LOT. I need to curate down to ≤200 items. The four priority dirs alone give ~362 raw lines but many are duplicates of the same system or informational. Let me also quickly check remaining dirs (fx, drops, net, ui, save, player, items, physics, lighting, stats, wld, mainFlow, etc.) with the tight pattern, briefly.

Then I'll curate: pick the meaningful gap items, classify A/B/C/D, and produce grouped output with counts.

Let me get the remaining dirs.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:33:11.799Z · glm-x-preview-260804

```
再扫其余目录（fx/drops/net/ui/save/player 等）。
```


---

## 🤖 Assistant · 2026-08-18T03:33:16.127Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|deferred|暂不|暂略|暂缺|未做|未建|未接\" ~/Project/GLM/SandboxWorld/game/src/fx ~/Project/GLM/SandboxWorld/game/src/drops ~/Project/GLM/SandboxWorld/game/src/net ~/Project/GLM/SandboxWorld/game/src/save ~/Project/GLM/SandboxWorld/game/src/player ~/Project/GLM/SandboxWorld/game/src/items ~/Project/GLM/SandboxWorld/game/src/physics ~/Project/GLM/SandboxWorld/game/src/lighting ~/Project/GLM/SandboxWorld/game/src/stats ~/Project/GLM/SandboxWorld/game/src/wld --include=\"*.ts\" 2>/dev/null | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植|已注册\" | grep -vE \"缺口.*露出|1px|发丝缝\" | head -60",
 "description": "Scan remaining src subdirectories for gap markers"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:33:16.202Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:243:            d.x += playerDx; d.y += playerDy;             //  本仓无消费方——备案不建）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:260:            d.vx *= 1.02; d.vy *= 1.02;                   //  两档本仓无消费方——备案不建）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:285:            && solidTileAt(Math.floor(d.x / 16), Math.floor(d.y / 16))) {  //  10×10 盒≈本格，备案）
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:289:          // :1812 Main.snowDust++ 是全屏雪密度计数（无本仓等价物）——备案不建
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:297:          d.vx *= 0.99;   // 均不设——备案）；其余同 217 走兜底
~/Project/GLM/SandboxWorld/game/src/fx/VanillaDust.ts:441:      case 229: return { rgb: 1, a: 25 / 255 };   // :2659-2663（Lerp(lighting,White,0.6) 近似为全亮基底，备案）
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:16://   rollCoins 双轮极值/rollHeartsAndStars）。遗留登记（非 luck 链缺口）：
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:141:    // remix 秘密种子未实装（remixWorld 恒 false）→ 前者退化为 !hardMode（同 NotRemixSeedHardmode
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:170:      // 再需三王一眼 AnyNPCs 扫描。秘密种子系统未实装 → 恒 false
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:204:      // （bossAI_lategame.ts:370 IsInPhase2=ai3∈{1,3}），但白天暴怒分支未实现
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:224:      // （Andrew/Whitney/Jim，ItemDropDatabase.cs:732-734）——具名系统未实装 → 恒 false
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:287:    case 'SkyblockIsNotUp': return true;                   // Conditions.cs:1534（天空盒世界未实装）
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:290:    // 备案（无法精确实现，当前 JSON 也未用到）：IsUsingSpecificAIValues(Conditions.cs:27)
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:368:      // _unresolved 备案），防御性兜底防 ids.length-1 为负
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:516:      warnOnce(`rule:${rule.k}`, `未实现的规则 kind ${rule.k}（按 failedCond 跳过）`);
~/Project/GLM/SandboxWorld/game/src/net/leashedSync.ts:12://                                    见 Game.netLeashedHostSweep 差异备案）
~/Project/GLM/SandboxWorld/game/src/net/leashedSync.ts:51: *  线序差异备案：锚格 (ax,ay) 在 kind 之前（原版 Type 在锚格前）；kind 为 0/1
~/Project/GLM/SandboxWorld/game/src/player/HairDyeColor.ts:178: *    与盔甲染料 3039 同属 effect 二进制缺口（vanillaDyes.ts 头注）；此处取
~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts:47:/** ItemID.cs:254 IsPaintScraper（油漆刮刀；本作油漆系统未建——集合保留，策略 8 可选中刮刀） */
~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts:59: *  提取缺口同上（json 中均为 -1），按原版补正。 */
~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts:148:  /** Player.gravDir（反重力未实装，恒 1；SmartSelectGamepadPointer.cs:28-30 的翻转分支保留） */
~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts:304:    if (env.player.gravDir === -1) {                            // :27-30（反重力未实装，恒不达）
~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts:479:   * 荧光弹族的 useAmmo/ammo 提取缺口按原版源码补正（见 FLARE_GUN_USE_AMMO 注释）。
~/Project/GLM/SandboxWorld/game/src/player/PlayerSitting.ts:11:// 屎堆 5395——本仓物品未注册，粒子近似+登记）。红帽骷髅触发（:84-90：夜间坐
~/Project/GLM/SandboxWorld/game/src/player/PlayerSitting.ts:12:// 长凳 89 的 frameX∈[2322,2358]）依赖 killClothier 旗标未持久化，登记。
~/Project/GLM/SandboxWorld/game/src/items/Inventory.ts:169:   *  涂层（paintCoating 4668/5344）系统未建——本仓 PaintOrCoating 仅 paint>0，涂层惰性 */
~/Project/GLM/SandboxWorld/game/src/items/LucyAxe.ts:7:// MP msg141 跨玩家同步未接（纯视觉，各自客户端本地生成，记档偏差）。
~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts:80:/** ItemID.cs:254 IsPaintScraper（油漆刮刀）——油漆系统未建，策略 no-op 但集合保留 */
~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts:1368:  // ---- 油漆三策略（SmartCursorHelper.cs:668-807）1:1。涂层（paintCoating）系统未建——
~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts:1771:  if (sheet === 314) return true; // gravDir 恒 1（反重力未实装）
~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts:1811: *  env.alchemy 缺省（未接世界态）时 83/84 均按不可收——等价语义 = 只认"非药草"分支，
~/Project/GLM/SandboxWorld/game/src/physics/TileCollision.ts:254: *  - 未移植 :2003 的"重跑 TileCollision 校验"本体（分轴结构代价高,
~/Project/GLM/SandboxWorld/game/src/physics/Conveyor.ts:38://    Main.cs:38049，渲染层未接，备案）。
~/Project/GLM/SandboxWorld/game/src/lighting/lightTables.ts:40:  // blind（buff 22 黑暗）×0.95（:185-189）——headcovered ×0.85 头埋方块未跟踪，登记
~/Project/GLM/SandboxWorld/game/src/lighting/LightingEngine.ts:120:      case State.MinimapUpdate: // 空槽(小地图导出未移植;保留维持 4 tick 周期)
~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts:40://      shimmer=GetShimmerBaseColor×1.5、paint 档=固定 (0.37,0.8,1)——涂装覆盖本仓未实装恒走该色）
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:77:/** 原版 item id → 内部 item id（未注册 -1；全量物品经 VANILLA_ITEM_KEY_BY_ID 占位注册） */
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:126:// ============ decraft（ShimmerTransforms.cs 2026-08-13 完整移植,替换 GAP） ============
~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts:98:// DebuffTimeMultiplier(:70)/LightningPlayerDamageScaling(:71) 未消费暂不列）
~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts:392://     UpdateNPC_BuffApplyVFX 鞭标闪电粒子门（:92135）——两消费者本仓均未移植
~/Project/GLM/SandboxWorld/game/src/stats/Luck.ts:38://     仍登记：风筝/恶臭 buff 的授予物品（风筝族 4371 等/恶臭药水 1332/弹幕 1080）未移植;
~/Project/GLM/SandboxWorld/game/src/stats/Luck.ts:108:   *  即 stinky）；此位仅作环境外注入备用。授予来源（恶臭药水 1332/弹幕 1080）未移植 */
~/Project/GLM/SandboxWorld/game/src/stats/SellChain.ts:40:// shopCustomPrice 未实装（本仓无店主自定义价）→ 恒回落 item.value。
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:12://      （debuff 系统未移植，对冲分支暂缺）；授予来源 = 浸蜜（Player.cs:27436
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:47:  Sharpened = 24,    // 磨刀石(159,右键)：近战穿甲 +12（:9625，穿甲系统未接先登记）
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:49:  Bewitched = 26,    // 附魔台(150,右键)：maxMinions+1（:9857，召唤位未接先登记）
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:50:  WarTable = 27,     // 战争桌(348,右键)：maxTurrets+1（:9863，哨兵位未接先登记）
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:104:                   //   本仓吸血/治疗弹链未实装，效果位 getter 备用；
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:108:                   //   luck += 档×0.1/3 :28675）。授予物品（风筝族 4371 等）未移植，登记
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:111:                   //   ApplyBuffTo(120,600)）——物品与弹体未移植，登记
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:160:                      //   ——授予链 = 隐身药水 297（10800t=3min）。敌怪索敌无视未移植
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:167:                      //   （Projectile.cs:11606-11608）。光衰减消费点 lightTables.ts 未接
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:172:                      //   未接（本条目先作 debuff 登记/护士可清），登记
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:371: *  未实装 buff 返回 undefined，调用方静默跳过 */
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:410: *  未移植,登记 GAP（OnFire 的 vampireSeed 翻番 slime 分支同理 :18803-18805） */
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:428: *  （常规世界 -8 = 4 HP/s；slime 翻倍分支 :18803-18805 依赖 Slimed 未移植） */
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:456:   *  buffTime>60 且 Main.debuff；NurseCannotRemoveDebuff 排除表未实装，登记） */
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:478:   *  drippingSlime 再翻到 -200 :18803-18805——Slimed(137) 未移植,登记）。本仓
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:479:   *  秘密种子系统未实装（世界创建链无种子位），常 false；分支按原版数值落地，
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:480:   *  种子接线后置 true 即活（另 Main.cs:42715 buff 图标 <10t 不显示秒数,UI 侧未接） */

```


---

## 🤖 Assistant · 2026-08-18T03:33:18.684Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"未实装|未实现|未移植|未建模|未跟踪|未持久化|未注册|未提取|未接入|缺口|GAP|备案|留待|待办|另案|暂不|暂略|暂缺|未做|未建|未接|近似\" ~/Project/GLM/SandboxWorld/game/src/ui ~/Project/GLM/SandboxWorld/game/src/mainFlow.ts --include=\"*.ts\" 2>/dev/null | grep -vE \"曾|已废|退役|销核|已闭合|已接\\)|已落位|已实装|已移植\" | grep -vE \"登记世界槽位|登记到 WorldStore\" | head -50",
 "description": "Scan src/ui and mainFlow for gap markers"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:33:18.857Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/ui/HousingPanel.ts:43:  private readonly scale: number;   // inventoryScale 近似(1.0;UIScale 影响下的 DOM canvas 走 1:1 像素)
~/Project/GLM/SandboxWorld/game/src/ui/HousingPanel.ts:124:    // 行高 56×scale;列 = floor(mx / 48)(第 0 列宽 56,后续列 48 间隔换算近似——
~/Project/GLM/SandboxWorld/game/src/ui/JourneyPowersUI.ts:20:/** 背包内物品点击给 1 / shift 给整堆（原版 UIItemSlot 抓取语义的 UI 近似） */
~/Project/GLM/SandboxWorld/game/src/ui/ResearchUI.ts:1:// Journey 研究献祭面板（CreativePowers ItemSacrifices 的 DOM 近似入口）。
~/Project/GLM/SandboxWorld/game/src/ui/ResearchUI.ts:7:// ItemSacrificesUITab），此处为整包列表近似——献祭语义与计数 1:1，布局近似。
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:11://     掉落表 = vanilla-npcdrops.json 规则树展平（ItemDropBestiaryInfoElement 近似）
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:19:// 登记缺口（后续批次）：
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:310:// ============ 掉落表展平（ItemDropBestiaryInfoElement 近似） ============
~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts:1181:      // 此处以文本星近似并按星数着色 1-5 灰→金）
~/Project/GLM/SandboxWorld/game/src/ui/AchievementsUI.ts:53:/* ---- 背包提示牌（AchievementAdvisor.DrawOneAchievement 小卡 0.35 缩放近似） ---- */
~/Project/GLM/SandboxWorld/game/src/ui/MobileControls.ts:289:      // 坐骑（槽 3）引擎未实装（矿车除外）——仅提示
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:217: *  CSS 近似：色层 alpha 沿二次曲线 0.5→0 衰减，5s（300 tick） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:445:   *  DOM 近似为文本域 + 保存按钮）。保存写回 Sign 登记（Sign.TextSign） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:831:  /** 一键装备（ItemSlot.SwapEquip/ArmorSwap :3022-3346 近似）：部位→armor[0-2]（时装→[10-12]），
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:1261:    //（tools/extract-itemrare.mjs 从 Item.cs case 块提取 1643 条）；缺条目 fallback value 近似
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2094:   *  0.8 倍字号）、悬停提亮（原版 buffAlpha 0.4↔1.0 的 CSS 近似）、右键取消
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2125:    // 悬停提亮（原版 buffAlpha 悬停 +0.1/t 至 1、离开 -0.05/t 至 0.4 的 CSS 近似）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2416:   *  hslToRgb(hue,1,0.5) 色层 (time/300)²/2 衰减 5s；CSS 动画近似二次曲线） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2621:      // 专家/大师叠辉光行(静态 α0.45 近似原版脉动;大师红绿脉冲未做,偏差记录)
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2658:  /** 原版配方列表（数据驱动 1456 全量；鱼眼缩放 = 100/(|Δ|+100) 下限 0.75，CraftingUI.cs:184-192 DOM 近似） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2800:  /** 材料格放入：从背包按缺口拉取（组材料依序拉组内成员） */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2859:   *  点击关闭(原版跳成就页,成就页 UI 未接 GAP) */
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2887:    card.onclick = kill; // 原版点击开成就页并移除;成就页 UI 未接,先关闭(GAP)
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3013:      // 环境 debuff(原版用专属 buff 贴图,此处以近义物品图标近似)
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3028:      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3030:      // 食物三档（以已注册食物贴图为图标近似）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3033:      // 微光化 353：银河珍珠 5340 近似（原版 Buff 353 无独立物品图标，debuff 显示
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3041:  /** 消息缓冲:ChatMonitor 未建(initInGame 之前,如新世界 afterWorldLoad
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3170:      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3172:      // 食物三档（以已注册食物贴图为图标近似）
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:3175:      // 微光化 353：银河珍珠 5340 近似（与上方 init 全量路径的 map 保持同步）

```


---

## 🤖 Assistant · 2026-08-18T03:33:27.358Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have comprehensive data. Let me look at a few important multi-line headers to confirm what they contain, then curate. Key multi-item headers worth reading (one line of context each):
- src/world/JourneyPowers.ts:63 (登记 = 引擎级缺口)
- src/render/CritterCage.ts:20 GAP 登记 block
- src/entities/PetFollower.ts:558 登记缺口 block
- src/entities/LeashedCritter.ts:2551 GAP 处置台账
- src/ui/BestiaryPanel.ts:19 登记缺口（后续批次）
- src/world/wiring/devices.ts:236
- src/world/evolution/RuntimeEvents.ts:2 六缺口
- src/fx/VanillaDust.ts header (近似沿用)
- src/world/audit/exemptions.ts:39

Let me read those blocks quickly (a few lines each) to summarize accurately.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:33:27.768Z · glm-x-preview-260804

```
拉取几个多行登记块的内容（各读几行）。
```


---

## 🤖 Assistant · 2026-08-18T03:33:29.638Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '18,30p' ~/Project/GLM/SandboxWorld/game/src/render/CritterCage.ts; echo ---; sed -n '556,568p' ~/Project/GLM/SandboxWorld/game/src/entities/PetFollower.ts; echo ---; sed -n '2549,2570p' ~/Project/GLM/SandboxWorld/game/src/entities/LeashedCritter.ts",
 "description": "Read GAP ledger blocks in three files"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:33:29.735Z

**📎 ToolResult**

```
//   (族,样式,槽位) 种子化的确定性 RNG 复刻同一状态机（联机/测试可重放），转移结构
//   （段帧域/持帧时长/概率分支/回卷）与原版逐行对应。
// GAP 登记：
//   ① 放置链（已闭环）：原版无"捕获"机制——笼=普通家具放置（Player.cs
//      PlaceThing_Tiles → TileObject.CanPlace/Place），物种身份 = tile type 本身
//      （每物种独立 tile id），placeStyle 恒 0，frameX/frameY 只存物体列/行偏移
//      （TileObjectData.cs:2690-2710 Style6x3/Style3x2 + :3658-3710 Style2x2 罐缸族），
//      动画纯渲染侧。笼/缸物品 tile: 链接 92 条全量已接（items.ts CAGE_ITEM_SHEET
//      表，Item.cs createTile 赋值段提取 + TEdit items.json createTile 列 92/92
//      交叉吻合；itemfunc 只覆盖 5 条直赋），放置走 tryPlace vanilla-style 通用
//      分支（单格帧合成 = world/FurnitureStyle.ts framedCellFrame）。
//      ★注意：坊间"空笼右键野生小动物入笼"机制不存在于原版——笼由捕获小动物
//      物品 + 玻璃水族箱合成（Recipe 链），放置前物种身份已在物品侧确定。
---

  // =============== 回退：旧统一肩后悬停近似（表外 proj id 用） ===============
  // 登记缺口（本次升级后残留的近似项）：
  //  ① Wisp(211)/ShadowOrb(18) 的控制键偏移（controlUp/Down ±40、controlLeft/Right
  //    ±120）——ownerRef 无输入态，未建模；
  //  ② 764 UpbeatStar 透明度脉冲、1050 AxeFairyPet 砍树行为、653 同伴方块岩浆
  //    尖叫/黑暗戳人、1090 彩虹巨石微光粒子——纯视觉/彩蛋，未移植；
  //  ③ 地面族逐款帧窗口（958 行走 5-12、825 待机表情轮盘等）与 208 鹦鹉 0.95
  //    水平阻尼、1027 波浪帧段——按家族通用规则近似；
  //  ④ AI_026 抚摸(petting)交互帧、尘/Gore 特效未移植。
  private legacyAI(p: OwnerRef): void {
    // 目标位：玩家肩后（朝向反向 ×22px，头侧 -26px）+ 正弦浮动（±4px，0.06/t）
    const bob = Math.sin(this.animTick * 0.06) * 4;
---

// ============================================================================
// GAP 处置台账（2026-08-13 尾项清零批）
//   ① KiteLogic/DrawKite —— 已对齐：KiteLogic（Projectile.cs:45809-46036）全量
//     入 LeashedKiteEntity.kiteLogic；DrawKite（Main.cs:36614-37069）全量入
//     Renderer.drawLeashedKite（24 型绳索参数表 KITE_ROPE_PARAMS + FishingLine
//     锚绳分段 + Extra 尾条 + oldPos 拖尾）。收放线（:45816-45837 channel −5 /
//     controlUseItem +5）经源码证实 owner==Main.myPlayer 才走——LeashedKite 恒
//     owner=255（MoveKite :168）→ 锚桩风筝原版即无收放输入，等价（不移植）。
//     残留：HandleMovement 的 SlopeCollision 坡面贴合段从略（生成期坡面罕见）；
//     风筝无碰撞音效（kiteSoundPitch 计算无消费端，:45845-45854 owner!=myPlayer
//     不播）。
//   ② DrawBubble —— 已对齐：Renderer.drawLeashedBubble（Gore_413 +
//     (isAquatic&&liquid<255)||(!isAquatic&&liquid>0) 判定，LeashedCritter.cs:200-205）。
//   ③ FindFrame —— 已对齐：拴绳全集 31 组 case（兔/金鱼/鸟/鹦鹉/鸮/鸭+泳姿/
//     海鸥/鼠/蛙/龟/海马/蝎/松鼠/企鹅/蚱蜢/松露虫/萤火虫/微光之灵/蜻蜓/蝶/蠕虫/
//     夜爬虫/蜗牛/妖精/水黾/瓢虫+椿象/河豚）逐条件入 findFrame；spriteDirection
//     覆写持久、rotation 覆写证实被 Draw 期 CopyToDummy 重置（:176）→ 绘制只取
//     rotationScalar 档（蝶族 vx*0.3 已据此移除）。
//   ④ ShimmerFly 拖尾 + Dust —— 已对齐：oldPositions（TrailCacheLength[677]=60）
//     每帧右移入 shiftShimmerTrail，绘制走 DrawNPCDirect_Faeling（Main.cs:26306-
//     26362）四列表 17 段环绕渐隐；尘改走原版 Dust 池（金系 43 带照度门 / Recall

```


---

## 🤖 Assistant · 2026-08-18T03:33:31.580Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '14,24p' ~/Project/GLM/SandboxWorld/game/src/ui/BestiaryPanel.ts; echo ---; sed -n '60,80p' ~/Project/GLM/SandboxWorld/game/src/world/JourneyPowers.ts; echo ---; sed -n '1,40p' ~/Project/GLM/SandboxWorld/game/src/world/evolution/RuntimeEvents.ts; echo ---; sed -n '35,45p' ~/Project/GLM/SandboxWorld/game/src/world/audit/exemptions.ts",
 "description": "Read gap ledger headers in four files"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:33:31.679Z

**📎 ToolResult**

```
// 已闭合登记（数据层 → UI 消费）：
//   - 排序：Sort_BestiaryID（ContentSamples.NpcBestiarySortingId 九键链全键提取，
//     含 GetLowestBiomeGroupIndex）/ Sort_Rarity（NpcBestiaryRarityStars，npcStats 投影）
//   - 头像背景：IBestiaryBackgroundImagePathAndColorProvider（MapBG1-42 按出没环境
//     推导，偏好 AddTags/世界恶双路/月总特例；网格=首个带图条件，详情=末个+bgColor 着色）
// 登记缺口（后续批次）：
//   - Visuals.* 装饰叠层（MapBGOverlay1-9：Rain/Blizzard/Sun/Moon/Meteor 等）——
//     提取数据已含 derivations 推导规则，DOM 头像暂只铺底图不叠装饰层
//   - 筛选：稀有生物（RareSpawnBestiaryInfoElement）/ 群系 / 事件标签
import { upgradeToBitmap, USE_BITMAP } from '../assets/SpriteAtlas';
import { Lang } from '../i18n/Lang';
---

// ---------------------------------------------------------------------------
// 原版注册表（CreativePowerManager.Initialize :90-104）——id = PowerId = 世界存档
// 写入顺序；本仓实现状态见各条注释（登记 = 引擎级缺口，见报告）
// ---------------------------------------------------------------------------
export const JOURNEY_POWER_REGISTRY = [
  { id: 0, cls: 'FreezeTime', cfg: 'time_setfrozen', persist: 'world', status: 'implemented' },
  { id: 1, cls: 'StartDayImmediately', cfg: 'time_setdawn', persist: 'none', status: 'implemented' },
  { id: 2, cls: 'StartNoonImmediately', cfg: 'time_setnoon', persist: 'none', status: 'implemented' },
  { id: 3, cls: 'StartNightImmediately', cfg: 'time_setdusk', persist: 'none', status: 'implemented' },
  { id: 4, cls: 'StartMidnightImmediately', cfg: 'time_setmidnight', persist: 'none', status: 'implemented' },
  { id: 5, cls: 'GodmodePower', cfg: 'godmode', persist: 'player', status: 'implemented' },
  { id: 6, cls: 'ModifyWindDirectionAndStrength', cfg: 'wind_setstrength', persist: 'none', status: 'implemented' },
  { id: 7, cls: 'ModifyRainPower', cfg: 'rain_setstrength', persist: 'none', status: 'implemented' },
  { id: 8, cls: 'ModifyTimeRate', cfg: 'time_setspeed', persist: 'world', status: 'implemented' },
  { id: 9, cls: 'FreezeRainPower', cfg: 'rain_setfrozen', persist: 'world', status: 'implemented' },
  { id: 10, cls: 'FreezeWindDirectionAndStrength', cfg: 'wind_setfrozen', persist: 'world', status: 'implemented' },
  { id: 11, cls: 'FarPlacementRangePower', cfg: 'increaseplacementrange', persist: 'player', status: 'implemented' },
  { id: 12, cls: 'DifficultySliderPower', cfg: 'setdifficulty', persist: 'world', status: 'implemented' },
  { id: 13, cls: 'StopBiomeSpreadPower', cfg: 'biomespread_setfrozen', persist: 'world', status: 'implemented' },
  { id: 14, cls: 'SpawnRateSliderPerPlayerPower', cfg: 'setspawnrate', persist: 'player', status: 'implemented' },
---
// 运行时世界事件三件套 1:1（Terarria1456 反编译源为唯一标杆）——运行时审计台账
// 六缺口的三个系统落点（调用方 = core/Game.ts）：
//   ① setFireFlyChance（NPC.cs:94557-94610）：每夜 StartNight 重掷萤火虫/蝴蝶/椿象
//      生成概率（Main.cs:64706 调用）。原版写 NPC 静态位；本仓落 World 字段
//      （fireFlyChance/fireFlyFriendly/fireFlyMultiple/butterflyChance/stinkBugChance）
//      并按台账要求随存档。
//      ★任务台账曾写 jewelBeetleChance——1.4.5.6 原文无该字段（1405 亦无），实际
//      五件套为 fireFly×3 + butterfly + stinkBug，以原文为准。
//   ② CultistRitual（CultistRitual.cs 全文）：地牢拜月教石碑 437 自然重生计时。
//      Main.cs:64427 每帧 UpdateTime；delay 随存档（WorldFile.cs:1340 写 / :2192 读，
//      缺省 86400 = delayStart——新世界 ResetTempsToDayTime WF:1018 / v108 前旧档
//      WF:2188 同值），recheck 为运行时静态位不落盘。
//   ③ MysticLogFairiesEvent（MysticLogFairiesEvent.cs 全文）：倒木（tile 488）桩
//      附近夜放仙女。Main.cs:64710 StartNight / :64433 每帧 UpdateTime /
//      WorldGen.cs:3303 OnWorldLoad StartWorld / :49866 KillTile FallenLogDestroyed。
// 近似项（原版依赖系统缺失，逐一注明）：
//   - PlayerLOS（CultistRitual.TrySpawning / MysticLogFairies 的落点隐藏性）→
//     玩家 50 格内视为可见（WorldEvolution.playerLOS 同款近似；原版 WorldGen.cs:
//     69500-69515 实为"点矩形 ∩ 屏幕×1.2 矩形"，非视线判定）
//   - RNG 流勘误（2026-08-13 复核）：1.4.5.6 里 WorldGen.genRand 与 Main.rand
//     是**同一条流**（WorldGen.cs:4391 赋值一次），并非两条流——本文件单
//     Math.random 流按原版掷序消费统计等价，仅损失种子可复现性
//   - remixWorld（地牢 Y 基准翻转 / 仙女时间窗豁免 / 倒木扫描带翻转）本仓无该
//     种子体系 → 恒 false
import type { World } from '../World';
import type { TileStore } from '../TileStore';
import { TILE_BY_KEY } from '../../data/tiles';

/** 倒木 tile（TileID 488 FallenLog；SurfaceDecorPasses place3x2 同一来源） */
const FALLEN_LOG = TILE_BY_KEY['v_488_fallen_log'] ?? 0;

// ============================================================
// ① setFireFlyChance（NPC.cs:94557-94610）
// ============================================================
/** C# UnifiedRandom.Next(n)（0..n-1） */
const next = (n: number): number => Math.floor(Math.random() * n);
/** C# UnifiedRandom.Next(lo, hi)（lo..hi-1，上界开区间） */
const nextRange = (lo: number, hi: number): number => lo + Math.floor(Math.random() * (hi - lo));

/**
---
]);
// ★存【残片/形态差】不进本表(规则层),由 tests/world-invariants.test.ts 集成组的
//  FRAGMENTS 白名单+计数基线管理(新类型/同类暴增必红):
//  v_529_sea_oats(原版单格写入 cs:58333)、pot/26(残片语义疑点,KillTile 整块清
//  未接通)、186/187(多带表帧语义)、105 雕像/411 起爆器/103 bowls/crystal_heart。

```


---

## 🤖 Assistant · 2026-08-18T03:37:11.034Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have enough material. Let me curate the final list. Constraint: ≤200 items, grouped by file, priority core → entities → world → render → others. Classify A (fully missing feature, player-perceivable), B (behavior simplification / numeric approximation), C (pure visual/audio), D (multiplayer/save edge cases).

Let me carefully go through what I have and select the meaningful items, excluding:
- Registration-table descriptive uses (登记表/登记箱子 etc.)
- Geometric "缺口" (1px seams, grass overlay gaps)
- Stale/closed notes (销核/退役/已过期/已闭合/已对齐)
- "近似" that's just describing method names... no, actually 近似 items count as B (numeric/behavior approximations) or C (visual). I'll select the significant ones.

Let me curate by file:

### src/core
1. constants.ts:7-18 — GRAVITY 偏差登记：维持 0.4；NPC 深度缩放修正未移植，留待重力专项 — B
2. Sfx.ts:48 — sandstormWind ★登记缺失：原版沙暴无专属 wav，素材缺失登记 — C
3. Sfx.ts:150 — 未登记=1.0 音量修正 — informational, skip? It's about registry semantics — skip.
4. Game.ts:296 — 4703 四管固定 8 原版 π/2 旋转扰动近似同表 — B
5. Game.ts:590-591 — 3643 大琥珀 CTF 族物品未注册（CTF 模式未实装，引擎级缺口登记）— A (CTF mode missing)
6. Game.ts:1091 — TE OnRemoved 时机差异备案（服务器即时 vs 本仓）— D
7. Game.ts:1163 — 右键取回拴绳小动物是本仓扩展交互——备案 — informational (documented deviation) — D maybe. Keep as D.
8. Game.ts:1229 — 未知 vanillaId 数据表缺口只丢一条 — data robustness; skip or B. It's a data gap note. I'll skip (defensive).
9. Game.ts:1338 — 龙卷 tag 近似收紧（中途入视野按快照恢复）— B
10. Game.ts:1410 — teamTank 冷却/减伤以独立字段近似（计划备案）— B
11. Game.ts:1420 — 消耗/甲虫壳等 Hurt 内副作用未模拟（登记）— B
12. Game.ts:1510 — 熔岩石 accfx 未登记直接扫槽 — B
13. Game.ts:1550 — includeSelf 死亡观战未接 — D (spectate)
14. Game.ts:1580 — gfxOffY 未建模取 0 — B
15. Game.ts:1593 — NoMoreTargets 相机推挤未实装（屏震近似暂略）— C
16. Game.ts:1945 — dead 门近似 — B
17. Game.ts:2065 — 后备两档矿车为无装备槽 UI 近似 — B
18. Game.ts:2119 — 热喷泉 443 登记，15 tick 采样近似 — B
19. Game.ts:2267 — lastMouseInterface/inventory 门近似 — B
20. Game.ts:2629 — EmitDust 四色按格数加权（曾用区旗近似 — historical, but the note is "曾用" → the current is correct. Skip! It says 曾用区旗近似 meaning now fixed.) Actually line reads "四色按【格数】加权（曾用区旗近似）" — current implementation is correct, past was approximation. EXCLUDE per user's instruction.
21. Game.ts:3007 — 687 城镇史莱姆黄 → 683 链无对应实体（未实装，登记）— A
22. Game.ts:3008 — 11/463 AttemptToConvertNPCToEvil 未接（登记）— A/B (bunny/penguin conversion) — B (partial)
23. Game.ts:3263 — 床危险/血月/日食门近似重置 — B
24. Game.ts:3330 — oceanDepths 以 zoneBeach 同式近似 — B
25. Game.ts:3366 — 盒 = NPC 中心对屏盒求交 cx/cy 对玩家中心近似 — B
26. Game.ts:3569 — combat 表无 useTurn 列（提取器回填登记遗留）— B (data extraction gap)
27. Game.ts:4093 — renderer 侧脉冲近似 — C
28. Game.ts:4357 — 全组号 -1/-2 近似交由 despawn 收尾 — B
29. Game.ts:4559 — luck 字段近似（玩家±640px 单机）— B
30. Game.ts:4786 — 狙击镜配饰门未接（登记）；lastMouseInterface 门 uiBlocking 近似 — A/B. 狙击镜右键 zoom未接 — A (player can perceive missing sniper scope zoom). 
31. Game.ts:4864 — 4.5 格泛光近似省略 — C
32. Game.ts:4872 — 曾近似 6 档 — historical → EXCLUDE.
33. Game.ts:4925 — 曾为静态近似/六色跳变 — historical → EXCLUDE.
34. Game.ts:5090 — essScale 未跟踪取 1 近似（登记）— B
35. Game.ts:5278 — 旧 0.5/t+0.8 封顶是自造近似，位图字体对齐时归位 — current still 自造? It says 旧…自造近似 → planned fix. The note: "旧 0.5/t+0.8 封顶是 monospace 时代自造近似,位图字体对齐时一并归位" — current approximation still in effect, pending bitmap font. — B (UI scroll). Keep.
36. Game.ts:5412 — 无数据→30 中位近似（useAnimation）— B
37. Game.ts:5505 — 虚空袋 bank4 路径无载体（登记）— A (void bag missing) — actually "虚空袋 bank4 路径无载体" = void bag storage missing — A.
38. Game.ts:5506 — 硬核档未接（掉钱链最小实现）— B
39. Game.ts:5550-5551 — buffs 无槽上限（登记偏离）；光宠/vanityPet 互斥与 603 收藏版门未接（登记）— B
40. Game.ts:5654 — KillTile_PlaySounds 四档近似 — C
41. Game.ts:5658 — (全表 1:1 登记遗留) — skip, ambiguous. Skip.
42. Game.ts:5667 — CopyPaintAndCoating 涂料复制未建模（涂装系统缺席）— A (coating system missing)
43. Game.ts:5860 — 反重力未实装 — A (gravity reversal potions/buckets) — player perceivable.
44. Game.ts:5880 — pendingItemReuse 未实装 — B
45. Game.ts:6036 — 爱心尘近似 — C
46. Game.ts:6360 — -1（无限）沿用 3 近似 — B
47. Game.ts:6930 — 回归药水 4870：床/回归点 stash 未实装→出生点近似 — B (recall potion goes to spawn instead of bed)
48. Game.ts:6971-6972 — LimitPointToPlayerReachable/AnyWallOfTypeOnLine 未移植；teleportToMouse 就近落点 BFS 近似 — B
49. Game.ts:7012 — RerollVariation 变体系统未实装（公告备案）— A (pet reroll) — actually it announces fallback. A.
50. Game.ts:7029 — 换装失败语义近似（备案）— B
51. Game.ts:7307 — 单发化 DPS 曾差 3-8 倍 — historical context, current fixed. EXCLUDE.
52. Game.ts:7511 — 持物近似（holdout 画枪）— C
53. Game.ts:7962 — delegate 成功格尘/音近似 — C
54. Game.ts:8051 — 插入序近似 cheapest-first — B
55. Game.ts:8090 — 地面型判定省略统一飞行（walk 近似后续细分）— B
56. Game.ts:8144 — 248 箭物理 grav 0.3，射出音 Item17 未提取 GAP — C (sound missing) — "射出音未提取" = missing sound asset — C.
57. Game.ts:8186 — 配重球曾直线坠落 — historical "曾" → but line 8190 says 1:1 now. EXCLUDE both.
58. Game.ts:8475 — 食人鱼枪 1156 → 弹 190 GAP G3 行为层：直飞 Arrow 表达不了 — A (Piranha Gun behavior missing)
59. Game.ts:8554 — reuseDelay2 = useTime 52 近似 — B
60. Game.ts:8869 — 平台族锤循环（坡面/楼梯）未接入——依赖登记 — A (hammer platform slopes/stairs missing)
61. Game.ts:9027 — killTileBreakSound 四档近似 — C
62. Game.ts:9092 — 弹 655 蜂巢未实装——登记跳过 — A
63. Game.ts:9096 — TreeGrowFX_AshShake 粒子近似 — C
64. Game.ts:9114 — NPC 数据表缺口静默丢弃 — skip (defensive) — actually it's a data gap. Skip.
65. Game.ts:10201 — KillWall_DropItems 墙掉落表未移植 — A/B (walls don't drop items) — B.
66. Game.ts:10214 — 墙尘近似 — C
67. Game.ts:10259 — 涂层系统未建（4668/5344）惰性 — A (coating items no effect)
68. Game.ts:10474 — 平台/火把/篝火/箱/柜 style 族分支 :39299-39349 登记未接 — B
69. Game.ts:10488 — tileCut 族由 decor 近似覆盖 — B
70. Game.ts:10612-10613 — 全量锚点表未提取，"邻格有内容"近似 — B
71. Game.ts:10791 — 开关 UI 未实装登记 GAP（公告盒？）wait context: line 10791 "(开关 UI 未实装,登记 GAP);无线/同色不耗;上漆在冷却前" — about teleporter? Let me not overthink: "开关 UI 未实装" — A (lever/switch UI?). Actually context is likely pressure plate/teleporter. I'll summarize generically.
72. Game.ts:11009 — 5395 屎堆物品未注册，粒子近似+登记引擎级缺口 — A
73. Game.ts:11027 — killClothier 旗标未持久化，登记 — D (save gap)
74. Game.ts:11033 — 屎堆 5395 vi_ 未注册——物品侧缺口登记 — A (dup of 11009; combine)
75. Game.ts:11186 — CanSnapToPosition 畅通检查未移植（登记）— B
76. Game.ts:11216 — RemoveSpawn 未移植——无原始出生点存档,登记 — D (spawn removal persistence)
77. Game.ts:11933 — 压板 135 白名单由 critters 桶近似 — B
78. Game.ts:11980 — atmo 玩家深度线性近似 — C (ambience volume)
79. Game.ts:12134 — 雷声按距离衰减近似 — C
80. Game.ts:12153 — 视觉光效由粒子近似 — C
81. Game.ts:12345 — 陷阱族发射音=敲石近似 — C
82. Game.ts:12789 — 倾倒实心门仓库近似 — B
83. Game.ts:12880 — 传送族青尘近似 — C
84. Game.ts:12921 — MagicConch 近似取世界两缘 380 格带内地表落点 — B
85. Game.ts:13276 — MouthPosition 近似 — B
86. Game.ts:13305 — 18×18 近似 marshmallow 串贴图 — C
87. Game.ts:13309 — 档本仓无手持槽，登记 — B
88. Game.ts:13403 — 泰坦手套未实装 scale 恒 1 — A (Titan Glove meleeScaleGlove) — item exists but effect missing — B? meleeScaleGlove ×1.1 未实装 — B (numeric missing → actually effect missing = A-ish; it's an accessory effect not working = A player perceivable). I'll mark A.
89. Game.ts:13483 — 网不砍草不打怪（金/防火网 cutExtraTiles 登记近似省略）— B
90. Game.ts:13543 — historical (旧"1-5 铜"近似已退役) — EXCLUDE.
91. Game.ts:13578 — 甲虫进攻套窗口刷新时间蓄能模型近似 — B
92. Game.ts:13580 — 派对浸剂彩纸纯视觉粒子近似 — C
93. Game.ts:13625 — 453 模式转桶；spawnBound 只交付占位体——589/685 — related to 14373. Keep one.
94. Game.ts:13693 — bound 态以 TownNPC 近似 → 反查登记 — B
95. Game.ts:13755 — historical (旧 zoneDesert 近似退役) — EXCLUDE.
96. Game.ts:14067 — 睡渔夫补放近似 — B
97. Game.ts:14146 — 兔/猫/狗 bought* 旗依赖许可证商店未实装，登记缺失 — A (pet license shop missing)
98. Game.ts:14198 — MushroomTileThreshold 现已 1:1 (备案 prior) — EXCLUDE (fixed).
99. Game.ts:14373 — bound TownNPC npcKey → 绑缚态反查表 (bound 近似) — B
100. Game.ts:14386 — HasNoPartyText 表未移植 — C (party text)
101. Game.ts:14516 — 射程门 = 各站点 IsWithinSnappngRangeToTile 近似统一 inTileRange — B
102. Game.ts:14718/14753/14772/14839 — NPC 对话文本若干未实现（血月 64/65、玩家头部时装 113、幸运/DD2 文本、巫医 DD2 档位）— C (dialog text gaps) — combine as one entry each file line? They're 4 separate lines. I'll list them individually but compact.
103. Game.ts:14912 — 旅行商人/骷髅商/钓鱼娃等非房屋 NPC 未注册不可达（bestiary housing? context shop?) — context is shop/housing text replacement. Hmm line 14912 "其余类型(旅行商人368/骷髅商453/钓鱼娃369 等非房屋 NPC 未注册,不可达)" — data gap. B.
104. Game.ts:14934 — 酒馆老板未实装,恒用类型名 — C (name display) — wait Bartender 550 未实装 = DD2 bartender NPC missing — A. Actually "酒馆老板未实装,恒用类型名" in a text replace context. The Bartender NPC itself may be missing — A.
105. Game.ts:15105 — 坐姿 +5 未跟踪（钓鱼）— B
106. Game.ts:15320/15325 — extract-shops 未捕获 if 门同类缺口直补 — B (data extraction gap, already patched in place). These are "已直补" so current OK — skip? The note says the extractor missed it and they patched directly — that's resolved. EXCLUDE.
107. Game.ts:15433 — 未实现事件门不上架（商店）— B
108. Game.ts:15504 — 入场怪近似 Boss 槽/世吞体节在场 — B
109. Game.ts:15533 — DangerThatPreventsOtherDangers 小集合未跟踪（登记 RuntimeEvents.ts）— B
110. Game.ts:15548 — WorldGen.PlayerLOS 近似 50 格内可见 — B
111. Game.ts:16123 — PunchCameraModifier 近似 — C
112. Game.ts:16170 — 折扣 0.8 未实装 discountAvailable 恒 false（登记）— B (shop discount missing)
113. Game.ts:16176 — boss 专属 debuff 排除表未实装（登记）— A/B — nurse remove debuff exclusion — B.
114. Game.ts:16360 — 608 追踪弹未实装,直伤近似,登记 — A
115. Game.ts:16407 — Arrow 无 ai 槽登记依赖 — skip (dependency note).
116. Game.ts:16433 — aiStyle 36 追踪 AI 未建模，瞄敌近似（登记）— A/B — B.
117. Game.ts:16525 — 无背包宝石，近似为不掉（extractinator gemsOnly）— B
118. Game.ts:16575 — 叠加取 ±8/±6 近似 — B
119. Game.ts:16664 — hurt 无伤害源参数，近似全部计入 — B
120. Game.ts:16697 — claimable 对话领取→自动授予近似,登记 — B
121. Game.ts:16712 — 气球碎块 Gore 近似粒子 — C
122. Game.ts:16900-16901 — 光宠 7 款恒发光近似暖光；逐款色差登记二期 — C
123. Game.ts:16968 — 摇杆无纵轴略朝上（移动端近似）— B/C — C.
124. Game.ts:17630-17638 — TreeGrowFX 绿叶爆散近似、成树沙沙声近似 — C
125. Game.ts:17793 — 门槛近似 — B
126. Game.ts:18210 — "非近似" — EXCLUDE.
127. Game.ts:19013 — netMode!=0 近似（队伍发色剂单机恒白）— B/D — B.
128. Game.ts:19257 — 圣骑士盾独立槽近似 + 狱火光环 per-owner — B
129. Game.ts:18612 — SpawnWOF 专用链暂不支持意图，维持访客拦截（备案）— A/D — intent API for WOF spawn — D? It's about spawn intents. B/D. I'll say D.
130. Game.ts:4659 — 3611 高尔夫球车坐骑未实装（等价边界）— A

That's a lot from Game.ts alone (~70). Too many; I should compress. The user allows up to 200 total. Game.ts is the biggest. I'll include most meaningful ones but merge trivially-visual ones.

Hmm, budget: Let me target ~150-170 entries total. I need to be disciplined.

Let me also finalize entities, world, render, and others.

### src/entities (select)
- MinionProj.ts:908 — 半砖 +8 未实装 — B
- MinionProj.ts:929 — AI_137_CanHit 两次弧线绕行未实装 — B
- bossAI_lategame.ts:145,190 — CultistDragonHead/Squidhead 两 AI 族未移植（登记），不召 — A
- bossAI_lategame.ts:251 — expert 基线未实装（闪电 num80−20）— B
- bossAI_dd2.ts:541 — 瞄准帧渲染未接仅保状态 — C
- ItemDrop.ts:349 — 成就项 RealEstateAndTownSlimes 未接（登记）— A (achievement)
- bossAI.ts:206 — 经典模式无传送暂不移植（专家专属传送）— B — actually "暂不移植传送" means slime king teleport missing in classic? It says 经典模式无传送(专家专属),暂不移植传送 — the expert teleport not ported. B.
- bossAI.ts:375 — ZombieMoan wav 未提取 → 略，登记 — C
- bossAI.ts:622 — 基线行为未建模无可挂载点,登记跳过 — B
- Enemy.ts:138 — ai0 恒 0 = 永远休眠（未移植时）— B
- Enemy.ts:329/353 — 弹 540 星尘孵化链未移植，登记缺口 — A
- Enemy.ts:543 — eow_dig 音轨未提取近似 — C
- Enemy.ts:729 — 染色门/鞭标 VFX 门未移植字段先行 — B
- Enemy.ts:841 — 魂镰 3006 未实装登记 GAP（SoulDrain）— A
- Enemy.ts:948 — Chippy 沙发召唤链未实装恒 false — B
- Enemy.ts:972 — debuff 自发光段未移植（批次B）— C
- Enemy.ts:1011 — ReflectProjectile 反向归属管线未接 — B
- Enemy.ts:1328 — shimmerTransparency 视觉渐隐未接（GAP）— C
- Enemy.ts:1604-1672 — 天空盒世界未实装（Skyblock 分支 6 处跳过）— A (skybox seed missing — but only for secret seed) — D? Skyblock is a secret seed feature. Classify A but note secret-seed. I'll merge to one entry.
- Enemy.ts:1854/1866 — 尘 228/41 视觉未接（登记）— C
- Enemy.ts:3316 — 同型个体分离/穿平台未移植（注释备案）— B
- Enemy.ts:3502 — getGoodWorld 350 未接入 — D (secret seed)
- Enemy.ts:4360 — 未接，登记 — need context. Skip? I don't have content. Let me keep with generic summary "命中链未接登记". Hmm I only have the grep line "未接，登记。 */" — insufficient. I'll fetch context for a few ambiguous ones? That'd cost more calls. I'll skip ambiguous ones lacking content.
- Enemy.ts:4755 — 光照层未接入小动物，备案 — C
- Enemy.ts:4869 — 四象限 rotation 视觉未接备案 — C
- Enemy.ts:4995 — 宝箱引导链（状态 2-7）需宝箱搜索基建未移植备案 — A (mimic/lunch box引导?) Actually "宝箱怪引导" — A.
- Enemy.ts:5912 — 红帽召唤链未实装恒 0 — B
- Enemy.ts:5962 — getGood+24+血肉墙同型双倍档未接（FTW 种子消费登记）— D
- Enemy.ts:6084-6085 — tile 50 放书系统缺失引擎级缺口（书怪 AI_FindNearbyBook 扫描恒空）— A
- Enemy.ts:6821 — CanHitLine 视线阻隔未接省略 — B
- Enemy.ts:6906 — 弹型覆写 1-8 表未接登记 — B
- Enemy.ts:7046 — 693 受击段未接登记 — B
- TownShot.ts:75 — 950 四层脉冲叠画未接登记 — C
- GorePiece.ts:575 — 联机远端玩家不在面，仅主角备案 — D
- bossAI_martian.ts:56 — 447 MartianDeathray 死光电报 AI 未实装→直飞代 — A
- projStatus.ts:8 — remix 秘密种子/附着态未跟踪 — D
- projStatus.ts:51 — 魂镰 3006 联动登记 GAP — A (dup with Enemy 841)
- projStatus.ts:98 — 未实装 buff 静默跳过 — B
- WeaponProj.ts:362 — 301 变调未建模（playSfxFiles 无 pitch 参数）— C
- WeaponProj.ts:378 — releaseUseItem 输入语义未建模（GAP,登记 docs）— B
- WeaponProj.ts:562 — 383 冲击波/HitTilesInACircle 未建模 — B
- WeaponProj.ts:1332/1478/1609 — GAP#8 系列（朝鼠标转面、撞墙坠落态、冲击波）— B (3 entries or 1). List as 3? Compact to 2 entries (1332, 1609).
- WeaponProj.ts:1725 — Item54 音效未提取登记 GAP — C
- WeaponProj.ts:2282 — 尘迹省略（粒子钩子未接）— C
- WeaponProj.ts:2369 — 浸剂链未接登记偏差 — B
- WeaponProj.ts:2499 — 953 DaybreakExplosion 未实装登记偏差 — B
- Minecart.ts:781 — 矿车无重力翻转（gravDir 翻转坐骑未实装）— B
- projTargets.ts:195 — getGoodWorld 星弹特例未接入 — D
- projTargets.ts:256-259 — deadMansSweater 减半未移植；creativeGodMode 未建模；buffImmune 早退独立缺口 — B
- projTargets.ts:316 — 未实装 buff 静默跳过 — B (dup projStatus:98)
- MissileProj.ts:18 — AI_009 回旋语义另案登记 — A/B — "另案登记" — A? It's magic missile old homing semantics — B.
- MissileProj.ts:572 — 近距档进入判定未建模登记偏差 — B
- TownNPC.ts:547 — Shimmered 档对话差分登记 GAP — C
- TownNPC.ts:916 — 城镇 buff 系统未建无载体 — A
- TownNPC.ts:919 — 变体贴图已接但对话差分未接（GAP）— C
- TownNPC.ts:953 — 变身尘/烟粒子未接（登记）— C
- TownNPC.ts:1428 — 550 扔麦酒/229 海盗表演未接（登记）— C
- TownNPC.ts:1595 — 登记未接 — ambiguous, skip.
- TownNPC.ts:1985 — dryadWard 荆棘反伤/HurtingBees 未接略 — B
- TownNPC.ts:2179 — 挥击态逐 tick 弧形判定未接（近似中段）— B
- WhipProj.ts:57 — TagEffectState 5478 计数链机制整块登记 GAP — A (whip tag counter missing)
- Mounts.ts:274 — AllowsWind 墙表白名单未实装有墙即挡风 — B
- Mounts.ts:279 — remix 世界反转未实装 — D
- Mounts.ts:790 — 55 爬墙族 UpdateAfterEquips 未实装登记 — A
- Mounts.ts:1891 — mount 61 仙灵武库色光纯装饰未建模登记 — C
- Mounts.ts:1917 — InAPlaceWithWind 未建模恒 0.5 档 — B
- Mounts.ts:2003 — 930 穿透 -1 弹跳/引信未实装 — B
- bossAI_queenbee_plantera.ts:432 — expert justHit 蓄力视线未建模登记 — B
- Dart.ts:1026 — rotation 自旋纯视觉未接登记 — C
- Arrow.ts:126 — 食人鱼 190 GAP G3 行为层（dup of Game 8475）
- Arrow.ts:182 — 1.4.5 已无武器射出未移植登记 — skip (dead code note). EXCLUDE.
- Arrow.ts:197 — scale 渐缩通道登记未接 — C
- Arrow.ts:837 — 雕像产怪 flag 未实装；ghostHurt 未接登记 — B
- Arrow.ts:991 — SetDummyItemTime 持物锁未接登记 GAP — B
- PetFollower.ts:22 — 表外 proj id 回退旧肩后悬停近似 — B
- PetFollower.ts:558-565 — 登记缺口块：①控制键偏移未建模 ②纯视觉/彩蛋未移植 ③帧窗口家族通用近似 ④petting 交互未移植 — 4 items (B/C/C/C)
- Portal.ts:57 — 细分集合未接入实心即挡 — B
- LeashedCritter.ts:665 — 测试确定性备案偏差 — skip (test infra). D.
- LeashedCritter.ts:690 — 编码差异备案（7bit→u16 等）— D (net encode)
- LeashedCritter.ts:1833 — 渲染层暂未接登记遗留项（GAP 台账⑤）— C — wait, the GAP ledger at 2551 says DrawKite 已对齐. 1833 might be stale? The ledger 2026-08-13 says aligned. But 1833 says "本仓渲染层暂未接". Contradiction — 1833 is likely older text. Risky; I'll note it as listed but possibly superseded. Actually I should trust ledger. Skip 1833? The instruction: only current gaps. The tail-clearing batch 2026-08-13 aligned things. I'll skip 1833 as superseded. Hmm, but safer to include with note. I'll skip to avoid noise.
- LeashedCritter.ts:2163 — SlopeCollision 坡面贴合段从略（登记备案）— B
- Bobber.ts:125 — 坐姿 +5 未接（登记）— B
- Bobber.ts:413 — 钓具箱族 accfx 未提取（按装备名判定）— B
- Player.ts:82 — 分层色阶不区分越界判定略偏宽（备案）— B
- Player.ts:280 — 312/365 登记持续期（效果端暂不接）— B
- Player.ts:976 — War Table buff 未实装暂缺 maxTurrets — B
- Player.ts:1381 — (RT-3000)/300 连续加成未实装登记 — B
- Player.ts:1394 — 闪亮石 0.75 档 skip；坐/睡 ×1.3 未实装 — B
- Player.ts:1484 — shimmerImmune 旗标来源未移植恒 false — B
- Player.ts:1583 — 十字盾族第 6 门未实装恒 0 — B
- Player.ts:1666 — 浅蓝近似 dust 34（sprite 粒子未实装）— C
- Player.ts:2253/2265 — downDash 未建模恒 false — B
- Player.ts:2759 — stoned 态未实装（摔伤分支）— B
- Player.ts:3148 — aiStyle 7 弹 Kill 段登记不适用 — skip (N/A note). EXCLUDE.
- Player.ts:3167 — ByOther(11)/(12) 文案包未移植→npc 归因 — C
- Player.ts:3960 — Boss 专属弹幕 371 等不可闪避源未移植 — B
- Player.ts:3975 — 反击 608 弹/冲撞命中消耗登记未接 — B
- SolarEruption.ts:10 — 单层近似双层视觉差异小备案 — C
- GrappleProj.ts:13 — 等价边界块 — need content. I have the header line only. It's "等价边界（与原版差异，见 tests/grapple.test.ts 头注）" — I'll include with generic summary D/B. Let me read a couple lines... I've already done many calls. I'll summarize generically as B.

Actually to be safe about GrappleProj and OldOnesArmy 等价边界 blocks, generic one-liners suffice.

### src/world (select)
- SceneMetrics.ts:139 — bestiary/刷怪上下文未接（本仓无消费端）— B
- SceneMetrics.ts:145 — 室外天气效应强度本仓天气渲染未接（登记）— C
- Wiring.ts:673 — 容器内容与门锁系统未接入恒按可杀 — A (door lock/container check missing → "杀" refers to? probably 能否摧毁/开门) — B.
- FurnitureItems.ts:181 — useStyle 提取缺口补丁（45 个金属工具族）— B (patched; resolved) — it says 补丁 exists → resolved. EXCLUDE? "useStyle 提取缺口补丁" — the patch is in place. EXCLUDE.
- LunarEvent.ts:132 — remix/getGood 深层支省略；PlayerLOS 未接入按 SolidTiles 判窗 — B
- Paint.ts:19 — 涂层存储/渲染链未建，涂层物品惰性（购买后无效果）登记 — A
- Paint.ts:104/129 — 涂层系统未建另行登记 — A (merge)
- FurnitureStyle.ts:55 — 388/389 高门与 617 遗物座未加专属 case（备案）— B
- JourneyPowers.ts:63 — 注册表逐条 status（登记=引擎级缺口）— need which are registered as gaps. I saw up to id 14 all implemented. Later entries may include 'registered'. I'll summarize: registry lists per-power status; some marked 登记. — B. Let me check quickly with grep for status: 'registered' in that file... worth one quick grep. I'll do it.
- golf/GolfState.ts:144-147 — 单人镜头语义未接（等价边界）；镜头跟随缓存未接 — D/B
- liquid/settle.ts:36 — 落水越 waterLine 转岩浆缺口（H 批备案）— B
- LiquidSim.ts:20 — NetMessage 广播=多人层未接 — D
- LiquidSim.ts:296 — 部分格仍按 style0 档判定（备案）— B
- World.ts:107 — 旗帜击杀计数随会话,存档登记未接 — D
- gen/vanilla/TileCleanupPass.ts:189 — 墙 87 extraLiquid 特殊种子分支未实装 — D
- GenSolid.ts:43-44,55 — UndergroundJungleTrees 头翻转/QuickCleanup 翻转缺失（备案）；特殊种子专属翻转不接线 — B/D
- OasisPass.ts:14 — 下游联动本轮不实现备案（pass 96 头段）— B
- OasisPass.ts:197 — skyblock/notTheBees 未建模 — D
- WorldGen.ts:728/731 — Webs pass(27) 未移植；Webs 后置既有偏差另案 — A (webs generation missing) — B.
- WorldGen.ts:779 — SmoothWorld 头还原窗口本仓数据无法表达备案 — B
- TrackPass.ts:17/377 — dualDungeons/errorWorld/notTheBees 分支未接 — D
- FinalCleanupPass.ts:10/25 — FillWallHoles 未实装备案跳过；DirtiestBlock 彩蛋备案跳过 — B/C
- BuriedChestsPass.ts:68 — properTopFrame 帧位不建模备案 — B
- MicroBiomesPass.ts:33/38 — 债务期箱位错位备案；帧落 0 渲染端备案 — B
- MicroBiomesPass.ts:188 — errorWorld 分支未建模 — D
- MushroomPass.ts:197 — FTW ×1.5 未接 — D
- TreePass.ts:223 — K 事件链实证零击杀备案省略 — B
- JungleShrinePass.ts:156 — 神龛内飞镖陷阱缺件备案 — B
- UndergroundJungleTreesPass.ts:3 — 世界状态缺丛林地下树（pass 缺失备案）— B
- QuickCleanupPass.ts:2 — 整 pass 曾缺失（已补） — the note at :2 says "整 pass 缺失（GenSolid.ts 备案…）" describing history; the pass now exists (file itself). EXCLUDE.
- TrapsPass.ts:70 — tile 重力未移植（巨石落下致动语义 1:1）— A (boulder falling not implemented) — B.
- PilesPass.ts:119 — noTrapsWorldGen 门备案 — D
- wiring/devices.ts:216 — AnnouncementBox 设置系统未接恒可用+全图 — B
- wiring/devices.ts:236 — 657 回声/658 微光/720 CRT/721 复古/725 黑白/733 收音机柱屏幕滤镜未接入 — C
- wiring/devices.ts:871-872 — 设置门未接恒全图；牌面文字编辑 UI 未接入（现存 signs 只读）— A (sign text editing UI missing!) — wait, UI.ts:445 says 保存写回 Sign 登记 with DOM textarea... contradictory. devices.ts:872 says 牌面文字编辑 UI 未接入（现存 signs 只读：墓碑/导入存档）— that's about announcement box text editing. Hmm. Announcement box text edit UI not available. A/B.
- SurfaceDecorPasses.ts:15/18 — CheckDye/CheckLog 等恒 no-op 未移植；秘密种子分支全部不触发未移植 — B/D
- SurfaceDecorPasses.ts:1260 — 518 CheckLilyPad 恒 no-op 未移植 — B
- SurfaceDecorPasses.ts:1772/1783 — 巨型蘑菇树未移植恒败零掷骰（C 组备案）— B
- HellFortPass.ts:127 — 箱登记不在 dump 四通道备案 — D
- evolution/WorldEvolution.ts:18/845 — Convert case 0 与 case 14-21 无消费方未移植 — B
- WorldEvolution.ts:389 — 海洋贝壳/内陆仙人掌（绿洲/海藻系统未接）— B
- WorldEvolution.ts:757/771 — 蘑菇树再生运行时接口未接 — B
- LivingTreePass.ts:261 — 备案见审计文档 — B
- StructuresPass.ts:1060-1062 — 绿洲棕榈 323/海滨燕麦/绿洲植物 530 段未实现（备案）— B
- HalfBrickPass.ts:9 — tileSolidTop 近似 !platform；495 特判未移植 — B
- GenState.ts:165 — 绿洲棕榈/海滨燕麦/绿洲植物未实现备案 — B (dup StructuresPass)
- spawn/VanillaSpawner.ts:2 — 简化纪律：未移植/近似须登记 docs/spawn-parity-gaps.md — meta note. Include as reference.
- VanillaSpawner.ts:629 — 677-679 安全变体未注册缺席=0 — B
- VanillaSpawner.ts:715 — 仙女 isNearFairy 倍率未实现（依赖仙女随从实体）登记 — B
- VanillaSpawner.ts:963 — 专家 1/30 例外未实装 — B
- VanillaSpawner.ts:1380 — 活跃玩家数未跟踪单人取 1 — D
- VanillaSpawner.ts:1437 — skyBehindPlayer/AnyDanger 上下文未跟踪 — B
- VanillaSpawner.ts:1546 — skyblock lowTiles 子档未建模备案 — D
- VanillaSpawner.ts:1610 — 注释已过时 — EXCLUDE.
- VanillaSpawner.ts:1645/1659 — 巨骨舌鱼此前未移植（now? "★此前未移植:困难模式丛林湖泊…" then presumably fixed — the note describes what was added. Ambiguous. It says 此前未移植 then presumably this pass added it. And 1659 救援链未实装（376→369 转换无）— A.
- VanillaSpawner.ts:1694 — Chum 物品/弹体 820 未注册恒 10 — B
- VanillaSpawner.ts:2057 — 书架实体系统未实现暂缺（693/694 书怪）— A
- VanillaSpawner.ts:2116 — skyblock lowTiles 档未建模恒 10 — D
- VanillaSpawner.ts:2175 — remix 未实装恒 65 — D
- VanillaSpawner.ts:2438 — AnyDanger 压制未实装恒放行（登记台账）— B
- VanillaSpawner.ts:2548 — SpawnOnPlayer 未移植以…近似 — B
- VanillaSpawner.ts:2663 — 节日未接→墓地单门（乌鸦）— B
- VanillaSpawner.ts:2712/2723 — skyblock/节日僵尸段省略 — D/B
- VanillaSpawner.ts:2838 — 影烛未实现 — B
- VanillaSpawner.ts:2847 — offensiveToTim buff 未接 — B
- VanillaSpawner.ts:3035 — remix 阈值未接恒 40 — D
- VanillaSpawner.ts:3088 — 万圣/圣诞史莱姆门（节日系统未移植备案）— B
- HiveSpiderPass.ts:680/781 — 存档时间线差异备案 — D
- RuntimeEvents.ts:2+ — 运行时审计台账六缺口三件套落点；近似项 PlayerLOS 50 格、单 Math.random 流损失种子可复现、remixWorld 恒 false — B (3 approx items)
- DungeonPass.ts:395/1296/2524 — properTopFrame 未建模备案；CanPound 全门近似 — B
- DungeonPass.ts:3781-3782 — Dome 体未转录另案，入口体以 Legacy 城堡近似 — B
- audit/exemptions.ts:39-41 — 残片/形态差白名单：pot/26 KillTile 整块清未接通、186/187 多带表帧语义、105 雕像/411 起爆器/103 bowls — B

### src/render (select)
- CursorItemIcon.ts:94-95 — FlexibleTileWand 分支未实装（碎块魔杖族 5324/5329/5330 放置系统缺,引擎级缺口登记）— A
- CursorItemIcon.ts:108 — 重命名链恒不进（引擎级缺口）— B
- CritterCage.ts:20-45 — GAP 登记块（放置链已闭环；残余 GAP：KiteLogic/DrawKite 近似、DrawBubble、逐型 FindFrame 登记在文件尾）— but ledger says aligned. The header 45 says 残余 GAP 登记在该文件尾. Mixed. I'll include as C with note.
- TileAnim.ts:42 — 原版逐列错相未接 — C
- VanillaTiler.ts:36 — 坡面圆角带(18+n)*18 超表宽未移植 — C
- VanillaTiler.ts:1263 — 518 按水位动态偏移未移植（备案）— C
- VanillaTiler.ts:1335 — 751 非锚点帧原版跳过绘制未移植 — C
- VanillaTiler.ts:1398 — AllowsWind 墙集合未提取保守近似 — B
- VanillaTiler.ts:1475 — 593 临时帧未移植 — C
- BiomeBackground.ts:478 — 逐 16px 切片光照未实装整行绘制近似 — C
- SkyRenderer.ts:1106-1118 — 柱背景天空贴图依赖登记 + FilterMoonLord shader 未接入 — C
- SkyRenderer.ts:1763 — bgColor 以本帧天空底色近似（登记）— C
- SkyRenderer.ts:2134 — 月总眼睛世界变换段恒等变换近似（登记：位置偏早）— C
- SkyRenderer.ts:2228 — 遮挡调制 sunVisibility 乘 intensity（登记：层级偏早）— C
- BreathMeter.ts:17-18 — gfxOffY 恒 0（坐骑未实装）；ingameOptionsWindow 分支未移植 — C
- MonolithFilters.ts:323 — dontStarveShader 药水 buff 引擎未接恒 false — B/C — the buff perspectivePlayer not implemented — C (visual) but buff missing is A-ish. Mark C.
- Renderer.ts:522 — gamePaused 冻结语义本仓无暂停态恒推进（差异登记）— B
- Renderer.ts:650 — 差异登记：113 ai[2] 放虫轮定帧 — C
- Renderer.ts:708 — 传送 5t 内错取带内高帧，差异登记 — C
- Renderer.ts:1742 — PvP 头顶血条备案偏差（原版无）— C (extra feature)
- Renderer.ts:2681 — halfBrick 贴地从略备案 — C
- Renderer.ts:3752 — 第二批已接（销核）— EXCLUDE.
- Renderer.ts:3890 — 光染色管线按全亮叠（差异登记）— C
- Renderer.ts:4270 — AI_003 无 425 ai3 瞄准蓄力（登记）— B
- Renderer.ts:4301 — AI_003 未写 lai3 旋转恒 0（登记）— C
- Renderer.ts:4716 — QueenSlime shader 残影/Extra_186 水晶未实装（素材/系统缺）— C
- Renderer.ts:4737/4766 — 出生紫雾 3 层叠画未实装（spawnAlpha 替代）×2 — C
- Renderer.ts:4751 — 投影层 row+18 半透明重绘；ai0==2 表情气泡未实装 — C
- Renderer.ts:5014 — 瞳孔静态居中（登记）— C
- Renderer.ts:5039 — 破体帧行缺 localAI[2]/[3] 取行 0（登记）— C
- Renderer.ts:6155 — 589 在 vanilla-npcs.json 缺登记（json 缺口族 588/633/663）— B
- Renderer.ts:6346 — Glow 变体档 S 备案 npcGlowVariantTex 接通 — C
- Renderer.ts:6640/6658 — bodyRotation 未建模取 0（登记）— B/C
- Renderer.ts:9156 — 世吞 134 多段质心平均未接画头段位置 — C
- InfoAccsLayer.ts:8 — 字体偏差登记（MouseText vs canvas+strokeText）— C
- TileFlames.ts:17/124/545 — 简化登记 blocks（S1/S3 已核销）— mostly resolved. 17 【简化登记】header — need status. The others say 已核销. Header 17 may list remaining. Skip or include generic. I'll include one entry noting header with 核销 status.
- VanillaLiquidRenderer.ts:597 — 坡面格与玻璃族双 pass 差异【简化登记】— C
- MapColors.ts:67 — SKY_FALLBACK 近似兜底 — C
- TileParticles.ts:85 — lightGate=20 二值门近似（登记）— C
- WaterfallRenderer.ts:58 — 视口外起点长瀑登记（functional, not gap）— EXCLUDE.
- heldProj.ts:29 — "恰好一致,非缺口" — EXCLUDE.
- EmoteBubble.ts:28 — byID 近似 — C
- ChunkCache.ts:512 — 涂色 16×16 格区域着色 vs 原版整张贴图（登记）— C/B — B.

### others
- ui/UI.ts:445 — 木牌编辑 DOM 近似（已接 Sign 写回）— resolved mostly; the note says implemented as DOM approximation. B/C — B (UI approximation).
- ui/UI.ts:831 — 一键装备 SwapEquip 近似 — B
- ui/UI.ts:1261 — 缺条目 fallback value 近似 — B
- ui/UI.ts:2094/2125/2416 — buff 悬停提亮/右键取消 CSS 近似 — C
- ui/UI.ts:2621 — 大师红绿脉冲未做偏差记录 — C
- ui/UI.ts:2658 — 鱼眼缩放 DOM 近似 — C
- ui/UI.ts:2859/2887 — 成就页 UI 未接 GAP — A
- ui/UI.ts:3013-3033 — buff 图标近似（近义物品图标）— C
- ui/UI.ts:3041 — ChatMonitor 未建消息缓冲 — B
- ui/HousingPanel.ts:43/124 — scale 近似、列换算近似 — C
- ui/BestiaryPanel.ts:19-22 — 登记缺口（后续批次）：Visuals 装饰叠层、稀有/群系/事件筛选 — C
- ui/BestiaryPanel.ts:1181 — 文本星近似 — C
- ui/ResearchUI.ts:6-7 — 献祭面板整包列表近似（偏差登记）— B
- ui/JourneyPowersUI.ts:7/20 — 横滑杆代竖滑杆偏差登记；点击抓取 UI 近似 — C/B
- ui/MobileControls.ts:289 — 坐骑（槽 3）引擎未实装（矿车除外）— A
- fx/VanillaDust.ts:15/26/184 — 链 A 命中者不乘 0.99 沿用既有近似 — B
- fx/VanillaDust.ts:243/260/285/289/297/441 — 备案不建（无消费方/无等价物）— C
- drops/NpcDrops.ts:16 — 遗留登记（非 luck 链缺口）— B
- drops/NpcDrops.ts:141/170/224/287 — remix/三王/具名/天空盒条件恒 false（系统未实装）— D/B
- drops/NpcDrops.ts:204 — 白天暴怒分支未实现 — B
- drops/NpcDrops.ts:290 — IsUsingSpecificAIValues 备案（无法精确实现）— B
- drops/NpcDrops.ts:516 — 未实现规则 kind warnOnce — B
- net/leashedSync.ts:12/51 — 差异备案（条带补发、线序）— D
- net/ClientNet.ts — 登记箱子 functional — EXCLUDE.
- player/HairDyeColor.ts:178 — effect 二进制缺口 — C
- player/SmartSelect.ts:47/148/304 — 油漆系统未建策略 no-op；反重力恒 1 — B
- player/SmartSelect.ts:59/479 — 提取缺口按原版补正（resolved）— EXCLUDE.
- player/PlayerSitting.ts:11-12 — 屎堆 5395 未注册；killClothier 未持久化 — A/D (dup Game 11027)
- player/SmartCursor.ts:80/1368/1771 — 油漆刮刀 no-op（涂层系统未建）；gravDir 恒 1 — B
- player/SmartCursor.ts:1811 — alchemy 缺省未接世界态等价语义 — B
- items/Inventory.ts:169 — 涂层惰性（dup Paint）— A
- items/LucyAxe.ts:7 — MP msg141 跨玩家同步未接（纯视觉）— D
- physics/TileCollision.ts:254 — 重跑校验本体未移植 — B
- physics/Conveyor.ts:38 — 传送带渲染层未接备案 — C
- lighting/lightTables.ts:40 — headcovered ×0.85 头埋方块未跟踪登记 — B
- lighting/LightingEngine.ts:120 — 小地图导出未移植（空槽）— C
- lighting/TileLightScanner.ts:40 — 涂装覆盖未实装恒走固定色 — B
- stats/Shimmer.ts:126 — decraft 完整移植替换 GAP（resolved）— EXCLUDE.
- stats/ScaleStats.ts:98/392 — DebuffTimeMultiplier/LightningPlayerDamageScaling 未消费暂不列；鞭标闪电粒子门未移植 — B/C
- stats/Luck.ts:38/108 — 风筝/恶臭 buff 授予物品未移植登记 — B
- stats/SellChain.ts:40 — shopCustomPrice 未实装恒回落 item.value — B
- stats/Buffs.ts:12 — debuff 系统未移植对冲分支暂缺 — B
- stats/Buffs.ts:47/49/50 — 磨刀石/附魔台/战争桌 buff 枚举登记但效果未接（穿甲/maxMinions/maxTurrets）— A/B — these are buff sources (sharpening station etc.) — A.
- stats/Buffs.ts:104/108/111/160/167/172 — 吸血弹链/风筝/lady bug/隐身敌怪索敌/光衰减未接登记 — B (merge several)
- stats/Buffs.ts:371 — 未实装 buff 返回 undefined 静默跳过 — B
- stats/Buffs.ts:410/428/456/478-480 — vampireSeed/slime 翻倍、NurseCannotRemoveDebuff 排除表、种子系统未实装、buff 图标秒数 UI 未接 — B
- mainFlow.ts — 登记世界槽位 functional — EXCLUDE.

OK. That's a huge amount. I must compress to ≤200. Realistically I'll produce ~180 entries. Let me count as I structure.

I also want a quick check on JourneyPowers registry statuses (which are registered as gaps) — one quick grep. And Sfx.ts:48 already have. Let me do that one grep, then write the report.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:37:11.473Z · glm-x-preview-260804

```
补一个快查：JourneyPowers 注册表中哪些标记为缺口。
```


---

## 🤖 Assistant · 2026-08-18T03:37:13.048Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"status: 'registered'\\|status: 'partial'\\|status: 'gap'\\|登记\" ~/Project/GLM/SandboxWorld/game/src/world/JourneyPowers.ts | head -30",
 "description": "Check JourneyPowers registry gap statuses"
}
```


---

## 👤 User(sidechain) · 2026-08-18T03:37:13.129Z

**📎 ToolResult**

```
63:// 写入顺序；本仓实现状态见各条注释（登记 = 引擎级缺口，见报告）
94: *  读档后滑杆落在整档位——偏差登记：原版持久化滑杆原始 float */

```


---

## 🤖 Assistant · 2026-08-18T03:40:17.592Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK so no 'registered' statuses visible in grep — most implemented; line 94 has a deviation note (slider float persistence → integer steps). Good.

Now write the final report. Structure: grouped by directory/file, each entry `file:line | 标记类型 | summary | 分类`. Then totals A/B/C/D.

Let me carefully build and count. I'll be selective and compress visual/audio near-duplicates into single lines covering multiple ids where sensible (but each line = one grep hit ideally). Target under 200.

Let me draft per file with classification:

SRC/CORE:

core/constants.ts:7 — GRAVITY 偏差登记 — B
core/constants.ts:14-18 — NPC 重力深度缩放未移植，留待重力专项 — B
core/Sfx.ts:48 — sandstormWind 素材缺失登记（无专属 wav） — C
core/Game.ts:296 — 4703 四管固定 8，π/2 旋转扰动近似同表 — B
core/Game.ts:590 — 3643 大琥珀/夺旗族物品未注册（CTF 模式未实装，引擎级缺口） — A
core/Game.ts:1091 — TE OnRemoved 时机差异备案 — D
core/Game.ts:1163 — 拴绳右键取回为本仓扩展（备案） — D
core/Game.ts:1338 — 龙卷 tag 近似收紧② — B
core/Game.ts:1410 — teamTank 冷却/减伤独立字段近似（计划备案） — B
core/Game.ts:1420 — 甲虫壳等 Hurt 副作用未模拟 — B
core/Game.ts:1510 — 熔岩石 accfx 未登记直扫配饰槽 — B
core/Game.ts:1550 — 死亡观战 includeSelf 未接 — D
core/Game.ts:1580 — gfxOffY 未建模取 0 — B
core/Game.ts:1593 — NoMoreTargets 相机推挤未实装（屏震近似暂略） — C
core/Game.ts:2065 — 矿车后备两档无装备槽近似 — B
core/Game.ts:2119 — 热喷泉 443 以 15tick 采样近似逐帧扫描 — B
core/Game.ts:2267 — lastMouseInterface/inventory 门近似 — B
core/Game.ts:3007 — 687 城镇史莱姆黄链无实体（未实装登记） — A
core/Game.ts:3008 — 11/463 兔/企鹅邪化转换未接（登记） — B
core/Game.ts:3263 — 床危险/血月/日食门近似重置 — B
core/Game.ts:3330 — oceanDepths 以 zoneBeach 同式近似 — B
core/Game.ts:3569 — combat 表无 useTurn 列（提取器遗留） — B
core/Game.ts:4357 — 全组号 -1/-2 近似由 despawn 收尾 — B
core/Game.ts:4559 — 单机 luck 字段近似 ±640px 邻域 — B
core/Game.ts:4659 — 3611 高尔夫球车坐骑未实装（等价边界） — A
core/Game.ts:4786 — 狙击镜右键 zoom 门未接（登记） — A
core/Game.ts:4864 — 附 4.5 格泛光近似省略 — C
core/Game.ts:5090 — essScale 未跟踪取 1（登记） — B
core/Game.ts:5278 — 字号缩放 0.5/t+0.8 封顶为自造近似，待位图字体归位 — B
core/Game.ts:5412 — useAnimation 无数据取 30 中位近似 — B
core/Game.ts:5505 — 虚空袋 bank4 无载体（登记） — A
core/Game.ts:5506 — 硬核档 QuickHeal 分支未接（最小实现） — B
core/Game.ts:5550 — buffs 无槽上限（登记偏离）；光宠/vanityPet 互斥与 603 收藏版门未接 — B
core/Game.ts:5667 — CopyPaintAndCoating 未建模（涂装缺席） — A
core/Game.ts:5860 — 反重力 gravDir 未实装 — A
core/Game.ts:5880 — pendingItemReuse 未实装 — B
core/Game.ts:6360 — 无限 -1 沿用 3 近似 — B
core/Game.ts:6930 — 回归药水床/回归点 stash 未实装→出生点近似 — B
core/Game.ts:6971 — LimitPointToPlayerReachable/墙线检查未移植；就近落点 BFS 近似 — B
core/Game.ts:7012 — 宠物 RerollVariation 变体系统未实装（公告备案） — A
core/Game.ts:7029 — 换装失败语义近似（备案） — B
core/Game.ts:7511 — 600 holdout 持物近似 — C
core/Game.ts:8051 — cheapest-first 插入序近似 — B
core/Game.ts:8090 — 地面 3 件 walk 近似（后续按 aiStyle 细分） — B
core/Game.ts:8144 — 248 箭射出音 Item17 未提取（GAP） — C
core/Game.ts:8475 — 食人鱼枪 1156→弹 190 GAP G3 行为层（直飞 Arrow 代） — A
core/Game.ts:8869 — 平台坡面/楼梯锤循环未接入（依赖登记） — A
core/Game.ts:9092 — 弹 655 摇树蜂巢未实装（登记跳过） — A
core/Game.ts:10201 — KillWall_DropItems 墙掉落表未移植 — B
core/Game.ts:10259 — 涂层 4668/5344 系统未建（惰性） — A
core/Game.ts:10474 — 平台/火把/篝火/箱/柜 style 族分支未接 — B
core/Game.ts:10612 — TileObjectData 全量锚点表未提取（邻格近似） — B
core/Game.ts:10791 — 开关 UI 未实装（登记 GAP） — A
core/Game.ts:11009 — 屎堆 5395 物品未注册（粒子近似+引擎级缺口） — A
core/Game.ts:11027 — killClothier 旗标未持久化（登记） — D
core/Game.ts:11186 — CanSnapToPosition 畅通检查未移植 — B
core/Game.ts:11216 — RemoveSpawn 未移植（无原始出生点存档） — D
core/Game.ts:11933 — 压板 135 白名单以 critters 桶近似 — B
core/Game.ts:11980 — atmo 深度线性近似；雷声距离衰减近似(12134) — C (merge 12134)
core/Game.ts:12789 — 倾倒实心门仓库近似 — B
core/Game.ts:12921 — MagicConch 对侧海滩 380 格带近似 — B
core/Game.ts:13276 — MouthPosition 近似 — B
core/Game.ts:13305 — marshmallow 18×18 近似串贴图 — C
core/Game.ts:13403 — 泰坦手套 meleeScaleGlove ×1.1 未实装 — B
core/Game.ts:13483 — 金/防火网 cutExtraTiles 登记近似省略 — B
core/Game.ts:13578 — 甲虫进攻套窗口时间蓄能模型近似 — B
core/Game.ts:13693 — bound 态以 TownNPC 近似（反查表 14373） — B
core/Game.ts:14067 — 睡渔夫补放近似 — B
core/Game.ts:14146 — 兔/猫/狗许可证商店未实装（bought* 旗缺失） — A
core/Game.ts:14386 — HasNoPartyText 表未移植 — C
core/Game.ts:14718 — NPC 对话：血月 64/65、时装 113、幸运/DD2、巫医 DD2 档未实现（4 行合并） — C
core/Game.ts:14934 — 酒馆老板 550 未实装恒用类型名 — A
core/Game.ts:15105 — 钓鱼坐姿 +5 未跟踪 — B
core/Game.ts:15433 — 商店未实现事件门不上架 — B
core/Game.ts:15533 — DangerThatPreventsOtherDangers 小集合未跟踪 — B
core/Game.ts:15548 — WorldGen.PlayerLOS 50 格近似 — B
core/Game.ts:16123 — PunchCameraModifier 鹿角怪震屏近似 — C
core/Game.ts:16170 — 商店折扣 0.8 未实装（discountAvailable 恒 false） — B
core/Game.ts:16176 — boss 专属 debuff 护士排除表未实装 — B
core/Game.ts:16360 — 弹 608 追踪弹未实装（直伤近似） — A
core/Game.ts:16433 — aiStyle 36 追踪 AI 未建模（瞄敌近似） — B
core/Game.ts:16525 — 无背包宝石，提取器 gemsOnly 近似不掉 — B
core/Game.ts:16664 — hurt 无伤害源参数近似全部计入 — B
core/Game.ts:16697 — 奖励 claimable 自动授予近似 — B
core/Game.ts:16900 — 光宠 7 款恒定暖光近似（逐款色差登记二期） — C
core/Game.ts:17630 — TreeGrowFX 绿叶爆散/沙沙声近似（17638） — C
core/Game.ts:18612 — SpawnWOF 意图链暂不支持（访客拦截备案） — D
core/Game.ts:19013 — 队伍发色剂单机恒白（netMode 近似） — D
core/Game.ts:19257 — 圣骑士盾独立槽近似+狱火光环 per-owner — B

That's 96 entries for core alone. Too many. I need to trim core to ~55-60. Cut some minor B/C approximations: 2267, 3263, 3330, 4357, 4864, 5412, 6360, 7511, 8051, 11980, 12789, 13276, 13305... hmm. But the user did ask for comprehensive coverage up to 200. Total budget 200. core is the biggest file; give it ~60, entities ~45, world ~45, render ~30, others ~20 = 200. Tight.

Let me trim core to the most important. I'll drop the most trivial B-approximations (keep ones tied to gameplay):
Drop: 2267, 3263, 3330, 4357, 4864, 5412, 6360, 8051, 12789, 13276, 13305, 11980 (keep as merged C? drop), 1510, 1580.
Keep list (~78 → trim to ~62):

Final core list (62):
1. constants.ts:7 GRAVITY 偏差登记维持 0.4 — B
2. constants.ts:14 NPC 重力深度缩放未移植留待专项 — B
3. Sfx.ts:48 sandstormWind 素材缺失 — C
4. Game.ts:296 4703 四管固定 8 近似 — B
5. Game.ts:590 CTF 族物品未注册（引擎级缺口） — A
6. Game.ts:1091 TE OnRemoved 时机差异 — D
7. Game.ts:1163 右键取回扩展（备案） — D
8. Game.ts:1338 龙卷 tag 快照近似 — B
9. Game.ts:1410 teamTank 独立字段近似 — B
10. Game.ts:1420 甲虫壳 Hurt 副作用未模拟 — B
11. Game.ts:1593 观战相机推挤未实装 — C
12. Game.ts:2065 矿车后备档近似 — B
13. Game.ts:2119 热喷泉 15tick 采样近似 — B
14. Game.ts:3007 687 城镇史莱姆黄链未实装 — A
15. Game.ts:3008 兔/企鹅邪化转换未接 — B
16. Game.ts:3569 useTurn 列提取遗留 — B
17. Game.ts:4559 单机 luck 邻域近似 — B
18. Game.ts:4659 高尔夫球车坐骑未实装 — A
19. Game.ts:4786 狙击镜 zoom 门未接 — A
20. Game.ts:5090 essScale 取 1 — B
21. Game.ts:5278 字号自造近似待位图字体 — B
22. Game.ts:5505 虚空袋 bank4 无载体 — A
23. Game.ts:5506 硬核 QuickHeal 未接 — B
24. Game.ts:5550 buff 无槽上限+宠物互斥未接 — B
25. Game.ts:5667 涂料复制未建模 — A
26. Game.ts:5860 反重力未实装 — A
27. Game.ts:5880 pendingItemReuse 未实装 — B
28. Game.ts:6930 回归药水回出生点近似 — B
29. Game.ts:6971 传送可达性检查未移植（BFS 近似） — B
30. Game.ts:7012 宠物变体 RerollVariation 未实装 — A
31. Game.ts:7029 换装失败二掷近似 — B
32. Game.ts:8090 地面 walk 近似 — B
33. Game.ts:8144 箭射出音 Item17 未提取 — C
34. Game.ts:8475 食人鱼枪 GAP G3 — A
35. Game.ts:8869 平台锤循环未接入 — A
36. Game.ts:9092 弹 655 蜂巢未实装 — A
37. Game.ts:10201 墙掉落表未移植 — B
38. Game.ts:10259 涂层系统未建 — A
39. Game.ts:10474 style 族放置分支未接 — B
40. Game.ts:10612 锚点表未提取（邻格近似） — B
41. Game.ts:10791 开关 UI 未实装 — A
42. Game.ts:11009 屎堆 5395 未注册 — A
43. Game.ts:11027 killClothier 未持久化 — D
44. Game.ts:11186 CanSnapToPosition 未移植 — B
45. Game.ts:11216 RemoveSpawn 未移植 — D
46. Game.ts:11933 压板白名单 critters 桶近似 — B
47. Game.ts:12921 MagicConch 380 格带近似 — B
48. Game.ts:13403 泰坦手套效果未实装 — B
49. Game.ts:13483 网 cutExtraTiles 省略 — B
50. Game.ts:13578 甲虫窗口蓄能近似 — B
51. Game.ts:13693 bound 态 TownNPC 近似 — B
52. Game.ts:14146 宠物许可证商店未实装 — A
53. Game.ts:14386 派对文本表未移植 — C
54. Game.ts:14718+ 对话文本 4 处未实现 — C
55. Game.ts:14934 酒馆老板未实装 — A
56. Game.ts:15105 钓鱼坐姿 +5 未跟踪 — B
57. Game.ts:15433 商店事件门不上架 — B
58. Game.ts:15533 Danger 小集合未跟踪 — B
59. Game.ts:15548 PlayerLOS 50 格近似 — B
60. Game.ts:16170 折扣 0.8 未实装 — B
61. Game.ts:16176 护士 debuff 排除表未实装 — B
62. Game.ts:16360 弹 608 追踪弹未实装 — A
63. Game.ts:16433 aiStyle 36 追踪未建模 — B
64. Game.ts:16525 提取器宝石近似不掉 — B
65. Game.ts:16664 伤害源参数近似 — B
66. Game.ts:16697 奖励自动授予近似 — B
67. Game.ts:16900 光宠恒定暖光近似 — C
68. Game.ts:17630 成树 FX/音近似 — C
69. Game.ts:18612 SpawnWOF 意图拦截 — D
70. Game.ts:19013 队伍发色剂恒白 — D
71. Game.ts:19257 圣骑士盾槽近似 — B

71 core entries. Hmm. Plus entities ~40, world ~40, render ~25, others ~18 = 194. OK that works, tight. Let me trim core a bit more — drop 1338, 8090, 11933? I'll keep. Actually let me drop a few weak ones to be safe: drop #4 (296), #16 (3569), #21 (5278)? Keep — they're legit. I'll keep 71 but merge some (e.g., 14718 merge 4 lines into one entry). Fine.

Entities (~40):
1. MinionProj.ts:908 半砖+8 未实装 — B
2. MinionProj.ts:929 AI_137 CanHit 弧线绕行未实装 — B
3. bossAI_lategame.ts:145 教徒龙首/乌贼头两 AI 族未移植不召 — A
4. bossAI_lategame.ts:251 专家基线闪电参数未实装 — B
5. bossAI_dd2.ts:541 瞄准帧渲染未接 — C
6. ItemDrop.ts:349 成就 RealEstateAndTownSlimes 未接 — A
7. bossAI.ts:206 史莱姆王专家传送暂不移植 — B
8. bossAI.ts:375 ZombieMoan wav 未提取 — C
9. bossAI.ts:622 基线行为未建模跳过 — B
10. Enemy.ts:329 星尘 540 孵化链未移植（+353） — A
11. Enemy.ts:543 eow_dig 音轨近似 — C
12. Enemy.ts:729 染色/鞭标 VFX 门未移植（字段先行） — B
13. Enemy.ts:841 魂镰 SoulDrain GAP（projStatus.ts:51 同） — A
14. Enemy.ts:948 Chippy 沙发召唤链未实装 — B
15. Enemy.ts:1011 ReflectProjectile 管线未接 — B
16. Enemy.ts:1328 微光渐隐 shimmerTransparency 未接 — C
17. Enemy.ts:1604 天空盒 Skyblock 分支 6 处跳过 — D
18. Enemy.ts:3316 同型分离/穿平台未移植 — B
19. Enemy.ts:4755 光照层未接入小动物 — C
20. Enemy.ts:4995 宝箱引导链（状态 2-7）未移植 — A
21. Enemy.ts:5912 红帽召唤链未实装恒 0 — B
22. Enemy.ts:6084 tile 50 放书系统缺失（书怪扫描恒空） — A
23. Enemy.ts:6821 CanHitLine 视线阻隔未接 — B
24. Enemy.ts:6906 弹型覆写 1-8 表未接 — B
25. GorePiece.ts:575 联机远端玩家不在面 — D
26. bossAI_martian.ts:56 447 死光电报 AI 未实装直飞代 — A
27. projStatus.ts:8 remix/附着态未跟踪 — D
28. projStatus.ts:98 未实装 buff 静默跳过 — B
29. WeaponProj.ts:378 releaseUseItem 语义未建模（GAP#docs） — B
30. WeaponProj.ts:1332 GAP#8① 朝鼠标转面 — B
31. WeaponProj.ts:1609 GAP#8④ 撞墙冲击波 — B
32. WeaponProj.ts:1725 Item54 未提取 — C
33. WeaponProj.ts:2369 浸剂链未接 — B
34. WeaponProj.ts:2499 953 DaybreakExplosion 未实装 — B
35. Minecart.ts:781 gravDir 翻转坐骑未实装 — B
36. projTargets.ts:195 getGood 星弹特例未接入 — D
37. projTargets.ts:256 死人毛衣减半/创意上帝模式未建模 — B
38. MissileProj.ts:18 AI_009 回旋语义另案登记 — B
39. TownNPC.ts:547 Shimmered 对话差分 GAP — C
40. TownNPC.ts:916 城镇 buff 系统未建 — A
41. TownNPC.ts:1428 酒馆/海盗表演未接 — C
42. TownNPC.ts:1985 dryadWard 反伤/HurtingBees 未接 — B
43. TownNPC.ts:2179 挥击弧形判定近似 — B
44. WhipProj.ts:57 TagEffectState 5478 计数整块 GAP — A
45. Mounts.ts:274 AllowsWind 表未实装有墙即挡 — B
46. Mounts.ts:790 55 爬墙族坐骑未实装 — A
47. Mounts.ts:1891 mount 61 色光未建模 — C
48. Mounts.ts:1917 InAPlaceWithWind 恒 0.5 — B
49. Mounts.ts:2003 930 弹跳/引信未实装 — B
50. bossAI_queenbee_plantera.ts:432 expert justHit 视线未建模 — B
51. Arrow.ts:837 雕像产怪 flag 未实装/ghostHurt 未接 — B
52. Arrow.ts:991 SetDummyItemTime 持物锁未接 — B
53. PetFollower.ts:22 表外 proj id 回退悬停近似 — B
54. PetFollower.ts:558 登记缺口块 ①控制键偏移未建模 ②纯视觉彩蛋未移植 ③帧窗口通用近似 ④petting 交互未移植 — B
55. Bobber.ts:125 坐姿+5 未接 — B (dup Game 15105 — keep one; drop Game's)
56. Bobber.ts:413 钓具箱 accfx 未提取（按名判定） — B
57. Player.ts:82 色阶不区分判定偏宽 — B
58. Player.ts:280 312/365 持续期效果端不接 — B
59. Player.ts:976 War Table maxTurrets 未实装 — B
60. Player.ts:1381 RT-3000 连续加成未实装 — B
61. Player.ts:1394 闪亮石 0.75/坐睡 ×1.3 未实装 — B
62. Player.ts:1484 shimmerImmune 恒 false — B
63. Player.ts:1583 十字盾第 6 门恒 0 — B
64. Player.ts:2253 downDash 未建模 — B
65. Player.ts:2759 stoned 态未实装 — B
66. Player.ts:3167 ByOther 文案包未移植 — C
67. Player.ts:3960 不可闪避源未移植 — B
68. Player.ts:3975 反击消耗登记未接 — B
69. SolarEruption.ts:10 单层近似 — C
70. GrappleProj.ts:13 等价边界块 — B

That's 70 — too many for entities. Trim to ~45: drop 5, 8, 9, 11(C keep? drop), 15, 25... hmm. I'll cut: bossAI_dd2:541 (C, minor), bossAI.ts:375 (C minor), bossAI.ts:622, Enemy.ts:543, Enemy.ts:1011, Enemy.ts:3316, WeaponProj.ts:2369, Mounts.ts:1891, Arrow.ts:991, Player.ts:82, Player.ts:3167, SolarEruption.ts:10, GrappleProj.ts:13, MissileProj.ts:572 (not listed), projStatus.ts:98 (dup), Bobber.ts:125 (dup), MinionProj.ts:908 (minor)... 

Let me just target overall ~190 and distribute: core 62, entities 48, world 42, render 24, others 16 = 192. I'll trim during writing.

World (~42):
1. SceneMetrics.ts:139 bestiary/刷怪上下文无消费端 — B
2. SceneMetrics.ts:145 天气渲染未接 — C
3. Wiring.ts:673 门锁/容器内容未接入恒可杀 — B
4. LunarEvent.ts:132 remix/getGood 支省略+PlayerLOS 未接 — B
5. Paint.ts:19 涂层存储/渲染链未建（购买无效果） — A
6. Paint.ts:126 深浅漆等价边界（登记） — B
7. FurnitureStyle.ts:55 388/389 高门与 617 遗物座无专属 case — B
8. JourneyPowers.ts:94 滑杆持久化落整档位（偏差登记） — B
9. golf/GolfState.ts:144 单人镜头语义未接（等价边界） — D
10. liquid/settle.ts:36 落水转岩浆缺口（H 批备案） — B
11. liquid/LiquidSim.ts:20 液体 NetMessage 多人广播未接 — D
12. liquid/LiquidSim.ts:296 部分 style 档按 0 判定 — B
13. World.ts:107 旗帜击杀计数不随存档 — D
14. GenSolid.ts:43 UndergroundJungleTrees/QuickCleanup 翻转缺失（备案） — B
15. GenSolid.ts:55 特殊种子翻转不接线（备案） — D
16. OasisPass.ts:14 pass 96 下游联动不实现（备案） — B
17. WorldGen.ts:728 Webs pass 27 未移植 — B
18. TrackPass.ts:17 dualDungeons/errorWorld/notTheBees 未接 — D
19. FinalCleanupPass.ts:10 FillWallHoles 未实装备案跳过 — B
20. BuriedChestsPass.ts:68 properTopFrame 不建模 — B
21. MicroBiomesPass.ts:33 债务期箱位错位备案 — B
22. TrapsPass.ts:70 tile 重力未移植（巨石不落） — B
23. wiring/devices.ts:216 公告盒设置系统未接恒全图 — B
24. wiring/devices.ts:236 6 种屏幕滤镜（657/658/720/721/725/733）未接入 — C
25. wiring/devices.ts:872 公告盒文字编辑 UI 未接入（signs 只读） — A
26. SurfaceDecorPasses.ts:18 秘密种子分支全部不触发 — D
27. SurfaceDecorPasses.ts:1772 巨型蘑菇树未移植恒败 — B
28. evolution/WorldEvolution.ts:18 Convert case 0/14-21 未移植 — B
29. WorldEvolution.ts:389 贝壳/仙人掌（绿洲系统未接） — B
30. WorldEvolution.ts:771 蘑菇树再生运行时接口未接 — B
31. StructuresPass.ts:1061 绿洲棕榈 323/燕麦/植物 530 段未实现 — B
32. HalfBrickPass.ts:9 tileSolidTop 近似+495 特判未移植 — B
33. spawn/VanillaSpawner.ts:2 简化纪律：登记 docs/spawn-parity-gaps.md — meta
34. VanillaSpawner.ts:715 仙女 isNearFairy 倍率未实现 — B
35. VanillaSpawner.ts:963 专家 1/30 友好例外未实装 — B
36. VanillaSpawner.ts:1380 活跃玩家数未跟踪（单人取 1） — D
37. VanillaSpawner.ts:1659 睡渔夫 376→369 救援转换链未实装 — A
38. VanillaSpawner.ts:1694 Chum 物品/弹 820 未注册恒 10 — B
39. VanillaSpawner.ts:2057 书架实体系统未实现（693/694 书怪缺） — A
40. VanillaSpawner.ts:2438 AnyDanger 压制未实装恒放行 — B
41. VanillaSpawner.ts:2663 节日未接（乌鸦/节日僵尸 2712/2723/3088） — B
42. VanillaSpawner.ts:2838 影烛未实现 — B
43. evolution/RuntimeEvents.ts:24 近似项：PlayerLOS 50 格/单流 RNG/无 remix — B
44. DungeonPass.ts:3781 Dome 体未转录（Legacy 城堡近似，另案） — B
45. audit/exemptions.ts:39 pot/26 整块清未接通、186/187 帧语义等白名单 — B

Render (~24):
1. CursorItemIcon.ts:95 碎块魔杖族 5324/5329/5330 放置系统缺（引擎级缺口） — A
2. CursorItemIcon.ts:108 重命名链恒不进 — B
3. CritterCage.ts:20 GAP 登记块（尾部残余：Kite 近似/DrawBubble/FindFrame） — C
4. TileAnim.ts:42 逐列错相未接 — C
5. VanillaTiler.ts:36 坡面圆角带未移植 — C
6. VanillaTiler.ts:1263 518 水位偏移未移植（备案） — C
7. VanillaTiler.ts:1398 AllowsWind 墙集合保守近似 — B
8. BiomeBackground.ts:478 逐 16px 切片光照未实装（整行近似） — C
9. SkyRenderer.ts:1106 柱背景贴图+FilterMoonLord shader 依赖登记未接入 — C
10. SkyRenderer.ts:2134 月总眼恒等变换近似（位置偏早） — C
11. BreathMeter.ts:17 gfxOffY 恒 0（坐骑未实装） — C
12. MonolithFilters.ts:323 dontStarveShader buff 引擎未接恒 false — C
13. Renderer.ts:522 无暂停态恒推进（差异登记） — B
14. Renderer.ts:1742 PvP 头顶血条备案偏差 — C
15. Renderer.ts:4270 AI_003 无 425 ai3 蓄力（登记） — B
16. Renderer.ts:4716 QueenSlime shader 残影/Extra_186 未实装 — C
17. Renderer.ts:4751 表情气泡未实装 — C
18. Renderer.ts:6155 589 json 缺登记（缺口族 588/633/663） — B
19. Renderer.ts:6640 bodyRotation 未建模取 0 — B
20. Renderer.ts:9156 世吞质心平均未接（画头段） — C
21. InfoAccsLayer.ts:8 字体偏差登记 — C
22. VanillaLiquidRenderer.ts:597 坡面/玻璃双 pass 差异简化登记 — C
23. TileParticles.ts:85 lightGate=20 二值门近似（登记） — C
24. ChunkCache.ts:511 涂色按 16×16 格区域 vs 原版整张贴图（等价边界） — B
25. EmoteBubble.ts:28 byID 近似 — C
26. MapColors.ts:67 SKY_FALLBACK 近似 — C

Others (~16):
1. ui/UI.ts:831 一键装备 SwapEquip 近似 — B
2. ui/UI.ts:2859 成就页 UI 未接（GAP） — A
3. ui/UI.ts:3013 buff 图标近义物品近似（月噬/遮挡/食物/微光 353） — C
4. ui/UI.ts:2621 大师红绿脉冲未做 — C
5. ui/BestiaryPanel.ts:19 登记缺口：装饰叠层/稀有群系筛选（后续批次） — C
6. ui/ResearchUI.ts:6 献祭面板整包列表近似（偏差登记） — B
7. ui/JourneyPowersUI.ts:7 横滑杆代竖滑杆（偏差登记） — C
8. ui/MobileControls.ts:289 坐骑槽引擎未实装（矿车除外） — A
9. fx/VanillaDust.ts:243/260/285/289 备案不建（无消费方×4+雪密度计数） — C
10. drops/NpcDrops.ts:204 白天暴怒分支未实现 — B
11. drops/NpcDrops.ts:290 IsUsingSpecificAIValues 备案 — B
12. net/leashedSync.ts:51 线序差异备案 — D
13. physics/TileCollision.ts:254 重跑校验本体未移植 — B
14. lighting/TileLightScanner.ts:40 涂装覆盖未实装恒固定色 — B
15. stats/Buffs.ts:47 磨刀石/附魔台/战争桌 buff 枚举登记效果未接（:47/49/50） — A
16. stats/Buffs.ts:410 vampireSeed/slime 翻倍未移植（GAP） — B
17. stats/Luck.ts:38 风筝/恶臭授予物品未移植 — B
18. stats/SellChain.ts:40 shopCustomPrice 未实装 — B
19. player/SmartCursor.ts:80 油漆刮刀 no-op（涂层系统未建） — B
20. items/LucyAxe.ts:7 MP msg141 同步未接（纯视觉） — D

Counting A/B/C/D:

Core A: 590 CTF, 3007 687史莱姆, 4659 高尔夫车, 4786 狙击镜, 5505 虚空袋, 5667 涂料复制, 5860 反重力, 7012 变体, 8475 食人鱼枪, 8869 平台锤, 9092 弹655, 10259 涂层, 10791 开关UI, 11009 屎堆, 14146 许可证, 14934 酒馆老板, 16360 弹608 = 17
Core D: 1091, 1163, 11027, 11216, 18612, 19013 = 6
Core C: Sfx:48, 1593, 8144, 14386, 14718(合并), 16900, 17630 = 7
Core B: rest = 71-17-6-7 = 41

Entities A: bossAI_lategame:145, ItemDrop:349, Enemy:329, Enemy:841, Enemy:4995, Enemy:6084, bossAI_martian:56, TownNPC:916, WhipProj:57, Mounts:790 = 10
Entities D: Enemy:1604(skybox—secret seed → D), GorePiece:575, projStatus:8, projTargets:195 = 4
Entities C: Enemy:1328, Enemy:4755, TownNPC:547, TownNPC:1428, Mounts:1891 = 5
Entities B: rest.

Hmm wait, skybox: skyblock is a secret seed — the world can't be created with it (seed system 未实装), so it's unreachable content — classify D (edge/seed-gated). OK.

World A: Paint:19, devices:872, VanillaSpawner:1659, VanillaSpawner:2057 = 4
World D: GolfState:144, LiquidSim:20, World:107, GenSolid:55, TrackPass:17, SurfaceDecor:18, VanillaSpawner:1380 = 7
World C: SceneMetrics:145, devices:236 = 2
World B: rest.

Render A: CursorItemIcon:95 = 1
Render C: many.
Render B: VanillaTiler:1398, Renderer:522, Renderer:4270, Renderer:6155, Renderer:6640, ChunkCache:511 = 6

Others A: UI:2859 成就页, MobileControls:289 坐骑槽, Buffs:47 磨刀石三件 = 3
Others D: LucyAxe:7, leashedSync:51 = 2

Total A = 17+10+4+1+3 = 35
Total D = 6+4+7+0+2 = 19
C = core 7 + entities 5 + world 2 + render ~20 + others ~4 = ~38
B = rest.

Total entries: let me make sure ≤200. I'll finalize while writing and count precisely.

Let me count precisely as I write. I'll write the report now. Use compact format: `file:line | 类型 | 摘要 — 分类`. Group headers per directory.

Actually to keep it readable and within budget, I'll number nothing; just list. And final stats.

Let me count entries per file as I write, carefully:

CORE (I'll list 64):
constants.ts ×2, Sfx.ts ×1, Game.ts ×61.

Game.ts list (final, 61):
296, 590, 1091, 1163, 1338, 1410, 1420, 1593, 2065, 2119, 3007, 3008, 3569, 4559, 4659, 4786, 5090, 5278, 5505, 5506, 5550, 5667, 5860, 5880, 6930, 6971, 7012, 7029, 8090, 8144, 8475, 8869, 9092, 10201, 10259, 10474, 10612, 10791, 11009, 11027, 11186, 11216, 11933, 12921, 13403, 13483, 13578, 13693, 14067, 14146, 14386, 14718, 14934, 15105, 15433, 15533, 15548, 16170, 16176, 16360, 16433, 16525, 16664, 16697, 16900, 17630, 18612, 19013, 19257 — that's 69. Trim: drop 296, 1338, 3569, 8090, 11933, 14067, 16664, 19257, 5278, 7029 → 59. Hmm, keep some. Let me settle at ~58 for Game.ts.

Final Game.ts (58): 590, 1091, 1163, 1410, 1420, 1593, 2065, 2119, 3007, 3008, 3569, 4559, 4659, 4786, 5090, 5278, 5505, 5506, 5550, 5667, 5860, 5880, 6930, 6971, 7012, 8144, 8475, 8869, 9092, 10201, 10259, 10474, 10612, 10791, 11009, 11027, 11186, 11216, 12921, 13403, 13483, 13578, 13693, 14146, 14386, 14718, 14934, 15433, 15533, 15548, 16170, 16176, 16360, 16433, 16525, 16900, 17630, 18612, 19013 = 59 entries.

core total = 59 + 3 = 62.

Game.ts classification recount:
A: 590, 3007, 4659, 4786, 5505, 5667, 5860, 7012, 8475, 8869, 9092, 10259, 10791, 11009, 14146, 14934, 16360 → 17
D: 1091, 1163, 11027, 11216, 18612, 19013 → 6
C: 1593, 8144, 14386, 14718, 16900, 17630 → 6
B: 59−17−6−6 = 30

core: constants ×2 B, Sfx ×1 C → core totals: A17 B32 C7 D6 = 62 ✓

ENTITIES (final ~48):
MinionProj:908 B, MinionProj:929 B, bossAI_lategame:145 A, bossAI_lategame:190 A(同前合并→keep as one), bossAI_lategame:251 B, ItemDrop:349 A, bossAI:206 B, Enemy:329 A, Enemy:729 B, Enemy:841 A, Enemy:948 B, Enemy:1328 C, Enemy:1604 D, Enemy:3316 B, Enemy:4755 C, Enemy:4995 A, Enemy:5912 B, Enemy:6084 A, Enemy:6821 B, Enemy:6906 B, GorePiece:575 D, bossAI_martian:56 A, projStatus:8 D, projStatus:51 A(dup→skip, merged into Enemy:841), projStatus:98 B, WeaponProj:378 B, WeaponProj:1332 B, WeaponProj:1609 B, WeaponProj:1725 C, WeaponProj:2499 B, Minecart:781 B, projTargets:195 D, projTargets:256 B, MissileProj:18 B, TownNPC:547 C, TownNPC:916 A, TownNPC:1428 C, TownNPC:1985 B, TownNPC:2179 B, WhipProj:57 A, Mounts:274 B, Mounts:790 A, Mounts:1917 B, Mounts:2003 B, bossAI_queenbee_plantera:432 B, Arrow:837 B, PetFollower:22 B, PetFollower:558 B(块), Bobber:125 B, Bobber:413 B, Player:280 B, Player:976 B, Player:1381 B, Player:1394 B, Player:1484 B, Player:1583 B, Player:2253 B, Player:2759 B, Player:3960 B, Player:3975 B, GrappleProj:13 B.

Count: let me count: MinionProj2, lategame2, ItemDrop1, bossAI1, Enemy: 329,729,841,948,1328,1604,3316,4755,4995,5912,6084,6821,6906 =13, GorePiece1, martian1, projStatus: 8,98 =2, WeaponProj: 378,1332,1609,1725,2499 =5, Minecart1, projTargets: 195,256 =2, MissileProj1, TownNPC: 547,916,1428,1985,2179 =5, WhipProj1, Mounts: 274,790,1917,2003 =4, qb_plantera1, Arrow1, PetFollower2, Bobber2, Player: 280,976,1381,1394,1484,1583,2253,2759,3960,3975 =10, Grapple1.
Total = 2+2+1+1+13+1+1+2+5+1+2+1+5+1+4+1+1+2+2+10+1 = 59. Trim 11: drop Enemy:3316, Enemy:6906, projStatus:98, WeaponProj:1332 (merge with 1609 → keep 1609 only, mention ①④), Mounts:1917, Bobber:125 (merged into Game:15105? I dropped Game:15105 earlier — keep Bobber:125 instead), Player:1484, Player:1583, GrappleProj:13, MissileProj:18? Keep Missile (另案 is a keyword group the user asked). Keep GrappleProj (等价边界 keyword). Drop: Enemy:3316, Enemy:6906, projStatus:98, WeaponProj:1332, Mounts:1917, Player:1484, Player:1583, Player:280, bossAI:206, Minecart:781 → 10 dropped → 49.

Entities final 49: 
A: lategame:145, lategame:190? — merge to one entry (145) — so A: 145, ItemDrop:349, Enemy:329, Enemy:841, Enemy:4995, Enemy:6084, martian:56, TownNPC:916, WhipProj:57, Mounts:790 = 10
D: Enemy:1604, GorePiece:575, projStatus:8, projTargets:195 = 4
C: Enemy:1328, Enemy:4755, TownNPC:547, TownNPC:1428 = 4
B: 49−18 = 31

WORLD (final ~45):
SceneMetrics:139 B, SceneMetrics:145 C, Wiring:673 B, LunarEvent:132 B, Paint:19 A, Paint:126 B, FurnitureStyle:55 B, JourneyPowers:94 B, GolfState:144 D, settle:36 B, LiquidSim:20 D, LiquidSim:296 B, World:107 D, GenSolid:43 B, GenSolid:55 D, OasisPass:14 B, WorldGen:728 B, TrackPass:17 D, FinalCleanupPass:10 B, BuriedChestsPass:68 B, MicroBiomesPass:33 B, TrapsPass:70 B, devices:216 B, devices:236 C, devices:872 A, SurfaceDecorPasses:18 D, SurfaceDecorPasses:1772 B, WorldEvolution:18 B, WorldEvolution:389 B, WorldEvolution:771 B, StructuresPass:1061 B, HalfBrickPass:9 B, VanillaSpawner:715 B, VanillaSpawner:963 B, VanillaSpawner:1380 D, VanillaSpawner:1659 A, VanillaSpawner:1694 B, VanillaSpawner:2057 A, VanillaSpawner:2438 B, VanillaSpawner:2663 B, VanillaSpawner:2838 B, RuntimeEvents:24 B, DungeonPass:3781 B, audit/exemptions:39 B.

Count = 44. 
A: Paint:19, devices:872, VS:1659, VS:2057 = 4
D: GolfState:144, LiquidSim:20, World:107, GenSolid:55, TrackPass:17, SurfaceDecor:18, VS:1380 = 7
C: SceneMetrics:145, devices:236 = 2
B: 44−13 = 31

RENDER (final ~24):
CursorItemIcon:95 A, CursorItemIcon:108 B, CritterCage:20 C, TileAnim:42 C, VanillaTiler:36 C, VanillaTiler:1263 C, VanillaTiler:1398 B, BiomeBackground:478 C, SkyRenderer:1106 C, SkyRenderer:2134 C, BreathMeter:17 C, MonolithFilters:323 C, Renderer:522 B, Renderer:1742 C, Renderer:4270 B, Renderer:4716 C, Renderer:4751 C, Renderer:6155 B, Renderer:6640 B, Renderer:9156 C, InfoAccsLayer:8 C, VanillaLiquidRenderer:597 C, TileParticles:85 C, ChunkCache:511 B, EmoteBubble:28 C.
= 25. A:1 B:6 C:18.

OTHERS (final ~18):
ui/UI:831 B, ui/UI:2859 A, ui/UI:3013 C, ui/UI:2621 C, ui/BestiaryPanel:19 C, ui/ResearchUI:6 B, ui/JourneyPowersUI:7 C, ui/MobileControls:289 A, fx/VanillaDust:243 C(备案不建×5 合并), drops/NpcDrops:204 B, drops/NpcDrops:290 B, net/leashedSync:51 D, physics/TileCollision:254 B, lighting/TileLightScanner:40 B, lighting/lightTables:40 B, stats/Buffs:47 A, stats/Buffs:410 B, stats/Luck:38 B, stats/SellChain:40 B, player/SmartCursor:80 B, items/LucyAxe:7 D.
= 21. A:3 B:13 C:4 D:2... count: UI:831 B(1), UI:2859 A, UI:3013 C, UI:2621 C, Bestiary:19 C, ResearchUI:6 B, JourneyPowersUI:7 C, MobileControls:289 A, VanillaDust:243 C, NpcDrops:204 B, NpcDrops:290 B, leashedSync:51 D, TileCollision:254 B, TileLightScanner:40 B, lightTables:40 B, Buffs:47 A, Buffs:410 B, Luck:38 B, SellChain:40 B, SmartCursor:80 B, LucyAxe:7 D → A3 B11 C5 D2 = 21 ✓

TOTALS:
A = 17+10+4+1+3 = 35
B = 32+31+31+6+11 = 111
C = 7+4+2+18+5 = 36
D = 6+4+7+0+2 = 19
Total = 35+111+36+19 = 201. One over — drop one B (e.g. core Game:3569 useTurn). → 200 total, B=110.

Grand total 200. Perfect.

Now write the final answer. Format: grouped by directory, entries as `file:line | 标记 | summary | 分类`. Keep summaries tight with key ids. This will be long but that's what was requested.
```

</details>


---

## 🤖 Assistant · 2026-08-18T03:42:28.115Z · glm-x-preview-260804

```
扫描完成。365 个 .ts 文件全量 grep（关键词组 1-5），已剔除历史叙述（"曾用近似/旧 X/已退役/销核/已闭合/已过期"）与"登记表/登记箱子"这类功能性命名（非缺口），以及几何意义上的"缺口"（1px 发丝缝、草皮覆盖开孔等）。以下按重要性排序（core → entities → world → render → 其他），共 200 条。

# 未完成工作标记清单

## src/core（62 条）

**core/constants.ts**
- constants.ts:7 | 偏差登记 | GRAVITY 维持 0.4 不改 0.3（水体交互批结论） | B
- constants.ts:14 | 未移植/留待 | NPC 重力深度缩放修正未移植，全套移植留待"重力专项" | B

**core/Sfx.ts**
- Sfx.ts:48 | 登记缺失 | sandstormWind 无专属 wav（原版沙暴只有视觉 shader+BGM），素材入库前恒 null | C

**core/Game.ts**
- Game.ts:590 | 引擎级缺口 | 3643 大琥珀/夺旗 CTF 族物品未注册（CTF 模式未实装），按缺席等价为不掉 | A
- Game.ts:1091 | 备案 | TE OnRemoved 触发时机差异（原版服务器即时 vs 本仓延迟） | D
- Game.ts:1163 | 备案 | 拴绳小动物右键取回是本仓扩展交互（原版无） | D
- Game.ts:1410 | 近似/计划备案 | teamTank 冷却/减伤以独立字段近似（不吃常规无敌帧） | B
- Game.ts:1420 | 登记 | 消耗品/甲虫壳等 Hurt 内副作用未模拟（极端叠装场景） | B
- Game.ts:1593 | 未实装/暂略 | 死亡观战 NoMoreTargets 相机推挤未实装（屏震近似暂略） | C
- Game.ts:2065 | 近似 | 矿车装备后备两档为无装备槽 UI 时的近似；全无→木质车 13 | B
- Game.ts:2119 | 近似/登记 | 热喷泉 443 原版逐帧扫描，本仓 15 tick 采样近似 | B
- Game.ts:3007 | 未实装/登记 | 687 城镇史莱姆黄→683 链无对应实体 | A
- Game.ts:3008 | 未接/登记 | 11/463 AttemptToConvertNPCToEvil（兔/企鹅击杀邪化）未接 | B
- Game.ts:3569 | 提取遗留 | combat 表无 useTurn 列（提取器回填遗留），按 itemfunc 判定 | B
- Game.ts:4559 | 近似 | 单机以 luck 字段近似玩家±640px 邻域（原版 LadyBug 邻域扫描） | B
- Game.ts:4659 | 等价边界 | 3611 高尔夫球车坐骑未实装 | A
- Game.ts:4786 | 未接/登记 | 狙击镜右键 zoom 门（需配饰门）未接；lastMouseInterface 以 uiBlocking 近似 | A
- Game.ts:5090 | 登记 | essScale 未跟踪取 1 近似（亮晶簇/矿族 jitter、四柱魂缩放） | B
- Game.ts:5278 | 自造近似 | 字号 0.5/t+0.8 封顶是 monospace 时代自造近似，待位图字体对齐时归位 | B
- Game.ts:5505 | 登记 | 虚空袋 bank4 路径无载体 | A
- Game.ts:5506 | 未接 | 硬核档 QuickHeal 分支未接（掉钱链取最小实现） | B
- Game.ts:5550 | 登记 | buffs 无槽上限（偏离原版 maxBuffs 门）；光宠/vanityPet 互斥与 603 收藏版门未接 | B
- Game.ts:5667 | 未建模 | CopyPaintAndCoating 涂料复制未建模（涂装系统缺席） | A
- Game.ts:5860 | 未实装 | 反重力 gravDir 未实装（同 SmartCursor 口径恒 1） | A
- Game.ts:5880 | 未实装 | pendingItemReuse 未实装 | B
- Game.ts:6930 | 未实装/偏差 | 回归药水 4870：床/回归点 stash 未实装→传送出生点近似 | B
- Game.ts:6971 | 未移植/近似 | LimitPointToPlayerReachable/AnyWallOfTypeOnLine(350)/丛林蜥蜴墙 87 未移植；teleportToMouse 就近落点 BFS 近似 | B
- Game.ts:7012 | 未实装/备案 | 动物学家宠物 RerollVariation 变体系统未实装（公告兜底） | A
- Game.ts:8144 | GAP | 248 箭射出音 Item17 未提取 | C
- Game.ts:8475 | GAP G3 | 食人鱼枪 1156→弹 190 行为层：直飞 Arrow 表达不了回转链 | A
- Game.ts:8869 | 未接入/依赖登记 | 平台族锤循环（:45394-45440 平台坡面/楼梯）未接入 | A
- Game.ts:9092 | 未实装/登记 | 弹 655 摇树蜂巢（AI_016 裂蜂）未实装，登记跳过 | A
- Game.ts:10201 | 未移植 | KillWall_DropItems 墙掉落表未移植（旧墙不掉物） | B
- Game.ts:10259 | 未建 | 涂层系统（paintCoating 4668/5344）未建，涂层物品惰性无效果 | A
- Game.ts:10474 | 登记 | 平台/火把/篝火/箱/柜 style 族放置分支（:39299-39349）未接 | B
- Game.ts:10612 | 未提取/近似 | TileObjectData 全量锚点表未提取，以"邻格有内容或墙"近似 | B
- Game.ts:10791 | 未实装/GAP | 开关 UI 未实装（登记 GAP） | A
- Game.ts:11009 | 引擎级缺口 | 屎堆 5395 物品未注册（粒子近似 + 缺口登记，:11033 同） | A
- Game.ts:11027 | 未持久化/登记 | killClothier 旗标不随存档 | D
- Game.ts:11186 | 未移植/登记 | CanSnapToPosition 目标格畅通检查未移植（床位链已保证非实心） | B
- Game.ts:11216 | 未移植/登记 | RemoveSpawn 再点移除未移植（无原始出生点存档） | D
- Game.ts:12921 | 近似 | MagicConch 对侧海滩带近似取世界两缘 380 格带内找地表落点 | B
- Game.ts:13403 | 未实装 | 泰坦手套 meleeScaleGlove ×1.0 未实装（scale 恒 1） | B
- Game.ts:13483 | 近似省略 | 金/防火网 cutExtraTiles 登记近似省略（网不砍草不打怪） | B
- Game.ts:13578 | 近似 | 甲虫进攻套窗口刷新（beetleCounter）以时间蓄能模型近似 | B
- Game.ts:13693 | 近似 | bound 态以 TownNPC 近似（反查表见 :14373 BOUND_TOWN_NPC_ID） | B
- Game.ts:14146 | 未实装/登记缺失 | 兔 656/猫 637/狗 638 bought* 旗依赖许可证商店未实装 | A
- Game.ts:14386 | 未移植 | HasNoPartyText 表未移植（派对文本缺席） | C
- Game.ts:14718 | 未实现 | NPC 对话文本缺口 4 处：血月 64/65、头部时装 113、幸运/DD2 文本 151-155、巫医 DD2 档位（:14753/:14772/:14839） | C
- Game.ts:14934 | 未实装 | 酒馆老板 550 未实装，台词恒用类型名 | A
- Game.ts:15433 | 未实现 | 商店未实现事件门不上架（SetupShop if 门映射） | B
- Game.ts:15533 | 未跟踪/登记 | DangerThatPreventsOtherDangers 小集合未跟踪（登记 RuntimeEvents.ts） | B
- Game.ts:15548 | 近似 | WorldGen.PlayerLOS 近似：50 格内视为可见 | B
- Game.ts:16170 | 未实装/登记 | 商店折扣 0.8 未实装（discountAvailable 恒 false） | B
- Game.ts:16176 | 未实装/登记 | 护士可清 debuff 的 boss 专属排除表未实装 | B
- Game.ts:16360 | 未实装/登记 | 弹 608 追踪弹未实装（150×meleeDamage 直伤近似） | A
- Game.ts:16433 | 未建模/登记 | aiStyle 36 追踪 AI 未建模（初速扰动以瞄敌近似） | B
- Game.ts:16525 | 近似 | 提取器本仓无背包宝石→gemsOnly 近似为不掉 | B
- Game.ts:16664 | 近似 | hurt 无伤害源参数，环境击杀近似全部计入 | B
- Game.ts:16697 | 近似/登记 | 成就奖励 claimable+对话领取→本仓自动授予近似 | B
- Game.ts:16900 | 近似/登记二期 | 光宠 7 款（Fairy 等）恒定暖光 1.1/1.0/0.85，逐款色差登记二期 | C
- Game.ts:17630 | 近似 | TreeGrowFXCheck 成树绿叶爆散/沙沙声（:17638）近似 | C
- Game.ts:18612 | 暂不支持/备案 | SpawnWOF 专用链（舌头/推进多实体联动）意图暂不支持，维持访客拦截 | D
- Game.ts:19013 | 近似 | 队伍发色剂单机恒白（netMode!=0 近似） | D

## src/entities（49 条）

- MinionProj.ts:908 | 未实装 | 半砖落点 +8 未实装 | B
- MinionProj.ts:929 | 未实装 | AI_137_CanHit 两次弧线绕行视线判定未实装 | B
- bossAI_lategame.ts:145 | 未移植/登记 | CultistDragonHead/Squidhead 两 AI 族未移植，不召唤（:190 同，454/521 跳过） | A
- bossAI_lategame.ts:251 | 未实装 | 专家基线闪电 num80−20 未实装（g 按经典值调整） | B
- ItemDrop.ts:349 | 未接/登记 | 成就 CheckAchievement_RealEstateAndTownSlimes 未接 | A
- Enemy.ts:329 | 登记 | 星尘生物链：本仓无弹 540 孵化 AI（:353 同），≥600 ai[2] 归零不生效 | A
- Enemy.ts:729 | 未移植 | NPC 染色门 :92026 / 鞭标 VFX 门 :92135 未移植（字段先行保数据链） | B
- Enemy.ts:841 | 登记 GAP | 魂镰 3006 未实装（SoulDrainDebuff :91952-91979；projStatus.ts:51 同） | A
- Enemy.ts:948 | 未实装 | Chippy 沙发召唤链未实装→恒 false | B
- Enemy.ts:1328 | 未接 | 微光渐隐 shimmerTransparency 视觉侧未接 | C
- Enemy.ts:1604 | 未实装 | 天空盒 Skyblock 世界分支 6 处跳过（:1624/:1638/:1643/:1651/:1664/:1672 化石/生命水晶/矿桶等） | D
- Enemy.ts:4755 | 未接/备案 | 光照层未接入小动物（发光小动物白天不发光语义近似） | C
- Enemy.ts:4995 | 未移植/备案 | 宝箱怪引导链（状态 2-7）需宝箱搜索基建，未移植 | A
- Enemy.ts:5912 | 未实装 | 红帽骷髅召唤链未实装（redHat 恒 false→帧侧恒 0） | B
- Enemy.ts:6084 | 引擎级缺口 | tile 50 放书系统缺失（书怪 AI_FindNearbyBook 扫描恒空走兜底） | A
- Enemy.ts:6821 | 未接/省略 | CanHitLine 视线阻隔门未接 | B
- GorePiece.ts:575 | 备案 | 爆炸 gore 只判主角（联机远端玩家不在面） | D
- bossAI_martian.ts:56 | 未实装 | 447 MartianDeathray 死光电报 AI 未实装→直飞代 | A
- projStatus.ts:8 | 未跟踪 | remix 秘密种子/附着态未跟踪（'remixWorld→N' 等 3 类条件恒 false） | D
- WeaponProj.ts:378 | GAP/登记 | releaseUseItem 输入语义未建模（docs/weapon-proj-audit） | B
- WeaponProj.ts:1609 | GAP#8④ | 掷出态撞墙冲击波：原版两连，本仓单发（:1332 GAP#8① 朝鼠标转面未接） | B
- WeaponProj.ts:1725 | 未提取/GAP | Kill 爆尘伴生音效 Item54 未提取 | C
- WeaponProj.ts:2499 | 未实装/登记偏差 | 伴生弹 953 DaybreakExplosion 未实装（尘爆近似） | B
- Minecart.ts:781 | 未实装 | 矿车无重力翻转（gravDir 翻转坐骑未实装） | B
- projTargets.ts:195 | 未接入 | getGoodWorld 星弹 reflectsProjectiles 特例未接入（运行时 flag 恒 false） | D
- projTargets.ts:256 | GAP | "死人毛衣"减半未移植；creativeGodMode 字段未建模；buffImmune 早退独立缺口 | B
- MissileProj.ts:18 | 另案登记 | AI_009_MagicMissiles_Old :40753 回旋语义另案 | B
- TownNPC.ts:547 | 登记 GAP | Shimmered 档（StackedNPCProfile）对话差分（:919 同） | C
- TownNPC.ts:916 | 未建 | 城镇 buff 系统未建（摘 buff 353 无载体） | A
- TownNPC.ts:1428 | 未接/登记 | 酒馆老板扔麦酒(1/600)/海盗(1/600) 表演未接 | C
- TownNPC.ts:1985 | 未接/略 | 树妖 dryadWard 荆棘反伤与 HurtingBees 未接 | B
- TownNPC.ts:2179 | 登记 | 城镇 NPC 挥击态逐 tick 弧形判定未接（近似中段） | B
- WhipProj.ts:57 | 登记 GAP | TagEffectState 5478 计数链机制整块缺席（310 markedByScytheWhip 依赖） | A
- Mounts.ts:274 | 未实装 | AllowsWind 墙表白名单未实装（有墙即挡风） | B
- Mounts.ts:790 | 未实装/登记 | 55 爬墙族坐骑（UpdateAfterEquips :2967-2997）未实装 | A
- Mounts.ts:2003 | 未实装 | 930 穿透 -1 的弹跳/引信未实装（penetrate 1 近似） | B
- bossAI_queenbee_plantera.ts:432 | 未建模/登记 | 专家 justHit 蓄力越视线门未建模 | B
- Arrow.ts:837 | 未实装/未接 | 雕像产怪 flag 未实装；ghostHurt 幽灵伤害头 156 未接（登记） | B
- Arrow.ts:991 | 登记 GAP | 食人鱼 190 SetDummyItemTime 持物锁未接 | B
- PetFollower.ts:22 | 数据缺口 | 表外 proj id 回退旧"肩后悬停近似"（61 款已覆盖） | B
- PetFollower.ts:558 | 登记 | 残留近似块：①Wisp/ShadowOrb 控制键偏移未建模 ②764/1050/653/1090 纯视觉彩蛋未移植 ③地面族帧窗口/208 阻尼/1027 波浪帧段按家族通用近似 ④petting 抚摸交互未移植 | B
- Bobber.ts:125 | 未接/登记 | 钓鱼坐姿 +5 未跟踪（Tipsy +5 已接） | B
- Bobber.ts:413 | 未提取 | 钓具箱族 accfx 未提取（按装备名 2374/3721/2375 快速判定近似） | B
- Player.ts:976 | 未实装 | War Table buff 27 未实装暂缺 maxTurrets（Buffs.ts:50 同源） | B
- Player.ts:1381 | 未实装/登记 | 生命再生 (RT-3000)/300 连续加成未实装 | B
- Player.ts:1394 | 未实装 | 闪亮石 0.75 档 skip；坐/睡 ×1.3 再生档未实装 | B
- Player.ts:2253 | 未建模 | downDash（下跳冲刺）未建模恒 false（:2265 同） | B
- Player.ts:2759 | 未实装 | stoned 石化态未实装（摔伤分支同门不生效） | B
- Player.ts:3960 | 未移植 | Boss 专属弹幕 371 等不可闪避源未移植 | B
- Player.ts:3975 | 登记 | 反击 608 弹/冲撞命中消耗登记未接 | B
- GrappleProj.ts:13 | 等价边界 | 与原版差异块（见 tests/grapple.test.ts 头注；:117 Stoned/Webbed 恒 false） | B

## src/world（44 条）

- SceneMetrics.ts:139 | 登记 | 本仓尚无消费端（bestiary/刷怪上下文未接） | B
- SceneMetrics.ts:145 | 未接/登记 | 室外天气效应强度（风沙/雨 ±0.005/t）天气渲染未接 | C
- Wiring.ts:673 | 未接入/登记 | 门锁/容器内容检查未接入，恒按"可杀"处理 | B
- LunarEvent.ts:132 | 省略/未接入 | remix/getGood 深层支省略；PlayerLOS 未接入→只按 SolidTiles 判窗 | B
- Paint.ts:19 | 登记 | 涂层存储/渲染链未建，涂层物品购买后无效果 | A
- Paint.ts:126 | 等价边界（登记） | 深层漆 13-24 与浅层 1-12 在 paintColor（:43948-44061）的分层色阶不区分 | B
- FurnitureStyle.ts:55 | 备案 | 388/389 高门（TallGate）与 617 遗物座未加专属 case | B
- JourneyPowers.ts:94 | 偏差登记 | 滑杆持久化落整档位（原版持久化 float 原始值） | B
- golf/GolfState.ts:144 | 未接/等价边界 | 单人镜头语义未接（:147 镜头跟随缓存未接，无计分副作用） | D
- liquid/settle.ts:36 | 缺口（H 批备案） | 落水越 waterLine 转岩浆（Liquid.cs:177-190）未实现 | B
- liquid/LiquidSim.ts:20 | 未接 | 液体 NetMessage 广播=多人层未接 | D
- liquid/LiquidSim.ts:296 | 备案 | 部分 style 档按 style0 判定（报告 2-C 节） | B
- World.ts:107 | 登记 | 旗帜击杀计数随会话，不随存档 | D
- gen/vanilla/GenSolid.ts:43 | 缺 pass/备案 | UndergroundJungleTrees 头 379=true 与 QuickCleanup 137/130 翻转缺失（:44） | B
- gen/vanilla/GenSolid.ts:55 | 备案 | 特殊种子专属翻转（Pots/Traps 等）不接线 | D
- gen/vanilla/OasisPass.ts:14 | 不实现/备案 | pass 96 CactusPalmTreesAndCoral 头段下游联动未实现 | B
- gen/WorldGen.ts:728 | 未移植 | Webs pass 27 未移植（:731 既有 Webs 后置偏差另案） | B
- gen/vanilla/TrackPass.ts:17 | 未接 | dualDungeons/errorWorld/notTheBees 分支未接（:377 无 DungeonUtils） | D
- gen/vanilla/FinalCleanupPass.ts:10 | 备案跳过 | FillWallHoles 未实装（:25 DirtiestBlock 彩蛋审计裁决跳过） | B
- gen/vanilla/BuriedChestsPass.ts:68 | 不建模/备案 | properTopFrame 帧位不建模 | B
- gen/vanilla/MicroBiomesPass.ts:33 | 备案 | 债务期个别箱位/缺箱错位（docs 尾批 2-A；:38 帧落 0 渲染端备案） | B
- gen/vanilla/TrapsPass.ts:70 | 未移植 | tile 重力未移植（触板→致动→巨石落下不发生，数据 1:1） | B
- world/wiring/devices.ts:216 | 未接 | 公告盒 Disabled/Range 设置系统未接恒可用+全图（:871 同） | B
- world/wiring/devices.ts:236 | 依赖登记 | 657 回声/658 微光/720 CRT/721 复古/725 黑白/733 收音机柱屏幕滤镜未接入 | C
- world/wiring/devices.ts:872 | 未接入 | 公告盒牌面文字编辑 UI 未接入（现存 signs 只读：墓碑/导入档） | A
- gen/vanilla/SurfaceDecorPasses.ts:18 | 未移植 | 秘密种子分支（notTheBees/remix/frozen/extraLiquid）全部不触发 | D
- gen/vanilla/SurfaceDecorPasses.ts:1772 | 未移植 | 巨型蘑菇树未移植（恒败零掷骰，:1783 C 组备案） | B
- world/evolution/WorldEvolution.ts:18 | 未移植 | Convert case 0（纯净化墙链）与 case 14-21（1.4.4+ 反转换）无消费方（:845 同） | B
- world/evolution/WorldEvolution.ts:389 | 未接 | 海洋贝壳补充/内陆仙人掌（绿洲/海藻系统未接） | B
- world/evolution/WorldEvolution.ts:771 | 未接 | 蘑菇树再生 TryGrowingTreeByType(5) 运行时接口未接 | B
- gen/vanilla/StructuresPass.ts:1061 | 未实现/备案 | 绿洲棕榈 323/海滨燕麦/绿洲植物 530 段（cs:21129-21320）未实现（:1062） | B
- gen/vanilla/HalfBrickPass.ts:9 | 近似/未移植 | tileSolidTop 近似为 !platform；PlaceTile 495 特判未移植 | B
- world/spawn/VanillaSpawner.ts:2 | 纪律标记 | 任何"未移植/近似/恒X"须登记 docs/spawn-parity-gaps.md | （索引）
- VanillaSpawner.ts:715 | 未实现/登记 | 仙女 isNearFairy 倍率（:653-656）未实现（依赖仙女随从实体） | B
- VanillaSpawner.ts:963 | 未实装 | 专家 1/30 非友好例外未实装 | B
- VanillaSpawner.ts:1380 | 未跟踪 | 活跃玩家数未跟踪→单人取 1 | D
- VanillaSpawner.ts:1659 | 未实装 | 睡渔夫 376→369 救援转换链未实装（flags 亦无） | A
- VanillaSpawner.ts:1694 | 未实装 | Chum 物品未注册、无弹体 820→恒 10 | B
- VanillaSpawner.ts:2057 | 未实现 | 书架实体系统未实现（书怪 693/694 暂缺） | A
- VanillaSpawner.ts:2438 | 未实装/登记 | flag17 AnyDanger 压制未实装→恒放行 | B
- VanillaSpawner.ts:2663 | 未接 | 节日系统未接（乌鸦 301 走墓地单门；:2712/:2723/:3088 节日僵尸/史莱姆门） | B
- VanillaSpawner.ts:2838 | 未实现 | 影烛（蜡烛压制）未实现 | B
- evolution/RuntimeEvents.ts:24 | 近似项 | PlayerLOS 50 格近似；单 Math.random 流损失种子可复现；remixWorld 恒 false | B
- gen/vanilla/DungeonPass.ts:3781 | 另案 | 地牢 Dome 体未转录（WorldUtils 形状族另案），入口体以 Legacy 城堡近似 | B
- world/audit/exemptions.ts:39 | 白名单 | pot/26 KillTile 整块清未接通、186/187 多带表帧语义、105 雕像/411 起爆器/103 bowls/crystal_heart | B

## src/render（25 条）

- CursorItemIcon.ts:95 | 引擎级缺口 | 碎块魔杖族 5324/5329/5330 放置系统缺（:94 FlexibleTileWand 分支未实装） | A
- CursorItemIcon.ts:108 | 引擎级缺口 | 物品重命名链恒不进（勿误当悬停侧缺陷） | B
- CritterCage.ts:20 | 登记 | 笼/缸 GAP 登记块：放置链已闭环，残余 Kite 近似/DrawBubble/逐型 FindFrame 登记文件尾 | C
- TileAnim.ts:42 | 未接 | 原版逐列错相（TileDrawing :6007-6014 addFrY）未接 | C
- VanillaTiler.ts:36 | 未移植 | 坡面圆角带 (18+n)*18 超出 16 列表宽未移植 | C
- VanillaTiler.ts:1263 | 未移植/备案 | 518 按水位动态偏移未移植 | C
- VanillaTiler.ts:1398 | 未提取/近似 | AllowsWind 墙集合未提取（任何墙挡风保守近似） | B
- BiomeBackground.ts:478 | 未实装 | 逐 16px 切片光照（暗洞挖空/贴墙裁剪）未实装，整行绘制近似 | C
- SkyRenderer.ts:1106 | 依赖登记 | 四柱背景天空贴图 + FilterMoonLord 专用 shader 未接入（:1118 视觉近似点登记） | C
- SkyRenderer.ts:2134 | 近似/登记 | 月总眼睛世界变换段恒等变换近似（位置偏早；:2228 层级偏早） | C
- BreathMeter.ts:17 | 偏差记录 | gfxOffY 恒 0（坐骑未实装）；ingameOptionsWindow 分支未移植 | C
- MonolithFilters.ts:323 | 未接 | dontStarveShader 药水 buff（perspectivePlayer）引擎未接恒 false | C
- Renderer.ts:522 | 差异登记 | gamePaused 冻结语义：本仓无暂停态恒推进 | B
- Renderer.ts:1742 | 备案 | PvP 头顶血条为本仓扩展（原版无） | C
- Renderer.ts:4270 | 登记 | AI_003 无 425 ai3 瞄准蓄力（:4301 lai3 旋转恒 0） | B
- Renderer.ts:4716 | 未实装 | QueenSlime shader 残影(ai0==4)/Extra_186 水晶（素材/系统缺） | C
- Renderer.ts:4751 | 未实装 | ai0==2 表情气泡未实装（:4737/:4766 出生紫雾以 spawnAlpha 替代） | C
- Renderer.ts:6155 | json 缺口 | 589 缺登记（缺口族 588/633/663） | B
- Renderer.ts:6640 | 未建模/登记 | bodyRotation 未建模取 0（:6658 恒 0） | B
- Renderer.ts:9156 | 未接 | 世吞 134 多段质心平均（:55575-55589）未接，画头段位置 | C
- InfoAccsLayer.ts:8 | 偏差登记 | 字体：原版 MouseText vs 本仓 canvas+四向 strokeText | C
- VanillaLiquidRenderer.ts:597 | 简化登记 | 坡面格与玻璃族的双 pass 液体贴合差异简化 | C
- TileParticles.ts:85 | 近似/登记 | 光门以 lightGate=20 二值门近似（src/core 禁区） | C
- ChunkCache.ts:511 | 等价边界 | 涂色按 16×16 格区域 vs 原版按绘制调用整张贴图（多格家具只有被涂格显色） | B
- EmoteBubble.ts:28 | 近似 | 同一实体一次一个（原版 byID 近似） | C

## 其他目录（21 条）

- ui/UI.ts:831 | 近似 | 一键装备 SwapEquip/ArmorSwap :3022-3346 近似（部位→armor[0-2]） | B
- ui/UI.ts:2859 | 未接/GAP | 成就页 UI 未接（点击关闭替代；:2887 同） | A
- ui/UI.ts:2621 | 偏差记录 | 大师难度红绿脉冲未做（静态 α0.45 近似原版脉动） | C
- ui/UI.ts:3013 | 近似 | 环境 debuff 图标以近义物品图标近似（月噬/遮挡/食物三档/微光 353→银河珍珠 5340；:3170 同步份） | C
- ui/BestiaryPanel.ts:19 | 登记（后续批次） | Visuals 装饰叠层（MapBGOverlay1-9）不铺；稀有/群系/事件筛选缺 | C
- ui/ResearchUI.ts:6 | 偏差登记 | 献祭面板为整包列表近似（原版是背包内每物品按钮） | B
- ui/JourneyPowersUI.ts:7 | 偏差登记 | 横滑杆代原版竖滑杆（:20 抓取语义 UI 近似） | C
- ui/MobileControls.ts:289 | 未实装 | 坐骑槽 3 引擎未实装（矿车除外）仅提示 | A
- fx/VanillaDust.ts:243 | 备案不建 | 尘位移/风场两档无消费方（:260）；:285 10×10 盒≈本格；:289 snowDust 全屏计数无等价物；:297 减速均不设；:441 229 全亮基底近似 | C
- drops/NpcDrops.ts:204 | 未实现 | 白天暴怒（Enraged）掉落分支未实现 | B
- drops/NpcDrops.ts:290 | 备案 | IsUsingSpecificAIValues(Conditions.cs:27) 无法精确实现（当前 JSON 未用到） | B
- net/leashedSync.ts:51 | 备案 | 拴绳线序差异（锚格在 kind 前）；:12 条带补发差异备案 | D
- physics/TileCollision.ts:254 | 未移植 | :2003 重跑 TileCollision 校验本体未移植（分轴代价高） | B
- lighting/TileLightScanner.ts:40 | 未实装 | 涂装覆盖档恒走固定色 (0.37,0.8,1) | B
- lighting/lightTables.ts:40 | 未跟踪/登记 | headcovered ×0.85（头埋方块）未跟踪 | B
- stats/Buffs.ts:47 | 先登记 | 磨刀石 24 近战穿甲 / 附魔台 26 maxMinions / 战争桌 27 maxTurrets 枚举在但效果位未接（:49/:50） | A
- stats/Buffs.ts:410 | 登记 GAP | vampireSeed/slime 翻倍分支依赖未移植（:428/:478 同）；:456 护士排除表未实装；:480 buff 图标 <10t 秒数 UI 未接 | B
- stats/Luck.ts:38 | 登记 | 风筝/恶臭 buff 授予物品（4371/1332/弹 1080）未移植（:108 同） | B
- stats/SellChain.ts:40 | 未实装 | shopCustomPrice 恒回落 item.value | B
- player/SmartCursor.ts:80 | 未建 | 油漆刮刀策略 no-op（油漆/涂层系统未建，:1368 同） | B
- items/LucyAxe.ts:7 | 未接 | MP msg141 跨玩家同步未接（纯视觉本地生成） | D

# 总数统计（共 200 条）

| 分类 | 条数 | 说明 |
|---|---|---|
| **A 功能完全缺失（玩家可感知）** | **35** | 坐骑槽/高尔夫球车、狙击镜 zoom、虚空袋、涂层系统、食人鱼枪行为、平台锤循环、书架书怪、CTF 族物品、酒馆老板、许可证商店、魂镰/608 弹/教徒龙首/死光电报、公告盒编辑 UI、成就页 UI、磨刀石三件 buff、旗帜引导链等 |
| **B 行为简化/数值近似** | **110** | 占大头：PlayerLOS 50 格近似、luck 邻域近似、回归药水回出生点、墙不掉落、商店折扣恒 false、MagicConch 落点带、各提取器数据缺口回填近似等 |
| **C 纯视觉/音效** | **36** | 近义 buff 图标、滤镜/柱天空 shader、出生紫雾替代、若干 wav 未提取（Item17/Item54/ZombieMoan/eow_dig/sandstormWind）、尘/Gore 粒子近似等 |
| **D 多人/存档/种子等边角** | **19** | killClothier 不持久化、旗帜计数不落盘、液体/拴绳多人广播差异、Skyblock/remix/getGood/FTW 秘密种子分支恒 false、队伍发色剂恒白等 |

补充说明：
- TODO/FIXME/XXX/HACK 组零真命中（仅 bossAI.ts:630 `numXXX`、vanillaNpcs.ts:10 `AI_XXX` 两个标识符误报）。
- "等价边界"共 8 处声明（Game:4659/11622、GrappleProj:13/117、GolfState:144、ChunkCache:511、Paint:126、OldOnesArmy:23），多为有意裁剪的单机语义边界。
- 已核销/退役的历史项（如 Renderer.ts:3752 第二批 Glow 已接、LeashedCritter.ts:2551 台账 ①②③④ 已对齐、TileFlames S1/S3 核销）已按要求排除，但 CritterCage.ts:20 头注仍引用"残余 GAP 登记在文件尾"，与 LeashedCritter 台账的"已对齐"存在口径矛盾，建议人工复核哪份是最新状态。
```
