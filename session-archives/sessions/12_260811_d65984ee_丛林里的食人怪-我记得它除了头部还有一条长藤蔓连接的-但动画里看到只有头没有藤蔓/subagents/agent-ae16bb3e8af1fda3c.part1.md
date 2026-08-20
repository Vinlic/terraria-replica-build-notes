# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T07:14:41.060Z

```
在 ~/Project/GLM/SandboxWorld/game/src 里盘点"敌怪/实体特殊绘制"的已实现清单。重点文件 render/Renderer.ts（drawEnemy、drawSkeletronArm、drawPlantVine、纸娃娃等）、render/ 下其他文件、entities/ 下自带 draw() 的实体。

对每个特殊绘制实现输出：
- 文件+行号
- 触发条件（vanillaId 值 / aiStyle 值）
- 画的内容（贴图、几何）
- 注释里引用的原版源码位置（Main.cs 行号等）

另外检查：entities/Enemy.ts 里有哪些 AI 分族的注释声称"1:1"，特别是 AI_013（plantAI）、AI_011/12（骷髅王）、AI_047（石巨人）等涉及多部件的族。不要改任何文件。输出 markdown 清单。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T07:14:41.062Z

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

## 🤖 Assistant · 2026-08-11T07:14:42.591Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants an inventory of special enemy/entity drawing implementations in ~/Project/GLM/SandboxWorld/game/src. Let me explore the render/ directory and entities/ directory in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:43.111Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/game/src/render/ ~/Project/GLM/SandboxWorld/game/src/entities/ 2>/dev/null; echo \"---\"; ls ~/Project/GLM/SandboxWorld/game/src/",
 "description": "List render and entities directories"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:43.162Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/:
total 1080
drwxr-xr-x@ 24 user  staff     768  8月 11 15:12 .
drwxr-xr-x@ 24 user  staff     768  8月 11 12:12 ..
-rw-r--r--@  1 user  staff    6239  8月 11 12:17 Arrow.ts
-rw-r--r--@  1 user  staff   45632  8月 11 15:06 bossAI_duke_moonlord.ts
-rw-r--r--@  1 user  staff   27615  8月 11 14:59 bossAI_golem.ts
-rw-r--r--@  1 user  staff   44598  8月 11 15:06 bossAI_lategame.ts
-rw-r--r--@  1 user  staff   26672  8月 11 14:30 bossAI_queenbee_plantera.ts
-rw-r--r--@  1 user  staff   19006  8月 10 14:21 bossAI_wof.ts
-rw-r--r--@  1 user  staff   42669  8月 11 15:00 bossAI.ts
-rw-r--r--@  1 user  staff   13624  8月  6 18:41 Critter.ts
-rw-r--r--@  1 user  staff   10422  8月 11 12:17 Dart.ts
-rw-r--r--@  1 user  staff  171264  8月 11 15:12 Enemy.ts
-rw-r--r--@  1 user  staff    2317  8月 11 12:16 Entity.ts
-rw-r--r--@  1 user  staff    4397  8月 11 12:17 FallingBlock.ts
-rw-r--r--@  1 user  staff    5146  8月 11 14:43 ItemDrop.ts
-rw-r--r--@  1 user  staff    2485  8月 11 12:17 MagicProj.ts
-rw-r--r--@  1 user  staff    2481  8月 10 13:51 Minecart.ts
-rw-r--r--@  1 user  staff   47085  8月 11 14:42 Player.ts
-rw-r--r--@  1 user  staff    1625  8月 10 14:56 projTargets.ts
-rw-r--r--@  1 user  staff    5695  8月 10 13:32 Tombstone.ts
-rw-r--r--@  1 user  staff    9702  8月 11 10:54 TownNPC.ts
-rw-r--r--@  1 user  staff    2103  8月 11 12:13 types.ts
-rw-r--r--@  1 user  staff    1049  8月  6 18:36 waterAvoid.ts
-rw-r--r--@  1 user  staff   13707  8月 11 12:17 WeaponProj.ts

~/Project/GLM/SandboxWorld/game/src/render/:
total 712
drwxr-xr-x@ 21 user  staff     672  8月 11 15:14 .
drwxr-xr-x@ 24 user  staff     768  8月 11 12:12 ..
-rw-r--r--@  1 user  staff   17653  8月  6 00:52 AutoTiler.ts
-rw-r--r--@  1 user  staff   28118  8月 10 21:48 BiomeBackground.ts
-rw-r--r--@  1 user  staff   12213  8月  7 15:33 BlendFraming.ts
-rw-r--r--@  1 user  staff    1884  8月  5 18:29 Camera.ts
-rw-r--r--@  1 user  staff   17938  8月 11 00:09 ChunkCache.ts
-rw-r--r--@  1 user  staff    3102  8月 11 11:47 EmoteBubble.ts
-rw-r--r--@  1 user  staff    2067  8月 11 13:12 MapColors.ts
-rw-r--r--@  1 user  staff    6477  8月 10 23:55 MenuBackground.ts
-rw-r--r--@  1 user  staff  114972  8月 11 15:14 Renderer.ts
-rw-r--r--@  1 user  staff    6951  8月 10 12:07 ResourceBars.ts
-rw-r--r--@  1 user  staff   19796  8月 10 23:50 SkyRenderer.ts
-rw-r--r--@  1 user  staff    3397  8月 11 00:10 TileAnim.ts
-rw-r--r--@  1 user  staff   12928  8月 11 10:44 TileParticles.ts
-rw-r--r--@  1 user  staff   20335  8月 11 11:09 VanillaLiquidRenderer.ts
-rw-r--r--@  1 user  staff   29524  8月 11 00:25 VanillaTiler.ts
-rw-r--r--@  1 user  staff    6094  8月 11 00:57 VanillaWallTiler.ts
-rw-r--r--@  1 user  staff    7123  8月  5 17:21 WallTiler.ts
-rw-r--r--@  1 user  staff    8407  8月 11 14:40 WaterfallRenderer.ts
-rw-r--r--@  1 user  staff   10473  8月 10 23:50 WeatherRenderer.ts
---
assets
core
data
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

## 🤖 Assistant · 2026-08-11T07:14:43.427Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"draw(\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" -l | head -50",
 "description": "Find files containing draw methods"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:43.472Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/ui/WorldCreation.ts
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts
~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts
~/Project/GLM/SandboxWorld/game/src/render/MenuBackground.ts
~/Project/GLM/SandboxWorld/game/src/render/BiomeBackground.ts
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts
~/Project/GLM/SandboxWorld/game/src/render/VanillaWallTiler.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/render/WeatherRenderer.ts
~/Project/GLM/SandboxWorld/game/src/render/ResourceBars.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/UIElement.ts
~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/UserInterface.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIScrollbar.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIPanel.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIImage.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIList.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/GenWorldPreview.ts
~/Project/GLM/SandboxWorld/game/src/vui/draw/UISpriteBatch.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIGenProgressBar.ts
~/Project/GLM/SandboxWorld/game/src/vui/draw/PixelText.ts
~/Project/GLM/SandboxWorld/game/src/entities/Critter.ts
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts
~/Project/GLM/SandboxWorld/game/src/entities/Tombstone.ts

```


---

## 🤖 Assistant · 2026-08-11T07:14:44.579Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me search for the special drawing methods in Renderer.ts and the Enemy.ts AI family comments. Renderer.ts is huge (114972 bytes). Let me grep for the draw methods and special cases.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:45.555Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"drawEnemy\\|drawSkeletronArm\\|drawPlantVine\\|private draw\\|draw[A-Z][a-zA-Z]*(\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | grep -v \"drawTile\\|drawWall\\|drawLiquid\\|drawBackground\\|drawSky\\|drawWeather\\|drawUI\\|drawMenu\\|drawMap\\|drawMinimap\\|drawWaterfall\\|drawEmote\\|drawResource\" | head -80",
 "description": "Find draw method definitions in Renderer.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:45.600Z

**📎 ToolResult**

```
177:    this.redrawAll();
208:  redrawAll() {
468:        ctx.drawImage(chunks.get(cx, cy).wall, cx * CHUNK * ts, cy * CHUNK * ts, CHUNK * ts + over, CHUNK * ts + over);
476:        ctx.drawImage(chunks.get(cx, cy).tile, cx * CHUNK * ts, cy * CHUNK * ts, CHUNK * ts + over, CHUNK * ts + over);
481:    this.drawWires(world, cam, viewW, viewH, z);
483:    this.drawGrandPreview();
496:    this.drawHouseBanners(entities, world, cam);
501:      if (e instanceof Enemy) this.drawEnemy(e, world);
502:      else if (e instanceof ItemDrop) this.drawDrop(e);
503:      else if (e instanceof TownNPC) this.drawTownNPC(e);
504:      else if (e instanceof Tombstone) this.drawTombstone(e);
505:      else if (e instanceof Critter) this.drawCritter(e);
516:    this.drawPlayer(player, world, swing);
520:    for (const rp of this.remotePlayers) this.drawPlayer(rp, world, rp.swingNet);
584:      this.drawFullMap(ctx, world, this._mouseX, this._mouseY, this._mouseDown);
607:    if (this.debugMode) this.drawDebugOverlay(ctx, cam, viewW, viewH, player, entities, mouseX, mouseY, hover);
612:      this.drawBossBar(ctx, viewW, boss);
616:    if (invasion) this.drawInvasionBar(ctx, viewW, invasion);
633:    drawVanillaLiquids(this.ctx, this.atlas, world.store, world.groundLevel, tx0, ty0, tx1, ty1, this._liquidNow, isBackground);
640:  private drawWires(world: World, cam: Camera, viewW: number, viewH: number, z: number) {
678:          ctx.drawImage(wires, mask, rowY, 16, 16, tx * ts, ty * ts, ts, ts);
682:          ctx.drawImage(actuatorImg, 0, 0, 16, 16, tx * ts, ty * ts, ts, ts);
690:  private drawGrandPreview() {
736:  private drawTombstone(t: Tombstone) {
754:          cx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, dx * 16, dy * 16, 16, 16);
760:      ctx.drawImage(img, -16, -16, 32, 32);
763:      ctx.drawImage(pc, -8, -11, 16, 22);
769:  private drawCritter(c: Critter) {
805:    ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h + pad * (h / fr.sh), w, h);
809:  private drawDrop(d: ItemDrop) {
816:      ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, d.x, d.y + bob, 14, drawH);
822:        ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, d.x, d.y + bob, 14, drawH);
825:        ctx.drawImage(tinted, d.x, d.y + bob, 14, drawH);
832:    this.ctx.drawImage(icon, d.x, d.y + bob, 12, 12);
850:  private drawEnemy(e: Enemy, world: World) {
860:    if (e.vanillaId === 36 && e.master) this.drawSkeletronArm(e, e.master);
863:    if (e.vanilla?.aiStyle === 13) this.drawPlantVine(e);
923:        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, anchorY + eocOff, r.sw, r.sh);
937:          ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, anchorY, r.sw, r.sh);
940:          ctx.drawImage(tinted, -r.sw / 2, anchorY, r.sw, r.sh);
954:            ctx.drawImage(ninja.img, -ninja.sw / 2, -ninja.sh / 2, ninja.sw, ninja.sh);
965:            ctx.drawImage(crown.img, -crown.sw / 2, -e.h / 2 - (70 - num223) * scale - crown.sh / 2, crown.sw, crown.sh);
1043:          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h + pad * (h / fr.sh), w, h);
1049:          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h / 2, w, h);
1054:          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h / 2, w, h);
1057:          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h / 2, w, h);
1061:        this.drawEnemyHpBar(e);
1074:      ctx.drawImage(spr.canvas, -w / 2, -h, w, h);
1086:          ctx.drawImage(spr.canvas, f * fw, 0, fw, spr.fh, -e.w / 2, -e.h / 2, e.w, e.h);
1089:          ctx.drawImage(spr.canvas, frame * fw, 0, fw, spr.fh, -e.w / 2, -e.h / 2, e.w, e.h);
1094:        ctx.drawImage(spr.canvas, frame * fw, 0, fw, spr.fh, -spr.fw / 2, -spr.fh / 2, spr.fw, spr.fh);
1099:    this.drawEnemyHpBar(e);
1111:  private drawPlantVine(e: Enemy) {
1142:        ctx.drawImage(chain.img, chain.sx, chain.sy, chain.sw, seg,
1151:  private drawSkeletronArm(hand: Enemy, head: Enemy) {
1175:      ctx.drawImage(img, -img.naturalWidth / 2, -img.naturalHeight / 2);
1190:  private drawEnemyHpBar(e: { hp: number; maxHp: number; cx: number; y: number; h: number }) {
1219:  private drawHouseBanners(entities: unknown[], world: World, cam: Camera) {
1248:      ctx.drawImage(cloth.img, cloth.sx, cloth.sy, cloth.sw, cloth.sh,
1256:        ctx.drawImage(head.img, head.sx, head.sy, head.sw, head.sh,
1296:  private drawTownNPC(n: TownNPC) {
1300:    this.drawEnemyHpBar(n);
1315:        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, -r.sh + pad, r.sw, r.sh);
1327:    ctx.drawImage(spr.canvas, -spr.fw / 2, -spr.fh / 2, spr.fw, spr.fh);
1331:  private drawPlayer(p: Player, world: World, swing: { t: number; dur: number; item: number } | null) {
1357:              ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, 0, -h, w, h);
1359:              ctx.drawImage(icon, 0, -icon.height * 0.6, icon.width * 0.6, icon.height * 0.6);
1368:      this.drawUseItem(ctx, p, swing);
1399:        ctx.drawImage(f.img, f.sx, f.sy, f.sw, f.sh, -f.sw / 2, -f.sh + pad, f.sw, f.sh);
1441:        ctx.drawImage(frame.img, frame.sx, frame.sy, frame.sw, frame.sh, -w / 2, -h + pad * (h / frame.sh), w, h);
1451:      ctx.drawImage(sheet, frame * fw, 0, fw, fh, -fw / 2, -fh, fw, fh);
1457:      this.drawUseItem(ctx, p, swing);
1486:          ctx.drawImage(bub.img, bub.sx, bub.sy, bub.sw, bub.sh, bx - 5.5, by - 5.5, 11, 11);
1510:  private drawUseItem(ctx: CanvasRenderingContext2D, p: Player, swing: { t: number; dur: number; item: number }) {
1547:      ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, fw / 2, -fh, ar.sw, ar.sh);
1549:      ctx.drawImage(icon, 7, -14, 14, 14);
1575:   *  alpha 保持精灵原样（XNA 预乘混合的 RGB 贡献不随 color.A 缩减，见 drawEnemy color pass）
1588:    cx.drawImage(frame.img, frame.sx, frame.sy, frame.sw, frame.sh, 0, 0, c.width, c.height);
1595:    cx.drawImage(frame.img, frame.sx, frame.sy, frame.sw, frame.sh, 0, 0, c.width, c.height);
1612:      cx.drawImage(frame.img, frame.sx, frame.sy, frame.sw, frame.sh, 0, 0, frame.sw, frame.sh);

```


---

## 🤖 Assistant · 2026-08-11T07:14:46.269Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"1:1\\|1:1移植\\|AI_013\\|AI_011\\|AI_012\\|AI_047\\|plantAI\\|PlantAI\\|Skeletron\\|Golem\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -80",
 "description": "Find 1:1 claims and AI family comments in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:46.299Z

**📎 ToolResult**

```
348:          break;                                                         // AI_011 骷髅王头战斗核/地牢守卫
349:        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
356:        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
385:        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
655:  // ai[1] = 体内物品 id → 目标色表（蛆/凝胶/铂金币等占位色的 1:1 表）；踩油漆色 lerp 暂缺（无油漆系统）
903:  /** NPCCanStickToWalls 1:1（NPC.cs:56209-56229）：身体中心 3×3 内"非实心 tile 且有背景墙"
922:  /** Transform 1:1（NPC.cs:81861-81919）：换类型 + 按比例结转 HP + ai[0..3] 清零；
959:  /** AI_040 爬墙蜘蛛族 1:1（NPC.cs:29784-30022）：无重力、贴背景墙表面爬行。
1058:  /** AI_042 失落女孩 1:1（NPC.cs:30281-30310）：伪装成无害 NPC 静止站立（无移动逻辑，
1590:  /** AI_013 植物/攀爬者族(NPC.cs:22604-22700 一比一):锚点格(ai0/ai1)固定,
1593:  private plantAI(game: GameHooks, player: Player | null) {
1833:  // AI_011 骷髅王(35)战斗状态机在 bossAI.ts skeletronBossAI；68 守卫走下方专用分支
1835:  /** AI_011 地牢守卫(68)（NPC.145.cs:21937-21941, 22277-22288）：
2206:   *  各家族原版行为（蚱蜢 ai1 跳/鸟 ai24 飞/蚯蚓 ai66 爬）后续逐族 1:1，先统一温和地面行为 */
2330:  /** 小动物路由：按 aiStyle 精确分流到各家族 1:1 实现（AI_001/016 复用既有精确 AI） */
2941:   * AI_004 克苏鲁之眼 1:1（1456 NPC.cs:19909-20757，普通模式数值；专家分支未启用）。

```


---

## 🤖 Assistant · 2026-08-11T07:14:48.028Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the key sections in Renderer.ts (drawEnemy, drawPlantVine, drawSkeletronArm), and the paper doll code (drawPlayer area), plus other special draws. Renderer.ts is huge. Let me read the relevant sections.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:48.170Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "offset": 840,
 "limit": 360
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:48.182Z

**📎 ToolResult**

```
840	      const map: Record<string, string> = {
841	        slime_green: 'Slime/Jump', slime_blue: 'Slime/Jump',
842	        zombie: 'Zombie/Walk',
843	      };
844	      f = this.atlas && map[key] ? this.atlas.animFrames(map[key]) : [];
845	      this.enemyAnimCache.set(key, f);
846	    }
847	    return f;
848	  }
849	
850	  private drawEnemy(e: Enemy, world: World) {
851	    const ctx = this.ctx;
852	    const spr = this.assets.enemySprites.get(e.key);
853	    // 受击闪白
854	    const flash = e.iframes > 0 && e.iframes % 4 < 2;
855	    // 水下滤镜：与主角一致的蓝色调（检查怪物头部位置是否浸水）
856	    const headI = world.store.idx(Math.floor(e.cx / TILE), Math.floor((e.y + 2) / TILE));
857	    const underwater = world.store.liquid[headI] > 100;
858	    // 骷髅王手（36）的两节臂骨 IK（Main.cs:22543-22596 1:1）：从手部锚点向头
859	    // 中心做两段收缩（92/60 缩比），段间旋转 atan2-π/2——贴图 Arm_Bone.png
860	    if (e.vanillaId === 36 && e.master) this.drawSkeletronArm(e, e.master);
861	    // AI_013 食人怪族茎蔓（Main.cs:22433-22514 1:1）：头中心 → 锚点格(ai0/ai1)
862	    // 每 28px 一段 Chain 贴图步进，剩余 <40px 画一段收缩尾段对齐锚点
863	    if (e.vanilla?.aiStyle === 13) this.drawPlantVine(e);
864	    // ---- 原版 NPC 表精灵（数据驱动路径：纵向帧条 + 朝向翻转，原版贴图默认朝左） ----
865	    if (e.vanillaId != null && this.atlas) {
866	      const frames = Math.max(1, e.vanilla?.frames ?? 1);
867	      const frameIdx = vanillaFrameIdx(e, frames);
868	      const r = this.atlas.vnpc(e.vanillaId, frameIdx);
869	      if (r) {
870	        const flying = !!e.vanilla?.noGravity; void flying; // 中心锚后地面/飞行统一,仅保留语义注释
871	        // 原版 NPC.scale（SetDefaults base × netID scale）——作用于碰撞盒与渲染
872	        const scale = (e.vanilla?.scale ?? 1) * e.vanillaScale;
873	        ctx.save();
874	        // 锚点:飞行型=帧中心(原版默认分支 Main.cs:23635 语义);地面型=底锚+逐帧
875	        // 实测底部透明行数补偿(spriteBottomPad)——NPC 帧底普遍 ~2px 透明边距,
876	        // 裸底锚会悬空 2px、中心锚会入地 2px(实测反馈),pad 补偿数学上保证贴地。
877	        // 与纸娃娃(:1266)/legacy(:1301)/小动物(:763)四路统一
878	        const grounded = !flying;
879	        ctx.translate(e.cx, grounded ? e.y + e.h : e.cy);
880	        // 旋转族:整体随自转角旋转(原版 npc.rotation;朝向翻转不适用)。
881	        // 4=克眼 visAngle;35/68=骷髅王头 spin;125/126=双子;127-131=Prime 头+部件;134-136=毁灭者链
882	        const rotId = ROTATION_NPC.has(e.vanillaId);
883	        // ★旋转驱动族总判定：朝向完全由 rotation 决定，原版这些家族不动 spriteDirection
884	        // （默认 -1 从不镜像）——渲染层禁止对其叠加 facing 镜像，否则"屁股朝前"
885	        // （噬魂怪 aiStyle5 实踩）。新增旋转族 AI 时必须登记在此，旋转与镜像共用本判定。
886	        // 例外：AI_005 内的"仅倾斜"成员（黄蜂 42/231-235、孢子蝠 176/205、蜜蜂 210/211）
887	        // 贴图横画、只 tilt 不转头——它们仍需镜像翻转朝向（原版同款 spriteDirection 翻转）。
888	        const idR = e.vanillaId ?? -1;
889	        const stR = e.vanilla?.aiStyle ?? 0;
890	        const tiltOnly5 = stR === 5 && (idR === 42 || idR === 176 || idR === 205 || idR === 210
891	          || idR === 211 || (idR >= 231 && idR <= 235));
892	        const rotationDriven = !tiltOnly5
893	          && (idR === 4 || rotId || stR === 5 || stR === 6 || stR === 23 || stR === 40 || stR === 56);
894	        if (e.vanillaId === 4) ctx.rotate(e.visAngle);
895	        else if (e.vanilla?.aiStyle === 5) {
896	          // AI_005 旋转按族分流（cs:51045-51054 + FindFrame 蜜蜂覆盖 L75553）：
897	          // 黄蜂 42/231-235、孢子蝠 176、205 仅倾斜 vx*0.1（不随飞行方向转头）；
898	          // 蜜蜂 210/211 倾斜 vx*0.2；其余（噬魂怪族等）朝目标/速度方向转头。
899	          // 全族统一转头会让黄蜂蜜蜂飞行中整只倒转=贴图翻转观感
900	          const id5 = e.vanillaId;
901	          if (id5 === 42 || id5 === 176 || id5 === 205 || (id5 >= 231 && id5 <= 235)) ctx.rotate(e.vx * 0.1);
902	          else if (id5 === 210 || id5 === 211) ctx.rotate(e.vx * 0.2);
903	          else ctx.rotate(e.visAngle);
904	        }
905	        else if (e.vanilla?.aiStyle === 6) ctx.rotate(e.visAngle); // AI_006 蠕虫族:cs:51500 段随链方向旋转(贴图正面朝上,+π/2)
906	        else if (e.vanilla?.aiStyle === 40) ctx.rotate(e.visAngle); // AI_040 爬墙蜘蛛:npc.rotation 随移动/期望速度角(cs:29865/29919),531 +π/2
907	        else if (e.vanilla?.aiStyle === 23) ctx.rotate(e.visAngle); // AI_023 飞行武器:冲刺角 atan2+0.785 / 蓄转递增(cs:25336-25390)
908	        else if (e.vanilla?.aiStyle === 56) ctx.rotate(e.visAngle); // AI_056 地牢之魂:rotation=atan2(v)-π/2(cs:32927)
909	        else if (rotId) ctx.rotate(e.spin);
910	        ctx.scale(scale, scale);
911	        if (!rotationDriven && e.facing > 0) ctx.scale(-1, 1); // 原版默认朝左；旋转族（rotationDriven）禁镜像
912	        // 原版 alpha 语义（NPC.Opacity/GetAlpha）：不透明度 = 1 - alpha/255。
913	        // alpha 是 SetDefaults 每类型静态值（0=实体；史莱姆 175=半透明凝胶），无通用渐隐
914	        ctx.globalAlpha = 1 - Math.min(255, Math.max(e.spawnAlpha, 0)) / 255;
915	        // EoC 锚点修正:NPC_4 每帧 110×166,眼球主体质心在帧内 y≈106(张嘴帧 113),
916	        // 帧中心 83——原版通用锚点(帧中心==碰撞盒中心)会让 100×110 的盒偏在
917	        // 血管尾/眼球上方。碰撞盒尺寸保持原版,绘制整体下移 (质心−帧中心)
918	        // 让眼球主体居中于盒(用户 2026-08-11 拍板;张嘴帧偏移略大)
919	        // 地面型:底锚 + pad(帧底透明行)贴地;飞行型:中心锚。EoC 额外 +23/+30 眼球修正
920	        const pad = grounded ? this.spriteBottomPad(r, `npc${e.vanillaId}:f${frameIdx}`) : 0;
921	        const anchorY = grounded ? -r.sh + pad : -r.sh / 2;
922	        const eocOff = e.vanillaId === 4 ? (frameIdx < 3 ? 23 : 30) : 0;
923	        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, anchorY + eocOff, r.sw, r.sh);
924	        // 原版 color 二次绘制（Main.cs:24527 + NPC.GetColor L94903）：color≠default 时用
925	        // 同贴图再画一遍、逐像素乘 color（XNA SpriteBatch 天生贴轮廓）；
926	        // color.A 决定该 pass 强度（史莱姆贴图是白剪影，颜色全靠这层）
927	        if (e.colorRGBA && e.colorRGBA[3] > 0) {
928	          // XNA 预乘混合等价（BlendState.AlphaBlend：out = texel×colorRGB + D×(1-colorA/255)）。
929	          // 普通 drawImage 会把染色 RGB 再乘 alpha（蓝色糊成灰绿）——改为两步：
930	          // ① 原始精灵 destination-out 按 colorA 削弱底下内容 ② lighter 全量加染色精灵
931	          const tinted = this.tintedSprite(`npc${e.vanillaId}`, r, e.colorRGBA);
932	          const anchorY2 = grounded ? -r.sh + pad : -r.sh / 2;
933	          const anchorY = anchorY2 + eocOff; // 与基础层同锚——曾残留旧底锚条件,
934	          // 基础/染色两层错位 → 史莱姆"彩色+灰影"双画
935	          ctx.globalCompositeOperation = 'destination-out';
936	          ctx.globalAlpha = e.colorRGBA[3] / 255;
937	          ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, anchorY, r.sw, r.sh);
938	          ctx.globalCompositeOperation = 'lighter';
939	          ctx.globalAlpha = 1;
940	          ctx.drawImage(tinted, -r.sw / 2, anchorY, r.sw, r.sh);
941	          ctx.globalCompositeOperation = 'source-over';
942	        }
943	        // 史莱姆王体内忍者（Main.cs:22798-22818 1:1）：独立贴图 Ninja.png 叠画在
944	        // KS 中心，随速度反向摆动（zero=-vy / -vx*2）+ rotation=vx*0.05，
945	        // 帧顶 120/360/480 的挤压帧 y 修正（+2/-2/-6）
946	        if (e.vanillaId === 50) {
947	          const ninja = this.atlas.vmisc('vanilla/Ninja.png');
948	          if (ninja) {
949	            const zeroY = -e.vy + (r.sy === 120 ? 2 : r.sy === 360 ? -2 : r.sy === 480 ? -6 : 0);
950	            const zeroX = -e.vx * 2;
951	            ctx.save();
952	            ctx.translate(zeroX, -e.h / 2 + zeroY);   // 当前原点=KS 底心 → 中心=(0,-h/2)
953	            ctx.rotate(e.vx * 0.05);
954	            ctx.drawImage(ninja.img, -ninja.sw / 2, -ninja.sh / 2, ninja.sw, ninja.sh);
955	            ctx.restore();
956	          }
957	          // 头顶金冠（Main.cs:25571-25595 case 50，1:1）：贴图 Extra_39（82×56，
958	          // wiki"the crown...separate image files...Extra_39 internally"）。锚点 =
959	          // KS Center 上移 (70-num223)×scale，num223 按帧序 [2,-6,2,10,2,0]；
960	          // 朝向翻转继承外层 facing scale。gfxOffY 恒 0（KS 无悬浮偏移）
961	          const crown = this.atlas.vmisc('vanilla/Extra_39.png');
962	          if (crown) {
963	            const frameIdx2 = Math.round(r.sy / r.sh);
964	            const num223 = [2, -6, 2, 10, 2, 0][frameIdx2] ?? 0;
965	            ctx.drawImage(crown.img, -crown.sw / 2, -e.h / 2 - (70 - num223) * scale - crown.sh / 2, crown.sw, crown.sh);
966	          }
967	        }
968	        ctx.restore();
969	        ctx.globalAlpha = 1;
970	        ctx.globalCompositeOperation = 'source-over';
971	        return;
972	      }
973	      return; // 表未加载完成：本帧不画（下帧懒加载完成）
974	    }
975	    // ---- Maples 精灵优先 ----
976	    if (this.atlas) {
977	      let frames: ReturnType<SpriteAtlas['animFrames']> = [];
978	      let anchor: 'feet' | 'center' = 'feet';
979	      if (e.key.startsWith('slime')) { frames = this.enemyAnim(e.key); anchor = 'feet'; }
980	      else if (e.key === 'zombie') { frames = this.enemyAnim(e.key); anchor = 'feet'; }
981	      else if (e.key === 'cave_bat') {
982	        // 洞穴蝙蝠：原版 NPC_49（44x32×5 帧扑翼），逐帧动画
983	        if (!this.enemyAnimCache.has('bat49')) {
984	          const list: ReturnType<SpriteAtlas['animFrames']> = [];
985	          for (let k = 0; k < 5; k++) {
986	            const r = this.atlas!.vnpc(49, k);
987	            if (r) list.push(r);
988	          }
989	          this.enemyAnimCache.set('bat49', list);
990	        }
991	        frames = this.enemyAnimCache.get('bat49') ?? [];
992	        anchor = 'center';
993	      }
994	      else if (e.key === 'demon_eye') {
995	        // 恶魔之眼：NPC_2 双帧
996	        frames = this.enemyAnimCache.get('deye') ?? [];
997	        if (!frames.length) {
998	          const file = this.atlas.data.files['角色/NPC_2.png'];
999	          if (file) {
1000	            frames = file.sprites.map((sp) => this.atlas!.rect('角色/NPC_2.png', sp.name)).filter(Boolean) as typeof frames;
1001	          }
1002	          this.enemyAnimCache.set('deye', frames);
1003	        }
1004	        anchor = 'center';
1005	      }
1006	      else if (e.key === 'eye_of_cthulhu') {
1007	        // Boss 用 NPC_4：底部 3 帧 = 一阶段动画，顶部 3 帧 = 二阶段（实测对调）
1008	        if (!this.enemyAnimCache.has('eoc_p1')) {
1009	          const file = this.atlas.data.files['角色/NPC_4.png'];
1010	          const toFrames = (arr: typeof file.sprites) =>
1011	            arr.map((s) => this.atlas!.rect('角色/NPC_4.png', s.name)).filter(Boolean) as ReturnType<SpriteAtlas['animFrames']>;
1012	          if (file) {
1013	            const sorted = [...file.sprites].sort((a, b) => a.y - b.y); // 顶部在前
1014	            this.enemyAnimCache.set('eoc_p1', toFrames(sorted.slice(3, 6)));
1015	            this.enemyAnimCache.set('eoc_p2', toFrames(sorted.slice(0, 3)));
1016	          } else {
1017	            this.enemyAnimCache.set('eoc_p1', []);
1018	            this.enemyAnimCache.set('eoc_p2', []);
1019	          }
1020	        }
1021	        frames = e.phase === 2
1022	          ? (this.enemyAnimCache.get('eoc_p2') ?? [])
1023	          : (this.enemyAnimCache.get('eoc_p1') ?? []);
1024	        anchor = 'center';
1025	      }
1026	      if (frames.length) {
1027	        const rate = e.key === 'eye_of_cthulhu' ? (e.phase === 2 ? 6 : 10) : 12;
1028	        const idx = Math.floor(e.animT / rate) % frames.length;
1029	        const fr = frames[idx];
1030	        ctx.save();
1031	        if (flash) ctx.filter = 'brightness(2.5)';
1032	        else if (underwater) ctx.filter = 'sepia(0.45) hue-rotate(175deg) saturate(0.9) brightness(0.82)';
1033	        // 缩放贴合碰撞盒
1034	        const h = anchor === 'feet' ? e.h * 1.25 : e.h;
1035	        const w = (fr.sw / fr.sh) * h;
1036	        if (anchor === 'feet') {
1037	          ctx.translate(e.cx, e.y + e.h);
1038	          // 素材默认朝左：向右移动时镜像（僵尸实测需要与其它怪一致的翻转）
1039	          const flip = -e.facing;
1040	          ctx.scale(flip, 1);
1041	          // 贴底：按精灵最低不透明行对齐脚底（史莱姆贴图底部有透明留白会浮空）
1042	          const pad = this.spriteBottomPad(fr);
1043	          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h + pad * (h / fr.sh), w, h);
1044	        } else if (e.key === 'demon_eye') {
1045	          // 恶魔之眼：以眼球为原点按移动方向自由旋转（贴图默认朝左，与 NPC 系素材一致）
1046	          const ang = Math.atan2(e.vy, e.vx) + Math.PI;
1047	          ctx.translate(e.cx, e.cy);
1048	          ctx.rotate(ang);
1049	          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h / 2, w, h);
1050	        } else if (e.key === 'eye_of_cthulhu') {
1051	          // 朝向移动方向自由旋转（AI 端平滑追踪目标角度，变身时三圈自转叠加）
1052	          ctx.translate(e.cx, e.cy);
1053	          ctx.rotate(e.visAngle);
1054	          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h / 2, w, h);
1055	        } else {
1056	          ctx.translate(e.cx, e.cy);
1057	          ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h / 2, w, h);
1058	        }
1059	        ctx.restore();
1060	        ctx.filter = 'none';
1061	        this.drawEnemyHpBar(e);
1062	        return;
1063	      }
1064	    }
1065	    // ---- 程序化兜底 ----
1066	    if (e.key.startsWith('slime') && spr) {
1067	      const sq = 1 + e.squash * 0.25;
1068	      const w = e.w * 1.3 * sq, h = e.h * 1.25 / sq;
1069	      ctx.save();
1070	      if (flash) ctx.filter = 'brightness(2.5)';
1071	      else if (underwater) ctx.filter = 'sepia(0.45) hue-rotate(175deg) saturate(0.9) brightness(0.82)';
1072	      ctx.translate(e.cx, e.y + e.h);
1073	      ctx.scale(e.facing, 1);
1074	      ctx.drawImage(spr.canvas, -w / 2, -h, w, h);
1075	      ctx.restore();
1076	      ctx.filter = 'none';
1077	    } else if (spr) {
1078	      const fw = spr.fw;
1079	      const frame = spr.canvas.width > fw ? Math.floor(e.animT / 12) % (spr.canvas.width / fw) : 0;
1080	      ctx.save();
1081	      if (flash) ctx.filter = 'brightness(2.5)';
1082	      if (e.key === 'eye_of_cthulhu') {
1083	        ctx.translate(e.cx, e.cy);
1084	        if (e.phase === 2) {
1085	          const f = Math.floor(e.animT / 10) % 2;
1086	          ctx.drawImage(spr.canvas, f * fw, 0, fw, spr.fh, -e.w / 2, -e.h / 2, e.w, e.h);
1087	        } else {
1088	          ctx.scale(e.facing, 1);
1089	          ctx.drawImage(spr.canvas, frame * fw, 0, fw, spr.fh, -e.w / 2, -e.h / 2, e.w, e.h);
1090	        }
1091	      } else {
1092	        ctx.translate(e.cx, e.cy);
1093	        ctx.scale(e.facing, 1);
1094	        ctx.drawImage(spr.canvas, frame * fw, 0, fw, spr.fh, -spr.fw / 2, -spr.fh / 2, spr.fw, spr.fh);
1095	      }
1096	      ctx.restore();
1097	      ctx.filter = 'none';
1098	    }
1099	    this.drawEnemyHpBar(e);
1100	    void world;
1101	  }
1102	
1103	  /** Arm_Bone.png 懒加载（骷髅王臂骨；vanilla 独立贴图，非 NPC 表） */
1104	  private armBoneImg: HTMLImageElement | null | undefined;
1105	  /** AI_013 植物/攀爬者族茎蔓（Main.cs:22433-22514 1:1）：从 NPC 中心向锚点格
1106	   *  中心（ai0/ai1 各 ×16+8）逐段画 Chain 贴图——步长 28px、距锚 <40px 时尾段
1107	   *  缩短对齐（259/260 真菌球为 12/20）；整链 rotation=atan2(dy,dx)-π/2（贴图
1108	   *  正面向上）。贴图分流（:22480-22510）：56→Chain5、175→Chain14、259/260→
1109	   *  Chain24/25，默认（43 食人怪/101 邪恶触手）→Chain4。光照由 compositeLight
1110	   *  全屏合成，此处不逐段取光 */
1111	  private drawPlantVine(e: Enemy) {
1112	    if (!this.atlas || e.ai0 < 0 || e.ai1 < 0) return;
1113	    const id = e.vanillaId;
1114	    // num7/num8：段长/终止距离（Main.cs:22442-22447）
1115	    let step = 28, stop = 40;
1116	    if (id === 259 || id === 260) { step = 12; stop = 20; }
1117	    const chain = this.atlas.vmisc(
1118	      id === 56 ? 'vanilla/Chain5.png'
1119	        : id === 175 ? 'vanilla/Chain14.png'
1120	          : id === 259 ? 'vanilla/Chain24.png'
1121	            : id === 260 ? 'vanilla/Chain25.png'
1122	              : 'vanilla/Chain4.png');
1123	    if (!chain) return;
1124	    const ctx = this.ctx;
1125	    const ax = e.ai0 * 16 + 8, ay = e.ai1 * 16 + 8;
1126	    let px = e.cx, py = e.cy;
1127	    let dx = ax - px, dy = ay - py;
1128	    const rot = Math.atan2(dy, dx) - Math.PI / 2;   // :22438
1129	    let running = true;
1130	    while (running) {                               // :22441-22512
1131	      const dist = Math.hypot(dx, dy);
1132	      let seg = step;
1133	      if (dist < stop) { seg = dist - stop + step; running = false; }
1134	      if (dist > 0 && seg > 0) {
1135	        const k = seg / dist;
1136	        px += dx * k; py += dy * k;                 // 段心向锚点步进（:22454-22455）
1137	        dx = ax - px; dy = ay - py;
1138	        ctx.save();
1139	        ctx.translate(px, py);
1140	        ctx.rotate(rot);
1141	        // 源矩形取贴图顶部 seg 行，origin=贴图中心（:22504-22505 scale 1）
1142	        ctx.drawImage(chain.img, chain.sx, chain.sy, chain.sw, seg,
1143	          -chain.sw / 2, -chain.sh / 2, chain.sw, seg);
1144	        ctx.restore();
1145	      } else {
1146	        running = false;                            // 头贴锚点（dist≈0）不画段
1147	      }
1148	    }
1149	  }
1150	
1151	  private drawSkeletronArm(hand: Enemy, head: Enemy) {
1152	    if (this.armBoneImg === undefined) {
1153	      this.armBoneImg = new Image();
1154	      this.armBoneImg.src = 'sprites/vanilla/Arm_Bone.png';
1155	    }
1156	    const img = this.armBoneImg;
1157	    if (!img || !img.complete || img.naturalWidth === 0) return;
1158	    const ctx = this.ctx;
1159	    const ai0 = hand.ai0 >= 0 ? 1 : -1; // ai[0]：-1 左手 / 1 右手
1160	    // vector5 = 手部锚点（Main.cs:22545：position + width/2 - 5*ai[0], +20）
1161	    let vx = hand.x + hand.w / 2 - 5 * ai0;
1162	    let vy = hand.y + 20;
1163	    for (let j = 0; j < 2; j++) {
1164	      // num14/num15 = 头中心（position + w/2, +h/2）相对锚点的向量（Main.cs:22547-22548）
1165	      let dx = head.x + head.w / 2 - vx;
1166	      let dy = head.y + head.h / 2 - vy;
1167	      let k: number;
1168	      if (j === 0) { dx -= 200 * ai0; dy += 130; const len = Math.hypot(dx, dy) || 1; k = 92 / len; }
1169	      else { dx -= 50 * ai0; dy += 80; const len = Math.hypot(dx, dy) || 1; k = 60 / len; }
1170	      vx += dx * k; vy += dy * k;
1171	      const rot = Math.atan2(dy, dx) - Math.PI / 2; // Main.cs:22572
1172	      ctx.save();
1173	      ctx.translate(vx, vy);
1174	      ctx.rotate(rot);
1175	      ctx.drawImage(img, -img.naturalWidth / 2, -img.naturalHeight / 2);
1176	      ctx.restore();
1177	      if (j === 0) { vx += dx * k / 2; vy += dy * k / 2; } // Main.cs:22587 段间推进
1178	    }
1179	  }
1180	
1181	  /**
1182	   * NPC 血条 1:1（Main.DrawHealthBar Main.cs:21748-21839 + 显示门
1183	   * DrawInterface_14_EntityHealthBars :45223：life != lifeMax && !dontTakeDamage——
1184	   * 掉血即常驻显示、满血隐藏；immortal 实体血量恒满自动排除）。
1185	   * Hb1/Hb2 贴图未入素材管线——几何绘制同布局：总宽 36px（scale=1）、填充 min 3px、
1186	   * Y=实体脚下（settings=1 经典锚点 position.Y+height+NPCAddHeight）、
1187	   * 颜色公式 :21771-21810（ratio-0.1 → >0.5 绿 r=255*(1-n)*2 / 否则红 g=255*n*2，b=0，
1188	   * ×0.95 alpha；前景/背景同色 tint 靠明度区分）
1189	   */
1190	  private drawEnemyHpBar(e: { hp: number; maxHp: number; cx: number; y: number; h: number }) {
1191	    if (e.hp <= 0 || e.hp >= e.maxHp) return;
1192	    const ctx = this.ctx;
1193	    let r = e.hp / e.maxHp;
1194	    if (r > 1) r = 1;
1195	    const fill = Math.min(36, Math.max(3, Math.floor(36 * r)));  // num2：填充宽（min 3）
1196	    const x = Math.round(e.cx - 18);                             // num3 = X - 18*scale
1197	    const y = Math.round(e.y + e.h);                             // 实体脚下（经典锚点）
1198	    const n = r - 0.1;                                           // ratio 偏移（:21771）
1199	    const cr = n > 0.5 ? Math.round(255 * (1 - n) * 2) : 255;

```


---

## 🤖 Assistant · 2026-08-11T07:14:48.731Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Main.cs\\|Main\\.cs\\|NPC.cs\\|NPC_1\\|Drawing.cs\\|Projectile.cs\\|Item.cs\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -60",
 "description": "Find vanilla source references in Renderer.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:48.753Z

**📎 ToolResult**

```
43:/** 原版 holdStyle!=0 物品集（Item.cs SetDefaults holdStyle=1 实证 + TEdit 实名核对）：
67:// ============ 原版 FindFrame 分族帧引擎（1.4.5.6 Terarria1456/Terraria/NPC.cs:67295+） ============
449:    // 2. chunks 绘制序列（对照原版 Main.cs 帧序：背景水 → 墙 → 方块 → 瀑布 → 实体 → 前景水）
457:    // 2a. 液体背景 pass（原版 backWaterTarget 先于墙合成，Main.cs:46619）：
480:    // 2c'. 导线覆盖层(原版画在水之上实体之下,Main.cs:46721;手持电路工具或 F7 时可见)
485:    // 2d. 瀑布贴图（原版画在 tile 层后、实体前，Main.cs:47460，被地形遮挡）
494:    // 3.5 入驻旗帜（Main.cs:40152 DrawNPCHousesInWorld：有家 NPC 在家坐标上方
522:    // 4.5 液体前景 pass（原版 waterTarget 在玩家/掉落物之后合成，Main.cs:46720）：
614:    // 入侵进度条（DrawInvasionProgress Main.cs:47071 语义；布局与 Boss 条并列居中，
629:    // 底边 +5 行（原版 Main.cs:42900-42908 屏下 +5/+4 边距）：P3 不处理窗口底部 10 行，
636:  /** 导线覆盖层(Main.cs:43543-43954 DrawWires 移植:四色行/连接掩码/多色淡化/致动器覆盖) */
663:          const bit = 1 << c; // 红0 蓝1 绿2 黄3(图集行序,Main.cs:43641 等)
666:          // 行 Y = 色行*18;分线盒/像素盒额外行偏移(Main.cs:43596-43616)
671:          // 连接掩码(Main.cs:43621-43640):上+18 右+36 下+72 左+144
858:    // 骷髅王手（36）的两节臂骨 IK（Main.cs:22543-22596 1:1）：从手部锚点向头
861:    // AI_013 食人怪族茎蔓（Main.cs:22433-22514 1:1）：头中心 → 锚点格(ai0/ai1)
874:        // 锚点:飞行型=帧中心(原版默认分支 Main.cs:23635 语义);地面型=底锚+逐帧
924:        // 原版 color 二次绘制（Main.cs:24527 + NPC.GetColor L94903）：color≠default 时用
943:        // 史莱姆王体内忍者（Main.cs:22798-22818 1:1）：独立贴图 Ninja.png 叠画在
957:          // 头顶金冠（Main.cs:25571-25595 case 50，1:1）：贴图 Extra_39（82×56，
1105:  /** AI_013 植物/攀爬者族茎蔓（Main.cs:22433-22514 1:1）：从 NPC 中心向锚点格
1114:    // num7/num8：段长/终止距离（Main.cs:22442-22447）
1160:    // vector5 = 手部锚点（Main.cs:22545：position + width/2 - 5*ai[0], +20）
1164:      // num14/num15 = 头中心（position + w/2, +h/2）相对锚点的向量（Main.cs:22547-22548）
1171:      const rot = Math.atan2(dy, dx) - Math.PI / 2; // Main.cs:22572
1177:      if (j === 0) { vx += dx * k / 2; vy += dy * k / 2; } // Main.cs:22587 段间推进
1182:   * NPC 血条 1:1（Main.DrawHealthBar Main.cs:21748-21839 + 显示门
1214:  /** 入驻旗帜（Main.cs:40152-40236 DrawNPCHousesInWorld 1:1）：
1244:      // num9=18；实心格是平台（tile 19）时 -8（Main.cs:40212-40214）——
1250:      // 头像叠画（原版 TownNPCProfiles/TypeToDefaultHeadIndex NPC.cs:7489——head 索引≠NPC id）
1302:    // 注意：不再回退 Maples 角色/NPC_1.png——那是原版绿史莱姆贴图（Maples 沿用原版命名），
1576:   *  （GetColor 二次绘制语义，Main.cs:24986 / NPC.cs:94903） */
1707:  /** 小地图缩放（原版 mapMinimapScale，默认 1.05；钳 0.2..3，Main.cs:54953-54959） */
1738:    // 原版锚点（Main.cs:54696-54706 UpdateMinimapAnchors + 54944-54949，MapScale=1）：

```


---

## 🤖 Assistant · 2026-08-11T07:14:51.251Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the paper doll section (drawPlayer around 1331-1510), the findFrame engine at line 67, drawTownNPC at 1296, and the entities with draw() methods. Also need to check Enemy.ts for AI family comments claiming 1:1, and the bossAI files for draw().

Let me read more of Renderer.ts: paper doll part 1331-1510 and drawTownNPC, drawCritter, drawHouseBanners. And the FindFrame engine at 67.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:51.459Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 100,
 "offset": 1
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:51.472Z

**📎 ToolResult**

```
1	// 主渲染器：天空 → chunk → 液体 → 实体 → 粒子/飘字 → 光照合成 → 小地图
2	import { TILE, CHUNK } from '../core/constants';
3	import type { Camera } from './Camera';
4	import { SkyRenderer } from './SkyRenderer';
5	import { ChunkCache } from './ChunkCache';
6	import type { World, Clock } from '../world/World';
7	import type { AssetBundle } from '../assets/AssetGen';
8	import type { SpriteAtlas } from '../assets/SpriteAtlas';
9	import { atlasIconForKey, VANILLA_ITEM_ICON_MAP } from '../assets/SpriteAtlas';
10	import { TOOL_CUTTER } from '../world/Wiring';
11	import { compositePaperDoll, dollFrame } from '../player/PaperDoll';
12	import type { Inventory } from '../items/Inventory';
13	import { VanillaResourceBars } from './ResourceBars';
14	import type { FlickerClock } from '../lighting/SkyColor';
15	
16	/** 装备 → 纸娃娃渲染参数。贴图索引 = item.head/body/legs 槽位序号（原版语义，
17	 *  非物品 id——铁甲三件的槽位序号都是 2）；原版物品 id 经 vanilla.json armorIndex 查表 */
18	function dollEquipFromInv(inv: Inventory, atlas: import('../assets/SpriteAtlas').SpriteAtlas | null): { head: number | null; body: number | null; legs: number | null } {
19	  const idx = (itemId: number | null | undefined): number | null => {
20	    if (itemId == null) return null;
21	    const def = ITEM_DEFS[itemId];
22	    if (!def?.armor) return null;
23	    const key = def.key;
24	    const vid = VANILLA_ITEM_ICON_MAP[key] ?? (key.startsWith('vi_') ? parseInt(key.slice(3), 10) : NaN);
25	    if (!Number.isFinite(vid)) return null;
26	    const entry = atlas?.vanilla.armorIndex?.[String(vid)];
27	    if (!entry) return null;
28	    const slot = def.armor.slot; // 0头 1胸 2腿
29	    return slot === 0 ? (entry.head || null) : slot === 1 ? (entry.body || null) : (entry.legs || null);
30	  };
31	  const disp = inv.displayArmor();
32	  return { head: idx(disp[0]), body: idx(disp[1]), legs: idx(disp[2]) };
33	}
34	import { WeatherRenderer } from './WeatherRenderer';
35	import { drawVanillaLiquids } from './VanillaLiquidRenderer';
36	import { WaterfallRenderer } from './WaterfallRenderer';
37	import { BiomeBackground } from './BiomeBackground';
38	import type { SceneFlags } from '../world/SceneMetrics';
39	import { TILE_DEFS, WALL_DEFS } from '../data/tiles';
40	import { viIdFromKey } from '../data/vanillaItemCombat';
41	import { drawEmotes } from './EmoteBubble';
42	
43	/** 原版 holdStyle!=0 物品集（Item.cs SetDefaults holdStyle=1 实证 + TEdit 实名核对）：
44	 *  火把族（8/彩色 427-433/群系 523..5353）+ 荧光棒族 ItemID.Sets.Glowsticks(282,286,3112,3002,4776,5643)。
45	 *  PlayerDrawLayers.cs:3857：holdStyle!=0 → 静持也渲染（手臂抬起） */
46	const HOLD_STYLE_ITEMS = new Set([
47	  8, 427, 428, 429, 430, 431, 432, 433, 523, 974, 1245, 1333, 2274, 3004, 3045, 3114,
48	  4383, 4384, 4385, 4386, 4387, 4388, 5293, 5353,
49	  282, 286, 3112, 3002, 4776, 5643,
50	]);
51	import { Lang } from '../i18n/Lang';
52	import { ITEM_DEFS } from '../data/items';
53	import { townExtraFrames, TOWN_NPC_HEAD_INDEX } from '../data/vanillaNpcs';
54	import type { Player } from '../entities/Player';
55	import { Enemy } from '../entities/Enemy';
56	import { ItemDrop } from '../entities/ItemDrop';
57	import { TownNPC } from '../entities/TownNPC';
58	import { Tombstone, getTombstoneCanvas } from '../entities/Tombstone';
59	import { Critter } from '../entities/Critter';
60	import type { Entity } from '../entities/Entity';
61	
62	export interface Particle { x: number; y: number; vx: number; vy: number; life: number; maxLife: number; color: string; size: number; damp?: number; grav?: number; }
63	
64	// 光照合成 4-tap 标量缓冲(替代每像素 [r,g,b] 元组,2026-08 审计 G2)
65	const _lightTap = new Uint8Array(12);
66	
67	// ============ 原版 FindFrame 分族帧引擎（1.4.5.6 Terarria1456/Terraria/NPC.cs:67295+） ============
68	// 僵尸族 case 3（L77026）：腾空/逆向→帧2；站定→帧0；行走 counter+=|vx| 按 8/16/24/32 → 0,1,2,1 往复
69	const ZOMBIE_FRAME_TYPES = new Set([3, 52, 53, 132, 161, 186, 187, 188, 189, 200, 223, 251, 254, 255, 319, 320, 321, 331, 332, 342, 536, 590, 691]);
70	// 蝙蝠族 case 49（L75523→148 块 L75585）：每 6 tick 推进；49/51/60/634 循环到倒数第 2 帧（末帧=挂机姿势）
71	const BAT_SKIP_LAST = new Set([49, 51, 60, 634]);
72	// 旋转族 NPC（原版 npc.rotation 驱动绘制朝向；FindFrame 不做朝向翻转）：
73	// 35/68=骷髅王头/守卫、113-115=血肉墙/之眼/饥饿者、125/126=双子、127-131=Prime 头+四部件、
74	// 134-136=毁灭者链、261-265=世花族(孢子/本体/钩蔓/触须)、370=猪鲨、396/397=月总头/手、657=史莱姆皇后(飞行倾斜)
75	const ROTATION_NPC = new Set([35, 68, 113, 114, 115, 125, 126, 127, 128, 129, 130, 131, 134, 135, 136, 246, 247, 248, 249, 261, 262, 263, 264, 265, 370, 396, 397, 657]);
76	
77	/** 按原版 FindFrame 分族规则算当前帧 index */
78	function vanillaFrameIdx(e: Enemy, frames: number): number {
79	  const id = e.vanillaId ?? 0;
80	  const ai = e.vanilla?.aiStyle ?? 0;
81	  const t = e.animT; // tick 计数（≈原版 frameCounter 驱动源）
82	  const walking = Math.abs(e.vx) > 0.05;
83	  // 僵尸族（L77049-77085）：行走 0,1,2,1 按 |vx| 累加；腾空=2；站定=0
84	  if (ZOMBIE_FRAME_TYPES.has(id)) {
85	    if (!e.onGround) return Math.min(2, frames - 1);
86	    if (!walking) return 0;
87	    const phase = (e.walkCycleT + Math.abs(e.vx) * 8) % 32; // 每 tick +|vx|，32 一循环
88	    return phase < 8 ? 0 : phase < 16 ? 1 : phase < 24 ? 2 : 1;
89	  }
90	  // 栖息态 NPC（秃鹫 61 cs:24082 ai[0]=0 栖息 / 宝箱怪 85 族 cs:25645 ai[0]=0 伪装）：
91	  // 静止帧 0；激活后从帧 1 起循环
92	  if (ai === 17 || ai === 25) {
93	    if ((e as Enemy & { ai0: number }).ai0 === 0) return 0;
94	    return frames > 1 ? 1 + Math.floor(t / 8) % (frames - 1) : 0;
95	  }
96	  // 爬墙蜘蛛族（FindFrame case 165/237/238/240/531, cs:73795-73817）：
97	  // frameCounter += (|vx|+|vy|)×0.5（531 ×0.4），24 一循环 4 帧
98	  if (ai === 40) {
99	    return Math.floor(((e.crawlT ?? 0) / 6)) % frames;
100	  }

```


---

## 🤖 Assistant · 2026-08-11T07:14:52.228Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"draw(\\s*)\\|draw(\\|override draw\" ~/Project/GLM/SandboxWorld/game/src/entities/*.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI*.ts 2>/dev/null | grep -i \"draw\" | head -60",
 "description": "Find draw methods in entities"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:52.273Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:64:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:73:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:176:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Critter.ts:298:  draw() { /* Renderer 统一绘制 */ }
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:82:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts:22:  abstract draw(r: Renderer, cam: Camera): void;
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3298:  draw() { /* Renderer 统一绘制 */ }
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts:29:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:929:  draw() { /* 由 Renderer 统一绘制 */ }
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts:24:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:120:  draw() { /* Renderer 统一绘制 */ }
~/Project/GLM/SandboxWorld/game/src/entities/Tombstone.ts:128:  draw() { /* Renderer 统一绘制 */ }
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:219:  draw() { /* Renderer 统一绘制 */ }
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:103:  draw(r: Renderer, cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:174:  draw(r: Renderer, cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:230:  draw(r: Renderer, cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:316:  draw(r: Renderer, cam: Camera): void {

```


---

## 🤖 Assistant · 2026-08-11T07:14:56.319Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now, entities with draw(): Arrow, Dart (two classes), FallingBlock, MagicProj, Minecart, WeaponProj (multiple classes). These are projectiles rather than enemies, but they're entities with special draw. The user asked about "敌怪/实体特殊绘制" — enemy/entity special drawing. Let me look at these files, plus WeaponProj, and the paper doll (player/PaperDoll.ts) and drawPlayer in Renderer.

Also I should check Enemy.ts for AI family comments claiming 1:1, particularly AI_013 plantAI, AI_011/12 skeletron, AI_047 golem — multi-part families.

Also check the bossAI*.ts files for draw-related comments (they probably only have AI, but check for draw hooks).

Let me parallelize: read Enemy.ts AI routing section (around 300-400), plantAI at 1590, skeletron at 1833, golem fist AI. Also grep Enemy.ts for all "1:1" / "一比一" claims with AI numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:56.979Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AI_0[0-9][0-9]\\|1:1\\|一比一\\|一一对应\\|cs:\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | grep -i \"1:1\\|一比一\" ",
 "description": "List all 1:1 claims in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:57.008Z

**📎 ToolResult**

```
655:  // ai[1] = 体内物品 id → 目标色表（蛆/凝胶/铂金币等占位色的 1:1 表）；踩油漆色 lerp 暂缺（无油漆系统）
903:  /** NPCCanStickToWalls 1:1（NPC.cs:56209-56229）：身体中心 3×3 内"非实心 tile 且有背景墙"
922:  /** Transform 1:1（NPC.cs:81861-81919）：换类型 + 按比例结转 HP + ai[0..3] 清零；
959:  /** AI_040 爬墙蜘蛛族 1:1（NPC.cs:29784-30022）：无重力、贴背景墙表面爬行。
1058:  /** AI_042 失落女孩 1:1（NPC.cs:30281-30310）：伪装成无害 NPC 静止站立（无移动逻辑，
1590:  /** AI_013 植物/攀爬者族(NPC.cs:22604-22700 一比一):锚点格(ai0/ai1)固定,
2206:   *  各家族原版行为（蚱蜢 ai1 跳/鸟 ai24 飞/蚯蚓 ai66 爬）后续逐族 1:1，先统一温和地面行为 */
2330:  /** 小动物路由：按 aiStyle 精确分流到各家族 1:1 实现（AI_001/016 复用既有精确 AI） */
2941:   * AI_004 克苏鲁之眼 1:1（1456 NPC.cs:19909-20757，普通模式数值；专家分支未启用）。

```


---

## 🤖 Assistant · 2026-08-11T07:14:57.186Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 110,
 "offset": 300
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:57.193Z

**📎 ToolResult**

```
300	      this.y += this.vy;
301	      this.onGround = Math.abs(this.vy) < 0.6;
302	      if (Math.abs(this.vx) > 0.05) this.walkCycleT += Math.abs(this.vx);
303	      if (this.iframes > 0) this.iframes--;
304	      return;
305	    }
306	    this.aiT++;
307	    if (this.iframes > 0) this.iframes--;
308	    if (this.justHitT > 0) this.justHitT--;
309	    this.lightRGB = null; // 点光由 AI 每帧重写（不残留上一帧状态）
310	    if (this.hpBarT > 0) this.hpBarT--;
311	    if (this.squash !== 0) this.squash *= 0.85;
312	    this.animT++;
313	    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
314	
315	    // EoW 族出生渐显（每 tick alpha-1;原版 AI_006）——静态半透明不受影响
316	    if (this.alphaFade) {
317	      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
318	      if (this.spawnAlpha === 0) this.alphaFade = false;
319	    }
320	
321	    const player = (game as unknown as { player: Player }).player;
322	    const hasPlayer = !!player && !player.dead;
323	
324	    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
325	    // 蠕虫身体段（wormFollow 非空）无 AI：位置由头部 wormAI 沿链驱动，但仍走共享尾段（接触伤害等）
326	    // 小动物（critter）优先走被动游荡，绝不落入 default 的追击 fallback
327	    if (this.vanilla && !this.wormFollow && this.vanilla.critter) {
328	      this.critterWanderAI(game, hasPlayer ? player : null);
329	    } else if (this.vanilla && !this.wormFollow) {
330	      const p = hasPlayer ? player : null;
331	      switch (this.vanilla.aiStyle) {
332	        case 92: this.dummyAI(game); break;                            // AI_092 训练假人（NPC 488）
333	        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
334	        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
335	        case 3: this.fighterAI(game, p); break;                        // AI_003 战士族（原版通用核）
336	        // EoC 传参例外:玩家死亡也要传原对象(cs:19931 dead 判定走逃离分支,
337	        // 冲刺计时合法冻结;传 null 会让 aiT 照走、状态机停摆 → 首冲时长翻倍)
338	        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
339	        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
340	        case 6: this.wormAI(game, p); break;                           // AI_006 蠕虫族（头）
341	        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
342	        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
343	        case 11:
344	          // 68 守卫走专用分支（bossAI.skeletronBossAI 注释"守卫分支已在 skeletronHeadAI"
345	          // 即此拆分：守卫恒速追击与骷髅王战斗状态机互不混用）
346	          if (this.vanillaId === 68) this.dungeonGuardianAI(game, p);
347	          else skeletronBossAI(this, game, p);
348	          break;                                                         // AI_011 骷髅王头战斗核/地牢守卫
349	        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
350	        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
351	        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
352	        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）
353	        case 16: this.swimAI(game, p); break;                           // AI_016 游泳族（鲨鱼/食人鱼）
354	        case 18: this.jellyfishAI(game, p); break;                      // AI_018 水母族（脉冲游动）
355	        case 22: this.ghostAI(game, p); break;                          // AI_022 幽灵族（穿墙缓速）
356	        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
357	        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
358	        case 54: brainOfCthulhuAI(this, game, p); break;                  // AI_054 克脑(爬行者环→瞬移冲刺)
359	        case 55: creeperAI(this, game, p); break;                         // AI_055 爬行者(环绕漂移)
360	        case 30: twinsAI(this, game, p, false); break;                    // AI_030 雷神之眼 125(悬浮/连冲/变身/激光)
361	        case 31: twinsAI(this, game, p, true); break;                     // AI_031 魔神之眼 126(诅咒焰/火焰喷射)
362	        case 32: skeletronPrimeAI(this, game, p); break;                  // AI_032 机械骷髅王头 127(4 部件/旋冲/白天狂暴)
363	        case 33: case 34: case 35: case 36: primePartAI(this, game, p); break; // AI_033-036 Prime 部件(锯/激光/钳/炮)
364	        case 37: destroyerAI(this, game, p); break;                       // AI_037 毁灭者 134(80 段链穿地/探针激光)
365	        case 27: wallOfFleshAI(this, game, (game as unknown as { player: Player }).player ?? null); break; // AI_027 血肉墙(空腔扫描/速度血量档/Leech 轮)
366	        case 28: wofEyeAI(this, game, p); break;                          // AI_028 血肉墙之眼(钉墙吸附/激光连射 83)
367	        case 29: hungryAI(this, game, p); break;                          // AI_029 饥饿者(挂墙环绕→受击脱落扑咬)
368	        case 84: lunaticCultistAI(this, game, p); break;                  // AI_084 拜月教邪教徒(瞬移+四系弹幕轮换)
369	        case 120: empressOfLightAI(this, game, p); break;                 // AI_120 光之女皇(连段选招/半血变身)
370	        case 121: queenSlimeAI(this, game, p); break;                     // AI_121 史莱姆皇后(走路四连跳→飞行二阶段)
371	        case 100: ancientLightAI(this, game, p); break;                  // AI_100 远古之光 522(直飞投射物型)
372	        case 101: ancientDoomAI(this, game, p); break;                  // AI_101 远古末日 523(锚邪教徒蓄能自爆)
373	        case 43: queenBeeAI(this, game, p); break;                        // AI_043 蜂后(悬浮俯冲/蜜蜂机枪/毒刺)
374	        case 50: planteraHookAI(this, game, p); break;                    // AI_050 真菌孢子 261/孢子 265
375	        case 51: planteraAI(this, game, p); break;                        // AI_051 世纪之花(钩蔓牵引→二阶段)
376	        case 52: planteraTentacleAI(this, game, p); break;                // AI_052 钩蔓 263(抓墙换锚收线)
377	        case 53: planteraTentacle2AI(this, game, p); break;               // AI_053 触须 264(二阶段环绕)
378	        case 69: dukeFishronAI(this, game, p); break;                     // AI_069 猪鲨(冲撞/泡泡/龙卷,半血变身)
379	        case 70: dukeBubbleAI(this, game, p); break;                      // AI_070 爆裂泡泡 371
380	        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
381	        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
382	        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
383	        case 45: golemAI(this, game, p); break;                        // AI_045 石巨人本体 245(蓄力跳/挂头无敌)
384	        case 46: golemHeadAI(this, game, p); break;                      // AI_046 挂载头 246(锚本体/火焰弹眼激光;249 自由态)
385	        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
386	        case 40: this.wallCreeperAI(game, p); break;                      // AI_040 爬墙蜘蛛族（贴背景墙爬行+形态互转）
387	        case 42: this.lostGirlAI(game, p); break;                         // AI_042 失落女孩（伪装静止→Nymph 变身 cs:30281-30310）
388	        case 0: this.boundNPCAI(game, p); break;                          // AI_000 被缚NPC（cs:19774 站立/水上漂流；Enemy 侧防御，常规走 TownNPC.bound）
389	        case 17: this.vultureAI(game, p); break;                          // AI_017 秃鹫（cs:24079 栖息→200px盒/受击起飞，单向不回落）
390	        case 19: this.antlionAI(game, p); break;                          // AI_019 蚁狮（cs:24465 扎沙不动+沙球；传送带特例略）
391	        case 23: this.flyingWeaponAI(game, p); break;                     // AI_023 飞行武器（cs:25316 冲/漂100/转120 循环，受击回蓄转）
392	        case 25: this.mimicAI(game, p); break;                            // AI_025 宝箱怪（cs:25621 伪装200px盒→小小大跳循环）
393	        case 39: this.tortoiseAI(game, p); break;                         // AI_039 陆龟族（cs:29257 待机蓄力→蓄势→旋冲→恢复）
394	        case 41: this.herplingAI(game, p); break;                         // AI_041 赫柏林/德普林（cs:30017 低跳连扑；378 炸弹自爆略）
395	        case 44: this.flyingSwarmerAI(game, p); break;                    // AI_044 飞鱼/蚁狮蜂（cs:30999 分轴限速追+失视逃逸）
396	        case 56: this.dungeonSpiritAI(game, p); break;                    // AI_056 地牢之魂（cs:32915 穿墙0.99惯性追踪）
397	        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
398	        case 107: this.chargerAI(game, p, 1); break;                    // AI_107 ImprovedWalkers（0.07/±1.0 walker 档，NPC.145.cs:43153 引擎核同构）
399	        default: this.zombieAI(game, p); break;                        // 其余家族待逐个移植
400	      }
401	    } else switch (this.key) {
402	      case 'slime_green':
403	      case 'slime_blue': this.slimeAI(game, hasPlayer ? player : null); break;
404	      case 'zombie': this.zombieAI(game, hasPlayer ? player : null); break;
405	      case 'demon_eye':
406	      case 'cave_bat': this.flyAI(game, hasPlayer ? player : null, 0.09); break;
407	      case 'servant_of_cthulhu': this.flyAI(game, hasPlayer ? player : null, 0.22); break;
408	      case 'eye_of_cthulhu': this.eocAI(game, player ?? null); break;
409	    }

```


---

## 🤖 Assistant · 2026-08-11T07:14:58.930Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the plantAI (1590), and the multi-part families' comments — AI_011/12 skeletron (1833-), AI_047 golem fist. Also bossAI.ts headers for skeletron, and bossAI_golem.ts golemFistAI. Let me get those.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:14:59.150Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 130,
 "offset": 1585
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:14:59.159Z

**📎 ToolResult**

```
1585	   *  目标方向 8px 网格量化 → 期望速度 = 归一化方向 × maxSpd；
1586	   *  ai[0] 环绕摆动（>0 加 vy、|>100| 加 vx，±200 循环）产生盘旋蜂群感（L17742-17752）；
1587	   *  近距(<150) 附加 0.007×期望速度制导（L17754-17757）；
1588	   *  各轴以 accel 步进逼近期望速度（L17774-17789）。
1589	   *  速度表（L17610-17617）：Eater of Souls(6)/Crimera(173) 4/0.02，默认 6/0.05 */
1590	  /** AI_013 植物/攀爬者族(NPC.cs:22604-22700 一比一):锚点格(ai0/ai1)固定,
1591	   *  朝玩家伸展(range 内钳制),逆向加速 ×1.5;锚点格被挖掉即死;300-450 tick 周期 range ×1.3。
1592	   *  攀爬者 101: range 175、accel 0.035、noTileCollide 幽灵位移(穿墙摆动)。 */
1593	  private plantAI(game: GameHooks, player: Player | null) {
1594	    const st = game.world.store;
1595	    // 锚点格失活 → 死亡(原版 :22608-22620)
1596	    if (this.ai0 < 0 || this.ai1 < 0 || !st.inBounds(this.ai0, this.ai1)
1597	      || st.type[st.idx(this.ai0, this.ai1)] === 0) {
1598	      this.dead = true;
1599	      return;
1600	    }
1601	    let range = 150;  // 默认 num218(:22632)；族内覆盖(:22636-22658)
1602	    let accel = 0.035; // num217(:22630)
1603	    if (this.vanillaId === 43) range = 250;          // 食人怪（getGoodWorld 350 未接入）
1604	    else if (this.vanillaId === 101) range = 175;    // 邪恶触手
1605	    else if (this.vanillaId === 259) range = 100;    // 真菌球
1606	    else if (this.vanillaId === 175) { range = 500; accel = 0.05; }   // 怒牙捕兽草
1607	    else if (this.vanillaId === 260) { range = 350; accel = 0.15; }   // 巨型真菌球
1608	    // ai2:300-450 tick 周期 → range ×1.3(:22644-22653)
1609	    this.ai2 += 1;
1610	    if (this.ai2 > 300) {
1611	      range = Math.floor(range * 1.3);
1612	      if (this.ai2 > 450) this.ai2 = 0;
1613	    }
1614	    const ax = this.ai0 * 16 + 8, ay = this.ai1 * 16 + 8;
1615	    // 目标点 = 锚点 + 朝玩家偏移(钳制在 range 内,:22655-22665)
1616	    let ox = 0, oy = 0;
1617	    if (player) {
1618	      ox = player.cx - this.w / 2 - ax;
1619	      oy = player.cy - this.h / 2 - ay;
1620	      const d = Math.hypot(ox, oy);
1621	      if (d > range) { ox = ox / d * range; oy = oy / d * range; }
1622	    }
1623	    // 各轴逼近,逆向 ×1.5(:22666-22699)
1624	    const tx = ax + ox, ty = ay + oy;
1625	    if (this.x < tx) {
1626	      this.vx += accel;
1627	      if (this.vx < 0 && ox > 0) this.vx += accel * 1.5;
1628	    } else if (this.x > tx) {
1629	      this.vx -= accel;
1630	      if (this.vx > 0 && ox < 0) this.vx -= accel * 1.5;
1631	    }
1632	    if (this.y < ty) {
1633	      this.vy += accel;
1634	      if (this.vy < 0 && oy > 0) this.vy += accel * 1.5;
1635	    } else if (this.y > ty) {
1636	      this.vy -= accel;
1637	      if (this.vy > 0 && oy < 0) this.vy -= accel * 1.5;
1638	    }
1639	    this.facing = this.vx > 0 ? 1 : -1;
1640	    // ---- 爬行者 101 诅咒焰（cs:22823-22856）：ai[3] 每 tick +1，≥120 且自身未嵌实心
1641	    // 且有视线 → 喷诅咒焰（速 10、伤 22、散布 ±10）；条件不满足回退 ai[3]=100（20t 重试）
1642	    if (this.vanillaId === 101 && player && !player.dead) {
1643	      this.ai3 += 1;
1644	      if (this.ai3 >= 120) {
1645	        let embedded = false;
1646	        for (let tx = Math.floor(this.x / TILE); tx <= Math.floor((this.x + this.w - 0.01) / TILE) && !embedded; tx++) {
1647	          for (let ty = Math.floor(this.y / TILE); ty <= Math.floor((this.y + this.h - 0.01) / TILE); ty++) {
1648	            if (st.isSolid(tx, ty)) { embedded = true; break; }
1649	          }
1650	        }
1651	        if (!embedded && this.canSeePlayer(st, player)) {
1652	          this.shootDart(game, this.cx, this.cy,
1653	            player.cx - this.cx + (Math.random() * 20 - 10),
1654	            player.cy - this.cy + (Math.random() * 20 - 10), 10, 22);
1655	          this.ai3 = 0;
1656	        } else this.ai3 = 100;
1657	      }
1658	    }
1659	    // noTileCollide:幽灵位移(原版 plants 不做 tile 碰撞)
1660	    this.x += this.vx;
1661	    this.y += this.vy;
1662	  }
1663	
1664	  private swarmerAI(game: GameHooks, player: Player | null) {
1665	    const isEater = this.vanillaId === 6 || this.vanillaId === 173 || this.vanillaId === 139;
1666	    // 蜜蜂（210/211，L50768-50784）：ai[1] 计数爬坡 num3=(ai1-60)/60≤1；
1667	    // 暖机期（num3<1）逐轴速度钳 ±6；速度档 5 / 加速 0.1×num3
1668	    const isBee = this.vanillaId === 210 || this.vanillaId === 211;
1669	    let maxSpd = isEater ? 4 : this.vanillaId === 94 ? 4.2 : this.vanillaId === 5 ? 5 : 6;
1670	    let accel = isEater ? 0.02 : this.vanillaId === 94 ? 0.022 : this.vanillaId === 5 ? 0.03 : 0.05;
1671	    if (isBee) {
1672	      this.ai1 += 1;
1673	      let ramp = (this.ai1 - 60) / 60;
1674	      if (ramp > 1) ramp = 1;
1675	      else if (this.vx > 6) this.vx = 6;
1676	      else if (this.vx < -6) this.vx = -6;
1677	      if (ramp < 1) {
1678	        if (this.vy > 6) this.vy = 6;
1679	        else if (this.vy < -6) this.vy = -6;
1680	      }
1681	      maxSpd = 5;
1682	      accel = 0.1 * ramp;
1683	    }
1684	    // flag4（L50829）：非 173/6/42/231-235/94/139/619 = 双步加速（蜂族真；eater 族假）
1685	    const vid = this.vanillaId ?? 0;   // swarmerAI 仅数据驱动路径可达，vanillaId 恒非空
1686	    const flag4 = !isEater && vid !== 94 && vid !== 619
1687	      && vid !== 42 && !(vid >= 231 && vid <= 235) && vid !== 139;
1688	    const tx = player ? player.cx : this.cx + this.facing * 100;
1689	    const ty = player ? player.cy : this.cy - 100;
1690	    // 8px 网格量化（L17705-17710）
1691	    const dx = Math.floor(tx / 8) * 8 - Math.floor(this.cx / 8) * 8;
1692	    const dy = Math.floor(ty / 8) * 8 - Math.floor(this.cy / 8) * 8;
1693	    const dist = Math.hypot(dx, dy) || 1;
1694	    const sx = (dx / dist) * maxSpd;
1695	    const sy = (dy / dist) * maxSpd;
1696	    // 摆动项（L50837-50848）：num8 族（6/139/173/205）需 dist>100；flag3 族
1697	    // （42/94/619/176/210/211/231-235，含蜜蜂）无条件摆动
1698	    const swarmGated = isEater || this.vanillaId === 205;
1699	    const swarmAlways = vid === 42 || vid === 94 || vid === 619
1700	      || vid === 176 || isBee || (vid >= 231 && vid <= 235);
1701	    if ((swarmGated && dist > 100) || swarmAlways) {
1702	      this.ai0 += 1;
1703	      if (this.ai0 > 200) this.ai0 = -200;
1704	      this.vy += this.ai0 > 0 ? 0.023 : -0.023;
1705	      this.vx += Math.abs(this.ai0) > 100 ? 0.023 : -0.023;
1706	    } else if (swarmGated) {
1707	      this.ai0 = 0; // 近距无摆动
1708	    }
1709	    // 近距制导（6/94/173/619）
1710	    if (dist < 150 && (isEater || this.vanillaId === 94 || this.vanillaId === 619)) {
1711	      this.vx += sx * 0.007;
1712	      this.vy += sy * 0.007;
1713	    }
1714	    // 各轴步进逼近期望速度（L50924-50961）：flag4 族逆向时追加一步（num2 再乘一次）

```


---

## 🤖 Assistant · 2026-08-11T07:15:00.272Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"1:1\\|一比一\\|1:1移植\\|cs:\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_wof.ts | grep \"1:1\\|一比一\" | head -40",
 "description": "Find 1:1 claims in bossAI files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:00.303Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:1:// Boss AI 1:1 移植(Terarria1456 NPC.cs SetDefaults 指定 aiStyle 的专用核)。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:308:// 经典模式参数 1:1;专家/大师/FTW 分支仅注释保留。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts:1:// 石巨人 Boss 族 AI 1:1 移植(Terarria1456,1.4.5.6):
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts:7:// 经典模式主链 1:1;expert/getGoodWorld 分支保留注释;netcode/纯视觉尘(Gore/netOffset)跳过。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts:620:    // ---- 直飞追击(:19394-19446;原版无处置 ai[0]=3 的代码,保留 1:1) ----
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:1:// 蜂后 222(aiStyle 43,NPC.cs:30312-30998)+ 世纪之花族 1:1 移植(Terarria1456,1.4.5.6)。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:5:// 经典模式参数 1:1;expert/getGoodWorld 分支只注释保留;netcode(netUpdate/Main.netMode)跳过。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_wof.ts:1:// 血肉墙 Boss 族 1:1 移植(Terarria1456 NPC.cs ilspycmd 反编译,经典模式参数):
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:1:// 后期三大 Boss AI 1:1 移植(Terarria1456 = 1.4.5.6 反编译源码,经典模式主链):
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:929:// (当前邪教徒远古之光已收敛为 468 直飞弹,本核供数据完整性/未来 1:1 替换)
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:1:// Boss AI 1:1 移植(二):猪鲨鱼龙 AI_069(NPC 370)与月亮领主 aiStyle 77/78/79(NPC 398 核心 / 397 手 / 396 头)。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:9:// 经典模式主链 1:1;expert/getGoodWorld 分支保留注释;netcode 跳过。

```


---

## 🤖 Assistant · 2026-08-11T07:15:03.720Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now, let me look at the entity draw() methods: WeaponProj.ts (multiple classes), Dart.ts, Arrow.ts, MagicProj.ts, Minecart.ts, FallingBlock.ts. These are entity special draws. Also the paper doll drawPlayer part (1331-1510) and drawTownNPC and drawCritter, drawHouseBanners, drawDrop, drawTombstone.

Let me also check for other special drawing in Renderer: drawBossBar, drawInvasionBar maybe out of scope. The user focus is "敌怪/实体特殊绘制" - enemy/entity special drawing. So:
- Renderer.ts: drawEnemy (with special cases: skeletron arm, plant vine, KS ninja+crown, rotation families, color pass), drawPlantVine, drawSkeletronArm, drawEnemyHpBar, drawCritter, drawDrop, drawTombstone, drawTownNPC, drawHouseBanners, drawPlayer (paper doll)
- entities with own draw(): Arrow, Dart, MagicProj, Minecart, FallingBlock, WeaponProj classes
- player/PaperDoll.ts

Let me read these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:03.836Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:03.874Z

**📎 ToolResult**

```
1	// 数据驱动近战/爆炸武器投射物（1456 aiStyle 家族行为，Game.useCombatWeapon 派发）：
2	//   Boomerang  aiStyle 3   —— 飞出减速后返回主角（AI_003）
3	//   SpearProj  aiStyle 19/161 —— 随主角前刺伸缩（AI_019 的 owner 相对位移简化）
4	//   YoyoProj   aiStyle 99  —— 按住鼠标滞留追光标，松手收回（AI_099 channel 语义）；
5	//                              连枷 aiStyle 15 复用（甩链球近似，重力头由加速度兜住）
6	//   GrenadeProj aiStyle 16 —— 弹跳 + 引信爆炸（手雷 180/炸弹 150/炸药 135 tick）
7	// 贴图统一 Projectile_N.png 懒加载（Arrow.projSprite 共享缓存）。
8	import { Entity } from './Entity';
9	import { TILE } from '../core/constants';
10	import type { GameHooks } from './types';
11	import type { Renderer } from '../render/Renderer';
12	import type { Camera } from '../render/Camera';
13	import { projSprite } from './Arrow';
14	import { hitCritters, playEnemyHitSound } from './projTargets';
15	
16	/** 共用绘制：投射物贴图按角度旋转（贴图纵向，rotation = ang+π/2 与 AI_001 一致）。
17	 *  世界坐标绘制(Renderer 实体循环运行在世界变换内,勿再自算屏幕坐标) */
18	function drawProj(r: Renderer, _cam: Camera, e: { x: number; y: number; w: number }, projId: number, ang: number, fallbackColor: string): void {
19	  const ctx = r.canvas.getContext('2d');
20	  if (!ctx) return;
21	  const img = projSprite(projId);
22	  ctx.save();
23	  ctx.translate(e.x + e.w / 2, e.y + e.w / 2);
24	  ctx.rotate(ang);
25	  ctx.imageSmoothingEnabled = false;
26	  if (img && img.complete && img.naturalWidth > 0) {
27	    ctx.drawImage(img, -e.w / 2, -e.w / 2, e.w, e.w * (img.naturalHeight / img.naturalWidth));
28	  } else {
29	    ctx.fillStyle = fallbackColor;
30	    ctx.fillRect(-e.w / 2, -e.w / 2, e.w, e.w);
31	  }
32	  ctx.restore();
33	}
34	
35	/** 同敌命中去重 + 冷却的通用伤害结算。
36	 *  hitCd 记录每敌剩余冷却 tick，每 fixedUpdate 调用方先 tickCd() 递减；
37	 *  cooldown >= 9999 视作单次结算（突刺类：一击每敌只中一次） */
38	class HitCooldown {
39	  private map = new Map<number, number>();
40	  tick(): void {
41	    for (const [k, v] of this.map) {
42	      if (v <= 1) this.map.delete(k);
43	      else this.map.set(k, v - 1);
44	    }
45	  }
46	  ready(id: number, cooldown: number): boolean {
47	    if (this.map.has(id)) return false;
48	    if (cooldown < 9999) this.map.set(id, cooldown);
49	    else this.map.set(id, 2147483647); // 永不再中
50	    return true;
51	  }
52	  clear(): void { this.map.clear(); }
53	}
54	
55	function hitEnemies(
56	  self: { x: number; y: number; w: number; h: number; damage: number; knockback: number },
57	  game: GameHooks,
58	  hitCd: HitCooldown,
59	  cooldown: number,
60	  dirX: number,
61	): void {
62	  // 小动物:一击致死(原版小动物是 NPC;近战挥砍同语义)。回旋镖/悠悠球等穿透型
63	  // 命中小动物不消耗穿透语义——hurt 自带 iframes 防同帧连击
64	  hitCritters(self, game);
65	  for (const ent of game.enemies()) {
66	    const e = ent as unknown as { x: number; y: number; w: number; h: number; id: number; dead: boolean; hurt: (d: number, kx: number, ky: number, g: GameHooks) => boolean; def?: { hitSound?: string[] } };
67	    if (e.dead) continue;
68	    if (!(self.x < e.x + e.w && self.x + self.w > e.x && self.y < e.y + e.h && self.y + self.h > e.y)) continue;
69	    if (!hitCd.ready(e.id, cooldown)) continue;
70	    const crit = Math.random() < 0.04;
71	    const dmg = crit ? self.damage * 2 : self.damage;
72	    const kdir = Math.sign((e.x + e.w / 2) - (self.x + self.w / 2)) || dirX;
73	    playEnemyHitSound(game, e);
74	    e.hurt(dmg, kdir * self.knockback * 0.65, -2.5, game);
75	    game.addDamageNumber(self.x + self.w / 2, self.y, Math.round(dmg), crit, crit ? '#FFD040' : '#FF7060');
76	  }
77	}
78	
79	// ================= 回旋镖（aiStyle 3，AI_003） =================
80	
81	export class Boomerang extends Entity {
82	  w = 22; h = 22; // 原版 SetDefaults（type 6：22×22）
83	  damage: number;
84	  knockback: number;
85	  projId: number;
86	  /** 旋转角（回旋镖持续自旋） */
87	  private rot = 0;
88	  /** 飞出段累计；返回段置 true */
89	  private returning = false;
90	  private hitCd = new HitCooldown();
91	  life = 900;
92	  dead = false;
93	
94	  constructor(x: number, y: number, vx: number, vy: number, damage: number, knockback: number, projId: number) {
95	    super();
96	    this.x = x; this.y = y;
97	    this.vx = vx; this.vy = vy;
98	    this.damage = damage;
99	    this.knockback = knockback;
100	    this.projId = projId;
101	  }
102	
103	  draw(r: Renderer, cam: Camera): void {
104	    drawProj(r, cam, this, this.projId, this.rot, '#C0A060');
105	  }
106	
107	  fixedUpdate(_dt: number, game: GameHooks) {
108	    // 联机傀儡（远端弹幕快照驱动）：纯位移外推，不跑命中/碰撞（伤害归拥有者客户端结算）
109	    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
110	    if (--this.life <= 0) { this.dead = true; return; }
111	    const p = game.player;
112	    this.rot += 0.35;
113	    this.hitCd.tick();
114	    if (!this.returning) {
115	      // 飞出段：速度衰减（原版摩擦），衰减到阈值/撞墙 → 进入返回段
116	      this.vx *= 0.985;
117	      this.vy *= 0.985;
118	      this.x += this.vx;
119	      this.y += this.vy;
120	      const tx = Math.floor((this.x + this.w / 2) / TILE);
121	      const ty = Math.floor((this.y + this.h / 2) / TILE);
122	      if (game.world.store.isSolid(tx, ty) || Math.hypot(this.vx, this.vy) < 2.2) {
123	        this.returning = true;
124	        this.hitCd.clear(); // 返程可再次命中（原版去而复返二次伤害语义）
125	        // 轻微弹出防嵌入墙内
126	        this.x -= this.vx; this.y -= this.vy;
127	      }
128	    } else {
129	      // 返回段：朝主角加速（原版 AI_003 尾段朝 owner 归位）
130	      const dx = p.cx - (this.x + this.w / 2);
131	      const dy = p.cy - (this.y + this.h / 2);
132	      const d = Math.hypot(dx, dy) || 1;
133	      this.vx += (dx / d) * 0.9;
134	      this.vy += (dy / d) * 0.9;
135	      const sp = Math.hypot(this.vx, this.vy);
136	      if (sp > 12) { this.vx = (this.vx / sp) * 12; this.vy = (this.vy / sp) * 12; }
137	      this.x += this.vx;
138	      this.y += this.vy;
139	      if (d < 16) { this.dead = true; return; } // 回到手中
140	    }
141	    hitEnemies(this, game, this.hitCd, 20, Math.sign(this.vx));
142	  }
143	}
144	
145	// ================= 长矛（aiStyle 19，AI_019 随角色前刺） =================
146	
147	export class SpearProj extends Entity {
148	  w = 20; h = 20;
149	  damage: number;
150	  knockback: number;
151	  projId: number;
152	  /** 刺出方向（单位向量，原版出手时定死） */
153	  private dx: number;
154	  private dy: number;
155	  /** 最大刺出距离 px（原版 spear reach ≈ 5.5 格 + shootSpeed 修正） */
156	  private reach: number;
157	  private t = 0;
158	  private dur: number;
159	  private hitCd = new HitCooldown();
160	  dead = false;
161	
162	  constructor(dirX: number, dirY: number, reach: number, dur: number, damage: number, knockback: number, projId: number) {
163	    super();
164	    const n = Math.hypot(dirX, dirY) || 1;
165	    this.dx = dirX / n;
166	    this.dy = dirY / n;
167	    this.reach = reach;
168	    this.dur = dur;
169	    this.damage = damage;
170	    this.knockback = knockback;
171	    this.projId = projId;
172	  }
173	
174	  draw(r: Renderer, cam: Camera): void {
175	    drawProj(r, cam, this, this.projId, Math.atan2(this.dy, this.dx) + Math.PI / 2, '#A0A0B0');
176	  }
177	
178	  fixedUpdate(_dt: number, game: GameHooks) {
179	    // 联机傀儡（远端弹幕快照驱动）：纯位移外推，不跑命中/碰撞（伤害归拥有者客户端结算）
180	    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
181	    this.t++;
182	    if (this.t >= this.dur) { this.dead = true; return; }
183	    // 原版 AI_019：矛锚定在角色中心，沿出手方向伸缩（sin 曲线 0→reach→0）
184	    const k = Math.sin((this.t / this.dur) * Math.PI);
185	    const ext = k * this.reach;
186	    const p = game.player;
187	    this.x = p.cx - this.w / 2 + this.dx * ext;
188	    this.y = p.cy - this.h / 2 + this.dy * ext;
189	    hitEnemies(this, game, this.hitCd, 9999, this.dx > 0 ? 1 : -1); // 一次突刺每敌只结算一次
190	  }
191	}
192	
193	// ================= 悠悠球 / 连枷（aiStyle 99 / 15，channel 语义） =================
194	
195	export class YoyoProj extends Entity {
196	  w = 16; h = 16;
197	  damage: number;
198	  knockback: number;
199	  projId: number;
200	  /** 持续按住判定（原版 channel：按住时悠悠球滞留追光标） */
201	  private channel: () => boolean;
202	  /** 光标世界坐标 getter */
203	  private target: () => { x: number; y: number };
204	  /** 线长上限 px（原版 stringLength，按 shootSpeed 修正） */
205	  private stringLen: number;
206	  /** 连枷头带重力（aiStyle 15 的链球比悠悠球更坠） */
207	  private flail: boolean;
208	  private hitCd = new HitCooldown();
209	  private rot = 0;
210	  /** 手部坐标（线起点，fixedUpdate 每帧刷新为主角中心） */
211	  handX = 0;
212	  handY = 0;
213	  life = 7200;
214	  dead = false;
215	
216	  constructor(x: number, y: number, damage: number, knockback: number, projId: number,
217	    stringLen: number, channel: () => boolean, target: () => { x: number; y: number }, flail = false) {
218	    super();
219	    this.x = x; this.y = y;
220	    this.handX = x; this.handY = y;
221	    this.damage = damage;
222	    this.knockback = knockback;
223	    this.projId = projId;
224	    this.stringLen = stringLen;
225	    this.channel = channel;
226	    this.target = target;
227	    this.flail = flail;
228	  }
229	
230	  draw(r: Renderer, cam: Camera): void {
231	    // 线（原版 yoyo string / 连枷链：手部 → 球体）。世界坐标(实体循环在世界变换内)
232	    const c = r.canvas.getContext('2d');
233	    if (c) {
234	      c.strokeStyle = this.flail ? '#605848' : '#D0D0D8';
235	      c.lineWidth = 1.5;
236	      c.beginPath();
237	      c.moveTo(this.handX, this.handY);
238	      c.lineTo(this.x + this.w / 2, this.y + this.h / 2);
239	      c.stroke();
240	    }
241	    this.rot += 0.25;
242	    drawProj(r, cam, this, this.projId, this.rot, '#E04040');
243	  }
244	
245	  fixedUpdate(_dt: number, game: GameHooks) {
246	    // 联机傀儡（远端弹幕快照驱动）：纯位移外推，不跑命中/碰撞（伤害归拥有者客户端结算）
247	    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
248	    if (--this.life <= 0) { this.dead = true; return; }
249	    const p = game.player;
250	    this.handX = p.cx;
251	    this.handY = p.cy;
252	    this.hitCd.tick();
253	    if (!this.channel()) {
254	      // 松手/切走：回收到手（原版 channel 结束语义）
255	      const dx = p.cx - (this.x + this.w / 2);
256	      const dy = p.cy - (this.y + this.h / 2);
257	      const d = Math.hypot(dx, dy) || 1;
258	      this.vx = (dx / d) * 16;
259	      this.vy = (dy / d) * 16;
260	      this.x += this.vx;
261	      this.y += this.vy;
262	      if (d < 16) this.dead = true;
263	      return;
264	    }
265	    // 追光标（原版 AI_099：朝光标位置加速，限线长内）
266	    const t = this.target();
267	    const dx = t.x - (this.x + this.w / 2);
268	    const dy = t.y - (this.y + this.h / 2);
269	    const d = Math.hypot(dx, dy) || 1;
270	    this.vx += (dx / d) * 0.55;
271	    this.vy += (dy / d) * 0.55 + (this.flail ? 0.12 : 0.02);
272	    const sp = Math.hypot(this.vx, this.vy);
273	    const cap = this.flail ? 11 : 13;
274	    if (sp > cap) { this.vx = (this.vx / sp) * cap; this.vy = (this.vy / sp) * cap; }
275	    this.x += this.vx;
276	    this.y += this.vy;
277	    // 线长约束：超出即向手方向拉回
278	    const ox = this.x + this.w / 2 - p.cx;
279	    const oy = this.y + this.h / 2 - p.cy;
280	    const od = Math.hypot(ox, oy);
281	    if (od > this.stringLen) {
282	      const k = this.stringLen / od;
283	      this.x = p.cx + ox * k - this.w / 2;
284	      this.y = p.cy + oy * k - this.h / 2;
285	    }
286	    // 弹墙（原版 yoyo tileCollide=false 穿墙，连枷也穿；不做碰撞）
287	    hitEnemies(this, game, this.hitCd, 15, Math.sign(this.vx));
288	  }
289	}
290	
291	// ================= 手雷/炸弹/炸药（aiStyle 16，AI_016 引信爆炸） =================
292	
293	export class GrenadeProj extends Entity {
294	  w = 14; h = 14;
295	  vx: number;
296	  vy: number;
297	  damage: number;
298	  projId: number;
299	  /** 引信（原版 timeLeft：手雷 180 / 炸弹 150 / 炸药 135） */
300	  fuse: number;
301	  onExplode: (x: number, y: number, damage: number) => void;
302	  private rot = 0;
303	  dead = false;
304	
305	  constructor(x: number, y: number, vx: number, vy: number, damage: number, fuse: number,
306	    projId: number, onExplode: (x: number, y: number, damage: number) => void) {
307	    super();
308	    this.x = x; this.y = y;
309	    this.vx = vx; this.vy = vy;
310	    this.damage = damage;
311	    this.fuse = fuse;
312	    this.projId = projId;
313	    this.onExplode = onExplode;
314	  }
315	
316	  draw(r: Renderer, cam: Camera): void {
317	    drawProj(r, cam, this, this.projId, this.rot, '#408040');
318	  }
319	
320	  fixedUpdate(_dt: number, game: GameHooks) {
321	    this.rot += Math.hypot(this.vx, this.vy) * 0.03;
322	    if (--this.fuse <= 0) {
323	      this.dead = true;
324	      this.onExplode(this.x + this.w / 2, this.y + this.h / 2, this.damage);
325	      return;
326	    }
327	    // AI_016：重力 + 弹跳（碰墙法向反弹，保部分动能）。
328	    // 碰撞探测用「底边中点」而非中心——中心探测会让 14px 弹体在地面沉降 ~4px 嵌入
329	    this.vy = Math.min(this.vy + 0.3, 16);
330	    let nx = this.x + this.vx;
331	    let ny = this.y + this.vy;
332	    const st = game.world.store;
333	    const solidAt = (px: number, py: number) => {
334	      const tx = Math.floor(px / TILE);
335	      const ty = Math.floor(py / TILE);
336	      return st.inBounds(tx, ty) && st.isSolid(tx, ty);
337	    };
338	    if (solidAt(nx + this.w / 2, this.y + this.h / 2) || solidAt(nx + this.w / 2, this.y + this.h - 1)) {
339	      this.vx *= -0.85; nx = this.x;
340	    }
341	    if (solidAt(nx + this.w / 2, ny + this.h - 1)) {
342	      if (this.vy > 1) { this.vy = -this.vy * 0.5; } else { this.vy = 0; }
343	      this.vx *= 0.92;
344	      ny = this.y;
345	    }
346	    this.x = nx;
347	    this.y = ny;
348	    if (!st.inBounds(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))) this.dead = true;
349	  }
350	}
351	

```


---

## 🤖 Assistant · 2026-08-11T07:15:04.839Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"class \\|draw(\\|cs:\\|Main.cs\\|Projectile.cs\\|原版\\|1:1\" ~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts ~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts ~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts ~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts ~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts | head -80",
 "description": "Inspect entity draw methods and vanilla refs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:04.951Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts:1:// 魔法投射物(原版 Projectile 14 Spark / 短命发光弹语义):
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts:2:// 直线飞行、撞块消失、命中伤害、寿命短(原版 spark 30tick)。
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts:10:export class MagicProj extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts:29:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:1:// 飞镖投射物(原版 Projectile 10 Dart 语义:直线飞行、撞块消失、命中伤害)。
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:10:/** 电路陷阱投射物(Wiring.cs:1495-1743)。贴图 = 原版 projectile id;
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:13:// tile 137 kind ↔ projectile 对应(Wiring.cs:1495-1743 + Item.cs placeStyle 核实):
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:18:// 走色块回退 + 粒子拖尾——与原版"隐形弹体+尘埃视觉"一致(Projectile.cs:24222 188 同族 dust 驱动)
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:31:export class TrapShot extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:70:    if (kind === 'spiky') this.life = 1800; // 原版尖刺球 timeLeft 1800
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:73:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:80:      // 原版弹幕贴图(整帧):飞行类贴图默认朝上(镖尖/火苗向上),对齐速度方向需 +90°;
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:103:    // 粒子拖尾(原版火焰陷阱/热喷泉的视觉主体是沿途粒子;每 2 tick 一次防刷屏)
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:127:    // ---- 命中怪物/小动物/城镇 NPC（原版陷阱弹幕对全实体敌对，Projectile.DamageNPC 语义） ----
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:128:    // 穿透规则（近似原版）：巨石碾压穿透；尖刺球/火焰穿透（靠受击者无敌帧节流连击）；
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:144:    const buckets = (game as unknown as { entities?: { critters: Array<{ x: number; y: number; w: number; h: number; dead: boolean; hurt: (g: GameHooks) => boolean }>; npcs: Array<{ x: number; y: number; w: number; h: number; dead: boolean; hurt: (d: number, kx: number, ky: number, g: GameHooks) => boolean }> } }).entities;
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:161:export class Dart extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:166:  life = 600; // tick 上限(原版 timeLeft 600)
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:176:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:1:// 箭矢/通用直飞·抛物线投射物（原版 Projectile type 1/2、aiStyle 1/2 主干，Projectile.cs:546-566 + AI_001/AI_002）：
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:3:// 原版贴图 Projectile_N.png；命中敌人伤害/击退/暴击（穿透>1 时同敌免疫防连击）；
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:12:/** 原版投射物贴图懒加载（Projectile_1.png = 木箭、Projectile_2.png = 燃烧箭，泛用所有 id） */
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:27:  /** 原版 timeLeft（Projectile.cs:554 默认 1200） */
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:29:  /** 穿透次数（原版 penetrate：手里剑 4、箭 1；-1 视作 1） */
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:33:export class Arrow extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:34:  w = 10; h = 10; // 原版 SetDefaults type 1：width/height = 10
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:39:  /** 原版投射物类型（1=木箭 2=燃烧箭，PickAmmo projToShoot = ammo.shoot） */
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:64:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:73:    ctx.rotate(ang + Math.PI / 2); // 原版贴图纵向：rotation = atan2+π/2（AI_001 L54877）
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:94:    // aiStyle 1/2 通用重力（原版箭 0.3/tick 抛物线；直飞弹 grav=0）
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:108:      // 实心块：1/3 概率回收掉落（原版箭 Kill 的掉落），然后消失
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:113:    // 小动物:一击致死并消耗弹体(原版小动物是 NPC;近战挥砍同语义)
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:115:    // 命中敌人（原版 penetrate：箭 1 射中即停；手里剑 4 穿 4 敌，同敌免疫防连击）
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:121:        // 暴击：玩家远程基础 4%（原版 ranged 初始 4）
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:1:// 下落沙族(原版 Projectile 31/56/67/71/179/241 SandBallFalling 系,aiStyle 10 = AI_010):
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:13:export class FallingBlock extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:14:  w = 10; h = 10; // 原版 width/height = 10(vanilla-projectiles.json 全沙族一致)
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:19:  /** 同敌冷却 tick(原版穿透弹 per-NPC 免疫帧语义) */
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:22:  static readonly DAMAGE = 10; // 原版 SandBallFalling damage = 10
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:68:    // ---- 落地:变回 tile(原版 Kill 时 ai[0] 的 tile 类型放回世界) ----
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:82:  draw(r: Renderer, _cam: Camera): void {
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:83:    // 世界坐标绘制(实体循环在世界变换内):取该 tile 的原版表首帧,随下落旋转
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts:1:// 矿车实体(原版 Minecart 语义简化):沿轨道(v_314)骑行,无轨重力下落,跳车脱离。
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts:9:export class Minecart extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts:24:  draw(r: Renderer, _cam: Camera): void {

```


---

## 🤖 Assistant · 2026-08-11T07:15:06.678Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the remaining entity draw bodies (Arrow.ts 64-80, Dart.ts 73-110, 176-200, MagicProj.ts 29-50, FallingBlock 82-100, Minecart 24-40) and the paper doll part of Renderer (drawPlayer 1331-1510), drawTownNPC, drawCritter, drawHouseBanners. Also player/PaperDoll.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:07.273Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts",
 "limit": 40,
 "offset": 70
}
```


---

## 🤖 Assistant · 2026-08-11T07:15:07.309Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts",
 "limit": 30,
 "offset": 60
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:07.326Z

**📎 ToolResult**

```
60	    this.life = opts?.life ?? 1200;
61	    this.pierce = opts?.pierce ?? 1;
62	  }
63	
64	  draw(r: Renderer, _cam: Camera): void {
65	    // 世界坐标绘制(Renderer 实体循环运行在世界变换内,勿再自算屏幕坐标——
66	    // 曾双变换把箭甩出屏幕,表现为"箭隐形但能命中")
67	    const ctx = r.canvas.getContext('2d');
68	    if (!ctx) return;
69	    const ang = Math.atan2(this.vy, this.vx);
70	    const img = projSprite(this.projId);
71	    ctx.save();
72	    ctx.translate(this.x + this.w / 2, this.y + this.h / 2);
73	    ctx.rotate(ang + Math.PI / 2); // 原版贴图纵向：rotation = atan2+π/2（AI_001 L54877）
74	    ctx.imageSmoothingEnabled = false;
75	    if (img && img.complete && img.naturalWidth > 0) {
76	      ctx.drawImage(img, -this.w / 2, -this.w / 2, this.w, this.w * (img.naturalHeight / img.naturalWidth));
77	    } else {
78	      // 贴图未就绪：短线兜底
79	      ctx.strokeStyle = this.projId === 2 ? '#FFB060' : '#D8C8A0';
80	      ctx.lineWidth = 2;
81	      ctx.beginPath();
82	      ctx.moveTo(0, 0);
83	      ctx.lineTo(0, -Math.min(14, Math.hypot(this.vx, this.vy) * 1.4));
84	      ctx.stroke();
85	    }
86	    ctx.restore();
87	  }
88	
89	  fixedUpdate(_dt: number, game: GameHooks) {

```


---

## 👤 User(sidechain) · 2026-08-11T07:15:07.328Z

**📎 ToolResult**

```
70	    if (kind === 'spiky') this.life = 1800; // 原版尖刺球 timeLeft 1800
71	  }
72	
73	  draw(r: Renderer, _cam: Camera): void {
74	    // 世界坐标绘制(Renderer 实体循环运行在世界变换内,勿再自算屏幕坐标)
75	    const ctx = r.canvas.getContext('2d');
76	    if (!ctx) return;
77	    const st = TRAP_SHOT_STYLE[this.kind];
78	    const img = st.proj && r.atlas ? r.atlas.vimages.get(st.proj) : null;
79	    if (img && st.fw && st.fh && !TrapShot.isBlank(r, st.proj!)) {
80	      // 原版弹幕贴图(整帧):飞行类贴图默认朝上(镖尖/火苗向上),对齐速度方向需 +90°;
81	      // 尖刺球/巨石不随速度旋转,按位移滚转
82	      ctx.save();
83	      ctx.translate(this.x + this.w / 2, this.y + this.h / 2);
84	      if (st.spin) ctx.rotate(this.rot);
85	      else if (Math.abs(this.vx) + Math.abs(this.vy) > 0.01) ctx.rotate(Math.atan2(this.vy, this.vx) + (st.rotOff ?? 0));
86	      ctx.drawImage(img, 0, 0, st.fw, st.fh, -st.fw / 2, -st.fh / 2, st.fw, st.fh);
87	      ctx.restore();
88	      return;
89	    }
90	    ctx.fillStyle = st.color;
91	    ctx.fillRect(this.x, this.y, this.w, this.h);
92	  }
93	
94	  fixedUpdate(_dt: number, game: GameHooks) {
95	    // 联机傀儡（远端弹幕快照驱动）：纯位移外推，不跑命中/碰撞（伤害归拥有者客户端结算）
96	    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
97	    if (--this.life <= 0) { this.dead = true; return; }
98	    const st = TRAP_SHOT_STYLE[this.kind];
99	    if (st.spin) this.rot += this.vx * 0.03;
100	    this.vy += st.grav;
101	    this.x += this.vx;
102	    this.y += this.vy;
103	    // 粒子拖尾(原版火焰陷阱/热喷泉的视觉主体是沿途粒子;每 2 tick 一次防刷屏)
104	    if (st.trail && (this.life & 1) === 0) {
105	      game.spawnParticles(
106	        this.x + this.w / 2, this.y + this.h / 2,
107	        st.trail.colors[(this.life >> 1) % st.trail.colors.length],
108	        st.trail.count, 0.4, { life: st.trail.life, damp: 0.96, grav: st.trail.grav },
109	      );

```


---

## 🤖 Assistant · 2026-08-11T07:15:07.351Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts",
 "limit": 25,
 "offset": 78
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:07.364Z

**📎 ToolResult**

```
78	      this.dead = true;
79	    }
80	  }
81	
82	  draw(r: Renderer, _cam: Camera): void {
83	    // 世界坐标绘制(实体循环在世界变换内):取该 tile 的原版表首帧,随下落旋转
84	    const ctx = r.canvas.getContext('2d');
85	    if (!ctx || !r.atlas) return;
86	    const tid = TILE_BY_KEY[this.tileKey];
87	    const sheet = tid !== undefined ? TILE_DEFS[tid]?.vanilla?.sheet : undefined;
88	    if (sheet === undefined) return;
89	    const fr = r.atlas.vframeAt(sheet, 0, 0);
90	    if (!fr) return;
91	    ctx.save();
92	    ctx.translate(this.x + this.w / 2, this.y + this.h / 2);
93	    ctx.rotate(this.rot);
94	    ctx.imageSmoothingEnabled = false;
95	    ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -8, -8, 16, 16);
96	    ctx.restore();
97	  }
98	}
99	

```


---

## 🤖 Assistant · 2026-08-11T07:15:07.616Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts",
 "limit": 30,
 "offset": 25
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:07.635Z

**📎 ToolResult**

```
25	    this.life = life;
26	    this.color = color;
27	  }
28	
29	  draw(r: Renderer, _cam: Camera): void {
30	    // 世界坐标绘制(Renderer 实体循环运行在世界变换内,勿再自算屏幕坐标)
31	    const ctx = r.canvas.getContext('2d');
32	    if (!ctx) return;
33	    ctx.fillStyle = this.color;
34	    ctx.beginPath();
35	    ctx.arc(this.x + this.w / 2, this.y + this.h / 2, 4, 0, Math.PI * 2);
36	    ctx.fill();
37	  }
38	
39	  fixedUpdate(_dt: number, game: GameHooks) {
40	    // 联机傀儡（远端弹幕快照驱动）：纯位移外推，不跑命中/碰撞（伤害归拥有者客户端结算）
41	    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
42	    if (--this.life <= 0) { this.dead = true; return; }
43	    this.x += this.vx;
44	    this.y += this.vy;
45	    const tx = Math.floor((this.x + this.w / 2) / TILE);
46	    const ty = Math.floor((this.y + this.h / 2) / TILE);
47	    if (game.world.store.isSolid(tx, ty)) { this.dead = true; return; }
48	    // 小动物:一击致死并消耗弹体(近战挥砍同语义)
49	    if (hitCritters(this, game)) { this.dead = true; return; }
50	    for (const ent of game.enemies()) {
51	      const e = ent as unknown as { x: number; y: number; w: number; h: number; hurt: (d: number, kx: number, ky: number, g: GameHooks) => boolean; dead: boolean; def?: { hitSound?: string[] } };
52	      if (e.dead) continue;
53	      if (this.x < e.x + e.w && this.x + this.w > e.x && this.y < e.y + e.h && this.y + this.h > e.y) {
54	        playEnemyHitSound(game, e);

```


---

## 🤖 Assistant · 2026-08-11T07:15:08.818Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the paper doll section of Renderer (drawPlayer, 1331-1510) and drawTownNPC, drawCritter, drawHouseBanners. Also player/PaperDoll.ts. Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:09.142Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 180,
 "offset": 1331
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:09.183Z

**📎 ToolResult**

```
1331	  private drawPlayer(p: Player, world: World, swing: { t: number; dur: number; item: number } | null) {
1332	    const ctx = this.ctx;
1333	    if (p.dead) return;
1334	    // ---- 手持物（PlayerDrawLayers.cs:3857 门槛）：itemAnimation>0 || (holdStyle!=0) ----
1335	    // 武器/工具 holdStyle=0 → 仅使用中渲染（下方挥舞动画）；火把/荧光棒族 holdStyle=1
1336	    // → 静持时也渲染、手臂抬起（ItemCheck_ApplyHoldStyle 近似：竖举在身前）；
1337	    // noWet（火把 noWet=true）→ 水下不显示（与手持光源熄灭同步）。
1338	    if (!swing) {
1339	      const held = p.inv.heldItem();
1340	      const def = held ? ITEM_DEFS[held.id] : undefined;
1341	      if (held && def && !p.inWater) {
1342	        const vid = def.key === 'torch' ? 8 : viIdFromKey(def.key);
1343	        const holdStyle = Number.isFinite(vid) && HOLD_STYLE_ITEMS.has(vid) ? 1 : 0;
1344	        if (holdStyle) {
1345	          const ar = this.atlasIcon(held.id);
1346	          const icon = ar ? null : this.itemIcon(held.id);
1347	          if (ar || icon) {
1348	            ctx.save();
1349	            // 原版 holdStyle=1（ItemCheck_ApplyHoldStyle :49671/:49720）：
1350	            // itemLocation = (中心 + (frameW*0.5+2)*dir, 顶 + 24)；**itemRotation = 0**——
1351	            // 贴图以原生 45° 倾角呈现（贴图本身斜指右上），握把=左下角锚在手部，
1352	            // 朝左时整图镜像。此前归竖(-0.8rad)是错的：原版就不转。
1353	            ctx.translate(p.cx + p.facing * 7, p.y + p.h * 0.57);
1354	            ctx.scale(p.facing, 1);
1355	            if (ar) {
1356	              const w = ar.sw, h = ar.sh;
1357	              ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, 0, -h, w, h);
1358	            } else if (icon) {
1359	              ctx.drawImage(icon, 0, -icon.height * 0.6, icon.width * 0.6, icon.height * 0.6);
1360	            }
1361	            ctx.restore();
1362	          }
1363	        }
1364	      }
1365	    }
1366	    // 挥舞动画（工具）：人物身后图层——挥砍弧大部分在身体轮廓外，身后不遮挡
1367	    if (swing && swing.item >= 0 && ITEM_DEFS[swing.item]?.tool) {
1368	      this.drawUseItem(ctx, p, swing);
1369	    }
1370	
1371	    // 无敌帧闪烁：半透明而非消失（主角本体永不全隐）
1372	    ctx.save();
1373	    // 水下滤镜：只作用于主角本体素材（蓝色调：去饱和 + 压暗 + 蓝移）
1374	    if (p.headUnderwater) ctx.filter = 'sepia(0.45) hue-rotate(175deg) saturate(0.9) brightness(0.82)';
1375	    if (p.iframes > 0 && p.iframes % 6 < 2) ctx.globalAlpha = 0.45;
1376	    // 跨台阶时用渲染补偿高度（从旧高度缓升），消除物理瞬移的顿挫感；
1377	    // 联机远端叠加 netOffset（原版 Player.netOffset 平滑收敛，本地玩家恒 0）
1378	    ctx.translate(p.cx - p.facing * 2.5 + p.netOffX, p.y + p.h + p.stepRenderY + p.netOffY); // 脚底中心（精灵后移2.5px = 碰撞盒微前移）
1379	    ctx.scale(p.facing, 1);
1380	
1381	    // ---- 纸娃娃帧（捏人外观优先，M7；20 帧表默认朝右，与 NPC 相反不做内层翻转） ----
1382	    let drawn = false;
1383	    if (p.appearance) {
1384	      const doll = compositePaperDoll(p.appearance, dollEquipFromInv(p.inv, this.atlas));
1385	      if (doll) {
1386	        let row = 0; // 0 站立
1387	        if (swing) {
1388	          // 原版 useStyle=1 三段 use 姿势（Player.cs:35876-35890）：
1389	          // p>2/3 行1（举）/1/3-2/3 行2（挥）/p<1/3 行3（收）——手臂烘焙在帧内随行切换
1390	          const pAnim = Math.min(1, Math.max(0, swing.t / swing.dur));
1391	          row = pAnim > 2 / 3 ? 1 : pAnim > 1 / 3 ? 2 : 3;
1392	        }
1393	        else if (!p.onGround) row = p.vy < 0 ? 1 : 4;
1394	        else if (Math.abs(p.vx) > 0.3) row = 6 + Math.floor(p.animTime / 6) % 14; // 行走循环 6-19
1395	        const f = dollFrame(doll, row);
1396	        // 贴底:纸娃娃帧底有 ~2px 透明边距(Player_0_10 全帧实测),底锚会悬空——
1397	        // 与 legacy 路径(:1301)/小动物同一 spriteBottomPad 补偿
1398	        const pad = this.spriteBottomPad(f, `doll:${row}`);
1399	        ctx.drawImage(f.img, f.sx, f.sy, f.sw, f.sh, -f.sw / 2, -f.sh + pad, f.sw, f.sh);
1400	        drawn = true;
1401	      }
1402	    }
1403	    if (!drawn && this.atlas) {
1404	      const idle = this.atlas.rect('角色/Player.png', 'Player_0');
1405	      const runFrames = this.runFramesCache ??= this.atlas.animFrames('Player/Run');
1406	      // 动作帧池（Player.png 12-22 号帧）
1407	      if (!this.actionFramesCache) {
1408	        const pool: Record<string, ReturnType<SpriteAtlas['rect']>> = {};
1409	        for (let k = 12; k <= 22; k++) {
1410	          const fr = this.atlas!.rect('角色/Player.png', 'Player_' + k);
1411	          if (fr) pool['Player_' + k] = fr;
1412	        }
1413	        this.actionFramesCache = pool;
1414	      }
1415	      const af = this.actionFramesCache;
1416	      let frame: typeof idle = null;
1417	      // 挥砍/使用中：三段 use 姿势（原版 bodyFrame 行 1/2/3，Player.cs:35876）
1418	      if (swing) {
1419	        const pAnim = Math.min(1, Math.max(0, swing.t / swing.dur));
1420	        const swingIdx = pAnim > 2 / 3 ? 19 : pAnim > 1 / 3 ? 20 : 21;
1421	        frame = af['Player_' + swingIdx] ?? idle;
1422	      } else if (!p.onGround) {
1423	        // 空中：上升用 12（收腿）、下落用 14（张腿）
1424	        frame = (p.vy < 0 ? af['Player_12'] : af['Player_14']) ?? runFrames[0] ?? idle;
1425	      } else if (Math.abs(p.vx) > 0.3) {
1426	        const idx = Math.floor(p.animTime / 6) % runFrames.length;
1427	        frame = runFrames[idx] ?? idle;
1428	      } else {
1429	        frame = idle;
1430	      }
1431	      if (frame) {
1432	        // 精灵视觉高度固定 56px（≈3.5 格）——与碰撞盒解耦，
1433	        // 碰撞盒缩小只影响物理，贴图保持高大观感不变
1434	        const h = 56;
1435	        const w = (frame.sw / frame.sh) * h;
1436	        // 脚踏实地：按精灵最低不透明行对齐脚底（消除底部透明留白导致的浮空）
1437	        const pad = this.spriteBottomPad(frame);
1438	        // Maples 精灵默认朝左 → 内层翻转，画完还原（否则手持物会被一起翻到背后）
1439	        ctx.save();
1440	        ctx.scale(-1, 1);
1441	        ctx.drawImage(frame.img, frame.sx, frame.sy, frame.sw, frame.sh, -w / 2, -h + pad * (h / frame.sh), w, h);
1442	        ctx.restore();
1443	        drawn = true;
1444	      }
1445	    }
1446	    if (!drawn) {
1447	      // 程序化兜底（锚点同样为脚底中心）
1448	      const sheet = this.assets.playerSheet;
1449	      const fw = this.assets.playerFrameW, fh = this.assets.playerFrameH;
1450	      const frame = p.frame;
1451	      ctx.drawImage(sheet, frame * fw, 0, fw, fh, -fw / 2, -fh, fw, fh);
1452	    }
1453	
1454	    ctx.restore();
1455	    // 使用类物品（托举：药水/方块等非工具）：身体前方图层，避免被身体挡住
1456	    if (swing && swing.item >= 0 && !ITEM_DEFS[swing.item]?.tool) {
1457	      this.drawUseItem(ctx, p, swing);
1458	    }
1459	
1460	    // 气口气泡：头部浸水时显示（在朝向变换外绘制——左右移动不镜像），
1461	    // 随气量消散；整体更透明
1462	    if (p.headUnderwater || p.breath < 5 || p.refillT >= 0) {
1463	      const gap = 12.5; // 间距 12.5px，气泡直径 11px，留 ~1.5px 视觉分隔
1464	      const baseX = p.cx - (5 * gap) / 2 + gap / 2, baseY = p.y - p.h * 0.4 - 14;
1465	      // 优先原版 Bubble.png（22×22，不透明），程序化圆仅兜底
1466	      const bub = this.atlas ? this.atlas.vmisc('vanilla/Bubble.png') : null;
1467	      // 平滑气量 = (气口-1) + 当前正在消耗那颗的剩余比例 → 逐个渐隐（不画已耗尽的）。
1468	      // 直接 breath+drain 会在扣气瞬间把气泡重新顶满一格
1469	      // 水下：平滑消耗（当前颗渐隐）；出水：0.8s 快速补满动画
1470	      let display: number;
1471	      if (p.refillT >= 0) {
1472	        // 从余量处起填：refillFrom + 缺口 × 进度（不从第一颗重新冒）
1473	        display = p.refillFrom + (5 - p.refillFrom) * p.refill01;
1474	      } else {
1475	        const drain = p.headUnderwater && p.breath > 0 ? p.breathDrain01 : 1;
1476	        display = p.breath - 1 + drain;
1477	      }
1478	      // 5 个槽位固定占位（消耗时槽位不挪动，只是该槽的气泡渐隐消失）
1479	      for (let b = 0; b < 5; b++) {
1480	        const v = display - b; // 该颗的可见度：≥1 满，0..1 渐隐，≤0 跳过
1481	        if (v <= 0) continue;
1482	        const bx = baseX + b * gap;
1483	        const by = baseY;
1484	        ctx.globalAlpha = Math.min(1, v);
1485	        if (bub) {
1486	          ctx.drawImage(bub.img, bub.sx, bub.sy, bub.sw, bub.sh, bx - 5.5, by - 5.5, 11, 11);
1487	        } else {
1488	          ctx.fillStyle = '#BFE3FF';
1489	          ctx.beginPath();
1490	          ctx.arc(bx, by, 4.5, 0, Math.PI * 2);
1491	          ctx.fill();
1492	          ctx.fillStyle = 'rgba(255,255,255,0.5)';
1493	          ctx.beginPath();
1494	          ctx.arc(bx - 1.5, by - 1.5, 1.5, 0, Math.PI * 2);
1495	          ctx.fill();
1496	        }
1497	      }
1498	      ctx.globalAlpha = 1;
1499	    }
1500	
1501	    void world;
1502	  }
1503	
1504	  /** 使用/挥舞动画（与静持同尺寸：原始像素比例 ×0.9，不放大）。
1505	   *  工具/武器：绕持握点旋转挥砍（-63° → +57° 完整弧，身后图层）。
1506	   *  使用类物品（托举）：前半程旋转举起（与已验证效果一致），
1507	   *  后半程沿同一路径转回（三角波往返），收尾回到起始位——
1508	   *  不会继续向前转导致"放下时飘到身前一格"。
1509	   *  图层：工具/武器挥砍在身体之前调用（身后），使用类托举在身体之后调用（身前） */
1510	  private drawUseItem(ctx: CanvasRenderingContext2D, p: Player, swing: { t: number; dur: number; item: number }) {

```


---

## 🤖 Assistant · 2026-08-11T07:15:09.756Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"cs:\\|Main.cs\\|1:1\\|PlayerDrawLayers\\|原版\" ~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts | head -40; echo \"=== Minecart ===\"; sed -n '20,45p' ~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts",
 "description": "Check PaperDoll and Minecart vanilla refs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:09.825Z

**📎 ToolResult**

```
2:// 40×(20×56) 的完整帧表，缓存复用。通道映射实测自 PlayerDrawLayers.cs：
26: * ★ 臂部像素偏移勘误(2026-08-10,用户报"部件不够贴合"):原版 GetCompositeOffset
42:/** GetHairSettings（1456 Player.cs:16645-16760，switch(head) 精确提取）：
97:/** 合成完整帧表（含发型+装备）。equip 为原版物品 id（Armor_Head_/Armor_Legs_/Armor_Armor_ 贴图索引） */
130:  // 后发层（1.4.4+ PlayerDrawLayers:206-212：backHairDraw 时画在身体之后，即先画）
171:      // 全部部件左上角对齐帧锚点(原版 position-origin 相消;臂偏移仅是旋转 pivot,见文件头)
180:      // 身甲复合绘制（PlayerDrawLayers:1345-1366 同构）：后肩→后臂→躯干→前肩→前臂，不再画衣着层
192:    //   肩/躯干按层序:底衫4(后肩→躯干→前肩) → 衬衫6(同序)——对应原版 13/14 两个 pass
=== Minecart ===
    return !!(st.inBounds(tx, ty) && st.flags[st.idx(tx, ty)]
      && st.type[st.idx(tx, ty)] === (game as unknown as { trackTile: number }).trackTile);
  }

  draw(r: Renderer, _cam: Camera): void {
    // 世界坐标绘制(Renderer 实体循环运行在世界变换内,勿再自算屏幕坐标)
    const ctx = r.canvas.getContext('2d');
    if (!ctx) return;
    // 车身近似:灰底+深轮(素材暂无独立 cart sprite,用主色块)
    ctx.fillStyle = '#7A6A50';
    ctx.fillRect(this.x, this.y + 6, this.w, 8);
    ctx.fillStyle = '#3A3230';
    ctx.fillRect(this.x + 2, this.y + 12, 4, 4);
    ctx.fillRect(this.x + 10, this.y + 12, 4, 4);
  }

  fixedUpdate(_dt: number, game: GameHooks) {
    if (--this.life <= 0) { this.dead = true; return; }
    const st = game.world.store;
    // 轨道检测:身体中心所在格及下一格
    const cx = Math.floor((this.x + this.w / 2) / TILE);
    const cy = Math.floor((this.y + this.h / 2) / TILE);
    const onTrack = this.trackAt(game, cx, cy) || this.trackAt(game, cx, cy + 1);
    if (onTrack) {
      // 贴轨:轨道中心线 = 格底
      const trackTop = (cy + 1) * TILE;

```


---

## 🤖 Assistant · 2026-08-11T07:15:11.951Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me check the drawCritter, drawTownNPC, drawDrop, drawTombstone, drawHouseBanners in Renderer, plus the remaining parts of drawEnemy hp bar, and the Enemy.ts AI_011/12 and AI_047 multi-part families. Also check Enemy.ts sections for skeletron hand AI and golem fist AI in bossAI.ts and bossAI_golem.ts for multi-part claims.

Let me also grep Enemy.ts for "部件" and "master" / "anchor" comments.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:12.210Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 130,
 "offset": 1196
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:12.280Z

**📎 ToolResult**

```
1196	    const x = Math.round(e.cx - 18);                             // num3 = X - 18*scale
1197	    const y = Math.round(e.y + e.h);                             // 实体脚下（经典锚点）
1198	    const n = r - 0.1;                                           // ratio 偏移（:21771）
1199	    const cr = n > 0.5 ? Math.round(255 * (1 - n) * 2) : 255;
1200	    const cg = n > 0.5 ? 255 : Math.round(255 * n * 2);
1201	    const rgb = (mul: number) => `rgb(${Math.min(255, Math.round(cr * mul))},${Math.min(255, Math.round(cg * mul))},0)`;
1202	    ctx.globalAlpha = 0.95;                                      // alpha×0.95（光照亮度并入常量）
1203	    // 背景空槽（Hb2 等价：暗框+同色调暗填充）
1204	    ctx.fillStyle = 'rgba(0,0,0,0.55)';
1205	    ctx.fillRect(x - 1, y - 1, 38, 5);
1206	    ctx.fillStyle = rgb(0.45);
1207	    ctx.fillRect(x, y, 36, 3);
1208	    // 前景填充（Hb1 等价：全亮同色 tint）
1209	    ctx.fillStyle = rgb(1);
1210	    ctx.fillRect(x, y, fill, 3);
1211	    ctx.globalAlpha = 1;
1212	  }
1213	
1214	  /** 入驻旗帜（Main.cs:40152-40236 DrawNPCHousesInWorld 1:1）：
1215	   *  有家非流浪城镇 NPC（bound/守卫老人除外）在家坐标上方挂 House_Banner_1
1216	   *  （2×2 帧 16×20：X=单/双人旗、Y=housingCategory——城镇 NPC 全 0）+ 头像
1217	   *  叠画（NPC_Head_{id} 24×24）。同房多 NPC 每面旗下移 26px。锚点=帧中心。
1218	   *  位置 = home.x*16+8，y = 首个实心格下沿+18 */
1219	  private drawHouseBanners(entities: unknown[], world: World, cam: Camera) {
1220	    if (!this.atlas) return;
1221	    const cloth = this.atlas.vmisc('vanilla/House_Banner_1.png');
1222	    if (!cloth) return;
1223	    const ctx = this.ctx;
1224	    const st = world.store;
1225	    const banners: TownNPC[] = [];
1226	    for (const e of entities) {
1227	      if (e instanceof TownNPC && !e.dead && !e.bound && e.home && e.npcKey !== 'old_man') banners.push(e);
1228	    }
1229	    // 同房重复偏移（原版 num4：同 home 的排序在后计数 ×26）
1230	    for (const n of banners) {
1231	      const dup = banners.filter((o) => o !== n && o.home!.x === n.home!.x && o.home!.y === n.home!.y
1232	        && banners.indexOf(o) > banners.indexOf(n)).length;
1233	      // 从 home.y-1 向上找第一个实心格（天花板/上表面）
1234	      let cy = n.home!.y - 1;
1235	      let found = false;
1236	      while (cy >= 10) {
1237	        if (st.isSolid(n.home!.x, cy)) { found = true; break; }
1238	        cy--;
1239	      }
1240	      if (!found) continue;
1241	      // 整面旗帜绘制（House_Banner_1 = 吊杆+垂布的完整旗，32×40 ≈ 2×2.5 格；
1242	      // 用户对照官方原版实测旗帜约 4 格方形——此前按 Frame(2,2) 切 16×20 画小了）
1243	      const bx = n.home!.x * 16 + 8;                    // 原版 num8=8 偏移
1244	      // num9=18；实心格是平台（tile 19）时 -8（Main.cs:40212-40214）——
1245	      // 平台只有半格厚，旗帜上移贴平台上表面
1246	      const onPlatform = TILE_DEFS[st.type[st.idx(n.home!.x, cy)]]?.vanilla?.sheet === 19;
1247	      const by = (cy + 1) * 16 + (onPlatform ? 10 : 18) + dup * 26;
1248	      ctx.drawImage(cloth.img, cloth.sx, cloth.sy, cloth.sw, cloth.sh,
1249	        bx - cloth.sw / 2, by - cloth.sh / 2, cloth.sw, cloth.sh);
1250	      // 头像叠画（原版 TownNPCProfiles/TypeToDefaultHeadIndex NPC.cs:7489——head 索引≠NPC id）
1251	      const headIdx = TOWN_NPC_HEAD_INDEX[n.vanillaId];
1252	      const head = headIdx != null ? this.atlas.vmisc(`vanilla/NPC_Head_${headIdx}.png`) : null;
1253	      if (head) {
1254	        const hs = Math.min(1, 24 / Math.max(head.sw, head.sh));
1255	        const hw = head.sw * hs, hh = head.sh * hs;
1256	        ctx.drawImage(head.img, head.sx, head.sy, head.sw, head.sh,
1257	          bx - hw / 2, by - hh / 2 + 2, hw, hh);
1258	      }
1259	      // 光照色调（原版 Lighting.GetColor(homeTileX, num3)：旗布头像受所在格光照染色。
1260	      //  lightCanvas 为屏幕空间 2× 超采样光照图（合成在本层之后，此处取上一帧数据——
1261	      //  光照变化平缓一帧滞后无感；首帧全黑跳过）
1262	      const rectW = cloth.sw, rectH = cloth.sh + 4;
1263	      const [lsx, lsy] = cam.worldToScreen(bx, by - 12);
1264	      const lx = Math.round(lsx * 2), ly = Math.round(lsy * 2);
1265	      if (lx >= 0 && ly >= 0 && lx < this.lightCanvas.width && ly < this.lightCanvas.height) {
1266	        const ld = this.lightCtx.getImageData(lx, ly, 1, 1).data;
1267	        if (ld[0] + ld[1] + ld[2] > 0) {
1268	          ctx.save();
1269	          ctx.globalCompositeOperation = 'multiply';
1270	          ctx.fillStyle = `rgb(${ld[0]},${ld[1]},${ld[2]})`;
1271	          ctx.fillRect(bx - rectW / 2, by - rectH / 2, rectW, rectH);
1272	          ctx.restore();
1273	        }
1274	      }
1275	      // hover 名条（原版 40255+：鼠标悬停旗帜显示 NPC 名）
1276	      if (this._mouseX >= 0) {
1277	        const [mwx, mwy] = cam.screenToWorld(this._mouseX, this._mouseY);
1278	        if (mwx >= bx - rectW / 2 && mwx <= bx + rectW / 2 && mwy >= by - rectH / 2 && mwy <= by + rectH / 2) {
1279	          // FullName 语义（Lang.cs:416 GetNPCHouseBannerText → NPC.FullName:6657）：
1280	          //  有个人名 → Game.NPCTitle（zh "{1}{0}"=类型名+个人名）；无 → 类型名
1281	          const typeName = Lang.npcName(n.vanillaId) ?? n.npcKey;
1282	          const label = n.givenName ? Lang.text('Game.NPCTitle', n.givenName, typeName) : typeName;
1283	          ctx.font = '12px "Fusion Pixel 12px", sans-serif';
1284	          const tw = ctx.measureText(label).width;
1285	          ctx.fillStyle = 'rgba(20,16,28,0.85)';
1286	          ctx.fillRect(bx - tw / 2 - 5, by - rectH / 2 - 20, tw + 10, 15);
1287	          ctx.fillStyle = '#E8E4F0';
1288	          ctx.textAlign = 'center';
1289	          ctx.fillText(label, bx, by - rectH / 2 - 9);
1290	          ctx.textAlign = 'left';
1291	        }
1292	      }
1293	    }
1294	  }
1295	
1296	  private drawTownNPC(n: TownNPC) {
1297	    const ctx = this.ctx;
1298	    // 血条与怪物同规（原版 DrawInterface_14 对 friendly NPC 同函数绘制：
1299	    // life != lifeMax 即常驻显示——城镇 NPC 受伤掉血后可见；贴图条加载未就绪也照画）
1300	    this.drawEnemyHpBar(n);
1301	    // ---- 原版贴图条（Images/NPC_{id}，40×56 帧、默认朝左）：帧语义见 TownNPC.fixedUpdate ----
1302	    // 注意：不再回退 Maples 角色/NPC_1.png——那是原版绿史莱姆贴图（Maples 沿用原版命名），
1303	    // 曾导致全部城镇 NPC 显示为史莱姆
1304	    if (this.atlas) {
1305	      const r = this.atlas.vnpc(n.vanillaId, n.frame);
1306	      if (r) {
1307	        ctx.save();
1308	        // 底锚 + 逐帧实测底部透明行数补偿(spriteBottomPad):帧底 ~2px 透明边距
1309	        // 裸底锚悬空 2px、中心锚入地 2px(实测反馈)——pad 补偿保证贴地,
1310	        // 与怪物(:854)/纸娃娃(:1266)/legacy(:1301)统一
1311	        const pad = this.spriteBottomPad(r, `npc${n.vanillaId}:f${n.frame}`);
1312	        ctx.translate(n.cx, n.y + n.h); // 脚底中心
1313	        if (n.facing > 0) ctx.scale(-1, 1); // 原版贴图默认朝左，向右镜像
1314	        if (n.iframes > 0 && n.iframes % 4 < 2) ctx.filter = 'brightness(2.5)'; // 受击闪白
1315	        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, -r.sw / 2, -r.sh + pad, r.sw, r.sh);
1316	        ctx.filter = 'none';
1317	        ctx.restore();
1318	        return;
1319	      }
1320	      // 贴图条懒加载首帧未就绪：落入下方程序化兜底，本帧后懒加载完成
1321	    }
1322	    const spr = this.assets.enemySprites.get(n.npcKey);
1323	    if (!spr) return;
1324	    ctx.save();
1325	    ctx.translate(n.cx, n.cy);

```


---

## 🤖 Assistant · 2026-08-11T07:15:13.112Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"master\\|部件\\|AI_011\\|AI_012\\|AI_047\\|AI_045\\|AI_046\\|anchored\\|锚定\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts | head -40; echo \"=== golem ===\"; grep -n \"master\\|部件\\|AI_045\\|AI_046\\|AI_047\\|锚\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts | head -40",
 "description": "Find multi-part family comments in bossAI files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:13.178Z

**📎 ToolResult**

```
2:// 由 Enemy.fixedUpdate 的 aiStyle 分发调用;弹幕用 MagicProj/投射桶,部件用 fromVanilla。
21:/** AI_011 骷髅王战斗状态机(NPC.cs:21904-22288 完整核;守卫分支已在 skeletronHeadAI)。
131:/** AI_012 骷髅王手(NPC.cs:22289-22400):锚定头(ai1=头 id),头离场 → 自毁;
139:  e.master = head; // 臂骨 IK 渲染用（Renderer.drawSkeletronArm）
524:/** AI_032 机械骷髅王头 127(NPC.cs:27736-28054):初生成 4 部件;
609:/** AI_033-036 Prime 四部件(NPC.cs:28055-29110):ai1=头 id,ai0=侧 ±1。
620:  const ax = head.cx - 200 * side, ay = head.y + 230; // 部件锚点(vanilla num528 系)
624:  if (head.ai1 === 3) { e.dead = true; return; } // 头离场:部件跟随消散
=== golem ===
2://   本体 245  aiStyle 45  AI_045_Golem        NPC.cs:19447-19722(地面蓄力→跳跃循环/断臂尘/离场)
3://   挂载头 246 aiStyle 46                       NPC.cs:31273-31499(锚本体;嘴部火焰弹/眼激光)
4://   拳 247/248 aiStyle 47  AI_047_GolemFist    NPC.cs:19171-19446(肩锚归位→蓄力→直线冲拳→回位)
207:// AI_045 石巨人本体 245(NPC.cs:19447-19722)
216:  e.ai3 = 1;          // 自由态标记(探针/部件锚定可观测)
234:  // ---- 首帧:localAI[0]==0 生成部件(NPC.cs:19458-19467) ----
273:  // ---- 部件存活扫描(NPC.cs:19487-19512):flag=头/flag2=左拳/flag3=右拳 ----
417:    // noTileCollide = true(:31284);锚点 = 本体.Center + (-3*scale,-57*scale)(:31290-31308)
421:    if (dist < 100) { e.spin = 0; e.vx = dx; e.vy = dy; }        // 100 内整帧贴锚
509:// AI_047 石巨人拳 247/248(NPC.cs:19171-19446)
525:  // ---- 锚主:golemBoss 缺失 → 自毁(NPC.cs:19182-19186) ----
526:  //  本体存活(含死亡演出)→ 锚本体;本体死透 → 锚自由头(任务约定"锚定本体(或头)")
536:  // ---- 肩锚点(:19197-19199):锚主.Center + 锚主.velocity + (±84/78*scale, -9*scale) ----
578:    e.x = tx - e.w / 2;                     // 原版 base.Center = vector(整帧钉在肩锚)
617:    // 离锚 700 → 回位(:19389-19392;撞墙分支在位移后判定)
629:  // ---- 位移(蓄力态已整帧钉锚;冲拳非穿墙段撞墙即回位) ----

```


---

## 🤖 Assistant · 2026-08-11T07:15:16.493Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have a good picture. Let me also check drawCritter (769-810) and drawDrop (809-840), drawTombstone (736-769), and the remaining special parts: drawBossBar maybe. Also check Enemy.ts around AI_011/12 section (1833-1900) and the skeletron hand AI in bossAI.ts 131-150 for master assignment. Also the ROTATION_NPC handling already noted. Also check `visAngle`, `spin` fields in Enemy.

Also check for any draw hooks in bossAI files (gore/netOffset skipped — noted).

Let me also check the Critter.ts draw() (empty), Tombstone draw (empty), ItemDrop draw (empty) — Renderer draws them.

Let me read drawCritter and the skeletron section in Enemy.ts and bossAI.ts lines 21-160.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:16.692Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 115,
 "offset": 736
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:16.708Z

**📎 ToolResult**

```
736	  private drawTombstone(t: Tombstone) {
737	    const ctx = this.ctx;
738	    ctx.save();
739	    // 投射物旋转原点 = 中心（Projectile.Draw 语义）
740	    ctx.translate(t.cx, t.cy);
741	    ctx.rotate(t.angle);
742	    const styleCol = t.style * 2; // Tiles_85 样式块起点列（style 0-10 → 偶数列 0-20）
743	    let img: CanvasImageSource | null = this.tombstoneCache.get(styleCol) ?? null;
744	    if (!img && this.atlas) {
745	      // 无缝拼接四格（表内 stride 18：格间有 2px 间隙需跳过）
746	      const c = document.createElement('canvas');
747	      c.width = 32; c.height = 32;
748	      const cx = c.getContext('2d')!;
749	      let ok = true;
750	      for (let dy = 0; dy < 2; dy++) {
751	        for (let dx = 0; dx < 2; dx++) {
752	          const fr = this.atlas.vframeAt(85, (styleCol + dx) * 18, dy * 18);
753	          if (!fr) { ok = false; break; }
754	          cx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, dx * 16, dy * 16, 16, 16);
755	        }
756	      }
757	      if (ok) { this.tombstoneCache.set(styleCol, c); img = c; }
758	    }
759	    if (img) {
760	      ctx.drawImage(img, -16, -16, 32, 32);
761	    } else {
762	      const pc = getTombstoneCanvas();
763	      ctx.drawImage(pc, -8, -11, 16, 22);
764	    }
765	    ctx.restore();
766	  }
767	
768	  /** 小动物：原版 NPC 纵向帧条动画（移动时循环全帧，静止首帧；贴图默认朝左镜像） */
769	  private drawCritter(c: Critter) {
770	    if (!this.atlas) return;
771	    const meta = this.atlas.vnpcMeta(c.def.npc);
772	    if (!meta) return;
773	    // 帧选择优先级：分段动画（鸭子） > 鸟类栖息末帧 > 蝴蝶物种窗口 > 全表循环
774	    let frame: number;
775	    const anim = c.def.anim;
776	    if (anim) {
777	      // 状态选段（游水只认滞回锁：flying 后 inWater 冻结的历史 bug 不会再影响显示）
778	      const seg = c.swimLatch > 0 ? (anim.swim ?? anim.walk)
779	        : !c.onGround ? (anim.fly ?? anim.walk)
780	        : Math.abs(c.vx) > 0.15 ? (anim.walk ?? anim.idle) : (anim.idle ?? anim.walk);
781	      if (seg) {
782	        const active = Math.abs(c.vx) > 0.15 || !c.onGround || c.swimLatch > 0;
783	        frame = seg[0] + (active ? Math.floor(c.animT / 8) % seg[1] : 0);
784	      } else frame = 0;
785	    } else if (c.perchState === 1 && meta.count > 1) frame = meta.count - 1;
786	    else {
787	      const moving = Math.abs(c.vx) > 0.15 || !c.onGround;
788	      if (c.animLen > 0) frame = c.animBase + (moving ? Math.floor(c.animT / 8) % c.animLen : 0);
789	      else frame = moving ? Math.floor(c.animT / 8) % meta.count : 0;
790	    }
791	    const fr = this.atlas.vnpc(c.def.npc, frame);
792	    if (!fr) return;
793	    const ctx = this.ctx;
794	    // 缩放贴合碰撞盒；按帧最低不透明行对齐脚底（帧底透明内边距会导致悬浮）
795	    const h = c.h * 1.25;
796	    const w = (fr.sw / fr.sh) * h;
797	    const pad = this.spriteBottomPad(fr, `npc${c.def.npc}:f${frame}`); // 帧内底部透明行数（按 NPC+帧号稳定缓存）
798	    ctx.save();
799	    ctx.translate(c.cx, c.y + c.h); // 脚底中心
800	    ctx.scale(c.facing >= 0 ? -1 : 1, 1); // 贴图默认朝左
801	    if (c.def.glow) {
802	      ctx.shadowColor = 'rgba(220,255,140,0.9)';
803	      ctx.shadowBlur = 6; // 萤火虫发光
804	    }
805	    ctx.drawImage(fr.img, fr.sx, fr.sy, fr.sw, fr.sh, -w / 2, -h + pad * (h / fr.sh), w, h);
806	    ctx.restore();
807	  }
808	
809	  private drawDrop(d: ItemDrop) {
810	    const bob = Math.sin((d.age + d.bobPhase * 60) * 0.1) * 1.5;
811	    // 优先 Maples 图标
812	    const ar = this.atlasIcon(d.itemId);
813	    if (ar) {
814	      const ctx = this.ctx;
815	      const drawH = 14 * ar.sh / ar.sw;
816	      ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, d.x, d.y + bob, 14, drawH);
817	      // 原版 Item.color（彩色凝胶）：同贴图逐像素乘 color，XNA 预乘两步（同 NPC color pass）
818	      if (d.color && d.color[3] > 0) {
819	        const tinted = this.tintedSprite(`item${d.itemId}`, ar, d.color);
820	        ctx.globalCompositeOperation = 'destination-out';
821	        ctx.globalAlpha = d.color[3] / 255;
822	        ctx.drawImage(ar.img, ar.sx, ar.sy, ar.sw, ar.sh, d.x, d.y + bob, 14, drawH);
823	        ctx.globalCompositeOperation = 'lighter';
824	        ctx.globalAlpha = 1;
825	        ctx.drawImage(tinted, d.x, d.y + bob, 14, drawH);
826	        ctx.globalCompositeOperation = 'source-over';
827	      }
828	      return;
829	    }
830	    const icon = this.itemIcon(d.itemId);
831	    if (!icon) return;
832	    this.ctx.drawImage(icon, d.x, d.y + bob, 12, 12);
833	  }
834	
835	  // 敌人 → Maples 动画映射
836	  private enemyAnimCache = new Map<string, ReturnType<SpriteAtlas['animFrames']>>();
837	  private enemyAnim(key: string): ReturnType<SpriteAtlas['animFrames']> {
838	    let f = this.enemyAnimCache.get(key);
839	    if (!f) {
840	      const map: Record<string, string> = {
841	        slime_green: 'Slime/Jump', slime_blue: 'Slime/Jump',
842	        zombie: 'Zombie/Walk',
843	      };
844	      f = this.atlas && map[key] ? this.atlas.animFrames(map[key]) : [];
845	      this.enemyAnimCache.set(key, f);
846	    }
847	    return f;
848	  }
849	
850	  private drawEnemy(e: Enemy, world: World) {

```


---

## 🤖 Assistant · 2026-08-11T07:15:17.391Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '120,160p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts; echo \"=== Enemy 1833-1900 ===\"; sed -n '1830,1880p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read skeletron hand AI and Enemy dungeon guardian section"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:17.481Z

**📎 ToolResult**

```
let enemyCtor: (typeof import('./Enemy'))['Enemy'] | null = null;
/** Enemy 构造注入(Enemy.ts import 时回填,避免循环依赖) */
export function bindEnemyCtor(c: (typeof import('./Enemy'))['Enemy']) { enemyCtor = c; }

export function spawnPart(game: GameHooks, src: Enemy, id: number): Enemy | null {
  if (!enemyCtor) return null;
  const p = enemyCtor.fromVanilla(id, src.cx, src.cy);
  if (!p) return null;
  return addEnemy(game, p);
}

/** AI_012 骷髅王手(NPC.cs:22289-22400):锚定头(ai1=头 id),头离场 → 自毁;
 *  头非悬浮态 → 漂在头两侧(±120×ai0, 头上方 100);悬浮态 → 缓慢环绕(±200, +230)。
 *  每 300t(ai3 计)朝玩家挥击冲刺。 */
export function skeletronHandAI(e: Enemy, game: GameHooks, player: Player | null) {
  const headId = e.ai1;
  const enemies = game.enemies() as unknown[];
  const head = enemies.find((n) => (n as Enemy).id === headId) as Enemy | undefined;
  if (!head || head.vanilla?.aiStyle !== 11 || head.dead) { e.dead = true; return; }
  e.master = head; // 臂骨 IK 渲染用（Renderer.drawSkeletronArm）
  if (head.ai1 === 3) { e.dead = true; return; }
  e.facing = -(e.ai0 || 1);
  if (!player) { e.x += e.vx; e.y += e.vy; return; }
  // 缓慢环绕(头悬浮态);头冲撞态则回到侧位
  const ty = head.y - 100;
  const tx = head.x + head.w / 2 - e.w / 2 - 120 * (e.ai0 || 1);
  if (head.ai1 === 0) {
    e.ai3 += 1;
    if (e.ai3 >= 300) { e.ai3 = -120; } // 负值=挥击中
    if (e.ai3 < 0) {
      // 挥击:朝玩家冲刺 8 速
      const dx = player.cx - e.cx, dy = player.cy - e.cy;
      const d = Math.hypot(dx, dy) || 1;
      e.vx += ((dx / d) * 8 - e.vx) * 0.15;
      e.vy += ((dy / d) * 8 - e.vy) * 0.15;
    } else {
      // 环绕位:头右/左 200px、下方 230(原版 num200 系)
      const ox = head.x + head.w / 2 - e.w / 2 - 200 * (e.ai0 || 1);
      const oy = head.y + 230;
      e.vx += ((ox - e.x) * 0.02 - e.vx) * 0.1;
      e.vy += ((oy - e.y) * 0.02 - e.vy) * 0.1;
=== Enemy 1833-1900 ===
    this.y += this.vy;
  }

  // AI_011 骷髅王(35)战斗状态机在 bossAI.ts skeletronBossAI；68 守卫走下方专用分支

  /** AI_011 地牢守卫(68)（NPC.145.cs:21937-21941, 22277-22288）：
   *  恒 ai[1]=2：伤害 9999、恒速 8 直线追击；玩家死/超 2000px → ai[1]=3 下坠脱场。
   *  noTileCollide 直移 */
  private dungeonGuardianAI(game: GameHooks, player: Player | null) {
    if (!this.aiInit) { this.aiInit = true; this.ai0 = 1; } // 初始化（L21910；68 无手 NPC）
    if (!player || Math.abs(this.cx - player.cx) > 2000 || Math.abs(this.cy - player.cy) > 2000) {
      this.ai1 = 3;
    } else if (this.ai1 !== 3) {
      this.ai1 = 2;
    }
    if (this.ai1 === 2) {
      this.def.damage = 9999;
      const dx = player!.cx - this.cx, dy = player!.cy - this.cy;
      const d = Math.hypot(dx, dy) || 1;
      this.vx = (dx / d) * 8;
      this.vy = (dy / d) * 8;
    } else {
      this.vy += 0.1;
      if (this.vy < 0) this.vy *= 0.95;
      this.vx *= 0.95;
    }
    this.x += this.vx;
    this.y += this.vy;
  }

  /** AI_020 火轮（NPC.145.cs:24596+）：ai[3]=1+Next(15)*0.1 速度档；
   *  首段垂直俯冲 spd/acc/2≈15 tick（L24617-24622），随后恒速 ±spd 弹跳——
   *  noTileCollide 穿墙，"弹"靠 |v|≥spd 时 direction 翻转（L24637-24660）而非碰撞 */
  private blazingWheelAI() {
    if (!this.aiInit) { this.aiInit = true;
      this.facing *= -1;
      this.y += this.h / 2 + 8;
      if (this.facing === 0) this.facing = 1;
      this.ai3 = 1 + Math.floor(Math.random() * 15) * 0.1;
      this.vy = 6 * this.ai3 * this.dirY;
      this.ai0 = 1;
      this.x += this.vx;
      this.y += this.vy;
      return;
    }
    const spd = 6 * this.ai3, accel = 0.2 * this.ai3;
    const phaseLen = Math.floor(spd / accel / 2); // num304（ai3 约掉=15）
    if (this.ai0 >= 1 && this.ai0 < phaseLen) {
      this.vy = this.dirY * spd;
      this.ai0 += 1;
    } else if (this.ai0 >= phaseLen) {

```


---

## 🤖 Assistant · 2026-08-11T07:15:24.013Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have comprehensive coverage. Let me also quickly verify the Enemy fields (master, spin, visAngle) and check golem fist AI visual notes. Also check if there are any other special draws I missed: drawBossBar, drawInvasionBar, EmoteBubble, ResourceBars — those are UI, probably out of scope but I can mention briefly.

Also check the ROTATION_NPC usage in drawEnemy — done. Check "visAngle" definition in Enemy.ts and "spin".

Also check PaperDoll.ts head briefly. I have enough from grep.

One more thing: the user asked about "AI 分族的注释声称 1:1" in Enemy.ts — particularly AI_013, AI_011/12, AI_047. I found:
- Enemy.ts:1590 AI_013 plantAI claims "NPC.cs:22604-22700 一比一"
- Enemy.ts:2941 AI_004 EoC 1:1
- Enemy.ts:959 AI_040 1:1
- Enemy.ts:1058 AI_042 1:1
- Enemy.ts:903 NPCCanStickToWalls 1:1
- Enemy.ts:922 Transform 1:1
- AI_011/12: in bossAI.ts line 21/131 with "完整核" claim (AI_011 says "NPC.cs:21904-22288 完整核"), not literal "1:1" but bossAI.ts:1 header says "Boss AI 1:1 移植". AI_047 in bossAI_golem.ts with header "1:1 移植" and comment "经典模式主链 1:1;expert/getGoodWorld 分支保留注释;netcode/纯视觉尘(Gore/netOffset)跳过".

Let me verify exact wording of AI_013 comment re 1:1 vs partial. Line 1590-1592. Done.

Let me get the golem fist AI snippet around 509-540 for details on master anchoring, and check Enemy.ts field master/spin/visAngle definitions. Also confirm whether drawEnemy handles golem parts visually via ROTATION_NPC (246-249 are in ROTATION_NPC set — yes: 246,247,248,249 listed).

Let me quickly grep Enemy.ts for "visAngle" and "spin" and "master" declarations.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:24.730Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"visAngle\\|spin\\b\\|spin =\\|master\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -20; echo \"=== golem fist 505-545 ===\"; sed -n '505,545p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts",
 "description": "Check Enemy visual fields and golem fist AI"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:24.774Z

**📎 ToolResult**

```
101:      this.visAngle = Math.atan2(this.vy, this.vx) + Math.PI * 0.5;
121:    this.visAngle = Math.atan2(this.vy, this.vx) + Math.PI * 0.5;
140:      if (dist > 0.01) s.visAngle = Math.atan2(dyC, dxC) + Math.PI * 0.5;
221:  visAngle = Math.PI;    // EoC 显示角度（素材正面朝下:瞳孔角=π/2+θ,盯玩家须 θ=φ−π/2）
222:  spin = 0;              // EoC 变身旋转进度 0..1
279:  master: Enemy | null = null;
997:      this.visAngle = Math.atan2(this.vy, this.vx);
1018:      this.visAngle = Math.atan2(sy, sx);
1020:    if (this.vanillaId === 531) this.visAngle += Math.PI / 2; // :29922
1200:        this.visAngle = Math.atan2(this.vy, this.vx) + 0.785;
1217:      this.visAngle += (0.1 + (this.ai1 / 120) * 0.4) * this.facing; // 越转越快
1511:    this.visAngle = Math.atan2(this.vy, this.vx) - Math.PI / 2;
1733:    this.visAngle = Math.atan2(this.vy, this.vx) + Math.PI * 0.5;
2971:  /** EoC 旋转追踪：visAngle 向 target 以 rate 步进（最短弧，cs:19975-20000） */
2976:    let a = this.visAngle;
2982:    this.visAngle = a + diff * Math.min(1, rate * 10);
3027:          this.visAngle += this.spinSpeed;
3076:        this.visAngle = Math.atan2(this.vy, this.vx) - Math.PI * 0.5;
3095:        this.visAngle += this.spinSpeed;
=== golem fist 505-545 ===
  e.y += e.vy;
}

// ---------------------------------------------------------------------------
// AI_047 石巨人拳 247/248(NPC.cs:19171-19446)
// ---------------------------------------------------------------------------
// 原版 ai[0] 是状态机(0 归位/1 蓄力/2 冲拳/3 直飞);任务约定 ai0=侧别,
// 状态机落在本文件 WeakMap(fistX.state),计时仍用 ai[1]。

export function golemFistAI(e: Enemy, game: GameHooks, player: Player | null) {
  const x = fistXOf(e);
  if (!e.bInit) {
    e.bInit = true;
    e.ai0 = e.vanillaId === 247 ? -1 : 1;   // ai0=侧别(-1 左拳/1 右拳;由本体生成时预置)
    e.ai1 = 0;
    e.alphaFade = false;
    x.alpha = 255;
  }
  const isLeft = e.vanillaId === 247;

  // ---- 锚主:golemBoss 缺失 → 自毁(NPC.cs:19182-19186) ----
  //  本体存活(含死亡演出)→ 锚本体;本体死透 → 锚自由头(任务约定"锚定本体(或头)")
  const body = findBody(game);
  const head = findHead(game);
  const anchor = body && !body.dead ? body : head;
  if (!anchor) { e.dead = true; return; }

  const num = balanceNum(game, player);
  // 渐显(:19187-19194):期间 ai[1]=0
  if (fadeAlpha(e, x) > 0) e.ai1 = 0;

  // ---- 肩锚点(:19197-19199):锚主.Center + 锚主.velocity + (±84/78*scale, -9*scale) ----
  const offX = isLeft ? -84 : 78;
  const tx = anchor.cx + anchor.vx + offX * SCALE;
  const ty = anchor.cy + anchor.vy - 9 * SCALE;
  const dx = tx - e.cx, dy = ty - e.cy;
  const dist = Math.hypot(dx, dy);
  e.facing = isLeft ? 1 : -1;               // 镜像朝向(原版贴图方向)

  if (!player) { e.x += e.vx; e.y += e.vy; return; }

```


---

## 🤖 Assistant · 2026-08-11T07:15:31.091Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have enough. Now let me write the markdown inventory. Let me double check a couple of things:

1. drawBossBar/drawInvasionBar — UI, mention briefly as out of enemy scope? The user asked specifically about enemy/entity special drawing. I'll focus on that and include a short "UI/overlay" note.

2. Check whether there's a special draw for Plantera vines/hooks — grep for "Chain" usage elsewhere in Renderer or elsewhere for plantera tentacles. drawPlantVine is only aiStyle 13. Plantera hooks (263) use aiStyle 52 — do they draw vines? Let me check quickly.

Also check for "Chain" in other render places, and for WOF drawing special (hungry / eyes anchored) — the ROTATION_NPC covers 113-115. Any special draw for moon lord hands? ROTATION_NPC covers 396/397.

Let me grep for special drawing hooks for aiStyle 50/51/52/53 (plantera) and golem in Renderer — I saw none in drawEnemy besides vanilla table. Let me verify there's no other conditional inside drawEnemy I missed (lines 850-975 read fully — yes, only vanillaId 36 arm, aiStyle 13 vine, vanillaId 50 ninja+crown).

Also check the legacy (Maples) path and procedural fallback — noted.

Let me also check EmoteBubble quickly? Not enemy-specific; skip. But maybe mention briefly.

One more check: does anything else in render/ draw enemies? WaterfallRenderer draws waterfalls; TileParticles draws particles. Not enemy.

Let me quickly grep for "Chain" across src to see if plantera hook vines are drawn anywhere.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:32.077Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Chain\\|Tentacle\\|tentacle\\|Gore\" ~/Project/GLM/SandboxWorld/game/src/render/*.ts | grep -v \"Chunk\\|ChainOf\" | head -20; echo \"=== drawBossBar ===\"; grep -n \"drawBossBar\\|drawInvasionBar\\|BossBar\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head",
 "description": "Check for chain/tentacle drawing and boss bar"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:32.126Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:862:    // 每 28px 一段 Chain 贴图步进，剩余 <40px 画一段收缩尾段对齐锚点
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1106:   *  中心（ai0/ai1 各 ×16+8）逐段画 Chain 贴图——步长 28px、距锚 <40px 时尾段
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1108:   *  正面向上）。贴图分流（:22480-22510）：56→Chain5、175→Chain14、259/260→
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1109:   *  Chain24/25，默认（43 食人怪/101 邪恶触手）→Chain4。光照由 compositeLight
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1118:      id === 56 ? 'vanilla/Chain5.png'
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1119:        : id === 175 ? 'vanilla/Chain14.png'
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1120:          : id === 259 ? 'vanilla/Chain24.png'
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1121:            : id === 260 ? 'vanilla/Chain25.png'
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1122:              : 'vanilla/Chain4.png');
=== drawBossBar ===
612:      this.drawBossBar(ctx, viewW, boss);
616:    if (invasion) this.drawInvasionBar(ctx, viewW, invasion);
2252:  private drawInvasionBar(ctx: CanvasRenderingContext2D, viewW: number, invasion: { name: string; pct: number }) {
2267:  private drawBossBar(ctx: CanvasRenderingContext2D, viewW: number, boss: { name: string; hp: number; maxHp: number; cx: number; cy: number }) {

```


---

## 🤖 Assistant · 2026-08-11T07:15:48.384Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have everything. Time to write the markdown inventory.

Structure:
1. 渲染入口与分发 (Renderer.ts:496-520)
2. 敌怪特殊绘制（Renderer.ts drawEnemy 及子函数）
   - drawSkeletronArm
   - drawPlantVine
   - KS ninja + crown
   - rotation families / tilt-only
   - color pass
   - alpha
   - EoC anchor offset
   - spriteBottomPad anchoring
   - FindFrame engine (line 67-100+)
3. 其他实体（drawTombstone, drawCritter, drawDrop, drawHouseBanners, drawTownNPC, drawPlayer/paper doll, drawEnemyHpBar）
4. entities/ 自带 draw() 的实体（Arrow, Dart TrapShot, Dart, MagicProj, FallingBlock, Minecart, WeaponProj x4）
5. Enemy.ts AI 分族 1:1 声称清单（AI_013, AI_040, AI_042, AI_004, NPCCanStickToWalls, Transform, critter routing, ai[1] color table）+ 多部件族的声称（AI_011/12 in bossAI.ts, AI_045/46/47 in bossAI_golem.ts, AI_032-036 prime, plantera, etc.）with caveats noted (expert 分支未启用, netcode/Gore 跳过, 任务约定 deviations for golem fist).

Let me note specific line numbers carefully.

Renderer.ts:
- 67-101: FindFrame 分族帧引擎 header (NPC.cs:67295+), ZOMBIE_FRAME_TYPES :69, BAT_SKIP_LAST :71, ROTATION_NPC :72-75, vanillaFrameIdx :78
- 850-1101 drawEnemy
- 858-860: skeletron arm hook (vanillaId 36 && master)
- 861-863: plant vine hook (aiStyle 13)
- 865-973: vanilla NPC table path
- 870-877: anchoring grounded/flying, spriteBottomPad
- 880-893: rotation-driven families (ROTATION_NPC, aiStyle 4/5/6/23/40/56), tiltOnly5
- 894-909: per-family rotation
- 911: facing mirror
- 912-914: alpha semantics
- 920-923: EoC offset +23/30
- 924-942: color pass (Main.cs:24527 + NPC.GetColor L94903)
- 943-956: KS ninja (vanillaId 50) Main.cs:22798-22818
- 957-966: KS crown Main.cs:25571-25595, Extra_39
- 975-1064: Maples 精灵优先路径 (legacy keys: slime/zombie/cave_bat 49/demon_eye 2/EoC 4)
- 1066-1099: 程序化兜底
- 1103-1104: armBoneImg
- 1105-1149: drawPlantVine (Main.cs:22433-22514)
- 1151-1179: drawSkeletronArm (Main.cs:22543-22596)
- 1181-1212: drawEnemyHpBar (Main.cs:21748-21839)
- 1214-1294: drawHouseBanners (Main.cs:40152-40236)
- 1296-1330: drawTownNPC
- 1331-1502: drawPlayer (holdStyle PlayerDrawLayers.cs:3857, useStyle rows Player.cs:35876, breath bubbles)
- 1510+: drawUseItem
- 1575+: tintedSprite (Main.cs:24986 / NPC.cs:94903)
- 736-766 drawTombstone (Projectile.Draw 语义)
- 769-807 drawCritter
- 809-833 drawDrop (Item.color)
- 636-688 drawWires (Main.cs:43543-43954) — not enemy but special draw; mention briefly.
- 2252/2267: drawInvasionBar (Main.cs:47071), drawBossBar — UI overlay.

Enemy.ts:
- 331-400: aiStyle dispatch table
- 1590-1662: plantAI (NPC.cs:22604-22700 一比一)
- 1835-1860: dungeonGuardianAI (NPC.145.cs:21937-21941, 22277-22288)
- 903: NPCCanStickToWalls 1:1 (NPC.cs:56209-56229)
- 922: Transform 1:1 (NPC.cs:81861-81919)
- 959: AI_040 1:1 (NPC.cs:29784-30022)
- 1058: AI_042 1:1 (NPC.cs:30281-30310)
- 2941: AI_004 1:1 (1456 NPC.cs:19909-20757, 专家分支未启用)
- 655: ai[1] 体内物品色表 1:1 (油漆 lerp 缺)
- 2206: critter 各家族后续逐族 1:1 (未完成声称)
- 2330: 小动物路由按 aiStyle 精确分流到各家族 1:1

bossAI.ts:
- 1: header "Boss AI 1:1 移植"
- 21: AI_011 骷髅王战斗状态机 (NPC.cs:21904-22288 完整核;守卫分支已在 skeletronHeadAI)
- 131-139: AI_012 骷髅王手 (NPC.cs:22289-22400), e.master = head at 139
- 308: 经典模式参数 1:1;专家/大师/FTW 分支仅注释保留
- 524: AI_032 Prime 头 (NPC.cs:27736-28054) 初生成 4 部件
- 609: AI_033-036 Prime 四部件 (NPC.cs:28055-29110)

bossAI_golem.ts:
- 1-7: header 1:1 移植, 经典模式主链 1:1; expert/getGoodWorld 分支保留注释; netcode/纯视觉尘(Gore/netOffset)跳过
- 207: AI_045 本体 (NPC.cs:19447-19722)
- 246 (head aiStyle 46 NPC.cs:31273-31499) at line 3
- 509: AI_047 fist (NPC.cs:19171-19446); 任务约定 deviations: ai0=侧别 instead of state machine, state in WeakMap; anchor 本体或自由头.

bossAI_queenbee_plantera.ts: header 1:1 (NPC.cs:30312-30998 蜂后; 世纪之花族), 经典模式参数 1:1.
bossAI_wof.ts: header 1:1 (ilspycmd 反编译, 经典模式参数).
bossAI_lategame.ts: header 后期三大 Boss AI 1:1 移植 (邪教徒/光之女皇/史莱姆皇后?), 929 note about ancientLight 收敛为直飞弹 (非 1:1).
bossAI_duke_moonlord.ts: header 1:1 移植(二).

Which are the lategame three bosses? Let me not guess — could check quickly but it's minor. The header says "后期三大 Boss". I could check function names quickly. Not critical but let me be accurate — I'll do one quick grep.

Actually let me do a fast grep of exported function names in bossAI_lategame.ts to name them.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:15:48.996Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"export function\\|^// ---\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts | head -40",
 "description": "List exported AI functions in bossAI files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T07:15:49.030Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:41:export function queenBeeAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:274:export function planteraHookAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:314:export function planteraAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:467:export function planteraTentacleAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_queenbee_plantera.ts:566:export function planteraTentacle2AI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:120:export function lunaticCultistAI(e: Enemy, game: GameHooks, player: Player | null): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:363:export function empressOfLightAI(e: Enemy, game: GameHooks, player: Player | null): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:653:export function queenSlimeAI(e: Enemy, game: GameHooks, player: Player | null): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:931:export function ancientLightAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts:961:export function ancientDoomAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:25:export function skeletronBossAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:122:export function bindEnemyCtor(c: (typeof import('./Enemy'))['Enemy']) { enemyCtor = c; }
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:124:export function spawnPart(game: GameHooks, src: Enemy, id: number): Enemy | null {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:134:export function skeletronHandAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:172:export function kingSlimeAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:235:export function brainOfCthulhuAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:293:export function creeperAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:311:export function accelTo(v: number, target: number, a: number): number {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:317:export function seek(e: Enemy, tx: number, ty: number, spd: number, acc: number): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:324:export function losClear(game: GameHooks, x0: number, y0: number, x1: number, y1: number): boolean {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:335:export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:344:export function twinsAI(e: Enemy, game: GameHooks, player: Player | null, spaz: boolean) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:527:export function skeletronPrimeAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:613:export function primePartAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:835:export function seekSteer(e: Enemy, target: { cx: number; cy: number }, spd: number, acc: number): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:845:export function seekSteer2(e: Enemy, tx0: number, ty0: number, spd: number, accX: number, accY: number): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:859:export function destroyerAI(e: Enemy, game: GameHooks, player: Player | null) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:964:export function enemySpawnChain(head: Enemy, count: number): Enemy[] {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:970:export function driveChain(head: Enemy, linkDist: number): void {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:986:// ---- 工具 ----

```


---

## 🤖 Assistant · 2026-08-11T07:15:50.171Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything I need. Now write the markdown report.
```

</details>


---

## 🤖 Assistant · 2026-08-11T07:16:59.613Z · glm-x-preview-260804

```
# 敌怪/实体特殊绘制 已实现清单

以下均为只读盘点结果，未改动任何文件。所有行号基于当前工作区文件。

---

## 1. 渲染分发入口

**`~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:496-520`** — 实体循环：
- `:496` `drawHouseBanners`（旗帜层，实体前）
- `:501` `if (e instanceof Enemy) this.drawEnemy(e, world)`
- `:502-505` `drawDrop` / `drawTownNPC` / `drawTombstone` / `drawCritter`
- `:508-509` 投射物类实体走自带 `draw()`（见第 5 节）
- `:516/:520` 本地与远端玩家 `drawPlayer`（纸娃娃）

`~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts:22` 定义抽象 `draw(r: Renderer, cam: Camera)`；`Enemy.ts:3298`、`Player.ts:929`、`Critter.ts:298`、`ItemDrop.ts:120`、`Tombstone.ts:128`、`TownNPC.ts:219` 均为空实现（`/* Renderer 统一绘制 */`），即这些族的绘制全部集中在 Renderer。

---

## 2. drawEnemy 内的敌怪特殊绘制（核心）

### 2.1 骷髅王手 臂骨 IK
- **位置**：调用点 `Renderer.ts:858-860`；实现 `Renderer.ts:1151-1179 drawSkeletronArm(hand, head)`
- **触发**：`e.vanillaId === 36 && e.master != null`（`master` 由 AI 写入，见第 6.2 节）
- **内容**：两段收缩 IK，从手部锚点 `position + w/2 − 5·ai[0], +20` 向头中心做两段（92/60 缩比）插值；每段 `rotation = atan2(dy,dx) − π/2`；贴图 `sprites/vanilla/Arm_Bone.png`（懒加载，`:1103-1104 armBoneImg`）；`ai[0]` 决定 −1 左手 / 1 右手；j=0 段后追加半段推进
- **原版引用**：注释声称 **Main.cs:22543-22596 1:1**（锚点 `:22545`、向量 `:22547-22548`、旋转 `:22572`、段间推进 `:22587`）

### 2.2 AI_013 植物/攀爬者族 茎蔓
- **位置**：调用点 `Renderer.ts:861-863`；实现 `Renderer.ts:1105-1149 drawPlantVine(e)`
- **触发**：`e.vanilla?.aiStyle === 13`（食人怪 43、爬行者 101、吞噬怪 56、捕兽草 175、真菌球 259/260）
- **内容**：头中心 → 锚点格 `(ai0·16+8, ai1·16+8)` 逐段画 Chain 贴图；默认步长 28px、终止距离 40px（259/260 为 12/20）；整链 `rotation = atan2(dy,dx) − π/2`；源矩形取贴图顶部 `seg` 行、origin=贴图中心。贴图分流：56→Chain5、175→Chain14、259→Chain24、260→Chain25、默认（43/101）→Chain4。`ai0/ai1 < 0` 或表未就绪时直接返回
- **原版引用**：注释声称 **Main.cs:22433-22514 1:1**（num7/num8 段长/终止距离 `:22442-22447`、循环 `:22441-22512`、步进 `:22454-22555`、尾段对齐 `:22504-22505`、贴图分流 `:22480-22510`）

### 2.3 史莱姆王（vanillaId 50）体内忍者 + 头顶金冠
- **位置**：`Renderer.ts:943-967`（在 `drawEnemy` 原版表路径内，仅 `e.vanillaId === 50`）
- **忍者**：独立贴图 `vanilla/Ninja.png` 叠画在 KS 中心；随速度反向摆动（`zeroY = -vy`、`zeroX = -vx*2`）+ `rotation = vx*0.05`；按帧序 `sy===120/360/480`（挤压帧）做 +2/−2/−6 的 y 修正。注释引用 **Main.cs:22798-22818 1:1**
- **金冠**：贴图 `vanilla/Extra_39.png`（82×56）；锚点 = KS Center 上移 `(70 − num223)×scale`，`num223` 按帧序取 `[2,-6,2,10,2,0]`；gfxOffY 恒 0；朝向翻转继承外层 facing。注释引用 **Main.cs:25571-25595 case 50，1:1**（另引 wiki "Extra_39 internally"）

### 2.4 旋转驱动族（多部件 Boss 的本体/部件朝向）
- **位置**：`Renderer.ts:880-911`（`drawEnemy` 内）
- **触发**：
  - 集合 `ROTATION_NPC` `:72-75`：35/68（骷髅王头/守卫）、113-115（WoF/之眼/饥饿者）、125/126（双子）、127-131（Prime 头+四部件）、134-136（毁灭者链）、246-249（石巨人头/双拳）、261-265（世花族）、370（猪鲨）、396/397（月总头/手）、657（史莱姆皇后）
  - aiStyle 显式：4（克眼）、5（噬魂怪/蜂群）、6（蠕虫）、23（飞行武器）、40（爬墙蜘蛛）、56（地牢之魂）
- **内容**：`rotationDriven` 为真时禁止 facing 镜像（"屁股朝前"防线，`:883-885`）；按族分别 `ctx.rotate(e.visAngle)` 或 `ctx.rotate(e.spin)`。AI_005 内再分三档（`:896-903`）：黄蜂 42/231-235、孢子蝠 176/205 只 tilt `vx*0.1`；蜜蜂 210/211 tilt `vx*0.2`（注释引 cs:51045-51054 + FindFrame 蜜蜂覆盖 L75553）；其余转头 `visAngle`。AI_006 注释引 cs:51500（+π/2）；AI_040 引 cs:29865/29919、531 +π/2；AI_023 引 cs:25336-25390；AI_056 引 cs:32927
- **注意**：`visAngle`/`spin` 是渲染专用字段，定义在 `Enemy.ts:221-222`，由各 AI 每帧写（`Enemy.ts:101/121/140/997/1018-1020/1200/1217/1511/1733/2976-2982/3027/3076/3095` 等）

### 2.5 color 二次绘制（XNA 预乘混合等价）
- **位置**：`Renderer.ts:924-942`（触发：`e.colorRGBA[3] > 0`，史莱姆凝胶等）；公共实现 `:1575+ tintedSprite`
- **内容**：同贴图再画一遍逐像素乘 color。两步模拟 XNA AlphaBlend：① `destination-out` 按 colorA 削弱底层 ② `lighter` 全量加染色精灵。注释明确"普通 drawImage 会把染色 RGB 再乘 alpha（蓝色糊成灰绿）"，并记录了曾因基础/染色两层锚点不一致导致史莱姆"彩色+灰影"双画的坑（`:933-934`）
- **原版引用**：**Main.cs:24527 + NPC.GetColor L94903**；tintedSprite 头注 `Main.cs:24986 / NPC.cs:94903`

### 2.6 alpha 渐显、锚点、EoC 质心修正
- **alpha**：`Renderer.ts:912-914`，`globalAlpha = 1 − clamp(spawnAlpha)/255`，注释引原版 `NPC.Opacity/GetAlpha`（SetDefaults 静态值：史莱姆 175 半透明凝胶，无通用渐隐）
- **锚点**：`:870-877` 飞行型=帧中心（引 Main.cs:23635 语义），地面型=底锚 + `spriteBottomPad` 逐帧底部透明行补偿（NPC 帧底普遍 ~2px 透明边距；声称与纸娃娃(:1266)/legacy(:1301)/小动物(:763)四路统一）
- **EoC 修正**：`:915-922`，NPC_4 每帧 110×166，眼球质心 y≈106（张嘴帧 113）≠ 帧中心 83；绘制整体下移 +23（张嘴帧 +30）让 100×110 盒居中（标注"用户 2026-08-11 拍板"）
- **FindFrame 帧引擎**：`:67-100+ vanillaFrameIdx`，注释声明基于 **1.4.5.6 Terarria1456/Terraria/NPC.cs:67295+**；已实现族：僵尸族 `ZOMBIE_FRAME_TYPES :69`（L77026，行走 0,1,2,1）、蝙蝠族 `BAT_SKIP_LAST :71`（L75523→L75585）、栖息态 aiStyle 17/25（秃鹫 cs:24082 / 宝箱怪 cs:25645）、爬墙蜘蛛 aiStyle 40（cs:73795-73817）

### 2.7 Maples 精灵优先 + 程序化兜底（非原版表路径）
- `Renderer.ts:975-1064`：key 分流 `slime*`（feet 锚+squash）、`zombie`、`cave_bat`（NPC_49 五帧扑翼，`:981-993`）、`demon_eye`（NPC_2 双帧，`:994-1005`，按 `atan2(vy,vx)+π` 自由旋转 `:1044-1049`）、`eye_of_cthulhu`（NPC_4 上下各 3 帧=一二阶段，"实测对调"，`:1006-1025`；`visAngle` 平滑追踪 `:1050-1054`）
- `Renderer.ts:1066-1099`：程序化兜底（slime squash 拉伸、帧条动画、EoC 二阶段双帧闪切）
- 受击闪白（`iframes % 4 < 2` → `brightness(2.5)`）与水下蓝色调滤镜（`sepia(0.45) hue-rotate(175deg) …`）贯穿各路径

---

## 3. 其他 Renderer 特殊绘制

| 实现 | 位置 | 触发/内容 | 原版引用 |
|---|---|---|---|
| `drawEnemyHpBar` | `Renderer.ts:1181-1212` | `hp<maxHp` 即常驻；几何绘制 36px 宽血条（Hb1/Hb2 未入素材管线），颜色公式 ratio−0.1 → 绿/红，alpha×0.95 | **Main.DrawHealthBar Main.cs:21748-21839** + 显示门 `DrawInterface_14_EntityHealthBars :45223`（:21771-21810） |
| `drawHouseBanners` | `Renderer.ts:1214-1294` | 有家非流浪城镇 NPC（bound/守卫老人除外）；`House_Banner_1.png` 整面旗 + `NPC_Head_{idx}` 头像叠画（24×24）；同房重复旗下移 26px；平台(tile 19)时 y−8；multiply 光照染色；hover 名条 | **Main.cs:40152-40236 DrawNPCHousesInWorld 1:1**（num8=8 `:40212-40214`、头像索引 `NPC.cs:7489`、名条 40255+、Lang.cs:416） |
| `drawTownNPC` | `Renderer.ts:1296-1330` | 原版贴图条 `Images/NPC_{id}` 40×56 帧；底锚+`spriteBottomPad`；受击闪白；受伤后血条（friendly NPC 同 DrawInterface_14） | 注释 `:1301-1303`（拒绝回退 Maples NPC_1——那是绿史莱姆贴图） |
| `drawTombstone` | `Renderer.ts:736-766` | 墓碑旋转（Tiles_85 样式块），四格无缝拼 32×32（表内 stride 18 跳 2px 间隙），程序化兜底 | 注释引 **Projectile.Draw 中心旋转语义** |
| `drawCritter` | `Renderer.ts:769-807` | 原版 NPC 纵向帧条；帧选择优先级：分段动画（鸭子游水/飞/走/待机）> 鸟类栖息末帧 > 蝴蝶物种窗口 > 全表循环；底锚+pad；萤火虫 `shadowBlur=6` 发光 | 无行号引用 |
| `drawDrop` | `Renderer.ts:809-833` | Maples 图标 + 上下 bob；彩色凝胶走 color pass（同 2.5 两步预乘） | 注释引 **原版 Item.color** |
| `drawPlayer`（纸娃娃） | `Renderer.ts:1331-1502` | 三层：①静持手持物（holdStyle=1 火把/荧光棒族，`HOLD_STYLE_ITEMS :46-50`）②纸娃娃/legacy/程序化帧 ③托举使用类。纸娃娃帧行选择引 **useStyle=1 三段 Player.cs:35876-35890**（>2/3 行1 / 中 行2 / <1/3 行3）；行走 6-19；气泡 `Bubble.png` 5 槽渐隐 | **PlayerDrawLayers.cs:3857**（渲染门槛）、**ItemCheck_ApplyHoldStyle :49671/:49720**（itemRotation=0 勘误注释 `:1349-1352`）、Player.cs:35876 |
| `drawUseItem` | `Renderer.ts:1510-1549` | 工具/武器绕持握点旋转挥砍（−63°→+57°，身后层）；使用类三角波托举（身前层） | 无行号 |
| `drawWires` | `Renderer.ts:636-688` | 四色导线行/连接掩码（上+18 右+36 下+72 左+144）/多色淡化/致动器覆盖 | **Main.cs:43543-43954 DrawWires**（行 Y `:43596-43616`、色行 `:43641`、掩码 `:43621-43640`） |
| `drawBossBar` / `drawInvasionBar` | `Renderer.ts:2267` / `:2252` | HUD Boss/入侵条（非实体层） | 注释 `:614` 引 **DrawInvasionProgress Main.cs:47071 语义** |

`render/` 其余文件（SkyRenderer / BiomeBackground / WeatherRenderer / VanillaLiquidRenderer / WaterfallRenderer / VanillaTiler / TileAnim / TileParticles / EmoteBubble / ResourceBars 等）均为背景/地形/UI 绘制，不涉及敌怪。

---

## 4. 纸娃娃合成（player/PaperDoll.ts）

- `compositePaperDoll`：40×(20×56) 完整帧表缓存；通道映射"实测自 **PlayerDrawLayers.cs**"
- `:26` 臂部像素偏移勘误（2026-08-10，"部件不够贴合"反馈，引原版 `GetCompositeOffset`）
- `:42` `GetHairSettings`（**1456 Player.cs:16645-16760**，switch(head) 精确提取）
- `:130` 后发层（**1.4.4+ PlayerDrawLayers:206-212**，backHairDraw 先画）
- `:171` 全部部件左上角对齐帧锚点（原版 position−origin 相消；臂偏移仅为旋转 pivot）
- `:180` 身甲复合绘制（**PlayerDrawLayers:1345-1366 同构**）：后肩→后臂→躯干→前肩→前臂
- `:192` 底衫/衬衫层序对应原版 13/14 两个 pass

---

## 5. entities/ 下自带 draw() 的实体

| 文件+行号 | 类 | 触发 | 内容 | 原版引用 |
|---|---|---|---|---|
| `entities/Arrow.ts:64-87` | `Arrow` | 所有箭/直飞抛物线弹 | `projSprite(projId)` 贴图按 `atan2(vy,vx)+π/2` 旋转；贴图未就绪画短线兜底 | 注释 `:73` **rotation = atan2+π/2（AI_001 L54877）**；文件头 Projectile.cs:546-566 |
| `entities/Dart.ts:73-92` | `TrapShot` | 电路陷阱弹（镖/矛/火焰/超压/尖刺球/巨石） | 原版弹幕整帧；飞行类贴图默认朝上需 `+90°` 对齐速度（`st.rotOff`）；尖刺球/巨石不随速度转、按位移滚转（`st.spin`）；无贴图走色块+粒子拖尾 | 文件头 `:10-18` **Wiring.cs:1495-1743** + **Projectile.cs:24222**（188 同族 dust 驱动） |
| `entities/Dart.ts:176` | `Dart` | 敌方飞镖（NPC 主动弹） | 同 Arrow 旋转逻辑 | `:1` 原版 Projectile 10 Dart 语义 |
| `entities/MagicProj.ts:29-37` | `MagicProj` | 魔法 spark 类短命发光弹 | 纯几何：4px 半径圆（fillStyle=color），无贴图 | `:1-2` 原版 Projectile 14 Spark / 30tick |
| `entities/FallingBlock.ts:82-97` | `FallingBlock` | 下落沙族投射物（Projectile 31/56/67/71/179/241, aiStyle 10） | 取该 tile 原版表首帧 `vframeAt(sheet,0,0)`，16×16，随下落自转 `this.rot` | 文件头 `:1`；`DAMAGE = 10` 原版 SandBallFalling |
| `entities/Minecart.ts:24-38` | `Minecart` | 矿车实体 | **程序化色块**（灰底 `#7A6A50` + 双深色轮 `#3A3230`），无原版贴图——注释自认"素材暂无独立 cart sprite" | `:1` "原版 Minecart 语义简化" |
| `entities/WeaponProj.ts:18-33` | `drawProj` 共用 | 所有近战/爆炸投射物 | 贴图按角度旋转 + 色块 fallback；注释强调世界坐标绘制（实体循环已在世界变换内） | `:16` rotation = ang+π/2 与 AI_001 一致 |
| `entities/WeaponProj.ts:103-105` | `Boomerang`（aiStyle 3） | 回旋镖 | `drawProj`，持续自旋 `rot += 0.35` | `:82` SetDefaults type 6：22×22 |
| `entities/WeaponProj.ts:174-176` | `SpearProj`（aiStyle 19/161） | 长矛 | `drawProj`，角度=出手方向+π/2 | `:155` reach ≈ 5.5 格 + shootSpeed |
| `entities/WeaponProj.ts:230-243` | `YoyoProj`（aiStyle 99 / 连枷 15） | 悠悠球/连枷 | **额外画线**：手部→球体 lineTo（连枷 `#605848` / 悠悠球 `#D0D0D8`，lineWidth 1.5），再 `drawProj` 自旋 | `:204` stringLength；`:231` 原 yoyo string/flail chain |
| `entities/WeaponProj.ts:316-318` | `GrenadeProj`（aiStyle 16） | 手雷/炸弹/炸药 | `drawProj`，滚转 `rot += |v|*0.03` | `:299` timeLeft：手雷 180/炸弹 150/炸药 135 |

---

## 6. Enemy.ts AI 分族的"1:1"声称盘点

### 6.1 Enemy.ts 内明确写"1:1 / 一比一"的注释

| 行号 | 对象 | 声称 | 原版引用 | 备注/偏差 |
|---|---|---|---|---|
| `:1590-1592` | **AI_013 plantAI** | "**NPC.cs:22604-22700 一比一**" | 锚点格(ai0/ai1)固定、朝玩家伸展（range 内钳制）、逆向加速 ×1.5、锚点格被挖即死、300-450 tick 周期 range×1.3 | 行内已标注偏差：食人怪 getGoodWorld 350 未接入（`:1603`）；爬行者 101 诅咒焰块引 cs:22823-22856（`:1640-1641`）；**AI 侧不含蔓的绘制**——蔓绘制在 Renderer.drawPlantVine（引 Main.cs 而非 NPC.cs） |
| `:903` | `NPCCanStickToWalls` | 1:1 | NPC.cs:56209-56229：身体中心 3×3 内"非实心 tile 且有背景墙" | — |
| `:922` | `Transform` | 1:1 | NPC.cs:81861-81919：换类型+按比例结转 HP+ai[0..3] 清零 | — |
| `:959` | **AI_040** 爬墙蜘蛛族 | 1:1 | NPC.cs:29784-30022 | — |
| `:1058` | **AI_042** 失落女孩 | 1:1 | NPC.cs:30281-30310 | 注明"伪装成无害 NPC 静止站立（无移动逻辑…）" |
| `:2941` | **AI_004** 克苏鲁之眼 | 1:1 | **1456 NPC.cs:19909-20757** | 注明"普通模式数值；**专家分支未启用**" |
| `:655` | ai[1] 体内物品 → 目标色表 | 占位色"1:1 表" | — | 注明"踩油漆色 lerp 暂缺（无油漆系统）" |
| `:2330` | 小动物路由 | 按 aiStyle 精确分流到各家族"1:1 实现"（AI_001/016 复用既有精确 AI） | — | — |
| `:2206` | 小动物通用 | — | — | **反向声称**："各家族原版行为（蚱蜢 ai1 跳/鸟 ai24 飞/蚯蚓 ai66 爬）**后续逐族 1:1**，先统一温和地面行为"——即当前非 1:1 |

### 6.2 多部件族的"1:1"声称（AI 在 bossAI*.ts，不在 Enemy.ts 本体）

**AI_011 / AI_012 骷髅王（头 35 + 手 36）**
- `entities/bossAI.ts:1` 文件头："Boss AI **1:1 移植**（Terarria1456 NPC.cs SetDefaults 指定 aiStyle 的专用核）"
- `bossAI.ts:21` AI_011 头："NPC.cs:21904-22288 **完整核**；守卫分支已在 skeletronHeadAI"（声称完整，非字面 1:1）
- `bossAI.ts:131-139` AI_012 手："NPC.cs:22289-22400：锚定头(ai1=头 id)，头离场→自毁；头非悬浮态漂两侧(±120×ai0, 上方 100)，悬浮态缓慢环绕(±200,+230)；每 300t 朝玩家挥击冲刺"。**`:139 e.master = head` 是渲染耦合点**（Renderer.drawSkeletronArm 依赖）
- `Enemy.ts:1835-1860` AI_011 地牢守卫 68 专用分支："NPC.145.cs:21937-21941, 22277-22288：恒 ai[1]=2，伤害 9999、恒速 8 直线追击；玩家死/超 2000px → ai[1]=3 下坠脱场"
- `bossAI.ts:308` "**经典模式参数 1:1**；专家/大师/FTW 分支仅注释保留"
- 分发：`Enemy.ts:343-349`（case 11：68 走 `dungeonGuardianAI`，否则 `skeletronBossAI`；case 12 → `skeletronHandAI`）

**AI_045 / 046 / 047 石巨人（本体 245 + 挂头 246 + 双拳 247/248）**
- `entities/bossAI_golem.ts:1-7` 文件头："石巨人 Boss 族 AI **1:1 移植**（Terarria1456, 1.4.5.6）… **经典模式主链 1:1**; expert/getGoodWorld 分支保留注释; **netcode/纯视觉尘(Gore/netOffset)跳过**"
- `:2-4` 行号映射：本体 245 NPC.cs:19447-19722（蓄力→跳跃循环/断臂尘/离场）；挂头 246 NPC.cs:31273-31499（锚本体；嘴部火焰弹/眼激光）；拳 247/248 NPC.cs:19171-19446（肩锚归位→蓄力→直线冲拳→回位）
- `:207` AI_045 本体；`:234` 首帧 localAI[0]==0 生成部件（NPC.cs:19458-19467）；`:273` 部件存活扫描（NPC.cs:19487-19512：flag=头/flag2=左拳/flag3=右拳）
- `:417` 挂头 noTileCollide=true(:31284)，锚点 = 本体.Center+(−3·scale, −57·scale)(:31290-31308)；`:421` 100 内整帧贴锚
- **`:509-517` AI_047 拳的明确偏差**："原版 ai[0] 是状态机(0 归位/1 蓄力/2 冲拳/3 直飞)；**任务约定 ai0=侧别**，状态机落在本文件 WeakMap(fistX.state)，计时仍用 ai[1]" —— 即**并非逐字段 1:1**
- `:526` 锚主选择偏差："本体存活(含死亡演出)→锚本体；本体死透→锚自由头（任务约定'锚定本体(或头)'）"
- `:536` 肩锚点(:19197-19199)：锚主.Center+velocity+(±84/78·scale, −9·scale)；`:578` 蓄力态整帧钉锚；`:617` 离锚 700 回位(:19389-19392)
- 渲染侧：246-249 已登记进 `Renderer.ts:75 ROTATION_NPC`（随 `spin` 旋转），**无额外绘制钩子**（无臂/链几何，纯贴图）

**其他多部件族（供对照）**
- `bossAI.ts:524` AI_032 机械骷髅王头 127（NPC.cs:27736-28054）：初生成 4 部件；`:609` AI_033-036 Prime 四部件（NPC.cs:28055-29110）：ai1=头 id、ai0=侧 ±1，`:620` 锚点 vanilla num528 系（头 Center ±200, +230），`:624` 头离场部件跟随消散。渲染仅靠 ROTATION_NPC（127-131）
- `bossAI.ts:859-983` AI_037 毁灭者 134：80 段链 `enemySpawnChain`/`driveChain`（每段独立 Enemy，wormFollow 驱动）；渲染靠 aiStyle 6 段旋转 + ROTATION_NPC 134-136
- `bossAI_queenbee_plantera.ts:1-5` 蜂后 222（aiStyle 43，**NPC.cs:30312-30998**）+ 世纪之花族 **1:1 移植**；"经典模式参数 1:1; expert/getGoodWorld 分支只注释保留; netcode 跳过"。世花族（`planteraHookAI :274` 钩蔓 263 / `planteraAI :314` 本体 262 / `planteraTentacleAI :467` / `planteraTentacle2AI :566`）**渲染无蔓/触须几何**，261-265 仅靠 ROTATION_NPC
- `bossAI_duke_moonlord.ts:1-9` 猪鲨 AI_069(370) + 月总 aiStyle 77/78/79（398 核心/397 手/396 头）："经典模式主链 1:1; expert/getGoodWorld 分支保留注释; netcode 跳过"。渲染：370/396/397 在 ROTATION_NPC，无部件连线
- `bossAI_lategame.ts:1` 拜月教邪教徒(`lunaticCultistAI :120`) / 光之女皇(`empressOfLightAI :363`) / 史莱姆皇后(`queenSlimeAI :653`) "后期三大 Boss AI 1:1 移植（经典模式主链）"；`:929` 注明邪教徒远古之光"**已收敛为 468 直飞弹，本核供数据完整性/未来 1:1 替换**"（即当前非 1:1）
- `bossAI_wof.ts:1` 血肉墙族 "1:1 移植（ilspycmd 反编译，经典模式参数）"；渲染：113-115 在 ROTATION_NPC，眼睛/饥饿者无连线绘制
- `bossAI.ts:172` kingSlimeAI（AI_015）、`:235` brainOfCthulhuAI（AI_054）、`:293` creeperAI（AI_055）、`:344` twinsAI（AI_030/031）

### 6.3 Enemy.ts aiStyle 分发表（`Enemy.ts:331-400`）

已接入专用核的族：92 假人 / 1 史莱姆 / 2 飘浮眼 / 3 战士 / 4 克眼 / 5 噬魂怪 / 6 蠕虫 / 8 法师 / 10 诅咒头骨 / 11 骷髅王头+守卫 / 12 骷髅王手 / 13 植物 / 14 蝙蝠 / 15 史莱姆王 / 16 游泳 / 17 秃鹫 / 18 水母 / 19 蚁狮 / 20 火轮 / 21 刺球 / 22 幽灵 / 23 飞行武器 / 25 宝箱怪 / 26 冲锋 / 27-29 WoF 族 / 30-31 双子 / 32-36 Prime / 37 毁灭者 / 39 陆龟 / 40 爬墙蜘蛛 / 41 赫柏林 / 42 失落女孩 / 43 蜂后 / 44 飞鱼 / 45-47 石巨人 / 50-53 世花族 / 54-55 克脑 / 56 地牢之魂 / 69-70 猪鲨 / 77-79 月总 / 84 邪教徒 / 100-101 远古之光/末日 / 107 ImprovedWalkers / 120 光之女皇 / 121 史莱姆皇后；**`:399 default → zombieAI "其余家族待逐个移植"`**

---

## 7. 关键结论

1. **敌怪特殊几何绘制只有两处**：`drawSkeletronArm`（vanillaId 36，Main.cs:22543-22596）与 `drawPlantVine`（aiStyle 13，Main.cs:22433-22514），均为"实体 + 附属链/臂"结构；另有 KS（50）忍者+金冠两个叠画层（Main.cs:22798-22818 / 25571-25595）。
2. **多部件 Boss 的绘制策略是"零几何、纯贴图 + 旋转登记"**：Prime 四部件、毁灭者链、世花钩蔓/触须、石巨人双拳、月总双手、WoF 三件套全部只登记 `ROTATION_NPC`（`Renderer.ts:75`）+ aiStyle 旋转分支，**没有任何部件连线/蔓藤几何**；唯一的例外是骷髅王手（靠 AI 写 `master` 字段触发臂骨 IK）。
3. **"1:1"声称的真实边界**普遍是"经典模式主链 1:1"，且各文件头明示豁免项：expert/getGoodWorld/FTW 分支仅注释保留、netcode 跳过、Gore/netOffset 纯视觉尘跳过（bossAI_golem.ts:7 最完整）。两处明确的非 1:1 点：**AI_047 石巨人拳的 ai[0] 语义被任务约定改写**（bossAI_golem.ts:513-517），以及邪教徒远古之光收敛为直飞弹（bossAI_lategame.ts:929）。
4. AI 注释（NPC.cs 行号）与绘制注释（Main.cs 行号）分属两套引用体系——AI_013 的 AI 声称 NPC.cs:22604-22700，而其蔓绘制声称 Main.cs:22433-22514，二者行号区间不同源，盘点/审计时需分别核对。
```
