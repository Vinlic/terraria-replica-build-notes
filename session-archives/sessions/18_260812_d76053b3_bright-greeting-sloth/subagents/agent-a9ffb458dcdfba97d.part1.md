# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T15:52:00.899Z

```
在 ~/Project/GLM/SandboxWorld/game 做一次 very thorough 只读探索。背景:项目要废弃 172 个"本地自制物品"(data/items.ts 非 vi_ 前缀定义,如 'wood'/'gel'/'copper_bar'/'wood_pickaxe'/'torch'/'door' 等),全部迁移到原版 vi_<id> 空间。我需要这些本地 key/物品被代码引用的全部位置清单。

请 grep 全 src/(含 ui/、core/、entities/、world/、data/、net/、save/)与 tests/,分类报告(带 file:line):
1. **硬编码 key 引用**:形如 'wood'/'gel'/'copper_bar'/'iron_bar'/'lens'/'torch'/'platform'/'door'/'workbench'/'furnace'/'anvil'/'chest'/'coin_copper' 等本地 key 字符串出现的所有位置(ITEM_BY_KEY[...]、TILE_BY_KEY 无关、vanillaItemKey、掉落、配方、UI 判断)。注意区分:字符串恰好是 tile key(如 'torch' 作为 tile)还是 item key——TILE_BY_KEY['torch'] 是 tile 不用迁,ITEM_BY_KEY['torch'] 是 item 要迁。
2. **recipes.ts 自制配方表**:全部消费方(UI.refreshCrafting 的 RECIPES 段、Game.canCraft/craft/stationsNearby)。如果废弃 RECIPES 表,哪些功能会消失(早期合成链)?UI 的"── 原版配方 ──"段是否已能独立支撑?
3. **物品使用链**:本地工具/武器(wood_pickaxe/copper_pickaxe/iron_sword 等)的使用逻辑——tool 类型判定(ITEM_DEFS[].tool)、挖掘力、挥舞伤害,是否已经走 vanillaItemStats/vanillaItemCombat 的 vid 数据驱动(即 vi_ 物品已有同能力)?本地 magic/ranged 定义(magic_missile?)与 vi_ 版本能力对比。
4. **存档**:save/ 目录 serialize/loadSave 中玩家背包(inventory slots/armor/banks/piggy)怎么存物品(内部 id? key?);CharacterStore 初始装备;存档加载有没有已有的 id 迁移/版本机制(老存档兼容先例)。删掉本地定义后老存档会怎样。
5. **联机**:net/protocol 里物品 id 同步是否走内部 id。
6. **图标**:SpriteAtlas 图标解析对非 vi_ key 的路径(atlasIconForKey 的 fallback 链、VANILLA_ITEM_ICON_MAP),本地物品现在的图标哪来的。
7. **tests**:引用本地 key 的测试文件清单(迁移后要同步改)。
8. **SmartSelect/放置链**:placeTile 放置物品怎么从 item 找 tile(item.tile 字段 vs vi_ 物品的 createTile 反查),本地的 tile 字段 vs 原版 place 链差异。

输出结构化报告,按上面 8 类,每类列 file:line 与简述。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T15:52:00.900Z

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

## 🤖 Assistant · 2026-08-12T15:52:02.824Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the directory structure to understand the codebase layout.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:03.115Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game -type f -name \"*.ts\" -not -path \"*/node_modules/*\" | head -100",
 "description": "List TypeScript files in project"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:03.188Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/vite.config.ts
~/Project/GLM/SandboxWorld/game/tools/_dungeonside.test.ts
~/Project/GLM/SandboxWorld/game/tools/_biohang.test.ts
~/Project/GLM/SandboxWorld/game/tools/_fullhang.test.ts
~/Project/GLM/SandboxWorld/game/tools/_sidecheck.test.ts
~/Project/GLM/SandboxWorld/game/tools/_junglehang.test.ts
~/Project/GLM/SandboxWorld/game/tests/torch.test.ts
~/Project/GLM/SandboxWorld/game/tests/character-store.test.ts
~/Project/GLM/SandboxWorld/game/tests/cs-compat.test.ts
~/Project/GLM/SandboxWorld/game/tests/wld-furnace-mapping.test.ts
~/Project/GLM/SandboxWorld/game/tests/dart-proj-styles.test.ts
~/Project/GLM/SandboxWorld/game/tests/fishing-r7.test.ts
~/Project/GLM/SandboxWorld/game/tests/projectile-reflect.test.ts
~/Project/GLM/SandboxWorld/game/tests/env-hazards-util.ts
~/Project/GLM/SandboxWorld/game/tests/lategame-subsystems.test.ts
~/Project/GLM/SandboxWorld/game/tests/minecart-track.test.ts
~/Project/GLM/SandboxWorld/game/tests/proj-critter-hit.test.ts
~/Project/GLM/SandboxWorld/game/tests/_sandchk.test.ts
~/Project/GLM/SandboxWorld/game/tests/bestiary.test.ts
~/Project/GLM/SandboxWorld/game/tests/waterfall-draw.test.ts
~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts
~/Project/GLM/SandboxWorld/game/tests/a-batch1.test.ts
~/Project/GLM/SandboxWorld/game/tests/_ghost.test.ts
~/Project/GLM/SandboxWorld/game/tests/lang.test.ts
~/Project/GLM/SandboxWorld/game/tests/dungeon-ai.test.ts
~/Project/GLM/SandboxWorld/game/tests/luck-system.test.ts
~/Project/GLM/SandboxWorld/game/tests/boss-hostile-proj-sim.test.ts
~/Project/GLM/SandboxWorld/game/tests/smart-cursor.test.ts
~/Project/GLM/SandboxWorld/game/tests/world-final-hash.test.ts
~/Project/GLM/SandboxWorld/game/tests/world-difficulty.test.ts
~/Project/GLM/SandboxWorld/game/tests/pass-hash.test.ts
~/Project/GLM/SandboxWorld/game/tests/enemy-ai-families.test.ts
~/Project/GLM/SandboxWorld/game/tests/conveyor.test.ts
~/Project/GLM/SandboxWorld/game/tests/terrain-oracle.test.ts
~/Project/GLM/SandboxWorld/game/tests/wind-sway.test.ts
~/Project/GLM/SandboxWorld/game/tests/wall-creeper.test.ts
~/Project/GLM/SandboxWorld/game/tests/luck-r5.test.ts
~/Project/GLM/SandboxWorld/game/tests/vui-layout.test.ts
~/Project/GLM/SandboxWorld/game/tests/spawn-friendly-cycle.test.ts
~/Project/GLM/SandboxWorld/game/tests/luck-sources-lifesteal-batch.test.ts
~/Project/GLM/SandboxWorld/game/tests/a-batch3.test.ts
~/Project/GLM/SandboxWorld/game/tests/item-coverage.test.ts
~/Project/GLM/SandboxWorld/game/tests/hostile-proj-player-hit.test.ts
~/Project/GLM/SandboxWorld/game/tests/cactus-oasis.test.ts
~/Project/GLM/SandboxWorld/game/tests/caves-checkpoint.test.ts
~/Project/GLM/SandboxWorld/game/tests/cobweb.test.ts
~/Project/GLM/SandboxWorld/game/tests/nature-particles.test.ts
~/Project/GLM/SandboxWorld/game/tests/explosion.test.ts
~/Project/GLM/SandboxWorld/game/tests/unified-random.test.ts
~/Project/GLM/SandboxWorld/game/tests/furniture-items.test.ts
~/Project/GLM/SandboxWorld/game/tests/summon-r6.test.ts
~/Project/GLM/SandboxWorld/game/tests/tile-light-specials.test.ts
~/Project/GLM/SandboxWorld/game/tests/dungeon-spawn.test.ts
~/Project/GLM/SandboxWorld/game/tests/world-store.test.ts
~/Project/GLM/SandboxWorld/game/tests/npc-grid-draw.test.ts
~/Project/GLM/SandboxWorld/game/tests/boss-pylons.test.ts
~/Project/GLM/SandboxWorld/game/tests/monolith.test.ts
~/Project/GLM/SandboxWorld/game/tests/pixel-art.test.ts
~/Project/GLM/SandboxWorld/game/tests/pot-break.test.ts
~/Project/GLM/SandboxWorld/game/tests/weapons-entities.test.ts
~/Project/GLM/SandboxWorld/game/tests/dungeon-walls.test.ts
~/Project/GLM/SandboxWorld/game/tests/tile-anim.test.ts
~/Project/GLM/SandboxWorld/game/tests/plant-ai-rotation.test.ts
~/Project/GLM/SandboxWorld/game/tests/bossAI-dd2.test.ts
~/Project/GLM/SandboxWorld/game/tests/weather.test.ts
~/Project/GLM/SandboxWorld/game/tests/graveyard-biome.test.ts
~/Project/GLM/SandboxWorld/game/tests/resource-bars.test.ts
~/Project/GLM/SandboxWorld/game/tests/wld-real.test.ts
~/Project/GLM/SandboxWorld/game/tests/lunar-final-audit.test.ts
~/Project/GLM/SandboxWorld/game/tests/p5-equip-prefix-loadout.test.ts
~/Project/GLM/SandboxWorld/game/tests/liquid-shimmer-render.test.ts
~/Project/GLM/SandboxWorld/game/tests/a-batch2.test.ts
~/Project/GLM/SandboxWorld/game/tests/jungle-spawn.test.ts
~/Project/GLM/SandboxWorld/game/tests/old-ones-army.test.ts
~/Project/GLM/SandboxWorld/game/tests/bank-storage.test.ts
~/Project/GLM/SandboxWorld/game/tests/hive.test.ts
~/Project/GLM/SandboxWorld/game/tests/micro-biomes.test.ts
~/Project/GLM/SandboxWorld/game/tests/enemy-shooters.test.ts
~/Project/GLM/SandboxWorld/game/tests/wld.test.ts
~/Project/GLM/SandboxWorld/game/tests/boss-summon.test.ts
~/Project/GLM/SandboxWorld/game/tests/npc-drops.test.ts
~/Project/GLM/SandboxWorld/game/tests/spiky-ball.test.ts
~/Project/GLM/SandboxWorld/game/tests/env-hazards.test.ts
~/Project/GLM/SandboxWorld/game/tests/item-bridge.test.ts
~/Project/GLM/SandboxWorld/game/tests/bossAI-lunar-misc.test.ts
~/Project/GLM/SandboxWorld/game/tests/equip-stats.test.ts
~/Project/GLM/SandboxWorld/game/tests/l10n-data.test.ts
~/Project/GLM/SandboxWorld/game/tests/buffs.test.ts
~/Project/GLM/SandboxWorld/game/tests/world-border.test.ts
~/Project/GLM/SandboxWorld/game/tests/sky-invariant.test.ts
~/Project/GLM/SandboxWorld/game/tests/golden-wld-meta.test.ts
~/Project/GLM/SandboxWorld/game/tests/fireworks.test.ts
~/Project/GLM/SandboxWorld/game/tests/l10n-merge.test.ts
~/Project/GLM/SandboxWorld/game/tests/hell-background.test.ts
~/Project/GLM/SandboxWorld/game/tests/equip-r4.test.ts
~/Project/GLM/SandboxWorld/game/tests/critter-ai.test.ts
~/Project/GLM/SandboxWorld/game/tests/arrow-tree-pass.test.ts
~/Project/GLM/SandboxWorld/game/tests/cactus-frame.test.ts
~/Project/GLM/SandboxWorld/game/tests/gen-loot-passes.test.ts
~/Project/GLM/SandboxWorld/game/tests/tile-names.test.ts

```


---

## 🤖 Assistant · 2026-08-12T15:52:03.535Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game; echo \"---\"; ls ~/Project/GLM/SandboxWorld/game/src 2>/dev/null",
 "description": "List project root and src directories"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:03.576Z

**📎 ToolResult**

```
dbg-music.mjs
dist
docs
index.html
node_modules
package-lock.json
package.json
probe-bee-despawn.mjs
probe-boss-dead.mjs
probe-day-despawn.mjs
probe-eoc-dead.mjs
probe-eoc-trace.mjs
probe-events.mjs
probe-gems.mjs
probe-heart.mjs
probe-invasion.mjs
probe-music.mjs
probe-npc-chat.mjs
probe-npc-full.mjs
probe-npcdrops.mjs
probe-oldman.mjs
probe-pot-heart.mjs
probe-rain-spawn.mjs
probe-sky-preview.mjs
probe-statue.mjs
probe-tax.mjs
probe-time-ui.mjs
probe-town-arrival.mjs
probe-wind-spawn.mjs
public
scripts
shots
src
Starter_World Master.wld
tests
tools
tsconfig.json
vite.config.ts
whip-probe.mjs
whip10-batchB.mjs
whip11-batchC.mjs
whip12-batchD.mjs
whip13-dd2-wolf.mjs
whip14-fox.mjs
whip15-nebula.mjs
whip2.mjs
whip3-sfx.mjs
whip4-shoot.mjs
whip5-summon-full.mjs
whip6-mult-check.mjs
whip7-class-probe.mjs
whip8-time-probe.mjs
whip9-batchA.mjs
---
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

```


---

## 🤖 Assistant · 2026-08-12T15:52:05.138Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I'm in plan mode but I'm a read-only search agent anyway. Let me explore. First, look at data/items.ts to understand local item definitions.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:05.622Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/game/src/data/ ~/Project/GLM/SandboxWorld/game/src/items/ ~/Project/GLM/SandboxWorld/game/src/save/ ~/Project/GLM/SandboxWorld/game/src/net/ 2>/dev/null",
 "description": "List data, items, save, net directories"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:05.682Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/data/:
total 3048
drwxr-xr-x@ 47 user  staff    1504  8月 12 23:20 .
drwxr-xr-x@ 26 user  staff     832  8月 12 23:37 ..
-rw-r--r--@  1 user  staff   12397  8月 12 12:52 Bestiary.ts
-rw-r--r--@  1 user  staff    3194  8月 12 12:48 bestiaryStatics.generated.ts
-rw-r--r--@  1 user  staff    4707  8月 10 16:35 critters.ts
-rw-r--r--@  1 user  staff    6105  8月  9 17:58 enemies.ts
-rw-r--r--@  1 user  staff   85145  8月 12 18:50 items.ts
-rw-r--r--@  1 user  staff   12435  8月 11 22:28 Music.ts
-rw-r--r--@  1 user  staff     587  8月 11 14:07 npcLavaImmune.ts
-rw-r--r--@  1 user  staff    1096  8月 11 10:53 npcPortraits.ts
-rw-r--r--@  1 user  staff    8504  8月 12 23:20 recipes.ts
-rw-r--r--@  1 user  staff  188141  8月 12 14:10 tiles.ts
-rw-r--r--@  1 user  staff   14609  8月 12 17:12 vanilla-accfx.json
-rw-r--r--@  1 user  staff    1420  8月 11 20:29 vanilla-equip.json
-rw-r--r--@  1 user  staff  219566  8月 12 17:24 vanilla-itemcombat.json
-rw-r--r--@  1 user  staff  160120  8月 12 00:56 vanilla-itemfunc.json
-rw-r--r--@  1 user  staff   14397  8月 11 12:35 vanilla-itemrare.json
-rw-r--r--@  1 user  staff   22762  8月 11 20:29 vanilla-itemstats.json
-rw-r--r--@  1 user  staff   27738  8月 11 12:35 vanilla-itemvalue.json
-rw-r--r--@  1 user  staff   24850  8月 11 23:27 vanilla-mapcolors.json
-rw-r--r--@  1 user  staff   82736  8月 11 20:43 vanilla-npcdrops.json
-rw-r--r--@  1 user  staff    2288  8月 10 10:03 vanilla-npcnetid.json
-rw-r--r--@  1 user  staff    3925  8月 11 17:44 vanilla-npcvalue.json
-rw-r--r--@  1 user  staff   14665  8月 11 20:29 vanilla-prefix.json
-rw-r--r--@  1 user  staff  104229  8月 12 17:20 vanilla-projectiles.json
-rw-r--r--@  1 user  staff    2304  8月 12 00:59 vanilla-projframes.json
-rw-r--r--@  1 user  staff  313256  8月 11 11:35 vanilla-recipes.json
-rw-r--r--@  1 user  staff    5117  8月 12 14:27 vanilla-shimmer.json
-rw-r--r--@  1 user  staff   40922  8月 12 23:34 vanilla-shopstock.json
-rw-r--r--@  1 user  staff    3345  8月 10 22:20 vanilla-travelshop.json
-rw-r--r--@  1 user  staff    9584  8月 11 00:49 vanilla-wallitems.json
-rw-r--r--@  1 user  staff    1098  8月 12 09:49 vanilla-whips.json
-rw-r--r--@  1 user  staff     682  8月 11 20:29 vanilla-wingstats.json
-rw-r--r--@  1 user  staff    6642  8月 12 23:18 vanillaAccFx.ts
-rw-r--r--@  1 user  staff    3672  8月 12 14:18 vanillaArmorSets.ts
-rw-r--r--@  1 user  staff    1891  8月 11 11:56 vanillaEquip.ts
-rw-r--r--@  1 user  staff    5677  8月 12 18:16 vanillaFishing.ts
-rw-r--r--@  1 user  staff   11321  8月 12 18:14 vanillaItemCombat.ts
-rw-r--r--@  1 user  staff    1374  8月 11 22:09 vanillaItemFunc.ts
-rw-r--r--@  1 user  staff    2325  8月 11 20:31 vanillaItemStats.ts
-rw-r--r--@  1 user  staff    2061  8月 11 23:27 vanillaMapColors.ts
-rw-r--r--@  1 user  staff   11388  8月 12 15:47 vanillaNpcs.ts
-rw-r--r--@  1 user  staff    4821  8月 11 11:56 vanillaPrefixes.ts
-rw-r--r--@  1 user  staff    1925  8月 12 17:27 vanillaProjectiles.ts
-rw-r--r--@  1 user  staff    9135  8月 11 10:33 vanillaRecipes.ts
-rw-r--r--@  1 user  staff    4303  8月 12 11:39 vanillaSummonStats.ts
-rw-r--r--@  1 user  staff    2599  8月 12 12:09 vanillaWingStats.ts

~/Project/GLM/SandboxWorld/game/src/items/:
total 32
drwxr-xr-x@  3 user  staff     96  8月 11 23:33 .
drwxr-xr-x@ 26 user  staff    832  8月 12 23:37 ..
-rw-r--r--@  1 user  staff  15787  8月 11 23:33 Inventory.ts

~/Project/GLM/SandboxWorld/game/src/net/:
total 136
drwxr-xr-x@  6 user  staff    192  8月 12 16:47 .
drwxr-xr-x@ 26 user  staff    832  8月 12 23:37 ..
-rw-r--r--@  1 user  staff  35521  8月 12 17:20 ClientNet.ts
-rw-r--r--@  1 user  staff    930  8月 12 17:21 entitySyncHooks.ts
-rw-r--r--@  1 user  staff   4501  8月 11 09:48 LanDiscovery.ts
-rw-r--r--@  1 user  staff  19181  8月 12 17:20 protocol.ts

~/Project/GLM/SandboxWorld/game/src/save/:
total 88
drwxr-xr-x@  7 user  staff    224  8月 12 16:22 .
drwxr-xr-x@ 26 user  staff    832  8月 12 23:37 ..
-rw-r--r--@  1 user  staff   2483  8月  9 18:15 CharacterStore.ts
-rw-r--r--@  1 user  staff   3332  8月 10 15:35 KvStore.ts
-rw-r--r--@  1 user  staff  14065  8月 12 17:53 SaveFile.ts
-rw-r--r--@  1 user  staff  13835  8月 12 17:53 serialize.ts
-rw-r--r--@  1 user  staff   4081  8月  9 20:04 WorldStore.ts

```


---

## 🤖 Assistant · 2026-08-12T15:52:05.901Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/data/*.ts 2>/dev/null",
 "description": "Count lines in data directory files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:05.945Z

**📎 ToolResult**

```
     286 ~/Project/GLM/SandboxWorld/game/src/data/Bestiary.ts
       8 ~/Project/GLM/SandboxWorld/game/src/data/bestiaryStatics.generated.ts
      54 ~/Project/GLM/SandboxWorld/game/src/data/critters.ts
     123 ~/Project/GLM/SandboxWorld/game/src/data/enemies.ts
    1090 ~/Project/GLM/SandboxWorld/game/src/data/items.ts
     233 ~/Project/GLM/SandboxWorld/game/src/data/Music.ts
       9 ~/Project/GLM/SandboxWorld/game/src/data/npcLavaImmune.ts
      18 ~/Project/GLM/SandboxWorld/game/src/data/npcPortraits.ts
     113 ~/Project/GLM/SandboxWorld/game/src/data/recipes.ts
    1282 ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts
     122 ~/Project/GLM/SandboxWorld/game/src/data/vanillaAccFx.ts
      70 ~/Project/GLM/SandboxWorld/game/src/data/vanillaArmorSets.ts
      48 ~/Project/GLM/SandboxWorld/game/src/data/vanillaEquip.ts
     105 ~/Project/GLM/SandboxWorld/game/src/data/vanillaFishing.ts
     212 ~/Project/GLM/SandboxWorld/game/src/data/vanillaItemCombat.ts
      31 ~/Project/GLM/SandboxWorld/game/src/data/vanillaItemFunc.ts
      60 ~/Project/GLM/SandboxWorld/game/src/data/vanillaItemStats.ts
      46 ~/Project/GLM/SandboxWorld/game/src/data/vanillaMapColors.ts
     218 ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts
      96 ~/Project/GLM/SandboxWorld/game/src/data/vanillaPrefixes.ts
      42 ~/Project/GLM/SandboxWorld/game/src/data/vanillaProjectiles.ts
     239 ~/Project/GLM/SandboxWorld/game/src/data/vanillaRecipes.ts
      72 ~/Project/GLM/SandboxWorld/game/src/data/vanillaSummonStats.ts
      53 ~/Project/GLM/SandboxWorld/game/src/data/vanillaWingStats.ts
    4630 total

```


---

## 🤖 Assistant · 2026-08-12T15:52:07.698Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read items.ts to see the local item definitions structure.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:07.712Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/items.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:08.111Z

**📎 ToolResult**

```
1	// 物品注册表
2	export type ToolType = 'pick' | 'axe' | 'sword' | 'hammer';
3	// Buff 类型（药水饮用后生效）
4	export type PotionBuff = 'agility' | 'ironskin' | 'resistance' | 'thorns' | 'regen'
5	  | 'obsidianSkin' | 'gills' | 'manaRegen' | 'magicPower' | 'featherfall' | 'waterWalking' | 'archery' | 'nightOwl';
6	// 盔甲部位：0 头盔 1 胸甲 2 胫甲（与 Inventory.armorSlotReq 的格位对应）
7	export type ArmorSlot = 0 | 1 | 2;
8	
9	export interface ItemDef {
10	  key: string;
11	  name: string;
12	  maxStack: number;
13	  tile?: string;          // 放置的 tile key
14	  placeStyle?: number;     // 放置的样式索引(vanilla style 帧 X 偏移 = style*fw*18)
15	  magic?: {               // 魔法武器:消耗 mana 发射投射物
16	    damage: number;
17	    speed: number;        // 使用冷却 tick
18	    manaCost: number;
19	    projSpeed: number;
20	    proj?: 'spark' | 'bolt'; // 投射物外观
21	  };
22	  ranged?: {              // 远程武器:消耗 ammo 弹药发射投射物
23	    damage: number;
24	    speed: number;        // 使用冷却 tick
25	    knockback: number;
26	    ammo: string;         // 弹药 item key(箭)
27	    projSpeed: number;    // 投射物速度 px/tick
28	    /** 原版 item id（PickAmmo/ItemCheck_Shoot 数值以 vanilla-itemcombat.json 为准） */
29	    vid?: number;
30	  };
31	  /** 原版 AmmoID（40=箭；弹药物品自身标识，PickAmmo 匹配弓 useAmmo） */
32	  ammoId?: number;
33	  /** 原版 item id（战斗数值数据源） */
34	  vid?: number;
35	  wall?: string;          // 放置的 wall key
36	  /** 原版 createWall（Item.cs SetDefaults）：放置的背景墙 vanilla id。
37	   *  vanilla-wallitems.json 全量 124 项（tools/extract-wallitems.mjs 提取） */
38	  wallId?: number;
39	  tool?: {
40	    type: ToolType;
41	    power?: number;       // 工具力（镐/斧/锤）
42	    damage?: number;      // 武器伤害
43	    speed?: number;       // 挥砍动画 tick（≈原版 useAnimation）
44	    /** 原版 useTime（Item.cs SetDefaults）：挖掘每击冷却——原版挖掘节奏的真基准，
45	     *  铜 15-23 / 铁 13-20 / 银 11-19 / 金 17-23（applyItemTime 冷却=useTime） */
46	    useTime?: number;
47	    knockback?: number;
48	    reach?: number;       // 攻击/作用半径（px）
49	  };
50	  /** 副工具力（Hamaxe 系双工具：主 tool.type 外的另一力，挖掘入口按主类型判定） */
51	  axePower?: number;
52	  heal?: number;          // 食用/饮用回复
53	  potion?: {
54	    buff: PotionBuff;
55	    duration: number;     // 秒
56	    isHealType: boolean;  // 受"耐药性"封锁
57	  };
58	  accessory?: 'lucky_horseshoe' | 'feral_claws'; // 配饰效果
59	  armor?: { slot: ArmorSlot; defense: number };   // 盔甲（可穿装备/时装格，仅装备格计防御）
60	  value?: number;         // 钱币价值（铜币）
61	  wireTool?: {            // 电路工具（原版 Player.cs:30289-30444 ItemCheck_UseWiringTools）
62	    place?: number;       // 单击放置的导线位掩码(TOOL_RED/BLUE/GREEN/YELLOW/ACTUATOR)
63	    cutter?: boolean;     // 剪线钳:按优先级移除一件(致动器>黄>绿>蓝>红)
64	    rod?: boolean;        // 致动魔杖:手动翻转致动状态
65	    grand?: boolean;      // 宏伟蓝图:拖拽批量(R 键切模式)
66	  };
67	  desc?: string;
68	}
69	
70	export const ITEM_DEFS: ItemDef[] = [];
71	const byKey: Record<string, number> = {};
72	export const ITEM_BY_KEY: Record<string, number> = byKey;
73	
74	function item(d: Partial<ItemDef> & { key: string; name: string }) {
75	  byKey[d.key] = ITEM_DEFS.length;
76	  ITEM_DEFS.push({ maxStack: 999, ...d } as ItemDef);
77	}
78	
79	// ---- 基础方块 ----
80	item({ key: 'dirt_block', name: '泥土块', tile: 'dirt' });
81	item({ key: 'stone_block', name: '石块', tile: 'stone' });
82	item({ key: 'wood', name: '木材', tile: 'wood' });
83	item({ key: 'sand_block', name: '沙块', tile: 'sand' });
84	item({ key: 'snow_block', name: '雪块', tile: 'snow' });
85	item({ key: 'platform', name: '木平台', tile: 'platform', maxStack: 999 });
86	item({ key: 'torch', name: '火把', tile: 'torch' });
87	item({ key: 'door', name: '木门', tile: 'door_closed', maxStack: 99 });
88	item({ key: 'workbench', name: '工作台', tile: 'workbench', maxStack: 99 });
89	item({ key: 'furnace', name: '熔炉', tile: 'furnace', maxStack: 99 });
90	item({ key: 'anvil', name: '铁砧', tile: 'anvil', maxStack: 99 });
91	item({ key: 'chest', name: '宝箱', tile: 'chest', maxStack: 99 });
92	
93	// ---- 材料 ----
94	item({ key: 'gel', name: '凝胶', desc: '史莱姆的残留物' });
95	item({ key: 'acorn', name: '橡实', desc: '种在草块上会长成树', maxStack: 99, tile: 'acorn_sapling' });
96	item({ key: 'mushroom_item', name: '蘑菇', heal: 15, value: 1,
97	  // 原版 item 5（Item.cs:1424）：useStyle 2 咀嚼、healLife 15、potion=true（触发药水病）
98	  potion: { buff: 'resistance', duration: 60, isHealType: true } });
99	item({ key: 'copper_ore', name: '铜矿', desc: '可在熔炉炼成铜锭' });
100	item({ key: 'iron_ore', name: '铁矿' });
101	item({ key: 'silver_ore', name: '银矿' });
102	item({ key: 'gold_ore', name: '金矿' });
103	item({ key: 'copper_bar', name: '铜锭' });
104	item({ key: 'iron_bar', name: '铁锭' });
105	item({ key: 'silver_bar', name: '银锭' });
106	item({ key: 'gold_bar', name: '金锭' });
107	item({ key: 'lens', name: '晶状体', desc: '恶魔眼的眼睛' });
108	item({ key: 'suspicious_eye', name: '可疑的眼球', desc: '夜间使用会召唤不祥之物…', maxStack: 20 });
109	item({ key: 'lesser_healing_potion', name: '弱效治疗药水', heal: 50, maxStack: 30,
110	  // 原版 188 治疗药水族（DefaultToHealingPotion）：useStyle 9 举杯、potion=true
111	  potion: { buff: 'resistance', duration: 60, isHealType: true } });
112	item({ key: 'coin_copper', name: '铜币', maxStack: 999, value: 1 });
113	item({ key: 'coin_silver', name: '银币', maxStack: 999, value: 100 });
114	item({ key: 'coin_gold', name: '金币', maxStack: 999, value: 10000 });
115	item({ key: 'coin_platinum', name: '铂金币', maxStack: 999, value: 1000000, vid: 73 }); // 金币雨（WorldGen.cs:71848）
116	
117	// ---- 药水（Buff 来源;buffType/buffTime 对齐 1456 Item.cs case 288-305）----
118	// 时长换算:buffTime/60 = 秒(Regeneration/Swiftness/Ironskin/Thorns 均 28800t=480s=8min)
119	item({ key: 'heal_potion', name: '治疗药水', maxStack: 30, heal: 100, desc: '回复 100 生命',
120	  potion: { buff: 'resistance', duration: 60, isHealType: true } });
121	item({ key: 'agility_potion', name: '敏捷药水', maxStack: 30, desc: '移速 +25%，持续 8 分钟',
122	  potion: { buff: 'agility', duration: 480, isHealType: false } });
123	item({ key: 'ironskin_potion', name: '铁皮药水', maxStack: 30, desc: '防御 +8，持续 8 分钟',
124	  potion: { buff: 'ironskin', duration: 480, isHealType: false } });
125	item({ key: 'thorns_potion', name: '荆棘药水', maxStack: 30, desc: '受击反弹全额接触伤害，持续 8 分钟',
126	  potion: { buff: 'thorns', duration: 480, isHealType: false } });
127	item({ key: 'regen_potion', name: '恢复药水', maxStack: 30, desc: '每秒回复 2 生命，持续 8 分钟',
128	  // 原版 Regeneration Potion 是 buff 药水(heal=0),不触发 PotionSickness → isHealType:false
129	  potion: { buff: 'regen', duration: 480, isHealType: false } });
130	// ---- 药水 buff 族第二批（Item.cs case 288/291/293/294/295/302/303 buffTime/60 = 秒）----
131	item({ key: 'obsidian_skin_potion', name: '黑曜石皮药水', maxStack: 30, desc: '免疫岩浆与灼烧，持续 6 分钟',
132	  potion: { buff: 'obsidianSkin', duration: 360, isHealType: false } });   // 21600t
133	item({ key: 'gills_potion', name: '鱼鳃药水', maxStack: 30, desc: '可在水下呼吸，持续 4 分钟',
134	  potion: { buff: 'gills', duration: 240, isHealType: false } });          // 14400t
135	item({ key: 'mana_regen_potion', name: '魔力再生药水', maxStack: 30, desc: '大幅提升魔力恢复，持续 8 分钟',
136	  potion: { buff: 'manaRegen', duration: 480, isHealType: false } });      // 28800t
137	item({ key: 'magic_power_potion', name: '魔法力量药水', maxStack: 30, desc: '魔法伤害 +20%，持续 4 分钟',
138	  potion: { buff: 'magicPower', duration: 240, isHealType: false } });     // 14400t
139	item({ key: 'featherfall_potion', name: '羽落药水', maxStack: 30, desc: '减缓下落速度，持续 10 分钟',
140	  potion: { buff: 'featherfall', duration: 600, isHealType: false } });    // 36000t
141	item({ key: 'water_walking_potion', name: '水上行走药水', maxStack: 30, desc: '可在水面行走，持续 10 分钟',
142	  potion: { buff: 'waterWalking', duration: 600, isHealType: false } });   // 36000t
143	item({ key: 'archery_potion', name: '射手药水', maxStack: 30, desc: '箭伤害 ×1.1，持续 8 分钟',
144	  potion: { buff: 'archery', duration: 480, isHealType: false } });        // 28800t
145	item({ key: 'night_owl_potion', name: '夜枭药水', maxStack: 30, desc: '改善黑暗与水下视觉，持续 10 分钟',
146	  potion: { buff: 'nightOwl', duration: 600, isHealType: false } });       // 36000t(Item 299→buff 12)
147	
148	// ---- 配饰（移植自 Maples Accessory）----
149	item({ key: 'lucky_horseshoe', name: '幸运马掌', maxStack: 1, accessory: 'lucky_horseshoe',
150	  desc: '免疫摔落伤害' });
151	item({ key: 'feral_claws', name: '猛爪手套', maxStack: 1, accessory: 'feral_claws',
152	  desc: '近战攻速 ×2，伤害 +5' });
153	
154	// ---- 盔甲（铜/铁/银/金三件套，防御取原版）----
155	const armorTiers: Array<[string, string, [number, number, number]]> = [
156	  // key 前缀, 显示前缀, [头盔, 胸甲, 胫甲] 防御
157	  ['copper', '铜', [1, 2, 1]],
158	  ['iron', '铁', [2, 3, 2]],
159	  ['silver', '银', [3, 4, 3]],
160	  ['gold', '金', [4, 5, 4]],
161	];
162	const armorParts: Array<[string, string, ArmorSlot]> = [
163	  ['helmet', '头盔', 0], ['chainmail', '胸甲', 1], ['greaves', '胫甲', 2],
164	];
165	for (const [prefix, cn, defs] of armorTiers) {
166	  armorParts.forEach(([suffix, cnPart, slot], k) => {
167	    item({
168	      key: `${prefix}_${suffix}`, name: `${cn}${cnPart}`, maxStack: 1,
169	      armor: { slot, defense: defs[k] },
170	      desc: `防御 +${defs[k]}`,
171	    });
172	  });
173	}
174	
175	// ---- 工具/武器（数值 = 官方原版 1.4.0.5 Item.cs SetDefaults，铜币价值）----
176	// 木镐/木斧为自定义低档（原版无对应）；木剑(24)=官方 7 伤、木锤(196)=官方 25 锤力
177	item({ key: 'wood_pickaxe', name: '木镐', maxStack: 1, value: 50,
178	  tool: { type: 'pick', power: 12, damage: 2, speed: 23, useTime: 17, knockback: 2, reach: 2.6 * 16 } });
179	item({ key: 'wood_axe', name: '木斧', maxStack: 1, value: 50,
180	  tool: { type: 'axe', power: 4, damage: 2, speed: 30, useTime: 22, knockback: 4.5, reach: 2.4 * 16 } });
181	item({ key: 'wood_sword', name: '木剑', maxStack: 1, value: 100,
182	  tool: { type: 'sword', damage: 7, speed: 25, useTime: 25, knockback: 4, reach: 2.2 * 16 } });
183	item({ key: 'wood_hammer', name: '木锤', maxStack: 1, value: 50,
184	  tool: { type: 'hammer', power: 25, damage: 2, speed: 37, useTime: 25, knockback: 5.5, reach: 2.4 * 16 },
185	  desc: '敲除背景墙' });
186	// 铜（3509/3506/3508/3505）
187	item({ key: 'copper_pickaxe', name: '铜镐', maxStack: 1, value: 500,
188	  tool: { type: 'pick', power: 35, damage: 4, speed: 23, useTime: 15, knockback: 2, reach: 2.6 * 16 } });
189	item({ key: 'copper_axe', name: '铜斧', maxStack: 1, value: 400,
190	  tool: { type: 'axe', power: 7, damage: 3, speed: 30, useTime: 21, knockback: 4.5, reach: 2.4 * 16 } });
191	item({ key: 'copper_sword', name: '铜剑', maxStack: 1, value: 450,
192	  tool: { type: 'sword', damage: 8, speed: 23, useTime: 23, knockback: 5, reach: 2.2 * 16 } });
193	item({ key: 'copper_hammer', name: '铜锤', maxStack: 1, value: 400,
194	  tool: { type: 'hammer', power: 35, damage: 4, speed: 33, useTime: 23, knockback: 5.5, reach: 2.4 * 16 },
195	  desc: '敲除背景墙' });
196	// 铁（1/10/4/7）
197	item({ key: 'iron_pickaxe', name: '铁镐', maxStack: 1, value: 2000,
198	  tool: { type: 'pick', power: 40, damage: 5, speed: 20, useTime: 13, knockback: 2, reach: 2.6 * 16 } });
199	item({ key: 'iron_axe', name: '铁斧', maxStack: 1, value: 1600,
200	  tool: { type: 'axe', power: 9, damage: 5, speed: 27, useTime: 19, knockback: 4.5, reach: 2.4 * 16 } });
201	item({ key: 'iron_sword', name: '铁剑', maxStack: 1, value: 1800,
202	  tool: { type: 'sword', damage: 10, speed: 21, useTime: 20, knockback: 5, reach: 2.2 * 16 } });
203	item({ key: 'iron_hammer', name: '铁锤', maxStack: 1, value: 1600,
204	  tool: { type: 'hammer', power: 40, damage: 7, speed: 30, useTime: 20, knockback: 5.5, reach: 2.4 * 16 },
205	  desc: '敲除背景墙' });
206	// 银（3515/3512/3514/3511）
207	item({ key: 'silver_pickaxe', name: '银镐', maxStack: 1, value: 5000,
208	  tool: { type: 'pick', power: 45, damage: 6, speed: 19, useTime: 11, knockback: 2, reach: 2.6 * 16 } });
209	item({ key: 'silver_axe', name: '银斧', maxStack: 1, value: 4000,
210	  tool: { type: 'axe', power: 10, damage: 6, speed: 26, useTime: 18, knockback: 4.5, reach: 2.4 * 16 } });
211	item({ key: 'silver_sword', name: '银剑', maxStack: 1, value: 4500,
212	  tool: { type: 'sword', damage: 11, speed: 21, useTime: 20, knockback: 5, reach: 2.2 * 16 } });
213	item({ key: 'silver_hammer', name: '银锤', maxStack: 1, value: 4000,
214	  tool: { type: 'hammer', power: 45, damage: 9, speed: 29, useTime: 19, knockback: 5.5, reach: 2.4 * 16 },
215	  desc: '敲除背景墙' });
216	// 金（3521/3518/3520/3517）
217	item({ key: 'gold_pickaxe', name: '金镐', maxStack: 1, value: 10000,
218	  tool: { type: 'pick', power: 55, damage: 6, speed: 20, useTime: 17, knockback: 2, reach: 2.6 * 16 } });
219	item({ key: 'gold_axe', name: '金斧', maxStack: 1, value: 8000,
220	  tool: { type: 'axe', power: 11, damage: 7, speed: 26, useTime: 18, knockback: 4.5, reach: 2.4 * 16 } });
221	item({ key: 'gold_sword', name: '金剑', maxStack: 1, value: 9000,
222	  tool: { type: 'sword', damage: 13, speed: 20, useTime: 20, knockback: 5, reach: 2.2 * 16 } });
223	item({ key: 'gold_hammer', name: '金锤', maxStack: 1, value: 8000,
224	  tool: { type: 'hammer', power: 55, damage: 9, speed: 28, useTime: 23, knockback: 5.5, reach: 2.4 * 16 },
225	  desc: '敲除背景墙' });
226	
227	// ===================== 原版素材批次：新材料 / 方块 / 家具 =====================
228	// ---- 替代矿与困难模式矿（先做美术/掉落） ----
229	item({ key: 'tin_ore', name: '锡矿' });
230	item({ key: 'lead_ore', name: '铅矿' });
231	item({ key: 'tungsten_ore', name: '钨矿' });
232	item({ key: 'platinum_ore', name: '铂金矿' });
233	item({ key: 'tin_bar', name: '锡锭' });
234	item({ key: 'lead_bar', name: '铅锭' });
235	item({ key: 'tungsten_bar', name: '钨锭' });
236	item({ key: 'platinum_bar', name: '铂金锭' });
237	item({ key: 'demonite_ore', name: '魔矿' });
238	item({ key: 'meteorite', name: '陨石' });
239	item({ key: 'hellstone', name: '狱石' });
240	item({ key: 'crimtane_ore', name: '猩红矿' });
241	item({ key: 'cobalt_ore', name: '钴矿' });
242	item({ key: 'mythril_ore', name: '秘银矿' });
243	item({ key: 'adamantite_ore', name: '精金矿' });
244	item({ key: 'palladium_ore', name: '钯金矿' });
245	item({ key: 'orichalcum_ore', name: '山铜矿' });
246	item({ key: 'titanium_ore', name: '钛矿' });
247	item({ key: 'chlorophyte_ore', name: '叶绿矿' });
248	
249	// ---- 宝石 ----
250	item({ key: 'sapphire', name: '蓝宝石', value: 15 });
251	item({ key: 'ruby', name: '红宝石', value: 22 });
252	item({ key: 'emerald', name: '翡翠', value: 15 });
253	item({ key: 'topaz', name: '黄玉', value: 11 });
254	item({ key: 'amethyst', name: '紫水晶', value: 11 });
255	item({ key: 'diamond', name: '钻石', value: 30 });
256	
257	// ---- 冰雪 / 沙漠 / 基础方块 ----
258	item({ key: 'ice_block', name: '冰块', tile: 'ice' });
259	item({ key: 'ice_brick', name: '冰砖', tile: 'ice_brick' });
260	item({ key: 'snow_brick', name: '雪砖', tile: 'snow_brick' });
261	item({ key: 'sandstone_block', name: '沙岩', tile: 'sandstone' });
262	item({ key: 'hardened_sand_block', name: '硬化沙块', tile: 'hardened_sand' });
263	item({ key: 'desert_fossil', name: '沙漠化石' });
264	item({ key: 'clay_block', name: '粘土块', tile: 'clay' });
265	item({ key: 'glass', name: '玻璃', tile: 'glass' });
266	item({ key: 'obsidian', name: '黑曜石', tile: 'obsidian' });
267	item({ key: 'gray_brick', name: '灰砖', tile: 'gray_brick' });
268	item({ key: 'red_brick', name: '红砖', tile: 'red_brick' });
269	item({ key: 'mud_block', name: '泥块', tile: 'mud' });
270	item({ key: 'silt_block', name: '淤泥块', tile: 'silt' });
271	
272	// ---- 家具 ----
273	item({ key: 'table', name: '木桌', tile: 'table', maxStack: 99 });
274	item({ key: 'chair', name: '木椅', tile: 'chair', maxStack: 99 });
275	item({ key: 'bed', name: '床', tile: 'bed', maxStack: 99 });
276	item({ key: 'bookcase', name: '书架', tile: 'bookcase', maxStack: 99 });
277	item({ key: 'grandfather_clock', name: '落地钟', tile: 'grandfather_clock', maxStack: 99 });
278	item({ key: 'piano', name: '钢琴', tile: 'piano', maxStack: 99 });
279	item({ key: 'dresser', name: '梳妆台', tile: 'dresser', maxStack: 99 });
280	item({ key: 'bench', name: '长凳', tile: 'bench', maxStack: 99 });
281	item({ key: 'bathtub', name: '浴缸', tile: 'bathtub', maxStack: 99 });
282	item({ key: 'keg', name: '酒桶', tile: 'keg', maxStack: 99 });
283	item({ key: 'cooking_pot', name: '汤锅', tile: 'cooking_pot', maxStack: 99 });
284	item({ key: 'clay_pot', name: '陶盆', tile: 'clay_pot', maxStack: 99 });
285	item({ key: 'tombstone', name: '墓碑', tile: 'tombstone_v', maxStack: 99 });
286	item({ key: 'life_crystal', name: '水晶之心', maxStack: 99, desc: '古老的生命结晶' });
287	// 上限扩容三件套（Player.cs:44655-44700 ItemCheck_Use*；vi_ 前缀自动映射原版图标）
288	item({ key: 'vi_109_mana_crystal', name: '魔力水晶', maxStack: 99, desc: '使用：魔力上限 +20（上限 200）' });
289	item({ key: 'vi_1291_life_fruit', name: '生命果', maxStack: 99, desc: '生命上限 ≥400 时使用：+5（上限 500）' });
290	item({ key: 'candle', name: '蜡烛', tile: 'candle', maxStack: 99 });
291	item({ key: 'chandelier', name: '吊灯', tile: 'chandelier', maxStack: 99 });
292	item({ key: 'lantern', name: '吊挂灯笼', tile: 'lantern', maxStack: 99 });
293	item({ key: 'candelabra', name: '烛台', tile: 'candelabra', maxStack: 99 });
294	item({ key: 'chinese_lantern', name: '中式灯笼', tile: 'chinese_lantern', maxStack: 99 });
295	item({ key: 'skull_lantern', name: '骷髅灯笼', tile: 'skull_lantern', maxStack: 99 });
296	item({ key: 'water_candle', name: '水蜡烛', tile: 'water_candle', maxStack: 99 });
297	// 瓦罐战利品
298	item({ key: 'bomb', name: '小型炸弹', maxStack: 99, desc: '用力扔出去会爆炸…（待实装）', value: 5 });
299	item({ key: 'rope', name: '攀爬绳', maxStack: 999, desc: '左键放置绳列,触碰可攀爬', value: 1, tile: 'v_213_rope' });
300	
301	export interface ItemStack { id: number; stack: number; }
302	export function mkStack(key: string, stack = 1): ItemStack | null {
303	  const id = byKey[key];
304	  if (id === undefined) return null;
305	  return { id, stack };
306	}
307	
308	// ===================== wld 导入补全物品（compat-report 驱动） =====================
309	// 这些物品目前只做图标与存档保留（占位），后续按需实装功能
310	item({ key: 'vi_2350_recall_potion', name: '', maxStack: 999, value: 1 });
311	item({ key: 'vi_188_healing_potion', name: '', maxStack: 999, value: 1 });
312	item({ key: 'vi_282_glowstick', name: '', maxStack: 999, value: 1 });
313	item({ key: 'vi_41_flaming_arrow', name: '', maxStack: 999, value: 1 });
314	item({ key: 'vi_167_dynamite', name: '', maxStack: 999, value: 1 });
315	item({ key: 'vi_279_throwing_knife', name: '', maxStack: 999, value: 1 });
316	item({ key: 'vi_51_jester_s_arrow', name: '', maxStack: 999, value: 1 });
317	item({ key: 'vi_19_gold_bar', name: '', maxStack: 999, value: 1 });
318	item({ key: 'vi_302_water_walking_potion', name: '', maxStack: 999, value: 1 });
319	item({ key: 'vi_305_gravitation_potion', name: '', maxStack: 999, value: 1 });
320	item({ key: 'vi_43_suspicious_looking_eye', name: '', maxStack: 999, value: 1 });
321	item({ key: 'vi_296_spelunker_potion', name: '', maxStack: 999, value: 1 });
322	item({ key: 'vi_299_night_owl_potion', name: '', maxStack: 999, value: 1 });
323	item({ key: 'vi_965_rope', name: '', maxStack: 999, value: 1 });
324	item({ key: 'vi_303_archery_potion', name: '', maxStack: 999, value: 1 });
325	item({ key: 'vi_304_hunter_potion', name: '', maxStack: 999, value: 1 });
326	item({ key: 'vi_50_magic_mirror', name: '', maxStack: 999, value: 1 });
327	item({ key: 'vi_42_shuriken', name: '', maxStack: 999, value: 1 });
328	item({ key: 'vi_295_featherfall_potion', name: '', maxStack: 999, value: 1 });
329	item({ key: 'vi_53_cloud_in_a_bottle', name: '', maxStack: 999, value: 1 });
330	item({ key: 'vi_2329_dangersense_potion', name: '', maxStack: 999, value: 1 });
331	item({ key: 'vi_40_wooden_arrow', name: '', maxStack: 999, value: 1 });
332	item({ key: 'vi_975_shoe_spikes', name: '', maxStack: 999, value: 1 });
333	item({ key: 'vi_54_hermes_boots', name: '', maxStack: 999, value: 1 });
334	item({ key: 'vi_301_thorns_potion', name: '', maxStack: 999, value: 1 });
335	item({ key: 'vi_49_band_of_regeneration', name: '', maxStack: 999, value: 1 });
336	item({ key: 'vi_2326_titan_potion', name: '', maxStack: 999, value: 1 });
337	item({ key: 'vi_297_invisibility_potion', name: '', maxStack: 999, value: 1 });
338	item({ key: 'vi_166_bomb', name: '', maxStack: 999, value: 1 });
339	item({ key: 'vi_5011_mace', name: '', maxStack: 999, value: 1 });
340	item({ key: 'vi_4425_shark_bait', name: '', maxStack: 999, value: 1 });
341	item({ key: 'vi_2351_teleportation_potion', name: '', maxStack: 999, value: 1 });
342	item({ key: 'vi_4460_sandcastle_bucket', name: '', maxStack: 999, value: 1 });
343	item({ key: 'vi_168_grenade', name: '', maxStack: 999, value: 1 });
344	item({ key: 'vi_227_restoration_potion', name: '', maxStack: 999, value: 1 });
345	item({ key: 'vi_930_flare_gun', name: '', maxStack: 999, value: 1 });
346	item({ key: 'vi_931_flare', name: '', maxStack: 999, value: 1 });
347	item({ key: 'vi_997_extractinator', name: '', maxStack: 999, value: 1 });
348	item({ key: 'vi_52_angel_statue', name: '', maxStack: 999, value: 1 });
349	item({ key: 'vi_265_hellfire_arrow', name: '', maxStack: 999, value: 1 });
350	item({ key: 'vi_298_shine_potion', name: '', maxStack: 999, value: 1 });
351	item({ key: 'vi_5007_dead_man_s_sweater', name: '', maxStack: 999, value: 1 });
352	item({ key: 'vi_117_meteorite_bar', name: '', maxStack: 999, value: 1 });
353	item({ key: 'vi_186_breathing_reed', name: '', maxStack: 999, value: 1 });
354	// ---- 呼吸族（CheckDrowning 装备链，2026-08 补齐；stats/装备归属/图标全走 vanilla 数据自动接线）----
355	item({ key: 'vi_250_fish_bowl', name: '', maxStack: 999, value: 1 });            // 鱼缸头盔：戴着恒淹（:22917）
356	item({ key: 'vi_4275_gold_goldfish_bowl', name: '', maxStack: 999, value: 1 });  // 金金鱼缸：同上
357	item({ key: 'vi_268_diving_helmet', name: '', maxStack: 999, value: 1 });        // accDivingHelm：breathCDMax ×6（:12829）
358	item({ key: 'vi_394_diving_gear', name: '', maxStack: 999, value: 1 });          // 潜水装备：divingHelm+flipper（:14652）
359	item({ key: 'vi_1860_jellyfish_diving_gear', name: '', maxStack: 999, value: 1 }); // :14689（浸水发光 :14686）
360	item({ key: 'vi_1861_arctic_diving_gear', name: '', maxStack: 999, value: 1 });  // :14701（+arcticDivingGear 冰水免疫）
361	item({ key: 'vi_497_neptune_s_shell', name: '', maxStack: 999, value: 1 });      // accMerman（:15019）
362	item({ key: 'vi_861_moon_shell', name: '', maxStack: 999, value: 1 });           // accMerman+狼人夜变（:14587）
363	item({ key: 'vi_3110_celestial_shell', name: '', maxStack: 999, value: 1 });     // accMerman+狼人夜变（:14855）
364	item({ key: 'vi_329_shadow_key', name: '', maxStack: 999, value: 1 });
365	item({ key: 'vi_974_ice_torch', name: '', maxStack: 999, value: 1 });
366	item({ key: 'vi_2322_mining_potion', name: '', maxStack: 999, value: 1 });
367	item({ key: 'vi_4915_tungsten_bullet', name: '', maxStack: 999, value: 1 });
368	item({ key: 'vi_946_umbrella', name: '', maxStack: 999, value: 1 });
369	item({ key: 'vi_939_web_slinger', name: '', maxStack: 999, value: 1 });
370	item({ key: 'vi_4870_potion_of_return', name: '', maxStack: 999, value: 1 });
371	item({ key: 'vi_288_obsidian_skin_potion', name: '', maxStack: 999, value: 1 });
372	item({ key: 'vi_31_bottle', name: '', maxStack: 999, value: 1 });
373	item({ key: 'vi_211_feral_claws', name: '', maxStack: 999, value: 1 });
374	item({ key: 'vi_4404_inner_tube', name: '', maxStack: 999, value: 1 });
375	item({ key: 'vi_187_flipper', name: '', maxStack: 999, value: 1 });
376	item({ key: 'vi_2198_ice_machine', name: '', maxStack: 999, value: 1 });
377	item({ key: 'vi_274_dark_lance', name: '', maxStack: 999, value: 1 });
378	item({ key: 'vi_285_aglet', name: '', maxStack: 999, value: 1 });
379	item({ key: 'vi_213_staff_of_regrowth', name: '', maxStack: 999, value: 1 });
380	item({ key: 'vi_964_boomstick', name: '', maxStack: 999, value: 1 });
381	item({ key: 'vi_1293_lihzahrd_power_cell', name: '', maxStack: 999, value: 1 });
382	// 旧日军团三件（ItemID.cs：3817 奖牌 / 3822 埃特尼亚魔力 / 3828 永恒水晶）无需手工
383	// 注册——下方 vanilla.json 自动注册循环已建 vi_<id>_<PascalKey> 条目；
384	// Game 侧按原版 id 寻物（slotVanillaId），见 useLihzahrdAltar/useEterniaStand。
385	item({ key: 'vi_2195_lihzahrd_furnace', name: '', maxStack: 999, value: 1 });
386	item({ key: 'vi_2766_solar_tablet_fragment', name: '', maxStack: 999, value: 1 });
387	item({ key: 'vi_300_battle_potion', name: '', maxStack: 999, value: 1 });
388	item({ key: 'vi_2348_inferno_potion', name: '', maxStack: 999, value: 1 });
389	item({ key: 'vi_218_flamelash', name: '', maxStack: 999, value: 1 });
390	item({ key: 'vi_3019_hellwing_bow', name: '', maxStack: 999, value: 1 });
391	item({ key: 'vi_112_flower_of_fire', name: '', maxStack: 999, value: 1 });
392	item({ key: 'vi_220_sunfury', name: '', maxStack: 999, value: 1 });
393	item({ key: 'vi_4345_can_of_worms', name: '', maxStack: 999, value: 1 });
394	item({ key: 'vi_953_climbing_claws', name: '', maxStack: 999, value: 1 });
395	item({ key: 'vi_3069_wand_of_sparking', name: '', maxStack: 999, value: 1 });
396	item({ key: 'vi_212_anklet_of_the_wind', name: '', maxStack: 999, value: 1 });
397	item({ key: 'vi_2204_honey_dispenser', name: '', maxStack: 999, value: 1 });
398	item({ key: 'vi_277_trident', name: '', maxStack: 999, value: 1 });
399	item({ key: 'vi_863_water_walking_boots', name: '', maxStack: 999, value: 1 });
400	item({ key: 'vi_751_cloud', name: '', maxStack: 999, value: 1 });
401	item({ key: 'vi_155_muramasa', name: '', maxStack: 999, value: 1 });
402	item({ key: 'vi_289_regeneration_potion', name: '', maxStack: 999, value: 1 });
403	item({ key: 'vi_906_lava_charm', name: '', maxStack: 999, value: 1 });
404	item({ key: 'vi_4055_dunerider_boots', name: '', maxStack: 999, value: 1 });
405	item({ key: 'vi_724_ice_blade', name: '', maxStack: 999, value: 1 });
406	item({ key: 'vi_670_ice_boomerang', name: '', maxStack: 999, value: 1 });
407	item({ key: 'vi_4061_storm_spear', name: '', maxStack: 999, value: 1 });
408	item({ key: 'vi_987_blizzard_in_a_bottle', name: '', maxStack: 999, value: 1 });
409	item({ key: 'vi_4551_slice_of_hell_cake', name: '', maxStack: 999, value: 1 });
410	item({ key: 'vi_5010_treasure_magnet', name: '', maxStack: 999, value: 1 });
411	item({ key: 'vi_2323_heartreach_potion', name: '', maxStack: 999, value: 1 });
412	item({ key: 'vi_2345_lifeforce_potion', name: '', maxStack: 999, value: 1 });
413	item({ key: 'vi_290_swiftness_potion', name: '', maxStack: 999, value: 1 });
414	item({ key: 'vi_291_gills_potion', name: '', maxStack: 999, value: 1 });
415	item({ key: 'vi_280_spear', name: '', maxStack: 999, value: 1 });
416	item({ key: 'vi_2325_builder_potion', name: '', maxStack: 999, value: 1 });
417	item({ key: 'vi_284_wooden_boomerang', name: '', maxStack: 999, value: 1 });
418	item({ key: 'vi_2192_bone_welder', name: '', maxStack: 999, value: 1 });
419	item({ key: 'vi_5234_remnants_of_devotion', name: '', maxStack: 999, value: 1 });
420	item({ key: 'vi_156_cobalt_shield', name: '', maxStack: 999, value: 1 });
421	item({ key: 'vi_157_aqua_scepter', name: '', maxStack: 999, value: 1 });
422	item({ key: 'vi_163_blue_moon', name: '', maxStack: 999, value: 1 });
423	item({ key: 'vi_113_magic_missile', name: '', maxStack: 999, value: 1 });
424	item({ key: 'vi_3317_valor', name: '', maxStack: 999, value: 1 });
425	item({ key: 'vi_327_golden_key', name: '', maxStack: 999, value: 1 });
426	item({ key: 'vi_164_handgun', name: '', maxStack: 999, value: 1 });
427	item({ key: 'vi_294_magic_power_potion', name: '', maxStack: 999, value: 1 });
428	item({ key: 'vi_4263_magic_conch', name: '', maxStack: 999, value: 1 });
429	item({ key: 'vi_4062_thunder_zapper', name: '', maxStack: 999, value: 1 });
430	item({ key: 'vi_1579_flurry_boots', name: '', maxStack: 999, value: 1 });
431	item({ key: 'vi_4056_ancient_chisel', name: '', maxStack: 999, value: 1 });
432	item({ key: 'vi_4346_encumbering_stone', name: '', maxStack: 999, value: 1 });
433	item({ key: 'vi_1319_snowball_cannon', name: '', maxStack: 999, value: 1 });
434	item({ key: 'vi_3199_ice_mirror', name: '', maxStack: 999, value: 1 });
435	item({ key: 'vi_950_ice_skates', name: '', maxStack: 999, value: 1 });
436	item({ key: 'vi_4443_demonic_hellcart', name: '', maxStack: 999, value: 1 });
437	item({ key: 'vi_4737_ornate_shadow_key', name: '', maxStack: 999, value: 1 });
438	item({ key: 'vi_4276_bast_statue', name: '', maxStack: 999, value: 1 });
439	item({ key: 'vi_4262_snake_charmer_s_flute', name: '', maxStack: 999, value: 1 });
440	item({ key: 'vi_3093_herb_bag', name: '', maxStack: 999, value: 1 });
441	item({ key: 'vi_292_ironskin_potion', name: '', maxStack: 999, value: 1 });
442	item({ key: 'vi_3084_radar', name: '', maxStack: 999, value: 1 });
443	item({ key: 'vi_4341_step_stool', name: '', maxStack: 999, value: 1 });
444	item({ key: 'vi_4978_fledgling_wings', name: '', maxStack: 999, value: 1 });
445	item({ key: 'vi_2197_sky_mill', name: '', maxStack: 999, value: 1 });
446	item({ key: 'vi_158_lucky_horseshoe', name: '', maxStack: 999, value: 1 });
447	item({ key: 'vi_5254_blessing_from_the_heavens', name: '', maxStack: 999, value: 1 });
448	item({ key: 'vi_1156_piranha_gun', name: '', maxStack: 999, value: 1 });
449	item({ key: 'vi_1571_scourge_of_the_corruptor', name: '', maxStack: 999, value: 1 });
450	item({ key: 'vi_1260_rainbow_gun', name: '', maxStack: 999, value: 1 });
451	item({ key: 'vi_1572_staff_of_the_frost_hydra', name: '', maxStack: 999, value: 1 });
452	item({ key: 'vi_4607_desert_tiger_staff', name: '', maxStack: 999, value: 1 });
453	item({ key: 'vi_933_leaf_wand', name: '', maxStack: 999, value: 1 });
454	item({ key: 'vi_832_living_wood_wand', name: '', maxStack: 999, value: 1 });
455	item({ key: 'vi_4066_desert_minecart', name: '', maxStack: 999, value: 1 });
456	item({ key: 'vi_4450_shroom_minecart', name: '', maxStack: 999, value: 1 });
457	item({ key: 'vi_4423_scarab_bomb', name: '', maxStack: 999, value: 1 });
458	item({ key: 'vi_159_shiny_red_balloon', name: '', maxStack: 999, value: 1 });
459	item({ key: 'vi_5258_see_the_world_for_what_it_is', name: '', maxStack: 999, value: 1 });
460	item({ key: 'vi_65_starfury', name: '', maxStack: 999, value: 1 });
461	item({ key: 'vi_5388_eye_of_the_sun', name: '', maxStack: 999, value: 1 });
462	item({ key: 'vi_2219_celestial_magnet', name: '', maxStack: 999, value: 1 });
463	item({ key: 'vi_5255_love_is_in_the_trash_slot', name: '', maxStack: 999, value: 1 });
464	item({ key: 'vi_4426_bee_minecart', name: '', maxStack: 999, value: 1 });
465	item({ key: 'vi_3017_flower_boots', name: '', maxStack: 999, value: 1 });
466	item({ key: 'vi_3360_living_mahogany_wand', name: '', maxStack: 999, value: 1 });
467	item({ key: 'vi_3361_rich_mahogany_leaf_wand', name: '', maxStack: 999, value: 1 });
468	item({ key: 'vi_1309_slime_staff', name: '', maxStack: 999, value: 1 });
469	item({ key: 'vi_1845_necromantic_scroll', name: '', maxStack: 999, value: 1 });
470	item({ key: 'vi_1864_papyrus_scarab', name: '', maxStack: 999, value: 1 });
471	item({ key: 'vi_1158_pygmy_necklace', name: '', maxStack: 999, value: 1 });
472	item({ key: 'vi_3034_coin_ring', name: '', maxStack: 999, value: 1 });
473	item({ key: 'vi_308_moonglow_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 1 });
474	item({ key: 'vi_312_fireblossom_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 5 });
475	item({ key: 'vi_310_deathweed_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 4 });
476	item({ key: 'vi_307_daybloom_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 0 });
477	item({ key: 'vi_309_blinkroot_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 2 });
478	item({ key: 'vi_2357_shiverthorn_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 6 });
479	item({ key: 'vi_311_waterleaf_seeds', name: '', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 3 });
480	item({ key: 'vi_1828_pumpkin_seed', name: '', maxStack: 999, value: 1 });
481	item({ key: 'vi_126_bottled_water', name: '', maxStack: 999, value: 1 });
482	item({ key: 'vi_1134_bottled_honey', name: '', maxStack: 999, value: 1 });
483	item({ key: 'vi_3068_guide_to_plant_fiber_cordage', name: '', maxStack: 999, value: 1 });
484	item({ key: 'vi_4779_mushroom_hat', name: '', maxStack: 999, value: 1 });
485	item({ key: 'vi_4780_mushroom_vest', name: '', maxStack: 999, value: 1 });
486	item({ key: 'vi_4781_mushroom_pants', name: '', maxStack: 999, value: 1 });
487	
488	// ===================== FTW_V2 补全物品（占位收集品） =====================
489	item({ key: 'vi_678_red_potion', name: '', maxStack: 999, value: 1 });
490	item({ key: 'vi_281_blowpipe', name: '', maxStack: 999, value: 1 });
491	item({ key: 'vi_293_mana_regeneration_potion', name: '', maxStack: 999, value: 1 });
492	item({ key: 'vi_2767_solar_tablet', name: '', maxStack: 999, value: 1 });
493	item({ key: 'vi_3213_money_trough', name: '', maxStack: 999, value: 1 });
494	item({ key: 'vi_2757_vortex_helmet', name: '', maxStack: 999, value: 1 });
495	item({ key: 'vi_4989_soaring_insignia', name: '', maxStack: 999, value: 1 });
496	item({ key: 'vi_3383_stardust_leggings', name: '', maxStack: 999, value: 1 });
497	item({ key: 'vi_4914_kaleidoscope', name: '', maxStack: 999, value: 1 });
498	item({ key: 'vi_1991_bug_net', name: '', maxStack: 999, value: 1 });
499	item({ key: 'vi_4828_superheated_blood', name: '', maxStack: 999, value: 1 });
500	item({ key: 'vi_3509_copper_pickaxe', name: '', maxStack: 999, value: 1 });
501	item({ key: 'vi_3507_copper_shortsword', name: '', maxStack: 999, value: 1 });
502	item({ key: 'vi_4755_grox_the_great_s_horned_cowl', name: '', maxStack: 999, value: 1 });
503	item({ key: 'vi_4756_grox_the_great_s_chestplate', name: '', maxStack: 999, value: 1 });
504	item({ key: 'vi_4757_grox_the_great_s_greaves', name: '', maxStack: 999, value: 1 });
505	item({ key: 'vi_5000_terraspark_boots', name: '', maxStack: 999, value: 1 });
506	item({ key: 'vi_5339_arcane_crystal', name: '', maxStack: 999, value: 1 });
507	// 永久幸运消耗品（Player.cs:44786-44789：一次性 usedGalaxyPearl → luck +0.03 :28676-28678）
508	item({ key: 'vi_5340_galaxy_pearl', name: '', maxStack: 999, value: 1 });
509	// 漂亮镜子（Item 5577：投掷消耗品，shoot 1085；碎裂近身 150px → brokenMirrorBadLuckTime
510	// 25200，Projectile.cs:67554-67574）——投掷走 thrownCombat 通用管线
511	item({ key: 'vi_5577_pretty_mirror', name: '', maxStack: 999, value: 1 });
512	item({ key: 'vi_5391_uncumbering_stone', name: '', maxStack: 999, value: 1 });
513	item({ key: 'vi_2585_slime_hook', name: '', maxStack: 999, value: 1 });
514	item({ key: 'vi_313_daybloom', name: '', maxStack: 999, value: 1 });
515	item({ key: 'vi_267_guide_voodoo_doll', name: '', maxStack: 999, value: 1 });
516	item({ key: 'vi_2649_steampunk_candle', name: '', maxStack: 999, value: 1 });
517	item({ key: 'vi_286_sticky_glowstick', name: '', maxStack: 999, value: 1 });
518	item({ key: 'vi_3002_spelunker_glowstick', name: '', maxStack: 999, value: 1 });
519	item({ key: 'vi_4819_demon_conch', name: '', maxStack: 999, value: 1 });
520	item({ key: 'vi_1802_raven_staff', name: '', maxStack: 999, value: 1 });
521	item({ key: 'vi_3382_stardust_plate', name: '', maxStack: 999, value: 1 });
522	item({ key: 'vi_3270_item_frame', name: '', maxStack: 999, value: 1 });
523	item({ key: 'vi_3771_ancient_horn', name: '', maxStack: 999, value: 1 });
524	item({ key: 'vi_4281_finch_staff', name: '', maxStack: 999, value: 1 });
525	item({ key: 'vi_5407_star_royale_brick', name: '', maxStack: 999, value: 1, tile: 'v_675_star_royale_brick' });
526	item({ key: 'vi_5401_lunar_rust_brick', name: '', maxStack: 999, value: 1, tile: 'v_669_lunar_rust_brick' });
527	// 月相砖族补全（3461 微光转化目标，ItemID.cs:5401-5408;★曾缺 5402/5406/5408 →
528	// 转化到这三相静默丢物;tile 744-751? 见 vanilla sheet 注册——砖块放置链按需接）
529	item({ key: 'vi_5402_dark_celestial_brick', name: '', maxStack: 999, value: 1, tile: 'v_670_dark_celestial_brick' });
530	item({ key: 'vi_5406_mercury_brick', name: '', maxStack: 999, value: 1, tile: 'v_674_mercury_brick' });
531	item({ key: 'vi_5408_heavenforge_brick', name: '', maxStack: 999, value: 1, tile: 'v_676_heavenforge_brick' });
532	item({ key: 'vi_4716_mollusk_whistle', name: '', maxStack: 999, value: 1 });
533	item({ key: 'vi_3540_phantasm', name: '', maxStack: 999, value: 1 });
534	item({ key: 'vi_2176_shroomite_digging_claw', name: '', maxStack: 999, value: 1 });
535	item({ key: 'vi_2349_wrath_potion', name: '', maxStack: 999, value: 1 });
536	item({ key: 'vi_4679_morning_star', name: '', maxStack: 999, value: 1 });
537	item({ key: 'vi_1169_bone_key', name: '', maxStack: 999, value: 1 });
538	item({ key: 'vi_3863_betsy_mask', name: '', maxStack: 999, value: 1 });
539	item({ key: 'vi_3124_cell_phone', name: '', maxStack: 999, value: 1 });
540	item({ key: 'vi_3506_copper_axe', name: '', maxStack: 999, value: 1 });
541	item({ key: 'vi_4680_dark_harvest', name: '', maxStack: 999, value: 1 });
542	item({ key: 'vi_543_brown_pressure_plate', name: '', maxStack: 999, value: 1 });
543	item({ key: 'vi_171_sign', name: '', maxStack: 999, value: 1 });
544	item({ key: 'vi_1723_living_wood_wall', name: '', maxStack: 999, value: 1 });
545	item({ key: 'vi_4754_grox_the_great_s_wings', name: '', maxStack: 999, value: 1 });
546	item({ key: 'vi_3353_mechanical_cart', name: '', maxStack: 999, value: 1 });
547	item({ key: 'vi_2287_winter_cape', name: '', maxStack: 999, value: 1 });
548	item({ key: 'vi_1179_chlorophyte_bullet', name: '', maxStack: 999, value: 1 });
549	item({ key: 'vi_4766_world_globe', name: '', maxStack: 999, value: 1 });
550	item({ key: 'vi_4954_celestial_starboard', name: '', maxStack: 999, value: 1 });
551	item({ key: 'vi_4730_ghostar_s_infinity_eight', name: '', maxStack: 999, value: 1 });
552	item({ key: 'vi_4758_blade_staff', name: '', maxStack: 999, value: 1 });
553	item({ key: 'vi_4765_tree_globe', name: '', maxStack: 999, value: 1 });
554	item({ key: 'vi_5342_ambrosia', name: '', maxStack: 999, value: 1 });
555	item({ key: 'vi_5328_chest_lock', name: '', maxStack: 999, value: 1 });
556	item({ key: 'vi_5343_peddler_s_satchel', name: '', maxStack: 999, value: 1 });
557	item({ key: 'vi_5285_moon_globe', name: '', maxStack: 999, value: 1 });
558	item({ key: 'vi_5289_minecart_upgrade_kit', name: '', maxStack: 999, value: 1 });
559	item({ key: 'vi_5336_advanced_combat_techniques_volume_two', name: '', maxStack: 999, value: 1 });
560	item({ key: 'vi_5451_kwad_racer_drone', name: '', maxStack: 999, value: 1 });
561	item({ key: 'vi_5359_shellphone_spawn', name: '', maxStack: 999, value: 1 });
562	item({ key: 'vi_3032_super_absorbant_sponge', name: '', maxStack: 999, value: 1 });
563	item({ key: 'vi_3031_bottomless_water_bucket', name: '', maxStack: 999, value: 1 });
564	item({ key: 'vi_509_red_wrench', name: '', maxStack: 999, value: 1 });
565	item({ key: 'vi_4741_butcher_s_bloodstained_apron', name: '', maxStack: 999, value: 1 });
566	item({ key: 'vi_3065_star_wrath', name: '', maxStack: 999, value: 1 });
567	item({ key: 'vi_3063_meowmere', name: '', maxStack: 999, value: 1 });
568	item({ key: 'vi_3372_lunatic_cultist_mask', name: '', maxStack: 999, value: 1 });
569	item({ key: 'vi_1504_spectre_robe', name: '', maxStack: 999, value: 1 });
570	item({ key: 'vi_2769_cosmic_car_key', name: '', maxStack: 999, value: 1 });
571	item({ key: 'vi_216_shackle', name: '', maxStack: 999, value: 1 });
572	item({ key: 'vi_4415_stone_door', name: '', maxStack: 999, value: 1 });
573	item({ key: 'vi_1681_skeleton_banner', name: '', maxStack: 999, value: 1 });
574	item({ key: 'vi_283_seed', name: '', maxStack: 999, value: 1 });
575	item({ key: 'vi_1173_grave_marker', name: '', maxStack: 999, value: 1 });
576	item({ key: 'vi_4379_wyvern_kite', name: '', maxStack: 999, value: 1 });
577	item({ key: 'vi_4378_xenon_moss', name: '', maxStack: 999, value: 1 });
578	item({ key: 'vi_4377_krypton_moss', name: '', maxStack: 999, value: 1 });
579	item({ key: 'vi_4376_rat_cage', name: '', maxStack: 999, value: 1 });
580	item({ key: 'vi_4375_rat', name: '', maxStack: 999, value: 1 });
581	item({ key: 'vi_4484_1_2_second_timer', name: '', maxStack: 999, value: 1 });
582	item({ key: 'vi_4824_wet_bomb', name: '', maxStack: 999, value: 1 });
583	item({ key: 'vi_4485_1_4_second_timer', name: '', maxStack: 999, value: 1 });
584	item({ key: 'vi_5378_cursed_flare', name: '', maxStack: 999, value: 1 });
585	item({ key: 'vi_5354_reflective_shades', name: '', maxStack: 999, value: 1 });
586	item({ key: 'vi_5387_raynbro_s_pants', name: '', maxStack: 999, value: 1 });
587	item({ key: 'vi_5386_raynbro_s_hoodie', name: '', maxStack: 999, value: 1 });
588	item({ key: 'vi_5390_raynbro_s_hood', name: '', maxStack: 999, value: 1 });
589	item({ key: 'vi_5338_aegis_fruit', name: '', maxStack: 999, value: 1 });
590	item({ key: 'vi_5404_cosmic_ember_brick', name: '', maxStack: 999, value: 1, tile: 'v_672_cosmic_ember_brick' });
591	item({ key: 'vi_5405_cryocore_brick', name: '', maxStack: 999, value: 1, tile: 'v_673_cryocore_brick' });
592	item({ key: 'vi_5403_astra_brick', name: '', maxStack: 999, value: 1, tile: 'v_671_astra_brick' });
593	item({ key: 'vi_346_safe', name: '', maxStack: 999, value: 1 });
594	item({ key: 'vi_4829_cat_license', name: '', maxStack: 999, value: 1 });
595	item({ key: 'vi_3335_demon_heart', name: '', maxStack: 999, value: 1 });
596	item({ key: 'vi_4750_foodbarbarian_s_tattered_dragon_wings', name: '', maxStack: 999, value: 1 });
597	item({ key: 'vi_3042_phase_dye', name: '', maxStack: 999, value: 1 });
598	item({ key: 'vi_3024_skiphs_blood', name: '', maxStack: 999, value: 1 });
599	item({ key: 'vi_3054_shadowflame_knife', name: '', maxStack: 999, value: 1 });
600	item({ key: 'vi_5275_joja_cola', name: '', maxStack: 999, value: 1 });
601	item({ key: 'vi_5278_pomegranate', name: '', maxStack: 999, value: 1 });
602	item({ key: 'vi_5277_spicy_pepper', name: '', maxStack: 999, value: 1 });
603	item({ key: 'vi_5437_shellphone', name: '', maxStack: 999, value: 1 });
604	item({ key: 'vi_1507_spectre_hamaxe', name: '', maxStack: 999, value: 1 });
605	item({ key: 'vi_2250_steampunk_chest', name: '', maxStack: 999, value: 1 });
606	item({ key: 'vi_392_glass_wall', name: '', maxStack: 999, value: 1 });
607	item({ key: 'vi_2699_weapon_rack', name: '', maxStack: 999, value: 1 });
608	item({ key: 'vi_3552_blue_flame_and_silver_dye', name: '', maxStack: 999, value: 1 });
609	item({ key: 'vi_5005_terraprisma', name: '', maxStack: 999, value: 1 });
610	item({ key: 'vi_4604_exotic_chew_toy', name: '', maxStack: 999, value: 1 });
611	item({ key: 'vi_4611_world_feeder_kite', name: '', maxStack: 999, value: 1 });
612	item({ key: 'vi_4649_blue_jellyfish_kite', name: '', maxStack: 999, value: 1 });
613	item({ key: 'vi_4796_dark_mage_s_tome', name: '', maxStack: 999, value: 1 });
614	item({ key: 'vi_4553_plasma_lamp', name: '', maxStack: 999, value: 1 });
615	item({ key: 'vi_4365_celestial_wand', name: '', maxStack: 999, value: 1 });
616	item({ key: 'vi_331_jungle_spores', name: '', maxStack: 999, value: 1 });
617	item({ key: 'vi_2430_slimy_saddle', name: '', maxStack: 999, value: 1 });
618	item({ key: 'vi_4956_zenith', name: '', maxStack: 999, value: 1 });
619	item({ key: 'vi_2798_laser_drill', name: '', maxStack: 999, value: 1 });
620	item({ key: 'vi_2814_martian_chest', name: '', maxStack: 999, value: 1 });
621	item({ key: 'vi_210_vine', name: '', maxStack: 999, value: 1 });
622	item({ key: 'vi_4371_yellow_kite', name: '', maxStack: 999, value: 1 });
623	item({ key: 'vi_4291_lemon', name: '', maxStack: 999, value: 1 });
624	item({ key: 'vi_2493_king_slime_mask', name: '', maxStack: 999, value: 1 });
625	item({ key: 'vi_1919_sugar_cookie', name: '', maxStack: 999, value: 1 });
626	item({ key: 'vi_1912_eggnog', name: '', maxStack: 999, value: 1 });
627	item({ key: 'vi_4023_grapes', name: '', maxStack: 999, value: 1 });
628	item({ key: 'vi_4792_the_black_spot', name: '', maxStack: 999, value: 1 });
629	item({ key: 'vi_3066_smooth_marble_block', name: '', maxStack: 999, value: 1 });
630	item({ key: 'vi_1103_slush_block', name: '', maxStack: 999, value: 1 });
631	item({ key: 'vi_2119_stone_slab', name: '', maxStack: 999, value: 1 });
632	item({ key: 'vi_593_snow_block', name: '', maxStack: 999, value: 1 });
633	item({ key: 'vi_3081_marble_block', name: '', maxStack: 999, value: 1 });
634	item({ key: 'vi_1111_blue_berries', name: '', maxStack: 999, value: 1 });
635	item({ key: 'vi_1115_red_husk', name: '', maxStack: 999, value: 1 });
636	item({ key: 'vi_217_molten_hamaxe', name: '', maxStack: 999, value: 1 });
637	item({ key: 'vi_122_molten_pickaxe', name: '', maxStack: 999, value: 1 });
638	item({ key: 'vi_1827_bladed_glove', name: '', maxStack: 999, value: 1 });
639	item({ key: 'vi_2263_white_dynasty_wall', name: '', maxStack: 999, value: 1 });
640	item({ key: 'vi_330_obsidian_brick_wall', name: '', maxStack: 999, value: 1 });
641	item({ key: 'vi_2433_stone_slab_wall', name: '', maxStack: 999, value: 1 });
642	item({ key: 'vi_452_hornet_statue', name: '', maxStack: 999, value: 1 });
643	item({ key: 'vi_453_bomb_statue', name: '', maxStack: 999, value: 1 });
644	item({ key: 'vi_360_armor_statue', name: '', maxStack: 999, value: 1 });
645	item({ key: 'vi_3711_wraith_statue', name: '', maxStack: 999, value: 1 });
646	item({ key: 'vi_438_star_statue', name: '', maxStack: 999, value: 1 });
647	item({ key: 'vi_446_skeleton_statue', name: '', maxStack: 999, value: 1 });
648	item({ key: 'vi_458_cross_statue', name: '', maxStack: 999, value: 1 });
649	item({ key: 'vi_3655_scorpion_statue', name: '', maxStack: 999, value: 1 });
650	item({ key: 'vi_328_shadow_chest', name: '', maxStack: 999, value: 1 });
651	item({ key: 'vi_2196_living_loom', name: '', maxStack: 999, value: 1 });
652	item({ key: 'vi_916_shadewood_work_bench', name: '', maxStack: 999, value: 1 });
653	item({ key: 'vi_35_iron_anvil', name: '', maxStack: 999, value: 1 });
654	item({ key: 'vi_36_work_bench', name: '', maxStack: 999, value: 1 });
655	item({ key: 'vi_3240_tall_gate', name: '', maxStack: 999, value: 1 });
656	item({ key: 'vi_337_red_banner', name: '', maxStack: 999, value: 1 });
657	item({ key: 'vi_3381_stardust_helmet', name: '', maxStack: 999, value: 1 });
658	item({ key: 'vi_1765_vampire_pants', name: '', maxStack: 999, value: 1 });
659	item({ key: 'vi_2859_lunar_cultist_robe', name: '', maxStack: 999, value: 1 });
660	item({ key: 'vi_2857_lunar_cultist_hood', name: '', maxStack: 999, value: 1 });
661	item({ key: 'vi_2998_summoner_emblem', name: '', maxStack: 999, value: 1 });
662	item({ key: 'vi_1175_headstone', name: '', maxStack: 999, value: 1 });
663	item({ key: 'vi_25_wooden_door', name: '', maxStack: 999, value: 1 });
664	item({ key: 'vi_46_light_s_bane', name: '', maxStack: 999, value: 1 });
665	item({ key: 'vi_2340_minecart_track', name: '', maxStack: 999, value: 1 });
666	// 轨道族放置物（Minecart.PlaceTrack style：0 普通 / 1 压板(2492) / 2 左加速(2739)）。
667	// key 沿用全量注册的 vanilla.json 命名（vi_<id>_<key>），只补 tile/placeStyle
668	item({ key: 'vi_2492_PressureTrack', name: '', maxStack: 999, value: 1, tile: 'v_314_minecart_track', placeStyle: 1 });
669	item({ key: 'vi_2739_BoosterTrack', name: '', maxStack: 999, value: 1, tile: 'v_314_minecart_track', placeStyle: 2 });
670	item({ key: 'vi_498_mannequin', name: '', maxStack: 999, value: 1 });
671	item({ key: 'vi_4721_mushroom_beam', name: '', maxStack: 999, value: 1 });
672	item({ key: 'vi_819_living_wood_door', name: '', maxStack: 999, value: 1 });
673	item({ key: 'vi_1458_obsidian_door', name: '', maxStack: 999, value: 1 });
674	item({ key: 'vi_3763_0x33_s_aviators', name: '', maxStack: 999, value: 1 });
675	item({ key: 'vi_176_mud_block', name: '', maxStack: 999, value: 1 });
676	item({ key: 'vi_1569_vampire_knives', name: '', maxStack: 999, value: 1 });
677	item({ key: 'vi_857_sandstorm_in_a_bottle', name: '', maxStack: 999, value: 1 });
678	item({ key: 'vi_2292_fiberglass_fishing_pole', name: '', maxStack: 999, value: 1 });
679	item({ key: 'vi_5238_constellation', name: '', maxStack: 999, value: 1 });
680	item({ key: 'vi_753_seaweed', name: '', maxStack: 999, value: 1 });
681	// FTW_V2 物品补全（第二轮）
682	item({ key: 'vi_3_stone_block', name: '', maxStack: 999, value: 1 });
683	item({ key: 'vi_94_wood_platform', name: '', maxStack: 999, value: 1 });
684	item({ key: 'vi_75_fallen_star', name: '', maxStack: 999, value: 1 });
685	item({ key: 'vi_26_stone_wall', name: '', maxStack: 999, value: 1 });
686	item({ key: 'vi_214_hellstone_brick', name: '', maxStack: 999, value: 1 });
687	item({ key: 'vi_93_wood_wall', name: '', maxStack: 999, value: 1 });
688	item({ key: 'vi_172_ash_block', name: '', maxStack: 999, value: 1 });
689	item({ key: 'vi_118_hook', name: '', maxStack: 999, value: 1 });
690	item({ key: 'vi_529_red_pressure_plate', name: '', maxStack: 999, value: 1 });
691	item({ key: 'vi_183_glowing_mushroom', name: '', maxStack: 999, value: 1 });
692	item({ key: 'vi_130_gray_brick_wall', name: '', maxStack: 999, value: 1 });
693	item({ key: 'vi_352_keg', name: '', maxStack: 999, value: 1 });
694	
695	// 不负责任的女妖啤酒厂 补全物品（占位收集品）
696	item({ key: 'vi_5120_deer_thing', name: '', maxStack: 999, value: 1 });
697	item({ key: 'vi_5508_grim_old_barb', name: '', maxStack: 999, value: 1 });
698	item({ key: 'vi_5465_ram_rune', name: '', maxStack: 999, value: 1 });
699	item({ key: 'vi_5500_goat_s_tuft', name: '', maxStack: 999, value: 1 });
700	item({ key: 'vi_5499_froggy_neckband', name: '', maxStack: 999, value: 1 });
701	item({ key: 'vi_5507_balloony_beads', name: '', maxStack: 999, value: 1 });
702	item({ key: 'vi_5485_chicken_charm', name: '', maxStack: 999, value: 1 });
703	item({ key: 'vi_5502_cat_chime', name: '', maxStack: 999, value: 1 });
704	item({ key: 'vi_5504_turkey_wattle_necklace', name: '', maxStack: 999, value: 1 });
705	item({ key: 'vi_5506_crow_s_beak', name: '', maxStack: 999, value: 1 });
706	item({ key: 'vi_5503_dog_collar', name: '', maxStack: 999, value: 1 });
707	item({ key: 'vi_5534_fairy_choker', name: '', maxStack: 999, value: 1 });
708	item({ key: 'vi_5484_cow_bell', name: '', maxStack: 999, value: 1 });
709	item({ key: 'vi_5501_old_companion_locket', name: '', maxStack: 999, value: 1 });
710	item({ key: 'vi_5509_vampire_pendant', name: '', maxStack: 999, value: 1 });
711	item({ key: 'vi_5505_mean_goblin_s_spikes', name: '', maxStack: 999, value: 1 });
712	item({ key: 'vi_5525_cursed_piper_flute', name: '', maxStack: 999, value: 1 });
713	
714	
715	// ---- 阶段 5:v_ 图块放置物品自动注册 + 掉落连线 ----
716	// 每个 v_ 图块注册 place_v_<key> 放置物品(tryPlace 走 vanilla style 帧语义);
717	// 无掉落的 v_ 图块 drop 连到该物品(破坏可回收再放置)。
718	import { TILE_DEFS } from './tiles';
719	for (const td of TILE_DEFS) {
720	  if (!td.key.startsWith('v_')) continue;
721	  const ik = 'place_' + td.key;
722	  if (byKey[ik] === undefined) {
723	    item({ key: ik, name: '', maxStack: 999, value: 1, tile: td.key });
724	  }
725	  // 掉落连线在读取端回退(World.breakTileAt),避免多模块实例下改写失效
726	}
727	void 0;
728	
729	// ---- 阶段 5:生物群系草种子(种出对应草块)----
730	item({ key: 'corrupt_grass_seeds', name: '腐化草地种子', maxStack: 999, value: 1, tile: 'v_23_corrupt_grass_block' });
731	item({ key: 'crimson_grass_seeds', name: '猩红草地种子', maxStack: 999, value: 1, tile: 'v_199_crimson_grass_block' });
732	item({ key: 'jungle_grass_seeds', name: '丛林草地种子', maxStack: 999, value: 1, tile: 'v_60_jungle_grass_block' });
733	item({ key: 'mushroom_grass_seeds', name: '蘑菇草地种子', maxStack: 999, value: 1, tile: 'v_70_mushroom_grass_block' });
734	
735	
736	// ---- 阶段 5:原版物品全量注册(6146 件,图标走 atlas.vicon(id) 回退) ----
737	import vanillaItemMeta from '../../public/sprites/vanilla.json';
738	import { MUSIC_BOX_ITEM_BY_STYLE } from '../world/wiring/devices';
739	/** 原版物品 id → 注册 key（wld 导入兜底映射：ITEM_MAP 之外的 id 不再跳过） */
740	// ===================== 原版工具力道具补齐（锤/镐梯度,Item.cs 提取） =====================
741	item({ key: 'vi_103_nightmare_pickaxe', name: '', maxStack: 999, value: 1 });
742	item({ key: 'vi_104_the_breaker', name: '', maxStack: 999, value: 1 });
743	item({ key: 'vi_122_molten_pickaxe', name: '', maxStack: 999, value: 1 });
744	item({ key: 'vi_204_meteor_hamaxe', name: '', maxStack: 999, value: 1 });
745	item({ key: 'vi_217_molten_hamaxe', name: '', maxStack: 999, value: 1 });
746	item({ key: 'vi_367_pwnhammer', name: '', maxStack: 999, value: 1 });
747	item({ key: 'vi_579_drax', name: '', maxStack: 999, value: 1 });
748	item({ key: 'vi_654_ebonwood_hammer', name: '', maxStack: 999, value: 1 });
749	item({ key: 'vi_657_rich_mahogany_hammer', name: '', maxStack: 999, value: 1 });
750	item({ key: 'vi_660_pearlwood_hammer', name: '', maxStack: 999, value: 1 });
751	item({ key: 'vi_776_cobalt_pickaxe', name: '', maxStack: 999, value: 1 });
752	item({ key: 'vi_777_mythril_pickaxe', name: '', maxStack: 999, value: 1 });
753	item({ key: 'vi_778_adamantite_pickaxe', name: '', maxStack: 999, value: 1 });
754	item({ key: 'vi_787_hammush', name: '', maxStack: 999, value: 1 });
755	item({ key: 'vi_797_flesh_grinder', name: '', maxStack: 999, value: 1 });
756	item({ key: 'vi_798_deathbringer_pickaxe', name: '', maxStack: 999, value: 1 });
757	item({ key: 'vi_922_shadewood_hammer', name: '', maxStack: 999, value: 1 });
758	item({ key: 'vi_990_pickaxe_axe', name: '', maxStack: 999, value: 1 });
759	item({ key: 'vi_1188_palladium_pickaxe', name: '', maxStack: 999, value: 1 });
760	item({ key: 'vi_1195_orichalcum_pickaxe', name: '', maxStack: 999, value: 1 });
761	item({ key: 'vi_1202_titanium_pickaxe', name: '', maxStack: 999, value: 1 });
762	item({ key: 'vi_1234_chlorophyte_warhammer', name: '', maxStack: 999, value: 1 });
763	item({ key: 'vi_1262_chlorophyte_jackhammer', name: '', maxStack: 999, value: 1 });
764	item({ key: 'vi_1305_the_axe', name: '', maxStack: 999, value: 1 });
765	item({ key: 'vi_1506_spectre_pickaxe', name: '', maxStack: 999, value: 1 });
766	item({ key: 'vi_1507_spectre_hamaxe', name: '', maxStack: 999, value: 1 });
767	item({ key: 'vi_3481_platinum_hammer', name: '', maxStack: 999, value: 1 });
768	item({ key: 'vi_3487_tungsten_hammer', name: '', maxStack: 999, value: 1 });
769	item({ key: 'vi_3493_lead_hammer', name: '', maxStack: 999, value: 1 });
770	item({ key: 'vi_3499_tin_hammer', name: '', maxStack: 999, value: 1 });
771	item({ key: 'vi_3505_copper_hammer', name: '', maxStack: 999, value: 1 });
772	item({ key: 'vi_3511_silver_hammer', name: '', maxStack: 999, value: 1 });
773	item({ key: 'vi_3517_gold_hammer', name: '', maxStack: 999, value: 1 });
774	item({ key: 'vi_3525_stardust_hamaxe', name: '', maxStack: 999, value: 1 });
775	item({ key: 'vi_4317_haemorrhaxe', name: '', maxStack: 999, value: 1 });
776	
777	// 月事件触发物品（Player.cs:43294/43361：夜晚 && 无进行中月事件；Main.startPumpkinMoon/
778	// startSnowMoon :10903-10940）。键用 vanilla.json 权威驼峰键（下方自动注册循环按此键
779	// 跳过，避免同 vid 双注册）；原版 maxStack 20 / useTime 45（Item.cs:20377-21128）
780	item({ key: 'vi_1844_PumpkinMoonMedallion', name: '', vid: 1844, maxStack: 20, value: 1, desc: '夜晚使用:召唤南瓜月' });
781	item({ key: 'vi_1958_NaughtyPresent', name: '', vid: 1958, maxStack: 20, value: 1, desc: '夜晚使用:召唤霜月' });
782	
783	export const VANILLA_ITEM_KEY_BY_ID: Record<number, string> = {};
784	const _vim = (vanillaItemMeta as unknown as { items: Record<string, { name: string; key: string }> }).items ?? {};
785	for (const [idStr, m] of Object.entries(_vim)) {
786	  if (!m || typeof m.key !== 'string' || !m.key) continue;
787	  const ik = 'vi_' + idStr + '_' + m.key.replace(/[^A-Za-z0-9]/g, '');
788	  VANILLA_ITEM_KEY_BY_ID[Number(idStr)] = ik; // 已注册的同样入表（wld 导入按 id 反查）
789	  if (byKey[ik] !== undefined) continue;
790	  item({ key: ik, name: '', maxStack: 999, value: 1 });
791	}
792	
793	// ---- 音乐盒唱片全量 101 曲（Item.cs DefaultToMusicBox：createTile=139、
794	// placeStyle=曲目 style、accessory；style 表 = WorldGen.GetItemDrop_MusicBoxes
795	// :43138-43366 逆表）。6145 彩虹巨石/6146 静音盒无素材不在 vanilla.json，单独注册。
796	// 放置帧走 FurnitureStyle case 139（frameY = style*36）；录音变身链见
797	// world/wiring/devices.ts musicBoxRecordItem（Player.cs:15053） ----
798	const MB_NO_SPRITE: Record<number, number> = { 6145: 99, 6146: 100 };
799	for (const [mbVid, mbStyle] of Object.entries(MB_NO_SPRITE)) {
800	  const mbKey = `vi_${mbVid}_MusicBox${Number(mbVid) === 6146 ? 'Silence' : 'RainbowBoulder'}`;
801	  VANILLA_ITEM_KEY_BY_ID[Number(mbVid)] = mbKey; // 掉落/录音链按 vid 反查
802	  item({ key: mbKey, name: '', maxStack: 1, value: 100000, tile: 'v_139_musicboxes', placeStyle: mbStyle });
803	}
804	for (let mbStyle = 0; mbStyle < 100; mbStyle++) {
805	  const mbKey = VANILLA_ITEM_KEY_BY_ID[MUSIC_BOX_ITEM_BY_STYLE[mbStyle]];
806	  if (mbKey === undefined) continue; // 6145/6146 无素材，上方单独注册
807	  const mbDef = ITEM_DEFS[byKey[mbKey]];
808	  if (!mbDef) continue;
809	  mbDef.tile = 'v_139_musicboxes';
810	  mbDef.placeStyle = mbStyle;
811	  mbDef.maxStack = 1;   // 原版唱片 maxStack 1（DefaultToMusicBox 非 stackable）
812	  mbDef.value = 100000; // DefaultToMusicBox value = 10 金
813	}
814	
815	// ---- 水喷泉全量 10 色（Item.cs createTile=207：909 纯净/910 沙漠 940-945 丛林·
816	// 冰雪·腐化·猩红·神圣·血月/4922 洞穴/4417 绿洲；placeStyle 0-9 =
817	// WorldGen.Check2xX :38199-38226 掉落表逆表）。放置帧 X 向 style*36（fw=2，
818	// FurnitureStyle default 分支即正确） ----
819	const FOUNTAIN_ITEM_STYLE: Array<[number, number]> = [
820	  [909, 0], [910, 1], [940, 2], [941, 3], [942, 4], [943, 5], [944, 6], [945, 7], [4922, 8], [4417, 9],
821	];
822	for (const [fnVid, fnStyle] of FOUNTAIN_ITEM_STYLE) {
823	  const fnKey = VANILLA_ITEM_KEY_BY_ID[fnVid];
824	  if (fnKey === undefined) continue;
825	  const fnDef = ITEM_DEFS[byKey[fnKey]];
826	  if (!fnDef) continue;
827	  fnDef.tile = 'v_207_water_fountains';
828	  fnDef.placeStyle = fnStyle;
829	  fnDef.maxStack = 99;
830	}
831	void 0;
832	
833	// ---- 宝石系统：gemcorn 4851-4857（Item.cs createTile=590 宝石树苗，style=宝石序号；
834	// 种在石/苔上必须地下长成宝石树，见 growSaplings）----
835	item({ key: 'vi_4851_GemTreeTopazSeed', name: '黄玉宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 0 });
836	item({ key: 'vi_4852_GemTreeAmethystSeed', name: '紫水晶宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 1 });
837	item({ key: 'vi_4853_GemTreeSapphireSeed', name: '蓝宝石宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 2 });
838	item({ key: 'vi_4854_GemTreeEmeraldSeed', name: '翡翠宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 3 });
839	item({ key: 'vi_4855_GemTreeRubySeed', name: '红宝石宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 4 });
840	item({ key: 'vi_4856_GemTreeDiamondSeed', name: '钻石宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 5 });
841	item({ key: 'vi_4857_GemTreeAmberSeed', name: '琥珀宝石橡实', maxStack: 999, value: 100, tile: 'v_590_gem_saplings', placeStyle: 6 });
842	
843	// ---- 阶段 6:功能道具(桶三态/绳圈) ----
844	item({ key: 'empty_bucket', name: '空桶', maxStack: 99, value: 1, desc: '右键舀取液体' });
845	item({ key: 'water_bucket', name: '水桶', maxStack: 1, value: 1, desc: '右键放置水' });
846	item({ key: 'lava_bucket', name: '岩浆桶', maxStack: 1, value: 1, desc: '右键放置岩浆' });
847	item({ key: 'honey_bucket', name: '蜂蜜桶', maxStack: 1, value: 1, desc: '右键放置蜂蜜' });
848	
849	// ---- 阶段 6 第三轮:替代矿工具链(官方数值,与铜/铁/银/金同档) ----
850	item({ key: 'tin_pickaxe', name: '锡镐', maxStack: 1, value: 400,
851	  tool: { type: 'pick', power: 35, damage: 4, speed: 23, knockback: 2, reach: 2.6 * 16 } });
852	item({ key: 'tin_axe', name: '锡斧', maxStack: 1, value: 350,
853	  tool: { type: 'axe', power: 7, damage: 3, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
854	item({ key: 'tin_sword', name: '锡剑', maxStack: 1, value: 450,
855	  tool: { type: 'sword', damage: 8, speed: 23, knockback: 5, reach: 2.2 * 16 } });
856	item({ key: 'lead_pickaxe', name: '铅镐', maxStack: 1, value: 900,
857	  tool: { type: 'pick', power: 45, damage: 5, speed: 22, knockback: 2.5, reach: 2.6 * 16 } });
858	item({ key: 'lead_axe', name: '铅斧', maxStack: 1, value: 800,
859	  tool: { type: 'axe', power: 9, damage: 4, speed: 30, knockback: 5, reach: 2.4 * 16 } });
860	item({ key: 'lead_sword', name: '铅剑', maxStack: 1, value: 900,
861	  tool: { type: 'sword', damage: 10, speed: 23, knockback: 5, reach: 2.2 * 16 } });
862	item({ key: 'tungsten_pickaxe', name: '钨镐', maxStack: 1, value: 1800,
863	  tool: { type: 'pick', power: 55, damage: 6, speed: 21, knockback: 2.5, reach: 2.6 * 16 } });
864	item({ key: 'tungsten_axe', name: '钨斧', maxStack: 1, value: 1600,
865	  tool: { type: 'axe', power: 11, damage: 5, speed: 29, knockback: 5.5, reach: 2.4 * 16 } });
866	item({ key: 'tungsten_sword', name: '钨剑', maxStack: 1, value: 1800,
867	  tool: { type: 'sword', damage: 13, speed: 22, knockback: 5.5, reach: 2.2 * 16 } });
868	item({ key: 'platinum_pickaxe', name: '铂金镐', maxStack: 1, value: 3600,
869	  tool: { type: 'pick', power: 59, damage: 7, speed: 20, knockback: 3, reach: 2.6 * 16 } });
870	item({ key: 'platinum_axe', name: '铂金斧', maxStack: 1, value: 3200,
871	  tool: { type: 'axe', power: 13, damage: 6, speed: 28, knockback: 6, reach: 2.4 * 16 } });
872	item({ key: 'platinum_sword', name: '铂金剑', maxStack: 1, value: 3600,
873	  tool: { type: 'sword', damage: 15, speed: 22, knockback: 6, reach: 2.2 * 16 } });
874	
875	// ---- 阶段 6 第五轮:弓箭系统(官方数值 Item.cs:2996-3010:木弓伤4/UseTime30/射速6.1/击退0) ----
876	item({ key: 'wooden_bow', name: '木弓', maxStack: 1, value: 100, vid: 39,
877	  ranged: { damage: 4, speed: 30, knockback: 0, ammo: 'wooden_arrow', projSpeed: 6.1, vid: 39 } });
878	item({ key: 'wooden_arrow', name: '木箭', maxStack: 999, value: 1, vid: 40, ammoId: 40 });
879	item({ key: 'flaming_arrow', name: '燃烧箭', maxStack: 999, value: 1, vid: 41, ammoId: 40 });
880	item({ key: 'iron_bow', name: '铁弓', maxStack: 1, value: 360, vid: 99,
881	  ranged: { damage: 8, speed: 28, knockback: 0, ammo: 'wooden_arrow', projSpeed: 6.6, vid: 99 } });
882	
883	// ---- 阶段 6 第六轮:矿车 ----
884	item({ key: 'minecart_item', name: '矿车', maxStack: 99, value: 1, desc: '右键轨道放置并骑乘' });
885	
886	// ---- 阶段 6 第八轮:魔法武器(官方 Item.cs:30765-30778,火花法杖=ItemID 3069:伤14/魔力2/UseTime26/射速7/暴击10) ----
887	item({ key: 'wand_of_sparking', name: '火花法杖', maxStack: 1, value: 100,
888	  magic: { damage: 14, speed: 26, manaCost: 2, projSpeed: 7, proj: 'spark' } });
889	item({ key: 'amethyst_bolt', name: '紫晶法杖', maxStack: 1, value: 900,
890	  magic: { damage: 14, speed: 26, manaCost: 5, projSpeed: 9, proj: 'bolt' } });
891	
892	// ---- 阶段 6 第九轮:Boss 召唤物(官方:蠕虫食物 70/血腥脊椎 1331/史莱姆王冠 560) ----
893	item({ key: 'worm_food', name: '蠕虫食物', maxStack: 20, value: 1, desc: '腐化之地使用:召唤世界吞噬者' });
894	// 入侵触发物品（Player.ItemCheck_UseEventItems，Player.cs:43243/43260/43277）
895	item({ key: 'goblin_battle_standard', name: '哥布林战旗', vid: 361, maxStack: 20, value: 1, desc: '任意时刻:召唤哥布林军队' });
896	item({ key: 'snow_globe', name: '雪球', vid: 602, maxStack: 20, value: 1, desc: '使用:召唤雪人军团' });
897	item({ key: 'pirate_map', name: '海盗地图', vid: 1301, maxStack: 20, value: 1, desc: '使用:召唤海盗入侵' });
898	item({ key: 'bloody_spine', name: '血腥脊椎', maxStack: 20, value: 1, desc: '猩红之地使用:召唤克苏鲁之脑' });
899	item({ key: 'slime_crown', name: '史莱姆王冠', maxStack: 20, value: 1, desc: '任意时刻:召唤史莱姆王' });
900	
901	// ---- 机械三王召唤物(官方 556 机械蠕虫/544 机械魔眼/557 机械骷髅头;需夜晚+困难模式) ----
902	item({ key: 'mechanical_worm', name: '机械蠕虫', maxStack: 20, value: 1, vid: 556, desc: '夜晚使用:召唤毁灭者' });
903	item({ key: 'mechanical_eye', name: '机械魔眼', maxStack: 20, value: 1, vid: 544, desc: '夜晚使用:召唤双子魔眼' });
904	item({ key: 'mechanical_skull', name: '机械骷髅头', maxStack: 20, value: 1, vid: 557, desc: '夜晚使用:召唤机械骷髅王' });
905	
906	// ---- 电路工具(原版 530 电线/509,850,851,3612 扳手/510 剪线钳/849 致动器/3620 致动魔杖/3625 五彩扳手/3611 宏伟蓝图) ----
907	// 位掩码见 world/Wiring.ts TOOL_*。扳手消耗背包中的 wire(原版语义:找第一组 530 扣 1)
908	item({ key: 'wire', name: '电线', maxStack: 999, value: 1, desc: '四色扳手与宏伟蓝图的耗材' });
909	item({ key: 'red_wrench', name: '红扳手', maxStack: 1, value: 1, wireTool: { place: 1 }, desc: '左键铺红线(消耗电线)' });
910	item({ key: 'blue_wrench', name: '蓝扳手', maxStack: 1, value: 1, wireTool: { place: 2 }, desc: '左键铺蓝线(消耗电线)' });
911	item({ key: 'green_wrench', name: '绿扳手', maxStack: 1, value: 1, wireTool: { place: 4 }, desc: '左键铺绿线(消耗电线)' });
912	item({ key: 'yellow_wrench', name: '黄扳手', maxStack: 1, value: 1, wireTool: { place: 8 }, desc: '左键铺黄线(消耗电线)' });
913	item({ key: 'wire_cutter', name: '钢丝钳', maxStack: 1, value: 1, wireTool: { cutter: true }, desc: '左键剪线(优先级:致动器>黄>绿>蓝>红)' });
914	item({ key: 'actuator_item', name: '致动器', maxStack: 999, value: 1, wireTool: { place: 16 }, desc: '左键给方块装致动器,通电缩入' });
915	item({ key: 'actuation_rod', name: '致动魔杖', maxStack: 1, value: 1, wireTool: { rod: true }, desc: '左键手动翻转方块致动状态' });
916	item({ key: 'multicolor_wrench', name: '五彩扳手', maxStack: 1, value: 1, wireTool: { place: 15, grand: false }, desc: 'R 键切换模式(四色/剪线/致动器),左键单点' });
917	item({ key: 'grand_design', name: '宏伟蓝图', maxStack: 1, value: 1, wireTool: { place: 15, grand: true }, desc: '拖拽批量铺线(R 键切换模式)' });
918	
919	
920	// ===================== 存档稳定 id(根治 ITEM_DEFS 数组下标漂移;存档 v3 起生效) =====================
921	// vi_* 稳定 id = 原版物品 id(key 内嵌);自造物品 = 私有段 10000+(下表,2026-08 冻结快照)。
922	// ★ PRIV_ITEM_STABLE 冻结表 append-only:新自造物品只许表尾追加,已分配号码永不复用/改派。
923	const PRIV_ITEM_STABLE: Record<string, number> = {
924	  'dirt_block': 10000, 'stone_block': 10001, 'wood': 10002, 'sand_block': 10003,
925	  'snow_block': 10004, 'platform': 10005, 'torch': 10006, 'door': 10007,
926	  'workbench': 10008, 'furnace': 10009, 'anvil': 10010, 'chest': 10011,
927	  'gel': 10012, 'acorn': 10013, 'mushroom_item': 10014, 'copper_ore': 10015,
928	  'iron_ore': 10016, 'silver_ore': 10017, 'gold_ore': 10018, 'copper_bar': 10019,
929	  'iron_bar': 10020, 'silver_bar': 10021, 'gold_bar': 10022, 'lens': 10023,
930	  'suspicious_eye': 10024, 'lesser_healing_potion': 10025, 'coin_copper': 10026, 'coin_silver': 10027,
931	  'coin_gold': 10028, 'heal_potion': 10029, 'agility_potion': 10030, 'ironskin_potion': 10031,
932	  'thorns_potion': 10032, 'regen_potion': 10033, 'lucky_horseshoe': 10034, 'feral_claws': 10035,
933	  'copper_helmet': 10036, 'copper_chainmail': 10037, 'copper_greaves': 10038, 'iron_helmet': 10039,
934	  'iron_chainmail': 10040, 'iron_greaves': 10041, 'silver_helmet': 10042, 'silver_chainmail': 10043,
935	  'silver_greaves': 10044, 'gold_helmet': 10045, 'gold_chainmail': 10046, 'gold_greaves': 10047,
936	  'wood_pickaxe': 10048, 'wood_axe': 10049, 'wood_sword': 10050, 'wood_hammer': 10051,
937	  'copper_pickaxe': 10052, 'copper_axe': 10053, 'copper_sword': 10054, 'copper_hammer': 10055,
938	  'iron_pickaxe': 10056, 'iron_axe': 10057, 'iron_sword': 10058, 'iron_hammer': 10059,
939	  'silver_pickaxe': 10060, 'silver_axe': 10061, 'silver_sword': 10062, 'silver_hammer': 10063,
940	  'gold_pickaxe': 10064, 'gold_axe': 10065, 'gold_sword': 10066, 'gold_hammer': 10067,
941	  'tin_ore': 10068, 'lead_ore': 10069, 'tungsten_ore': 10070, 'platinum_ore': 10071,
942	  'tin_bar': 10072, 'lead_bar': 10073, 'tungsten_bar': 10074, 'platinum_bar': 10075,
943	  'demonite_ore': 10076, 'meteorite': 10077, 'hellstone': 10078, 'crimtane_ore': 10079,
944	  'cobalt_ore': 10080, 'mythril_ore': 10081, 'adamantite_ore': 10082, 'palladium_ore': 10083,
945	  'orichalcum_ore': 10084, 'titanium_ore': 10085, 'chlorophyte_ore': 10086, 'sapphire': 10087,
946	  'ruby': 10088, 'emerald': 10089, 'topaz': 10090, 'amethyst': 10091,
947	  'diamond': 10092, 'ice_block': 10093, 'ice_brick': 10094, 'snow_brick': 10095,
948	  'sandstone_block': 10096, 'hardened_sand_block': 10097, 'desert_fossil': 10098, 'clay_block': 10099,
949	  'glass': 10100, 'obsidian': 10101, 'gray_brick': 10102, 'red_brick': 10103,
950	  'mud_block': 10104, 'silt_block': 10105, 'table': 10106, 'chair': 10107,
951	  'bed': 10108, 'bookcase': 10109, 'grandfather_clock': 10110, 'piano': 10111,
952	  'dresser': 10112, 'bench': 10113, 'bathtub': 10114, 'keg': 10115,
953	  'cooking_pot': 10116, 'clay_pot': 10117, 'tombstone': 10118, 'life_crystal': 10119,
954	  'candle': 10120, 'chandelier': 10121, 'lantern': 10122, 'candelabra': 10123,
955	  'chinese_lantern': 10124, 'skull_lantern': 10125, 'water_candle': 10126, 'bomb': 10127,
956	  'rope': 10128, 'place_v_29_piggy_bank': 10129, 'place_v_463_defenders_forge': 10130, 'place_v_51_cobweb': 10131,
957	  'place_v_368_granite_block': 10132, 'place_v_226_lihzahrd_brick': 10133, 'place_v_367_marble_block': 10134, 'place_v_633_ash_grass_block': 10135,
958	  'place_v_181_red_moss_block': 10136, 'place_v_189_cloud_block': 10137, 'place_v_183_purple_moss_block': 10138, 'place_v_536_xenon_moss_block': 10139,
959	  'place_v_225_hive_block': 10140, 'place_v_483_cracked_pink_brick': 10141, 'place_v_224_slush_block': 10142, 'place_v_383_living_mahogany_block': 10143,
960	  'place_v_179_green_moss_block': 10144, 'place_v_384_living_mahogany_leaves_block': 10145, 'place_v_273_stone_slab': 10146, 'place_v_381_lava_moss': 10147,
961	  'place_v_48_spike': 10148, 'place_v_192_living_leaf_block': 10149, 'place_v_191_living_wood_block': 10150, 'place_v_196_rain_cloud_block': 10151,
962	  'place_v_118_pearlstone_brick': 10152, 'place_v_321_boreal_wood': 10153, 'place_v_152_ebonstone_brick': 10154, 'place_v_158_rich_mahogany': 10155,
963	  'place_v_357_smooth_marble_block': 10156, 'place_v_272_cog_block': 10157, 'place_v_229_honey_block': 10158, 'place_v_311_dynasty_wood': 10159,
964	  'place_v_130_active_stone_block': 10160, 'place_v_193_slime_block': 10161, 'place_v_190_glowing_mushroom_block': 10162, 'place_v_350_martian_conduit_plating': 10163,
965	  'place_v_369_smooth_granite_block': 10164, 'place_v_137_traps': 10165, 'place_v_117_pearlstone_block': 10166, 'place_v_112_ebonsand_block': 10167,
966	  'place_v_232_wooden_spike': 10168, 'place_v_274_sandstone_slab': 10169, 'place_v_322_palm_wood': 10170, 'place_v_109_hallowed_grass_block': 10171,
967	  'place_v_312_red_dynasty_shingles': 10172, 'place_v_422_conveyor_belt_ccw': 10173, 'place_v_495_shell_pile_block': 10174, 'place_v_479_smooth_sandstone_block': 10175,
968	  'place_v_353_vine_rope': 10176, 'place_v_477_mowed_grass_block': 10177, 'place_v_380_planter_boxes': 10178, 'place_v_230_crispy_honey_block': 10179,
969	  'place_v_562_bamboo_block': 10180, 'place_v_371_pink_slime_block': 10181, 'place_v_668_the_dirtiest_block': 10182, 'place_v_398_corrupt_hardened_sand_block': 10183,
970	  'place_v_379_bubble': 10184, 'place_v_618_stone_accent_slab': 10185, 'place_v_165_cave_decos': 10186, 'place_v_184_moss_plants': 10187,
971	  'place_v_314_minecart_track': 10188, 'place_v_185_small_decos': 10189, 'place_v_373_water_drip': 10190, 'place_v_187_decos_3x2_group_2': 10191,
972	  'place_v_484_rolling_cactus': 10192, 'place_v_374_lava_drip': 10193, 'place_v_233_jungle_large_plants': 10194, 'place_v_105_statue': 10195,
973	  'place_v_186_decos_3x2': 10196, 'place_v_461_sand_drip': 10197, 'place_v_178_gems': 10198, 'place_v_485_antlion_larva': 10199,
974	  'place_v_637_ash_short_plants': 10200, 'place_v_444_bee_hive': 10201, 'place_v_240_wall_hangings_3x3': 10202, 'place_v_519_cattails': 10203,
975	  'place_v_138_boulder': 10204, 'place_v_634_ash_tree': 10205, 'place_v_26_altars': 10206, 'place_v_82_herbs_sprout': 10207,
976	  'place_v_323_palm_trees': 10208, 'place_v_135_pressure_plates': 10209, 'place_v_91_banners': 10210, 'place_v_242_paintings_6x4': 10211,
977	  'place_v_50_books': 10212, 'place_v_93_lamps': 10213, 'place_v_549_seaweed': 10214, 'place_v_254_pumpkin_plant': 10215,
978	  'place_v_571_bamboo': 10216, 'place_v_246_paintings_3x2': 10217, 'place_v_245_paintings_2x3': 10218, 'place_v_586_emerald_tree': 10219,
979	  'place_v_596_vanity_tree_sakura': 10220, 'place_v_467_chests_group_2': 10221, 'place_v_443_geyser': 10222, 'place_v_589_amber_tree': 10223,
980	  'place_v_411_detonator': 10224, 'place_v_518_lily_pads': 10225, 'place_v_588_diamond_tree': 10226, 'place_v_585_sapphire_tree': 10227,
981	  'place_v_583_topaz_tree': 10228, 'place_v_13_placed_bottles': 10229, 'place_v_530_oasis_plants': 10230, 'place_v_616_vanity_tree_yellow_willow': 10231,
982	  'place_v_215_campfires': 10232, 'place_v_141_explosives': 10233, 'place_v_597_pylons': 10234, 'place_v_592_hanging_brazier': 10235,
983	  'place_v_375_honey_drip': 10236, 'place_v_227_dye_plants': 10237, 'place_v_584_amethyst_tree': 10238, 'place_v_231_larva': 10239,
984	  'place_v_395_item_frame': 10240, 'place_v_241_catacombs': 10241, 'place_v_587_ruby_tree': 10242, 'place_v_86_loom': 10243,
985	  'place_v_376_fishing_crates': 10244, 'place_v_470_mannequins': 10245, 'place_v_324_seashells': 10246, 'place_v_81_coral': 10247,
986	  'place_v_136_switch': 10248, 'place_v_355_alchemy_table': 10249, 'place_v_354_bewitching_table': 10250, 'place_v_103_bowls': 10251,
987	  'place_v_529_sea_oats': 10252, 'place_v_506_bast_statue': 10253, 'place_v_349_mushroom_statue': 10254, 'place_v_377_sharpening_station': 10255,
988	  'place_v_613_potted_lava_plants': 10256, 'place_v_219_extractinator': 10257, 'place_v_388_tall_gate_closed': 10258, 'place_v_389_tall_gate_open': 10259,
989	  'place_v_129_crystal_shard': 10260, 'place_v_466_elder_cystal_stand': 10261, 'place_v_220_solidifier': 10262, 'place_v_303_lihzahrd_furnace': 10263,
990	  'place_v_469_tables_group_2': 10264, 'place_v_304_living_loom': 10265, 'place_v_488_fallen_log': 10266, 'place_v_548_potted_trees_group_2': 10267,
991	  'place_v_614_potted_ember_tendrils': 10268, 'place_v_598_lava_serpent_bowl': 10269, 'place_v_406_chimney': 10270, 'place_v_305_sky_mill': 10271,
992	  'place_v_300_bone_welder': 10272, 'place_v_302_glass_kiln': 10273, 'place_v_306_ice_machine': 10274, 'place_v_247_autohammer': 10275,
993	  'place_v_491_void_vault': 10276, 'place_v_106_sawmill': 10277, 'place_v_642_chlorophyte_extractinator': 10278, 'place_v_319_ship_in_a_bottle': 10279,
994	  'place_v_487_picnic_tables': 10280, 'place_v_97_safe': 10281, 'place_v_320_seaweed_planter': 10282, 'place_v_405_fireplace': 10283,
995	  'place_v_378_target_dummy': 10284, 'place_v_218_meat_grinder': 10285, 'place_v_356_enchanted_sundial': 10286, 'place_v_114_tinkerer_s_workshop': 10287,
996	  'place_v_237_lihzahrd_altar': 10288, 'place_v_110_hallow_short_plants': 10289, 'place_v_621_slice_of_cake': 10290, 'place_v_387_trap_door_closed': 10291,
997	  'place_v_316_blue_jellyfish_jar': 10292, 'place_v_125_crystal_ball': 10293, 'place_v_287_ammo_box': 10294, 'place_v_294_zebra_swallowtail_butterfly_jar': 10295,
998	  'place_v_291_ulysses_butterfly_jar': 10296, 'place_v_292_sulphur_butterfly_jar': 10297, 'place_v_289_purple_emperor_butterfly_jar': 10298, 'place_v_172_sinks': 10299,
999	  'place_v_656_glow_tulip': 10300, 'place_v_113_hallow_tall_plants': 10301, 'place_v_235_teleporter': 10302, 'place_v_567_garden_gnome': 10303,
1000	  'place_v_638_ash_vines': 10304, 'place_v_528_mushroom_vines': 10305, 'place_v_382_flower_vines': 10306, 'place_v_124_wooden_beam': 10307,
1001	  'place_v_575_rich_mahogany_beam': 10308, 'place_v_213_rope': 10309, 'place_v_636_corrupt_vines': 10310, 'place_v_574_boreal_beam': 10311,
1002	  'place_v_333_platinum_coin_pile': 10312, 'place_v_332_gold_coin_pile': 10313, 'place_v_577_sandstone_column': 10314, 'place_v_561_marble_column': 10315,
1003	  'place_v_576_granite_column': 10316, 'place_v_214_chain': 10317, 'place_v_578_mushroom_beam': 10318, 'place_v_52_vines': 10319,
1004	  'place_v_62_jungle_vines': 10320, 'place_v_69_jungle_thorns': 10321, 'place_v_625_neon_moss_block': 10322, 'place_v_151_sandstone_brick': 10323,
1005	  'place_v_234_crimsand_block': 10324, 'place_v_182_blue_moss_block': 10325, 'place_v_205_crimson_vines': 10326, 'place_v_45_gold_brick': 10327,
1006	  'place_v_399_crimson_hardened_sand_block': 10328, 'place_v_352_crimtane_thorns': 10329, 'place_v_248_palladium_column': 10330, 'place_v_340_living_cursed_fire_block': 10331,
1007	  'place_v_207_water_fountains': 10332, 'place_v_144_timers': 10333, 'place_v_475_hat_rack': 10334, 'place_v_175_tin_brick': 10335,
1008	  'place_v_132_lever': 10336, 'place_v_539_argon_moss_block': 10337, 'place_v_481_cracked_blue_brick': 10338, 'place_v_120_mudstone_brick': 10339,
1009	  'place_v_714_spider_boulder': 10340, 'place_v_752_chillet_egg': 10341, 'place_v_751_sleeping_digtoise': 10342, 'place_v_664_bouncy_boulder': 10343,
1010	  'place_v_711_rainbow_boulder': 10344, 'place_v_715_ghoulder': 10345, 'place_v_716_friendly_boulder': 10346, 'place_v_713_lava_boulder': 10347,
1011	  'place_v_23_corrupt_grass_block': 10348, 'place_v_31_orb_heart': 10349, 'place_v_41_blue_brick': 10350, 'place_v_75_obsidian_brick': 10351,
1012	  'place_v_199_crimson_grass_block': 10352, 'place_v_60_jungle_grass_block': 10353, 'place_v_70_mushroom_grass_block': 10354, 'place_v_25_ebonstone_block': 10355,
1013	  'place_v_202_sunplate_block': 10356, 'place_v_71_mushroom_plant': 10357, 'place_v_24_corruption_short_plants': 10358, 'place_v_32_corruption_thorns': 10359,
1014	  'place_v_27_sunflower': 10360, 'place_v_5_trees': 10361, 'place_v_80_cactus': 10362, 'place_v_3_forest_short_plants': 10363,
1015	  'place_v_73_forest_tall_plants': 10364, 'place_v_61_jungle_short_plants': 10365, 'place_v_74_jungle_tall_plants': 10366, 'place_v_83_herbs_mature': 10367,
1016	  'place_v_84_herbs_bloom': 10368, 'place_v_72_mushroom_tree': 10369, 'place_v_43_green_brick': 10370, 'place_v_44_pink_brick': 10371,
1017	  'place_v_203_crimstone_block': 10372, 'place_v_201_crimson_short_plants': 10373, 'place_v_35_jackolanterns': 10374, 'place_v_92_lampposts': 10375,
1018	  'place_v_126_discoball': 10376, 'place_v_131_inactivestoneblock': 10377, 'place_v_139_musicboxes': 10378, 'place_v_142_inletpump': 10379,
1019	  'place_v_143_outletpump': 10380, 'place_v_149_holidaylights': 10381, 'place_v_173_platinumcandelabra': 10382, 'place_v_174_platinumcandle': 10383,
1020	  'place_v_209_cannon': 10384, 'place_v_210_landmine': 10385, 'place_v_212_snowballlauncher': 10386, 'place_v_216_firework': 10387,
1021	  'place_v_244_bubblemachine': 10388, 'place_v_255_amethystgemsparkoff': 10389, 'place_v_256_topazgemsparkoff': 10390, 'place_v_257_sapphiregemsparkoff': 10391,
1022	  'place_v_258_emeraldgemsparkoff': 10392, 'place_v_259_rubygemsparkoff': 10393, 'place_v_260_diamondgemsparkoff': 10394, 'place_v_261_ambergemsparkoff': 10395,
1023	  'place_v_262_amethystgemspark': 10396, 'place_v_263_topazgemspark': 10397, 'place_v_264_sapphiregemspark': 10398, 'place_v_265_emeraldgemspark': 10399,
1024	  'place_v_266_rubygemspark': 10400, 'place_v_267_diamondgemspark': 10401, 'place_v_268_ambergemspark': 10402, 'place_v_335_fireworksbox': 10403,
1025	  'place_v_338_fireworkfountain': 10404, 'place_v_372_peacecandle': 10405, 'place_v_386_trapdooropen': 10406, 'place_v_389_tallgateopen': 10407,
1026	  'place_v_410_lunarmonolith': 10408, 'place_v_419_logicgatelamp': 10409, 'place_v_420_logicgate': 10410, 'place_v_421_conveyorbeltleft': 10411,
1027	  'place_v_423_logicsensor': 10412, 'place_v_424_wirepipe': 10413, 'place_v_425_announcementbox': 10414, 'place_v_428_weightedpressureplate': 10415,
1028	  'place_v_429_wirebulb': 10416, 'place_v_440_gemlocks': 10417, 'place_v_441_fakecontainers': 10418, 'place_v_442_projectilepressurepad': 10419,
1029	  'place_v_445_pixelbox': 10420, 'place_v_452_sillyballoonmachine': 10421, 'place_v_455_partymonolith': 10422, 'place_v_468_fakecontainers2': 10423,
1030	  'place_v_476_golfhole': 10424, 'place_v_480_bloodmoonmonolith': 10425, 'place_v_497_toilets': 10426, 'place_v_509_voidmonolith': 10427,
1031	  'place_v_531_boulderstatue': 10428, 'place_v_546_grate': 10429, 'place_v_557_grateclosed': 10430, 'place_v_564_plasmalamp': 10431,
1032	  'place_v_565_fogmachine': 10432, 'place_v_593_volcanosmall': 10433, 'place_v_594_volcanolarge': 10434, 'place_v_482_cracked_green_brick': 10435,
1033	  'place_v_163_purple_ice_block': 10436, 'place_v_200_red_ice_block': 10437, 'place_v_116_pearlsand_block': 10438, 'place_v_76_hellstone_brick': 10439,
1034	  'place_v_77_hellforge': 10440, 'place_v_55_signs': 10441, 'place_v_301_flesh_cloning_vat': 10442, 'place_v_307_steampunk_boiler': 10443,
1035	  'place_v_308_honey_dispenser': 10444, 'place_v_499_decay_chamber': 10445, 'corrupt_grass_seeds': 10446, 'crimson_grass_seeds': 10447,
1036	  'jungle_grass_seeds': 10448, 'mushroom_grass_seeds': 10449, 'empty_bucket': 10450, 'water_bucket': 10451,
1037	  'lava_bucket': 10452, 'honey_bucket': 10453, 'tin_pickaxe': 10454, 'tin_axe': 10455,
1038	  'tin_sword': 10456, 'lead_pickaxe': 10457, 'lead_axe': 10458, 'lead_sword': 10459,
1039	  'tungsten_pickaxe': 10460, 'tungsten_axe': 10461, 'tungsten_sword': 10462, 'platinum_pickaxe': 10463,
1040	  'platinum_axe': 10464, 'platinum_sword': 10465, 'wooden_bow': 10466, 'wooden_arrow': 10467,
1041	  'flaming_arrow': 10468, 'iron_bow': 10469, 'minecart_item': 10470, 'wand_of_sparking': 10471,
1042	  'amethyst_bolt': 10472, 'worm_food': 10473, 'bloody_spine': 10474, 'slime_crown': 10475,
1043	  'mechanical_worm': 10476, 'mechanical_eye': 10477, 'mechanical_skull': 10478, 'wire': 10479,
1044	  'red_wrench': 10480, 'blue_wrench': 10481, 'green_wrench': 10482, 'yellow_wrench': 10483,
1045	  'wire_cutter': 10484, 'actuator_item': 10485, 'actuation_rod': 10486, 'multicolor_wrench': 10487,
1046	  'grand_design': 10488,
1047	  'goblin_battle_standard': 10489, 'snow_globe': 10490, 'pirate_map': 10491,
1048	  'coin_platinum': 10492,
1049	  'place_v_119_iridescent_brick': 10493,
1050	  'obsidian_skin_potion': 10494, 'gills_potion': 10495, 'mana_regen_potion': 10496,
1051	  'magic_power_potion': 10497, 'featherfall_potion': 10498, 'water_walking_potion': 10499,
1052	  'archery_potion': 10500,
1053	  'night_owl_potion': 10501,
1054	};
1055	
1056	// ---- 墙面物品全量（vanilla-wallitems.json = Item.cs createWall 提取，124 项）：
1057	// 已注册的 vi_ 墙物品补 wallId；缺的按 vi_ 命名注册（稳定 id = 物品 id 自动派生）
1058	import wallItemsJson from './vanilla-wallitems.json';
1059	for (const wi of Object.values(wallItemsJson as Record<string, { wall: number; key: string }>)) {
1060	  const existing = byKey[wi.key];
1061	  if (existing !== undefined) { ITEM_DEFS[existing].wallId = wi.wall; continue; }
1062	  item({ key: wi.key, name: '', maxStack: 999, value: 1, wallId: wi.wall });
1063	}
1064	/** internal id → 稳定 id(保存方向;0=无映射,不应出现) */
1065	export const ITEM_STABLE_OF_INTERNAL = new Uint16Array(ITEM_DEFS.length);
1066	/** 稳定 id → internal id(加载方向;同 vid 重复注册时归一到首个 def——内容等价) */
1067	export const ITEM_INTERNAL_OF_STABLE = new Map<number, number>();
1068	for (let i = 0; i < ITEM_DEFS.length; i++) {
1069	  const k = ITEM_DEFS[i].key;
1070	  const vm = /^vi_(\d+)_/.exec(k);
1071	  // place_v_N_* 未在 PRIV 表登记时按 sheet 派生 20000+N(确定性,与表内显式号不冲突:
1072	  // 表尾已到 10500,20000+ 区段独占)——新注册 tile 的放置物不再逐个补表
1073	  const pm = !vm ? /^place_v_(\d+)_/.exec(k) : null;
1074	  const s = vm ? Number(vm[1]) : PRIV_ITEM_STABLE[k] ?? (pm ? 20000 + Number(pm[1]) : undefined);
1075	  if (s === undefined) { console.error(`[stable-id] item 缺稳定 id: ${k}`); continue; }
1076	  ITEM_STABLE_OF_INTERNAL[i] = s;
1077	  if (!ITEM_INTERNAL_OF_STABLE.has(s)) ITEM_INTERNAL_OF_STABLE.set(s, i);
1078	}
1079	// ---- 原版工具力表补齐(Item.cs SetDefaults 提取)→ vi_ 道具 tool 元数据 ----
1080	// 条件破坏链的道具入口:圣锤 80 砸祭坛/邪恶石 65 需梦魇镐/神庙砖 210 需 Picksaw 级等
1081	const VANILLA_TOOL_POWERS: Record<number, { pick?: number; hammer?: number; axe?: number }> = JSON.parse("{\"103\":{\"pick\":65},\"104\":{\"hammer\":55},\"122\":{\"pick\":100},\"204\":{\"hammer\":60,\"axe\":60},\"217\":{\"hammer\":70,\"axe\":70},\"367\":{\"hammer\":80},\"579\":{\"pick\":200,\"axe\":70},\"654\":{\"hammer\":40},\"657\":{\"hammer\":35},\"660\":{\"hammer\":55},\"776\":{\"pick\":110},\"777\":{\"pick\":150},\"778\":{\"pick\":180},\"787\":{\"hammer\":85},\"797\":{\"hammer\":55},\"798\":{\"pick\":70},\"922\":{\"hammer\":40},\"990\":{\"pick\":200,\"axe\":70},\"1188\":{\"pick\":130},\"1195\":{\"pick\":165},\"1202\":{\"pick\":190},\"1234\":{\"hammer\":90},\"1262\":{\"hammer\":90},\"1305\":{\"hammer\":100,\"axe\":70},\"1506\":{\"pick\":200},\"1507\":{\"hammer\":90,\"axe\":70},\"3481\":{\"hammer\":59},\"3487\":{\"hammer\":50},\"3493\":{\"hammer\":43},\"3499\":{\"hammer\":38},\"3505\":{\"hammer\":35},\"3511\":{\"hammer\":45},\"3517\":{\"hammer\":55},\"3525\":{\"hammer\":100,\"axe\":70},\"4317\":{\"hammer\":80}}");
1082	for (const [idS, tp] of Object.entries(VANILLA_TOOL_POWERS)) {
1083	  const key = VANILLA_ITEM_KEY_BY_ID[Number(idS)];
1084	  if (!key) continue;
1085	  const def = ITEM_DEFS[ITEM_BY_KEY[key]];
1086	  if (!def) continue;
1087	  const type = tp.pick !== undefined ? 'pick' : 'hammer';
1088	  def.tool = { type: type as ToolType, power: tp.pick ?? tp.hammer ?? 0 };
1089	  if (tp.axe !== undefined) def.axePower = tp.axe;
1090	}
1091	

```


---

## 🤖 Assistant · 2026-08-12T15:52:11.848Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the items.ts structure. Local keys are the non-vi_ prefixed ones. The PRIV_ITEM_STABLE table has all local keys.

Let me now read recipes.ts and then grep for hardcoded key references. First read recipes.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:11.856Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/recipes.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:11.861Z

**📎 ToolResult**

```
1	// 配方表。station: 'hand' | 'workbench' | 'furnace' | 'anvil'
2	export type Station = 'hand' | 'workbench' | 'furnace' | 'anvil';
3	
4	export interface Recipe {
5	  out: string;          // 产物 item key
6	  count: number;
7	  station: Station;
8	  inputs: Array<[string, number]>; // [itemKey, 数量]
9	}
10	
11	export const RECIPES: Recipe[] = [
12	  { out: 'workbench', count: 1, station: 'hand', inputs: [['wood', 10]] },
13	  { out: 'torch', count: 3, station: 'hand', inputs: [['wood', 1], ['gel', 1]] },
14	  { out: 'platform', count: 2, station: 'workbench', inputs: [['wood', 1]] },
15	  { out: 'door', count: 1, station: 'workbench', inputs: [['wood', 6]] },
16	  { out: 'chest', count: 1, station: 'workbench', inputs: [['wood', 8], ['iron_bar', 2]] },
17	  { out: 'furnace', count: 1, station: 'workbench', inputs: [['stone_block', 20], ['wood', 4], ['torch', 3]] },
18	  { out: 'wood_pickaxe', count: 1, station: 'workbench', inputs: [['wood', 12]] },
19	  { out: 'wood_axe', count: 1, station: 'workbench', inputs: [['wood', 9]] },
20	  { out: 'wood_sword', count: 1, station: 'workbench', inputs: [['wood', 7]] },
21	  { out: 'wood_hammer', count: 1, station: 'workbench', inputs: [['wood', 8]] },
22	  // 熔炼
23	  { out: 'copper_bar', count: 1, station: 'furnace', inputs: [['copper_ore', 3]] },
24	  { out: 'iron_bar', count: 1, station: 'furnace', inputs: [['iron_ore', 3]] },
25	  { out: 'silver_bar', count: 1, station: 'furnace', inputs: [['silver_ore', 4]] },
26	  { out: 'gold_bar', count: 1, station: 'furnace', inputs: [['gold_ore', 4]] },
27	  { out: 'anvil', count: 1, station: 'workbench', inputs: [['iron_bar', 5]] },
28	  // 金属工具链
29	  { out: 'copper_pickaxe', count: 1, station: 'anvil', inputs: [['copper_bar', 8], ['wood', 3]] },
30	  { out: 'copper_axe', count: 1, station: 'anvil', inputs: [['copper_bar', 6], ['wood', 3]] },
31	  { out: 'copper_sword', count: 1, station: 'anvil', inputs: [['copper_bar', 7]] },
32	  { out: 'iron_pickaxe', count: 1, station: 'anvil', inputs: [['iron_bar', 8], ['wood', 3]] },
33	  { out: 'iron_axe', count: 1, station: 'anvil', inputs: [['iron_bar', 6], ['wood', 3]] },
34	  { out: 'iron_sword', count: 1, station: 'anvil', inputs: [['iron_bar', 7]] },
35	  { out: 'iron_hammer', count: 1, station: 'anvil', inputs: [['iron_bar', 6], ['wood', 3]] },
36	  { out: 'silver_pickaxe', count: 1, station: 'anvil', inputs: [['silver_bar', 8], ['wood', 3]] },
37	  { out: 'silver_sword', count: 1, station: 'anvil', inputs: [['silver_bar', 7]] },
38	  { out: 'gold_pickaxe', count: 1, station: 'anvil', inputs: [['gold_bar', 8], ['wood', 3]] },
39	  { out: 'gold_sword', count: 1, station: 'anvil', inputs: [['gold_bar', 7]] },
40	  // 盔甲（铁砧）
41	  { out: 'copper_helmet', count: 1, station: 'anvil', inputs: [['copper_bar', 15]] },
42	  { out: 'copper_chainmail', count: 1, station: 'anvil', inputs: [['copper_bar', 20]] },
43	  { out: 'copper_greaves', count: 1, station: 'anvil', inputs: [['copper_bar', 15]] },
44	  { out: 'iron_helmet', count: 1, station: 'anvil', inputs: [['iron_bar', 20]] },
45	  { out: 'iron_chainmail', count: 1, station: 'anvil', inputs: [['iron_bar', 25]] },
46	  { out: 'iron_greaves', count: 1, station: 'anvil', inputs: [['iron_bar', 20]] },
47	  { out: 'silver_helmet', count: 1, station: 'anvil', inputs: [['silver_bar', 15]] },
48	  { out: 'silver_chainmail', count: 1, station: 'anvil', inputs: [['silver_bar', 20]] },
49	  { out: 'silver_greaves', count: 1, station: 'anvil', inputs: [['silver_bar', 15]] },
50	  { out: 'gold_helmet', count: 1, station: 'anvil', inputs: [['gold_bar', 10]] },
51	  { out: 'gold_chainmail', count: 1, station: 'anvil', inputs: [['gold_bar', 15]] },
52	  { out: 'gold_greaves', count: 1, station: 'anvil', inputs: [['gold_bar', 10]] },
53	  // 杂项
54	  { out: 'suspicious_eye', count: 1, station: 'workbench', inputs: [['lens', 6]] },
55	  { out: 'lesser_healing_potion', count: 1, station: 'workbench', inputs: [['gel', 2], ['mushroom_item', 1]] },
56	  // 药水链（移植自 Maples 合成表 + 扩展）
57	  { out: 'heal_potion', count: 1, station: 'workbench', inputs: [['lesser_healing_potion', 2], ['gel', 1]] },
58	  { out: 'regen_potion', count: 1, station: 'workbench', inputs: [['gel', 2], ['mushroom_item', 2]] },
59	  { out: 'agility_potion', count: 1, station: 'workbench', inputs: [['mushroom_item', 1], ['iron_bar', 1]] },
60	  { out: 'ironskin_potion', count: 1, station: 'workbench', inputs: [['stone_block', 5], ['iron_bar', 1]] },
61	  { out: 'thorns_potion', count: 1, station: 'workbench', inputs: [['wood', 5], ['lens', 1]] },
62	  // ---- 原版素材批次：方块 / 家具 / 熔炼 ----
63	  // 替代矿熔炼（钨/铂已在上文"熔炼"段,勿重复登记）
64	  { out: 'tin_bar', count: 1, station: 'furnace', inputs: [['tin_ore', 3]] },
65	  { out: 'lead_bar', count: 1, station: 'furnace', inputs: [['lead_ore', 3]] },
66	  // 方块加工
67	  { out: 'glass', count: 1, station: 'furnace', inputs: [['sand_block', 2]] },
68	  { out: 'gray_brick', count: 2, station: 'furnace', inputs: [['stone_block', 2]] },
69	  { out: 'red_brick', count: 2, station: 'furnace', inputs: [['clay_block', 2]] },
70	  { out: 'sandstone_block', count: 1, station: 'furnace', inputs: [['sand_block', 4]] },
71	  { out: 'ice_brick', count: 1, station: 'furnace', inputs: [['ice_block', 1]] },
72	  { out: 'snow_brick', count: 1, station: 'furnace', inputs: [['snow_block', 1]] },
73	  // 家具
74	  { out: 'table', count: 1, station: 'workbench', inputs: [['wood', 8]] },
75	  { out: 'chair', count: 1, station: 'workbench', inputs: [['wood', 4]] },
76	  { out: 'bed', count: 1, station: 'workbench', inputs: [['wood', 15]] },
77	  { out: 'bookcase', count: 1, station: 'workbench', inputs: [['wood', 20]] },
78	  { out: 'grandfather_clock', count: 1, station: 'workbench', inputs: [['wood', 10], ['iron_bar', 3]] },
79	  { out: 'piano', count: 1, station: 'workbench', inputs: [['wood', 15], ['iron_bar', 2]] },
80	  { out: 'dresser', count: 1, station: 'workbench', inputs: [['wood', 12]] },
81	  { out: 'bench', count: 1, station: 'workbench', inputs: [['wood', 8]] },
82	  { out: 'bathtub', count: 1, station: 'workbench', inputs: [['clay_block', 6]] },
83	  { out: 'keg', count: 1, station: 'workbench', inputs: [['wood', 14]] },
84	  { out: 'cooking_pot', count: 1, station: 'workbench', inputs: [['iron_bar', 2], ['wood', 4]] },
85	  { out: 'clay_pot', count: 1, station: 'workbench', inputs: [['clay_block', 5]] },
86	  { out: 'tombstone', count: 1, station: 'workbench', inputs: [['stone_block', 5]] },
87	  // 灯具
88	  { out: 'candle', count: 4, station: 'workbench', inputs: [['torch', 1], ['gel', 1]] },
89	  { out: 'chandelier', count: 1, station: 'anvil', inputs: [['torch', 4], ['iron_bar', 3]] },
90	  { out: 'lantern', count: 1, station: 'anvil', inputs: [['torch', 1], ['iron_bar', 1]] },
91	  { out: 'candelabra', count: 1, station: 'anvil', inputs: [['torch', 3], ['iron_bar', 1]] },
92	  { out: 'chinese_lantern', count: 1, station: 'workbench', inputs: [['torch', 1], ['wood', 3]] },
93	  { out: 'skull_lantern', count: 1, station: 'anvil', inputs: [['torch', 2], ['iron_bar', 1]] },
94	
95	// ---- 阶段 6:替代矿熔炼与工具链(与主矿同档配方) ----
96	  { out: 'tungsten_bar', count: 1, station: 'furnace', inputs: [['tungsten_ore', 4]] },
97	  { out: 'platinum_bar', count: 1, station: 'furnace', inputs: [['platinum_ore', 4]] },
98	  { out: 'tin_pickaxe', count: 1, station: 'anvil', inputs: [['tin_bar', 8], ['wood', 3]] },
99	  { out: 'tin_axe', count: 1, station: 'anvil', inputs: [['tin_bar', 6], ['wood', 3]] },
100	  { out: 'tin_sword', count: 1, station: 'anvil', inputs: [['tin_bar', 7]] },
101	  { out: 'lead_pickaxe', count: 1, station: 'anvil', inputs: [['lead_bar', 8], ['wood', 3]] },
102	  { out: 'lead_axe', count: 1, station: 'anvil', inputs: [['lead_bar', 6], ['wood', 3]] },
103	  { out: 'lead_sword', count: 1, station: 'anvil', inputs: [['lead_bar', 7]] },
104	  { out: 'tungsten_pickaxe', count: 1, station: 'anvil', inputs: [['tungsten_bar', 8], ['wood', 3]] },
105	  { out: 'tungsten_axe', count: 1, station: 'anvil', inputs: [['tungsten_bar', 6], ['wood', 3]] },
106	  { out: 'tungsten_sword', count: 1, station: 'anvil', inputs: [['tungsten_bar', 7]] },
107	  { out: 'platinum_pickaxe', count: 1, station: 'anvil', inputs: [['platinum_bar', 8], ['wood', 3]] },
108	  { out: 'platinum_axe', count: 1, station: 'anvil', inputs: [['platinum_bar', 6], ['wood', 3]] },
109	  { out: 'platinum_sword', count: 1, station: 'anvil', inputs: [['platinum_bar', 7]] },
110	  // 注：vi_ 产物（木墙 93/石墙 26/魔力水晶 109 等）一律走原版配方段
111	  // （vanilla-recipes.json），本表禁登——防双显。魔力水晶原版为徒手
112	  // 坠星×5（曾误写 ×3）。
113	];
114	

```


---

## 🤖 Assistant · 2026-08-12T15:52:12.326Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"RECIPES\" src tests tools --include=\"*.ts\" | grep -v \"vanilla-recipes.json\" | head -60",
 "description": "Find RECIPES consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:12.378Z

**📎 ToolResult**

```
src/ui/UI.ts:6:import { RECIPES } from '../data/recipes';
src/ui/UI.ts:7:import { vanillaItemKey, ingredientKey, VANILLA_RECIPES, RECIPE_GROUP_ITEMS, invIndexOfVanilla, type VanillaRecipeLike } from '../data/vanillaRecipes';
src/ui/UI.ts:1401:    for (const r of VANILLA_RECIPES) {
src/ui/UI.ts:2133:    for (const r of RECIPES) {
src/core/Game.ts:85:import { RECIPES } from '../data/recipes';
src/core/Game.ts:9678:  canCraft(r: (typeof RECIPES)[number]): boolean {
src/core/Game.ts:9683:  craft(r: (typeof RECIPES)[number]) {
src/data/recipes.ts:11:export const RECIPES: Recipe[] = [
src/data/vanillaRecipes.ts:27:export const VANILLA_RECIPES = DOC.recipes;
src/data/vanillaRecipes.ts:168:  for (const r of VANILLA_RECIPES) {
src/data/vanillaRecipes.ts:234:  for (const r of VANILLA_RECIPES) for (const req of r.items) s.add(req.id);
tests/vanilla-recipes.test.ts:4:  VANILLA_RECIPES, RECIPE_GROUPS, RECIPE_GROUP_ITEMS, expandStationTiles,
tests/vanilla-recipes.test.ts:10:import { RECIPES } from '../src/data/recipes';
tests/vanilla-recipes.test.ts:19:    expect(VANILLA_RECIPES.length).toBe(3173); // 线性+生成器+模板22件套+小动物雕像+反向平台/墙，源码重复注册已去重
tests/vanilla-recipes.test.ts:25:    const torch = VANILLA_RECIPES.find((r) => r.create === 8);
tests/vanilla-recipes.test.ts:61:    const torch = VANILLA_RECIPES.find((r) => r.create === 8)!;
tests/vanilla-recipes.test.ts:68:    const anvilRecipe = VANILLA_RECIPES.find((r) => r.tile === 16);
tests/vanilla-recipes.test.ts:80:describe('自制配方表 RECIPES 去重 + 与原版表不重叠', () => {
tests/vanilla-recipes.test.ts:83:    for (const r of RECIPES) {
tests/vanilla-recipes.test.ts:91:    const bad = RECIPES.filter((r) => r.out.startsWith('vi_'));
tests/vanilla-recipes.test.ts:96:    expect(RECIPES.filter((r) => r.out === 'wood_hammer')).toHaveLength(1);
tests/vanilla-recipes.test.ts:97:    expect(RECIPES.some((r) => r.out === 'vi_109_mana_crystal')).toBe(false);
tests/vanilla-recipes.test.ts:98:    const mc = VANILLA_RECIPES.find((r) => r.create === 109)!;

```


---

## 🤖 Assistant · 2026-08-12T15:52:26.902Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me grep for hardcoded local key references across src and tests. I'll do a big grep for the local keys. Let me extract the local keys list from PRIV_ITEM_STABLE (non-place_v_ ones).

Local keys (from PRIV_ITEM_STABLE, excluding place_v_*):
dirt_block, stone_block, wood, sand_block, snow_block, platform, torch, door, workbench, furnace, anvil, chest, gel, acorn, mushroom_item, copper_ore, iron_ore, silver_ore, gold_ore, copper_bar, iron_bar, silver_bar, gold_bar, lens, suspicious_eye, lesser_healing_potion, coin_copper, coin_silver, coin_gold, heal_potion, agility_potion, ironskin_potion, thorns_potion, regen_potion, lucky_horseshoe, feral_claws, copper_helmet/chainmail/greaves, iron_*, silver_*, gold_*, wood_pickaxe, wood_axe, wood_sword, wood_hammer, copper_pickaxe/axe/sword/hammer, iron_*, silver_*, gold_*, tin_ore, lead_ore, tungsten_ore, platinum_ore, tin_bar...platinum_bar, demonite_ore, meteorite, hellstone, crimtane_ore, cobalt_ore, mythril_ore, adamantite_ore, palladium_ore, orichalcum_ore, titanium_ore, chlorophyte_ore, sapphire, ruby, emerald, topaz, amethyst, diamond, ice_block, ice_brick, snow_brick, sandstone_block, hardened_sand_block, desert_fossil, clay_block, glass, obsidian, gray_brick, red_brick, mud_block, silt_block, table, chair, bed, bookcase, grandfather_clock, piano, dresser, bench, bathtub, keg, cooking_pot, clay_pot, tombstone, life_crystal, candle, chandelier, lantern, candelabra, chinese_lantern, skull_lantern, water_candle, bomb, rope, corrupt_grass_seeds, crimson_grass_seeds, jungle_grass_seeds, mushroom_grass_seeds, empty_bucket, water_bucket, lava_bucket, honey_bucket, tin_pickaxe, tin_axe, tin_sword, lead_*, tungsten_*, platinum_*, wooden_bow, wooden_arrow, flaming_arrow, iron_bow, minecart_item, wand_of_sparking, amethyst_bolt, worm_food, bloody_spine, slime_crown, mechanical_worm, mechanical_eye, mechanical_skull, wire, red_wrench, blue_wrench, green_wrench, yellow_wrench, wire_cutter, actuator_item, actuation_rod, multicolor_wrench, grand_design, goblin_battle_standard, snow_globe, pirate_map, coin_platinum, obsidian_skin_potion, gills_potion, mana_regen_potion, magic_power_potion, featherfall_potion, water_walking_potion, archery_potion, night_owl_potion, vi_109_mana_crystal (vi_, not local).

Also grass seed items: corrupt_grass_seeds etc.

Note: many of these keys are also tile keys (wood, torch, door_closed, platform, furnace, anvil, chest, dirt, stone, sand, snow, ice, glass, obsidian, etc.). Need to distinguish.

Let me do greps. I'll use a comprehensive approach: grep for quoted occurrences of each key. Better: build a regex of the local keys and grep src + tests.

Let me be smart and use grep -rnE with alternation. But note keys like 'bench' would match 'workbench' etc. Need word boundaries. Since keys appear quoted as 'wood' I can grep for ['"`]key['"`].

Let me write the grep carefully. Keys list (item keys, local, non-place_v):

dirt_block stone_block wood sand_block snow_block platform torch door workbench furnace anvil chest gel acorn mushroom_item copper_ore iron_ore silver_ore gold_ore copper_bar iron_bar silver_bar gold_bar lens suspicious_eye lesser_healing_potion coin_copper coin_silver coin_gold coin_platinum heal_potion agility_potion ironskin_potion thorns_potion regen_potion lucky_horseshoe feral_claws copper_helmet copper_chainmail copper_greaves iron_helmet iron_chainmail iron_greaves silver_helmet silver_chainmail silver_greaves gold_helmet gold_chainmail gold_greaves wood_pickaxe wood_axe wood_sword wood_hammer copper_pickaxe copper_axe copper_sword copper_hammer iron_pickaxe iron_axe iron_sword iron_hammer silver_pickaxe silver_axe silver_sword silver_hammer gold_pickaxe gold_axe gold_sword gold_hammer tin_ore lead_ore tungsten_ore platinum_ore tin_bar lead_bar tungsten_bar platinum_bar demonite_ore meteorite hellstone crimtane_ore cobalt_ore mythril_ore adamantite_ore palladium_ore orichalcum_ore titanium_ore chlorophyte_ore sapphire ruby emerald topaz amethyst diamond ice_block ice_brick snow_brick sandstone_block hardened_sand_block desert_fossil clay_block glass obsidian gray_brick red_brick mud_block silt_block table chair bed bookcase grandfather_clock piano dresser bench bathtub keg cooking_pot clay_pot tombstone life_crystal candle chandelier lantern candelabra chinese_lantern skull_lantern water_candle bomb rope corrupt_grass_seeds crimson_grass_seeds jungle_grass_seeds mushroom_grass_seeds empty_bucket water_bucket lava_bucket honey_bucket tin_pickaxe tin_axe tin_sword lead_pickaxe lead_axe lead_sword tungsten_pickaxe tungsten_axe tungsten_sword platinum_pickaxe platinum_axe platinum_sword wooden_bow wooden_arrow flaming_arrow iron_bow minecart_item wand_of_sparking amethyst_bolt worm_food bloody_spine slime_crown mechanical_worm mechanical_eye mechanical_skull wire red_wrench blue_wrench green_wrench yellow_wrench wire_cutter actuator_item actuation_rod multicolor_wrench grand_design goblin_battle_standard snow_globe pirate_map obsidian_skin_potion gills_potion mana_regen_potion magic_power_potion featherfall_potion water_walking_potion archery_potion night_owl_potion

That's ~165. Plus armor etc. The user said 172. Fine.

Now grep. I'll run a few greps in parallel with subsets. Use pattern like ['"]key['"] to get exact quoted matches.

Let me do it with a long alternation. Careful: shell escaping. Use single-quoted grep -E pattern with ['\"].

Let me generate the pattern with a script... but no writing files. I can build it inline in bash.

Actually simpler: grep -rnoE "['\"\`](wood|gel|...)['\"\`]" with all keys. Let me construct.

I'll run multiple greps grouped to keep pattern sizes manageable, excluding data/items.ts and data/recipes.ts themselves (we know those). Also exclude vanilla json data.

Let me do it.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:28.614Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "KEYS='dirt_block|stone_block|wood|sand_block|snow_block|platform|torch|door|workbench|furnace|anvil|chest|gel|acorn|mushroom_item|copper_ore|iron_ore|silver_ore|gold_ore|copper_bar|iron_bar|silver_bar|gold_bar|lens|suspicious_eye|lesser_healing_potion|coin_copper|coin_silver|coin_gold|coin_platinum|heal_potion|agility_potion|ironskin_potion|thorns_potion|regen_potion|lucky_horseshoe|feral_claws'; grep -rnE \"['\\\"\\`/]($KEYS)['\\\"\\`]\" src tests tools --include=\"*.ts\" | grep -v \"^src/data/items.ts\" | grep -v \"^src/data/recipes.ts\" | grep -vE \"vanilla(-|\\.)(item|recipes)\" | sort | head -200",
 "description": "Grep local item keys group 1"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:28.670Z

**📎 ToolResult**

```
<persisted-output>
Output too large (33.6KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/d76053b3-a9fb-4d75-a43d-41f181c7cab5/tool-results/bnnzdvqoa.txt

Preview (first 2KB):
src/assets/ItemIconGen.ts:170:  if (def.tile && ['dirt', 'stone', 'sand', 'snow', 'wood', 'platform'].includes(def.tile)) {
src/assets/ItemIconGen.ts:173:  if (def.tile === 'torch') {
src/assets/ItemIconGen.ts:181:  if (def.tile === 'workbench') {
src/assets/ItemIconGen.ts:187:  if (def.tile === 'furnace') {
src/assets/ItemIconGen.ts:193:  if (def.tile === 'anvil') {
src/assets/ItemIconGen.ts:200:  if (def.tile === 'chest') {
src/assets/ItemIconGen.ts:208:  if (def.tile === 'door') {
src/assets/ItemIconGen.ts:229:    case 'gel':
src/assets/ItemIconGen.ts:237:    case 'mushroom_item':
src/assets/ItemIconGen.ts:244:    case 'lens':
src/assets/ItemIconGen.ts:252:    case 'suspicious_eye':
src/assets/ItemIconGen.ts:261:    case 'lesser_healing_potion':
src/assets/ItemIconGen.ts:270:    case 'coin_copper':
src/assets/ItemIconGen.ts:41:    case 'wood': return MATS.wood;
src/assets/ItemIconGen.ts:42:    case 'platform': return MATS.wood;
src/core/Game.ts:10103:    return n('coin_copper', 1) + n('coin_silver', 100) + n('coin_gold', 10000) + n('coin_platinum', 1000000)
src/core/Game.ts:2986:      const gvid = heldDef.key === 'torch' ? -1 : viIdFromKey(heldDef.key);
src/core/Game.ts:3001:    const heldVid0 = heldDef ? (heldDef.key === 'torch' ? 8 : viIdFromKey(heldDef.key)) : -1;
src/core/Game.ts:3012:      const vid = heldDef.key === 'torch' ? 8 : viIdFromKey(heldDef.key);
src/core/Game.ts:3084:      const isTorch = def.tile === 'torch';
src/core/Game.ts:3562:      } else if (heldDef?.key === 'suspicious_eye') {
src/core/Game.ts:3728:      if (heldDef.key === 'suspicious_eye') {
src/core/Game.ts:4753:      this.spawnDrop(doorAnchor[0] * TILE + 8, doorAnchor[1] * TILE, def.drop ?? 'door', 1);
src/core/Game.ts:4852:        sheet === 3 && fx === 144 ? 'mushroom_item'
src/core/Game.ts:5004:      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-12T15:52:30.048Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Large. Let me view the persisted output file.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:30.359Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/d76053b3-a9fb-4d75-a43d-41f181c7cab5/tool-results/bnnzdvqoa.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:30.743Z

**📎 ToolResult**

```
1	src/assets/ItemIconGen.ts:170:  if (def.tile && ['dirt', 'stone', 'sand', 'snow', 'wood', 'platform'].includes(def.tile)) {
2	src/assets/ItemIconGen.ts:173:  if (def.tile === 'torch') {
3	src/assets/ItemIconGen.ts:181:  if (def.tile === 'workbench') {
4	src/assets/ItemIconGen.ts:187:  if (def.tile === 'furnace') {
5	src/assets/ItemIconGen.ts:193:  if (def.tile === 'anvil') {
6	src/assets/ItemIconGen.ts:200:  if (def.tile === 'chest') {
7	src/assets/ItemIconGen.ts:208:  if (def.tile === 'door') {
8	src/assets/ItemIconGen.ts:229:    case 'gel':
9	src/assets/ItemIconGen.ts:237:    case 'mushroom_item':
10	src/assets/ItemIconGen.ts:244:    case 'lens':
11	src/assets/ItemIconGen.ts:252:    case 'suspicious_eye':
12	src/assets/ItemIconGen.ts:261:    case 'lesser_healing_potion':
13	src/assets/ItemIconGen.ts:270:    case 'coin_copper':
14	src/assets/ItemIconGen.ts:41:    case 'wood': return MATS.wood;
15	src/assets/ItemIconGen.ts:42:    case 'platform': return MATS.wood;
16	src/core/Game.ts:10103:    return n('coin_copper', 1) + n('coin_silver', 100) + n('coin_gold', 10000) + n('coin_platinum', 1000000)
17	src/core/Game.ts:2986:      const gvid = heldDef.key === 'torch' ? -1 : viIdFromKey(heldDef.key);
18	src/core/Game.ts:3001:    const heldVid0 = heldDef ? (heldDef.key === 'torch' ? 8 : viIdFromKey(heldDef.key)) : -1;
19	src/core/Game.ts:3012:      const vid = heldDef.key === 'torch' ? 8 : viIdFromKey(heldDef.key);
20	src/core/Game.ts:3084:      const isTorch = def.tile === 'torch';
21	src/core/Game.ts:3562:      } else if (heldDef?.key === 'suspicious_eye') {
22	src/core/Game.ts:3728:      if (heldDef.key === 'suspicious_eye') {
23	src/core/Game.ts:4753:      this.spawnDrop(doorAnchor[0] * TILE + 8, doorAnchor[1] * TILE, def.drop ?? 'door', 1);
24	src/core/Game.ts:4852:        sheet === 3 && fx === 144 ? 'mushroom_item'
25	src/core/Game.ts:5004:      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
26	src/core/Game.ts:5007:      this.spawnDrop(b.x * TILE + 8, b.y * TILE + 8, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
27	src/core/Game.ts:5015:        this.spawnDrop(ax * TILE + 8, ay * TILE, 'acorn', 1, (Math.random() - 0.5) * 3, -3 - Math.random());
28	src/core/Game.ts:5045:      ? (isDemonHeart ? [['coin_gold', 1], ['gel', 100]] : [['suspicious_eye', 1], ['gel', 100]])
29	src/core/Game.ts:5046:      : [['coin_silver', 5], ['gel', 60]];
30	src/core/Game.ts:5104:        const key = dropId === 3 ? 'stone_block' : VANILLA_ITEM_KEY_BY_ID[dropId];
31	src/core/Game.ts:5125:      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
32	src/core/Game.ts:5133:        this.spawnDrop(ax * TILE + 8, ay * TILE, 'acorn', 1, (Math.random() - 0.5) * 3, -3 - Math.random());
33	src/core/Game.ts:5328:    if (itemDef.key === 'acorn' && st.get(tx, ty + 1) !== T.GRASS) {
34	src/core/Game.ts:6457:        const key = type === 71 ? 'coin_silver' : type === 72 ? 'coin_gold' : 'coin_platinum';
35	src/core/Game.ts:7009:      const override: Record<number, string> = { 8: 'torch', 73: 'coin_copper' };
36	src/core/Game.ts:7250:        this.spawnDrop(e.cx, e.y, 'coin_copper', 1 + Math.floor(Math.random() * 5), 0, -2);
37	src/core/Game.ts:7436:          if (def.key === 'coin_copper') copper += s.stack;
38	src/core/Game.ts:7437:          else if (def.key === 'coin_silver') copper += s.stack * 100;
39	src/core/Game.ts:7438:          else if (def.key === 'coin_gold') copper += s.stack * 10000;
40	src/core/Game.ts:8470:    if (gold) inv.add(ITEM_BY_KEY['coin_gold'], gold);
41	src/core/Game.ts:8471:    if (silver) inv.add(ITEM_BY_KEY['coin_silver'], silver);
42	src/core/Game.ts:8472:    if (copper) inv.add(ITEM_BY_KEY['coin_copper'], copper);
43	src/core/Game.ts:8498:      if (sl.id === ITEM_BY_KEY['coin_copper'] || sl.id === ITEM_BY_KEY['coin_silver']
44	src/core/Game.ts:8499:        || sl.id === ITEM_BY_KEY['coin_gold'] || sl.id === ITEM_BY_KEY['coin_platinum']
45	src/core/Game.ts:8510:    if (plat) inv.add(ITEM_BY_KEY['coin_platinum'], plat);
46	src/core/Game.ts:8511:    if (gold) inv.add(ITEM_BY_KEY['coin_gold'], gold);
47	src/core/Game.ts:8512:    if (silver) inv.add(ITEM_BY_KEY['coin_silver'], silver);
48	src/core/Game.ts:8513:    if (copper) inv.add(ITEM_BY_KEY['coin_copper'], copper);
49	src/core/Game.ts:8687:            ['coin_copper', 'vi_71_CopperCoin'], ['coin_silver', 'vi_72_SilverCoin'],
50	src/core/Game.ts:8688:            ['coin_gold', 'vi_73_GoldCoin'], ['coin_platinum', 'vi_74_PlatinumCoin'],
51	src/core/Game.ts:9605:      this.spawnDrop(tx * TILE + 8, ty * TILE, 'torch', 1);
52	src/core/Game.ts:9670:        if (t === T.WORKBENCH) found.add('workbench');
53	src/core/Game.ts:9671:        if (t === T.FURNACE) found.add('furnace');
54	src/core/Game.ts:9672:        if (t === T.ANVIL) found.add('anvil');
55	src/data/enemies.ts:120:    drops: [{ item: 'coin_gold', min: 1, max: 1, chance: 1 }],
56	src/data/enemies.ts:33:    drops: [{ item: 'gel', min: 1, max: 2, chance: 1 }],
57	src/data/enemies.ts:40:    drops: [{ item: 'gel', min: 1, max: 2, chance: 1 }],
58	src/data/enemies.ts:48:      { item: 'coin_copper', min: 40, max: 80, chance: 1 },
59	src/data/enemies.ts:49:      { item: 'iron_ore', min: 1, max: 2, chance: 0.15 },
60	src/data/enemies.ts:50:      { item: 'lesser_healing_potion', min: 1, max: 1, chance: 0.04 },
61	src/data/enemies.ts:59:      { item: 'lens', min: 1, max: 1, chance: 0.33 },
62	src/data/enemies.ts:60:      { item: 'coin_copper', min: 50, max: 100, chance: 1 },
63	src/data/enemies.ts:68:    drops: [{ item: 'coin_copper', min: 1, max: 4, chance: 0.5 }],
64	src/data/enemies.ts:75:    drops: [{ item: 'gel', min: 1, max: 3, chance: 1 }, { item: 'torch', min: 1, max: 2, chance: 0.4 }],
65	src/data/enemies.ts:82:    drops: [{ item: 'iron_ore', min: 1, max: 2, chance: 0.3 }, { item: 'coin_copper', min: 5, max: 15, chance: 0.8 }],
66	src/data/enemies.ts:90:      { item: 'lesser_healing_potion', min: 2, max: 4, chance: 1 },
67	src/data/enemies.ts:91:      { item: 'coin_gold', min: 3, max: 3, chance: 1 },
68	src/data/enemies.ts:99:    drops: [{ item: 'lens', min: 1, max: 1, chance: 0.25 }],
69	src/data/tiles.ts:49:def({ key: 'dirt', name: '泥土', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: 'dirt_block', vanilla: { sheet: 0, frame: 'blend' } });
70	src/data/tiles.ts:50:def({ key: 'stone', name: '石块', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: 'stone_block', vanilla: { sheet: 1, frame: 'blend' } });
71	src/data/tiles.ts:51:def({ key: 'grass', name: '草块', solid: true, opacity: 1, pick: 0, mapColor: '#1CD85E', blend: true, drop: 'dirt_block', vanilla: { sheet: 2, frame: 'blend' } });
72	src/data/tiles.ts:52:def({ key: 'ore_copper', name: '铜矿', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: false, drop: 'copper_ore', vanilla: { sheet: 7, frame: 'auto' } });
73	src/data/tiles.ts:53:def({ key: 'ore_iron', name: '铁矿', solid: true, opacity: 1, pick: 0, mapColor: '#8C6550', blend: false, drop: 'iron_ore', vanilla: { sheet: 6, frame: 'auto' } });
74	src/data/tiles.ts:54:def({ key: 'ore_silver', name: '银矿', solid: true, opacity: 1, pick: 20, mapColor: '#B9C2C3', blend: false, drop: 'silver_ore', vanilla: { sheet: 9, frame: 'auto' } });
75	src/data/tiles.ts:55:def({ key: 'ore_gold', name: '金矿', solid: true, opacity: 1, pick: 40, mapColor: '#B9A417', blend: false, drop: 'gold_ore', vanilla: { sheet: 8, frame: 'auto' } });
76	src/data/tiles.ts:56:def({ key: 'tree', name: '树干', solid: false, framed: true, opacity: 0.1, axe: 0, mapColor: '#976B4B', drop: 'wood', vanilla: { sheet: 5, frame: 'style', fw: 1, fh: 1 } });
77	src/data/tiles.ts:58:def({ key: 'wood', name: '木材块', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: 'wood', vanilla: { sheet: 30, frame: 'auto' } });
78	src/data/tiles.ts:59:def({ key: 'platform', name: '木平台', platform: true, opacity: 0.15, pick: 0, axe: 0, mapColor: '#BF8E6F', drop: 'platform', vanilla: { sheet: 19, frame: 'style', fw: 1, fh: 1 } });
79	src/data/tiles.ts:60:def({ key: 'torch', name: '火把', decor: true, framed: true, opacity: 0, pick: 0, light: [255, 225, 150], mapColor: '#FDDD03', drop: 'torch', vanilla: { sheet: 4, frame: 'style', fw: 1, fh: 1 } });
80	src/data/tiles.ts:62:def({ key: 'workbench', name: '工作台', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#BF8E6F', drop: 'workbench', vanilla: { sheet: 18, frame: 'style', fw: 2, fh: 1 } });
81	src/data/tiles.ts:63:def({ key: 'furnace', name: '熔炉', solid: false, /* 原版 tileSolid[17]=false：熔炉可通行 */ framed: true, opacity: 1, pick: 0, w: 3, h: 2, light: [255, 140, 70], mapColor: '#909490', drop: 'furnace', vanilla: { sheet: 17, frame: 'style', fw: 3, fh: 2 } });
82	src/data/tiles.ts:64:def({ key: 'anvil', name: '铁砧', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#8C8274', drop: 'anvil', vanilla: { sheet: 16, frame: 'style', fw: 2, fh: 1 } });
83	src/data/tiles.ts:65:def({ key: 'chest', name: '宝箱', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#AE815C', drop: 'chest', vanilla: { sheet: 21, frame: 'style', fw: 2, fh: 2 } });
84	src/data/tiles.ts:66:def({ key: 'door_closed', name: '门', solid: true, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#77694F', drop: 'door', vanilla: { sheet: 10, frame: 'style', fw: 1, fh: 3 } });
85	src/data/tiles.ts:67:def({ key: 'door_open', name: '门(开)', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#77694F', drop: 'door', vanilla: { sheet: 11, frame: 'style', fw: 2, fh: 3 } });
86	src/data/tiles.ts:68:def({ key: 'mushroom', name: '蘑菇', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#1AC454', drop: 'mushroom_item', vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
87	src/data/tiles.ts:70:def({ key: 'tallgrass', name: '草丛', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#1AC454', drop: 'acorn', vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
88	src/data/tiles.ts:71:def({ key: 'sand', name: '沙块', solid: true, opacity: 1, pick: 0, mapColor: '#BAA854', blend: true, drop: 'sand_block', vanilla: { sheet: 53, frame: 'blend' } });
89	src/data/tiles.ts:72:def({ key: 'snow', name: '雪块', solid: true, opacity: 1, pick: 0, mapColor: '#D3ECF1', blend: true, drop: 'snow_block', vanilla: { sheet: 147, frame: 'blend' } });
90	src/data/tiles.ts:73:def({ key: 'acorn_sapling', name: '树苗', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#A37451', drop: 'acorn', vanilla: { sheet: 20, frame: 'style', fw: 1, fh: 1 } });
91	src/data/tiles.ts:74:def({ key: 'ash', name: '灰烬块', solid: true, opacity: 1, pick: 0, mapColor: '#44444C', blend: true, drop: 'stone_block', vanilla: { sheet: 57, frame: 'auto' } });
92	src/entities/Enemy.ts:59:  71: 'coin_copper', 72: 'coin_silver', 73: 'coin_gold', 74: 'coin_platinum',
93	src/entities/Enemy.ts:60:  23: 'gel', 8: 'torch', 236: 'lens', 3: 'stone_block', 2: 'dirt_block', 9: 'wood',
94	src/entities/Enemy.ts:61:  28: 'lesser_healing_potion',
95	src/entities/ItemDrop.ts:85:          game.playSfx(ITEM_DEFS[this.itemId]?.key === 'coin_copper' ? 'coin' : 'pickup', 0.75);
96	src/entities/Player.ts:186:      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
97	src/entities/Player.ts:193:      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
98	src/i18n/idNames.generated.ts:25003:export const ITEM_KEY_TO_ID: Record<string, number> = {"dirt_block":2,"stone_block":3,"wood":9,"sand_block":169,"snow_block":593,"platform":94,"torch":8,"door":25,"workbench":36,"furnace":33,"anvil":35,"chest":48,"gel":23,"acorn":27,"mushroom_item":5,"copper_ore":12,"iron_ore":11,"silver_ore":14,"gold_ore":13,"copper_bar":20,"iron_bar":22,"silver_bar":21,"gold_bar":19,"lens":38,"suspicious_eye":43,"lesser_healing_potion":28,"coin_copper":71,"coin_silver":72,"coin_gold":73,"heal_potion":188,"agility_potion":290,"ironskin_potion":292,"thorns_potion":301,"regen_potion":289,"obsidian_skin_potion":288,"gills_potion":291,"magic_power_potion":294,"featherfall_potion":295,"water_walking_potion":302,"archery_potion":303,"night_owl_potion":299,"lucky_horseshoe":158,"feral_claws":211,"wood_sword":24,"wood_hammer":196,"copper_pickaxe":3509,"copper_axe":3506,"copper_sword":3508,"copper_hammer":3505,"iron_pickaxe":1,"iron_axe":10,"iron_sword":4,"iron_hammer":7,"silver_pickaxe":3515,"silver_axe":3512,"silver_sword":3514,"silver_hammer":3511,"gold_pickaxe":3521,"gold_axe":3518,"gold_sword":3520,"gold_hammer":3517,"tin_ore":699,"lead_ore":700,"tungsten_ore":701,"platinum_ore":702,"tin_bar":703,"lead_bar":704,"tungsten_bar":705,"platinum_bar":706,"demonite_ore":56,"meteorite":116,"hellstone":174,"crimtane_ore":880,"cobalt_ore":364,"mythril_ore":365,"adamantite_ore":366,"palladium_ore":1104,"orichalcum_ore":1105,"titanium_ore":1106,"chlorophyte_ore":947,"sapphire":177,"ruby":178,"emerald":179,"topaz":180,"amethyst":181,"diamond":182,"ice_block":664,"ice_brick":883,"snow_brick":594,"sandstone_block":3271,"hardened_sand_block":3272,"desert_fossil":3347,"clay_block":133,"glass":170,"obsidian":173,"gray_brick":129,"red_brick":131,"mud_block":176,"silt_block":424,"table":32,"chair":34,"bed":224,"bookcase":354,"grandfather_clock":359,"piano":333,"dresser":334,"bench":335,"bathtub":336,"keg":352,"cooking_pot":345,"clay_pot":222,"tombstone":321,"life_crystal":29,"vi_109_mana_crystal":109,"vi_1291_life_fruit":1291,"candle":105,"chandelier":106,"lantern":136,"candelabra":349,"chinese_lantern":344,"skull_lantern":347,"water_candle":148,"bomb":166,"rope":965,"vi_2350_recall_potion":2350,"vi_188_healing_potion":188,"vi_282_glowstick":282,"vi_41_flaming_arrow":41,"vi_167_dynamite":167,"vi_279_throwing_knife":279,"vi_51_jester_s_arrow":51,"vi_19_gold_bar":19,"vi_302_water_walking_potion":302,"vi_305_gravitation_potion":305,"vi_43_suspicious_looking_eye":43,"vi_296_spelunker_potion":296,"vi_299_night_owl_potion":299,"vi_965_rope":965,"vi_303_archery_potion":303,"vi_304_hunter_potion":304,"vi_50_magic_mirror":50,"vi_42_shuriken":42,"vi_295_featherfall_potion":295,"vi_53_cloud_in_a_bottle":53,"vi_2329_dangersense_potion":2329,"vi_40_wooden_arrow":40,"vi_975_shoe_spikes":975,"vi_54_hermes_boots":54,"vi_301_thorns_potion":301,"vi_49_band_of_regeneration":49,"vi_2326_titan_potion":2326,"vi_297_invisibility_potion":297,"vi_166_bomb":166,"vi_5011_mace":5011,"vi_4425_shark_bait":4425,"vi_2351_teleportation_potion":2351,"vi_4460_sandcastle_bucket":4460,"vi_168_grenade":168,"vi_227_restoration_potion":227,"vi_930_flare_gun":930,"vi_931_flare":931,"vi_997_extractinator":997,"vi_52_angel_statue":52,"vi_265_hellfire_arrow":265,"vi_298_shine_potion":298,"vi_5007_dead_man_s_sweater":5007,"vi_117_meteorite_bar":117,"vi_186_breathing_reed":186,"vi_329_shadow_key":329,"vi_974_ice_torch":974,"vi_2322_mining_potion":2322,"vi_4915_tungsten_bullet":4915,"vi_946_umbrella":946,"vi_939_web_slinger":939,"vi_4870_potion_of_return":4870,"vi_288_obsidian_skin_potion":288,"vi_31_bottle":31,"vi_211_feral_claws":211,"vi_4404_inner_tube":4404,"vi_187_flipper":187,"vi_2198_ice_machine":2198,"vi_274_dark_lance":274,"vi_285_aglet":285,"vi_213_staff_of_regrowth":213,"vi_964_boomstick":964,"vi_1293_lihzahrd_power_cell":1293,"vi_2195_lihzahrd_furnace":2195,"vi_2766_solar_tablet_fragment":2766,"vi_300_battle_potion":300,"vi_2348_inferno_potion":2348,"vi_218_flamelash":218,"vi_3019_hellwing_bow":3019,"vi_112_flower_of_fire":112,"vi_220_sunfury":220,"vi_4345_can_of_worms":4345,"vi_953_climbing_claws":953,"vi_3069_wand_of_sparking":3069,"vi_212_anklet_of_the_wind":212,"vi_2204_honey_dispenser":2204,"vi_277_trident":277,"vi_863_water_walking_boots":863,"vi_751_cloud":751,"vi_155_muramasa":155,"vi_289_regeneration_potion":289,"vi_906_lava_charm":906,"vi_4055_dunerider_boots":4055,"vi_724_ice_blade":724,"vi_670_ice_boomerang":670,"vi_4061_storm_spear":4061,"vi_987_blizzard_in_a_bottle":987,"vi_4551_slice_of_hell_cake":4551,"vi_5010_treasure_magnet":5010,"vi_2323_heartreach_potion":2323,"vi_2345_lifeforce_potion":2345,"vi_290_swiftness_potion":290,"vi_291_gills_potion":291,"vi_280_spear":280,"vi_2325_builder_potion":2325,"vi_284_wooden_boomerang":284,"vi_2192_bone_welder":2192,"vi_5234_remnants_of_devotion":5234,"vi_156_cobalt_shield":156,"vi_157_aqua_scepter":157,"vi_163_blue_moon":163,"vi_113_magic_missile":113,"vi_3317_valor":3317,"vi_327_golden_key":327,"vi_164_handgun":164,"vi_294_magic_power_potion":294,"vi_4263_magic_conch":4263,"vi_4062_thunder_zapper":4062,"vi_1579_flurry_boots":1579,"vi_4056_ancient_chisel":4056,"vi_4346_encumbering_stone":4346,"vi_1319_snowball_cannon":1319,"vi_3199_ice_mirror":3199,"vi_950_ice_skates":950,"vi_4443_demonic_hellcart":4443,"vi_4737_ornate_shadow_key":4737,"vi_4276_bast_statue":4276,"vi_4262_snake_charmer_s_flute":4262,"vi_3093_herb_bag":3093,"vi_292_ironskin_potion":292,"vi_3084_radar":3084,"vi_4341_step_stool":4341,"vi_4978_fledgling_wings":4978,"vi_2197_sky_mill":2197,"vi_158_lucky_horseshoe":158,"vi_5254_blessing_from_the_heavens":5254,"vi_1156_piranha_gun":1156,"vi_1571_scourge_of_the_corruptor":1571,"vi_1260_rainbow_gun":1260,"vi_1572_staff_of_the_frost_hydra":1572,"vi_4607_desert_tiger_staff":4607,"vi_933_leaf_wand":933,"vi_832_living_wood_wand":832,"vi_4066_desert_minecart":4066,"vi_4450_shroom_minecart":4450,"vi_4423_scarab_bomb":4423,"vi_159_shiny_red_balloon":159,"vi_5258_see_the_world_for_what_it_is":5258,"vi_65_starfury":65,"vi_5388_eye_of_the_sun":5388,"vi_2219_celestial_magnet":2219,"vi_5255_love_is_in_the_trash_slot":5255,"vi_4426_bee_minecart":4426,"vi_3017_flower_boots":3017,"vi_3360_living_mahogany_wand":3360,"vi_3361_rich_mahogany_leaf_wand":3361,"vi_1309_slime_staff":1309,"vi_1845_necromantic_scroll":1845,"vi_1864_papyrus_scarab":1864,"vi_1158_pygmy_necklace":1158,"vi_3034_coin_ring":3034,"vi_308_moonglow_seeds":308,"vi_312_fireblossom_seeds":312,"vi_310_deathweed_seeds":310,"vi_307_daybloom_seeds":307,"vi_309_blinkroot_seeds":309,"vi_2357_shiverthorn_seeds":2357,"vi_311_waterleaf_seeds":311,"vi_1828_pumpkin_seed":1828,"vi_126_bottled_water":126,"vi_1134_bottled_honey":1134,"vi_3068_guide_to_plant_fiber_cordage":3068,"vi_4779_mushroom_hat":4779,"vi_4780_mushroom_vest":4780,"vi_4781_mushroom_pants":4781,"vi_678_red_potion":678,"vi_281_blowpipe":281,"vi_293_mana_regeneration_potion":293,"vi_2767_solar_tablet":2767,"vi_3213_money_trough":3213,"vi_2757_vortex_helmet":2757,"vi_4989_soaring_insignia":4989,"vi_3383_stardust_leggings":3383,"vi_4914_kaleidoscope":4914,"vi_1991_bug_net":1991,"vi_4828_superheated_blood":4828,"vi_3509_copper_pickaxe":3509,"vi_3507_copper_shortsword":3507,"vi_4755_grox_the_great_s_horned_cowl":4755,"vi_4756_grox_the_great_s_chestplate":4756,"vi_4757_grox_the_great_s_greaves":4757,"vi_5000_terraspark_boots":5000,"vi_5339_arcane_crystal":5339,"vi_5340_galaxy_pearl":5340,"vi_5577_pretty_mirror":5577,"vi_5391_uncumbering_stone":5391,"vi_2585_slime_hook":2585,"vi_313_daybloom":313,"vi_267_guide_voodoo_doll":267,"vi_2649_steampunk_candle":2649,"vi_286_sticky_glowstick":286,"vi_3002_spelunker_glowstick":3002,"vi_4819_demon_conch":4819,"vi_1802_raven_staff":1802,"vi_3382_stardust_plate":3382,"vi_3270_item_frame":3270,"vi_3771_ancient_horn":3771,"vi_4281_finch_staff":4281,"vi_5407_star_royale_brick":5407,"vi_5401_lunar_rust_brick":5401,"vi_5402_dark_celestial_brick":5402,"vi_5406_mercury_brick":5406,"vi_5408_heavenforge_brick":5408,"vi_4716_mollusk_whistle":4716,"vi_3540_phantasm":3540,"vi_2176_shroomite_digging_claw":2176,"vi_2349_wrath_potion":2349,"vi_4679_morning_star":4679,"vi_1169_bone_key":1169,"vi_3863_betsy_mask":3863,"vi_3124_cell_phone":3124,"vi_3506_copper_axe":3506,"vi_4680_dark_harvest":4680,"vi_543_brown_pressure_plate":543,"vi_171_sign":171,"vi_1723_living_wood_wall":1723,"vi_4754_grox_the_great_s_wings":4754,"vi_3353_mechanical_cart":3353,"vi_2287_winter_cape":2287,"vi_1179_chlorophyte_bullet":1179,"vi_4766_world_globe":4766,"vi_4954_celestial_starboard":4954,"vi_4730_ghostar_s_infinity_eight":4730,"vi_4758_blade_staff":4758,"vi_4765_tree_globe":4765,"vi_5342_ambrosia":5342,"vi_5328_chest_lock":5328,"vi_5343_peddler_s_satchel":5343,"vi_5285_moon_globe":5285,"vi_5289_minecart_upgrade_kit":5289,"vi_5336_advanced_combat_techniques_volume_two":5336,"vi_5451_kwad_racer_drone":5451,"vi_5359_shellphone_spawn":5359,"vi_3032_super_absorbant_sponge":3032,"vi_3031_bottomless_water_bucket":3031,"vi_509_red_wrench":509,"vi_4741_butcher_s_bloodstained_apron":4741,"vi_3065_star_wrath":3065,"vi_3063_meowmere":3063,"vi_3372_lunatic_cultist_mask":3372,"vi_1504_spectre_robe":1504,"vi_2769_cosmic_car_key":2769,"vi_216_shackle":216,"vi_4415_stone_door":4415,"vi_1681_skeleton_banner":1681,"vi_283_seed":283,"vi_1173_grave_marker":1173,"vi_4379_wyvern_kite":4379,"vi_4378_xenon_moss":4378,"vi_4377_krypton_moss":4377,"vi_4376_rat_cage":4376,"vi_4375_rat":4375,"vi_4484_1_2_second_timer":4484,"vi_4824_wet_bomb":4824,"vi_4485_1_4_second_timer":4485,"vi_5378_cursed_flare":5378,"vi_5354_reflective_shades":5354,"vi_5387_raynbro_s_pants":5387,"vi_5386_raynbro_s_hoodie":5386,"vi_5390_raynbro_s_hood":5390,"vi_5338_aegis_fruit":5338,"vi_5404_cosmic_ember_brick":5404,"vi_5405_cryocore_brick":5405,"vi_5403_astra_brick":5403,"vi_346_safe":346,"vi_4829_cat_license":4829,"vi_3335_demon_heart":3335,"vi_4750_foodbarbarian_s_tattered_dragon_wings":4750,"vi_3042_phase_dye":3042,"vi_3024_skiphs_blood":3024,"vi_3054_shadowflame_knife":3054,"vi_5275_joja_cola":5275,"vi_5278_pomegranate":5278,"vi_5277_spicy_pepper":5277,"vi_5437_shellphone":5437,"vi_1507_spectre_hamaxe":1507,"vi_2250_steampunk_chest":2250,"vi_392_glass_wall":392,"vi_2699_weapon_rack":2699,"vi_3552_blue_flame_and_silver_dye":3552,"vi_5005_terraprisma":5005,"vi_4604_exotic_chew_toy":4604,"vi_4611_world_feeder_kite":4611,"vi_4649_blue_jellyfish_kite":4649,"vi_4796_dark_mage_s_tome":4796,"vi_4553_plasma_lamp":4553,"vi_4365_celestial_wand":4365,"vi_331_jungle_spores":331,"vi_2430_slimy_saddle":2430,"vi_4956_zenith":4956,"vi_2798_laser_drill":2798,"vi_2814_martian_chest":2814,"vi_210_vine":210,"vi_4371_yellow_kite":4371,"vi_4291_lemon":4291,"vi_2493_king_slime_mask":2493,"vi_1919_sugar_cookie":1919,"vi_1912_eggnog":1912,"vi_4023_grapes":4023,"vi_4792_the_black_spot":4792,"vi_3066_smooth_marble_block":3066,"vi_1103_slush_block":1103,"vi_2119_stone_slab":2119,"vi_593_snow_block":593,"vi_3081_marble_block":3081,"vi_1111_blue_berries":1111,"vi_1115_red_husk":1115,"vi_217_molten_hamaxe":217,"vi_122_molten_pickaxe":122,"vi_1827_bladed_glove":1827,"vi_2263_white_dynasty_wall":2263,"vi_330_obsidian_brick_wall":330,"vi_2433_stone_slab_wall":2433,"vi_452_hornet_statue":452,"vi_453_bomb_statue":453,"vi_360_armor_statue":360,"vi_3711_wraith_statue":3711,"vi_438_star_statue":438,"vi_446_skeleton_statue":446,"vi_458_cross_statue":458,"vi_3655_scorpion_statue":3655,"vi_328_shadow_chest":328,"vi_2196_living_loom":2196,"vi_916_shadewood_work_bench":916,"vi_35_iron_anvil":35,"vi_36_work_bench":36,"vi_3240_tall_gate":3240,"vi_337_red_banner":337,"vi_3381_stardust_helmet":3381,"vi_1765_vampire_pants":1765,"vi_2859_lunar_cultist_robe":2859,"vi_2857_lunar_cultist_hood":2857,"vi_2998_summoner_emblem":2998,"vi_1175_headstone":1175,"vi_25_wooden_door":25,"vi_46_light_s_bane":46,"vi_2340_minecart_track":2340,"vi_498_mannequin":498,"vi_4721_mushroom_beam":4721,"vi_819_living_wood_door":819,"vi_1458_obsidian_door":1458,"vi_3763_0x33_s_aviators":3763,"vi_176_mud_block":176,"vi_1569_vampire_knives":1569,"vi_857_sandstorm_in_a_bottle":857,"vi_2292_fiberglass_fishing_pole":2292,"vi_5238_constellation":5238,"vi_753_seaweed":753,"vi_3_stone_block":3,"vi_94_wood_platform":94,"vi_75_fallen_star":75,"vi_26_stone_wall":26,"vi_214_hellstone_brick":214,"vi_93_wood_wall":93,"vi_172_ash_block":172,"vi_118_hook":118,"vi_529_red_pressure_plate":529,"vi_183_glowing_mushroom":183,"vi_130_gray_brick_wall":130,"vi_352_keg":352,"vi_5120_deer_thing":5120,"vi_5508_grim_old_barb":5508,"vi_5465_ram_rune":5465,"vi_5500_goat_s_tuft":5500,"vi_5499_froggy_neckband":5499,"vi_5507_balloony_beads":5507,"vi_5485_chicken_charm":5485,"vi_5502_cat_chime":5502,"vi_5504_turkey_wattle_necklace":5504,"vi_5506_crow_s_beak":5506,"vi_5503_dog_collar":5503,"vi_5534_fairy_choker":5534,"vi_5484_cow_bell":5484,"vi_5501_old_companion_locket":5501,"vi_5509_vampire_pendant":5509,"vi_5505_mean_goblin_s_spikes":5505,"vi_5525_cursed_piper_flute":5525,"corrupt_grass_seeds":59,"crimson_grass_seeds":2171,"jungle_grass_seeds":195,"mushroom_grass_seeds":194,"vi_103_nightmare_pickaxe":103,"vi_104_the_breaker":104,"vi_204_meteor_hamaxe":204,"vi_367_pwnhammer":367,"vi_579_drax":579,"vi_654_ebonwood_hammer":654,"vi_657_rich_mahogany_hammer":657,"vi_660_pearlwood_hammer":660,"vi_776_cobalt_pickaxe":776,"vi_777_mythril_pickaxe":777,"vi_778_adamantite_pickaxe":778,"vi_787_hammush":787,"vi_797_flesh_grinder":797,"vi_798_deathbringer_pickaxe":798,"vi_922_shadewood_hammer":922,"vi_990_pickaxe_axe":990,"vi_1188_palladium_pickaxe":1188,"vi_1195_orichalcum_pickaxe":1195,"vi_1202_titanium_pickaxe":1202,"vi_1234_chlorophyte_warhammer":1234,"vi_1262_chlorophyte_jackhammer":1262,"vi_1305_the_axe":1305,"vi_1506_spectre_pickaxe":1506,"vi_3481_platinum_hammer":3481,"vi_3487_tungsten_hammer":3487,"vi_3493_lead_hammer":3493,"vi_3499_tin_hammer":3499,"vi_3505_copper_hammer":3505,"vi_3511_silver_hammer":3511,"vi_3517_gold_hammer":3517,"vi_3525_stardust_hamaxe":3525,"vi_4317_haemorrhaxe":4317,"empty_bucket":205,"water_bucket":206,"lava_bucket":207,"honey_bucket":1128,"tin_pickaxe":3503,"tin_axe":3500,"tin_sword":3502,"lead_pickaxe":3497,"lead_axe":3494,"lead_sword":3496,"tungsten_pickaxe":3491,"tungsten_axe":3488,"tungsten_sword":3490,"platinum_pickaxe":3485,"platinum_axe":3482,"platinum_sword":3484,"wooden_bow":39,"wooden_arrow":40,"flaming_arrow":41,"iron_bow":99,"minecart_item":2343,"wand_of_sparking":3069,"amethyst_bolt":739,"worm_food":70,"goblin_battle_standard":361,"snow_globe":602,"pirate_map":1315,"bloody_spine":1331,"slime_crown":560,"mechanical_worm":556,"mechanical_eye":544,"mechanical_skull":557,"wire":530,"red_wrench":509,"blue_wrench":850,"green_wrench":851,"yellow_wrench":3612,"wire_cutter":510,"actuator_item":849,"actuation_rod":3620,"multicolor_wrench":3625,"grand_design":3625};
99	src/items/Inventory.ts:39:export const COIN_KEYS = ['coin_copper', 'coin_silver', 'coin_gold', 'coin_platinum'] as const;
100	src/mainFlow.ts:323:      g.player.inv.add(ITEM_BY_KEY['torch'], 20);
101	src/player/SmartCursor.ts:1216:    const isTorch = (vid != null && TORCH_ITEMS.has(vid)) || sem.createTileSheet === 4 || env.held.def?.key === 'torch';
102	src/render/Renderer.ts:3131:        const vid = def.key === 'torch' ? 8 : viIdFromKey(def.key);
103	src/ui/UI.ts:1797:      grid.appendChild(this.makeSlotEl(i, 'chest'));
104	src/ui/UI.ts:1844:      if (cur.id === ITEM_BY_KEY['coin_copper'] || cur.id === ITEM_BY_KEY['coin_silver']
105	src/ui/UI.ts:1845:        || cur.id === ITEM_BY_KEY['coin_gold'] || cur.id === ITEM_BY_KEY['coin_platinum']) continue;
106	src/ui/UI.ts:1884:        this.setSlotGlow('chest', k, ((order.get(id) ?? 0) + 0.5) / n);
107	src/ui/UI.ts:1936:    else if (where === 'chest') tex = 'Inventory_Back5';
108	src/ui/UI.ts:2113:        const slotEl = this.slotEl(i, 'chest');
109	src/ui/UI.ts:2116:          this.paintSlotChrome(slotEl, 'chest', i);
110	src/ui/UI.ts:22:type SlotWhere = 'inv' | 'chest' | 'armor' | 'dye' | 'misc' | 'miscDye';
111	src/ui/UI.ts:2412:      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
112	src/ui/UI.ts:2413:      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
113	src/ui/UI.ts:2414:      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
114	src/ui/UI.ts:2416:      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
115	src/ui/UI.ts:2417:      [BuffType.Bleeding, 'lesser_healing_potion'], [BuffType.Suffocation, 'sand_block'],
116	src/ui/UI.ts:2490:      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
117	src/ui/UI.ts:2491:      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
118	src/ui/UI.ts:2492:      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
119	src/ui/UI.ts:2493:      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
120	src/ui/UI.ts:2494:      [BuffType.Bleeding, 'lesser_healing_potion'], [BuffType.Suffocation, 'sand_block'],
121	src/ui/UI.ts:757:    if (where === 'chest') {
122	src/ui/UI.ts:935:      if (tw === 'chest' && !this.openChest) return;
123	src/wld/WldImport.ts:116:  4: { key: 'torch', copyFrame: true },  // Torch（保留原版墙面/熄灭变体帧）
124	src/wld/WldImport.ts:123:  16: 'anvil',        // Anvil(2×1,铁/铅两款 style)
125	src/wld/WldImport.ts:124:  17: 'furnace',      // Furnace(3×2!曾误映射 anvil——导入的熔炉渲染成半格铁砧/拆除波及邻砧)
126	src/wld/WldImport.ts:125:  18: 'workbench',    // Work Bench
127	src/wld/WldImport.ts:126:  19: { key: 'platform', copyFrame: true },  // Wood Platform（原版帧直拷）
128	src/wld/WldImport.ts:127:  21: 'chest',  // Chest（帧按格距重建，不直拷——wld 存的是格偏移 0/1 不是像素）
129	src/wld/WldImport.ts:357:  28: { key: 'pot', copyFrame: true }, 29: { key: 'v_29_piggy_bank', copyFrame: true }, 30: 'wood',  // Pots(原版) / Piggy Bank(2×1 framed) / Wood→木材
130	src/wld/WldImport.ts:420:  2: 'dirt_block', 8: 'torch', 9: 'wood', 175: 'stone_block',
131	src/wld/WldImport.ts:421:  11: 'iron_ore', 12: 'copper_ore', 13: 'gold_ore', 14: 'silver_ore',
132	src/wld/WldImport.ts:422:  20: 'copper_bar', 22: 'iron_bar', 23: 'gel',
133	src/wld/WldImport.ts:423:  28: 'lesser_healing_potion', 38: 'lens',
134	src/wld/WldImport.ts:424:  71: 'coin_copper', 72: 'coin_copper', 73: 'coin_copper', 74: 'coin_copper',
135	src/wld/WldImport.ts:433:  5: 'mushroom_item', 27: 'acorn',
136	src/wld/WldImport.ts:909:    type[c.y * w + c.x] = TILE_BY_KEY['chest'];
137	src/wld/WldImport.ts:912:    if (c.x + 1 < w) { type[c.y * w + c.x + 1] = TILE_BY_KEY['chest']; frameX[c.y * w + c.x + 1] = 18; frameY[c.y * w + c.x + 1] = 0; }
138	src/wld/WldImport.ts:913:    if (c.y + 1 < h) { type[(c.y + 1) * w + c.x] = TILE_BY_KEY['chest']; frameX[(c.y + 1) * w + c.x] = 0; frameY[(c.y + 1) * w + c.x] = 18; }
139	src/wld/WldImport.ts:914:    if (c.x + 1 < w && c.y + 1 < h) { type[(c.y + 1) * w + c.x + 1] = TILE_BY_KEY['chest']; frameX[(c.y + 1) * w + c.x + 1] = 18; frameY[(c.y + 1) * w + c.x + 1] = 18; }
140	src/world/Door.ts:141:  sfx?.('door'); // SoundID 8
141	src/world/Extractinator.ts:72:  71: 'coin_copper', 72: 'coin_silver', 73: 'coin_gold', 74: 'coin_platinum',
142	src/world/gen/vanilla/BuriedChestsPass.ts:19:const CHEST = TILE_BY_KEY['chest']!;
143	src/world/gen/vanilla/CaveHousePass.ts:141:    ['wood', count(SC0) + count(SC1)],
144	src/world/gen/vanilla/CaveHousePass.ts:21:type Theme = 'wood' | 'ice' | 'jungle' | 'desert' | 'granite' | 'marble' | 'mushroom';
145	src/world/gen/vanilla/CaveHousePass.ts:265:  if (theme === 'wood') {
146	src/world/gen/vanilla/CaveHousePass.ts:416:    ['anvil', 0],
147	src/world/gen/vanilla/CaveHousePass.ts:417:    ['workbench', def.workbench],
148	src/world/gen/vanilla/CaveHousePass.ts:44:const PLATFORM = TILE_BY_KEY['platform']!;
149	src/world/gen/vanilla/DungeonPass.ts:26:const CHEST = TILE_BY_KEY['chest']!;
150	src/world/gen/vanilla/DungeonPass.ts:28:const WORKBENCH = TILE_BY_KEY['workbench']!;
151	src/world/gen/vanilla/DungeonPass.ts:32:const PLATFORM = TILE_BY_KEY['platform']!;
152	src/world/gen/vanilla/HellFortPass.ts:14:const PLATFORM = TILE_BY_KEY['platform']!;
153	src/world/gen/vanilla/HellFortPass.ts:15:const TORCH = TILE_BY_KEY['torch']!;
154	src/world/gen/vanilla/IslandHousePass.ts:13:const CHEST = TILE_BY_KEY['chest']!;
155	src/world/gen/vanilla/JungleShrinePass.ts:26:const TORCH = TILE_BY_KEY['torch']!;
156	src/world/gen/vanilla/LivingTreePass.ts:25:const PLATFORM = TILE_BY_KEY['platform']!;
157	src/world/gen/vanilla/MicroBiomesPass.ts:258:        if (key.includes('chest') || key.includes('dresser')) return false; // IsAContainer 近似
158	src/world/gen/vanilla/MicroBiomesPass.ts:59:const CHEST = TILE_BY_KEY['chest']!;                       // 21(金箱 style 1 帧 36)
159	src/world/gen/vanilla/MicroBiomesPass.ts:90:  return key.includes('chest') || key.includes('dresser');
160	src/world/gen/vanilla/StructuresPass.ts:530:const TORCH = TILE_BY_KEY['torch']!;
161	src/world/gen/vanilla/TemplePass.ts:563:            ? { tile: TILE_BY_KEY['workbench']!, style: 10 }
162	src/world/gen/vanilla/TrapsPass.ts:25:const CHEST = TILE_BY_KEY['chest']!;
163	src/world/Housing.ts:41:  return key.includes('table') || key === 'workbench' || sheet === 14 || sheet === 18;
164	src/world/Torch.ts:88: *  /17（珊瑚 4384）；legacy 'torch' 与其余 → 0 */
165	src/world/Torch.ts:94:  if (key === 'torch') return 0;
166	tests/cavewalls.test.ts:46:    const CHAIR = TILE_BY_KEY['chair'], TABLE = TILE_BY_KEY['table'], WB = TILE_BY_KEY['workbench'];
167	tests/conveyor.test.ts:16:const PLATFORM = TILE_BY_KEY['platform']!;
168	tests/living-tree.test.ts:21:const CHEST = TILE_BY_KEY['chest']!;
169	tests/lunar-final-audit.test.ts:83:  const DIRT = 1, PLAT = TILE_BY_KEY['platform'], DOOR_C = TILE_BY_KEY['door_closed'],
170	tests/micro-biomes.test.ts:17:const CHEST = TILE_BY_KEY['chest']!;
171	tests/pot-break.test.ts:108:    const CHEST = TILE_BY_KEY['chest']!;
172	tests/pot-break.test.ts:74:    const CHEST = TILE_BY_KEY['chest']!;
173	tests/save.test.ts:26:    world.chests.push({ x: 5, y: 5, items: [{ id: ITEM_BY_KEY['torch'], stack: 3 }, null] });
174	tests/save.test.ts:29:    inv.add(ITEM_BY_KEY['dirt_block'], 77);
175	tests/shimmer.test.ts:127:    const key = 'coin_gold';
176	tests/shimmer.test.ts:138:    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY['torch'], 5);
177	tests/smart-cursor.test.ts:46:const torchItem = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['torch']], tool: null });
178	tests/smart-cursor.test.ts:47:const dirtItem = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['dirt_block']], tool: null });
179	tests/smart-cursor.test.ts:48:const platformItem = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['platform']], tool: null });
180	tests/tile-drop-null.test.ts:18:    expect(world.breakTileAt(32, 16)).toBe('dirt_block');
181	tests/wld-furnace-mapping.test.ts:21:    const F = TILE_BY_KEY['furnace']!, A = TILE_BY_KEY['anvil']!;
182	tests/wld-furnace-mapping.test.ts:26:        const nm = type[j] === F ? 'furnace' : type[j] === A ? 'anvil' : type[j] === 0 ? '.' : String(type[j]);
183	tests/world-difficulty.test.ts:68:    const torch = ITEM_BY_KEY['torch']!;
184	tests/world-difficulty.test.ts:80:    expect(dropped.some(([k, n]) => k === 'torch' && n === 30)).toBe(true);
185	

```


---

## 🤖 Assistant · 2026-08-12T15:52:36.702Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is group 1. Now group 2 (armor/tools/ores/bars etc.). Let me run the second grep. Also I need to filter better — e.g. `src/ui/UI.ts` "chest" where-clause is UI slot names, not item keys. I'll note these distinctions in the report.

Group 2 keys: copper_helmet, copper_chainmail, copper_greaves, iron_helmet, iron_chainmail, iron_greaves, silver_helmet, silver_chainmail, silver_greaves, gold_helmet, gold_chainmail, gold_greaves, wood_pickaxe, wood_axe, wood_sword, wood_hammer, copper_pickaxe, copper_axe, copper_sword, copper_hammer, iron_pickaxe, iron_axe, iron_sword, iron_hammer, silver_pickaxe, silver_axe, silver_sword, silver_hammer, gold_pickaxe, gold_axe, gold_sword, gold_hammer, tin_ore, lead_ore, tungsten_ore, platinum_ore, tin_bar, lead_bar, tungsten_bar, platinum_bar, demonite_ore, meteorite, hellstone, crimtane_ore, cobalt_ore, mythril_ore, adamantite_ore, palladium_ore, orichalcum_ore, titanium_ore, chlorophyte_ore, sapphire, ruby, emerald, topaz, amethyst, diamond, ice_block, ice_brick, snow_brick, sandstone_block, hardened_sand_block, desert_fossil, clay_block, glass, obsidian, gray_brick, red_brick, mud_block, silt_block, table, chair, bed, bookcase, grandfather_clock, piano, dresser, bench, bathtub, keg, cooking_pot, clay_pot, tombstone, life_crystal, candle, chandelier, lantern, candelabra, chinese_lantern, skull_lantern, water_candle, bomb, rope, empty_bucket, water_bucket, lava_bucket, honey_bucket.

Careful: 'glass','rope','bomb','bench','lantern','candle' etc. have substring issues but quoted so exact match ok.

Note some keys are both item key and tile key: wood, platform, torch, workbench, furnace, anvil, chest, door, glass, obsidian, table, chair, bed, bench, ice, clay... The user wants distinction: TILE_BY_KEY['torch'] tile vs ITEM_BY_KEY['torch'] item.

Let me run grep group 2.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:39.195Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "KEYS='copper_helmet|copper_chainmail|copper_greaves|iron_helmet|iron_chainmail|iron_greaves|silver_helmet|silver_chainmail|silver_greaves|gold_helmet|gold_chainmail|gold_greaves|wood_pickaxe|wood_axe|wood_sword|wood_hammer|copper_pickaxe|copper_axe|copper_sword|copper_hammer|iron_pickaxe|iron_axe|iron_sword|iron_hammer|silver_pickaxe|silver_axe|silver_sword|silver_hammer|gold_pickaxe|gold_axe|gold_sword|gold_hammer|tin_ore|lead_ore|tungsten_ore|platinum_ore|tin_bar|lead_bar|tungsten_bar|platinum_bar|demonite_ore|meteorite|hellstone|crimtane_ore|cobalt_ore|mythril_ore|adamantite_ore|palladium_ore|orichalcum_ore|titanium_ore|chlorophyte_ore|sapphire|ruby|emerald|topaz|amethyst|diamond|ice_block|ice_brick|snow_brick|sandstone_block|hardened_sand_block|desert_fossil|clay_block|glass|obsidian|gray_brick|red_brick|mud_block|silt_block|table|chair|bed|bookcase|grandfather_clock|piano|dresser|bench|bathtub|keg|cooking_pot|clay_pot|tombstone|life_crystal|candle|chandelier|lantern|candelabra|chinese_lantern|skull_lantern|water_candle|bomb|rope'; grep -rnE \"['\\\"\\`]($KEYS)['\\\"\\`]\" src tests tools --include=\"*.ts\" | grep -v \"^src/data/items.ts\" | grep -v \"^src/data/recipes.ts\" | grep -v \"idNames.generated\" | sort",
 "description": "Grep local item keys group 2"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:39.267Z

**📎 ToolResult**

```
src/core/Game.ts:1456:    const order = ['iron_helmet', 'iron_chainmail', 'iron_greaves'];
src/core/Game.ts:1645:    this.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
src/core/Game.ts:1646:    this.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
src/core/Game.ts:1647:    this.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
src/core/Game.ts:2313:      if (!w.store.inBounds(bx, by) || w.store.type[w.store.idx(bx, by)] !== (TILE_BY_KEY['bed'] ?? -1)) {
src/core/Game.ts:2558:    const heldWC = !!held2 && ITEM_DEFS[held2.id]?.key === 'water_candle';
src/core/Game.ts:2565:      const WCT = TILE_BY_KEY['water_candle'];
src/core/Game.ts:2579:      const LANTERN = TILE_BY_KEY['lantern'];
src/core/Game.ts:3085:      const isCandle = def.tile === 'candle';
src/core/Game.ts:3767:    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && (heldDef.key === 'life_crystal' || heldDef.key === 'vi_29_LifeCrystal')) {
src/core/Game.ts:390:  const starter = [VANILLA_ITEM_KEY_BY_ID[3507] ?? 'copper_sword',
src/core/Game.ts:391:    VANILLA_ITEM_KEY_BY_ID[3509] ?? 'copper_pickaxe', VANILLA_ITEM_KEY_BY_ID[3506] ?? 'copper_axe'];
src/core/Game.ts:5334:    if (itemDef.key === 'rope') {
src/core/Game.ts:5689:    } else if (type === TILE_BY_KEY['bed']) {
src/core/Game.ts:7460:        const bombKeys = new Set(['bomb', 'vi_166_bomb', 'vi_167_dynamite', 'vi_168_grenade',
src/data/tiles.ts:100:def({ key: 'gem_emerald', name: '翡翠矿', solid: true, opacity: 1, pick: 30, mapColor: '#389661', drop: 'emerald', vanilla: { sheet: 65, frame: 'auto' } });
src/data/tiles.ts:101:def({ key: 'gem_topaz', name: '黄玉矿', solid: true, opacity: 1, pick: 30, mapColor: '#A0763A', drop: 'topaz', vanilla: { sheet: 66, frame: 'auto' } });
src/data/tiles.ts:102:def({ key: 'gem_amethyst', name: '紫水晶矿', solid: true, opacity: 1, pick: 30, mapColor: '#8C3AA6', drop: 'amethyst', vanilla: { sheet: 67, frame: 'auto' } });
src/data/tiles.ts:103:def({ key: 'gem_diamond', name: '钻石矿', solid: true, opacity: 1, pick: 30, mapColor: '#7DBFC5', drop: 'diamond', vanilla: { sheet: 68, frame: 'auto' } });
src/data/tiles.ts:106:def({ key: 'ice', name: '冰块', solid: true, opacity: 1, pick: 0, mapColor: '#90C3E8', blend: true, drop: 'ice_block', vanilla: { sheet: 161, frame: 'auto' } });
src/data/tiles.ts:107:def({ key: 'thin_ice', name: '薄冰', solid: true, opacity: 1, pick: 0, mapColor: '#B8DBF0', blend: true, drop: 'ice_block', vanilla: { sheet: 162, frame: 'auto' } });
src/data/tiles.ts:108:def({ key: 'ice_brick', name: '冰砖', solid: true, opacity: 1, pick: 0, mapColor: '#7CAFC9', blend: true, drop: 'ice_brick', vanilla: { sheet: 206, frame: 'auto' } });
src/data/tiles.ts:109:def({ key: 'snow_brick', name: '雪砖', solid: true, opacity: 1, pick: 0, mapColor: '#D3ECF1', blend: true, drop: 'snow_brick', vanilla: { sheet: 148, frame: 'auto' } });
src/data/tiles.ts:112:def({ key: 'sandstone', name: '沙岩', solid: true, opacity: 1, pick: 0, mapColor: '#C67C4E', blend: true, drop: 'sandstone_block', vanilla: { sheet: 396, frame: 'auto' } });
src/data/tiles.ts:113:def({ key: 'hardened_sand', name: '硬化沙块', solid: true, opacity: 1, pick: 0, mapColor: '#D4C064', blend: true, drop: 'hardened_sand_block', vanilla: { sheet: 397, frame: 'auto' } });
src/data/tiles.ts:114:def({ key: 'desert_fossil', name: '沙漠化石', solid: true, opacity: 1, pick: 0, mapColor: '#D49458', blend: true, drop: 'desert_fossil', vanilla: { sheet: 404, frame: 'auto' } });
src/data/tiles.ts:115:def({ key: 'clay', name: '粘土块', solid: true, opacity: 1, pick: 0, mapColor: '#925144', blend: true, drop: 'clay_block', vanilla: { sheet: 40, frame: 'auto' } });
src/data/tiles.ts:116:def({ key: 'glass', name: '玻璃', solid: true, opacity: 0.15, pick: 0, mapColor: '#C8F6FE', drop: 'glass', vanilla: { sheet: 54, frame: 'auto' } });
src/data/tiles.ts:117:def({ key: 'obsidian', name: '黑曜石', solid: true, opacity: 1, pick: 55, mapColor: '#2B2854', blend: true, drop: 'obsidian', vanilla: { sheet: 56, frame: 'auto' } });
src/data/tiles.ts:118:def({ key: 'gray_brick', name: '灰砖', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: 'gray_brick', vanilla: { sheet: 38, frame: 'auto' } });
src/data/tiles.ts:119:def({ key: 'red_brick', name: '红砖', solid: true, opacity: 1, pick: 0, mapColor: '#B53E3B', blend: true, drop: 'red_brick', vanilla: { sheet: 39, frame: 'auto' } });
src/data/tiles.ts:120:def({ key: 'mud', name: '泥块', solid: true, opacity: 1, pick: 0, mapColor: '#5C4449', blend: true, drop: 'mud_block', vanilla: { sheet: 59, frame: 'blend' } });
src/data/tiles.ts:121:def({ key: 'silt', name: '淤泥块', solid: true, opacity: 1, pick: 0, mapColor: '#6A6B76', blend: true, drop: 'silt_block', vanilla: { sheet: 123, frame: 'auto' } });
src/data/tiles.ts:126:def({ key: 'table', name: '木桌', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'table', ...VAN(14, 3, 2) });
src/data/tiles.ts:127:def({ key: 'chair', name: '木椅', framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#BF8E6F', drop: 'chair', ...VAN(15, 1, 2) });
src/data/tiles.ts:128:def({ key: 'bed', name: '床', framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#BF8E6F', drop: 'bed', ...VAN(79, 4, 2) });
src/data/tiles.ts:129:def({ key: 'bookcase', name: '书架', framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#BF8E6F', drop: 'bookcase', ...VAN(101, 3, 4) });
src/data/tiles.ts:130:def({ key: 'grandfather_clock', name: '落地钟', framed: true, opacity: 0.05, pick: 0, w: 2, h: 5, mapColor: '#BF8E6F', drop: 'grandfather_clock', ...VAN(104, 2, 5) });
src/data/tiles.ts:131:def({ key: 'piano', name: '钢琴', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'piano', ...VAN(87, 3, 2) });
src/data/tiles.ts:132:def({ key: 'dresser', name: '梳妆台', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'dresser', ...VAN(88, 3, 2) });
src/data/tiles.ts:133:def({ key: 'bench', name: '长凳', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'bench', ...VAN(89, 3, 2) });
src/data/tiles.ts:134:def({ key: 'bathtub', name: '浴缸', framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#909490', drop: 'bathtub', ...VAN(90, 4, 2) });
src/data/tiles.ts:135:def({ key: 'keg', name: '酒桶', framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: 'keg', ...VAN(94, 2, 2) });
src/data/tiles.ts:136:def({ key: 'cooking_pot', name: '汤锅', framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: 'cooking_pot', ...VAN(96, 2, 2) });
src/data/tiles.ts:137:def({ key: 'clay_pot', name: '陶盆', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#796E61', drop: 'clay_pot', ...VAN(78, 1, 1) });
src/data/tiles.ts:138:def({ key: 'tombstone_v', name: '墓碑', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#C0C0C0', drop: 'tombstone', ...VAN(85, 2, 2) });
src/data/tiles.ts:139:def({ key: 'crystal_heart', name: '水晶之心', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#AE1845', drop: 'life_crystal', light: [255, 60, 90], ...VAN(12, 2, 2) });
src/data/tiles.ts:141:def({ key: 'candle', name: '蜡烛', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#FDDD03', drop: 'candle', light: [255, 185, 110], ...VAN(33, 1, 1) });
src/data/tiles.ts:142:def({ key: 'chandelier', name: '吊灯', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#EBA687', drop: 'chandelier', light: [255, 190, 120], ...VAN(34, 3, 3) });
src/data/tiles.ts:143:def({ key: 'lantern', name: '吊挂灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 2, mapColor: '#FBEB7F', drop: 'lantern', ...VAN(42, 1, 2) });
src/data/tiles.ts:145:def({ key: 'candelabra', name: '烛台', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: 'candelabra', light: [255, 185, 110], ...VAN(100, 2, 2) });
src/data/tiles.ts:146:def({ key: 'chinese_lantern', name: '中式灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FFA21F', drop: 'chinese_lantern', light: [255, 160, 70], ...VAN(95, 2, 2) });
src/data/tiles.ts:147:def({ key: 'skull_lantern', name: '骷髅灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: 'skull_lantern', light: [255, 160, 70], ...VAN(98, 2, 2) });
src/data/tiles.ts:148:def({ key: 'water_candle', name: '水蜡烛', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#2B8FFF', drop: 'water_candle', light: [140, 180, 255], ...VAN(49, 1, 1) });
src/data/tiles.ts:81:def({ key: 'ore_tin', name: '锡矿', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', drop: 'tin_ore', vanilla: { sheet: 166, frame: 'auto' } });
src/data/tiles.ts:82:def({ key: 'ore_lead', name: '铅矿', solid: true, opacity: 1, pick: 0, mapColor: '#3E5272', drop: 'lead_ore', vanilla: { sheet: 167, frame: 'auto' } });
src/data/tiles.ts:83:def({ key: 'ore_tungsten', name: '钨矿', solid: true, opacity: 1, pick: 20, mapColor: '#849D7F', drop: 'tungsten_ore', vanilla: { sheet: 168, frame: 'auto' } });
src/data/tiles.ts:84:def({ key: 'ore_platinum', name: '铂金矿', solid: true, opacity: 1, pick: 40, mapColor: '#98ABC6', drop: 'platinum_ore', vanilla: { sheet: 169, frame: 'auto' } });
src/data/tiles.ts:85:def({ key: 'ore_demonite', name: '魔矿', solid: true, opacity: 1, pick: 55, mapColor: '#625FA7', drop: 'demonite_ore', light: [255, 255, 153], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 22, frame: 'auto' } });
src/data/tiles.ts:86:def({ key: 'ore_meteorite', name: '陨石', solid: true, opacity: 1, pick: 50, mapColor: '#685654', drop: 'meteorite', light: [143, 110, 38], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 37, frame: 'auto' } });
src/data/tiles.ts:87:def({ key: 'ore_hellstone', name: '狱石', solid: true, opacity: 1, pick: 65, mapColor: '#8E4242', drop: 'hellstone', light: [255, 90, 40], vanilla: { sheet: 58, frame: 'auto' } });
src/data/tiles.ts:88:def({ key: 'ore_crimtane', name: '猩红矿', solid: true, opacity: 1, pick: 55, mapColor: '#7D3741', drop: 'crimtane_ore', light: [89, 0, 0], /* 原版 tileLighted 发光色（TileLightScanner ApplyTileLight 提取） */ vanilla: { sheet: 204, frame: 'auto' } });
src/data/tiles.ts:89:def({ key: 'ore_cobalt', name: '钴矿', solid: true, opacity: 1, pick: 100, mapColor: '#0B508F', drop: 'cobalt_ore', vanilla: { sheet: 107, frame: 'auto' } });
src/data/tiles.ts:90:def({ key: 'ore_mythril', name: '秘银矿', solid: true, opacity: 1, pick: 110, mapColor: '#5BA9A9', drop: 'mythril_ore', vanilla: { sheet: 108, frame: 'auto' } });
src/data/tiles.ts:91:def({ key: 'ore_adamantite', name: '精金矿', solid: true, opacity: 1, pick: 150, mapColor: '#801A34', drop: 'adamantite_ore', vanilla: { sheet: 111, frame: 'auto' } });
src/data/tiles.ts:92:def({ key: 'ore_palladium', name: '钯金矿', solid: true, opacity: 1, pick: 100, mapColor: '#EF5A32', drop: 'palladium_ore', vanilla: { sheet: 221, frame: 'auto' } });
src/data/tiles.ts:93:def({ key: 'ore_orichalcum', name: '山铜矿', solid: true, opacity: 1, pick: 110, mapColor: '#E760E4', drop: 'orichalcum_ore', vanilla: { sheet: 222, frame: 'auto' } });
src/data/tiles.ts:94:def({ key: 'ore_titanium', name: '钛矿', solid: true, opacity: 1, pick: 150, mapColor: '#395565', drop: 'titanium_ore', vanilla: { sheet: 223, frame: 'auto' } });
src/data/tiles.ts:95:def({ key: 'ore_chlorophyte', name: '叶绿矿', solid: true, opacity: 1, pick: 65, mapColor: '#BFE973', drop: 'chlorophyte_ore', vanilla: { sheet: 211, frame: 'auto' } });
src/data/tiles.ts:98:def({ key: 'gem_sapphire', name: '蓝宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#6E8CB6', drop: 'sapphire', vanilla: { sheet: 63, frame: 'auto' } });
src/data/tiles.ts:99:def({ key: 'gem_ruby', name: '红宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#C46072', drop: 'ruby', vanilla: { sheet: 64, frame: 'auto' } });
src/mainFlow.ts:320:      g.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
src/mainFlow.ts:321:      g.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
src/mainFlow.ts:322:      g.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
src/render/ChunkCache.ts:63:    this.truncatesWalls = ['glass', 'v_328_shadow_chest', 'v_459_', 'v_748_']
src/ui/UI.ts:2416:      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
src/ui/UI.ts:2493:      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
src/wld/WldImport.ts:133:  57: 'ash', 123: 'silt', 40: 'clay', 54: 'glass', 56: 'obsidian',
src/wld/WldImport.ts:134:  38: 'gray_brick', 39: 'red_brick',
src/wld/WldImport.ts:135:  161: 'ice', 162: 'thin_ice', 206: 'ice_brick', 148: 'snow_brick',
src/wld/WldImport.ts:136:  396: 'sandstone', 397: 'hardened_sand', 404: 'desert_fossil',
src/wld/WldImport.ts:144:  14: { key: 'table', copyFrame: true },
src/wld/WldImport.ts:145:  15: { key: 'chair', copyFrame: true },
src/wld/WldImport.ts:146:  79: { key: 'bed', copyFrame: true },
src/wld/WldImport.ts:147:  33: { key: 'candle', copyFrame: true },
src/wld/WldImport.ts:148:  34: { key: 'chandelier', copyFrame: true },
src/wld/WldImport.ts:149:  42: { key: 'lantern', copyFrame: true },
src/wld/WldImport.ts:150:  100: { key: 'candelabra', copyFrame: true },
src/wld/WldImport.ts:151:  101: { key: 'bookcase', copyFrame: true },
src/wld/WldImport.ts:152:  104: { key: 'grandfather_clock', copyFrame: true },
src/wld/WldImport.ts:153:  87: { key: 'piano', copyFrame: true },
src/wld/WldImport.ts:154:  88: { key: 'dresser', copyFrame: true },
src/wld/WldImport.ts:155:  89: { key: 'bench', copyFrame: true },
src/wld/WldImport.ts:156:  90: { key: 'bathtub', copyFrame: true },
src/wld/WldImport.ts:157:  94: { key: 'keg', copyFrame: true },
src/wld/WldImport.ts:158:  95: { key: 'chinese_lantern', copyFrame: true },
src/wld/WldImport.ts:159:  96: { key: 'cooking_pot', copyFrame: true },
src/wld/WldImport.ts:160:  98: { key: 'skull_lantern', copyFrame: true },
src/wld/WldImport.ts:161:  78: { key: 'clay_pot', copyFrame: true },
src/wld/WldImport.ts:164:  49: { key: 'water_candle', copyFrame: true },
src/wld/WldImport.ts:426:  699: 'tin_ore', 700: 'lead_ore', 701: 'tungsten_ore', 702: 'platinum_ore',
src/wld/WldImport.ts:427:  703: 'tin_bar', 704: 'lead_bar', 705: 'tungsten_bar', 706: 'platinum_bar',
src/wld/WldImport.ts:428:  177: 'sapphire', 178: 'ruby', 179: 'emerald', 180: 'topaz', 181: 'amethyst', 182: 'diamond',
src/wld/WldImport.ts:429:  664: 'ice_block', 883: 'ice_brick', 594: 'snow_brick',
src/wld/WldImport.ts:430:  133: 'clay_block', 170: 'glass', 173: 'obsidian', 129: 'gray_brick', 131: 'red_brick',
src/wld/WldImport.ts:431:  32: 'table', 34: 'chair', 224: 'bed', 354: 'bookcase', 359: 'grandfather_clock',
src/wld/WldImport.ts:432:  105: 'candle', 136: 'lantern', 349: 'candelabra', 222: 'clay_pot', 29: 'life_crystal',
src/world/gen/vanilla/CaveHousePass.ts:415:    [def.tables2 ? 'v_469_tables_group_2' : 'table', def.table],
src/world/gen/vanilla/CaveHousePass.ts:419:    ['piano', def.piano],
src/world/gen/vanilla/CaveHousePass.ts:420:    ['keg', 0],
src/world/gen/vanilla/CaveHousePass.ts:421:    ['bookcase', def.bookcase],
src/world/gen/vanilla/CaveHousePass.ts:437:      placeFurniture(st, 'candelabra', x, y, rng.int(0, 5), 'top');
src/world/gen/vanilla/CaveHousePass.ts:45:const CANDELABRA = TILE_BY_KEY['candelabra']!;
src/world/gen/vanilla/DesertPass.ts:136:const FOSSIL = TILE_BY_KEY['desert_fossil']!;
src/world/gen/vanilla/DungeonPass.ts:29:const TABLE = TILE_BY_KEY['table']!;
src/world/gen/vanilla/DungeonPass.ts:30:const CHAIR = TILE_BY_KEY['chair']!;
src/world/gen/vanilla/DungeonPass.ts:31:const CANDLE = TILE_BY_KEY['candle']!;
src/world/gen/vanilla/DungeonPass.ts:33:const LANTERN = TILE_BY_KEY['lantern']!;
src/world/gen/vanilla/DungeonPass.ts:34:const CHANDELIER = TILE_BY_KEY['chandelier']!;
src/world/gen/vanilla/DungeonPass.ts:35:const WATER_CANDLE = TILE_BY_KEY['water_candle']!;
src/world/gen/vanilla/DungeonPass.ts:39:const CANDELABRA = TILE_BY_KEY['candelabra']!;
src/world/gen/vanilla/DungeonPass.ts:40:const PIANO = TILE_BY_KEY['piano']!;
src/world/gen/vanilla/DungeonPass.ts:41:const DRESSER = TILE_BY_KEY['dresser']!;
src/world/gen/vanilla/DungeonPass.ts:42:const BENCH = TILE_BY_KEY['bench']!;
src/world/gen/vanilla/DungeonPass.ts:43:const BATHTUB = TILE_BY_KEY['bathtub']!;
src/world/gen/vanilla/DungeonPass.ts:44:const BED = TILE_BY_KEY['bed']!;
src/world/gen/vanilla/DungeonPass.ts:46:const CLOCK = TILE_BY_KEY['grandfather_clock']!;
src/world/gen/vanilla/DungeonPass.ts:47:const BOOKCASE = TILE_BY_KEY['bookcase']!;
src/world/gen/vanilla/IslandHousePass.ts:14:const TABLE = TILE_BY_KEY['table']!;
src/world/gen/vanilla/IslandHousePass.ts:15:const CHAIR = TILE_BY_KEY['chair']!;
src/world/gen/vanilla/LivingTreePass.ts:26:const CHAIR = TILE_BY_KEY['chair']!;
src/world/gen/vanilla/MicroBiomesPass.ts:258:        if (key.includes('chest') || key.includes('dresser')) return false; // IsAContainer 近似
src/world/gen/vanilla/MicroBiomesPass.ts:38:const FOSSIL = TILE_BY_KEY['desert_fossil']!;
src/world/gen/vanilla/MicroBiomesPass.ts:90:  return key.includes('chest') || key.includes('dresser');
src/world/gen/vanilla/TemplePass.ts:565:              ? { tile: TILE_BY_KEY['table']!, style: 9 }
src/world/gen/vanilla/TemplePass.ts:566:              : { tile: TILE_BY_KEY['chair']!, style: 12 };
src/world/Housing.ts:41:  return key.includes('table') || key === 'workbench' || sheet === 14 || sheet === 18;
src/world/Housing.ts:45:  return key.includes('chair') || key.includes('throne') || sheet === 15 || sheet === 21;
src/world/liquid/LiquidSim.ts:33:const OBSIDIAN = TILE_BY_KEY['obsidian'];
src/world/spawn/VanillaSpawner.ts:57:    SANDSTONE: get('sandstone'), FOSSIL: get('desert_fossil'),
src/world/spawn/VanillaSpawner.ts:61:    CACTUS: get('v_80_cactus'), SNOW_BRICK: get('snow_brick'), CATTAIL: get('v_519_cattails'),
tests/cavewalls.test.ts:46:    const CHAIR = TILE_BY_KEY['chair'], TABLE = TILE_BY_KEY['table'], WB = TILE_BY_KEY['workbench'];
tests/explosion.test.ts:25:    place(world, 'obsidian', 21, 20);
tests/explosion.test.ts:27:    expect(can(world, 'obsidian', 21, 20)).toBe(true);
tests/fireworks.test.ts:222:    placeToilet(w, 'chair', 40, 50, 20); // 椅表马桶（黄金马桶带）
tests/fireworks.test.ts:235:    placeToilet(w, 'chair', 44, 50, 0);
tests/item-coverage.test.ts:37:    expect(Lang.itemNameByKey('copper_pickaxe')).toBe('铜镐');
tests/mining.test.ts:46:    expect_('copper_pickaxe', 'pick', 35, 4, 15);   // 3509
tests/mining.test.ts:47:    expect_('copper_axe', 'axe', 7, 3, 21);          // 3506
tests/mining.test.ts:48:    expect_('iron_pickaxe', 'pick', 40, 5, 13);       // 1
tests/mining.test.ts:49:    expect_('iron_axe', 'axe', 9, 5, 19);             // 10
tests/mining.test.ts:50:    expect_('silver_pickaxe', 'pick', 45, 6, 11);     // 3515
tests/mining.test.ts:51:    expect_('silver_axe', 'axe', 10, 6, 18);          // 3512
tests/mining.test.ts:52:    expect_('gold_pickaxe', 'pick', 55, 6, 17);       // 3521
tests/mining.test.ts:53:    expect_('gold_axe', 'axe', 11, 7, 18);            // 3518
tests/mining.test.ts:54:    expect_('wood_hammer', 'hammer', 25, 2, 25);      // 196
tests/smart-cursor.test.ts:287:    const dual = { ...ITEM_DEFS[ITEM_BY_KEY['copper_pickaxe']], key: 'test_drax', axePower: 100 };
tests/smart-cursor.test.ts:43:const pick = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['copper_pickaxe']], tool: { type: 'pick' as const, power: 35 } });
tests/smart-cursor.test.ts:44:const axe = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['copper_axe']], tool: { type: 'axe' as const, power: 7 } });
tests/smart-cursor.test.ts:45:const hammer = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['wood_hammer']], tool: { type: 'hammer' as const, power: 25 } });
tests/vanilla-recipes.test.ts:96:    expect(RECIPES.filter((r) => r.out === 'wood_hammer')).toHaveLength(1);
tests/world-difficulty.test.ts:69:    const pick = ITEM_BY_KEY['copper_pickaxe']!;
tests/world-difficulty.test.ts:81:    expect(dropped.some(([k, n]) => k === 'copper_pickaxe' && n === 1)).toBe(true);

```


---

## 🤖 Assistant · 2026-08-12T15:52:42.912Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now group 3: potions, buckets, tools (tin/lead etc), bows, magic, boss summons, wire tools, seeds, minecart, etc.

Keys: empty_bucket water_bucket lava_bucket honey_bucket tin_pickaxe tin_axe tin_sword lead_pickaxe lead_axe lead_sword tungsten_pickaxe tungsten_axe tungsten_sword platinum_pickaxe platinum_axe platinum_sword wooden_bow wooden_arrow flaming_arrow iron_bow minecart_item wand_of_sparking amethyst_bolt worm_food bloody_spine slime_crown mechanical_worm mechanical_eye mechanical_skull wire red_wrench blue_wrench green_wrench yellow_wrench wire_cutter actuator_item actuation_rod multicolor_wrench grand_design goblin_battle_standard snow_globe pirate_map corrupt_grass_seeds crimson_grass_seeds jungle_grass_seeds mushroom_grass_seeds heal_potion agility_potion ironskin_potion thorns_potion regen_potion obsidian_skin_potion gills_potion mana_regen_potion magic_power_potion featherfall_potion water_walking_potion archery_potion night_owl_potion lucky_horseshoe feral_claws

Some already covered. Let me grep the remaining.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:44.527Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "KEYS='empty_bucket|water_bucket|lava_bucket|honey_bucket|tin_pickaxe|tin_axe|tin_sword|lead_pickaxe|lead_axe|lead_sword|tungsten_pickaxe|tungsten_axe|tungsten_sword|platinum_pickaxe|platinum_axe|platinum_sword|wooden_bow|wooden_arrow|flaming_arrow|iron_bow|minecart_item|wand_of_sparking|amethyst_bolt|worm_food|bloody_spine|slime_crown|mechanical_worm|mechanical_eye|mechanical_skull|red_wrench|blue_wrench|green_wrench|yellow_wrench|wire_cutter|actuator_item|actuation_rod|multicolor_wrench|grand_design|goblin_battle_standard|snow_globe|pirate_map|corrupt_grass_seeds|crimson_grass_seeds|jungle_grass_seeds|mushroom_grass_seeds'; grep -rnE \"['\\\"\\`]($KEYS)['\\\"\\`]\" src tests tools --include=\"*.ts\" | grep -v \"^src/data/items.ts\" | grep -v \"^src/data/recipes.ts\" | grep -v \"idNames.generated\" | sort",
 "description": "Grep local item keys group 3"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:44.577Z

**📎 ToolResult**

```
src/core/Game.ts:1083:    if (key === 'minecart_item') return DEFAULT_CART_TEXTURE;
src/core/Game.ts:1320:        if (held && ITEM_DEFS[held.id]?.wireTool && (ITEM_DEFS[held.id]?.key === 'multicolor_wrench' || ITEM_DEFS[held.id]?.key === 'grand_design')) {
src/core/Game.ts:3964:    } else if (heldDef && (heldDef.key === 'worm_food' || heldDef.key === 'bloody_spine' || heldDef.key === 'slime_crown')
src/core/Game.ts:3967:      if (heldDef.key === 'worm_food') this.summonBoss('eater_of_worlds_head');
src/core/Game.ts:3968:      else if (heldDef.key === 'bloody_spine') this.summonBoss('brain_of_cthulhu');
src/core/Game.ts:3974:    } else if (heldDef && (heldDef.key === 'mechanical_worm' || heldDef.key === 'mechanical_eye' || heldDef.key === 'mechanical_skull')
src/core/Game.ts:3982:        if (heldDef.key === 'mechanical_worm') this.summonBoss('destroyer');
src/core/Game.ts:3983:        else if (heldDef.key === 'mechanical_eye') this.summonBoss('twins');
src/core/Game.ts:4004:    } else if (heldDef && (heldDef.key === 'goblin_battle_standard' || heldDef.key === 'snow_globe' || heldDef.key === 'pirate_map')
src/core/Game.ts:4008:      const type = heldDef.key === 'goblin_battle_standard' ? INVASION_GOBLIN
src/core/Game.ts:4009:        : heldDef.key === 'snow_globe' ? INVASION_SNOW_LEGION : INVASION_PIRATE;
src/core/Game.ts:4062:    } else if (heldDef && (heldDef.key === 'empty_bucket' || heldDef.key === 'water_bucket'
src/core/Game.ts:4063:      || heldDef.key === 'lava_bucket' || heldDef.key === 'honey_bucket')) {
src/core/Game.ts:4856:                ? (roll.nextInt(40) === 0 ? 'mushroom_grass_seeds'
src/core/Game.ts:5079:        const key = roll.nextInt(40) === 0 ? 'mushroom_grass_seeds'
src/core/Game.ts:5178:      const actuators = mode & TOOL_CUTTER ? 9999 : inv.countOf(ITEM_BY_KEY['actuator_item'] ?? -1);
src/core/Game.ts:5182:        if (res.actuator > 0) inv.remove(ITEM_BY_KEY['actuator_item'] ?? -1, res.actuator);
src/core/Game.ts:5190:    const mode = itemDef.key === 'multicolor_wrench' ? this.wireToolMode : (wt.place ?? 0);
src/core/Game.ts:5210:    const actHave = inv.countOf(ITEM_BY_KEY['actuator_item'] ?? -1);
src/core/Game.ts:5222:      if (needActuator > 0) inv.remove(ITEM_BY_KEY['actuator_item'] ?? -1, needActuator);
src/core/Game.ts:6872:    if (key === 'empty_bucket') {
src/core/Game.ts:6902:      swap(t === 2 ? 'lava_bucket' : t === 3 ? 'honey_bucket' : 'water_bucket');
src/core/Game.ts:6913:      swap('empty_bucket');
src/player/SmartCursor.ts:1493:    const isBucket = vid === 205 || env.held.def?.key === 'empty_bucket';
src/player/SmartCursor.ts:1523:    const isActuatorItem = sem.vid === 849 || env.held.def?.key === 'actuator_item';
src/ui/UI.ts:2414:      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
src/ui/UI.ts:2492:      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
tests/arrow-tree-pass.test.ts:31:    const arrow = new Arrow(32 * 16 - 12, 16 * 16 + 3, 6, 0, 10, 0, 1, 'wooden_arrow');
tests/arrow-tree-pass.test.ts:43:    const arrow = new Arrow(32 * 16 - 12, 16 * 16 + 3, 6, 0, 10, 0, 1, 'wooden_arrow');
tests/hostile-proj-player-hit.test.ts:73:    const arrow = new Arrow(30 * 16 - 40, 10 * 16 + 8, 8, 0, 9, 1, 1, 'wooden_arrow');
tests/proj-critter-hit.test.ts:32:    const arrow = new Arrow(40 * 16 - 20, 20 * 16 + 4, 8, 0, 9, 1, 1, 'wooden_arrow');
tests/proj-critter-hit.test.ts:51:    const arrow = new Arrow(40 * 16 - 20, 23 * 16, 8, 0, 9, 1, 1, 'wooden_arrow');
tests/projectile-reflect.test.ts:109:    const arrow = new Arrow(20 * 16 - 12, 10 * 16, 8, 0, 40, 0, 1, 'wooden_arrow', { grav: 0 });
tests/projectile-reflect.test.ts:132:    const arrow = new Arrow(20 * 16 - 12, 10 * 16, 8, 0, 40, 0, 1, 'wooden_arrow', { grav: 0 });
tests/projectile-reflect.test.ts:74:    const arrow = new Arrow(20 * 16 - 12, 10 * 16, 8, 0, 40, 0, 1, 'wooden_arrow', { grav: 0 });
tests/projectile-reflect.test.ts:92:    const arrow = new Arrow(20 * 16 - 12, 10 * 16, 8, 0, 40, 0, 1, 'wooden_arrow', { grav: 0 });
tests/smart-cursor.test.ts:278:    const target = run(mkEnv(st, mouseAt(104, 97), { def: ITEM_DEFS[ITEM_BY_KEY['empty_bucket']], tool: null }));
tests/thrown-weapons.test.ts:46:    const arrow = ITEM_DEFS[ITEM_BY_KEY['wooden_arrow']];
tests/vi-weapons.test.ts:63:    expect(combatWeapon({ key: 'wooden_bow', vid: 39 })).toBeNull();

```


---

## 🤖 Assistant · 2026-08-12T15:52:45.634Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "KEYS='heal_potion|agility_potion|ironskin_potion|thorns_potion|regen_potion|obsidian_skin_potion|gills_potion|mana_regen_potion|magic_power_potion|featherfall_potion|water_walking_potion|archery_potion|night_owl_potion|lucky_horseshoe|feral_claws|^wire$|dye'; grep -rnE \"['\\\"\\`]($KEYS)['\\\"\\`]\" src tests tools --include=\"*.ts\" | grep -v \"^src/data/items.ts\" | grep -v \"^src/data/recipes.ts\" | grep -v \"idNames.generated\" | sort",
 "description": "Grep potion and accessory keys"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:45.691Z

**📎 ToolResult**

```
src/data/vanillaEquip.ts:40:  return KIND_BY_IID.get(id) === 'dye';
src/data/vanillaEquip.ts:8:export type EquipKind = 'dye' | 'pet' | 'light' | 'mount' | 'cart' | 'hook';
src/entities/Player.ts:186:      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
src/entities/Player.ts:193:      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
src/ui/UI.ts:1594:    this.eqPageEl.appendChild(vcol2(Lang.text('LegacyInterface.57'), 0, 3, 3, 7, 'dye'));            // 染料 dye[0-2]+[3-9]
src/ui/UI.ts:1930:    if (where === 'armor' || where === 'dye') {
src/ui/UI.ts:1933:      tint = where === 'dye' ? lo[2] : i <= 9 ? lo[0] : lo[1];
src/ui/UI.ts:197:    if (where === 'dye') return this.game.player.inv.dye[i];
src/ui/UI.ts:2094:    for (const where of ['armor', 'dye', 'misc', 'miscDye'] as const) {
src/ui/UI.ts:22:type SlotWhere = 'inv' | 'chest' | 'armor' | 'dye' | 'misc' | 'miscDye';
src/ui/UI.ts:2412:      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
src/ui/UI.ts:2413:      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
src/ui/UI.ts:2414:      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
src/ui/UI.ts:2418:      [BuffType.ObsidianSkin, 'obsidian_skin_potion'], [BuffType.Gills, 'gills_potion'],
src/ui/UI.ts:2419:      [BuffType.ManaRegen, 'mana_regen_potion'], [BuffType.MagicPower, 'magic_power_potion'],
src/ui/UI.ts:2420:      [BuffType.Featherfall, 'featherfall_potion'], [BuffType.WaterWalking, 'water_walking_potion'],
src/ui/UI.ts:2421:      [BuffType.Archery, 'archery_potion'], [BuffType.NightOwl, 'night_owl_potion'],
src/ui/UI.ts:2490:      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
src/ui/UI.ts:2491:      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
src/ui/UI.ts:2492:      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
src/ui/UI.ts:2495:      [BuffType.ObsidianSkin, 'obsidian_skin_potion'], [BuffType.Gills, 'gills_potion'],
src/ui/UI.ts:2496:      [BuffType.ManaRegen, 'mana_regen_potion'], [BuffType.MagicPower, 'magic_power_potion'],
src/ui/UI.ts:2497:      [BuffType.Featherfall, 'featherfall_potion'], [BuffType.WaterWalking, 'water_walking_potion'],
src/ui/UI.ts:2498:      [BuffType.Archery, 'archery_potion'], [BuffType.NightOwl, 'night_owl_potion'],
src/ui/UI.ts:665:    return k === 'dye' || k === 'pet' || k === 'light' || k === 'cart' || k === 'mount' || k === 'hook';
src/ui/UI.ts:689:      if (kind === 'dye') {
src/ui/UI.ts:694:        targetWhere = 'dye';
src/ui/UI.ts:703:    const arr = targetWhere === 'armor' ? inv.armor : targetWhere === 'dye' ? inv.dye : inv.miscEquips;
src/ui/UI.ts:708:    else if (where === 'dye') inv.dye[i] = tmp ?? null;
src/ui/UI.ts:718:    if (where === 'armor' || where === 'dye' || where === 'misc' || where === 'miscDye') {
src/ui/UI.ts:821:    else if (where === 'dye') this.game.player.inv.dye[i] = null;
src/ui/UI.ts:837:    else if (where === 'armor' || where === 'dye' || where === 'misc' || where === 'miscDye') {
src/ui/UI.ts:854:    if (where === 'dye') return inv.dye;
src/ui/UI.ts:862:    if (where === 'armor' || where === 'dye' || where === 'misc' || where === 'miscDye') {
src/ui/UI.ts:867:      if (where === 'dye' && !inv.dyeAccepts(this.heldStack.id)) return;
tests/p5-equip-prefix-loadout.test.ts:20:    expect(equipKindOfVid(1007)).toBe('dye');
tests/p5-equip-prefix-loadout.test.ts:21:    expect(equipKindOfVid(1031)).toBe('dye');
tests/p5-equip-prefix-loadout.test.ts:22:    expect(equipKindOfVid(2877)).toBe('dye');

```


---

## 🤖 Assistant · 2026-08-12T15:52:48.080Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to look at specific areas. Let me look at the key files in parallel:

1. UI.refreshCrafting (UI.ts around 1401 and 2133)
2. Game.canCraft/craft/stationsNearby (Game.ts ~9670)
3. Save serialize.ts / SaveFile.ts / CharacterStore.ts
4. net/protocol.ts item sync
5. SpriteAtlas atlasIconForKey / VANILLA_ITEM_ICON_MAP
6. placeTile / SmartSelect
7. vanillaItemStats/vanillaItemCombat

Let me read these.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:48.647Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1370,1480p' ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts; echo \"====2100-2230\"; sed -n '2100,2230p' ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "description": "Read UI crafting sections"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:48.698Z

**📎 ToolResult**

```
      for (const e of entries) {
        if (q && !e.lc.includes(q)) continue;
        if (++shown > 40) break;
        const chip = el('div');
        chip.title = e.name;
        chip.style.cssText = 'display:flex; align-items:center; gap:3px; width:150px; padding:2px 4px; background:#1f1f28; border:1px solid #444; border-radius:3px; cursor:pointer; font-size:12px; color:#ddd;';
        const img = el('img') as HTMLImageElement;
        img.src = iconUrl(this.game!, e.id);
        img.style.cssText = 'width:22px; height:22px; image-rendering:pixelated; flex:none;';
        chip.appendChild(img);
        const lbl = el('span');
        lbl.textContent = e.name;
        lbl.style.cssText = 'overflow:hidden; text-overflow:ellipsis; white-space:nowrap;';
        chip.appendChild(lbl);
        chip.addEventListener('click', () => this.renderGuideRecipes(recipeList, e.vid));
        itemRow.appendChild(chip);
      }
      if (!shown) itemRow.appendChild(el('div', 'sw-lbl', '无匹配'));
    };
    input.addEventListener('input', renderItems);
    renderItems();
    input.focus();
  }

  /** 材料的配方列表（CollectGuideRecipes：items 直接命中或 RecipeGroup 成员命中） */
  private renderGuideRecipes(listEl: HTMLElement, vid: number): void {
    listEl.textContent = '';
    const game = this.game;
    const avail = new Map<unknown, number>();
    for (const { r, count } of game.vanillaAvailableRecipes()) avail.set(r, count);
    let hits = 0;
    for (const r of VANILLA_RECIPES) {
      const used = r.items.some((req) => req.id === vid
        || (req.id >= 1000000 && (RECIPE_GROUP_ITEMS[String(req.id - 1000000)] ?? []).includes(vid)));
      if (!used) continue;
      if (++hits > 60) { listEl.appendChild(el('div', 'sw-lbl', '…更多结果请细化')); break; }
      const outKey = vanillaItemKey(r.create);
      if (!outKey) continue;
      const row = el('div', 'sw-recipe' + (avail.has(r) ? '' : ' no'));
      const img = el('img') as HTMLImageElement;
      img.src = iconUrl(game, game.itemId(outKey));
      row.appendChild(img);
      const label = el('span', '', `${Lang.itemNameByKey(outKey)}${r.createStack > 1 ? ` ×${r.createStack}` : ''}`);
      row.appendChild(label);
      const info = el('span', '', `${r.tile >= 0 ? (Lang.tileName(r.tile) ?? `站点 ${r.tile}`) : Lang.text('Mods.SandboxWorld.UI.StationHand')} · ${
        r.items.map((req) => `${req.id >= 1000000 ? '任何组物' : (Lang.itemNameByKey(ingredientKey(req.id) ?? '') ?? req.id)} ${req.stack}`).join(' +')}`);
      info.style.cssText = 'margin-left:auto; color:#9a8ab8; font-size:11px; text-align:right; max-width:280px;';
      row.appendChild(info);
      if (avail.has(r)) {
        row.onclick = () => {
          game.vanillaCraft(r, 1);
          this.refreshAll();
        };
      }
      listEl.appendChild(row);
    }
    if (!hits) listEl.appendChild(el('div', 'sw-lbl', '该物品不用于任何配方'));
  }

  closeGuideSearch(): void {
    if (this.guideEl) {
      this.guideEl.remove();
      this.guideEl = null;
    }
  }

  /** 垃圾桶暂存（关闭背包才删除；可取回） */
  /** @deprecated 改走 inv.trash 持久槽（Player.trashItem 语义）——保留字段仅作 UI 缓存兼容 */

  private placeTrash(): void {
    if (!this.heldStack) return;
    const t = this.game.player.inv.trash;
    if (!t) {
      this.game.player.inv.trash = this.heldStack;
      this.heldStack = null;
    } else if (t.id === this.heldStack.id) {
      const max = ITEM_DEFS[t.id].maxStack;
      const put = Math.min(max - t.stack, this.heldStack.stack);
      t.stack += put;
      this.heldStack.stack -= put;
      if (this.heldStack.stack <= 0) this.heldStack = null;
    } else {
      this.game.player.inv.trash = this.heldStack; // 交换：可把误放的东西取回
      this.heldStack = t;
    }
    this.paintTrash();
  }

  private paintTrash() {
    if (!this.trashEl) return;
    const img = this.trashEl.querySelector('img');
    const cnt = this.trashEl.querySelector('.cnt');
    img?.remove();
    cnt?.remove();
    if (this.game.player.inv.trash) {
      const im = el('img') as HTMLImageElement;
      im.src = iconUrl(this.game, this.game.player.inv.trash!.id);
      im.draggable = false;
      this.trashEl.appendChild(im);
      if (this.game.player.inv.trash!.stack > 1) {
        this.trashEl.appendChild(el('span', 'cnt', String(this.game.player.inv.trash!.stack)));
      }
    }
  }

  trashEl: HTMLElement | null = null;
  /** 装备/杂项页签与 Loadout 按钮（背包面板顶部） */
  private eqPageEl: HTMLElement | null = null;
  private miscPageEl: HTMLElement | null = null;
  private loadoutBtns: HTMLButtonElement[] = [];
  private eqPageBtns: HTMLButtonElement[] = [];
====2100-2230
          this.paintSlotChrome(slotEl, where, i);
        }
      }
    }
    // Loadout 按钮（Extra[259] 图集：选中=列1；悬停态由 mouseenter/leave 管）
    this.loadoutBtns.forEach((b, k) => {
      const cur = k === inv.currentLoadout;
      b.style.backgroundPosition = `${(cur ? 1 : 0) * 50}% ${k * 50}%`;
    });
    this.refreshBuffs();
    if (this.openChest) {
      const n = Math.min(40, this.openChest.items.length);
      for (let i = 0; i < n; i++) {
        const slotEl = this.slotEl(i, 'chest');
        if (slotEl) {
          this.paintSlot(slotEl, this.openChest.items[i]);
          this.paintSlotChrome(slotEl, 'chest', i);
        }
      }
    }
    this.refreshCrafting();
  }

  private refreshCrafting() {
    const game = this.game;
    if (!game || !this.craftListEl) return;
    const stations = game.stationsNearby();
    const stationsEl = this.invPanel.querySelector('[data-role="stations"]') as HTMLElement;
    if (stationsEl) {
      const stName: Record<string, string> = { hand: Lang.text('Mods.SandboxWorld.UI.StationHand'), workbench: '🛠 ' + Lang.text('ItemName.WorkBench'), furnace: '🔥 ' + Lang.text('ItemName.Furnace'), anvil: '⚒ ' + Lang.text('ItemName.IronAnvil') };
      stationsEl.textContent = Lang.text('Mods.SandboxWorld.UI.CraftStations', [...stations].map((s) => stName[s] ?? s).join('、'));
    }
    this.craftListEl.innerHTML = '';
    for (const r of RECIPES) {
      if (!stations.has(r.station)) continue;
      const ok = game.canCraft(r);
      const row = el('div', 'sw-recipe' + (ok ? '' : ' no'));
      const outDef = ITEM_DEFS[game.itemId(r.out)];
      const img = el('img') as HTMLImageElement;
      img.src = iconUrl(game, game.itemId(r.out));
      row.appendChild(img);
      const label = el('span', '', `${Lang.itemNameByKey(outDef.key)}${r.count > 1 ? ` ×${r.count}` : ''}`);
      row.appendChild(label);
      const mats = el('span', '', r.inputs.map(([k, n]) => {
        const have = game.player.inv.countOf(game.itemId(k));
        return ` ${Lang.itemNameByKey(ITEM_DEFS[game.itemId(k)].key)} ${have}/${n}`;
      }).join(' ·'));
      mats.style.cssText = 'margin-left:auto; color:#9a8ab8; font-size:11px; text-align:right;';
      row.appendChild(mats);
      if (ok) {
        row.onclick = () => {
          game.craft(r);
          this.refreshAll();
        };
      }
      this.craftListEl.appendChild(row);
    }
    // ---- 原版配方（2688 条，Recipe.UpdateRecipeList 主干：环境+材料双门） ----
    this.refreshVanillaCrafting();
  }

  /** 鱼眼合成列表焦点行（原版 focusRecipe；滚轮 ±1，CraftingUI 滚动 ±6.5/帧） */
  private craftFocus = 0;
  /** Modern 合成网格：搜索栏 + 焦点配方材料格（1.4.5 CraftingGrid 语义） */
  private craftSearchEl: HTMLInputElement | null = null;
  private craftGridEl: HTMLElement | null = null;
  /** 材料格已存（原版 vid → 数量；焦点配方切换/关面板时归还背包） */
  private craftGrid = new Map<number, number>();
  private craftGridRecipe: VanillaRecipeLike | null = null;
  /** 原版配方列表（数据驱动 1456 全量；鱼眼缩放 = 100/(|Δ|+100) 下限 0.75，CraftingUI.cs:184-192 DOM 近似） */
  private refreshVanillaCrafting(): void {
    const game = this.game;
    if (!game || !this.craftListEl) return;
    let avail = game.vanillaAvailableRecipes();
    if (!avail.length) return;
    // 搜索过滤（Modern 网格搜索栏：按成品名过滤）
    const q = this.craftSearchEl?.value.trim().toLowerCase() ?? '';
    if (q) {
      const filtered = avail.filter(({ r }) => {
        const k = vanillaItemKey(r.create);
        const name = k ? Lang.itemNameByKey(k) : '';
        return name.toLowerCase().includes(q);
      });
      if (filtered.length) avail = filtered;
    }
    const head = el('div', 'sw-lbl', '── 原版配方 ──');
    this.craftListEl.appendChild(head);
    const MAX_ROWS = 60; // 焦点 ±30（超出原版 middleY 视口即 alpha→0 :177）
    const start = Math.max(0, Math.min(this.craftFocus - 30, avail.length - MAX_ROWS));
    if (this.craftFocus >= avail.length) this.craftFocus = 0;
    for (let idx = start; idx < Math.min(avail.length, start + MAX_ROWS); idx++) {
      const { r, count } = avail[idx];
      const dy = idx - this.craftFocus; // 相对焦点的连续偏移（原版 availableRecipeY）
      const scale = Math.max(0.75, 100 / (Math.abs(dy) + 100));
      const outKey = vanillaItemKey(r.create);
      if (!outKey) continue;
      const row = el('div', 'sw-recipe');
      row.style.cssText += ` transform:scale(${scale.toFixed(3)}); transform-origin:left center; opacity:${(1 - Math.min(0.75, Math.abs(dy) / 30)).toFixed(2)}; transition:transform 0.08s;`;
      const img = el('img') as HTMLImageElement;
      img.src = iconUrl(game, game.itemId(outKey));
      row.appendChild(img);
      const label = el('span', '', `${Lang.itemNameByKey(outKey)}${r.createStack > 1 ? ` ×${r.createStack}` : ''} ×${count}`);
      row.appendChild(label);
      const mats = el('span', '', r.items.map((req) => {
        const k = ingredientKey(req.id);
        if (!k) return ` ? ${req.stack}`;
        const have = game.player.inv.countOf(game.itemId(k));
        return ` ${Lang.itemNameByKey(k)} ${Math.min(have, req.stack)}/${req.stack}`;
      }).join(' ·'));
      mats.style.cssText = 'margin-left:auto; color:#9a8ab8; font-size:11px; text-align:right;';
      row.appendChild(mats);
      row.addEventListener('mousedown', (ev) => {
        ev.stopPropagation();
        this.craftFocus = idx; // 选中置焦（原版 focusRecipe=i）
        game.vanillaCraft(r, (ev as MouseEvent).shiftKey ? 10 : 1);
        this.refreshAll();
      });
      this.craftListEl.appendChild(row);
    }
    // 滚轮：焦点 ±1（原版 ScrollCraftingList；±6.5/帧的平滑由 transition 兜）
    if (!this._craftWheelBound) {
      this._craftWheelBound = true;
      this.craftListEl.addEventListener('wheel', (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        this.craftFocus = Math.max(0, this.craftFocus + (ev.deltaY > 0 ? 1 : -1));
        this.refreshAll();
      }, { passive: false });
    }
    // Modern 合成网格材料格（焦点配方）
    this.refreshCraftGrid(avail);

```


---

## 🤖 Assistant · 2026-08-12T15:52:48.985Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '9640,9720p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read Game canCraft/craft/stationsNearby"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:49.024Z

**📎 ToolResult**

```
      const life = Math.round(base * (0.6 + Math.random() * 0.4));
      this.particles.push({
        x, y,
        vx: Math.cos(a) * sp * (opts.xMul ?? 1),
        vy: Math.sin(a) * sp * (opts.yMul ?? 1),
        life, maxLife: life, color, size: 2 + Math.random() * 2,
        damp: opts.damp, grav: opts.grav,
      });
    }
    if (this.particles.length > 600) this.particles.splice(0, this.particles.length - 600);
  }

  setZoom(z: number) {
    if (!this.camera) return;
    this.camera.setZoomTarget(z);
  }

  // ================= 合成 =================

  itemId(key: string): number {
    return ITEM_BY_KEY[key];
  }

  stationsNearby(): Set<string> {
    const st = this.world.store;
    const px = Math.floor(this.player.cx / TILE), py = Math.floor(this.player.cy / TILE);
    const found = new Set<string>(['hand']);
    for (let dx = -4; dx <= 4; dx++) {
      for (let dy = -3; dy <= 3; dy++) {
        const t = st.get(px + dx, py + dy);
        if (t === T.WORKBENCH) found.add('workbench');
        if (t === T.FURNACE) found.add('furnace');
        if (t === T.ANVIL) found.add('anvil');
      }
    }
    return found;
  }

  canCraft(r: (typeof RECIPES)[number]): boolean {
    if (!this.stationsNearby().has(r.station)) return false;
    return r.inputs.every(([key, n]) => this.player.inv.countOf(ITEM_BY_KEY[key]) >= n);
  }

  craft(r: (typeof RECIPES)[number]) {
    if (!this.canCraft(r)) return;
    for (const [key, n] of r.inputs) this.player.inv.remove(ITEM_BY_KEY[key], n);
    this.player.inv.add(ITEM_BY_KEY[r.out], r.count);
    // 原版合成音 = SoundID 7 物品抓取（成品上鼠标的 grab 声，ItemSlot 族 PlaySound(7)）
    this.sfx.play('pickup');
    this.cb.onInventoryChanged();
  }

  // ================= 原版配方（1456 全量 2688 条） =================

  /** 附近站点集合（内部 tile id）+ 液体/群系 → VanillaCraftCtx（每帧缓存由 UI 调用侧刷新） */
  vanillaNearbyStations(): Set<number> {
    const st = this.world.store;
    const out = new Set<number>();
    const px = Math.floor(this.player.cx / TILE), py = Math.floor(this.player.cy / TILE);
    const ALCHEMY = new Set<number>(); // 炼金台 sheet 355/699
    for (const k of ['v_355_alchemy_table', 'v_699_deadcellspotionstation']) {
      const t = TILE_BY_KEY[k];
      if (t !== undefined) ALCHEMY.add(t);
    }
    // 液体源（Player.cs:35235-35243：liquid>200 且 liquidType 0水/2蜜/1岩浆；
    // CountsAsWaterForCrafting tile 172 水槽/207 也算水）
    this._nearLiquid = { water: false, honey: false, lava: false };
    for (let dx = -20; dx <= 20; dx++) {
      for (let dy = -15; dy <= 15; dy++) {
        const x = px + dx, y = py + dy;
        if (!st.inBounds(x, y)) continue;
        const ii = st.idx(x, y);
        if (st.isActive(x, y)) {
          const t = st.type[ii];
          out.add(t);
          if (ALCHEMY.has(t)) this._alchemyTable = true;
          // CountsAsWaterForCrafting（水槽 172/207 近似：本仓库按 sheet 判）
          const sheet = TILE_DEFS[t]?.vanilla?.sheet;
          if (sheet === 172 || sheet === 207) this._nearLiquid.water = true;
        }
        if (st.liquid[ii] > 200) {

```


---

## 🤖 Assistant · 2026-08-12T15:52:50.401Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now save/serialize and SaveFile and CharacterStore.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:50.475Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/serialize.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:50.497Z

**📎 ToolResult**

```
1	// 存档序列化纯核心(无任何 DOM/World 依赖——save.worker.ts 直接引用,
2	// 主线程 SaveFile.ts 与存档 worker 共用同一份字节级实现,输出逐位一致)。
3	// 性能(2026-08 审计 #2):RLE 输出为密度增长 Uint8Array(varint 字节流)。
4	// 【v3 稳定 id 方案】磁盘 tile/item id 不再存数组下标:TILE_STABLE_OF_INTERNAL /
5	// ITEM_STABLE_OF_INTERNAL 内联映射(data/tiles.ts + data/items.ts 末段,根治顺序漂移)。
6	
7	import { TILE_STABLE_OF_INTERNAL } from '../data/tiles';
8	import { ITEM_STABLE_OF_INTERNAL } from '../data/items';
9	import type { WeatherSave } from '../world/weather/Weather';
10	import type { FurnitureSaveEntry } from '../world/FurnitureItems';
11	
12	class ByteWriter {
13	  buf = new Uint8Array(1 << 16);
14	  len = 0;
15	  private grow(need: number) {
16	    if (this.len + need <= this.buf.length) return;
17	    let cap = this.buf.length;
18	    while (cap < this.len + need) cap *= 2;
19	    const nb = new Uint8Array(cap);
20	    nb.set(this.buf.subarray(0, this.len));
21	    this.buf = nb;
22	  }
23	  varint(v: number) {
24	    v = v < 0 ? 0 : v;
25	    this.grow(5);  // 32 位 varint 至多 5 字节
26	    while (v >= 0x80) {
27	      this.buf[this.len++] = (v & 0x7f) | 0x80;
28	      v >>>= 7;
29	    }
30	    this.buf[this.len++] = v;
31	  }
32	  bytes(): Uint8Array {
33	    return this.buf.subarray(0, this.len);
34	  }
35	}
36	
37	export function bytesToB64(u8: Uint8Array): string {
38	  // 分块拼接(8192)避免逐字符 += 的 ConsString 链;输出与逐字符版一致
39	  let s = '';
40	  const CH = 8192;
41	  for (let i = 0; i < u8.length; i += CH) {
42	    s += String.fromCharCode.apply(null, u8.subarray(i, Math.min(i + CH, u8.length)) as unknown as number[]);
43	  }
44	  return btoa(s);
45	}
46	
47	// ---- 正式 RLE 格式 ----
48	// tiles 每条目: varint(run-1) varint(type) [varint(frameX) varint(frameY) 仅当 type!=0]
49	// walls/liquid: varint(run-1) varint(value)
50	
51	export interface SaveData {
52	  format: 'sandboxworld.save';
53	  version: number;
54	  /** v3: tile/item 磁盘 id = 原版 sheet/item id + 私有段(见 data/tiles.ts 稳定表);v2=旧内部下标 */
55	  idScheme?: 'sheet';
56	  header: {
57	    name: string; seed: number; width: number; height: number;
58	    spawn: [number, number]; groundLevel: number; rockLevel: number; lavaLine?: number;
59	    crimson?: boolean; dungeonX?: number; dungeonY?: number; jungleX?: number;
60	    treeX?: number[]; treeStyle?: number[]; treeTops?: number[];
61	    created: number; playTimeMs: number;
62	    wldVersion?: number;
63	    moonType?: number;   // 月亮贴图样式（原版 header WF:1252；旧档缺省 0 标准月）
64	    seedFlags?: Record<string, boolean>; // 彩蛋种子旗标（旧档缺省={}）
65	    /** 世界难度 = Main.GameMode（Main.cs:2677：0 经典 1 专家 2 大师 3 旅程；
66	     *  原版随 WorldFileData 持久化；旧档缺省 0=经典） */
67	    difficulty?: number;
68	    /** 旅程时间倍率（CreativePowers.ModifyTimeRate.TargetTimeRate，CreativePowers.cs:866-884；
69	     *  IPersistentPerWorldContent 随世界存档；旧档缺省 1） */
70	    journeyTimeRate?: number;
71	    /** 旅程时间冻结（CreativePowers.FreezeTime，CreativePowers.cs:1448；旧档缺省 false） */
72	    journeyFreezeTime?: boolean;
73	  };
74	  clock: {
75	    timeOfDay: number; dayCount: number;
76	    /** 原版 header _tempBloodMoon/_tempEclipse/_tempMoonPhase（WF:1276-1278,读写血月/日食/月相;
77	     *  旧档缺省=false/0/0——血月按夜重掷、月相回满月） */
78	    bloodMoon?: boolean; eclipse?: boolean; moonPhase?: number;
79	  };
80	  /** 入侵状态（原版 WorldFile.cs:1306-1339 五元组；旧档缺省=无入侵） */
81	  invasion?: { type: number; size: number; sizeStart: number; x: number; delay: number };
82	  /** 已砸祭坛数（WorldGen.altarCount，WorldFile.cs:1303/2100；旧档缺省 0） */
83	  altarCount?: number;
84	  tiles: string;   // base64 RLE
85	  walls: string;
86	  liquid: string;
87	  liquidType: string;  // base64 RLE（0无 1水 2岩浆 3蜂蜜 4微光）
88	  wire?: string;       // base64 RLE 电路位（bit0-3 四色线 bit4 致动器 bit5 已致动；旧档缺此字段=全 0）
89	  blocks?: string;     // base64 RLE 半砖/坡面（0=整砖 1=半砖 2-5=slope1-4;旧档缺=全整砖）
90	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null>; locked?: boolean }>;
91	  player: {
92	    hp: number; x: number; y: number;
93	    inventory: Array<SavedItem | null>;
94	    selected: number;
95	    baseMaxHp?: number;   // 生命上限（水晶之心/生命果扩容；旧档缺省 100）
96	    baseMaxMana?: number; // 魔力上限（魔力水晶扩容；旧档缺省 20）
97	    mana?: number;        // 当前魔力
98	    banks?: Array<Array<SavedItem | null>>; // 玩家储物×4（29/97/463/491；旧档缺省全空）
99	    /** armor[20]（0-2 盔甲/3-9 配饰/10-12 时装盔甲/13-19 时装配饰）——旧档缺省经 migrateLegacy 从旧 54 槽布局迁出 */
100	    armor?: Array<SavedItem | null>;
101	    dye?: Array<SavedItem | null>;
102	    trash?: SavedItem | null; // 垃圾桶持久槽（Player.trashItem；死亡清空）
103	    /** miscEquips[5]（宠物/光源/矿车/坐骑/钩爪）与 miscDyes[5]（Player.cs:1376-1379） */
104	    miscEquips?: Array<SavedItem | null>;
105	    miscDyes?: Array<SavedItem | null>;
106	    /** 三套 Loadout（EquipmentLoadout：armor[20]+dye[10]；当前套序号） */
107	    loadouts?: Array<{ armor: Array<SavedItem | null>; dye: Array<SavedItem | null> }>;
108	    currentLoadout?: number;
109	    /** Buff 槽（原版 buffType+buffTime 44 槽,PL:53913-53925;[vanillaBuffId, 剩余秒],
110	     *  Main.buffNoSave 已过滤——旧档缺省=无 buff） */
111	    buffs?: Array<[number, number]>;
112	    /** 税务员累积税款（Player.taxMoney 铜币,PL:53839;旧档缺省 0） */
113	    taxMoney?: number;
114	    /** 高尔夫累计分（Player.golferScoreAccumulated :1792;旧档缺省 0） */
115	    golferScoreAccumulated?: number;
116	    /** PVE 死亡计数（Player.numberOfDeathsPVE,PL:53840;旧档缺省 0） */
117	    deathsPve?: number;
118	  };
119	  npcs: Array<{ key: string; x: number; y: number; home: [number, number] | null; bound?: boolean; givenName?: string }>;
120	  signs?: Array<{ x: number; y: number; text: string }>; // 墓碑碑文（旧档缺省无）
121	  /** 世界事件态（原版 header 内 party/灯笼夜段,WF:1361-1368/1381-1384;旧档缺省=无派对无预约） */
122	  events?: {
123	    partyManual: boolean;            // BirthdayParty.ManualParty
124	    lanternManual: boolean;          // 服务端手动灯笼（本仓无入口,位保留）
125	    lanternGenuine: boolean;         // 真灯笼夜兑现中
126	    lanternNext: boolean;            // 次夜灯笼夜预约
127	    lanternCooldown: number;         // 冷却夜数
128	  };
129	  /** 挂物族存放物（物品框 395/武器架 471/模特 470/帽架 475/食物盘 520/展示罐 698；
130	   *  原版 TileEntity 段的最小等价，旧档缺省无） */
131	  furniture?: FurnitureSaveEntry[];
132	  flags: Record<string, boolean>;
133	  weather?: WeatherSave; // 天气快照（雨/风/云/沙尘暴；旧档缺省=晴）
134	  /** 图鉴统计（BestiaryUnlocksTracker——原版随世界文件持久化 WorldFile.cs:3399/3405；
135	   *  旧档缺省=空三桶） */
136	  bestiary?: import('../data/Bestiary').BestiarySave;
137	}
138	
139	/** 存档物品实例（Inventory.InvItem 的可序列化形——favorited/prefix 为实例态可选字段） */
140	export interface SavedItem {
141	  id: number; stack: number;
142	  favorited?: boolean;
143	  prefix?: number; // 重铸词缀（Item.prefix；0/缺省=无）
144	}
145	
146	/** 序列化所需的 tilestore 视图(worker 路径=副本包装;主线程=活存储) */
147	export interface SaveStoreView {
148	  type: Uint16Array; flags: Uint8Array;
149	  frameX: Uint16Array; frameY: Uint16Array;
150	  wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; wire: Uint8Array;
151	  half: Uint8Array; slope: Uint8Array;
152	}
153	/** 序列化所需的世界元数据(全部可结构化克隆) */
154	export interface SaveMeta {
155	  name: string; seed: number; w: number; h: number;
156	  spawnX: number; spawnY: number; groundLevel: number; rockLevel: number; lavaLine?: number;
157	  treeX?: number[]; treeStyle?: number[]; treeTops?: number[];
158	  crimson?: boolean; dungeonX?: number; dungeonY?: number; jungleX?: number;
159	  timeOfDay: number; dayCount: number;
160	  bloodMoon?: boolean; eclipse?: boolean; moonPhase?: number; moonType?: number;
161	  seedFlags?: Record<string, boolean>;
162	  /** 世界难度 = Main.GameMode（Main.cs:2677；旧档缺省 0=经典） */
163	  difficulty?: number;
164	  /** 旅程时间倍率/冻结（CreativePowers.cs:866/:1448；旧档缺省 1/false） */
165	  journeyTimeRate?: number;
166	  journeyFreezeTime?: boolean;
167	  chests: SaveData['chests']; signs?: SaveData['signs']; furniture?: FurnitureSaveEntry[]; flags: Record<string, boolean>;
168	  weather?: WeatherSave;
169	  invasion?: { type: number; size: number; sizeStart: number; x: number; delay: number };
170	  /** 已砸祭坛数（WorldGen.altarCount，WorldFile.cs:1303/2100；旧档缺省 0） */
171	  altarCount?: number;
172	  /** 图鉴三桶（杀数/遇数/聊天）——data/Bestiary.ts BestiarySave */
173	  bestiary?: import('../data/Bestiary').BestiarySave;
174	}
175	
176	export function rlePairs(values: ArrayLike<number>): Uint8Array {
177	  const out = new ByteWriter();
178	  const n = values.length;
179	  let i = 0;
180	  while (i < n) {
181	    const v = values[i];
182	    let run = 1;
183	    while (i + run < n && values[i + run] === v && run < 0x7fffffff) run++;
184	    out.varint(run - 1);
185	    out.varint(v);
186	    i += run;
187	  }
188	  return out.bytes();
189	}
190	
191	/** RLE tiles。stableMap 非空时逐元素映射为稳定 id(v3 存档路径) */
192	export function rleTiles(st: { type: Uint16Array; frameX: Uint16Array; frameY: Uint16Array }, stableMap?: Uint16Array): Uint8Array {
193	  const out = new ByteWriter();
194	  const n = st.type.length;
195	  let i = 0;
196	  while (i < n) {
197	    const raw = st.type[i];
198	    const t = stableMap ? (raw === 0 ? 0 : stableMap[raw]) : raw;
199	    const fx = st.frameX[i], fy = st.frameY[i];
200	    let run = 1;
201	    // 游程比较必须 raw 对 raw（t 是映射后的稳定 id，与原始 id 比较恒不等 →
202	    // 自定义 tile（stable≠internal）游程全断，4200x1200 规则地形 17B 膨胀到 21MB）
203	    while (i + run < n && st.type[i + run] === raw && st.frameX[i + run] === fx && st.frameY[i + run] === fy) run++;
204	    out.varint(run - 1);
205	    out.varint(t);
206	    if (t !== 0) {
207	      out.varint(fx);
208	      out.varint(fy);
209	    }
210	    i += run;
211	  }
212	  return out.bytes();
213	}
214	
215	/** 存档序列化主体。幽灵净化在视图上就地执行(主线程=活存储原语义;
216	 * worker=副本,净化不影响游戏内状态,存档字节一致) */
217	export function serializeSave(
218	  st: SaveStoreView, meta: SaveMeta,
219	  player: SaveData['player'], playTimeMs: number,
220	  townNpcs?: SaveData['npcs'],
221	  events?: SaveData['events'],
222	): string {
223	  // 幽灵净化:存档格式不携带 active 位(加载时 type≠0 即激活),
224	  // 非活性格上的残留 type 必须归零,否则重读后全部变成浮空实体块
225	  for (let i = 0; i < st.type.length; i++) {
226	    if (!st.flags[i] && st.type[i] !== 0) st.type[i] = 0;
227	  }
228	  // 物品 id → 稳定 id(箱子/背包/储物;量小直接遍历)
229	  const mapItem = (it: { id: number; stack: number } | null) =>
230	    it ? { id: it.id === 0 ? 0 : ITEM_STABLE_OF_INTERNAL[it.id] ?? 0, stack: it.stack } : null;
231	  const data: SaveData = {
232	    format: 'sandboxworld.save',
233	    version: 3,
234	    header: {
235	      name: meta.name, seed: meta.seed, width: meta.w, height: meta.h,
236	      spawn: [meta.spawnX, meta.spawnY], groundLevel: meta.groundLevel, rockLevel: meta.rockLevel,
237	      lavaLine: meta.lavaLine,
238	      treeX: meta.treeX, treeStyle: meta.treeStyle, treeTops: meta.treeTops,
239	      crimson: meta.crimson, dungeonX: meta.dungeonX, dungeonY: meta.dungeonY, jungleX: meta.jungleX,
240	      created: Date.now(), playTimeMs,
241	      moonType: meta.moonType ?? 0,
242	      seedFlags: meta.seedFlags,
243	      difficulty: meta.difficulty ?? 0,   // Main.GameMode（旧档缺省=经典）
244	      journeyTimeRate: meta.journeyTimeRate ?? 1,
245	      journeyFreezeTime: meta.journeyFreezeTime ?? false,
246	    },
247	    clock: {
248	      timeOfDay: meta.timeOfDay, dayCount: meta.dayCount,
249	      bloodMoon: meta.bloodMoon ?? false, eclipse: meta.eclipse ?? false,
250	      moonPhase: meta.moonPhase ?? 0,
251	    },
252	    invasion: meta.invasion ?? { type: 0, size: 0, sizeStart: 0, x: 0, delay: 0 },
253	    altarCount: meta.altarCount ?? 0,
254	    tiles: bytesToB64(rleTiles(st, TILE_STABLE_OF_INTERNAL)),
255	    walls: bytesToB64(rlePairs(st.wall)),
256	    liquid: bytesToB64(rlePairs(st.liquid)),
257	    liquidType: bytesToB64(rlePairs(st.liquidType)),
258	    wire: bytesToB64(rlePairs(st.wire)),
259	    blocks: bytesToB64(rlePairs(combineBlocks(st.half, st.slope))),
260	    chests: meta.chests.map((c) => ({ x: c.x, y: c.y, locked: c.locked || undefined, items: c.items.map(mapItem) })),
261	    player: { ...player, inventory: player.inventory.map(mapItem), banks: player.banks?.map((b) => b.map(mapItem)) },
262	    npcs: townNpcs ?? [],   // 城镇 NPC 段(WorldFile.cs:1703-1750 NPC 段;曾硬编码 [] 断链)
263	    signs: meta.signs,
264	    // 挂物族：存放物 id 走与 chests 相同的稳定 id 映射（mapItem 同构，保留 prefix）
265	    furniture: meta.furniture?.map((e) => ({
266	      x: e.x, y: e.y, kind: e.kind,
267	      slots: e.slots.map((s) => (s ? { id: s.id === 0 ? 0 : ITEM_STABLE_OF_INTERNAL[s.id] ?? 0, stack: s.stack, prefix: s.prefix } : null)),
268	    })),
269	    flags: meta.flags,
270	    weather: meta.weather,
271	    events,
272	    bestiary: meta.bestiary,
273	    idScheme: 'sheet',
274	  };
275	  return JSON.stringify(data);
276	}
277	
278	/** half + slope → 单字节 blockType(原版 Tile.blockType: 0=整砖 1=半砖 2-5=slope1-4) */
279	function combineBlocks(half: Uint8Array, slope: Uint8Array): Uint8Array {
280	  const out = new Uint8Array(half.length);
281	  for (let i = 0; i < half.length; i++) {
282	    out[i] = half[i] ? 1 : (slope[i] >= 1 && slope[i] <= 4 ? slope[i] + 1 : 0);
283	  }
284	  return out;
285	}
286	

```


---

## 🤖 Assistant · 2026-08-12T15:52:50.627Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/CharacterStore.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:50.650Z

**📎 ToolResult**

```
1	// 多角色存储：KvStore 索引 + 每角色一条记录。
2	// index: sandboxworld.players.index → [{id,name,difficulty,createdAt}]
3	// data : sandboxworld.player.<id>   → Appearance JSON
4	import { kvGet, kvSet, kvHas, kvDelete } from './KvStore';
5	import { validateAppearance, type Appearance } from '../player/Appearance';
6	
7	const INDEX_KEY = 'sandboxworld.players.index';
8	const dataKey = (id: number) => `sandboxworld.player.${id}`;
9	
10	export interface CharacterMeta { id: number; name: string; difficulty: number; createdAt: number; }
11	
12	let nextId = 1;
13	
14	export class CharacterStore {
15	  private index: CharacterMeta[] = [];
16	  private loaded = false;
17	
18	  async ensureLoaded() {
19	    if (this.loaded) return;
20	    const raw = await kvGet(INDEX_KEY);
21	    if (raw) {
22	      try {
23	        const arr = JSON.parse(raw);
24	        if (Array.isArray(arr)) this.index = arr.filter((x) => x && typeof x.id === 'number');
25	      } catch { /* 损坏索引当空 */ }
26	    }
27	    for (const m of this.index) if (m.id >= nextId) nextId = m.id + 1;
28	    this.loaded = true;
29	  }
30	
31	  private async saveIndex() {
32	    await kvSet(INDEX_KEY, JSON.stringify(this.index));
33	  }
34	
35	  list(): CharacterMeta[] { return [...this.index]; }
36	
37	  async get(id: number): Promise<Appearance | null> {
38	    if (!await kvHas(dataKey(id))) return null;
39	    const raw = await kvGet(dataKey(id));
40	    if (!raw) return null;
41	    try {
42	      return validateAppearance(JSON.parse(raw));
43	    } catch {
44	      return null;
45	    }
46	  }
47	
48	  async create(a: Appearance): Promise<CharacterMeta> {
49	    await this.ensureLoaded();
50	    const meta: CharacterMeta = { id: nextId++, name: a.name || '无名角色', difficulty: a.difficulty, createdAt: Date.now() };
51	    this.index.push(meta);
52	    await this.saveIndex();
53	    await kvSet(dataKey(meta.id), JSON.stringify(a));
54	    return meta;
55	  }
56	
57	  async update(id: number, a: Appearance) {
58	    await this.ensureLoaded();
59	    const m = this.index.find((x) => x.id === id);
60	    if (!m) return;
61	    m.name = a.name || m.name;
62	    m.difficulty = a.difficulty;
63	    await this.saveIndex();
64	    await kvSet(dataKey(id), JSON.stringify(a));
65	  }
66	
67	  async delete(id: number) {
68	    await this.ensureLoaded();
69	    this.index = this.index.filter((x) => x.id !== id);
70	    await this.saveIndex();
71	    await kvDelete(dataKey(id));
72	  }
73	
74	  async copy(id: number): Promise<CharacterMeta | null> {
75	    const a = await this.get(id);
76	    if (!a) return null;
77	    return this.create({ ...a, name: `${a.name} 副本` });
78	  }
79	}
80	

```


---

## 🤖 Assistant · 2026-08-12T15:52:52.867Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
CharacterStore stores only Appearance (no items). Starter gear is in Game.ts:1645-1647 and mainFlow.ts:320-322 (copper_pickaxe/axe/sword). Also Game.ts:390-391 starter array.

Now the load side — SaveFile.ts, and the migration mechanisms (migrateLegacy, ITEM_INTERNAL_OF_STABLE). Let me read SaveFile.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:52.984Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:53.009Z

**📎 ToolResult**

```
1	// 自有存档格式：JSON 外壳（人可读）+ RLE 二进制 tile 段（base64）
2	// 序列化纯核心在 ./serialize(无 DOM/World 依赖,主线程与 save.worker.ts 共用同一实现);
3	// 本文件保留 SaveData 类型/读档解码与主线程同步 saveGame(兼容入口,worker 不可用时回退)。
4	import type { World } from '../world/World';
5	import { World as WorldClass } from '../world/World';
6	import type { Player } from '../entities/Player';
7	import { serializeSave } from './serialize';
8	import type { SaveData, SaveStoreView, SaveMeta } from './serialize';
9	import { TILE_INTERNAL_OF_STABLE } from '../data/tiles';
10	import { ITEM_INTERNAL_OF_STABLE } from '../data/items';
11	import { weatherToSave } from '../world/weather/Weather';
12	import { applyLunarSave } from '../world/LunarEvent';
13	import { furnitureFromSave } from '../world/FurnitureItems';
14	
15	export { bytesToB64, rlePairs, rleTiles, serializeSave } from './serialize';
16	export type { SaveData, SaveStoreView, SaveMeta } from './serialize';
17	
18	function b64ToBytes(b64: string): Uint8Array {
19	  const s = atob(b64);
20	  const u8 = new Uint8Array(s.length);
21	  for (let i = 0; i < s.length; i++) u8[i] = s.charCodeAt(i);
22	  return u8;
23	}
24	
25	function readVarint(u8: Uint8Array, pos: { i: number }): number {
26	  let v = 0, shift = 0;
27	  while (pos.i < u8.length) {
28	    const b = u8[pos.i++];
29	    v |= (b & 0x7f) << shift;
30	    if (!(b & 0x80)) break;
31	    shift += 7;
32	  }
33	  return v;
34	}
35	
36	/** 主线程同步存档(兼容入口/worker 回退路径)。常规保存请走 SaveClient.saveAsync */
37	export function saveGame(world: World, player: Player, playTimeMs: number, townNpcs?: SaveData['npcs'], events?: SaveData['events']): string {
38	  const st = world.store;
39	  const view: SaveStoreView = {
40	    type: st.type, flags: st.flags, frameX: st.frameX, frameY: st.frameY,
41	    wall: st.wall, liquid: st.liquid, liquidType: st.liquidType, wire: st.wire,
42	    half: st.half, slope: st.slope,
43	  };
44	  const meta: SaveMeta = {
45	    name: world.name, seed: world.seed, w: st.w, h: st.h,
46	    spawnX: world.spawnX, spawnY: world.spawnY,
47	    groundLevel: world.groundLevel, rockLevel: world.rockLevel, lavaLine: world.lavaLine,
48	    treeX: world.treeX, treeStyle: world.treeStyle, treeTops: world.treeTops,
49	    crimson: world.crimson, dungeonX: world.dungeonX, dungeonY: world.dungeonY, jungleX: world.jungleX,
50	    timeOfDay: world.clock.timeOfDay, dayCount: world.clock.dayCount,
51	    bloodMoon: world.clock.bloodMoon, eclipse: world.clock.eclipse,
52	    moonPhase: world.clock.moonPhase, moonType: world.moonType,
53	    seedFlags: { ...world.seedFlags },
54	    difficulty: world.difficulty,   // Main.GameMode（Main.cs:2677）
55	    journeyTimeRate: world.journeyTimeRate, journeyFreezeTime: world.journeyFreezeTime,
56	    chests: world.chests, signs: world.signs, flags: world.flags,
57	    weather: weatherToSave(world.weather),
58	    invasion: { type: world.invasionType, size: world.invasionSize, sizeStart: world.invasionSizeStart,
59	      x: world.invasionX, delay: world.invasionDelay },
60	    altarCount: world.altarCount,   // WorldGen.altarCount（WorldFile.cs:1303/2100）
61	    bestiary: world.bestiary.toSave(),  // BestiaryUnlocksTracker（WorldFile.cs:3399）
62	    // 挂物族存放物（内部 id；serializeSave 内过稳定 id 表）
63	    // 挂物族存放物：内部 id 直传（serializeSave 内统一过稳定 id 表，与 chests 同路径）
64	    furniture: world.furnitureItems,
65	  };
66	  const playerData: SaveData['player'] = {
67	    hp: player.hp, x: player.x, y: player.y,
68	    inventory: player.inv.slots, selected: player.inv.selected,
69	    baseMaxHp: player.baseMaxHp, baseMaxMana: player.baseMaxMana, mana: player.mana,
70	    banks: player.banks,
71	    armor: player.inv.armor,
72	    dye: player.inv.dye,
73	    trash: player.inv.trash,
74	    miscEquips: player.inv.miscEquips,
75	    miscDyes: player.inv.miscDyes,
76	    loadouts: player.inv.loadouts,
77	    currentLoadout: player.inv.currentLoadout,
78	    buffs: player.buffs?.toSave?.() ?? [],  // buffType+buffTime 槽（PL:53913-53925;桩 player 容忍）
79	    taxMoney: player.taxMoney ?? 0,         // PL:53839
80	    golferScoreAccumulated: player.golferScoreAccumulated ?? 0, // PL:1792
81	    deathsPve: player.deathsPve ?? 0,       // PL:53840
82	  };
83	  return serializeSave(view, meta, playerData, playTimeMs, townNpcs, events);
84	}
85	
86	export function loadSave(json: string): ReturnType<typeof loadSaveData> {
87	  return loadSaveData(JSON.parse(json) as SaveData);
88	}
89	
90	/** 服务器侧世界-only 存档（P3.1 持久化）：tile/箱子/clock/flags/天气，不含玩家/城镇NPC。
91	 *  player 字段以空壳占位（格式必填；语义上服务器档无玩家，加载方忽略）。
92	 *  注意：serializeSave 的幽灵净化会就地写 store——服务器存储由 setTileSilent/
93	 *  loadSaveData 保持 type/flags 一致，该循环为 no-op，活存储不受影响。 */
94	export function saveWorldOnly(world: World): string {
95	  const st = world.store;
96	  const view: SaveStoreView = {
97	    type: st.type, flags: st.flags, frameX: st.frameX, frameY: st.frameY,
98	    wall: st.wall, liquid: st.liquid, liquidType: st.liquidType, wire: st.wire,
99	    half: st.half, slope: st.slope,
100	  };
101	  const meta: SaveMeta = {
102	    name: world.name, seed: world.seed, w: st.w, h: st.h,
103	    spawnX: world.spawnX, spawnY: world.spawnY,
104	    groundLevel: world.groundLevel, rockLevel: world.rockLevel, lavaLine: world.lavaLine,
105	    treeX: world.treeX, treeStyle: world.treeStyle, treeTops: world.treeTops,
106	    crimson: world.crimson, dungeonX: world.dungeonX, dungeonY: world.dungeonY, jungleX: world.jungleX,
107	    timeOfDay: world.clock.timeOfDay, dayCount: world.clock.dayCount,
108	    difficulty: world.difficulty,   // Main.GameMode（Main.cs:2677）——服务器档随世界下发
109	    chests: world.chests, signs: world.signs, flags: world.flags,
110	    weather: weatherToSave(world.weather),
111	    invasion: { type: world.invasionType, size: world.invasionSize, sizeStart: world.invasionSizeStart,
112	      x: world.invasionX, delay: world.invasionDelay },
113	    altarCount: world.altarCount,
114	    bestiary: world.bestiary.toSave(),  // BestiaryUnlocksTracker（WorldFile.cs:3399）
115	    // 挂物族存放物：内部 id 直传（serializeSave 内统一过稳定 id 表，与 chests 同路径）
116	    furniture: world.furnitureItems,
117	  };
118	  const placeholderPlayer: SaveData['player'] = {
119	    hp: 0, x: world.spawnX * 16, y: world.spawnY * 16,
120	    inventory: [], selected: 0,
121	  };
122	  return serializeSave(view, meta, placeholderPlayer, 0);
123	}
124	
125	/** 直接从内存 SaveData 构建(导入 .wld 路径用——跳过 stringify→parse 双拷贝,
126	 *  2026-08 审计 #3:该往返单次 20~50MB×2) */
127	export function loadSaveData(data: SaveData): { world: World; player: SaveData['player']; data: SaveData } {
128	  // v3 物品稳定 id → internal(箱子/背包/储物就地重写;v2 旧档直读)
129	  const v3 = (data.version ?? 1) >= 3;
130	  const mapItem = (it: { id: number; stack: number } | null) =>
131	    it && v3 ? { id: it.id === 0 ? 0 : ITEM_INTERNAL_OF_STABLE.get(it.id) ?? 0, stack: it.stack } : it;
132	  // v3 稳定 id → 内部 id(含 locked 透传);★曾未接线直接用 data.chests——
133	  // 现有物品 stable≡internal 掩盖,自定义物品进箱即错
134	  const v3Chests = v3
135	    ? data.chests.map((c) => ({ x: c.x, y: c.y, locked: c.locked, items: c.items.map(mapItem) }))
136	    : data.chests;
137	  if (v3 && data.player) {
138	    data.player = {
139	      ...data.player,
140	      inventory: data.player.inventory.map(mapItem),
141	      banks: data.player.banks?.map((b) => b.map(mapItem)),
142	    };
143	  }
144	  const world = new WorldClass(data.header.width, data.header.height, data.header.seed, data.header.name);
145	  world.spawnX = data.header.spawn[0];
146	  world.spawnY = data.header.spawn[1];
147	  world.groundLevel = data.header.groundLevel;
148	  world.rockLevel = data.header.rockLevel;
149	  // 旧档缺 lavaLine（原版 UnderworldLayer = maxTilesY-200）
150	  world.lavaLine = data.header.lavaLine ?? data.header.height - 200;
151	  if (data.header.treeX) world.treeX = data.header.treeX;
152	  if (data.header.treeStyle) world.treeStyle = data.header.treeStyle;
153	  if (data.header.treeTops?.length) world.treeTops = data.header.treeTops;
154	  if (data.header.crimson !== undefined) world.crimson = data.header.crimson;
155	  if (data.header.dungeonX !== undefined) world.dungeonX = data.header.dungeonX;
156	  // dungeonY 缺省（旧档/导入）回退地表线：CheckToSpawnDungeonEnemies 的 pY<dungeonY+40 门槛近似成立
157	  if (data.header.dungeonY !== undefined && data.header.dungeonY > 0) world.dungeonY = data.header.dungeonY;
158	  else world.dungeonY = world.groundLevel;
159	  if (data.header.jungleX !== undefined) world.jungleX = data.header.jungleX;
160	  world.clock.timeOfDay = data.clock.timeOfDay;
161	  world.clock.dayCount = data.clock.dayCount;
162	  // 原版 header _temp 三件套（WF:1276-1278）;旧档缺省=无血月/无日食/满月
163	  if (data.clock.bloodMoon !== undefined) world.clock.bloodMoon = data.clock.bloodMoon;
164	  if (data.clock.eclipse !== undefined) world.clock.eclipse = data.clock.eclipse;
165	  if (data.clock.moonPhase !== undefined) world.clock.moonPhase = data.clock.moonPhase;
166	  if (data.header.moonType !== undefined) world.moonType = data.header.moonType;
167	  if (data.header.seedFlags) world.seedFlags = { ...data.header.seedFlags };
168	  // 世界难度（Main.GameMode，Main.cs:2677）——旧档缺省 0=经典
169	  if (data.header.difficulty !== undefined) world.difficulty = data.header.difficulty;
170	  // 旅程时间倍率/冻结（CreativePowers.cs:866/:1448）——旧档缺省 1/false
171	  if (data.header.journeyTimeRate !== undefined) world.journeyTimeRate = data.header.journeyTimeRate;
172	  if (data.header.journeyFreezeTime !== undefined) world.journeyFreezeTime = data.header.journeyFreezeTime;
173	  if (data.invasion) { // 入侵五元组回填（旧档缺省=无入侵）
174	    world.invasionType = data.invasion.type;
175	    world.invasionSize = data.invasion.size;
176	    world.invasionSizeStart = data.invasion.sizeStart;
177	    world.invasionX = data.invasion.x;
178	    world.invasionDelay = data.invasion.delay;
179	  }
180	  if (data.altarCount != null) world.altarCount = data.altarCount; // 旧档缺省 0
181	  world.applyBestiary(data.bestiary); // 图鉴三桶（旧档缺省=空）
182	  world.chests = v3Chests;      // v3 id 翻译+locked 透传
183	  if (data.weather) world.applyWeather(data.weather); // 天气回填（旧档缺省=晴）
184	  world.flags = data.flags;
185	  // 星璇塔运行时态回填（WorldFile.cs:2220-2255 尾段：downedTower*/towerActive*/lunarApocalypseUp
186	  // 三类 bool 走 flags 落盘；盾值不存——TowerActive=true 读档重置满盾）
187	  applyLunarSave(world);
188	  // 城镇 NPC 段（原版 NPC 段 WF:1703-1750;旧档/曾断链=空数组 → 走新世界出生分支）
189	  if (data.npcs?.length) world.pendingTownNpcs = data.npcs;
190	  if (data.signs) world.signs = data.signs;
191	  // 挂物族存放物（v3 稳定 id → 内部 id；未知 id 归 0 由 furnitureFromSave 置空槽）
192	  world.furnitureItems = furnitureFromSave(
193	    data.furniture,
194	    (id) => (v3 ? ITEM_INTERNAL_OF_STABLE.get(id) ?? 0 : id),
195	  );
196	
197	  const st = world.store;
198	  // tiles(v3:RLE 里的 type 是稳定 id,查 INTERNAL_OF_STABLE 还原;v2 旧档=内部下标直读)
199	  {
200	    const v3 = (data.version ?? 1) >= 3;
201	    const u8 = b64ToBytes(data.tiles);
202	    const pos = { i: 0 };
203	    let i = 0;
204	    while (i < st.type.length && pos.i < u8.length) {
205	      const run = readVarint(u8, pos) + 1;
206	      const tRaw = readVarint(u8, pos);
207	      const t = v3 ? (tRaw === 0 ? 0 : TILE_INTERNAL_OF_STABLE[tRaw]) : tRaw;
208	      let fx = 0, fy = 0;
209	      if (t !== 0) {
210	        fx = readVarint(u8, pos);
211	        fy = readVarint(u8, pos);
212	      }
213	      for (let k = 0; k < run && i < st.type.length; k++, i++) {
214	        st.type[i] = t; st.flags[i] = t !== 0 ? 1 : 0;
215	        st.frameX[i] = fx; st.frameY[i] = fy;
216	      }
217	    }
218	  }
219	  // walls（version<2 的旧档墙值迁移：1=土→2, 2=石→1, 3=木→4（现为原版 id））
220	  {
221	    const legacy = (data.version ?? 1) < 2;
222	    const migrate = (v: number) => (legacy ? (v === 1 ? 2 : v === 2 ? 1 : v === 3 ? 4 : v) : v);
223	    const u8 = b64ToBytes(data.walls);
224	    const pos = { i: 0 };
225	    let i = 0;
226	    while (i < st.wall.length && pos.i < u8.length) {
227	      const run = readVarint(u8, pos) + 1;
228	      const v = migrate(readVarint(u8, pos));
229	      for (let k = 0; k < run && i < st.wall.length; k++, i++) st.wall[i] = v;
230	    }
231	  }
232	  // wire 电路位（旧存档缺此字段 → 全 0 = 无导线，缺字段容忍同 liquidType）
233	  {
234	    const u8 = b64ToBytes(data.wire ?? '');
235	    const pos = { i: 0 };
236	    let i = 0;
237	    while (i < st.wire.length && pos.i < u8.length) {
238	      const run = readVarint(u8, pos) + 1;
239	      const v = readVarint(u8, pos);
240	      for (let k = 0; k < run && i < st.wire.length; k++, i++) st.wire[i] = v;
241	    }
242	  }
243	  // half/slope(旧存档缺 → 全整砖;v3+ 语义)
244	  {
245	    const u8 = b64ToBytes(data.blocks ?? '');
246	    const pos = { i: 0 };
247	    let i = 0;
248	    while (i < st.half.length && pos.i < u8.length) {
249	      const run = readVarint(u8, pos) + 1;
250	      const v = readVarint(u8, pos);
251	      for (let k = 0; k < run && i < st.half.length; k++, i++) {
252	        st.half[i] = v === 1 ? 1 : 0;
253	        st.slope[i] = v >= 2 && v <= 5 ? v - 1 : 0;
254	      }
255	    }
256	  }
257	  // liquid type（旧存档缺此字段 → 全 0，由液体模拟按 1=水 补全）
258	  {
259	    const u8 = b64ToBytes(data.liquidType ?? '');
260	    const pos = { i: 0 };
261	    let i = 0;
262	    while (i < st.liquidType.length && pos.i < u8.length) {
263	      const run = readVarint(u8, pos) + 1;
264	      const v = readVarint(u8, pos);
265	      for (let k = 0; k < run && i < st.liquidType.length; k++, i++) st.liquidType[i] = v;
266	    }
267	  }
268	  // liquid
269	  {
270	    const u8 = b64ToBytes(data.liquid);
271	    const pos = { i: 0 };
272	    let i = 0;
273	    while (i < st.liquid.length && pos.i < u8.length) {
274	      const run = readVarint(u8, pos) + 1;
275	      const v = readVarint(u8, pos);
276	      for (let k = 0; k < run && i < st.liquid.length; k++, i++) st.liquid[i] = v;
277	    }
278	  }
279	  return { world, player: data.player, data };
280	}
281	

```


---

## 🤖 Assistant · 2026-08-12T15:52:56.600Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key finding: loadSaveData only maps inventory + banks with mapItem, but NOT armor, dye, trash, miscEquips, miscDyes, loadouts! Let me check: `data.player = {...data.player, inventory: ..., banks: ...}`. armor/dye/trash/miscEquips/miscDyes/loadouts are NOT mapped. Wait — but the save writes armor etc. raw (player.inv.armor internal ids) without ITEM_STABLE mapping either (serializeSave only maps inventory and banks: `player: { ...player, inventory: player.inventory.map(mapItem), banks: player.banks?.map(b => b.map(mapItem)) }`). So armor etc. are saved as RAW internal ids (bug-prone but existing behavior). Interesting. Let me check for migrateLegacy — mentioned in the doc comment. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:52:57.055Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"migrateLegacy\\|ITEM_INTERNAL_OF_STABLE\\|ITEM_STABLE_OF_INTERNAL\\|PRIV_ITEM_STABLE\" src tests tools --include=\"*.ts\" | grep -v \"idNames.generated\"",
 "description": "Find stable id migration usage"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:57.098Z

**📎 ToolResult**

```
src/mainFlow.ts:194:    // 背包布局迁移（旧 54 槽自创布局 → 原版 58 槽+armor[20]；Inventory.migrateLegacy 判别）
src/mainFlow.ts:195:    const mig = Inventory.migrateLegacy(player.inventory);
src/world/FurnitureItems.ts:446://   与 chests 的 ITEM_STABLE_OF_INTERNAL 路径同构）
src/items/Inventory.ts:331:  static migrateLegacy(legacy: Array<{ id: number; stack: number } | null>): {
src/data/items.ts:922:// ★ PRIV_ITEM_STABLE 冻结表 append-only:新自造物品只许表尾追加,已分配号码永不复用/改派。
src/data/items.ts:923:const PRIV_ITEM_STABLE: Record<string, number> = {
src/data/items.ts:1065:export const ITEM_STABLE_OF_INTERNAL = new Uint16Array(ITEM_DEFS.length);
src/data/items.ts:1067:export const ITEM_INTERNAL_OF_STABLE = new Map<number, number>();
src/data/items.ts:1074:  const s = vm ? Number(vm[1]) : PRIV_ITEM_STABLE[k] ?? (pm ? 20000 + Number(pm[1]) : undefined);
src/data/items.ts:1076:  ITEM_STABLE_OF_INTERNAL[i] = s;
src/data/items.ts:1077:  if (!ITEM_INTERNAL_OF_STABLE.has(s)) ITEM_INTERNAL_OF_STABLE.set(s, i);
src/save/serialize.ts:5:// ITEM_STABLE_OF_INTERNAL 内联映射(data/tiles.ts + data/items.ts 末段,根治顺序漂移)。
src/save/serialize.ts:8:import { ITEM_STABLE_OF_INTERNAL } from '../data/items';
src/save/serialize.ts:99:    /** armor[20]（0-2 盔甲/3-9 配饰/10-12 时装盔甲/13-19 时装配饰）——旧档缺省经 migrateLegacy 从旧 54 槽布局迁出 */
src/save/serialize.ts:230:    it ? { id: it.id === 0 ? 0 : ITEM_STABLE_OF_INTERNAL[it.id] ?? 0, stack: it.stack } : null;
src/save/serialize.ts:267:      slots: e.slots.map((s) => (s ? { id: s.id === 0 ? 0 : ITEM_STABLE_OF_INTERNAL[s.id] ?? 0, stack: s.stack, prefix: s.prefix } : null)),
src/save/SaveFile.ts:10:import { ITEM_INTERNAL_OF_STABLE } from '../data/items';
src/save/SaveFile.ts:131:    it && v3 ? { id: it.id === 0 ? 0 : ITEM_INTERNAL_OF_STABLE.get(it.id) ?? 0, stack: it.stack } : it;
src/save/SaveFile.ts:194:    (id) => (v3 ? ITEM_INTERNAL_OF_STABLE.get(id) ?? 0 : id),
tests/furniture-items.test.ts:10:import { ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID, ITEM_STABLE_OF_INTERNAL } from '../src/data/items';
tests/furniture-items.test.ts:282:    // 见 items.ts ITEM_INTERNAL_OF_STABLE 注释）——按内容等价（稳定 id 一致）断言
tests/furniture-items.test.ts:285:    expect(ITEM_STABLE_OF_INTERNAL[f2.slots[0]!.id]).toBe(ITEM_STABLE_OF_INTERNAL[iid(VID.sword)]);
tests/furniture-items.test.ts:288:    expect(ITEM_STABLE_OF_INTERNAL[d2.slots[0]!.id]).toBe(ITEM_STABLE_OF_INTERNAL[iid(VID.head)]);
tests/furniture-items.test.ts:289:    expect(ITEM_STABLE_OF_INTERNAL[d2.slots[9]!.id]).toBe(ITEM_STABLE_OF_INTERNAL[iid(VID.sword)]);

```


---

## 🤖 Assistant · 2026-08-12T15:52:57.642Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"def.tool\\|\\.tool\\b\" src/core/Game.ts | grep -in \"tool\" | head -50",
 "description": "Find tool usage in Game"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:57.681Z

**📎 ToolResult**

```
1:src/core/Game.ts:3285:   *  vi_ 取 vanilla-itemcombat.useAnimation；legacy 工具 def.tool.speed；
2:src/core/Game.ts:3289:    if (def.tool?.speed) return Math.max(10, def.tool.speed);
3:src/core/Game.ts:3360:    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
4:src/core/Game.ts:3462:   * 三力取 vanilla-itemfunc 全量（Hamaxe 斧+锤 / Drax 镐+斧 副力保留），legacy def.tool
5:src/core/Game.ts:3477:        def?.tool ? { type: def.tool.type as 'pick' | 'axe' | 'hammer', power: def.tool.power ?? 0 } : null,
6:src/core/Game.ts:3526:    // 工具判定：legacy def.tool 优先；vi_ 镐/斧/锤经 vanilla-itemfunc 桥接（数值取 combat 表）
7:src/core/Game.ts:3527:    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
8:src/core/Game.ts:3724:    if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool
9:src/core/Game.ts:7116:    const tool = heldDef.tool ?? this.itemFuncTool(held.id);
10:src/core/Game.ts:7120:    // 一击致死，均为原版没有的行为（vi_ 数值取 combat 表，legacy 工具取 def.tool）
11:src/core/Game.ts:10443:    if (def.tool?.type === 'sword' || combatWeapon(def)?.kind === 'melee') {
12:src/core/Game.ts:10445:      return Math.max(12, Math.round((cw?.useTime ?? def.tool?.speed ?? 42) / spd));
13:src/core/Game.ts:10447:    if (def.tool && (def.tool.type === 'pick' || def.tool.type === 'axe' || def.tool.type === 'hammer')) {
14:src/core/Game.ts:10448:      return Math.max(14, Math.round((def.tool.speed ?? 46) / spd));

```


---

## 🤖 Assistant · 2026-08-12T15:52:59.778Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3270,3300p;3340,3400p;3450,3560p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read tool stats bridge in Game"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:52:59.820Z

**📎 ToolResult**

```
  /** 手持物 useStyle 分族（Player.cs:49939 ItemCheck_ApplyUseStyle switch）：
   *  vi_ → vanilla-itemfunc.useStyle（2141 件分布 1:1504 / 4:74 / 5:243 / 9:70 …）；
   *  legacy 药水无 vid → 9（Item.DefaultToHealingPotion：useStyle=9 举杯）；
   *  其余 legacy 缺数据 → 1（挥砍）。返回值供 Renderer 姿势/身体行路由 */
  private heldUseStyle(def: (typeof ITEM_DEFS)[number] | null): number {
    if (!def) return 1;
    const vid = def.vid ?? viIdFromKey(def.key);
    if (vid >= 0) return itemFuncOfVid(vid)?.useStyle ?? 1;
    if (def.potion || def.heal) return 9; // 治疗类（含仅标 heal 的 legacy）
    // legacy 无 vid 的原版 4 族（Boss 召唤物/生命水晶，Item.cs SetDefaults useStyle=4）
    return LEGACY_USE_STYLE[def.key] ?? 1;
  }

  /** 使用动画时长（Player.itemAnimationMax = item.useAnimation）：
   *  vi_ 取 vanilla-itemcombat.useAnimation；legacy 工具 def.tool.speed；
   *  无数据 → 30（原版绝大多数消耗品 useAnimation 15-45 的中位近似） */
  private heldUseAnimation(def: (typeof ITEM_DEFS)[number] | null): number {
    if (!def) return 30;
    if (def.tool?.speed) return Math.max(10, def.tool.speed);
    const vid = def.vid ?? viIdFromKey(def.key);
    if (vid >= 0) {
      const ua = itemCombat(vid)?.useAnimation;
      if (ua && ua > 0) return Math.max(4, ua);
    }
    return 30;
  }

  /** 启动一次使用动画（itemAnimation>0 的本项目等价）。
   *  useStyle 5/13（弓/枪/法杖/短剑）附 aim 瞄准角——Renderer 持物姿势与
   *  bodyFrame 行档（Player.cs:35986 useStyle==5 的 itemRotation*direction 档）依赖 */
    };
  }

  /**
   * 智能光标每帧驱动（Player.cs:25159-25163 每帧 SmartCursorLookup + :28344-28374 Toggle/Hold 状态机）。
   * Ctrl 按下沿翻转（Toggle）/跟随（Hold）；切换播音效 12（menuTick）。
   * 必须在 updateUse 之前跑——同帧 lookup 结果即被挖掘/放置路径覆盖 tx/ty。
   */
  private updateSmartCursor() {
    const inp = this.input;
    const sc = this.smartCursor;
    const s = this.smartSettings();
    const controlSmart = inp.down('ControlLeft') || inp.down('ControlRight');
    if (sc.updateWanted(controlSmart, !!inp.mouseDown, s)) this.sfx.play('menuTick');
    const blocked = inp.uiBlocking || this.player.dead || !!this.minecart
      || this.renderer.fullMap.open || this.renderer.timeUiHover || this.renderer.weatherUiHover
      || this.annotateMode;
    if (blocked || !sc.wanted) { sc.showing = false; VUI.smartCursorOn = false; return; }
    const held = this.player.inv.heldItem();
    const heldDef = held ? ITEM_DEFS[held.id] : null;
    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
    const [mx, my] = this.camera.screenToWorld(inp.mouseX, inp.mouseY);
    const p = this.player;
    // 放置物才有 blockRange（原版 SmartCursorLookup :95-98 createWall/createTile 才加）；
    // 工具 tileBoost=0
    const placing = heldDef?.tile != null || heldDef?.wallId != null;
    const tb = placing
      ? (p.equipStats.tileRange ? 3 : 0) + (p.buffs.has(BuffType.Builder) ? 1 : 0)
      : 0;
    // EmptyTile 的占位实体（玩家 + 敌怪 + 城镇 NPC）
    const occupants: Array<{ x: number; y: number; w: number; h: number }> = [
      { x: p.x, y: p.y, w: p.w, h: p.h },
    ];
    for (const e of this.entities.enemies) occupants.push({ x: e.x, y: e.y, w: e.w, h: e.h });
    for (const e of this.entities.npcs) occupants.push({ x: e.x, y: e.y, w: e.w, h: e.h });
    sc.lookup({
      st: this.world.store,
      mouse: { x: mx, y: my },
      actor: { x: p.x, y: p.y, w: p.w, h: p.h, cx: p.cx, cy: p.cy, facing: p.facing },
      held: { def: heldDef, tool: tool ? { type: tool.type, power: tool.power ?? 0 } : null },
      settings: s,
      tileBoost: tb,
      wireToolMode: this.wireToolMode,
      occupants,
      controlUseItem: !!inp.mouseDown,
      // Step_AlchemySeeds 成熟药草判定（WorldGen.cs:66198-66225 IsAlchemyPlantHarvestable）
      // 所需世界态；Main.time 口径 = 白天 (t-0.25)*54000 / 夜晚 (t-0.75 / t+0.25)*32400
      alchemy: {
        dayTime: this.world.clock.isDay,
        bloodMoon: this.world.clock.bloodMoon,
        moonPhase: this.world.clock.moonPhase,
        raining: this.world.weather.raining,
        cloudAlpha: this.world.weather.cloudAlpha,
        time: vanillaMainTime(this.world.clock.timeOfDay),
        worldSurface: this.world.groundLevel,
        remixWorld: false,
        maxTilesY: this.world.store.h,
      },
    });
    // 指针切到 Cursors[12] 智能光标帧（Main.cs:47442-47513 num=11+smart.ToInt()）
    VUI.smartCursorOn = sc.showing;
      // 本作 swing = itemAnimation、player.useTime = itemTime；reuseDelay/channel/
      // pendingItemReuse 未实装
      isSlotEmpty: (i) => !p.inv.slots[i],
      onSelectionChanged: () => this.cb.onInventoryChanged(),
    };
    this.smartSelect.update(env, host);
    p.inv.selected = host.selected;
  }

  /**
   * inventory 0-57 的 Smart Select 槽画像（Player.cs:17326 的 inventory[i].type 等窄视图）。
   * 0-49 背包 + 50-53 钱币 + 54-57 弹药——case 4/5 信号枪弹药门扫到 57（:17374/:17410）。
   * 三力取 vanilla-itemfunc 全量（Hamaxe 斧+锤 / Drax 镐+斧 副力保留），legacy def.tool
   * 画像只覆盖自身类型主力（与 updateUse 的工具判定同序）。
   * 结果写入复用缓冲（每帧调用，防分配热点——perf-audit-2026-08 口径）。
   */
  private smartSelectSlots(): SmartSelectSlot[] {
    const inv = this.player.inv;
    for (let i = 0; i < INV_SIZE; i++) {
      const it = inv.slots[i];
      const buf = this._smartSelectSlots[i];
      if (!it) { this._smartSelectSlots[i] = EMPTY_SLOT; continue; }
      const def = ITEM_DEFS[it.id];
      this._smartSelectSlots[i] = smartSelectSlotOf(
        def,
        it.stack,
        itemFuncOfInternal(it.id, def?.key ?? ''),
        def?.tool ? { type: def.tool.type as 'pick' | 'axe' | 'hammer', power: def.tool.power ?? 0 } : null,
        buf === EMPTY_SLOT ? undefined : buf,
      );
    }
    return this._smartSelectSlots;
  }

  private updateUse(_dt: number) {
    const inp = this.input;
    // ---- 矿车坐骑（Mount 6 + Minecart.cs 轨道运动学；物理在 Minecart.fixedUpdate）----
    if (this.minecart) {
      const cart = this.minecart;
      const [mtx, mty] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
      const mType = this.world.store.get(mtx, mty);
      // R（坐骑键）：骑乘中下车（Player.TryToDismount 路径 :5768-5776）
      if (inp.down('KeyR') && !this.cartKeyLatch) {
        this.dismountMinecart();
        this.cartKeyLatch = true;
      }
      if (!inp.down('KeyR')) this.cartKeyLatch = false;
      // 右键轨道：骑乘中 → 下车（Player.cs:32806-32812 type==314 && mount.Cart 分支）
      if (inp.rightDown && mType === this.trackTile && this.trackTile !== 0) {
        this.dismountMinecart();
        this.input.rightDown = false;
      }
      if (cart.dead || !cart.mounted) {
        this.minecart = null;
        this.player.ridingCart = false;
        this.player.cart = null;
      }
      return;
    }
    // R（坐骑键）：未骑乘 + 附近有轨道 → QuickMinecart 上车（Player.cs:5796-5827：
    // 射程内取最近轨道格 + CanHitLine 视线门）
    if (inp.down('KeyR') && !this.cartKeyLatch && this.trackTile !== 0) {
      this.cartKeyLatch = true;
      this.tryQuickMinecart();
    }
    if (!inp.down('KeyR')) this.cartKeyLatch = false;
    // 全屏地图打开时鼠标交给地图（拖动/缩放/传送），不触发挖掘/放置/攻击/使用。
    // 时间调整按钮/面板悬停同理（renderer.timeUiHover 渲染期写入）
    if (inp.uiBlocking || this.player.dead || this.renderer.fullMap.open || this.renderer.timeUiHover || this.renderer.weatherUiHover) {
      this.mining = null;
      return;
    }
    const held = this.player.inv.heldItem();
    const heldDef = held ? ITEM_DEFS[held.id] : null;
    const [rawTx, rawTy] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
    let tx = rawTx, ty = rawTy;
    // 工具判定：legacy def.tool 优先；vi_ 镐/斧/锤经 vanilla-itemfunc 桥接（数值取 combat 表）
    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
    const vw2 = this.renderer.canvas.width, vh2 = this.renderer.canvas.height;

    // 右键轨道：(最优先,防 NPC 交谈拦截) → 附近宝箱 → NPC 交谈 → 交互
    //（Player.cs:32806-32812：右键轨道格 → LaunchMinecartHook——与手持物品无关，
    //  用"最佳矿车"（装备槽 > 手持 > 背包）；矿车是坐骑召唤物，不消耗）
    const type = this.world.store.get(tx, ty);
    if (inp.rightDown && !this.minecart && type === this.trackTile && this.trackTile !== 0) {
      const tex = this.bestCartTexture();
      if (tex) {
        if (this.mountMinecartAt(tx, ty, tex)) this.input.rightDown = false;
        return;
      }
    }
    if (inp.rightDown) {
      // 光标格本身是蜥蜴祭坛时跳过 ±1 格宝箱搜索——神庙宝箱全庙随机散布可能
      // 贴着祭坛，原版无 ±1 搜索（点到箱本体才开箱）；不跳过则右键祭坛变成开箱
      const cursorIsAltar = type === TILE_BY_KEY['v_237_lihzahrd_altar'];
      const nearChest = cursorIsAltar ? null : this.findChestNear(tx, ty);
      if (nearChest) {
        this.tryOpenChest(nearChest);
        this.input.rightDown = false;
      } else if (this.talkToNearbyNpc(tx, ty)) {
        this.input.rightDown = false;
      } else if (heldDef && viIdFromKey(heldDef.key) === 5289) {
        // 矿车升级套件（Item 5289 MinecartPowerup → Player.unlockedSuperCart = true）：
        // 永久解锁 SuperCart 档（runSpeed 20/accel 0.1/jump 5.15，Mount.cs:371-379），
        // 持久化于世界 flags；已解锁时不再消耗
        if (!this.superCartUnlocked()) {
          (this.world.flags as Record<string, boolean>).superCart = true;
          this.player.inv.removeAt(this.player.inv.selected, 1);
          this.cb.onInventoryChanged();
          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.SuperCartUnlocked'));
        }

```


---

## 🤖 Assistant · 2026-08-12T15:53:02.110Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now let me look at:
- itemFuncTool (vanilla-itemfunc bridge)
- viIdFromKey
- magic/ranged defs and combatWeapon
- placeTile / place chain (item.tile vs createTile)
- SpriteAtlas atlasIconForKey / VANILLA_ITEM_ICON_MAP
- net/protocol item ids

Let me grep those.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:02.927Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"itemFuncTool\\|viIdFromKey\\|itemFuncOfInternal\\|itemFuncOfVid\" src --include=\"*.ts\" | grep -v \"idNames.generated\" | head -30; echo \"==== vanillaItemStats/Combat\"; sed -n '1,60p' src/data/vanillaItemStats.ts; echo \"==== func\"; cat src/data/vanillaItemFunc.ts",
 "description": "Read vanilla item bridges"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:03.056Z

**📎 ToolResult**

```
src/core/Game.ts:76:import { itemCombat, AMMO_ARROW, combatWeapon, thrownCombat, viIdFromKey, projGravity, rangedAmmoWeapon, type CombatWeapon } from '../data/vanillaItemCombat';
src/core/Game.ts:77:import { itemFuncOfVid, itemFuncOfInternal } from '../data/vanillaItemFunc';
src/core/Game.ts:338:  const vid = viIdFromKey(key);
src/core/Game.ts:1084:    const vid = viIdFromKey(key);
src/core/Game.ts:2149:        if (!heldDef || viIdFromKey(heldDef.key) !== MUSIC_BOX_EMPTY_VID) continue;
src/core/Game.ts:2322:      const fVid = fDef ? (fDef.vid ?? viIdFromKey(fDef.key)) : -1;
src/core/Game.ts:2986:      const gvid = heldDef.key === 'torch' ? -1 : viIdFromKey(heldDef.key);
src/core/Game.ts:3001:    const heldVid0 = heldDef ? (heldDef.key === 'torch' ? 8 : viIdFromKey(heldDef.key)) : -1;
src/core/Game.ts:3012:      const vid = heldDef.key === 'torch' ? 8 : viIdFromKey(heldDef.key);
src/core/Game.ts:3092:      const vid = viIdFromKey(def.key);
src/core/Game.ts:3226:      const f = itemFuncOfVid(+m[1]);
src/core/Game.ts:3239:  private itemFuncTool(id: number): (typeof ITEM_DEFS)[number]['tool'] {
src/core/Game.ts:3244:    const f = itemFuncOfVid(+m[1]);
src/core/Game.ts:3266:    const ff = fm ? itemFuncOfVid(+fm[1]) : null;
src/core/Game.ts:3277:    const vid = def.vid ?? viIdFromKey(def.key);
src/core/Game.ts:3278:    if (vid >= 0) return itemFuncOfVid(vid)?.useStyle ?? 1;
src/core/Game.ts:3290:    const vid = def.vid ?? viIdFromKey(def.key);
src/core/Game.ts:3360:    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
src/core/Game.ts:3476:        itemFuncOfInternal(it.id, def?.key ?? ''),
src/core/Game.ts:3527:    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
src/core/Game.ts:3551:      } else if (heldDef && viIdFromKey(heldDef.key) === 5289) {
src/core/Game.ts:3824:      const ff = fm ? itemFuncOfVid(+fm[1]) : null;
src/core/Game.ts:3865:      const bowVid = rg?.vid ?? viIdFromKey(heldDef.key);
src/core/Game.ts:3871:        d.ammoId ?? (d.vid != null || viIdFromKey(d.key) >= 0 ? itemCombat(d.vid ?? viIdFromKey(d.key))?.ammo ?? 0 : 0);
src/core/Game.ts:3884:        const ammoC = ammoDef.vid != null || viIdFromKey(ammoDef.key) >= 0
src/core/Game.ts:3885:          ? itemCombat(ammoDef.vid ?? viIdFromKey(ammoDef.key)) : null;
src/core/Game.ts:3933:      const vid = heldDef.vid ?? viIdFromKey(heldDef.key);
src/core/Game.ts:4126:      const ff = fm ? itemFuncOfVid(+fm[1]) : null;
src/core/Game.ts:4140:            const df = dm ? itemFuncOfVid(+dm[1]) : null;
src/core/Game.ts:7116:    const tool = heldDef.tool ?? this.itemFuncTool(held.id);
==== vanillaItemStats/Combat
// 盔甲/配饰基础属性运行时（tools/extract-equip-prefix.mjs → vanilla-itemstats.json）。
// vi_ 批次物品注册期无 armor/accessory 字段——槽位归属与防御值以本表为权威：
//   s: 'h'|'b'|'l' 盔甲部位（headSlot/bodySlot/legSlot 赋值即归属，Item.cs SetDefaults）
//   def: 防御值（defense = N 字面量）
//   acc: 1 功能配饰 / 0 社交配饰（vanity=true；无功能效果）
import statsJson from './vanilla-itemstats.json';
import { ITEM_DEFS } from './items';

export interface VanillaItemStat {
  s?: 'h' | 'b' | 'l';
  def?: number;
  acc?: 0 | 1;
  life?: number;   // 生命回复（Item.lifeRegen，再生手环族）
  wing?: number;   // 翅膀槽（Item.wingSlot>0 即翅膀；飞行属性查 vanilla-wingstats）
  hs?: number; bs?: number; ls?: number; // 盔甲绘制槽序号（套装匹配键，Player.cs UpdateArmorSets）

  str?: number;    // 悠悠球线（Item.stringColor>0 → yoyoString，Player.cs:14170）
}

const STATS = statsJson as Record<string, VanillaItemStat>;

/** 原版 item id → 盔甲/配饰属性 */
export function vanillaStatOfVid(vid: number): VanillaItemStat | null {
  return STATS[String(vid)] ?? null;
}

/** 内部 item id → 属性（ITEM_DEFS 缓存） */
const STAT_BY_IID = (() => {
  const m = new Map<number, VanillaItemStat>();
  for (let i = 0; i < ITEM_DEFS.length; i++) {
    const d = ITEM_DEFS[i];
    if (!d) continue;
    const vid = d.vid ?? (d.key.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
    if (vid < 0) continue;
    const s = STATS[String(vid)];
    if (s) m.set(i, s);
  }
  return m;
})();

export function statOfInternal(id: number): VanillaItemStat | null {
  return STAT_BY_IID.get(id) ?? null;
}

/** 盔甲部位槽序（0 头 / 1 身 / 2 腿；非盔甲 -1） */
export function armorSlotIndexOfInternal(id: number): number {
  const s = STAT_BY_IID.get(id)?.s;
  return s === 'h' ? 0 : s === 'b' ? 1 : s === 'l' ? 2 : -1;
}

/** 功能配饰判定（ItemSlot context 10：accessory && !vanity） */
export function isFunctionalAccessory(id: number): boolean {
  return STAT_BY_IID.get(id)?.acc === 1;
}

/** 任意配饰（含社交）判定 */
export function isAnyAccessory(id: number): boolean {
  const acc = STAT_BY_IID.get(id)?.acc;
  return acc !== undefined;
}
==== func
// 道具功能画像运行时（tools/extract-itemfunc.mjs 从 1456 Item.cs 提取）。
// 用途：vi_ 批次物品的功能桥接——工具（镐/斧/锤挖掘）、药水（治疗/魔力/Buff）。
export interface ItemFunc {
  melee?: number; ranged?: number; magic?: number; summon?: number;
  noMelee?: number; damage?: number; mana?: number;
  pick?: number; axe?: number; hammer?: number;
  createTile?: number; createWall?: number; placeStyle?: number;
  consumable?: number; potion?: number;
  healLife?: number; healMana?: number;
  buffType?: number; buffTime?: number;
  ammo?: number; useAmmo?: number; notAmmo?: number;
  shoot?: number; channel?: number; holdStyle?: number; torch?: number;
  useStyle?: number; knockBack?: number; autoReuse?: number;
  fishingPole?: number;  // 钓竿力度（9 支；抛竿入口判定）
  bait?: number;        // 鱼饵力度（29 种；消耗率 1/(1+bait/6)）
}

import funcJson from './vanilla-itemfunc.json';

const FUNC = funcJson as Record<string, ItemFunc>;

/** 原版 item id → 功能画像 */
export function itemFuncOfVid(vid: number): ItemFunc | null {
  return FUNC[String(vid)] ?? null;
}

/** 内部 item id（vi_ key）→ 功能画像 */
export function itemFuncOfInternal(id: number, key: string): ItemFunc | null {
  const m = /^vi_(\d+)_/.exec(key);
  return m ? FUNC[m[1]] ?? null : null;
}

```


---

## 🤖 Assistant · 2026-08-12T15:53:03.393Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"atlasIconForKey\\|VANILLA_ITEM_ICON_MAP\\|iconUrl\\|vicon\" src --include=\"*.ts\" | grep -v idNames | head -40",
 "description": "Find icon resolution chain"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:03.468Z

**📎 ToolResult**

```
src/ui/BestiaryPanel.ts:602:  /** 掉落行物品小图标（atlas.vicon 懒载未就绪时仅文字） */
src/ui/BestiaryPanel.ts:606:    const ar = atlas.vicon(itemId);
src/ui/UI.ts:10:import { atlasIconForKey } from '../assets/SpriteAtlas';
src/ui/UI.ts:42:function iconUrl(game: Game, id: number): string {
src/ui/UI.ts:48:      const ar = atlasIconForKey(game.atlas, def.key);
src/ui/UI.ts:975:      img.src = iconUrl(this.game, this.heldStack.id);
src/ui/UI.ts:981:    const url = iconUrl(this.game, this.heldStack.id);
src/ui/UI.ts:1153:        img.src = iconUrl(this.game!, e.id);
src/ui/UI.ts:1272:      img.src = iconUrl(this.game, this.reforgeItem.id);
src/ui/UI.ts:1377:        img.src = iconUrl(this.game!, e.id);
src/ui/UI.ts:1410:      img.src = iconUrl(game, game.itemId(outKey));
src/ui/UI.ts:1466:      im.src = iconUrl(this.game, this.game.player.inv.trash!.id);
src/ui/UI.ts:1775:      if (iconId && !ui.icon.src) ui.icon.src = iconUrl(this.game, iconId);
src/ui/UI.ts:2056:      img.src = iconUrl(this.game, content.id);
src/ui/UI.ts:2139:      img.src = iconUrl(game, game.itemId(r.out));
src/ui/UI.ts:2199:      img.src = iconUrl(game, game.itemId(outKey));
src/ui/UI.ts:2262:        img.src = iconUrl(this.game, this.game.itemId(k));
src/ui/UI.ts:2481:      iconUrl: this.game ? iconUrl(this.game, it.vanillaId) || '' : '',
src/ui/NpcDialog.ts:17:  iconUrl: string | null;
src/ui/NpcDialog.ts:145:        ${it.iconUrl ? `<img src="${it.iconUrl}">` : '<span style="width:26px;height:26px;display:inline-block"></span>'}
src/core/Game.ts:150:import { SpriteAtlas, VANILLA_ITEM_ICON_MAP, atlasIconForKey } from '../assets/SpriteAtlas';
src/core/Game.ts:1404:    // vicon→ensureVImage 懒加载（未就绪回退程序化图标，paintSlot 每次刷新自愈升级）；
src/core/Game.ts:1415:      const vid = VANILLA_ITEM_ICON_MAP[def.key] ?? (def.key.startsWith('vi_') ? parseInt(def.key.slice(3), 10) : NaN);
src/core/Game.ts:1550:        // 图块表首帧（atlasIconForKey → vframeAt），此前只认 Item_Atlas → 开宝箱
src/core/Game.ts:7134:    const ar = this.renderer?.atlas ? atlasIconForKey(this.renderer.atlas, ITEM_DEFS[held.id].key) : null;
src/render/Renderer.ts:10:import { atlasIconForKey, VANILLA_ITEM_ICON_MAP } from '../assets/SpriteAtlas';
src/render/Renderer.ts:35:    const vid = VANILLA_ITEM_ICON_MAP[key] ?? (key.startsWith('vi_') ? parseInt(key.slice(3), 10) : NaN);
src/render/Renderer.ts:676:    return atlasIconForKey(this.atlas, def.key);
src/assets/SpriteAtlas.ts:183:    // (onWorldReady 之前完成,首帧 chunk 烘焙无回退);物品图标 → vicon 按需
src/assets/SpriteAtlas.ts:325:  vicon(itemId: number): DrawRect | null {
src/assets/SpriteAtlas.ts:486:export function atlasIconForKey(atlas: SpriteAtlas, key: string): DrawRect | null {
src/assets/SpriteAtlas.ts:487:  const vid = VANILLA_ITEM_ICON_MAP[key];
src/assets/SpriteAtlas.ts:488:  if (vid !== undefined) return atlas.vicon(vid);
src/assets/SpriteAtlas.ts:492:    if (Number.isFinite(id)) return atlas.vicon(id);
src/assets/SpriteAtlas.ts:508:export const VANILLA_ITEM_ICON_MAP: Record<string, number> = {
src/data/items.ts:736:// ---- 阶段 5:原版物品全量注册(6146 件,图标走 atlas.vicon(id) 回退) ----

```


---

## 🤖 Assistant · 2026-08-12T15:53:05.248Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '470,560p' ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts",
 "description": "Read atlasIconForKey and VANILLA_ITEM_ICON_MAP"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:05.425Z

**📎 ToolResult**

```
    const entry = this.data.files[file];
    if (!img || !entry) return null;
    const s = entry.sprites.find((x) => x.name === sprite);
    if (!s) return null;
    return { img, sx: s.x, sy: img.height - s.y - s.h, sw: s.w, sh: s.h };
  }

  animFrames(anim: string): DrawRect[] {
    const frames = this.resources.anims[anim] ?? [];
    return frames.map((f) => this.rect(f.file, f.sprite)).filter(Boolean) as DrawRect[];
  }
}

// ---- 物品图标：一律原版 Item_N（旧 Maples UI/ 图标层已整体移除） ----
import { TILE_BY_KEY, TILE_DEFS } from '../data/tiles';

export function atlasIconForKey(atlas: SpriteAtlas, key: string): DrawRect | null {
  const vid = VANILLA_ITEM_ICON_MAP[key];
  if (vid !== undefined) return atlas.vicon(vid);
  // 阶段 5:vi_<id>_* 全量物品回退原版图标
  if (key.startsWith('vi_')) {
    const id = parseInt(key.slice(3), 10);
    if (Number.isFinite(id)) return atlas.vicon(id);
  }
  // 阶段 5:place_v_* 放置物品回退用图块贴图首帧作图标
  if (key.startsWith('place_v_')) {
    const tk = key.slice('place_'.length);
    const tid = TILE_BY_KEY[tk];
    if (tid !== undefined) {
      const td = TILE_DEFS[tid];
      // vframeAt 而非 vframe:窄条表(如压板 135 的 16×200 竖条)cols=0 会让 vframe 判越界
      if (td?.vanilla) return atlas.vframeAt(td.vanilla.sheet, 0, 0) ?? atlas.vframe(td.vanilla.sheet, 0, 0);
    }
  }
  return null;
}

// 我们的 item key → 原版物品图标 id（TEdit items.json 核实；Maples 缺图标的用这层）
export const VANILLA_ITEM_ICON_MAP: Record<string, number> = {
  dirt_block: 2, stone_block: 3, sand_block: 169, snow_block: 593,
  platform: 94, door: 25, chest: 48, torch: 8,
  mushroom_item: 5, gel: 23, acorn: 27,
  copper_ore: 12, iron_ore: 11, silver_ore: 14, gold_ore: 13,
  copper_bar: 20, iron_bar: 22, silver_bar: 21, gold_bar: 19,
  lens: 38, suspicious_eye: 43,
  iron_sword: 4,   // IronBroadsword（ItemID.cs:1547）
  // 电路工具(id-maps items.json 核实:530 电线/509,850,851,3612 四色扳手/510 钢丝钳/
  // 849 致动器/3620 致动魔杖/3625 五彩扳手/3611 宏伟蓝图)
  wire: 530, red_wrench: 509, blue_wrench: 850, green_wrench: 851, yellow_wrench: 3612,
  wire_cutter: 510, actuator_item: 849, actuation_rod: 3620,
  multicolor_wrench: 3625, grand_design: 3611,
  lesser_healing_potion: 28, coin_copper: 71,
  heal_potion: 188, agility_potion: 290, ironskin_potion: 292,
  thorns_potion: 301, regen_potion: 289,
  wood_sword: 24, wood_hammer: 196,
  copper_pickaxe: 3509, copper_axe: 3506, copper_sword: 3508, copper_hammer: 3505,
  iron_pickaxe: 1, iron_axe: 10, silver_pickaxe: 3515, silver_axe: 3512,
  silver_hammer: 3511, gold_pickaxe: 3521, gold_axe: 3518, gold_hammer: 3517,
  // 盔甲三件套（原版 id：胫甲 76-79 / 胸甲 80-83 / 头盔 89-92）
  copper_greaves: 76, iron_greaves: 77, silver_greaves: 78, gold_greaves: 79,
  copper_chainmail: 80, iron_chainmail: 81, silver_chainmail: 82, gold_chainmail: 83,
  copper_helmet: 89, iron_helmet: 90, silver_helmet: 91, gold_helmet: 92,
  coin_silver: 72, coin_gold: 73,
  // ---- 原版批次新材料 / 方块 / 家具 ----
  tin_ore: 699, lead_ore: 700, tungsten_ore: 701, platinum_ore: 702,
  tin_bar: 703, lead_bar: 704, tungsten_bar: 705, platinum_bar: 706,
  demonite_ore: 56, meteorite: 116, hellstone: 174,
  crimtane_ore: 880, cobalt_ore: 364, mythril_ore: 365, adamantite_ore: 366,
  palladium_ore: 1104, orichalcum_ore: 1105, titanium_ore: 1106, chlorophyte_ore: 947,
  sapphire: 177, ruby: 178, emerald: 179, topaz: 180, amethyst: 181, diamond: 182,
  ice_block: 664, ice_brick: 883, snow_brick: 594,
  sandstone_block: 3271, hardened_sand_block: 3272, desert_fossil: 3347,
  clay_block: 133, glass: 170, obsidian: 173, gray_brick: 129, red_brick: 131,
  mud_block: 176, silt_block: 424,
  table: 32, chair: 34, bed: 224, bookcase: 354, grandfather_clock: 359,
  piano: 333, dresser: 334, bench: 335, bathtub: 336, keg: 352, cooking_pot: 345,
  clay_pot: 222, tombstone: 321, life_crystal: 29,
  candle: 105, chandelier: 106, lantern: 136, candelabra: 349,
  chinese_lantern: 344, skull_lantern: 347, water_candle: 148,
  bomb: 166, rope: 965,
  // wld 导入补全物品图标
  vi_2350_recall_potion: 2350,
  vi_188_healing_potion: 188,
  vi_282_glowstick: 282,
  vi_41_flaming_arrow: 41,
  vi_167_dynamite: 167,
  vi_279_throwing_knife: 279,
  vi_51_jester_s_arrow: 51,
  vi_19_gold_bar: 19,
  vi_302_water_walking_potion: 302,
  vi_305_gravitation_potion: 305,

```


---

## 🤖 Assistant · 2026-08-12T15:53:05.741Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '30,60p' src/ui/UI.ts; echo ====; sed -n '1390,1440p' src/core/Game.ts",
 "description": "Read UI iconUrl and Game icon init"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:05.857Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
function prefixDisplayName(prefix: number): string {
  const key = PREFIX_NAMES[String(prefix)];
  if (!key) return '';
  const t = Lang.text(`Prefix.${key}`);
  return t && t !== `Prefix.${key}` ? t : key;
}

/** 词缀后伤害值（Item.Prefix :551：damage = round(damage × dmg)） */
function prefixedDamage(def: (typeof ITEM_DEFS)[number], prefix?: number): number {
  if (!def.tool?.damage || !prefix) return def.tool?.damage ?? 0;
  return Math.max(1, Math.round(def.tool.damage * prefixStat(prefix).dmg));
}
function iconUrl(game: Game, id: number): string {
  let url = iconCache.get(id);
  if (!url) {
    // 优先原版素材图标（合成 32×32 dataURL）
    const def = ITEM_DEFS[id];
    if (game.atlas && def) {
      const ar = atlasIconForKey(game.atlas, def.key);
      if (ar) {
        const c = document.createElement('canvas');
        c.width = 32; c.height = 32;
        const cx = c.getContext('2d')!;
        cx.imageSmoothingEnabled = false;
        const s = Math.min(32 / ar.sw, 32 / ar.sh);
        const w = ar.sw * s, h = ar.sh * s;
        cx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, (32 - w) / 2, (32 - h) / 2, w, h);
        url = c.toDataURL();
        iconCache.set(id, url);
        return url;
      }
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-12T15:53:08.204Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me see the rest of VANILLA_ITEM_ICON_MAP (local keys remaining) and also check what fallback exists for keys not in map (ItemIconGen?). UI iconUrl falls back presumably to procedural. Let me check the remaining part of the map and ItemIconGen usage.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:08.823Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '560,650p' src/assets/SpriteAtlas.ts; echo \"=== total lines of map\"; awk '/export const VANILLA_ITEM_ICON_MAP/,/^};/' src/assets/SpriteAtlas.ts | grep -c \":\"",
 "description": "Read rest of VANILLA_ITEM_ICON_MAP"
}
```


---

## 🤖 Assistant · 2026-08-12T15:53:09.486Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ItemIconGen\\|procedural\\|iconFor\" src --include=\"*.ts\" | grep -v idNames | head -20; echo ====; sed -n '1,60p' src/assets/ItemIconGen.ts",
 "description": "Find procedural icon fallback"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:13.411Z

**📎 ToolResult**

```
  vi_305_gravitation_potion: 305,
  vi_43_suspicious_looking_eye: 43,
  vi_296_spelunker_potion: 296,
  vi_299_night_owl_potion: 299,
  vi_965_rope: 965,
  vi_303_archery_potion: 303,
  vi_304_hunter_potion: 304,
  vi_50_magic_mirror: 50,
  vi_42_shuriken: 42,
  vi_295_featherfall_potion: 295,
  vi_53_cloud_in_a_bottle: 53,
  vi_2329_dangersense_potion: 2329,
  vi_40_wooden_arrow: 40,
  vi_975_shoe_spikes: 975,
  vi_54_hermes_boots: 54,
  vi_301_thorns_potion: 301,
  vi_49_band_of_regeneration: 49,
  vi_2326_titan_potion: 2326,
  vi_297_invisibility_potion: 297,
  vi_166_bomb: 166,
  vi_5011_mace: 5011,
  vi_4425_shark_bait: 4425,
  vi_2351_teleportation_potion: 2351,
  vi_4460_sandcastle_bucket: 4460,
  vi_168_grenade: 168,
  vi_227_restoration_potion: 227,
  vi_930_flare_gun: 930,
  vi_931_flare: 931,
  vi_997_extractinator: 997,
  vi_52_angel_statue: 52,
  vi_265_hellfire_arrow: 265,
  vi_298_shine_potion: 298,
  vi_5007_dead_man_s_sweater: 5007,
  vi_117_meteorite_bar: 117,
  vi_186_breathing_reed: 186,
  vi_329_shadow_key: 329,
  vi_974_ice_torch: 974,
  vi_2322_mining_potion: 2322,
  vi_4915_tungsten_bullet: 4915,
  vi_946_umbrella: 946,
  vi_939_web_slinger: 939,
  vi_4870_potion_of_return: 4870,
  vi_288_obsidian_skin_potion: 288,
  vi_31_bottle: 31,
  vi_211_feral_claws: 211,
  vi_4404_inner_tube: 4404,
  vi_187_flipper: 187,
  vi_2198_ice_machine: 2198,
  vi_274_dark_lance: 274,
  vi_285_aglet: 285,
  vi_213_staff_of_regrowth: 213,
  vi_964_boomstick: 964,
  vi_1293_lihzahrd_power_cell: 1293,
  vi_2195_lihzahrd_furnace: 2195,
  vi_2766_solar_tablet_fragment: 2766,
  vi_300_battle_potion: 300,
  vi_2348_inferno_potion: 2348,
  vi_218_flamelash: 218,
  vi_3019_hellwing_bow: 3019,
  vi_112_flower_of_fire: 112,
  vi_220_sunfury: 220,
  vi_4345_can_of_worms: 4345,
  vi_953_climbing_claws: 953,
  vi_3069_wand_of_sparking: 3069,
  vi_212_anklet_of_the_wind: 212,
  vi_2204_honey_dispenser: 2204,
  vi_277_trident: 277,
  vi_863_water_walking_boots: 863,
  vi_751_cloud: 751,
  vi_155_muramasa: 155,
  vi_289_regeneration_potion: 289,
  vi_906_lava_charm: 906,
  vi_4055_dunerider_boots: 4055,
  vi_724_ice_blade: 724,
  vi_670_ice_boomerang: 670,
  vi_4061_storm_spear: 4061,
  vi_987_blizzard_in_a_bottle: 987,
  vi_4551_slice_of_hell_cake: 4551,
  vi_5010_treasure_magnet: 5010,
  vi_2323_heartreach_potion: 2323,
  vi_2345_lifeforce_potion: 2345,
  vi_290_swiftness_potion: 290,
  vi_291_gills_potion: 291,
  vi_280_spear: 280,
  vi_2325_builder_potion: 2325,
  vi_284_wooden_boomerang: 284,
  vi_2192_bone_welder: 2192,
  vi_5234_remnants_of_devotion: 5234,
  vi_156_cobalt_shield: 156,
  vi_157_aqua_scepter: 157,
  vi_163_blue_moon: 163,
=== total lines of map
424

```


---

## 👤 User(sidechain) · 2026-08-12T15:53:13.477Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
src/assets/AssetGen.ts:3:import { generateAllItemIcons } from './ItemIconGen';
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-12T15:53:15.641Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The map has local keys at the beginning. Let me get the full local-key portion of the map (lines 508-547ish plus more). Let me grep the map for local keys only.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:16.085Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk '/export const VANILLA_ITEM_ICON_MAP/,/^};/' src/assets/SpriteAtlas.ts | grep -vE \"vi_|place_v_\" ",
 "description": "List local keys in icon map"
}
```


---

## 🤖 Assistant · 2026-08-12T15:53:16.750Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,50p' src/assets/ItemIconGen.ts; echo \"=== AssetGen\"; sed -n '1,40p' src/assets/AssetGen.ts; echo \"=== who uses AssetGen\"; grep -rn \"AssetGen\\|generateAllItemIcons\" src --include=\"*.ts\"",
 "description": "Read ItemIconGen and AssetGen"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:26.581Z

**📎 ToolResult**

```
export const VANILLA_ITEM_ICON_MAP: Record<string, number> = {
  dirt_block: 2, stone_block: 3, sand_block: 169, snow_block: 593,
  platform: 94, door: 25, chest: 48, torch: 8,
  mushroom_item: 5, gel: 23, acorn: 27,
  copper_ore: 12, iron_ore: 11, silver_ore: 14, gold_ore: 13,
  copper_bar: 20, iron_bar: 22, silver_bar: 21, gold_bar: 19,
  lens: 38, suspicious_eye: 43,
  iron_sword: 4,   // IronBroadsword（ItemID.cs:1547）
  // 电路工具(id-maps items.json 核实:530 电线/509,850,851,3612 四色扳手/510 钢丝钳/
  // 849 致动器/3620 致动魔杖/3625 五彩扳手/3611 宏伟蓝图)
  wire: 530, red_wrench: 509, blue_wrench: 850, green_wrench: 851, yellow_wrench: 3612,
  wire_cutter: 510, actuator_item: 849, actuation_rod: 3620,
  multicolor_wrench: 3625, grand_design: 3611,
  lesser_healing_potion: 28, coin_copper: 71,
  heal_potion: 188, agility_potion: 290, ironskin_potion: 292,
  thorns_potion: 301, regen_potion: 289,
  wood_sword: 24, wood_hammer: 196,
  copper_pickaxe: 3509, copper_axe: 3506, copper_sword: 3508, copper_hammer: 3505,
  iron_pickaxe: 1, iron_axe: 10, silver_pickaxe: 3515, silver_axe: 3512,
  silver_hammer: 3511, gold_pickaxe: 3521, gold_axe: 3518, gold_hammer: 3517,
  // 盔甲三件套（原版 id：胫甲 76-79 / 胸甲 80-83 / 头盔 89-92）
  copper_greaves: 76, iron_greaves: 77, silver_greaves: 78, gold_greaves: 79,
  copper_chainmail: 80, iron_chainmail: 81, silver_chainmail: 82, gold_chainmail: 83,
  copper_helmet: 89, iron_helmet: 90, silver_helmet: 91, gold_helmet: 92,
  coin_silver: 72, coin_gold: 73,
  // ---- 原版批次新材料 / 方块 / 家具 ----
  tin_ore: 699, lead_ore: 700, tungsten_ore: 701, platinum_ore: 702,
  tin_bar: 703, lead_bar: 704, tungsten_bar: 705, platinum_bar: 706,
  demonite_ore: 56, meteorite: 116, hellstone: 174,
  crimtane_ore: 880, cobalt_ore: 364, mythril_ore: 365, adamantite_ore: 366,
  palladium_ore: 1104, orichalcum_ore: 1105, titanium_ore: 1106, chlorophyte_ore: 947,
  sapphire: 177, ruby: 178, emerald: 179, topaz: 180, amethyst: 181, diamond: 182,
  ice_block: 664, ice_brick: 883, snow_brick: 594,
  sandstone_block: 3271, hardened_sand_block: 3272, desert_fossil: 3347,
  clay_block: 133, glass: 170, obsidian: 173, gray_brick: 129, red_brick: 131,
  mud_block: 176, silt_block: 424,
  table: 32, chair: 34, bed: 224, bookcase: 354, grandfather_clock: 359,
  piano: 333, dresser: 334, bench: 335, bathtub: 336, keg: 352, cooking_pot: 345,
  clay_pot: 222, tombstone: 321, life_crystal: 29,
  candle: 105, chandelier: 106, lantern: 136, candelabra: 349,
  chinese_lantern: 344, skull_lantern: 347, water_candle: 148,
  bomb: 166, rope: 965,
  // wld 导入补全物品图标
  // ---- 旧 UI 移除迁移补全（2026-08-09，全部 id 经 TEdit items.json 核实；
  //      木镐/木斧原版不存在，用铜镐 3509/铜斧 3506 代位） ----
  wood: 9, workbench: 36, furnace: 33, anvil: 35,
  wood_pickaxe: 3509, wood_axe: 3506, iron_hammer: 7,
  silver_sword: 3514, gold_sword: 3520, iron_bow: 99,
  wooden_bow: 39, wooden_arrow: 40, flaming_arrow: 41,
  tin_pickaxe: 3503, tin_axe: 3500, tin_sword: 3502,
  lead_pickaxe: 3497, lead_axe: 3494, lead_sword: 3496,
  tungsten_pickaxe: 3491, tungsten_axe: 3488, tungsten_sword: 3490,
  platinum_pickaxe: 3485, platinum_axe: 3482, platinum_sword: 3484,
  corrupt_grass_seeds: 59, crimson_grass_seeds: 2171,
  jungle_grass_seeds: 195, mushroom_grass_seeds: 194,
  empty_bucket: 205, water_bucket: 206, lava_bucket: 207, honey_bucket: 1128,
  lucky_horseshoe: 158, feral_claws: 211,
  minecart_item: 2343, wand_of_sparking: 3069, amethyst_bolt: 739,  // 紫晶法杖=Amethyst Staff
  worm_food: 70, bloody_spine: 1331, slime_crown: 560,
};

```


---

## 👤 User(sidechain) · 2026-08-12T15:53:26.671Z

**📎 ToolResult**

```
// 物品图标程序化生成（16×16）
import { ITEM_DEFS, ITEM_BY_KEY } from '../data/items';
import { MATS, shade } from './Palette';
import { T, TILE_BY_KEY } from '../data/tiles';
import { RNG, hash2 } from '../core/rng';

function mk(w: number, h: number): [HTMLCanvasElement, CanvasRenderingContext2D] {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const ctx = c.getContext('2d')!;
  return [c, ctx];
}

function tileThumb(tileKey: string): HTMLCanvasElement {
  // 从 tile sheet 提取一个 16×16 缩样（用 mask=0 全边框帧）
  const [c, ctx] = mk(16, 16);
  // 直接画简化方块
  const m = matForTile(tileKey);
  const px = ctx.createImageData(16, 16);
  for (let y = 0; y < 16; y++) {
    for (let x = 0; x < 16; x++) {
      const n = hash2(x, y, TILE_BY_KEY[tileKey] ?? 3);
      let f = 0.92 + n * 0.16;
      if (y === 0 || x === 0) f *= 1.18;
      if (y === 15 || x === 15) f *= 0.82;
      const v = parseInt(shade(m.base, f).slice(1), 16);
      const i = (y * 16 + x) * 4;
      px.data[i] = (v >> 16) & 255; px.data[i + 1] = (v >> 8) & 255; px.data[i + 2] = v & 255; px.data[i + 3] = 255;
    }
  }
  ctx.putImageData(px, 0, 0);
  return c;
}

function matForTile(tileKey: string) {
  switch (tileKey) {
    case 'dirt': return MATS.dirt;
    case 'stone': return MATS.stone;
    case 'sand': return MATS.sand;
    case 'snow': return MATS.snow;
    case 'wood': return MATS.wood;
    case 'platform': return MATS.wood;
    default: return MATS.wood;
  }
}

function drawTool(kind: 'pick' | 'axe' | 'sword' | 'hammer', metal: Mat): HTMLCanvasElement {
  const [c, ctx] = mk(16, 16);
  const px = ctx.createImageData(16, 16);
  const set = (x: number, y: number, col: string) => {
=== AssetGen
// 素材总装：启动期一次性生成全部贴图
import { generateAllTileSheets, TileSheetEntry } from './TileSheetGen';
import { generateAllItemIcons } from './ItemIconGen';
import { generatePlayerSheet, generateEnemySprites, EnemySprite, PLAYER_FRAME_W, PLAYER_FRAME_H } from './CharacterSheetGen';

export interface AssetBundle {
  tileSheets: Map<number, TileSheetEntry>;
  itemIcons: Map<number, HTMLCanvasElement>;
  playerSheet: HTMLCanvasElement;
  enemySprites: Map<string, EnemySprite>;
  playerFrameW: number;
  playerFrameH: number;
}

export function buildAssets(): AssetBundle {
  // 全局单例:程序化生成是确定性的(每次内容完全相同),此前每个 Game 实例重建
  // ——物品图标 ~6700 张 canvas + 全部 tile 表/角色表/敌人贴图,进一次世界泄漏一套,
  // 多次读档累积显存最终 contextlost 风暴(2026-08-10 双 trace 实证)。生成一次全程复用
  shared ??= {
    tileSheets: generateAllTileSheets(),
    itemIcons: generateAllItemIcons(),
    playerSheet: generatePlayerSheet(),
    enemySprites: generateEnemySprites(),
    playerFrameW: PLAYER_FRAME_W,
    playerFrameH: PLAYER_FRAME_H,
  };
  return shared;
}
let shared: AssetBundle | null = null;
=== who uses AssetGen
src/core/Game.ts:9:import { buildAssets, AssetBundle } from '../assets/AssetGen';
src/render/Renderer.ts:7:import type { AssetBundle } from '../assets/AssetGen';
src/assets/AssetGen.ts:3:import { generateAllItemIcons } from './ItemIconGen';
src/assets/AssetGen.ts:21:    itemIcons: generateAllItemIcons(),
src/assets/ItemIconGen.ts:284:export function generateAllItemIcons(): Map<number, HTMLCanvasElement> {

```


---

## 🤖 Assistant · 2026-08-12T15:53:29.145Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now, where do itemIcons (procedural) get used? Renderer.ts:676 `return atlasIconForKey(this.atlas, def.key)`. Let me check Renderer around 660-690 and 30-40 to understand fallback. Also check where itemIcons bundle used (probably renderer.itemIcon).

Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:29.584Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '25,45p;660,690p' src/render/Renderer.ts; echo \"=== itemIcons usage\"; grep -rn \"itemIcons\" src --include=\"*.ts\" | head",
 "description": "Read Renderer icon fallback"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:29.653Z

**📎 ToolResult**

```
}

/** 装备 → 纸娃娃渲染参数。贴图索引 = item.head/body/legs 槽位序号（原版语义，
 *  非物品 id——铁甲三件的槽位序号都是 2）；原版物品 id 经 vanilla.json armorIndex 查表 */
function dollEquipFromInv(inv: Inventory, atlas: import('../assets/SpriteAtlas').SpriteAtlas | null): { head: number | null; body: number | null; legs: number | null } {
  const idx = (itemId: number | null | undefined): number | null => {
    if (itemId == null) return null;
    const def = ITEM_DEFS[itemId];
    if (!def?.armor) return null;
    const key = def.key;
    const vid = VANILLA_ITEM_ICON_MAP[key] ?? (key.startsWith('vi_') ? parseInt(key.slice(3), 10) : NaN);
    if (!Number.isFinite(vid)) return null;
    const entry = atlas?.vanilla.armorIndex?.[String(vid)];
    if (!entry) return null;
    const slot = def.armor.slot; // 0头 1胸 2腿
    return slot === 0 ? (entry.head || null) : slot === 1 ? (entry.body || null) : (entry.legs || null);
  };
  const disp = inv.displayArmor();
  return { head: idx(disp[0]), body: idx(disp[1]), legs: idx(disp[2]) };
}
import { WeatherRenderer } from './WeatherRenderer';
    this.lightCanvas.width = 0; this.lightCanvas.height = 0;
    if (this.fogCanvas) { this.fogCanvas.width = 0; this.fogCanvas.height = 0; this.fogCanvas = null; }
    this.minimap?.dispose();
    this.minimap = null;
  }

  /** 物品图标：优先 Maples 素材，缺省回退程序化 */
  itemIcon(id: number): HTMLCanvasElement | null {
    return this.assets.itemIcons.get(id) ?? null;
  }

  /** Maples 图标绘制矩形（找不到返回 null） */
  atlasIcon(id: number) {
    if (!this.atlas) return null;
    const def = ITEM_DEFS[id];
    if (!def) return null;
    return atlasIconForKey(this.atlas, def.key);
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  attach(parent: HTMLElement) {
    parent.appendChild(this.canvas);
  }

  private _mouseX = 0;
  private _mouseY = 0;
  private _mouseDown = false;
=== itemIcons usage
src/ui/UI.ts:63:      const c = game.assets.itemIcons.get(id);
src/ui/UI.ts:66:    const c = game.assets.itemIcons.get(id);
src/render/Renderer.ts:668:    return this.assets.itemIcons.get(id) ?? null;
src/assets/AssetGen.ts:8:  itemIcons: Map<number, HTMLCanvasElement>;
src/assets/AssetGen.ts:21:    itemIcons: generateAllItemIcons(),

```


---

## 🤖 Assistant · 2026-08-12T15:53:29.904Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"def.tile\\|\\.tile\\b\" src/core/Game.ts | head -50",
 "description": "Find item.tile usage in Game"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:29.952Z

**📎 ToolResult**

```
src/core/Game.ts:1007:      if (!def.tile) continue;
src/core/Game.ts:1008:      const tid = TILE_BY_KEY[def.tile];
src/core/Game.ts:2035:        const heldTorchStyle = heldDef?.tile != null && TILE_BY_KEY[heldDef.tile] === T.TORCH
src/core/Game.ts:3084:      const isTorch = def.tile === 'torch';
src/core/Game.ts:3085:      const isCandle = def.tile === 'candle';
src/core/Game.ts:3365:    const placing = heldDef?.tile != null || heldDef?.wallId != null;
src/core/Game.ts:3713:    if (heldDef?.tile && !inp.rightDown) {
src/core/Game.ts:5312:    const tileId = TILE_BY_KEY[itemDef.tile!];

```


---

## 🤖 Assistant · 2026-08-12T15:53:32.438Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the place chain: Game.ts 3713 placeItem, 5312, 1007-1008. Also the vanilla place chain (createTile). Let me look at those areas and also vi place chain (tryPlace). Let me grep tryPlace / createTile.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:32.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '995,1015p' src/core/Game.ts; echo \"=== 3700-3830\"; sed -n '3700,3830p' src/core/Game.ts",
 "description": "Read place chain in Game"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:32.897Z

**📎 ToolResult**

```
    for (let x = x0; x <= x1; x++) {
      for (let y = yTop; y <= yBot; y++) {
        st.setTile(x, y, 0);
        st.setLiquid(x, y, 0, 0);
      }
      st.setTile(x, yBot, T.STONE);
      st.setTile(x, yBot + 1, T.STONE);
    }
    // 收集可放置 tile（有物品指向，去重）
    const placeable: number[] = [];
    const seen = new Set<number>();
    for (const def of ITEM_DEFS) {
      if (!def.tile) continue;
      const tid = TILE_BY_KEY[def.tile];
      if (tid === undefined || tid === 0 || seen.has(tid)) continue;
      seen.add(tid);
      placeable.push(tid);
    }
    // 逐行摆放：行高 7（最高家具 5 格 + 间隙），每行放满换行并铺新地板
    let cx = x0 + 1, cy = yBot - 1;
    const rowH = 7;
=== 3700-3830

    // 电路工具(扳手/剪线钳/致动器/致动魔杖/五彩扳手/宏伟蓝图):左键,目标格可被占用
    if (heldDef?.wireTool && inp.mouseDown && !inp.rightDown) {
      this.useWireTool(tx, ty, heldDef);
      return;
    }

    // 可放置物品：左键放置
    // 墙面物品（Player.PlaceThing_Walls，Player.cs:38937）：左键铺墙
    if (heldDef?.wallId != null && inp.mouseDown && !inp.rightDown) {
      this.tryPlaceWall(tx, ty, heldDef);
      return;
    }
    if (heldDef?.tile && !inp.rightDown) {
      this.tryPlace(tx, ty, heldDef);
      return;
    }

    // 其它物品（药水/食物/镜子/召唤物等）：左键使用，useStyle 分族姿势
    // （Player.ItemCheck：itemAnimationMax = useAnimation，ApplyUseStyle 按 useStyle
    //  路由——4 举过头（镜子/机械三王召唤）/5 朝鼠标静持（火把族非放置路径）/
    //  9 举杯（增益药水 DefaultToHealingPotion）/2 咀嚼（食物 DefaultToFood）/
    //  6 饮用旋转（回归药水）；此前的统一 30t 挥砍对 395 件 4/5/9 族全错族）
    // （召唤武器例外——交给下方 cw 分发 kind='summon'）
    if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool
      && cw?.kind !== 'summon') {
      this.useSwing(heldDef);
      // 召唤道具（原版左键使用）
      if (heldDef.key === 'suspicious_eye') {
        if (!this.world.clock.isDay) {
          this.useSuspiciousEye();
          this.player.inv.removeAt(this.player.inv.selected, 1);
          this.cb.onInventoryChanged();
        } else {
          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NothingHappened'));
        }
        this.player.useTime = 30;
      }
    }
    // 药水饮用（移植自 Maples：点击饮用，治疗类受耐药性封锁）
    if (heldDef?.potion && inp.mouseDown && this.player.useTime === 0) {
      const p = heldDef.potion;
      const buffTypeMap: Record<string, BuffType> = {
        agility: BuffType.Agility, ironskin: BuffType.Ironskin,
        resistance: BuffType.Resistance, thorns: BuffType.Thorns, regen: BuffType.Regen,
        obsidianSkin: BuffType.ObsidianSkin, gills: BuffType.Gills,
        manaRegen: BuffType.ManaRegen, magicPower: BuffType.MagicPower,
        featherfall: BuffType.Featherfall, waterWalking: BuffType.WaterWalking,
        archery: BuffType.Archery, nightOwl: BuffType.NightOwl,
      };
      if (p.isHealType && this.player.buffs.healBlocked) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.HealBlock'));
        this.player.useTime = 30;
      } else {
        const bt = buffTypeMap[p.buff];
        // 贤者之石（pStone：药水 CD -25%，Player.pStone → PotionSickness 2850→2140）
        this.player.buffs.apply(bt, Math.round(p.duration * (this.player.equipStats.pStone ? 0.75 : 1)));
        if (heldDef.heal) {
          this.player.hp = Math.min(this.player.maxHp, this.player.hp + heldDef.heal);
          this.addDamageNumber(this.player.cx, this.player.y, heldDef.heal, false, '#40E080');
        }
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 60;
        this.sfx.play('drink');
        this.cb.onInventoryChanged();
        this.cb.onToast(`${heldDef.name}：${p.duration} 秒`);
      }
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && (heldDef.key === 'life_crystal' || heldDef.key === 'vi_29_LifeCrystal')) {
      // 物品态生命水晶(Player.cs:29358:item 29,statLifeMax<400 → +20)
      if (this.player.baseMaxHp >= 400) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.LifeMaxReached'));
      } else {
        this.player.baseMaxHp += 20;
        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 20);
        this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#40E080');
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 30;
        this.sfx.play('drink');
        this.cb.onInventoryChanged();
      }
      this.player.useTime = Math.max(this.player.useTime, 30);
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && heldDef.key === 'vi_109_mana_crystal') {
      // 魔力水晶(Player.cs:44655:statManaMax<200 → +20 上限并回复)
      if (this.player.baseMaxMana >= 200) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.ManaMaxReached'));
      } else {
        this.player.baseMaxMana += 20;
        this.player.mana = Math.min(this.player.maxMana, this.player.mana + 20);
        this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#4080FF');
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 30;
        this.sfx.play('drink');
        this.cb.onInventoryChanged();
      }
      this.player.useTime = Math.max(this.player.useTime, 30);
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && heldDef.key === 'vi_1291_life_fruit') {
      // 生命果(Player.cs:44665:statLifeMax≥400 且 <500 → +5)
      if (this.player.baseMaxHp < 400) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NeedLifeCrystalFirst'));
      } else if (this.player.baseMaxHp >= 500) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.LifeMaxReached500'));
      } else {
        this.player.baseMaxHp += 5;
        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 5);
        this.addDamageNumber(this.player.cx, this.player.y, 5, false, '#40E080');
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 30;
        this.sfx.play('drink');
        this.cb.onInventoryChanged();
      }
      this.player.useTime = Math.max(this.player.useTime, 30);
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && heldDef.key === 'vi_5340_galaxy_pearl') {
      // 银河珍珠（Player.cs:44786-44789：一次性 usedGalaxyPearl → luck +0.03 :28676-28678；
      // 已用过 → 无动作不消耗，原版 !usedGalaxyPearl 门）
      if (!this.player.luckState.usedGalaxyPearl) {
        this.player.luckState.usedGalaxyPearl = true;
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.cb.onInventoryChanged();
      }
      this.player.useTime = 45;   // Item 5340 useTime（Item.cs:42342）
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && this.consumableFuncGate(heldDef)) {
      // vi_ 药水/食物桥接（vanilla-itemfunc：healLife/healMana/buffType → 治疗/回魔/Buff）。
      // 纯消耗品门（consumable 且无放置/射击/工具语义——宠物坐骑等 buffType 物品不在此列）
      const fm = /^vi_(\d+)_/.exec(heldDef.key);
      const ff = fm ? itemFuncOfVid(+fm[1]) : null;
      // ★ 无消耗品语义（水晶/果/弓族等）不得空占本 else-if 槽位——否则链条后续
      // 全部分支被饿死（else-if 匹配即终止）。命中才处理，否则落空交还链条
      if (ff?.consumable && !ff.createTile && !ff.shoot && !ff.pick && !ff.axe && !ff.hammer
        && (ff.healLife || ff.healMana || (ff.buffType && ff.buffType > 0))) {
        if (ff.healLife && this.player.buffs.healBlocked) {
          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.HealBlock'));

```


---

## 🤖 Assistant · 2026-08-12T15:53:36.381Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now tryPlace — the item.tile field. For vi_ items, tile is set in defs for some, but for vanilla items createTile from vanilla-itemfunc. Let me look at tryPlace.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:36.851Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tryPlace\\b\\|private tryPlace\\|tryPlace(\" src/core/Game.ts | head; echo ====; sed -n '5280,5360p' src/core/Game.ts",
 "description": "Read tryPlace implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:36.934Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
3714:      this.tryPlace(tx, ty, heldDef);
5239:  private tryPlaceWall(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
5243:    // 射程（ItemReach，与 tryPlace 一致 5.5 格）
5304:  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-12T15:53:38.511Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5304,5450p' src/core/Game.ts",
 "description": "Read tryPlace body"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:38.552Z

**📎 ToolResult**

```
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
    // 旧日军团竞技场建造封锁（Player.cs:25669-25672：DD2Event.Ongoing &&
    // ShouldBlockBuilding → 禁改方块，DD2Event.cs:794-796 包围盒判定）
    if (this.world.oldOnesArmy.ongoing
      && shouldBlockBuilding(this.world.oldOnesArmy, tx * TILE + 8, ty * TILE + 8)) {
      return;
    }
    // 传送晶塔放置门（TETeleportationPylon.PlacementPreviewHook_CheckIfCanPlace :158-166）：
    // 同型晶塔全图仅一座（HasPylonOfType TeleportPylonsSystem.cs:41-44）
    if (def?.vanilla?.sheet === 597) {
      this.refreshPylons();
      const style = itemDef.placeStyle ?? 0;
      if (hasPylonOfType(this.pylons, style)) return;
    }
    // 橡实: 只能种在草块正上方
    if (itemDef.key === 'acorn' && st.get(tx, ty + 1) !== T.GRASS) {
      this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.AcornGrassOnly'));
      return;
    }
    const ow = def.w ?? 1, oh = def.h ?? 1;
    // 绳索(RopeCoil 语义):从放置点向下延伸至实心/最多 10 格
    if (itemDef.key === 'rope') {
      const ropeTile = TILE_BY_KEY['v_213_rope']!;
      let placed = 0;
      for (let y = ty; y < ty + 10; y++) {
        if (!st.inBounds(tx, y) || st.isActive(tx, y)) break;
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
        const px = tx + dx2, py = ty + dy2;
        // 原版多格家具：帧用 18px 步长偏移（与 .wld 原生一致，渲染端直用）。
        // 原版帧语义（TileObject.Place L74-102）：frameY 从【顶行 = 0】向下递增；
        // ty 是顶部行（放置时鼠标指向顶部锚点）→ dy2=0 即顶行，frameY = dy2*18 正确
        if (isVanillaStyle) {
          // placeStyle → 样式基偏移:权威布局表(FurnitureStyle.ts;竖排族写 Y,
          // 旧公式 style*fw*18 一刀切会把灯笼/蜡烛/吊灯等写成非法帧)
          const [bx2, by2] = furnitureStyleBase(def.vanilla?.sheet ?? -1, itemDef.placeStyle ?? 0, def.vanilla?.fw ?? 1);
          st.setTile(px, py, tileId, bx2 + dx2 * 18, by2 + dy2 * 18);
        } else {
          st.setTile(px, py, tileId, dx2, dy2);
        }
        // 水被方块挤出：水量转移到相邻可容纳的格子（上/左/右），
        // 而不是被方块吞掉消失。封闭无处可去时才消失
        const pi = st.idx(px, py);
        const liq = st.liquid[pi];
        if (liq > 0) {
          const ltype = st.liquidType[pi];
          st.setLiquid(px, py, 0, 0);
          let remaining = liq;
          for (const [ox, oy] of [[0, -1], [-1, 0], [1, 0]] as const) {
            if (remaining <= 0) break;
            const nx = px + ox, ny = py + oy;
            if (!st.inBounds(nx, ny)) continue;
            const nd = TILE_DEFS[st.type[st.idx(nx, ny)]];
            if (nd && nd.solid) continue;
            const ni = st.idx(nx, ny);
            const cap = 255 - st.liquid[ni];
            if (cap <= 0) continue;
            const t = Math.min(remaining, cap);
            st.setLiquid(nx, ny, st.liquid[ni] + t, ltype || st.liquidType[ni] || 1);
            remaining -= t;
          }
        }
      }
    }
    if (tileId === T.CHEST) {
      this.world.chests.push({ x: tx, y: ty, items: Array(10).fill(null) });
    }
    // 挂物族放置登记（原版 TileLoader.PlaceTile → TE*.Hook_AfterPlacement：
    //  TEItemFrame.cs:15 / TEWeaponsRack.cs:40 / TEDisplayDoll.cs:123 / TEHatRack.cs:31 /
    //  TEFoodPlatter.cs:15 / TEDeadCellsDisplayJar.cs:15 → TileEntityType.Place）。
    //  记录在放置点(=锚点左上格)登记；空记录等价于无物，交互侧取用时也会按需补建
    if (FURNITURE_TILE_KIND.has(tileId)) {
      const fKind = FURNITURE_TILE_KIND.get(tileId)!;

```


---

## 🤖 Assistant · 2026-08-12T15:53:41.759Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
tryPlace only uses itemDef.tile — vi_ items with createTile but no tile field never enter tryPlace (they must have tile set via defs or... wait, in items.ts many vi_ items have tile set explicitly; the auto-registered vi_ items from vanilla.json loop have NO tile). So how do generic vi_ placeable items place? Perhaps via a separate vi place path. Let me search for createTile usage.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:42.154Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"createTile\" src --include=\"*.ts\" | grep -v idNames | grep -v \"\\.json\" | head -40",
 "description": "Find createTile usage"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:42.216Z

**📎 ToolResult**

```
src/ui/MultiplayerSelect.ts:50:  private createTiles: HTMLInputElement;
src/ui/MultiplayerSelect.ts:168:    this.createTiles = mkCheck('破坏保护（其他玩家不能挖掘/建造，仅房主可以）', false);
src/ui/MultiplayerSelect.ts:264:          protectTiles: this.createTiles.checked,
src/core/Game.ts:2032:        // 手持火把物品（inventory[selectedItem].createTile==4）才计 placeStyle（:17775-17778）
src/core/Game.ts:3075:    // createTile==4 火把族 → TorchColor；蜡烛(105) → [1,0.95,0.8]；均 !wet。
src/core/Game.ts:3227:      if (f?.healMana && f.consumable && !f.createTile) {
src/core/Game.ts:3267:    return !!ff?.consumable && !ff.createTile && !ff.shoot && !ff.pick && !ff.axe && !ff.hammer
src/core/Game.ts:3363:    // 放置物才有 blockRange（原版 SmartCursorLookup :95-98 createWall/createTile 才加）；
src/core/Game.ts:3827:      if (ff?.consumable && !ff.createTile && !ff.shoot && !ff.pick && !ff.axe && !ff.hammer
src/world/FurnitureItems.ts:12://        放置物品 2699（Item.cs:26028 createTile = 471）
src/world/wiring/devices.ts:146:/** 空音乐盒物品（ItemID.MusicBox = 576，Item.cs:8082-8089：accessory 无 createTile）。
src/world/wiring/devices.ts:194: *  8→4922 洞穴 / 9→4417 绿洲；Item.cs createTile=207 placeStyle 互为逆表） */
src/stats/Luck.ts:207:  /** 手持火把 placeStyle（inventory[selectedItem].createTile==4 && placeStyle<24；无 = null） */
src/stats/Shimmer.ts:87:/** 音乐盒动态分支（ShimmerTransforms.cs:95-105：createTile==139 按 placeStyle）：
src/i18n/Lang.ts:131:   * ① 放置它的物品名(TILE_NAME_ITEM_BY_SHEET:Item.createTile 反查,取基础款最小 id；
src/assets/SpriteAtlas.ts:127:  name: string; key: string; icon: string; createTile: number | null;
src/data/items.ts:793:// ---- 音乐盒唱片全量 101 曲（Item.cs DefaultToMusicBox：createTile=139、
src/data/items.ts:815:// ---- 水喷泉全量 10 色（Item.cs createTile=207：909 纯净/910 沙漠 940-945 丛林·
src/data/items.ts:833:// ---- 宝石系统：gemcorn 4851-4857（Item.cs createTile=590 宝石树苗，style=宝石序号；
src/data/vanillaItemFunc.ts:7:  createTile?: number; createWall?: number; placeStyle?: number;
src/player/SmartCursor.ts:368:  createTileSheet: number | null;
src/player/SmartCursor.ts:382:    createTileSheet: def?.tile != null ? sheetOf(TILE_BY_KEY[def.tile] ?? -1) : null,
src/player/SmartCursor.ts:902:    const createSheet = sem.createTileSheet;
src/player/SmartCursor.ts:987:    // 原版按物品 id 2340/2739 门；我方轨道放置物（place_v_314_*）无 vid → 以 createTile sheet==314 认定
src/player/SmartCursor.ts:988:    const isTrackItem = sem.createTileSheet === 314 || sem.vid === 2340 || sem.vid === 2739 || sem.vid === 2492;
src/player/SmartCursor.ts:1075:  /** :1026-1097 南瓜种子（createTile 254） */
src/player/SmartCursor.ts:1080:    if (sem.createTileSheet !== 254 || taken()) return;
src/player/SmartCursor.ts:1152:  /** :968-1024 皮纳塔（createTile 454） */
src/player/SmartCursor.ts:1157:    if (sem.createTileSheet !== 454 || taken()) return;
src/player/SmartCursor.ts:1188:    const cs = sem.createTileSheet;
src/player/SmartCursor.ts:1216:    const isTorch = (vid != null && TORCH_ITEMS.has(vid)) || sem.createTileSheet === 4 || env.held.def?.key === 'torch';
src/player/SmartCursor.ts:1274:    const cs = sem.createTileSheet;
src/player/SmartCursor.ts:1328:    const cs = sem.createTileSheet;
src/player/SmartCursor.ts:1541:  /** :482-570 炼金种子（createTile 82）：各药草适配的盆/土/沙面。
src/player/SmartCursor.ts:1548:    if (sem.createTileSheet !== 82 && sem.createTileSheet !== 83 || taken()) return;
src/player/SmartCursor.ts:1591:  /** :427-480 种植盆（createTile 380）：已有盆的左右空位 */
src/player/SmartCursor.ts:1596:    if (sem.createTileSheet !== 380 || taken()) return;
src/player/SmartCursor.ts:1620:  /** :371-425 陶盆（createTile 78）：空位 + 下方平实心顶 */
src/player/SmartCursor.ts:1625:    if (sem.createTileSheet !== 78 || taken()) return;

```


---

## 🤖 Assistant · 2026-08-12T15:53:47.772Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So placement for vi_ items relies on `def.tile` being set (manually in items.ts for specific ones), not a createTile reverse lookup in tryPlace. Let me verify: are there vi_ items where tile comes from createTile data automatically? Search for where ITEM_DEFS get tile assigned besides items.ts. grep "def.tile =" or ".tile =".
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:48.381Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"\\.tile = \\|\\.tile=\" src --include=\"*.ts\" | grep -v idNames | head -20; echo \"=== wallId assign\"; grep -rn \"wallId = \\|wallId=\" src --include=\"*.ts\" | head",
 "description": "Find runtime tile field assignment"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:48.470Z

**📎 ToolResult**

```
src/data/items.ts:809:  mbDef.tile = 'v_139_musicboxes';
src/data/items.ts:827:  fnDef.tile = 'v_207_water_fountains';
=== wallId assign
src/core/Game.ts:5248:    const wallId = itemDef.wallId!;
src/render/ChunkCache.ts:199:          const wallId = st.wall[i];
src/world/gen/vanilla/DungeonPass.ts:155:  const wallId = brick === BLUE ? 7 : brick === GREEN ? 8 : 9;
src/data/items.ts:1061:  if (existing !== undefined) { ITEM_DEFS[existing].wallId = wi.wall; continue; }

```


---

## 🤖 Assistant · 2026-08-12T15:53:49.032Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"TILE_NAME_ITEM_BY_SHEET\\|itemNameByKey\\|Lang.itemNameByKey\" src/i18n/Lang.ts | head; sed -n '120,175p' src/i18n/Lang.ts",
 "description": "Read Lang item name resolution"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:49.090Z

**📎 ToolResult**

```
src/i18n/Lang.ts:8:import { ITEM_KEY_TO_ID, ITEM_NAME_BY_ID, NPC_NAME_BY_ID, BUFF_NAME_BY_ID, PROJECTILE_NAME_BY_ID, TILE_NAME_BY_ID, TILE_NAME_ITEM_BY_SHEET, TILE_NAME_ZH_BY_ID, TILE_NAME_EN_BY_ID, ITEM_NAME_ZH_BY_ID, ITEM_NAME_EN_BY_ID, WALL_NAME_ITEM_BY_WALL, WALL_NAME_ZH_BY_ID, WALL_NAME_EN_BY_ID } from './idNames.generated';
src/i18n/Lang.ts:76:  itemNameByKey(key: string): string {
src/i18n/Lang.ts:131:   * ① 放置它的物品名(TILE_NAME_ITEM_BY_SHEET:Item.createTile 反查,取基础款最小 id；
src/i18n/Lang.ts:140:    const placer = TILE_NAME_ITEM_BY_SHEET[id];
    return internal && Lang.has(`BuffDescription.${internal}`) ? Lang.text(`BuffDescription.${internal}`) : null;
  },

  /** 投射物名(Lang.cs:444 GetProjectileName;ProjectileName 在 Projectiles 分片) */
  projectileName(id: number): string | null {
    const internal = PROJECTILE_NAME_BY_ID[id];
    return internal && Lang.has(`ProjectileName.${internal}`) ? Lang.text(`ProjectileName.${internal}`) : null;
  },

  /**
   * 图块名。解析链(1.4.4+ 原版语义:方块无独立显示名——Tiles 分节为空)：
   * ① 放置它的物品名(TILE_NAME_ITEM_BY_SHEET:Item.createTile 反查,取基础款最小 id；
   *    如 tile14 表 → 木桌 WoodenTable)——12 语言官方译名权威来源
   * ② MapObject 族名(Lang.cs:77 GetMapObjectName 系,仅 79 键,族级泛称如"桌子")
   * ③ id-maps 方块名(TILE_NAME_ZH/EN_BY_ID：世界生成专属块——树/藤蔓/药草等
   *    无放置物品且 MapObject 缺失；原版对它们无 UI 显示名,此为唯一译名来源。
   *    zh 系语言取 zh,其余语言取 en)
   * ④ null(调用方回退 TILE_DEFS[].name)
   */
  tileName(id: number): string | null {
    const placer = TILE_NAME_ITEM_BY_SHEET[id];
    if (placer !== undefined) {
      const n = Lang.itemName(Number(placer));
      if (n) return n;
    }
    const internal = TILE_NAME_BY_ID[id];
    if (internal && Lang.has(`MapObject.${internal}`)) return Lang.text(`MapObject.${internal}`);
    const isZh = (languageManager.activeCulture?.name ?? '').startsWith('zh');
    const fallback = isZh ? TILE_NAME_ZH_BY_ID[id] : TILE_NAME_EN_BY_ID[id];
    return fallback ?? null;
  },

  /**
   * 墙名。与 tileName 同构（原版墙无独立显示名）：
   * ① 放置它的物品名（WALL_NAME_ITEM_BY_WALL：Item.createWall 反查，取最小 id）
   * ② id-maps walls 的 zh/en（自然墙无放置物品——泥土墙/石墙等）
   * ③ null（调用方回退 WALL_DEFS[].name）
   */
  wallName(id: number): string | null {
    const placer = WALL_NAME_ITEM_BY_WALL[id];
    if (placer !== undefined) {
      const n = Lang.itemName(Number(placer));
      if (n) return n;
    }
    const isZh = (languageManager.activeCulture?.name ?? '').startsWith('zh');
    return (isZh ? WALL_NAME_ZH_BY_ID[id] : WALL_NAME_EN_BY_ID[id]) ?? null;
  },

  /** 类别内取模循环取值(原版 IndexedFromCategory) */
  indexedFromCategory(category: string, index: number): string | null {
    return languageManager.indexedFromCategory(category, index);
  },

  /** 类别内随机(原版 RandomFromCategory,如小贴士 LoadingTips_Default) */
  randomFromCategory(category: string, rng?: () => number): string | null {
    return languageManager.randomFromCategory(category, rng);

```


---

## 🤖 Assistant · 2026-08-12T15:53:51.655Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now Lang.itemNameByKey: uses ITEM_KEY_TO_ID (in idNames.generated) → key → vanilla id → ITEM_NAME_BY_ID. So local keys are mapped to vanilla ids in the generated table (which I saw: "wood":9, etc.). This is important for migration — the generated i18n table contains ALL local keys.

Let me check Lang.itemNameByKey and Lang.itemName.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:53:52.112Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '60,110p' src/i18n/Lang.ts; echo \"=== ITEM_NAME_BY_ID usage\"; grep -rn \"ITEM_NAME_BY_ID\\|ITEM_KEY_TO_ID\" src --include=\"*.ts\" | grep -v idNames.generated | head",
 "description": "Read Lang.itemNameByKey"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:52.176Z

**📎 ToolResult**

```
  },

  // ---- 名字类便捷方法(Lang.cs FillNameCacheArray:键 = category + ID 常量名)----

  /** 物品名(原版 id)。缺失回退 null */
  itemName(id: number): string | null {
    const internal = ITEM_NAME_BY_ID[id];
    return internal && Lang.has(`ItemName.${internal}`) ? Lang.text(`ItemName.${internal}`) : null;
  },

  /** 物品名(本仓库 item key)。解析链：
   *  ① vi_<id>_ 前缀/ITEM_KEY_TO_ID → 原版 ItemName（12 语言官方译文）
   *  ①.5 place_v_* → 其放置的 tile sheet → Lang.tileName（放置物品无独立名，
   *      原版语义=方块名，如 place_v_144_timers → 1秒计时器）
   *  ② Mods.SandboxWorld.ItemName.<PascalKey>（l10n-custom 自有物品——原版不存在的发明物）
   *  ③ ItemDef.name 硬编码兜底 */
  itemNameByKey(key: string): string {
    const vi = key.match(/^vi_(\d+)_/);
    const id = vi ? Number(vi[1]) : ITEM_KEY_TO_ID[key];
    if (id != null) {
      const n = Lang.itemName(id);
      if (n) return n;
      // id-maps 兜底（l10n 缺译的少数 id；zh 系取 zh 其余取 en）
      const isZh = (languageManager.activeCulture?.name ?? '').startsWith('zh');
      const fb = isZh ? ITEM_NAME_ZH_BY_ID[id] : ITEM_NAME_EN_BY_ID[id];
      if (fb) return fb;
    }
    if (key.startsWith('place_v_')) {
      const tileKey = ITEM_DEFS[ITEM_BY_KEY[key]]?.tile;
      const sheet = tileKey !== undefined ? TILE_DEFS[TILE_BY_KEY[tileKey]]?.vanilla?.sheet : undefined;
      if (sheet !== undefined) {
        const n = Lang.tileName(sheet);
        if (n) return n;
      }
    }
    const custom = `Mods.SandboxWorld.ItemName.${key.replace(/(^|_)([a-z0-9])/g, (_, p, c) => (p ? c.toUpperCase() : c.toUpperCase()))}`;
    if (Lang.has(custom)) return Lang.text(custom);
    return ITEM_DEFS[ITEM_BY_KEY[key]]?.name || key;
  },

  /**
   * NPC 名(原版 netID,Lang.cs:175 GetNPCName)。
   * 正 id → NPCName.<Internal>;负 id(变种史莱姆)暂按 -netId 正查近似——
   * 原版 65 条 _negativeNpcNameCache 硬表(Lang.cs:520-535)待 NPC 变种移植时补全。
   */
  npcName(netId: number): string | null {
    const id = netId > 0 ? netId : -netId;
    const internal = NPC_NAME_BY_ID[id];
    return internal && Lang.has(`NPCName.${internal}`) ? Lang.text(`NPCName.${internal}`) : null;
  },

=== ITEM_NAME_BY_ID usage
src/i18n/Lang.ts:66:    const internal = ITEM_NAME_BY_ID[id];
src/i18n/Lang.ts:71:   *  ① vi_<id>_ 前缀/ITEM_KEY_TO_ID → 原版 ItemName（12 语言官方译文）
src/i18n/Lang.ts:78:    const id = vi ? Number(vi[1]) : ITEM_KEY_TO_ID[key];

```


---

## 🤖 Assistant · 2026-08-12T15:53:57.548Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"magic\\b\\|\\.ranged\\b\\|def.magic\\|def.ranged\" src/core/Game.ts src/entities/Player.ts src/player/SmartCursor.ts 2>/dev/null | grep -v \"//\" | head -40",
 "description": "Find magic/ranged def usage"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:57.661Z

**📎 ToolResult**

```
src/entities/Player.ts:502:   *  不再复用 magic——MagicPower 等 magic-only 来源不吃召唤；四系通用来源照常） */
src/entities/Player.ts:535:   *  minionDamage 链：装备走 SUMMON_GEAR/SET，不含 magic-only 来源） */
src/entities/Player.ts:536:  damageMult(kind: 'melee' | 'ranged' | 'magic' | 'summon'): number {
src/entities/Player.ts:549:    if (kind === 'magic') {
src/entities/Player.ts:617:  critChance(kind: 'melee' | 'ranged' | 'magic'): number {
src/core/Game.ts:3856:      && (heldDef.ranged || rangedAmmoWeapon(heldDef))) {
src/core/Game.ts:3864:      const rg = heldDef.ranged ?? null;
src/core/Game.ts:4034:    } else if (heldDef?.magic && inp.mouseDown && this.player.useTime === 0) {
src/core/Game.ts:4036:      const mg = heldDef.magic;
src/core/Game.ts:4187:    const dmgKind = cwIn.kind === 'magic' ? 'magic' : (cwIn.kind === 'boomerang' || cwIn.kind === 'spear' || cwIn.kind === 'yoyo' || cwIn.kind === 'flail') ? 'melee' as const : 'ranged' as const;
src/core/Game.ts:4196:    if (cw.kind === 'grenade' || cw.kind === 'magic' || cw.kind === 'shot' || cw.kind === 'summon') {
src/core/Game.ts:4342:      case 'magic': {
src/core/Game.ts:7124:    const noMelee = heldDef.magic || swingCombat?.noMelee;
src/core/Game.ts:9780:        Math.round(30 * p.damageMult('magic')), 3, 92, null,

```


---

## 🤖 Assistant · 2026-08-12T15:53:59.306Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3850,4060p' src/core/Game.ts",
 "description": "Read ranged/magic use chains"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:53:59.350Z

**📎 ToolResult**

```
          this.player.useTime = 60;
          this.sfx.play('drink');
          this.cb.onInventoryChanged();
        }
      }
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0
      && (heldDef.ranged || rangedAmmoWeapon(heldDef))) {
      // 远程武器（弓/枪/吹箭筒）：PickAmmo + ItemCheck_Shoot 1:1（Player.cs:52590+/46426）
      //   速度 = 弓 shootSpeed + 弹药 shootSpeed；伤害 = 弓 damage + 弹药 damage；
      //   击退 = 弓 kb + 弹药 kb；投射物类型 = 弹药 shoot；音效 = 弓 UseSound(Item5)
      //   弹药查找：原版先扫 54-57 弹药栏（Inventory.add 已把弹药归入 54-57），再扫背包 0-53 第一组
      //   ★ vi_ 枪族（164 手枪/964 火铳/1319 雪球炮/281 吹箭筒等 useAmmo 武器）此前
      //   combatWeapon 按 useAmmo 排除后无人接管 = 静默失效；此处经
      //   vanilla-itemcombat.useAmmo 数据驱动接入（930 信号枪 useAmmo=-1 原版语义不接）
      const rg = heldDef.ranged ?? null;
      const bowVid = rg?.vid ?? viIdFromKey(heldDef.key);
      const bowC = bowVid >= 0 ? itemCombat(bowVid) : null;
      const useAmmo = bowC?.useAmmo ?? AMMO_ARROW;
      // PickAmmo：弹药栏 54-57 优先，再背包 0-53 第一组 useAmmo 匹配
      // （def.ammoId = legacy 注册；vi_ 弹药经 combat.ammo 反查）
      const ammoOf = (d: (typeof ITEM_DEFS)[number]): number =>
        d.ammoId ?? (d.vid != null || viIdFromKey(d.key) >= 0 ? itemCombat(d.vid ?? viIdFromKey(d.key))?.ammo ?? 0 : 0);
      let ammoSlot = -1;
      let ammoDef: (typeof ITEM_DEFS)[number] | null = null;
      for (const [from, to] of [[54, 58], [0, 54]] as const) {
        for (let i = from; i < to; i++) {
          const sl = this.player.inv.slots[i];
          if (!sl || sl.stack <= 0) continue;
          const d = ITEM_DEFS[sl.id];
          if (d && ammoOf(d) === useAmmo) { ammoSlot = i; ammoDef = d; break; }
        }
        if (ammoSlot >= 0) break;
      }
      if (ammoSlot >= 0 && ammoDef) {
        const ammoC = ammoDef.vid != null || viIdFromKey(ammoDef.key) >= 0
          ? itemCombat(ammoDef.vid ?? viIdFromKey(ammoDef.key)) : null;
        // 箭速：射手 buff ×1.2（cap 20，:52717）+ 箭袋族 ×1.1（:52711）——仅箭族吃
        const isArrowKind = bowC?.useAmmo !== 97 && bowC?.useAmmo !== 771 && bowC?.useAmmo !== 283;
        let speed = (bowC?.shootSpeed ?? rg?.projSpeed ?? 7) + (ammoC?.shootSpeed ?? 0);
        if (isArrowKind) speed = Math.min(20, speed * this.player.buffs.arrowSpeedMult
          * (this.player.equipStats.quiver ? 1.1 : 1));
        // 词缀乘区只作用于武器基伤（GetWeaponDamage：item.damage 含词缀，弹药另加）；
        // 装备远程伤害乘区（侦察镜/复仇者徽章等）
        const ps = this.heldPrefixStat();
        // 弹药分道（Player.cs:3820 bowEffectiveDamage 拆分）：箭吃箭袋/射手/蘑菇矿箭头，
      // 弹/火箭吃对应蘑菇矿头；Archery 不再误伤枪械
      const rKind = bowC?.useAmmo === 97 ? 'bullet' : bowC?.useAmmo === 771 ? 'rocket' : bowC?.useAmmo === 283 ? 'other' : 'arrow';
      let damage = Math.round((bowC?.damage ?? rg?.damage ?? 1) * (ps?.dmg ?? 1) * this.player.rangedDamageMult(rKind)) + (ammoC?.damage ?? 0) + this.player.equipStats.armorPen;
        let knockback = (bowC?.knockBack ?? rg?.knockback ?? 2) * (ps?.kb ?? 1) + (ammoC?.knockBack ?? 0);
        if (isArrowKind && this.player.equipStats.quiver) knockback *= 1.1; // 箭袋击退 ×1.1（:52713）
        const projId = ammoC?.shoot ?? bowC?.shoot ?? 1; // PickAmmo：projToShoot = 弹药 shoot
        if (isArrowKind && this.player.equipStats.moltenQuiver && projId === 1) damage += 2; // 熔箭袋木箭→火矢+2（:52700，火矢 proj 换体从略）
        const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
        const ax = this.player.cx + Math.cos(ang) * 14;
        const ay = this.player.cy - 4 + Math.sin(ang) * 14;
        // 回收掉落：仅木箭（原版燃烧箭 Kill 不掉；子弹/飞镖不可回收）
        const dropKey = projId === 1 ? ammoDef.key : null;
        this.entities.add(new Arrow(ax, ay, Math.cos(ang) * speed, Math.sin(ang) * speed,
          damage, knockback, projId, dropKey), 'projectiles');
        // 弹药节约（ammoCost80：20% 概率不耗弹——蘑菇矿胸甲族，Player.PickAmmo 语义）
        if (!(((this.player.equipStats.ammoSave || this.player.buffs.has(BuffType.AmmoReservation)) && Math.random() < 0.2))) {
          this.player.inv.removeAt(ammoSlot, 1);
        }
        this.player.useTime = bowC?.useTime ?? rg?.speed ?? 30;
        // useStyle 5（弓枪族恒 5）：朝鼠标静持姿势 + 身体行档（Player.cs:46708 itemRotation=瞄准角）
        this.useSwing(heldDef, ang);
        // 发射音（原版 Item.cs UseSound）：弓（useAmmo 40）=Item_5；枪械通用=Item_11；
        // 霰弹枪族 534/964/3788/4703=Item_36；手枪族 164/219/1255/1929/2269/2270=Item_41
        // （Item_36/41 此前登记"素材未提取"，现已落位 public/sounds/——销核）
        this.sfx.play(useAmmo === AMMO_ARROW ? 'bowShoot'
          : GUN_SHOTGUN_VIDS.has(bowVid) ? 'gunShotgun'
          : GUN_HANDGUN_VIDS.has(bowVid) ? 'gunHandgun' : 'gunShot');
        this.cb.onInventoryChanged();
      }
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && cw && cw.kind !== 'melee') {
      // vi_* 数据驱动武器（1456 aiStyle 家族）：回旋镖/长矛/悠悠球/连枷/手雷/魔法/直射兜底。
      // 必须排在 thrownCombat 之前——手雷(166 等)满足投掷判定但语义是 ai16 弹跳引信
      this.useCombatWeapon(cw, heldDef);
    } else if (heldDef && inp.mouseDown && this.player.useTime === 0 && thrownCombat(heldDef)) {
      // 消耗型投掷武器（手里剑/飞刀/毒刀等，Item.shoot + consumable + noMelee 且无 useAmmo）：
      // 朝鼠标投出 item.shoot 投射物，消耗 1 个，数值全取 vanilla-itemcombat.json；
      // 投射物复用 Arrow（重力 0.3/tick = 原版 aiStyle 2 抛物线同值；命中可回收）
      const tc = thrownCombat(heldDef)!;
      const vid = heldDef.vid ?? viIdFromKey(heldDef.key);
      const c = itemCombat(vid);
      const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
      const px = this.player.cx + Math.cos(ang) * 14;
      const py = this.player.cy - 4 + Math.sin(ang) * 14;
      // 粉末族（净化粉 66 / 邪恶粉 67 / 猩红粉 2886）：proj 10/11/463 是 aiStyle 6
      // 粉末云（64×64 无碰撞盒、180 tick、无重力），不是 aiStyle 2 抛物投掷物——
      // 必须先于下方 Arrow 分流，否则退化成"可回收的投掷刀"（GAP 补齐）。
      // 云体以玩家为中心生成（原版 ItemCheck_Shoot 弹心 = 人物中心）
      const powderProj = POWDER_PROJ_BY_ITEM[vid];
      if (powderProj) {
        this.entities.add(new PowderProj(this.player.cx - 32, this.player.cy - 32,
          Math.cos(ang) * (c?.shootSpeed ?? 4), Math.sin(ang) * (c?.shootSpeed ?? 4), powderProj), 'projectiles');
      } else {
        // 穿透取原版 penetrate（手里剑 4；-1 无限上限 6）。
        // ★伤害对账：1.4.4+ 投掷系并入 melee（Item 277 手里剑 SetDefaults melee=true）——
        // 乘区=近战链×词缀+armorPen（此前裸 tc.damage 完全无乘区）
        const psT = this.heldPrefixStat();
        const dmgT = Math.max(1, Math.round(tc.damage * (psT?.dmg ?? 1) * this.player.damageMult('melee'))
          + this.player.equipStats.armorPen + this.player.meleeArmorPen); // 磨刀穿甲含投掷
        let pen = projectileData(tc.shoot)?.penetrate ?? 1;
        if (pen < 0) pen = 6;
        pen = Math.max(1, Math.min(pen, 6));
        this.entities.add(new Arrow(px, py,
          Math.cos(ang) * (c?.shootSpeed ?? 9), Math.sin(ang) * (c?.shootSpeed ?? 9),
          dmgT, (c?.knockBack ?? 0) * (psT?.kb ?? 1), tc.shoot, heldDef.key, { pierce: pen }), 'projectiles');
      }
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = c?.useTime ?? 15;
      this.sfx.play('throw');
      this.cb.onInventoryChanged();
    } else if (heldDef && (heldDef.key === 'worm_food' || heldDef.key === 'bloody_spine' || heldDef.key === 'slime_crown')
      && inp.mouseDown && this.player.useTime === 0) {
      // Boss 召唤物(原版 worm food/bloody spine/slime crown)
      if (heldDef.key === 'worm_food') this.summonBoss('eater_of_worlds_head');
      else if (heldDef.key === 'bloody_spine') this.summonBoss('brain_of_cthulhu');
      else this.summonBoss('king_slime');
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = 60;
      this.cb.onInventoryChanged();
      this.input.mouseDown = false;
    } else if (heldDef && (heldDef.key === 'mechanical_worm' || heldDef.key === 'mechanical_eye' || heldDef.key === 'mechanical_skull')
      && inp.mouseDown && this.player.useTime === 0) {
      // 机械三王召唤物(原版 556/544/557:需困难模式+夜晚)
      if (!this.world.flags.hardMode) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.MechNotAwake'));
      } else if (this.world.clock.isDay) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NightOnly'));
      } else {
        if (heldDef.key === 'mechanical_worm') this.summonBoss('destroyer');
        else if (heldDef.key === 'mechanical_eye') this.summonBoss('twins');
        else this.summonBoss('skeletron_prime');
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 60;
        this.cb.onInventoryChanged();
      }
      this.input.mouseDown = false;
    } else if (heldDef && heldDef.key === 'vi_2767_solar_tablet'
      && inp.mouseDown && this.player.useTime === 0) {
      // 日耀碑牌（Player.cs:43308/51431：dayTime && !eclipse && hardMode 才可用，
      // 成功 → Main.eclipse=true + Lang.misc[20] 公告；非白天/已日食/肉前静默不可用）
      if (this.world.flags.hardMode && this.world.clock.isDay && !this.world.clock.eclipse) {
        this.world.clock.eclipse = true;
        this.newText(Lang.misc(20), 50, 255, 130);   // ChatColors.World
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 60;
        this.cb.onInventoryChanged();
      } else if (!this.world.clock.isDay) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NightOnly'));
      }
      this.input.mouseDown = false;
    } else if (heldDef && (heldDef.key === 'goblin_battle_standard' || heldDef.key === 'snow_globe' || heldDef.key === 'pirate_map')
      && inp.mouseDown && this.player.useTime === 0) {
      // 入侵触发物品（Player.ItemCheck_UseEventItems，Player.cs:43243/43260/43277：
      // 战旗 ignoreDelay，成功才消耗）
      const type = heldDef.key === 'goblin_battle_standard' ? INVASION_GOBLIN
        : heldDef.key === 'snow_globe' ? INVASION_SNOW_LEGION : INVASION_PIRATE;
      if (this.startInvasionAndAnnounce(type, true)) {
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 60;
        this.cb.onInventoryChanged();
      }
      this.input.mouseDown = false;
    } else if (heldDef && (heldDef.key === 'vi_1844_PumpkinMoonMedallion' || heldDef.key === 'vi_1958_NaughtyPresent')
      && inp.mouseDown && this.player.useTime === 0) {
      // 南瓜月/霜月召唤物（1844 PumpkinMoonMedallion / 1958 NaughtyPresent，
      //  Player.cs:43294/43361 ItemCheck + Main.startPumpkinMoon/startSnowMoon :10903-10940）：
      //  门 = !dayTime && !pumpkinMoon && !snowMoon；成功 → 置位 + 清血月 + 广播 wave 1 文案。
      //  useTime 45（Item.cs:20377-20385 / 21121-21128）。军队入侵进行中不开
      //  （invaders 与月事件刷怪段互斥，避免两事件打架——原版 DD2 同门）
      const kind = heldDef.key === 'vi_1844_PumpkinMoonMedallion' ? MOON_KIND_PUMPKIN : MOON_KIND_FROST;
      if (this.world.clock.isDay) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NightOnly'));
      } else if (this.world.moonEvent.kind === 0 && this.world.invasionType === 0) {
        const ann = startMoonEvent(this.world, kind);
        if (ann) this.newText(invasionWaveText(ann), 175, 75, 255);
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 45;
        this.cb.onInventoryChanged();
      }
      this.input.mouseDown = false;
    } else if (heldDef?.magic && inp.mouseDown && this.player.useTime === 0) {
      // 魔法武器:消耗 mana → 发射魔法弹(Player.ItemCheck_Shoot 语义)
      const mg = heldDef.magic;
      // 魔力花族：耗魔 -8%（manaCost -= 0.08，Player.cs:14040）；不足时自动喝蓝
      // 魔力花族 -8% + 丛林套 manaCostMul（:14040 / :15878）
      const mgCost = Math.max(1, Math.round(mg.manaCost * (this.player.equipStats.manaFlower ? 0.92 : 1) * this.player.equipStats.manaCostMul));
      if (this.player.mana < mgCost) {
        if (!(this.player.equipStats.manaFlower && this.tryAutoManaPotion() && this.player.mana >= mgCost)) {
          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NoMana'));
          this.input.mouseDown = false;
        }
      }
      if (this.player.mana >= mgCost) {
        this.player.mana -= mgCost;
        // （星云叠层已改为 booster 掉落拾取链 nebulaCb/nebulaLevelup——耗魔直叠旧路径移除）
        const ang = Math.atan2(inp.mouseY - vh2 / 2, inp.mouseX - vw2 / 2);
        const mx = this.player.cx + Math.cos(ang) * 14;
        const my = this.player.cy - 4 + Math.sin(ang) * 14;
        const color = mg.proj === 'bolt' ? '#A040FF' : '#FFB040';
        const proj = new MagicProj(mx, my, Math.cos(ang) * mg.projSpeed, Math.sin(ang) * mg.projSpeed, mg.damage, 45, color);
        this.entities.add(proj, 'projectiles');
        this.player.useTime = mg.speed;
        this.player.onManaItemUsed(); // 用魔动画窗（manaRegenDelay 重置期，:42131-42137）
        // 法杖 useStyle 5：朝鼠标静持姿势（Player.cs:46708 itemRotation=瞄准角）
        this.useSwing(heldDef, ang);
        this.sfx.play('tink');
        this.input.mouseDown = false;

```


---

## 🤖 Assistant · 2026-08-12T15:54:01.613Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now the net/protocol. Let me grep item id sync in protocol.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:01.941Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"item\\|Item\" src/net/protocol.ts | head -60",
 "description": "Find item sync in protocol"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:01.995Z

**📎 ToolResult**

```
26:  SyncPlayerItem = 5, // C→S→广播（v2 对齐原版 msg5 SyncPlayerItem 语义，批量变体）：
28:                      //    u8 itemSlot, u16 itemId(0=空), u16 stack}]}
37:                      //   u8 selectedItem, f32 x, f32 y, [f32 vx, f32 vy 若 flagBits[2]]}
38:                      //   ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction
45:  SyncItem = 21,       // 房主→广播 {u32 netId, u8 op(0=spawn/1=take/2=despawn), str key,
46:                       //   u16 stack, f32 x,y,vx,vy}（原版同号 SyncItem）
63:  SyncChestItem = 32,  // S→C 下发 / C→S 槽位编辑（原版同号 SyncChestItem）：
64:                       //   {u16 chestIdx, i32 x, i32 y, u16 count, [u8 slot, u16 itemId, u16 stack]}
71:  RoomPolicy = 200,   // S→C {roomCode, roomName, isHost, protectTiles, protectItems, u16 maxPlayers(v4)}
219:// ================= 玩家物品同步（msg5 SyncPlayerItem 批量变体） =================
221:export const enum ItemContainer {
227:export interface ItemSyncEntry {
228:  container: ItemContainer;
229:  itemSlot: number;
230:  itemId: number;   // 0 = 空
236:export function writePlayerItems(entries: Array<ItemSyncEntry & { playerSlot: number }>): Uint8Array {
237:  const w = new NetWriter(Msg.SyncPlayerItem);
242:    w.u8(e.itemSlot);
243:    w.u16(e.itemId & 0xffff);
249:export function readPlayerItems(r: NetReader): Array<ItemSyncEntry & { playerSlot: number }> {
251:  const out: Array<ItemSyncEntry & { playerSlot: number }> = [];
254:    const container = r.u8() as ItemContainer;
255:    const itemSlot = r.u8();
256:    const itemId = r.u16();
258:    out.push({ playerSlot, container, itemSlot, itemId, stack });

```


---

## 🤖 Assistant · 2026-08-12T15:54:05.563Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40,50p' src/net/protocol.ts; echo \"=== SyncItem usage\"; grep -rn \"SyncItem\\|writeSyncItem\\|readSyncItem\\|netId\" src/net/protocol.ts | head -20; echo \"=== ClientNet item key/vid\"; grep -n \"VANILLA_ITEM_KEY_BY_ID\\|viIdFromKey\\|key\\b\" src/net/ClientNet.ts | head -30",
 "description": "Read SyncItem and ClientNet item sync"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:05.674Z

**📎 ToolResult**

```
  PlayerActive = 14,  // S→C 广播 {slot, active, name}
  TileBatch = 17,     // C→S→广播 {count, ops[]}（tile 操作批量，对齐 msg17 语义）
  SetTime = 18,       // S→C {timeOfDay, dayCount}
  // ---- v3 实体同步（房主权威 + 服务器中继；ID 对齐原版 MessageID.cs） ----
  PlayerLifeMana = 16, // 双向 {u8 slot, i16 hp, i16 maxHp}（原版同号：客户端权威 HP，服务器中继）
  SyncItem = 21,       // 房主→广播 {u32 netId, u8 op(0=spawn/1=take/2=despawn), str key,
                       //   u16 stack, f32 x,y,vx,vy}（原版同号 SyncItem）
  SyncNPC = 23,        // C→S（房主上行）：{u16 count, [u32 netId, str key, f32 x,y,vx,vy,
                       //    i16 hp, i16 maxHp, u16 animT, u8 flags(bit0=boss)]}
                       // S→C（v4 短码+AOI 逐端过滤）：{u16 count, [u8 eflags, ...,
                       //    eflags.bit0=含 key 全量(u32 netId + u16 codeId + str key)
=== SyncItem usage
src/net/protocol.ts:45:  SyncItem = 21,       // 房主→广播 {u32 netId, u8 op(0=spawn/1=take/2=despawn), str key,
src/net/protocol.ts:46:                       //   u16 stack, f32 x,y,vx,vy}（原版同号 SyncItem）
src/net/protocol.ts:47:  SyncNPC = 23,        // C→S（房主上行）：{u16 count, [u32 netId, str key, f32 x,y,vx,vy,
src/net/protocol.ts:50:                       //    eflags.bit0=含 key 全量(u32 netId + u16 codeId + str key)
src/net/protocol.ts:51:                       //             bit1=boss；否则仅 u16 codeId（客户端 codeId→netId/key 表）]}
src/net/protocol.ts:53:                       //   {u16 count, [u32 netId, u8 kind, str tag, i16 dmg, i16 aux, f32 x,y,vx,vy]}
src/net/protocol.ts:59:  ProjDespawn = 28,  // C→S→广播（v6）：{u16 count, [u32 netId]}——弹幕消亡上报，
src/net/protocol.ts:65:  StrikeNPC = 42,      // 访客→房主（服务器定向转发）{u32 netId, i16 dmg, f32 kbx, f32 kby}
=== ClientNet item key/vid
44:  netId: number; key: string;
60:  key: string; stack: number;
115:  /** msg23 短码表（v4：codeId → {netId, key}；服务器端分配，全量条目重建） */
116:  private npcCodes = new Map<number, { netId: number; key: string }>();
418:        // v4 短码格式：每条 1B eflags——bit0=含 key 全量(u32 netId+u16 codeId+str key)，
419:        // bit1=boss；否则仅 u16 codeId（查本端 codeId→netId/key 表）。
426:          let netId = 0, key = '';
430:            key = r.str();
431:            this.npcCodes.set(code, { netId, key });
436:            key = e?.key ?? '';
441:          snaps.push({ netId, key, x, y, vx, vy, hp, maxHp, animT, flags: eflags & 2 ? 1 : 0 });
449:        let key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0;
451:          key = r.str(); stack = r.u16();
454:        this.hooks.onItemOp?.({ op, netId, key, stack, x, y, vx, vy });
691:      w.u32(s.netId); w.str(s.key);
703:  sendItemOp(op: 0 | 1 | 2, netId: number, key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0) {
707:      w.str(key); w.u16(stack);

```


---

## 🤖 Assistant · 2026-08-12T15:54:08.364Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
SyncItem (msg21) uses string KEY (not internal id) — good. msg5 SyncPlayerItem uses u16 itemId internal id. SyncChestItem uses u16 itemId internal id.

Let me check where writePlayerItems is called and where itemId comes from (internal id). Grep in src for writePlayerItems / ItemContainer usage.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:08.907Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"writePlayerItems\\|readPlayerItems\\|ItemContainer\\|SyncChestItem\\|chestItem\" src --include=\"*.ts\" | grep -v protocol.ts | head -20; echo \"=== entitySyncHooks\"; cat src/net/entitySyncHooks.ts",
 "description": "Find item id sync consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:08.981Z

**📎 ToolResult**

```
src/net/ClientNet.ts:8:  ItemContainer, ItemSyncEntry, INV_SYNC_SIZES, writePlayerItems, readPlayerItems,
src/net/ClientNet.ts:324:        const entries = readPlayerItems(r);
src/net/ClientNet.ts:413:      case Msg.SyncChestItem: {
src/net/ClientNet.ts:629:    const w = new NetWriter(Msg.SyncChestItem);
src/net/ClientNet.ts:792:        entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: arr[i]?.id ?? 0, stack: arr[i]?.stack ?? 0 });
src/net/ClientNet.ts:795:    this.send(writePlayerItems(entries));
src/net/ClientNet.ts:815:          entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: a?.id ?? 0, stack: a?.stack ?? 0 });
src/net/ClientNet.ts:820:    if (entries.length) this.send(writePlayerItems(entries));
=== entitySyncHooks
// 实体同步注入点（沿用 TileStore.netReporter 注入模式——entities 层不反向依赖 net 层）。
// Game 在联机模式下注入；单机恒 null（零开销）。
export const entityNet = {
  /** 傀儡受击上报（访客→房主 StrikeNPC：原始伤害+击退，房主权威结算）。
   *  掉落物 spawn/take 不走此钩子（Game.netDropSweep/netSweepPuppets 直调
   *  net.sendItemOp——曾预留的 reportSpawn/reportTake 终审清扫已删） */
  reportStrike: null as null | ((netId: number, rawDmg: number, kbx: number, kby: number) => void),
};

/** 实体 netId 合成：高 8 位 = 拥有者 slot（防跨客户端本地 id 撞号），低 24 位 = 本地实体 id */
export function makeNetId(ownerSlot: number, localId: number): number {
  return ((ownerSlot & 0xff) << 24) | (localId & 0xffffff);
}

export function netIdLocal(netId: number): number {
  return netId & 0xffffff;
}

```


---

## 🤖 Assistant · 2026-08-12T15:54:12.614Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: msg5 itemId = internal id (arr[i]?.id). SyncChestItem similarly internal ids.

Now: mining/tool chain with tool.power and useTime; check vanillaItemCombat itemCombat/combatWeapon. Also check where def.tool used for damage in melee swings (Game.ts 10443-10448 applyItemTime). Let me read vanillaItemCombat.ts briefly and the melee swing damage code.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:12.894Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,90p' src/data/vanillaItemCombat.ts",
 "description": "Read vanillaItemCombat head"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:12.943Z

**📎 ToolResult**

```
// 原版物品战斗数据（tools/extract-itemcombat.mjs 从 Terarria1456 Item.cs SetDefaults 提取）：
// damage/knockBack/useTime/useAnimation/shoot/useAmmo/shootSpeed/ammo/consumable/noMelee/autoReuse/mana
import combatJson from './vanilla-itemcombat.json';
import { projectileData, AI_ANCHORED, AI_BOOMERANG, AI_FLAIL, AI_GLOWSTICK, AI_GRENADE, AI_SPEAR, AI_SHORTSWORD, AI_THROWN, AI_YOYO } from './vanillaProjectiles';

export interface ItemCombat {
  damage?: number;
  knockBack?: number;
  useTime?: number;
  useAnimation?: number;
  shoot?: number;
  useAmmo?: number;
  shootSpeed?: number;
  ammo?: number;
  consumable?: boolean;
  noMelee?: boolean;
  autoReuse?: boolean;
  mana?: number;
  melee?: boolean;
  ranged?: boolean;
  magic?: boolean;
  summon?: boolean;
}

const RAW = combatJson as unknown as Record<string, ItemCombat>;

// ---- 鞭系（DefaultToWhip 提取，Item.cs SetDefaults switch 共 18 把）----
import whipsJson from './vanilla-whips.json';
const WHIPS = whipsJson as unknown as Record<string, { proj: number; dmg: number; kb: number; speed: number; anim: number }>;

// ---- 提取缺口补丁（tools/extract-itemcombat.mjs 只解析 case 内字面赋值）----
// DefaultToSpear/DefaultToStaff/DefaultToMagicWeapon/DefaultToRangedWeapon 的形参
// 赋值（Item.cs:47630/:48045/:48057）漏提：4347/4348/4703/5629 仅剩 damage/knockBack、
// 4788-4790（剑矛三件 DefaultToSpear+SetWeaponValues）与 4060-4062 整条缺失。
// 下表按源码 case 逐件 1:1（:35651/:35672/:37119/:38629/:39341-39353/:44212）：
//   DefaultToSpear → useStyle5 / useTime=useAnimation=animationTime / shootSpeed=push / noMelee+melee
//   DefaultToStaff → magic / autoReuse / mana=manaPerShot / UseSound43
//   DefaultToMagicWeapon → magic / noMelee / useTime=useAnimation=singleShotTime
//   DefaultToRangedWeapon → noMelee / ranged / useAmmo=ammoID（5629 随后 ranged=false 已在表内）
const EXTRACT_PATCH: Record<string, Partial<ItemCombat>> = {
  '4060': { shoot: 728, useAmmo: 75, useTime: 18, useAnimation: 18, shootSpeed: 20, damage: 60, knockBack: 5, noMelee: true, ranged: true, autoReuse: true },
  '4061': { shoot: 730, useTime: 28, useAnimation: 28, shootSpeed: 3.5, damage: 14, knockBack: 6, noMelee: true, melee: true },
  '4062': { shoot: 731, useTime: 17, useAnimation: 17, shootSpeed: 8, mana: 6, damage: 24, knockBack: 3, noMelee: true, magic: true, autoReuse: true },
  '4347': { shoot: 876, useTime: 36, useAnimation: 36, shootSpeed: 15, noMelee: true, magic: true },
  '4348': { shoot: 876, useTime: 36, useAnimation: 36, shootSpeed: 15, noMelee: true, magic: true },
  '4703': { shoot: 14, useAmmo: 97, useTime: 55, useAnimation: 55, shootSpeed: 7, noMelee: true, ranged: true },
  '4788': { shoot: 877, useTime: 24, useAnimation: 24, shootSpeed: 3.5, damage: 60, knockBack: 12, noMelee: true, melee: true },
  '4789': { shoot: 878, useTime: 24, useAnimation: 24, shootSpeed: 3.5, damage: 130, knockBack: 14, noMelee: true, melee: true },
  '4790': { shoot: 879, useTime: 24, useAnimation: 24, shootSpeed: 3.5, damage: 90, knockBack: 13, noMelee: true, melee: true },
  '5629': { shoot: 1088, useAmmo: 27, useTime: 20, useAnimation: 20, shootSpeed: 10, noMelee: true, autoReuse: true },
};

const TABLE: Record<string, ItemCombat> = { ...RAW };
for (const k of Object.keys(EXTRACT_PATCH)) {
  TABLE[k] = { ...(RAW[k] ?? {}), ...EXTRACT_PATCH[k] } as ItemCombat;
}

/** 原版 item id → 战斗数据（无条目返回 null） */
export function itemCombat(vanillaId: number): ItemCombat | null {
  return TABLE[String(vanillaId)] ?? null;
}

/** 弓类 AmmoID.Arrow = 40（AmmoID.cs:116） */
export const AMMO_ARROW = 40;
/** AmmoID 常量（AmmoID.cs:114-146）：子弹/凝胶/钱币/坠落之星/沙/飞镖/火箭/溶液/信号弹 */
export const AMMO_GEL = 23;
export const AMMO_COIN = 71;
export const AMMO_FALLEN_STAR = 75;
export const AMMO_BULLET = 97;
export const AMMO_SAND = 169;
export const AMMO_DART = 283;
export const AMMO_ROCKET = 771;
export const AMMO_SOLUTION = 780;
export const AMMO_FLARE = 931;

// ================= vi_* 武器语义解析（1456 数据驱动） =================

/** vi_<id>_<slug> key → 原版 item id（vi_ 批次未显式存 vid 时从 key 反解） */
export function viIdFromKey(key: string): number {
  const m = key.match(/^vi_(\d+)_/);
  return m ? Number(m[1]) : -1;
}

export type CombatWeapon =
  | { kind: 'melee'; damage: number; knockback: number; useTime: number; useAnimation: number; autoReuse: boolean; shoot?: number; shootSpeed?: number }
  | { kind: 'summon'; shoot: number; sentry: boolean; damage: number; knockback: number; useTime: number; shootSpeed: number }
  | { kind: 'whip'; shoot: number; damage: number; knockback: number; useTime: number; shootSpeed: number; itemId: number }
  | {
      kind: 'boomerang' | 'spear' | 'yoyo' | 'flail' | 'grenade' | 'glowstick' | 'magic' | 'shot' | 'summon';
      shoot: number;

```


---

## 🤖 Assistant · 2026-08-12T15:54:12.990Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '7100,7200p' src/core/Game.ts",
 "description": "Read melee swing chain"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:13.036Z

**📎 ToolResult**

```
    else if (style >= 25 && style <= 27) num = 10;
    else if (style >= 28 && style <= 30) num = 4; // hardMode 才 ×4，肉前应为 1——此处取肉前
    else if (style >= 31 && style <= 33) num = 2;
    else if (style >= 34 && style <= 36) num = 1.25;
    coins *= (num * 2 + 1) / 3;
    if (coins > 1000) coins = 1000; // 防御性上限（原版由 Item.NewItem 内部面值转换）
    drop(73, Math.max(1, Math.round(coins)));
  }

  private updateSwingHits() {
    if (!this.swing) return;
    this.swing.t--;
    if (this.swing.t <= 0) { this.swing = null; return; }
    const held = this.player.inv.heldItem();
    if (!held) return;
    const heldDef = ITEM_DEFS[held.id];
    const tool = heldDef.tool ?? this.itemFuncTool(held.id);
    // ---- 近战整体门（Player.cs:42964）：(damage>=0 && !noMelee) 才进 GetMeleeHitbox，
    // 且 CutTiles/MeleeHitNPCs 都在 damage>0 内（cs:42991-43006）——
    // 此前挥动药水/镜子（damage=0）也带 32×32 近战盒：砍草 + 对敌 1 点伤害 + 对小动物
    // 一击致死，均为原版没有的行为（vi_ 数值取 combat 表，legacy 工具取 def.tool）
    const swingVid = heldDef.vid ?? viIdFromKey(heldDef.key);
    const swingCombat = swingVid >= 0 ? itemCombat(swingVid) : null;
    const meleeDmg = this.swing.dmg ?? tool?.damage ?? swingCombat?.damage ?? 0;
    const noMelee = heldDef.magic || swingCombat?.noMelee;
    if (noMelee || meleeDmg <= 0) return;
    // ---- 原版 ItemCheck_GetMeleeHitbox（Player.cs:44480）1:1：矩形判定非圆形 ----
    // 基础矩形 = ApplyUseStyle 三段 itemLocation（手部位置，公式同 drawUseItem）+ **恒 32×32**
    // （cs:44489 new Rectangle(itemLocation.X, itemLocation.Y, 32, 32) ×adjustedItemScale≈1，
    // 与武器贴图尺寸无关——此前误用贴图帧宽高当基底，小武器欠打大武器超打）；
    // 方向/重力翻转（cs:44506-44513）；useStyle1 三段扩展（cs:44516-44540）：
    // **早段(anim≥0.666max) 宽×2 高×1.4 X 退 1.2宽 / 中段原样 / 晚段(anim<0.333max)
    // 宽×1.4 高×1.1 Y 下移半高**——此前早/晚段扩展对调，注释也反
    const pAnim = Math.min(1, Math.max(0, this.swing.t / this.swing.dur));
    const ar = this.renderer?.atlas ? atlasIconForKey(this.renderer.atlas, ITEM_DEFS[held.id].key) : null;
    const sprW = ar?.sw ?? 16, sprH = ar?.sh ?? 16;
    const xTier = (w: number, phase: 0 | 1 | 2) => phase === 0
      ? w >= 92 ? 38 : w >= 64 ? 28 : w >= 52 ? 24 : w > 32 ? 14 : 10
      : phase === 1
        ? w >= 92 ? 38 : w >= 64 ? 28 : w >= 52 ? 24 : w > 32 ? 18 : 10
        : w >= 92 ? 38 : w >= 64 ? 28 : w >= 52 ? 24 : w >= 48 ? 18 : w > 32 ? 14 : 6;
    const yTier = (h: number, phase: 0 | 1 | 2) => phase === 0 ? 24
      : h > 64 ? 14 : h > 52 ? 12 : phase === 1 && h > 32 ? 8 : 10;
    let offX: number, offY: number;
    const phase: 0 | 1 | 2 = pAnim > 2 / 3 ? 0 : pAnim > 1 / 3 ? 1 : 2;
    const hitUs = this.swing.useStyle ?? 1;
    if (hitUs === 3) {
      // useStyle 3（雨伞 946/4707）单一持位（cs:50279-50294）：
      // offX = fw/2-4-max(pAnim*fw*1.2-10, 8)、offY = 顶+24
      offX = sprW * 0.5 - 4 - Math.max(pAnim * sprW * 1.2 - 10, 8);
      offY = 24;
    } else if (phase === 0) { offX = sprW * 0.5 - xTier(sprW, 0); offY = yTier(sprH, 0); }
    else if (phase === 1) { offX = sprW * 0.5 - xTier(sprW, 1); offY = yTier(sprH, 1); }
    else { offX = -(sprW * 0.5 - xTier(sprW, 2)); offY = yTier(sprH, 2); }
    const p = this.player;
    let bx = p.cx + p.facing * offX;
    let by = p.y + offY;
    let bw = 32, bh = 32; // 恒定基底（cs:44489），与武器贴图无关
    if (p.facing === -1) bx -= bw;
    by -= bh;
    if (hitUs === 3) {
      // useStyle 3（cs:44545-44560 + :50279-50312）：anim>0.666 收势段 dontAttack；
      // 判定段宽×1.4 / 高×0.6（Y 下移 0.6 高）；雨伞本体再 高+14 宽-10（朝左 X+10）
      if (pAnim > 0.666) return;
      if (p.facing === -1) bx -= Math.floor(bw * 1.4 - bw);
      bw = Math.floor(bw * 1.4);
      by += Math.floor(bh * 0.6);
      bh = Math.floor(bh * 0.6);
      if (swingVid === 946 || swingVid === 4707) {
        bh += 14;
        bw -= 10;
        if (p.facing === -1) bx += 10;
      }
    } else if (phase === 0) {
      // 三段扩展（cs:44516-44540）：早段大盒覆盖抡起区、晚段小盒收势
      if (p.facing === 1) bx -= Math.floor(bw * 1.2);
      bw *= 2;
      by -= Math.floor(bh * 1.4 - bh);
      bh = Math.floor(bh * 1.4);
    } else if (phase === 2) {
      if (p.facing === -1) bx -= Math.floor(bw * 1.4 - bw);
      bw = Math.floor(bw * 1.4);
      by += Math.floor(bh * 0.5);
      bh = Math.floor(bh * 1.1);
    }
    // 原版 ItemCheck_CutTiles（Player.cs:44002）：挥击矩形内所有 tileCut/KillTile
    for (let ty = Math.floor(by / TILE); ty <= Math.floor((by + bh - 1) / TILE); ty++) {
      for (let tx = Math.floor(bx / TILE); tx <= Math.floor((bx + bw - 1) / TILE); tx++) {
        const tk = tx * 100000 + ty;
        if (this.swingTileCutSet.has(tk)) continue;
        const t = this.world.store.get(tx, ty);
        if (t === POT_TILE) {
          this.swingTileCutSet.add(tk);
          this.smashPot(tx, ty);
        } else if (TILE_CUT.has(t)) {
          this.swingTileCutSet.add(tk);
          this.breakTile(tx, ty);
        }
      }
    }
    // 矩形-AABB 相交判定（原版 ItemCheck_MeleeHitNPCs 的 npc.getRect().Intersects(itemRectangle)）

```


---

## 🤖 Assistant · 2026-08-12T15:54:16.769Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — the melee chain already prioritizes legacy def.tool then falls back to vi combat. Actually: `const tool = heldDef.tool ?? this.itemFuncTool(held.id)` and `meleeDmg = this.swing.dmg ?? tool?.damage ?? swingCombat?.damage ?? 0`.

Now tests referencing local keys. I have partial lists. Let me do a comprehensive grep of tests for local keys. Also tools/. Let me compile a list of test files with matches using the union of the key sets.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:21.041Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "KEYS='dirt_block|stone_block|wood|sand_block|snow_block|platform|torch|door|workbench|furnace|anvil|chest|gel|acorn|mushroom_item|copper_ore|iron_ore|silver_ore|gold_ore|copper_bar|iron_bar|silver_bar|gold_bar|lens|suspicious_eye|lesser_healing_potion|coin_copper|coin_silver|coin_gold|coin_platinum|heal_potion|agility_potion|ironskin_potion|thorns_potion|regen_potion|lucky_horseshoe|feral_claws|_helmet|_chainmail|_greaves|wood_pickaxe|wood_axe|wood_sword|wood_hammer|copper_pickaxe|copper_axe|copper_sword|copper_hammer|iron_pickaxe|iron_axe|iron_sword|iron_hammer|silver_pickaxe|silver_axe|silver_sword|silver_hammer|gold_pickaxe|gold_axe|gold_sword|gold_hammer|tin_ore|lead_ore|tungsten_ore|platinum_ore|tin_bar|lead_bar|tungsten_bar|platinum_bar|demonite_ore|meteorite|hellstone|crimtane_ore|cobalt_ore|mythril_ore|adamantite_ore|palladium_ore|orichalcum_ore|titanium_ore|chlorophyte_ore|sapphire|ruby|emerald|topaz|amethyst|diamond|ice_block|ice_brick|snow_brick|sandstone_block|hardened_sand_block|desert_fossil|clay_block|glass|obsidian|gray_brick|red_brick|mud_block|silt_block|bookcase|grandfather_clock|piano|dresser|bathtub|keg|cooking_pot|clay_pot|tombstone|life_crystal|candle|chandelier|lantern|candelabra|chinese_lantern|skull_lantern|water_candle|bomb|rope|grass_seeds|_bucket|tin_pickaxe|tin_axe|tin_sword|lead_pickaxe|lead_axe|lead_sword|tungsten_pickaxe|tungsten_axe|tungsten_sword|platinum_pickaxe|platinum_axe|platinum_sword|wooden_bow|wooden_arrow|flaming_arrow|iron_bow|minecart_item|wand_of_sparking|amethyst_bolt|worm_food|bloody_spine|slime_crown|mechanical_worm|mechanical_eye|mechanical_skull|red_wrench|blue_wrench|green_wrench|yellow_wrench|wire_cutter|actuator_item|actuation_rod|multicolor_wrench|grand_design|goblin_battle_standard|snow_globe|pirate_map|obsidian_skin_potion|gills_potion|mana_regen_potion|magic_power_potion|featherfall_potion|water_walking_potion|archery_potion|night_owl_potion'; grep -rlE \"['\\\"\\`]($KEYS)['\\\"\\`]\" tests tools --include=\"*.ts\" | sort",
 "description": "List test files referencing local keys"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:21.106Z

**📎 ToolResult**

```
tests/arrow-tree-pass.test.ts
tests/cavewalls.test.ts
tests/conveyor.test.ts
tests/explosion.test.ts
tests/hostile-proj-player-hit.test.ts
tests/item-coverage.test.ts
tests/living-tree.test.ts
tests/lunar-final-audit.test.ts
tests/micro-biomes.test.ts
tests/mining.test.ts
tests/pot-break.test.ts
tests/proj-critter-hit.test.ts
tests/projectile-reflect.test.ts
tests/save.test.ts
tests/shimmer.test.ts
tests/smart-cursor.test.ts
tests/thrown-weapons.test.ts
tests/tile-drop-null.test.ts
tests/vanilla-recipes.test.ts
tests/vi-weapons.test.ts
tests/wld-furnace-mapping.test.ts
tests/world-difficulty.test.ts

```


---

## 🤖 Assistant · 2026-08-12T15:54:23.739Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Some of those only use tile keys (cavewalls, conveyor, explosion, living-tree, lunar-final-audit, micro-biomes, pot-break, wld-furnace-mapping). Let me distinguish per test file which matches are item keys vs tile keys. Let me grep each item-key-only pattern per file. Actually let me do a targeted grep for ITEM_BY_KEY / ITEM_DEFS / item usage in tests.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:24.506Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"ITEM_BY_KEY\\['[^v]|ITEM_BY_KEY\\[\\\"[^v]|def\\.key === '[^v]|key === '[a-z]\" tests --include=\"*.ts\" | grep -v \"vi_\" | head -60",
 "description": "Find item-key usage in tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:24.552Z

**📎 ToolResult**

```
tests/shimmer.test.ts:138:    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY['torch'], 5);
tests/world-difficulty.test.ts:68:    const torch = ITEM_BY_KEY['torch']!;
tests/world-difficulty.test.ts:69:    const pick = ITEM_BY_KEY['copper_pickaxe']!;
tests/smart-cursor.test.ts:43:const pick = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['copper_pickaxe']], tool: { type: 'pick' as const, power: 35 } });
tests/smart-cursor.test.ts:44:const axe = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['copper_axe']], tool: { type: 'axe' as const, power: 7 } });
tests/smart-cursor.test.ts:45:const hammer = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['wood_hammer']], tool: { type: 'hammer' as const, power: 25 } });
tests/smart-cursor.test.ts:46:const torchItem = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['torch']], tool: null });
tests/smart-cursor.test.ts:47:const dirtItem = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['dirt_block']], tool: null });
tests/smart-cursor.test.ts:48:const platformItem = () => ({ def: ITEM_DEFS[ITEM_BY_KEY['platform']], tool: null });
tests/smart-cursor.test.ts:278:    const target = run(mkEnv(st, mouseAt(104, 97), { def: ITEM_DEFS[ITEM_BY_KEY['empty_bucket']], tool: null }));
tests/smart-cursor.test.ts:287:    const dual = { ...ITEM_DEFS[ITEM_BY_KEY['copper_pickaxe']], key: 'test_drax', axePower: 100 };
tests/wind-sway.test.ts:159:    const dirt = TILE_DEFS.findIndex((d) => d.key === 'dirt');
tests/wind-sway.test.ts:161:    const tree = TILE_DEFS.findIndex((d) => d.key === 'tree');
tests/save.test.ts:26:    world.chests.push({ x: 5, y: 5, items: [{ id: ITEM_BY_KEY['torch'], stack: 3 }, null] });
tests/save.test.ts:29:    inv.add(ITEM_BY_KEY['dirt_block'], 77);
tests/thrown-weapons.test.ts:39:    const bow = ITEM_DEFS[ITEM_BY_KEY['wood_bow']];
tests/thrown-weapons.test.ts:46:    const arrow = ITEM_DEFS[ITEM_BY_KEY['wooden_arrow']];

```


---

## 🤖 Assistant · 2026-08-12T15:54:25.307Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"ITEM_BY_KEY|ITEM_DEFS\" tests/item-coverage.test.ts tests/mining.test.ts tests/vi-weapons.test.ts tests/save.test.ts tests/shimmer.test.ts tests/thrown-weapons.test.ts 2>/dev/null | grep -v \"vi_\" | head -40",
 "description": "Check item usage in key tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:25.353Z

**📎 ToolResult**

```
tests/item-coverage.test.ts:5:import { ITEM_DEFS, ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID } from '../src/data/items';
tests/item-coverage.test.ts:17:    expect(ITEM_DEFS.length).toBeGreaterThanOrEqual(6100);
tests/item-coverage.test.ts:22:      expect(ITEM_BY_KEY[key]).toBeDefined();
tests/shimmer.test.ts:24:import { ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID } from '../src/data/items';
tests/shimmer.test.ts:128:    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY[key], 2);
tests/shimmer.test.ts:138:    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY['torch'], 5);
tests/shimmer.test.ts:152:    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY[VANILLA_ITEM_KEY_BY_ID[75]], 1);
tests/mining.test.ts:7:import { ITEM_DEFS, ITEM_BY_KEY } from '../src/data/items';
tests/mining.test.ts:40:      const t = ITEM_DEFS[ITEM_BY_KEY[key]]?.tool;
tests/thrown-weapons.test.ts:4:import { ITEM_BY_KEY, ITEM_DEFS } from '../src/data/items';
tests/thrown-weapons.test.ts:12:function thrownCombat(def: (typeof ITEM_DEFS)[number]): { shoot: number; damage: number } | null {
tests/thrown-weapons.test.ts:39:    const bow = ITEM_DEFS[ITEM_BY_KEY['wood_bow']];
tests/thrown-weapons.test.ts:46:    const arrow = ITEM_DEFS[ITEM_BY_KEY['wooden_arrow']];
tests/save.test.ts:6:import { ITEM_BY_KEY } from '../src/data/items';
tests/save.test.ts:26:    world.chests.push({ x: 5, y: 5, items: [{ id: ITEM_BY_KEY['torch'], stack: 3 }, null] });
tests/save.test.ts:29:    inv.add(ITEM_BY_KEY['dirt_block'], 77);
tests/vi-weapons.test.ts:5:import { ITEM_BY_KEY, ITEM_DEFS } from '../src/data/items';
tests/vi-weapons.test.ts:7:const def = (key: string) => ITEM_DEFS[ITEM_BY_KEY[key]];
tests/vi-weapons.test.ts:76:    for (const d of ITEM_DEFS) {

```


---

## 🤖 Assistant · 2026-08-12T15:54:28.173Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: tests/thrown-weapons.test.ts:39 uses 'wood_bow' which doesn't exist ('wooden_bow' does) — likely returns undefined. Interesting but not needed.

Also tests/item-coverage.test.ts:37 `Lang.itemNameByKey('copper_pickaxe')`.

Let me read item-coverage.test.ts fully (it may enumerate local keys), mining.test.ts, vi-weapons.test.ts, vanilla-recipes.test.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:28.274Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/item-coverage.test.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:28.294Z

**📎 ToolResult**

```
1	import { describe, it, expect, beforeAll } from 'vitest';
2	import { readFileSync } from 'node:fs';
3	import { languageManager } from '../src/i18n/LanguageManager';
4	import { Lang } from '../src/i18n/Lang';
5	import { ITEM_DEFS, ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID } from '../src/data/items';
6	
7	// 真实包注入（后加载覆盖：zh-Hans 最后 → 断言中文）
8	beforeAll(() => {
9	  for (const c of ['en-US', 'zh-Hans']) {
10	    languageManager.loadPackJson(JSON.parse(readFileSync(`public/l10n/${c}.json`, 'utf8')));
11	  }
12	});
13	
14	// 全量物品多语言覆盖：6146 件原版物品 + place_v_* 放置物品走方块译名链
15	describe('物品全量多语言覆盖', () => {
16	  it('注册表覆盖全部原版物品（≥6100）且 VANILLA_ITEM_KEY_BY_ID 同规模', () => {
17	    expect(ITEM_DEFS.length).toBeGreaterThanOrEqual(6100);
18	    expect(Object.keys(VANILLA_ITEM_KEY_BY_ID).length).toBeGreaterThanOrEqual(6000);
19	    // 映射表条目全部指向真实注册 key
20	    for (const [id, key] of Object.entries(VANILLA_ITEM_KEY_BY_ID).slice(0, 500)) {
21	      void id;
22	      expect(ITEM_BY_KEY[key]).toBeDefined();
23	    }
24	  });
25	
26	  it('原版物品名 12 语言官方译名链（vi_ 前缀 → ItemName）', () => {
27	    // 动态注册的物品经 id 反查表取名（任意抽 3 个动态 id）
28	    const dyn = Object.entries(VANILLA_ITEM_KEY_BY_ID).slice(4000, 4003);
29	    for (const [id, key] of dyn) {
30	      void id;
31	      const n = Lang.itemNameByKey(key);
32	      expect(n).toBeTruthy();
33	      expect(n).not.toBe(key); // 不是裸 key 兜底
34	    }
35	    // 抽查既有物品
36	    expect(Lang.itemNameByKey('vi_75_fallen_star')).toBe('坠落之星');
37	    expect(Lang.itemNameByKey('copper_pickaxe')).toBe('铜镐');
38	  });
39	
40	  it('place_v_* 放置物品名 = 方块译名（place_v_144_timers → 1秒计时器）', () => {
41	    expect(Lang.itemNameByKey('place_v_144_timers')).toBe('1秒计时器');
42	    expect(Lang.itemNameByKey('place_v_136_switch')).toBe('开关');
43	    // 世界生成专属块（树）→ tileName 第③级 id-maps zh
44	    expect(Lang.itemNameByKey('place_v_5_trees')).toBeTruthy();
45	  });
46	
47	  it('英文 def.name 已清空（vi_/place_v_ 不再携带英文名兜底）', () => {
48	    const vi = ITEM_DEFS.filter((d) => d.key.startsWith('vi_'));
49	    expect(vi.length).toBeGreaterThan(5000);
50	    for (const d of vi.slice(0, 1000)) {
51	      expect(d.name === '' || /[一-鿿]/.test(d.name)).toBe(true);
52	    }
53	  });
54	
55	  it('墙名链（wallName）：放置墙走物品名，自然墙走 id-maps', () => {
56	    expect(Lang.wallName(1)).toBeTruthy();   // Stone Wall（自然墙 → id-maps/物品）
57	    expect(Lang.wallName(9999)).toBeNull();
58	  });
59	});
60	

```


---

## 🤖 Assistant · 2026-08-12T15:54:28.633Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,80p' tests/mining.test.ts; echo \"=== vi-weapons\"; sed -n '1,90p' tests/vi-weapons.test.ts",
 "description": "Read mining and vi-weapons tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:28.690Z

**📎 ToolResult**

```
// 挖掘/砍伐击数验证（原版 1:1，阈值 100，冷却 useTime）：
// 伤害公式（Player.cs:45098 axe×1.2 / :52981 pick + 分档除数 / tileNoFail=100）
// 铜斧(7)砍树：int(7×1.2)=8/击 → 13 击（用户实测原版 ≈13，此前我们 ×5.5=3 击是错的）
// 铜镐(35)泥土：35/击 → 3 击；金镐(55)石：55/击 → 2 击；银镐(45)银矿(门槛20)：45→3 击
// tileNoFail（草丛 sheet 3 等）：100 → 1 击
import { describe, it, expect } from 'vitest';
import { ITEM_DEFS, ITEM_BY_KEY } from '../src/data/items';
import { TILE_DEFS, TILE_BY_KEY } from '../src/data/tiles';

/** 原版每击伤害（Game.tryMine 移植的同一公式——此处独立复算做回归锚） */
export function vanillaHitDamage(sheet: number, toolType: 'pick' | 'axe', power: number): number {
  const NO_FAIL = new Set([3, 4, 24, 32, 35, 50, 51, 52, 61, 62, 69, 73, 74, 81, 82, 83, 84, 110, 113, 115, 129, 162, 165, 184, 185, 186, 187, 192, 201, 205, 227, 233, 254, 324, 330, 331, 332, 333, 373, 374, 375, 382, 384, 461, 481, 482, 483, 484, 485, 518, 519, 528, 529, 530, 549, 624, 636, 637, 638, 654, 655, 656, 666, 697, 700, 701, 705, 709]);
  const AXE = new Set([5, 72, 80, 323, 488, 583, 584, 585, 586, 587, 589, 596, 616, 634, 704]);
  if (NO_FAIL.has(sheet)) return 100;
  if (AXE.has(sheet)) return toolType === 'axe' ? Math.floor((sheet === 80 ? power * 3 : power) * 1.2) : 0;
  if (toolType !== 'pick') return 0;
  let dmg = power;
  if (sheet === 107 || sheet === 221) dmg = Math.floor(power / 2);
  else if (sheet === 108 || sheet === 222) dmg = Math.floor(power / 3);
  else if (sheet === 111 || sheet === 223) dmg = Math.floor(power / 4);
  else if (sheet === 211) dmg = Math.floor(power / 5);
  else if (sheet === 226 || sheet === 237) dmg = Math.floor(power / 4);
  else if ([25, 203, 117, 58, 41, 43, 44, 481, 482, 483].includes(sheet)) dmg = Math.floor(power / 2);
  else if (sheet === 48 || sheet === 232) dmg = power * 2;
  // 门槛（取地表上方；地下门槛建另一用例）
  const gates: Array<[number, number]> = [[211, 200], [25, 65], [203, 65], [117, 65], [37, 50], [56, 55], [58, 65], [226, 210], [237, 210], [41, 100], [43, 100], [44, 100]];
  for (const [sh, gate] of gates) if (sheet === sh && power < gate) return 0;
  return dmg;
}

const hits = (sheet: number, toolType: 'pick' | 'axe', power: number): number => {
  const d = vanillaHitDamage(sheet, toolType, power);
  if (d <= 0) return Infinity;
  return Math.ceil(100 / d);
};

describe('工具数据（原版 Item.cs SetDefaults 提取值核对）', () => {
  it('铜镐/铜斧/铁镐/铁斧/银/金 全字段', () => {
    const expect_ = (key: string, type: string, power: number, damage: number, useTime: number) => {
      const t = ITEM_DEFS[ITEM_BY_KEY[key]]?.tool;
      expect(t?.type).toBe(type);
      expect(t?.power).toBe(power);
      expect(t?.damage).toBe(damage);
      expect(t?.useTime).toBe(useTime);
    };
    expect_('copper_pickaxe', 'pick', 35, 4, 15);   // 3509
    expect_('copper_axe', 'axe', 7, 3, 21);          // 3506
    expect_('iron_pickaxe', 'pick', 40, 5, 13);       // 1
    expect_('iron_axe', 'axe', 9, 5, 19);             // 10
    expect_('silver_pickaxe', 'pick', 45, 6, 11);     // 3515
    expect_('silver_axe', 'axe', 10, 6, 18);          // 3512
    expect_('gold_pickaxe', 'pick', 55, 6, 17);       // 3521
    expect_('gold_axe', 'axe', 11, 7, 18);            // 3518
    expect_('wood_hammer', 'hammer', 25, 2, 25);      // 196
  });
});

describe('击数（阈值 100，原版公式）', () => {
  it('树：斧族专属；铜斧 13 击 / 铁斧 10 击 / 金斧 8 击', () => {
    expect(hits(5, 'axe', 7)).toBe(13);    // int(8.4)=8 → ceil(100/8)=13
    expect(hits(5, 'axe', 9)).toBe(10);    // int(10.8)=10
    expect(hits(5, 'axe', 11)).toBe(8);    // int(13.2)=13 → ceil=8
    expect(hits(5, 'pick', 35)).toBe(Infinity); // 镐不能砍树（tileAxe 排除）
  });
  it('泥土/石/矿：铜镐 3 击 / 金镐 2 击', () => {
    expect(hits(0, 'pick', 35)).toBe(3);    // 泥土
    expect(hits(1, 'pick', 35)).toBe(3);    // 石
    expect(hits(1, 'pick', 55)).toBe(2);    // 金镐
    expect(hits(7, 'pick', 35)).toBe(3);    // 铜矿
  });
  it('tileNoFail：花草/蘑菇植物 1 击', () => {
    expect(hits(3, 'pick', 35)).toBe(1);    // 森林短草
    expect(hits(24, 'pick', 12)).toBe(1);   // 腐化短草（木镐也秒）
  });
  it('门槛：黑檀石 65 / 陨石 50 / 黑曜石 55 / 地牢砖 100', () => {
    expect(hits(25, 'pick', 55)).toBe(Infinity);  // 银镐 55 < 65
    expect(hits(25, 'pick', 65)).toBe(4);         // int(65/2)=32 → 4 击
    expect(hits(37, 'pick', 40)).toBe(Infinity);  // 铁镐 < 50
    expect(hits(56, 'pick', 54)).toBe(Infinity);  // < 55
    expect(hits(56, 'pick', 55)).toBe(2);         // 黑曜石无除数（全伤 55）→ 2 击（原版非 /2 族）
=== vi-weapons
// vi_* 数据驱动武器分类与数值测试（1456 combat/projectiles 表驱动）
import { describe, it, expect } from 'vitest';
import { combatWeapon, thrownCombat, projGravity } from '../src/data/vanillaItemCombat';
import { projectileData } from '../src/data/vanillaProjectiles';
import { ITEM_BY_KEY, ITEM_DEFS } from '../src/data/items';

const def = (key: string) => ITEM_DEFS[ITEM_BY_KEY[key]];

describe('vi_* 武器分类（combatWeapon）', () => {
  it('纯近战：铁剑走 melee 分支且数值来自 combat 表', () => {
    const w = combatWeapon({ key: 'vi_4_iron_shortsword' });
    // useAnimation=挥击动画时长 / autoReuse=持按连挥（Player.ItemCheck 分立计数）
    expect(w).toEqual({ kind: 'melee', damage: 12, knockback: 5.5, useTime: 20, useAnimation: 20, autoReuse: false });
  });

  it('回旋镖：附魔回旋镖 → boomerang + 投射物 6（aiStyle 3）', () => {
    const w = combatWeapon({ key: 'vi_55_enchanted_boomerang' });
    expect(w?.kind).toBe('boomerang');
    if (w?.kind === 'boomerang') expect(w.shoot).toBe(6);
    expect(projectileData(6)?.aiStyle).toBe(3);
  });

  it('长矛：木矛 → spear + 投射物 46（aiStyle 19，DefaultToSpear 展开验证）', () => {
    const w = combatWeapon({ key: 'vi_274_spear' });
    expect(w?.kind).toBe('spear');
    if (w?.kind === 'spear') expect(w.shoot).toBe(46);
    expect(projectileData(46)?.aiStyle).toBe(19);
  });

  it('悠悠球：投影射物 546 → yoyo（aiStyle 99，区间块+DefaultToYoyo 展开验证）', () => {
    // 找一个 shoot=546 的物品：直接验证投射物表与分发器的联动
    expect(projectileData(546)?.aiStyle).toBe(99);
    const yoyo = combatWeapon({ key: 'vi_3284_amarok' });
    expect(yoyo?.kind).toBe('yoyo');
  });

  it('连枷：链球 → flail（aiStyle 15，DefaultToFlail 展开验证）', () => {
    const w = combatWeapon({ key: 'vi_162_ball_o_hurt' });
    expect(w?.kind).toBe('flail');
    expect(projectileData(25)?.aiStyle).toBe(15);
  });

  it('爆炸物：手雷 → grenade（ai16，必须先于投掷判定）', () => {
    const w = combatWeapon({ key: 'vi_166_grenade' });
    expect(w?.kind).toBe('grenade');
    if (w?.kind === 'grenade') {
      expect(w.shoot).toBe(28);
      expect(projectileData(28)?.aiStyle).toBe(16);
    }
  });

  it('魔法：紫晶法杖 → magic，mana 5、shoot 121', () => {
    const w = combatWeapon({ key: 'vi_739_amethyst_staff' });
    expect(w).toMatchObject({ kind: 'magic', mana: 5, shoot: 121, damage: 15, useTime: 37 });
  });

  it('手里剑仍是 ai2 投掷武器（combatWeapon 不接管，thrownCombat 命中）', () => {
    expect(combatWeapon({ key: 'vi_42_shuriken' })).toBeNull();
    expect(thrownCombat({ key: 'vi_42_shuriken' })).toEqual({ shoot: 3, damage: 10 });
  });

  it('弓（useAmmo 体系）不被 combatWeapon 分流', () => {
    expect(combatWeapon({ key: 'wooden_bow', vid: 39 })).toBeNull();
  });
});

describe('辅助数据', () => {
  it('projGravity：ai2/16 抛物线 0.3，直飞 0', () => {
    expect(projGravity(3)).toBe(0.3);   // 手里剑 ai2
    expect(projGravity(28)).toBe(0.3);  // 手雷 ai16
    expect(projGravity(121)).toBe(0);   // 紫晶弹 ai29 直飞
  });

  it('已注册物品全链路：分类器对 ITEM_DEFS 的 vi_ 武器可稳定判定', () => {
    let n = 0;
    for (const d of ITEM_DEFS) {
      if (!d.key.startsWith('vi_')) continue;
      if (combatWeapon(d) || thrownCombat(d)) n++;
    }
    expect(n).toBeGreaterThan(80); // 至少覆盖近战+回旋镖+长矛+魔法+投掷各族
  });
});

```


---

## 🤖 Assistant · 2026-08-12T15:54:30.760Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now vanilla-recipes.test.ts — RECIPES dedup tests. Let me read it and vanillaRecipes.ts to understand vanillaItemKey/ingredientKey and whether vanilla recipes can cover early game chain.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:30.985Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,120p' tests/vanilla-recipes.test.ts",
 "description": "Read vanilla-recipes test"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:31.061Z

**📎 ToolResult**

```
// 原版配方管线测试（2688 条提取 + 组匹配 + 可用性）
import { describe, it, expect } from 'vitest';
import {
  VANILLA_RECIPES, RECIPE_GROUPS, RECIPE_GROUP_ITEMS, expandStationTiles,
  collectOwnedItems, craftableCount, envOk, vanillaItemKey, invIndexOfVanilla,
  type VanillaCraftCtx,
} from '../src/data/vanillaRecipes';
import { Inventory } from '../src/items/Inventory';
import { ITEM_BY_KEY, ITEM_DEFS } from '../src/data/items';
import { RECIPES } from '../src/data/recipes';

const ctx = (over: Partial<VanillaCraftCtx> = {}): VanillaCraftCtx => ({
  nearbyInternal: new Set(),
  ...over,
});

describe('原版配方提取', () => {
  it('3173 条（去重终态：模板+雕像+反向全含）+组 31+继承 9', () => {
    expect(VANILLA_RECIPES.length).toBe(3173); // 线性+生成器+模板22件套+小动物雕像+反向平台/墙，源码重复注册已去重
    expect(Object.keys(RECIPE_GROUPS).length).toBe(31);
    expect(Object.keys(RECIPE_GROUP_ITEMS).length).toBe(31);
  });

  it('火把配方：1 木(组)+1 凝胶 徒手 出 3', () => {
    const torch = VANILLA_RECIPES.find((r) => r.create === 8);
    expect(torch).toBeDefined();
    expect(torch!.tile).toBe(-1);
    expect(torch!.createStack).toBe(3);
    expect(torch!.items).toEqual([{ id: 23, stack: 1 }, { id: 9, stack: 1 }]);
    expect(torch!.groups).toContain(RECIPE_GROUPS['Wood']);
  });

  it('Wood 组含 9 种木材（id 9/619/620/621/911/1729/2504/2503/5215）', () => {
    const wood = RECIPE_GROUP_ITEMS[String(RECIPE_GROUPS['Wood'])];
    expect(wood).toEqual([9, 619, 620, 621, 911, 1729, 2504, 2503, 5215]);
  });

  it('站点继承链：玻璃窑302→熔炉17→篝火215', () => {
    expect(expandStationTiles(302)).toEqual([302, 17, 215]);
    expect(expandStationTiles(134)).toEqual([134, 16]);
  });
});

describe('可用性计算', () => {
  it('组聚合：持有任一木材即满足 Wood 组计数', () => {
    const inv = new Inventory();
    // 木头=9：先确认内部 id 可反查
    const woodIid = invIndexOfVanilla(9);
    expect(woodIid).toBeGreaterThanOrEqual(0);
    inv.slots[10] = { id: woodIid, stack: 5 };
    const owned = collectOwnedItems(inv);
    expect(owned.get(9)).toBe(5);
    expect(owned.get(1000000 + RECIPE_GROUPS['Wood'])).toBe(5);
  });

  it('craftableCount：火把 5 木+1 凝胶 → 5 次；缺凝胶 → 0', () => {
    const inv = new Inventory();
    const woodIid = invIndexOfVanilla(9);
    const gelIid = invIndexOfVanilla(23);
    inv.slots[10] = { id: woodIid, stack: 5 };
    const torch = VANILLA_RECIPES.find((r) => r.create === 8)!;
    expect(craftableCount(torch, collectOwnedItems(inv))).toBe(0); // 缺凝胶
    inv.slots[11] = { id: gelIid, stack: 2 };
    expect(craftableCount(torch, collectOwnedItems(inv))).toBe(2); // 凝胶 2 木 5 → min(5,2)
  });

  it('envOk：铁砧配方需附近铁砧（tile16）；徒手配方恒过', () => {
    const anvilRecipe = VANILLA_RECIPES.find((r) => r.tile === 16);
    expect(anvilRecipe).toBeDefined();
    expect(envOk(anvilRecipe!, ctx())).toBe(false);
    // 附近有秘银砧(134)也算（继承链 134→16）
    const mithril = expandStationTiles(134);
    const fakeNearby = new Set<number>(mithril); // 模拟站点扫描（内部 id 近似用 sheet id 演示）
    // envOk 用 SHEET_TO_INTERNAL——此处直接断言展开链语义
    expect(mithril).toContain(16);
  });
});

// ---- 自制配方表防回归（2026-08 重复配方事故：木锤×2/钨锭×2/铂锭×2 + vi_ 产物双显） ----
describe('自制配方表 RECIPES 去重 + 与原版表不重叠', () => {
  it('内部无重复配方（out+count+station+inputs 全同）', () => {
    const seen = new Set<string>();
    for (const r of RECIPES) {
      const key = `${r.out}|${r.count}|${r.station}|${r.inputs.map(([k, n]) => `${k}x${n}`).sort().join(',')}`;
      expect(seen.has(key), `重复配方: ${r.out}`).toBe(false);
      seen.add(key);
    }
  });

  it('产物禁用 vi_ 前缀（防与原版配方段双显；vi_ 一律走 vanilla-recipes）', () => {
    const bad = RECIPES.filter((r) => r.out.startsWith('vi_'));
    expect(bad, `vi_ 产物: ${bad.map((r) => r.out).join(',')}`).toEqual([]);
  });

  it('木锤恰好一条；魔力水晶走原版表（徒手坠星×5）', () => {
    expect(RECIPES.filter((r) => r.out === 'wood_hammer')).toHaveLength(1);
    expect(RECIPES.some((r) => r.out === 'vi_109_mana_crystal')).toBe(false);
    const mc = VANILLA_RECIPES.find((r) => r.create === 109)!;
    expect(mc.tile).toBe(-1); // 徒手
    expect(mc.items).toEqual([{ id: 75, stack: 5 }]);
  });
});

```


---

## 🤖 Assistant · 2026-08-12T15:54:31.121Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/vanillaRecipes.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:31.146Z

**📎 ToolResult**

```
1	// 原版配方数据运行时（tools/extract-recipes.mjs 从 Terarria1456 Recipe.cs 提取，2688 条）。
2	// 可用性 = Recipe.UpdateRecipeList（Recipe.cs:229-258）：环境条件（站点/液体/群系）× 材料计数。
3	// 组匹配 = RecipeGroup（id 假偏移 1000000，Recipe.cs:20）——组计数 = 组内所有物品持有数之和。
4	import recipesJson from './vanilla-recipes.json';
5	import { itemCombat } from './vanillaItemCombat';
6	import { TILE_DEFS, TILE_BY_KEY } from './tiles';
7	import { ITEM_DEFS } from './items';
8	import type { Inventory } from '../items/Inventory';
9	
10	export interface VanillaRecipe {
11	  create: number;          // 原版 item id
12	  createStack: number;
13	  tile: number;           // 站点 TileID（-1=徒手）
14	  items: Array<{ id: number; stack: number }>;
15	  groups: number[];
16	  honey?: boolean; water?: boolean; lava?: boolean;
17	  snow?: boolean; graveyard?: boolean; alchemy?: boolean;
18	}
19	
20	const DOC = recipesJson as unknown as {
21	  count: number;
22	  groups: Record<string, number>;
23	  groupItems: Record<string, number[]>;
24	  tileCountsAs: Record<string, number>;
25	  recipes: VanillaRecipe[];
26	};
27	export const VANILLA_RECIPES = DOC.recipes;
28	export const RECIPE_GROUPS = DOC.groups;
29	export const RECIPE_GROUP_ITEMS = DOC.groupItems;
30	export const TILE_COUNTS_AS = DOC.tileCountsAs;
31	
32	/** 站点继承递归展开（Player.SetAdjTile :35192-35208）：tile 本身 + CountsAs 链全部置位 */
33	export function expandStationTiles(tile: number): number[] {
34	  const out = [tile];
35	  let cur = tile;
36	  for (let hop = 0; hop < 6; hop++) {
37	    const next = TILE_COUNTS_AS[String(cur)];
38	    if (next === undefined) break;
39	    out.push(next);
40	    cur = next;
41	  }
42	  return out;
43	}
44	
45	/** vi_<id> key → 原版 item id 反解 */
46	export function vanillaIdOfItemKey(key: string): number {
47	  const m = key.match(/^vi_(\d+)_/);
48	  return m ? Number(m[1]) : -1;
49	}
50	
51	/** 玩家持有的原版 id 计数表（含 RecipeGroup 假 id 聚合，Recipe.cs:408-415） */
52	export function collectOwnedItems(inv: Inventory): Map<number, number> {
53	  const owned = new Map<number, number>();
54	  const add = (vid: number, n: number) => owned.set(vid, (owned.get(vid) ?? 0) + n);
55	  const inc = (key: string, stack: number) => {
56	    const def = ITEM_DEFS[inv[key as never] as unknown as number];
57	    void def;
58	  };
59	  void inc;
60	  // slots 0-57（背包+钱币+弹药）
61	  for (const s of inv.slots) {
62	    if (!s) continue;
63	    const def = ITEM_DEFS[s.id];
64	    if (!def) continue;
65	    const vid = def.vid ?? (def.key.startsWith('vi_') ? parseInt(def.key.slice(3), 10) : -1);
66	    if (vid >= 0) add(vid, s.stack);
67	  }
68	  // RecipeGroup 假 id 聚合（组内所有物品持有数之和）
69	  for (const [gidS, items] of Object.entries(RECIPE_GROUP_ITEMS)) {
70	    let sum = 0;
71	    for (const it of items) sum += owned.get(it) ?? 0;
72	    if (sum > 0) add(1000000 + Number(gidS), sum);
73	  }
74	  return owned;
75	}
76	
77	/** 材料匹配（RequiredItemEntry.Matches Recipe.cs:35-42）：普通物比 id，组查假 id */
78	function itemMatches(reqId: number, groupIds: number[], owned: Map<number, number>): number {
79	  if (reqId >= 1000000) return owned.get(reqId) ?? 0;
80	  return owned.get(reqId) ?? 0;
81	}
82	
83	/** 单条配方当前可合成次数（HowManyTimesCanRecipeBeCrafted Recipe.cs:289-310）；
84	 *  返回 0 = 材料不足 */
85	export function craftableCount(r: VanillaRecipe, owned: Map<number, number>): number {
86	  let min = Infinity;
87	  for (const req of r.items) {
88	    const have = itemMatches(req.id, r.groups, owned);
89	    if (have < req.stack) return 0;
90	    min = Math.min(min, Math.floor(have / req.stack));
91	  }
92	  return min === Infinity ? 0 : min;
93	}
94	
95	/** 站点 TileID → 本仓库内部 tile id（TILE_BY_KEY 反查 v_<id>_ key 不稳定，按 vanilla.sheet 扫 TILE_DEFS） */
96	const SHEET_TO_INTERNAL = (() => {
97	  const m = new Map<number, number>();
98	  for (let i = 0; i < TILE_DEFS.length; i++) {
99	    const sheet = TILE_DEFS[i]?.vanilla?.sheet;
100	    if (sheet !== undefined && !m.has(sheet)) m.set(sheet, i);
101	  }
102	  return m;
103	})();
104	
105	export interface VanillaCraftCtx {
106	  /** 附近站点（内部 tile id 集合——Game.stationsNearby 扫描结果） */
107	  nearbyInternal: Set<number>;
108	  /** 附近有炼金台（tile 355/699 经继承算 tile 13；player.alchemyTable）——炼金配方材料 1/3 免费 */
109	  alchemyTable?: boolean;
110	  /** 附近液体：水/蜂蜜/岩浆源（adjWaterSource/adjHoney/adjLava） */
111	  nearWater?: boolean;
112	  nearHoney?: boolean;
113	  nearLava?: boolean;
114	  zoneSnow?: boolean;
115	  zoneGraveyard?: boolean;
116	}
117	
118	/** 环境条件（PlayerMeetsEnvironmentConditions Recipe.cs:321-357） */
119	export function envOk(r: VanillaRecipe, ctx: VanillaCraftCtx): boolean {
120	  if (r.tile >= 0) {
121	    const expanded = expandStationTiles(r.tile);
122	    // 任一等价站点在附近（adjTile[requiredTile] + CountsAs 继承）
123	    const ok = expanded.some((t) => {
124	      const internal = SHEET_TO_INTERNAL.get(t);
125	      return internal !== undefined && ctx.nearbyInternal.has(internal);
126	    });
127	    if (!ok) return false;
128	  }
129	  if (r.water && !ctx.nearWater) return false;
130	  if (r.honey && !ctx.nearHoney) return false;
131	  if (r.lava && !ctx.nearLava) return false;
132	  if (r.snow && !ctx.zoneSnow) return false;
133	  if (r.graveyard && !ctx.zoneGraveyard) return false;
134	  return true;
135	}
136	
137	/** 成品 → 本仓库 item key（vi_<id>_* 反查） */
138	const VID_TO_KEY = (() => {
139	  const m = new Map<number, string>();
140	  for (const def of ITEM_DEFS) {
141	    const vid = def.vid ?? (def.key.startsWith('vi_') ? parseInt(def.key.slice(3), 10) : -1);
142	    if (vid >= 0 && !m.has(vid)) m.set(vid, def.key);
143	  }
144	  return m;
145	})();
146	
147	export function vanillaItemKey(vid: number): string | undefined {
148	  return VID_TO_KEY.get(vid);
149	}
150	
151	/** 材料原版 id → 显示名用的本仓库 key（组内物品可能部分缺，取第一个存在的） */
152	export function ingredientKey(vid: number): string | undefined {
153	  if (vid >= 1000000) {
154	    const items = RECIPE_GROUP_ITEMS[String(vid - 1000000)];
155	    if (items) for (const it of items) {
156	      const k = VID_TO_KEY.get(it);
157	      if (k) return k;
158	    }
159	    return undefined;
160	  }
161	  return VID_TO_KEY.get(vid);
162	}
163	
164	/** 计算可用配方索引列表（UpdateRecipeList 主干） */
165	export function availableRecipes(inv: Inventory, ctx: VanillaCraftCtx): Array<{ r: VanillaRecipe; count: number }> {
166	  const owned = collectOwnedItems(inv);
167	  const out: Array<{ r: VanillaRecipe; count: number }> = [];
168	  for (const r of VANILLA_RECIPES) {
169	    if (!envOk(r, ctx)) continue;
170	    const count = craftableCount(r, owned);
171	    if (count > 0) out.push({ r, count });
172	  }
173	  return out;
174	}
175	
176	/** 执行合成（CraftingRequests.CraftLocally 主干）：扣材料→返成品 key（放置进背包由调用方） */
177	export function consumeMaterials(inv: Inventory, r: VanillaRecipe, times = 1, alchemyTable = false): boolean {
178	  for (const req of r.items) {
179	    let need = req.stack * times;
180	    // 炼金折扣（GetIngredientCraftingDiscount Recipe.cs:213-227：alchemy 配方且 alchemyTable
181	    // 时每个材料独立掷 1/3 概率该份免费——按"每份独立掷骰"逐个扣）
182	    if (r.alchemy && alchemyTable && times === 1) {
183	      let discounted = 0;
184	      for (let k = 0; k < need; k++) if (Math.random() < 1 / 3) discounted++;
185	      need -= discounted;
186	      if (need <= 0) continue;
187	    }
188	    // 组材料：按组内物品依序扣
189	    if (req.id >= 1000000) {
190	      const items = RECIPE_GROUP_ITEMS[String(req.id - 1000000)] ?? [];
191	      for (const gid of items) {
192	        if (need <= 0) break;
193	        const key = VID_TO_KEY.get(gid);
194	        if (!key) continue;
195	        const internal = (Object as unknown as { _k?: never });
196	        void internal;
197	        // 直接经 ITEM_DEFS 反查内部 id 再 inv.remove
198	        const iid = invIndexOfVanilla(gid);
199	        if (iid < 0) continue;
200	        const have = inv.countOf(iid);
201	        const take = Math.min(have, need);
202	        if (take > 0) { inv.remove(iid, take); need -= take; }
203	      }
204	      if (need > 0) return false;
205	    } else {
206	      const iid = invIndexOfVanilla(req.id);
207	      if (iid < 0 || inv.countOf(iid) < need) return false;
208	      inv.remove(iid, need);
209	    }
210	  }
211	  return true;
212	}
213	
214	/** 原版 item id → Inventory 内部 item id（缓存） */
215	const _iidCache = new Map<number, number>();
216	export function invIndexOfVanilla(vid: number): number {
217	  let hit = _iidCache.get(vid);
218	  if (hit !== undefined) return hit;
219	  const key = VID_TO_KEY.get(vid);
220	  // ITEM_DEFS 下标即内部 id——线性扫一次后缓存
221	  for (let i = 0; i < ITEM_DEFS.length; i++) {
222	    const d = ITEM_DEFS[i];
223	    const v = d.vid ?? (d.key.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
224	    if (v === vid) { hit = i; break; }
225	  }
226	  hit ??= -1;
227	  _iidCache.set(vid, hit);
228	  return hit;
229	}
230	
231	/** 供合成 UI 判定"此物品是合成材料吗"（ItemID.Sets.IsAMaterial 近似：出现在任一配方材料中） */
232	export const MATERIAL_VIDS = (() => {
233	  const s = new Set<number>();
234	  for (const r of VANILLA_RECIPES) for (const req of r.items) s.add(req.id);
235	  return s;
236	})();
237	
238	export type VanillaRecipeLike = VanillaRecipe;
239	export { itemCombat };
240	

```


---

## 🤖 Assistant · 2026-08-12T15:54:43.273Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Critical: `collectOwnedItems` only counts items with vid >= 0 — local keys without `vid` field contribute NOTHING. So local wood/gel etc. (no vid in defs) are invisible to vanilla recipes. This is a big migration finding: currently the vanilla recipe section can't use local 'wood'/'gel' as materials because they have no vid. Only coin_platinum (vid 73), wooden_bow (vid 39), wooden_arrow (vid 40), flaming_arrow (vid 41), iron_bow (vid 99), goblin_battle_standard (vid 361), snow_globe (vid 602), pirate_map (vid 1301... wait pirate_map: 1301 in map but PRIV says 10491; ITEM_KEY_TO_ID says 1315 — discrepancy), mechanical_* have vid. So if RECIPES is removed without giving local items vid, early crafting chain breaks because vanilla recipes require vid-keyed items.

Wait but VID_TO_KEY maps vid → first ITEM_DEFS entry with that vid. vi_9_wood is registered? Let's check: 'vi_3_stone_block', 'vi_94_wood_platform', 'vi_26_stone_wall', 'vi_93_wood_wall' are registered but wood itself (vi_9_wood)? Not in items.ts explicit list, but the auto-registration loop registers ALL vanilla.json items as vi_<id>_<key> — so vi_9_wood exists. And VID_TO_KEY picks the FIRST def with vid 9 — the local 'wood' has no vid, so vi_9_wood is picked. invIndexOfVanilla(9) → vi_9_wood. So vanilla recipes already produce/consume vi_ items. Good — meaning the vanilla recipe chain is self-sufficient on the vi_ side (it crafts vi_8_torch? Actually create=8 → vanillaItemKey(8) → first def with vid 8 → 'torch' has no vid... hmm 'torch' local def has no vid field. So VID_TO_KEY.get(8) = vi_8_Torch (auto-registered). Let me confirm 'vi_8_' exists in vanilla.json. Probably yes.

But wait — collectOwnedItems counts by vid: local 'wood' (no vid) is not counted, so if the player holds local 'wood' from tree chopping, vanilla torch recipe (wood group 9) sees 0. This is the "early chain" dependency: local wood from breaking trees feeds RECIPES table (legacy) but NOT vanilla recipes. Actually let me verify: does the wood drop key 'wood' have vid? In items.ts line 82: item({ key: 'wood', name: '木材', tile: 'wood' }) — no vid. Correct.

So currently: legacy RECIPES consumes local items; vanilla recipes consume vi_ items. If local items are deleted and drops remapped to vi_ keys, vanilla recipes become usable with materials. 

Now, spawn drops: Game.ts 5104: `const key = dropId === 3 ? 'stone_block' : VANILLA_ITEM_KEY_BY_ID[dropId]` — dropId 3 = stone → local 'stone_block' special-cased. Interesting: VANILLA_ITEM_KEY_BY_ID[3] = 'vi_3_stone_block' exists, so why special case? Probably because local key first. Whatever.

Also Game.ts 7009: `const override: Record<number, string> = { 8: 'torch', 73: 'coin_copper' }` — override map vid→local key.

Let me now check spawnDrop signature and Enemy drop key mapping (Enemy.ts:59-61 ITEM_DROP_KEY_OVERRIDE).

Also check Game.ts 8687 coin remap table (coin_copper → vi_71_CopperCoin etc.) — that's an existing migration precedent! Let me read that context.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:43.943Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '8660,8720p' src/core/Game.ts; echo \"=== 6990-7020\"; sed -n '6995,7020p' src/core/Game.ts; echo \"=== 5090-5115\"; sed -n '5095,5115p' src/core/Game.ts",
 "description": "Read coin remap and drop override"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:44.004Z

**📎 ToolResult**

```
        // 世界难度不参与死亡惩罚（只管掉落/伤害倍率等），曾两轴混接
        const charDiff = p.appearance?.difficulty ?? 0;
        // 先记死亡时身家（Player.cs:38247-38250 lostCoins=coinsOwned——死亡 UI「掉了{0}」；
        // 软核/旅程随后被 DropCoins 实际掉落额覆盖 :38318-38324，中核/硬核的钱随
        // 物品全掉 → 身家即损失额）
        this.lostCoins = this.coinsOwned();
        // 中核/硬核：掉落全部物品（Player.cs:38254 DropItems(gemsOnly=false)：软核/旅程
        // 才走 gemsOnly=true 只掉宝石——本仓无背包宝石，近似为不掉）
        if (dropsAllItemsOnDeath(charDiff)) {
          dropInventoryOnDeath(p.inv, (key, stack) => {
            this.spawnDrop(p.cx, p.cy, key, stack, (Math.random() - 0.5) * 8, -2 - Math.random() * 2);
          });
        }
        // 硬核：角色消亡（Player.cs:38255-38257 HardcoreDeathPenalty → KillMeForGood :38173+
        // 删 .plr 角色档 + ghost 化 :16894；本仓最小集 = 标记不可重生 + 流程层回写角色存档）
        if (charDiff === 2 && p.appearance && !p.appearance.hardcoreDead) {
          p.appearance = { ...p.appearance, hardcoreDead: true };
          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.HardcoreDeath', this.playerName()));
          this.cb.onHardcoreDeath?.(p.appearance);
        }
        // 软核/旅程：掉钱（Player.cs:38318-38326 difficulty==0||3 才走 DropCoins；
        // DropCoins :53351-53390 掉钱档按**世界难度**：经典掉一半/专家 3/4/大师全掉）
        if (dropsCoinsOnDeath(charDiff)) {
          const keep = deathCoinKeepFraction(this.world.difficulty);  // Main.GameMode（Main.cs:2677）
          let lost = 0;
          const face = [1, 100, 10000, 1000000];
          const coinKeys = [
            ['coin_copper', 'vi_71_CopperCoin'], ['coin_silver', 'vi_72_SilverCoin'],
            ['coin_gold', 'vi_73_GoldCoin'], ['coin_platinum', 'vi_74_PlatinumCoin'],
          ];
          coinKeys.forEach(([ck, vk], ci) => {
            for (const k of [ck, vk]) {
              const id = ITEM_BY_KEY[k];
              if (id === undefined) continue;
              const n = p.inv.countOf(id);
              if (n > 0) {
                lost += (n - Math.floor(n * keep)) * face[ci];
                p.inv.remove(id, n - Math.floor(n * keep));
              }
            }
          });
          this.lostCoins = lost; // DrawInterface_35 "掉了{0}"（重生于 respawnPlayer 清零）
        }
        // 垃圾桶死亡清空（Player.cs:53394 mouseItem/trashItem 语义）
        p.inv.trash = null;
      }
    }
  }

  addDamageNumber(x: number, y: number, amount: number, crit: boolean, color = '#FFF') {
    this.dmgNumbers.push({ x, y, vy: -1.6, value: amount, crit, color, life: 50 });
  }

  /** 弹幕消亡钩子（Projectile.Kill 按弹型分发）：
   *  碎镜 1085（Projectile.cs:67554-67574）——弹体命中盒外扩 150px 与玩家矩形
   *  相交 → brokenMirrorBadLuckTime = 25200（luck −0.25 档，UpdateBrokenMirrorLuck
   *  :28700-28711 衰减）。原版此处另有 Gore 1394-1397 碎片与尘 330——未移植，登记 */
  onProjectileDeath(projId: number, x: number, y: number, w = 0, h = 0) {
    if (projId !== 1085) return;
    const R = 150;
    const p = this.player;
=== 6990-7020
    this.sfx.play('shatter');
    this.spawnParticles(ax * TILE + 16, ay * TILE + 16, '#9A6A5A', 10, 2.6, { life: 200, damp: 0.985, grav: 0.09 });
    this.spawnParticles(ax * TILE + 16, ay * TILE + 16, '#C4A48C', 6, 2.0, { life: 180, damp: 0.985, grav: 0.09 });
    this.potLoot(ax, ay, style);
  }

  /** 瓦罐掉落（SpawnThingsFromPot 肉前普通世界分支，WorldGen.cs:57100-57760） */
  private potLoot(x: number, y: number, style: number) {
    const w = this.world;
    const underworldY = w.store.h - 200; // UnderworldLayer ≈ maxTilesY-200
    const flag = y < w.rockLevel;         // 原版 flag：j < rockLayer（地表+泥土层）
    // item id → 我们 key：VANILLA_ITEM_KEY_BY_ID 全量映射（vi_ 表覆盖 6146 件）+
    // 原生 def 覆盖（火把/铜币有原生实现）
    const drop = (itemId: number, n = 1): ItemDrop | null => {
      const override: Record<number, string> = { 8: 'torch', 73: 'coin_copper' };
      const key = override[itemId] ?? VANILLA_ITEM_KEY_BY_ID[itemId];
      if (!key) return null;
      return this.spawnDrop(x * TILE + 8, y * TILE + 8, key, n, (Math.random() - 0.5) * 2.4, -2 - Math.random());
    };
    /** 心 pickup（item 58 是 IsAPickup：触碰回血不进包——此处曾误当蘑菇收集物） */
    const dropHeart = () => { const h = drop(58); if (h) h.pickup = 'heart'; };
    const R = (n: number) => (Math.random() * n) | 0;
    // L57213：1/45 稀有 → 按深度三张药水表
    if (R(45) === 0) {
      if (y < w.groundLevel) {
        const n = R(10);
=== 5090-5115
      const gemOf: Record<number, [number, number]> = {
        583: [180, 4851], 584: [181, 4852], 585: [177, 4853],
        586: [179, 4854], 587: [178, 4855], 588: [182, 4856], 589: [999, 4857],
      };
      const [gemId, seedId] = gemOf[gemSheet];
      const height2 = bottom - top + 1;
      for (let yy = top; yy <= bottom; yy++) {
        const dropId = Math.random() < 0.1 ? gemId : 3;   // 1/10 宝石 / 9/10 石块
        const stack = dropId === 3 ? 1 + Math.floor(Math.random() * 2) : 1;
        const key = dropId === 3 ? 'stone_block' : VANILLA_ITEM_KEY_BY_ID[dropId];
        if (key && ITEM_BY_KEY[key] !== undefined) {
          this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, yy * TILE,
            key, stack, (Math.random() - 0.5) * 2, -2 - Math.random());
        }
      }
      // 干基格 50% gemcorn（树苗种子；frameX≥22 即主干底格）
      if (isBase && Math.random() < 0.5) {
        const seedKey = VANILLA_ITEM_KEY_BY_ID[seedId];
        if (seedKey && ITEM_BY_KEY[seedKey] !== undefined) {
          this.spawnDrop(x * TILE + 8, bottom * TILE, seedKey, 1, (Math.random() - 0.5) * 2, -2 - Math.random());
        }

```


---

## 🤖 Assistant · 2026-08-12T15:54:44.466Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '50,70p' src/entities/Enemy.ts; echo \"=== Extractinator\"; sed -n '60,85p' src/world/Extractinator.ts",
 "description": "Read Enemy drop key override"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:44.511Z

**📎 ToolResult**

```
  dropVelocity, npcValueOf, type NpcDropCtx,
} from '../drops/NpcDrops';
import { npcShimmerTransformTo, npcShimmerTransformToItem } from '../stats/Shimmer';

/** 无 key 映射的原版物品 id（一次性告警用） */
const UNMAPPED_WARNED = new Set<number>();
/** 有原生实现的原版物品 id → 原生 key（钱币=货币计数/凝胶火把晶状体=配方素材，
 *  必须走原生 def 而非 vi_ 占位注册） */
const NATIVE_DROP_KEY: Record<number, string> = {
  71: 'coin_copper', 72: 'coin_silver', 73: 'coin_gold', 74: 'coin_platinum',
  23: 'gel', 8: 'torch', 236: 'lens', 3: 'stone_block', 2: 'dirt_block', 9: 'wood',
  28: 'lesser_healing_potion',
};
/** 雕像产怪战利品门（NPCID.Sets，NPC.cs :79648-79654 NPCLoot 早退用） */
const STATUE_NO_EARLYMODE_LOOT = new Set([480, 82, 86, 170, 180, 171]);
/** DoesntDespawnToInactivity 名单（NPC.cs:78584-78641）中本批涉及的仪式/月总链类型——
 *  神秘石碑 437/忠实信徒 438/弓手 379,380（拜月仪式链条，离屏消失会断 439 召唤链）与
 *  月总游离眼 400（锚核心 398 生命周期，自身不参与离屏消散）。
 *  690 雕像宝箱怪休眠态（CheckActive :78692 `type==690 && ai[0]==0` 豁免）——AI_126
 *  未移植时 ai0 恒 0 = 永远休眠，离屏不消散与原版休眠态一致 */
const NO_DESPAWN_IDS = new Set([379, 380, 400, 437, 438, 690]);
=== Extractinator
/** 普通苔藓池（:222-242 与 :247-267，4349 绿/4350 棕/4351 红/4352 蓝/4353 紫） */
const MOSS_COMMON = [4349, 4350, 4351, 4352, 4353] as const;
/** 稀有苔藓池（:198-218，仅叶绿版 642 有 1/10 机会；4354 熔岩/4389 氩/4377 氪/5127 紫/4378 氙） */
const MOSS_RARE = [4354, 4389, 4377, 5127, 4378] as const;
/** 前困难矿石（RollOreEarlymode :511-523：12 铜/11 铁/14 银/13 金/699 锡/700 铅/701 钨/702 铂） */
const ORE_PREHM = [12, 11, 14, 13, 699, 700, 701, 702] as const;
/** 困难矿石（RollOreHardmode :490-509，仅 642 且 Main.hardMode：
 *  12/11/14/13/699/700/701/702 + 364 钴/1104 钯/365 秘银/1105 山铜/366 精金/1106 钛金） */
const ORE_HM = [12, 11, 14, 13, 699, 700, 701, 702, 364, 1104, 365, 1105, 366, 1106] as const;

/** 钱币（71 铜/72 银/73 金/74 铂）→ 掉落用 coin key（Game 侧消费） */
export const COIN_KEY_BY_VID: Readonly<Record<number, string>> = {
  71: 'coin_copper', 72: 'coin_silver', 73: 'coin_gold', 74: 'coin_platinum',
};

/**
 * RollExtractinatorDrop（ExtractinatorHelper.cs:5-488）1:1。
 * 判定链顺序不可调换（原版 if/else-if 短路即概率表）：
 *   num4 坚固化石(仅 mode1) → num7 钱币大表 → num 琥珀蚊 → num5 垃圾 → num6 苔藓
 *   → num9 草种(仅 mode4) → num8 泥土 → num11 蜂蜜块 → num10 沙 → num2 宝石
 *   → num3 琥珀 → 1/3 钱币小表 → 兜底矿石
 */
export function rollExtractinatorDrop(
  extractionMode: number,
  extractinatorBlockType: number,
  rand: ExtractinatorRand,

```


---

## 🤖 Assistant · 2026-08-12T15:54:51.909Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Very good. NATIVE_DROP_KEY in Enemy.ts and COIN_KEY_BY_VID in Extractinator.ts and override in Game.potLoot are the three "vid → local key" drop bridges.

Now let me check NpcDrops to see how drops flow (vid → key resolution).
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:54:52.908Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"NATIVE_DROP_KEY\\|VANILLA_ITEM_KEY_BY_ID\\|COIN_KEY_BY_VID\" src --include=\"*.ts\" | grep -v idNames | head -20; echo \"=== NpcDrops key resolve\"; grep -n \"key\" src/drops/NpcDrops.ts | head -30",
 "description": "Find drop key resolution"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:52.969Z

**📎 ToolResult**

```
src/wld/WldImport.ts:7:import { ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID } from '../data/items';
src/wld/WldImport.ts:918:      const key = ITEM_MAP[it.id] ?? VANILLA_ITEM_KEY_BY_ID[it.id];
src/core/Game.ts:63:  CHLOROPHYTE_TRADES, COIN_KEY_BY_VID, findExtractinatorChest,
src/core/Game.ts:74:import { ITEM_DEFS, ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID } from '../data/items';
src/core/Game.ts:372:      // VANILLA_ITEM_KEY_BY_ID 以 vanilla id 为键，不能反过来用（内部 id 撞号会掉错物品）
src/core/Game.ts:373:      const key = ITEM_DEFS[s.id]?.key ?? VANILLA_ITEM_KEY_BY_ID[s.id];
src/core/Game.ts:390:  const starter = [VANILLA_ITEM_KEY_BY_ID[3507] ?? 'copper_sword',
src/core/Game.ts:391:    VANILLA_ITEM_KEY_BY_ID[3509] ?? 'copper_pickaxe', VANILLA_ITEM_KEY_BY_ID[3506] ?? 'copper_axe'];
src/core/Game.ts:1582:        const key = VANILLA_ITEM_KEY_BY_ID[vid];
src/core/Game.ts:1593:        const key = VANILLA_ITEM_KEY_BY_ID[vid];
src/core/Game.ts:2152:        const recKey = VANILLA_ITEM_KEY_BY_ID[musicBoxRecordItem(this.lastMusic)];
src/core/Game.ts:4815:        dropKey = VANILLA_ITEM_KEY_BY_ID[musicBoxDropItemOf(Math.floor(preFrameY / 36))] ?? dropKey;
src/core/Game.ts:4818:        if (fDrop > 0) dropKey = VANILLA_ITEM_KEY_BY_ID[fDrop] ?? dropKey;
src/core/Game.ts:4853:          : sheet === 24 && fx === 144 ? VANILLA_ITEM_KEY_BY_ID[60]
src/core/Game.ts:4854:            : sheet === 201 && fx === 270 ? VANILLA_ITEM_KEY_BY_ID[2887]
src/core/Game.ts:4878:      const gemKey = VANILLA_ITEM_KEY_BY_ID[gemId];
src/core/Game.ts:4946:      dropKey = VANILLA_ITEM_KEY_BY_ID[4144] ?? null;
src/core/Game.ts:4948:      dropKey = VANILLA_ITEM_KEY_BY_ID[Math.random() < 1 / 30 ? 4144 : 989] ?? null;
src/core/Game.ts:5104:        const key = dropId === 3 ? 'stone_block' : VANILLA_ITEM_KEY_BY_ID[dropId];
src/core/Game.ts:5112:        const seedKey = VANILLA_ITEM_KEY_BY_ID[seedId];
=== NpcDrops key resolve
99:function warnOnce(key: string, msg: string) {
100:  if (warned.has(key)) return;
101:  warned.add(key);

```


---

## 🤖 Assistant · 2026-08-12T15:54:53.235Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"spawnDrop(\" src/core/Game.ts | head -5; echo \"=== spawnDrop def\"; grep -n \"spawnDrop(x\" src/core/Game.ts | head -3; sed -n \"$(grep -n 'spawnDrop(x: number, y: number, key' src/core/Game.ts | head -1 | cut -d: -f1),+25p\" src/core/Game.ts",
 "description": "Read spawnDrop signature"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:54:59.078Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
src/core/Game.ts:1038:      this.spawnDrop(dxDrop * TILE + 8, dyDrop * TILE, key, n, 0, 0);
src/core/Game.ts:1594:        if (key) this.spawnDrop(px, py, key, 1);
src/core/Game.ts:4728:        this.spawnDrop(ax * TILE + 8, ay * TILE, 'vi_1291_life_fruit', 1);
src/core/Game.ts:4745:      this.spawnDrop(x * TILE + 8, y * TILE + 8, dropKey, 1);
src/core/Game.ts:4753:      this.spawnDrop(doorAnchor[0] * TILE + 8, doorAnchor[1] * TILE, def.drop ?? 'door', 1);
=== spawnDrop def
4745:      this.spawnDrop(x * TILE + 8, y * TILE + 8, dropKey, 1);
4860:        this.spawnDrop(x * TILE + 8, y * TILE + 8, mushroomDrop, 1);
4880:        this.spawnDrop(x * TILE + 8, y * TILE + 8, gemKey, 1);
sed: 1: ",+25p
": invalid command code ,

```


---

## 🤖 Assistant · 2026-08-12T15:55:05.815Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enough on drops. Now check remaining areas:

1. mainFlow.ts starter items + dev toolbars.
2. UI.ts other local key references (I have most).
3. SmartCursor local key references (env.held.def?.key === 'torch', 'empty_bucket', 'actuator_item').
4. Renderer.ts:3131 'torch' special case.
5. Game.ts:1456 iron armor order; 1645-1647 starter; 2313 bed; 2558 water_candle; 2565; 2579; 3084-3085; 3562/3728 suspicious_eye; 3767 life_crystal; 5328 acorn; 5334 rope; 5689 bed; 6457 coins; 7250 coin drop; 7436-7438 coin counting; 7460 bomb keys; 8470-8513 coin deposit; 8687 coin keys; 9605 torch spawn; 9670-72 stations; 10103 coin value; 1083 minecart texture; 1320 wire tools; 3964+ boss summons; 4062 buckets; 6872-6913 bucket swap; 5178-5222 actuator.

Let me check mainFlow.ts around 320 and 194.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:55:05.818Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '180,230p;310,335p' src/mainFlow.ts",
 "description": "Read mainFlow starter gear and migration"
}
```


---

## 🤖 Assistant · 2026-08-12T15:55:05.849Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '380,400p;1440,1470p;1630,1660p' src/core/Game.ts",
 "description": "Read Game starter and iron armor order"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:05.904Z

**📎 ToolResult**

```
  async function quickLoad() {
    if (!quickSaveExists) { ui.toast(Lang.text('Mods.SandboxWorld.Toast.NoQuickSave')); return; }
    await loadFromKey(QUICK_SAVE_KEY);
  }

  /** 玩家状态回填（worker/主线程两路共用） */
  function applyPlayer(g: Game, player: ReturnType<typeof loadSaveData>['player']) {
    g.player.hp = player.hp;
    g.player.x = player.x;
    g.player.y = player.y;
    // 上限扩容进度（水晶之心/生命果/魔力水晶；旧档缺省 100/20/20）
    if (player.baseMaxHp !== undefined) g.player.baseMaxHp = player.baseMaxHp;
    if (player.baseMaxMana !== undefined) g.player.baseMaxMana = player.baseMaxMana;
    if (player.mana !== undefined) g.player.mana = player.mana;
    // 背包布局迁移（旧 54 槽自创布局 → 原版 58 槽+armor[20]；Inventory.migrateLegacy 判别）
    const mig = Inventory.migrateLegacy(player.inventory);
    g.player.inv.slots = mig.slots;
    if (player.armor) g.player.inv.armor = player.armor.map((it) => it ? { ...it } : null);
    if (player.dye) g.player.inv.dye = player.dye.map((it) => it ? { ...it } : null);
    if (player.trash) g.player.inv.trash = { ...player.trash };
    // 杂项装备/染料 + 三套 Loadout 回填（旧档缺省全空）
    if (player.miscEquips) g.player.inv.miscEquips = player.miscEquips.map((it) => it ? { ...it } : null);
    if (player.miscDyes) g.player.inv.miscDyes = player.miscDyes.map((it) => it ? { ...it } : null);
    if (player.loadouts) {
      for (let k = 0; k < 3; k++) {
        const src = player.loadouts[k];
        if (!src) continue;
        g.player.inv.loadouts[k] = {
          armor: src.armor.map((it) => it ? { ...it } : null),
          dye: src.dye.map((it) => it ? { ...it } : null),
        };
      }
    }
    if (player.currentLoadout !== undefined) g.player.inv.currentLoadout = player.currentLoadout;
    g.player.inv.selected = player.selected;
    // 玩家储物×4 回填（29/97/463/491；旧档缺省全空）
    if (player.banks) {
      for (let b = 0; b < 4; b++) {
        const src = player.banks[b] ?? [];
        g.player.banks[b] = src.concat(Array(Math.max(0, 40 - src.length)).fill(null)).slice(0, 40);
      }
    }
    // Buff 槽（PL:53913-53925;Main.buffNoSave 已在序列化侧过滤）
    g.player.buffs.applySaved(player.buffs);
    if (player.taxMoney !== undefined) g.player.taxMoney = player.taxMoney;   // PL:53839
    if (player.golferScoreAccumulated) g.player.golferScoreAccumulated = player.golferScoreAccumulated; // PL:1792
    if (player.deathsPve !== undefined) g.player.deathsPve = player.deathsPve; // PL:53840
    // ★ 读档回填后必须刷 UI：HUD 快捷栏在 makeGame 时以空背包画过一次，
    //   此前不刷新 → 存档道具要等用户点工具栏/开背包才显示
    g.cb.onInventoryChanged();
  }
    ui.showProgress(Lang.text('Mods.SandboxWorld.Progress.ParsingWld'), 0.1);
    try {
      const { save, report, seedText, gameMode } = parseWldToSave(buf);
      (window as unknown as { __lastCompatReport?: unknown }).__lastCompatReport = report;
      ui.showProgress(Lang.text('Mods.SandboxWorld.Progress.ConvertingWld'), 0.7);
      const g = makeGame();
      // 直接消费内存 SaveData(2026-08 审计 #3:此前的 stringify→parse 双拷贝
      // 每次导入多出 2×20~50MB 峰值,且让 5 份全图副本并存更久)
      const { world } = loadSaveData(save);
      await g.loadWorld(world, (label, p) => ui.showProgress(label, 0.7 + p * 0.3));
      g.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
      g.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
      g.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
      g.player.inv.add(ITEM_BY_KEY['torch'], 20);
      ui.toast(Lang.text('Mods.SandboxWorld.Toast.WldImported', save.header.name ?? '', save.header.wldVersion ?? 0));
      // 登记世界槽位并持久化：导入不再是一次性的，重进游戏可在世界列表中看到并继续游玩
      await worldStore.ensureLoaded();
      const names = new Set(worldStore.list().map((m) => m.name));
      let name = save.header.name;
      if (names.has(name)) {
        let i = 2;
        while (names.has(`${name} (${i})`)) i++;
        name = `${name} (${i})`;
      }
      currentWorld = await worldStore.register({
        name, seed: seedText || String(save.header.seed),

```


---

## 👤 User(sidechain) · 2026-08-12T15:55:05.939Z

**📎 ToolResult**

```
  drop(inv.miscEquips);
  drop(inv.miscDyes);
  for (const l of inv.loadouts) { drop(l.armor); drop(l.dye); }  // EquipmentLoadout.TryDroppingItems
  inv.slots.fill(null);
  inv.armor.fill(null);
  inv.dye.fill(null);
  inv.miscEquips.fill(null);
  inv.miscDyes.fill(null);
  for (const l of inv.loadouts) { l.armor.fill(null); l.dye.fill(null); }
  // 发还铜制起始三件套（原版 1:1 顺序：[0]短剑 3507 / [1]镐 3509 / [2]斧 3506）
  const starter = [VANILLA_ITEM_KEY_BY_ID[3507] ?? 'copper_sword',
    VANILLA_ITEM_KEY_BY_ID[3509] ?? 'copper_pickaxe', VANILLA_ITEM_KEY_BY_ID[3506] ?? 'copper_axe'];
  starter.forEach((key, i) => {
    const id = ITEM_BY_KEY[key];
    if (id !== undefined) inv.slots[i] = { id, stack: 1 };
  });
}

export interface GameCallbacks {
  onWorldReady: () => void;
  onInventoryChanged: () => void;
        }
        if (st.wall[i] > 0) wallIds.add(st.wall[i]);
      }
    }
    // 兜底常驻:草/泥/石表全时有(暴露地表转草、autotile 邻接)
    for (const k of ['dirt', 'stone', 'grass']) {
      const vs = TILE_DEFS[TILE_BY_KEY[k]]?.vanilla?.sheet;
      if (vs !== undefined) tileSheets.add(vs);
    }
    return { tileSheets, wallIds };
  }

  /** 预载期的装备槽位(此时 player 尚未创建,读初始装备常量:afterWorldLoad 同源) */
  private playerPreviewArmor(): Array<number | null> {
    // 与 afterWorldLoad 初始装备一致:铁三件(头/胸/腿)
    const ids: Array<number | null> = [null, null, null];
    const order = ['iron_helmet', 'iron_chainmail', 'iron_greaves'];
    for (let k = 0; k < 3; k++) {
      const id = ITEM_BY_KEY[order[k]];
      ids[k] = id !== undefined ? id : null;
    }
    return ids;
  }

  /** 全图液体沉降（薄封装 → settleWorldLiquids，主线程 fallback 与 worker 共用同一实现）。
   *  mode 语义见 src/world/liquid/settle.ts 头注释 */
  private settleLiquids(onProgress?: (p: number) => void, mode: 'gen' | 'load' = 'gen') {
    return settleWorldLiquids(this.world, mode, onProgress);
  }

  async loadWorld(world: World, onProgress?: (label: string, p: number) => void, opts?: { settled?: boolean }) {
    // setTile 再次触发本监听器自然完成;生成/导入期 setTileSilent 不触发)
    this.sandQueue.length = 0;
    w.store.onTileChanged((x, y) => {
      const above = TILE_DEFS[w.store.type[w.store.idx(x, Math.max(0, y - 1))]];
      if (above && Game.FALLING_TILES.has(w.store.type[w.store.idx(x, Math.max(0, y - 1))])) {
        this.sandQueue.push([x, y - 1]);
      }
    });
    this.entities.clear();
    clearPortals();                 // 传送门为世界内实体，切世界/重载一并清（BirthdayParty.WorldClear 同位）
    partyWorldClear(this.partyState);
    LanternNight.worldClear();      // LanternNight.WorldClear（Main.cs:51656）：运行时态不进存档
    this.player = new Player(w.spawnX * TILE + 8, (w.spawnY - 3) * TILE, new Inventory()); // 主角 3 格高，抬高出生点
    // 初始装备 = 原版经典开局三件套（铜镐/铜斧/铜剑），其余一概不给——
    // 调试用道具经背包面板的"搜索添加"按钮获取（UI.ts 道具搜索器）
    this.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
    this.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
    this.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
    this.camera.x = this.player.cx;
    this.camera.y = this.player.cy;
    this.boss = null;
    // ---- 历史存档索引帧修复 ----
    // 旧版生成代码曾把多格家具的格内偏移写成【格索引】(0/1)而非【像素】(0/18)，
    // 渲染端 ofx=1 只偏 1px → 2×2 宝箱四格显示同一贴图。特征：多格 vanilla framed
    // 物体的全部格帧 <18 且非全 0（合法块必有一格 ≥18；全 0 由渲染端锚点扫描重建）
    this.repairIndexFrames();

    // ---- 城镇 NPC 恢复（原版 WorldFile 加载：存档里的 town NPC 原位生成）----
    const savedNpcs = this.world.pendingTownNpcs ?? [];
    this.world.pendingTownNpcs = [];
    this.guideSpawned = true;

```


---

## 🤖 Assistant · 2026-08-12T15:55:11.363Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now UI.ts dev item search list — check if there's a list of local keys for the "search add" panel. Grep UI.ts for arrays of keys.

Also check UI.ts 2410-2500 buff icon maps (uses local keys as icons via ITEM_BY_KEY presumably).

Let me read UI.ts 2400-2430 and check how those keys are consumed.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:55:11.698Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2400,2430p;2470,2510p' src/ui/UI.ts",
 "description": "Read UI buff icon maps"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:11.736Z

**📎 ToolResult**

```
    this.chatMonitor?.clear();
    this.chatMonitor = new ChatMonitor(this.root, () => UISfx.sfx.play('menuTick', 0.6));
    // 回放进世界前缓冲的消息(如新世界出生时的 NPC 入驻公告)
    for (const [t, r, g, b, width] of this.chatPending) this.chatMonitor.message(t, r, g, b, width);
    this.chatPending = [];

    this.buildInventoryPanel();
    this.buildChestPanel();
    this.buildBuffBar();
    this.buildHud(this.game);
    // Buff → 图标物品映射
    const map: Array<[BuffType, string]> = [
      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
      // 环境 debuff(原版用专属 buff 贴图,此处以近义物品图标近似)
      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
      [BuffType.Bleeding, 'lesser_healing_potion'], [BuffType.Suffocation, 'sand_block'],
      [BuffType.ObsidianSkin, 'obsidian_skin_potion'], [BuffType.Gills, 'gills_potion'],
      [BuffType.ManaRegen, 'mana_regen_potion'], [BuffType.MagicPower, 'magic_power_potion'],
      [BuffType.Featherfall, 'featherfall_potion'], [BuffType.WaterWalking, 'water_walking_potion'],
      [BuffType.Archery, 'archery_potion'], [BuffType.NightOwl, 'night_owl_potion'],
      // R1 数值批（vi_ 药水物品图标）
      [BuffType.Battle, 'vi_300_BattlePotion'], [BuffType.Calming, 'vi_2324_CalmingPotion'],
      [BuffType.Mining, 'vi_2322_MiningPotion'], [BuffType.Builder, 'vi_2325_BuilderPotion'],
      [BuffType.Heartreach, 'vi_2323_HeartreachPotion'], [BuffType.FlipperPotion, 'vi_2327_FlipperPotion'],
      [BuffType.Titan, 'vi_2326_TitanPotion'], [BuffType.AmmoReservation, 'vi_2344_AmmoReservationPotion'],
      [BuffType.Lifeforce, 'vi_2345_LifeforcePotion'], [BuffType.Endurance, 'vi_2346_EndurancePotion'],
      [BuffType.Wrath, 'vi_2349_WrathPotion'], [BuffType.Rage, 'vi_2347_RagePotion'],
      [BuffType.Tipsy, 'vi_2266_Sake'],
      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
  }

  showNpcShop(title: string, items: Array<{ key: string; vanillaId: number; name: string; price: number }>, copper: number): void {
    if (!this.npcShop) {
      this.npcShop = new NpcShop(this.root,
        (vid) => this.game?.npcShopBuy(vid),
        () => { this.npcShop?.close(); this.npcShop = null; });
    }
    // 图标由 UI 侧按原版 id 补(atlas 管线)
    const entries: ShopEntry[] = items.map((it) => ({
      ...it,
      iconUrl: this.game ? iconUrl(this.game, it.vanillaId) || '' : '',
    }));
    this.npcShop.open(title, entries, copper);
  }

  /** M5：背包/快捷栏已 Canvas 化，DOM 仅保留 Buff 栏 + Toast */
  initInGameLite() {
    this.buildBuffBar();
    const map: Array<[BuffType, string]> = [
      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
      [BuffType.Bleeding, 'lesser_healing_potion'], [BuffType.Suffocation, 'sand_block'],
      [BuffType.ObsidianSkin, 'obsidian_skin_potion'], [BuffType.Gills, 'gills_potion'],
      [BuffType.ManaRegen, 'mana_regen_potion'], [BuffType.MagicPower, 'magic_power_potion'],
      [BuffType.Featherfall, 'featherfall_potion'], [BuffType.WaterWalking, 'water_walking_potion'],
      [BuffType.Archery, 'archery_potion'], [BuffType.NightOwl, 'night_owl_potion'],
      // R1 数值批（vi_ 药水物品图标）
      [BuffType.Battle, 'vi_300_BattlePotion'], [BuffType.Calming, 'vi_2324_CalmingPotion'],
      [BuffType.Mining, 'vi_2322_MiningPotion'], [BuffType.Builder, 'vi_2325_BuilderPotion'],
      [BuffType.Heartreach, 'vi_2323_HeartreachPotion'], [BuffType.FlipperPotion, 'vi_2327_FlipperPotion'],
      [BuffType.Titan, 'vi_2326_TitanPotion'], [BuffType.AmmoReservation, 'vi_2344_AmmoReservationPotion'],
      [BuffType.Lifeforce, 'vi_2345_LifeforcePotion'], [BuffType.Endurance, 'vi_2346_EndurancePotion'],
      [BuffType.Wrath, 'vi_2349_WrathPotion'], [BuffType.Rage, 'vi_2347_RagePotion'],
      [BuffType.Tipsy, 'vi_2266_Sake'],
      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
      [BuffType.MoonLeech, 'vi_1569_vampire_knives'], [BuffType.Obstructed, 'vi_329_shadow_key'],
      // 食物三档（以已注册食物贴图为图标近似）
      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],

```


---

## 🤖 Assistant · 2026-08-12T15:55:12.994Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"COIN_KEYS\" src --include=\"*.ts\"; echo ===; grep -n \"COIN_KEYS\\|coinAccepts\\|isCoin\" src/items/Inventory.ts | head",
 "description": "Find COIN_KEYS consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:13.048Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
src/items/Inventory.ts:39:export const COIN_KEYS = ['coin_copper', 'coin_silver', 'coin_gold', 'coin_platinum'] as const;
src/items/Inventory.ts:63:  return id === ITEM_BY_KEY[COIN_KEYS[i - COIN_START]];
src/items/Inventory.ts:97:  return COIN_KEYS.findIndex((k) => ITEM_BY_KEY[k] === id);
src/items/Inventory.ts:274:      if (s && s.id === ITEM_BY_KEY[COIN_KEYS[tier]] && s.stack >= 100) {
src/items/Inventory.ts:277:        const left = this.add(ITEM_BY_KEY[COIN_KEYS[tier + 1]], 1);
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T15:55:21.195Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have most. A few remaining checks:

1. SmartCursor references: lines 1216, 1493, 1523 (done).
2. Renderer.ts:3131 torch special case (done - line 3131).
3. Game.ts:3084-3092 torch/candle light (check quickly).
4. World.Torch.ts:88-94 'torch' key (tile key context — torchStyleOfItemKey uses item key 'torch').
5. Also check UI item search panel: does it enumerate ITEM_DEFS (all items)? Probably yes, no local key list.
6. Check world/Housing.ts:41 'workbench' tile key (tile side, no migration).
7. Check `Torch.ts` torchStyleOfItemKey — key === 'torch' item key check.

Also check Game.ts 2558-2585 water_candle / lantern; those are def.key === 'water_candle' (item) and TILE_BY_KEY (tile).

Also check whether there's a debug/dev panel with local keys (src/debug, src/dev).

Let me grep src/dev and src/debug.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:55:22.308Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls src/dev src/debug 2>/dev/null; grep -rnE \"['\\\"\\`](wood|gel|torch|copper_bar|iron_bar|coin_copper|wood_pickaxe)['\\\"\\`]\" src/dev src/debug src/vui 2>/dev/null | head",
 "description": "Check dev/debug/vui for local keys"
}
```


---

## 🤖 Assistant · 2026-08-12T15:55:22.621Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '80,100p' src/world/Torch.ts; echo \"=== Game 3075-3100\"; sed -n '3070,3100p' src/core/Game.ts; echo \"=== Renderer 3125-3140\"; sed -n '3125,3140p' src/render/Renderer.ts",
 "description": "Read torch key handling"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:36.236Z

**📎 ToolResult**

```
src/debug:
DebugReport.ts

src/dev:
PixelArtImport.ts

```


---

## 👤 User(sidechain) · 2026-08-12T15:55:36.290Z

**📎 ToolResult**

```
/** 该火把 tile（frameY）是否水炬样式——液体冲毁豁免/水中放置门 */
export function isWaterTorchStyle(frameY: number): boolean {
  return WATER_TORCH_STYLES.has(Math.floor(frameY / 22));
}

/** 物品 key → 放置火把样式 torchId（Item.cs SetDefaults placeStyle + 生物群系火把显式表）。
 *  彩色火把 427-433 = id-426（1-7）；群系火把 BIOME 表；水炬 = 8（咒火 523）/11（灵液 1333）
 *  /17（珊瑚 4384）；legacy 'torch' 与其余 → 0 */
const BIOME_TORCH_ITEM: Record<number, number> = {
  523: 8, 974: 9, 1245: 10, 1333: 11, 2274: 12, 3004: 13, 3045: 14, 3114: 15,
  4383: 16, 4384: 17, 4385: 18, 4386: 19, 4387: 20, 4388: 21, 5293: 22, 5353: 23,
};
export function torchStyleOfItemKey(key: string): number {
  if (key === 'torch') return 0;
  const m = /^vi_(\d+)_/.exec(key);
  if (!m) return 0;
  const id = Number(m[1]);
  if (id >= 427 && id <= 433) return id - 426;
  return BIOME_TORCH_ITEM[id] ?? 0;
}
=== Game 3075-3100
        Math.floor((pe.x + pe.w / 2) / TILE), Math.floor((pe.y + pe.h / 2) / TILE),
        l * rgb[0], l * rgb[1], l * rgb[2],
      );
    }
    // 掉落物点光（WorldItem.UpdateItem_VisualEffects :1467-1471 + :1455-1461 + :1684-1703）：
    // createTile==4 火把族 → TorchColor；蜡烛(105) → [1,0.95,0.8]；均 !wet。
    // 荧光棒族（282/286/3002）：水中也发光（原版分支无 !wet 门控）
    for (const dent of this.entities.drops) {
      const d = dent as ItemDrop;
      const def = ITEM_DEFS[d.itemId];
      if (!def) continue;
      const tx = Math.floor((d.x + d.w / 2) / TILE), ty = Math.floor((d.y + d.h / 2) / TILE);
      const dst = this.world.store;
      if (!dst.inBounds(tx, ty)) continue;
      const isTorch = def.tile === 'torch';
      const isCandle = def.tile === 'candle';
      if (isTorch || isCandle) {
        if (dst.liquid[dst.idx(tx, ty)] > 100) continue; // !wet
        this.lighting.addLight(tx, ty, 1, 0.95, 0.8);
        continue;
      }
      // 荧光棒族（vi id → 原版色；无 wet 门控）
      const vid = viIdFromKey(def.key);
      if (vid === 282) this.lighting.addLight(tx, ty, 0.7, 1, 0.8);
      else if (vid === 286) this.lighting.addLight(tx, ty, 0.7, 0.8, 1);
      else if (vid === 3002) this.lighting.addLight(tx, ty, 1.05, 0.95, 0.55);
      else if (vid === 75) this.lighting.addLight(tx, ty, 0.8, 0.7, 0.1);      // 坠落之星 :1719
      else if (vid === 183) this.lighting.addLight(tx, ty, 0.15, 0.45, 0.9);   // 陨石锭 :1715
    }
    // 实体点光（原版 Lighting.AddLight 的 NPC 侧调用）：AI 每 tick 写 lightRGB——
    // 萤火虫族闪烁（NPC.cs:34395-34407，昼地表不亮）、发光蜗牛/熔岩蜗牛恒定（:34623-34630）、
=== Renderer 3125-3140
    // HOLD_STYLE_ITEMS 手工补）；7 无持位分支（仅 bodyFrame 行 11）不画
    let staticHoldStyle = 0;
    if (!swing) {
      const held = p.inv.heldItem();
      const def = held ? ITEM_DEFS[held.id] : undefined;
      if (held && def && !p.inWater) {
        const vid = def.key === 'torch' ? 8 : viIdFromKey(def.key);
        const hs = vid >= 0 ? itemFuncOfVid(vid)?.holdStyle ?? (HOLD_STYLE_ITEMS.has(vid) ? 1 : 0) : 0;
        staticHoldStyle = hs === 7 ? 0 : hs;
        if (staticHoldStyle) {
          const ar = this.atlasIcon(held.id);
          const icon = ar ? null : this.itemIcon(held.id);
          if (ar || icon) {
            const fw = ar ? ar.sw : 14, fh = ar ? ar.sh : 14;
            // 持位（ApplyHoldStyle dir=1 空间；offX 正=身前，offY 从 p.y 起算）：
            //  1 默认 = (fw/2+2, 24)（:49720）；2 雨伞 = (-16, 22)（:49764）、

```


---

## 🤖 Assistant · 2026-08-12T15:55:46.467Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
A few last checks:
- src/ui/UI.ts item search panel (addItem search) — does it filter local keys? Not crucial.
- src/drops/NpcDrops.ts — how drops map vid → key (NATIVE_DROP_KEY used in Enemy.ts). Fine.
- Check `World.breakTileAt` fallback for drop wiring (items.ts comment mentions "掉落连线在读取端回退(World.breakTileAt)"). tile drop keys are item keys — those in tiles.ts `drop:` fields are local keys for many tiles. That's a big one for category 1! tiles.ts drop: 'dirt_block' etc. I captured those in the grep group 2 (src/data/tiles.ts lines 49-148). Good.
- Check Housing.ts:41 (tile key — no migration).
- Check tools/ test files (tools/_*.test.ts) for local keys — my grep of tools returned nothing? The grep -rl included tools; no tools files appeared. Let me double check tools/*.test.ts reference ITEM_BY_KEY.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:55:47.396Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ITEM_BY_KEY\\|ITEM_DEFS\\|RECIPES\" tools/*.ts tools/*.mjs 2>/dev/null | grep -v \"vi_\" | head -20; echo \"=== scripts\"; ls scripts | head; grep -rln \"ITEM_BY_KEY\\|'wood'\\|'gel'\" scripts 2>/dev/null | head",
 "description": "Check tools and scripts for local keys"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:47.465Z

**📎 ToolResult**

```
tools/migrate-save.mjs:3:// 原理:存档写入时的 TILE_DEFS/ITEM_DEFS 顺序可从 git 历史恢复
=== scripts
_alphaprobe.mjs
_amber-ascii.mjs
_amber-pixel.mjs
_amber-tree-audit.mjs
_ascii-frame.mjs
_audit7.mjs
_ballooncheck.mjs
_batprobe.mjs
_beach-probe.mjs
_behavior-smoke.mjs
scripts/probe.mjs
scripts/_smart-cursor-probe.mjs
scripts/buffs.mjs
scripts/_craftdupprobe.mjs
scripts/feat-test3.mjs
scripts/_lootprobe.mjs
scripts/_p5-smoke.mjs
scripts/liquidlab.ts
scripts/_weap-probe.mts
scripts/item-audit.ts

```


---

## 🤖 Assistant · 2026-08-12T15:55:48.200Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"def.drop\\|drop ?? \\|\\.drop\\b\" src/world/World.ts | head -20; echo \"=== breakTileAt\"; sed -n \"$(grep -n 'breakTileAt' src/world/World.ts | head -1 | cut -d: -f1),+40p\" src/world/World.ts",
 "description": "Read World.breakTileAt drop wiring"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:52.413Z

**📎 ToolResult**

```
src/world/World.ts:256:    return d.drop === undefined ? (d.key.startsWith('v_') ? 'place_' + d.key : null) : d.drop;
=== breakTileAt
  breakTileAt(x: number, y: number): string | null {
    const t = this.store.get(x, y);
    if (t === 0) return null;
    const d = TILE_DEFS[t];
    this.store.setTile(x, y, 0);
    // v_ 图块无显式 drop → 回退同名放置物品(阶段5 自动注册)。
    // drop:null = 显式无掉落(原版装饰类)——?? 会把 null 也走兜底,必须显式判 undefined
    return d.drop === undefined ? (d.key.startsWith('v_') ? 'place_' + d.key : null) : d.drop;
  }

  isSolidPx(px: number, py: number): boolean {
    return this.store.isSolid(Math.floor(px / 16), Math.floor(py / 16));
  }

  /** 液体量（0-255）按像素坐标 */
  liquidAt(px: number, py: number): number {
    return this.store.liquid[this.store.idx(Math.floor(px / 16), Math.floor(py / 16))];
  }

  registerTree(x: number, y: number, h: number) {
    this.trees.push({ x, y, h });
  }
}

export { T };

```


---

## 🤖 Assistant · 2026-08-12T15:55:56.014Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
tools/migrate-save.mjs — save migration tool (relevant precedent for id migration). Let me look at it briefly. And scripts/item-audit.ts maybe references local keys.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:55:56.215Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1,60p' tools/migrate-save.mjs",
 "description": "Read migrate-save tool"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:56.247Z

**📎 ToolResult**

```
#!/usr/bin/env node
// 旧存档(v1/v2,内部下标 id)→ v3 稳定 id 迁移工具。
// 原理:存档写入时的 TILE_DEFS/ITEM_DEFS 顺序可从 git 历史恢复
//   (header.created 时间戳 → 该时刻的最后一个 commit → git show 提取 def/item 注册顺序),
//   旧下标 → 当时 key → 当前稳定 id(sheet/私有段),重写 tiles/chests/inventory/banks。
// 用法:
//   node tools/migrate-save.mjs <save.json> [out.json] [--ref <git-ref>]
//   不给 --ref 时按 header.created 自动选(ref=该时间前最后一个 commit;工作区未提交的
//   改动用 --ref HEAD 近似——本次漂移源正是未提交插入,HEAD 顺序=存档写入时顺序)。
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

// ---- varint/RLE 编解码(与 src/save/serialize.ts 同格式) ----
function b64ToBytes(b64) {
  return Buffer.from(b64, 'base64');
}
function readVarint(u8, pos) {
  let v = 0, shift = 0;
  while (pos.i < u8.length) {
    const b = u8[pos.i++];
    v += (b & 0x7f) * 2 ** shift;
    if (!(b & 0x80)) break;
    shift += 7;
  }
  return v;
}
class ByteWriter {
  buf = new Uint8Array(1 << 16);
  len = 0;
  grow(need) {
    if (this.len + need <= this.buf.length) return;
    let cap = this.buf.length;
    while (cap < this.len + need) cap *= 2;
    const nb = new Uint8Array(cap);
    nb.set(this.buf.subarray(0, this.len));
    this.buf = nb;
  }
  varint(v) {
    v = v < 0 ? 0 : v;
    this.grow(5);
    while (v >= 0x80) { this.buf[this.len++] = (v & 0x7f) | 0x80; v = Math.floor(v / 128); }
    this.buf[this.len++] = v;
  }
  bytes() { return this.buf.subarray(0, this.len); }
}
function bytesToB64(u8) { return Buffer.from(u8).toString('base64'); }

// ---- 从 git 历史提取注册顺序 ----
function keyOrderAtRef(ref, file, callRe) {
  const src = execSync(`git show ${ref}:src/data/${file}`, { cwd: process.cwd(), encoding: 'utf8', maxBuffer: 1 << 28 });
  const keys = [];
  for (const m of src.matchAll(callRe)) keys.push(m[1]);
  // 运行时循环注册的 vi_ 批量段无法从文本提取——由调用方用稳定表兜底(vi_ key 含 id 自解析)
  return keys;
}

// ---- 当前稳定 id 源(与 src/data/*.ts 同规则;直接解析当前文件,避免引入 TS 运行时) ----
function buildStableMaps() {
  // tiles:PRIV 表(文本提取) + def 的 vanilla.sheet
  const tilesSrc = readFileSync('src/data/tiles.ts', 'utf8');

```


---

## 🤖 Assistant · 2026-08-12T15:55:56.901Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"['\\\"](wood|gel|torch|copper_bar|iron_bar|coin_copper|wood_pickaxe|copper_pickaxe|iron_sword)[ '\\\"]\" scripts/item-audit.ts scripts/_craftdupprobe.mjs scripts/buffs.mjs 2>/dev/null | head -20",
 "description": "Check scripts for local keys"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:55:56.932Z

**📎 ToolResult**

```
scripts/_craftdupprobe.mjs:21:  const wood = window.__swItems['wood'];

```


---

## 🤖 Assistant · 2026-08-12T15:56:00.355Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have enough for the report. Let me do a final sweep for any remaining local key references I might have missed in src: grep for 'wood'/'gel' etc. in files I haven't covered: src/stats, src/lighting, src/physics, src/render (done), src/vui, src/workers, src/wld (done). Also check src/ui/UI.ts full list of local keys — I got the buff maps. Also check src/player for local keys.

Let me do one final comprehensive grep across src excluding files already known, for the top local keys to be safe.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:56:03.135Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rnE \"['\\\"\\`](wood|gel|copper_bar|iron_bar|silver_bar|gold_bar|lens|torch|platform|door|workbench|furnace|anvil|chest|coin_copper|coin_silver|coin_gold|coin_platinum|wood_pickaxe|copper_pickaxe|iron_pickaxe|iron_sword|wooden_arrow|wooden_bow|iron_bow|flaming_arrow|life_crystal|suspicious_eye|lucky_horseshoe|feral_claws|acorn|rope|bomb|wire|minecart_item|wand_of_sparking|amethyst_bolt|empty_bucket|water_bucket|lava_bucket|honey_bucket|worm_food|bloody_spine|slime_crown|mechanical_worm|mechanical_eye|mechanical_skull|actuator_item|wire_cutter|multicolor_wrench|grand_design|goblin_battle_standard|snow_globe|pirate_map|tin_bar|lead_bar|tungsten_bar|platinum_bar|copper_ore|iron_ore|silver_ore|gold_ore|dirt_block|stone_block|sand_block|snow_block|mushroom_item|lesser_healing_potion|heal_potion|agility_potion|ironskin_potion|thorns_potion|regen_potion)['\\\"\\`]\" src/stats src/lighting src/physics src/vui src/workers src/player src/entities src/world 2>/dev/null | grep -v \"TILE_BY_KEY\\|TILE_DEFS\\|def({ key\" | head -40",
 "description": "Final sweep for local keys in remaining dirs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:56:12.048Z

**📎 ToolResult**

```
src/physics/LineOfSight.ts:18:type Store = Pick<TileStore, 'w' | 'h' | 'type' | 'wire' | 'half' | 'slope' | 'inBounds' | 'idx'>;
src/player/SmartCursor.ts:1216:    const isTorch = (vid != null && TORCH_ITEMS.has(vid)) || sem.createTileSheet === 4 || env.held.def?.key === 'torch';
src/player/SmartCursor.ts:1493:    const isBucket = vid === 205 || env.held.def?.key === 'empty_bucket';
src/player/SmartCursor.ts:1523:    const isActuatorItem = sem.vid === 849 || env.held.def?.key === 'actuator_item';
src/entities/ItemDrop.ts:85:          game.playSfx(ITEM_DEFS[this.itemId]?.key === 'coin_copper' ? 'coin' : 'pickup', 0.75);
src/entities/Enemy.ts:59:  71: 'coin_copper', 72: 'coin_silver', 73: 'coin_gold', 74: 'coin_platinum',
src/entities/Enemy.ts:60:  23: 'gel', 8: 'torch', 236: 'lens', 3: 'stone_block', 2: 'dirt_block', 9: 'wood',
src/entities/Enemy.ts:61:  28: 'lesser_healing_potion',
src/entities/Player.ts:186:      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
src/entities/Player.ts:193:      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
src/world/Door.ts:141:  sfx?.('door'); // SoundID 8
src/world/Torch.ts:88: *  /17（珊瑚 4384）；legacy 'torch' 与其余 → 0 */
src/world/Torch.ts:94:  if (key === 'torch') return 0;
src/world/Housing.ts:41:  return key.includes('table') || key === 'workbench' || sheet === 14 || sheet === 18;
src/world/Extractinator.ts:72:  71: 'coin_copper', 72: 'coin_silver', 73: 'coin_gold', 74: 'coin_platinum',
src/world/gen/vanilla/CaveHousePass.ts:21:type Theme = 'wood' | 'ice' | 'jungle' | 'desert' | 'granite' | 'marble' | 'mushroom';
src/world/gen/vanilla/CaveHousePass.ts:141:    ['wood', count(SC0) + count(SC1)],
src/world/gen/vanilla/CaveHousePass.ts:265:  if (theme === 'wood') {
src/world/gen/vanilla/CaveHousePass.ts:416:    ['anvil', 0],
src/world/gen/vanilla/CaveHousePass.ts:417:    ['workbench', def.workbench],
src/world/gen/vanilla/MicroBiomesPass.ts:90:  return key.includes('chest') || key.includes('dresser');
src/world/gen/vanilla/MicroBiomesPass.ts:258:        if (key.includes('chest') || key.includes('dresser')) return false; // IsAContainer 近似

```


---

## 🤖 Assistant · 2026-08-12T15:56:19.160Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
One more: CaveHousePass lines 415-421 — those are tile keys passed to placeFurniture (tile keys, not item). Confirmed by line 437 `placeFurniture(st, 'candelabra', ...)` which is tile-based.

Also check the accessory field values 'lucky_horseshoe'/'feral_claws' — these are ItemDef.accessory enum values, tied to local defs. If local defs deleted, Player.ts:186/193 checks die; vi_158/vi_211 have equip stats via vanillaItemStats (acc:1) — but the special effects (no fall damage, melee speed) are implemented via `accessory` field only. Check Player.ts around 180-200 to see.

Also check equipStats for these — grep 'lucky_horseshoe' in stats/. Already did: only items.ts and Player.ts.

Let me check Player.ts 180-200 quickly and how equipStats handles vi_ equivalents.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:56:19.163Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '175,205p' src/entities/Player.ts; echo \"=== equipStats accessory\"; grep -rn \"lucky\\|feral\\|noFallDmg\\|meleeSpeed\" src/stats/*.ts src/entities/Player.ts | head -15",
 "description": "Read accessory effect checks"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:56:19.243Z

**📎 ToolResult**

```
  constructor(x: number, y: number, inv: Inventory) {
    super();
    this.x = x; this.y = y;
    this.inv = inv;
  }

  // ---- 配饰效果（重算式聚合，幂等）----
  get hasHorseshoe(): boolean {
    for (let i = ACC_ARMOR_START; i < ACC_ARMOR_START + 7; i++) { // armor[3-9] 配饰槽（原版 Player.cs:36326）
      const s = this.inv.armor[i];
      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
    }
    return false;
  }
  get hasFeralClaws(): boolean {
    for (let i = ACC_ARMOR_START; i < ACC_ARMOR_START + 7; i++) {
      const s = this.inv.armor[i];
      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
    }
    return false;
  }
  /** 防御 = 基础(0) + 盔甲/配饰（含 vi_ 表防御+accfx def+词缀 62-65）+ 铁皮 Buff(+6)（时装不计） */
  get defense(): number {
    let d = this.buffs.defenseBonus + this.equipStats.def;
    for (const id of this.inv.equippedArmor()) {
      if (id != null) d += ITEM_DEFS[id]?.armor?.defense ?? statOfInternal(id)?.def ?? 0;
    }
    return d;
  }

=== equipStats accessory
src/stats/Luck.ts:181:// 窗口：玩家 Center tile ±40（81×81）。原版每 tick 只扫一行（luckyTorchCounter 逐行推进），
src/stats/Buffs.ts:395:  /** 近战速度 +5/7.5/10%（meleeSpeed += ,:11528+） */
src/entities/Player.ts:186:      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
src/entities/Player.ts:193:      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
src/entities/Player.ts:213:    moveMult: number; meleeSpeed: number;
src/entities/Player.ts:218:    noKnockback: boolean; noFallDmg: boolean; desertBoots: boolean;
src/entities/Player.ts:224:    treasureMagnet: boolean; goldRing: boolean; luckyCoin: boolean; discount: boolean;
src/entities/Player.ts:264:    let move = 0, meleeSpeed = 0, runSpeed = 0;
src/entities/Player.ts:268:    let autoJump = false, fireWalk = false, noKnockback = false, noFallDmg = false;
src/entities/Player.ts:281:    let treasureMagnet = false, goldRing = false, luckyCoin = false, discount = false;
src/entities/Player.ts:309:        if (fx.meleeSpd) meleeSpeed += fx.meleeSpd;
src/entities/Player.ts:326:        if (fx.noFallDmg) noFallDmg = true;
src/entities/Player.ts:347:        if (fx.luckyCoin) luckyCoin = true;
src/entities/Player.ts:379:        else meleeSpeed += (p - 76) / 100;        // 77-80：+1..4% 近战速度
src/entities/Player.ts:432:      if (sb.meleeSpd) meleeSpeed += sb.meleeSpd;

```


---

## 🤖 Assistant · 2026-08-12T15:56:23.480Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — vi_ accessories get effects via vanillaAccFx (fx.noFallDmg etc.), so vi_158_lucky_horseshoe and vi_211_feral_claws already have data-driven equivalents. The local accessory field is a legacy parallel path.

Now I have everything needed. Let me also quickly verify the count of "172 local items" and list keys not covered by VANILLA_ITEM_ICON_MAP (icons missing for some local keys). Local keys in PRIV minus those in icon map: e.g. 'wood_sword' is in map... Let me compute which local keys lack icon map entries (they'd fall back to procedural ItemIconGen). Quick check with node? That'd be read-only compute, fine.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:56:26.044Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst fs=require('fs');\nconst src=fs.readFileSync('src/data/items.ts','utf8');\nconst m=src.match(/const PRIV_ITEM_STABLE[\\s\\S]*?\\n\\};/)[0];\nconst keys=[...m.matchAll(/'([a-z0-9_]+)':\\s*\\d+/g)].map(x=>x[1]).filter(k=>!k.startsWith('place_v_'));\nconst atlas=fs.readFileSync('src/assets/SpriteAtlas.ts','utf8');\nconst mapSec=atlas.match(/export const VANILLA_ITEM_ICON_MAP[\\s\\S]*?\\n\\};/)[0];\nconst mapped=new Set([...mapSec.matchAll(/^\\s*([a-z0-9_]+):\\s*\\d+/gm)].map(x=>x[1]));\nconsole.log('local keys:',keys.length);\nconsole.log('no icon map entry:',keys.filter(k=>!mapped.has(k)).join(', '));\nconst items=src.slice(0,src.indexOf('PRIV_ITEM_STABLE'));\nconst noVid=keys.filter(k=>!new RegExp(\\\"key: '\\\"+k+\\\"'[^)]*vid\\\").test(items.replace(/\\n/g,' ')));\n\"",
 "description": "Count local keys and icon map gaps"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:56:31.985Z

**📎 ToolResult**

```
local keys: 184
no icon map entry: stone_block, sand_block, snow_block, torch, door, workbench, furnace, anvil, chest, gel, acorn, iron_ore, silver_ore, gold_ore, iron_bar, silver_bar, gold_bar, suspicious_eye, coin_copper, coin_gold, agility_potion, ironskin_potion, regen_potion, feral_claws, iron_helmet, iron_chainmail, iron_greaves, silver_helmet, silver_chainmail, silver_greaves, gold_helmet, gold_chainmail, gold_greaves, wood_axe, wood_hammer, copper_axe, copper_sword, copper_hammer, iron_axe, iron_hammer, silver_pickaxe, silver_axe, gold_pickaxe, gold_axe, gold_sword, gold_hammer, lead_ore, tungsten_ore, platinum_ore, lead_bar, tungsten_bar, platinum_bar, meteorite, hellstone, cobalt_ore, mythril_ore, adamantite_ore, orichalcum_ore, titanium_ore, chlorophyte_ore, ruby, emerald, topaz, amethyst, diamond, ice_brick, snow_brick, hardened_sand_block, desert_fossil, glass, obsidian, gray_brick, red_brick, silt_block, chair, bed, bookcase, grandfather_clock, dresser, bench, bathtub, keg, cooking_pot, tombstone, life_crystal, chandelier, lantern, candelabra, skull_lantern, water_candle, rope, crimson_grass_seeds, mushroom_grass_seeds, water_bucket, lava_bucket, honey_bucket, tin_axe, tin_sword, lead_axe, lead_sword, tungsten_axe, tungsten_sword, platinum_axe, platinum_sword, wooden_arrow, flaming_arrow, iron_bow, wand_of_sparking, amethyst_bolt, bloody_spine, slime_crown, mechanical_worm, mechanical_eye, mechanical_skull, red_wrench, blue_wrench, green_wrench, yellow_wrench, actuator_item, actuation_rod, grand_design, goblin_battle_standard, snow_globe, pirate_map, coin_platinum, obsidian_skin_potion, gills_potion, mana_regen_potion, magic_power_potion, featherfall_potion, water_walking_potion, archery_potion, night_owl_potion

```


---

## 🤖 Assistant · 2026-08-12T15:56:35.358Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
My regex was multiline-broken (keys on shared lines like `dirt_block: 2, stone_block: 3` — only first key per line matched). The map uses multiple keys per line, so my `^\s*key:` only catches first. So "no icon map entry" list is inaccurate. Not critical — I'll note the icon map covers the local keys (multiline), and exact per-key coverage needs care. Let me redo properly by extracting all `word: number` pairs.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:56:36.845Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst fs=require('fs');\nconst src=fs.readFileSync('src/data/items.ts','utf8');\nconst m=src.match(/const PRIV_ITEM_STABLE[\\s\\S]*?\\n\\};/)[0];\nconst keys=[...m.matchAll(/'([a-z0-9_]+)':\\s*\\d+/g)].map(x=>x[1]).filter(k=>!k.startsWith('place_v_'));\nconst atlas=fs.readFileSync('src/assets/SpriteAtlas.ts','utf8');\nconst mapSec=atlas.match(/export const VANILLA_ITEM_ICON_MAP[\\s\\S]*?\\n\\};/)[0];\nconst mapped=new Set([...mapSec.matchAll(/([a-z0-9_]+)\\s*:\\s*\\d+/g)].map(x=>x[1]));\nconsole.log('local keys:',keys.length,'mapped:',keys.filter(k=>mapped.has(k)).length);\nconsole.log('NOT in icon map:',keys.filter(k=>!mapped.has(k)).join(', ')||'(none)');\n\"",
 "description": "Recheck icon map coverage per key"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:56:47.969Z

**📎 ToolResult**

```
local keys: 184 mapped: 169
NOT in icon map: mechanical_worm, mechanical_eye, mechanical_skull, goblin_battle_standard, snow_globe, pirate_map, coin_platinum, obsidian_skin_potion, gills_potion, mana_regen_potion, magic_power_potion, featherfall_potion, water_walking_potion, archery_potion, night_owl_potion

```


---

## 🤖 Assistant · 2026-08-12T15:56:51.242Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
184 non-place_v_ keys in PRIV table (user said 172; close enough — includes buckets/seeds etc.).

15 keys without atlas icon → they fall back to procedural ItemIconGen (assets.itemIcons) — check ItemIconGen covers them (case 'mechanical_worm' etc.). ItemIconGen has a switch on key with cases for gel/mushroom_item/lens/suspicious_eye/lesser_healing_potion/coin_copper... let me check its switch for those 15.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:56:51.709Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case '\" src/assets/ItemIconGen.ts | head -60; echo \"=== default branch\"; sed -n '280,300p' src/assets/ItemIconGen.ts",
 "description": "Read ItemIconGen cases"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:56:51.760Z

**📎 ToolResult**

```
37:    case 'dirt': return MATS.dirt;
38:    case 'stone': return MATS.stone;
39:    case 'sand': return MATS.sand;
40:    case 'snow': return MATS.snow;
41:    case 'wood': return MATS.wood;
42:    case 'platform': return MATS.wood;
229:    case 'gel':
237:    case 'mushroom_item':
244:    case 'lens':
252:    case 'suspicious_eye':
261:    case 'lesser_healing_potion':
270:    case 'coin_copper':
=== default branch
    for (let x = 3; x <= 12; x++) for (let y = 3; y <= 12; y++) s(x, y, '#777');
  });
}

export function generateAllItemIcons(): Map<number, HTMLCanvasElement> {
  const map = new Map<number, HTMLCanvasElement>();
  for (const def of ITEM_DEFS) {
    map.set(ITEM_BY_KEY[def.key], genItemIcon(def.key));
  }
  return map;
}

```


---

## 🤖 Assistant · 2026-08-12T15:56:53.649Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '160,280p' src/assets/ItemIconGen.ts",
 "description": "Read genItemIcon switch"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:56:53.684Z

**📎 ToolResult**

```
}

import type { Mat } from './Palette';

function genItemIcon(key: string): HTMLCanvasElement {
  const def = ITEM_DEFS[ITEM_BY_KEY[key]];
  const metals: Record<string, Mat> = {
    copper: MATS.copper, iron: MATS.iron, silver: MATS.silver, gold: MATS.gold,
  };
  // 方块类
  if (def.tile && ['dirt', 'stone', 'sand', 'snow', 'wood', 'platform'].includes(def.tile)) {
    return tileThumb(def.tile);
  }
  if (def.tile === 'torch') {
    return simple('#000', (s) => {
      for (let y = 7; y <= 14; y++) { s(7, y, MATS.wood.base); s(8, y, MATS.wood.dark); }
      s(7, 4, MATS.fire.light2); s(8, 4, MATS.fire.light2);
      s(6, 5, MATS.fire.light); s(7, 5, MATS.fire.base); s(8, 5, MATS.fire.base); s(9, 5, MATS.fire.light);
      s(7, 6, MATS.fire.dark); s(8, 6, MATS.fire.dark);
    });
  }
  if (def.tile === 'workbench') {
    return simple('#000', (s) => {
      for (let x = 1; x <= 14; x++) for (let y = 1; y <= 5; y++) s(x, y, y === 1 ? MATS.wood.light : MATS.wood.base);
      for (let y = 6; y <= 14; y++) { s(2, y, MATS.wood.dark); s(13, y, MATS.wood.dark); }
    });
  }
  if (def.tile === 'furnace') {
    return simple('#000', (s) => {
      for (let x = 1; x <= 14; x++) for (let y = 1; y <= 14; y++) s(x, y, (x === 1 || y === 1) ? MATS.stone.light : (x === 14 || y === 14) ? MATS.stone.dark : MATS.stone.base);
      for (let x = 5; x <= 10; x++) for (let y = 8; y <= 13; y++) s(x, y, y > 11 ? MATS.fire.light : MATS.fire.base);
    });
  }
  if (def.tile === 'anvil') {
    return simple('#000', (s) => {
      for (let x = 2; x <= 13; x++) { s(x, 3, MATS.metal.light2); s(x, 4, MATS.metal.base); }
      for (let y = 5; y <= 7; y++) for (let x = 6; x <= 9; x++) s(x, y, MATS.metal.dark);
      for (let x = 4; x <= 11; x++) { s(x, 8, MATS.metal.base); s(x, 9, MATS.metal.dark); }
    });
  }
  if (def.tile === 'chest') {
    return simple('#000', (s) => {
      for (let x = 2; x <= 13; x++) for (let y = 3; y <= 13; y++) s(x, y, y < 7 ? MATS.woodDark.light : MATS.woodDark.base);
      for (let x = 2; x <= 13; x++) s(x, 7, '#5A4520');
      s(7, 6, MATS.gold.light); s(8, 6, MATS.gold.light); s(7, 7, MATS.gold.base); s(8, 7, MATS.gold.base); s(7, 8, MATS.gold.dark); s(8, 8, MATS.gold.dark);
      for (let y = 3; y <= 13; y++) { s(2, y, MATS.gold.dark); s(13, y, MATS.gold.dark); }
    });
  }
  if (def.tile === 'door') {
    return simple('#000', (s) => {
      for (let x = 3; x <= 12; x++) for (let y = 1; y <= 14; y++) s(x, y, (x === 3 || x === 12 || y === 1 || y === 14) ? MATS.wood.dark : MATS.wood.base);
      s(7, 8, MATS.gold.light); s(8, 8, MATS.gold.light);
    });
  }
  // 工具
  if (def.tool && ['pick', 'axe', 'sword'].includes(def.tool.type)) {
    const tier = key.split('_')[0];
    const metal = metals[tier] ?? MATS.wood;
    return drawTool(def.tool.type as 'pick' | 'axe' | 'sword' | 'hammer', metal);
  }
  // 锭
  if (key.endsWith('_bar')) {
    return drawBar(metals[key.replace('_bar', '')] ?? MATS.iron);
  }
  // 矿石
  if (key.endsWith('_ore')) {
    return drawOreIcon(metals[key.replace('_ore', '')] ?? MATS.copper);
  }
  switch (key) {
    case 'gel':
      return simple('#000', (s) => {
        for (let x = 4; x <= 11; x++) for (let y = 6; y <= 12; y++) {
          if ((x === 4 || x === 11) && (y === 6 || y === 12)) continue;
          s(x, y, y === 6 ? '#8CE88C' : y === 12 ? '#3AA03A' : '#5FD35F');
        }
        s(6, 8, '#B0F5B0'); s(7, 8, '#B0F5B0');
      });
    case 'mushroom_item':
      return simple('#000', (s) => {
        for (let x = 5; x <= 10; x++) s(x, 9, '#E8DFC8');
        for (let x = 3; x <= 12; x++) s(x, 8, x < 5 || x > 10 ? MATS.copper.dark : MATS.copper.base);
        for (let x = 5; x <= 10; x++) s(x, 7, MATS.copper.light);
        s(5, 8, '#F0E8D8'); s(10, 7, '#F0E8D8');
      });
    case 'lens':
      return simple('#000', (s) => {
        for (let x = 4; x <= 11; x++) for (let y = 4; y <= 11; y++) {
          const dx = x - 7.5, dy = y - 7.5;
          if (dx * dx + dy * dy < 15) s(x, y, (dx < 0 && dy < 0) ? '#FFFFFF' : MATS.eye.base);
        }
        s(7, 7, '#202020'); s(8, 7, '#202020'); s(7, 8, '#202020'); s(8, 8, '#202020');
      });
    case 'suspicious_eye':
      return simple('#000', (s) => {
        for (let x = 2; x <= 13; x++) for (let y = 2; y <= 13; y++) {
          const dx = x - 7.5, dy = y - 7.5;
          if (dx * dx + dy * dy < 30) s(x, y, MATS.eye.base);
        }
        for (let x = 6; x <= 9; x++) for (let y = 5; y <= 10; y++) s(x, y, MATS.eyeRed.base);
        s(7, 7, '#101010'); s(8, 7, '#101010'); s(7, 8, '#101010'); s(8, 8, '#101010');
      });
    case 'lesser_healing_potion':
      return simple('#000', (s) => {
        for (let x = 6; x <= 9; x++) for (let y = 3; y <= 5; y++) s(x, y, '#9A8060');
        for (let x = 5; x <= 10; x++) for (let y = 6; y <= 13; y++) {
          if ((x === 5 || x === 10) && (y === 6 || y === 13)) continue;
          s(x, y, y < 9 ? '#E83050' : '#B01838');
        }
        s(6, 7, '#FF7088');
      });
    case 'coin_copper':
      return simple('#000', (s) => {
        for (let x = 5; x <= 10; x++) for (let y = 5; y <= 10; y++) {
          const dx = x - 7.5, dy = y - 7.5;
          if (dx * dx + dy * dy < 8) s(x, y, (dx < 0 && dy < 0) ? MATS.copper.light : MATS.copper.base);
        }
      });
  }
  // 兜底：问号块
  return simple('#888', (s) => {
    for (let x = 3; x <= 12; x++) for (let y = 3; y <= 12; y++) s(x, y, '#777');

```


---

## 🤖 Assistant · 2026-08-12T15:56:59.091Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything now. Also, quickly note: does UI iconUrl check `game.atlas` first then fall back to `game.assets.itemIcons` (procedural)? Yes (UI.ts:63/66).

One more check — the ItemIconGen icon for def.key lookup: `generateAllItemIcons` iterates ITEM_DEFS — includes vi_ items (question mark fallback for all vi_ — 6000+ canvases, but atlas covers them first).

Also note: ItemIconGen uses `def.tile === 'torch'` (tile key string compare, works for any item whose tile field is 'torch') and `key.endsWith('_bar')`/`'_ore'` (covers tin_bar etc.), and tool check by tier prefix.

Now, also need: does anything reference local keys in src/ui beyond what I found? Let me quickly grep UI.ts for all local keys to be complete — I covered: coin keys (1844-1845), buff maps (2412-2421, 2490-2498), RECIPES loop. Also 'chest' slot where (not item). Also there might be an item search panel listing local keys. Let me check UI.ts for a curated item list.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:57:00.611Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -nE \"'(wood|gel|copper_bar|iron_bar|lens|torch|platform|door|workbench|furnace|anvil|chest|coin_|wood_|copper_|iron_|silver_|gold_|tin_|lead_|tungsten_|platinum_|wooden_|iron_bow|wand_of_sparking|amethyst_bolt|worm_food|bloody_spine|slime_crown|mechanical_|wire|_wrench|wire_cutter|actuator|multicolor|grand_design|goblin_|snow_globe|pirate_map|_bucket|minecart_item|life_crystal|suspicious_eye|acorn|rope|bomb|_potion|_horseshoe|feral_claws)'\" src/ui/UI.ts | grep -v \"vi_\" | head -40",
 "description": "Final UI.ts local key sweep"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:57:00.655Z

**📎 ToolResult**

```
22:type SlotWhere = 'inv' | 'chest' | 'armor' | 'dye' | 'misc' | 'miscDye';
757:    if (where === 'chest') {
935:      if (tw === 'chest' && !this.openChest) return;
1797:      grid.appendChild(this.makeSlotEl(i, 'chest'));
1884:        this.setSlotGlow('chest', k, ((order.get(id) ?? 0) + 0.5) / n);
1936:    else if (where === 'chest') tex = 'Inventory_Back5';
2113:        const slotEl = this.slotEl(i, 'chest');
2116:          this.paintSlotChrome(slotEl, 'chest', i);
2416:      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
2493:      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],

```


---

## 🤖 Assistant · 2026-08-12T15:57:10.365Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — UI.ts 'chest' hits are slot-where strings, not item keys.

I now have everything for a comprehensive report. Let me also double-check src/core/Game.ts 10103 (coinsOwned) and 7436-7438 (shop currency), 7250, 6457, 9605, 5689, 2313, 2558-2585, 5328-5334, 7460, 8470-8513, 1083, 1320, 5178-5222, 6872-6913 — I have enough context for all.

One thing: does anything in src/net reference local item keys? SyncItem passes key strings — the key is whatever def.key is, so local keys flow over the wire as strings. That's a compat note: migrating keys changes wire strings (no version gate). Check ClientNet sendItemOp callers to see what key is passed — Game.spawnDrop. Fine.

Also check Game.netDropSweep for how key is derived.

I think we're done. Let me write the report.

Actually — one more: check whether vanilla recipes produce items that overlap legacy RECIPES outputs (double display). The test at vanilla-recipes.test.ts:91 asserts RECIPES outs are never vi_. But do vanilla recipes duplicate legacy ones (e.g., torch create=8 exists in VANILLA_RECIPES AND RECIPES out='torch')? Yes! Test line 25: VANILLA_RECIPES has torch recipe (1 wood + 1 gel → 3, hand). And RECIPES line 13 also has torch. So currently BOTH show (double display) — the legacy table is redundant with vanilla for torch. But vanilla torch recipe requires owned vid 9 (vi_9_wood) and 23 (vi_23_Gel); if player holds local 'wood'/'gel' (no vid), vanilla sees 0 → shows nothing; legacy RECIPES sees local wood/gel. So they coexist serving different item identities.

Early chain if RECIPES deleted: workbench (create 36 in vanilla? yes vi_36_work_bench registered; vanilla recipe exists), torch, platform, door, furnace, anvil, chest — vanilla-recipes.json has all these (2688 recipes). So the vanilla section covers them, provided materials have vid. Key risk: local materials without vid are invisible to collectOwnedItems.

Let me verify a couple in vanilla-recipes.json: create 33 (furnace), 35 (anvil), 48 (chest)? Quick node check.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:57:12.894Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst d=require('~/Project/GLM/SandboxWorld/game/src/data/vanilla-recipes.json');\nconst want={8:'Torch',9:'Wood',25:'WoodenDoor',33:'Furnace',35:'IronAnvil',36:'WorkBench',48:'Chest',94:'Platform',19:'GoldBar',20:'CopperBar',22:'IronBar',70:'WormFood',43:'SuspiciousEye',188:'HealingPotion',28:'LesserHealing',24:'WoodenSword',196:'WoodenHammer',1:'IronPickaxe',3509:'CopperPickaxe',89:'CopperHelmet',80:'CopperChainmail',76:'CopperGreaves'};\nfor(const [id,n] of Object.entries(want)){\n  const rs=d.recipes.filter(r=>r.create===+id);\n  console.log(n,'('+id+'):',rs.length?rs.map(r=>({tile:r.tile,items:r.items,grp:r.groups})): 'NONE');\n}\n\" 2>&1 | head -40",
 "description": "Check vanilla recipes for early chain items"
}
```


---

## 👤 User(sidechain) · 2026-08-12T15:57:29.906Z

**📎 ToolResult**

```
IronPickaxe (1): [ { tile: 16, items: [ [Object], [Object] ], grp: [ 24 ] } ]
Torch (8): [ { tile: -1, items: [ [Object], [Object] ], grp: [ 24 ] } ]
Wood (9): [
  { tile: 304, items: [ [Object] ], grp: [] },
  { tile: 304, items: [ [Object] ], grp: [] },
  { tile: 18, items: [ [Object] ], grp: [] },
  { tile: 18, items: [ [Object] ], grp: [] }
]
GoldBar (19): [ { tile: 17, items: [ [Object] ], grp: [] } ]
CopperBar (20): [ { tile: 17, items: [ [Object] ], grp: [] } ]
IronBar (22): [
  { tile: 17, items: [ [Object] ], grp: [] },
  { tile: 16, items: [ [Object] ], grp: [] }
]
WoodenSword (24): [ { tile: 18, items: [ [Object] ], grp: [] } ]
WoodenDoor (25): [ { tile: 18, items: [ [Object] ], grp: [] } ]
LesserHealing (28): [ { tile: 13, items: [ [Object], [Object], [Object] ], grp: [] } ]
Furnace (33): [
  {
    tile: 18,
    items: [ [Object], [Object], [Object] ],
    grp: [ 24, 25 ]
  }
]
IronAnvil (35): [ { tile: 18, items: [ [Object] ], grp: [] } ]
WorkBench (36): [ { tile: -1, items: [ [Object] ], grp: [] } ]
SuspiciousEye (43): [ { tile: 26, items: [ [Object] ], grp: [] } ]
Chest (48): [ { tile: 18, items: [ [Object], [Object] ], grp: [ 27 ] } ]
WormFood (70): [ { tile: 26, items: [ [Object], [Object] ], grp: [] } ]
CopperGreaves (76): [ { tile: 16, items: [ [Object] ], grp: [] } ]
CopperChainmail (80): [ { tile: 16, items: [ [Object] ], grp: [] } ]
CopperHelmet (89): [ { tile: 16, items: [ [Object] ], grp: [] } ]
Platform (94): [ { tile: -1, items: [ [Object] ], grp: [] } ]
HealingPotion (188): [ { tile: 13, items: [ [Object], [Object] ], grp: [] } ]
WoodenHammer (196): [ { tile: 18, items: [ [Object] ], grp: [] } ]
CopperPickaxe (3509): [ { tile: 16, items: [ [Object], [Object] ], grp: [ 24 ] } ]

```


---

## 🤖 Assistant · 2026-08-12T15:57:33.437Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vanilla recipe table covers the whole early chain (workbench hand, torch hand, platform hand, door/furnace/anvil/chest at workbench, bars at furnace, tools/armor at anvil, suspicious eye at demon altar 26). So the vanilla section CAN support the early game — provided the materials resolve to vi_ items with vid.

Now I'm ready to write the final structured report. I should be thorough but organized by the 8 categories with file:line references. Since I'm in plan mode as a read-only search agent, my deliverable is the report text itself.

Let me compile everything.
```

</details>


---

## 🤖 Assistant · 2026-08-12T15:58:47.829Z · glm-x-preview-260804

```
# 本地自制物品引用清单（迁移影响面审计）

前置事实（决定后面所有结论）：
- 本地 key 的权威清单 = `~/Project/GLM/SandboxWorld/game/src/data/items.ts:923-1054` 的 `PRIV_ITEM_STABLE`（非 `place_v_*` 段共 **184 个** key，稳定 id 10000–10501 段）。vi_* 的稳定 id = key 内嵌原版 id（items.ts:1068-1078）。
- 本地 key 与 tile key 大量同名（`wood`/`torch`/`door`/`workbench`/`furnace`/`anvil`/`chest`/`platform`/`table`/`chair`/`bed`/`glass`/`obsidian`/`candle`/`lantern`…）。判定法：`TILE_BY_KEY[...]`、`TILE_DEFS[]`、`def.tile ===`、世界生成 pass 里的裸字符串 = **tile 侧不用迁**；`ITEM_BY_KEY[...]`、`ITEM_DEFS[]`、`def.key ===`、`spawnDrop(key)`、`RECIPES` = **item 侧要迁**。
- i18n 生成表 `src/i18n/idNames.generated.ts:25003` 的 `ITEM_KEY_TO_ID` **已含全部本地 key → 原版 id** 映射（`"wood":9, "gel":23, "copper_bar":20, "copper_pickaxe":3509 …`），迁移改名后名称链可自动复用。

---

## 1. 硬编码 key 引用（item 侧，要迁）

### src/core/Game.ts（最重）
| 位置 | 内容 |
|---|---|
| Game.ts:390-391 | 死亡发还起始三件套 fallback：`VANILLA_ITEM_KEY_BY_ID[3507] ?? 'copper_sword'` 等 |
| Game.ts:1083 | `key === 'minecart_item'` → 矿车贴图 |
| Game.ts:1320 | `key === 'multicolor_wrench' \|\| 'grand_design'` → R 键切模式 |
| Game.ts:1645-1647 | `loadWorld` 初始装备 `ITEM_BY_KEY['copper_pickaxe'/'copper_axe'/'copper_sword']` |
| Game.ts:1456 | `playerPreviewArmor()`：`['iron_helmet','iron_chainmail','iron_greaves']` |
| Game.ts:2558 / 2565 / 2579 | 手持 `key === 'water_candle'`（item）＋ `TILE_BY_KEY['water_candle'/'lantern']`（tile，不迁） |
| Game.ts:2986 / 3001 / 3012 | 火把光照特判 `heldDef.key === 'torch' ? 8 : viIdFromKey(...)`（3 处，item） |
| Game.ts:3084-3085 | 掉落物点光 `def.tile === 'torch'` / `def.tile === 'candle'`（经 tile 字段间接绑本地 key） |
| Game.ts:3562 / 3728 / 3767 | `heldDef.key === 'suspicious_eye'`、`'life_crystal' \|\| 'vi_29_LifeCrystal'`（后者已是 vi_ 双轨先例） |
| Game.ts:3964-3983 | Boss 召唤物：`'worm_food'/'bloody_spine'/'slime_crown'`、`'mechanical_worm'/'mechanical_eye'/'mechanical_skull'` |
| Game.ts:4004-4009 | 入侵物：`'goblin_battle_standard'/'snow_globe'/'pirate_map'` |
| Game.ts:4062-4063 | 桶四态 `'empty_bucket'/'water_bucket'/'lava_bucket'/'honey_bucket'` |
| Game.ts:4753 | 门拆除掉落 `def.drop ?? 'door'` |
| Game.ts:4852-4856 | 瓦罐/蘑菇掉落 `'mushroom_item'`、`'mushroom_grass_seeds'` |
| Game.ts:5004-5015, 5079, 5125-5133 | 树/宝箱怪掉落 `'wood'`、`'acorn'`、`'mushroom_grass_seeds'` |
| Game.ts:5045-5046 | King Slime 掉落 `[['coin_gold',1],['gel',100]]` 等（本地 key 直写） |
| Game.ts:5104 | 宝石树掉落 `dropId === 3 ? 'stone_block' : VANILLA_ITEM_KEY_BY_ID[dropId]` |
| Game.ts:5178-5222 | 电路工具耗材 `ITEM_BY_KEY['actuator_item']`（4 处）＋ `key === 'multicolor_wrench'`（5190） |
| Game.ts:5328 / 5334 | `itemDef.key === 'acorn'`（种草门）、`=== 'rope'`（绳圈放置） |
| Game.ts:6457 | 钱币掉落 `type===71/72/73 ? 'coin_silver'/'coin_gold'/'coin_platinum'` |
| Game.ts:6872-6913 | 桶使用链 `key === 'empty_bucket'`、`swap('lava_bucket'/'honey_bucket'/'water_bucket'/'empty_bucket')` |
| Game.ts:7009 | 瓦罐掉落 override `{ 8:'torch', 73:'coin_copper' }`（vid→本地 key 桥） |
| Game.ts:7250 | 敌死掉钱 `spawnDrop(..., 'coin_copper', ...)` |
| Game.ts:7436-7438 | NPC 商店货币统计 `def.key === 'coin_copper'/'coin_silver'/'coin_gold'` |
| Game.ts:7460 | 炸弹钥匙集合 `new Set(['bomb','vi_166_bomb',...])`（双轨先例） |
| Game.ts:8470-8513 | 钱币存/取 `ITEM_BY_KEY['coin_gold'/'coin_silver'/'coin_copper'/'coin_platinum']`（多处）＋ 8498-8499 钱币槽跳过判断 |
| Game.ts:8687-8688 | ★死亡掉钱双轨表 `[['coin_copper','vi_71_CopperCoin'], ...]` —— **已有的本地→vi_ 兼容先例** |
| Game.ts:9605 | 火把放置掉落 `spawnDrop(..., 'torch', 1)` |
| Game.ts:9670-9672 | `stationsNearby()` 用 tile id（T.WORKBENCH/FURNACE/ANVIL）产字符串 `'workbench'/'furnace'/'anvil'` —— 字符串本身与 RECIPES.station 耦合，迁 RECIPES 时一起处理 |
| Game.ts:10103 | `coinsOwned()`：`n('coin_copper',1)+n('coin_silver',100)+...` |
| Game.ts:5689 / 2313 | `TILE_BY_KEY['bed']`（tile，不迁） |

### 其他 src
- `src/data/enemies.ts:33,40,48-50,59-60,68,75,82,90-91,99,120` — 敌人掉落表 `item:'gel'/'torch'/'coin_copper'/'iron_ore'/'lens'/'lesser_healing_potion'/'coin_gold'`。
- `src/data/tiles.ts:49-148` — **tile 的 `drop:` 字段指向本地 item key**（`drop:'dirt_block'/'stone_block'/'wood'/'torch'/'workbench'/'furnace'/'anvil'/'chest'/'door'/'mushroom_item'/'acorn'/'copper_ore'/'iron_bar'…`）。这是掉落链最大的一批引用（tile key 本身不迁，但 drop 值要迁）。
- `src/entities/Enemy.ts:59-61` — `NATIVE_DROP_KEY`（vid→本地 key 的掉落桥）：`71-74→coin_*`、`23:'gel'`、`8:'torch'`、`236:'lens'`、`3:'stone_block'`、`2:'dirt_block'`、`9:'wood'`、`28:'lesser_healing_potion'`。
- `src/entities/ItemDrop.ts:85` — 拾取音效 `key === 'coin_copper'`。
- `src/entities/Player.ts:186,193` — 配饰效果 `accessory === 'lucky_horseshoe' / 'feral_claws'`（字段值绑定本地 def）。
- `src/items/Inventory.ts:39` — `COIN_KEYS = ['coin_copper','coin_silver','coin_gold','coin_platinum']`（63/97/274/277 处消费：钱币槽归属、100 进位合成）。
- `src/mainFlow.ts:320-323` — wld 导入后赠品 `ITEM_BY_KEY['copper_pickaxe'/'copper_axe'/'copper_sword'/'torch']`。
- `src/player/SmartCursor.ts:1216,1493,1523` — `env.held.def?.key === 'torch' / 'empty_bucket' / 'actuator_item'`（每处都已是 `vid === ... ||` 双轨）。
- `src/render/Renderer.ts:3131` — 持物姿势 `def.key === 'torch' ? 8 : viIdFromKey(...)`。
- `src/world/Torch.ts:94` — `torchStyleOfItemKey`: `key === 'torch'` 返回 0（legacy 火把样式分支）。
- `src/world/Extractinator.ts:72` — `COIN_KEY_BY_VID {71:'coin_copper'...}`。
- `src/wld/WldImport.ts:420-433` — ★wld 物品导入映射 `ITEM_MAP`：`2:'dirt_block', 8:'torch', 9:'wood', 11-14 矿, 20/22 锭, 23:'gel', 28/38 药水/晶状体, 71-74 全→'coin_copper'（旧 bug）, 5:'mushroom_item', 27:'acorn', 699-706, 177-182, 664…`。
- `src/ui/UI.ts:1844-1845, 2412-2421, 2490-2498` — 钱币排序跳过、两张 Buff→图标物品映射表（agility/ironskin/heal/thorns/regen/obsidian_skin/gills/mana_regen/magic_power/featherfall/water_walking/archery/night_owl 药水 ＋ torch/meteorite/honey_bucket/lesser_healing_potion/sand_block 近义图标）。
- `src/assets/ItemIconGen.ts:170-280` — 程序化图标按 `def.tile`/`def.tool`/`key.endsWith('_bar'|'_ore')`/switch case `'gel'/'mushroom_item'/'lens'/'suspicious_eye'/'lesser_healing_potion'/'coin_copper'` 分派（迁走后这些分支变死代码）。

### tile 侧同名 key（**不用迁**，列出来防误伤）
`TILE_BY_KEY['chest'/'platform'/'torch'/'workbench'/'furnace'/'anvil'/'table'/'chair'/'bed'/'water_candle'/'lantern'/'candelabra'/'door_closed'/'obsidian'/'desert_fossil']`（src/world/gen/vanilla/* 多处、Game.ts:2313/2565/2579/5689、tests 多处）、`src/world/Housing.ts:41,45`（`key === 'workbench'`、`key.includes('table')` 是 tile key）、`src/render/ChunkCache.ts:63`（`'glass'` 是 tile key）、`src/wld/WldImport.ts:116-164`（tile 映射）、`src/world/gen/vanilla/CaveHousePass.ts:141,265,415-421,437`（theme/家具 tile key）、`src/ui/UI.ts` 的 `'chest'`（SlotWhere，UI 槽位名非物品）、`src/world/Door.ts:141`（音效名）。

---

## 2. recipes.ts 自制配方表及其消费方

表本体：`src/data/recipes.ts:11-113`（RECIPES，94 条；产物全为本地 key，材料也全是本地 key；recipes.ts:110-112 注释明确“vi_ 产物一律走原版配方段，本表禁登”）。

消费方：
- `src/ui/UI.ts:2127-2161` `refreshCrafting()` 的 **RECIPES 段**（`game.canCraft(r)` → 行渲染 → `game.craft(r)`），在 `── 原版配方 ──`（UI.ts:2183）之前渲染。站点名映射 UI.ts:2134（hand/workbench/furnace/anvil）。
- `src/core/Game.ts:9678-9693`：`itemId()`、`stationsNearby()`、`canCraft(r)`、`craft(r)`（`ITEM_BY_KEY[key]` 扣/加）。
- `tests/vanilla-recipes.test.ts:80-99`：RECIPES 去重 / 禁 vi_ 产物 / `out === 'wood_hammer'` 恰好一条 的三个防回归用例。

**废弃 RECIPES 会失去什么**：失去的是“以本地 key 计数”的合成入口。**早期合成链本身不会消失**——已核实 `vanilla-recipes.json`（3173 条）完整覆盖：WorkBench(36)徒手、Torch(8)徒手 1木+1凝胶→3、Platform(94)徒手、Door(25)/Furnace(33)/Anvil(35)/Chest(48)在工作台、四系锭(19/20/21/22)在熔炉、铜/铁/银/金镐斧剑锤与三件套盔甲在铁砧、WoodenHammer(196)、SuspiciousEye(43)在恶魔祭坛、LesserHealingPotion(28)/HealingPotion(188)在放置瓶。UI 的“── 原版配方 ──”段（UI.ts:2183-2240）独立渲染、独立 `game.vanillaCraft(r, n)`（UI.ts:2225），不依赖 RECIPES。

**真正的依赖坑**：`src/data/vanillaRecipes.ts:61-67` `collectOwnedItems()` 只统计 `vid >= 0` 的物品。本地 `wood/gel/铜矿/铁锭…` 的 def **没有 `vid` 字段**（items.ts:82-115），因此玩家手里的本地材料对原版配方段**完全不可见**。→ 迁移若只是“删本地 def + 掉落改指 vi_ key”，材料自动获得 vid，原版配方段即可接管早期链；反之若先删 RECIPES 而掉落仍发本地 key，早期合成会全断。另注意 `VID_TO_KEY`（vanillaRecipes.ts:138-145）与 `invIndexOfVanilla`（:216-229）取**首个** vid 匹配 def——迁移后同 vid 双注册会归一到首个（items.ts:1067 注释已声明该语义）。

---

## 3. 物品使用链（工具/武器/魔法/远程）

工具判定与数值已**双轨且 vi_ 侧已数据驱动**：
- 判定入口 `src/core/Game.ts:3527`（updateUse）、`:3360`（updateSmartCursor）、`:7116`（updateSwingHits）：`const tool = heldDef?.tool ?? this.itemFuncTool(held.id)` —— legacy `def.tool` 优先，vi_ 走 `itemFuncTool`（Game.ts:3239-3250，解析 `/^vi_(\d+)_/` → `vanilla-itemfunc.json` 的 pick/axe/hammer）。
- 挖掘力/击数：vi_ 取 vanilla-itemfunc + combat 表（见 `tests/mining.test.ts` 与 `src/data/items.ts:1081-1090` `VANILLA_TOOL_POWERS` 给 vi_ 道具补 `def.tool`，含铜/铁/银/金锤 3505/3511/3517、Pwnhammer 367、Drax 579 等）。
- 挥舞伤害/近战盒：Game.ts:7116-7140 `meleeDmg = this.swing.dmg ?? tool?.damage ?? swingCombat?.damage ?? 0`；`noMelee = heldDef.magic || swingCombat?.noMelee`。
- 使用节奏：Game.ts:3285-3299 `heldUseAnimation`（legacy 取 `def.tool.speed`，vi_ 取 combat.useAnimation）；`heldUseStyle`（:3274-3283）legacy 无 vid 时查 `LEGACY_USE_STYLE[def.key]`（Game.ts:3239 附近）——**按本地 key 的表，迁移时要么删要么换成 vid 判定**。
- 弓/远程：Game.ts:3854-3945，`heldDef.ranged || rangedAmmoWeapon(heldDef)`；`bowVid = rg?.vid ?? viIdFromKey(heldDef.key)`，数值取 `itemCombat(bowVid)`；弹药匹配 `ammoOf(d) = d.ammoId ?? itemCombat(...)?.ammo`（本地 `wooden_arrow`/`flaming_arrow` 靠 `ammoId:40`，vi_ 靠 combat.ammo）。木弓/铁弓的 def 已带 `vid:39/99`（items.ts:876-881）。
- 魔法：Game.ts:4034-4076，走 **legacy 专属** `heldDef.magic`（damage/speed/manaCost/projSpeed/proj:'spark'|'bolt'），发射自绘 `MagicProj`。vi_ 对照：`vi_113_magic_missile`、`vi_739_amethyst_staff`（tests/vi-weapons.test.ts:53-56 断言 `{kind:'magic', mana:5, shoot:121, damage:15, useTime:37}`）走 `combatWeapon` 的 `useCombatWeapon` 分支（Game.ts:3944 附近 + 4342 case 'magic'），**数值/投射物全部数据驱动且能力更强**（原版弹体、mana、autoReuse）。本地 `wand_of_sparking`/`amethyst_bolt`（items.ts:887-890）的 `magic` 结构是自创简化版，vi_3069/vi_739 已能完全替代。
- 配饰：本地 `accessory:'lucky_horseshoe'/'feral_claws'` 仅 `Player.ts:186/193` 两处消费；vi_158/vi_211 走 `vanilla-itemstats.json` + `vanillaAccFx`（Player.ts:309-347 `fx.noFallDmg/fx.meleeSpd`），**vi_ 侧已有等价能力**，本地字段是并行旧路径。

结论：除 `LEGACY_USE_STYLE`、`heldDef.magic` 自定义 MagicProj、`accessory` 枚举三处外，vi_ 物品能力覆盖 ≥ 本地物品。

---

## 4. 存档

- **存的是稳定 id，不是 key**。序列化：`src/save/serialize.ts:228-230` `mapItem()` 把内部 id 经 `ITEM_STABLE_OF_INTERNAL`（items.ts:1065）写盘；读档：`src/save/SaveFile.ts:129-143` 经 `ITEM_INTERNAL_OF_STABLE` 还原。背包/箱子/储物均走此路径。
- **覆盖面缺口**：`serializeSave` 只映射 `player.inventory` 与 `player.banks`（serialize.ts:261）；`armor/dye/trash/miscEquips/miscDyes/loadouts`（serialize.ts:261 经 `{...player}` 透传）**以原始内部下标直写**，读档侧（SaveFile.ts:137-143）也只回映 inventory/banks → 这些槽位本来就对注册顺序敏感（迁移时的次生风险点，值得顺手补）。
- **版本/迁移先例（可直接套用）**：
  - v3 稳定 id 方案本体：items.ts:920-1078（注释明言“根治下标漂移；PRIV 表 append-only，号码永不复用”）。
  - 读档版本门：SaveFile.ts:129 `const v3 = (data.version ?? 1) >= 3`；v2 旧档直读 + walls 旧值迁移（:219-231 `version<2` 墙 id remap）——**已有按 version 分支迁移的先例**。
  - `Inventory.migrateLegacy`（src/items/Inventory.ts:331，mainFlow.ts:195 调用）：旧 54 槽 → 58 槽+armor[20] 的布局迁移。
  - 离线工具 `tools/migrate-save.mjs`：v1/v2 下标 → v3 稳定 id 重写器（从 git 历史还原注册顺序）。
- **CharacterStore**（src/save/CharacterStore.ts）：只存 `Appearance`（外观/难度），**不含任何物品**；起始装备不在角色档，而在 Game.ts:1645-1647 / mainFlow.ts:320-323。
- **删本地定义后老存档会怎样**：老 v3 档里本地物品的稳定 id 是 10000-10501 私有段。若直接删 PRIV 表登记项，items.ts:1074 `PRIV_ITEM_STABLE[k] ?? ...` 返回 undefined → :1075 `console.error('[stable-id] item 缺稳定 id')` 且 `ITEM_STABLE_OF_INTERNAL[i] = 0`；读档时 `ITEM_INTERNAL_OF_STABLE.get(100xx) ?? 0`（SaveFile.ts:131）→ **背包/箱子里这些物品全部变成 id 0（凭空消失）**，且 armor/dye 等未映射槽位会因内部下标整体左移而**错位成别的物品**。所以迁移必须保留一张 `旧稳定 id 100xx → 原版 vid` 的换算表（读档时在 `mapItem` 里多一步 remap，或按 v4 版本号门控）。

---

## 5. 联机

`src/net/protocol.ts`：
- **msg5 SyncPlayerItem（protocol.ts:26-28, 219-258）**：`u16 itemId` = **内部 id**（`w.u16(e.itemId & 0xffff)` :243）。写入侧 `src/net/ClientNet.ts:792/815` 直接取 `arr[i]?.id`（Inventory 内部 id）。内部 id 随注册顺序漂移 → 本地 def 删除后**联机双方内部 id 表必须一致**，旧客户端/新客户端混房会错物品。
- **msg32 SyncChestItem（protocol.ts:63-64, ClientNet.ts:629）**：`u16 itemId` 同为内部 id。
- **msg21 SyncItem（掉落物，protocol.ts:45-46）**：传 **字符串 key**（`str key`），ClientNet.ts:449-454/691/703-707。本地 key 改名后，跨版本掉落物 key 会对不上（`ITEM_BY_KEY[newKey] === undefined` 路径）。
- 无任何协议层 id 版本协商；迁移时需同版本发布。

---

## 6. 图标

解析链 `src/assets/SpriteAtlas.ts:486-505` `atlasIconForKey()`：
1. `VANILLA_ITEM_ICON_MAP[key]`（SpriteAtlas.ts:508 起）——**169/184 个本地 key 在此显式映射到原版图标 id**（含 `wood_pickaxe:3509`、`amethyst_bolt:739`、`worm_food:70` 等全量），即本地物品图标**现在就来自原版 Item_N 图集**；
2. `vi_<id>_*` → `atlas.vicon(id)`；
3. `place_v_*` → 图块表首帧；
4. null → 调用方回退程序化图标。

**15 个本地 key 无 atlas 映射**（会落到程序化 ItemIconGen，多数最终是“问号块”）：`mechanical_worm/eye/skull, goblin_battle_standard, snow_globe, pirate_map, coin_platinum, obsidian_skin_potion, gills_potion, mana_regen_potion, magic_power_potion, featherfall_potion, water_walking_potion, archery_potion, night_owl_potion` —— 迁移到 vi_ 后这 15 个**反而升级**为真原版图标。

回退消费方：`src/ui/UI.ts:42-70` `iconUrl()`（atlas 失败 → `game.assets.itemIcons.get(id)` 程序化）；`src/render/Renderer.ts:674-678` `atlasIcon()`；`src/core/Game.ts:1404-1415`（`VANILLA_ITEM_ICON_MAP[def.key] ?? vi_ 前缀解析` → vicon 懒载）；`src/assets/ItemIconGen.ts:284-289` 为**每个** ITEM_DEFS 生成程序化图标（本地 key 分支见第 1 节；删除本地 def 后相应分支成为死代码）。

---

## 7. tests（迁移后要同步改）

引用**本地 item key** 的测试：
- `tests/mining.test.ts:46-54` — copper/iron/silver/gold pickaxe/axe、wood_hammer 的 `def.tool` 字段断言（迁移后 vi_ 道具的 tool 由 VANILLA_TOOL_POWERS 补，断言需换 key）
- `tests/smart-cursor.test.ts:43-48, 278, 287` — `ITEM_BY_KEY['copper_pickaxe'/'copper_axe'/'wood_hammer'/'torch'/'dirt_block'/'platform'/'empty_bucket']`
- `tests/save.test.ts:26, 29` — 箱内 `ITEM_BY_KEY['torch']`、背包 `ITEM_BY_KEY['dirt_block']`（★存档往返用例，迁移后可直接验证稳定 id remap）
- `tests/shimmer.test.ts:127, 138` — `'coin_gold'`、`ITEM_BY_KEY['torch']` 掉落
- `tests/world-difficulty.test.ts:68-69, 80-81` — torch / copper_pickaxe 掉落断言
- `tests/item-coverage.test.ts:37` — `Lang.itemNameByKey('copper_pickaxe') === '铜镐'`
- `tests/vanilla-recipes.test.ts:96` — `RECIPES.filter(r => r.out === 'wood_hammer')`（删 RECIPES 时整段 describe 移除）
- `tests/vi-weapons.test.ts:63` — `combatWeapon({ key:'wooden_bow', vid:39 })` 为 null 的用例
- `tests/thrown-weapons.test.ts:39, 46` — `ITEM_BY_KEY['wood_bow']`（★疑为 `'wooden_bow'` 笔误，当前取到 undefined）、`'wooden_arrow'`
- 弹药/投射物类用 Arrow 构造器第 9 参 `'wooden_arrow'`（掉落回收 key）：`tests/arrow-tree-pass.test.ts:31,43`、`tests/hostile-proj-player-hit.test.ts:73`、`tests/proj-critter-hit.test.ts:32,51`、`tests/projectile-reflect.test.ts:74,92,109,132`
- `tests/tile-drop-null.test.ts:18` — `breakTileAt` 返回 `'dirt_block'`（tile drop 链断言）
- `scripts/_craftdupprobe.mjs:21` — `window.__swItems['wood']`（调试脚本）

只引用**同名 tile key**（不用改）：tests/cavewalls / conveyor / explosion / living-tree / lunar-final-audit / micro-biomes / pot-break / wld-furnace-mapping（全是 `TILE_BY_KEY['chest'/'platform'/'furnace'/'anvil'/'chair'...]`）、tests/fireworks（`'chair'` tile）、tests/wind-sway（`'dirt'/'tree'`）。

---

## 8. SmartSelect / 放置链

- **本地放置链**：`src/core/Game.ts:3713-3715` `heldDef?.tile != null → this.tryPlace(tx,ty,heldDef)`；`tryPlace`（Game.ts:5304-5450）全程用 **`itemDef.tile` 字段** → `TILE_BY_KEY[itemDef.tile!]`（:5315），再按 `TILE_DEFS[tileId]` 的 w/h/framed/vanilla.frame 处理。`placeStyle` 来自 `itemDef.placeStyle`。本地放置物（torch/door/workbench/furnace/anvil/chest/platform/家具/种子/绳）全部靠 items.ts 里手写的 `tile:` 字段。
- **vi_ 放置链**：**没有 createTile 反查**。`vanilla-itemfunc.json` 虽提取了 `createTile/createWall/placeStyle`（src/data/vanillaItemFunc.ts:11），但 tryPlace 不读它；vi_ 物品能放置仅因为 items.ts 手工补了 `tile`（音乐盒 :804-813、喷泉 :819-830、gemcorn :835-841、轨道 :668-669、药草种子 :473-479、月相砖 :525-531 等）或 key 恰好是 `place_v_*`。→ **迁移时每个有放置语义的本地物品，必须确认目标 vi_ key 已带 `tile`/`placeStyle`，否则放置能力丢失**（例如 `torch`→vi_8、`door`→vi_25（items.ts:663 已注册）、`workbench`→vi_36（:654）、`anvil`→vi_35（:653）、`platform`→vi_94（:683）、`furnace`→vi_33、`chest`→vi_48、`rope`→vi_965（:323）——多数已注册但**多数没补 tile 字段**）。
- tryPlace 内的 key 特判：`itemDef.key === 'acorn'`（:5328 草上种植门）、`=== 'rope'`（:5334 绳圈下延）、`tileId === T.TORCH` 走 `torchStyleOfItemKey(itemDef.key)`（:5352；Torch.ts:94 对 `'torch'` 返回 0，vi_ 彩炬/群系炬按 vid）。
- **SmartSelect/SmartCursor 画像**：`src/core/Game.ts:3462-3485` `smartSelectSlots()` 用 `def?.tool ?? itemFuncTool`；`src/player/SmartCursor.ts:368-382` `createTileSheet` 由 **`def?.tile`**（非 createTile 数据）派生，`:987-988` 轨道判定 `sem.createTileSheet === 314 || vid===2340/2739/2492`，`:1216` 火把、`:1493` 桶(vid 205)、`:1523` 致动器(vid 849) 均已 vid 双轨。放置范围判定 Game.ts:3365 `placing = heldDef?.tile != null || heldDef?.wallId != null`。
- 墙放置：Game.ts:3708-3711 `heldDef?.wallId != null → tryPlaceWall`；`wallId` 对 vi_ 由 `vanilla-wallitems.json` 自动补（items.ts:1058-1063），对本地墙面物品无（本地无 wall 物品）。
- 沙盒展示区 Game.ts:1006-1013：遍历 `ITEM_DEFS` 收集 `def.tile` 指向的所有 tile —— 删本地 def 后该列表自动缩。

---

## 迁移要点速记（基于以上证据）
1. 必建 **10000-10501 旧稳定 id → 原版 vid** 换算表（读档 remap，SaveFile.ts:130-143 处加一步），否则老档物品变 0、装备槽错位。
2. **先改掉落/瓦罐/NPC 掉落/树掉落来源**（tiles.ts `drop:`、Enemy.ts `NATIVE_DROP_KEY`、Game.ts 5004-5133/6457/7009/7250、Extractinator `COIN_KEY_BY_VID`、WldImport `ITEM_MAP`、enemies.ts drops）→ 再删 RECIPES → 早期链由原版配方段接管（`collectOwnedItems` 的 vid 门槛自动满足）。
3. **给目标 vi_ key 补 `tile`/`placeStyle`**（tryPlace 不读 createTile），否则放置语义丢失。
4. 同步清理：`LEGACY_USE_STYLE`（Game.ts:3279）、本地 `magic`/`accessory`/`ranged`/`ammoId` 旧路径、`VANILLA_ITEM_ICON_MAP` 本地段、ItemIconGen 本地分支、UI 两张 Buff 图标表、Inventory `COIN_KEYS`、Player.ts:186/193。
5. 联机需同版本发布（msg5/msg32 内部 id、msg21 key 串都随注册表变）。
```
