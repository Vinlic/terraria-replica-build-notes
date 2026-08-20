# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T15:57:59.221Z

```
审计 Terraria 1.4.5.6 反编译源码中【方块绘制的接缝/偏移处理机制】的完整清单,并与我们的 TS 实现对照找出缺失项。

原版源码(只读):
- ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs
  - GetTileDrawData(约 :4600-5700 的巨型 switch,含 tileWidth/tileHeight/tileTop/addFrX/addFrY/半砖处理)
  - DrawBasicTile / 主绘制循环(约 :1010-1660,含 num5 X 居中、半砖裁剪、:1609-1660 的"邻居是半砖时本格补条"逻辑、slope 切条)
  - DrawTrees / DrawGrass 等特殊通道
- ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs(Sets: IgnoresNearbyHalfbricksWhenDrawn 等)

我们的实现(只读对照):
- ~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts(drawVanillaCell 主路径、DRAW_Y_OFFSET 表、drawTreeCell、drawSlopedFrame)
- ~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts(chunk 三/四遍)
- ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts(vmeta/grid/stride,如相关)

任务:枚举原版所有"影响接缝/相邻衔接"的绘制机制,分五类:
A. 精灵尺寸 ≠16(tileWidth/tileHeight 20/18/20×20 等,产生下溢/居中)——逐 case 列出 tile id + 尺寸 + 锚定语义
B. tileTop 下沉(2/4px 插地)——逐 case 列出 tile id 与值,并核对我们 DRAW_Y_OFFSET 表是否覆盖(列出我们表的内容)
C. vector.X/Y 手动偏移(如 :1069-1138 的 726 按坡面 blockType 偏移 ±6/±2、129、723/724 等)——逐 case 列出
D. 邻接衔接特判——重点读 :1609-1660(邻居半砖时本格 8px 补条 + IgnoresNearbyHalfbricksWhenDrawn + 底部半砖光照条),说明精确绘制规则
E. 其他接缝相关(addFrX/addFrY 帧重排如 case 100/530、全帧/特殊路径)

对每一项标注:我们已移植(给出我们代码位置)/ 未移植(给出原版行号与规则摘要)。输出精炼清单,不要贴大段代码。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T15:57:59.225Z

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

## 🤖 Assistant · 2026-08-11T15:58:01.330Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a comprehensive audit of seam/offset handling mechanisms in Terraria 1.4.5.6 decompiled source for tile drawing, compared against the TS implementation. This is a read-only exploration task across multiple files.

Let me start by exploring the key files in parallel. First, let me look at the Vanilla TileDrawing.cs sections mentioned, the TileID.cs Sets, and the TS files.

Let me read the key sections:
1. TileDrawing.cs GetTileDrawData (~4600-5700)
2. TileDrawing.cs DrawBasicTile / main draw loop (~1010-1660)
3. TileID.cs Sets
4. VanillaTiler.ts
5. ChunkCache.ts
6. SpriteAtlas.ts

These are big files. Let me start with targeted greps and reads in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:01.588Z · glm-x-preview-260804

```
我将对原版 TileDrawing 的接缝/偏移机制做系统审计,并对照 TS 实现。先并行读取关键区域。
```


---

## 🤖 Assistant · 2026-08-11T15:58:01.961Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileWidth\\|tileHeight\\|tileTop\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | head -150",
 "description": "List tile dimension assignments in TileDrawing.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:02.024Z

**📎 ToolResult**

```
<persisted-output>
Output too large (36.1KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/8f9c7b63-58b1-49de-a435-85fe12e156d6/tool-results/bhhsvehfo.txt

Preview (first 2KB):
884:		GetTileDrawData(tileX, tileY, tileDrawInfo.tileCache, tileDrawInfo.typeCache, ref tileDrawInfo.tileFrameX, ref tileDrawInfo.tileFrameY, out tileDrawInfo.tileWidth, out tileDrawInfo.tileHeight, out tileDrawInfo.tileTop, out tileDrawInfo.halfBrickHeight, out tileDrawInfo.addFrX, out tileDrawInfo.addFrY, out tileDrawInfo.tileSpriteEffect, out tileDrawInfo.glowTexture, out tileDrawInfo.glowSourceRect, out tileDrawInfo.glowColor);
885:		if (tileDrawInfo.tileTop < 0)
889:		else if (tileDrawInfo.tileTop + tileDrawInfo.tileHeight <= 16)
1019:		Rectangle rectangle = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight - tileDrawInfo.halfBrickHeight);
1020:		float num5 = ((float)tileDrawInfo.tileWidth - 16f) / 2f;
1025:		Vector2 vector = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - num5, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + tileDrawInfo.halfBrickHeight) + screenOffset;
1293:					Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector + num12.ToRotationVector2() * 2f, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY + num11, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight), color2, Vector2.Zero, 1f, SpriteEffects.None);
1316:					Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight), color2, Vector2.Zero, 1f, SpriteEffects.None);
1375:				Vector2 position2 = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop) + screenOffset;
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-11T15:58:02.658Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs ~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts ~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts",
 "description": "Count lines in target files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:02.786Z

**📎 ToolResult**

```
    9831 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs
    1942 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs
     715 ~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts
     372 ~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts
     925 ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts
   13785 total

```


---

## 🤖 Assistant · 2026-08-11T15:58:03.934Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me look at the saved grep output for tileWidth/tileHeight/tileTop assignments, and also read the GetTileDrawData region.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:04.263Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/8f9c7b63-58b1-49de-a435-85fe12e156d6/tool-results/bhhsvehfo.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:04.437Z

**📎 ToolResult**

```
1	884:		GetTileDrawData(tileX, tileY, tileDrawInfo.tileCache, tileDrawInfo.typeCache, ref tileDrawInfo.tileFrameX, ref tileDrawInfo.tileFrameY, out tileDrawInfo.tileWidth, out tileDrawInfo.tileHeight, out tileDrawInfo.tileTop, out tileDrawInfo.halfBrickHeight, out tileDrawInfo.addFrX, out tileDrawInfo.addFrY, out tileDrawInfo.tileSpriteEffect, out tileDrawInfo.glowTexture, out tileDrawInfo.glowSourceRect, out tileDrawInfo.glowColor);
2	885:		if (tileDrawInfo.tileTop < 0)
3	889:		else if (tileDrawInfo.tileTop + tileDrawInfo.tileHeight <= 16)
4	1019:		Rectangle rectangle = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight - tileDrawInfo.halfBrickHeight);
5	1020:		float num5 = ((float)tileDrawInfo.tileWidth - 16f) / 2f;
6	1025:		Vector2 vector = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - num5, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + tileDrawInfo.halfBrickHeight) + screenOffset;
7	1293:					Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector + num12.ToRotationVector2() * 2f, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY + num11, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight), color2, Vector2.Zero, 1f, SpriteEffects.None);
8	1316:					Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight), color2, Vector2.Zero, 1f, SpriteEffects.None);
9	1375:				Vector2 position2 = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop) + screenOffset;
10	1381:				Vector2 vector2 = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop) + screenOffset;
11	1427:			empty = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight);
12	1430:			Main.tileBatch.Draw(highlightTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f + (float)num24, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + num25) + screenOffset, empty, highlightColor, _zero, 1f, tileDrawInfo.tileSpriteEffect);
13	1613:				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 8f), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY + 8, drawData.tileWidth, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
14	1628:				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 8f), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY + 8, drawData.tileWidth, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
15	1629:				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(num8, 0f), new Rectangle(drawData.tileFrameX + num8 + drawData.addFrX, drawData.addFrY + drawData.tileFrameY, drawData.tileWidth - num8, drawData.tileHeight), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
16	1643:				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 8f), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY + 8, drawData.tileWidth, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
17	1644:				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY, drawData.tileWidth - num9, drawData.tileHeight), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
18	1667:				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 4f), new Rectangle(144 + drawData.addFrX, 66 + drawData.addFrY, drawData.tileWidth, 4), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
19	1704:			Rectangle rectangle = new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight);
20	2714:			Main.tileBatch.Draw(TextureAssets.GlowMask[297].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), Color.White, _zero, 1f, drawData.tileSpriteEffect);
21	2718:			Main.tileBatch.Draw(TextureAssets.GlowMask[298].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), Color.White, _zero, 1f, drawData.tileSpriteEffect);
22	2722:			Main.tileBatch.Draw(TextureAssets.GlowMask[299].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), Color.White, _zero, 1f, drawData.tileSpriteEffect);
23	2726:			Main.tileBatch.Draw(TextureAssets.GlowMask[295].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), Color.White, _zero, 1f, drawData.tileSpriteEffect);
24	2730:			Main.tileBatch.Draw(TextureAssets.GlowMask[296].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), Color.White, _zero, 1f, drawData.tileSpriteEffect);
25	2748:			Main.tileBatch.Draw(TextureAssets.Flames[num].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), color, _zero, 1f, drawData.tileSpriteEffect);
26	2762:				Vector2 vector = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset;
27	2763:				Rectangle value = new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight);
28	2780:			Rectangle value3 = new Rectangle(drawData.tileFrameX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight);
29	2789:				Main.tileBatch.Draw(value2, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num6, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num7) + screenOffset, value3, color3, _zero, 1f, drawData.tileSpriteEffect);
30	2795:			Rectangle value5 = new Rectangle(drawData.tileFrameX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight);
31	2797:			Main.tileBatch.Draw(value4, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, value5, Color.White * ((float)(int)Main.mouseTextColor / 255f), _zero, 1f, drawData.tileSpriteEffect);
32	2801:			Main.tileBatch.Draw(TextureAssets.GlowSnail.Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(75, 100, 255, 0), _zero, 1f, drawData.tileSpriteEffect);
33	2805:			Main.tileBatch.Draw(TextureAssets.GlowMask[293].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(200, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
34	2809:			Main.tileBatch.Draw(TextureAssets.GlowMask[131].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(250, 250, 250, 200), _zero, 1f, drawData.tileSpriteEffect);
35	2813:			Main.tileBatch.Draw(TextureAssets.GlowMask[300].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(75, 100, 255, 0), _zero, 1f, drawData.tileSpriteEffect);
36	2817:			Main.tileBatch.Draw(TextureAssets.FireflyJar.Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
37	2821:			Main.tileBatch.Draw(TextureAssets.LightningbugJar.Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
38	2825:			Main.tileBatch.Draw(TextureAssets.GlowMask[291].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
39	2829:			Main.tileBatch.Draw(TextureAssets.JellyfishBowl[drawData.typeCache - 316].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
40	2833:			Main.tileBatch.Draw(TextureAssets.XmasLight.Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
41	2850:			Main.tileBatch.Draw(TextureAssets.Flames[num8].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
42	2905:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num93, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num94) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
43	2924:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num87, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num88) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
44	2934:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num75, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num76) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
45	2944:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num78, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num79) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
46	2954:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num84, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num85) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
47	2964:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num81, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num82) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
48	2970:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
49	2984:						Main.tileBatch.Draw(tileFlameData7.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num90, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num91) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), tileFlameData7.flameColor, _zero, 1f, drawData.tileSpriteEffect);
50	3001:							Main.tileBatch.Draw(tileFlameData6.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num69, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num70) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), tileFlameData6.flameColor, _zero, 1f, drawData.tileSpriteEffect);
51	3010:							Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num72, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num73) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
52	3029:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num115, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num116) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
53	3039:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num103, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num104) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
54	3049:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num106, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num107) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
55	3059:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num112, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num113) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
56	3069:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num109, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num110) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
57	3075:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
58	3089:						Main.tileBatch.Draw(tileFlameData9.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num118, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num119) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), tileFlameData9.flameColor, _zero, 1f, drawData.tileSpriteEffect);
59	3106:							Main.tileBatch.Draw(tileFlameData8.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num97, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num98) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), tileFlameData8.flameColor, _zero, 1f, drawData.tileSpriteEffect);
60	3115:							Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num100, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num101) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
61	3138:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num17, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num18) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
62	3148:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num26, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num27) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
63	3158:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num23, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num24) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
64	3168:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num35, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num36) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
65	3179:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num29, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num30) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
66	3189:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num20, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num21) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
67	3195:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
68	3209:						Main.tileBatch.Draw(tileFlameData3.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num32, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num33) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), tileFlameData3.flameColor, _zero, 1f, drawData.tileSpriteEffect);
69	3226:							Main.tileBatch.Draw(tileFlameData2.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num13, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num14) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), tileFlameData2.flameColor, _zero, 1f, drawData.tileSpriteEffect);
70	3235:							Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num15, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num16) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
71	3254:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num65, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num66) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
72	3265:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num45, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num46) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
73	3275:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num53, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num54) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
74	3285:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num62, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num63) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
75	3295:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num56, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num57) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
76	3305:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num48, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num49) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
77	3313:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num50, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num51) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(Utils.RandomInt(ref seed2, 90, 111), Utils.RandomInt(ref seed2, 90, 111), Utils.RandomInt(ref seed2, 90, 111), 0), _zero, 1f, drawData.tileSpriteEffect);
78	3318:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
79	3332:						Main.tileBatch.Draw(tileFlameData5.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num59, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num60) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), tileFlameData5.flameColor, _zero, 1f, drawData.tileSpriteEffect);
80	3349:							Main.tileBatch.Draw(tileFlameData4.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num39, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num40) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), tileFlameData4.flameColor, _zero, 1f, drawData.tileSpriteEffect);
81	3358:							Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num42, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num43) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
82	3388:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num134, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num135) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(100, 100, 100, 0), _zero, 1f, drawData.tileSpriteEffect);
83	3400:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num131, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num132) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(50, 50, 50, 0), _zero, 1f, drawData.tileSpriteEffect);
84	3413:							Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num125, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num126) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(25, 25, 25, 0), _zero, 1f, drawData.tileSpriteEffect);
85	3419:						Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(75, 75, 75, 0), _zero, 1f, drawData.tileSpriteEffect);
86	3433:							Main.tileBatch.Draw(tileFlameData11.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num128, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num129) + screenOffset, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), tileFlameData11.flameColor, _zero, 1f, drawData.tileSpriteEffect);
87	3450:								Main.tileBatch.Draw(tileFlameData10.flameTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num122, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num123) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), tileFlameData10.flameColor, _zero, 1f, drawData.tileSpriteEffect);
88	3485:					Main.tileBatch.Draw(TextureAssets.Flames[num9].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f + num10, (float)(tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + num11) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), color4, _zero, 1f, drawData.tileSpriteEffect);
89	3493:			Main.tileBatch.Draw(TextureAssets.Timer.Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(200, 200, 200, 0), _zero, 1f, drawData.tileSpriteEffect);
90	3497:			Main.tileBatch.Draw(TextureAssets.SunAltar.Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset, new Rectangle(drawData.tileFrameX, drawData.tileFrameY, drawData.tileWidth, drawData.tileHeight), new Color(Main.mouseTextColor / 2, Main.mouseTextColor / 2, Main.mouseTextColor / 2, 0), _zero, 1f, drawData.tileSpriteEffect);
91	3508:			Vector2 position = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - (float)drawData.tileWidth / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop) + screenOffset + vector2;
92	3695:			Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
93	3704:			drawData.tileTop -= 16 * drawData.tileFrameY;
94	3773:		Main.tileBatch.Draw(TextureAssets.XmasTree[0].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop + num) + screenOffset, new Rectangle(0, 0, 64, 128), color, _zero, 1f, SpriteEffects.None);
95	3782:			Main.tileBatch.Draw(TextureAssets.XmasTree[3].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop + num) + screenOffset, new Rectangle(66 * num2, 0, 64, 128), color2, _zero, 1f, SpriteEffects.None);
96	3787:			Main.tileBatch.Draw(TextureAssets.XmasTree[1].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop + num) + screenOffset, new Rectangle(66 * num3, 0, 64, 128), color, _zero, 1f, SpriteEffects.None);
97	3792:			Main.tileBatch.Draw(TextureAssets.XmasTree[2].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop + num) + screenOffset, new Rectangle(66 * num4, 0, 64, 128), color, _zero, 1f, SpriteEffects.None);
98	3797:			Main.tileBatch.Draw(TextureAssets.XmasTree[4].Value, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)drawData.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + drawData.tileTop + num) + screenOffset, new Rectangle(66 * num5, 130 * Main.tileFrame[171], 64, 128), new Color(255, 255, 255, 255), _zero, 1f, SpriteEffects.None);
99	4368:				drawData.tileHeight = 18;
100	4372:				drawData.glowSourceRect = new Rectangle(16 * (num % 2), drawData.tileFrameY + drawData.addFrY, drawData.tileWidth, drawData.tileHeight);
101	4562:	private void GetTileDrawData(int x, int y, Tile tileCache, ushort typeCache, ref short tileFrameX, ref short tileFrameY, out int tileWidth, out int tileHeight, out int tileTop, out int halfBrickHeight, out int addFrX, out int addFrY, out SpriteEffects tileSpriteEffect, out Texture2D glowTexture, out Rectangle glowSourceRect, out Color glowColor)
102	4564:		tileTop = 0;
103	4565:		tileWidth = 16;
104	4566:		tileHeight = 16;
105	4578:			tileHeight = 38;
106	4579:			tileWidth = 36;
107	4580:			tileTop = 2;
108	4584:			tileHeight = 46;
109	4585:			tileWidth = 56;
110	4600:			tileWidth = 20;
111	4601:			tileHeight = 20;
112	4615:				tileTop = -2;
113	4619:				tileTop = 2;
114	4627:			tileTop = 2;
115	4631:			tileWidth = 36;
116	4634:			tileHeight = 44;
117	4640:				tileTop = 2;
118	4644:			tileTop -= 2;
119	4645:			tileHeight = 20;
120	4673:			tileTop -= num28;
121	4680:			tileTop += 2;
122	4693:			tileWidth = 20;
123	4694:			tileHeight = 20;
124	4709:			tileWidth = 20;
125	4710:			tileHeight = 20;
126	4713:			tileWidth = 20;
127	4714:			tileHeight = 18;
128	4718:			tileWidth = 20;
129	4719:			tileHeight = 20;
130	4725:			tileWidth = 20;
131	4726:			tileHeight = 20;
132	4729:				tileTop = 4;
133	4747:			tileTop = 2;
134	4751:			tileTop = 2;
135	4774:			tileTop = 2;
136	4778:			tileTop = 2;
137	4782:			tileTop = 2;
138	4794:			tileTop = 2;
139	4809:			tileTop = 2;
140	4892:			tileHeight = 20;
141	4893:			tileTop = -4;
142	4911:			tileHeight = 32;
143	4912:			tileTop = -14;
144	4927:			tileHeight = 20;
145	4936:			tileHeight = 18;
146	4943:			tileHeight = 18;
147	4976:			tileHeight = 18;
148	4980:			tileHeight = 18;
149	5003:				tileWidth = 18;
150	5005:			tileHeight = 20;
151	

```


---

## 🤖 Assistant · 2026-08-11T15:58:06.182Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The grep output was truncated (only first 150 lines). Let me get the full list of tileWidth/tileHeight/tileTop assignments in the GetTileDrawData region (4562-5700). Let me grep with more targeted approach, and read the GetTileDrawData region directly. It's about 1100 lines. Let me read it in chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:06.276Z · glm-x-preview-260804

```
现在读取 GetTileDrawData 巨型 switch 的完整区域。
```


---

## 🤖 Assistant · 2026-08-11T15:58:06.531Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "offset": 4562,
 "limit": 400
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:06.549Z

**📎 ToolResult**

```
4562		private void GetTileDrawData(int x, int y, Tile tileCache, ushort typeCache, ref short tileFrameX, ref short tileFrameY, out int tileWidth, out int tileHeight, out int tileTop, out int halfBrickHeight, out int addFrX, out int addFrY, out SpriteEffects tileSpriteEffect, out Texture2D glowTexture, out Rectangle glowSourceRect, out Color glowColor)
4563		{
4564			tileTop = 0;
4565			tileWidth = 16;
4566			tileHeight = 16;
4567			halfBrickHeight = 0;
4568			addFrY = Main.tileFrame[typeCache] * 38;
4569			addFrX = 0;
4570			tileSpriteEffect = SpriteEffects.None;
4571			glowTexture = null;
4572			glowSourceRect = Rectangle.Empty;
4573			glowColor = Color.Transparent;
4574			Color color = Lighting.GetColor(x, y);
4575			switch (typeCache)
4576			{
4577			case 752:
4578				tileHeight = 38;
4579				tileWidth = 36;
4580				tileTop = 2;
4581				break;
4582			case 751:
4583			{
4584				tileHeight = 46;
4585				tileWidth = 56;
4586				int num3 = (x + y * 2) % 7;
4587				tileFrameY += (short)(num3 * 46);
4588				break;
4589			}
4590			case 739:
4591			case 748:
4592			{
4593				int num19 = Main.tileFrame[typeCache];
4594				addFrY = num19 * 90;
4595				break;
4596			}
4597			case 726:
4598				tileFrameX = 0;
4599				tileFrameY = 0;
4600				tileWidth = 20;
4601				tileHeight = 20;
4602				break;
4603			case 719:
4604			{
4605				int num34 = (x + y + (int)(Main.GlobalTimeWrappedHourly * 15f)) % 14;
4606				int num35 = num34 / 4;
4607				int num36 = num34 % 4;
4608				addFrX += 288 * num35;
4609				addFrY += 270 * num36;
4610				break;
4611			}
4612			case 443:
4613				if (tileFrameX / 36 >= 2)
4614				{
4615					tileTop = -2;
4616				}
4617				else
4618				{
4619					tileTop = 2;
4620				}
4621				break;
4622			case 571:
4623				if (x % 2 == 0)
4624				{
4625					tileSpriteEffect = SpriteEffects.FlipHorizontally;
4626				}
4627				tileTop = 2;
4628				break;
4629			case 698:
4630			{
4631				tileWidth = 36;
4632				int num62 = tileFrameX / 18;
4633				tileFrameX = (short)(num62 * 38);
4634				tileHeight = 44;
4635				break;
4636			}
4637			case 136:
4638				if (tileFrameX == 0)
4639				{
4640					tileTop = 2;
4641				}
4642				break;
4643			case 561:
4644				tileTop -= 2;
4645				tileHeight = 20;
4646				addFrY = tileFrameY / 18 * 4;
4647				break;
4648			case 518:
4649			{
4650				int num28 = tileCache.liquid / 16;
4651				num28 -= 3;
4652				if (WorldGen.SolidTile(x, y - 1) && num28 > 8)
4653				{
4654					num28 = 8;
4655				}
4656				if (tileCache.liquid == 0)
4657				{
4658					Tile tileSafely = Framing.GetTileSafely(x, y + 1);
4659					if (tileSafely.nactive())
4660					{
4661						switch (tileSafely.blockType())
4662						{
4663						case 1:
4664							num28 = -16 + Math.Max(8, tileSafely.liquid / 16);
4665							break;
4666						case 2:
4667						case 3:
4668							num28 -= 4;
4669							break;
4670						}
4671					}
4672				}
4673				tileTop -= num28;
4674				break;
4675			}
4676			case 330:
4677			case 331:
4678			case 332:
4679			case 333:
4680				tileTop += 2;
4681				break;
4682			case 129:
4683				addFrY = 0;
4684				if (tileFrameX >= 324)
4685				{
4686					int num56 = (tileFrameX - 324) / 18;
4687					int num57 = (num56 + Main.tileFrame[typeCache]) % 6 - num56;
4688					addFrX = num57 * 18;
4689				}
4690				break;
4691			case 5:
4692			{
4693				tileWidth = 20;
4694				tileHeight = 20;
4695				int treeBiome = GetTreeBiome(x, y, tileFrameX, tileFrameY);
4696				tileFrameX += (short)(176 * (treeBiome + 1));
4697				break;
4698			}
4699			case 583:
4700			case 584:
4701			case 585:
4702			case 586:
4703			case 587:
4704			case 588:
4705			case 589:
4706			case 596:
4707			case 616:
4708			case 634:
4709				tileWidth = 20;
4710				tileHeight = 20;
4711				break;
4712			case 476:
4713				tileWidth = 20;
4714				tileHeight = 18;
4715				break;
4716			case 323:
4717			{
4718				tileWidth = 20;
4719				tileHeight = 20;
4720				int palmTreeBiome = GetPalmTreeBiome(x, y);
4721				tileFrameY = (short)(22 * palmTreeBiome);
4722				break;
4723			}
4724			case 4:
4725				tileWidth = 20;
4726				tileHeight = 20;
4727				if (WorldGen.SolidTile(x, y - 1))
4728				{
4729					tileTop = 4;
4730				}
4731				break;
4732			case 78:
4733			case 85:
4734			case 133:
4735			case 134:
4736			case 173:
4737			case 210:
4738			case 233:
4739			case 254:
4740			case 283:
4741			case 378:
4742			case 457:
4743			case 466:
4744			case 520:
4745			case 651:
4746			case 652:
4747				tileTop = 2;
4748				break;
4749			case 100:
4750			{
4751				tileTop = 2;
4752				int num58 = tileFrameY / 2016;
4753				addFrY -= 2016 * num58;
4754				addFrX += 72 * num58;
4755				break;
4756			}
4757			case 530:
4758			{
4759				int num51 = y - tileFrameY % 36 / 18 + 2;
4760				int num52 = x - tileFrameX % 54 / 18;
4761				WorldGen.GetBiomeInfluence(num52, num52 + 3, num51, num51, out var corruptCount2, out var crimsonCount2, out var hallowedCount2);
4762				int num53 = corruptCount2;
4763				if (num53 < crimsonCount2)
4764				{
4765					num53 = crimsonCount2;
4766				}
4767				if (num53 < hallowedCount2)
4768				{
4769					num53 = hallowedCount2;
4770				}
4771				int num54 = 0;
4772				num54 = ((corruptCount2 != 0 || crimsonCount2 != 0 || hallowedCount2 != 0) ? ((hallowedCount2 == num53) ? 1 : ((crimsonCount2 != num53) ? 3 : 2)) : 0);
4773				addFrY += 36 * num54;
4774				tileTop = 2;
4775				break;
4776			}
4777			case 705:
4778				tileTop = 2;
4779				break;
4780			case 485:
4781			{
4782				tileTop = 2;
4783				int num14 = Main.tileFrameCounter[typeCache];
4784				num14 /= 5;
4785				int num15 = y - tileFrameY / 18;
4786				int num16 = x - tileFrameX / 18;
4787				num14 += num15 + num16;
4788				num14 %= 4;
4789				addFrY = num14 * 36;
4790				break;
4791			}
4792			case 489:
4793			{
4794				tileTop = 2;
4795				int num47 = y - tileFrameY / 18;
4796				int num48 = x - tileFrameX / 18;
4797				if (InAPlaceWithWind(num48, num47, 2, 3))
4798				{
4799					int num49 = Main.tileFrameCounter[typeCache];
4800					num49 /= 5;
4801					num49 += num47 + num48;
4802					num49 %= 16;
4803					addFrY = num49 * 54;
4804				}
4805				break;
4806			}
4807			case 490:
4808			{
4809				tileTop = 2;
4810				int y2 = y - tileFrameY / 18;
4811				int x2 = x - tileFrameX / 18;
4812				bool num20 = InAPlaceWithWind(x2, y2, 2, 2);
4813				int num21 = (num20 ? Main.tileFrame[typeCache] : 0);
4814				int num22 = 0;
4815				if (num20)
4816				{
4817					if (Math.Abs(Main.WindForVisuals) > 0.5f)
4818					{
4819						switch (Main.weatherVaneBobframe)
4820						{
4821						case 0:
4822							num22 = 0;
4823							break;
4824						case 1:
4825							num22 = 1;
4826							break;
4827						case 2:
4828							num22 = 2;
4829							break;
4830						case 3:
4831							num22 = 1;
4832							break;
4833						case 4:
4834							num22 = 0;
4835							break;
4836						case 5:
4837							num22 = -1;
4838							break;
4839						case 6:
4840							num22 = -2;
4841							break;
4842						case 7:
4843							num22 = -1;
4844							break;
4845						}
4846					}
4847					else
4848					{
4849						switch (Main.weatherVaneBobframe)
4850						{
4851						case 0:
4852							num22 = 0;
4853							break;
4854						case 1:
4855							num22 = 1;
4856							break;
4857						case 2:
4858							num22 = 0;
4859							break;
4860						case 3:
4861							num22 = -1;
4862							break;
4863						case 4:
4864							num22 = 0;
4865							break;
4866						case 5:
4867							num22 = 1;
4868							break;
4869						case 6:
4870							num22 = 0;
4871							break;
4872						case 7:
4873							num22 = -1;
4874							break;
4875						}
4876					}
4877				}
4878				num21 += num22;
4879				if (num21 < 0)
4880				{
4881					num21 += 12;
4882				}
4883				num21 %= 12;
4884				addFrY = num21 * 36;
4885				break;
4886			}
4887			case 33:
4888			case 49:
4889			case 174:
4890			case 372:
4891			case 646:
4892				tileHeight = 20;
4893				tileTop = -4;
4894				break;
4895			case 529:
4896			{
4897				int num38 = y + 1;
4898				WorldGen.GetBiomeInfluence(x, x, num38, num38, out var corruptCount, out var crimsonCount, out var hallowedCount);
4899				int num39 = corruptCount;
4900				if (num39 < crimsonCount)
4901				{
4902					num39 = crimsonCount;
4903				}
4904				if (num39 < hallowedCount)
4905				{
4906					num39 = hallowedCount;
4907				}
4908				int num40 = 0;
4909				num40 = ((corruptCount == 0 && crimsonCount == 0 && hallowedCount == 0) ? ((x < WorldGen.beachDistance || x > Main.maxTilesX - WorldGen.beachDistance) ? 1 : 0) : ((hallowedCount == num39) ? 2 : ((crimsonCount != num39) ? 4 : 3)));
4910				addFrY += 34 * num40 - tileFrameY;
4911				tileHeight = 32;
4912				tileTop = -14;
4913				if (x % 2 == 0)
4914				{
4915					tileSpriteEffect = SpriteEffects.FlipHorizontally;
4916				}
4917				break;
4918			}
4919			case 3:
4920			case 24:
4921			case 61:
4922			case 71:
4923			case 110:
4924			case 201:
4925			case 637:
4926			case 703:
4927				tileHeight = 20;
4928				if (x % 2 == 0)
4929				{
4930					tileSpriteEffect = SpriteEffects.FlipHorizontally;
4931				}
4932				break;
4933			case 20:
4934			case 590:
4935			case 595:
4936				tileHeight = 18;
4937				if (x % 2 == 0)
4938				{
4939					tileSpriteEffect = SpriteEffects.FlipHorizontally;
4940				}
4941				break;
4942			case 615:
4943				tileHeight = 18;
4944				if (x % 2 == 0)
4945				{
4946					tileSpriteEffect = SpriteEffects.FlipHorizontally;
4947				}
4948				break;
4949			case 16:
4950			case 17:
4951			case 26:
4952			case 32:
4953			case 69:
4954			case 72:
4955			case 77:
4956			case 124:
4957			case 137:
4958			case 138:
4959			case 352:
4960			case 462:
4961			case 487:

```


---

## 🤖 Assistant · 2026-08-11T15:58:07.325Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileWidth = \\|tileHeight = \\|tileTop = \\|tileTop -= \\|tileTop += \\|addFrX = \\|addFrY = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | awk -F: '$1>=4562 && $1<=5800'",
 "description": "List dimension assignments inside GetTileDrawData range"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:10.962Z

**📎 ToolResult**

```
4564:		tileTop = 0;
4565:		tileWidth = 16;
4566:		tileHeight = 16;
4568:		addFrY = Main.tileFrame[typeCache] * 38;
4569:		addFrX = 0;
4578:			tileHeight = 38;
4579:			tileWidth = 36;
4580:			tileTop = 2;
4584:			tileHeight = 46;
4585:			tileWidth = 56;
4594:			addFrY = num19 * 90;
4600:			tileWidth = 20;
4601:			tileHeight = 20;
4615:				tileTop = -2;
4619:				tileTop = 2;
4627:			tileTop = 2;
4631:			tileWidth = 36;
4634:			tileHeight = 44;
4640:				tileTop = 2;
4644:			tileTop -= 2;
4645:			tileHeight = 20;
4646:			addFrY = tileFrameY / 18 * 4;
4673:			tileTop -= num28;
4680:			tileTop += 2;
4683:			addFrY = 0;
4688:				addFrX = num57 * 18;
4693:			tileWidth = 20;
4694:			tileHeight = 20;
4709:			tileWidth = 20;
4710:			tileHeight = 20;
4713:			tileWidth = 20;
4714:			tileHeight = 18;
4718:			tileWidth = 20;
4719:			tileHeight = 20;
4725:			tileWidth = 20;
4726:			tileHeight = 20;
4729:				tileTop = 4;
4747:			tileTop = 2;
4751:			tileTop = 2;
4774:			tileTop = 2;
4778:			tileTop = 2;
4782:			tileTop = 2;
4789:			addFrY = num14 * 36;
4794:			tileTop = 2;
4803:				addFrY = num49 * 54;
4809:			tileTop = 2;
4884:			addFrY = num21 * 36;
4892:			tileHeight = 20;
4893:			tileTop = -4;
4911:			tileHeight = 32;
4912:			tileTop = -14;
4927:			tileHeight = 20;
4936:			tileHeight = 18;
4943:			tileHeight = 18;
4976:			tileHeight = 18;
4980:			tileHeight = 18;
5003:				tileWidth = 18;
5005:			tileHeight = 20;
5010:			tileTop += 2;
5019:				tileHeight = 18;
5026:				tileHeight = 18;
5033:				tileHeight = 18;
5039:				tileHeight = 18;
5044:			tileTop = 2;
5045:			tileHeight = 18;
5050:			tileHeight = 20;
5051:			tileTop = -2;
5058:			tileWidth = 20;
5059:			tileHeight = 20;
5060:			tileTop = -2;
5067:			tileTop = 2;
5077:			tileTop = -2;
5086:			tileTop = 2;
5090:			tileTop = 2;
5099:			tileTop = -12;
5100:			tileHeight = 32;
5110:			tileTop = -2;
5113:				tileHeight = 18;
5117:				tileTop = 0;
5122:			tileWidth = 32;
5123:			tileHeight = 38;
5126:				tileTop -= 6;
5130:				tileTop -= 20;
5155:			tileWidth = 20;
5156:			tileHeight = 16;
5157:			tileTop += 2;
5165:			tileWidth = 24;
5166:			tileHeight = 34;
5167:			tileTop -= 16;
5175:			tileWidth = 20;
5176:			tileHeight = 20;
5177:			tileTop -= 2;
5183:					addFrY = 22;
5187:					addFrY = 0;
5192:				addFrY = 0;
5196:				addFrY = 22;
5201:			tileWidth = 26;
5202:			tileHeight = 18;
5205:				tileTop = -2;
5215:			tileTop = 2;
5254:			tileTop = 2;
5258:			tileTop = 2;
5266:			tileTop = 2;
5270:			tileTop = 2;
5279:				tileTop = 2;
5283:			tileWidth = 20;
5286:				tileTop = 2;
5290:				tileTop = -2;
5294:			tileTop = 2;
5319:						addFrY = num6 * 36;
5327:						addFrY = num6 * 36;
5331:			tileTop = 2;
5349:			tileTop = 2;
5352:			tileTop = 2;
5357:			addFrX = Main.tileFrame[typeCache] * 54;
5358:			addFrY = 0;
5359:			tileTop = 2;
5362:			tileTop -= 8;
5363:			tileHeight = 26;
5364:			tileWidth = 24;
5371:			addFrY = 0;
5374:			addFrY = Main.tileFrame[typeCache] * 54;
5388:			addFrY = Main.tileFrame[typeCache] * 54;
5389:			tileTop = 2;
5392:			addFrY = Main.tileFrame[typeCache] * 38;
5393:			tileTop = 2;
5397:			addFrY = Main.tileFrame[typeCache] * 72;
5398:			tileTop = 2;
5401:			tileTop = 2;
5402:			addFrX = 54;
5405:			addFrY = Main.tileFrame[typeCache] * 90;
5409:			tileTop = 2;
5423:				tileHeight = 18;
5434:			addFrY = Main.tileFrame[typeCache] * 36;
5437:			addFrY = 0;
5438:			tileTop = 2;
5441:			tileTop = 2;
5445:			tileHeight = 16;
5448:				tileHeight = 18;
5459:			addFrY = num55 * 56;
5470:			addFrY = num50 * 54;
5475:			addFrY = 0;
5476:			tileTop = 2;
5482:			addFrY = num46 * 54;
5486:			addFrY = Main.tileFrame[typeCache] * 54;
5495:			addFrY = num44 * 54;
5506:			addFrY = num41 * 54;
5511:			tileHeight = 16;
5514:				tileHeight = 18;
5521:			addFrY = num37 * 38;
5530:			addFrY = Main.tileFrame[typeCache] * 36;
5533:			tileTop = 2;
5534:			addFrY = Main.tileFrame[typeCache] * 36;
5540:				addFrX = -18;
5542:			tileTop = 2;
5545:				addFrY = (short)(18 * frameData2);
5549:				addFrY = Main.tileFrame[typeCache] * 18;
5553:				addFrY = 0;
5561:				addFrX = -36;
5563:			tileTop = 2;
5568:				addFrY = (short)(36 * frameData);
5572:				addFrY = Main.tileFrame[typeCache] * 36;
5576:				addFrY = 0;
5581:			addFrY = Main.tileFrame[typeCache] * 54;
5587:			tileTop = 2;
5588:			addFrY = Main.tileFrame[typeCache] * 54;
5591:			tileTop = 2;
5594:				addFrY = Main.tileFrame[typeCache] * 36;
5598:				addFrY = 0;
5602:			tileTop = 2;
5605:				addFrY = Main.tileFrame[typeCache] * 36;
5609:				addFrY = 0;
5613:			addFrY = Main.tileFrame[typeCache] * 18;
5618:			addFrY = Main.tileFrame[typeCache] * 36;
5619:			tileTop = 2;
5624:			addFrY = Main.tileFrame[typeCache] * 54;
5625:			tileTop = 2;
5648:			addFrX = num23 * 18;
5649:			addFrY = 0;
5675:			addFrX = num18 * 18;
5676:			addFrY = 0;
5689:			addFrX = num17 * 18;
5690:			addFrY = 0;
5698:			tileTop += 4;
5705:			tileWidth = 20;
5706:			tileHeight = 20;
5710:				tileTop = -4;
5713:				tileTop = -2;
5714:				tileWidth = 24;
5717:				tileTop = -2;
5763:			tileTop = 2;
5777:				addFrY = Main.bunnyCageFrame[bigAnimalCageFrame] * 54;
5781:				addFrY = Main.turtleCageFrame[bigAnimalCageFrame] * 54;
5784:				addFrY = Main.owlCageFrame[bigAnimalCageFrame] * 54;
5796:				addFrY = Main.squirrelCageFrame[bigAnimalCageFrame] * 54;
5799:				addFrY = Main.mallardCageFrame[bigAnimalCageFrame] * 54;

```


---

## 🤖 Assistant · 2026-08-11T15:58:13.070Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to read the rest of GetTileDrawData (4961-5850) to get the case labels for all these assignments. Let me read that region.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:13.312Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 450,
 "offset": 4961
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:13.322Z

**📎 ToolResult**

```
4961			case 487:
4962			case 488:
4963			case 574:
4964			case 575:
4965			case 576:
4966			case 577:
4967			case 578:
4968			case 664:
4969			case 695:
4970			case 704:
4971			case 712:
4972			case 713:
4973			case 714:
4974			case 715:
4975			case 716:
4976				tileHeight = 18;
4977				break;
4978			case 79:
4979			{
4980				tileHeight = 18;
4981				int num33 = tileFrameY / 2016;
4982				addFrY -= 2016 * num33;
4983				addFrX += 144 * num33;
4984				break;
4985			}
4986			case 90:
4987			{
4988				int num32 = tileFrameY / 2016;
4989				addFrY -= 2016 * num32;
4990				addFrX += 144 * num32;
4991				break;
4992			}
4993			case 18:
4994			{
4995				int num31 = tileFrameX / 2016;
4996				addFrX -= 2016 * num31;
4997				addFrY += 20 * num31;
4998				break;
4999			}
5000			case 711:
5001				if (tileFrameX > 0)
5002				{
5003					tileWidth = 18;
5004				}
5005				tileHeight = 20;
5006				glowTexture = TextureAssets.Tile[711].Value;
5007				glowSourceRect = new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight);
5008				break;
5009			case 654:
5010				tileTop += 2;
5011				break;
5012			case 14:
5013			case 21:
5014			case 411:
5015			case 467:
5016			case 469:
5017				if (tileFrameY == 18)
5018				{
5019					tileHeight = 18;
5020				}
5021				break;
5022			case 15:
5023			case 497:
5024				if (tileFrameY % 40 == 18)
5025				{
5026					tileHeight = 18;
5027				}
5028				break;
5029			case 172:
5030			case 376:
5031				if (tileFrameY % 38 == 18)
5032				{
5033					tileHeight = 18;
5034				}
5035				break;
5036			case 27:
5037				if (tileFrameY % 74 == 54)
5038				{
5039					tileHeight = 18;
5040				}
5041				break;
5042			case 132:
5043			case 135:
5044				tileTop = 2;
5045				tileHeight = 18;
5046				break;
5047			case 82:
5048			case 83:
5049			case 84:
5050				tileHeight = 20;
5051				tileTop = -2;
5052				if (x % 2 == 0)
5053				{
5054					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5055				}
5056				break;
5057			case 324:
5058				tileWidth = 20;
5059				tileHeight = 20;
5060				tileTop = -2;
5061				if (x % 2 == 0)
5062				{
5063					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5064				}
5065				break;
5066			case 494:
5067				tileTop = 2;
5068				break;
5069			case 52:
5070			case 62:
5071			case 115:
5072			case 205:
5073			case 382:
5074			case 528:
5075			case 636:
5076			case 638:
5077				tileTop = -2;
5078				if (x % 2 == 0)
5079				{
5080					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5081				}
5082				break;
5083			case 80:
5084			case 142:
5085			case 143:
5086				tileTop = 2;
5087				break;
5088			case 139:
5089			{
5090				tileTop = 2;
5091				int num5 = tileFrameY / 2016;
5092				addFrY -= 2016 * num5;
5093				addFrX += 72 * num5;
5094				break;
5095			}
5096			case 73:
5097			case 74:
5098			case 113:
5099				tileTop = -12;
5100				tileHeight = 32;
5101				if (x % 2 == 0)
5102				{
5103					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5104				}
5105				break;
5106			case 388:
5107			case 389:
5108			{
5109				int num59 = 94;
5110				tileTop = -2;
5111				if (tileFrameY == num59 - 20 || tileFrameY == num59 * 2 - 20 || tileFrameY == 0 || tileFrameY == num59)
5112				{
5113					tileHeight = 18;
5114				}
5115				if (tileFrameY != 0 && tileFrameY != num59)
5116				{
5117					tileTop = 0;
5118				}
5119				break;
5120			}
5121			case 227:
5122				tileWidth = 32;
5123				tileHeight = 38;
5124				if (tileFrameX == 238)
5125				{
5126					tileTop -= 6;
5127				}
5128				else
5129				{
5130					tileTop -= 20;
5131				}
5132				if (tileFrameX == 204)
5133				{
5134					WorldGen.GetCactusType(x, y, tileFrameX, tileFrameY, out var evil, out var good, out var crimson);
5135					if (good)
5136					{
5137						tileFrameX += 238;
5138					}
5139					if (evil)
5140					{
5141						tileFrameX += 204;
5142					}
5143					if (crimson)
5144					{
5145						tileFrameX += 272;
5146					}
5147				}
5148				if (x % 2 == 0)
5149				{
5150					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5151				}
5152				break;
5153			case 624:
5154			case 700:
5155				tileWidth = 20;
5156				tileHeight = 16;
5157				tileTop += 2;
5158				if (x % 2 == 0)
5159				{
5160					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5161				}
5162				break;
5163			case 656:
5164			case 701:
5165				tileWidth = 24;
5166				tileHeight = 34;
5167				tileTop -= 16;
5168				if (x % 2 == 0)
5169				{
5170					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5171				}
5172				break;
5173			case 579:
5174			{
5175				tileWidth = 20;
5176				tileHeight = 20;
5177				tileTop -= 2;
5178				bool flag = (float)(x * 16 + 8) > Main.LocalPlayer.Center.X;
5179				if (tileFrameX > 0)
5180				{
5181					if (flag)
5182					{
5183						addFrY = 22;
5184					}
5185					else
5186					{
5187						addFrY = 0;
5188					}
5189				}
5190				else if (flag)
5191				{
5192					addFrY = 0;
5193				}
5194				else
5195				{
5196					addFrY = 22;
5197				}
5198				break;
5199			}
5200			case 567:
5201				tileWidth = 26;
5202				tileHeight = 18;
5203				if (tileFrameY == 0)
5204				{
5205					tileTop = -2;
5206				}
5207				if (x % 2 == 0)
5208				{
5209					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5210				}
5211				break;
5212			case 185:
5213			case 186:
5214			case 187:
5215				tileTop = 2;
5216				switch (typeCache)
5217				{
5218				case 185:
5219					if (tileFrameY == 18 && tileFrameX >= 576 && tileFrameX <= 882)
5220					{
5221						Main.tileShine2[185] = true;
5222					}
5223					else
5224					{
5225						Main.tileShine2[185] = false;
5226					}
5227					if (tileFrameY == 18)
5228					{
5229						int num27 = tileFrameX / 1908;
5230						addFrX -= 1908 * num27;
5231						addFrY += 18 * num27;
5232					}
5233					break;
5234				case 186:
5235					if (tileFrameX >= 864 && tileFrameX <= 1170)
5236					{
5237						Main.tileShine2[186] = true;
5238					}
5239					else
5240					{
5241						Main.tileShine2[186] = false;
5242					}
5243					break;
5244				case 187:
5245				{
5246					int num26 = tileFrameX / 1890;
5247					addFrX -= 1890 * num26;
5248					addFrY += 36 * num26;
5249					break;
5250				}
5251				}
5252				break;
5253			case 650:
5254				tileTop = 2;
5255				break;
5256			case 649:
5257			{
5258				tileTop = 2;
5259				int num25 = tileFrameX / 1908;
5260				addFrX -= 1908 * num25;
5261				addFrY += 18 * num25;
5262				break;
5263			}
5264			case 647:
5265			case 706:
5266				tileTop = 2;
5267				break;
5268			case 648:
5269			{
5270				tileTop = 2;
5271				int num24 = tileFrameX / 1890;
5272				addFrX -= 1890 * num24;
5273				addFrY += 36 * num24;
5274				break;
5275			}
5276			case 178:
5277				if (tileFrameY <= 36)
5278				{
5279					tileTop = 2;
5280				}
5281				break;
5282			case 184:
5283				tileWidth = 20;
5284				if (tileFrameY <= 36)
5285				{
5286					tileTop = 2;
5287				}
5288				else if (tileFrameY <= 108)
5289				{
5290					tileTop = -2;
5291				}
5292				break;
5293			case 519:
5294				tileTop = 2;
5295				if (x % 2 == 0)
5296				{
5297					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5298				}
5299				break;
5300			case 493:
5301				if (tileFrameY == 0)
5302				{
5303					int num6 = Main.tileFrameCounter[typeCache];
5304					float num7 = Math.Abs(Main.WindForVisuals);
5305					int num8 = y - tileFrameY / 18;
5306					int num9 = x - tileFrameX / 18;
5307					if (!InAPlaceWithWind(x, num8, 1, 1))
5308					{
5309						num7 = 0f;
5310					}
5311					if (!(num7 < 0.1f))
5312					{
5313						if (num7 < 0.5f)
5314						{
5315							num6 /= 20;
5316							num6 += num8 + num9;
5317							num6 %= 6;
5318							num6 = ((!(Main.WindForVisuals < 0f)) ? (num6 + 1) : (6 - num6));
5319							addFrY = num6 * 36;
5320						}
5321						else
5322						{
5323							num6 /= 10;
5324							num6 += num8 + num9;
5325							num6 %= 6;
5326							num6 = ((!(Main.WindForVisuals < 0f)) ? (num6 + 7) : (12 - num6));
5327							addFrY = num6 * 36;
5328						}
5329					}
5330				}
5331				tileTop = 2;
5332				break;
5333			case 28:
5334			case 105:
5335			case 470:
5336			case 475:
5337			case 506:
5338			case 547:
5339			case 548:
5340			case 552:
5341			case 560:
5342			case 597:
5343			case 613:
5344			case 621:
5345			case 622:
5346			case 623:
5347			case 653:
5348			case 699:
5349				tileTop = 2;
5350				break;
5351			case 617:
5352				tileTop = 2;
5353				tileFrameY %= 144;
5354				tileFrameX %= 54;
5355				break;
5356			case 614:
5357				addFrX = Main.tileFrame[typeCache] * 54;
5358				addFrY = 0;
5359				tileTop = 2;
5360				break;
5361			case 81:
5362				tileTop -= 8;
5363				tileHeight = 26;
5364				tileWidth = 24;
5365				if (x % 2 == 0)
5366				{
5367					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5368				}
5369				break;
5370			case 272:
5371				addFrY = 0;
5372				break;
5373			case 106:
5374				addFrY = Main.tileFrame[typeCache] * 54;
5375				break;
5376			case 300:
5377			case 301:
5378			case 302:
5379			case 303:
5380			case 304:
5381			case 305:
5382			case 306:
5383			case 307:
5384			case 308:
5385			case 354:
5386			case 355:
5387			case 499:
5388				addFrY = Main.tileFrame[typeCache] * 54;
5389				tileTop = 2;
5390				break;
5391			case 377:
5392				addFrY = Main.tileFrame[typeCache] * 38;
5393				tileTop = 2;
5394				break;
5395			case 463:
5396			case 464:
5397				addFrY = Main.tileFrame[typeCache] * 72;
5398				tileTop = 2;
5399				break;
5400			case 491:
5401				tileTop = 2;
5402				addFrX = 54;
5403				break;
5404			case 379:
5405				addFrY = Main.tileFrame[typeCache] * 90;
5406				break;
5407			case 349:
5408			{
5409				tileTop = 2;
5410				int num63 = tileFrameX % 36;

```


---

## 🤖 Assistant · 2026-08-11T15:58:14.247Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me continue reading 5410-5900.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:14.499Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 480,
 "offset": 5410
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:14.507Z

**📎 ToolResult**

```
5410				int num63 = tileFrameX % 36;
5411				int num64 = tileFrameY % 54;
5412				if (Animation.GetTemporaryFrame(x - num63 / 18, y - num64 / 18, out var frameData4))
5413				{
5414					tileFrameX = (short)(36 * frameData4 + num63);
5415				}
5416				break;
5417			}
5418			case 441:
5419			case 468:
5420			{
5421				if (tileFrameY == 18)
5422				{
5423					tileHeight = 18;
5424				}
5425				int num60 = tileFrameX % 36;
5426				int num61 = tileFrameY % 38;
5427				if (Animation.GetTemporaryFrame(x - num60 / 18, y - num61 / 18, out var frameData3))
5428				{
5429					tileFrameY = (short)(38 * frameData3 + num61);
5430				}
5431				break;
5432			}
5433			case 390:
5434				addFrY = Main.tileFrame[typeCache] * 36;
5435				break;
5436			case 412:
5437				addFrY = 0;
5438				tileTop = 2;
5439				break;
5440			case 36:
5441				tileTop = 2;
5442				break;
5443			case 406:
5444			{
5445				tileHeight = 16;
5446				if (tileFrameY % 54 >= 36)
5447				{
5448					tileHeight = 18;
5449				}
5450				int num55 = Main.tileFrame[typeCache];
5451				if (tileFrameY >= 108)
5452				{
5453					num55 = 6 - tileFrameY / 54;
5454				}
5455				else if (tileFrameY >= 54)
5456				{
5457					num55 = Main.tileFrame[typeCache] - 1;
5458				}
5459				addFrY = num55 * 56;
5460				addFrY += tileFrameY / 54 * 2;
5461				break;
5462			}
5463			case 452:
5464			{
5465				int num50 = Main.tileFrame[typeCache];
5466				if (tileFrameX >= 54)
5467				{
5468					num50 = 0;
5469				}
5470				addFrY = num50 * 54;
5471				break;
5472			}
5473			case 455:
5474			{
5475				addFrY = 0;
5476				tileTop = 2;
5477				int num46 = 1 + Main.tileFrame[typeCache];
5478				if (!BirthdayParty.PartyIsUp)
5479				{
5480					num46 = 0;
5481				}
5482				addFrY = num46 * 54;
5483				break;
5484			}
5485			case 454:
5486				addFrY = Main.tileFrame[typeCache] * 54;
5487				break;
5488			case 453:
5489			{
5490				int num44 = Main.tileFrameCounter[typeCache];
5491				num44 /= 20;
5492				int num45 = y - tileFrameY / 18;
5493				num44 += num45 + x;
5494				num44 %= 3;
5495				addFrY = num44 * 54;
5496				break;
5497			}
5498			case 456:
5499			{
5500				int num41 = Main.tileFrameCounter[typeCache];
5501				num41 /= 20;
5502				int num42 = y - tileFrameY / 18;
5503				int num43 = x - tileFrameX / 18;
5504				num41 += num42 + num43;
5505				num41 %= 4;
5506				addFrY = num41 * 54;
5507				break;
5508			}
5509			case 405:
5510			{
5511				tileHeight = 16;
5512				if (tileFrameY > 0)
5513				{
5514					tileHeight = 18;
5515				}
5516				int num37 = Main.tileFrame[typeCache];
5517				if (tileFrameX >= 54)
5518				{
5519					num37 = 0;
5520				}
5521				addFrY = num37 * 38;
5522				break;
5523			}
5524			case 12:
5525			case 31:
5526			case 96:
5527			case 639:
5528			case 665:
5529			case 696:
5530				addFrY = Main.tileFrame[typeCache] * 36;
5531				break;
5532			case 238:
5533				tileTop = 2;
5534				addFrY = Main.tileFrame[typeCache] * 36;
5535				break;
5536			case 593:
5537			{
5538				if (tileFrameX >= 18)
5539				{
5540					addFrX = -18;
5541				}
5542				tileTop = 2;
5543				if (Animation.GetTemporaryFrame(x, y, out var frameData2))
5544				{
5545					addFrY = (short)(18 * frameData2);
5546				}
5547				else if (tileFrameX < 18)
5548				{
5549					addFrY = Main.tileFrame[typeCache] * 18;
5550				}
5551				else
5552				{
5553					addFrY = 0;
5554				}
5555				break;
5556			}
5557			case 594:
5558			{
5559				if (tileFrameX >= 36)
5560				{
5561					addFrX = -36;
5562				}
5563				tileTop = 2;
5564				int num29 = tileFrameX % 36;
5565				int num30 = tileFrameY % 36;
5566				if (Animation.GetTemporaryFrame(x - num29 / 18, y - num30 / 18, out var frameData))
5567				{
5568					addFrY = (short)(36 * frameData);
5569				}
5570				else if (tileFrameX < 36)
5571				{
5572					addFrY = Main.tileFrame[typeCache] * 36;
5573				}
5574				else
5575				{
5576					addFrY = 0;
5577				}
5578				break;
5579			}
5580			case 592:
5581				addFrY = Main.tileFrame[typeCache] * 54;
5582				break;
5583			case 228:
5584			case 231:
5585			case 243:
5586			case 247:
5587				tileTop = 2;
5588				addFrY = Main.tileFrame[typeCache] * 54;
5589				break;
5590			case 244:
5591				tileTop = 2;
5592				if (tileFrameX < 54)
5593				{
5594					addFrY = Main.tileFrame[typeCache] * 36;
5595				}
5596				else
5597				{
5598					addFrY = 0;
5599				}
5600				break;
5601			case 565:
5602				tileTop = 2;
5603				if (tileFrameX < 36)
5604				{
5605					addFrY = Main.tileFrame[typeCache] * 36;
5606				}
5607				else
5608				{
5609					addFrY = 0;
5610				}
5611				break;
5612			case 235:
5613				addFrY = Main.tileFrame[typeCache] * 18;
5614				break;
5615			case 217:
5616			case 218:
5617			case 564:
5618				addFrY = Main.tileFrame[typeCache] * 36;
5619				tileTop = 2;
5620				break;
5621			case 219:
5622			case 220:
5623			case 642:
5624				addFrY = Main.tileFrame[typeCache] * 54;
5625				tileTop = 2;
5626				break;
5627			case 270:
5628			case 271:
5629			case 581:
5630			{
5631				int num23 = Main.tileFrame[typeCache] + x % 6;
5632				if (x % 2 == 0)
5633				{
5634					num23 += 3;
5635				}
5636				if (x % 3 == 0)
5637				{
5638					num23 += 3;
5639				}
5640				if (x % 4 == 0)
5641				{
5642					num23 += 3;
5643				}
5644				while (num23 > 5)
5645				{
5646					num23 -= 6;
5647				}
5648				addFrX = num23 * 18;
5649				addFrY = 0;
5650				if (x % 2 == 0)
5651				{
5652					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5653				}
5654				break;
5655			}
5656			case 660:
5657			{
5658				int num18 = Main.tileFrame[typeCache] + x % 5;
5659				if (x % 2 == 0)
5660				{
5661					num18 += 3;
5662				}
5663				if (x % 3 == 0)
5664				{
5665					num18 += 3;
5666				}
5667				if (x % 4 == 0)
5668				{
5669					num18 += 3;
5670				}
5671				while (num18 > 4)
5672				{
5673					num18 -= 5;
5674				}
5675				addFrX = num18 * 18;
5676				addFrY = 0;
5677				if (x % 2 == 0)
5678				{
5679					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5680				}
5681				break;
5682			}
5683			case 572:
5684			{
5685				int num17;
5686				for (num17 = Main.tileFrame[typeCache] + x % 4; num17 > 3; num17 -= 4)
5687				{
5688				}
5689				addFrX = num17 * 18;
5690				addFrY = 0;
5691				if (x % 2 == 0)
5692				{
5693					tileSpriteEffect = SpriteEffects.FlipHorizontally;
5694				}
5695				break;
5696			}
5697			case 428:
5698				tileTop += 4;
5699				if (PressurePlateHelper.PressurePlatesPressed.ContainsKey(new Point(x, y)))
5700				{
5701					addFrX += 18;
5702				}
5703				break;
5704			case 442:
5705				tileWidth = 20;
5706				tileHeight = 20;
5707				switch (tileFrameX / 22)
5708				{
5709				case 1:
5710					tileTop = -4;
5711					break;
5712				case 2:
5713					tileTop = -2;
5714					tileWidth = 24;
5715					break;
5716				case 3:
5717					tileTop = -2;
5718					break;
5719				}
5720				break;
5721			case 275:
5722			case 276:
5723			case 277:
5724			case 278:
5725			case 279:
5726			case 280:
5727			case 281:
5728			case 296:
5729			case 297:
5730			case 309:
5731			case 358:
5732			case 359:
5733			case 413:
5734			case 414:
5735			case 542:
5736			case 550:
5737			case 551:
5738			case 553:
5739			case 554:
5740			case 558:
5741			case 559:
5742			case 599:
5743			case 600:
5744			case 601:
5745			case 602:
5746			case 603:
5747			case 604:
5748			case 605:
5749			case 606:
5750			case 607:
5751			case 608:
5752			case 609:
5753			case 610:
5754			case 611:
5755			case 612:
5756			case 632:
5757			case 640:
5758			case 643:
5759			case 644:
5760			case 645:
5761			case 710:
5762			{
5763				tileTop = 2;
5764				Main.critterCage = true;
5765				int bigAnimalCageFrame = GetBigAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5766				switch (typeCache)
5767				{
5768				case 275:
5769				case 359:
5770				case 599:
5771				case 600:
5772				case 601:
5773				case 602:
5774				case 603:
5775				case 604:
5776				case 605:
5777					addFrY = Main.bunnyCageFrame[bigAnimalCageFrame] * 54;
5778					break;
5779				case 550:
5780				case 551:
5781					addFrY = Main.turtleCageFrame[bigAnimalCageFrame] * 54;
5782					break;
5783				case 542:
5784					addFrY = Main.owlCageFrame[bigAnimalCageFrame] * 54;
5785					break;
5786				case 276:
5787				case 413:
5788				case 414:
5789				case 606:
5790				case 607:
5791				case 608:
5792				case 609:
5793				case 610:
5794				case 611:
5795				case 612:
5796					addFrY = Main.squirrelCageFrame[bigAnimalCageFrame] * 54;
5797					break;
5798				case 277:
5799					addFrY = Main.mallardCageFrame[bigAnimalCageFrame] * 54;
5800					break;
5801				case 278:
5802					addFrY = Main.duckCageFrame[bigAnimalCageFrame] * 54;
5803					break;
5804				case 553:
5805					addFrY = Main.grebeCageFrame[bigAnimalCageFrame] * 54;
5806					break;
5807				case 554:
5808					addFrY = Main.seagullCageFrame[bigAnimalCageFrame] * 54;
5809					break;
5810				case 279:
5811				case 358:
5812					addFrY = Main.birdCageFrame[bigAnimalCageFrame] * 54;
5813					break;
5814				case 280:
5815					addFrY = Main.blueBirdCageFrame[bigAnimalCageFrame] * 54;
5816					break;
5817				case 281:
5818					addFrY = Main.redBirdCageFrame[bigAnimalCageFrame] * 54;
5819					break;
5820				case 632:
5821				case 640:
5822				case 643:
5823				case 644:
5824				case 645:
5825					addFrY = Main.macawCageFrame[bigAnimalCageFrame] * 54;
5826					break;
5827				case 296:
5828				case 297:
5829					addFrY = Main.scorpionCageFrame[0, bigAnimalCageFrame] * 54;
5830					break;
5831				case 309:
5832					addFrY = Main.penguinCageFrame[bigAnimalCageFrame] * 54;
5833					break;
5834				case 558:
5835				case 559:
5836					addFrY = Main.seahorseCageFrame[bigAnimalCageFrame] * 54;
5837					break;
5838				case 710:
5839				{
5840					int num13 = Main.pufferfishCageFrame[bigAnimalCageFrame] / 33;
5841					addFrX = 108 * num13;
5842					addFrY = (Main.pufferfishCageFrame[bigAnimalCageFrame] - num13 * 33) * 54;
5843					break;
5844				}
5845				}
5846				break;
5847			}
5848			case 285:
5849			case 286:
5850			case 298:
5851			case 299:
5852			case 310:
5853			case 339:
5854			case 361:
5855			case 362:
5856			case 363:
5857			case 364:
5858			case 391:
5859			case 392:
5860			case 393:
5861			case 394:
5862			case 532:
5863			case 533:
5864			case 538:
5865			case 544:
5866			case 555:
5867			case 556:
5868			case 582:
5869			case 619:
5870			case 629:
5871			{
5872				tileTop = 2;
5873				Main.critterCage = true;
5874				int smallAnimalCageFrame2 = GetSmallAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5875				switch (typeCache)
5876				{
5877				case 285:
5878					addFrY = Main.snailCageFrame[smallAnimalCageFrame2] * 36;
5879					break;
5880				case 286:
5881				case 582:
5882					addFrY = Main.snail2CageFrame[smallAnimalCageFrame2] * 36;
5883					break;
5884				case 298:
5885				case 361:
5886					addFrY = Main.frogCageFrame[smallAnimalCageFrame2] * 36;
5887					break;
5888				case 339:
5889				case 362:

```


---

## 🤖 Assistant · 2026-08-11T15:58:16.041Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good, I have the bulk of GetTileDrawData. Let me check the tail end (5890-6000ish) to see if there are more cases after the small animal cages.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:16.309Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 120,
 "offset": 5889
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:16.317Z

**📎 ToolResult**

```
5889				case 362:
5890					addFrY = Main.grasshopperCageFrame[smallAnimalCageFrame2] * 36;
5891					break;
5892				case 299:
5893				case 363:
5894					addFrY = Main.mouseCageFrame[smallAnimalCageFrame2] * 36;
5895					break;
5896				case 310:
5897				case 364:
5898				case 391:
5899				case 619:
5900					addFrY = Main.wormCageFrame[smallAnimalCageFrame2] * 36;
5901					break;
5902				case 392:
5903				case 393:
5904				case 394:
5905					addFrY = Main.slugCageFrame[typeCache - 392, smallAnimalCageFrame2] * 36;
5906					break;
5907				case 532:
5908					addFrY = Main.maggotCageFrame[smallAnimalCageFrame2] * 36;
5909					break;
5910				case 533:
5911					addFrY = Main.ratCageFrame[smallAnimalCageFrame2] * 36;
5912					break;
5913				case 538:
5914				case 544:
5915				case 629:
5916					addFrY = Main.ladybugCageFrame[smallAnimalCageFrame2] * 36;
5917					break;
5918				case 555:
5919				case 556:
5920					addFrY = Main.waterStriderCageFrame[smallAnimalCageFrame2] * 36;
5921					break;
5922				}
5923				break;
5924			}
5925			case 282:
5926			case 505:
5927			case 543:
5928			{
5929				tileTop = 2;
5930				Main.critterCage = true;
5931				int waterAnimalCageFrame5 = GetWaterAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5932				addFrY = Main.fishBowlFrame[waterAnimalCageFrame5] * 36;
5933				break;
5934			}
5935			case 598:
5936			{
5937				tileTop = 2;
5938				Main.critterCage = true;
5939				int waterAnimalCageFrame4 = GetWaterAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5940				addFrY = Main.lavaFishBowlFrame[waterAnimalCageFrame4] * 36;
5941				break;
5942			}
5943			case 568:
5944			case 569:
5945			case 570:
5946			{
5947				tileTop = 2;
5948				Main.critterCage = true;
5949				int waterAnimalCageFrame3 = GetWaterAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5950				addFrY = Main.fairyJarFrame[waterAnimalCageFrame3] * 36;
5951				break;
5952			}
5953			case 288:
5954			case 289:
5955			case 290:
5956			case 291:
5957			case 292:
5958			case 293:
5959			case 294:
5960			case 295:
5961			case 360:
5962			case 580:
5963			case 620:
5964			{
5965				tileTop = 2;
5966				Main.critterCage = true;
5967				int waterAnimalCageFrame2 = GetWaterAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5968				int num12 = typeCache - 288;
5969				if (typeCache == 360 || typeCache == 580 || typeCache == 620)
5970				{
5971					num12 = 8;
5972				}
5973				addFrY = Main.butterflyCageFrame[num12, waterAnimalCageFrame2] * 36;
5974				break;
5975			}
5976			case 521:
5977			case 522:
5978			case 523:
5979			case 524:
5980			case 525:
5981			case 526:
5982			case 527:
5983			{
5984				tileTop = 2;
5985				Main.critterCage = true;
5986				int waterAnimalCageFrame = GetWaterAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5987				int num11 = typeCache - 521;
5988				addFrY = Main.dragonflyJarFrame[num11, waterAnimalCageFrame] * 36;
5989				break;
5990			}
5991			case 316:
5992			case 317:
5993			case 318:
5994			{
5995				tileTop = 2;
5996				Main.critterCage = true;
5997				int smallAnimalCageFrame = GetSmallAnimalCageFrame(x, y, tileFrameX, tileFrameY);
5998				int num10 = typeCache - 316;
5999				addFrY = Main.jellyfishCageFrame[num10, smallAnimalCageFrame] * 36;
6000				break;
6001			}
6002			case 207:
6003				tileTop = 2;
6004				if (tileFrameY >= 72)
6005				{
6006					addFrY = Main.tileFrame[typeCache];
6007					int num4 = x;
6008					if (tileFrameX % 36 != 0)

```


---

## 🤖 Assistant · 2026-08-11T15:58:16.635Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 180,
 "offset": 1010
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:16.654Z

**📎 ToolResult**

```
1010				{
1011					num4 = 1;
1012				}
1013				else if (tileDrawInfo.tileFrameY == 36)
1014				{
1015					num4 = 2;
1016				}
1017				Main.tileBatch.Draw(TextureAssets.ShroomCap.Value, new Vector2(tileX * 16 - (int)screenPosition.X - 22, tileY * 16 - (int)screenPosition.Y - 26) + screenOffset, new Rectangle(num4 * 62, 0, 60, 42), Lighting.GetColor(tileX, tileY), _zero, 1f, tileDrawInfo.tileSpriteEffect);
1018			}
1019			Rectangle rectangle = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight - tileDrawInfo.halfBrickHeight);
1020			float num5 = ((float)tileDrawInfo.tileWidth - 16f) / 2f;
1021			if (tileDrawInfo.typeCache >= 0 && TileID.Sets.DoNotAdjustDrawPositionBasedOnTileWidth[tileDrawInfo.typeCache])
1022			{
1023				num5 = 0f;
1024			}
1025			Vector2 vector = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - num5, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + tileDrawInfo.halfBrickHeight) + screenOffset;
1026			if (!flag)
1027			{
1028				return;
1029			}
1030			tileDrawInfo.colorTint = Color.White;
1031			tileDrawInfo.finalColor = GetFinalLight(tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileLight, tileDrawInfo.colorTint);
1032			switch (tileDrawInfo.typeCache)
1033			{
1034			case 751:
1035				if (tileDrawInfo.tileFrameX != 0 || tileDrawInfo.tileCache.frameY != 0)
1036				{
1037					return;
1038				}
1039				vector.X += 11f;
1040				vector.Y -= 8f;
1041				break;
1042			case 752:
1043				if (tileDrawInfo.tileFrameX != 0 || tileDrawInfo.tileFrameY != 0)
1044				{
1045					return;
1046				}
1047				vector.X += 8f;
1048				break;
1049			case 136:
1050				switch (tileDrawInfo.tileFrameX / 18)
1051				{
1052				case 1:
1053					vector.X += -2f;
1054					break;
1055				case 2:
1056					vector.X += 2f;
1057					break;
1058				}
1059				break;
1060			case 442:
1061			{
1062				int num7 = tileDrawInfo.tileFrameX / 22;
1063				if (num7 == 3)
1064				{
1065					vector.X += 2f;
1066				}
1067				break;
1068			}
1069			case 726:
1070				vector.X -= 2f;
1071				switch (tileDrawInfo.tileCache.blockType())
1072				{
1073				case 3:
1074					vector.X -= 6f;
1075					vector.Y += 2f;
1076					break;
1077				case 2:
1078					vector.X += 6f;
1079					vector.Y += 2f;
1080					break;
1081				case 5:
1082					vector.X -= 6f;
1083					break;
1084				case 4:
1085					vector.X += 6f;
1086					break;
1087				}
1088				break;
1089			case 51:
1090			case 697:
1091				tileDrawInfo.finalColor = tileDrawInfo.tileLight * 0.5f;
1092				break;
1093			case 160:
1094			case 692:
1095			{
1096				Color color = new Color(Main.DiscoR, Main.DiscoG, Main.DiscoB, 255);
1097				if (tileDrawInfo.tileCache.inActive())
1098				{
1099					color = tileDrawInfo.tileCache.actColor(color);
1100				}
1101				tileDrawInfo.finalColor = color;
1102				break;
1103			}
1104			case 129:
1105			{
1106				tileDrawInfo.finalColor = new Color(255, 255, 255, 100);
1107				int num6 = 2;
1108				if (tileDrawInfo.tileFrameX >= 324)
1109				{
1110					tileDrawInfo.finalColor = Color.Transparent;
1111				}
1112				if (tileDrawInfo.tileFrameY < 36)
1113				{
1114					vector.Y += num6 * (tileDrawInfo.tileFrameY == 0).ToDirectionInt();
1115				}
1116				else
1117				{
1118					vector.X += num6 * (tileDrawInfo.tileFrameY == 36).ToDirectionInt();
1119				}
1120				break;
1121			}
1122			case 723:
1123			case 724:
1124				switch (tileDrawInfo.tileFrameX / 18)
1125				{
1126				case 0:
1127					vector += new Vector2(0f, 2f);
1128					break;
1129				case 1:
1130					vector += new Vector2(0f, -2f);
1131					break;
1132				case 2:
1133					vector += new Vector2(-2f, 0f);
1134					break;
1135				case 3:
1136					vector += new Vector2(2f, 0f);
1137					break;
1138				}
1139				break;
1140			case 272:
1141			{
1142				int num8 = Main.tileFrame[tileDrawInfo.typeCache];
1143				num8 += tileX % 2;
1144				num8 += tileY % 2;
1145				num8 += tileX % 3;
1146				num8 += tileY % 3;
1147				num8 %= 2;
1148				num8 *= 90;
1149				tileDrawInfo.addFrY += num8;
1150				rectangle.Y += num8;
1151				break;
1152			}
1153			case 80:
1154			{
1155				WorldGen.GetCactusType(tileX, tileY, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, out var evil, out var good, out var crimson);
1156				if (evil)
1157				{
1158					rectangle.Y += 54;
1159				}
1160				if (good)
1161				{
1162					rectangle.Y += 108;
1163				}
1164				if (crimson)
1165				{
1166					rectangle.Y += 162;
1167				}
1168				break;
1169			}
1170			case 83:
1171				tileDrawInfo.drawTexture = GetTileDrawTexture(tileDrawInfo.tileCache, tileX, tileY);
1172				break;
1173			case 323:
1174				if (tileDrawInfo.tileCache.frameX <= 132 && tileDrawInfo.tileCache.frameX >= 88)
1175				{
1176					return;
1177				}
1178				vector.X += tileDrawInfo.tileCache.frameY;
1179				break;
1180			case 114:
1181				if (tileDrawInfo.tileFrameY > 0)
1182				{
1183					rectangle.Height += 2;
1184				}
1185				break;
1186			}
1187			if (tileDrawInfo.typeCache == 314)
1188			{
1189				DrawTile_MinecartTrack(screenPosition, screenOffset, tileX, tileY, tileDrawInfo);

```


---

## 🤖 Assistant · 2026-08-11T15:58:18.859Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the main DrawBasicTile section 1186-1700 which includes slope slicing, halfbrick clipping, and the 1609-1660 neighbor-halfbrick logic.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:19.055Z · glm-x-preview-260804

```
现在读取主绘制循环的剩余部分(半砖/坡面/邻居补条)。
```


---

## 🤖 Assistant · 2026-08-11T15:58:19.265Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 490,
 "offset": 1186
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:19.285Z

**📎 ToolResult**

```
1186			}
1187			if (tileDrawInfo.typeCache == 314)
1188			{
1189				DrawTile_MinecartTrack(screenPosition, screenOffset, tileX, tileY, tileDrawInfo);
1190			}
1191			else if (tileDrawInfo.typeCache == 171)
1192			{
1193				DrawXmasTree(screenPosition, screenOffset, tileX, tileY, tileDrawInfo);
1194			}
1195			else
1196			{
1197				DrawBasicTile(screenPosition, screenOffset, tileX, tileY, tileDrawInfo, rectangle, vector);
1198			}
1199			if (Main.tileGlowMask[tileDrawInfo.tileCache.type] != -1)
1200			{
1201				short num9 = Main.tileGlowMask[tileDrawInfo.tileCache.type];
1202				if (TextureAssets.GlowMask.IndexInRange(num9))
1203				{
1204					tileDrawInfo.drawTexture = TextureAssets.GlowMask[num9].Value;
1205				}
1206				double num10 = Main.timeForVisualEffects * 0.08;
1207				Color color2 = Color.White;
1208				bool flag3 = false;
1209				switch (tileDrawInfo.tileCache.type)
1210				{
1211				case 718:
1212					color2 = new Color(0, 0, 0, 0);
1213					break;
1214				case 717:
1215				{
1216					float num13 = LavaLightA(tileX, tileY);
1217					color2 = new Color(num13, num13, num13, num13 / 2f);
1218					break;
1219				}
1220				case 633:
1221					color2 = Color.Lerp(Color.White, tileDrawInfo.finalColor, 0.75f);
1222					break;
1223				case 659:
1224				case 667:
1225				case 708:
1226					color2 = LiquidRenderer.GetShimmerGlitterColor(top: true, tileX, tileY);
1227					break;
1228				case 350:
1229					color2 = new Color(new Vector4((float)((0.0 - Math.Cos(((int)(num10 / 6.283) % 3 == 1) ? num10 : 0.0)) * 0.2 + 0.2)));
1230					break;
1231				case 381:
1232				case 517:
1233				case 687:
1234					color2 = _lavaMossGlow;
1235					break;
1236				case 534:
1237				case 535:
1238				case 689:
1239					color2 = _kryptonMossGlow;
1240					break;
1241				case 536:
1242				case 537:
1243				case 690:
1244					color2 = _xenonMossGlow;
1245					break;
1246				case 539:
1247				case 540:
1248				case 688:
1249					color2 = _argonMossGlow;
1250					break;
1251				case 625:
1252				case 626:
1253				case 691:
1254					color2 = _violetMossGlow;
1255					break;
1256				case 627:
1257				case 628:
1258				case 692:
1259					color2 = new Color(Main.DiscoR, Main.DiscoG, Main.DiscoB);
1260					break;
1261				case 699:
1262					color2 = Color.White;
1263					break;
1264				case 370:
1265				case 390:
1266					color2 = _meteorGlow;
1267					break;
1268				case 391:
1269					color2 = new Color(250, 250, 250, 200);
1270					break;
1271				case 209:
1272					color2 = PortalHelper.GetPortalColor(Main.myPlayer, (tileDrawInfo.tileCache.frameX >= 288) ? 1 : 0);
1273					break;
1274				case 429:
1275				case 445:
1276					tileDrawInfo.drawTexture = GetTileDrawTexture(tileDrawInfo.tileCache, tileX, tileY);
1277					tileDrawInfo.addFrY = 18;
1278					break;
1279				case 129:
1280				{
1281					if (tileDrawInfo.tileFrameX < 324)
1282					{
1283						flag3 = true;
1284						break;
1285					}
1286					tileDrawInfo.drawTexture = GetTileDrawTexture(tileDrawInfo.tileCache, tileX, tileY);
1287					color2 = Main.hslToRgb(0.7f + (float)Math.Sin(MathF.PI * 2f * Main.GlobalTimeWrappedHourly * 0.16f + (float)tileX * 0.3f + (float)tileY * 0.7f) * 0.16f, 1f, 0.5f);
1288					color2.A /= 2;
1289					color2 *= 0.3f;
1290					int num11 = 72;
1291					for (float num12 = 0f; num12 < MathF.PI * 2f; num12 += MathF.PI / 2f)
1292					{
1293						Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector + num12.ToRotationVector2() * 2f, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY + num11, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight), color2, Vector2.Zero, 1f, SpriteEffects.None);
1294					}
1295					color2 = new Color(255, 255, 255, 100);
1296					break;
1297				}
1298				case 725:
1299				{
1300					float opacity = Filters.Scene["Noir"].Opacity;
1301					if (opacity > 0f && tileDrawInfo.tileFrameX % 36 == 0 && tileDrawInfo.tileFrameY == 54)
1302					{
1303						Vector2 position = vector + new Vector2(16f, 24f);
1304						SpriteEffects effects = ((tileDrawInfo.tileFrameX >= 36) ? SpriteEffects.FlipHorizontally : SpriteEffects.None);
1305						color2 = new Color(255, 255, 255, 100) * opacity;
1306						Main.tileBatch.Draw(tileDrawInfo.drawTexture, position, tileDrawInfo.drawTexture.Frame(), color2, tileDrawInfo.drawTexture.Frame().Center.ToVector2(), 1f, effects);
1307					}
1308					flag3 = true;
1309					break;
1310				}
1311				}
1312				if (!flag3)
1313				{
1314					if (tileDrawInfo.tileCache.slope() == 0 && !tileDrawInfo.tileCache.halfBrick())
1315					{
1316						Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight), color2, Vector2.Zero, 1f, SpriteEffects.None);
1317					}
1318					else if (tileDrawInfo.tileCache.halfBrick())
1319					{
1320						Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector, rectangle, color2, _zero, 1f, SpriteEffects.None);
1321					}
1322					else if (TileID.Sets.HasSlopeFrames[tileDrawInfo.tileCache.type])
1323					{
1324						Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector, new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, 16, 16), color2, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1325					}
1326					else
1327					{
1328						int num14 = tileDrawInfo.tileCache.slope();
1329						int num15 = 2;
1330						for (int i = 0; i < 8; i++)
1331						{
1332							int num16 = i * -2;
1333							int num17 = 16 - i * 2;
1334							int num18 = 16 - num17;
1335							int num19;
1336							switch (num14)
1337							{
1338							case 1:
1339								num16 = 0;
1340								num19 = i * 2;
1341								num17 = 14 - i * 2;
1342								num18 = 0;
1343								break;
1344							case 2:
1345								num16 = 0;
1346								num19 = 16 - i * 2 - 2;
1347								num17 = 14 - i * 2;
1348								num18 = 0;
1349								break;
1350							case 3:
1351								num19 = i * 2;
1352								break;
1353							default:
1354								num19 = 16 - i * 2 - 2;
1355								break;
1356							}
1357							Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector + new Vector2(num19, i * num15 + num16), new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX + num19, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY + num18, num15, num17), color2, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1358						}
1359						int num20 = ((num14 <= 2) ? 14 : 0);
1360						Main.tileBatch.Draw(tileDrawInfo.drawTexture, vector + new Vector2(0f, num20), new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY + num20, 16, 2), color2, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1361					}
1362				}
1363			}
1364			if (tileDrawInfo.glowTexture != null)
1365			{
1366				if (tileDrawInfo.typeCache == 412)
1367				{
1368					int num21 = Main.tileFrame[tileDrawInfo.typeCache] / 60;
1369					int num22 = (num21 + 1) % 4;
1370					float num23 = (float)(Main.tileFrame[tileDrawInfo.typeCache] % 60) / 60f;
1371					Rectangle glowSourceRect = tileDrawInfo.glowSourceRect;
1372					glowSourceRect.Y += num21 * 18 * 3;
1373					Rectangle glowSourceRect2 = tileDrawInfo.glowSourceRect;
1374					glowSourceRect2.Y += num22 * 18 * 3;
1375					Vector2 position2 = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop) + screenOffset;
1376					Main.tileBatch.Draw(tileDrawInfo.glowTexture, position2, glowSourceRect, tileDrawInfo.glowColor * (1f - num23), _zero, 1f, tileDrawInfo.tileSpriteEffect);
1377					Main.tileBatch.Draw(tileDrawInfo.glowTexture, position2, glowSourceRect2, tileDrawInfo.glowColor * num23, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1378				}
1379				else
1380				{
1381					Vector2 vector2 = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop) + screenOffset;
1382					if (TileID.Sets.Platforms[tileDrawInfo.typeCache])
1383					{
1384						vector2 = vector;
1385					}
1386					Main.tileBatch.SetLayer(Layer_Tiles, 1);
1387					Main.tileBatch.Draw(tileDrawInfo.glowTexture, vector2, tileDrawInfo.glowSourceRect, tileDrawInfo.glowColor, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1388					if (TileID.Sets.Platforms[tileDrawInfo.typeCache] && tileDrawInfo.tileCache.slope() != 0)
1389					{
1390						Tile tile = Main.tile[tileX, tileY + 1];
1391						Tile tile2 = Main.tile[tileX - 1, tileY + 1];
1392						Tile tile3 = Main.tile[tileX + 1, tileY + 1];
1393						bool shouldShowInvisibleBlocks = _shouldShowInvisibleBlocks;
1394						if (tileDrawInfo.tileCache.slope() == 1 && tile3.active() && (shouldShowInvisibleBlocks || !tile3.invisibleBlock()) && Main.tileSolid[tile3.type] && tile3.slope() != 2 && !tile3.halfBrick() && (!tile.active() || (!shouldShowInvisibleBlocks && tile.invisibleBlock()) || (tile.blockType() != 0 && tile.blockType() != 5) || !TileID.Sets.BlocksStairs[tile.type]))
1395						{
1396							Rectangle glowSourceRect3 = tileDrawInfo.glowSourceRect;
1397							if (TileID.Sets.Platforms[tile3.type] && tile3.slope() == 0)
1398							{
1399								glowSourceRect3.X = 324;
1400							}
1401							else
1402							{
1403								glowSourceRect3.X = 198;
1404							}
1405							Main.tileBatch.SetLayer(Layer_BehindTiles, 1);
1406							Main.tileBatch.Draw(tileDrawInfo.glowTexture, vector2 + new Vector2(0f, 16f), glowSourceRect3, tileDrawInfo.glowColor, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1407						}
1408						else if (tileDrawInfo.tileCache.slope() == 2 && tile2.active() && (shouldShowInvisibleBlocks || !tile2.invisibleBlock()) && Main.tileSolid[tile2.type] && tile2.slope() != 1 && !tile2.halfBrick() && (!tile.active() || (!shouldShowInvisibleBlocks && tile.invisibleBlock()) || (tile.blockType() != 0 && tile.blockType() != 4) || !TileID.Sets.BlocksStairs[tile.type]))
1409						{
1410							Rectangle glowSourceRect4 = tileDrawInfo.glowSourceRect;
1411							if (TileID.Sets.Platforms[tile2.type] && tile2.slope() == 0)
1412							{
1413								glowSourceRect4.X = 306;
1414							}
1415							else
1416							{
1417								glowSourceRect4.X = 162;
1418							}
1419							Main.tileBatch.SetLayer(Layer_BehindTiles, 1);
1420							Main.tileBatch.Draw(tileDrawInfo.glowTexture, vector2 + new Vector2(0f, 16f), glowSourceRect4, tileDrawInfo.glowColor, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1421						}
1422					}
1423				}
1424			}
1425			if (highlightTexture != null)
1426			{
1427				empty = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight);
1428				int num24 = 0;
1429				int num25 = 0;
1430				Main.tileBatch.Draw(highlightTexture, new Vector2((float)(tileX * 16 - (int)screenPosition.X) - ((float)tileDrawInfo.tileWidth - 16f) / 2f + (float)num24, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + num25) + screenOffset, empty, highlightColor, _zero, 1f, tileDrawInfo.tileSpriteEffect);
1431			}
1432		}
1433	
1434		private bool IsVisible(Tile tile)
1435		{
1436			bool flag = tile.invisibleBlock();
1437			switch (tile.type)
1438			{
1439			case 19:
1440				if (tile.frameY / 18 == 48)
1441				{
1442					flag = true;
1443				}
1444				break;
1445			case 541:
1446			case 631:
1447				flag = true;
1448				break;
1449			}
1450			if (flag)
1451			{
1452				return _shouldShowInvisibleBlocks;
1453			}
1454			return true;
1455		}
1456	
1457		public Texture2D GetTileDrawTexture(Tile tile, int tileX, int tileY)
1458		{
1459			TilePaintSystemV2.TileVariationkey key = new TilePaintSystemV2.TileVariationkey
1460			{
1461				TileType = tile.type,
1462				TileStyle = 0,
1463				PaintColor = tile.color()
1464			};
1465			switch (tile.type)
1466			{
1467			case 5:
1468				key.TileStyle = GetTreeBiome(tileX, tileY, tile.frameX, tile.frameY);
1469				break;
1470			case 323:
1471				key.TileStyle = GetPalmTreeBiome(tileX, tileY);
1472				break;
1473			case 83:
1474				if (WorldGen.IsAlchemyPlantHarvestable(tile.frameX / 18, tileY))
1475				{
1476					key.TileType = 84;
1477				}
1478				break;
1479			}
1480			return GetTileDrawTexture(key);
1481		}
1482	
1483		public Texture2D GetTileDrawTexture(int tileType, int paintColor)
1484		{
1485			return GetTileDrawTexture(new TilePaintSystemV2.TileVariationkey
1486			{
1487				TileType = tileType,
1488				PaintColor = paintColor
1489			});
1490		}
1491	
1492		public Texture2D GetTileDrawTexture(TilePaintSystemV2.TileVariationkey key)
1493		{
1494			if (_lastPaintLookupKey == key)
1495			{
1496				return _lastPaintLookupTexture;
1497			}
1498			_lastPaintLookupKey = key;
1499			_lastPaintLookupTexture = LookupTileDrawTexture(key);
1500			return _lastPaintLookupTexture;
1501		}
1502	
1503		private Texture2D LookupTileDrawTexture(TilePaintSystemV2.TileVariationkey key)
1504		{
1505			Main.instance.LoadTiles(key.TileType);
1506			if (key.PaintColor != 0 || key.TileStyle != 0)
1507			{
1508				Texture2D texture2D = _paintSystem.TryGetTileAndRequestIfNotReady(key.TileType, key.TileStyle, key.PaintColor);
1509				if (texture2D != null)
1510				{
1511					return texture2D;
1512				}
1513			}
1514			return TextureAssets.Tile[key.TileType].Value;
1515		}
1516	
1517		private Texture2D LookupCageTopDrawTexture(TilePaintSystemV2.CageTopVariationkey key)
1518		{
1519			if (key.PaintColor != 0)
1520			{
1521				Texture2D texture2D = _paintSystem.TryGetCageTopAndRequestIfNotReady(key.CageStyle, key.PaintColor);
1522				if (texture2D != null)
1523				{
1524					return texture2D;
1525				}
1526			}
1527			return TextureAssets.CageTop[key.CageStyle].Value;
1528		}
1529	
1530		private void DrawBasicTile(Vector2 screenPosition, Vector2 screenOffset, int tileX, int tileY, TileDrawInfo drawData, Rectangle normalTileRect, Vector2 normalTilePosition)
1531		{
1532			bool flag = !TileID.Sets.DontDrawTileSliced[drawData.tileCache.type];
1533			bool flag2 = !TileID.Sets.DontDrawTileSlopes[drawData.tileCache.type];
1534			if (drawData.typeCache == 380 || TileID.Sets.Platforms[drawData.typeCache])
1535			{
1536				DrawTile_BackRope(screenPosition, screenOffset, tileX, tileY, drawData);
1537			}
1538			if (flag2 && drawData.tileCache.slope() > 0)
1539			{
1540				if (TileID.Sets.Platforms[drawData.tileCache.type])
1541				{
1542					Tile tile = Main.tile[tileX, tileY + 1];
1543					Tile tile2 = Main.tile[tileX - 1, tileY + 1];
1544					Tile tile3 = Main.tile[tileX + 1, tileY + 1];
1545					bool shouldShowInvisibleBlocks = _shouldShowInvisibleBlocks;
1546					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, normalTileRect, drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1547					if (drawData.tileCache.slope() == 1 && tile3.active() && (shouldShowInvisibleBlocks || !tile3.invisibleBlock()) && Main.tileSolid[tile3.type] && tile3.slope() != 2 && !tile3.halfBrick() && (!tile.active() || (!shouldShowInvisibleBlocks && tile.invisibleBlock()) || (tile.blockType() != 0 && tile.blockType() != 5) || !TileID.Sets.BlocksStairs[tile.type]))
1548					{
1549						Main.tileBatch.SetLayer(Layer_BehindTiles, 0);
1550						Rectangle value = new Rectangle(198, drawData.tileFrameY, 16, 16);
1551						if (TileID.Sets.Platforms[tile3.type] && tile3.slope() == 0)
1552						{
1553							value.X = 324;
1554						}
1555						Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 16f), value, drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1556					}
1557					else if (drawData.tileCache.slope() == 2 && tile2.active() && (shouldShowInvisibleBlocks || !tile2.invisibleBlock()) && Main.tileSolid[tile2.type] && tile2.slope() != 1 && !tile2.halfBrick() && (!tile.active() || (!shouldShowInvisibleBlocks && tile.invisibleBlock()) || (tile.blockType() != 0 && tile.blockType() != 4) || !TileID.Sets.BlocksStairs[tile.type]))
1558					{
1559						Main.tileBatch.SetLayer(Layer_BehindTiles, 0);
1560						Rectangle value2 = new Rectangle(162, drawData.tileFrameY, 16, 16);
1561						if (TileID.Sets.Platforms[tile2.type] && tile2.slope() == 0)
1562						{
1563							value2.X = 306;
1564						}
1565						Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 16f), value2, drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1566					}
1567					return;
1568				}
1569				if (TileID.Sets.HasSlopeFrames[drawData.tileCache.type])
1570				{
1571					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY, 16, 16), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1572					return;
1573				}
1574				int num = drawData.tileCache.slope();
1575				int num2 = 2;
1576				for (int i = 0; i < 8; i++)
1577				{
1578					int num3 = i * -2;
1579					int num4 = 16 - i * 2;
1580					int num5 = 16 - num4;
1581					int num6;
1582					switch (num)
1583					{
1584					case 1:
1585						num3 = 0;
1586						num6 = i * 2;
1587						num4 = 14 - i * 2;
1588						num5 = 0;
1589						break;
1590					case 2:
1591						num3 = 0;
1592						num6 = 16 - i * 2 - 2;
1593						num4 = 14 - i * 2;
1594						num5 = 0;
1595						break;
1596					case 3:
1597						num6 = i * 2;
1598						break;
1599					default:
1600						num6 = 16 - i * 2 - 2;
1601						break;
1602					}
1603					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(num6, i * num2 + num3), new Rectangle(drawData.tileFrameX + drawData.addFrX + num6, drawData.tileFrameY + drawData.addFrY + num5, num2, num4), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1604				}
1605				int num7 = ((num <= 2) ? 14 : 0);
1606				Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, num7), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.tileFrameY + drawData.addFrY + num7, 16, 2), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1607				return;
1608			}
1609			if (flag2 && !TileID.Sets.Platforms[drawData.typeCache] && !TileID.Sets.IgnoresNearbyHalfbricksWhenDrawn[drawData.typeCache] && _tileSolid[drawData.typeCache] && !TileID.Sets.NotReallySolid[drawData.typeCache] && !drawData.tileCache.halfBrick() && (Main.tile[tileX - 1, tileY].halfBrick() || Main.tile[tileX + 1, tileY].halfBrick()))
1610			{
1611				if (Main.tile[tileX - 1, tileY].halfBrick() && Main.tile[tileX + 1, tileY].halfBrick())
1612				{
1613					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 8f), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY + 8, drawData.tileWidth, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1614					Rectangle value3 = new Rectangle(126 + drawData.addFrX, drawData.addFrY, 16, 8);
1615					if (Main.tile[tileX, tileY - 1].active() && !Main.tile[tileX, tileY - 1].bottomSlope() && Main.tile[tileX, tileY - 1].type == drawData.typeCache)
1616					{
1617						value3 = new Rectangle(90 + drawData.addFrX, drawData.addFrY, 16, 8);
1618					}
1619					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, value3, drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1620				}
1621				else if (Main.tile[tileX - 1, tileY].halfBrick())
1622				{
1623					int num8 = 4;
1624					if (TileID.Sets.AllBlocksWithSmoothBordersToResolveHalfBlockIssue[drawData.typeCache])
1625					{
1626						num8 = 2;
1627					}
1628					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 8f), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY + 8, drawData.tileWidth, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1629					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(num8, 0f), new Rectangle(drawData.tileFrameX + num8 + drawData.addFrX, drawData.addFrY + drawData.tileFrameY, drawData.tileWidth - num8, drawData.tileHeight), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1630					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, new Rectangle(144 + drawData.addFrX, drawData.addFrY, num8, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1631					if (num8 == 2)
1632					{
1633						Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, new Rectangle(148 + drawData.addFrX, drawData.addFrY, 2, 2), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1634					}
1635				}
1636				else if (Main.tile[tileX + 1, tileY].halfBrick())
1637				{
1638					int num9 = 4;
1639					if (TileID.Sets.AllBlocksWithSmoothBordersToResolveHalfBlockIssue[drawData.typeCache])
1640					{
1641						num9 = 2;
1642					}
1643					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 8f), new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY + 8, drawData.tileWidth, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1644					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, new Rectangle(drawData.tileFrameX + drawData.addFrX, drawData.addFrY + drawData.tileFrameY, drawData.tileWidth - num9, drawData.tileHeight), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1645					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(16 - num9, 0f), new Rectangle(144 + (16 - num9), 0, num9, 8), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1646					if (num9 == 2)
1647					{
1648						Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(14f, 0f), new Rectangle(156, 0, 2, 2), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1649					}
1650				}
1651				return;
1652			}
1653			if (flag && Lighting.NotRetro && _tileSolid[drawData.typeCache] && !drawData.tileCache.halfBrick())
1654			{
1655				DrawSingleTile_SlicedBlock(normalTilePosition, tileX, tileY, drawData);
1656				return;
1657			}
1658			if (drawData.halfBrickHeight == 8 && (!Main.tile[tileX, tileY + 1].active() || !_tileSolid[Main.tile[tileX, tileY + 1].type] || Main.tile[tileX, tileY + 1].halfBrick()))
1659			{
1660				if (TileID.Sets.Platforms[drawData.typeCache])
1661				{
1662					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, normalTileRect, drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1663				}
1664				else
1665				{
1666					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition, normalTileRect.Modified(0, 0, 0, -4), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1667					Main.tileBatch.Draw(drawData.drawTexture, normalTilePosition + new Vector2(0f, 4f), new Rectangle(144 + drawData.addFrX, 66 + drawData.addFrY, drawData.tileWidth, 4), drawData.finalColor, _zero, 1f, drawData.tileSpriteEffect);
1668				}
1669			}
1670			else if (TileID.Sets.CritterCageLidStyle[drawData.typeCache] >= 0)
1671			{
1672				int num10 = TileID.Sets.CritterCageLidStyle[drawData.typeCache];
1673				if ((num10 < 3 && normalTileRect.Y % 54 == 0) || (num10 >= 3 && normalTileRect.Y % 36 == 0))
1674				{
1675					Vector2 position = normalTilePosition;

```


---

## 🤖 Assistant · 2026-08-11T15:58:21.715Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the halfbrick handling earlier - the tileTop/halfBrickHeight logic at lines ~880-1010, which includes halfbrick height computation and the lighting-based approach. Let me read 880-1010.

Also need:
- TileID.Sets: IgnoresNearbyHalfbricksWhenDrawn, AllBlocksWithSmoothBordersToResolveHalfBlockIssue, DoNotAdjustDrawPositionBasedOnTileWidth, HasSlopeFrames, NotReallySolid, DontDrawTileSliced, DontDrawTileSlopes, BlocksStairs
- DrawSingleTile_SlicedBlock
- VanillaTiler.ts full read
- ChunkCache.ts
- SpriteAtlas.ts relevant parts

Let me do these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:21.965Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 160,
 "offset": 880
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:21.971Z

**📎 ToolResult**

```
880			if (tileDrawInfo.tileCache.liquid > 0 && tileDrawInfo.tileCache.type == 518)
881			{
882				return;
883			}
884			GetTileDrawData(tileX, tileY, tileDrawInfo.tileCache, tileDrawInfo.typeCache, ref tileDrawInfo.tileFrameX, ref tileDrawInfo.tileFrameY, out tileDrawInfo.tileWidth, out tileDrawInfo.tileHeight, out tileDrawInfo.tileTop, out tileDrawInfo.halfBrickHeight, out tileDrawInfo.addFrX, out tileDrawInfo.addFrY, out tileDrawInfo.tileSpriteEffect, out tileDrawInfo.glowTexture, out tileDrawInfo.glowSourceRect, out tileDrawInfo.glowColor);
885			if (tileDrawInfo.tileTop < 0)
886			{
887				Main.tileBatch.SetLayer(Layer_OverTiles, 0);
888			}
889			else if (tileDrawInfo.tileTop + tileDrawInfo.tileHeight <= 16)
890			{
891				Main.tileBatch.SetLayer(Layer_Tiles, 0);
892			}
893			else
894			{
895				Main.tileBatch.SetLayer(Layer_BehindTiles, 0);
896			}
897			tileDrawInfo.drawTexture = GetTileDrawTexture(tileDrawInfo.tileCache, tileX, tileY);
898			Texture2D highlightTexture = null;
899			Rectangle empty = Rectangle.Empty;
900			Color highlightColor = Color.Transparent;
901			if (TileID.Sets.HasOutlines[tileDrawInfo.typeCache])
902			{
903				GetTileOutlineInfo(tileX, tileY, tileDrawInfo.typeCache, ref tileDrawInfo.tileLight, ref highlightTexture, ref highlightColor);
904			}
905			if (_perspectivePlayer.dangerSense && IsTileDangerous(_perspectivePlayer, tileDrawInfo.tileCache, tileDrawInfo.typeCache))
906			{
907				if (tileDrawInfo.tileLight.R < byte.MaxValue)
908				{
909					tileDrawInfo.tileLight.R = byte.MaxValue;
910				}
911				if (tileDrawInfo.tileLight.G < 50)
912				{
913					tileDrawInfo.tileLight.G = 50;
914				}
915				if (tileDrawInfo.tileLight.B < 50)
916				{
917					tileDrawInfo.tileLight.B = 50;
918				}
919				if (_isActiveAndNotPaused && _rand.Next(30) == 0)
920				{
921					int num = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 60, 0f, 0f, 100, default(Color), 0.3f);
922					_dust[num].fadeIn = 1f;
923					_dust[num].velocity *= 0.1f;
924					_dust[num].noLight = true;
925					_dust[num].noGravity = true;
926				}
927			}
928			if (_perspectivePlayer.findTreasure && Main.IsTileSpelunkable(tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY))
929			{
930				if (tileDrawInfo.tileLight.R < 200)
931				{
932					tileDrawInfo.tileLight.R = 200;
933				}
934				if (tileDrawInfo.tileLight.G < 170)
935				{
936					tileDrawInfo.tileLight.G = 170;
937				}
938				if (_isActiveAndNotPaused && _rand.Next(60) == 0)
939				{
940					int num2 = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 204, 0f, 0f, 150, default(Color), 0.3f);
941					_dust[num2].fadeIn = 1f;
942					_dust[num2].velocity *= 0.1f;
943					_dust[num2].noLight = true;
944				}
945			}
946			if (_perspectivePlayer.biomeSight)
947			{
948				Color sightColor = Color.White;
949				if (Main.IsTileBiomeSightable(tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, ref sightColor))
950				{
951					if (tileDrawInfo.tileLight.R < sightColor.R)
952					{
953						tileDrawInfo.tileLight.R = sightColor.R;
954					}
955					if (tileDrawInfo.tileLight.G < sightColor.G)
956					{
957						tileDrawInfo.tileLight.G = sightColor.G;
958					}
959					if (tileDrawInfo.tileLight.B < sightColor.B)
960					{
961						tileDrawInfo.tileLight.B = sightColor.B;
962					}
963					if (_isActiveAndNotPaused && _rand.Next(480) == 0)
964					{
965						Color newColor = sightColor;
966						int num3 = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
967						_dust[num3].noGravity = true;
968						_dust[num3].fadeIn = 1f;
969						_dust[num3].velocity *= 0.1f;
970						_dust[num3].noLightEmittance = true;
971					}
972				}
973			}
974			if (_isActiveAndNotPaused)
975			{
976				if (!Lighting.UpdateEveryFrame || new FastRandom(Main.TileFrameSeed).WithModifier(tileX, tileY).Next(4) == 0)
977				{
978					DrawTiles_EmitParticles(tileY, tileX, tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, tileDrawInfo.tileLight);
979				}
980				tileDrawInfo.tileLight = DrawTiles_GetLightOverride(tileY, tileX, tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, tileDrawInfo.tileLight);
981			}
982			bool flag = false;
983			if (tileDrawInfo.glowTexture != null || Main.tileGlowMask[tileDrawInfo.typeCache] != -1 || Main.tileFlame[tileDrawInfo.typeCache])
984			{
985				flag = true;
986			}
987			if (tileDrawInfo.tileLight.R >= 1 || tileDrawInfo.tileLight.G >= 1 || tileDrawInfo.tileLight.B >= 1 || TileID.Sets.IgnoreDrawLightConditions[tileDrawInfo.typeCache])
988			{
989				flag = true;
990			}
991			if (tileDrawInfo.tileCache.wall > 0 && (tileDrawInfo.tileCache.wall == 318 || tileDrawInfo.tileCache.fullbrightWall()))
992			{
993				flag = true;
994			}
995			bool flag2 = IsVisible(tileDrawInfo.tileCache);
996			if (!flag2)
997			{
998				flag = false;
999			}
1000			if (!flag && flag2 && TileDrawingBase.DrawOwnBlacks)
1001			{
1002				drawBlackHelper.DrawBlack(tileX, tileY);
1003			}
1004			CacheSpecialDraws_Part1(tileX, tileY, tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, !flag);
1005			CacheSpecialDraws_Part2(tileX, tileY, tileDrawInfo);
1006			if (tileDrawInfo.typeCache == 72 && tileDrawInfo.tileFrameX >= 36)
1007			{
1008				int num4 = 0;
1009				if (tileDrawInfo.tileFrameY == 18)
1010				{
1011					num4 = 1;
1012				}
1013				else if (tileDrawInfo.tileFrameY == 36)
1014				{
1015					num4 = 2;
1016				}
1017				Main.tileBatch.Draw(TextureAssets.ShroomCap.Value, new Vector2(tileX * 16 - (int)screenPosition.X - 22, tileY * 16 - (int)screenPosition.Y - 26) + screenOffset, new Rectangle(num4 * 62, 0, 60, 42), Lighting.GetColor(tileX, tileY), _zero, 1f, tileDrawInfo.tileSpriteEffect);
1018			}
1019			Rectangle rectangle = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight - tileDrawInfo.halfBrickHeight);
1020			float num5 = ((float)tileDrawInfo.tileWidth - 16f) / 2f;
1021			if (tileDrawInfo.typeCache >= 0 && TileID.Sets.DoNotAdjustDrawPositionBasedOnTileWidth[tileDrawInfo.typeCache])
1022			{
1023				num5 = 0f;
1024			}
1025			Vector2 vector = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - num5, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + tileDrawInfo.halfBrickHeight) + screenOffset;
1026			if (!flag)
1027			{
1028				return;
1029			}
1030			tileDrawInfo.colorTint = Color.White;
1031			tileDrawInfo.finalColor = GetFinalLight(tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileLight, tileDrawInfo.colorTint);
1032			switch (tileDrawInfo.typeCache)
1033			{
1034			case 751:
1035				if (tileDrawInfo.tileFrameX != 0 || tileDrawInfo.tileCache.frameY != 0)
1036				{
1037					return;
1038				}
1039				vector.X += 11f;

```


---

## 🤖 Assistant · 2026-08-11T15:58:22.700Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"IgnoresNearbyHalfbricksWhenDrawn\\|AllBlocksWithSmoothBordersToResolveHalfBlockIssue\\|DoNotAdjustDrawPositionBasedOnTileWidth\\|HasSlopeFrames\\|NotReallySolid\\|DontDrawTileSliced\\|DontDrawTileSlopes\\|BlocksStairs\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Locate seam-related Sets declarations in TileID.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:22.734Z

**📎 ToolResult**

```
151:		public static bool[] DontDrawTileSliced = Factory.CreateBoolSet(false, 137, 235, 388, 476, 160, 138, 664, 665, 630, 631, 711, 712, 713, 714, 715, 716, 723, 726);
153:		public static bool[] DontDrawTileSlopes = Factory.CreateBoolSet(false, 137, 235, 388, 476, 138, 664, 665, 630, 631, 711, 712, 713, 714, 715, 716, 723, 726);
175:		public static bool[] AllBlocksWithSmoothBordersToResolveHalfBlockIssue = Factory.CreateBoolSet(false, 321, 157, 208, 159, 190, 80, 251, 202, 229, 56, 38, 39, 152, 118, 151, 148, 206, 119, 175, 46, 176, 45, 140, 347, 370, 121, 122, 680, 681, 682, 685, 686, 346, 687, 688, 689, 690, 691, 692, 160, 226, 54, 156, 155, 153, 154, 150, 250, 198, 273, 274, 325, 284, 348, 385, 327, 326, 345, 328, 329, 357, 369, 268, 261, 262, 255, 267, 260, 265, 258, 266, 259, 264, 257, 263, 256, 311, 426, 430, 431, 432, 433, 434, 727, 728, 729, 730, 731, 732, 272, 145, 146, 350, 127, 472, 473, 477, 478, 479, 492, 496, 507, 508, 563, 618, 708, 722, 735, 748);
253:		public static bool[] DoNotAdjustDrawPositionBasedOnTileWidth = Factory.CreateBoolSet(711);
267:		public static bool[] HasSlopeFrames = Factory.CreateBoolSet(421, 422);
271:		public static bool[] IgnoresNearbyHalfbricksWhenDrawn = Factory.CreateBoolSet(380, 476, 235, 138, 664, 137, 484, 421, 422, 711, 712, 713, 714, 715, 716);
353:		public static bool[] BlocksStairs = Factory.CreateBoolSet(386, 387, 54, 328, 459, 541);
355:		public static bool[] NotReallySolid = Factory.CreateBoolSet(387, 388, 10);

```


---

## 🤖 Assistant · 2026-08-11T15:58:23.875Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the TS files: VanillaTiler.ts (715 lines), ChunkCache.ts (372), SpriteAtlas.ts relevant parts.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:23.994Z · glm-x-preview-260804

```
现在读取我们的 TS 实现进行对照。
```


---

## 🤖 Assistant · 2026-08-11T15:58:24.144Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts"
}
```


---

## 🤖 Assistant · 2026-08-11T15:58:24.297Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:24.305Z

**📎 ToolResult**

```
1	// chunk 静态缓存：每 chunk 16×16 tile 预渲染到离屏 canvas（墙层+tile 层）
2	import { CHUNK, TILE } from '../core/constants';
3	import { T, TILE_DEFS, WALL_DEFS, TILE_BY_KEY } from '../data/tiles';
4	import { hash2 } from '../core/rng';
5	import { drawVanillaCell, drawTreeCell } from './VanillaTiler';
6	import { TILE_ANIM_RATE, tileAnim, animYOffset, campfireYOffset } from './TileAnim';
7	import { VanillaWallTiler } from './VanillaWallTiler';
8	import { shade } from '../assets/Palette';
9	import type { TileSheetEntry } from '../assets/TileSheetGen';
10	import type { AutoTiler } from './AutoTiler';
11	import type { World } from '../world/World';
12	
13	// 我们的 tile → Maples RuleTile 规则名（有规则的走素材自动贴合，无规则回退程序化）
14	// Grass 走人工标注（'@grass'）：Tiles_2.png 是多 tile 混排图集，自动分类不可靠；
15	// 用 public/annotator.html 标注后写入 sprites/annotations.json。无标注时回退程序化。
16	const TILE_RULES: Record<number, string> = {
17	  // 泥土/石/草走原版 BlendRules；铁矿走原版表——均不再用 Maples 规则
18	  13: '工作台', 14: '熔炉', 15: '铁砧',
19	};
20	
21	export interface ChunkPair {
22	  wall: HTMLCanvasElement;   // 背景墙层（水画在它之上）
23	  tile: HTMLCanvasElement;   // 前景 tile/物体层（画在水之上）
24	}
25	
26	export class ChunkCache {
27	  chunks = new Map<number, ChunkPair>();
28	  dirtyQueue: number[] = [];
29	  sheets: Map<number, TileSheetEntry>;
30	  world: World;
31	  autotiler: AutoTiler | null;
32	  wallTiler: VanillaWallTiler | null;
33	  truncatesWalls: number[] = [];
34	  /** 含动画 tile 的 chunk，按 sheet 分组（换帧时只重建对应 chunk，避免全量重烘焙） */
35	  private animChunksBySheet = new Map<number, Set<number>>();
36	  /** LRU 上限:每 chunk 2×256² canvas = 512KB;384 chunk ≈ 196MB(缩放 0.5 时
37	   *  可视 ~100 chunk 仍绰绰有余)。此前 Map 只增不减——跑图积累无界(内存泄漏 #1) */
38	  static readonly MAX_CHUNKS = 384;
39	
40	  /** 释放全部 chunk 画布 GPU 背板并清表(退出世界必须调用)。
41	   *  detached canvas 的回收依赖 GC 且明显滞后——连续多次读档累积数百 MB
42	   *  显存,最终 contextlost/contextrestored 风暴卡死(2026-08-10 trace 实证) */
43	  dispose(): void {
44	    for (const pair of this.chunks.values()) {
45	      pair.wall.width = 0; pair.wall.height = 0;
46	      pair.tile.width = 0; pair.tile.height = 0;
47	    }
48	    this.chunks.clear();
49	    this.dirtyQueue.length = 0;
50	    this.animChunksBySheet.clear();
51	  }
52	
53	  constructor(world: World, sheets: Map<number, TileSheetEntry>, autotiler: AutoTiler | null = null, wallTiler: VanillaWallTiler | null = null) {
54	    this.world = world;
55	    this.sheets = sheets;
56	    this.autotiler = autotiler;
57	    this.wallTiler = wallTiler;
58	    // 原版 TileID.Sets.TruncatesWalls（54 玻璃 / 328 暗影宝箱 / 459 / 748）→ 内部 tile id
59	    this.truncatesWalls = ['glass', 'v_328_shadow_chest', 'v_459_', 'v_748_']
60	      .map((k) => TILE_BY_KEY[k] ?? -1)
61	      .filter((id) => id >= 0);
62	    world.store.onTileChanged((x, y) => this.markDirtyAround(x, y));
63	  }
64	
65	  static key(cx: number, cy: number): number {
66	    return (cx & 0xffff) | ((cy & 0xffff) << 16);
67	  }
68	
69	  markDirty(cx: number, cy: number) {
70	    const k = ChunkCache.key(cx, cy);
71	    if (!this.chunks.has(k)) return; // 未生成的 chunk 惰性创建
72	    this.chunks.set(k, undefined as unknown as ChunkPair); // 标记删除，重绘时重建
73	    if (!this.dirtyQueue.includes(k)) this.dirtyQueue.push(k);
74	  }
75	
76	  /** 区域标脏（tile 范围）：供树冠等大范围精灵清理使用 */
77	  markDirtyArea(x0: number, y0: number, x1: number, y1: number) {
78	    for (let cy = Math.floor(y0 / CHUNK); cy <= Math.floor(y1 / CHUNK); cy++) {
79	      for (let cx = Math.floor(x0 / CHUNK); cx <= Math.floor(x1 / CHUNK); cx++) {
80	        if (cx < 0 || cy < 0) continue;
81	        this.markDirty(cx, cy);
82	      }
83	    }
84	  }
85	
86	  markDirtyAround(x: number, y: number) {
87	    const cx = Math.floor(x / CHUNK), cy = Math.floor(y / CHUNK);
88	    this.markDirty(cx, cy);
89	    // 边缘融合：邻接 chunk 也要标脏
90	    if (x % CHUNK === 0) this.markDirty(cx - 1, cy);
91	    if (x % CHUNK === CHUNK - 1) this.markDirty(cx + 1, cy);
92	    if (y % CHUNK === 0) this.markDirty(cx, cy - 1);
93	    if (y % CHUNK === CHUNK - 1) this.markDirty(cx, cy + 1);
94	  }
95	
96	  /** 全量标脏(atlas 懒加载晚到的新表 → 已烘焙的 chunk 里可能烤了 fallback)。
97	   *  4/帧 的 flushDirty 会逐步重烘焙,dirtyQueue.includes 去重防重复入队 */
98	  invalidateAll(): void {
99	    for (const k of this.chunks.keys()) {
100	      if (this.chunks.get(k) === undefined) continue; // 已是待重建哨兵
101	      this.chunks.set(k, undefined as unknown as ChunkPair);
102	      if (!this.dirtyQueue.includes(k)) this.dirtyQueue.push(k);
103	    }
104	  }
105	
106	  /** 每帧重绘脏 chunk:数量上限 maxN 之外再加时间预算 budgetMs——
107	   *  跑图/全量标脏时烘焙突发不再挤占帧预算(实测 87ms 尖峰来源) */
108	  flushDirty(maxN = 4, budgetMs = 6) {
109	    let n = 0;
110	    const t0 = performance.now();
111	    while (this.dirtyQueue.length && n < maxN) {
112	      const k = this.dirtyQueue.shift()!;
113	      const cx = k & 0xffff, cy = (k >> 16) & 0xffff;
114	      if (this.chunks.get(k) !== undefined) continue; // 已重建
115	      this.get(cx, cy);
116	      n++;
117	      if (performance.now() - t0 > budgetMs) break; // 单 chunk 烘焙超预算也至少完成 1 个
118	    }
119	  }
120	
121	  /** 动画时钟推进（Game 每帧调用）：sheet 到达换帧 tick → 只重建含该 sheet 的 chunk。
122	   *  原版语义 = AnimateTiles 每 rate tick 推进 tileFrame；帧内 chunk 复用零开销 */
123	  advanceAnim(): void {
124	    tileAnim.tick++;
125	    if (!this.animChunksBySheet.size) return;
126	    for (const [sheet, set] of this.animChunksBySheet) {
127	      const rate = TILE_ANIM_RATE[sheet];
128	      if (!rate || tileAnim.tick % rate !== 0) continue;
129	      for (const k of set) this.markDirty(k & 0xffff, (k >> 16) & 0xffff);
130	    }
131	  }
132	
133	  /** 取 chunk 双层画布（惰性生成，LRU 淘汰最久未用） */
134	  get(cx: number, cy: number): ChunkPair {
135	    const k = ChunkCache.key(cx, cy);
136	    let c = this.chunks.get(k);
137	    if (c) {
138	      // LRU:命中即刷新 recency(delete+set 移到 Map 尾部)。渲染循环每帧都 get
139	      // 可视 chunk,故屏上 chunk 永远最新、不会被误淘汰
140	      this.chunks.delete(k);
141	      this.chunks.set(k, c);
142	      return c;
143	    }
144	    c = this.renderChunk(cx, cy);
145	    this.chunks.set(k, c);
146	    while (this.chunks.size > ChunkCache.MAX_CHUNKS) {
147	      const oldest = this.chunks.keys().next().value as number | undefined;
148	      if (oldest === undefined) break;
149	      this.chunks.delete(oldest);
150	    }
151	    return c;
152	  }
153	
154	  /** 树枝判定：TREE 且上下皆非 TREE、恰好一侧为 TREE（横向独连树干）。
155	   *  下方是实心地面的属于树根底座 —— 走规则表渲染底座贴图，不算枝干 */
156	
157	  private neighborMask(x: number, y: number, type: number): number {
158	    const st = this.world.store;
159	    let mask = 0;
160	    const same = (nx: number, ny: number) => st.inBounds(nx, ny) && st.flags[st.idx(nx, ny)] && st.type[st.idx(nx, ny)] === type ? 1 : 0;
161	    mask |= same(x, y - 1);        // N
162	    mask |= same(x + 1, y) << 1;   // E
163	    mask |= same(x, y + 1) << 2;   // S
164	    mask |= same(x - 1, y) << 3;   // W
165	    mask |= same(x + 1, y - 1) << 4; // NE
166	    mask |= same(x + 1, y + 1) << 5; // SE
167	    mask |= same(x - 1, y + 1) << 6; // SW
168	    mask |= same(x - 1, y - 1) << 7; // NW
169	    return mask;
170	  }
171	
172	  private renderChunk(cx: number, cy: number): ChunkPair {
173	    // 双层画布：墙层 / tile 层分离 —— 水渲染在两层之间（墙之上、图块之下）
174	    const wall = document.createElement('canvas');
175	    wall.width = CHUNK * TILE; wall.height = CHUNK * TILE;
176	    const tile = document.createElement('canvas');
177	    tile.width = CHUNK * TILE; tile.height = CHUNK * TILE;
178	    let ctx = wall.getContext('2d')!;
179	    ctx.imageSmoothingEnabled = false;
180	    const st = this.world.store;
181	    const x0 = cx * CHUNK, y0 = cy * CHUNK;
182	
183	    // ---- 第一遍：背景墙全部先画（避免后格的墙盖住跨格物体如宝箱/树冠）----
184	    // 原版墙 framing（VanillaWallTiler）：32×32 帧以格为中心外溢 8px →
185	    // 扫描范围外扩 1 格，跨 chunk 边界的帧由相邻 chunk 补齐（像素一致无副作用）
186	    if (this.wallTiler) {
187	      const EXT = 1;
188	      for (let ly = -EXT; ly < CHUNK + EXT; ly++) {
189	        for (let lx = -EXT; lx < CHUNK + EXT; lx++) {
190	          const x = x0 + lx, y = y0 + ly;
191	          if (!st.inBounds(x, y)) continue;
192	          const i = st.idx(x, y);
193	          const wallId = st.wall[i];
194	          if (wallId === 0) continue;
195	          const px = lx * TILE, py = ly * TILE;
196	          if (this.wallTiler.hasTexture(wallId)) {
197	            this.wallTiler.draw(ctx, st, x, y, wallId, this.truncatesWalls, px, py);
198	          } else {
199	            const wd = WALL_DEFS[wallId];
200	            if (wd) {
201	              ctx.fillStyle = wd.mapColor;
202	              ctx.fillRect(px, py, TILE, TILE);
203	              ctx.fillStyle = shade(wd.mapColor, 0.8);
204	              ctx.fillRect(px, py + TILE - 1, TILE, 1);
205	              ctx.fillRect(px + TILE - 1, py, 1, TILE);
206	            }
207	          }
208	        }
209	      }
210	    }
211	
212	    // ---- 第二遍：前景 tile / 物体（绘制到 tile 层画布；水渲染在墙层与 tile 层之间）----
213	    ctx = tile.getContext('2d')!;
214	    ctx.imageSmoothingEnabled = false;
215	    for (let ly = 0; ly < CHUNK; ly++) {
216	      for (let lx = 0; lx < CHUNK; lx++) {
217	        const x = x0 + lx, y = y0 + ly;
218	        if (!st.inBounds(x, y)) continue;
219	        const i = st.idx(x, y);
220	        const px = lx * TILE, py = ly * TILE;
221	        const type = st.type[i];
222	        // 原版语义:非活性格不渲染(TileRunner 会给空气格写幽灵 type)
223	        if (type === 0 || !st.flags[i]) continue;
224	        // 已致动(inActive):幽灵态淡显(原版 DrawInactiveSorter,Main.cs:2828 附近)
225	        // 每格开头统一设定 alpha(各 continue 路径无需逐个恢复,下一格自愈)
226	        const actuated = (st.wire[i] & 32) !== 0;
227	        ctx.globalAlpha = actuated ? 0.3 : 1;
228	        const def = TILE_DEFS[type];
229	        if (!def) { ctx.fillStyle = '#808080'; ctx.fillRect(px, py, TILE, TILE); continue; }
230	        // 原版素材图块（TileDef.vanilla）：TEdit framing 查找表（auto）或显式 18px 帧（style）
231	        if (def.vanilla && this.autotiler) {
232	          // 动画陈设（原版 AnimateTiles/GetTileDrawData addFrY）：frameY += 帧索引*pitch
233	          // （pitch 默认 38，3 格高特例组 54，篝火族特例 36+熄灭行静止——见 TileAnim）
234	          let fy = st.frameY[i];
235	          if (def.vanilla.sheet === 215) {
236	            fy += campfireYOffset(st.frameY[i]);
237	            let set215 = this.animChunksBySheet.get(215);
238	            if (!set215) { set215 = new Set(); this.animChunksBySheet.set(215, set215); }
239	            set215.add(ChunkCache.key(cx, cy));
240	          } else if (TILE_ANIM_RATE[def.vanilla.sheet]) {
241	            const rows = this.autotiler.atlas.vmeta(def.vanilla.sheet)?.rows ?? 0;
242	            fy += animYOffset(def.vanilla.sheet, rows * 18);
243	            let set = this.animChunksBySheet.get(def.vanilla.sheet);
244	            if (!set) { set = new Set(); this.animChunksBySheet.set(def.vanilla.sheet, set); }
245	            set.add(ChunkCache.key(cx, cy));
246	          }
247	          drawVanillaCell(
248	            ctx, this.autotiler.atlas, def.vanilla.sheet, def.vanilla.frame,
249	            def.vanilla.fw ?? 1, def.vanilla.fh ?? 1,
250	            st, x, y, type,
251	            (t) => t === type, // 同 id 融合判定（后续可扩 mergeWith）
252	            px, py, st.frameX[i], fy,
253	            { treeX: this.world.treeX, treeStyle: this.world.treeStyle, treeTops: this.world.treeTops,
254	              worldSurface: this.world.groundLevel, worldW: this.world.w },
255	          );
256	          continue;
257	        }
258	        // 树苗：Tree_Bodys 树干段作小苗（底部对齐）
259	        if (type === T.SAPLING && this.autotiler) {
260	          const r = this.autotiler.saplingSprite(x, y);
261	          if (r) {
262	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px + (TILE - r.sw) / 2, py + TILE - r.sh, r.sw, r.sh);
263	            continue;
264	          }
265	        }
266	        // 杂草：Maples Tiles_3 杂草贴图（16×20，底部对齐，hash 选变体）
267	        if (type === T.TALLGRASS && this.autotiler) {
268	          const r = this.autotiler.weedSprite(x, y);
269	          if (r) {
270	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px - (r.sw - TILE) / 2, py + TILE - r.sh, r.sw, r.sh);
271	            continue;
272	          }
273	        }
274	        // 有 RuleTile 规则的 tile 用 Maples 素材自动贴合
275	        const ruleName = this.autotiler ? TILE_RULES[type] : undefined;
276	        if (ruleName && this.autotiler) {
277	          // 草皮覆盖件：保持原生透明（缺口露出背后的墙/天空），不做任何垫底/填充
278	          if (ruleName === '@grass') {
279	            const r = this.autotiler.tile(ruleName, st, x, y, type);
280	            if (r) ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px, py, TILE, TILE);
281	            continue;
282	          }
283	          const r = this.autotiler.tile(ruleName, st, x, y, type);
284	          if (r) {
285	            // 大图（树冠 80×80，宽>2格）跳过 —— 第三遍统一绘制（跨 chunk 补全 + 树叶盖树干）
286	            if (r.sw > TILE * 2) continue;
287	            // 按精灵原始尺寸绘制。树干等"宽≤2格、高>1格"的竖向件顶部对齐：
288	            // 溢出向下伸，由更下方的格（后画）覆盖 —— 下层不压上层。
289	            let dy = py + (TILE - r.sh) / 2;
290	            if (r.sh > TILE && r.sw <= TILE * 2) dy = py;
291	            const dx = px + (TILE - r.sw) / 2;
292	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, dx, dy, r.sw, r.sh);
293	            continue;
294	          }
295	        }
296	        const entry = this.sheets.get(type);
297	        if (!entry) {
298	          ctx.fillStyle = '#FF00FF';
299	          ctx.fillRect(px, py, TILE, TILE);
300	          continue;
301	        }
302	        if (entry.kind === 'blend') {
303	          const mask = this.neighborMask(x, y, type);
304	          const col = mask & 15, row = mask >> 4;
305	          ctx.drawImage(entry.canvas, col * TILE, row * TILE, TILE, TILE, px, py, TILE, TILE);
306	        } else if (entry.kind === 'object') {
307	          // 仅锚点绘制整体
308	          if (st.frameX[i] === 0 && st.frameY[i] === 0) {
309	            const w = (entry.w ?? 1) * TILE, h = (entry.h ?? 1) * TILE;
310	            ctx.drawImage(entry.canvas, px, py, w, h);
311	          }
312	        } else {
313	          // single：帧偏移直接取
314	          ctx.drawImage(entry.canvas, st.frameX[i], st.frameY[i], TILE, TILE, px, py, TILE, TILE);
315	        }
316	      }
317	    }
318	    ctx.globalAlpha = 1; // 致动幽灵 alpha 复位(防影响后续 pass)
319	
320	    // ---- 第三遍：半砖（halfBrick）——主绘制后清掉上半 8px ----
321	    // VanillaTiler blend/auto/style 三路径已按原版源矩形裁剪（源 y+8 高-8）；
322	    // 此处 clearRect 仅作兜底（uv 查找失败走 vframe(1,1) 全帧回退等路径仍画满 16×16）
323	    for (let ly = 0; ly < CHUNK; ly++) {
324	      for (let lx = 0; lx < CHUNK; lx++) {
325	        const i = st.idx(x0 + lx, y0 + ly);
326	        if (st.half[i]) ctx.clearRect(lx * TILE, ly * TILE, TILE, 8);
327	      }
328	    }
329	
330	    // ---- 第四遍：原版树冠/树枝（tile 5 标记帧，跨 chunk 外扩绘制） ----
331	    // 树冠 80×80 / 树枝 40×40 跨多格，主遍跳过这些标记帧，由此外扩遍统一绘制防裁剪。
332	    // 棕榈（323）整棵都在此绘制：干身 frameY 是倾斜偏移（最大 ±12px 跨列），
333	    // 主遍画会在 chunk 边缘列被裁剪 → 干+冠全部走外扩遍
334	    if (this.autotiler) {
335	      const treeIds = ['tree', 'v_72_mushroom_tree', 'v_323_palm_trees', 'v_5_trees',
336	        'v_583_topaz_tree', 'v_584_amethyst_tree', 'v_585_sapphire_tree', 'v_586_emerald_tree',
337	        'v_587_ruby_tree', 'v_588_diamond_tree', 'v_589_amber_tree',
338	        'v_596_vanity_tree_sakura', 'v_616_vanity_tree_yellow_willow', 'v_634_ash_tree']
339	        .map((k) => TILE_BY_KEY[k]).filter((id) => id !== undefined);
340	      for (const v5 of treeIds) {
341	        const EXT = 6;
342	        for (let ty = y0 - EXT; ty < y0 + CHUNK + EXT; ty++) {
343	          for (let tx = x0 - EXT; tx < x0 + CHUNK + EXT; tx++) {
344	            if (!st.inBounds(tx, ty)) continue;
345	            const i = st.idx(tx, ty);
346	            if (st.type[i] !== v5) continue;
347	            const fx = st.frameX[i], fy = st.frameY[i];
348	            const def = TILE_DEFS[st.type[i]];
349	            const sheet = def?.vanilla?.sheet ?? 5;
350	            const isPalm = sheet === 323;
351	            const isCrown = isPalm ? (fx >= 88 && fx <= 132) : (fy >= 198); // 原版只看 frameY
352	            if (isPalm) {
353	              // 棕榈：干+冠都画（干身倾斜跨列，必须外扩遍）
354	              drawTreeCell(ctx, this.autotiler.atlas, st, tx, ty, fx, fy,
355	                tx * TILE - x0 * TILE, ty * TILE - y0 * TILE, sheet, isCrown,
356	                { treeX: this.world.treeX, treeStyle: this.world.treeStyle, treeTops: this.world.treeTops,
357	                worldSurface: this.world.groundLevel, worldW: this.world.w });
358	            } else if (isCrown) {
359	              // 其他树：仅标记帧（干身由主遍绘制）
360	              drawTreeCell(ctx, this.autotiler.atlas, st, tx, ty, fx, fy,
361	                tx * TILE - x0 * TILE, ty * TILE - y0 * TILE, sheet, true,
362	                { treeX: this.world.treeX, treeStyle: this.world.treeStyle, treeTops: this.world.treeTops,
363	                worldSurface: this.world.groundLevel, worldW: this.world.w });
364	            }
365	          }
366	        }
367	      }
368	    }
369	
370	    return { wall, tile };
371	  }
372	}
373	

```


---

## 👤 User(sidechain) · 2026-08-11T15:58:24.392Z

**📎 ToolResult**

```
1	// 原版图块通用渲染器：TEdit TileFraming.SelfFrame8Way 移植（8 向 47 项查找表）
2	// 用于 TileDef.vanilla.frame === 'auto' 的 1x1 实心块（泥土/矿石/冰雪等同表系）。
3	// 位序（与游戏 neighborMask 不同！）：U=1 L=2 R=4 D=8 UL=16 UR=32 DL=64 DR=128
4	// 变体选择 (x*7 + y*11) % 3；无条目/越界回退默认帧 (1,1)
5	import type { SpriteAtlas, DrawRect } from '../assets/SpriteAtlas';
6	import type { TileStore } from '../world/TileStore';
7	import { TILE } from '../core/constants';
8	import { TILE_BY_KEY, TILE_DEFS } from '../data/tiles';
9	import { getUVForMasks } from './BlendFraming';
10	
11	type Frame = [number, number];
12	
13	// 47 项查找表（源：TEdit Render/TileFraming.cs BuildSelfFrame8WayLookup）
14	const LOOKUP: Record<number, Frame[]> = {
15	  0: [[9, 3], [10, 3], [11, 3]],
16	  1: [[6, 3], [7, 3], [8, 3]],
17	  2: [[12, 0], [12, 1], [12, 2]],
18	  3: [[15, 2]],
19	  4: [[9, 0], [9, 1], [9, 2]],
20	  5: [[13, 2]],
21	  6: [[6, 4], [7, 4], [8, 4]],
22	  7: [[14, 2]],
23	  8: [[6, 0], [7, 0], [8, 0]],
24	  9: [[5, 0], [5, 1], [5, 2]],
25	  10: [[15, 0]],
26	  11: [[15, 1]],
27	  12: [[13, 0]],
28	  13: [[13, 1]],
29	  14: [[14, 0]],
30	  15: [[14, 1]],
31	  19: [[1, 4], [3, 4], [5, 4]],
32	  23: [[16, 3]],
33	  27: [[17, 0]],
34	  31: [[13, 4]],
35	  37: [[0, 4], [2, 4], [4, 4]],
36	  39: [[17, 3]],
37	  45: [[16, 0]],
38	  47: [[12, 4]],
39	  55: [[1, 2], [2, 2], [3, 2]],
40	  63: [[6, 2], [7, 2], [8, 2]],
41	  74: [[1, 3], [3, 3], [5, 3]],
42	  75: [[17, 1]],
43	  78: [[16, 2]],
44	  79: [[13, 3]],
45	  91: [[4, 0], [4, 1], [4, 2]],
46	  95: [[11, 0], [11, 1], [11, 2]],
47	  111: [[17, 4]],
48	  127: [[14, 3]],
49	  140: [[0, 3], [2, 3], [4, 3]],
50	  141: [[16, 1]],
51	  142: [[17, 2]],
52	  143: [[12, 3]],
53	  159: [[16, 4]],
54	  173: [[0, 0], [0, 1], [0, 2]],
55	  175: [[10, 0], [10, 1], [10, 2]],
56	  191: [[15, 3]],
57	  206: [[1, 0], [2, 0], [3, 0]],
58	  207: [[6, 1], [7, 1], [8, 1]],
59	  223: [[14, 4]],
60	  239: [[15, 4]],
61	  255: [[1, 1], [2, 1], [3, 1]],
62	};
63	
64	const DEFAULT_FRAME: Frame = [1, 1];
65	
66	/** 8 向邻居掩码（vanilla 位序：U=1 L=2 R=4 D=8 UL=16 UR=32 DL=64 DR=128）。
67	 *  含 BlockStyle 双向门控（与 blend 路径同款,Framing.cs:92-98/199-316）:
68	 *  half 断上;slope1 断上/右;2 断上/左;3 断下/右;4 断下/左;角落需对角反向两向放行 */
69	export function mask8(st: TileStore, x: number, y: number, type: number, same: (t: number) => boolean): number {
70	  const BS = [0b1111, 0b1110, 0b0110, 0b1010, 0b0101, 0b1001]; // bit0=up 1=down 2=left 3=right
71	  const edges = (ii: number) => {
72	    const b = st.half[ii] ? 1 : (st.slope[ii] >= 1 && st.slope[ii] <= 4 ? st.slope[ii] + 1 : 0);
73	    return BS[b];
74	  };
75	  const cE = edges(st.idx(x, y));
76	  // 各方向所需(中心 edge, 对面格 edge);角方向额外查对角格反向两向
77	  const NEED: Array<[number, number]> = [
78	    [0b0001, 0b0010], // U: 中心 up / 上邻 down
79	    [0b0100, 0b1000], // L: 中心 left / 左邻 right
80	    [0b1000, 0b0100], // R: 中心 right / 右邻 left
81	    [0b0010, 0b0001], // D: 中心 down / 下邻 up
82	  ];
83	  const diagNeed = (dx: number, dy: number): number => {
84	    // 对角格需放行朝向中心的两个反向边
85	    let need = 0;
86	    if (dy < 0) need |= 0b0010; else if (dy > 0) need |= 0b0001; // 对角在下→up / 在上→down
87	    if (dx < 0) need |= 0b1000; else if (dx > 0) need |= 0b0100; // 对角在右→left / 在左→right
88	    return need;
89	  };
90	  const at = (ax: number, ay: number) => st.inBounds(ax, ay) && same(st.type[st.idx(ax, ay)]);
91	  let m = 0;
92	  // 四正交（:70-73）：类型同 + BlockStyle 双向放行
93	  const sides: Array<[number, number, number]> = [[0, -1, 0], [-1, 0, 1], [1, 0, 2], [0, 1, 3]];
94	  for (const [dx, dy, di] of sides) {
95	    const [cNeed, nNeed] = NEED[di];
96	    if ((cE & cNeed) !== cNeed) continue;
97	    const oi = st.idx(x + dx, y + dy);
98	    if ((edges(oi) & nNeed) !== nNeed) continue;
99	    if (!at(x + dx, y + dy)) continue;
100	    m |= 1 << di;
101	  }
102	  // 角（:75-78）：两正交均在 + 对角格反向两向放行 + 类型同
103	  const corners: Array<[number, number, number, number]> = [
104	    [-1, -1, 3, 16], [1, -1, 5, 32], [-1, 1, 10, 64], [1, 1, 12, 128], // dx,dy,正交位组合(U|L 等),角位
105	  ];
106	  for (const [dx, dy, combo, bit] of corners) {
107	    if ((m & combo) !== combo) continue;
108	    if (!at(x + dx, y + dy)) continue;
109	    const oi = st.idx(x + dx, y + dy);
110	    if ((edges(oi) & diagNeed(dx, dy)) !== diagNeed(dx, dy)) continue;
111	    m |= bit;
112	  }
113	  return m;
114	}
115	
116	/** auto 帧格的实际渲染帧（col,row）——与渲染端同一查找表，供纠错面板定位 */
117	export function autoFrameAt(st: TileStore, x: number, y: number, type: number): { col: number; row: number } {
118	  const entry = LOOKUP[mask8(st, x, y, type, (t) => t === type)];
119	  if (!entry) return { col: DEFAULT_FRAME[0], row: DEFAULT_FRAME[1] };
120	  const v = ((x * 7) + (y * 11)) % 3 % entry.length;
121	  return { col: entry[v][0], row: entry[v][1] };
122	}
123	
124	/** 'auto' 帧：查表 + 变体。返回 (col,row) 或 null（回退默认帧由调用方处理） */
125	export function frameFor(atlas: SpriteAtlas, sheet: number, st: TileStore, x: number, y: number, type: number, same: (t: number) => boolean): DrawRect | null {
126	  const entry = LOOKUP[mask8(st, x, y, type, same)];
127	  let r: DrawRect | null = null;
128	  if (entry) {
129	    const v = entry[((x * 7) + (y * 11)) % 3 % entry.length];
130	    r = atlas.vframe(sheet, v[0], v[1]);
131	    if (r && !frameHasContent(r)) r = null; // 空帧（如草皮表缺 13-17 列的边缘帧）→ 回退
132	  }
133	  if (!r) r = atlas.vframe(sheet, DEFAULT_FRAME[0], DEFAULT_FRAME[1]);
134	  return r;
135	}
136	
137	/** auto 帧内容检测缓存：key = 图像:像素偏移。查找表引用的帧在部分表（草皮族等
138	 *  窄表）上是空像素，直画会整格空白 → 检出后回退默认帧 */
139	const frameContentCache = new Map<string, boolean>();
140	function frameHasContent(r: DrawRect): boolean {
141	  const key = `${(r.img as HTMLImageElement).naturalWidth || r.img.width}x${r.img.height}:${r.sx},${r.sy}`;
142	  const hit = frameContentCache.get(key);
143	  if (hit !== undefined) return hit;
144	  let ok = false;
145	  try {
146	    const c = document.createElement('canvas');
147	    c.width = r.sw; c.height = r.sh;
148	    const cx = c.getContext('2d', { willReadFrequently: true })!;
149	    cx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, 0, 0, r.sw, r.sh);
150	    const d = cx.getImageData(0, 0, r.sw, r.sh).data;
151	    let n = 0;
152	    for (let i = 3; i < d.length; i += 16) { if (d[i] > 40 && ++n >= 4) { ok = true; break; } }
153	  } catch { ok = true; /* 采样失败按有内容处理 */ }
154	  frameContentCache.set(key, ok);
155	  return ok;
156	}
157	
158	/** 树木专用渲染（tile 5，移植 TEdit WorldRenderXna 树逻辑）：
159	 *  - 树干帧（frameY < 198）：按树下草地生物群系选 Tiles_5_0..6 变体，取 (U,V,20,20) 压入 16px 格
160	 *  - 标记帧（frameX >= 22 且 frameY >= 198）：不采样 Tiles_5——
161	 *    U=22 树顶（Tree_Tops_style 80×80 底部锚定）、U=44 左枝（Tree_Branches 40×40 右锚定）、
162	 *    U=66 右枝（左锚定）；变体 x%3
163	 *  treeStyle 固定 0（wld 树样式段未解析，默认森林） */
164	// 树类 tile → Tree_Tops/Branches 样式（TEdit：5 森林 0 / 宝石树 583-589 → 22-28 /
165	// 装饰树 596 樱花→29、616 柳→30 / 灰烬树 634 → 31）
166	const TREE_SHEET_STYLES: Record<number, number> = { 5: 0, 596: 29, 616: 30, 634: 31 };
167	for (let i = 583; i <= 589; i++) TREE_SHEET_STYLES[i] = 22 + (i - 583);
168	/** 树冠帧尺寸按 PNG 实际宽度推导（3 变体等分 + 2px 间隔；高度 -2）：
169	 *  自动覆盖全部样式（森林 80×80 / 丛林·宝石 114-116×96 / 装饰 118×96 / 神圣 80-114×140） */
170	function treeTopSize(img: HTMLImageElement): [number, number] {
171	  return [Math.floor(img.width / 3) - 2, img.height - 2];
172	}
173	// 树下草地 → 生物群系树干变体（TEdit treeType；-1 = 基础 Tiles_5）
174	const TREE_GROUND: Array<[string, number]> = [
175	  ['v_23_corrupt_grass_block', 0],
176	  ['v_60_jungle_grass_block', 1],
177	  ['v_109_hallowed_grass_block', 2],
178	  ['snow', 3],
179	  ['v_199_crimson_grass_block', 4],
180	  ['v_70_mushroom_grass_block', 6],
181	];
182	/** 原版 WorldGen.GetCommonTreeFoliageData 样式选择移植（WorldGen.cs:37381-37496）。
183	 *  trees = { treeX, treeStyle(header), treeTops(v≥211 权威 13 变体), worldSurface, worldW }
184	 *  变体来源优先 treeTops（GetTreeStyle(areaId)），空表回退 header treeStyle[0..3] */
185	function areaStyle(trees: TreeStyleData, areaId: number): number {
186	  if (trees.treeTops?.length) return trees.treeTops[areaId] ?? 0;
187	  return trees.treeStyle?.[areaId] ?? 0;
188	}
189	
190	export function crownStyleFor(x: number, treeType: number, floorY: number, trees: TreeStyleData): number {
191	  const gs = (id: number) => areaStyle(trees, id);
192	  switch (treeType) {
193	    case 0: return 1;   // 23 腐化草
194	    case 1: {           // 60 丛林草：v[5]==1 → 11；深处 → 13（覆盖）；否则 2
195	      let st = gs(5) === 1 ? 11 : 2;
196	      if (floorY > (trees.worldSurface ?? 0)) st = 13;
197	      return st;
198	    }
199	    case 2: {           // 109/492 神圣草：hallowBG 未解析 → 固定 3
200	      return 3;
201	    }
202	    case 3: {           // 147 雪原：完整 case-147 逻辑
203	      let st = 4;
204	      const v6 = gs(6);
205	      if (v6 === 0) { st = 12; if (x % 10 === 0) st = 18; }
206	      if (v6 === 2 || v6 === 3 || v6 === 32 || v6 === 4 || v6 === 42 || v6 === 5 || v6 === 7) {
207	        st = v6 % 2 !== 0
208	          ? (x <= (trees.worldW ?? 0) / 2 ? 17 : 16)
209	          : (x >= (trees.worldW ?? 0) / 2 ? 17 : 16);
210	      }
211	      return st;
212	    }
213	    case 4: return 5;   // 199 猩红草
214	    case 6: return 14;  // 70 蘑菇草
215	    default: {          // 2/477 普通草：四区 + 0→0/5→10/其余 5+s
216	      const num = x > (trees.treeX?.[0] ?? 0) ? (x > (trees.treeX?.[1] ?? 0) ? (x > (trees.treeX?.[2] ?? 0) ? gs(3) : gs(2)) : gs(1)) : gs(0);
217	      if (num === 0) return 0;
218	      return num === 5 ? 10 : 5 + num;
219	    }
220	  }
221	}
222	
223	/** 向下扫描树下的草地定生物群系树型（原版 GetCommonTreeFoliageData 扫描）。
224	 *  返回 treeType（-1 普通草/森林）与发现草地的深度 floorY（丛林深处判定用） */
225	export function scanTreeType(st: TileStore, x: number, y: number): { type: number; floorY: number } {
226	  let type = -1;
227	  let floorY = y;
228	  for (let i = 0; i < 100; i++) {
229	    const ty = y + i;
230	    if (ty >= st.h) break;
231	    floorY = ty;
232	    const t = st.type[st.idx(x, ty)];
233	    if (t === 0) continue;
234	    if (t === TILE_BY_KEY['grass']) { type = -1; break; }
235	    const hit = TREE_GROUND.find(([k]) => TILE_BY_KEY[k] === t);
236	    if (hit) { type = hit[1]; break; }
237	  }
238	  return { type, floorY };
239	}
240	
241	export interface TreeStyleData {
242	  treeX: number[];
243	  treeStyle: number[];
244	  treeTops?: number[];
245	  worldSurface?: number;
246	  worldW?: number;
247	}
248	
249	export function drawTreeCell(
250	  ctx: CanvasRenderingContext2D, atlas: SpriteAtlas,
251	  st: TileStore, x: number, y: number, fx: number, fy: number, px: number, py: number,
252	  sheet = 5,
253	  foliageOnly = false,
254	  trees?: TreeStyleData,
255	): void {
256	  const style = TREE_SHEET_STYLES[sheet] ?? 0;
257	  // 棕榈树（tile 323）：树冠帧藏在树干列内（frameX 88-132，无独立标记格）。
258	  //  TEdit：Tree_Tops_15（80×80、82px 步长），srcX = 变体×82、srcY = 沙型×82，
259	  //  底部锚定 + X 偏移 frameY/16 格；沙型 = 下方沙块种类（普通0/猩红1/珍珠2/腐化3）
260	  if (sheet === 323) {
261	    if (fx >= 88 && fx <= 132) {
262	      if (!foliageOnly) return; // 树冠/干身全部由外扩遍绘制（倾斜跨列/跨 chunk 防裁剪）
263	      const img15 = atlas.ensureVImage('vanilla/Tree_Tops_15.png');
264	      if (!img15) return;
265	      // 沙型：向下扫沙块
266	      let palmType = 0;
267	      for (let i = 0; i < 100; i++) {
268	        const ty = y + i;
269	        if (ty >= st.h) break;
270	        const t = st.type[st.idx(x, ty)];
271	        if (t === 0) continue;
272	        const tk = TILE_DEFS[t]?.key;
273	        palmType = tk === 'v_234_crimsand_block' ? 1 : tk === 'v_116_pearlsand_block' ? 2
274	          : tk === 'v_112_ebonsand_block' ? 3 : 0;
275	        break;
276	      }
277	      const v323 = Math.floor((fx - 88) / 22); // 0/1/2 变体
278	      const sx15 = v323 * 82, sy15 = palmType * 82;
279	      if (sx15 + 80 > img15.width || sy15 + 80 > img15.height) return;
280	      // 底部锚定居中 + X 偏移 = frameY【像素·有符号】（原版 dest.X += V*zoom/16，
281	      // zoom=16 即 V 像素；65534 = -2 的 u16 回绕）
282	      const leanCrown = fy >= 32768 ? fy - 65536 : fy;
283	      ctx.drawImage(img15, sx15, sy15, 80, 80,
284	        px + (TILE - 80) / 2 + leanCrown, py + TILE - 80, 80, 80);
285	      return;
286	    }
287	    // 干身（原版 GetTileDrawData case 323：20×20 顶锚定、X 居中 -2——向下溢出
288	    // 4px 盖住下方格顶,干底接缝由下溢覆盖;frameY 是**有符号像素偏移**——
289	    // 棕榈树干随高度倾斜，65534 = -2 的 u16 回绕）
290	    const img323 = atlas.ensureVImage('vanilla/Tiles_323.png');
291	    if (!img323 || fx + 20 > img323.width) return;
292	    const lean = fy >= 32768 ? fy - 65536 : fy; // 原版 vector2.X += frameY
293	    ctx.drawImage(img323, fx, 0, 20, 20, px - 2 + lean, py, 20, 20);
294	    return;
295	  }
296	  // 蘑菇树（tile 72）：独立渲染路径——U≥36 标记帧 = 巨蘑菇顶（Shroom_Tops，60×42、62px 步长、底部锚定）
297	  if (sheet === 72) {
298	    if (foliageOnly === false && fx >= 36) return; // 顶格由外扩遍画
299	    if (fx >= 36) {
300	      const img72 = atlas.ensureVImage('vanilla/Shroom_Tops.png');
301	      if (img72 && fx + 60 <= img72.width && fy + 42 <= img72.height) {
302	        // TEdit：source.X = (V/18)*62；60×42 底部锚定居中
303	        const sx72 = Math.floor(fy / 18) * 62;
304	        if (sx72 + 60 <= img72.width) {
305	          ctx.drawImage(img72, sx72, 0, 60, 42, px + (TILE - 60) / 2, py + TILE - 42, 60, 42);
306	        }
307	      }
308	      return;
309	    }
310	    // 干身：Tiles_72 直取（54×54 表，2×2 帧 18px 网格）
311	    const img72 = atlas.ensureVImage('vanilla/Tiles_72.png');
312	    if (img72 && fx + 16 <= img72.width && fy + 16 <= img72.height) {
313	      ctx.drawImage(img72, fx, fy, 16, 16, px, py, TILE, TILE);
314	    }
315	    return;
316	  }
317	  if (fy >= 198) {   // 冠/枝标记帧（原版只看 frameY；fx 0/22=顶 44/66=枝）
318	    // 树冠/树枝标记帧（仅由 ChunkCache 的外扩遍绘制，防跨 chunk 裁剪）
319	    if (foliageOnly === false) return;
320	    // 变体来源 = 标记帧自身 frameY（原版 WorldGen.GetTreeFrame：198→0/220→1/242→2）
321	    const frame = fy >= 242 ? 2 : fy >= 220 ? 1 : 0;
322	    // 样式选择（原版 GetCommonTreeFoliageData；树族 tile 用固定样式映射）
323	    // 树型扫描列：左枝在右侧树干列找地 / 右枝在左侧（原版 xoffset）
324	    const scanX = x + (fx === 44 ? 1 : fx === 66 ? -1 : 0);
325	    const scan = scanTreeType(st, scanX, y);
326	    const crown = sheet === 5 && trees
327	      ? crownStyleFor(scanX, scan.type, scan.floorY, trees)
328	      : style;
329	    let img: HTMLImageElement | null;
330	    let sx = 0, sy = 0, sw = 0, sh = 0, anchor = 0; // 0=底中(顶) 1=右中(左枝) 2=左中(右枝)
331	    if (fx === 22 || fx === 0) {   // fx=0：1/13 概率的顶冠变体（TreePass 与原版一致）
332	      img = atlas.ensureVImage(`vanilla/Tree_Tops_${crown}.png`)
333	        ?? atlas.ensureVImage(`vanilla/Tree_Tops_${style}.png`) ?? null;
334	      if (!img) return;
335	      // 帧尺寸按 PNG 实宽推导（3 变体 + 2px 间隔），自动覆盖全部样式（含神圣 140 高）
336	      [sw, sh] = treeTopSize(img);
337	      sx = frame * (sw + 2); anchor = 0;
338	    } else {
339	      // 分叉枝（原版固定 40×40 帧、42px 步长；左枝 X=0 / 右枝 X=42；Y = frame*42）
340	      img = atlas.ensureVImage(`vanilla/Tree_Branches_${crown}.png`)
341	        ?? atlas.ensureVImage(`vanilla/Tree_Branches_${style}.png`) ?? null;
342	      if (!img) return;
343	      sw = 40; sh = 40;
344	      sx = fx === 44 ? 0 : 42;
345	      sy = frame * 42; anchor = fx === 44 ? 1 : 2;
346	    }
347	    if (sx + sw > img.width || sy + sh > img.height) return;
348	    let dx = px, dy = py;
349	    if (anchor === 0) { dx = px + (TILE - sw) / 2; dy = py + TILE - sh; }
350	    else if (anchor === 1) { dx = px + TILE - sw; dy = py + (TILE - sh) / 2; }
351	    else { dy = py + (TILE - sh) / 2; }
352	    ctx.drawImage(img, sx, sy, sw, sh, dx, dy, sw, sh);
353	    return;
354	  }
355	  if (foliageOnly) return; // 外扩遍只画树冠/树枝
356	  // 树干贴图来源（TileDrawing GetTileDrawData case 5 vs 583-589/596/616/634 实证）：
357	  // 仅 tile 5 普通树按树下草地生物群系选 Tiles_5_N 变体（frameX += 176*(biome+1)）；
358	  // 宝石树/装饰树/灰烬树的树干 = 自身 sheet（Tiles_596 等），不查生物群系——
359	  // 此前一律套 Tiles_5(_N) 致樱花树长出普通树干（用户标注）
360	  const img = sheet === 5
361	    ? (() => {
362	        // TEdit baseX 奇偶修正（特殊帧横向偏一列扫草地）+ 100 格深扫描
363	        let baseX = 0;
364	        if (fx === 66 && fy <= 45) baseX++;
365	        if (fx === 88 && fy >= 66 && fy <= 110) baseX--;
366	        if (fx === 22 && fy >= 132 && fy < 198) baseX--;
367	        if (fx === 44 && fy >= 132 && fy < 198) baseX++;
368	        const type = scanTreeType(st, x + baseX, y).type;
369	        return type >= 0
370	          ? atlas.ensureVImage(`vanilla/Tiles_5_${type}.png`) ?? atlas.ensureVImage('vanilla/Tiles_5.png')
371	          : atlas.ensureVImage('vanilla/Tiles_5.png');
372	      })()
373	    : atlas.ensureVImage(`vanilla/Tiles_${sheet}.png`);
374	  if (!img) return;
375	  if (fx + 20 <= img.width && fy + 20 <= img.height) {
376	    // 原版 GetTileDrawData case 5(:4688-4694)+ DrawBasicTile(:1019-1025):
377	    // 20×20 精灵**顶锚定**、X 居中 -2((20-16)/2)——向下溢出 4px 压住下方格顶,
378	    // 干底与草块的接缝由下溢覆盖。此前按测量美术高度底锚定,整体上移 4px,
379	    // 干底停在格边界 → wld 导入出现透明接缝(用户标注)
380	    ctx.drawImage(img, fx, fy, 20, 20, px - 2, py, 20, 20);
381	  }
382	}
383	
384	/** 仙人掌渲染（tile 80，移植 TEdit WorldRenderXna 5467-5706）：
385	 *  wld 不存仙人掌帧——按邻接关系现场判定角色并取 Tiles_80（18px 网格）对应帧：
386	 *  - 列高比较：相邻列更高 → 本列是手臂（左臂 X=3 / 右臂 X=2；顶端 X=6）
387	 *  - 主干：顶格 Y=0（含手臂连接位 X=1/4/5），身格 (0,1)
388	 *  - 生物群系变体：向下扫 100 格沙类 → Evil/Good/Crimson_Cactus 独立贴图 */
389	/** 仙人掌生物群系贴图（向下扫沙类：腐化/猩红/神圣 → 独立变体贴图）。
390	 *  扫描带 baseX 偏移（TEdit 同款）：手臂格朝主干列方向扫——手臂列自身下方
391	 *  可能没有沙（如浮空装饰/黑檀石地基），直下扫会漏判 */
392	export function cactusTextureFor(atlas: SpriteAtlas, st: TileStore, x: number, y: number): HTMLImageElement | null {
393	  let img = atlas.ensureVImage('vanilla/Tiles_80.png');
394	  // 角色判定：与 cactusFrameAt 同一列高比较 → 决定扫描列偏移
395	  const isC = (ax: number, ay: number) => st.inBounds(ax, ay) && st.type[st.idx(ax, ay)] === TILE_BY_KEY['v_80_cactus'];
396	  let top = y;
397	  while (isC(x, top - 1)) top--;
398	  const colH = (ax: number) => { let n = 0; while (isC(ax, top + n)) n++; return n; };
399	  const hSelf = colH(x), hR = colH(x + 1), hL = colH(x - 1);
400	  const baseX = hR > hSelf ? 1 : hL > hSelf ? -1 : 0; // 左臂扫 x+1 / 右臂扫 x-1 / 主干扫 x
401	  const ebonsand = TILE_BY_KEY['v_112_ebonsand_block'] ?? -1;
402	  const crimsand = TILE_BY_KEY['v_234_crimsand_block'] ?? -1;
403	  const pearlsand = TILE_BY_KEY['v_116_pearlsand_block'] ?? -1;
404	  for (let i = 0; i < 100 && y + i < st.h; i++) {
405	    const t = st.type[st.idx(x + baseX, y + i)];
406	    if (t === 0) continue;
407	    if (t === ebonsand) { img = atlas.ensureVImage('vanilla/Evil_Cactus.png') ?? img; break; }
408	    if (t === crimsand) { img = atlas.ensureVImage('vanilla/Crimson_Cactus.png') ?? img; break; }
409	    if (t === pearlsand) { img = atlas.ensureVImage('vanilla/Good_Cactus.png') ?? img; break; }
410	  }
411	  return img ?? null;
412	}
413	
414	/** 仙人掌实际渲染帧（列角色判定，与 drawCactusCell 共用）——供渲染与纠错面板定位 */
415	export function cactusFrameAt(st: TileStore, x: number, y: number, type: number): { col: number; row: number } {
416	  const isC = (ax: number, ay: number) => st.inBounds(ax, ay) && st.type[st.idx(ax, ay)] === type;
417	  // 本列顶部与各列下行高度（同一行起算，对齐 TEdit 的 length1/length2 比较）
418	  let top = y;
419	  while (isC(x, top - 1)) top--;
420	  const colH = (ax: number) => { let n = 0; while (isC(ax, top + n)) n++; return n; };
421	  const hSelf = colH(x), hR = colH(x + 1), hL = colH(x - 1);
422	  const hasN = isC(x, y - 1), hasS = isC(x, y + 1);
423	  let ux = 0, uy = 0;
424	  if (hR > hSelf) {
425	    // 左臂（西侧手臂，贴图靠右桥接主干）：顶格 (3,0) / 身格 (3,1) /
426	    // 底格 (3,2) / 单格孤立手臂才是尖帽 (6,2)
427	    if (!hasN && !hasS) { ux = 6; uy = 2; }
428	    else { ux = 3; uy = !hasN ? 0 : hasS ? 1 : 2; }
429	  } else if (hL > hSelf) {
430	    // 右臂（东侧手臂，贴图靠左桥接主干）：(2,0)/(2,1)/(2,2)，单格尖帽 (6,1)
431	    if (!hasN && !hasS) { ux = 6; uy = 1; }
432	    else { ux = 2; uy = !hasN ? 0 : hasS ? 1 : 2; }
433	  } else {
434	    // 主干：顶格 Y=0 / 身格 Y=2，两者都做手臂连接位判定（w/e/sw/se）
435	    uy = hasN ? 2 : 0;
436	    const w = isC(x - 1, y), sw = isC(x - 1, y + 1), e = isC(x + 1, y), se = isC(x + 1, y + 1);
437	    if (w && !sw && (!e || se)) ux = 4;
438	    else if (e && !se && (!w || sw)) ux = 1;
439	    else if (w && !sw && e && !se) ux = 5;
440	    else ux = 0;
441	  }
442	  return { col: ux, row: uy };
443	}
444	
445	export function drawCactusCell(
446	  ctx: CanvasRenderingContext2D, atlas: SpriteAtlas,
447	  st: TileStore, x: number, y: number, type: number, px: number, py: number,
448	): void {
449	  const { col: ux, row: uy } = cactusFrameAt(st, x, y, type);
450	  // 生物群系变体：向下扫沙类（腐化/猩红/神圣）
451	  const img = cactusTextureFor(atlas, st, x, y);
452	  if (!img) return;
453	  if (ux * 18 + 16 <= img.width && uy * 18 + 16 <= img.height) {
454	    ctx.drawImage(img, ux * 18, uy * 18, 16, 16, px, py, TILE, TILE);
455	  }
456	}
457	
458	/** 绘制一格原版图块。
459	 *  auto：现场算帧；style：显式 18px 帧偏移。
460	 *  重要修正：wld 里多格家具每格 frameX 往往全 0（不是 0/18 交错），
461	 *  直接用存储帧会让 2 格宽家具两格都画锚点帧（重复左侧贴图）。
462	 *  style 模式改为：若本格帧偏移为 0，向左/上扫描同类同物体格子，
463	 *  按到锚点的格距重算帧偏移（锚点=左侧或上方最近格） */
464	export function drawVanillaCell(
465	  ctx: CanvasRenderingContext2D, atlas: SpriteAtlas,
466	  sheet: number, frame: 'auto' | 'style' | 'blend', fw: number, fh: number,
467	  st: TileStore, x: number, y: number, type: number,
468	  same: (t: number) => boolean, px: number, py: number, fx: number, fy: number,
469	  trees?: TreeStyleData,
470	): void {
471	  // 树木族（tile 5 + 宝石树 583-589 + 装饰树 596/616 + 灰烬树 634 + 棕榈 323 + 蘑菇树 72）：
472	  // 树冠/树枝标记帧 + 生物群系树干（TEdit 同一套逻辑）。
473	  // 棕榈干身 frameY 是倾斜偏移（跨列）——主遍跳过，整棵由树族外扩遍绘制防裁剪
474	  if (frame === 'style' && (TREE_SHEET_STYLES[sheet] !== undefined || sheet === 323)) {
475	    if (sheet !== 323) drawTreeCell(ctx, atlas, st, x, y, fx, fy, px, py, sheet, false, trees);
476	    return;
477	  }
478	  // 仙人掌（tile 80）：wld 无帧，按邻接现场分帧 + 生物群系变体
479	  if (sheet === 80 && frame === 'style') {
480	    drawCactusCell(ctx, atlas, st, x, y, type, px, py);
481	    return;
482	  }
483	  // blend 类（泥土/石族/草族/沙/泥/雪）：TEdit BlendRules 移植
484	  // （掩码位序：E=0x1 N=0x10 W=0x100 S=0x1000；角 TR/TL/BL/BR <<16）
485	  if (frame === 'blend') {
486	    const myMeta = atlas.vmeta(sheet);
487	    const myMerge = myMeta?.mergeWith ?? null;
488	    const myStone = !!myMeta?.isStone;
489	    const nMeta = (t: number) => {
490	      const d = TILE_DEFS[t];
491	      return d?.vanilla ? atlas.vmeta(d.vanilla.sheet) : null;
492	    };
493	    // Merges() 链（TEdit TileProperty.Merges）：对方 mergeWith 指向我 / 我指向对方 / 双方同指
494	    const merges = (ot: number) => {
495	      if (ot === type) return true;
496	      const om = nMeta(ot);
497	      if (!om) return false;
498	      const oid = TILE_DEFS[ot]?.vanilla?.sheet ?? -1;
499	      if (om.mergeWith != null && om.mergeWith === sheet) return true;
500	      if (myMerge != null && myMerge === oid) return true;
501	      if (myMerge != null && om.mergeWith != null && myMerge === om.mergeWith) return true;
502	      return false;
503	    };
504	    const dirs: Array<[number, number, number]> = [
505	      [1, 0, 0x1], [0, -1, 0x10], [-1, 0, 0x100], [0, 1, 0x1000],          // E N W S
506	      [1, -1, 0x10000], [-1, -1, 0x100000], [-1, 1, 0x1000000], [1, 1, 0x10000000], // NE NW SW SE
507	    ];
508	    // 原版 BlockStyle 双向连通门控（Framing.cs:92-98 + SelfFrame8Way:199-316）：
509	    // 半砖/坡面按 blockStyleLookup 断开对应方向——half 断上；slope1 断上/右；
510	    // slope2 断上/左；slope3 断下/右；slope4 断下/左。中心与邻居两侧都要放行
511	    //（中心 own edge && 邻居 opposite edge；角落需相邻两条边同时放行）。
512	    // edge mask: bit0=up bit1=down bit2=left bit3=right（blockType 0-5，half=1 slope1-4=2-5）
513	    const BLOCK_STYLE = [0b1111, 0b1110, 0b0110, 0b1010, 0b0101, 0b1001];
514	    const edgesOf = (ii: number): number => {
515	      const b = st.half[ii] ? 1 : (st.slope[ii] >= 1 && st.slope[ii] <= 4 ? st.slope[ii] + 1 : 0);
516	      return BLOCK_STYLE[b];
517	    };
518	    const cE = edgesOf(st.idx(x, y));
519	    // 方向 (dx,dy) 连通 = 中心各分量 edge && 邻居各反向 edge。
520	    // 角方向额外要求两个正交邻居的交叉边（SelfFrame8Way:269-316 Clear() 语义：
521	    // 正交方向未连通时其 BlockStyle 被 Clear → 角检查随之失败）
522	    const DIR_EDGE: Array<[number, number]> = [
523	      [0b1000, 0b0100], // E: 中心 right / 邻居 left
524	      [0b0001, 0b0010], // N: 中心 up / 邻居 down
525	      [0b0100, 0b1000], // W: 中心 left / 邻居 right
526	      [0b0010, 0b0001], // S: 中心 down / 邻居 up
527	      [0b1001, 0b0110], // NE: 中心 up|right / 对角 left|down
528	      [0b0101, 0b1010], // NW: 中心 up|left / 对角 right|down
529	      [0b0110, 0b1001], // SW: 中心 down|left / 对角 up|right
530	      [0b1010, 0b0101], // SE: 中心 down|right / 对角 up|left
531	    ];
532	    // 角方向的正交邻居交叉边：[旁格坐标, 所需 edge]
533	    const CORNER_CROSS: Array<Array<[number, number, number]>> = [
534	      [], [],
535	      [], [],
536	      [[1, 0, 0b0101], [0, -1, 0b1010]],  // NE: E 邻 left|top, N 邻 down|right
537	      [[-1, 0, 0b1001], [0, -1, 0b0110]], // NW: W 邻 right|top, N 邻 down|left
538	      [[-1, 0, 0b1010], [0, 1, 0b0101]],  // SW: W 邻 right|down, S 邻 up|left
539	      [[1, 0, 0b0110], [0, 1, 0b1001]],   // SE: E 邻 left|down, S 邻 up|right
540	    ];
541	    const edgeOK = (ax: number, ay: number, need: number): boolean =>
542	      st.inBounds(ax, ay) && (edgesOf(st.idx(ax, ay)) & need) === need;
543	    let same = 0, mergeMask = 0;
544	    for (let di = 0; di < dirs.length; di++) {
545	      const [dx, dy, bit] = dirs[di];
546	      const [cNeed, nNeed] = DIR_EDGE[di];
547	      const ax = x + dx, ay = y + dy;
548	      if (!st.inBounds(ax, ay)) continue;
549	      const oi = st.idx(ax, ay);
550	      const ot = st.type[oi];
551	      if (ot === 0) continue;
552	      // 中心或邻居任一侧 BlockStyle 断边 → 该方向不连通（不算 same/merge）
553	      if ((cE & cNeed) !== cNeed || (edgesOf(oi) & nNeed) !== nNeed) continue;
554	      // 角方向:两个正交邻居的交叉边也要放行
555	      if (di >= 4) {
556	        let ok = true;
557	        for (const [cdx, cdy, need] of CORNER_CROSS[di]) {
558	          if (!edgeOK(x + cdx, y + cdy, need)) { ok = false; break; }
559	        }
560	        if (!ok) continue;
561	      }
562	      const om = nMeta(ot);
563	      // 同型：石族按 isStone 互认，其余走 Merges 链
564	      if (myStone ? !!om?.isStone : merges(ot)) same |= bit;
565	      // 合并位：邻居是 mergeWith 目标
566	      if (myMerge != null && (TILE_DEFS[ot]?.vanilla?.sheet ?? -1) === myMerge) mergeMask |= bit;
567	    }
568	    const strictness = myMeta?.isGrass ? 2 : myMerge != null ? 1 : 0;
569	    const uv = getUVForMasks(same, mergeMask, strictness, ((x * 7) + (y * 11)) % 3);
570	    const r = atlas.vframe(sheet, uv.col, uv.row);
571	    if (r) {
572	      const si = st.idx(x, y);
573	      const slope = st.slope[si];
574	      const half = !!st.half[si];
575	      if (half && slope === 0) {
576	        ctx.drawImage(r.img, r.sx, r.sy + 8, r.sw, r.sh - 8, px, py + 8, r.sw, r.sh - 8);
577	      } else if (slope > 0 && !half) {
578	        drawSlopedFrame(ctx, r, slope, px, py);
579	      } else {
580	        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px, py, TILE, TILE);
581	      }
582	      return;
583	    }
584	    const fb = atlas.vframe(sheet, 1, 1);
585	    if (fb) ctx.drawImage(fb.img, fb.sx, fb.sy, fb.sw, fb.sh, px, py, TILE, TILE);
586	    return;
587	  }
588	  let r: DrawRect | null = null;
589	  if (frame === 'auto') {
590	    r = frameFor(atlas, sheet, st, x, y, type, same);
591	  } else {
592	    // 重建帧偏移：只针对帧数据全 0 的残缺物体（wld 部分家具）。
593	    // 邻居必须同样存 (0,0) 才视为同物体的待重建格——已带 18px 偏移的邻居
594	    // 一定是相邻物体的格子（如并排宝箱的 (18,0)），必须挡住扫描
595	    let ofx = fx, ofy = fy;
596	    if (ofx === 0 && ofy === 0 && (fw > 1 || fh > 1)) {
597	      // 向左扫描最多 fw-1 格：同类且帧全 0
598	      let ax = 0;
599	      for (let k = 1; k < fw; k++) {
600	        const li = st.idx(x - k, y);
601	        if (st.inBounds(x - k, y) && st.type[li] === type && st.frameX[li] === 0 && st.frameY[li] === 0) ax = k;
602	        else break;
603	      }
604	      ofx = ax * 18;
605	      // 向上扫描最多 fh-1 格：同类且帧全 0
606	      let ay = 0;
607	      for (let k = 1; k < fh; k++) {
608	        const ui2 = st.idx(x, y - k);
609	        if (st.inBounds(x, y - k) && st.type[ui2] === type && st.frameX[ui2] === 0 && st.frameY[ui2] === 0) ay = k;
610	        else break;
611	      }
612	      ofy = ay * 18;
613	    }
614	    // 旧版素材表【分带布局】兼容：wld 帧按新游戏单行布局存储（样式全部横排一行），
615	    // 而素材包里的表较窄、样式分多带排列（一行放不下就换到下一带）。
616	    // 样式索引超出一带容量 → 换带重算（如 Tiles_187：带宽 35 样式×54px，
617	    // 样式 52 头骨 wld 帧 (2808,0) → 实际 (52%35)*54=918, y+36）。
618	    // 带 = 物体占格宽×步长；带高 = 物体占格高×步长
619	    const meta = atlas.vmeta(sheet);
620	    if (meta && fw > 0) {
621	      const imgW = atlas.ensureVImage(meta.sheet)?.width ?? 0;
622	      if (imgW > 0 && ofx + meta.grid[0] > imgW) {
623	        const objW = fw * meta.stride[0];
624	        const bandH = (fh || 1) * meta.stride[1];
625	        const colsPerBand = Math.floor(imgW / objW);
626	        if (colsPerBand > 0) {
627	          const styleIdx = Math.floor(ofx / objW);
628	          if (styleIdx >= colsPerBand) {
629	            ofx = (styleIdx % colsPerBand) * objW + (ofx % objW);
630	            ofy += Math.floor(styleIdx / colsPerBand) * bandH;
631	          }
632	        }
633	      }
634	    }
635	    // 标准 18px stride 像素偏移直取（宝箱 Tiles_21 也是标准网格：
636	    // 样式横向排列 36px/个，closed 状态占前 2 行，下面是开启动画帧）
637	    r = atlas.vframeAt(sheet, ofx, ofy);
638	    if (!r) r = atlas.vframeAt(sheet, 0, 0);
639	  }
640	  if (!r) return;
641	  // 蜡烛类高格（grid 16×20）：底部对齐本格
642	  const dy = py + TILE - r.sh;
643	  // 原版 TileObjectData DrawYOffset：落地家具普遍 +2（腿部插入地面 2px）、
644	  // 挂墙/特殊件为负。从反编译 ObjectData/TileObjectData.cs 全量提取。
645	  let dyOff = DRAW_Y_OFFSET[sheet] ?? 0;
646	  // 火把（tile 4）：原版 GetTileDrawData case 4(:4724-4731) tileWidth=20 → 主绘制
647	  // X = tileX*16 - (20-16)/2(:1020-1025 num5) = 格内居中 -2(左右各溢 2px);
648	  // Y:上方实心 = 天花板火把 tileTop=4 下移(:4727-4730),地面/墙面为 0。
649	  // (此前的 +4 引用了 :1084 的 case 4 —— 那是 tile 726 的半砖坡面分支,不是火把)
650	  const dxOff = sheet === 4 ? -2 : 0;
651	  if (sheet === 4 && st.inBounds(x, y - 1) && st.isSolid(x, y - 1)) dyOff += 4;
652	
653	  // ---- 坡面/半砖分支(原版 TileDrawing.cs:1314-1361) ----
654	  const si = st.idx(x, y);
655	  const slope = st.slope[si];
656	  const half = !!st.half[si];
657	  const dpx = px + dxOff, dpy = Math.max(py, dy) + dyOff;
658	  if (half && slope === 0) {
659	    // 半砖:画下半 8px(源 y+8 高-8,目标 y+8;GetTileDrawData halfBrickHeight=8)
660	    ctx.drawImage(r.img, r.sx, r.sy + 8, r.sw, r.sh - 8, dpx, dpy + 8, r.sw, r.sh - 8);
661	    return;
662	  }
663	  if (slope > 0 && !half) {
664	    drawSlopedFrame(ctx, r, slope, dpx, dpy);
665	    return;
666	  }
667	
668	  ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, dpx, dpy, r.sw, r.sh);
669	  void fw; void fh;
670	}
671	
672	/**
673	 * 坡面切条绘制(原版 TileDrawing.cs:1328-1360 1:1):非独立贴图帧,同帧错位采样。
674	 * slope1(左高右低)/2(右高左低):8 条 2px 竖条,每条从帧顶部取高 14-2i,
675	 * 目标 y 逐条下移 2i;补底部 16×2 整条。
676	 * slope3(左低右高)/4(右低左高):8 条 2px 竖条,源行偏移 2i(取帧中段),
677	 * 目标 y=0;补顶部 16×2 整条。
678	 */
679	function drawSlopedFrame(ctx: CanvasRenderingContext2D, r: { img: HTMLImageElement | HTMLCanvasElement; sx: number; sy: number; sw: number; sh: number }, slope: number, px: number, py: number): void {
680	  const fx = r.sx, fy = r.sy;
681	  for (let i = 0; i < 8; i++) {
682	    let num19: number; // 源X/目标X
683	    let num17: number; // 条高
684	    let num18: number; // 源行偏移
685	    let num16: number; // 目标Y附加偏移
686	    if (slope === 1) { num16 = 0; num19 = i * 2; num17 = 14 - i * 2; num18 = 0; }
687	    else if (slope === 2) { num16 = 0; num19 = 16 - i * 2 - 2; num17 = 14 - i * 2; num18 = 0; }
688	    else if (slope === 3) { num16 = i * -2; num19 = i * 2; num17 = 16 - i * 2; num18 = 16 - num17; }
689	    else { num16 = i * -2; num19 = 16 - i * 2 - 2; num17 = 16 - i * 2; num18 = 16 - num17; }
690	    const dstY = i * 2 + num16;
691	    // 源矩形越界保护（HTMLImageElement/HTMLCanvasElement 均有 .width/.height）
692	    if (fx + num19 + 2 > r.img.width || fy + num18 + num17 > r.img.height) continue;
693	    ctx.drawImage(r.img, fx + num19, fy + num18, 2, num17, px + num19, py + dstY, 2, num17);
694	  }
695	  // 补条:slope 1/2 在底部 y=14,slope 3/4 在顶部 y=0
696	  const padY = slope <= 2 ? 14 : 0;
697	  if (fy + padY + 2 <= r.img.height) {
698	    ctx.drawImage(r.img, fx, fy + padY, 16, 2, px, py + padY, 16, 2);
699	  }
700	}
701	
702	/** 原版 TileObjectData.newTile.DrawYOffset 全量表（ObjectData/TileObjectData.cs 逐条提取；未列出 = 0） */
703	const DRAW_Y_OFFSET: Record<number, number> = {
704	  33: -4, 34: -2, 42: -2, 49: -4, 78: 2, 81: -8, 82: -1, 85: 2, 89: 2, 91: -2, 93: 2, 95: -2,
705	  100: 2, 102: 2, 104: 2, 105: 2, 126: -2, 132: 2, 133: 2, 134: 2, 135: 2, 136: 2, 139: 2,
706	  142: 2, 143: 2, 174: -4, 186: 2, 187: 2, 207: 2, 210: 2, 215: 2, 217: 2, 218: 2, 219: 2,
707	  220: 2, 227: -6, 228: 2, 231: 2, 243: 2, 244: 2, 247: 2, 254: 2, 270: -2, 271: -2, 275: 2,
708	  282: 2, 283: 2, 285: 2, 300: 2, 301: 2, 302: 2, 303: 2, 304: 2, 305: 2, 306: 2, 307: 2,
709	  308: 2, 324: -2, 349: 2, 354: 2, 355: 2, 372: -4, 377: 2, 378: 2, 388: -2, 389: -2, 412: 2, 428: 2,
710	  444: -2, 454: -2, 455: 2, 457: 2, 463: 2, 464: 2, 465: -2, 470: 2, 475: 2, 485: 2, 490: 2,
711	  491: 2, 494: 2, 499: 2, 505: 2, 506: 2, 520: 2, 521: 2, 522: 2, 523: 2, 524: 2, 525: 2,
712	  526: 2, 527: 2, 543: 2, 547: 2, 548: 2, 552: 2, 560: 2, 564: 2, 565: 2, 567: 2, 568: 2,
713	  569: 2, 570: 2, 572: -2, 579: -2, 581: -2, 591: -2, 592: -2, 593: 2, 594: 2, 597: 2, 598: 2,
714	  613: 2, 614: 2, 617: 2, 621: 2, 622: 2,
715	};
716	

```


---

## 🤖 Assistant · 2026-08-11T15:58:39.427Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the TS implementation. I still need:
1. SpriteAtlas.ts vmeta/grid/stride (relevant to seam handling).
2. Confirm whether TS handles halfBrickHeight computation (where does halfBrickHeight=8 get set in original? Let me check — in GetTileDrawData, halfBrickHeight initialized 0; where is it set to 8? Let me grep).
3. Check DrawSingleTile_SlicedBlock — sliced drawing.
4. Check case 518 (lava droplet) etc.

Let me grep halfBrickHeight assignments and check DrawSingleTile_SlicedBlock. Also check the tileTop layering (Layer_OverTiles etc.) semantics.

Also, DRAW_Y_OFFSET in our table: I have it. Need to compare against vanilla GetTileDrawData tileTop=2 list.

Vanilla tileTop=2 cases (from GetTileDrawData):
- 752 (also 36×38)
- 443 (tileFrameX/36 >= 2 ? -2 : 2)
- 571 (2)
- 136 (tileFrameX==0 → 2)
- 561 (tileTop -= 2; height 20)
- 518 (liquid-based dynamic)
- 330-333 (+2)
- 78,85,133,134,173,210,233,254,283,378,457,466,520,651,652 (2)
- 100 (2)
- 530 (2)
- 705 (2)
- 485 (2), 489 (2), 490 (2)
- 33,49,174,372,646 (height 20, tileTop -4)
- 529 (height 32, top -14)
- 654 (+2)
- 132,135 (2, height18)
- 82,83,84 (height 20, top -2)
- 324 (20×20, top -2)
- 494 (2)
- 80,142,143 (2)
- 139 (2)
- 73,74,113 (top -12, height 32)
- 388,389 (-2 / 0)
- 227 (32×38, -6/-20)
- 624,700 (20×16, +2)
- 656,701 (24×34, -16)
- 579 (20×20, -2)
- 567 (26×18, frameY==0→-2)
- 185,186,187 (2)
- 650 (2), 649 (2), 647/706 (2), 648 (2)
- 178 (frameY<=36 → 2)
- 184 (width 20; frameY<=36→2; <=108→-2)
- 519 (2)
- 493 (2)
- 28,105,470,475,506,547,548,552,560,597,613,621,622,623,653,699 (2)
- 617 (2)
- 614 (2)
- 300-308,354,355,499 (2)
- 377 (2)
- 463,464 (2)
- 491 (2)
- 349 (2)
- 412 (2)
- 36 (2)
- 455 (2)
- 238 (2)
- 593 (2), 594 (2)
- 228,231,243,247 (2)
- 244 (2), 565 (2)
- 217,218,564 (2), 219,220,642 (2)
- 428 (+4)
- 442 (20×20; case1 -4; case2 -2 w24; case3 -2)
- cages 275+ etc (2)
- 207 (2)

Also tileWidth≠16 cases:
- 752: 36
- 751: 56
- 726: 20
- 698: 36
- 5: 20
- 583-589,596,616,634: 20
- 476: 20 (h 18)
- 323: 20
- 4: 20
- 711: 18 (if frameX>0)
- 227: 32
- 624,700: 20
- 656,701: 24
- 579: 20
- 567: 26
- 81: 24
- 184: 20
- 442: 20/24
- 82-84: height 20 (width 16)

tileHeight≠16:
- 752: 38, 751: 46, 726: 20, 698: 44, 561: 20, 5/583-589/596/616/634: 20, 476: 18, 323: 20, 4: 20, 33/49/174/372/646: 20, 529: 32, 3/24/61/71/110/201/637/703: 20, 20/590/595: 18, 615: 18, 16,17,26,32,69,72,77,124,137,138,352,462,487,488,574-578,664,695,704,712-716: 18, 79: 18, 14/21/411/467/469: conditional 18, 15/497: 18, 172/376: 18, 27: 18, 132/135: 18, 82-84: 20, 324: 20, 73/74/113: 32, 388/389: 18 cond, 227: 38, 624/700: 16, 656/701: 34, 579: 20, 567: 18, 81: 26, 406: 16/18, 405: 16/18, 441/468: 18 cond, 711: 20, 442: 20, 518: 16 (tileTop dynamic), 90: 16 (default, but addFr adjustments), 114: rectangle.Height += 2 (in DrawSingleTile loop, not GetTileDrawData).

Wait, where does halfBrickHeight get set to 8? Let me grep. Probably in the caller of GetTileDrawData or after. Actually in the DrawSingleTile method before calling. Let me check lines ~860-880.

Also need to check DoNotAdjustDrawPositionBasedOnTileWidth (711).

Let me also check DrawSingleTile_SlicedBlock and the liquid (518) details. And check TS SpriteAtlas vmeta.

Let me grep halfBrickHeight.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:40.004Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"halfBrickHeight\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | head -30; echo ---; grep -n \"DrawSingleTile_SlicedBlock\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "description": "Find halfBrickHeight assignment and sliced block drawer"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:40.061Z

**📎 ToolResult**

```
884:		GetTileDrawData(tileX, tileY, tileDrawInfo.tileCache, tileDrawInfo.typeCache, ref tileDrawInfo.tileFrameX, ref tileDrawInfo.tileFrameY, out tileDrawInfo.tileWidth, out tileDrawInfo.tileHeight, out tileDrawInfo.tileTop, out tileDrawInfo.halfBrickHeight, out tileDrawInfo.addFrX, out tileDrawInfo.addFrY, out tileDrawInfo.tileSpriteEffect, out tileDrawInfo.glowTexture, out tileDrawInfo.glowSourceRect, out tileDrawInfo.glowColor);
1019:		Rectangle rectangle = new Rectangle(tileDrawInfo.tileFrameX + tileDrawInfo.addFrX, tileDrawInfo.tileFrameY + tileDrawInfo.addFrY, tileDrawInfo.tileWidth, tileDrawInfo.tileHeight - tileDrawInfo.halfBrickHeight);
1025:		Vector2 vector = new Vector2((float)(tileX * 16 - (int)screenPosition.X) - num5, tileY * 16 - (int)screenPosition.Y + tileDrawInfo.tileTop + tileDrawInfo.halfBrickHeight) + screenOffset;
1658:		if (drawData.halfBrickHeight == 8 && (!Main.tile[tileX, tileY + 1].active() || !_tileSolid[Main.tile[tileX, tileY + 1].type] || Main.tile[tileX, tileY + 1].halfBrick()))
4562:	private void GetTileDrawData(int x, int y, Tile tileCache, ushort typeCache, ref short tileFrameX, ref short tileFrameY, out int tileWidth, out int tileHeight, out int tileTop, out int halfBrickHeight, out int addFrX, out int addFrY, out SpriteEffects tileSpriteEffect, out Texture2D glowTexture, out Rectangle glowSourceRect, out Color glowColor)
4567:		halfBrickHeight = 0;
6139:			halfBrickHeight = 8;
6174:			glowSourceRect = new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight);
8499:			GetTileDrawData(x, y, tile, type, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var glowTexture, out var glowSourceRect, out var glowColor);
8529:				DrawNature(tileDrawTexture, position, new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), tileLight, num3 * 0.1f, new Vector2(tileWidth / 2, 16 - halfBrickHeight - tileTop), 1f, tileSpriteEffect, 0f);
8532:					DrawNatureGlowmask(glowTexture, position, glowSourceRect, glowColor, num3 * 0.1f, new Vector2(tileWidth / 2, 16 - halfBrickHeight - tileTop), 1f, tileSpriteEffect, 0f);
8557:			GetTileDrawData(x, y, tile, type, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var glowTexture, out var _, out var glowColor);
8584:			Vector2 origin = new Vector2(tileWidth / 2, 16 - halfBrickHeight - tileTop);
8590:				origin = new Vector2(tileWidth / 2, 16 - halfBrickHeight - tileTop);
8608:				origin = new Vector2(2f, (16 - halfBrickHeight - tileTop) / 2);
8617:				origin = new Vector2(14f, (16 - halfBrickHeight - tileTop) / 2);
8628:				DrawNature(tileDrawTexture, position, new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), tileLight, num3 * 0.1f, origin, 1f, tileSpriteEffect, 0f);
8631:					DrawNatureGlowmask(glowTexture, position, new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), glowColor, num3 * 0.1f, origin, 1f, tileSpriteEffect, 0f);
9137:				GetTileDrawData(i, j, tile, type2, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var _, out var _, out var _);
9188:					DrawNature(tileDrawTexture, vector + new Vector2(0f, vector3.Y), new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), tileLight, windCycle * num * num3, origin, 1f, tileSpriteEffect, 0f, sideFlags);
9191:						DrawNatureGlowmask(texture2D, vector + new Vector2(0f, vector3.Y), new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY + num2, tileWidth, tileHeight - halfBrickHeight), color, windCycle * num * num3, origin, 1f, tileSpriteEffect, 0f);
9247:			GetTileDrawData(x, i, tile, type, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var glowTexture, out var glowSourceRect, out var glowColor);
9291:				DrawNature(tileDrawTexture, position, new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), color, num6, new Vector2(tileWidth / 2, halfBrickHeight - tileTop), 1f, tileSpriteEffect, 0f, flag ? SideFlags.Bottom : SideFlags.None);
9294:					DrawNatureGlowmask(glowTexture, position, glowSourceRect, glowColor, num6, new Vector2(tileWidth / 2, halfBrickHeight - tileTop), 1f, tileSpriteEffect, 0f);
9341:				GetTileDrawData(x, num6, tile, type, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var _, out var _, out var _);
9357:					DrawNature(tileDrawTexture, position, new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), color, num7, new Vector2(tileWidth / 2, halfBrickHeight - tileTop + tileHeight), 1f, tileSpriteEffect, 0f, flag ? SideFlags.Top : SideFlags.None);
9654:				GetTileDrawData(i, j, tile2, type2, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var _, out var _, out var _);
9673:				Rectangle rectangle = new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight);
---
1655:			DrawSingleTile_SlicedBlock(normalTilePosition, tileX, tileY, drawData);
3545:	private void DrawSingleTile_SlicedBlock(Vector2 normalTilePosition, int tileX, int tileY, TileDrawInfo drawData)

```


---

## 🤖 Assistant · 2026-08-11T15:58:40.378Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"vmeta\\|grid\\|stride\\|DrawRect\\|rows\" ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts | head -40",
 "description": "Locate vmeta/grid/stride in SpriteAtlas.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:40.438Z

**📎 ToolResult**

```
43:export interface DrawRect { img: HTMLImageElement | HTMLCanvasElement; sx: number; sy: number; sw: number; sh: number; }
110:  grid: [number, number];      // 帧像素尺寸（蜡烛类 [16,20]）
111:  stride: [number, number];    // 表内帧步长（grid+gap，如 [18,18]）
113:  cols: number; rows: number;
123:  grid: [number, number]; stride: [number, number]; cols: number; rows: number;
205:  vmeta(sheetId: number): VanillaTileMeta | null {
210:  vframe(sheetId: number, col: number, row: number): DrawRect | null {
211:    const m = this.vmeta(sheetId);
215:    if (col < 0 || row < 0 || col >= m.cols || row >= m.rows) return null;
216:    return { img, sx: col * m.stride[0], sy: row * m.stride[1], sw: m.grid[0], sh: m.grid[1] };
220:  vframeAt(sheetId: number, fx: number, fy: number): DrawRect | null {
221:    const m = this.vmeta(sheetId);
227:    if (fx < 0 || fy < 0 || fx + m.grid[0] > img.width || fy + m.grid[1] > img.height) return null;
228:    return { img, sx: fx, sy: fy, sw: m.grid[0], sh: m.grid[1] };
232:  vrect(sheetId: number, fx: number, fy: number, w: number, h: number): DrawRect | null {
233:    const m = this.vmeta(sheetId);
244:  vnpc(npcId: number, frameIdx: number): DrawRect | null {
280:  vmisc(path: string): DrawRect | null {
288:  vui(name: string): DrawRect | null {
312:  vicon(itemId: number): DrawRect | null {
455:  rect(file: string, sprite: string): DrawRect | null {
464:  animFrames(anim: string): DrawRect[] {
466:    return frames.map((f) => this.rect(f.file, f.sprite)).filter(Boolean) as DrawRect[];
473:export function atlasIconForKey(atlas: SpriteAtlas, key: string): DrawRect | null {

```


---

## 🤖 Assistant · 2026-08-11T15:58:43.595Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
halfBrickHeight = 8 is set at :6139, which is after GetTileDrawData's switch — let me read 6100-6180 to see the post-switch logic.

Also DrawSingleTile_SlicedBlock at 3545 — let me read that (it's the lighting-sliced block drawing which is the main seam mechanism for solid blocks!). This is important: for solid blocks with lighting (NotRetro), vanilla draws the tile sliced into 4 quadrants each lit separately. This is a seam-related mechanism (per-tile lighting slices), which is likely not in TS (TS uses no lighting). I'll mention it.

Let me read 6100-6180 and 3545-3640.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:58:43.891Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 80,
 "offset": 6100
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:43.902Z

**📎 ToolResult**

```
6100				break;
6101			case 507:
6102			case 508:
6103			{
6104				int num = 20;
6105				int num2 = (Main.tileFrameCounter[typeCache] + x * 11 + y * 27) % (num * 8);
6106				addFrY = 90 * (num2 / num);
6107				break;
6108			}
6109			case 336:
6110			case 340:
6111			case 341:
6112			case 342:
6113			case 343:
6114			case 344:
6115				addFrY = Main.tileFrame[typeCache] * 90;
6116				tileTop = 2;
6117				break;
6118			case 89:
6119				tileTop = 2;
6120				break;
6121			case 102:
6122				tileTop = 2;
6123				break;
6124			}
6125			if (TileID.Sets.Campfires[tileCache.type])
6126			{
6127				if (tileFrameY < 36)
6128				{
6129					addFrY = Main.tileFrame[typeCache] * 36;
6130				}
6131				else
6132				{
6133					addFrY = 252;
6134				}
6135				tileTop = 2;
6136			}
6137			if (tileCache.halfBrick())
6138			{
6139				halfBrickHeight = 8;
6140			}
6141			switch (typeCache)
6142			{
6143			case 412:
6144				glowTexture = TextureAssets.GlowMask[202].Value;
6145				glowSourceRect = new Rectangle(tileFrameX, tileFrameY + addFrY, tileWidth, tileHeight);
6146				glowColor = new Color(255, 255, 255, 255);
6147				break;
6148			case 657:
6149				if (tileFrameY >= 54)
6150				{
6151					glowTexture = TextureAssets.GlowMask[330].Value;
6152					glowSourceRect = new Rectangle(tileFrameX, tileFrameY + addFrY, tileWidth, tileHeight);
6153					glowColor = Color.White;
6154				}
6155				break;
6156			case 656:
6157			case 701:
6158				glowTexture = TextureAssets.GlowMask[329].Value;
6159				glowSourceRect = new Rectangle(tileFrameX, tileFrameY + addFrY, tileWidth, tileHeight);
6160				glowColor = new Color(255, 255, 255, 0) * ((float)(int)Main.mouseTextColor / 255f);
6161				break;
6162			case 634:
6163				glowTexture = TextureAssets.GlowMask[315].Value;
6164				glowSourceRect = new Rectangle(tileFrameX, tileFrameY + addFrY, tileWidth, tileHeight);
6165				glowColor = Color.White;
6166				break;
6167			case 637:
6168				glowTexture = GetTileDrawTexture(tileCache, x, y);
6169				glowSourceRect = new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight);
6170				glowColor = Color.Lerp(Color.White, color, 0.75f);
6171				break;
6172			case 638:
6173				glowTexture = TextureAssets.GlowMask[327].Value;
6174				glowSourceRect = new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight);
6175				glowColor = Color.Lerp(Color.White, color, 0.75f);
6176				break;
6177			case 568:
6178				glowTexture = TextureAssets.GlowMask[268].Value;
6179				glowSourceRect = new Rectangle(tileFrameX, tileFrameY + addFrY, tileWidth, tileHeight);

```


---

## 🤖 Assistant · 2026-08-11T15:58:44.160Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 90,
 "offset": 3545
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:58:44.168Z

**📎 ToolResult**

```
3545		private void DrawSingleTile_SlicedBlock(Vector2 normalTilePosition, int tileX, int tileY, TileDrawInfo drawData)
3546		{
3547			Color color = default(Color);
3548			Vector2 origin = default(Vector2);
3549			Rectangle value = default(Rectangle);
3550			Vector3 tileLight = default(Vector3);
3551			Vector2 position = default(Vector2);
3552			if (drawData.tileLight.R > _highQualityLightingRequirement.R || drawData.tileLight.G > _highQualityLightingRequirement.G || drawData.tileLight.B > _highQualityLightingRequirement.B)
3553			{
3554				Vector3[] slices = drawData.colorSlices;
3555				Lighting.GetColor9Slice(tileX, tileY, ref slices);
3556				Vector3 vector = drawData.tileLight.ToVector3();
3557				Vector3 tint = drawData.colorTint.ToVector3();
3558				if (drawData.tileCache.fullbrightBlock())
3559				{
3560					slices = _glowPaintColorSlices;
3561				}
3562				for (int i = 0; i < 9; i++)
3563				{
3564					value.X = 0;
3565					value.Y = 0;
3566					value.Width = 4;
3567					value.Height = 4;
3568					switch (i)
3569					{
3570					case 1:
3571						value.Width = 8;
3572						value.X = 4;
3573						break;
3574					case 2:
3575						value.X = 12;
3576						break;
3577					case 3:
3578						value.Height = 8;
3579						value.Y = 4;
3580						break;
3581					case 4:
3582						value.Width = 8;
3583						value.Height = 8;
3584						value.X = 4;
3585						value.Y = 4;
3586						break;
3587					case 5:
3588						value.X = 12;
3589						value.Y = 4;
3590						value.Height = 8;
3591						break;
3592					case 6:
3593						value.Y = 12;
3594						break;
3595					case 7:
3596						value.Width = 8;
3597						value.Height = 4;
3598						value.X = 4;
3599						value.Y = 12;
3600						break;
3601					case 8:
3602						value.X = 12;
3603						value.Y = 12;
3604						break;
3605					}
3606					tileLight.X = (slices[i].X + vector.X) * 0.5f;
3607					tileLight.Y = (slices[i].Y + vector.Y) * 0.5f;
3608					tileLight.Z = (slices[i].Z + vector.Z) * 0.5f;
3609					GetFinalLight(drawData.tileCache, drawData.typeCache, ref tileLight, ref tint);
3610					position.X = normalTilePosition.X + (float)value.X;
3611					position.Y = normalTilePosition.Y + (float)value.Y;
3612					value.X += drawData.tileFrameX + drawData.addFrX;
3613					value.Y += drawData.tileFrameY + drawData.addFrY;
3614					int num = (int)(tileLight.X * 255f);
3615					int num2 = (int)(tileLight.Y * 255f);
3616					int num3 = (int)(tileLight.Z * 255f);
3617					if (num > 255)
3618					{
3619						num = 255;
3620					}
3621					if (num2 > 255)
3622					{
3623						num2 = 255;
3624					}
3625					if (num3 > 255)
3626					{
3627						num3 = 255;
3628					}
3629					num3 <<= 16;
3630					num2 <<= 8;
3631					color.PackedValue = (uint)(num | num2 | num3 | -16777216);
3632					Main.tileBatch.Draw(drawData.drawTexture, position, value, color, origin, 1f, drawData.tileSpriteEffect);
3633				}
3634			}

```


---

## 🤖 Assistant · 2026-08-11T15:59:10.798Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have a solid picture. Let me also quickly verify a couple of items:

1. The TS DRAW_Y_OFFSET list — compare to vanilla tileTop=2 list. Vanilla tileTop=2 tile ids. Let me build the vanilla list of tileTop=2 (from GetTileDrawData):

tileTop = 2 (or +=2):
- 752 (2)
- 443 (2 if frameX/36<2, else -2)
- 571 (2)
- 136 (2 if frameX==0)
- 561 (-2)
- 330,331,332,333 (+2)
- 78, 85, 133, 134, 173, 210, 233, 254, 283, 378, 457, 466, 520, 651, 652 (2)
- 100 (2)
- 530 (2)
- 705 (2)
- 485, 489, 490 (2)
- 654 (+2)
- 132,135 (2)
- 494 (2)
- 80,142,143 (2)
- 139 (2)
- 185,186,187 (2)
- 650 (2), 649 (2), 647,706 (2), 648 (2)
- 178 (2 if frameY<=36)
- 184 (2 if frameY<=36, else -2 if <=108)
- 519 (2)
- 493 (2)
- 28,105,470,475,506,547,548,552,560,597,613,621,622,623,653,699 (2)
- 617 (2)
- 614 (2)
- 300-308,354,355,499 (2)
- 377 (2)
- 463,464 (2)
- 491 (2)
- 349 (2)
- 412 (2)
- 36 (2)
- 455 (2)
- 238 (2)
- 593 (2), 594 (2)
- 228,231,243,247 (2)
- 244 (2), 565 (2)
- 217,218,564 (2), 219,220,642 (2)
- 428 (+4)
- cages (275...645, 568-570, 521-527, 316-318, etc.) (2)
- 207 (2)
- 336,340-344 (2) [at 6109-6117]
- 89 (2) [6118]
- 102 (2) [6121]
- Campfires (Sets.Campfires) (2) [6125-6136]

Negative tops:
- 443 (-2 when frameX/36>=2)
- 561 (-2)
- 33,49,174,372,646 (-4)
- 529 (-14)
- 82,83,84 (-2)
- 324 (-2)
- 52,62,115,205,382,528,636,638 (-2)
- 73,74,113 (-12)
- 388,389 (-2 or 0)
- 227 (-6/-20)
- 656,701 (-16)
- 579 (-2)
- 567 (-2 when frameY==0)
- 184 (-2 when frameY<=108 && >36)
- 81 (-8)
- 518 (dynamic liquid)
- 442 (-4/-2/-2)
- 624,700 (+2)
- 726 (special vector offsets in DrawSingleTile, not tileTop)

Now TS DRAW_Y_OFFSET (from VanillaTiler.ts:703-715):
33:-4, 34:-2, 42:-2, 49:-4, 78:2, 81:-8, 82:-1, 85:2, 89:2, 91:-2, 93:2, 95:-2, 100:2, 102:2, 104:2, 105:2, 126:-2, 132:2, 133:2, 134:2, 135:2, 136:2, 139:2, 142:2, 143:2, 174:-4, 186:2, 187:2, 207:2, 210:2, 215:2, 217:2, 218:2, 219:2, 220:2, 227:-6, 228:2, 231:2, 243:2, 244:2, 247:2, 254:2, 270:-2, 271:-2, 275:2, 282:2, 283:2, 285:2, 300-308:2, 324:-2, 349:2, 354:2, 355:2, 372:-4, 377:2, 378:2, 388:-2, 389:-2, 412:2, 428:2, 444:-2, 454:-2, 455:2, 457:2, 463:2, 464:2, 465:-2, 470:2, 475:2, 485:2, 490:2, 491:2, 494:2, 499:2, 505:2, 506:2, 520:2, 521-527:2, 543:2, 547:2, 548:2, 552:2, 560:2, 564:2, 565:2, 567:2, 568:2, 569:2, 570:2, 572:-2, 579:-2, 581:-2, 591:-2, 592:-2, 593:2, 594:2, 597:2, 598:2, 613:2, 614:2, 617:2, 621:2, 622:2.

Note the TS table is sourced from TileObjectData.DrawYOffset (ObjectData), which is a *different* source than GetTileDrawData tileTop! Interesting — TileObjectData.newTile.DrawYOffset is applied at frame placement (in TileObjectData DrawYOffset affects frameY?), actually in vanilla, TileObjectData DrawYOffset offsets where the object's frames are placed? No — actually in Terraria, `TileObjectData.DrawYOffset` isn't used for rendering directly... Hmm. Actually there IS `DrawYOffset` in TileObjectData used by TileDrawing? Let me think. In TileDrawing, tileTop comes from GetTileDrawData switch only. TileObjectData.DrawYOffset is used in... hmm, I believe it's not used in rendering at all; it may be vestigial. Let me check quickly: grep DrawYOffset in the decompiled source to see where it's used. This matters for the audit: if our table comes from TileObjectData but vanilla rendering uses GetTileDrawData's tileTop, the values may differ (e.g., 82: -1 in ours vs vanilla -2; 95:-2 vs vanilla...? 95 isn't in GetTileDrawData list... 34/42/91/93/95/126/215/270/271/444/454/465/572/581/591/592 not in GetTileDrawData list either).

So there's a real discrepancy: the two sources are different mechanisms. Let me verify with grep where DrawYOffset is referenced.

Also I should check differences:
- Ours 227: -6 but vanilla is -6 only when frameX==238, else -20. Partially ported (missing -20 branch).
- Ours 388/389: -2 but vanilla: -2 only for certain frames; else 0. Partial.
- Ours 567: 2 but vanilla: -2 when frameY==0 (and no +2!). Wrong sign.
- Ours 82: -1 vs vanilla -2. Mismatch.
- Ours 530 missing (vanilla tileTop=2). Ours doesn't have 530.
- 443 missing (±2).
- 571 missing (+2).
- 330-333 missing (+2).
- 518 missing (dynamic).
- 705 missing.
- 654 missing.
- 184 missing (20 width + ±2).
- 442 missing (20/24 width + -4/-2).
- 579: ours -2 matches vanilla -2. Good.
- 136: ours +2 — vanilla only when frameX==0. Partially (we always apply).
- 489 missing, 493 missing, 519 missing, 178 missing, 185/186/187: ours 186:2,187:2 — 185 missing.
- 617: ours 2 ✓.
- 428: ours +2, vanilla +4! Mismatch (vanilla tileTop += 4).
- 624/700 missing (+2), 656/701 missing (-16), 227 partial, 73/74/113 missing (-12), 529 missing (-14), 33/49/174/372/646: 646 missing, 82-84 ours -1/-2 mismatch (83,84 missing too).

Wait ours has 82:-2? Let me re-read: "78: 2, 81: -8, 82: -1, 85: 2" — so 82:-1 (vanilla -2, mismatch), 83/84 missing.

Also 441/468 etc not in list.

OK. Also important: ours applies dyOff only in the 'style'/'auto' general path (after blend branch) — the blend path returns early without applying DRAW_Y_OFFSET (blend is only for solid blocks with tileTop 0, fine).

Also our dy computation: `const dy = py + TILE - r.sh;` — bottom-aligns when grid sh > 16 (candles 16×20). Note: this bottom alignment is NOT what vanilla does. Vanilla: drawY = tileY*16 + tileTop; a 16×20 sprite with tileTop=0 draws at y=0..20 (overflows DOWN 4px), not bottom-aligned. Hmm — for candles (tile 476: tileWidth 20, tileHeight 18, no tileTop). Vanilla tileHeight=18 means source rect height 18 drawn at top. Our code bottom-aligns: dy = py + 16 - 18 = py - 2 → shifted UP 2px relative to vanilla (vanilla draws 18px starting at py, overflowing to py+18). So candles: ours -2 vs vanilla 0. That's a discrepancy worth flagging (A/B class).

Hmm wait, but for the tree we explicitly chose top-anchored (matching vanilla). For the generic path we do bottom-align. That's inconsistent with vanilla tileTop semantics. Let me note: our generic path anchors sprite bottom to the tile bottom (py + TILE - sh), whereas vanilla anchors TOP at py + tileTop. For sh=18 that's a 2px difference; for 20 a 4px difference.

Let me verify where TileObjectData.DrawYOffset is used in vanilla to confirm our table's provenance is not a rendering path.

Also need to check the DrawYOffset in decompiled ObjectData. Let me grep the whole Terraria dir for DrawYOffset usage.

Also for class D, I should confirm the TS implementation has none of :1609-1660 logic. Indeed: VanillaTiler has no neighbor-halfbrick logic; ChunkCache pass 3 only clearRects top 8px for half bricks. The `IgnoresNearbyHalfbricksWhenDrawn` and `AllBlocksWithSmoothBordersToResolveHalfBlockIssue` sets are not ported. Also missing: the bottom-halfbrick light strip (:1658-1668: when halfBrickHeight==8 and below is not solid → draw rect(144,66,w,4) at +4).

Also missing: DrawSingleTile_SlicedBlock 9-slice lighting (not needed without lighting).
Also missing: HasSlopeFrames (421,422) special path; Platforms slope neighbor fill (:1540-1567); DontDrawTileSliced/DontDrawTileSlopes sets; slope for glowmasks.

Let me quickly grep DrawYOffset usage.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:59:11.179Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"DrawYOffset\" ~/Project/GLM/SandboxWorld/Terarria1456 --include=*.cs | grep -v \"public int DrawYOffset\" | head -20",
 "description": "Find where TileObjectData.DrawYOffset is consumed"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:11.214Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-11T15:59:12.174Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 518\\|tileCache.liquid\\|Lava\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | head; echo ---; grep -rn \"DRAW_Y_OFFSET\\|tileTop\\|halfBrick\\|IgnoresNearby\\|SmoothBorders\\|HasSlopeFrames\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts -l",
 "description": "Check TS files referencing seam-related vanilla mechanisms"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:12.198Z

**📎 ToolResult**

```
857:	private static float LavaLightA(int tileX, int tileY)
880:		if (tileDrawInfo.tileCache.liquid > 0 && tileDrawInfo.tileCache.type == 518)
1216:				float num13 = LavaLightA(tileX, tileY);
3915:		if (tileCache.type == 379 && tileCache.liquid > 0)
3919:		if (tileCache.type == 546 && tileCache.liquid > 0)
3925:			switch (tileCache.liquidType())
3940:			num = tileCache.liquid;
3944:			if (tileCache.liquid > 0 && num4 != 0 && (num4 != 1 || tileCache.liquid > 160))
3947:				switch (tileCache.liquidType())
3962:				if (tileCache.liquid > num)
---
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-11T15:59:13.942Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
zsh glob issue with --include. Use grep -r with --include quoted or use find. Let me redo with quotes.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:59:14.376Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"DrawYOffset\" ~/Project/GLM/SandboxWorld/Terarria1456 2>/dev/null | grep -v \"DrawYOffset = \\|DrawYOffset;\" | head -20",
 "description": "Find consumers of DrawYOffset in decompiled source"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:14.447Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/TileObject.cs:911:					num5 = ((j != 0) ? tileData.DrawYOffset : (tileData.DrawYOffset - 2));
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData/TileObjectData.cs:778:	public int DrawYOffset

```


---

## 🤖 Assistant · 2026-08-11T15:59:14.810Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"DRAW_Y_OFFSET\\|IgnoresNearby\\|SmoothBorders\\|HasSlopeFrames\\|tileTop\" ~/Project/GLM/SandboxWorld/game/src 2>/dev/null",
 "description": "Find TS files referencing seam mechanisms"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:14.841Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts

```


---

## 🤖 Assistant · 2026-08-11T15:59:48.932Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: TileObjectData.DrawYOffset is used only in TileObject.cs:911 — that's the object PLACEMENT preview drawing (TileObject.Draw, i.e., ghost preview when placing), NOT the world tile rendering. So our DRAW_Y_OFFSET table is sourced from a different mechanism than the actual render path (GetTileDrawData tileTop). Many values coincide (since both encode "sit 2px into ground") but several differ. This is an important audit finding.

Let me check TileObject.cs:911 context briefly to confirm it's placement preview.

Also let me verify what TS does about DrawYOffset — they use it as the render-time offset. It's a reasonable approximation but mismatches exist. Let me compute the exact mismatches between our table and vanilla GetTileDrawData tileTop.

Vanilla GetTileDrawData tileTop map (type → value):
+2: 752, 571, 136(only fx==0), 330,331,332,333, 78,85,133,134,173,210,233,254,283,378,457,466,520,651,652, 100,530,705,485,489,490,654,132,135,494,80,142,143,139,185,186,187,650,649,647,706,648,178(fy<=36),184(fy<=36),519,493,28,105,470,475,506,547,548,552,560,597,613,621,622,623,653,699,617,614,300,301,302,303,304,305,306,307,308,354,355,499,377,463,464,491,349,412,36,455,238,593,594,228,231,243,247,244,565,217,218,564,219,220,642, cages(275-281,296,297,309,358,359,413,414,542,550,551,553,554,558,559,599-612,632,640,643,644,645,710, 285,286,298,299,310,339,361-364,391-394,532,533,538,544,555,556,582,619,629, 282,505,543,598,568,569,570,288-295,360,580,620,521-527,316,317,318), 207, 336,340,341,342,343,344, 89, 102, campfires(215 etc? Sets.Campfires)
+4: 4(when solid above — torch), 428
-2: 443(fx/36>=2), 561, 82,83,84, 324, 52,62,115,205,382,528,636,638, 388,389, 579, 567(fy==0), 184(36<fy<=108), 442(case2/3)
-4: 33,49,174,372,646, 442(case1)
-8: 81
-12: 73,74,113
-14: 529
-16: 656,701
-6/-20: 227
dynamic: 518
+2 with 20×16: 624,700

Our table entries vs vanilla:
- 33:-4 ✓(vanilla -4) ✓
- 34:-2 — vanilla: no tileTop for 34 (0). Ours -2. ✗ extra
- 42:-2 — vanilla 0. ✗ extra
- 49:-4 ✓
- 78:2 ✓
- 81:-8 ✓
- 82:-1 — vanilla -2 ✗ value mismatch
- 85:2 ✓
- 89:2 ✓ (vanilla 2 at :6118)
- 91:-2 — vanilla 0 ✗
- 93:2 — vanilla 0 ✗
- 95:-2 — vanilla 0 ✗
- 100:2 ✓
- 102:2 ✓
- 104:2 — vanilla 0 ✗
- 105:2 ✓
- 126:-2 — vanilla 0 ✗
- 132:2 ✓
- 133:2 ✓,134:2 ✓,135:2 ✓
- 136:2 — vanilla only frameX==0 ✗ partial
- 139:2 ✓
- 142:2 ✓,143:2 ✓
- 174:-4 ✓
- 186:2 ✓,187:2 ✓ — 185 missing ✗
- 207:2 ✓
- 210:2 ✓
- 215:2 — campfire, vanilla tileTop=2 via Sets.Campfires ✓ (and addFrY 36/252 handled by campfireYOffset)
- 217:2 ✓,218:2 ✓,219:2 ✓,220:2 ✓
- 227:-6 — vanilla -6 only frameX==238 else -20 ✗ partial
- 228:2 ✓,231:2 ✓,243:2 ✓,244:2 ✓,247:2 ✓
- 254:2 ✓
- 270:-2,271:-2 — vanilla 0 ✗ (270/271/581/572 are addFrX frame shuffle cases, no tileTop)
- 275:2 ✓ (cage)
- 282:2 ✓,283:2 ✓,285:2 ✓
- 300-308:2 ✓
- 324:-2 ✓
- 349:2 ✓,354:2 ✓,355:2 ✓
- 372:-4 ✓
- 377:2 ✓,378:2 ✓
- 388:-2,389:-2 — vanilla: -2 only when frameY in top rows, else 0 ✗ partial
- 412:2 ✓
- 428:2 — vanilla +4 ✗
- 444:-2 — vanilla 0 ✗
- 454:-2 — vanilla 0 ✗ (454 is addFrY anim)
- 455:2 ✓
- 457:2 ✓
- 463:2 ✓,464:2 ✓
- 465:-2 — vanilla 0 ✗
- 470:2 ✓,475:2 ✓
- 485:2 ✓,490:2 ✓,491:2 ✓,494:2 ✓,499:2 ✓
- 505:2 ✓,506:2 ✓
- 520:2 ✓
- 521-527:2 ✓
- 543:2 ✓,547:2 ✓,548:2 ✓,552:2 ✓,560:2 ✓
- 564:2 ✓,565:2 ✓
- 567:2 — vanilla -2 when frameY==0, else 0 ✗ wrong sign
- 568:2 ✓,569:2 ✓,570:2 ✓
- 572:-2 — vanilla 0 ✗
- 579:-2 ✓ (vanilla -2)
- 581:-2 — vanilla 0 ✗
- 591:-2 — vanilla 0 ✗
- 592:-2 — vanilla 0 ✗
- 593:2 ✓,594:2 ✓,597:2 ✓,598:2 ✓
- 613:2 ✓,614:2 ✓,617:2 ✓,621:2 ✓,622:2 ✓

Missing from ours (vanilla has value): 443(±2), 571(+2), 330-333(+2), 530(+2), 705(+2), 489(+2), 654(+2), 185(+2), 178(cond+2), 184(±2 + width20), 493(+2), 519(+2), 336/340-344(+2), 73/74/113(-12), 529(-14), 518(dynamic), 646(-4), 83/84(-2), 624/700(+2,20×16), 656/701(-16,24×34), 442(-4/-2 +20/24 width), 528? wait 528 is in vanilla -2 group (52,62,115,205,382,528,636,638) — ours has none of those except 636/638? Not present. ✗ missing 52,62,115,205,382,528,636,638 (-2)

OK, that's a thorough B comparison.

Now for class A, our implementation: vmeta grid/stride handles sprite size per sheet (e.g., candles 16×20 grid). The generic path draws r.sw × r.sh at (dpx, py + TILE - r.sh + dyOff) — bottom anchored. Vanilla: draws tileWidth × tileHeight at (x*16 - (w-16)/2, y*16 + tileTop) — top anchored, X centered. So:
- Torch (4): handled via dxOff=-2 ✓ (special-cased)
- Tree (5 etc): handled in drawTreeCell with px-2, py, 20×20 ✓ top-anchored
- Palm 323: handled ✓
- Others with width 20 (726, 476, 624/700, 184, 442, 579, 3/24/61/71/110/201/637/703 are height 20 width 16...) — not X-centered in TS generic path. 476 (20×18) missing; 726 (20×20) missing + slope offsets; 579 (20×20) missing; 442, 184, 624/700 missing.
- Bottom-anchoring (dy = py+TILE-r.sh) mismatches vanilla top-anchor for any sh>16 sheet (476: 18 → ours -2 vs vanilla 0; 3/24/61/...: 20 → ours -4 vs vanilla 0; candles grid 16×20 → -4).

Wait — careful. The comment in TS says "蜡烛类高格（grid 16×20）：底部对齐本格". Candles = tile 476? No — 476 is "Lava lamp"? Actually tile 476 is... Whatever. But vanilla treats those with tileHeight 18/20 and NO tileTop, drawn top-anchored at py, overflowing 2-4px into the tile BELOW. That's the vanilla seam mechanism (overflow covers the gap). Our bottom-alignment pulls it up into the current tile, leaving a gap at top? No—bottom aligning means the sprite occupies py-2..py+16 instead of py..py+18. The vanilla design intentionally overflows downward.

Hmm, but wait: is that right? For tile 3 (plants), vanilla tileHeight=20, tileTop=0 → drawn py..py+20, i.e., extends 4px below into the next tile. Yes that's vanilla behavior for tall grass etc.

OK so class A: our generic path is bottom-anchored instead of top-anchored — a systematic deviation. Only tree/torch/palm paths are top-anchored.

Now class C (vector.X/Y manual offsets) — vanilla :1032-1186 switch:
- 751: +11 X, -8 Y (only anchor frame)
- 752: +8 X (anchor frame)
- 136: -2/+2 X by frameX/18
- 442: +2 X when frameX/22==3
- 726: X-=2; plus slope-based: blockType 3 → X-6,Y+2; 2 → X+6,Y+2; 5 → X-6; 4 → X+6
- 129: ±2 Y (frameY==0 → +2; ==36... actually vector.Y += 2*(frameY==0?1:-1) when frameY<36) and ±2 X for frameY>=36
- 723/724: (0,+2),(0,-2),(-2,0),(+2,0) by frameX/18
- 272: addFrY random 0/90
- 80: cactus variant rectangle.Y += 54/108/162
- 83: texture swap
- 323: vector.X += frameY (palm lean) ✓ ported
- 114: rectangle.Height += 2 (extra tall)
- 72: shroom cap special draw at -22,-26 (before) ✓ ported in drawTreeCell

Our TS: only 323 lean and 72 shroom top and torch dx handled. 726, 129, 723/724, 136, 442, 751/752, 114 not ported.

Class E (addFrX/addFrY frame rewrites): vanilla cases:
- 739/748: addFrY = frame*90
- 719: 288×270 grid anim
- 129: addFrX shuffle (324+ frames)
- 5: frameX += 176*(biome+1) ✓ ported (Tiles_5_N)
- 323: frameY = 22*palmBiome ✓ (palmType) 
- 561: addFrY = frameY/18*4
- 100: addFrY -= 2016*n; addFrX += 72*n
- 530: addFrY += 36*biome
- 485/489/490: wind anim
- 79: addFrY -= 2016*n; addFrX += 144*n
- 90: same
- 18: addFrX -= 2016*n; addFrY += 20*n
- 185/187/649/648: style band reshuffle (1898/1890/1908)
- 617: tileFrameY %= 144; X %= 54
- 270/271/581, 660, 572: per-x frame rotation (addFrX)
- 428: pressed plate addFrX += 18
- 593/594: addFrX = -18/-36; temp frame
- 507/508: addFrY = 90*(...)
- 336/340-344: anim 90
- 406/405: height 16/18 + addFrY *56/*38
- Campfires: 36/252 ✓ ported via campfireYOffset
- default: addFrY = Main.tileFrame[type]*38 ✓ ported via animYOffset (rate table) — but note vanilla addFrY default is 38 for ALL types (even those whose sprite is 18 tall — that's vanilla's quirk; TS animYOffset uses rows*18 presumably). Let me check TileAnim animYOffset quickly to describe. Not strictly required but helpful. Let me peek at TileAnim.

Also class E: TS band-layout reshuffle (ofx/ofy) is their own compat for narrow sheets — analogous to vanilla's 100/79/90/18/185/187/649/648 style-band rewrites but implemented generically.

Let me quickly read TileAnim.ts to confirm animYOffset semantics.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:59:49.045Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/TileAnim.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:49.058Z

**📎 ToolResult**

```
1	// 原版 Main.AnimateTiles（Main.cs:18366-19155）竖直帧动画表：sheet → 每 N tick 推进一帧。
2	// 绘制语义 = TileDrawing.GetTileDrawData addFrY：frameY += frameIdx * pitch。
3	// ★ pitch 有两组（TileDrawing.cs:4568+ 实证）：**默认 38px**（2 格高物体的帧带 2px 额外
4	//   间距——熔炉 17(456/38=12帧)/磨刀站 377(152/38=4帧) 走默认；篝火 215 走专属 36
5	//   （TileDrawing.cs:6124 Campfires 覆盖，帧块 36px 无缝——勿并入默认 38！曾致胶片滚动）；
6	//   特例组 *54（3 格高 3×18）：锯木机 106、固化机 220、自动锻造机 247、300-308 制作台组、
7	//   巫惑/炼金台 354/355、腐变室 499。
8	// 帧数不写死：frames = floor(素材像素高 / pitch)，与 AnimateTiles 的回卷上限互证
9	// （17→12、215→8、306→12、300→7、247→8 全吻合）。
10	// 304 Living Loom 原版无动画（AnimateTiles 无 304 条目，素材 54×54 单帧）。
11	// rate 归一化：原版 counter>N → 每 N+1 tick；counter>=N → 每 N tick。
12	export const TILE_ANIM_RATE: Record<number, number> = {
13	  17: 6,   // 熔炉（12 帧，pitch 38）
14	  106: 5,  // 锯木机（2 帧，pitch 54）
15	  215: 4,  // 篝火（8 帧；pitch 走 campfireYOffset 的 36，本表只管换帧节奏）
16	  220: 5,  // 固化机 Solidifier（4 帧，pitch 54）
17	  247: 5,  // 自动锻造机 Autohammer（8 帧，pitch 54）
18	  300: 5,  // 骨焊机（7 帧）
19	  301: 5,  // 血肉克隆台（8 帧）
20	  302: 5,  // 玻璃窑（4 帧）
21	  303: 5,  // 神庙熔炉（5 帧）
22	  305: 5,  // 天空磨（12 帧）
23	  306: 5,  // 制冰机（12 帧）
24	  307: 5,  // 蒸汽锅炉（2 帧，TEdit 实名）
25	  308: 5,  // 蜂蜜分配机（8 帧，TEdit 实名）
26	  354: 5,  // 巫惑台（8 帧）
27	  355: 5,  // 炼金台
28	  377: 5,  // 磨刀站（4 帧，pitch 38）
29	  499: 5,  // 腐变室 Decay Chamber（8 帧）
30	};
31	
32	/** pitch 54 特例组（其余走默认 38，TileDrawing GetTileDrawData switch 实证） */
33	const PITCH_54 = new Set([106, 219, 220, 228, 231, 243, 247, 300, 301, 302, 303, 305, 306, 307, 308, 354, 355, 499, 592]);
34	
35	/** 篝火族（TileDrawing.cs:6124-6133 Campfires 覆盖）：pitch=36（非默认 38！素材帧块
36	 *  36px 无缝排布——曾按默认 38 导致每帧 +2px 漂移，火焰像胶片滚动）；
37	 *  frameY≥36 的行（熄灭/灰烬变体）恒取静止帧 252 */
38	export function campfireYOffset(frameY: number): number {
39	  return frameY < 36 ? animFrameIdx(215, 324) * 36 : 252;
40	}
41	
42	/** 全局动画时钟（Game 主循环每帧 +1；暂停时冻结） */
43	export const tileAnim = { tick: 0 };
44	
45	/** 该 sheet 当前动画帧索引（无动画表项/单帧返回 0）。
46	 *  sheetHeightPx = 素材总像素高（rows×18）；pitch 54 特例组外默认 38 */
47	export function animFrameIdx(sheet: number, sheetHeightPx: number): number {
48	  const rate = TILE_ANIM_RATE[sheet];
49	  if (!rate) return 0;
50	  const pitch = PITCH_54.has(sheet) ? 54 : 38;
51	  const frames = Math.floor(sheetHeightPx / pitch);
52	  if (frames <= 1) return 0;
53	  return Math.floor(tileAnim.tick / rate) % frames;
54	}
55	
56	/** 绘制时的 frameY 偏移（= 帧索引 × pitch） */
57	export function animYOffset(sheet: number, sheetHeightPx: number): number {
58	  const rate = TILE_ANIM_RATE[sheet];
59	  if (!rate) return 0;
60	  const pitch = PITCH_54.has(sheet) ? 54 : 38;
61	  return animFrameIdx(sheet, sheetHeightPx) * pitch;
62	}
63	

```


---

## 🤖 Assistant · 2026-08-11T15:59:58.886Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have everything I need. Let me also double check a couple of remaining details for class D and E:

- The 1609-1660 rule summary (already read fully).
- Slope slicing loop (ported ✓ at drawSlopedFrame, verified matches num16/num17/num18/num19 semantics; slope numbering: vanilla num=1..4 (slope()); ours slope 1-4 same mapping; check mapping: vanilla case 1: num16=0, num19=i*2 (left-to-right descending?) Actually vanilla slope() 1 = downslope left? Our mapping matches since comments state verified 1:1.)
- HasSlopeFrames (421,422) — special-case draw full 16×16 frame when sloped; ours: drawSlopedFrame for all slopes regardless → deviation for 421/422 (hammers? 421/422 are... probably "Echo Chamber"? Actually 421=??? whatever). Not ported.
- Platforms slope neighbor fill (:1540-1567) — not ported (no platforms in TS? maybe). Not ported.
- The bottom-halfbrick strip :1658-1668 — not ported.
- Also :1653 sliced block — not applicable (no lighting).
- Layering by tileTop sign (:885-896): tileTop<0 → OverTiles layer; top+height<=16 → Tiles; else BehindTiles. TS has wall/tile two layers only; no equivalent. Not ported (affects draw order/seams with walls for tall sprites like trees 20×20 going behind). Worth listing under E or D.

I think I have enough. One more check — does the TS implement 428 (+4)? It has 428: 2 (mismatch, vanilla +4). Confirmed above.

Also `DoNotAdjustDrawPositionBasedOnTileWidth` (711 only) — TS: no X centering at all except torch/tree; so not ported as a set.

Now compose the final report. Keep it a precise list, five classes, with vanilla line numbers and ported/not-ported status with our code locations.

Our code locations:
- drawVanillaCell: ~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts:464-670
- DRAW_Y_OFFSET: VanillaTiler.ts:703-715
- drawTreeCell: VanillaTiler.ts:249-382
- drawSlopedFrame: VanillaTiler.ts:679-700
- halfbrick clip: VanillaTiler.ts:658-661 (and blend path :575-576)
- ChunkCache passes: ChunkCache.ts:172-371 (pass1 wall :186-210, pass2 tiles :215-317, pass3 halfbrick clear :323-328, pass4 trees :334-368)
- SpriteAtlas vframe/vframeAt/vmeta: SpriteAtlas.ts:205-242
- anim: TileAnim.ts

Let me write the final answer in Chinese, organized A-E.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:52.667Z · glm-x-preview-260804

```
# 原版方块绘制接缝/偏移机制审计清单(vs TS 实现)

原版锚点公式(`TileDrawing.cs:1019-1025`):源矩形 `(frameX+addFrX, frameY+addFrY, tileWidth, tileHeight-halfBrickHeight)`,目标 `X = x*16 - (tileWidth-16)/2`(受 `DoNotAdjustDrawPositionBasedOnTileWidth` 关闭,`TileID.cs:253`,仅 711),`Y = y*16 + tileTop + halfBrickHeight`。**顶锚定 + X 居中**,溢出向下。我们通用路径是**底锚定 + 不居中**(`VanillaTiler.ts:641-642` `dy = py + TILE - r.sh`),这是系统性偏差,下文逐项标注。

---

## A. 精灵尺寸 ≠ 16(tileWidth/tileHeight)

原版列表(GetTileDrawData,`TileDrawing.cs:4562-6124`)。锚定语义:**顶锚定、X 居中**,高>16 的向下溢出盖住下格顶。

| tile | 尺寸 | 原版行号 | 我们状态 |
|---|---|---|---|
| 5(树)| 20×20 | :4691-4697 | **已移植** `VanillaTiler.ts:380`(px-2, py, 20×20) |
| 583-589/596/616/634(宝石/装饰/灰烬树)| 20×20 | :4699-4711 | **已移植**(走 drawTreeCell 同一 `:380`) |
| 323(棕榈)| 20×20 + frameY 斜倾 | :4716-4723 | **已移植** `VanillaTiler.ts:287-294` |
| 4(火把)| 20×20 | :4724-4731 | **已移植** `VanillaTiler.ts:650` dxOff=-2(仅 X 居中;Y 走 +4 特判见 B) |
| 726 | 20×20 | :4597-4602 | **未移植**(另有 C 类坡面偏移) |
| 476 | 20×**18** | :4712-4715 | **未移植**(高 18 应顶锚溢 2px;我们若 grid 18 会底锚 -2) |
| 711 | **18**×20(frameX>0 时)| :5000-5008 | **未移植**;且 711 是 `DoNotAdjustDrawPositionBasedOnTileWidth` 唯一成员(:1021-1024)→ 不做 X 居中,我们也未实现该 Set |
| 752 | **36×38** | :4577-4581 | 未移植 |
| 751 | **56×46** | :4582-4589 | 未移植(仅锚点帧,另有 C 类 +11/-8) |
| 698 | **36×44** | :4629-4636 | 未移植(帧重排 frameX/18*38) |
| 227(仙人掌)| **32×38**,tileTop -6/-20 | :5121-5152 | 部分(见 B) |
| 624/700 | 20×**16**,tileTop +2 | :5153-5162 | 未移植 |
| 656/701 | **24×34**,tileTop -16 | :5163-5172 | 未移植 |
| 579 | 20×20,tileTop -2 | :5173-5199 | 未移植尺寸(顶锚 -2 我们表里有 -2,但底锚路径会再 -4) |
| 567 | **26×18** | :5200-5211 | 未移植 |
| 81 | **24×26**,tileTop -8 | :5361-5369 | 尺寸未移植 |
| 184 | **20** 宽,tileTop ±2 分段 | :5282-5292 | 未移植 |
| 442 | 20×20 / 24×20 分段,tileTop -4/-2 | :5704-5720 | 未移植 |
| 82/83/84 | 16×**20**,tileTop -2 | :5047-5056 | 未移植 |
| 324 | 20×20,tileTop -2 | :5057-5065 | 未移植 |
| 3/24/61/71/110/201/637/703 | 16×**20** | :4919-4932 | 未移植(高草/藤蔓类,顶锚溢 4px) |
| 20/590/595、615、16/17/26/…/716(长列表)| 16×**18** | :4933-4977 | 未移植(溢 2px);我们 vmeta grid 16×20/16×18 表走底锚,**方向相反** |
| 405/406 | 16 或 18 高,按帧切换 | :5443-5462, :5509-5523 | 未移植 |
| 33/49/174/372/646 | 16×20 + tileTop -4 | :4887-4894 | 高度未移植 |
| 73/74/113 | 16×**32**,tileTop -12 | :5096-5105 | 未移植 |
| 529 | 16×**32**,tileTop -14 | :4895-4918 | 未移植 |
| 114 | 源高 +2(rectangle.Height += 2)| :1180-1185 | 未移植 |

**结构性结论**:我们的 `dy = py + TILE - r.sh`(`VanillaTiler.ts:642`)对所有 sh>16 的表做底对齐,与原版"顶锚 + 下溢"相反——凡 vmeta grid 高 18/20 的表都会差 2/4px,且失去"溢出盖住下格"的接缝合拢效果。

---

## B. tileTop 下沉(2/4px 插地)

原版全部 case(见上表各行号)。**重要审计发现**:我们的 `DRAW_Y_OFFSET`(`VanillaTiler.ts:703-715`)注释称取自 `TileObjectData.DrawYOffset`,但该字段在原版**只用于放置预览虚影**(`Terraria/TileObject.cs:911`),世界渲染的 Y 偏移唯一来源是 `GetTileDrawData` 的 tileTop。两者大量重合但**不是同一张表**。

我们表内容(VanillaTiler.ts:703-715):`33:-4, 34:-2, 42:-2, 49:-4, 78:2, 81:-8, 82:-1, 85:2, 89:2, 91:-2, 93:2, 95:-2, 100:2, 102:2, 104:2, 105:2, 126:-2, 132:2, 133:2, 134:2, 135:2, 136:2, 139:2, 142:2, 143:2, 174:-4, 186:2, 187:2, 207:2, 210:2, 215:2, 217:2, 218:2, 219:2, 220:2, 227:-6, 228:2, 231:2, 243:2, 244:2, 247:2, 254:2, 270:-2, 271:-2, 275:2, 282:2, 283:2, 285:2, 300-308:2, 324:-2, 349:2, 354:2, 355:2, 372:-4, 377:2, 378:2, 388:-2, 389:-2, 412:2, 428:2, 444:-2, 454:-2, 455:2, 457:2, 463:2, 464:2, 465:-2, 470:2, 475:2, 485:2, 490:2, 491:2, 494:2, 499:2, 505:2, 506:2, 520:2, 521-527:2, 543:2, 547:2, 548:2, 552:2, 560:2, 564:2, 565:2, 567:2, 568:2, 569:2, 570:2, 572:-2, 579:-2, 581:-2, 591:-2, 592:-2, 593:2, 594:2, 597:2, 598:2, 613:2, 614:2, 617:2, 621:2, 622:2`

对照结果:

- **值错误**:`82` 我们 -1 / 原版 **-2**(:5051);`428` 我们 2 / 原版 **+4**(:5698);`567` 我们 +2 / 原版 **-2(仅 frameY==0,否则 0)**(:5203-5206,符号反了)
- **多出(原版 tileTop=0)**:34、42、91、93、95、104、126、270、271、444、454、465、572、581、591、592(其中 270/271/572/581 原版只做 addFrX 帧轮换,:5627-5695,无 Y 偏移)
- **条件缺失(无条件套用)**:`136` 原版仅 frameX==0 时 +2(:4637-4642);`227` 原版 frameX==238 → -6、**否则 -20**(:5124-5131,我们恒 -6);`388/389` 原版仅顶行帧 -2、其余帧 0(:5106-5119);`443` 原版 frameX/36≥2 → -2 否则 +2(:4612-4621)
- **完全缺失**:571(+2)、330-333(+2)、530(+2)、705(+2)、489(+2)、654(+2)、185(+2)、178(frameY≤36 → +2)、184(分段 ±2)、493(+2)、519(+2)、336/340-344(+2,:6109-6117)、52/62/115/205/382/528/636/638(-2,:5069-5082)、646(-4)、83/84(-2)、73/74/113(-12)、529(-14)、656/701(-16)、624/700(+2)、442(-4/-2 分段)、518(**动态**:按 liquid 水位上移,下邻半砖/坡面再补,:4648-4675——原版唯一连续型 tileTop)
- **已正确**:33/49/174/372(-4)、78/85/133/134/210/254/283/378/457/466/520、100/105/139/142/143、186/187、207、215(篝火经 `Sets.Campfires` :6125-6136,我们走 campfireYOffset)、217-220、228/231/243/244/247、275+ 笼族、282/285、300-308、349/354/355、377、412、455、463/464、470/475、485/490/491/494/499、505/506、521-527、543/547/548/552/560、564/565、568-570、579(-2)、593/594/597/598、613/614/617/621/622、89/102
- 火把 4 的 +4(上方实心时)已特判移植 `VanillaTiler.ts:651`

另外注意:我们的 dyOff 只在 style/auto 通用路径生效(`:645`);blend 路径(`:485-587`)提前 return 不查表——对实心块无影响,属正确范围。

---

## C. vector.X/Y 手动偏移(DrawSingleTile 第二段 switch,:1032-1186)

| case | 原版规则 | 行号 | 我们 |
|---|---|---|---|
| 726 | X-=2;base + blockType: 3→(-6,+2)、2→(+6,+2)、5→(-6,0)、4→(+6,0) | :1069-1088 | **未移植**(726 也没进 DRAW_Y_OFFSET,且 A 类 20×20 未做) |
| 129 | Y ±2(frameY==0 → +2,frameY<36 → -2);frameY≥36 → X ±2 | :1104-1121 | 未移植 |
| 723/724 | frameX/18: 0→(0,+2)、1→(0,-2)、2→(-2,0)、3→(+2,0) | :1122-1139 | 未移植 |
| 751 | 锚点帧 X+=11、Y-=8(非锚点帧直接跳过) | :1034-1041 | 未移植 |
| 752 | 锚点帧 X+=8 | :1042-1048 | 未移植 |
| 136 | frameX/18==1 → X-2;==2 → X+2 | :1049-1059 | 未移植 |
| 442 | frameX/22==3 → X+2 | :1060-1068 | 未移植 |
| 80(仙人掌)| 变体行偏移 rectangle.Y += 54/108/162 | :1153-1169 | **已移植**(改用独立贴图 Evil/Crimson/Good_Cactus,`VanillaTiler.ts:392-412`) |
| 323 | vector.X += frameY(棕榈斜倾,u16 回绕)| :1173-1179 | **已移植** `VanillaTiler.ts:282-293` |
| 114 | rectangle.Height += 2 | :1180-1185 | 未移植 |
| 72(蘑菇树)| ShroomCap 60×42 画在 (-22,-26) | :1006-1017 | **已移植** `VanillaTiler.ts:296-315`(底部锚定居中,与原版略异但视觉等价) |

---

## D. 邻接衔接特判

### D1. 邻居是半砖时本格补条(:1609-1652)——**未移植(整体缺失)**

进入条件(全部同时满足):非平台、`!IgnoresNearbyHalfbricksWhenDrawn[type]`、`_tileSolid[type]`、`!NotReallySolid[type]`、本格**非半砖非坡面**、且左右任一邻是半砖。`IgnoresNearbyHalfbricksWhenDrawn`(`TileID.cs:271`)= {380, 476, 235, 138, 664, 137, 484, 421, 422, 711-716};`NotReallySolid`(:355)= {387, 388, 10}。

精确规则:
- **左右都是半砖**(:1611-1620):画①下半 8px 条(源 y+8 高 8,目标 +8);②上半 8px 用**通用衔接帧** `Rect(126, 0, 16, 8)`(相对 addFrX/addFrY);若上邻是同类型且非 bottomSlope → 改用 `Rect(90, 0, 16, 8)`(无顶边版本)
- **仅左邻半砖**(:1621-1635):条宽 `num8 = AllBlocksWithSmoothBordersToResolveHalfBlockIssue[type] ? 2 : 4`(Set 见 `TileID.cs:175`,~150 项);画①下半 8px 条;②主体从 x=num8 起取 `tileWidth-num8` 宽(即砍掉左侧 num8 列);③左上角块 `Rect(144, 0, num8, 8)`;④num8==2 时再补 `Rect(148,0,2,2)` 像素点
- **仅右邻半砖**(:1636-1650):镜像——主体取 `tileWidth-num9` 宽从 0 起;右上角块 `Rect(144+(16-num9), 0, num9, 8)` 画在 x=16-num9;num9==2 再补 `Rect(156,0,2,2)` 于 (14,0)
- 语义:实心块在半砖旁时,用素材表里预制的"斜切衔接角"(X=90/126/144/148/156 处的装饰帧)把 8px 高差抹平。

我们:`VanillaTiler.ts` 无任何邻居半砖查询;`ChunkCache.ts:323-328` 第三遍只对本格 half 做 `clearRect(top 8px)`,方向是"裁自己"而不是原版的"邻格补条"。

### D2. 本格是半砖且下格悬空(:1658-1668)——**未移植**

`halfBrickHeight==8` 且(下格无 / 非实心 / 下格也是半砖)时:非平台先画裁剪后主体再 -4 高,再补**光照底条** `Rect(144, 66, tileWidth, 4)` 于 (0,+4)——半砖底部接缝的暗边。我们只做了裁剪(`VanillaTiler.ts:658-661` 源 y+8 高-8;blend 路径 :575-576 同),无 4px 底条。

### D3. 平台坡面邻接填充(:1540-1567 及 glowmask 版 :1388-1422)——未移植

平台在 slope 1/2 时,若斜下方的对侧格是实心非半砖非反向坡 → 在 (0,+16) 额外画 `Rect(198/324 或 162/306, frameY, 16, 16)` 的背面填充(层 BehindTiles)。

### D4. HasSlopeFrames 特例(:1569-1573,Set = {421,422},`TileID.cs:267`)——未移植

带坡帧的 tile 坡面时直接整帧 16×16,不走切条。我们对所有 slope 一律 `drawSlopedFrame`(`VanillaTiler.ts:663-665`)。

### D5. 坡面切条(:1574-1606)——**已移植**

8 条 2px 竖条 + 底/顶 16×2 补条,逐参数核对一致(`VanillaTiler.ts:679-700`,注释 :673-678 亦 1:1)。注意原版 `DontDrawTileSlopes`(:153,{137,235,388,476,138,664,665,630,631,711-716,723,726})与 `DontDrawTileSliced`(:151)两 Set 我们均未实现——这些 tile 应跳过切条/切片路径。

### D6. 按 tileTop 分层(:885-896)——未移植

tileTop<0 → OverTiles 层(画在其他 tile 之上);tileTop+tileHeight≤16 → Tiles 层;否则 BehindTiles 层(画到**其他 tile 背后**——树干 20×20 下溢 4px 即靠此不遮下格)。我们只有 wall/tile 两层(`ChunkCache.ts:172-177`),树干溢出靠"后画覆盖"近似。

### D7. DrawSingleTile_SlicedBlock(:1653-1657, :3545-3634)——不适用

实心块 9 宫格逐块取光。我们无光照系统,可豁免;但它是 :1609 半砖补条的**前置分支**(实心非半砖块优先走这里),移植 D1 时需注意条件互斥顺序。

---

## E. 其他接缝相关(addFrX/addFrY 帧重排)

| tile | 原版规则 | 行号 | 我们 |
|---|---|---|---|
| 默认 | addFrY = tileFrame[type]*38 | :4568 | **已移植** `TileAnim.ts:47-62`(38 默认 + PITCH_54 特例组) |
| 215 篝火族 | pitch 36 / 熄灭行恒 252 | :6125-6136 | **已移植** `TileAnim.ts:38-40`、`ChunkCache.ts:235-239` |
| 106/220/247/300-308/354/355/499 | pitch 54 | :5374, :5397, :5588 等 | **已移植** `TileAnim.ts:33` PITCH_54 |
| 5 | frameX += 176*(biome+1) | :4695-4696 | **已移植**(`Tiles_5_N` 变体贴图,`VanillaTiler.ts:360-373`) |
| 323 | frameY = 22*palmBiome | :4720-4721 | **已移植**(改用 Tree_Tops_15 沙型行,`VanillaTiler.ts:266-278`) |
| 739/748 | addFrY = frame*90 | :4590-4596 | 未移植 |
| 719 | 288×270 网格动画 | :4603-4611 | 未移植 |
| 129 | addFrX = ((f-324)/18 + frame)%6 - n)*18 | :4682-4690 | 未移植 |
| 100 | addFrY -= 2016*n;addFrX += 72*n(样式带重排)| :4749-4756 | **替代实现**:通用分带重排 `VanillaTiler.ts:614-634`(按 imgW/带宽换带) |
| 79 / 90 / 18 | 同类带重排(144/20 步)| :4978-4999 | 同上替代 |
| 530 | addFrY += 36*biome(corrupt/crimson/hallow)| :4757-4776 | 未移植 |
| 485/489/490/493 | 风力摆动帧 | :4780-4886, :5300-5332 | 未移植 |
| 185/187/649/648 | 带重排(1908/1890/1898)| :5227-5251, :5256-5275 | 通用分带替代(见上) |
| 617 | tileFrameY %= 144;X %= 54 | :5351-5355 | 未移植 |
| 270/271/581、660、572 | 按 x%2/%3/%4 轮换 addFrX | :5627-5695 | 未移植 |
| 428 | 被踩下时 addFrX += 18 | :5697-5703 | 未移植 |
| 593/594 | addFrX = -18/-36 + 临时帧 | :5536-5579 | 未移植 |
| 507/508 | addFrY = 90*((counter+x*11+y*27)%160/20) | :6101-6108 | 未移植 |
| 336/340-344 | addFrY = frame*90 | :6109-6117 | 未移植 |
| 405/406 | addFrY = *38/*56 + 高度切换 | :5443-5462, :5509-5523 | 未移植 |
| 452/455/454/453/456/455 等杂项帧偏移 | :5463-5508 | 未移植 |
| 349/441/468 | Animation.GetTemporaryFrame | :5407-5432 | 未移植 |
| X 翻转(x%2==0 → FlipHorizontally)| 3/24/61/71/110/201/637/703、20/590/595、615、82-84、324、52 族、73/74/113、227、624/700、656/701、567、529、571、270 族 等 | 各 case | **未移植**(无 SpriteEffects 等价物;镜像帧会产生左右接缝错位) |

---

## 优先级建议(按接缝可见度)

1. **D1 邻居半砖补条 + D2 半砖底条**——半砖旁实心块的 8px 错位是最显眼的缺失,且需引 `IgnoresNearbyHalfbricksWhenDrawn`/`AllBlocksWithSmoothBordersToResolveHalfBlockIssue`/`NotReallySolid` 三 Set(`TileID.cs:271/175/355`)与素材 X=90/126/144/148/156 装饰帧。
2. **B 类表纠正**——`DRAW_Y_OFFSET` 换成 GetTileDrawData tileTop 权威表;至少先修 `82(-1→-2)`、`428(2→4)`、`567(+2→-2 条件)`、`227(补 -20 分支)`、`388/389(条件化)`,并补 52/62/115/205/382/528/636/638(-2)、73/74/113(-12)、529(-14)。
3. **A 类锚定方向**——通用路径改顶锚 + X 居中,替换 `VanillaTiler.ts:642` 的底锚;补 726/476/711/82-84/324/442/184/624/656 等尺寸 case。
4. **E 类 X 翻转**——canvas 可用 `translate+scale(-1,1)` 实现,影响面大(约 30 组)。
5. C 类 726/129/723/724 属小众机关,可后置。
```
