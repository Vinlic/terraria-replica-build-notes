# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T09:09:08.340Z

```
调研 ~/Project/GLM/SandboxWorld/game/ 目录（一个用 vite + TypeScript 复刻泰拉瑞亚的项目）。搜索广度：very thorough。

我需要全面了解：
1. 项目整体结构：入口文件、渲染方式（Canvas 2D? WebGL? PixiJS?）、游戏主循环位置、状态机/场景管理方式
2. 现有的 UI 相关代码：背包/物品栏界面、主菜单、设置界面等现在是否已存在？在哪些文件？实现到什么程度？用什么模式写的（DOM overlay? Canvas 绘制? 即时模式还是保留模式 UI 框架?）
3. 现有的输入处理、鼠标/键盘事件系统
4. 素材加载方式：贴图如何加载（路径、懒加载模式）、字体如何处理、缩放方式（原版 2x 像素风格?）
5. 物品系统：物品数据结构、Item 类定义、合成表是否已存在、物品贴图如何关联
6. 世界生成入口：worldgen 管线从哪里被调用，是否已有进度回调/事件机制可以暴露 UI
7. 玩家/角色数据结构：Player 类有哪些字段（外观、名称等），存档如何保存
8. 现有的语言/i18n 支持（原版文本是否需要中文?）

请给出关键文件的路径和行号、关键类名/函数名，以及现有 UI 的截图级描述（布局代码逻辑）。最后总结现有架构对实现「主菜单→创建角色→创建世界→世界生成进度（带地图实时预览）→游戏内背包/合成/设置」这条 UI 链路的适配程度和缺口。
```

---

## 📎 Attachment · skill_listing · 2026-08-09T09:09:08.342Z

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

## 🤖 Assistant · 2026-08-09T09:09:13.369Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a very thorough investigation of the SandboxWorld/game directory. Let me start by exploring the project structure.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:13.371Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld -maxdepth 2 -not -path '*/node_modules*' -not -path '*/.git*' | head -100",
 "description": "List top-level project structure"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:13.444Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game -type d -not -path '*node_modules*' -not -path '*.git*' | sort",
 "description": "List all directories under game"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:13.465Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld
~/Project/GLM/SandboxWorld/verify-torch.mjs
~/Project/GLM/SandboxWorld/check-size.mjs
~/Project/GLM/SandboxWorld/tools
~/Project/GLM/SandboxWorld/verify-bleed2.mjs
~/Project/GLM/SandboxWorld/.DS_Store
~/Project/GLM/SandboxWorld/Terarria1405
~/Project/GLM/SandboxWorld/verify-swing.mjs
~/Project/GLM/SandboxWorld/verify-dev.mjs
~/Project/GLM/SandboxWorld/game
~/Project/GLM/SandboxWorld/verify-stable.mjs
~/Project/GLM/SandboxWorld/verify-quickload.mjs
~/Project/GLM/SandboxWorld/verify-wld2.mjs
~/Project/GLM/SandboxWorld/backups
~/Project/GLM/SandboxWorld/terraria-wiki-md
~/Project/GLM/SandboxWorld/annotations.json
~/Project/GLM/SandboxWorld/terraria.wiki.gg_en_all_2026-07a.zim
~/Project/GLM/SandboxWorld/terraria-assets
~/Project/GLM/SandboxWorld/Terraia_Maples
~/Project/GLM/SandboxWorld/Terraria-Map-Editor
~/Project/GLM/SandboxWorld/tools/build-id-maps.mjs
~/Project/GLM/SandboxWorld/tools/l10n
~/Project/GLM/SandboxWorld/tools/extract_l10n.py
~/Project/GLM/SandboxWorld/tools/wiki-mirror.mjs
~/Project/GLM/SandboxWorld/tools/xnb-unpack
~/Project/GLM/SandboxWorld/tools/id-maps
~/Project/GLM/SandboxWorld/tools/zim-convert.py
~/Project/GLM/SandboxWorld/tools/zim-read.py
~/Project/GLM/SandboxWorld/tools/build-asset-table.mjs
~/Project/GLM/SandboxWorld/Terarria1405/Cinematics
~/Project/GLM/SandboxWorld/Terarria1405/Netplay.cs
~/Project/GLM/SandboxWorld/Terarria1405/ObjectData
~/Project/GLM/SandboxWorld/Terarria1405/UI
~/Project/GLM/SandboxWorld/Terarria1405/Liquid.cs
~/Project/GLM/SandboxWorld/Terarria1405/WorldBuilding
~/Project/GLM/SandboxWorld/Terarria1405/Terraria1405.pdb
~/Project/GLM/SandboxWorld/Terarria1405/Gore.cs
~/Project/GLM/SandboxWorld/Terarria1405/Dust.cs
~/Project/GLM/SandboxWorld/Terarria1405/MessageBuffer.cs
~/Project/GLM/SandboxWorld/Terarria1405/ResolutionChangeEvent.cs
~/Project/GLM/SandboxWorld/Terarria1405/Star.cs
~/Project/GLM/SandboxWorld/Terarria1405/Minecart.cs
~/Project/GLM/SandboxWorld/Terarria1405/Net
~/Project/GLM/SandboxWorld/Terarria1405/AssemblyInfo.cs
~/Project/GLM/SandboxWorld/Terarria1405/NPCSpawnParams.cs
~/Project/GLM/SandboxWorld/Terarria1405/Collision.cs
~/Project/GLM/SandboxWorld/Terarria1405/Terraria1405.sln
~/Project/GLM/SandboxWorld/Terarria1405/Chat
~/Project/GLM/SandboxWorld/Terarria1405/Achievements
~/Project/GLM/SandboxWorld/Terarria1405/Lighting.cs
~/Project/GLM/SandboxWorld/Terarria1405/DelegateMethods.cs
~/Project/GLM/SandboxWorld/Terarria1405/DataStructures
~/Project/GLM/SandboxWorld/Terarria1405/NetMessage.cs
~/Project/GLM/SandboxWorld/Terarria1405/TileChangeReceivedEvent.cs
~/Project/GLM/SandboxWorld/Terarria1405/Tile.cs
~/Project/GLM/SandboxWorld/Terarria1405/StrayMethods.cs
~/Project/GLM/SandboxWorld/Terarria1405/Lang.cs
~/Project/GLM/SandboxWorld/Terarria1405/Microsoft
~/Project/GLM/SandboxWorld/Terarria1405/World.cs
~/Project/GLM/SandboxWorld/Terarria1405/Enums
~/Project/GLM/SandboxWorld/Terarria1405/IO
~/Project/GLM/SandboxWorld/Terarria1405/ZoomContext.cs
~/Project/GLM/SandboxWorld/Terarria1405/PopupText.cs
~/Project/GLM/SandboxWorld/Terarria1405/DeprecatedClassLeftInForLoading.cs
~/Project/GLM/SandboxWorld/Terarria1405/Libraries
~/Project/GLM/SandboxWorld/Terarria1405/NPC.cs
~/Project/GLM/SandboxWorld/Terarria1405/Server
~/Project/GLM/SandboxWorld/Terarria1405/Cloud.cs
~/Project/GLM/SandboxWorld/Terarria1405/FrameSkipTest.cs
~/Project/GLM/SandboxWorld/Terarria1405/WindowsLaunch.cs
~/Project/GLM/SandboxWorld/Terarria1405/Extensions
~/Project/GLM/SandboxWorld/Terarria1405/README.md
~/Project/GLM/SandboxWorld/Terarria1405/Mount.cs
~/Project/GLM/SandboxWorld/Terarria1405/Recipe.cs
~/Project/GLM/SandboxWorld/Terarria1405/Utilities
~/Project/GLM/SandboxWorld/Terarria1405/Testing
~/Project/GLM/SandboxWorld/Terarria1405/GetItemSettings.cs
~/Project/GLM/SandboxWorld/Terarria1405/Social
~/Project/GLM/SandboxWorld/Terarria1405/WaterfallManager.cs
~/Project/GLM/SandboxWorld/Terarria1405/Terraria1405.csproj
~/Project/GLM/SandboxWorld/Terarria1405/Terraria1405.csproj.user
~/Project/GLM/SandboxWorld/Terarria1405/Main.cs
~/Project/GLM/SandboxWorld/Terarria1405/PlayerSpawnContext.cs
~/Project/GLM/SandboxWorld/Terarria1405/Audio
~/Project/GLM/SandboxWorld/Terarria1405/Map
~/Project/GLM/SandboxWorld/Terarria1405/ItemSerializationContext.cs
~/Project/GLM/SandboxWorld/Terarria1405/RemoteServer.cs
~/Project/GLM/SandboxWorld/Terarria1405/GameContent
~/Project/GLM/SandboxWorld/Terarria1405/Sign.cs
~/Project/GLM/SandboxWorld/Terarria1405/SceneMetricsScanSettings.cs
~/Project/GLM/SandboxWorld/Terarria1405/WorldSections.cs
~/Project/GLM/SandboxWorld/Terarria1405/TileObject.cs
~/Project/GLM/SandboxWorld/Terarria1405/Rain.cs
~/Project/GLM/SandboxWorld/Terarria1405/SceneMetrics.cs
~/Project/GLM/SandboxWorld/Terarria1405/TimeLogger.cs
~/Project/GLM/SandboxWorld/Terarria1405/PopupTextContext.cs
~/Project/GLM/SandboxWorld/Terarria1405/TestHighFPSIssues.cs
~/Project/GLM/SandboxWorld/Terarria1405/Item.cs
~/Project/GLM/SandboxWorld/Terarria1405/Chest.cs
~/Project/GLM/SandboxWorld/Terarria1405/Wiring.cs

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:13.474Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game
~/Project/GLM/SandboxWorld/game/dist
~/Project/GLM/SandboxWorld/game/dist/assets
~/Project/GLM/SandboxWorld/game/dist/audios
~/Project/GLM/SandboxWorld/game/dist/sounds
~/Project/GLM/SandboxWorld/game/dist/sprites
~/Project/GLM/SandboxWorld/game/dist/sprites/UI
~/Project/GLM/SandboxWorld/game/dist/sprites/UI/Buff
~/Project/GLM/SandboxWorld/game/dist/sprites/UI/工具
~/Project/GLM/SandboxWorld/game/dist/sprites/UI/饰品
~/Project/GLM/SandboxWorld/game/dist/sprites/UI/药水
~/Project/GLM/SandboxWorld/game/dist/sprites/vanilla
~/Project/GLM/SandboxWorld/game/dist/sprites/地形
~/Project/GLM/SandboxWorld/game/dist/sprites/封面
~/Project/GLM/SandboxWorld/game/dist/sprites/角色
~/Project/GLM/SandboxWorld/game/docs
~/Project/GLM/SandboxWorld/game/docs/vanilla-algos
~/Project/GLM/SandboxWorld/game/public
~/Project/GLM/SandboxWorld/game/public/audios
~/Project/GLM/SandboxWorld/game/public/sounds
~/Project/GLM/SandboxWorld/game/public/sprites
~/Project/GLM/SandboxWorld/game/public/sprites/UI
~/Project/GLM/SandboxWorld/game/public/sprites/UI/Buff
~/Project/GLM/SandboxWorld/game/public/sprites/UI/工具
~/Project/GLM/SandboxWorld/game/public/sprites/UI/饰品
~/Project/GLM/SandboxWorld/game/public/sprites/UI/药水
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla
~/Project/GLM/SandboxWorld/game/public/sprites/地形
~/Project/GLM/SandboxWorld/game/public/sprites/封面
~/Project/GLM/SandboxWorld/game/public/sprites/角色
~/Project/GLM/SandboxWorld/game/scripts
~/Project/GLM/SandboxWorld/game/shots
~/Project/GLM/SandboxWorld/game/src
~/Project/GLM/SandboxWorld/game/src/assets
~/Project/GLM/SandboxWorld/game/src/core
~/Project/GLM/SandboxWorld/game/src/data
~/Project/GLM/SandboxWorld/game/src/entities
~/Project/GLM/SandboxWorld/game/src/items
~/Project/GLM/SandboxWorld/game/src/lighting
~/Project/GLM/SandboxWorld/game/src/physics
~/Project/GLM/SandboxWorld/game/src/render
~/Project/GLM/SandboxWorld/game/src/save
~/Project/GLM/SandboxWorld/game/src/stats
~/Project/GLM/SandboxWorld/game/src/ui
~/Project/GLM/SandboxWorld/game/src/wld
~/Project/GLM/SandboxWorld/game/src/world
~/Project/GLM/SandboxWorld/game/src/world/gen
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla
~/Project/GLM/SandboxWorld/game/src/world/liquid
~/Project/GLM/SandboxWorld/game/tests
~/Project/GLM/SandboxWorld/game/tools

```


---

## 🤖 Assistant · 2026-08-09T09:09:15.389Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I'm in plan mode but I'm a read-only search agent anyway. Let me continue exploring with read-only commands. Let me list all source files.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:15.945Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src ~/Project/GLM/SandboxWorld/game/tests -type f \\( -name '*.ts' -o -name '*.tsx' -o -name '*.js' \\) | xargs wc -l | sort -rn | head -80",
 "description": "List source files by line count"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:15.969Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/ ~/Project/GLM/SandboxWorld/game/src/ui ~/Project/GLM/SandboxWorld/game/public",
 "description": "List game root, ui dir, public dir"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:15.991Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/:
dist
docs
index.html
node_modules
package-lock.json
package.json
public
scripts
shots
src
Starter_World Master.wld
tests
tools
tsconfig.json

~/Project/GLM/SandboxWorld/game/public:
annotator.html
audios
sheet-probe.html
sounds
sprites

~/Project/GLM/SandboxWorld/game/src/ui:
UI.ts

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:16.003Z

**📎 ToolResult**

```
   22671 total
    2332 ~/Project/GLM/SandboxWorld/game/src/core/Game.ts
    1426 ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
    1061 ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts
     893 ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts
     851 ~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts
     839 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
     796 ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts
     742 ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts
     724 ~/Project/GLM/SandboxWorld/game/src/data/items.ts
     675 ~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts
     672 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts
     590 ~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts
     589 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts
     415 ~/Project/GLM/SandboxWorld/game/src/assets/TileSheetGen.ts
     407 ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts
     394 ~/Project/GLM/SandboxWorld/game/src/main.ts
     389 ~/Project/GLM/SandboxWorld/game/src/render/AutoTiler.ts
     379 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts
     366 ~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts
     356 ~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts
     349 ~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts
     299 ~/Project/GLM/SandboxWorld/game/src/entities/Critter.ts
     297 ~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts
     294 ~/Project/GLM/SandboxWorld/game/src/assets/CharacterSheetGen.ts
     290 ~/Project/GLM/SandboxWorld/game/src/assets/ItemIconGen.ts
     267 ~/Project/GLM/SandboxWorld/game/src/render/VanillaLiquidRenderer.ts
     262 ~/Project/GLM/SandboxWorld/game/tests/wld.test.ts
     212 ~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts
     204 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/JunglePass.ts
     203 ~/Project/GLM/SandboxWorld/game/src/lighting/LightingEngine.ts
     199 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts
     198 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts
     182 ~/Project/GLM/SandboxWorld/game/src/items/Inventory.ts
     174 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts
     173 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CavesPass.ts
     168 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts
     166 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts
     159 ~/Project/GLM/SandboxWorld/game/src/render/WallTiler.ts
     157 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts
     147 ~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts
     144 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts
     141 ~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts
     140 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HellFortPass.ts
     130 ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts
     127 ~/Project/GLM/SandboxWorld/game/src/render/VanillaWallTiler.ts
     122 ~/Project/GLM/SandboxWorld/game/src/data/enemies.ts
     116 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts
     113 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts
     112 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts
     112 ~/Project/GLM/SandboxWorld/game/src/data/recipes.ts
     108 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts
     107 ~/Project/GLM/SandboxWorld/game/src/entities/Tombstone.ts
     104 ~/Project/GLM/SandboxWorld/game/src/world/World.ts
     101 ~/Project/GLM/SandboxWorld/game/src/physics/TileCollision.ts
      91 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts
      84 ~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts
      77 ~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts
      73 ~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
      72 ~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts
      71 ~/Project/GLM/SandboxWorld/game/tests/wld-real.test.ts
      70 ~/Project/GLM/SandboxWorld/game/src/wld/BinaryReaderLE.ts
      67 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/Spread.ts
      67 ~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts
      66 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IceBiomePass.ts
      65 ~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts
      62 ~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts
      61 ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts
      59 ~/Project/GLM/SandboxWorld/game/tests/save.test.ts
      59 ~/Project/GLM/SandboxWorld/game/src/core/HitTile.ts
      58 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenState.ts
      57 ~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts
      54 ~/Project/GLM/SandboxWorld/game/src/core/Input.ts
      52 ~/Project/GLM/SandboxWorld/game/src/assets/Palette.ts
      50 ~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts
      50 ~/Project/GLM/SandboxWorld/game/src/data/critters.ts
      50 ~/Project/GLM/SandboxWorld/game/src/core/Audio.ts
      48 ~/Project/GLM/SandboxWorld/game/src/render/Camera.ts
      47 ~/Project/GLM/SandboxWorld/game/src/core/rng.ts
      40 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DirtToMudPass.ts

```


---

## 🤖 Assistant · 2026-08-09T09:09:18.141Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read the key files. Start with main.ts, UI.ts, Game.ts, Input.ts, items, recipes, Inventory, Player, SaveFile, KvStore, WorldGen.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:18.143Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/main.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:18.150Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:18.163Z

**📎 ToolResult**

```
1	// 入口：加载素材 → 菜单 → 生成/加载世界 → 进入游戏
2	import { Game } from './core/Game';
3	import { UI } from './ui/UI';
4	import { saveGame, loadSave } from './save/SaveFile';
5	import { kvGet, kvSet, kvHas } from './save/KvStore';
6	import { ITEM_BY_KEY } from './data/items';
7	import { TILE_BY_KEY, T, TILE_DEFS, WALL_DEFS } from './data/tiles';
8	import { parseWldToSave } from './wld/WldImport';
9	import { INV_SIZE } from './items/Inventory';
10	// 调试句柄：页面内直接测 .wld 转换
11	(window as unknown as { __parseWld?: (b: Uint8Array) => unknown; __lastCompatReport?: unknown }).__parseWld = parseWldToSave as unknown as (b: Uint8Array) => unknown;
12	import { SpriteAtlas } from './assets/SpriteAtlas';
13	import { AudioSystem } from './core/Audio';
14	import { setDebugPool } from './data/vanillaNpcs';
15	
16	const root = document.getElementById('game-root')!;
17	const ui = new UI(root);
18	const audio = new AudioSystem();
19	let atlas: SpriteAtlas | null = null;
20	
21	let game: Game | null = null;
22	let inGame = false;
23	let pausePanel: HTMLElement | null = null;
24	let playStart = 0;
25	
26	const QUICK_SAVE_KEY = 'sandboxworld.quicksave';
27	
28	async function loadAssets() {
29	  atlas = new SpriteAtlas();
30	  try {
31	    await atlas.load();
32	  } catch {
33	    atlas = null; // 素材缺失时回退程序化生成
34	  }
35	}
36	
37	function enterGame(g: Game) {
38	  game = g;
39	  (window as unknown as { __swGame: Game }).__swGame = g;
40	  (window as unknown as { __swTiles: typeof TILE_BY_KEY }).__swTiles = TILE_BY_KEY;
41	  (window as unknown as { __swItems: typeof ITEM_BY_KEY }).__swItems = ITEM_BY_KEY;
42	  // 探针调试：强制原版生成池（确定性验证生成路径；传 null 恢复环境池）
43	  (window as unknown as { __swSetPool?: (p: number[] | null) => void }).__swSetPool = setDebugPool;
44	  inGame = true;
45	  playStart = Date.now();
46	  ui.game = g;
47	  ui.initInGame();
48	  ui.refreshAll();
49	  g.start();
50	  audio.play('main');
51	  ui.toast(`欢迎来到 ${g.world.name}！A/D 移动，空格跳跃，E 背包，Esc 暂停`);
52	}
53	
54	function maybeDev(g: Game) {
55	  if (!ui.devMode) return;
56	  g.setupDevMode();
57	  // 开发者模式：全图迷雾点亮（小地图/大地图不再有未探索黑区）
58	  g.world.explored.fill(1);
59	  g.world.exploredVersion++; // 使 Renderer 的迷雾缓存失效重建
60	}
61	
62	function quitToMenu() {
63	  inGame = false;
64	  pausePanel = null;
65	  game?.destroy();
66	  game = null;
67	  ui.closeAll();
68	  audio.play('title');
69	  showMenu();
70	}
71	
72	function showMenu() {
73	  audio.play('title');
74	  ui.showMainMenu({
75	    onNew: async (seed, w, h) => {
76	      const g = new Game(root, {
77	        onWorldReady: () => {
78	          ui.hideProgress();
79	          enterGame(g);
80	          maybeDev(g);
81	        },
82	        onInventoryChanged: () => ui.refreshAll(),
83	        onBuffsChanged: () => ui.refreshBuffs(),
84	        onToast: (m) => ui.toast(m),
85	        onDayNight: (isDay) => audio.setDayNight(isDay),
86	      }, atlas);
87	      (window as unknown as { __swGame: Game }).__swGame = g;
88	      (window as unknown as { __swTiles: typeof TILE_BY_KEY }).__swTiles = TILE_BY_KEY;
89	      (window as unknown as { __swItems: typeof ITEM_BY_KEY }).__swItems = ITEM_BY_KEY;
90	  (window as unknown as { __swTiles: typeof TILE_BY_KEY }).__swTiles = TILE_BY_KEY;
91	  (window as unknown as { __swItems: typeof ITEM_BY_KEY }).__swItems = ITEM_BY_KEY;
92	      ui.showProgress('正在生成世界…', 0.05);
93	      await g.newWorld(seed || String(Date.now()), w, h, (label, p) => ui.showProgress(label, p));
94	    },
95	    onLoadFile: async (file) => {
96	      const text = await file.text();
97	      try {
98	        const { world, player } = loadSave(text);
99	        const g = new Game(root, {
100	          onWorldReady: () => { ui.hideProgress(); enterGame(g); },
101	          onInventoryChanged: () => ui.refreshAll(),
102	        onBuffsChanged: () => ui.refreshBuffs(),
103	          onToast: (m) => ui.toast(m),
104	        }, atlas);
105	        ui.showProgress('读取存档…', 0.3);
106	        await g.loadWorld(world, (label, p) => ui.showProgress(label, 0.3 + p * 0.6));
107	        // 恢复玩家状态（旧存档 45 长度 → 补齐到当前 INV_SIZE，防止 UI 越界）
108	        g.player.hp = player.hp;
109	        g.player.x = player.x;
110	        g.player.y = player.y;
111	        g.player.inv.slots = player.inventory.concat(Array(Math.max(0, INV_SIZE - player.inventory.length)).fill(null));
112	        g.player.inv.selected = player.selected;
113	        maybeDev(g);
114	        ui.refreshAll();
115	      } catch (e) {
116	        console.error(e);
117	        alert('存档读取失败：' + (e as Error).message);
118	        showMenu();
119	      }
120	    },
121	    onImportWld: async (file) => {
122	      ui.showProgress('正在解析 .wld 地图…', 0.1);
123	      try {
124	        const buf = new Uint8Array(await file.arrayBuffer());
125	        const { save, report } = parseWldToSave(buf);
126	        (window as unknown as { __lastCompatReport?: import('./ui/UI').CompatReport }).__lastCompatReport = report;
127	        ui.showProgress('正在转换世界…', 0.7);
128	        const g = new Game(root, {
129	          onWorldReady: () => {
130	            ui.hideProgress();
131	            enterGame(g);
132	            maybeDev(g);
133	            ui.toast(`成功导入「${save.header.name}」(v${save.header.wldVersion})`);
134	            // 兼容报告：有降级/跳过内容时弹窗 + 支持导出
135	            const rpt = (window as unknown as { __lastCompatReport?: import('./ui/UI').CompatReport }).__lastCompatReport;
136	            if (rpt && (rpt.tilesDegraded.length || rpt.tilesCleared.length || rpt.itemsSkipped.length)) {
137	              ui.showCompatReport(rpt);
138	            }
139	          },
140	          onInventoryChanged: () => ui.refreshAll(),
141	        onBuffsChanged: () => ui.refreshBuffs(),
142	          onToast: (m) => ui.toast(m),
143	        }, atlas);
144	        const { world } = loadSave(JSON.stringify(save));
145	        await g.loadWorld(world, (label, p) => ui.showProgress(label, 0.7 + p * 0.3));
146	        // wld 导入给基础工具
147	        g.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
148	        g.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
149	        g.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
150	        g.player.inv.add(ITEM_BY_KEY['torch'], 20);
151	      } catch (e) {
152	        console.error(e);
153	        ui.hideProgress();
154	        alert('.wld 导入失败：' + (e as Error).message);
155	        showMenu();
156	      }
157	    },
158	    onQuickLoad: quickSaveExists
159	      ? async () => {
160	          const text = await kvGet(QUICK_SAVE_KEY);
161	          if (!text) return;
162	          const { world, player } = loadSave(text);
163	          const g = new Game(root, {
164	            onWorldReady: () => { ui.hideProgress(); enterGame(g); },
165	            onInventoryChanged: () => ui.refreshAll(),
166	        onBuffsChanged: () => ui.refreshBuffs(),
167	            onToast: (m) => ui.toast(m),
168	          }, atlas);
169	          ui.showProgress('读取存档…', 0.3);
170	          // 必须 await：预沉降完成后 player 才存在（否则恢复状态时 undefined 崩溃）
171	          await g.loadWorld(world, (label, p) => ui.showProgress(label, 0.3 + p * 0.6));
172	          g.player.hp = player.hp;
173	          g.player.x = player.x;
174	          g.player.y = player.y;
175	          g.player.inv.slots = player.inventory.concat(Array(Math.max(0, INV_SIZE - player.inventory.length)).fill(null));
176	          g.player.inv.selected = player.selected;
177	          maybeDev(g);
178	        }
179	      : null,
180	  });
181	}
182	
183	// ---- 键盘：背包/暂停/保存 ----
184	window.addEventListener('keydown', (e) => {
185	  if (!inGame || !game) return;
186	  switch (e.code) {
187	    case 'KeyE':
188	    case 'Escape':
189	      e.preventDefault();
190	      if (game.renderer.fullMap.open) {
191	        game.renderer.fullMap.open = false;
192	        break;
193	      }
194	      if (pausePanel) {
195	        pausePanel.remove();
196	        pausePanel = null;
197	        game.paused = false;
198	        ui.closeInventory();
199	        game.input.uiBlocking = false;
200	      } else if (ui.invPanel && ui.invPanel.style.display === 'block') {
201	        ui.closeInventory();
202	      } else if (e.code === 'Escape') {
203	        game.paused = true;
204	        pausePanel = ui.showPause({
205	          onResume: () => {
206	            pausePanel?.remove();
207	            pausePanel = null;
208	            game!.paused = false;
209	          },
210	          onSave: () => doSave(),
211	          onQuit: () => {
212	            pausePanel = null;
213	            game!.paused = false;
214	            quitToMenu();
215	          },
216	        });
217	      } else {
218	        ui.openInventory();
219	      }
220	      break;
221	    case 'F3':
222	      e.preventDefault();
223	      game.renderer.debugMode = !game.renderer.debugMode;
224	      ui.toast(game.renderer.debugMode ? '调试面板已开启（碰撞盒高亮）' : '调试面板已关闭');
225	      break;
226	    case 'F4':
227	      e.preventDefault();
228	      game.world.explored.fill(1);
229	      game.world.exploredVersion++; // 使迷雾缓存失效重建
230	      ui.toast('已消除全图迷雾');
231	      break;
232	    case 'F5':
233	      e.preventDefault();
234	      toggleAnnotate();
235	      break;
236	    case 'F6':
237	      e.preventDefault();
238	      doSave();
239	      break;
240	    case 'F8':
241	      e.preventDefault();
242	      game.enemySpawnEnabled = !game.enemySpawnEnabled;
243	      ui.toast(game.enemySpawnEnabled ? '怪物生成已开启' : '怪物生成已关闭（已有怪物不受影响）');
244	      break;
245	    case 'F9':
246	      e.preventDefault();
247	      game.renderer.fullbright = !game.renderer.fullbright;
248	      ui.toast(game.renderer.fullbright ? '已开灯：全画面无暗影' : '已关灯：恢复正常光照');
249	      break;
250	    case 'KeyM':
251	      if (game.renderer.fullMap.open) {
252	        game.renderer.fullMap.open = false;
253	      } else {
254	        ui.toast(audio.toggleMute() ? '音乐已关闭' : '音乐已开启');
255	      }
256	      break;
257	  }
258	});
259	
260	function doSave() {
261	  if (!game) return;
262	  const json = saveGame(game.world, game.player, Date.now() - playStart);
263	  // 大地图存档可能超 localStorage 5MB 限制 → 优先 IndexedDB（数百 MB）
264	  const mb = json.length / 1024 / 1024;
265	  kvSet(QUICK_SAVE_KEY, json).then((where) => {
266	    if (where === 'fail') ui.toast('保存失败：存储不可用');
267	    else ui.toast(`已保存（${where === 'idb' ? mb.toFixed(1) + ' MB → IndexedDB' : '本地'}）`);
268	  });
269	}
270	
271	function downloadText(filename: string, text: string) {
272	  const blob = new Blob([text], { type: 'application/json' });
273	  const a = document.createElement('a');
274	  a.href = URL.createObjectURL(blob);
275	  a.download = filename;
276	  a.click();
277	  URL.revokeObjectURL(a.href);
278	}
279	
280	// ---- 方块标注模式（F5）：标记问题方块，导出标注 + 地图给开发者 ----
281	function toggleAnnotate() {
282	  if (!game) return;
283	  game.annotateMode = !game.annotateMode;
284	  if (game.annotateMode) {
285	    ui.showAnnotatePanel({
286	      onExportMarks: exportMarks,
287	      onExportMap: exportMap,
288	      onClear: () => {
289	        if (!game) return;
290	        game.marks = [];
291	        ui.updateAnnotateCount(0);
292	      },
293	      onClose: () => toggleAnnotate(),
294	      onToggleFix: () => {
295	        if (!game) return;
296	        game.fixTexMode = !game.fixTexMode;
297	        ui.setFixModeLabel(game.fixTexMode);
298	        ui.toast(game.fixTexMode ? '贴图纠错模式：点击方块打开其贴图表' : '已关闭贴图纠错模式');
299	      },
300	      onExportFixes: exportTexFixes,
301	    });
302	    ui.updateAnnotateCount(game.marks.length);
303	    ui.toast('标注模式已开启：点击方块标记，F5 关闭');
304	  } else {
305	    ui.closeAnnotatePanel();
306	    ui.toast('标注模式已关闭');
307	  }
308	}
309	
310	function exportMarks() {
311	  if (!game) return;
312	  const g = game;
313	  const st = g.world.store;
314	  const marks = g.marks.map((m, i) => {
315	    const idx = st.idx(m.x, m.y);
316	    const t = st.type[idx];
317	    const def = TILE_DEFS[t];
318	    // 诊断增强：8 邻居（类型+帧）、液体、贴图表尺寸与帧越界检测
319	    const nb: Record<string, { key: string | null; fx: number; fy: number } | null> = {};
320	    const dirs: Array<[string, number, number]> = [['n', 0, -1], ['s', 0, 1], ['w', -1, 0], ['e', 1, 0],
321	      ['nw', -1, -1], ['ne', 1, -1], ['sw', -1, 1], ['se', 1, 1]];
322	    for (const [tag, dx, dy] of dirs) {
323	      const nx = m.x + dx, ny = m.y + dy;
324	      if (!st.inBounds(nx, ny)) { nb[tag] = null; continue; }
325	      const ni = st.idx(nx, ny);
326	      const nt = st.type[ni];
327	      nb[tag] = nt === 0 ? null : { key: TILE_DEFS[nt]?.key ?? String(nt), fx: st.frameX[ni], fy: st.frameY[ni] };
328	    }
329	    // 贴图表元数据 + 越界检测（style 帧超出 PNG = 素材包版本旧）
330	    let sheetInfo: { sheet: number; name: string; png: string; oob: boolean } | null = null;
331	    const sheetId = def?.vanilla?.sheet;
332	    if (sheetId !== undefined && g.renderer.atlas) {
333	      const meta = g.renderer.atlas.vmeta(sheetId);
334	      const img = meta ? g.renderer.atlas.vimages.get(meta.sheet) : null;
335	      if (meta && img) {
336	        const oob = def!.vanilla!.frame === 'style'
337	          && (st.frameX[idx] + meta.grid[0] > img.width || st.frameY[idx] + meta.grid[1] > img.height);
338	        sheetInfo = { sheet: sheetId, name: meta.name, png: `${img.width}×${img.height}`, oob };
339	      }
340	    }
341	    return {
342	      no: i + 1, x: m.x, y: m.y,
343	      typeId: t, typeKey: def?.key ?? null, typeName: def?.name ?? null,
344	      frameX: st.frameX[idx], frameY: st.frameY[idx],
345	      wall: st.wall[idx],
346	      liquid: st.liquid[idx], liquidType: st.liquidType[idx],
347	      wallName: WALL_DEFS[st.wall[idx]]?.name ?? null,
348	      neighbors: nb, sheetInfo,
349	    };
350	  });
351	  const out = {
352	    worldName: g.world.name, size: [g.world.w, g.world.h],
353	    player: { x: Math.floor(g.player.x / 16), y: Math.floor(g.player.y / 16) },
354	    exportedAt: new Date().toISOString(),
355	    marks,
356	  };
357	  downloadText(`marks-${g.world.name.replace(/\s+/g, '_')}.json`, JSON.stringify(out, null, 2));
358	  ui.toast(`已导出 ${marks.length} 处标注`);
359	}
360	
361	function exportMap() {
362	  if (!game) return;
363	  const json = saveGame(game.world, game.player, Date.now() - playStart);
364	  downloadText(`map-${game.world.name.replace(/\s+/g, '_')}.json`, json);
365	  ui.toast('已导出地图存档');
366	}
367	
368	function exportTexFixes() {
369	  if (!game) return;
370	  const fixes = ui.texFixes;
371	  if (!fixes.length) { ui.toast('还没有记录任何贴图纠错'); return; }
372	  const out = {
373	    worldName: game.world.name, size: [game.world.w, game.world.h],
374	    exportedAt: new Date().toISOString(),
375	    note: '每条 = 地图坐标处应使用的正确帧偏移（对应 Tiles_N 表的像素偏移）',
376	    fixes,
377	  };
378	  downloadText(`texfix-${game.world.name.replace(/\s+/g, '_')}.json`, JSON.stringify(out, null, 2));
379	  ui.toast(`已导出 ${fixes.length} 处贴图纠错`);
380	}
381	
382	// 暴露 tile/key 常量给调试控制台
383	void TILE_BY_KEY; void T;
384	void game;
385	
386	// 快速存档存在性（IndexedDB 异步）——查完再进菜单
387	let quickSaveExists = false;
388	kvHas(QUICK_SAVE_KEY).then((v) => {
389	  quickSaveExists = v;
390	  return loadAssets();
391	}).then(() => showMenu());
392	
393	// 供 showMenu 引用的存在性（初次菜单在 Promise 完成后才弹出，值已就绪）
394	void 0;
395	

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:18.320Z

**📎 ToolResult**

```
1	// DOM overlay UI：主菜单 / HUD 快捷栏 / 背包+配饰栏 / 合成 / 宝箱 / Buff栏 / 暂停 / Tooltip / Toast
2	import type { Game } from '../core/Game';
3	import { ITEM_DEFS, ITEM_BY_KEY } from '../data/items';
4	import { TILE_DEFS } from '../data/tiles';
5	import { autoFrameAt, cactusFrameAt, cactusTextureFor } from '../render/VanillaTiler';
6	import { RECIPES } from '../data/recipes';
7	import { atlasIconForKey } from '../assets/SpriteAtlas';
8	import { BuffType, BUFF_DEFS } from '../stats/Buffs';
9	import { ACCESSORY_START, ARMOR_START, COIN_START, INV_SIZE, VANITY_START } from '../items/Inventory';
10	import type { ChestData } from '../world/World';
11	
12	const iconCache = new Map<number, string>();
13	function iconUrl(game: Game, id: number): string {
14	  let url = iconCache.get(id);
15	  if (!url) {
16	    // 优先 Maples 素材图标（合成 32×32 dataURL）
17	    const def = ITEM_DEFS[id];
18	    if (game.atlas && def) {
19	      const ar = atlasIconForKey(game.atlas, def.key);
20	      if (ar) {
21	        const c = document.createElement('canvas');
22	        c.width = 32; c.height = 32;
23	        const cx = c.getContext('2d')!;
24	        cx.imageSmoothingEnabled = false;
25	        const s = Math.min(32 / ar.sw, 32 / ar.sh);
26	        const w = ar.sw * s, h = ar.sh * s;
27	        cx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, (32 - w) / 2, (32 - h) / 2, w, h);
28	        url = c.toDataURL();
29	        iconCache.set(id, url);
30	        return url;
31	      }
32	    }
33	    const c = game.assets.itemIcons.get(id);
34	    url = c ? c.toDataURL() : '';
35	    iconCache.set(id, url);
36	  }
37	  return url;
38	}
39	
40	function el<K extends keyof HTMLElementTagNameMap>(tag: K, cls?: string, text?: string): HTMLElementTagNameMap[K] {
41	  const e = document.createElement(tag);
42	  if (cls) e.className = cls;
43	  if (text !== undefined) e.textContent = text;
44	  return e;
45	}
46	
47	const CSS = `
48	.sw-root { position:fixed; inset:0; pointer-events:none; font-family:inherit; z-index:10; }
49	/* ---- 原版风格：深蓝面板 + 浅蓝描边 ---- */
50	.sw-panel { pointer-events:auto;
51	  background:linear-gradient(rgba(38,50,90,0.96), rgba(22,30,58,0.97));
52	  border:2px solid #7d92d6; border-radius:6px; color:#e8ecf8; padding:12px;
53	  box-shadow:0 0 0 2px rgba(10,14,30,0.8), 0 6px 28px rgba(0,0,0,0.65),
54	    inset 0 0 18px rgba(90,120,220,0.12); }
55	.sw-btn { pointer-events:auto; display:block; width:100%; margin:6px 0; padding:10px 16px;
56	  background:linear-gradient(#4a3a6a,#3a2a5a); color:#fff; border:1px solid #6a5a8a;
57	  border-radius:6px; cursor:pointer; font-size:15px; text-align:center; }
58	.sw-btn:hover { background:linear-gradient(#5a4a7e,#4a3a6e); }
59	.sw-btn:disabled { opacity:0.45; cursor:default; }
60	.sw-slot { pointer-events:auto; width:44px; height:44px; background:rgba(24,34,70,0.9);
61	  border:2px solid #4d5f9e; border-radius:4px; position:relative; cursor:pointer; }
62	.sw-slot:hover { border-color:#aebfe8; background:rgba(40,56,110,0.95); }
63	.sw-slot.sel { border-color:#ffd75a; box-shadow:0 0 8px rgba(255,215,90,0.5); }
64	.sw-slot img { position:absolute; inset:4px; width:36px; height:36px; image-rendering:pixelated; }
65	.sw-slot .cnt { position:absolute; right:3px; bottom:1px; font-size:12px; font-weight:bold; color:#fff;
66	  text-shadow:1px 1px 0 #000; }
67	.sw-slot.trash::after { content:'🗑'; position:absolute; left:50%; top:50%;
68	  transform:translate(-50%,-52%); font-size:18px; opacity:0.55; pointer-events:none; }
69	.sw-slot.trash:hover { border-color:#e08a8a; }
70	.sw-lbl { font-size:12px; color:#9fb0dd; margin:6px 0 2px 0; }
71	.sw-title { font-size:17px; font-weight:bold; margin-bottom:8px; color:#ffe8a0; }
72	.sw-drag-ghost { position:fixed; z-index:200; pointer-events:none; width:40px; height:40px; }
73	.sw-drag-ghost img { width:40px; height:40px; image-rendering:pixelated;
74	  filter:drop-shadow(2px 3px 2px rgba(0,0,0,0.6)); }
75	.sw-drag-ghost .cnt { position:absolute; right:-2px; bottom:-4px; font-size:12px; font-weight:bold;
76	  color:#fff; text-shadow:1px 1px 0 #000; }
77	.sw-drop-ok { border-color:#7de08a !important; }
78	.sw-toast { position:fixed; left:50%; top:64px; transform:translateX(-50%);
79	  background:rgba(20,16,28,0.9); color:#ffe8a0; padding:8px 18px; border-radius:6px;
80	  border:1px solid #6a5a8a; font-size:14px; transition:opacity 0.4s; pointer-events:none; }
81	.sw-tooltip { position:fixed; background:rgba(10,8,16,0.95); border:1px solid #6a5a8a; border-radius:4px;
82	  padding:6px 10px; color:#e8e4f0; font-size:13px; pointer-events:none; z-index:100; max-width:260px; }
83	.sw-buff { pointer-events:auto; position:relative; width:30px; height:30px; background:rgba(40,32,60,0.9);
84	  border:1px solid #6a5a8a; border-radius:4px; align-items:center; justify-content:center; }
85	.sw-recipe { pointer-events:auto; display:flex; align-items:center; gap:6px; padding:5px 8px; margin:3px 0;
86	  background:rgba(50,40,70,0.8); border-radius:4px; cursor:pointer; font-size:13px; }
87	.sw-recipe:hover { background:rgba(70,55,100,0.9); }
88	.sw-recipe.no { opacity:0.4; cursor:default; }
89	.sw-recipe img { width:22px; height:22px; image-rendering:pixelated; }
90	.sw-progress { position:fixed; inset:0; background:rgba(5,5,12,0.85); display:flex;
91	  flex-direction:column; align-items:center; justify-content:center; color:#e8e4f0; }
92	.sw-progress .bar { width:320px; height:14px; background:#2a2440; border:1px solid #6a5a8a; border-radius:7px; margin-top:14px; overflow:hidden; }
93	.sw-progress .fill { height:100%; width:0%; background:linear-gradient(90deg,#6a8ae0,#8ad0e0); transition:width 0.2s; }
94	`;
95	
96	export interface CompatEntry { id: number; name: string | null; count: number; action: string }
97	export interface CompatReport {
98	  worldName: string; wldVersion: number; size: [number, number];
99	  tilesDegraded: CompatEntry[]; tilesCleared: CompatEntry[]; itemsSkipped: CompatEntry[];
100	}
101	
102	export class UI {
103	  devMode = false; // 开发者模式：进世界时全道具入包 + 出生点展示区
104	  root: HTMLElement;
105	  game!: Game;
106	  hotbarEl!: HTMLElement;
107	  invPanel!: HTMLElement;
108	  chestPanel!: HTMLElement;
109	  craftListEl!: HTMLElement;
110	  tooltip!: HTMLElement;
111	  toastEl: HTMLElement | null = null;
112	  heldStack: { id: number; stack: number } | null = null;
113	  heldFrom: 'inv' | 'chest' = 'inv';
114	  openChest: ChestData | null = null;
115	  private toastTimer: number | null = null;
116	
117	  constructor(parent: HTMLElement) {
118	    const style = el('style');
119	    style.textContent = CSS;
120	    document.head.appendChild(style);
121	    this.root = el('div', 'sw-root');
122	    parent.appendChild(this.root);
123	    this.installDragListeners();
124	    (window as unknown as { __swUI?: UI }).__swUI = this; // 调试句柄
125	  }
126	
127	  private slotContent(where: 'inv' | 'chest', i: number): { id: number; stack: number } | null {
128	    if (where === 'inv') return this.game.player.inv.slots[i];
129	    return this.openChest?.items[i] ?? null;
130	  }
131	
132	  // ============ 主菜单 ============
133	  showMainMenu(handlers: {
134	    onNew: (seed: string, w: number, h: number) => void;
135	    onLoadFile: (file: File) => void;
136	    onImportWld: (file: File) => void;
137	    onQuickLoad: (() => void) | null;
138	  }) {
139	    this.closeAll();
140	    const panel = el('div', 'sw-panel');
141	    panel.style.cssText = 'pointer-events:auto; position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); width:340px;';
142	    panel.appendChild(el('div', 'sw-title', '🌍 SandboxWorld'));
143	    const sub = el('div', '', '2D 沙盒动作冒险 · 泰拉瑞亚风格复刻');
144	    sub.style.cssText = 'font-size:12px; color:#9a8ab8; margin-bottom:10px;';
145	    panel.appendChild(sub);
146	
147	    const seedInput = el('input') as HTMLInputElement;
148	    seedInput.placeholder = '世界种子（留空随机）';
149	    seedInput.style.cssText = 'width:100%; padding:8px; margin:4px 0; background:#241e38; color:#fff; border:1px solid #6a5a8a; border-radius:4px; box-sizing:border-box;';
150	    panel.appendChild(seedInput);
151	
152	    const sizeSel = el('select') as HTMLSelectElement;
153	    sizeSel.style.cssText = 'width:100%; padding:8px; margin:4px 0; background:#241e38; color:#fff; border:1px solid #6a5a8a; border-radius:4px;';
154	    for (const [label, w, h] of [['小世界 4200×1200', 4200, 1200], ['中世界 6400×1800', 6400, 1800], ['大世界 8400×2400', 8400, 2400]] as const) {
155	      const o = el('option', '', label);
156	      o.value = `${w}x${h}`;
157	      sizeSel.appendChild(o);
158	    }
159	    sizeSel.selectedIndex = 1;
160	    panel.appendChild(sizeSel);
161	
162	    const bNew = el('button', 'sw-btn', '创建新世界');
163	    bNew.onclick = () => {
164	      const [w, h] = sizeSel.value.split('x').map(Number);
165	      panel.remove();
166	      handlers.onNew(seedInput.value.trim(), w, h);
167	    };
168	    panel.appendChild(bNew);
169	
170	    const bQuick = el('button', 'sw-btn', '继续上次存档');
171	    bQuick.onclick = () => { panel.remove(); handlers.onQuickLoad?.(); };
172	    bQuick.disabled = !handlers.onQuickLoad;
173	    panel.appendChild(bQuick);
174	
175	    const fileWrap = el('div');
176	    const bLoad = el('button', 'sw-btn', '读取存档文件…');
177	    const fileInput = el('input') as HTMLInputElement;
178	    fileInput.type = 'file';
179	    fileInput.accept = '.json';
180	    fileInput.style.display = 'none';
181	    fileInput.onchange = () => {
182	      if (fileInput.files?.[0]) { panel.remove(); handlers.onLoadFile(fileInput.files[0]); }
183	    };
184	    bLoad.onclick = () => fileInput.click();
185	    fileWrap.appendChild(bLoad);
186	    fileWrap.appendChild(fileInput);
187	    panel.appendChild(fileWrap);
188	
189	    const wldWrap = el('div');
190	    const bWld = el('button', 'sw-btn', '导入泰拉瑞亚地图 (.wld)…');
191	    const wldInput = el('input') as HTMLInputElement;
192	    wldInput.type = 'file';
193	    wldInput.accept = '.wld';
194	    wldInput.style.display = 'none';
195	    wldInput.onchange = () => {
196	      if (wldInput.files?.[0]) { panel.remove(); handlers.onImportWld(wldInput.files[0]); }
197	    };
198	    bWld.onclick = () => wldInput.click();
199	    wldWrap.appendChild(bWld);
200	    wldWrap.appendChild(wldInput);
201	    panel.appendChild(wldWrap);
202	
203	    // 开发者模式开关：进世界时全道具入包 + 出生点摆放全部可放置图块
204	    const devRow = el('div');
205	    devRow.style.cssText = 'display:flex; align-items:center; gap:6px; margin-top:8px; font-size:12px; color:#9a8ab8;';
206	    const devCb = el('input') as HTMLInputElement;
207	    devCb.type = 'checkbox';
208	    devCb.checked = this.devMode;
209	    devCb.onchange = () => { this.devMode = devCb.checked; };
210	    devRow.appendChild(devCb);
211	    devRow.appendChild(el('span', '', '开发者模式（全道具入包 + 出生点展示区）'));
212	    panel.appendChild(devRow);
213	
214	    this.root.appendChild(panel);
215	  }
216	
217	  /** 兼容报告弹窗：降级/清空/跳过内容列表 + 导出详情 JSON */
218	  showCompatReport(rpt: CompatReport) {
219	    // 不 closeAll：会把已初始化的 HUD（快捷栏等）一起拆掉，报告只叠加一层
220	    const panel = el('div', 'sw-panel');
221	    panel.style.cssText = 'pointer-events:auto; position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); width:480px; max-height:80vh; overflow:auto;';
222	    panel.appendChild(el('div', 'sw-title', '⚠ 导入兼容报告'));
223	    const info = el('div', '', `「${rpt.worldName}」 v${rpt.wldVersion} · ${rpt.size[0]}×${rpt.size[1]}<br>以下内容在本版本中被降级或跳过：`);
224	    info.style.cssText = 'font-size:12px; color:#9a8ab8; margin-bottom:8px;';
225	    panel.appendChild(info);
226	    const section = (title: string, entries: CompatEntry[], desc: string) => {
227	      if (!entries.length) return;
228	      panel.appendChild(el('div', '', title));
229	      const ul = el('div');
230	      ul.style.cssText = 'font-size:12px; margin:4px 0 8px 0; line-height:1.7;';
231	      for (const e of entries.slice(0, 40)) {
232	        ul.appendChild(el('div', '', `· id ${e.id} ${e.name ? `「${e.name}」` : ''} ×${e.count} <span style="color:#7a6a9a">(${desc})</span>`));
233	      }
234	      if (entries.length > 40) ul.appendChild(el('div', '', `… 共 ${entries.length} 种（导出查看全部）`));
235	      panel.appendChild(ul);
236	    };
237	    section('🧱 方块 → 降级为石块', rpt.tilesDegraded, 'degraded-to-stone');
238	    section('🚫 方块 → 清空丢弃', rpt.tilesCleared, 'cleared');
239	    section('🎒 宝箱物品 → 跳过', rpt.itemsSkipped, 'skipped');
240	    const row = el('div');
241	    row.style.cssText = 'display:flex; gap:8px; margin-top:8px;';
242	    const bExport = el('button', 'sw-btn', '导出详情 JSON');
243	    bExport.style.flex = '1';
244	    bExport.onclick = () => {
245	      const blob = new Blob([JSON.stringify({ ...rpt, exportedAt: new Date().toISOString(), note: '把此文件交回开发者即可补全缺失内容' }, null, 2)], { type: 'application/json' });
246	      const a = document.createElement('a');
247	      a.href = URL.createObjectURL(blob);
248	      a.download = `compat-report-${rpt.worldName.replace(/\s+/g, '_')}-${rpt.wldVersion}.json`;
249	      a.click();
250	      URL.revokeObjectURL(a.href);
251	    };
252	    const bClose = el('button', 'sw-btn', '关闭');
253	    bClose.style.flex = '1';
254	    bClose.onclick = () => panel.remove();
255	    row.appendChild(bExport);
256	    row.appendChild(bClose);
257	    panel.appendChild(row);
258	    this.root.appendChild(panel);
259	  }
260	
261	  /** 方块标注面板（F5 标注模式）：下载标注 / 下载地图 / 贴图纠错 / 清空 */
262	  annotatePanel: HTMLElement | null = null;
263	  texFixes: Array<{ x: number; y: number; typeKey: string; sheet: number; frameX: number; frameY: number }> = [];
264	  private fixModeBtn: HTMLButtonElement | null = null;
265	  private fixesCountEl: HTMLElement | null = null;
266	  showAnnotatePanel(handlers: {
267	    onExportMarks: () => void;
268	    onExportMap: () => void;
269	    onClear: () => void;
270	    onClose: () => void;
271	    onToggleFix: () => void;
272	    onExportFixes: () => void;
273	  }) {
274	    this.closeAnnotatePanel();
275	    const panel = el('div', 'sw-panel');
276	    panel.style.cssText = 'pointer-events:auto; position:fixed; left:14px; top:90px; width:200px; padding:10px;';
277	    panel.appendChild(el('div', 'sw-title', '📍 方块标注模式'));
278	    const hint = el('div', '', '点击方块标记/取消，导出后发给开发者');
279	    hint.style.cssText = 'font-size:11px; color:#9fb0dd; margin-bottom:6px;';
280	    panel.appendChild(hint);
281	    this.annotateCountEl = el('div', '', '已标记：0 处');
282	    this.annotateCountEl.style.cssText = 'font-size:12px; color:#ffe8a0; margin-bottom:6px;';
283	    panel.appendChild(this.annotateCountEl);
284	    this.fixesCountEl = el('div', '', '贴图纠错：0 处');
285	    this.fixesCountEl.style.cssText = 'font-size:12px; color:#8ad0a0; margin-bottom:6px;';
286	    panel.appendChild(this.fixesCountEl);
287	    const mk = (label: string, fn: () => void) => {
288	      const b = el('button', 'sw-btn', label);
289	      b.style.margin = '4px 0';
290	      b.onclick = fn;
291	      panel.appendChild(b);
292	      return b;
293	    };
294	    mk('⬇ 下载标注 JSON', handlers.onExportMarks);
295	    mk('⬇ 下载地图存档', handlers.onExportMap);
296	    this.fixModeBtn = mk('🔧 贴图纠错模式：关', handlers.onToggleFix) as HTMLButtonElement;
297	    mk('⬇ 下载贴图纠错', handlers.onExportFixes);
298	    mk('🗑 清空标注', handlers.onClear);
299	    mk('✕ 关闭（再按 F5）', handlers.onClose);
300	    this.annotatePanel = panel;
301	    this.root.appendChild(panel);
302	  }
303	
304	  setFixModeLabel(on: boolean) {
305	    if (this.fixModeBtn) this.fixModeBtn.textContent = `🔧 贴图纠错模式：${on ? '开' : '关'}`;
306	  }
307	
308	  updateFixesCount(n: number) {
309	    if (this.fixesCountEl) this.fixesCountEl.textContent = `贴图纠错：${n} 处`;
310	  }
311	
312	  /** 贴图纠错：点击方块后弹出该图块的完整原版贴图表，选正确帧 */
313	  openTexPicker(tx: number, ty: number) {
314	    this.closeTexPicker();
315	    const g = this.game;
316	    const st = g.world.store;
317	    if (!st.inBounds(tx, ty)) return;
318	    const i = st.idx(tx, ty);
319	    const t = st.type[i];
320	    const def = TILE_DEFS[t];
321	    const sheetId = def?.vanilla?.sheet;
322	    if (sheetId === undefined) { this.toast('该图块没有原版贴图表'); return; }
323	    const atlas = g.renderer.atlas;
324	    const meta = atlas ? atlas.vmeta(sheetId) : null;
325	    if (!atlas || !meta) { this.toast('贴图表加载失败'); return; }
326	    // 实际渲染用的贴图：仙人掌按生物群系换变体（腐化/猩红/神圣）
327	    let img: HTMLImageElement | null = atlas.vimages.get(meta.sheet) ?? null;
328	    if (sheetId === 80) img = cactusTextureFor(atlas, st, tx, ty) ?? img;
329	    if (!img) { this.toast('贴图表加载失败'); return; }
330	    // 当前实际渲染帧：
331	    // - auto 类不存储帧 → 渲染端同一查找表现算
332	    // - 仙人掌不存储帧 → 列角色判定现算
333	    // - 其余 style 类 → 存储帧
334	    let curCol: number, curRow: number;
335	    let autoNote = '';
336	    if (sheetId === 80) {
337	      const f = cactusFrameAt(st, tx, ty, t);
338	      curCol = f.col; curRow = f.row;
339	      autoNote = '（仙人掌：列角色现算）';
340	    } else if (def.vanilla!.frame === 'auto') {
341	      const f = autoFrameAt(st, tx, ty, t);
342	      curCol = f.col; curRow = f.row;
343	      autoNote = '（auto 分帧：按邻居现算）';
344	    } else {
345	      curCol = Math.floor(st.frameX[i] / meta.stride[0]);
346	      curRow = Math.floor(st.frameY[i] / meta.stride[1]);
347	    }
348	    const panel = el('div', 'sw-panel sw-texpicker');
349	    panel.style.cssText = 'pointer-events:auto; position:fixed; right:14px; top:60px; width:420px; max-height:86vh; overflow:auto; padding:10px;';
350	    panel.appendChild(el('div', 'sw-title', `🔧 纠错 (${tx}, ${ty})`));
351	    const info = el('div', '', `${def.key} · sheet ${sheetId} · 当前帧 第${curCol}列 第${curRow}行${autoNote} · 网格 ${meta.grid}×${meta.stride}`);
352	    info.style.cssText = 'font-size:11px; color:#9fb0dd; margin-bottom:6px;';
353	    panel.appendChild(info);
354	
355	    const scale = Math.max(2, Math.min(4, Math.floor(400 / Math.max(1, meta.stride[0]))));
356	    const cv = document.createElement('canvas');
357	    cv.width = img.width * scale; cv.height = img.height * scale;
358	    cv.style.cssText = `image-rendering:pixelated; border:1px solid #4d5f9e; cursor:crosshair;`;
359	    // 可双向滚动的视口（大表不压缩，保持可读比例）
360	    const viewport = el('div');
361	    viewport.style.cssText = 'overflow:auto; max-height:56vh; border-radius:4px;';
362	    viewport.appendChild(cv);
363	    const cx = cv.getContext('2d')!;
364	    cx.imageSmoothingEnabled = false;
365	    let sel: { col: number; row: number } | null = { col: curCol, row: curRow };
366	    const redraw = () => {
367	      cx.drawImage(img, 0, 0, cv.width, cv.height);
368	      // 网格
369	      cx.strokeStyle = 'rgba(160,180,255,0.25)';
370	      cx.lineWidth = 1;
371	      for (let x = 0; x <= img.width; x += meta.stride[0]) {
372	        cx.beginPath(); cx.moveTo(x * scale + 0.5, 0); cx.lineTo(x * scale + 0.5, cv.height); cx.stroke();
373	      }
374	      for (let y = 0; y <= img.height; y += meta.stride[1]) {
375	        cx.beginPath(); cx.moveTo(0, y * scale + 0.5); cx.lineTo(cv.width, y * scale + 0.5); cx.stroke();
376	      }
377	      // 选中帧高亮（绿）
378	      if (sel) {
379	        cx.strokeStyle = '#40FF80'; cx.lineWidth = 2;
380	        cx.strokeRect(sel.col * meta.stride[0] * scale, sel.row * meta.stride[1] * scale, meta.grid[0] * scale, meta.grid[1] * scale);
381	      }
382	    };
383	    redraw();
384	    cv.addEventListener('mousedown', (e) => {
385	      e.stopPropagation();
386	      const r = cv.getBoundingClientRect();
387	      const px = (e.clientX - r.left) * (cv.width / r.width);
388	      const py = (e.clientY - r.top) * (cv.height / r.height);
389	      sel = { col: Math.floor(px / scale / meta.stride[0]), row: Math.floor(py / scale / meta.stride[1]) };
390	      redraw();
391	      selInfo.textContent = `选中：第 ${sel.col} 列 第 ${sel.row} 行 → 像素偏移 (${sel.col * meta.stride[0]}, ${sel.row * meta.stride[1]})`;
392	    });
393	    panel.appendChild(viewport);
394	    const selInfo = el('div', '', '');
395	    selInfo.style.cssText = 'font-size:11px; color:#40FF80; margin:6px 0; min-height:14px;';
396	    if (sel) selInfo.textContent = `当前（已预选）：第 ${sel.col} 列 第 ${sel.row} 行 → 像素偏移 (${sel.col * meta.stride[0]}, ${sel.row * meta.stride[1]})`;
397	    panel.appendChild(selInfo);
398	    // 滚动定位到预选帧（视口中部）
399	    requestAnimationFrame(() => {
400	      if (sel) {
401	        viewport.scrollTop = Math.max(0, sel.row * meta.stride[1] * scale - viewport.clientHeight / 3);
402	        viewport.scrollLeft = Math.max(0, sel.col * meta.stride[0] * scale - viewport.clientWidth / 3);
403	      }
404	    });
405	    const mk2 = (label: string, fn: () => void) => {
406	      const b = el('button', 'sw-btn', label);
407	      b.style.margin = '4px 0';
408	      b.onclick = fn;
409	      panel.appendChild(b);
410	    };
411	    mk2('✓ 记录此纠错', () => {
412	      if (!sel) { this.toast('先在表上点选一帧'); return; }
413	      // 单选：只保留一条纠错记录，新的覆盖旧的
414	      this.texFixes = [{
415	        x: tx, y: ty, typeKey: def.key, sheet: sheetId,
416	        frameX: sel!.col * meta.stride[0], frameY: sel!.row * meta.stride[1],
417	      }];
418	      this.updateFixesCount(this.texFixes.length);
419	      this.toast(`已记录纠错：(${tx},${ty}) → (${sel!.col},${sel!.row})`);
420	      this.closeTexPicker();
421	    });
422	    mk2('✕ 取消', () => this.closeTexPicker());
423	    this.texPickerPanel = panel;
424	    this.root.appendChild(panel);
425	  }
426	
427	  private texPickerPanel: HTMLElement | null = null;
428	  closeTexPicker() {
429	    this.texPickerPanel?.remove();
430	    this.texPickerPanel = null;
431	  }
432	
433	  private annotateCountEl: HTMLElement | null = null;
434	  updateAnnotateCount(n: number) {
435	    if (this.annotateCountEl) this.annotateCountEl.textContent = `已标记：${n} 处`;
436	  }
437	
438	  closeAnnotatePanel() {
439	    this.annotatePanel?.remove();
440	    this.annotatePanel = null;
441	    this.annotateCountEl = null;
442	    this.fixModeBtn = null;
443	    this.fixesCountEl = null;
444	    this.closeTexPicker();
445	  }
446	
447	  showProgress(label: string, p: number) {
448	    let prog = this.root.querySelector('.sw-progress') as HTMLElement | null;
449	    if (!prog) {
450	      prog = el('div', 'sw-progress');
451	      prog.appendChild(el('div', '', label));
452	      const bar = el('div', 'bar');
453	      bar.appendChild(el('div', 'fill'));
454	      prog.appendChild(bar);
455	      this.root.appendChild(prog);
456	    }
457	    prog.children[0].textContent = label;
458	    (prog.querySelector('.fill') as HTMLElement).style.width = `${Math.round(p * 100)}%`;
459	  }
460	
461	  hideProgress() {
462	    this.root.querySelector('.sw-progress')?.remove();
463	  }
464	
465	  // ============ HUD ============
466	
467	  buildHud(game: Game) {
468	    this.game = game;
469	    // 快捷栏
470	    this.hotbarEl = el('div');
471	    this.hotbarEl.style.cssText = 'pointer-events:auto; position:fixed; bottom:12px; left:50%; transform:translateX(-50%); display:flex; gap:5px;';
472	    for (let i = 0; i < 10; i++) {
473	      this.hotbarEl.appendChild(this.makeSlotEl(i, 'inv'));
474	    }
475	    this.root.appendChild(this.hotbarEl);
476	    this.refreshHotbar();
477	
478	    // Tooltip
479	    this.tooltip = el('div', 'sw-tooltip');
480	    this.tooltip.style.display = 'none';
481	    this.root.appendChild(this.tooltip);
482	
483	    // 背包入口按钮（#12）
484	    const bag = el('button', 'sw-btn', '🎒 背包 (E)');
485	    bag.style.cssText = 'pointer-events:auto; position:fixed; right:14px; bottom:14px; width:auto; margin:0; font-size:14px; z-index:11;';
486	    bag.onclick = (ev) => {
487	      ev.stopPropagation();
488	      if (this.invPanel.style.display === 'block') this.closeInventory();
489	      else this.openInventory();
490	    };
491	    this.root.appendChild(bag);
492	
493	    game.openChest = (c) => this.openChestPanel(c);
494	  }
495	
496	  slotEl(i: number, where: 'inv' | 'chest'): HTMLElement {
497	    // 背包格（idx>=10）在背包面板里，快捷栏格在 HUD 上——全文档查
498	    const found = document.querySelector(`[data-idx="${i}"][data-where="${where}"]`);
499	    return found as HTMLElement;
500	  }
501	
502	  private makeSlotEl(i: number, where: 'inv' | 'chest'): HTMLElement {
503	    const s = el('div', 'sw-slot');
504	    s.dataset.idx = String(i);
505	    s.dataset.where = where;
506	    s.addEventListener('mousedown', (e) => {
507	      e.stopPropagation();
508	      e.preventDefault();
509	      if (e.button === 2) {
510	        this.splitHalf(i, where);
511	      } else {
512	        this.dragFrom = { i, where, sx: e.clientX, sy: e.clientY };
513	      }
514	    });
515	    s.addEventListener('mouseenter', () => this.showTooltipFor(i, where));
516	    s.addEventListener('mouseleave', () => (this.tooltip.style.display = 'none'));
517	    s.addEventListener('contextmenu', (e) => e.preventDefault());
518	    return s;
519	  }
520	
521	  // ---- 拖拽系统：按下起点 + 光标持有物（ghost 跟随） ----
522	  private dragFrom: { i: number; where: 'inv' | 'chest'; sx: number; sy: number } | null = null;
523	  private ghostEl: HTMLElement | null = null;
524	  private mouseX = 0; private mouseY = 0;
525	
526	  private installDragListeners() {
527	    // 点击面板外的世界区域：光标持有物直接丢出（原版行为）
528	    document.addEventListener('mousedown', (e) => {
529	      if (!this.heldStack) return;
530	      const t = e.target as HTMLElement | null;
531	      if (t?.closest?.('.sw-slot') || t?.closest?.('.sw-panel') || t?.closest?.('.sw-btn')) return;
532	      this.throwHeldToWorld();
533	      this.refreshAll();
534	    });
535	    document.addEventListener('mousemove', (e) => {
536	      this.mouseX = e.clientX; this.mouseY = e.clientY;
537	      this.moveGhost();
538	      // 未持有物品时按下并移动 >4px → 整叠拾取开始拖拽
539	      if (this.dragFrom && !this.heldStack) {
540	        const d = Math.hypot(e.clientX - this.dragFrom.sx, e.clientY - this.dragFrom.sy);
541	        if (d > 4) this.pickUp(this.dragFrom.i, this.dragFrom.where);
542	      }
543	    });
544	    document.addEventListener('mouseup', (e) => {
545	      if (!this.dragFrom) return;
546	      const from = this.dragFrom;
547	      this.dragFrom = null;
548	      if (e.button !== 0) return;
549	      if (this.heldStack) {
550	        this.resolveDrop(from);
551	      } else {
552	        // 无拖动的普通点击：快捷栏（面板关）选中；否则拾取到光标（点击移动仍可用）
553	        const panelOpen = this.invPanel && this.invPanel.style.display === 'block';
554	        if (from.where === 'inv' && from.i < 10 && !panelOpen) {
555	          this.game.player.inv.selected = from.i;
556	          this.refreshHotbar();
557	        } else {
558	          this.pickUp(from.i, from.where);
559	        }
560	      }
561	      this.refreshAll();
562	    });
563	  }
564	
565	  /** 整叠拾取到光标 */
566	  private pickUp(i: number, where: 'inv' | 'chest') {
567	    const cur = this.slotContent(where, i);
568	    if (!cur) return;
569	    if (this.heldStack && this.heldStack.id !== cur.id) return;
570	    if (where === 'inv') this.game.player.inv.slots[i] = null;
571	    else if (this.openChest) this.openChest.items[i] = null;
572	    if (this.heldStack) this.heldStack.stack += cur.stack;
573	    else this.heldStack = { id: cur.id, stack: cur.stack };
574	    this.refreshAll();
575	  }
576	
577	  /** 右键：拆半到光标 */
578	  private splitHalf(i: number, where: 'inv' | 'chest') {
579	    if (this.heldStack) return;
580	    const cur = this.slotContent(where, i);
581	    if (!cur) return;
582	    const half = Math.ceil(cur.stack / 2);
583	    if (where === 'inv') this.game.player.inv.removeAt(i, half);
584	    else if (this.openChest) {
585	      cur.stack -= half;
586	      if (cur.stack <= 0) this.openChest.items[i] = null;
587	    }
588	    this.heldStack = { id: cur.id, stack: half };
589	    this.refreshAll();
590	  }
591	
592	  /** 放下到背包/宝箱格（合并→交换，装备位校验） */
593	  private placeHeld(i: number, where: 'inv' | 'chest'): void {
594	    if (!this.heldStack) return;
595	    if (where === 'inv') {
596	      const inv = this.game.player.inv;
597	      if (!inv.canAccept(i, this.heldStack.id)) return; // 装备位校验失败：弹回原处
598	      const cur = inv.slots[i];
599	      if (!cur) {
600	        inv.slots[i] = this.heldStack;
601	        this.heldStack = null;
602	      } else if (cur.id === this.heldStack.id) {
603	        const max = ITEM_DEFS[cur.id].maxStack;
604	        const put = Math.min(max - cur.stack, this.heldStack.stack);
605	        cur.stack += put;
606	        this.heldStack.stack -= put;
607	        if (this.heldStack.stack <= 0) this.heldStack = null;
608	      } else if (inv.canAccept(i, cur.id) === false) {
609	        return; // 占位物品放不回普通格（理论不发生，防御）
610	      } else {
611	        inv.slots[i] = this.heldStack;
612	        this.heldStack = cur;
613	      }
614	    } else {
615	      const chest = this.openChest;
616	      if (!chest) return;
617	      const cur = chest.items[i];
618	      if (!cur) {
619	        chest.items[i] = this.heldStack;
620	        this.heldStack = null;
621	      } else if (cur.id === this.heldStack.id) {
622	        const max = ITEM_DEFS[cur.id].maxStack;
623	        const put = Math.min(max - cur.stack, this.heldStack.stack);
624	        cur.stack += put;
625	        this.heldStack.stack -= put;
626	        if (this.heldStack.stack <= 0) this.heldStack = null;
627	      } else {
628	        chest.items[i] = this.heldStack;
629	        this.heldStack = cur;
630	      }
631	    }
632	  }
633	
634	  /** 拖拽松手：判定落点（格子/垃圾桶/面板外丢弃/面板空白放回） */
635	  private resolveDrop(from: { i: number; where: 'inv' | 'chest' }) {
636	    const target = document.elementFromPoint(this.mouseX, this.mouseY) as HTMLElement | null;
637	    const slotEl = target?.closest?.('.sw-slot') as HTMLElement | null;
638	    if (slotEl?.dataset.idx !== undefined && slotEl?.dataset.where) {
639	      const ti = Number(slotEl.dataset.idx);
640	      const tw = slotEl.dataset.where as 'inv' | 'chest';
641	      if (tw === 'chest' && !this.openChest) return;
642	      this.placeHeld(ti, tw);
643	      return;
644	    }
645	    if (target?.closest?.('.sw-trash')) {
646	      this.placeTrash();
647	      return;
648	    }
649	    // 面板外：丢进世界；面板内空白：放回原格
650	    const inPanel = target?.closest?.('.sw-panel');
651	    if (!inPanel) {
652	      this.throwHeldToWorld();
653	    } else {
654	      this.placeHeld(from.i, from.where);
655	    }
656	  }
657	
658	  /** 垃圾桶：丢弃暂存（关闭背包时结算删除） */
659	  private trashHeld() {
660	    this.placeTrash();
661	  }
662	
663	  /** 拖出面板：以掉落物形式丢在角色面前 */
664	  private throwHeldToWorld() {
665	    if (!this.heldStack || !this.game) return;
666	    const p = this.game.player;
667	    const key = ITEM_DEFS[this.heldStack.id].key;
668	    this.game.spawnDrop(p.cx + p.facing * 18, p.y + 6, key, this.heldStack.stack, p.facing * 1.5, -2);
669	    this.heldStack = null;
670	  }
671	
672	  /** 光标持有物的 ghost 跟随 */
673	  private moveGhost() {
674	    if (!this.heldStack) {
675	      if (this.ghostEl) { this.ghostEl.remove(); this.ghostEl = null; }
676	      return;
677	    }
678	    if (!this.ghostEl) {
679	      this.ghostEl = el('div', 'sw-drag-ghost');
680	      const img = el('img') as HTMLImageElement;
681	      img.src = iconUrl(this.game, this.heldStack.id);
682	      img.draggable = false;
683	      this.ghostEl.appendChild(img);
684	      document.body.appendChild(this.ghostEl);
685	    }
686	    const img = this.ghostEl.querySelector('img') as HTMLImageElement;
687	    const url = iconUrl(this.game, this.heldStack.id);
688	    if (img.src !== url) img.src = url;
689	    let cnt = this.ghostEl.querySelector('.cnt') as HTMLElement | null;
690	    if (this.heldStack.stack > 1) {
691	      if (!cnt) { cnt = el('span', 'cnt'); this.ghostEl.appendChild(cnt); }
692	      cnt.textContent = String(this.heldStack.stack);
693	    } else cnt?.remove();
694	    this.ghostEl.style.left = `${this.mouseX - 20}px`;
695	    this.ghostEl.style.top = `${this.mouseY - 20}px`;
696	  }
697	
698	  private showTooltipFor(i: number, where: 'inv' | 'chest') {
699	    const s = this.slotContent(where, i);
700	    if (!s) { this.tooltip.style.display = 'none'; return; }
701	    const def = ITEM_DEFS[s.id];
702	    let html = `<b style="color:#ffe8a0">${def.name}</b> ×${s.stack}`;
703	    if (def.tool?.damage) html += `<br>伤害 ${def.tool.damage}`;
704	    if (def.tool?.power && def.tool.type !== 'sword') html += `<br>${def.tool.type === 'pick' ? '镐力' : '斧力'} ${def.tool.power}`;
705	    if (def.heal) html += `<br>回复 ${def.heal} 生命`;
706	    if (def.desc) html += `<br><span style="color:#9a8ab8">${def.desc}</span>`;
707	    this.tooltip.innerHTML = html;
708	    this.tooltip.style.display = 'block';
709	    const slotEl = this.slotEl(i, where);
710	    if (slotEl) {
711	      const r = slotEl.getBoundingClientRect();
712	      this.tooltip.style.left = `${r.right + 8}px`;
713	      this.tooltip.style.top = `${r.top}px`;
714	    }
715	  }
716	
717	  // ============ 背包 + 合成 ============
718	
719	  openInventory() {
720	    if (this.invPanel.style.display === 'block') {
721	      this.closeInventory();
722	      return;
723	    }
724	    this.invPanel.style.display = 'block';
725	    this.refreshAll();
726	    this.game.input.uiBlocking = true;
727	  }
728	
729	  closeInventory() {
730	    this.invPanel.style.display = 'none';
731	    this.closeChest();
732	    // 放回手上物品
733	    if (this.heldStack) {
734	      this.game.player.inv.add(this.heldStack.id, this.heldStack.stack);
735	      this.heldStack = null;
736	    }
737	    // 垃圾桶结算：关闭背包才真正删除
738	    if (this.trashStack) {
739	      const def = ITEM_DEFS[this.trashStack.id];
740	      this.toast(`已丢弃 ${def.name} ×${this.trashStack.stack}`);
741	      this.trashStack = null;
742	      this.paintTrash();
743	    }
744	    this.moveGhost();
745	    this.game.input.uiBlocking = false;
746	  }
747	
748	  /** 垃圾桶暂存（关闭背包才删除；可取回） */
749	  trashStack: { id: number; stack: number } | null = null;
750	
751	  private placeTrash(): void {
752	    if (!this.heldStack) return;
753	    const t = this.trashStack;
754	    if (!t) {
755	      this.trashStack = this.heldStack;
756	      this.heldStack = null;
757	    } else if (t.id === this.heldStack.id) {
758	      const max = ITEM_DEFS[t.id].maxStack;
759	      const put = Math.min(max - t.stack, this.heldStack.stack);
760	      t.stack += put;
761	      this.heldStack.stack -= put;
762	      if (this.heldStack.stack <= 0) this.heldStack = null;
763	    } else {
764	      this.trashStack = this.heldStack; // 交换：可把误放的东西取回
765	      this.heldStack = t;
766	    }
767	    this.paintTrash();
768	  }
769	
770	  private paintTrash() {
771	    if (!this.trashEl) return;
772	    const img = this.trashEl.querySelector('img');
773	    const cnt = this.trashEl.querySelector('.cnt');
774	    img?.remove();
775	    cnt?.remove();
776	    if (this.trashStack) {
777	      const im = el('img') as HTMLImageElement;
778	      im.src = iconUrl(this.game, this.trashStack.id);
779	      im.draggable = false;
780	      this.trashEl.appendChild(im);
781	      if (this.trashStack.stack > 1) {
782	        this.trashEl.appendChild(el('span', 'cnt', String(this.trashStack.stack)));
783	      }
784	    }
785	  }
786	
787	  trashEl: HTMLElement | null = null;
788	
789	  private buildInventoryPanel() {
790	    this.invPanel = el('div', 'sw-panel');
791	    this.invPanel.style.cssText = 'position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); display:none; max-height:88vh; overflow:auto;';
792	    this.invPanel.appendChild(el('div', 'sw-title', '🎒 背包'));
793	
794	    // 主体：左纸娃娃列（装备/时装/垃圾桶/配饰/金钱） + 右背包 10×4
795	    const body = el('div');
796	    body.style.cssText = 'display:flex; gap:14px; margin-bottom:8px;';
797	    const left = el('div');
798	    left.style.cssText = 'width:152px; flex:none;';
799	    const equipRow = (label: string, from: number, n: number, cols = 3) => {
800	      const wrap = el('div');
801	      wrap.appendChild(el('div', 'sw-lbl', label));
802	      const row = el('div');
803	      row.style.cssText = `display:grid; grid-template-columns:repeat(${cols},44px); gap:4px; margin-bottom:6px;`;
804	      for (let k = 0; k < n; k++) row.appendChild(this.makeSlotEl(from + k, 'inv'));
805	      wrap.appendChild(row);
806	      return wrap;
807	    };
808	    left.appendChild(equipRow('🛡 装备', ARMOR_START, 3));
809	    left.appendChild(equipRow('👑 时装', VANITY_START, 3));
810	    // 垃圾桶（暂存，关闭背包时才真正删除；可交换取回）
811	    left.appendChild(el('div', 'sw-lbl', '丢弃'));
812	    const trash = el('div', 'sw-slot trash sw-trash');
813	    trash.style.cssText = 'width:44px; height:44px; flex:none;';
814	    trash.addEventListener('mousedown', (e) => {
815	      e.stopPropagation();
816	      if (this.heldStack) {
817	        this.placeTrash();
818	      } else if (this.trashStack) {
819	        this.heldStack = this.trashStack; // 取回
820	        this.trashStack = null;
821	        this.paintTrash();
822	      }
823	      this.refreshAll();
824	    });
825	    this.trashEl = trash;
826	    left.appendChild(trash);
827	    left.appendChild(equipRow('💫 配饰', ACCESSORY_START, 5)); // 3 列自动换行
828	    left.appendChild(equipRow('💰 金钱', COIN_START, 3));
829	    body.appendChild(left);
830	
831	    // 背包 10×4（10-39）
832	    const right = el('div');
833	    right.appendChild(el('div', 'sw-lbl', '背包'));
834	    const grid = el('div');
835	    grid.style.cssText = 'display:grid; grid-template-columns:repeat(10,48px); gap:4px;';
836	    for (let i = 10; i < ACCESSORY_START; i++) {
837	      grid.appendChild(this.makeSlotEl(i, 'inv'));
838	    }
839	    right.appendChild(grid);
840	    body.appendChild(right);
841	    this.invPanel.appendChild(body);
842	
843	    // 合成区
844	    this.invPanel.appendChild(el('div', 'sw-title', '合成'));
845	    const stations = el('div', '', '');
846	    stations.style.cssText = 'font-size:12px; color:#8ad0a0; margin-bottom:6px;';
847	    stations.dataset.role = 'stations';
848	    this.invPanel.appendChild(stations);
849	    this.craftListEl = el('div');
850	    this.craftListEl.style.cssText = 'max-height:240px; overflow-y:auto; width:520px;';
851	    this.invPanel.appendChild(this.craftListEl);
852	    this.root.appendChild(this.invPanel);
853	  }
854	
855	  /** Buff 状态栏（常驻格 + 秒级倒计时，移植自 Maples BuffBar） */
856	  private buildBuffBar() {
857	    this.buffBar = el('div');
858	    this.buffBar.style.cssText = 'pointer-events:auto; position:fixed; top:44px; left:14px; display:flex; gap:4px;';
859	    this.root.appendChild(this.buffBar);
860	    this.buffBlocks.clear();
861	    for (const t of [BuffType.Agility, BuffType.Ironskin, BuffType.Resistance, BuffType.Thorns, BuffType.Regen]) {
862	      const block = el('div', 'sw-buff');
863	      block.style.display = 'none';
864	      const icon = el('img') as HTMLImageElement;
865	      icon.draggable = false;
866	      icon.style.cssText = 'width:28px; height:28px; image-rendering:pixelated;';
867	      block.appendChild(icon);
868	      const time = el('span', '', '');
869	      time.style.cssText = 'position:absolute; right:2px; bottom:0; font-size:11px; font-weight:bold; color:#fff; text-shadow:1px 1px 0 #000;';
870	      block.appendChild(time);
871	      this.buffBar.appendChild(block);
872	      this.buffBlocks.set(t, { block, icon, time });
873	    }
874	  }
875	
876	  buffBar: HTMLElement | null = null;
877	  buffBlocks = new Map<BuffType, { block: HTMLElement; icon: HTMLImageElement; time: HTMLElement }>();
878	
879	  /** 每秒左右调用一次（由 Game 经 callbacks 驱动） */
880	  refreshBuffs() {
881	    if (!this.game || !this.buffBar) return;
882	    const buffs = this.game.player.buffs;
883	    for (const [t, ui] of this.buffBlocks) {
884	      const left = buffs.active.get(t);
885	      if (left === undefined) {
886	        ui.block.style.display = 'none';
887	        continue;
888	      }
889	      ui.block.style.display = 'flex';
890	      ui.block.title = `${BUFF_DEFS[t].name}：${BUFF_DEFS[t].desc}`;
891	      const iconId = this.buffIconItem.get(t);
892	      if (iconId && !ui.icon.src) ui.icon.src = iconUrl(this.game, iconId);
893	      const s = Math.ceil(left);
894	      ui.time.textContent = s >= 60 ? `${Math.floor(s / 60)}m${s % 60}` : String(s);
895	    }
896	  }
897	
898	  // Buff → 显示用物品图标（药水图标即 Buff 图标）
899	  buffIconItem = new Map<BuffType, number>();
900	
901	  private buildChestPanel() {
902	    this.chestPanel = el('div', 'sw-panel');
903	    this.chestPanel.style.cssText = 'position:fixed; left:50%; top:16%; transform:translateX(-50%); display:none;';
904	    this.chestPanel.appendChild(el('div', 'sw-title', '宝箱'));
905	    const grid = el('div');
906	    grid.style.cssText = 'display:grid; grid-template-columns:repeat(5,48px); gap:5px;';
907	    for (let i = 0; i < 10; i++) {
908	      grid.appendChild(this.makeSlotEl(i, 'chest'));
909	    }
910	    this.chestPanel.appendChild(grid);
911	    this.root.appendChild(this.chestPanel);
912	  }
913	
914	  private openChestPanel(c: ChestData) {
915	    this.openChest = c;
916	    this.chestPanel.style.display = 'block';
917	    this.openInventory();
918	    this.refreshAll();
919	  }
920	
921	  closeChest() {
922	    this.openChest = null;
923	    this.chestPanel.style.display = 'none';
924	  }
925	
926	  // ============ 刷新 ============
927	
928	  refreshHotbar() {
929	    if (!this.game) return;
930	    const inv = this.game.player.inv;
931	    for (let i = 0; i < 10; i++) {
932	      const slotEl = this.slotEl(i, 'inv');
933	      if (!slotEl) continue;
934	      this.paintSlot(slotEl, inv.slots[i]);
935	      slotEl.classList.toggle('sel', i === inv.selected);
936	    }
937	  }
938	
939	  private paintSlot(slotEl: HTMLElement, content: { id: number; stack: number } | null) {
940	    const oldImg = slotEl.querySelector('img');
941	    const oldCnt = slotEl.querySelector('.cnt');
942	    if (oldImg) oldImg.remove();
943	    if (oldCnt) oldCnt.remove();
944	    if (content) {
945	      const img = el('img') as HTMLImageElement;
946	      img.src = iconUrl(this.game, content.id);
947	      img.draggable = false;
948	      slotEl.appendChild(img);
949	      if (content.stack > 1) {
950	        slotEl.appendChild(el('span', 'cnt', String(content.stack)));
951	      }
952	    }
953	  }
954	
955	  refreshAll() {
956	    if (!this.game) return;
957	    this.moveGhost();
958	    this.paintTrash();
959	    this.refreshHotbar();
960	    const inv = this.game.player.inv;
961	    for (let i = 10; i < INV_SIZE; i++) {
962	      const slotEl = this.slotEl(i, 'inv');
963	      if (slotEl) this.paintSlot(slotEl, inv.slots[i]);
964	    }
965	    this.refreshBuffs();
966	    if (this.openChest) {
967	      for (let i = 0; i < 10; i++) {
968	        const slotEl = this.slotEl(i, 'chest');
969	        if (slotEl) this.paintSlot(slotEl, this.openChest.items[i]);
970	      }
971	    }
972	    this.refreshCrafting();
973	  }
974	
975	  private refreshCrafting() {
976	    const game = this.game;
977	    if (!game || !this.craftListEl) return;
978	    const stations = game.stationsNearby();
979	    const stationsEl = this.invPanel.querySelector('[data-role="stations"]') as HTMLElement;
980	    if (stationsEl) {
981	      stationsEl.textContent = `可用合成站：${[...stations].map((s) => ({ hand: '徒手', workbench: '🛠 工作台', furnace: '🔥 熔炉', anvil: '⚒ 铁砧' } as Record<string, string>)[s] ?? s).join('、')}`;
982	    }
983	    this.craftListEl.innerHTML = '';
984	    for (const r of RECIPES) {
985	      if (!stations.has(r.station)) continue;
986	      const ok = game.canCraft(r);
987	      const row = el('div', 'sw-recipe' + (ok ? '' : ' no'));
988	      const outDef = ITEM_DEFS[game.itemId(r.out)];
989	      const img = el('img') as HTMLImageElement;
990	      img.src = iconUrl(game, game.itemId(r.out));
991	      row.appendChild(img);
992	      const label = el('span', '', `${outDef.name}${r.count > 1 ? ` ×${r.count}` : ''}`);
993	      row.appendChild(label);
994	      const mats = el('span', '', r.inputs.map(([k, n]) => {
995	        const have = game.player.inv.countOf(game.itemId(k));
996	        return ` ${ITEM_DEFS[game.itemId(k)].name} ${have}/${n}`;
997	      }).join(' ·'));
998	      mats.style.cssText = 'margin-left:auto; color:#9a8ab8; font-size:11px; text-align:right;';
999	      row.appendChild(mats);
1000	      if (ok) {
1001	        row.onclick = () => {
1002	          game.craft(r);
1003	          this.refreshAll();
1004	        };
1005	      }
1006	      this.craftListEl.appendChild(row);
1007	    }
1008	  }
1009	
1010	  // ============ Toast ============
1011	
1012	  toast(msg: string) {
1013	    if (this.toastEl) this.toastEl.remove();
1014	    const t = el('div', 'sw-toast', msg);
1015	    this.toastEl = t;
1016	    this.root.appendChild(t);
1017	    if (this.toastTimer) clearTimeout(this.toastTimer);
1018	    this.toastTimer = window.setTimeout(() => {
1019	      t.style.opacity = '0';
1020	      setTimeout(() => t.remove(), 500);
1021	    }, 2500);
1022	  }
1023	
1024	  // ============ 暂停菜单 ============
1025	
1026	  showPause(handlers: { onResume: () => void; onSave: () => void; onQuit: () => void }) {
1027	    const panel = el('div', 'sw-panel');
1028	    panel.style.cssText = 'pointer-events:auto; position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); width:280px;';
1029	    panel.appendChild(el('div', 'sw-title', '已暂停'));
1030	    const bRes = el('button', 'sw-btn', '继续游戏');
1031	    bRes.onclick = () => { panel.remove(); handlers.onResume(); };
1032	    const bSave = el('button', 'sw-btn', '保存存档');
1033	    bSave.onclick = () => handlers.onSave();
1034	    const bQuit = el('button', 'sw-btn', '回到主菜单');
1035	    bQuit.onclick = () => { panel.remove(); handlers.onQuit(); };
1036	    panel.append(bRes, bSave, bQuit);
1037	    this.root.appendChild(panel);
1038	    return panel;
1039	  }
1040	
1041	  closeAll() {
1042	    this.root.innerHTML = '';
1043	    this.heldStack = null;
1044	    this.openChest = null;
1045	  }
1046	
1047	  /** 初始化 HUD 相关面板（进入游戏后调用一次） */
1048	  initInGame() {
1049	    this.buildInventoryPanel();
1050	    this.buildChestPanel();
1051	    this.buildBuffBar();
1052	    this.buildHud(this.game);
1053	    // Buff → 图标物品映射
1054	    const map: Array<[BuffType, string]> = [
1055	      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
1056	      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
1057	      [BuffType.Regen, 'regen_potion'],
1058	    ];
1059	    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);
1060	  }
1061	}
1062	

```


---

## 🤖 Assistant · 2026-08-09T09:09:20.292Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read Game.ts, Input.ts, Inventory.ts, items.ts, recipes.ts, Player.ts, SaveFile.ts, KvStore.ts, WorldGen.ts (relevant parts). Let me read in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:20.294Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:20.299Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Input.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:20.310Z

**📎 ToolResult**

```
1	// 键盘/鼠标输入。UI 打开时屏蔽游戏输入。
2	export class Input {
3	  keys = new Set<string>();
4	  mouseX = 0; mouseY = 0;
5	  mouseDown = false;
6	  rightDown = false;
7	  uiBlocking = false;     // 背包/合成等打开时为 true
8	  wheelDelta = 0;
9	  keydownHandlers: Array<(code: string) => void> = [];
10	
11	  private el: HTMLElement;
12	
13	  constructor(el: HTMLElement) {
14	    this.el = el;
15	    window.addEventListener('keydown', (e) => {
16	      if (e.repeat) return;
17	      this.keys.add(e.code);
18	      this.keydownHandlers.forEach((fn) => fn(e.code));
19	      if (['Space', 'ArrowUp', 'ArrowDown', 'Tab'].includes(e.code)) e.preventDefault();
20	    });
21	    window.addEventListener('keyup', (e) => this.keys.delete(e.code));
22	    window.addEventListener('blur', () => this.keys.clear());
23	    el.addEventListener('mousemove', (e) => {
24	      const r = this.el.getBoundingClientRect();
25	      this.mouseX = e.clientX - r.left;
26	      this.mouseY = e.clientY - r.top;
27	    });
28	    // mousedown 挂 window：不依赖事件目标是否恰好是 canvas
29	    window.addEventListener('mousedown', (e) => {
30	      // UI 面板上的点击不穿透为游戏输入
31	      if ((e.target as HTMLElement)?.closest?.('.sw-panel, .sw-slot, .sw-recipe, .sw-btn')) return;
32	      if (e.button === 0) this.mouseDown = true;
33	      if (e.button === 2) this.rightDown = true;
34	    });
35	    window.addEventListener('mouseup', (e) => {
36	      if (e.button === 0) this.mouseDown = false;
37	      if (e.button === 2) this.rightDown = false;
38	    });
39	    el.addEventListener('contextmenu', (e) => e.preventDefault());
40	    el.addEventListener('wheel', (e) => {
41	      this.wheelDelta += Math.sign(e.deltaY);
42	      e.preventDefault();
43	    }, { passive: false });
44	  }
45	
46	  down(code: string): boolean {
47	    return !this.uiBlocking && this.keys.has(code);
48	  }
49	
50	  /** 每帧末调用，处理一次性输入（滚轮切换快捷栏） */
51	  endFrame() {
52	    this.wheelDelta = 0;
53	  }
54	}
55	

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:20.471Z

**📎 ToolResult**

```
1	// 游戏主控制器：状态、主循环、挖掘/放置/战斗/生成/存档的总装
2	import { TILE, SPAWN_CHECK_INTERVAL, ENEMY_CAP, SPAWN_MIN_DIST, SPAWN_MAX_DIST } from './constants';
3	import { RNG } from './rng';
4	import { Input } from './Input';
5	import { buildAssets, AssetBundle } from '../assets/AssetGen';
6	import { World, ChestData } from '../world/World';
7	import { generateWorld } from '../world/gen/WorldGen';
8	import { TILE_DEFS, T, TILE_BY_KEY } from '../data/tiles';
9	import { ITEM_DEFS, ITEM_BY_KEY } from '../data/items';
10	import { poolFor, vanillaNpc } from '../data/vanillaNpcs';
11	import { ENEMY_DEFS } from '../data/enemies';
12	import { RECIPES } from '../data/recipes';
13	import { Player } from '../entities/Player';
14	import { Enemy } from '../entities/Enemy';
15	import { ItemDrop } from '../entities/ItemDrop';
16	import { TownNPC } from '../entities/TownNPC';
17	import { Tombstone } from '../entities/Tombstone';
18	import { Critter } from '../entities/Critter';
19	import { CRITTER_DEFS } from '../data/critters';
20	import { EntityManager, Entity } from '../entities/Entity';
21	import { Camera } from '../render/Camera';
22	import { ChunkCache } from '../render/ChunkCache';
23	import { Renderer, Particle, DamageNumber, Minimap } from '../render/Renderer';
24	import { LightingEngine } from '../lighting/LightingEngine';
25	import { Inventory, ACCESSORY_START, ARMOR_START } from '../items/Inventory';
26	
27	// 导入的原版树族 tile（fellImportedTree 整棵砍伐）：普通树 + 宝石树 + 装饰树 + 灰烬树
28	const IMPORTED_TREE_TYPES = new Set<number>(
29	  ['v_5_trees',
30	    'v_583_topaz_tree', 'v_584_amethyst_tree', 'v_585_sapphire_tree', 'v_586_emerald_tree',
31	    'v_587_ruby_tree', 'v_588_diamond_tree', 'v_589_amber_tree',
32	    'v_596_vanity_tree_sakura', 'v_616_vanity_tree_yellow_willow', 'v_634_ash_tree',
33	    'v_72_mushroom_tree', 'v_323_palm_trees']
34	    .map((k) => TILE_BY_KEY[k])
35	    .filter((v): v is number => v !== undefined),
36	);
37	import { LiquidSim } from '../world/liquid/LiquidSim';
38	import { BuffType } from '../stats/Buffs';
39	import { SpriteAtlas } from '../assets/SpriteAtlas';
40	import { AutoTiler } from '../render/AutoTiler';
41	import { VanillaWallTiler } from '../render/VanillaWallTiler';
42	import { Sfx, SfxName } from './Sfx';
43	import { HitTile } from './HitTile';
44	import type { GameHooks } from '../entities/types';
45	import { Dart } from '../entities/Dart';
46	import { Arrow } from '../entities/Arrow';
47	import { Minecart } from '../entities/Minecart';
48	import { MagicProj } from '../entities/MagicProj';
49	
50	const FIXED_DT = 1 / 60;
51	
52	export interface GameCallbacks {
53	  onWorldReady: () => void;
54	  onInventoryChanged: () => void;
55	  onToast: (msg: string) => void;
56	  onBuffsChanged?: () => void;
57	  onDayNight?: (isDay: boolean) => void;
58	}
59	
60	export class Game implements GameHooks {
61	  assets: AssetBundle;
62	  atlas: SpriteAtlas | null = null;
63	  autotiler: AutoTiler | null = null;
64	  world!: World;
65	  player!: Player;
66	  camera!: Camera;
67	  renderer: Renderer;
68	  chunks!: ChunkCache;
69	  lighting!: LightingEngine;
70	  liquid!: LiquidSim;
71	  entities = new EntityManager();
72	  input: Input;
73	  cb: GameCallbacks;
74	  sfx = new Sfx();
75	
76	  running = false;
77	  paused = false;
78	  private acc = 0;
79	  private lastTime = 0;
80	  private tickCount = 0;
81	
82	  // 挖掘状态
83	  private mining: { x: number; y: number; progress: number } | null = null;
84	  /** 当前挖掘目标的硬度缓存（进度归一化用） */
85	  private hardnessCache = 1;
86	  /** 原版 HitTile 伤害积累（劈砍/挖掘通用，阈值 100） */
87	  private hitTiles = new HitTile();
88	  private lastMineHitTick = -999;
89	  swing: { t: number; dur: number; item: number } | null = null;
90	  private swingHitSet = new Set<number>();
91	
92	  // 弹药
93	  particles: Particle[] = [];
94	  dmgNumbers: DamageNumber[] = [];
95	
96	  // 敌人生成
97	  private spawnTimer = 0;
98	  boss: Enemy | null = null;
99	  /** tile key → id 反查表（调试句柄/wld 导入映射用） */
100	  tileByKey = TILE_BY_KEY;
101	
102	  /** 开发者模式：全部道具入包（溢出的落在展示区上方）+ 出生点右侧摆放所有可放置图块供检验 */
103	  setupDevMode() {
104	    const p = this.player;
105	    const st = this.world.store;
106	    // ---- 1) 全道具入包 ----
107	    const overflow: Array<[string, number]> = [];
108	    for (const def of ITEM_DEFS) {
109	      const n = def.maxStack === 1 ? 1 : Math.min(def.maxStack, 99);
110	      const left = p.inv.add(ITEM_BY_KEY[def.key], n);
111	      if (left > 0) overflow.push([def.key, left]);
112	    }
113	    // ---- 2) 展示区：出生点右侧清空并逐行摆放全部可放置图块 ----
114	    const sx = this.world.spawnX, sy = this.world.spawnY;
115	    const x0 = sx + 6, x1 = sx + 70, yBot = sy - 2, yTop = sy - 40;
116	    for (let x = x0; x <= x1; x++) {
117	      for (let y = yTop; y <= yBot; y++) {
118	        st.setTile(x, y, 0);
119	        st.setLiquid(x, y, 0, 0);
120	      }
121	      st.setTile(x, yBot, T.STONE);
122	      st.setTile(x, yBot + 1, T.STONE);
123	    }
124	    // 收集可放置 tile（有物品指向，去重）
125	    const placeable: number[] = [];
126	    const seen = new Set<number>();
127	    for (const def of ITEM_DEFS) {
128	      if (!def.tile) continue;
129	      const tid = TILE_BY_KEY[def.tile];
130	      if (tid === undefined || tid === 0 || seen.has(tid)) continue;
131	      seen.add(tid);
132	      placeable.push(tid);
133	    }
134	    // 逐行摆放：行高 7（最高家具 5 格 + 间隙），每行放满换行并铺新地板
135	    let cx = x0 + 1, cy = yBot - 1;
136	    const rowH = 7;
137	    for (const tid of placeable) {
138	      const td = TILE_DEFS[tid];
139	      const w = td.vanilla?.fw ?? td.w ?? 1;
140	      const h = td.vanilla?.fh ?? td.h ?? 1;
141	      if (cx + w > x1 - 1) {
142	        cx = x0 + 1;
143	        cy -= rowH;
144	        for (let x = x0; x <= x1; x++) st.setTile(x, cy, T.STONE);
145	      }
146	      for (let dx = 0; dx < w; dx++) {
147	        for (let dy = 0; dy < h; dy++) {
148	          // 原版帧语义（TileObject.Place）：顶行 frameY=0，底行最大——
149	          // 此处 cy 是底部行，dy=0 是底行 → frameY = (h-1-dy)*18
150	          st.setTile(cx + dx, cy - dy, tid, td.vanilla ? dx * 18 : dx, td.vanilla ? (h - 1 - dy) * 18 : dy);
151	        }
152	      }
153	      cx += w + 1;
154	    }
155	    // ---- 3) 溢出道具以掉落物排在展示区上方（背包 40 格装不下的部分） ----
156	    let dxDrop = x0;
157	    let dyDrop = yTop + 3;
158	    for (const [key, n] of overflow) {
159	      this.spawnDrop(dxDrop * TILE + 8, dyDrop * TILE, key, n, 0, 0);
160	      dxDrop += 2;
161	      if (dxDrop > x1 - 1) { dxDrop = x0; dyDrop += 3; }
162	    }
163	    this.cb.onInventoryChanged();
164	    this.cb.onToast(`开发者模式：${overflow.length} 种道具背包装不下，已排在展示区上方；全部可放置图块在出生点右侧`);
165	  }
166	
167	  // NPC 系统
168	  private housingCheckTimer = 0;
169	  guideSpawned = false;
170	  private lastWasDay: boolean | null = null;
171	  private _mapClickLatch = false;
172	  private _mapClickLatch2 = false;
173	  /** 地图内按压起点（松开时与当前位置比对 <6px 判定为点击，否则是拖动） */
174	  private _mapPressX = 0;
175	  private _mapPressY = 0;
176	  private _tpTarget: { x: number; y: number } | null = null;
177	  // 方块标注模式（F5）：点击标记问题方块，导出标注+地图给开发者定位
178	  annotateMode = false;
179	  waterCandleNear = false;
180	  trackTile = TILE_BY_KEY['v_314_minecart_track'] ?? 0;
181	  minecart: import('../entities/Minecart').Minecart | null = null;
182	  trapCooldown = new Map<string, number>();
183	  plateLatch = new Set<string>();
184	  // 贴图纠错子模式：点击方块弹出该图块的完整原版贴图表供选帧
185	  fixTexMode = false;
186	  // 敌人生成开关（F8）：关闭后不再生成新怪物（已有的不受影响）
187	  enemySpawnEnabled = true;
188	  marks: Array<{ x: number; y: number }> = [];
189	  private _annoLatch = false;
190	
191	  constructor(root: HTMLElement, cb: GameCallbacks, atlas?: SpriteAtlas | null) {
192	    this.assets = buildAssets();
193	    if (atlas) {
194	      this.atlas = atlas;
195	      this.autotiler = new AutoTiler(atlas);
196	    }
197	    this.renderer = new Renderer(this.assets, atlas);
198	    this.renderer.attach(root);
199	    this.sfx.load(); // 原版 wav 预解码（挂起态也可解码）
200	    // 怪物专属声效文件追加载入
201	    const extra = new Set<string>();
202	    for (const d of Object.values(ENEMY_DEFS)) for (const f of [...d.hitSound, ...d.killedSound]) extra.add(f);
203	    this.sfx.addFiles([...extra]);
204	    this.input = new Input(this.renderer.canvas);
205	    this.cb = cb;
206	    // 快捷栏数字键：事件驱动（避免单帧内 down+up 被轮询漏掉）
207	    this.input.keydownHandlers.push((code) => {
208	      if (this.player && /^Digit[0-9]$/.test(code)) {
209	        this.player.inv.selected = code === 'Digit0' ? 9 : Number(code.slice(5)) - 1;
210	        this.cb.onInventoryChanged();
211	      }
212	      // 缩放调节
213	      if (code === 'Equal' || code === 'NumpadAdd') this.setZoom(this.camera?.zoomTarget + 0.15);
214	      if (code === 'Minus' || code === 'NumpadSubtract') this.setZoom(this.camera?.zoomTarget - 0.15);
215	    });
216	  }
217	
218	  // ================= 生命周期 =================
219	
220	  async newWorld(seedText: string, width: number, height: number, onProgress?: (label: string, p: number) => void) {
221	    this.world = await generateWorld({ width, height, seedText }, (label, p) => onProgress?.(label, p * 0.7));
222	    // 水体预沉降：创建世界时全图激活+步进至稳定，带进度条
223	    onProgress?.('水体沉降', 0.72);
224	    await this.settleLiquids((p) => onProgress?.('水体沉降', 0.72 + p * 0.27));
225	    onProgress?.('完成', 1);
226	    this.afterWorldLoad();
227	    this.cb.onWorldReady();
228	  }
229	
230	  /** 全图液体沉降：原版 WorldFile.cs:365-389 读档时序 1:1 移植。
231	   *  QuickWater 自底向上直接搬运 → WaterCheck 重建活动列表 →
232	   *  quickSettle 循环 UpdateLiquid 至收敛 → 复位后再次 WaterCheck。
233	   *  收敛后世界液体即达最终静止状态，进游戏不再有"靠近才流动" */
234	  private async settleLiquids(onProgress?: (p: number) => void) {
235	    const sim = new LiquidSim(this.world);
236	    onProgress?.(0.05);
237	    sim.quickWater();
238	    onProgress?.(0.35);
239	    await new Promise((r) => setTimeout(r, 0));
240	    sim.waterCheck();
241	    sim.quickSettle = true;
242	    const MAX_ITER = 100000; // 原版 WorldFile 同上限
243	    let iter = 0;
244	    while (sim.numLiquid > 0 && iter < MAX_ITER) {
245	      sim.updateLiquid();
246	      iter++;
247	      if (iter % 500 === 0) {
248	        onProgress?.(0.35 + Math.min(0.6, iter / 20000));
249	        await new Promise((r) => setTimeout(r, 0));
250	      }
251	    }
252	    sim.quickSettle = false;
253	    sim.waterCheck();
254	    sim.dispose(); // 丢弃临时模拟器（注销监听，避免泄漏到运行期）
255	    onProgress?.(1);
256	  }
257	
258	  async loadWorld(world: World, onProgress?: (label: string, p: number) => void) {
259	    this.world = world;
260	    onProgress?.('水体沉降', 0.5);
261	    await this.settleLiquids((p) => onProgress?.('水体沉降', p));
262	    this.afterWorldLoad();
263	    this.cb.onWorldReady();
264	  }
265	
266	  private afterWorldLoad() {
267	    const w = this.world;
268	    // 原版墙渲染器（TEdit WallFraming 移植；墙 id 直用 wld id，贴图 Wall_N.png）
269	    const wallTiler = this.atlas ? new VanillaWallTiler(this.atlas) : null;
270	    this.chunks = new ChunkCache(w, this.assets.tileSheets, this.autotiler, wallTiler);
271	    this.lighting = new LightingEngine(w);
272	    this.liquid = new LiquidSim(w);
273	    this.liquid.waterCheck(); // 原版读档末尾的 WaterCheck：把沉降后仍可流动的少量格子交给运行时收敛
274	    this.camera = new Camera(w.w, w.h);
275	    this.renderer.minimap = new Minimap(w);
276	    this.entities.clear();
277	    this.player = new Player(w.spawnX * TILE + 8, (w.spawnY - 3) * TILE, new Inventory()); // 主角 3 格高，抬高出生点
278	    // 初始装备（铁器三件套与 Maples 素材对齐；含药水与配饰便于体验 Buff/配饰系统）
279	    this.player.inv.add(ITEM_BY_KEY['iron_pickaxe'], 1);
280	    this.player.inv.add(ITEM_BY_KEY['iron_axe'], 1);
281	    this.player.inv.add(ITEM_BY_KEY['iron_sword'], 1);
282	    this.player.inv.add(ITEM_BY_KEY['torch'], 12);
283	    // 药水/召唤物放入背包格（10 起），不占快捷栏
284	    const bag: Array<[string, number]> = [
285	      ['heal_potion', 2], ['agility_potion', 2], ['ironskin_potion', 2],
286	      ['thorns_potion', 2], ['regen_potion', 2], ['suspicious_eye', 3], ['lens', 6],
287	    ];
288	    let bi = 10;
289	    for (const [key, n] of bag) {
290	      this.player.inv.slots[bi++] = { id: ITEM_BY_KEY[key], stack: n };
291	    }
292	    // 开局体验盔甲：铁三件套穿上
293	    this.player.inv.slots[ARMOR_START] = { id: ITEM_BY_KEY['iron_helmet'], stack: 1 };
294	    this.player.inv.slots[ARMOR_START + 1] = { id: ITEM_BY_KEY['iron_chainmail'], stack: 1 };
295	    this.player.inv.slots[ARMOR_START + 2] = { id: ITEM_BY_KEY['iron_greaves'], stack: 1 };
296	    // 配饰直接放入配饰栏（槽 40-44）
297	    this.player.inv.slots[ACCESSORY_START] = { id: ITEM_BY_KEY['lucky_horseshoe'], stack: 1 };
298	    this.player.inv.slots[ACCESSORY_START + 1] = { id: ITEM_BY_KEY['feral_claws'], stack: 1 };
299	    this.camera.x = this.player.cx;
300	    this.camera.y = this.player.cy;
301	    this.boss = null;
302	    this.guideSpawned = true; // 向导已移除；保留字段避免存档兼容问题
303	    // 商人 NPC(原版 Merchant 语义简化:出生点旁常驻,对话=购买)
304	    const merch = new TownNPC('merchant', this.world.spawnX * 16 - 40, (this.world.spawnY - 2) * 16);
305	    this.entities.add(merch, 'npcs');
306	    // 护士(原版:击败任一 Boss 后入住;checkNpcArrival 每帧判定)
307	    const nurse = new TownNPC('nurse', this.world.spawnX * 16 + 40, (this.world.spawnY - 2) * 16);
308	    this.entities.add(nurse, 'npcs');
309	    this.cb.onInventoryChanged();
310	  }
311	
312	  /** 销毁：停止循环并移除画布（退出到主菜单时调用） */
313	  destroy() {
314	    this.running = false;
315	    this.renderer.canvas.remove();
316	  }
317	
318	  start() {
319	    if (this.running) return;
320	    this.running = true;
321	    this.lastTime = performance.now();
322	    const loop = (now: number) => {
323	      if (!this.running) return;
324	      this.frame(now);
325	      requestAnimationFrame(loop);
326	    };
327	    requestAnimationFrame(loop);
328	  }
329	
330	  private frame(now: number) {
331	    const elapsed = Math.min((now - this.lastTime) / 1000, 0.25);
332	    this.lastTime = now;
333	    if (!this.paused) {
334	      this.acc += elapsed;
335	      let steps = 0;
336	      while (this.acc >= FIXED_DT && steps < 5) {
337	        this.fixedUpdate(FIXED_DT);
338	        this.acc -= FIXED_DT;
339	        steps++;
340	      }
341	    }
342	    this.render();
343	  }
344	
345	  // ================= 固定步逻辑 =================
346	
347	  private fixedUpdate(dt: number) {
348	    this.tickCount++;
349	    // 原版 HitTile 衰减（每 2 tick 一次——原版按帧衰减配原版 ~27 帧挥速；
350	    // 我们的挥击间隔更长，等比减半保持"连击可积累、停手会消退"）
351	    if (this.tickCount % 2 === 0) this.hitTiles.update();
352	    const w = this.world;
353	    w.clock.tick(dt * 1000);
354	    // 昼夜切换：提示 + BGM 变奏
355	    const isDay = w.clock.isDay;
356	    if (isDay !== this.lastWasDay) {
357	      if (this.lastWasDay !== null) {
358	        this.cb.onToast(isDay ? '☀ 太阳升起来了，新的一天开始了' : '🌙 夜幕降临，小心出没的怪物…');
359	        this.cb.onDayNight?.(isDay);
360	      }
361	      this.lastWasDay = isDay;
362	    }
363	    const player = this.player;
364	
365	    // ---- 玩家输入 ----
366	    const inp = this.input;
367	    // 点击右上角小地图 → 开关全屏地图
368	    if (inp.mouseDown && !this._mapClickLatch) {
369	      const r = this.renderer.minimapRect;
370	      const fm = this.renderer.fullMap;
371	      const inMap = inp.mouseX >= r.x && inp.mouseX <= r.x + r.w && inp.mouseY >= r.y && inp.mouseY <= r.y + r.h;
372	      if (!fm.open && inMap && !inp.uiBlocking) {
373	        fm.open = true;
374	        // 打开即放大到主角：锚点 = 主角 tile 坐标 → 屏幕中心，
375	        // zoom 从 0.5 缓动到 2，缓动期间 applyMapAnchor 每帧补偿 pan，主角始终居中
376	        fm.zoom = 0.5;
377	        fm.zoomTarget = 2;
378	        fm.anchorU = player.cx / TILE;
379	        fm.anchorV = player.cy / TILE;
380	        fm.anchorMX = this.renderer.canvas.width / 2;
381	        fm.anchorMY = this.renderer.canvas.height / 2;
382	        // 预置 pan（此时 _fmWorldW 可能还是 0，不能等 easeFullMap 反解，首帧会跳）
383	        fm.panX = (this.world.w * fm.zoom) / 2 - fm.anchorU * fm.zoom;
384	        fm.panY = (this.world.h * fm.zoom) / 2 - fm.anchorV * fm.zoom;
385	        this.renderer['_mapInit'] = false;
386	        // 打开地图的这次点击不算拖拽（否则按住期间 drawFullMap 会把锚点重设到点击处，飞向主角变飞向点击处）
387	        this.renderer['_mapOpenClick'] = true;
388	        this._mapClickLatch = true;
389	      }
390	    }
391	    if (!inp.mouseDown) this._mapClickLatch = false;
392	    // 全屏地图：点击传送（两次确认）——第一次预选标记，第二次传送。
393	    // 按下只记起点，松开时位移 < 6px 才算"点击"（拖动平移、打开地图的按压都不误触传送）
394	    if (this.renderer.fullMap.open && !inp.uiBlocking) {
395	      if (inp.mouseDown && !this._mapClickLatch2 && !this._mapClickLatch && !this.renderer['_mapOpenClick']) {
396	        this._mapClickLatch2 = true;
397	        this._mapPressX = inp.mouseX;
398	        this._mapPressY = inp.mouseY;
399	      }
400	      if (!inp.mouseDown && this._mapClickLatch2) {
401	        this._mapClickLatch2 = false;
402	        const moved = Math.hypot(inp.mouseX - this._mapPressX, inp.mouseY - this._mapPressY);
403	        if (moved < 6) {
404	          const fm = this.renderer.fullMap;
405	          // 屏幕坐标 → 地图源坐标（与 zoomFullMapAt 的逆变换一致）
406	          const viewW = this.renderer.canvas.width, viewH = this.renderer.canvas.height;
407	          const cx0 = viewW / 2 - (this.world.w * fm.zoom) / 2 + fm.panX;
408	          const cy0 = viewH / 2 - (this.world.h * fm.zoom) / 2 + fm.panY;
409	          // 地图绘制：mapW = world.w * zoom（1 tile = zoom 像素）——直接除 zoom 得 tile 坐标
410	          const tx = Math.floor((inp.mouseX - cx0) / fm.zoom);
411	          const ty = Math.floor((inp.mouseY - cy0) / fm.zoom);
412	          if (tx >= 0 && ty >= 0 && tx < this.world.w && ty < this.world.h) {
413	            if (this._tpTarget && this._tpTarget.x === tx && this._tpTarget.y === ty) {
414	              // 第二次点击同一点 → 传送；失败不关图、保留标记可重试
415	              if (this.teleportNear(tx, ty)) {
416	                this._tpTarget = null;
417	                this.renderer.tpMark = null;
418	                this.renderer.fullMap.open = false;
419	                this.cb.onToast('传送完成');
420	              }
421	            } else {
422	              this._tpTarget = { x: tx, y: ty };
423	              this.renderer.tpMark = { x: tx, y: ty };
424	              this.cb.onToast(`已选传送点 (${tx}, ${ty})，再次点击确认`);
425	            }
426	          }
427	        }
428	      }
429	    } else {
430	      this._mapClickLatch2 = false;
431	    }
432	    // ---- 标注模式：点击标记方块（优先于挖掘/放置/使用） ----
433	    if (this.annotateMode && inp.mouseDown && !this._annoLatch && !inp.uiBlocking && !this.renderer.fullMap.open) {
434	      this._annoLatch = true;
435	      const [tx, ty] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
436	      if (this.fixTexMode) {
437	        // 贴图纠错子模式：点击弹出该图块的完整原版贴图表
438	        if (this.world.store.inBounds(tx, ty)) {
439	          (window as unknown as { __swUI?: { openTexPicker?: (x: number, y: number) => void } }).__swUI?.openTexPicker?.(tx, ty);
440	        }
441	      } else if (this.world.store.inBounds(tx, ty)) {
442	        const existed = this.marks.some((m) => m.x === tx && m.y === ty);
443	        this.marks = this.marks.filter((m) => m.x !== tx || m.y !== ty); // 同格重复点 = 取消
444	        if (!existed) this.marks.push({ x: tx, y: ty });
445	        this.cb.onToast(existed ? `已取消标记 (${tx}, ${ty})` : `已标记 (${tx}, ${ty})，再次点击取消`);
446	        (window as unknown as { __swUI?: { updateAnnotateCount: (n: number) => void } }).__swUI?.updateAnnotateCount(this.marks.length);
447	      }
448	    }
449	    if (!inp.mouseDown) this._annoLatch = false;
450	    player.inputX = (inp.down('KeyA') || inp.down('ArrowLeft') ? -1 : 0) + (inp.down('KeyD') || inp.down('ArrowRight') ? 1 : 0);
451	    player.inputJump = inp.down('Space') || inp.down('KeyW') || inp.down('ArrowUp');
452	    player.inputDown = inp.down('KeyS') || inp.down('ArrowDown');
453	    player.inputUp = inp.down('KeyW') || inp.down('ArrowUp');
454	
455	    // 滚轮：全屏地图打开时缩放地图，否则缩放游戏画面
456	    if (inp.wheelDelta !== 0) {
457	      if (this.renderer.fullMap.open) {
458	        // 以鼠标为锚点缩放（缩放不乱飞）
459	        this.renderer.zoomFullMapAt(
460	          this.renderer.fullMap.zoom * (inp.wheelDelta > 0 ? 0.85 : 1.18),
461	          inp.mouseX, inp.mouseY,
462	        );
463	      } else {
464	        this.setZoom(this.camera.zoomTarget * (inp.wheelDelta > 0 ? 0.94 : 1.064));
465	      }
466	    }
467	
468	    player.fixedUpdate(dt, this);
469	    if (player.dead) {
470	      // 死亡瞬间：红色粉碎粒子 + 原地留墓碑（只处理一次）
471	      if (!this._deathHandled) {
472	        this._deathHandled = true;
473	        this.handlePlayerDeath();
474	      }
475	      // 重生计时
476	      player.respawnTimer++;
477	      if (player.respawnTimer > 180) this.respawnPlayer();
478	    } else {
479	      this._deathHandled = false;
480	    }
481	
482	    // ---- 使用物品（鼠标） ----
483	    this.updateUse(dt);
484	
485	    // ---- 实体 ----
486	    this.entities.update(dt, this);
487	
488	    // ---- 液体（原版每 2 tick 一次 UpdateLiquid）----
489	    if (this.tickCount % 2 === 0) {
490	      this.liquid.step();
491	      // 液体直接写数组绕过 store 监听：有活动液体时手动通知光照衰减变化
492	      if (this.liquid.numLiquid > 0) this.lighting.liquidDirty = true;
493	    }
494	
495	    // ---- 敌人生成（F8 可关闭） ----
496	    this.spawnTimer++;
497	    // 水蜡烛(Main.waterCandle 语义):手持或 32 格内有放置态 → 刷怪率 ×2(间隔减半)
498	    const held2 = this.player.inv.heldItem();
499	    const heldWC = !!held2 && ITEM_DEFS[held2.id]?.key === 'water_candle';
500	    let nearWC = false;
501	    if (this.tickCount % 30 === 0) {
502	      nearWC = false;
503	      const st2 = this.world.store;
504	      const ptx = Math.floor(this.player.cx / TILE), pty = Math.floor(this.player.cy / TILE);
505	      const WCT = TILE_BY_KEY['water_candle'];
506	      for (let dx = -32; dx <= 32 && !nearWC; dx += 4) {
507	        for (let dy = -24; dy <= 24; dy += 4) {
508	          if (st2.get(ptx + dx, pty + dy) === WCT) { nearWC = true; break; }
509	        }
510	      }
511	      this.waterCandleNear = nearWC;
512	    }
513	    // 篝火/心灯光环(Main.campfire 语义:170 格内篝火=1hp/s;心灯 BuffID115 再+1)
514	    // 和平蜡烛(peaceCandleNear):刷怪率减半
515	    if (this.tickCount % 20 === 0) {
516	      const ptx2 = Math.floor(this.player.cx / TILE), pty2 = Math.floor(this.player.cy / TILE);
517	      let fire = 0, heart = 0, peace = false;
518	      const FIRE = TILE_BY_KEY['v_215_campfires'];
519	      for (let dx = -48; dx <= 48 && fire === 0; dx += 3) {
520	        for (let dy = -36; dy <= 36; dy += 3) {
521	          if (this.world.store.get(ptx2 + dx, pty2 + dy) === FIRE) { fire = 1; break; }
522	        }
523	      }
524	      if (fire > 0) this.player.buffs.apply(BuffType.Campfire, 0.5);
525	    }
526	    const wcBoost = heldWC || this.waterCandleNear;
527	    const interval = wcBoost ? Math.ceil(SPAWN_CHECK_INTERVAL / 2) : SPAWN_CHECK_INTERVAL;
528	    if (this.enemySpawnEnabled && this.spawnTimer >= interval) {
529	      this.spawnTimer = 0;
530	      this.trySpawnEnemy();
531	    }
532	
533	    // ---- 压力板触发 ----
534	    this.checkPressurePlates();
535	
536	    // ---- Boss 逻辑 ----
537	    if (this.boss) {
538	      if (this.boss.dead || w.clock.isDay) {
539	        if (this.boss.dead && !w.flags.downedEyeOfCthulhu) {
540	          w.flags.downedEyeOfCthulhu = true;
541	          this.cb.onToast('克苏鲁之眼已被击败！');
542	        }
543	        if (w.clock.isDay && !this.boss.dead) {
544	          this.boss.dead = true;
545	          this.cb.onToast('克苏鲁之眼在黎明逃走了…');
546	        }
547	        this.boss = null;
548	      }
549	    }
550	
551	    // ---- 树苗生长（每 5 秒扫一次） ----
552	    if (this.tickCount % 300 === 0) this.growSaplings();
553	
554	    // ---- 战争迷雾：玩家周围探索标记（每 15 tick） ----
555	    if (this.tickCount % 15 === 0) {
556	      w.markExplored(Math.floor(player.cx / TILE), Math.floor(player.cy / TILE), 28);
557	    }
558	
559	    // ---- Buff 状态栏刷新（每秒） ----
560	    if (this.tickCount % 60 === 0) this.cb.onBuffsChanged?.();
561	
562	    // ---- 相机 / 光照 ----
563	    this.camera.follow(player.cx, player.cy);
564	    this.camera.easeZoom();
565	    this.camera.clamp();
566	    this.chunks.flushDirty();
567	    const viewTW = Math.ceil(this.camera.viewW / this.camera.zoom / TILE) + 2;
568	    const viewTH = Math.ceil(this.camera.viewH / this.camera.zoom / TILE) + 2;
569	    this.lighting.ensureRegion(player.cx, player.cy, viewTW, viewTH);
570	    // 手持火把照明：选中火把即点亮周围（#11）
571	    const heldDef = player.inv.heldDef();
572	    const torchOn = !!heldDef && heldDef.key === 'torch';
573	    const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
574	    const prevLight = this.lighting.heldLight;
575	    this.lighting.heldLight = torchOn ? { tx: ptx, ty: pty } : null;
576	    if (torchOn !== !!prevLight ||
577	      (torchOn && prevLight && (prevLight.tx !== ptx || prevLight.ty !== pty))) {
578	      this.lighting.dirty = true;
579	    }
580	    this.lighting.compute(w.clock.dayFactor);
581	
582	    // ---- 粒子与飘字 ----
583	    this.flushInvNotify();
584	    // 小动物环境生成：按昼夜在地表视野外生成，上限 8 只
585	    if (this.tickCount % 120 === 0 && this.entities.critters.length < 8) {
586	      this.spawnCritter();
587	    }
588	    // 怪物碾压小动物：任意敌人身体接触即杀死（不视为交战）
589	    if (this.tickCount % 4 === 0 && this.entities.critters.length) {
590	      for (const cent of this.entities.critters) {
591	        const c = cent as Critter;
592	        if (c.dead) continue;
593	        for (const eent of this.entities.enemies) {
594	          const e = eent as Enemy;
595	          if (c.x < e.x + e.w && c.x + c.w > e.x && c.y < e.y + e.h && c.y + c.h > e.y) {
596	            c.hurt(this);
597	            break;
598	          }
599	        }
600	      }
601	    }
602	    // 僵尸环境呻吟：附近有僵尸时偶发（每 ~4-8 秒）
603	    if (this.tickCount % 300 === 0) {
604	      for (const ent of this.entities.enemies) {
605	        const e = ent as Enemy;
606	        if (e.key !== 'zombie' && e.key !== 'magma_zombie') continue;
607	        if (Math.hypot(e.cx - this.player.cx, e.cy - this.player.cy) < TILE * 30) {
608	          this.sfx.playWav('zombie', 0.6);
609	          break;
610	        }
611	      }
612	    }
613	    // 火把火苗：视内点燃火把随机飘出火星（火点在格顶上方 20px 精灵的火焰处）
614	    this.emitTorchSparks();
615	    for (const p of this.particles) {
616	      p.life--;
617	      p.vy += p.grav ?? 0.12;
618	      if (p.damp) { p.vx *= p.damp; p.vy *= p.damp; } // 空气阻力：喷溅后缓慢减速飘散
619	      // 地形碰撞：目标位置实心则反弹（冲击大）或停驻地表（冲击小，重力归零缓慢淡出）
620	      const st = this.world.store;
621	      const solidAt = (x: number, y: number) => {
622	        const tx = Math.floor(x / TILE), ty = Math.floor(y / TILE);
623	        return st.inBounds(tx, ty) && st.isSolid(tx, ty);
624	      };
625	      let nx = p.x + p.vx;
626	      if (solidAt(nx, p.y)) { p.vx *= -0.4; nx = p.x; }
627	      let ny = p.y + p.vy;
628	      if (solidAt(nx, ny)) {
629	        if (p.vy > 1.6) {
630	          p.vy = -p.vy * 0.35; // 溅落反弹
631	          p.vx *= 0.6;
632	        } else {
633	          p.vy = 0; p.vx *= 0.5; p.grav = 0; // 停驻地表
634	        }
635	        ny = p.y;
636	      }
637	      p.x = nx; p.y = ny;
638	    }
639	    this.particles = this.particles.filter((p) => p.life > 0);
640	    for (const d of this.dmgNumbers) {
641	      d.life--;
642	      d.y += d.vy;
643	      d.vy *= 0.94;
644	    }
645	    this.dmgNumbers = this.dmgNumbers.filter((d) => d.life > 0);
646	
647	    inp.endFrame();
648	
649	    // 挥剑命中判定（实体更新后）
650	    this.postUpdate();
651	  }
652	
653	  // ================= 物品使用：挖掘 / 放置 / 攻击 / 使用 =================
654	
655	  private updateUse(dt: number) {
656	    const inp = this.input;
657	    // 矿车骑乘驱动:左右加速,跳车
658	    if (this.minecart) {
659	      const cart = this.minecart;
660	      const ix = this.player.inputX;
661	      if (ix !== 0) cart.vx = Math.max(-8, Math.min(8, cart.vx + ix * 0.15));
662	      if (inp.down('KeyR')) {
663	        // 跳车(原版 R 键下车;Space 与跳跃共用会误触)
664	        this.player.x = cart.x;
665	        this.player.y = cart.y - 24;
666	        this.player.vy = -4;
667	        cart.mounted = false;
668	        this.minecart = null;
669	        this.input.rightDown = false;
670	      }
671	      // 玩家跟随车位置
672	      this.player.x = cart.x;
673	      this.player.y = cart.y - 26;
674	      this.player.vx = cart.vx;
675	      this.player.vy = 0;
676	      if (cart.dead) { this.minecart = null; }
677	      return;
678	    }
679	    // 全屏地图打开时鼠标交给地图（拖动/缩放/传送），不触发挖掘/放置/攻击/使用
680	    if (inp.uiBlocking || this.player.dead || this.renderer.fullMap.open) {
681	      this.mining = null;
682	      return;
683	    }
684	    const held = this.player.inv.heldItem();
685	    const heldDef = held ? ITEM_DEFS[held.id] : null;
686	    const [tx, ty] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
687	    const tool = heldDef?.tool;
688	    const vw2 = this.renderer.canvas.width, vh2 = this.renderer.canvas.height;
689	
690	    // 右键：手持矿车点轨道(最优先,防 NPC 交谈拦截)→ 附近宝箱 → NPC 交谈 → 交互
691	    const type = this.world.store.get(tx, ty);
692	    if (inp.rightDown && !this.minecart && type === this.trackTile && this.trackTile !== 0) {
693	      const h = this.player.inv.heldItem();
694	      if (h && ITEM_DEFS[h.id]?.key === 'minecart_item') {
695	        const cart = new Minecart();
696	        cart.x = tx * TILE; cart.y = (ty - 1) * TILE;
697	        this.entities.add(cart, 'props');
698	        this.minecart = cart;
699	        cart.mounted = true;
700	        this.player.inv.removeAt(this.player.inv.selected, 1);
701	        this.cb.onInventoryChanged();
702	        this.input.rightDown = false;
703	        return;
704	      }
705	    }
706	    if (inp.rightDown) {
707	      const nearChest = this.findChestNear(tx, ty);
708	      if (nearChest) {
709	        this.tryOpenChest(nearChest);
710	        this.input.rightDown = false;
711	      } else if (this.talkToNearbyNpc(tx, ty)) {
712	        this.input.rightDown = false;
713	      } else if (heldDef?.key === 'suspicious_eye') {
714	        if (!this.world.clock.isDay) {
715	          this.useSuspiciousEye();
716	          this.player.inv.removeAt(this.player.inv.selected, 1);
717	          this.cb.onInventoryChanged();
718	        } else {
719	          this.cb.onToast('什么都没有发生...');
720	        }
721	        this.input.rightDown = false;
722	      } else {
723	        this.interactAt(tx, ty);
724	      }
725	    }
726	
727	    if (!inp.mouseDown || this.annotateMode) {
728	      this.mining = null;
729	      return;
730	    }
731	
732	    // 近战挥剑（攻速配饰：猛爪手套 ×2）
733	    if (tool?.type === 'sword') {
734	      const spd = Math.max(12, Math.round((tool.speed ?? 42) / this.player.attackSpeedMult));
735	      if (!this.swing && this.player.useTime === 0) {
736	        this.swing = { t: spd, dur: spd, item: held!.id };
737	        this.player.useTime = spd;
738	        this.swingHitSet.clear();
739	      }
740	      this.mining = null;
741	      return;
742	    }
743	
744	    // 镐/斧/锤：挖掘（按住累计）+ 同时作为武器挥击（伤害低于剑）
745	    if (tool && (tool.type === 'pick' || tool.type === 'axe' || tool.type === 'hammer')) {
746	      const spd = Math.max(14, Math.round((tool.speed ?? 46) / this.player.attackSpeedMult));
747	      if (!this.swing && this.player.useTime === 0) {
748	        this.swing = { t: spd, dur: spd, item: held!.id };
749	        this.player.useTime = spd;
750	        this.swingHitSet.clear();
751	        // 每次挥砍一声：斧砍植物纤维、镐按材质区分土闷/石金（跟随挥砍节奏，不再密集连响）。
752	        // 没有生效对象（镐没对准可挖方块 / 斧没对准树）则不出声
753	        const hType = this.world.store.get(tx, ty);
754	        const hovered = TILE_DEFS[hType];
755	        const axeOnTarget = hType === T.TREE || (hovered?.decor ?? false);
756	        const pickOnTarget = hType !== 0 && this.toolCanBreak(hType, tool.power ?? 10, tool.type);
757	        if (tool.type === 'axe' ? axeOnTarget : pickOnTarget) {
758	          if (tool.type === 'axe') this.sfx.play('chop');
759	          else if (hovered && /stone|ore|brick|obsidian|ash|gem_|fossil|silt/i.test(hovered.key)) this.sfx.play('tink');
760	          else this.sfx.play('dig');
761	        }
762	      }
763	      // HitTile 节流窗 = 实际挥击间隔（含攻速配饰加成），保证一挥一击
764	      this.tryMine(tx, ty, tool.power ?? 10, tool.type, spd);
765	      return;
766	    }
767	
768	    // 可放置物品：左键放置
769	    if (heldDef?.tile && !inp.rightDown) {
770	      this.tryPlace(tx, ty, heldDef);
771	      return;
772	    }
773	
774	    // 其它物品（方块/药水等）：左键使用并带挥砍动画
775	    if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool) {
776	      const spd = 30;
777	      this.swing = { t: spd, dur: spd, item: held!.id };
778	      this.swingHitSet.clear();
779	      // 召唤道具（原版左键使用）
780	      if (heldDef.key === 'suspicious_eye') {
781	        if (!this.world.clock.isDay) {
782	          this.useSuspiciousEye();
783	          this.player.inv.removeAt(this.player.inv.selected, 1);
784	          this.cb.onInventoryChanged();
785	        } else {
786	          this.cb.onToast('什么都没有发生...');
787	        }
788	        this.player.useTime = 30;
789	      }
790	    }
791	    // 药水饮用（移植自 Maples：点击饮用，治疗类受耐药性封锁）
792	    if (heldDef?.potion && inp.mouseDown && this.player.useTime === 0) {
793	      const p = heldDef.potion;
794	      const buffTypeMap: Record<string, BuffType> = {
795	        agility: BuffType.Agility, ironskin: BuffType.Ironskin,
796	        resistance: BuffType.Resistance, thorns: BuffType.Thorns, regen: BuffType.Regen,
797	      };
798	      if (p.isHealType && this.player.buffs.healBlocked) {
799	        this.cb.onToast('耐药性生效中，无法饮用治疗药水');
800	        this.player.useTime = 30;
801	      } else {
802	        const bt = buffTypeMap[p.buff];
803	        this.player.buffs.apply(bt, p.duration);
804	        if (heldDef.heal) {
805	          this.player.hp = Math.min(this.player.maxHp, this.player.hp + heldDef.heal);
806	          this.addDamageNumber(this.player.cx, this.player.y, heldDef.heal, false, '#40E080');
807	        }
808	        this.player.inv.removeAt(this.player.inv.selected, 1);
809	        this.player.useTime = 60;
810	        this.sfx.play('drink');
811	        this.cb.onInventoryChanged();
812	        this.cb.onToast(`${heldDef.name}：${p.duration} 秒`);
813	      }
814	    } else if (heldDef && (heldDef.key === 'life_crystal' || heldDef.key === 'vi_29_LifeCrystal')) {
815	      // 物品态生命水晶(Player.cs:29358:item 29,statLifeMax<400 → +20)
816	      if (this.player.baseMaxHp >= 400) {
817	        this.cb.onToast('生命上限已达到 400');
818	      } else {
819	        this.player.baseMaxHp += 20;
820	        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 20);
821	        this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#40E080');
822	        this.player.inv.removeAt(this.player.inv.selected, 1);
823	        this.player.useTime = 30;
824	        this.sfx.play('drink');
825	        this.cb.onInventoryChanged();
826	      }
827	      this.player.useTime = Math.max(this.player.useTime, 30);
828	    } else if (heldDef?.ranged && inp.mouseDown && this.player.useTime === 0) {
829	      // 远程武器(弓):消耗弹药 → 沿鼠标方向发射箭(Player.ItemCheck_Shoot 语义)
830	      const rg = heldDef.ranged;
831	      const ammoId = ITEM_BY_KEY[rg.ammo];
832	      let ammoSlot = -1;
833	      for (let i = 0; i < this.player.inv.slots.length; i++) {
834	        const sl = this.player.inv.slots[i];
835	        if (sl && sl.id === ammoId && sl.stack > 0) { ammoSlot = i; break; }
836	      }
837	      if (ammoSlot >= 0) {
838	        const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
839	        const ax = this.player.cx + Math.cos(ang) * 14;
840	        const ay = this.player.cy - 4 + Math.sin(ang) * 14;
841	        const arrow = new Arrow(ax, ay, Math.cos(ang) * rg.projSpeed, Math.sin(ang) * rg.projSpeed, rg.damage, rg.ammo);
842	        this.entities.add(arrow, 'projectiles');
843	        this.player.inv.removeAt(ammoSlot, 1);
844	        this.player.useTime = rg.speed;
845	        this.sfx.play('tink');
846	        this.cb.onInventoryChanged();
847	      }
848	    } else if (heldDef && (heldDef.key === 'worm_food' || heldDef.key === 'bloody_spine' || heldDef.key === 'slime_crown')
849	      && inp.mouseDown && this.player.useTime === 0) {
850	      // Boss 召唤物(原版 worm food/bloody spine/slime crown)
851	      if (heldDef.key === 'worm_food') this.summonBoss('eater_of_worlds_head');
852	      else if (heldDef.key === 'bloody_spine') this.summonBoss('brain_of_cthulhu');
853	      else this.summonBoss('king_slime');
854	      this.player.inv.removeAt(this.player.inv.selected, 1);
855	      this.player.useTime = 60;
856	      this.cb.onInventoryChanged();
857	      this.input.mouseDown = false;
858	    } else if (heldDef?.magic && inp.mouseDown && this.player.useTime === 0) {
859	      // 魔法武器:消耗 mana → 发射魔法弹(Player.ItemCheck_Shoot 语义)
860	      const mg = heldDef.magic;
861	      if (this.player.mana < mg.manaCost) {
862	        this.cb.onToast('魔力不足');
863	        this.input.mouseDown = false;
864	      } else {
865	        this.player.mana -= mg.manaCost;
866	        const ang = Math.atan2(inp.mouseY - vh2 / 2, inp.mouseX - vw2 / 2);
867	        const mx = this.player.cx + Math.cos(ang) * 14;
868	        const my = this.player.cy - 4 + Math.sin(ang) * 14;
869	        const color = mg.proj === 'bolt' ? '#A040FF' : '#FFB040';
870	        const proj = new MagicProj(mx, my, Math.cos(ang) * mg.projSpeed, Math.sin(ang) * mg.projSpeed, mg.damage, 45, color);
871	        this.entities.add(proj, 'projectiles');
872	        this.player.useTime = mg.speed;
873	        this.sfx.play('tink');
874	        this.input.mouseDown = false;
875	      }
876	    } else if (heldDef && (heldDef.key === 'empty_bucket' || heldDef.key === 'water_bucket'
877	      || heldDef.key === 'lava_bucket' || heldDef.key === 'honey_bucket')) {
878	      this.useBucket(heldDef.key, tx, ty);
879	    }
880	    this.mining = null;
881	  }
882	
883	  private toolCanBreak(type: number, power: number, toolType: string): boolean {
884	    const d = TILE_DEFS[type];
885	    if (!d) return false;
886	    if (toolType === 'pick') return d.pick >= 0 && power >= d.pick;
887	    if (toolType === 'axe') return d.axe >= 0;
888	    return false;
889	  }
890	
891	  private tryMine(tx: number, ty: number, power: number, toolType: 'pick' | 'axe' | 'hammer', speed: number) {
892	    // 范围检查
893	    const dx = tx - Math.floor(this.player.cx / TILE);
894	    const dy = ty - Math.floor(this.player.cy / TILE);
895	    if (Math.hypot(dx, dy) > 4.5) { this.mining = null; return; }
896	    const type = this.world.store.get(tx, ty);
897	    // 锤：敲除背景墙（无墙则无事发生；也可清装饰）
898	    if (toolType === 'hammer') {
899	      // 原版语义:锤子优先循环实心块状态(整块→半砖→整块;坡面渲染未实现暂两态)
900	      if (type !== 0 && this.world.store.isSolid(tx, ty) && this.tickCount - this.lastMineHitTick >= Math.max(8, speed)) {
901	        this.lastMineHitTick = this.tickCount;
902	        const i = this.world.store.idx(tx, ty);
903	        const cur = this.world.store.half[i];
904	        this.world.store.setHalfBrick(tx, ty, !cur);
905	        this.sfx.play('tink');
906	        this.mining = null;
907	        return;
908	      }
909	      const wall = this.world.store.get(tx, ty) === 0 ? this.world.store.wall[this.world.store.idx(tx, ty)] : 0;
910	      if (type !== 0 && TILE_DEFS[type]?.decor) {
911	        this.breakTile(tx, ty);
912	        this.sfx.play('chop');
913	        this.mining = null;
914	        return;
915	      }
916	      if (!wall) { this.mining = null; return; }
917	      // HitTile 制（type 2 = 墙）：每挥一击，阈值 100
918	      if (this.tickCount - this.lastMineHitTick < Math.max(8, speed)) {
919	        this.hardnessCache = 100;
920	        this.mining = { x: tx, y: ty, progress: this.hitTiles.getDamage(tx, ty, 2) };
921	        return;
922	      }
923	      this.lastMineHitTick = this.tickCount;
924	      const total = this.hitTiles.addDamage(tx, ty, Math.round(power * 2), 2); // 锤墙：木 5 击 / 铜 2 击
925	      this.hardnessCache = 100;
926	      this.mining = { x: tx, y: ty, progress: total };
927	      this.spawnParticles(tx * TILE + 8, ty * TILE + 8, '#5C4436', 2, 1.2);
928	      if (total >= 100) {
929	        this.hitTiles.clear(tx, ty, 2);
930	        this.world.store.setWall(tx, ty, 0);
931	        this.spawnParticles(tx * TILE + 8, ty * TILE + 8, '#5C4436', 8, 1.8);
932	        this.sfx.play('chop');
933	        this.mining = null;
934	      }
935	      return;
936	    }
937	    if (type === 0 || !this.toolCanBreak(type, power, toolType)) {
938	      // 装饰物（杂草等）任意工具/武器一下清掉并掉落
939	      if (type !== 0 && TILE_DEFS[type]?.decor && (toolType === 'pick' || toolType === 'axe')) {
940	        this.breakTile(tx, ty);
941	        this.sfx.play('chop');
942	        this.mining = null;
943	        return;
944	      }
945	      this.mining = null;
946	      return;
947	    }
948	    // ---- 原版 HitTile 制（Player.PickTile 移植）：每挥一击积累伤害，阈值 100 破坏 ----
949	    // 每挥一击（按工具速度节流），伤害 = 工具力 × 材质系数（GetPickaxeDamage 简化）
950	    if (this.tickCount - this.lastMineHitTick < Math.max(8, speed)) {
951	      // 节流窗内：只刷新裂缝显示，不积累
952	      this.hardnessCache = 100;
953	      this.mining = { x: tx, y: ty, progress: this.hitTiles.getDamage(tx, ty) };
954	      return;
955	    }
956	    this.lastMineHitTick = this.tickCount;
957	    const d = TILE_DEFS[type];
958	    // 原版 GetPickaxeDamage：普通块 = 镐力；泥土族（0/40/53/57/59/123/147/224/397）= 镐力×2。
959	    // 矿石无系数（只靠镐力门槛 gate）；家具软质 ×2 保持原版 tileNoFail 方向。
960	    // 斧 = 斧力×1.2（原版 Player.cs:29576）——绝对值配原版节奏需十击太多，
961	    // 按同比例放大（≈斧力×5.5）适配我们的挥击间隔+衰减：铜斧 7→39（3 击）/ 金斧 11→61（2 击）
962	    let dmg: number;
963	    if (type === T.TREE || IMPORTED_TREE_TYPES.has(type)) {
964	      dmg = toolType === 'axe' ? Math.round(power * 5.5) : power;
965	    } else if (toolType === 'axe') {
966	      dmg = Math.round(power * 5.5);
967	    } else if (d.decor || (d.framed && !d.solid)) {
968	      dmg = power * 2;
969	    } else {
970	      const dirtFamily = /^(dirt|grass|sand|snow|mud|silt|clay|ash|slush|ebonsand|crimsand|pearlsand|hardened_sand)/i.test(d.key)
971	        || d.key === 'v_123_silt' || d.key === 'v_224_slush_block' || d.key === 'v_397_hardened_sand' || d.key === 'v_112_ebonsand_block';
972	      dmg = power * (dirtFamily ? 2 : 1);
973	    }
974	    const total = this.hitTiles.addDamage(tx, ty, dmg);
975	    this.hardnessCache = 100;
976	    this.mining = { x: tx, y: ty, progress: total }; // 裂缝显示 = 积累进度
977	    this.spawnParticles(tx * TILE + 8, ty * TILE + 8, d.mapColor, 2, 1.2);
978	    if (total >= 100) {
979	      this.hitTiles.clear(tx, ty);
980	      this.breakTile(tx, ty);
981	      this.mining = null;
982	      // 破坏完成音：按材质区分
983	      if (toolType === 'axe') this.sfx.play('chop');
984	      else if (/stone|ore|brick|obsidian|ash|gem_|fossil|silt/i.test(d.key)) this.sfx.play('tink');
985	      else this.sfx.play('dig');
986	    }
987	  }
988	
989	  private tileHardness(type: number): number {
990	    const d = TILE_DEFS[type];
991	    // 铜镐基准（52/tick）：泥土 ~0.25s / 石 ~0.6s / 铜矿 ~0.8s / 金矿 ~1.6s
992	    // 树（斧）：木斧 ~2s / 铜斧 ~1s / 金斧 ~0.4s
993	    if (type === T.TREE) return 3400;
994	    if (type === T.LEAVES) return 40;
995	    if (d.decor) return 60;
996	    if (d.framed && !d.solid) return 300;               // 工作台/铁砧等
997	    switch (type) {
998	      case T.DIRT: case T.GRASS: case T.SAND: case T.SNOW: return 780;
999	      case T.STONE: return 1870;
1000	      case T.WOOD: case T.PLATFORM: return 1250;
1001	      case T.ORE_COPPER: return 2500;
1002	      case T.ORE_IRON: return 3100;
1003	      case T.ORE_SILVER: return 4100;
1004	      case T.ORE_GOLD: return 5000;
1005	      default: return 1000;
1006	    }
1007	  }
1008	
1009	  /** 破坏 tile：处理树整体砍伐与 object 锚点 */
1010	  private breakTile(x: number, y: number) {
1011	    const st = this.world.store;
1012	    const type = st.get(x, y);
1013	    if (type === 0) return;
1014	    const def = TILE_DEFS[type];
1015	
1016	    // 树：砍树干 → 整棵树倒下（自有树 + 导入的原版树族）
1017	    if (type === T.TREE) {
1018	      this.fellTree(x, y);
1019	      return;
1020	    }
1021	    // 暗影之球/恶魔之心：整体破碎（原版 WorldGen.CheckOrb 移植）
1022	    if (type === TILE_BY_KEY['v_31_orb_heart']) {
1023	      this.smashOrbHeart(x, y);
1024	      return;
1025	    }
1026	    if (IMPORTED_TREE_TYPES.has(type)) {
1027	      this.fellImportedTree(x, y, type);
1028	      return;
1029	    }
1030	    // object：找锚点整体移除
1031	    if ((def.w ?? 1) > 1 || (def.h ?? 1) > 1) {
1032	      const fi = st.idx(x, y);
1033	      const fv = st.frameX[fi], fyv = st.frameY[fi];
1034	      // 原版家具帧是 18px 像素偏移，先归一成格偏移再找锚点
1035	      const gx = def.vanilla ? Math.floor(fv / 18) : fv;
1036	      const gy = def.vanilla ? Math.floor(fyv / 18) : fyv;
1037	      const ax = gx === 0 && gy === 0 ? x : x - gx;
1038	      const ay = gx === 0 && gy === 0 ? y : y - gy;
1039	      for (let dx = 0; dx < (def.w ?? 1); dx++) {
1040	        for (let dy = 0; dy < (def.h ?? 1); dy++) {
1041	          st.setTile(ax + dx, ay + dy, 0);
1042	        }
1043	      }
1044	      this.spawnDrop(ax * TILE + 8, ay * TILE, def.drop ?? (def.key.startsWith('v_') ? 'place_' + def.key : ''), 1);
1045	      // 宝箱内容物掉出
1046	      if (type === T.CHEST) this.dumpChest(ax, ay);
1047	      this.spawnParticles(x * TILE + 8, y * TILE + 8, def.mapColor, 8, 1.8);
1048	      return;
1049	    }
1050	    // 瓦罐：碎裂音 + 随机战利品（火把/炸弹/绳/小血瓶/铜币）
1051	    if (TILE_BY_KEY['pot'] !== undefined && type === TILE_BY_KEY['pot']) {
1052	      st.setTile(x, y, 0);
1053	      this.sfx.play('shatter');
1054	      this.spawnParticles(x * TILE + 8, y * TILE + 8, '#974F50', 10, 2);
1055	      const loot: Array<[string, number, number, number]> = [
1056	        // [itemKey, min, max, 概率]
1057	        ['torch', 3, 8, 0.55],
1058	        ['bomb', 1, 3, 0.22],
1059	        ['rope', 5, 15, 0.20],
1060	        ['lesser_healing_potion', 1, 1, 0.22],
1061	        ['coin_copper', 5, 20, 0.45],
1062	        ['gel', 1, 2, 0.15],
1063	      ];
1064	      for (const [key, mn, mx, ch] of loot) {
1065	        if (Math.random() < ch) {
1066	          this.spawnDrop(x * TILE + 8, y * TILE, key, mn + Math.floor(Math.random() * (mx - mn + 1)),
1067	            (Math.random() - 0.5) * 2.5, -2.5 - Math.random());
1068	        }
1069	      }
1070	      return;
1071	    }
1072	    // 普通
1073	    st.setTile(x, y, 0);
1074	    // 破坏树木正下方的支撑方块 → 整棵树倒下（掉木材）
1075	    const treeOnTop = this.world.trees.find((t) => t.x === x && t.y + t.h === y);
1076	    if (treeOnTop) this.fellTree(x, y - 1);
1077	    if (def.drop) this.spawnDrop(x * TILE + 8, y * TILE + 8, def.drop, 1);
1078	    this.spawnParticles(x * TILE + 8, y * TILE + 8, def.mapColor, 6, 1.5);
1079	  }
1080	
1081	  private fellTree(x: number, y: number) {
1082	    // 向上找树顶（同列 TREE tile），向下到 Grass
1083	    const st = this.world.store;
1084	    let top = y;
1085	    while (st.get(x, top - 1) === T.TREE) top--;
1086	    let bottom = y;
1087	    while (st.get(x, bottom + 1) === T.TREE) bottom++;
1088	    const height = bottom - top + 1;
1089	    // 树冠 80×80 以树顶为中心外扩 2-3 格：显式区域标脏，
1090	    // 否则不含树干格的邻 chunk 不会重绘 → 树叶残留
1091	    this.chunks.markDirtyArea(x - 4, top - 4, x + 4, bottom + 1);
1092	    // 清除树干 + 两侧树枝（支干只在紧邻树干处生成，不会误伤邻树），并记录枝干位置
1093	    const branchSpots: Array<{ x: number; y: number }> = [];
1094	    for (let yy = top; yy <= bottom; yy++) {
1095	      st.setTile(x, yy, 0);
1096	      for (const s of [-1, 1]) {
1097	        if (st.get(x + s, yy) === T.TREE) {
1098	          branchSpots.push({ x: x + s, y: yy });
1099	          st.setTile(x + s, yy, 0);
1100	        }
1101	      }
1102	    }
1103	    // 清除树冠（树顶周围半径 3 的 LEAVES）
1104	    for (let dx = -3; dx <= 3; dx++) {
1105	      for (let dy = -4; dy <= 1; dy++) {
1106	        if (st.get(x + dx, top + dy) === T.LEAVES) st.setTile(x + dx, top + dy, 0);
1107	      }
1108	    }
1109	    // 掉木材：树干每段 1 个独立掉落物沿干散落；每根枝干也额外掉 1 份（掉在枝干处）
1110	    const wood = Math.max(1, Math.floor(height * 0.8));
1111	    for (let p = 0; p < wood; p++) {
1112	      const dropY = (top + Math.floor((p + 0.5) * height / wood)) * TILE;
1113	      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
1114	    }
1115	    for (const b of branchSpots) {
1116	      this.spawnDrop(b.x * TILE + 8, b.y * TILE + 8, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
1117	    }
1118	    // 橡实：较大概率（75%）掉 2-3 颗，沿树冠区域散落供补种
1119	    if (Math.random() < 0.75) {
1120	      const nAcorn = 2 + Math.floor(Math.random() * 2);
1121	      for (let a = 0; a < nAcorn; a++) {
1122	        const ax = x + (Math.random() - 0.5) * 2.5;
1123	        const ay = top + Math.random() * height * 0.4;
1124	        this.spawnDrop(ax * TILE + 8, ay * TILE, 'acorn', 1, (Math.random() - 0.5) * 3, -3 - Math.random());
1125	      }
1126	    }
1127	    this.spawnParticles(x * TILE + 8, top * TILE + 8, '#2E8B3D', 14, 2.2);
1128	    // 从登记表移除
1129	    const t = this.world.trees.findIndex((tr) => tr.x === x && Math.abs(tr.y - top) <= 2);
1130	    if (t >= 0) this.world.trees.splice(t, 1);
1131	  }
1132	
1133	  /** 砍导入的原版树（tile 5 / 宝石树 / 装饰树 / 灰烬树）：
1134	   *  同列同类型连续段 = 整棵树（含顶部树冠标记格），整棵移除 + 掉木材。
1135	   *  首击即倒（不做倒树动画——动画实体绑定自有树的登记表结构） */
1136	  /** 暗影之球/恶魔之心整体破碎（原版 WorldGen.CheckOrb 移植，WorldGen.cs:31813-31960）：
1137	   *  帧锚点定位（frameX∈{0,36} 是左列）→ 2×2 四格一起清除；
1138	   *  战利品：首破固定（暗影之球:恶魔之心 + 凝胶100；恶魔之心:生命水晶 + 凝胶100），
1139	   *  之后 5 选 1 随机；无原版物品的部分用现有道具近似 */
1140	  private smashOrbHeart(x: number, y: number) {
1141	    const st = this.world.store;
1142	    const orbId = TILE_BY_KEY['v_31_orb_heart'];
1143	    const i = st.idx(x, y);
1144	    const fx = st.frameX[i];
1145	    const isDemonHeart = fx >= 36; // 原版：frameX ≥ 36 = 恶魔之心（猩红世界）
1146	    const ax = (fx === 0 || fx === 36) ? x : x - 1;
1147	    const ay = st.frameY[i] !== 0 ? y - 1 : y;
1148	    this.chunks.markDirtyArea(ax - 1, ay - 1, ax + 2, ay + 2);
1149	    for (let dx = 0; dx < 2; dx++) {
1150	      for (let dy = 0; dy < 2; dy++) st.setTile(ax + dx, ay + dy, 0);
1151	    }
1152	    // 战利品（近似：首破固定 + 之后随机）
1153	    const drops: Array<[string, number]> = !this.world.flags.shadowOrbSmashed
1154	      ? (isDemonHeart ? [['coin_gold', 1], ['gel', 100]] : [['suspicious_eye', 1], ['gel', 100]])
1155	      : [['coin_silver', 5], ['gel', 60]];
1156	    for (const [key, n] of drops) {
1157	      this.spawnDrop(ax * TILE + 8, ay * TILE + 8, key, n, (Math.random() - 0.5) * 3, -3);
1158	    }
1159	    this.spawnParticles(ax * TILE + 16, ay * TILE + 16, isDemonHeart ? '#FF4060' : '#9A6AE0', 16, 2.5);
1160	    this.sfx.play('tink');
1161	    this.cb.onToast(isDemonHeart ? '恶魔之心被击碎了！' : '暗影之球被击碎了！');
1162	    if (!this.world.flags.shadowOrbSmashed) {
1163	      this.world.flags.shadowOrbSmashed = true;
1164	    }
1165	  }
1166	
1167	  private fellImportedTree(x: number, y: number, type: number) {
1168	    const st = this.world.store;
1169	    let top = y;
1170	    while (st.get(x, top - 1) === type) top--;
1171	    let bottom = y;
1172	    while (st.get(x, bottom + 1) === type) bottom++;
1173	    const height = bottom - top + 1;
1174	    this.chunks.markDirtyArea(x - 6, top - 7, x + 6, bottom + 1);
1175	    // 清树干列 + 紧邻的侧枝（同类型，仅 ±1 防 "格洞" 残留）
1176	    for (let yy = top; yy <= bottom; yy++) {
1177	      st.setTile(x, yy, 0);
1178	      for (const s of [-1, 1]) {
1179	        if (st.get(x + s, yy) === type) st.setTile(x + s, yy, 0);
1180	      }
1181	    }
1182	    // 掉木材（与自有树同比例）+ 树顶枝条额外几份
1183	    const wood = Math.max(1, Math.floor(height * 0.8));
1184	    for (let p = 0; p < wood; p++) {
1185	      const dropY = (top + Math.floor((p + 0.5) * height / wood)) * TILE;
1186	      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
1187	    }
1188	    // 橡实：与自有树同规则（75% 掉 2-3 颗，沿树冠区域散落供补种）
1189	    if (Math.random() < 0.75) {
1190	      const nAcorn = 2 + Math.floor(Math.random() * 2);
1191	      for (let a = 0; a < nAcorn; a++) {
1192	        const ax = x + (Math.random() - 0.5) * 2.5;
1193	        const ay = top + Math.random() * height * 0.4;
1194	        this.spawnDrop(ax * TILE + 8, ay * TILE, 'acorn', 1, (Math.random() - 0.5) * 3, -3 - Math.random());
1195	      }
1196	    }
1197	    this.spawnParticles(x * TILE + 8, top * TILE + 8, '#2E8B3D', 14, 2.2);
1198	  }
1199	
1200	  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
1201	    const st = this.world.store;
1202	    if (!st.inBounds(tx, ty)) return;
1203	    // 距离
1204	    const dx = tx - Math.floor(this.player.cx / TILE);
1205	    const dy = ty - Math.floor(this.player.cy / TILE);
1206	    if (Math.hypot(dx, dy) > 5.5) return;
1207	    const tileId = TILE_BY_KEY[itemDef.tile!];
1208	    const def = TILE_DEFS[tileId];
1209	    // 橡实: 只能种在草块正上方
1210	    if (itemDef.key === 'acorn' && st.get(tx, ty + 1) !== T.GRASS) {
1211	      this.cb.onToast('橡实只能种在草块上');
1212	      return;
1213	    }
1214	    const ow = def.w ?? 1, oh = def.h ?? 1;
1215	    // 绳索(RopeCoil 语义):从放置点向下延伸至实心/最多 10 格
1216	    if (itemDef.key === 'rope') {
1217	      const ropeTile = TILE_BY_KEY['v_213_rope']!;
1218	      let placed = 0;
1219	      for (let y = ty; y < ty + 10; y++) {
1220	        if (!st.inBounds(tx, y) || st.isActive(tx, y)) break;
1221	        st.setTile(tx, y, ropeTile, 0, 0);
1222	        placed++;
1223	      }
1224	      if (placed > 0) {
1225	        this.player.inv.removeAt(this.player.inv.selected, 1);
1226	        this.player.useTime = 14;
1227	        this.sfx.play('place');
1228	        this.cb.onInventoryChanged();
1229	      }
1230	      return;
1231	    }
1232	    // 放置空间检查
1233	    for (let dx2 = 0; dx2 < ow; dx2++) {
1234	      for (let dy2 = 0; dy2 < oh; dy2++) {
1235	        const px = tx + dx2, py = ty + dy2;
1236	        if (!st.inBounds(px, py)) return;
1237	        if (st.isActive(px, py)) return;
1238	        // 实心物不能与玩家重叠
1239	        if (def.solid && this.overlapsEntity(px, py)) return;
1240	      }
1241	    }
1242	    // 支撑检查：非漂浮（简化：需要任意相邻格有内容或墙）
1243	    const needSupport = def.solid || def.platform || def.framed;
1244	    if (needSupport && !this.hasSupport(tx, ty, ow, oh)) return;
1245	    if (this.player.useTime > 0) return;
1246	
1247	    // 放置
1248	    const isVanillaStyle = !!def.vanilla && def.vanilla.frame === 'style';
1249	    for (let dx2 = 0; dx2 < ow; dx2++) {
1250	      for (let dy2 = 0; dy2 < oh; dy2++) {
1251	        const px = tx + dx2, py = ty + dy2;
1252	        // 原版多格家具：帧用 18px 步长偏移（与 .wld 原生一致，渲染端直用）。
1253	        // 原版帧语义（TileObject.Place L74-102）：frameY 从【顶行 = 0】向下递增；
1254	        // ty 是顶部行（放置时鼠标指向顶部锚点）→ dy2=0 即顶行，frameY = dy2*18 正确
1255	        if (isVanillaStyle) {
1256	          // placeStyle:样式索引 → X 偏移 style*fw*18(2 宽物件步长 36,3 宽 54)
1257	          const strideX = (def.vanilla?.fw ?? 1) * 18;
1258	          st.setTile(px, py, tileId, (itemDef.placeStyle ?? 0) * strideX + dx2 * 18, dy2 * 18);
1259	        } else {
1260	          st.setTile(px, py, tileId, dx2, dy2);
1261	        }
1262	        // 水被方块挤出：水量转移到相邻可容纳的格子（上/左/右），
1263	        // 而不是被方块吞掉消失。封闭无处可去时才消失
1264	        const pi = st.idx(px, py);
1265	        const liq = st.liquid[pi];
1266	        if (liq > 0) {
1267	          const ltype = st.liquidType[pi];
1268	          st.setLiquid(px, py, 0, 0);
1269	          let remaining = liq;
1270	          for (const [ox, oy] of [[0, -1], [-1, 0], [1, 0]] as const) {
1271	            if (remaining <= 0) break;
1272	            const nx = px + ox, ny = py + oy;
1273	            if (!st.inBounds(nx, ny)) continue;
1274	            const nd = TILE_DEFS[st.type[st.idx(nx, ny)]];
1275	            if (nd && nd.solid) continue;
1276	            const ni = st.idx(nx, ny);
1277	            const cap = 255 - st.liquid[ni];
1278	            if (cap <= 0) continue;
1279	            const t = Math.min(remaining, cap);
1280	            st.setLiquid(nx, ny, st.liquid[ni] + t, ltype || st.liquidType[ni] || 1);
1281	            remaining -= t;
1282	          }
1283	        }
1284	      }
1285	    }
1286	    if (tileId === T.CHEST) {
1287	      this.world.chests.push({ x: tx, y: ty, items: Array(10).fill(null) });
1288	    }
1289	    this.player.inv.removeAt(this.player.inv.selected, 1);
1290	    this.player.useTime = 14;
1291	    this.sfx.play('place');
1292	    this.cb.onInventoryChanged();
1293	  }
1294	
1295	  private overlapsEntity(px: number, py: number): boolean {
1296	    const rx = px * TILE, ry = py * TILE;
1297	    if (this.player.x < rx + TILE && this.player.x + this.player.w > rx && this.player.y < ry + TILE && this.player.y + this.player.h > ry) return true;
1298	    for (const e of this.entities.enemies) {
1299	      if (e.x < rx + TILE && e.x + e.w > rx && e.y < ry + TILE && e.y + e.h > ry) return true;
1300	    }
1301	    return false;
1302	  }
1303	
1304	  private hasSupport(x: number, y: number, w: number, h: number): boolean {
1305	    const st = this.world.store;
1306	    // 下方
1307	    for (let dx = 0; dx < w; dx++) {
1308	      if (st.isActive(x + dx, y + h) || st.isSolid(x + dx, y + h) || st.wall[st.idx(x + dx, y + h)] !== 0) return true;
1309	    }
1310	    // 上方（火把等贴墙物）
1311	    for (let dx = 0; dx < w; dx++) {
1312	      if (st.isActive(x + dx, y - 1)) return true;
1313	    }
1314	    // 侧邻
1315	    for (let dy = 0; dy < h; dy++) {
1316	      if (st.isActive(x - 1, y + dy) || st.isActive(x + w, y + dy)) return true;
1317	    }
1318	    return false;
1319	  }
1320	
1321	  private interactAt(tx: number, ty: number) {
1322	    const st = this.world.store;
1323	    const type = st.get(tx, ty);
1324	    if (type === T.DOOR_CLOSED) {
1325	      // 切换为开门
1326	      const isOpen = st.get(tx + 1, ty) !== 0 || st.get(tx + 1, ty + 1) !== 0 || st.get(tx + 1, ty + 2) !== 0;
1327	      this.toggleDoor(tx, ty, true, isOpen);
1328	      this.input.rightDown = false;
1329	    } else if (type === T.DOOR_OPEN) {
1330	      this.toggleDoor(tx, ty, false, false);
1331	      this.input.rightDown = false;
1332	    } else if (type === T.CHEST) {
1333	      // 打开宝箱：精确命中或 3×3 容差（点击宝箱边缘也算）
1334	      const chest = this.findChest(tx, ty) ?? this.findChestNear(tx, ty);
1335	      if (chest) this.tryOpenChest(chest);
1336	    } else if (type === TILE_BY_KEY['crystal_heart']) {
1337	      // 生命水晶(放置态):右键使用(Player.cs ItemCheck_UseLifeCrystal L29358)
1338	      // statLifeMax<400 → +20 上限并回满该部分,放置物消耗
1339	      this.usePlacedLifeCrystal(tx, ty);
1340	    } else if (type === TILE_BY_KEY['bed']) {
1341	      // 床:设重生点(vanilla Player.FindBed 语义;敌怪环绕检查略)
1342	      this.world.spawnX = tx + 1;
1343	      this.world.spawnY = ty - 1;
1344	      this.cb.onToast('重生点已设置');
1345	      this.input.rightDown = false;
1346	    } else if (type === TILE_BY_KEY['v_132_lever'] || type === TILE_BY_KEY['v_136_switch']) {
1347	      // 拉杆/开关:切换通断(帧 +18 翻转),触发直线可见的陷阱(WorldGen Wiring 简化)
1348	      this.toggleSwitch(tx, ty, type);
1349	    } else if (type === TILE_BY_KEY['v_83_herbs_mature'] || type === TILE_BY_KEY['v_84_herbs_bloom']) {
1350	      // 药草收获:成熟/开花态右键 → 掉种子(style 对应 frameX/36)
1351	      const i = st.idx(tx, ty);
1352	      const style = Math.floor(st.frameX[i] / 36);
1353	      st.setTile(tx, ty, 0);
1354	      const seedKeys = ['vi_307_daybloom_seeds', 'vi_308_moonglow_seeds', 'vi_309_blinkroot_seeds',
1355	        'vi_311_waterleaf_seeds', 'vi_310_deathweed_seeds', 'vi_312_fireblossom_seeds', 'vi_2357_shiverthorn_seeds'];
1356	      const sk = seedKeys[style] ?? seedKeys[0];
1357	      this.spawnDrop(tx * 16 + 8, ty * 16, sk, 1);
1358	      this.input.rightDown = false;
1359	    }
1360	  }
1361	
1362	  /** 放置态生命水晶使用(Player.cs:29358:statLifeMax≥400 拒绝,+20 上限+回复,消耗) */
1363	  private usePlacedLifeCrystal(tx: number, ty: number): void {
1364	    const st = this.world.store;
1365	    const def = TILE_DEFS[st.get(tx, ty)];
1366	    if (this.player.baseMaxHp >= 400) {
1367	      this.cb.onToast('生命上限已达到 400');
1368	      this.input.rightDown = false;
1369	      return;
1370	    }
1371	    this.player.baseMaxHp += 20;
1372	    this.player.hp = Math.min(this.player.maxHp, this.player.hp + 20);
1373	    this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#40E080');
1374	    // 消耗放置物(2×2)
1375	    for (let dx = 0; dx < 2; dx++) {
1376	      for (let dy = 0; dy < 2; dy++) {
1377	        if (st.get(tx + dx, ty + dy) === TILE_BY_KEY['crystal_heart']) st.setTile(tx + dx, ty + dy, 0);
1378	      }
1379	    }
1380	    this.sfx.play('drink');
1381	    this.input.rightDown = false;
1382	    void def;
1383	  }
1384	
1385	  /** 开宝箱统一入口:锁定箱(原版 Chest.locked)需金钥匙,首次开启消耗 */
1386	  private tryOpenChest(chest: { locked?: boolean }): void {
1387	    if (chest.locked) {
1388	      const keyId = ITEM_BY_KEY['vi_327_golden_key'];
1389	      let keySlot = -1;
1390	      for (let i = 0; i < this.player.inv.slots.length; i++) {
1391	        const sl = this.player.inv.slots[i];
1392	        if (sl && sl.id === keyId && sl.stack > 0) { keySlot = i; break; }
1393	      }
1394	      if (keySlot < 0) { this.cb.onToast('宝箱被锁住了,需要金钥匙'); this.input.rightDown = false; return; }
1395	      this.player.inv.removeAt(keySlot, 1);
1396	      chest.locked = false;
1397	      this.sfx.play('tink');
1398	      this.cb.onToast('用金钥匙打开了宝箱');
1399	      this.cb.onInventoryChanged();
1400	    }
1401	    this.openChest?.(chest as never);
1402	    this.input.rightDown = false;
1403	  }
1404	
1405	  /** 拉杆/开关切换:帧翻转(原版 style 内 on/off 两态),直线驱动陷阱 */
1406	  private toggleSwitch(x: number, y: number, type: number): void {
1407	    const st = this.world.store;
1408	    const i = st.idx(x, y);
1409	    const on = st.frameX[i] >= 18;
1410	    st.setTile(x, y, type, on ? 0 : 18, st.frameY[i]);
1411	    this.sfx.play('tink');
1412	    this.fireTrapsFrom(x, y, !on);
1413	    this.input.rightDown = false;
1414	  }
1415	
1416	  /** 从电源点向四方向直线扫描 ≤60 格,遇陷阱(无实心阻挡)发射飞镖 */
1417	  private fireTrapsFrom(px: number, py: number, powerOn: boolean): void {
1418	    if (!powerOn) return;
1419	    const st = this.world.store;
1420	    const TRAP = TILE_BY_KEY['v_137_traps'];
1421	    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
1422	      for (let d = 1; d <= 60; d++) {
1423	        const x = px + dx * d, y = py + dy * d;
1424	        if (!st.inBounds(x, y)) break;
1425	        if (st.isSolid(x, y) && st.get(x, y) !== TRAP) break;
1426	        if (st.get(x, y) === TRAP) {
1427	          const key = x + ',' + y;
1428	          const last = this.trapCooldown.get(key) ?? -999;
1429	          if (this.tickCount - last < 40) return;
1430	          this.trapCooldown.set(key, this.tickCount);
1431	          const dart = new Dart(x * TILE + 8 + dx * 10, y * TILE + 8 + dy * 10, dx * 9, dy * 9, 20);
1432	          this.entities.add(dart, 'projectiles');
1433	          this.sfx.play('tink');
1434	          return;
1435	        }
1436	      }
1437	    }
1438	  }
1439	
1440	  /** 压力板:玩家踩上瞬间触发(原版 PressurePlate 语义,人触发灰板) */
1441	  private checkPressurePlates(): void {
1442	    const st = this.world.store;
1443	    const p = this.player;
1444	    const tx = Math.floor(p.cx / TILE), ty = Math.floor((p.y + p.h) / TILE);
1445	    const key = tx + ',' + ty;
1446	    if (st.get(tx, ty) === TILE_BY_KEY['v_135_pressure_plates'] && !this.plateLatch.has(key)) {
1447	      this.plateLatch.add(key);
1448	      this.fireTrapsFrom(tx, ty, true);
1449	    } else if (st.get(tx, ty) !== TILE_BY_KEY['v_135_pressure_plates']) {
1450	      this.plateLatch.delete(key);
1451	    }
1452	  }
1453	
1454	  /** 桶三态(Player.cs ItemCheck_Buckets L28137 语义):
1455	   *  空桶点液体 → 舀成对应满桶;满桶点空格 → 放置液体变空桶 */
1456	  private useBucket(key: string, tx: number, ty: number): void {
1457	    const st = this.world.store;
1458	    const liqTypeMap: Record<string, number> = { water_bucket: 1, lava_bucket: 2, honey_bucket: 3 };
1459	    const swap = (toKey: string) => {
1460	      // 原版语义:桶在手中原格替换(不跳格)
1461	      this.player.inv.slots[this.player.inv.selected] = { id: ITEM_BY_KEY[toKey], stack: 1 };
1462	      this.cb.onInventoryChanged();
1463	      this.player.useTime = 30;
1464	      this.input.rightDown = false;
1465	    };
1466	    if (key === 'empty_bucket') {
1467	      const i = st.idx(tx, ty);
1468	      if (st.liquid[i] > 0) {
1469	        const t = st.liquidType[i] || 1;
1470	        st.setLiquid(tx, ty, 0, 0);
1471	        swap(t === 2 ? 'lava_bucket' : t === 3 ? 'honey_bucket' : 'water_bucket');
1472	      }
1473	    } else {
1474	      // 满桶:目标格须空且(相邻可铺展/有底)——简化:空即可
1475	      const i = st.idx(tx, ty);
1476	      if (!st.flags[i]) {
1477	        const lt = liqTypeMap[key];
1478	        st.setLiquid(tx, ty, 255, lt);
1479	        swap('empty_bucket');
1480	      }
1481	    }
1482	  }
1483	
1484	  private toggleDoor(x: number, y: number, open: boolean, flipLeft: boolean) {
1485	    const st = this.world.store;
1486	    // 找锚点（帧可能是格偏移或 vanilla 18px 偏移——统一按格归一）
1487	    const defClosed = TILE_DEFS[T.DOOR_CLOSED];
1488	    const step = defClosed.vanilla ? 18 : 1;
1489	    const fx = st.frameX[st.idx(x, y)], fy = st.frameY[st.idx(x, y)];
1490	    const ax = (fx === 0 && fy === 0) ? x : x - Math.floor(fx / step);
1491	    const ay = (fx === 0 && fy === 0) ? y : y - Math.floor(fy / step);
1492	    void flipLeft;
1493	    // 开门状态占 2 列，全部清掉再放新状态
1494	    for (let dx = 0; dx < 2; dx++) {
1495	      for (let dy = 0; dy < 3; dy++) {
1496	        if (st.inBounds(ax + dx, ay + dy)) st.setTile(ax + dx, ay + dy, 0);
1497	      }
1498	    }
1499	    if (open) {
1500	      for (let dx = 0; dx < 2; dx++) {
1501	        for (let dy = 0; dy < 3; dy++) {
1502	          if (st.inBounds(ax + dx, ay + dy)) st.setTile(ax + dx, ay + dy, T.DOOR_OPEN, dx * 18, dy * 18);
1503	        }
1504	      }
1505	      this.sfx.play('door_open');
1506	    } else {
1507	      for (let dy = 0; dy < 3; dy++) st.setTile(ax, ay + dy, T.DOOR_CLOSED, 0, dy * 18);
1508	      this.sfx.play('door_close');
1509	    }
1510	  }
1511	
1512	  openChest: ((c: ChestData) => void) | null = null;
1513	
1514	  private findChest(tx: number, ty: number): ChestData | null {
1515	    for (const c of this.world.chests) {
1516	      if ((c.x === tx || c.x + 1 === tx) && (c.y === ty || c.y + 1 === ty)) return c;
1517	    }
1518	    return null;
1519	  }
1520	
1521	  /** 3×3 邻域内找宝箱（点击容差） */
1522	  private findChestNear(tx: number, ty: number): ChestData | null {
1523	    for (let dy = -1; dy <= 1; dy++) {
1524	      for (let dx = -1; dx <= 1; dx++) {
1525	        const c = this.findChest(tx + dx, ty + dy);
1526	        if (c) return c;
1527	      }
1528	    }
1529	    return null;
1530	  }
1531	
1532	  private dumpChest(x: number, y: number) {
1533	    const c = this.findChest(x, y);
1534	    if (!c) return;
1535	    for (const item of c.items) {
1536	      if (item) this.spawnDrop(x * TILE + 16, y * TILE, ITEM_DEFS[item.id].key, item.stack);
1537	    }
1538	    this.world.chests = this.world.chests.filter((cc) => cc !== c);
1539	  }
1540	
1541	  // ================= 战斗 =================
1542	
1543	  private updateSwingHits() {
1544	    if (!this.swing) return;
1545	    this.swing.t--;
1546	    if (this.swing.t <= 0) { this.swing = null; return; }
1547	    const held = this.player.inv.heldItem();
1548	    if (!held) return;
1549	    const tool = ITEM_DEFS[held.id].tool;
1550	    // 近战判定范围因武器而异：剑用完整 reach；镐/斧/锤当武器不顺手（×0.8）；
1551	    // 空手默认 3 格
1552	    const reach = (tool?.reach ?? TILE * 3) * (tool?.type === 'sword' ? 1 : tool ? 0.8 : 1);
1553	    // 剑/工具挥舞顺带清除鼠标处的杂草
1554	    {
1555	      const [htx, hty] = this.camera.tileUnder(this.input.mouseX, this.input.mouseY);
1556	      if (this.world.store.get(htx, hty) === T.TALLGRASS) this.breakTile(htx, hty);
1557	    }
1558	    // 弧线判定：圆心向朝向方向平移（身后不再被波及；小动物/怪物共用同一判定圆）
1559	    const arcX = this.player.cx + this.player.facing * reach * 0.35;
1560	    const prog = 1 - this.swing.t / this.swing.dur;
1561	    // 小动物：任何挥击一击致死
1562	    for (const cent of this.entities.critters) {
1563	      const c = cent as Critter;
1564	      if (this.swingHitSet.has(c.id)) continue;
1565	      const cdx = c.cx - arcX, cdy = c.cy - this.player.cy;
1566	      if (Math.hypot(cdx, cdy) <= reach + c.w / 2) {
1567	        this.swingHitSet.add(c.id);
1568	        c.hurt(this);
1569	      }
1570	    }
1571	    for (const ent of this.entities.enemies) {
1572	      const e = ent as Enemy;
1573	      if (this.swingHitSet.has(e.id)) continue;
1574	      const dx = e.cx - arcX;
1575	      const dy = e.cy - this.player.cy;
1576	      const dist = Math.hypot(dx, dy);
1577	      if (dist > reach + e.w / 2) continue;
1578	      // 朝向检查（挥舞半程后命中判定放宽）
1579	      if (Math.sign(dx) !== this.player.facing && Math.abs(dx) > e.w / 2) continue;
1580	      this.swingHitSet.add(e.id);
1581	      // 怪物专属受击声（各家族不同）；播放失败回退通用 hit
1582	      if (!this.sfx.playFiles(e.def.hitSound)) this.sfx.play('hit');
1583	      const crit = Math.random() < 0.04; // 原版近战基础暴击 4%（Player.meleeCrit）
1584	      // 工具（镐/斧）也有攻击力但远弱于剑：功率/16（铁镐 3 / 铁斧 4，铁剑 16）—— 仅应急
1585	      const baseDmg = tool?.damage ?? Math.max(1, Math.ceil((tool?.power ?? 10) / 16));
1586	      // 原版 Main.DamageVar：±15% 浮动（1 + rand(-15..15)/100）
1587	      const dmg = Math.max(1, Math.round((baseDmg + this.player.meleeDamageBonus) * (crit ? 2 : 1) * (1 + (Math.random() * 30 - 15) / 100)));
1588	      const kdir = Math.sign(dx) || this.player.facing;
1589	      // 击退 = 工具官方击退值（原版 knockBack 2-5.5 → 速度系数 0.65）
1590	      const kb = (tool?.knockback ?? 3) * 0.65;
1591	      const killed = e.hurt(dmg, kdir * kb, -2.5, this);
1592	      this.addDamageNumber(e.cx, e.y, dmg, crit, crit ? '#FFD040' : '#FF7060');
1593	      if (killed && e.def.boss) { /* boss 死亡处理在 fixedUpdate */ }
1594	    }
1595	    void prog;
1596	  }
1597	
1598	  // ================= 生成 =================
1599	
1600	  private trySpawnEnemy() {
1601	    const w = this.world;
1602	    const p = this.player;
1603	    if (p.dead) return;
1604	    const isDay = w.clock.isDay;
1605	    const count = this.entities.enemies.filter((e) => !(e as Enemy).def.boss && !(e as Enemy).wormFollow).length;
1606	    if (count >= ENEMY_CAP) return;
1607	    if (this.boss) return;
1608	
1609	    const rng = new RNG((Math.random() * 1e9) | 0);
1610	    // 生成点：玩家周围环带
1611	    const ang = rng.range(0, Math.PI * 2);
1612	    const dist = rng.range(SPAWN_MIN_DIST, SPAWN_MAX_DIST);
1613	    const ex = p.cx + Math.cos(ang) * dist;
1614	    const ey = p.cy + Math.sin(ang) * dist;
1615	    const tx = Math.floor(ex / TILE), ty = Math.floor(ey / TILE);
1616	    const st = w.store;
1617	    if (!st.inBounds(tx, ty) || tx < 2 || tx > st.w - 3) return;
1618	
1619	    const isUnderground = st.wall[st.idx(tx, ty)] !== 0 || ty > w.rockLevel;
1620	    // 海洋/水域排除：该列从天空到 rockLevel 全是液体 = 海里——除鱼类外不生成
1621	    // （蝙蝠等飞行怪在海面上盘旋也不合理，一并排除）
1622	    {
1623	      let liquidTop = -1;
1624	      for (let y = 2; y < Math.min(w.rockLevel, st.h); y++) {
1625	        if (st.liquid[st.idx(tx, y)] > 40) { liquidTop = y; break; }
1626	      }
1627	      if (liquidTop >= 0) {
1628	        // 水面之下 10 格仍是液体 → 判定为海/深水区
1629	        let deep = true;
1630	        for (let y = liquidTop; y < Math.min(liquidTop + 10, st.h); y++) {
1631	          if (st.liquid[st.idx(tx, y)] <= 40) { deep = false; break; }
1632	        }
1633	        if (deep) return;
1634	      }
1635	    }
1636	    // 地狱区：熔岩史莱姆 / 熔岩僵尸（不怕岩浆）
1637	    const hellTop = Math.floor(st.h * 0.86);
1638	    let key: string | null = null;
1639	    if (ty > hellTop) {
1640	      key = rng.chance(0.55) ? 'lava_slime' : 'magma_zombie';
1641	    } else if (isUnderground) {
1642	      key = rng.chance(0.6) ? 'cave_bat' : (rng.chance(0.5) ? 'slime_blue' : 'slime_green');
1643	    } else if (isDay) {
1644	      key = 'slime_green';
1645	    } else {
1646	      // 夜间地表：僵尸/恶魔眼/史莱姆——洞穴蝙蝠不在此列（只在洞里）
1647	      const r = rng.next();
1648	      key = r < 0.4 ? 'zombie' : r < 0.75 ? 'demon_eye' : 'slime_blue';
1649	    }
1650	    const def = ENEMY_DEFS[key];
1651	    if (def.nightOnly && isDay) return;
1652	    if (def.dayOnly && !isDay && !isUnderground) { /* 史莱姆夜间也可少量 */ }
1653	    // 找落脚点：从 ty 向下找空中有地面的位置
1654	    let spawnY = -1;
1655	    // 原版数据驱动怪（50% 概率从原版生成池选，属性/AI/贴图全走 vanilla-npcs.json）
1656	    let vanillaSpawn: Enemy | null = null;
1657	    if (rng.chance(0.5)) {
1658	      const pool = poolFor(Math.floor(w.groundLevel), st.h - 200, ty, isDay);
1659	      const vid = pool[(rng.next() * pool.length) | 0];
1660	      vanillaSpawn = Enemy.fromVanilla(vid, 0, 0);
1661	    }
1662	    const effDef = vanillaSpawn?.def ?? def;
1663	    // 蠕虫族（aiStyle 6）穿墙钻地：直接用环带点生成，不找空中落脚位
1664	    if (vanillaSpawn?.vanilla?.aiStyle === 6) {
1665	      vanillaSpawn.x = tx * TILE + 8 - vanillaSpawn.w / 2;
1666	      vanillaSpawn.y = ty * TILE + 8 - vanillaSpawn.h / 2;
1667	      vanillaSpawn.id = this.entities.nextId++;
1668	      this.entities.enemies.push(vanillaSpawn);
1669	      const segs = Enemy.spawnWormChain(vanillaSpawn, 5 + ((rng.next() * 4) | 0));
1670	      for (const s of segs) { s.id = this.entities.nextId++; this.entities.enemies.push(s); }
1671	      return;
1672	    }
1673	    for (let dy = -8; dy <= 12; dy++) {
1674	      const yy = ty + dy;
1675	      if (yy < 2 || yy > st.h - 3) continue;
1676	      // 落脚点必须无液体（方块之上有水 = 水下/水面，非鱼类不生成——
1677	      // 否则史莱姆会从湖/海底生成然后浮上来）
1678	      const dry = st.liquid[st.idx(tx, yy)] <= 40 && st.liquid[st.idx(tx, yy - 1)] <= 40;
1679	      const clear = !st.isSolid(tx, yy) && !st.isSolid(tx, yy - 1) && dry;
1680	      const ground = st.isSolid(tx, yy + 1) || st.isSolid(tx, yy + 2);
1681	      if (effDef.flying) {
1682	        if (!st.isSolid(tx, yy) && dry) { spawnY = yy; break; }
1683	      } else if (clear && ground) {
1684	        spawnY = yy;
1685	        break;
1686	      }
1687	    }
1688	    if (spawnY < 0) return;
1689	    // 地表暗处不生成（夜间地表有天空光 0.12，算可见）
1690	    if (vanillaSpawn) {
1691	      vanillaSpawn.x = tx * TILE + 8 - vanillaSpawn.w / 2;
1692	      vanillaSpawn.y = spawnY * TILE + TILE - vanillaSpawn.h;
1693	      vanillaSpawn.id = this.entities.nextId++;
1694	      this.entities.enemies.push(vanillaSpawn);
1695	      // 蠕虫族（aiStyle 6）：生成身×n+尾的段链（原版 NewNPC 链 NPC.cs:18174+）
1696	      if (vanillaSpawn.vanilla?.aiStyle === 6 && vanillaNpc(vanillaSpawn.vanillaId! + 1)) {
1697	        const segs = Enemy.spawnWormChain(vanillaSpawn, 5 + ((rng.next() * 4) | 0));
1698	        for (const s of segs) { s.id = this.entities.nextId++; this.entities.enemies.push(s); }
1699	      }
1700	      return;
1701	    }
1702	    this.spawnEnemy(key, tx * TILE + 8, spawnY * TILE);
1703	  }
1704	
1705	  // ================= NPC =================
1706	
1707	  private checkHousing() {
1708	    // 向导已随世界出生；此处仅在有合格房屋时为其安家
1709	    const guide = this.entities.npcs.find((n) => (n as TownNPC).npcKey === 'guide') as TownNPC | undefined;
1710	    if (!guide || guide.home) return;
1711	    const st = this.world.store;
1712	    outer:
1713	    for (let x = 3; x < st.w - 3; x++) {
1714	      for (let y = 3; y < st.h - 4; y++) {
1715	        if (st.get(x, y) !== T.DOOR_CLOSED) continue;
1716	        if (this.isValidHouse(x, y)) {
1717	          guide.home = { x: x + 2, y: y - 2 };
1718	          break outer;
1719	        }
1720	      }
1721	    }
1722	  }
1723	
1724	  /** 右键与附近 NPC 交谈(#13):点击目标须在 NPC 4 格内(否则不拦截右键交互) */
1725	  private talkToNearbyNpc(ctX: number, ctY: number): boolean {
1726	    const p = this.player;
1727	    for (const n of this.entities.npcs) {
1728	      const npc = n as TownNPC;
1729	      if (Math.hypot(npc.cx - p.cx, npc.cy - p.cy) > TILE * 3.5) continue;
1730	      if (Math.hypot(npc.cx - (ctX + 0.5) * TILE, npc.cy - (ctY + 1) * TILE) > TILE * 2) continue;
1731	      const tips = [
1732	        '你好！我是向导。按 E 打开背包，那里可以合成物品。',
1733	        '用镐挖矿、斧砍树。木头+凝胶可以做火把！',
1734	        '夜里会有僵尸和恶魔眼出现，小心行事。',
1735	        '挖到矿石后，用熔炉炼锭、铁砧做更好的装备。',
1736	        '手持火把也能照亮周围，不用非得放置。',
1737	        '想知道更多？去地下找找宝箱吧！',
1738	      ];
1739	      if (npc.npcKey === 'nurse') {
1740	        // 护士:50 铜币治疗至满(原版 Nurse 治疗费随缺失血量;简化固定)
1741	        if (npc.talkCooldown <= 0) {
1742	          if (p.hp >= p.maxHp) { this.cb.onToast('护士:你很健康,不需要我'); }
1743	          else {
1744	            const coinId2 = ITEM_BY_KEY['coin_copper'];
1745	            let coins2 = 0;
1746	            for (const sl of this.player.inv.slots) if (sl && sl.id === coinId2) coins2 += sl.stack;
1747	            if (coins2 < 50) { this.cb.onToast('护士:治疗要 50 铜币'); }
1748	            else {
1749	              let left2 = 50;
1750	              for (let i = 0; i < this.player.inv.slots.length && left2 > 0; i++) {
1751	                const sl = this.player.inv.slots[i];
1752	                if (!sl || sl.id !== coinId2) continue;
1753	                const take = Math.min(sl.stack, left2);
1754	                sl.stack -= take; left2 -= take;
1755	                if (sl.stack <= 0) this.player.inv.slots[i] = null;
1756	              }
1757	              p.hp = p.maxHp;
1758	              this.cb.onInventoryChanged();
1759	              this.addDamageNumber(p.cx, p.y, p.maxHp - p.hp, false, '#40E080');
1760	              this.cb.onToast('护士:治疗完成(-50 铜币)');
1761	            }
1762	          }
1763	          npc.talkCooldown = 120;
1764	        }
1765	        return true;
1766	      }
1767	      if (npc.npcKey === 'merchant') {
1768	        if (npc.talkCooldown <= 0) {
1769	          this.merchantTrade();
1770	          npc.talkCooldown = 120;
1771	        }
1772	        return true;
1773	      }
1774	      npc.bubble = tips[Math.floor(Math.random() * tips.length)];
1775	      npc.bubbleT = 360;
1776	      npc.talkCooldown = 600;
1777	      return true;
1778	    }
1779	    return false;
1780	  }
1781	
1782	  /** 商人交易(简化商店):铜币买固定商品——火把10/木材20/铜镐/次级治疗药水 */
1783	  private merchantTrade(): void {
1784	    const inv = this.player.inv;
1785	    const coinId = ITEM_BY_KEY['coin_copper'];
1786	    let coins = 0;
1787	    for (const sl of inv.slots) if (sl && sl.id === coinId) coins += sl.stack;
1788	    const stock: Array<[string, number, number]> = [
1789	      ['torch', 10, 50], ['wood', 20, 20], ['copper_pickaxe', 1, 500], ['lesser_healing_potion', 3, 150],
1790	    ];
1791	    const affordable = stock.filter(([, , cost]) => cost <= coins);
1792	    if (affordable.length === 0) {
1793	      this.cb.onToast('商人:铜币不够呀(最便宜木材 20)');
1794	      return;
1795	    }
1796	    const [key, n, cost] = affordable[Math.floor(Math.random() * affordable.length)];
1797	    // 扣币
1798	    let left = cost;
1799	    for (let i = 0; i < inv.slots.length && left > 0; i++) {
1800	      const sl = inv.slots[i];
1801	      if (!sl || sl.id !== coinId) continue;
1802	      const take = Math.min(sl.stack, left);
1803	      sl.stack -= take; left -= take;
1804	      if (sl.stack <= 0) inv.slots[i] = null;
1805	    }
1806	    inv.add(ITEM_BY_KEY[key], n);
1807	    this.cb.onInventoryChanged();
1808	    this.cb.onToast(`商人:买到 ${n} × ${ITEM_DEFS[ITEM_BY_KEY[key]].name}(-${cost} 铜币)`);
1809	  }
1810	
1811	  private isValidHouse(doorX: number, doorY: number): boolean {
1812	    // 门占 3 格（doorY 为门顶），检查门内空间：有光源 + 有实心地板 + 有背景墙
1813	    // doorY+3 为地板行
1814	    const st = this.world.store;
1815	    let light = false, solidFloor = 0, walls = 0;
1816	    for (let dx = 1; dx <= 12; dx++) {
1817	      for (let dy = -6; dy <= 4; dy++) {
1818	        const x = doorX + dx, y = doorY + dy;
1819	        if (!st.inBounds(x, y)) continue;
1820	        if (st.get(x, y) === T.TORCH) light = true;
1821	        if (dy === 3 && st.isSolid(x, y)) solidFloor++;
1822	        if (dy >= -2 && dy <= 2 && st.wall[st.idx(x, y)] !== 0) walls++;
1823	      }
1824	    }
1825	    return light && solidFloor >= 6 && walls >= 20;
1826	  }
1827	
1828	  // ================= GameHooks 实现 =================
1829	
1830	  enemies() {
1831	    return this.entities.enemies;
1832	  }
1833	
1834	  spawnDrop(x: number, y: number, itemKey: string, count = 1, vx = 0, vy = -2) {
1835	    const id = ITEM_BY_KEY[itemKey];
1836	    if (id === undefined) return;
1837	    const drop = new ItemDrop(x - 6, y - 6, id, count, vx, vy);
1838	    this.entities.add(drop, 'drops');
1839	  }
1840	
1841	  damagePlayer(dmg: number, srcX: number, srcY: number, attacker?: Enemy) {
1842	    const p = this.player;
1843	    if (p.dead) return;
1844	    const ok = p.damage(dmg, srcX, srcY);
1845	    if (ok) {
1846	      // 致死一击：不播受击声，只播死亡声（保证最后听到的音效是死亡）
1847	      if (p.hp <= 0) this.sfx.play('pkilled');
1848	      else this.sfx.play('hurt');
1849	      // 实际扣血 = max(1, dmg - defense*0.5)（在 Player.damage 内）
1850	      const dealt = Math.max(1, dmg - p.defense * 0.5);
1851	      this.addDamageNumber(p.cx, p.y, Math.round(dealt), false, '#FF5050');
1852	      // 荆棘 Buff：受击反弹 2 伤害（移植自 Maples Player.Thorn）
1853	      if (p.thornsActive && attacker && !attacker.dead) {
1854	        attacker.hurt(2, Math.sign(attacker.cx - p.cx) || 1, -1.5, this);
1855	        this.addDamageNumber(attacker.cx, attacker.y, 2, false, '#80FF80');
1856	      }
1857	      if (p.hp <= 0) {
1858	        p.dead = true;
1859	        p.respawnTimer = 0;
1860	        // 死亡音由 Player 中央逻辑统一发声（覆盖所有死法），此处不重复
1861	        this.cb.onToast('你死了…');
1862	        // 掉一半铜币
1863	        const coins = p.inv.countOf(ITEM_BY_KEY['coin_copper']);
1864	        if (coins > 0) {
1865	          p.inv.remove(ITEM_BY_KEY['coin_copper'], Math.floor(coins / 2));
1866	        }
1867	      }
1868	    }
1869	  }
1870	
1871	  addDamageNumber(x: number, y: number, amount: number, crit: boolean, color = '#FFF') {
1872	    this.dmgNumbers.push({ x, y, vy: -1.6, value: amount, crit, color, life: 50 });
1873	  }
1874	
1875	  onEnemyKilled(key: string) {
1876	    if (key === 'eye_of_cthulhu') {
1877	      this.world.flags.downedEyeOfCthulhu = true;
1878	    }
1879	  }
1880	
1881	  /** 小动物生成：视野外地表，按昼夜 + 栖息生态筛选，权重抽取。
1882	   *  地面种：脚底精确贴地表格顶（此前高度>1格的实体被埋进地里卡死）；
1883	   *  飞行种：仅开阔天空（向上 30 格无实心）且地表无水（鸭子除外）；
1884	   *  蝴蝶：低空（地表上 1-4 格），优先附近有花的列 */
1885	  private spawnCritter() {
1886	    const st = this.world.store;
1887	    const isDay = this.world.clock.isDay;
1888	    const halfView = Math.ceil((this.camera.viewW / (this.camera.zoom || 1)) / 2 / TILE) + 8;
1889	    const side = Math.random() < 0.5 ? -1 : 1;
1890	    // 找列：蝴蝶优先附近 8 格内有 FLOWER 的列
1891	    let tx = Math.floor(this.player.cx / TILE) + side * (halfView + Math.floor(Math.random() * 18));
1892	    const isButterflyTentative = isDay && Math.random() < 0.35;
1893	    if (isButterflyTentative) {
1894	      for (let attempt = 0; attempt < 6; attempt++) {
1895	        const fx = tx + Math.floor((Math.random() - 0.5) * 16);
1896	        if (fx < 4 || fx >= st.w - 4) continue;
1897	        let found = false;
1898	        for (let dx = -4; dx <= 4 && !found; dx++) {
1899	          for (let y = Math.max(4, Math.floor(this.player.cy / TILE) - 24); y < Math.min(st.h - 4, Math.floor(this.player.cy / TILE) + 30); y++) {
1900	            if (st.type[st.idx(fx + dx, y)] === T.FLOWER) { found = true; break; }
1901	          }
1902	        }
1903	        if (found) { tx = fx; break; }
1904	      }
1905	    }
1906	    if (tx < 4 || tx >= st.w - 4) return;
1907	    // 找地表
1908	    const startY = Math.max(4, Math.floor(this.player.cy / TILE) - 24);
1909	    let groundY = -1;
1910	    for (let y = startY; y < Math.min(st.h - 4, startY + 70); y++) {
1911	      if (st.isSolid(tx, y)) { groundY = y; break; }
1912	    }
1913	    if (groundY < 0) return;
1914	    const surfaceWater = st.liquid[st.idx(tx, groundY - 1)] > 80;
1915	    // 生态判定
1916	    const gTile = st.type[st.idx(tx, groundY)];
1917	    let biome: 'forest' | 'snow' | 'sand' = 'forest';
1918	    if (gTile === T.SNOW) biome = 'snow';
1919	    else if (gTile === T.SAND || gTile === TILE_BY_KEY['sandstone'] || gTile === TILE_BY_KEY['hardened_sand']) biome = 'sand';
1920	    const nearWater = surfaceWater || (() => {
1921	      for (let dx = -2; dx <= 2; dx++) {
1922	        for (let dy = 0; dy <= 2; dy++) {
1923	          if (st.liquid[st.idx(tx + dx, groundY + dy)] > 80) return true;
1924	        }
1925	      }
1926	      return false;
1927	    })();
1928	    // 按昼夜 + 栖息生态过滤（水面列只出 water 生态或飞行种）
1929	    const pool = CRITTER_DEFS.filter((c) => {
1930	      if (c.dayOnly && !isDay) return false;
1931	      if (c.nightOnly && isDay) return false;
1932	      // 鸭子是两栖：水面列可生成（落在岸边浅水/滩涂），其余地面种不能在水列
1933	      if (surfaceWater && !c.water && c.kind !== 'fly' && c.key !== 'duck') return false;
1934	      if (!c.biomes.includes(biome) && !(nearWater && c.biomes.includes('water'))) return false;
1935	      return true;
1936	    });
1937	    if (!pool.length) return;
1938	    const total = pool.reduce((s2, c) => s2 + c.weight, 0);
1939	    let r = Math.random() * total;
1940	    let pick = pool[0];
1941	    for (const c of pool) { r -= c.weight; if (r <= 0) { pick = c; break; } }
1942	
1943	    if (pick.kind === 'fly') {
1944	      // 飞行种：地表不能是水（水面飞鸟/蝴蝶不合理，鸭子除外但鸭子不是 fly）
1945	      if (surfaceWater) return;
1946	      // 开阔天空检查（洞穴/地底不生成）
1947	      for (let k = 2; k <= 30; k++) {
1948	        if (groundY - k < 4) return;
1949	        if (st.isSolid(tx, groundY - k)) return;
1950	      }
1951	      // 蝴蝶低空（1-4 格）、鸟/萤火虫中高空
1952	      const lowFly = pick.key === 'butterfly' || pick.key === 'gold_butterfly';
1953	      const flyY = lowFly ? (groundY - 1 - Math.random() * 3) * TILE : (groundY - 8 - Math.random() * 12) * TILE;
1954	      this.entities.add(new Critter(pick.key, tx * TILE + 8, flyY), 'critters');
1955	    } else if (pick.water && surfaceWater) {
1956	      // 水生种（鸭子）：落在水面上（自上而下第一个液体格），不是湖底
1957	      let surfY = 4;
1958	      while (surfY < st.h - 4 && st.liquid[st.idx(tx, surfY)] <= 80) surfY++;
1959	      if (surfY >= st.h - 4) return;
1960	      this.entities.add(new Critter(pick.key, tx * TILE + 8, surfY * TILE), 'critters');
1961	    } else {
1962	      // 地面种：参数即脚底 y（构造器内减 h），精确站上地表格顶
1963	      const c = new Critter(pick.key, tx * TILE + 8, groundY * TILE);
1964	      // 安全兜底：身体中心在实心块内则放弃（防卡死）
1965	      const ci = st.idx(Math.floor(c.cx / TILE), Math.floor(c.cy / TILE));
1966	      if (st.type[ci] !== 0 && st.isSolid(Math.floor(c.cx / TILE), Math.floor(c.cy / TILE))) return;
1967	      this.entities.add(c, 'critters');
1968	    }
1969	  }
1970	
1971	  spawnEnemy(key: string, x: number, y: number) {
1972	    const e = new Enemy(key, x, y);
1973	    this.entities.add(e, 'enemies');
1974	    if (e.def.boss) this.boss = e;
1975	    return e;
1976	  }
1977	
1978	  /** 树苗生长成树 */
1979	  private growSaplings() {
1980	    const st = this.world.store;
1981	    const grown: Array<[number, number]> = [];
1982	    // 只扫玩家附近 60×40 区域
1983	    const ptx = Math.floor(this.player.cx / TILE), pty = Math.floor(this.player.cy / TILE);
1984	    for (let dy = -20; dy <= 20; dy++) {
1985	      for (let dx = -30; dx <= 30; dx++) {
1986	        const x = ptx + dx, y = pty + dy;
1987	        if (!st.inBounds(x, y) || st.get(x, y) !== T.SAPLING) continue;
1988	        // 上方 2-3 格净空才长
1989	        if (st.isActive(x, y - 1) || st.isActive(x, y - 2) || st.isActive(x, y - 3)) continue;
1990	        if (Math.random() < 0.5) { // 每次一半概率，模拟时间流逝
1991	          grown.push([x, y]);
1992	        }
1993	      }
1994	    }
1995	    for (const [x, y] of grown) {
1996	      const groundY = y + 1;
1997	      const th = 5 + Math.floor(Math.random() * 4);
1998	      st.setTile(x, y, 0);
1999	      for (let dy2 = 1; dy2 <= th; dy2++) {
2000	        if (!st.inBounds(x, groundY - dy2)) break;
2001	        if (st.isActive(x, groundY - dy2)) break;
2002	        st.setTile(x, groundY - dy2, T.TREE, dy2 === th ? 22 : 0, dy2 === th ? 198 : 0); // 原版帧：顶标记(22,198)+干身(0,0)
2003	      }
2004	      this.world.registerTree(x, groundY - th, th);
2005	      this.chunks.markDirtyArea(x - 4, groundY - th - 4, x + 4, groundY);
2006	    }
2007	  }
2008	
2009	  /** 拾取物品飘名（主角旁浅白文本）。同一时间只保留一个，
2010	   * 新拾取直接替换旧的 —— 不产生拖影，不会误读为多个物品 */
2011	  showPickupLabel(itemKey: string) {
2012	    const def = ITEM_DEFS[ITEM_BY_KEY[itemKey]];
2013	    if (!def) return;
2014	    this.dmgNumbers = this.dmgNumbers.filter((d) => !d.label);
2015	    this.dmgNumbers.push({
2016	      x: this.player.cx, y: this.player.y - 8, vy: -0.7,
2017	      value: 0, crit: false, color: '#F0F0F0', life: 55, label: def.name,
2018	    });
2019	  }
2020	
2021	  playSfx(name: string, vol?: number) {
2022	    this.sfx.play(name as SfxName, vol ?? 1);
2023	  }
2024	
2025	  playSfxFiles(files: string[], vol?: number) {
2026	    if (!this.sfx.playFiles(files, vol ?? 1)) this.sfx.play('hit', vol ?? 1);
2027	  }
2028	
2029	  /** 拾取物品后刷新 UI（带轻量节流 + 尾包补发，最多延迟 ~166ms） */
2030	  private invNotifyAt = -100;
2031	  private invNotifyPending = false;
2032	  /** 新物品入手飘名（主角旁浅白文本） */
2033	
2034	  notifyInventoryChanged() {
2035	    // 检测新物品：与上次快照比较，新增的种类在主角旁飘名
2036	    const inv = this.player.inv;
2037	    if (!this._invSnapshot) {
2038	      this._invSnapshot = new Map<number, number>();
2039	      for (const s2 of inv.slots) {
2040	        if (s2) this._invSnapshot.set(s2.id, (this._invSnapshot.get(s2.id) ?? 0) + s2.stack);
2041	      }
2042	      return;
2043	    }
2044	    const now = new Map<number, number>();
2045	    for (const s2 of inv.slots) {
2046	      if (s2) now.set(s2.id, (now.get(s2.id) ?? 0) + s2.stack);
2047	    }
2048	    for (const [id, n] of now) {
2049	      const before = this._invSnapshot.get(id) ?? 0;
2050	      if (n > before && this.tickCount - this.lastNotifiedAt > 30) {
2051	        this.lastNotifiedAt = this.tickCount;
2052	        const def = ITEM_DEFS[id];
2053	        if (def) {
2054	          this.dmgNumbers.push({
2055	            x: this.player.cx, y: this.player.y - 6, vy: -0.9,
2056	            value: 0, crit: false, color: '#FFFFFF', life: 60, label: def.name,
2057	          } as DamageNumber & { label: string });
2058	        }
2059	        break; // 每次 refresh 只飘一个
2060	      }
2061	    }
2062	    this._invSnapshot = now;
2063	    if (this.tickCount - this.invNotifyAt >= 10) {
2064	      this.invNotifyAt = this.tickCount;
2065	      this.invNotifyPending = false;
2066	      this.cb.onInventoryChanged();
2067	    } else {
2068	      this.invNotifyPending = true;
2069	    }
2070	  }
2071	  private _invSnapshot: Map<number, number> | null = null;
2072	  private lastNotifiedAt = 0;
2073	
2074	  private flushInvNotify() {
2075	    if (this.invNotifyPending && this.tickCount - this.invNotifyAt >= 10) {
2076	      this.invNotifyAt = this.tickCount;
2077	      this.invNotifyPending = false;
2078	      this.cb.onInventoryChanged();
2079	    }
2080	  }
2081	
2082	  /** 火把火星：视区内点燃的火把按概率在火点处飘出上浮火粒 */
2083	  private emitTorchSparks() {
2084	    if (this.tickCount % 3 !== 0) return; // 20Hz 足够，省扫描
2085	    const st = this.world.store;
2086	    const cam = this.camera;
2087	    const z = cam.zoom || 1;
2088	    const tx0 = Math.max(0, Math.floor((cam.x - cam.viewW / 2 / z) / TILE));
2089	    const tx1 = Math.min(this.world.w - 1, Math.ceil((cam.x + cam.viewW / 2 / z) / TILE));
2090	    const ty0 = Math.max(0, Math.floor((cam.y - cam.viewH / 2 / z) / TILE));
2091	    const ty1 = Math.min(this.world.h - 1, Math.ceil((cam.y + cam.viewH / 2 / z) / TILE));
2092	    for (let y = ty0; y <= ty1; y++) {
2093	      for (let x = tx0; x <= tx1; x++) {
2094	        const i = st.idx(x, y);
2095	        if (st.type[i] !== T.TORCH) continue;
2096	        if (Math.random() >= 0.14) continue;
2097	        // 帧为 0(地面) 时火点在格顶上方；墙面变体也近似取格顶
2098	        this.particles.push({
2099	          x: x * TILE + 5 + Math.random() * 6,
2100	          y: y * TILE - 2 + Math.random() * 4,
2101	          vx: (Math.random() - 0.5) * 0.25,
2102	          vy: -0.35 - Math.random() * 0.4,
2103	          life: 16 + Math.random() * 12, maxLife: 28,
2104	          color: Math.random() < 0.55 ? '#FFB642' : Math.random() < 0.5 ? '#FF8A2A' : '#FFD97A',
2105	          size: 1 + Math.random() * 1.2,
2106	          grav: -0.015,  // 微浮力：火星徐徐上飘
2107	          damp: 0.985,
2108	        });
2109	      }
2110	    }
2111	  }
2112	
2113	  spawnParticles(
2114	    x: number, y: number, color: string, count: number, speed = 2,
2115	    opts: { life?: number; damp?: number; grav?: number } = {},
2116	  ) {
2117	    const base = opts.life ?? 40;
2118	    for (let i = 0; i < count; i++) {
2119	      const a = Math.random() * Math.PI * 2;
2120	      const life = Math.round(base * (0.6 + Math.random() * 0.4));
2121	      this.particles.push({
2122	        x, y, vx: Math.cos(a) * speed * Math.random(), vy: Math.sin(a) * speed * Math.random() - 1,
2123	        life, maxLife: life, color, size: 2 + Math.random() * 2,
2124	        damp: opts.damp, grav: opts.grav,
2125	      });
2126	    }
2127	    if (this.particles.length > 600) this.particles.splice(0, this.particles.length - 600);
2128	  }
2129	
2130	  setZoom(z: number) {
2131	    if (!this.camera) return;
2132	    this.camera.setZoomTarget(z);
2133	  }
2134	
2135	  // ================= 合成 =================
2136	
2137	  itemId(key: string): number {
2138	    return ITEM_BY_KEY[key];
2139	  }
2140	
2141	  stationsNearby(): Set<string> {
2142	    const st = this.world.store;
2143	    const px = Math.floor(this.player.cx / TILE), py = Math.floor(this.player.cy / TILE);
2144	    const found = new Set<string>(['hand']);
2145	    for (let dx = -4; dx <= 4; dx++) {
2146	      for (let dy = -3; dy <= 3; dy++) {
2147	        const t = st.get(px + dx, py + dy);
2148	        if (t === T.WORKBENCH) found.add('workbench');
2149	        if (t === T.FURNACE) found.add('furnace');
2150	        if (t === T.ANVIL) found.add('anvil');
2151	      }
2152	    }
2153	    return found;
2154	  }
2155	
2156	  canCraft(r: (typeof RECIPES)[number]): boolean {
2157	    if (!this.stationsNearby().has(r.station)) return false;
2158	    return r.inputs.every(([key, n]) => this.player.inv.countOf(ITEM_BY_KEY[key]) >= n);
2159	  }
2160	
2161	  craft(r: (typeof RECIPES)[number]) {
2162	    if (!this.canCraft(r)) return;
2163	    for (const [key, n] of r.inputs) this.player.inv.remove(ITEM_BY_KEY[key], n);
2164	    this.player.inv.add(ITEM_BY_KEY[r.out], r.count);
2165	    this.cb.onInventoryChanged();
2166	  }
2167	
2168	  // ================= 召唤 Boss =================
2169	
2170	  /** 通用 Boss 召唤:vanilla 数据路径(NPC 13=世吞头带体节链 / 50=史莱姆王 / 266=克脑) */
2171	  summonBoss(key: string): void {
2172	    if (this.boss) { this.cb.onToast('已有 Boss 在场'); return; }
2173	    const side = Math.random() < 0.5 ? -1 : 1;
2174	    const tx = Math.floor((this.player.cx + side * 55 * TILE) / TILE);
2175	    let ty = 10;
2176	    for (; ty < this.world.h; ty++) {
2177	      if (this.world.store.type[this.world.store.idx(tx, ty)] !== 0) break;
2178	    }
2179	    const spawnY = Math.max(4, ty - 12) * TILE;
2180	    const vanillaId = key === 'eater_of_worlds_head' ? 13 : key === 'king_slime' ? 50 : key === 'brain_of_cthulhu' ? 266 : -1;
2181	    if (vanillaId >= 0 && Enemy.fromVanilla) {
2182	      const head = Enemy.fromVanilla(vanillaId, tx * TILE + 8, spawnY);
2183	      if (head) {
2184	        this.entities.add(head, 'enemies');
2185	        this.boss = head;
2186	        if (vanillaId === 13) {
2187	          // 世吞体节链(原版 15-30 段)
2188	          const segs = Enemy.spawnWormChain(head, 15 + Math.floor(Math.random() * 16));
2189	          for (const sg of segs) this.entities.add(sg, 'enemies');
2190	        }
2191	        this.sfx.playWav('roar');
2192	        this.cb.onToast('你感到有个邪恶的东西在看着你……');
2193	        return;
2194	      }
2195	    }
2196	    this.spawnEnemy(key, tx * TILE + 8, spawnY);
2197	    this.sfx.playWav('roar');
2198	    this.cb.onToast('你感到有个邪恶的东西在看着你……');
2199	  }
2200	
2201	  useSuspiciousEye() {
2202	    if (this.world.clock.isDay) {
2203	      this.cb.onToast('夜晚才能使用…');
2204	      return;
2205	    }
2206	    if (this.boss) return;
2207	    // 从远处地表生成（离玩家 ~55 格），Boss 会自己飞过来
2208	    const side = Math.random() < 0.5 ? -1 : 1;
2209	    const tx = Math.floor((this.player.cx + side * 55 * TILE) / TILE);
2210	    let ty = 10;
2211	    for (; ty < this.world.h; ty++) {
2212	      if (this.world.store.type[this.world.store.idx(tx, ty)] !== 0) break;
2213	    }
2214	    const spawnY = Math.max(4, ty - 12) * TILE;
2215	    const e = this.spawnEnemy('eye_of_cthulhu', tx * TILE + 8, spawnY);
2216	    void e;
2217	    this.sfx.playWav('roar');
2218	    this.cb.onToast('你感到有个邪恶的东西在看着你……');
2219	  }
2220	
2221	  /** 地图传送：在目标点附近找可容纳主角的空间（2 格高净空 + 站立地面）。
2222	   *  优先目标点自身，然后螺旋外扩到 24 格内就近安置 */
2223	  private teleportNear(tx: number, ty: number): boolean {
2224	    const st = this.world.store;
2225	    const p = this.player;
2226	    // 空中落点：2 格净空即可（无地面要求）
2227	    const fitsAir = (x: number, y: number) => {
2228	      for (let dy = 0; dy <= 1; dy++) {
2229	        if (!st.inBounds(x, y - dy) || st.isSolid(x, y - dy)) return false;
2230	      }
2231	      return true;
2232	    };
2233	    const fits = (x: number, y: number) => {
2234	      // (x, y-1..y) 两格净空（无实心/无液体），y+1 格实心站立
2235	      for (let dy = 0; dy <= 1; dy++) {
2236	        if (!st.inBounds(x, y - dy) || st.isSolid(x, y - dy)) return false;
2237	        if (st.liquid[st.idx(x, y - dy)] > 100) return false;
2238	      }
2239	      return st.inBounds(x, y + 1) && st.isSolid(x, y + 1);
2240	    };
2241	    if (fits(tx, ty)) {
2242	      p.x = tx * TILE + 1; p.y = (ty - 1) * TILE;
2243	    } else {
2244	      // 螺旋外扩找最近可站位置
2245	      let found = false;
2246	      for (let r = 1; r <= 24 && !found; r++) {
2247	        for (let dx = -r; dx <= r && !found; dx++) {
2248	          for (let dy = -r; dy <= r && !found; dy++) {
2249	            if (Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
2250	            if (fits(tx + dx, ty + dy)) {
2251	              p.x = (tx + dx) * TILE + 1;
2252	              p.y = (ty + dy - 1) * TILE;
2253	              found = true;
2254	            }
2255	          }
2256	        }
2257	      }
2258	      if (!found) {
2259	        // 高空/无地面：允许落在空中（目标列上下找 2 格净空，重力会带下来）
2260	        for (let dy = 0; dy <= 6; dy++) {
2261	          for (const sy of [ty - dy, ty + dy]) {
2262	            if (fitsAir(tx, sy)) {
2263	              p.x = tx * TILE + 1; p.y = (sy - 1) * TILE;
2264	              p.vx = 0; p.vy = 0;
2265	              this.camera.x = p.cx; this.camera.y = p.cy;
2266	              return true;
2267	            }
2268	          }
2269	        }
2270	        this.cb.onToast('传送失败：目标区域完全实心');
2271	        return false;
2272	      }
2273	    }
2274	    p.vx = 0; p.vy = 0;
2275	    this.camera.x = p.cx; this.camera.y = p.cy;
2276	    return true;
2277	  }
2278	
2279	  // ================= 重生 =================
2280	
2281	  /** 玩家死亡瞬间：红色粉碎粒子散落 + 脚下留一块墓碑 */
2282	  private _deathHandled = false;
2283	  private handlePlayerDeath() {
2284	    const p = this.player;
2285	    // 红色粉碎粒子：身体范围多层爆散，喷溅落地反弹/停驻后缓慢淡出（约 5 秒）
2286	    this.spawnParticles(p.cx, p.y + 8, '#C02020', 22, 3.2, { life: 300, damp: 0.988, grav: 0.09 });
2287	    this.spawnParticles(p.cx, p.cy, '#8A1010', 16, 2.4, { life: 280, damp: 0.985, grav: 0.09 });
2288	    this.spawnParticles(p.cx, p.cy - 6, '#E85050', 10, 2.8, { life: 260, damp: 0.988, grav: 0.09 });
2289	    // 墓碑：作为物理实体从死亡点掉落（空中死亡则从空中坠落，落地弹跳翻滚后安放）
2290	    this.entities.add(new Tombstone(p.cx, p.cy), 'props');
2291	  }
2292	
2293	
2294	  respawnPlayer() {
2295	    const p = this.player;
2296	    p.hp = p.maxHp;
2297	    p.dead = false;
2298	    p.iframes = 90;
2299	    p.respawnTimer = 0;
2300	    p.x = this.world.spawnX * TILE + 8;
2301	    p.y = (this.world.spawnY - 3) * TILE;
2302	    p.vx = 0; p.vy = 0;
2303	  }
2304	
2305	  // ================= 渲染 =================
2306	
2307	  render() {
2308	    const cam = this.camera;
2309	    const L = this.lighting;
2310	    this.renderer.annotateMarks = this.annotateMode ? this.marks : null;
2311	    const hover = this.input.uiBlocking ? null : (() => {
2312	      const [tx, ty] = cam.tileUnder(this.input.mouseX, this.input.mouseY);
2313	      return this.world.store.inBounds(tx, ty) ? { x: tx, y: ty } : null;
2314	    })();
2315	    this.renderer.render(
2316	      cam, this.world, this.world.clock, this.chunks,
2317	      L.r, L.g, L.b, L.rx, L.ry, L.rw, L.rh,
2318	      this.player,
2319	      this.entities.all(),
2320	      this.particles, this.dmgNumbers,
2321	      this.swing, hover,
2322	      this.boss ? { name: this.boss.def.name, hp: this.boss.hp, maxHp: this.boss.maxHp } : null,
2323	      this.input.mouseX, this.input.mouseY, this.input.mouseDown,
2324	      this.mining ? Math.min(1, this.mining.progress / this.hardnessCache) : 0,
2325	    );
2326	  }
2327	
2328	  /** 每逻辑帧后处理挥舞命中（在 fixedUpdate 实体更新后调用） */
2329	  postUpdate() {
2330	    this.updateSwingHits();
2331	  }
2332	}
2333	

```


---

## 🤖 Assistant · 2026-08-09T09:09:25.400Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read: items.ts (data structure), Inventory.ts, Player.ts, SaveFile.ts, KvStore.ts, recipes.ts, WorldGen.ts, World.ts, SpriteAtlas.ts (load paths), index.html, package.json. Let me batch.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:25.401Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/items.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:25.406Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/items/Inventory.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:25.418Z

**📎 ToolResult**

```
1	// 物品栏：0-39 背包（首行 0-9 快捷栏）+ 40-44 配饰 + 45-47 盔甲 + 48-50 时装 + 51-53 金钱（铜/银/金）
2	import { ITEM_DEFS, ITEM_BY_KEY, type ArmorSlot } from '../data/items';
3	
4	export const INV_COLS = 10;
5	export const INV_ROWS = 4;
6	export const ACCESSORY_SLOTS = 5;
7	export const ARMOR_SLOTS = 3;   // 头盔/胸甲/胫甲
8	export const VANITY_SLOTS = 3;  // 同部位时装
9	export const COIN_SLOTS = 3;    // 铜币/银币/金币
10	export const ACCESSORY_START = INV_COLS * INV_ROWS; // 40
11	export const ARMOR_START = ACCESSORY_START + ACCESSORY_SLOTS; // 45
12	export const VANITY_START = ARMOR_START + ARMOR_SLOTS; // 48
13	export const COIN_START = VANITY_START + VANITY_SLOTS; // 51
14	export const INV_SIZE = COIN_START + COIN_SLOTS; // 54
15	export const COIN_KEYS = ['coin_copper', 'coin_silver', 'coin_gold'] as const;
16	
17	export function isCoinSlot(i: number): boolean {
18	  return i >= COIN_START && i < INV_SIZE;
19	}
20	
21	/** 金钱格只收对应币种 */
22	export function coinSlotAccepts(i: number, id: number): boolean {
23	  if (!isCoinSlot(i)) return false;
24	  return id === ITEM_BY_KEY[COIN_KEYS[i - COIN_START]];
25	}
26	
27	/** 是否任一币种 */
28	export function coinIndexOf(id: number): number {
29	  return COIN_KEYS.findIndex((k) => ITEM_BY_KEY[k] === id);
30	}
31	
32	export function isAccessorySlot(i: number): boolean {
33	  return i >= ACCESSORY_START && i < ARMOR_START;
34	}
35	
36	export function isAccessoryItem(id: number): boolean {
37	  return !!ITEM_DEFS[id]?.accessory;
38	}
39	
40	/** 盔甲/时装格（45-50）。返回该格要求的部位，非盔甲格返回 null */
41	export function armorSlotReq(i: number): ArmorSlot | null {
42	  if (i >= ARMOR_START && i < VANITY_START) return (i - ARMOR_START) as ArmorSlot; // 0头1胸2腿
43	  if (i >= VANITY_START && i < INV_SIZE) return (i - VANITY_START) as ArmorSlot;
44	  return null;
45	}
46	
47	export function isArmorItem(id: number): boolean {
48	  return !!ITEM_DEFS[id]?.armor;
49	}
50	
51	export class Inventory {
52	  slots: Array<{ id: number; stack: number } | null>;
53	  selected = 0; // 快捷栏选中格
54	
55	  constructor() {
56	    this.slots = Array(INV_SIZE).fill(null);
57	  }
58	
59	  heldItem(): { id: number; stack: number } | null {
60	    return this.slots[this.selected];
61	  }
62	
63	  heldDef() {
64	    const it = this.heldItem();
65	    return it ? ITEM_DEFS[it.id] : null;
66	  }
67	
68	  /** 已装备的配饰列表（扫描配饰栏） */
69	  equippedAccessories(): number[] {
70	    const out: number[] = [];
71	    for (let i = ACCESSORY_START; i < ARMOR_START; i++) {
72	      const s = this.slots[i];
73	      if (s && ITEM_DEFS[s.id]?.accessory) out.push(s.id);
74	    }
75	    return out;
76	  }
77	
78	  /** 已穿戴的盔甲 id（45-47，时装不计防御） */
79	  equippedArmor(): Array<number | null> {
80	    return [0, 1, 2].map((k) => this.slots[ARMOR_START + k]?.id ?? null);
81	  }
82	
83	  /** 显示用部位贴图：时装格优先，为空回落装备格 */
84	  displayArmor(): Array<number | null> {
85	    return [0, 1, 2].map((k) => {
86	      const v = this.slots[VANITY_START + k];
87	      if (v) return v.id;
88	      return this.slots[ARMOR_START + k]?.id ?? null;
89	    });
90	  }
91	
92	  /** 添加物品（不进配饰/盔甲/时装栏；币种自动进金钱格），返回未能放入的数量（0 = 全部放入） */
93	  add(id: number, count: number): number {
94	    const max = ITEM_DEFS[id].maxStack;
95	    // 币种优先入金钱格（合并→空格）
96	    const ci = coinIndexOf(id);
97	    if (ci >= 0) {
98	      const slot = COIN_START + ci;
99	      const s = this.slots[slot];
100	      if (s) {
101	        const put = Math.min(max - s.stack, count);
102	        s.stack += put;
103	        count -= put;
104	      } else {
105	        const put = Math.min(max, count);
106	        this.slots[slot] = { id, stack: put };
107	        count -= put;
108	      }
109	      return count;
110	    }
111	    for (let i = 0; i < ACCESSORY_START && count > 0; i++) {
112	      const s = this.slots[i];
113	      if (s && s.id === id && s.stack < max) {
114	        const put = Math.min(max - s.stack, count);
115	        s.stack += put;
116	        count -= put;
117	      }
118	    }
119	    for (let i = 0; i < ACCESSORY_START && count > 0; i++) {
120	      if (!this.slots[i]) {
121	        const put = Math.min(max, count);
122	        this.slots[i] = { id, stack: put };
123	        count -= put;
124	      }
125	    }
126	    return count;
127	  }
128	
129	  removeAt(i: number, count = 1): boolean {
130	    const s = this.slots[i];
131	    if (!s || s.stack < count) return false;
132	    s.stack -= count;
133	    if (s.stack <= 0) this.slots[i] = null;
134	    return true;
135	  }
136	
137	  countOf(id: number): number {
138	    let n = 0;
139	    for (const s of this.slots) if (s && s.id === id) n += s.stack;
140	    return n;
141	  }
142	
143	  remove(id: number, count: number): boolean {
144	    if (this.countOf(id) < count) return false;
145	    for (let i = 0; i < this.slots.length && count > 0; i++) {
146	      const s = this.slots[i];
147	      if (s && s.id === id) {
148	        const take = Math.min(s.stack, count);
149	        s.stack -= take;
150	        count -= take;
151	        if (s.stack <= 0) this.slots[i] = null;
152	      }
153	    }
154	    return true;
155	  }
156	
157	  /** 某格能否接收物品（配饰位只收配饰；盔甲/时装位只收对应部位；金钱位只收对应币种） */
158	  canAccept(i: number, id: number): boolean {
159	    if (isAccessorySlot(i)) return isAccessoryItem(id);
160	    if (isCoinSlot(i)) return coinSlotAccepts(i, id);
161	    const req = armorSlotReq(i);
162	    if (req !== null) return ITEM_DEFS[id]?.armor?.slot === req;
163	    return true;
164	  }
165	
166	  /** 交换/合并格子（UI 拖拽）。带装备位校验。 */
167	  swap(i: number, j: number) {
168	    const a = this.slots[i], b = this.slots[j];
169	    if (a && !this.canAccept(j, a.id)) return; // 拒绝
170	    if (b && !this.canAccept(i, b.id)) return; // 反向也要合法（交换）
171	    if (a && b && a.id === b.id) {
172	      const max = ITEM_DEFS[a.id].maxStack;
173	      const put = Math.min(max - b.stack, a.stack);
174	      b.stack += put;
175	      a.stack -= put;
176	      if (a.stack <= 0) this.slots[i] = null;
177	    } else {
178	      this.slots[i] = b;
179	      this.slots[j] = a;
180	    }
181	  }
182	}
183	

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:25.574Z

**📎 ToolResult**

```
1	// 物品注册表
2	export type ToolType = 'pick' | 'axe' | 'sword' | 'hammer';
3	// Buff 类型（药水饮用后生效）
4	export type PotionBuff = 'agility' | 'ironskin' | 'resistance' | 'thorns' | 'regen';
5	// 盔甲部位：0 头盔 1 胸甲 2 胫甲（与 Inventory.armorSlotReq 的格位对应）
6	export type ArmorSlot = 0 | 1 | 2;
7	
8	export interface ItemDef {
9	  key: string;
10	  name: string;
11	  maxStack: number;
12	  tile?: string;          // 放置的 tile key
13	  placeStyle?: number;     // 放置的样式索引(vanilla style 帧 X 偏移 = style*fw*18)
14	  magic?: {               // 魔法武器:消耗 mana 发射投射物
15	    damage: number;
16	    speed: number;        // 使用冷却 tick
17	    manaCost: number;
18	    projSpeed: number;
19	    proj?: 'spark' | 'bolt'; // 投射物外观
20	  };
21	  ranged?: {              // 远程武器:消耗 ammo 弹药发射投射物
22	    damage: number;
23	    speed: number;        // 使用冷却 tick
24	    knockback: number;
25	    ammo: string;         // 弹药 item key(箭)
26	    projSpeed: number;    // 投射物速度 px/tick
27	  };
28	  wall?: string;          // 放置的 wall key
29	  tool?: {
30	    type: ToolType;
31	    power?: number;       // 工具力（镐/斧/锤）
32	    damage?: number;      // 武器伤害
33	    speed?: number;       // 使用间隔 tick
34	    knockback?: number;
35	    reach?: number;       // 攻击/作用半径（px）
36	  };
37	  heal?: number;          // 食用/饮用回复
38	  potion?: {
39	    buff: PotionBuff;
40	    duration: number;     // 秒
41	    isHealType: boolean;  // 受"耐药性"封锁
42	  };
43	  accessory?: 'lucky_horseshoe' | 'feral_claws'; // 配饰效果
44	  armor?: { slot: ArmorSlot; defense: number };   // 盔甲（可穿装备/时装格，仅装备格计防御）
45	  value?: number;         // 钱币价值（铜币）
46	  desc?: string;
47	}
48	
49	export const ITEM_DEFS: ItemDef[] = [];
50	const byKey: Record<string, number> = {};
51	export const ITEM_BY_KEY: Record<string, number> = byKey;
52	
53	function item(d: Partial<ItemDef> & { key: string; name: string }) {
54	  byKey[d.key] = ITEM_DEFS.length;
55	  ITEM_DEFS.push({ maxStack: 999, ...d } as ItemDef);
56	}
57	
58	// ---- 基础方块 ----
59	item({ key: 'dirt_block', name: '泥土块', tile: 'dirt' });
60	item({ key: 'stone_block', name: '石块', tile: 'stone' });
61	item({ key: 'wood', name: '木材', tile: 'wood' });
62	item({ key: 'sand_block', name: '沙块', tile: 'sand' });
63	item({ key: 'snow_block', name: '雪块', tile: 'snow' });
64	item({ key: 'platform', name: '木平台', tile: 'platform', maxStack: 999 });
65	item({ key: 'torch', name: '火把', tile: 'torch' });
66	item({ key: 'door', name: '木门', tile: 'door_closed', maxStack: 99 });
67	item({ key: 'workbench', name: '工作台', tile: 'workbench', maxStack: 99 });
68	item({ key: 'furnace', name: '熔炉', tile: 'furnace', maxStack: 99 });
69	item({ key: 'anvil', name: '铁砧', tile: 'anvil', maxStack: 99 });
70	item({ key: 'chest', name: '宝箱', tile: 'chest', maxStack: 99 });
71	
72	// ---- 材料 ----
73	item({ key: 'gel', name: '凝胶', desc: '史莱姆的残留物' });
74	item({ key: 'acorn', name: '橡实', desc: '种在草块上会长成树', maxStack: 99, tile: 'acorn_sapling' });
75	item({ key: 'mushroom_item', name: '蘑菇', heal: 15, value: 1 });
76	item({ key: 'copper_ore', name: '铜矿', desc: '可在熔炉炼成铜锭' });
77	item({ key: 'iron_ore', name: '铁矿' });
78	item({ key: 'silver_ore', name: '银矿' });
79	item({ key: 'gold_ore', name: '金矿' });
80	item({ key: 'copper_bar', name: '铜锭' });
81	item({ key: 'iron_bar', name: '铁锭' });
82	item({ key: 'silver_bar', name: '银锭' });
83	item({ key: 'gold_bar', name: '金锭' });
84	item({ key: 'lens', name: '晶状体', desc: '恶魔眼的眼睛' });
85	item({ key: 'suspicious_eye', name: '可疑的眼球', desc: '夜间使用会召唤不祥之物…', maxStack: 20 });
86	item({ key: 'lesser_healing_potion', name: '弱效治疗药水', heal: 50, maxStack: 30 });
87	item({ key: 'coin_copper', name: '铜币', maxStack: 999, value: 1 });
88	item({ key: 'coin_silver', name: '银币', maxStack: 999, value: 100 });
89	item({ key: 'coin_gold', name: '金币', maxStack: 999, value: 10000 });
90	
91	// ---- 药水（Buff 来源，数值移植自 Maples Potions/*.asset）----
92	item({ key: 'heal_potion', name: '治疗药水', maxStack: 30, heal: 100, desc: '回复 100 生命',
93	  potion: { buff: 'resistance', duration: 60, isHealType: true } });
94	item({ key: 'agility_potion', name: '敏捷药水', maxStack: 30, desc: '移速 +25%，持续 4 分钟',
95	  potion: { buff: 'agility', duration: 240, isHealType: false } });
96	item({ key: 'ironskin_potion', name: '铁皮药水', maxStack: 30, desc: '防御 +6，持续 5 分钟',
97	  potion: { buff: 'ironskin', duration: 300, isHealType: false } });
98	item({ key: 'thorns_potion', name: '荆棘药水', maxStack: 30, desc: '受击反弹 2 伤害，持续 2 分钟',
99	  potion: { buff: 'thorns', duration: 120, isHealType: false } });
100	item({ key: 'regen_potion', name: '恢复药水', maxStack: 30, desc: '每 5 秒回复 10 生命，持续 2 分钟',
101	  potion: { buff: 'regen', duration: 120, isHealType: true } });
102	
103	// ---- 配饰（移植自 Maples Accessory）----
104	item({ key: 'lucky_horseshoe', name: '幸运马掌', maxStack: 1, accessory: 'lucky_horseshoe',
105	  desc: '免疫摔落伤害' });
106	item({ key: 'feral_claws', name: '猛爪手套', maxStack: 1, accessory: 'feral_claws',
107	  desc: '近战攻速 ×2，伤害 +5' });
108	
109	// ---- 盔甲（铜/铁/银/金三件套，防御取原版）----
110	const armorTiers: Array<[string, string, [number, number, number]]> = [
111	  // key 前缀, 显示前缀, [头盔, 胸甲, 胫甲] 防御
112	  ['copper', '铜', [1, 2, 1]],
113	  ['iron', '铁', [2, 3, 2]],
114	  ['silver', '银', [3, 4, 3]],
115	  ['gold', '金', [4, 5, 4]],
116	];
117	const armorParts: Array<[string, string, ArmorSlot]> = [
118	  ['helmet', '头盔', 0], ['chainmail', '胸甲', 1], ['greaves', '胫甲', 2],
119	];
120	for (const [prefix, cn, defs] of armorTiers) {
121	  armorParts.forEach(([suffix, cnPart, slot], k) => {
122	    item({
123	      key: `${prefix}_${suffix}`, name: `${cn}${cnPart}`, maxStack: 1,
124	      armor: { slot, defense: defs[k] },
125	      desc: `防御 +${defs[k]}`,
126	    });
127	  });
128	}
129	
130	// ---- 工具/武器（数值 = 官方原版 1.4.0.5 Item.cs SetDefaults，铜币价值）----
131	// 木镐/木斧为自定义低档（原版无对应）；木剑(24)=官方 7 伤、木锤(196)=官方 25 锤力
132	item({ key: 'wood_pickaxe', name: '木镐', maxStack: 1, value: 50,
133	  tool: { type: 'pick', power: 12, damage: 2, speed: 23, knockback: 2, reach: 2.6 * 16 } });
134	item({ key: 'wood_axe', name: '木斧', maxStack: 1, value: 50,
135	  tool: { type: 'axe', power: 4, damage: 2, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
136	item({ key: 'wood_sword', name: '木剑', maxStack: 1, value: 100,
137	  tool: { type: 'sword', damage: 7, speed: 25, knockback: 4, reach: 2.2 * 16 } });
138	item({ key: 'wood_hammer', name: '木锤', maxStack: 1, value: 50,
139	  tool: { type: 'hammer', power: 25, damage: 2, speed: 37, knockback: 5.5, reach: 2.4 * 16 },
140	  desc: '敲除背景墙' });
141	// 铜（3509/3506/3508/3505）
142	item({ key: 'copper_pickaxe', name: '铜镐', maxStack: 1, value: 500,
143	  tool: { type: 'pick', power: 35, damage: 4, speed: 23, knockback: 2, reach: 2.6 * 16 } });
144	item({ key: 'copper_axe', name: '铜斧', maxStack: 1, value: 400,
145	  tool: { type: 'axe', power: 7, damage: 3, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
146	item({ key: 'copper_sword', name: '铜剑', maxStack: 1, value: 450,
147	  tool: { type: 'sword', damage: 8, speed: 23, knockback: 5, reach: 2.2 * 16 } });
148	item({ key: 'copper_hammer', name: '铜锤', maxStack: 1, value: 400,
149	  tool: { type: 'hammer', power: 35, damage: 4, speed: 33, knockback: 5.5, reach: 2.4 * 16 },
150	  desc: '敲除背景墙' });
151	// 铁（1/10/4/7）
152	item({ key: 'iron_pickaxe', name: '铁镐', maxStack: 1, value: 2000,
153	  tool: { type: 'pick', power: 40, damage: 5, speed: 20, knockback: 2, reach: 2.6 * 16 } });
154	item({ key: 'iron_axe', name: '铁斧', maxStack: 1, value: 1600,
155	  tool: { type: 'axe', power: 9, damage: 5, speed: 27, knockback: 4.5, reach: 2.4 * 16 } });
156	item({ key: 'iron_sword', name: '铁剑', maxStack: 1, value: 1800,
157	  tool: { type: 'sword', damage: 10, speed: 21, knockback: 5, reach: 2.2 * 16 } });
158	item({ key: 'iron_hammer', name: '铁锤', maxStack: 1, value: 1600,
159	  tool: { type: 'hammer', power: 40, damage: 7, speed: 30, knockback: 5.5, reach: 2.4 * 16 },
160	  desc: '敲除背景墙' });
161	// 银（3515/3512/3514/3511）
162	item({ key: 'silver_pickaxe', name: '银镐', maxStack: 1, value: 5000,
163	  tool: { type: 'pick', power: 45, damage: 6, speed: 19, knockback: 2, reach: 2.6 * 16 } });
164	item({ key: 'silver_axe', name: '银斧', maxStack: 1, value: 4000,
165	  tool: { type: 'axe', power: 10, damage: 6, speed: 26, knockback: 4.5, reach: 2.4 * 16 } });
166	item({ key: 'silver_sword', name: '银剑', maxStack: 1, value: 4500,
167	  tool: { type: 'sword', damage: 11, speed: 21, knockback: 5, reach: 2.2 * 16 } });
168	item({ key: 'silver_hammer', name: '银锤', maxStack: 1, value: 4000,
169	  tool: { type: 'hammer', power: 45, damage: 9, speed: 29, knockback: 5.5, reach: 2.4 * 16 },
170	  desc: '敲除背景墙' });
171	// 金（3521/3518/3520/3517）
172	item({ key: 'gold_pickaxe', name: '金镐', maxStack: 1, value: 10000,
173	  tool: { type: 'pick', power: 55, damage: 6, speed: 20, knockback: 2, reach: 2.6 * 16 } });
174	item({ key: 'gold_axe', name: '金斧', maxStack: 1, value: 8000,
175	  tool: { type: 'axe', power: 11, damage: 7, speed: 26, knockback: 4.5, reach: 2.4 * 16 } });
176	item({ key: 'gold_sword', name: '金剑', maxStack: 1, value: 9000,
177	  tool: { type: 'sword', damage: 13, speed: 20, knockback: 5, reach: 2.2 * 16 } });
178	item({ key: 'gold_hammer', name: '金锤', maxStack: 1, value: 8000,
179	  tool: { type: 'hammer', power: 55, damage: 9, speed: 28, knockback: 5.5, reach: 2.4 * 16 },
180	  desc: '敲除背景墙' });
181	
182	// ===================== 原版素材批次：新材料 / 方块 / 家具 =====================
183	// ---- 替代矿与困难模式矿（先做美术/掉落） ----
184	item({ key: 'tin_ore', name: '锡矿' });
185	item({ key: 'lead_ore', name: '铅矿' });
186	item({ key: 'tungsten_ore', name: '钨矿' });
187	item({ key: 'platinum_ore', name: '铂金矿' });
188	item({ key: 'tin_bar', name: '锡锭' });
189	item({ key: 'lead_bar', name: '铅锭' });
190	item({ key: 'tungsten_bar', name: '钨锭' });
191	item({ key: 'platinum_bar', name: '铂金锭' });
192	item({ key: 'demonite_ore', name: '魔矿' });
193	item({ key: 'meteorite', name: '陨石' });
194	item({ key: 'hellstone', name: '狱石' });
195	item({ key: 'crimtane_ore', name: '猩红矿' });
196	item({ key: 'cobalt_ore', name: '钴矿' });
197	item({ key: 'mythril_ore', name: '秘银矿' });
198	item({ key: 'adamantite_ore', name: '精金矿' });
199	item({ key: 'palladium_ore', name: '钯金矿' });
200	item({ key: 'orichalcum_ore', name: '山铜矿' });
201	item({ key: 'titanium_ore', name: '钛矿' });
202	item({ key: 'chlorophyte_ore', name: '叶绿矿' });
203	
204	// ---- 宝石 ----
205	item({ key: 'sapphire', name: '蓝宝石', value: 15 });
206	item({ key: 'ruby', name: '红宝石', value: 22 });
207	item({ key: 'emerald', name: '翡翠', value: 15 });
208	item({ key: 'topaz', name: '黄玉', value: 11 });
209	item({ key: 'amethyst', name: '紫水晶', value: 11 });
210	item({ key: 'diamond', name: '钻石', value: 30 });
211	
212	// ---- 冰雪 / 沙漠 / 基础方块 ----
213	item({ key: 'ice_block', name: '冰块', tile: 'ice' });
214	item({ key: 'ice_brick', name: '冰砖', tile: 'ice_brick' });
215	item({ key: 'snow_brick', name: '雪砖', tile: 'snow_brick' });
216	item({ key: 'sandstone_block', name: '沙岩', tile: 'sandstone' });
217	item({ key: 'hardened_sand_block', name: '硬化沙块', tile: 'hardened_sand' });
218	item({ key: 'desert_fossil', name: '沙漠化石' });
219	item({ key: 'clay_block', name: '粘土块', tile: 'clay' });
220	item({ key: 'glass', name: '玻璃', tile: 'glass' });
221	item({ key: 'obsidian', name: '黑曜石', tile: 'obsidian' });
222	item({ key: 'gray_brick', name: '灰砖', tile: 'gray_brick' });
223	item({ key: 'red_brick', name: '红砖', tile: 'red_brick' });
224	item({ key: 'mud_block', name: '泥块', tile: 'mud' });
225	item({ key: 'silt_block', name: '淤泥块', tile: 'silt' });
226	
227	// ---- 家具 ----
228	item({ key: 'table', name: '木桌', tile: 'table', maxStack: 99 });
229	item({ key: 'chair', name: '木椅', tile: 'chair', maxStack: 99 });
230	item({ key: 'bed', name: '床', tile: 'bed', maxStack: 99 });
231	item({ key: 'bookcase', name: '书架', tile: 'bookcase', maxStack: 99 });
232	item({ key: 'grandfather_clock', name: '落地钟', tile: 'grandfather_clock', maxStack: 99 });
233	item({ key: 'piano', name: '钢琴', tile: 'piano', maxStack: 99 });
234	item({ key: 'dresser', name: '梳妆台', tile: 'dresser', maxStack: 99 });
235	item({ key: 'bench', name: '长凳', tile: 'bench', maxStack: 99 });
236	item({ key: 'bathtub', name: '浴缸', tile: 'bathtub', maxStack: 99 });
237	item({ key: 'keg', name: '酒桶', tile: 'keg', maxStack: 99 });
238	item({ key: 'cooking_pot', name: '汤锅', tile: 'cooking_pot', maxStack: 99 });
239	item({ key: 'clay_pot', name: '陶盆', tile: 'clay_pot', maxStack: 99 });
240	item({ key: 'tombstone', name: '墓碑', tile: 'tombstone_v', maxStack: 99 });
241	item({ key: 'life_crystal', name: '水晶之心', maxStack: 99, desc: '古老的生命结晶' });
242	item({ key: 'candle', name: '蜡烛', tile: 'candle', maxStack: 99 });
243	item({ key: 'chandelier', name: '吊灯', tile: 'chandelier', maxStack: 99 });
244	item({ key: 'lantern', name: '吊挂灯笼', tile: 'lantern', maxStack: 99 });
245	item({ key: 'candelabra', name: '烛台', tile: 'candelabra', maxStack: 99 });
246	item({ key: 'chinese_lantern', name: '中式灯笼', tile: 'chinese_lantern', maxStack: 99 });
247	item({ key: 'skull_lantern', name: '骷髅灯笼', tile: 'skull_lantern', maxStack: 99 });
248	item({ key: 'water_candle', name: '水蜡烛', tile: 'water_candle', maxStack: 99 });
249	// 瓦罐战利品
250	item({ key: 'bomb', name: '小型炸弹', maxStack: 99, desc: '用力扔出去会爆炸…（待实装）', value: 5 });
251	item({ key: 'rope', name: '攀爬绳', maxStack: 999, desc: '左键放置绳列,触碰可攀爬', value: 1, tile: 'v_213_rope' });
252	
253	export interface ItemStack { id: number; stack: number; }
254	export function mkStack(key: string, stack = 1): ItemStack | null {
255	  const id = byKey[key];
256	  if (id === undefined) return null;
257	  return { id, stack };
258	}
259	
260	// ===================== wld 导入补全物品（compat-report 驱动） =====================
261	// 这些物品目前只做图标与存档保留（占位），后续按需实装功能
262	item({ key: 'vi_2350_recall_potion', name: 'Recall Potion', maxStack: 999, value: 1 });
263	item({ key: 'vi_188_healing_potion', name: 'Healing Potion', maxStack: 999, value: 1 });
264	item({ key: 'vi_282_glowstick', name: 'Glowstick', maxStack: 999, value: 1 });
265	item({ key: 'vi_41_flaming_arrow', name: 'Flaming Arrow', maxStack: 999, value: 1 });
266	item({ key: 'vi_167_dynamite', name: 'Dynamite', maxStack: 999, value: 1 });
267	item({ key: 'vi_279_throwing_knife', name: 'Throwing Knife', maxStack: 999, value: 1 });
268	item({ key: 'vi_51_jester_s_arrow', name: 'Jester\'s Arrow', maxStack: 999, value: 1 });
269	item({ key: 'vi_19_gold_bar', name: 'Gold Bar', maxStack: 999, value: 1 });
270	item({ key: 'vi_302_water_walking_potion', name: 'Water Walking Potion', maxStack: 999, value: 1 });
271	item({ key: 'vi_305_gravitation_potion', name: 'Gravitation Potion', maxStack: 999, value: 1 });
272	item({ key: 'vi_43_suspicious_looking_eye', name: 'Suspicious Looking Eye', maxStack: 999, value: 1 });
273	item({ key: 'vi_296_spelunker_potion', name: 'Spelunker Potion', maxStack: 999, value: 1 });
274	item({ key: 'vi_299_night_owl_potion', name: 'Night Owl Potion', maxStack: 999, value: 1 });
275	item({ key: 'vi_965_rope', name: 'Rope', maxStack: 999, value: 1 });
276	item({ key: 'vi_303_archery_potion', name: 'Archery Potion', maxStack: 999, value: 1 });
277	item({ key: 'vi_304_hunter_potion', name: 'Hunter Potion', maxStack: 999, value: 1 });
278	item({ key: 'vi_50_magic_mirror', name: 'Magic Mirror', maxStack: 999, value: 1 });
279	item({ key: 'vi_42_shuriken', name: 'Shuriken', maxStack: 999, value: 1 });
280	item({ key: 'vi_295_featherfall_potion', name: 'Featherfall Potion', maxStack: 999, value: 1 });
281	item({ key: 'vi_53_cloud_in_a_bottle', name: 'Cloud in a Bottle', maxStack: 999, value: 1 });
282	item({ key: 'vi_2329_dangersense_potion', name: 'Dangersense Potion', maxStack: 999, value: 1 });
283	item({ key: 'vi_40_wooden_arrow', name: 'Wooden Arrow', maxStack: 999, value: 1 });
284	item({ key: 'vi_975_shoe_spikes', name: 'Shoe Spikes', maxStack: 999, value: 1 });
285	item({ key: 'vi_54_hermes_boots', name: 'Hermes Boots', maxStack: 999, value: 1 });
286	item({ key: 'vi_301_thorns_potion', name: 'Thorns Potion', maxStack: 999, value: 1 });
287	item({ key: 'vi_49_band_of_regeneration', name: 'Band of Regeneration', maxStack: 999, value: 1 });
288	item({ key: 'vi_2326_titan_potion', name: 'Titan Potion', maxStack: 999, value: 1 });
289	item({ key: 'vi_297_invisibility_potion', name: 'Invisibility Potion', maxStack: 999, value: 1 });
290	item({ key: 'vi_166_bomb', name: 'Bomb', maxStack: 999, value: 1 });
291	item({ key: 'vi_5011_mace', name: 'Mace', maxStack: 999, value: 1 });
292	item({ key: 'vi_4425_shark_bait', name: 'Shark Bait', maxStack: 999, value: 1 });
293	item({ key: 'vi_2351_teleportation_potion', name: 'Teleportation Potion', maxStack: 999, value: 1 });
294	item({ key: 'vi_4460_sandcastle_bucket', name: 'Sandcastle Bucket', maxStack: 999, value: 1 });
295	item({ key: 'vi_168_grenade', name: 'Grenade', maxStack: 999, value: 1 });
296	item({ key: 'vi_227_restoration_potion', name: 'Restoration Potion', maxStack: 999, value: 1 });
297	item({ key: 'vi_930_flare_gun', name: 'Flare Gun', maxStack: 999, value: 1 });
298	item({ key: 'vi_931_flare', name: 'Flare', maxStack: 999, value: 1 });
299	item({ key: 'vi_997_extractinator', name: 'Extractinator', maxStack: 999, value: 1 });
300	item({ key: 'vi_52_angel_statue', name: 'Angel Statue', maxStack: 999, value: 1 });
301	item({ key: 'vi_265_hellfire_arrow', name: 'Hellfire Arrow', maxStack: 999, value: 1 });
302	item({ key: 'vi_298_shine_potion', name: 'Shine Potion', maxStack: 999, value: 1 });
303	item({ key: 'vi_5007_dead_man_s_sweater', name: 'Dead Man\'s Sweater', maxStack: 999, value: 1 });
304	item({ key: 'vi_117_meteorite_bar', name: 'Meteorite Bar', maxStack: 999, value: 1 });
305	item({ key: 'vi_186_breathing_reed', name: 'Breathing Reed', maxStack: 999, value: 1 });
306	item({ key: 'vi_329_shadow_key', name: 'Shadow Key', maxStack: 999, value: 1 });
307	item({ key: 'vi_974_ice_torch', name: 'Ice Torch', maxStack: 999, value: 1 });
308	item({ key: 'vi_2322_mining_potion', name: 'Mining Potion', maxStack: 999, value: 1 });
309	item({ key: 'vi_4915_tungsten_bullet', name: 'Tungsten Bullet', maxStack: 999, value: 1 });
310	item({ key: 'vi_946_umbrella', name: 'Umbrella', maxStack: 999, value: 1 });
311	item({ key: 'vi_939_web_slinger', name: 'Web Slinger', maxStack: 999, value: 1 });
312	item({ key: 'vi_4870_potion_of_return', name: 'Potion of Return', maxStack: 999, value: 1 });
313	item({ key: 'vi_288_obsidian_skin_potion', name: 'Obsidian Skin Potion', maxStack: 999, value: 1 });
314	item({ key: 'vi_31_bottle', name: 'Bottle', maxStack: 999, value: 1 });
315	item({ key: 'vi_211_feral_claws', name: 'Feral Claws', maxStack: 999, value: 1 });
316	item({ key: 'vi_4404_inner_tube', name: 'Inner Tube', maxStack: 999, value: 1 });
317	item({ key: 'vi_187_flipper', name: 'Flipper', maxStack: 999, value: 1 });
318	item({ key: 'vi_2198_ice_machine', name: 'Ice Machine', maxStack: 999, value: 1 });
319	item({ key: 'vi_274_dark_lance', name: 'Dark Lance', maxStack: 999, value: 1 });
320	item({ key: 'vi_285_aglet', name: 'Aglet', maxStack: 999, value: 1 });
321	item({ key: 'vi_213_staff_of_regrowth', name: 'Staff of Regrowth', maxStack: 999, value: 1 });
322	item({ key: 'vi_964_boomstick', name: 'Boomstick', maxStack: 999, value: 1 });
323	item({ key: 'vi_1293_lihzahrd_power_cell', name: 'Lihzahrd Power Cell', maxStack: 999, value: 1 });
324	item({ key: 'vi_2195_lihzahrd_furnace', name: 'Lihzahrd Furnace', maxStack: 999, value: 1 });
325	item({ key: 'vi_2766_solar_tablet_fragment', name: 'Solar Tablet Fragment', maxStack: 999, value: 1 });
326	item({ key: 'vi_300_battle_potion', name: 'Battle Potion', maxStack: 999, value: 1 });
327	item({ key: 'vi_2348_inferno_potion', name: 'Inferno Potion', maxStack: 999, value: 1 });
328	item({ key: 'vi_218_flamelash', name: 'Flamelash', maxStack: 999, value: 1 });
329	item({ key: 'vi_3019_hellwing_bow', name: 'Hellwing Bow', maxStack: 999, value: 1 });
330	item({ key: 'vi_112_flower_of_fire', name: 'Flower of Fire', maxStack: 999, value: 1 });
331	item({ key: 'vi_220_sunfury', name: 'Sunfury', maxStack: 999, value: 1 });
332	item({ key: 'vi_4345_can_of_worms', name: 'Can Of Worms', maxStack: 999, value: 1 });
333	item({ key: 'vi_953_climbing_claws', name: 'Climbing Claws', maxStack: 999, value: 1 });
334	item({ key: 'vi_3069_wand_of_sparking', name: 'Wand of Sparking', maxStack: 999, value: 1 });
335	item({ key: 'vi_212_anklet_of_the_wind', name: 'Anklet of the Wind', maxStack: 999, value: 1 });
336	item({ key: 'vi_2204_honey_dispenser', name: 'Honey Dispenser', maxStack: 999, value: 1 });
337	item({ key: 'vi_277_trident', name: 'Trident', maxStack: 999, value: 1 });
338	item({ key: 'vi_863_water_walking_boots', name: 'Water Walking Boots', maxStack: 999, value: 1 });
339	item({ key: 'vi_751_cloud', name: 'Cloud', maxStack: 999, value: 1 });
340	item({ key: 'vi_155_muramasa', name: 'Muramasa', maxStack: 999, value: 1 });
341	item({ key: 'vi_289_regeneration_potion', name: 'Regeneration Potion', maxStack: 999, value: 1 });
342	item({ key: 'vi_906_lava_charm', name: 'Lava Charm', maxStack: 999, value: 1 });
343	item({ key: 'vi_4055_dunerider_boots', name: 'Dunerider Boots', maxStack: 999, value: 1 });
344	item({ key: 'vi_724_ice_blade', name: 'Ice Blade', maxStack: 999, value: 1 });
345	item({ key: 'vi_670_ice_boomerang', name: 'Ice Boomerang', maxStack: 999, value: 1 });
346	item({ key: 'vi_4061_storm_spear', name: 'Storm Spear', maxStack: 999, value: 1 });
347	item({ key: 'vi_987_blizzard_in_a_bottle', name: 'Blizzard in a Bottle', maxStack: 999, value: 1 });
348	item({ key: 'vi_4551_slice_of_hell_cake', name: 'Slice of Hell Cake', maxStack: 999, value: 1 });
349	item({ key: 'vi_5010_treasure_magnet', name: 'Treasure Magnet', maxStack: 999, value: 1 });
350	item({ key: 'vi_2323_heartreach_potion', name: 'Heartreach Potion', maxStack: 999, value: 1 });
351	item({ key: 'vi_2345_lifeforce_potion', name: 'Lifeforce Potion', maxStack: 999, value: 1 });
352	item({ key: 'vi_290_swiftness_potion', name: 'Swiftness Potion', maxStack: 999, value: 1 });
353	item({ key: 'vi_291_gills_potion', name: 'Gills Potion', maxStack: 999, value: 1 });
354	item({ key: 'vi_280_spear', name: 'Spear', maxStack: 999, value: 1 });
355	item({ key: 'vi_2325_builder_potion', name: 'Builder Potion', maxStack: 999, value: 1 });
356	item({ key: 'vi_284_wooden_boomerang', name: 'Wooden Boomerang', maxStack: 999, value: 1 });
357	item({ key: 'vi_2192_bone_welder', name: 'Bone Welder', maxStack: 999, value: 1 });
358	item({ key: 'vi_5234_remnants_of_devotion', name: 'Remnants of Devotion', maxStack: 999, value: 1 });
359	item({ key: 'vi_156_cobalt_shield', name: 'Cobalt Shield', maxStack: 999, value: 1 });
360	item({ key: 'vi_157_aqua_scepter', name: 'Aqua Scepter', maxStack: 999, value: 1 });
361	item({ key: 'vi_163_blue_moon', name: 'Blue Moon', maxStack: 999, value: 1 });
362	item({ key: 'vi_113_magic_missile', name: 'Magic Missile', maxStack: 999, value: 1 });
363	item({ key: 'vi_3317_valor', name: 'Valor', maxStack: 999, value: 1 });
364	item({ key: 'vi_327_golden_key', name: 'Golden Key', maxStack: 999, value: 1 });
365	item({ key: 'vi_164_handgun', name: 'Handgun', maxStack: 999, value: 1 });
366	item({ key: 'vi_294_magic_power_potion', name: 'Magic Power Potion', maxStack: 999, value: 1 });
367	item({ key: 'vi_4263_magic_conch', name: 'Magic Conch', maxStack: 999, value: 1 });
368	item({ key: 'vi_4062_thunder_zapper', name: 'Thunder Zapper', maxStack: 999, value: 1 });
369	item({ key: 'vi_1579_flurry_boots', name: 'Flurry Boots', maxStack: 999, value: 1 });
370	item({ key: 'vi_4056_ancient_chisel', name: 'Ancient Chisel', maxStack: 999, value: 1 });
371	item({ key: 'vi_4346_encumbering_stone', name: 'Encumbering Stone', maxStack: 999, value: 1 });
372	item({ key: 'vi_1319_snowball_cannon', name: 'Snowball Cannon', maxStack: 999, value: 1 });
373	item({ key: 'vi_3199_ice_mirror', name: 'Ice Mirror', maxStack: 999, value: 1 });
374	item({ key: 'vi_950_ice_skates', name: 'Ice Skates', maxStack: 999, value: 1 });
375	item({ key: 'vi_4443_demonic_hellcart', name: 'Demonic Hellcart', maxStack: 999, value: 1 });
376	item({ key: 'vi_4737_ornate_shadow_key', name: 'Ornate Shadow Key', maxStack: 999, value: 1 });
377	item({ key: 'vi_4276_bast_statue', name: 'Bast Statue', maxStack: 999, value: 1 });
378	item({ key: 'vi_4262_snake_charmer_s_flute', name: 'Snake Charmer\'s Flute', maxStack: 999, value: 1 });
379	item({ key: 'vi_3093_herb_bag', name: 'Herb Bag', maxStack: 999, value: 1 });
380	item({ key: 'vi_292_ironskin_potion', name: 'Ironskin Potion', maxStack: 999, value: 1 });
381	item({ key: 'vi_3084_radar', name: 'Radar', maxStack: 999, value: 1 });
382	item({ key: 'vi_4341_step_stool', name: 'Step Stool', maxStack: 999, value: 1 });
383	item({ key: 'vi_4978_fledgling_wings', name: 'Fledgling Wings', maxStack: 999, value: 1 });
384	item({ key: 'vi_2197_sky_mill', name: 'Sky Mill', maxStack: 999, value: 1 });
385	item({ key: 'vi_158_lucky_horseshoe', name: 'Lucky Horseshoe', maxStack: 999, value: 1 });
386	item({ key: 'vi_5254_blessing_from_the_heavens', name: 'Blessing from the Heavens', maxStack: 999, value: 1 });
387	item({ key: 'vi_1156_piranha_gun', name: 'Piranha Gun', maxStack: 999, value: 1 });
388	item({ key: 'vi_1571_scourge_of_the_corruptor', name: 'Scourge of the Corruptor', maxStack: 999, value: 1 });
389	item({ key: 'vi_1260_rainbow_gun', name: 'Rainbow Gun', maxStack: 999, value: 1 });
390	item({ key: 'vi_1572_staff_of_the_frost_hydra', name: 'Staff of the Frost Hydra', maxStack: 999, value: 1 });
391	item({ key: 'vi_4607_desert_tiger_staff', name: 'Desert Tiger Staff', maxStack: 999, value: 1 });
392	item({ key: 'vi_933_leaf_wand', name: 'Leaf Wand', maxStack: 999, value: 1 });
393	item({ key: 'vi_832_living_wood_wand', name: 'Living Wood Wand', maxStack: 999, value: 1 });
394	item({ key: 'vi_4066_desert_minecart', name: 'Desert Minecart', maxStack: 999, value: 1 });
395	item({ key: 'vi_4450_shroom_minecart', name: 'Shroom Minecart', maxStack: 999, value: 1 });
396	item({ key: 'vi_4423_scarab_bomb', name: 'Scarab Bomb', maxStack: 999, value: 1 });
397	item({ key: 'vi_159_shiny_red_balloon', name: 'Shiny Red Balloon', maxStack: 999, value: 1 });
398	item({ key: 'vi_5258_see_the_world_for_what_it_is', name: 'See The World For What It Is', maxStack: 999, value: 1 });
399	item({ key: 'vi_65_starfury', name: 'Starfury', maxStack: 999, value: 1 });
400	item({ key: 'vi_5388_eye_of_the_sun', name: 'Eye of the Sun', maxStack: 999, value: 1 });
401	item({ key: 'vi_2219_celestial_magnet', name: 'Celestial Magnet', maxStack: 999, value: 1 });
402	item({ key: 'vi_5255_love_is_in_the_trash_slot', name: 'Love is in the Trash Slot', maxStack: 999, value: 1 });
403	item({ key: 'vi_4426_bee_minecart', name: 'Bee Minecart', maxStack: 999, value: 1 });
404	item({ key: 'vi_3017_flower_boots', name: 'Flower Boots', maxStack: 999, value: 1 });
405	item({ key: 'vi_3360_living_mahogany_wand', name: 'Living Mahogany Wand', maxStack: 999, value: 1 });
406	item({ key: 'vi_3361_rich_mahogany_leaf_wand', name: 'Rich Mahogany Leaf Wand', maxStack: 999, value: 1 });
407	item({ key: 'vi_1309_slime_staff', name: 'Slime Staff', maxStack: 999, value: 1 });
408	item({ key: 'vi_1845_necromantic_scroll', name: 'Necromantic Scroll', maxStack: 999, value: 1 });
409	item({ key: 'vi_1864_papyrus_scarab', name: 'Papyrus Scarab', maxStack: 999, value: 1 });
410	item({ key: 'vi_1158_pygmy_necklace', name: 'Pygmy Necklace', maxStack: 999, value: 1 });
411	item({ key: 'vi_3034_coin_ring', name: 'Coin Ring', maxStack: 999, value: 1 });
412	item({ key: 'vi_308_moonglow_seeds', name: 'Moonglow Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 1 });
413	item({ key: 'vi_312_fireblossom_seeds', name: 'Fireblossom Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 5 });
414	item({ key: 'vi_310_deathweed_seeds', name: 'Deathweed Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 4 });
415	item({ key: 'vi_307_daybloom_seeds', name: 'Daybloom Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 0 });
416	item({ key: 'vi_309_blinkroot_seeds', name: 'Blinkroot Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 2 });
417	item({ key: 'vi_2357_shiverthorn_seeds', name: 'Shiverthorn Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 6 });
418	item({ key: 'vi_311_waterleaf_seeds', name: 'Waterleaf Seeds', maxStack: 999, value: 1, tile: 'v_83_herbs_mature', placeStyle: 3 });
419	item({ key: 'vi_1828_pumpkin_seed', name: 'Pumpkin Seed', maxStack: 999, value: 1 });
420	item({ key: 'vi_126_bottled_water', name: 'Bottled Water', maxStack: 999, value: 1 });
421	item({ key: 'vi_1134_bottled_honey', name: 'Bottled Honey', maxStack: 999, value: 1 });
422	item({ key: 'vi_3068_guide_to_plant_fiber_cordage', name: 'Guide to Plant Fiber Cordage', maxStack: 999, value: 1 });
423	item({ key: 'vi_4779_mushroom_hat', name: 'Mushroom Hat', maxStack: 999, value: 1 });
424	item({ key: 'vi_4780_mushroom_vest', name: 'Mushroom Vest', maxStack: 999, value: 1 });
425	item({ key: 'vi_4781_mushroom_pants', name: 'Mushroom Pants', maxStack: 999, value: 1 });
426	
427	// ===================== FTW_V2 补全物品（占位收集品） =====================
428	item({ key: 'vi_678_red_potion', name: 'Red Potion', maxStack: 999, value: 1 });
429	item({ key: 'vi_281_blowpipe', name: 'Blowpipe', maxStack: 999, value: 1 });
430	item({ key: 'vi_293_mana_regeneration_potion', name: 'Mana Regeneration Potion', maxStack: 999, value: 1 });
431	item({ key: 'vi_2767_solar_tablet', name: 'Solar Tablet', maxStack: 999, value: 1 });
432	item({ key: 'vi_3213_money_trough', name: 'Money Trough', maxStack: 999, value: 1 });
433	item({ key: 'vi_2757_vortex_helmet', name: 'Vortex Helmet', maxStack: 999, value: 1 });
434	item({ key: 'vi_4989_soaring_insignia', name: 'Soaring Insignia', maxStack: 999, value: 1 });
435	item({ key: 'vi_3383_stardust_leggings', name: 'Stardust Leggings', maxStack: 999, value: 1 });
436	item({ key: 'vi_4914_kaleidoscope', name: 'Kaleidoscope', maxStack: 999, value: 1 });
437	item({ key: 'vi_1991_bug_net', name: 'Bug Net', maxStack: 999, value: 1 });
438	item({ key: 'vi_4828_superheated_blood', name: 'Superheated Blood', maxStack: 999, value: 1 });
439	item({ key: 'vi_3509_copper_pickaxe', name: 'Copper Pickaxe', maxStack: 999, value: 1 });
440	item({ key: 'vi_3507_copper_shortsword', name: 'Copper Shortsword', maxStack: 999, value: 1 });
441	item({ key: 'vi_4755_grox_the_great_s_horned_cowl', name: 'Grox The Great\'s Horned Cowl', maxStack: 999, value: 1 });
442	item({ key: 'vi_4756_grox_the_great_s_chestplate', name: 'Grox The Great\'s Chestplate', maxStack: 999, value: 1 });
443	item({ key: 'vi_4757_grox_the_great_s_greaves', name: 'Grox The Great\'s Greaves', maxStack: 999, value: 1 });
444	item({ key: 'vi_5000_terraspark_boots', name: 'Terraspark Boots', maxStack: 999, value: 1 });
445	item({ key: 'vi_5339_arcane_crystal', name: 'Arcane Crystal', maxStack: 999, value: 1 });
446	item({ key: 'vi_5391_uncumbering_stone', name: 'Uncumbering Stone', maxStack: 999, value: 1 });
447	item({ key: 'vi_2585_slime_hook', name: 'Slime Hook', maxStack: 999, value: 1 });
448	item({ key: 'vi_313_daybloom', name: 'Daybloom', maxStack: 999, value: 1 });
449	item({ key: 'vi_267_guide_voodoo_doll', name: 'Guide Voodoo Doll', maxStack: 999, value: 1 });
450	item({ key: 'vi_2649_steampunk_candle', name: 'Steampunk Candle', maxStack: 999, value: 1 });
451	item({ key: 'vi_286_sticky_glowstick', name: 'Sticky Glowstick', maxStack: 999, value: 1 });
452	item({ key: 'vi_3002_spelunker_glowstick', name: 'Spelunker Glowstick', maxStack: 999, value: 1 });
453	item({ key: 'vi_4819_demon_conch', name: 'Demon Conch', maxStack: 999, value: 1 });
454	item({ key: 'vi_1802_raven_staff', name: 'Raven Staff', maxStack: 999, value: 1 });
455	item({ key: 'vi_3382_stardust_plate', name: 'Stardust Plate', maxStack: 999, value: 1 });
456	item({ key: 'vi_3270_item_frame', name: 'Item Frame', maxStack: 999, value: 1 });
457	item({ key: 'vi_3771_ancient_horn', name: 'Ancient Horn', maxStack: 999, value: 1 });
458	item({ key: 'vi_4281_finch_staff', name: 'Finch Staff', maxStack: 999, value: 1 });
459	item({ key: 'vi_5407_star_royale_brick', name: 'Star Royale Brick', maxStack: 999, value: 1 });
460	item({ key: 'vi_5401_lunar_rust_brick', name: 'Lunar Rust Brick', maxStack: 999, value: 1 });
461	item({ key: 'vi_4716_mollusk_whistle', name: 'Mollusk Whistle', maxStack: 999, value: 1 });
462	item({ key: 'vi_3540_phantasm', name: 'Phantasm', maxStack: 999, value: 1 });
463	item({ key: 'vi_2176_shroomite_digging_claw', name: 'Shroomite Digging Claw', maxStack: 999, value: 1 });
464	item({ key: 'vi_2349_wrath_potion', name: 'Wrath Potion', maxStack: 999, value: 1 });
465	item({ key: 'vi_4679_morning_star', name: 'Morning Star', maxStack: 999, value: 1 });
466	item({ key: 'vi_1169_bone_key', name: 'Bone Key', maxStack: 999, value: 1 });
467	item({ key: 'vi_3863_betsy_mask', name: 'Betsy Mask', maxStack: 999, value: 1 });
468	item({ key: 'vi_3124_cell_phone', name: 'Cell Phone', maxStack: 999, value: 1 });
469	item({ key: 'vi_3506_copper_axe', name: 'Copper Axe', maxStack: 999, value: 1 });
470	item({ key: 'vi_4680_dark_harvest', name: 'Dark Harvest', maxStack: 999, value: 1 });
471	item({ key: 'vi_543_brown_pressure_plate', name: 'Brown Pressure Plate', maxStack: 999, value: 1 });
472	item({ key: 'vi_171_sign', name: 'Sign', maxStack: 999, value: 1 });
473	item({ key: 'vi_1723_living_wood_wall', name: 'Living Wood Wall', maxStack: 999, value: 1 });
474	item({ key: 'vi_4754_grox_the_great_s_wings', name: 'Grox The Great\'s Wings', maxStack: 999, value: 1 });
475	item({ key: 'vi_3353_mechanical_cart', name: 'Mechanical Cart', maxStack: 999, value: 1 });
476	item({ key: 'vi_2287_winter_cape', name: 'Winter Cape', maxStack: 999, value: 1 });
477	item({ key: 'vi_1179_chlorophyte_bullet', name: 'Chlorophyte Bullet', maxStack: 999, value: 1 });
478	item({ key: 'vi_4766_world_globe', name: 'World Globe', maxStack: 999, value: 1 });
479	item({ key: 'vi_4954_celestial_starboard', name: 'Celestial Starboard', maxStack: 999, value: 1 });
480	item({ key: 'vi_4730_ghostar_s_infinity_eight', name: 'Ghostar\'s Infinity Eight', maxStack: 999, value: 1 });
481	item({ key: 'vi_4758_blade_staff', name: 'Blade Staff', maxStack: 999, value: 1 });
482	item({ key: 'vi_4765_tree_globe', name: 'Tree Globe', maxStack: 999, value: 1 });
483	item({ key: 'vi_5342_ambrosia', name: 'Ambrosia', maxStack: 999, value: 1 });
484	item({ key: 'vi_5328_chest_lock', name: 'Chest Lock', maxStack: 999, value: 1 });
485	item({ key: 'vi_5343_peddler_s_satchel', name: 'Peddler\'s Satchel', maxStack: 999, value: 1 });
486	item({ key: 'vi_5285_moon_globe', name: 'Moon Globe', maxStack: 999, value: 1 });
487	item({ key: 'vi_5289_minecart_upgrade_kit', name: 'Minecart Upgrade Kit', maxStack: 999, value: 1 });
488	item({ key: 'vi_5336_advanced_combat_techniques_volume_two', name: 'Advanced Combat Techniques: Volume Two', maxStack: 999, value: 1 });
489	item({ key: 'vi_5451_kwad_racer_drone', name: 'Kwad Racer Drone', maxStack: 999, value: 1 });
490	item({ key: 'vi_5359_shellphone_spawn', name: 'Shellphone (Spawn)', maxStack: 999, value: 1 });
491	item({ key: 'vi_3032_super_absorbant_sponge', name: 'Super Absorbant Sponge', maxStack: 999, value: 1 });
492	item({ key: 'vi_3031_bottomless_water_bucket', name: 'Bottomless Water Bucket', maxStack: 999, value: 1 });
493	item({ key: 'vi_509_red_wrench', name: 'Red Wrench', maxStack: 999, value: 1 });
494	item({ key: 'vi_4741_butcher_s_bloodstained_apron', name: 'Butcher\'s Bloodstained Apron', maxStack: 999, value: 1 });
495	item({ key: 'vi_3065_star_wrath', name: 'Star Wrath', maxStack: 999, value: 1 });
496	item({ key: 'vi_3063_meowmere', name: 'Meowmere', maxStack: 999, value: 1 });
497	item({ key: 'vi_3372_lunatic_cultist_mask', name: 'Lunatic Cultist Mask', maxStack: 999, value: 1 });
498	item({ key: 'vi_1504_spectre_robe', name: 'Spectre Robe', maxStack: 999, value: 1 });
499	item({ key: 'vi_2769_cosmic_car_key', name: 'Cosmic Car Key', maxStack: 999, value: 1 });
500	item({ key: 'vi_216_shackle', name: 'Shackle', maxStack: 999, value: 1 });
501	item({ key: 'vi_4415_stone_door', name: 'Stone Door', maxStack: 999, value: 1 });
502	item({ key: 'vi_1681_skeleton_banner', name: 'Skeleton Banner', maxStack: 999, value: 1 });
503	item({ key: 'vi_283_seed', name: 'Seed', maxStack: 999, value: 1 });
504	item({ key: 'vi_1173_grave_marker', name: 'Grave Marker', maxStack: 999, value: 1 });
505	item({ key: 'vi_4379_wyvern_kite', name: 'Wyvern Kite', maxStack: 999, value: 1 });
506	item({ key: 'vi_4378_xenon_moss', name: 'Xenon Moss', maxStack: 999, value: 1 });
507	item({ key: 'vi_4377_krypton_moss', name: 'Krypton Moss', maxStack: 999, value: 1 });
508	item({ key: 'vi_4376_rat_cage', name: 'Rat Cage', maxStack: 999, value: 1 });
509	item({ key: 'vi_4375_rat', name: 'Rat', maxStack: 999, value: 1 });
510	item({ key: 'vi_4484_1_2_second_timer', name: '1/2 Second Timer', maxStack: 999, value: 1 });
511	item({ key: 'vi_4824_wet_bomb', name: 'Wet Bomb', maxStack: 999, value: 1 });
512	item({ key: 'vi_4485_1_4_second_timer', name: '1/4 Second Timer', maxStack: 999, value: 1 });
513	item({ key: 'vi_5378_cursed_flare', name: 'Cursed Flare', maxStack: 999, value: 1 });
514	item({ key: 'vi_5354_reflective_shades', name: 'Reflective Shades', maxStack: 999, value: 1 });
515	item({ key: 'vi_5387_raynbro_s_pants', name: 'Raynbro\'s Pants', maxStack: 999, value: 1 });
516	item({ key: 'vi_5386_raynbro_s_hoodie', name: 'Raynbro\'s Hoodie', maxStack: 999, value: 1 });
517	item({ key: 'vi_5390_raynbro_s_hood', name: 'Raynbro\'s Hood', maxStack: 999, value: 1 });
518	item({ key: 'vi_5338_aegis_fruit', name: 'Aegis Fruit', maxStack: 999, value: 1 });
519	item({ key: 'vi_5404_cosmic_ember_brick', name: 'Cosmic Ember Brick', maxStack: 999, value: 1 });
520	item({ key: 'vi_5405_cryocore_brick', name: 'Cryocore Brick', maxStack: 999, value: 1 });
521	item({ key: 'vi_5403_astra_brick', name: 'Astra Brick', maxStack: 999, value: 1 });
522	item({ key: 'vi_346_safe', name: 'Safe', maxStack: 999, value: 1 });
523	item({ key: 'vi_4829_cat_license', name: 'Cat License', maxStack: 999, value: 1 });
524	item({ key: 'vi_3335_demon_heart', name: 'Demon Heart', maxStack: 999, value: 1 });
525	item({ key: 'vi_4750_foodbarbarian_s_tattered_dragon_wings', name: 'FoodBarbarian\'s Tattered Dragon Wings', maxStack: 999, value: 1 });
526	item({ key: 'vi_3042_phase_dye', name: 'Phase Dye', maxStack: 999, value: 1 });
527	item({ key: 'vi_3024_skiphs_blood', name: 'Skiphs\' Blood', maxStack: 999, value: 1 });
528	item({ key: 'vi_3054_shadowflame_knife', name: 'Shadowflame Knife', maxStack: 999, value: 1 });
529	item({ key: 'vi_5275_joja_cola', name: 'Joja Cola', maxStack: 999, value: 1 });
530	item({ key: 'vi_5278_pomegranate', name: 'Pomegranate', maxStack: 999, value: 1 });
531	item({ key: 'vi_5277_spicy_pepper', name: 'Spicy Pepper', maxStack: 999, value: 1 });
532	item({ key: 'vi_5437_shellphone', name: 'Shellphone', maxStack: 999, value: 1 });
533	item({ key: 'vi_1507_spectre_hamaxe', name: 'Spectre Hamaxe', maxStack: 999, value: 1 });
534	item({ key: 'vi_2250_steampunk_chest', name: 'Steampunk Chest', maxStack: 999, value: 1 });
535	item({ key: 'vi_392_glass_wall', name: 'Glass Wall', maxStack: 999, value: 1 });
536	item({ key: 'vi_2699_weapon_rack', name: 'Weapon Rack', maxStack: 999, value: 1 });
537	item({ key: 'vi_3552_blue_flame_and_silver_dye', name: 'Blue Flame and Silver Dye', maxStack: 999, value: 1 });
538	item({ key: 'vi_5005_terraprisma', name: 'Terraprisma', maxStack: 999, value: 1 });
539	item({ key: 'vi_4604_exotic_chew_toy', name: 'Exotic Chew Toy', maxStack: 999, value: 1 });
540	item({ key: 'vi_4611_world_feeder_kite', name: 'World Feeder Kite', maxStack: 999, value: 1 });
541	item({ key: 'vi_4649_blue_jellyfish_kite', name: 'Blue Jellyfish Kite', maxStack: 999, value: 1 });
542	item({ key: 'vi_4796_dark_mage_s_tome', name: 'Dark Mage\'s Tome', maxStack: 999, value: 1 });
543	item({ key: 'vi_4553_plasma_lamp', name: 'Plasma Lamp', maxStack: 999, value: 1 });
544	item({ key: 'vi_4365_celestial_wand', name: 'Celestial Wand', maxStack: 999, value: 1 });
545	item({ key: 'vi_331_jungle_spores', name: 'Jungle Spores', maxStack: 999, value: 1 });
546	item({ key: 'vi_2430_slimy_saddle', name: 'Slimy Saddle', maxStack: 999, value: 1 });
547	item({ key: 'vi_4956_zenith', name: 'Zenith', maxStack: 999, value: 1 });
548	item({ key: 'vi_2798_laser_drill', name: 'Laser Drill', maxStack: 999, value: 1 });
549	item({ key: 'vi_2814_martian_chest', name: 'Martian Chest', maxStack: 999, value: 1 });
550	item({ key: 'vi_210_vine', name: 'Vine', maxStack: 999, value: 1 });
551	item({ key: 'vi_4371_yellow_kite', name: 'Yellow Kite', maxStack: 999, value: 1 });
552	item({ key: 'vi_4291_lemon', name: 'Lemon', maxStack: 999, value: 1 });
553	item({ key: 'vi_2493_king_slime_mask', name: 'King Slime Mask', maxStack: 999, value: 1 });
554	item({ key: 'vi_1919_sugar_cookie', name: 'Sugar Cookie', maxStack: 999, value: 1 });
555	item({ key: 'vi_1912_eggnog', name: 'Eggnog', maxStack: 999, value: 1 });
556	item({ key: 'vi_4023_grapes', name: 'Grapes', maxStack: 999, value: 1 });
557	item({ key: 'vi_4792_the_black_spot', name: 'The Black Spot', maxStack: 999, value: 1 });
558	item({ key: 'vi_3066_smooth_marble_block', name: 'Smooth Marble Block', maxStack: 999, value: 1 });
559	item({ key: 'vi_1103_slush_block', name: 'Slush Block', maxStack: 999, value: 1 });
560	item({ key: 'vi_2119_stone_slab', name: 'Stone Slab', maxStack: 999, value: 1 });
561	item({ key: 'vi_593_snow_block', name: 'Snow Block', maxStack: 999, value: 1 });
562	item({ key: 'vi_3081_marble_block', name: 'Marble Block', maxStack: 999, value: 1 });
563	item({ key: 'vi_1111_blue_berries', name: 'Blue Berries', maxStack: 999, value: 1 });
564	item({ key: 'vi_1115_red_husk', name: 'Red Husk', maxStack: 999, value: 1 });
565	item({ key: 'vi_217_molten_hamaxe', name: 'Molten Hamaxe', maxStack: 999, value: 1 });
566	item({ key: 'vi_122_molten_pickaxe', name: 'Molten Pickaxe', maxStack: 999, value: 1 });
567	item({ key: 'vi_1827_bladed_glove', name: 'Bladed Glove', maxStack: 999, value: 1 });
568	item({ key: 'vi_2263_white_dynasty_wall', name: 'White Dynasty Wall', maxStack: 999, value: 1 });
569	item({ key: 'vi_330_obsidian_brick_wall', name: 'Obsidian Brick Wall', maxStack: 999, value: 1 });
570	item({ key: 'vi_2433_stone_slab_wall', name: 'Stone Slab Wall', maxStack: 999, value: 1 });
571	item({ key: 'vi_452_hornet_statue', name: 'Hornet Statue', maxStack: 999, value: 1 });
572	item({ key: 'vi_453_bomb_statue', name: 'Bomb Statue', maxStack: 999, value: 1 });
573	item({ key: 'vi_360_armor_statue', name: 'Armor Statue', maxStack: 999, value: 1 });
574	item({ key: 'vi_3711_wraith_statue', name: 'Wraith Statue', maxStack: 999, value: 1 });
575	item({ key: 'vi_438_star_statue', name: 'Star Statue', maxStack: 999, value: 1 });
576	item({ key: 'vi_446_skeleton_statue', name: 'Skeleton Statue', maxStack: 999, value: 1 });
577	item({ key: 'vi_458_cross_statue', name: 'Cross Statue', maxStack: 999, value: 1 });
578	item({ key: 'vi_3655_scorpion_statue', name: 'Scorpion Statue', maxStack: 999, value: 1 });
579	item({ key: 'vi_328_shadow_chest', name: 'Shadow Chest', maxStack: 999, value: 1 });
580	item({ key: 'vi_2196_living_loom', name: 'Living Loom', maxStack: 999, value: 1 });
581	item({ key: 'vi_916_shadewood_work_bench', name: 'Shadewood Work Bench', maxStack: 999, value: 1 });
582	item({ key: 'vi_35_iron_anvil', name: 'Iron Anvil', maxStack: 999, value: 1 });
583	item({ key: 'vi_36_work_bench', name: 'Work Bench', maxStack: 999, value: 1 });
584	item({ key: 'vi_3240_tall_gate', name: 'Tall Gate', maxStack: 999, value: 1 });
585	item({ key: 'vi_337_red_banner', name: 'Red Banner', maxStack: 999, value: 1 });
586	item({ key: 'vi_3381_stardust_helmet', name: 'Stardust Helmet', maxStack: 999, value: 1 });
587	item({ key: 'vi_1765_vampire_pants', name: 'Vampire Pants', maxStack: 999, value: 1 });
588	item({ key: 'vi_2859_lunar_cultist_robe', name: 'Lunar Cultist Robe', maxStack: 999, value: 1 });
589	item({ key: 'vi_2857_lunar_cultist_hood', name: 'Lunar Cultist Hood', maxStack: 999, value: 1 });
590	item({ key: 'vi_2998_summoner_emblem', name: 'Summoner Emblem', maxStack: 999, value: 1 });
591	item({ key: 'vi_1175_headstone', name: 'Headstone', maxStack: 999, value: 1 });
592	item({ key: 'vi_25_wooden_door', name: 'Wooden Door', maxStack: 999, value: 1 });
593	item({ key: 'vi_46_light_s_bane', name: 'Light\'s Bane', maxStack: 999, value: 1 });
594	item({ key: 'vi_2340_minecart_track', name: 'Minecart Track', maxStack: 999, value: 1 });
595	item({ key: 'vi_498_mannequin', name: 'Mannequin', maxStack: 999, value: 1 });
596	item({ key: 'vi_4721_mushroom_beam', name: 'Mushroom Beam', maxStack: 999, value: 1 });
597	item({ key: 'vi_819_living_wood_door', name: 'Living Wood Door', maxStack: 999, value: 1 });
598	item({ key: 'vi_1458_obsidian_door', name: 'Obsidian Door', maxStack: 999, value: 1 });
599	item({ key: 'vi_3763_0x33_s_aviators', name: '0x33\'s Aviators', maxStack: 999, value: 1 });
600	item({ key: 'vi_176_mud_block', name: 'Mud Block', maxStack: 999, value: 1 });
601	item({ key: 'vi_1569_vampire_knives', name: 'Vampire Knives', maxStack: 999, value: 1 });
602	item({ key: 'vi_857_sandstorm_in_a_bottle', name: 'Sandstorm in a Bottle', maxStack: 999, value: 1 });
603	item({ key: 'vi_2292_fiberglass_fishing_pole', name: 'Fiberglass Fishing Pole', maxStack: 999, value: 1 });
604	item({ key: 'vi_5238_constellation', name: 'Constellation', maxStack: 999, value: 1 });
605	item({ key: 'vi_753_seaweed', name: 'Seaweed', maxStack: 999, value: 1 });
606	// FTW_V2 物品补全（第二轮）
607	item({ key: 'vi_3_stone_block', name: 'Stone Block', maxStack: 999, value: 1 });
608	item({ key: 'vi_94_wood_platform', name: 'Wood Platform', maxStack: 999, value: 1 });
609	item({ key: 'vi_75_fallen_star', name: 'Fallen Star', maxStack: 999, value: 1 });
610	item({ key: 'vi_26_stone_wall', name: 'Stone Wall', maxStack: 999, value: 1 });
611	item({ key: 'vi_214_hellstone_brick', name: 'Hellstone Brick', maxStack: 999, value: 1 });
612	item({ key: 'vi_93_wood_wall', name: 'Wood Wall', maxStack: 999, value: 1 });
613	item({ key: 'vi_172_ash_block', name: 'Ash Block', maxStack: 999, value: 1 });
614	item({ key: 'vi_118_hook', name: 'Hook', maxStack: 999, value: 1 });
615	item({ key: 'vi_529_red_pressure_plate', name: 'Red Pressure Plate', maxStack: 999, value: 1 });
616	item({ key: 'vi_183_glowing_mushroom', name: 'Glowing Mushroom', maxStack: 999, value: 1 });
617	item({ key: 'vi_130_gray_brick_wall', name: 'Gray Brick Wall', maxStack: 999, value: 1 });
618	item({ key: 'vi_352_keg', name: 'Keg', maxStack: 999, value: 1 });
619	
620	// 不负责任的女妖啤酒厂 补全物品（占位收集品）
621	item({ key: 'vi_5120_deer_thing', name: 'Deer Thing', maxStack: 999, value: 1 });
622	item({ key: 'vi_5508_grim_old_barb', name: 'Grim Old Barb', maxStack: 999, value: 1 });
623	item({ key: 'vi_5465_ram_rune', name: 'Ram Rune', maxStack: 999, value: 1 });
624	item({ key: 'vi_5500_goat_s_tuft', name: 'Goat\'s Tuft', maxStack: 999, value: 1 });
625	item({ key: 'vi_5499_froggy_neckband', name: 'Froggy Neckband', maxStack: 999, value: 1 });
626	item({ key: 'vi_5507_balloony_beads', name: 'Balloony Beads', maxStack: 999, value: 1 });
627	item({ key: 'vi_5485_chicken_charm', name: 'Chicken Charm', maxStack: 999, value: 1 });
628	item({ key: 'vi_5502_cat_chime', name: 'Cat Chime', maxStack: 999, value: 1 });
629	item({ key: 'vi_5504_turkey_wattle_necklace', name: 'Turkey Wattle Necklace', maxStack: 999, value: 1 });
630	item({ key: 'vi_5506_crow_s_beak', name: 'Crow\'s Beak', maxStack: 999, value: 1 });
631	item({ key: 'vi_5503_dog_collar', name: 'Dog Collar', maxStack: 999, value: 1 });
632	item({ key: 'vi_5534_fairy_choker', name: 'Fairy Choker', maxStack: 999, value: 1 });
633	item({ key: 'vi_5484_cow_bell', name: 'Cow Bell', maxStack: 999, value: 1 });
634	item({ key: 'vi_5501_old_companion_locket', name: 'Old Companion Locket', maxStack: 999, value: 1 });
635	item({ key: 'vi_5509_vampire_pendant', name: 'Vampire Pendant', maxStack: 999, value: 1 });
636	item({ key: 'vi_5505_mean_goblin_s_spikes', name: 'Mean Goblin\'s Spikes', maxStack: 999, value: 1 });
637	item({ key: 'vi_5525_cursed_piper_flute', name: 'Cursed Piper Flute', maxStack: 999, value: 1 });
638	
639	
640	// ---- 阶段 5:v_ 图块放置物品自动注册 + 掉落连线 ----
641	// 每个 v_ 图块注册 place_v_<key> 放置物品(tryPlace 走 vanilla style 帧语义);
642	// 无掉落的 v_ 图块 drop 连到该物品(破坏可回收再放置)。
643	import { TILE_DEFS } from './tiles';
644	for (const td of TILE_DEFS) {
645	  if (!td.key.startsWith('v_')) continue;
646	  const ik = 'place_' + td.key;
647	  if (byKey[ik] === undefined) {
648	    item({ key: ik, name: td.name, maxStack: 999, value: 1, tile: td.key });
649	  }
650	  // 掉落连线在读取端回退(World.breakTileAt),避免多模块实例下改写失效
651	}
652	void 0;
653	
654	// ---- 阶段 5:生物群系草种子(种出对应草块)----
655	item({ key: 'corrupt_grass_seeds', name: '腐化草地种子', maxStack: 999, value: 1, tile: 'v_23_corrupt_grass_block' });
656	item({ key: 'crimson_grass_seeds', name: '猩红草地种子', maxStack: 999, value: 1, tile: 'v_199_crimson_grass_block' });
657	item({ key: 'jungle_grass_seeds', name: '丛林草地种子', maxStack: 999, value: 1, tile: 'v_60_jungle_grass_block' });
658	item({ key: 'mushroom_grass_seeds', name: '蘑菇草地种子', maxStack: 999, value: 1, tile: 'v_70_mushroom_grass_block' });
659	
660	
661	// ---- 阶段 5:原版物品全量注册(6146 件,图标走 atlas.vicon(id) 回退) ----
662	import vanillaItemMeta from '../../public/sprites/vanilla.json';
663	const _vim = (vanillaItemMeta as unknown as { items: Record<string, { name: string; key: string }> }).items ?? {};
664	for (const [idStr, m] of Object.entries(_vim)) {
665	  if (!m || typeof m.key !== 'string' || !m.key) continue;
666	  const ik = 'vi_' + idStr + '_' + m.key.replace(/[^A-Za-z0-9]/g, '');
667	  if (byKey[ik] !== undefined) continue;
668	  item({ key: ik, name: m.name, maxStack: 999, value: 1 });
669	}
670	void 0;
671	
672	// ---- 阶段 6:功能道具(桶三态/绳圈) ----
673	item({ key: 'empty_bucket', name: '空桶', maxStack: 99, value: 1, desc: '右键舀取液体' });
674	item({ key: 'water_bucket', name: '水桶', maxStack: 1, value: 1, desc: '右键放置水' });
675	item({ key: 'lava_bucket', name: '岩浆桶', maxStack: 1, value: 1, desc: '右键放置岩浆' });
676	item({ key: 'honey_bucket', name: '蜂蜜桶', maxStack: 1, value: 1, desc: '右键放置蜂蜜' });
677	
678	// ---- 阶段 6 第三轮:替代矿工具链(官方数值,与铜/铁/银/金同档) ----
679	item({ key: 'tin_pickaxe', name: '锡镐', maxStack: 1, value: 400,
680	  tool: { type: 'pick', power: 35, damage: 4, speed: 23, knockback: 2, reach: 2.6 * 16 } });
681	item({ key: 'tin_axe', name: '锡斧', maxStack: 1, value: 350,
682	  tool: { type: 'axe', power: 7, damage: 3, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
683	item({ key: 'tin_sword', name: '锡剑', maxStack: 1, value: 450,
684	  tool: { type: 'sword', damage: 8, speed: 23, knockback: 5, reach: 2.2 * 16 } });
685	item({ key: 'lead_pickaxe', name: '铅镐', maxStack: 1, value: 900,
686	  tool: { type: 'pick', power: 45, damage: 5, speed: 22, knockback: 2.5, reach: 2.6 * 16 } });
687	item({ key: 'lead_axe', name: '铅斧', maxStack: 1, value: 800,
688	  tool: { type: 'axe', power: 9, damage: 4, speed: 30, knockback: 5, reach: 2.4 * 16 } });
689	item({ key: 'lead_sword', name: '铅剑', maxStack: 1, value: 900,
690	  tool: { type: 'sword', damage: 10, speed: 23, knockback: 5, reach: 2.2 * 16 } });
691	item({ key: 'tungsten_pickaxe', name: '钨镐', maxStack: 1, value: 1800,
692	  tool: { type: 'pick', power: 55, damage: 6, speed: 21, knockback: 2.5, reach: 2.6 * 16 } });
693	item({ key: 'tungsten_axe', name: '钨斧', maxStack: 1, value: 1600,
694	  tool: { type: 'axe', power: 11, damage: 5, speed: 29, knockback: 5.5, reach: 2.4 * 16 } });
695	item({ key: 'tungsten_sword', name: '钨剑', maxStack: 1, value: 1800,
696	  tool: { type: 'sword', damage: 13, speed: 22, knockback: 5.5, reach: 2.2 * 16 } });
697	item({ key: 'platinum_pickaxe', name: '铂金镐', maxStack: 1, value: 3600,
698	  tool: { type: 'pick', power: 59, damage: 7, speed: 20, knockback: 3, reach: 2.6 * 16 } });
699	item({ key: 'platinum_axe', name: '铂金斧', maxStack: 1, value: 3200,
700	  tool: { type: 'axe', power: 13, damage: 6, speed: 28, knockback: 6, reach: 2.4 * 16 } });
701	item({ key: 'platinum_sword', name: '铂金剑', maxStack: 1, value: 3600,
702	  tool: { type: 'sword', damage: 15, speed: 22, knockback: 6, reach: 2.2 * 16 } });
703	
704	// ---- 阶段 6 第五轮:弓箭系统(官方数值:木弓 9 伤/UseTime 28;箭伤 4 木/5 燃烧) ----
705	item({ key: 'wooden_bow', name: '木弓', maxStack: 1, value: 100,
706	  ranged: { damage: 9, speed: 28, knockback: 1, ammo: 'wooden_arrow', projSpeed: 11 } });
707	item({ key: 'wooden_arrow', name: '木箭', maxStack: 999, value: 1 });
708	item({ key: 'flaming_arrow', name: '燃烧箭', maxStack: 999, value: 1 });
709	item({ key: 'iron_bow', name: '铁弓', maxStack: 1, value: 360,
710	  ranged: { damage: 11, speed: 25, knockback: 1.5, ammo: 'wooden_arrow', projSpeed: 11 } });
711	
712	// ---- 阶段 6 第六轮:矿车 ----
713	item({ key: 'minecart_item', name: '矿车', maxStack: 99, value: 1, desc: '右键轨道放置并骑乘' });
714	
715	// ---- 阶段 6 第八轮:魔法武器(官方数值:火花法杖 ItemID 3067 伤12/魔力15/UseTime 21/射速 9) ----
716	item({ key: 'wand_of_sparking', name: '火花法杖', maxStack: 1, value: 100,
717	  magic: { damage: 12, speed: 21, manaCost: 5, projSpeed: 9, proj: 'spark' } });
718	item({ key: 'amethyst_bolt', name: '紫晶法杖', maxStack: 1, value: 900,
719	  magic: { damage: 14, speed: 26, manaCost: 5, projSpeed: 9, proj: 'bolt' } });
720	
721	// ---- 阶段 6 第九轮:Boss 召唤物(官方:蠕虫食物 70/血腥脊椎 1331/史莱姆王冠 560) ----
722	item({ key: 'worm_food', name: '蠕虫食物', maxStack: 20, value: 1, desc: '腐化之地使用:召唤世界吞噬者' });
723	item({ key: 'bloody_spine', name: '血腥脊椎', maxStack: 20, value: 1, desc: '猩红之地使用:召唤克苏鲁之脑' });
724	item({ key: 'slime_crown', name: '史莱姆王冠', maxStack: 20, value: 1, desc: '任意时刻:召唤史莱姆王' });
725	

```


---

## 🤖 Assistant · 2026-08-09T09:09:28.098Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now Player.ts, SaveFile.ts, KvStore.ts, recipes.ts, WorldGen.ts, World.ts. Also SpriteAtlas.ts, index.html, package.json. Batch reads.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:28.099Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:28.101Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:28.111Z

**📎 ToolResult**

```
1	// 玩家实体：移动、跳跃、游泳、Buff/配饰属性聚合、摔伤
2	import { Entity } from './Entity';
3	import type { GameHooks } from './types';
4	import {
5	  GRAVITY, MAX_FALL_SPEED, PLAYER_WALK_ACCEL, PLAYER_WALK_MAX,
6	  PLAYER_FRICTION, PLAYER_AIR_FRICTION, PLAYER_JUMP_SPEED, PLAYER_JUMP_TICKS,
7	  PLAYER_IFRAME_TICKS, TILE,
8	} from '../core/constants';
9	import { moveAndCollide } from '../physics/TileCollision';
10	import { Inventory, ACCESSORY_START } from '../items/Inventory';
11	import { BuffState } from '../stats/Buffs';
12	import { ITEM_DEFS } from '../data/items';
13	import { TILE_DEFS } from '../data/tiles';
14	
15	// 摔伤参数（移植自 Maples Player.Fall，单位换算为 tile）
16	// 对齐原版体感：跳跃/小坡绝不受伤（原版约 25 格起伤）；落水另行豁免
17	const FALL_SAFE_TILES = 22;
18	const FALL_FATAL_TILES = 45;
19	
20	export class Player extends Entity {
21	  w = 16; h = 39;        // 16×39：1 格宽碰撞盒 + 前向偏移
22	  facing = 1;            // 1 右 -1 左
23	  baseMaxHp = 100;
24	  baseMaxMana = 20;   // 原版 statManaMax2 起步 20,坠落之星 +20/颗(上限 200)
25	  mana = 20;
26	  manaRegenAccum = 0;
27	  hp = 100;
28	  inv: Inventory;
29	  buffs = new BuffState();
30	  iframes = 0;
31	  jumpHold = 0;          // 长按跳跃剩余加速 tick
32	  inWater = false;
33	  headUnderwater = false;
34	  // 气口：5 个气泡，共 23.33 秒（原版参数），每颗 ≈4.67 秒
35	  static readonly BREATH_BUBBLES = 5;
36	  static readonly BREATH_SECONDS = 23.33;
37	  breath = Player.BREATH_BUBBLES;
38	  private breathAccum = 0;
39	  private drownAccum = 0;
40	  inLava = false;
41	  private lavaAccum = 0;
42	  animTime = 0;          // 走路动画计时
43	  useTime = 0;           // 通用动作冷却
44	  dead = false;
45	  respawnTimer = 0;
46	  // 摔伤追踪
47	  private fallStartY: number | null = null;
48	  private surfaceJumpCd = 0;  // 水面起跳冷却
49	  sinceHurt = 0;               // 距上次受击 tick（自然回血计时；渲染层读取做心心跳动效）
50	  private regenAccum = 0;
51	  stepRenderY = 0;             // 跨台阶的渲染高度补偿（缓动到 0，消除瞬移顿挫）
52	
53	  constructor(x: number, y: number, inv: Inventory) {
54	    super();
55	    this.x = x; this.y = y;
56	    this.inv = inv;
57	  }
58	
59	  // ---- 配饰效果（重算式聚合，幂等）----
60	  get hasHorseshoe(): boolean {
61	    for (let i = ACCESSORY_START; i < this.inv.slots.length; i++) {
62	      const s = this.inv.slots[i];
63	      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
64	    }
65	    return false;
66	  }
67	  get hasFeralClaws(): boolean {
68	    for (let i = ACCESSORY_START; i < this.inv.slots.length; i++) {
69	      const s = this.inv.slots[i];
70	      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
71	    }
72	    return false;
73	  }
74	  /** 防御 = 基础(0) + 盔甲 + 铁皮 Buff(+6)（时装不计） */
75	  get defense(): number {
76	    let d = this.buffs.defenseBonus;
77	    for (const id of this.inv.equippedArmor()) {
78	      if (id != null) d += ITEM_DEFS[id]?.armor?.defense ?? 0;
79	    }
80	    return d;
81	  }
82	  get maxHp(): number {
83	    return this.baseMaxHp + this.buffs.healthBonus;
84	  }
85	  get maxMana(): number {
86	    return this.baseMaxMana;
87	  }
88	  get thornsActive(): boolean {
89	    return this.buffs.hasThorns;
90	  }
91	  /** 近战攻速倍率（猛爪手套 ×2） */
92	  get attackSpeedMult(): number {
93	    return this.hasFeralClaws ? 2 : 1;
94	  }
95	  /** 近战伤害加成（猛爪手套 +5） */
96	  get meleeDamageBonus(): number {
97	    return this.hasFeralClaws ? 5 : 0;
98	  }
99	
100	  get frame(): number {
101	    if (!this.onGround) return 4;
102	    if (Math.abs(this.vx) > 0.3) {
103	      return 1 + Math.floor(this.animTime / 8) % 3;
104	    }
105	    return 0;
106	  }
107	
108	  fixedUpdate(dt: number, game: GameHooks) {
109	    const world = game.world;
110	    if (this.iframes > 0) this.iframes--;
111	    if (this.useTime > 0) this.useTime--;
112	
113	    // Buff tick：自然回复（恢复 Buff）
114	    const buffHeal = this.buffs.tick(dt);
115	    if (buffHeal > 0 && this.hp > 0) this.hp = Math.min(this.maxHp, this.hp + buffHeal);
116	    // 自然回血：脱离战斗 5 秒后每秒缓回 1 点
117	    this.sinceHurt++;
118	    if (this.sinceHurt > 300 && this.hp > 0 && this.hp < this.maxHp) {
119	      this.regenAccum += dt;
120	      if (this.regenAccum >= 1) {
121	        this.regenAccum -= 1;
122	        this.hp = Math.min(this.maxHp, this.hp + 1);
123	      }
124	    }
125	    // 上限收缩时钳制
126	    if (this.hp > this.maxHp) this.hp = this.maxHp;
127	    // 魔力自然回复(原版 Player.manaRegen:越满越快,简化为每秒 maxMana*0.08+0.5)
128	    if (this.mana < this.maxMana) {
129	      this.manaRegenAccum += dt;
130	      if (this.manaRegenAccum >= 1) {
131	        this.manaRegenAccum -= 1;
132	        this.mana = Math.min(this.maxMana, this.mana + Math.ceil(this.maxMana * 0.08) + 1);
133	      }
134	    }
135	
136	    // 液体检测：身体采样在脚底上方固定 4px（贴脚即入水，不随身高缩放）
137	    const liq = world.store.liquid[world.store.idx(
138	      Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 4) / TILE),
139	    )];
140	    const wasInWater = this.inWater;
141	    this.inWater = liq > 100;
142	    // 入水瞬间：水花声（出水不响）
143	    if (this.inWater && !wasInWater) game.playSfx('splash');
144	    const centerIdx = world.store.idx(Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 4) / TILE));
145	    this.inLava = world.store.liquidType[centerIdx] === 2 && world.store.liquid[centerIdx] > 60;
146	    const headLiq = world.store.liquid[world.store.idx(
147	      Math.floor(this.cx / TILE), Math.floor((this.y + 8) / TILE), // 鼻子位置（头顶下方半格）
148	    )];
149	    const prevHeadUnderwater = this.headUnderwater; // 旧值（判定"刚出水"必须用更新前状态）
150	    this.headUnderwater = headLiq > 40; // 液面漫过鼻子（低阈值——部分液体也浸没）
151	    // 岩浆伤害：每半秒 15
152	    if (this.inLava) {
153	      this.lavaAccum += dt;
154	      if (this.lavaAccum >= 0.5) {
155	        this.lavaAccum = 0;
156	        this.damage(15, this.cx, this.y - 10);
157	        game.addDamageNumber(this.cx, this.y, 15, false, '#FF6020');
158	      }
159	    } else this.lavaAccum = 0;
160	
161	    // 气口：头部浸水时 23.33 秒耗尽，耗尽后每秒掉 10 血；出水立即恢复
162	    const wasHead = prevHeadUnderwater;
163	    if (this.headUnderwater) {
164	      this.breathAccum += dt;
165	      const per = Player.BREATH_SECONDS / Player.BREATH_BUBBLES;
166	      while (this.breathAccum >= per && this.breath > 0) {
167	        this.breathAccum -= per;
168	        this.breath--;
169	      }
170	      if (this.breath <= 0) {
171	        this.drownAccum += dt;
172	        if (this.drownAccum >= 1) {
173	          this.drownAccum -= 1;
174	          this.damage(10, this.cx, this.y - 10, false); // 窒息环境伤害：只掉血，无击退
175	          game.playSfx('drown');
176	          game.addDamageNumber(this.cx, this.y, 10, false, '#FF5050'); // 与受击同色
177	        }
178	      }
179	    } else if (wasHead || this.breath < Player.BREATH_BUBBLES) {
180	      // 出水补气。关键：刚出水时 breath 可能仍为满值但有一颗正在渐隐消耗中
181	      // （breathAccum > 0）——只判 breath==5 会跳过补气导致气泡瞬间消失。
182	      // 余量取「整口气 + 正在消耗那颗的剩余比例」的精确小数，从该状态回满
183	      const per = Player.BREATH_SECONDS / Player.BREATH_BUBBLES;
184	      const drainRemain = wasHead ? Math.max(0, Math.min(1, 1 - this.breathAccum / per)) : 1;
185	      this.refillFrom = Math.min(Player.BREATH_BUBBLES, this.breath - 1 + drainRemain);
186	      const missing = 1 - this.refillFrom / Player.BREATH_BUBBLES;
187	      this.breath = Player.BREATH_BUBBLES;
188	      this.breathAccum = 0;
189	      this.drownAccum = 0;
190	      // 补气时长：缺口比例（1.11s × 缺口），保底 0.55s 能看清；满后停留 0.35s 再隐藏
191	      this.refillDur = Math.max(0.55, 1.11 * missing);
192	      this.refillT = 0;
193	    }
194	    // 补气动画推进（补满后停留 REFILL_HOLD 再隐藏）
195	    if (this.refillT >= 0) {
196	      this.refillT += dt;
197	      if (this.refillT >= this.refillDur + 0.15) this.refillT = -1;
198	    }
199	
200	    // 死亡等待重生（任何死法统一在此发声——溺水/岩浆/摔落/受击都经过这里）
201	    if (this.hp <= 0) {
202	      if (!this.dead) game.playSfx('pkilled');
203	      this.dead = true;
204	      return;
205	    }
206	
207	    // 水平（敏捷 Buff 提速）
208	    const speedMult = this.buffs.moveSpeedMult;
209	    const ix = this.inputX;
210	    if (ix !== 0) {
211	      this.vx += ix * PLAYER_WALK_ACCEL * (this.inWater ? 0.6 : 1) * speedMult;
212	      this.facing = ix;
213	    } else {
214	      this.vx *= this.onGround ? PLAYER_FRICTION : PLAYER_AIR_FRICTION;
215	      if (Math.abs(this.vx) < 0.05) this.vx = 0;
216	    }
217	    const maxSpd = PLAYER_WALK_MAX * (this.inWater ? 0.55 : 1) * speedMult;
218	    this.vx = Math.max(-maxSpd, Math.min(maxSpd, this.vx));
219	
220	    // 绳索攀爬(原版:身体中心格为绳(213/353/950-9)时无重力,上/下键攀爬,左右离绳)
221	    const st = world.store;
222	    const ropeTx = Math.floor((this.x + this.w / 2) / TILE);
223	    const ropeTy = Math.floor((this.y + this.h / 2) / TILE);
224	    const ropeHere = !!(st.inBounds(ropeTx, ropeTy) && st.flags[st.idx(ropeTx, ropeTy)]
225	      && TILE_DEFS[st.type[st.idx(ropeTx, ropeTy)]]?.rope);
226	    this.onRope = ropeHere;
227	    if (ropeHere && !this.inWater) {
228	      // 上爬 2.2 / 下滑 3.0(原版攀爬速度),静止缓降 0.6
229	      if (this.inputJump) this.vy = Math.max(this.vy - 0.62, -2.2);
230	      else if (this.inputDown) this.vy = Math.min(this.vy + 0.5, 3.0);
231	      else this.vy = Math.min(this.vy + 0.08, 0.6);
232	      this.vy = Math.max(-2.2, Math.min(3.0, this.vy));
233	      this.fallStartY = null; // 绳上不计摔伤
234	    } else
235	    // 跳跃 / 游泳
236	    if (this.inWater) {
237	      // 头部露出水面（踩水状态）→ 允许正常力度起跳跃上岸块（带冷却防连跳）
238	      if (this.inputJump && !this.headUnderwater) {
239	        if (this.surfaceJumpCd <= 0) {
240	          this.vy = -PLAYER_JUMP_SPEED;
241	          this.jumpHold = PLAYER_JUMP_TICKS;
242	          this.surfaceJumpCd = 24;
243	        }
244	      } else if (this.inputJump) {
245	        // 全浸没：游泳上浮
246	        this.vy = Math.max(this.vy - 0.62, -4.4);
247	      }
248	      if (this.surfaceJumpCd > 0) this.surfaceJumpCd--;
249	      this.vy += GRAVITY * 0.3;
250	      this.vy = Math.max(-4.6, Math.min(3.0, this.vy));
251	      this.fallStartY = null;
252	    } else {
253	      if (this.inputJump && this.onGround) {
254	        this.vy = -PLAYER_JUMP_SPEED;
255	        this.jumpHold = PLAYER_JUMP_TICKS;
256	      }
257	      if (this.inputJump && this.jumpHold > 0) {
258	        this.vy -= 0.22;
259	        this.jumpHold--;
260	      } else {
261	        this.jumpHold = 0;
262	      }
263	      this.vy = Math.min(this.vy + GRAVITY, MAX_FALL_SPEED);
264	    }
265	    // 松键截断上升（手感）
266	    if (!this.inputJump && this.vy < -2) this.vy = -2;
267	
268	    // 摔伤追踪：开始下落记录高度，落地结算
269	    if (!this.onGround && this.vy > 0 && this.fallStartY === null) {
270	      this.fallStartY = this.y;
271	    }
272	    if (this.vy < -0.1) this.fallStartY = null; // 重新上升则重置
273	
274	    this.dropThrough = !!this.inputDown;
275	    moveAndCollide(this, world, this.vx, this.vy);
276	
277	    // 边缘滑落：已移除（改为收窄支撑判定宽度——本质相同但无侧推力）
278	    if (false) {
279	      const fy = Math.floor((this.y + this.h + 1) / TILE);
280	      const fx0 = Math.floor(this.x / TILE), fx1 = Math.floor((this.x + this.w - 0.01) / TILE);
281	      let support = 0;
282	      let supportX = 0; // 支撑面积加权重心
283	      for (let tx = fx0; tx <= fx1; tx++) {
284	        if (!world.store.isSolid(tx, fy)) continue;
285	        const left = Math.max(this.x, tx * TILE);
286	        const right = Math.min(this.x + this.w, tx * TILE + TILE);
287	        const ov = Math.max(0, right - left);
288	        support += ov;
289	        supportX += (left + right) / 2 * ov;
290	      }
291	      // 主动移动（上行爬坡/走动）时只在彻底失撑（≤2px）才坠落，不参与缓滑——
292	      // 爬台阶时身体经常大半悬空，缓滑会把人往回推；静止站边缘才触发缓滑
293	      const moving = this.inputX !== 0 && Math.abs(this.vx) > 0.3;
294	      // 固定 3px 阈值：几乎完全悬空才滑落（比例阈值对放大后的宽碰撞盒过敏）
295	      void moving;
296	      if (support > 0 && support < 3) {
297	        const cen = supportX / support;
298	        const dir = cen < this.cx ? 1 : -1; // 支撑在身体哪侧，就往反侧滑
299	        if (support <= 2) {
300	          this.x += dir * 1.2;
301	          this.onGround = false; // 彻底失撑，下坠
302	        } else {
303	          this.x += dir * 0.9; // 缓慢滑向悬空侧
304	        }
305	      }
306	    }
307	
308	    // 自动上台阶：贴地行走撞 1 格高台阶且上方净空 → 直接踏上去（无需跳跃）
309	    // 注意碰撞后 vx 已清零，用输入方向判断
310	    if (this.onGround && this.hitWall && this.inputX !== 0) {
311	      const dir = this.inputX;
312	      const frontX = dir > 0 ? this.x + this.w + 1 : this.x - 1;
313	      const fx = Math.floor(frontX / TILE);
314	      const fy = Math.floor((this.y + this.h - 1) / TILE);
315	      const stepSolid = world.store.isSolid(fx, fy);
316	      const headroom = !world.store.isSolid(fx, fy - 1) && !world.store.isSolid(fx, fy - 2);
317	      if (stepSolid && headroom) {
318	        const ny = this.y - TILE;
319	        // 抬升后自身所占空间必须无实心
320	        let clear = true;
321	        const tx0 = Math.floor(this.x / TILE), tx1 = Math.floor((this.x + this.w - 1) / TILE);
322	        const ty0 = Math.floor(ny / TILE), ty1 = Math.floor((ny + this.h - 1) / TILE);
323	        for (let tx = tx0; tx <= tx1 && clear; tx++) {
324	          for (let ty = ty0; ty <= ty1; ty++) {
325	            if (world.store.isSolid(tx, ty)) { clear = false; break; }
326	          }
327	        }
328	        if (clear) {
329	          this.y = ny;
330	          this.x += dir * 2.5;
331	          this.onGround = true;
332	          this.stepRenderY = TILE; // 渲染补偿：从旧高度缓升，消除瞬移顿挫
333	        }
334	      }
335	    }
336	    // 台阶视觉缓动：每帧向 0 收敛
337	    if (this.stepRenderY > 0.5) this.stepRenderY *= 0.55;
338	    else this.stepRenderY = 0;
339	
340	    // 落地摔伤结算（幸运马掌免疫；落在水里豁免——水有缓冲）
341	    if (this.onGround && this.fallStartY !== null) {
342	      const fallTiles = (this.y - this.fallStartY) / TILE;
343	      this.fallStartY = null;
344	      const feetLiq = world.store.liquid[world.store.idx(Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 1) / TILE))];
345	      const landedInWater = feetLiq > 60 || this.inWater;
346	      if (landedInWater) { /* 落水缓冲：不计摔伤 */ }
347	      else if (fallTiles > FALL_SAFE_TILES && !this.hasHorseshoe) {
348	        const t = Math.min(1, (fallTiles - FALL_SAFE_TILES) / (FALL_FATAL_TILES - FALL_SAFE_TILES));
349	        const dmgPercent = 10 + 90 * t * t * t; // 10%~100% 三次方曲线（Maples 公式）
350	        const dmg = Math.max(1, Math.round((dmgPercent / 100) * this.hp));
351	        this.damage(dmg, this.cx, this.y - 10);
352	        game.playSfx('hurt');
353	        game.addDamageNumber(this.cx, this.y, dmg, false, '#FF5050');
354	      }
355	    }
356	
357	    // 走跑动画计时（仅地面；空中贴图静态不参与动画）
358	    if (Math.abs(this.vx) > 0.3 && this.onGround) this.animTime += Math.abs(this.vx);
359	    else this.animTime = 0;
360	
361	    // 越界保护
362	    const maxY = world.h * TILE;
363	    if (this.y > maxY + 100) this.damage(9999, this.cx, this.y);
364	  }
365	
366	  /** 出水补气动画进度 0..1（-1 = 未在补气） */
367	  refillT = -1;
368	  refillDur = 1.11; // 本次补气总时长（按出水时的缺口比例：1.11s × 缺口）
369	  refillFrom = 0;   // 出水时的余量（补气动画从此处起填）
370	  static readonly REFILL_HOLD = 0.35; // 补满后满格停留时长
371	  get refill01(): number {
372	    return this.refillT < 0 ? 1 : Math.min(1, this.refillT / this.refillDur);
373	  }
374	
375	  /** 当前正在消耗的那口气泡进度 0..1（1=满，趋 0 渐隐）；头部浸水外为 0 */
376	  get breathDrain01(): number {
377	    if (!this.headUnderwater || this.breath <= 0) return 0;
378	    const per = Player.BREATH_SECONDS / Player.BREATH_BUBBLES;
379	    return Math.max(0, Math.min(1, 1 - this.breathAccum / per));
380	  }
381	
382	  // 输入状态由 Game 每帧写入
383	  inputX = 0;
384	  inputJump = false;
385	  inputDown = false;
386	  inputUp = false;
387	  onRope = false;
388	
389	  /** 受击：防御减伤公式 max(1, dmg - defense*0.5)（移植自 Maples Player.OnAttacked）。
390	   *  knockback=false 用于窒息等环境伤害（只掉血不击退） */
391	  damage(dmg: number, srcX: number, srcY: number, knockback = true): boolean {
392	    if (this.iframes > 0 || this.dead) return false;
393	    const reduction = Math.max(1, dmg - this.defense * 0.5);
394	    this.hp -= reduction;
395	    this.iframes = PLAYER_IFRAME_TICKS;
396	    this.sinceHurt = 0; // 受击打断自然回血
397	    // 击退
398	    if (knockback) {
399	      const dir = this.cx < srcX ? -1 : 1;
400	      this.vx = dir * 3.4;
401	      this.vy = -3;
402	    }
403	    return true;
404	  }
405	
406	  draw() { /* 由 Renderer 统一绘制 */ }
407	}
408	

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:28.111Z

**📎 ToolResult**

```
1	// 自有存档格式：JSON 外壳（人可读）+ RLE 二进制 tile 段（base64）
2	import type { World } from '../world/World';
3	import { World as WorldClass } from '../world/World';
4	import type { Player } from '../entities/Player';
5	
6	// ---- varint / base64 工具 ----
7	function writeVarint(out: number[], v: number) {
8	  v = v < 0 ? 0 : v;
9	  while (v >= 0x80) {
10	    out.push((v & 0x7f) | 0x80);
11	    v >>>= 7;
12	  }
13	  out.push(v);
14	}
15	
16	export function bytesToB64(bytes: number[]): string {
17	  const u8 = new Uint8Array(bytes);
18	  let s = '';
19	  for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]);
20	  return btoa(s);
21	}
22	
23	function b64ToBytes(b64: string): Uint8Array {
24	  const s = atob(b64);
25	  const u8 = new Uint8Array(s.length);
26	  for (let i = 0; i < s.length; i++) u8[i] = s.charCodeAt(i);
27	  return u8;
28	}
29	
30	function readVarint(u8: Uint8Array, pos: { i: number }): number {
31	  let v = 0, shift = 0;
32	  while (pos.i < u8.length) {
33	    const b = u8[pos.i++];
34	    v |= (b & 0x7f) << shift;
35	    if (!(b & 0x80)) break;
36	    shift += 7;
37	  }
38	  return v;
39	}
40	
41	// ---- 正式 RLE 格式 ----
42	// tiles 每条目: varint(run-1) varint(type) [varint(frameX) varint(frameY) 仅当 type!=0]
43	// walls/liquid: varint(run-1) varint(value)
44	
45	export interface SaveData {
46	  format: 'sandboxworld.save';
47	  version: number;
48	  header: {
49	    name: string; seed: number; width: number; height: number;
50	    spawn: [number, number]; groundLevel: number; rockLevel: number;
51	    crimson?: boolean; dungeonX?: number; jungleX?: number;
52	    treeX?: number[]; treeStyle?: number[]; treeTops?: number[];
53	    created: number; playTimeMs: number;
54	    wldVersion?: number;
55	  };
56	  clock: { timeOfDay: number; dayCount: number };
57	  tiles: string;   // base64 RLE
58	  walls: string;
59	  liquid: string;
60	  liquidType: string;  // base64 RLE（0无 1水 2岩浆 3蜂蜜）
61	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>;
62	  player: {
63	    hp: number; x: number; y: number;
64	    inventory: Array<{ id: number; stack: number } | null>;
65	    selected: number;
66	  };
67	  npcs: Array<{ key: string; x: number; y: number; home: [number, number] | null }>;
68	  flags: Record<string, boolean>;
69	}
70	
71	export function rlePairs(values: ArrayLike<number>): number[] {
72	  const out: number[] = [];
73	  const n = values.length;
74	  let i = 0;
75	  while (i < n) {
76	    const v = values[i];
77	    let run = 1;
78	    while (i + run < n && values[i + run] === v && run < 0x7fffffff) run++;
79	    writeVarint(out, run - 1);
80	    writeVarint(out, v);
81	    i += run;
82	  }
83	  return out;
84	}
85	
86	export function rleTiles(st: { type: Uint16Array; frameX: Uint16Array; frameY: Uint16Array }): number[] {
87	  const out: number[] = [];
88	  const n = st.type.length;
89	  let i = 0;
90	  while (i < n) {
91	    const t = st.type[i], fx = st.frameX[i], fy = st.frameY[i];
92	    let run = 1;
93	    while (i + run < n && st.type[i + run] === t && st.frameX[i + run] === fx && st.frameY[i + run] === fy) run++;
94	    writeVarint(out, run - 1);
95	    writeVarint(out, t);
96	    if (t !== 0) {
97	      writeVarint(out, fx);
98	      writeVarint(out, fy);
99	    }
100	    i += run;
101	  }
102	  return out;
103	}
104	
105	export function saveGame(world: World, player: Player, playTimeMs: number): string {
106	  const st = world.store;
107	  // 幽灵净化:存档格式不携带 active 位(加载时 type≠0 即激活),
108	  // 非活性格上的残留 type 必须归零,否则重读后全部变成浮空实体块
109	  for (let i = 0; i < st.type.length; i++) {
110	    if (!st.flags[i] && st.type[i] !== 0) st.type[i] = 0;
111	  }
112	  const data: SaveData = {
113	    format: 'sandboxworld.save',
114	    version: 2,
115	    header: {
116	      name: world.name, seed: world.seed, width: st.w, height: st.h,
117	      spawn: [world.spawnX, world.spawnY], groundLevel: world.groundLevel, rockLevel: world.rockLevel,
118	      treeX: world.treeX, treeStyle: world.treeStyle,
119	      crimson: world.crimson, dungeonX: world.dungeonX, jungleX: world.jungleX,
120	      created: Date.now(), playTimeMs,
121	    },
122	    clock: { timeOfDay: world.clock.timeOfDay, dayCount: world.clock.dayCount },
123	    tiles: bytesToB64(rleTiles(st)),
124	    walls: bytesToB64(rlePairs(st.wall)),
125	    liquid: bytesToB64(rlePairs(st.liquid)),
126	    liquidType: bytesToB64(rlePairs(st.liquidType)),
127	    chests: world.chests,
128	    player: {
129	      hp: player.hp, x: player.x, y: player.y,
130	      inventory: player.inv.slots, selected: player.inv.selected,
131	    },
132	    npcs: [],
133	    flags: world.flags,
134	  };
135	  return JSON.stringify(data);
136	}
137	
138	export function loadSave(json: string): { world: World; player: { hp: number; x: number; y: number; inventory: Array<{ id: number; stack: number } | null>; selected: number } } {
139	  const data = JSON.parse(json) as SaveData;
140	  const world = new WorldClass(data.header.width, data.header.height, data.header.seed, data.header.name);
141	  world.spawnX = data.header.spawn[0];
142	  world.spawnY = data.header.spawn[1];
143	  world.groundLevel = data.header.groundLevel;
144	  world.rockLevel = data.header.rockLevel;
145	  if (data.header.treeX) world.treeX = data.header.treeX;
146	  if (data.header.treeStyle) world.treeStyle = data.header.treeStyle;
147	  if (data.header.treeTops?.length) world.treeTops = data.header.treeTops;
148	  if (data.header.crimson !== undefined) world.crimson = data.header.crimson;
149	  if (data.header.dungeonX !== undefined) world.dungeonX = data.header.dungeonX;
150	  if (data.header.jungleX !== undefined) world.jungleX = data.header.jungleX;
151	  world.clock.timeOfDay = data.clock.timeOfDay;
152	  world.clock.dayCount = data.clock.dayCount;
153	  world.chests = data.chests;
154	  world.flags = data.flags;
155	
156	  const st = world.store;
157	  // tiles
158	  {
159	    const u8 = b64ToBytes(data.tiles);
160	    const pos = { i: 0 };
161	    let i = 0;
162	    while (i < st.type.length && pos.i < u8.length) {
163	      const run = readVarint(u8, pos) + 1;
164	      const t = readVarint(u8, pos);
165	      let fx = 0, fy = 0;
166	      if (t !== 0) {
167	        fx = readVarint(u8, pos);
168	        fy = readVarint(u8, pos);
169	      }
170	      for (let k = 0; k < run && i < st.type.length; k++, i++) {
171	        st.type[i] = t; st.flags[i] = t !== 0 ? 1 : 0;
172	        st.frameX[i] = fx; st.frameY[i] = fy;
173	      }
174	    }
175	  }
176	  // walls（version<2 的旧档墙值迁移：1=土→2, 2=石→1, 3=木→4（现为原版 id））
177	  {
178	    const legacy = (data.version ?? 1) < 2;
179	    const migrate = (v: number) => (legacy ? (v === 1 ? 2 : v === 2 ? 1 : v === 3 ? 4 : v) : v);
180	    const u8 = b64ToBytes(data.walls);
181	    const pos = { i: 0 };
182	    let i = 0;
183	    while (i < st.wall.length && pos.i < u8.length) {
184	      const run = readVarint(u8, pos) + 1;
185	      const v = migrate(readVarint(u8, pos));
186	      for (let k = 0; k < run && i < st.wall.length; k++, i++) st.wall[i] = v;
187	    }
188	  }
189	  // liquid type（旧存档缺此字段 → 全 0，由液体模拟按 1=水 补全）
190	  {
191	    const u8 = b64ToBytes(data.liquidType ?? '');
192	    const pos = { i: 0 };
193	    let i = 0;
194	    while (i < st.liquidType.length && pos.i < u8.length) {
195	      const run = readVarint(u8, pos) + 1;
196	      const v = readVarint(u8, pos);
197	      for (let k = 0; k < run && i < st.liquidType.length; k++, i++) st.liquidType[i] = v;
198	    }
199	  }
200	  // liquid
201	  {
202	    const u8 = b64ToBytes(data.liquid);
203	    const pos = { i: 0 };
204	    let i = 0;
205	    while (i < st.liquid.length && pos.i < u8.length) {
206	      const run = readVarint(u8, pos) + 1;
207	      const v = readVarint(u8, pos);
208	      for (let k = 0; k < run && i < st.liquid.length; k++, i++) st.liquid[i] = v;
209	    }
210	  }
211	  return { world, player: data.player };
212	}
213	

```


---

## 🤖 Assistant · 2026-08-09T09:09:30.108Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read WorldGen.ts, World.ts, recipes.ts, KvStore.ts. Also SpriteAtlas.ts, index.html, package.json.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:30.109Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts",
 "limit": 160
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:30.113Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/World.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:30.121Z

**📎 ToolResult**

```
1	// 世界门面：TileStore + 元数据 + 实体容器 + 昼夜时钟
2	import { TileStore } from './TileStore';
3	import { T, TILE_DEFS } from '../data/tiles';
4	
5	export interface ChestData { x: number; y: number; items: Array<{ id: number; stack: number } | null>; locked?: boolean; }
6	
7	export class Clock {
8	  timeOfDay: number = 0.3;   // 0-1，0=午夜 0.5=正午（起始上午 7:12 ≈ 0.3）
9	  dayCount: number = 1;
10	  readonly dayLengthMs: number;
11	  constructor(dayLengthMs: number) { this.dayLengthMs = dayLengthMs; }
12	  tick(dtMs: number) {
13	    this.timeOfDay += dtMs / this.dayLengthMs;
14	    while (this.timeOfDay >= 1) { this.timeOfDay -= 1; this.dayCount++; }
15	  }
16	  get isDay(): boolean { return this.timeOfDay > 0.25 && this.timeOfDay < 0.75; }
17	  get dayFactor(): number {
18	    // 昼夜平滑系数：白天 1，夜晚 0.32（月光下地表仍可见，火把不再像贴在黑幕上），晨昏过渡
19	    const t = this.timeOfDay;
20	    if (t > 0.28 && t < 0.72) return 1;
21	    if (t >= 0.72 && t < 0.80) return 1 - (t - 0.72) / 0.08 * 0.68;
22	    if (t >= 0.80 || t < 0.20) return 0.32;
23	    return 0.32 + (t - 0.20) / 0.08 * 0.68;
24	  }
25	  get hourFloat(): number { return this.timeOfDay * 24; }
26	}
27	
28	export class World {
29	  store: TileStore;
30	  name: string;
31	  seed: number;
32	  spawnX = 0; spawnY = 0;
33	  groundLevel = 0; rockLevel = 0;   // tile 坐标
34	  clock: Clock;
35	  chests: ChestData[] = [];
36	  // Boss 进度旗标
37	  flags: Record<string, boolean> = { downedEyeOfCthulhu: false, shadowOrbSmashed: false };
38	  // 树登记：砍树干时找到整棵树（roots → 范围）
39	  trees: Array<{ x: number; y: number; h: number }> = [];
40	  /** 战争迷雾：1 = 已探索。按 tile 粒度。 */
41	  explored: Uint8Array;
42	  /** 原版树样式数据（header treeX/treeStyle）：横向 4 区森林树冠样式 */
43	  treeX: number[] = [];
44	  treeStyle: number[] = [0, 0, 0, 0];
45	  /** 世界级生物群系常量(原版 header,生成期 Reset pass 掷出) */
46	  crimson = false;          // true=猩红 false=腐化
47	  dungeonX = 0;            // 地牢位置
48	  jungleX = 0;             // 丛林位置
49	  /** TreeTops 13 区域变体（v≥211 wld 权威；索引 0-3 森林/5 丛林/6 雪/7 神圣） */
50	  treeTops: number[] = [];
51	
52	  exploredVersion = 0;
53	  markExplored(cx: number, cy: number, radius: number) {
54	    this.exploredVersion++;
55	    const st = this.store;
56	    const x0 = Math.max(0, cx - radius), x1 = Math.min(st.w - 1, cx + radius);
57	    const y0 = Math.max(0, cy - radius), y1 = Math.min(st.h - 1, cy + radius);
58	    for (let y = y0; y <= y1; y++) {
59	      for (let x = x0; x <= x1; x++) {
60	        if ((x - cx) ** 2 + (y - cy) ** 2 <= radius * radius) {
61	          this.explored[y * st.w + x] = 1;
62	        }
63	      }
64	    }
65	  }
66	
67	  constructor(w: number, h: number, seed: number, name = '新世界') {
68	    this.store = new TileStore(w, h);
69	    this.explored = new Uint8Array(w * h);
70	    this.seed = seed;
71	    this.name = name;
72	    // 1 游戏日 = 30 现实分钟（24→40 后折中）
73	    this.clock = new Clock(30 * 60 * 1000);
74	  }
75	
76	  get w() { return this.store.w; }
77	  get h() { return this.store.h; }
78	  get tiles() { return this.store; }
79	
80	  /** 破坏一个 tile（含 framed 物体的锚点处理由调用方负责），返回掉落 item key */
81	  breakTileAt(x: number, y: number): string | null {
82	    const t = this.store.get(x, y);
83	    if (t === 0) return null;
84	    const d = TILE_DEFS[t];
85	    this.store.setTile(x, y, 0);
86	    // v_ 图块无显式 drop → 回退同名放置物品(阶段5 自动注册)
87	    return d.drop ?? (d.key.startsWith('v_') ? 'place_' + d.key : null);
88	  }
89	
90	  isSolidPx(px: number, py: number): boolean {
91	    return this.store.isSolid(Math.floor(px / 16), Math.floor(py / 16));
92	  }
93	
94	  /** 液体量（0-255）按像素坐标 */
95	  liquidAt(px: number, py: number): number {
96	    return this.store.liquid[this.store.idx(Math.floor(px / 16), Math.floor(py / 16))];
97	  }
98	
99	  registerTree(x: number, y: number, h: number) {
100	    this.trees.push({ x, y, h });
101	  }
102	}
103	
104	export { T };
105	

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:30.123Z

**📎 ToolResult**

```
1	// 程序化世界生成管线：地形 → 洞穴 → 矿石 → 液体 → 表面 → 结构
2	// 分帧执行以显示进度。纯函数式 pass，每个 pass 直接写 TileStore（生成期用 silent 写入）。
3	import { createNoise2D } from 'simplex-noise';
4	import { RNG, hashString } from '../../core/rng';
5	import { T, W, TILE_DEFS, TILE_BY_KEY } from '../../data/tiles';
6	import { World } from '../World';
7	
8	export interface GenConfig {
9	  width: number;
10	  height: number;
11	  seedText: string;
12	  name?: string;
13	  structures?: boolean;
14	}
15	
16	export interface Pass {
17	  name: string;
18	  run: (ctx: GenCtx, report: (p: number) => void) => void;
19	}
20	
21	export interface GenCtx {
22	  world: World;
23	  store: World['store'];
24	  rng: RNG;
25	  noise2D: (x: number, y: number) => number;
26	  surface: Float32Array;   // 每列地表高度（tile y）
27	  cfg: GenConfig;
28	}
29	
30	/** 生成一个世界。passes 按序执行，每帧尽量做完一个 pass 后让出主线程。 */
31	export async function generateWorld(cfg: GenConfig, onProgress?: (label: string, p: number) => void): Promise<World> {
32	  const seed = hashString(cfg.seedText || String(Date.now()));
33	  const world = new World(cfg.width, cfg.height, seed, cfg.name ?? '新世界');
34	  const rng = new RNG(seed);
35	  const noise2D = createNoise2D(() => rng.next());
36	  const ctx: GenCtx = {
37	    world, store: world.store, rng, noise2D,
38	    surface: new Float32Array(cfg.width),
39	    cfg,
40	  };
41	
42	  // 原版管线:TerrainPass(五特征随机走) + TileRunner 泥石/洞穴;其余 pass 沿用
43	  // (lgcTerrain=false 走旧 fbm 地形作为回退开关)
44	  const useVanillaTerrain = (cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain !== false;
45	  const passes: Pass[] = [
46	    ...(useVanillaTerrain ? [
47	      { name: '原版地形', run: vanillaTerrain },
48	      { name: '洞穴', run: vanillaCaves },
49	      { name: '海滩', run: vanillaBeaches },
50	      { name: '生物群系', run: vanillaBiomes },
51	      { name: '清理', run: vanillaCleanup },
52	      { name: '生命水晶', run: vanillaLifeCrystals },
53	    ] as Pass[] : [
54	      { name: '地形', run: terrainPass },
55	      { name: '洞穴', run: cavePass },
56	    ]),
57	    { name: '矿石', run: orePass },
58	    { name: '液体', run: liquidPass },
59	    ...(useVanillaTerrain ? [
60	      // 原版 "Smooth World"(L7568)+"Waterfalls"(L7697)：地表凸起与水边唇缘砸半砖
61	      // （半砖 = 原版水浸润/瀑布触发的核心，见 HalfBrickPass.ts）
62	      { name: '半砖平滑', run: halfBrickSmoothPass },
63	      { name: '瀑布唇缘', run: waterfallLipPass },
64	    ] as Pass[] : []),
65	    { name: '地狱', run: hellPass },
66	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [{ name: '清浮空', run: floatCleanupPass }] : []),
67	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地狱屋', run: vanillaHellHouses }]),
68	    { name: '瓦罐', run: potPass },
69	    { name: '表面', run: surfacePass },
70	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地表装饰', run: vanillaSurfaceDecor }]),
71	    ...(cfg.structures === false ? [] : [{ name: '结构', run: structurePass }]),
72	  ];
73	
74	  for (let i = 0; i < passes.length; i++) {
75	    onProgress?.(passes[i].name, i / passes.length);
76	    await nextFrame();
77	    passes[i].run(ctx, () => {});
78	  }
79	
80	  finalize(ctx);
81	  onProgress?.('完成', 1);
82	  return world;
83	}
84	
85	// ---------- 原版管线 pass(阶段 1-2 移植) ----------
86	import { newGenState, type GenState } from './vanilla/GenState';
87	import { runTerrainPass } from './vanilla/TerrainPass';
88	import { runRocksAndClayPass, runCavesPass } from './vanilla/CavesPass';
89	import { runOceanSandPass, runBeachesPass } from './vanilla/BeachPass';
90	import { runIceBiomePass } from './vanilla/IceBiomePass';
91	import { runGrassPass } from './vanilla/GrassPass';
92	import { runJunglePass } from './vanilla/JunglePass';
93	import { spreadGrassAll } from './vanilla/Spread';
94	import { runDesertPass } from './vanilla/DesertPass';
95	import { runMushroomPass } from './vanilla/MushroomPass';
96	import { runMarbleGranitePass } from './vanilla/MarbleGranitePass';
97	import { runDirtToMudAndSiltPass } from './vanilla/DirtToMudPass';
98	import { runCleanupPass } from './vanilla/CleanupPass';
99	import { runSmoothWorldPass, runWaterfallLipPass } from './vanilla/HalfBrickPass';
100	import { runFloatingIslandsPass, runLifeCrystalsPass, runSurfaceDecorPass, runPyramidPass, runWetJunglePass } from './vanilla/StructuresPass';
101	import { runBeehivePass, runSpiderNestPass } from './vanilla/HiveSpiderPass';
102	import { tileRunner } from './vanilla/TileRunner';
103	import { runDungeonPass } from './vanilla/DungeonPass';
104	import { runTemplePass } from './vanilla/TemplePass';
105	import { runIslandHousePass } from './vanilla/IslandHousePass';
106	import { runHellFortPass } from './vanilla/HellFortPass';
107	import { runSwordShrinePass } from './vanilla/SwordShrinePass';
108	import { runCorruptionPass } from './vanilla/CorruptionPass';
109	
110	function vanillaTerrain({ store, rng, world, surface }: GenCtx) {
111	  const gs = newGenState(store.w, store.h);
112	  // Reset pass 掷骰(WorldGen.cs L4780-4880,掷骰顺序 = RNG 契约不可调换)
113	  // 矿石替代对:Next(2)==0 → 替代矿(内部 id)
114	  gs.oreTiers = {
115	    copper: rng.next() < 0.5 ? TILE_BY_KEY['ore_tin']! : TILE_BY_KEY['ore_copper']!,
116	    iron: rng.next() < 0.5 ? TILE_BY_KEY['ore_lead']! : TILE_BY_KEY['ore_iron']!,
117	    silver: rng.next() < 0.5 ? TILE_BY_KEY['ore_tungsten']! : TILE_BY_KEY['ore_silver']!,
118	    gold: rng.next() < 0.5 ? TILE_BY_KEY['ore_platinum']! : TILE_BY_KEY['ore_gold']!,
119	  };
120	  gs.crimson = rng.next() < 0.5;
121	  world.crimson = gs.crimson;
122	  gs.dungeonSide = rng.next() < 0.5 ? -1 : 1;
123	  // 丛林:与地牢异侧(Next(15,30) 即 15-29)
124	  const jf = rng.int(15, 29) * 0.01;
125	  gs.jungleX = Math.floor(store.w * (gs.dungeonSide === -1 ? 1 - jf : jf));
126	  world.jungleX = gs.jungleX;
127	  // 地牢 X:拒绝采样直到落在地牢侧 15% 区间
128	  let dX = rng.int(0, store.w - 1);
129	  const dLo = store.w * (gs.dungeonSide === 1 ? 0.60 : 0.25);
130	  const dHi = store.w * (gs.dungeonSide === 1 ? 0.75 : 0.40);
131	  while (dX < dLo || dX > dHi) dX = rng.int(0, store.w - 1);
132	  gs.dungeonX = dX;
133	  // 雪原:以地牢 X 为中心向两侧扩展(L4863-4879)——原版雪原与地牢同侧
134	  const snowScale = store.w / 4200;
135	  const snowExtend = () => rng.int(50, 89) + Math.floor(rng.int(20, 39) * snowScale) + Math.floor(rng.int(20, 39) * snowScale);
136	  gs.snowOriginLeft = Math.max(0, dX - snowExtend());
137	  gs.snowOriginRight = Math.min(store.w, dX + snowExtend());
138	  // 海滩宽度(原版固定 300-340+档位加成,按 4200 宽设计;小世界线性缩放保持比例)
139	  const beachRoll = () => Math.max(20, Math.floor(rng.int(300, 339) * snowScale));
140	  gs.beachLeftEnd = beachRoll() + (gs.dungeonSide === 1 ? 40 : 20) * (snowScale >= 1 ? 1 : Math.max(0.3, snowScale));
141	  gs.beachRightStart = store.w - beachRoll() - (gs.dungeonSide === -1 ? 40 : 20) * (snowScale >= 1 ? 1 : Math.max(0.3, snowScale));
142	  // 地牢入口(L4891-4894):地牢侧海滩内 15% 区间随机
143	  if (gs.dungeonSide === -1) {
144	    gs.dungeonLocation = rng.int(gs.beachLeftEnd + 50, Math.floor(store.w * 0.2));
145	  } else {
146	    gs.dungeonLocation = rng.int(Math.floor(store.w * 0.8), gs.beachRightStart - 50);
147	  }
148	  world.dungeonX = gs.dungeonLocation;
149	  // Terrain pass
150	  runTerrainPass(store, rng, gs);
151	  // surface 数组给后续旧 pass(surfacePass 树木等)用:每列首个实心行
152	  for (let x = 0; x < store.w; x++) {
153	    for (let y = 0; y < store.h; y++) {
154	      if (store.flags[store.idx(x, y)]) { surface[x] = y; break; }
155	    }
156	  }
157	  ctxGs[0] = gs;
158	  // 世界级常量同步
159	  world.groundLevel = gs.worldSurface;
160	  world.rockLevel = gs.rockLevel;

```


---

## 🤖 Assistant · 2026-08-09T09:09:32.366Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now assets: SpriteAtlas.ts (loading paths, fonts), index.html, package.json, KvStore.ts, recipes.ts. Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:32.368Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts",
 "limit": 260
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:32.372Z

**📎 ToolResult**

```
1	// Unity 素材图集运行时加载器
2	// 数据由 scripts/build-atlas.mjs 生成（public/sprites/atlas.json + resources.json）
3	// 原版素材由 scripts/vanilla-atlas.mjs 生成（public/sprites/vanilla.json，独立命名空间、无 Unity y 翻转）
4	// 注意：Unity 精灵 rect 的 y 轴原点在【左下】，Canvas 在【左上】，取用时要翻转。
5	import atlasJson from '../../public/sprites/atlas.json';
6	import resourcesJson from '../../public/sprites/resources.json';
7	import vanillaJson from '../../public/sprites/vanilla.json';
8	import vanillaNpcsJson from '../../public/sprites/vanilla-npcs.json';
9	
10	/** npc id → 动画帧数（SetDefaults 提取数据派生；懒加载 NPC 表用） */
11	const vanillaNpcFrames: Record<string, number> = Object.fromEntries(
12	  Object.entries(vanillaNpcsJson as Record<string, { frames?: number }>).map(([k, v]) => [k, v.frames ?? 1]),
13	);
14	
15	export interface SpriteRect { name: string; x: number; y: number; w: number; h: number; }
16	export interface SpriteRef { file: string; sprite: string; }
17	export interface RuleDef {
18	  id: number;
19	  sprites: SpriteRef[];
20	  neighbors: number[];
21	  positions: Array<[number, number]>;
22	  transform: number;
23	  output: number;
24	}
25	export interface RuleTileDef { defaultSprite: SpriteRef | null; tilingRules: RuleDef[]; }
26	
27	export interface AtlasFile { guid: string; sprites: SpriteRect[]; idToName: Record<string, string>; }
28	export interface AtlasData {
29	  files: Record<string, AtlasFile>;
30	  guidToFile: Record<string, string>;
31	}
32	export interface ResourcesData {
33	  items: Array<{ name: string; type: string; iconGuid: string | null; placeTile: string | null; funcList: string }>;
34	  tiles: Array<{ name: string; tileGuid: string; layer: string; digList: string; digTime: string; dropItemGuid: string }>;
35	  potions: Array<{ name: string; type: string; iconGuid: string | null; buffType: number | null; duration: number | null; isHealType: string }>;
36	  accessories: Array<{ name: string; type: string; iconGuid: string | null }>;
37	  buffs: Array<{ name: string; iconGuid: string | null }>;
38	  anims: Record<string, SpriteRef[]>;
39	  rules: Record<string, RuleTileDef>;
40	}
41	
42	export interface DrawRect { img: HTMLImageElement | HTMLCanvasElement; sx: number; sy: number; sw: number; sh: number; }
43	
44	// ---- 原版素材命名空间（vanilla.json，TEdit 数据驱动） ----
45	
46	// 杂项单图素材（非表驱动，直接整图使用）
47	// 树木专用：Tree_Tops/Branches（树冠树枝，TEdit style 0-10）+ Tiles_5_N（生物群系树干）
48	export const VANILLA_MISC = [
49	  'vanilla/Bubble.png',
50	  ...Array.from({ length: 32 }, (_, i) => `vanilla/Tree_Tops_${i}.png`),
51	  ...Array.from({ length: 32 }, (_, i) => `vanilla/Tree_Branches_${i}.png`),
52	  ...Array.from({ length: 7 }, (_, i) => `vanilla/Tiles_5_${i}.png`),
53	  'vanilla/Evil_Cactus.png', 'vanilla/Good_Cactus.png', 'vanilla/Crimson_Cactus.png',
54	  'vanilla/Liquid_0.png', 'vanilla/Liquid_1.png', 'vanilla/Liquid_11.png', 'vanilla/Liquid_14.png',
55	  'vanilla/Misc_water_0.png', 'vanilla/Misc_water_1.png', 'vanilla/Misc_water_11.png',
56	  'vanilla/Waterfall_0.png', 'vanilla/Waterfall_1.png', 'vanilla/Waterfall_14.png',
57	  'vanilla/Shroom_Tops.png',
58	];
59	export interface VanillaTileMeta {
60	  name: string; key: string; sheet: string;
61	  solid: boolean; blend: boolean; framed: boolean; light: boolean;
62	  color: string; placement: string | null;
63	  grid: [number, number];      // 帧像素尺寸（蜡烛类 [16,20]）
64	  stride: [number, number];    // 表内帧步长（grid+gap，如 [18,18]）
65	  frameSize: Array<[number, number]>; // 每个 style 的占格数
66	  cols: number; rows: number;
67	  isStone?: boolean; isGrass?: boolean; mergeWith?: number | null;
68	}
69	export interface VanillaItemMeta { name: string; key: string; icon: string; createTile: number | null; }
70	export interface VanillaWallMeta {
71	  name: string; key: string; sheet: string; color: string;
72	  grid: [number, number]; stride: [number, number]; cols: number; rows: number;
73	  largeFrame?: number;
74	}
75	// NPC 贴图表（纵向帧条：小动物等）
76	export interface VanillaNpcMeta { sheet: string; frameW: number; frameH: number; count: number; }
77	export interface VanillaData {
78	  tiles: Record<string, VanillaTileMeta>;
79	  items: Record<string, VanillaItemMeta>;
80	  walls: Record<string, VanillaWallMeta>;
81	  npcs?: Record<string, VanillaNpcMeta>;
82	  tileNames?: Record<string, string>;  // 全量原版 tile id → 英文名（兼容报告用）
83	  itemNames?: Record<string, string>;
84	}
85	
86	/** 整图硬 alpha：alpha ≥128 → 255，<128 → 0（并清零 RGB），消除提取 PNG 的半透明镶边 */
87	function hardAlpha(img: HTMLImageElement): HTMLCanvasElement {
88	  const c = document.createElement('canvas');
89	  c.width = img.width; c.height = img.height;
90	  const ctx = c.getContext('2d')!;
91	  ctx.drawImage(img, 0, 0);
92	  const d = ctx.getImageData(0, 0, c.width, c.height);
93	  const px = d.data;
94	  for (let i = 0; i < px.length; i += 4) {
95	    if (px[i + 3] >= 128) px[i + 3] = 255;
96	    else {
97	      px[i] = 0; px[i + 1] = 0; px[i + 2] = 0; px[i + 3] = 0;
98	    }
99	  }
100	  ctx.putImageData(d, 0, 0);
101	  return c;
102	}
103	
104	export class SpriteAtlas {
105	  data = atlasJson as unknown as AtlasData;
106	  resources = resourcesJson as unknown as ResourcesData;
107	  vanilla = vanillaJson as unknown as VanillaData;
108	  images = new Map<string, HTMLImageElement | HTMLCanvasElement>();
109	  vimages = new Map<string, HTMLImageElement>(); // 原版 PNG（干净像素，不做 hardAlpha）
110	  /** 人工标注（annotator.html 导出）：sheet → spriteName → 方位标签 */
111	  annotations: Record<string, Record<string, string>> = {};
112	
113	  async load(onProgress?: (p: number) => void): Promise<void> {
114	    const files = Object.keys(this.data.files);
115	    const vfiles = [
116	      ...Object.values(this.vanilla.tiles).map((t) => t.sheet),
117	      ...Object.values(this.vanilla.items).map((i) => i.icon),
118	      ...Object.values(this.vanilla.walls).map((w) => w.sheet),
119	      ...Object.values(this.vanilla.npcs ?? {}).map((n) => n.sheet),
120	      ...VANILLA_MISC, // 杂项单图（呼吸气泡等）
121	    ];
122	    let done = 0;
123	    const total = files.length + vfiles.length;
124	    await Promise.all([
125	      ...files.map((f) => new Promise<void>((resolve) => {
126	        const img = new Image();
127	        img.onload = () => {
128	          // 根源处理：整图硬 alpha —— 抗锯齿半透明像素（提取 PNG 的灰/黑镶边来源）
129	          // 二值化为 0/255，所有消费方（tile/墙/图标/角色）统一获得干净像素
130	          this.images.set(f, hardAlpha(img));
131	          done++;
132	          onProgress?.(done / total);
133	          resolve();
134	        };
135	        img.onerror = () => resolve();
136	        img.src = `sprites/${encodeURI(f)}`;
137	      })),
138	      // 原版素材：并行加载，失败跳过（vframe/vicon 返回 null 兜底）
139	      ...vfiles.map((f) => new Promise<void>((resolve) => {
140	        const img = new Image();
141	        img.onload = () => { this.vimages.set(f, img); done++; onProgress?.(done / total); resolve(); };
142	        img.onerror = () => resolve();
143	        img.src = `sprites/${encodeURI(f)}`;
144	      })),
145	    ]);
146	    // 人工标注（可选，缺失时回退）
147	    try {
148	      const r = await fetch('sprites/annotations.json');
149	      if (r.ok) this.annotations = await r.json();
150	    } catch { /* 无标注 */ }
151	  }
152	
153	  // ---- 原版素材 API（无 Unity y 翻转，按 TEdit 网格寻址） ----
154	
155	  /** 原版图块元数据 */
156	  vmeta(sheetId: number): VanillaTileMeta | null {
157	    return this.vanilla.tiles[String(sheetId)] ?? null;
158	  }
159	
160	  /** 原版图块表取帧（col,row 从 0 起）。越界/缺失返回 null */
161	  vframe(sheetId: number, col: number, row: number): DrawRect | null {
162	    const m = this.vmeta(sheetId);
163	    if (!m) return null;
164	    const img = this.vimages.get(m.sheet);
165	    if (!img) return null;
166	    if (col < 0 || row < 0 || col >= m.cols || row >= m.rows) return null;
167	    return { img, sx: col * m.stride[0], sy: row * m.stride[1], sw: m.grid[0], sh: m.grid[1] };
168	  }
169	
170	  /** 原版表内任意像素偏移取帧（style/显式帧：18px 步长的 frameX/frameY 直用） */
171	  vframeAt(sheetId: number, fx: number, fy: number): DrawRect | null {
172	    const m = this.vmeta(sheetId);
173	    if (!m) return null;
174	    const img = this.vimages.get(m.sheet);
175	    if (!img) return null;
176	    if (fx < 0 || fy < 0 || fx + m.grid[0] > img.width || fy + m.grid[1] > img.height) return null;
177	    return { img, sx: fx, sy: fy, sw: m.grid[0], sh: m.grid[1] };
178	  }
179	
180	  /** 原版表内任意矩形（多格物体整体取图，如墓碑 2×2 = 34×34px） */
181	  vrect(sheetId: number, fx: number, fy: number, w: number, h: number): DrawRect | null {
182	    const m = this.vmeta(sheetId);
183	    if (!m) return null;
184	    const img = this.vimages.get(m.sheet);
185	    if (!img) return null;
186	    if (fx < 0 || fy < 0 || fx + w > img.width || fy + h > img.height) return null;
187	    return { img, sx: fx, sy: fy, sw: w, sh: h };
188	  }
189	
190	  /** 原版 NPC 贴图表取帧（纵向帧条，frameIdx 0-based）。
191	   *  未登记的 id 懒加载 vanilla/NPC_{id}.png（帧数来自 vanilla-npcs.json），首帧返回 null 下一帧生效 */
192	  private lazyNpcMeta = new Map<string, VanillaNpcMeta>();
193	  vnpc(npcId: number, frameIdx: number): DrawRect | null {
194	    let m: VanillaNpcMeta | undefined = this.vanilla.npcs?.[String(npcId)];
195	    if (!m) {
196	      const key = String(npcId);
197	      m = this.lazyNpcMeta.get(key);
198	      if (!m) {
199	        const sheet = `vanilla/NPC_${npcId}.png`;
200	        const img = this.vimages.get(sheet);
201	        if (!img) {
202	          const im = new Image();
203	          im.onload = () => this.vimages.set(sheet, im);
204	          im.src = `sprites/${sheet}`;
205	          return null;
206	        }
207	        const frames = (vanillaNpcFrames as Record<string, number>)[key] ?? 1;
208	        const fh = Math.max(1, Math.floor(img.height / frames));
209	        const meta: VanillaNpcMeta = { sheet, frameW: img.width, frameH: fh, count: frames };
210	        this.lazyNpcMeta.set(key, meta);
211	        m = meta;
212	      }
213	    }
214	    const img = this.vimages.get(m.sheet);
215	    if (!img) return null;
216	    const idx = Math.max(0, Math.min(m.count - 1, frameIdx));
217	    return { img, sx: 0, sy: idx * m.frameH, sw: m.frameW, sh: m.frameH };
218	  }
219	
220	  /** 原版 tile/item 英文名（全量表，未白名单的也有） */
221	  vTileName(id: number): string | null { return this.vanilla.tileNames?.[String(id)] ?? null; }
222	  vItemName(id: number): string | null { return this.vanilla.itemNames?.[String(id)] ?? null; }
223	
224	  vnpcMeta(npcId: number): VanillaNpcMeta | null {
225	    return this.vanilla.npcs?.[String(npcId)] ?? null;
226	  }
227	
228	  /** 原版杂项单图（呼吸气泡等） */
229	  vmisc(path: string): DrawRect | null {
230	    const img = this.vimages.get(path);
231	    if (!img) return null;
232	    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
233	  }
234	
235	  /** 原版物品图标（整图） */
236	  vicon(itemId: number): DrawRect | null {
237	    const m = this.vanilla.items[String(itemId)];
238	    if (!m) return null;
239	    const img = this.vimages.get(m.icon);
240	    if (!img) return null;
241	    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
242	  }
243	
244	  has(file: string): boolean {
245	    return this.images.has(file);
246	  }
247	
248	  /** 取精灵绘制矩形（Unity y 翻转已处理）。找不到返回 null。 */
249	  rect(file: string, sprite: string): DrawRect | null {
250	    const img = this.images.get(file);
251	    const entry = this.data.files[file];
252	    if (!img || !entry) return null;
253	    const s = entry.sprites.find((x) => x.name === sprite);
254	    if (!s) return null;
255	    return { img, sx: s.x, sy: img.height - s.y - s.h, sw: s.w, sh: s.h };
256	  }
257	
258	  /** 按资源名取整图（物品/Buff 图标等单图资源） */
259	  byGuid(guid: string | null | undefined): DrawRect | null {
260	    if (!guid) return null;

```


---

## 🤖 Assistant · 2026-08-09T09:09:32.561Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cat ~/Project/GLM/SandboxWorld/game/index.html ~/Project/GLM/SandboxWorld/game/package.json ~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts",
 "description": "Show index.html, package.json, KvStore.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:32.596Z

**📎 ToolResult**

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><rect width='16' height='10' y='6' fill='%23976B4B'/><rect width='16' height='4' y='2' fill='%233E9E42'/></svg>" />
  <title>SandboxWorld</title>
  <style>
    html, body {
      margin: 0; padding: 0; width: 100%; height: 100%;
      overflow: hidden; background: #000;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      user-select: none;
    }
    #game-root { position: fixed; inset: 0; }
    canvas { display: block; image-rendering: pixelated; }
  </style>
</head>
<body>
  <div id="game-root"></div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
{
  "name": "sandboxworld",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "start": "vite build && vite preview"
  },
  "dependencies": {
    "simplex-noise": "^4.0.3"
  },
  "devDependencies": {
    "@types/node": "^26.1.2",
    "typescript": "^5.6.0",
    "vite": "^5.4.0",
    "vitest": "^2.1.0"
  }
}
// 键值存储：优先 IndexedDB（容量数百 MB+，大地图存档不受 localStorage ~5MB 限制），
// localStorage 作为小存档缓存与回退。async API，调用方 await。
const DB_NAME = 'sandboxworld';
const STORE = 'kv';
let dbPromise: Promise<IDBDatabase> | null = null;

function openDb(): Promise<IDBDatabase> {
  if (dbPromise) return dbPromise;
  dbPromise = new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = () => {
      if (!req.result.objectStoreNames.contains(STORE)) req.result.createObjectStore(STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
  return dbPromise;
}

/** 是否有某 key（IndexedDB 或 localStorage） */
export async function kvHas(key: string): Promise<boolean> {
  if (localStorage.getItem(key) !== null) return true;
  try {
    const db = await openDb();
    return await new Promise<boolean>((resolve) => {
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).getKey(key);
      req.onsuccess = () => resolve(req.result !== undefined);
      req.onerror = () => resolve(false);
    });
  } catch {
    return false;
  }
}

/** 读取（IndexedDB 优先——大存档只进 IDB，localStorage 可能留着旧的小存档；
   读取顺序必须与写入优先级一致，否则会读到过期档） */
export async function kvGet(key: string): Promise<string | null> {
  try {
    const db = await openDb();
    const idbVal = await new Promise<string | null>((resolve) => {
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).get(key);
      req.onsuccess = () => resolve(typeof req.result === 'string' ? req.result : null);
      req.onerror = () => resolve(null);
    });
    if (idbVal !== null) return idbVal;
  } catch { /* IDB 不可用 → 回退 localStorage */ }
  return localStorage.getItem(key);
}

/** 写入：字符串 ≤ 2MB 进 localStorage（快速路径），否则只进 IndexedDB */
export async function kvSet(key: string, value: string): Promise<'local' | 'idb' | 'fail'> {
  if (value.length <= 2 * 1024 * 1024) {
    try {
      localStorage.setItem(key, value);
      return 'local';
    } catch { /* 超限或被禁 → 落 IndexedDB */ }
  }
  try {
    const db = await openDb();
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite');
      tx.objectStore(STORE).put(value, key);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
    return 'idb';
  } catch {
    return 'fail';
  }
}

```


---

## 🤖 Assistant · 2026-08-09T09:09:35.129Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at: Renderer.ts (Canvas 2D? render method, minimap), recipes.ts, atlasIconForKey, ItemIconGen, docs, fonts handling, i18n/l10n tools, camera zoom/scale, and the 封面 (cover) sprites directory — possibly a title background. Also check shots/ for screenshots. And check the tools/l10n directory for i18n.

Let me check several things in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:35.929Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"getContext\\|canvas.width\\|devicePixelRatio\\|zoom\\|imageSmoothing\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -40; echo ----; grep -n \"class\\|attach\\|render(\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -40",
 "description": "Inspect Renderer for canvas setup and classes"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:35.983Z

**📎 ToolResult**

```
31:    this.canvas.width = world.w;
33:    this.ctx = this.canvas.getContext('2d')!;
111:  // 全屏地图查看器状态（zoom 向 zoomTarget 缓动；缓动期间按锚点补偿 pan）
113:    open: false, zoom: 0.5, zoomTarget: 0.5, panX: 0, panY: 0,
118:  zoomFullMapAt(newZoom: number, mouseX: number, mouseY: number) {
120:    const viewW = this.canvas.width, viewH = this.canvas.height;
123:    // 缓动期间每帧按公式 pan = anchorMX - viewW/2 + W*zoom/2 - u*zoom 重解，
125:    const cx0 = viewW / 2 - (this._fmWorldW * fm.zoom) / 2 + fm.panX;
126:    const cy0 = viewH / 2 - (this._fmWorldH * fm.zoom) / 2 + fm.panY;
127:    fm.anchorU = (mouseX - cx0) / fm.zoom;
128:    fm.anchorV = (mouseY - cy0) / fm.zoom;
131:    fm.zoomTarget = clamped;
135:  /** 按锚点反解 pan（当前 zoom 下鼠标处的地图点固定在鼠标下） */
138:    const viewW = this.canvas.width, viewH = this.canvas.height;
139:    fm.panX = fm.anchorMX - viewW / 2 + (this._fmWorldW * fm.zoom) / 2 - fm.anchorU * fm.zoom;
140:    fm.panY = fm.anchorMY - viewH / 2 + (this._fmWorldH * fm.zoom) / 2 - fm.anchorV * fm.zoom;
143:  /** 每帧缓动 fullMap.zoom → zoomTarget；缓动期间同步按锚点补偿 pan */
146:    const diff = fm.zoomTarget - fm.zoom;
147:    if (Math.abs(diff) < 0.002) { fm.zoom = fm.zoomTarget; return; }
148:    fm.zoom += diff * 0.16;
159:    this.ctx = this.canvas.getContext('2d')!;
161:    this.lightCtx = this.lightCanvas.getContext('2d')!;
180:    this.canvas.width = window.innerWidth;
211:    const viewW = this.canvas.width, viewH = this.canvas.height;
213:    const z = cam.zoom;
221:    ctx.imageSmoothingEnabled = false;
339:      const z = cam.zoom;
408:      const cx = c.getContext('2d')!;
632:      const frame = spr.canvas.width > fw ? Math.floor(e.animT / 12) % (spr.canvas.width / fw) : 0;
918:      const cx = c.getContext('2d')!;
947:    const z = cam.zoom;
999:    ctx.imageSmoothingEnabled = true;
1012:    const ox = ctx.canvas.width - size - pad, oy = pad;
1030:    ctx.imageSmoothingEnabled = false;
1071:    const fc = this.fogCanvas.getContext('2d')!;
1105:    ctx.imageSmoothingEnabled = false;
1128:    const viewW = ctx.canvas.width, viewH = ctx.canvas.height;
1140:        const viewW = ctx.canvas.width, viewH = ctx.canvas.height;
1141:        fm.anchorU = (mouseX - (viewW / 2 - (this._fmWorldW * fm.zoom) / 2 + fm.panX)) / fm.zoom;
1142:        fm.anchorV = (mouseY - (viewH / 2 - (this._fmWorldH * fm.zoom) / 2 + fm.panY)) / fm.zoom;
----
25:export class Minimap {
97:export class Renderer {
184:  attach(parent: HTMLElement) {
192:  render(

```


---

## 🤖 Assistant · 2026-08-09T09:09:36.431Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cat ~/Project/GLM/SandboxWorld/game/src/data/recipes.ts; echo ====; ls ~/Project/GLM/SandboxWorld/game/docs ~/Project/GLM/SandboxWorld/game/docs/vanilla-algos ~/Project/GLM/SandboxWorld/game/shots 2>/dev/null | head -60",
 "description": "Show recipes and docs listing"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:36.470Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
// 配方表。station: 'hand' | 'workbench' | 'furnace' | 'anvil'
export type Station = 'hand' | 'workbench' | 'furnace' | 'anvil';

export interface Recipe {
  out: string;          // 产物 item key
  count: number;
  station: Station;
  inputs: Array<[string, number]>; // [itemKey, 数量]
}

export const RECIPES: Recipe[] = [
  { out: 'workbench', count: 1, station: 'hand', inputs: [['wood', 10]] },
  { out: 'torch', count: 3, station: 'hand', inputs: [['wood', 1], ['gel', 1]] },
  { out: 'platform', count: 2, station: 'workbench', inputs: [['wood', 1]] },
  { out: 'door', count: 1, station: 'workbench', inputs: [['wood', 6]] },
  { out: 'chest', count: 1, station: 'workbench', inputs: [['wood', 8], ['iron_bar', 2]] },
  { out: 'furnace', count: 1, station: 'workbench', inputs: [['stone_block', 20], ['wood', 4], ['torch', 3]] },
  { out: 'wood_pickaxe', count: 1, station: 'workbench', inputs: [['wood', 12]] },
  { out: 'wood_axe', count: 1, station: 'workbench', inputs: [['wood', 9]] },
  { out: 'wood_sword', count: 1, station: 'workbench', inputs: [['wood', 7]] },
  // 熔炼
  { out: 'copper_bar', count: 1, station: 'furnace', inputs: [['copper_ore', 3]] },
  { out: 'iron_bar', count: 1, station: 'furnace', inputs: [['iron_ore', 3]] },
  { out: 'silver_bar', count: 1, station: 'furnace', inputs: [['silver_ore', 4]] },
  { out: 'gold_bar', count: 1, station: 'furnace', inputs: [['gold_ore', 4]] },
  { out: 'anvil', count: 1, station: 'workbench', inputs: [['iron_bar', 5]] },
  // 金属工具链
  { out: 'copper_pickaxe', count: 1, station: 'anvil', inputs: [['copper_bar', 8], ['wood', 3]] },
  { out: 'copper_axe', count: 1, station: 'anvil', inputs: [['copper_bar', 6], ['wood', 3]] },
  { out: 'copper_sword', count: 1, station: 'anvil', inputs: [['copper_bar', 7]] },
  { out: 'iron_pickaxe', count: 1, station: 'anvil', inputs: [['iron_bar', 8], ['wood', 3]] },
  { out: 'iron_axe', count: 1, station: 'anvil', inputs: [['iron_bar', 6], ['wood', 3]] },
  { out: 'iron_sword', count: 1, station: 'anvil', inputs: [['iron_bar', 7]] },
  { out: 'wood_hammer', count: 1, station: 'workbench', inputs: [['wood', 8]] },
  { out: 'iron_hammer', count: 1, station: 'anvil', inputs: [['iron_bar', 6], ['wood', 3]] },
  { out: 'silver_pickaxe', count: 1, station: 'anvil', inputs: [['silver_bar', 8], ['wood', 3]] },
  { out: 'silver_sword', count: 1, station: 'anvil', inputs: [['silver_bar', 7]] },
  { out: 'gold_pickaxe', count: 1, station: 'anvil', inputs: [['gold_bar', 8], ['wood', 3]] },
  { out: 'gold_sword', count: 1, station: 'anvil', inputs: [['gold_bar', 7]] },
  // 盔甲（铁砧）
  { out: 'copper_helmet', count: 1, station: 'anvil', inputs: [['copper_bar', 15]] },
  { out: 'copper_chainmail', count: 1, station: 'anvil', inputs: [['copper_bar', 20]] },
  { out: 'copper_greaves', count: 1, station: 'anvil', inputs: [['copper_bar', 15]] },
  { out: 'iron_helmet', count: 1, station: 'anvil', inputs: [['iron_bar', 20]] },
  { out: 'iron_chainmail', count: 1, station: 'anvil', inputs: [['iron_bar', 25]] },
  { out: 'iron_greaves', count: 1, station: 'anvil', inputs: [['iron_bar', 20]] },
  { out: 'silver_helmet', count: 1, station: 'anvil', inputs: [['silver_bar', 15]] },
  { out: 'silver_chainmail', count: 1, station: 'anvil', inputs: [['silver_bar', 20]] },
  { out: 'silver_greaves', count: 1, station: 'anvil', inputs: [['silver_bar', 15]] },
  { out: 'gold_helmet', count: 1, station: 'anvil', inputs: [['gold_bar', 10]] },
  { out: 'gold_chainmail', count: 1, station: 'anvil', inputs: [['gold_bar', 15]] },
  { out: 'gold_greaves', count: 1, station: 'anvil', inputs: [['gold_bar', 10]] },
  // 杂项
  { out: 'suspicious_eye', count: 1, station: 'workbench', inputs: [['lens', 6]] },
  { out: 'lesser_healing_potion', count: 1, station: 'workbench', inputs: [['gel', 2], ['mushroom_item', 1]] },
  // 药水链（移植自 Maples 合成表 + 扩展）
  { out: 'heal_potion', count: 1, station: 'workbench', inputs: [['lesser_healing_potion', 2], ['gel', 1]] },
  { out: 'regen_potion', count: 1, station: 'workbench', inputs: [['gel', 2], ['mushroom_item', 2]] },
  { out: 'agility_potion', count: 1, station: 'workbench', inputs: [['mushroom_item', 1], ['iron_bar', 1]] },
  { out: 'ironskin_potion', count: 1, station: 'workbench', inputs: [['stone_block', 5], ['iron_bar', 1]] },
  { out: 'thorns_potion', count: 1, station: 'workbench', inputs: [['wood', 5], ['lens', 1]] },
  // ---- 原版素材批次：方块 / 家具 / 熔炼 ----
  // 替代矿熔炼
  { out: 'tin_bar', count: 1, station: 'furnace', inputs: [['tin_ore', 3]] },
  { out: 'lead_bar', count: 1, station: 'furnace', inputs: [['lead_ore', 3]] },
  { out: 'tungsten_bar', count: 1, station: 'furnace', inputs: [['tungsten_ore', 4]] },
  { out: 'platinum_bar', count: 1, station: 'furnace', inputs: [['platinum_ore', 4]] },
  // 方块加工
  { out: 'glass', count: 1, station: 'furnace', inputs: [['sand_block', 2]] },
  { out: 'gray_brick', count: 2, station: 'furnace', inputs: [['stone_block', 2]] },
  { out: 'red_brick', count: 2, station: 'furnace', inputs: [['clay_block', 2]] },
  { out: 'sandstone_block', count: 1, station: 'furnace', inputs: [['sand_block', 4]] },
  { out: 'ice_brick', count: 1, station: 'furnace', inputs: [['ice_block', 1]] },
  { out: 'snow_brick', count: 1, station: 'furnace', inputs: [['snow_block', 1]] },
  // 家具
  { out: 'table', count: 1, station: 'workbench', inputs: [['wood', 8]] },
  { out: 'chair', count: 1, station: 'workbench', inputs: [['wood', 4]] },
  { out: 'bed', count: 1, station: 'workbench', inputs: [['wood', 15]] },
  { out: 'bookcase', count: 1, station: 'workbench', inputs: [['wood', 20]] },
  { out: 'grandfather_clock', count: 1, station: 'workbench', inputs: [['wood', 10], ['iron_bar', 3]] },
  { out: 'piano', count: 1, station: 'workbench', inputs: [['wood', 15], ['iron_bar', 2]] },
  { out: 'dresser', count: 1, station: 'workbench', inputs: [['wood', 12]] },
  { out: 'bench', count: 1, station: 'workbench', inputs: [['wood', 8]] },
  { out: 'bathtub', count: 1, station: 'workbench', inputs: [['clay_block', 6]] },
  { out: 'keg', count: 1, station: 'workbench', inputs: [['wood', 14]] },
  { out: 'cooking_pot', count: 1, station: 'workbench', inputs: [['iron_bar', 2], ['wood', 4]] },
  { out: 'clay_pot', count: 1, station: 'workbench', inputs: [['clay_block', 5]] },
  { out: 'tombstone', count: 1, station: 'workbench', inputs: [['stone_block', 5]] },
  // 灯具
  { out: 'candle', count: 4, station: 'workbench', inputs: [['torch', 1], ['gel', 1]] },
  { out: 'chandelier', count: 1, station: 'anvil', inputs: [['torch', 4], ['iron_bar', 3]] },
  { out: 'lantern', count: 1, station: 'anvil', inputs: [['torch', 1], ['iron_bar', 1]] },
  { out: 'candelabra', count: 1, station: 'anvil', inputs: [['torch', 3], ['iron_bar', 1]] },
  { out: 'chinese_lantern', count: 1, station: 'workbench', inputs: [['torch', 1], ['wood', 3]] },
  { out: 'skull_lantern', count: 1, station: 'anvil', inputs: [['torch', 2], ['iron_bar', 1]] },

// ---- 阶段 6:替代矿熔炼与工具链(与主矿同档配方) ----
  { out: 'tungsten_bar', count: 1, station: 'furnace', inputs: [['tungsten_ore', 4]] },
  { out: 'platinum_bar', count: 1, station: 'furnace', inputs: [['platinum_ore', 4]] },
  { out: 'tin_pickaxe', count: 1, station: 'anvil', inputs: [['tin_bar', 8], ['wood', 3]] },
  { out: 'tin_axe', count: 1, station: 'anvil', inputs: [['tin_bar', 6], ['wood', 3]] },
  { out: 'tin_sword', count: 1, station: 'anvil', inputs: [['tin_bar', 7]] },
  { out: 'lead_pickaxe', count: 1, station: 'anvil', inputs: [['lead_bar', 8], ['wood', 3]] },
  { out: 'lead_axe', count: 1, station: 'anvil', inputs: [['lead_bar', 6], ['wood', 3]] },
  { out: 'lead_sword', count: 1, station: 'anvil', inputs: [['lead_bar', 7]] },
  { out: 'tungsten_pickaxe', count: 1, station: 'anvil', inputs: [['tungsten_bar', 8], ['wood', 3]] },
  { out: 'tungsten_axe', count: 1, station: 'anvil', inputs: [['tungsten_bar', 6], ['wood', 3]] },
  { out: 'tungsten_sword', count: 1, station: 'anvil', inputs: [['tungsten_bar', 7]] },
  { out: 'platinum_pickaxe', count: 1, station: 'anvil', inputs: [['platinum_bar', 8], ['wood', 3]] },
  { out: 'platinum_axe', count: 1, station: 'anvil', inputs: [['platinum_bar', 6], ['wood', 3]] },
  { out: 'platinum_sword', count: 1, station: 'anvil', inputs: [['platinum_bar', 7]] },
];
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-09T09:09:38.600Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `====` was interpreted; whatever. Let me check docs, shots, fonts, i18n/l10n, and Renderer details (attach, render, minimap, camera zoom defaults), Camera.ts, and atlasIconForKey in SpriteAtlas. Also 封面 sprites (cover). And check the tools/l10n.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:39.379Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/docs ~/Project/GLM/SandboxWorld/game/docs/vanilla-algos 2>/dev/null; ls ~/Project/GLM/SandboxWorld/game/shots | head; ls ~/Project/GLM/SandboxWorld/tools/l10n | head; ls \"~/Project/GLM/SandboxWorld/game/public/sprites/封面\" 2>/dev/null | head; ls ~/Project/GLM/SandboxWorld/game/public/sprites | head -30",
 "description": "List docs, shots, l10n tools, sprites dirs"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:39.411Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/docs:
vanilla-algos

~/Project/GLM/SandboxWorld/game/docs/vanilla-algos:
dungeon.md
hive-temple-spider.md
island-house-hellfort-chasm-sword.md
01-spawn.png
02-walk.png
03-jump.png
04-later.png
10-wld-import.png
20-maples-tiles.png
30-black-check.png
40-feet-check.png
de-DE.Game.json
de-DE.Items.json
de-DE.json
de-DE.Legacy.json
de-DE.NPCs.json
de-DE.Projectiles.json
de-DE.Town.json
en-US.Game.json
en-US.Items.json
en-US.json
Logo3.png
MapBG1.png
Splash_6_0.png
Splash_9_0.png
annotations.json
atlas.json
resources.json
UI
vanilla
vanilla-npcloot.json
vanilla-npcs.json
vanilla.json
地形
封面
角色

```


---

## 🤖 Assistant · 2026-08-09T09:09:40.226Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 240,360p ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts; echo ----CAMERA----; cat ~/Project/GLM/SandboxWorld/game/src/render/Camera.ts; echo ----FONT----; grep -rn \"font\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -20",
 "description": "Show atlasIconForKey, Camera, font usage"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:40.259Z

**📎 ToolResult**

```
    if (!img) return null;
    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
  }

  has(file: string): boolean {
    return this.images.has(file);
  }

  /** 取精灵绘制矩形（Unity y 翻转已处理）。找不到返回 null。 */
  rect(file: string, sprite: string): DrawRect | null {
    const img = this.images.get(file);
    const entry = this.data.files[file];
    if (!img || !entry) return null;
    const s = entry.sprites.find((x) => x.name === sprite);
    if (!s) return null;
    return { img, sx: s.x, sy: img.height - s.y - s.h, sw: s.w, sh: s.h };
  }

  /** 按资源名取整图（物品/Buff 图标等单图资源） */
  byGuid(guid: string | null | undefined): DrawRect | null {
    if (!guid) return null;
    const file = this.data.guidToFile[guid];
    if (!file) return null;
    const img = this.images.get(file);
    if (!img) return null;
    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
  }

  animFrames(anim: string): DrawRect[] {
    const frames = this.resources.anims[anim] ?? [];
    return frames.map((f) => this.rect(f.file, f.sprite)).filter(Boolean) as DrawRect[];
  }
}

// ---- 资源名（resources.json 的 name 字段是 \uXXXX 转义，JSON.parse 已还原）----
export function itemIconByType(atlas: SpriteAtlas, typeNum: number): DrawRect | null {
  const it = atlas.resources.items.find((x) => Number(x.type) === typeNum);
  return atlas.byGuid(it?.iconGuid ?? null);
}

export function findItem(atlas: SpriteAtlas, name: string) {
  return atlas.resources.items.find((x) => x.name === name);
}

// 我们的 item key → Maples 物品资源名（图标替换表）
export const ITEM_ICON_MAP: Record<string, string> = {
  dirt_block: '泥土', stone_block: '石头', wood: '木材', torch: '火把',
  workbench: '工作台', furnace: '熔炉', anvil: '铁砧',
  iron_sword: '铁剑', iron_pickaxe: '铁镐', iron_axe: '铁斧', iron_ore: '铁矿', iron_bar: '铁锭',
  heal_potion: '治疗药水', agility_potion: '敏捷药水', ironskin_potion: '铁皮药水',
  thorns_potion: '荆棘药水', regen_potion: '恢复药水',
  lucky_horseshoe: '幸运马掌', feral_claws: '猛爪手套',
};

// 特殊手动映射（无 .asset 登记的图标）
const ITEM_DIRECT_MAP: Record<string, { file: string; sprite: string }> = {};

/** 按我们的 item key 取 Maples 图标矩形（搜索 items + potions + accessories 三个来源）。
 *  Maples 没有的回退原版 Item_N 图标（第二查找层，id 实读自 TEdit items.json） */
import { TILE_BY_KEY, TILE_DEFS } from '../data/tiles';

export function atlasIconForKey(atlas: SpriteAtlas, key: string): DrawRect | null {
  const direct = ITEM_DIRECT_MAP[key];
  if (direct) return atlas.rect(direct.file, direct.sprite);
  const resName = ITEM_ICON_MAP[key];
  if (resName) {
    const r = atlas.resources;
    const res =
      r.items.find((x) => x.name === resName) ??
      (r.potions ?? []).find((x) => x.name === resName) ??
      (r.accessories ?? []).find((x) => x.name === resName);
    const m = atlas.byGuid(res?.iconGuid ?? null);
    if (m) return m;
  }
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
      if (td?.vanilla) return atlas.vframe(td.vanilla.sheet, 0, 0);
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
----CAMERA----
// 相机：跟随玩家 + 缓动 + 世界边界钳制
import { TILE } from '../core/constants';

export class Camera {
  x = 0; y = 0;         // 视野中心（世界 px）
  zoom = 1.25;          // 当前缩放（向 targetZoom 缓动）
  zoomTarget = 1.25;    // 目标缩放
  static ZOOM_MIN = 0.75;
  static ZOOM_MAX = 2.5;
  /** 每帧把 zoom 向 target 缓动（指数趋近，永不到达导致卡死） */
  easeZoom() {
    const diff = this.zoomTarget - this.zoom;
    if (Math.abs(diff) < 0.0005) { this.zoom = this.zoomTarget; return; }
    this.zoom += diff * 0.18;
  }
  setZoomTarget(z: number) {
    this.zoomTarget = Math.max(Camera.ZOOM_MIN, Math.min(Camera.ZOOM_MAX, z));
  }
  viewW = 800; viewH = 600; // 屏幕尺寸

  constructor(public worldW: number, public worldH: number) {}

  follow(targetX: number, targetY: number) {
    this.x += (targetX - this.x) * 0.15;
    this.y += (targetY - this.y) * 0.15;
  }

  clamp() {
    const halfW = this.viewW / 2 / this.zoom;
    const halfH = this.viewH / 2 / this.zoom;
    this.x = Math.max(halfW, Math.min(this.worldW * TILE - halfW, this.x));
    this.y = Math.max(halfH, Math.min(this.worldH * TILE - halfH, this.y));
    // 世界比视野小的情况
    if (this.worldW * TILE < halfW * 2) this.x = this.worldW * TILE / 2;
    if (this.worldH * TILE < halfH * 2) this.y = this.worldH * TILE / 2;
  }

  worldToScreen(wx: number, wy: number): [number, number] {
    return [(wx - this.x) * this.zoom + this.viewW / 2, (wy - this.y) * this.zoom + this.viewH / 2];
  }
  screenToWorld(sx: number, sy: number): [number, number] {
    return [(sx - this.viewW / 2) / this.zoom + this.x, (sy - this.viewH / 2) / this.zoom + this.y];
  }
  tileUnder(sx: number, sy: number): [number, number] {
    const [wx, wy] = this.screenToWorld(sx, sy);
    return [Math.floor(wx / TILE), Math.floor(wy / TILE)];
  }
}
----FONT----
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:303:    ctx.font = 'bold 14px monospace';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:310:        ctx.font = '13px sans-serif';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:319:      ctx.font = d.crit ? 'bold 18px monospace' : 'bold 14px monospace';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:341:      ctx.font = `bold ${Math.max(10, 12 * z)}px monospace`;
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:706:      ctx.font = '12px sans-serif';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1047:    ctx.font = 'bold 14px monospace';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1200:    ctx.font = '13px sans-serif';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1244:    ctx.font = 'bold 13px sans-serif';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1275:        ctx.font = '10px monospace';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1302:        ctx.font = '10px monospace';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1336:    ctx.font = '12px monospace';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1361:    ctx.font = 'bold 13px sans-serif';

```


---

## 🤖 Assistant · 2026-08-09T09:09:46.648Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The l10n dir listing got merged into the docs listing. Let me re-check: it printed docs listing (3 md files), then shots listing (01-spawn.png etc), then tools/l10n listing? Actually the output ordering: docs has vanilla-algos (3 md). Then shots: 01-spawn.png ... 10-wld-import.png, 20-maples-tiles.png, 30-black-check.png, 40-feet-check.png. Then tools/l10n: de-DE.Game.json, de-DE.Items.json, ... en-US.Game.json... Then 封面: Logo3.png, MapBG1.png, Splash_6_0.png, Splash_9_0.png? Then sprites root: annotations.json, atlas.json, resources.json, UI, vanilla, vanilla-npcloot.json, vanilla-npcs.json, vanilla.json, 地形, 封面, 角色.

So tools/l10n has de-DE and en-US translation files (Terraria localization JSON extracted from game). Note there's no zh-Hans in l10n? Let me check for zh. Also check whether any code references l10n.

Also need: Renderer HUD drawing (hearts, hotbar is DOM, minimap), how rendering handles zoom, and check whether there's a title screen background. Also check the worldgen progress callback mapping already exists (yes, onProgress with label+p).

Also check: is there any character creation? Player has no name/appearance fields. Check character rendering: CharacterSheetGen, and how player is drawn (hair color etc.). Let me grep for 'hair' and 'skin' in render.

Also check i18n: grep for "zh" or "lang" or "i18n" in src.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:47.278Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/tools/l10n; echo ----; grep -rniE \"i18n|locale|zh-Hans|zh_CN|translation|Lang\\b\" ~/Project/GLM/SandboxWorld/game/src | head -20; echo ----HAIR----; grep -rniE \"hair|skin|eyeColor|shirt|pants\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts -l | head",
 "description": "Check l10n files and character appearance code"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:47.284Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 150,300p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Read Renderer attach/render/HUD section"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:47.300Z

**📎 ToolResult**

```
  }
  private _fmWorldW = 0;
  private _fmWorldH = 0;
  minimapRect = { x: 0, y: 0, w: 0, h: 0 };
  private mapDragging = false;
  private lastMouse = { x: 0, y: 0 };

  constructor(public assets: AssetBundle, public atlas: SpriteAtlas | null = null) {
    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d')!;
    this.lightCanvas = document.createElement('canvas');
    this.lightCtx = this.lightCanvas.getContext('2d')!;
    window.addEventListener('resize', () => this.resize());
    this.resize();
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

  render(
    cam: Camera, world: World, clock: Clock,
    chunks: ChunkCache,
    lightR: Uint8Array, lightG: Uint8Array, lightB: Uint8Array,
    lightRX: number, lightRY: number, lightRW: number, lightRH: number,
    player: Player, entities: Entity[],
    particles: Particle[], dmgNumbers: DamageNumber[],
    swing: { t: number; dur: number; item: number } | null,
    hover: { x: number; y: number } | null,
    boss: { name: string; hp: number; maxHp: number } | null,
    mouseX = 0, mouseY = 0, mouseDown = false,
    mineProgress = 0,
  ) {
    this._mouseX = mouseX;
    this._mouseY = mouseY;
    this._mouseDown = mouseDown;
    this._liquidNow = performance.now(); // 帧 first thing 采样：背景水/瀑布/前景水共用同一时刻
    this.easeFullMap();
    const ctx = this.ctx;
    const viewW = this.canvas.width, viewH = this.canvas.height;
    cam.viewW = viewW; cam.viewH = viewH;
    const z = cam.zoom;

    // 1. 天空
    this.sky.draw(ctx, clock, viewW, viewH, cam.x);

    ctx.save();
    // 世界变换：平移 + 缩放（以屏幕中心为相机中心）
    // 像素风关键：tile/实体用最近邻采样保持锐利（光照层单独用平滑）
    ctx.imageSmoothingEnabled = false;
    ctx.translate(viewW / 2, viewH / 2);
    ctx.scale(z, z);
    ctx.translate(-cam.x, -cam.y);

    // 2. chunks 绘制序列（对照原版 Main.cs 帧序：背景水 → 墙 → 方块 → 瀑布 → 实体 → 前景水）
    const ts = TILE;
    const x0 = Math.floor((cam.x - viewW / 2 / z) / (CHUNK * ts)) - 1;
    const x1 = Math.floor((cam.x + viewW / 2 / z) / (CHUNK * ts)) + 1;
    const y0 = Math.floor((cam.y - viewH / 2 / z) / (CHUNK * ts)) - 1;
    const y1 = Math.floor((cam.y + viewH / 2 / z) / (CHUNK * ts)) + 1;
    const chunkVisible = (cx: number, cy: number) =>
      cx >= 0 && cy >= 0 && cx * CHUNK < world.w && cy * CHUNK < world.h;
    // 2a. 液体背景 pass（原版 backWaterTarget 先于墙合成，Main.cs:46619）：
    //     不透明水画在墙/方块之前——方块贴图透明像素处露出这层水 = 浸润，
    //     有墙的水格由墙盖住、只留前景 0.6 层 → 墙在水中可见
    this.drawLiquids(world, cam, viewW, viewH, z, true);

    // 2b. 背景墙层
    for (let cy = y0; cy <= y1; cy++) {
      for (let cx = x0; cx <= x1; cx++) {
        if (!chunkVisible(cx, cy)) continue;
        ctx.drawImage(chunks.get(cx, cy).wall, cx * CHUNK * ts, cy * CHUNK * ts);
      }
    }

    // 2c. 前景 tile/物体层
    for (let cy = y0; cy <= y1; cy++) {
      for (let cx = x0; cx <= x1; cx++) {
        if (!chunkVisible(cx, cy)) continue;
        ctx.drawImage(chunks.get(cx, cy).tile, cx * CHUNK * ts, cy * CHUNK * ts);
      }
    }

    // 2d. 瀑布贴图（原版画在 tile 层后、实体前，Main.cs:47460，被地形遮挡）
    this.drawWaterfalls(world, cam, viewW, viewH, z);

    // 4. 实体（按 y 排序）
    const sorted = [...entities].sort((a, b) => a.y - b.y);
    for (const e of sorted) {
      if (e instanceof Enemy) this.drawEnemy(e, world);
      else if (e instanceof ItemDrop) this.drawDrop(e);
      else if (e instanceof TownNPC) this.drawTownNPC(e);
      else if (e instanceof Tombstone) this.drawTombstone(e);
      else if (e instanceof Critter) this.drawCritter(e);
      else (e as Player).draw && null;
    }
    this.drawPlayer(player, world, swing);

    // 4.5 液体前景 pass（原版 waterTarget 在玩家/掉落物之后合成，Main.cs:46720）：
    //     水 0.6 半透明盖在实体上——水中角色带水色
    this.drawLiquids(world, cam, viewW, viewH, z, false);

    // 5. 粒子
    for (const p of particles) {
      ctx.globalAlpha = Math.max(0, p.life / p.maxLife);
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
    }
    ctx.globalAlpha = 1;

    // 6. 挖掘/放置光标：挖掘中黄色填充随进度加深（半透明黄 → 破坏完成时最深）
    if (hover) {
      ctx.strokeStyle = 'rgba(255,255,255,0.7)';
      ctx.lineWidth = 1 / z;
      ctx.strokeRect(hover.x * ts + 0.5, hover.y * ts + 0.5, ts - 1, ts - 1);
      if (mineProgress > 0) {
        // 进度 0→1，黄色 alpha 0.15→0.8 加深渐变（接近破坏时深黄）
        ctx.globalAlpha = 0.15 + Math.min(1, mineProgress) * 0.65;
        ctx.fillStyle = '#FFC419';
        ctx.fillRect(hover.x * ts + 1, hover.y * ts + 1, ts - 2, ts - 2);
        ctx.globalAlpha = 1;
      }
    }

    ctx.restore();

    // 7. 光照合成
    this.compositeLight(cam, viewW, viewH, lightR, lightG, lightB, lightRX, lightRY, lightRW, lightRH);

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:47.305Z

**📎 ToolResult**

```
de-DE.Game.json
de-DE.Items.json
de-DE.json
de-DE.Legacy.json
de-DE.NPCs.json
de-DE.Projectiles.json
de-DE.Town.json
en-US.Game.json
en-US.Items.json
en-US.json
en-US.Legacy.json
en-US.NPCs.json
en-US.Projectiles.json
en-US.Town.json
es-ES.Game.json
es-ES.Items.json
es-ES.json
es-ES.Legacy.json
es-ES.NPCs.json
es-ES.Projectiles.json
es-ES.Town.json
fr-FR.Game.json
fr-FR.Items.json
fr-FR.json
fr-FR.Legacy.json
fr-FR.NPCs.json
fr-FR.Projectiles.json
fr-FR.Town.json
it-IT.Game.json
it-IT.Items.json
it-IT.json
it-IT.Legacy.json
it-IT.NPCs.json
it-IT.Projectiles.json
it-IT.Town.json
ja-JP.Game.json
ja-JP.Items.json
ja-JP.json
ja-JP.Legacy.json
ja-JP.NPCs.json
ja-JP.Projectiles.json
ja-JP.Town.json
ko-KR.Game.json
ko-KR.Items.json
ko-KR.json
ko-KR.Legacy.json
ko-KR.NPCs.json
ko-KR.Projectiles.json
ko-KR.Town.json
pl-PL.Game.json
pl-PL.Items.json
pl-PL.json
pl-PL.Legacy.json
pl-PL.NPCs.json
pl-PL.Projectiles.json
pl-PL.Town.json
pt-BR.Game.json
pt-BR.Items.json
pt-BR.json
pt-BR.Legacy.json
pt-BR.NPCs.json
pt-BR.Projectiles.json
pt-BR.Town.json
ru-RU.Game.json
ru-RU.Items.json
ru-RU.json
ru-RU.Legacy.json
ru-RU.NPCs.json
ru-RU.Projectiles.json
ru-RU.Town.json
zh-Hans.Game.json
zh-Hans.Items.json
zh-Hans.json
zh-Hans.Legacy.json
zh-Hans.NPCs.json
zh-Hans.Projectiles.json
zh-Hans.Town.json
zh-Hant.Game.json
zh-Hant.Items.json
zh-Hant.json
zh-Hant.Legacy.json
zh-Hant.NPCs.json
zh-Hant.Projectiles.json
zh-Hant.Town.json
----
----HAIR----
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-09T09:09:51.530Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. There's zh-Hans localization files in tools/l10n (extracted from Terraria). But no i18n code in src.

Now check how the player is drawn (CharacterSheetGen, character sprites 角色 dir), and whether appearance customization exists. Also check the HUD drawing in Renderer (hearts/mana/breath/minimap) — lines 940-1100.

Also confirm: worldgen progress — the progress callback exists; map preview during generation doesn't. Minimap class uses world. Let me read Minimap + HUD part quickly, and CharacterSheetGen briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:51.532Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 1,96p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts; sed -n 940,1060p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Read Minimap class and HUD render code"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:51.557Z

**📎 ToolResult**

```
// 主渲染器：天空 → chunk → 液体 → 实体 → 粒子/飘字 → 光照合成 → 小地图
import { TILE, CHUNK } from '../core/constants';
import type { Camera } from './Camera';
import { SkyRenderer } from './SkyRenderer';
import { ChunkCache } from './ChunkCache';
import type { World, Clock } from '../world/World';
import type { AssetBundle } from '../assets/AssetGen';
import type { SpriteAtlas } from '../assets/SpriteAtlas';
import { atlasIconForKey } from '../assets/SpriteAtlas';
import { drawVanillaLiquids } from './VanillaLiquidRenderer';
import { WaterfallRenderer } from './WaterfallRenderer';
import { TILE_DEFS, WALL_DEFS } from '../data/tiles';
import { ITEM_DEFS } from '../data/items';
import type { Player } from '../entities/Player';
import { Enemy } from '../entities/Enemy';
import { ItemDrop } from '../entities/ItemDrop';
import { TownNPC } from '../entities/TownNPC';
import { Tombstone, getTombstoneCanvas } from '../entities/Tombstone';
import { Critter } from '../entities/Critter';
import type { Entity } from '../entities/Entity';

export interface Particle { x: number; y: number; vx: number; vy: number; life: number; maxLife: number; color: string; size: number; damp?: number; grav?: number; }
export interface DamageNumber { x: number; y: number; vy: number; value: number; crit: boolean; color: string; life: number; label?: string; }

export class Minimap {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  dirtyChunks = new Set<number>();
  constructor(public world: World) {
    this.canvas = document.createElement('canvas');
    this.canvas.width = world.w;
    this.canvas.height = world.h;
    this.ctx = this.canvas.getContext('2d')!;
    this.redrawAll();
    world.store.onTileChanged((x, y) => {
      this.dirtyChunks.add(ChunkCache.key(Math.floor(x / CHUNK), Math.floor(y / CHUNK)));
    });
  }

  colorFor(x: number, y: number): string | null {
    const st = this.world.store;
    const i = st.idx(x, y);
    if (st.type[i] !== 0) {
      const d = TILE_DEFS[st.type[i]];
      return d ? d.mapColor : '#808080';
    }
    // 液体：水蓝 / 岩浆橙
    if (st.liquid[i] > 40) return st.liquidType[i] === 2 ? '#E8622C' : '#3D6FD1';
    if (st.wall[i] !== 0) {
      // 墙色 = 深化（地下洞穴空气）
      const w = st.wall[i];
      return WALL_DEFS[w]?.mapColor ?? '#2E2E2E'; // 全量权威墙色（TEdit walls.json）
    }
    // 探索过的天空 = 亮蓝（未探索区域由迷雾层另盖黑）
    return '#7EB6E8';
  }

  redrawAll() {
    const { world, ctx } = this;
    const img = ctx.createImageData(world.w, world.h);
    for (let y = 0; y < world.h; y++) {
      for (let x = 0; x < world.w; x++) {
        const c = this.colorFor(x, y);
        const i = (y * world.w + x) * 4;
        if (c) {
          const v = parseInt(c.slice(1), 16);
          img.data[i] = (v >> 16) & 255; img.data[i + 1] = (v >> 8) & 255; img.data[i + 2] = v & 255;
        }
        img.data[i + 3] = 255;
      }
    }
    ctx.putImageData(img, 0, 0);
    this.dirtyChunks.clear();
  }

  flushDirty() {
    if (this.dirtyChunks.size === 0) return;
    const st = this.world.store;
    let n = 0;
    for (const k of this.dirtyChunks) {
      if (n++ > 24) break;
      this.dirtyChunks.delete(k);
      const cx = (k & 0xffff) << 16 >> 16, cy = (k >> 16) << 16 >> 16;
      const x0 = cx * CHUNK, y0 = cy * CHUNK;
      for (let y = y0; y < y0 + CHUNK; y++) {
        for (let x = x0; x < x0 + CHUNK; x++) {
          if (!st.inBounds(x, y)) continue;
          const c = this.colorFor(x, y);
          this.ctx.fillStyle = c ?? '#000';
          this.ctx.fillRect(x, y, 1, 1);
        }
      }
    }
  }
}


  private compositeLight(
    cam: Camera, viewW: number, viewH: number,
    lightR: Uint8Array, lightG: Uint8Array, lightB: Uint8Array,
    rx: number, ry: number, rw: number, rh: number,
  ) {
    if (this.fullbright) return; // 开灯：不做 multiply，全部原色
    const z = cam.zoom;
    const ts = TILE;
    const tilesX = Math.ceil(viewW / z / ts) + 2;
    const tilesY = Math.ceil(viewH / z / ts) + 2;
    const tx0 = Math.floor((cam.x - viewW / 2 / z) / ts);
    const ty0 = Math.floor((cam.y - viewH / 2 / z) / ts);
    // 2× 超采样：光照图每半格一个采样点，tile 中心间双线性插值，
    // 光斑梯度曲率更细腻（每格一采样时火把光斑有明显的马赛克棱面感）
    const SS = 2;
    const w2 = tilesX * SS, h2 = tilesY * SS;
    if (this.lightCanvas.width !== w2 || this.lightCanvas.height !== h2) {
      this.lightCanvas.width = w2;
      this.lightCanvas.height = h2;
    }
    const lc = this.lightCtx;
    const img = lc.createImageData(w2, h2);
    const lut = Renderer.lightLUT;
    // tile 中心光值采样（区域外 0，由环境光下限兜底）
    const tap = (gx: number, gy: number): [number, number, number] => {
      const tx = tx0 + gx, ty = ty0 + gy;
      if (tx >= rx && ty >= ry && tx < rx + rw && ty < ry + rh) {
        const li = (ty - ry) * rw + (tx - rx);
        return [lightR[li], lightG[li], lightB[li]];
      }
      return [0, 0, 0];
    };
    for (let py = 0; py < h2; py++) {
      const gy = py / SS - 0.5;              // 亚格坐标（tile 中心在整数处）
      const y0 = Math.floor(gy), fy = gy - y0;
      const wy0 = 1 - fy, wy1 = fy;
      for (let px = 0; px < w2; px++) {
        const gx = px / SS - 0.5;
        const x0 = Math.floor(gx), fx = gx - x0;
        const wx0 = 1 - fx, wx1 = fx;
        // 4 tap 双线性
        const a = tap(x0, y0), b = tap(x0 + 1, y0), c = tap(x0, y0 + 1), d = tap(x0 + 1, y0 + 1);
        const w00 = wx0 * wy0, w10 = wx1 * wy0, w01 = wx0 * wy1, w11 = wx1 * wy1;
        let r = a[0] * w00 + b[0] * w10 + c[0] * w01 + d[0] * w11;
        let g = a[1] * w00 + b[1] * w10 + c[1] * w01 + d[1] * w11;
        let b2 = a[2] * w00 + b[2] * w10 + c[2] * w01 + d[2] * w11;
        // gamma 柔化 + 最低可见度
        const amb = 10;
        const i = (py * w2 + px) * 4;
        img.data[i] = Math.max(lut[Math.min(255, Math.round(r))], amb);
        img.data[i + 1] = Math.max(lut[Math.min(255, Math.round(g))], amb);
        img.data[i + 2] = Math.max(lut[Math.min(255, Math.round(b2))], amb);
        img.data[i + 3] = 255;
      }
    }
    lc.putImageData(img, 0, 0);
    const ctx = this.ctx;
    ctx.save();
    ctx.imageSmoothingEnabled = true;
    ctx.globalCompositeOperation = 'multiply';
    const [sx, sy] = cam.worldToScreen(tx0 * ts, ty0 * ts);
    ctx.drawImage(this.lightCanvas, sx, sy, tilesX * ts * z, tilesY * ts * z);
    ctx.restore();
    ctx.globalCompositeOperation = 'source-over';
  }

  private drawMinimap(ctx: CanvasRenderingContext2D, cam: Camera, world: World, player: Player, clock: Clock) {
    if (!this.minimap) return;
    this.minimap.flushDirty();
    const size = 240;                 // 放大
    const pad = 12;
    const ox = ctx.canvas.width - size - pad, oy = pad;
    const viewTilesW = 220, viewTilesH = Math.floor(220 * world.h / world.w);
    const px = player.cx / TILE, py = player.cy / TILE;
    const sx = Math.max(0, Math.min(world.w - viewTilesW, Math.floor(px - viewTilesW / 2)));
    const sy = Math.max(0, Math.min(world.h - viewTilesH, Math.floor(py - viewTilesH / 2)));
    const mmH = size * viewTilesH / viewTilesW;
    ctx.save();
    // 边框
    ctx.strokeStyle = '#5A4A7A';
    ctx.lineWidth = 3;
    ctx.strokeRect(ox - 2, oy - 2, size + 4, mmH + 4);
    ctx.strokeStyle = 'rgba(0,0,0,0.5)';
    ctx.lineWidth = 1;
    ctx.strokeRect(ox - 4, oy - 4, size + 8, mmH + 8);
    // 底色：天空色（非黑）
    ctx.fillStyle = '#7EB6E8';
    ctx.fillRect(ox, oy, size, mmH);
    ctx.globalAlpha = 0.92;
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(this.minimap.canvas, sx, sy, viewTilesW, viewTilesH, ox, oy, size, mmH);
    ctx.globalAlpha = 1;
    // 迷雾（缩略图 1 tile = size/viewTilesW px；世界→屏幕偏移）
    this.drawFog(ctx, world,
      ox - sx * size / viewTilesW, oy - sy * mmH / viewTilesH,
      size / viewTilesW, 2 * size / viewTilesW,
      { x: ox, y: oy, w: size, h: mmH });
    // 玩家图标
    this.drawPlayerMarker(ctx,
      ox + (px - sx) / viewTilesW * size, oy + (py - sy) / viewTilesH * mmH, 10);
    // 记录小地图区域供点击检测
    this.minimapRect = { x: ox - 4, y: oy - 4, w: size + 8, h: mmH + 8 };
    // 时间显示
    const hFloat = clock.hourFloat;
    const hh = String(Math.floor(hFloat)).padStart(2, '0');
    const mm2 = String(Math.floor((hFloat % 1) * 60)).padStart(2, '0');
    ctx.font = 'bold 14px monospace';
    ctx.fillStyle = '#FFF';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 3;
    ctx.textAlign = 'center';
    const timeText = `\u65f6\u95f4 ${hh}:${mm2}`;
    ctx.strokeText(timeText, ox + size / 2, oy + mmH + 18);
    ctx.fillText(timeText, ox + size / 2, oy + mmH + 18);
    ctx.restore();
  }

  /** 迷雾遮罩：未探索区域黑色覆盖（世界坐标 → 目标矩形） */
  // 迷雾缓存：探索版本号变化时才重绘半分辨率画布（避免每帧百万格循环卡顿）
  private fogCanvas: HTMLCanvasElement | null = null;

```


---

## 🤖 Assistant · 2026-08-09T09:09:52.056Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 1,80p ~/Project/GLM/SandboxWorld/game/src/assets/CharacterSheetGen.ts; ls \"~/Project/GLM/SandboxWorld/game/public/sprites/角色\" | head -20; ls \"~/Project/GLM/SandboxWorld/game/public/sprites/UI\" | head -30",
 "description": "Read CharacterSheetGen and list character/UI sprites"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:52.078Z

**📎 ToolResult**

```
// 角色 sprite 程序化生成：玩家动画帧 + 敌人形象
import { MATS, shade } from './Palette';

function mk(w: number, h: number): [HTMLCanvasElement, CanvasRenderingContext2D] {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const ctx = c.getContext('2d')!;
  ctx.imageSmoothingEnabled = false;
  return [c, ctx];
}

class Px {
  img: ImageData;
  constructor(public ctx: CanvasRenderingContext2D, public w: number, public h: number, public ox = 0, public oy = 0) {
    this.img = ctx.createImageData(w, h);
  }
  set(x: number, y: number, color: string, a = 255) {
    if (x < 0 || y < 0 || x >= this.w || y >= this.h) return;
    const v = parseInt(color.slice(1), 16);
    const i = (y * this.w + x) * 4;
    this.img.data[i] = (v >> 16) & 255;
    this.img.data[i + 1] = (v >> 8) & 255;
    this.img.data[i + 2] = v & 255;
    this.img.data[i + 3] = a;
  }
  rect(x0: number, y0: number, w: number, h: number, color: string, a = 255) {
    for (let y = y0; y < y0 + h; y++) for (let x = x0; x < x0 + w; x++) this.set(x, y, color, a);
  }
  flush() { this.ctx.putImageData(this.img, this.ox, this.oy); }
}

// 玩家：20 宽 × 42 高 hitbox，sprite 画 24×44，帧横排
// 形象参考原版轮廓比例（大头小身、刺猬棕发、蓝上衣棕长裤），像素画为原创绘制
// 布局（y 坐标全部落帧内）：发 0-8 / 头 6-17 / 躯干 19-30 / 腿 31-40 / 鞋 41-42
export const PLAYER_FRAME_W = 24;
export const PLAYER_FRAME_H = 44;

interface Pose { legL: number; legR: number; armSwing: number; bodyBob: number; }

function drawPlayerFrame(px: Px, pose: Pose) {
  const skin = MATS.skin.base, skinDark = shade(MATS.skin.base, 0.82);
  const shirt = '#3E5CBE', shirtDark = '#2C4494', shirtLight = '#5A78D4';
  const pants = '#4A3826', pantsDark = '#382A1C';
  const hair = '#8A5A28', hairDark = '#6A4420';
  const boot = '#33241A';
  const eyeW = '#F0F0F0';
  const cx = 12;
  const bob = pose.bodyBob; // ±1，只作用于头/躯干/手臂，脚固定在地面

  // ---- 头发（帧顶，y 0..8）----
  const hy = 0 + bob;
  px.rect(cx - 6, hy + 2, 12, 6, hair);            // 发主体
  px.rect(cx - 7, hy + 4, 2, 6, hair);             // 后脑勺
  px.rect(cx + 6, hy + 4, 2, 4, hair);             // 鬓角
  // 发刺（原版后掠感）
  px.set(cx - 5, hy + 0, hair); px.set(cx - 2, hy + 0, hair);
  px.set(cx + 2, hy + 0, hair); px.set(cx + 5, hy + 0, hair);
  px.set(cx - 4, hy + 1, hair); px.set(cx + 1, hy + 1, hair); px.set(cx + 4, hy + 1, hair);
  px.rect(cx - 6, hy + 7, 12, 1, hairDark);        // 刘海底边

  // ---- 头（y 6..17，大头小身）----
  const fy = 6 + bob;
  px.rect(cx - 6, fy, 12, 12, skin);               // 脸
  px.rect(cx - 6, fy + 10, 12, 2, skinDark);       // 下颌阴影
  px.rect(cx - 1, fy + 11, 2, 2, skinDark);        // 脖子
  // 眼白 + 瞳孔 + 眉（面向右）
  px.rect(cx + 0, fy + 4, 2, 3, eyeW);
  px.rect(cx + 4, fy + 4, 2, 3, eyeW);
  px.set(cx + 1, fy + 5, '#183050');
  px.set(cx + 5, fy + 5, '#183050');
  px.rect(cx + 0, fy + 3, 2, 1, hairDark);
  px.rect(cx + 4, fy + 3, 2, 1, hairDark);

  // ---- 躯干（y 19..30）----
  const ty = 19 + bob;
  px.rect(cx - 5, ty, 10, 11, shirt);              // 上衣
  px.rect(cx - 5, ty, 2, 11, shirtLight);          // 左受光
  px.rect(cx + 3, ty, 2, 11, shirtDark);           // 右背光
  px.rect(cx - 5, ty + 9, 10, 2, pantsDark);       // 腰带

NPC_1.png
NPC_2.png
NPC_3.png
NPC_4.png
NPC_81.png
Player.png
Achievement_Borders_MouseHoverThin.png
Achievement_Borders.png
Buff
Inventory_Back14.png
Inventory_Back15.png
工具
饰品
药水

```


---

## 🤖 Assistant · 2026-08-09T09:09:56.245Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good picture. Player appearance: procedural CharacterSheetGen, fixed colors (no customization fields). Player.png exists in 角色 dir (Maples asset). Let me quickly check how drawPlayer works — does it use atlas (Player.png) or procedural sheet? Also check the worldgen UI gap: generateWorld onProgress reports pass name but no map preview. There's no "character" concept, no name.

Also check for existing "设置/settings" UI: none found (only pause with save/quit). Confirm by grep '设置' in src.

Also check Sfx/Audio for BGM (title/main), which matters for menu.

Let me grep quickly for a few remaining details: 'drawPlayer' implementation, 'settings', '音频' etc.
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:09:57.023Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"drawPlayer(\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -3; grep -n \"private drawPlayer\" -A 40 ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -60",
 "description": "Inspect drawPlayer implementation"
}
```


---

## 🤖 Assistant · 2026-08-09T09:09:57.028Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"设置\\|settings\\|Settings\" ~/Project/GLM/SandboxWorld/game/src | grep -v \"\\.test\\.\" | head -20; echo ----AUDIO----; sed -n 1,50p ~/Project/GLM/SandboxWorld/game/src/core/Audio.ts",
 "description": "Search settings UI and audio system"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:09:57.051Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1344:      this.cb.onToast('重生点已设置');
----AUDIO----
// 音频系统：BGM（标题曲/主曲）循环播放 + 静音开关
// 音乐来自 Terraia_Maples 项目资源
export class AudioSystem {
  private current: HTMLAudioElement | null = null;
  private title: HTMLAudioElement;
  private main: HTMLAudioElement;
  muted = false;

  constructor() {
    this.title = new Audio('audios/title.mp3');
    this.main = new Audio('audios/main.mp3');
    for (const a of [this.title, this.main]) {
      a.loop = true;
      a.volume = 0.35;
    }
  }

  play(which: 'title' | 'main') {
    if (this.muted) return;
    const next = which === 'title' ? this.title : this.main;
    if (this.current === next) return;
    this.current?.pause();
    this.current = next;
    next.currentTime = 0;
    next.play().catch(() => { /* 浏览器需用户交互后才能播放，忽略 */ });
  }

  /** 昼夜 BGM 变奏：白天正常速度，夜晚放慢+降调+减音量 */
  setDayNight(isDay: boolean) {
    if (this.muted) return;
    if (isDay) {
      this.main.playbackRate = 1;
      this.main.volume = 0.35;
    } else {
      this.main.playbackRate = 0.88;
      this.main.volume = 0.2;
    }
  }

  stop() {
    this.current?.pause();
    this.current = null;
  }

  toggleMute(): boolean {
    this.muted = !this.muted;
    if (this.muted) this.stop();
    return this.muted;
  }
}

```


---

## 👤 User(sidechain) · 2026-08-09T09:09:57.056Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:268:    this.drawPlayer(player, world, swing);
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:716:  private drawPlayer(p: Player, world: World, swing: { t: number; dur: number; item: number } | null) {
716:  private drawPlayer(p: Player, world: World, swing: { t: number; dur: number; item: number } | null) {
717-    const ctx = this.ctx;
718-    if (p.dead) return;
719-    // ---- 持有物/挥舞物：先画（人物身后图层） ----
720-    // 持有物显示：当前快捷栏选中物品静态握在手中（挥舞时由下方动画覆盖）
721-    // 尺寸按物品图标原始像素比例（×0.9）：镐/剑等大件大、凝胶等小件小，不再统一归一化
722-    {
723-      const held = p.inv.heldItem();
724-      if (!swing && held) {
725-        const ar = this.atlasIcon(held.id);
726-        const icon = ar ? null : this.itemIcon(held.id);
727-        // 静持锚点比挥砍更低更贴身（火把类小件已验证合适的位置基准）
728-        const shX = p.cx + p.facing * p.w * 0.48, shY = p.y + p.h * 0.8;
729-        ctx.save();
730-        ctx.translate(shX, shY);
731-        if (p.facing === -1) ctx.scale(-1, 1); // 整体镜像（贴图+姿态），左右完全对称
732-        ctx.rotate(0.45);
733-        if (ar) {
734-          const s = 0.9;
735-          const w = ar.sw * s, h = ar.sh * s;
736-          // 握把在左下角，并向手内侧收回 35%：避免整件往外杵
737-          ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, -w * 0.35, -h, w, h);
738-        } else if (icon) {
739-          ctx.drawImage(icon, -3.5, -9, 9, 9);
740-        }
741-        ctx.restore();
742-      }
743-    }
744-
745-    // 挥舞动画（工具/武器）：人物身后图层——挥砍弧大部分在身体轮廓外，身后不遮挡
746-    // 静持物品 + 工具/武器挥砍：人物身后图层（挥砍在前太露馅，收回身后）
747-    if (swing && swing.item >= 0 && ITEM_DEFS[swing.item]?.tool) {
748-      this.drawUseItem(ctx, p, swing);
749-    }
750-
751-    // 无敌帧闪烁：半透明而非消失（主角本体永不全隐）
752-    ctx.save();
753-    // 水下滤镜：只作用于主角本体素材（蓝色调：去饱和 + 压暗 + 蓝移）
754-    if (p.headUnderwater) ctx.filter = 'sepia(0.45) hue-rotate(175deg) saturate(0.9) brightness(0.82)';
755-    if (p.iframes > 0 && p.iframes % 6 < 2) ctx.globalAlpha = 0.45;
756-    // 跨台阶时用渲染补偿高度（从旧高度缓升），消除物理瞬移的顿挫感
--
1111:  private drawPlayerMarker(ctx: CanvasRenderingContext2D, x: number, y: number, size: number) {
1112-    let fw: number, fh: number, img: CanvasImageSource;
1113-    const atlasFrame = this.atlas ? this.atlas.rect('角色/Player.png', 'Player_0') : null;
1114-    if (atlasFrame) {
1115-      img = atlasFrame.img; fw = atlasFrame.sw; fh = atlasFrame.sh;
1116-    } else {
1117-      const sheet = this.assets.playerSheet;
1118-      img = sheet; fw = this.assets.playerFrameW; fh = this.assets.playerFrameH;
1119-    }
1120-    const aspect = fw / fh;
1121-    const h = size, w = size * aspect;
1122-    ctx.drawImage(img, 0, 0, fw, fh, x - w / 2, y - h / 2, w, h);
1123-  }
1124-
1125-  /** 全屏地图：半透明背景 + 完整世界图 + 边框 + 操作提示；支持拖动/缩放 */
1126-  drawFullMap(ctx: CanvasRenderingContext2D, world: World, mouseX: number, mouseY: number, mouseDown: boolean) {
1127-    const fm = this.fullMap;
1128-    const viewW = ctx.canvas.width, viewH = ctx.canvas.height;

```


---

## 🤖 Assistant · 2026-08-09T09:10:07.226Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have a comprehensive picture now. A couple more checks worth doing quickly:
1. Where in drawPlayer the character sprite is sourced (atlas 角色/Player.png vs procedural) — I saw drawPlayerMarker uses atlas 角色/Player.png. drawPlayer likely similar. Good enough.
2. Check docs for existing README about worldgen progress.
3. Check if `Sfx` loads audio from public/sounds.
4. Confirm generateWorld yields only between passes (yes), so map preview during generation isn't possible without further work — but the Minimap.colorFor could be reused to render a preview of the partial world; the world object is created inside generateWorld and returned only at end (no exposure of partial world).

Actually GenCtx has world; generateWorld calls onProgress(label, p) with the pass name only — no world reference. That's a gap for live map preview.

Also check the tests dir briefly and wld import for completeness. And check `dist/sprites/封面` has Logo/MapBG (title art assets available: Logo3.png, MapBG1.png, Splash_*.png). These are in tools/l10n? No wait — the listing order confused. Let me verify: the 4th ls command output was for 封面 dir: Logo3.png, MapBG1.png, Splash_6_0.png, Splash_9_0.png. And the 5th listing (sprites root): annotations.json, atlas.json, resources.json, UI, vanilla, vanilla-npcloot.json, vanilla-npcs.json, vanilla.json, 地形, 封面, 角色. Yes.

So title screen art exists: 封面/Logo3.png, MapBG1.png (menu background), Splash images.

Let me verify a couple of last things: whether there's any screenshot of the current UI in shots (the user asked "截图级描述" meaning describe layout in detail — not actual screenshots, but a detailed description). I have enough.

Let me also check the worldgen passes count and nextFrame, and check for `onProgress` granularity inside passes (report callback passed as noop — passes[i].run(ctx, () => {}), so no intra-pass progress). Important gap: intra-pass progress isn't reported, only per-pass.

Also quickly verify Game.newWorld onProgress mapping and the UI.showProgress implementation (done).

One more: check whether there's any scene/state machine abstraction — no, main.ts orchestrates imperatively with booleans.

I think I can now write the report. Since I'm a subagent with plan mode active... Actually the system says plan mode is active and I could create a plan file, but my role is read-only search; the instruction says return findings directly as final message. The plan-mode reminder says answer the user's query comprehensively. I'll just deliver the report as my final message.

Let me do a final quick check on a few facts: drawPlayer body sprite source and Sfx path; also verify no zh i18n usage in game src (already confirmed none). Also check UI 封面 usage anywhere (grep 封面).
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:10:07.715Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"封面\\|Logo3\\|MapBG\" ~/Project/GLM/SandboxWorld/game/src | head; echo ----; sed -n 756,830p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts; echo ----SFX----; sed -n 1,40p ~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts",
 "description": "Check title art usage, player sprite source, sfx"
}
```


---

## 👤 User(sidechain) · 2026-08-09T09:10:07.755Z

**📎 ToolResult**

```
----
    // 跨台阶时用渲染补偿高度（从旧高度缓升），消除物理瞬移的顿挫感
    ctx.translate(p.cx - p.facing * 2.5, p.y + p.h + p.stepRenderY); // 脚底中心（精灵后移2.5px = 碰撞盒微前移）
    ctx.scale(p.facing, 1);

    // ---- Maples 主角帧（40×58，Run 11 帧循环）----
    let drawn = false;
    if (this.atlas) {
      const idle = this.atlas.rect('角色/Player.png', 'Player_0');
      const runFrames = this.runFramesCache ??= this.atlas.animFrames('Player/Run');
      // 动作帧池（Player.png 12-22 号帧）
      if (!this.actionFramesCache) {
        const pool: Record<string, ReturnType<SpriteAtlas['rect']>> = {};
        for (let k = 12; k <= 22; k++) {
          const fr = this.atlas!.rect('角色/Player.png', 'Player_' + k);
          if (fr) pool['Player_' + k] = fr;
        }
        this.actionFramesCache = pool;
      }
      const af = this.actionFramesCache;
      let frame: typeof idle = null;
      // 挥砍/使用中：身体切换到动作姿态（Player.png 倒数 4 帧 = Player_19-22）
      if (swing) {
        // 手部动作帧比道具旋转慢约 16%（跟手），并钳在末帧——
        // 原来的 %4 会让手在 prog=1 时跳回第一帧，比工具"快半拍"
        const swingIdx = 19 + Math.min(3, Math.floor((1 - swing.t / swing.dur) * 0.84 * 4));
        frame = af['Player_' + swingIdx] ?? idle;
      } else if (!p.onGround) {
        // 空中：上升用 12（收腿）、下落用 14（张腿）
        frame = (p.vy < 0 ? af['Player_12'] : af['Player_14']) ?? runFrames[0] ?? idle;
      } else if (Math.abs(p.vx) > 0.3) {
        const idx = Math.floor(p.animTime / 6) % runFrames.length;
        frame = runFrames[idx] ?? idle;
      } else {
        frame = idle;
      }
      if (frame) {
        // 精灵视觉高度固定 56px（≈3.5 格）——与碰撞盒解耦，
        // 碰撞盒缩小只影响物理，贴图保持高大观感不变
        const h = 56;
        const w = (frame.sw / frame.sh) * h;
        // 脚踏实地：按精灵最低不透明行对齐脚底（消除底部透明留白导致的浮空）
        const pad = this.spriteBottomPad(frame);
        // Maples 精灵默认朝左 → 内层翻转，画完还原（否则手持物会被一起翻到背后）
        ctx.save();
        ctx.scale(-1, 1);
        ctx.drawImage(frame.img, frame.sx, frame.sy, frame.sw, frame.sh, -w / 2, -h + pad * (h / frame.sh), w, h);
        ctx.restore();
        drawn = true;
      }
    }
    if (!drawn) {
      // 程序化兜底（锚点同样为脚底中心）
      const sheet = this.assets.playerSheet;
      const fw = this.assets.playerFrameW, fh = this.assets.playerFrameH;
      const frame = p.frame;
      ctx.drawImage(sheet, frame * fw, 0, fw, fh, -fw / 2, -fh, fw, fh);
    }

    ctx.restore();
    // 使用类物品（托举：药水/方块等非工具）：身体前方图层，避免被身体挡住
    if (swing && swing.item >= 0 && !ITEM_DEFS[swing.item]?.tool) {
      this.drawUseItem(ctx, p, swing);
    }

    // 气口气泡：头部浸水时显示（在朝向变换外绘制——左右移动不镜像），
    // 随气量消散；整体更透明
    if (p.headUnderwater || p.breath < 5 || p.refillT >= 0) {
      const gap = 12.5; // 间距 12.5px，气泡直径 11px，留 ~1.5px 视觉分隔
      const baseX = p.cx - (5 * gap) / 2 + gap / 2, baseY = p.y - p.h * 0.4 - 14;
      // 优先原版 Bubble.png（22×22，不透明），程序化圆仅兜底
      const bub = this.atlas ? this.atlas.vmisc('vanilla/Bubble.png') : null;
      // 平滑气量 = (气口-1) + 当前正在消耗那颗的剩余比例 → 逐个渐隐（不画已耗尽的）。
      // 直接 breath+drain 会在扣气瞬间把气泡重新顶满一格
      // 水下：平滑消耗（当前颗渐隐）；出水：0.8s 快速补满动画
      let display: number;
----SFX----
// 音效：原版 wav 素材（public/sounds/）+ WebAudio 合成兜底
// hit 敌人受击 / hurt 玩家受击 / pickup 拾取 / dig 挖掘 / place 放置 / drink 饮用 / chop 砍树 / splash 落水
// + killed 怪物死亡 / zombie 僵尸环境声 / roar Boss咆哮 / coin 拾币 / door_open door_close / tink 敲石 / shatter 玻璃破碎 / drown 溺水
export type SfxName =
  | 'hit' | 'hurt' | 'pickup' | 'dig' | 'place' | 'drink' | 'chop' | 'splash'
  | 'killed' | 'pkilled' | 'zombie' | 'roar' | 'coin' | 'door_open' | 'door_close' | 'tink' | 'shatter' | 'drown';

// 逻辑名 → 原版 wav 文件（多文件随机选 + 音高扰动）
const WAV_MAP: Record<SfxName, string[]> = {
  hit: ['NPC_Hit_1', 'NPC_Hit_2', 'NPC_Hit_3', 'NPC_Hit_4', 'NPC_Hit_5'],
  hurt: ['Player_Hit_0', 'Player_Hit_1', 'Player_Hit_2'],
  killed: ['NPC_Killed_1', 'NPC_Killed_2', 'NPC_Killed_3'],
  pkilled: ['Player_Killed'],
  zombie: ['Zombie_1', 'Zombie_2', 'Zombie_3', 'Zombie_4', 'Zombie_5', 'Zombie_6'],
  roar: ['Roar_0', 'Roar_1'],
  pickup: ['Grab'],
  dig: ['Dig_0', 'Dig_1', 'Dig_2'],
  chop: ['Grass'],
  tink: ['Tink_0', 'Tink_1'],
  place: ['Dig_1', 'Dig_2'],
  shatter: ['Shatter'],
  coin: ['Coin_0', 'Coin_1', 'Coins'],
  door_open: ['Door_Opened'],
  door_close: ['Door_Closed'],
  splash: ['Splash_0', 'Splash_1'],
  drown: ['Drown'],
  // 以下无原版素材，走合成
  drink: [],
};

export class Sfx {
  private ctx: AudioContext | null = null;
  private buffers = new Map<string, AudioBuffer>();
  muted = false;

  private extraFiles = new Set<string>();
  /** 追加加载额外 wav 文件（怪物专属声效等） */
  addFiles(files: string[]) {
    for (const f of files) this.extraFiles.add(f);
    const ctx = this.ctx;

```


---

## 🤖 Assistant · 2026-08-09T09:10:11.492Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have everything I need for a comprehensive report. The 封面 (cover/title art: Logo3.png, MapBG1.png, Splash_6_0.png, Splash_9_0.png) exists in public/sprites/封面 but is NOT used by any code (grep found nothing).

Let me write the final report. It should be thorough, with file paths + line numbers, class/function names, layout descriptions, and the final gap analysis for the target UI chain.

Since plan mode is active but I'm a read-only search subagent, my deliverable is the report text. I will not create a plan file (the parent agent reads my text output). Actually the plan-mode system reminder says I "should create your plan at ... using the Write tool if you need to". It's optional ("if you need to"). My final message is the deliverable. I'll skip file creation since my role forbids writes and the reminder says reports go in the message.

Now compose the answer in Chinese (user asked in Chinese).
```

</details>


---

## 🤖 Assistant · 2026-08-09T09:11:07.540Z · glm-x-preview-260804

````
# SandboxWorld `game/` 目录调研报告

## 1. 项目整体结构

**技术栈**：Vite 5 + TypeScript 5.6 + vitest。唯一运行时依赖是 `simplex-noise`。无任何 UI 框架（无 React/PixiJS/DOM 框架）。

```
game/
├── index.html                 # 唯一 HTML：#game-root 容器 + 全局样式
├── public/sprites/            # 静态素材（atlas.json / vanilla.json / 角色 / UI / 封面 / 地形）
├── public/sounds|audios/      # 原版 wav 音效 + title/main 两首 BGM
├── src/
│   ├── main.ts                # 入口：素材加载 → 菜单 → 生成/导入 → 进游戏（394 行）
│   ├── core/                  # Game.ts(2332), Input.ts, Audio.ts, Sfx.ts, constants, rng, HitTile
│   ├── render/                # Renderer.ts(1426), Camera, ChunkCache, SkyRenderer, 各类 Tiler
│   ├── ui/UI.ts               # 全部 DOM overlay UI（1061 行，单文件）
│   ├── world/                 # World.ts, TileStore.ts, gen/(WorldGen + vanilla/* 30 个 pass)
│   ├── entities/  items/  data/  assets/  save/  stats/  lighting/  physics/  wld/
```

**渲染方式：纯 Canvas 2D**（无 WebGL/OffscreenCanvas）。
- `src/render/Renderer.ts:97` `class Renderer`，构造时 `document.createElement('canvas')` + `getContext('2d')`（`:158-161`），`attach(parent)`（`:186`）挂到 `#game-root`。
- `resize()` 直接 `canvas.width = window.innerWidth`（`:180-182`），**无 devicePixelRatio 处理**（1x CSS 像素 = 1 canvas 像素）。
- 绘制序（`render()`，`:192-360`）：天空 →（translate/scale 相机变换，`imageSmoothingEnabled=false` 最近邻）→ 背景水 → 墙 chunk → tile chunk → 瀑布 → 实体 → 玩家 → 前景水 → 粒子 → 挖掘光标 → restore → 光照 multiply 合成（2× 超采样双线性）→ Canvas 内 HUD（心/魔力/气口/Boss 条/小地图/全屏地图）。
- 缩放：`Camera.zoom` 默认 **1.25**，范围 0.75–2.5（`Camera.ts:6-9`），`+/-` 键步进 0.15、滚轮 ×0.94/1.064（`Game.ts:213-214, 456-466`）。**不是固定 2x 像素风格，而是连续 zoom**；像素锐利靠 `image-rendering: pixelated`（index.html）+ nearest-neighbor。

**游戏主循环**：`Game.start()`（`Game.ts:318-328`）`requestAnimationFrame` → `frame()`（`:330-343`）：累加器固定步长 `FIXED_DT = 1/60`（最多 5 步 catch-up，`paused` 时跳过），每帧末尾 `this.render()`。

**状态机/场景管理：没有**。`main.ts` 用模块级布尔/变量（`inGame`、`game`、`pausePanel`、`playStart`，`main.ts:21-24`）命令式编排。菜单→游戏→暂停的切换都是手写函数（`showMenu/enterGame/quitToMenu`），没有 Scene 抽象、没有事件总线。Game↔UI 解耦靠 `GameCallbacks` 接口（`Game.ts:52-58`：`onWorldReady/onInventoryChanged/onToast/onBuffsChanged/onDayNight`）。

## 2. 现有 UI 代码（全部在 `src/ui/UI.ts` 单文件）

模式：**原生 DOM overlay + 保留模式（retained mode）+ 手写命令式刷新**。CSS 是模板字符串注入 `<style>`（`UI.ts:47-94`）。无框架、无虚拟 DOM、无组件抽象；唯一工具函数 `el()`（`:40-45`）做 createElement。

样式基调：`.sw-panel` 深蓝渐变面板 + `#7d92d6` 描边（模仿原版蓝框），`.sw-btn` 紫渐变按钮，`.sw-slot` 44×44 格子 + 选中金边。`sw-root` 层 `position:fixed; inset:0; pointer-events:none; z-index:10`，面板内 `pointer-events:auto`。

已存在的界面：

- **主菜单** `showMainMenu()`（`UI.ts:133-215`）：340px 居中面板，标题「🌍 SandboxWorld」→ 种子输入框 → 世界尺寸 `<select>`（4200×1200 / 6400×1800 / 8400×2400，默认中）→ 按钮「创建新世界」「继续上次存档」「读取存档文件…(.json)」「导入泰拉瑞亚地图 (.wld)…」→ 底部「开发者模式」checkbox。**没有角色创建步骤，世界名也不能填**（名字在 `generateWorld` 里硬编码 `'新世界'`，`WorldGen.ts:33`）。
- **进度遮罩** `showProgress(label, p)` / `hideProgress()`（`UI.ts:447-463`）：全屏半黑 + 一行文字 + 320×14 圆角进度条。**纯文字，无地图预览**。
- **HUD** `buildHud()`（`:467-494`）：底部居中 10 格快捷栏（44px 格 + 图标 + 数量 + 金色选中框）；右下「🎒 背包 (E)」按钮；Tooltip 元素。心/魔力/气口/Boss 条/时间/小地图是 **Canvas 绘制**（`Renderer.ts` `drawMinimap` 等，`:1011-1108`；字体 `bold 14px monospace`）。
- **背包+纸娃娃** `buildInventoryPanel()`（`:789-853`）：居中面板。左列 152px：装备 3 格 / 时装 3 格 / 垃圾桶 1 格 / 配饰 5 格（3 列自动换行）/ 金钱 3 格；右侧背包 **10×4 grid**（槽 10–39）。下方「合成」区：可用合成站文字行 + 520px 宽、240px 高可滚动配方列表。
- **合成列表** `refreshCrafting()`（`:975-1008`）：按 `RECIPES` 过滤（站匹配 + 材料够不够），每行 = 图标 + 产物名×数量 + 右对齐「材料 have/need」。不可合成行 40% 透明。
- **宝箱** `buildChestPanel()`（`:901-912`）：5×2 十格，打开宝箱时与背包同显。
- **Buff 栏** `buildBuffBar()`（`:856-899`）：左上角 30px 方块 ×5，秒级倒计时，由 `onBuffsChanged` 每秒驱动。
- **拖拽系统**（`:521-696`）：按住 >4px 整叠拾取 / 右键拆半 / 光标持有 ghost 跟随 / `elementFromPoint` 判落点（格/垃圾桶/面板外丢世界/面板空白放回）/ 关包结算垃圾桶。装备位合法性靠 `Inventory.canAccept`。
- **暂停菜单** `showPause()`（`:1026-1039`）：280px 居中，三个按钮「继续游戏 / 保存存档 / 回到主菜单」。**无设置项**。
- **辅助面板**：`.wld` 导入兼容报告 `showCompatReport()`（`:218-259`）、F5 方块标注面板 `showAnnotatePanel()`（`:266-302`）、贴图纠错选择器 `openTexPicker()`（`:313-425`，内嵌 canvas 贴图表浏览）。Toast（`:1012-1022`）。
- **不存在的**：设置/选项界面、角色创建/选择、世界列表（只有单个 quicksave + 文件导入）、音量调节、键位说明。

## 3. 输入系统

`src/core/Input.ts`（54 行）：
- 键盘：`window keydown/keyup` 维护 `Set<string>`；`keydownHandlers` 数组（Game 注入数字键选格/缩放，`Game.ts:207-215`）；`blur` 清空。
- 鼠标：`mousemove` 记录 canvas 相对坐标；`mousedown/up` 挂 **window**（`Input.ts:29-38`），并按 `e.target.closest('.sw-panel, .sw-slot, .sw-recipe, .sw-btn')` 过滤 UI 点击不穿透为游戏输入；`wheel` 累计 `wheelDelta`；`contextmenu` preventDefault。
- **UI 屏蔽机制**：`uiBlocking` 布尔（背包/地图打开时置 true，`UI.ts:727,746`、`main.ts:199`），`down()` 返回 `!uiBlocking && keys.has(code)`。是全局单闸门，不是焦点/模态栈。
- 游戏内快捷键在 `main.ts:184-258`（window 级 keydown）：E/Esc 背包与暂停、F3 调试、F4 去迷雾、F5 标注、F6 保存、F8 刷怪、F9 fullbright、M 静音。

## 4. 素材加载

`src/assets/SpriteAtlas.ts`：
- **启动全量加载，无懒加载**（NPC 表除外）。`load()`（`:113-151`）把 `atlas.json` 所有文件 + vanilla 全部 tile/item/wall/npc 表 + `VANILLA_MISC` 并行 `new Image()`，路径前缀 `sprites/`（即 `public/sprites/`）。失败静默 resolve，整体失败时 `main.ts:32-34` 回退程序化素材。有 `onProgress` 参数但 `main.ts` 调用时没传 → **启动期无进度 UI**。
- Unity 图集 sprite rect 做 y 翻转（`:249-256`）+ 整图 hardAlpha 二值化去镶边（`:87-102`）。
- **懒加载仅一处**：`vnpc()`（`:192-218`）未登记 NPC 按 `vanilla/NPC_{id}.png` 现取。
- API：`vmeta/vframe/vframeAt/vrect/vicon/vmisc/rect/byGuid/animFrames`。图标查找链 `atlasIconForKey()`（`:317-345`）：手动表 → Maples 中文名表（`ITEM_ICON_MAP`）→ 原版物品 id 表（`VANILLA_ITEM_ICON_MAP`）→ `vi_<id>_*` 用 `vicon(id)` → `place_v_*` 用图块首帧。
- 图标进 DOM 前合成 32×32 dataURL 并缓存（`UI.ts:12-38` `iconCache`）。
- **字体**：无任何自定义字体/字体文件。Canvas 内用 `'bold 14px monospace'` / `'12px sans-serif'`（Renderer.ts 各处），DOM 继承 index.html 的 `"Segoe UI","PingFang SC","Microsoft YaHei"`。**没有像素字体**（原版 Andy 字体未使用）。
- 标题素材已备好但**完全未接**：`public/sprites/封面/` 有 `Logo3.png`、`MapBG1.png`、`Splash_6_0.png`、`Splash_9_0.png`（grep 无引用）。
- 音频：`Audio.ts` 两首 mp3 BGM（title/main，`public/audios/`）；`Sfx.ts` 原版 wav（`public/sounds/`）+ WebAudio 合成兜底。

## 5. 物品系统

- **数据结构**：`src/data/items.ts`。`interface ItemDef`（`:8-47`：`key/name/maxStack/tile?/placeStyle?/tool?{type,power,damage,speed,knockback,reach}/heal?/potion?/accessory?/armor?{slot,defense}/value?/desc?` 以及 `magic/ranged`）。**没有 Item 类实例**——物品运行态就是 `{ id: number; stack: number }`（`ItemStack`，`:253`），静态数据在 `ITEM_DEFS: ItemDef[]`（id 即数组下标）+ `ITEM_BY_KEY` 反查。注册函数 `item()`（`:53-56`）。
- 规模：自有物品 ~250 个；`vi_<id>_*` 从 `public/sprites/vanilla.json` **全量自动注册 6000+ 原版物品占位**（`:661-669`）；`v_` 图块自动注册 `place_v_*` 放置物（`:640-651`）。名字：自有的是中文，`vi_` 批次是英文原名。
- **合成表存在**：`src/data/recipes.ts`，`interface Recipe { out, count, station, inputs }`，`RECIPES` 约 80 条，station 仅 `'hand'|'workbench'|'furnace'|'anvil'` 四种（无放置型合成台/水槽/书架等）。判定在 `Game.stationsNearby()`（`Game.ts:2141-2154`，玩家 ±4×3 格扫描）/ `canCraft` / `craft`（`:2156-2166`）。
- 贴图关联：见第 4 节 `atlasIconForKey` 三层回退 + 程序化 `ItemIconGen.ts` 兜底。
- 背包布局常量在 `src/items/Inventory.ts:4-14`：0–39 背包（0–9 快捷栏）、40–44 配饰、45–47 盔甲、48–50 时装、51–53 金钱，`INV_SIZE = 54`。`class Inventory` 提供 add/removeAt/countOf/remove/canAccept/swap/heldItem/heldDef/equippedArmor/displayArmor。

## 6. 世界生成入口与进度回调

- 入口：`generateWorld(cfg, onProgress?)`，`src/world/gen/WorldGen.ts:31-83`。由 `Game.newWorld(seed, w, h, onProgress)` 调用（`Game.ts:220-228`），后者再串「水体沉降」（`settleLiquids`，`:234-256`，每 500 iter 让出主线程）。菜单侧调用点 `main.ts:93`。
- 管线：`passes: Pass[]`（`WorldGen.ts:45-72`）按序跑原版移植 pass（地形→洞穴→海滩→群系→清理→生命水晶→矿石→液体→半砖→瀑布→地狱→地狱屋→瓦罐→表面→装饰→结构），**每个 pass 之间 `await nextFrame()` 让出主线程**（`:74-78`），进度按 pass 序号线性上报（`:75`）。
- **进度回调已有**：签名 `(label: string, p: number) => void`，label 是 pass 名（如「原版地形」「水体沉降」），`main.ts:92-93` 直接接到 `ui.showProgress`。
- **缺口**：① `onProgress` 只在 pass 之间触发，pass 内部 `report` 回调被传成空函数（`:77`），长 pass（地形/洞穴）内部无细粒度进度；② **World 对象在 `generateWorld` 内部创建、最终才返回**（`:33, :82`），回调里拿不到部分生成的世界 → 无法做实时地图预览；③ 无取消/取消确认机制。

## 7. 玩家/角色数据与存档

- `src/entities/Player.ts:20-57`：`w=16,h=39`、`facing`、`baseMaxHp/baseMaxMana/hp/mana`、`inv: Inventory`、`buffs: BuffState`、`iframes/dead/respawnTimer`、`breath`、`animTime`、`inputX/inputJump/...`。**没有 `name`、没有任何外观字段（发型/发色/肤色/衣色/瞳色）**。
- 外观来源是素材固定帧：优先 Maples `角色/Player.png`（`atlas.rect('角色/Player.png','Player_0')` + `Player/Run` 动画 + 12–22 动作帧，`Renderer.ts:760-805`），否则程序化 `CharacterSheetGen.ts`（颜色硬编码：棕发 `#8A5A28`、蓝衣 `#3E5CBE`，`:46-52`）。盔甲有显示区分（`inv.displayArmor()`，时装优先），但仅 3 段式，非原版部件化纸娃娃。
- 存档：`src/save/SaveFile.ts`。JSON 外壳 + base64 RLE tile 段（`saveGame` `:105-136` / `loadSave` `:138-212`，version 2，带旧档墙 id 迁移）。**单槽位**：key `sandboxworld.quicksave` 写 `KvStore`（IndexedDB 优先、≤2MB 走 localStorage，`src/save/KvStore.ts`），或导出 .json 文件。存档里玩家只存 `hp/x/y/inventory/selected`（`SaveFile.ts:62-66, 128-131`）——**无角色名/外观可存**。`.wld` 导入走 `src/wld/WldImport.ts`（含 CompatReport）。

## 8. 语言 / i18n

- **代码内零 i18n**：grep `i18n|locale|translation|Lang` 在 `game/src` 无命中。所有 UI 字符串是硬编码中文（UI.ts、main.ts、Game.ts 的 toast）；`vi_*` 批次物品名是英文（占位）；`vanilla.json` 的 `tileNames/itemNames` 是英文原名。
- **素材已备**：仓库根 `tools/l10n/` 有从泰拉瑞亚客户端提取的全语言 JSON（**zh-Hans**、zh-Hant、en-US、ja-JP 等 13 语言 × 7 类：`*.Game/Items/Legacy/NPCs/Projectiles/Town.json`），`tools/extract_l10n.py` 是提取脚本。目前 **game 侧没有任何加载/映射逻辑**；原版文本要中文需要自己建 key→zh-Hans 查询表。

## 9. 对目标 UI 链路的适配度总结

目标链路：主菜单 → 创建角色 → 创建世界 → 世界生成进度（带地图实时预览）→ 游戏内背包/合成/设置。

**已具备（可直接复用）**
- DOM overlay 保留模式 + 原版风格皮肤（面板/按钮/格子/Tooltip/Toast）成熟，拖拽/合成/垃圾桶/装备位校验完整，背包+合成已是可用终态。
- 主菜单、进度条（label+pct）、暂停菜单骨架都在，链路 `main.ts showMenu→onNew→newWorld→enterGame` 已通。
- worldgen 已分帧 + 已有 `(label, p)` 进度回调，接进度 UI 零成本。
- 存档系统（IDB/localStorage/文件导出）、BGM 切换、`uiBlocking` 输入闸门可支撑各面板。
- 标题 Logo/背景图、zh-Hans 全量原版文本已备好（未接）。

**缺口（需要新建的部分）**
1. **无场景/状态机**：菜单、角色、世界列表、游戏、暂停的切换全是 `main.ts` 散装函数 + 模块级变量。多级菜单（菜单↔角色↔世界↔进游戏回退）建议先抽一个轻量 Scene/Screen 管理（哪怕只是 `UI.showScreen(name)` + 栈）。
2. **无角色概念**：`Player` 无 name/外观字段，存档不存角色，无角色列表/多角色。需要新增 `CharacterData`（name + hair/skin/eye/shirt/pants 色等），`saveGame`/`loadSave` 扩展，角色列表存 KvStore 多 key 或一个 index key。
3. **创建角色 UI 不存在**：需新建纸娃娃预览（可复用 `角色/Player.png` 帧 + 调色替换，或 CharacterSheetGen 参数化）。
4. **世界生成进度无地图预览**：`generateWorld` 不暴露中间 World。最小改法：`GenCtx.world` 在首个 pass 后通过 `onProgress` 附带传出（或新增 `onWorldPartial(world)` 回调），UI 侧用 `Minimap.colorFor` 的同款 tile→色逻辑（`Renderer.ts:33-52`）把部分世界画到预览 canvas。另外 pass 内 `report` 目前是 noop，长 pass 内无进度细分。
5. **无设置界面**：音量（`AudioSystem.volume` 固定 0.35）、静音（M 键）、缩放、`enemySpawnEnabled`、`devMode` 都有现成状态，缺一个 Settings 面板 + 持久化（KvStore）。
6. **无世界列表/多存档**：只有单 quicksave + 文件导入；`SaveData.header` 已有 `name/seed/created/playTimeMs`，做列表只差按 key 枚举（IDB getAll）+ UI。
7. **无 i18n 层**：若要原版文本中文化，需建 `vi_*/tile` 名 → `tools/l10n/zh-Hans.*.json` 的映射加载器（素材已备好，纯接线工作）。
8. **无像素字体**：原版 Andy 字体未打包，Canvas HUD 用 monospace、DOM 用系统字体；要原版观感需引入像素字体并统一 DOM+Canvas 两处。
9. **素材加载无进度 UI**：`atlas.load(onProgress)` 有回调但 `main.ts:31` 没传；大素材包首屏会白等，应接到 `showProgress`。
10. 小问题：`Input.uiBlocking` 是单布尔（同时开背包+地图+设置会互相踩）；`UI.closeAll()`（`UI.ts:1041`）直接 `innerHTML=''` 会把 HUD 一起拆掉（`showCompatReport` 注释已绕过过一次），多界面叠加时需改栈式管理。

**总体评价**：渲染、世界生成、物品/合成、存档等「游戏本体」相当完整（worldgen 已是原版 pass 级移植），UI 层是能用的单文件 DOM overlay；目标链路里「背包/合成/进度条/主菜单」已有雏形，**真正从零要做的是：屏幕管理、角色系统（数据+创建 UI）、生成期地图预览的数据通道、设置面板、世界列表、i18n 接线**。
````
