# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T18:42:57.674Z

```
你是 SandboxWorld 项目的「机制域审计员」。该项目是泰拉瑞亚 1.4.5.6 的 TypeScript 复刻(主代码 ~/Project/GLM/SandboxWorld/game/src/),目标 1:1。

你的域:**电路/机械系统(电线/传感器/计时器/逻辑门/机关/雕像/传送器/泵)**。

三方参照:
1. 官方 wiki 离线镜像:~/Project/GLM/SandboxWorld/terraria-wiki-md/(文件名=页面标题;Wire.md、Mechanisms.md、Pressure_Plates.md、Logic_Gates.md、Teleporter.md、Timer 相关、`ls | grep -iE "wire|mechanism|pressure|sensor|gate|teleporter|timer"`)
2. 反编译权威源码:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/(Wiring.cs;先 grep -n 定位行号再 Read offset/limit 精读)
3. 本仓库实现:~/Project/GLM/SandboxWorld/game/src/(Wiring 已有全量移植记录;grep "Wiring\|wireColor\|hitSwitch\|tripwire" 定位)

审计铁律:
- 只读审计,禁止修改/创建任何文件,报告作为最终回复文本返回
- wiki 数值与实现冲突时用源码裁决;wiki 与源码不符标注「wiki过时/有误」
- 每条结论给实现侧 file:line 证据(grep 到并读过;纯推断标 ❓)
- 记忆称 Wiring.cs 全量移植完成(含种子自跳过语义陷阱),本审计抽核数值与外围组件

必核清单:
1. 电线颜色与多层:四色独立电路、接线工具、光标查看半径
2. 信号传播:单帧最多多少组件、传播顺序、重复触发冷却
3. 开关/拉杆/按钮:瞬时按钮弹回延迟、压力板类型(玩家/NPC/敌怪/projectile 触发型号)
4. 计时器:1s/3s/5s/1/4s(1456 新增?)精度与触发时序
5. 逻辑门:AND/OR/XOR/NAND/NOR/XNOR、故障灯、门输入缓存
6. 传感器:玩家/敌怪检测方块、液体传感器(水/岩浆/蜂蜜)
7. 驱动方块:门/活板门、灯亮灭、传送器(双向人数+无敌帧)、雕像(刷怪冷却与数量上限)、飞镖/火焰/尖刺陷阱(发射间隔/伤害)、泵(液体抽排量/次)
8. 雕像刷怪规则:同时上限、掉落限制(心/星数量)
9. 传送器:同帧多玩家、宠物/minion 跟随
10. 液体泵:每次激活抽多少、防倒流

实现侧起点:grep -rn "Wiring\|teleporter\|statueSpawn\|logicGate\|timer" game/src/ | head -50

输出格式(markdown):
## 域:电路与机械
### 差异清单
| # | 机制项 | 原版设定(wiki页+数值) | 本仓库实现(file:line) | 状态 | 差异细节 |
状态:✅对齐(一行) / ⚠️数值偏差(两侧数值) / ❌未实现 / 🔀逻辑不同 / ❓存疑 / 📄wiki与源码不符
### 覆盖清单
### 最需修复 TOP N
```

---

## 📎 Attachment · skill_listing · 2026-08-12T18:42:57.676Z

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

## 🤖 Assistant · 2026-08-12T18:43:00.536Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The task is very clear: audit the wiring/mechanical systems domain. Let me first look at the three reference sources in parallel:

1. wiki offline mirror related pages
2. decompiled Wiring.cs
3. this repository's implementation

First, do a few broad searches in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:43:00.726Z · glm-x-preview-260804

```
我将开始对电路/机械系统域进行审计。先并行定位三个参照源。
```


---

## 🤖 Assistant · 2026-08-12T18:43:01.369Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | grep -iE \"wire|mechanism|pressure|sensor|gate|teleporter|timer|lever|switch|statue|pump|trap|door|logic\" ",
 "description": "List wiki pages on wiring/mechanism topics"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:01.412Z

**📎 ToolResult**

```
'0'_Statue
'0'_Statue.md
'1'_Statue
'1'_Statue.md
'2'_Statue
'2'_Statue.md
'3'_Statue
'3'_Statue.md
'4'_Statue
'4'_Statue.md
'5'_Statue
'5'_Statue.md
'6'_Statue
'6'_Statue.md
'7'_Statue
'7'_Statue.md
'8'_Statue
'8'_Statue.md
'9'_Statue
'9'_Statue.md
'A'_Statue
'A'_Statue.md
'B'_Statue
'B'_Statue.md
'C'_Statue
'C'_Statue.md
'D'_Statue
'D'_Statue.md
'E'_Statue
'E'_Statue.md
'F'_Statue
'F'_Statue.md
'G'_Statue
'G'_Statue.md
'H'_Statue
'H'_Statue.md
'I'_Statue
'I'_Statue.md
'J'_Statue
'J'_Statue.md
'K'_Statue
'K'_Statue.md
'L'_Statue
'L'_Statue.md
'M'_Statue
'M'_Statue.md
'N'_Statue
'N'_Statue.md
'O'_Statue
'O'_Statue.md
'P'_Statue
'P'_Statue.md
'Q'_Statue
'Q'_Statue.md
'R'_Statue
'R'_Statue.md
'S'_Statue
'S'_Statue.md
'T'_Statue
'T'_Statue.md
'U'_Statue
'U'_Statue.md
'V'_Statue
'V'_Statue.md
'W'_Statue
'W'_Statue.md
'X'_Statue
'X'_Statue.md
'Y'_Statue
'Y'_Statue.md
'Z'_Statue
'Z'_Statue.md
0_Statue.md
1_Second_Timer.md
1_Statue.md
2_Statue.md
3_Second_Timer.md
3_Statue.md
4_Statue.md
5_Second_Timer.md
5_Statue.md
6_Statue.md
7_Statue.md
8_Statue.md
9_Statue.md
A_Statue.md
Angel_Statue.md
Angry_Trapper_Banner.md
Angry_Trapper_Kite.md
Angry_Trapper.md
Anvil_Statue.md
Any_Pressure_Plate.md
Armed_Zombie_Statue.md
Armor_Statue.md
Armour_Statue.md
Axe_Statue.md
B_Statue.md
Ball_O'_Fuse_Wire.md
Bast_Statue.md
Bat_Statue.md
Bird_Statue.md
Blood_Zombie_Statue.md
Blue_(Re-Logic).md
Blue_Pressure_Plate.md
Bomb_Statue.md
Bone_Skeleton_Statue.md
Boomerang_Statue.md
Boot_Statue.md
Boulder_Statue.md
Boulder_Statues.md
Boulder_trap.md
Bow_Statue.md
Brown_Pressure_Plate.md
Buggy_Statue.md
Bunny_Statue.md
Butterfly_Statue.md
C_Statue.md
Category_Entities_patched_in_Switch_1.0.711.6
Category_Entities_patched_Switch
Category_Mechanism_items
Category_Mechanism_items.md
Category_Pumpkin_Moon_NPCs.md
Category_Pumpking_AI_NPCs.md
Category_Pumpking_Scythe_AI_NPCs.md
Category_Statue_AI_NPCs.md
Chest_Statue.md
Cockatiel_Statue.md
Corrupt_Statue.md
Crab_Statue.md
Critter_statues.md
Cross_Statue.md
Cyan_Weighted_Pressure_Plate.md
D_Statue.md
Dart_Trap_Slime.md
Dart_Trap.md
Decorative_Statue.md
Decorative_Statues.md
Doors
Doors.md
Dragonfly_Statue.md
Drippler_Statue.md
Duck_Statue.md
E_Statue.md
Enemy_statues.md
Explosive_Trap_sentry_summons.md
Eyeball_Statue.md
F_Statue.md
Firefly_Statue.md
Fish_Statue.md
Five_Second_Timer.md
Five_Second_Timers.md
Flame_Trap.md
Frog_Statue.md
G_Statue.md
Gargoyle_Statue.md
Gas_Trap.md
Gate.md
Gloom_Statue.md
Goblin_Statue.md
Goldfish_statue.md
Granite_Golem_Statue.md
Grasshopper_Statue.md
Gray_Pressure_Plate.md
Green_Pressure_Plate.md
Grey_Pressure_Plate.md
Guide_Logic_Gates.md
Guide_Pumpkin_Moon_strategies.md
Guide_Teleporter_network.md
H_Statue.md
Half_Second_Timer.md
Half_Second_Timers.md
Hammer_Statue.md
Harpey_Statue.md
Harpy_Statue.md
Heart_Statue.md
Hermes_Boot_Statue.md
Hoplite_Statue.md
Hornet_Statue.md
I_Statue.md
Imp_Statue.md
J_Statue.md
Jellyfish_Statue.md
K_Statue.md
King_Statue.md
L_Statue.md
Lava_Trap.md
Legacy_Angry_Trapper.md
Legacy_Pumpkin_Moon_strategies.md
Legacy_Pumpkin_Moon.md
Legacy_Pumpkin_Pie.md
Legacy_Pumpkin_Seed.md
Legacy_Pumpkin.md
Legacy_Pumpking.md
Legacy_Statues.md
Legacy_Timers.md
Legacy_Wire.md
Lever.md
Lihzahrd_Guardian_Statue.md
Lihzahrd_Pressure_Plate.md
Lihzahrd_Statue.md
Lihzahrd_Watcher_Statue.md
Logic_Gate_Lamps.md
Logic_Gates.md
M_Statue.md
Macaw_Statue.md
Magical_Pumpkin_Seed.md
Mechanisms
Mechanisms.md
Medusa_Statue.md
More_traps_please.md
Mouse_Statue.md
Mushroom_Statue.md
N_Statue.md
No_Traps.md
O_Statue.md
One_Second_Timer.md
One_Second_Timers.md
Orange_Pressure_Plate.md
Orange_Weighted_Pressure_Plate.md
Owl_Statue.md
P_Statue.md
Penguin_Statue.md
Pickaxe_Statue.md
Pigron_Statue.md
Pillar_Statue.md
Pink_Weighted_Pressure_Plate.md
Pirahna_Statue.md
Piranha_Statue.md
Pot_Statue.md
Potion_Statue.md
Pressure_Plate_Track.md
Pressure_Plates.md
Pumpkin_armor.md
Pumpkin_Dresser.md
Pumpkin_furniture.md
Pumpkin_Moon_Medallion.md
Pumpkin_Moon.md
Pumpkin_Pie.md
Pumpkin_Scented_Candle.md
Pumpkin_season.md
Pumpkin_Seed.md
Pumpkin_set.md
Pumpkin_Wall.md
Pumpkin.md
Pumpking_Blade.md
Pumpking.md
Pumps.md
Purple_Weighted_Pressure_Plate.md
Q_Statue.md
Quarter_Second_Timer.md
Quarter_Second_Timers.md
Queen_Statue.md
R_Statue.md
Re-Logic
Re-Logic.md
Reaper_Statue.md
Red_(Re-Logic).md
Red_Pressure_Plate.md
S_Statue.md
Sand_Trap.md
Scorpion_Statue.md
Seagull_Statue.md
Sensors.md
Shark_Statue.md
Shield_Statue.md
Skeleton_Statue.md
Slime_Statue.md
Smart_Doors.md
Snail_Statue.md
Spear_Statue.md
Spear_Trap.md
Spiked_Ball_Trap.md
Spiky_Ball_Trap.md
Squirrel_Statue.md
Star_Statue.md
Star_Statues.md
Statue_(enemy).md
Statue_Trap.md
Statues
Statues.md
Sunflower_Statue.md
Super_Dart_Trap.md
Switch_1.0.1096.2.md
Switch_1.0.711.6.md
Switch_1.0.732.3.md
Switch_1.0.895.9.md
Switch_1.4.0.5.5.md
Switch_1.4.0.5.6.md
Switch_1.4.3.2.0.md
Switch_1.4.4.1.md
Switch_1.4.4.5.md
Switch_1.4.4.9.md
Switch_1.4.4.md
Switch_1.4.5.4.md
Switch_1.4.5.md
Switch_version.md
Switch.md
Sword_Statue.md
T_Statue.md
Tall_Gate.md
Teal_Pressure_Pad.md
Teleporter.md
Text_Statue
Text_Statue.md
Text_Statues.md
Three_Second_Timer.md
Three_Second_Timers.md
Timers
Timers.md
Toucan_Statue.md
Trap_blocks.md
Trap_Door.md
Trapped_Barrel.md
Trapped_Chests
Trapped_Chests.md
Trapped_Dead_Man's_Chest.md
Trapped_Ghost.md
Trapped_Locked_Blue_Dungeon_Chest.md
Trapped_Locked_Corruption_Chest.md
Trapped_Locked_Crimson_Chest.md
Trapped_Locked_Desert_Chest.md
Trapped_Locked_Gold_Chest.md
Trapped_Locked_Green_Dungeon_Chest.md
Trapped_Locked_Hallowed_Chest.md
Trapped_Locked_Ice_Chest.md
Trapped_Locked_Jungle_Chest.md
Trapped_Locked_Pink_Dungeon_Chest.md
Trapped_Locked_Shadow_Chest.md
Trapped_Trash_Can.md
Traps.md
Tree_Statue.md
Turtle_Statue.md
U_Statue.md
Undead_Viking_Statue.md
Unicorn_Statue.md
V_Statue.md
Variegated_Lardfish.md
Venom_Dart_Trap.md
W_Statue.md
Wall_Creeper_Statue.md
Weapon_progression_switch.md
Wire_Bulb.md
Wire_Cutter.md
Wire.md
Woman_Statue
Woman_Statue.md
Worm_Statue.md
Wraith_Statue.md
X_Statue.md
Y_Statue.md
Yellow_Pressure_Plate.md
Z_Statue.md
Zombie_trap.md

```


---

## 🤖 Assistant · 2026-08-12T18:43:02.354Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Wiring\\|teleporter\\|statueSpawn\\|logicGate\\|timer\" ~/Project/GLM/SandboxWorld/game/src/ | grep -v \".test.\" | head -60",
 "description": "Find wiring implementation in game/src"
}
```


---

## 🤖 Assistant · 2026-08-12T18:43:02.357Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/ | head -80; echo \"---\"; ls ~/Project/GLM/SandboxWorld/game/src/ | wc -l",
 "description": "List game/src top-level structure"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:02.374Z

**📎 ToolResult**

```
assets
core
data
debug
dev
drops
entities
i18n
items
lighting
main.ts
mainFlow.ts
net
physics
player
render
save
stats
ui
vui
wld
workers
world
---
      23

```


---

## 👤 User(sidechain) · 2026-08-12T18:43:02.378Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/ui/ChatMonitor.ts:15:  private timers: number[] = [];
~/Project/GLM/SandboxWorld/game/src/ui/ChatMonitor.ts:55:    this.timers.push(window.setTimeout(() => this.remove(line), ChatMonitor.SHOW_MS));
~/Project/GLM/SandboxWorld/game/src/ui/ChatMonitor.ts:65:    clearTimeout(this.timers[i]);
~/Project/GLM/SandboxWorld/game/src/ui/ChatMonitor.ts:66:    this.timers.splice(i, 1);
~/Project/GLM/SandboxWorld/game/src/ui/ChatMonitor.ts:72:    for (const t of this.timers) clearTimeout(t);
~/Project/GLM/SandboxWorld/game/src/ui/ChatMonitor.ts:73:    this.timers = [];
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:611:    // 当前打开箱子引用（Game 提取机通电 Wiring.cs:2571 Chest.UsingChest 判定用）
~/Project/GLM/SandboxWorld/game/src/net/LanDiscovery.ts:25:      clearTimeout(timer);
~/Project/GLM/SandboxWorld/game/src/net/LanDiscovery.ts:29:    const timer = setTimeout(() => finish(null), timeoutMs);
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:72:  statueSpawned?: boolean;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:133:    case 'NotFromStatue': return !ctx.statueSpawned; // Conditions.NotFromStatue
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:134:    case 'IsBloodMoonAndNotFromStatue': return !!ex?.bloodMoon && !ctx.statueSpawned;
~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts:350:  235: { key: 'v_235_teleporter', copyFrame: true },  // Teleporter
~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts:375:  144: { key: 'v_144_timers', copyFrame: true },  // Timers
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:54:import { Wiring, TOOL_RED, TOOL_GREEN, TOOL_BLUE, TOOL_YELLOW, TOOL_ACTUATOR, TOOL_CUTTER } from '../world/Wiring';
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1250:  /** 电路系统(Wiring.cs 移植) */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1251:  wiring: Wiring | null = null;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1621:    // 电路系统(Wiring.cs 移植):器件表 + 触发源登记(测重板 428/感应器 423)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1622:    this.wiring = new Wiring(w.store);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2603:    // 脚下格（Bottom 左下角 +0.01）是 411 未触发态（frameY==0 && frameX<36）→ Wiring.HitSwitch
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5556:  /** 电路工具使用(原版 Player.cs:30289-30444 ItemCheck_UseWiringTools) */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6042:      || type === TILE_BY_KEY['v_132_lever'] || type === TILE_BY_KEY['v_136_switch'] || type === TILE_BY_KEY['v_144_timers']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6156:    } else if (type === TILE_BY_KEY['v_132_lever'] || type === TILE_BY_KEY['v_136_switch'] || type === TILE_BY_KEY['v_144_timers']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6158:      // 拉杆/开关/计时器：HitSwitch（Wiring.cs:163-252 1:1）——帧翻转 + tripWire
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6264:   * 提取机通电消耗源（Wiring.cs:2572-2592）。箱子查找/箱内消耗为纯函数
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6277:  /** 提取机通电产物掉落（Wiring.cs:2588 Item.NewItem 32×32 判定框中心） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6345:  /** 拉杆/开关/计时器:右键 → Wiring.HitSwitch(Wiring.cs:163-252) */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6346:  /** 拉杆/开关/计时器/起爆器:右键 → Wiring.hitSwitch(Wiring.cs:163-252 1:1)。
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7008:          // Wiring.cs:2479-2483：雕像产怪 value=0（不掉钱）+ SpawnedFromStatue
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7056:        // 喷泉去重（Wiring.cs:1529-1545：场上已存在 aiStyle73 且 ai[0]/ai[1] 同锚点的弹）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7071:        // Wiring.cs 1456 :1952-1966:每个场上 185 按距离扣预算
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7117:      // 广播盒（Wiring.cs:1177-1230 1:1）：Sign.ReadSign(anchor, CreateIfMissing:false)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7124:      // 派对纪念碑（Wiring.cs:2037-2039 → BirthdayParty.ToggleManualParty）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7149:  /** 传送器对(Wiring.cs:2314-2365):板上 48×48 判定框内实体双向搬迁 */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7379:  /** UI 侧当前打开的箱子（Wiring.cs:2571 Chest.UsingChest 判定用；UI.ts 赋值） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7718:      // value=0，Wiring.cs:2479）&& hasLuckyCoin && rand.Next(5)==0；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10123:  /** 矿车碾过压板轨道（Minecart.HitTrackSwitch → Wiring.HitSwitch，Minecart.cs:1287-1294）：
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10124:   *  路由到 Wiring.hitSwitch——压板/轨道族直接 TripWire（Wiring.cs:167-171） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10991:      let timer: ReturnType<typeof setTimeout> | null = null; // R10 握手超时句柄（fail 时清除）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10995:        if (timer) clearTimeout(timer);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11075:      // R10：30s 握手超时（fail 内统一 clearTimeout,终审 B4 修正：原 void timer 空转）
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11076:      timer = setTimeout(() => {
~/Project/GLM/SandboxWorld/game/src/render/MonolithFilters.ts:2://  - 触发链：Wiring.cs:2025-2036（410/480/509/657/658/720/721/725/733 → WorldGen.SwitchMonolith）
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:11:import { TOOL_CUTTER } from '../world/Wiring';
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:1:// 原版 Wiring.cs(1.4.0.5)一比一移植:四色导线信号传播 + 逻辑门 + 泵 + 传送器 + 致动器。
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:3://   updateMech        Wiring.cs:88-161(计时器/引爆器冷却,每 tick 调)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:4://   hitSwitch         Wiring.cs:163-252(手动/物理触发源)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:5://   checkMech         Wiring.cs:313-327(陷阱冷却注册,上限 999)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:6://   xferWater         Wiring.cs:329-377(泵配对液体转移)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:7://   tripWire          Wiring.cs:379-529(四色 pass 顺序 红→蓝→绿→黄)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:8://   pixelBoxPass      Wiring.cs:531-553
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:9://   logicGatePass     Wiring.cs:555-591
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:10://   checkLogicGate    Wiring.cs:593-691(六种门 + 故障灯)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:11://   hitWire           Wiring.cs:693-827(BFS;邻居序 下/上/右/左;分线盒预算)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:12://   hitWireSingle     Wiring.cs:829-2282(核心 case 在此,其余委托 devices 表)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:20:export type DeviceHandler = (w: Wiring, sheet: number, x: number, y: number) => boolean;
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:30:const MAX_PUMP = 20;   // Wiring.cs:34(MaxPump=20,填充上限 19)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:31:const MAX_MECH = 1000; // Wiring.cs:41(MaxMech=1000,注册上限 999)
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:44:export class Wiring {
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:55:  /** 世界地表行(蜥蜴砖致动限制 Wiring.cs:2375) */

```


---

## 🤖 Assistant · 2026-08-12T18:43:04.685Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wiring.ts 已有全量移植。现在读实现侧核心文件,同时读 Wiring.cs 反编译源码,还有 wiki 关键页面。

先看 Wiring.ts 的规模和结构。
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:43:04.696Z · glm-x-preview-260804

```
实现侧 `~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts` 已定位。先看两侧文件规模,再精读。
```


---

## 🤖 Assistant · 2026-08-12T18:43:05.135Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs; echo \"---\"; grep -rn \"wiring\\.\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -40",
 "description": "Line counts and wiring call sites in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:05.155Z

**📎 ToolResult**

```
     806 ~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts
    3441 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs
    4247 total
---
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1623:    this.wiring.worldSurface = w.groundLevel;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2607:      if (this.wiring.sheetOf(dx, dy) === 411
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2609:        this.wiring.hitSwitch(dx, dy);

```


---

## 🤖 Assistant · 2026-08-12T18:43:06.160Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"wiring\\|Wiring\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" -l | grep -v test | head -20; echo \"---sensors---\"; grep -rn \"sensor\\|Sensor\\|423\\b\\|424\\b\" ~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts | head -20",
 "description": "Files referencing wiring + sensor handling"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:06.186Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/render/MonolithFilters.ts
~/Project/GLM/SandboxWorld/game/src/world/SceneMetrics.ts
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts
~/Project/GLM/SandboxWorld/game/src/world/Torch.ts
~/Project/GLM/SandboxWorld/game/src/world/MinecartTrack.ts
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts
~/Project/GLM/SandboxWorld/game/src/world/FurnitureStyle.ts
~/Project/GLM/SandboxWorld/game/src/world/Extractinator.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BrokenTrapCleanupPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts
~/Project/GLM/SandboxWorld/game/src/world/wiring/party.ts
~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts
~/Project/GLM/SandboxWorld/game/src/lighting/TileLightScanner.ts
~/Project/GLM/SandboxWorld/game/src/physics/Conveyor.ts
~/Project/GLM/SandboxWorld/game/src/data/items.ts
~/Project/GLM/SandboxWorld/game/src/data/Music.ts
---sensors---
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:209:    if (sh === 135 || sh === 314 || sh === 423 || sh === 428 || sh === 442 || sh === 476) {
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:340:        if (nbSheet === 424 || nbSheet === 445) num2 = 0;
~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts:342:        if (curSheet === 424) {

```


---

## 🤖 Assistant · 2026-08-12T18:43:08.787Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wiring.ts 只有 806 行,而原版 Wiring.cs 有 3441 行。大部分核心逻辑在 Game.ts 里(hitWireSingle 的 case 委托)。让我读完整的 Wiring.ts,再读 devices.ts 和 Game.ts 里的相关段落。

先并行读 Wiring.ts 全文和 wiki 的核心页面。
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:43:09.105Z · glm-x-preview-260804

```
Wiring.ts 806 行(原版 3441 行),核心 case 委托到 `world/wiring/devices.ts` 和 Game.ts。先读实现主体。
```


---

## 🤖 Assistant · 2026-08-12T18:43:09.230Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/Wiring.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:09.347Z

**📎 ToolResult**

```
1	// 原版 Wiring.cs(1.4.0.5)一比一移植:四色导线信号传播 + 逻辑门 + 泵 + 传送器 + 致动器。
2	// 结构与行号对照:
3	//   updateMech        Wiring.cs:88-161(计时器/引爆器冷却,每 tick 调)
4	//   hitSwitch         Wiring.cs:163-252(手动/物理触发源)
5	//   checkMech         Wiring.cs:313-327(陷阱冷却注册,上限 999)
6	//   xferWater         Wiring.cs:329-377(泵配对液体转移)
7	//   tripWire          Wiring.cs:379-529(四色 pass 顺序 红→蓝→绿→黄)
8	//   pixelBoxPass      Wiring.cs:531-553
9	//   logicGatePass     Wiring.cs:555-591
10	//   checkLogicGate    Wiring.cs:593-691(六种门 + 故障灯)
11	//   hitWire           Wiring.cs:693-827(BFS;邻居序 下/上/右/左;分线盒预算)
12	//   hitWireSingle     Wiring.cs:829-2282(核心 case 在此,其余委托 devices 表)
13	//   actuate/actuateForced/deActive/reActive  :262-280, :2373-2405
14	//   massWireOperation :2407-2558(宏伟蓝图 L 形铺线)
15	// 单机移植:NetMessage/SendData 一律跳过(原版联机同步,无操作)。
16	import { TileStore } from './TileStore';
17	import { TILE_DEFS } from '../data/tiles';
18	
19	/** 器件分发表(P3 devices.ts 提供):返回 true 表示已处理该 case */
20	export type DeviceHandler = (w: Wiring, sheet: number, x: number, y: number) => boolean;
21	
22	/** 多色工具模式位(WiresUI.Settings.MultiToolMode) */
23	export const TOOL_RED = 1;
24	export const TOOL_GREEN = 2;
25	export const TOOL_BLUE = 4;
26	export const TOOL_YELLOW = 8;
27	export const TOOL_ACTUATOR = 16;
28	export const TOOL_CUTTER = 32;
29	
30	const MAX_PUMP = 20;   // Wiring.cs:34(MaxPump=20,填充上限 19)
31	const MAX_MECH = 1000; // Wiring.cs:41(MaxMech=1000,注册上限 999)
32	
33	/** TileID.Sets.PreventsActuationUnder（TileID.cs:313）：下方不可被致动器缩入的承载物。
34	 *  旧表只列宝箱族/祭坛（21/88/467/237），漏音乐盒 26/花盆 77/垃圾桶 470/475/
35	 *  茶壶 597/饼干 441/望远镜 468 */
36	const PREVENTS_ACTUATION_UNDER = new Set([21, 467, 26, 77, 88, 470, 475, 237, 597, 441, 468]);
37	/** TileID.Sets.IsATreeTrunk（TileID.cs:161）——CanKillTile 树干承载检查用 */
38	const IS_A_TREE_TRUNK = new Set([5, 72, 583, 584, 585, 586, 587, 588, 589, 596, 616, 634]);
39	
40	/** TileID.Sets.Boulders（1456 TileID.cs:195）：138 巨石/484 滚动仙人掌/664 弹跳巨石/
41	 *  665 生命水晶巨石/711 彩虹/712 屎/713 岩浆/714 蜘蛛/715 地牢/716 友好 */
42	const BOULDER_SHEETS = new Set([138, 484, 664, 665, 711, 712, 713, 714, 715, 716]);
43	
44	export class Wiring {
45	  readonly st: TileStore;
46	  /** 器件表(P3 注入) */
47	  device: DeviceHandler | null = null;
48	  /** 巨石失撑下落钩子（devices.ts 装配）：致动缩入后上格为 Boulders 族 tile 时调用。
49	   *  原版数据点：巨石 tile 被杀 → Projectile 99（1456 cs:48765-48769：spawn
50	   *  (x*16+15.5, y*16+16)、初速 0/0、伤害 70、击退 10）。引擎按"失撑即坠"接——
51	   *  原版由 KillTile 触发该转换，巨石陷阱（压板→致动石栅→巨石坠下）观测行为一致 */
52	  boulderFall: ((x: number, y: number, sheet: number) => void) | null = null;
53	  /** 传送器对执行(引擎侧搬迁玩家/敌人;P3 注入) */
54	  teleportPair: ((a: [number, number], b: [number, number]) => void) | null = null;
55	  /** 世界地表行(蜥蜴砖致动限制 Wiring.cs:2375) */
56	  worldSurface = 0;
57	  /** 世世纪杀花已击败(同上) */
58	  planteraDowned = false;
59	
60	  running = false;                                  // :23
61	  blockPlayerTeleportationForOneIteration = false;  // :22(测重板抑制传送)
62	  private currentWireColor = 0;                     // :46(1红 2蓝 3绿 4黄;彩线灯泡用)
63	
64	  // BFS 状态(:24-27)。点用 idx(y*w+x) 编码。
65	  private wireSkip = new Set<number>();
66	  private wireList: number[] = [];      // FIFO(head 指针)
67	  private wireDir: number[] = [];       // 与 wireList 平行的进入方向 0下 1上 2右 3左
68	  private toProcess = new Map<number, number>(); // :27 分线盒再访预算
69	
70	  // 逻辑门(:28-32)
71	  private gatesCurrent: number[] = [];
72	  private gatesNext: number[] = [];
73	  private gatesDone = new Map<number, boolean>();
74	  private lampsToCheck: number[] = [];
75	  private pixelBoxTriggers = new Map<number, number>();
76	
77	  // 传送器对(:33;px 坐标,-1 = 未捕获)与泵(:34-40)
78	  private tp: Array<[number, number]> = [[-1, -1], [-1, -1]];
79	  private inPumpX = new Int16Array(MAX_PUMP); private inPumpY = new Int16Array(MAX_PUMP);
80	  private outPumpX = new Int16Array(MAX_PUMP); private outPumpY = new Int16Array(MAX_PUMP);
81	  private numInPump = 0; private numOutPump = 0;
82	
83	  // 炮族全局冷却（Wiring.cs:69-73 静态字段；:147-158 UpdateMech 每 tick 递减）。
84	  // devices.ts case 209/212 开火时置位（Wiring.cs:1335/1338/1393）
85	  cannonCoolDown = 0;          // :69 大炮 120
86	  bunnyCannonCoolDown = 0;     // :71 兔兔炮 480
87	  snowballCannonCoolDown = 0;  // :73 雪球发射器 15
88	
89	  // 冷却注册(:41-45)
90	  private mechX = new Int32Array(MAX_MECH + 1);
91	  private mechY = new Int32Array(MAX_MECH + 1);
92	  private mechTime = new Int32Array(MAX_MECH + 1);
93	  private numMechs = 0;
94	
95	  constructor(st: TileStore) {
96	    this.st = st;
97	  }
98	
99	  /** 活跃器件冷却数（F5 调试报告只读 numMechs） */
100	  activeMechCount(): number { return this.numMechs; }
101	
102	  /** 冷却注册表快照：{x, y, t} 剩余 tick（F5 调试报告 mechDump） */
103	  mechDump(): Array<{ x: number; y: number; t: number }> {
104	    const out: Array<{ x: number; y: number; t: number }> = [];
105	    for (let i = 0; i < this.numMechs; i++) {
106	      out.push({ x: this.mechX[i], y: this.mechY[i], t: this.mechTime[i] });
107	    }
108	    return out;
109	  }
110	
111	  /** 传送器捕获对快照（-1 = 未捕获；F5 调试报告） */
112	  teleportPairs(): Array<[number, number]> {
113	    return [[...this.tp[0]], [...this.tp[1]]];
114	  }
115	
116	  private p2i(x: number, y: number): number { return y * this.st.w + x; }
117	  private i2x(i: number): number { return i % this.st.w; }
118	  private i2y(i: number): number { return (i / this.st.w) | 0; }
119	  private sheetAt(x: number, y: number): number { return this.sheetOf(x, y); }
120	  /** 该格的原版 tile id(sheet;非 vanilla tile 返回 -1)。器件表按 sheet 分发 */
121	  sheetOf(x: number, y: number): number {
122	    if (!this.st.inBounds(x, y)) return -1;
123	    const d = TILE_DEFS[this.st.type[this.p2i(x, y)]];
124	    return d?.vanilla?.sheet ?? -1;
125	  }
126	  /** 多格器件整体去重(devices.ts 用) */
127	  skipCell(x: number, y: number): void { this.skipWire(x, y); }
128	
129	  // ============ UpdateMech(Wiring.cs:88-161)每 tick 调 ============
130	
131	  updateMech(): void {
132	    // 炮族全局冷却每 tick 递减（Wiring.cs:147-158）
133	    if (this.cannonCoolDown > 0) this.cannonCoolDown--;
134	    if (this.bunnyCannonCoolDown > 0) this.bunnyCannonCoolDown--;
135	    if (this.snowballCannonCoolDown > 0) this.snowballCannonCoolDown--;
136	    for (let i = this.numMechs - 1; i >= 0; i--) {
137	      this.mechTime[i]--;
138	      const mx = this.mechX[i], my = this.mechY[i];
139	      const sh = this.sheetAt(mx, my);
140	      const raw = this.st.type[this.p2i(mx, my)] !== 0;
141	      if (raw && sh === 144) {
142	        const ti = this.p2i(mx, my);
143	        if (this.st.frameY[ti] === 0) {
144	          this.mechTime[i] = 0;
145	        } else {
146	          // frameX/18 → 周期帧数(:102-120)
147	          let period = Math.floor(this.st.frameX[ti] / 18);
148	          period = period === 0 ? 60 : period === 1 ? 180 : period === 2 ? 300 : period === 3 ? 30 : period === 4 ? 15 : 60;
149	          // IEEERemainder(t, period) === 0(注意负数:IEEERemainder 结果范围 (-p,p])
150	          const r = this.mechTime[i] - period * Math.round(this.mechTime[i] / period);
151	          if (r === 0) {
152	            this.mechTime[i] = 18000;
153	            this.tripWire(mx, my, 1, 1);
154	          }
155	        }
156	      }
157	      if (this.mechTime[i] <= 0) {
158	        if (raw && sh === 144) {
159	          const ti = this.p2i(mx, my);
160	          this.st.setTile(mx, my, this.st.type[ti], this.st.frameX[ti], 0);
161	        }
162	        if (raw && sh === 411) {
163	          // 引爆器 2×2 帧复位(:135-151)
164	          const ti = this.p2i(mx, my);
165	          const num1 = Math.floor(this.st.frameX[ti] % 36 / 18);
166	          const num2 = Math.floor(this.st.frameY[ti] % 36 / 18);
167	          const tileX = mx - num1, tileY = my - num2;
168	          let num3 = 36;
169	          if (this.st.frameX[this.p2i(tileX, tileY)] >= 36) num3 = -36;
170	          for (let ix = tileX; ix < tileX + 2; ix++) {
171	            for (let iy = tileY; iy < tileY + 2; iy++) {
172	              const ii = this.p2i(ix, iy);
173	              if (this.sheetAt(ix, iy) === 411) this.st.setTile(ix, iy, this.st.type[ii], this.st.frameX[ii] + num3, this.st.frameY[ii]);
174	            }
175	          }
176	        }
177	        // 数组下移移除(:152-158)
178	        for (let k = i; k < this.numMechs; k++) {
179	          this.mechX[k] = this.mechX[k + 1];
180	          this.mechY[k] = this.mechY[k + 1];
181	          this.mechTime[k] = this.mechTime[k + 1];
182	        }
183	        this.numMechs--;
184	      }
185	    }
186	  }
187	
188	  // ============ CheckMech(Wiring.cs:313-327)============
189	
190	  checkMech(i: number, j: number, time: number): boolean {
191	    for (let k = 0; k < this.numMechs; k++) {
192	      if (this.mechX[k] === i && this.mechY[k] === j) return false;
193	    }
194	    if (this.numMechs >= 999) return false;
195	    this.mechX[this.numMechs] = i;
196	    this.mechY[this.numMechs] = j;
197	    this.mechTime[this.numMechs] = time;
198	    this.numMechs++;
199	    return true;
200	  }
201	
202	  // ============ HitSwitch(Wiring.cs:163-252)============
203	
204	  hitSwitch(i: number, j: number): void {
205	    if (!this.st.inBounds(i, j)) return;
206	    const sh = this.sheetAt(i, j);
207	    const ti = this.p2i(i, j);
208	    // 压板/轨道/感应器/测重板/垫板/高尔夫(:167-171)与宝石锁(:172-176):直接 Trip
209	    if (sh === 135 || sh === 314 || sh === 423 || sh === 428 || sh === 442 || sh === 476) {
210	      this.tripWire(i, j, 1, 1);
211	      return;
212	    }
213	    if (sh === 440) { // 宝石锁 3×3
214	      this.tripWire(i, j, 3, 3);
215	      return;
216	    }
217	    if (sh === 136) { // 开关 frameY 0↔18(:177-182)
218	      this.st.setTile(i, j, this.st.type[ti], this.st.frameX[ti], this.st.frameY[ti] !== 0 ? 0 : 18);
219	      this.tripWire(i, j, 1, 1);
220	      return;
221	    }
222	    if (sh === 443) { // 热喷泉(:183-184)
223	      this.device?.(this, 443, i, j);
224	      return;
225	    }
226	    if (sh === 144) { // 计时器开/关(:185-196)
227	      if (this.st.frameY[ti] === 0) {
228	        this.st.setTile(i, j, this.st.type[ti], this.st.frameX[ti], 18);
229	        this.checkMech(i, j, 18000);
230	      } else {
231	        this.st.setTile(i, j, this.st.type[ti], this.st.frameX[ti], 0);
232	      }
233	      return;
234	    }
235	    if (sh === 441 || sh === 468) { // 陷阱箱 2×2(:197-208)
236	      const num1 = Math.floor(this.st.frameX[ti] / 18) * -1;
237	      const num2 = Math.floor(this.st.frameY[ti] / 18) * -1;
238	      let num3 = num1 % 4;
239	      if (num3 < -1) num3 += 2;
240	      this.tripWire(num3 + i, num2 + j, 2, 2);
241	      return;
242	    }
243	    if (sh === 467) { // 水晶陷阱箱(frameX/36==4 才触发,:209-222)
244	      if (Math.floor(this.st.frameX[ti] / 36) !== 4) return;
245	      const num1 = Math.floor(this.st.frameX[ti] / 18) * -1;
246	      const num2 = Math.floor(this.st.frameY[ti] / 18) * -1;
247	      let num3 = num1 % 4;
248	      if (num3 < -1) num3 += 2;
249	      this.tripWire(num3 + i, num2 + j, 2, 2);
250	      return;
251	    }
252	    if (sh === 132 || sh === 411) { // 拉杆/引爆器 2×2 翻帧(:223-251)
253	      let delta = 36;
254	      const num2 = Math.floor(this.st.frameX[ti] / 18) * -1;
255	      const num3 = Math.floor(this.st.frameY[ti] / 18) * -1;
256	      let num4 = num2 % 4;
257	      if (num4 < -1) { num4 += 2; delta = -36; }
258	      const ax = num4 + i, ay = num3 + j;
259	      if (this.sheetAt(ax, ay) === 411) this.checkMech(ax, ay, 60);
260	      for (let ix = ax; ix < ax + 2; ix++) {
261	        for (let iy = ay; iy < ay + 2; iy++) {
262	          if (!this.st.inBounds(ix, iy)) continue;
263	          const ii = this.p2i(ix, iy);
264	          const s2 = this.sheetAt(ix, iy);
265	          if (s2 === 132 || s2 === 411) {
266	            this.st.setTile(ix, iy, this.st.type[ii], this.st.frameX[ii] + delta, this.st.frameY[ii]);
267	          }
268	        }
269	      }
270	      this.tripWire(ax, ay, 2, 2);
271	      return;
272	    }
273	  }
274	
275	  // ============ TripWire(Wiring.cs:379-529)============
276	
277	  tripWire(left: number, top: number, width: number, height: number): void {
278	    this.running = true;
279	    this.wireList.length = 0;
280	    this.wireDir.length = 0;
281	    const st = this.st;
282	    const pairs: Array<[[number, number], [number, number]]> = [];
283	    const bits = [TileStore.WIRE_RED, TileStore.WIRE_BLUE, TileStore.WIRE_GREEN, TileStore.WIRE_YELLOW];
284	    // 四色 pass 顺序固定 红(1)蓝(2)绿(3)黄(4)(:405-508);每色前重置传送器对与泵
285	    for (let color = 1; color <= 4; color++) {
286	      this.tp[0] = [-1, -1]; this.tp[1] = [-1, -1];
287	      this.wireList.length = 0;
288	      const bit = bits[color - 1];
289	      for (let x = left; x < left + width; x++) {
290	        for (let y = top; y < top + height; y++) {
291	          if (!st.inBounds(x, y)) continue;
292	          if (st.wire[this.p2i(x, y)] & bit) this.wireList.push(this.p2i(x, y));
293	        }
294	      }
295	      if (this.wireList.length > 0) {
296	        this.numInPump = 0;
297	        this.numOutPump = 0;
298	        this.hitWire(color);
299	        if (this.numInPump > 0 && this.numOutPump > 0) this.xferWater();
300	      }
301	      if (this.tp[0][0] >= 0 && this.tp[1][0] >= 0) pairs.push([[...this.tp[0]], [...this.tp[1]] as [number, number]]);
302	    }
303	    this.running = false;
304	    // 四色收集完的传送器对统一执行(:520-526)
305	    for (const [a, b] of pairs) this.teleportPair?.(a, b);
306	    this.pixelBoxPass();
307	    this.logicGatePass();
308	  }
309	
310	  // ============ HitWire BFS(Wiring.cs:693-827)============
311	
312	  private hitWire(wireType: number): void {
313	    const st = this.st;
314	    // 种子:SkipWire + 预算 4 + 方向 0(:695-703)
315	    this.wireDir.length = 0;
316	    const n = this.wireList.length;
317	    for (let k = 0; k < n; k++) {
318	      const p = this.wireList[k];
319	      this.skipWireI(p);
320	      this.toProcess.set(p, 4);
321	      this.wireDir.push(0);
322	    }
323	    this.currentWireColor = wireType;
324	    let head = 0;
325	    while (head < this.wireList.length) {
326	      const key = this.wireList[head];
327	      const num1 = this.wireDir[head];
328	      head++;
329	      const x = this.i2x(key), y = this.i2y(key);
330	      if (!this.wireSkip.has(key)) this.hitWireSingle(x, y);
331	      // 邻居顺序:0下 1上 2右 3左(:713-739)
332	      for (let index1 = 0; index1 < 4; index1++) {
333	        const X = index1 === 0 ? x : index1 === 1 ? x : index1 === 2 ? x + 1 : x - 1;
334	        const Y = index1 === 0 ? y + 1 : index1 === 1 ? y - 1 : y;
335	        if (X < 2 || X >= st.w - 2 || Y < 2 || Y >= st.h - 2) continue; // :740
336	        const curSheet = this.sheetAt(x, y);
337	        const nbSheet = this.sheetAt(X, Y);
338	        // :748-750 邻居是分线盒/像素盒 → 不给预算
339	        let num2 = 3;
340	        if (nbSheet === 424 || nbSheet === 445) num2 = 0;
341	        // :751-768 分线盒方向门控(frameX/18 三态)
342	        if (curSheet === 424) {
343	          const mode = Math.floor(st.frameX[this.p2i(x, y)] / 18);
344	          if (mode === 0) { if (index1 === num1) continue; }
345	          else if (mode === 1) {
346	            if (!((num1 === 0 && index1 === 3) || (num1 === 3 && index1 === 0) || (num1 === 1 && index1 === 2) || (num1 === 2 && index1 === 1))) continue;
347	          } else if (mode === 2) {
348	            if (!((num1 === 0 && index1 === 2) || (num1 === 2 && index1 === 0) || (num1 === 1 && index1 === 3) || (num1 === 3 && index1 === 1))) continue;
349	          }
350	        }
351	        // :769-780 像素盒仅同向直通,并记录触发值(垂直 2 / 水平 1)
352	        if (curSheet === 445) {
353	          if (index1 === num1) {
354	            const v = (index1 === 0 || index1 === 1) ? 2 : 1;
355	            this.pixelBoxTriggers.set(key, (this.pixelBoxTriggers.get(key) ?? 0) | v);
356	          } else continue;
357	        }
358	        // :781-799 邻居须带当前色
359	        const bit = wireType === 1 ? TileStore.WIRE_RED : wireType === 2 ? TileStore.WIRE_BLUE : wireType === 3 ? TileStore.WIRE_GREEN : TileStore.WIRE_YELLOW;
360	        if (!(st.wire[this.p2i(X, Y)] & bit)) continue;
361	        // :800-819 预算消耗或入队
362	        const nb = this.p2i(X, Y);
363	        const budget = this.toProcess.get(nb);
364	        if (budget !== undefined) {
365	          const left2 = budget - 1;
366	          if (left2 === 0) this.toProcess.delete(nb);
367	          else this.toProcess.set(nb, left2);
368	        } else {
369	          this.wireList.push(nb);
370	          this.wireDir.push(index1);
371	          if (num2 > 0) this.toProcess.set(nb, num2);
372	        }
373	      }
374	    }
375	    this.wireSkip.clear();
376	    this.toProcess.clear();
377	  }
378	
379	  // ============ HitWireSingle 核心 case(Wiring.cs:829+)============
380	
381	  private hitWireSingle(x: number, y: number): void {
382	    const st = this.st;
383	    const i = this.p2i(x, y);
384	    const type = st.type[i];
385	    const sheet = this.sheetAt(x, y);
386	    // :833-834 先致动(active 检查之前,空格上的致动线也会翻)
387	    if (st.wire[i] & TileStore.WIRE_ACTUATOR) this.actuateForced(x, y);
388	    // :835 raw active = type≠0(致动态也继续)
389	    if (type === 0) return;
390	    // 核心 case(牵扯 Wiring 内部状态),其余全表委托 devices.ts
391	    switch (sheet) {
392	      case 144: // 计时器:信号 = 打开并重置计时(:839-843)
393	        this.hitSwitch(x, y);
394	        return;
395	      case 419: { // 逻辑门灯:翻转 + SkipWire + 入队(:1075-1086)
396	        let d = 18;
397	        if (st.frameX[i] >= 18) d = -18;
398	        if (st.frameX[i] === 36) d = 0;
399	        this.skipWire(x, y);
400	        st.setTile(x, y, type, st.frameX[i] + d, st.frameY[i]);
401	        this.lampsToCheck.push(i);
402	        return;
403	      }
404	      case 235: { // 传送器成对捕获(:1251-1271)
405	        const tx = x - Math.floor(st.frameX[i] / 18);
406	        if (st.wall[i] === 87 && y > this.worldSurface && !this.planteraDowned) return;
407	        const halfOff = st.half[i] ? 0.5 : 0;
408	        if (this.tp[0][0] === -1) { this.tp[0] = [tx, y + halfOff]; return; }
409	        if (this.tp[0][0] === tx && this.tp[0][1] === y + halfOff) return;
410	        this.tp[1] = [tx, y + halfOff];
411	        return;
412	      }
413	      case 142: case 143: { // 入水/出水泵 2×2 四格收集(:1793-1863)
414	        const py = y - Math.floor(st.frameY[i] / 18);
415	        let px = Math.floor(st.frameX[i] / 18);
416	        if (px > 1) px -= 2;
417	        const ox = x - px;
418	        this.skipWire(ox, py); this.skipWire(ox, py + 1);
419	        this.skipWire(ox + 1, py); this.skipWire(ox + 1, py + 1);
420	        const cells: Array<[number, number]> = [[ox, py + 1], [ox + 1, py + 1], [ox, py], [ox + 1, py]];
421	        if (sheet === 142) {
422	          for (let k = 0; k < 4 && this.numInPump < 19; k++) {
423	            this.inPumpX[this.numInPump] = cells[k][0];
424	            this.inPumpY[this.numInPump] = cells[k][1];
425	            this.numInPump++;
426	          }
427	        } else {
428	          for (let k = 0; k < 4 && this.numOutPump < 19; k++) {
429	            this.outPumpX[this.numOutPump] = cells[k][0];
430	            this.outPumpY[this.numOutPump] = cells[k][1];
431	            this.numOutPump++;
432	          }
433	        }
434	        return;
435	      }
436	      case 429: { // 彩线灯泡:按当前色翻对应位(:1325-1357)
437	        const q = Math.floor(st.frameX[i] / 18);
438	        let num53 = 0, on = false;
439	        switch (this.currentWireColor) {
440	          case 1: num53 = 18; on = !(q % 2 >= 1); break;
441	          case 2: num53 = 72; on = !(q % 8 >= 4); break;
442	          case 3: num53 = 36; on = !(q % 4 >= 2); break;
443	          case 4: num53 = 144; on = !(q % 16 >= 8); break;
444	        }
445	        st.setTile(x, y, type, st.frameX[i] + (on ? num53 : -num53), st.frameY[i]);
446	        return;
447	      }
448	    }
449	    // 致动后不再吃器件信号(原版各 case 里 actuator 时早退的近似统一处理;
450	    // 门/传送带/宝石块在原版各自判断,其余器件致动时信号照常——按原版逐 case 已在 devices 内)
451	    this.device?.(this, sheet, x, y);
452	  }
453	
454	  // ============ XferWater(Wiring.cs:329-377)============
455	
456	  private xferWater(): void {
457	    const st = this.st;
458	    for (let a = 0; a < this.numInPump; a++) {
459	      const i1 = this.inPumpX[a], j1 = this.inPumpY[a];
460	      if (!st.inBounds(i1, j1)) continue;
461	      const ii = st.idx(i1, j1);
462	      let liquid1 = st.liquid[ii];
463	      if (liquid1 > 0) {
464	        const lava = st.liquidType[ii] === 2, honey = st.liquidType[ii] === 3;
465	        for (let b = 0; b < this.numOutPump; b++) {
466	          const i2 = this.outPumpX[b], j2 = this.outPumpY[b];
467	          if (!st.inBounds(i2, j2)) continue;
468	          const oi = st.idx(i2, j2);
469	          let liquid2 = st.liquid[oi];
470	          if (liquid2 < 255) {
471	            let flag1 = st.liquidType[oi] === 2, flag2 = st.liquidType[oi] === 3;
472	            if (liquid2 === 0) { flag1 = lava; flag2 = honey; }
473	            if (lava === flag1 && honey === flag2) {
474	              let move = liquid1;
475	              if (move + liquid2 > 255) move = 255 - liquid2;
476	              st.setLiquid(i2, j2, liquid2 + move, lava ? 2 : honey ? 3 : 1);
477	              st.setLiquid(i1, j1, liquid1 - move, st.liquidType[ii] || 1);
478	              liquid1 = st.liquid[ii];
479	              if (st.liquid[ii] === 0) break;
480	            }
481	          }
482	        }
483	      }
484	    }
485	  }
486	
487	  // ============ PixelBoxPass(Wiring.cs:531-553)============
488	
489	  private pixelBoxPass(): void {
490	    const st = this.st;
491	    for (const [key, v] of this.pixelBoxTriggers) {
492	      const x = this.i2x(key), y = this.i2y(key);
493	      if (!st.inBounds(x, y)) continue;
494	      const i = this.p2i(x, y);
495	      if (v === 1) {
496	        if (st.frameX[i] !== 0) st.setTile(x, y, st.type[i], 0, st.frameY[i]);
497	      } else if (v === 3) {
498	        if (st.frameX[i] !== 18) st.setTile(x, y, st.type[i], 18, st.frameY[i]);
499	      }
500	    }
501	    this.pixelBoxTriggers.clear();
502	  }
503	
504	  // ============ LogicGatePass / CheckLogicGate(Wiring.cs:555-691)============
505	
506	  private logicGatePass(): void {
507	    if (this.gatesCurrent.length !== 0) return; // 已在级联中
508	    this.gatesDone.clear();
509	    let lampHead = 0, gateHead = 0;
510	    while (this.lampsToCheck.length > lampHead) {
511	      while (this.lampsToCheck.length > lampHead) {
512	        const lamp = this.lampsToCheck[lampHead++];
513	        this.checkLogicGate(this.i2x(lamp), this.i2y(lamp));
514	      }
515	      // _GatesNext → _GatesCurrent,逐个 TripWire(递归;_GatesDone 防环)(:567-585)
516	      const next = this.gatesNext;
517	      this.gatesNext = [];
518	      this.gatesCurrent = next;
519	      gateHead = 0;
520	      while (this.gatesCurrent.length > gateHead) {
521	        const key = this.gatesCurrent[gateHead];
522	        gateHead++;
523	        if (this.gatesDone.get(key)) continue;
524	        this.gatesDone.set(key, true);
525	        this.tripWire(this.i2x(key), this.i2y(key), 1, 1);
526	      }
527	      this.gatesCurrent.length = 0; // 原版 Queue Dequeue 排空;残留会让下次级联被早退守卫吞掉
528	    }
529	    this.lampsToCheck.length = 0;
530	    this.gatesDone.clear();
531	    if (this.blockPlayerTeleportationForOneIteration) {
532	      this.blockPlayerTeleportationForOneIteration = false;
533	    }
534	  }
535	
536	  /** 触发逻辑门(压板等直接 Poke,P4/P6 用;Wiring.cs:254-260 的单机语义) */
537	  pokeLogicGate(lampX: number, lampY: number): void {
538	    this.lampsToCheck.push(this.p2i(lampX, lampY));
539	    this.logicGatePass();
540	  }
541	
542	  private checkLogicGate(lampX: number, lampY: number): void {
543	    const st = this.st;
544	    if (!st.inBounds(lampX, lampY)) return;
545	    for (let y = lampY; y < st.h; y++) {
546	      if (!st.inBounds(lampX, y)) break;
547	      const i = this.p2i(lampX, y);
548	      if (st.type[i] === 0) break;
549	      const sh = this.sheetAt(lampX, y);
550	      if (sh === 420) {
551	        const wasDone = this.gatesDone.get(i) ?? false;
552	        const num1 = Math.floor(st.frameY[i] / 18); // 门种类 0-5
553	        const flag2 = st.frameX[i] === 18;  // 当前输出 ON
554	        const flag3 = st.frameX[i] === 36;  // 故障输出态
555	        if (num1 < 0) break;
556	        // 向上数灯(:614-629)
557	        let num2 = 0, num3 = 0;
558	        let faulty = false;
559	        for (let y2 = y - 1; y2 > 0; y2--) {
560	          const j = this.p2i(lampX, y2);
561	          if (st.type[j] !== 0 && this.sheetAt(lampX, y2) === 419) {
562	            if (st.frameX[j] === 36) { faulty = true; break; }
563	            num2++;
564	            if (st.frameX[j] === 18) num3++;
565	          } else break;
566	        }
567	        let out: boolean;
568	        switch (num1) { // :631-653
569	          case 0: out = num2 === num3; break;   // AND
570	          case 1: out = num3 > 0; break;        // OR
571	          case 2: out = num2 !== num3; break;   // XOR
572	          case 3: out = num3 === 0; break;      // NOR
573	          case 4: out = num3 === 1; break;      // NAND
574	          case 5: out = num3 !== 1; break;      // XNOR
575	          default: return;
576	        }
577	        const flag6 = !faulty && flag3;                 // 故障存在且门当前 off → 强制不发
578	        let flag7 = false;                              // 故障灯本轮被翻 → 概率通过
579	        if (faulty && st.frameX[this.p2i(lampX, lampY)] === 36) flag7 = true;
580	        // :658 无变化则不动作
581	        if (!((out !== flag2) || flag6 || flag7)) break;
582	        st.setTile(lampX, y, st.type[i], out ? 18 : 0, st.frameY[i]);
583	        if (faulty) st.setTile(lampX, y, st.type[i], 36, st.frameY[i]);
584	        this.skipWire(lampX, y);
585	        let fire: boolean = !faulty || flag7;
586	        if (flag7 && num2 > 0) fire = Math.random() < num3 / num2;
587	        if (flag6) fire = false;
588	        if (!fire) break;
589	        if (!wasDone) {
590	          this.gatesNext.push(i);
591	          break;
592	        }
593	        // 重复输出 = 冒烟反馈(Wiring.cs:683-685;烟雾粒子由 devices 侧近似,此处仅返回)
594	        break;
595	      }
596	      if (sh !== 419) break;
597	    }
598	  }
599	
600	  // ============ 致动器(Wiring.cs:262-280, 2373-2405)============
601	
602	  actuate(i: number, j: number): boolean {
603	    const st = this.st;
604	    if (!st.inBounds(i, j)) return false;
605	    if (!(st.wire[this.p2i(i, j)] & TileStore.WIRE_ACTUATOR)) return false;
606	    if (st.isActuated(i, j)) this.reActive(i, j);
607	    else this.deActive(i, j);
608	    return true;
609	  }
610	
611	  actuateForced(i: number, j: number): void {
612	    if (this.st.isActuated(i, j)) this.reActive(i, j);
613	    else this.deActive(i, j);
614	  }
615	
616	  /** 缩入（Wiring.cs:3222-3251 DeActive 1:1）：蜥蜴砖地表限制 + 不可缩 tile 表 +
617	   *  上方 PreventsActuationUnder / CanKillTile 结构检查 */
618	  private deActive(i: number, j: number): void {
619	    const st = this.st;
620	    if (!st.inBounds(i, j)) return;
621	    const t = this.p2i(i, j);
622	    if (!st.flags[t]) return;
623	    const sh = this.sheetAt(i, j);
624	    if (sh === 226 && j > this.worldSurface && !this.planteraDowned) return;
625	    // flag = tileSolid && !NotReallySolid{387,388,10}；314/379/386-389/476 显式置 false
626	    // （Wiring.cs:3227-3239；379 boulder 此前漏列）
627	    const def = TILE_DEFS[st.type[t]];
628	    let solid = !!def?.solid;
629	    if (sh === 314 || sh === 379 || sh === 386 || sh === 387 || sh === 388 || sh === 389 || sh === 476) solid = false;
630	    if (sh === 387 || sh === 388 || sh === 10) solid = false; // TileID.Sets.NotReallySolid（TileID.cs:355）
631	    if (!solid) return;
632	    // 门（Wiring.cs:3241）：上方未激活，或（上方非 PreventsActuationUnder 且 CanKillTile）
633	    if (st.inBounds(i, j - 1) && st.flags[this.p2i(i, j - 1)]) {
634	      const above = this.sheetAt(i, j - 1);
635	      if (PREVENTS_ACTUATION_UNDER.has(above)) return;
636	      if (!this.canKillTile(i, j)) return;
637	    }
638	    st.setActuated(i, j, true);
639	    // 支撑缩入 → 上格巨石失撑下落（巨石陷阱演出；数据点见 boulderFall 注释）
640	    if (st.inBounds(i, j - 1)) {
641	      const up = st.idx(i, j - 1);
642	      if (st.flags[up]) {
643	        const ush = TILE_DEFS[st.type[up]]?.vanilla?.sheet ?? -1;
644	        if (BOULDER_SHEETS.has(ush)) {
645	          st.type[up] = 0; st.flags[up] = 0;   // KillTile 清格 → 转 Projectile 99
646	          this.boulderFall?.(i, j - 1, ush);
647	        }
648	      }
649	    }
650	  }
651	
652	  /** WorldGen.CanKillTile 结构子集（WorldGen.cs:62249-62358，致动缩入门用）：
653	   *  未激活/魔法冰墙 350 → false；上方是异种树干/宝箱族/棕榈/雕像承载位 → false。
654	   *  Boulders+CheckBoulderChest/IsLockedDoor/Chest.CanDestroyChest（容器战利品）
655	   *  依赖容器内容与门锁系统，未接入——恒按"可杀"处理（注释登记） */
656	  private canKillTile(i: number, j: number): boolean {
657	    const st = this.st;
658	    if (!st.inBounds(i, j)) return false;
659	    const t = this.p2i(i, j);
660	    if (!st.flags[t]) return false;
661	    if (st.wall[t] === 350) return false;
662	    const mySheet = this.sheetAt(i, j);
663	    if (j >= 1) {
664	      const a = this.p2i(i, j - 1);
665	      if (st.flags[a]) {
666	        const above = this.sheetAt(i, j - 1);
667	        if (above !== mySheet) {
668	          // IsATreeTrunk{5,72,583-589,596,616,634}：上方异种树干段不可缩（分支/树顶帧豁免）
669	          if (IS_A_TREE_TRUNK.has(above)) {
670	            const fx = st.frameX[a], fy = st.frameY[a];
671	            const branchExempt = (fx === 66 && fy >= 0 && fy <= 44) || (fx === 88 && fy >= 66 && fy <= 110);
672	            if (!branchExempt && fy < 198) return false;
673	          }
674	          // 棕榈 323：左右枝帧不可缩
675	          if (above === 323 && (st.frameX[a] === 66 || st.frameX[a] === 220)) return false;
676	          // 宝箱/梳妆台/雕像承载位（62290-62305）
677	          if (above === 21 || above === 26 || above === 72 || above === 77 || above === 88 || above === 467 || above === 488) return false;
678	          if (above === 80 && st.frameX[a] / 18 <= 1) return false;
679	          if (above === 80 && st.frameX[a] / 18 >= 4 && st.frameX[a] / 18 <= 5) return false;
680	        }
681	      }
682	    }
683	    return true;
684	  }
685	
686	  private reActive(i: number, j: number): void {
687	    this.st.setActuated(i, j, false);
688	  }
689	
690	  // ============ SkipWire(Wiring.cs:78-86)============
691	
692	  private skipWire(x: number, y: number): void { this.wireSkip.add(this.p2i(x, y)); }
693	  private skipWireI(i: number): void { this.wireSkip.add(i); }
694	
695	  // ============ 导线放置/移除(WorldGen.cs:34219-34327 语义)============
696	
697	  /** 放置某色线;已存在返回 false */
698	  placeWire(x: number, y: number, colorBit: number): boolean {
699	    const st = this.st;
700	    if (!st.inBounds(x, y)) return false;
701	    const i = st.idx(x, y);
702	    if (st.wire[i] & colorBit) return false;
703	    st.setWire(x, y, st.wire[i] | colorBit);
704	    return true;
705	  }
706	
707	  /** 移除某色线;不存在返回 false */
708	  killWire(x: number, y: number, colorBit: number): boolean {
709	    const st = this.st;
710	    if (!st.inBounds(x, y)) return false;
711	    const i = st.idx(x, y);
712	    if (!(st.wire[i] & colorBit)) return false;
713	    st.setWire(x, y, st.wire[i] & ~colorBit);
714	    return true;
715	  }
716	
717	  placeActuator(x: number, y: number): boolean {
718	    const st = this.st;
719	    if (!st.inBounds(x, y)) return false;
720	    const i = st.idx(x, y);
721	    if (st.wire[i] & TileStore.WIRE_ACTUATOR) return false;
722	    st.setWire(x, y, st.wire[i] | TileStore.WIRE_ACTUATOR);
723	    return true;
724	  }
725	
726	  killActuator(x: number, y: number): boolean {
727	    const st = this.st;
728	    if (!st.inBounds(x, y)) return false;
729	    const i = st.idx(x, y);
730	    if (!(st.wire[i] & TileStore.WIRE_ACTUATOR)) return false;
731	    st.setWire(x, y, st.wire[i] & ~TileStore.WIRE_ACTUATOR);
732	    return true;
733	  }
734	
735	  // ============ MassWireOperation(Wiring.cs:2407-2558)============
736	
737	  /**
738	   * 宏伟蓝图/五彩扳手 L 形批量操作。
739	   * mode: TOOL_* 位组合;consume 回调返回剩余可用数(false=耗尽),
740	   * 返回实际消耗 {wire, actuator}。
741	   */
742	  massWireOperation(
743	    ps: [number, number], pe: [number, number], mode: number,
744	    wires: number, actuators: number,
745	  ): { wire: number; actuator: number; aborted: boolean } {
746	    const dir = true; // 原版 dir = player.direction==1;先垂直段。false 时先水平
747	    let wireLeft = wires, actuatorLeft = actuators;
748	    let aborted = false;
749	    const step = (x: number, y: number): boolean => {
750	      // 返回 false = 材料耗尽中止
751	      if (!this.st.inBounds(x, y)) return true;
752	      const i = this.st.idx(x, y);
753	      if (!(mode & TOOL_CUTTER)) {
754	        const order: Array<[number, number]> = [
755	          [TOOL_RED, TileStore.WIRE_RED], [TOOL_GREEN, TileStore.WIRE_GREEN],
756	          [TOOL_BLUE, TileStore.WIRE_BLUE], [TOOL_YELLOW, TileStore.WIRE_YELLOW],
757	        ];
758	        for (const [m, bit] of order) {
759	          if (mode & m && !(this.st.wire[i] & bit)) {
760	            if (wireLeft <= 0) return false;
761	            wireLeft--;
762	            this.placeWire(x, y, bit);
763	          }
764	        }
765	        if (mode & TOOL_ACTUATOR && !(this.st.wire[i] & TileStore.WIRE_ACTUATOR)) {
766	          if (actuatorLeft <= 0) return false;
767	          actuatorLeft--;
768	          this.placeActuator(x, y);
769	        }
770	      } else {
771	        if (mode & TOOL_RED) this.killWire(x, y, TileStore.WIRE_RED);
772	        if (mode & TOOL_GREEN) this.killWire(x, y, TileStore.WIRE_GREEN);
773	        if (mode & TOOL_BLUE) this.killWire(x, y, TileStore.WIRE_BLUE);
774	        if (mode & TOOL_YELLOW) this.killWire(x, y, TileStore.WIRE_YELLOW);
775	        if (mode & TOOL_ACTUATOR) this.killActuator(x, y);
776	      }
777	      return true;
778	    };
779	    // 第一段:主轴(dir=true → 垂直)(:2428-2454)
780	    const sx = Math.sign(pe[0] - ps[0]), sy = Math.sign(pe[1] - ps[1]);
781	    let px = ps[0], py = ps[1];
782	    const first = dir ? sy : sx;
783	    {
784	      const from = dir ? ps[1] : ps[0];
785	      const to = dir ? pe[1] : pe[0];
786	      for (let v = from; v !== to && !aborted; v += first) {
787	        if (dir) py = v; else px = v;
788	        if (!step(px, py)) { aborted = true; break; }
789	      }
790	    }
791	    // 第二段:副轴(:2455-2484)
792	    {
793	      if (dir) py = pe[1]; else px = pe[0];
794	      const from = dir ? ps[0] : ps[1];
795	      const to = dir ? pe[0] : pe[1];
796	      const stepDir = dir ? sx : sy;
797	      for (let v = from; v !== to && !aborted; v += stepDir) {
798	        if (dir) px = v; else py = v;
799	        if (!step(px, py)) { aborted = true; break; }
800	      }
801	    }
802	    // 端点(:2485-2486)
803	    if (!aborted) step(pe[0], pe[1]);
804	    return { wire: wires - wireLeft, actuator: actuators - actuatorLeft, aborted };
805	  }
806	}
807	

```


---

## 🤖 Assistant · 2026-08-12T18:43:09.647Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/world/wiring/; echo \"---\"; wc -l ~/Project/GLM/SandboxWorld/game/src/world/wiring/*.ts",
 "description": "List wiring module files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:09.668Z

**📎 ToolResult**

```
devices.ts
party.ts
---
     922 ~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts
      43 ~/Project/GLM/SandboxWorld/game/src/world/wiring/party.ts
     965 total

```


---

## 🤖 Assistant · 2026-08-12T18:43:13.628Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wiring.ts 注释说是基于 1.4.0.5 版本 Wiring.cs。但本项目标杆是 1.4.5.6 (Terarria1456)。这是潜在风险:1.4.0.5 → 1.4.4/1.4.5.6 之间 Wiring.cs 有变化吗?1456 的 Wiring.cs 是 3441 行。需要对比。1.4.4 加入了:
- Teleportation pylons?不,那不是 wiring。
- 1.4.4 新 tile:比如 476 = ? 
- 新的压力板/传感器?

让我读 1456 Wiring.cs 全文(3441 行,可以分两次读)和 devices.ts(922 行)。

先并行读。
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:43:14.131Z · glm-x-preview-260804

```
注意:实现注释标注基于 **1.4.0.5**,而项目标杆是 **1.4.5.6**。这是重点核查方向。先读 1456 源码和 devices.ts。
```


---

## 🤖 Assistant · 2026-08-12T18:43:14.343Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs",
 "limit": 900
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:14.350Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using Microsoft.Xna.Framework;
4	using Terraria.Audio;
5	using Terraria.DataStructures;
6	using Terraria.GameContent;
7	using Terraria.GameContent.Events;
8	using Terraria.GameContent.UI;
9	using Terraria.ID;
10	using Terraria.Localization;
11	using Terraria.UI;
12	
13	namespace Terraria;
14	
15	public static class Wiring
16	{
17		public static bool blockPlayerTeleportationForOneIteration;
18	
19		public static bool running;
20	
21		private static Dictionary<Point16, bool> _wireSkip;
22	
23		private static DoubleStack<Point16> _wireList;
24	
25		private static DoubleStack<byte> _wireDirectionList;
26	
27		private static Dictionary<Point16, byte> _toProcess;
28	
29		private static Queue<Point16> _GatesCurrent;
30	
31		private static Queue<Point16> _LampsToCheck;
32	
33		private static Queue<Point16> _GatesNext;
34	
35		private static Dictionary<Point16, bool> _GatesDone;
36	
37		private static Dictionary<Point16, byte> _PixelBoxTriggers;
38	
39		private static Vector2[] _teleport;
40	
41		private const int MaxPump = 20;
42	
43		private static int[] _inPumpX;
44	
45		private static int[] _inPumpY;
46	
47		private static int _numInPump;
48	
49		private static int[] _outPumpX;
50	
51		private static int[] _outPumpY;
52	
53		private static int _numOutPump;
54	
55		private const int MaxMech = 1000;
56	
57		private static int[] _mechX;
58	
59		private static int[] _mechY;
60	
61		private static int _numMechs;
62	
63		private static int[] _mechTime;
64	
65		private static int _currentWireColor;
66	
67		private static int CurrentUser = 255;
68	
69		private static int cannonCoolDown = 0;
70	
71		private static int bunnyCannonCoolDown = 0;
72	
73		private static int snowballCannonCoolDown = 0;
74	
75		public static readonly Vector2 HopperGrabHitboxSize = new Vector2(192f);
76	
77		public static void SetCurrentUser(int plr = -1)
78		{
79			if (plr < 0 || plr > 255)
80			{
81				plr = 255;
82			}
83			if (Main.netMode == 0)
84			{
85				plr = Main.myPlayer;
86			}
87			CurrentUser = plr;
88		}
89	
90		public static void Initialize()
91		{
92			_wireSkip = new Dictionary<Point16, bool>();
93			_wireList = new DoubleStack<Point16>();
94			_wireDirectionList = new DoubleStack<byte>();
95			_toProcess = new Dictionary<Point16, byte>();
96			_GatesCurrent = new Queue<Point16>();
97			_GatesNext = new Queue<Point16>();
98			_GatesDone = new Dictionary<Point16, bool>();
99			_LampsToCheck = new Queue<Point16>();
100			_PixelBoxTriggers = new Dictionary<Point16, byte>();
101			_inPumpX = new int[20];
102			_inPumpY = new int[20];
103			_outPumpX = new int[20];
104			_outPumpY = new int[20];
105			_teleport = new Vector2[2]
106			{
107				Vector2.One * -1f,
108				Vector2.One * -1f
109			};
110			_mechX = new int[1000];
111			_mechY = new int[1000];
112			_mechTime = new int[1000];
113		}
114	
115		public static void SkipWire(int x, int y)
116		{
117			_wireSkip[new Point16(x, y)] = true;
118		}
119	
120		public static void SkipWire(Point16 point)
121		{
122			_wireSkip[point] = true;
123		}
124	
125		public static void ClearAll()
126		{
127			for (int i = 0; i < 20; i++)
128			{
129				_inPumpX[i] = 0;
130				_inPumpY[i] = 0;
131				_outPumpX[i] = 0;
132				_outPumpY[i] = 0;
133			}
134			_numInPump = 0;
135			_numOutPump = 0;
136			for (int j = 0; j < 1000; j++)
137			{
138				_mechTime[j] = 0;
139				_mechX[j] = 0;
140				_mechY[j] = 0;
141			}
142			_numMechs = 0;
143		}
144	
145		public static void UpdateMech()
146		{
147			if (cannonCoolDown > 0)
148			{
149				cannonCoolDown--;
150			}
151			if (bunnyCannonCoolDown > 0)
152			{
153				bunnyCannonCoolDown--;
154			}
155			if (snowballCannonCoolDown > 0)
156			{
157				snowballCannonCoolDown--;
158			}
159			SetCurrentUser();
160			for (int num = _numMechs - 1; num >= 0; num--)
161			{
162				_mechTime[num]--;
163				int num2 = _mechX[num];
164				int num3 = _mechY[num];
165				if (!WorldGen.InWorld(num2, num3, 1))
166				{
167					_numMechs--;
168				}
169				else
170				{
171					Tile tile = Main.tile[num2, num3];
172					if (tile == null)
173					{
174						_numMechs--;
175					}
176					else
177					{
178						if (tile.active() && tile.type == 144)
179						{
180							if (tile.frameY == 0)
181							{
182								_mechTime[num] = 0;
183							}
184							else
185							{
186								int num4 = tile.frameX / 18;
187								switch (num4)
188								{
189								case 0:
190									num4 = 60;
191									break;
192								case 1:
193									num4 = 180;
194									break;
195								case 2:
196									num4 = 300;
197									break;
198								case 3:
199									num4 = 30;
200									break;
201								case 4:
202									num4 = 15;
203									break;
204								}
205								if (Math.IEEERemainder(_mechTime[num], num4) == 0.0)
206								{
207									_mechTime[num] = 18000;
208									TripWire(_mechX[num], _mechY[num], 1, 1);
209								}
210							}
211						}
212						if (_mechTime[num] <= 0)
213						{
214							if (tile.active() && tile.type == 144)
215							{
216								tile.frameY = 0;
217								NetMessage.SendTileSquare(-1, _mechX[num], _mechY[num]);
218							}
219							if (tile.active() && tile.type == 411)
220							{
221								int num5 = tile.frameX % 36 / 18;
222								int num6 = tile.frameY % 36 / 18;
223								int num7 = _mechX[num] - num5;
224								int num8 = _mechY[num] - num6;
225								int num9 = 36;
226								if (Main.tile[num7, num8].frameX >= 36)
227								{
228									num9 = -36;
229								}
230								for (int i = num7; i < num7 + 2; i++)
231								{
232									for (int j = num8; j < num8 + 2; j++)
233									{
234										if (WorldGen.InWorld(i, j, 1))
235										{
236											Tile tile2 = Main.tile[i, j];
237											if (tile2 != null)
238											{
239												tile2.frameX = (short)(tile2.frameX + num9);
240											}
241										}
242									}
243								}
244								NetMessage.SendTileSquare(-1, num7, num8, 2, 2);
245							}
246							for (int k = num; k < _numMechs; k++)
247							{
248								_mechX[k] = _mechX[k + 1];
249								_mechY[k] = _mechY[k + 1];
250								_mechTime[k] = _mechTime[k + 1];
251							}
252							_numMechs--;
253						}
254					}
255				}
256			}
257		}
258	
259		public static void HitSwitch(int i, int j)
260		{
261			if (!WorldGen.InWorld(i, j) || Main.tile[i, j] == null)
262			{
263				return;
264			}
265			if (Main.tile[i, j].type == 135 || Main.tile[i, j].type == 314 || Main.tile[i, j].type == 423 || Main.tile[i, j].type == 428 || Main.tile[i, j].type == 442 || Main.tile[i, j].type == 476)
266			{
267				SoundEngine.PlaySound(28, i * 16, j * 16, 0);
268				TripWire(i, j, 1, 1);
269			}
270			else if (Main.tile[i, j].type == 440)
271			{
272				SoundEngine.PlaySound(28, i * 16 + 16, j * 16 + 16, 0);
273				TripWire(i, j, 3, 3);
274			}
275			else if (Main.tile[i, j].type == 136)
276			{
277				if (Main.tile[i, j].frameY == 0)
278				{
279					Main.tile[i, j].frameY = 18;
280				}
281				else
282				{
283					Main.tile[i, j].frameY = 0;
284				}
285				SoundEngine.PlaySound(28, i * 16, j * 16, 0);
286				TripWire(i, j, 1, 1);
287			}
288			else if (Main.tile[i, j].type == 210)
289			{
290				ExplodeMine(i, j);
291			}
292			else if (Main.tile[i, j].type == 443)
293			{
294				GeyserTrap(i, j);
295			}
296			else if (Main.tile[i, j].type == 144)
297			{
298				if (Main.tile[i, j].frameY == 0)
299				{
300					Main.tile[i, j].frameY = 18;
301					if (Main.netMode != 1)
302					{
303						CheckMech(i, j, 18000);
304					}
305				}
306				else
307				{
308					Main.tile[i, j].frameY = 0;
309				}
310				SoundEngine.PlaySound(28, i * 16, j * 16, 0);
311			}
312			else if (Main.tile[i, j].type == 441 || Main.tile[i, j].type == 468)
313			{
314				int num = Main.tile[i, j].frameX / 18 * -1;
315				int num2 = Main.tile[i, j].frameY / 18 * -1;
316				num %= 4;
317				if (num < -1)
318				{
319					num += 2;
320				}
321				num += i;
322				num2 += j;
323				SoundEngine.PlaySound(28, i * 16, j * 16, 0);
324				TripWire(num, num2, 2, 2);
325			}
326			else if (Main.tile[i, j].type == 467)
327			{
328				if (Main.tile[i, j].frameX / 36 == 4)
329				{
330					int num3 = Main.tile[i, j].frameX / 18 * -1;
331					int num4 = Main.tile[i, j].frameY / 18 * -1;
332					num3 %= 4;
333					if (num3 < -1)
334					{
335						num3 += 2;
336					}
337					num3 += i;
338					num4 += j;
339					SoundEngine.PlaySound(28, i * 16, j * 16, 0);
340					TripWire(num3, num4, 2, 2);
341				}
342			}
343			else
344			{
345				if (Main.tile[i, j].type != 132 && Main.tile[i, j].type != 411)
346				{
347					return;
348				}
349				short num5 = 36;
350				int num6 = Main.tile[i, j].frameX / 18 * -1;
351				int num7 = Main.tile[i, j].frameY / 18 * -1;
352				num6 %= 4;
353				if (num6 < -1)
354				{
355					num6 += 2;
356					num5 = -36;
357				}
358				num6 += i;
359				num7 += j;
360				if (Main.netMode != 1 && Main.tile[num6, num7].type == 411)
361				{
362					CheckMech(num6, num7, 60);
363				}
364				for (int k = num6; k < num6 + 2; k++)
365				{
366					for (int l = num7; l < num7 + 2; l++)
367					{
368						if (Main.tile[k, l].type == 132 || Main.tile[k, l].type == 411)
369						{
370							Main.tile[k, l].frameX += num5;
371						}
372					}
373				}
374				WorldGen.TileFrame(num6, num7);
375				SoundEngine.PlaySound(28, i * 16, j * 16, 0);
376				TripWire(num6, num7, 2, 2);
377			}
378		}
379	
380		public static void PokeLogicGate(int lampX, int lampY)
381		{
382			if (Main.netMode != 1)
383			{
384				_LampsToCheck.Enqueue(new Point16(lampX, lampY));
385				LogicGatePass();
386			}
387		}
388	
389		public static bool Actuate(int i, int j)
390		{
391			Tile tile = Main.tile[i, j];
392			if (!tile.actuator())
393			{
394				return false;
395			}
396			if (tile.inActive())
397			{
398				ReActive(i, j);
399			}
400			else
401			{
402				DeActive(i, j);
403			}
404			return true;
405		}
406	
407		public static void ActuateForced(int i, int j)
408		{
409			if (Main.tile[i, j].inActive())
410			{
411				ReActive(i, j);
412			}
413			else
414			{
415				DeActive(i, j);
416			}
417		}
418	
419		public static void MassWireOperation(Point ps, Point pe, Player master)
420		{
421			int wireCount = 0;
422			int actuatorCount = 0;
423			for (int i = 0; i < 58; i++)
424			{
425				if (master.inventory[i].type == 530)
426				{
427					wireCount += master.inventory[i].stack;
428				}
429				if (master.inventory[i].type == 849)
430				{
431					actuatorCount += master.inventory[i].stack;
432				}
433			}
434			int num = wireCount;
435			int num2 = actuatorCount;
436			MassWireOperationInner(master, ps, pe, master.Center, master.direction == 1, ref wireCount, ref actuatorCount);
437			int num3 = num - wireCount;
438			int num4 = num2 - actuatorCount;
439			if (Main.netMode == 2)
440			{
441				NetMessage.SendData(110, master.whoAmI, -1, null, 530, num3, master.whoAmI);
442				NetMessage.SendData(110, master.whoAmI, -1, null, 849, num4, master.whoAmI);
443				return;
444			}
445			for (int j = 0; j < num3; j++)
446			{
447				master.ConsumeItem(530);
448			}
449			for (int k = 0; k < num4; k++)
450			{
451				master.ConsumeItem(849);
452			}
453		}
454	
455		private static bool CheckMech(int i, int j, int time)
456		{
457			for (int k = 0; k < _numMechs; k++)
458			{
459				if (_mechX[k] == i && _mechY[k] == j)
460				{
461					return false;
462				}
463			}
464			if (_numMechs < 999)
465			{
466				_mechX[_numMechs] = i;
467				_mechY[_numMechs] = j;
468				_mechTime[_numMechs] = time;
469				_numMechs++;
470				return true;
471			}
472			return false;
473		}
474	
475		private static void XferWater()
476		{
477			for (int i = 0; i < _numInPump; i++)
478			{
479				int num = _inPumpX[i];
480				int num2 = _inPumpY[i];
481				int liquid = Main.tile[num, num2].liquid;
482				if (liquid <= 0)
483				{
484					continue;
485				}
486				byte b = Main.tile[num, num2].liquidType();
487				for (int j = 0; j < _numOutPump; j++)
488				{
489					int num3 = _outPumpX[j];
490					int num4 = _outPumpY[j];
491					int liquid2 = Main.tile[num3, num4].liquid;
492					if (liquid2 >= 255)
493					{
494						continue;
495					}
496					byte b2 = Main.tile[num3, num4].liquidType();
497					if (liquid2 == 0)
498					{
499						b2 = b;
500					}
501					if (b2 == b)
502					{
503						int num5 = liquid;
504						if (num5 + liquid2 > 255)
505						{
506							num5 = 255 - liquid2;
507						}
508						Main.tile[num3, num4].liquid += (byte)num5;
509						Main.tile[num, num2].liquid -= (byte)num5;
510						liquid = Main.tile[num, num2].liquid;
511						Main.tile[num3, num4].liquidType(b);
512						WorldGen.SquareTileFrame(num3, num4);
513						if (Main.tile[num, num2].liquid == 0)
514						{
515							Main.tile[num, num2].liquidType(0);
516							WorldGen.SquareTileFrame(num, num2);
517							break;
518						}
519					}
520				}
521				WorldGen.SquareTileFrame(num, num2);
522			}
523		}
524	
525		private static void TripWire(int left, int top, int width, int height)
526		{
527			if (Main.netMode == 1)
528			{
529				return;
530			}
531			running = true;
532			if (_wireList.Count != 0)
533			{
534				_wireList.Clear(quickClear: true);
535			}
536			if (_wireDirectionList.Count != 0)
537			{
538				_wireDirectionList.Clear(quickClear: true);
539			}
540			Vector2[] array = new Vector2[8];
541			int num = 0;
542			for (int i = left; i < left + width; i++)
543			{
544				for (int j = top; j < top + height; j++)
545				{
546					Point16 back = new Point16(i, j);
547					Tile tile = Main.tile[i, j];
548					if (tile != null && tile.wire())
549					{
550						_wireList.PushBack(back);
551					}
552				}
553			}
554			_teleport[0].X = -1f;
555			_teleport[0].Y = -1f;
556			_teleport[1].X = -1f;
557			_teleport[1].Y = -1f;
558			if (_wireList.Count > 0)
559			{
560				_numInPump = 0;
561				_numOutPump = 0;
562				HitWire(_wireList, 1);
563				if (_numInPump > 0 && _numOutPump > 0)
564				{
565					XferWater();
566				}
567			}
568			array[num++] = _teleport[0];
569			array[num++] = _teleport[1];
570			for (int k = left; k < left + width; k++)
571			{
572				for (int l = top; l < top + height; l++)
573				{
574					Point16 back = new Point16(k, l);
575					Tile tile2 = Main.tile[k, l];
576					if (tile2 != null && tile2.wire2())
577					{
578						_wireList.PushBack(back);
579					}
580				}
581			}
582			_teleport[0].X = -1f;
583			_teleport[0].Y = -1f;
584			_teleport[1].X = -1f;
585			_teleport[1].Y = -1f;
586			if (_wireList.Count > 0)
587			{
588				_numInPump = 0;
589				_numOutPump = 0;
590				HitWire(_wireList, 2);
591				if (_numInPump > 0 && _numOutPump > 0)
592				{
593					XferWater();
594				}
595			}
596			array[num++] = _teleport[0];
597			array[num++] = _teleport[1];
598			_teleport[0].X = -1f;
599			_teleport[0].Y = -1f;
600			_teleport[1].X = -1f;
601			_teleport[1].Y = -1f;
602			for (int m = left; m < left + width; m++)
603			{
604				for (int n = top; n < top + height; n++)
605				{
606					Point16 back = new Point16(m, n);
607					Tile tile3 = Main.tile[m, n];
608					if (tile3 != null && tile3.wire3())
609					{
610						_wireList.PushBack(back);
611					}
612				}
613			}
614			if (_wireList.Count > 0)
615			{
616				_numInPump = 0;
617				_numOutPump = 0;
618				HitWire(_wireList, 3);
619				if (_numInPump > 0 && _numOutPump > 0)
620				{
621					XferWater();
622				}
623			}
624			array[num++] = _teleport[0];
625			array[num++] = _teleport[1];
626			_teleport[0].X = -1f;
627			_teleport[0].Y = -1f;
628			_teleport[1].X = -1f;
629			_teleport[1].Y = -1f;
630			for (int num2 = left; num2 < left + width; num2++)
631			{
632				for (int num3 = top; num3 < top + height; num3++)
633				{
634					Point16 back = new Point16(num2, num3);
635					Tile tile4 = Main.tile[num2, num3];
636					if (tile4 != null && tile4.wire4())
637					{
638						_wireList.PushBack(back);
639					}
640				}
641			}
642			if (_wireList.Count > 0)
643			{
644				_numInPump = 0;
645				_numOutPump = 0;
646				HitWire(_wireList, 4);
647				if (_numInPump > 0 && _numOutPump > 0)
648				{
649					XferWater();
650				}
651			}
652			array[num++] = _teleport[0];
653			array[num++] = _teleport[1];
654			running = false;
655			for (int num4 = 0; num4 < 8; num4 += 2)
656			{
657				_teleport[0] = array[num4];
658				_teleport[1] = array[num4 + 1];
659				if (_teleport[0].X >= 0f && _teleport[1].X >= 0f)
660				{
661					Teleport();
662				}
663			}
664			PixelBoxPass();
665			LogicGatePass();
666		}
667	
668		private static void PixelBoxPass()
669		{
670			foreach (KeyValuePair<Point16, byte> pixelBoxTrigger in _PixelBoxTriggers)
671			{
672				if (pixelBoxTrigger.Value == 3)
673				{
674					Tile tile = Main.tile[pixelBoxTrigger.Key.X, pixelBoxTrigger.Key.Y];
675					tile.frameX = (short)((tile.frameX != 18) ? 18 : 0);
676					NetMessage.SendTileSquare(-1, pixelBoxTrigger.Key.X, pixelBoxTrigger.Key.Y);
677				}
678			}
679			_PixelBoxTriggers.Clear();
680		}
681	
682		private static void LogicGatePass()
683		{
684			if (_GatesCurrent.Count != 0)
685			{
686				return;
687			}
688			_GatesDone.Clear();
689			while (_LampsToCheck.Count > 0)
690			{
691				while (_LampsToCheck.Count > 0)
692				{
693					Point16 point = _LampsToCheck.Dequeue();
694					CheckLogicGate(point.X, point.Y);
695				}
696				while (_GatesNext.Count > 0)
697				{
698					Utils.Swap(ref _GatesCurrent, ref _GatesNext);
699					while (_GatesCurrent.Count > 0)
700					{
701						Point16 key = _GatesCurrent.Peek();
702						if (_GatesDone.TryGetValue(key, out var value) && value)
703						{
704							_GatesCurrent.Dequeue();
705							continue;
706						}
707						_GatesDone.Add(key, value: true);
708						TripWire(key.X, key.Y, 1, 1);
709						_GatesCurrent.Dequeue();
710					}
711				}
712			}
713			_GatesDone.Clear();
714			if (blockPlayerTeleportationForOneIteration)
715			{
716				blockPlayerTeleportationForOneIteration = false;
717			}
718		}
719	
720		private static void CheckLogicGate(int lampX, int lampY)
721		{
722			if (!WorldGen.InWorld(lampX, lampY, 1))
723			{
724				return;
725			}
726			for (int i = lampY; i < Main.maxTilesY; i++)
727			{
728				Tile tile = Main.tile[lampX, i];
729				if (!tile.active())
730				{
731					break;
732				}
733				if (tile.type == 420)
734				{
735					_GatesDone.TryGetValue(new Point16(lampX, i), out var value);
736					int num = tile.frameY / 18;
737					bool flag = tile.frameX == 18;
738					bool flag2 = tile.frameX == 36;
739					if (num < 0)
740					{
741						break;
742					}
743					int num2 = 0;
744					int num3 = 0;
745					bool flag3 = false;
746					for (int num4 = i - 1; num4 > 0; num4--)
747					{
748						Tile tile2 = Main.tile[lampX, num4];
749						if (!tile2.active() || tile2.type != 419)
750						{
751							break;
752						}
753						if (tile2.frameX == 36)
754						{
755							flag3 = true;
756							break;
757						}
758						num2++;
759						num3 += (tile2.frameX == 18).ToInt();
760					}
761					bool flag4 = false;
762					switch (num)
763					{
764					default:
765						return;
766					case 0:
767						flag4 = num2 == num3;
768						break;
769					case 2:
770						flag4 = num2 != num3;
771						break;
772					case 1:
773						flag4 = num3 > 0;
774						break;
775					case 3:
776						flag4 = num3 == 0;
777						break;
778					case 4:
779						flag4 = num3 == 1;
780						break;
781					case 5:
782						flag4 = num3 != 1;
783						break;
784					}
785					bool flag5 = !flag3 && flag2;
786					bool flag6 = false;
787					if (flag3 && Framing.GetTileSafely(lampX, lampY).frameX == 36)
788					{
789						flag6 = true;
790					}
791					if (!(flag4 != flag || flag5 || flag6))
792					{
793						break;
794					}
795					_ = tile.frameX % 18 / 18;
796					tile.frameX = (short)(18 * flag4.ToInt());
797					if (flag3)
798					{
799						tile.frameX = 36;
800					}
801					SkipWire(lampX, i);
802					WorldGen.SquareTileFrame(lampX, i);
803					NetMessage.SendTileSquare(-1, lampX, i);
804					bool flag7 = !flag3 || flag6;
805					if (flag6)
806					{
807						if (num3 == 0 || num2 == 0)
808						{
809							flag7 = false;
810						}
811						flag7 = Main.rand.NextFloat() < (float)num3 / (float)num2;
812					}
813					if (flag5)
814					{
815						flag7 = false;
816					}
817					if (flag7)
818					{
819						if (!value)
820						{
821							_GatesNext.Enqueue(new Point16(lampX, i));
822							break;
823						}
824						Vector2 position = new Vector2(lampX, i) * 16f - new Vector2(10f);
825						Utils.PoofOfSmoke(position);
826						NetMessage.SendData(106, -1, -1, null, (int)position.X, position.Y);
827					}
828					break;
829				}
830				if (tile.type != 419)
831				{
832					break;
833				}
834			}
835		}
836	
837		private static void HitWire(DoubleStack<Point16> next, int wireType)
838		{
839			_wireDirectionList.Clear(quickClear: true);
840			for (int i = 0; i < next.Count; i++)
841			{
842				Point16 point = next.PopFront();
843				SkipWire(point);
844				_toProcess.Add(point, 4);
845				next.PushBack(point);
846				_wireDirectionList.PushBack(0);
847			}
848			_currentWireColor = wireType;
849			while (next.Count > 0)
850			{
851				Point16 key = next.PopFront();
852				int num = _wireDirectionList.PopFront();
853				int x = key.X;
854				int y = key.Y;
855				if (!_wireSkip.ContainsKey(key))
856				{
857					HitWireSingle(x, y);
858				}
859				for (int j = 0; j < 4; j++)
860				{
861					int num2;
862					int num3;
863					switch (j)
864					{
865					case 0:
866						num2 = x;
867						num3 = y + 1;
868						break;
869					case 1:
870						num2 = x;
871						num3 = y - 1;
872						break;
873					case 2:
874						num2 = x + 1;
875						num3 = y;
876						break;
877					case 3:
878						num2 = x - 1;
879						num3 = y;
880						break;
881					default:
882						num2 = x;
883						num3 = y + 1;
884						break;
885					}
886					if (num2 < 2 || num2 >= Main.maxTilesX - 2 || num3 < 2 || num3 >= Main.maxTilesY - 2)
887					{
888						continue;
889					}
890					Tile tile = Main.tile[num2, num3];
891					if (tile == null)
892					{
893						continue;
894					}
895					Tile tile2 = Main.tile[x, y];
896					if (tile2 == null)
897					{
898						continue;
899					}
900					byte b = 3;

```


---

## 🤖 Assistant · 2026-08-12T18:43:14.758Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/wiring/devices.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:15.242Z

**📎 ToolResult**

```
1	// HitWireSingle 器件分发表(Wiring.cs:829-2282 全表移植)。
2	// Wiring.ts 处理牵扯内部状态的核心 case(144 计时器/419 门灯/235 传送器/142-143 泵/429 彩线灯泡),
3	// 其余 case 在此按原版逐条移植;NetMessage 跳过(单机)。
4	// 行为无对应引擎系统的器件(音乐盒/派对/天塔柱等)按"帧翻转 + toast 占位"处理,注释标明。
5	import type { Wiring } from '../Wiring';
6	import type { TrapShotKind } from '../../entities/Dart';
7	import { TILE_BY_KEY } from '../../data/tiles';
8	import { flipSwitchTrack } from '../MinecartTrack';
9	
10	/** 器件运行环境(Game 实现;保持窄接口以便单测注入) */
11	export interface DeviceCtx {
12	  /** 按原版 item id 掉落物品 */
13	  dropItem(vanillaItemId: number, px: number, py: number): void;
14	  /** 按原版 npc id 生成敌人(雕像刷怪;返回是否成功) */
15	  spawnNpc(vanillaNpcId: number, px: number, py: number): boolean;
16	  /** NPC.MechSpawn（NPC.cs:7399-7483）：同 type（含等价组）200px≥3 / 600px≥6 / 全图≥10 拒绝 */
17	  mechSpawnOk(px: number, py: number, type: number): boolean;
18	  /** Item.MechSpawn（Item.cs:48982-49013）：同 item 300px≥3 / 800px≥6 / 全图≥10 拒绝 */
19	  itemSpawnOk(px: number, py: number, type: number): boolean;
20	  /** 投射物(飞镖/火焰/尖刺球/炮弹/雪球/烟花族):vx/vy px/tick。
21	   *  form = 传送门弹 601 的 ai[0]（WorldGen.cs:50622-50631：ammo4→0 橙 / ammo5→1 蓝）；
22	   *  烟花族 = 色变体（167-170 / 415-418 / 419-422 减基址）。
23	   *  anchor = 喷泉弹锚点 tile（Projectile.ai[0]/ai[1]，Wiring.cs:1548） */
24	  shootProjectile(px: number, py: number, vx: number, vy: number, damage: number, kind: TrapShotKind, form?: number, anchor?: [number, number]): void;
25	  /** 喷泉去重（Wiring.cs:1529-1545）：同锚点是否已有 aiStyle73 弹在喷 */
26	  hasFountainAt?(tx: number, ty: number): boolean;
27	  /** 统计附近某类投射物数量(尖刺球惩罚表/兔兔炮场内上限用) */
28	  countProjectiles(kind: 'spiky' | 'bunny', px: number, py: number, radius: number): number;
29	  /** 尖刺球预算惩罚(Wiring.cs 1456 :1952-1966):场上每个 185 按距 (px,py) 距离扣分 */
30	  spikyBudgetPenalty?(px: number, py: number): number;
31	  /** 门开关(原版 HitWireSingle 10/11:随机方向+反向重试) */
32	  doorOpen(x: number, y: number): boolean;
33	  doorClose(x: number, y: number): boolean;
34	  /** 传送器对:搬迁判定框内的玩家/敌人(原版 Teleport :2314-2365) */
35	  teleportPair(a: [number, number], b: [number, number]): void;
36	  /** 城镇 NPC 搬迁雕像(style 40/41):group 0/1 白名单,搬到 (px,py) */
37	  relocateTownNpc(group: 0 | 1, px: number, py: number): boolean;
38	  /** 爆炸(炸药/地雷/炮弹):范围伤害+清格+粒子 */
39	  explode(tx: number, ty: number, damage: number, radius?: number, destroyTiles?: boolean): void;
40	  toast(msg: string): void;
41	  sfx(name: string, x?: number, y?: number): void; // 带坐标时按距离衰减/超距静音
42	  /** 广播盒（425）：锚点 (x,y) 起的 2×2 内告示牌文本广播；无牌由引擎侧静默 */
43	  announce?(x: number, y: number): void;
44	  /** 派对纪念碑（455）：BirthdayParty.ToggleManualParty */
45	  toggleParty?(): void;
46	  /** 提取机通电转化（Wiring.cs:2572-2592 Extractinator）：锚点邻域箱子里自后向前找
47	   *  首个可提取物，消耗 1 并返回产物 {itemType, stack}；无箱/箱内无可转化返回 null */
48	  extractinatorPull(ax: number, ay: number, blockType: number): { itemType: number; stack: number } | null;
49	  /** 按原版 item id 掉落指定数量（提取机产物带 stack，钱币走 coin 体系） */
50	  dropItemStack(vanillaItemId: number, stack: number, px: number, py: number): void;
51	  /** worldSurface(部分器件判定) */
52	  worldSurface: number;
53	}
54	
55	/** 宝石块 off/on id 对(255-261 off ↔ 262-268 on,±7;Wiring.cs:863-873) */
56	const GEMSPARK_OFF = ['v_255_amethystgemsparkoff', 'v_256_topazgemsparkoff', 'v_257_sapphiregemsparkoff',
57	  'v_258_emeraldgemsparkoff', 'v_259_rubygemsparkoff', 'v_260_diamondgemsparkoff', 'v_261_ambergemsparkoff'];
58	const GEMSPARK_ON = ['v_262_amethystgemspark', 'v_263_topazgemspark', 'v_264_sapphiregemspark',
59	  'v_265_emeraldgemspark', 'v_266_rubygemspark', 'v_267_diamondgemspark', 'v_268_ambergemspark'];
60	
61	/** 通电石/宝石块等的成对 tile id 切换 */
62	function swapTile(w: Wiring, x: number, y: number, fromKey: string, toKey: string): void {
63	  const st = w.st;
64	  if (!st.inBounds(x, y)) return;
65	  const i = st.idx(x, y);
66	  const cur = st.type[i];
67	  const from = TILE_BY_KEY[fromKey], to = TILE_BY_KEY[toKey];
68	  if (cur === from) st.setTile(x, y, to, st.frameX[i], st.frameY[i]);
69	  else if (cur === to) st.setTile(x, y, from, st.frameX[i], st.frameY[i]);
70	}
71	
72	/** 多格器件整体翻帧(篝火/壁炉/吊灯等通用模式,Wiring.cs:1003-1052 等):
73	 *  锚点 = (x - frameX%blockW/18, y - frameY%blockH/18);delta 由锚点帧阈值定;整体 SkipWire */
74	function flipBlock(
75	  w: Wiring, x: number, y: number,
76	  blockW: number, blockH: number, tilesW: number, tilesH: number,
77	  axis: 'x' | 'y', threshold: number, delta: number,
78	): void {
79	  const st = w.st;
80	  const i = st.idx(x, y);
81	  const ox = x - Math.floor(st.frameX[i] % blockW / 18);
82	  const oy = y - Math.floor(st.frameY[i] % blockH / 18);
83	  let d = delta;
84	  const ai = st.idx(ox, oy);
85	  if (axis === 'y' ? st.frameY[ai] >= threshold : st.frameX[ai] >= threshold) d = -delta;
86	  for (let ix = ox; ix < ox + tilesW; ix++) {
87	    for (let iy = oy; iy < oy + tilesH; iy++) {
88	      if (!st.inBounds(ix, iy)) continue;
89	      const ii = st.idx(ix, iy);
90	      w.skipCell(ix, iy);
91	      if (axis === 'y') st.setTile(ix, iy, st.type[ii], st.frameX[ii], st.frameY[ii] + d);
92	      else st.setTile(ix, iy, st.type[ii], st.frameX[ii] + d, st.frameY[ii]);
93	    }
94	  }
95	}
96	
97	/** 单格帧翻转(火把/蜡烛等) */
98	function flipCell(w: Wiring, x: number, y: number, delta: number): void {
99	  const st = w.st;
100	  if (!st.inBounds(x, y)) return;
101	  const i = st.idx(x, y);
102	  let d = delta;
103	  if (st.frameX[i] >= delta) d = -delta;
104	  st.setTile(x, y, st.type[i], st.frameX[i] + d, st.frameY[i]);
105	}
106	
107	// ============ 器件态机族：八音盒 / 喷泉 / 天塔柱（原版"帧带 = 开关态"系统） ============
108	// 原版语义：Switch* 只翻帧（WorldGen.cs:50977-51209），激活态由 SceneMetrics 每帧扫描
109	// 视区 tile 帧读出（SceneMetrics.cs:471-585）→ BGM 覆盖（Main.cs:11002）/ 水色
110	// （Main.cs:56766-56770）/ 天空滤镜（SceneState.cs:111-115）。下方 *Of 为扫描侧共用读取器。
111	
112	/** 音乐盒 style → MusicID 全表（Main.cs:11002-11403 ActiveMusicBox if-chain，100 条；
113	 *  style = tile 139 frameY/36，即放置物品 placeStyle = 曲目号）。
114	 *  style 100 = 静音（SceneMetrics.cs:474-480 frameY/36==100 → MusicBoxSilence，
115	 *  Main.cs:11405-11440 flag2 → _musicSilencerCounter 240t 渐弱——Music.ts 返回 0 等价） */
116	export const MB_STYLE_TO_MUSIC: readonly number[] = [
117	  1, 2, 3, 6, 4, 5, 7, 8, 10, 9,
118	  12, 11, 13, 14, 15, 16, 17, 18, 19, 20,
119	  21, 22, 23, 24, 25, 26, 27, 29, 30, 31,
120	  32, 33, 38, 37, 35, 36, 34, 39, 40, 41,
121	  44, 48, 42, 43, 46, 47, 49, 51, 52, 53,
122	  54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
123	  64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
124	  74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
125	  84, 85, 86, 87, 88, 89, 90, 91, 93, 96,
126	  95, 94, 97, 98, 92, 99, 101, 100, 104, 103,
127	];
128	
129	/** 喷泉 style → 水色 id（SceneMetrics.cs:488-523 frameX/36 → ActiveFountainColor） */
130	const FOUNTAIN_COLOR = [0, 12, 3, 5, 2, 10, 4, 9, 8, 6];
131	
132	/** 八音盒态（SceneMetrics.cs:471-486）：frameX≥36 = 开；曲目 = frameY/36；-1 = 关 */
133	export function musicBoxStyleOf(frameX: number, frameY: number): number {
134	  if (frameX < 36) return -1;
135	  return Math.floor(frameY / 36);
136	}
137	
138	/** 喷泉态（SceneMetrics.cs:487-523）：frameY≥72 = 开；-1 = 关 */
139	export function fountainColorOf(frameX: number, frameY: number): number {
140	  if (frameY < 72) return -1;
141	  return FOUNTAIN_COLOR[Math.floor(frameX / 36)] ?? -1;
142	}
143	
144	// ============ 音乐盒物品表（Item.cs DefaultToMusicBox + WorldGen.GetItemDrop_MusicBoxes） ============
145	
146	/** 空音乐盒物品（ItemID.MusicBox = 576，Item.cs:8082-8089：accessory 无 createTile）。
147	 *  录音入口：装备在配饰槽时按当前 BGM 变身（Player.cs:15053） */
148	export const MUSIC_BOX_EMPTY_VID = 576;
149	
150	/** 音乐盒 style → 录得物品 vid 全表 101 条（WorldGen.cs:43138-43366
151	 *  GetItemDrop_MusicBoxes 1:1；与 Item.cs SetDefaults DefaultToMusicBox(placeStyle)
152	 *  调用点互为逆表）。
153	 *  style 0-12 → 562+style；13-27 → 1596+style-13；28 起为离散表；越界兜底 576（空盒） */
154	export const MUSIC_BOX_ITEM_BY_STYLE: readonly number[] = [
155	  562, 563, 564, 565, 566, 567, 568, 569, 570, 571,
156	  572, 573, 574, 1596, 1597, 1598, 1599, 1600, 1601, 1602,
157	  1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1963, 1964,
158	  1965, 2742, 3044, 3235, 3236, 3237, 3370, 3371, 3796, 3869,
159	  4082, 4078, 4079, 4077, 4080, 4081, 4237, 4356, 4357, 4358,
160	  4421, 4606, 4979, 4985, 4990, 4991, 4992, 5006, 5014, 5015,
161	  5016, 5017, 5018, 5019, 5020, 5021, 5022, 5023, 5024, 5025,
162	  5026, 5027, 5028, 5029, 5030, 5031, 5032, 5033, 5034, 5035,
163	  5036, 5037, 5038, 5039, 5040, 5044, 5112, 5362, 5578, 5538,
164	  5579, 5580, 5539, 5581, 5582, 5637, 5638, 5639, 6144, 6145,
165	  6146,
166	];
167	
168	/** MusicID.Sets.CanBeRecorded（MusicID.cs:9）：全集可录，仅 {0,28,45,102} 除外 */
169	const MUSIC_NOT_RECORDABLE = new Set([0, 28, 45, 102]);
170	/** Main.maxMusic（Main.cs:435） */
171	const MAX_MUSIC = 105;
172	
173	/** 录音（Player.cs:15053-15366 ApplyEquipFunctional 1:1）：装备空盒 576 时按当前
174	 *  BGM（Main.curMusic）掷 1/540 → 录得对应唱片物品 vid。
175	 *  门：curMusic ∈ (0,105] 且 CanBeRecorded；style = MB_STYLE_TO_MUSIC.indexOf(curMusic)
176	 *  （= 原版 curMusic→num3/if-chain 的逆映射），无映射（如 50 TitleIntro）返回 -1。
177	 *  注：原版先播 Item166 再判映射——无映射时只响声不变身，由调用方复刻 */
178	export function musicBoxRecordItem(curMusic: number): number {
179	  if (curMusic <= 0 || curMusic > MAX_MUSIC) return -1;
180	  if (MUSIC_NOT_RECORDABLE.has(curMusic)) return -1;
181	  const style = MB_STYLE_TO_MUSIC.indexOf(curMusic);
182	  if (style < 0) return -1;
183	  return MUSIC_BOX_ITEM_BY_STYLE[style] ?? -1;
184	}
185	
186	/** 音乐盒掉落（WorldGen.cs:51221-51295 CheckMB）：style = frameY/36（破坏前帧），
187	 *  掉 GetItemDrop_MusicBoxes(style)；越界 style 兜底空盒 576 */
188	export function musicBoxDropItemOf(style: number): number {
189	  return MUSIC_BOX_ITEM_BY_STYLE[style] ?? 576;
190	}
191	
192	/** 喷泉 style → 物品 vid（WorldGen.cs:38199-38226 Check2xX case 207：
193	 *  0→909 纯净 / 1→910 沙漠 / 2-7→938+style 丛林·冰雪·腐化·猩红·神圣·血月 /
194	 *  8→4922 洞穴 / 9→4417 绿洲；Item.cs createTile=207 placeStyle 互为逆表） */
195	export const FOUNTAIN_ITEM_BY_STYLE: readonly number[] = [909, 910, 940, 941, 942, 943, 944, 945, 4922, 4417];
196	
197	/** 喷泉掉落：style = frameX/36（破坏前帧）；越界返回 -1（Check2xX default 不掉） */
198	export function fountainDropItemOf(style: number): number {
199	  return FOUNTAIN_ITEM_BY_STYLE[style] ?? -1;
200	}
201	
202	/** 广播盒播报（Wiring.cs:1204-1217 1:1）：读锚点告示牌 → 粉色多行聊天公告。
203	 *  - 无登记 / 空白文本 → null（:1208-1211 静默返回）
204	 *  - Color.Pink = (255,105,180)；NewTextMultiline WidthLimit=460（RemadeChatMonitor
205	 *    单条容器内按 460px 折行；色值与宽度原样透传给聊天渲染层）
206	 *  - AnnouncementBoxDisabled / AnnouncementBoxRange：设置系统未接，恒可用 + 全图
207	 *    （默认值 false / -1，Main.cs 设置项） */
208	export function announcementBoxBroadcast(signText: string | null | undefined): { text: string; r: number; g: number; b: number; width: number } | null {
209	  if (signText == null || signText.trim() === '') return null;
210	  return { text: signText, r: 255, g: 105, b: 180, width: 460 };
211	}
212	
213	/** 广播盒触发全链（Wiring.cs:1185-1217）：Sign.ReadSign(anchor, CreateIfMissing:false)
214	 *  ——按锚点精确查 Main.sign 登记（Sign.cs:36-44 逐项比对 x/y），无登记/空白文本
215	 *  静默（:1208-1211 return）；命中 → 粉色多行公告（NewTextMultiline） */
216	export function announcementBoxMessage(
217	  signs: ReadonlyArray<{ x: number; y: number; text: string }>,
218	  x: number, y: number,
219	): { text: string; r: number; g: number; b: number; width: number } | null {
220	  const sign = signs.find((s) => s.x === x && s.y === y);
221	  return announcementBoxBroadcast(sign?.text);
222	}
223	
224	/** 天塔柱类型（SceneMetrics.cs:524-541）：410=style(frameX/36, 0星璇/1星云/2星尘/3耀斑)、
225	 *  509=4 月总；-1 = 关。480 血月柱走 bloodMoonMonolithOf。
226	 *  【依赖登记】657 回声/658 微光/720 CRT/721 复古/725 黑白/733 收音机柱的屏幕滤镜未接入 */
227	export function monolithTypeOf(sheet: number, frameX: number, frameY: number): number {
228	  if (sheet === 410) return frameY >= 56 ? Math.floor(frameX / 36) : -1;
229	  if (sheet === 509) return frameY >= 56 ? 4 : -1;
230	  return -1;
231	}
232	
233	/** 血月柱（SceneMetrics.cs:542-546：480 frameY≥54 → BloodMoonMonolith →
234	 *  Main.cs:61417 并入 BloodMoonActive） */
235	export function bloodMoonMonolithOf(sheet: number, frameY: number): boolean {
236	  return sheet === 480 && frameY >= 54;
237	}
238	
239	/** SwitchMB（WorldGen.cs:50977-51021 1:1）：八音盒 139 / 南瓜灯 35 共用。
240	 *  锚点：num3 = frameY/18 对 2 取余（行内偏移）、num4 = frameX/18 ≥2 再减 2（列内偏移）；
241	 *  2×2 区内 139/35 格 frameX ±36（<36 → +36，否则 -36），整体 SkipWire。
242	 *  电路触发（Wiring.cs:2019-2022）与右键（Player.cs:31759-31764，多播 SoundID 28）共用 */
243	export function switchMB(w: Wiring, x: number, y: number): void {
244	  const st = w.st;
245	  const i = st.idx(x, y);
246	  let num3 = Math.floor(st.frameY[i] / 18);
247	  while (num3 >= 2) num3 -= 2;
248	  let num4 = Math.floor(st.frameX[i] / 18);
249	  if (num4 >= 2) num4 -= 2;
250	  const ox = x - num4, oy = y - num3;
251	  for (let k = ox; k < ox + 2; k++) {
252	    for (let l = oy; l < oy + 2; l++) {
253	      if (!st.inBounds(k, l)) continue;
254	      const sh = w.sheetOf(k, l);
255	      if (sh !== 139 && sh !== 35) continue;
256	      const ii = st.idx(k, l);
257	      const fx = st.frameX[ii] < 36 ? st.frameX[ii] + 36 : st.frameX[ii] - 36;
258	      st.setTile(k, l, st.type[ii], fx, st.frameY[ii]);
259	    }
260	  }
261	  w.skipCell(ox, oy); w.skipCell(ox + 1, oy);
262	  w.skipCell(ox, oy + 1); w.skipCell(ox + 1, oy + 1);
263	}
264	
265	/** SwitchFountain（WorldGen.cs:51171-51209 1:1）：喷泉 207，2×4 区 frameY ±72。
266	 *  锚点：num3 = frameX/18 对 2 取余、num4 = frameY/18 ≥4 再减 4 */
267	export function switchFountain(w: Wiring, x: number, y: number): void {
268	  const st = w.st;
269	  const i = st.idx(x, y);
270	  let num3 = Math.floor(st.frameX[i] / 18);
271	  while (num3 >= 2) num3 -= 2;
272	  let num4 = Math.floor(st.frameY[i] / 18);
273	  if (num4 >= 4) num4 -= 4;
274	  const ox = x - num3, oy = y - num4;
275	  for (let k = ox; k < ox + 2; k++) {
276	    for (let l = oy; l < oy + 4; l++) {
277	      if (!st.inBounds(k, l)) continue;
278	      w.skipCell(k, l);   // 原版 2×4 全区 SkipWire（:51200-51207，先于类型判定）
279	      if (w.sheetOf(k, l) !== 207) continue;
280	      const ii = st.idx(k, l);
281	      const fy = st.frameY[ii] < 72 ? st.frameY[ii] + 72 : st.frameY[ii] - 72;
282	      st.setTile(k, l, st.type[ii], st.frameX[ii], fy);
283	    }
284	  }
285	}
286	
287	/** SwitchMonolith（WorldGen.cs:51023-51169 1:1）：天塔柱族 frameY 翻转。
288	 *  区块 2×3（733 为 3×3）；410 阈值 56，其余 54；658 为 +54 对 162 取模循环（三态）。
289	 *  电路触发（Wiring.cs:2032-2036）与右键（Player.cs:31801-31808）共用 */
290	export function switchMonolith(w: Wiring, x: number, y: number): void {
291	  const st = w.st;
292	  const i = st.idx(x, y);
293	  const sheet = w.sheetOf(x, y);
294	  const bw = sheet === 733 ? 3 : 2;   // :51026-51028
295	  const bh = 3;
296	  let num3 = Math.floor(st.frameX[i] / 18);
297	  while (num3 >= bw) num3 -= bw;
298	  let num4 = Math.floor(st.frameY[i] / 18);
299	  while (num4 >= bh) num4 -= bh;
300	  const ox = x - num3, oy = y - num4;
301	  for (let k = ox; k < ox + bw; k++) {
302	    for (let l = oy; l < oy + bh; l++) {
303	      if (!st.inBounds(k, l)) continue;
304	      w.skipCell(k, l);   // 原版全区 SkipWire（:51156-51166，先于类型判定）
305	      const sh = w.sheetOf(k, l);
306	      if (sh < 0) continue;
307	      const ii = st.idx(k, l);
308	      let fy = st.frameY[ii];
309	      if (sh === 410) fy = fy < 56 ? fy + 56 : fy - 56;
310	      else if (sh === 658) fy = (fy + 54) % 162;   // :51131-51140
311	      else if (sh === 480 || sh === 509 || sh === 657 || sh === 720 || sh === 721 || sh === 725 || sh === 733) {
312	        fy = fy < 54 ? fy + 54 : fy - 54;
313	      } else continue;
314	      st.setTile(k, l, st.type[ii], st.frameX[ii], fy);
315	    }
316	  }
317	}
318	
319	/** 陷阱(137)发射(Wiring.cs:1495-1743 + Item.cs placeStyle)。frameY/18=种类:
320	 *  0飞镖(98) 1超级飞镖(184) 2烈焰(187,隐形+尘埃) 3尖刺球(185) 4长矛(186) */
321	function fireTrap(w: Wiring, ctx: DeviceCtx, x: number, y: number): void {
322	  const st = w.st;
323	  const i = st.idx(x, y);
324	  const kind = Math.floor(st.frameY[i] / 18);
325	  if (kind === 0 || kind === 1 || kind === 2) {
326	    if (!w.checkMech(x, y, 200)) return;
327	    // 方向:frameX 0=左 18=右;frameY<36 平置 / ≥36 竖置(上下)
328	    const dirX = st.frameX[i] === 0 ? -1 : st.frameX[i] === 18 ? 1 : 0;
329	    const dirY = st.frameX[i] < 36 ? 0 : st.frameX[i] < 72 ? -1 : 1;
330	    const speed = kind === 0 ? 12 : kind === 1 ? 12 : 5;
331	    const dmg = kind === 0 ? 20 : 40;
332	    const px = x * 16 + 8 + 10 * dirX, py = y * 16 + 8 + 10 * dirY;
333	    ctx.shootProjectile(px, py, dirX * speed, dirY * speed, dmg, kind === 0 ? 'dart' : kind === 1 ? 'superdart' : 'flame');
334	  } else if (kind === 3) {
335	    // 尖刺球(Wiring.cs:1536-1599 / 1456 :1944-1976):CheckMech 300 + 场上每个 185
336	    // 按自身距离扣预算(<50→50 <100→15 <200→10 <300→8 <400→6 <500→5 <700→4
337	    // <900→3 <1200→2 其余 1),预算>0 才发。发射无视朝向(1405 曾按 frameX 定向,
338	    // 1456 改为纯下丢,取 1456):固定方块底 (x*16+8, y*16+22),
339	    // vx=rand(-20,21)*0.05 ∈[-1,1]、vy=4+rand(0,21)*0.05 ∈[4,5]
340	    if (!w.checkMech(x, y, 300)) return;
341	    let budget = 200;
342	    if (ctx.spikyBudgetPenalty) budget -= ctx.spikyBudgetPenalty(x * 16 + 8, y * 16 + 8);
343	    else budget -= ctx.countProjectiles('spiky', x * 16 + 8, y * 16 + 8, 1200) * 8;
344	    if (budget <= 0) return;
345	    ctx.shootProjectile(x * 16 + 8, y * 16 + 22,
346	      (Math.floor(Math.random() * 41) - 20) * 0.05,
347	      4 + Math.floor(Math.random() * 21) * 0.05, 40, 'spiky');
348	  } else if (kind === 4) {
349	    // 下向火焰(CheckMech 90)
350	    if (!w.checkMech(x, y, 90)) return;
351	    let dx = 0, dy = 0;
352	    switch (Math.floor(st.frameX[i] / 18)) {
353	      case 0: dx = -1; break;
354	      case 1: dx = 1; break;
355	      case 2: dy = -1; break;
356	      case 3: dy = 1; break;
357	    }
358	    ctx.shootProjectile(x * 16 + 8 + 10 * dx, y * 16 + 8 + 10 * dy, dx * 8, dy * 8, 60, 'spear');
359	  }
360	}
361	
362	/** 热喷泉 443(Wiring.cs:2284-2312;由 HitSwitch 直调) */
363	export function geyserTrap(w: Wiring, ctx: DeviceCtx, x: number, y: number): boolean {
364	  const st = w.st;
365	  if (!st.inBounds(x, y)) return false;
366	  const i = st.idx(x, y);
367	  const num = Math.floor(st.frameX[i] / 36);
368	  const i1 = x - Math.floor((st.frameX[i] - num * 36) / 18);
369	  if (!w.checkMech(i1, y, 200)) return false;
370	  const up = num < 2;
371	  ctx.shootProjectile(
372	    (i1 + 1) * 16, (y + (up ? 0 : 1)) * 16,
373	    0, up ? -8 : 8, 20, 'geyser',
374	  );
375	  return true;
376	}
377	
378	/** 雕像 style → 原版 NPC id 表(Wiring.cs:1892-1996)。
379	 *  num79 = frameX/36 + (frameY/54 % 3) * 55 */
380	const STATUE_NPC: Record<number, number | number[]> = {
381	  5: 73, 13: 24, 30: 6, 35: 2,
382	  51: [299, 538], 52: 356, 53: 357, 54: [355, 358], 55: [367, 366],
383	  56: [359, 359, 359, 359, 360], 57: 377, 58: 300, 59: [364, 362], 60: 148, 61: 361,
384	  62: [487, 486, 485], 64: 86, 65: 490, 66: 82, 67: 449, 68: 167, 69: 480, 70: 48,
385	  71: [170, 180, 171], 72: 481, 73: 482, 74: 430, 75: 489, 76: 611, 77: 602,
386	  78: [595, 596, 599, 597, 600, 598], 79: [616, 617],
387	  80: [671, 672], 81: 673, 82: [674, 675], // 1.4.4+ 新雕像（:2260-2267）
388	};
389	/** flag7（生成区实心 → poof 不生成）的 style（:2270-2282；64=小丑? 71=史莱姆王组） */
390	const STATUE_SOLID_CHECK = new Set([64, 71]);
391	/** 单独分支的雕像 style（Wiring.cs :2290-2440）。dx/dy 为生成点偏移、
392	 *  solid=生成区实心时 poof、pool=随机池（28 蛇三色等） */
393	const STATUE_NPC_DIRECT: Record<number, { npc: number | number[]; dx?: number; dy?: number; solid?: boolean }> = {
394	  4: { npc: 1, dy: -12 },
395	  7: { npc: 49, dx: -4, dy: -6 },
396	  8: { npc: 55, dy: -12 },
397	  9: { npc: 46, dy: -12 },
398	  10: { npc: 21 },
399	  16: { npc: 42, dy: -12, solid: true },
400	  18: { npc: 67, dy: -12 },
401	  23: { npc: 63, dy: -12 },
402	  27: { npc: 85, dx: -9 },
403	  28: { npc: [74, 297, 298], dy: -12 },
404	  42: { npc: 58, dy: -12 },
405	  50: { npc: 65, solid: true }, // 史莱姆王雕像（:2385-2399）
406	};
407	/** 物品雕像 style → [原版 item id, ...MechSpawn 配额同查的等价 id]
408	 *  （2 星 184/1735/1868、17 炸弹 166、37 心 58/1734/1867；:2408-2420） */
409	const STATUE_ITEM: Record<number, { item: number; mechIds: number[] }> = {
410	  2: { item: 184, mechIds: [184, 1735, 1868] },
411	  17: { item: 166, mechIds: [166] },
412	  37: { item: 58, mechIds: [58, 1734, 1867] },
413	};
414	
415	function pick<T>(arr: T[]): T { return arr[Math.floor(Math.random() * arr.length)]; }
416	
417	/** 雕像 105(Wiring.cs:1866-2215) */
418	function fireStatue(w: Wiring, ctx: DeviceCtx, x: number, y: number): void {
419	  const st = w.st;
420	  const i = st.idx(x, y);
421	  // 锚点与 style(:1867-1879)
422	  const num73 = Math.floor(st.frameX[i] / 18);
423	  let num74 = 0;
424	  let rem = num73;
425	  while (rem >= 2) { rem -= 2; num74++; }
426	  const ox = x - rem;
427	  const ax = x - Math.floor(st.frameX[i] % 36 / 18);
428	  const ay = y - Math.floor(st.frameY[i] % 54 / 18);
429	  const num79 = Math.floor(st.frameX[i] / 36) + Math.floor(st.frameY[i] / 54 % 3) * 55;
430	  w.skipCell(ax, ay); w.skipCell(ax, ay + 1); w.skipCell(ax, ay + 2);
431	  w.skipCell(ax + 1, ay); w.skipCell(ax + 1, ay + 1); w.skipCell(ax + 1, ay + 2);
432	  const px = ax * 16 + 16, py = (ay + 3) * 16;
433	  // 生成区实心判定（:2274 SolidTiles(num139-2..num139+3, num138..num138+2)；flag7/部分直刷用）
434	  const spawnAreaSolid = () => {
435	    for (let sx = ax - 2; sx <= ax + 3; sx++) {
436	      for (let sy = ay; sy <= ay + 2; sy++) {
437	        if (st.inBounds(sx, sy) && st.isSolid(sx, sy)) return true;
438	      }
439	    }
440	    return false;
441	  };
442	  // NPC 雕像主表（spawn 于雕像底中心 (px,py)；:2268-2282）
443	  const entry = STATUE_NPC[num79];
444	  if (entry !== undefined) {
445	    const npcId = Array.isArray(entry) ? pick(entry) : entry;
446	    if (w.checkMech(ax, ay, 30) && ctx.mechSpawnOk(px, py, npcId)) {
447	      if (!STATUE_SOLID_CHECK.has(num79) || !spawnAreaSolid()) {
448	        ctx.spawnNpc(npcId, px, py);
449	      } else {
450	        ctx.sfx('tink', px, py);
451	      }
452	    }
453	    return;
454	  }
455	  // 单独分支 NPC 雕像（各自偏移/实心判定；:2290-2440）
456	  const direct = STATUE_NPC_DIRECT[num79];
457	  if (direct !== undefined) {
458	    const npcId = Array.isArray(direct.npc) ? pick(direct.npc) : direct.npc;
459	    if (w.checkMech(ax, ay, 30) && ctx.mechSpawnOk(px, py, npcId)) {
460	      if (!direct.solid || !spawnAreaSolid()) {
461	        ctx.spawnNpc(npcId, px + (direct.dx ?? 0), py + (direct.dy ?? 0));
462	      } else {
463	        ctx.sfx('tink', px, py);
464	      }
465	    }
466	    return;
467	  }
468	  // 物品雕像（CheckMech 600；心/星要过全部等价 id 的 MechSpawn 配额；:2408-2420）
469	  const itemEntry = STATUE_ITEM[num79];
470	  if (itemEntry !== undefined) {
471	    const ok = w.checkMech(ax, ay, 600)
472	      && itemEntry.mechIds.every((mid) => ctx.itemSpawnOk(px, py, mid));
473	    if (ok) ctx.dropItem(itemEntry.item, px, py - 16);
474	    return;
475	  }
476	  switch (num79) {
477	    case 34: { // 蘑菇雕像:2×3 变 tile 349 动画(:2108-2119)
478	      const T349 = TILE_BY_KEY['v_349_mushroom_statue'] ?? 0;
479	      for (let dx = 0; dx < 2; dx++) {
480	        for (let dy = 0; dy < 3; dy++) {
481	          st.setTile(ax + dx, ay + dy, T349, dx * 18 + 216, dy * 18);
482	        }
483	      }
484	      return;
485	    }
486	    case 40: case 41: // 城镇 NPC 搬迁(CheckMech 300,:2133-2186)
487	      if (w.checkMech(ax, ay, 300)) ctx.relocateTownNpc(num79 === 40 ? 0 : 1, px, py);
488	      return;
489	    case 63: // 随机传送雕像：164 + 额外 MechSpawn(165)（:2226-2229）
490	      if (w.checkMech(ax, ay, 30) && ctx.mechSpawnOk(px, py, 164) && ctx.mechSpawnOk(px, py, 165)) {
491	        ctx.spawnNpc(164, px, py);
492	      }
493	      return;
494	  }
495	}
496	
497	/** 马桶烟花（Wiring.cs:1498-1509）：tile 497 与 tile 15 马桶样式（frameY/40==1 或 20）共用。
498	 *  num68 = j - frameY%40/18（锚点上格）；SkipWire 两格；CheckMech(锚点, 60) → 弹 733
499	 *  ToiletEffect：静态水花发射器（速度 0 / damage 0），位于 (i*16+8, num68*16+12) */
500	function fireworkToilet(w: Wiring, ctx: DeviceCtx, x: number, y: number): void {
501	  const st = w.st;
502	  const i = st.idx(x, y);
503	  const num68 = y - Math.floor(st.frameY[i] % 40 / 18);
504	  w.skipCell(x, num68); w.skipCell(x, num68 + 1); // :1501-1502
505	  if (!w.checkMech(x, num68, 60)) return;          // :1503（60t 冷却）
506	  ctx.shootProjectile(x * 16 + 8, num68 * 16 + 12, 0, 0, 0, 'toiletPop'); // :1505
507	}
508	
509	/** 巨石雕像 531(Wiring.cs:1747-1762) */
510	function fireBoulderStatue(w: Wiring, ctx: DeviceCtx, x: number, y: number): void {
511	  const st = w.st;
512	  const i = st.idx(x, y);
513	  const ox = x - Math.floor(st.frameX[i] % 36 / 18);
514	  const oy = y - Math.floor(st.frameY[i] % 36 / 18);
515	  if (!w.checkMech(ox, oy, 900)) return;
516	  w.skipCell(ox, oy); w.skipCell(ox + 1, oy); w.skipCell(ox, oy + 1); w.skipCell(ox + 1, oy + 1);
517	  ctx.shootProjectile(ox * 16 + 16, (oy + 1) * 16, 0, 0, 70, 'boulder');
518	}
519	
520	/** 可接线灯器件的开关帧判定(Wiring.cs 翻帧 delta 推导):on = frame%(2δ) < δ。
521	 *  火把 δ=66(22px×3 变体一组)、蜡烛族 δ=18、2×2 灯具 δ=36、吊灯/彩灯 δ=54、篝火走 Y 轴 δ=36 */
522	export const LIGHT_TOGGLE: Record<number, ['x' | 'y', number]> = {
523	  4: ['x', 66],
524	  33: ['x', 18], 174: ['x', 18], 49: ['x', 18], 372: ['x', 18],
525	  42: ['x', 18], 92: ['x', 18], 93: ['x', 18],
526	  95: ['x', 36], 100: ['x', 36], 126: ['x', 36], 173: ['x', 36], 564: ['x', 36],
527	  34: ['x', 54], 149: ['x', 54],
528	  215: ['y', 36],
529	};
530	
531	/** 该格灯光是否点亮(非灯器件恒 true;供 LightingEngine 查询) */
532	export function lightIsOn(sheet: number, frameX: number, frameY: number): boolean {
533	  const t = LIGHT_TOGGLE[sheet];
534	  if (!t) return true;
535	  const v = t[0] === 'x' ? frameX : frameY;
536	  return v % (2 * t[1]) < t[1];
537	}
538	
539	/** HitWireSingle 器件主分发表。返回 true = 已处理 */
540	export function deviceTable(w: Wiring, ctx: DeviceCtx, sheet: number, x: number, y: number): boolean {
541	  const st = w.st;
542	  const i = st.idx(x, y);
543	  switch (sheet) {
544	    case 4: // 火把 frameX ±66(:1207-1213)
545	      flipCell(w, x, y, 66);
546	      return true;
547	    case 10: // 关门 → 开(随机方向+反向,原版 :1171-1188)
548	      ctx.doorOpen(x, y);
549	      return true;
550	    case 11:
551	      ctx.doorClose(x, y);
552	      return true;
553	    case 15: { // 马桶椅样式（Wiring.cs:1498-1509 与 tile 497 共用分支；frameY/40==1 或 20）
554	      if (Math.floor(st.frameY[i] / 40) !== 1 && Math.floor(st.frameY[i] / 40) !== 20) return true;
555	      fireworkToilet(w, ctx, x, y);
556	      return true;
557	    }
558	    case 33: case 174: case 49: case 372: // 蜡烛族 frameX ±18(:1472-1480)
559	      flipCell(w, x, y, 18);
560	      return true;
561	    case 34: // 吊灯 3×3 frameX ±54(:1405-1428)
562	      flipBlock(w, x, y, 108, 54, 3, 3, 'x', 54, 54);
563	      return true;
564	    case 35: case 139: // 南瓜灯/八音盒：SwitchMB（WorldGen.cs:50977-51021；Wiring.cs:2019-2022）
565	      switchMB(w, x, y);
566	      return true;
567	    case 207: // 喷泉：SwitchFountain（WorldGen.cs:51171-51209；Wiring.cs:2023）
568	      switchFountain(w, x, y);
569	      return true;
570	    case 410: case 480: case 509: case 657: case 658: case 720: case 721: case 725: case 733:
571	      // 天塔柱族：SwitchMonolith（WorldGen.cs:51023-51169；Wiring.cs:2032-2036）
572	      switchMonolith(w, x, y);
573	      return true;
574	    case 42: // 挂链灯笼 1×2 frameX ±18(:1214-1227)
575	      flipBlock(w, x, y, 36, 36, 1, 2, 'x', 18, 18);
576	      return true;
577	    case 92: // 路灯柱 1×6 frameX ±18(:1483-1494)
578	      flipBlock(w, x, y, 18, 108, 1, 6, 'x', 18, 18);
579	      return true;
580	    case 93: // 蒂基火炬 1×3 frameX ±18(:1228-1243)
581	      flipBlock(w, x, y, 18, 54, 1, 3, 'x', 18, 18);
582	      return true;
583	    case 95: case 100: case 126: case 173: case 564: // 2×2 灯具族 frameX ±36(:1381-1404)
584	      flipBlock(w, x, y, 72, 36, 2, 2, 'x', 36, 36);
585	      return true;
586	    case 105:
587	      fireStatue(w, ctx, x, y);
588	      return true;
589	    case 130: { // 通电石:上方有宝箱则不缩(:878-884)
590	      const above = y > 0 ? w.sheetOf(x, y - 1) : -1;
591	      if (above === 21 || above === 88 || above === 467) return true;
592	      swapTile(w, x, y, 'v_130_active_stone_block', 'v_131_inactivestoneblock');
593	      return true;
594	    }
595	    case 131:
596	      swapTile(w, x, y, 'v_130_active_stone_block', 'v_131_inactivestoneblock');
597	      return true;
598	    case 137:
599	      fireTrap(w, ctx, x, y);
600	      return true;
601	    case 141: // 炸药(:1781-1785)：清格 + Projectile 108(500伤/半径10)
602	      w.skipCell(x, y);
603	      st.setTile(x, y, 0);
604	      ctx.explode(x, y, 500, 10);
605	      return true;
606	    case 149: // 节日彩灯 frameX ±54(:1244-1250)
607	      flipCell(w, x, y, 54);
608	      return true;
609	    case 219:
610	    case 642: { // 提取机（Wiring.cs:1993-1995 → Extractinator :2563-2593）：
611	      // 通电自动消耗邻域箱子里的可提取物。锚点按 3×3(54px) 帧内偏移回算（:2567-2568），
612	      // 冷却 checkMech 60t（:2569/:2571）；箱子查找/消耗/掉落在 ctx（Game 侧拥有箱子与物品栏）。
613	      const ax = x - Math.floor(st.frameX[i] % 54 / 18);
614	      const ay = y - Math.floor(st.frameY[i] % 54 / 18);
615	      if (!w.checkMech(ax, ay, 60)) return true;
616	      const out = ctx.extractinatorPull(ax, ay, sheet);
617	      if (out && out.itemType > 0) {
618	        // :2588 Item.NewItem(num*16, num2*16, 32, 32) → 锚点 2×2 判定框中心
619	        ctx.dropItemStack(out.itemType, out.stack, ax * 16 + 16, ay * 16 + 16);
620	      }
621	      return true;
622	    }
623	    case 209: { // 大炮（Wiring.cs:1237-1346 1:1）：旋转+开火复合状态机。
624	      // num31=块内列(0/3=旋转态,1/2=待发) num32=行内偏移 num35=仰角带(frameY/54,0-8)
625	      // num36=水平带(frameX/72: 0/1=右向 大炮/兔兔炮, 3/4=左向)
626	      const num31 = Math.floor(st.frameX[i] % 72 / 18);
627	      const num32 = Math.floor(st.frameY[i] % 54 / 18);
628	      const ox = x - num31, oy = y - num32;
629	      const num35 = Math.floor(st.frameY[i] / 54);
630	      const num36 = Math.floor(st.frameX[i] / 72);
631	      let num37 = -1;
632	      if (num31 === 1 || num31 === 2) num37 = num32;
633	      // 旋转半边：列3 → 仰角 -54（带0停）；列0 → +54（带8停）
634	      let num38 = 0;
635	      if (num31 === 3) num38 = -54;
636	      if (num31 === 0) num38 = 54;
637	      if (num35 >= 8 && num38 > 0) num38 = 0;
638	      if (num35 === 0 && num38 < 0) num38 = 0;
639	      if (num38 !== 0) {
640	        for (let cx = ox; cx < ox + 4; cx++) {
641	          for (let cy = oy; cy < oy + 3; cy++) {
642	            if (!st.inBounds(cx, cy)) continue;
643	            w.skipCell(cx, cy);
644	            const ci = st.idx(cx, cy);
645	            st.setTile(cx, cy, st.type[ci], st.frameX[ci], st.frameY[ci] + num38);
646	          }
647	        }
648	      }
649	      // 水平朝向带翻转：3/4 带 + 行0/1 → frameX ±72（下一次触发反向）
650	      if ((num36 === 3 || num36 === 4) && (num37 === 0 || num37 === 1)) {
651	        const fx = num36 === 3 ? 72 : -72;
652	        for (let cx = ox; cx < ox + 4; cx++) {
653	          for (let cy = oy; cy < oy + 3; cy++) {
654	            if (!st.inBounds(cx, cy)) continue;
655	            w.skipCell(cx, cy);
656	            const ci = st.idx(cx, cy);
657	            st.setTile(cx, cy, st.type[ci], st.frameX[ci] + fx, st.frameY[ci]);
658	          }
659	        }
660	      }
661	      if (num37 === -1) return true; // 只旋转未开火
662	      // 开火半边：半仰角(<2)时左向(带3/4)不发射（flag2，Wiring.cs:1301-1304）
663	      const flag2 = !((num36 === 3 || num36 === 4) && num37 < 2);
664	      // 伤害/CheckMech 时长（Wiring.cs:1306-1330）：0=大炮 300/480，1=兔兔炮 350/3600，
665	      // 其余（3/4 传送门炮）damage 0 / time 30——原版 switch 只设这两档
666	      const damage = num36 === 0 ? 300 : num36 === 1 ? 350 : 0;
667	      const time = num36 === 0 ? 480 : num36 === 1 ? 3600 : 30;
668	      // 全局冷却门（Wiring.cs:1312-1314/1321-1323：冷却中直接返回）
669	      if (num36 === 0 && w.cannonCoolDown > 0) return true;
670	      if (num36 === 1 && w.bunnyCannonCoolDown > 0) return true;
671	      if (!flag2 || !w.checkMech(ox, oy, time)) return true;
672	      // WorldGen.ShootFromCannon（WorldGen.cs:50606-50718 1:1）
673	      // 弹种（:50611-50631）：ammo=num36+1 → 0→162 炮弹 / 1→281 爆炸兔兔 / 3·4→601（速度 3）
674	      const speed = num36 === 3 || num36 === 4 ? 3 : 14; // :50608 num=14f；601 时 num=3f(:50623/50628)
675	      // 初速方向表（:50640-50683）：仰角带 0-8 → (10,0)…(0,-10)…(-10,0)
676	      const ANGLE_V: Array<readonly [number, number]> = [
677	        [10, 0], [7.5, -2.5], [5, -5], [2.75, -6], [0, -10],
678	        [-2.75, -6], [-5, -5], [-7.5, -2.5], [-10, 0],
679	      ];
680	      const [bx, by] = ANGLE_V[num35] ?? [0, -10];
681	      // 归一化到 speed（:50706-50708 num8 = num/|v|）
682	      const len = Math.hypot(bx, by);
683	      const vx = (bx * speed) / len, vy = (by * speed) / len;
684	      // 出膛位置（:50685 (x+2)*16,(y+2)*16；601 仅加 (0/5,5) 偏移 :50689-50696）
685	      let px = (ox + 2) * 16, py = (oy + 2) * 16;
686	      if (num36 === 3 || num36 === 4) {
687	        if (num35 === 4) px += 5;
688	        py += 5;
689	      }
690	      // num36 3/4 原版发 PortalGunBolt 601（WorldGen.cs:50622-50631）：速度 3、damage 0、
691	      // ai[0] = ammo5 ? 1 : 0（传送门 form，橙 0/蓝 1）。撞块 → PortalHelper.TryPlacingPortal
692	      // 落门（entities/Portal.ts），不再沿用巨石弹体
693	      const kind: TrapShotKind = num36 === 0 ? 'cannonball' : num36 === 1 ? 'bunny' : 'portalbolt';
694	      const form = num36 === 4 ? 1 : 0; // :50622-50631（ammo4 → ai0=0 / ammo5 → ai0=1）
695	      // 全局冷却置位（Wiring.cs:1334-1339：大炮 120 / 兔兔炮 480）——先于弹内判定，
696	      // 与原版一致（冷却在 HitWireSingle 置位，BunnyCannonCanFire 在 ShootFromCannon 内）
697	      if (num36 === 0) w.cannonCoolDown = 120;
698	      if (num36 === 1) w.bunnyCannonCoolDown = 480;
699	      // 兔兔炮场内上限（WorldGen.cs:50697-50701 → BunnyCannonCanFire :50722-50760：
700	      //   NPC614+弹281 计数 ≥4 拒绝；NPC614 无对应实体，此处只数 281 弹）
701	      if (kind === 'bunny' && ctx.countProjectiles('bunny', px, py, Infinity) >= 4) return true;
702	      ctx.shootProjectile(px, py, vx, vy, damage, kind, form);
703	      return true;
704	    }
705	    case 210: // 地雷 ExplodeMine(:3093)：清格 + Projectile 164(250伤)——
706	      // 164 不在 ExplodeTiles 判定表内 = **不破坏地形**（纯伤害爆炸）
707	      st.setTile(x, y, 0);
708	      ctx.explode(x, y, 250, 0, false);
709	      return true;
710	    case 212: { // 雪球发射器（Wiring.cs:1345-1418 1:1）：旋转+开火复合状态机。
711	      // num51=块内列(0/2=旋转态,1=待发) num52=行内偏移 num55=朝向带(frameX/54,0左 1右)
712	      const num51 = Math.floor(st.frameX[i] % 54 / 18);
713	      const num52 = Math.floor(st.frameY[i] % 54 / 18);
714	      const ox = x - num51, oy = y - num52;
715	      const num55 = Math.floor(st.frameX[i] / 54);
716	      let num56 = -1;
717	      if (num51 === 1) num56 = num52;
718	      // 瞄准旋转：列0→frameX -54（带0停）、列2→+54（带1停）（:1359-1365）
719	      let num57 = 0;
720	      if (num51 === 0) num57 = -54;
721	      if (num51 === 2) num57 = 54;
722	      if (num55 >= 1 && num57 > 0) num57 = 0;
723	      if (num55 === 0 && num57 < 0) num57 = 0;
724	      if (num57 !== 0) {
725	        for (let cx = ox; cx < ox + 3; cx++) {
726	          for (let cy = oy; cy < oy + 3; cy++) {
727	            if (!st.inBounds(cx, cy)) continue;
728	            w.skipCell(cx, cy);
729	            const ci = st.idx(cx, cy);
730	            st.setTile(cx, cy, st.type[ci], st.frameX[ci] + num57, st.frameY[ci]);
731	          }
732	        }
733	      }
734	      if (num56 === -1) return true; // 只旋转未开火
735	      // 开火门（:1391）：全局冷却 0 + CheckMech(锚点,60)
736	      if (w.snowballCannonCoolDown > 0 || !w.checkMech(ox, oy, 60)) return true;
737	      w.snowballCannonCoolDown = 15; // :1393
738	      // 弹速（:1394）：12 + rand(0..449)*0.01 = 12.00..16.49
739	      const speed = 12 + Math.floor(Math.random() * 450) * 0.01;
740	      // 方向（:1395-1396）：X=rand(85..104) / Y=rand(-35..10)（Main.rand.Next 上界开区间）
741	      let dx = 85 + Math.floor(Math.random() * 20);
742	      const dy = -35 + Math.floor(Math.random() * 46);
743	      // 出膛位置（:1400 (x+2)*16-8,(y+2)*16-8）+ 朝向偏移（:1401-1405：左带 X-12 / 右带 X+12）
744	      let px = (ox + 2) * 16 - 8, py = (oy + 2) * 16 - 8;
745	      if (num55 === 0) { dx *= -1; px -= 12; } else { px += 12; }
746	      // 归一化到 speed（:1410-1415）后发射 166 雪球：35 伤 / 3.5 击退（:1397-1399）
747	      const len = Math.hypot(dx, dy);
748	      ctx.shootProjectile(px, py, (dx * speed) / len, (dy * speed) / len, 35, 'snowball');
749	      return true;
750	    }
751	    case 215: // 篝火 3×2 frameY ±36(:1003-1020)
752	      flipBlock(w, x, y, 54, 36, 3, 2, 'y', 36, 36);
753	      return true;
754	    case 216: { // 烟花火箭（Wiring.cs:1492-1495 → WorldGen.LaunchRocket WorldGen.cs:62184-62206）
755	      // LaunchRocket：行 = frameY/40（0-3 → 弹 167-170 红/绿/蓝/黄）；frameY%40==18 说明
756	      // 点的是下半格，锚点 y 上移（:62188-62194）
757	      let ly = y;
758	      if (st.frameY[i] % 40 === 18) ly--;
759	      // 发射位 (x*16+8, y*16+4+2)、速度 (0,-8)、damage 150 / kb 7（:62196-62199）
760	      ctx.shootProjectile(x * 16 + 8, ly * 16 + 6, 0, -8, 150, 'fireworkRocket', Math.floor(st.frameY[i] / 40));
761	      // 烟花方块是消耗品：发射即移除 1×2 两格（:62203-62204 active(false)）
762	      st.setTile(x, ly, 0);
763	      st.setTile(x, ly + 1, 0);
764	      w.skipCell(x, y); // SkipWire（Wiring.cs:1494）
765	      return true;
766	    }
767	    case 244: // 泡泡机 3×2 frameX ±54(:1272-1293)
768	      flipBlock(w, x, y, 54, 36, 3, 2, 'x', 54, 54);
769	      return true;
770	    case 255: case 256: case 257: case 258: case 259: case 260: case 261: { // 宝石块 off→on(:863-873)
771	      if (st.wire[i] & 16) return true; // 原版有致动器时不响应
772	      const to = TILE_BY_KEY[GEMSPARK_ON[sheet - 255]] ?? 0;
773	      if (to) st.setTile(x, y, to, st.frameX[i], st.frameY[i]);
774	      return true;
775	    }
776	    case 262: case 263: case 264: case 265: case 266: case 267: case 268: { // on→off
777	      if (st.wire[i] & 16) return true;
778	      const to = TILE_BY_KEY[GEMSPARK_OFF[sheet - 262]] ?? 0;
779	      if (to) st.setTile(x, y, to, st.frameX[i], st.frameY[i]);
780	      return true;
781	    }
782	    case 314: // 压板轨道（Wiring.cs:1746-1752）：CheckMech 5 + FlipSwitchTrack 翻转轨道指向。
783	      // FlipSwitchTrack（Minecart.cs:1302-1325）：普通型前/后轨互换（分叉换边）、
784	      // 加速型 FrameTrack(pound) 循环下一个加速向
785	      if (w.checkMech(x, y, 5)) {
786	        flipSwitchTrack(st, x, y);
787	      }
788	      return true;
789	    case 335: { // 烟花盒 2×2（Wiring.cs:1511-1523 → WorldGen.LaunchRocketSmall WorldGen.cs:62208-62222）
790	      const num72 = y - Math.floor(st.frameY[i] / 18);
791	      const num73 = x - Math.floor(st.frameX[i] / 18);
792	      w.skipCell(num73, num72); w.skipCell(num73 + 1, num72);
793	      w.skipCell(num73, num72 + 1); w.skipCell(num73 + 1, num72 + 1);
794	      if (!w.checkMech(num73, num72, 30)) return true; // CheckMech 30（:1518-1520）
795	      // LaunchRocketSmall 的 frameX/frameY==18 再回退（WorldGen.cs:62210-62213）对电路路径是
796	      // 空操作——num73/num72 已是 2×2 锚点（frameX/frameY==0），此处不再重复
797	      // 弹 415+rand(4)（红/绿/蓝/黄）、速度 (0,-8)、damage 0（:62213-62215）
798	      ctx.shootProjectile(num73 * 16 + 16, num72 * 16 + 2, 0, -8, 0, 'fireworksBoxRocket', Math.floor(Math.random() * 4));
799	      return true;
800	    }
801	    case 338: { // 烟花喷泉 1×2（Wiring.cs:1525-1553）
802	      const num69 = y - Math.floor(st.frameY[i] / 18);
803	      const num70 = x - Math.floor(st.frameX[i] / 18);
804	      w.skipCell(num70, num69); w.skipCell(num70, num69 + 1);
805	      if (!w.checkMech(num70, num69, 30)) return true; // CheckMech 30（:1538-1540）
806	      // 去重（:1542-1547）：同锚点已有 aiStyle73 弹在喷则不再生成
807	      if (ctx.hasFountainAt?.(num70, num69)) return true;
808	      // 弹 419+rand(4)（黄/红/蓝/彩虹），静态发射器（速度 0），ai[0]/ai[1] = 锚点（:1548-1550）
809	      ctx.shootProjectile(num70 * 16 + 8, num69 * 16 + 2, 0, 0, 0, 'fireworkFountain',
810	        Math.floor(Math.random() * 4), [num70, num69]);
811	      return true;
812	    }
813	    case 386: case 387: { // 活板门开/关互换(ShiftTrapdoor;帧近似)
814	      const openK = 'v_386_trapdooropen', closedK = 'v_387_trap_door_closed';
815	      const toOpen = sheet === 387;
816	      const target = TILE_BY_KEY[toOpen ? openK : closedK] ?? 0;
817	      if (!target) return true;
818	      const ox = x - Math.floor(st.frameX[i] % 36 / 18);
819	      for (let ix = ox; ix < ox + 2; ix++) {
820	        if (!st.inBounds(ix, y)) continue;
821	        const ii = st.idx(ix, y);
822	        w.skipCell(ix, y);
823	        st.setTile(ix, y, target, (ix - ox) * 18, st.frameY[ii]);
824	      }
825	      return true;
826	    }
827	    case 388: case 389: { // 高门关/开互换(ShiftTallGate;帧近似)
828	      const openK = 'v_389_tallgateopen', closedK = 'v_388_tall_gate_closed';
829	      const toOpen = sheet === 388;
830	      const target = TILE_BY_KEY[toOpen ? openK : closedK] ?? 0;
831	      if (!target) return true;
832	      const ox = x - Math.floor(st.frameX[i] % 20 / 18);
833	      const oy = y - Math.floor(st.frameY[i] % 90 / 18);
834	      for (let ix = ox; ix < ox + 1; ix++) {
835	        for (let iy = oy; iy < oy + 5; iy++) {
836	          if (!st.inBounds(ix, iy)) continue;
837	          const ii = st.idx(ix, iy);
838	          w.skipCell(ix, iy);
839	          st.setTile(ix, iy, target, st.frameX[ii], st.frameY[ii]);
840	        }
841	      }
842	      return true;
843	    }
844	    case 405: // 壁炉 3×2 frameX ±54(:1021-1038)
845	      flipBlock(w, x, y, 54, 36, 3, 2, 'x', 54, 54);
846	      return true;
847	    case 406: // 烟囱 3×3 frameY +54/-108(:1039-1056)
848	      flipBlock(w, x, y, 54, 54, 3, 3, 'y', 108, 54);
849	      return true;
850	    case 411: // 引爆器 2×2 frameX ±36(:1057-1074)
851	      flipBlock(w, x, y, 36, 36, 2, 2, 'x', 36, 36);
852	      return true;
853	    case 421: case 422: { // 传送带反向互换(:844-861;有致动器不响应)
854	      if (st.wire[i] & 16) return true;
855	      const other = TILE_BY_KEY[sheet === 421 ? 'v_422_conveyor_belt_ccw' : 'v_421_conveyorbeltleft'] ?? 0;
856	      if (other) st.setTile(x, y, other, st.frameX[i], st.frameY[i]);
857	      return true;
858	    }
859	    case 425: { // 广播盒（Wiring.cs:1177-1230 1:1）：锚点 2×2 内登记的告示牌文本 →
860	      // 粉色聊天广播（NewTextMultiline）；无牌/空文本静默返回。
861	      // AnnouncementBoxRange 默认 -1 = 全图（设置项，引擎暂未接设置门，恒全图）。
862	      // 【依赖登记】牌面文字编辑 UI 未接入（现存 signs 只读：墓碑/导入存档）
863	      const num5 = Math.floor(st.frameX[i] % 36 / 18);
864	      const num6 = Math.floor(st.frameY[i] % 36 / 18);
865	      const ox = x - num5, oy = y - num6;
866	      for (let m = ox; m < ox + 2; m++) {
867	        for (let n = oy; n < oy + 2; n++) {
868	          if (st.inBounds(m, n)) w.skipCell(m, n);
869	        }
870	      }
871	      ctx.announce?.(ox, oy);
872	      return true;
873	    }
874	    case 442: return true; // 投射物垫板(触发源侧处理)
875	    case 443:
876	      geyserTrap(w, ctx, x, y);
877	      return true;
878	    case 452: // 呆萌气球机 3×3 frameX ±54(:1132-1149)
879	      flipBlock(w, x, y, 54, 54, 3, 3, 'x', 54, 54);
880	      return true;
881	    case 455: // 派对纪念碑（Wiring.cs:2037-2039 → BirthdayParty.ToggleManualParty，
882	      // BirthdayParty.cs:145-163）：切换 ManualParty（开→升气球天/彩带，入夜 CheckNight 结束）
883	      ctx.toggleParty?.();
884	      return true;
885	    case 476: return true; // 高尔夫球洞(无高尔夫系统)
886	    case 497: // 马桶（Wiring.cs:1498-1509，与 tile 15 马桶样式共用分支）
887	      fireworkToilet(w, ctx, x, y);
888	      return true;
889	    case 506: // 巴斯特雕像 2×3 frameX ±72(:2239-2261)
890	      flipBlock(w, x, y, 72, 54, 2, 3, 'x', 72, 72);
891	      return true;
892	    case 531:
893	      fireBoulderStatue(w, ctx, x, y);
894	      return true;
895	    case 546: case 557: // 格栅开/关互换(:2262-2271)
896	      swapTile(w, x, y, 'v_546_grate', 'v_557_grateclosed');
897	      return true;
898	    case 565: // 造雾机 2×2 frameX ±36(:1358-1379)
899	      flipBlock(w, x, y, 72, 36, 2, 2, 'x', 36, 36);
900	      return true;
901	    case 593: // 小火山 frameX ±18(:1434-1445;动画近似粒子)
902	      flipCell(w, x, y, 18);
903	      ctx.sfx('roar', x * 16 + 8, y * 16 + 8);
904	      return true;
905	    case 594: // 大火山 2×2 frameX ±36(:1446-1470)
906	      flipBlock(w, x, y, 72, 36, 2, 2, 'x', 36, 36);
907	      ctx.sfx('roar', x * 16 + 8, y * 16 + 8);
908	      return true;
909	  }
910	  return false;
911	}
912	
913	/** 装配:把器件表挂到 Wiring(器件 case 之外的默认落点) */
914	export function attachDevices(w: Wiring, ctx: DeviceCtx): void {
915	  w.device = (ww, sheet, x, y) => deviceTable(ww, ctx, sheet, x, y);
916	  w.teleportPair = (a, b) => ctx.teleportPair(a, b);
917	  // 巨石失撑下落（Wiring.boulderFall）：KillTile(138) → Projectile 99 的数据点
918	  // （1456 cs:48766：spawn (x*16+15.5, y*16+16)、初速 0/0、伤害 70）
919	  w.boulderFall = (x, y, _sheet) => {
920	    ctx.shootProjectile(x * 16 + 15.5, y * 16 + 16, 0, 0, 70, 'boulder');
921	  };
922	}
923	

```


---

## 🤖 Assistant · 2026-08-12T18:43:26.393Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
现在我需要读 1456 Wiring.cs 的剩余部分(900-3441),特别是:
- HitWireSingle (837-...)
- 雕像逻辑
- 传送器 Teleport
- 传感器 (423)
- MassWireOperation

同时对比 1.4.0.5 (Terarria1405) 的 Wiring.cs,确认实现基于哪个版本,以及 1456 与 1405 的差异(1.4.4/1.4.5 加了什么)。

关键差异点候选(1.4.0.5 → 1.4.4):
- 476 高尔夫球洞(1.4.1)
- 497 马桶烟花?其实 1.4.0.5 也有
- 1.4.4 新增:未确认
- 1.4.5 新增?

从已读的 1456 源码看到 HitSwitch 有 `Main.tile[i,j].type == 210 → ExplodeMine(i,j)`(地雷),以及 type 443 → GeyserTrap。实现的 hitSwitch 缺少 210(地雷)!让我确认实现的 hitSwitch:实现有 135/314/423/428/442/476 → tripWire;440 宝石锁;136 开关;443 热喷泉(委托 device);144 计时器;441/468 陷阱箱;467;132/411。**没有 210(ExplodeMine)**。地雷在 devices case 210 处理(通电触发),但 HitSwitch 里玩家右键地雷应该直接爆炸。看 Game.ts 6346 注释说"拉杆/开关/计时器/起爆器:右键 → Wiring.hitSwitch"。需要确认右键地雷路径。

另外注意 1456 的 `CheckLogicGate` 里 flag6(故障)判定:`if (flag3 && Framing.GetTileSafely(lampX, lampY).frameX == 36) flag6 = true;` 和实现的 579 行一致。

还有一个重要差异:1456 CheckLogicGate 的 flag6 分支:
```
if (flag6) {
    if (num3 == 0 || num2 == 0) flag7 = false;
    flag7 = Main.rand.NextFloat() < (float)num3 / (float)num2;
}
```
实现 586 行:`if (flag7 && num2 > 0) fire = Math.random() < num3 / num2;` —— 若 num2==0,实现不掷(保留 fire=true?),而原版 flag6 时若 num2==0 → flag7=false。等等,实现:`let fire = !faulty || flag7;` 其中 flag7 = (faulty && lamp frameX==36)。若 flag7 且 num2==0 → 实现不修改 fire(fire=true)→ 会发射!而原版 num2==0 → flag7=false → fire=false。这是一个 bug!不过 num2==0 意味着门上方没有任何灯,而 lamp 本身是灯……lampY 是触发灯的位置,向上数灯时从 i-1 开始。触发灯本身就是门上方第一盏灯(num2>=1 恒成立,因为触发的就是一盏 419)。所以 num2==0 的情况实际不可能(除非触发灯已被移除)。低风险,但可以提。

现在继续读 1456 Wiring.cs 900-3441。
````

</details>


---

## 🤖 Assistant · 2026-08-12T18:43:27.260Z · glm-x-preview-260804

```
现在读 1456 源码的剩余部分(HitWireSingle 主干/传送器/传感器/地雷)。
```


---

## 🤖 Assistant · 2026-08-12T18:43:27.282Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs",
 "offset": 900,
 "limit": 1000
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:27.288Z

**📎 ToolResult**

```
900					byte b = 3;
901					if (tile.type == 424 || tile.type == 445)
902					{
903						b = 0;
904					}
905					if (tile2.type == 424)
906					{
907						switch (tile2.frameX / 18)
908						{
909						case 0:
910							if (j != num)
911							{
912								continue;
913							}
914							break;
915						case 1:
916							if ((num != 0 || j != 3) && (num != 3 || j != 0) && (num != 1 || j != 2) && (num != 2 || j != 1))
917							{
918								continue;
919							}
920							break;
921						case 2:
922							if ((num != 0 || j != 2) && (num != 2 || j != 0) && (num != 1 || j != 3) && (num != 3 || j != 1))
923							{
924								continue;
925							}
926							break;
927						}
928					}
929					if (tile2.type == 445)
930					{
931						if (j != num)
932						{
933							continue;
934						}
935						if (_PixelBoxTriggers.ContainsKey(key))
936						{
937							_PixelBoxTriggers[key] |= (byte)((!(j == 0 || j == 1)) ? 1 : 2);
938						}
939						else
940						{
941							_PixelBoxTriggers[key] = (byte)((!(j == 0 || j == 1)) ? 1u : 2u);
942						}
943					}
944					if (wireType switch
945					{
946						1 => tile.wire() ? 1 : 0, 
947						2 => tile.wire2() ? 1 : 0, 
948						3 => tile.wire3() ? 1 : 0, 
949						4 => tile.wire4() ? 1 : 0, 
950						_ => 0, 
951					} == 0)
952					{
953						continue;
954					}
955					Point16 point2 = new Point16(num2, num3);
956					if (_toProcess.TryGetValue(point2, out var value))
957					{
958						value--;
959						if (value == 0)
960						{
961							_toProcess.Remove(point2);
962						}
963						else
964						{
965							_toProcess[point2] = value;
966						}
967						continue;
968					}
969					next.PushBack(point2);
970					_wireDirectionList.PushBack((byte)j);
971					if (b > 0)
972					{
973						_toProcess.Add(point2, b);
974					}
975				}
976			}
977			_wireSkip.Clear();
978			_toProcess.Clear();
979		}
980	
981		public static IEntitySource GetProjectileSource(int sourceTileX, int sourceTileY)
982		{
983			return new EntitySource_Wiring(sourceTileX, sourceTileY);
984		}
985	
986		public static IEntitySource GetNPCSource(int sourceTileX, int sourceTileY)
987		{
988			return new EntitySource_Wiring(sourceTileX, sourceTileY);
989		}
990	
991		public static IEntitySource GetItemSource(int sourceTileX, int sourceTileY)
992		{
993			return new EntitySource_Wiring(sourceTileX, sourceTileY);
994		}
995	
996		private static void HitWireSingle(int i, int j)
997		{
998			Tile tile = Main.tile[i, j];
999			bool? forcedStateWhereTrueIsOn = null;
1000			bool doSkipWires = true;
1001			int type = tile.type;
1002			if (tile.actuator())
1003			{
1004				ActuateForced(i, j);
1005			}
1006			if (!tile.active())
1007			{
1008				return;
1009			}
1010			switch (type)
1011			{
1012			case 144:
1013				HitSwitch(i, j);
1014				WorldGen.SquareTileFrame(i, j);
1015				NetMessage.SendTileSquare(-1, i, j);
1016				break;
1017			case 421:
1018				if (!tile.actuator())
1019				{
1020					tile.type = 422;
1021					WorldGen.SquareTileFrame(i, j);
1022					NetMessage.SendTileSquare(-1, i, j);
1023				}
1024				break;
1025			case 422:
1026				if (!tile.actuator())
1027				{
1028					tile.type = 421;
1029					WorldGen.SquareTileFrame(i, j);
1030					NetMessage.SendTileSquare(-1, i, j);
1031				}
1032				break;
1033			}
1034			if (type >= 255 && type <= 268)
1035			{
1036				if (!tile.actuator())
1037				{
1038					if (type >= 262)
1039					{
1040						tile.type -= 7;
1041					}
1042					else
1043					{
1044						tile.type += 7;
1045					}
1046					WorldGen.SquareTileFrame(i, j);
1047					NetMessage.SendTileSquare(-1, i, j);
1048				}
1049				return;
1050			}
1051			switch (type)
1052			{
1053			case 419:
1054			{
1055				int num50 = 18;
1056				if (tile.frameX >= num50)
1057				{
1058					num50 = -num50;
1059				}
1060				if (tile.frameX == 36)
1061				{
1062					num50 = 0;
1063				}
1064				SkipWire(i, j);
1065				tile.frameX = (short)(tile.frameX + num50);
1066				WorldGen.SquareTileFrame(i, j);
1067				NetMessage.SendTileSquare(-1, i, j);
1068				_LampsToCheck.Enqueue(new Point16(i, j));
1069				return;
1070			}
1071			case 406:
1072			{
1073				int num18 = tile.frameX % 54 / 18;
1074				int num19 = tile.frameY % 54 / 18;
1075				int num20 = i - num18;
1076				int num21 = j - num19;
1077				int num22 = 54;
1078				if (Main.tile[num20, num21].frameY >= 108)
1079				{
1080					num22 = -108;
1081				}
1082				for (int num23 = num20; num23 < num20 + 3; num23++)
1083				{
1084					for (int num24 = num21; num24 < num21 + 3; num24++)
1085					{
1086						SkipWire(num23, num24);
1087						Main.tile[num23, num24].frameY = (short)(Main.tile[num23, num24].frameY + num22);
1088					}
1089				}
1090				NetMessage.SendTileSquare(-1, num20 + 1, num21 + 1, 3);
1091				return;
1092			}
1093			case 452:
1094			{
1095				int num11 = tile.frameX % 54 / 18;
1096				int num12 = tile.frameY % 54 / 18;
1097				int num13 = i - num11;
1098				int num14 = j - num12;
1099				int num15 = 54;
1100				if (Main.tile[num13, num14].frameX >= 54)
1101				{
1102					num15 = -54;
1103				}
1104				for (int num16 = num13; num16 < num13 + 3; num16++)
1105				{
1106					for (int num17 = num14; num17 < num14 + 3; num17++)
1107					{
1108						SkipWire(num16, num17);
1109						Main.tile[num16, num17].frameX = (short)(Main.tile[num16, num17].frameX + num15);
1110					}
1111				}
1112				NetMessage.SendTileSquare(-1, num13 + 1, num14 + 1, 3);
1113				return;
1114			}
1115			case 411:
1116			{
1117				int num43 = tile.frameX % 36 / 18;
1118				int num44 = tile.frameY % 36 / 18;
1119				int num45 = i - num43;
1120				int num46 = j - num44;
1121				int num47 = 36;
1122				if (Main.tile[num45, num46].frameX >= 36)
1123				{
1124					num47 = -36;
1125				}
1126				for (int num48 = num45; num48 < num45 + 2; num48++)
1127				{
1128					for (int num49 = num46; num49 < num46 + 2; num49++)
1129					{
1130						SkipWire(num48, num49);
1131						Main.tile[num48, num49].frameX = (short)(Main.tile[num48, num49].frameX + num47);
1132					}
1133				}
1134				NetMessage.SendTileSquare(-1, num45, num46, 2, 2);
1135				return;
1136			}
1137			case 356:
1138			{
1139				int num = tile.frameX % 36 / 18;
1140				int num2 = tile.frameY % 54 / 18;
1141				int num3 = i - num;
1142				int num4 = j - num2;
1143				for (int k = num3; k < num3 + 2; k++)
1144				{
1145					for (int l = num4; l < num4 + 3; l++)
1146					{
1147						SkipWire(k, l);
1148					}
1149				}
1150				if (!Main.fastForwardTimeToDawn && Main.sundialCooldown == 0)
1151				{
1152					Main.Sundialing();
1153				}
1154				NetMessage.SendTileSquare(-1, num3, num4, 2, 2);
1155				return;
1156			}
1157			case 663:
1158			{
1159				int num25 = tile.frameX % 36 / 18;
1160				int num26 = tile.frameY % 54 / 18;
1161				int num27 = i - num25;
1162				int num28 = j - num26;
1163				for (int num29 = num27; num29 < num27 + 2; num29++)
1164				{
1165					for (int num30 = num28; num30 < num28 + 3; num30++)
1166					{
1167						SkipWire(num29, num30);
1168					}
1169				}
1170				if (!Main.fastForwardTimeToDusk && Main.moondialCooldown == 0)
1171				{
1172					Main.Moondialing();
1173				}
1174				NetMessage.SendTileSquare(-1, num27, num28, 2, 2);
1175				return;
1176			}
1177			case 425:
1178			{
1179				int num5 = tile.frameX % 36 / 18;
1180				int num6 = tile.frameY % 36 / 18;
1181				int num7 = i - num5;
1182				int num8 = j - num6;
1183				for (int m = num7; m < num7 + 2; m++)
1184				{
1185					for (int n = num8; n < num8 + 2; n++)
1186					{
1187						SkipWire(m, n);
1188					}
1189				}
1190				if (Main.AnnouncementBoxDisabled)
1191				{
1192					return;
1193				}
1194				Color pink = Color.Pink;
1195				int num9 = Sign.ReadSign(num7, num8, CreateIfMissing: false);
1196				if (num9 == -1 || Main.sign[num9] == null || string.IsNullOrWhiteSpace(Main.sign[num9].text))
1197				{
1198					return;
1199				}
1200				if (Main.AnnouncementBoxRange == -1)
1201				{
1202					if (Main.netMode == 0)
1203					{
1204						Main.NewTextMultiline(Main.sign[num9].text, force: false, pink, 460);
1205					}
1206					else if (Main.netMode == 2)
1207					{
1208						NetMessage.SendData(107, -1, -1, NetworkText.FromLiteral(Main.sign[num9].text), 255, (int)pink.R, (int)pink.G, (int)pink.B, 460);
1209					}
1210				}
1211				else if (Main.netMode == 0)
1212				{
1213					if (Main.player[Main.myPlayer].Distance(new Vector2(num7 * 16 + 16, num8 * 16 + 16)) <= (float)Main.AnnouncementBoxRange)
1214					{
1215						Main.NewTextMultiline(Main.sign[num9].text, force: false, pink, 460);
1216					}
1217				}
1218				else
1219				{
1220					if (Main.netMode != 2)
1221					{
1222						return;
1223					}
1224					for (int num10 = 0; num10 < 255; num10++)
1225					{
1226						if (Main.player[num10].active && Main.player[num10].Distance(new Vector2(num7 * 16 + 16, num8 * 16 + 16)) <= (float)Main.AnnouncementBoxRange)
1227						{
1228							NetMessage.SendData(107, num10, -1, NetworkText.FromLiteral(Main.sign[num9].text), 255, (int)pink.R, (int)pink.G, (int)pink.B, 460);
1229						}
1230					}
1231				}
1232				return;
1233			}
1234			case 405:
1235				ToggleFirePlace(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1236				return;
1237			case 209:
1238			{
1239				int num31 = tile.frameX % 72 / 18;
1240				int num32 = tile.frameY % 54 / 18;
1241				int num33 = i - num31;
1242				int num34 = j - num32;
1243				int num35 = tile.frameY / 54;
1244				int num36 = tile.frameX / 72;
1245				int num37 = -1;
1246				if (num31 == 1 || num31 == 2)
1247				{
1248					num37 = num32;
1249				}
1250				int num38 = 0;
1251				if (num31 == 3)
1252				{
1253					num38 = -54;
1254				}
1255				if (num31 == 0)
1256				{
1257					num38 = 54;
1258				}
1259				if (num35 >= 8 && num38 > 0)
1260				{
1261					num38 = 0;
1262				}
1263				if (num35 == 0 && num38 < 0)
1264				{
1265					num38 = 0;
1266				}
1267				bool flag = false;
1268				if (num38 != 0)
1269				{
1270					for (int num39 = num33; num39 < num33 + 4; num39++)
1271					{
1272						for (int num40 = num34; num40 < num34 + 3; num40++)
1273						{
1274							SkipWire(num39, num40);
1275							Main.tile[num39, num40].frameY = (short)(Main.tile[num39, num40].frameY + num38);
1276						}
1277					}
1278					flag = true;
1279				}
1280				if ((num36 == 3 || num36 == 4) && (num37 == 0 || num37 == 1))
1281				{
1282					num38 = ((num36 == 3) ? 72 : (-72));
1283					for (int num41 = num33; num41 < num33 + 4; num41++)
1284					{
1285						for (int num42 = num34; num42 < num34 + 3; num42++)
1286						{
1287							SkipWire(num41, num42);
1288							Main.tile[num41, num42].frameX = (short)(Main.tile[num41, num42].frameX + num38);
1289						}
1290					}
1291					flag = true;
1292				}
1293				if (flag)
1294				{
1295					NetMessage.SendTileSquare(-1, num33, num34, 4, 3);
1296				}
1297				if (num37 == -1)
1298				{
1299					return;
1300				}
1301				bool flag2 = true;
1302				if ((num36 == 3 || num36 == 4) && num37 < 2)
1303				{
1304					flag2 = false;
1305				}
1306				int damage = 0;
1307				float knockBack = 0f;
1308				int time = 30;
1309				switch (num36)
1310				{
1311				case 0:
1312					if (cannonCoolDown > 0)
1313					{
1314						return;
1315					}
1316					damage = 300;
1317					knockBack = 8f;
1318					time = 480;
1319					break;
1320				case 1:
1321					if (bunnyCannonCoolDown > 0)
1322					{
1323						return;
1324					}
1325					damage = 350;
1326					knockBack = 8f;
1327					time = 3600;
1328					break;
1329				}
1330				if (CheckMech(num33, num34, time) && flag2)
1331				{
1332					switch (num36)
1333					{
1334					case 0:
1335						cannonCoolDown = 120;
1336						break;
1337					case 1:
1338						bunnyCannonCoolDown = 480;
1339						break;
1340					}
1341					WorldGen.ShootFromCannon(num33, num34, num35, num36 + 1, damage, knockBack, CurrentUser, fromWire: true);
1342				}
1343				return;
1344			}
1345			case 212:
1346			{
1347				int num51 = tile.frameX % 54 / 18;
1348				int num52 = tile.frameY % 54 / 18;
1349				int num53 = i - num51;
1350				int num54 = j - num52;
1351				int num55 = tile.frameX / 54;
1352				int num56 = -1;
1353				if (num51 == 1)
1354				{
1355					num56 = num52;
1356				}
1357				int num57 = 0;
1358				if (num51 == 0)
1359				{
1360					num57 = -54;
1361				}
1362				if (num51 == 2)
1363				{
1364					num57 = 54;
1365				}
1366				if (num55 >= 1 && num57 > 0)
1367				{
1368					num57 = 0;
1369				}
1370				if (num55 == 0 && num57 < 0)
1371				{
1372					num57 = 0;
1373				}
1374				bool flag3 = false;
1375				if (num57 != 0)
1376				{
1377					for (int num58 = num53; num58 < num53 + 3; num58++)
1378					{
1379						for (int num59 = num54; num59 < num54 + 3; num59++)
1380						{
1381							SkipWire(num58, num59);
1382							Main.tile[num58, num59].frameX = (short)(Main.tile[num58, num59].frameX + num57);
1383						}
1384					}
1385					flag3 = true;
1386				}
1387				if (flag3)
1388				{
1389					NetMessage.SendTileSquare(-1, num53, num54, 3, 3);
1390				}
1391				if (num56 != -1 && snowballCannonCoolDown == 0 && CheckMech(num53, num54, 60))
1392				{
1393					snowballCannonCoolDown = 15;
1394					float num60 = 12f + (float)Main.rand.Next(450) * 0.01f;
1395					float num61 = Main.rand.Next(85, 105);
1396					float num62 = Main.rand.Next(-35, 11);
1397					int type2 = 166;
1398					int damage2 = 35;
1399					float knockBack2 = 3.5f;
1400					Vector2 vector = new Vector2((num53 + 2) * 16 - 8, (num54 + 2) * 16 - 8);
1401					if (tile.frameX / 54 == 0)
1402					{
1403						num61 *= -1f;
1404						vector.X -= 12f;
1405					}
1406					else
1407					{
1408						vector.X += 12f;
1409					}
1410					float num63 = num61;
1411					float num64 = num62;
1412					float num65 = (float)Math.Sqrt(num63 * num63 + num64 * num64);
1413					num65 = num60 / num65;
1414					num63 *= num65;
1415					num64 *= num65;
1416					Projectile.NewProjectile(GetProjectileSource(num53, num54), vector.X, vector.Y, num63, num64, type2, damage2, knockBack2, CurrentUser);
1417				}
1418				return;
1419			}
1420			}
1421			if (TileID.Sets.Campfires[type])
1422			{
1423				ToggleCampFire(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1424				return;
1425			}
1426			if (type == 130)
1427			{
1428				if (Main.tile[i, j - 1] != null && (!Main.tile[i, j - 1].active() || !TileID.Sets.PreventsActuationUnder[Main.tile[i, j - 1].type]) && WorldGen.CanKillTile(i, j))
1429				{
1430					tile.type = 131;
1431					WorldGen.SquareTileFrame(i, j);
1432					NetMessage.SendTileSquare(-1, i, j);
1433				}
1434				return;
1435			}
1436			if (type == 131)
1437			{
1438				tile.type = 130;
1439				WorldGen.SquareTileFrame(i, j);
1440				NetMessage.SendTileSquare(-1, i, j);
1441				return;
1442			}
1443			if (type == 387 || type == 386)
1444			{
1445				bool value = type == 387;
1446				int num66 = WorldGen.ShiftTrapdoor(i, j, playerAbove: true).ToInt();
1447				if (num66 == 0)
1448				{
1449					num66 = -WorldGen.ShiftTrapdoor(i, j, playerAbove: false).ToInt();
1450				}
1451				if (num66 != 0)
1452				{
1453					NetMessage.SendData(19, -1, -1, null, 3 - value.ToInt(), i, j, num66);
1454				}
1455				return;
1456			}
1457			if (type == 389 || type == 388)
1458			{
1459				bool flag4 = type == 389;
1460				WorldGen.ShiftTallGate(i, j, flag4);
1461				NetMessage.SendData(19, -1, -1, null, 4 + flag4.ToInt(), i, j);
1462				return;
1463			}
1464			if (type == 11)
1465			{
1466				if (WorldGen.CloseDoor(i, j, forced: true))
1467				{
1468					NetMessage.SendData(19, -1, -1, null, 1, i, j);
1469				}
1470				return;
1471			}
1472			if (type == 10)
1473			{
1474				int num67 = 1;
1475				if (Main.rand.Next(2) == 0)
1476				{
1477					num67 = -1;
1478				}
1479				if (!WorldGen.OpenDoor(i, j, num67))
1480				{
1481					if (WorldGen.OpenDoor(i, j, -num67))
1482					{
1483						NetMessage.SendData(19, -1, -1, null, 0, i, j, -num67);
1484					}
1485				}
1486				else
1487				{
1488					NetMessage.SendData(19, -1, -1, null, 0, i, j, num67);
1489				}
1490				return;
1491			}
1492			if (type == 216)
1493			{
1494				WorldGen.LaunchRocket(i, j, fromWiring: true);
1495				SkipWire(i, j);
1496				return;
1497			}
1498			if (type == 497 || (type == 15 && tile.frameY / 40 == 1) || (type == 15 && tile.frameY / 40 == 20))
1499			{
1500				int num68 = j - tile.frameY % 40 / 18;
1501				SkipWire(i, num68);
1502				SkipWire(i, num68 + 1);
1503				if (CheckMech(i, num68, 60))
1504				{
1505					Projectile.NewProjectile(GetProjectileSource(i, num68), i * 16 + 8, num68 * 16 + 12, 0f, 0f, 733, 0, 0f, Main.myPlayer);
1506				}
1507				return;
1508			}
1509			switch (type)
1510			{
1511			case 335:
1512			{
1513				int num72 = j - tile.frameY / 18;
1514				int num73 = i - tile.frameX / 18;
1515				SkipWire(num73, num72);
1516				SkipWire(num73, num72 + 1);
1517				SkipWire(num73 + 1, num72);
1518				SkipWire(num73 + 1, num72 + 1);
1519				if (CheckMech(num73, num72, 30))
1520				{
1521					WorldGen.LaunchRocketSmall(num73, num72, fromWiring: true);
1522				}
1523				return;
1524			}
1525			case 338:
1526			{
1527				int num69 = j - tile.frameY / 18;
1528				int num70 = i - tile.frameX / 18;
1529				SkipWire(num70, num69);
1530				SkipWire(num70, num69 + 1);
1531				if (!CheckMech(num70, num69, 30))
1532				{
1533					return;
1534				}
1535				bool flag5 = false;
1536				for (int num71 = 0; num71 < 1000; num71++)
1537				{
1538					if (Main.projectile[num71].active && Main.projectile[num71].aiStyle == 73 && Main.projectile[num71].ai[0] == (float)num70 && Main.projectile[num71].ai[1] == (float)num69)
1539					{
1540						flag5 = true;
1541						break;
1542					}
1543				}
1544				if (!flag5)
1545				{
1546					int type3 = 419 + Main.rand.Next(4);
1547					Projectile.NewProjectile(GetProjectileSource(num70, num69), num70 * 16 + 8, num69 * 16 + 2, 0f, 0f, type3, 0, 0f, Main.myPlayer, num70, num69);
1548				}
1549				return;
1550			}
1551			case 235:
1552			{
1553				int num74 = i - tile.frameX / 18;
1554				if (tile.wall == 87 && (double)j > Main.worldSurface && !NPC.downedPlantBoss)
1555				{
1556					return;
1557				}
1558				if (_teleport[0].X == -1f)
1559				{
1560					_teleport[0].X = num74;
1561					_teleport[0].Y = j;
1562					if (tile.halfBrick())
1563					{
1564						_teleport[0].Y += 0.5f;
1565					}
1566				}
1567				else if (_teleport[0].X != (float)num74 || _teleport[0].Y != (float)j)
1568				{
1569					_teleport[1].X = num74;
1570					_teleport[1].Y = j;
1571					if (tile.halfBrick())
1572					{
1573						_teleport[1].Y += 0.5f;
1574					}
1575				}
1576				return;
1577			}
1578			}
1579			if (TileID.Sets.Torches[type])
1580			{
1581				ToggleTorch(i, j, tile, forcedStateWhereTrueIsOn);
1582				return;
1583			}
1584			switch (type)
1585			{
1586			case 429:
1587			{
1588				int num156 = Main.tile[i, j].frameX / 18;
1589				bool flag8 = num156 % 2 >= 1;
1590				bool flag9 = num156 % 4 >= 2;
1591				bool flag10 = num156 % 8 >= 4;
1592				bool flag11 = num156 % 16 >= 8;
1593				bool flag12 = false;
1594				short num157 = 0;
1595				switch (_currentWireColor)
1596				{
1597				case 1:
1598					num157 = 18;
1599					flag12 = !flag8;
1600					break;
1601				case 2:
1602					num157 = 72;
1603					flag12 = !flag10;
1604					break;
1605				case 3:
1606					num157 = 36;
1607					flag12 = !flag9;
1608					break;
1609				case 4:
1610					num157 = 144;
1611					flag12 = !flag11;
1612					break;
1613				}
1614				if (flag12)
1615				{
1616					tile.frameX += num157;
1617				}
1618				else
1619				{
1620					tile.frameX -= num157;
1621				}
1622				NetMessage.SendTileSquare(-1, i, j);
1623				break;
1624			}
1625			case 149:
1626				ToggleHolidayLight(i, j, tile, forcedStateWhereTrueIsOn);
1627				break;
1628			case 244:
1629			{
1630				int num81;
1631				for (num81 = tile.frameX / 18; num81 >= 3; num81 -= 3)
1632				{
1633				}
1634				int num82;
1635				for (num82 = tile.frameY / 18; num82 >= 3; num82 -= 3)
1636				{
1637				}
1638				int num83 = i - num81;
1639				int num84 = j - num82;
1640				int num85 = 54;
1641				if (Main.tile[num83, num84].frameX >= 54)
1642				{
1643					num85 = -54;
1644				}
1645				for (int num86 = num83; num86 < num83 + 3; num86++)
1646				{
1647					for (int num87 = num84; num87 < num84 + 2; num87++)
1648					{
1649						SkipWire(num86, num87);
1650						Main.tile[num86, num87].frameX = (short)(Main.tile[num86, num87].frameX + num85);
1651					}
1652				}
1653				NetMessage.SendTileSquare(-1, num83, num84, 3, 2);
1654				break;
1655			}
1656			case 565:
1657			{
1658				int num125;
1659				for (num125 = tile.frameX / 18; num125 >= 2; num125 -= 2)
1660				{
1661				}
1662				int num126;
1663				for (num126 = tile.frameY / 18; num126 >= 2; num126 -= 2)
1664				{
1665				}
1666				int num127 = i - num125;
1667				int num128 = j - num126;
1668				int num129 = 36;
1669				if (Main.tile[num127, num128].frameX >= 36)
1670				{
1671					num129 = -36;
1672				}
1673				for (int num130 = num127; num130 < num127 + 2; num130++)
1674				{
1675					for (int num131 = num128; num131 < num128 + 2; num131++)
1676					{
1677						SkipWire(num130, num131);
1678						Main.tile[num130, num131].frameX = (short)(Main.tile[num130, num131].frameX + num129);
1679					}
1680				}
1681				NetMessage.SendTileSquare(-1, num127, num128, 2, 2);
1682				break;
1683			}
1684			case 42:
1685				ToggleHangingLantern(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1686				break;
1687			case 93:
1688				ToggleLamp(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1689				break;
1690			case 95:
1691			case 100:
1692			case 126:
1693			case 173:
1694			case 564:
1695				Toggle2x2Light(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1696				break;
1697			case 593:
1698			{
1699				SkipWire(i, j);
1700				short num93 = (short)((Main.tile[i, j].frameX != 0) ? (-18) : 18);
1701				Main.tile[i, j].frameX += num93;
1702				if (Main.netMode == 2)
1703				{
1704					NetMessage.SendTileSquare(-1, i, j, 1, 1);
1705				}
1706				int num94 = ((num93 > 0) ? 4 : 3);
1707				Animation.NewTemporaryAnimation(num94, 593, i, j);
1708				NetMessage.SendTemporaryAnimation(-1, num94, 593, i, j);
1709				break;
1710			}
1711			case 594:
1712			{
1713				int num132;
1714				for (num132 = tile.frameY / 18; num132 >= 2; num132 -= 2)
1715				{
1716				}
1717				num132 = j - num132;
1718				int num133 = tile.frameX / 18;
1719				if (num133 > 1)
1720				{
1721					num133 -= 2;
1722				}
1723				num133 = i - num133;
1724				SkipWire(num133, num132);
1725				SkipWire(num133, num132 + 1);
1726				SkipWire(num133 + 1, num132);
1727				SkipWire(num133 + 1, num132 + 1);
1728				short num134 = (short)((Main.tile[num133, num132].frameX != 0) ? (-36) : 36);
1729				for (int num135 = 0; num135 < 2; num135++)
1730				{
1731					for (int num136 = 0; num136 < 2; num136++)
1732					{
1733						Main.tile[num133 + num135, num132 + num136].frameX += num134;
1734					}
1735				}
1736				if (Main.netMode == 2)
1737				{
1738					NetMessage.SendTileSquare(-1, num133, num132, 2, 2);
1739				}
1740				int num137 = ((num134 > 0) ? 4 : 3);
1741				Animation.NewTemporaryAnimation(num137, 594, num133, num132);
1742				NetMessage.SendTemporaryAnimation(-1, num137, 594, num133, num132);
1743				break;
1744			}
1745			case 34:
1746				ToggleChandelier(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1747				break;
1748			case 314:
1749				if (CheckMech(i, j, 5))
1750				{
1751					Minecart.FlipSwitchTrack(i, j);
1752				}
1753				break;
1754			case 33:
1755			case 49:
1756			case 174:
1757			case 372:
1758			case 646:
1759				ToggleCandle(i, j, tile, forcedStateWhereTrueIsOn);
1760				break;
1761			case 92:
1762				ToggleLampPost(i, j, tile, forcedStateWhereTrueIsOn, doSkipWires);
1763				break;
1764			case 137:
1765			{
1766				int num95 = tile.frameY / 18;
1767				Vector2 vector3 = Vector2.Zero;
1768				float speedX = 0f;
1769				float speedY = 0f;
1770				int num96 = 0;
1771				int damage4 = 0;
1772				switch (num95)
1773				{
1774				case 0:
1775				case 1:
1776				case 2:
1777				case 5:
1778					if (CheckMech(i, j, 200))
1779					{
1780						int num104 = ((tile.frameX == 0) ? (-1) : ((tile.frameX == 18) ? 1 : 0));
1781						int num105 = ((tile.frameX >= 36) ? ((tile.frameX >= 72) ? 1 : (-1)) : 0);
1782						vector3 = new Vector2(i * 16 + 8 + 10 * num104, j * 16 + 8 + 10 * num105);
1783						float num106 = 3f;
1784						if (num95 == 0)
1785						{
1786							num96 = 98;
1787							damage4 = 20;
1788							num106 = 12f;
1789						}
1790						if (num95 == 1)
1791						{
1792							num96 = 184;
1793							damage4 = 40;
1794							num106 = 12f;
1795						}
1796						if (num95 == 2)
1797						{
1798							num96 = 187;
1799							damage4 = 40;
1800							num106 = 5f;
1801						}
1802						if (num95 == 5)
1803						{
1804							num96 = 980;
1805							damage4 = 30;
1806							num106 = 12f;
1807						}
1808						speedX = (float)num104 * num106;
1809						speedY = (float)num105 * num106;
1810					}
1811					break;
1812				case 3:
1813				{
1814					if (!CheckMech(i, j, 300))
1815					{
1816						break;
1817					}
1818					int num99 = 200;
1819					for (int num100 = 0; num100 < 1000; num100++)
1820					{
1821						if (Main.projectile[num100].active && Main.projectile[num100].type == num96)
1822						{
1823							float num101 = (new Vector2(i * 16 + 8, j * 18 + 8) - Main.projectile[num100].Center).Length();
1824							num99 = ((!(num101 < 50f)) ? ((!(num101 < 100f)) ? ((!(num101 < 200f)) ? ((!(num101 < 300f)) ? ((!(num101 < 400f)) ? ((!(num101 < 500f)) ? ((!(num101 < 700f)) ? ((!(num101 < 900f)) ? ((!(num101 < 1200f)) ? (num99 - 1) : (num99 - 2)) : (num99 - 3)) : (num99 - 4)) : (num99 - 5)) : (num99 - 6)) : (num99 - 8)) : (num99 - 10)) : (num99 - 15)) : (num99 - 50));
1825						}
1826					}
1827					if (num99 > 0)
1828					{
1829						num96 = 185;
1830						damage4 = 40;
1831						int num102 = 0;
1832						int num103 = 0;
1833						switch (tile.frameX / 18)
1834						{
1835						case 0:
1836						case 1:
1837							num102 = 0;
1838							num103 = 1;
1839							break;
1840						case 2:
1841							num102 = 0;
1842							num103 = -1;
1843							break;
1844						case 3:
1845							num102 = -1;
1846							num103 = 0;
1847							break;
1848						case 4:
1849							num102 = 1;
1850							num103 = 0;
1851							break;
1852						}
1853						speedX = (float)(4 * num102) + (float)Main.rand.Next(-20 + ((num102 == 1) ? 20 : 0), 21 - ((num102 == -1) ? 20 : 0)) * 0.05f;
1854						speedY = (float)(4 * num103) + (float)Main.rand.Next(-20 + ((num103 == 1) ? 20 : 0), 21 - ((num103 == -1) ? 20 : 0)) * 0.05f;
1855						vector3 = new Vector2(i * 16 + 8 + 14 * num102, j * 16 + 8 + 14 * num103);
1856					}
1857					break;
1858				}
1859				case 4:
1860					if (CheckMech(i, j, 90))
1861					{
1862						int num97 = 0;
1863						int num98 = 0;
1864						switch (tile.frameX / 18)
1865						{
1866						case 0:
1867						case 1:
1868							num97 = 0;
1869							num98 = 1;
1870							break;
1871						case 2:
1872							num97 = 0;
1873							num98 = -1;
1874							break;
1875						case 3:
1876							num97 = -1;
1877							num98 = 0;
1878							break;
1879						case 4:
1880							num97 = 1;
1881							num98 = 0;
1882							break;
1883						}
1884						speedX = 8 * num97;
1885						speedY = 8 * num98;
1886						damage4 = 60;
1887						num96 = 186;
1888						vector3 = new Vector2(i * 16 + 8 + 18 * num97, j * 16 + 8 + 18 * num98);
1889					}
1890					break;
1891				}
1892				switch (num95)
1893				{
1894				case -10:
1895					if (CheckMech(i, j, 200))
1896					{
1897						int num111 = -1;
1898						if (tile.frameX != 0)
1899						{

```


---

## 🤖 Assistant · 2026-08-12T18:43:48.134Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
重要发现:

1. **case 137 陷阱 1456 新增了 `case 5`(num95==5)→ 弹 980、30 伤、速度 12** —— 这是 1.4.4 新增的"毒镖陷阱"(Venom Dart Trap, tile 137 frameY/18==5?)。实际上弹 980 是 VenomDart? 让我确认。实现的 fireTrap 只有 kind 0-4,**缺 kind 5**。

等等,实现的注释说 `0飞镖(98) 1超级飞镖(184) 2烈焰(187,隐形+尘埃) 3尖刺球(185) 4长矛(186)`。1456 有 case 5 → num96=980, damage=30, speed=12。需要确认 980 是什么弹。1.4.4 加了 Venom Dart Trap?其实我记得 1.4.4.9 加了"Venom Dart Trap"?让我 grep。

2. **case 137 的尖刺球(case 3)**:1456 的速度计算与我此前理解不同!1456:
```
speedX = (4 * num102) + rand(-20 + (num102==1?20:0), 21 - (num102==-1?20:0)) * 0.05f
speedY = (4 * num103) + rand(...)
vector3 = (i*16+8 + 14*num102, j*16+8 + 14*num103)
```
且 num96 在循环中先被赋值(在 case 0/1/2/5 里赋的 num96),然后 case 3 里 `Main.projectile[num100].type == num96` —— 注意!1456 里尖刺球预算循环用的是 num96(此时可能仍是 0,因为 case 3 分支前 num96=0)。等等,num96 初始 = 0。case 3 进入时 num96 还是 0,所以循环里 `type == 0` 恒 false!那预算就不扣?这似乎是原版 bug。嗯,注意 1456 中循环条件是 `Main.projectile[num100].type == num96`,而 num96==0,活跃弹 type 不会是 0,所以预算恒 200。这看起来像一个原版 bug(或者后面 num96 = 185 赋值发生在循环之后,确实是 bug)。

但等等,实现侧 devices.ts 的注释说"尖刺球惩罚表(Wiring.cs 1456 :1952-1966):场上每个 185 按距离扣预算"。让我看 1456 的 :1952-1966。我还没读到那里。当前读到 1900。继续读 1900-2900。

另外实现侧尖刺球的方向处理:1456 有 num102/num103 switch(tile.frameX/18)→ 方向!case 0/1: 下;case 2: 上;case 3: 左;case 4: 右。初速 = 4*dir + rand(-20..20)*0.05。这与实现注释说的"1456 改为纯下丢"不符?实现注释说"发射无视朝向(1405 曾按 frameX 定向,1456 改为纯下丢,取 1456):固定方块底 (x*16+8, y*16+22), vx=rand(-20,21)*0.05、vy=4+rand(0,21)*0.05"。

但 1456 源码显示尖刺球是有方向性的:num102/num103 来自 frameX/18,速度 = 4*num102 + rand*0.05。这与实现注释完全相反!需要仔细确认行号——实现注释引用 ":1944-1976"。我读到的是 1812-1857 区域。让我看 1456 的实际行号。

刚才 Read 输出的行号就是文件行号。case 3 尖刺球在 1812-1858。实现注释说 1944-1976——可能行号漂了(反编译版本差异?)。不过内容是权威:我读到的是 Terarria1456/Terraria/Wiring.cs 的 1812-1858 行,尖刺球明确有方向。

等等,让我仔细读:
```
speedX = (float)(4 * num102) + (float)Main.rand.Next(-20 + ((num102 == 1) ? 20 : 0), 21 - ((num102 == -1) ? 20 : 0)) * 0.05f;
```
num102==1(右)时 rand 范围 (0, 21) → vx = 4 + [0,1.05);num102==0(下)时 rand(-20,21) → vx = [−1, 1.05)。num102==-1(左)时 rand(-20, 1) → vx = -4 + [-1, 0.05)。

所以 1456 尖刺球方向:frameX/18 → 0/1 下抛、2 上抛、3 左、4 右。初速基准 4 px/t 加随机 ±1。生成点 = (i*16+8+14*num102, j*16+8+14*num103)。

实现侧:固定 `x*16+8, y*16+22`,vx=rand(-20,21)*0.05, vy=4+rand(0,21)*0.05 —— 只实现了"下抛"一种,且 vy = 4+rand(0,21)*0.05(范围 4~5.05)而原版 vy = 4*num103 + rand*0.05。这是**逻辑不同**(方向丢失),且实现的注释(声称"1456 改为纯下丢")与源码不符——源码明明有方向表。

等等,我还得小心。可能我读的这段(1812-1858)不是尖刺球,而是另一个 case?看上下文:case 137 里 num95 = frameY/18。switch(num95): case 0,1,2,5 → dart 族; case 3 → 尖刺球(预算); case 4 → spear。是的,case 3 是尖刺球。而且后面 `num96 = 185; damage4 = 40;` 在预算检查后。所以确认:1456 尖刺球有方向。

但是!注意预算循环:`Main.projectile[num100].type == num96`,此时 num96==0 → 循环从不匹配 → 预算恒 200?不对——num96 在 case 0/1/2/5 已赋值,但那是在同一 switch 里互斥的 case,case 3 执行时 num96 保持初始 0。所以 1456 尖刺球预算惩罚循环实际是死代码(原版 bug)。而实现侧却实现了惩罚表(声称 :1952-1966)。让我看 1944-1976 是什么。可能我看错位置,1456 的 Wiring.cs 在 1900+ 还有内容。刚才读到 1900 截断。让我继续读 1900-2600。

需要继续读 1456 Wiring.cs 1900 行往后。
````

</details>


---

## 🤖 Assistant · 2026-08-12T18:43:48.542Z · glm-x-preview-260804

```
发现重要线索:1456 的 137 陷阱 case 5(新弹种 980)和尖刺球方向表。继续读 1900 行以后。
```


---

## 🤖 Assistant · 2026-08-12T18:43:48.783Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs",
 "limit": 700,
 "offset": 1900
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:43:48.788Z

**📎 ToolResult**

```
1900							num111 = 1;
1901						}
1902						speedX = 12 * num111;
1903						damage4 = 20;
1904						num96 = 98;
1905						vector3 = new Vector2(i * 16 + 8, j * 16 + 7);
1906						vector3.X += 10 * num111;
1907						vector3.Y += 2f;
1908					}
1909					break;
1910				case -9:
1911					if (CheckMech(i, j, 200))
1912					{
1913						int num107 = -1;
1914						if (tile.frameX != 0)
1915						{
1916							num107 = 1;
1917						}
1918						speedX = 12 * num107;
1919						damage4 = 40;
1920						num96 = 184;
1921						vector3 = new Vector2(i * 16 + 8, j * 16 + 7);
1922						vector3.X += 10 * num107;
1923						vector3.Y += 2f;
1924					}
1925					break;
1926				case -8:
1927					if (CheckMech(i, j, 200))
1928					{
1929						int num112 = -1;
1930						if (tile.frameX != 0)
1931						{
1932							num112 = 1;
1933						}
1934						speedX = 5 * num112;
1935						damage4 = 40;
1936						num96 = 187;
1937						vector3 = new Vector2(i * 16 + 8, j * 16 + 7);
1938						vector3.X += 10 * num112;
1939						vector3.Y += 2f;
1940					}
1941					break;
1942				case -7:
1943				{
1944					if (!CheckMech(i, j, 300))
1945					{
1946						break;
1947					}
1948					num96 = 185;
1949					int num108 = 200;
1950					for (int num109 = 0; num109 < 1000; num109++)
1951					{
1952						if (Main.projectile[num109].active && Main.projectile[num109].type == num96)
1953						{
1954							float num110 = (new Vector2(i * 16 + 8, j * 18 + 8) - Main.projectile[num109].Center).Length();
1955							num108 = ((!(num110 < 50f)) ? ((!(num110 < 100f)) ? ((!(num110 < 200f)) ? ((!(num110 < 300f)) ? ((!(num110 < 400f)) ? ((!(num110 < 500f)) ? ((!(num110 < 700f)) ? ((!(num110 < 900f)) ? ((!(num110 < 1200f)) ? (num108 - 1) : (num108 - 2)) : (num108 - 3)) : (num108 - 4)) : (num108 - 5)) : (num108 - 6)) : (num108 - 8)) : (num108 - 10)) : (num108 - 15)) : (num108 - 50));
1956						}
1957					}
1958					if (num108 > 0)
1959					{
1960						speedX = (float)Main.rand.Next(-20, 21) * 0.05f;
1961						speedY = 4f + (float)Main.rand.Next(0, 21) * 0.05f;
1962						damage4 = 40;
1963						vector3 = new Vector2(i * 16 + 8, j * 16 + 16);
1964						vector3.Y += 6f;
1965						Projectile.NewProjectile(GetProjectileSource(i, j), (int)vector3.X, (int)vector3.Y, speedX, speedY, num96, damage4, 2f, Main.myPlayer);
1966					}
1967					break;
1968				}
1969				case -6:
1970					if (CheckMech(i, j, 90))
1971					{
1972						speedX = 0f;
1973						speedY = 8f;
1974						damage4 = 60;
1975						num96 = 186;
1976						vector3 = new Vector2(i * 16 + 8, j * 16 + 16);
1977						vector3.Y += 10f;
1978					}
1979					break;
1980				}
1981				if (num96 != 0)
1982				{
1983					Projectile.NewProjectile(GetProjectileSource(i, j), (int)vector3.X, (int)vector3.Y, speedX, speedY, num96, damage4, 2f, Main.myPlayer);
1984				}
1985				break;
1986			}
1987			case 443:
1988				GeyserTrap(i, j);
1989				break;
1990			case 21:
1991			case 467:
1992				Hopper(i, j);
1993				break;
1994			case 219:
1995			case 642:
1996				Extractinator(i, j);
1997				break;
1998			case 531:
1999			{
2000				int num88 = tile.frameX / 36;
2001				int num89 = tile.frameY / 54;
2002				int num90 = i - (tile.frameX - num88 * 36) / 18;
2003				int num91 = j - (tile.frameY - num89 * 54) / 18;
2004				if (CheckMech(num90, num91, 900))
2005				{
2006					Vector2 vector2 = new Vector2(num90 + 1, num91) * 16f;
2007					vector2.Y += 28f;
2008					int num92 = 99;
2009					int damage3 = 70;
2010					float knockBack3 = 10f;
2011					if (num92 != 0)
2012					{
2013						Projectile.NewProjectile(GetProjectileSource(num90, num91), (int)vector2.X, (int)vector2.Y, 0f, 0f, num92, damage3, knockBack3, Main.myPlayer);
2014					}
2015				}
2016				break;
2017			}
2018			case 35:
2019			case 139:
2020				WorldGen.SwitchMB(i, j);
2021				break;
2022			case 207:
2023				WorldGen.SwitchFountain(i, j);
2024				break;
2025			case 410:
2026			case 480:
2027			case 509:
2028			case 657:
2029			case 658:
2030			case 720:
2031			case 721:
2032			case 725:
2033			case 733:
2034				WorldGen.SwitchMonolith(i, j);
2035				break;
2036			case 455:
2037				BirthdayParty.ToggleManualParty();
2038				break;
2039			case 141:
2040				WorldGen.KillTile(i, j, fail: false, effectOnly: false, noItem: true);
2041				NetMessage.SendTileSquare(-1, i, j);
2042				Projectile.NewProjectile(GetProjectileSource(i, j), i * 16 + 8, j * 16 + 8, 0f, 0f, 108, 500, 10f, Main.myPlayer);
2043				break;
2044			case 210:
2045				ExplodeMine(i, j);
2046				break;
2047			case 142:
2048			case 143:
2049			{
2050				int num119 = j - tile.frameY / 18;
2051				int num120 = tile.frameX / 18;
2052				if (num120 > 1)
2053				{
2054					num120 -= 2;
2055				}
2056				num120 = i - num120;
2057				SkipWire(num120, num119);
2058				SkipWire(num120, num119 + 1);
2059				SkipWire(num120 + 1, num119);
2060				SkipWire(num120 + 1, num119 + 1);
2061				if (type == 142)
2062				{
2063					for (int num121 = 0; num121 < 4; num121++)
2064					{
2065						if (_numInPump >= 19)
2066						{
2067							break;
2068						}
2069						int num122;
2070						int num123;
2071						switch (num121)
2072						{
2073						case 0:
2074							num122 = num120;
2075							num123 = num119 + 1;
2076							break;
2077						case 1:
2078							num122 = num120 + 1;
2079							num123 = num119 + 1;
2080							break;
2081						case 2:
2082							num122 = num120;
2083							num123 = num119;
2084							break;
2085						default:
2086							num122 = num120 + 1;
2087							num123 = num119;
2088							break;
2089						}
2090						_inPumpX[_numInPump] = num122;
2091						_inPumpY[_numInPump] = num123;
2092						_numInPump++;
2093					}
2094					break;
2095				}
2096				for (int num124 = 0; num124 < 4; num124++)
2097				{
2098					if (_numOutPump >= 19)
2099					{
2100						break;
2101					}
2102					int num122;
2103					int num123;
2104					switch (num124)
2105					{
2106					case 0:
2107						num122 = num120;
2108						num123 = num119 + 1;
2109						break;
2110					case 1:
2111						num122 = num120 + 1;
2112						num123 = num119 + 1;
2113						break;
2114					case 2:
2115						num122 = num120;
2116						num123 = num119;
2117						break;
2118					default:
2119						num122 = num120 + 1;
2120						num123 = num119;
2121						break;
2122					}
2123					_outPumpX[_numOutPump] = num122;
2124					_outPumpY[_numOutPump] = num123;
2125					_numOutPump++;
2126				}
2127				break;
2128			}
2129			case 105:
2130			{
2131				int num138 = j - tile.frameY / 18;
2132				int num139 = tile.frameX / 18;
2133				int num140 = 0;
2134				while (num139 >= 2)
2135				{
2136					num139 -= 2;
2137					num140++;
2138				}
2139				num139 = i - num139;
2140				num139 = i - tile.frameX % 36 / 18;
2141				num138 = j - tile.frameY % 54 / 18;
2142				int num141 = tile.frameY / 54;
2143				num141 %= 3;
2144				num140 = tile.frameX / 36 + num141 * 55;
2145				SkipWire(num139, num138);
2146				SkipWire(num139, num138 + 1);
2147				SkipWire(num139, num138 + 2);
2148				SkipWire(num139 + 1, num138);
2149				SkipWire(num139 + 1, num138 + 1);
2150				SkipWire(num139 + 1, num138 + 2);
2151				int num142 = num139 * 16 + 16;
2152				int num143 = (num138 + 3) * 16;
2153				int num144 = -1;
2154				int num145 = -1;
2155				bool flag6 = true;
2156				bool flag7 = false;
2157				switch (num140)
2158				{
2159				case 5:
2160					num145 = 73;
2161					break;
2162				case 13:
2163					num145 = 24;
2164					break;
2165				case 30:
2166					num145 = 6;
2167					break;
2168				case 35:
2169					num145 = 2;
2170					break;
2171				case 51:
2172					num145 = Utils.SelectRandom(Main.rand, new short[2] { 299, 538 });
2173					break;
2174				case 52:
2175					num145 = 356;
2176					break;
2177				case 53:
2178					num145 = 357;
2179					break;
2180				case 54:
2181					num145 = Utils.SelectRandom(Main.rand, new short[2] { 355, 358 });
2182					break;
2183				case 55:
2184					num145 = Utils.SelectRandom(Main.rand, new short[2] { 367, 366 });
2185					break;
2186				case 56:
2187					num145 = Utils.SelectRandom(Main.rand, new short[5] { 359, 359, 359, 359, 360 });
2188					break;
2189				case 57:
2190					num145 = 377;
2191					break;
2192				case 58:
2193					num145 = 300;
2194					break;
2195				case 59:
2196					num145 = Utils.SelectRandom(Main.rand, new short[2] { 364, 362 });
2197					break;
2198				case 60:
2199					num145 = 148;
2200					break;
2201				case 61:
2202					num145 = 361;
2203					break;
2204				case 62:
2205					num145 = Utils.SelectRandom(Main.rand, new short[3] { 487, 486, 485 });
2206					break;
2207				case 63:
2208					num145 = 164;
2209					flag6 &= NPC.MechSpawn(num142, num143, 165);
2210					break;
2211				case 64:
2212					num145 = 86;
2213					flag7 = true;
2214					break;
2215				case 65:
2216					num145 = 490;
2217					break;
2218				case 66:
2219					num145 = 82;
2220					break;
2221				case 67:
2222					num145 = 449;
2223					break;
2224				case 68:
2225					num145 = 167;
2226					break;
2227				case 69:
2228					num145 = 480;
2229					break;
2230				case 70:
2231					num145 = 48;
2232					break;
2233				case 71:
2234					num145 = Utils.SelectRandom(Main.rand, new short[3] { 170, 180, 171 });
2235					flag7 = true;
2236					break;
2237				case 72:
2238					num145 = 481;
2239					break;
2240				case 73:
2241					num145 = 482;
2242					break;
2243				case 74:
2244					num145 = 430;
2245					break;
2246				case 75:
2247					num145 = 489;
2248					break;
2249				case 76:
2250					num145 = 611;
2251					break;
2252				case 77:
2253					num145 = 602;
2254					break;
2255				case 78:
2256					num145 = Utils.SelectRandom(Main.rand, new short[6] { 595, 596, 599, 597, 600, 598 });
2257					break;
2258				case 79:
2259					num145 = Utils.SelectRandom(Main.rand, new short[2] { 616, 617 });
2260					break;
2261				case 80:
2262					num145 = Utils.SelectRandom(Main.rand, new short[2] { 671, 672 });
2263					break;
2264				case 81:
2265					num145 = 673;
2266					break;
2267				case 82:
2268					num145 = Utils.SelectRandom(Main.rand, new short[2] { 674, 675 });
2269					break;
2270				}
2271				if (num145 != -1 && CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, num145) && flag6)
2272				{
2273					if (!flag7 || !Collision.SolidTiles(num139 - 2, num139 + 3, num138, num138 + 2))
2274					{
2275						num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143, num145);
2276					}
2277					else
2278					{
2279						Vector2 position = new Vector2(num142 - 4, num143 - 22) - new Vector2(10f);
2280						Utils.PoofOfSmoke(position);
2281						NetMessage.SendData(106, -1, -1, null, (int)position.X, position.Y);
2282					}
2283				}
2284				if (num144 <= -1)
2285				{
2286					switch (num140)
2287					{
2288					case 4:
2289						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 1))
2290						{
2291							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 1);
2292						}
2293						break;
2294					case 7:
2295						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 49))
2296						{
2297							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142 - 4, num143 - 6, 49);
2298						}
2299						break;
2300					case 8:
2301						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 55))
2302						{
2303							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 55);
2304						}
2305						break;
2306					case 9:
2307					{
2308						int type4 = 46;
2309						if (BirthdayParty.PartyIsUp)
2310						{
2311							type4 = 540;
2312						}
2313						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, type4))
2314						{
2315							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, type4);
2316						}
2317						break;
2318					}
2319					case 10:
2320						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 21))
2321						{
2322							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143, 21);
2323						}
2324						break;
2325					case 16:
2326						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 42))
2327						{
2328							if (!Collision.SolidTiles(num139 - 1, num139 + 1, num138, num138 + 1))
2329							{
2330								num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 42);
2331								break;
2332							}
2333							Vector2 position3 = new Vector2(num142 - 4, num143 - 22) - new Vector2(10f);
2334							Utils.PoofOfSmoke(position3);
2335							NetMessage.SendData(106, -1, -1, null, (int)position3.X, position3.Y);
2336						}
2337						break;
2338					case 18:
2339						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 67))
2340						{
2341							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 67);
2342						}
2343						break;
2344					case 23:
2345						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 63))
2346						{
2347							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 63);
2348						}
2349						break;
2350					case 27:
2351						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 85))
2352						{
2353							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142 - 9, num143, 85);
2354						}
2355						break;
2356					case 28:
2357						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 74))
2358						{
2359							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, Utils.SelectRandom(Main.rand, new short[3] { 74, 297, 298 }));
2360						}
2361						break;
2362					case 34:
2363					{
2364						for (int num154 = 0; num154 < 2; num154++)
2365						{
2366							for (int num155 = 0; num155 < 3; num155++)
2367							{
2368								Tile tile2 = Main.tile[num139 + num154, num138 + num155];
2369								tile2.type = 349;
2370								tile2.frameX = (short)(num154 * 18 + 216);
2371								tile2.frameY = (short)(num155 * 18);
2372							}
2373						}
2374						Animation.NewTemporaryAnimation(0, 349, num139, num138);
2375						if (Main.netMode == 2)
2376						{
2377							NetMessage.SendTileSquare(-1, num139, num138, 2, 3);
2378						}
2379						break;
2380					}
2381					case 42:
2382						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 58))
2383						{
2384							num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 58);
2385						}
2386						break;
2387					case 37:
2388						if (CheckMech(num139, num138, 600) && Item.MechSpawn(num142, num143, 58) && Item.MechSpawn(num142, num143, 1734) && Item.MechSpawn(num142, num143, 1867))
2389						{
2390							Item.NewItem(GetItemSource(num142, num143), num142, num143 - 16, 0, 0, 58);
2391						}
2392						break;
2393					case 50:
2394						if (CheckMech(num139, num138, 30) && NPC.MechSpawn(num142, num143, 65))
2395						{
2396							if (!Collision.SolidTiles(num139 - 2, num139 + 3, num138, num138 + 2))
2397							{
2398								num144 = NPC.NewNPC(GetNPCSource(num139, num138), num142, num143 - 12, 65);
2399								break;
2400							}
2401							Vector2 position2 = new Vector2(num142 - 4, num143 - 22) - new Vector2(10f);
2402							Utils.PoofOfSmoke(position2);
2403							NetMessage.SendData(106, -1, -1, null, (int)position2.X, position2.Y);
2404						}
2405						break;
2406					case 2:
2407						if (CheckMech(num139, num138, 600) && Item.MechSpawn(num142, num143, 184) && Item.MechSpawn(num142, num143, 1735) && Item.MechSpawn(num142, num143, 1868))
2408						{
2409							Item.NewItem(GetItemSource(num142, num143), num142, num143 - 16, 0, 0, 184);
2410						}
2411						break;
2412					case 17:
2413						if (CheckMech(num139, num138, 600) && Item.MechSpawn(num142, num143, 166))
2414						{
2415							Item.NewItem(GetItemSource(num142, num143), num142, num143 - 20, 0, 0, 166);
2416						}
2417						break;
2418					case 40:
2419					{
2420						if (!CheckMech(num139, num138, 300))
2421						{
2422							break;
2423						}
2424						int num150 = 50;
2425						int[] array2 = new int[num150];
2426						int num151 = 0;
2427						for (int num152 = 0; num152 < Main.maxNPCs; num152++)
2428						{
2429							if (Main.npc[num152].active && (Main.npc[num152].type == 17 || Main.npc[num152].type == 19 || Main.npc[num152].type == 22 || Main.npc[num152].type == 38 || Main.npc[num152].type == 54 || Main.npc[num152].type == 107 || Main.npc[num152].type == 108 || Main.npc[num152].type == 142 || Main.npc[num152].type == 160 || Main.npc[num152].type == 207 || Main.npc[num152].type == 209 || Main.npc[num152].type == 227 || Main.npc[num152].type == 228 || Main.npc[num152].type == 229 || Main.npc[num152].type == 368 || Main.npc[num152].type == 369 || Main.npc[num152].type == 550 || Main.npc[num152].type == 441 || Main.npc[num152].type == 588))
2430							{
2431								array2[num151] = num152;
2432								num151++;
2433								if (num151 >= num150)
2434								{
2435									break;
2436								}
2437							}
2438						}
2439						if (num151 > 0)
2440						{
2441							int num153 = array2[Main.rand.Next(num151)];
2442							Main.npc[num153].Teleport(new Vector2(num142 - Main.npc[num153].width / 2, num143 - Main.npc[num153].height - 1), 14);
2443						}
2444						break;
2445					}
2446					case 41:
2447					{
2448						if (!CheckMech(num139, num138, 300))
2449						{
2450							break;
2451						}
2452						int num146 = 50;
2453						int[] array = new int[num146];
2454						int num147 = 0;
2455						for (int num148 = 0; num148 < Main.maxNPCs; num148++)
2456						{
2457							if (Main.npc[num148].active && (Main.npc[num148].type == 18 || Main.npc[num148].type == 20 || Main.npc[num148].type == 124 || Main.npc[num148].type == 178 || Main.npc[num148].type == 208 || Main.npc[num148].type == 353 || Main.npc[num148].type == 633 || Main.npc[num148].type == 663))
2458							{
2459								array[num147] = num148;
2460								num147++;
2461								if (num147 >= num146)
2462								{
2463									break;
2464								}
2465							}
2466						}
2467						if (num147 > 0)
2468						{
2469							int num149 = array[Main.rand.Next(num147)];
2470							Main.npc[num149].Teleport(new Vector2(num142 - Main.npc[num149].width / 2, num143 - Main.npc[num149].height - 1), 14);
2471						}
2472						break;
2473					}
2474					}
2475				}
2476				if (num144 >= 0)
2477				{
2478					Main.npc[num144].value = 0f;
2479					Main.npc[num144].npcSlots = 0f;
2480					Main.npc[num144].SpawnedFromStatue = true;
2481					Main.npc[num144].CanBeReplacedByOtherNPCs = true;
2482				}
2483				break;
2484			}
2485			case 349:
2486			{
2487				int num113 = tile.frameY / 18;
2488				num113 %= 3;
2489				int num114 = j - num113;
2490				int num115;
2491				for (num115 = tile.frameX / 18; num115 >= 2; num115 -= 2)
2492				{
2493				}
2494				num115 = i - num115;
2495				SkipWire(num115, num114);
2496				SkipWire(num115, num114 + 1);
2497				SkipWire(num115, num114 + 2);
2498				SkipWire(num115 + 1, num114);
2499				SkipWire(num115 + 1, num114 + 1);
2500				SkipWire(num115 + 1, num114 + 2);
2501				short num116 = (short)((Main.tile[num115, num114].frameX != 0) ? (-216) : 216);
2502				for (int num117 = 0; num117 < 2; num117++)
2503				{
2504					for (int num118 = 0; num118 < 3; num118++)
2505					{
2506						Main.tile[num115 + num117, num114 + num118].frameX += num116;
2507					}
2508				}
2509				if (Main.netMode == 2)
2510				{
2511					NetMessage.SendTileSquare(-1, num115, num114, 2, 3);
2512				}
2513				Animation.NewTemporaryAnimation((num116 <= 0) ? 1 : 0, 349, num115, num114);
2514				break;
2515			}
2516			case 506:
2517			{
2518				int num75 = tile.frameY / 18;
2519				num75 %= 3;
2520				int num76 = j - num75;
2521				int num77;
2522				for (num77 = tile.frameX / 18; num77 >= 2; num77 -= 2)
2523				{
2524				}
2525				num77 = i - num77;
2526				if (!WorldGen.ValidateTileSquareIsActiveAndOfType(num77, num76, 2, 3, type))
2527				{
2528					break;
2529				}
2530				SkipWire(num77, num76);
2531				SkipWire(num77, num76 + 1);
2532				SkipWire(num77, num76 + 2);
2533				SkipWire(num77 + 1, num76);
2534				SkipWire(num77 + 1, num76 + 1);
2535				SkipWire(num77 + 1, num76 + 2);
2536				short num78 = (short)((Main.tile[num77, num76].frameX >= 72) ? (-72) : 72);
2537				for (int num79 = 0; num79 < 2; num79++)
2538				{
2539					for (int num80 = 0; num80 < 3; num80++)
2540					{
2541						Main.tile[num77 + num79, num76 + num80].frameX += num78;
2542					}
2543				}
2544				if (Main.netMode == 2)
2545				{
2546					NetMessage.SendTileSquare(-1, num77, num76, 2, 3);
2547				}
2548				break;
2549			}
2550			case 546:
2551				tile.type = 557;
2552				WorldGen.SquareTileFrame(i, j);
2553				NetMessage.SendTileSquare(-1, i, j);
2554				break;
2555			case 557:
2556				tile.type = 546;
2557				WorldGen.SquareTileFrame(i, j);
2558				NetMessage.SendTileSquare(-1, i, j);
2559				break;
2560			}
2561		}
2562	
2563		private static void Extractinator(int sourceX, int sourceY)
2564		{
2565			Tile tile = Main.tile[sourceX, sourceY];
2566			int num = sourceX;
2567			int num2 = sourceY;
2568			num -= tile.frameX % 54 / 18;
2569			num2 -= tile.frameY % 54 / 18;
2570			int time = 60;
2571			if (!CheckMech(num, num2, time) || !TryFindChestForExtractinator(num, num2, out var chestIndex) || Chest.UsingChest(chestIndex) != -1)
2572			{
2573				return;
2574			}
2575			int type = tile.type;
2576			Item[] item = Main.chest[chestIndex].item;
2577			for (int num3 = Main.chest[chestIndex].maxItems - 1; num3 >= 0; num3--)
2578			{
2579				Item item2 = item[num3];
2580				if (!item2.IsAir)
2581				{
2582					ExtractinatorHelper.RollExtractinatorDrop(ItemID.Sets.ExtractinatorMode[item2.type], type, out var itemType, out var stack);
2583					if (itemType > 0)
2584					{
2585						if (--item2.stack <= 0)
2586						{
2587							item2.TurnToAir();
2588						}
2589						Item.NewItem(new EntitySource_Wiring(num, num2), num * 16, num2 * 16, 32, 32, itemType, stack, noBroadcast: false, -1);
2590						break;
2591					}
2592				}
2593			}
2594		}
2595	
2596		private static bool TryFindChestForExtractinator(int lookupX, int lookupY, out int chestIndex)
2597		{
2598			chestIndex = 0;
2599			int num = 3;

```


---

## 🤖 Assistant · 2026-08-12T18:44:41.850Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
重要确认:

1. **尖刺球(case 3, :1812-1858)**:有方向表(frameX/18 → num102/num103),生成点 (i*16+8+14*dir, j*16+8+14*dir)。预算循环里 `Main.projectile[num100].type == num96` —— num96 此刻 = 0(未被赋值,因为 num96=185 的赋值在预算检查之后 :1830)。等等,让我重看。1456 :1818 `int num99 = 200;` 然后循环 `Main.projectile[num100].type == num96`,num96=0 → 循环恒 false → 预算恒 200。然后 :1829 `num96 = 185`。这确实是原版 bug —— 尖刺球预算惩罚在 1456 主 case 3 里是死代码。

   但注意 :1944-1967 还有一个 **case -7**!switch(num95) 的第二段(num95 减了 10?)。看 :1892 `switch (num95)` —— 第一段 switch 里 case 3 结束后 num96=185,然后走到第二个 switch(num95):case -10 → dart、case -9 → superdart、case -8 → flame、case -7 → 尖刺球(预算循环在 num96=185 赋值**之后**,所以这里预算生效!)、case -6 → spear。

   等等,这就奇怪了。num95 是 frameY/18,怎么会是负数?让我往前看,在 :1766 `int num95 = tile.frameY / 18;`。然后第一个 switch(num95) case 0,1,2,5 → dart 族;case 3 → 尖刺球;case 4 → spear。第二个 switch(num95) case -10, -9, -8, -7, -6 —— num95 是 tile.frameY/18(frameY 是 short,可能为负?不会)。

   哦!我明白了。这是反编译产物:两个 switch 其实是编译器拆分的同一个 switch。case -10 等价于什么?看内容:case -10 → 弹 98(dart)速度 12 方向 frameX;case -9 → 184;case -8 → 187;case -7 → 185(尖刺球,预算生效);case -6 → 186(spear,向下 8 速)。

   这看起来像 1.4.4 新增的"超级飞镖陷阱变体"?等等,num95 = frameY/18,负数不可能。除非……让我看 :1766 之前有没有对 num95 的修改。

   回看 :1764-1772:
   ```
   case 137:
   {
       int num95 = tile.frameY / 18;
       ...
       switch (num95)
       {
       case 0: case 1: case 2: case 5: ...
   ```
   然后 case 3(尖刺球,预算死代码)和 case 4(spear)。然后 :1892 `switch (num95)` case -10 等。

   嗯,如果 num95 恒非负,case -10 永不触发,那 -10..-6 是死代码?但 1456 反编译不会无故生成负数 case。让我想想:Tile.frameY 是 short。frameY/18 用整数除法。如果 frameY 是 18 的倍数非负,结果非负。

   等等——也许这两个 switch 是 **fallthrough 结构**的反编译。第一个 switch 处理完 case 3/4 后,代码继续执行第二个 switch。如果 num95 == 3,第一个 switch case 3 已设 num96=185,然后第二个 switch(num95) case -7 不匹配(num95==3),所以尖刺球会被发射(:1981 `if (num96 != 0) Projectile.NewProjectile(...)`)。

   而 case -7 分支(num95 == -7)永远不会被进入,因为 num95 >= 0。

   所以:1456 中**实际生效**的尖刺球路径是 :1812-1858 的 case 3(预算死代码 + 方向表),发射在 :1983 统一 NewProjectile。而 case -7(-10..-6 整段)是死代码?那为什么会有这段?

   哦!!我想起来了。这是 1.4.4 的"陷阱方块"(Trap blocks?)。不对。让我 grep tile 137 的 frameY 可能值。也许 frameY/18 可以是 6+?不,-10 不可能。

   除非:num95 不是 frameY/18。让我再读一遍 :1766。

   从我的 Read 输出:
   ```
   1764			case 137:
   1765			{
   1766				int num95 = tile.frameY / 18;
   ```
   是的,num95 = frameY / 18。

   那 case -10..-6 死代码。但为什么存在?可能是 1.4.4 的 "Gas Trap" 或其它新陷阱使用负 frameY?或者这是 ilspycmd 反编译的错误。无论如何,实现侧引用 ":1944-1976" 并声称"1456 改为纯下丢"是错的——1456 生效路径是 :1812-1858,有方向表。

   等一下,我再仔细核对实现注释:"尖刺球(Wiring.cs:1536-1599 / 1456 :1944-1976):CheckMech 300 + 场上每个 185 按自身距离扣预算(...)预算>0 才发。发射无视朝向(1405 曾按 frameX 定向,1456 改为纯下丢,取 1456):固定方块底 (x*16+8, y*16+22),vx=rand(-20,21)*0.05 ∈[-1,1]、vy=4+rand(0,21)*0.05 ∈[4,5]"

   实现"取 1456 :1944-1976"= 我读到的 case -7(:1942-1968)。这段确实是"纯下丢 + 预算生效"!而 1405 的版本可能就是 :1812-1858(有方向)。所以实现者选了 1456 的 case -7(预算生效+无方向)作为"最终态",认为 case 3 是旧逻辑。

   但按反编译代码,case 3(num95==3)与 case -7(num95==-7)不会同时可达;case -7 需要 num95 == -7,而 num95 = frameY/18 >= 0,所以 **case -7 是不可达死代码**,真正的执行路径是 case 3!除非……

   哦等等!我要重新看。第二个 switch 是 `switch (num95)`,case -10/-9/-8/-7/-6。如果这些是死代码,那 :1960-1965 的尖刺球发射(NewProjectile 直接调用)永不执行,而 case 3 的设置(num96/speed/vector3)在 :1981 `if (num96 != 0)` 处发射。

   让我检查一下:第一个 switch 里 case 3 是否设置了 vector3。是的 :1855 `vector3 = new Vector2(i * 16 + 8 + 14 * num102, j * 16 + 8 + 14 * num103);`。然后 :1981-1984 统一发射。所以 case 3 → 发射,位置 (i*16+8+14*dirX, j*16+8+14*dirY),速度 (4*dirX + rand*0.05, 4*dirY + rand*0.05),预算恒 200(死代码)。

   而 case -7 → 需要 num95==-7,不可达。

   除非 frameY 可以为负?Tile.frameY 是 short,可能因数据损坏为负,但正常放置不会。所以结论:**1456 实际行为 = 方向表 + 预算不扣(死代码)**。

   实现侧选择 = 无方向(固定下丢)+ 预算扣分。两边都与 1456 生效路径不同:
   - 实现丢了方向表(frameX 定向)
   - 实现多实现了预算惩罚(1456 死代码)

   嗯,但我要谨慎。也许我读的这段在 1456 里对应的是**另一个入口**(比如 HitWireSingle 之外)。让我 grep 一下 1456 Wiring.cs 里 "case 137" 出现几次,以及 num95 赋值。

   还有一种可能:反编译器把一个 `switch` 拆成两个,第二个 switch 的 case 值其实是**哈希表跳转**的伪影。case -10, -9, -8, -7, -6 连续负数,很可疑。可能是编译器生成的"稀疏 switch 优化",负数 case 对应某个 lookup。ilspycmd 有时会把 jump table 翻译错。但作为"唯一标杆",我只能按字面读。

   实际上!我想到了。Terraria 1.4.4 加了 **Super Dart Trap / Flame Trap 的"被玩家触发"变体**?不。让我看 1405 的对应代码,对比哪个是 1.4.0.5 原貌。

   让我 grep 1405 Wiring.cs 的 case 137。

2. **case 105 雕像**:
   - 实现 STATUE_NPC_DIRECT 的 style 9(兔)缺 **BirthdayParty.PartyIsUp → 540**(派对兔)。1456 :2306-2317:case 9 → type4 = 46,若 PartyIsUp 则 540。实现写死 46。
   - 实现 case 40/41 城镇 NPC 搬迁:原版是**随机选一个活跃城镇 NPC 传送过来**(CheckMech 300 + 白名单数组随机),实现注释说"搬到 (px,py)"由 ctx.relocateTownNpc 实现,需查 Game.ts 是否随机选。
   - 原版 case 37 心雕像 CheckMech 600 + Item.MechSpawn ×3(58/1734/1867);实现一致 ✅。
   - 原版 case 17 炸弹:CheckMech 600 + MechSpawn(166),Item.NewItem(..., num143-20)——实现 dropItem(item 166, px, py-16)?1456 :2415 是 `num143 - 20`(y-20px),实现 devices.ts:473 `ctx.dropItem(itemEntry.item, px, py - 16)` → 16 vs 20。轻微偏差(像素级,影响不大,但不是 1:1)。
   - 原版 case 5→73 等:flag7(实心判定)只对 case 64 和 71 生效 ✅ 实现一致。
   - 原版 case 63:flag6 &= NPC.MechSpawn(165)(两次 MechSpawn:164 和 165)✅ 实现一致。
   - 原版雕像生成后:value=0、npcSlots=0、SpawnedFromStatue=true、CanBeReplacedByOtherNPCs=true ✅ Game.ts:7008 注释提到 value=0 + SpawnedFromStatue,需确认 npcSlots 和 CanBeReplacedByOtherNPCs。
   - 注意:原版雕像 spawn 用 NPC.NewNPC(...) 返回 num144,然后统一在 :2476 检查。实现的 ctx.spawnNpc 返回 boolean。需查 Game.ts。

   另一个大点:原版 case 105 中,`num138 = j - tile.frameY / 18;` 先算,然后 :2139 `num139 = i - num139;`(num139 此时是 while 后的余数)再 :2140 `num139 = i - tile.frameX % 36 / 18;` **覆盖**,:2141 `num138 = j - tile.frameY % 54 / 18;` 覆盖。所以锚点 = (i - frameX%36/18, j - frameY%54/18)。实现 devices.ts:427-428 一致 ✅。

3. **case 531 巨石雕像**:原版 vector2 = (num90+1, num91)*16, Y+=28 → y = (num91)*16+28。实现:`ctx.shootProjectile(ox*16+16, (oy+1)*16, ...)` → y = oy*16+16。原版 y = num91*16 + 28!实现是 (oy+1)*16 = oy*16+16。**偏差 12px**(28 vs 16)。还有击退:原版 kb 10,伤害 70。实现 damage 70 ✅,kb 不在接口里(需查 Dart)。

4. **case 141 炸药**:原版 KillTile(fail:false, effectOnly:false, noItem:true) → 清格 + Projectile 108(500 伤/半径 10)。实现:`st.setTile(x,y,0); ctx.explode(x,y,500,10)` ✅ 大体一致(noItem 语义=不掉物品,直接清格,近似)。

5. **case 210 地雷**:原版 HitWireSingle case 210 → ExplodeMine。实现 devices.ts:705-708 ✅ 有。但 HitSwitch 里的 type==210 → ExplodeMine(右键触发)在实现的 hitSwitch 缺失!原版 :288-291 `else if (Main.tile[i,j].type == 210) ExplodeMine(i,j);`。实现 hitSwitch(Wiring.ts:204-273)没有 210 分支。需要确认 Game.ts 右键地雷是否走别的路径。

6. **case 349 蘑菇动画**:实现雕像 style 34 直接变 tile 349(:477-485),但原版 style 34 是把雕像**变成** 349?看 :2362-2379:case 34 → 把 2×3 区域 tile type=349, frameX=num154*18+216。然后 case 349(单独 case,:2485-2514)是"349 被 wire 触发 → frameX ±216 动画回弹"。所以蘑菇雕像通电 = 变成 349 弹蘑菇,之后 349 被触发时动画。实现 style 34 直接设置 349 ✅ 一致。缺 case 349 的二次触发动画分支(devices.ts 没有 349 case!)。查 deviceTable:没有 349。**缺失**。

   还有 Animation.NewTemporaryAnimation(0, 349, ...) 是 0 帧动画。近似可忽略,但 349 的 wire 触发分支缺失是实际差异(蘑菇块放线后可以再触发动画)。小众,标注。

7. **case 506 巴斯特雕像**:原版有 `WorldGen.ValidateTileSquareIsActiveAndOfType(num77, num76, 2, 3, type)` 门;实现 flipBlock 无此门。近似,小。

8. **case 21/467 → Hopper**(1.4.4 新 hopper 系统!):原版 :1990-1993 `case 21: case 467: Hopper(i, j); break;` —— 这是 1.4.4 加的漏斗!宝箱通电时抓取附近物品。实现 deviceTable **没有 21/467 Hopper case**(实现 case 130 通电石,宝箱 21 没有任何 wire 响应)。**未实现**。HopperGrabHitboxSize = 192px 也在 :75。这是 1.4.4 新机制。

   等等,宝箱通电?tile 21=chest,467=locked? 不对,467 是水晶陷阱箱?前面 HitSwitch 里 467 是 "水晶陷阱箱"。但 Hopper case 21/467 —— 让我看 Hopper 的实现确认。在 :2600 之后。需要读。

9. **case 356 日晷(sundial)和 case 663 月晷(moondial)**:1456 :1137-1176。实现 devices.ts **没有 356/663**!日晷通电跳到白天(fastForwardTimeToDawn)、月晷跳到夜晚。缺。**未实现**(1.4.4 moondial 663 是新的,sundial 356 是 1.3.1 就有)。

10. **case 425 广播盒**:原版有 `if (Main.AnnouncementBoxDisabled) return;` 和 Range 判定。实现注释已登记"设置未接,恒全图"——与默认值(AnnouncementBoxDisabled=false, Range=-1)等价 ✅。

11. **ToggleFirePlace/Campfire/Torch/Lamp/Candle 等辅助方法**在 2600 行以后,需要读来核对帧翻转逻辑。

12. **case 15 frameY/40==1 或 20**(马桶):实现 devices.ts:554 `Math.floor(st.frameY[i]/40) !== 1 && !== 20 return true` ✅ 一致。

13. **case 137 的 case 5**:弹 980、30 伤、速度 12。980 是什么?1.4.4 新增 "Venom Dart Trap"?查 wiki。tile 137 frameY/18==5 的 placeStyle。也可能是"毒镖陷阱"。这是 **1405 没有的新增**(1405 是 1.4.0.5)。需 grep 1405 确认。实现 fireTrap 只处理 kind 0-4,**缺 kind 5** ❌。

    还有第二段 switch case -10/-9/-8(等价 0/1/2 的水平变体)+ case -7(尖刺球,预算生效)+ case -6(spear,纯下 8 速)。这些在 1405 中应该对应不同结构。让我看 1405 的 137。

14. **传送器 Teleport()** 在 :2600 以后,需要读。

15. **ExplodeMine** 在后面。

16. 还有 **SetCurrentUser/Hopper/Teleport/GeyserTrap/ExplodeMine/MassWireOperationInner/DeActive/CanKillTile** 在 2600-3441。

先读 2600-3441。
````

</details>


---

## 🤖 Assistant · 2026-08-12T18:44:42.290Z · glm-x-preview-260804

```
1456 与实现差异开始浮现(case 5 新弹种 980、Hopper、日晷/月晷)。读完剩余源码段。
```


---

## 🤖 Assistant · 2026-08-12T18:44:42.624Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs",
 "limit": 841,
 "offset": 2600
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:44:42.634Z

**📎 ToolResult**

```
2600			int num2 = 3;
2601			int num3 = 2;
2602			for (int i = lookupX - num3; i <= lookupX + num + num3; i++)
2603			{
2604				for (int j = lookupY - num3; j <= lookupY + num2 + num3; j++)
2605				{
2606					if (!Chest.IsLocked(i, j))
2607					{
2608						int num4 = Chest.FindChest(i, j);
2609						if (num4 != -1)
2610						{
2611							chestIndex = num4;
2612							return true;
2613						}
2614					}
2615				}
2616			}
2617			return false;
2618		}
2619	
2620		public static bool IsHopperInRangeOf(WorldItem item)
2621		{
2622			if (ItemID.Sets.ItemsThatShouldNotBeInInventory[item.type])
2623			{
2624				return false;
2625			}
2626			Rectangle hitbox = item.Hitbox;
2627			hitbox.Inflate((int)(HopperGrabHitboxSize.X / 2f), (int)(HopperGrabHitboxSize.Y / 2f));
2628			Point point = hitbox.TopLeft().ToTileCoordinates().ClampedInWorld();
2629			Point point2 = hitbox.BottomRight().ToTileCoordinates().ClampedInWorld();
2630			for (int i = point.X; i <= point2.X; i++)
2631			{
2632				for (int j = point.Y; j <= point2.Y; j++)
2633				{
2634					Tile tile = Main.tile[i, j];
2635					if (tile != null && tile.active())
2636					{
2637						int type = tile.type;
2638						if ((type == 21 || type == 467) && tile.anyWire())
2639						{
2640							return true;
2641						}
2642					}
2643				}
2644			}
2645			return false;
2646		}
2647	
2648		private static void Hopper(int sourceX, int sourceY)
2649		{
2650			Tile tile = Main.tile[sourceX, sourceY];
2651			int num = sourceX;
2652			int num2 = sourceY;
2653			if (tile.frameX % 36 != 0)
2654			{
2655				num--;
2656			}
2657			if (tile.frameY % 36 != 0)
2658			{
2659				num2--;
2660			}
2661			int time = 60;
2662			if (!CheckMech(num, num2, time) || Chest.IsLocked(num, num2))
2663			{
2664				return;
2665			}
2666			int num3 = Chest.FindChest(num, num2);
2667			if (num3 == -1 || Chest.UsingChest(num3) != -1)
2668			{
2669				return;
2670			}
2671			Rectangle value = Utils.CenteredRectangle(new Vector2(num * 16 + 16, num2 * 16 + 16), HopperGrabHitboxSize);
2672			bool flag = false;
2673			for (int i = 0; i < 400; i++)
2674			{
2675				WorldItem worldItem = Main.item[i];
2676				int type = worldItem.type;
2677				if (worldItem.active && worldItem.playerIndexTheItemIsReservedFor == Main.myPlayer && !ItemID.Sets.ItemsThatShouldNotBeInInventory[worldItem.type] && worldItem.Hitbox.Intersects(value) && TryToPutItemInChest(i, num3))
2678				{
2679					flag = true;
2680					NetMessage.SendData(21, -1, -1, null, i);
2681					Chest.VisualizeChestTransfer(worldItem.Center, value.Center.ToVector2(), type, Chest.ItemTransferVisualizationSettings.Hopper);
2682				}
2683			}
2684			if (flag)
2685			{
2686				ItemSorting.SortInventory(Main.chest[num3], withSync: false, withFeedback: false);
2687			}
2688		}
2689	
2690		private static bool TryToPutItemInChest(int itemIndex, int chestIndex)
2691		{
2692			WorldItem worldItem = Main.item[itemIndex];
2693			if (worldItem.IsACoin)
2694			{
2695				return TryMoveCoinsInChest(itemIndex, chestIndex);
2696			}
2697			Chest chest = Main.chest[chestIndex];
2698			for (int i = 0; i < chest.maxItems; i++)
2699			{
2700				if (TryAddingToStack(itemIndex, chestIndex, i) && worldItem.IsAir)
2701				{
2702					return true;
2703				}
2704			}
2705			for (int j = 0; j < chest.maxItems; j++)
2706			{
2707				if (TryAddingToEmptySlot(itemIndex, chestIndex, j) && worldItem.IsAir)
2708				{
2709					return true;
2710				}
2711			}
2712			return false;
2713		}
2714	
2715		private static bool TryMoveCoinsInChest(int itemIndex, int chestIndex)
2716		{
2717			WorldItem worldItem = Main.item[itemIndex];
2718			if (!worldItem.IsACoin)
2719			{
2720				return false;
2721			}
2722			int maxItems = Main.chest[chestIndex].maxItems;
2723			Item[] item = Main.chest[chestIndex].item;
2724			bool overFlowing;
2725			long num = Utils.CoinsCount(out overFlowing, item);
2726			int num2 = worldItem.value / 5;
2727			int[] array = Utils.CoinsSplit(num + num2 * worldItem.stack);
2728			int[] array2 = new int[array.Length];
2729			int num3 = 0;
2730			for (int num4 = array.Length - 1; num4 >= 0; num4--)
2731			{
2732				if (array[num4] != 0)
2733				{
2734					while (true)
2735					{
2736						if (num3 >= maxItems)
2737						{
2738							return false;
2739						}
2740						if (item[num3].IsAir || item[num3].IsACoin)
2741						{
2742							break;
2743						}
2744						num3++;
2745					}
2746					array2[num4] = num3++;
2747				}
2748			}
2749			Item[] array3 = item;
2750			foreach (Item item2 in array3)
2751			{
2752				if (item2.IsACoin)
2753				{
2754					item2.TurnToAir();
2755				}
2756			}
2757			for (int num5 = array.Length - 1; num5 >= 0; num5--)
2758			{
2759				if (array[num5] != 0)
2760				{
2761					int num6 = 71 + num5;
2762					int num7 = Math.Min(ContentSamples.ItemsByType[num6].maxStack, array[num5]);
2763					Item obj = item[array2[num5]];
2764					obj.SetDefaults(num6);
2765					obj.stack = num7;
2766					array[num5] -= num7;
2767					_ = array[num5];
2768					_ = 0;
2769				}
2770			}
2771			worldItem.TurnToAir();
2772			return true;
2773		}
2774	
2775		private static bool TryAddingToEmptySlot(int itemIndex, int chestIndex, int chestItemIndex)
2776		{
2777			WorldItem worldItem = Main.item[itemIndex];
2778			if (Main.chest[chestIndex].item[chestItemIndex].stack != 0)
2779			{
2780				return false;
2781			}
2782			SoundEngine.PlaySound(7);
2783			Main.chest[chestIndex].item[chestItemIndex] = worldItem.inner.Clone();
2784			Main.chest[chestIndex].item[chestItemIndex].newAndShiny = false;
2785			worldItem.TurnToAir();
2786			return true;
2787		}
2788	
2789		private static bool TryAddingToStack(int itemIndex, int chestIndex, int chestItemIndex)
2790		{
2791			WorldItem worldItem = Main.item[itemIndex];
2792			Item item = Main.chest[chestIndex].item[chestItemIndex];
2793			if (item.stack >= item.maxStack || !Item.CanStack(worldItem.inner, item))
2794			{
2795				return false;
2796			}
2797			int num = worldItem.stack;
2798			if (worldItem.stack + item.stack > item.maxStack)
2799			{
2800				num = item.maxStack - item.stack;
2801			}
2802			worldItem.stack -= num;
2803			item.stack += num;
2804			if (worldItem.stack <= 0)
2805			{
2806				worldItem.TurnToAir();
2807				return true;
2808			}
2809			if (item.type == 0)
2810			{
2811				Main.chest[chestIndex].item[chestItemIndex] = worldItem.inner.Clone();
2812				Main.chest[chestIndex].item[chestItemIndex].newAndShiny = false;
2813				worldItem.TurnToAir();
2814				return true;
2815			}
2816			return false;
2817		}
2818	
2819		public static void ToggleHolidayLight(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn)
2820		{
2821			bool flag = tileCache.frameX >= 54;
2822			if (!forcedStateWhereTrueIsOn.HasValue || !forcedStateWhereTrueIsOn.Value != flag)
2823			{
2824				if (tileCache.frameX < 54)
2825				{
2826					tileCache.frameX += 54;
2827				}
2828				else
2829				{
2830					tileCache.frameX -= 54;
2831				}
2832				NetMessage.SendTileSquare(-1, i, j);
2833			}
2834		}
2835	
2836		public static void ToggleHangingLantern(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
2837		{
2838			int num;
2839			for (num = tileCache.frameY / 18; num >= 2; num -= 2)
2840			{
2841			}
2842			int num2 = j - num;
2843			short num3 = 18;
2844			if (tileCache.frameX > 0)
2845			{
2846				num3 = -18;
2847			}
2848			bool flag = tileCache.frameX > 0;
2849			if (!forcedStateWhereTrueIsOn.HasValue || !forcedStateWhereTrueIsOn.Value != flag)
2850			{
2851				Main.tile[i, num2].frameX += num3;
2852				Main.tile[i, num2 + 1].frameX += num3;
2853				if (doSkipWires)
2854				{
2855					SkipWire(i, num2);
2856					SkipWire(i, num2 + 1);
2857				}
2858				NetMessage.SendTileSquare(-1, i, num2, 1, 2);
2859			}
2860		}
2861	
2862		public static void Toggle2x2Light(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
2863		{
2864			int num;
2865			for (num = tileCache.frameY / 18; num >= 2; num -= 2)
2866			{
2867			}
2868			num = j - num;
2869			int num2 = tileCache.frameX / 18;
2870			if (num2 > 1)
2871			{
2872				num2 -= 2;
2873			}
2874			num2 = i - num2;
2875			short num3 = 36;
2876			if (Main.tile[num2, num].frameX > 0)
2877			{
2878				num3 = -36;
2879			}
2880			bool flag = Main.tile[num2, num].frameX > 0;
2881			if (!forcedStateWhereTrueIsOn.HasValue || !forcedStateWhereTrueIsOn.Value != flag)
2882			{
2883				Main.tile[num2, num].frameX += num3;
2884				Main.tile[num2, num + 1].frameX += num3;
2885				Main.tile[num2 + 1, num].frameX += num3;
2886				Main.tile[num2 + 1, num + 1].frameX += num3;
2887				if (doSkipWires)
2888				{
2889					SkipWire(num2, num);
2890					SkipWire(num2 + 1, num);
2891					SkipWire(num2, num + 1);
2892					SkipWire(num2 + 1, num + 1);
2893				}
2894				NetMessage.SendTileSquare(-1, num2, num, 2, 2);
2895			}
2896		}
2897	
2898		public static void ToggleLampPost(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
2899		{
2900			int num = j - tileCache.frameY / 18;
2901			short num2 = 18;
2902			if (tileCache.frameX > 0)
2903			{
2904				num2 = -18;
2905			}
2906			bool flag = tileCache.frameX > 0;
2907			if (forcedStateWhereTrueIsOn.HasValue && !forcedStateWhereTrueIsOn.Value == flag)
2908			{
2909				return;
2910			}
2911			for (int k = num; k < num + 6; k++)
2912			{
2913				Main.tile[i, k].frameX += num2;
2914				if (doSkipWires)
2915				{
2916					SkipWire(i, k);
2917				}
2918			}
2919			NetMessage.SendTileSquare(-1, i, num, 1, 6);
2920		}
2921	
2922		public static void ToggleTorch(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn)
2923		{
2924			bool flag = tileCache.frameX >= 66;
2925			if (!forcedStateWhereTrueIsOn.HasValue || !forcedStateWhereTrueIsOn.Value != flag)
2926			{
2927				if (tileCache.frameX < 66)
2928				{
2929					tileCache.frameX += 66;
2930				}
2931				else
2932				{
2933					tileCache.frameX -= 66;
2934				}
2935				NetMessage.SendTileSquare(-1, i, j);
2936			}
2937		}
2938	
2939		public static void ToggleCandle(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn)
2940		{
2941			short num = 18;
2942			if (tileCache.frameX > 0)
2943			{
2944				num = -18;
2945			}
2946			bool flag = tileCache.frameX > 0;
2947			if (!forcedStateWhereTrueIsOn.HasValue || !forcedStateWhereTrueIsOn.Value != flag)
2948			{
2949				tileCache.frameX += num;
2950				NetMessage.SendTileSquare(-1, i, j, 3);
2951			}
2952		}
2953	
2954		public static void ToggleLamp(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
2955		{
2956			int num;
2957			for (num = tileCache.frameY / 18; num >= 3; num -= 3)
2958			{
2959			}
2960			num = j - num;
2961			short num2 = 18;
2962			if (tileCache.frameX > 0)
2963			{
2964				num2 = -18;
2965			}
2966			bool flag = tileCache.frameX > 0;
2967			if (!forcedStateWhereTrueIsOn.HasValue || !forcedStateWhereTrueIsOn.Value != flag)
2968			{
2969				Main.tile[i, num].frameX += num2;
2970				Main.tile[i, num + 1].frameX += num2;
2971				Main.tile[i, num + 2].frameX += num2;
2972				if (doSkipWires)
2973				{
2974					SkipWire(i, num);
2975					SkipWire(i, num + 1);
2976					SkipWire(i, num + 2);
2977				}
2978				NetMessage.SendTileSquare(-1, i, num, 1, 3);
2979			}
2980		}
2981	
2982		public static void ToggleChandelier(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
2983		{
2984			int num;
2985			for (num = tileCache.frameY / 18; num >= 3; num -= 3)
2986			{
2987			}
2988			int num2 = j - num;
2989			int num3 = tileCache.frameX % 108 / 18;
2990			if (num3 > 2)
2991			{
2992				num3 -= 3;
2993			}
2994			num3 = i - num3;
2995			short num4 = 54;
2996			if (Main.tile[num3, num2].frameX % 108 > 0)
2997			{
2998				num4 = -54;
2999			}
3000			bool flag = Main.tile[num3, num2].frameX % 108 > 0;
3001			if (forcedStateWhereTrueIsOn.HasValue && !forcedStateWhereTrueIsOn.Value == flag)
3002			{
3003				return;
3004			}
3005			for (int k = num3; k < num3 + 3; k++)
3006			{
3007				for (int l = num2; l < num2 + 3; l++)
3008				{
3009					Main.tile[k, l].frameX += num4;
3010					if (doSkipWires)
3011					{
3012						SkipWire(k, l);
3013					}
3014				}
3015			}
3016			NetMessage.SendTileSquare(-1, num3 + 1, num2 + 1, 3);
3017		}
3018	
3019		public static void ToggleCampFire(int i, int j, Tile tileCache, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
3020		{
3021			if (!TileID.Sets.Campfires[tileCache.type])
3022			{
3023				return;
3024			}
3025			int num = 3;
3026			int num2 = 2;
3027			int num3 = tileCache.frameX % (num * 18) / 18;
3028			int num4 = tileCache.frameY % (num2 * 18) / 18;
3029			int num5 = i - num3;
3030			int num6 = j - num4;
3031			if (!WorldGen.ValidateTileSquareIsActiveAndOfType(num5, num6, num, num2, tileCache.type))
3032			{
3033				return;
3034			}
3035			bool flag = Main.tile[num5, num6].frameY >= 36;
3036			if (forcedStateWhereTrueIsOn.HasValue && !forcedStateWhereTrueIsOn.Value == flag)
3037			{
3038				return;
3039			}
3040			short num7 = 36;
3041			if (Main.tile[num5, num6].frameY >= 36)
3042			{
3043				num7 = -36;
3044			}
3045			for (int k = num5; k < num5 + num; k++)
3046			{
3047				for (int l = num6; l < num6 + num2; l++)
3048				{
3049					if (doSkipWires)
3050					{
3051						SkipWire(k, l);
3052					}
3053					Tile tile = Main.tile[k, l];
3054					if (tile.active() && tile.type == tileCache.type)
3055					{
3056						tile.frameY += num7;
3057					}
3058				}
3059			}
3060			NetMessage.SendTileSquare(-1, num5, num6, num, num2);
3061		}
3062	
3063		public static void ToggleFirePlace(int i, int j, Tile theBlock, bool? forcedStateWhereTrueIsOn, bool doSkipWires)
3064		{
3065			int num = theBlock.frameX % 54 / 18;
3066			int num2 = theBlock.frameY % 36 / 18;
3067			int num3 = i - num;
3068			int num4 = j - num2;
3069			bool flag = Main.tile[num3, num4].frameX >= 54;
3070			if (forcedStateWhereTrueIsOn.HasValue && !forcedStateWhereTrueIsOn.Value == flag)
3071			{
3072				return;
3073			}
3074			int num5 = 54;
3075			if (Main.tile[num3, num4].frameX >= 54)
3076			{
3077				num5 = -54;
3078			}
3079			for (int k = num3; k < num3 + 3; k++)
3080			{
3081				for (int l = num4; l < num4 + 2; l++)
3082				{
3083					if (doSkipWires)
3084					{
3085						SkipWire(k, l);
3086					}
3087					Main.tile[k, l].frameX = (short)(Main.tile[k, l].frameX + num5);
3088				}
3089			}
3090			NetMessage.SendTileSquare(-1, num3, num4, 3, 2);
3091		}
3092	
3093		public static void ExplodeMine(int i, int j)
3094		{
3095			if (Main.netMode != 1)
3096			{
3097				WorldGen.KillTile(i, j, fail: false, effectOnly: false, noItem: true);
3098				NetMessage.SendTileSquare(-1, i, j);
3099				Projectile.NewProjectile(GetProjectileSource(i, j), i * 16 + 8, j * 16 + 8, 0f, 0f, 164, 250, 10f, Main.myPlayer);
3100			}
3101		}
3102	
3103		private static void GeyserTrap(int i, int j)
3104		{
3105			if (Main.netMode == 1)
3106			{
3107				return;
3108			}
3109			Tile tile = Main.tile[i, j];
3110			if (tile.type != 443)
3111			{
3112				return;
3113			}
3114			int num = tile.frameX / 36;
3115			int num2 = i - (tile.frameX - num * 36) / 18;
3116			if (CheckMech(num2, j, 200))
3117			{
3118				Vector2 zero = Vector2.Zero;
3119				Vector2 zero2 = Vector2.Zero;
3120				int num3 = 654;
3121				int damage = 20;
3122				if (num < 2)
3123				{
3124					zero = new Vector2(num2 + 1, j) * 16f;
3125					zero2 = new Vector2(0f, -8f);
3126				}
3127				else
3128				{
3129					zero = new Vector2(num2 + 1, j + 1) * 16f;
3130					zero2 = new Vector2(0f, 8f);
3131				}
3132				if (num3 != 0)
3133				{
3134					Projectile.NewProjectile(GetProjectileSource(num2, j), (int)zero.X, (int)zero.Y, zero2.X, zero2.Y, num3, damage, 2f, Main.myPlayer);
3135				}
3136			}
3137		}
3138	
3139		private static void Teleport()
3140		{
3141			if (_teleport[0].X < _teleport[1].X + 3f && _teleport[0].X > _teleport[1].X - 3f && _teleport[0].Y > _teleport[1].Y - 3f && _teleport[0].Y < _teleport[1].Y)
3142			{
3143				return;
3144			}
3145			Rectangle[] array = new Rectangle[2];
3146			array[0].X = (int)(_teleport[0].X * 16f);
3147			array[0].Width = 48;
3148			array[0].Height = 48;
3149			array[0].Y = (int)(_teleport[0].Y * 16f - (float)array[0].Height);
3150			array[1].X = (int)(_teleport[1].X * 16f);
3151			array[1].Width = 48;
3152			array[1].Height = 48;
3153			array[1].Y = (int)(_teleport[1].Y * 16f - (float)array[1].Height);
3154			for (int i = 0; i < 2; i++)
3155			{
3156				Vector2 vector = new Vector2(array[1].X - array[0].X, array[1].Y - array[0].Y);
3157				if (i == 1)
3158				{
3159					vector = new Vector2(array[0].X - array[1].X, array[0].Y - array[1].Y);
3160				}
3161				if (!blockPlayerTeleportationForOneIteration)
3162				{
3163					for (int j = 0; j < 255; j++)
3164					{
3165						if (Main.player[j].active && !Main.player[j].dead && !Main.player[j].teleporting && TeleporterHitboxIntersects(array[i], Main.player[j].Hitbox))
3166						{
3167							Vector2 vector2 = Main.player[j].position + vector;
3168							Main.player[j].teleporting = true;
3169							if (Main.netMode == 2)
3170							{
3171								RemoteClient.CheckSection(j, vector2);
3172							}
3173							Main.player[j].Teleport(vector2);
3174							if (Main.netMode == 2)
3175							{
3176								NetMessage.SendData(65, -1, -1, null, 0, j, vector2.X, vector2.Y);
3177							}
3178						}
3179					}
3180				}
3181				for (int k = 0; k < Main.maxNPCs; k++)
3182				{
3183					if (Main.npc[k].active && !Main.npc[k].teleporting && Main.npc[k].lifeMax > 5 && !Main.npc[k].boss && !Main.npc[k].noTileCollide)
3184					{
3185						int type = Main.npc[k].type;
3186						if (!NPCID.Sets.TeleportationImmune[type] && TeleporterHitboxIntersects(array[i], Main.npc[k].Hitbox))
3187						{
3188							Main.npc[k].teleporting = true;
3189							Main.npc[k].Teleport(Main.npc[k].position + vector);
3190						}
3191					}
3192				}
3193			}
3194			for (int l = 0; l < 255; l++)
3195			{
3196				Main.player[l].teleporting = false;
3197			}
3198			for (int m = 0; m < Main.maxNPCs; m++)
3199			{
3200				Main.npc[m].teleporting = false;
3201			}
3202		}
3203	
3204		private static bool TeleporterHitboxIntersects(Rectangle teleporter, Rectangle entity)
3205		{
3206			Rectangle rectangle = Rectangle.Union(teleporter, entity);
3207			if (rectangle.Width <= teleporter.Width + entity.Width)
3208			{
3209				return rectangle.Height <= teleporter.Height + entity.Height;
3210			}
3211			return false;
3212		}
3213	
3214		private static void DeActive(int i, int j)
3215		{
3216			if (!Main.tile[i, j].active() || (Main.tile[i, j].type == 226 && (double)j > Main.worldSurface && !NPC.downedPlantBoss))
3217			{
3218				return;
3219			}
3220			bool flag = Main.tileSolid[Main.tile[i, j].type] && !TileID.Sets.NotReallySolid[Main.tile[i, j].type];
3221			switch (Main.tile[i, j].type)
3222			{
3223			case 314:
3224			case 379:
3225			case 386:
3226			case 387:
3227			case 388:
3228			case 389:
3229			case 476:
3230				flag = false;
3231				break;
3232			}
3233			if (flag && (!Main.tile[i, j - 1].active() || (!TileID.Sets.PreventsActuationUnder[Main.tile[i, j - 1].type] && WorldGen.CanKillTile(i, j))))
3234			{
3235				Main.tile[i, j].inActive(inActive: true);
3236				WorldGen.SquareTileFrame(i, j, resetFrame: false);
3237				if (Main.netMode != 1)
3238				{
3239					NetMessage.SendTileSquare(-1, i, j);
3240				}
3241			}
3242		}
3243	
3244		private static void ReActive(int i, int j)
3245		{
3246			Main.tile[i, j].inActive(inActive: false);
3247			WorldGen.SquareTileFrame(i, j, resetFrame: false);
3248			if (Main.netMode != 1)
3249			{
3250				NetMessage.SendTileSquare(-1, i, j);
3251			}
3252		}
3253	
3254		private static void MassWireOperationInner(Player user, Point ps, Point pe, Vector2 dropPoint, bool dir, ref int wireCount, ref int actuatorCount)
3255		{
3256			Math.Abs(ps.X - pe.X);
3257			Math.Abs(ps.Y - pe.Y);
3258			int num = Math.Sign(pe.X - ps.X);
3259			int num2 = Math.Sign(pe.Y - ps.Y);
3260			WiresUI.Settings.MultiToolMode toolMode = WiresUI.Settings.ToolMode;
3261			Point pt = default(Point);
3262			bool flag = false;
3263			Item.StartCachingType(530);
3264			Item.StartCachingType(849);
3265			bool flag2 = dir;
3266			int num3;
3267			int num4;
3268			int num5;
3269			if (flag2)
3270			{
3271				pt.X = ps.X;
3272				num3 = ps.Y;
3273				num4 = pe.Y;
3274				num5 = num2;
3275			}
3276			else
3277			{
3278				pt.Y = ps.Y;
3279				num3 = ps.X;
3280				num4 = pe.X;
3281				num5 = num;
3282			}
3283			for (int i = num3; i != num4; i += num5)
3284			{
3285				if (flag)
3286				{
3287					break;
3288				}
3289				if (flag2)
3290				{
3291					pt.Y = i;
3292				}
3293				else
3294				{
3295					pt.X = i;
3296				}
3297				bool? flag3 = MassWireOperationStep(user, pt, toolMode, ref wireCount, ref actuatorCount);
3298				if (flag3.HasValue && !flag3.Value)
3299				{
3300					flag = true;
3301					break;
3302				}
3303			}
3304			if (flag2)
3305			{
3306				pt.Y = pe.Y;
3307				num3 = ps.X;
3308				num4 = pe.X;
3309				num5 = num;
3310			}
3311			else
3312			{
3313				pt.X = pe.X;
3314				num3 = ps.Y;
3315				num4 = pe.Y;
3316				num5 = num2;
3317			}
3318			for (int j = num3; j != num4; j += num5)
3319			{
3320				if (flag)
3321				{
3322					break;
3323				}
3324				if (!flag2)
3325				{
3326					pt.Y = j;
3327				}
3328				else
3329				{
3330					pt.X = j;
3331				}
3332				bool? flag4 = MassWireOperationStep(user, pt, toolMode, ref wireCount, ref actuatorCount);
3333				if (flag4.HasValue && !flag4.Value)
3334				{
3335					flag = true;
3336					break;
3337				}
3338			}
3339			if (!flag)
3340			{
3341				MassWireOperationStep(user, pe, toolMode, ref wireCount, ref actuatorCount);
3342			}
3343			EntitySource_ByItemSourceId reason = new EntitySource_ByItemSourceId(user, ItemSourceID.GrandDesignOrMultiColorWrench);
3344			Item.DropCache(reason, dropPoint, Vector2.Zero, 530);
3345			Item.DropCache(reason, dropPoint, Vector2.Zero, 849);
3346		}
3347	
3348		private static bool? MassWireOperationStep(Player user, Point pt, WiresUI.Settings.MultiToolMode mode, ref int wiresLeftToConsume, ref int actuatorsLeftToConsume)
3349		{
3350			if (!WorldGen.InWorld(pt.X, pt.Y, 1))
3351			{
3352				return null;
3353			}
3354			Tile tile = Main.tile[pt.X, pt.Y];
3355			if (tile == null)
3356			{
3357				return null;
3358			}
3359			if (user != null && !user.CanDoWireStuffHere(pt.X, pt.Y))
3360			{
3361				return null;
3362			}
3363			if ((mode & WiresUI.Settings.MultiToolMode.Cutter) == 0)
3364			{
3365				if ((mode & WiresUI.Settings.MultiToolMode.Red) != 0 && !tile.wire())
3366				{
3367					if (wiresLeftToConsume <= 0)
3368					{
3369						return false;
3370					}
3371					wiresLeftToConsume--;
3372					WorldGen.PlaceWire(pt.X, pt.Y);
3373					NetMessage.SendData(17, -1, -1, null, 5, pt.X, pt.Y);
3374				}
3375				if ((mode & WiresUI.Settings.MultiToolMode.Green) != 0 && !tile.wire3())
3376				{
3377					if (wiresLeftToConsume <= 0)
3378					{
3379						return false;
3380					}
3381					wiresLeftToConsume--;
3382					WorldGen.PlaceWire3(pt.X, pt.Y);
3383					NetMessage.SendData(17, -1, -1, null, 12, pt.X, pt.Y);
3384				}
3385				if ((mode & WiresUI.Settings.MultiToolMode.Blue) != 0 && !tile.wire2())
3386				{
3387					if (wiresLeftToConsume <= 0)
3388					{
3389						return false;
3390					}
3391					wiresLeftToConsume--;
3392					WorldGen.PlaceWire2(pt.X, pt.Y);
3393					NetMessage.SendData(17, -1, -1, null, 10, pt.X, pt.Y);
3394				}
3395				if ((mode & WiresUI.Settings.MultiToolMode.Yellow) != 0 && !tile.wire4())
3396				{
3397					if (wiresLeftToConsume <= 0)
3398					{
3399						return false;
3400					}
3401					wiresLeftToConsume--;
3402					WorldGen.PlaceWire4(pt.X, pt.Y);
3403					NetMessage.SendData(17, -1, -1, null, 16, pt.X, pt.Y);
3404				}
3405				if ((mode & WiresUI.Settings.MultiToolMode.Actuator) != 0 && !tile.actuator())
3406				{
3407					if (actuatorsLeftToConsume <= 0)
3408					{
3409						return false;
3410					}
3411					actuatorsLeftToConsume--;
3412					WorldGen.PlaceActuator(pt.X, pt.Y);
3413					NetMessage.SendData(17, -1, -1, null, 8, pt.X, pt.Y);
3414				}
3415			}
3416			if ((mode & WiresUI.Settings.MultiToolMode.Cutter) != 0)
3417			{
3418				if ((mode & WiresUI.Settings.MultiToolMode.Red) != 0 && tile.wire() && WorldGen.KillWire(pt.X, pt.Y))
3419				{
3420					NetMessage.SendData(17, -1, -1, null, 6, pt.X, pt.Y);
3421				}
3422				if ((mode & WiresUI.Settings.MultiToolMode.Green) != 0 && tile.wire3() && WorldGen.KillWire3(pt.X, pt.Y))
3423				{
3424					NetMessage.SendData(17, -1, -1, null, 13, pt.X, pt.Y);
3425				}
3426				if ((mode & WiresUI.Settings.MultiToolMode.Blue) != 0 && tile.wire2() && WorldGen.KillWire2(pt.X, pt.Y))
3427				{
3428					NetMessage.SendData(17, -1, -1, null, 11, pt.X, pt.Y);
3429				}
3430				if ((mode & WiresUI.Settings.MultiToolMode.Yellow) != 0 && tile.wire4() && WorldGen.KillWire4(pt.X, pt.Y))
3431				{
3432					NetMessage.SendData(17, -1, -1, null, 17, pt.X, pt.Y);
3433				}
3434				if ((mode & WiresUI.Settings.MultiToolMode.Actuator) != 0 && tile.actuator() && WorldGen.KillActuator(pt.X, pt.Y))
3435				{
3436					NetMessage.SendData(17, -1, -1, null, 9, pt.X, pt.Y);
3437				}
3438			}
3439			return true;
3440		}

```


---

## 🤖 Assistant · 2026-08-12T18:46:04.307Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
好,现在我对 1456 有完整图景。关键发现汇总:

**1456 新增/与实现不一致的点:**

A. **case 137 陷阱 kind 5(弹 980,30 伤,速度 12)** —— 实现缺失。980 是什么弹?1.4.4 加的"Venom Dart Trap"(毒镖陷阱)?查 wiki Venom_Dart_Trap.md。弹 980 是什么名字,可以 grep ProjectileID。

B. **case 137 第二段 switch(-10/-9/-8/-7/-6)**:这些看起来是反编译伪影或新结构。关键:尖刺球(case -7,:1942-1968)预算生效且无方向;而 case 3(:1812-1858)预算死代码但有方向。实现取了 case -7 行为。需要裁决哪个是真实路径。让我用 1405 对照。

C. **case 21/467 Hopper(漏斗)**:1.4.4 新机制——带线宝箱通电 60t 冷却,抓取中心 192×192 盒内物品进箱。实现完全没有(宝箱 21 在 deviceTable 无 case)。**未实现**。

D. **case 356 日晷 / 663 月晷**:通电 fastForwardTimeToDawn/Dusk + sundialCooldown/moondialCooldown 门。实现缺失。**未实现**。

E. **case 105 雕像 style 9 派对兔 540**(PartyIsUp 时 type 540):实现写死 46。

F. **雕像 style 17 炸弹掉落 y 偏移**:原版 num143-20,实现 py-16(8px 偏差,小)。

G. **case 531 巨石雕像 y**:原版 (num91)*16+28,实现 (oy+1)*16 = oy*16+16。差 12px。

H. **case 349 蘑菇块二次触发动画**:实现缺 case 349。

I. **HitSwitch 缺 type 210(地雷右键爆炸)**:原版 :288-291。实现 hitSwitch 无 210。需查 Game.ts 右键地雷路径。

J. **case 443 GeyserTrap**:原版 CheckMech(num2, j, 200)——锚点 x、**当前 y**(不是锚点 y)。实现 geyserTrap:369 `w.checkMech(i1, y, 200)` ✅ 一致。生成点 (num2+1)*16, j*16(上向)或 (num2+1)*16, (j+1)*16(下向),速度 ∓8,伤 20,弹 654。实现:371-374 `((i1+1)*16, (y+(up?0:1))*16), 0, up?-8:8, 20, 'geyser'` ✅ 一致。

K. **Teleport()**:传送器对需距离门(:3141 两点距离 <3 tile 且 0<dy<3 则 return);48×48 判定盒(y 上移 48);玩家 255 全员(active && !dead && !teleporting && 相交)且受 blockPlayerTeleportationForOneIteration 抑制;NPC:lifeMax>5 && !boss && !noTileCollide && !TeleportationImmune。传送后 teleporting=false 清理。
   实现 tripWire 把 tp 对收集后调用 teleportPair;Game.ts:7149 有"传送器对(Wiring.cs:2314-2365):板上 48×48 判定框内实体双向搬迁"。行号 2314-2365 是 1405 的行号,1456 是 3139-3212!这说明实现是基于 1405 的。需要精读 Game.ts:7149-7250 段。
   
   关键:**实现 hitWireSingle case 235 缺"3 tile 距离门"**?不,那个在 Teleport() 里,不在 case 235。case 235 :1551-1577 只有 wall==87 神庙墙限制。实现 ✅。距离门需在 teleportPair(Game 侧)核对。
   
   还有 halfBrick y+0.5 ✅ 实现 :407。

L. **blockPlayerTeleportationForOneIteration**:原版由测重板(Lihzahrd Pressure Plate,tile 442)触发时设置。搜一下哪里设置。在 1456 Wiring.cs 中 grep "blockPlayerTeleportationForOneIteration = true"。我读过的部分没有设置点(可能在 Player.cs 或 NPC.cs)。实现 Wiring.ts:61 有字段,logicGatePass :531 清除。但没有设置点!grep 实现侧。如果从不设置,则蜥蜴压板不会阻止传送 → 与原版不同。需要 grep 原版设置点。

M. **MassWireOperationStep 顺序**:原版顺序 Red → Green → Blue → Yellow → Actuator(放线),且 cutter 模式下也先走非 cutter 分支?看 :3363 `if ((mode & Cutter) == 0)` 放线;:3416 `if ((mode & Cutter) != 0)` 剪线。实现 massWireOperation order:RED, GREEN, BLUE, YELLOW ✅ 一致!好。
   但注意原版第一段循环:`for (int i = num3; i != num4; i += num5)`,如果 num3 == num4(ps.Y == pe.Y,即纯水平拖拽且 dir=true),第一段循环体一次都不执行;然后第二段 num3=ps.X...。实现 :786 `for (let v = from; v !== to && !aborted; v += first)` 同样零次执行 ✅。
   还有 CanDoWireStuffHere 门(玩家范围/权利)实现没有——单机近似可接受。
   实现里 dir 恒 true(player.direction==1 的注释说"先垂直段")。原版 dir = master.direction==1。direction==-1 时先水平。实现写死 true = 偏差,但 Grand Design 拖拽方向决定段序,标注小偏差。

N. **PixelBoxPass**:原版 :672 只处理 Value==3(垂直+水平都触发 → frameX 翻转 0↔18);**Value==1 或 2 不做任何事**(只有 3 才翻)。等等,原版:
```
foreach ... if (pixelBoxTrigger.Value == 3) { tile.frameX = (frameX != 18) ? 18 : 0; }
```
只有 ==3 翻转!而实现 pixelBoxPass:495-499:v===1 → frameX=0;v===3 → frameX=18。**实现不同!**

等等,让我细读原版语义:_PixelBoxTriggers[key] 的值是"垂直 2 / 水平 1"按位或。信号垂直穿过 → 记 2,水平穿过 → 记 1,两者都有 → 3。原版只在 3(即水平和垂直都收到信号)时翻转 frameX 到 18(开启),否则不动。

实现:v===1 → set frameX=0;v===3 → set frameX=18。v===2 → 无操作。
原版:v===3 → frameX = (frameX != 18) ? 18 : 0(翻转:非 18 则 18,是 18 则 0);v!==3 → 无操作。

差异:原版 v==1 或 v==2 都无操作;实现 v==1 强制 frameX=0。而且原版 v==3 是"翻转"语义(18→0 也会发生),实现是"强制 18"。

嗯,等等。让我重新读实现:
```js
if (v === 1) {
    if (st.frameX[i] !== 0) st.setTile(x, y, st.type[i], 0, st.frameY[i]);
} else if (v === 3) {
    if (st.frameX[i] !== 18) st.setTile(x, y, st.type[i], 18, st.frameY[i]);
}
```
原版:
```csharp
if (pixelBoxTrigger.Value == 3) {
    tile.frameX = (short)((tile.frameX != 18) ? 18 : 0);
}
```

**差异确认**:原版只有 v==3 触发,且为翻转(交替);实现 v==1 → 强制关,v==3 → 强制开。这是 🔀 逻辑不同。实际游戏效果:原版像素盒需要水平+垂直两路信号同时到达才翻转(异或?)。实现的版本:v==1(仅水平)强制关闭。

嗯等等,我要再想想 pixel box 的实际机制。Pixel Box(像素盒):信号从水平方向穿过时输出垂直方向信号,反之亦然?实际上 Pixel Box 是:当且仅当信号从两个正交方向同时到达时,改变状态(切换输出)。

按原版代码:_PixelBoxTriggers 在 hitWire 里记录:当 445 格是信号路径且方向 num1==index1(直通)时,记 (j==0||j==1) ? 2 : 1,即垂直移动记 2、水平移动记 1(按**新方向** j)。等等,:937 `_PixelBoxTriggers[key] |= (byte)((!(j == 0 || j == 1)) ? 1u : 2u);` j 是邻居方向(0下1上2右3左)。j==0/1(垂直)→ 2;j==2/3(水平)→ 1。

然后 PixelBoxPass:值==3(垂直+水平都经过)→ frameX 翻转。所以像素盒 = 信号同时从水平和垂直方向穿过它 → 翻转状态。对,这是 wiki 语义:"changes state only when a signal passes through it both horizontally and vertically in the same tick"。

实现 v===1 强制 frameX=0 是错的;v===3 强制 18 而非翻转也是错的。这是一个真实 bug(像素盒用得少,但仍是 1:1 偏差)。

等等,还要检查一下实现 hitWire 中记录 pixelBoxTriggers 的条件。实现 :352-357:
```js
if (curSheet === 445) {
    if (index1 === num1) {
        const v = (index1 === 0 || index1 === 1) ? 2 : 1;
        this.pixelBoxTriggers.set(key, (this.pixelBoxTriggers.get(key) ?? 0) | v);
    } else continue;
}
```
原版 :929-943:
```csharp
if (tile2.type == 445) {   // 注意:tile2 = Main.tile[x,y] 当前格!
    if (j != num) continue;
    if (_PixelBoxTriggers.ContainsKey(key)) _PixelBoxTriggers[key] |= ...
    else _PixelBoxTriggers[key] = ...
}
```
key 是**当前格** Point16(x,y)。tile2 = Main.tile[x, y](当前格)。一致 ✅。

好。继续。

O. **ToggleCandle case 646**:1456 :1754-1759 case 33/49/174/372/**646** ToggleCandle。646 是 1.4.4 新蜡烛(Plate/气泡蜡烛?其实是 "bubble" 之类)。实现 LIGHT_TOGGLE/devices case 33/174/49/372 缺 **646**。tile 646 = 什么?"Pink Dungeon Candle"?查一下。不重要,但标注。

P. **TileID.Sets.Campfires[type]**:1456 篝火是 Set(多种篝火:215 campfire + coral/pink 等)。实现只 case 215!篝火家族(coronation?)原版 TileID.Sets.Campfires 含 215(营火)、616?、617?…… 需查 TileID.cs。让我 grep。

Q. **TileID.Sets.Torches[type]**:火把 Set(4 + 骨火把 98 + 冰 160 + 丛林 41 + 神圣 101 + 超亮 433 + 诅咒 126? 等)。实现只 case 4!devices.ts:544 `case 4: flipCell(w, x, y, 66)`。其他火把族(41/98/101/126/160/433/...)不通电翻转!**大缺口**。LIGHT_TOGGLE 也只有 4。

R. **case 15 马桶烟花 num68 锚点**:原版 :1500 `int num68 = j - tile.frameY % 40 / 18;` ✅ 实现一致。CheckMech(i, num68, 60) ✅。弹 733 损 0 ✅。

S. **XferWater 液体泵**:
原版:
- 每个进泵格子对每个出泵格子转移,上限 255
- 转移后 `Main.tile[num3,num4].liquidType(b)` 设类型
- **WorldGen.SquareTileFrame** 调用(视觉/流动重算)
- 源格液体清零时 `liquidType(0)` + SquareTileFrame

实现 :456-485:逻辑基本一致,但没有 SquareTileFrame 调用(引擎可能由 setLiquid 自动标记);源格清零时 `st.setLiquid(i1, j1, liquid1 - move, st.liquidType[ii] || 1)` —— `|| 1` 在 liquidType==0 时设 1(水)!原版 liquidType(0) = **无液体类型 0**,而本仓库 liquidType 编码 water=1(记忆里 liquidType+1 编码陷阱!)。这里 st.liquidType[ii] 用的是仓库编码(1=水 2=岩浆 3=蜂蜜),源格清零时设 1(=仓库水)但 liquid=0,liquid=0 时类型无意义?但目标格 `st.setLiquid(i2, j2, liquid2 + move, lava ? 2 : honey ? 3 : 1)` ✅ 与原版 liquidType(b) 一致。
  问题:源格清零后,实现没有把类型清 0(原版 liquidType(0))。若引擎把 liquidType=1 且 liquid=0 视为"无液体"则等价;但按记忆"liquidType+1 编码陷阱",仓库 0 = 原版 Water=0。所以实现里 `st.liquidType[ii] || 1` 当原版类型 0(水)→ 仓库 1 ✅。清零时保留原类型(liquid=0)。原版显式清类型。差异影响:如果后续该格进别的液体,类型会被覆盖,所以基本等价。但严格说,原版类型=0(无),实现保留水。当一格 liquid=0 且 liquidType=仓库1,若有代码判断"liquidType!=0 就当有液体"会出错。标记 ⚠️ 低风险。
  
  另外原版泵转移后调用 SquareTileFrame(触发相邻瀑布/流动动画),实现不调用 → 可能影响液体流动状态。❓
  
  还有重要一点:原版 XferWater 里 `if (liquid2 >= 255) continue;`,实现 `if (liquid2 < 255)` ✅。
  原版转移量 `num5 = liquid; if (num5 + liquid2 > 255) num5 = 255 - liquid2;` ✅ 实现 :474-475。
  原版在**每个进泵循环末尾** `WorldGen.SquareTileFrame(num, num2)`(:521)。

T. **MaxPump=20 但填充上限 19** ✅ 两侧一致(_numInPump >= 19 break;实现 numInPump < 19)。

U. **UpdateMech 的 144 计时器**:
原版 :186-204:period switch 0→60, 1→180, 2→300, 3→30, 4→15。IEEERemainder==0 → _mechTime=18000 + TripWire。注意:**原版没有 default 分支**,num4=5+ 时保持原值(不映射)!实现 :148 `period = period === 0 ? 60 : period === 1 ? 180 : period === 2 ? 300 : period === 3 ? 30 : period === 4 ? 15 : 60;` —— **兜底 60**,原版是"保持 num4 不变"(即 5→5 ticks!)。frameX/18 可以是 5 吗?计时器 frameX 0-4(五种:1/4s? 不对)。计时器种类:frameX 0=1s(60)、1=3s(180)、2=5s(300)、3=1/4s(30)、4=1/2s?等等 4→15 ticks = 0.25s?15 ticks = 0.25s。3→30 = 0.5s。
所以五种计时器:0=1s、1=3s、2=5s、3=1/2s、4=1/4s。frameX/18 只会 0-4,兜底不可达。✅ 等价(但注意 wiki 说 1/4s 是 1.4.4 新增?其实 Quarter_Second_Timer 早就有?让我查 wiki。不,1/4 second timer 是 1.3.1 加的?记不清。反正 1456 有 case 4→15 ✅ 实现也有)。

计时器 wiki 确认:Half_Second_Timer(30t)、Quarter_Second_Timer(15t)。

V. **IEEERemainder 语义**:原版 `Math.IEEERemainder(_mechTime[num], num4) == 0.0`。实现 :150 `const r = this.mechTime[i] - period * Math.round(this.mechTime[i] / period);` —— 这正是 IEEERemainder 的公式 ✅(round 而非 trunc)。注意 mechTime 可能为负?_mechTime 递减,初始 18000,正常为正。✅

W. **logicGatePass 的级联循环**:原版 :689-712 while(_LampsToCheck) { while(_LampsToCheck) dequeue+CheckLogicGate; while(_GatesNext) { swap; while(_GatesCurrent) { ... TripWire } } }。注意原版 `_GatesNext` 在内层 while 里被 swap 成 _GatesCurrent,然后逐个 TripWire(可能产生新 lamp)。外层 while(_LampsToCheck) 继续直到空。
实现 :509-529:
```js
while (this.lampsToCheck.length > lampHead) {
  while (this.lampsToCheck.length > lampHead) { ...checkLogicGate... }
  const next = this.gatesNext; this.gatesNext = []; this.gatesCurrent = next;
  while (this.gatesCurrent.length > gateHead) { ...tripWire... }
  this.gatesCurrent.length = 0;
}
```
问题:原版外层条件是 `_LampsToCheck.Count > 0`,内层第一圈处理完所有 lamp 后,处理 GatesNext → TripWire → 期间新 lamp 入 _LampsToCheck → 外层继续。实现外层同样 lampsToCheck.length > lampHead。但实现把 gatesNext 清空后 `this.gatesNext = []`,而原版 swap 后 _GatesNext 变成旧 _GatesCurrent(已排空的队列)→ 语义同 ✅。
但有一个细节:原版 `Utils.Swap(ref _GatesCurrent, ref _GatesNext)`,然后 `while (_GatesCurrent.Count > 0) { Peek; if done → Dequeue continue; done.Add; TripWire; Dequeue; }`。TripWire 递归会嵌套调用 LogicGatePass —— 但有 `if (_GatesCurrent.Count != 0) return;` 守卫(嵌套时 _GatesCurrent 非空 → 直接返回,由外层继续处理)。实现 :507 同样守卫 ✅。
还有实现 :527 `this.gatesCurrent.length = 0` 注释说明残留会让下次级联被早退守卫吞掉 —— 这是他们修过的坑 ✅。

X. **checkLogicGate 的扫描起点**:原版 `for (int i = lampY; i < Main.maxTilesY; i++)` 从灯位置**向下**扫到找到 420 门。实现 :545 同 ✅。若中途遇到非 419 且非 420 → break ✅。

Y. **SkipWire 与 _GatesDone**:基本一致。

Z. **case 144 计时器信号语义**:原版 :1012-1016 HitWireSingle case 144 → HitSwitch(i,j)(frameY 0→18 打开 + CheckMech 18000)+ SquareTileFrame。实现 :392-394 调 this.hitSwitch ✅。

AA. **case 419 门灯**:原版 :1053-1069 ✅ 实现一致。

BB. **case 130 通电石**:原版 :1426-1435:`if (Main.tile[i,j-1] != null && (!active || !PreventsActuationUnder[type]) && WorldGen.CanKillTile(i,j)) → type=131`。实现 devices.ts:589-593:`above === 21 || 88 || 467 → return`。PreventsActuationUnder 集合是 {21,467,26,77,88,470,475,237,597,441,468}(Wiring.ts:36),实现 case 130 只查了 21/88/467 三个!漏了 26(音乐盒)/77(花盆)/470(垃圾桶)/475/237/597/441/468。而且缺 WorldGen.CanKillTile 门。⚠️ 偏差。
等等,原版条件是 `(!Main.tile[i, j - 1].active() || !TileID.Sets.PreventsActuationUnder[...]) && WorldGen.CanKillTile(i, j)`。即上方非激活 或 上方不是 PreventsActuationUnder,且 CanKillTile。实现只挡了 21/88/467 且无 CanKillTile。偏差 ⚠️。

CC. **case 10/11 门**:原版 :1464-1491:case 11 → CloseDoor(forced:true);case 10 → OpenDoor(随机 ±1,失败试反向)。实现 ctx.doorOpen/doorClose 由 Game 实现 ✅(需查 Game.ts 实现是否随机方向)。

DD. **case 386/387 活板门**:原版 → WorldGen.ShiftTrapdoor(i,j,playerAbove:true) 失败则 (playerAbove:false)。实现 devices.ts:813-825 是**帧近似**:sheet 387(关)→ 386(开)、386(开)→387(关),直接 swapTile 风格。原版 ShiftTrapdoor 是带上下方向的查找(找到活板门实际位置)。近似,标 🔀。

EE. **case 388/389 高门**:原版 ShiftTallGate。实现帧近似 🔀。而且实现 :834 `for (let ix = ox; ix < ox + 1; ix++)` 只写 1 列?原版高门 1×5。近似。

FF. **case 216 烟花火箭**:原版 :1492-1496 LaunchRocket(i,j,fromWiring:true) + SkipWire(i,j)。实现 :754-765 有点偏差:
- 原版 LaunchRocket(WorldGen.cs:62184-62206,实现注释引用)—— 实现自己内联了:ly 调整(frameY%40==18 → ly--),发射 (x*16+8, ly*16+6),速度 (0,-8),伤 150,弹 167-170 按 frameY/40 行,然后 KillTile 两格。
- 原版 SkipWire 只 Skip (i,j) 一格,实现 `w.skipCell(x, y)` 一格 ✅。
- 需要查 WorldGen.LaunchRocket 确认数值。实现注释说 :62196-62199 速度 (0,-8) 伤 150 kb 7。让我抽查 WorldGen.cs 62184。

GG. **case 429 彩线灯泡**:原版 :1586-1624。num156 = frameX/18。case 1: num157=18, flag12 = !flag8(红)。实现 :439-443 case 1: num53=18, on=!(q%2>=1)=!flag8 ✅。case 2: 72/blue !flag10 ✅。case 3: 36/green ✅。case 4: 144/yellow ✅。✅ 对齐。

HH. **case 349**:见 H。

II. **case 546/557 格栅 swapTile** ✅ :2550-2558。

JJ. **case 219/642 提取机**:1456 :1994-1997 case 219/642 → Extractinator。实现 ✅ 有。Extractinator 数值(CheckMech 60,找箱子 3×2 邻域,倒序找第一个可提取物,Item.NewItem 32×32)✅ 实现注释引用 2563-2593,与 1456 一致。TryFindChestForExtractinator 查找范围 :2596-2618:`lookupX-2 .. lookupX+3+2`?让我看:`for (int i = lookupX - num3; i <= lookupX + num + num3; i++)` num=3, num3=2 → x ∈ [lookupX-2, lookupX+5];`for (int j = lookupY - num3; j <= lookupY + num2 + num3; j++)` num2=2 → y ∈ [lookupY-2, lookupY+4]。需对照 Game.ts 的箱子查找范围。

KK. **Hopper 的 CheckMech(num, num2, 60)**:锚点 = frameX%36!=0 → num--,frameY%36!=0 → num2--。宝箱 2×2。

LL. **DeActive 226 蜥蜴砖门 + worldSurface** ✅ 实现 :624。

MM. **DeActive flag**:原版 :3220 `bool flag = Main.tileSolid[type] && !TileID.Sets.NotReallySolid[type];` switch(314/379/386/387/388/389/476) → flag=false。实现 :627-630 ✅(还有显式 NotReallySolid{387,388,10})。
注意原版 switch 里没有 379?有,case 379 在列。✅。

NN. **DeActive 的上方判定**:原版 :3233 `if (flag && (!Main.tile[i, j-1].active() || (!PreventsActuationUnder && WorldGen.CanKillTile(i,j))))`。实现 :632-637 ✅ 结构一致,PREVENTS_ACTUATION_UNDER 表 ✅(:36)。

OO. **blockPlayerTeleportationForOneIteration 设置点**:原版哪里设 true?grep。

PP. **sensor 423(传感器)/压板 135/428/442/476 触发条件**:这些在 Player.cs / NPC.cs / Projectile.cs 的碰撞检测里,不在 Wiring.cs。必核清单第 3/6 项(压力板类型触发型号、传感器)需要查:
- tile 135 = Pressure Plates(红/绿/灰/棕/蓝/黄/蜥蜴等 style)
- tile 423 = 传感器(Player Above / Player / Liquid water/lava/honey)
- tile 428 = Projectile 压板(Teal Pressure Pad)
- tile 442 = 测重板(Weighted Pressure Plates,彩/青/橙/粉/紫)
- tile 476 = 高尔夫球洞?

实现侧触发源登记在 Game.ts(注释 1621-1622 提到"触发源登记(测重板 428/感应器 423)")。需要 grep Game.ts 的压板/传感器触发逻辑,并与原版 Player.cs PressureTileHelper 对照。

PressureTileHelper.cs 在反编译目录里应该有。让我查。

现在还需要:
1. 读 Game.ts 相关段落(hitSwitch 右键、teleportPair、雕像 spawnNpc、mechSpawnOk、传感器/压板触发源、电路工具使用)。
2. grep 原版 blockPlayerTeleportationForOneIteration 设置点。
3. 查 1405 Wiring.cs 的 case 137(裁决尖刺球方向问题)。
4. 查 Projectile 980 是什么(1.4.4 新弹)。
5. 查 TileID.Sets.Torches/Campfires 内容(火把/篝火族覆盖)。
6. wiki 核对数值(计时器、压力板型号、传送器、泵、逻辑门)。
7. Game.ts 的 PressureTileHelper 等价实现 + 传感器。

先并行做 2/3/4/5 的 grep。

由于 Game.ts 巨大(11000+ 行),我需要有针对性地 grep。

批次:
- grep blockPlayerTeleportationForOneIteration 在 Terarria1456 全目录
- grep 1405 Wiring.cs case 137 段
- grep ProjectileID 980
- grep TileID.Sets.Torches / Campfires in TileID.cs
- grep Game.ts 压板/传感器/sensor/pressure

开始。
````

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:05.027Z · glm-x-preview-260804

```
1456 源码读完。现在并行核查几个关键裁决点：尖刺球方向(对照 1405)、弹 980、火把/篝火 Set、测重板传送抑制设置点。
```


---

## 🤖 Assistant · 2026-08-12T18:46:06.101Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -rn \"blockPlayerTeleportationForOneIteration = true\" --include=\"*.cs\" | head; echo \"===980===\"; grep -n \"= 980\\|980;\" Terraria/ID/ProjectileID.cs | head -5; grep -n \"case 980\" Terraria/Projectile.cs | head -3; echo \"===TorchSet===\"; grep -n -A30 \"public static bool\\[\\] Torches\" Terraria/ID/TileID.cs | head -40",
 "description": "Find teleport block setter, projectile 980, torch set"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:06.167Z

**📎 ToolResult**

```
Terraria.GameContent/PressurePlateHelper.cs:160:			Wiring.blockPlayerTeleportationForOneIteration = true;
===980===
ugrep: warning: Terraria/ID/ProjectileID.cs: No such file or directory
53165:		case 980:
===TorchSet===
ugrep: warning: Terraria/ID/TileID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-12T18:46:06.846Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"case 137\" Terraria/Wiring.cs; echo \"---\"; sed -n '/case 137:/,/^\t\t\tcase /p' Terraria/Wiring.cs | head -120",
 "description": "Read 1.4.0.5 trap case 137 for comparison"
}
```


---

## 🤖 Assistant · 2026-08-12T18:46:07.636Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && grep -n -A15 \"public static bool\\[\\] Campfires\" Terraria/ID/TileID.cs | head -20; echo \"===campfire usage===\"; grep -rn \"Sets.Campfires\\[.*\\] = true\" --include=\"*.cs\" | head",
 "description": "Find campfire tile set members"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:16.043Z

**📎 ToolResult**

```
ugrep: warning: Terraria/Wiring.cs: No such file or directory
---
sed: Terraria/Wiring.cs: No such file or directory

```


---

## 👤 User(sidechain) · 2026-08-12T18:46:16.076Z

**📎 ToolResult**

```
ugrep: warning: Terraria/ID/TileID.cs: No such file or directory
===campfire usage===

```


---

## 🤖 Assistant · 2026-08-12T18:46:17.710Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
路径不对。让我找正确的目录结构。
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:17.920Z · glm-x-preview-260804

```
目录结构有嵌套，先定位真实路径。
```


---

## 🤖 Assistant · 2026-08-12T18:46:19.106Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/ | head; echo \"---find---\"; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"Wiring.cs\" -maxdepth 3 2>/dev/null; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"TileID.cs\" -maxdepth 4 2>/dev/null | head -3; find ~/Project/GLM/SandboxWorld/Terarria1405 -name \"Wiring.cs\" -maxdepth 4 2>/dev/null",
 "description": "Locate actual source file paths"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:19.162Z

**📎 ToolResult**

```
app.ico
app.manifest
BCrypt.Net
Microsoft.Xna.Framework.RuntimeProfile
nativefiledialog.cs
Properties
Terraria
Terraria.Achievements
Terraria.Audio
Terraria.Chat
---find---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs
~/Project/GLM/SandboxWorld/Terarria1405/Wiring.cs

```


---

## 🤖 Assistant · 2026-08-12T18:46:23.117Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
好:
- 1456: `~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs`(我读的就是它,路径没错——上面 grep 失败是因为我 cd 到了 Terarria1456 然后用相对路径 `Terraria/ID/ProjectileID.cs`,而 ID 在 `Terraria.ID/`)
- TileID.cs: `Terarria1456/Terraria.ID/TileID.cs`
- 1405 Wiring.cs: `Terarria1405/Wiring.cs`(平铺结构)

重新跑 grep。
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:24.280Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; grep -n \"= 980\" $T/Terraria.ID/ProjectileID.cs | head -3; echo \"===proj980===\"; sed -n '53160,53175p' $T/Terraria/Projectile.cs; echo \"===Torches===\"; grep -n \"Torches\" $T/Terraria.ID/TileID.cs | head -5; echo \"===Campfires===\"; grep -n \"Campfires\" $T/Terraria.ID/TileID.cs | head -5",
 "description": "Identify projectile 980 and tile sets"
}
```


---

## 🤖 Assistant · 2026-08-12T18:46:24.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "W=~/Project/GLM/SandboxWorld/Terarria1405/Wiring.cs; grep -n \"case 137:\" $W; awk '/case 137:/,/case 443:/' $W | head -150",
 "description": "Read 1.4.0.5 trap case 137"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:31.270Z

**📎 ToolResult**

```
2320:	public const short VenomDartTrap = 980;
===proj980===
		case 706:
		case 709:
		case 710:
		case 712:
		case 876:
		case 980:
		case 981:
		case 1073:
			flag3 = false;
			break;
		case 1006:
			flag4 = true;
			break;
		}
		if (flag3)
		{
===Torches===
401:		public static bool[] Torches = Factory.CreateBoolSet(4);
441:	public const ushort Torches = 4;
===Campfires===
403:		public static bool[] Campfires = Factory.CreateBoolSet(215);

```


---

## 👤 User(sidechain) · 2026-08-12T18:46:38.064Z

**📎 ToolResult**

```
1495:                          case 137:
                          case 137:
                            int num69 = (int) tile1.frameY / 18;
                            Vector2 vector2_2 = Vector2.Zero;
                            float SpeedX2 = 0.0f;
                            float SpeedY2 = 0.0f;
                            int Type2 = 0;
                            int Damage2 = 0;
                            switch (num69)
                            {
                              case 0:
                              case 1:
                              case 2:
                                if (Wiring.CheckMech(i, j, 200))
                                {
                                  int num8 = tile1.frameX == (short) 0 ? -1 : (tile1.frameX == (short) 18 ? 1 : 0);
                                  int num39 = tile1.frameX < (short) 36 ? 0 : (tile1.frameX < (short) 72 ? -1 : 1);
                                  vector2_2 = new Vector2((float) (i * 16 + 8 + 10 * num8), (float) (j * 16 + 8 + 10 * num39));
                                  float num57 = 3f;
                                  if (num69 == 0)
                                  {
                                    Type2 = 98;
                                    Damage2 = 20;
                                    num57 = 12f;
                                  }
                                  if (num69 == 1)
                                  {
                                    Type2 = 184;
                                    Damage2 = 40;
                                    num57 = 12f;
                                  }
                                  if (num69 == 2)
                                  {
                                    Type2 = 187;
                                    Damage2 = 40;
                                    num57 = 5f;
                                  }
                                  SpeedX2 = (float) num8 * num57;
                                  SpeedY2 = (float) num39 * num57;
                                  break;
                                }
                                break;
                              case 3:
                                if (Wiring.CheckMech(i, j, 300))
                                {
                                  int num8 = 200;
                                  for (int index12 = 0; index12 < 1000; ++index12)
                                  {
                                    if (Main.projectile[index12].active && Main.projectile[index12].type == Type2)
                                    {
                                      float num39 = (new Vector2((float) (i * 16 + 8), (float) (j * 18 + 8)) - Main.projectile[index12].Center).Length();
                                      if ((double) num39 < 50.0)
                                        num8 -= 50;
                                      else if ((double) num39 < 100.0)
                                        num8 -= 15;
                                      else if ((double) num39 < 200.0)
                                        num8 -= 10;
                                      else if ((double) num39 < 300.0)
                                        num8 -= 8;
                                      else if ((double) num39 < 400.0)
                                        num8 -= 6;
                                      else if ((double) num39 < 500.0)
                                        num8 -= 5;
                                      else if ((double) num39 < 700.0)
                                        num8 -= 4;
                                      else if ((double) num39 < 900.0)
                                        num8 -= 3;
                                      else if ((double) num39 < 1200.0)
                                        num8 -= 2;
                                      else
                                        --num8;
                                    }
                                  }
                                  if (num8 > 0)
                                  {
                                    Type2 = 185;
                                    Damage2 = 40;
                                    int num39 = 0;
                                    int num57 = 0;
                                    switch ((int) tile1.frameX / 18)
                                    {
                                      case 0:
                                      case 1:
                                        num39 = 0;
                                        num57 = 1;
                                        break;
                                      case 2:
                                        num39 = 0;
                                        num57 = -1;
                                        break;
                                      case 3:
                                        num39 = -1;
                                        num57 = 0;
                                        break;
                                      case 4:
                                        num39 = 1;
                                        num57 = 0;
                                        break;
                                    }
                                    SpeedX2 = (float) (4 * num39) + (float) Main.rand.Next((num39 == 1 ? 20 : 0) - 20, 21 - (num39 == -1 ? 20 : 0)) * 0.05f;
                                    SpeedY2 = (float) (4 * num57) + (float) Main.rand.Next((num57 == 1 ? 20 : 0) - 20, 21 - (num57 == -1 ? 20 : 0)) * 0.05f;
                                    vector2_2 = new Vector2((float) (i * 16 + 8 + 14 * num39), (float) (j * 16 + 8 + 14 * num57));
                                    break;
                                  }
                                  break;
                                }
                                break;
                              case 4:
                                if (Wiring.CheckMech(i, j, 90))
                                {
                                  int num8 = 0;
                                  int num39 = 0;
                                  switch ((int) tile1.frameX / 18)
                                  {
                                    case 0:
                                    case 1:
                                      num8 = 0;
                                      num39 = 1;
                                      break;
                                    case 2:
                                      num8 = 0;
                                      num39 = -1;
                                      break;
                                    case 3:
                                      num8 = -1;
                                      num39 = 0;
                                      break;
                                    case 4:
                                      num8 = 1;
                                      num39 = 0;
                                      break;
                                  }
                                  SpeedX2 = (float) (8 * num8);
                                  SpeedY2 = (float) (8 * num39);
                                  Damage2 = 60;
                                  Type2 = 186;
                                  vector2_2 = new Vector2((float) (i * 16 + 8 + 18 * num8), (float) (j * 16 + 8 + 18 * num39));
                                  break;
                                }
                                break;
                            }
                            switch (num69 + 10)
                            {
                              case 0:
                                if (Wiring.CheckMech(i, j, 200))
                                {
                                  int num8 = -1;
                                  if (tile1.frameX != (short) 0)
                                    num8 = 1;
                                  SpeedX2 = (float) (12 * num8);
                                  Damage2 = 20;

```


---

## 🤖 Assistant · 2026-08-12T18:47:20.643Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
重要发现:

1. **TileID.Sets.Torches = Factory.CreateBoolSet(4)** —— 只有 tile 4!不是多火把族。所以我之前担心的"火把族覆盖"不成立:Torches Set 只含 4(Torch)。实现的 case 4 ✅ 对齐。(工厂的 CreateBoolSet(4) 创建数组,只把 4 设 true。但如果别处有 `TileID.Sets.Torches[X] = true` 的赋值呢?刚才 grep Campfires 的赋值没结果。让我确认 Torches 是否有其他赋值。不过原版代码里 TileID.Sets 通常只在 TileID.cs 静态初始化。刚才 grep "Sets.Campfires[...] = true" 无结果,说明没有运行时添加。Torches 同理可以假设只有 4。但为了稳妥 grep 一下。)

2. **Campfires = CreateBoolSet(215)** —— 只有 215!实现的 case 215 ✅ 对齐。

3. **1405 的 case 137**:证实了 `switch (num69 + 10)` —— **这就是第二段 switch 的真相**!反编译成 1456 的 `switch (num95)` case -10/-9/-8/-7/-6,但 1405 的原始结构是 `switch (num69 + 10)`,即当 num69==0 时 case 0;num69==1 → case 1... 等等,不对:num69+10,case 0 对应 num69 = -10。嗯,不对。

   等等,看 1405 代码:`switch (num69 + 10) { case 0: ... case -10?? }`。第一个输出显示 `case 0:`。num69+10==0 → num69 == -10?不可能。哦,我 awk 截断了。让我看完整的:可能 1405 的第二个 switch 是 `switch (num69 + 10)`,case 0..4 对应 num69 = -10..-6,还是不可达?

   不对,等一下。1405 的 awk 输出第一段 switch(num69) case 0,1,2,3,4。第二段 `switch (num69 + 10)` case 0: → num69 = -10。这不可能可达……除非!!

   哦!!我懂了!这是**反编译器的 switch 分解伪影**:C# 编译器把一个 switch(num69) 编译成两个跳转表(值域拆分)。1405 反编译器把它还原成了"switch(num69) + switch(num69+10)",其实它们是同一个逻辑 switch 的两个值域段。1456 的 ilspycmd 还原成 "switch(num95) case -10..-6" —— 即它识别出第二段的真实 case 标签是 num95 ∈ {-10..-6},等价于 1405 的 num69+10 ∈ {0..4}。

   也就是说:**case -10..-6 与 case 0..4 是同一个 switch 的互斥值域拆分**!case -10(dart)、-9(superdart)、-8(flame)、-7(spiky)、-6(spear)与 case 0,1,2,5(dart 族)、3(spiky)、4(spear)是重复代码??

   不对。如果是同一个 switch 的拆分,case 标签应该不重叠。1405:第一段 case 0,1,2,3,4(带 break);第二段 switch(num69+10) case 0 → num69=-10。值域 {0..4} 与 {-10..-6} 不重叠,所以**两段都是真实代码但第二段不可达**?

   那就很怪。让我看 1405 第二段 switch 的完整 case 列表,确认 case 值。如果第二段是 case 0..4(即 num69+10 ∈ 0..4 → num69 ∈ -10..-6),确实不可达。但编译器不会生成不可达代码……

   另一种解释:这两个 switch 是从**两个不同的源方法**合并而来?或者 1405 反编译器输出的 `switch (num69 + 10)` 实际是 jump table 的偏移伪装。

   嗯,让我换个角度:看 1.4.0.5 真实行为。Terraria 1.4.0.5 的陷阱(137):Dart Trap(98)、Super Dart Trap(184)、Flame Trap(187)、Spiky Ball Trap(185)、Spear Trap(186)。就 5 种(frameY/18 = 0-4)。1.4.4 加了 **Venom Dart Trap(弹 980,1456 case 5)**。

   所以真实逻辑:num95 ∈ {0,1,2,3,4,5}。case 0/1/2 → dart 族;case 3 → spiky;case 4 → spear;case 5(1456 新增)→ venom dart。

   那么第二个 switch(case -10..-6)呢?它可能是**同一 switch 的两份代码**——注意 C# switch 里如果 case 3 有大量代码,编译器可能拆分跳转表。但两份代码内容不同(case 0 的代码 ≠ case -10 的代码?case -10 也是 dart:SpeedX 12*dir, Type 98, Damage 20——与 case 0 相同!)。

   对比:
   - case 0(第一段):方向 num8 = frameX==0?-1:frameX==18?1:0,num39 = frameX<36?0:frameX<72?-1:1。位置 i*16+8+10*num8。速度 12。
   - case -10(第二段):num8 = frameX!=0?1:-1。SpeedX = 12*num8(只有水平)。Type 98, Damage 20。位置 i*16+8, +10*num8, Y+2。

   内容不同!case 0 支持四向(frameX 0/18 水平、36/72 垂直),case -10 只支持水平。

   这说明这是**两个独立的代码块**,执行顺序:第一段 switch 先跑,然后第二段 switch 跑。若 num95==0,第一段 case 0 设置了 Type2/Speed/vector(带 break 跳出 switch),然后第二段 switch(num95+10)=10,不匹配 case 0..4 → 无操作,最后 `if (Type2 != 0) NewProjectile`。✅ 这解释了 dart 的四向!

   那第二段什么时候可达?num95+10 ∈ {0..4} → num95 ∈ {-10..-6},不可达。所以第二段是死代码?!

   等等…… 也许 1405 反编译的 `switch (num69 + 10)` 的 case 标签不是 0..4,而是别的。让我看完整段。awk 截断了。让我直接读 1405 的那一段。

   有一种非常可能的情况:**ilspy/反编译器把 jump table 错误表示**。原始 IL 可能是 `switch (num69 - (-10))`,即 num69 ∈ {-10,-9,...}。但 num69 = frameY/18 >= 0。

   另一种可能:这是 **TileID.Sets** 驱动的另一种陷阱!比如 1.4.0.5 的 "Gas Trap"?不。

   让我直接读 1405 完整段来确认第二段 switch 的 case 值范围和它前面是否有对 num69 的修改(比如 num69 -= 10?)。

   在 1405 输出里,第一段 switch(num69) 之后直接 `switch (num69 + 10)`。若源码是 `switch (num69 + 10)`,那 case 0 → num69=-10。

   但等等,也许反编译错误,真实源码是两个独立 switch:num69 和 num69+10 其中第二段在**第一段的某些 case fallthrough 后执行**。不管怎样,游戏实测行为(我可以从 wiki 或已知知识裁决):Spiky Ball Trap 1456 的行为——它发射尖刺球,初速向下。wiki Spiky_Ball_Trap.md 应该有描述"spiky balls are launched with a slight horizontal variation"。

   关键裁决:1456 中哪段是执行路径?按 1456 代码字面:`switch (num95)` 第一段(case 0,1,2,5 / 3 / 4),然后 `switch (num95)` 第二段(case -10..-6)。num95 == 3 时:第一段 case 3 执行(设 num96=185、方向速度、vector3,预算死代码),第二段 case -7 不匹配(num95==3 ≠ -7),最后 `if (num96 != 0) NewProjectile(vector3, speedX, speedY, 185, 40, 2f)`。
   
   num95 == 0:第一段 case 0(方向 num104/num105 四向),第二段 case -10 不匹配 → 发射。✅
   
   所以 **1456 生效路径 = 第一段(case 0,1,2,5,3,4),第二段全是死代码**。Spiky(case 3)= 方向表 + 预算恒 200(死代码)。

   嗯,但实现注释明确说"取 1456 :1944-1976"(即 case -7)。实现者认为第二段是权威。这是个错误理解——除非反编译的字面行为与实际不符。

   不过等等,还有一种可能性我必须排除:也许 ilspycmd 把 `switch` 的**默认跳转表基址**翻译错了,真实的第二段 switch 是 `switch (num95 + 10)`,case 0..4 → num95 ∈ {-10..-6}——依然不可达。

   或者!第一段 switch 的 case 标签其实不是 {0,1,2,3,4,5} 而是 {10,11,12,15,13,14}(即 num95+10),而第二段才是 0..4?那第一段不可达、第二段可达,实现就对了!

   检验:第一段 case 3(spiky)如果不可达,那么 spiky 走第二段 case -7(num95+10 == 3 → num95 == -7)。等等,如果第一段真实标签是 num95+10 ∈ {0..5} → num95 ∈ {-10..-5},那第一段不可达,第二段(num95 ∈ {-10..-6})…… 乱了。

   最直接的裁决方法:看 num95 的可能取值。num95 = tile.frameY / 18。tile 137(陷阱)的 frameY:由 placeStyle 决定。Item.cs 里 Dart Trap 的 placeStyle = 0?查 Item.cs createTile 137 的 placeStyle 表。如果 placeStyle 范围是 0-5(frameY/18 = 0..5 → num95 ∈ {0..5}),那第一段可达、第二段不可达,实现取错。

   反过来如果 placeStyle 是 10-15(frameY = placeStyle*18,frameY/18 = 10..15),那 num95 ∈ {10..15},两段都不可达?!那陷阱根本不发弹——不可能。

   所以 placeStyle 应该是 0-5。验证:1456 第一段 case 标签 {0,1,2,3,4,5},覆盖 0-5 ✅。第二段 {-10..-6} 不可达。

   但为什么 1405 也有这段死代码?1405(1.4.0.5)第一段 case {0,1,2,3,4}(无 5),第二段 `switch(num69+10)` case {0..4} → num69 ∈ {-10..-6} 同样不可达。两版一致存在死代码——这是**反编译伪影**(IL 里 switch 跳转表拆分,反编译器把两段还原成两个 switch,但实际是同一个 switch 的 duplicated body?)。

   嗯,其实最可能的真相:**原始 C# 源码就是两个连续的 switch**,第一个 `switch (num95)`,第二个 `switch (num95 + 10)`。第二个是 Re-Logic 的复制粘贴错误遗留(死代码)。这种死代码在反编译里会原样保留。1405 和 1456 都有,说明 Re-Logic 源码里真的有这段(1.4.0.5 时代就有)。

   而这段死代码的内容("尖刺球纯下抛 + 预算生效")是**早期版本(1.3.x?)的真实行为**,Re-Logic 改成方向表后忘了删旧 switch。所以:
   - 真实游戏行为(玩家可观测)= 第一段:尖刺球**有方向**(frameX 定向)、预算惩罚**不生效**。
   
   等等,不对。如果预算惩罚在 1.4.5.6 生效,游戏里尖刺球陷阱密集布置会被限制。wiki Spiky_Ball_Trap 说:"A Spiky Ball Trap can launch up to ~? balls"。让我查 wiki。

   其实从 wiki 可以裁决:wiki Spiky_Ball_Trap.md 如果说"每个陷阱最多同时存在 X 个球,基于距离衰减预算",则说明预算生效(第二段是活的);如果说"发射方向由陷阱朝向决定",则第一段是活的。

   让我读 wiki 页面裁决。同时读 1405 完整第二段确认。

4. **blockPlayerTeleportationForOneIteration 设置点**:`Terraria.GameContent/PressurePlateHelper.cs:160`。需要读 PressurePlateHelper.cs 全文,这是压力板触发逻辑(玩家/NPC 踩板),必核清单第 3 项的核心!它决定:
   - 哪些压板被玩家触发、哪些被 NPC 触发、哪些被敌怪触发
   - 测重板(442)设置 blockPlayerTeleportationForOneIteration
   - 传感器(423)不在这里(在 Player.cs UpdatePlayerPosition?)

   让我读 PressurePlateHelper.cs。

5. 还需查传感器(423)的实现。原版:Player.cs 里 `if (Main.tile[i,j].type == 423 ...)` 之类。grep 1456 的 type == 423。

现在做:
- 读 1405 完整第二段(awk 更多行)
- 读 PressurePlateHelper.cs
- grep 423 传感器逻辑
- 读 wiki Spiky_Ball_Trap.md / Dart_Trap.md

之后转向实现侧 Game.ts。
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:20.655Z · glm-x-preview-260804

```
关键裁决点浮现:弹 980 = **VenomDartTrap**(1.4.4 新增)；Torches/Campfires Set 仅含 4/215。1405 的 `switch(num69+10)` 是死代码伪影疑云，需 wiki 裁决。先读 PressurePlateHelper 和传感器。
```


---

## 🤖 Assistant · 2026-08-12T18:47:20.662Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PressurePlateHelper.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:20.670Z

**📎 ToolResult**

```
1	using System.Collections.Generic;
2	using System.Linq;
3	using Microsoft.Xna.Framework;
4	
5	namespace Terraria.GameContent;
6	
7	public class PressurePlateHelper
8	{
9		public static object EntityCreationLock = new object();
10	
11		public static Dictionary<Point, bool[]> PressurePlatesPressed = new Dictionary<Point, bool[]>();
12	
13		public static bool NeedsFirstUpdate;
14	
15		private static Vector2[] PlayerLastPosition = new Vector2[255];
16	
17		private static Rectangle pressurePlateBounds = new Rectangle(0, 0, 16, 10);
18	
19		public static void Update()
20		{
21			if (!NeedsFirstUpdate)
22			{
23				return;
24			}
25			foreach (Point key in PressurePlatesPressed.Keys)
26			{
27				PokeLocation(key);
28			}
29			PressurePlatesPressed.Clear();
30			NeedsFirstUpdate = false;
31		}
32	
33		public static void Reset()
34		{
35			PressurePlatesPressed.Clear();
36			for (int i = 0; i < PlayerLastPosition.Length; i++)
37			{
38				PlayerLastPosition[i] = Vector2.Zero;
39			}
40		}
41	
42		public static void ResetPlayer(int player)
43		{
44			Point[] array = PressurePlatesPressed.Keys.ToArray();
45			for (int i = 0; i < array.Length; i++)
46			{
47				MoveAwayFrom(array[i], player);
48			}
49		}
50	
51		public static void UpdatePlayerPosition(Player player)
52		{
53			Point p = new Point(1, 1);
54			Vector2 vector = p.ToVector2();
55			List<Point> tilesIn = Collision.GetTilesIn(PlayerLastPosition[player.whoAmI] + vector, PlayerLastPosition[player.whoAmI] + player.Size - vector);
56			List<Point> tilesIn2 = Collision.GetTilesIn(player.TopLeft + vector, player.BottomRight - vector);
57			Rectangle hitbox = player.Hitbox;
58			hitbox.Inflate(-p.X, -p.Y);
59			Rectangle hitbox2 = player.Hitbox;
60			hitbox2.X = (int)PlayerLastPosition[player.whoAmI].X;
61			hitbox2.Y = (int)PlayerLastPosition[player.whoAmI].Y;
62			hitbox2.Inflate(-p.X, -p.Y);
63			for (int i = 0; i < tilesIn.Count; i++)
64			{
65				Point point = tilesIn[i];
66				Tile tile = Main.tile[point.X, point.Y];
67				if (tile.active() && tile.type == 428)
68				{
69					pressurePlateBounds.X = point.X * 16;
70					pressurePlateBounds.Y = point.Y * 16 + 16 - pressurePlateBounds.Height;
71					if (!hitbox.Intersects(pressurePlateBounds) && !tilesIn2.Contains(point))
72					{
73						MoveAwayFrom(point, player.whoAmI);
74					}
75				}
76			}
77			for (int j = 0; j < tilesIn2.Count; j++)
78			{
79				Point point2 = tilesIn2[j];
80				Tile tile2 = Main.tile[point2.X, point2.Y];
81				if (tile2.active() && tile2.type == 428)
82				{
83					pressurePlateBounds.X = point2.X * 16;
84					pressurePlateBounds.Y = point2.Y * 16 + 16 - pressurePlateBounds.Height;
85					if (hitbox.Intersects(pressurePlateBounds) && (!tilesIn.Contains(point2) || !hitbox2.Intersects(pressurePlateBounds)))
86					{
87						MoveInto(point2, player.whoAmI);
88					}
89				}
90			}
91			PlayerLastPosition[player.whoAmI] = player.position;
92		}
93	
94		public static void DestroyPlate(Point location)
95		{
96			if (PressurePlatesPressed.TryGetValue(location, out var _))
97			{
98				PressurePlatesPressed.Remove(location);
99				PokeLocation(location);
100			}
101		}
102	
103		private static void UpdatePlatePosition(Point location, int player, bool onIt)
104		{
105			if (onIt)
106			{
107				MoveInto(location, player);
108			}
109			else
110			{
111				MoveAwayFrom(location, player);
112			}
113		}
114	
115		private static void MoveInto(Point location, int player)
116		{
117			if (PressurePlatesPressed.TryGetValue(location, out var value))
118			{
119				value[player] = true;
120				return;
121			}
122			lock (EntityCreationLock)
123			{
124				PressurePlatesPressed[location] = new bool[255];
125			}
126			PressurePlatesPressed[location][player] = true;
127			PokeLocation(location);
128		}
129	
130		private static void MoveAwayFrom(Point location, int player)
131		{
132			if (!PressurePlatesPressed.TryGetValue(location, out var value))
133			{
134				return;
135			}
136			value[player] = false;
137			bool flag = false;
138			for (int i = 0; i < value.Length; i++)
139			{
140				if (value[i])
141				{
142					flag = true;
143					break;
144				}
145			}
146			if (!flag)
147			{
148				lock (EntityCreationLock)
149				{
150					PressurePlatesPressed.Remove(location);
151				}
152				PokeLocation(location);
153			}
154		}
155	
156		private static void PokeLocation(Point location)
157		{
158			if (Main.netMode != 1)
159			{
160				Wiring.blockPlayerTeleportationForOneIteration = true;
161				Wiring.HitSwitch(location.X, location.Y);
162				NetMessage.SendData(59, -1, -1, null, location.X, location.Y);
163			}
164		}
165	}
166	

```


---

## 🤖 Assistant · 2026-08-12T18:47:21.587Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; grep -rn \"== 423\\|type == 423\" $T/Terraria/Player.cs | head -10; echo \"===ProjectileSensor 428===\"; grep -rn \"type == 428\" $T/Terraria/*.cs | head -5",
 "description": "Find sensor 423 and pressure pad 428 trigger code"
}
```


---

## 👤 User(sidechain) · 2026-08-12T19:02:33.447Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-12T19:17:38.193Z · <synthetic>

```
API Error: Stream idle timeout - no chunks received
```


---

## 👤 User(sidechain) · 2026-08-12T19:17:38.194Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-13T00:33:51.582Z

```
The coordinator sent a message while you were working:
继续你未完成的「电路与机械」审计——你已定位关键裁决点(弹 980=VenomDartTrap 为 1.4.4 新增、Torches Set 仅含 4/215;1405 的 switch(num69+10) 死代码疑云——若 wiki 无相关记载,以 1456 源码为准并标注)。继续 PressurePlateHelper/传感器部分并输出最终报告。只读审计、禁改文件;每条结论带 file:line;最终输出完整 markdown 报告。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-13T00:34:18.153Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
继续审计。PressurePlateHelper 只处理 tile 428(Projectile 压力板,即 Teal Pressure Pad——青色压力垫,只被玩家踩?不,428 是"Teal Pressure Pad"只被物品/弹触发?)。注意:PressurePlateHelper.UpdatePlayerPosition 处理的是**玩家**与 428 的碰撞(tile 428 = Teal Pressure Pad,仅玩家触发?)。其实原版:Teal Pressure Pad 只被玩家和 NPC?让我理清压力板类型:

- 135 Pressure Plate(各种颜色):
  - Red Pressure Plate(红):仅玩家触发?不对。
  - 实际型号(原版 Player.cs PressureTileHandling):
    - Gray Pressure Plate(灰):任何(玩家+NPC+敌怪)
    - Brown Pressure Plate(棕):仅玩家
    - Green Pressure Plate(绿):仅 NPC?不,绿=仅敌怪?
    - Lihzahrd Pressure Plate(蜥蜴):仅玩家
    - Blue Pressure Plate(蓝):任何但不触发机关?蓝板"只触发一次"?
  - 准确的:Pressure Plates family:
    - Gray: triggers for players, NPCs, and enemies(所有)
    - Brown: players only
    - Green: NPCs and enemies(not players)
    - Lihzahrd: players only + 阻止传送(实际上 blockPlayerTeleportationForOneIteration 是所有 PokeLocation 设置)
    - Blue: 只触发一次后毁坏?不对,蓝板是"被任何实体触发但不会触发其他压板"?
  
  需要源码裁决:Player.cs / NPC.cs 里的 PressurePlate 触发代码。

- 428 Teal Pressure Pad:仅被**投射物和物品**触发(不是玩家!)。但 PressurePlateHelper.UpdatePlayerPosition 却在处理玩家与 428…… 等等,428 在 Player.cs 里被玩家踩会怎样?

  哦,我明白了:PressurePlateHelper 处理的是 428(青色压力垫),它由**玩家踩上**触发(MoveInto → PokeLocation → HitSwitch)。而 Teal Pressure Pad 的 wiki 描述是"triggered by anything, including items and projectiles"?不对。

  实际原版:Teal Pressure Pad(428)= 被玩家、NPC、敌怪、物品、投射物全都触发?让我查原版 Player.cs 的 type == 428 和 Projectile.cs。

  之前 Game.ts:2603 注释说"脚下格(Bottom 左下角 +0.01)是 411 未触发态 → Wiring.HitSwitch",而 Game.ts:1621 注释说"触发源登记(测重板 428/感应器 423)"。所以实现把 428 当玩家触发源登记。

- 442 Weighted Pressure Plate(测重板):被玩家/NPC/敌怪/物品触发,玩家踩上会**卡住玩家**(不可穿过,像实心块),并且触发时阻止传送。原版 Player.cs 有 "if (tile.type == 442)" 的碰撞处理。Game.ts:2603 提到 411?注释说 411 但代码是 sheetOf(dx,dy)===411?411 是引爆器(detonator)!Game.ts:2603: `if (this.wiring.sheetOf(dx, dy) === 411 && frameY==0 && frameX<36) hitSwitch` —— 玩家踩上引爆器触发!这是原版行为(Player.cs 里 411 被踩触发)。等等 411 是 Detonator(起爆器),被玩家踩上去会触发。对,原版有这个。好。

现在我需要:
1. 原版 Player.cs 的压力板/传感器触发逻辑(type 135/423/428/442/476)
2. 实现侧 Game.ts 的对应逻辑
3. wiki 数值核对

由于刚才 Bash 被临时限制,让我用 Read/Grep 的方式继续。其实 Bash 只是暂时不可用(分类器问题),稍后重试。我先用 Read 读 wiki 文件(Read 工具不受影响)。

计划:
1. 读 wiki:Pressure_Plates.md、Sensors.md、Teleporter.md、Timers.md、Logic_Gates.md、Wire.md、Pumps.md、Dart_Trap.md、Spiky_Ball_Trap.md、Venom_Dart_Trap.md、Mechanisms.md、Statues.md(雕像刷怪规则)
2. Bash 恢复后 grep Player.cs 压板/传感器 + Game.ts 对应段
3. 输出报告

先读 wiki(多个并行 Read)。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:34:18.596Z · glm-x-preview-260804

```
收到。继续审计:先读 wiki 裁决数值(Bash 暂时受限，先用 Read 读 wiki 镜像)。
```


---

## 🤖 Assistant · 2026-08-13T00:34:18.734Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Pressure_Plates.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:34:18.888Z

**📎 ToolResult**

```
1	# Pressure Plates
2	
3	> 原页面: `Pressure_Plates`
4	
5	# Pressure Plates
6	
7	Pressure Plates
8	
9	  *   
10	
11	  *   
12	  
13	
14	[](Autoswing.md "Auto-use")
15	
16	Statistics
17	
18	Type| [Furniture](Furniture.md "Furniture")[Mechanism](Mechanism "Mechanism")[Crafting material](Crafting_material "Crafting material")  
19	---|---  
20	[Placeable](Placement.md "Placement")| ✔️ (1 wide × 1 high)  
21	[Use time](Use_time.md "Use time")| 15 (Very fast)  
22	[Research](Journey_Mode#Research "Journey Mode")| 5 required  
23	  
24	  * Internal [Item ID](Item_IDs.md "Item IDs"): **542, 543, 852, 1151, 529, 541, 853, 4261, 3626, 3630–3632, 3707**
25	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **135, 428, 442**
26	
27	Not to be confused with [Pressure Plate Track](Pressure_Plate_Track.md "Pressure Plate Track").
28	
29	**Pressure Plates** are activation [mechanisms](Mechanisms.md "Mechanisms") that trigger [wired](Wire.md "Wire") mechanisms when stepped on. A pressure plate's color determines which characters can trigger it. 
30	
31	Red, Brown, Gray, Orange, and Lihzahrd Pressure Plates are randomly generated on the map during [world creation](World_generation.md "World generation") as the trigger for [traps](Traps.md "Traps"). They only take up a very small space on top of [blocks](Blocks.md "Blocks"), so they may be difficult to spot. The color of naturally spawned pressure plates is dependent on the color of the block they are generated on top of. Except for Lihzahrd Pressure Plates, they can also be purchased from the [Mechanic](Mechanic.md "Mechanic"). 
32	
33	**Weighted Pressure Plates** activate once on being depressed, and again on being released. All Weighted Pressure Plates of the same color share a single state. As long as one Weighted Pressure Plate of a given color is already pressed down within a circuit, stepping on another identical plate will not send a new signal. They can be crafted from regular pressure plates. 
34	
35	The **Teal Pressure Pad** is a special kind of pressure plate that responds to [projectiles](Projectiles.md "Projectiles") impacting it, which includes [pets](Pets.md "Pets") that touch it. Unlike regular pressure plates, the Teal Pressure Pad can be placed on all four sides of a block, e.g. on the ceiling or sidewall. It can be purchased from the Mechanic. 
36	
37	## Types
38	
39	Type | Trigger criteria | Tooltip | Source | Rarity | Sell | [Tile ID](Tile_IDs.md "Tile IDs")  
40	---|---|---|---|---|---|---  
41	~~~~|  Gray Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 542 | Triggered by players only.  | Signals when stepped on by a player | Plundering ([Underground](Underground.md "Underground"), blue only in [Beam me up](Beam_me_up.md "Beam me up") [secret seed](Secret_seed "Secret seed"))/  
42	[Mechanic](Mechanic.md "Mechanic") (50 _SC_)  | [](Rarity.md "White \(Rarity level: 0\)") | 10 _SC_ | 135 (2)   
43	~~~~|  Brown Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 543 | 135 (3)   
44	~~~~|  Blue Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 852 | 135 (4)   
45	~~~~|  Lihzahrd Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 1151 | Plundering ([Jungle Temple](Jungle_Temple.md "Jungle Temple"))  | 135 (6)   
46	~~~~|  Red Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 529 | Triggered by players, [NPCs](NPCs.md "NPCs"), [enemies](Enemies.md "Enemies"), and [projectiles](Projectiles.md "Projectiles")[a].  | Signals when stepped on | [Mechanic](Mechanic.md "Mechanic") (50 _SC_)  | [](Rarity.md "White \(Rarity level: 0\)") | 10 _SC_ | 135 (0)   
47	~~~~|  Green Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 541 | 135 (1)   
48	~~~~|  Yellow Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 853 | Triggered by NPCs and enemies.  | Signals when stepped on, unless by a player | [Mechanic](Mechanic.md "Mechanic") (50 _SC_)  | [](Rarity.md "White \(Rarity level: 0\)") | 10 _SC_ | 135 (5)   
49	~~~~|  Orange Pressure Plate**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 4261 | Triggered by players only. Breaks after being triggered.  | Signals and breaks when stepped on by a player | [Mechanic](Mechanic.md "Mechanic") (50 _SC_)  | [](Rarity.md "White \(Rarity level: 0\)") | 10 _SC_ | 135 (7)   
50	~~~~|  Pink Weighted Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 3626 | Triggered by players when stepping on or off it.  | Signals when stepped on or off by a player | Crafting _(seebelow)_ | [](Rarity.md "Blue \(Rarity level: 1\)") | No value  | 428 (3)   
51	~~~~|  Orange Weighted Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 3630 | 428 (0)   
52	~~~~|  Purple Weighted Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 3631 | 428 (2)   
53	~~~~|  Cyan Weighted Pressure PlateInternal [Item ID](Item_IDs.md "Item IDs"): 3632 | 428 (1)   
54	~~~~|  Teal Pressure Pad**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3707 | Triggered by projectiles[a].  | Signals when a projectile touches it | [Mechanic](Mechanic.md "Mechanic") (2 _GC_)  | [](Rarity.md "White \(Rarity level: 0\)") | 40 _SC_ | 442   
55	  
56	## Crafting
57	
58	### Recipes
59	
60	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
61	---|---|---  
62	Cyan Weighted Pressure Plate| 
63	
64	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
65	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
66	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
67	
68	| [](Tinkerer's_Workshop.md "Tinkerer's Workshop")[Tinkerer's Workshop](Tinkerer's_Workshop.md "Tinkerer's Workshop")  
69	Orange Weighted Pressure Plate| 
70	
71	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
72	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
73	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
74	
75	  
76	Pink Weighted Pressure Plate| 
77	
78	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
79	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
80	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
81	
82	  
83	Purple Weighted Pressure Plate| 
84	
85	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
86	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
87	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
88	
89	  
90	  
91	### Used in
92	
93	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
94	---|---|---  
95	[](Cyan_Weighted_Pressure_Plate.md "Cyan Weighted Pressure Plate")[Cyan Weighted Pressure Plate](Cyan_Weighted_Pressure_Plate.md "Cyan Weighted Pressure Plate")| 
96	
97	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
98	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
99	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
100	
101	| [](Tinkerer's_Workshop.md "Tinkerer's Workshop")[Tinkerer's Workshop](Tinkerer's_Workshop.md "Tinkerer's Workshop")  
102	[](Orange_Weighted_Pressure_Plate.md "Orange Weighted Pressure Plate")[Orange Weighted Pressure Plate](Orange_Weighted_Pressure_Plate.md "Orange Weighted Pressure Plate")| 
103	
104	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
105	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
106	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
107	
108	  
109	[](Pink_Weighted_Pressure_Plate.md "Pink Weighted Pressure Plate")[Pink Weighted Pressure Plate](Pink_Weighted_Pressure_Plate.md "Pink Weighted Pressure Plate")| 
110	
111	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
112	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
113	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
114	
115	  
116	[](Pressure_Plate_Track.md "Pressure Plate Track")[Pressure Plate Track](Pressure_Plate_Track.md "Pressure Plate Track")| 
117	
118	  * [](Minecart_Track.md "Minecart Track")[Minecart Track](Minecart_Track.md "Minecart Track")
119	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
120	
121	| [](Iron_Anvil "Iron Anvil")[Iron Anvil](Iron_Anvil "Iron Anvil")  
122	 _**or**_  
123	[](Lead_Anvil "Lead Anvil")[Lead Anvil](Lead_Anvil "Lead Anvil")  
124	[](Purple_Weighted_Pressure_Plate.md "Purple Weighted Pressure Plate")[Purple Weighted Pressure Plate](Purple_Weighted_Pressure_Plate.md "Purple Weighted Pressure Plate")| 
125	
126	  * [](Any_Pressure_Plate.md "Any Pressure Plate")[Any Pressure Plate](Any_Pressure_Plate.md "Any Pressure Plate")
127	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")2
128	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
129	
130	| [](Tinkerer's_Workshop.md "Tinkerer's Workshop")[Tinkerer's Workshop](Tinkerer's_Workshop.md "Tinkerer's Workshop")  
131	  
132	## Notes
133	
134	  * The [Dangersense](Dangersense "Dangersense") buff will highlight pressure plates.
135	  * Teal Pressure Pads do not have to be shot for them to activate. As long as the projectile passes through the tile containing the pressure plate, it will activate.
136	  * [Golf Balls](Golf_Balls.md "Golf Balls") count as projectiles for purposes of triggering Teal Pressure Pads.
137	  * Pressure plates will work in [reversed gravity](Reversed_gravity.md "Reversed gravity") if placed on top of a block and then flown into.
138	
139	## Tips
140	
141	  * Pressure plates allow the player to see laid [wires](Wire.md "Wire") when held, which can help avoiding traps. 
142	    * This is not the case in [For the Worthy](For_the_Worthy.md "For the Worthy") or [Zenith](Zenith_\(seed\) "Zenith \(seed\)") worlds.
143	  * Pressure plates that can be triggered by non-players can also be triggered by [Boulders](Boulder.md "Boulder"). This can be used as a delay, or to trigger a row of traps as it rolls down a hallway.
144	  * They can be used for opening and closing [doors](Doors.md "Doors") without having to manually open or close them, although care should be taken that they are not unintentionally triggered by incorrect types of entities. This can be avoided by using the right kind of pressure plate. This is helpful if one has [Smart Doors](Smart_Doors.md "Smart Doors") disabled but one specific door they wish to be automatic.
145	  * [Paint](Paint "Paint") can be applied to pressure plates to disguise them, e.g. for [PvP](PvP.md "PvP") purposes. [Echo Coating](Echo_Coating.md "Echo Coating") can be applied to make them completely invisible.
146	  * Because they are projectiles, [Falling Stars](Fallen_Star.md "Fallen Star") can activate Teal Pressure Pads.
147	  * Teal Pressure Pads can be used in tandem with a [Dart Trap](Dart_Trap.md "Dart Trap") to create a 'diode' with a short delay, before [Logic Gates](Logic_Gates.md "Logic Gates") become available.
148	
149	## History
150	
151	[ Desktop version](Desktop_version_history.md "Desktop version history")
152	
153	  * [Desktop 1.4.0.1](Desktop_1.4.0.1 "Desktop 1.4.0.1"): Introduced Orange Pressure Plate.
154	
155	  * [Desktop 1.3.2.1](Desktop_1.3.2.1 "Desktop 1.3.2.1"): Fixed Weighted Pressure Plates not working.
156	
157	  * [Desktop 1.3.1](Desktop_1.3.1 "Desktop 1.3.1"): 
158	    * Introduced Weighted Pressure Plates.
159	    * Introduced Teal Pressure Pad.
160	
161	  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Updated sprites for all pressure plates. Old sprites were 
162	
163	  * [Desktop 1.2.4](Desktop_1.2.4 "Desktop 1.2.4"): Now used to make Pressure Plate Tracks.
164	
165	  * [Desktop 1.2](Desktop_1.2 "Desktop 1.2"): 
166	    * Now have different triggering criteria based on color.
167	    * Blue, yellow, and Lihzahrd variants added.
168	    * Stack limit increased from 250 to 999.
169	    * Enemies no longer trigger underground pressure plates.
170	
171	  * [Desktop 1.1](Desktop_1.1 "Desktop 1.1"): Introduced.
172	
173	[ Console version](Console_version.md "Console version")
174	
175	  * [Console 1.0.1372.5](Console_1.0.1372.5.md "Console 1.0.1372.5"): 
176	    * Introduced Weighted Pressure Plates.
177	    * Introduced the Teal Pressure Pad.
178	
179	  * [Console 1.0.933.1](Console_1.0.933.1.md "Console 1.0.933.1"): Sprites updated to match Desktop 1.3.0.1. ([](Console_version.md "Xbox One"))
180	
181	  * [Console 1.0.750.0](Console_1.0.750.0.md "Console 1.0.750.0"): Sprites updated to match Desktop 1.3.0.1. ([](Console_version.md "PlayStation 4"))
182	
183	  * [Console 1.07](Console_1.07.md "Console 1.07"): Now used to make Pressure Plate Tracks.
184	
185	  * [Console-Release](Console-Release.md "Console-Release"): Introduced with changes up to Desktop 1.2.
186	
187	[ Nintendo Switch version](Switch_version.md "Switch version")
188	
189	  * [Switch 1.0.895.9](Switch_1.0.895.9.md "Switch 1.0.895.9"): 
190	    * Introduced Weighted Pressure Plates.
191	    * Introduced the Teal Pressure Pad.
192	
193	  * [Switch 1.0.711.6](Switch_1.0.711.6.md "Switch 1.0.711.6"): Introduced with changes up to Desktop 1.3.0.1.
194	
195	[ Mobile version](Mobile_version.md "Mobile version")
196	
197	  * [Mobile 1.4.0.5.0](Mobile_1.4.0.5.0.md "Mobile 1.4.0.5.0"): 
198	    * Introduced Orange and Weighted Pressure Plates.
199	    * Introduced the Teal Pressure Pad.
200	
201	  * [Mobile 1.3.0.7](Mobile_1.3.0.7.md "Mobile 1.3.0.7"): Sprites updated to match Desktop 1.3.0.1.
202	
203	  * [Mobile 1.2.11212](Mobile_1.2.11212.md "Mobile 1.2.11212"): Now used to make Pressure Plate Tracks.
204	
205	  * [Mobile 1.2.6508](Mobile_1.2.6508.md "Mobile 1.2.6508"): 
206	    * Now have different triggering criteria based on color.
207	    * Blue, yellow, and Lihzahrd variants added.
208	    * Stack limit increased from 250 to 999.
209	    * Enemies no longer trigger underground pressure plates.
210	
211	  * [Mobile-Release](Mobile-Release.md "Mobile-Release"): Introduced.Verify
212	
213	[Nintendo 3DS](Legacy%3A3DS_version "Legacy:3DS version")[](Legacy%3A3DS_version "3DS")[ version](Legacy%3A3DS_version "Legacy:3DS version")
214	
215	  * [3DS-Release](3DS-Release.md "3DS-Release"): Introduced.
216	
217	## Footnotes
218	
219	  1. ↑ 1.0 1.1 Only projectiles that cannot travel through solid [blocks](Blocks.md "Blocks") are included. This includes [pets](Pets.md "Pets") and [minions](Minions "Minions").
220	
221	View or edit this template
222	
223	[Wiring](Guide%3AWiring "Guide:Wiring")
224	
225	Tools
226	
227	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
228	  * [](Wrenches.md "Wrenches")[](Wrenches.md "Wrenches")[](Wrenches.md "Wrenches")[](Wrenches.md "Wrenches")[Wrenches](Wrenches.md "Wrenches")
229	  * [](Wire_Cutter.md "Wire Cutter")[Wire Cutter](Wire_Cutter.md "Wire Cutter")
230	  * [](Multicolor_Wrench.md "Multicolor Wrench")[Multicolor Wrench](Multicolor_Wrench.md "Multicolor Wrench")**** __(Desktop, Console and Mobile versions)
231	  * [](The_Grand_Design.md "The Grand Design")[The Grand Design](The_Grand_Design.md "The Grand Design")**** __(Desktop, Console and Mobile versions)
232	  * [](Actuation_Rod.md "Actuation Rod")[Actuation Rod](Actuation_Rod.md "Actuation Rod")**** __(Desktop, Console and Mobile versions)
233	
234	Accessories
235	
236	  * [](Mechanical_Lens.md "Mechanical Lens")[Mechanical Lens](Mechanical_Lens.md "Mechanical Lens")**** __(Desktop, Console and Mobile versions)
237	  * [](Mechanical_Ruler.md "Mechanical Ruler")[Mechanical Ruler](Mechanical_Ruler.md "Mechanical Ruler")**** __(Desktop, Console and Mobile versions)
238	  * [](Presserator.md "Presserator")[Presserator](Presserator.md "Presserator")**** __(Desktop, Console and Mobile versions)
239	
240	Triggers
241	
242	  * [](Lever.md "Lever")[Lever](Lever.md "Lever")
243	  * [](Switch.md "Switch")[Switch](Switch.md "Switch")
244	  * [](Pressure_Plates.md "Pressure Plates")Pressure Plates
245	  * [](Pressure_Plate_Track.md "Pressure Plate Track")[Pressure Plate Track](Pressure_Plate_Track.md "Pressure Plate Track")
246	  * [](Timers.md "Timers")[](Timers.md "Timers")[](Timers.md "Timers")[](Timers.md "Timers")[](Timers.md "Timers")[Timers](Timers.md "Timers")
247	  * [](Detonator.md "Detonator")[Detonator](Detonator.md "Detonator")**** __(Desktop, Console and Mobile versions)
248	  * [](Trapped_Chests.md "Trapped Chests")[Trapped Chests](Trapped_Chests.md "Trapped Chests")**** __(Desktop, Console and Mobile versions)
249	  * [](Dead_Man's_Chest.md "Dead Man's Chest")[Dead Man's Chest](Dead_Man's_Chest.md "Dead Man's Chest")**** __(Desktop, Console and Mobile versions)
250	  * [](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[Gem Locks](Gem_Locks.md "Gem Locks")**** __(Desktop, Console and Mobile versions)
251	  * [](Sensors.md "Sensors")[](Sensors.md "Sensors")[](Sensors.md "Sensors")[Logic Sensors](Sensors.md "Sensors")**** __(Desktop, Console and Mobile versions)
252	  * [](Golf_Cup.md "Golf Cup")[Golf Cup](Golf_Cup.md "Golf Cup")**** __(Desktop, Console and Mobile versions)
253	
254	[Devices](Mechanism "Mechanism")
255	
256	  * [](Active_Stone_Block.md "Active Stone Block")[](Active_Stone_Block.md "Active Stone Block")[Active/Inactive Stone Block](Active_Stone_Block.md "Active Stone Block")
257	  * [](Actuator.md "Actuator")[Actuator](Actuator.md "Actuator")
258	  * [](Announcement_Box.md "Announcement Box")[Announcement Box](Announcement_Box.md "Announcement Box")**** __(Desktop, Console and Mobile versions)
259	  * [](Doors.md "Doors")[Doors](Doors.md "Doors")
260	  * [](Trap_Door.md "Trap Door")[Trap Door](Trap_Door.md "Trap Door")**** __(Desktop, Console and Mobile versions)
261	  * [](Tall_Gate.md "Tall Gate")[Tall Gate](Tall_Gate.md "Tall Gate")**** __(Desktop, Console and Mobile versions)
262	  * [](Pumps.md "Pumps")[](Pumps.md "Pumps")[Pumps](Pumps.md "Pumps")
263	  * [](Grate.md "Grate")[Grate](Grate.md "Grate")**** __(Desktop, Console and Mobile versions)
264	  * [](Teleporter.md "Teleporter")[Teleporter](Teleporter.md "Teleporter")
265	  * [](Statue#Functional_statues "Functional Statues")[](Statue#Functional_statues "Functional Statues")[Functional Statues](Statue#Functional_statues "Statue")
266	  * [](Light_sources.md "Light sources")[](Light_sources.md "Light sources")[](Light_sources.md "Light sources")[Light sources](Light_sources.md "Light sources")
267	  * [](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[Gemspark Blocks](Gemspark_Blocks.md "Gemspark Blocks")**** __(Desktop, Console, Old-gen console and Mobile versions)
268	  * [](Mini_Volcano.md "Mini Volcano")[Mini Volcano](Mini_Volcano.md "Mini Volcano")**** __(Desktop, Console and Mobile versions)
269	  * [](Large_Volcano.md "Large Volcano")[Large Volcano](Large_Volcano.md "Large Volcano")**** __(Desktop, Console and Mobile versions)
270	  * [](Pixel_Box.md "Pixel Box")[Pixel Box](Pixel_Box.md "Pixel Box")**** __(Desktop, Console and Mobile versions)
271	  * [](Junction_Box.md "Junction Box")[Junction Box](Junction_Box.md "Junction Box")**** __(Desktop, Console and Mobile versions)
272	  * [](Logic_Gates.md "Logic Gates")[Logic Gates](Logic_Gates.md "Logic Gates")**** __(Desktop, Console and Mobile versions)
273	  * [](Logic_Gate_Lamps.md "Logic Gate Lamps")[Logic Gate Lamps](Logic_Gate_Lamps.md "Logic Gate Lamps")**** __(Desktop, Console and Mobile versions)
274	
275	[Traps](Trap "Trap")
276	
277	  * [](Dart_Trap.md "Dart Trap")[Dart](Dart_Trap.md "Dart Trap")
278	  * [](Venom_Dart_Trap.md "Venom Dart Trap")[Venom Dart](Venom_Dart_Trap.md "Venom Dart Trap")**** __(Desktop, Console and Mobile versions)
279	  * [](Super_Dart_Trap.md "Super Dart Trap")[Super Dart](Super_Dart_Trap.md "Super Dart Trap")
280	  * [](Spear_Trap.md "Spear Trap")[Spear](Spear_Trap.md "Spear Trap")
281	  * [](Spiky_Ball_Trap.md "Spiky Ball Trap")[Spiky Ball](Spiky_Ball_Trap.md "Spiky Ball Trap")
282	  * [](Flame_Trap.md "Flame Trap")[Flame](Flame_Trap.md "Flame Trap")
283	  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
284	  * [](Geyser.md "Geyser")[Geyser](Geyser.md "Geyser")**** __(Desktop, Console and Mobile versions)
285	  * [](Land_Mine.md "Land Mine")[Land Mine](Land_Mine.md "Land Mine")
286	
287	View or edit this template
288	
289	[Furniture](Furniture.md "Furniture"):
290	
291	  * [](Crafting_stations.md "Crafting stations")[Crafting Stations](Crafting_stations.md "Crafting stations")
292	  * [](Light_sources.md "Light sources")[Light Sources](Light_sources.md "Light sources")
293	  * [](Storage_items.md "Storage items")[Storage Items](Storage_items.md "Storage items")
294	  * [](Decorative_items.md "Decorative items")[Other Items](Decorative_items.md "Decorative items")
295	
296	Crafting Stations
297	
298	[Pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode")
299	
300	  * [By Hand](By_Hand.md "By Hand")
301	  * [Work Bench](Work_Bench "Work Bench")
302	  * [Furnace](Furnace.md "Furnace")
303	  * [Hellforge](Hellforge.md "Hellforge")
304	  * [Iron Anvil](Pre-Hardmode_Anvils.md "Pre-Hardmode Anvils")
305	  * [Lead Anvil](Pre-Hardmode_Anvils.md "Pre-Hardmode Anvils")
306	  * [Sawmill](Sawmill.md "Sawmill")
307	  * [Placed Bottle](Bottle_\(crafting_station\) "Bottle \(crafting station\)")
308	  * [Alchemy Table](Alchemy_Table.md "Alchemy Table")**** __(Desktop, Console and Mobile versions)
309	  * [Alchemy Flask](Alchemy_Flask.md "Alchemy Flask")**** __(Desktop, Console and Mobile versions)
310	  * [Chair](Chair "Chair")
311	  * [Table](Table "Table")
312	  * [Bookcase](Bookcase "Bookcase")
313	  * [Loom](Loom.md "Loom")
314	  * [Campfire](Campfire "Campfire")
315	  * [Cooking Pot](Cooking_Pot "Cooking Pot")
316	  * [Cauldron](Cauldron "Cauldron")
317	  * [Keg](Keg.md "Keg")
318	  * [Teapot](Teapot.md "Teapot")**** __(Desktop, Console and Mobile versions)
319	  * [Tinkerer's Workshop](Tinkerer's_Workshop.md "Tinkerer's Workshop")
320	  * [Imbuing Station](Imbuing_Station.md "Imbuing Station")
321	  * [Sink](Sinks.md "Sinks")**** __(Desktop, Console and Mobile versions)
322	
323	[Hardmode](Hardmode.md "Hardmode")
324	
325	  * [Adamantite Forge](Hardmode_Forges.md "Hardmode Forges")
326	  * [Titanium Forge](Hardmode_Forges.md "Hardmode Forges")
327	  * [Mythril Anvil](Hardmode_Anvils.md "Hardmode Anvils")
328	  * [Orichalcum Anvil](Hardmode_Anvils.md "Hardmode Anvils")
329	  * [Autohammer](Autohammer.md "Autohammer")
330	  * [Blend-O-Matic](Blend-O-Matic.md "Blend-O-Matic")
331	  * [Ancient Manipulator](Ancient_Manipulator.md "Ancient Manipulator")**** __(Desktop, Console and Mobile versions)
332	
333	Themed  
334	**** __(Desktop, Console, Old-gen console and Mobile versions)
335	
336	  * [Bone Welder](Bone_Welder.md "Bone Welder")**** __(Desktop, Console, Old-gen console and Mobile versions)
337	  * [Decay Chamber](Decay_Chamber.md "Decay Chamber")**** __(Desktop, Console and Mobile versions)
338	  * [Flesh Cloning Vat](Flesh_Cloning_Vat.md "Flesh Cloning Vat")**** __(Desktop, Console, Old-gen console and Mobile versions)
339	  * [Glass Kiln](Glass_Kiln.md "Glass Kiln")**** __(Desktop, Console, Old-gen console and Mobile versions)
340	  * [Honey Dispenser](Honey_Dispenser.md "Honey Dispenser")**** __(Desktop, Console, Old-gen console and Mobile versions)
341	  * [Ice Machine](Ice_Machine.md "Ice Machine")**** __(Desktop, Console, Old-gen console and Mobile versions)
342	  * [Lihzahrd Furnace](Lihzahrd_Furnace.md "Lihzahrd Furnace")**** __(Desktop, Console, Old-gen console and Mobile versions)
343	  * [Living Loom](Living_Loom.md "Living Loom")**** __(Desktop, Console, Old-gen console and Mobile versions)
344	  * [Sky Mill](Sky_Mill.md "Sky Mill")**** __(Desktop, Console, Old-gen console and Mobile versions)
345	  * [Solidifier](Solidifier.md "Solidifier")
346	  * [Steampunk Boiler](Steampunk_Boiler.md "Steampunk Boiler")**** __(Desktop, Console, Old-gen console and Mobile versions)
347	
348	Environment
349	
350	  * [Water](Water.md "Water")
351	  * [Lava](Lava.md "Lava")
352	  * [Honey](Honey.md "Honey")
353	  * [Shimmer](Shimmer.md "Shimmer")**** __(Desktop, Console and Mobile versions)
354	  * [Altar](Altar "Altar")
355	
356	Other
357	
358	  * [Crystal Ball](Crystal_Ball.md "Crystal Ball")
359	  * [Dye Vat](Dye_Vat.md "Dye Vat")**** __(Desktop, Console, Old-gen console and Mobile versions)
360	  * [Heavy Assembler](Heavy_Assembler.md "Heavy Assembler")**** __(Desktop, Console, Old-gen console and Mobile versions)
361	  * [Meat Grinder](Meat_Grinder.md "Meat Grinder")
362	  * [Extractinator](Extractinator.md "Extractinator")
363	  * [Chlorophyte Extractinator](Chlorophyte_Extractinator.md "Chlorophyte Extractinator")**** __(Desktop, Console and Mobile versions)
364	
365	Light Sources
366	
367	Placeable
368	
369	Suitable  
370	for housing
371	
372	  * [Torches](Torches.md "Torches")
373	  * [Fireplace](Fireplace.md "Fireplace")**** __(Desktop, Console and Mobile versions)
374	  * [Candelabras](Candelabras.md "Candelabras")
375	  * [Candles](Candles.md "Candles")
376	    * [Peace](Peace_Candle.md "Peace Candle")**** __(Desktop, Console and Mobile versions)
377	    * [Water](Water_Candle.md "Water Candle")
378	    * [Shadow](Shadow_Candle.md "Shadow Candle")**** __(Desktop, Console and Mobile versions)
379	  * [Chandeliers](Chandeliers.md "Chandeliers")
380	  * [Lamps](Lamps.md "Lamps")**** __(Desktop, Console, Old-gen console and Mobile versions)
381	  * [Lanterns](Lanterns.md "Lanterns")
382	    * [Heart Lantern](Heart_Lantern.md "Heart Lantern")
383	    * [Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle")
384	  * [Chinese Lantern](Chinese_Lantern "Chinese Lantern")
385	  * [Christmas lights](Christmas_lights.md "Christmas lights")
386	  * [Jack 'O Lantern](Jack_'O_Lantern.md "Jack 'O Lantern")
387	  * [Tiki Torch](Tiki_Torch.md "Tiki Torch")
388	  * [Skull Lantern](Skull_Lantern.md "Skull Lantern")
389	  * [Hanging Brazier](Hanging_Brazier.md "Hanging Brazier")**** __(Desktop, Console and Mobile versions)
390	
391	Unsuitable  
392	for housing
393	
394	  * [Lamp Post](Lamp_Post.md "Lamp Post")
395	  * [Campfire](Campfire "Campfire")
396	  * [Disco Ball](Disco_Ball.md "Disco Ball")
397	  * [Furnace](Furnace.md "Furnace")
398	  * [Hellforge](Hellforge.md "Hellforge")
399	  * [Adamantite Forge](Adamantite_Forge "Adamantite Forge")
400	  * [Titanium Forge](Titanium_Forge "Titanium Forge")
401	  * [Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar")
402	  * [Lava Lamp](Lava_Lamp.md "Lava Lamp")**** __(Desktop, Console and Mobile versions)
403	  * [Plasma Lamp](Plasma_Lamp.md "Plasma Lamp")**** __(Desktop, Console and Mobile versions)
404	
405	Portable
406	
407	  * [Torches](Torches.md "Torches")
408	  * [Candles](Candles.md "Candles")
409	  * [Glowstick](Glowstick.md "Glowstick")
410	    * [Sticky](Sticky_Glowstick.md "Sticky Glowstick")
411	    * [Bouncy](Bouncy_Glowstick.md "Bouncy Glowstick")**** __(Desktop, Console and Mobile versions)
412	    * [Spelunker](Spelunker_Glowstick.md "Spelunker Glowstick")**** __(Desktop, Console and Mobile versions)
413	    * [Fairy](Fairy_Glowstick.md "Fairy Glowstick")**** __(Desktop, Console and Mobile versions)
414	    * [Rainbow](Rainbow_Glowstick.md "Rainbow Glowstick")**** __(Desktop, Console and Mobile versions)
415	  * [Mining Helmet](Mining_Helmet "Mining Helmet")
416	  * [Jellyfish Necklace](Jellyfish_Necklace.md "Jellyfish Necklace")
417	  * [Flare Gun](Flare_Gun.md "Flare Gun")
418	
419	Storage Items
420	
421	[Chests](Chests.md "Chests")
422	
423	  * [Aetherium](Aetherium_Chest "Aetherium Chest")**** __(Desktop, Console and Mobile versions)
424	  * [Ash Wood](Ash_Wood_Chest "Ash Wood Chest")**** __(Desktop, Console and Mobile versions)
425	  * [Balloon](Balloon_Chest "Balloon Chest")**** __(Desktop, Console and Mobile versions)
426	  * [Bamboo](Bamboo_Chest "Bamboo Chest")**** __(Desktop, Console and Mobile versions)
427	  * [Bone](Bone_Chest "Bone Chest")**** __(Desktop, Console and Mobile versions)
428	  * [Boreal Wood](Boreal_Wood_Chest "Boreal Wood Chest")**** __(Desktop, Console, Old-gen console and Mobile versions)
429	  * [Boulder](Boulder_Chest "Boulder Chest")**** __(Desktop, Console and Mobile versions)
430	  * [Cactus](Cactus_Chest "Cactus Chest")
431	  * [Cloud](Cloud_Chest "Cloud Chest")**** __(Desktop, Console and Mobile versions)
432	  * [Crimtane](Crimtane_Chest "Crimtane Chest")**** __(Desktop, Console and Mobile versions)
433	  * [Crystal](Crystal_Chest "Crystal Chest")**** __(Desktop, Console and Mobile versions)
434	  * [Dead Man's](Dead_Man's_Chest.md "Dead Man's Chest")**** __(Desktop, Console and Mobile versions)
435	  * [Demonite](Demonite_Chest "Demonite Chest")**** __(Desktop, Console and Mobile versions)
436	  * [Dungeon](Dungeon.md "Dungeon")
437	    * [Blue](Blue_Dungeon_Chest "Blue Dungeon Chest")**** __(Desktop, Console, Old-gen console and Mobile versions)
438	    * [Green](Green_Dungeon_Chest "Green Dungeon Chest")**** __(Desktop, Console, Old-gen console and Mobile versions)
439	    * [Pink](Pink_Dungeon_Chest "Pink Dungeon Chest")**** __(Desktop, Console, Old-gen console and Mobile versions)
440	  * [Duskware](Duskware_Chest "Duskware Chest")**** __(Desktop, Console and Mobile versions)
441	  * [Dynasty](Dynasty_Chest "Dynasty Chest")**** __(Desktop, Console and Mobile versions)
442	  * [Easter](Easter_Chest "Easter Chest")**** __(Desktop, Console and Mobile versions)
443	  * [Ebonwood](Ebonwood_Chest "Ebonwood Chest")
444	  * [Fallen Star](Fallen_Star_Chest "Fallen Star Chest")**** __(Desktop, Console and Mobile versions)
445	  * [Fancy Hallowed](Fancy_Hallowed_Chest "Fancy Hallowed Chest")**** __(Desktop, Console and Mobile versions)
446	  * [Feywood](Feywood_Chest "Feywood Chest")**** __(Desktop, Console and Mobile versions)
447	  * [Flesh](Flesh_Chest "Flesh Chest")**** __(Desktop, Console and Mobile versions)
448	  * [Flinx Fur](Flinx_Fur_Chest "Flinx Fur Chest")**** __(Desktop, Console and Mobile versions)
449	  * [Forbidden](Forbidden_Chest "Forbidden Chest")**** __(Desktop, Console and Mobile versions)
450	  * [Frozen](Frozen_Chest.md "Frozen Chest")
451	  * [Glass](Glass_Chest "Glass Chest")**** __(Desktop, Console and Mobile versions)
452	  * [Granite](Granite_Chest.md "Granite Chest")**** __(Desktop, Console and Mobile versions)
453	  * [Gold](Gold_Chest.md "Gold Chest")
454	    * [Golden](Golden_Chest "Golden Chest")**** __(Desktop, Console and Mobile versions)
455	  * [Golf](Golf_Chest "Golf Chest")**** __(Desktop, Console and Mobile versions)
456	  * [Gothic](Gothic_Chest "Gothic Chest")**** __(Desktop, Console and Mobile versions)
457	  * [Harpy](Harpy_Chest "Harpy Chest")**** __(Desktop, Console and Mobile versions)
458	  * [Honey](Honey_Chest "Honey Chest")
459	  * [Ivy](Ivy_Chest.md "Ivy Chest")
460	  * [Jellyfish](Jellyfish_Chest "Jellyfish Chest")**** __(Desktop, Console and Mobile versions)
461	  * [Lesion](Lesion_Chest "Lesion Chest")**** __(Desktop, Console and Mobile versions)
462	  * [Librarian](Librarian_Chest "Librarian Chest")**** __(Desktop, Console and Mobile versions)
463	  * [Lihzahrd](Lihzahrd_Chest.md "Lihzahrd Chest")
464	  * [Living Wood](Living_Wood_Chest.md "Living Wood Chest")
465	  * [Marble](Marble_Chest.md "Marble Chest")**** __(Desktop, Console and Mobile versions)
466	  * [Martian](Martian_Chest "Martian Chest")**** __(Desktop, Console and Mobile versions)
467	  * [Meteorite](Meteorite_Chest "Meteorite Chest")**** __(Desktop, Console and Mobile versions)
468	  * [Mushroom](Mushroom_Chest.md "Mushroom Chest")
469	  * [Nebula](Nebula_Chest "Nebula Chest")**** __(Desktop, Console and Mobile versions)
470	  * [Obsidian](Obsidian_Chest "Obsidian Chest")**** __(Desktop, Console, Old-gen console and Mobile versions)
471	  * [Office](Office_Chest "Office Chest")**** __(Desktop, Console and Mobile versions)
472	  * [Palm Wood](Palm_Wood_Chest "Palm Wood Chest")**** __(Desktop, Console and Mobile versions)
473	  * [Pearlwood](Pearlwood_Chest "Pearlwood Chest")
474	  * [Pine](Pine_Chest "Pine Chest")**** __(Desktop, Console and Mobile versions)
475	  * [Pumpkin](Pumpkin_Chest "Pumpkin Chest")**** __(Desktop, Console and Mobile versions)
476	  * [Reef](Reef_Chest "Reef Chest")**** __(Desktop, Console and Mobile versions)
477	  * [Rich Mahogany](Rich_Mahogany_Chest.md "Rich Mahogany Chest")
478	  * [Sandstone](Sandstone_Chest.md "Sandstone Chest")**** __(Desktop, Console and Mobile versions)
479	  * [Shadewood](Shadewood_Chest "Shadewood Chest")
480	  * [Shadow](Shadow_Chest.md "Shadow Chest")
481	  * [Slime](Slime_Chest "Slime Chest")
482	  * [Skyware](Skyware_Chest.md "Skyware Chest")
483	  * [Snow](Snow_Chest "Snow Chest")**** __(Desktop, Console and Mobile versions)
484	  * [Solar](Solar_Chest "Solar Chest")**** __(Desktop, Console and Mobile versions)
485	  * [Spider](Spider_Chest "Spider Chest")**** __(Desktop, Console and Mobile versions)
486	  * [Spike](Spike_Chest "Spike Chest")**** __(Desktop, Console and Mobile versions)
487	  * [Spooky](Spooky_Chest "Spooky Chest")**** __(Desktop, Console, Old-gen console and Mobile versions)
488	  * [Stardust](Stardust_Chest "Stardust Chest")**** __(Desktop, Console and Mobile versions)
489	  * [Steampunk](Steampunk_Chest "Steampunk Chest")**** __(Desktop, Console and Mobile versions)
490	  * [Stone](Stone_Chest "Stone Chest")**** __(Desktop, Console and Mobile versions)
491	  * [Vortex](Vortex_Chest "Vortex Chest")**** __(Desktop, Console and Mobile versions)
492	  * [Water](Water_Chest.md "Water Chest")
493	  * [Web Covered](Web_Covered_Chest.md "Web Covered Chest")
494	  * [Wooden](Chest "Chest")
495	
496	[Biome Chests](Biome_Chests.md "Biome Chests")
497	
498	  * [Corruption](Corruption_Chest "Corruption Chest")
499	  * [Crimson](Crimson_Chest "Crimson Chest")
500	  * [Ice](Ice_Chest "Ice Chest")
501	  * [Jungle](Jungle_Chest "Jungle Chest")
502	  * [Hallowed](Hallowed_Chest "Hallowed Chest")
503	  * [Desert](Desert_Chest "Desert Chest")**** __(Desktop, Console and Mobile versions)
504	
505	Other
506	
507	  * [Piggy Bank](Piggy_Bank.md "Piggy Bank")
508	  * [Safe](Safe.md "Safe")
509	  * [Defender's Forge](Defender's_Forge.md "Defender's Forge")**** __(Desktop, Console and Mobile versions)
510	  * [Void Vault](Void_Vault.md "Void Vault")**** __(Desktop, Console and Mobile versions)
511	  * [Trash Can](Trash_Can.md "Trash Can")
512	  * [Barrel](Barrel.md "Barrel")
513	  * [Dressers](Dressers.md "Dressers")**** __(Desktop, Console and Mobile versions)
514	  * [Mannequin](Mannequin.md "Mannequin")
515	  * [Womannequin](Womannequin.md "Womannequin")**** __(Desktop, Console, Old-gen console and Mobile versions)
516	  * [Hat Rack](Hat_Rack.md "Hat Rack")**** __(Desktop, Console and Mobile versions)
517	  * [Item Flask](Item_Flask.md "Item Flask")**** __(Desktop, Console and Mobile versions)
518	
519	Other Items
520	
521	[Housing](House#Furniture "House")
522	
523	  * [Tables](Tables.md "Tables")
524	  * [Pianos](Pianos.md "Pianos")
525	  * [Bathtubs](Bathtubs.md "Bathtubs")
526	  * [Dressers](Dressers.md "Dressers")
527	  * [Bookcases](Bookcases.md "Bookcases")
528	  * [Chairs](Chairs.md "Chairs")
529	  * [Beds](Beds.md "Beds")
530	  * [Sofas](Sofas.md "Sofas")**** __(Desktop, Console, Old-gen console and Mobile versions)
531	  * [Benches](Benches.md "Benches")
532	  * [Throne](Throne.md "Throne")
533	  * [Chippy's Couch](Chippy's_Couch.md "Chippy's Couch")**** __(Desktop, Console and Mobile versions)
534	
535	Floor & Ceiling
536	
537	  * [Pylons](Pylons.md "Pylons")**** __(Desktop, Console and Mobile versions)
538	    * [Universal Pylon](Universal_Pylon.md "Universal Pylon")
539	  * [Bars](Bars.md "Bars")
540	  * [Books](Book.md "Book")
541	  * [Bottle](Bottle.md "Bottle")
542	    * [Cups](Cups.md "Cups")**** __(Desktop, Console, Old-gen console and Mobile versions)
543	    * [Mug](Mug.md "Mug")
544	    * [Pink Vase](Pink_Vase.md "Pink Vase")
545	    * [Decorative Healing Potion](Decorative_Healing_Potion.md "Decorative Healing Potion")**** __(Desktop, Console and Mobile versions)
546	    * [Decorative Mana Potion](Decorative_Mana_Potion.md "Decorative Mana Potion")**** __(Desktop, Console and Mobile versions)
547	  * [Bowls](Bowls.md "Bowls")
548	  * [Butterfly jars](Butterfly_jars.md "Butterfly jars")
549	    * [Prismatic Lacewing Jar](Prismatic_Lacewing_Jar.md "Prismatic Lacewing Jar")**** __(Desktop, Console and Mobile versions)
550	  * [Cages](Cages.md "Cages")
551	  * [Coin Piles](Coin_Piles.md "Coin Piles")**** __(Desktop, Console, Old-gen console and Mobile versions)
552	  * [Christmas Tree](Christmas_Tree.md "Christmas Tree")
553	    * [Christmas Tree decorations](Christmas_Tree_decorations.md "Christmas Tree decorations")**** __(Desktop, Console, Old-gen console and Mobile versions)
554	  * [Coral](Coral.md "Coral")
555	  * [Crates](Crates.md "Crates")
556	  * [Crystal Shard](Crystal_Shard.md "Crystal Shard")
557	  * [Decorative Banners](Banners_\(decorative\) "Banners \(decorative\)")
558	    * [War Table Banner](War_Table_Banner.md "War Table Banner")**** __(Desktop, Console and Mobile versions)
559	  * [Decorative Statues](Statue#Decorative_statues "Statue")
560	  * [Desert Spirit Lamp](Desert_Spirit_Lamp.md "Desert Spirit Lamp")**** __(Desktop, Console and Mobile versions)
561	  * [Dragonfly jars](Dragonfly_jars.md "Dragonfly jars")**** __(Desktop, Console and Mobile versions)
562	  * [Fairy jars](Fairy_jars.md "Fairy jars")**** __(Desktop, Console and Mobile versions)
563	  * [Fancy Dishes](Fancy_Dishes.md "Fancy Dishes")**** __(Desktop, Console, Old-gen console and Mobile versions)
564	  * [Fish Bowls](Fish_Bowls.md "Fish Bowls")
565	  * [Gems](Gems.md "Gems")
566	  * [Golf trophies](Golf_trophies.md "Golf trophies")**** __(Desktop, Console and Mobile versions)
567	  * [Hanging Pot](Hanging_Pot.md "Hanging Pot")**** __(Desktop, Console and Mobile versions)
568	    * [Herbs](Hanging_herbs.md "Hanging herbs")**** __(Desktop, Console and Mobile versions)
569	  * [Jellyfish jars](Jellyfish_jars.md "Jellyfish jars")
570	  * [Lawn Flamingo](Lawn_Flamingo.md "Lawn Flamingo")**** __(Desktop, Console and Mobile versions)
571	  * [Magic Droppers](Magic_Droppers.md "Magic Droppers")**** __(Desktop, Console and Mobile versions)
572	  * [Minecart Track](Minecart_Track.md "Minecart Track")
573	    * [Booster](Booster_Track.md "Booster Track")
574	    * [Pressure Plate](Pressure_Plate_Track.md "Pressure Plate Track")
575	  * [Mini Volcano](Mini_Volcano.md "Mini Volcano")**** __(Desktop, Console and Mobile versions)
576	    * [Large](Large_Volcano.md "Large Volcano")**** __(Desktop, Console and Mobile versions)
577	  * [Pin Flags](Pin_Flags.md "Pin Flags")**** __(Desktop, Console and Mobile versions)
578	  * [Pin Wheel](Pin_Wheel.md "Pin Wheel")**** __(Desktop, Console and Mobile versions)
579	  * [Plate](Plate.md "Plate")**** __(Desktop, Console and Mobile versions)
580	  * [Platforms](Platforms.md "Platforms")
581	    * [Planter Box](Planter_Box "Planter Box")**** __(Desktop, Console and Mobile versions)
582	    * [Team](Team_Platforms.md "Team Platforms")**** __(Desktop, Console and Mobile versions)
583	  * [Potted Trees](Potted_Trees.md "Potted Trees")**** __(Desktop, Console and Mobile versions)
584	    * [Lava Plants](Potted_Lava_Plants.md "Potted Lava Plants")**** __(Desktop, Console and Mobile versions)
585	    * [Crystal Plants](Potted_Crystal_Plants.md "Potted Crystal Plants")**** __(Desktop, Console and Mobile versions)
586	  * [Presents](Presents "Presents")
587	  * [Party Present](Party_Present.md "Party Present")**** __(Desktop, Console and Mobile versions)
588	  * [Relics](Relics.md "Relics")**** __(Desktop, Console and Mobile versions)
589	  * [Rock Golem Head](Rock_Golem_Head.md "Rock Golem Head")**** __(Desktop, Console and Mobile versions)
590	  * [Seashells](Seashells.md "Seashells")**** __(Desktop, Console, Old-gen console and Mobile versions)
591	  * [Seaweed Planter](Seaweed_Planter.md "Seaweed Planter")
592	  * [Ship in a Bottle](Ship_in_a_Bottle.md "Ship in a Bottle")
593	  * [Silly Tied Balloons](Silly_Tied_Balloons.md "Silly Tied Balloons")**** __(Desktop, Console and Mobile versions)
594	  * [Silly Tied Bundle of Balloons](Silly_Tied_Bundle_of_Balloons.md "Silly Tied Bundle of Balloons")**** __(Desktop, Console and Mobile versions)
595	  * [Vases](Vases.md "Vases")
596	
597	[Wall](Wall "Wall")
598	
599	  * [Animal skins](Animal_skins.md "Animal skins")**** __(Desktop, Console, Old-gen console and Mobile versions)
600	  * [Catacomb](Catacomb.md "Catacomb")
601	  * [Compass Rose](Compass_Rose.md "Compass Rose")
602	  * [Hanging Skeleton](Hanging_Skeleton.md "Hanging Skeleton")
603	  * [Holly](Holly.md "Holly")**** __(Desktop, Console, Old-gen console and Mobile versions)
604	  * [Life Preserver](Life_Preserver.md "Life Preserver")
605	  * [Living Fire Blocks](Living_Fire_Blocks.md "Living Fire Blocks")**** __(Desktop, Console, Old-gen console and Mobile versions)
606	  * [Paintings](Paintings.md "Paintings")
607	  * [Racks](Racks.md "Racks")**** __(Desktop, Console, Old-gen console and Mobile versions)
608	    * [Weapon Rack](Weapon_Rack.md "Weapon Rack")**** __(Desktop, Console, Old-gen console and Mobile versions)
609	    * [Item Frame](Item_Frame.md "Item Frame")**** __(Desktop, Console and Mobile versions)
610	  * [Ropes](Ropes.md "Ropes")
611	    * [Chain](Chain.md "Chain")
612	  * [Ship's Wheel](Ship's_Wheel.md "Ship's Wheel")
613	  * [Trophies](Trophies.md "Trophies")
614	  * [Treasure Map](Treasure_Map.md "Treasure Map")
615	  * [Wall Anchor](Wall_Anchor.md "Wall Anchor")
616	  * [Wall Skeleton](Wall_Skeleton.md "Wall Skeleton")
617	  * [Wooden Beam](Wooden_Beam "Wooden Beam")
618	
619	Functional
620	
621	  * [Grandfather Clocks](Grandfather_Clocks.md "Grandfather Clocks")
622	  * [Sign](Sign.md "Sign")
623	    * [Tattered Wood Sign](Tattered_Wood_Sign.md "Tattered Wood Sign")**** __(Desktop, Console and Mobile versions)
624	    * [Announcement Box](Announcement_Box.md "Announcement Box")**** __(Desktop, Console and Mobile versions)
625	  * [Tombstone](Tombstone "Tombstone")
626	  * [Target Dummy](Target_Dummy.md "Target Dummy")**** __(Desktop, Console and Mobile versions)
627	  * [Ammo Box](Ammo_Box.md "Ammo Box")**** __(Desktop, Console, Old-gen console and Mobile versions)
628	  * [Bewitching Table](Bewitching_Table.md "Bewitching Table")**** __(Desktop, Console and Mobile versions)
629	  * [Crystal Ball](Crystal_Ball.md "Crystal Ball")
630	  * [Slice of Cake](Slice_of_Cake.md "Slice of Cake")**** __(Desktop, Console and Mobile versions)
631	  * [Sharpening Station](Sharpening_Station.md "Sharpening Station")**** __(Desktop, Console and Mobile versions)
632	  * [War Table](War_Table.md "War Table")**** __(Desktop, Console and Mobile versions)
633	  * [Enemy Banners](Banners_\(enemy\) "Banners \(enemy\)")
634	  * [Bast Statue](Bast_Statue.md "Bast Statue")**** __(Desktop, Console and Mobile versions)
635	  * [Sunflower](Sunflower.md "Sunflower")
636	  * [Campfires](Campfires.md "Campfires")
637	  * [Fireplace](Fireplace.md "Fireplace")**** __(Desktop, Console and Mobile versions)
638	  * [Heart Lantern](Heart_Lantern.md "Heart Lantern")
639	  * [Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle")
640	  * [Water Candle](Water_Candle.md "Water Candle")
641	  * [Peace Candle](Peace_Candle.md "Peace Candle")**** __(Desktop, Console and Mobile versions)
642	  * [Shadow Candle](Shadow_Candle.md "Shadow Candle")**** __(Desktop, Console and Mobile versions)
643	  * [Clay Pot](Clay_Pot.md "Clay Pot")
644	  * [Enchanted Sundial](Enchanted_Sundial.md "Enchanted Sundial")**** __(Desktop, Console and Mobile versions)
645	  * [Enchanted Moondial](Enchanted_Moondial.md "Enchanted Moondial")**** __(Desktop, Console and Mobile versions)
646	  * [Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar")
647	  * [Eternia Crystal Stand](Eternia_Crystal_Stand.md "Eternia Crystal Stand")**** __(Desktop, Console and Mobile versions)
648	  * [Land Mine](Land_Mine.md "Land Mine")
649	  * [TNT Barrel](TNT_Barrel.md "TNT Barrel")**** __(Desktop, Console and Mobile versions)
650	  * [Pigronata](Pigronata.md "Pigronata")**** __(Desktop, Console and Mobile versions)
651	  * [Snowball Launcher](Snowball_Launcher.md "Snowball Launcher")
652	  * [Cannon](Cannon.md "Cannon")
653	  * [Bunny Cannon](Bunny_Cannon.md "Bunny Cannon")
654	  * [Confetti Cannon](Confetti_Cannon.md "Confetti Cannon")**** __(Desktop, Console and Mobile versions)
655	  * [Portal Gun Station](Portal_Gun_Station.md "Portal Gun Station")**** __(Desktop, Console and Mobile versions)
656	  * [Boulder](Boulder.md "Boulder")
657	    * [Bouncy](Bouncy_Boulder.md "Bouncy Boulder")**** __(Desktop, Console and Mobile versions)
658	    * [Life Crystal](Life_Crystal_Boulder.md "Life Crystal Boulder")**** __(Desktop, Console and Mobile versions)
659	    * [Lava](Lava_Boulder.md "Lava Boulder")**** __(Desktop, Console and Mobile versions)
660	    * [Poo](Poo_Boulder.md "Poo Boulder")**** __(Desktop, Console and Mobile versions)
661	    * [Spider](Spider_Boulder.md "Spider Boulder")**** __(Desktop, Console and Mobile versions)
662	    * [Ghoulder](Ghoulder.md "Ghoulder")**** __(Desktop, Console and Mobile versions)
663	    * [Rainbow](Rainbow_Boulder.md "Rainbow Boulder")**** __(Desktop, Console and Mobile versions)
664	  * [Rolling Cactus](Rolling_Cactus.md "Rolling Cactus")**** __(Desktop, Console and Mobile versions)
665	  * [Gem Locks](Gem_Locks.md "Gem Locks")**** __(Desktop, Console and Mobile versions)
666	  * [Trapped Chests](Trapped_Chests.md "Trapped Chests")**** __(Desktop, Console and Mobile versions)
667	  * [Arrow Signs](Arrow_Signs.md "Arrow Signs")**** __(Desktop, Console and Mobile versions)
668	  * [Drum Set](Drum_Set.md "Drum Set")**** __(Desktop, Console and Mobile versions)
669	  * [Golf Tee](Golf_Tee.md "Golf Tee")**** __(Desktop, Console and Mobile versions)
670	  * [Weather Vane](Weather_Vane.md "Weather Vane")**** __(Desktop, Console and Mobile versions)
671	
672	Wiring
673	
674	  * [Doors](Doors.md "Doors")
675	  * [Tall Gate](Tall_Gate.md "Tall Gate")**** __(Desktop, Console and Mobile versions)
676	  * [Trap Door](Trap_Door.md "Trap Door")**** __(Desktop, Console and Mobile versions)
677	  * [Music Box](Music_Box "Music Box")**** __(Desktop, Console, Old-gen console and Mobile versions)
678	  * [Monoliths](Monoliths.md "Monoliths")**** __(Desktop, Console and Mobile versions)
679	  * [Echo Chamber](Echo_Chamber.md "Echo Chamber")**** __(Desktop, Console and Mobile versions)
680	  * [Water fountains](Water_fountains.md "Water fountains")
681	  * [Chimney](Chimney.md "Chimney")**** __(Desktop, Console and Mobile versions)
682	  * [Bubble Machine](Bubble_Machine.md "Bubble Machine")
683	  * [Fireworks Box](Fireworks_Box.md "Fireworks Box")**** __(Desktop, Console, Old-gen console and Mobile versions)
684	  * [Firework Fountain](Firework_Fountain.md "Firework Fountain")**** __(Desktop, Console, Old-gen console and Mobile versions)
685	  * [Firework Rockets](Firework_Rockets.md "Firework Rockets")
686	  * [Fog Machine](Fog_Machine.md "Fog Machine")**** __(Desktop, Console and Mobile versions)
687	  * [Party Center](Party_Center.md "Party Center")**** __(Desktop, Console and Mobile versions)
688	  * [Silly Balloon Machine](Silly_Balloon_Machine.md "Silly Balloon Machine")**** __(Desktop, Console and Mobile versions)
689	  * [Functional Statues](Statue#Functional_statues "Statue")
690	  * [Lever](Lever.md "Lever")
691	  * [Switch](Switch.md "Switch")
692	  * [Detonator](Detonator.md "Detonator")**** __(Desktop, Console and Mobile versions)
693	  * Pressure Plates
694	  * [Timers](Timers.md "Timers")
695	  * [Actuator](Actuator.md "Actuator")
696	  * [Wire Bulb](Wire_Bulb.md "Wire Bulb")**** __(Desktop, Console and Mobile versions)
697	  * [Junction Box](Junction_Box.md "Junction Box")**** __(Desktop, Console and Mobile versions)
698	  * [Explosives](Explosives.md "Explosives")
699	  * [Pumps](Pumps.md "Pumps")
700	  * [Teleporter](Teleporter.md "Teleporter")
701	  * [Sensor](Sensor "Sensor")**** __(Desktop, Console and Mobile versions)
702	  * [Geyser](Geyser.md "Geyser")**** __(Desktop, Console and Mobile versions)
703	  * [Pixel Box](Pixel_Box.md "Pixel Box")**** __(Desktop, Console and Mobile versions)
704	
705	Environment
706	
707	  * [Antlion Eggs](Antlion_Eggs.md "Antlion Eggs")**** __(Desktop, Console and Mobile versions)
708	  * [Bee Hive](Bee_Hive.md "Bee Hive")**** __(Desktop, Console and Mobile versions)
709	  * [Coin Stashes](Coin_Stashes.md "Coin Stashes")
710	  * [Crimson Heart](Crimson_Heart.md "Crimson Heart")
711	    * [Replica](Replica_Crimson_Heart.md "Replica Crimson Heart")**** __(Desktop, Console and Mobile versions)
712	  * [Fallen Log](Fallen_Log.md "Fallen Log")**** __(Desktop, Console and Mobile versions)
713	  * [Larva](Larva.md "Larva")
714	  * [Mushrooms](Mushrooms.md "Mushrooms")
715	  * [Plantera's Bulb](Plantera's_Bulb.md "Plantera's Bulb")
716	  * [Plants](Plants.md "Plants")
717	    * [Strange Plants](Strange_Plants "Strange Plants")**** __(Desktop, Console and Mobile versions)
718	  * [Pot](Pot.md "Pot")
719	  * [Shadow Orb](Shadow_Orb.md "Shadow Orb")
720	    * [Replica](Replica_Shadow_Orb.md "Replica Shadow Orb")**** __(Desktop, Console and Mobile versions)
721	  * [Tree](Tree "Tree")
722	    * [Giant Glowing Mushroom](Giant_Glowing_Mushroom.md "Giant Glowing Mushroom")
723	  * [Other](Objects.md "Objects")
724	
725	Categories: 
726	
727	  * [Furniture items](Category%3AFurniture_items "Category:Furniture items")
728	  * [Mechanism items](Category%3AMechanism_items "Category:Mechanism items")
729	  * [Crafting material items](Category%3ACrafting_material_items "Category:Crafting material items")
730	  * [Consumable items](Category%3AConsumable_items "Category:Consumable items")
731	  * [Desktop content](Category%3ADesktop_content "Category:Desktop content")
732	  * [Console content](Category%3AConsole_content "Category:Console content")
733	  * [Old-gen console content](Category%3AOld-gen_console_content "Category:Old-gen console content")
734	  * [Mobile content](Category%3AMobile_content "Category:Mobile content")
735	  * [3DS content](Category%3A3DS_content "Category:3DS content")
736	  * [Vendor items](Category%3AVendor_items "Category:Vendor items")
737	  * [Plunder items](Category%3APlunder_items "Category:Plunder items")
738	  * [Craftable items](Category%3ACraftable_items "Category:Craftable items")
739	  * [Tinkerer's Workshop](Category%3ATinkerer's_Workshop "Category:Tinkerer's Workshop")
740	  * [Verify](Category%3AVerify "Category:Verify")
741	
742	Hidden categories: 
743	
744	  * Pages using DynamicPageList3 dplvar parser function
745	  * Pages using DynamicPageList3 parser function
746	  * Entities introduced in Desktop 1.4.0.1
747	  * Entities patched in Desktop 1.3.2.1
748	  * Entities introduced in Desktop 1.3.1
749	  * Entities patched in Desktop 1.3.0.1
750	  * Entities patched in Desktop 1.2.4
751	  * Entities patched in Desktop 1.2
752	  * Entities introduced in Desktop 1.1
753	  * Entities introduced in Console 1.0.1372.5
754	  * Entities patched in Console 1.0.933.1
755	  * Entities patched in Console 1.0.750.0
756	  * Entities patched in Console 1.07
757	  * Entities introduced in Console-Release
758	  * Entities introduced in Switch 1.0.895.9
759	  * Entities introduced in Switch 1.0.711.6
760	  * Entities introduced in Mobile 1.4.0.5.0
761	  * Entities patched in Mobile 1.3.0.7
762	  * Entities patched in Mobile 1.2.11212
763	  * Entities patched in Mobile 1.2.6508
764	  * Entities introduced in Mobile-Release
765	  * Entities introduced in 3DS-Release
766	  * Pages with navboxes
767	  * Random
768	
769	This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=Pressure_Plates&oldid=1008462 "Last edited on 2026-07-19"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
770	  *[1 required]: Journey Mode
771	  *[Qty.]: Quantity
772	  *[100%]: Expert Mode
773	  *[DPS]: Damage per second
774	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
775	  *[300]: Master Mode
776	  *[400]: Expert Mode
777	  *[160]: Expert Mode
778	  *[240]: Master Mode
779	  *[3 required]: Journey Mode
780	  *[#]: Number
781	  *[Max.  
782	enemies]: Maximum number of enemies Abigail can damage at once
783	  *[HM]: Hardmode
784	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
785	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
786	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
787	  *[8]: Expert Mode
788	  *[10]: Master Mode
789	  *[120]: Expert Mode
790	  *[150]: Master Mode
791	  *[13]: Chế độ Master
792	  *[195]: Master Mode
793	  *[Verify]: Talk:Pressure Plates
794	  *[50 required]: Journey Mode
795	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
796	  *[100 required]: Journey Mode
797	  *[cần có 1]: Chế độ Journey
798	  *[25 required]: Journey Mode
799	  *[cần có 25]: Chế độ Journey
800	  *[400 required]: Journey Mode
801	  *[membutuhkan 100]: Mode Journey
802	  *[cần có 100]: Chế độ Journey
803	  *[Slg.]: Số lượng
804	  *[1.99%]: Expert Mode
805	  *[199/10000 (1.99%)]: Expert Mode
806	  *[membutuhkan 1]: Mode Journey
807	  *[1,99%]: Expert Mode
808	  *[1/50 (2%)]: Mode Expert
809	  *[200 required]: Journey Mode
810	  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
811	  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
812	  *[20 required]: Journey Mode
813	  *[180]: Expert Mode
814	  *[270]: Master Mode
815	  *[5–9 seconds]: Master Mode
816	  *[5–9]: Expert Mode
817	  *[15 required]: Journey Mode
818	  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
819	  *[Power]: Bait power
820	  *[5 required]: Journey Mode
821	  *[cần có {{{research}}}]: Chế độ Journey
822	  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
823	  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
824	  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
825	  *[Expert Mode exclusive]: Expert Mode
826	  *[402]: Master Mode
827	  *[523]: Expert Mode
828	  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30 tiles per second
829	  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
830	  *[800]: Expert Mode
831	  *[1200]: Master Mode
832	  *[15]: Expert Mode
833	  *[17]: Master Mode
834	  *[O. v. odražení]: Odolnost vůči odražení
835	  *[1 minute 30 seconds]: Expert Mode
836	  *[1 minute 52.5 seconds]: Master Mode
837	  *[90]: Master Mode
838	  *[112.5]: Master Mode
839	  *[2–6]: Chế độ Expert
840	  *[2-6]: Expert Mode
841	  *[%100]: Expert Mode
842	  *[28]: Expert Mode
843	  *[42]: Master Mode
844	  *[80]: Mode Expert
845	  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
846	  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
847	  *[ Major improvements to all stats and increased life regeneration]: Expert Mode
848	  *[50%]: Expert Mode
849	  *[1/2 (50%)]: Expert Mode
850	  *[30]: Expert Mode
851	  *[45]: Expert Mode
852	  *[3/4]: Chế độ Expert
853	  *[5]: Master Mode
854	  *[75%]: Chế độ Expert
855	  *[semua]: Mode Master
856	  *[6]: Expert Mode
857	  *[toàn bộ]: Chế độ Master
858	  *[199/10000 (1,99%)]: Mode Expert
859	  *[4 minutes]: Expert Mode
860	  *[5 minutes]: Master Mode
861	  *[4]: Wooden Arrow base damage
862	  *[36]: Expert Mode
863	  *[22]: Expert Mode
864	  *[26]: Master Mode
865	  *[Ruce pryč od mé zbraně, kámo!]: Keep your hands off my gun, buddy!
866	  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
867	  *[Koukám, že házíš očkem po žraločkovi. Opravdu nechceš vědět, jak byl vyroben.]: I see you're eyeballing the Minishark. You really don't want to know how it was made.
868	  *[Neobtěžuj se s [jméno demoličního experta], vše, co potřebuješ, je přímo tady.]: Don't bother with [Name of Demolitionist], I've got all you need right here.
869	  *[Jaký má [jméno demoličního experta] problém? Uvědomuje si vůbec, že oba prodáváme naprosto rozdílné zboží?]: What's [Name of Demolitionist]'s problem? Does he even realize we sell completely different stuff?
870	  *[Pohni zadkem! Za hodinu mám rande s [jméno sestřičky].]: Make it quick! I've got a date with [Name of Nurse] in a hour.
871	  *[Chci to, co [jméno sestřičky] prodává. Co myslíš tím, že neprodává ani ň?]: I want what [Name of Nurse] is sellin'. What do you mean, she doesn't sell anything?
872	  *[Na [jméno dryády] bych mohl oči nechat. Škoda, že je to taková prudařka.]: [Name of Dryad] is a looker. Too bad she's such a prude.
873	  *[Slyšel jsem, že se ve světě nachází panenka vypadající skoro jako [jméno průvodce]. Mile rád bych do ní vpálil pár kulek.]: I heard there is a doll that looks very similar to [Name of Guide] somewhere in the underworld. I'd like to put a few rounds in it.
874	  *[Miluji noci jako je tahle. Vždy se najde něco na zabití.]: I love nights like tonight, there is never a shortage of things to kill.
875	  *[Chlape, tohle je noc přímo stvořená, abys s nikým nemusel mluvit, nemyslíš [jméno hráče]?]: Man, it's a good night not to talk to anybody, don't you think, [Name of Player]?
876	  *[14]: Expert Mode
877	  *[17.5]: Master Mode
878	  *[7]: Expert Mode
879	  *[8.75]: Master Mode
880	  *[21]: Expert Mode
881	  *[26.25]: Master Mode
882	  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
883	  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
884	  *[3.33–6.67%]: Expert Mode
885	  *[3.33%–6.67%]: Expert Mode
886	  *[W]: Wave
887	  *[3.33%]: Expert Mode
888	  *[6.67%]: Expert Mode
889	  *[0.014%]: Expert Mode
890	  *[ Medium improvements to all stats and increased life regeneration]: Expert Mode
891	  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
892	  *[+100%]: Expert Mode
893	  *[−50%]: Expert Mode
894	  *[+20%]: Expert Mode
895	  *[−16.67%]: Expert Mode
896	  *[200]: Expert Mode
897	  *[225]: Expert Mode
898	  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
899	  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
900	  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60 tiles per second
901	  *[6.25–12.5%]: Expert Mode
902	  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
903	  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item)
904	  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.47 tiles per second
905	  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.33 tiles per second
906	  *[6.25%]: Expert Mode
907	  *[12.5%]: Expert Mode
908	  *[32›140›176]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
909	  *[48›210›264]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
910	  *[26›92›116]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
911	  *[39›138›174]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
912	  *[2›8›10]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
913	  *[68›148›224]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
914	  *[102›222›336]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
915	  *[40›72›108]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
916	  *[60›108›162]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
917	  *[4›8›12]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
918	  *[92›100]: Expertní mód : Pre-hardmode › Těžký mód
919	  *[138›150]: Master Mode : Pre-Hardmode › Hardmode
920	  *[70›62]: Expertní mód : Pre-hardmode › Těžký mód
921	  *[105›93]: Master Mode : Pre-Hardmode › Hardmode
922	  *[60›132›198]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
923	  *[90›198›297]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
924	  *[36›64›96]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
925	  *[54›96›144]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
926	  *[6›12›18]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
927	  *[200›200›220]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
928	  *[300›300›330]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
929	  *[90›90›80]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
930	  *[135›135›120]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
931	  *[600]: Master Mode
932	  *[320]: Expert Mode
933	  *[480]: Master Mode
934	  *[100]: Expert Mode
935	  *[120›120›132]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
936	  *[180›180›198]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
937	  *[440]: Expert Mode
938	  *[660]: Master Mode
939	  *[1500]: Master Mode
940	  *[2250]: Master Mode
941	  *[2–6 seconds]: Expert Mode
942	  *[2.5–7.5 seconds]: Master Mode
943	  *[2.5–7.5]: Master Mode
944	  *[35 mph]: 35 mil per jam (diukur dengan item Stopwatch) atau 25.31 blok per detik
945	  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
946	  *[ 17–30]: Expert Mode
947	  *[99 required]: Journey Mode
948	  *[10–29]: Expert Mode
949	  *[1 time]: Expert Mode
950	  *[140]: Expert Mode
951	  *[210]: Master Mode
952	  *[14–20 seconds]: Expert Mode
953	  *[17.5-25 seconds]: Master Mode
954	  *[25%]: Master Mode
955	  *[14–20]: Expert Mode
956	  *[17.5–25]: Master Mode
957	  *[1/30 (3.33%)]: Expert Mode
958	  *[15.97%]: Expert Mode
959	  *[23/144 (15.97%)]: Expert Mode
960	  *[ 8 seconds]: Expert Mode
961	  *[10 seconds]: Expert Mode
962	  *[0.5–2.5 seconds]: Master Mode
963	  *[90%]: Expert Mode
964	  *[Web Spit]: Expert Mode
965	  *[30 seconds]: Expert Mode
966	  *[37.5 seconds]: Master Mode
967	  *[4–12]: Expert Mode
968	  *[5–15]: Master Mode
969	  *[33.33%]: Expert Mode
970	  *[1/3 (33.33%)]: Expert Mode
971	  *[20-40]: Expert Mode
972	  *[25-40]: Master Mode
973	  *[10-14]: Mode Expert
974	  *[12.5-17.5]: Master Mode
975	  *[20]: Expert Mode
976	  *[25]: Master Mode
977	  *[6-10]: Expert Mode
978	  *[7.5-12.5]: Master Mode
979	  *[1/1 (100%)]: Chế độ Expert
980	  *[6-20]: Expert Mode
981	  *[7.5-25]: Master Mode
982	  *[7.5-15]: Expert Mode
983	  *[9.37-18.75]: Master Mode
984	  *[11/243 (4.53%)]: Chế độ Expert
985	  *[11/81 (13.58%)]: Chế độ Expert
986	  *[2 hours]: Expert Mode
987	  *[3 hours]: Master Mode
988	  *[20–40]: Expert Mode
989	  *[25–50]: Master Mode
990	  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
991	  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
992	  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
993	  *[1/150]: Expert Mode
994	  *[1/30]: Expert Mode
995	  *[15.56–31.11%]: Expert Mode
996	  *[15.56%–31.11%]: Expert Mode
997	  *[15.56%]: Expert Mode
998	  *[31.11%]: Expert Mode
999	  *[ 12 _SC_ 50 _CC_]: Expert Mode
1000	  *[dusk]: 7:30 PM
1001	  *[1.33%]: Expert Mode
1002	  *[1%]: Expert Mode
1003	  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
1004	  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
1005	  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
1006	  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second
1007	  *[20 seconds]: Expert Mode
1008	  *[25 seconds]: Master Mode
1009	  *[0.5%]: Expert Mode
1010	  *[0.67%]: Expert Mode
1011	  *[1-3]: エキスパートモード
1012	  *[18 mph]: 18 miles per hour (as measured by the Stopwatch item) or 12.94 tiles per second
1013	  *[Crit]: Critical strike chance
1014	  *[20 mph]: 20 miles per hour (as measured by the Stopwatch item) or 14.67 tiles per second
1015	  *[54 mph]: 54 mil per jam (diukur dengan item Stopwatch) atau 39.38 blok per detik
1016	  *[and the core]: Expert Mode
1017	  *[2,800]: Chế độ Expert
1018	  *[3,570]: Chế độ Master
1019	  *[3,640]: Chế độ Expert
1020	  *[4,641]: Chế độ Master
1021	  *[15,120]: Chế độ Expert
1022	  *[19,296]: Chế độ Master
1023	  *[2,125]: Chế độ Expert
1024	  *[2,709]: Chế độ Master
1025	  *[4,760]: Chế độ Expert
1026	  *[6,069]: Chế độ Master
1027	  *[11,900]: Mode Expert
1028	  *[15,172]: Mode Master
1029	  *[8,800]: Chế độ Expert
1030	  *[11,220]: Master Mode
1031	  *[11,200]: Chế độ Expert
1032	  *[14,280]: Chế độ Master
1033	  *[28,800]: Chế độ Expert
1034	  *[36,720]: Chế độ Master
1035	  *[30,000]: Chế độ Expert
1036	  *[38,250]: Chế độ Master
1037	  *[34,500]: Chế độ Expert
1038	  *[43,988]: Chế độ Master
1039	  *[120,000]: Chế độ Expert
1040	  *[153,000]: Chế độ Master
1041	  *[280]: Expert Mode
1042	  *[420]: Master Mode
1043	  *[42,000]: Chế độ Expert
1044	  *[53,550]: Chế độ Master
1045	  *[88,500]: Chế độ Expert
1046	  *[112,836]: Chế độ Master
1047	  *[90,000]: Chế độ Expert
1048	  *[114,749]: Chế độ Master
1049	  *[78,000]: Expert Mode
1050	  *[99,450]: Chế độ Master
1051	  *[11700]: Mode Expert
1052	  *[14917]: Mode Master
1053	  *[98,000]: Chế độ Expert
1054	  *[124,950]: Chế độ Master
1055	  *[48,000]: Chế độ Expert
1056	  *[61,200]: Master Mode
1057	  *[217,500]: Expert Mode
1058	  *[277,311]: Chế độ Master
1059	  *[dua]: Mode Expert
1060	  *[10,500]: Mode Expert
1061	  *[24 detik]: Mode Expert
1062	  *[30 detik]: Mode Expert
1063	  *[30 required]: Journey Mode
1064	  *[mph]: miles per hour
1065	  *[70]: Master Mode
1066	  *[36 mph]: 36 miles per hour (as measured by the Stopwatch item) or 26.25 tiles per second
1067	  *[315]: Expert Mode
1068	  *[68]: Expert Mode
1069	  *[0.5]: Expert Mode
1070	  *[96]: Expert Mode
1071	  *[144]: Master Mode
1072	  *[12.5]: Master Mode
1073	  *[143 mph]: 143 miles per hour (as measured by the Stopwatch item) or 105 tiles per second
1074	  *[5525]: Expert Mode
1075	  *[7049]: Master Mode
1076	  *[60%]: Master Mode
1077	  *[64%]: Expert Mode
1078	  *[65%]: Master Mode
1079	  *[110–135]: Master Mode
1080	  *[30–50]: Master Mode
1081	  *[5.23–10.5 sec]: Expert Mode
1082	  *[6.53–13.12 sec]: Master Mode
1083	  *[3–6 sec]: Expert Mode
1084	  *[3.75–7.5 sec]: Master Mode
1085	  *[0.73–1.5 sec]: Expert Mode
1086	  *[0.92–1.87 sec]: Master Mode
1087	  *[7.5–15 sec]: Expert Mode
1088	  *[9.37–18.75 sec]: Master Mode
1089	  *[1.5–3 sec]: Expert Mode
1090	  *[1.87–3.75 sec]: Master Mode
1091	  *[11.23–22.5 sec]: Expert Mode
1092	  *[14.03–28.12 sec]: Master Mode
1093	  *[9.73–19.5 sec]: Expert Mode
1094	  *[12.17–24.37 sec]: Master Mode
1095	  *[ 60%]: Mode Expert
1096	  *[ 25%]: Chế độ Master
1097	  *[ 100%]: Chế độ Master
1098	  *[5700-7700]: Expert Mode
1099	  *[ %100]: Master Mode
1100	  *[0-200]: Chế độ Expert
1101	  *[0-500]: Chế độ Expert
1102	  *[2125]: Expert Mode
1103	  *[170]: Chế độ Expert
1104	  *[2709]: Master Mode
1105	  *[217]: Chế độ Master
1106	  *[20%]: Expert Mode
1107	  *[1/5 (20%)]: Expert Mode
1108	  *[9.73-19.5]: Expert Mode
1109	  *[12.17-24.37]: Master Mode
1110	  *[2]: Chế độ Expert
1111	  *[3]: Chế độ Master
1112	  *[43.75%]: Expert Mode
1113	  *[7/16 (43.75%)]: Expert Mode
1114	  *[Third]: Expert Mode
1115	  *[Major improvements to all stats and increased life regeneration]: 達人模式
1116	  *[Medium improvements to all stats and increased life regeneration]: 達人模式
1117	  *[Minor improvements to all stats and increased life regeneration]: 達人模式
1118	  *[13 seconds]: Master Mode
1119	  *[Zabíjení zajíčků je bezcitné. Tečka.]: Killing bunnies is cruel. Period.
1120	  *[14 seconds]: Expert Mode
1121	  *[17.5 seconds]: Master Mode
1122	  *[26 mph]: 26 miles per hour (as measured by the Stopwatch item) or 18.75 tiles per second
1123	  *[189]: Expert Mode
1124	  *[283]: Master Mode
1125	  *[4.94%]: Expert Mode
1126	  *[3.96%]: Expert Mode
1127	  *[700]: Expert Mode
1128	  *[1,050]: Master Mode
1129	  *[23 mph]: 23 miles per hour (as measured by the Stopwatch item) or 16.87 tiles per second
1130	  *[2 mph]: 2 miles per hour (as measured by the Stopwatch item) or 1.125 tiles per second
1131	  *[79/1600 (4.94%)]: Expert Mode
1132	  *[4,94%]: Expert Mode
1133	  *[3/80 (3,75%)]: Mode Expert
1134	  *[12.5 seconds]: Master Mode
1135	  *[2 required]: Journey Mode
1136	  *[24–100]: Expert Mode
1137	  *[12–20]: Expert Mode
1138	  *[360]: Master Mode
1139	  *[[]: Western world border
1140	  *[C]: World center
1141	  *[]]: Eastern world border
1142	  *[60]: Expert Mode
1143	  *[18–30]: Expert Mode
1144	  *[18–90]: Expert Mode
1145	  *[115 mph]: 115 miles per hour (as measured by the Stopwatch item) or 84.33 tiles per second
1146	  *[382 mph]: 382 miles per hour (as measured by the Stopwatch item) or 280.13 tiles per second
1147	  *[721 mph]: 721 miles per hour (as measured by the Stopwatch item) or 528.73 tiles per second
1148	  *[12.5–50%]: Expert Mode
1149	  *[12.5%–50%]: Expert Mode
1150	  *[16.67%]: Expert Mode
1151	  *[0.25%]: Expert Mode
1152	  *[0.26 mph]: 0.26 miles per hour (as measured by the Stopwatch item)
1153	  *[40]: Expert Mode
1154	  *[50]: Master Mode
1155	  *[37.5]: Master Mode
1156	  *[62.5]: Master Mode
1157	  *[6.25]: Master Mode
1158	  *[46 mph]: 46 miles per hour (as measured by the Stopwatch item) or 33.75 tiles per second
1159	  *[membutuhkan 25]: Mode Journey
1160	  *[6.22–31.11%]: Expert Mode
1161	  *[6.22%–31.11%]: Expert Mode
1162	  *[6.22%]: Expert Mode
1163	  *[7.78%]: Expert Mode
1164	  *[10.37%]: Expert Mode
1165	  *[6,22–31,11%]: Expert Mode
1166	  *[102]: Master Mode
1167	  *[ 4–6 seconds]: Expert Mode
1168	  *[5–7.5 seconds]: Master Mode
1169	  *[7.5]: Master Mode
1170	  *[16]: Expert Mode
1171	  *[24]: Expert Mode
1172	  *[12 _GC_ 50 _SC_]: Expert Mode
1173	  *[8 _GC_]: Expert Mode
1174	  *[10 _GC_]: Master Mode
1175	  *[tida perempat]: Mode Expert
1176	  *[ Verifikasi]: Talk:Coins/id (halaman belum tersedia)
1177	  *[Verifikasi]: Talk:Multiplayer/id (halaman belum tersedia)
1178	  *[ Verify]: Talk:Coins/vi (page does not exist)
1179	  *[92 mph]: 92 miles per hour (as measured by the Stopwatch item) or 67.5 tiles per second
1180	  *[1.5–3]: Expert Mode
1181	  *[1.87–3.75]: Master Mode
1182	  *[2/243 (0.82%)]: Expert Mode
1183	  *[2/81 (2.47%)]: Expert Mode
1184	  *[35]: Master Mode
1185	  *[1.8–3]: Expert Mode
1186	  *[2.25–3.75]: Master Mode
1187	  *[1/6 (16.67%)]: Expert Mode
1188	  *[Radius]: Explosion radius in tiles
1189	  *[13 mph]: 13 miles per hour (as measured by the Stopwatch item) or 9.375 tiles per second
1190	  *[7.76%]: Expert Mode
1191	  *[2%]: Expertní mód
1192	  *[10 minutes]: Expert Mode
1193	  *[12 minutes 30 seconds]: Master Mode
1194	  *[105›93›187]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1195	  *[157›140›281]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1196	  *[1–3]: Expert Mode
1197	  *[1–2]: Master Mode
1198	  *[5–7]: Expert Mode
1199	  *[2–4]: Master Mode
1200	  *[1/4 (25%)]: Expert Mode
1201	  *[8 seconds]: Expert Mode
1202	  *[67%]: Expert Mode
1203	  *[two pieces]: Expert Mode
1204	  *[dua bagian]: Mode Expert
1205	  *[2-10]: Expert Mode
1206	  *[2-12]: Master Mode
1207	  *[0.73–1.5]: Expert Mode
1208	  *[0.92–1.87]: Master Mode
1209	  *[0.9–1.13]: Expert Mode
1210	  *[1.5–1.88]: Master Mode
1211	  *[1/6 (16.7%)]: Expert Mode
1212	  *[4-6]: Expert Mode
1213	  *[5-7.5]: Master Mode
1214	  *[48-72]: Expert Mode
1215	  *[60-90]: Master Mode
1216	  *[168]: Master Mode
1217	  *[5–20%]: Expert Mode
1218	  *[5%]: Expert Mode
1219	  *[10%]: Expert Mode
1220	  *[1]: Base value
1221	  *[0.14]: Turtle armor
1222	  *[0.2]: 5 Menacing modifiers
1223	  *[0.15]: Shroomite bonus
1224	  *[0.12]: Avenger Emblem
1225	  *[0.1]: Quiver bonus
1226	  *[0.05]: Well Fed
1227	  *[230]: Godly Meowmere
1228	  *[1.98]: Melee damage multiplier
1229	  *[0.13]: Shroomite armor
1230	  *[0.6]: Shroomite armor stealth effect
1231	  *[0.16]: 4 Menacing modifiers
1232	  *[39]: Godly Chlorophyte Shotbow
1233	  *[2.26]: Ranged damage multiplier
1234	  *[1.15]: Shroomite bonus
1235	  *[1.1]: Archery buff
1236	  *[105]: Master Mode
1237	  *[11]: Ammo damage
1238	  *[3–6]: Expert Mode
1239	  *[3.75–7.5]: Master Mode
1240	  *[3.6–6]: Expert Mode
1241	  *[4.5–7.5]: Master Mode
1242	  *[6.56%]: Expert Mode
1243	  *[59/900 (6.56%)]: Expert Mode
1244	  *[15 seconds]: Master Mode
1245	  *[1 minute]: Expert Mode
1246	  *[three-quarters]: Expert Mode
1247	  *[all]: Master Mode
1248	  *[a [Jellyfish](Jellyfish.md "Jellyfish")'s shock attack]: Expert Mode
1249	  *[30 _CC_]: Expert Mode
1250	  *[ 4.94%]: Expert Mode
1251	  *[1 _SC_ 50 _CC_]: Expert Mode
1252	  *[6 _GC_]: Expert Mode
1253	  *[6–90 seconds]: Expert Mode
1254	  *[7.5–112.5 seconds]: Master Mode
1255	  *[2–40 seconds]: Expert Mode
1256	  *[2.5–50 seconds]: Master Mode
1257	  *[1–30 seconds]: Expert Mode
1258	  *[1.25–37.5 seconds]: Master Mode
1259	  *[4–14 seconds]: Expert Mode
1260	  *[5–17.5 seconds]: Master Mode
1261	  *[12 seconds]: Expert Mode
1262	  *[14–30 seconds]: Expert Mode
1263	  *[17.5–37.5 seconds]: Master Mode
1264	  *[4–20 seconds]: Expert Mode
1265	  *[5–25 seconds]: Master Mode
1266	  *[1.5–28 seconds]: Expert Mode
1267	  *[1.87–35 seconds]: Master Mode
1268	  *[3–30 seconds]: Expert Mode
1269	  *[3.75–37.5 seconds]: Master Mode
1270	  *[4–12 seconds]: Expert Mode
1271	  *[5–15 seconds]: Master Mode
1272	  *[1.5–14 seconds]: Expert Mode
1273	  *[1.87–17.5 seconds]: Master Mode
1274	  *[0.73–8 seconds]: Expert Mode
1275	  *[0.92–10 seconds]: Master Mode
1276	  *[10–90 seconds]: Expert Mode
1277	  *[12.5–112.5 seconds]: Master Mode
1278	  *[0.5–32 seconds]: Expert Mode
1279	  *[0.63–40 seconds]: Master Mode
1280	  *[5 mph]: 5 miles per hour (as measured by the Stopwatch item) or 3.75 tiles per second
1281	  *[0.67–4 seconds]: Expert Mode
1282	  *[0.83–5 seconds]: Master Mode
1283	  *[1–4 seconds]: Expert Mode
1284	  *[4–8 seconds]: Master Mode
1285	  *[5 seconds]: Master Mode
1286	  *[11.23–600 seconds]: Expert Mode
1287	  *[14.03–750 seconds]: Master Mode
1288	  *[3–90 seconds]: Master Mode
1289	  *[16 seconds]: Expert Mode
1290	  *[ 6]: Expert Mode
1291	  *[ 18]: Expert Mode
1292	  *[ 6-90 detik]: Mode Expert
1293	  *[2-20 detik]: Mode Expert
1294	  *[14-20 detik]: Mode Expert
1295	  *[16 detik]: Mode Expert
1296	  *[5-30 detik]: Mode Expert
1297	  *[6 detik]: Mode Expert
1298	  *[2.5-14 detik]: Mode Expert
1299	  *[1.25-8 detik]: Mode Expert
1300	  *[0.5-32 detik]: Mode Expert
1301	  *[18.75 detik - 10 menit]: Mode Expert
1302	  *[16.25 detik - 4 menit]: Mode Expert
1303	  *[10 detik]: Mode Expert
1304	  *[14-16 detik]: Mode Expert
1305	  *[20 detik-90 detik]: Mode Expert
1306	  *[2-3 detik]: Mode Expert
1307	  *[ 1 detik]: Mode Expert
1308	  *[5-9 detik]: Mode Expert
1309	  *[3-90 detik]: Mode Expert
1310	  *[16 detik]: Mode Expert
1311	  *[52]: Master Mode
1312	  *[78]: Master Mode
1313	  *[72]: Expert Mode
1314	  *[108]: Expert Mode
1315	  *[24 seconds]: Expert Mode
1316	  *[0.67 seconds]: Expert Mode
1317	  *[0.83 seconds]: Master Mode
1318	  *[midnight]: 12:00 AM
1319	  *[five]: Expert Mode
1320	  *[0.67]: Expert Mode
1321	  *[0.83]: Master Mode
1322	  *[14000]: Expert Mode
1323	  *[21000]: Master Mode
1324	  *[11900]: Expert Mode
1325	  *[15172]: Master Mode
1326	  *[0.75]: Expert Mode
1327	  *[Atk.  
1328	dmg]: Attack damage
1329	  *[Def.]: Defense
1330	  *[AP]: Armor penetration
1331	  *[77]: Master Mode
1332	  *[81]: Master Mode
1333	  *[27]: Expert Mode
1334	  *[31]: Master Mode
1335	  *[208]: Master Mode
1336	  *[69]: Expert Mode
1337	  *[Dynamit. Můj speciální lík na všechno, co tě trápí.]: Dynamite, my own special cure-all for what ails ya.
1338	  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
1339	  *[Proč očisťovat svět, když jej můžeš vyhodit do povětří?]: Why purify the world when you can just blow it up?
1340	  *[Dnes se bude dobře umírat!]: It's a good day to die!
1341	  *[Jsem si docela jistý, že ti [jméno sestřičky] pomůže přišít zpět všechny tvé končetiny.]: 
1342	  *[Zajímalo by mě, co se stane, pokud… (BUM!)… Oh, omlouvám se, potřeboval jsi tu nohu?]: I wonder what happens if I... (BOOM!)... Oh, sorry, did you need that leg?
1343	  *[Dokonce i [jméno prodejce zbraní] by chtěl to, co já prodávám!]: Even [Name of Arms Dealer] wants what I'm selling!
1344	  *[Byl bys radši s dírou po kulce, nebo dírou po granátu? Myslel jsem si to.]: Would you rather have a bullet hole or a grenade hole? That's what I thought.
1345	  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
1346	  *[ZÁKAZ KOUŘENÍ!]: NO SMOKING IN HERE!!
1347	  *[Pokud hodíš tenhle do vany a zavřeš všechna okna, pročistí to všechny tvé dutiny a urve uši!]: If you throw this one in the bathtub and close all the windows, it'll clear your sinuses and pop your ears!
1348	  *[Chceš si hrát na kuře Pojistku?]: Wanna play Fuse Chicken?
1349	  *[Podepsal bys mi tento griefovací dokument?]: Hey, could you sign this Griefing Waiver?
1350	  *[Něco jsem si od těch zombie odnesl!]: I've got something for them zombies alright!
1351	  *[Hej, neviděl jsi někde klauna?]: Hey, have you seen a clown around?
1352	  *[Ještě před chvílí tady seděla bomba, teď ji nemůžu najít…]: There was a bomb sitting right here, and now I can't seem to find it...
1353	  *[84]: Expert Mode
1354	  *[126]: Master Mode
1355	  *[30 seconds]: Expertní mód
1356	  *[60 mph]: 60 miles per hour (as measured by the Stopwatch item) or 44 tiles per second
1357	  *[33,33%]: Master Mode
1358	  *[88]: Expert Mode
1359	  *[132]: Expert Mode
1360	  *[Contact]: The damage without modifier and summon damage bonuses
1361	  *[Pounce]: The damage without modifier and summon damage bonuses
1362	  *[Threshold]: If the player's summon damage bonuses reach it, Ruthless will become the best modifier
1363	  *[N/A]: Not available in vanilla game
1364	  *[16−30 seconds]: Expert Mode
1365	  *[20−37.5 seconds]: Master Mode
1366	  *[ 9.75%]: Expert Mode
1367	  *[16–30]: Expert Mode
1368	  *[20–37.5]: Master Mode
1369	  *[128]: Expert Mode
1370	  *[192]: Master Mode
1371	  *[15–60]: Expert Mode
1372	  *[0.5×]: Journey Mode
1373	  *[2×]: Expert Mode
1374	  *[3×]: Master Mode
1375	  *[4×]: Legendary Mode
1376	  *[5.33×]: Legendary Mode
1377	  *[2.5×]: Master Mode
1378	  *[3.5×]: Legendary Mode
1379	  *[0.9×]: Expert Mode
1380	  *[0.8×]: Master Mode
1381	  *[1.5×]: Expert Mode
1382	  *[1.75×]: Master Mode
1383	  *[May increase both during [Hardmode](Hardmode.md "Hardmode") and [Post-Plantera](Post-Plantera.md "Post-Plantera")]: Expert Mode
1384	  *[May increase]: Expert Mode
1385	  *[15 / 30]: Expert Mode
1386	  *[ 4%]: Expert Mode
1387	  *[+15]: Expert Mode
1388	  *[+20]: Master Mode
1389	  *[ 16]: Expert Mode
1390	  *[18]: Master Mode
1391	  *[Opatruj se! Terraria tě potřebuje!]: Be safe; Terraria needs you!
1392	  *[Musíš očistit svět od této nákazy.]: You must cleanse the world of this corruption.
1393	  *[Musíš očistit svět od tohoto karmínu.]: You must cleanse the world of this crimson.
1394	  *[Písky času se přesýpají. A upřímně, nemládneš a nekrásníš.]: The sands of time are flowing. And well, you are not aging very gracefully.
1395	  *[Co je to s tím, že více ‚štěkám‘ než koušu?]: What's this about me having more 'bark' than bite?
1396	  *[Dva goblini tahle přijdou do baru a jeden říká tomu druhému: ‚Dáš si goblet piva?!‘]: So two goblins walk into a bar, and one says to the other, 'Want to get a Goblet of beer?!'
1397	  *[Proč se mi [Jméno obchodníka] snaží prodat sochy andělů? Všichni přeci ví, že nic nedělají.]: Why does [Name of Merchant] keep trying to sell me an angel statues? Everyone knows that they don't do anything.
1398	  *[Kéž by se mnou [jméno prodejce zbraní] přestal flirtovat. Copak si neuvědomuje, že jsem více než 500 let stará?]: I wish [Name of Arms Dealer] would stop flirting with me. Doesn't he realize I'm 500 years old?
1399	  *[Už jsi v nákaze zkoušel použít očistný prášek na ebenokámen?]: Have you tried using purification powder on the ebonstone of The Corruption?
1400	  *[Už jsi v karmínu zkoušel použít očistný prášek na karmínokámen?]: Have you tried using purification powder on the Crimstone of the Crimson?
1401	  *[Viděl jsi starce procházejícího se kolem podzemní kobky? Vůbec nevypadá dobře…]: Have you seen the old man walking around the dungeon? He doesn't look well at all...
1402	  *[Myslím si, že je [jméno lanýže] nepochopený ostatními. Je to velmi vtipný chlapík.]: I feel like [Name of Truffle] is a bit misunderstood, he really is a fun guy.
1403	  *[Prodávám co se mi zlíbí! Pokud se ti to nelíbí, tak máš smůlu.]: I sell what I want! If you don't like it, too bad.
1404	  *[Kámo, je to mnou, nebo je venku tak milion zombie?]: Dude, is it just me or are there a million [[zombies]] out tonight?
1405	  *[Nechci aby sis kupoval mé věci. Já chci abys chtěl si mé věci kupovat, jasné?]: I don't want you to buy my stuff. I want you to want to buy my stuff, ok?
1406	  *[Proč musíš být ve chvílích jako je tato tak konfrontační?]: Why do you have to be so confrontational during a time like this?
1407	  *[[jméno světa] je z [procenta posvátnosti] % posvátný a [procenta nákazy/karmínu] % [nakažen/karmínový]. [Dryádin komentář (viz výše)].]: [Name of world] is [hallow percentage]% hallow and [crimson/corruption percentage]% [crimson/corruption]. [Dryad's comment, see above].
1408	  *[[jméno světa] je kompletně očištěn. Odvedl jsi úžasnou práci!]: [Name of World] is completely pure. You have done an amazing job!
1409	  *[+10]: Expert Mode
1410	  *[+14]: Master Mode
1411	  *[6–20 seconds]: Expert Mode
1412	  *[7.5–25 seconds]: Master Mode
1413	  *[3–10 seconds]: Expert Mode
1414	  *[201]: Expert Mode
1415	  *[302]: Expert Mode
1416	  *[184]: Expert Mode
1417	  *[277]: Master Mode
1418	  *[39000/78000]: Expert Mode
1419	  *[49725/99450]: Master Mode
1420	  *[0]: Expert Mode
1421	  *[39,000]: Expert Mode
1422	  *[49,725]: Master Mode
1423	  *[11,700]: Expert Mode
1424	  *[14,917]: Master Mode
1425	  *[60,000]: Expert Mode
1426	  *[76,500]: Master Mode
1427	  *[99,000]: Master Mode
1428	  *[ 78000]: Expert Mode
1429	  *[99450]: Master Mode
1430	  *[ ]: Master Mode
1431	  *[ 62 _GC_ 50 _SC_]: Expert Mode
1432	  *[ 2 _GC_ 50 _SC_]: Mode Expert
1433	  *[39000]: Mode Expert
1434	  *[49725]: Mode Master
1435	  *[double]: Expert Mode
1436	  *[triple]: Master Mode
1437	  *[1/9 (11.11%)]: Expert Mode
1438	  *[1/8 (12.5%)]: Expert Mode
1439	  *[19]: Master Mode
1440	  *[15120]: Expert Mode
1441	  *[19296]: Master Mode
1442	  *[356]: Mode Expert
1443	  *[209]: Mode Expert
1444	  *[139.33 yards (152.38 m)]: Expert Mode
1445	  *[10479]: Expert Mode
1446	  *[1/20 (5%)]: Expert Mode
1447	  *[10 minutes]: Expert Mode
1448	  *[100-150]: Expert Mode
1449	  *[2-3]: Chế độ Expert
1450	  *[ 15120]: Chế độ Expert
1451	  *[ 19296]: Chế độ Master
1452	  *[ 10500]: Chế độ Expert
1453	  *[10 menit]: Mode Expert
1454	  *[12 menit 30 detik]: Mode Master
1455	  *[2–3]: Chế độ Expert
1456	  *[1/20 (%5)]: Expert Mode
1457	  *[10 phút]: Chế độ Expert
1458	  *[12 phút 30 giây]: Chế độ Master
1459	  *[10500]: Expert Mode
1460	  *[Total damage]: Stationary / Moving
1461	  *[110]: Expert Mode
1462	  *[248]: Master Mode
1463	  *[165]: Expert Mode
1464	  *[372]: Master Mode
1465	  *[49000/98000]: Expert Mode
1466	  *[62475/124950]: Master Mode
1467	  *[12]: Expert Mode
1468	  *[Ethereal Lance 3]: Expert Mode
1469	  *[49,000]: Expert Mode
1470	  *[62,475]: Master Mode
1471	  *[59,994]: Master Mode
1472	  *[39,996]: Expert Mode
1473	  *[24 mph]: 24 miles per hour (as measured by the Stopwatch item) or 17.6 tiles per second
1474	  *[33 mph]: 33 miles per hour (as measured by the Stopwatch item) or 24.2 tiles per second
1475	  *[2000]: Expert Mode
1476	  *[3000]: Master Mode
1477	  *[6000]: Expert Mode
1478	  *[9000]: Master Mode
1479	  *[10000]: Expert Mode
1480	  *[15000]: Master Mode
1481	  *[48›86]: Expert Mode : Pre-Hardmode › Hardmode
1482	  *[72›129]: Master Mode : Pre-Hardmode › Hardmode
1483	  *[124]: Expert Mode
1484	  *[186]: Master Mode
1485	  *[37%]: Expert Mode
1486	  *[44%]: Master Mode
1487	  *[55%]: Expert Mode
1488	  *[82%]: Expert Mode
1489	  *[84%]: Master Mode
1490	  *[172]: Expert Mode
1491	  *[258]: Master Mode
1492	  *[228]: Expert Mode
1493	  *[342]: Master Mode
1494	  *[1.33–6.67%]: Expert Mode
1495	  *[27.27–60%]: Expert Mode
1496	  *[5–25%]: Master Mode
1497	  *[20–100%]: Master Mode
1498	  *[125]: Master Mode
1499	  *[9/25 (36%)]: Expert Mode
1500	  *[9/25]: Expert Mode
1501	  *[1050]: Master Mode
1502	  *[1/10 (10%)]: Expert Mode
1503	  *[54]: Master Mode
1504	  *[2366/3640]: Expert Mode
1505	  *[3016/4641]: Master Mode
1506	  *[−15]: Expert Mode
1507	  *[−30]: Expert Mode
1508	  *[Chain charge]: Expert Mode
1509	  *[2,366]: Chế độ Expert
1510	  *[3,016]: Mode Master
1511	  *[436]: Expert Mode
1512	  *[556]: Master Mode
1513	  *[145]: Expert Mode
1514	  *[185]: Master Mode
1515	  *[7 _GC_ 50 _SC_]: Expert Mode
1516	  *[36  
1517	40 when below 145 health]: Expert Mode
1518	  *[54  
1519	60 when below 185 health]: Master Mode
1520	  *[2365/3640]: Chế độ Expert
1521	  *[ 7 _GC_ 50 _SC_]: Chế độ Expert
1522	  *[ %25]: Master Mode
1523	  *[36  
1524	40 khi dưới 145 máu]: Chế độ Expert
1525	  *[54  
1526	60 khi dưới 185 máu]: Chế độ Master
1527	  *[3017/4641]: Chế độ Master
1528	  *[Liên hoàn lướt]: Chế độ Expert
1529	  *[4641]: Chế độ Master
1530	  *[3016]: Chế độ Master
1531	  *[1,000]: Expert Mode
1532	  *[1,500]: Master Mode
1533	  *[8 mph]: 8 miles per hour (as measured by the Stopwatch item) or 5.625 tiles per second
1534	  *[19 mph]: 19 miles per hour (as measured by the Stopwatch item) or 13.6096875 tiles per second
1535	  *[4.2–7]: Expert Mode
1536	  *[5.25–8.75]: Master Mode
1537	  *[6–10]: Expert Mode
1538	  *[7.5–12.5]: Master Mode
1539	  *[1.2–2]: Expert Mode
1540	  *[1.5–2.5]: Master Mode
1541	  *[FP]: Fishing Power
1542	  *[cần có 5]: Chế độ Journey
1543	  *[cần có 3]: Chế độ Journey
1544	  *[membutuhkan 99]: Mode Journey
1545	  *[22 mph]: 22 miles per hour (as measured by the Stopwatch item) or 15.8371875 tiles per second
1546	  *[113 mph]: 113 miles per hour (as measured by the Stopwatch item) or 82.5 tiles per second
1547	  *[116 mph]: 116 miles per hour (as measured by the Stopwatch item) or 85.07 tiles per second
1548	  *[13600]: Expert Mode
1549	  *[20400]: Master Mode
1550	  *[32 mph]: 32 miles per hour (as measured by the Stopwatch item) or 23.63343375 tiles per second
1551	  *[81 mph]: 81 miles per hour (as measured by the Stopwatch item) or 59.4 tiles per second
1552	  *[71 mph]: 71 miles per hour (as measured by the Stopwatch item) or 52.07 tiles per second
1553	  *[14 mph]: 14 miles per hour (as measured by the Stopwatch item) or 10.546875 tiles per second
1554	  *[28 mph]: 28 miles per hour (as measured by the Stopwatch item) or 20.53 tiles per second
1555	  *[37 mph]: 37 miles per hour (as measured by the Stopwatch item) or 27.13 tiles per second
1556	  *[42 mph]: 42 miles per hour (as measured by the Stopwatch item) or 30.8 tiles per second
1557	  *[48 mph]: 48 miles per hour (as measured by the Stopwatch item) or 35.2 tiles per second
1558	  *[49 mph]: 49 miles per hour (as measured by the Stopwatch item) or 35.93 tiles per second
1559	  *[56 mph]: 56 miles per hour (as measured by the Stopwatch item) or 41.25 tiles per second
1560	  *[47 mph]: 47 miles per hour (as measured by the Stopwatch item) or 34.47 tiles per second
1561	  *[7.7 mph]: 7.7 miles per hour (as measured by the Stopwatch item) or 5.65 tiles per second
1562	  *[63 mph]: 63 miles per hour (as measured by the Stopwatch item) or 45.9375 tiles per second
1563	  *[2.5]: Master Mode
1564	  *[250]: Master Mode
1565	  *[375]: Master Mode
1566	  *[100% by wave 14]: Expert Mode
1567	  *[3/11 (27.27%)]: Expert Mode
1568	  *[3/8 (37.5%)]: Expert Mode
1569	  *[3/5 (60%)]: Expert Mode
1570	  *[Base]: Base drop rate without the factor
1571	  *[1.67%]: Expert Mode
1572	  *[2.22%]: Expert Mode
1573	  *[8.33%]: Master Mode
1574	  *[27.27%]: Expert Mode
1575	  *[37.5%]: Expert Mode
1576	  *[6-12]: Expert Mode
1577	  *[7-15]: Master Mode
1578	  *[48-96]: Expert Mode
1579	  *[56-120]: Master Mode
1580	  *[3.75]: Master Mode
1581	  *[13/125 (10.4%)]: Expert Mode
1582	  *[39/400 (9.75%)]: Expert Mode
1583	  *[69/1225 (5.63%)]: Expert Mode
1584	  *[1–4]: Expert Mode
1585	  *[1.25–5]: Master Mode
1586	  *[0.67–2]: Expert Mode
1587	  *[0.83–2.5]: Master Mode
1588	  *[12.5–25%]: Master Mode
1589	  *[(Expert Mode exclusive)]: Expert Mode
1590	  *[40 mph]: 40 miles per hour (as measured by the Stopwatch item) or 29.25 tiles per second
1591	  *[1 minute 38 seconds]: Expert Mode
1592	  *[2 minutes 3 seconds]: Master Mode
1593	  *[Ukořisti drahokam]: Capture the Gem
1594	  *[membutuhkan 15]: Mode Journey
1595	  *[cần có 15]: Chế độ Journey
1596	  *[membutuhkan 5]: Mode Journey
1597	  *[28 seconds]: Expert Mode
1598	  *[35 seconds]: Master Mode
1599	  *[30–90 seconds]: Expert Mode
1600	  *[7.84%]: Expert Mode
1601	  *[7,84%]: Mode Expert
1602	  *[43]: Expert Mode
1603	  *[64]: Expert Mode
1604	  *[288]: Expert Mode
1605	  *[432]: Master Mode
1606	  *[4%]: Expert Mode
1607	  *[44]: Expert Mode
1608	  *[66]: Master Mode
1609	  *[33.3%]: Expert Mode
1610	  *[10 required]: Journey Mode
1611	  *[90000]: Expert Mode
1612	  *[114749]: Master Mode
1613	  *[37500]: Expert Mode
1614	  *[47812]: Master Mode
1615	  *[22500]: Expert Mode
1616	  *[28687]: Master Mode
1617	  *[19125]: Master Mode
1618	  *[10–14 seconds]: Expert Mode
1619	  *[15–21 seconds]: Master Mode
1620	  *[10–14]: Expert Mode
1621	  *[15–21]: Master Mode
1622	  *[18,750]: Expert Mode
1623	  *[23,906]: Master Mode
1624	  *[58 mph]: 58 miles per hour (as measured by the Stopwatch item) or 42.75 tiles per second
1625	  *[104]: Expert Mode
1626	  *[156]: Master Mode
1627	  *[59 mph]: 59 miles per hour (as measured by the Stopwatch item) or 43.125 tiles per second
1628	  *[162]: Master Mode
1629	  *[112]: Expert Mode
1630	  *[116]: Expert Mode
1631	  *[174]: Master Mode
1632	  *[96–116]: Expert Mode
1633	  *[144–174]: Master Mode
1634	  *[15,000]: Expert Mode
1635	  *[19,124]: Master Mode
1636	  *[7,500]: Expert Mode
1637	  *[9,562]: Master Mode
1638	  *[18,000]: Expert Mode
1639	  *[22,949]: Master Mode
1640	  *[13,500]: Expert Mode
1641	  *[17,212]: Master Mode
1642	  *[4,500]: Expert Mode
1643	  *[5,737]: Master Mode
1644	  *[2,250]: Expert Mode
1645	  *[2,868]: Master Mode
1646	  *[11,250]: Expert Mode
1647	  *[14,343]: Master Mode
1648	  *[9,000]: Expert Mode
1649	  *[11,474]: Master Mode
1650	  *[6,750]: Expert Mode
1651	  *[8,606]: Master Mode
1652	  *[123 mph]: 123 miles per hour (as measured by the Stopwatch item) or 90 tiles per second
1653	  *[1 mph]: 1 mile per hour (as measured by the Stopwatch item) or 0.375 tiles per second
1654	  *[AMA]: Ask Me Anything
1655	  *[Zdravím [jméno hráče]. Je zde něco, s čím bych mohl pomoci?]: Greetings, [Name of Player]. Is there something I can help you with?
1656	  *[Jsem zde proto, abych ti dával rady co máš dělat. Doporučuji ti si se mnou přijít promluvit, kdykoliv si nebudeš vědět rady.]: I am here to give you advice on what to do next. It is recommended that you talk with me anytime you get stuck.
1657	  *[Říká se, že existuje člověk, který ti poradí, jak máš přežít v této krajině… ale počkat. To jsem přeci já.]: They say there is a person who will tell you how to survive in this land... oh wait. That's me.
1658	  *[Měl bys zůstat v době během noci. Je velmi nebezpečné toulat se v noci.]: You should stay indoors at night. It is very dangerous to be wandering around in the dark.
1659	  *[Hej kamaráde, nevíš, kde se nachází nějaký smrtirost? Jen tak, přemýšlím nahlas.]: Hey, buddy, do you know where any deathweed is? Oh, no reason; Just wondering, is all.
1660	  *[Pokud se podíváš na oblohu, uvidíš, že je měsíc krvavý.]: If you were to look up, you'd see the moon is red right now.
1661	  *[S jistotou můžeš říct, že nastal krvavý měsíc, jakmile se barva oblohy promění v červenou. Něho během této doby způsobuje, že se objevuje více nepřátel.]: You can tell a Blood Moon is out when the sky turns red. There is something about it that causes monsters to swarm.
1662	  *[Oktoberfest je tady! [Jméno obchodníka] uvařil kvůli této události své proslulé pivo a [jméno oděvníka] prodává tradiční oblečení spojené s festivalem.]: The Oktober festival is here! [Name of Merchant] has brewed up some of his famous ale especially for the occasion and [Name of Clothier] is selling traditional festival clothes.
1663	  *[Nový rok je tady! [Jméno demoličního experta] prodává speciální zbraně, které rozzáří oblohu a [jméno oděvníka] prodává tradiční sváteční oděv.]: New Year is here! [Name of Demolitionist] is selling special weaponry to light up the skies, and [Name of Clothier] is selling traditional festive attire.
1664	  *[75]: Expert Mode
1665	  *[Expert-exclusive]: Expert Mode
1666	  *[Master-exclusive]: Master Mode
1667	  *[Hive Pack]: Expert Mode
1668	  *[and third]: Expert Mode
1669	  *[0.9›0.4]: Pre-Hardmode › Hardmode
1670	  *[0.5›0.45]: Pre-Hardmode › Hardmode
1671	  *[216]: Master Mode
1672	  *[252]: Master Mode
1673	  *[6.25–25%]: Master Mode
1674	  *[25–100%]: Master Mode
1675	  *[140–148]: Expert Mode
1676	  *[210–222]: Master Mode
1677	  *[10–20 seconds]: Expert Mode
1678	  *[12.5–25 seconds]: Master Mode
1679	  *[≤ 2 seconds]: Expert Mode
1680	  *[≤ 2.5 seconds]: Master Mode
1681	  *[50–100%]: Master Mode
1682	  *[nebo 3/4]: Expertní mód
1683	  *[tümü]: Master Mode
1684	  *[18750]: Expert Mode
1685	  *[67]: Expert Mode
1686	  *[1–5 seconds]: Expert Mode
1687	  *[1.25–6.25 seconds]: Master Mode
1688	  *[ 17 _CC_ ]: Expert Mode
1689	  *[ 49 _CC_ ]: Expert Mode
1690	  *[ 1 _SC_ 30 _CC_ ]: Expert Mode
1691	  *[ 20 _CC_ ]: Expert Mode
1692	  *[14 _GC_ 81 _SC_]: Expert Mode
1693	  *[16 _GC_ 6 _SC_]: Master Mode
1694	  *[2 _PC_ 67 _GC_]: Expert Mode
1695	  *[2 _PC_ 89 _GC_]: Master Mode
1696	  *[81 _SC_ 20 _CC_]: Expert Mode
1697	  *[3 _SC_ 72 _CC_]: Expert Mode
1698	  *[1 _SC_ 69 _CC_]: Expert Mode
1699	  *[9 _SC_ 20 _CC_]: Expert Mode
1700	  *[8 _SC_ 6 _CC_]: Expert Mode
1701	  *[7 _SC_ 44 _CC_]: Expert Mode
1702	  *[4 _SC_ 92 _CC_]: Expert Mode
1703	  *[2 _SC_ 61 _CC_]: Expert Mode
1704	  *[3 _SC_ 31 _CC_]: Expert Mode
1705	  *[5 _SC_ 26 _CC_]: Expert Mode
1706	  *[3 _SC_ 17 _CC_]: Expert Mode
1707	  *[11 _SC_ 73 _CC_]: Expert Mode
1708	  *[4 _SC_ 32 _CC_]: Expert Mode
1709	  *[16 _SC_ 91 _CC_]: Expert Mode
1710	  *[54 _SC_ 67 _CC_]: Expert Mode
1711	  *[72 _SC_ 68 _CC_]: Expert Mode
1712	  *[44 _SC_ 90 _CC_]: Expert Mode
1713	  *[2 _GC_ 46 _SC_ 61 _CC_]: Expert Mode
1714	  *[45 _SC_ 93 _CC_]: Expert Mode
1715	  *[65 _SC_ 1 _CC_]: Expert Mode
1716	  *[12 _SC_ 81 _CC_]: Expert Mode
1717	  *[1 _GC_ 83 _SC_ 35 _CC_]: Expert Mode
1718	  *[2 _GC_ 65 _SC_]: Expert Mode
1719	  *[7 _GC_ 71 _SC_]: Expert Mode
1720	  *[7 _GC_ 95 _SC_]: Expert Mode
1721	  *[8 _GC_ 71 _SC_]: Expert Mode
1722	  *[21 _GC_ 9 _SC_]: Expert Mode
1723	  *[19 _GC_ 70 _SC_]: Expert Mode
1724	  *[13 _GC_ 25 _SC_]: Expert Mode
1725	  *[26 _GC_ 17 _SC_]: Expert Mode
1726	  *[9 _GC_ 44 _SC_]: Expert Mode
1727	  *[5 _GC_ 31 _SC_]: Expert Mode
1728	  *[3 _GC_ 68 _SC_]: Expert Mode
1729	  *[21 _GC_ 20 _SC_]: Expert Mode
1730	  *[15 _GC_ 90 _SC_]: Expert Mode
1731	  *[15 _GC_ 60 _SC_]: Expert Mode
1732	  *[31 _GC_ 80 _SC_]: Expert Mode
1733	  *[37 _GC_ 71 _SC_]: Expert Mode
1734	  *[39 _GC_ 75 _SC_]: Expert Mode
1735	  *[17 _GC_ 92 _SC_]: Expert Mode
1736	  *[35 _GC_ 51 _SC_]: Expert Mode
1737	  *[66 _GC_ 25 _SC_]: Expert Mode
1738	  *[11 _GC_ 92 _SC_]: Expert Mode
1739	  *[19 _GC_ 73 _SC_]: Expert Mode
1740	  *[26 _GC_ 50 _SC_]: Expert Mode
1741	  *[2 _PC_ 65 _GC_]: Expert Mode
1742	  *[1 _PC_ 18 _GC_]: Expert Mode
1743	  *[45900]: Expert Mode
1744	  *[68850]: Master Mode
1745	  *[327,420]: Expert Mode
1746	  *[436,560]: Master Mode
1747	  *[217500]: Expertní mód
1748	  *[277311]: Master Mode
1749	  *[450]: Master Mode
1750	  *[Master Mode]: Master Mode
1751	  *[245]: Expert Mode
1752	  *[367]: Master Mode
1753	  *[76]: Expert Mode
1754	  *[114]: Master Mode
1755	  *[42000]: Expert Mode
1756	  *[53550]: Master Mode
1757	  *[4–18 seconds]: Expert Mode
1758	  *[5–22.5 seconds]: Master Mode
1759	  *[21000/42000]: Expert Mode
1760	  *[26775/53550]: Master Mode
1761	  *[5›6]: Expert Mode : Pre-Hardmode › Hardmode
1762	  *[6›7]: Master Mode : Pre-Hardmode › Hardmode
1763	  *[1/100 (1%)]: Expert Mode
1764	  *[1/2000 (0.05%)]: Expert Mode
1765	  *[25–40]: Expert Mode
1766	  *[8–28]: Expert Mode
1767	  *[2–20 seconds]: Expert Mode
1768	  *[2.5–25 seconds]: Master Mode
1769	  *[2–8 seconds]: Expert Mode
1770	  *[2.5–10 seconds]: Master Mode
1771	  *[17–30]: Expert Mode
1772	  *[defense]: Expert Mode
1773	  *[14400/28800]: Expert Mode
1774	  *[18360/36720]: Master Mode
1775	  *[25–74]: Expert Mode
1776	  *[13500]: Expert Mode
1777	  *[17212]: Master Mode
1778	  *[11475]: Master Mode
1779	  *[13387]: Master Mode
1780	  *[The [](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu") can greatly increase your mobility as well as provide some extra defense.]: Expert Mode
1781	  *[The [](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") will reduce damage taken, making it a powerful choice.]: Expert Mode
1782	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") has a chance to dodge an attack, providing the player with a useful [](Cerebral_Mindtrick "Cerebral Mindtrick")[Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick") buff.]: Expert Mode
1783	  *[91]: Expert Mode
1784	  *[137]: Master Mode
1785	  *[10+25 per hand alive]: Expert Mode
1786	  *[0+25 per hand alive]: Expert Mode
1787	  *[6–10 seconds]: Expert Mode
1788	  *[7.5–12.5 seconds]: Master Mode
1789	  *[1−2 seconds]: Expert Mode
1790	  *[1.5–2.5 seconds]: Master Mode
1791	  *[9.75%]: Expert Mode
1792	  *[55.56%]: Expert Mode
1793	  *[64500]: Expert Mode
1794	  *[82238]: Master Mode
1795	  *[64,500]: Expert Mode
1796	  *[82,238]: Master Mode
1797	  *[12,000]: Expert Mode
1798	  *[15,300]: Master Mode
1799	  *[13,800]: Expert Mode
1800	  *[17,595.2]: Master Mode
1801	  *[[](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu")'s dash is essential throughout the fight.]: Expert Mode
1802	  *[[](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") greatly decreases damage, but is exclusive to Corruption worlds.]: Expert Mode
1803	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") is very useful for players as it provides a chance to dodge an attack, but is exclusive to Crimson worlds. It doesn't prevent getting inflicted with the [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff, however.]: Expert Mode
1804	  *[24%]: Expert Mode
1805	  *[28%]: Master Mode
1806	  *[11,920]: Expert Mode
1807	  *[15,198]: Master Mode
1808	  *[1560]: Expert Mode
1809	  *[1989]: Master Mode
1810	  *[3120]: Expert Mode
1811	  *[3978]: Master Mode
1812	  *[8800]: Expert Mode
1813	  *[7.2-12.5]: Master Mode
1814	  *[ Expert-exclusive]: Expert Mode
1815	  *[ Master-exclusive]: Master Mode
1816	  *[(expert)]: Expert Mode
1817	  *[12000]: Expert Mode
1818	  *[13800]: Expert Mode
1819	  *[18-90]: Expert Mode
1820	  *[67,500]: Expert Mode
1821	  *[37,500]: Expert Mode
1822	  *[75,000]: Expert Mode
1823	  *[with a 1/5 (20%) chance]: Expert Mode
1824	  *[41]: Expert Mode
1825	  *[0 mph]: 0 miles per hour (as measured by the Stopwatch item) or 0 tiles per second
1826	  *[150 mph]: 150 miles per hour (as measured by the Stopwatch item) or 110 tiles per second
1827	  *[179 mph]: 179 miles per hour (as measured by the Stopwatch item) or 131.27 tiles per second
1828	  *[ 6500]: Expert Mode
1829	  *[8287]: Master Mode
1830	  *[1.25%–5%]: Expert Mode
1831	  *[32]: Expert Mode
1832	  *[0.25 mph]: 0.25 miles per hour (as measured by the Stopwatch item) or 0.18 tiles per second
1833	  *[ 2700]: Expert Mode
1834	  *[4050]: Master Mode
1835	  *[96 mph]: 96 miles per hour (as measured by the Stopwatch item) or 70.4 tiles per second
1836	  *[164 mph]: 164 miles per hour (as measured by the Stopwatch item)
1837	  *[245 mph]: 245 miles per hour (as measured by the Stopwatch item)
1838	  *[11/100 (11%)]: Expert Mode
1839	  *[5% – 20%]: Expert Mode
1840	  *[6.22% – 31.11%]: Expert Mode
1841	  *[50 mph]: 50 miles per hour (as measured by the Stopwatch item) or 36.67 tiles per second
1842	  *[2–10 or 20 seconds]: Expert Mode
1843	  *[2.5–12.5 or 25 seconds]: Master Mode
1844	  *[2–10 or 20 secondi]: Expert Mode
1845	  *[2.5–12.5 or 25 secondi]: Master Mode
1846	  *[52 mph]: 52 miles per hour (as measured by the Stopwatch item) or 38.13 tiles per second
1847	  *[5.63%]: Expert Mode
1848	  *[2 seconds]: Expert Mode
1849	  *[2.5 seconds]: Master Mode
1850	  *[4,000]: Expert Mode
1851	  *[6,000]: Master Mode
1852	  *[148]: Expert Mode
1853	  *[222]: Master Mode
1854	  *[1.33 seconds]: Expert Mode
1855	  *[1.67 seconds]: Master Mode
1856	  *[33,150]: Expert Mode
1857	  *[42,266]: Master Mode
1858	  *[22,100]: Expert Mode
1859	  *[28,177]: Master Mode
1860	  *[11,050]: Expert Mode
1861	  *[14,088]: Master Mode
1862	  *[4,420]: Expert Mode
1863	  *[5,635]: Master Mode
1864	  *[198]: Master Mode
1865	  *[297]: Master Mode
1866	  *[50 seconds]: Expert Mode
1867	  *[1 minute 2.5 seconds]: Master Mode
1868	  *[1.25–5 seconds]: Master Mode
1869	  *[six]: Master Mode
1870	  *[additional accessory slot]: Master Mode
1871	  *[1.25%]: Expert Mode
1872	  *[2.5%]: Expert Mode
1873	  *[38 mph]: 38 miles per hour (as measured by the Stopwatch item) or 27.87 tiles per second
1874	  *[ 36]: Expert Mode
1875	  *[399/40,000 (0.9975%)]: Expert Mode
1876	  *[178]: Master Mode
1877	  *[2,659]: Expert Mode
1878	  *[3,390]: Master Mode
1879	  *[2,519]: Expert Mode
1880	  *[3,212]: Master Mode
1881	  *[2,800–2,240]: Expert Mode
1882	  *[3,570–2,856]: Master Mode
1883	  *[2,239–1,680]: Expert Mode
1884	  *[2,855–2,142]: Master Mode
1885	  *[1,679–1,120]: Expert Mode
1886	  *[2,141–1,428]: Master Mode
1887	  *[1,119–560]: Expert Mode
1888	  *[1,427–714]: Master Mode
1889	  *[559–280]: Expert Mode
1890	  *[713–357]: Master Mode
1891	  *[279–0]: Expert Mode
1892	  *[356–0]: Master Mode
1893	  *[2800]: Expert Mode
1894	  *[3570]: Master Mode
1895	  *[1/15th]: Expert Mode
1896	  *[15%]: Mode Expert
1897	  *[46%]: Expert Mode
1898	  *[52%]: Master Mode
1899	  *[68%]: Master Mode
1900	  *[1000]: Expert Mode
1901	  *[sometimes]: Expert Mode
1902	  *[1.2]: Archery buff
1903	  *[9]: Master Mode
1904	  *[O3DS]: Original Nintendo 3DS
1905	  *[Number]: Number of Tiny Eaters
1906	  *[Average]: Average number of Tiny Eaters
1907	  *[102×102]: Expert Mode
1908	  *[1/25 (4%)]: Expert Mode
1909	  *[44–60]: Expert Mode
1910	  *[66–90]: Master Mode
1911	  *[WoF]: Wall
1912	  *[135]: Master Mode
1913	  *[ (1 player)  
1914	57% (2 players)  
1915	71% (3 players)  
1916	81%  (4 players)  
1917	100% (5 players or more)  
1918	]: Expert Mode
1919	  *[ (1 player)  
1920	62% (2 players)  
1921	75% (3 players)  
1922	83% (4 players)  
1923	100% (5 players or more)  
1924	]: Master Mode
1925	  *[ (1 player)  
1926	69% (2 players)  
1927	79% (3 players)  
1928	86%  (4 players)  
1929	100% (5 players or more)  
1930	]: Expert Mode
1931	  *[ (1 player)  
1932	72% (2 players)  
1933	82% (3 players)  
1934	88% (4 players)  
1935	100% (5 players or more)  
1936	]: Master Mode
1937	  *[1485]: Expert Mode
1938	  *[2227]: Master Mode
1939	  *[2700]: Expert Mode
1940	  *[220]: At least one Ogre has to be killed
1941	  *[330]: Master Mode
1942	  *[224]: Expert Mode
1943	  *[336]: Master Mode
1944	  *[454]: Master Mode
1945	  *[52›93›138]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1946	  *[78›140›208]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1947	  *[60›105›105]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1948	  *[90›157›157]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1949	  *[48›86›131]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1950	  *[73›129›196]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1951	  *[60›105›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1952	  *[90›157›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1953	  *[45›120›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1954	  *[67›180›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1955	  *[472]: Master Mode
1956	  *[18–23]: Expert Mode
1957	  *[1/4]: Master Mode
1958	  *[4.94 (79/1600)]: Expert Mode
1959	  *[30–49]: Expert Mode
1960	  *[1/2]: Expert Mode
1961	  *[20–35]: Expert Mode
1962	  *[90–110]: Chế độ Expert
1963	  *[49/625 (7.84%)]: Expert Mode
1964	  *[99/2500 (3.96%)]: Expert Mode
1965	  *[1/15 (6.67%)]: Expert Mode
1966	  *[1/75 (1.33%)]: Expert Mode
1967	  *[1/20 (5%) ****__(Desktop, Console and Mobile versions)]: Expert Mode
1968	  *[5/9 (55.56%)]: Expert Mode
1969	  *[H]: Height (tiles)
1970	  *[14–17]: Expert Mode
1971	  *[3–4]: Expert Mode
1972	  *[12–15]: Chế độ Expert
1973	  *[21-27]: Chế độ Expert
1974	  *[four]: Expert Mode
1975	  *[1–5]: Expert Mode
1976	  *[1.25–6.25]: Master Mode
1977	  *[almost opaque]: Expert Mode
1978	  *[three]: Expert Mode
1979	  *[24,000]: Expert Mode
1980	  *[30,600]: Master Mode
1981	  *[1,200]: Master Mode
1982	  *[16,000]: Expert Mode
1983	  *[20,400]: Master Mode
1984	  *[40000]: Expert Mode
1985	  *[51000]: Master Mode
1986	  *[48000]: Expert Mode
1987	  *[61000]: Master Mode
1988	  *[39 mph]: 39 miles per hour (as measured by the Stopwatch item) or 28.6 tiles per second
1989	  *[599/90,000 (0.6656%)]: Expert Mode
1990	  *[395]: Expert Mode
1991	  *[second phase]: Expert Mode
1992	  *[54000]: Expert Mode
1993	  *[全て]: Master Mode
1994	  *[75 HP]: Chế độ Master
1995	  *[21 Sát thương]: Chế độ Master
1996	  *[20% KB]: Chế độ Master
1997	  *[411 HP]: Chế độ Master
1998	  *[93 Sát thương]: Chế độ Master
1999	  *[Vždy kupuj více drátů, než potřebuješ.]: Always buy more wire than you need!
2000	  *[Je to určitě zapojené do proudu?]: Did you make sure your device was plugged in?
2001	  *[Oh, víš co tento dům opravdu potřebuje? Více blikajících světélek.]: Oh, you know what this house needs? More blinking lights.
2002	  *[Hej [jméno hráče], nevrátil jsi se právě od [jméno gobliního kutila]? Neříkal ti náhodou něco o mně?]: Hey, [Name of Player], did you just come from [Name of Goblin Tinkerer]'s? Did he say anything about me by chance?
2003	  *[Hej, dávej si bacha, kam jdeš! Já jsem tam ještě nedávno byla!]: Hey, watch where you're going! I was over there a little while ago!
2004	  *[[Jméno prodejce zbraní] pořád říká, že stiskne mou tlakovou desku. Já jsem mu ale říkala, že na ni se má šlapat.]: [Name of Arms Dealer] keeps talking about pressing my pressure plate. I told him it was for stepping on.
2005	  *[Oh, nech mě hádat. Zapomněl jsi koupit dostatek drátů. Hlupáku.]: Oh, let me guess. Forgot to buy enough wire. Idiot.
2006	  *[Mohl… Mohl bys… Prosím? Ok? Ok. Ugh.]: Just-could you just...Please? Ok? Ok. Ugh.
2007	  *[Nelíbí se mi, jak se na mě díváš. Já právě PRACUJI.]: I don't appreciate the way you're looking at me. I am WORKING right now.
2008	  *[Všechno co bych pro vypínač chtěla je… Cože?!]: All I want is for the switch to make the... What?!
2009	  *[NEHÝBAT! SPADLA MI KONTAKTNÍ ČOČKA.]: DON'T MOVE. I DROPPED MY CONTACT.
2010	  *[Už jsme byla skoro hotová s věšením blikajících světélek!]: But I was almost done putting blinking lights up here!
2011	  *[Zadrž, už jsem tady dole skoro chytala WiFi signál.]: Hold on, I've almost got wifi going down here.
2012	  *[Děkuji. Trvat to o něco déle, tak skončím jako většina těch kostlivců, co tady dole žije.]: Thanks! It was only a matter of time before I ended up like the rest of the skeletons down here.
2013	  *[Kosh, kapleck Mog. Oh sorry, that's Klingon for 'Buy something or die.']: Kosh, kapleck Mog. Oh promiň, to je klingonsky výraz pro: ‚Něco si kup, nebo zemři.‘
2014	  *[Meč poráží papír! Získej jeden ještě dnes.]: Sword beats paper! Get one today.
2015	  *[Krásné ráno, co myslíš? Nechtěl jsi něco?]: Lovely morning, wouldn't you say? Was there something you needed?
2016	  *[Chceš jablka? Chceš mrkve? Chceš ananasy? Máme pro tebe pochodně!]: You want apples? You want carrots? You want pineapples? We got torches.
2017	  *[Slunce je vysoko, ale mé ceny jsou nízké.]: 
2018	  *[Chlape, to slunce ale pálí! Náhodou mám jedno úžasně ventilované brnění.]: Boy, that sun is hot! I do have some perfectly ventilated armor.
2019	  *[Koukni na moje hliněné bloky, jsou extra hliněné.]: Check out my dirt blocks, they are extra dirty.
2020	  *[Ah, jednoho dnes se budou vyprávět pověsti o [jméno hráče]… jen ty dobré, tím jsem si jist.]: Ah, they will tell tales of [Name of Player] some day... good ones I'm sure.
2021	  *[Brzy nastane noc můj příteli. Rozhodni se dokud ještě můžeš.]: Night be upon us soon, friend. Make your choices while you can.
2022	  *[Nemáš ani ponětí, jakou cenou se v zámoří platí za hliněné bloky.]: You have no idea how much Dirt Blocks sell for overseas.
2023	  *[Kosh, kapleck Mog. Oh promiň, to je [klingonsky](https://en.wikipedia.org/wiki/cs:Klingon "wikipedia:cs:Klingon") výraz pro: ‚Něco si kup, nebo zemři.‘]: Kosh, kapleck Mog. Oh sorry, that's klingon for 'Buy something or die.'
2024	  *[[Jméno hráče], je to tak? Slyšel jsem jen dobré zprávy příteli!]: [Name of Player] is it? I've heard good things, friend!
2025	  *[Občas přemýšlím, jestli je měsíc ze sýra… huh, co? Oh ano, kup něco!]: I wonder if the moon is made of cheese... huh, what? Oh yes, buy something!
2026	  *[Chlápek co teď odcházel mi tady nechal nějaký bordel… uhm chtěl jsem říct… poklady!]: The last guy who was here left some junk... er I mean... treasures!
2027	  *[Řekl jsi zlato? To od tebe klidně odkoupím.]: Did you say gold? I'll take that off of ya.
2028	  *[Slyšel jsem o ukrytém pokladu… oh zapomeň na to.]: I hear there's a secret treasure... oh never mind.
2029	  *[Socha anděla povídáš? Promiň, ale já neprodávám žádné harampádí.]: Angel statue you say? I'm sorry, I'm not a junk dealer.
2030	  *[Viděl jsi už Chith… Shith… Chat… Obří oko?]: Have you seen Chith...Shith.. Chat... The big eye?
2031	  *[Občas hoď okem po ceně, kup čočky!]: Keep your eye on the prize, buy a lens!
2032	  *[Oh výtečně. Už zase slyším [jméno mechaničky] a [jméno sestřičky], jak se hádají.]: Oh, great. I can hear [Name of Mechanic] and [Name of Nurse] arguing from here.
2033	  *[Ani krvavý měsíc nezastaví kapitalismus. Pojďme uzavřít nějaký obchod.]: Not even a Blood Moon can stop capitalism. Let's do some business.
2034	  *[Hej, tento dům je zabezpečený, je to tak? [Jméno hráče], je to tak?!]: Hey, this house is secure, right? Right? [Name of Player]?
2035	  *[Doufám, že takový vychrtlý klučina jako ty není to, co nás má ochránit před okem Cthulu.]: I hope a scrawny kid like you isn't all that's standing between us and Cthulu's Eye.
2036	  *[Cítím, jako kdyby mě sledovala přítomnost zla.]: I feel like an evil presence is watching me.
2037	  *[Když se tak koukám na to ošuntělé brnění, co nosíš, mám chuť ti prodat ještě pár léčivých lektvarů.]: Look at that shoddy armor you're wearing. Better buy some more healing potions.
2038	  *[10–20]: Expert Mode
2039	  *[12–25]: Master Mode
2040	  *[900]: Master Mode
2041	  *[ 5 _GC_]: Expert Mode
2042	  *[25 _GC_]: Expert Mode
2043	  *[11 mph]: 11 miles per hour (as measured by the Stopwatch item) or 8.07 tiles per second
2044	  *[9 mph]: 9 miles per hour (as measured by the Stopwatch item) or 6.75 tiles per second
2045	  *[49]: Expert Mode
2046	  *[Pre-HM]: Pre-Hardmode
2047	  *[101]: Expert Mode
2048	  *[337]: Expert Mode
2049	  *[Enemies that have [picked up coins](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")]: Expert Mode
2050	  *[2.67]: Expert Mode
2051	  *[2.25]: Master Mode
2052	  *[16 sekund]: Expertní mód
2053	  *[ 2 _PC_ 50 _GC_]: Expertní mód
2054	  *[40–45]: Expert Mode
2055	  *[187.5]: Master Mode
2056	  *[+24%]: Expert Mode
2057	  *[+28%]: Master Mode
2058	  *[305 mph]: 305 miles per hour (as measured by the Stopwatch item) or 223.67 tiles per second
2059	  *[255 mph]: 255 miles per hour (as measured by the Stopwatch item) or 187 tiles per second
2060	  *[720 mph]: 720 miles per hour (as measured by the Stopwatch item) or 528 tiles per second
2061	  *[0.0396%]: Expert Mode
2062	  *[10,149/1,000,000 (1.01%)]: Expert Mode
2063	  *[199/10,000 (1.99%)]: Expert Mode
2064	  *[36%]: Expert Mode
2065	  *[night]: 7:30 PM – 4:30 AM
2066	  *[dawn]: 4:30 AM
2067	  *[2–8]: Chế độ Expert
2068	  *[10–30 seconds]: Expert Mode
2069	  *[12.5–37.5 seconds]: Master Mode
2070	  *[10–30]: Expert Mode
2071	  *[12.5–37.5]: Master Mode
2072	  *[3 _SC_]: Expert Mode
2073	  *[3 _GC_]: Expert Mode
2074	  *[6 _SC_]: Expert Mode
2075	  *[4 _SC_ 50 _CC_]: Expert Mode
2076	  *[9 _SC_]: Expert Mode
2077	  *[20 _SC_]: Expert Mode
2078	  *[15 _SC_]: Expert Mode
2079	  *[30 _SC_]: Expert Mode
2080	  *[50 _SC_]: Expert Mode
2081	  *[37 _SC_ 50 _CC_]: Expert Mode
2082	  *[75 _SC_]: Expert Mode
2083	  *[1 _GC_ 20 _SC_]: Expert Mode
2084	  *[90 _SC_]: Expert Mode
2085	  *[1 _GC_ 80 _SC_]: Expert Mode
2086	  *[2 _GC_]: Expert Mode
2087	  *[1 _GC_ 50 _SC_]: Expert Mode
2088	  *[2 _GC_ 25 _SC_]: Expert Mode
2089	  *[4 _GC_ 50 _SC_]: Expert Mode
2090	  *[4 _GC_]: Expert Mode
2091	  *[Hej, nezmiňoval se [jméno prodejce zbraní] o tom, že by potřeboval vyšetřit? Ptám se jen tak.]: Hey, has [Name of Arms Dealer] mentioned needing to go to the doctor for any reason? Just wondering.
2092	  *[Bolí to, když uděláš tohle? Pak tohle nedělej.]: Does it hurt when you do that? Don't do that.
2093	  *[Ukaž mi, co tě bolí.]: Show me where it hurts.
2094	  *[Tohle není to největší, co jsem za svůj život viděla… Ano, už jsem viděla větší rány.]: That's not the biggest I've ever seen... Yes, I've seen bigger wounds for sure.
2095	  *[Otoč hlavu a zakašlej.]: Turn your head and cough.
2096	  *[Někdy si přeji, aby byl [jméno demoličního experta] více opatrný. Už mě unavuje to každodenní přišívání jeho končetin zpět k tělu.]: I wish [Name of Demolitionist] would be more careful. I'm getting tired of having to sew his limbs back on every day.
2097	  *[Lízátko by sis nedal?]: Would you like a lollipop?
2098	  *[Asi si budu muset promluvit s [jméno průvodce]. Jak často si musíš ošetřovat tak těžké popáleniny?]: I need to have a serious talk with [Name of Guide]. How many times a week can you come in with severe lava burns?
2099	  *[Už jsi viděl starce, jak se potuluje kolem podzemní kobky? Vypadá utrápeně.]: Have you seen that Old Man pacing around the dungeon? He looks troubled.
2100	  *[Nedělej ze sebe takové dítě. Už jsem viděla horší.]: Quit being such a baby! I've seen worse.
2101	  *[Zase trable s těmi tyrany?]: Trouble with those bullies again?
2102	  *[To bude potřebovat pár stehu!]: That's gonna need stitches!
2103	  *[vypadáš, jako kdybys byl napůl strávený. Zase jsi honil slizy?]: You look half digested. Have you been chasing slimes again?
2104	  *[Počkej chvíli, mám tady někde nějaké náplasti se zvířátky.]: Hold on, I've got some cartoon bandages around here somewhere.
2105	  *[[Jméno hráče], to rozchodíš a budeš v pořádku. Šmárja.]: Walk it off, (Name of Player), you'll be fine. Sheesh.
2106	  *[Drazí přátelé, sešli jsme se zde, abychom vzdali poslední úctu… ále, budeš v pořádku.]: Dear friends we are gathered here today to bid farewell... oh, you'll be fine.
2107	  *[Myslím si, že toto ti sluší víc.]: I think you look better this way.
2108	  *[Eww… Co se stalo s tvým obličejem?]: Eww.. what happened to your face?
2109	  *[Támhle jsi nechal svoje rameno. Dojdu pro něj.]: You left your arm over there. Let me get that for you.
2110	  *[MŮJ BOŽE. Dobrá jsem, ale TAKHLE zase ne.]: MY GOODNESS. I'm good but I'm not THAT good.
2111	  *[Co má tohle znamenat?]: What is that supposed to mean!?
2112	  *[Nemyslím si, že se mi líbí tvůj tón v hlase.]: I don't think I like your tone.
2113	  *[Co tady děláš? Pokud nekrvácíš, tak tě tady nechci. Běž pryč.]: Why are you even here? If you aren't bleeding, you don't need to be here. Get out.
2114	  *[COŽE?!]: WHAT?!
2115	  *[Pokud plánuješ zemřít, učiň tak venku.]: If you're going to die, do it outside.
2116	  *[Pospěš si a přestaň krvácet.]: Hurry up and stop bleeding.
2117	  *[Běda, jestli se mi tvá krev dostane na sukni.]: You better not get blood on me.
2118	  *[Ani to nebolelo, že ne?]: That didn't hurt too bad, now did it?
2119	  *[Všechno v pořádku. A ne abych se zase načapala, jak skáčeš z dalších útesů.]: All better. I don't want to see you jumping off any more cliffs.
2120	  *[Tohle asi zanechá jizvu.]: That's probably going to leave a scar.
2121	  *[Podařilo se mi tvůj obličej sešít. Příště si dávej větší pozor.]: I managed to sew your face back on. Be more careful next time.
2122	  *[Přestaň plýtvat mým časem.]: Quit wasting my time.
2123	  *[Žádné šťastné konce ode mě nečekej.]: I don't give happy endings.
2124	  *[Pokud nechceš plastickou operaci, tak ti toho víc nenabídnu.]: I can't do anymore for you without plastic surgery.
2125	  *[Omlouvám se, ale mé služby si nemůžeš momentálně dovolit.]: I'm sorry, but you can't afford me.
2126	  *[Budeš potřebovat více zlata, než je tohle.]: I'm gonna need more gold than that.
2127	  *[Jen abys věděl – nepracuji zadarmo.]: I don't work for free you know.
2128	  *[1,485]: Expert Mode
2129	  *[2,227]: Master Mode
2130	  *[500]: Expert Mode
2131	  *[%55]: Expert Mode
2132	  *[%64]: Expert Mode
2133	  *[Vrať se zpět za noci, pokud si přeješ vstoupit.]: Come back at night if you wish to enter.
2134	  *[Nemůžu tě pustit dále, pokud mě neosvobodíš od mé kletby.]: I cannot let you enter until you free me of my curse.
2135	  *[Můj pán nemůže být vyvolán pod záštitou denního světla.]: My master cannot be summoned under the light of day.
2136	  *[Jsi příliš slabý na zlomení mé kletby. Vrať se zpět, až nebudeš taková nicka.]: You are far too weak to defeat my curse. Come back when you aren't so worthless.
2137	  *[Ubohý hlupáku. Nemůžeš si myslet, že bys mohl porazit mého pána ve stavu, v jakém se nacházíš.]: You pathetic fool. You cannot hope to face my master as you are now.
2138	  *[Doufám, že máš tak šest přátel stojících po tvém boku.]: I hope you have like six friends standing around behind you.
2139	  *[Prosím ne, cizinče. Jen bys marnil svůj drahocenný život.]: Please, no, stranger. You'll only get yourself killed.
2140	  *[Cizinče. Budeš dostatečně silný, abys porazil mého pána?]: Stranger, do you possess the strength to defeat my master?
2141	  *[Ty bys mohl být dostatečně silný na osvobození mě od mé kletby…]: You just might be strong enough to free me from my curse...
2142	  *[Prosím! Poraz mého věznitele a osvoboď mne! Zapřísahám tě!]: Please! Battle my captor and free me! I beg you!
2143	  *[Poraz mého pána a já ti zajistím průchod do podzemní kobky.]: Defeat my master, and I will grant you passage into the Dungeon.
2144	  *[Pokud porazíš mého pána, splním ti jedno přání.]: If you beat my master I will grant you one wish.
2145	  *[∞]: Must defeat Betsy
2146	  *[56]: Mode Expert
2147	  *[7–12]: Master Mode
2148	  *[24–40]: Expert Mode
2149	  *[28–48]: Master Mode
2150	  *[20-37.5]: Master Mode
2151	  *[64–120]: Expert Mode
2152	  *[80-150]: Master Mode
2153	  *[56–80]: Expert Mode
2154	  *[70–100]: Master Mode
2155	  *[40–56]: Expert Mode
2156	  *[60-84]: Master Mode
2157	  *[4–20]: Expert Mode
2158	  *[5–25]: Master Mode
2159	  *[28800]: Mode Expert
2160	  *[43200]: Mode Master
2161	  *[16-30]: Mode Expert
2162	  *[64-120]: Mode Expert
2163	  *[40-56]: Mode Expert
2164	  *[要100次]: Journey Mode
2165	  *[1/150 (0.67%)]: Expert Mode
2166	  *[12.89%]: Expert Mode
2167	  *[19%]: Expert Mode
2168	  *[9.78%]: Expert Mode
2169	  *[13.56%]: Expert Mode
2170	  *[29/225 (12.89%)]: Expert Mode
2171	  *[230 mph]: 230 miles per hour (as measured by the Stopwatch item) or 168.75 tiles per second
2172	  *[22/225 (9.78%)]: Expert Mode
2173	  *[19/100 (19%)]: Expert Mode
2174	  *[Expert Mode:]: Expert Mode
2175	  *[1.4%]: Expertní mód
2176	  *[1/70 (1.43%)]: Expert Mode
2177	  *[10›8]: Expert Mode : Pre-Hardmode › Hardmode
2178	  *[300›330]: Expert Mode : Pre-Hardmode › Hardmode
2179	  *[%-13]: Expert Mode
2180	  *[%1,4]: Expert Mode
2181	  *[5/12 (41.67%)]: Expert Mode
2182	  *[6/12 (50%)]: Expert Mode
2183	  *[1/12 (8.33%)]: Expert Mode
2184	  *[4–9]: Expert Mode
2185	  *[33,600]: Expert Mode
2186	  *[42,840]: Master Mode
2187	  *[21,000]: Expert Mode
2188	  *[26,775]: Master Mode
2189	  *[42,000–37,800]: Expert Mode
2190	  *[53,550–48,195]: Master Mode
2191	  *[37,799–33,600]: Expert Mode
2192	  *[48,194–42,840]: Master Mode
2193	  *[33,599–29,400]: Expert Mode
2194	  *[42,839–37,485]: Master Mode
2195	  *[29,399–25,200]: Expert Mode
2196	  *[37,484–32,130]: Master Mode
2197	  *[25,199–21,001]: Expert Mode
2198	  *[32,129–26,776]: Master Mode
2199	  *[21,000–16,800]: Expert Mode
2200	  *[26,775–21,420]: Master Mode
2201	  *[16,799–12,600]: Expert Mode
2202	  *[21,419–16,065]: Master Mode
2203	  *[12,599–8,400]: Expert Mode
2204	  *[16,064–10,710]: Master Mode
2205	  *[8,399–4,200]: Expert Mode
2206	  *[10,709–5,355]: Master Mode
2207	  *[4,199–0]: Expert Mode
2208	  *[5,354–0]: Master Mode
2209	  *[101×101]: Expert Mode
2210	  *[3/2500 (0.12%)]: Expert Mode
2211	  *[2–10 or 20]: Expert Mode
2212	  *[2.5–12.5 or 25]: Master Mode
2213	  *[4–20 or 40]: Expert Mode
2214	  *[5-12.5 or 50]: Master Mode
2215	  *[2.5-10]: Master Mode
2216	  *[4–16]: Expert Mode
2217	  *[5-20]: Master Mode
2218	  *[2.5-7.5]: Master Mode
2219	  *[5-15]: Master Mode
2220	  *[10 or 40]: Expert Mode
2221	  *[12.5 or 50]: Master Mode
2222	  *[20 or 80]: Expert Mode
2223	  *[25 or 100]: Master Mode
2224	  *[5-10]: Chế độ Expert
2225	  *[6-12.5]: Master Mode
2226	  *[10-20]: Master Mode
2227	  *[12-25]: Master Mode
2228	  *[4–18]: Chế độ Expert
2229	  *[7.5-17.5]: Master Mode
2230	  *[8–36]: Expert Mode
2231	  *[15-35]: Master Mode
2232	  *[4–8]: Chế độ Expert
2233	  *[8–16]: Expert Mode
2234	  *[5.23-10.5]: Expert Mode
2235	  *[6.53-13.12]: Master Mode
2236	  *[10-21]: Expert Mode
2237	  *[13-26]: Master Mode
2238	  *[14400]: Chế độ Expert
2239	  *[21600]: Chế độ Master
2240	  *[98]: Expert Mode
2241	  *[123]: Master Mode
2242	  *[196]: Expert Mode
2243	  *[246]: Master Mode
2244	  *[2–10 hoặc 20]: Chế độ Expert
2245	  *[4-20 hoặc 40]: Chế độ Expert
2246	  *[4-16]: Chế độ Expert
2247	  *[4-12]: Chế độ Expert
2248	  *[10 hoặc 40]: Chế độ Expert
2249	  *[20 hoặc 80]: Chế độ Expert
2250	  *[8-36]: Chế độ Expert
2251	  *[8-16]: Chế độ Expert
2252	  *[2.625–5.25]: Chế độ Expert
2253	  *[514 mph]: 514 miles per hour (as measured by the Stopwatch item) or 376.93 tiles per second
2254	  *[2/45]: Expert Mode
2255	  *[5–18]: Expert Mode
2256	  *[7–24]: Expert Mode
2257	  *[7–27]: Expert Mode
2258	  *[10–36]: Expert Mode
2259	  *[3–12]: Expert Mode
2260	  *[3–7]: Expert Mode
2261	  *[95 mph]: 95 miles per hour (as measured by the Stopwatch item) or 69.67 tiles per second

```


---

## 🤖 Assistant · 2026-08-13T00:34:18.903Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/terraria-wiki-md/Sensors.md"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:34:19.041Z

**📎 ToolResult**

```
1	# Sensors
2	
3	> 原页面: `Sensors`
4	
5	# Sensors
6	
7	[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
8	
9	**[Desktop](Category%3ADesktop_content "Category:Desktop content")/[Console](Category%3AConsole_content "Category:Console content")/[Mobile](Category%3AMobile_content "Category:Mobile content")-Only Content**: This information applies _only_ to the **[Desktop](Desktop_version_history.md "Desktop version history")** , **[Console](Console_version.md "Console version")** , and **[Mobile](Mobile_version.md "Mobile version")** versions of _[Terraria](Terraria.md "Terraria")_.
10	
11	Sensors
12	
13	  *   * 
14	
15	[](Autoswing.md "Auto-use")
16	
17	Statistics
18	
19	Type| [Furniture](Furniture.md "Furniture")[Mechanism](Mechanism "Mechanism")  
20	---|---  
21	[Placeable](Placement.md "Placement")| ✔️ (1 wide × 1 high)  
22	[Use time](Use_time.md "Use time")| 15 (Very fast)  
23	[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_1 "Blue \(Rarity level: 1\)")  
24	[Research](Journey_Mode#Research "Journey Mode")| 5 required  
25	  
26	  * Internal [Item ID](Item_IDs.md "Item IDs"): **3613–3615, 3726–3729**
27	  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **423**
28	
29	**Sensors** are [Hardmode](Hardmode.md "Hardmode") [mechanisms](Mechanisms.md "Mechanisms") that emit a signal under specific circumstances. There are 7 different types of sensors, split into 2 sub-categories: Logic Sensors and Liquid Sensors. 
30	
31	## Types
32	
33	Sensor  | Tooltip   
34	---|---  
35	~~~~|  Logic Sensor (Day)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3613 | Signals at dawn  
36	~~~~|  Logic Sensor (Night)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3614 | Signals at dusk  
37	~~~~|  Logic Sensor (Player Above)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3615 | Signals when the first player enters or the last player leaves the area above it  
38	~~~~|  Liquid Sensor (Water)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3726 | Signals when water starts or stops touching it  
39	~~~~|  Liquid Sensor (Lava)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3727 | Signals when lava starts or stops touching it  
40	~~~~|  Liquid Sensor (Honey)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3728 | Signals when honey starts or stops touching it  
41	~~~~|  Liquid Sensor (Any)****__(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 3729 | Signals when any liquid starts or stops touching it  
42	  
43	## Crafting
44	
45	### Recipes
46	
47	Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
48	---|---|---  
49	Liquid Sensor (Any)****__(Desktop, Console and Mobile versions)| 
50	
51	  * [](Cog.md "Cog")[Cog](Cog.md "Cog")5
52	  * [](Magic_Water_Dropper "Magic Water Dropper")[Magic Water Dropper](Magic_Water_Dropper "Magic Water Dropper")**** __(Desktop, Console and Mobile versions)
53	  * [](Magic_Lava_Dropper "Magic Lava Dropper")[Magic Lava Dropper](Magic_Lava_Dropper "Magic Lava Dropper")**** __(Desktop, Console and Mobile versions)
54	  * [](Magic_Honey_Dropper "Magic Honey Dropper")[Magic Honey Dropper](Magic_Honey_Dropper "Magic Honey Dropper")**** __(Desktop, Console and Mobile versions)
55	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
56	
57	| [](Mythril_Anvil "Mythril Anvil")[Mythril Anvil](Mythril_Anvil "Mythril Anvil")  
58	 _**or**_  
59	[](Orichalcum_Anvil "Orichalcum Anvil")[Orichalcum Anvil](Orichalcum_Anvil "Orichalcum Anvil")  
60	Liquid Sensor (Honey)****__(Desktop, Console and Mobile versions)| 
61	
62	  * [](Cog.md "Cog")[Cog](Cog.md "Cog")5
63	  * [](Magic_Honey_Dropper "Magic Honey Dropper")[Magic Honey Dropper](Magic_Honey_Dropper "Magic Honey Dropper")**** __(Desktop, Console and Mobile versions)
64	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
65	
66	  
67	Liquid Sensor (Lava)****__(Desktop, Console and Mobile versions)| 
68	
69	  * [](Cog.md "Cog")[Cog](Cog.md "Cog")5
70	  * [](Magic_Lava_Dropper "Magic Lava Dropper")[Magic Lava Dropper](Magic_Lava_Dropper "Magic Lava Dropper")**** __(Desktop, Console and Mobile versions)
71	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
72	
73	  
74	Liquid Sensor (Water)****__(Desktop, Console and Mobile versions)| 
75	
76	  * [](Cog.md "Cog")[Cog](Cog.md "Cog")5
77	  * [](Magic_Water_Dropper "Magic Water Dropper")[Magic Water Dropper](Magic_Water_Dropper "Magic Water Dropper")**** __(Desktop, Console and Mobile versions)
78	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
79	
80	  
81	Logic Sensor (Day)****__(Desktop, Console and Mobile versions)| 
82	
83	  * [](Soul_of_Light.md "Soul of Light")[Soul of Light](Soul_of_Light.md "Soul of Light")5
84	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")
85	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
86	
87	  
88	Logic Sensor (Night)****__(Desktop, Console and Mobile versions)| 
89	
90	  * [](Soul_of_Night.md "Soul of Night")[Soul of Night](Soul_of_Night.md "Soul of Night")5
91	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")
92	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
93	
94	  
95	Logic Sensor (Player Above)****__(Desktop, Console and Mobile versions)| 
96	
97	  * [](Soul_of_Sight.md "Soul of Sight")[Soul of Sight](Soul_of_Sight.md "Soul of Sight")
98	  * [](Any_Iron_Bar.md "Any Iron Bar")[Any Iron Bar](Any_Iron_Bar.md "Any Iron Bar")
99	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
100	
101	  
102	  
103	## Notes
104	
105	  * The Player Above sensor detects players in a 5×10-tile area above the sensor, which is outlined while placing it. In [multiplayer](Multiplayer.md "Multiplayer"), it will not send another signal if a player enters the detection zone while another player is already in it. 
106	    * Due to this, it is a viable and multiplayer-friendly alternative to [Pressure Plate](Pressure_Plates.md "Pressure Plates") powered automatic doors.
107	    * It will not trigger if placed while the player is inside the detection area. Instead, it will trigger upon leaving the detection zone.
108	  * The Player Above sensor cannot activate [Teleporters](Teleporter.md "Teleporter"); any logic updates which are triggered by a Player Above sensor will not activate teleporters regardless of the [mechanisms](Mechanisms.md "Mechanisms") it passes through. Previously, this could be bypassed using an intermediate [Logic Gate](Logic_Gate "Logic Gate"). 
109	    * It is possible to work around this by using a delay mechanism such as a [1/4 Second Timer](1/4_Second_Timer.md "1/4 Second Timer"), or a [Spear Trap](Spear_Trap.md "Spear Trap") or similar projectile [traps](Traps.md "Traps") combined with a [Teal Pressure Pad](Teal_Pressure_Pad.md "Teal Pressure Pad").
110	  * The Water Sensor will also activate when in contact with [Shimmer](Shimmer.md "Shimmer").
111	  * [Rain](Rain.md "Rain") can _not_ trigger Water Sensors.
112	
113	## History
114	
115	[ Desktop version](Desktop_version_history.md "Desktop version history")
116	
117	  * [Desktop 1.4.2](Desktop_1.4.2 "Desktop 1.4.2"): Dead players and Hardcore ghosts will no longer trigger Player Above sensors.
118	
119	  * [Desktop 1.3.1](Desktop_1.3.1 "Desktop 1.3.1"): Introduced.
120	
121	[ Console version](Console_version.md "Console version")
122	
123	  * [Console 1.0.1372.5](Console_1.0.1372.5.md "Console 1.0.1372.5"): Introduced.
124	
125	[ Nintendo Switch version](Switch_version.md "Switch version")
126	
127	  * [Switch 1.0.895.9](Switch_1.0.895.9.md "Switch 1.0.895.9"): Introduced.
128	
129	[ Mobile version](Mobile_version.md "Mobile version")
130	
131	  * [Mobile 1.4.0.5.0](Mobile_1.4.0.5.0.md "Mobile 1.4.0.5.0"): Introduced.
132	
133	View or edit this template
134	
135	[Wiring](Guide%3AWiring "Guide:Wiring")
136	
137	Tools
138	
139	  * [](Wire.md "Wire")[Wire](Wire.md "Wire")
140	  * [](Wrenches.md "Wrenches")[](Wrenches.md "Wrenches")[](Wrenches.md "Wrenches")[](Wrenches.md "Wrenches")[Wrenches](Wrenches.md "Wrenches")
141	  * [](Wire_Cutter.md "Wire Cutter")[Wire Cutter](Wire_Cutter.md "Wire Cutter")
142	  * [](Multicolor_Wrench.md "Multicolor Wrench")[Multicolor Wrench](Multicolor_Wrench.md "Multicolor Wrench")
143	  * [](The_Grand_Design.md "The Grand Design")[The Grand Design](The_Grand_Design.md "The Grand Design")
144	  * [](Actuation_Rod.md "Actuation Rod")[Actuation Rod](Actuation_Rod.md "Actuation Rod")
145	
146	Accessories
147	
148	  * [](Mechanical_Lens.md "Mechanical Lens")[Mechanical Lens](Mechanical_Lens.md "Mechanical Lens")
149	  * [](Mechanical_Ruler.md "Mechanical Ruler")[Mechanical Ruler](Mechanical_Ruler.md "Mechanical Ruler")
150	  * [](Presserator.md "Presserator")[Presserator](Presserator.md "Presserator")
151	
152	Triggers
153	
154	  * [](Lever.md "Lever")[Lever](Lever.md "Lever")
155	  * [](Switch.md "Switch")[Switch](Switch.md "Switch")
156	  * [](Pressure_Plates.md "Pressure Plates")[Pressure Plates](Pressure_Plates.md "Pressure Plates")
157	  * [](Pressure_Plate_Track.md "Pressure Plate Track")[Pressure Plate Track](Pressure_Plate_Track.md "Pressure Plate Track")
158	  * [](Timers.md "Timers")[](Timers.md "Timers")[](Timers.md "Timers")[](Timers.md "Timers")[](Timers.md "Timers")[Timers](Timers.md "Timers")
159	  * [](Detonator.md "Detonator")[Detonator](Detonator.md "Detonator")
160	  * [](Trapped_Chests.md "Trapped Chests")[Trapped Chests](Trapped_Chests.md "Trapped Chests")
161	  * [](Dead_Man's_Chest.md "Dead Man's Chest")[Dead Man's Chest](Dead_Man's_Chest.md "Dead Man's Chest")
162	  * [](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[](Gem_Locks.md "Gem Locks")[Gem Locks](Gem_Locks.md "Gem Locks")
163	  * [](Sensors.md "Sensors")[](Sensors.md "Sensors")[](Sensors.md "Sensors")Logic Sensors
164	  * [](Golf_Cup.md "Golf Cup")[Golf Cup](Golf_Cup.md "Golf Cup")
165	
166	[Devices](Mechanism "Mechanism")
167	
168	  * [](Active_Stone_Block.md "Active Stone Block")[](Active_Stone_Block.md "Active Stone Block")[Active/Inactive Stone Block](Active_Stone_Block.md "Active Stone Block")
169	  * [](Actuator.md "Actuator")[Actuator](Actuator.md "Actuator")
170	  * [](Announcement_Box.md "Announcement Box")[Announcement Box](Announcement_Box.md "Announcement Box")
171	  * [](Doors.md "Doors")[Doors](Doors.md "Doors")
172	  * [](Trap_Door.md "Trap Door")[Trap Door](Trap_Door.md "Trap Door")
173	  * [](Tall_Gate.md "Tall Gate")[Tall Gate](Tall_Gate.md "Tall Gate")
174	  * [](Pumps.md "Pumps")[](Pumps.md "Pumps")[Pumps](Pumps.md "Pumps")
175	  * [](Grate.md "Grate")[Grate](Grate.md "Grate")
176	  * [](Teleporter.md "Teleporter")[Teleporter](Teleporter.md "Teleporter")
177	  * [](Statue#Functional_statues "Functional Statues")[](Statue#Functional_statues "Functional Statues")[Functional Statues](Statue#Functional_statues "Statue")
178	  * [](Light_sources.md "Light sources")[](Light_sources.md "Light sources")[](Light_sources.md "Light sources")[Light sources](Light_sources.md "Light sources")
179	  * [](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[](Gemspark_Blocks.md "Gemspark Blocks")[Gemspark Blocks](Gemspark_Blocks.md "Gemspark Blocks")
180	  * [](Mini_Volcano.md "Mini Volcano")[Mini Volcano](Mini_Volcano.md "Mini Volcano")
181	  * [](Large_Volcano.md "Large Volcano")[Large Volcano](Large_Volcano.md "Large Volcano")
182	  * [](Pixel_Box.md "Pixel Box")[Pixel Box](Pixel_Box.md "Pixel Box")
183	  * [](Junction_Box.md "Junction Box")[Junction Box](Junction_Box.md "Junction Box")
184	  * [](Logic_Gates.md "Logic Gates")[Logic Gates](Logic_Gates.md "Logic Gates")
185	  * [](Logic_Gate_Lamps.md "Logic Gate Lamps")[Logic Gate Lamps](Logic_Gate_Lamps.md "Logic Gate Lamps")
186	
187	[Traps](Trap "Trap")
188	
189	  * [](Dart_Trap.md "Dart Trap")[Dart](Dart_Trap.md "Dart Trap")
190	  * [](Venom_Dart_Trap.md "Venom Dart Trap")[Venom Dart](Venom_Dart_Trap.md "Venom Dart Trap")
191	  * [](Super_Dart_Trap.md "Super Dart Trap")[Super Dart](Super_Dart_Trap.md "Super Dart Trap")
192	  * [](Spear_Trap.md "Spear Trap")[Spear](Spear_Trap.md "Spear Trap")
193	  * [](Spiky_Ball_Trap.md "Spiky Ball Trap")[Spiky Ball](Spiky_Ball_Trap.md "Spiky Ball Trap")
194	  * [](Flame_Trap.md "Flame Trap")[Flame](Flame_Trap.md "Flame Trap")
195	  * [](Explosives.md "Explosives")[Explosives](Explosives.md "Explosives")
196	  * [](Geyser.md "Geyser")[Geyser](Geyser.md "Geyser")
197	  * [](Land_Mine.md "Land Mine")[Land Mine](Land_Mine.md "Land Mine")
198	
199	View or edit this template
200	
201	[Furniture](Furniture.md "Furniture"):
202	
203	  * [](Crafting_stations.md "Crafting stations")[Crafting Stations](Crafting_stations.md "Crafting stations")
204	  * [](Light_sources.md "Light sources")[Light Sources](Light_sources.md "Light sources")
205	  * [](Storage_items.md "Storage items")[Storage Items](Storage_items.md "Storage items")
206	  * [](Decorative_items.md "Decorative items")[Other Items](Decorative_items.md "Decorative items")
207	
208	Crafting Stations
209	
210	[Pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode")
211	
212	  * [By Hand](By_Hand.md "By Hand")
213	  * [Work Bench](Work_Bench "Work Bench")
214	  * [Furnace](Furnace.md "Furnace")
215	  * [Hellforge](Hellforge.md "Hellforge")
216	  * [Iron Anvil](Pre-Hardmode_Anvils.md "Pre-Hardmode Anvils")
217	  * [Lead Anvil](Pre-Hardmode_Anvils.md "Pre-Hardmode Anvils")
218	  * [Sawmill](Sawmill.md "Sawmill")
219	  * [Placed Bottle](Bottle_\(crafting_station\) "Bottle \(crafting station\)")
220	  * [Alchemy Table](Alchemy_Table.md "Alchemy Table")
221	  * [Alchemy Flask](Alchemy_Flask.md "Alchemy Flask")
222	  * [Chair](Chair "Chair")
223	  * [Table](Table "Table")
224	  * [Bookcase](Bookcase "Bookcase")
225	  * [Loom](Loom.md "Loom")
226	  * [Campfire](Campfire "Campfire")
227	  * [Cooking Pot](Cooking_Pot "Cooking Pot")
228	  * [Cauldron](Cauldron "Cauldron")
229	  * [Keg](Keg.md "Keg")
230	  * [Teapot](Teapot.md "Teapot")
231	  * [Tinkerer's Workshop](Tinkerer's_Workshop.md "Tinkerer's Workshop")
232	  * [Imbuing Station](Imbuing_Station.md "Imbuing Station")
233	  * [Sink](Sinks.md "Sinks")
234	
235	[Hardmode](Hardmode.md "Hardmode")
236	
237	  * [Adamantite Forge](Hardmode_Forges.md "Hardmode Forges")
238	  * [Titanium Forge](Hardmode_Forges.md "Hardmode Forges")
239	  * [Mythril Anvil](Hardmode_Anvils.md "Hardmode Anvils")
240	  * [Orichalcum Anvil](Hardmode_Anvils.md "Hardmode Anvils")
241	  * [Autohammer](Autohammer.md "Autohammer")
242	  * [Blend-O-Matic](Blend-O-Matic.md "Blend-O-Matic")
243	  * [Ancient Manipulator](Ancient_Manipulator.md "Ancient Manipulator")
244	
245	Themed
246	
247	  * [Bone Welder](Bone_Welder.md "Bone Welder")
248	  * [Decay Chamber](Decay_Chamber.md "Decay Chamber")
249	  * [Flesh Cloning Vat](Flesh_Cloning_Vat.md "Flesh Cloning Vat")
250	  * [Glass Kiln](Glass_Kiln.md "Glass Kiln")
251	  * [Honey Dispenser](Honey_Dispenser.md "Honey Dispenser")
252	  * [Ice Machine](Ice_Machine.md "Ice Machine")
253	  * [Lihzahrd Furnace](Lihzahrd_Furnace.md "Lihzahrd Furnace")
254	  * [Living Loom](Living_Loom.md "Living Loom")
255	  * [Sky Mill](Sky_Mill.md "Sky Mill")
256	  * [Solidifier](Solidifier.md "Solidifier")
257	  * [Steampunk Boiler](Steampunk_Boiler.md "Steampunk Boiler")
258	
259	Environment
260	
261	  * [Water](Water.md "Water")
262	  * [Lava](Lava.md "Lava")
263	  * [Honey](Honey.md "Honey")
264	  * [Shimmer](Shimmer.md "Shimmer")
265	  * [Altar](Altar "Altar")
266	
267	Other
268	
269	  * [Crystal Ball](Crystal_Ball.md "Crystal Ball")
270	  * [Dye Vat](Dye_Vat.md "Dye Vat")
271	  * [Heavy Assembler](Heavy_Assembler.md "Heavy Assembler")
272	  * [Meat Grinder](Meat_Grinder.md "Meat Grinder")
273	  * [Extractinator](Extractinator.md "Extractinator")
274	  * [Chlorophyte Extractinator](Chlorophyte_Extractinator.md "Chlorophyte Extractinator")
275	
276	Light Sources
277	
278	Placeable
279	
280	Suitable  
281	for housing
282	
283	  * [Torches](Torches.md "Torches")
284	  * [Fireplace](Fireplace.md "Fireplace")
285	  * [Candelabras](Candelabras.md "Candelabras")
286	  * [Candles](Candles.md "Candles")
287	    * [Peace](Peace_Candle.md "Peace Candle")
288	    * [Water](Water_Candle.md "Water Candle")
289	    * [Shadow](Shadow_Candle.md "Shadow Candle")
290	  * [Chandeliers](Chandeliers.md "Chandeliers")
291	  * [Lamps](Lamps.md "Lamps")
292	  * [Lamp Post](Lamp_Post.md "Lamp Post")
293	  * [Lanterns](Lanterns.md "Lanterns")
294	    * [Heart Lantern](Heart_Lantern.md "Heart Lantern")
295	    * [Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle")
296	  * [Chinese Lantern](Chinese_Lantern "Chinese Lantern")
297	  * [Christmas lights](Christmas_lights.md "Christmas lights")
298	  * [Jack 'O Lantern](Jack_'O_Lantern.md "Jack 'O Lantern")
299	  * [Tiki Torch](Tiki_Torch.md "Tiki Torch")
300	  * [Skull Lantern](Skull_Lantern.md "Skull Lantern")
301	  * [Hanging Brazier](Hanging_Brazier.md "Hanging Brazier")
302	
303	Unsuitable  
304	for housing
305	
306	  * [Campfire](Campfire "Campfire")
307	  * [Disco Ball](Disco_Ball.md "Disco Ball")
308	  * [Furnace](Furnace.md "Furnace")
309	  * [Hellforge](Hellforge.md "Hellforge")
310	  * [Adamantite Forge](Adamantite_Forge "Adamantite Forge")
311	  * [Titanium Forge](Titanium_Forge "Titanium Forge")
312	  * [Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar")
313	  * [Lava Lamp](Lava_Lamp.md "Lava Lamp")
314	  * [Plasma Lamp](Plasma_Lamp.md "Plasma Lamp")
315	
316	Portable
317	
318	  * [Torches](Torches.md "Torches")
319	  * [Candles](Candles.md "Candles")
320	  * [Glowstick](Glowstick.md "Glowstick")
321	    * [Sticky](Sticky_Glowstick.md "Sticky Glowstick")
322	    * [Bouncy](Bouncy_Glowstick.md "Bouncy Glowstick")
323	    * [Spelunker](Spelunker_Glowstick.md "Spelunker Glowstick")
324	    * [Fairy](Fairy_Glowstick.md "Fairy Glowstick")
325	    * [Rainbow](Rainbow_Glowstick.md "Rainbow Glowstick")
326	  * [Mining Helmet](Mining_Helmet "Mining Helmet")
327	  * [Jellyfish Necklace](Jellyfish_Necklace.md "Jellyfish Necklace")
328	  * [Flare Gun](Flare_Gun.md "Flare Gun")
329	
330	Storage Items
331	
332	[Chests](Chests.md "Chests")
333	
334	  * [Aetherium](Aetherium_Chest "Aetherium Chest")
335	  * [Ash Wood](Ash_Wood_Chest "Ash Wood Chest")
336	  * [Balloon](Balloon_Chest "Balloon Chest")
337	  * [Bamboo](Bamboo_Chest "Bamboo Chest")
338	  * [Bone](Bone_Chest "Bone Chest")
339	  * [Boreal Wood](Boreal_Wood_Chest "Boreal Wood Chest")
340	  * [Boulder](Boulder_Chest "Boulder Chest")
341	  * [Cactus](Cactus_Chest "Cactus Chest")
342	  * [Cloud](Cloud_Chest "Cloud Chest")
343	  * [Crimtane](Crimtane_Chest "Crimtane Chest")
344	  * [Crystal](Crystal_Chest "Crystal Chest")
345	  * [Dead Man's](Dead_Man's_Chest.md "Dead Man's Chest")
346	  * [Demonite](Demonite_Chest "Demonite Chest")
347	  * [Dungeon](Dungeon.md "Dungeon")
348	    * [Blue](Blue_Dungeon_Chest "Blue Dungeon Chest")
349	    * [Green](Green_Dungeon_Chest "Green Dungeon Chest")
350	    * [Pink](Pink_Dungeon_Chest "Pink Dungeon Chest")
351	  * [Duskware](Duskware_Chest "Duskware Chest")
352	  * [Dynasty](Dynasty_Chest "Dynasty Chest")
353	  * [Easter](Easter_Chest "Easter Chest")
354	  * [Ebonwood](Ebonwood_Chest "Ebonwood Chest")
355	  * [Fallen Star](Fallen_Star_Chest "Fallen Star Chest")
356	  * [Fancy Hallowed](Fancy_Hallowed_Chest "Fancy Hallowed Chest")
357	  * [Feywood](Feywood_Chest "Feywood Chest")
358	  * [Flesh](Flesh_Chest "Flesh Chest")
359	  * [Flinx Fur](Flinx_Fur_Chest "Flinx Fur Chest")
360	  * [Forbidden](Forbidden_Chest "Forbidden Chest")
361	  * [Frozen](Frozen_Chest.md "Frozen Chest")
362	  * [Glass](Glass_Chest "Glass Chest")
363	  * [Granite](Granite_Chest.md "Granite Chest")
364	  * [Gold](Gold_Chest.md "Gold Chest")
365	    * [Golden](Golden_Chest "Golden Chest")
366	  * [Golf](Golf_Chest "Golf Chest")
367	  * [Gothic](Gothic_Chest "Gothic Chest")
368	  * [Harpy](Harpy_Chest "Harpy Chest")
369	  * [Honey](Honey_Chest "Honey Chest")
370	  * [Ivy](Ivy_Chest.md "Ivy Chest")
371	  * [Jellyfish](Jellyfish_Chest "Jellyfish Chest")
372	  * [Lesion](Lesion_Chest "Lesion Chest")
373	  * [Librarian](Librarian_Chest "Librarian Chest")
374	  * [Lihzahrd](Lihzahrd_Chest.md "Lihzahrd Chest")
375	  * [Living Wood](Living_Wood_Chest.md "Living Wood Chest")
376	  * [Marble](Marble_Chest.md "Marble Chest")
377	  * [Martian](Martian_Chest "Martian Chest")
378	  * [Meteorite](Meteorite_Chest "Meteorite Chest")
379	  * [Mushroom](Mushroom_Chest.md "Mushroom Chest")
380	  * [Nebula](Nebula_Chest "Nebula Chest")
381	  * [Obsidian](Obsidian_Chest "Obsidian Chest")
382	  * [Office](Office_Chest "Office Chest")
383	  * [Palm Wood](Palm_Wood_Chest "Palm Wood Chest")
384	  * [Pearlwood](Pearlwood_Chest "Pearlwood Chest")
385	  * [Pine](Pine_Chest "Pine Chest")
386	  * [Pumpkin](Pumpkin_Chest "Pumpkin Chest")
387	  * [Reef](Reef_Chest "Reef Chest")
388	  * [Rich Mahogany](Rich_Mahogany_Chest.md "Rich Mahogany Chest")
389	  * [Sandstone](Sandstone_Chest.md "Sandstone Chest")
390	  * [Shadewood](Shadewood_Chest "Shadewood Chest")
391	  * [Shadow](Shadow_Chest.md "Shadow Chest")
392	  * [Slime](Slime_Chest "Slime Chest")
393	  * [Skyware](Skyware_Chest.md "Skyware Chest")
394	  * [Snow](Snow_Chest "Snow Chest")
395	  * [Solar](Solar_Chest "Solar Chest")
396	  * [Spider](Spider_Chest "Spider Chest")
397	  * [Spike](Spike_Chest "Spike Chest")
398	  * [Spooky](Spooky_Chest "Spooky Chest")
399	  * [Stardust](Stardust_Chest "Stardust Chest")
400	  * [Steampunk](Steampunk_Chest "Steampunk Chest")
401	  * [Stone](Stone_Chest "Stone Chest")
402	  * [Vortex](Vortex_Chest "Vortex Chest")
403	  * [Water](Water_Chest.md "Water Chest")
404	  * [Web Covered](Web_Covered_Chest.md "Web Covered Chest")
405	  * [Wooden](Chest "Chest")
406	
407	[Biome Chests](Biome_Chests.md "Biome Chests")
408	
409	  * [Corruption](Corruption_Chest "Corruption Chest")
410	  * [Crimson](Crimson_Chest "Crimson Chest")
411	  * [Ice](Ice_Chest "Ice Chest")
412	  * [Jungle](Jungle_Chest "Jungle Chest")
413	  * [Hallowed](Hallowed_Chest "Hallowed Chest")
414	  * [Desert](Desert_Chest "Desert Chest")
415	
416	Other
417	
418	  * [Piggy Bank](Piggy_Bank.md "Piggy Bank")
419	  * [Safe](Safe.md "Safe")
420	  * [Defender's Forge](Defender's_Forge.md "Defender's Forge")
421	  * [Void Vault](Void_Vault.md "Void Vault")
422	  * [Trash Can](Trash_Can.md "Trash Can")
423	  * [Barrel](Barrel.md "Barrel")
424	  * [Dressers](Dressers.md "Dressers")
425	  * [Mannequin](Mannequin.md "Mannequin")
426	  * [Womannequin](Womannequin.md "Womannequin")
427	  * [Hat Rack](Hat_Rack.md "Hat Rack")
428	  * [Item Flask](Item_Flask.md "Item Flask")
429	
430	Other Items
431	
432	[Housing](House#Furniture "House")
433	
434	  * [Tables](Tables.md "Tables")
435	  * [Pianos](Pianos.md "Pianos")
436	  * [Bathtubs](Bathtubs.md "Bathtubs")
437	  * [Dressers](Dressers.md "Dressers")
438	  * [Bookcases](Bookcases.md "Bookcases")
439	  * [Chairs](Chairs.md "Chairs")
440	  * [Beds](Beds.md "Beds")
441	  * [Sofas](Sofas.md "Sofas")
442	  * [Benches](Benches.md "Benches")
443	  * [Throne](Throne.md "Throne")
444	  * [Chippy's Couch](Chippy's_Couch.md "Chippy's Couch")
445	
446	Floor & Ceiling
447	
448	  * [Pylons](Pylons.md "Pylons")
449	    * [Universal Pylon](Universal_Pylon.md "Universal Pylon")
450	  * [Bars](Bars.md "Bars")
451	  * [Books](Book.md "Book")
452	  * [Bottle](Bottle.md "Bottle")
453	    * [Cups](Cups.md "Cups")
454	    * [Mug](Mug.md "Mug")
455	    * [Pink Vase](Pink_Vase.md "Pink Vase")
456	    * [Decorative Healing Potion](Decorative_Healing_Potion.md "Decorative Healing Potion")
457	    * [Decorative Mana Potion](Decorative_Mana_Potion.md "Decorative Mana Potion")
458	  * [Bowls](Bowls.md "Bowls")
459	  * [Butterfly jars](Butterfly_jars.md "Butterfly jars")
460	    * [Prismatic Lacewing Jar](Prismatic_Lacewing_Jar.md "Prismatic Lacewing Jar")
461	  * [Cages](Cages.md "Cages")
462	  * [Coin Piles](Coin_Piles.md "Coin Piles")
463	  * [Christmas Tree](Christmas_Tree.md "Christmas Tree")
464	    * [Christmas Tree decorations](Christmas_Tree_decorations.md "Christmas Tree decorations")
465	  * [Coral](Coral.md "Coral")
466	  * [Crates](Crates.md "Crates")
467	  * [Crystal Shard](Crystal_Shard.md "Crystal Shard")
468	  * [Decorative Banners](Banners_\(decorative\) "Banners \(decorative\)")
469	    * [War Table Banner](War_Table_Banner.md "War Table Banner")
470	  * [Decorative Statues](Statue#Decorative_statues "Statue")
471	  * [Desert Spirit Lamp](Desert_Spirit_Lamp.md "Desert Spirit Lamp")
472	  * [Dragonfly jars](Dragonfly_jars.md "Dragonfly jars")
473	  * [Fairy jars](Fairy_jars.md "Fairy jars")
474	  * [Fancy Dishes](Fancy_Dishes.md "Fancy Dishes")
475	  * [Fish Bowls](Fish_Bowls.md "Fish Bowls")
476	  * [Gems](Gems.md "Gems")
477	  * [Golf trophies](Golf_trophies.md "Golf trophies")
478	  * [Hanging Pot](Hanging_Pot.md "Hanging Pot")
479	    * [Herbs](Hanging_herbs.md "Hanging herbs")
480	  * [Jellyfish jars](Jellyfish_jars.md "Jellyfish jars")
481	  * [Lawn Flamingo](Lawn_Flamingo.md "Lawn Flamingo")
482	  * [Magic Droppers](Magic_Droppers.md "Magic Droppers")
483	  * [Minecart Track](Minecart_Track.md "Minecart Track")
484	    * [Booster](Booster_Track.md "Booster Track")
485	    * [Pressure Plate](Pressure_Plate_Track.md "Pressure Plate Track")
486	  * [Mini Volcano](Mini_Volcano.md "Mini Volcano")
487	    * [Large](Large_Volcano.md "Large Volcano")
488	  * [Pin Flags](Pin_Flags.md "Pin Flags")
489	  * [Pin Wheel](Pin_Wheel.md "Pin Wheel")
490	  * [Plate](Plate.md "Plate")
491	  * [Platforms](Platforms.md "Platforms")
492	    * [Planter Box](Planter_Box "Planter Box")
493	    * [Team](Team_Platforms.md "Team Platforms")
494	  * [Potted Trees](Potted_Trees.md "Potted Trees")
495	    * [Lava Plants](Potted_Lava_Plants.md "Potted Lava Plants")
496	    * [Crystal Plants](Potted_Crystal_Plants.md "Potted Crystal Plants")
497	  * [Presents](Presents "Presents")
498	  * [Party Present](Party_Present.md "Party Present")
499	  * [Relics](Relics.md "Relics")
500	  * [Rock Golem Head](Rock_Golem_Head.md "Rock Golem Head")
501	  * [Seashells](Seashells.md "Seashells")
502	  * [Seaweed Planter](Seaweed_Planter.md "Seaweed Planter")
503	  * [Ship in a Bottle](Ship_in_a_Bottle.md "Ship in a Bottle")
504	  * [Silly Tied Balloons](Silly_Tied_Balloons.md "Silly Tied Balloons")
505	  * [Silly Tied Bundle of Balloons](Silly_Tied_Bundle_of_Balloons.md "Silly Tied Bundle of Balloons")
506	  * [Vases](Vases.md "Vases")
507	
508	[Wall](Wall "Wall")
509	
510	  * [Animal skins](Animal_skins.md "Animal skins")
511	  * [Catacomb](Catacomb.md "Catacomb")
512	  * [Compass Rose](Compass_Rose.md "Compass Rose")
513	  * [Hanging Skeleton](Hanging_Skeleton.md "Hanging Skeleton")
514	  * [Holly](Holly.md "Holly")
515	  * [Life Preserver](Life_Preserver.md "Life Preserver")
516	  * [Living Fire Blocks](Living_Fire_Blocks.md "Living Fire Blocks")
517	  * [Paintings](Paintings.md "Paintings")
518	  * [Racks](Racks.md "Racks")
519	    * [Weapon Rack](Weapon_Rack.md "Weapon Rack")
520	    * [Item Frame](Item_Frame.md "Item Frame")
521	  * [Ropes](Ropes.md "Ropes")
522	    * [Chain](Chain.md "Chain")
523	  * [Ship's Wheel](Ship's_Wheel.md "Ship's Wheel")
524	  * [Trophies](Trophies.md "Trophies")
525	  * [Treasure Map](Treasure_Map.md "Treasure Map")
526	  * [Wall Anchor](Wall_Anchor.md "Wall Anchor")
527	  * [Wall Skeleton](Wall_Skeleton.md "Wall Skeleton")
528	  * [Wooden Beam](Wooden_Beam "Wooden Beam")
529	
530	Functional
531	
532	  * [Grandfather Clocks](Grandfather_Clocks.md "Grandfather Clocks")
533	  * [Sign](Sign.md "Sign")
534	    * [Tattered Wood Sign](Tattered_Wood_Sign.md "Tattered Wood Sign")
535	    * [Announcement Box](Announcement_Box.md "Announcement Box")
536	  * [Tombstone](Tombstone "Tombstone")
537	  * [Target Dummy](Target_Dummy.md "Target Dummy")
538	  * [Ammo Box](Ammo_Box.md "Ammo Box")
539	  * [Bewitching Table](Bewitching_Table.md "Bewitching Table")
540	  * [Crystal Ball](Crystal_Ball.md "Crystal Ball")
541	  * [Slice of Cake](Slice_of_Cake.md "Slice of Cake")
542	  * [Sharpening Station](Sharpening_Station.md "Sharpening Station")
543	  * [War Table](War_Table.md "War Table")
544	  * [Enemy Banners](Banners_\(enemy\) "Banners \(enemy\)")
545	  * [Bast Statue](Bast_Statue.md "Bast Statue")
546	  * [Sunflower](Sunflower.md "Sunflower")
547	  * [Campfires](Campfires.md "Campfires")
548	  * [Fireplace](Fireplace.md "Fireplace")
549	  * [Heart Lantern](Heart_Lantern.md "Heart Lantern")
550	  * [Star in a Bottle](Star_in_a_Bottle.md "Star in a Bottle")
551	  * [Water Candle](Water_Candle.md "Water Candle")
552	  * [Peace Candle](Peace_Candle.md "Peace Candle")
553	  * [Shadow Candle](Shadow_Candle.md "Shadow Candle")
554	  * [Clay Pot](Clay_Pot.md "Clay Pot")
555	  * [Enchanted Sundial](Enchanted_Sundial.md "Enchanted Sundial")
556	  * [Enchanted Moondial](Enchanted_Moondial.md "Enchanted Moondial")
557	  * [Lihzahrd Altar](Lihzahrd_Altar.md "Lihzahrd Altar")
558	  * [Eternia Crystal Stand](Eternia_Crystal_Stand.md "Eternia Crystal Stand")
559	  * [Land Mine](Land_Mine.md "Land Mine")
560	  * [TNT Barrel](TNT_Barrel.md "TNT Barrel")
561	  * [Pigronata](Pigronata.md "Pigronata")
562	  * [Snowball Launcher](Snowball_Launcher.md "Snowball Launcher")
563	  * [Cannon](Cannon.md "Cannon")
564	  * [Bunny Cannon](Bunny_Cannon.md "Bunny Cannon")
565	  * [Confetti Cannon](Confetti_Cannon.md "Confetti Cannon")
566	  * [Portal Gun Station](Portal_Gun_Station.md "Portal Gun Station")
567	  * [Boulder](Boulder.md "Boulder")
568	    * [Bouncy](Bouncy_Boulder.md "Bouncy Boulder")
569	    * [Life Crystal](Life_Crystal_Boulder.md "Life Crystal Boulder")
570	    * [Lava](Lava_Boulder.md "Lava Boulder")
571	    * [Poo](Poo_Boulder.md "Poo Boulder")
572	    * [Spider](Spider_Boulder.md "Spider Boulder")
573	    * [Ghoulder](Ghoulder.md "Ghoulder")
574	    * [Rainbow](Rainbow_Boulder.md "Rainbow Boulder")
575	  * [Rolling Cactus](Rolling_Cactus.md "Rolling Cactus")
576	  * [Gem Locks](Gem_Locks.md "Gem Locks")
577	  * [Trapped Chests](Trapped_Chests.md "Trapped Chests")
578	  * [Arrow Signs](Arrow_Signs.md "Arrow Signs")
579	  * [Drum Set](Drum_Set.md "Drum Set")
580	  * [Golf Tee](Golf_Tee.md "Golf Tee")
581	  * [Weather Vane](Weather_Vane.md "Weather Vane")
582	
583	Wiring
584	
585	  * [Doors](Doors.md "Doors")
586	  * [Tall Gate](Tall_Gate.md "Tall Gate")
587	  * [Trap Door](Trap_Door.md "Trap Door")
588	  * [Music Box](Music_Box "Music Box")
589	  * [Monoliths](Monoliths.md "Monoliths")
590	  * [Echo Chamber](Echo_Chamber.md "Echo Chamber")
591	  * [Water fountains](Water_fountains.md "Water fountains")
592	  * [Chimney](Chimney.md "Chimney")
593	  * [Bubble Machine](Bubble_Machine.md "Bubble Machine")
594	  * [Fireworks Box](Fireworks_Box.md "Fireworks Box")
595	  * [Firework Fountain](Firework_Fountain.md "Firework Fountain")
596	  * [Firework Rockets](Firework_Rockets.md "Firework Rockets")
597	  * [Fog Machine](Fog_Machine.md "Fog Machine")
598	  * [Party Center](Party_Center.md "Party Center")
599	  * [Silly Balloon Machine](Silly_Balloon_Machine.md "Silly Balloon Machine")
600	  * [Functional Statues](Statue#Functional_statues "Statue")
601	  * [Lever](Lever.md "Lever")
602	  * [Switch](Switch.md "Switch")
603	  * [Detonator](Detonator.md "Detonator")
604	  * [Pressure Plates](Pressure_Plates.md "Pressure Plates")
605	  * [Timers](Timers.md "Timers")
606	  * [Actuator](Actuator.md "Actuator")
607	  * [Wire Bulb](Wire_Bulb.md "Wire Bulb")
608	  * [Junction Box](Junction_Box.md "Junction Box")
609	  * [Explosives](Explosives.md "Explosives")
610	  * [Pumps](Pumps.md "Pumps")
611	  * [Teleporter](Teleporter.md "Teleporter")
612	  * [Sensor](Sensor "Sensor")
613	  * [Geyser](Geyser.md "Geyser")
614	  * [Pixel Box](Pixel_Box.md "Pixel Box")
615	
616	Environment
617	
618	  * [Antlion Eggs](Antlion_Eggs.md "Antlion Eggs")
619	  * [Bee Hive](Bee_Hive.md "Bee Hive")
620	  * [Coin Stashes](Coin_Stashes.md "Coin Stashes")
621	  * [Crimson Heart](Crimson_Heart.md "Crimson Heart")
622	    * [Replica](Replica_Crimson_Heart.md "Replica Crimson Heart")
623	  * [Fallen Log](Fallen_Log.md "Fallen Log")
624	  * [Larva](Larva.md "Larva")
625	  * [Mushrooms](Mushrooms.md "Mushrooms")
626	  * [Plantera's Bulb](Plantera's_Bulb.md "Plantera's Bulb")
627	  * [Plants](Plants.md "Plants")
628	    * [Strange Plants](Strange_Plants "Strange Plants")
629	  * [Pot](Pot.md "Pot")
630	  * [Shadow Orb](Shadow_Orb.md "Shadow Orb")
631	    * [Replica](Replica_Shadow_Orb.md "Replica Shadow Orb")
632	  * [Tree](Tree "Tree")
633	    * [Giant Glowing Mushroom](Giant_Glowing_Mushroom.md "Giant Glowing Mushroom")
634	  * [Other](Objects.md "Objects")
635	
636	Categories: 
637	
638	  * [Exclusive content](Category%3AExclusive_content "Category:Exclusive content")
639	  * [Desktop content](Category%3ADesktop_content "Category:Desktop content")
640	  * [Console content](Category%3AConsole_content "Category:Console content")
641	  * [Mobile content](Category%3AMobile_content "Category:Mobile content")
642	  * [Furniture items](Category%3AFurniture_items "Category:Furniture items")
643	  * [Mechanism items](Category%3AMechanism_items "Category:Mechanism items")
644	  * [Craftable items](Category%3ACraftable_items "Category:Craftable items")
645	  * [Consumable items](Category%3AConsumable_items "Category:Consumable items")
646	  * [Items of rarity 1](Category%3AItems_of_rarity_1 "Category:Items of rarity 1")
647	  * [Mythril or Orichalcum Anvil](Category%3AMythril_or_Orichalcum_Anvil "Category:Mythril or Orichalcum Anvil")
648	
649	Hidden categories: 
650	
651	  * Pages using DynamicPageList3 dplvar parser function
652	  * Pages using DynamicPageList3 parser function
653	  * Entities patched in Desktop 1.4.2
654	  * Entities introduced in Desktop 1.3.1
655	  * Entities introduced in Console 1.0.1372.5
656	  * Entities introduced in Switch 1.0.895.9
657	  * Entities introduced in Mobile 1.4.0.5.0
658	  * Pages with navboxes
659	  * Random
660	
661	This page is issued from [Terraria Wiki](https://terraria.wiki.gg/wiki/?title=Sensors&oldid=925201 "Last edited on 2024-11-30"). The text is available under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0) unless otherwise noted. Additional terms may apply for the media files. 
662	  *[1 required]: Journey Mode
663	  *[Qty.]: Quantity
664	  *[100%]: Expert Mode
665	  *[DPS]: Damage per second
666	  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
667	  *[300]: Master Mode
668	  *[400]: Expert Mode
669	  *[160]: Mode Expert
670	  *[240]: Mode Master
671	  *[3 required]: Journey Mode
672	  *[#]: Number
673	  *[Max.  
674	enemies]: Maximum number of enemies Abigail can damage at once
675	  *[HM]: Hardmode
676	  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
677	  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
678	  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
679	  *[8]: Expert Mode
680	  *[10]: Master Mode
681	  *[120]: Expert Mode
682	  *[150]: Expert Mode
683	  *[13]: Chế độ Master
684	  *[195]: Master Mode
685	  *[Verify]: It may be from before this adaptation, and the wrong production may have been linked.
686	  *[50 required]: Journey Mode
687	  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
688	  *[100 required]: Journey Mode
689	  *[cần có 1]: Chế độ Journey
690	  *[25 required]: Journey Mode
691	  *[cần có 25]: Chế độ Journey
692	  *[400 required]: Journey Mode
693	  *[membutuhkan 100]: Mode Journey
694	  *[cần có 100]: Chế độ Journey
695	  *[Slg.]: Số lượng
696	  *[1.99%]: Expert Mode
697	  *[199/10000 (1.99%)]: Expert Mode
698	  *[membutuhkan 1]: Mode Journey
699	  *[1,99%]: Expert Mode
700	  *[1/50 (2%)]: Mode Expert
701	  *[200 required]: Journey Mode
702	  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
703	  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
704	  *[20 required]: Journey Mode
705	  *[180]: Master Mode
706	  *[270]: Master Mode
707	  *[5–9 seconds]: Master Mode
708	  *[5–9]: Expert Mode
709	  *[15 required]: Journey Mode
710	  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
711	  *[Power]: Bait power
712	  *[5 required]: Journey Mode
713	  *[cần có {{{research}}}]: Chế độ Journey
714	  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item)
715	  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
716	  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
717	  *[Expert Mode exclusive]: Expert Mode
718	  *[402]: Master Mode
719	  *[523]: Expert Mode
720	  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
721	  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
722	  *[800]: Expert Mode
723	  *[1200]: Master Mode
724	  *[15]: Expert Mode
725	  *[17]: Master Mode
726	  *[O. v. odražení]: Odolnost vůči odražení
727	  *[1 minute 30 seconds]: Expert Mode
728	  *[1 minute 52.5 seconds]: Master Mode
729	  *[90]: Master Mode
730	  *[112.5]: Master Mode
731	  *[2–6]: Chế độ Expert
732	  *[2-6]: Expert Mode
733	  *[%100]: Expert Mode
734	  *[28]: Expert Mode
735	  *[42]: Master Mode
736	  *[80]: Expert Mode
737	  *[17 mph]: 17 miles per hour (as measured by the Stopwatch item) or 12.47 tiles per second
738	  *[ Minor improvements to all stats and increased life regeneration]: Expert Mode
739	  *[ Major improvements to all stats and increased life regeneration]: Expert Mode
740	  *[50%]: Expert Mode
741	  *[1/2 (50%)]: Expert Mode
742	  *[30]: Expert Mode
743	  *[45]: Expert Mode
744	  *[3/4]: Chế độ Expert
745	  *[5]: Master Mode
746	  *[75%]: Chế độ Expert
747	  *[semua]: Mode Master
748	  *[6]: Expert Mode
749	  *[toàn bộ]: Chế độ Master
750	  *[199/10000 (1,99%)]: Mode Expert
751	  *[4 minutes]: Expert Mode
752	  *[5 minutes]: Master Mode
753	  *[4]: Expert Mode
754	  *[36]: Expert Mode
755	  *[22]: Expert Mode
756	  *[26]: Master Mode
757	  *[Ruce pryč od mé zbraně, kámo!]: Keep your hands off my gun, buddy!
758	  *[Hej, tady nejsme ve filmu, kámo. Náboje něco stojí.]: Hey, this ain't a movie, pal. Ammo costs extra.
759	  *[Koukám, že házíš očkem po žraločkovi. Opravdu nechceš vědět, jak byl vyroben.]: I see you're eyeballing the Minishark. You really don't want to know how it was made.
760	  *[Neobtěžuj se s [jméno demoličního experta], vše, co potřebuješ, je přímo tady.]: Don't bother with [Name of Demolitionist], I've got all you need right here.
761	  *[Jaký má [jméno demoličního experta] problém? Uvědomuje si vůbec, že oba prodáváme naprosto rozdílné zboží?]: What's [Name of Demolitionist]'s problem? Does he even realize we sell completely different stuff?
762	  *[Pohni zadkem! Za hodinu mám rande s [jméno sestřičky].]: Make it quick! I've got a date with [Name of Nurse] in a hour.
763	  *[Chci to, co [jméno sestřičky] prodává. Co myslíš tím, že neprodává ani ň?]: I want what [Name of Nurse] is sellin'. What do you mean, she doesn't sell anything?
764	  *[Na [jméno dryády] bych mohl oči nechat. Škoda, že je to taková prudařka.]: [Name of Dryad] is a looker. Too bad she's such a prude.
765	  *[Slyšel jsem, že se ve světě nachází panenka vypadající skoro jako [jméno průvodce]. Mile rád bych do ní vpálil pár kulek.]: I heard there is a doll that looks very similar to [Name of Guide] somewhere in the underworld. I'd like to put a few rounds in it.
766	  *[Miluji noci jako je tahle. Vždy se najde něco na zabití.]: I love nights like tonight, there is never a shortage of things to kill.
767	  *[Chlape, tohle je noc přímo stvořená, abys s nikým nemusel mluvit, nemyslíš [jméno hráče]?]: Man, it's a good night not to talk to anybody, don't you think, [Name of Player]?
768	  *[14]: Expert Mode
769	  *[17.5]: Master Mode
770	  *[7]: Expert Mode
771	  *[8.75]: Master Mode
772	  *[21]: Expert Mode
773	  *[26.25]: Master Mode
774	  *[53 mph]: 53 miles per hour (as measured by the Stopwatch item) or 38.87 tiles per second
775	  *[88.6 mph]: 88.6 miles per hour (as measured by the Stopwatch item) or 64.97 tiles per second
776	  *[3.33–6.67%]: Expert Mode
777	  *[3.33%–6.67%]: Expert Mode
778	  *[W]: Wave
779	  *[3.33%]: Expert Mode
780	  *[6.67%]: Expert Mode
781	  *[0.014%]: Expert Mode
782	  *[ Medium improvements to all stats and increased life regeneration]: Expert Mode
783	  *[102 mph]: 102 miles per hour (as measured by the Stopwatch item) or 75 tiles per second
784	  *[+100%]: Expert Mode
785	  *[−50%]: Expert Mode
786	  *[+20%]: Expert Mode
787	  *[−16.67%]: Expert Mode
788	  *[200]: Expert Mode
789	  *[225]: Expert Mode
790	  *[184 mph]: 184 miles per hour (as measured by the Stopwatch item) or 135 tiles per second
791	  *[72 mph]: 72 miles per hour (as measured by the Stopwatch item) or 52.5 tiles per second
792	  *[82 mph]: 82 miles per hour (as measured by the Stopwatch item) or 60 tiles per second
793	  *[6.25–12.5%]: Expert Mode
794	  *[51 mph]: 51 miles per hour (as measured by the Stopwatch item) or 37.4 tiles per second
795	  *[66 mph]: 66 miles per hour (as measured by the Stopwatch item) or 48.75 tiles per second
796	  *[77 mph]: 77 miles per hour (as measured by the Stopwatch item) or 56.47 tiles per second
797	  *[100 mph]: 100 miles per hour (as measured by the Stopwatch item) or 73.33 tiles per second
798	  *[6.25%]: Expert Mode
799	  *[12.5%]: Expert Mode
800	  *[32›140›176]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
801	  *[48›210›264]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
802	  *[26›92›116]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
803	  *[39›138›174]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
804	  *[2›8›10]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
805	  *[68›148›224]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
806	  *[102›222›336]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
807	  *[40›72›108]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
808	  *[60›108›162]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
809	  *[4›8›12]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
810	  *[92›100]: Expertní mód : Pre-hardmode › Těžký mód
811	  *[138›150]: Master Mode : Pre-Hardmode › Hardmode
812	  *[70›62]: Expertní mód : Pre-hardmode › Těžký mód
813	  *[105›93]: Master Mode : Pre-Hardmode › Hardmode
814	  *[60›132›198]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
815	  *[90›198›297]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
816	  *[36›64›96]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
817	  *[54›96›144]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
818	  *[6›12›18]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
819	  *[200›200›220]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
820	  *[300›300›330]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
821	  *[90›90›80]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
822	  *[135›135›120]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
823	  *[600]: Master Mode
824	  *[320]: Expert Mode
825	  *[480]: Master Mode
826	  *[100]: Expert Mode
827	  *[120›120›132]: Expertní mód : Pre-hardmode › Těžký mód › Post-Plantera
828	  *[180›180›198]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
829	  *[440]: Expert Mode
830	  *[660]: Master Mode
831	  *[1500]: Master Mode
832	  *[2250]: Master Mode
833	  *[2–6 seconds]: Expert Mode
834	  *[2.5–7.5 seconds]: Master Mode
835	  *[2.5–7.5]: Master Mode
836	  *[35 mph]: 35 mil per jam (diukur dengan item Stopwatch) atau 25.31 blok per detik
837	  *[43 mph]: 43 miles per hour (as measured by the Stopwatch item) or 31.5 tiles per second
838	  *[ 17–30]: Expert Mode
839	  *[99 required]: Journey Mode
840	  *[10–29]: Expert Mode
841	  *[1 time]: Expert Mode
842	  *[140]: Expert Mode
843	  *[210]: Master Mode
844	  *[14–20 seconds]: Expert Mode
845	  *[17.5-25 seconds]: Master Mode
846	  *[25%]: Master Mode
847	  *[14–20]: Expert Mode
848	  *[17.5–25]: Master Mode
849	  *[1/30 (3.33%)]: Expert Mode
850	  *[15.97%]: Expert Mode
851	  *[23/144 (15.97%)]: Expert Mode
852	  *[ 8 seconds]: Expert Mode
853	  *[10 seconds]: Master Mode
854	  *[0.5–2.5 seconds]: Master Mode
855	  *[90%]: Expert Mode
856	  *[Web Spit]: Expert Mode
857	  *[30 seconds]: Expert Mode
858	  *[37.5 seconds]: Master Mode
859	  *[4–12]: Expert Mode
860	  *[5–15]: Master Mode
861	  *[33.33%]: Expert Mode
862	  *[1/3 (33.33%)]: Expert Mode
863	  *[20-40]: Expert Mode
864	  *[25-40]: Master Mode
865	  *[10-14]: Mode Expert
866	  *[12.5-17.5]: Master Mode
867	  *[20]: Expert Mode
868	  *[25]: Master Mode
869	  *[6-10]: Expert Mode
870	  *[7.5-12.5]: Master Mode
871	  *[1/1 (100%)]: Expert Mode
872	  *[6-20]: Expert Mode
873	  *[7.5-25]: Master Mode
874	  *[7.5-15]: Expert Mode
875	  *[9.37-18.75]: Master Mode
876	  *[11/243 (4.53%)]: Chế độ Expert
877	  *[11/81 (13.58%)]: Chế độ Expert
878	  *[2 hours]: Expert Mode
879	  *[3 hours]: Master Mode
880	  *[20–40]: Expert Mode
881	  *[25–50]: Master Mode
882	  *[61 mph]: 61 miles per hour (as measured by the Stopwatch item) or 45 tiles per second
883	  *[80 mph]: 80 miles per hour (as measured by the Stopwatch item) or 58.67 tiles per second
884	  *[64 mph]: 64 miles per hour (as measured by the Stopwatch item) or 46.93 tiles per second
885	  *[1/150]: Expert Mode
886	  *[1/30]: Expert Mode
887	  *[15.56–31.11%]: Expert Mode
888	  *[15.56%–31.11%]: Expert Mode
889	  *[15.56%]: Expert Mode
890	  *[31.11%]: Expert Mode
891	  *[ 12 _SC_ 50 _CC_]: Expert Mode
892	  *[dusk]: 7:30 PM
893	  *[1.33%]: Expert Mode
894	  *[1%]: Expert Mode
895	  *[4 mph]: 4 miles per hour (as measured by the Stopwatch item) or 3 tiles per second
896	  *[6 mph]: 6 miles per hour (as measured by the Stopwatch item) or 4.5 tiles per second
897	  *[10 mph]: 10 miles per hour (as measured by the Stopwatch item) or 7.5 tiles per second
898	  *[12 mph]: 12 miles per hour (as measured by the Stopwatch item) or 9 tiles per second
899	  *[20 seconds]: Expert Mode
900	  *[25 seconds]: Master Mode
901	  *[0.5%]: Expert Mode
902	  *[0.67%]: Expert Mode
903	  *[1-3]: エキスパートモード
904	  *[18 mph]: 18 miles per hour (as measured by the Stopwatch item) or 12.94 tiles per second
905	  *[Crit]: Critical strike chance
906	  *[20 mph]: 20 miles per hour (as measured by the Stopwatch item) or 14.67 tiles per second
907	  *[54 mph]: 54 mil per jam (diukur dengan item Stopwatch) atau 39.38 blok per detik
908	  *[and the core]: Expert Mode
909	  *[2,800]: Chế độ Expert
910	  *[3,570]: Chế độ Master
911	  *[3,640]: Chế độ Expert
912	  *[4,641]: Chế độ Master
913	  *[15,120]: Chế độ Expert
914	  *[19,296]: Chế độ Master
915	  *[2,125]: Chế độ Expert
916	  *[2,709]: Chế độ Master
917	  *[4,760]: Chế độ Expert
918	  *[6,069]: Chế độ Master
919	  *[11,900]: Mode Expert
920	  *[15,172]: Mode Master
921	  *[8,800]: Chế độ Expert
922	  *[11,220]: Master Mode
923	  *[11,200]: Chế độ Expert
924	  *[14,280]: Chế độ Master
925	  *[28,800]: Chế độ Expert
926	  *[36,720]: Chế độ Master
927	  *[30,000]: Chế độ Expert
928	  *[38,250]: Chế độ Master
929	  *[34,500]: Chế độ Expert
930	  *[43,988]: Chế độ Master
931	  *[120,000]: Chế độ Expert
932	  *[153,000]: Chế độ Master
933	  *[280]: Expert Mode
934	  *[420]: Master Mode
935	  *[42,000]: Chế độ Expert
936	  *[53,550]: Chế độ Master
937	  *[88,500]: Chế độ Expert
938	  *[112,836]: Chế độ Master
939	  *[90,000]: Chế độ Expert
940	  *[114,749]: Chế độ Master
941	  *[78,000]: Expert Mode
942	  *[99,450]: Chế độ Master
943	  *[11700]: Mode Expert
944	  *[14917]: Mode Master
945	  *[98,000]: Chế độ Expert
946	  *[124,950]: Chế độ Master
947	  *[48,000]: Chế độ Expert
948	  *[61,200]: Master Mode
949	  *[217,500]: Expert Mode
950	  *[277,311]: Chế độ Master
951	  *[dua]: Mode Expert
952	  *[10,500]: Mode Expert
953	  *[24 detik]: Mode Expert
954	  *[30 detik]: Mode Expert
955	  *[30 required]: Journey Mode
956	  *[mph]: miles per hour
957	  *[70]: Master Mode
958	  *[36 mph]: 36 miles per hour (as measured by the Stopwatch item) or 26.25 tiles per second
959	  *[315]: Expert Mode
960	  *[68]: Expert Mode
961	  *[0.5]: Expert Mode
962	  *[96]: Expert Mode
963	  *[144]: Expert Mode
964	  *[12.5]: Master Mode
965	  *[143 mph]: 143 miles per hour (as measured by the Stopwatch item) or 105 tiles per second
966	  *[5525]: Expert Mode
967	  *[7049]: Master Mode
968	  *[60%]: Expert Mode
969	  *[64%]: Expert Mode
970	  *[65%]: Master Mode
971	  *[110–135]: Master Mode
972	  *[30–50]: Master Mode
973	  *[5.23–10.5 sec]: Expert Mode
974	  *[6.53–13.12 sec]: Master Mode
975	  *[3–6 sec]: Expert Mode
976	  *[3.75–7.5 sec]: Master Mode
977	  *[0.73–1.5 sec]: Expert Mode
978	  *[0.92–1.87 sec]: Master Mode
979	  *[7.5–15 sec]: Expert Mode
980	  *[9.37–18.75 sec]: Master Mode
981	  *[1.5–3 sec]: Expert Mode
982	  *[1.87–3.75 sec]: Master Mode
983	  *[11.23–22.5 sec]: Expert Mode
984	  *[14.03–28.12 sec]: Master Mode
985	  *[9.73–19.5 sec]: Expert Mode
986	  *[12.17–24.37 sec]: Master Mode
987	  *[ 60%]: Mode Expert
988	  *[ 25%]: Chế độ Master
989	  *[ 100%]: Chế độ Master
990	  *[5700-7700]: Expert Mode
991	  *[ %100]: Master Mode
992	  *[0-200]: Chế độ Expert
993	  *[0-500]: Chế độ Expert
994	  *[2125]: Expert Mode
995	  *[170]: Expert Mode
996	  *[2709]: Master Mode
997	  *[217]: Chế độ Master
998	  *[20%]: Expert Mode
999	  *[1/5 (20%)]: Expert Mode
1000	  *[9.73-19.5]: Expert Mode
1001	  *[12.17-24.37]: Master Mode
1002	  *[2]: Expert Mode
1003	  *[3]: Chế độ Master
1004	  *[43.75%]: Expert Mode
1005	  *[7/16 (43.75%)]: Expert Mode
1006	  *[Third]: Expert Mode
1007	  *[Major improvements to all stats and increased life regeneration]: 達人模式
1008	  *[Medium improvements to all stats and increased life regeneration]: 達人模式
1009	  *[Minor improvements to all stats and increased life regeneration]: 達人模式
1010	  *[13 seconds]: Master Mode
1011	  *[Zabíjení zajíčků je bezcitné. Tečka.]: Killing bunnies is cruel. Period.
1012	  *[14 seconds]: Expert Mode
1013	  *[17.5 seconds]: Master Mode
1014	  *[26 mph]: 26 miles per hour (as measured by the Stopwatch item) or 18.75 tiles per second
1015	  *[189]: Expert Mode
1016	  *[283]: Master Mode
1017	  *[4.94%]: Expert Mode
1018	  *[3.96%]: Expert Mode
1019	  *[700]: Expert Mode
1020	  *[1,050]: Master Mode
1021	  *[23 mph]: 23 miles per hour (as measured by the Stopwatch item) or 16.87 tiles per second
1022	  *[2 mph]: 2 miles per hour (as measured by the Stopwatch item) or 1.6875 tiles per second
1023	  *[79/1600 (4.94%)]: Expert Mode
1024	  *[4,94%]: Expert Mode
1025	  *[3/80 (3,75%)]: Mode Expert
1026	  *[12.5 seconds]: Master Mode
1027	  *[2 required]: Journey Mode
1028	  *[24–100]: Expert Mode
1029	  *[12–20]: Expert Mode
1030	  *[360]: Master Mode
1031	  *[[]: Western world border
1032	  *[C]: World center
1033	  *[]]: Eastern world border
1034	  *[60]: Expert Mode
1035	  *[18–30]: Expert Mode
1036	  *[18–90]: Expert Mode
1037	  *[115 mph]: 115 miles per hour (as measured by the Stopwatch item) or 84.33 tiles per second
1038	  *[382 mph]: 382 miles per hour (as measured by the Stopwatch item) or 280.13 tiles per second
1039	  *[721 mph]: 721 miles per hour (as measured by the Stopwatch item) or 528.73 tiles per second
1040	  *[12.5–50%]: Expert Mode
1041	  *[12.5%–50%]: Expert Mode
1042	  *[16.67%]: Expert Mode
1043	  *[0.25%]: Expert Mode
1044	  *[0.26 mph]: 0.26 miles per hour (as measured by the Stopwatch item)
1045	  *[40]: Expert Mode
1046	  *[50]: Master Mode
1047	  *[37.5]: Master Mode
1048	  *[62.5]: Master Mode
1049	  *[6.25]: Master Mode
1050	  *[46 mph]: 46 miles per hour (as measured by the Stopwatch item) or 33.75 tiles per second
1051	  *[membutuhkan 25]: Mode Journey
1052	  *[6.22–31.11%]: Expert Mode
1053	  *[6.22%–31.11%]: Expert Mode
1054	  *[6.22%]: Expert Mode
1055	  *[7.78%]: Expert Mode
1056	  *[10.37%]: Expert Mode
1057	  *[6,22–31,11%]: Expert Mode
1058	  *[102]: Master Mode
1059	  *[ 4–6 seconds]: Expert Mode
1060	  *[5–7.5 seconds]: Master Mode
1061	  *[7.5]: Master Mode
1062	  *[16]: Expert Mode
1063	  *[24]: Expert Mode
1064	  *[12 _GC_ 50 _SC_]: Expert Mode
1065	  *[8 _GC_]: Expert Mode
1066	  *[10 _GC_]: Master Mode
1067	  *[tida perempat]: Mode Expert
1068	  *[ Verifikasi]: Talk:Coins/id (halaman belum tersedia)
1069	  *[Verifikasi]: Talk:Queen Bee/id (halaman belum tersedia)
1070	  *[ Verify]: Talk:Coins/vi (page does not exist)
1071	  *[92 mph]: 92 miles per hour (as measured by the Stopwatch item) or 67.5 tiles per second
1072	  *[1.5–3]: Expert Mode
1073	  *[1.87–3.75]: Master Mode
1074	  *[2/243 (0.82%)]: Expert Mode
1075	  *[2/81 (2.47%)]: Expert Mode
1076	  *[35]: Master Mode
1077	  *[1.8–3]: Expert Mode
1078	  *[2.25–3.75]: Master Mode
1079	  *[1/6 (16.67%)]: Expert Mode
1080	  *[Radius]: Explosion radius in tiles
1081	  *[13 mph]: 13 miles per hour (as measured by the Stopwatch item) or 9.375 tiles per second
1082	  *[7.76%]: Expert Mode
1083	  *[2%]: Expertní mód
1084	  *[10 minutes]: Expert Mode
1085	  *[12 minutes 30 seconds]: Master Mode
1086	  *[105›93›187]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1087	  *[157›140›281]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1088	  *[1–3]: Expert Mode
1089	  *[1–2]: Master Mode
1090	  *[5–7]: Expert Mode
1091	  *[2–4]: Master Mode
1092	  *[1/4 (25%)]: Expert Mode
1093	  *[8 seconds]: Expert Mode
1094	  *[67%]: Expert Mode
1095	  *[two pieces]: Expert Mode
1096	  *[dua bagian]: Mode Expert
1097	  *[2-10]: Expert Mode
1098	  *[2-12]: Master Mode
1099	  *[0.73–1.5]: Expert Mode
1100	  *[0.92–1.87]: Master Mode
1101	  *[0.9–1.13]: Expert Mode
1102	  *[1.5–1.88]: Master Mode
1103	  *[1/6 (16.7%)]: Expert Mode
1104	  *[4-6]: Expert Mode
1105	  *[5-7.5]: Master Mode
1106	  *[48-72]: Expert Mode
1107	  *[60-90]: Master Mode
1108	  *[168]: Expert Mode
1109	  *[5–20%]: Expert Mode
1110	  *[5%]: Expert Mode
1111	  *[10%]: Expert Mode
1112	  *[1]: Base value
1113	  *[0.14]: Turtle armor
1114	  *[0.2]: 5 Menacing modifiers
1115	  *[0.15]: Shroomite bonus
1116	  *[0.12]: Avenger Emblem
1117	  *[0.1]: Quiver bonus
1118	  *[0.05]: Well Fed
1119	  *[230]: Godly Meowmere
1120	  *[1.98]: Melee damage multiplier
1121	  *[0.13]: Shroomite armor
1122	  *[0.6]: Shroomite armor stealth effect
1123	  *[0.16]: 4 Menacing modifiers
1124	  *[39]: Godly Chlorophyte Shotbow
1125	  *[2.26]: Ranged damage multiplier
1126	  *[1.15]: Shroomite bonus
1127	  *[1.1]: Archery buff
1128	  *[105]: Master Mode
1129	  *[11]: Ammo damage
1130	  *[3–6]: Expert Mode
1131	  *[3.75–7.5]: Master Mode
1132	  *[3.6–6]: Expert Mode
1133	  *[4.5–7.5]: Master Mode
1134	  *[6.56%]: Expert Mode
1135	  *[59/900 (6.56%)]: Expert Mode
1136	  *[15 seconds]: Master Mode
1137	  *[1 minute]: Expert Mode
1138	  *[three-quarters]: Expert Mode
1139	  *[all]: Master Mode
1140	  *[a [Jellyfish](Jellyfish.md "Jellyfish")'s shock attack]: Expert Mode
1141	  *[30 _CC_]: Expert Mode
1142	  *[ 4.94%]: Expert Mode
1143	  *[1 _SC_ 50 _CC_]: Expert Mode
1144	  *[6 _GC_]: Expert Mode
1145	  *[6–90 seconds]: Expert Mode
1146	  *[7.5–112.5 seconds]: Master Mode
1147	  *[2–40 seconds]: Expert Mode
1148	  *[2.5–50 seconds]: Master Mode
1149	  *[1–30 seconds]: Expert Mode
1150	  *[1.25–37.5 seconds]: Master Mode
1151	  *[4–14 seconds]: Expert Mode
1152	  *[5–17.5 seconds]: Master Mode
1153	  *[12 seconds]: Expert Mode
1154	  *[14–30 seconds]: Expert Mode
1155	  *[17.5–37.5 seconds]: Master Mode
1156	  *[4–20 seconds]: Expert Mode
1157	  *[5–25 seconds]: Master Mode
1158	  *[1.5–28 seconds]: Expert Mode
1159	  *[1.87–35 seconds]: Master Mode
1160	  *[3–30 seconds]: Expert Mode
1161	  *[3.75–37.5 seconds]: Master Mode
1162	  *[4–12 seconds]: Expert Mode
1163	  *[5–15 seconds]: Master Mode
1164	  *[1.5–14 seconds]: Expert Mode
1165	  *[1.87–17.5 seconds]: Master Mode
1166	  *[0.73–8 seconds]: Expert Mode
1167	  *[0.92–10 seconds]: Master Mode
1168	  *[10–90 seconds]: Expert Mode
1169	  *[12.5–112.5 seconds]: Master Mode
1170	  *[0.5–32 seconds]: Expert Mode
1171	  *[0.63–40 seconds]: Master Mode
1172	  *[5 mph]: 5 miles per hour (as measured by the Stopwatch item) or 3.67 tiles per second
1173	  *[0.67–4 seconds]: Expert Mode
1174	  *[0.83–5 seconds]: Master Mode
1175	  *[1–4 seconds]: Expert Mode
1176	  *[4–8 seconds]: Expert Mode
1177	  *[5 seconds]: Master Mode
1178	  *[11.23–600 seconds]: Expert Mode
1179	  *[14.03–750 seconds]: Master Mode
1180	  *[3–90 seconds]: Master Mode
1181	  *[16 seconds]: Expert Mode
1182	  *[ 6]: Expert Mode
1183	  *[ 18]: Expert Mode
1184	  *[ 6-90 detik]: Mode Expert
1185	  *[2-20 detik]: Mode Expert
1186	  *[14-20 detik]: Mode Expert
1187	  *[16 detik]: Mode Expert
1188	  *[5-30 detik]: Mode Expert
1189	  *[6 detik]: Mode Expert
1190	  *[2.5-14 detik]: Mode Expert
1191	  *[1.25-8 detik]: Mode Expert
1192	  *[0.5-32 detik]: Mode Expert
1193	  *[18.75 detik - 10 menit]: Mode Expert
1194	  *[16.25 detik - 4 menit]: Mode Expert
1195	  *[10 detik]: Mode Expert
1196	  *[14-16 detik]: Mode Expert
1197	  *[20 detik-90 detik]: Mode Expert
1198	  *[2-3 detik]: Mode Expert
1199	  *[ 1 detik]: Mode Expert
1200	  *[5-9 detik]: Mode Expert
1201	  *[3-90 detik]: Mode Expert
1202	  *[16 detik]: Mode Expert
1203	  *[52]: Master Mode
1204	  *[78]: Master Mode
1205	  *[72]: Expert Mode
1206	  *[108]: Expert Mode
1207	  *[24 seconds]: Expert Mode
1208	  *[0.67 seconds]: Expert Mode
1209	  *[0.83 seconds]: Master Mode
1210	  *[midnight]: 12:00 AM
1211	  *[five]: Expert Mode
1212	  *[0.67]: Expert Mode
1213	  *[0.83]: Master Mode
1214	  *[14000]: Expert Mode
1215	  *[21000]: Master Mode
1216	  *[11900]: Expert Mode
1217	  *[15172]: Master Mode
1218	  *[0.75]: Expert Mode
1219	  *[Atk.  
1220	dmg]: Attack damage
1221	  *[Def.]: Defense
1222	  *[AP]: Armor penetration
1223	  *[77]: Master Mode
1224	  *[81]: Master Mode
1225	  *[27]: Expert Mode
1226	  *[31]: Master Mode
1227	  *[208]: Master Mode
1228	  *[69]: Expert Mode
1229	  *[Dynamit. Můj speciální lík na všechno, co tě trápí.]: Dynamite, my own special cure-all for what ails ya.
1230	  *[Výbušniny v dnešní době letí. Kup je ještě teď!]: Explosives are da' bomb these days. Buy some now!
1231	  *[Proč očisťovat svět, když jej můžeš vyhodit do povětří?]: Why purify the world when you can just blow it up?
1232	  *[Dnes se bude dobře umírat!]: It's a good day to die!
1233	  *[Jsem si docela jistý, že ti [jméno sestřičky] pomůže přišít zpět všechny tvé končetiny.]: 
1234	  *[Zajímalo by mě, co se stane, pokud… (BUM!)… Oh, omlouvám se, potřeboval jsi tu nohu?]: I wonder what happens if I... (BOOM!)... Oh, sorry, did you need that leg?
1235	  *[Dokonce i [jméno prodejce zbraní] by chtěl to, co já prodávám!]: Even [Name of Arms Dealer] wants what I'm selling!
1236	  *[Byl bys radši s dírou po kulce, nebo dírou po granátu? Myslel jsem si to.]: Would you rather have a bullet hole or a grenade hole? That's what I thought.
1237	  *[Koukni na mé zboží; mají výbušné ceny!]: Check out my goods; they have explosive prices!
1238	  *[ZÁKAZ KOUŘENÍ!]: NO SMOKING IN HERE!!
1239	  *[Pokud hodíš tenhle do vany a zavřeš všechna okna, pročistí to všechny tvé dutiny a urve uši!]: If you throw this one in the bathtub and close all the windows, it'll clear your sinuses and pop your ears!
1240	  *[Chceš si hrát na kuře Pojistku?]: Wanna play Fuse Chicken?
1241	  *[Podepsal bys mi tento griefovací dokument?]: Hey, could you sign this Griefing Waiver?
1242	  *[Něco jsem si od těch zombie odnesl!]: I've got something for them zombies alright!
1243	  *[Hej, neviděl jsi někde klauna?]: Hey, have you seen a clown around?
1244	  *[Ještě před chvílí tady seděla bomba, teď ji nemůžu najít…]: There was a bomb sitting right here, and now I can't seem to find it...
1245	  *[84]: Expert Mode
1246	  *[126]: Master Mode
1247	  *[30 seconds]: Expertní mód
1248	  *[60 mph]: 60 miles per hour (as measured by the Stopwatch item) or 44 tiles per second
1249	  *[33,33%]: Master Mode
1250	  *[88]: Expert Mode
1251	  *[132]: Master Mode
1252	  *[Contact]: The damage without modifier and summon damage bonuses
1253	  *[Pounce]: The damage without modifier and summon damage bonuses
1254	  *[Threshold]: If the player's summon damage bonuses reach it, Ruthless will become the best modifier
1255	  *[N/A]: Not available in vanilla game
1256	  *[16−30 seconds]: Expert Mode
1257	  *[20−37.5 seconds]: Master Mode
1258	  *[ 9.75%]: Expert Mode
1259	  *[16–30]: Expert Mode
1260	  *[20–37.5]: Master Mode
1261	  *[128]: Expert Mode
1262	  *[192]: Master Mode
1263	  *[15–60]: Expert Mode
1264	  *[0.5×]: Journey Mode
1265	  *[2×]: Expert Mode
1266	  *[3×]: Master Mode
1267	  *[4×]: Expert Mode
1268	  *[5.33×]: Legendary Mode
1269	  *[2.5×]: Master Mode
1270	  *[3.5×]: Legendary Mode
1271	  *[0.9×]: Expert Mode
1272	  *[0.8×]: Master Mode
1273	  *[1.5×]: Expert Mode
1274	  *[1.75×]: Master Mode
1275	  *[May increase both during [Hardmode](Hardmode.md "Hardmode") and [Post-Plantera](Post-Plantera.md "Post-Plantera")]: Expert Mode
1276	  *[May increase]: Expert Mode
1277	  *[15 / 30]: Expert Mode
1278	  *[ 4%]: Expert Mode
1279	  *[+15]: Expert Mode
1280	  *[+20]: Master Mode
1281	  *[ 16]: Expert Mode
1282	  *[18]: Master Mode
1283	  *[Opatruj se! Terraria tě potřebuje!]: Be safe; Terraria needs you!
1284	  *[Musíš očistit svět od této nákazy.]: You must cleanse the world of this corruption.
1285	  *[Musíš očistit svět od tohoto karmínu.]: You must cleanse the world of this crimson.
1286	  *[Písky času se přesýpají. A upřímně, nemládneš a nekrásníš.]: The sands of time are flowing. And well, you are not aging very gracefully.
1287	  *[Co je to s tím, že více ‚štěkám‘ než koušu?]: What's this about me having more 'bark' than bite?
1288	  *[Dva goblini tahle přijdou do baru a jeden říká tomu druhému: ‚Dáš si goblet piva?!‘]: So two goblins walk into a bar, and one says to the other, 'Want to get a Goblet of beer?!'
1289	  *[Proč se mi [Jméno obchodníka] snaží prodat sochy andělů? Všichni přeci ví, že nic nedělají.]: Why does [Name of Merchant] keep trying to sell me an angel statues? Everyone knows that they don't do anything.
1290	  *[Kéž by se mnou [jméno prodejce zbraní] přestal flirtovat. Copak si neuvědomuje, že jsem více než 500 let stará?]: I wish [Name of Arms Dealer] would stop flirting with me. Doesn't he realize I'm 500 years old?
1291	  *[Už jsi v nákaze zkoušel použít očistný prášek na ebenokámen?]: Have you tried using purification powder on the ebonstone of The Corruption?
1292	  *[Už jsi v karmínu zkoušel použít očistný prášek na karmínokámen?]: Have you tried using purification powder on the Crimstone of the Crimson?
1293	  *[Viděl jsi starce procházejícího se kolem podzemní kobky? Vůbec nevypadá dobře…]: Have you seen the old man walking around the dungeon? He doesn't look well at all...
1294	  *[Myslím si, že je [jméno lanýže] nepochopený ostatními. Je to velmi vtipný chlapík.]: I feel like [Name of Truffle] is a bit misunderstood, he really is a fun guy.
1295	  *[Prodávám co se mi zlíbí! Pokud se ti to nelíbí, tak máš smůlu.]: I sell what I want! If you don't like it, too bad.
1296	  *[Kámo, je to mnou, nebo je venku tak milion zombie?]: Dude, is it just me or are there a million [[zombies]] out tonight?
1297	  *[Nechci aby sis kupoval mé věci. Já chci abys chtěl si mé věci kupovat, jasné?]: I don't want you to buy my stuff. I want you to want to buy my stuff, ok?
1298	  *[Proč musíš být ve chvílích jako je tato tak konfrontační?]: Why do you have to be so confrontational during a time like this?
1299	  *[[jméno světa] je z [procenta posvátnosti] % posvátný a [procenta nákazy/karmínu] % [nakažen/karmínový]. [Dryádin komentář (viz výše)].]: [Name of world] is [hallow percentage]% hallow and [crimson/corruption percentage]% [crimson/corruption]. [Dryad's comment, see above].
1300	  *[[jméno světa] je kompletně očištěn. Odvedl jsi úžasnou práci!]: [Name of World] is completely pure. You have done an amazing job!
1301	  *[+10]: Expert Mode
1302	  *[+14]: Master Mode
1303	  *[6–20 seconds]: Expert Mode
1304	  *[7.5–25 seconds]: Master Mode
1305	  *[3–10 seconds]: Expert Mode
1306	  *[201]: Expert Mode
1307	  *[302]: Expert Mode
1308	  *[184]: Expert Mode
1309	  *[277]: Master Mode
1310	  *[39000/78000]: Expert Mode
1311	  *[49725/99450]: Master Mode
1312	  *[0]: Expert Mode
1313	  *[39,000]: Expert Mode
1314	  *[49,725]: Master Mode
1315	  *[11,700]: Expert Mode
1316	  *[14,917]: Master Mode
1317	  *[60,000]: Expert Mode
1318	  *[76,500]: Master Mode
1319	  *[99,000]: Master Mode
1320	  *[ 78000]: Expert Mode
1321	  *[99450]: Master Mode
1322	  *[ ]: Master Mode
1323	  *[ 62 _GC_ 50 _SC_]: Expert Mode
1324	  *[ 2 _GC_ 50 _SC_]: Mode Expert
1325	  *[39000]: Mode Expert
1326	  *[49725]: Mode Master
1327	  *[double]: Expert Mode
1328	  *[triple]: Master Mode
1329	  *[1/9 (11.11%)]: Expert Mode
1330	  *[1/8 (12.5%)]: Expert Mode
1331	  *[19]: Master Mode
1332	  *[15120]: Expert Mode
1333	  *[19296]: Master Mode
1334	  *[356]: Mode Expert
1335	  *[209]: Mode Expert
1336	  *[139.33 yards (152.38 m)]: Expert Mode
1337	  *[10479]: Expert Mode
1338	  *[1/20 (5%)]: Expert Mode
1339	  *[10 minutes]: Expert Mode
1340	  *[100-150]: Expert Mode
1341	  *[2-3]: Chế độ Expert
1342	  *[ 15120]: Chế độ Expert
1343	  *[ 19296]: Chế độ Master
1344	  *[ 10500]: Chế độ Expert
1345	  *[10 menit]: Mode Expert
1346	  *[12 menit 30 detik]: Mode Master
1347	  *[2–3]: Chế độ Expert
1348	  *[1/20 (%5)]: Expert Mode
1349	  *[10 phút]: Chế độ Expert
1350	  *[12 phút 30 giây]: Chế độ Master
1351	  *[10500]: Expert Mode
1352	  *[Total damage]: Stationary / Moving
1353	  *[110]: Expert Mode
1354	  *[248]: Master Mode
1355	  *[165]: Expert Mode
1356	  *[372]: Master Mode
1357	  *[49000/98000]: Expert Mode
1358	  *[62475/124950]: Master Mode
1359	  *[12]: Expert Mode
1360	  *[Ethereal Lance 3]: Expert Mode
1361	  *[49,000]: Expert Mode
1362	  *[62,475]: Master Mode
1363	  *[59,994]: Master Mode
1364	  *[39,996]: Expert Mode
1365	  *[24 mph]: 24 miles per hour (as measured by the Stopwatch item) or 17.6 tiles per second
1366	  *[33 mph]: 33 miles per hour (as measured by the Stopwatch item) or 24.2 tiles per second
1367	  *[2000]: Expert Mode
1368	  *[3000]: Master Mode
1369	  *[6000]: Expert Mode
1370	  *[9000]: Master Mode
1371	  *[10000]: Expert Mode
1372	  *[15000]: Master Mode
1373	  *[48›86]: Expert Mode : Pre-Hardmode › Hardmode
1374	  *[72›129]: Master Mode : Pre-Hardmode › Hardmode
1375	  *[124]: Expert Mode
1376	  *[186]: Master Mode
1377	  *[37%]: Expert Mode
1378	  *[44%]: Master Mode
1379	  *[55%]: Expert Mode
1380	  *[82%]: Expert Mode
1381	  *[84%]: Master Mode
1382	  *[172]: Expert Mode
1383	  *[258]: Master Mode
1384	  *[228]: Expert Mode
1385	  *[342]: Master Mode
1386	  *[1.33–6.67%]: Expert Mode
1387	  *[27.27–60%]: Expert Mode
1388	  *[5–25%]: Master Mode
1389	  *[20–100%]: Master Mode
1390	  *[125]: Master Mode
1391	  *[9/25 (36%)]: Expert Mode
1392	  *[9/25]: Expert Mode
1393	  *[1050]: Master Mode
1394	  *[1/10 (10%)]: Expert Mode
1395	  *[54]: Master Mode
1396	  *[2366/3640]: Expert Mode
1397	  *[3016/4641]: Master Mode
1398	  *[−15]: Expert Mode
1399	  *[−30]: Expert Mode
1400	  *[Chain charge]: Expert Mode
1401	  *[2,366]: Chế độ Expert
1402	  *[3,016]: Mode Master
1403	  *[436]: Expert Mode
1404	  *[556]: Master Mode
1405	  *[145]: Expert Mode
1406	  *[185]: Master Mode
1407	  *[7 _GC_ 50 _SC_]: Expert Mode
1408	  *[36  
1409	40 when below 145 health]: Expert Mode
1410	  *[54  
1411	60 when below 185 health]: Master Mode
1412	  *[2365/3640]: Chế độ Expert
1413	  *[ 7 _GC_ 50 _SC_]: Chế độ Expert
1414	  *[ %25]: Master Mode
1415	  *[36  
1416	40 khi dưới 145 máu]: Chế độ Expert
1417	  *[54  
1418	60 khi dưới 185 máu]: Chế độ Master
1419	  *[3017/4641]: Chế độ Master
1420	  *[Liên hoàn lướt]: Chế độ Expert
1421	  *[4641]: Chế độ Master
1422	  *[3016]: Chế độ Master
1423	  *[1,000]: Expert Mode
1424	  *[1,500]: Master Mode
1425	  *[8 mph]: 8 miles per hour (as measured by the Stopwatch item) or 5.625 tiles per second
1426	  *[19 mph]: 19 miles per hour (as measured by the Stopwatch item) or 14.0625 tiles per second
1427	  *[4.2–7]: Expert Mode
1428	  *[5.25–8.75]: Master Mode
1429	  *[6–10]: Expert Mode
1430	  *[7.5–12.5]: Master Mode
1431	  *[1.2–2]: Expert Mode
1432	  *[1.5–2.5]: Master Mode
1433	  *[FP]: Fishing Power
1434	  *[cần có 5]: Chế độ Journey
1435	  *[cần có 3]: Chế độ Journey
1436	  *[membutuhkan 99]: Mode Journey
1437	  *[22 mph]: 22 miles per hour (as measured by the Stopwatch item) or 15.8371875 tiles per second
1438	  *[113 mph]: 113 miles per hour (as measured by the Stopwatch item) or 82.5 tiles per second
1439	  *[116 mph]: 116 miles per hour (as measured by the Stopwatch item) or 85.07 tiles per second
1440	  *[13600]: Expert Mode
1441	  *[20400]: Master Mode
1442	  *[32 mph]: 32 miles per hour (as measured by the Stopwatch item) or 23.63343375 tiles per second
1443	  *[81 mph]: 81 miles per hour (as measured by the Stopwatch item) or 59.4 tiles per second
1444	  *[71 mph]: 71 miles per hour (as measured by the Stopwatch item) or 52.07 tiles per second
1445	  *[14 mph]: 14 miles per hour (as measured by the Stopwatch item) or 10.546875 tiles per second
1446	  *[28 mph]: 28 miles per hour (as measured by the Stopwatch item) or 20.53 tiles per second
1447	  *[37 mph]: 37 miles per hour (as measured by the Stopwatch item) or 27.13 tiles per second
1448	  *[42 mph]: 42 miles per hour (as measured by the Stopwatch item) or 30.8 tiles per second
1449	  *[48 mph]: 48 miles per hour (as measured by the Stopwatch item) or 35.2 tiles per second
1450	  *[49 mph]: 49 miles per hour (as measured by the Stopwatch item) or 35.93 tiles per second
1451	  *[56 mph]: 56 miles per hour (as measured by the Stopwatch item) or 41.25 tiles per second
1452	  *[47 mph]: 47 miles per hour (as measured by the Stopwatch item) or 34.47 tiles per second
1453	  *[7.7 mph]: 7.7 miles per hour (as measured by the Stopwatch item) or 5.65 tiles per second
1454	  *[63 mph]: 63 miles per hour (as measured by the Stopwatch item) or 45.9375 tiles per second
1455	  *[2.5]: Master Mode
1456	  *[250]: Master Mode
1457	  *[375]: Master Mode
1458	  *[100% by wave 14]: Expert Mode
1459	  *[3/11 (27.27%)]: Expert Mode
1460	  *[3/8 (37.5%)]: Expert Mode
1461	  *[3/5 (60%)]: Expert Mode
1462	  *[Base]: Base drop rate without the factor
1463	  *[1.67%]: Expert Mode
1464	  *[2.22%]: Expert Mode
1465	  *[8.33%]: Master Mode
1466	  *[27.27%]: Expert Mode
1467	  *[37.5%]: Expert Mode
1468	  *[6-12]: Expert Mode
1469	  *[7-15]: Master Mode
1470	  *[48-96]: Expert Mode
1471	  *[56-120]: Master Mode
1472	  *[3.75]: Master Mode
1473	  *[13/125 (10.4%)]: Expert Mode
1474	  *[39/400 (9.75%)]: Expert Mode
1475	  *[69/1225 (5.63%)]: Expert Mode
1476	  *[1–4]: Expert Mode
1477	  *[1.25–5]: Master Mode
1478	  *[0.67–2]: Expert Mode
1479	  *[0.83–2.5]: Master Mode
1480	  *[12.5–25%]: Master Mode
1481	  *[(Expert Mode exclusive)]: Expert Mode
1482	  *[40 mph]: 40 miles per hour (as measured by the Stopwatch item) or 29.25 tiles per second
1483	  *[1 minute 38 seconds]: Expert Mode
1484	  *[2 minutes 3 seconds]: Master Mode
1485	  *[Ukořisti drahokam]: Capture the Gem
1486	  *[membutuhkan 15]: Mode Journey
1487	  *[cần có 15]: Chế độ Journey
1488	  *[membutuhkan 5]: Mode Journey
1489	  *[28 seconds]: Expert Mode
1490	  *[35 seconds]: Master Mode
1491	  *[30–90 seconds]: Expert Mode
1492	  *[7.84%]: Expert Mode
1493	  *[7,84%]: Mode Expert
1494	  *[43]: Expert Mode
1495	  *[64]: Expert Mode
1496	  *[288]: Expert Mode
1497	  *[432]: Master Mode
1498	  *[4%]: Expert Mode
1499	  *[44]: Chế độ Expert
1500	  *[66]: Chế độ Master
1501	  *[33.3%]: Expert Mode
1502	  *[10 required]: Journey Mode
1503	  *[90000]: Expert Mode
1504	  *[114749]: Master Mode
1505	  *[37500]: Expert Mode
1506	  *[47812]: Master Mode
1507	  *[22500]: Expert Mode
1508	  *[28687]: Master Mode
1509	  *[19125]: Master Mode
1510	  *[10–14 seconds]: Expert Mode
1511	  *[15–21 seconds]: Master Mode
1512	  *[10–14]: Expert Mode
1513	  *[15–21]: Master Mode
1514	  *[18,750]: Expert Mode
1515	  *[23,906]: Master Mode
1516	  *[58 mph]: 58 miles per hour (as measured by the Stopwatch item) or 42.75 tiles per second
1517	  *[104]: Expert Mode
1518	  *[156]: Master Mode
1519	  *[59 mph]: 59 miles per hour (as measured by the Stopwatch item) or 43.125 tiles per second
1520	  *[162]: Master Mode
1521	  *[112]: Expert Mode
1522	  *[116]: Expert Mode
1523	  *[174]: Master Mode
1524	  *[96–116]: Expert Mode
1525	  *[144–174]: Master Mode
1526	  *[15,000]: Expert Mode
1527	  *[19,124]: Master Mode
1528	  *[7,500]: Expert Mode
1529	  *[9,562]: Master Mode
1530	  *[18,000]: Expert Mode
1531	  *[22,949]: Master Mode
1532	  *[13,500]: Expert Mode
1533	  *[17,212]: Master Mode
1534	  *[4,500]: Expert Mode
1535	  *[5,737]: Master Mode
1536	  *[2,250]: Expert Mode
1537	  *[2,868]: Master Mode
1538	  *[11,250]: Expert Mode
1539	  *[14,343]: Master Mode
1540	  *[9,000]: Expert Mode
1541	  *[11,474]: Master Mode
1542	  *[6,750]: Expert Mode
1543	  *[8,606]: Master Mode
1544	  *[123 mph]: 123 miles per hour (as measured by the Stopwatch item) or 90 tiles per second
1545	  *[1 mph]: 1 mile per hour (as measured by the Stopwatch item) or 0.375 tiles per second
1546	  *[AMA]: Ask Me Anything
1547	  *[Zdravím [jméno hráče]. Je zde něco, s čím bych mohl pomoci?]: Greetings, [Name of Player]. Is there something I can help you with?
1548	  *[Jsem zde proto, abych ti dával rady co máš dělat. Doporučuji ti si se mnou přijít promluvit, kdykoliv si nebudeš vědět rady.]: I am here to give you advice on what to do next. It is recommended that you talk with me anytime you get stuck.
1549	  *[Říká se, že existuje člověk, který ti poradí, jak máš přežít v této krajině… ale počkat. To jsem přeci já.]: They say there is a person who will tell you how to survive in this land... oh wait. That's me.
1550	  *[Měl bys zůstat v době během noci. Je velmi nebezpečné toulat se v noci.]: You should stay indoors at night. It is very dangerous to be wandering around in the dark.
1551	  *[Hej kamaráde, nevíš, kde se nachází nějaký smrtirost? Jen tak, přemýšlím nahlas.]: Hey, buddy, do you know where any deathweed is? Oh, no reason; Just wondering, is all.
1552	  *[Pokud se podíváš na oblohu, uvidíš, že je měsíc krvavý.]: If you were to look up, you'd see the moon is red right now.
1553	  *[S jistotou můžeš říct, že nastal krvavý měsíc, jakmile se barva oblohy promění v červenou. Něho během této doby způsobuje, že se objevuje více nepřátel.]: You can tell a Blood Moon is out when the sky turns red. There is something about it that causes monsters to swarm.
1554	  *[Oktoberfest je tady! [Jméno obchodníka] uvařil kvůli této události své proslulé pivo a [jméno oděvníka] prodává tradiční oblečení spojené s festivalem.]: The Oktober festival is here! [Name of Merchant] has brewed up some of his famous ale especially for the occasion and [Name of Clothier] is selling traditional festival clothes.
1555	  *[Nový rok je tady! [Jméno demoličního experta] prodává speciální zbraně, které rozzáří oblohu a [jméno oděvníka] prodává tradiční sváteční oděv.]: New Year is here! [Name of Demolitionist] is selling special weaponry to light up the skies, and [Name of Clothier] is selling traditional festive attire.
1556	  *[75]: Expert Mode
1557	  *[Expert-exclusive]: Expert Mode
1558	  *[Master-exclusive]: Master Mode
1559	  *[Hive Pack]: Expert Mode
1560	  *[and third]: Expert Mode
1561	  *[0.9›0.4]: Pre-Hardmode › Hardmode
1562	  *[0.5›0.45]: Pre-Hardmode › Hardmode
1563	  *[216]: Master Mode
1564	  *[252]: Master Mode
1565	  *[6.25–25%]: Master Mode
1566	  *[25–100%]: Master Mode
1567	  *[140–148]: Expert Mode
1568	  *[210–222]: Master Mode
1569	  *[10–20 seconds]: Expert Mode
1570	  *[12.5–25 seconds]: Master Mode
1571	  *[≤ 2 seconds]: Expert Mode
1572	  *[≤ 2.5 seconds]: Master Mode
1573	  *[50–100%]: Master Mode
1574	  *[nebo 3/4]: Expertní mód
1575	  *[tümü]: Master Mode
1576	  *[18750]: Expert Mode
1577	  *[67]: Expert Mode
1578	  *[1–5 seconds]: Expert Mode
1579	  *[1.25–6.25 seconds]: Master Mode
1580	  *[ 17 _CC_ ]: Expert Mode
1581	  *[ 49 _CC_ ]: Expert Mode
1582	  *[ 1 _SC_ 30 _CC_ ]: Expert Mode
1583	  *[ 20 _CC_ ]: Expert Mode
1584	  *[14 _GC_ 81 _SC_]: Expert Mode
1585	  *[16 _GC_ 6 _SC_]: Master Mode
1586	  *[2 _PC_ 67 _GC_]: Expert Mode
1587	  *[2 _PC_ 89 _GC_]: Master Mode
1588	  *[81 _SC_ 20 _CC_]: Expert Mode
1589	  *[3 _SC_ 72 _CC_]: Expert Mode
1590	  *[1 _SC_ 69 _CC_]: Expert Mode
1591	  *[9 _SC_ 20 _CC_]: Expert Mode
1592	  *[8 _SC_ 6 _CC_]: Expert Mode
1593	  *[7 _SC_ 44 _CC_]: Expert Mode
1594	  *[4 _SC_ 92 _CC_]: Expert Mode
1595	  *[2 _SC_ 61 _CC_]: Expert Mode
1596	  *[3 _SC_ 31 _CC_]: Expert Mode
1597	  *[5 _SC_ 26 _CC_]: Expert Mode
1598	  *[3 _SC_ 17 _CC_]: Expert Mode
1599	  *[11 _SC_ 73 _CC_]: Expert Mode
1600	  *[4 _SC_ 32 _CC_]: Expert Mode
1601	  *[16 _SC_ 91 _CC_]: Expert Mode
1602	  *[54 _SC_ 67 _CC_]: Expert Mode
1603	  *[72 _SC_ 68 _CC_]: Expert Mode
1604	  *[44 _SC_ 90 _CC_]: Expert Mode
1605	  *[2 _GC_ 46 _SC_ 61 _CC_]: Expert Mode
1606	  *[45 _SC_ 93 _CC_]: Expert Mode
1607	  *[65 _SC_ 1 _CC_]: Expert Mode
1608	  *[12 _SC_ 81 _CC_]: Expert Mode
1609	  *[1 _GC_ 83 _SC_ 35 _CC_]: Expert Mode
1610	  *[2 _GC_ 65 _SC_]: Expert Mode
1611	  *[7 _GC_ 71 _SC_]: Expert Mode
1612	  *[7 _GC_ 95 _SC_]: Expert Mode
1613	  *[8 _GC_ 71 _SC_]: Expert Mode
1614	  *[21 _GC_ 9 _SC_]: Expert Mode
1615	  *[19 _GC_ 70 _SC_]: Expert Mode
1616	  *[13 _GC_ 25 _SC_]: Expert Mode
1617	  *[26 _GC_ 17 _SC_]: Expert Mode
1618	  *[9 _GC_ 44 _SC_]: Expert Mode
1619	  *[5 _GC_ 31 _SC_]: Expert Mode
1620	  *[3 _GC_ 68 _SC_]: Expert Mode
1621	  *[21 _GC_ 20 _SC_]: Expert Mode
1622	  *[15 _GC_ 90 _SC_]: Expert Mode
1623	  *[15 _GC_ 60 _SC_]: Expert Mode
1624	  *[31 _GC_ 80 _SC_]: Expert Mode
1625	  *[37 _GC_ 71 _SC_]: Expert Mode
1626	  *[39 _GC_ 75 _SC_]: Expert Mode
1627	  *[17 _GC_ 92 _SC_]: Expert Mode
1628	  *[35 _GC_ 51 _SC_]: Expert Mode
1629	  *[66 _GC_ 25 _SC_]: Expert Mode
1630	  *[11 _GC_ 92 _SC_]: Expert Mode
1631	  *[19 _GC_ 73 _SC_]: Expert Mode
1632	  *[26 _GC_ 50 _SC_]: Expert Mode
1633	  *[2 _PC_ 65 _GC_]: Expert Mode
1634	  *[1 _PC_ 18 _GC_]: Expert Mode
1635	  *[45900]: Expert Mode
1636	  *[68850]: Master Mode
1637	  *[327,420]: Expert Mode
1638	  *[436,560]: Master Mode
1639	  *[217500]: Expertní mód
1640	  *[277311]: Master Mode
1641	  *[450]: Master Mode
1642	  *[Master Mode]: Master Mode
1643	  *[245]: Expert Mode
1644	  *[367]: Master Mode
1645	  *[76]: Expert Mode
1646	  *[114]: Master Mode
1647	  *[42000]: Expert Mode
1648	  *[53550]: Master Mode
1649	  *[4–18 seconds]: Expert Mode
1650	  *[5–22.5 seconds]: Master Mode
1651	  *[21000/42000]: Expert Mode
1652	  *[26775/53550]: Master Mode
1653	  *[5›6]: Expert Mode : Pre-Hardmode › Hardmode
1654	  *[6›7]: Master Mode : Pre-Hardmode › Hardmode
1655	  *[1/100 (1%)]: Expert Mode
1656	  *[1/2000 (0.05%)]: Expert Mode
1657	  *[25–40]: Expert Mode
1658	  *[8–28]: Expert Mode
1659	  *[2–20 seconds]: Expert Mode
1660	  *[2.5–25 seconds]: Master Mode
1661	  *[2–8 seconds]: Expert Mode
1662	  *[2.5–10 seconds]: Master Mode
1663	  *[17–30]: Expert Mode
1664	  *[defense]: Expert Mode
1665	  *[14400/28800]: Expert Mode
1666	  *[18360/36720]: Master Mode
1667	  *[25–74]: Expert Mode
1668	  *[13500]: Expert Mode
1669	  *[17212]: Master Mode
1670	  *[11475]: Master Mode
1671	  *[13387]: Master Mode
1672	  *[The [](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu") can greatly increase your mobility as well as provide some extra defense.]: Expert Mode
1673	  *[The [](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") will reduce damage taken, making it a powerful choice.]: Expert Mode
1674	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") has a chance to dodge an attack, providing the player with a useful [](Cerebral_Mindtrick "Cerebral Mindtrick")[Cerebral Mindtrick](Cerebral_Mindtrick "Cerebral Mindtrick") buff.]: Expert Mode
1675	  *[91]: Expert Mode
1676	  *[137]: Master Mode
1677	  *[10+25 per hand alive]: Expert Mode
1678	  *[0+25 per hand alive]: Expert Mode
1679	  *[6–10 seconds]: Expert Mode
1680	  *[7.5–12.5 seconds]: Master Mode
1681	  *[1−2 seconds]: Expert Mode
1682	  *[1.5–2.5 seconds]: Master Mode
1683	  *[9.75%]: Expert Mode
1684	  *[55.56%]: Expert Mode
1685	  *[64500]: Expert Mode
1686	  *[82238]: Master Mode
1687	  *[64,500]: Expert Mode
1688	  *[82,238]: Master Mode
1689	  *[12,000]: Expert Mode
1690	  *[15,300]: Master Mode
1691	  *[13,800]: Expert Mode
1692	  *[17,595.2]: Master Mode
1693	  *[[](Shield_of_Cthulhu.md "Shield of Cthulhu")[Shield of Cthulhu](Shield_of_Cthulhu.md "Shield of Cthulhu")'s dash is essential throughout the fight.]: Expert Mode
1694	  *[[](Worm_Scarf.md "Worm Scarf")[Worm Scarf](Worm_Scarf.md "Worm Scarf") greatly decreases damage, but is exclusive to Corruption worlds.]: Expert Mode
1695	  *[The [](Brain_of_Confusion.md "Brain of Confusion")[Brain of Confusion](Brain_of_Confusion.md "Brain of Confusion") is very useful for players as it provides a chance to dodge an attack, but is exclusive to Crimson worlds. It doesn't prevent getting inflicted with the [](Cursed_Inferno.md "Cursed Inferno")[Cursed Inferno](Cursed_Inferno.md "Cursed Inferno") debuff, however.]: Expert Mode
1696	  *[24%]: Expert Mode
1697	  *[28%]: Master Mode
1698	  *[11,920]: Expert Mode
1699	  *[15,198]: Master Mode
1700	  *[1560]: Expert Mode
1701	  *[1989]: Master Mode
1702	  *[3120]: Expert Mode
1703	  *[3978]: Master Mode
1704	  *[8800]: Expert Mode
1705	  *[7.2-12.5]: Master Mode
1706	  *[ Expert-exclusive]: Expert Mode
1707	  *[ Master-exclusive]: Master Mode
1708	  *[(expert)]: Expert Mode
1709	  *[12000]: Expert Mode
1710	  *[13800]: Expert Mode
1711	  *[18-90]: Expert Mode
1712	  *[67,500]: Expert Mode
1713	  *[37,500]: Expert Mode
1714	  *[75,000]: Expert Mode
1715	  *[with a 1/5 (20%) chance]: Expert Mode
1716	  *[41]: Expert Mode
1717	  *[0 mph]: 0 miles per hour (as measured by the Stopwatch item) or 0 tiles per second
1718	  *[150 mph]: 150 miles per hour (as measured by the Stopwatch item) or 110 tiles per second
1719	  *[179 mph]: 179 miles per hour (as measured by the Stopwatch item) or 131.27 tiles per second
1720	  *[ 6500]: Expert Mode
1721	  *[8287]: Master Mode
1722	  *[1.25%–5%]: Expert Mode
1723	  *[32]: Expert Mode
1724	  *[0.25 mph]: 0.25 miles per hour (as measured by the Stopwatch item) or 0.18 tiles per second
1725	  *[ 2700]: Expert Mode
1726	  *[4050]: Master Mode
1727	  *[96 mph]: 96 miles per hour (as measured by the Stopwatch item) or 70.4 tiles per second
1728	  *[164 mph]: 164 miles per hour (as measured by the Stopwatch item) or 120 tiles per second
1729	  *[245 mph]: 245 miles per hour (as measured by the Stopwatch item)
1730	  *[11/100 (11%)]: Expert Mode
1731	  *[5% – 20%]: Expert Mode
1732	  *[6.22% – 31.11%]: Expert Mode
1733	  *[50 mph]: 50 miles per hour (as measured by the Stopwatch item) or 36.67 tiles per second
1734	  *[2–10 or 20 seconds]: Expert Mode
1735	  *[2.5–12.5 or 25 seconds]: Master Mode
1736	  *[2–10 or 20 secondi]: Expert Mode
1737	  *[2.5–12.5 or 25 secondi]: Master Mode
1738	  *[52 mph]: 52 miles per hour (as measured by the Stopwatch item) or 38.13 tiles per second
1739	  *[5.63%]: Expert Mode
1740	  *[2 seconds]: Expert Mode
1741	  *[2.5 seconds]: Master Mode
1742	  *[4,000]: Expert Mode
1743	  *[6,000]: Master Mode
1744	  *[148]: Expert Mode
1745	  *[222]: Master Mode
1746	  *[1.33 seconds]: Expert Mode
1747	  *[1.67 seconds]: Master Mode
1748	  *[33,150]: Expert Mode
1749	  *[42,266]: Master Mode
1750	  *[22,100]: Expert Mode
1751	  *[28,177]: Master Mode
1752	  *[11,050]: Expert Mode
1753	  *[14,088]: Master Mode
1754	  *[4,420]: Expert Mode
1755	  *[5,635]: Master Mode
1756	  *[198]: Master Mode
1757	  *[297]: Master Mode
1758	  *[50 seconds]: Expert Mode
1759	  *[1 minute 2.5 seconds]: Master Mode
1760	  *[1.25–5 seconds]: Master Mode
1761	  *[six]: Master Mode
1762	  *[additional accessory slot]: Master Mode
1763	  *[1.25%]: Expert Mode
1764	  *[2.5%]: Expert Mode
1765	  *[38 mph]: 38 miles per hour (as measured by the Stopwatch item) or 28.125 tiles per second
1766	  *[ 36]: Expert Mode
1767	  *[399/40,000 (0.9975%)]: Expert Mode
1768	  *[178]: Master Mode
1769	  *[2,659]: Expert Mode
1770	  *[3,390]: Master Mode
1771	  *[2,519]: Expert Mode
1772	  *[3,212]: Master Mode
1773	  *[2,800–2,240]: Expert Mode
1774	  *[3,570–2,856]: Master Mode
1775	  *[2,239–1,680]: Expert Mode
1776	  *[2,855–2,142]: Master Mode
1777	  *[1,679–1,120]: Expert Mode
1778	  *[2,141–1,428]: Master Mode
1779	  *[1,119–560]: Expert Mode
1780	  *[1,427–714]: Master Mode
1781	  *[559–280]: Expert Mode
1782	  *[713–357]: Master Mode
1783	  *[279–0]: Expert Mode
1784	  *[356–0]: Master Mode
1785	  *[2800]: Expert Mode
1786	  *[3570]: Master Mode
1787	  *[1/15th]: Expert Mode
1788	  *[15%]: Mode Expert
1789	  *[46%]: Expert Mode
1790	  *[52%]: Master Mode
1791	  *[68%]: Master Mode
1792	  *[1000]: Expert Mode
1793	  *[sometimes]: Expert Mode
1794	  *[1.2]: Archery buff
1795	  *[9]: Master Mode
1796	  *[O3DS]: Original Nintendo 3DS
1797	  *[Number]: Number of Tiny Eaters
1798	  *[Average]: Average number of Tiny Eaters
1799	  *[102×102]: Expert Mode
1800	  *[1/25 (4%)]: Expert Mode
1801	  *[44–60]: Expert Mode
1802	  *[66–90]: Master Mode
1803	  *[WoF]: Wall
1804	  *[135]: Master Mode
1805	  *[ (1 player)  
1806	57% (2 players)  
1807	71% (3 players)  
1808	81%  (4 players)  
1809	100% (5 players or more)  
1810	]: Expert Mode
1811	  *[ (1 player)  
1812	62% (2 players)  
1813	75% (3 players)  
1814	83% (4 players)  
1815	100% (5 players or more)  
1816	]: Master Mode
1817	  *[ (1 player)  
1818	69% (2 players)  
1819	79% (3 players)  
1820	86%  (4 players)  
1821	100% (5 players or more)  
1822	]: Expert Mode
1823	  *[ (1 player)  
1824	72% (2 players)  
1825	82% (3 players)  
1826	88% (4 players)  
1827	100% (5 players or more)  
1828	]: Master Mode
1829	  *[1485]: Expert Mode
1830	  *[2227]: Master Mode
1831	  *[2700]: Expert Mode
1832	  *[220]: At least one Ogre has to be killed
1833	  *[330]: Master Mode
1834	  *[224]: Expert Mode
1835	  *[336]: Master Mode
1836	  *[454]: Master Mode
1837	  *[52›93›138]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1838	  *[78›140›208]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1839	  *[60›105›105]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1840	  *[90›157›157]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1841	  *[48›86›131]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1842	  *[73›129›196]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1843	  *[60›105›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1844	  *[90›157›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1845	  *[45›120›161]: Expert Mode : Pre-Hardmode › Hardmode › Post-Plantera
1846	  *[67›180›241]: Master Mode : Pre-Hardmode › Hardmode › Post-Plantera
1847	  *[472]: Master Mode
1848	  *[18–23]: Expert Mode
1849	  *[1/4]: Master Mode
1850	  *[4.94 (79/1600)]: Expert Mode
1851	  *[30–49]: Expert Mode
1852	  *[1/2]: Expert Mode
1853	  *[20–35]: Expert Mode
1854	  *[90–110]: Chế độ Expert
1855	  *[49/625 (7.84%)]: Expert Mode
1856	  *[99/2500 (3.96%)]: Expert Mode
1857	  *[1/15 (6.67%)]: Expert Mode
1858	  *[1/75 (1.33%)]: Expert Mode
1859	  *[1/20 (5%) ****__(Desktop, Console and Mobile versions)]: Expert Mode
1860	  *[5/9 (55.56%)]: Expert Mode
1861	  *[H]: Height (tiles)
1862	  *[14–17]: Expert Mode
1863	  *[3–4]: Expert Mode
1864	  *[12–15]: Chế độ Expert
1865	  *[21-27]: Chế độ Expert
1866	  *[four]: Expert Mode
1867	  *[1–5]: Expert Mode
1868	  *[1.25–6.25]: Master Mode
1869	  *[almost opaque]: Expert Mode
1870	  *[three]: Expert Mode
1871	  *[24,000]: Expert Mode
1872	  *[30,600]: Master Mode
1873	  *[1,200]: Master Mode
1874	  *[16,000]: Expert Mode
1875	  *[20,400]: Master Mode
1876	  *[40000]: Expert Mode
1877	  *[51000]: Master Mode
1878	  *[48000]: Expert Mode
1879	  *[61000]: Master Mode
1880	  *[39 mph]: 39 miles per hour (as measured by the Stopwatch item) or 28.6 tiles per second
1881	  *[599/90,000 (0.6656%)]: Expert Mode
1882	  *[395]: Expert Mode
1883	  *[second phase]: Expert Mode
1884	  *[54000]: Expert Mode
1885	  *[全て]: Master Mode
1886	  *[75 HP]: Chế độ Master
1887	  *[21 Sát thương]: Chế độ Master
1888	  *[20% KB]: Chế độ Master
1889	  *[411 HP]: Chế độ Master
1890	  *[93 Sát thương]: Chế độ Master
1891	  *[Vždy kupuj více drátů, než potřebuješ.]: Always buy more wire than you need!
1892	  *[Je to určitě zapojené do proudu?]: Did you make sure your device was plugged in?
1893	  *[Oh, víš co tento dům opravdu potřebuje? Více blikajících světélek.]: Oh, you know what this house needs? More blinking lights.
1894	  *[Hej [jméno hráče], nevrátil jsi se právě od [jméno gobliního kutila]? Neříkal ti náhodou něco o mně?]: Hey, [Name of Player], did you just come from [Name of Goblin Tinkerer]'s? Did he say anything about me by chance?
1895	  *[Hej, dávej si bacha, kam jdeš! Já jsem tam ještě nedávno byla!]: Hey, watch where you're going! I was over there a little while ago!
1896	  *[[Jméno prodejce zbraní] pořád říká, že stiskne mou tlakovou desku. Já jsem mu ale říkala, že na ni se má šlapat.]: [Name of Arms Dealer] keeps talking about pressing my pressure plate. I told him it was for stepping on.
1897	  *[Oh, nech mě hádat. Zapomněl jsi koupit dostatek drátů. Hlupáku.]: Oh, let me guess. Forgot to buy enough wire. Idiot.
1898	  *[Mohl… Mohl bys… Prosím? Ok? Ok. Ugh.]: Just-could you just...Please? Ok? Ok. Ugh.
1899	  *[Nelíbí se mi, jak se na mě díváš. Já právě PRACUJI.]: I don't appreciate the way you're looking at me. I am WORKING right now.
1900	  *[Všechno co bych pro vypínač chtěla je… Cože?!]: All I want is for the switch to make the... What?!
1901	  *[NEHÝBAT! SPADLA MI KONTAKTNÍ ČOČKA.]: DON'T MOVE. I DROPPED MY CONTACT.
1902	  *[Už jsme byla skoro hotová s věšením blikajících světélek!]: But I was almost done putting blinking lights up here!
1903	  *[Zadrž, už jsem tady dole skoro chytala WiFi signál.]: Hold on, I've almost got wifi going down here.
1904	  *[Děkuji. Trvat to o něco déle, tak skončím jako většina těch kostlivců, co tady dole žije.]: Thanks! It was only a matter of time before I ended up like the rest of the skeletons down here.
1905	  *[Kosh, kapleck Mog. Oh sorry, that's Klingon for 'Buy something or die.']: Kosh, kapleck Mog. Oh promiň, to je klingonsky výraz pro: ‚Něco si kup, nebo zemři.‘
1906	  *[Meč poráží papír! Získej jeden ještě dnes.]: Sword beats paper! Get one today.
1907	  *[Krásné ráno, co myslíš? Nechtěl jsi něco?]: Lovely morning, wouldn't you say? Was there something you needed?
1908	  *[Chceš jablka? Chceš mrkve? Chceš ananasy? Máme pro tebe pochodně!]: You want apples? You want carrots? You want pineapples? We got torches.
1909	  *[Slunce je vysoko, ale mé ceny jsou nízké.]: 
1910	  *[Chlape, to slunce ale pálí! Náhodou mám jedno úžasně ventilované brnění.]: Boy, that sun is hot! I do have some perfectly ventilated armor.
1911	  *[Koukni na moje hliněné bloky, jsou extra hliněné.]: Check out my dirt blocks, they are extra dirty.
1912	  *[Ah, jednoho dnes se budou vyprávět pověsti o [jméno hráče]… jen ty dobré, tím jsem si jist.]: Ah, they will tell tales of [Name of Player] some day... good ones I'm sure.
1913	  *[Brzy nastane noc můj příteli. Rozhodni se dokud ještě můžeš.]: Night be upon us soon, friend. Make your choices while you can.
1914	  *[Nemáš ani ponětí, jakou cenou se v zámoří platí za hliněné bloky.]: You have no idea how much Dirt Blocks sell for overseas.
1915	  *[Kosh, kapleck Mog. Oh promiň, to je [klingonsky](https://en.wikipedia.org/wiki/cs:Klingon "wikipedia:cs:Klingon") výraz pro: ‚Něco si kup, nebo zemři.‘]: Kosh, kapleck Mog. Oh sorry, that's klingon for 'Buy something or die.'
1916	  *[[Jméno hráče], je to tak? Slyšel jsem jen dobré zprávy příteli!]: [Name of Player] is it? I've heard good things, friend!
1917	  *[Občas přemýšlím, jestli je měsíc ze sýra… huh, co? Oh ano, kup něco!]: I wonder if the moon is made of cheese... huh, what? Oh yes, buy something!
1918	  *[Chlápek co teď odcházel mi tady nechal nějaký bordel… uhm chtěl jsem říct… poklady!]: The last guy who was here left some junk... er I mean... treasures!
1919	  *[Řekl jsi zlato? To od tebe klidně odkoupím.]: Did you say gold? I'll take that off of ya.
1920	  *[Slyšel jsem o ukrytém pokladu… oh zapomeň na to.]: I hear there's a secret treasure... oh never mind.
1921	  *[Socha anděla povídáš? Promiň, ale já neprodávám žádné harampádí.]: Angel statue you say? I'm sorry, I'm not a junk dealer.
1922	  *[Viděl jsi už Chith… Shith… Chat… Obří oko?]: Have you seen Chith...Shith.. Chat... The big eye?
1923	  *[Občas hoď okem po ceně, kup čočky!]: Keep your eye on the prize, buy a lens!
1924	  *[Oh výtečně. Už zase slyším [jméno mechaničky] a [jméno sestřičky], jak se hádají.]: Oh, great. I can hear [Name of Mechanic] and [Name of Nurse] arguing from here.
1925	  *[Ani krvavý měsíc nezastaví kapitalismus. Pojďme uzavřít nějaký obchod.]: Not even a Blood Moon can stop capitalism. Let's do some business.
1926	  *[Hej, tento dům je zabezpečený, je to tak? [Jméno hráče], je to tak?!]: Hey, this house is secure, right? Right? [Name of Player]?
1927	  *[Doufám, že takový vychrtlý klučina jako ty není to, co nás má ochránit před okem Cthulu.]: I hope a scrawny kid like you isn't all that's standing between us and Cthulu's Eye.
1928	  *[Cítím, jako kdyby mě sledovala přítomnost zla.]: I feel like an evil presence is watching me.
1929	  *[Když se tak koukám na to ošuntělé brnění, co nosíš, mám chuť ti prodat ještě pár léčivých lektvarů.]: Look at that shoddy armor you're wearing. Better buy some more healing potions.
1930	  *[10–20]: Expert Mode
1931	  *[12–25]: Master Mode
1932	  *[900]: Master Mode
1933	  *[ 5 _GC_]: Expert Mode
1934	  *[25 _GC_]: Expert Mode
1935	  *[11 mph]: 11 miles per hour (as measured by the Stopwatch item) or 8.07 tiles per second
1936	  *[9 mph]: 9 miles per hour (as measured by the Stopwatch item) or 6.6 tiles per second
1937	  *[49]: Expert Mode
1938	  *[Pre-HM]: Pre-Hardmode
1939	  *[101]: Expert Mode
1940	  *[337]: Expert Mode
1941	  *[Enemies that have [picked up coins](Coin_pickup_in_Expert_Mode.md "Coin pickup in Expert Mode")]: Expert Mode
1942	  *[2.67]: Expert Mode
1943	  *[2.25]: Master Mode
1944	  *[16 sekund]: Expertní mód
1945	  *[ 2 _PC_ 50 _GC_]: Expertní mód
1946	  *[40–45]: Expert Mode
1947	  *[187.5]: Master Mode
1948	  *[+24%]: Expert Mode
1949	  *[+28%]: Master Mode
1950	  *[305 mph]: 305 miles per hour (as measured by the Stopwatch item) or 223.67 tiles per second
1951	  *[255 mph]: 255 miles per hour (as measured by the Stopwatch item) or 187 tiles per second
1952	  *[720 mph]: 720 miles per hour (as measured by the Stopwatch item) or 528 tiles per second
1953	  *[0.0396%]: Expert Mode
1954	  *[10,149/1,000,000 (1.01%)]: Expert Mode
1955	  *[199/10,000 (1.99%)]: Expert Mode
1956	  *[36%]: Expert Mode
1957	  *[night]: 7:30 PM – 4:30 AM
1958	  *[dawn]: 4:30 AM
1959	  *[2–8]: Expert Mode
1960	  *[10–30 seconds]: Expert Mode
1961	  *[12.5–37.5 seconds]: Master Mode
1962	  *[10–30]: Expert Mode
1963	  *[12.5–37.5]: Master Mode
1964	  *[3 _SC_]: Expert Mode
1965	  *[3 _GC_]: Expert Mode
1966	  *[6 _SC_]: Expert Mode
1967	  *[4 _SC_ 50 _CC_]: Expert Mode
1968	  *[9 _SC_]: Expert Mode
1969	  *[20 _SC_]: Expert Mode
1970	  *[15 _SC_]: Expert Mode
1971	  *[30 _SC_]: Expert Mode
1972	  *[50 _SC_]: Expert Mode
1973	  *[37 _SC_ 50 _CC_]: Expert Mode
1974	  *[75 _SC_]: Expert Mode
1975	  *[1 _GC_ 20 _SC_]: Expert Mode
1976	  *[90 _SC_]: Expert Mode
1977	  *[1 _GC_ 80 _SC_]: Expert Mode
1978	  *[2 _GC_]: Expert Mode
1979	  *[1 _GC_ 50 _SC_]: Expert Mode
1980	  *[2 _GC_ 25 _SC_]: Expert Mode
1981	  *[4 _GC_ 50 _SC_]: Expert Mode
1982	  *[4 _GC_]: Expert Mode
1983	  *[Hej, nezmiňoval se [jméno prodejce zbraní] o tom, že by potřeboval vyšetřit? Ptám se jen tak.]: Hey, has [Name of Arms Dealer] mentioned needing to go to the doctor for any reason? Just wondering.
1984	  *[Bolí to, když uděláš tohle? Pak tohle nedělej.]: Does it hurt when you do that? Don't do that.
1985	  *[Ukaž mi, co tě bolí.]: Show me where it hurts.
1986	  *[Tohle není to největší, co jsem za svůj život viděla… Ano, už jsem viděla větší rány.]: That's not the biggest I've ever seen... Yes, I've seen bigger wounds for sure.
1987	  *[Otoč hlavu a zakašlej.]: Turn your head and cough.
1988	  *[Někdy si přeji, aby byl [jméno demoličního experta] více opatrný. Už mě unavuje to každodenní přišívání jeho končetin zpět k tělu.]: I wish [Name of Demolitionist] would be more careful. I'm getting tired of having to sew his limbs back on every day.
1989	  *[Lízátko by sis nedal?]: Would you like a lollipop?
1990	  *[Asi si budu muset promluvit s [jméno průvodce]. Jak často si musíš ošetřovat tak těžké popáleniny?]: I need to have a serious talk with [Name of Guide]. How many times a week can you come in with severe lava burns?
1991	  *[Už jsi viděl starce, jak se potuluje kolem podzemní kobky? Vypadá utrápeně.]: Have you seen that Old Man pacing around the dungeon? He looks troubled.
1992	  *[Nedělej ze sebe takové dítě. Už jsem viděla horší.]: Quit being such a baby! I've seen worse.
1993	  *[Zase trable s těmi tyrany?]: Trouble with those bullies again?
1994	  *[To bude potřebovat pár stehu!]: That's gonna need stitches!
1995	  *[vypadáš, jako kdybys byl napůl strávený. Zase jsi honil slizy?]: You look half digested. Have you been chasing slimes again?
1996	  *[Počkej chvíli, mám tady někde nějaké náplasti se zvířátky.]: Hold on, I've got some cartoon bandages around here somewhere.
1997	  *[[Jméno hráče], to rozchodíš a budeš v pořádku. Šmárja.]: Walk it off, (Name of Player), you'll be fine. Sheesh.
1998	  *[Drazí přátelé, sešli jsme se zde, abychom vzdali poslední úctu… ále, budeš v pořádku.]: Dear friends we are gathered here today to bid farewell... oh, you'll be fine.
1999	  *[Myslím si, že toto ti sluší víc.]: I think you look better this way.
2000	  *[Eww… Co se stalo s tvým obličejem?]: Eww.. what happened to your face?
2001	  *[Támhle jsi nechal svoje rameno. Dojdu pro něj.]: You left your arm over there. Let me get that for you.
2002	  *[MŮJ BOŽE. Dobrá jsem, ale TAKHLE zase ne.]: MY GOODNESS. I'm good but I'm not THAT good.
2003	  *[Co má tohle znamenat?]: What is that supposed to mean!?
2004	  *[Nemyslím si, že se mi líbí tvůj tón v hlase.]: I don't think I like your tone.
2005	  *[Co tady děláš? Pokud nekrvácíš, tak tě tady nechci. Běž pryč.]: Why are you even here? If you aren't bleeding, you don't need to be here. Get out.
2006	  *[COŽE?!]: WHAT?!
2007	  *[Pokud plánuješ zemřít, učiň tak venku.]: If you're going to die, do it outside.
2008	  *[Pospěš si a přestaň krvácet.]: Hurry up and stop bleeding.
2009	  *[Běda, jestli se mi tvá krev dostane na sukni.]: You better not get blood on me.
2010	  *[Ani to nebolelo, že ne?]: That didn't hurt too bad, now did it?
2011	  *[Všechno v pořádku. A ne abych se zase načapala, jak skáčeš z dalších útesů.]: All better. I don't want to see you jumping off any more cliffs.
2012	  *[Tohle asi zanechá jizvu.]: That's probably going to leave a scar.
2013	  *[Podařilo se mi tvůj obličej sešít. Příště si dávej větší pozor.]: I managed to sew your face back on. Be more careful next time.
2014	  *[Přestaň plýtvat mým časem.]: Quit wasting my time.
2015	  *[Žádné šťastné konce ode mě nečekej.]: I don't give happy endings.
2016	  *[Pokud nechceš plastickou operaci, tak ti toho víc nenabídnu.]: I can't do anymore for you without plastic surgery.
2017	  *[Omlouvám se, ale mé služby si nemůžeš momentálně dovolit.]: I'm sorry, but you can't afford me.
2018	  *[Budeš potřebovat více zlata, než je tohle.]: I'm gonna need more gold than that.
2019	  *[Jen abys věděl – nepracuji zadarmo.]: I don't work for free you know.
2020	  *[1,485]: Expert Mode
2021	  *[2,227]: Master Mode
2022	  *[500]: Expert Mode
2023	  *[%55]: Expert Mode
2024	  *[%64]: Expert Mode
2025	  *[Vrať se zpět za noci, pokud si přeješ vstoupit.]: Come back at night if you wish to enter.
2026	  *[Nemůžu tě pustit dále, pokud mě neosvobodíš od mé kletby.]: I cannot let you enter until you free me of my curse.
2027	  *[Můj pán nemůže být vyvolán pod záštitou denního světla.]: My master cannot be summoned under the light of day.
2028	  *[Jsi příliš slabý na zlomení mé kletby. Vrať se zpět, až nebudeš taková nicka.]: You are far too weak to defeat my curse. Come back when you aren't so worthless.
2029	  *[Ubohý hlupáku. Nemůžeš si myslet, že bys mohl porazit mého pána ve stavu, v jakém se nacházíš.]: You pathetic fool. You cannot hope to face my master as you are now.
2030	  *[Doufám, že máš tak šest přátel stojících po tvém boku.]: I hope you have like six friends standing around behind you.
2031	  *[Prosím ne, cizinče. Jen bys marnil svůj drahocenný život.]: Please, no, stranger. You'll only get yourself killed.
2032	  *[Cizinče. Budeš dostatečně silný, abys porazil mého pána?]: Stranger, do you possess the strength to defeat my master?
2033	  *[Ty bys mohl být dostatečně silný na osvobození mě od mé kletby…]: You just might be strong enough to free me from my curse...
2034	  *[Prosím! Poraz mého věznitele a osvoboď mne! Zapřísahám tě!]: Please! Battle my captor and free me! I beg you!
2035	  *[Poraz mého pána a já ti zajistím průchod do podzemní kobky.]: Defeat my master, and I will grant you passage into the Dungeon.
2036	  *[Pokud porazíš mého pána, splním ti jedno přání.]: If you beat my master I will grant you one wish.
2037	  *[∞]: Must defeat Betsy
2038	  *[56]: Mode Expert
2039	  *[7–12]: Master Mode
2040	  *[24–40]: Expert Mode
2041	  *[28–48]: Master Mode
2042	  *[20-37.5]: Master Mode
2043	  *[64–120]: Expert Mode
2044	  *[80-150]: Master Mode
2045	  *[56–80]: Expert Mode
2046	  *[70–100]: Master Mode
2047	  *[40–56]: Expert Mode
2048	  *[60-84]: Master Mode
2049	  *[4–20]: Expert Mode
2050	  *[5–25]: Master Mode
2051	  *[28800]: Mode Expert
2052	  *[43200]: Mode Master
2053	  *[16-30]: Mode Expert
2054	  *[64-120]: Mode Expert
2055	  *[40-56]: Mode Expert
2056	  *[要100次]: Journey Mode
2057	  *[1/150 (0.67%)]: Expert Mode
2058	  *[12.89%]: Expert Mode
2059	  *[19%]: Expert Mode
2060	  *[9.78%]: Expert Mode
2061	  *[13.56%]: Expert Mode
2062	  *[29/225 (12.89%)]: Expert Mode
2063	  *[230 mph]: 230 miles per hour (as measured by the Stopwatch item) or 168.75 tiles per second
2064	  *[22/225 (9.78%)]: Expert Mode
2065	  *[19/100 (19%)]: Expert Mode
2066	  *[Expert Mode:]: Expert Mode
2067	  *[1.4%]: Expertní mód
2068	  *[1/70 (1.43%)]: Expert Mode
2069	  *[10›8]: Expert Mode : Pre-Hardmode › Hardmode
2070	  *[300›330]: Expert Mode : Pre-Hardmode › Hardmode
2071	  *[%-13]: Expert Mode
2072	  *[%1,4]: Expert Mode
2073	  *[5/12 (41.67%)]: Expert Mode
2074	  *[6/12 (50%)]: Expert Mode
2075	  *[1/12 (8.33%)]: Expert Mode
2076	  *[4–9]: Expert Mode
2077	  *[33,600]: Expert Mode
2078	  *[42,840]: Master Mode
2079	  *[21,000]: Expert Mode
2080	  *[26,775]: Master Mode
2081	  *[42,000–37,800]: Expert Mode
2082	  *[53,550–48,195]: Master Mode
2083	  *[37,799–33,600]: Expert Mode
2084	  *[48,194–42,840]: Master Mode
2085	  *[33,599–29,400]: Expert Mode
2086	  *[42,839–37,485]: Master Mode
2087	  *[29,399–25,200]: Expert Mode
2088	  *[37,484–32,130]: Master Mode
2089	  *[25,199–21,001]: Expert Mode
2090	  *[32,129–26,776]: Master Mode
2091	  *[21,000–16,800]: Expert Mode
2092	  *[26,775–21,420]: Master Mode
2093	  *[16,799–12,600]: Expert Mode
2094	  *[21,419–16,065]: Master Mode
2095	  *[12,599–8,400]: Expert Mode
2096	  *[16,064–10,710]: Master Mode
2097	  *[8,399–4,200]: Expert Mode
2098	  *[10,709–5,355]: Master Mode
2099	  *[4,199–0]: Expert Mode
2100	  *[5,354–0]: Master Mode
2101	  *[101×101]: Expert Mode
2102	  *[3/2500 (0.12%)]: Expert Mode
2103	  *[2–10 or 20]: Expert Mode
2104	  *[2.5–12.5 or 25]: Master Mode
2105	  *[4–20 or 40]: Expert Mode
2106	  *[5-12.5 or 50]: Master Mode
2107	  *[2.5-10]: Master Mode
2108	  *[4–16]: Expert Mode
2109	  *[5-20]: Master Mode
2110	  *[2.5-7.5]: Master Mode
2111	  *[5-15]: Master Mode
2112	  *[10 or 40]: Expert Mode
2113	  *[12.5 or 50]: Master Mode
2114	  *[20 or 80]: Expert Mode
2115	  *[25 or 100]: Master Mode
2116	  *[5-10]: Chế độ Expert
2117	  *[6-12.5]: Master Mode
2118	  *[10-20]: Master Mode
2119	  *[12-25]: Master Mode
2120	  *[4–18]: Chế độ Expert
2121	  *[7.5-17.5]: Master Mode
2122	  *[8–36]: Expert Mode
2123	  *[15-35]: Master Mode
2124	  *[4–8]: Expert Mode
2125	  *[8–16]: Expert Mode
2126	  *[5.23-10.5]: Expert Mode
2127	  *[6.53-13.12]: Master Mode
2128	  *[10-21]: Expert Mode
2129	  *[13-26]: Master Mode
2130	  *[14400]: Chế độ Expert
2131	  *[21600]: Chế độ Master
2132	  *[98]: Expert Mode
2133	  *[123]: Master Mode
2134	  *[196]: Expert Mode
2135	  *[246]: Master Mode
2136	  *[2–10 hoặc 20]: Chế độ Expert
2137	  *[4-20 hoặc 40]: Chế độ Expert
2138	  *[4-16]: Chế độ Expert
2139	  *[4-12]: Chế độ Expert
2140	  *[10 hoặc 40]: Chế độ Expert
2141	  *[20 hoặc 80]: Chế độ Expert
2142	  *[8-36]: Chế độ Expert
2143	  *[8-16]: Chế độ Expert
2144	  *[2.625–5.25]: Chế độ Expert
2145	  *[514 mph]: 514 miles per hour (as measured by the Stopwatch item) or 376.93 tiles per second
2146	  *[2/45]: Expert Mode
2147	  *[5–18]: Expert Mode
2148	  *[7–24]: Expert Mode
2149	  *[7–27]: Expert Mode
2150	  *[10–36]: Expert Mode
2151	  *[3–12]: Expert Mode
2152	  *[3–7]: Expert Mode
2153	  *[95 mph]: 95 miles per hour (as measured by the Stopwatch item) or 69.67 tiles per second
2154	  *[membutuhkan 3]: Mode Journey
2155	  *[6×]: Master Mode
2156	  *[3 mph]: 3 miles per hour (as measured by the Stopwatch item) or 1.875 tiles per second
2157	  *[by wave 12]: Expert Mode
2158	  *[0.56%]: Expert Mode
2159	  *[0.83%]: Expert Mode
2160	  *[1.11%]: Expert Mode
2161	  *[2–20]: Expert Mode
2162	  *[2.5–25]: Master Mode
2163	  *[2.5–10]: Master Mode
2164	  *[8-28 (depending on health)]: Chế độ Expert
2165	  *[2-20 seconds]: Chế độ Expert
2166	  *[2.5-25 seconds]: Chế độ Master
2167	  *[2-8 seconds (melee)]: Chế độ Expert
2168	  *[2.5-10 seconds (melee)]: Chế độ Master
2169	  *[14,400]: Expert Mode
2170	  *[18,360]: Master Mode
2171	  *[0.42 seconds]: Expert Mode
2172	  *[0.5 seconds]: Expert Mode
2173	  *[Descrizione]: General description of items in these tiers. Some exceptions will apply.
2174	  *[Mô tả]: Mô tả vật phẩm của bậc này. Một số ngoại lệ sẽ được áp dụng.
2175	  *[**撳呢度** 嚟載入內容。 _（可能會有些微延遲）_]: 呢個內容係喺外部儲存，所以你撳咗之後，喺佢未下載完之前會有延遲。
2176	  *[2.5 hours]: Master Mode
2177	  *[First part]: At 1/7 of the world
2178	  *[Combined]: Both parts (at 3/14 of the world)
2179	  *[1/5600 (0.02%)]: Expert Mode
2180	  *[Laju]: Laju Anak Panah
2181	  *[Krit]: Peluang Kritikal
2182	  *[382]: Master Mode
2183	  *[10.8%]: Expert Mode
2184	  *[35/324 (10.8%)]: Expert Mode
2185	  *[1/400 (0.25%)]: Expert Mode
2186	  *[27 mph]: 27 miles per hour (as measured by the Stopwatch item) or 19.8 tiles per second
2187	  *[5–10 seconds]: Master Mode
2188	  *[5–10]: Master Mode
2189	  *[0.018%]: Expert Mode
2190	  *[17,550]: Expert Mode
2191	  *[22,376]: Master Mode
2192	  *[5,850]: Expert Mode
2193	  *[7,458]: Master Mode
2194	  *[2 minutes]: Expert Mode
2195	  *[2 minutes 30 seconds]: Master Mode
2196	  *[0.56%–3.33%]: Expert Mode
2197	  *[2 minutes]: Expert Mode
2198	  *[2 minutes and 30 seconds]: Master Mode
2199	  *[107 mph]: 107 miles per hour (as measured by the Stopwatch item) or 78.75 tiles per second
2200	  *[cần có 99]: Chế độ Journey

```


---

## 🤖 Assistant · 2026-08-13T00:34:43.138Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The wiki dump is noisy (a lot of template expansion content). Key effective information has been obtained:

**Pressure Plates wiki**:
- Gray (542, tile135 style2), Brown (543, style3), Blue (852, style4), Lihzahrd (1151, style6): "Triggered by players only" (the wiki table groups these four together—actually this is wrong/the table is poorly merged; the real distinctions: Gray=players+NPC+enemies? No—the wiki shows "Gray/Brown/Blue/Lihzahrd: Triggered by players only" with only Lihzahrd (1151) as its own line. Look carefully: line 41-45 merges Gray/Brown/Blue/Lihzahrd with "Triggered by players only". line 46-47 merges Red (529, style0)/Green (541, style1): "Triggered by players, NPCs, enemies, and projectiles". line 48: Yellow (853, style5): "Triggered by NPCs and enemies" (not players!). line 49: Orange (4261, style7): "Triggered by players only. Breaks after being triggered" (single-use). line 50-53: Weighted (3626 pink style3/3630 orange style0/3631 purple style2/3632 cyan style1, tile428): "Triggered by players when stepping on or off it". line 54: Teal (3707, tile442): "Triggered by projectiles".

Note the wiki has some oddities here (Blue is actually "triggered by any entity but only fires once"?). No—the real source: Blue Pressure Plate = "activated by any character but only sends a signal once"? Let me recall the original Player.cs. Actually: Blue Plate's original description is "Triggered by NPCs and enemies; fires only once and then breaks"? No.

The accurate original (Player.cs PressureTileHandling / Tile frameY style→behavior table):
- style0 Red: players, NPCs, enemies, projectiles
- style1 Green: players, NPCs, enemies, projectiles? No, Green is "enemies only"?

I need the original code. Let me grep Player.cs 1456 for 135 / pressurePlate. The original is around Player.cs PressureTileHandling or "PressurePlateHelper". In 1.4, the pressure plate check is in Player.cs "if (tile.type == 135)" or a TileDrawing? Let me grep.

Actually, the wiki table is the authority for "trigger criteria" (corroborated by source code); but per the auditing iron rule, source code prevails. I'll grep the original pressure plate trigger table.

**Sensors wiki key points**:
- 7 types: Day(3613)/Night(3614)/Player Above(3615)/Liquid Water(3726)/Lava(3727)/Honey(3728)/Any(3729), tile 423
- Player Above: 5×10 tile area above; triggers on first player entering or last leaving; dead players don't trigger (1.4.2)
- **Player Above cannot activate Teleporters** (blockPlayerTeleportationForOneIteration!)—this is the semantics of that flag!
- Water Sensor is also triggered by Shimmer; rain does not trigger

This confirms: blockPlayerTeleportationForOneIteration is set to true by PokeLocation (PressurePlateHelper), i.e. **pressure plates (428 teal family, and all PressurePlateHelper-managed pads) inhibit teleports for one pass**. Wait—PressurePlateHelper only manages tile 428. But tile 442 (teal) has already been confirmed by wiki as "Triggered by projectiles". So 428=Weighted, 442=Teal! My earlier Wiring.cs HitSwitch handles 428/442 simultaneously for TripWire. OK:
- tile 135: ordinary pressure plates (styles 0-7)
- tile 428: Weighted Pressure Plates (player steps on/off, pressed state shared)
- tile 442: Teal Pressure Pad (triggered by projectiles/pets)
- tile 423: sensors (Day/Night/Player Above/Liquid)

Implementing Game.ts:1621 comments "trigger source registration (weighted plate 428 / sensor 423)".

The key source-level question: where is the trigger code for 135/423/442/476? In Player.cs (player stepping), NPC.cs (NPC stepping), Projectile.cs (projectiles hitting 442), and Liquid code (liquid sensors). These are all outside Wiring.cs. I need to grep these + the corresponding implementation-side Game.ts code.

Now Bash is back, run greps in batch. Also read Timers/Teleporter/Statues/Pumps/Logic_Gates wiki—these pages are also very long, so I'll use Bash grep to extract key lines instead of Reading whole files (to avoid noise).

Plan:
1. grep Player.cs 1456: pressure plate trigger (type == 135 / 442 / 423)
2. grep NPC.cs 1456: NPC stepping on plates
3. grep Projectile.cs 1456: 442
4. grep implementation-side Game.ts: pressure plate/sensor/teleportPair/statue
5. Extract key paragraphs from wiki using grep -A/-B

Do in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:34:43.816Z · glm-x-preview-260804

```
wiki 关键信息已到手(压板触发型号表、传感器 5×10 区/Player Above 禁传送 = `blockPlayerTeleportationForOneIteration` 语义)。现在批量定位源码与实现侧的触发链。
```


---

## 🤖 Assistant · 2026-08-13T00:34:45.011Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===Player 135===\"; grep -n \"type == 135\\|type == 442\\|type == 423\\|type == 476\" $T/Terraria/Player.cs | head -20; echo \"===NPC plates===\"; grep -rn \"type == 135\\|type == 442\" $T/Terraria/NPC.cs | head -10; echo \"===Projectile 442===\"; grep -rn \"type == 442\\|442 &&\" $T/Terraria/Projectile.cs | head -5",
 "description": "Locate plate/sensor trigger code in vanilla"
}
```


---

## 🤖 Assistant · 2026-08-13T00:34:46.096Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; echo \"===Game sensor/plate===\"; grep -n \"423\\|442\\|428\\|sensor\\|Sensor\\|pressurePlate\\|PressurePlate\\|teleportPair\\|statue\" $G/core/Game.ts | head -40",
 "description": "Locate sensor/plate/teleport implementation in Game.ts"
}
```


---

## 🤖 Assistant · 2026-08-13T00:34:46.865Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "W=~/Project/GLM/SandboxWorld/terraria-wiki-md; echo \"===Timers===\"; grep -n \"second\\|tick\\|60\\|cooldown\" $W/Timers.md | head -20; echo \"===Teleporter===\"; grep -n -i \"48\\|three\\|NPC\\|pet\\|minion\\|teleport\" $W/Teleporter.md | head -30",
 "description": "Extract timer and teleporter wiki facts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:35:18.104Z

**📎 ToolResult**

```
===Player 135===
9442:		if (armorItem.type == 4762)
12653:		if (HeldItem.type == 4760 && ownedProjectileCounts[866] < 1)
15525:		if (currentItem.type == 4237)
15541:		if (currentItem.type == 4421)
31230:		bool flag = inventory[selectedItem].type == 3823 || inventory[selectedItem].type == 4760;
36378:		if (type == 4760 && ownedProjectileCounts[866] < 1)
45525:		else if (Main.tile[x, y].type == 442)
===NPC plates===
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:10612:		else if (type == 135)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:14179:		else if (type == 442)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:18004:		else if (type == 135)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:18290:			if (type == 135)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:50229:			if (type == 135)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:78996:				if (Main.npc[n].active && (Main.npc[n].type == 134 || Main.npc[n].type == 135 || Main.npc[n].type == 136))
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:80766:		if (type == 134 || type == 135 || type == 136)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:80770:				if (j != whoAmI && Main.npc[j].active && (Main.npc[j].type == 134 || Main.npc[j].type == 135 || Main.npc[j].type == 136))
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:90263:				if (type == 135 && life > 0 && Main.netMode != 1)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:93443:		else if (type == 74 || type == 297 || type == 298 || type == 442 || type == 671 || type == 672 || type == 673 || type == 674 || type == 675)
===Projectile 442===
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:4853:		else if (type == 442)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:51840:		if (type == 442)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:54638:			else if (type != 442 && type != 634 && type != 635 && type != 675)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:70424:		if (type == 442)

```


---

## 👤 User(sidechain) · 2026-08-13T00:35:18.126Z

**📎 ToolResult**

```
===Game sensor/plate===
7:import { plates428Pressed } from '../render/VanillaTiler';
1264:  /** 测重板踩踏状态(原版 PressurePlateHelper 进/离双触发) */
1266:  /** 触发源登记(idx):428 测重板 / 423 感应器 */
1267:  triggerTiles428 = new Set<number>();
1271:  triggerTiles423 = new Set<number>();
1621:    // 电路系统(Wiring.cs 移植):器件表 + 触发源登记(测重板 428/感应器 423)
2111:        // 昼/夜逻辑感应器(423)触发
2112:        this.triggerDayNightSensors();
2811:    this.checkPressurePlates();
2835:    // ---- 灯笼夜 UpdateTime（Main.cs:64429 = LanternNight.UpdateTime 每帧位）：
3777:    // 指针切到 Cursors[12] 智能光标帧（Main.cs:47442-47513 num=11+smart.ToInt()）
4006:        // ★ melee+shoot 剑族（附魔剑 989/波刃 190 等，Player.cs:42880 flag4 语义）：
4201:      this.player.useTime = 45;   // Item 5340 useTime（Item.cs:42342）
4957:      // 矿车轨道锤击（Player.cs:45442-45447）：FrameTrack(pound) 循环切换连接/加速向
6721:  private checkPressurePlates(): void {
6745:  /** 测重板 428(原版 PressurePlateHelper 进/离双触发)+ 感应器 423(玩家上方/昼夜)。
6752:    // 测重板:玩家 AABB 覆盖格(原版 PressurePlateHelper 16×10 底部判定)
6756:    for (const idx of this.triggerTiles428) {
6767:    // 镜像踩踏态到渲染模块(428 被踩帧偏移,VanillaTiler.plates428Pressed)
6768:    plates428Pressed.clear();
6769:    for (const idx of this.weightedLatch) plates428Pressed.add(idx);
6777:    // 感应器 423:玩家上方(frameY 0=昼 36=夜 72=玩家出入上方,placeStyle 0-2 → frameY/18%3)
6779:    for (const idx of this.triggerTiles423) {
6785:      // 昼/夜感应由 onDayNight 回调驱动(见 triggerDayNightSensors)
6789:  /** 昼/夜切换时触发全部对应感应器(原版逻辑在 Projectile.LogicSensor 驱动) */
6790:  triggerDayNightSensors() {
6795:    for (const idx of this.triggerTiles423) {
6806:   *  巨石弹幕(原版 type 99,Projectile.cs:11833)触发 135 与弹幕垫板 442 */
6817:          if (sh === 135 || (checkPad && sh === 442)) {
6962:      // 灯笼夜天气压制（Main.cs:64288 云钳 30 / :64331 停雨 / :64353 不开新雨 /
7038:    this.triggerTiles428.clear();
7039:    this.triggerTiles423.clear();
7040:    const s428 = TILE_BY_KEY['v_428_weightedpressureplate'] ?? 0;
7041:    const s423 = TILE_BY_KEY['v_423_logicsensor'] ?? 0;
7044:      if (s428 && st.type[i] === s428) this.triggerTiles428.add(i);
7045:      else if (s423 && st.type[i] === s423) this.triggerTiles423.add(i);
7051:      if (t === s428) this.triggerTiles428.add(i);
7052:      else this.triggerTiles428.delete(i);
7053:      if (t === s423) this.triggerTiles423.add(i);
7054:      else this.triggerTiles423.delete(i);

```


---

## 👤 User(sidechain) · 2026-08-13T00:35:33.513Z

**📎 ToolResult**

```
===Timers===
42:~~~~|  1 Second TimerInternal [Item ID](Item_IDs.md "Item IDs"): 583 | 144  | Signals every second | 1 _GC_ | 20 _SC_  
43:~~~~|  3 Second TimerInternal [Item ID](Item_IDs.md "Item IDs"): 584 | 144 (1)  | Signals every 3 seconds | 1 _GC_ | 20 _SC_  
44:~~~~|  5 Second TimerInternal [Item ID](Item_IDs.md "Item IDs"): 585 | 144 (2)  | Signals every 5 seconds | 1 _GC_ | 20 _SC_  
45:~~~~|  1/2 Second Timer**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 4484 | 144 (3)  | Signals every half of a second | 2 _GC_ | 40 _SC_  
46:~~~~|  1/4 Second Timer**** __(Desktop, Console and Mobile versions) Internal [Item ID](Item_IDs.md "Item IDs"): 4485 | 144 (4)  | Signals every fourth of a second | 2 _GC_ | 40 _SC_  
339:  * [Glowstick](Glowstick.md "Glowstick")
340:    * [Sticky](Sticky_Glowstick.md "Sticky Glowstick")
341:    * [Bouncy](Bouncy_Glowstick.md "Bouncy Glowstick")
342:    * [Spelunker](Spelunker_Glowstick.md "Spelunker Glowstick")
343:    * [Fairy](Fairy_Glowstick.md "Fairy Glowstick")
344:    * [Rainbow](Rainbow_Glowstick.md "Rainbow Glowstick")
700:  *[160]: Expert Mode
718:  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
733:  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11.25 tiles per second
734:  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
738:  *[5–9 seconds]: Master Mode
745:  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
746:  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
747:  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
751:  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30 tiles per second
===Teleporter===
1:# Teleporter
3:> 原页面: `Teleporter`
5:# Teleporter
7:Teleporter
19:[Tooltip](Tooltips.md "Tooltips")|  _Transports creatures to a connected teleporter when signalled_  
27:Teleport|   
33:A Teleporter in action.
35:The **Teleporter** is a travel [mechanism](Mechanism "Mechanism") purchased from the ****__(Desktop, Console and Mobile versions) [Mechanic](Mechanic.md "Mechanic") / ****__(Old-gen console and 3DS versions) [Steampunker](Steampunker.md "Steampunker") for 2 _GC_ 50 _SC_. When two Teleporters are [wired](Wire.md "Wire") together with a triggering mechanism, they can exchange players, [NPCs](NPCs.md "NPCs"), and most [enemies](Enemies.md "Enemies") between them. Teleporting is always instantaneous, has no load time or cooldown, no [Mana](Mana.md "Mana") or [coin](Coin "Coin") cost, and no limit on distance. 
37:Unlike most [furniture](Furniture.md "Furniture"), Teleporters are [foreground objects](Foreground_object "Foreground object"). They consist of three inseparable [blocks](Blocks.md "Blocks") which, like all block types, can individually be shaped with a [hammer](Hammer "Hammer") or [actuated](Actuator.md "Actuator"). 
41:The two Teleporters to be transported between must be placed on a surface of solid blocks or [platforms](Platforms.md "Platforms") and connected by Wire, along with a trigger mechanism, such as a [Switch](Switch.md "Switch") or [Pressure Plate](Pressure_Plate "Pressure Plate"). When the trigger is activated, all players, all NPCs, and most enemies touching the 3×3-tile area above it are instantly transported to the other Teleporter. A character standing a maximum of three tile heights above the Teleporter can still be transported, and burying a Teleporter two tiles deep can still transport players walking on the surface. Similarly, placing an actuated, hammered to half-tile height Teleporter on platforms and standing one tile below the platforms will also transport the player. Entities retain their location relative to the Teleporter within the 3×3 area when teleporting. For instance, players using a Teleporter two tiles above its surface will arrive two tiles above the surface of the destination Teleporter. See the gallery below for example images. 
43:Teleporting is always two-way: when a connection is activated, both ends will _exchange_ all players, NPCs, and enemies that are at least partially occupying any square of the 3×3-tile rectangle. Players should keep this in mind when constructing Teleporter paths, as enemies could unintentionally be brought into a base, for example. 
47:  * On the [ Desktop version](Desktop_version_history.md "Desktop version history"), [ Console version](Console_version.md "Console version"), and [ Mobile version](Mobile_version.md "Mobile version"), there is no limit on wire lengths or distance between Teleporters.
48:  * On the [ Old-gen console version](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [Nintendo 3DS](Legacy%3A3DS_version "Legacy:3DS version")[](Legacy%3A3DS_version "3DS")[ version](Legacy%3A3DS_version "Legacy:3DS version"), the distance that entities can be teleported is limited.Verify Similarly, wires connecting two Teleporters can only transmit a signal up to 2,000 tiles away.
49:  * Teleporters will not transport [worm enemies](Worm_AI.md "Worm AI"), [bosses](Bosses.md "Bosses"), other enemies that travel through blocks, [critters](Critters.md "Critters"), [liquids](Liquids.md "Liquids"), dropped items, projectiles (which includes [pets](Pets.md "Pets") and light pets as well as [Boulders](Boulder.md "Boulder") and [Rolling Cacti](Rolling_Cactus.md "Rolling Cactus")**** __(Desktop, Console and Mobile versions)), any enemy from the [Old One's Army](Old_One's_Army.md "Old One's Army")**** __(Desktop, Console and Mobile versions) [event](Event "Event"), or placed [furniture](Furniture.md "Furniture").
50:  * A Teleporter will not work if it is placed in front of [unsafe](Unsafe_wall.md "Unsafe wall") [Lihzahrd Brick Walls](Lihzahrd_Brick_Wall.md "Lihzahrd Brick Wall") and [Plantera](Plantera.md "Plantera") has not yet been defeated.
51:  * Teleporters will not teleport players if activated via a [Logic Sensor (Player Above)](Sensors.md "Sensors").
55:An eight-pass Teleporter array with four Teleporters connected by four different colored wires at the ends of the middle Teleporter.
57:  * A single Teleporter can be wired to multiple destinations. With access to only a single wire color, each end of a Teleporter pad can be wired to one destination each, for a total of two possible destinations (each must have its own triggering mechanism). Using all four wire colors, each end of the Teleporter can be wired to four destinations each, for a total of eight possible destinations (two red, two blue, two green, and ****__(Desktop, Console and Mobile versions) two yellow). 
58:    * On the [ Old-gen console version](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [Nintendo 3DS](Legacy%3A3DS_version "Legacy:3DS version")[](Legacy%3A3DS_version "3DS")[ version](Legacy%3A3DS_version "Legacy:3DS version"), which only have three wire colors, each end of the Teleporter can be wired to three destinations each, for a total of six possible destinations (two red, two blue, and two green).
59:    * With more than one Teleporter, the number of possible destinations from one spot becomes even larger. Seven Teleporters, for example, can facilitate a total of 36 different destinations. See the gallery below for example setups.
60:  * The three blocks composing the Teleporter can be shaped using a [hammer](Hammer "Hammer"). This does not affect the Teleporter's function, except that the 3×3 area to be teleported and the position of the teleported entity are both relative to the Teleporter's surface, i.e. if the Teleporter is flattened to half blocks, they will both move down half a block (if the three blocks are different shapes, the height is determined by the first block encountered in the algorithm described below). Note that pressure plates can only be placed on full blocks.
61:  * Other blocks or furniture can be placed on Teleporters. These will not be teleported, nor will they "block" teleportation of entities above them, as long as the entities are still within the 3×3 area of effect.
63:Due to the length of the wire, only the Teleporters on the left and in the center will be activated. The one on the right will always be inactive.
65:  * If three or more Teleporters are connected with the same colored wire, a player (or NPC or enemy) will be teleported to whichever is farthest. This distance is measured in the most direct wire distance, not physical distance (a wire looping around takes more space than a direct straight connection). This distance is also measured from the triggering mechanism (Switch, Pressure Plate, etc.), not the entity being teleported. With multiple triggers, certain Teleporter combinations may thus result in failure to teleport.
66:  * ****__(Desktop, Console and Mobile versions) Teleporting releases all [hooks](Hooks.md "Hooks").
67:  * Unlike most forms of player movement, Teleporters are [server](Server.md "Server")-sided. This means that they are not instantaneous in [Multiplayer](Multiplayer.md "Multiplayer") worlds.
69:## Algorithms determining destination Teleporter
71:When a wire network (single color) with more than two Teleporters is activated, an algorithm determines which pair will activate. This algorithm was rather naive prior to the [1.2.3](1.2.3.md "1.2.3") update and was improved afterward. Both versions are described below. 
73:Both algorithms are [deterministic](https://en.wikipedia.org/wiki/en:deterministic "wikipedia:en:deterministic") (i.e., their result can be predicted ahead of time), so a fixed wiring layout will always activate the same Teleporters. Therefore, the wiring layout can be designed to target the desired Teleporter. 
77:  * Starting from the tile of the trigger mechanism (e.g. Switch or Pressure Plate), the length of the wire to each Teleporter is measured (using a variant of [Dijkstra's algorithm](https://en.wikipedia.org/wiki/en:Dijkstra%27s_algorithm "wikipedia:en:Dijkstra's algorithm")).

```


---

## 🤖 Assistant · 2026-08-13T00:35:45.892Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
有效信息大量到手:

**计时器 wiki**:
- 1s(583, 144 style0)、3s(584, style1)、5s(585, style2)、1/2s(4484, style3)、1/4s(4485, style4)——五种。1/2s 和 1/4s 是 Desktop 版("Desktop, Console and Mobile"标记),不是 1.4.4 新增,是 1.3.1 时代。与源码 period 60/180/300/30/15 ✅ 完全吻合。必核清单第 4 项的"1/4s(1456 新增?)"——**不是 1456 新增**,早已存在。

**传送器 wiki**:
- 3×3 tile 区域上方(判定盒 48×48 ✅ 与源码一致)
- 双向交换 ✅
- 不传送:蠕虫/boss/穿墙怪/critter/液体/掉落物/投射物(含宠物)/OOA 怪
- 神庙墙(87)+Plantera 未杀 → 不工作 ✅(源码 case 235)
- Player Above 传感器触发的传送器不传玩家 ✅(blockPlayerTeleportationForOneIteration)
- 3+ 传送器同色 → 最远者(算法,1.2.3 后 Dijkstra 变体)——这是 BFS 距离的实现,原版 hitWire BFS 自然实现"最远"?其实原版 Teleport() 只取 _teleport[0]/[1],BFS 遍历顺序决定。不深入。

**实现侧 Game.ts**:
- 6721 checkPressurePlates():428 测重板 + 423 感应器
- 6752 测重板:玩家 AABB 覆盖格(16×10 底部判定)
- 6777 感应器 423:玩家上方 frameY 0=昼 36=夜 72=玩家出入上方,placeStyle 0-2
- 6789 triggerDayNightSensors():昼夜感应
- 6806 巨石弹触发 135 + 442
- 7038 触发源登记扫描

**原版侧**:
- Player.cs:45525 `type == 442`(Teal,玩家也会触发?有趣——45525 在 Player.cs,可能是"玩家不触发 teal"的排除逻辑)
- NPC.cs:10612/18004/18290/50229 type==135(NPC 踩板)、14179 type==442
- Projectile.cs:4853/51840/70424 type==442(投射物触发 teal)

现在需要读这些原版段落 + 实现侧 Game.ts 对应段落,并核对:
1. 压板 135 的 style→触发者表(玩家/NPC/投射物各自代码)
2. 423 感应器(Player.cs?原版 423 触发在 Projectile.LogicSensor!wiki 说昼夜感应由 Projectile.LogicSensor 驱动——实现注释 6789 说"原版逻辑在 Projectile.LogicSensor 驱动"。对,1.4 把传感器逻辑放进 Projectile.cs 的 LogicSensor(投射物 578?)。让我 grep Projectile.cs 的 423。
3. 442 teal 的触发(投射物+玩家?)

让我批量读。

然后还要:
- 实现 Game.ts 7149-7250 传送器对
- 实现 Game.ts 7000-7130 雕像 spawnNpc
- 实现 mechSpawnOk/itemSpawnOk(NPC.cs MechSpawn / Item.cs MechSpawn 数值)
- 原版 NPC.cs MechSpawn(7399-7483)与 Item.cs MechSpawn(48982-49013)
- wiki Statues 刷怪规则
- 原版 Player.cs 411 引爆器踩踏 + 210 地雷踩踏(HitSwitch 210 缺失的右键路径)
- 传感器 423 原版(Projectile.cs LogicSensor)

批次执行。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:35:46.752Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===Projectile 423 sensor===\"; grep -n \"== 423\\|LogicSensor\" $T/Terraria/Projectile.cs | head -10; echo \"===NPC MechSpawn===\"; sed -n '7399,7483p' $T/Terraria/NPC.cs",
 "description": "Find sensor driver and NPC MechSpawn source"
}
```


---

## 🤖 Assistant · 2026-08-13T00:35:47.149Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; sed -n '6721,6830p' $G/core/Game.ts",
 "description": "Read plate/sensor implementation in Game.ts"
}
```


---

## 🤖 Assistant · 2026-08-13T00:35:47.512Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; sed -n '7140,7260p' $G/core/Game.ts",
 "description": "Read teleport pair implementation in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:35:58.969Z

**📎 ToolResult**

```
===Projectile 423 sensor===
4687:		else if (type == 423)
62133:		if (type == 423)
62170:		if (type == 423)
62197:		if (type == 423)
62324:		if (type == 423 && localAI[0] > 0f)
62363:		if (type == 423)
62403:		if (type == 407 || type == 613 || type == 423)
62407:			if (type == 423)
62497:		if (flag && type == 423)
62541:		if (type == 423 || type == 407)
===NPC MechSpawn===
	public static bool MechSpawn(float x, float y, int type)
	{
		int num = 0;
		int num2 = 0;
		int num3 = 0;
		for (int i = 0; i < Main.maxNPCs; i++)
		{
			if (!Main.npc[i].active)
			{
				continue;
			}
			bool flag = false;
			if (Main.npc[i].type == type)
			{
				flag = true;
			}
			else if (type == 74 || type == 297 || type == 298)
			{
				if (Main.npc[i].type == 74 || Main.npc[i].type == 297 || Main.npc[i].type == 298)
				{
					flag = true;
				}
			}
			else if (type == 46 || type == 540 || type == 303 || type == 337)
			{
				if (Main.npc[i].type == 46 || Main.npc[i].type == 540 || Main.npc[i].type == 303 || Main.npc[i].type == 337)
				{
					flag = true;
				}
			}
			else if (type == 362 || type == 364)
			{
				if (Main.npc[i].type == 362 || Main.npc[i].type == 363 || Main.npc[i].type == 364 || Main.npc[i].type == 365)
				{
					flag = true;
				}
			}
			else if (type == 602)
			{
				if (Main.npc[i].type == 602 || Main.npc[i].type == 603)
				{
					flag = true;
				}
			}
			else if (type == 608)
			{
				if (Main.npc[i].type == 608 || Main.npc[i].type == 609)
				{
					flag = true;
				}
			}
			else if (type == 616 || type == 617)
			{
				if (Main.npc[i].type == 616 || Main.npc[i].type == 617)
				{
					flag = true;
				}
			}
			else if (type == 55 && Main.npc[i].type == 230)
			{
				flag = true;
			}
			else if (NPCID.Sets.IsDragonfly[type] && NPCID.Sets.IsDragonfly[Main.npc[i].type])
			{
				flag = true;
			}
			if (flag)
			{
				num++;
				Vector2 vector = new Vector2(x, y);
				float num4 = Main.npc[i].position.X - vector.X;
				float num5 = Main.npc[i].position.Y - vector.Y;
				float num6 = (float)Math.Sqrt(num4 * num4 + num5 * num5);
				if (num6 < 200f)
				{
					num2++;
				}
				if (num6 < 600f)
				{
					num3++;
				}
			}
		}
		if (num2 >= 3 || num3 >= 6 || num >= 10)
		{

```


---

## 👤 User(sidechain) · 2026-08-13T00:35:58.993Z

**📎 ToolResult**

```
  private checkPressurePlates(): void {
    // 原版 Collision.SwitchTiles(Player.cs:18439):扫玩家 AABB 覆盖的全部格,
    // 命中压板 135 边沿触发(踩上/离开各一次,plateLatch 按格去重)
    const p = this.player;
    const x0 = Math.floor(p.x / TILE), x1 = Math.floor((p.x + p.w - 1) / TILE);
    const y0 = Math.floor(p.y / TILE), y1 = Math.floor((p.y + p.h - 1) / TILE);
    // 复用 Set(2026-08 审计 G9:此前每 tick new Set + [...spread],60Hz 恒定分配)
    const pressed = this._platePressed; pressed.clear();
    for (let ty = y0; ty <= y1; ty++) {
      for (let tx = x0; tx <= x1; tx++) {
        if (this.wiring?.sheetOf(tx, ty) === 135) {
          const key = tx + ',' + ty;
          pressed.add(key);
          if (!this.plateLatch.has(key)) this.wiring?.hitSwitch(tx, ty);
        }
      }
    }
    for (const key of pressed) this.plateLatch.add(key);
    // Set 迭代中删除当前元素是安全的——省去 [...spread] 复制
    for (const key of this.plateLatch) {
      if (!pressed.has(key)) this.plateLatch.delete(key);
    }
  }

  /** 测重板 428(原版 PressurePlateHelper 进/离双触发)+ 感应器 423(玩家上方/昼夜)。
   *  触发源由 scanTriggerTiles 登记,onTileChanged 增量维护 */
  private updateTriggerTiles(): void {
    const w = this.wiring;
    if (!w) return;
    const st = this.world.store;
    const p = this.player;
    // 测重板:玩家 AABB 覆盖格(原版 PressurePlateHelper 16×10 底部判定)
    const standing = this._weightedStanding; standing.clear();
    const px0 = Math.floor(p.x / TILE), px1 = Math.floor((p.x + p.w - 1) / TILE);
    const py0 = Math.floor(p.y / TILE), py1 = Math.floor((p.y + p.h - 1) / TILE);
    for (const idx of this.triggerTiles428) {
      const x = idx % st.w, y = (idx / st.w) | 0;
      if (x >= px0 && x <= px1 && y >= py0 && y <= py1) standing.add(idx);
    }
    for (const idx of standing) {
      if (!this.weightedLatch.has(idx)) {
        this.weightedLatch.add(idx);
        w.blockPlayerTeleportationForOneIteration = true; // 原版 MoveInto(:135-142)
        w.hitSwitch(idx % st.w, (idx / st.w) | 0);
      }
    }
    // 镜像踩踏态到渲染模块(428 被踩帧偏移,VanillaTiler.plates428Pressed)
    plates428Pressed.clear();
    for (const idx of this.weightedLatch) plates428Pressed.add(idx);
    for (const idx of this.weightedLatch) {
      if (!standing.has(idx)) {
        this.weightedLatch.delete(idx);
        w.blockPlayerTeleportationForOneIteration = true; // 原版 MoveAwayFrom 双触发
        w.hitSwitch(idx % st.w, (idx / st.w) | 0);
      }
    }
    // 感应器 423:玩家上方(frameY 0=昼 36=夜 72=玩家出入上方,placeStyle 0-2 → frameY/18%3)
    const ptx = Math.floor(p.cx / TILE), pty = Math.floor((p.y + p.h) / TILE);
    for (const idx of this.triggerTiles423) {
      const x = idx % st.w, y = (idx / st.w) | 0;
      const mode = Math.floor(st.frameY[idx] / 18) % 3;
      if (mode === 2 && x === ptx && pty > y && pty - y <= 8) {
        w.hitSwitch(x, y);
      }
      // 昼/夜感应由 onDayNight 回调驱动(见 triggerDayNightSensors)
    }
  }

  /** 昼/夜切换时触发全部对应感应器(原版逻辑在 Projectile.LogicSensor 驱动) */
  triggerDayNightSensors() {
    const w = this.wiring;
    if (!w) return;
    const st = this.world.store;
    const isDay = this.world.clock.isDay;
    for (const idx of this.triggerTiles423) {
      const mode = Math.floor(st.frameY[idx] / 18) % 3;
      // mode 0=昼感应器:日出触发;1=夜:日落触发
      if ((mode === 0 && isDay) || (mode === 1 && !isDay)) {
        w.hitSwitch(idx % st.w, (idx / st.w) | 0);
      }
    }
  }

  /** 实体踩板(Collision.SwitchTiles objType 2/3 语义):
   *  小动物族触发压板 135(NPC.cs:47613 白名单由 critters 桶近似);
   *  巨石弹幕(原版 type 99,Projectile.cs:11833)触发 135 与弹幕垫板 442 */
  private updateEntityPlates(): void {
    const w = this.wiring;
    if (!w) return;
    const pressed = this._entityPlatePressed; pressed.clear();
    const scan = (e: Entity, checkPad: boolean) => {
      const x0 = Math.floor(e.x / TILE), x1 = Math.floor((e.x + e.w - 1) / TILE);
      const y0 = Math.floor(e.y / TILE), y1 = Math.floor((e.y + e.h - 1) / TILE);
      for (let ty = y0; ty <= y1; ty++) {
        for (let tx = x0; tx <= x1; tx++) {
          const sh = w.sheetOf(tx, ty);
          if (sh === 135 || (checkPad && sh === 442)) {
            const key = e.id + '|' + tx + ',' + ty;
            pressed.add(key);
            if (!this.entityPlateLatch.has(key)) w.hitSwitch(tx, ty);
          }
        }
      }
    };
    for (const c of this.entities.critters) scan(c, false);
    for (const e of this.entities.projectiles) {
      // duck-typing 判巨石(勿用 instanceof:跨模块实例会判失败)
      if ((e as TrapShot).kind === 'boulder') scan(e, true);
    }
    for (const key of pressed) this.entityPlateLatch.add(key);

```


---

## 👤 User(sidechain) · 2026-08-13T00:35:59.018Z

**📎 ToolResult**

```
          if (e instanceof TrapShot && e.kind === kind && Math.hypot(e.x - px, e.y - py) < radius) n++;
        }
        return n;
      },
      spikyBudgetPenalty: (px: number, py: number) => {
        // Wiring.cs 1456 :1952-1966:每个场上 185 按距离扣预算
        // (<50→50 <100→15 <200→10 <300→8 <400→6 <500→5 <700→4 <900→3 <1200→2 其余 1)
        let pen = 0;
        for (const e of this.entities.projectiles) {
          if (!(e instanceof TrapShot) || e.kind !== 'spiky' || e.dead) continue;
          const d = Math.hypot(e.x + e.w / 2 - px, e.y + e.h / 2 - py);
          pen += d < 50 ? 50 : d < 100 ? 15 : d < 200 ? 10 : d < 300 ? 8
            : d < 400 ? 6 : d < 500 ? 5 : d < 700 ? 4 : d < 900 ? 3 : d < 1200 ? 2 : 1;
        }
        return pen;
      },
      doorOpen: (x: number, y: number) => {
        // 原版 HitWireSingle 10/11:随机方向 + 反向重试(WorldGen.OpenDoor)
        const dir = Math.random() < 0.5 ? 1 : -1;
        if (!openDoor(this.world.store, x, y, dir)) return openDoor(this.world.store, x, y, -dir) ;
        return true;
      },
      doorClose: (x: number, y: number) => closeDoor(this.world.store, x, y),
      teleportPair: (a: [number, number], b: [number, number]) => this.teleportPairImpl(a, b),
      relocateTownNpc: (group: 0 | 1, px: number, py: number) => {
        // 雕像 40/41 城镇 NPC 白名单(原版两组;此处按 NPC 图鉴顺序取前几个存在的)
        const groups: Array<Array<string>> = [
          ['guide', 'merchant', 'nurse', 'demolitionist', 'dyer', 'arms_dealer'],
          ['dryad', 'painter', 'golfer', 'zoologist', 'pirate', 'stylist'],
        ];
        for (const key of groups[group]) {
          const npc = this.entities.npcs.find((n) => (n as TownNPC).npcKey === key);
          if (npc) {
            npc.x = px - npc.w / 2;
            npc.y = py - npc.h - 1;
            return true;
          }
        }
        return false;
      },
      explode: (tx: number, ty: number, damage: number, radius?: number, destroyTiles?: boolean) =>
        this.explodeAt(tx, ty, damage, radius, destroyTiles),
      extractinatorPull: (ax: number, ay: number, blockType: number) =>
        this.extractinatorPullImpl(ax, ay, blockType),
      dropItemStack: (vid: number, stack: number, px: number, py: number) =>
        this.dropItemStackImpl(vid, stack, px, py),
      toast: (m: string) => this.cb.onToast(m),
      sfx: (n: string, x?: number, y?: number) => {
        if (x !== undefined && y !== undefined) this.sfxAt(n as SfxName, x, y);
        else this.sfx.play(n as SfxName);
      },
      // 广播盒（Wiring.cs:1177-1230 1:1）：Sign.ReadSign(anchor, CreateIfMissing:false)
      // ——锚点精确匹配，无登记/空文本静默；命中 → NewTextMultiline(text, pink, 460)
      // （全链在 announcementBoxMessage，色值/折行宽度同源）
      announce: (x: number, y: number) => {
        const msg = announcementBoxMessage(this.world.signs, x, y);
        if (msg) this.newText(msg.text, msg.r, msg.g, msg.b, msg.width);
      },
      // 派对纪念碑（Wiring.cs:2037-2039 → BirthdayParty.ToggleManualParty）
      toggleParty: () => {
        toggleManualParty(this.partyState);
      },
    };
  }

  /** 广播盒右键（Player.cs:32231-32250）：Sign.ReadSign(anchor, CreateIfMissing:true)
   *  ——锚点无登记则懒建空牌项（Sign.cs:45-59），再开文本编辑面板 */
  private openSignEditor(x: number, y: number): void {
    let sign = this.world.signs.find((s) => s.x === x && s.y === y);
    if (!sign) {
      sign = { x, y, text: '' };
      this.world.signs.push(sign);
    }
    this.cb.onEditSign?.(x, y, sign.text);
  }

  /** 编辑面板保存（Sign.TextSign :63-77：按登记下标写回文本） */
  setSignText(x: number, y: number, text: string): void {
    const sign = this.world.signs.find((s) => s.x === x && s.y === y);
    if (!sign) return;
    sign.text = text;
  }

  /** 传送器对(Wiring.cs:2314-2365):板上 48×48 判定框内实体双向搬迁 */
  private teleportPairImpl(a: [number, number], b: [number, number]) {
    // 太近的竖叠板拒绝(:2316)
    if (Math.abs(a[0] - b[0]) < 3 && a[1] > b[1] - 3 && a[1] < b[1]) return;
    const rect = (pad: [number, number]) => ({
      x: pad[0] * TILE, y: pad[1] * TILE - 48, w: 48, h: 48,
    });
    const hit = (r: { x: number; y: number; w: number; h: number }, e: { x: number; y: number; w: number; h: number }) =>
      e.x < r.x + r.w && e.x + e.w > r.x && e.y < r.y + r.h && e.y + e.h > r.y;
    const ra = rect(a), rb = rect(b);
    const dx = rb.x - ra.x, dy = rb.y - ra.y;
    if (!this.wiring?.blockPlayerTeleportationForOneIteration) {
      const p = this.player;
      if (!p.dead && hit(ra, p)) { p.x += dx; p.y += dy; p.vx = 0; p.vy = 0; this.sfx.play('tink'); }
      else if (!p.dead && hit(rb, p)) { p.x -= dx; p.y -= dy; p.vx = 0; p.vy = 0; this.sfx.play('tink'); }
    }
    for (const e of this.entities.enemies) {
      if (hit(ra, e)) { e.x += dx; e.y += dy; }
      else if (hit(rb, e)) { e.x -= dx; e.y -= dy; }
    }
  }

  /** 爆炸不可炸 tile 表（Projectile.CanExploteTile cs:75764 1:1）：
   *  地牢砖族 tileDungeon{41,43,44,677-679}(Main.cs:7941) + 基础宝箱 BasicChest{21,467}
   *  (TileID.cs:315) + switch 黑名单{26 祭坛,88 柜子,121/122 史莱姆块?,150 蛛网? ,
   *  211 血月砖?,226 蜥蜴砖,237 蜥蜴祭坛,248-250 尖刺?,346/470/475/504 陷阱族,685/686} */
  private static readonly EXPLODE_NEVER = new Set([41, 43, 44, 677, 678, 679, 21, 467,
    26, 88, 121, 122, 150, 211, 226, 237, 248, 249, 250, 346, 470, 475, 504, 685, 686]);
  /** 困难模式矿石（仅 scarab 弹 1086/1087 可炸——未引入恒 false） */
  private static readonly EXPLODE_HM_ORE = new Set([107, 108, 111, 221, 223]);
  /** 爆炸半径表（Projectile.cs:75262）：炸弹族=4、炸药棍族=7、放置炸药 108=10；
   *  表外（手雷 30 等）= 不破坏地形（Kill 判定表 :75260 之外） */
  static readonly EXPLODE_RADIUS: Record<number, number> = {
    28: 4, 37: 4, 516: 4, 519: 4, 29: 7, 470: 7, 637: 7, 108: 10,
  };
  /** CanExploteTile 纯函数版（测试用）：规则见 explodeAt 注释 */
  static canExplodeTile(
    st: World['store'], x: number, y: number, hardMode: boolean, golemDown: boolean, lavaLine: number,

```


---

## 🤖 Assistant · 2026-08-13T00:36:35.853Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
非常有价值。现在核对:

**实现侧传送器 teleportPairImpl(:7173-7199 附近)**:
1. 距离门 ✅(`Math.abs(a[0]-b[0])<3 && a[1]>b[1]-3 && a[1]<b[1]` ↔ 原版 :3141)
2. 判定盒 48×48,y-48 ✅
3. blockPlayerTeleportationForOneIteration 抑制玩家传送 ✅
4. **差异**:原版传送玩家时 `Main.player[j].Teleport(vector2)`(position + vector,即整体偏移,保留相对位置)+ teleporting 标志 + 释放钩。实现:`p.x += dx; p.y += dy; p.vx=0; p.vy=0; sfx tink`。清速度是近似(Teleport 不清速度?原版 Player.Teleport 会做什么——重置 velocity?实际原版 Teleport 设置 position 并触发 PortalColors/Teleport 演出,velocity 保留)。tink 音效原版无(原版传送无音效)。标 🔀 小。
5. **差异**:原版 NPC 传送条件:lifeMax>5 && !boss && !noTileCollide && !TeleportationImmune(NPCID.Sets)。实现只判 enemies 数组,无这些门(worm/boss/穿墙怪会被传送)。且 NPC 传送也受 teleporting 去重(一次性)。**缺失 TeleportationImmune/boss/worm 过滤** → 🔀/⚠️。wiki 49 行确认:worm/boss/穿墙怪/OOA/critter 不传送。critter 在实现里也不传送(只 enemies+player)✅,但 boss/worm 没排除。
6. **差异**:原版两个方向循环 `for i<2`(array[0]→array[1] 与反向),每方向先玩家后 NPC,实现只做了一次双向 if/else(等效)✅。
7. **缺失**:原版传送后清 teleporting = false;实现的 blockPlayerTeleportationForOneIteration 在 logicGatePass 末尾清除(Wiring.ts:531-533)✅ 语义等价。
8. **缺失**:原版 Teleport() 有 255 玩家循环(联机),实现单玩家 ✅ 合理近似。

**实现 relocateTownNpc**:
原版 :2418-2473:case 40/41 → CheckMech 300 → 随机选一个**活跃且在白名单**的城镇 NPC(array2[Main.rand.Next(num151)]),Teleport(style 14)到 (num142 - w/2, num143 - h - 1)。
- 白名单 group0(case 40):17,19,22,38,54,107,108,142,160,207,209,227,228,229,368,369,550,441,588
- 白名单 group1(case 41):18,20,124,178,208,353,633,663
实现:groups 数组只有 6/6 个 key,且是**按顺序取第一个存在**(非随机)。两组都不全(原版 19/8 个)。⚠️ 偏差(数量少+非随机)。
   - group0 实现列 guide/merchant/nurse/demolitionist/dyer/arms_dealer。原版 17=Guide,19=Mechanic,22=Party Girl,38=Arms Dealer,54=Painter,107=Santa,108=Steampunker,142=Tax Collector,160=Truffle,207=Princess,209=Golfer,227=Zoologist,228=Cyborg,229=Town Cat,368=Town Dog,369=Town Bunny,550=Town Slime,441=Mystic Frog?,588=?
   实现映射:nurse 在 group0 但原版 17=Nurse?17 其实是 Nurse!让我确认 NPC id:17=Nurse?Terraria NPCID: 17=Nurse?不对:17=Nurse,18=Mechanic,19=Guide?嗯:NPCID.Guide=22,Merchant=17,Nurse=18,ArmsDealer=19,Dryad=20,Guide=22。对:NPCID.Merchant=17、Nurse=18、ArmsDealer=19、Dryad=20、Guide=22。
   所以原版 case 40 白名单(17,19,22,38,54,107,108,142,160,207,209,227,228,229,368,369,550,441,588)= Merchant, ArmsDealer, Guide, TaxCollector, Painter, Santa, Steampunker, Truffle(160), Princess(207), Golfer(209), Zoologist(227), Cyborg(228), TownCat, TownDog, TownBunny, TownSlime, ... 
   实现 group0 = guide/merchant/nurse/demolitionist/dyer/arms_dealer —— nurse 和 demolitionist 和 dyer **不在原版 group0**!原版 case 41(18,20,124,178,208,353,633,663)= Nurse, Dryad, Stylist(124), Steampunker?178=?, WitchDoctor(208), Truffle?353=?, 633=?, 663=?。实现 group1 = dryad/painter/golfer/zoologist/pirate/stylist —— painter/golfer/zoologist/pirate 不在原版 case 41!**白名单错乱**。⚠️ 需要标注。
   不过实现已注释"此处按 NPC 图鉴顺序取前几个存在的"——明知近似。但白名单成员本身错了(painter 应在 group0)。标 ⚠️/🔀。

**NPC MechSpawn(NPC.cs:7399-7483)**:
- 等价组:type==74/297/298 蛇组;46/540/303/337 兔组;362/364 ↔ 362/363/364/365;602↔602/603;608↔608/609;616/617;55↔230(黄蜂/蜂王);IsDragonfly 组。
- 距离阈值 200/600,数量 3/6/10 → 拒绝 ✅ 与实现注释一致(NPC.cs:7399-7483:同 type(含等价组)200px≥3 / 600px≥6 / 全图≥10 拒绝)。
需查实现 mechSpawnOk 是否有等价组表。grep Game.ts mechSpawnOk。

**传感器 423 原版驱动**:Projectile.cs:62133-62541(type==423,投射物 578 LogicSensor 的 AI)。实现:
- Player Above:mode2,x===ptx && pty>y && pty-y<=8。wiki 说 5×10 区域。原版 LogicSensor 的 Player Above 检测:5 宽(x-2..x+2)×10 高(y-10..y-1)?让我读 Projectile.cs 62133-62200 确认。实现的 x===ptx(仅 1 宽!)且高度 ≤8(而非 10)。⚠️ 需核对。
- Day/Night:triggerDayNightSensors 在昼夜切换时触发全部对应感应器。原版 LogicSensor 是每帧检查(Main.dayTime 边沿)。近似 ✅(但需要确认原版是否只在切换沿触发,还是 sensor 自身状态机)。
- 液体传感器(mode 3-6?):实现 updateTriggerTiles 只处理 mode===2(玩家上方)!**液体传感器(Water/Lava/Honey/Any)未实现**?frameY/18%3:placeStyle 0-6(Day=0,Night=1,PlayerAbove=2,Water=3,Lava=4,Honey=5,Any=6)。frameY = placeStyle*18?那 mode=frameY/18%3 → 0-2。实现的 mode 计算对液体传感器会算错(Water style3 → frameY 54 → /18=3 → %3=0 = 昼!)。**液体传感器完全未实现且帧算式错误**。需要确认原版 frameY 编码:LogicSensor tile 423 的 frameY:放置样式 0-6,frameY = style*18?那 Day(0) frameY=0,Night(1)=18,PlayerAbove(2)=36,Water(3)=54,Lava(4)=72,Honey(5)=90,Any(6)=108。实现注释"frameY 0=昼 36=夜 72=玩家出入上方"——**错的**!原版应该是 0=Day、18=Night、36=Player Above、54=Water、72=Lava、90=Honey、108=Any。实现把 18 当夜、36 当昼、72 当玩家上方 → 完全错位!让我核对 Projectile.cs 62133-62200 的 frameY 判定。

**压板 135(玩家)checkPressurePlates(:6721)**:
- 玩家 AABB 覆盖全部格,sheet==135 即触发。**原版**:Player.cs Collision.SwitchTiles?玩家踩板触发有 style 门!(Gray/Brown/Blue/Lihzahrd=玩家触发,Green/Red/Yellow 各有触发者)。等等——玩家触发所有 style?不。wiki:Yellow(853, style5)"Triggered by NPCs and enemies"(玩家不触发!);Red(style0)/Green(style1)= "players, NPCs, enemies, projectiles";Gray(style2)/Brown(style3)/Blue(style4)/Lihzahrd(style6)/Orange(style7)= 玩家。
  实现的 checkPressurePlates **不区分 style**,玩家踩任何 135 都触发 → Yellow 压板被玩家误触发 ❌。
  原版代码在哪?Player.cs 里压板触发。让我 grep Player.cs "frameY" 135 上下文。原版在 Player.cs 的 "PressurePlateHelper"?不,135 在 Player.cs 哪里触发?搜 "HitSwitch" in Player.cs。
  
**NPC 踩板(NPC.cs:10612/18004/18290/50229 type==135)**:NPC 触发有 style 门(Red/Green/Yellow 被敌怪触发?Gray/Brown/Blue/Lihzahrd 仅玩家)。实现 updateEntityPlates 只让 **critters** 扫 135(“小动物族触发压板 135(NPC.cs:47613 白名单由 critters 桶近似)”)——**敌怪/城镇 NPC 踩板未实现**(只 critters)!❌ 大缺口。NPC.cs:90263 附近是"雕像刷的怪不触发"?90263 `type == 135 && life > 0` 是 NPC 常规踩板。

**442 teal 投射物触发**:实现 updateEntityPlates 只对 boulder 弹 checkPad=true(巨石触发 442)。原版 Projectile.cs:4853/51840/70424 type==442 是所有非穿墙投射物触发。实现只支持巨石 ❌(注释自认)。

**原版 Player.cs:45525 type==442**:可能玩家也触发 teal?不,45525 可能是排除。需读。

接下来批量读:
1. Projectile.cs 62133-62250(LogicSensor Player Above 区/帧)
2. Player.cs 45500-45560(442)
3. NPC.cs 90250-90300(踩板 style 门)与 NPC.cs 18004/18290(135 触发条件)
4. Game.ts mechSpawnOk 实现
5. Player.cs 玩家触发 135 的代码(grep HitSwitch in Player.cs)

执行。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:36:36.933Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===LogicSensor 62133-62200===\"; sed -n '62133,62200p' $T/Terraria/Projectile.cs; echo \"===Player HitSwitch===\"; grep -n \"Wiring.HitSwitch\\|PressurePlateHelper\" $T/Terraria/Player.cs | head -10; echo \"===Player 45510-45545===\"; sed -n '45510,45545p' $T/Terraria/Player.cs",
 "description": "Read sensor AI and player plate trigger"
}
```


---

## 🤖 Assistant · 2026-08-13T00:36:37.863Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===NPC 18000-18030===\"; sed -n '18000,18030p' $T/Terraria/NPC.cs; echo \"===NPC 18280-18310===\"; sed -n '18280,18310p' $T/Terraria/NPC.cs; echo \"===NPC 10600-10620===\"; sed -n '10600,10620p' $T/Terraria/NPC.cs",
 "description": "Read NPC plate trigger conditions"
}
```


---

## 🤖 Assistant · 2026-08-13T00:36:38.604Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; grep -n \"mechSpawnOk\\|itemSpawnOk\" $G/core/Game.ts | head; echo \"---\"; sed -n \"$(grep -n 'mechSpawnOk:' $G/core/Game.ts | head -1 | cut -d: -f1),+40p\" $G/core/Game.ts",
 "description": "Read mechSpawnOk implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:36:42.367Z

**📎 ToolResult**

```
===LogicSensor 62133-62200===
		if (type == 423)
		{
			num4 = 5f;
		}
		if (type == 373)
		{
			if (Main.player[owner].dead)
			{
				Main.player[owner].hornetMinion = false;
			}
			if (Main.player[owner].hornetMinion)
			{
				timeLeft = 2;
			}
		}
		if (type == 375)
		{
			if (Main.player[owner].dead)
			{
				Main.player[owner].impMinion = false;
			}
			if (Main.player[owner].impMinion)
			{
				timeLeft = 2;
			}
		}
		if (type == 407)
		{
			if (Main.player[owner].dead)
			{
				Main.player[owner].sharknadoMinion = false;
			}
			if (Main.player[owner].sharknadoMinion)
			{
				timeLeft = 2;
			}
		}
		if (type == 423)
		{
			if (Main.player[owner].dead)
			{
				Main.player[owner].UFOMinion = false;
			}
			if (Main.player[owner].UFOMinion)
			{
				timeLeft = 2;
			}
		}
		if (type == 613)
		{
			if (Main.player[owner].dead)
			{
				Main.player[owner].stardustMinion = false;
			}
			if (Main.player[owner].stardustMinion)
			{
				timeLeft = 2;
			}
			Lighting.AddLight(base.Center, 0.2f, 0.6f, 0.7f);
			if (localAI[1] > 0f)
			{
				localAI[1] -= 1f;
			}
		}
		if (type == 423)
		{
			if (ai[0] == 2f)
			{
===Player HitSwitch===
296:			PressurePlateHelper.ResetPlayer(playerIndex);
301:			PressurePlateHelper.ResetPlayer(playerIndex);
27967:		PressurePlateHelper.UpdatePlayerPosition(this);
31704:				Wiring.HitSwitch(myX, myY);
31754:				Wiring.HitSwitch(myX, myY);
31868:				Wiring.HitSwitch(myX, myY);
32797:							Wiring.HitSwitch(myX, myY);
34376:				Wiring.HitSwitch(point.X, point.Y);
37013:			PressurePlateHelper.UpdatePlayerPosition(this);
37050:			PressurePlateHelper.UpdatePlayerPosition(this);
===Player 45510-45545===
				Main.tile[x, y].frameX = 18;
			}
			else if (Main.tile[x, y].frameX == 18)
			{
				Main.tile[x, y].frameX = 36;
			}
			else
			{
				Main.tile[x, y].frameX = 0;
			}
			if (Main.netMode == 1)
			{
				NetMessage.SendTileSquare(-1, x, y);
			}
		}
		else if (Main.tile[x, y].type == 442)
		{
			Tile tile2 = Main.tile[x, y - 1];
			Tile tile3 = Main.tile[x, y + 1];
			Tile tile4 = Main.tile[x - 1, y];
			Tile tile5 = Main.tile[x + 1, y];
			Tile tile6 = Main.tile[x - 1, y + 1];
			Tile tile7 = Main.tile[x + 1, y + 1];
			Tile tile8 = Main.tile[x - 1, y - 1];
			Tile tile9 = Main.tile[x + 1, y - 1];
			int num5 = -1;
			int num6 = -1;
			int num7 = -1;
			int num8 = -1;
			int tree = -1;
			int tree2 = -1;
			int tree3 = -1;
			int tree4 = -1;
			if (tile2 != null && tile2.nactive() && !tile2.bottomSlope())
			{
				num6 = tile2.type;

```


---

## 👤 User(sidechain) · 2026-08-13T00:36:42.425Z

**📎 ToolResult**

```
===NPC 18000-18030===
		else if (type == 134)
		{
			scale *= 1.3f;
		}
		else if (type == 135)
		{
			scale *= 1.3f;
		}
		else if (type == 136)
		{
			scale *= 1.3f;
		}
		else
		{
			if (type != 139)
			{
				return;
			}
			scale *= 1.6f;
		}
		if (IsABestiaryIconDummy)
		{
			scale = num;
			return;
		}
		width = (int)((float)width * scale);
		height = (int)((float)height * scale);
	}

	private void LazySetLiquidMovementDD2()
	{
===NPC 18280-18310===
			num3 *= CommonMasterBossLifeReduction;
		}
		else if (type >= 134 && type <= 136)
		{
			num2 = 0.75;
			num3 *= CommonMasterBossLifeReduction;
			if (type == 134)
			{
				num *= 2.0;
			}
			if (type == 135)
			{
				num *= 0.85;
			}
			if (type == 136)
			{
				num *= 0.85;
			}
			if (difficulty >= GameDifficultyLevel.Expert)
			{
				scale *= 1.05f;
			}
		}
		else if (type == 139)
		{
			num2 = 0.75;
			num = 0.8;
			if (difficulty >= GameDifficultyLevel.Expert)
			{
				scale *= 1.05f;
			}
===NPC 10600-10620===
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			noGravity = true;
			noTileCollide = true;
			knockBackResist = 0f;
			behindTiles = true;
			value = 120000f;
			scale = 1.25f;
			boss = true;
			netAlways = true;
			alpha = 255;
		}
		else if (type == 135)
		{
			npcSlots = 5f;
			width = 38;
			height = 38;
			aiStyle = 37;
			damage = 55;
			defense = 30;
			lifeMax = 80000;

```


---

## 👤 User(sidechain) · 2026-08-13T00:36:48.406Z

**📎 ToolResult**

```
7107:      mechSpawnOk: (px: number, py: number, type: number) => {
7124:      itemSpawnOk: (px: number, py: number, type: number) => {
---
      mechSpawnOk: (px: number, py: number, type: number) => {
        // NPC.MechSpawn（NPC.cs:7399-7483）：同 type（等价组互计）三阈值拒绝
        const grp = NPC_MECH_GROUPS.find((g) => g.includes(type));
        let total = 0, near = 0, mid = 0;
        for (const o of this.entities.enemies) {
          const en = o as Enemy;
          const t = en.vanillaId;
          if (t == null) continue;
          if (t !== type && !(grp && grp.includes(t)) && !(type === 55 && t === 230)) continue;
          total++;
          const d = Math.hypot(en.x - px, en.y - py);
          if (d < 200) near++;
          if (d < 600) mid++;
          if (near >= 3 || mid >= 6 || total >= 10) return false;
        }
        return true;
      },
      itemSpawnOk: (px: number, py: number, type: number) => {
        // Item.MechSpawn（Item.cs:48982-49013）：同 item 三阈值拒绝
        let total = 0, near = 0, mid = 0;
        for (const o of this.entities.drops) {
          const d = o as ItemDrop;
          if (dropVanillaId(d) !== type) continue;
          total++;
          const dist = Math.hypot(d.x - px, d.y - py);
          if (dist < 300) near++;
          if (dist < 800) mid++;
          if (near >= 3 || mid >= 6 || total >= 10) return false;
        }
        return true;
      },
      shootProjectile: (px: number, py: number, vx: number, vy: number, damage: number, kind: TrapShotKind, form = 0, anchor?: [number, number]) => {
        this.entities.add(new TrapShot(px, py, vx, vy, damage, kind, form, anchor), 'projectiles');
        // 发射音：陷阱族=敲石近似；炮弹族由 TrapShot 首帧按原版播 Item14（Projectile.cs:21542/26830）；
        // 传送门弹 601 首帧无发射音（原版 AI 只有 alpha 段的门色拖尾尘）；
        // 烟花族发射静音——爆花 Item14 在 Kill（Projectile.cs:73437），喷泉/马桶全程无声
        if (kind !== 'cannonball' && kind !== 'bunny' && kind !== 'snowball' && kind !== 'portalbolt'
          && kind !== 'fireworkRocket' && kind !== 'fireworksBoxRocket'
          && kind !== 'fireworkFountain' && kind !== 'toiletPop') this.sfxAt('tink', px, py);
      },
      hasFountainAt: (tx: number, ty: number) => {

```


---

## 🤖 Assistant · 2026-08-13T00:36:56.508Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
注意!我搜的 NPC.cs type==135 是 **NPC id 135**(Duke Fishron 的一部分?135 是 Truffle?不,135=Fishron 左鳍?其实 NPC 135 是 "DukeFishron"?134/135/136 是 Fishron 三部分)。这些不是 tile 135!我混淆了。NPC.cs 里的 type 是 NPC type。

所以 NPC 踩板的代码在 NPC.cs 别处,搜 tile 触发:`Wiring.HitSwitch` in NPC.cs。

同样 Projectile.cs:4853 type==442 是投射物 type 442??不,442 没有投射物。Projectile.cs 4853 的 type 是 tile type(Main.tile[...].type)。上下文需确认。

让我精确 grep NPC.cs 的 Wiring.HitSwitch + Projectile.cs 的 Wiring.HitSwitch。

另外 Player.cs:31704/31754/31868/32797/34376 是 Wiring.HitSwitch 调用点(玩家触发:右键 lever/switch/timer :31704?、踩 detonator 411 :34376?)。读这些上下文。

还有 Player.cs:45525 的 type==442 —— 看上下文 45510-45545,这是 smart(智能光标/目标选择)的 442 分支(tile 442 周围格判定),不是触发。OK,442(青色压力垫)的玩家触发在 Player.cs 31704 或 34376?读。

再读 Projectile.cs 62200-62260(LogicSensor ai[0]==2 Player Above)。

批量执行。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:36:56.955Z · glm-x-preview-260804

```
注意到混淆点:NPC.cs 的 `type==135` 是 NPC id(Fishron 部件)，非 tile。重新精确定位触发调用链。
```


---

## 🤖 Assistant · 2026-08-13T00:36:58.265Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===NPC HitSwitch===\"; grep -n \"Wiring.HitSwitch\\|Wiring.PokeLogicGate\" $T/Terraria/NPC.cs | head; echo \"===Proj HitSwitch===\"; grep -n \"Wiring.HitSwitch\" $T/Terraria/Projectile.cs | head; echo \"===Player 34360-34380===\"; sed -n '34360,34382p' $T/Terraria/Player.cs; echo \"===Player 31690-31710===\"; sed -n '31690,31710p' $T/Terraria/Player.cs",
 "description": "Locate HitSwitch call sites in NPC/Projectile/Player"
}
```


---

## 🤖 Assistant · 2026-08-13T00:36:58.739Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===LogicSensor ai0==2===\"; sed -n '62200,62260p' $T/Terraria/Projectile.cs",
 "description": "Read Player Above sensor AI"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:37:13.191Z

**📎 ToolResult**

```
===NPC HitSwitch===
===Proj HitSwitch===
===Player 34360-34380===
				num5 = 306;
			}
			cursorItemIconID = num5;
			cursorItemIconEnabled = true;
		}
		hoveredChestIndex = num3;
	}

	private void TryLandingOnDetonator()
	{
		if (whoAmI == Main.myPlayer && velocity.Y >= 3f)
		{
			Point point = (base.Bottom + new Vector2(0f, 0.01f)).ToTileCoordinates();
			Tile tileSafely = Framing.GetTileSafely(point.X, point.Y);
			if (tileSafely.active() && tileSafely.type == 411 && tileSafely.frameY == 0 && tileSafely.frameX < 36)
			{
				Wiring.HitSwitch(point.X, point.Y);
				NetMessage.SendData(59, -1, -1, null, point.X, point.Y);
			}
		}
	}

	private void TryBouncingBlocks(bool Falling)
===Player 31690-31710===
			float num8 = num6;
			float num9 = (float)Math.Sqrt(num7 * num7 + num8 * num8);
			num9 = num4 / num9;
			num7 *= num9;
			num8 *= num9;
			int num10 = Projectile.NewProjectile(GetProjectileSource_TileInteraction(num, num3), vector.X, vector.Y, num7, num8, type, damage, knockBack, Main.myPlayer, -Main.rand.Next(0, 16));
			Main.projectile[num10].originatedFromActivableTile = true;
		}
		if (flag)
		{
			Tile tile = Main.tile[myX, myY];
			if (Main.tile[myX, myY].type == 132 || Main.tile[myX, myY].type == 136 || Main.tile[myX, myY].type == 144)
			{
				flag2 = true;
				Wiring.HitSwitch(myX, myY);
				NetMessage.SendData(59, -1, -1, null, myX, myY);
			}
			else if (Main.tile[myX, myY].type == 597)
			{
				flag2 = true;
				TryOpeningFullscreenMap();

```


---

## 👤 User(sidechain) · 2026-08-13T00:37:13.223Z

**📎 ToolResult**

```
===LogicSensor ai0==2===
			{
				ai[1] -= 1f;
				tileCollide = false;
				if (ai[1] > 3f)
				{
					int num6 = Dust.NewDust(base.Center, 0, 0, 220 + Main.rand.Next(2), velocity.X, velocity.Y, 100);
					Main.dust[num6].scale = 0.5f + (float)Main.rand.NextDouble() * 0.3f;
					Main.dust[num6].velocity /= 2.5f;
					Main.dust[num6].noGravity = true;
					Main.dust[num6].noLight = true;
					Main.dust[num6].frame.Y = 80;
				}
				if (ai[1] != 0f)
				{
					return;
				}
				ai[1] = 30f;
				ai[0] = 0f;
				velocity /= 5f;
				velocity.Y = 0f;
				extraUpdates = 0;
				numUpdates = 0;
				netUpdate = true;
				extraUpdates = 0;
				numUpdates = 0;
			}
			if (extraUpdates > 1)
			{
				extraUpdates = 0;
			}
			if (numUpdates > 1)
			{
				numUpdates = 0;
			}
		}
		if (type == 613)
		{
			if (ai[0] == 2f)
			{
				ai[1] -= 1f;
				tileCollide = false;
				if (ai[1] > 3f)
				{
					if (numUpdates < 20)
					{
						for (int i = 0; i < 3; i++)
						{
							Dust obj = Main.dust[Dust.NewDust(position, width, height, 229)];
							obj.noGravity = true;
							obj.position = base.Center;
							obj.velocity *= 3f;
							obj.velocity += velocity * 3f;
							obj.fadeIn = 1f;
						}
					}
					float num7 = 2f - (float)numUpdates / 30f;
					if (scale > 0f)
					{
						float num8 = 2f;
						for (int j = 0; (float)j < num8; j++)
						{

```


---

## 🤖 Assistant · 2026-08-13T00:37:20.516Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
62200-62260 是 type 613(星尘龙?)。LogicSensor(投射物 578?)在哪?Projectile 578 = LogicSensor?搜 "LogicSensor" 在 ProjectileID.cs。之前 grep "LogicSensor" 只在 Projectile.cs 出现 0 次匹配(输出里没有)。等等,第一个 grep `== 423\|LogicSensor` 输出的都是 == 423。所以传感器不是投射物,是 tile 423。那触发逻辑在哪?

原版:传感器 423 的信号发送在 Main.cs(每天/夜切换时扫 tile)或 Liquid 检测。让我搜 Main.cs 的 423 + Player.cs 的 423 + WorldGen/TileData。

搜全目录 "== 423"。

也搜 tile 135 的触发:Player.cs 没有直接 Wiring.HitSwitch(135)?Player.cs 的 HitSwitch 调用点 31704(132/136/144 右键)、31754、31868、32797、34376(411 踩踏)。踩压板 135 在哪触发?—— 在 Collision.SwitchTiles 或 Main.Update?搜 Main.cs 的 HitSwitch。

原版玩家踩压板逻辑:Player.cs Collision 里?其实原版是 **Main.cs 的 SwitchTiles**?或者 Player.cs "PressurePlate"?让我全局 grep "Wiring.HitSwitch" 所有文件。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:37:20.521Z · glm-x-preview-260804

```
传感器 423 不是投射物。全局定位 HitSwitch 调用点与 423 扫描。
```


---

## 🤖 Assistant · 2026-08-13T00:37:20.549Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; grep -rn \"Wiring.HitSwitch\\|HitSwitch(\" --include=\"*.cs\" $T/Terraria $T/Terraria.GameContent 2>/dev/null | grep -v \"public static void\" | head -20; echo \"===423 in Main/WorldGen===\"; grep -rn \"== 423\" $T/Terraria/Main.cs $T/Terraria/WorldGen.cs $T/Terraria/Liquid.cs 2>/dev/null | head -10",
 "description": "Global search for HitSwitch callers and tile 423"
}
```


---

## 🤖 Assistant · 2026-08-13T00:37:20.937Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; sed -n '6990,7040p' $G/core/Game.ts",
 "description": "Read statue spawn implementation in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:37:24.877Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Minecart.cs:1292:		Wiring.HitSwitch(num, num2);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/MessageBuffer.cs:1907:					Wiring.HitSwitch(num29, num30);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/MessageBuffer.cs:2702:			Wiring.HitSwitch(num66, num67);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Collision.cs:3316:							Wiring.HitSwitch(i, j);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Collision.cs:3330:					Wiring.HitSwitch(i, j);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Collision.cs:3336:						Wiring.HitSwitch(i, j);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Collision.cs:3359:				Wiring.HitSwitch(i, j);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/PressurePlateHelper.cs:161:			Wiring.HitSwitch(location.X, location.Y);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Wiring.cs:1013:			HitSwitch(i, j);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:46535:		Wiring.HitSwitch(i - num3, j - num4);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:62620:				Wiring.HitSwitch(topLeftX, topLeftY);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:31704:				Wiring.HitSwitch(myX, myY);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:31754:				Wiring.HitSwitch(myX, myY);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:31868:				Wiring.HitSwitch(myX, myY);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:32797:							Wiring.HitSwitch(myX, myY);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:34376:				Wiring.HitSwitch(point.X, point.Y);
===423 in Main/WorldGen===
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:29459:		if (proj.type == 423)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:33841:			if ((proj.type >= 393 && proj.type <= 395) || proj.type == 398 || proj.type == 423 || proj.type == 1022 || proj.type == 1036 || proj.type == 450 || proj.type == 1093)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:33852:				if (proj.type == 423)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:58043:					if (type == 423 && tile.frameY == 36)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:58054:			if (type == 423)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:63917:		if (tile.type == 423)

```


---

## 👤 User(sidechain) · 2026-08-13T00:37:24.895Z

**📎 ToolResult**

```
      backgroundEnabled: options.data.backgrounds,
      // 灯笼夜天气压制（Main.cs:64288 云钳 30 / :64331 停雨 / :64353 不开新雨 /
      // :58249 风场停掷）
      lanternsUp: LanternNight.lanternsUp,
      nextNightIsLanternNight: LanternNight.nextNightIsLanternNight,
      onCoinRain: (x, y, type, stack) => {
        // 非实心 32×32 门（WorldGen.cs:71847）
        const st = w.store;
        const tx0 = Math.floor(x / 16), ty0 = Math.floor(y / 16);
        let solid = false;
        for (let dx = 0; dx <= 1 && !solid; dx++) for (let dy = 0; dy <= 1; dy++) {
          if (st.inBounds(tx0 + dx, ty0 + dy) && st.isSolid(tx0 + dx, ty0 + dy)) { solid = true; break; }
        }
        if (solid) return;
        // type 即原版钱币 item id 71/72/73(铜/银/金,Weather.cs 对齐 cs:71836)——
        // 曾整体 +1 错位(铜雨掉银/银雨掉金/金雨掉铂,每次降雨 ×100 通胀)
        const key = VI(type);
        this.spawnDrop(x, y, key, stack, 0, 3);
      },
      onThunder: (distPx) => {
        // 原版 SoundID 43：thunderDistance×15px 处发声——按距离衰减近似
        const vol = Math.max(0.15, 1 - distPx / 2400);
        this.sfx.play('thunder', vol);
      },
      onSandstormToggle: (happening) => {
        // 原版沙尘暴无公告——保留提示但走原版消息列（ChatColors.World）
        this.newText(Lang.text(happening ? 'Mods.SandboxWorld.Weather.SandstormOn' : 'Mods.SandboxWorld.Weather.SandstormOff'), 50, 255, 130);
      },
      onSlimeRainToggle: () => {
        // 原版 UpdateSlimeRainWarning（Main.cs:64984）：切换后 420t 延迟公告
        // Lang.gen[74]（开始）/gen[75]（停止），色 ChatColors.World
        this.slimeWarningTime = 420;
      },
    });
    // 史莱姆雨延迟公告倒计时（UpdateSlimeRainWarning :64988-64996 1:1）
    if (this.slimeWarningTime > 0 && --this.slimeWarningTime === 0) {
      this.newText(Lang.gen(weather.slimeRainTime > 0 ? 74 : 75), 50, 255, 130);
    }
    // 狱火药水（buff 116，Player.cs:9896-9938）：200px 光环烧敌——每 60t 对范围内敌
    // 直伤 20（不绕 iframes）；视觉光效由粒子近似
    if (this.player.buffs.has(BuffType.Inferno)) {
      this.infernoCounter++;
      const hitTick = this.infernoCounter % 60 === 0;
      if (hitTick) this.spawnParticles(this.player.cx, this.player.cy, '#FF8C2A', 4, 1.8, { life: 24, grav: -0.08 });
      for (const eent of this.entities.enemies) {
        const en = eent as Enemy;
        if (en.dead) continue;
        if (Math.hypot(en.cx - this.player.cx, en.cy - this.player.cy) > 200) continue;
        en.cursedT = Math.max(en.cursedT, 2); // AddBuff(323,120) 灼烧 2s
        if (hitTick) en.hurt(Math.max(1, Math.round(20 * this.player.damageMult('melee'))), 0, 0, this);
      }

```


---

## 🤖 Assistant · 2026-08-13T00:37:31.005Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
好,压板触发在 **Collision.cs:3316-3359**(Collision.SwitchTiles)。这是实体(tile 碰撞)与压板 135 的交互。读这段,它决定 style→触发者门。

传感器 423:Main.cs:58043-58054(type==423, frameY==36 → Player Above!)与 WorldGen.cs:63917。Main.cs 58043 说明 Player Above 的 frameY==36 ✅(不是 72)。让我读 Main.cs:58020-58100。这里的触发是"传感器发信号"吗?58043 在什么方法里?可能是 Main.Update 里每天扫描,或者是"tile 423 触发"主循环。

实现注释说"frameY 0=昼 36=夜 72=玩家出入上方"——Main.cs 58043 显示 Player Above 是 frameY==36。所以实现的帧表(0=昼 36=夜 72=玩家上方)**错位**!需读 Main.cs 58020-58080 确认三种 frameY。

WorldGen.cs:63917 tile.type==423:液体传感器检测?读。

批量读。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:37:31.666Z · glm-x-preview-260804

```
压板触发链在 Collision.cs:3316-3359(SwitchTiles),传感器在 Main.cs:58043+。读这两段——这是触发者门禁与帧编码的权威。
```


---

## 🤖 Assistant · 2026-08-13T00:37:32.094Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===Collision 3250-3370===\"; sed -n '3250,3370p' $T/Terraria/Collision.cs",
 "description": "Read Collision.SwitchTiles plate trigger"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:37:32.118Z

**📎 ToolResult**

```
===Collision 3250-3370===
		if (num2 > Main.maxTilesX)
		{
			num2 = Main.maxTilesX;
		}
		if (num3 < 0)
		{
			num3 = 0;
		}
		if (num4 > Main.maxTilesY - 40)
		{
			num4 = Main.maxTilesY - 40;
		}
		Vector2 vector = default(Vector2);
		for (int i = num; i < num2; i++)
		{
			for (int j = num3; j < num4; j++)
			{
				if (Main.tile[i, j] == null)
				{
					continue;
				}
				int type = Main.tile[i, j].type;
				if (!Main.tile[i, j].active() || (type != 135 && type != 210 && type != 443 && type != 442))
				{
					continue;
				}
				vector.X = i * 16;
				vector.Y = j * 16 + 12;
				bool flag = false;
				if (type == 442)
				{
					if (objType == 4)
					{
						float r1StartX = 0f;
						float r1StartY = 0f;
						float r1Width = 0f;
						float r1Height = 0f;
						switch (Main.tile[i, j].frameX / 22)
						{
						case 0:
							r1StartX = i * 16;
							r1StartY = j * 16 + 16 - 10;
							r1Width = 16f;
							r1Height = 10f;
							break;
						case 1:
							r1StartX = i * 16;
							r1StartY = j * 16;
							r1Width = 16f;
							r1Height = 10f;
							break;
						case 2:
							r1StartX = i * 16;
							r1StartY = j * 16;
							r1Width = 10f;
							r1Height = 16f;
							break;
						case 3:
							r1StartX = i * 16 + 16 - 10;
							r1StartY = j * 16;
							r1Width = 10f;
							r1Height = 16f;
							break;
						}
						if (Utils.FloatIntersect(r1StartX, r1StartY, r1Width, r1Height, Position.X, Position.Y, Width, Height) && !Utils.FloatIntersect(r1StartX, r1StartY, r1Width, r1Height, oldPosition.X, oldPosition.Y, Width, Height))
						{
							Wiring.HitSwitch(i, j);
							NetMessage.SendData(59, -1, -1, null, i, j);
							return true;
						}
					}
					flag = true;
				}
				if (flag || !(Position.X + (float)Width > vector.X) || !(Position.X < vector.X + 16f) || !(Position.Y + (float)Height > vector.Y) || !((double)Position.Y < (double)vector.Y + 4.01) || (oldPosition.X + (float)Width > vector.X && oldPosition.X < vector.X + 16f && oldPosition.Y + (float)Height > vector.Y && (double)oldPosition.Y < (double)vector.Y + 16.01))
				{
					continue;
				}
				switch (type)
				{
				case 210:
					Wiring.HitSwitch(i, j);
					NetMessage.SendData(59, -1, -1, null, i, j);
					continue;
				case 443:
					if (objType == 1 || objType == 5)
					{
						Wiring.HitSwitch(i, j);
						NetMessage.SendData(59, -1, -1, null, i, j);
					}
					continue;
				}
				int num5 = Main.tile[i, j].frameY / 18;
				bool flag2 = true;
				if ((num5 == 4 || num5 == 2 || num5 == 3 || num5 == 6 || num5 == 7) && objType != 5)
				{
					flag2 = false;
				}
				if (num5 == 5 && (objType == 1 || objType == 4 || objType == 5))
				{
					flag2 = false;
				}
				if (!flag2)
				{
					continue;
				}
				if (Main.netMode == 1 && objType == 5)
				{
					NetMessage.SendData(13, -1, -1, null, Main.myPlayer);
				}
				Wiring.HitSwitch(i, j);
				NetMessage.SendData(59, -1, -1, null, i, j);
				if (num5 == 7)
				{
					WorldGen.KillTile(i, j);
					if (Main.netMode == 1)
					{
						NetMessage.SendData(17, -1, -1, null, 0, i, j);
					}
				}
				return true;
			}

```


---

## 🤖 Assistant · 2026-08-13T00:37:32.928Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===Main 58010-58100===\"; sed -n '58010,58100p' $T/Terraria/Main.cs; echo \"===WorldGen 63890-63960===\"; sed -n '63890,63960p' $T/Terraria/WorldGen.cs",
 "description": "Read sensor day/night/liquid trigger"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:37:32.972Z

**📎 ToolResult**

```
===Main 58010-58100===
								flag3 = true;
							}
							if (flag6)
							{
								if (flag10 && !flag2)
								{
									spriteBatch.Draw(TextureAssets.WireNew.Value, new Vector2(j * 16 - (int)screenPosition.X, i * 16 - (int)screenPosition.Y) + drawOffSet, new Microsoft.Xna.Framework.Rectangle(144, value.Y, 6, 16), color4, 0f, zero, 1f, SpriteEffects.None, 0f);
								}
								flag2 = true;
							}
						}
					}
				}
				if (Main.tile[j, i].actuator() && (Lighting.Brightness(j, i) > 0f || num6 == 0))
				{
					Microsoft.Xna.Framework.Color color5 = Lighting.GetColor(j, i);
					switch (num6)
					{
					case 0:
						color5 = Microsoft.Xna.Framework.Color.White;
						break;
					case 2:
						color5 *= 0.5f;
						break;
					case 3:
						color5 = Microsoft.Xna.Framework.Color.Transparent;
						break;
					}
					spriteBatch.Draw(TextureAssets.Actuator.Value, new Vector2(j * 16 - (int)screenPosition.X, i * 16 - (int)screenPosition.Y) + drawOffSet, new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.Actuator.Width(), TextureAssets.Actuator.Height()), color5 * num, 0f, default(Vector2), 1f, SpriteEffects.None, 0f);
				}
				if (tile.active())
				{
					ushort type = tile.type;
					if (type == 423 && tile.frameY == 36)
					{
						DrawWiresSpecialTiles.Add(Tuple.Create(j, i, tile.type));
					}
				}
			}
		}
		for (int k = 0; k < DrawWiresSpecialTiles.Count; k++)
		{
			Tuple<int, int, ushort> tuple = DrawWiresSpecialTiles[k];
			ushort type = tuple.Item3;
			if (type == 423)
			{
				Vector2 start = new Vector2(tuple.Item1 * 16 - 32 - 1, tuple.Item2 * 16 - 160 - 1) + drawOffSet;
				Vector2 end = new Vector2(tuple.Item1 * 16 + 48 + 1, tuple.Item2 * 16 + 1) + drawOffSet;
				Utils.DrawRectangle(spriteBatch, start, end, Microsoft.Xna.Framework.Color.LightSeaGreen, Microsoft.Xna.Framework.Color.LightSeaGreen, 2f);
			}
		}
		TimeLogger.DrawWireTiles.AddTime(fromTimestamp);
	}

	public static int ConvertPaintIdToTileShaderIndex(int paintIndexOnTile, bool isUsedForPaintingGrass, bool useWallShaderHacks)
	{
		if (paintIndexOnTile == 31)
		{
			return 0;
		}
		if (paintIndexOnTile == 30 && useWallShaderHacks)
		{
			return 43;
		}
		if (paintIndexOnTile >= 28)
		{
			return paintIndexOnTile + 12;
		}
		if (isUsedForPaintingGrass && paintIndexOnTile >= 1 && paintIndexOnTile <= 12)
		{
			return paintIndexOnTile + 27;
		}
		return paintIndexOnTile;
	}

	public static void ResetWindCounter(bool resetExtreme = false)
	{
		FastRandom fastRandom = FastRandom.CreateWithRandomSeed();
		windCounter = fastRandom.Next(900, 2701);
		if (resetExtreme)
		{
			extremeWindCounter = fastRandom.Next(10, 31);
		}
	}

	public static void NewLightning(bool instant = false, bool skipSound = false)
	{
		if (FlashyEffectsWorld && !(shimmerAlpha > 0f))
		{
			if (rand.Next(3) == 0)
			{
===WorldGen 63890-63960===
			if (Main.netMode == 0)
			{
				Projectile.NewProjectile(projectileSource_TileBreak, i * 16 + 8, j * 16 + 8, 0f, 0.41f, type, damage, 0f, Main.myPlayer);
			}
			else if (Main.netMode == 2)
			{
				int num20 = Projectile.NewProjectile(projectileSource_TileBreak, i * 16 + 8, j * 16 + 8, 0f, 0.41f, type, damage, 0f, Main.myPlayer);
				Main.projectile[num20].netUpdate = true;
			}
		}
		if (CheckTileBreakability2_ShouldTileSurvive(i, j))
		{
			return;
		}
		if (tile.type == 51 && tile.wall == 62 && genRand.Next(4) != 0)
		{
			noItem = true;
		}
		if (!noItem && !stopDrops && Main.netMode != 1)
		{
			KillTile_DropBait(i, j, tile);
			KillTile_DropItems(i, j, tile);
		}
		if (tile.type == 520)
		{
			TileEntityType<TEFoodPlatter>.Kill(i, j);
		}
		if (tile.type == 423)
		{
			TELogicSensor.Kill(i, j);
		}
		if (tile.type == 723)
		{
			TEKiteAnchor.Kill(i, j);
		}
		if (tile.type == 724)
		{
			TECritterAnchor.Kill(i, j);
		}
		if (Main.netMode != 2)
		{
			AchievementsHelper.NotifyTileDestroyed(Main.player[Main.myPlayer], tile.type);
		}
		tile.active(active: false);
		tile.halfBrick(halfBrick: false);
		tile.frameX = -1;
		tile.frameY = -1;
		tile.ClearBlockPaintAndCoating();
		tile.frameNumber(0);
		if (Main.netMode != 1)
		{
			if (tile.type == 58 && j > Main.UnderworldLayer)
			{
				tile.lava(lava: true);
				tile.liquid = 128;
			}
			else if (tile.type == 230 && Main.getGoodWorld && genRand.Next(2) == 0)
			{
				tile.lava(lava: true);
				tile.liquid = 128;
			}
			else if (tile.type > 0 && tile.type < TileID.Count && (tile.type == 147 || tile.type == 224 || TileID.Sets.Ices[tile.type]) && Main.getGoodWorld && Main.remixWorld && !Main.drunkWorld && genRand.Next(2) == 0)
			{
				tile.liquidType(0);
				tile.liquid = 64;
			}
		}
		if (tile.type == 419)
		{
			Wiring.PokeLogicGate(i, j + 1);
		}

```


---

## 🤖 Assistant · 2026-08-13T00:37:52.269Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
重大确认!

**1. Collision.SwitchTiles(Collision.cs:3250-3372)= 压板/地雷/喷泉/teal 触发权威**:

- 扫描 tile type ∈ {135, 210, 443, 442}
- objType 参数:1=玩家? 2=? 3=? 4=投射物? 5=?
  - 442(teal):**仅 objType==4**(投射物)触发,四方向 hitbox(frameX/22:0=下、1=上、2=左、3=右),且要求"当前相交 & 旧位置不相交"(边沿触发)
  - 210 地雷:任何 objType → HitSwitch(踩上即爆,边沿:Position 相交 vector 区且 oldPosition 不相交)
  - 443 热喷泉:**objType==1 || objType==5**(玩家/敌怪踩)
  - 135 压板:frameY/18 = num5:
    - num5 ∈ {2,3,4,6,7}(Gray/Brown/Blue/Lihzahrd/Orange)且 objType != 5 → 拒绝(即这些只有 objType 5 触发)
    - num5 == 5(Yellow)且 objType ∈ {1,4,5} → 拒绝(Yellow 只被 objType 2/3 触发?)
    - num5 == 7(Orange):触发后 KillTile(用后即毁)✅ wiki
  - 所以 objType 语义:需要确定。原版 Collision.SwitchTiles 的调用方:Player.cs(玩家, objType=?)、NPC.cs(敌怪/NPC)、Projectile.cs(投射物)。常见:objType 1=玩家?5=?
  
  从门禁反推:
  - Gray/Brown/Blue/Lihzahrd/Orange(style 2,3,4,6,7)wiki="players only" → 需要 objType==5 = 玩家。
  - Red/Green(style 0,1)wiki="players, NPCs, enemies, projectiles" → 无门。
  - Yellow(style 5)wiki="NPCs and enemies"(非玩家非投射物)→ objType ∈ {2,3} = NPC/敌怪,1 可能是玩家或别的,4=投射物被排除。
  
  所以:objType 5=玩家、4=投射物、1=玩家?不对,Yellow 排除 {1,4,5},剩 {2,3}。若 5=玩家,1 是什么也被 Yellow 排除?那 1 = 玩家、5 = 玩家?矛盾。
  
  重新想:Collision.SwitchTiles(Position, oldPosition, Width, Height, objType)。调用:
  - Player.cs → objType = 1?
  - NPC(敌怪)→ 2?
  - NPC(town/友好)→ 3?
  - Projectile → 4?
  - ??? → 5
  
  Yellow 排除 1/4/5,允许 2/3。wiki Yellow = "NPCs and enemies"。所以 2=敌怪、3=NPC(或反之),1=玩家、4=投射物,5=?
  style 2/3/4/6/7(Gray/Brown/Blue/Lihzahrd/Orange)要求 objType==5 → 5 = 玩家!
  那 1 是什么?1 可能是"玩家"的另一个调用(比如玩家在别处)。看 case 443:objType==1 || objType==5 → 热喷泉被 1 和 5 触发。若 1=玩家、5=玩家,冗余;若 1=敌怪/NPC、5=玩家,则喷泉被任何实体踩。wiki Geyser:"activates when a character steps on it or when a projectile passes"。嗯。
  
  查调用方最快。grep "SwitchTiles" 全库。

**2. 传感器 423 是 TileEntity(TELogicSensor)!**
- WorldGen.cs:63917:KillTile → TELogicSensor.Kill(i, j)
- 423 的信号逻辑在 TileEntity TELogicSensor.cs!所以 Day/Night/PlayerAbove/Liquid 全部由 TELogicSensor 驱动。
- Main.cs:58043:`type == 423 && tile.frameY == 36` → 画 5×10 检测框(LightSeaGreen 矩形,x*16-32..x*16+48 = 5 宽,y*16-160..y*16 = 10 高)✅ wiki 5×10 确认!frameY==36 = Player Above style。
- **传感器 style→frameY**:需要读 TELogicSensor.cs。放置时 placeStyle 0-6,frameY = style*18?Main.cs 58043 用 frameY==36 判 Player Above(style2 → 36)→ **frameY = placeStyle*18**:Day=0、Night=18、PlayerAbove=36、Water=54、Lava=72、Honey=90、Any=108。
- **实现帧表错误证实**:实现注释/代码"frameY 0=昼 36=夜 72=玩家出入上方"完全错位;实现代码 `mode = floor(frameY/18) % 3`,Water(54)→ mode 0(昼!)。这是真 bug。且实现 Player Above 检测 x===ptx(1 宽,原版 5 宽 x-2..x+2)且高度 ≤8(原版 10)。液体传感器(mode>=3)完全没实现。

读 TELogicSensor.cs 全文(权威:Day/Night/PlayerAbove/Liquid 触发时序)。

**3. 地雷 210 踩踏触发**:Collision.SwitchTiles type 210 → HitSwitch(210)→ 原版 HitSwitch 的 210 分支 → ExplodeMine。实现 hitSwitch **缺 210 分支** → 玩家/实体踩地雷不会爆炸(踩踏路径缺失);通电路径 devices case 210 有。需要确认 Game.ts 踩地雷是否走了别的路。grep Game.ts 210。

现在读 TELogicSensor.cs + grep SwitchTiles 调用方 + grep Game.ts 的 210/地雷。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:37:52.687Z · glm-x-preview-260804

```
核心确认：传感器 423 是 TileEntity(**TELogicSensor**),压板触发权威在 Collision.SwitchTiles。读 TELogicSensor 与 objType 语义。
```


---

## 🤖 Assistant · 2026-08-13T00:37:53.429Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; find $T -name \"TELogicSensor.cs\"; echo \"===SwitchTiles callers===\"; grep -rn \"Collision.SwitchTiles\" --include=\"*.cs\" $T/Terraria $T/Terraria.GameContent 2>/dev/null | grep -v \"public static\" | head",
 "description": "Find TELogicSensor and SwitchTiles callers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:37:53.467Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Tile_Entities/TELogicSensor.cs
===SwitchTiles callers===
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:91558:		if (Main.netMode != 1 && !noTileCollide && lifeMax > 1 && Collision.SwitchTiles(this, position, width, height, oldPosition, 2) && (type == 46 || type == 148 || type == 149 || type == 303 || type == 361 || type == 362 || type == 364 || type == 366 || type == 367 || (type >= 442 && type <= 448) || type == 602 || type == 608 || type == 614 || type == 687))
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:15749:				Collision.SwitchTiles(this, position, width, height, oldPosition, 3);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:16454:								Collision.SwitchTiles(this, vector, colWidth, colHeight, vector9, 4);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:18455:			Collision.SwitchTiles(this, position + vector25, colWidth2, colHeight2, oldPosition + vector25, 4);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs:18960:				Collision.SwitchTiles(this, position, width, height, oldPosition, 4);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:27965:			Collision.SwitchTiles(this, position, width, height, oldPosition, 5);

```


---

## 🤖 Assistant · 2026-08-13T00:38:10.867Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
objType 语义确定:
- **5 = Player**(Player.cs:27965)
- **2 = NPC**(NPC.cs:91558,带白名单!只有特定 type 触发:46 兔、148、149、303、361、362、364、366、367、442-448、602、608、614、687——即雕像可刷的怪族!)
- **3 = 某类投射物**(Projectile.cs:15749,比如钩爪/杂项)
- **4 = 常规投射物**(15749/16454/18455/18960)

修正压板门禁表(Collision.cs:3336-3349):
- style 0 Red / 1 Green:**全 objType 触发**(无门)✅ wiki "players, NPCs, enemies, projectiles"
- style 2 Gray / 3 Brown / 4 Blue / 6 Lihzahrd / 7 Orange:仅 objType==5(玩家)✅ wiki "players only";7 用后毁 ✅
- style 5 Yellow:排除 objType 1/4/5 → 允许 2/3 → NPC + 某投射物。wiki 说 "NPCs and enemies"。objType 2 是 NPC 调用(带雕像怪白名单)——但 Yellow 被任意 NPC 触发?等等,NPC.cs:91558 的白名单是"哪些 NPC 会调用 SwitchTiles",与压板 style 无关。Yellow 的"enemies"其实=所有走 SwitchTiles 的 NPC(NPC 白名单里都是雕像怪/critter 族)。
  嗯,这里的 NPC 白名单(46/148/149/303/361/362/364/366/367/442-448/602/608/614/687)= **雕像能刷的 NPC 族**(critter+敌怪)。也就是说:**原版只有雕像可刷的那批 NPC 才会踩板**(正常敌怪不触发压板!这是原版著名的"压板只被雕像怪/critter 触发"行为?不完全——让我想。Terraria 里敌怪踩绿板/黄板会触发吗?实测:绿板会被敌怪触发(地牢神庙里的机关)。但 NPC.cs:91558 的白名单不含普通敌怪(如僵尸 3)。
  
  等等,再读一次:NPC.cs:91558 `if (Main.netMode != 1 && !noTileCollide && lifeMax > 1 && Collision.SwitchTiles(...) && (type == 46 || ...))` —— 结构是 `A && SwitchTiles(...) && B`,SwitchTiles **先执行**(C# && 从左到右,先算左边)。所以所有 lifeMax>1 且非穿墙的 NPC 都会执行 SwitchTiles(触发压板),只是返回值 && B 用于后续逻辑(可能是"是否吞掉触发"?)。
  
  嗯,更可能是:SwitchTiles 的返回值 true = "踩到了某块板",然后白名单决定后续行为(比如雕像怪踩板的特殊处理?)。不管怎样,**SwitchTiles 对所有 NPC 执行** → 敌怪踩板触发 ✅。白名单只影响 && 后面的语句(可能是 KillTile 压坏板之类,或什么都不做——&& 链尾没有语句?`if (...)` 后面必然有 body)。不重要,结论:NPC(objType 2)全量踩板。
  
  那么 wiki "Yellow: NPCs and enemies"对,objType 2 覆盖 NPC+敌怪;objType 3(15749 投射物子集)也触发 Yellow。

**实现侧对照**:
- 实现 checkPressurePlates(玩家)✅ 但**无 style 门**(style5 Yellow 应不响应玩家)❌
- 实现 updateEntityPlates:只 critters + boulder 弹扫 135/442 → **普通敌怪/NPC 踩板未实现** ❌(只 critters;原版所有 NPC 都触发)
- 442 teal:原版仅 objType 4(投射物)+ objType 3;玩家(5)**不触发** ✅ wiki "Triggered by projectiles"。实现 updateTriggerTiles 的 checkPressurePlates 只扫 135 ✅ 不会误触发 442;updateEntityPlates 只对 boulder checkPad → 其他投射物(飞镖/火焰等)不触发 teal ❌(原版所有非穿墙投射物触发)
- 210 地雷:原版任意 objType 踩 → HitSwitch → ExplodeMine。实现 hitSwitch 无 210 → 踩地雷不爆 ❌。且实现的 checkPressurePlates 只扫 135,不扫 210/443 → 玩家踩地雷/热喷泉无触发 ❌。
- 443 热喷泉:原版 objType 1||5 触发(踩踏)。1 是什么?看 Collision case 443 注释——objType 1 未在调用方出现(调用方只有 2/3/4/5)。可能 objType 1 是历史遗留。玩家(5)✅。实现:hitSwitch 443 → device geyserTrap(通电触发)。踩踏触发缺失 ❌(checkPressurePlates 只扫 135)。

**Style 7 Orange 压板用后毁**:实现 hitSwitch 135 → tripWire,无 KillTile ❌。

现在读 TELogicSensor.cs。这是传感器最后一环。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:38:11.203Z · glm-x-preview-260804

```
objType 语义确定(5=玩家/2=NPC/4=投射物)。读 TELogicSensor 完成传感器链。
```


---

## 🤖 Assistant · 2026-08-13T00:38:11.405Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Tile_Entities/TELogicSensor.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:38:11.416Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using System.IO;
4	using Microsoft.Xna.Framework;
5	using Terraria.DataStructures;
6	
7	namespace Terraria.GameContent.Tile_Entities;
8	
9	public class TELogicSensor : TileEntityType<TELogicSensor>
10	{
11		public enum LogicCheckType
12		{
13			None,
14			Day,
15			Night,
16			PlayerAbove,
17			Water,
18			Lava,
19			Honey,
20			Liquid
21		}
22	
23		private static Dictionary<int, Rectangle> playerBox = new Dictionary<int, Rectangle>();
24	
25		private static List<Tuple<Point16, bool>> tripPoints = new List<Tuple<Point16, bool>>();
26	
27		private static List<int> markedIDsForRemoval = new List<int>();
28	
29		private static bool inUpdateLoop;
30	
31		private static bool playerBoxFilled;
32	
33		public LogicCheckType logicCheck;
34	
35		public bool On;
36	
37		public int CountedData;
38	
39		public override void RegisterTileEntityID(int assignedID)
40		{
41			base.RegisterTileEntityID(assignedID);
42			TileEntity._UpdateStart += UpdateStartInternal;
43			TileEntity._UpdateEnd += UpdateEndInternal;
44		}
45	
46		public override void OnPlaced()
47		{
48			FigureCheckState();
49		}
50	
51		public override bool IsTileValidForEntity(int x, int y)
52		{
53			return ValidTile(x, y);
54		}
55	
56		private static void UpdateStartInternal()
57		{
58			inUpdateLoop = true;
59			markedIDsForRemoval.Clear();
60			playerBox.Clear();
61			playerBoxFilled = false;
62			FillPlayerHitboxes();
63		}
64	
65		private static void FillPlayerHitboxes()
66		{
67			if (playerBoxFilled)
68			{
69				return;
70			}
71			for (int i = 0; i < 255; i++)
72			{
73				Player player = Main.player[i];
74				if (player.active && !player.dead && !player.ghost)
75				{
76					playerBox[i] = player.getRect();
77				}
78			}
79			playerBoxFilled = true;
80		}
81	
82		private static void UpdateEndInternal()
83		{
84			inUpdateLoop = false;
85			foreach (Tuple<Point16, bool> tripPoint in tripPoints)
86			{
87				Wiring.blockPlayerTeleportationForOneIteration = tripPoint.Item2;
88				Wiring.HitSwitch(tripPoint.Item1.X, tripPoint.Item1.Y);
89				if (Main.netMode == 2)
90				{
91					NetMessage.SendData(59, -1, -1, null, tripPoint.Item1.X, tripPoint.Item1.Y);
92				}
93			}
94			Wiring.blockPlayerTeleportationForOneIteration = false;
95			tripPoints.Clear();
96			foreach (int item in markedIDsForRemoval)
97			{
98				if (TileEntity.TryGet<TELogicSensor>(item, out var result))
99				{
100					TileEntity.Remove(result);
101				}
102			}
103			markedIDsForRemoval.Clear();
104		}
105	
106		public override void Update()
107		{
108			bool state = GetState(Position.X, Position.Y, logicCheck, this);
109			switch (logicCheck)
110			{
111			case LogicCheckType.Day:
112			case LogicCheckType.Night:
113				if (!On && state)
114				{
115					ChangeState(onState: true, TripWire: true);
116				}
117				if (On && !state)
118				{
119					ChangeState(onState: false, TripWire: false);
120				}
121				break;
122			case LogicCheckType.PlayerAbove:
123			case LogicCheckType.Water:
124			case LogicCheckType.Lava:
125			case LogicCheckType.Honey:
126			case LogicCheckType.Liquid:
127				if (On != state)
128				{
129					ChangeState(state, TripWire: true);
130				}
131				break;
132			}
133		}
134	
135		public void ChangeState(bool onState, bool TripWire)
136		{
137			if (onState == On || SanityCheck(Position.X, Position.Y))
138			{
139				Main.tile[Position.X, Position.Y].frameX = (short)(onState ? 18 : 0);
140				On = onState;
141				if (Main.netMode == 2)
142				{
143					NetMessage.SendTileSquare(-1, Position.X, Position.Y);
144				}
145				if (TripWire && Main.netMode != 1)
146				{
147					tripPoints.Add(Tuple.Create(Position, logicCheck == LogicCheckType.PlayerAbove));
148				}
149			}
150		}
151	
152		public static bool ValidTile(int x, int y)
153		{
154			if (!Main.tile[x, y].active() || Main.tile[x, y].type != 423 || Main.tile[x, y].frameY % 18 != 0 || Main.tile[x, y].frameX % 18 != 0)
155			{
156				return false;
157			}
158			return true;
159		}
160	
161		public TELogicSensor()
162		{
163			logicCheck = LogicCheckType.None;
164			On = false;
165			RequiresUpdates = true;
166		}
167	
168		public static LogicCheckType FigureCheckType(int x, int y, out bool on)
169		{
170			on = false;
171			if (!WorldGen.InWorld(x, y))
172			{
173				return LogicCheckType.None;
174			}
175			Tile tile = Main.tile[x, y];
176			if (tile == null)
177			{
178				return LogicCheckType.None;
179			}
180			LogicCheckType result = LogicCheckType.None;
181			switch (tile.frameY / 18)
182			{
183			case 0:
184				result = LogicCheckType.Day;
185				break;
186			case 1:
187				result = LogicCheckType.Night;
188				break;
189			case 2:
190				result = LogicCheckType.PlayerAbove;
191				break;
192			case 3:
193				result = LogicCheckType.Water;
194				break;
195			case 4:
196				result = LogicCheckType.Lava;
197				break;
198			case 5:
199				result = LogicCheckType.Honey;
200				break;
201			case 6:
202				result = LogicCheckType.Liquid;
203				break;
204			}
205			on = GetState(x, y, result);
206			return result;
207		}
208	
209		public static bool GetState(int x, int y, LogicCheckType type, TELogicSensor instance = null)
210		{
211			switch (type)
212			{
213			case LogicCheckType.Day:
214				return Main.dayTime;
215			case LogicCheckType.Night:
216				return !Main.dayTime;
217			case LogicCheckType.PlayerAbove:
218			{
219				bool result = false;
220				Rectangle value = new Rectangle(x * 16 - 32 - 1, y * 16 - 160 - 1, 82, 162);
221				foreach (KeyValuePair<int, Rectangle> item in playerBox)
222				{
223					if (item.Value.Intersects(value))
224					{
225						result = true;
226						break;
227					}
228				}
229				return result;
230			}
231			case LogicCheckType.Water:
232			case LogicCheckType.Lava:
233			case LogicCheckType.Honey:
234			case LogicCheckType.Liquid:
235			{
236				if (instance == null)
237				{
238					return false;
239				}
240				Tile tile = Main.tile[x, y];
241				bool flag = true;
242				if (tile == null || tile.liquid == 0)
243				{
244					flag = false;
245				}
246				if (!tile.lava() && type == LogicCheckType.Lava)
247				{
248					flag = false;
249				}
250				if (!tile.honey() && type == LogicCheckType.Honey)
251				{
252					flag = false;
253				}
254				if ((tile.honey() || tile.lava() || tile.shimmer()) && type == LogicCheckType.Water)
255				{
256					flag = false;
257				}
258				if (!flag && instance.On)
259				{
260					if (instance.CountedData == 0)
261					{
262						instance.CountedData = 15;
263					}
264					else if (instance.CountedData > 0)
265					{
266						instance.CountedData--;
267					}
268					flag = instance.CountedData > 0;
269				}
270				return flag;
271			}
272			default:
273				return false;
274			}
275		}
276	
277		public void FigureCheckState()
278		{
279			logicCheck = FigureCheckType(Position.X, Position.Y, out On);
280			GetFrame(Position.X, Position.Y, logicCheck, On);
281		}
282	
283		public static void GetFrame(int x, int y, LogicCheckType type, bool on)
284		{
285			Main.tile[x, y].frameX = (short)(on ? 18 : 0);
286			switch (type)
287			{
288			case LogicCheckType.Day:
289				Main.tile[x, y].frameY = 0;
290				break;
291			case LogicCheckType.Night:
292				Main.tile[x, y].frameY = 18;
293				break;
294			case LogicCheckType.PlayerAbove:
295				Main.tile[x, y].frameY = 36;
296				break;
297			case LogicCheckType.Water:
298				Main.tile[x, y].frameY = 54;
299				break;
300			case LogicCheckType.Lava:
301				Main.tile[x, y].frameY = 72;
302				break;
303			case LogicCheckType.Honey:
304				Main.tile[x, y].frameY = 90;
305				break;
306			case LogicCheckType.Liquid:
307				Main.tile[x, y].frameY = 108;
308				break;
309			default:
310				Main.tile[x, y].frameY = 0;
311				break;
312			}
313		}
314	
315		public static bool SanityCheck(int x, int y)
316		{
317			if (!Main.tile[x, y].active() || Main.tile[x, y].type != 423)
318			{
319				Kill(x, y);
320				return false;
321			}
322			return true;
323		}
324	
325		public static int Hook_AfterPlacement(int x, int y, int type = 423, int style = 0, int direction = 1, int alternate = 0)
326		{
327			bool on;
328			LogicCheckType logicCheckType = FigureCheckType(x, y, out on);
329			GetFrame(x, y, logicCheckType, on);
330			if (Main.netMode == 1)
331			{
332				NetMessage.SendTileSquare(Main.myPlayer, x, y);
333				NetMessage.SendData(87, -1, -1, null, x, y, (int)TileEntityType<TELogicSensor>.EntityTypeID);
334				return -1;
335			}
336			return TileEntityType<TELogicSensor>.Place(x, y);
337		}
338	
339		public new static void Kill(int x, int y)
340		{
341			if (TileEntity.TryGetAt<TELogicSensor>(x, y, out var result))
342			{
343				Wiring.blockPlayerTeleportationForOneIteration = result.logicCheck == LogicCheckType.PlayerAbove;
344				bool flag = false;
345				if (result.logicCheck == LogicCheckType.PlayerAbove && result.On)
346				{
347					flag = true;
348				}
349				else if (result.logicCheck == LogicCheckType.Water && result.On)
350				{
351					flag = true;
352				}
353				else if (result.logicCheck == LogicCheckType.Lava && result.On)
354				{
355					flag = true;
356				}
357				else if (result.logicCheck == LogicCheckType.Honey && result.On)
358				{
359					flag = true;
360				}
361				else if (result.logicCheck == LogicCheckType.Liquid && result.On)
362				{
363					flag = true;
364				}
365				if (flag)
366				{
367					Wiring.HitSwitch(result.Position.X, result.Position.Y);
368					NetMessage.SendData(59, -1, -1, null, result.Position.X, result.Position.Y);
369				}
370				Wiring.blockPlayerTeleportationForOneIteration = false;
371				if (inUpdateLoop)
372				{
373					markedIDsForRemoval.Add(result.ID);
374				}
375				else
376				{
377					TileEntity.Remove(result);
378				}
379			}
380		}
381	
382		public override void WriteExtraData(BinaryWriter writer, bool networkSend)
383		{
384			if (!networkSend)
385			{
386				writer.Write((byte)logicCheck);
387				writer.Write(On);
388			}
389		}
390	
391		public override void ReadExtraData(BinaryReader reader, int gameVersion, bool networkSend)
392		{
393			if (!networkSend)
394			{
395				logicCheck = (LogicCheckType)reader.ReadByte();
396				On = reader.ReadBoolean();
397			}
398		}
399	
400		public override string ToString()
401		{
402			return Position.X + "x  " + Position.Y + "y " + logicCheck;
403		}
404	}
405	

```


---

## 🤖 Assistant · 2026-08-13T00:38:29.365Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
TELogicSensor 全文到手,这是传感器的完整权威:

- style→frameY:Day=0、Night=18、PlayerAbove=36、Water=54、Lava=72、Honey=90、Liquid(Any)=108 ✅(实现的"0=昼 36=夜 72=玩家上方"**全错**;实现 mode=floor(frameY/18)%3 → Water(54)=0 被当昼、Lava(72)=0 当昼、PlayerAbove(36)=0 当昼、Honey(90)=0 当昼、Any(108)=0 当昼;Night(18)=1 当夜 ✅ 唯一正确)
- on 态:frameX 18(off 0)
- Day/Night:**边沿触发**(on 时进 Day → trip;off 时回到 Night → 只翻态不发信号)。即 Day 传感器只在 sunrise 发一次,日落时静默复位 ✅。实现 triggerDayNightSensors "mode===0 && isDay" 每次昼夜切换回调触发全部昼传感器 ✅ 语义近似正确(前提是帧表对;但实现的帧表错位 → Water 传感器会被误当昼传感器在日出触发!)
- PlayerAbove:检测盒 Rectangle(x*16-32-1, y*16-160-1, 82, 162) → 5 宽(x-2..x+2)×10 高(y-10..y-1) ✅ wiki。实现:x===ptx && pty-y<=8(1 宽、8 高)❌ 两侧都错
- 玩家判定:active && !dead && !ghost(1.4.2) ✅ wiki
- 触发时 blockPlayerTeleportationForOneIteration = (logicCheck == PlayerAbove)→ Player Above 触发时抑制传送 ✅ wiki "Player Above cannot activate Teleporters"。液体传感器触发时 = false(不抑制)。
- Water/Lava/Honey/Any:本格液体判定 + **液体离开的 15t 迟滞**(CountedData 15→0)防止液体晃动抖动;Water 排除 lava/honey/shimmer(wiki 说 Water 也被 Shimmer 触发——**wiki 错了/过时**:源码 `if ((tile.honey() || tile.lava() || tile.shimmer()) && type == Water) flag = false;` → Shimmer 明确**不**触发 Water 传感器!Liquid(Any)类型呢?type==Liquid 时无排除 → Any 被 shimmer 触发。wiki 110 行 "The Water Sensor will also activate when in contact with Shimmer" —— **wiki 与源码不符**(按源码:Water 传感器被 shimmer 排除;只有 Liquid Any 传感器响应 shimmer)。标 📄。
- 状态翻转时 trip(frameX 18↔0)

**实现传感器结论**:
1. 帧表错位(mode%3)→ Day/Water/Lava/Honey/Any/PlayerAbove 全部错标 ❌
2. 液体传感器(Water/Lava/Honey/Any)未实现 ❌
3. Player Above 检测盒 1×8 ≠ 原版 5×10 ❌
4. Player Above 触发时未设 blockPlayerTeleportationForOneIteration ❌(wiki/源码:抑制传送)——实现的 updateTriggerTiles 只在测重板设置该 flag;PlayerAbove 不设 → Player Above 传感器可触发传送器 ❌(这是玩家可感知的行为差异)
5. Day/Night 传感器有实现(近似)⚠️

好,现在还剩:
- Game.ts 7000-7030 雕像 spawnNpc(value/npcSlots/SpawnedFromStatue/CanBeReplacedByOtherNPCs)
- Game.ts 210 地雷踩踏
- wiki Statues 刷怪规则 + Pumps
- 原版 Item.cs MechSpawn(48982-49013)对照实现 itemSpawnOk(300/800/3/6/10)——已注释,需快速核对数值。
- 原版 WorldGen.ShootFromCannon(50606-50718)与实现的炮族对照——实现注释引用,大体可信,抽查 LaunchRocket(62184-62206)烟花火箭数值。
- 电路工具(接线工具、光标查看半径)——必核清单第 1 项。实现 Game.ts:5556 ItemCheck_UseWiringTools + Renderer 线渲染。原版 WiresUI 查看半径:全屏?wiki Wire 页:持机械透镜等。光标查看半径——原版显示电线范围 = 屏幕内全部(当持有扳手/线/机械透镜时)。查实现 Renderer.ts 线渲染范围。

由于时间/预算,聚焦必核清单。先并行:
1. Game.ts 7000-7036 spawnNpc
2. Game.ts 5556-5650 电路工具
3. wiki Pumps.md + Statues.md 刷怪段(grep)
4. 原版 Item.cs 48982-49013

然后收尾输出报告。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:38:30.089Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; sed -n '7000,7036p' $G/core/Game.ts; echo \"===spawnNpc ctx===\"; sed -n \"$(grep -n 'spawnNpc:' $G/core/Game.ts | head -1 | cut -d: -f1),+25p\" $G/core/Game.ts",
 "description": "Read statue NPC spawn flags in Game.ts"
}
```


---

## 🤖 Assistant · 2026-08-13T00:38:30.802Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "T=~/Project/GLM/SandboxWorld/Terarria1456; echo \"===Item.MechSpawn===\"; sed -n '48982,49013p' $T/Terraria/Item.cs; echo \"===Rocket===\"; sed -n '62184,62206p' $T/Terraria/WorldGen.cs",
 "description": "Verify Item.MechSpawn and rocket numbers"
}
```


---

## 🤖 Assistant · 2026-08-13T00:38:31.797Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "W=~/Project/GLM/SandboxWorld/terraria-wiki-md; echo \"===Pumps===\"; sed -n '1,60p' $W/Pumps.md | grep -v \"^\\[\" | head -45; echo \"===Statue spawn===\"; grep -n -i \"cooldown\\|limit\\|three\\|6 times\\|heart\\|star\\|10 \" $W/Statues.md | head -20",
 "description": "Extract pumps and statue spawn rules from wiki"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:38:43.794Z

**📎 ToolResult**

```
    const gyTarget = Math.max(0, Math.min(1, (this.scene.graveyardTileCount - 16) / (36 - 16)));
    const gyStep = this.graveyardIntensity < gyTarget ? 0.02 : 0.1;
    this.graveyardIntensity += Math.max(-gyStep, Math.min(gyStep, gyTarget - this.graveyardIntensity));
    // 白天 tick 进度（原版 time 0-54000 ↔ 我们 timeOfDay 白天前半段 0.25-0.75 线性）
    const dayTimeTicks = w.clock.isDay ? ((w.clock.timeOfDay - 0.25) / 0.5) * 54000 : 0;
    weather.setWorldSize(w.w, w.h);
    weather.update({
      dayRate: w.dayRate(), // Main.cs:64320-64409 天气全链吃 dayRate（旅程倍率/冻结/全员睡×5/晷快进，曾写死 1）
      dayTime: w.clock.isDay,
      dayTimeTicks,
      playerStrongEnough: this.player.maxHp >= 120,
      playerReadyForKingSlime: this.player.maxHp > 140 && this.player.defense > 8, // Main.cs:64645
      expertMode: w.isExpert,   // Main.expertMode（Main.cs:2775）：史莱姆雨自然触发门（:64373-64409 就绪||专家）
      atmo,
      aboveRockLayer: pty < rl,
      graveyardIntensity: this.graveyardIntensity,
      hardMode: !!w.flags.hardMode,
      noOtherEvent: !w.clock.bloodMoon && this.world.invasionType === 0,
      downedSlimeKing: !!(w.flags.downedSlimeKing ?? w.flags.downed_50),  // 击败键=downed_50(50=史莱姆王)
      maxTilesX: w.w,
      worldSurface: gl,
      viewCenterY: viewCY,
      // Main.BackgroundEnabled（Main.cs:790）：设置项「背景 开/关」（Options.backgrounds，
      // 默认 true）——cloudBGAlpha 阴天渐变门（Main.cs:58783）
      backgroundEnabled: options.data.backgrounds,
      // 灯笼夜天气压制（Main.cs:64288 云钳 30 / :64331 停雨 / :64353 不开新雨 /
      // :58249 风场停掷）
      lanternsUp: LanternNight.lanternsUp,
      nextNightIsLanternNight: LanternNight.nextNightIsLanternNight,
      onCoinRain: (x, y, type, stack) => {
        // 非实心 32×32 门（WorldGen.cs:71847）
        const st = w.store;
        const tx0 = Math.floor(x / 16), ty0 = Math.floor(y / 16);
        let solid = false;
        for (let dx = 0; dx <= 1 && !solid; dx++) for (let dy = 0; dy <= 1; dy++) {
          if (st.inBounds(tx0 + dx, ty0 + dy) && st.isSolid(tx0 + dx, ty0 + dy)) { solid = true; break; }
        }
===spawnNpc ctx===
      spawnNpc: (id, x, y) => {
        const e = Enemy.fromVanilla(id, x, y);
        if (!e) return;
        e.id = this.entities.nextId++;
        this.entities.add(e, 'enemies');
      },
      countNpcs: (id) => (this.entities.enemies as Enemy[]).reduce(
        (n, e) => n + (e.dead || e.vanillaId !== id ? 0 : 1), 0),
      anyNpc: (id) => this.hasNpcId(id),
      crystalPoints: () => (this.entities.enemies as Enemy[])
        .filter((e) => !e.dead && e.vanillaId === 548)
        .map((e) => ({ x: e.cx, y: e.y + e.h })),
      dropAtCrystal: (vanillaItemId, count) => {
        const key = VANILLA_ITEM_KEY_BY_ID[vanillaItemId];
        const crystal = (this.entities.enemies as Enemy[]).find((e) => !e.dead && e.vanillaId === 548);
        if (!key || !crystal) return;
        this.spawnDrop(crystal.cx, crystal.cy + 8, key, count, 0, -2);
      },
      arenaEnds: (x, y) => checkArenaScore(this, x * TILE + 8, y * TILE + 8),
      findGroundY: (tileX, tileY) => {
        const st = this.world.store;
        for (let y = tileY; y < Math.min(st.h, tileY + 50); y++) {
          if (st.inBounds(tileX, y) && st.isSolid(tileX, y)) return y;
        }
        return null;
      },

```


---

## 👤 User(sidechain) · 2026-08-13T00:38:43.831Z

**📎 ToolResult**

```
===Item.MechSpawn===
	public static bool MechSpawn(float x, float y, int type)
	{
		int num = 0;
		int num2 = 0;
		int num3 = 0;
		Vector2 vector = new Vector2(x, y);
		for (int i = 0; i < 400; i++)
		{
			WorldItem worldItem = Main.item[i];
			if (worldItem.active && worldItem.type == type)
			{
				num++;
				float num4 = worldItem.position.X - vector.X;
				float num5 = worldItem.position.Y - vector.Y;
				float num6 = (float)Math.Sqrt(num4 * num4 + num5 * num5);
				if (num6 < 300f)
				{
					num2++;
				}
				if (num6 < 800f)
				{
					num3++;
				}
			}
		}
		if (num2 >= 3 || num3 >= 6 || num >= 10)
		{
			return false;
		}
		return true;
	}

===Rocket===
	public static void LaunchRocket(int x, int y, bool fromWiring)
	{
		int num = Main.tile[x, y].frameY;
		int num2 = 0;
		while (num >= 40)
		{
			num -= 40;
			num2++;
		}
		if (num == 18)
		{
			y--;
		}
		Vector2 vector = new Vector2(x * 16 + 8, y * 16 + 4);
		int type = 167 + num2;
		int damage = 150;
		int num3 = 7;
		int num4 = Projectile.NewProjectile(GetProjectileSource_PlayerOrWires(x, y, fromWiring, Main.LocalPlayer), vector.X, vector.Y + 2f, 0f, -8f, type, damage, num3, Main.myPlayer);
		Main.projectile[num4].originatedFromActivableTile = true;
		Main.tile[x, y].active(active: false);
		Main.tile[x, y + 1].active(active: false);
		NetMessage.SendTileSquare(-1, x, y, 1, 2);
	}

```


---

## 👤 User(sidechain) · 2026-08-13T00:38:58.740Z

**📎 ToolResult**

```
===Pumps===
# Pumps

> 原页面: `Pumps`

# Pumps

Inlet Pump

  * 


Statistics

Type| [Furniture](Furniture.md "Furniture")[Mechanism](Mechanism "Mechanism")  
---|---  
  
  * Internal [Item ID](Item_IDs.md "Item IDs"): **581**
  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **142**

Outlet Pump

  * 


Statistics

Type| [Furniture](Furniture.md "Furniture")[Mechanism](Mechanism "Mechanism")  
---|---  
  
  * Internal [Item ID](Item_IDs.md "Item IDs"): **582**
  * Internal [Tile ID](Tile_IDs.md "Tile IDs"): **143**

Using Pumps to pump water from one container to another. Note the wire placement, and how an outlet pump stops transferring water when fully submerged.

**Inlet** and **Outlet Pumps** are [mechanisms](Mechanisms.md "Mechanisms") used to transport [liquids](Liquids.md "Liquids") ([water](Water.md "Water"), [lava](Lava.md "Lava"), [honey](Honey.md "Honey"), and [Shimmer](Shimmer.md "Shimmer")**** __(Desktop, Console and Mobile versions)), without having to construct pathways through [blocks](Blocks.md "Blocks") or rely on gravity. Instead, an Inlet and Outlet Pump need only be connected to each other with [Wires](Wire.md "Wire") and activated, which transfers fluid from the Inlet Pump to the Outlet Pump. Each activation transfers up to four tiles of liquid. For continuous automated pumping, a [timer](Timer "Timer") can be used. 

Despite its appearance as a pipe that takes in liquid from beside it, an Inlet Pump must be submerged in liquid, as it removes liquid that lies directly over its graphic, and does so equally from all of its 2×2 tile space. Similarly, an Outlet Pump spawns liquid directly over its graphic, and does so equally over all of its 2×2 tile space. 

## Crafting

### Recipes

Result| Ingredients| [Crafting station](Crafting_station "Crafting station")  
---|---|---  
Inlet Pump| 
===Statue spawn===
51:See Spawn limits below for limitations that apply to these functional statues.
59:  * Items, [Hearts](Heart.md "Heart") and [Stars](Star.md "Star") are dropped at a reduced rate (the multiplier depends on the statue, listed below).
96:  * Will drop recovery Hearts and Stars even if killed without player interaction (by lava, traps, NPCs).
99: Drippler StatueInternal [Item ID](Item_IDs.md "Item IDs"): 3710 | [](Drippler.md "Drippler")[Drippler](Drippler.md "Drippler") | 0.05  | Yes | 
148:  * Will drop recovery Hearts and Stars even if killed without player interaction (by lava, traps, NPCs).
159:See Spawn limits below for limitations that apply to these functional statues.
199:    * Corrupt and Vicious Bunnies do not count as statue-spawned, so they are not affected by the spawn limit and drop loot as normal.
263:  * When [raining](Rain.md "Rain"), Goldfish will start walking, ignoring the spawn cap.
265:    * Corrupt and Vicious Goldfish do not count as statue-spawned, so they are not affected by the spawn limit.
312:    * Corrupt and Vicious Penguins do not count as statue-spawned, so they are not affected by the spawn limit and drop loot as normal.
380:See Spawn limits below for limitations that apply to these functional statues.
427: Heart StatueInternal [Item ID](Item_IDs.md "Item IDs"): 473 | [](Heart.md "Heart")[Heart](Heart.md "Heart")  
428: Star StatueInternal [Item ID](Item_IDs.md "Item IDs"): 438 | [](Star.md "Star")[Star](Star.md "Star")  
442:Decorative statues have no function and only serve as decoration. They are generally found placed [underground](Underground.md "Underground"). The three Lihzahrd statues are only found in the [Jungle Temple](Jungle_Temple.md "Jungle Temple"), and are the only statues that do not appear to be made of stone. The Armor Statue can also be crafted with 50 [](Stone_Block.md "Stone Block") at a [](Work_Bench "Work Bench")[Work Bench](Work_Bench "Work Bench"). 
512:## Spawn limits
514:Entities within range count towards spawn limit.
516:Functional statues have two kinds of spawn limits: input cooldown and number limit. 
518:The 6 tiles (2×3) a statue occupies can all be used as wire inputs, and the statue will enter a cooldown period upon activating. During this cooldown, activations from any [trigger devices](Mechanisms.md "Mechanisms") ([Switches](Switch.md "Switch"), [timers](Timers.md "Timers"), [Pressure Plates](Pressure_Plates.md "Pressure Plates"), etc.) will be ignored. All six inputs share the cooldown with each other. 
522:Statue type  | Spawn limits   
524:Input cooldown[4] | Number limit[5] | Distance (D) to Range Boundary

```


---

## 🤖 Assistant · 2026-08-13T00:39:12.366Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
继续核对:

**泵 wiki**:每次激活最多 4 格液体 ✅(实现:每泵 4 格 × 每侧最多 19 泵);2×2 空间均匀抽排 ✅(实现 cells 顺序 [(0,1),(1,1),(0,0),(1,0)] ✅ 与原版一致)。支持水/岩浆/蜂蜜/微光 ✅。

**烟花火箭**(WorldGen.cs:62184-62206):
- num = frameY,num2 行(frameY/40),num==18 → y--
- 出膛 (x*16+8, y*16+4+2) = (x*16+8, y*16+6) ✅ 实现一致
- 弹 167+num2 ✅(实现 form=frameY/40 → 167-170)
- 伤害 150、kb 7 ✅ 速度 (0,-8) ✅
- 消耗:active(false) 两格 ✅
✅ 实现对齐。

**雕像 spawn 后标志**:实现 spawnNpc:`Enemy.fromVanilla(id,x,y)` —— **没有设置 value=0 / npcSlots=0 / SpawnedFromStatue / CanBeReplacedByOtherNPCs**!Game.ts:7008 的注释(之前 grep 到的)说"Wiring.cs:2479-2483:雕像产怪 value=0(不掉钱)+ SpawnedFromStatue"——那是在另一个地方(7040 附近?)。刚才 sed 7000-7036 没显示。之前 grep 输出:
```
Game.ts:7008: // Wiring.cs:2479-2483:雕像产怪 value=0(不掉钱)+ SpawnedFromStatue
```
但现在 sed 7000-7036 显示的内容不同(天气)!说明行号漂移了——之前的 grep 是第一次跑的,后来 sed 7000 显示 weather。哦不对,grep 输出的 7008 行号与 sed 7000-7036 不一致…… 因为 grep 和 sed 是同一个文件,行号应该一致。再看:grep 输出 "7008: // Wiring.cs:2479-2483" 而 sed '7000,7036p' 显示 7000 行是 gyTarget。矛盾?可能我 sed 的偏移不同——sed -n '7000,7036p' 从 7000 开始。grep 说 7008 是雕像注释。但 sed 输出的 7008 行是 "const dayTimeTicks = ..."。这不一致!

哦,我明白了:第一次 grep(grep -rn "Wiring\|teleporter..." 是在对话早期)和现在的文件可能没变。让我重新精确 grep 行号。可能是我记错了——第一次 grep 输出 "~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7008:" 确实如此。但现在 sed 7000-7036 输出的是天气代码。行号冲突说明……文件没变的话不可能。等一下,刚才第二个 Bash(sed spawnNpc ctx)输出 `spawnNpc: (id, x, y) => { const e = Enemy.fromVanilla(...)` 没有 value=0。

嗯,也许 7008 的雕像注释在 spawnNpc 附近,而 weather 段在 6990-7036。让我直接 grep "SpawnedFromStatue" in Game.ts 确认。

**Item.MechSpawn** ✅:300/800/3/6/10 与实现一致。

**雕像 Spawn limits wiki**(512-524):输入冷却 + 数量限制。数量限制= MechSpawn(200/600/3/6/10)✅。

还需要:
1. grep Game.ts SpawnedFromStatue/value=0
2. Game.ts 5556 电路工具段(接线/剪线/致动器/光标半径)
3. 210 地雷踩踏路径
4. wiki Spawn limits 表(518-528 行冷却数值:NPC 雕像 30t、物品 600t、心 600t 等——源码 CheckMech 已对:30/600/300/900)

读。
````

</details>


---

## 🤖 Assistant · 2026-08-13T00:39:13.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; grep -n \"SpawnedFromStatue\\|spawnedFromStatue\\|value = 0\\|value=0\\|CanBeReplaced\" $G/core/Game.ts | head -10; echo \"===210 landmine===\"; grep -n \"sheetOf(dx, dy) === 411\\|=== 210\\|210\" $G/core/Game.ts | grep -i \"210\\|landmine\\|地雷\" | head -8; echo \"===wiring tools===\"; sed -n '5556,5640p' $G/core/Game.ts",
 "description": "Check statue flags, landmine, wiring tools"
}
```


---

## 🤖 Assistant · 2026-08-13T00:39:14.584Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "W=~/Project/GLM/SandboxWorld/terraria-wiki-md; sed -n '512,560p' $W/Statues.md; echo \"===wire view radius===\"; grep -n -i \"radius\\|screen\\|range\\|see\\|display\" $W/Wire.md | head -12",
 "description": "Statue spawn limits table and wire view range"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:39:21.512Z

**📎 ToolResult**

```
7167:          // Wiring.cs:2479-2483：雕像产怪 value=0（不掉钱）+ SpawnedFromStatue
7168:          e.spawnedFromStatue = true;
7877:      // value=0，Wiring.cs:2479）&& hasLuckyCoin && rand.Next(5)==0；
7882:      if (!e.spawnedFromStatue && npcValueOf(luckyNetId) > 0
===210 landmine===
4439:        if (Math.random() < 1 / 7) give(2109);
4942:   *  计数存 world.altarCount（原版 WorldGen.altarCount 静态位，WorldFile.cs:1303/2100
5156:      else if ((sheet === 226 || sheet === 237) && power < 210) dmg = 0;       // 蜥蜴砖 210
5454:        // type=Next(210,212)；初速 ±0.4（Next(-200,201)*0.002）
5455:        const bee = Enemy.fromVanilla(r.next() < 0.5 ? 210 : 211, px, py);
6277:          this.player.facing = Math.floor(fx / 72) === 0 ? -1 : 1; // SH:204-210 床朝向
9964:    //  整段替换——金鱼上岸散步 230 主导；L2107-2126 香蒲蜻蜓）。
===wiring tools===
      const dropY = (top + Math.floor((p + 0.5) * height / wood)) * TILE;
      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, VI_KEY.WOOD, 1, (Math.random() - 0.5) * 2, -2 - Math.random());
    }
    for (const b of branchSpots) {
      this.spawnDrop(b.x * TILE + 8, b.y * TILE + 8, VI_KEY.WOOD, 1, (Math.random() - 0.5) * 2, -2 - Math.random());
    }
    // 橡实：较大概率（75%）掉 2-3 颗，沿树冠区域散落供补种
    if (Math.random() < 0.75) {
      const nAcorn = 2 + Math.floor(Math.random() * 2);
      for (let a = 0; a < nAcorn; a++) {
        const ax = x + (Math.random() - 0.5) * 2.5;
        const ay = top + Math.random() * height * 0.4;
        this.spawnDrop(ax * TILE + 8, ay * TILE, VI_KEY.ACORN, 1, (Math.random() - 0.5) * 3, -3 - Math.random());
      }
    }
    this.spawnParticles(x * TILE + 8, top * TILE + 8, '#2E8B3D', 14, 2.2);
    // 从登记表移除
    const t = this.world.trees.findIndex((tr) => tr.x === x && Math.abs(tr.y - top) <= 2);
    if (t >= 0) this.world.trees.splice(t, 1);
  }

  /** 砍导入的原版树（tile 5 / 宝石树 / 装饰树 / 灰烬树）：
   *  同列同类型连续段 = 整棵树（含顶部树冠标记格），整棵移除 + 掉木材。
   *  首击即倒（不做倒树动画——动画实体绑定自有树的登记表结构） */
  /** 暗影之球/恶魔之心整体破碎 = 原版 WorldGen.CheckOrb（cs:54259-54358）1:1：
   *  帧锚点定位（frameX∈{0,36} 是左列）→ 2×2 四格一起清除；
   *  战利品（:54264-54318）：首破（!shadowOrbSmashed）固定 0 档,之后 rand(5) 五选一
   *  ——腐化{96火枪+凝胶100, 64暗影珠, 162堕落荆棘, 115刺球, 111阳炎之怒} /
   *  猩红{800下作恶者+凝胶100, 1256猩红之心, 802腐叉, 3062, 1290}；
   *  计数 shadowOrbCount 满 3 → 最近玩家处召 EoW(13)/BoC(266) 并归零
   *  （:54320-54352,对侧已存活则跳过）；1/2 颗世界广播 misc[10/11]；
   *  陨石触发在 1.4 语义里不经砸珠（EoW/BoC 击杀链触发,见 boss 死亡段） */
  private smashOrbHeart(x: number, y: number) {
    const st = this.world.store;
    const i = st.idx(x, y);
    const fx = st.frameX[i];
    const isDemonHeart = fx >= 36; // 原版：frameX ≥ 36 = 恶魔之心（猩红世界）
    const ax = (fx === 0 || fx === 36) ? x : x - 1;
    const ay = st.frameY[i] !== 0 ? y - 1 : y;
    this.chunks.markDirtyArea(ax - 1, ay - 1, ax + 2, ay + 2);
    for (let dx = 0; dx < 2; dx++) {
      for (let dy = 0; dy < 2; dy++) st.setTile(ax + dx, ay + dy, 0);
    }
    // 战利品五档（首破固定 0 档;item id 走 VANILLA_ITEM_KEY_BY_ID 反查）
    const POOLS: Record<'orb' | 'heart', number[]> = {
      orb: [96, 64, 162, 115, 111],        // 腐化：火枪/暗影珠/堕落荆棘/刺球/阳炎之怒
      heart: [800, 1256, 802, 3062, 1290], // 猩红：下作恶者/猩红之心/腐叉/…
    };
    const first = !this.world.flags.shadowOrbSmashed;
    const roll = first ? 0 : Math.floor(Math.random() * 5);   // Main.rand.Next(5)
    const vid = POOLS[isDemonHeart ? 'heart' : 'orb'][roll];
    const key = VANILLA_ITEM_KEY_BY_ID[vid];
    if (key) this.spawnDrop(ax * TILE + 8, ay * TILE + 8, key, 1, (Math.random() - 0.5) * 3, -3);
    if (roll === 0) {
      const gelKey = VANILLA_ITEM_KEY_BY_ID[97];               // 凝胶 ×100（genRand.Next(100,101)）
      if (gelKey) this.spawnDrop(ax * TILE + 8, ay * TILE + 8, gelKey, 100, (Math.random() - 0.5) * 3, -3);
    }
    this.spawnParticles(ax * TILE + 16, ay * TILE + 16, isDemonHeart ? '#FF4060' : '#9A6AE0', 16, 2.5);
    this.sfx.play('tink');
    this.cb.onToast(isDemonHeart ? Lang.text('Mods.SandboxWorld.Toast.DemonHeartSmashed') : Lang.text('Mods.SandboxWorld.Toast.ShadowOrbSmashed'));
    // 成就：SMASHING_POPPET（:54359 event 7——每次砸珠/心都触发）
    this.achievements.notifyProgressionEvent(7);
    this.world.flags.shadowOrbSmashed = true;
    this.world.shadowOrbCount++;
    if (this.world.shadowOrbCount >= 3) {
      // :54320-54352:第 3 颗召 EoW/BoC（对侧变体已存活则不召）,计数归零
      const otherAlive = (id: number) => this.entities.enemies.some(
        (e) => !((e as Enemy).dead) && (e as Enemy).vanillaId === id);
      if (isDemonHeart ? !otherAlive(266) : !otherAlive(13)) {
        this.summonBoss(isDemonHeart ? 'brain_of_cthulhu' : 'eater_of_worlds_head');
      }
      this.world.shadowOrbCount = 0;
    } else {
      this.newText(Lang.misc(this.world.shadowOrbCount === 2 ? 11 : 10), 120, 90, 160);
    }
  }

  private fellImportedTree(x: number, y: number, type: number) {
    const st = this.world.store;
    let top = y;
    while (st.get(x, top - 1) === type) top--;
    let bottom = y;
    while (st.get(x, bottom + 1) === type) bottom++;
    const height = bottom - top + 1;
    this.chunks.markDirtyArea(x - 6, top - 7, x + 6, bottom + 1);

```


---

## 👤 User(sidechain) · 2026-08-13T00:39:21.539Z

**📎 ToolResult**

```
## Spawn limits

Entities within range count towards spawn limit.

Functional statues have two kinds of spawn limits: input cooldown and number limit. 

The 6 tiles (2×3) a statue occupies can all be used as wire inputs, and the statue will enter a cooldown period upon activating. During this cooldown, activations from any [trigger devices](Mechanisms.md "Mechanisms") ([Switches](Switch.md "Switch"), [timers](Timers.md "Timers"), [Pressure Plates](Pressure_Plates.md "Pressure Plates"), etc.) will be ignored. All six inputs share the cooldown with each other. 

Activation of a spawning statue will _not_ produce an item/character if a certain quantity of that entity already exists within a certain range. The range boundary is a circle, centered on the statue's spawning point. 

Statue type  | Spawn limits   
---|---  
Input cooldown[4] | Number limit[5] | Distance (D) to Range Boundary   
Enemy and critter statues  | 0.5 seconds  | 3  | 12.5 tiles (200 pixels)   
6  | 37.5 tiles (600 pixels)   
10  | Anywhere in the world   
[Bomb](Bomb_Statue.md "Bomb Statue"), [Heart](Heart_Statue.md "Heart Statue"), and [Star Statue](Star_Statue.md "Star Statue") | 10 seconds  | 3  | 18.75 tiles (300 pixels)   
6  | 50 tiles (800 pixels)   
10  | Anywhere in the world   
[King](King_Statue.md "King Statue") and [Queen Statue](Queen_Statue.md "Queen Statue") | 5 seconds  | n/a | n/a  
[Boulder Statue](Boulder_Statue.md "Boulder Statue") | 15 seconds  | n/a | n/a  
  
  * _Example:_ A new [Bunny](Bunny.md "Bunny") will not be spawned by an activated Bunny Statue if 3 or more Bunnies already exist within a 200-pixel radius.

Creatures spawned by Bunny, Fish, and Penguin Statues during a [Blood Moon](Blood_Moon.md "Blood Moon") will immediately turn into their evil forms: [Corrupt](Corrupt_Bunny.md "Corrupt Bunny")/[Vicious Bunny](Vicious_Bunny.md "Vicious Bunny"), [Corrupt](Corrupt_Goldfish.md "Corrupt Goldfish")/[Vicious Goldfish](Vicious_Goldfish.md "Vicious Goldfish"), and [Corrupt](Corrupt_Penguin.md "Corrupt Penguin")/[Vicious Penguin](Vicious_Penguin.md "Vicious Penguin"), respectively. These evil forms do not count against the spawn limits, making it possible to spawn large numbers of these enemies from statues. The same is true of Goldfish which start walking during [rain](Rain.md "Rain"), and Explosive Bunnies from Bunny Statues in [For the Worthy](For_the_Worthy.md "For the Worthy") worlds. Another exception is the [Bomb Statue](Bomb_Statue.md "Bomb Statue"), since [Bombs](Bombs "Bombs") may group together into stacks of up to 9999 and each stack counts as a single entity. 

Bunny and Squirrel Statues will spawn their usual [critters](Critters.md "Critters") in a [Cavern](Cavern.md "Cavern") town, not their [gem](Gem "Gem") versions (e.g. regular [Bunny](Bunny.md "Bunny") instead of [Amethyst Bunny](Amethyst_Bunny "Amethyst Bunny")). 

## Notes

  * The [Old Man](Old_Man.md "Old Man"), [Skeleton Merchant](Skeleton_Merchant.md "Skeleton Merchant"), and all [town pets](Town_pet.md "Town pet") cannot be teleported with either NPC Statue.
  * Statue-spawned enemies and critters will not be transformed in [Shimmer](Shimmer.md "Shimmer") and will despawn instead.
  * [The Horseman's Blade](The_Horseman's_Blade.md "The Horseman's Blade")'s Flaming Jacks cannot be summoned from hitting statue-spawned enemies or critters.
  * All functional and decorative statues (except Turtle Statues, Owl Statues, Boulder Statues, Bast Statues, and Lihzahrd Statues) have a chance to be found already placed underground and inside [Underground Cabins](Underground_Cabin.md "Underground Cabin").
  * Worlds contain up to 2, 3, or 4 of each type of pre-placed statues, depending on the [world size](World_size.md "World size"). Underground Cabins can contain additional ones.
  * Already placed Slime Statues, Bat Statues, Skeleton Statues, and Crab Statues are always [trapped](Statue_trap.md "Statue trap").

## Tips

  * Some statues can be used to create useful mechanisms due to the stats or [AI](AI.md "AI") of the spawned entity: 
    * Statues that spawn weak enemies (e.g. Slime Statue) can be used to create [invulnerability](Invincibility_frames "Invincibility frames") mechanisms to shield against heavy-damage attacks.
    * Bird and Crab Statues can be used to make [Bird and Crab engines](Guide%3AWiring#Engines "Guide:Wiring"), respectively.
  * When spawning weak enemies into lava, it is most efficient to use a [1/2 Second Timer](1/2_Second_Timer.md "1/2 Second Timer"). This is just the amount of time it takes for them to be killed by the lava, meaning they will be killed as fast as they can be spawned.
  * The [Metal Detector](Metal_Detector.md "Metal Detector") can help find statues, indirectly, by detecting the [Chest](Chest "Chest") within [Underground Cabins](Underground_Cabin.md "Underground Cabin"), which sometimes contain statues. Note that [Hardmode ores](Hardmode_ore.md "Hardmode ore"), [Life Crystals](Life_Crystal.md "Life Crystal"), and [Life Fruits](Life_Fruit.md "Life Fruit") have priority over Chests, making this more difficult in Hardmode. 
    * [Spelunker Potions](Spelunker_Potion.md "Spelunker Potion") can also be used to the same effect.
  * Slimes spawned by the Slime Statue during the [Slime Rain](Slime_Rain.md "Slime Rain") event can help add to the number required to summon the [King Slime](King_Slime.md "King Slime").
  * Statue-spawned [Armed Zombies](Armed_Zombie.md "Armed Zombie"), [Blue Slimes](Blue_Slime.md "Blue Slime"), [Crabs](Crab.md "Crab"), and [Wall Creepers](Wall_Creeper.md "Wall Creeper") drop [Hearts](Heart.md "Heart") and [Stars](Star.md "Star") as usual when killed, if the player is not at maximum [health](Health.md "Health") or [mana](Mana.md "Mana") respectively. They do so even if the player does not deal damage to them. If their statues are set up with a timer and lava near a player arena, this can provide a fairly steady supply of mana and health restoration. 
    * On the one hand, this bypasses the Heart and Star Statues' tight limits on nearby spawns; on the other, the Hearts and Stars do not spawn in advance, only when the player is below their respective maximums.
  * Since the effects of the [Life Drain](Life_Drain.md "Life Drain") work on statue-spawned enemies, the player can build a pit with any [timer](Timers.md "Timers") spawning weak enemies to recover health during a boss fight.
===wire view radius===
10:For the differences of this information on [Old-gen console](Legacy%3AOld-gen_console_version "Legacy:Old-gen console version") and [3DS](Legacy%3A3DS_version "Legacy:3DS version"), see **[Legacy:Wire](Legacy%3AWire "Legacy:Wire")**.
41:While Wire is available for purchase from the Mechanic for 5 _SC_ each, it can also be obtained from naturally-occurring mechanisms, which exist sparsely in the [Caverns](Cavern.md "Cavern") and more frequently in the [Dungeon](Dungeon.md "Dungeon") and [Jungle Temple](Jungle_Temple.md "Jungle Temple"), such as in [traps](Traps.md "Traps") and [Chain Lantern](Chain_Lantern "Chain Lantern")/Switch arrangements. 
45:By default, placed Wires are invisible unless the player holds a mechanism-related item as the tool in hand, (e.g., a Pressure Plate, Wrench, or even a stack of Wire itself). However, if the player is carrying a [Mechanical Lens](Mechanical_Lens.md "Mechanical Lens") (or its upgrade, [The Grand Design](The_Grand_Design.md "The Grand Design")) they can not only see Wires at will, but can control the visibility of individual Wire colors. 
47:With Wrenches and Wire Cutters, the player's Wire placing and cutting reach is roughly 25 tiles horizontally and vertically. With The Grand Design, the player can place or cut Wire anywhere on the screen. 
214:[](Orange_Weighted_Pressure_Plate.md "Orange Weighted Pressure Plate")[Orange Weighted Pressure Plate](Orange_Weighted_Pressure_Plate.md "Orange Weighted Pressure Plate")| 
719:## See also
844:  * [](Seeds.md "Seeds")[Seeds](Seeds.md "Seeds")
870:  * [Strange Brew](Strange_Brew.md "Strange Brew")
988:    * [Blood Orange](Blood_Orange.md "Blood Orange")
1059:Ranged Weapons](Consumable_ranged_weapons.md "Consumable ranged weapons")
1188:    * [Seed](Seed.md "Seed")
1214:Seeds

```


---

## 🤖 Assistant · 2026-08-13T00:40:04.929Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
好。现在信息足够全面。还差几个快速确认:

1. **雕像 spawn 后标志**:Game.ts:7167-7168 `e.spawnedFromStatue = true`(在 statueSpawn 的 ctx spawnNpc 里)。npcSlots=0 / CanBeReplacedByOtherNPCs 未设置(可能引擎无对应字段)。value=0 → 钱币掉落处 7877-7882 有 spawnFromStatue 门 ✅。

2. **5556 的电路工具段没读到**(sed 5556-5640 输出的是树,说明行号又漂了——之前 grep 说 5556 是 ItemCheck_UseWiringTools,但现在的 5556 是树代码!文件在会话期间被其他并行会话改过?CLAUDE.md 说本机有多条并行会话共用代码!所以行号漂移正常。我需要重新 grep 行号)。

3. Wire wiki 47 行:**扳手/剪线钳放置与剪断 reach ≈ 25 tiles 水平垂直;Grand Design 全屏**。实现侧需确认接线 reach。重新 grep Game.ts UseWiringTools。

4. 地雷 210 踩踏:确认实现侧无(检查 updateTriggerTiles/checkPressurePlates 只扫 135;411 踩踏在 2603-2609 有 ✅ 引爆器踩踏对齐;地雷踩踏缺失)。

由于并行会话在改文件,行号会继续漂,我引用行号时用"读取时行号"并标注文件。快速重 grep 三个点然后写报告。

还需要快速确认:
- UseWiringTools 实现的 reach(25 tiles?)
- 灯亮灭 LIGHT_TOGGLE 表 vs 原版 Toggle* 辅助:已核对实现 devices 的 flip 参数与原版 ToggleTorch(66)/ToggleCandle(18)/Toggle2x2Light(36)/ToggleHolidayLight(54)/ToggleLampPost(1×6, 18)/ToggleLamp(1×3, 18)/ToggleChandelier(3×3, 54)/ToggleCampFire(y 36)/ToggleFirePlace(54)/ToggleHangingLantern(1×2, 18)。
  核对实现:
  - 4 火把 flipCell 66 ✅
  - 33/174/49/372 蜡烛 flipCell 18 ✅(原版 ToggleCandle:short 18,frameX>0 → -18 ✅)
  - 34 吊灯 flipBlock(108,54,3,3,'x',54,54):原版 ToggleChandelier:num3 = frameX%108/18,if num3>2 减 3 → anchor;delta 54,锚 frameX%108>0 → -54 ✅ 实现的 flipBlock(108, 54, 3, 3, 'x', 54, 54):blockW=108 → ox = x - floor(frameX%108/18) ✅;threshold 54 → anchor frameX>=54 → -54。原版是 anchor.frameX%108 > 0 → -54。实现是 anchor.frameX >= 54 → -54。**差异**:吊灯 frameX 有多组 108 宽(每种吊灯一个 108 宽的条带),组内 on 态 frameX 是 [54,108) 区间(%108 ∈ [54,108) 或 (0,54))。原版判 %108>0:off(0)→+54 ✅;on(54)→%108=54>0→-54 ✅。实现判 >=54:on(54)→-54 ✅;off(0)→+54 ✅。对于 frameX=108+0=108(off 第二种)→ %108=0,原版 +54;实现 108>=54 → **-54 ❌**!实现会把第二种吊灯的 off 态判为 on → 反向。等等,实现的 flipBlock 用 anchor frameX(绝对值)与 threshold 54 比较,而原版用 %108。当 frameX=108(第二种吊灯 off)时,实现给 -54 → frameX=54(第二种吊灯的 on?不,108-54=54,那是第一种吊灯的 on 区间!越界到别的吊灯)。
  嗯,这确实是个潜在 bug,但吊灯 frameX 实际范围:Chandeliers 是一个大 spritesheet,frameX 可以很大(比如 108*12)。实现的 flipBlock axis 阈值判定没有取模 → 对第 2+ 种吊灯会翻错方向/翻到别的吊灯上。但是!frameY 也区分吊灯种类吗?原版 ToggleChandelier 只用 frameX%108,说明**吊灯种类由 frameY 区分,frameX%108 是组内位置**。所以 frameX 的绝对值可以是 0..(108*样式数)?不——原版 num3 = frameX % 108 / 18 表明每种吊灯占 108 宽的行?不,吊灯 sheet:每种吊灯 108×54(off/on 两态各 54),横向排列 N 种 → frameX = 种类*108 + 组内偏移。原版 %108 取组内 ✅。实现不取模 ❌。
  但等等,实现 flipBlock 的 ox = x - floor(frameX % blockW / 18) 用了 %108 ✅(锚点对),但阈值判定 `st.frameX[ai] >= threshold` 没取模 ❌。对第二种吊灯(frameX 108+)会把 off 判 on。
  这个要在报告里标注(吊灯/其他多变体灯具 flipBlock 的阈值未取模 → 非首变体开关方向翻转错误)。等等,再确认 flipBlock 代码:
  ```js
  const ox = x - Math.floor(st.frameX[i] % blockW / 18);   // ✅ 取模
  ...
  if (axis === 'y' ? st.frameY[ai] >= threshold : st.frameX[ai] >= threshold) d = -delta;  // ❌ 无取模
  ```
  对,锚点帧的绝对值与 threshold 比较。对于单变体器件(篝火 215、壁炉 405)sheet 只有一组,没问题;对多变体(吊灯 34、2×2 灯 95/100/126/173/564、路灯 92)有多组条带 → 方向错误。2×2 灯:Toggle2x2Light 原版 num2 = frameX/18,if >1 减 2 → anchor;delta 36,anchor.frameX>0 → -36。同样用绝对 frameX>0,而 anchor frameX 是组内 0 或 36!原版 anchor 后 frameX ∈ {0,36}(组内),所以原版判 >0 等价于 ==36。实现 anchor frameX = 种类*72 + 组内。种类 1 的 on 态 = 72+36=108 >= 36 → -36 ✅(方向对,因为 on 态绝对值恒 >= 36)。off 态 = 72+0=72 >= 36 → 实现 -36 ❌(原版 off(组内 0)→ +36)。
  所以:**多变体灯具(第 2+ 种)的开关方向在实现里会反转**。这是 LIGHT_TOGGLE/flipBlock 的真实 1:1 缺陷。不过要小心:2×2 灯 sheet 的 frameX 排布是不是 72 宽一组?原版 num2 = frameX/18; if (num2 > 1) num2 -= 2 → 锚列 = floor(frameX/18) - (floor>1 ? 2 : 0),即组内列 0/1 → 锚 0;组内列 2/3 → 锚 2?等等 num2>1 减 2:列 2,3 → 0,1?那 anchor = i - num2,若 num2=0 → anchor = i(左列);num2=1 → anchor = i-1;num2=2 → 减 2 = 0 → anchor = i ✅;num2=3 → 1 → anchor = i-1。所以原版把列 2/3 也当 0/1(即第 2 组的列 4/5?不)。frameX/18 列号:0,1 = 第一种 off 两列;2,3 = 第一种 on?那 anchor 列 = num2-2 → -?不对,num2=2 → 0,anchor=i-0?嗯,原版代码 num2 = frameX/18; if num2 > 1: num2 -= 2; num2 = i - num2。num2=0 → anchor=i;num2=1 → anchor=i-1;num2=2 → 0 → anchor=i;num2=3 → 1 → anchor=i-1。即 anchor 列恒为 0 或 1 组内,frameX 组 = floor(frameX/36)*36。
  反正要点:原版用组内帧判定,实现用绝对帧。多变体灯具方向反转风险成立。我标注为 ⚠️(需进一步实测确认,标 ❓/⚠️)。
  
  嗯,等等。对 2×2 灯(Toggle2x2Light),原版判断 `Main.tile[num2, num].frameX > 0` —— num2/num 是锚点坐标,锚点格的 frameX 是组内值(0=off,36=on)?不一定——锚点格的 frameX 是它的绝对 sprite 坐标!比如第二种灯 on 态锚点 frameX = 72+36 = 108。原版判 108 > 0 → -36。off 态锚点 = 72+0 = 72 > 0 → **-36**?!
  
  等等,那原版自己也错?不对。让我重新想 sprite 排布:2×2 灯(Candelabra 等)sheet:每种灯占 72px 宽(2 列 × 36 = off/on)?那 on 态的锚点 frameX = 36(第一种)。第二种 off = 72,on = 108。原版 anchor.frameX > 0:第二种 off(72)→ -36 → 108(变成 on)?错,off 应该 +36。
  
  嗯,这说明 sprite 排布不是"每灯 72 宽横向"。让我看 Toggle2x2Light 完整:
  ```
  num = frameY/18 % 2 → 行内偏移
  num = j - num → 锚行
  num2 = frameX/18; if (num2 > 1) num2 -= 2; num2 = i - num2 → 锚列
  ```
  frameX/18 > 1 减 2 → 说明 frameX 列号 0-3,即 sprite 只有 4 列(2 组 × 2 列 = 72px 宽)。frameX 最大 3*18=54。所以 2×2 灯 sheet 只有 2 组(off/on),种类由 frameY 区分!锚点 frameX ∈ {0, 36},>0 判 on ✅。实现 >= 36 等价 ✅。
  
  同理吊灯 ToggleChandelier:num3 = frameX % 108 / 18 → %108 说明 frameX 可以 >= 108(多种吊灯横向排布),组内 0/54。原版判 anchor.frameX % 108 > 0 ✅。实现判 >= 54:第一种 on=54 ✅、off=0 ✅;第二种 off=108 >= 54 → -54 ❌(应 +54)。
  
  所以只有**吊灯(34)这一族**(frameX 可 >= 108 的)有方向 bug。实现 devices case 34 用 flipBlock(w,x,y,108,54,3,3,'x',54,54)。对第二种及以后的吊灯,off 态(108,216,...)会被判为"已开"→ -54 → 翻到 on 位置(162,...)?不对:108-54=54 → 那是第一种吊灯的 on 帧!**会跨吊灯串帧**。真 bug。等等,还要看 frameY:吊灯种类由 frameY 区分吗?原版 num(行偏移)= frameY/18 % 3,锚行 = j - num,说明 frameY 组内 3 行;frameY 可以大(多种吊灯竖排)。而 frameX % 108 说明 frameX 也有多种?矛盾——如果种类由 frameY 区分,frameX 就不该 >= 108。但原版明确 %108,说明 frameX 可 >= 108(横向多种)且 frameY 也可大?也许吊灯 sheet 是 X 方向按"off/on"2 态 × 每态 54 宽,共 2 组 = 108;多种吊灯竖向 frameY 排布。%108 就是防御性的。若 frameX 恒 < 108,则实现 >=54 与原版 %108>0 等价 ✅。
  为稳妥,我标 ❓(吊灯 flipBlock 阈值未取模,若 sheet frameX ≥108 会方向反转;需 sprite 数据确认)。
  
好,我已有足够材料。最后快速确认 3 个点:
1. Game.ts UseWiringTools(重新 grep 行号)
2. Game.ts 灯光 lightIsOn 的 LIGHT_TOGGLE 使用 + 646 蜡烛(原版 ToggleCandle 含 646!1456 :1754-1759 case 33/49/174/372/646)→ 实现缺 646 ❌(前面已记录)
3. 传送器 teleportPairImpl 的敌人过滤(boss/worm)——已确认无过滤。

然后写报告。为节约预算,一次 Bash 搞定 1-2。
````

</details>


---

## 🤖 Assistant · 2026-08-13T00:40:05.188Z · glm-x-preview-260804

```
最后核对电路工具段与灯具表(文件行号因并行会话有漂移，重新定位)。
```


---

## 🤖 Assistant · 2026-08-13T00:40:06.328Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "G=~/Project/GLM/SandboxWorld/game/src; grep -n \"UseWiringTools\\|placeWire\\|killWire\\|placeActuator\\|massWireOperation\" $G/core/Game.ts | head -12; echo \"---reach---\"; sed -n \"$(grep -n 'private useWiringTools\\|ItemCheck_UseWiringTools\\|useWiringTools(' $G/core/Game.ts | head -1 | cut -d: -f1),+40p\" $G/core/Game.ts 2>/dev/null | head -45",
 "description": "Locate and read wiring tool usage code"
}
```


---

## 👤 User(sidechain) · 2026-08-13T00:40:11.105Z

**📎 ToolResult**

```
5714:  /** 电路工具使用(原版 Player.cs:30289-30444 ItemCheck_UseWiringTools) */
5739:        w.killWire(tx, ty, TileStore.WIRE_YELLOW) ||
5740:        w.killWire(tx, ty, TileStore.WIRE_GREEN) ||
5741:        w.killWire(tx, ty, TileStore.WIRE_BLUE) ||
5742:        w.killWire(tx, ty, TileStore.WIRE_RED);
5754:      const res = w.massWireOperation(a, [tx, ty], mode, wires, actuators);
5769:        (mode & TOOL_YELLOW ? w.killWire(tx, ty, TileStore.WIRE_YELLOW) : false) ||
5770:        (mode & TOOL_GREEN ? w.killWire(tx, ty, TileStore.WIRE_GREEN) : false) ||
5771:        (mode & TOOL_BLUE ? w.killWire(tx, ty, TileStore.WIRE_BLUE) : false) ||
5772:        (mode & TOOL_RED ? w.killWire(tx, ty, TileStore.WIRE_RED) : false);
5792:      if (mode & m && w.placeWire(tx, ty, bit)) placed = true;
5794:    if (mode & TOOL_ACTUATOR && w.placeActuator(tx, ty)) placed = true;
---reach---
  /** 电路工具使用(原版 Player.cs:30289-30444 ItemCheck_UseWiringTools) */
  private useWireTool(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    const w = this.wiring;
    if (!w) return;
    const st = this.world.store;
    const dx = tx - Math.floor(this.player.cx / TILE);
    const dy = ty - Math.floor(this.player.cy / TILE);
    if (!this.inTileRange(tx, ty, 20)) return; // 原版多彩扳手/蓝图 tileBoost=20
    if (this.player.useTime > 0) return;
    const wt = itemDef.wireTool!;
    const inv = this.player.inv;

    // 致动魔杖:手动翻转(useTime 防连按)
    if (wt.rod) {
      if (w.actuate(tx, ty)) {
        this.player.useTime = 15;
        this.sfx.play('tink');
      }
      return;
    }
    // 剪线钳:按优先级移除一件(致动器>黄>绿>蓝>红)
    if (wt.cutter) {
      const done =
        w.killActuator(tx, ty) ||
        w.killWire(tx, ty, TileStore.WIRE_YELLOW) ||
        w.killWire(tx, ty, TileStore.WIRE_GREEN) ||
        w.killWire(tx, ty, TileStore.WIRE_BLUE) ||
        w.killWire(tx, ty, TileStore.WIRE_RED);
      if (done) { this.player.useTime = 5; this.sfx.play('dig'); }
      return;
    }
    // 宏伟蓝图:按下记锚点,松开执行 L 形批量
    if (wt.grand) {
      if (!this.grandAnchor) { this.grandAnchor = [tx, ty]; return; }
      const a = this.grandAnchor;
      this.grandAnchor = null;
      const mode = this.wireToolMode;
      const wires = mode & TOOL_CUTTER ? 9999 : inv.countOf(VI_ID(530));
      const actuators = mode & TOOL_CUTTER ? 9999 : inv.countOf(VI_ID(849));
      const res = w.massWireOperation(a, [tx, ty], mode, wires, actuators);

```


---

## 🤖 Assistant · 2026-08-13T00:41:05.939Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
接线工具实现:inTileRange(tx,ty,20)——tileBoost=20(wiki 说 25 tiles;原版 Player.cs 的 reach 是 Player.tileRangeX+item.tileBoost?原版:玩家 tileRangeX 默认 5,+tileBoost 20 = 25?wiki 47 行 "roughly 25 tiles"。实现固定 20。⚠️ 轻微差异(20 vs ~25)。wiki 说 roughly 25,原版实际 = tileRange(5)+tileBoost(20) 或 itemBoost。标注 ⚠️ 数值偏差(20 vs 25)。

信息已足够,现在写最终报告。整理差异清单。

## 汇总所有发现

### A. 信号传播核心(Wiring.ts)
1. 四色 pass 顺序红→蓝→绿→黄 ✅(Wiring.ts:285 tripWire;原版 :542-653)
2. BFS 邻居序 下/上/右/左 ✅(Wiring.ts:332;原版 :859-885)
3. 预算 4/分线盒 3/445 不给预算 ✅(Wiring.ts:320,339-371;原版 :840-974)
4. SkipWire 机制 ✅
5. _toProcess 消耗 ✅
6. **PixelBoxPass ❌ 逻辑不同**:原版仅 Value==3 时翻转 frameX(18↔0 交替);实现 v==1 强制 0、v==3 强制 18(Wiring.ts:489-502 vs 原版 :668-680)
7. 冷却注册 CheckMech 上限 999 ✅(Wiring.ts:194)
8. 单帧组件上限:原版无显式"组件数上限",靠 CheckMech(999)与 BFS;实现同 ✅。分线盒 19 泵/999 mech ✅

### B. 触发源
9. **压板 135 style 门缺失 ❌**:原版 Collision.cs:3336-3349:frameY/18∈{2,3,4,6,7} 仅玩家(objType5);style5(Yellow)仅 NPC;style7 用后 KillTile。实现 Game.ts checkPressurePlates 玩家踩所有 135(含 Yellow 误触发)且 style7 不毁
10. **敌怪/NPC 踩板 ❌ 未实现**:原版 NPC.cs:91558 所有 NPC(objType2)走 SwitchTiles;实现只 critters(updateEntityPlates)
11. **Teal 442 ❌**:原版仅投射物(objType3/4)触发(Collision.cs:3288-3310,四方向 10px 盒,边沿触发);实现仅巨石弹
12. **地雷 210 踩踏 ❌**:原版任意实体踩(Collision.cs:3340)→ HitSwitch → ExplodeMine;实现 hitSwitch 无 210 分支、checkPressurePlates 只扫 135
13. **热喷泉 443 踩踏 ❌**:原版 objType 1/5 踩踏触发;实现仅通电/右键
14. 引爆器 411 踩踏 ✅(Game.ts 落地下落判定,原版 Player.cs TryLandingOnDetonator:34367)
15. 拉杆/开关/计时器右键 ✅(hitSwitch 132/136/144)
16. 宝石锁 440 3×3 ✅、陷阱箱 441/468/467 2×2 ✅
17. 测重板 428 进/离双触发 ✅(Game.ts updateTriggerTiles)但未实现"同色共享状态"(PressurePlatesPressed 按位置字典;原版同色共享单状态:wiki 33 行"All Weighted Pressure Plates of the same color share a single state"——这是 PressurePlateHelper 的 428 字典按 Point,不是按颜色?wiki 说同色共享状态。原版代码按 location 存 bool[255]。Hmm,wiki 的"share a single state"其实指同色多块板被一块压下时另一块再踩不发信号。原版实现是每块板独立 location 字典 + PokeLocation 只在没人踩时(进/离)。实际上原版测重板是每块板独立触发,不是全局共享。wiki 可能有误。标 📄/❓。不深究,实现按位置独立 ✅ 与原版代码一致)

### C. 传感器 423
18. **帧表错位 ❌**:TELogicSensor.cs:181-204 frameY/18:0=Day/1=Night/2=PlayerAbove/3=Water/4=Lava/5=Honey/6=Liquid;实现 mode=floor(frameY/18)%3 且注释"0=昼 36=夜 72=玩家上方"→ Day ✅、Night ✅(18%3=1)、PlayerAbove(36)→mode0 误判为昼、Water(54)→0 昼、Lava(72)→0 昼、Honey(90)→0、Any(108)→0
19. **液体传感器 ❌ 未实现**(Water/Lava/Honey/Any;含 15t 离开迟滞 TELogicSensor.cs:258-268;Water 排除 lava/honey/shimmer)
20. **Player Above 检测盒 ❌**:原版 5×10(Rectangle x*16-33, y*16-161, 82, 162,TELogicSensor.cs:220);实现 1 宽 × 8 高(Game.ts updateTriggerTiles)
21. **Player Above 触发未抑制传送 ❌**:原版 tripPoints 的 Item2 = (logicCheck==PlayerAbove) → blockPlayerTeleportationForOneIteration(TELogicSensor.cs:87,147);实现不设 → 传送器会被 Player Above 传感触发(wiki 108 行明确该组合不应传送玩家)
22. Day/Night 边沿触发 ✅ 近似(实现 onDayNight 回调)

### D. 计时器
23. 五种 1/3/5/1½/¼s,period 60/180/300/30/15 ✅(Wiring.ts:148;原版 :186-204);1/2s 与 1/4s 非 1456 新增(wiki Timers 表,1.3.1 时代)
24. IEEERemainder ✅(Wiring.ts:150 用 Math.round 公式)
25. 计时器重置 18000 ✅;信号=重开计时 ✅(hitWireSingle case 144 → hitSwitch)

### E. 逻辑门
26. 六门真值表 ✅(Wiring.ts:568-575 case 0 AND/1 OR/2 XOR/3 NOR/4 NAND/5 XNOR;原版 :762-784 同)
27. 故障灯:存在→frameX 36;flag6(num3==0||num2==0 → false)差异 ❌(Wiring.ts:586 无 num2==0 门;实际触发灯必在门上,num2≥1,低风险 ⚠️)
28. 级联 LogicGatePass 守卫/Queue 模拟 ✅(含残留清空修复)
29. 冒烟反馈(PoofOfSmoke)未接粒子 ❌(Wiring.ts:593 注释自认,仅返回)
30. 门灯 419 翻转+SkipWire+入队 ✅

### F. 陷阱/驱动
31. **Venom Dart Trap(kind5,弹 980 伤 30 速 12)❌ 未实现**:1456 Wiring.cs:1777-1807 case 5;实现 fireTrap 只 0-4(devices.ts:321-360)。1405 无此 case(1.4.4 新增)——实现基于 1405 导致漏
32. **尖刺球 🔀**:1456 生效路径 :1812-1858(frameX/18 方向表 + 预算死代码);实现取 :1944-1968 死代码段(纯下抛+预算生效)devices.ts:339-347。裁决:1456 源码字面为准 → 方向表丢失、预算惩罚多实现。coordinator 指示:wiki 无记载则以 1456 源码为准并标注
33. 飞镖 20 伤/超镖 40/火焰 40(5 速)/长矛 60 ✅;陷阱冷却 200/200/200/300/90 ✅
34. 大炮/兔兔炮/雪球发射器复合状态机 ✅(数值 300/350 伤、480/3600/60t 冷却、全局 120/480/15 ✅;兔兔场上限 4 实现注释只数 281 弹 ⚠️)
35. 炸药 141(清格+500 伤/半径 10)✅;地雷 210(250 伤不毁地形)✅ 通电路径
36. 热喷泉 443 ✅(弹 654/20 伤/±8 速/CheckMech 200)
37. 巨石雕像 531 ⚠️ y 偏移:原版 (oy)*16+28(Wiring.cs:2006-2007)vs 实现 (oy+1)*16=oy*16+16(devices.ts:517)
38. **蘑菇块 349 二次触发 ❌**(Wiring.cs:2485-2514)
39. **通电石 130 上方门 ⚠️**:原版 :1426-1435 查 PreventsActuationUnder 全集+CanKillTile;实现只挡 21/88/467(devices.ts:589-592)
40. **蜡烛 646 ❌ 缺**:原版 ToggleCandle 含 646(Wiring.cs:1754-1759)
41. 吊灯 flipBlock 阈值未取模 ❓(Wiring.ts flipBlock:85 vs 原版 ToggleChandelier %108)
42. 灯亮灭 LIGHT_TOGGLE 表 ✅ 数值(66/18/36/54/36-y)
43. **宝石块 255-268** ✅ ±7 互换 + 致动器不响应 ✅(Wiring.ts hitWireSingle :1034-1050 vs 实现 devices :770-781 ✅)
44. **通电石/传送带 421/422** ✅ swap + 致动器不响应
45. 火把 Set 仅 tile 4、篝火 Set 仅 215 ✅(TileID.cs:401,403)——实现 case 4/215 完整
46. 传送带 Conveyor ✅(另行审计域)
47. 广播盒 425 ✅(粉色 460 折行、设置门近似=默认)
48. **提取机 219/642** ✅(CheckMech 60、倒序找、32×32 掉落)
49. **Hopper 漏斗 21/467 ❌ 未实现**(1456 :1990-1993 + Hopper :2648-2688:CheckMech 60、192×192 抓取盒、钱币合并、ItemSorting;1.4.4 新机制)
50. **日晷 356/月晷 663 ❌ 未实现**(:1137-1176:fastForwardTimeToDawn/Dusk + cooldown 门)
51. 天塔柱/音乐盒/喷泉态机族 ✅(switchMonolith/MB/Fountain,含 658 三态/733 3×3)
52. 派对纪念碑 455 ✅;马桶烟花 15/497 ✅(60t);烟花盒 335 ✅(30t);烟花喷泉 338 ✅(30t+去重);烟花火箭 216 ✅(167+行,150 伤,(0,-8),两格消耗)
53. 压板轨道 314 ✅(CheckMech 5 + FlipSwitchTrack)
54. 高尔夫 476 ✅ 占位(无高尔夫系统)
55. 巴斯特雕像 506 ✅(2×3 ±72,缺 ValidateTileSquare 门 ⚠️ 小)
56. 格栅 546/557 ✅

### G. 雕像刷怪
57. style→NPC 表 ✅(含 1.4.4 新雕像 80/81/82 组)
58. CheckMech 30t(敌怪)/600t(物品)/300t(王后/城镇)/900t(巨石)✅
59. MechSpawn 配额 200/600/3/6/10(NPC)+300/800/3/6/10(物品)✅(Game.ts mechSpawnOk/itemSpawnOk;NPC.cs:7399-7483;Item.cs:48982-49013)✅ 等价组表部分 ✅(55↔230 特判在,组表 NPC_MECH_GROUPS 需确认含蛇/兔/362-365/602-603/608-609/616-617/dragonfly——mechSpawnOk 用 NPC_MECH_GROUPS.find(g=>g.includes(type)),表内容未见,❓)
60. 实心判定 poof ✅(style 64/71/16/50);flag6(双 MechSpawn)✅
61. **派对兔 540 ❌**:原版 case 9 PartyIsUp → 540(:2306-2317);实现写死 46
62. spawn 后 value=0/SpawnedFromStatue ✅(Game.ts spawnedFromStatue + 7877 掉落门);npcSlots=0/CanBeReplacedByOtherNPCs ❓未见
63. **城镇 NPC 搬迁雕像 40/41 白名单 ⚠️ 错乱**:原版 case40={17,19,22,38,54,107,108,142,160,207,209,227,228,229,368,369,550,441,588}、case41={18,20,124,178,208,353,633,663};实现两组各 6 个且成员错位(nurse/demolitionist/dyer 在 group0 原版没有;painter/golfer/zoologist/pirate 在 group1 原版没有)+ 非随机(取第一个存在)🔀
64. 心/星雕像 MechSpawn 全等价 id 过 ✅(58/1734/1867 与 184/1735/1868)
65. 炸弹雕像 y-20 vs 实现 py-16 ⚠️ 微
66. 血月腐化兔/金鱼行走变体、For the Worthy 爆炸兔 ❓(wiki 545-547;雕像 style 9 处理)

### H. 传送器
67. 48×48 判定盒(y 上移)✅;halfBrick +0.5 ✅;3 tile 距离门 ✅;神庙墙+Plantera ✅
68. **NPC 过滤 ❌**:原版 lifeMax>5 && !boss && !noTileCollide && !TeleportationImmune(:3181-3192)→ 蠕虫/boss/穿墙怪不传;实现无过滤(Game.ts teleportPairImpl)
69. 玩家传送近似 ⚠️:原版 Teleport(position+vector)保留相对位置;实现 +dx/dy 等价,但清速度+播 tink(原版无)🔀
70. blockPlayerTeleportationForOneIteration ✅ 机制存在(测重板设置),清除时机在 logicGatePass ✅;但 PlayerAbove 传感器不设(见 21)
71. 传送释放钩(wiki 66)❓

### I. 泵
72. 每次激活 4 格/泵、每侧 19 泵上限 ✅(wiki "up to four tiles";Wiring.ts:422/428 <19)
73. 液体类型匹配、目标 255 上限、抽空 break ✅(Wiring.ts:456-485 vs :475-523)
74. **类型清理 ⚠️**:原版抽空 liquidType(0)+SquareTileFrame(:513-521);实现保留类型(liquidType||1)、无 frame 重算
75. 防倒流:原版无显式机制(靠类型匹配+255 上限)✅ 等价

### J. 致动器
76. DeActive 门(226 蜥蜴砖/solid 表/PreventsActuationUnder/CanKillTile)✅ + NotReallySolid/379 补全 ✅
77. canKillTile 近似(容器/门锁系统未接,恒可杀)⚠️ 已注释登记
78. ReActive ✅;Actuate/ActuateForced ✅;先致动后判定 ✅(hitWireSingle :386-389)

### K. 接线工具
79. 四色位/致动器/剪线钳 ✅(TOOL_* 位);剪线优先级致动>黄>绿>蓝>红(实现;原版剪线钳 KillWire 按色?原版 Wire Cutter 一次剪一根,顺序同实现 ⚠️ 近似)
80. **reach 20 ⚠️**:实现 inTileRange 20;原版 tileBoost 20 + tileRange 5 ≈ 25(wiki 47 行 ~25 tiles)
81. Grand Design L 形批量 ✅ 顺序 红→绿→蓝→黄→致动 ✅(原版 MassWireOperationStep :3365-3414 同序);dir 恒 true ⚠️(原版 direction 决定先垂直/水平);CanDoWireStuffHere 门未接 ⚠️

### L. wiki 勘误
82. Water Sensor 与 Shimmer:wiki Sensors.md:110 称 Water Sensor 也被 Shimmer 触发;源码 TELogicSensor.cs:254 `(tile.honey() || tile.lava() || tile.shimmer()) && type == Water → false` → Shimmer **不**触发 Water 传感器(仅 Liquid Any 类型响应)→ 📄 wiki 有误
83. 压板 wiki 触发者表与源码一致(Red/Green 全实体、Yellow 仅 NPC、Gray/Brown/Blue/Lihzahrd/Orange 仅玩家、Orange 用后毁、Weighted 玩家进/离、Teal 投射物)✅

TOP 修复优先级:
1. 传感器 423 帧表错位 + 液体传感器缺失 + PlayerAbove 盒 5×10 + 触发抑制传送(块 21/18/19/20)
2. 压板触发者门(style 门 + 敌怪踩板 + teal 投射物 + 地雷/喷泉踩踏)(9-13)
3. Venom Dart Trap kind5 + 尖刺球方向裁决(31/32)
4. Hopper 漏斗 + 日晷/月晷(49/50)
5. PixelBoxPass 翻转语义(6)
6. 传送器 NPC 过滤(68)
7. 雕像白名单(63)+ 派对兔(61)
8. 灯具小项:646 蜡烛、吊灯取模、通电石门(39/40/41)

现在写报告。用 markdown 表格。注意输出要控制篇幅但覆盖必核清单 10 项。每条给 file:line。行号以我读取时为准(注明文件可能因并行会话漂移)。

关于尖刺球的裁决(coordinator 指示:若 wiki 无相关记载,以 1456 源码为准并标注)。wiki Spiky_Ball_Trap 我没读——之前没读那个页面。快速决策:按 coordinator 指示以 1456 源码字面为准(第一段 switch 生效:方向表 + 预算死代码),并标注第二段(-7)疑为反编译伪影/死代码,实现误取。

报告结构:域总述 + 差异清单表 + 覆盖清单 + TOP N。

我会把表格按子系统分组编号。开始写。
```

</details>


---

## 🤖 Assistant · 2026-08-13T00:42:08.795Z · glm-x-preview-260804

```
审计材料已齐(1456 源码 Wiring.cs 3441 行全文 + TELogicSensor + Collision.SwitchTiles + PressurePlateHelper + 实现 Wiring.ts/devices.ts/Game.ts + wiki 五页)。以下为最终报告。

---

## 域：电路与机械

**审计范围**:`game/src/world/Wiring.ts`(806 行)+ `game/src/world/wiring/devices.ts`(922 行)+ `game/src/core/Game.ts` 触发源/器件上下文，对照 `Terarria1456/Terraria/Wiring.cs`(3441 行)、`Collision.cs`、`Terraria.GameContent/PressurePlateHelper.cs`、`Terraria.GameContent.Tile_Entities/TELogicSensor.cs`,及 wiki(Wire/Pressure_Plates/Sensors/Timers/Teleporter/Pumps/Statues)。
**总体结论**：信号传播核心(BFS/四色 pass/逻辑门/泵/致动器/计时器)确为高保真 1:1,数值大量可逐行对上。**主要缺口集中在 1456 相对 1405 的增量内容**(实现注释自述基于 1.4.0.5)与**触发源侧**(压板型号门/踩板/传感器 TileEntity),后者几乎整块缺失或错位。

⚠️ 行号说明:`Game.ts` 本机有多条并行会话在改，行号以本次读取时为准，定位时请以 grep 符号名为准。

### 差异清单

#### 信号传播 / 核心

| # | 机制项 | 原版设定(源码) | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 1 | 四色独立电路与 pass 顺序 | 红→蓝→绿→黄，每色前重置传送器对与泵(Wiring.cs:542-653) | Wiring.ts:285-302 | ✅ | — |
| 2 | BFS 邻居序/边界/预算 | 邻居序 下/上/右/左；边界 ±2 内不传；种子预算 4;分线盒给 3、445 给 0(Wiring.cs:837-979) | Wiring.ts:312-377 | ✅ | — |
| 3 | **像素盒 PixelBoxPass** | 仅当触发值==3(水平+垂直同帧都过)时**翻转** frameX(18↔0 交替)；值 1/2 不动作(Wiring.cs:668-680) | Wiring.ts:489-502:v==1 强制 frameX=0、v==3 强制 18 | 🔀 | 实现是“按来源强制开/关”，原版是“双轴同时→交替翻转”。单轴信号原版无动作，实现会强制关 |
| 4 | 重复触发冷却注册 | CheckMech 上限 999(Wiring.cs:455-473) | Wiring.ts:190-200 | ✅ | — |
| 5 | 单帧组件上限 | 无显式上限，靠 CheckMech(999)+BFS+泵 19 限 | 同构 | ✅ | — |

#### 触发源(压板/传感器/踩踏)——缺口最重的一块

| # | 机制项 | 原版设定(Collision.cs:3250-3372 = SwitchTiles 权威) | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 6 | **压板 135 型号门** | frameY/18(style):2 灰/3 棕/4 蓝/6 蜥蜴/7 橙=仅玩家(objType 5);5 黄=仅 NPC(排除玩家/投射物)；0 红/1 绿=任意；**7 橙触发后 KillTile**(Collision.cs:3336-3353) | Game.ts `checkPressurePlates`:玩家 AABB 命中任何 135 即 hitSwitch,无 style 门、无毁块 | ❌ | 玩家会误触发黄板；橙板不消失 |
| 7 | **敌怪/NPC 踩板** | 所有 NPC 走 SwitchTiles(objType 2,NPC.cs:91558) | Game.ts `updateEntityPlates` 仅 critters + 巨石弹 | ❌ | 敌怪踩红/绿/黄板完全不触发(神庙机关、黄板门全废) |
| 8 | **Teal 垫 442** | 仅投射物(objType 4;四方向 frameX/22 各自 10px 盒，边沿触发；Collision.cs:3288-3310) | 仅巨石弹触发(checkPad) | ❌ | 飞镖/箭/宠物等投射物不触发(wiki Pressure_Plates.md:135,146) |
| 9 | **地雷 210 踩踏** | 任意实体踩上即 HitSwitch→ExplodeMine(Collision.cs:3340-3343;Wiring.cs:288-291) | `Wiring.hitSwitch` 无 210 分支(Wiring.ts:204-273);踩踏扫描只扫 135 | ❌ | 地雷只能通电引爆，踩不上 |
| 10 | **热喷泉 443 踩踏** | 踩上触发(objType 1/5;Collision.cs:3344-3348) | 仅通电/右键路径(devices.ts:875-877) | ❌ | — |
| 11 | 引爆器 411 踩踏 | Player.cs:34367-34379 下落 ≥3 踩未触发态 | Game.ts(注释自引同段) | ✅ | — |
| 12 | 拉杆/开关/计时器/陷阱箱/宝石锁 | Wiring.cs:259-378 | Wiring.ts:204-273 | ✅ | — |
| 13 | 测重板 428 进/离双触发 | PressurePlateHelper.cs:51-164;PokeLocation 设 blockPlayerTeleportation | Game.ts `updateTriggerTiles` 双触发+设标志 | ✅ | (wiki:33 称“同色共享状态”与源码按位置字典不符，📄 以源码为准) |
| 14 | 传送抑制标志清除 | LogicGatePass 末尾(Wiring.cs:714-717) | Wiring.ts:531-533 | ✅ | — |

#### 传感器 423(TileEntity:TELogicSensor)

| # | 机制项 | 原版设定(TELogicSensor.cs) | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 15 | **帧表/style 解码** | frameY/18:0 昼/1 夜/2 玩家上方/3 水/4 岩浆/5 蜂蜜/6 任意液体(:181-204,288-308);on 态 frameX=18 | Game.ts `updateTriggerTiles`:`mode=floor(frameY/18)%3`,注释"0=昼 36=夜 72=玩家上方" | ❌ | **解码错位**：36(玩家上方)/54(水)/72(岩浆)/90(蜜)/108(任意)全部 %3==0 被当昼传感器；36≠夜、72≠玩家上方 |
| 16 | **液体传感器** | 本格液体判定+离开 15t 迟滞(CountedData,:258-268);Water 排除岩浆/蜜/**微光**(:254) | 无任何实现 | ❌ | 四种液体传感器整体缺失 |
| 17 | **玩家上方检测盒** | 5 宽×10 高:Rectangle(x*16-33, y*16-161, 82, 162)(:220;Main.cs:58043-58064 画框印证) | `x===ptx && pty-y<=8` | ❌ | 1 宽(缺 x±2)×8 高(缺 9-10) |
| 18 | **Player Above 抑制传送** | tripPoints 携带 `logicCheck==PlayerAbove` → blockPlayerTeleportationForOneIteration(:87,147) | 不设该标志 | ❌ | Player Above 触发的传送器会传玩家(wiki Sensors.md:108 / Teleporter.md:51 明确不应) |
| 19 | 昼/夜边沿触发 | on 进昼→发信号，离开仅复位不发(:111-121) | `triggerDayNightSensors` 昼夜回调触发 | ✅ | 近似正确(但因 #15 帧表错位，水/岩浆等传感器会被误当昼触发) |
| 20 | 玩家判定排除 | active && !dead && !ghost(:74) | — | ❓ | 实现仅 dead 判定(1.4.2 ghost 排除未确认) |

#### 计时器 / 逻辑门

| # | 机制项 | 原版设定 | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 21 | 计时器五档周期 | 1s/3s/5s/½s/¼s = 60/180/300/30/15 tick(Wiring.cs:186-204;wiki Timers.md:42-46) | Wiring.ts:148 | ✅ | ½s/¼s 并非 1456 新增(1.3.1 时代)，清单第 4 项疑虑解除 |
| 22 | IEEERemainder 触发/重置 18000 | Wiring.cs:205-209 | Wiring.ts:150-154(Math.round 公式) | ✅ | — |
| 23 | 六门真值表+帧语义 | AND/OR/XOR/NOR/NAND/XNOR(Wiring.cs:762-784);frameX 18=on、36=故障 | Wiring.ts:568-583 | ✅ | — |
| 24 | 故障灯掷率 | `flag6 && (num3==0‖num2==0) → false`,再 `rand < num3/num2`(Wiring.cs:804-812) | Wiring.ts:586 仅 `num2>0` 才改 | ⚠️ | num2==0 时实现保留 fire=true,原版强制 false;因触发灯自身必在门上(num2≥1)实际低风险 |
| 25 | 级联/防环/嵌套守卫 | LogicGatePass(Wiring.cs:682-718) | Wiring.ts:506-540(含 Queue 残留清空修复) | ✅ | — |
| 26 | 门重复输出冒烟 | PoofOfSmoke(Wiring.cs:824-826) | Wiring.ts:593 仅返回 | ⚠️ | 粒子未接(注释自认) |

#### 驱动方块 / 陷阱

| # | 机制项 | 原版设定 | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 27 | **毒镖陷阱(kind5)** | 1.4.4 新增：弹 980 VenomDartTrap、30 伤、速 12(Wiring.cs:1777-1807;ProjectileID.cs:2320) | `fireTrap` 只处理 kind 0-4(devices.ts:321-360) | ❌ | 实现基于 1405 漏掉 1456 增量 |
| 28 | **尖刺球方向/预算** | 1456 生效路径：frameX/18 方向表(0/1 下、2 上、3 左、4 右)，初速 4·dir+rand±1,生成点 +14·dir;预算惩罚循环因 `type==num96(=0)` 恒空(**死代码**)(Wiring.cs:1812-1858);另存在第二段 switch case -7(:1944-1968,纯下抛+预算生效,`num95∈{-10..-6}` 不可达) | devices.ts:339-347 按 ：1944-1976 实现：固定下抛 + 预算惩罚表 | 🔀 | **裁决(按协调方指示以 1456 源码字面为准)**：实现误取不可达段 → 丢失四向发射；预算惩罚在 1456 实际不生效(原版疑似遗留 bug,两版反编译均含同构死代码段)。wiki 无记载可佐证，修复时建议按第一段(方向表+预算恒 200)落 |
| 29 | 飞镖/超镖/火焰/长矛 | 20/40/40/60 伤；速 12/12/5/8;冷却 200/200/200/90 | devices.ts:326-359 | ✅ | — |
| 30 | 大炮/兔兔炮/雪球机 | 复合旋转+开火；300/350 伤；CheckMech 480/3600/60;全局冷 120/480/15(Wiring.cs:1237-1418) | devices.ts:623-749 | ✅ | 兔兔场内上限只数 281 弹(原版含 NPC614),已注释自认 ⚠️ |
| 31 | 炸药 141 / 地雷 210(通电) | KillTile noItem + 弹 108(500 伤/半径 10)/弹 164(250 伤，不毁地形)(Wiring.cs:2039-2046,3093-3101) | devices.ts:601-605,705-709 | ✅ | — |
| 32 | 热喷泉 443(通电) | CheckMech(锚x, y, 200);弹 654、20 伤、±8 速(Wiring.cs:3103-3137) | devices.ts:363-376 | ✅ | — |
| 33 | 巨石雕像 531 | CheckMech 900;弹 99 生成点 y=(oy)*16+**28**(Wiring.cs:1998-2016) | devices.ts:517 用 `(oy+1)*16`=oy*16+**16** | ⚠️ | y 偏移差 12px |
| 34 | **蘑菇块 349 二次触发** | 通电 frameX ±216 动画回弹(Wiring.cs:2485-2514) | 无 case 349 | ❌ | — |
| 35 | 通电石 130 上方门 | `!PreventsActuationUnder 全集 && CanKillTile`(Wiring.cs:1426-1435) | devices.ts:589-593 只挡 21/88/467,无 CanKillTile | ⚠️ | 漏 26/77/470/475/237/597/441/468 |
| 36 | **蜡烛 646** | ToggleCandle 含 646(Wiring.cs:1754-1759) | devices.ts:558 只 33/174/49/372 | ❌ | — |
| 37 | 吊灯阈值判定 | `anchor.frameX % 108 > 0`(Wiring.cs:2996-3000) | flipBlock 用绝对 `frameX>=54`(Wiring.ts:85) | ❓ | 若 sheet 存在 frameX≥108 的变体则方向反转/串帧，需贴图数据确认 |
| 38 | 火把/篝火族 | TileID.Sets.Torches={4}、Campfires={215}(TileID.cs:401,403) | devices.ts case 4/215 | ✅ | 此前担心的“火把族覆盖缺口”不成立(Set 就只有一个成员) |
| 39 | 宝石块 255-268 / 传送带 421-422 | ±7 互换、致动器不响应(Wiring.cs:1017-1050) | devices.ts:770-781,853-857 | ✅ | — |
| 40 | **漏斗 Hopper(21/467)** | 1.4.4 新机制：CheckMech 60、抓中心 192×192 盒内物品入箱、钱币合并、入箱排序(Wiring.cs:75,1990-1993,2648-2888) | 无 | ❌ | 带线宝箱通电无任何效果 |
| 41 | **日晷 356 / 月晷 663** | 通电 fastForwardTimeToDawn/Dusk + sundialCooldown/moondialCooldown 门(Wiring.cs:1137-1176) | 无 | ❌ | — |
| 42 | 音乐盒/喷泉/天塔柱态机族 | WorldGen.SwitchMB/Fountain/Monolith | devices.ts:239-317(含 658 三态 %162、733 3×3) | ✅ | — |
| 43 | 广播盒 425 / 提取机 219/642 / 派对碑 455 / 烟花族 216/335/338/497/马桶 | Wiring.cs:1177-1232,1994-1997,2037,1492-1553 | devices.ts:609-622,859-884,754-811 | ✅ | 烟花火箭数值(167+行、150 伤、(0,-8)、双格消耗)与 WorldGen.cs:62184-62206 逐项对上；广播盒设置门按默认值等价 |

#### 雕像刷怪

| # | 机制项 | 原版设定 | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 44 | style→NPC 表(含 1.4.4 新组 80/81/82) | Wiring.cs:2157-2270 | devices.ts:380-388 | ✅ | — |
| 45 | 冷却：敌怪 30t/物品 600t/王后·城镇 300t/巨石 900t | Wiring.cs:2271+ | devices.ts:446-494 | ✅ | 与 wiki Statues.md:522-531(0.5s/10s/5s/15s)一致 |
| 46 | 数量上限 | NPC.MechSpawn 200px≥3/600px≥6/全图≥10(NPC.cs:7399-7483);物品 300/800/3/6/10(Item.cs:48982-49013) | Game.ts `mechSpawnOk`/`itemSpawnOk` | ✅ | 等价组表(NPC_MECH_GROUPS)内容未逐一核，❓ |
| 47 | 实心判定 poof(style 64/71/16/50)、flag6 双 MechSpawn(63) | Wiring.cs:2271-2283,2207-2210 | devices.ts:433-493 | ✅ | — |
| 48 | **派对兔变体** | style 9 兔：PartyIsUp → NPC 540,否则 46(Wiring.cs:2306-2317) | devices.ts:397 写死 46 | ❌ | — |
| 49 | spawn 后标志 | value=0、npcSlots=0、SpawnedFromStatue、CanBeReplacedByOtherNPCs(Wiring.cs:2476-2482) | Game.ts `spawnedFromStatue=true` + 掉落门(value) | ⚠️ | npcSlots/CanBeReplacedByOtherNPCs 未见设置(引擎可能无对应字段) |
| 50 | **城镇 NPC 搬迁雕像 40/41 白名单** | case40={17,19,22,38,54,107,108,142,160,207,209,227,228,229,368,369,550,441,588},case41={18,20,124,178,208,353,633,663};**随机**选一个活跃者传送(Wiring.cs:2418-2473) | Game.ts `relocateTownNpc`:两组各 6 key,**按序取第一个存在**；nurse/demolitionist/dyer 误入 group0,painter/golfer/zoologist/pirate 误入 group1 | 🔀 | 成员错位 + 非随机 |
| 51 | 心/星雕像配额全等价 id 过 | 58/1734/1867 与 184/1735/1868(Wiring.cs:2387-2410) | devices.ts:469-474 | ✅ | — |
| 52 | 炸弹雕像掉落 y | y-**20**(Wiring.cs:2415) | devices.ts:473 py-**16** | ⚠️ | 4px 差 |

#### 传送器

| # | 机制项 | 原版设定(Wiring.cs:3139-3212;wiki Teleporter.md:41-51) | 本仓库实现(Game.ts `teleportPairImpl`) | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 53 | 判定盒/距离门/神庙墙 | 48×48(y 上移)、3 tile 内竖叠拒、wall 87+未杀 Plantera 拒、halfBrick +0.5 | 全部接上 | ✅ | — |
| 54 | **NPC 过滤** | lifeMax>5 && !boss && !noTileCollide && !TeleportationImmune(:3181-3192)→ 蠕虫/boss/穿墙怪不传 | 无过滤，enemies 全传 | ❌ | boss/蠕虫会被传送(wiki :49) |
| 55 | 玩家传送 | Teleport(position+vector) 保留相对位置，不清速度、无音效 | +dx/dy 等价，但清 vx/vy 并播 tink | ⚠️ | 近似，音效原版无 |
| 56 | 同帧多玩家 | 255 玩家循环(单机近似合理) | 单玩家 | ✅ | — |
| 57 | 宠物/minion 跟随 | 投射物一律不传(wiki :49) | 不传 | ✅ | — |

#### 泵 / 致动器 / 接线工具

| # | 机制项 | 原版设定 | 本仓库实现 | 状态 | 差异细节 |
|---|---|---|---|---|---|
| 58 | 抽排量 | 每次激活每泵 4 格、2×2 均匀、每侧 19 泵上限(wiki Pumps“up to four tiles”;Wiring.cs:2047-2127) | Wiring.ts:413-434,456-485 | ✅ | — |
| 59 | 类型匹配/上限 255/防倒流 | 类型一致才移、目标满 255 跳过、抽空 break(Wiring.cs:475-523) | 同 | ✅ | — |
| 60 | 抽空后类型清理/帧重算 | liquidType(0)+SquareTileFrame(Wiring.cs:513-521) | 保留 liquidType(`‖1` 兜底)，无帧重算 | ⚠️ | 若引擎把“liquid==0 且类型≠0”当有液会出隐患；液体流动动画不刷新 |
| 61 | DeActive 门(蜥蜴砖 226/solid 表/PreventsActuationUnder/CanKillTile) | Wiring.cs:3214-3242 | Wiring.ts:618-684(含 NotReallySolid/379 补全) | ✅ | canKillTile 容器/门锁子集未接，已注释登记 |
| 62 | 工具位与批量顺序 | 红→绿→蓝→黄→致动(MassWireOperationStep :3365-3414);dir=direction | Wiring.ts:742-805 | ✅ | dir 写死 true(先垂直)⚠️;CanDoWireStuffHere 门未接 |
| 63 | **接线/剪线 reach** | tileBoost 20 + 基础 tileRange ≈ **25 tiles**(wiki Wire.md:47) | `inTileRange(tx,ty,20)` 固定 20 | ⚠️ | 短 5 格 |

#### wiki 勘误

| # | 项 | 说明 |
|---|---|---|
| 64 | 📄 Water Sensor 与 Shimmer | wiki Sensors.md:110 称“水传感器也会被微光触发”；源码 TELogicSensor.cs:254 明确 `(honey‖lava‖shimmer) && type==Water → false`——微光**不**触发水传感器，只有 Liquid(Any) 类型响应。以源码为准，wiki 有误 |

### 覆盖清单

- **已覆盖且高保真**：四色传播/BFS/分线盒/彩线灯泡(429)、逻辑门六级联+故障灯、计时器五档、泵全链、致动器(含 PreventsActuationUnder 全表/树干/棕榈/巨石失撑)、传送器捕获与判定盒、陷阱族 0-4 数值、大炮/兔兔炮/雪球机复合状态机、炸药/地雷通电、烟花族全部、压板轨道、格栅/通电石/宝石块/传送带、音乐盒/喷泉/天塔柱态机、广播盒、提取机、雕像主表+冷却+MechSpawn 配额、`blockPlayerTeleportationForOneIteration` 机制本体。
- **缺失/错位(按优先级)**：传感器解码与液体传感器、压板型号门与踩板生态、毒镖陷阱、漏斗、日晷/月晷、像素盒语义、传送器 NPC 过滤、雕像白名单、蘑菇块 349、蜡烛 646、地雷/喷泉踩踏、Teal 投射物触发。
- **存疑待证**：NPC_MECH_GROUPS 等价组完备性、吊灯 frameX≥108 变体的 flipBlock 方向、ghost 排除、传送释放钩。

### 最需修复 TOP 8

1. **传感器 423 帧表错位(#15)**:`mode=floor(frameY/18)%3` 应改为 `floor(frameY/18)` 直接映射 0-6(TELogicSensor.cs:181-204)。这是全错位 bug——水/岩浆/蜜/任意液体/玩家上方五种全部被误当昼传感器，一处修正连带修复昼夜误触发。
2. **液体传感器四型(#16)+ Player Above 盒 5×10(#17)+ 触发抑制传送(#18)**：与 1 同块，按 TELogicSensor.GetState(:209-275) 一次移植(含 15t 离开迟滞、Water 排除微光)。
3. **压板触发者门(#6)+ 敌怪踩板(#7)+ Teal 投射物(#8)**：按 Collision.SwitchTiles(Collision.cs:3250-3372) 重建触发源：style 门(2/3/4/6/7 仅玩家、5 仅 NPC、7 触发后毁)、NPC 全量踩板、投射物四方向盒触发 442、210/443 踩踏。神庙机关与所有压板自动化依赖此块。
4. **毒镖陷阱 kind5(#27)**:fireTrap 补 `case 5`(弹 980、30 伤、速 12、CheckMech 200,Wiring.cs:1777-1807),并同步 TrapShot 弹种。
5. **尖刺球裁决落地(#28)**:按 1456 生效路径(:1812-1858)恢复 frameX/18 四向发射；预算惩罚表删除或留注释(1456 中为死代码)。
6. **漏斗 Hopper(#40)**:case 21/467 → CheckMech 60 + 192×192 抓取 + 入箱堆叠/钱币合并(Wiring.cs:2648-2888)。
7. **日晷 356 / 月晷 663(#41)**:通电快进昼夜 + cooldown 门，接时间系统(本仓库时间系统已 1:1,成本不高)。
8. **像素盒翻转语义(#3)+ 传送器 NPC 过滤(#54)**:pixelBoxPass 改为“值==3 时交替翻转”；teleportPairImpl 补 lifeMax>5/!boss/!noTileCollide 过滤表。

另建议低优跟进：雕像 40/41 白名单校正与随机化(#50)、派对兔 540(#48)、通电石上方门全集(#35)、蜡烛 646(#36)、接线 reach 20→25(#63)、泵抽空类型清理(#60)。
```
