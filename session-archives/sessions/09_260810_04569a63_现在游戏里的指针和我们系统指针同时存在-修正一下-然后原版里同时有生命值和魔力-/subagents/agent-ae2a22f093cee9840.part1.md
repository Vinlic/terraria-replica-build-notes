# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T02:32:06.976Z

```
Read the file ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs and extract ALL ambient/per-tile particle emission blocks. Specifically look at the method that runs per visible tile (contains many `typeCache == N` or `tileCache.type == N` checks followed by Dust.NewDust / Dust.NewDustDirect / Dust.NewDustPerfect with probability gates like _rand.Next(N)).

Search terms: "Dust.NewDust", "_rand.Next", "typeCache ==", "tileCache.type ==" in that file.

Produce a complete table of every tile type that emits ambient particles: tile id, dust id(s), probability (rand.Next(N)==0 or <2 etc.), position/velocity specifics if notable (e.g. rises up, drifts left), and frameX conditions if any (e.g. only frameX==0 lit state). Include the line numbers of each block.

Known ones I already have (skip detail for these but list line numbers): torch (type 4), candle 33, water candle 49, peace candle 372, lava lamps/volcano 593/594, tiki torch etc. I want the FULL list including: 51 cobweb?, 229 honey?, any grass/flowers/mushroom glow particles, demon altar, crystallized things, fog machines, sprinklers, bubbles (bubble tile), smoke blocks, fireplaces, chimneys, brandy/furnace smoke, torch god's, gem sparkles, biome-specific (coral, sea oats? that's grass), etc.

Also check ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs for tile ambient particles if there's a legacy list (search "Dust.NewDust" near tile drawing loops, but only list entries NOT already in TileDrawing).

Return a markdown table sorted by tile id, columns: tileId | tileName (if inferable) | dustId | probability | notes/line numbers. Be exhaustive — do not truncate the list.
```

---

## 📎 Attachment · skill_listing · 2026-08-11T02:32:06.980Z

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

## 🤖 Assistant · 2026-08-11T02:32:14.841Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to read a specific file and extract ambient particle emission blocks. Let me start by finding the relevant sections in the TileDrawing.cs file.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:32:15.303Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs && grep -n \"Dust.NewDust\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "description": "Count lines and find Dust.NewDust occurrences"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:15.390Z

**📎 ToolResult**

```
    9831 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs
921:				int num = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 60, 0f, 0f, 100, default(Color), 0.3f);
940:				int num2 = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 204, 0f, 0f, 150, default(Color), 0.3f);
966:					int num3 = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
6844:				int num5 = Dust.NewDust(new Vector2(i * 16, j * 16 - 2), 1, 1, 58, 0f, 0f, 150);
6895:			int num6 = Dust.NewDust(new Vector2(i * 16 + 2, j * 16 - 4), 4, 8, 31, 0f, 0f, 100);
6911:			int num7 = Dust.NewDust(new Vector2(i * 16 + 2, j * 16 + 4), 4, 8, 31, 0f, 0f, 100);
7073:			int num11 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 168);
7105:						Dust dust2 = Dust.NewDustDirect(new Vector2(i * 16 + 4, j * 16), 36, 8, 16);
7119:						Dust dust3 = Dust.NewDustDirect(new Vector2(i * 16, j * 16), 8, 8, 274);
7139:						Dust dust4 = Dust.NewDustDirect(new Vector2(i * 16, j * 16 + 8), 16, 12, 43);
7154:				int num13 = Dust.NewDust(new Vector2(i * 16 + 2, j * 16 + 6), 8, 4, 153);
7171:						int num17 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 + 4), 8, 8, 58, 0f, 0f, 150);
7184:						int num19 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16), 8, 8, 59, 0f, 0f, 100);
7196:						int num16 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16), 8, 8, 57, 0f, 0f, 100);
7208:						int num15 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 + 2), 4, 4, 242, 0f, 0f, 100);
7227:				22 => Dust.NewDust(new Vector2(i * 16 + 6, j * 16), 4, 4, num21, 0f, 0f, 100), 
7228:				44 => Dust.NewDust(new Vector2(i * 16 + 2, j * 16), 4, 4, num21, 0f, 0f, 100), 
7229:				_ => Dust.NewDust(new Vector2(i * 16 + 4, j * 16), 4, 4, num21, 0f, 0f, 100), 
7276:					int num25 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 + 2), 4, 4, num24, 0f, 0f, 100);
7322:					num28 = Dust.NewDust(position5, 4, 4, num27, 0f, 0f, 100);
7334:			int num29 = Dust.NewDust(new Vector2(i * 16 + 12, j * 16 + 2), 4, 4, 6, 0f, 0f, 100);
7344:			int num30 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 - 4), 4, 4, 172, 0f, 0f, 100);
7359:			int num31 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 - 4), 4, 4, 242, 0f, 0f, 100);
7417:					int num35 = Dust.NewDust(new Vector2(i * 16, j * 16 + 2), 14, 6, num34, 0f, 0f, 100);
7437:			Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7441:			Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7445:			Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7449:			Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7455:				int num36 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 5, 0f, 0f, 100);
7461:				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14, 0f, 0f, 100);
7468:				int num37 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 5, 0f, 0f, 100);
7475:				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14, 0f, 0f, 100);
7480:			Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 41, 0f, 0f, 250, default(Color), 0.8f);
7486:				int num38 = Dust.NewDust(new Vector2(i * 16 - 4, j * 16 - 6), 8, 6, 6, 0f, 0f, 100);
7497:				int num39 = Dust.NewDust(new Vector2(i * 16 - 4, j * 16 - 6), 24, 10, 6, 0f, 0f, 100);
7506:			int num40 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 6, 0f, 0f, 0, default(Color), _rand.Next(3));
7514:			int num41 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 6, 0f, 0f, 0, default(Color), _rand.Next(3));
7525:				int num42 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 44, 0f, 0f, 250, default(Color), 0.4f);
7565:					int num46 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, newColor, 0.5f);
7596:				int num44 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, newColor, 0.5f);
7644:			int num47 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, newColor, 0.5f);
7663:				int num49 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, white, scale2);
8655:				int num = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 60, 0f, 0f, 100, default(Color), 0.3f);
8674:				int num2 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 204, 0f, 0f, 150, default(Color), 0.3f);
8702:				int num3 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
9274:						int num7 = Dust.NewDust(new Vector2(x * 16, i * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
9784:			int num = Dust.NewDust(new Vector2(i * 16, j * 16 - 4), 16, 16, 19, 0f, 0f, 160, default(Color), 0.1f);
9792:			Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 41, 0f, 0f, 250, default(Color), 0.8f);
9798:				int num2 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14, 0f, 0f, 100, default(Color), 0.2f);
9803:				int num3 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 27, 0f, 0f, 100);
9810:			int num4 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 8, 16);
9821:			int num5 = Dust.NewDust(new Vector2(i * 16, j * 16 - 6), 16, 16, 6, 0f, 0f, 0, default(Color), 1.5f);
9827:			int num6 = Dust.NewDust(newColor: new Color(50, 255, 255, 255), Position: new Vector2(i * 16, j * 16), Width: 16, Height: 16, Type: 43, SpeedX: 0f, SpeedY: 0f, Alpha: 254, Scale: 0.5f);

```


---

## 🤖 Assistant · 2026-08-11T02:32:15.717Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"typeCache ==\\|tileCache.type ==\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "description": "Find typeCache comparisons"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:15.808Z

**📎 ToolResult**

```
880:		if (tileDrawInfo.tileCache.liquid > 0 && tileDrawInfo.tileCache.type == 518)
1006:		if (tileDrawInfo.typeCache == 72 && tileDrawInfo.tileFrameX >= 36)
1187:		if (tileDrawInfo.typeCache == 314)
1191:		else if (tileDrawInfo.typeCache == 171)
1366:			if (tileDrawInfo.typeCache == 412)
1534:		if (drawData.typeCache == 380 || TileID.Sets.Platforms[drawData.typeCache])
1702:		else if (drawData.typeCache == 711)
2712:		if (drawData.typeCache == 548 && drawData.tileFrameX / 54 > 6)
2716:		if (drawData.typeCache == 613)
2720:		if (drawData.typeCache == 614)
2724:		if (drawData.typeCache == 593)
2728:		if (drawData.typeCache == 594)
2732:		if (drawData.typeCache == 215 && drawData.tileFrameY < 36)
2750:		if (drawData.typeCache == 85)
2777:		if (drawData.typeCache == 356 && Main.sundialCooldown == 0)
2792:		if (drawData.typeCache == 663 && Main.moondialCooldown == 0)
2799:		if (drawData.typeCache == 286)
2803:		if (drawData.typeCache == 582)
2807:		if (drawData.typeCache == 391)
2811:		if (drawData.typeCache == 619)
2815:		if (drawData.typeCache == 270)
2819:		if (drawData.typeCache == 271)
2823:		if (drawData.typeCache == 581)
2827:		if (drawData.typeCache == 316 || drawData.typeCache == 317 || drawData.typeCache == 318)
2831:		if (drawData.typeCache == 149 && drawData.tileFrameX < 54)
2835:		if (drawData.typeCache == 300 || drawData.typeCache == 302 || drawData.typeCache == 303 || drawData.typeCache == 306)
2838:			if (drawData.typeCache == 302)
2842:			if (drawData.typeCache == 303)
2846:			if (drawData.typeCache == 306)
3462:				if (drawData.tileCache.type == 4)
3477:				if (drawData.tileCache.type == 646)
3491:		if (drawData.typeCache == 144)
3495:		if (drawData.typeCache == 237)
3915:		if (tileCache.type == 379 && tileCache.liquid > 0)
3919:		if (tileCache.type == 546 && tileCache.liquid > 0)
4370:			if (drawData.typeCache == 21 && (num3 == 48 || num3 == 49))
4486:		bool flag = false || typeCache == 135 || typeCache == 137 || TileID.Sets.Boulders[typeCache] || typeCache == 141 || typeCache == 210 || typeCache == 442 || typeCache == 443 || typeCache == 444 || typeCache == 411 || typeCache == 485 || typeCache == 85 || typeCache == 654 || (typeCache == 314 && Minecart.IsPressurePlate(tileCache));
4487:		flag |= Main.getGoodWorld && typeCache == 230;
4488:		flag |= Main.dontStarveWorld && typeCache == 80;
4491:			flag = flag || (typeCache >= 0 && TileID.Sets.TouchDamageImmediate[typeCache] > 0) || typeCache == 483 || typeCache == 482 || typeCache == 481 || typeCache == 51 || typeCache == 229;
4498:				flag = flag || typeCache == 162;
5969:			if (typeCache == 360 || typeCache == 580 || typeCache == 620)
6351:			if (typeCache == 15)
6800:		if (typeCache == 718 && !Main.dayTime && _rand.Next(3) == 0 && !WorldGen.SolidTile3(i, j - 1))
6860:		if (typeCache == 244 && tileFrameX == 18 && tileFrameY == 18 && _rand.Next(2) == 0)
6883:		if (typeCache == 565 && tileFrameX == 0 && tileFrameY == 18 && _rand.Next(3) == 0)
6893:		if (typeCache == 215 && tileFrameY < 36 && _rand.Next(3) == 0 && tileFrameY == 0)
6909:		if (typeCache == 592 && tileFrameY == 18 && _rand.Next(3) == 0)
6925:		else if (typeCache == 406 && tileFrameY == 54 && tileFrameX == 0 && _rand.Next(3) == 0)
6947:		else if (typeCache == 452 && tileFrameY == 0 && tileFrameX == 0 && _rand.Next(3) == 0)
6962:		if (typeCache == 192 && _rand.Next(leafFrequency) == 0)
6966:		if (typeCache == 384 && _rand.Next(leafFrequency) == 0)
6970:		if ((typeCache == 666 || typeCache == 712) && tileCache.liquid <= 0 && j - 1 > 0 && _rand.Next(100) == 0 && !WorldGen.ActiveAndWalkableTile(i, j - 1) && !WorldGen.AnyLiquidAt(i, j - 1))
6977:		if (typeCache == 711 && tileFrameX == 0 && tileFrameY == 0)
7071:		if (typeCache == 238 && _rand.Next(10) == 0)
7077:		if (typeCache == 139)
7097:		else if (typeCache == 463)
7131:		else if (typeCache == 497)
7150:		else if (typeCache == 165 && tileFrameX >= 162 && tileFrameX <= 214 && tileFrameY == 72)
7161:		else if (typeCache == 42 && tileFrameX == 0)
7220:		if (typeCache == 4 && _rand.Next(40) == 0 && tileFrameX < 66)
7243:		if (typeCache == 93 && _rand.Next(40) == 0 && tileFrameX == 0)
7286:		if (typeCache == 100 && _rand.Next(40) == 0 && tileFrameX < 36)
7332:		if (typeCache == 98 && _rand.Next(40) == 0 && tileFrameY == 0 && tileFrameX == 0)
7342:		if (typeCache == 49 && tileFrameX == 0 && _rand.Next(2) == 0)
7357:		if (typeCache == 372 && tileFrameX == 0 && _rand.Next(2) == 0)
7372:		if (typeCache == 646 && tileFrameX == 0)
7376:		if (typeCache == 34 && _rand.Next(40) == 0 && tileFrameX % 108 < 54)
7427:		if (typeCache == 83)
7435:		if (typeCache == 22 && _rand.Next(400) == 0)
7439:		else if ((typeCache == 23 || typeCache == 24 || typeCache == 32) && _rand.Next(500) == 0)
7443:		else if (typeCache == 25 && _rand.Next(700) == 0)
7447:		else if (typeCache == 112 && _rand.Next(700) == 0)
7451:		else if ((typeCache == 31 || typeCache == 696) && _rand.Next(20) == 0)
7464:		else if ((typeCache == 26 || typeCache == 695) && _rand.Next(20) == 0)
7478:		else if ((typeCache == 71 || typeCache == 72) && tileCache.color() == 0 && _rand.Next(500) == 0)
7482:		else if ((typeCache == 17 || typeCache == 77 || typeCache == 133) && _rand.Next(40) == 0)
7493:		else if (typeCache == 405 && _rand.Next(20) == 0)
7504:		else if (typeCache == 37 && _rand.Next(250) == 0)
7512:		else if ((typeCache == 58 || typeCache == 76 || typeCache == 684) && _rand.Next(250) == 0)
7521:		else if (typeCache == 61 || typeCache == 703)
7545:			if (_rand.Next(Main.tileShine[typeCache]) >= num43 || ((typeCache == 21 || typeCache == 441) && (tileFrameX < 36 || tileFrameX >= 180) && (tileFrameX < 396 || tileFrameX > 409)) || ((typeCache == 467 || typeCache == 468) && (tileFrameX < 144 || tileFrameX >= 180)))
7604:			if (typeCache == 64)
7608:			if (typeCache == 65)
7612:			if (typeCache == 66)
7616:			if (typeCache == 67)
7620:			if (typeCache == 68)
7624:			if (typeCache == 566)
7628:			if (typeCache == 12 || typeCache == 665)
7632:			if (typeCache == 639)
7636:			if (typeCache == 204)
7640:			if (typeCache == 211)
7768:		if (typeCache == 374)
7772:		if (typeCache == 375)
7776:		if (typeCache == 461)
7792:		if (typeCache == 709)
7838:		if (tileCache.type == 227 && (tileCache.frameX == 204 || tileCache.frameX == 238 || tileCache.frameX == 408 || tileCache.frameX == 442 || tileCache.frameX == 476))

```


---

## 🤖 Assistant · 2026-08-11T02:32:17.921Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The ambient particle method seems to span roughly lines 6800-7700. Let me read that whole region carefully. Also lines 8655-8702 and 9274 and 9784-9831 may be other methods (pre-hm draw / specific things). Let me read the method around 6750-7720 in full.

Plan mode is active but this is a read-only task anyway. I should do the reads and produce the report. Let me read in chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:32:18.357Z · glm-x-preview-260804

```
The ambient particle method appears to span roughly lines 6780–7720. Let me read that whole region, plus the other Dust blocks, in parallel chunks.
```


---

## 🤖 Assistant · 2026-08-11T02:32:18.633Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 450,
 "offset": 6780
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:18.663Z

**📎 ToolResult**

```
6780				break;
6781			case 481:
6782			case 482:
6783			case 483:
6784			{
6785				float num = 1f + (float)Math.Sin(Main.GlobalTimeWrappedHourly / 1.5f * (MathF.PI * 2f)) * 0.15f;
6786				byte a = tileLight.A;
6787				tileLight *= num;
6788				tileLight.A = a;
6789				break;
6790			}
6791			}
6792			return tileLight;
6793		}
6794	
6795		private void DrawTiles_EmitParticles(int j, int i, Tile tileCache, ushort typeCache, short tileFrameX, short tileFrameY, Color tileLight)
6796		{
6797			bool flag = IsVisible(tileCache);
6798			int leafFrequency = _leafFrequency;
6799			leafFrequency /= 4;
6800			if (typeCache == 718 && !Main.dayTime && _rand.Next(3) == 0 && !WorldGen.SolidTile3(i, j - 1))
6801			{
6802				if (Main.player[Main.myPlayer].RollLuck(100) == 0)
6803				{
6804					int num = Gore.NewGore(new Vector2(i * 16 + _rand.Next(16), j * 16 - 12), default(Vector2), 16);
6805					Main.gore[num].scale *= _rand.NextFloat() * 0.5f + 0.75f;
6806					Main.gore[num].velocity *= 0.2f;
6807					Main.gore[num].velocity.Y -= (float)_rand.Next(5, 31) * 0.1f;
6808					if (_rand.Next(5) == 0)
6809					{
6810						Main.gore[num].velocity.Y -= (float)_rand.Next(5, 41) * 0.1f;
6811					}
6812					if (_rand.Next(3) == 0)
6813					{
6814						Main.gore[num].velocity *= 0.5f;
6815					}
6816					Main.gore[num].velocity /= Main.gore[num].scale;
6817					int num2 = Gore.NewGore(new Vector2(i * 16, j * 16), default(Vector2), 16);
6818					Main.gore[num2].scale = Main.gore[num].scale;
6819					Main.gore[num2].position = Main.gore[num].position;
6820					Main.gore[num2].velocity = Main.gore[num].velocity;
6821				}
6822				if (Main.player[Main.myPlayer].RollLuck(60) == 0)
6823				{
6824					int num3 = Gore.NewGore(new Vector2(i * 16 + _rand.Next(16), j * 16 - 12), default(Vector2), 17);
6825					Main.gore[num3].scale *= _rand.NextFloat() * 0.5f + 0.75f;
6826					Main.gore[num3].velocity *= 0.2f;
6827					Main.gore[num3].velocity.Y -= (float)_rand.Next(5, 41) * 0.1f;
6828					if (_rand.Next(5) == 0)
6829					{
6830						Main.gore[num3].velocity.Y -= (float)_rand.Next(5, 51) * 0.1f;
6831					}
6832					if (_rand.Next(3) == 0)
6833					{
6834						Main.gore[num3].velocity *= 0.5f;
6835					}
6836					Main.gore[num3].velocity /= Main.gore[num3].scale;
6837					int num4 = Gore.NewGore(new Vector2(i * 16, j * 16), default(Vector2), 17);
6838					Main.gore[num4].scale = Main.gore[num3].scale;
6839					Main.gore[num4].position = Main.gore[num3].position;
6840					Main.gore[num4].velocity = Main.gore[num3].velocity;
6841				}
6842				if (Main.player[Main.myPlayer].RollLuck(30) == 0)
6843				{
6844					int num5 = Dust.NewDust(new Vector2(i * 16, j * 16 - 2), 1, 1, 58, 0f, 0f, 150);
6845					Main.dust[num5].scale *= _rand.NextFloat() * 0.5f + 0.75f;
6846					Main.dust[num5].color = new Color(255, 255, 255, 0);
6847					Main.dust[num5].velocity *= 0.2f;
6848					Main.dust[num5].velocity.Y -= (float)_rand.Next(5, 51) * 0.1f;
6849					if (_rand.Next(5) == 0)
6850					{
6851						Main.dust[num5].velocity.Y -= (float)_rand.Next(5, 61) * 0.1f;
6852					}
6853					if (_rand.Next(3) == 0)
6854					{
6855						Main.dust[num5].velocity *= 0.5f;
6856					}
6857					Main.dust[num5].velocity /= Main.dust[num5].scale;
6858				}
6859			}
6860			if (typeCache == 244 && tileFrameX == 18 && tileFrameY == 18 && _rand.Next(2) == 0)
6861			{
6862				if (_rand.Next(500) == 0)
6863				{
6864					Gore.NewGore(new Vector2(i * 16 + 8, j * 16 + 8), default(Vector2), 415, (float)_rand.Next(51, 101) * 0.01f);
6865				}
6866				else if (_rand.Next(250) == 0)
6867				{
6868					Gore.NewGore(new Vector2(i * 16 + 8, j * 16 + 8), default(Vector2), 414, (float)_rand.Next(51, 101) * 0.01f);
6869				}
6870				else if (_rand.Next(80) == 0)
6871				{
6872					Gore.NewGore(new Vector2(i * 16 + 8, j * 16 + 8), default(Vector2), 413, (float)_rand.Next(51, 101) * 0.01f);
6873				}
6874				else if (_rand.Next(10) == 0)
6875				{
6876					Gore.NewGore(new Vector2(i * 16 + 8, j * 16 + 8), default(Vector2), 412, (float)_rand.Next(51, 101) * 0.01f);
6877				}
6878				else if (_rand.Next(3) == 0)
6879				{
6880					Gore.NewGore(new Vector2(i * 16 + 8, j * 16 + 8), default(Vector2), 411, (float)_rand.Next(51, 101) * 0.01f);
6881				}
6882			}
6883			if (typeCache == 565 && tileFrameX == 0 && tileFrameY == 18 && _rand.Next(3) == 0)
6884			{
6885				Vector2 vector = new Point(i, j).ToWorldCoordinates();
6886				int type = 1202;
6887				float scale = 8f + Main.rand.NextFloat() * 1.6f;
6888				Vector2 position = vector + new Vector2(0f, -18f);
6889				Vector2 velocity = Main.rand.NextVector2Circular(0.7f, 0.25f) * 0.4f + Main.rand.NextVector2CircularEdge(1f, 0.4f) * 0.1f;
6890				velocity *= 4f;
6891				Gore.NewGorePerfect(position, velocity, type, scale);
6892			}
6893			if (typeCache == 215 && tileFrameY < 36 && _rand.Next(3) == 0 && tileFrameY == 0)
6894			{
6895				int num6 = Dust.NewDust(new Vector2(i * 16 + 2, j * 16 - 4), 4, 8, 31, 0f, 0f, 100);
6896				if (tileFrameX == 0)
6897				{
6898					_dust[num6].position.X += _rand.Next(8);
6899				}
6900				if (tileFrameX == 36)
6901				{
6902					_dust[num6].position.X -= _rand.Next(8);
6903				}
6904				_dust[num6].alpha += _rand.Next(100);
6905				_dust[num6].velocity *= 0.2f;
6906				_dust[num6].velocity.Y -= 0.5f + (float)_rand.Next(10) * 0.1f;
6907				_dust[num6].fadeIn = 0.5f + (float)_rand.Next(10) * 0.1f;
6908			}
6909			if (typeCache == 592 && tileFrameY == 18 && _rand.Next(3) == 0)
6910			{
6911				int num7 = Dust.NewDust(new Vector2(i * 16 + 2, j * 16 + 4), 4, 8, 31, 0f, 0f, 100);
6912				if (tileFrameX == 0)
6913				{
6914					_dust[num7].position.X += _rand.Next(8);
6915				}
6916				if (tileFrameX == 36)
6917				{
6918					_dust[num7].position.X -= _rand.Next(8);
6919				}
6920				_dust[num7].alpha += _rand.Next(100);
6921				_dust[num7].velocity *= 0.2f;
6922				_dust[num7].velocity.Y -= 0.5f + (float)_rand.Next(10) * 0.1f;
6923				_dust[num7].fadeIn = 0.5f + (float)_rand.Next(10) * 0.1f;
6924			}
6925			else if (typeCache == 406 && tileFrameY == 54 && tileFrameX == 0 && _rand.Next(3) == 0)
6926			{
6927				Vector2 position2 = new Vector2(i * 16 + 16, j * 16 + 8);
6928				Vector2 velocity2 = new Vector2(0f, 0f);
6929				if (Main.WindForVisuals < 0f)
6930				{
6931					velocity2.X = 0f - Main.WindForVisuals;
6932				}
6933				int type2 = _rand.Next(825, 828);
6934				if (_rand.Next(4) == 0)
6935				{
6936					Gore.NewGore(position2, velocity2, type2, _rand.NextFloat() * 0.2f + 0.2f);
6937				}
6938				else if (_rand.Next(2) == 0)
6939				{
6940					Gore.NewGore(position2, velocity2, type2, _rand.NextFloat() * 0.3f + 0.3f);
6941				}
6942				else
6943				{
6944					Gore.NewGore(position2, velocity2, type2, _rand.NextFloat() * 0.4f + 0.4f);
6945				}
6946			}
6947			else if (typeCache == 452 && tileFrameY == 0 && tileFrameX == 0 && _rand.Next(3) == 0)
6948			{
6949				Vector2 position3 = new Vector2(i * 16 + 16, j * 16 + 8);
6950				Vector2 velocity3 = new Vector2(0f, 0f);
6951				if (Main.WindForVisuals < 0f)
6952				{
6953					velocity3.X = 0f - Main.WindForVisuals;
6954				}
6955				int num8 = Main.tileFrame[typeCache];
6956				int type3 = 907 + num8 / 5;
6957				if (_rand.Next(2) == 0)
6958				{
6959					Gore.NewGore(position3, velocity3, type3, _rand.NextFloat() * 0.4f + 0.4f);
6960				}
6961			}
6962			if (typeCache == 192 && _rand.Next(leafFrequency) == 0)
6963			{
6964				EmitLivingTreeLeaf(i, j, 910);
6965			}
6966			if (typeCache == 384 && _rand.Next(leafFrequency) == 0)
6967			{
6968				EmitLivingTreeLeaf(i, j, 914);
6969			}
6970			if ((typeCache == 666 || typeCache == 712) && tileCache.liquid <= 0 && j - 1 > 0 && _rand.Next(100) == 0 && !WorldGen.ActiveAndWalkableTile(i, j - 1) && !WorldGen.AnyLiquidAt(i, j - 1))
6971			{
6972				ParticleOrchestrator.RequestParticleSpawn(clientOnly: true, ParticleOrchestraType.PooFly, new ParticleOrchestraSettings
6973				{
6974					PositionInWorld = new Vector2(i * 16 + 8, j * 16 - 8)
6975				});
6976			}
6977			if (typeCache == 711 && tileFrameX == 0 && tileFrameY == 0)
6978			{
6979				if (_rand.Next(45) == 0)
6980				{
6981					ParticleOrchestrator.RequestParticleSpawn(clientOnly: true, ParticleOrchestraType.RainbowBoulder3, new ParticleOrchestraSettings
6982					{
6983						PositionInWorld = new Vector2(i * 16 + 16, j * 16 + 16)
6984					});
6985				}
6986				if (_rand.Next(3) != 0)
6987				{
6988					ParticleOrchestrator.RequestParticleSpawn(clientOnly: true, ParticleOrchestraType.RainbowBoulder2, new ParticleOrchestraSettings
6989					{
6990						PositionInWorld = new Vector2(i * 16 + 16, j * 16 + 16) + _rand.NextVector2Circular(16f, 16f),
6991						MovementVector = _rand.NextVector2Circular(1f, 0.5f) * 0.5f
6992					});
6993				}
6994			}
6995			if (TileID.Sets.SpawnsNatureFlies[typeCache] && tileCache.liquid <= 0)
6996			{
6997				float lerpValue = Utils.GetLerpValue(0.08f, 0.18f, Math.Abs(Main.WindForVisuals), clamped: true);
6998				lerpValue += 0.3f;
6999				if (_rand.NextFloat() < lerpValue)
7000				{
7001					bool flag2 = _rand.Next(600) == 0;
7002					if (!flag2)
7003					{
7004						_windGrid.GetWindTime(i, j, 8, out var windTimeLeft, out var directionX, out directionX);
7005						flag2 = windTimeLeft > 0 && _rand.Next(48) == 0;
7006					}
7007					if (flag2)
7008					{
7009						ParticleOrchestrator.RequestParticleSpawn(clientOnly: true, ParticleOrchestraType.NatureFly, new ParticleOrchestraSettings
7010						{
7011							PositionInWorld = new Vector2(i * 16 + 8, j * 16)
7012						});
7013					}
7014				}
7015			}
7016			if (_rand.Next(1200) == 0)
7017			{
7018				bool flag3 = j + 1 < 0;
7019				bool flag4 = false;
7020				int num9 = 3;
7021				if ((double)j < Main.worldSurface)
7022				{
7023					if (_rand.Next(10) != 0)
7024					{
7025						flag3 = true;
7026					}
7027					else
7028					{
7029						num9--;
7030						flag4 = true;
7031					}
7032				}
7033				if (!TileID.Sets.MakesRubbleDust[typeCache])
7034				{
7035					flag3 = true;
7036				}
7037				if (!flag3 && WorldGen.ActiveAndWalkableTile(i, j + 1))
7038				{
7039					flag3 = true;
7040				}
7041				if (!flag3 && !WallID.Sets.AllowsWind[Main.tile[i, j].wall])
7042				{
7043					if (_rand.Next(2) == 0)
7044					{
7045						flag3 = true;
7046					}
7047					else
7048					{
7049						num9--;
7050					}
7051				}
7052				if (!flag3)
7053				{
7054					for (int k = 0; k < num9; k++)
7055					{
7056						int num10 = WorldGen.KillTile_MakeTileDust(i, j, tileCache);
7057						Dust dust = Main.dust[num10];
7058						dust.position.Y += 8f;
7059						dust.velocity *= 0.1f;
7060						if (flag4)
7061						{
7062							dust.scale -= 0.3f;
7063						}
7064					}
7065				}
7066			}
7067			if (!flag)
7068			{
7069				return;
7070			}
7071			if (typeCache == 238 && _rand.Next(10) == 0)
7072			{
7073				int num11 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 168);
7074				_dust[num11].noGravity = true;
7075				_dust[num11].alpha = 200;
7076			}
7077			if (typeCache == 139)
7078			{
7079				if (tileCache.frameX == 36 && tileCache.frameY % 36 == 0 && (int)Main.timeForVisualEffects % 7 == 0 && _rand.Next(3) == 0)
7080				{
7081					int num12 = _rand.Next(570, 573);
7082					Vector2 position4 = new Vector2(i * 16 + 8, j * 16 - 8);
7083					Vector2 velocity4 = new Vector2(Main.WindForVisuals * 2f, -0.5f);
7084					velocity4.X *= 1f + (float)_rand.Next(-50, 51) * 0.01f;
7085					velocity4.Y *= 1f + (float)_rand.Next(-50, 51) * 0.01f;
7086					if (num12 == 572)
7087					{
7088						position4.X -= 8f;
7089					}
7090					if (num12 == 571)
7091					{
7092						position4.X -= 4f;
7093					}
7094					Gore.NewGore(position4, velocity4, num12, 0.8f);
7095				}
7096			}
7097			else if (typeCache == 463)
7098			{
7099				if (tileFrameY == 54 && tileFrameX == 0)
7100				{
7101					for (int l = 0; l < 4; l++)
7102					{
7103						if (_rand.Next(2) != 0)
7104						{
7105							Dust dust2 = Dust.NewDustDirect(new Vector2(i * 16 + 4, j * 16), 36, 8, 16);
7106							dust2.noGravity = true;
7107							dust2.alpha = 140;
7108							dust2.fadeIn = 1.2f;
7109							dust2.velocity = Vector2.Zero;
7110						}
7111					}
7112				}
7113				if (tileFrameY == 18 && (tileFrameX == 0 || tileFrameX == 36))
7114				{
7115					for (int m = 0; m < 1; m++)
7116					{
7117						if (_rand.Next(13) == 0)
7118						{
7119							Dust dust3 = Dust.NewDustDirect(new Vector2(i * 16, j * 16), 8, 8, 274);
7120							dust3.position = new Vector2(i * 16 + 8, j * 16 + 8);
7121							dust3.position.X += ((tileFrameX == 36) ? 4 : (-4));
7122							dust3.noGravity = true;
7123							dust3.alpha = 128;
7124							dust3.fadeIn = 1.2f;
7125							dust3.noLight = true;
7126							dust3.velocity = new Vector2(0f, _rand.NextFloatDirection() * 1.2f);
7127						}
7128					}
7129				}
7130			}
7131			else if (typeCache == 497)
7132			{
7133				if (tileCache.frameY / 40 == 31 && tileCache.frameY % 40 == 0)
7134				{
7135					for (int n = 0; n < 1; n++)
7136					{
7137						if (_rand.Next(10) == 0)
7138						{
7139							Dust dust4 = Dust.NewDustDirect(new Vector2(i * 16, j * 16 + 8), 16, 12, 43);
7140							dust4.noGravity = true;
7141							dust4.alpha = 254;
7142							dust4.color = Color.White;
7143							dust4.scale = 0.7f;
7144							dust4.velocity = Vector2.Zero;
7145							dust4.noLight = true;
7146						}
7147					}
7148				}
7149			}
7150			else if (typeCache == 165 && tileFrameX >= 162 && tileFrameX <= 214 && tileFrameY == 72)
7151			{
7152				if (_rand.Next(60) == 0)
7153				{
7154					int num13 = Dust.NewDust(new Vector2(i * 16 + 2, j * 16 + 6), 8, 4, 153);
7155					_dust[num13].scale -= (float)_rand.Next(3) * 0.1f;
7156					_dust[num13].velocity.Y = 0f;
7157					_dust[num13].velocity.X *= 0.05f;
7158					_dust[num13].alpha = 100;
7159				}
7160			}
7161			else if (typeCache == 42 && tileFrameX == 0)
7162			{
7163				int num14 = tileFrameY / 36;
7164				if (tileFrameY / 18 % 2 == 1)
7165				{
7166					switch (num14)
7167					{
7168					case 7:
7169						if (_rand.Next(50) == 0)
7170						{
7171							int num17 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 + 4), 8, 8, 58, 0f, 0f, 150);
7172							_dust[num17].velocity *= 0.5f;
7173						}
7174						if (_rand.Next(100) == 0)
7175						{
7176							int num18 = Gore.NewGore(new Vector2(i * 16 - 2, j * 16 - 4), default(Vector2), _rand.Next(16, 18));
7177							_gore[num18].scale *= 0.7f;
7178							_gore[num18].velocity *= 0.25f;
7179						}
7180						break;
7181					case 29:
7182						if (_rand.Next(40) == 0)
7183						{
7184							int num19 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16), 8, 8, 59, 0f, 0f, 100);
7185							if (_rand.Next(3) != 0)
7186							{
7187								_dust[num19].noGravity = true;
7188							}
7189							_dust[num19].velocity *= 0.3f;
7190							_dust[num19].velocity.Y -= 1.5f;
7191						}
7192						break;
7193					case 50:
7194						if (_rand.Next(10) == 0)
7195						{
7196							int num16 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16), 8, 8, 57, 0f, 0f, 100);
7197							if (_rand.Next(3) != 0)
7198							{
7199								_dust[num16].noGravity = true;
7200							}
7201							_dust[num16].velocity *= 0.3f;
7202							_dust[num16].velocity.Y -= 1.5f;
7203						}
7204						break;
7205					case 51:
7206						if (_rand.Next(40) == 0)
7207						{
7208							int num15 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 + 2), 4, 4, 242, 0f, 0f, 100);
7209							if (_rand.Next(3) != 0)
7210							{
7211								_dust[num15].noGravity = true;
7212							}
7213							_dust[num15].velocity *= 0.3f;
7214							_dust[num15].velocity.Y -= 1.5f;
7215						}
7216						break;
7217					}
7218				}
7219			}
7220			if (typeCache == 4 && _rand.Next(40) == 0 && tileFrameX < 66)
7221			{
7222				int num20 = (int)MathHelper.Clamp(tileCache.frameY / 22, 0f, TorchID.Count - 1);
7223				int num21 = TorchID.Dust[num20];
7224				int num22 = 0;
7225				num22 = tileFrameX switch
7226				{
7227					22 => Dust.NewDust(new Vector2(i * 16 + 6, j * 16), 4, 4, num21, 0f, 0f, 100), 
7228					44 => Dust.NewDust(new Vector2(i * 16 + 2, j * 16), 4, 4, num21, 0f, 0f, 100), 
7229					_ => Dust.NewDust(new Vector2(i * 16 + 4, j * 16), 4, 4, num21, 0f, 0f, 100), 

```


---

## 🤖 Assistant · 2026-08-11T02:32:18.894Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 400,
 "offset": 7230
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:18.920Z

**📎 ToolResult**

```
7230				};
7231				if (_rand.Next(3) != 0)
7232				{
7233					_dust[num22].noGravity = true;
7234				}
7235				_dust[num22].velocity *= 0.3f;
7236				_dust[num22].velocity.Y -= 1.5f;
7237				if (num21 == 66)
7238				{
7239					_dust[num22].color = new Color(Main.DiscoR, Main.DiscoG, Main.DiscoB);
7240					_dust[num22].noGravity = true;
7241				}
7242			}
7243			if (typeCache == 93 && _rand.Next(40) == 0 && tileFrameX == 0)
7244			{
7245				int num23 = tileFrameY / 54;
7246				if (tileFrameY / 18 % 3 == 0)
7247				{
7248					int num24;
7249					switch (num23)
7250					{
7251					case 0:
7252					case 6:
7253					case 7:
7254					case 8:
7255					case 10:
7256					case 14:
7257					case 15:
7258					case 16:
7259						num24 = 6;
7260						break;
7261					case 20:
7262						num24 = 59;
7263						break;
7264					case 44:
7265						num24 = 57;
7266						break;
7267					case 45:
7268						num24 = 242;
7269						break;
7270					default:
7271						num24 = -1;
7272						break;
7273					}
7274					if (num24 != -1)
7275					{
7276						int num25 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 + 2), 4, 4, num24, 0f, 0f, 100);
7277						if (_rand.Next(3) != 0)
7278						{
7279							_dust[num25].noGravity = true;
7280						}
7281						_dust[num25].velocity *= 0.3f;
7282						_dust[num25].velocity.Y -= 1.5f;
7283					}
7284				}
7285			}
7286			if (typeCache == 100 && _rand.Next(40) == 0 && tileFrameX < 36)
7287			{
7288				int num26 = tileFrameY / 36;
7289				if (tileFrameY / 18 % 2 == 0)
7290				{
7291					int num27;
7292					switch (num26)
7293					{
7294					case 0:
7295					case 5:
7296					case 7:
7297					case 8:
7298					case 10:
7299					case 12:
7300					case 14:
7301					case 15:
7302					case 16:
7303						num27 = 6;
7304						break;
7305					case 20:
7306						num27 = 59;
7307						break;
7308					case 44:
7309						num27 = 57;
7310						break;
7311					case 45:
7312						num27 = 242;
7313						break;
7314					default:
7315						num27 = -1;
7316						break;
7317					}
7318					if (num27 != -1)
7319					{
7320						int num28 = 0;
7321						Vector2 position5 = ((tileFrameX == 0) ? ((_rand.Next(3) != 0) ? new Vector2(i * 16 + 14, j * 16 + 2) : new Vector2(i * 16 + 4, j * 16 + 2)) : ((_rand.Next(3) != 0) ? new Vector2(i * 16, j * 16 + 2) : new Vector2(i * 16 + 6, j * 16 + 2)));
7322						num28 = Dust.NewDust(position5, 4, 4, num27, 0f, 0f, 100);
7323						if (_rand.Next(3) != 0)
7324						{
7325							_dust[num28].noGravity = true;
7326						}
7327						_dust[num28].velocity *= 0.3f;
7328						_dust[num28].velocity.Y -= 1.5f;
7329					}
7330				}
7331			}
7332			if (typeCache == 98 && _rand.Next(40) == 0 && tileFrameY == 0 && tileFrameX == 0)
7333			{
7334				int num29 = Dust.NewDust(new Vector2(i * 16 + 12, j * 16 + 2), 4, 4, 6, 0f, 0f, 100);
7335				if (_rand.Next(3) != 0)
7336				{
7337					_dust[num29].noGravity = true;
7338				}
7339				_dust[num29].velocity *= 0.3f;
7340				_dust[num29].velocity.Y -= 1.5f;
7341			}
7342			if (typeCache == 49 && tileFrameX == 0 && _rand.Next(2) == 0)
7343			{
7344				int num30 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 - 4), 4, 4, 172, 0f, 0f, 100);
7345				if (_rand.Next(3) == 0)
7346				{
7347					_dust[num30].scale = 0.5f;
7348				}
7349				else
7350				{
7351					_dust[num30].scale = 0.9f;
7352					_dust[num30].noGravity = true;
7353				}
7354				_dust[num30].velocity *= 0.3f;
7355				_dust[num30].velocity.Y -= 1.5f;
7356			}
7357			if (typeCache == 372 && tileFrameX == 0 && _rand.Next(2) == 0)
7358			{
7359				int num31 = Dust.NewDust(new Vector2(i * 16 + 4, j * 16 - 4), 4, 4, 242, 0f, 0f, 100);
7360				if (_rand.Next(3) == 0)
7361				{
7362					_dust[num31].scale = 0.5f;
7363				}
7364				else
7365				{
7366					_dust[num31].scale = 0.9f;
7367					_dust[num31].noGravity = true;
7368				}
7369				_dust[num31].velocity *= 0.3f;
7370				_dust[num31].velocity.Y -= 1.5f;
7371			}
7372			if (typeCache == 646 && tileFrameX == 0)
7373			{
7374				_rand.Next(2);
7375			}
7376			if (typeCache == 34 && _rand.Next(40) == 0 && tileFrameX % 108 < 54)
7377			{
7378				int num32 = tileFrameY / 54;
7379				if (tileFrameX >= 108)
7380				{
7381					num32 += 37 * (tileFrameX / 108);
7382				}
7383				int num33 = tileFrameX / 18 % 3;
7384				if (tileFrameY / 18 % 3 == 1 && num33 != 1)
7385				{
7386					int num34;
7387					switch (num32)
7388					{
7389					case 0:
7390					case 1:
7391					case 2:
7392					case 3:
7393					case 4:
7394					case 5:
7395					case 12:
7396					case 13:
7397					case 16:
7398					case 19:
7399					case 21:
7400						num34 = 6;
7401						break;
7402					case 25:
7403						num34 = 59;
7404						break;
7405					case 50:
7406						num34 = 57;
7407						break;
7408					case 51:
7409						num34 = 242;
7410						break;
7411					default:
7412						num34 = -1;
7413						break;
7414					}
7415					if (num34 != -1)
7416					{
7417						int num35 = Dust.NewDust(new Vector2(i * 16, j * 16 + 2), 14, 6, num34, 0f, 0f, 100);
7418						if (_rand.Next(3) != 0)
7419						{
7420							_dust[num35].noGravity = true;
7421						}
7422						_dust[num35].velocity *= 0.3f;
7423						_dust[num35].velocity.Y -= 1.5f;
7424					}
7425				}
7426			}
7427			if (typeCache == 83)
7428			{
7429				int style = tileFrameX / 18;
7430				if (WorldGen.IsAlchemyPlantHarvestable(style, j))
7431				{
7432					EmitAlchemyHerbParticles(j, i, style);
7433				}
7434			}
7435			if (typeCache == 22 && _rand.Next(400) == 0)
7436			{
7437				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7438			}
7439			else if ((typeCache == 23 || typeCache == 24 || typeCache == 32) && _rand.Next(500) == 0)
7440			{
7441				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7442			}
7443			else if (typeCache == 25 && _rand.Next(700) == 0)
7444			{
7445				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7446			}
7447			else if (typeCache == 112 && _rand.Next(700) == 0)
7448			{
7449				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14);
7450			}
7451			else if ((typeCache == 31 || typeCache == 696) && _rand.Next(20) == 0)
7452			{
7453				if (tileFrameX >= 36)
7454				{
7455					int num36 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 5, 0f, 0f, 100);
7456					_dust[num36].velocity.Y = 0f;
7457					_dust[num36].velocity.X *= 0.3f;
7458				}
7459				else
7460				{
7461					Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14, 0f, 0f, 100);
7462				}
7463			}
7464			else if ((typeCache == 26 || typeCache == 695) && _rand.Next(20) == 0)
7465			{
7466				if (tileFrameX >= 54)
7467				{
7468					int num37 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 5, 0f, 0f, 100);
7469					_dust[num37].scale = 1.5f;
7470					_dust[num37].noGravity = true;
7471					_dust[num37].velocity *= 0.75f;
7472				}
7473				else
7474				{
7475					Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14, 0f, 0f, 100);
7476				}
7477			}
7478			else if ((typeCache == 71 || typeCache == 72) && tileCache.color() == 0 && _rand.Next(500) == 0)
7479			{
7480				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 41, 0f, 0f, 250, default(Color), 0.8f);
7481			}
7482			else if ((typeCache == 17 || typeCache == 77 || typeCache == 133) && _rand.Next(40) == 0)
7483			{
7484				if (tileFrameX == 18 && tileFrameY == 18)
7485				{
7486					int num38 = Dust.NewDust(new Vector2(i * 16 - 4, j * 16 - 6), 8, 6, 6, 0f, 0f, 100);
7487					if (_rand.Next(3) != 0)
7488					{
7489						_dust[num38].noGravity = true;
7490					}
7491				}
7492			}
7493			else if (typeCache == 405 && _rand.Next(20) == 0)
7494			{
7495				if (tileFrameX == 18 && tileFrameY == 18)
7496				{
7497					int num39 = Dust.NewDust(new Vector2(i * 16 - 4, j * 16 - 6), 24, 10, 6, 0f, 0f, 100);
7498					if (_rand.Next(5) != 0)
7499					{
7500						_dust[num39].noGravity = true;
7501					}
7502				}
7503			}
7504			else if (typeCache == 37 && _rand.Next(250) == 0)
7505			{
7506				int num40 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 6, 0f, 0f, 0, default(Color), _rand.Next(3));
7507				if (_dust[num40].scale > 1f)
7508				{
7509					_dust[num40].noGravity = true;
7510				}
7511			}
7512			else if ((typeCache == 58 || typeCache == 76 || typeCache == 684) && _rand.Next(250) == 0)
7513			{
7514				int num41 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 6, 0f, 0f, 0, default(Color), _rand.Next(3));
7515				if (_dust[num41].scale > 1f)
7516				{
7517					_dust[num41].noGravity = true;
7518				}
7519				_dust[num41].noLight = true;
7520			}
7521			else if (typeCache == 61 || typeCache == 703)
7522			{
7523				if (tileFrameX == 144 && _rand.Next(60) == 0)
7524				{
7525					int num42 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 44, 0f, 0f, 250, default(Color), 0.4f);
7526					_dust[num42].fadeIn = 0.7f;
7527				}
7528			}
7529			else if (Main.tileShine[typeCache] > 0)
7530			{
7531				if (tileLight.R <= 20 && tileLight.B <= 20 && tileLight.G <= 20)
7532				{
7533					return;
7534				}
7535				int num43 = tileLight.R;
7536				if (tileLight.G > num43)
7537				{
7538					num43 = tileLight.G;
7539				}
7540				if (tileLight.B > num43)
7541				{
7542					num43 = tileLight.B;
7543				}
7544				num43 /= 30;
7545				if (_rand.Next(Main.tileShine[typeCache]) >= num43 || ((typeCache == 21 || typeCache == 441) && (tileFrameX < 36 || tileFrameX >= 180) && (tileFrameX < 396 || tileFrameX > 409)) || ((typeCache == 467 || typeCache == 468) && (tileFrameX < 144 || tileFrameX >= 180)))
7546				{
7547					return;
7548				}
7549				Color newColor = Color.White;
7550				switch (typeCache)
7551				{
7552				case 617:
7553				{
7554					int x = i;
7555					int y = j;
7556					WorldGen.GetTopLeftAndStyles(ref x, ref y, 3, 4, 18, 18);
7557					int num45 = y;
7558					Tile tile = Main.tile[x + 1, y + 1];
7559					if (!IsVisible(tile))
7560					{
7561						num45 = y + 3;
7562					}
7563					if (j >= num45)
7564					{
7565						int num46 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, newColor, 0.5f);
7566						_dust[num46].velocity *= 0f;
7567					}
7568					return;
7569				}
7570				case 178:
7571				{
7572					switch (tileFrameX / 18)
7573					{
7574					case 0:
7575						newColor = new Color(255, 0, 255, 255);
7576						break;
7577					case 1:
7578						newColor = new Color(255, 255, 0, 255);
7579						break;
7580					case 2:
7581						newColor = new Color(0, 0, 255, 255);
7582						break;
7583					case 3:
7584						newColor = new Color(0, 255, 0, 255);
7585						break;
7586					case 4:
7587						newColor = new Color(255, 0, 0, 255);
7588						break;
7589					case 5:
7590						newColor = new Color(255, 255, 255, 255);
7591						break;
7592					case 6:
7593						newColor = new Color(255, 255, 0, 255);
7594						break;
7595					}
7596					int num44 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, newColor, 0.5f);
7597					_dust[num44].velocity *= 0f;
7598					return;
7599				}
7600				case 63:
7601					newColor = new Color(0, 0, 255, 255);
7602					break;
7603				}
7604				if (typeCache == 64)
7605				{
7606					newColor = new Color(255, 0, 0, 255);
7607				}
7608				if (typeCache == 65)
7609				{
7610					newColor = new Color(0, 255, 0, 255);
7611				}
7612				if (typeCache == 66)
7613				{
7614					newColor = new Color(255, 255, 0, 255);
7615				}
7616				if (typeCache == 67)
7617				{
7618					newColor = new Color(255, 0, 255, 255);
7619				}
7620				if (typeCache == 68)
7621				{
7622					newColor = new Color(255, 255, 255, 255);
7623				}
7624				if (typeCache == 566)
7625				{
7626					newColor = new Color(255, 255, 0, 255);
7627				}
7628				if (typeCache == 12 || typeCache == 665)
7629				{

```


---

## 🤖 Assistant · 2026-08-11T02:32:22.101Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to read lines 7629-7850 to finish the tileShine block and the ones after (374, 375, 461, 709, 227). Also check lines 8600-8730 and 9200-9300 and 9750-9831 for other Dust contexts. And lines 880-1010 (liquid particles - not tile ambient per se).
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:32:22.163Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 240,
 "offset": 7629
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:22.180Z

**📎 ToolResult**

```
7629				{
7630					newColor = new Color(255, 0, 0, 255);
7631				}
7632				if (typeCache == 639)
7633				{
7634					newColor = new Color(0, 0, 255, 255);
7635				}
7636				if (typeCache == 204)
7637				{
7638					newColor = new Color(255, 0, 0, 255);
7639				}
7640				if (typeCache == 211)
7641				{
7642					newColor = new Color(50, 255, 100, 255);
7643				}
7644				int num47 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, newColor, 0.5f);
7645				_dust[num47].velocity *= 0f;
7646			}
7647			else if (Main.tileSolid[tileCache.type] && Main.shimmerAlpha > 0f && (tileLight.R > 20 || tileLight.B > 20 || tileLight.G > 20))
7648			{
7649				int num48 = tileLight.R;
7650				if (tileLight.G > num48)
7651				{
7652					num48 = tileLight.G;
7653				}
7654				if (tileLight.B > num48)
7655				{
7656					num48 = tileLight.B;
7657				}
7658				int maxValue = 500;
7659				if ((float)_rand.Next(maxValue) < 2f * Main.shimmerAlpha)
7660				{
7661					Color white = Color.White;
7662					float scale2 = ((float)num48 / 255f + 1f) / 2f;
7663					int num49 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 43, 0f, 0f, 254, white, scale2);
7664					_dust[num49].velocity *= 0f;
7665				}
7666			}
7667		}
7668	
7669		private void EmitLivingTreeLeaf(int i, int j, int leafGoreType)
7670		{
7671			EmitLivingTreeLeaf_Below(i, j, leafGoreType);
7672			if (_rand.Next(2) == 0)
7673			{
7674				EmitLivingTreeLeaf_Sideways(i, j, leafGoreType);
7675			}
7676		}
7677	
7678		private void EmitLivingTreeLeaf_Below(int x, int y, int leafGoreType)
7679		{
7680			Tile tile = Main.tile[x, y + 1];
7681			if (!WorldGen.SolidTile(tile) && tile.liquid <= 0)
7682			{
7683				float windForVisuals = Main.WindForVisuals;
7684				if ((!(windForVisuals < -0.2f) || (!WorldGen.SolidTile(Main.tile[x - 1, y + 1]) && !WorldGen.SolidTile(Main.tile[x - 2, y + 1]))) && (!(windForVisuals > 0.2f) || (!WorldGen.SolidTile(Main.tile[x + 1, y + 1]) && !WorldGen.SolidTile(Main.tile[x + 2, y + 1]))))
7685				{
7686					Gore.NewGorePerfect(new Vector2(x * 16, y * 16 + 16), Vector2.Zero, leafGoreType).Frame.CurrentColumn = Main.tile[x, y].color();
7687				}
7688			}
7689		}
7690	
7691		private void EmitLivingTreeLeaf_Sideways(int x, int y, int leafGoreType)
7692		{
7693			int num = 0;
7694			if (Main.WindForVisuals > 0.2f)
7695			{
7696				num = 1;
7697			}
7698			else if (Main.WindForVisuals < -0.2f)
7699			{
7700				num = -1;
7701			}
7702			Tile tile = Main.tile[x + num, y];
7703			if (!WorldGen.SolidTile(tile) && tile.liquid <= 0)
7704			{
7705				int num2 = 0;
7706				if (num == -1)
7707				{
7708					num2 = -10;
7709				}
7710				Gore.NewGorePerfect(new Vector2(x * 16 + 8 + 4 * num + num2, y * 16 + 8), Vector2.Zero, leafGoreType).Frame.CurrentColumn = Main.tile[x, y].color();
7711			}
7712		}
7713	
7714		private void EmitLiquidDrops(int j, int i, Tile tileCache, ushort typeCache)
7715		{
7716			int num = 60;
7717			switch (typeCache)
7718			{
7719			case 374:
7720				num = 120;
7721				break;
7722			case 375:
7723				num = 180;
7724				break;
7725			case 461:
7726				num = 180;
7727				break;
7728			}
7729			if (tileCache.liquid != 0 || _rand.Next(num * 2) != 0)
7730			{
7731				return;
7732			}
7733			Rectangle rectangle = new Rectangle(i * 16, j * 16, 16, 16);
7734			rectangle.X -= 34;
7735			rectangle.Width += 68;
7736			rectangle.Y -= 100;
7737			rectangle.Height = 400;
7738			for (int k = 0; k < 600; k++)
7739			{
7740				Gore gore = _gore[k];
7741				if (gore.active && gore.type >= 0 && gore.type < GoreID.Count && GoreID.Sets.IsDrip[gore.type])
7742				{
7743					Rectangle value = new Rectangle((int)gore.position.X, (int)gore.position.Y, 16, 16);
7744					if (rectangle.Intersects(value))
7745					{
7746						return;
7747					}
7748				}
7749			}
7750			Vector2 position = new Vector2(i * 16, j * 16);
7751			int type = 706;
7752			if (Main.waterStyle == 14)
7753			{
7754				type = 706;
7755			}
7756			else if (Main.waterStyle == 13)
7757			{
7758				type = 706;
7759			}
7760			else if (Main.waterStyle == 12)
7761			{
7762				type = 1147;
7763			}
7764			else if (Main.waterStyle > 1)
7765			{
7766				type = 706 + Main.waterStyle - 1;
7767			}
7768			if (typeCache == 374)
7769			{
7770				type = 716;
7771			}
7772			if (typeCache == 375)
7773			{
7774				type = 717;
7775			}
7776			if (typeCache == 461)
7777			{
7778				type = 943;
7779				if (Main.SceneMetrics.ZoneCorrupt)
7780				{
7781					type = 1160;
7782				}
7783				if (Main.SceneMetrics.ZoneCrimson)
7784				{
7785					type = 1161;
7786				}
7787				if (Main.SceneMetrics.ZoneHallow)
7788				{
7789					type = 1162;
7790				}
7791			}
7792			if (typeCache == 709)
7793			{
7794				type = 1383;
7795			}
7796			int num2 = Gore.NewGore(position, default(Vector2), type);
7797			_gore[num2].velocity *= 0f;
7798		}
7799	
7800		private float GetWindCycle(int x, int y, double windCounter)
7801		{
7802			if (!Main.SettingsEnabled_TilesSwayInWind)
7803			{
7804				return 0f;
7805			}
7806			float num = (float)x * 0.5f + (float)(y / 100) * 0.5f;
7807			float num2 = (float)Math.Cos(windCounter * 6.2831854820251465 + (double)num) * 0.5f;
7808			if (Main.remixWorld)
7809			{
7810				if (!((double)y > Main.worldSurface))
7811				{
7812					return 0f;
7813				}
7814				num2 += Main.WindForVisuals;
7815			}
7816			else
7817			{
7818				if (!((double)y < Main.worldSurface))
7819				{
7820					return 0f;
7821				}
7822				num2 += Main.WindForVisuals;
7823			}
7824			float lerpValue = Utils.GetLerpValue(0.08f, 0.18f, Math.Abs(Main.WindForVisuals), clamped: true);
7825			return num2 * lerpValue;
7826		}
7827	
7828		private bool ShouldSwayInWind(int x, int y, Tile tileCache)
7829		{
7830			if (!Main.SettingsEnabled_TilesSwayInWind)
7831			{
7832				return false;
7833			}
7834			if (!TileID.Sets.SwaysInWindBasic[tileCache.type])
7835			{
7836				return false;
7837			}
7838			if (tileCache.type == 227 && (tileCache.frameX == 204 || tileCache.frameX == 238 || tileCache.frameX == 408 || tileCache.frameX == 442 || tileCache.frameX == 476))
7839			{
7840				return false;
7841			}
7842			return true;
7843		}
7844	
7845		private void UpdateLeafFrequency()
7846		{
7847			float num = Math.Abs(Main.WindForVisuals);
7848			if (num <= 0.1f)
7849			{
7850				_leafFrequency = 2000;
7851			}
7852			else if (num <= 0.2f)
7853			{
7854				_leafFrequency = 1000;
7855			}
7856			else if (num <= 0.3f)
7857			{
7858				_leafFrequency = 450;
7859			}
7860			else if (num <= 0.4f)
7861			{
7862				_leafFrequency = 300;
7863			}
7864			else if (num <= 0.5f)
7865			{
7866				_leafFrequency = 200;
7867			}
7868			else if (num <= 0.6f)

```


---

## 🤖 Assistant · 2026-08-11T02:32:22.353Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 120,
 "offset": 9780
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:22.372Z

**📎 ToolResult**

```
9780		private void EmitAlchemyHerbParticles(int j, int i, int style)
9781		{
9782			if (style == 0 && _rand.Next(100) == 0)
9783			{
9784				int num = Dust.NewDust(new Vector2(i * 16, j * 16 - 4), 16, 16, 19, 0f, 0f, 160, default(Color), 0.1f);
9785				_dust[num].velocity.X /= 2f;
9786				_dust[num].velocity.Y /= 2f;
9787				_dust[num].noGravity = true;
9788				_dust[num].fadeIn = 1f;
9789			}
9790			if (style == 1 && _rand.Next(100) == 0)
9791			{
9792				Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 41, 0f, 0f, 250, default(Color), 0.8f);
9793			}
9794			if (style == 3)
9795			{
9796				if (_rand.Next(200) == 0)
9797				{
9798					int num2 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 14, 0f, 0f, 100, default(Color), 0.2f);
9799					_dust[num2].fadeIn = 1.2f;
9800				}
9801				if (_rand.Next(75) == 0)
9802				{
9803					int num3 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 27, 0f, 0f, 100);
9804					_dust[num3].velocity.X /= 2f;
9805					_dust[num3].velocity.Y /= 2f;
9806				}
9807			}
9808			if (style == 4 && _rand.Next(150) == 0)
9809			{
9810				int num4 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 8, 16);
9811				_dust[num4].velocity.X /= 3f;
9812				_dust[num4].velocity.Y /= 3f;
9813				_dust[num4].velocity.Y -= 0.7f;
9814				_dust[num4].alpha = 50;
9815				_dust[num4].scale *= 0.1f;
9816				_dust[num4].fadeIn = 0.9f;
9817				_dust[num4].noGravity = true;
9818			}
9819			if (style == 5 && _rand.Next(40) == 0)
9820			{
9821				int num5 = Dust.NewDust(new Vector2(i * 16, j * 16 - 6), 16, 16, 6, 0f, 0f, 0, default(Color), 1.5f);
9822				_dust[num5].velocity.Y -= 2f;
9823				_dust[num5].noGravity = true;
9824			}
9825			if (style == 6 && _rand.Next(30) == 0)
9826			{
9827				int num6 = Dust.NewDust(newColor: new Color(50, 255, 255, 255), Position: new Vector2(i * 16, j * 16), Width: 16, Height: 16, Type: 43, SpeedX: 0f, SpeedY: 0f, Alpha: 254, Scale: 0.5f);
9828				_dust[num6].velocity *= 0f;
9829			}
9830		}
9831	}
9832	

```


---

## 🤖 Assistant · 2026-08-11T02:32:28.049Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the main method DrawTiles_EmitParticles fully (6795-7667) plus EmitAlchemyHerbParticles (9780-9830). Let me also check the other Dust blocks at 921/940/966 (liquid surface?), 8655/8674/8702, 9274 — these are probably in liquid drawing or ember methods. Also 9810 etc. covered. And check where 42 torch style things... Also check 1006 typeCache==72 (gem sparkles? no).

Let me check what methods lines 900-1000, 8640-8720, and 9240-9290 belong to, to determine whether they are tile-ambient (the user asked about the per-visible-tile method but also wants context). Also check Main.cs legacy list.

Also should check the "typeCache == 718" — 718 is... tile ids: 718 = Seaweed? Actually 577-... Let me recall 1.4.4 tile IDs: 718 might be "Seagrass"? Hmm. Actually 718 = ? Let me think: 706=Corrupt... 1.4.4 new tiles: 646 = "Torch god's favor"? No. Let me check TileID.cs for names if available. Let me grep for the IDs in a TileID file.

Let me check the method contexts and tile names.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:32:28.533Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '895,1000p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "description": "Read lines 895-1000 for context"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:28.575Z

**📎 ToolResult**

```
			Main.tileBatch.SetLayer(Layer_BehindTiles, 0);
		}
		tileDrawInfo.drawTexture = GetTileDrawTexture(tileDrawInfo.tileCache, tileX, tileY);
		Texture2D highlightTexture = null;
		Rectangle empty = Rectangle.Empty;
		Color highlightColor = Color.Transparent;
		if (TileID.Sets.HasOutlines[tileDrawInfo.typeCache])
		{
			GetTileOutlineInfo(tileX, tileY, tileDrawInfo.typeCache, ref tileDrawInfo.tileLight, ref highlightTexture, ref highlightColor);
		}
		if (_perspectivePlayer.dangerSense && IsTileDangerous(_perspectivePlayer, tileDrawInfo.tileCache, tileDrawInfo.typeCache))
		{
			if (tileDrawInfo.tileLight.R < byte.MaxValue)
			{
				tileDrawInfo.tileLight.R = byte.MaxValue;
			}
			if (tileDrawInfo.tileLight.G < 50)
			{
				tileDrawInfo.tileLight.G = 50;
			}
			if (tileDrawInfo.tileLight.B < 50)
			{
				tileDrawInfo.tileLight.B = 50;
			}
			if (_isActiveAndNotPaused && _rand.Next(30) == 0)
			{
				int num = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 60, 0f, 0f, 100, default(Color), 0.3f);
				_dust[num].fadeIn = 1f;
				_dust[num].velocity *= 0.1f;
				_dust[num].noLight = true;
				_dust[num].noGravity = true;
			}
		}
		if (_perspectivePlayer.findTreasure && Main.IsTileSpelunkable(tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY))
		{
			if (tileDrawInfo.tileLight.R < 200)
			{
				tileDrawInfo.tileLight.R = 200;
			}
			if (tileDrawInfo.tileLight.G < 170)
			{
				tileDrawInfo.tileLight.G = 170;
			}
			if (_isActiveAndNotPaused && _rand.Next(60) == 0)
			{
				int num2 = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 204, 0f, 0f, 150, default(Color), 0.3f);
				_dust[num2].fadeIn = 1f;
				_dust[num2].velocity *= 0.1f;
				_dust[num2].noLight = true;
			}
		}
		if (_perspectivePlayer.biomeSight)
		{
			Color sightColor = Color.White;
			if (Main.IsTileBiomeSightable(tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, ref sightColor))
			{
				if (tileDrawInfo.tileLight.R < sightColor.R)
				{
					tileDrawInfo.tileLight.R = sightColor.R;
				}
				if (tileDrawInfo.tileLight.G < sightColor.G)
				{
					tileDrawInfo.tileLight.G = sightColor.G;
				}
				if (tileDrawInfo.tileLight.B < sightColor.B)
				{
					tileDrawInfo.tileLight.B = sightColor.B;
				}
				if (_isActiveAndNotPaused && _rand.Next(480) == 0)
				{
					Color newColor = sightColor;
					int num3 = Dust.NewDust(new Vector2(tileX * 16, tileY * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
					_dust[num3].noGravity = true;
					_dust[num3].fadeIn = 1f;
					_dust[num3].velocity *= 0.1f;
					_dust[num3].noLightEmittance = true;
				}
			}
		}
		if (_isActiveAndNotPaused)
		{
			if (!Lighting.UpdateEveryFrame || new FastRandom(Main.TileFrameSeed).WithModifier(tileX, tileY).Next(4) == 0)
			{
				DrawTiles_EmitParticles(tileY, tileX, tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, tileDrawInfo.tileLight);
			}
			tileDrawInfo.tileLight = DrawTiles_GetLightOverride(tileY, tileX, tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, tileDrawInfo.tileLight);
		}
		bool flag = false;
		if (tileDrawInfo.glowTexture != null || Main.tileGlowMask[tileDrawInfo.typeCache] != -1 || Main.tileFlame[tileDrawInfo.typeCache])
		{
			flag = true;
		}
		if (tileDrawInfo.tileLight.R >= 1 || tileDrawInfo.tileLight.G >= 1 || tileDrawInfo.tileLight.B >= 1 || TileID.Sets.IgnoreDrawLightConditions[tileDrawInfo.typeCache])
		{
			flag = true;
		}
		if (tileDrawInfo.tileCache.wall > 0 && (tileDrawInfo.tileCache.wall == 318 || tileDrawInfo.tileCache.fullbrightWall()))
		{
			flag = true;
		}
		bool flag2 = IsVisible(tileDrawInfo.tileCache);
		if (!flag2)
		{
			flag = false;
		}
		if (!flag && flag2 && TileDrawingBase.DrawOwnBlacks)

```


---

## 🤖 Assistant · 2026-08-11T02:32:29.638Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '8630,8720p;9230,9290p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs && grep -n \"private void\\|private bool\\|public void\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | awk -F: '$1>8600 && $1<9800'",
 "description": "Read other dust blocks and method boundaries"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:32:33.518Z

**📎 ToolResult**

```
				{
					DrawNatureGlowmask(glowTexture, position, new Rectangle(tileFrameX + addFrX, tileFrameY + addFrY, tileWidth, tileHeight - halfBrickHeight), glowColor, num3 * 0.1f, origin, 1f, tileSpriteEffect, 0f);
				}
			}
		}
	}

	private void DrawAnimatedTile_AdjustForVisionChangers(int i, int j, Tile tileCache, ushort typeCache, short tileFrameX, short tileFrameY, ref Color tileLight, bool canDoDust)
	{
		if (_perspectivePlayer.dangerSense && IsTileDangerous(_perspectivePlayer, tileCache, typeCache))
		{
			if (tileLight.R < byte.MaxValue)
			{
				tileLight.R = byte.MaxValue;
			}
			if (tileLight.G < 50)
			{
				tileLight.G = 50;
			}
			if (tileLight.B < 50)
			{
				tileLight.B = 50;
			}
			if (_isActiveAndNotPaused && canDoDust && _rand.Next(30) == 0)
			{
				int num = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 60, 0f, 0f, 100, default(Color), 0.3f);
				_dust[num].fadeIn = 1f;
				_dust[num].velocity *= 0.1f;
				_dust[num].noLight = true;
				_dust[num].noGravity = true;
			}
		}
		if (_perspectivePlayer.findTreasure && Main.IsTileSpelunkable(typeCache, tileFrameX, tileFrameY))
		{
			if (tileLight.R < 200)
			{
				tileLight.R = 200;
			}
			if (tileLight.G < 170)
			{
				tileLight.G = 170;
			}
			if (_isActiveAndNotPaused && _rand.Next(60) == 0 && canDoDust)
			{
				int num2 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 204, 0f, 0f, 150, default(Color), 0.3f);
				_dust[num2].fadeIn = 1f;
				_dust[num2].velocity *= 0.1f;
				_dust[num2].noLight = true;
			}
		}
		if (!_perspectivePlayer.biomeSight)
		{
			return;
		}
		Color sightColor = Color.White;
		if (Main.IsTileBiomeSightable(typeCache, tileFrameX, tileFrameY, ref sightColor))
		{
			if (tileLight.R < sightColor.R)
			{
				tileLight.R = sightColor.R;
			}
			if (tileLight.G < sightColor.G)
			{
				tileLight.G = sightColor.G;
			}
			if (tileLight.B < sightColor.B)
			{
				tileLight.B = sightColor.B;
			}
			if (_isActiveAndNotPaused && canDoDust && _rand.Next(480) == 0)
			{
				Color newColor = sightColor;
				int num3 = Dust.NewDust(new Vector2(i * 16, j * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
				_dust[num3].noGravity = true;
				_dust[num3].fadeIn = 1f;
				_dust[num3].velocity *= 0.1f;
				_dust[num3].noLightEmittance = true;
			}
		}
	}

	private float GetWindGridPush(int i, int j, int pushAnimationTimeTotal, float pushForcePerFrame)
	{
		_windGrid.GetWindTime(i, j, pushAnimationTimeTotal, out var windTimeLeft, out var directionX, out var _);
		if (windTimeLeft >= pushAnimationTimeTotal / 2)
		{
			return (float)(pushAnimationTimeTotal - windTimeLeft) * pushForcePerFrame * (float)directionX;
		}
		return (float)windTimeLeft * pushForcePerFrame * (float)directionX;
	}

			if (Main.remixWorld)
			{
				if (WallID.Sets.AllowsWind[tile.wall] && (double)i > Main.worldSurface)
				{
					num2++;
				}
			}
			else if (WallID.Sets.AllowsWind[tile.wall] && (double)i < Main.worldSurface)
			{
				num2++;
			}
			float windGridPush = GetWindGridPush(x, i, 20, 0.01f);
			num4 = ((windGridPush != 0f || num5 == 0f) ? (num4 - windGridPush) : (num4 * -0.78f));
			num5 = windGridPush;
			short tileFrameX = tile.frameX;
			short tileFrameY = tile.frameY;
			Color color = Lighting.GetColor(x, i);
			GetTileDrawData(x, i, tile, type, ref tileFrameX, ref tileFrameY, out var tileWidth, out var tileHeight, out var tileTop, out var halfBrickHeight, out var addFrX, out var addFrY, out var tileSpriteEffect, out var glowTexture, out var glowSourceRect, out var glowColor);
			Vector2 position = new Vector2(-(int)screenPosition.X, -(int)screenPosition.Y) + offSet + vector;
			if (tile.fullbrightBlock())
			{
				color = Color.White;
			}
			float num6 = (float)num2 * num3 * windCycle + num4;
			if (_perspectivePlayer.biomeSight)
			{
				Color sightColor = Color.White;
				if (Main.IsTileBiomeSightable(type, tileFrameX, tileFrameY, ref sightColor))
				{
					if (color.R < sightColor.R)
					{
						color.R = sightColor.R;
					}
					if (color.G < sightColor.G)
					{
						color.G = sightColor.G;
					}
					if (color.B < sightColor.B)
					{
						color.B = sightColor.B;
					}
					if (_isActiveAndNotPaused && _rand.Next(480) == 0)
					{
						Color newColor = sightColor;
						int num7 = Dust.NewDust(new Vector2(x * 16, i * 16), 16, 16, 267, 0f, 0f, 150, newColor, 0.3f);
						_dust[num7].noGravity = true;
						_dust[num7].fadeIn = 1f;
						_dust[num7].velocity *= 0.1f;
						_dust[num7].noLightEmittance = true;
					}
				}
			}
			Texture2D tileDrawTexture = GetTileDrawTexture(tile, x, i);
			if (tileDrawTexture == null)
			{
				break;
			}
			if (IsVisible(tile))
			{
				Tile tile2 = Main.tile[x, i + 1];
				bool flag = tile2.active() && TileID.Sets.VineThreads[tile2.type];
8637:	private void DrawAnimatedTile_AdjustForVisionChangers(int i, int j, Tile tileCache, ushort typeCache, short tileFrameX, short tileFrameY, ref Color tileLight, bool canDoDust)
8721:	private void GetWindGridPush2Axis(int i, int j, int pushAnimationTimeTotal, float pushForcePerFrame, out float pushX, out float pushY)
8754:	private void DrawMasterTrophies()
8798:	private void DrawTeleportationPylons()
8868:	private void DrawVoidLenses()
8898:	private void DrawMultiTileGrass()
8989:	private void DrawMultiTileVines()
9050:	private void DrawVines()
9065:	private void DrawReverseVines()
9080:	private void DrawMultiTileGrassInWind(Vector2 screenPosition, Vector2 offSet, int topLeftX, int topLeftY, int sizeX, int sizeY)
9198:	private void DrawVineStrip(Vector2 screenPosition, Vector2 offSet, int x, int startY)
9301:	private void DrawRisingVineStrip(Vector2 screenPosition, Vector2 offSet, int x, int startY)
9407:	private void DrawMultiTileVinesInWind(Vector2 screenPosition, Vector2 offSet, int topLeftX, int topLeftY, int sizeX, int sizeY)
9780:	private void EmitAlchemyHerbParticles(int j, int i, int style)

```


---

## 🤖 Assistant · 2026-08-11T02:33:00.531Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So the other Dust blocks are vision-changer (danger sense/spelunker/biome sight) — not tile ambient per-tile emissions. Good to note but they're not tile-type specific (except spelunkable tiles). The user asked for ambient per-tile particle emissions. I'll note them briefly.

Now, the main DrawTiles_EmitParticles method (lines 6795–7667). Let me collect all entries:

Pre-visibility-gate (run regardless of `flag` = IsVisible):
1. 718 (night, _rand.Next(3)==0, not solid above) — gore 16/17 (firefly-ish) + dust 58 (RollLuck(30)) — lines 6800-6859. Tile 718 = ? In 1.4.4, 718... Let me check TileID.cs. Actually I recall 718 = "TallGrassFlowers"? No. 718 might be "FogMachine"? Hmm. Let me look up names from TileID.cs.

2. 244 (frameX==18 && frameY==18, rand(2)==0) — gore 411-415 probabilities (fireplace embers?) — lines 6860-6882. Tile 244 = Fireplace.
3. 565 (frameX==0, frameY==18, rand(3)==0) — Gore.NewGorePerfect type 1202 — 6883-6892. Tile 565 = Chimney (Smoke Block? actually 565 = "Smoke Block"). Yes, 565 = SmokeBlock.
4. 215 (frameY==0, frameY<36, rand(3)==0) — dust 31, rises (velocity.Y -= 0.5..1.4), x offset by frameX (0 → +rand(8), 36 → -rand(8)) — 6893-6908. Tile 215 = Brazier/Sconce? Actually 215 = "Sconce" (wall torch). Yes Sconce.
5. 592 (frameY==18, rand(3)==0) — dust 31 — 6909-6924. Tile 592 = Campfire.
6. 406 (frameY==54, frameX==0, rand(3)==0) — gore 825-827 (steam) — 6925-6946. Tile 406 = Geyser? Actually 406 = "LavaMosquito"? Hmm. 406 = Geyser yes.
7. 452 (frameY==0, frameX==0, rand(3)==0) — gore 907+ — 6947-6961. Tile 452 = Smoke blocks? Actually 452 = "Chimney". Hmm. Let me check names.
8. 192 (rand(leafFrequency)==0) — EmitLivingTreeLeaf 910 — 6962. Tile 192 = LivingMahoganyLeafy? 192 = LivingWood? Actually 192 = "LeafyLivingMahogany"? I think 192 = LivingMahoganyLeafyTree? Hmm. 192 = "LivingMahoganyLeaves"? Let me check TileID.
9. 384 — EmitLivingTreeLeaf 914 — 6966. 384 = LeafyJungleTree? Actually 384 = "LivingMahogany"? Need names.
10. 666 || 712 (liquid<=0, rand(100)==0, no tile above) — PooFly particle — 6970. 666 = ShadowOrb? No... 666 = "ShadowOrb"? Hmm — PooFly suggests these are "poop" tiles? No — PooFly particle is flies around poo. 666 and 712... hmm, in 1.4.4 tile 666 = "ShellPile"? Actually let me check. PooFly is used for... trash? Trash Can? 666 = "SolarBrick"? I'll check TileID.cs.
11. 711 (frameX==0, frameY==0) — RainbowBoulder particles — 6977-6994. 711 = RainbowBrick? "RainbowBoulder3/2" suggests 711 = ... hmm.

Then TileID.Sets.SpawnsNatureFlies generic (6995-7015), rubble dust generic (7016-7066).

Then visible-only (`flag`):
12. 238 rand(10)==0 — dust 168, noGravity, alpha 200 — 7071-7076. Tile 238 = Demonite? 238 = "CrystalBall"? Hmm. 238... demon altar is 55? Actually 238 = "Crystal Ball" is 87... Let me check: 238 = "BubbleMachine"? Hmm. Dust 168... Need names.
13. 139 — frameX==36 && frameY%36==0 && time%7==0 && rand(3)==0 — gore 570-572 (ember leaves) — 7077-7096. Tile 139 = Tree? no... 139 = "LivingRichMahoganyTree"? Hmm, actually 139 might be a tree with falling embers? Gore 570-572... 139 = "AshGrass"? Need lookup.
14. 463 — frameY==54, frameX==0 → dust 16 x4 (rand 2) steam; frameY==18 && (frameX 0 or 36) → dust 274 rand(13) vertical drift — 7097-7130. Tile 463 = Chimney! Yes 463 = Chimney (smoke).
15. 497 — frameY/40==31 — dust 43 rand(10) — 7131-7149. Tile 497 = FogMachine. Yes.
16. 165 — frameX 162-214 && frameY==72 — dust 153 rand(60) — 7150-7160. Tile 165 = Dresser? 165... dust 153 (bubble?). Hmm 165 = "Dresser". Actually frameY==72 with frameX range — dresser? Or "Placed bottle"? 165 = Dresser I believe.
17. 42 lantern variants frameX==0, frameY/36 cases: case 7 (rand50 dust 58; rand100 gore 16-17), case 29 (rand40 dust 59 rises), case 50 (rand10 dust 57), case 51 (rand40 dust 242) — 7161-7219. Tile 42 = Lantern.
18. 4 torch rand(40), frameX<66 — dust = TorchID.Dust[frameY/22], rises — 7220-7242.
19. 93 candelabra rand(40), frameX==0, frameY/18%3==0, styles dust 6/59/57/242 — 7243-7285. Tile 93 = Candelabra.
20. 100 chandelier rand(40), frameX<36, frameY/18%2==0, dust 6/59/57/242, position depends on frameX side — 7286-7331.
21. 98 rand(40), frameX==0 && frameY==0 — dust 6 — 7332-7341. Tile 98 = Candle? No candle is 33. 98 = ... hmm. Candle = 33. Then 98 = "LampPost"? Hmm — 98 might be "Candle" no. Let me check: torch 4, candle 33, ... 98? Hmm. In Terraria, 96 = "Grate"? Let me just look up TileID.cs.
22. 49 water candle frameX==0 rand(2) — dust 172 — 7342.
23. 372 peace candle frameX==0 rand(2) — dust 242 — 7357.
24. 646 frameX==0 — _rand.Next(2) only (no dust, dead code) — 7372-7375. 646 = TorchGodsFavor? no... 646 = "PlasmaLamp"? Actually 646 relates to "lavalamppre" hmm. Let me check names.
25. 34 rand(40) frameX%108<54, frameY/18%3==1 && col!=1, styles dust 6/59/57/242 — 7376-7426. Tile 34 = Bookcase? No — 34 = "Banner"? Hmm. 34 with styles... likely "WallTorch"? Hmm. Actually tile 34 = "Bookcase"? Bookcase is 101. 34 = "Lamp"? I think 34 = "HangingLantern"? no. Hmm — 34 could be "Chandelier"? no that's 100. Let me check TileID.cs.
26. 83 — alchemy herbs (EmitAlchemyHerbParticles, styles 0-6) — 7427-7434. Tile 83 = Blooming herbs.
27. 22 rand(400) — dust 14 — 7435. Tile 22 = Corrupt grass? No, 22 is... hmm. Dust 14? Tile 23 corrupt grass, 24 flesh grass? Wait: 23 = CorruptGrass, 24 = Crimson? Actually: 0 Dirt, 1 Stone, 2 ... 23 = Grass? No, 2 = Grass. 23 = CorruptGrass, 24 = CrimsonGrass(?), 25 = Ice? no. Hmm.

Wait: tile IDs: 2=Grass, 23=CorruptGrass, 24=? , 25=?, 27=?, 31=MushroomGrass? Hmm. Actually: 31 = MushroomGrass? No, 60 = MushroomGrass. Let me recall: 
- 23 = CorruptGrass
- 24 = CrimsonGrass? Actually I believe 24 isn't a tile; 199 = CrimsonGrass? Hmm no, 199 = Grass? Let me just look up the file.

Better to check TileID.cs in the repo. Let me grep for names.

Also 71/72 = CrystalShard? 71 = Crystal, 72 = Crystal? dust 41 (crystal sparkles), tileCache.color()==0, rand(500).
17/77/133 = DemonAltar(55?) hmm. 17 = DemonAltar? Actually 17 = "Demonite"? Let me check: 17 = Demon Altar? Hmm I think 25 = DemonAltar? No. 55 = DemonAltar. 17 = ... "Amber"? 

OK I really need TileID.cs. Let me find it.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:01.025Z · glm-x-preview-260804

```
The main method is `DrawTiles_EmitParticles` (lines 6795–7667) plus `EmitAlchemyHerbParticles` (9780–9830). Now let me resolve tile IDs to names via TileID.cs, and check Main.cs for legacy entries.
```


---

## 🤖 Assistant · 2026-08-11T02:33:01.528Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/ 2>/dev/null | head -30; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"TileID.cs\" 2>/dev/null",
 "description": "Locate TileID.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:01.593Z

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
Terraria.Chat.Commands
Terraria.Cinematics
Terraria.csproj
Terraria.DataStructures
Terraria.Enums
Terraria.GameContent
Terraria.GameContent.Achievements
Terraria.GameContent.Ambience
Terraria.GameContent.Animations
Terraria.GameContent.Bestiary
Terraria.GameContent.Biomes
Terraria.GameContent.Biomes.CaveHouse
Terraria.GameContent.Biomes.Desert
Terraria.GameContent.Creative
Terraria.GameContent.Creative.Content.Sacrifices.tsv
Terraria.GameContent.Drawing
Terraria.GameContent.Dyes
Terraria.GameContent.Events
Terraria.GameContent.FishDropRules
Terraria.GameContent.Generation
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs

```


---

## 🤖 Assistant · 2026-08-11T02:33:06.074Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
TileID.cs might not have numeric values if they're computed. Let me check how constants are defined.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:07.084Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public const ushort\\|new TileID.Constants\\|= [0-9]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | head -20; grep -n \"Dirt = \\|Stone = \\|Torch = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | head",
 "description": "Check TileID constant definitions format"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:07.141Z

**📎 ToolResult**

```
44:				if (tile == null || !tile.active() || tile.type != 4)
52:					if ((uint)(num - 18) <= 2u || num == 22)
58:					if ((uint)(num - 18) <= 2u)
426:			for (int i = 0; i < SaveSlopes.Length; i++)
433:	public const ushort Dirt = 0;
435:	public const ushort Stone = 1;
437:	public const ushort Grass = 2;
439:	public const ushort Plants = 3;
441:	public const ushort Torches = 4;
443:	public const ushort Trees = 5;
445:	public const ushort Iron = 6;
447:	public const ushort Copper = 7;
449:	public const ushort Gold = 8;
451:	public const ushort Silver = 9;
453:	public const ushort ClosedDoor = 10;
455:	public const ushort OpenDoor = 11;
457:	public const ushort Heart = 12;
459:	public const ushort Bottles = 13;
461:	public const ushort Tables = 14;
463:	public const ushort Chairs = 15;
22:			public static bool[] Dirt = Factory.CreateBoolSet(default(int));
26:			public static bool[] Stone = Factory.CreateBoolSet(1, 25, 117, 203);
119:			public static bool[] CountsAsTorch = Factory.CreateBoolSet(CountsAsTorchTypes);
285:		public static bool[] Dirt = Factory.CreateBoolSet(0, 668);
367:		public static int[] NeedsGrassFramingDirt = Factory.CreateIntSet(0, 633, 57);
433:	public const ushort Dirt = 0;
435:	public const ushort Stone = 1;

```


---

## 🤖 Assistant · 2026-08-11T02:33:12.314Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The constants have values. Let me build a name lookup. I'll grep the specific IDs I need. IDs needed: 4, 17, 22, 23, 24, 25, 26, 27, 31, 32, 33, 34, 37, 42, 49, 58, 59, 61, 63-68, 71, 72, 76, 77, 83, 93, 98, 100, 112, 133, 139, 165, 192, 204, 211, 215, 229, 238, 244, 372, 384, 405, 406, 441, 452, 461, 463, 467, 468, 497, 565, 566, 592, 617, 639, 646, 665, 666, 684, 695, 696, 703, 709, 711, 712, 718, 178.

Also gem sparkles: tileShine > 0 tiles (63-68 gems, 64 amethyst? etc.), 21 = gems? no 21 = Gems? Hmm: 21 = ? Actually 21 might be... let me just look up. Also 12 = Heart (Life Crystal - red), 204, 211, 566, 639, 178 (crystal ball pieces / disco).

Let me grep them all.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:13.940Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -oE \"public const ushort [A-Za-z0-9]+ = (4|12|17|21|22|23|24|25|26|27|31|32|33|34|37|42|49|58|59|61|63|64|65|66|67|68|71|72|76|77|83|93|98|100|112|133|139|165|178|192|204|211|215|229|238|244|372|384|405|406|441|452|461|463|467|468|497|565|566|592|617|639|646|665|666|684|695|696|703|709|711|712|718);\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Map tile IDs to names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:13.980Z

**📎 ToolResult**

```
public const ushort Torches = 4;
public const ushort Heart = 12;
public const ushort Furnaces = 17;
public const ushort Containers = 21;
public const ushort Demonite = 22;
public const ushort CorruptGrass = 23;
public const ushort CorruptPlants = 24;
public const ushort Ebonstone = 25;
public const ushort DemonAltar = 26;
public const ushort Sunflower = 27;
public const ushort ShadowOrbs = 31;
public const ushort CorruptThorns = 32;
public const ushort Candles = 33;
public const ushort Chandeliers = 34;
public const ushort Meteorite = 37;
public const ushort HangingLanterns = 42;
public const ushort WaterCandle = 49;
public const ushort Hellstone = 58;
public const ushort Mud = 59;
public const ushort JunglePlants = 61;
public const ushort Sapphire = 63;
public const ushort Ruby = 64;
public const ushort Emerald = 65;
public const ushort Topaz = 66;
public const ushort Amethyst = 67;
public const ushort Diamond = 68;
public const ushort MushroomPlants = 71;
public const ushort MushroomTrees = 72;
public const ushort HellstoneBrick = 76;
public const ushort Hellforge = 77;
public const ushort MatureHerbs = 83;
public const ushort Lamps = 93;
public const ushort SkullLanterns = 98;
public const ushort Candelabras = 100;
public const ushort Ebonsand = 112;
public const ushort AdamantiteForge = 133;
public const ushort MusicBoxes = 139;
public const ushort Stalactite = 165;
public const ushort ExposedGems = 178;
public const ushort LeafBlock = 192;
public const ushort Crimtane = 204;
public const ushort Chlorophyte = 211;
public const ushort Campfire = 215;
public const ushort HoneyBlock = 229;
public const ushort PlanteraBulb = 238;
public const ushort BubbleMachine = 244;
public const ushort PeaceCandle = 372;
public const ushort LivingMahoganyLeaves = 384;
public const ushort Fireplace = 405;
public const ushort Chimney = 406;
public const ushort FakeContainers = 441;
public const ushort SillyBalloonMachine = 452;
public const ushort SandDrip = 461;
public const ushort DefendersForge = 463;
public const ushort Containers2 = 467;
public const ushort FakeContainers2 = 468;
public const ushort Toilets = 497;
public const ushort FogMachine = 565;
public const ushort AmberStoneBlock = 566;
public const ushort BrazierSuspended = 592;
public const ushort MasterTrophyBase = 617;
public const ushort ManaCrystal = 639;
public const ushort ShadowCandle = 646;
public const ushort LifeCrystalBoulder = 665;
public const ushort PoopBlock = 666;
public const ushort AncientHellstoneBrick = 684;
public const ushort DemonAltarReplica = 695;
public const ushort ShadowOrbsReplica = 696;
public const ushort JunglePlantsEcho = 703;
public const ushort ShimmerDrip = 709;
public const ushort RainbowBoulder = 711;
public const ushort Poulder = 712;
public const ushort StarCloud = 718;

```


---

## 🤖 Assistant · 2026-08-11T02:33:29.834Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Names resolved. Notes:
- 592 = BrazierSuspended
- 565 = FogMachine (gore 1202 = fog puff). Wait, 565 = FogMachine and 497 = Toilets? Hmm, 497 with frameY/40==31 dust 43... Toilets frameY/40==31? Toilet frames are 2x2 40px... Hmm, that seems odd but ok — dust 43 sparkle in toilets? Actually frameY/40==31 → frameY=1240, that's the... hmm. Wait — maybe 497 is not Toilets. But the constant says Toilets = 497. Toilet frameY=1240? Toilet animation frames: Toilet has "flushed" states... The dust 43 with color White scale 0.7 noLight — sparkles. Toilet... hmm, "Toilets" — the sitting/occupied states. Actually I recall Toilet tile has frames for different types; frameY/40==31 is a specific style. It's fine — I'll report as-is.

- 452 = SillyBalloonMachine (gore 907+ = balloon steam puffs). Yes! frameX==0 frameY==0 emits steam puff gore.
- 463 = DefendersForge (smoke/steam dust 16 & 274). frameY==54 top emits steam dust 16; frameY==18 sides emit dust 274 (ember?). OK.
- 238 = PlanteraBulb (dust 168 pink, noGravity, alpha 200).
- 139 = MusicBoxes (gore 570-572 music notes!). Yes — frameX==36 is the open/playing box; notes drift with wind.
- 165 = Stalactite (dust 153 dripping water particle). frameX 162-214 && frameY==72 = dripping stalactite variant. Dust 153 = water drip.
- 42 = HangingLanterns styles: 7 = Cactus lantern (dust 58), 29 = ? dust 59 (that's... lantern styles), 50 = ? dust 57, 51 = ? dust 242 (peace?). Fine.
- 34 = Chandeliers (styles with dust 6 fire, 59 demon torch, 57 ice torch, 242 peace/desert torch).
- 93 = Lamps.
- 98 = SkullLanterns.
- 100 = Candelabras.
- 646 = ShadowCandle — the _rand.Next(2) is dead code (no emission).
- 718 = StarCloud — at night emits fireflies (gore 16/17) and dust 58 (RollLuck(30)).
- 666 = PoopBlock, 712 = Poulder → PooFly particles. 
- 711 = RainbowBoulder → RainbowBoulder particles.
- 617 = MasterTrophyBase → dust 43 colored, only on certain sub-tiles.
- 461 = SandDrip → EmitLiquidDrops sand drip gore 943/1160-1162; 374 = ? (type 716). Wait EmitLiquidDrops cases: 374, 375, 461, and 709. Let me get names for 374, 375, 709. 709 = ShimmerDrip, 461 = SandDrip. 374 and 375 = ? probably "LavaDrip"? Hmm, 373/374/375... Let me look up. Also check which tiles call EmitLiquidDrops.

- 192 = LeafBlock (leaf gore 910), 384 = LivingMahoganyLeaves (gore 914).
- 215 = Campfire? Wait — 215 = Campfire, and 592 = BrazierSuspended? But the 215 block (dust 31 smoke rising from top) has frameY==0 && frameY<36 — Campfire. And 592 frameY==18 — suspended brazier. Hmm wait, actually 215 = Campfire is right.

Hmm wait, the user said "candle 33, water candle 49, peace candle 372, lava lamps/volcano 593/594, tiki torch". Note 33 Candles isn't in this method — maybe handled elsewhere (drawData.typeCache == 33?). Let me search for 33 and 593/594 dust emission elsewhere — they were in the light-drawing section (2716-2724 mention 613/614/593/594 — those are light checks). Candle particles might be in the flame drawing. Let me grep for "33" checks near Dust. Actually the user says they already have those; skip detail but list line numbers. There are no Dust.NewDust for 33/593/594 in this file apparently (grep list showed none). Let me double check by searching "typeCache == 33" and "tileFrameX == 0" patterns.

Also 51 cobweb and 229 honey: line 4491 mentions typeCache == 51 || 229 but that's danger flag, not particles. So no ambient particles for cobweb/honey in this file.

Now get names 374, 375, 613, 614, 593, 594, 33, 548, 518, 72, 314, 171, 149, 300-306, 286, 582, 391, 619, 270, 271, 581, 316-318, 85, 356, 663 for the non-dust sections (not needed much).

Let me get 374/375 names and check where EmitLiquidDrops is called, and search Main.cs for tile ambient dust.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:31.005Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -oE \"public const ushort [A-Za-z0-9]+ = (33|51|229|374|375|518|546|593|594|613|614|72|314|171|85|583);\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs; grep -n \"EmitLiquidDrops\\|DrawTiles_EmitParticles\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "description": "Get remaining tile names and method call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:31.061Z

**📎 ToolResult**

```
public const ushort Candles = 33;
public const ushort Cobweb = 51;
public const ushort MushroomTrees = 72;
public const ushort Tombstones = 85;
public const ushort ChristmasTree = 171;
public const ushort HoneyBlock = 229;
public const ushort MinecartTrack = 314;
public const ushort LavaDrip = 374;
public const ushort HoneyDrip = 375;
public const ushort LilyPad = 518;
public const ushort Grate = 546;
public const ushort TreeTopaz = 583;
public const ushort VolcanoSmall = 593;
public const ushort VolcanoLarge = 594;
public const ushort PottedLavaPlants = 613;
public const ushort PottedLavaPlantTendrils = 614;
698:						EmitLiquidDrops(i, j, tile, type);
978:				DrawTiles_EmitParticles(tileY, tileX, tileDrawInfo.tileCache, tileDrawInfo.typeCache, tileDrawInfo.tileFrameX, tileDrawInfo.tileFrameY, tileDrawInfo.tileLight);
6795:	private void DrawTiles_EmitParticles(int j, int i, Tile tileCache, ushort typeCache, short tileFrameX, short tileFrameY, Color tileLight)
7714:	private void EmitLiquidDrops(int j, int i, Tile tileCache, ushort typeCache)
8506:				DrawTiles_EmitParticles(y, x, tile, type, tileFrameX, tileFrameY, tileLight);
8564:				DrawTiles_EmitParticles(y, x, tile, type, tileFrameX, tileFrameY, tileLight);
9144:					DrawTiles_EmitParticles(j, i, tile, type2, tileFrameX, tileFrameY, tileLight);
9661:					DrawTiles_EmitParticles(j, i, tile2, type2, tileFrameX, tileFrameY, tileLight);

```


---

## 🤖 Assistant · 2026-08-11T02:33:31.339Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Dust.NewDust\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head -60",
 "description": "Find Dust.NewDust in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:31.389Z

**📎 ToolResult**

```
13024:					int num10 = Dust.NewDust(new Vector2(num6, num7), 10, 10, 76);
13180:				int num3 = Dust.NewDust(new Vector2(effectRect.X, effectRect.Y), effectRect.Width, effectRect.Height, 159);
13200:				int num12 = Dust.NewDust(new Vector2(effectRect.X, effectRect.Y), effectRect.Width, effectRect.Height, 164);
13218:				Main.dust[Dust.NewDust(new Vector2(effectRect.X, effectRect.Y), effectRect.Width, effectRect.Height, 58, 0f, 0f, 150, Microsoft.Xna.Framework.Color.GhostWhite, 1.2f)].velocity *= 0.5f;
13228:				int num6 = Dust.NewDust(new Vector2(effectRect.X, effectRect.Y), effectRect.Width, effectRect.Height, 180);
13263:				Dust obj4 = Main.dust[Dust.NewDust(effectRect.TopLeft(), effectRect.Width, effectRect.Height, 263)];
13279:				Dust obj3 = Dust.NewDustDirect(position, effectRect.Width, effectRect.Height + 24, Dust.dustWater());
13297:				Dust obj5 = Dust.NewDustDirect(position2, effectRect.Width, effectRect.Height + 24, 35);
13330:				Dust dust = Dust.NewDustDirect(effectRect.TopLeft(), effectRect.Width, effectRect.Height, 267, 0f, 0f, 127, newColor);
13378:				Dust obj = Dust.NewDustPerfect(rand.NextVector2FromRectangle(effectRect), 267);
13392:				int num = Dust.NewDust(rand.NextVector2FromRectangle(effectRect), 2, 2, 27, 0f, 0f, 100, default(Microsoft.Xna.Framework.Color), rand.Next(1, 3));
22588:					int num17 = Dust.NewDust(new Vector2(vector5.X, vector5.Y), 30, 10, 5, num14 * 0.02f, num15 * 0.02f, 0, default(Microsoft.Xna.Framework.Color), 2f);
22671:					int num24 = Dust.NewDust(new Vector2(vector7.X, vector7.Y), 30, 10, 6, num21 * 0.02f, num22 * 0.02f, 0, default(Microsoft.Xna.Framework.Color), 2.5f);
24361:									dust[Dust.NewDust(vector26 + vector27, 0, 0, 6)].noGravity = true;
24373:									dust[Dust.NewDust(vector26, 0, 0, 6)].noGravity = true;
24377:									dust[Dust.NewDust(center2, 0, 0, 6)].noGravity = true;
24381:									dust[Dust.NewDust(vector26 + new Vector2(0f, num97).RotatedBy(vector27.ToRotation() - num102 - MathF.PI / 2f), 0, 0, 6)].noGravity = true;
27282:							Dust obj = Dust.NewDustDirect(vector7 - vector8 / 2f, (int)vector8.X, (int)vector8.Y, 4, 0f, 0f, 50, new Microsoft.Xna.Framework.Color(245, 200, 30, 155), 0.7f);
27285:							Dust.NewDustDirect(vector7 - vector8 / 2f, (int)vector8.X, (int)vector8.Y, 4, 0f, 0f, 50, new Microsoft.Xna.Framework.Color(245, 200, 30, 155), 0.6f).velocity *= 2f;
38100:			int num3 = Dust.NewDust(item.position, item.width, item.height, type, 0f, 0f, alpha, newColor, scale2);
57132:						int num21 = Dust.NewDust(new Vector2(j * 16, vector2.Y - 2f), 16, 8, 43, 0f, 0f, 254, newColor, 0.75f);
57155:							Dust.NewDust(new Vector2(j * 16, i * 16), 16, 16, 35);
57159:							int num22 = Dust.NewDust(new Vector2(j * 16, (float)(i * 16) + num11 * 2f - 8f), 16, 8, 35, 0f, 0f, 50, default(Microsoft.Xna.Framework.Color), 1.5f);

```


---

## 🤖 Assistant · 2026-08-11T02:33:34.165Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The Main.cs entries: 57132, 57155-57159 look like they could be near tile loops (uses j*16, i*16 = tile coords). Let me look at the context around 57080-57180 in Main.cs to see if it's tile ambient (this looks like it could be in a "UpdateTileDust" or in the block swap / tile destruction). Let me check.

Also 13024 area might be tile-related? Let me check context for each candidate quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:34.605Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '57060,57170p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Read Main.cs context around tile dust lines"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:34.649Z

**📎 ToolResult**

```
						}
						else if (tile[j, i - 1].liquid > 0)
						{
							vector2 = new Vector2(j * 16, i * 16 + 4);
							value = new Microsoft.Xna.Framework.Rectangle(0, 4, 16, 12);
							num17 = 0.5f;
						}
						else if (tile[j, i + 1].liquid > 0)
						{
							vector2 = new Vector2(j * 16, i * 16 + (int)num11 * 2 + (int)num18 * 2);
							value = new Microsoft.Xna.Framework.Rectangle(0, 4, 16, 16 - (int)num11 * 2);
						}
						else
						{
							vector2 = new Vector2(j * 16 + (int)num19, i * 16 + (int)num19 * 2 + (int)num18 * 2);
							value = new Microsoft.Xna.Framework.Rectangle(0, 4, 16 - (int)num19 * 2, 16 - (int)num19 * 2);
						}
					}
					else
					{
						num17 = 0.5f;
						value = new Microsoft.Xna.Framework.Rectangle(0, 4, 16, 16 - (int)num11 * 2 + (int)num18 * 2);
					}
				}
				else if (tile[j, i - 1].liquid > 32)
				{
					value = new Microsoft.Xna.Framework.Rectangle(0, 4, value.Width, value.Height);
				}
				else if (num11 < 1f && tile[j, i - 1].nactive() && tileSolid[tile[j, i - 1].type] && !tileSolidTop[tile[j, i - 1].type])
				{
					vector2 = new Vector2(j * 16, i * 16);
					value = new Microsoft.Xna.Framework.Rectangle(0, 4, 16, 16);
				}
				else
				{
					for (int k = i + 1; k < i + 6 && (!tile[j, k].nactive() || !tileSolid[tile[j, k].type] || tileSolidTop[tile[j, k].type]); k++)
					{
						if (tile[j, k].liquid < 200)
						{
							flag2 = false;
							break;
						}
					}
					if (!flag2)
					{
						num17 = 0.5f;
						value = new Microsoft.Xna.Framework.Rectangle(0, 4, 16, 16);
					}
					else if (tile[j, i - 1].liquid > 0)
					{
						value = new Microsoft.Xna.Framework.Rectangle(0, 2, value.Width, value.Height);
					}
				}
				if ((color.R > 20 || color.B > 20 || color.G > 20) && value.Y < 4)
				{
					int num20 = color.R;
					if (color.G > num20)
					{
						num20 = color.G;
					}
					if (color.B > num20)
					{
						num20 = color.B;
					}
					num20 /= 30;
					if (rand.Next(20000) < num20)
					{
						Microsoft.Xna.Framework.Color newColor = new Microsoft.Xna.Framework.Color(255, 255, 255);
						if (tile[j, i].honey())
						{
							newColor = new Microsoft.Xna.Framework.Color(255, 255, 50);
						}
						int num21 = Dust.NewDust(new Vector2(j * 16, vector2.Y - 2f), 16, 8, 43, 0f, 0f, 254, newColor, 0.75f);
						dust[num21].velocity *= 0f;
					}
				}
				if (tile[j, i].honey())
				{
					num17 *= 1.6f;
					if (num17 > 1f)
					{
						num17 = 1f;
					}
				}
				if (tile[j, i].lava())
				{
					num17 *= 1.8f;
					if (num17 > 1f)
					{
						num17 = 1f;
					}
					if (FocusHelper.AllowMiscDustEffects && Dust.lavaBubbles < 200)
					{
						if (tile[j, i].liquid > 200 && rand.Next(700) == 0)
						{
							Dust.NewDust(new Vector2(j * 16, i * 16), 16, 16, 35);
						}
						if (value.Y == 0 && rand.Next(350) == 0)
						{
							int num22 = Dust.NewDust(new Vector2(j * 16, (float)(i * 16) + num11 * 2f - 8f), 16, 8, 35, 0f, 0f, 50, default(Microsoft.Xna.Framework.Color), 1.5f);
							dust[num22].velocity *= 0.8f;
							dust[num22].velocity.X *= 2f;
							dust[num22].velocity.Y -= (float)rand.Next(1, 7) * 0.1f;
							if (rand.Next(10) == 0)
							{
								dust[num22].velocity.Y *= rand.Next(2, 5);
							}
							dust[num22].noGravity = true;
						}
					}
				}

```


---

## 🤖 Assistant · 2026-08-11T02:33:37.645Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
That's liquid surface sparkles/bubbles, not tile ambient. Other Main.cs Dust hits (13024, 13180+, 22588, etc.) — 13024 uses num6/num7 not tile coords; 13180-13392 are tile "effects" rectangle (probably tile "TileEffects" e.g. moondial? Actually they're in a method with effectRect). Let me quickly check 13150-13200 and 13370-13400 context, and 13000-13030, 22580-22680, 24350-24390, 27270-27290 to see if they are per-tile ambient.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:38.210Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '12990,13030p;13160,13190p;13360,13400p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Check Main.cs dust contexts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:38.258Z

**📎 ToolResult**

```
		{
			try
			{
				if (!((float)snowDust < (float)num4 * (gfxQuality / 2f + 0.5f) + (float)num4 * 0.1f))
				{
					break;
				}
				if (!(rand.NextFloat() < num))
				{
					continue;
				}
				int num6 = rand.Next((int)scaledSize.X + 1500) - 750;
				int num7 = (int)scaledPosition.Y - rand.Next(50);
				if (player[myPlayer].velocity.Y > 0f)
				{
					num7 -= (int)player[myPlayer].velocity.Y;
				}
				if (rand.Next(5) == 0)
				{
					num6 = rand.Next(500) - 500;
				}
				else if (rand.Next(5) == 0)
				{
					num6 = rand.Next(500) + (int)scaledSize.X;
				}
				if (num6 < 0 || (float)num6 > scaledSize.X)
				{
					num7 += rand.Next((int)((double)scaledSize.Y * 0.8)) + (int)((double)scaledSize.Y * 0.1);
				}
				num6 += (int)scaledPosition.X;
				int num8 = num6 / 16;
				int num9 = num7 / 16;
				if (WorldGen.InWorld(num8, num9) && tile[num8, num9] != null && !tile[num8, num9].nactive() && tile[num8, num9].wall == 0)
				{
					int num10 = Dust.NewDust(new Vector2(num6, num7), 10, 10, 76);
					dust[num10].scale += cloudAlpha * 0.2f;
					dust[num10].velocity.Y = 3f + (float)rand.Next(30) * 0.1f;
					dust[num10].velocity.Y *= dust[num10].scale;
					if (!raining)
					{
						dust[num10].velocity.X = windSpeedCurrent + (float)rand.Next(-10, 10) * 0.1f;
		{
			cloudBGActive = rand.Next(num2, num2 * 4);
			if (netMode == 2)
			{
				NetMessage.SendData(7);
			}
		}
	}

	public static void TeleportEffect(Microsoft.Xna.Framework.Rectangle effectRect, int Style, int extraInfo = 0, float dustCountMult = 1f, TeleportationSide side = TeleportationSide.Entry, Vector2 otherPosition = default(Vector2))
	{
		switch (Style)
		{
		case 0:
		{
			SoundEngine.PlaySound(SoundID.Item6, effectRect.X + effectRect.Width / 2, effectRect.Y + effectRect.Height / 2);
			int num2 = effectRect.Width * effectRect.Height / 5;
			num2 = (int)((float)num2 * dustCountMult);
			for (int j = 0; j < num2; j++)
			{
				int num3 = Dust.NewDust(new Vector2(effectRect.X, effectRect.Y), effectRect.Width, effectRect.Height, 159);
				Main.dust[num3].scale = (float)rand.Next(20, 70) * 0.01f;
				if (j < 10)
				{
					Main.dust[num3].scale += 0.25f;
				}
				if (j < 5)
				{
					Main.dust[num3].scale += 0.25f;
				}
			}
		{
			for (int k = 0; k < 50; k++)
			{
				int num4 = rand.Next(4);
				Microsoft.Xna.Framework.Color color = Microsoft.Xna.Framework.Color.Green;
				switch (num4)
				{
				case 0:
				case 1:
					color = new Microsoft.Xna.Framework.Color(100, 255, 100);
					break;
				case 2:
					color = Microsoft.Xna.Framework.Color.Yellow;
					break;
				case 3:
					color = Microsoft.Xna.Framework.Color.White;
					break;
				}
				Dust obj = Dust.NewDustPerfect(rand.NextVector2FromRectangle(effectRect), 267);
				obj.noGravity = true;
				obj.color = color;
				obj.velocity *= 2f;
				obj.scale = 0.8f + rand.NextFloat() * 0.6f;
				obj.fadeIn = 0.5f;
			}
			break;
		}
		case 13:
		{
			SoundEngine.PlaySound(SoundID.Item8, effectRect.Center.ToVector2());
			for (int i = 0; i < 21; i++)
			{
				int num = Dust.NewDust(rand.NextVector2FromRectangle(effectRect), 2, 2, 27, 0f, 0f, 100, default(Microsoft.Xna.Framework.Color), rand.Next(1, 3));
				Main.dust[num].velocity *= 1.75f;
				if (i % 3 == 0)
				{
					Main.dust[num].velocity *= 1.5f;
				}
				Main.dust[num].noLightEmittance = true;
				Main.dust[num].noGravity = true;
			}

```


---

## 🤖 Assistant · 2026-08-11T02:33:38.741Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '22570,22595p;22655,22680p;24345,24390p;27270,27290p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Check more Main.cs dust contexts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:38.784Z

**📎 ToolResult**

```
				Microsoft.Xna.Framework.Color color5 = Lighting.GetColor((int)vector5.X / 16, (int)(vector5.Y / 16f));
				if (rCurrentNPC.localAI[3] == 1f)
				{
					mySpriteBatch.Draw(TextureAssets.BoneArm3.Value, new Vector2(vector5.X - screenPos.X, vector5.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.BoneArm.Width(), TextureAssets.BoneArm.Height()), color5, rotation5, new Vector2((float)TextureAssets.BoneArm.Width() * 0.5f, (float)TextureAssets.BoneArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
				}
				else
				{
					mySpriteBatch.Draw(TextureAssets.BoneArm.Value, new Vector2(vector5.X - screenPos.X, vector5.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.BoneArm.Width(), TextureAssets.BoneArm.Height()), color5, rotation5, new Vector2((float)TextureAssets.BoneArm.Width() * 0.5f, (float)TextureAssets.BoneArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
				}
				if (j == 0)
				{
					vector5.X += num14 * num16 / 2f;
					vector5.Y += num15 * num16 / 2f;
				}
				else if (FocusHelper.AllowMiscDustEffects)
				{
					vector5.X += num14 * num16 - 16f;
					vector5.Y += num15 * num16 - 6f;
					int num17 = Dust.NewDust(new Vector2(vector5.X, vector5.Y), 30, 10, 5, num14 * 0.02f, num15 * 0.02f, 0, default(Microsoft.Xna.Framework.Color), 2f);
					dust[num17].noGravity = true;
				}
			}
		}
		if (rCurrentNPC.aiStyle == 47)
		{
			float scale = rCurrentNPC.scale;
					num23 = 60f / num23;
					vector7.X += num21 * num23;
					vector7.Y += num22 * num23;
				}
				float rotation7 = (float)Math.Atan2(num22, num21) - 1.57f;
				Microsoft.Xna.Framework.Color color7 = Lighting.GetColor((int)vector7.X / 16, (int)(vector7.Y / 16f));
				mySpriteBatch.Draw(TextureAssets.BoneArm2.Value, new Vector2(vector7.X - screenPos.X, vector7.Y - screenPos.Y), new Microsoft.Xna.Framework.Rectangle(0, 0, TextureAssets.BoneArm.Width(), TextureAssets.BoneArm.Height()), color7, rotation7, new Vector2((float)TextureAssets.BoneArm.Width() * 0.5f, (float)TextureAssets.BoneArm.Height() * 0.5f), 1f, SpriteEffects.None, 0f);
				if (k == 0)
				{
					vector7.X += num21 * num23 / 2f;
					vector7.Y += num22 * num23 / 2f;
				}
				else if (FocusHelper.AllowMiscDustEffects)
				{
					vector7.X += num21 * num23 - 16f;
					vector7.Y += num22 * num23 - 6f;
					int num24 = Dust.NewDust(new Vector2(vector7.X, vector7.Y), 30, 10, 6, num21 * 0.02f, num22 * 0.02f, 0, default(Microsoft.Xna.Framework.Color), 2.5f);
					dust[num24].noGravity = true;
				}
			}
		}
		if (type == 693)
		{
			float num25 = rCurrentNPC.localAI[1];
			float num26 = num25 - 60f;
			float num27 = rCurrentNPC.localAI[0];
							Vector2 vector25 = new Vector2((!flag9) ? 1 : (-1), 1f);
							int num100 = -1;
							for (int num101 = 0; num101 < maxNPCs; num101++)
							{
								if (npc[num101].active && npc[num101].type == 397 && npc[num101].ai[2] == (float)num99 && npc[num101].ai[3] == (float)rCurrentNPC.whoAmI)
								{
									num100 = num101;
									break;
								}
							}
							if (num100 != -1)
							{
								Vector2 vector26 = center2 + vector22 * vector25;
								Vector2 vector27 = (npc[num100].Center + vector24 - vector26) * num98;
								if (flag8)
								{
									dust[Dust.NewDust(vector26 + vector27, 0, 0, 6)].noGravity = true;
								}
								float num102 = (float)Math.Acos(vector27.Length() / num97) * (0f - vector25.X);
								SpriteEffects effects2 = ((!flag9) ? SpriteEffects.FlipHorizontally : SpriteEffects.None);
								Vector2 origin14 = vector23;
								if (!flag9)
								{
									origin14.X = (float)value29.Width - origin14.X;
								}
								mySpriteBatch.Draw(value29, vector26 - screenPos, null, alpha5, vector27.ToRotation() - num102 - MathF.PI / 2f, origin14, 1f, effects2, 0f);
								if (flag8)
								{
									dust[Dust.NewDust(vector26, 0, 0, 6)].noGravity = true;
								}
								if (flag8)
								{
									dust[Dust.NewDust(center2, 0, 0, 6)].noGravity = true;
								}
								if (flag8)
								{
									dust[Dust.NewDust(vector26 + new Vector2(0f, num97).RotatedBy(vector27.ToRotation() - num102 - MathF.PI / 2f), 0, 0, 6)].noGravity = true;
								}
							}
						}
						mySpriteBatch.Draw(value30, center2 - screenPos, null, alpha5, 0f, origin12, 1f, SpriteEffects.None, 0f);
						mySpriteBatch.Draw(value30, center2 - screenPos, null, alpha5, 0f, origin13, 1f, SpriteEffects.FlipHorizontally, 0f);
						mySpriteBatch.Draw(value28, center2 - screenPos, null, alpha5, 0f, new Vector2(112f, 101f), 1f, SpriteEffects.None, 0f);
						mySpriteBatch.Draw(value27, center2 - screenPos, rCurrentNPC.frame, alpha5, 0f, rCurrentNPC.frame.Size() / 2f, 1f, SpriteEffects.None, 0f);
						return;
					}
				bool flag = player.HeldItem.type == 353 && player.direction == Math.Sign(n.Center.X - player.Center.X);
				float num19 = player.Hitbox.Distance(n.Center);
				float num20 = n.localAI[3];
				if (num19 < 46f && flag)
				{
					n.localAI[3] = 1f;
					if (n.localAI[3] != num20)
					{
						Vector2 vector7 = n.Center + new Vector2(n.spriteDirection * 30, -6f);
						Vector2 vector8 = new Vector2(10f, 10f);
						for (int i = 0; i < 30; i++)
						{
							Dust obj = Dust.NewDustDirect(vector7 - vector8 / 2f, (int)vector8.X, (int)vector8.Y, 4, 0f, 0f, 50, new Microsoft.Xna.Framework.Color(245, 200, 30, 155), 0.7f);
							obj.noGravity = true;
							obj.velocity *= 1f;
							Dust.NewDustDirect(vector7 - vector8 / 2f, (int)vector8.X, (int)vector8.Y, 4, 0f, 0f, 50, new Microsoft.Xna.Framework.Color(245, 200, 30, 155), 0.6f).velocity *= 2f;
						}
					}
				}
				else if (n.localAI[3] == 1f)
				{

```


---

## 🤖 Assistant · 2026-08-11T02:33:46.920Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
None of these Main.cs Dust calls are tile-ambient; they're snow/weather, teleport effects, NPC drawing (bone arms, Target dummy with spear), item pickup. So the only "tile-adjacent" Main.cs dust is the liquid surface sparkle (57132) and lava bubbles (57155, 57159), which are liquid not tile.

Now I should also verify whether there's a "DrawTiles_EmitParticles" caller section that includes the Candles (33) emission — user says they already have candle 33 etc. In this file, grep showed no `typeCache == 33` check. So candle particles (33) aren't in this method — perhaps they're in a different file (TileDrawing? Main?). Actually let me grep for "== 33" in TileDrawing.cs. Also check for "== 593"/"594" emission which the user mentioned as "lava lamps/volcano 593/594". Line 2724-2728 mention them but in light. Hmm — maybe in DrawTiles_EmitParticles they are handled via `TileID.Sets.SetsNewTiles`... no. Let me grep for "593" and "33" dust. Actually the lava-lamp emission could be in a different method. Let me search for "PottedLavaPlants" or "613" dust emission. Line 2716-2720 handle 613/614 — light only. Perhaps the emission for lava lamp is handled by "TileID.Sets.Candle" loop... Let me grep for "TorchID.Dust" or "Candle" in the file to check.

Actually, the user said "Known ones I already have (skip detail for these but list line numbers): torch (type 4), candle 33, water candle 49, peace candle 372, lava lamps/volcano 593/594, tiki torch etc." — they want line numbers. Candles 33 might not exist in this method in this decompiled version. Let me verify with grep for 593/594/33 emission.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:47.727Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"== 33\\b\\|= 33;\\|33 &&\\|593\\|594\\|613\\|614\\|Tiki\\|torch\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | head -40",
 "description": "Search for candle 33 / volcano 593/594 references"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:47.771Z

**📎 ToolResult**

```
2716:		if (drawData.typeCache == 613)
2720:		if (drawData.typeCache == 614)
2724:		if (drawData.typeCache == 593)
2728:		if (drawData.typeCache == 594)
5343:		case 613:
5356:		case 614:
5536:		case 593:
5557:		case 594:
6359:				if (num65 == 33)
6372:				if (num65 == 33)
6438:				if (num65 == 33)
6473:			if (num65 == 33)

```


---

## 🤖 Assistant · 2026-08-11T02:33:54.509Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Lines 6351-6500 have num65 == 33 checks. Let me read that region (6300-6520) — it's the flame drawing for candles; dust may be emitted there. Let me read.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:33:54.510Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs",
 "limit": 230,
 "offset": 6300
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:33:54.529Z

**📎 ToolResult**

```
6300			case 89:
6301			{
6302				int num65 = tileFrameX / 54;
6303				int num68 = tileFrameX / 1998;
6304				addFrX -= 1998 * num68;
6305				addFrY += 36 * num68;
6306				if (num65 == 29)
6307				{
6308					glowTexture = TextureAssets.GlowMask[66].Value;
6309					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6310					glowColor = _martianGlow;
6311				}
6312				if (num65 == 30)
6313				{
6314					glowTexture = TextureAssets.GlowMask[123].Value;
6315					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6316					glowColor = _meteorGlow;
6317				}
6318				break;
6319			}
6320			case 100:
6321				if (tileFrameX / 36 == 0)
6322				{
6323					int num65 = tileFrameY / 36;
6324					if (num65 == 27)
6325					{
6326						glowTexture = TextureAssets.GlowMask[68].Value;
6327						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 36, tileWidth, tileHeight);
6328						glowColor = _martianGlow;
6329					}
6330				}
6331				break;
6332			case 33:
6333				if (tileFrameX / 18 == 0)
6334				{
6335					int num65 = tileFrameY / 22;
6336					if (num65 == 26)
6337					{
6338						glowTexture = TextureAssets.GlowMask[61].Value;
6339						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 22, tileWidth, tileHeight);
6340						glowColor = _martianGlow;
6341					}
6342				}
6343				break;
6344			case 15:
6345			case 497:
6346			{
6347				int num65 = tileFrameY / 40;
6348				int num72 = num65 / 51;
6349				addFrY -= 2040 * num72;
6350				addFrX += 36 * num72;
6351				if (typeCache == 15)
6352				{
6353					if (num65 == 32)
6354					{
6355						glowTexture = TextureAssets.GlowMask[54].Value;
6356						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 40, tileWidth, tileHeight);
6357						glowColor = _martianGlow;
6358					}
6359					if (num65 == 33)
6360					{
6361						glowTexture = TextureAssets.GlowMask[116].Value;
6362						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 40, tileWidth, tileHeight);
6363						glowColor = _meteorGlow;
6364					}
6365				}
6366				break;
6367			}
6368			case 34:
6369				if (tileFrameX / 54 == 0)
6370				{
6371					int num65 = tileFrameY / 54;
6372					if (num65 == 33)
6373					{
6374						glowTexture = TextureAssets.GlowMask[55].Value;
6375						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 54, tileWidth, tileHeight);
6376						glowColor = _martianGlow;
6377					}
6378				}
6379				break;
6380			case 21:
6381			case 467:
6382			{
6383				int num65 = tileFrameX / 36;
6384				if (num65 == 48)
6385				{
6386					glowTexture = TextureAssets.GlowMask[56].Value;
6387					glowSourceRect = new Rectangle(tileFrameX % 36, tileFrameY, tileWidth, tileHeight);
6388					glowColor = _martianGlow;
6389				}
6390				if (num65 == 49)
6391				{
6392					glowTexture = TextureAssets.GlowMask[117].Value;
6393					glowSourceRect = new Rectangle(tileFrameX % 36, tileFrameY, tileWidth, tileHeight);
6394					glowColor = _meteorGlow;
6395				}
6396				break;
6397			}
6398			case 441:
6399			case 468:
6400			{
6401				int num65 = tileFrameX / 36;
6402				if (num65 == 48)
6403				{
6404					glowTexture = TextureAssets.GlowMask[56].Value;
6405					glowSourceRect = new Rectangle(tileFrameX % 36, tileFrameY, tileWidth, tileHeight);
6406					glowColor = _martianGlow;
6407				}
6408				if (num65 == 49)
6409				{
6410					glowTexture = TextureAssets.GlowMask[117].Value;
6411					glowSourceRect = new Rectangle(tileFrameX % 36, tileFrameY, tileWidth, tileHeight);
6412					glowColor = _meteorGlow;
6413				}
6414				break;
6415			}
6416			case 10:
6417			{
6418				int num65 = tileFrameY / 54;
6419				if (tileFrameX < 54 && num65 == 32)
6420				{
6421					glowTexture = TextureAssets.GlowMask[57].Value;
6422					glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 54, tileWidth, tileHeight);
6423					glowColor = _martianGlow;
6424				}
6425				break;
6426			}
6427			case 11:
6428			{
6429				int num65 = tileFrameY / 54;
6430				if (tileFrameX < 54)
6431				{
6432					if (num65 == 32)
6433					{
6434						glowTexture = TextureAssets.GlowMask[58].Value;
6435						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 54, tileWidth, tileHeight);
6436						glowColor = _martianGlow;
6437					}
6438					if (num65 == 33)
6439					{
6440						glowTexture = TextureAssets.GlowMask[119].Value;
6441						glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 54, tileWidth, tileHeight);
6442						glowColor = _meteorGlow;
6443					}
6444				}
6445				break;
6446			}
6447			case 88:
6448			{
6449				int num65 = tileFrameX / 54;
6450				int num74 = tileFrameX / 1998;
6451				addFrX -= 1998 * num74;
6452				addFrY += 36 * num74;
6453				if (num65 == 24)
6454				{
6455					glowTexture = TextureAssets.GlowMask[59].Value;
6456					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6457					glowColor = _martianGlow;
6458				}
6459				if (num65 == 25)
6460				{
6461					glowTexture = TextureAssets.GlowMask[120].Value;
6462					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6463					glowColor = _meteorGlow;
6464				}
6465				break;
6466			}
6467			case 42:
6468			{
6469				int num65 = tileFrameY / 36;
6470				int num73 = tileFrameY / 2016;
6471				addFrY -= 2016 * num73;
6472				addFrX += 36 * num73;
6473				if (num65 == 33)
6474				{
6475					glowTexture = TextureAssets.GlowMask[63].Value;
6476					glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 36, tileWidth, tileHeight);
6477					glowColor = _martianGlow;
6478				}
6479				break;
6480			}
6481			case 87:
6482			{
6483				int num65 = tileFrameX / 54;
6484				int num71 = tileFrameX / 1998;
6485				addFrX -= 1998 * num71;
6486				addFrY += 36 * num71;
6487				if (num65 == 26)
6488				{
6489					glowTexture = TextureAssets.GlowMask[64].Value;
6490					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6491					glowColor = _martianGlow;
6492				}
6493				if (num65 == 27)
6494				{
6495					glowTexture = TextureAssets.GlowMask[121].Value;
6496					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6497					glowColor = _meteorGlow;
6498				}
6499				break;
6500			}
6501			case 14:
6502			{
6503				int num65 = tileFrameX / 54;
6504				if (num65 == 31)
6505				{
6506					glowTexture = TextureAssets.GlowMask[67].Value;
6507					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6508					glowColor = _martianGlow;
6509				}
6510				if (num65 == 32)
6511				{
6512					glowTexture = TextureAssets.GlowMask[124].Value;
6513					glowSourceRect = new Rectangle(tileFrameX % 54, tileFrameY, tileWidth, tileHeight);
6514					glowColor = _meteorGlow;
6515				}
6516				break;
6517			}
6518			case 93:
6519			{
6520				int num65 = tileFrameY / 54;
6521				int num70 = tileFrameY / 1998;
6522				addFrY -= 1998 * num70;
6523				addFrX += 36 * num70;
6524				tileTop += 2;
6525				if (num65 == 27)
6526				{
6527					glowTexture = TextureAssets.GlowMask[62].Value;
6528					glowSourceRect = new Rectangle(tileFrameX, tileFrameY % 54, tileWidth, tileHeight);
6529					glowColor = _martianGlow;

```


---

## 🤖 Assistant · 2026-08-11T02:34:05.173Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
That's the glowmask region, no dust for candles. So in this decompile, Candles (33) have no ambient dust emission in DrawTiles_EmitParticles. Interesting — maybe candles emit particles elsewhere (Main.cs or via TileID.Sets?). Actually vanilla Terraria candle particles: I recall candles do not emit dust in 1.4; only torch/candelabra/etc. Actually the vanilla DrawTiles_EmitParticles in 1.4.4 includes: 4 torches, 93 lamps, 100 candelabra, 98 skull lantern, 49 water candle, 372 peace candle, 34 chandelier... and 33 candles? Hmm. The decompiled code above shows the chain at 7435 (if 22 ... else if 23/24/32 ... ) which in vanilla is: typeCache == 22 (Demonite), 23 corrupt grass... Actually vanilla 1.4 code:

```
if (typeCache == 22 && _rand.Next(400) == 0) Dust 14   // Demonite sparkle
else if ((typeCache == 23 || typeCache == 24 || typeCache == 32) && _rand.Next(500) == 0) Dust 14 // corrupt grass/plants/thorns sparkle
else if (typeCache == 25 && _rand.Next(700)==0) // Ebonstone
else if (typeCache == 112 && _rand.Next(700)==0) // Ebonsand
else if ((31||696) && rand(20)) shadow orb + replica: frameX>=36 → dust 5 (shadow), else dust 14
else if ((26||695) && rand(20)) demon altar + replica: frameX>=54 → dust 5 scale 1.5 nogravity, else dust 14
else if ((71||72) && color()==0 && rand(500)) dust 41 (glowing mushroom sparkles)
else if ((17||77||133) && rand(40)) furnace/hellforge/adamantite forge: frameX==18&&frameY==18 (lit) → dust 6 smoke/ember above
else if (405 && rand(20)) fireplace lit → dust 6 (24x10 area)
else if (37 && rand(250)) meteorite dust 6
else if ((58||76||684) && rand(250)) hellstone, hellstone brick, ancient hellstone brick dust 6 noLight
else if (61||703) jungle plants / echo: frameX==144 && rand(60) → dust 44 (jungle spores)
else if (Main.tileShine>0) → gem sparkles (43) etc.
else if tileSolid && shimmerAlpha → shimmer dust 43
```

Good — matches.

Now, EmitLiquidDrops: called at line 698 in some UpdateTileDust-like method with types 374 (LavaDrip), 375 (HoneyDrip), 461 (SandDrip), 709 (ShimmerDrip) — note 374/375/461/709 are not "tiles" visually active but they're the drip tiles. EmitLiquidDrops also called for regular tiles? Let me check line ~690 context to see the calling condition. Let me read lines 660-710 of TileDrawing.cs.
````

</details>


---

## 🤖 Assistant · 2026-08-11T02:34:05.913Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '640,700p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs; grep -n \"private void\\|public void\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs | awk -F: '$1<700' | tail -5",
 "description": "Read EmitLiquidDrops call site context"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:34:23.580Z

**📎 ToolResult**

```
						continue;
					case 530:
						if (frameX < 270)
						{
							if (frameX % 54 == 0 && frameY == 0)
							{
								AddSpecialPoint(j, i, TileCounterType.MultiTileGrass);
							}
							continue;
						}
						break;
					case 705:
						if (frameX % 486 < 270)
						{
							if (frameX % 54 == 0 && frameY % 36 == 0)
							{
								AddSpecialPoint(j, i, TileCounterType.MultiTileGrass);
							}
							continue;
						}
						break;
					case 485:
					case 489:
					case 490:
						if (frameY == 0 && frameX % 36 == 0)
						{
							AddSpecialPoint(j, i, TileCounterType.MultiTileGrass);
						}
						continue;
					case 521:
					case 522:
					case 523:
					case 524:
					case 525:
					case 526:
					case 527:
						if (frameY == 0 && frameX % 36 == 0)
						{
							AddSpecialPoint(j, i, TileCounterType.MultiTileGrass);
						}
						continue;
					case 493:
						if (frameY == 0 && frameX % 18 == 0)
						{
							AddSpecialPoint(j, i, TileCounterType.MultiTileGrass);
						}
						continue;
					case 519:
						if (frameX / 18 <= 4)
						{
							AddSpecialPoint(j, i, TileCounterType.MultiTileGrass);
						}
						continue;
					case 373:
					case 374:
					case 375:
					case 461:
					case 709:
						EmitLiquidDrops(i, j, tile, type);
						continue;
					case 491:
409:	private void DrawNature(Texture2D texture, Vector2 position, Rectangle sourceRectangle, Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth, SideFlags seams = SideFlags.None)
414:	private void DrawNatureGlowmask(Texture2D texture, Vector2 position, Rectangle? sourceRectangle, Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth)
419:	public void PostDrawTiles(bool solidLayer)
449:	public void DrawLiquidBehindTiles(int waterStyleOverride = -1)
470:	public void Draw(bool solidLayer, bool intoRenderTargets, int waterStyleOverride = -1)

```


---

## 🤖 Assistant · 2026-08-11T02:35:04.128Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good: drip tiles 373 (DripTimer? = WaterDrip), 374 LavaDrip, 375 HoneyDrip, 461 SandDrip, 709 ShimmerDrip call EmitLiquidDrops. Get name for 373 too.

Let me check 373 name. Also verify style names for HangingLanterns (42) styles 7/29/50/51 — not needed in detail; dust IDs suffice.

Also need to double-check the pre-visibility block 238 PlanteraBulb — that's in the visible section (after `if (!flag) return;` at 7067). Yes 238 is after the return so visible-only.

Now I have everything. Let me also confirm tile names for the lantern styles 7/29/50/51? Not necessary — I'll describe as lantern styles.

One more: the 165 Stalactite block — frameY==72 && frameX 162-214 is the water-dripping stalactite frame; dust 153 is the water drip dust. Good.

Also line 7545: gem sparkle gate conditions:
- type 21 (Containers/chests) or 441 (FakeContainers): only when frameX in [36,180) or (409,396] i.e. lit chest styles? Actually condition: `((typeCache == 21 || 441) && (tileFrameX < 36 || tileFrameX >= 180) && (tileFrameX < 396 || tileFrameX > 409))` → return (no dust). So chest sparkles only for frameX 36..179 and 396..409 — those are golden chests? Actually 36..180 are the special chest frames? Hmm — in vanilla, chest sparkle happens when chest is "open" or when it's a golden/chromatic chest? I recall the sparkle appears for chests in the "locked"? Let me just state the condition as-is: sparkle emitted only when tileFrameX in [36,180) or [396,409] (i.e. NOT the listed exclusion).
- 467/468 (Containers2/FakeContainers2 — desert chests): only when tileFrameX in [144,180).

tileShine values: Main.tileShine[typeCache] > 0 — tiles with shine: 21 chest (shine), gems 63-68, 12 Heart, 566 AmberStoneBlock, 639 ManaCrystal, 665 LifeCrystalBoulder, 204 Crimtane, 211 Chlorophyte, 178 ExposedGems, 617 MasterTrophyBase, and various ores (6 copper, 7 iron, 8 gold, 9 silver, 37? no 37 is meteorite handled earlier...). Note: since the earlier else-if chain catches 37, 58, 76, 684, 12? No — 12 (Heart) has tileShine>0? Hmm. Actually the tileShine branch is `else if (Main.tileShine[typeCache] > 0)` — reached only if earlier conditions failed. So ores 6/7/8/9/22(demonite handled earlier) would emit dust 43 sparkles if tileShine>0. Actually in vanilla, ores don't sparkle... Hmm, but Main.tileShine is only > 0 for specific tiles set in SetTileNames: I recall tileShine set for gems, Life Crystal, Mana Crystal, Amber, Crimtane? no...

The user asked for a table of tile types emitting ambient particles. I'll include the tileShine branch as a group with the specific color overrides (617, 178, 63-68, 12/665, 566, 639, 204, 211) and note the generic set covers any tile with tileShine>0. Let me check what tileShine is set to, to be accurate — search Main.cs for "tileShine[".
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:35:04.798Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileShine\\[\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs | head; grep -oE \"public const ushort [A-Za-z0-9]+ = 373;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs",
 "description": "Find tileShine assignments and tile 373 name"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:35:04.852Z

**📎 ToolResult**

```
7083:		tileShine[221] = 925;
7084:		tileShine[222] = 875;
7085:		tileShine[223] = 825;
7137:		tileShine[129] = 300;
7455:		tileShine[22] = 1150;
7456:		tileShine[6] = 1150;
7457:		tileShine[7] = 1100;
7458:		tileShine[8] = 1000;
7459:		tileShine[9] = 1050;
7460:		tileShine[166] = 1125;
public const ushort WaterDrip = 373;

```


---

## 🤖 Assistant · 2026-08-11T02:35:07.147Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '7080,7090p;7130,7145p;7450,7500p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs; grep -oE \"public const ushort [A-Za-z0-9]+ = (221|222|223|129|166|167|168|169|170|107|221|108|222);\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | sort -u",
 "description": "Read tileShine values and map ore IDs"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:35:07.208Z

**📎 ToolResult**

```
		tileBlockLight[177] = true;
		tileBrick[225] = true;
		tileBrick[229] = true;
		tileShine[221] = 925;
		tileShine[222] = 875;
		tileShine[223] = 825;
		tileShine2[221] = true;
		tileShine2[222] = true;
		tileShine2[223] = true;
		tileMergeDirt[175] = true;
		tileMergeDirt[176] = true;
		tileShine2[117] = true;
		tileShine2[211] = true;
		tileShine2[682] = true;
		tileShine2[681] = true;
		tileShine2[680] = true;
		tileShine2[685] = true;
		tileShine2[686] = true;
		tileShine[129] = 300;
		tileNoFail[81] = true;
		tileCracked[481] = true;
		tileCracked[482] = true;
		tileCracked[483] = true;
		tileNoFail[481] = true;
		tileNoFail[482] = true;
		tileNoFail[483] = true;
		tileNoFail[330] = true;
		tileBlockLight[159] = true;
		tileSolid[159] = true;
		tileMergeDirt[159] = true;
		tileFrameImportant[320] = true;
		tileFrameImportant[49] = true;
		tileShine[22] = 1150;
		tileShine[6] = 1150;
		tileShine[7] = 1100;
		tileShine[8] = 1000;
		tileShine[9] = 1050;
		tileShine[166] = 1125;
		tileShine[167] = 1075;
		tileShine[168] = 1025;
		tileShine[169] = 975;
		tileShine[617] = 400;
		tileShine[178] = 500;
		tileShine2[178] = true;
		tileShine[12] = 300;
		tileShine[21] = 1200;
		tileShine[467] = 1200;
		tileShine[441] = 1200;
		tileShine[468] = 1200;
		tileShine[63] = 900;
		tileShine[64] = 900;
		tileShine[65] = 900;
		tileShine[66] = 900;
		tileShine[67] = 900;
		tileShine[68] = 900;
		tileShine[566] = 900;
		tileShine[45] = 1900;
		tileShine[680] = 1900;
		tileShine[46] = 2000;
		tileShine[681] = 2000;
		tileShine[47] = 2100;
		tileShine[682] = 2100;
		tileShine[122] = 1800;
		tileShine[686] = 1800;
		tileShine[121] = 1850;
		tileShine[685] = 1850;
		tileShine[125] = 600;
		tileShine[109] = 9000;
		tileShine[110] = 9000;
		tileShine[116] = 9000;
		tileShine[117] = 9000;
		tileShine[118] = 8000;
		tileShine[107] = 950;
		tileShine[108] = 900;
		tileShine[111] = 850;
		tileShine[211] = 500;
		tileLighted[699] = true;
		tileLighted[4] = true;
public const ushort Cobalt = 107;
public const ushort Crystals = 129;
public const ushort Lead = 167;
public const ushort Mythril = 108;
public const ushort Orichalcum = 222;
public const ushort Palladium = 221;
public const ushort PineTree = 170;
public const ushort Platinum = 169;
public const ushort Tin = 166;
public const ushort Titanium = 223;
public const ushort Tungsten = 168;

```


---

## 🤖 Assistant · 2026-08-11T02:35:12.886Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have tileShine list. Note: tileShine>0 tiles: 221,222,223 (hardmode ores), 129 (Crystal Shard? 129 = Crystals), 22 (Demonite, but caught earlier), 6,7,8,9 (ores — caught? No! 6/7/8/9 are not in the earlier else-if chain... wait, is 6 in the chain? Chain: 22, 23/24/32, 25, 112, 31/696, 26/695, 71/72, 17/77/133, 405, 37, 58/76/684, 61/703. So 6/7/8/9 fall through to tileShine branch and DO emit dust 43 sparkles). 166-169 (alt ores), 617, 178, 12, 21, 467, 441, 468, 63-68, 566, 45/680 (DemoniteAlt? 45=?), 46/681, 47/682, 122/686, 121/685, 125, 109/110/116/117/118, 107/108/111, 211, 639? (ManaCrystal 639 wasn't in list but code colors it... let me check tileShine[639] and 665 and 204 — grep continued past 7500. Let me get the rest.

Also names: 45, 46, 47, 121, 122, 125, 109, 110, 116, 117, 118, 111, 129.

Note that the probability gate is `_rand.Next(tileShine[type]) >= num43` → return. So probability = lightLevel/30 / tileShine.

Let me get remaining tileShine assignments and names.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:35:13.886Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '7500,7560p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs; grep -oE \"public const ushort [A-Za-z0-9]+ = (45|46|47|121|122|125|109|110|111|116|117|118|204|639|665|211);\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | sort -u",
 "description": "Read remaining tileShine and map names"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:35:14.261Z

**📎 ToolResult**

```
		tileLighted[4] = true;
		tileLighted[17] = true;
		tileLighted[133] = true;
		tileLighted[31] = true;
		tileLighted[696] = true;
		tileLighted[33] = true;
		tileLighted[34] = true;
		tileLighted[35] = true;
		tileLighted[37] = true;
		tileLighted[42] = true;
		tileLighted[49] = true;
		tileLighted[58] = true;
		tileLighted[61] = true;
		tileLighted[703] = true;
		tileLighted[70] = true;
		tileLighted[71] = true;
		tileLighted[72] = true;
		tileLighted[76] = true;
		tileLighted[684] = true;
		tileLighted[77] = true;
		tileLighted[19] = true;
		tileLighted[22] = true;
		tileLighted[26] = true;
		tileLighted[695] = true;
		tileLighted[83] = true;
		tileLighted[84] = true;
		tileLighted[92] = true;
		tileLighted[93] = true;
		tileLighted[95] = true;
		tileLighted[98] = true;
		tileLighted[100] = true;
		tileLighted[109] = true;
		tileLighted[125] = true;
		tileLighted[126] = true;
		tileLighted[129] = true;
		tileLighted[140] = true;
		tileLighted[270] = true;
		tileLighted[271] = true;
		tileLighted[581] = true;
		tileLighted[660] = true;
		tileLighted[578] = true;
		tileMergeDirt[1] = true;
		tileMergeDirt[6] = true;
		tileMergeDirt[7] = true;
		tileMergeDirt[8] = true;
		tileMergeDirt[9] = true;
		tileMergeDirt[166] = true;
		tileMergeDirt[167] = true;
		tileMergeDirt[168] = true;
		tileMergeDirt[169] = true;
		tileMergeDirt[22] = true;
		tileMergeDirt[25] = true;
		tileMergeDirt[30] = true;
		tileMergeDirt[37] = true;
		tileMergeDirt[38] = true;
		tileMergeDirt[40] = true;
		tileMergeDirt[53] = true;
		tileMergeDirt[56] = true;
		tileMergeDirt[107] = true;
		tileMergeDirt[108] = true;
		tileMergeDirt[111] = true;
public const ushort Adamantite = 111;
public const ushort Chlorophyte = 211;
public const ushort CobaltBrick = 121;
public const ushort CopperBrick = 47;
public const ushort Crimtane = 204;
public const ushort CrystalBall = 125;
public const ushort GoldBrick = 45;
public const ushort HallowedGrass = 109;
public const ushort HallowedPlants = 110;
public const ushort LifeCrystalBoulder = 665;
public const ushort ManaCrystal = 639;
public const ushort MythrilBrick = 122;
public const ushort Pearlsand = 116;
public const ushort Pearlstone = 117;
public const ushort PearlstoneBrick = 118;
public const ushort SilverBrick = 46;

```


---

## 🤖 Assistant · 2026-08-11T02:35:15.917Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now check tileShine for 204, 639, 665, 680-686, 566, 617, 178, 12, 221-223, 129. Let me grep specifically for those lines.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:35:16.846Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileShine\\[204\\]\\|tileShine\\[639\\]\\|tileShine\\[665\\]\\|tileShine\\[566\\]\\|tileShine\\[129\\]\\|tileShine\\[125\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs; grep -oE \"public const ushort [A-Za-z0-9]+ = (680|681|682|685|686|683);\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ID/TileID.cs | sort -u",
 "description": "Check remaining tileShine entries"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:35:16.974Z

**📎 ToolResult**

```
7137:		tileShine[129] = 300;
7478:		tileShine[566] = 900;
7489:		tileShine[125] = 600;
9562:		tileShine[639] = 300;
10200:		tileShine[204] = 1150;
public const ushort AncientCobaltBrick = 685;
public const ushort AncientCopperBrick = 682;
public const ushort AncientGoldBrick = 680;
public const ushort AncientMythrilBrick = 686;
public const ushort AncientObsidianBrick = 683;
public const ushort AncientSilverBrick = 681;

```


---

## 🤖 Assistant · 2026-08-11T02:35:25.042Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. 665 (LifeCrystalBoulder) — is tileShine[665] set? grep showed nothing. Hmm but code has `if (typeCache == 12 || typeCache == 665) newColor = red` — that's just color override inside the tileShine branch; 665 reaches it only if tileShine[665] > 0. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:35:25.045Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileShine\\[665\\]\\|tileShine\\[617\\]\\|tileShine\\[178\\]\\|tileShine\\[12\\]\\|tileShine\\[63\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs",
 "description": "Verify tileShine for 665, 617, 178, 12"
}
```


---

## 👤 User(sidechain) · 2026-08-11T02:35:25.117Z

**📎 ToolResult**

```
7464:		tileShine[617] = 400;
7465:		tileShine[178] = 500;
7467:		tileShine[12] = 300;
7472:		tileShine[63] = 900;

```


---

## 🤖 Assistant · 2026-08-11T02:36:04.832Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
665 has no tileShine set → LifeCrystalBoulder reaches the tileShine branch only if tileShine[665] = 0... then `Main.tileShine[typeCache] > 0` false → falls to shimmer branch (not solid? 665 is solid → shimmer dust possible). So the `typeCache == 12 || typeCache == 665` color line covers 12 only effectively (665 likely via... hmm, but maybe tileShine[665] is set elsewhere e.g. in TileLoader or SetDefaults). Whatever — I'll note the color mapping includes 665 conditionally.

Wait — but 12 Heart is non-solid (it's a crystal placed). The shimmer branch requires tileSolid so no.

Now also need to double check the earlier part of the method: lines 6795-6800 confirmed. Also need to check whether there are other emissions between 7067 (visibility return) and 7071 that I've covered — yes all covered.

Also check lines 5969 (`typeCache == 360 || 580 || 620`) and 6351 (typeCache == 15) — those are glow, not particles.

Also the "TileID.Sets.MakesRubbleDust" generic block (7016-7066): rubble dust for natural tiles — worth including as a generic entry.

Now assemble the table. Sort by tile id ascending. Include line numbers.

Entries (tile id → details):

Pre-visibility-gate section (runs even if tile not visible? Actually `flag = IsVisible(tileCache)`; the return at 7067 happens after these first blocks. So first blocks run regardless of visibility — note that):
- 192 LeafBlock — gore 910 leaf — rand.Next(leafFrequency)==0 where leafFrequency=_leafFrequency/4 (50..500 by wind) — 6962-6965, EmitLivingTreeLeaf 7669-7712
- 215 Campfire — dust 31 — rand(3)==0 && frameY==0 (frameY<36) — rises, x offset ±8 by frameX — 6893-6908
- 244 BubbleMachine — rand(2)==0 && frameX==18 && frameY==18 → gore 411 (rand3), 412 (rand10), 413 (rand80), 414 (rand250), 415 (rand500) — bubble sizes — 6860-6882
- 374/375/461/709 drip tiles (via EmitLiquidDrops at 7714, switch cases 374/375/461 lines 7719-7727; 709 at 7792) — rand(num*2)==0, num=60 default /120/180/180 → drip gore types 716 (lava), 717 (honey), 943/1160-1162 (sand by biome), 1383 (shimmer) — 7714-7798; also 373 WaterDrip handled (default num 60 → water drip gore 706+). Note these come from the tile scanning switch at lines 693-699.
- 384 LivingMahoganyLeaves — gore 914 — 6966-6969
- 406 Chimney — frameY==54 && frameX==0 && rand(3)==0 → gore 825-827 steam, wind-pushed — 6925-6946
- 452 SillyBalloonMachine — frameX==0 && frameY==0 && rand(3)==0 → gore 907+frame/5, rand(2) — 6947-6961
- 565 FogMachine — frameX==0 && frameY==18 && rand(3)==0 → Gore.NewGorePerfect 1202 fog, scale 8-9.6, drifts — 6883-6892
- 592 BrazierSuspended — dust 31 — rand(3)==0 && frameY==18 — 6909-6924
- 666 PoopBlock / 712 Poulder — rand(100)==0, dry, air above → PooFly particle — 6970-6976
- 711 RainbowBoulder — frameX==0 && frameY==0 → RainbowBoulder3 rand(45), RainbowBoulder2 2/3 of time — 6977-6994
- 718 StarCloud — night only, rand(3)==0, not solid above: firefly gores 16 (RollLuck 100) & 17 (RollLuck 60), dust 58 (RollLuck 30) — 6800-6859
- Generic: TileID.Sets.SpawnsNatureFlies (6995-7015), rubble dust MakesRubbleDust rand(1200) (7016-7066)

Visible-only (after line 7067-7070 return):
- 4 Torches — rand(40)==0, frameX<66 — dust TorchID.Dust[frameY/22], rises (vel.Y -= 1.5, *0.3), noGravity 2/3, disco color if dust 66 — 7220-7242
- 12 Heart (Life Crystal) — tileShine branch — dust 43 white? newColor red for 12/665 — rand(tileShine=300) vs light — 7604-7607 + 7529-7646
- 17 Furnaces / 77 Hellforge / 133 AdamantiteForge — rand(40)==0, frameX==18 && frameY==18 (lit) → dust 6 ember above — 7482-7492
- 21 Containers (chest) + 441 FakeContainers — tileShine 1200, frameX window [36,180) or [396,409] — dust 43 — 7529-7646 + 7545
- 22 Demonite — rand(400)==0 → dust 14 — 7435-7438
- 23 CorruptGrass / 24 CorruptPlants / 32 CorruptThorns — rand(500)==0 → dust 14 — 7439-7442
- 25 Ebonstone — rand(700)==0 → dust 14 — 7443-7446
- 26 DemonAltar / 695 DemonAltarReplica — rand(20)==0: frameX>=54 → dust 5 scale 1.5 noGravity rising-ish; else dust 14 — 7464-7477
- 31 ShadowOrbs / 696 ShadowOrbsReplica — rand(20)==0: frameX>=36 → dust 5 (vel.Y=0, vel.X*0.3); else dust 14 — 7451-7463
- 33 Candles — NOT present in this decompile (no emission)
- 34 Chandeliers — rand(40)==0, frameX%108<54, frameY/18%3==1, col!=1 — dust 6/59/57/242 by style row (25→59, 50→57, 51→242) — 7376-7426
- 37 Meteorite — rand(250)==0 → dust 6, scale rand(3), noGravity if scale>1 — 7504-7511
- 42 HangingLanterns — frameX==0, frameY/36 odd rows: style 7 → dust 58 rand(50) + firefly gore 16/17 rand(100); style 29 → dust 59 rand(40); style 50 → dust 57 rand(10); style 51 → dust 242 rand(40) — 7161-7219
- 45 GoldBrick (680 AncientGoldBrick), 46 SilverBrick (681), 47 CopperBrick (682), 121 MythrilBrick (686), 122 CobaltBrick (685) — tileShine 1900-2100 → dust 43 white — 7529-7646
- 49 WaterCandle — frameX==0 && rand(2)==0 → dust 172, scale 0.5/0.9 noGravity, rises — 7342-7356
- 58 Hellstone / 76 HellstoneBrick / 684 AncientHellstoneBrick — rand(250)==0 → dust 6 noLight — 7512-7520
- 61 JunglePlants / 703 JunglePlantsEcho — frameX==144 && rand(60)==0 → dust 44 (jungle spores) fadeIn 0.7 — 7521-7528
- 63-68 gems (Sapphire/Ruby/Emerald/Topaz/Amethyst/Diamond) — tileShine 900 → dust 43 colored (blue/red/green/yellow/purple/white) — 7600-7623
- 71 MushroomPlants / 72 MushroomTrees — color()==0 (blue) && rand(500)==0 → dust 41 glowing mushroom sparkle scale 0.8 — 7478-7481
- 83 MatureHerbs (blooming alchemy herbs) — EmitAlchemyHerbParticles by style: 0 Daybloom dust 19 rand(100); 1 Moonglow dust 41 rand(100); 3 Deathbloom? style 3 → dust 14 rand(200) + dust 27 rand(75); 4 Waterleaf dust 16 rand(150) rising; 5 Fireblossom dust 6 rand(40) scale 1.5 rises; 6 Shiverthorn dust 43 colored (50,255,255) rand(30) — 7427-7434 & 9780-9830. Note style 2 (Blinkroot) has no particles.
- 93 Lamps — rand(40)==0, frameX==0, frameY/18%3==0, rows 0/6/7/8/10/14/15/16 → dust 6; 20 → 59; 44 → 57; 45 → 242 — 7243-7285
- 98 SkullLanterns — rand(40)==0, frameX==0 && frameY==0 → dust 6 — 7332-7341
- 100 Candelabras — rand(40)==0, frameX<36, frameY/18%2==0, rows → dust 6/59/57/242; position by frameX side — 7286-7331
- 112 Ebonsand — rand(700)==0 → dust 14 — 7447-7450
- 125 CrystalBall — tileShine 600 → dust 43 — 7529-7646
- 129 Crystals (Crystal Shard) — tileShine 300 → dust 43 — 7529-7646
- 139 MusicBoxes — frameX==36 && frameY%36==0 && time%7==0 && rand(3)==0 → music note gore 570-572 drifting with wind — 7077-7096
- 165 Stalactite — frameX 162-214 && frameY==72 && rand(60)==0 → dust 153 water drip (vel.Y=0, vel.X*0.05) — 7150-7160
- 166 Tin / 167 Lead / 168 Tungsten / 169 Platinum ores — tileShine 975-1125 → dust 43
- 178 ExposedGems — tileShine 500 → dust 43, rainbow color by frameX/18 column (7 colors) — 7570-7599
- 192/384 already listed
- 204 Crimtane — tileShine 1150 → dust 43 red
- 211 Chlorophyte — tileShine 500 → dust 43 green (50,255,100)
- 215 campfire listed
- 221 Palladium / 222 Orichalcum / 223 Titanium ores — tileShine 825-925 → dust 43
- 238 PlanteraBulb — rand(10)==0 → dust 168 pink, noGravity, alpha 200 — 7071-7076
- 372 PeaceCandle — frameX==0 && rand(2)==0 → dust 242 — 7357-7371
- 405 Fireplace — rand(20)==0, frameX==18 && frameY==18 (lit) → dust 6 over 24x10 above — 7493-7503
- 441/467/468 chests — listed
- 463 DefendersForge — frameY==54 && frameX==0 → up to 4x dust 16 steam (rand2 each), noGravity alpha 140; frameY==18 && (frameX 0|36) && rand(13)==0 → dust 274 drifting vertically — 7097-7130
- 497 Toilets — frameY/40==31 && rand(10)==0 → dust 43 white sparkle scale 0.7 noLight — 7131-7149
- 565 fog machine listed
- 566 AmberStoneBlock — tileShine 900 → dust 43 yellow
- 592 listed
- 617 MasterTrophyBase — tileShine 400 → dust 43, only on bottom row sub-tiles (j >= num45 logic) — 7552-7569
- 639 ManaCrystal — tileShine 300 → dust 43 blue
- 646 ShadowCandle — frameX==0: `_rand.Next(2)` called but result discarded — NO emission (dead code) — 7372-7375
- 665 LifeCrystalBoulder — color override exists (red) but no tileShine assigned in Main.cs; effectively covered by generic tileShine branch only if shine set — mention.
- 680/681/682/685/686 ancient bricks — listed
- 695/696 replicas — listed
- 703 listed
- 709 shimmer drip listed (EmitLiquidDrops)
- 711/712/718 listed
- Shimmer solid tiles generic: any tileSolid && Main.shimmerAlpha>0 → dust 43 white, rand(500) < 2*shimmerAlpha — 7647-7666
- Ores 6/7/8/9 (Copper/Iron/Gold/Silver) — tileShine 1000-1150 → dust 43. Note 6 Copper etc. Yes: tileShine[6]=1150, [7]=1100, [8]=1000, [9]=1050. And 37? tileShine[37]? Not listed — no. Also 22 has tileShine 1150 but caught earlier by the rand(400) branch (else-if), so demonite uses dust 14 instead.
- 107 Cobalt / 108 Mythril / 111 Adamantite ores — tileShine 850-950 → dust 43
- 109/110 HallowedGrass/HallowedPlants — tileShine 9000 → dust 43 (very rare sparkle)
- 116 Pearlsand / 117 Pearlstone / 118 PearlstoneBrick — tileShine 8000-9000 → dust 43

Wait, need to double check: does 107/108/111 appear in tileShine? Lines: tileShine[107] = 950; [108] = 900; [111] = 850. Yes.

Also 166/167/168/169 yes.

Also 129 Crystals yes.

Also: what about 12 Heart — yes 300.

Now, "tileShine2" — not used in EmitParticles (only in drawing). Skip.

Note: 665 — check whether tileShine[665] set anywhere (TileLoader? no). I'll note it.

Also note the tileShine branch requires tileLight > 20 in some channel (returns otherwise at 7531-7534), and probability: _rand.Next(tileShine) < lightMax/30 → emit.

Also worth mentioning: `DrawTiles_EmitParticles` is called from multiple draw paths (lines 978, 8506, 8564, 9144, 9661) — regular tiles, animated tiles, multi-tile grass, vines.

Also the vision-changer dust (danger sense dust 60 line 921/8655; spelunker dust 204 line 940/8674; biome sight dust 267 line 966/8702/9274) — not tile-ambient per se; mention briefly as out of scope but present in file.

Now let me write the plan file? Wait — plan mode is active per the system reminder. Hmm, this is a read-only research task; the instruction says to create a plan at the path if needed. The task is purely informational (produce a markdown table). I think the appropriate response is to just answer with the table — the "plan" concept doesn't fit, but the reminder says answer comprehensively. I'm a file-search subagent whose job is to return findings. I'll return the final report directly. Writing a plan file is allowed but unnecessary; the user wants the table as the answer. I'll just give the answer.

Note the user said "skip detail for these but list line numbers" for torch/candle/water candle/peace candle/lava lamps/tiki torch. Candles (33) and volcano 593/594 have NO dust emission in this file (only light flags at 2724-2728, 6332-6343 glowmasks). I'll note that.

Let me produce the table sorted by tile id.
```

</details>


---

## 🤖 Assistant · 2026-08-11T02:36:49.456Z · glm-x-preview-260804

```
I have everything I need. Here is the complete extraction.

# Ambient per-tile particle emission in TileDrawing.cs

All entries below are from **`DrawTiles_EmitParticles(int j, int i, Tile tileCache, ushort typeCache, short tileFrameX, short tileFrameY, Color tileLight)`** at `~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Drawing/TileDrawing.cs` lines **6795–7667**, except where noted. It is invoked from 5 draw paths (lines 978, 8506, 8564, 9144, 9661).

Structural note: lines 6797–7066 run **before** the `if (!IsVisible(tileCache)) return;` gate at line 7067 (so those emit even for non-visible tiles); everything from line 7071 onward requires the tile be visible. Note the method signature order is `(j, i)` for the main loop but `(i, j)` at the EmitAlchemyHerbParticles call site (7432) — coordinates are swapped there.

## Pre-visibility gate (lines 6800–7066)

| tileId | tileName | dustId | probability | notes / lines |
|---|---|---|---|---|
| 192 | LeafBlock | gore 910 (leaf) | `_rand.Next(leafFrequency)==0`, leafFrequency = _leafFrequency/4 (50–500 by wind) | `EmitLivingTreeLeaf`, drops below + sideways on wind; 6962–6965, helper 7669–7712 |
| 215 | Campfire | 31 (smoke) | `_rand.Next(3)==0` && tileFrameY==0 (&& <36) | Rises (`vel.Y -= 0.5..1.4`), X nudged +rand(8) if frameX==0, −rand(8) if frameX==36; 6893–6908 |
| 244 | BubbleMachine | gore 411/412/413/414/415 | frameX==18 && frameY==18 && `_rand.Next(2)==0`; then nested rand(3)/rand(10)/rand(80)/rand(250)/rand(500) | Five bubble sizes; 6860–6882 |
| 373/374/375/461/709 | WaterDrip/LavaDrip/HoneyDrip/SandDrip/ShimmerDrip | gore 706+water style / 716 / 717 / 943,1160 (corrupt),1161 (crimson),1162 (hallow) / 1383 | `_rand.Next(num*2)==0`, num=60 (water/shimmer), 120 (lava), 180 (honey/sand); skipped if liquid present or a drip gore already nearby | `EmitLiquidDrops` 7714–7798; dispatched from tile scan switch at 693–699 |
| 384 | LivingMahoganyLeaves | gore 914 (leaf) | `_rand.Next(leafFrequency)==0` | Same leaf helper; 6966–6969 |
| 406 | Chimney | gore 825–827 (steam) | tileFrameY==54 && tileFrameX==0 && `_rand.Next(3)==0` | Steam puff; pushed by −WindForVisuals if wind < 0; 6925–6946 |
| 452 | SillyBalloonMachine | gore 907 + tileFrame/5 | tileFrameX==0 && tileFrameY==0 && `_rand.Next(3)==0`, then `_rand.Next(2)==0` for one of two scales | 6947–6961 |
| 565 | FogMachine | gore 1202 (fog) via `Gore.NewGorePerfect` | tileFrameX==0 && tileFrameY==18 && `_rand.Next(3)==0` | scale 8–9.6, spreads outward; 6883–6892 |
| 592 | BrazierSuspended | 31 (smoke) | tileFrameY==18 && `_rand.Next(3)==0` | Same rise/nudge pattern as campfire; 6909–6924 |
| 666, 712 | PoopBlock, Poulder | ParticleOrchestraType.PooFly | `_rand.Next(100)==0`, tile dry, no active/walkable tile or liquid above | 6970–6976 |
| 711 | RainbowBoulder | ParticleOrchestraType.RainbowBoulder3 / RainbowBoulder2 | tileFrameX==0 && tileFrameY==0; Boulder3 rand(45)==0, Boulder2 2-of-3 frames | 6977–6994 |
| 718 | StarCloud | dust 58 + gore 16, 17 (fireflies) | night only && `_rand.Next(3)==0` && not solid above; dust gated by `player.RollLuck(30)==0`, gores by RollLuck(100)/RollLuck(60) | Dust 58 white, rises strongly (`vel.Y -= 0.5..6.0`), 6800–6859 |
| (generic) | TileID.Sets.SpawnsNatureFlies | ParticleOrchestraType.NatureFly | `_rand.NextFloat() < lerp(|WindForVisuals|,0.08,0.18)+0.3`, then rand(600) or wind-grid rand(48) | 6995–7015 |
| (generic) | TileID.Sets.MakesRubbleDust | `WorldGen.KillTile_MakeTileDust` rubble dust | `_rand.Next(1200)==0`, weighted by depth/wall wind allowance | 1–3 dusts, damped `vel *= 0.1`, sink +8px; 7016–7066 |

## Visible-only (lines 7071–7667)

| tileId | tileName | dustId | probability | notes / lines |
|---|---|---|---|---|
| 4 | Torches | `TorchID.Dust[frameY/22]` (per torch style) | `_rand.Next(40)==0` && tileFrameX < 66 | X offset varies with frameX (22→+6, 44→+2, else +4); rises (`vel.Y -= 1.5`, `vel *= 0.3`); noGravity 2/3; disco color if dust 66; 7220–7242 |
| 6, 7, 8, 9 | Copper/Iron/Gold/Silver ore | 43 (sparkle) | tileShine 1150/1100/1000/1050, `_rand.Next(tileShine) < lightMax/30` | Requires tileLight > 20; generic shine branch 7529–7646 |
| 12, 665 | Heart (Life Crystal), LifeCrystalBoulder | 43, colored red | tileShine[12]=300 (665 has no tileShine assignment in Main.cs, so effectively heart only) | Color override 7604–7607; branch 7529–7646 |
| 17, 77, 133 | Furnaces, Hellforge, AdamantiteForge | 6 (ember/smoke) | `_rand.Next(40)==0` && tileFrameX==18 && tileFrameY==18 (lit state only) | Spawned above the tile (−4,−6 offset), noGravity 2/3; 7482–7492 |
| 21, 441 | Containers, FakeContainers (chests) | 43 | tileShine 1200 | Only when tileFrameX in [36,180) or [396,409] (lit/gold chest frames); gate at 7545 |
| 22 | Demonite | 14 | `_rand.Next(400)==0` | 7435–7438 |
| 23, 24, 32 | CorruptGrass, CorruptPlants, CorruptThorns | 14 | `_rand.Next(500)==0` | 7439–7442 |
| 25 | Ebonstone | 14 | `_rand.Next(700)==0` | 7443–7446 |
| 26, 695 | DemonAltar, DemonAltarReplica | 5 (shadow) or 14 | `_rand.Next(20)==0` | frameX>=54 → dust 5 (scale 1.5, noGravity, `vel *= 0.75`); else dust 14; 7464–7477 |
| 31, 696 | ShadowOrbs, ShadowOrbsReplica | 5 (shadow) or 14 | `_rand.Next(20)==0` | frameX>=36 → dust 5 with `vel.Y = 0`, `vel.X *= 0.3` (drifts sideways); else dust 14; 7451–7463 |
| 34 | Chandeliers | 6 (fire), 59 (demon), 57 (ice), 242 (peace) by style row | `_rand.Next(40)==0` && tileFrameX%108 < 54 && tileFrameY/18%3==1 && middle column excluded | Rises like torch; 7376–7426 |
| 37 | Meteorite | 6 | `_rand.Next(250)==0` | scale = `_rand.Next(3)`, noGravity if scale > 1; 7504–7511 |
| 42 | HangingLanterns | 58 / 59 / 57 / 242 (+gore 16–17) | tileFrameX==0, odd frameY rows only; style 7: dust 58 rand(50), firefly gore 16–17 rand(100); style 29: dust 59 rand(40); style 50: dust 57 rand(10); style 51: dust 242 rand(40) | Rise, noGravity 2/3; 7161–7219 |
| 45/680, 46/681, 47/682, 121/686, 122/685 | Gold/Silver/Copper/Mythril/Cobalt Brick + Ancient variants | 43 | tileShine 1900–2100 | Generic shine branch 7529–7646 |
| 49 | WaterCandle | 172 | tileFrameX==0 (lit) && `_rand.Next(2)==0` | scale 0.5 (1/3) or 0.9 + noGravity, rises; 7342–7356 |
| 58, 76, 684 | Hellstone, HellstoneBrick, AncientHellstoneBrick | 6 | `_rand.Next(250)==0` | `noLight = true`; 7512–7520 |
| 61, 703 | JunglePlants, JunglePlantsEcho | 44 (jungle spores) | tileFrameX==144 && `_rand.Next(60)==0` | fadeIn 0.7; 7521–7528 |
| 63, 64, 65, 66, 67, 68 | Sapphire/Ruby/Emerald/Topaz/Amethyst/Diamond | 43, colored (blue/red/green/yellow/purple/white) | tileShine 900 each | Gem sparkles; color overrides 7600–7623 |
| 71, 72 | MushroomPlants, MushroomTrees | 41 (glow) | `tileCache.color()==0` (blue) && `_rand.Next(500)==0` | scale 0.8; 7478–7481 |
| 83 | MatureHerbs (blooming herbs) | per style (see below) | per style | `EmitAlchemyHerbParticles`, 7427–7434 + 9780–9830 |
| 93 | Lamps | 6 / 59 / 57 / 242 by style row | `_rand.Next(40)==0` && tileFrameX==0 && tileFrameY/18%3==0; rows 0,6,7,8,10,14,15,16→6; 20→59; 44→57; 45→242 | Rises; 7243–7285 |
| 98 | SkullLanterns | 6 | `_rand.Next(40)==0` && tileFrameX==0 && tileFrameY==0 | Rises; 7332–7341 |
| 100 | Candelabras | 6 / 59 / 57 / 242 by style row | `_rand.Next(40)==0` && tileFrameX<36 && tileFrameY/18%2==0 | X position flips with frameX side (rand(3) picks inner/outer); 7286–7331 |
| 107, 108, 111 | Cobalt, Mythril, Adamantite ore | 43 | tileShine 950/900/850 | Generic shine branch |
| 109, 110, 116, 117, 118 | HallowedGrass, HallowedPlants, Pearlsand, Pearlstone, PearlstoneBrick | 43 | tileShine 8000–9000 (very rare) | Generic shine branch |
| 112 | Ebonsand | 14 | `_rand.Next(700)==0` | 7447–7450 |
| 121, 122, 125, 129, 166–169, 204, 211, 221–223, 566, 617, 639 | MythrilBrick, CobaltBrick, CrystalBall, Crystals, Tin/Lead/Tungsten/Platinum, Crimtane, Chlorophyte, Palladium/Orichalcum/Titanium, AmberStoneBlock, MasterTrophyBase, ManaCrystal | 43, various colors | tileShine per tile (see Main.cs 7455–7489, 7137, 9562, 10200) | 178 ExposedGems gets rainbow color by frameX/18 (7570–7599); 617 MasterTrophyBase only on lower sub-tiles (7552–7569); 204 red (7636), 211 green (50,255,100) (7640), 566 yellow (7624), 639 blue (7632) |
| 139 | MusicBoxes | gore 570–572 (music notes) | tileCache.frameX==36 && frameY%36==0 && `(int)Main.timeForVisualEffects % 7 == 0` && `_rand.Next(3)==0` | Notes drift with `Main.WindForVisuals * 2`, slight upward vel; 7077–7096 |
| 165 | Stalactite | 153 (water drip) | tileFrameX 162–214 && tileFrameY==72 && `_rand.Next(60)==0` | Dripping variant only; `vel.Y = 0`, `vel.X *= 0.05`, alpha 100; 7150–7160 |
| 238 | PlanteraBulb | 168 (pink) | `_rand.Next(10)==0` | noGravity, alpha 200; 7071–7076 |
| 372 | PeaceCandle | 242 | tileFrameX==0 (lit) && `_rand.Next(2)==0` | scale 0.5/0.9, noGravity, rises; 7357–7371 |
| 405 | Fireplace | 6 (smoke/ember) | `_rand.Next(20)==0` && tileFrameX==18 && tileFrameY==18 (lit) | Wide spawn area 24x10 above (−4,−6); noGravity 4/5; 7493–7503 |
| 463 | DefendersForge | 16 (steam) and 274 | frameY==54 && frameX==0: 4 attempts, each rand(2); frameY==18 && (frameX 0 or 36): `_rand.Next(13)==0` → dust 274 | Steam noGravity alpha 140 fadeIn 1.2; dust 274 drifts vertically (`vel = (0, rand ±1.2)`); 7097–7130 |
| 497 | Toilets | 43 (white sparkle) | `frameY/40 == 31 && frameY%40 == 0` && `_rand.Next(10)==0` | scale 0.7, noGravity, alpha 254, noLight; 7131–7149 |
| 646 | ShadowCandle | — (none) | tileFrameX==0 | **Dead code**: only calls `_rand.Next(2)` and discards the result; 7372–7375 |
| (generic) | any `Main.tileSolid[type]` tile | 43 (white) | `Main.shimmerAlpha > 0` && `_rand.Next(500) < 2 * shimmerAlpha` && lit | Shimmer-transmutation sparkle; 7647–7666 |

## Herbs in detail — `EmitAlchemyHerbParticles` (lines 9780–9830), called for tile 83 only when `WorldGen.IsAlchemyPlantHarvestable(style, j)` (7427–7434)

| style | herb | dustId | probability | notes / lines |
|---|---|---|---|---|
| 0 | Daybloom | 19 | `_rand.Next(100)==0` | Spawned 4px above, damped velocity, noGravity, fadeIn 1; 9782–9789 |
| 1 | Moonglow | 41 | `_rand.Next(100)==0` | scale 0.8, alpha 250; 9790–9793 |
| 2 | Blinkroot | — | — | No particles |
| 3 | Deathbloom | 14 and 27 | dust 14 rand(200), dust 27 rand(75) | dust 14 fadeIn 1.2 scale 0.2; dust 27 damped; 9794–9807 |
| 4 | Waterleaf | 16 | `_rand.Next(150)==0` | Tiny (scale *= 0.1), rises (`vel.Y -= 0.7`), noGravity; 9808–9818 |
| 5 | Fireblossom | 6 | `_rand.Next(40)==0` | Spawned 6px above, scale 1.5, rises 2.0, noGravity; 9819–9824 |
| 6 | Shiverthorn | 43 | `_rand.Next(30)==0` | Color (50,255,255), velocity zeroed; 9825–9829 |

## Answers to your specific questions

- **51 Cobweb — no ambient particles.** Its only appearance in this file is in the danger-highlight flag list at line 4491 (`typeCache == 51 || typeCache == 229`).
- **229 HoneyBlock — no ambient particles** in this file either (same line 4491 flag list). Honey visuals are liquid-side sparkle in Main.cs line 57132 (dust 43, `rand.Next(20000) < lightMax/30`, colored yellow when `tile.honey()`), which is a liquid-surface effect, not a tile emission.
- **Candles (33), VolcanoSmall/Large (593/594), PottedLavaPlants (613/614) — no Dust emission anywhere in this file.** They only appear in light/glowmask logic: 593/594 at lines 2724–2728, 613/614 at 2716–2720 and 5343–5356/5536–5557, and candle 33 in glowmask data at 6332–6343 and light flags in Main.cs (7502ff). If you have candle/volcano particles from another source, they are not in this decompile.
- Demon altar: yes — tiles 26 (+ replica 695), lines 7464–7477.
- Bubbles: BubbleMachine 244 (gore-based), lines 6860–6882. There is no plain "bubble" tile emission.
- Fog machine: tile 565, lines 6883–6892. Smoke: Chimney 406 (6925–6946), campfire 215 / brazier 592 (6893–6924), fireplace 405 (7493–7503), Defender's Forge 463 (7097–7130).
- Fireflies: StarCloud 718 at night (6800–6859) and HangingLanterns style 7 (7174–7179).
- Gem sparkles: gems 63–68, ExposedGems 178, AmberStoneBlock 566, ManaCrystal 639, Heart 12, CrystalBall 125, Crystals 129, plus all ores and gold/silver/copper bricks via the generic `Main.tileShine > 0` branch (7529–7646) — the full tileShine table is Main.cs lines 7083–7085, 7137, 7455–7489, 9562, 10200.
- Sea oats / grass: no dedicated emission; generic `SpawnsNatureFlies` (6995–7015) and `MakesRubbleDust` (7016–7066) sets cover grasses.

## Main.cs legacy check — nothing tile-ambient

Every `Dust.NewDust` in `~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs` falls into one of these buckets: weather/snow (13024), `TeleportEffect` styles (13180, 13200, 13218, 13228, 13263, 13279, 13297, 13330, 13378, 13392), NPC drawing — Dungeon Guardian bone arms, Lunatic Cultist, Target Dummy (22588, 22671, 24361–24381, 27282–27285), item pickups (38100), and liquid rendering (57132, 57155, 57159). None is a tile-type emission, so there is no legacy per-tile list to merge. The only borderline ones are the liquid ones: dust 43 surface sparkle (57132, `rand.Next(20000) < light/30`, white or yellow for honey) and lava bubbles dust 35 (57155 `rand(700)==0`, 57159 `rand(350)==0` on surface tiles) — these key off liquid flags, not tile type.

Also note, for completeness, that TileDrawing.cs lines 921–968, 8655–8702 and 9274 emit dust too, but those are player-vision effects (danger sense dust 60, spelunker dust 204, biome sight dust 267) triggered per tile by buff state, not ambient tile behavior.
```
