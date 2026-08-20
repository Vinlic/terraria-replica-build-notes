# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T07:07:25.326Z

```
你在为 SandboxWorld(泰拉瑞亚网页复刻)项目的"从0到1"展示页挖掘最新迭代的丰富素材。

数据源:
1. ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ 下 mtime ≥ 08-18 的所有记忆文件(约 60+ 份)——这是 08-18 到 08-19 的最新工作
2. ~/Project/GLM/SandboxWorld/tools/journey-inputs/archive-stream.json 中的 "08-18" 和 "08-19" 数组(418+96 条实录)

请产出三份清单,写入 /tmp/latest-mining.md:

## 一、新增亮点故事(非缺陷,是成就/工程突破)
每条格式:`- **故事名**(日期): 2-3 句描述,要生动、有画面感 | 证据:记忆文件或实录时刻`
目标 8-12 条。方向:
- WebGL2 一期(背景层+全屏地图 GL 化,从 Canvas 2D 升级到 GPU 渲染)
- SimHost 服务器权威房全链(进程内虚拟房主、刷怪镜像、ioWorker、E2E 15绿)
- remaster-studio-pipeline(重制管线)
- 液体 buffer-reflow 对齐
- AI 全量审计(逐族弹幕/重力/旋转/终端速度)
- 微残留清零(xxxx-microresidual-final-clear)
- 物品 tooltip 全量 1:1(悬停气泡 GetLinesInfo 20488-20920 行序)
- 钻石窗口 IO Surface 耗尽修复
- 弹幕绘制偏移表全量
- 鸟类帧族谱系
- Boss 审计第一波修复
- 石巨人三症状修复
- 地牢水宝箱浮空刀
- 液体最后清算(root59)

## 二、新增坑(有明确"现象→根因→修复"结构的)
每条格式:`- **坑名**(日期): 现象:xxx → 根因:xxx → 修复:xxx | 记忆文件:xxx.md`
目标 8-15 条。

## 三、有趣的原始对话片段(来自 archive-stream.json 的 08-18/08-19)
从实录流中挑出最生动的 5-8 个瞬间(人类的惊叹、模型的顿悟、深夜的幽默、意外发现),格式:
`- **[时刻]** 👤/🤖 原文片段(截断80字) [sid]`

要求:全部基于实际内容,不编造;中文;生动吸引人。完成后返回统计+你认为最震撼的 3 个故事一句话。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T07:07:25.329Z

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

## 🤖 Assistant · 2026-08-19T07:07:28.327Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the data sources. I need to:
1. Find memory files with mtime >= 08-18 in ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/
2. Read archive-stream.json's "08-18" and "08-19" arrays

Let me first list the memory files and check the archive-stream.json structure.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:07:28.530Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ -name \"*.md\" -newermt \"2026-08-18\" | sort",
 "description": "List memory files modified on or after Aug 18"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:28.563Z

**📎 ToolResult**

```
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/aaaaa-track-framechain-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ai-parity-audit-2026-08-19.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/bed-sleep-visual-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/bird-findframe-families.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/book-mimic-cultist-dragon-batch.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/boss-audit-wave1-fixes.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/boss-summon-drops-events-batch.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/bunny-walk-frame-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ccccc-place2x2-anchor-check2x2.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/chunk-seam-noninteger-zoom.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/cursor-icon-fullbright.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/debug-tools-f6-f2.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/deerclops-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/default-run-speed-parity.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/dome-slot32-pot-waterbolt-inact.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/dualwindow-iosurface-exhaustion.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/dungeon-waterchest-float-knife.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/equip-unique-stack-parity.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/explosion-family-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/fog-flicker-f4-latetex-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/golem-3symptom-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/half-slab-liquid-band-parity.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/imagebitmap-root-cure.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/item-tooltip-parity-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/journey-page.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/jungle-parity-and-id-collision.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/l10n-bare-key-incident.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/leftover-closeout-4batch.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/liquid-buffer-reflow-parity.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/liquid-desert-blast-finalgen-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/local-item-retirement.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/mechanics-audit-2026-08-12.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/MEMORY.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/npc-ambient-sound-audit.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/npc-damage-gate-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/oooo-deep-residuals-batch.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/oracle-dome-mirror-mmmm-sync.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/player-jump-vanilla-alignment.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/pppp-tail-debts-sweep.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/proj-draw-offset-table.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/pyramid-wallframe-die-debt.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/remaster-studio-pipeline.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/review-found-bugs-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/rrrr-frame-kill-engine.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/server-room-simhost-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/smoothworld-12345-checksuper-inactive.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/spawn-pool-aggro-audit-2026-08-17.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ssss-tail-clearance-batch.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/sw-asset-preload-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/time-system-11-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/tree-bottom-grass-overwrite.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/tree-statue-drop-investigation.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/treecrack-gc-frameguard-2026-08-18.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/uuuu-tttt-residual-clearance.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/vanilla-npc-drops-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/vine-cascade-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/vulture-firefly-ai-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/vvvv-matrix-final-preview.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/weapon-fx-audit-2026-08-13.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/webgl2-phase1-port.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/wof-voodoo-bossslot-fix.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/worldgen-tttt-golden-channels.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/worldgen-yyyy-fourchain-attribution.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/wwww-root59-liquidation.md
~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/xxxx-microresidual-final-clear.md

```


---

## 🤖 Assistant · 2026-08-19T07:07:29.701Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/tools/journey-inputs/archive-stream.json && python3 -c \"\nimport json\nwith open('~/Project/GLM/SandboxWorld/tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\nprint(type(data))\nif isinstance(data, dict):\n    for k, v in data.items():\n        print(k, type(v), len(v) if hasattr(v, '__len__') else '')\n\"",
 "description": "Check archive-stream.json structure and sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:29.757Z

**📎 ToolResult**

```
-rw-r--r--@ 1 user  staff  1477006  8月 19 11:55 ~/Project/GLM/SandboxWorld/tools/journey-inputs/archive-stream.json
<class 'dict'>
08-05 <class 'list'> 190
08-06 <class 'list'> 256
08-07 <class 'list'> 229
08-08 <class 'list'> 21
08-09 <class 'list'> 245
08-10 <class 'list'> 469
08-11 <class 'list'> 522
08-12 <class 'list'> 520
08-13 <class 'list'> 860
08-14 <class 'list'> 213
08-15 <class 'list'> 43
08-16 <class 'list'> 122
08-17 <class 'list'> 319
08-18 <class 'list'> 418
08-19 <class 'list'> 96

```


---

## 🤖 Assistant · 2026-08-19T07:07:32.857Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have 65 memory files modified on/after 08-18, and the archive-stream.json has 418 entries for 08-18 and 96 for 08-19. Let me read the memory files first — I'll read them in batches. Let me check the file sizes first to plan reading.

Actually, let me be efficient. I'll read the memory files (65 files, probably each ~1-2KB). Let me concatenate them with headers to read them all at once.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:07:33.329Z · glm-x-preview-260804

```
我已经获取到文件列表：65 个记忆文件以及 514 条实录条目。我先用 bash 工具批量读取记忆文件。
```


---

## 🤖 Assistant · 2026-08-19T07:07:34.697Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ && for f in webgl2-phase1-port.md server-room-simhost-port.md remaster-studio-pipeline.md liquid-buffer-reflow-parity.md ai-parity-audit-2026-08-19.md xxxx-microresidual-final-clear.md item-tooltip-parity-port.md dualwindow-iosurface-exhaustion.md proj-draw-offset-table.md bird-findframe-families.md boss-audit-wave1-fixes.md golem-3symptom-fix.md dungeon-waterchest-float-knife.md wwww-root59-liquidation.md; do echo \"=====FILE: $f=====\"; cat \"$f\"; echo; done",
 "description": "Read first batch of key memory files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:34.754Z

**📎 ToolResult**

```
<persisted-output>
Output too large (87.1KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/btz4j2jel.txt

Preview (first 2KB):
=====FILE: webgl2-phase1-port.md=====
---
name: webgl2-phase1-port
description: "WebGL2 一期完成(GLSpriteLayer+背景族+全屏地图,像素级对拍);y翻转两次翻车+回归守卫测试;texSubUpdate 9参/#362CFF/纹理键碰撞三大坑全记录"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-18T05:26:21.529Z
---

2026-08-18 一期完成落地(docs/webgl2-migration-plan.md 计划表,#3/#4 待二期)。

**形态**:GL 离屏画布 + 调用方在原 2D 链同一时序 `ctx.drawImage(glfx.canvas,0,0)`
单次合成——层序/透明度零改动。共享模块 `src/render/GLSpriteLayer.ts`
(quad/纹理LRU/双sampler/fillQuad/texSubUpdate)。#1 BiomeBackground 走
BGBlit 接口(2D=CanvasBgBlit 原语义/GL=GLBgBlit),`?bggl=0`/`?mapgl=0` 逃生
门(bgGlEnabled/mapGlEnabled 可运行时切,探针 A/B 用);#2 drawFullMap 四段
(MapBG/卷轴/地图/迷雾)GL,小地图纹理按 Minimap.flushedPixelRects 脏区增量
上传,迷雾按 version:row 键换纹理;MAX_TEXTURE_SIZE 守卫(8400 超限回 2D)。

**对拍结果(同会话 A/B,真实大世界存档 loadJson)**:背景 平均Δ0.02/Δ>8 占
0.1%;地图 Δ=0 完美。方法:暂停冻结→同屏切后端→主画布网格采样(对照组
2D-vs-2D=0.1% 验证冻结有效)。

**四大坑(全修+守卫)**:
1. **clip-space y 翻转两次翻车**(canvas2D y向下 vs GL y向上):修=`gl_Position.y
   = 1.0 - screen.y/uCanvas.y*2`;曾两次被并行会话写回旧版静默丢失(用户两报
   倒置)——**守卫=tests/gl-layer-regression.test.ts 源码级断言锁定五项
   (y翻转/mip采样器/generateMipmap/预乘上传/texSub 8参),丢任一立即红**。
   ★并行会话共用文件,关键修复必须配回归测试,否则"修好了"会被静默蒸发。
2. **texSubUpdate 9 参重载**:WebGL2 的 DOM 源重载只有 8 参(无宽高)——
   Chrome 把画布【左上角 w×h】贴进目标区 = 地图脏块渐变 #362CFF 退化块
   (用户实报+三层源采样定罪:主画布坏/小地图画布好/迷雾好)。修=抠 scratch
   画布走 8 参。**WebGL2 overload 陷阱:DOM 源取子区无原生 API**。
3. **纹理缓存键碰撞**:ImageBitmap 无 .src,键退化为"宽x高"——森林 t0/t2 同
   1024×699 共用一张纹理=满屏 Background_50 平面色(沙漠层尺寸各异侥幸完美,
   误导排查半天)。修=WeakMap 实例自增 id(同 PaperDoll/UISpriteBatch 旧坑)。
4. **mipmap 透明边缘黑化**:直 Alpha 上传+mip=透明像素 RGB(黑)混进边缘;
   修=UNPACK_PREMULTIPLY_ALPHA_WEBGL=true 预乘上传(mip 平均预乘=能量正确,
   shader 公式无需变:premul×tint×uAlpha ≡ straight×tint×a)+LINEAR_MIPMAP_LINEAR
   对齐 Skia 盒式降采样。

**基线(子代理 traceG 分析)**:常规 9.5-11.3ms/帧,背景族 1.5-2.6ms/帧;
地图时段 13.48ms(+20%)、GPUTask 52.3/帧(常规 15.9)。预期 #1 后 -1.5~2.5ms
/帧、#2 地图时段与常规持平/GPUTask ≤20。**restore 族(Canvas2D 状态机)占
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-19T07:07:36.082Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The output is large. Let me read the full persisted output file to get all the content.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:07:36.497Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/btz4j2jel.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:36.688Z

**📎 ToolResult**

````
1	=====FILE: webgl2-phase1-port.md=====
2	---
3	name: webgl2-phase1-port
4	description: "WebGL2 一期完成(GLSpriteLayer+背景族+全屏地图,像素级对拍);y翻转两次翻车+回归守卫测试;texSubUpdate 9参/#362CFF/纹理键碰撞三大坑全记录"
5	metadata: 
6	  node_type: memory
7	  type: project
8	  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
9	  modified: 2026-08-18T05:26:21.529Z
10	---
11	
12	2026-08-18 一期完成落地(docs/webgl2-migration-plan.md 计划表,#3/#4 待二期)。
13	
14	**形态**:GL 离屏画布 + 调用方在原 2D 链同一时序 `ctx.drawImage(glfx.canvas,0,0)`
15	单次合成——层序/透明度零改动。共享模块 `src/render/GLSpriteLayer.ts`
16	(quad/纹理LRU/双sampler/fillQuad/texSubUpdate)。#1 BiomeBackground 走
17	BGBlit 接口(2D=CanvasBgBlit 原语义/GL=GLBgBlit),`?bggl=0`/`?mapgl=0` 逃生
18	门(bgGlEnabled/mapGlEnabled 可运行时切,探针 A/B 用);#2 drawFullMap 四段
19	(MapBG/卷轴/地图/迷雾)GL,小地图纹理按 Minimap.flushedPixelRects 脏区增量
20	上传,迷雾按 version:row 键换纹理;MAX_TEXTURE_SIZE 守卫(8400 超限回 2D)。
21	
22	**对拍结果(同会话 A/B,真实大世界存档 loadJson)**:背景 平均Δ0.02/Δ>8 占
23	0.1%;地图 Δ=0 完美。方法:暂停冻结→同屏切后端→主画布网格采样(对照组
24	2D-vs-2D=0.1% 验证冻结有效)。
25	
26	**四大坑(全修+守卫)**:
27	1. **clip-space y 翻转两次翻车**(canvas2D y向下 vs GL y向上):修=`gl_Position.y
28	   = 1.0 - screen.y/uCanvas.y*2`;曾两次被并行会话写回旧版静默丢失(用户两报
29	   倒置)——**守卫=tests/gl-layer-regression.test.ts 源码级断言锁定五项
30	   (y翻转/mip采样器/generateMipmap/预乘上传/texSub 8参),丢任一立即红**。
31	   ★并行会话共用文件,关键修复必须配回归测试,否则"修好了"会被静默蒸发。
32	2. **texSubUpdate 9 参重载**:WebGL2 的 DOM 源重载只有 8 参(无宽高)——
33	   Chrome 把画布【左上角 w×h】贴进目标区 = 地图脏块渐变 #362CFF 退化块
34	   (用户实报+三层源采样定罪:主画布坏/小地图画布好/迷雾好)。修=抠 scratch
35	   画布走 8 参。**WebGL2 overload 陷阱:DOM 源取子区无原生 API**。
36	3. **纹理缓存键碰撞**:ImageBitmap 无 .src,键退化为"宽x高"——森林 t0/t2 同
37	   1024×699 共用一张纹理=满屏 Background_50 平面色(沙漠层尺寸各异侥幸完美,
38	   误导排查半天)。修=WeakMap 实例自增 id(同 PaperDoll/UISpriteBatch 旧坑)。
39	4. **mipmap 透明边缘黑化**:直 Alpha 上传+mip=透明像素 RGB(黑)混进边缘;
40	   修=UNPACK_PREMULTIPLY_ALPHA_WEBGL=true 预乘上传(mip 平均预乘=能量正确,
41	   shader 公式无需变:premul×tint×uAlpha ≡ straight×tint×a)+LINEAR_MIPMAP_LINEAR
42	   对齐 Skia 盒式降采样。
43	
44	**基线(子代理 traceG 分析)**:常规 9.5-11.3ms/帧,背景族 1.5-2.6ms/帧;
45	地图时段 13.48ms(+20%)、GPUTask 52.3/帧(常规 15.9)。预期 #1 后 -1.5~2.5ms
46	/帧、#2 地图时段与常规持平/GPUTask ≤20。**restore 族(Canvas2D 状态机)占
47	非 idle 34% = 下一优先级独立优化点,不依赖 GL**。
48	
49	探针族:_glpar(跨会话)/_glpar2(同会话A/B)/_glctrl(对照组)/_glflip(正式
50	对拍)/_glrow(行扫描)/_gldeg(退化复现)/_gltex/_glband/_glstate2/_glunit
51	(页内单测)。loadJson 探针存档 public/tmp-*.json 用完必删(会打进 dist)。
52	
53	相关:[[imagebitmap-root-cure]]
54	
55	**五号坑(2026-08-18 补)**:TEXTURE_MAG_FILTER 只接受 NEAREST|LINEAR——
56	mip 档(LINEAR_MIPMAP_LINEAR)传给 MAG = INVALID_ENUM 警告 + MAG 落回
57	sampler 默认 NEAREST(放大采样错过滤,地图 zoom>1 细微画质差)。修=mkSampler
58	分 min/mag 两参;守卫测试同步锁 MAG 恒 LINEAR。
59	
60	**六号坑(2026-08-18 二次崩溃会话)**:①GLSpriteLayer 漏挂 Renderer.dispose
61	世界切换清理链——连续读档逐次叠满 LRU=GB 级显存打爆(contextlost 风暴 26 万次/
62	tab 3.4GB/JS 堆 1GB,chunk 自适应沉到 64 底);同款病 2026-08-10 在 chunk 画布上
63	修过,新增资源池必须同步挂 dispose。②LRU 按条数(96)→按字节(192MB)+记账;
64	③熔断器固定 8s 冷却=永久振荡(期满放行→再抖→再熔),改逐次翻倍 8→16→32→60s
65	封顶+稳定 60s 回落;④小地图/迷雾纹理 noMip(8400×2400 每脏块全链 mip 重生成
66	=巨量 churn,且 MIN/mip 永不被采样);⑤迷雾纹理 version:row 换键→稳定键+行带
67	texSubUpdate(探索期换血烧穿预算)。守卫测试扩到 7 项。
68	
69	**泄漏终审(2026-08-18 用户"确保无其他泄漏点")**:全量资源池扫一遍,
70	补两处——①mainFlow.enterGame 曾直接 `game = g` 替换引用:旧 Game 的 rAF
71	循环靠每帧自注册永生,running 唯一关断入口是 destroy()——任何不经
72	quitToMenu 的直达进图路径(未来新增)都会旧实例永生叠加;兜底=enterGame
73	先拆仍存活的旧实例。②ChunkCache.MAX_CHUNKS 自适应收缩曾【无恢复点】:
74	熔断沉到 64 后所有后续世界永远 64(视野烘焙跟不上);修=afterWorldLoad
75	回满 384(真撑不住熔断器会再自适应,冷却已升级不振荡)。
76	已审清白池:GLSpriteLayer scratch/WHITE_PX(单例)、BG_TEX_ID(WeakMap)、
77	bmpFailStats/Warned(按唯一文件名有界)、tryBitmapUpgrade 重试(≤3,≤70s
78	瞬态)、breaker 定时器(有界)、uiTexCache(随 Renderer 亡)、
79	BiomeBackground imgs(按群系样式有界,随 Renderer 亡)、minimap
80	flushedPixelRects(cap 128)、imglog(flag 门,dev only)。
81	
82	**附带两修(2026-08-18 晚)**:①MAX_CHUNKS 恢复点曾写
83	`this.chunks?.constructor`——afterWorldLoad 头部 chunks 未构造,undefined
84	赋值即崩(用户进档即崩报);改直引 ChunkCache 类静态。**教训:静态恢复点
85	别经实例取,时序上实例可能未生**。②资产门槛"卡一下"真相:门槛等的是 SW
86	status 回包(SW 冷启动+cache.keys() 枚举万条 1-2s),期间 done=0 误显示
87	"正在下载 0%",trace 实证零实际下载;修=完成态落 localStorage(键含版本),
88	门槛先查标志秒开,SW 回包实测校准(被清理则撤销标志)。
89	
90	**全屏地图两修（2026-08-19 用户报"放大到一定程度全黑+背景随缩放变动"）**：①fullMapBgIndex 旧 vy=(cy0+mapH/2)/zoom 是"地图底边屏幕坐标÷zoom"纯错位量→随缩放漂移=背景自己换根因；修=视口顶世界 tile `-cy0/zoom`（原版 screenPosition.Y 语义，:55804 深度档其余档全玩家墙/群系），tests/fullmap-bg-index 4 绿（同视口顶 6 档 zoom 恒同档）。②MapBG*+Map.png vui 懒加载首开图几百 ms 未就绪→近黑底闪（很可能被用户归因为"放大变黑"）→进世界 preloadUiPrefix(['MapBG','Map.png']) 预取。黑屏本体六路复现不中（直调/全帧/DPR2/真滚轮+缓动/±雾/探索泡 0.5→6）+截图证实 z=6 内容正常——若残留需 F5 现场报告。★教训：canvas 像素采样必须用 canvas.getBoundingClientRect 换算（曾用 viewport CSS 坐标直乘 dpr→采到底边 UI 区，"变暗曲线"全是伪影）。
91	
92	**全黑终局（2026-08-19 二轮，用户确认背景修好但放大全黑仍在"只剩头像"）**：头像=2D 后画层 → 整块 GL 合成黑。显微镜探针定罪链：CPU pix 93% 彩色+纹理 isTexture+重传后仍黑，仅大 dst 黑小 dst 正常 → **GPU guard-band 裁剪**（dst 伸出画布数万 px 时部分驱动整图元丢弃）。三层落地：①`Renderer.clipMapQuadToView`（mm/fog quad src/dst 同比回裁进画布——根因修复）；②GL 合成哨兵（end 前 readPixel 中心 1px+CPU explored 对照，连续 3 黑帧→60s 内 2D 兜底——GLSpriteLayer.readPixel 公开 API）；③2D 兜底 `_fm2dDirtyAt` 脏块门重灌（曾一次性建死：建画布时条带重建未完成=永远空图）+F5 `fullMapDiag` 段（路径/探针/bg·scroll 解析/CPU 像素/centerTile）。★headless 无头环境 GL+2D 大图都渲染异常（233=MapBG 羊皮纸透出）——无头结论只可信"相对变化"，绝对正确性要真机截图；2D 兜底是 GL 化前跑了几个月的原始路径，真机可信。
93	
94	**全黑真凶终定罪（同日三轮）**：用户回传哨兵日志 **zoom 1.37 即黑**（非高倍专属）→ 与 `smooth: fm.zoom>=1` 的采样器切换线完全重合 → 查 `samp.linear = mkSampler(LINEAR_MIPMAP_LINEAR, LINEAR)`，而小地图/迷雾纹理 `noMip=true` 无 mip 链——**WebGL 采样器对象覆盖 texParameteri：用需 mip 的 MIN_FILTER 采无 mip 纹理 = 纹理不完整 → 采样恒黑 (0,0,0,1)**。z<1 走 nearest 档所以"缩小恢复"；此前"小矩形正常"对照恰好 smooth:false(nearest) 把我误导去 guard-band。修 = `samp.linearNoMip(LINEAR/LINEAR)`，quad()/tileX() 按 `e.mipped` 分流采样器；探针全档 0.5→6 中心全内容色、哨兵零触发。★GL 铁律：**sampler 对象与纹理参数是两套——incomplete 判定看生效组合**；noMip 纹理必须配无 mip 的 MIN_FILTER。clipMapQuadToView/哨兵/2D 重灌保留作加固与遥测。
95	
96	**迷雾消失排查（2026-08-19 四轮，未复现→遥测定案）**：用户报"迷雾消失没按 F4"。三方排查：F4(main.ts:220)/devMode(mainFlow maybeDev explored.fill(1)，报告 invNonEmpty 仅 3 格=排除)/markExplored r28 是 explored 仅三写入方。渲染侧 4200×1200 同尺寸+1.25% 覆盖率探针全档绿（远角恒雾色 5,5,8）。fullMapDiag 增 `exploredCoverage`（步 997 抽样）+`cornerTileExplored.canvasPx`（未探索角合成像素：雾色=正常/内容色=渲染丢雾/coverage≈1=数据全亮）——一份报告三分支定案。疑点存档：用户旧会话可能按过当时"失效"的 F4（修好后 fill 生效）或存档 explored 段已全 1。
97	
98	**远景背景 Y 偏下（2026-08-19）**：`camTopY = cam.y - viewH/2/1`——**/1 是缩放占位符**！zoom 1.25 下屏顶世界 Y 差 viewH/2×(1-1/zoom)≈86px → num3 偏大 → bgTopY=num3×topA+topB 整体下移 ~70px（实测远山档 476.4 vs 旧 546.4）。修 = `cam.y - viewH/2/cam.zoom`（Main.screenPosition 语义，X 同式 camLeftX）；地表深度门同改屏顶；横向 bgStartX 改 vanilla 式 `-ieeeRem(camLeftX×parallax,w)-w/2-w`（比正模多退一整块，loops ceil+3）；ieeeRemOf 提为类静态。tests/surface-bg-parallax 3 绿（断言修正档 476.4/594.8 出现+旧档恒不出现）。Cam 接口加 zoom 字段。★教训：占位符 `/1` 编译不报错——写死魔法数替代真实语义时 grep 一下语义来源。
99	
100	=====FILE: server-room-simhost-port.md=====
101	---
102	name: server-room-simhost-port
103	description: 服务器权威房(SimHost)B1-B3 批落地——进程内虚拟房主经 room.handle 复用中继管线;GM 规则执法;协议 v8 增量纪律
104	metadata: 
105	  node_type: memory
106	  type: project
107	  originSessionId: a476813d-a6ae-471c-84eb-8f868a94a617
108	  modified: 2026-08-18T08:10:11.383Z
109	---
110	
111	# 服务器权威房 SimHost 移植(2026-08-17 B1-B3 批)
112	
113	**生产修复二:worker 整体崩毁(2026-08-18,用户报障)**:`room.clients.filter is not a function` → worker exit(code=1)全房失联。根因=并行会话在 roomHost 时钟推进 interval 加"全员熟睡×5"时对 **Set 用了 .filter**(room.clients=Set 无此法)——**无守卫 setInterval 内一次抛错=worker 整体退出**(B6a 周期定时器全部裸奔)。修=①Set 先展开 `[...clients].filter`②四个周期定时器(时钟/看门狗/10s 广播/落盘)逐房 try/catch 只记日志。验证 _sr-probe 25/25+_aoi-probe 8/8。★教训:**并行会话向 worker 加周期逻辑时,无守卫 interval 是全局崩毁面——roomHost 的 interval 一律逐房 try/catch**;Set×数组方法(此前 clients.find 也实踩过)。
114	
115	**生产修复:UI 选角加入崩溃(2026-08-18,用户报障)**:`Cannot set properties of undefined (setting 'appearance')` @onJoinRoom——`makeGame().player` 在联机加入流程要到 loadWorld(世界数据到达,Game.ts:2816)才创建,MultiplayerSelect onJoinRoom 提前 `g.player.appearance=selectedAppearance` 踩空(仅选了角色的真实用户触发,探针无角色路径测不出!)。修=预置 `g.pendingJoinName`(Hello 名兜底,ClientNet connect 三级链 player→pendingJoinName→'玩家'),外观本体仍由 onWorldReady 的 applyAppearance 落位。验证 `_uijoin-probe.mjs` 8/8(页面 CharacterStore.create 播种角色→真实 UI 点选→点房→进房成功+PlayerActive 帧带真名)。★方法论:**探针必须覆盖"选了角色"的真实用户路径**;其余两处 appearance 早写(更衣窗回调/applyAppearance)核过安全(player 已建)。
116	
117	用户目标"开在服务器上的房,世界由服务器计算"已落地 MVP(docs/server-room-plan.md 为权威台账)。
118	
119	**核心架构(最低侵入)**:SimHost(`server/src/sim/SimHost.ts`)= 进程内"虚拟房主客户端"——以上行帧格式(C→S msg23/27/21/28)构造,经 `room.handleFromSim()` 走**与房主完全相同的中继管线**(AOI 滞回/短码/背压/限流零旁路)。`room.ts` 预留注释 `this.sim ? false : c.isHost` 的实际落法更优:**serverAuth 房 Hello 永不晋升房主**→全部既有访客门(Game.ts:13351 刷怪/:4081 世界事件等 ~30 处 `!isHost` 门)自动生效,客户端改动收敛到召唤路径一处。
120	
121	**关键事实**:
122	- `entities/types.ts:4` GameHooks 接口缝=实体层本就面向接口;`Enemy.shootDart` 经鸭子 cast 访问 `game.entities`(hooks 须公开 entities 字段);死亡掉落链全在 Enemy 内经 hooks.spawnDrop 出→SimHost 继承全部 1:1 掉落管线
123	- 合成 avatar:真实 `new Player(x,y,new Inventory())`(构造无 DOM,Player.ts:439);**逐实体摆到最近在线客户端**=多人最近目标语义且 Enemy.ts 零改动;掉落/弹幕更新期摆 -1e9(服务器不拾取、敌弹不命中——victim-settles 各客户端本地结算)
124	- Boss 召唤必须镜像 Game.summonBossAtTx:18314-18356 的 fromVanilla+链(世吞 65/70 节链/双子第二只 126/毁灭者地下落位)——`new Enemy(key,x,y)` 直放是错的!
125	- 液体不做逐格广播(协议无液体 op):SimHost 与各客户端跑同一份确定性 LiquidSim,输入一致收敛;进房 strip 反映服务器演化态(备案近似)
126	- **handleFromSim 尾部必须 flushOutbox()**——静默房无 WS 入站消息,P1.3 冲洗点只在 ws message 回调
127	- netId owner=255(服务器段);`255<<24` JS 位运算产生负数但 NetWriter.u32 `>>>0` 序列化回正确无符号
128	
129	**协议 v8(增量纪律,不升 PROTO_VER——SpectateFocus=150 同款先例)**:RoomPolicy 尾部 u8 ruleBits(bit0 serverAuth/bit1 禁Boss/bit2 禁破坏/bit3 禁放置/bit4 禁PvP/bit5 禁爆炸物/bit6 和平);Msg.SummonIntent=202(str npcKey+f32 x,y,vx,vy,客户端算好落位,服务器只查表+规则门);`RoomRules/rulesToBits/rulesFromBits` 在 protocol.ts 双端共享。
130	
131	**GM 系统**:gmToken 建房生成(POST 返回/`--server-room` 常驻房内部生成);URL `?gm=` 或聊天 `/gm <token>` 认证→isGM 规则豁免;`/rules` 回显;PATCH /rooms/<code>/rules 热更→updateRules 联动 SimHost+RoomPolicy 重播。执法门全服务器端:forbidBreak/Place 按 TileOpAction 分立(protectTiles=整包语义不变);爆炸物=单批>24 清格启发;forbidPvp 复用 pvpAllowed 墙。
132	
133	**探针**:`scripts/_sr-probe.mjs` 19 断言全绿(复用 _netfake.mjs 的 spawnServer/makeTinySave/Writer)。坑:探针 TileBatch 帧必须带 SetTile 的 fx/fy 尾字段;全空气微型世界自然刷怪不保证(改用 SummonIntent 确定性验证管线);PATCH 路由正则别复用 `/rooms/(\d{6})$` 的 m。
134	
135	**回归定责法(无 git 仓库!)**:vitest 8 失败(town/vanity/wing/worldgen)+_roomprobe 物品断言——全归并行会话在途物品表编辑(vanity 400≠402 是铁证;`ITEM_DEFS[4798]` undefined 崩 `.key`),本批 diff 零 `.key` 访问可证清白。中继房共享路径(房主门/双保护/AOI/观战)全绿。
136	
137	**B4 批完成(同日续)**:①ioWorker(`server/src/workers/ioWorker*.ts`)——parse=worker JSON.parse 回传纯对象;stringify=主线程 buildSaveParts(SaveFile 增量抽取)廉价视图→memcpy 克隆进 worker 做 RLE+stringify;故障/超时/队满全回退同步;SIGTERM=等在途→同步兜底→ioShutdown。②刷怪链全镜像 Game.trySpawnEnemy(旗标灌注+蠕虫链/水生/贴地/净空/萤火虫附加/骷髅商+bound TownNPC 转化,TOWN_SKIP 退役)。③入侵链(tickInvasion 推进+击杀扣分+日出沿自然 roll)。④SSC 强制(serverAuth 房不依赖 --ssc)。⑤浏览器 E2E `_sr-e2e.mjs` 15/15(真实客户端建房→访客→傀儡→召唤意图→Boss v_50 可见→msg42 打击→服务器结算→移除;探针坑:msg42 dmg 是 i16 用 9999 勿用 99999 会回绕)。
138	**探针总账**:`_sr-probe`(Node)20/20 + `_sr-e2e`(浏览器)15/15;双绿=验收门。
139	**并行会话撞车实录**:worldGen worker 运行期爆栈(栈溢出)系第三方在途改动(进程内 vitest 双种子全绿可证),E2E 用 `__swFlow.loadJson` 载现成档绕开——**浏览器 E2E 不必依赖 worldgen**;探针解析 msg7 时偏移 bug 连犯三次(长度当偏移),教训:手写 Reader 累计偏移必须 `o += len`。
140	**review 批+ B5(2026-08-18)**:自审修 4 件(step 异常防护+连续 600 次停机/召唤 Boss 傀儡预检/聊天命令只拦已知防吞正常聊天/take 重复抑制);AOI 空间索引落地(broadcastAt 2048px 网格桶+观战线性兜底★按自身位入格会漏观战者+msg23/27 整批包围盒早退;_aoi-probe 8/8);日食 roll 内联+夜沿清(避开 Eclipse.ts 的 Lang 依赖)。三探针台账:_sr-probe 20+_sr-e2e 15+_aoi-probe 8。
141	**B6a 房间进程化(2026-08-18 完成)**:Room/World/SimHost/persist/SSC **零改动**整体进 worker_hosts(`server/src/roomHost.ts` K 房/工,ShimSocket 还原 ws 背压语义=未ack字节+主进程回报缓冲);主进程 index.ts=lobby 路由+WS 装配(★早到帧缓冲——connOk 往返期 Hello 不丢;★onHostEvent 里 connOk 必须在 conns 守卫之前——曾全房进房超时);`--workers N` 多工扩展+stats 合并。★worker 加载 TS 的唯一解=**mjs 入口 `register()` tsx**(execArgv --import 三式全无效,Node 原生 strip-types 见 const enum 即炸)。验证:三探针 20+8+15 零改动全过+W=2 冒烟。坑:spawnServer killGroup 的 npx 转发慢+run-diag 0.5s 强退竞态会留孤儿(W=2 测试实测),手动 kill -TERM 直杀即退。
142	**聊天系统+世界频道批(2026-08-18,plan §14)**:客户端此前无聊天输入(只有显示)!补全:ChatInput(Enter 开框/Tab 切频道/300ms 重开抑制/键处理挂 window capture);协议 Text 尾部 u8 channel(0房/1世界,增量);世界链=Room 上抛→main 扇出全 worker→逐房 broadcastWorldChat([世界]<名>+金色,author=255,含回显);反刷屏 10s/8条;双房型同路径。验证:_sr-probe 25/25+_sr-e2e 20/20。★headless 键盘发送跳点悬案:监听器触发+各下游环独立全绿但链路在 CDP 语境断——证据指向页面闭包/模块双载,真机手动验证即可;生产已 window 活实例双路径加固。★诊断方法论:分级取证(页内埋点/服务器收帧日志/直调对照)+**先查环境再查代码**(vite 陈旧模块图/端口残留孤儿各浪费过整轮)。
143	
144	**千人单房优化批(2026-08-18 续,plan §13)**:差分剖析(relay 11.6% vs sim 82.1%@120bot=模拟占86%);三优化落地:①玩家1024px网格(avatar最近目标 O(E×P)→格查,灭平方项)②trySpawn 4tick一掷概率×4(期望不变,统计O(E)砍75%)③AOI密度降频(msg13 拥挤格>16降半>48降三,插值低频设计视觉无损)。**实测:120分散CPU 82→28.6%,60聚集人均10.8→3.27KB/s(-70%)**;千人外推=带宽24-48Mbps+CPU~1.6-2.5核→**最终形态简化为"中继线程+模拟线程"双线程(B7),无需分区并行**;SAB背衬TileStore(additive开关)为B7关键件。slot u16仍gated于worldGen worker修复(_roomprobe为门)。三探针20+8+15零回归。
145	**千人实测(2026-08-18,`_load-probe.mjs`)**:60分散/120分散/60聚集=人均0.44/1.05/**10.8KB/s**,worker CPU 46.6/82.1/59.8%。1000CCU今日拓扑=多房分线→8vCPU/16GB/100Mbps。国内带宽:常态热点型千人≈10TB/月≈8000-9000元(按量0.8元/GB),均匀分散型≈1.5-2.5TB。测量坑:★startBpsSampler须随迁worker(已修);★探针单位B/s误标KB/s造"洪水"假象——**双口径互证法**(bot收 vs /stats出)必用;随机端口防跨跑孤儿。相关:[[multiplayer-capacity-opt-batch]]
146	
147	=====FILE: remaster-studio-pipeline.md=====
148	---
149	name: remaster-studio-pipeline
150	description: 素材重制管线(Remaster Studio)全链落地:AssetCatalog 六类切帧聚合+gpt-image-2 逐帧重制+zip 素材包热补丁(类 mod 局部覆盖)
151	metadata: 
152	  node_type: memory
153	  type: project
154	  originSessionId: be9285e0-8206-48c4-a7de-b260d1c6d232
155	  modified: 2026-08-19T07:07:09.265Z
156	---
157	
158	# 素材重制管线(Remaster Studio,2026-08-19 落地)
159	
160	六里程碑全绿:catalog 单测 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7。
161	
162	**架构三层**:`src/remaster/`(types/AssetCatalog/NpcGridLayouts/FrameOps/PackFormat 进 bundle;ImageRemaster/PromptTemplates/WorkbenchState 工作台专属)+ `public/remaster.html`(dev-only 工作台,tree-inspect 模式直接 import '/src/*.ts')+ `tools/remaster-proxy.mjs`(OpenAI 代理 :5210,npm run remaster-proxy)。
163	
164	**关键坑与定谳**:
165	- ★`onBakeAssetArrived` 对已就位贴图替换是 **no-op**(chunkSheets 只登记烘焙期 miss,ensureVImage hit 早退在 note 前)→ 运行中热补替换 tile/wall 必须走新增的 `ChunkCache.onSheetReplaced`(查 chunkConsumed 消费登记表,500ms 去抖,★禁 invalidateAll)
166	- gpt-image-2 **不支持透明背景**+最小总像素 655,360(边长 16 倍数)→ 必须生成大图(computeGenLayout:帧放大到长边~1024,画布逐 16 扩边达标)后盒式缩回+原帧 alpha 蒙版(轮廓逐像素不变=特性)
167	- OpenAI CORS 两度移除 ACAO → 本地代理转发(node:http 原样 pipe multipart,key 走 Authorization 透传>env,300s 超时)
168	- 卸载/禁用 replay 的 restore 集合必须含【被删 pack 的文件】(只取现存 installed 并集 = 卸载后 vimages 停留 pack 图的根因,E2E 抓到)
169	- tile cols/rows 不可信(压板 135 cols=0 前科)→ AssetCatalog 按 sheet 实际尺寸+stride 步进枚举;696 不在 vanilla-npcs.json(网格兜底补建,694=693+1)
170	- **帧枚举≠渲染 idx**:2D 网格 NPC(npcGridFrames)按行优先网格序枚举 sheet 全格,perRow(696=9)是渲染 idx 折行语义,混入会丢帧(162→54 首版 bug)
171	- 独立缓存三处不经 atlas 须钩子:Arrow.spriteCache/frameCache(键 `id|idx` 无 texId)、UI.ts buff 栏直链 img.src、**UI.ts iconCache(物品id→dataURL,Plan 代理漏,验收时亲查补)**;BestiaryPanel.bstTintCache 经 sw:remaster-applied 事件清
172	- public html 的裸 URL import `'/public/sprites/*.json'` 走静态服务(JSON MIME)→ 模块加载失败;json 一律运行时 fetch
173	- upgradeToBitmap 在 USE_BITMAP=false 时两个回调都不调 → 先判 USE_BITMAP 再走
174	
175	**热补丁注入矩阵**:vanilla→`vimages.set`/vanilla-ui→`uiimages.set`/Projectile 双写+setProjSpriteOverride/Buff→buffIconUrl(objectURL)。KvStore **DB v2** 加 remaster blob store( pack+帧像素;onversionchange 让路)。启动应用在 loadAssets 后零竞争(后继懒加载 has 早退)。`__swRemaster` 桥(main.ts);标题菜单「素材包」→RemasterPanel。
176	
177	素材包 `sw-remaster-pack/1`:manifest(baseVersion=assetVersion 同源 fnv1a36;rect/hash 自带不依赖当前 vanilla.json)+ sheets/ 镜像原版路径混合 sheet png(仅 accepted 帧落重制像素);手写 ZIP_STORED+CRC32 零依赖。素材重打包后重跑 `node scripts/gen-remaster-index.mjs`(10974 张 IHDR 尺寸)。
178	
179	**遗留**:全量回归 25 失败全为并行会话 worldgen/AI 中间态(海马 626 等,与本管线零交集);真实 gpt-image-2 效果调优(prompt 模板/风格锚 edits 多输入图)待用户实跑;PaperDoll/Background/液体/树冠/NPC 横条(594)二期。
180	
181	**Review 修复批(2026-08-19 同日)**:8 项全修+复验 66 单测/17/17/7/7——①IDB v2 多标签 blocked 挂死(applyInstalled 8s 超时兜底+onblocked 告警;★onversionchange 只对同代码版本生效,生产首次部署旧页跑旧 bundle 必踩)②Item_Atlas 共享 sheet 的 manifest frames[frameIdx] 互相覆盖→键改 `${entryKey}#${idx}`(rect 自带,应用侧不依赖此键)③叠加对比语义(newcv CSS opacity 露背景格→原帧打底+临时 canvas α0.5 叠;★putImageData 不吃 globalAlpha)④algo select 缺 value(脏字符串碰巧落 box 分支)⑤PackStore 帧像素整行聚合 O(n²)→单帧单行(id=`frame:条目|帧`)⑥readPack sheet 路径白名单(zip 逃逸条目静默丢)⑦versionMismatch 实装(Manager 注入 getBaseVersion,不符警告不拒装)⑧objectUrls 冗余池删。★html 内联 script 是原生 JS——`getContext('2d')!` TS 非空断言=SyntaxError(修复时自己引入,探针即时抓住)。
182	
183	=====FILE: liquid-buffer-reflow-parity.md=====
184	# 液体缓冲器回灌双重错位 + TileFrameImportant 165/91（DDDDD 批 2026-08-19）
185	
186	- **根因一（主）**：LiquidBuffer 回灌（Liquid.cs:1134-1148，1405 双版一致）——
187	  回灌量 = `curMaxLiquid-(curMaxLiquid-numLiquid)` = **numLiquid**（当前活动数，
188	  非空余量）；`DelBuffer(0)` = **swap-remove**（尾元素补头位，出序 A,C,B… 非
189	  FIFO）；顺序 = 清 checking → AddWater → 后 DelBuffer（满载时同格空转）。JS 曾
190	  FIFO 环形 + 空余量上限 → 中世界（6400×1800）r0 唤醒链首触 24999 帽后回灌时序
191	  整体漂移 → 全图 475 条湖面薄膜高度全漂（#49 L=11,707）。小世界永不触帽 = 三条
192	  小链 #49 长绿的假象来源。修 = bufCount + 尾接 + swap-remove（O(1)）。
193	- **根因二**：YYY 级联 tileFrameGen 缺 165→CheckStalactite / 91→CheckBanner
194	  派发（蛛网水死表杀的 3×3 帧扫触发组拆）——UpdateStalagtiteStyle style≠desired
195	  耗 Next(3) 走 pass 链流；CheckBanner 锚门 tileSolid≈solid||platform 近似。
196	- **连带战果**：#53 Smooth_World 旧 Hf/Sl 半砖债全系 #49 薄膜液体差下游——液体
197	  对齐后整段消失；m/s 链首差 #49→#58（Statues 域新暴露）。
198	- **附带**：#49 pass 头 oceanDepths 归水扫（cs:16222，唯 #49 有——#97 无，
199	  QuickCleanup 自有窗口版）settleWorldLiquids +oceanStrip 参接线。
200	- **方法论**：独立重放器（golden 8 通道 + JS frame/wire/GenSolid 界 + RNG(seed)
201	  pass 流）复现自差 → 连通域聚类（475 条单行薄膜=全局调度差指纹）→ 阶段化重放
202	  （薄膜全在 r0 成形 + numLiquid 顶帽监测）→ 缓冲器介入实锤。
203	- **教训**：「账面 1:1」的模块在容量边界路径（curMaxLiquid 帽、49998 帽）可能藏着
204	  从未触发的分支——大尺寸世界是天然的压力测试；调度序差在混沌系统（薄膜圆整漂移）
205	  里呈现为"处处轻微不同"而非单点错位。
206	
207	=====FILE: ai-parity-audit-2026-08-19.md=====
208	---
209	name: ai-parity-audit-2026-08-19
210	description: 六代理AI全量1:1审计~200条:当日修15项(694崩溃/鸭子海马仙灵瓢虫反向/仙灵逃逸/石巨人胜利倒置/蜂群速度表/batAI双段/蚁狮/史莱姆激愤表);台账docs/ai-parity-gaps-2026-08-19;★死亡=只积分不steering(原版共享积分段:93808)
211	metadata: 
212	  node_type: memory
213	  type: project
214	  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
215	  modified: 2026-08-19T07:05:14.159Z
216	---
217	
218	2026-08-19 六分区代理 AI 全量 1:1 审计(死亡退化+追击门×2、地面/小动物/飞行水生/Boss 全量×4),~200 条。台账=game/docs/ai-parity-gaps-2026-08-19.md(未修项+原版行号),当日修 15 项(测试 tests/ai-parity-batch-2026-08-19 + float-eye-dead-player + fish-behavior)。
219	
220	**★最重要方法论**:原版 NPC 位移积分在 AI 外**共享段**(`Collision_MoveWhileDry` NPC.cs:93808 `position += velocity`)——AI 分支被跳过 ≠ 冻结,而是按冻结速度继续滑行。本仓各 AI 须自调 moveAndCollide ⇒ **死亡分支一律"只积分不 steering"**(birdAI/vultureAI/duckFlyAI 已照此修;仍有一批 `!player return` 早退冻结在台账 A 区)。另:原版 `GetTargetData()`(:6817)死亡时返回 (0,0) 默认位——部分 AI 字面上朝世界原点飞,实用语义仍取"保持最后方向"。
221	
222	**当日修复要点**(细节在代码注释与台账文首):
223	- 694 水书宝箱怪冲刺段 `player!.cx` null 解引用=必崩(玩家死于冲刺 10t 内)
224	- 行为反向族:鸭子逐帧背向玩家+水陆变形死循环、海马水面折返取反(顶出水)、仙灵追人(应逃逸,引导态仅虫网释放 ai2=2)、瓢虫陆行慢 20 倍+翻转轴错、秃鹫死亡自造 cy−100 目标无限上飞
225	- **石巨人胜利条件倒置**(坏档级):应=本体死亡终战+自由头 249 恒无敌(:12151);曾满血续命+杀自由头终战
226	- AI_005 速度表(陨石怪曾 6 倍速)/batAI 第二段移动 11 类/史莱姆恒激愤表/蚁狮开火在 rooted 前/小动物站走计时互换+危险扫描每 tick+canHit+乌龟豁免
227	
228	**★全量修复批(同日,五代理并行)**:A-F 区 ~190 条全部落地(台账 docs/ai-parity-gaps-2026-08-19.md 已逐区销项,含各批"已修 N 项"清单)。测试:五批新回归 critter-parity-fixes 25+ground-ai-parity-fixes 37+flyer-ai-parity-fixes 30+boss-parity-fixes-a/b 各 31=154 例+首日 8 例;合并终验 181/181、tsc src 零错。要点:
229	- A 区系统性:dispatch 改传原始 player(死亡对尸体坐标运转);solenian 恢复态"复位同 tick 拉满"结构 bug;projDmgMultiLerp (difficulty−1)/2
230	- C 区:史莱姆 per-type 跳跃梯/空中转向/金属矿强化段/204 专家分支;近身扑跳族 15 型;远程族重写(292 四连发/216 双档/火星七型+伺服飞行);471 术士六态机/482 石壳/631 连发循环;昼行表重构
231	- B 区:跳档 num27 语义(1 格台阶 StepUp 不跳)/wet 碰撞盒语义/家域 50 格回头/金鱼雨天形态链(fishTransformationDuringRain,Game 敌怪轮)/鸟拉屎 PoopProj(飞行鸭同款主会话补接)/蜗牛双轴贴墙重做/气球真碰撞(落地滑行不爆)
232	- D 区:蜂群全核(619 血鱿鱼/远距增速/朝向基座/白天驱散表——★5 号仆从白天上飞驱散是原版行为,shimmer 测试场景须钉夜)/幽灵族移动核/骷髅王手五态机/620 地精鲨陆地夜射连发
233	- E 区:Retinazer 侧移拓扑/双子+骷髅王专家档/史王全核/蜂后专家 11 处/月总 Lerp 0.98 命名参数陷阱/光女连段表+攻击12/月亮事件弹道物理表+noTileCollide/DD2 索敌夺标/火星真难度
234	- F 区存疑全部证据链定谳(世花×0.9 补 Remap/飞碟−1 两代反编译 no-op/鲨鱼龙 PlaySound 库 4=NPCKilled_19);遗留登记 5 项见台账 F(groundPhysics ±1 钳=仓内旧约定翻动需独立批/S10 携物梯余档/弹-NPC whoAmI 通道/蜗牛 spriteDirection/均证据性缓议非近似)
235	- ★全库批跑教训:新测试在全量扫描时偶发负载假红(单跑稳定),flaky 判定先单跑×3;测试世界高 <140 触发世界底钳(StepUp/WetCollision 屏蔽)是"旧测试恰好通过"的隐藏根因
236	
237	相关:[[spawn-pool-aggro-audit-2026-08-17]](死亡寻路语义+AI_016 flag22) [[bunny-walk-frame-fix]](帧速档)
238	
239	=====FILE: xxxx-microresidual-final-clear.md=====
240	# XXXX 批（2026-08-19）：UUUU 移交微残终清
241	
242	## 交付四件
243	1. **#101 掷流 20196→165353/1663744**（五修）：营地两链帧掷族（SetTile(397,setSelfFrames)五连帧+PlaceWall五连SquareWallFrame+All(data)链 SetFrames 在 OnlyWalls 前）+矿爆点同族三处；GenVars.rockLayer≠Main.rockLayer（TerrainPass.cs:232 num4 独立字段，矿爆 Y 域用错 571→523）；**★Tile.actuator()(0x800)≠Tile.inActive()(0x40)两大旗标**——SolidTile 族读 !inActive() 生成期恒真（无置位点），致动位当 inActive 排除=致动格误判非实心（ST 探针 (2430,920) inact=False wire=True 定罪）；**薄冰斑 AddStructure 非 AddProtected**（CanPlace 不查 _structures），JS 误入保护图挡掉原版放行矿爆点。残 1%=**TrackGenerator.cs:136/151/158 WorldUtils.TileFrame(frameNeighbors) 帧链**（TrackPass 域，'a 3' 苔藓掷）移交。
244	2. **剑冢 HashSet 豁免撤销**：枚举=槽分配序，Add-only≡插入序；Subtract 后无 Add≡幸存者插入序≡JS Set——ShrineShape 本就逐位等价；全样本流（a/b+**d/n 双盲区通道**）剑段零分叉；"34.5k 剑冢掷"归因证伪（真源=①+矿轨）。
245	3. **#63 preferSmall 裁决**：spiders 语境**不可达**（IL +005C brfalse +151；+0063=spiders 两格支起点，UUUU"+0063 单格 frameY=54"误读）；残 2 格=波内装饰时序/门读微差（visit 序两侧一致），需 vanilla 分支级 SpiderProbe 收口。
246	4. **地牢帧归零**：压板 135 样式在 **frameY**（曾 frameX）；Place2xX（cs:39705）style*36 帧（DG_ITEM_STYLE 表接线，1410=style48）；全管线 bad=0。
247	
248	## 方法论
249	- Cecil InsertBefore 缓存锚=后插者离锚近（再踩）；ProbeLib.dll 须随织拷入 Resources（漏=MissingMethod 静默空世界）；hs.exe 系 -autocreate 跑前必 rm HOME 下全部 wld（含异名）
250	- 全样本流 span（d=NextDouble/n=裸 Next）：参数流对齐不保证值层对齐（盲区掷计数差=静默移位）
251	- 金标 102 出口态自采配方：tttt-app 副本+SW_TT_FR_PASSES="Water Plants"（pass 头=上一 pass 末态）
252	- rig 槽重放的帧基座=捕获期 JS 边界（slots≤50 不注金标帧）——帧修复验证须走全管线
253	
254	=====FILE: item-tooltip-parity-port.md=====
255	---
256	name: item-tooltip-parity-port
257	description: "悬停气泡1:1(GetLinesInfo :20488-20920):vi_武器伤害/暴击/速度档/击退档/渔力/镐斧锤力×5/耗魔/可放置·弹药·消耗品/材料/容器/Buff持续全量;数据坑:item.ammo在combat json非func;斧显示×5;官方中文坑:Container译'收集附近掉落物'"
258	metadata: 
259	  node_type: memory
260	  type: user
261	  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
262	  modified: 2026-08-18T07:08:55.243Z
263	---
264	
265	# 物品悬停气泡 1:1（2026-08-18 用户"相比原版缺了不少信息，武器还有攻击力"触发）
266	
267	**原版行链**（`MouseText_DrawItemTooltip_GetLinesInfo`，Main.cs:20488-20920，
268	行序严格）：名(稀有度色/×N) → 伤害[+类型后缀 LegacyTooltip 2/3/4/53/55] →
269	暴击%（近/远/魔三系，4 基础+装备/buff+词条） → 速度档（useAnimation 分档
270	≤8/20/25/30/35/45/55/∞ → tip6-13） → 击退档（0/≤1.5/3/4/6/7/9/11/∞ →
271	tip14-22） → 渔力+需鱼饵/鱼饵力 → 可装备 → 时装 → 防御 → 镐力/斧力(×5!)/
272	锤力 → 恢复生命/魔力 → 耗魔(×manaCost) → 可放置/弹药/消耗品(else-if!) →
273	材料 → 容器/线触发 → 自带说明(ItemTooltip.*) → Buff 持续 → 词缀差分(绿/红)。
274	
275	**Why（旧实现缺口）**：只有名/词缀/legacy 工具行/防御/恢复/静态说明——
276	vi_ 武器**伤害行整缺**（damage 在 combat json 不在 def.tool）、暴击/速度/
277	击退/渔力/镐斧锤/耗魔/可放置/弹药/材料/持续全无。
278	
279	**样式批（同日 review）**：底=Inventory_Back13 九宫 × (23,25,81)×0.925
280	（:20252-20255；与面板同贴图不同染色，tooltipBgDataUrl 按 (w,h) 烘焙缓存 +
281	素材未就绪 onload 一次性补刷）；文字=MouseText 字体栈+1px 字影
282	（DrawColorCodedStringWithShadow :20256）；名称行**不加粗**（vanilla 同字号
283	渲染）、堆叠格式 " (N)"（GetHoverName :420-427 非 "×N"）；定位槽右锚+视口
284	18px 钳制（:20241-20250）。探针 _tpstyle 四断言（九宫/阴影/字体/堆叠）。
285	
286	**How to apply（src/ui/itemTooltip.ts 纯函数 + UI 消费）**：
287	- 数据面坑：**item.ammo（是弹药旗）在 combat json**（func json 箭族缺）；
288	  **斧力显示 = axe×5**（铜斧 axe=7 → 35%）；材料旗无数据 → VANILLA_RECIPES
289	  原料反查近似；可装备 = itemstats acc/hs/bs/ls + equipKind hook/mount/pet/
290	  light/cart。
291	- 伤害行乘区 = combat.damage × 词缀 dmg × player.damageMult(kind)；
292	  暴击 = 4 + player.critChance(kind)（equipStats 不含武器→与原版"playerClassCrit
293	  −选中武器+悬停武器"同式）+ 词条 crt×2；耗魔 × manaCostMul。
294	- l10n：LegacyTooltip.0-61 / CommonItemTooltip.* / GameUI.* 全在 zh 包；
295	  ★官方中文坑：`CommonItemTooltip.Container` 译作"接收到信号时会收集附近的
296	  掉落物品"（不是"容器"）——断言勿按直觉词。
297	- 测试 tests/item-tooltip.test.ts 10 条（tag 断言，l10n 未载回退键名）；
298	  探针 scripts/_tooltipprobe.mjs 10/10（真实 UI.showTooltipFor + spawnDrop
299	  注入法）。ITEM_DEFS 的 id=数组索引；vid 反查用 def.vid ?? 正则。
300	- **低频二批全接入（2026-08-18 用户令"低频也必须完整"）**：
301	  ①亮度脉冲=mouseTextColor 190↔255 ±1/tick（:18064-18075）→ startTooltipPulse
302	  rAF brightness 驱动，mouseleave cancel；②yoyo 商标位（:20845-20853 悠悠球
303	  11 件 3262/3282-3286/3315-3317/3291/3389）→ OneDropLogo.png 五层 drop-shadow；
304	  ③鞭速度档例外（:20545 `!summon || IsAWhip[shoot]`——WHIP_PROJS=aiStyle165
305	  全 18 枚）；④tileWand 消耗行（tip52）：表 {832→木材9,933→9,932→骨154,
306	  1129→蜂巢1124,3360/3361→红木620}——★Dirt Rod 114 无 tileWand（发射移土弹），
307	  勿想当然登表；⑤研究行（:21163-21178 旅程 difficulty==3 →
308	  Research.tryGetSacrificeNumbers → CreativeSacrificeNeeded 紫 JourneyMode）；
309	  ⑥商店价格行（:20309-20402 Game.npcShopOpen 门 → 买入 value×5；
310	  币名=LegacyInterface.15-18 非击退档！四档色 铂220/金224/银181/铜246）；
311	  ⑦专家/大师行（rare -12/-13 → GameUI.Expert/Master）。
312	- 鞭数据坑：combat json 鞭族是**残缺条目**（{noUseGraphic} 非 null 但无 damage）
313	  → `c ?? 兜底`够不着，whipsJson 存在时**无条件覆写**（spread+override）。
314	- 遗留极小项（视觉细节）：社交栏 tip0/61、任务品 inter65、特殊种子行
315	  （CursedByPlantera/DD2 未通关/misc104）——这些在原版悬停几乎不可见分支。
316	
317	**review 批修（2026-08-18 三审）**：
318	- ★商店价语义：货架条目=买入价（expectedPrices 全链：快乐度×/折扣0.8×/
319	  银行家舍入，Game.shopEntryPriceOf 新增反查）；**非货架自带物在商店内=卖出价
320	  value÷5 min1 ×stack**（:20312 isAShopItem 分流 + :20324-20326 ÷5）——曾
321	  一律 value×5 买入。价格行 UI 注入 stack。
322	- ★暴击=武器自身 crit（combat json 缺省 4，火枪 95=6）+装备+词条×2——
323	  曾恒 4（高暴武器显示偏低）。原版 num2=classCrit−选中crit+悬停crit 化简。
324	- ★击退档含玩家加成：melee+kbGlove(力量手套)×2、kbBuff(泰坦108)×1.5
325	  （:20195-20210，UI 读 equipStats.kbGlove/BuffType.Titan）。
326	- ★伤害行×ToolTipDamageMultiplier（ItemID.cs:246 回响族 10 件 ×2 显示）。
327	- ★prefix 差分行序改原版链：伤害39→速度40→暴击41→魔力42→大小43→弹速44→
328	  击退45（曾击退排第 3）。vanillaPrefixes.prefixLines 全局改（UI 槽位行同序受益）。
329	- ★expert/master 行序归位：原版在 prefix 差分**之后**（:21140s），曾错排在
330	  统计行里 → expertMasterLines 尾部字段。
331	
332	**终清零批（2026-08-18 四审）**：
333	- ★tileBoost 范围行（tip54 :20703-20715）：表 {509/510/511 扳手=20,
334	  851 多彩=20, 852 工具腰带=1, 2340/2341 矿车轨=5/2, 1305 The Axe=1}——
335	  itemfunc 无 tileBoost 字段（玩法侧 useWireTool 硬编码 20 已同值）。
336	- ★任务鱼行（inter65 :20663-20666）：ctx.anglerQuestItemId=Game.
337	  anglerQuestItemId()（当日任务鱼，种子^天数确定性掷）注入。
338	- ★套装奖励行（tip48 :21138-21143）：悬停护甲 + equipStats.setBonus.name
339	  → l10n ArmorSetBonus.*（67 键在 zh 包）；行序在词缀差分后。
340	- ★社交槽双行（tip0+tip1 :20508-20513）：where=dye/miscDye → UI 传
341	  socialSlot。★接口坑：并行编辑致 socialSlot 双声明 tsc 重复错——接口字段
342	  只留一处。
343	- 剩余永不达项（已核）：questItem 数据旗（本仓 angler 链走 id 表非物品旗）、
344	  DD2 misc104（3818+ 门 gate 未消费）、CursedByPlantera、特殊种子行——
345	  均为原版死码/特殊种子域。
346	
347	**用户报障批（2026-08-18 气泡透明感 + 数字键失效）**：
348	- ★透明感根因 = 脉冲 brightness 打在**整元素**上（面板一起呼吸变暗）——原版
349	  :20256 逐行 `lineColors[k] *= mouseTextColor/255` 只乘【文字色】，DrawInvBG
350	  面板色恒定。修 = 行内容包 .sw-tooltip-lines 容器，脉冲 filter 打文字层；
351	  startTooltipPulse 先清整元素历史 filter。
352	- ★数字键"失效"= refreshAllNow 里 achAdvisor.update() 抛错把 rAF 回调整体
353	  炸掉 → refreshHotbar 永不执行（selected 实际已变而画面不动）。修 =
354	  refreshHotbar 提到最前 + advisor try/catch 自摘。★教训：rAF/事件回调里
355	  QoL 件异常会静默吞掉后续关键刷新——关键刷新前置。
356	- 探针 _ttfix.mjs 9 绿（面板 filter 空/文字层脉冲在动/Digit3→2/7→6/0→9/
357	  1→0/refreshAllNow 无抛）。TS cast 勿写进 .mjs 探针（as any 炸 node 解析）。
358	
359	**不透明度真根因终案（2026-08-18 三轮报障）**：透明感的元凶是 tint 循环
360	alpha 通道误乘**红通道** `d.data[i]*tmul[3]`（应为 `d.data[i+3]*tmul[3]`）——
361	深蓝底红通道≈23 → alpha≈22 = 近全透明。三轮演变：①初报"几乎透明"（alpha 22
362	+ 亮度脉冲打整元素叠加）②修脉冲后"依然过透明"（仍 alpha 22）③铺不透明底后
363	"过于不透明"（alpha 255）→ 回退实底时暴露 typo。修复后回到**原版真值 0.925**
364	（alpha 236）——此前 0.925 从未真正渲染过。★教训：像素循环改 alpha 前先探针
365	采样输出（_ttopaq：dataURL 页内重绘 getImageData 采样，比截图可靠）；
366	三轮报障的"折中值"思维错了——该找根因而不是 0.925↔1.0 之间找点。
367	
368	**用户禁令（2026-08-18）**：禁止以"低频"为由不接——所有原版行为必须移植
369	完整，低频项也计入台账与记忆。
370	
371	关联 [[cursor-item-icon-port]]（指针图标）/ [[behavior-parity-batch-2026-08-17]]。
372	
373	=====FILE: dualwindow-iosurface-exhaustion.md=====
374	---
375	name: dualwindow-iosurface-exhaustion
376	description: "双开崩溃根因=GPU进程IOSurface张数耗尽(字节无关,16x16也失败)非显存预算;force-gpu-mem-available-mb=cc tile预算纯安慰剂;--disable-gpu全域软渲染双窗0失败"
377	metadata: 
378	  node_type: memory
379	  type: project
380	  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
381	  modified: 2026-08-19T07:05:11.812Z
382	---
383	
384	2026-08-18 用户实报"npm run play 冷启 Chrome(带 --force-gpu-mem-available-mb=16384)
385	双开联机依然 GPU 爆"→ 三线取证 + 三组 A/B 对照,机制钉死。
386	
387	## ① 旗标是安慰剂(Chromium 源码实证)
388	`--force-gpu-mem-available-mb` 定义在 `third_party/blink/common/switches.cc:104`,
389	官方注释:**"Sets the total amount of memory that may be allocated for GPU
390	resources in cc"** —— cc=合成器,只管 tile 光栅资源预算。转发链
391	`render_process_host_impl.cc:3955`(blink::switches 转给渲染进程),与画布后备
392	存储/WebGL 纹理/SharedImage **零关系**。Chrome 151 二进制里
393	`force-gpu-mem-available-mb`/`force-gpu-mem-discardable-limit-mb` 字符串都还在
394	(strings 实锤,开关没删但也不管我们的故障)。**教训:开关存在≠开关管用,
395	必须找到消费点读注释。**
396	
397	## ② 真根因=IOSurface 张数/内核资源耗尽,字节无关
398	双窗探针(puppeteer 系统 Chrome 同实例双 tab 大世界)stderr 铁证:
399	```
400	ERROR:ui/gfx/mac/io_surface.cc:273] Failed to allocate IOSurface of size 16x16.
401	ERROR:...iosurface_image_backing_factory.mm:386] CreateSharedImage: Failed...
402	ERROR:...command_buffer_proxy_impl.cc:488] GPU state invalid → 上下文死
403	```
404	**16x16(1KB)都分配失败**(64GB 机器!)——是按"张"计费的内核资源(mach
405	port/fileport 类)耗尽,非显存字节。FD 排除(lsof GPU 进程仅 36 个,系统上限
406	245k/进程)。每张加速画布后备=一个 IOSurface;双窗把 GPU 进程(共享)的张数
407	顶穿→分配失败→contextlost→恢复重分配→再失败=风暴。单窗不炸=张数在阈下。
408	
409	## ③ 三组双窗 A/B(headless 同负载,scripts/_dualgpu-probe.mjs)
410	| 模式 | contextlost | IOSurface 失败 | 熔断 |
411	|---|---|---|---|
412	| GPU 模式+play 旗标 | 9 | 27 | 3 |
413	| 游戏内 renderMode=cpu | 7 | 6 | 2 |
414	| **--disable-gpu 全域软渲染** | **0** | **0** | **0** |
415	- renderMode=cpu 只减 4.5×:chunk 画布 willReadFrequently→SHM 后备,但主画布
416	  合成链仍产 IOSurface(印证"willReadFrequently 后备仍进 GPU 进程"旧结论)。
417	- 游戏自身熔断器有效:10s 内 3 丢失→冷却+chunk 上限缩 64→风暴不再升级(两轮
418	  GPU 模式都是"受控慢渗"而非 16k/s 真窗风暴;headless 视口小+熔断早介入)。
419	- `--disable-gpu` 全干净=连合成器都不产 IOSurface。已做成 `npm run play --soft`
420	  (SW_PLAY_SOFT=1):双开联机测试就绪档(代价帧率降,单窗别开)。
421	
422	## ④ 结论/出路
423	- **没有任何 Chrome 旗标能救 GPU 模式双窗**(overlay 开关已从 151 移除)。
424	- 双开测试三选:**npm run playsoft**(最稳,见⑤)/ 第二窗 renderMode=cpu
425	  (可用但有残留)/ 单窗口双世界(正解,方案已给用户:同源 2×2px iframe +
426	  headless Game + bot,GPU 开销恒等单窗,等待用户拍板落地)。
427	- 游戏侧最大单点=**chunk 烘焙画布张数+churn 双料元凶**:每 chunk=墙层+tile 层
428	  **两张** 256² canvas(renderChunkInner 新建);稳态 35 chunk=70 张;移动期
429	  flushDirty 4 chunk/帧=**每帧 8 张新画布**(GPU 进程 ~480 次 IOSurface
430	  分配/释放/秒,双窗翻倍)。**chunk atlas 打包**(4×4 cell/1024² 页,墙/tile
431	  各一摞;重烘焙=原位重画 cell 零画布生命周期)→ 活张数 70→~10、churn→0,
432	  是 GPU 模式下同方向的正手;终局=渲染器 v2(WebGL2 纹理化)。
433	- 单页稳态基数:DOM canvas 3 + chunk 70(35 对) + vimages 231(CPU 位图)。
434	
435	## ⑤ --disable-gpu 有头生效性验证 + npm 参数坑(2026-08-18 用户实报)
436	用户反馈"play --soft 启动后 chrome://gpu 仍全硬加"→ 两层原因:
437	1. **npm 吞参**:`npm run play --soft` 的 --soft 是 npm 自己的配置,不传给脚本!
438	   必须 `npm run play -- --soft` 或 env SW_PLAY_SOFT=1。已加 **`npm run
439	   playsoft`** 专用脚本免坑(package.json)。
440	2. 有头 Chrome 151 实测(puppeteer headless:false + UNMASKED_RENDERER):带
441	   --disable-gpu → **WebGL 上下文直接拿不到**(全禁,旗标有效);无旗标 →
442	   ANGLE Metal Apple M5 Pro。用户那次 = 旗标没进进程(1 的锅)。
443	   chrome://gpu 全绿即旗标未吃到;chrome://version 看 Command Line 可复核。
444	   探针 scripts/_disgpu-check.mjs。
445	
446	## ⑥ 游戏侧优化落地(2026-08-18 晚,用户拍板"开始大型优化")
447	**三刀全落地,探针验证:**
448	1. **chunk atlas 页化**(ChunkCache.ts):每 chunk 2 张 256² 画布(稳态 70 张/
449	   满额 768 张,重烘焙=新建)→ 墙/tile 各一摞 1024² 页(4×4 cell),cell 池
450	   复用,重烘焙=clip+translate 原位重画。活张数 446→28(223 chunk 实测);运行
451	   期画布创建≈0(回头路二遍 9 张 vs 旧每遍 ~6000)。★跨格外溢绘制(墙 EXT=1/
452	   树 EXT=6 负坐标)必须 clip 在 cell 内;tintRegion 区域坐标要页内绝对 ox+lx*TILE;
453	   ChunkPair 增 sx/sy/cell,Renderer drawChunkGrid 改 9 参源矩形(4 参=整页
454	   误绘,类型合法的静默 bug!)。bakeChunkInto(cell<0)同函数喂独立画布=E2E
455	   逐字节对拍 8/8 的构造保证。dispose=唯一毁页点(setRenderMode→cbOnGpuRecover
456	   →dispose→按新模式重建)。
457	2. **cloudTint 染色画布池**(SkyRenderer.ts:1404):canvas 出生栈普查实锤的
458	   最大隐藏工厂——键含逐帧漂移 RGB+ImageBitmap 无 .src(恒 undefined 跨纹理
459	   碰撞)→ **每帧每云新建画布 ~340 张/秒**(12s 移动 4091 张,泄漏大扫除年代
460	   漏网:活集被 64 上限"界定"但出生率无界)。修=色键量化步进8+WeakMap 纹理id
461	   +LRU 淘汰画布进 free 池原位重画 → 出生归零。
462	3. 普查残余良性:frameHasContent 帧探测(willReadFrequently=SHM 不占 IOSurface,
463	   首见有界)/iconUrl/tintedSprite ≤6 张/12s。
464	**验证**:_chunkatlas-probe 4/4(对拍 8/8 逐字节+回头路 churn≈0+页数界);双窗
465	GPU 对照:IOSurface 失败 27→8(-70%),残余失败尺寸=1280×800(视口/合成器
466	swapchain,游戏外);contextlost 计数 7→18 属两页分布变化(B 基线全程 0 = 分配
467	顺序偶然),无风暴升级。**教训:①"泄漏审计"必须量出生率不只活集——池化
468	上限会掩盖 createElement 风暴;②canvas 出生栈普查(createElement patch+聚栈)
469	应成为渲染改动的常规探针;③类型合法 ≠ 语义正确(4 参 drawImage 画整页)。**
470	探针:_chunkatlas-probe.mjs(四项)/_canvasborn-probe.mjs(聚栈)。
471	
472	## ⑦ review 三修 + canvas 哨兵(2026-08-18 深夜,用户令"review 避免再发生+建早期抓取")
473	**自审揪出 2 真 bug + 1 效力回退:**
474	1. **油漆 pass 双重偏移**:bakeChunkInto 挂 translate(ox,oy) 而 tintRegion 回写
475	   用页内绝对坐标 → 落 (ox+px,oy+py),ox>0 的 cell 油漆被 clip 静默吞。对拍探针
476	   没抓到=新世界无油漆(paint 全 0)→ **对拍必须含油漆**(探针①' 涂 202 格红漆,
477	   cell=5 偏移位 vs 独立目标 diff=0 锁死;修=tintRegion 读写坐标分离
478	   readX/readY+writeX/writeY)。★教训:对拍覆盖面必须包含"改动触碰的每个 pass",
479	   空数据路径的逐字节一致≠全路径一致。
480	2. **cloudTint 池化复用双坑**:同尺寸复用残留上一轮 destination-in(首绘变擦除)
481	   +旧像素透过透明区串色 → 首绘改 globalCompositeOperation='copy' 整体替换;
482	   free 池封顶 8(工作集收缩时 surplus 弃,防池自身无界)。
483	3. **软收缩效力回退**:shrinkChunks 只还 cell 不放页(每页 2×4MB 背板滞留)→
484	   pageUsed[] 每页计数+trimFreePages() 尾部空页回收(Game.shrinkChunks 接线);
485	   bakeChunkInto 拆 bakeChunkBody+try/finally restore(异常逃逸=共享页残留
486	   clip+translate,下次烘焙 2×错位——独立画布时代异常自含,页化后必须显式复位)。
487	
488	**CanvasWatch 常驻哨兵**(src/render/CanvasWatch.ts,main.ts 装载,?cwatch=0 静默):
489	patch createElement 计数+聚栈,console.warn 带出生栈样例(进 __swWarns/F5);
490	renderLog/F5 快照新增 canvasWatch 段。★判据三轮真机标定才收敛(哨兵标定笔记):
491	①短窗速率(20/s×2 窗)误伤正常跑图(首见帧探测单窗 30/s);②滚动总量(2000/60s)
492	误伤进世界洪峰——SpriteAtlas.hardAlpha 一次性单窗 1621 张与事故 1700/窗不可区分;
493	③终版=【连续窗双档】:≥300 张/窗连 3 窗(急性)/≥100 张/窗连 6 窗(慢性),
494	一次性构建 1-2 窗即衰减天然免疫,真机零误报。哨兵自身初版还有 lastWarnAt=0
495	把首报挡进冷却的 bug(单测当场抓住,改 -Infinity)——★哨兵也要被测。
496	另:hardAlpha 进世界单窗 1621 张是合法一次性构建(表硬 alpha 处理,常驻资产),
497	非泄漏;真泄漏的判别特征是逐窗持续不衰减。
498	E2E:_chunkatlas-probe 5/5(含油漆对拍)+ _canvasborn-probe 增哨兵装/静默验证
499	(栈顶多一层 CanvasWatch wrapper 属预期)。
500	
501	## ⑧ 云染缓存二轮:真 LRU + cap 24(2026-08-18 用户"云染缓存在干啥,优化一下")
502	帧扫描探针(_framescan-probe:drawImage 按帧聚去重源)实测常驻账后点名:
503	cloudTintCache FIFO+64 把历史冷桶全留下(cap 打满 64 张常驻画布),而真实工作集
504	= 同屏云色桶 ~10-16。修:命中重插 Map 尾(真 LRU,冷桶先走)+ cap 64→24
505	(miss 重染成本=3 次 ~200×100 drawImage,超工作集也无感)。实测 64→24,
506	每帧绘制源不变(静止 11/移动 ~36 张),churn 仍归零,哨兵零误报。
507	★帧扫描数据留档:每帧绘制源 canvas 静止 p50=11/移动 ~36(移动段含烘焙表源
508	混入 ~25 张);bitmap 源 7(CPU 侧不占 IOSurface);常驻账 DOM 3+chunk 页 12
509	+云染 24+单例 ~5。四层口径:绘制源/常驻持有/每帧新建(≈0)/bitmap。
510	
511	## ⑨ 云透明根因+哨兵首战+云 GL 化(2026-08-18 深夜二)
512	**"好多云不渲染"根因 ≠ 渲染层**:drawCloudPass 的 globalCloudAlpha 曾接
513	`max(wr.cloudAlpha, 墓园×0.92)×atmo`——wr.cloudAlpha 是【雨云浓度】(晴天恒 0)
514	→ 晴天云全透明。原版真身(反编译实证):Main.cs:58752 `num5 =
515	SkyManager.ProcessCloudAlpha()×atmo`,ProcessCloudAlpha = 1×Π(激活
516	CustomSky.GetCloudAlpha()),默认恒 1,仅月总/四塔天空 override 1-fade
517	(MoonLordSky.cs:72),**墓园不压云**。修 = globalCloudAlpha = atmo 直取。
518	★教训:注释引用的公式要回反编译核对——"max(cloudAlpha,墓园)"是把某 CustomSky
519	内部式误当全局门;该 bug 期间云从未显示过,坐标/染色从未被真正检验。
520	
521	**canvas 哨兵首战告捷(用户真机)**:生产构建抓到 37-63 张/秒持续 30 窗,
522	压缩栈 new Ap→Ni.render→rt.render。定位 = **TileFlames._tintCache**:键含
523	火光连续 rgb(光照驱动) + imgId 裸读 .src(ImageBitmap 恒 undefined→跨表串色,
524	注释声称"src 唯一"在 bitmap 时代失效) + 超 512 整表 clear(下帧全量重烘雪崩)。
525	修 = WeakMap 实例 id + rgb 量化步进 8 + 逐条淘汰。tintedSand 查实 v 已 8 档
526	量化(键有界)非凶手。
527	
528	**云 GL 化落地**(用户拍板"直接 GL 化,不支持再回退 canvas2d"):
529	- 新 `src/render/CloudGL.ts`:WebGL2 逐精灵批绘(顶点 [x,y,u,v,r,g,b,a],
530	  CPU 预乘顶点色,fragment `t×vCol` = 原版 spritebatch.Draw(Color) 精确色语义);
531	  一张视口大小离屏画布同帧双 pass 复用(远云 sky.draw 内/近云 biomeBg 后,
532	  pass 间 clear);预乘上传+mipmap+LINEAR;preserveDrawingBuffer 同款合成。
533	- SkyRenderer.drawCloudPass 双轨:GL 主路径(quad 推送)/2D cloudTint 兜底;
534	  ensureCloudGL 死亡 5s 退避;Renderer.setRenderMode/�dispose 接线
535	  (cpuRender 关+释放);`?cloudgl=0` 逃生门;quadsLastPass 观测量。
536	- 验证:GL 路径截图 6 朵云正常;?cloudgl=0 兜底 3 朵云颜色正常无串色
537	  (copy 修复实证);哨兵静默;26 测试绿。
538	- 收益:GL 路径下 cloudTint 缓存归零(24+8 画布→1 张 GL 画布+纹理恒定);
539	  量化近似消失。
540	
541	**★仪表教训(两次误报"没云")**:①"覆盖度"用边缘检测(邻域差分)——平滑
542	色块云对它几乎不可见,必须用"与期望渐变的偏差"或直接看图;②"取最大画布"
543	在面积平局时抓错(主画布与光照画布同 1280×800)——必须 renderer.canvas 直取;
544	③GL readPixels 的 y 原点在**底**(顶行=height-1),两次采错行。
545	**视觉问题的终极判据 = 看截图(Read 图像文件),指标只是导航。**
546	
547	## ⑩ 哨兵二捕:BiomeBackground 昼夜染色(2026-08-19,用户再报 61/s 急档)
548	用户真机新构建再报:≥300/窗 3 连,61/s,栈 = 普通函数 `Dp←Wi.render←rt.render`
549	(上一轮 `new Ap` 是构造器形态,TileFlames 修复虽对症但非此栈真身)。真凶 =
550	**BiomeBackground.drawTiledTinted**:键 = `im.src`(bitmap 恒 undefined)+ 昼夜
551	tint `.toFixed(2)`(晨昏连续漂移→每帧新键)+ `>64 整表 clear()`(清光全重烘
552	=永远 miss 的雪崩)。触发条件 = 晨昏段(tint≠(1,1,1) 才走烘焙;白天直画)。
553	修 = texId + tint 步进 8 量化 + 逐条淘汰;黄昏强制复现(CB_DUSK=1)实证归零。
554	**同族清剿**:全仓扫"键内 .src"→ Portal/PortalGunBolt(帧染色)/
555	SkyRenderer.tintedFlareSprite(镜头光斑)/GLSpriteLayer.drawRect tag 四处同病
556	(碰撞型:画错图/串色)→ 统一 `src/render/texId.ts`(WeakMap 实例 id)接线。
557	★方法论:①哨兵的栈形态(有无 new)可区分函数/构造器;②"连续值键+整表
558	clear()"是最毒组合(清光=100% miss);③bitmap 时代"键内 .src"= 一类扫除
559	模式,已全仓清零,新代码一律 texId()。
560	
561	## ⑪ 哨兵三捕:tintedSprite 敌怪/掉落物光照染色(2026-08-19,主犯落网)
562	用户新构建再报(107 连窗≈9 分钟 60/s,暂停中持续,栈 `new Fp` 构造器形态——
563	BiomeBackground 修复后真凶露脸)。慢加载拉长复现(全部 vanilla 图随机延迟
564	300-900ms+90s 采样+中途暂停 30s):**Renderer.tintedSprite ← drawEnemy 612 张
565	/90s**——键含光照染色 color(连续漂移)+ `>1024 整表 clear()` 雪崩(第四个
566	同族据点,敌怪每个每帧调)。修 = 色键量化步进 8(烘焙用桶内首色,闪白瞬态
567	不受影响)+ 整表 clear→逐条淘汰。修后 612→4 张(99.3%)。
568	**"光照染色类"缓存家族至此全部清剿:cloudTint(天色)/TileFlames(火光)/
569	BiomeBackground(昼夜)/tintedSprite(光照)——共性 = 键含连续漂移的光照
570	派生色 + 无量化 + 整表 clear 或无上限。新写染色缓存三件套:texId+量化步进8
571	+逐条淘汰;池化仅高 churn 场景需要。**
572	探针:scripts/_slowload-probe.mjs(慢加载+暂停 90s 聚栈——暂停中持续 = 渲染
573	循环类工厂的特征签名)。
574	
575	## ⑫ 哨兵三捕真凶更正:GLSpriteLayer 初始化失败每帧重建(2026-08-19)
576	用户纠正"确定是最新构建"点破误判:tintedSprite(方法形态)修复真实但非用户
577	60/s 的主犯——用户栈 `new Fp` 是【构造器】形态。真凶 = **bg GL 路径的
578	diedAt=0 洞**:WebGL2 初始化失败(playsoft `--disable-gpu` 下必失败;或
579	上下文数满被浏览器拒发)时 GLSpriteLayer 构造器 unavailable 且 diedAt=0 →
580	消费方退避判 `now-0>5000` 恒真 → **每帧 dispose+new GLSpriteLayer(构造器
581	createElement)= 60 张/秒**,暂停中持续(渲染循环不停),与用户日志全吻合。
582	dev 复现不了(WebGL2 可用)——须 `--disable-gpu` 复现(canvasborn-probe 的
583	CB_ARGS)。修三层:①GLSpriteLayer 构造器三处失败分支补 `diedAt=now`;
584	②Renderer.acquireGL() 统一获取(死亡 5s 退避/初始化失败 30s 闩,bg+map
585	两处消费点接线);③setRenderMode 回切 GPU 时重置闩。修后 --disable-gpu 下
586	12s 移动期 ~25 张零重建。
587	**★教训:①栈形态(有无 new)是硬证据,方法/构造器两条排查线别混;②"复现
588	不了"先问测试环境与用户差在哪(playsoft!);③退避判据的初值语义(0=永不
589	退避)要显式审。** 附带:worldgen worker 偶发 "process is not defined"
590	(pass 58/59 终清理)再次出现,属已知 process.env 进 worker 坑家族,另行处理。
591	
592	## ⑬ ioreg 检测法不可用
593	用户转来的报告提 `ioreg -n IOSurfaceRoot -w 0` 数 IOSurface——实测只输出设备
594	树根,不列 surface 条目(需 root 且新版结构已变),当泄漏检测不可靠,勿依赖。
595	
596	探针:`scripts/_dualgpu-probe.mjs`(DGP_MODE=cpu/gpu、DGP_FLAGS、DGP_SECS;
597	renderMode 钉死防 auto 降级掩盖)、`scripts/_canvascount-probe.mjs`(张数普查)。
598	经 run-diag 跑,SW_ORIGIN 指私有 52xx 实例。
599	
600	## ⑭ 双开再爆+TintAtlas 染色图集(2026-08-19)
601	用户实报"昨晚 4-5 开没事,今天 2 开崩"(trace 202MB:GPU 任务全 45µs 碎片=
602	非算力;console:熔断→冷却→再熔断环+CloudGL dispose 的 INVALID_OPERATION 刷屏)。
603	同日并行会话正改 worldgen/AI(vitest 32 失败全是他们的种子哈希 checkpoint 中间态,
604	渲染链测试绿)。
605	
606	**盘点(_iosurface-inventory/_combat 探针,存档现场)**:静息态 DOM 5 张(主
607	+光照+探针覆盖层+2 小 UI)+ chunk 页 23-25 张 + glfx 6 纹理 17.9MB;战斗态旧
608	实现 tintCache 可冲 **1024 张独立 canvas**——按张计费下的头号大户。
609	
610	**TintAtlas(src/render/TintAtlas.ts)**:染色变体从"每条一张 canvas"合并进
611	≤4 张 512² 共享页(shelf 行打包+free-list 最优适应分裂+LRU 逐出冷 16 条重试);
612	★bake 回调在**私有 scratch** 上作画再整块 blit——destination-in/getImageData
613	等全画布语义绝不能直接上共享页。tintedSprite(乘法族)/lerpSprite(逐像素族)
614	两族全迁,~14 消费点 drawImage 改 9 参(TintRect{c,x,y,w,h};bake null=超大
615	精灵/图集满 → 调用方跳过该层兜底)。实测 41 变体=1 页(旧=41 张)。
616	GLSpriteLayer/CloudGL dispose 补 isContextLost() 守卫(死上下文 delete 只会
617	刷 INVALID_OPERATION)。
618	
619	**用户否决跨实例方案**:"不要这种降级的,从我们自己出发"——BroadcastChannel
620	互感缩预算(GpuBudget)已写完又整体回滚;方向定为**单实例自身减量**。
621	剩余候选:CloudGL 并入 GLSpriteLayer(省 1 个 GL 上下文+背板)、cloudTint 2D
622	兜底(24+8)、TileFlames、tombstone/minimap skin 小家族、MAX_CHUNKS 384
623	(24 页)再评估。
624	
625	**"染色不是迁 GL 了吗"勘误**:GL 化的是**背景层**(BiomeBackground→BGBlit
626	uniform,并行会话完成;2D 兜底缓存 64 条)与**云**(CloudGL)。实体侧染色
627	(NPC colorRGBA pass/物品 color/gore/glow 轨道/鹿角怪/月总 twoPass/血条)必须
628	逐精灵交织在 Canvas2D 实体链内——GL 层每帧只合成一次,没法逐实体穿插——所以
629	一直是"每变体一张 canvas"形态,这次才用图集合并。
630	
631	## ⑮ playtrace 取证档 + 崩溃日志铁证 + 写一次缓存恢复 bug(2026-08-19 午)
632	**npm run playtrace**(play.mjs --trace):不经 open 直接 spawn Chrome 二进制,
633	`--enable-logging=stderr --log-level=1`,stderr 落 `game/logs/gpu-stderr-<时间戳>.log`。
634	Chrome 行自带 `[pid:tid:MMDD/HHMMSS:severity:file(line)]`——DevTools Performance
635	两份 trace(20s/24.5s)都只录到"健康侧"(呈现持续到录停、无死亡事件,被录页
636	≠ 崩溃窗),真铁证永远在 stderr。
637	
638	**崩溃日志钉死**(gpu-stderr-2026-08-19-04-26-00.log):12:26:41.613 一张
639	**64×128**(角色合成级小图)分配失败→CreateSharedImage 失败→`Restarting GPU
640	process due to unrecoverable error. Context was lost.`=GPU 进程整死;恢复中
641	12:26:59 又一张 64×128 再死;12:27:04-07 第三次(108×70/256×104/238×72×2
642	+ Invalid mailbox ×3)。全程仅 6 次分配失败——张数预算卡死时小图也过不去,
643	每次失败都杀整个 GPU 进程。
644	
645	**"崩溃后角色贴图不恢复"根因**:写一次烘焙缓存画布(PaperDoll 角色合成等)
646	的后备随 GPU 进程死亡蒸发,永不重画——每帧重画的层天然自愈,写一次层全灭。
647	PaperDoll 的 clearPaperDollCache 早就存在且注释写着这病症,但只挂在进出世界,
648	**没接 contextlost**。修 = Renderer.onLost(主画布+window 双挂点)首次丢失即
649	统一失效扫:clearPaperDollCache/tintAtlas.dispose/sky.clearCloudTintCache/
650	clearAmbientTintCache(并行会话新加的 AMB_TINT_CACHE 同款风险,顺手接)/
651	biomeBg.clearTintCache/clearTileFlamesCache/tombstoneCache——清前 width=0
652	先还表面。E2E(合成 contextlost):tintAtlas 5 条/1 页→0/0 ✓。
653	
654	## ⑯ 第二份崩溃日志 + 基数压缩第一批(2026-08-19 午后,用户拍板 1+3 先做/2+4 登记)
655	第二场(gpu-stderr-...-04-37-51):启动 34s 即触顶——首败 52×26(HUD 小图)→
656	**Invalid mailbox ×487 跛行 11s**→恢复分配 5 连败(1088×64/3040×448/1088×864/
657	32×821/32×545×2)→64×128(角色合成)终败="Restarting GPU process"。与首场差别
658	=先跛行后死;预算比上午更满。
659	
660	**已落地**:
661	1. MAX_CHUNKS 384→192(-24 张/窗)。★陷阱:`Game.afterWorldLoad` 每次进世界
662	   **硬写回 384**(08-18"回满档"修复)——静态改 192 被静默覆盖,探针读运行时
663	   才暴露。修=单一事实源 `BASE_MAX_CHUNKS=192`(静态初始化+afterWorldLoad
664	   回满+熔断减半同源)。★改类静态常量必须 grep 全部运行时写入点。
665	2. HUD 防御盾 2×52×48 canvas→img+dataURL(模块级 52×48 scratch 烘焙按
666	   (难度列,辉光) 缓存 ≤6 条;-2 张/窗)。img 进共享合成层零专属面。
667	验证:tsc 清+5 测试文件 30 用例绿+运行时 maxChunks=192/has52x48=0/盾 img
668	loaded(debug-report.test 的 384 断言同步改 192)。
669	
670	**第三场(12:54)**:起跑 21s 首败→12:55:40 五连败 GPU 进程死→恢复期再 4 败,
671	扛 83s 无整页死(熔断梯 192→96→64+看门狗+缓存自愈全生效)。失败尺寸含
672	2464×256/1536×416 等非自有宽条(cc tile/另一窗)= 全机水位问题。★揪出 herd
673	共犯:afterWorldLoad **直回满档**——第二窗加载/崩溃重进(预算最紧时刻)反而
674	重堆 12 张页。修=爬档恢复 `max(64, min(BASE, cur*2))`(64→128→192 逐世界爬,
675	既有恢复点又不瞬时吃满;原"永远 64"bug 依旧被解)。
676	
677	**第四场(13:00,"第二 tab 永不恢复")**:GPU 进程【没死】(0 次 Restarting),
678	但主画布后备 **1088×864 连败 7 次**(+另一窗 1512×862)——看门狗每 20s 重建
679	画布元素、后备永远分不出 = 僵尸循环。auto 熔断降级(60s 内 2 次熔断)对
680	"进程活但后备分不出"不触发(只到第 1 次熔断)。修 = **看门狗僵尸三振**:
681	重建后 30s 内又死 ≥3 次 → auto 模式切 CPU 软渲染(主画布 willReadFrequently
682	→ SHM 后备零 IOSurface,分配必成,页面至少活着)。附带:CloudGL/GLSpriteLayer
683	补 **objectsStale 旗**——webglcontextrestored 后 isContextLost()=false 但旧
684	对象已蒸发,dispose 的 isContextLost 守卫挡不住(17 条 INVALID_OPERATION 的
685	真身),lost/restored 双事件置旗、dispose 见旗跳过 delete。dist 已重建
686	(index-xDbmOBYL,4173 旧 preview 直接服务新包,EADDRINUSE 属预期)。
687	
688	**第五场(13:09,"会恢复了但光标没了")**:防护栈全生效——**0 次 GPU 进程死**
689	(仅 5 次小图失败:40×56×2 角色帧/40×40/28×24/16×16=恢复期重烘焙的写一次
690	缓存,Chrome 对这些 canvas 软回退)+10 mailbox。光标不恢复根因 = **vui
691	ui-canvas 层零恢复链**:画布+batch 一次性创建,contextlost 后全部 vui 绘制
692	静默 no-op,游戏内该层只画光标(系统光标被 #sw-cursor-style 全树 cursor:none
693	藏掉)→ 症状恰好只剩光标。修 = `VUI.healCanvas()`(frame 头每帧查
694	batch.ctx.isContextLost,死即原位换画布重建 batch;★监听闭包必须取
695	VUI.canvas 当前引用——换画布后旧闭包 rect 全 0 鼠标坐标恒 0)。E2E:钉死
696	ctx→换新✓。dist=index-BjMpQP_t。**瓶颈现状**:不再有进程级死亡,天花板
697	表现为边际小 canvas 失败→软回退;下一刀=#A CloudGL 并入 GLSpriteLayer。
698	
699	**第六场(13:47,#A 后首战)**:★**GPU 进程零死亡**(六场首次),5 分钟仅 7 次小图
700	失败(16×16×2=两窗油漆 tintCanvas/32×22×2=UI 图标烘焙/18×17/640×128)+
701	一次 1512×862(另一窗主画布重建,旋即成功)——页面"擦伤自愈"而非崩死。
702	瓶颈=从不显示的纯 scratch/toDataURL 烘焙画布仍在向内核要 IOSurface。
703	**根治:纯 CPU 用途画布一律 willReadFrequently(→SHM 后备,零 IOSurface)**,
704	九处落地:ChunkCache.tintCanvas/TintAtlas.scratch/GLSpriteLayer.scratch/
705	PaperDoll.hairScratch/UI(防御盾+图标 32²+invBg×2+tooltipBg×2;dust 双 scratch
706	本就有)。
707	**#A CloudGL 并入 GLSpriteLayer 已落地**:CloudGL.ts 退役,SkyRenderer.cloudGlLayer
708	由 Renderer 每帧注入共享 glfx(bggl/cloudgl 任一门开);GLSpriteLayer QuadOpts
709	新增 flipX(u 镜像);quad 几何中心制→左上制。验证:weatherCounter 到期重掷后
710	13 张 cloud: 纹理进共享层渲染正常。**云量 0 勘误**:非 bug——游走/重掷与原版
711	逐条一致,存档停在干档低点,+110s 到期重掷自然回满 200(实测);"天气引起崩溃"
712	定性=脉冲贡献(重掷瞬间 ~13 张纹理上传),非主因。
713	dist:index-pFHWLwCR。
714	
715	**第七场(13:58)+ 两问(2026-08-19 午后)**:零进程死亡保持,17 次失败全是
716	不可压缩面(Chrome 合成器帧@DPR2 3024×1724/光栅 tile/光标层 16×16 + 我方
717	chunk 页 1024²×2)——机器全机水位贴顶,我方已到底。★用户问"菜单资源带进
718	世界?"——查证:enterGame 是 newWorld/loadJson 公共漏斗,stopMenu()(menuBg
719	destroy+titleMenu+VUI.clear)稳定执行;菜单期仅 menuBg+vui 两张全屏,vui 画布
720	复用为游戏内光标层;菜单贴图=CPU 位图零 IOSurface。**无泄漏**(补 menuBg
721	destroy 后 width=0 即还后备)。★自愈后数字键/Enter 失效根因:onCanvasRecreated
722	的 `input.destroy(); new Input()` 把 Game 启动时注册一次的 keydownHandlers
723	(Digit0-9 切栏/聊天)与 onKeyEvent 清空——新实例两张表为空,鼠标/移动(window
724	级+轮询)活着而数字键死。修=重建时迁移两张表。E2E:Digit3→recreate→Digit5
725	仍切栏 PASS。dist:index-lHeqdQHe。
726	
727	**渲染侧全量审计+压缩 #1#2(2026-08-19 傍晚,用户令"全面审计...哪些可不用 GPU 且不慢")**:
728	运行时盘点(1280×800 窗):DOM 画布实为 2 张(主+vui;"第三张全屏"系我 debug-line
729	覆盖层 offsetParent 假象)+chunk 26+lightCanvas **132×84**(1/10 分辨率,早最优,
730	"全屏光照"系我错误假设)+hardAlpha images 18 张 canvas+glfx 1+6+TintAtlas ≤4;
731	vimages/uiimages 350 张 27MP=ImageBitmap 形态**零持久面**。两形态结论:①ImageBitmap
732	= CPU 常驻+绘制走硬件+GPU 拷贝可驱逐(零持久面,可规模化);②SHM 只适合从不进
733	合成的 scratch(每帧合成源 SHM=每帧 5MB 上传,不可取)。
734	**#1 hardAlpha→ImageBitmap 已落地**:images.set 后 createImageBitmap 异步升格
735	(竞态守卫同引用才替换);消费面 AutoTiler/WallTiler/rect 全 drawImage 源,无缝。
736	实测 18/18 bitmap、canvas 归零。
737	**#2 vui 光标独占模式已落地**:setState(null)(游戏内)→ ui-canvas 从全屏缩成
738	80×80 跟鼠标(transform 移动);菜单态恢复全屏。★两坑:①mousemove 监听原用
739	vui 画布自身 rect 当原点——画布漂在鼠标下时坐标系跟着跑(越移越漂),必须
740	视口原点直取 e.clientX/scale;②healCanvas 重建后 curMode 复位重挂模式样式、
741	resize() 在光标模式不得吹回全屏。E2E:80×80+transform 跟随(632,392)+光标像素在。
742	审计/验证探针:scripts/_render-audit.mjs(分类型计 canvas/bitmap)。
743	dist:index-BpBpbwgM。剩余:chunk 96 档(#3,用户未拍板)、PaperDoll/AutoTiler
744	家族同法 ImageBitmap 化(#4)。
745	
746	**第八场(14:44,#1#2 后首战)**:0 进程死亡(第三连),**尖峰后完全干净**——
747	14:45 加载尖峰 70 秒 8 次失败(16×16×5=Chrome 光标层/40×56×2=PaperDoll 重烘/
748	1024²×1)→14:46:15 起零失败跑 4 分钟。形态已从"持续摩擦"变"尖峰对抗后稳定"。
749	
750	**#4 PaperDoll/AutoTiler 家族 ImageBitmap 化(2026-08-19 傍晚,用户拍板)**:
751	新 `src/render/bitmapize.ts`(bitmapize:map.set 后 createImageBitmap 异步升格,
752	同引用竞态守卫;freeBaked:淘汰按类型释放——canvas width=0/bitmap close())。
753	接线:PaperDoll cache(64 LRU)/tintCache(256)/stealthTintCache(inner 48)+
754	AutoTiler rotCache/filledCache;类型 `Baked = HTMLCanvasElement | ImageBitmap`
755	贯通(compositePaperDoll/tint/tintRGBA/eyelidFrame/dollFrame(Rows) 签名放宽,
756	消费面全 drawImage/.width 无感)。★rotCache/filledCache 的 return img 取
757	`map.get(key) ?? c`(升格后返回 bitmap 而非闭包 canvas)。E2E:首取 canvas→
758	900ms 后 ImageBitmap ✓ 玩家 640px 在画 ✓(d1=null 陷阱=贴图未就绪早退,
759	须等就绪再验)。40×56 失败类应消失。dist:index-IzPX9x1W。
760	
761	**已登记(docs/webgl2-migration-plan.md 尾"待办登记")**:#B 全屏地图纹理
762	封顶(3040×448 级,低优先);"双开档"BASE 96 可选(收益已入个位数)。
763	
764	相关:[[imagebitmap-root-cure]](第九台 contextlost 抖动环+熔断器) [[webgl2-phase1-port]]
765	
766	=====FILE: proj-draw-offset-table.md=====
767	---
768	name: proj-draw-offset-table
769	description: 投射物绘制偏移表 num143/num144 移植——炸弹引线出盒对齐的权威公式与已备案动态项
770	metadata: 
771	  node_type: memory
772	  type: project
773	  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
774	  modified: 2026-08-18T07:33:23.041Z
775	---
776	
777	投射物贴图与碰撞盒对齐走原版 **num143/num144 偏移表**（Main.cs:29375-29826）+ 通用绘制公式
778	（Main.cs:34040）:anchor=(盒左+num145+num144, 盒上+盒高/2),origin=(num145, 盒高/2+num143),
779	num145=(贴图宽+盒宽)/2 → 展开后**贴图左上角=(盒左+num144, 盒上−num143)**。典型:炸弹 28
780	上移 8(22×30 贴图,引线 y=0-7 全在盒外,弹体恰填 22×22 盒,:29560);雷管 29 上移 11。
781	
782	本仓:`WeaponProj.ts` `PROJ_DRAW_OFFSET` 118 条静态项(2026-08-18 脚本机械对拍 118/118 全对)。
783	
784	**Why:** 曾按"贴图中心=盒中心"绘制,引线半截进盒(用户校准 {x:1,y:8,w:22,h:22} 指出)。
785	
786	**How to apply:** 新投射物视觉错位先查该表再手调。消费端(2026-08-19 全接):①WeaponProj.
787	drawProj(武器弹)②**MinionProj.draw(aiStyle 26 随从族——该表主体即此族,曾从未消费,
788	一律盒心居中;现走 anchor=(盒左+num145+num144, 盒上+h/2) 公式,共享 projDrawOffsetFor
789	导出;AI_026 spriteDirection 恒−1→dirX=−1;未登记型号维持居中=备案差异,原版=盒左上对齐)**
790	③397 燃烧瓶经 GrenadeProj。浮标已接(2026-08-19:Bobber 走公式+bobber num143=8+钓线段链 DrawProj_FishingLine 1:1,含竿尖表/线色表/张力摆垂 lai0)。MINION_NO_FLIP 曾漏
791	112/959/1003/1004/1095/1096(同 AI_026 零赋值却被 facing<0 误翻)。验证法:拦截 5 参
792	drawImage 断言 dest 原点=(-num145, -(h/2+num143));★9 参形态是帧切片制作调用勿混淆;
793	浮点须容差。关联 [[melee-hitbox-sprite-base]][[summoner-full-parity-batch]]。
794	
795	=====FILE: bird-findframe-families.md=====
796	---
797	name: bird-findframe-families
798	description: 鸟/小动物 FindFrame 专属 case 全家族——地面鸟不踱步是站定帧前提;鸮族 spriteDirection 取反的双翻陷阱
799	metadata: 
800	  node_type: memory
801	  type: project
802	  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
803	  modified: 2026-08-18T07:33:55.658Z
804	---
805	
806	小动物帧调度多数不在 FindFrame 通用组(NPC.cs:69230 大 case),有专属 case,落
807	`vanillaFrameIdx` 通用 6t 档即错(2026-08-18 批量修正,均在 Renderer.ts):
808	鸟 74/297/298/442(:74326 站定=帧4/飞行0-3 每4t)、丛林鸟 671-675(:74352 站0/飞1+ 每4t)、
809	鸮 611/689(:74379 待机8帧转头/飞8+每5t)、萤火虫 355/358/654(:73369 4t亮3t闪+非发光
810	lai1≤0 暗带+2)、677/蜻蜓 595-601(3t 循环)、蚯蚓 357/448/484/606(:73455 静1/爬0↔1 12t/
811	腾空1)、蛆 485-487、瓢虫 604/605/椿象 669(:67616 地0-3/空4-7 每2t)、水鸟 363/365/603/609
812	(:74470 划水1↔2 8t/站1/飞11+每4t)、珍稀宝箱怪 473-476(:71831 伪装=帧0,曾14帧狂闪)。
813	
814	**Why:** ①地面鸟 AI 原版**不踱步**(AI_024 :25453 只重力,vx 恒 0——降落 :25488 显式归零),
815	曾自创 ±0.7 踱步 → 站定门 vx==0&&vy==0 永假 = 地面播飞行动画;②鸮族
816	`spriteDirection=-direction`(:74381),flip 极性=Main.cs:22985(spriteDirection==1 才翻)
817	→ 仅 direction==-1 翻——**必须从通用镜像行排除,否则两条叠加成恒翻转**(屁股朝前,终审抓出)。
818	
819	**How to apply:** 新小动物动画错位先 grep 原版 FindFrame 找专属 case;加镜像特判必查与
820	通用 `facing>0` 行的叠加。鸮族 AI:出生即飞(localAI[0] 门)、夜栖城镇 NPC 屋檐、689 夜间
821	玩家<80px→Transform(317 魔眼)、湿态 vy×0.95−0.5 钳−4(:25596 三态通用)、飞行帽 3/丛林鸟 4。
822	鸟粪弹已补(2026-08-19:PoopProj 全链,★仅负幸运玩家或 IsThisCenx 四名(cenx/cblox/jade lightning/cenigit,Player.cs:18032)会被掷——RollOnlyBadLuckExtreme 幸运≥0 恒返 −1, Luck.cs:53;尘 329 已引擎化含实心格×0.8 收缩)。蚯蚓自旋/坡面已接。鸮待机/宝箱怪状态机已 1:1(WeakMap 态)。关联 [[critter-ai-port]][[vanilla-npc-port]]。
823	
824	=====FILE: boss-audit-wave1-fixes.md=====
825	---
826	name: boss-audit-wave1-fixes
827	description: 全Boss同款四维审计波1(石巨人+机械三王+光女猪鲨史后+肉前五族+蜂后肉山世花)修复批:30+修;波2(月总/教徒四塔/鹿角怪飞碟/月亮事件)在途
828	metadata: 
829	  node_type: memory
830	  type: project
831	  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
832	  modified: 2026-08-19T06:38:12.811Z
833	---
834	
835	2026-08-19 全 Boss 同款审计(用户令"逐一审计"):石巨人双代理模式推广到全 25 Boss 族,
836	两波 8 代理。波 1 五报告全部落地修复:
837	
838	**★跨族系统性根因(波 1 抓出)**:
839	- BGM 链键 flag/num3 错位(石巨人批已修,17/24 族错曲)
840	- **弹幕自身出生音**(Projectile.cs 首 tick PlaySound)是 AI 侧审计盲区——须双代理交叉
841	  (音效代理查 NPC 侧+行为代理查弹侧):258→Item_20/259→Item_33(石巨人)、
842	  923→Item_159/926→Item_155(光女史后)全缺
843	- **PlaySound(4)=NPCKilled 死音库**:鲨鱼起扑/猪鲨泡泡/385 落地(全 NPC_Killed_19)、
844	  WoF 尖啸(NPC_Killed_10,曾 Zombie_10 错库+引错 Load 行)
845	- **json 1405 旧值**:猪鲨 50000→60000;蜂后死音 NPCDeath1→66
846	- **FindFrame type 表**(状态帧):蜂后 222(lai0 冲刺带 0-3/4-11)、世花 262(血量分带)、
847	  肉墙 113/114(12t+放虫冻结)、双子 125/126(并入 EoC 眨眼组)
848	- 静默退场须 bossFled(光女两处淡出自毁曾记为击杀→误 downed+LanternNight+零掉落)
849	
850	**机械三王**:变身双声两眼同播(:27467 纠旧批误读)/二阶段 HitSound→NPC_Hit_4/
851	锯臂 ai2+=1(0→1/**3→4 追玩家态** 曾恒→1 死码)/钳臂同款(3→**4 横扫**)/炮激光
852	旋冲射速×3/×4(:28661/:28897)/毁灭者头追近门(:50306)/proj96 scale 1.3/臂名正位
853	(128 Cannon/129 Saw/130 Vice/131 Laser——NPCID.cs:11321 权威)
854	
855	**肉前五族**:克脑二阶段 Roar_0(曾 Zombie_2 错音)/红帽帧 1(曾恒 0)/弹 270 髅骨
856	(pierce3+30-110t 转向窗口+Item_8 出生音,Arrow.skullBone opts)/史王死亡爆 4-7 小史莱姆/
857	史王公告收口(50 移出静默集)/骷髅王专家臂档
858	
859	**蜂后肉山世花**:蜂后毒刺 719 grav 0.1@15t(曾恒直飞)/刺球 277 物理重做(0.2@15t
860	+滚动摩擦 0.97+|vx|≤0.01 自灭+Y 门>1+专家 X 轴单混 homing.axis)/专家种子 noTileCollide
861	+life 钳 180/狂卷之舌 lavaLine→h-200(UnderworldLayer 坑)
862	
863	**遗留(登记)**:骷髅王红帽/FTW 头档全缺(damage×1.3/NPC32 召唤/Taunt)、史王动态
864	scale+盒重算、光女 case11 expert 表+白天暴怒环色、猪鲨 FindFrame 状态机+特效层包、
865	史后四附属层(Extra_185/186/177 素材在)+922/926 物理收敛、鹿角怪/飞碟/火把神/月亮事件
866	Boss 波 2 在途。测试:boss-music-parity 活链断言+两处旧口径更新(FTW 算式/起扑音)。
867	
868	相关:[[golem-3symptom-fix]](石巨人 13 修+BGM 链根因)
869	
870	=====FILE: golem-3symptom-fix.md=====
871	---
872	name: golem-3symptom-fix
873	description: 石巨人三症状:负血不死=hurt放行与AI首行契约断裂(放行在dead=true前!)/boss bar头像表漏245/帧=FindFrame状态帧非循环(customFrameIdx直读)
874	metadata: 
875	  node_type: memory
876	  type: project
877	  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
878	  modified: 2026-08-19T05:21:50.578Z
879	---
880	
881	2026-08-19 用户报三症状(debug report 锡桌子):①动画贴图乱闪 ②负血条不死
882	③boss bar 无头像。
883	
884	**②负血不死(最重,契约断裂)**:Enemy.hurt 的石巨人放行段
885	`if (245||246||247||248) return false` 在 `this.dead = true` **之前**——"转换在
886	AI 首行接管"的注释假设 hurt 已置 dead,实际啥也没做:本体/拳血尽后 AI 每帧重入
887	(hp≤0)却无人置 dead = 永不死、boss bar 负值。★铁律:**hurt 放行型特判的放行
888	必须挂在 dead=true 之前且只有"确有 AI 首行接管"的 id 才放行**——石巨人仅 246
889	(头转自由态)真有;245 本体/247/248 拳走标准死。修:放行列表收窄到 246;
890	245 在 hurt 内灭部件(246-249,并行会话 boss#19"部件随本体消亡"定案的
891	执行点从 golemAI 首行挪到 hurt——dead 实体 AI 分发已跳过,首行版永不达)。
892	golemAI 首行血尽段注释化;dying 演出段标注不可达保留(无置位点)。
893	并行会话同日写 boss#19 审计时引入此断裂——**跨会话契约改动必须核对方调用侧**。
894	
895	**③boss bar 头像**:BOSS_HEAD_INDEX 只给了 246/249→5,漏本体 245(boss bar
896	反查的是本体实体)→补 `245: 5`(Golem 头像=Head_Boss_5,与头共用)。
897	
898	**①帧乱闪**:石巨人族全是 FindFrame(NPC.cs:73581-73651)**状态帧非循环**:
899	- 245 本体 7 帧只用 0-4:待机按 ai1 蹲伏倒计档(-20..0 五档);跳跃 ai0==1 →
900	  原版 `frame.Y = 1`(1 像素笔误值≈帧0,照抄取0)
901	- 246 挂载头:基础=l0(张嘴)1:0;眼部阶段(ai0==1,血<半)按激光侧 l1:
902	  -1→+4 帧 / +1→+2 帧 / 0(正上/下)→基础帧
903	- 249 自由头:帧=l0(frameCounter16 循环无消费)
904	- 247/248 拳 1 帧无动画
905	修:AI 侧写 `e.customFrameIdx`(先例=水书怪694),Renderer vanillaFrameIdx
906	直读零改。曾走通用 animT 循环=7 帧/6 帧乱闪。
907	
908	测试 tests/golem-fix.test.ts 6 条(拳标准死/本体死+部件**下一拍自灭**/246 放行
909	(本体活门)+零死音/存量负血自愈/帧档/头像索引)。
910	★二轮 review 修正(用户质询"登记不修"后推翻自己):①"246 不能 die()"不成立——
911	原版头血尽转自由只发生在本体活(一阶段本体无敌必先打头);本体死后原版=StrikeNPCNoInteraction 标准死。修=**hurt 246 放行加本体活门**(本体死→落回标准死)。②"视觉噪音小"是搪塞——部件终战消亡全面改原版时序:**hurt 只杀本体,部件由各 AI 锚主检测后下一 tick die() 自杀**(碎块/音效管线,原版同构);
912	头 AI 本体缺失分支"转自由态继续战"(并行会话写)按原版改为 die(),与其
913	boss#19 定案"部件随本体消亡"本就矛盾。
914	★顺带发现:原版 246 SetDefaults **DeathSound = null(显式无声)**——json 补
915	`"DeathSound": null`,DeathSound 类型放宽 string|null,fromVanilla 两处
916	(初始/tryTransform)显式 null → killedSound=[](无声),hurt 死亡段撤
917	'killed' 合成 fallback(空=显式无声语义;无其他可达场景)。
918	★教训:登记"不可修"前先挑战自己的理由——"X 不能用 Y"常常只是"Y 的无条件
919	用法不行",加门(如本体活条件)即破。
920	
921	**★终审清零批(2026-08-19 双子代理全维审计:音效/AI 行为/弹幕/渲染)——13 修**:
922	- 数据:四条 lifeMax 是 1405 旧值(json 9000/16000/7000/11000→1456 的
923	  15000/25000/10000/16000);恒 SCALE=0.5 错(:17942-17962 是 getGoodAdjustments
924	  **FTW 专属**段!普通世界 scale=1——曾误读为 SetDefaults 尾,普通世界头/拳
925	  锚点全缩半=嵌错位)→改运行时 sc(e)=vanillaScale??1
926	- **P0 BGM 裁决链键号体系错位**(Music.ts SLOT_MUSIC_CHAIN 键写成 flag 号而
927	  Game 存 num3 号)→17/24 族错曲:石巨人放 Boss3、EoW/骷髅王查无键落群系曲、
928	  月总放世花曲;BOSS_MUSIC/bossMusicFor 是死表(测试断言死表所以一直绿)。
929	  修=链键逐条换 num3(非线性三处:鹿角怪 flag2→16/EoW 25→23/骷髅王 26→24)+
930	  测试改断言活链 resolveEventMusic
931	- P0 一阶段本体无敌被单发弹穿透:iframes=2→**dontTakeDamage**(hurt 的
932	  iframes 门有 pierce!==1 豁免,原版 :19509 是挡全通道的 dontTakeDamage)
933	- P0 软锁:先破头(转自由)再杀本体→无敌自由头+双拳永不退场。修=头 AI 本体
934	  亡分支去掉 !x.free 豁免(:31521-31525 自由头同样查 golemBoss)+拳锚删 head
935	  回退(原版 golemBoss 单锚,找不到即自灭)
936	- P1:弹 258/259 出生音 Item_20/Item_33(弹幕自身首 tick 播,发射点等效);
937	  夹玩家门重叠→**包含**(:19666);自由头渲染换画 NPC_249(246 变身后曾一直
938	  画 246 贴图);拳链 drawImage ×scale(曾原尺寸环叠压)
939	- P2:玩家死→本体穿墙(曾漏 player.dead);258 OnFire 50%/300-420t(活表
940	  vanilla-projstatus.json 整条缺,死表 vanillaProjStatusPlayer.ts 固定 300t/
941	  100%);变身 spin 清零;删 246→249 转换吼(对账行号 :32587 系幻影龙 266 段
942	  误引,原版无声)
943	- P3:自由头穿墙开关(flag48 noLos 穿墙/有视线嵌块走碰撞);258 恒旋 +0.3/t
944	  备案不修(近圆火球视觉影响极小);245 镜像备案(原版永不翻,美术近对称)
945	- ★方法论:死表+活链并存时测试必须断言**活链**(死表正确≠运行正确);
946	  引用反编译行号要核宿主函数(§ :17943 曾被误读为 SetDefaults、:32587 误引
947	  两次事故);审计任务卡交叉两代理(音效只查 NPC 侧漏了弹幕自身音——行为
948	  代理补上 Item_33)
949	
950	相关:[[npc-frame-golden-gate]](静态帧数闸门管不到运行时帧选择——
951	此案=数据全对但选帧错,闸门盲区)
952	
953	=====FILE: dungeon-waterchest-float-knife.md=====
954	# BBBBB 批：两新链 #32 Dungeon 清零（水覆写箱 loot 支 + 入口 0.6f float 刀口）
955	
956	- **s22222（A176/T178 陈设族位漂）根因**：入口上方 0 号房在 worldSurface 之上 →
957	  dgBasicChests 水覆写箱（num2<ws+50 → itemType=**327/chestStyle=0**）。vanilla
958	  AddBuriedChest 前置 flag（WG.cs:36062 chestStyle==0）使 loot 走 **surface 支**
959	  （(flag23&&(flag||flag6))||flag11，:36280）；JS `surf=…&&false` 恒假走金箱支 →
960	  掷数差 → G 段流错位连坐 I/T/F/Pa/Ba（家具地板跑扫中心 ±1 平移画像）。修=flag0
961	  传参+支门接真。★327=Golden Key 非水靴（零前缀零掷）；★Prefix 重掷链不存在
962	  （TryGetPrefixStatMultipliersForItem switch 内零 return false——81-89 均有乘子；
963	  唯后置四门可 false 但对地牢箱族 item 常量恒真）。
964	- **m20260811（W4 入口墙洞）根因**：Legacy 入口 0.6 框清墙上缘 b0=(int)(319−10×
965	  0.6000000238418579)=312.99999976→312（double）vs 二进制 **313**——float 乘积
966	  fl(10×0.6f)=6.0（半 ulp round-half-even）可复现；与 YYYY 金字塔案同族"二进制-
967	  反编译刀口分歧"。修=Math.fround 四界。9293480 侧两模型同解 235（无判别力、零回退）。
968	- **方法**：手制链探针（▶Dungeon 前 dump031 八通道 0 差=pass 自差裁决）；
969	  __dgTowerTrace 空谱系=Legacy 入口判别；ENT 段级八点探针定界 0.6 框；
970	  12345 全量回归抓回滚错误修（勘误两则均为中途自纠）。
971	- **YYYY 湖体级联归因证伪**：#32 清零后 m 链 #49 L=11,707 原样残留——湖体=
972	  沉降/液体模拟独立自差（#48 输入全绿），非地牢级联；移交 liquid 域。
973	- **oracle 债**：caves-oracle.cs（禁区）须镜像 flag0/surface 支+0.6f float 界；
974	  且 oracle 中世界支（worldSize=1）dungeonL 起自崩（首次跑中世界即暴露）。
975	- 首差推进：s22222 #32→#49（0..48 绿）、m #32→#49、12345 #54 基线原样、
976	  9293480 #63。报告=content-parity-vs-vanilla-2026-08-16.md BBBBB 章。
977	
978	=====FILE: wwww-root59-liquidation.md=====
979	# WWWW 批：#59 百格级根清偿（193→0）+ 帧杀级联引擎 + #89 藤归零 + 9293480 首差 #59→#63
980	
981	接 YYYY 归因（装饰位漂 4.3M 脊柱）。docs/worldgen/content-parity-vs-vanilla-2026-08-16.md WWWW 章。
982	
983	## 根清偿四修（全部 CaveHousePass 域，golden 实证）
984	1. **HouseBuilder FillRooms 陷阱雕像 = 无条件调**（HouseBuilder.cs:483-491：
985	   PlaceTile(105) 失败也调 PlaceStatueTrap；Statues pass cs:17045 相反=成功门内
986	   才调——两处语义相反勿互搬）。曾关进成功分支 → 4 屋漏陷阱+45 格漏线 → ±25
987	   红线扫描翻转全链。golden wire 对拍定位（TTTT 060 wire 快照 45 格 js=0）。
988	2. **AgeRoom 钟乳石 = 全族**：沙漠 396/397→378 列/花岗岩 368/大理石 367 都放
989	   （曾"仅冰族"局部近似漏 135 格）；用 ShimmerPass 全量 placeUncheckedStalactite
990	   替换局部副本。
991	3. **梁写 SetTileKeepWall=Clear(~(Wiring|Actuator))**：清液体/坡/半砖+梁底格
992	   slope/half 复位（78 格梁带水 L/Y 差根因）。
993	4. **跨物件帧杀级联引擎 frameKillSweep**（54 格终清）：vanilla 带帧写（PlaceTile
994	   尾 SquareTileFrame 九宫/SetFrames(frameNeighbors)）触发 Check2xX/Check3x2/
995	   CheckPile/Check2x2/CheckOrb/CheckStalactite 整盒击杀；**触发面=带帧写阶段**，
996	   蚀变裸 SetTile 不触发（(2634,479) 三格残破仙人掌存活实证）；杀=KillTile 生成
997	   期（noItem 零掷+type=0+清 half/slope）。**杀全族零掷的铁证：#60-62 全绿（流
998	   对齐）**。修后小屋序列 42/42 与 van_houses.json 对齐。
999	- 金标反事实方法论：SW_WWW_59G 注入 fr/wire/chest 全不动 → 输入债排除，定罪
1000	  写侧（TTTT 织入产物是 pass 头快照三通道，可复用）。
1001	
1002	## 放大器裁决
1003	- #71 罐 golden 基座重放**零自因**（勿修）；#89 藤 6 格自差两修归零（putVine 的
1004	  ClearSlope=清 slope+half 双轴；蜂巢凹龛 KillTile→九宫 CheckVines 级联——失锚
1005	  整列下杀 cs:85599-85698）。
1006	
1007	## 小项与移交
1008	- 12345 #54 Hf=1 单差 (3845,1045)：golden53 基座重放精确复现；修两处幽灵半砖
1009	  保真（loop1/loop2 active()&&halfBrick 双门）但单差仍在——vanilla 侧掷流织入
1010	  才能定位（YYYY 金字塔同类阻塞）。湖体±255=维持 m 链 #32 地牢债级联定谳，
1011	  移交 XXXX。
1012	
1013	## 战果与陷阱
1014	- 9293480 全管线首差 #59→#63（2 格=XXXX placeTightWebs 域）；12345 #59 128→12；
1015	  m2222 矩阵 typ-11.6%/wal-44.7%（装饰漂塌缩实证）；**s12345/l9293480 矩阵恶化
1016	  ≠本批**——panorama 定位在 #100-105 段（XXXX MicroBiomes/DungeonPass 在途编辑
1017	  窗口），本批域 ≤#99 全改善。矩阵横比必须记录并行会话 mtime 窗口，否则误归因。
1018	- mile8 尾段红集：#63=2+漂移带（GemPasses/Piles/FinalCleanup 等 mtime 实证）。
1019	- worldgen 域真回归零（3817 例 35 败全 KKKK 在案带；隔离复核 npc-liquid/paint/
1020	  hive 绿=他批探针 import 副作用）。液体 60/60。
1021	
1022	

````


---

## 🤖 Assistant · 2026-08-19T07:07:38.985Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent material. Now let me read the next batch of memory files.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:07:39.020Z · glm-x-preview-260804

```
很棒的资料。现在开始处理下一批记忆文件。
```


---

## 🤖 Assistant · 2026-08-19T07:07:40.630Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ && for f in aaaaa-track-framechain-port.md bed-sleep-visual-fix.md book-mimic-cultist-dragon-batch.md boss-summon-drops-events-batch.md bunny-walk-frame-fix.md ccccc-place2x2-anchor-check2x2.md chunk-seam-noninteger-zoom.md cursor-icon-fullbright.md dome-slot32-pot-waterbolt-inact.md fog-flicker-f4-latetex-fix.md half-slab-liquid-band-parity.md jungle-parity-and-id-collision.md leftover-closeout-4batch.md npc-ambient-sound-audit.md npc-damage-gate-port.md; do echo \"=====FILE: $f=====\"; cat \"$f\"; echo; done",
 "description": "Read second batch of memory files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:40.686Z

**📎 ToolResult**

```
<persisted-output>
Output too large (195.8KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bwbyrnzq0.txt

Preview (first 2KB):
=====FILE: aaaaa-track-framechain-port.md=====
# AAAAA：TrackGenerator 帧链 1:1（#101 残余尾 1% 处置）

接 XXXX 移交（van TrackGenerator.cs:136/151/158 TileFrame(frameNeighbors:true) 未镜像）。
对拍发现实际是**三链**：①循环一遍 KillTile=尘掷(RRRR 表)+击杀+尾部 SquareTileFrame
（cs:63967）——XXXX 未定罪但 'a 3' 苔藓掷大半在此；②cs:136 压板支 PlaceTile=
ClearEverything(墙/液体全清!)+PlaceTrack(20,-1)+SquareTileFrame 九宫；③cs:150-160
逐列 l<8/末列 m<playerHeight 五连 TileFrame(resetFrame:true)。JS 修（TrackPass.ts）：
killTileLane(尘掷全表复刻——killTileGen 私有,FinalCleanup 禁区只 import)+squareTileFrame314
(九宫=genSquareTileFrame+314 格补 frameTrack,两子系统零交叉可换序)+wuTileFrame 五连
字面镜像(tf314:314→frameTrack[零掷],余→genTileFrame)；退役"铺完统一 frameTrack"三循环
(等价论断撤销——van 链同时帧非轨道邻格且多轮 FrameTrack 时序不可交换)。HandleRopeEndFraming
生成期可证 no-op(GetRopeEnds 只停 inactive/绳格)；ResetToType 保墙清液体、线还原四色精确赋值。

验证：掷流 firstDiff 165353→**165546**(+193 掷逐条吻合)；帧位金标 102 .fr 路径吻合段
**48/50 逐位同**(2=路径分歧边界)。★残差定源**上游**：van 轨 y=735 直穿矿爆区而 JS 绕高
——金标出口实证 JS 411 起爆器 2×2 比 van 低一格(placeMiningExplosives findDown 首实心
低一行,掷不可见[411 杀零掷])→findPath **零掷**重路由→巷杀错位首曝掷流。矿爆段非轨道段
=域外移交。另一引擎缺口:case 138 巨石 Check2x2 缺(3 格 18,18vs0,0)移交引擎批。
工具资产:_wwwrep span 增 d/n 通道+rng.vanilla 'n'(SW_WWW_SPAN_DN=0 关);
★frtyp/.fr 是稀疏 (idx,val) 对/三元组数组——按格索引读=垃圾(本批翻车两次)。
mile8 9293480 0..62 绿;world-final-hash 常量待再生窗并入重基队列。

=====FILE: bed-sleep-visual-fix.md=====
---
name: bed-sleep-visual-fix
description: 躺床效果三根因(1tick误杀/镜像内旋转角/床偏移双重镜像)与1:1修法;原版无冻结=锚点脚底踩床下地板;引导性视觉提问会假确认
metadata: 
  node_type: memory
  type: project
  originSessionId: 9adce254-f6c0-44ed-947b-3a226dd16828
  modified: 2026-08-17T13:24:05.342Z
---

躺床（上床睡觉）状态效果 2026-08-17 修复，对照 `PlayerSleepingHelper.cs` + `PlayerDrawSet.BoringSetup:336-356` + `TransformDrawData:4199-4230`：

**三根因**（用户报告"躺床上的效果并不对"）：
1. **唤醒误杀**：wake 检查读 `feet+2`（=床下一行地板≠床格）→ 入睡 1 tick 即被杀，效果一闪而过。原版语义 = `Bottom+(0,−2)` 处必须是床格（GetSleepingTargetInfo 可解）+ `frameX/72` 朝向档与 facing 一致 + 任一移动/跳跃输入/骑乘 → StopSleeping（UpdateState :93-117）。
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-19T07:07:44.866Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bwbyrnzq0.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:45.020Z

**📎 ToolResult**

```
1	=====FILE: aaaaa-track-framechain-port.md=====
2	# AAAAA：TrackGenerator 帧链 1:1（#101 残余尾 1% 处置）
3	
4	接 XXXX 移交（van TrackGenerator.cs:136/151/158 TileFrame(frameNeighbors:true) 未镜像）。
5	对拍发现实际是**三链**：①循环一遍 KillTile=尘掷(RRRR 表)+击杀+尾部 SquareTileFrame
6	（cs:63967）——XXXX 未定罪但 'a 3' 苔藓掷大半在此；②cs:136 压板支 PlaceTile=
7	ClearEverything(墙/液体全清!)+PlaceTrack(20,-1)+SquareTileFrame 九宫；③cs:150-160
8	逐列 l<8/末列 m<playerHeight 五连 TileFrame(resetFrame:true)。JS 修（TrackPass.ts）：
9	killTileLane(尘掷全表复刻——killTileGen 私有,FinalCleanup 禁区只 import)+squareTileFrame314
10	(九宫=genSquareTileFrame+314 格补 frameTrack,两子系统零交叉可换序)+wuTileFrame 五连
11	字面镜像(tf314:314→frameTrack[零掷],余→genTileFrame)；退役"铺完统一 frameTrack"三循环
12	(等价论断撤销——van 链同时帧非轨道邻格且多轮 FrameTrack 时序不可交换)。HandleRopeEndFraming
13	生成期可证 no-op(GetRopeEnds 只停 inactive/绳格)；ResetToType 保墙清液体、线还原四色精确赋值。
14	
15	验证：掷流 firstDiff 165353→**165546**(+193 掷逐条吻合)；帧位金标 102 .fr 路径吻合段
16	**48/50 逐位同**(2=路径分歧边界)。★残差定源**上游**：van 轨 y=735 直穿矿爆区而 JS 绕高
17	——金标出口实证 JS 411 起爆器 2×2 比 van 低一格(placeMiningExplosives findDown 首实心
18	低一行,掷不可见[411 杀零掷])→findPath **零掷**重路由→巷杀错位首曝掷流。矿爆段非轨道段
19	=域外移交。另一引擎缺口:case 138 巨石 Check2x2 缺(3 格 18,18vs0,0)移交引擎批。
20	工具资产:_wwwrep span 增 d/n 通道+rng.vanilla 'n'(SW_WWW_SPAN_DN=0 关);
21	★frtyp/.fr 是稀疏 (idx,val) 对/三元组数组——按格索引读=垃圾(本批翻车两次)。
22	mile8 9293480 0..62 绿;world-final-hash 常量待再生窗并入重基队列。
23	
24	=====FILE: bed-sleep-visual-fix.md=====
25	---
26	name: bed-sleep-visual-fix
27	description: 躺床效果三根因(1tick误杀/镜像内旋转角/床偏移双重镜像)与1:1修法;原版无冻结=锚点脚底踩床下地板;引导性视觉提问会假确认
28	metadata: 
29	  node_type: memory
30	  type: project
31	  originSessionId: 9adce254-f6c0-44ed-947b-3a226dd16828
32	  modified: 2026-08-17T13:24:05.342Z
33	---
34	
35	躺床（上床睡觉）状态效果 2026-08-17 修复，对照 `PlayerSleepingHelper.cs` + `PlayerDrawSet.BoringSetup:336-356` + `TransformDrawData:4199-4230`：
36	
37	**三根因**（用户报告"躺床上的效果并不对"）：
38	1. **唤醒误杀**：wake 检查读 `feet+2`（=床下一行地板≠床格）→ 入睡 1 tick 即被杀，效果一闪而过。原版语义 = `Bottom+(0,−2)` 处必须是床格（GetSleepingTargetInfo 可解）+ `frameX/72` 朝向档与 facing 一致 + 任一移动/跳跃输入/骑乘 → StopSleeping（UpdateState :93-117）。
39	2. **旋转角**：原版 `fullRotation = π/2·(−direction)`、origin=Size/2。本仓镜像 `scale(facing,1)` 在旋转**之前**：`S·R(θ)=R(α)·S ⟹ θ = −α`，两朝向化简后**恒 −π/2**（曾写 `π/2·(−facing)` → 视觉恒 −π/2：变体B床恰好对、变体A床头落在脚尾）。
40	3. **床偏移双重镜像**：镜像空间内 translate 又乘 facing → 世界位移 = bo（丢了 Directions 乘子），朝左床水平偏移反向（差 2·bo.x）。修法 = 局部直接传 bo 原值（外层 scale 会把 x 再乘 facing，恰得 bo×Directions）。
41	
42	**Why:** 变换合成顺序（镜像/偏移/枢轴旋转）三个符号互相纠缠，单看一处"对"另一处就错——B 床(facing+1)碰巧三处全对掩盖了 A 床(facing−1)全错。
43	**How to apply:** 躺床变换已提取 `sleepingTransformOps`（Renderer.ts 导出纯函数）+ `tests/sleeping-bed-transform.test.ts` 逐点矩阵等价断言（头/脚/心/双肩 × 三组床型偏移 × 双朝向）；改这里必须过该测试。床贴图 Tiles_79：变体A(frameX<72)枕右→dir−1、B(≥72)枕左→dir+1。**原版无物理冻结**：锚点把脚底精确放到床下地板顶（床非 SolidTop），重力由地板接住——勿加"睡眠冻结"。SetOffsetbyBed 约 25 床型偏移表已在 Renderer.BED_VISUAL_OFFSET。
44	
45	**Review 二轮补修（2026-08-17 同日，交互分支 4 处旧偏差，Player.cs:32184-32228 权威）**：
46	1. ★**极性反**：原版 `!IsHoveringOverABottomSideOfABed → StartSleeping`——**枕端入睡、脚端设重生点**；我们曾脚端入睡/枕端设点。bottomSide 公式本身同款（fx%72<36 XOR 变体B），只是两分支接反。
47	2. 距离门错式：原版 IsWithinSnappngRangeToTile(:17214) = 悬停格中心(tx·16+8,ty·16+8) vs 玩家(Center.X, **Bottom.Y−16**) ≤ 96；曾用 (tx+2)·16 角点。
48	3. 重生点坐标帧盲：原版 = 变体A(bedLeft+2)/B(bedLeft+1)、行=**bedTop+2**（床下地面行，本仓 spawnY=落脚格约定一致）；曾 (tx+1, ty−1)。
49	4. StartSleeping 前置缺：清坐姿（否则坐姿平移+躺床旋转叠画）/收钩爪/试下坐骑（失败由唤醒门拦）/gravDir=1；同床再点=下床、异床点击=换床重睡（:170-175）。
50	未移植登记：CanSnapToPosition 目标格畅通检查（床位放置链已保证）、RemoveSpawn 再点移除（无原始出生点存档）、pulley 唤醒（单机无链挂）。
51	
52	**探针教训**：①视觉模型分析会被引导性提问带偏——两次"确认修复"实为幻觉，截图必须先做亮度/内容自检（纯黑=无光场景）；②headless 页面截图管线不可靠（rAF 不触发、合成器不出帧）——能用确定性单测（矩阵合成/录制式 ctx）就别折腾截图；③`page.evaluate` 内 boot 等待勿超 puppeteer protocolTimeout（默认 180s），launch 传 `protocolTimeout`。探针 `scripts/_sleepbedprobe.mjs`（行为断言部分有效：60/60 存活）。相关 [[behavior-parity-batch-2026-08-17]]。
53	
54	
55	**三轮全量补齐（2026-08-18，"完整移植不能漏"）——登记项全部落位**：
56	1. **CanSnapToPosition**（PC:32945-32981,Game.canSnapPlayerTo）：目标盒 SolidCollision + canHit 盒视线 + 四组 (w−2,0) 2px 窄条回退 + 横向 ±width 扫掠一步再试；失败=整个入睡静默不发生（隔墙/堵塞不能上床）。
57	2. **CheckSpawn 房间校验**（PC:53608-53666,Game.checkBedSpawn）：床必须处于合格房间（Housing.checkRoom=StartRoomCheck 1:1）；床上 3×3 净空→BedObstructed；Housing 新增 `lastRoomCheckFail` 穿透 floodRoom 五档失败原因（tooBig/tooSmall/hole/notValid/edge→Game.Bed* 五档文案,ServerMessage=(255,240,20)）；y 上界照抄原版 maxTilesX 笔误；UnsafeWalls 档并入 hole（门禁同,文案折叠,登记）。
58	3. **RemoveSpawn 再点移除**（:32215-32218 + Player.RemoveSpawn :53686）：World 新增 spawnX0/spawnY0 原始出生点快照（WorldGen/SaveFile(wld)/World.fromPacket/自有存档 header.spawn0 全链持久,旧档缺省回退 spawn）；再点同点回退+Game.SpawnPointRemoved 文案；设点成功文案换原版 Game.SpawnPointSet。
59	4. **物品使用唤醒**（SH:112-121）：itemAnimTicks>0（每帧由 swing.t 注入 Game.ts:3627——探针须造 swing 不能直写字段）且 damage>0&&!noMelee / fishingPole>0 / ForcesBreaksSleeping{1991,4821,3183}。★damage/noMelee 在 **itemfunc 表**（stats 表只有装备属性——曾查错表恒 false）。
60	5. **AnyActiveBossNPC**（NPC.cs:81040-81057 AnyDanger 终项）：场上任一活跃 boss→actUp 重置熟睡计时（不唤醒）。
61	6. **RemoveAllFishingBobbers**（:33120）：入睡前杀全部活鱼漂。
62	真 N/A：pulley 唤醒（本仓无绳索链挂机制——grep 仅注释）；mount 自定义尺寸子支（坐骑不改碰撞盒）；MP 双人叠床/睡姿同步（无 net 消息,网线协议勿动——曾误加读端险致流错位已回退为回退近似）。探针 `scripts/_sleepbedprobe.mjs` EXTRA 六断言全绿（双床入睡/snap 拒绝/spawn 拒绝/回退/boss 重置/挥砍唤醒）。
63	
64	**Review 四轮（2026-08-18 同日）三修正**：
65	1. ★**原版序**:CanSnapToPosition 在 toggle 之前（SH:165-175）——堵塞态连"下床点击"都不响应（只能移动键醒）;曾 toggle 先行。
66	2. 鱼漂按 ownerRef()===player 过滤（联机不误杀远端漂;vanilla owner==whoAmI）。
67	3. itemWake 使用窗并入 useTime>0（ForcesBreaksSleeping 三件非挥砍——单查 swing.t 会漏;swing.t 每帧覆写 itemAnimTicks Game.ts:3627）。
68	另:tile 379 泡泡块——原版静态表 solid=true 但 DoUpdateInWorld(:17675)每帧改 false（通行性既有偏差,登记不动 defs）;CheckSpawn 期间按 solid 算两版一致,床链无影响。
69	
70	**五轮"登记全清"（2026-08-18）：所有登记/N-A 项落位，无遗留**：
71	1. ★自查纠偏：床设点原版=StartRoomCheck**纯围合**（家具是 TownNPC RoomNeeds 独立步骤,PC:6000-6057 无家具检查）——曾用带家具 checkRoom 过严。Housing 新增 `checkRoomEnclosure`（floodRoom 选项化 requireFurniture/requireStand/extraSolid）。
72	2. **UnsafeWalls 档**：floodRoom 漏墙点细分——wall>0 且非房墙='unsafeWalls'（CheckRoom :6171-6176）→ Game.BedRoomHasUnsafeWalls；泛洪越界='edge'。★泥墙 wallHouse[1]=true 是原版事实（Main.cs:10295,可放置泥墙合法）——真不安全墙如地牢墙 7。
73	3. **tile 379 泡沫块**：defs 改 non-solid（原版静态表 true 但 DoUpdateInWorld :17675 每帧 false）；checkBedSpawn 3×3 与围合泛洪以 extraSolid={379} 补回检查期实心（翻转同构）。
74	4. **MP 睡眠全链**：msg13 flagBits[0]=sleeping（原版 bitsByte26[0];过服务器中继零改动）+ 变化即时发；代理 proxy.sleeping + 本地 timeSleeping 推进（原版各端跑 UpdateState 模型）；同床叠床 ≤2 人门 + 叠位序（slot 序,视觉 −4px/层 GetSleepingOffsetInfo 第二项）；服务器权威时钟按全员熟睡 ×5（roomHost 1s tick 累计 sleepMs≥2000,ghost 不计分子分母）。
75	5. **spawnX0 过网**：worldDataFrame 尾部追加两 i32（v8;客户端 remaining≥8 才读,旧服自动回退）。
76	6. **canSnap 横移精确化**：scratch Body 走 moveAndCollide 判位移完整（TileCollision(x)==x 同构;stepUp 关/dropThrough 开=fallThrough,ignorePlats 口径）。
77	7. **静持物随躺转**（段A 火把等手持层原版在 DrawDataCache 整组旋转）：世界空间施加 off+绕盒心 π/2·(−facing)。
78	8. **sleepingBedOffset 精确化**：先读 Bottom−2 床格 frameY/36（GetSleepingTargetInfo 同格），7×4 扫描退化为代理插值兜底。
79	真·空集（有据）:pulley 唤醒（引擎无绳索机制,grep 全库仅注释）;mount 自定义尺寸子支（坐骑不改碰撞盒,恒 20×42）。测试：bed-spawn-enclosure 4 项 + 全家桶 31/31;探针六断言全绿。
80	
81	**六轮 Review（2026-08-18）两修正 + 一顺手解封**：
82	1. ★**canSnap 浮点等值 bug**：`body.x === p.x+num·p.w` —— moveAndCollide 按 ≤8px 分步累加，任意起点处 dx/steps×steps 有 ~1e-14 尾（node 实证 from100: 120.00000000000001）→ 横移试探几乎恒 false。改 epsilon<0.01。★分步位移的"全位移"判定永远用 epsilon,禁用 ===。
83	2. **checkRoomEnclosure 直锚点**：原版 StartRoomCheck 单点入栈（:6031-6034），无 ±1/dy 探测（那是房门锚定用）——曾照抄 checkRoom 探测会在床贴门洞等边角判进隔壁房间;锚格实心→notValid(StartedInASolidTile 走 default 档)。
84	3. 顺手解封并行会话 boot 炸点:TrapsPass.ts 裸 `process.env.SW_EEEE_DBG`(浏览器无 process)——按同族 LT_TRACE/PYR_TRACE 的 typeof 守卫模式补齐。
85	验证:enclosure/housing/sleeping 23/23 + 探针六断言全绿。
86	
87	=====FILE: book-mimic-cultist-dragon-batch.md=====
88	---
89	name: book-mimic-cultist-dragon-batch
90	description: 书怪693/694全链+教徒幻影龙454召唤批：AI_010多状态机/贴书传送/书掉落vi_165链/仪式圈召唤/455-458数据补齐
91	metadata: 
92	  node_type: memory
93	  type: project
94	  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
95	  modified: 2026-08-18T10:14:07.781Z
96	---
97	
98	B 批（2026-08-18，task #150 收官）：审计四项全落地，tests/book-mimic.test.ts 14 绿。
99	
100	**694 水书宝箱怪（AI_010 :21552-21888 重写 cursedSkullAI）**：伪装态 3（静止/kb0/justHit→觉醒4）/觉醒 4（80t→活跃0）/冲刺链 flag18（d∈[100,300]，1/3 掷，蓄120t→态2 冲60t→ai2=-300 冷却，速度 14 直线）/咒球链 flag19（d≤500，态1 内 ai2==17 Center+(0,10) 出 NPC 33 水球）/逃逸 flag17（贴脸<100px ai1=-60，<-30 反向 8px/t）。★<100px 重置门是 flag10(694) 专属——曾全族误用。帧机（FindFrame :77905）在 AI 内算 customFrameIdx（Renderer.vanillaFrameIdx 顶部直读），npcFrameT=态切换清零的 frameCounter。34/289 通用档顺带 1:1：旋转=atan2(v)+<0 加 π+spriteDirection 翻转（Renderer stR===10 rotate e.visAngle）+289 justHit 清态。
101	
102	**693 贴书传送**：attemptToFindTeleportSpotNearBooks（fighterFamilies.ts，:18948-19024）——地牢墙窗随机列→交替方向走到墙面→垂直扫书（玩家 80px 扩展盒拒书）→落点=(书格外侧,书y+1)；±1 盒防原地。InWorld(Point) fluff=0 非 10。casterAI 传送先贴书后落通用。
103	
104	**spawner 书掷（:2655-2677）**：N(8)→最近书位生 694（ai3=3 伪装态）；else N(10)→693。AI_FindNearbyBook（spawnTile-16 起 32×32 closestBook+屏外门）；掷中无书空过落 num44 掷。findNearestBookForSpawn + tileClearOfPlayerScreens（屏外门抽成格坐标版）。
105	
106	**书链数据面**：tile50 掉落 KillTile_DropItems case 50（:65709）——frameX==90→vi_165 WaterBolt、其余 vi_149 Book（Game.ts framedSheet===50 分支）；放置帧随机 18*Next(5)（:45379）；桌面 1×1 族 {13,33,49,50,174,372,646} 须 TILE_TABLE_SHEETS（tiles.ts 导出 Main.tileTable 全表）。书=世界生成放（DungeonPass placeOnTableD(x,y-1,BOOKS)——DungeonGlobalPlatforms PlaceBooksChance）；waterbolt 帧 90 在 1456 有 X/Y 互换 typo（Main.tile[placeY,placeY]）几乎不触发——waterbolt 水术主获取=694 2.5% 掉落。法师商店已含 149。
107	
108	**教徒仪式圈召唤（Projectile 490 :31282-31292）**：age==300 场上无 454→幻影龙头+spawnWormChain(head,5,[455,456,457,458,459],sharedLife)；有→521（AI_086 phantomAI big 档本就齐）。454-459 渐显（:51379-51400）：头无条件 -42/t、段沿链 <85 门、渐隐期 dontTakeDamage+228 紫尘（Enemy 共享尾新块，与 EoW 位移门版并列）。spawnWormChain 扩 segIds+sharedLife 参数（realLifeHost=head 共享 10000 血池）。**455-458 原缺数据**（提取器漏 grouped SetDefaults）——vanilla-npcs.json 手补+454 对齐 1456（100伤/15防/10000HP；旧表 80/10/4000 是陈旧值）。
109	
110	坑：dash 态漂移——蓄力期逼近会使 d 跌破 100 使 flag18 失效转 flag19（原版同款，测试须把玩家放 ~256px）；书屏外门查【书位】非落点位。
111	
112	**C 批收尾（同日）**：vi_5395 屎堆注册（vanilla.json 有图标但 itemfunc 缺 createTile→自动注册成无 tile 摆设）+TryToPoop 1:1（**旧版"tier 递降"是自造**——原版整档移除+叠数=⌊剩余秒/3600⌋×tier 钳[3..999]+OnlyBadLuckExtreme(10)×1.2+noGrabDelay100）；{Bartender} 台词走 townName；DungeonPass 书帧 18*Next(5) 补写（掷值曾被丢=恒帧0；帧不入金标哈希安全）+waterbolt 帧按 1456 typo（tile[placeY,placeY] 对角检查）落地；687/睡渔夫两审计项实为已实现（注释过期，已勘误标记）。审计 A 级 35 条现余：坐骑槽UI/高尔夫球车3611/虚空袋/涂层/公告盒编辑/成就页UI/碎块魔杖/gravDir/事件门/RerollVariation/平台锤循环/builderAcc 开关/爬墙坐骑55。
113	
114	**★金鱼掉恐惧之魂事故（同日修）**：C 批曾把 vi_5395 手写 `item()` 插在自动注册循环【前】——ITEM_DEFS id=数组下标，插入点后全部物品 id 平移+1，按内部 id 反查 vid 的掉落链全体错位。修=删手写条目、tile 走 BLOCK_TILE_BACKFILL 追加 `[5395,666]`（回填改写现成 def 零位移）。tests/item-id-stability.test.ts 钉死：连续 vid 内部 id 严格递增 + 5395 tile 回填。**铁律：自动循环前禁止插 item()；补链一律回填表**。
115	
116	**createTile 双源回填+覆盖闸门（用户最佳实践质询后落地）**：手维护回填表只是折中非最佳——真实解=①createTile 双源（itemfunc 提取优先，缺时回退 vanilla.json .items.createTile【游戏数据最终态，覆盖提取器解不开的共享算式段 2189 件；双源交集 1042 中 1039 一致，3 件分歧均源码二次赋值、vanilla.json 更准：498=470/1989=470/3977=475】）②tests/item-id-stability.test.ts 覆盖闸门：vanilla.json 声明可放置且 tile 表已注册的物品 def.tile 必须非空（ALLOWLIST_NO_PLACE 登记有意豁免），静默"放置无效"从此必红。★坑：CRITTER_ANCHOR_ITEMS 循环的 `d.tile !== undefined` 跳过门在双源回填后会把锚桩 placeStyle 吞掉——改判 `d.tile !== CRITTER_ANCHOR_TILE`（只挡指向别 tile 的）。
117	
118	=====FILE: boss-summon-drops-events-batch.md=====
119	---
120	name: boss-summon-drops-events-batch
121	description: 全Boss三维总审计+修复:召唤链(成功才扣×5件/同型门BOSS_FAMILY增补/天界印记四重门/4988仅ZoneHallow/老人诅咒去hardMode门/眼球清spawnEyePending/DD2两压制门/世花灯泡支撑破坏) + 宝袋4+2真bug(sw按臂数/default独立branch/猪鲨2623/EoW矿量+devArmor 1/16全局表) + 光女白天ai3=2 + 裁缝娃娃召唤骷髅王 + 史莱姆雨计数门 + 旗标(陨石快照序/misc32·33/灯泡首杀门/史王停雨)
122	metadata: 
123	  node_type: memory
124	  type: project
125	  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
126	  modified: 2026-08-18T05:41:24.300Z
127	---
128	
129	全 Boss 召唤/掉落/触发事件总审计修复批（2026-08-18，用户令"检查各种boss的召唤方式、掉落物、触发事件是否全部齐全无误"）。三路审计（肉前召唤/肉后+事件/掉落旗标）发现 24 处偏离，三路修复代理全落地，src 全域 tsc 零错，Boss 回归 103/103。
130	
131	**A 路 Game.ts 14 项**：召唤物"成功才扣"统一（1133/4988/机械三王/5120——原版 SummonItemCheck false 不 ApplyItemTime；范本 useSuspiciousEye）；BOSS_FAMILY 增补 eye_of_cthulhu/king_slime/queen_bee/deerclops 同型门（原版配对表 :41514）；老人诅咒删 !hardMode 门；useSuspiciousEye 尾清 spawnEyePending；**天界印记 3601 四重门**（downedGolem&&hardMode&&!anyDanger&&!anyoneNearCultists 2500×1500 矩形+startImpendingDoom 副作用清教徒）+useTime 45；**史后水晶 4988 门仅 ZoneHallow**（原版无昼夜无 hardMode 门——获取在肉后但使用无门）；DD2 压制机械 roll+月事件门（删 invasionType 项——军队不阻月事件）；机械三王 useTime 45；世花首杀 misc[33]+三旗首齐 misc[32]（用 !wasDowned 翻转语义防旧档误补发）；**EoW/BoC 陨石快照序**（boss2Already 写键前求值——曾恒 true 致首杀必坠变恒真）；三王全灭灯泡加首杀门（防超发）；史王死停史莱姆雨+成就16；珠/心音效分档（**心=Killed_1 珠=Shatter——审计任务文字写反了，以源码为准**）；世花灯泡支撑破坏路径（CheckJunglePlant 2×2 锚回推）。
132	
133	**B 路 宝袋 4+2 真bug**（40000 次统计实证）：sw 掷面按袋内臂数（曾硬编码 8 面→四武器袋 50% 空手）+default 独立 branch（1313/1297/3858 撞号→共现双掉）；猪鲨袋 2623 chanceElse 撞 2609 的 1/10（90% 必掉→1/6 互斥）；史王/史后袋 dedup2 行自产两件（删冗余行，恰 2 件）；EoW/BoC 矿量 master 110-136/else 80-111 + **stackOf 优先级 bug**（stackVar 在 lo/hi 前吞区间）；EoC 袋 stackExpr 三段拆分；**devArmor=1/16 全局 Next(21) 套装表非 per-bag**（源码实证，21 组提取）。**光女白天 Enraged ai3+=2**（满血白天召出即 2；dash 重算曾覆盖 9999 白天档）→ Terraprisma 可达。骷髅王白天狂暴 Roar。
134	
135	**C 路**：**裁缝巫毒娃娃 1307 夜杀裁缝召骷髅王**（TownNPC.hurt 死亡钩→spawnVanillaEnemy(35)+Center 落位+boss 槽+HasAwoken）；史莱姆雨击杀计数加 AnyNPCs(50) 门（王在场不计数）。
136	
137	**审计勘误存档**：127=机械骷髅王本体（131=PrimeLaser 手臂！）——downed_134/125/127 三王判定本就正确；机械眼 544/蠕虫 556/骷髅头 557；血腥脊椎 1331 非 1329；明胶水晶 4988 非 4915；棱彩蜻蜓 661；塔→月总 3600t（12s 是天界印记专属）；猪鲨松露虫**有海洋带门**（:19213）；光女白天杀蝶**也召**（无日夜门）；蜂王浆无丛林门（原版本就无）。
138	
139	**遗留登记**：物品召唤落位仍用±55列顶扫（原版 SpawnOnPlayer 500 次屏幕外——已有 1:1 spawnBossOnPlayer 待统一迁移）；拒用 Toast 自造 UX；单 Boss 槽替代 AnyNPCs 精确门（架构性）；自然出王缺 HasAwoken（Game:16764 登记）；马桶 RedHatSkeletron 备案。
140	
141	关联 [[boss-summon-announce]] [[wof-voodoo-bossslot-fix]] [[boss-audit-prehardmode-2026-08-13]]。
142	
143	=====FILE: bunny-walk-frame-fix.md=====
144	---
145	name: bunny-walk-frame-fix
146	description: 兔子行走帧3倍速闪帧根因=aiStyle7小动物误套城镇NPC帧档;case46族专属分支(counter+=|vx|+1·>6进帧·全帧含帧0循环·腾空升4降6);aiStyle7路由须再分case族
147	metadata: 
148	  node_type: memory
149	  type: project
150	  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
151	  modified: 2026-08-18T15:53:31.543Z
152	---
153	
154	兔子跑动闪帧修复（2026-08-18，用户："兔子的能跑动画不对，帧换得非常快"）。
155	
156	**根因**：兔子 46 是 aiStyle 7，我们 vanillaFrameIdx 的 ai===7 分支是**城镇 NPC** 帧档（帧 2 起、counter += |vx|×2+1、每 2-3t 一换）——兔子 3 倍速闪帧且永远闪 2..6 帧（0/1 帧不可达）。
157	
158	**原版真值**（FindFrame switch **case 46 族**，NPC.cs:77553-77600：46/47 兔·病害兔、303/337/443/464/540/614、646-652）：站定=帧 0 清计数；腾空 vy<0=帧4 / vy>0=帧6；行走 counter += |vx|+1，**>6 才进一帧**，0..npcFrameCount-1 全帧含帧 0 循环。修：vanillaFrameIdx 在 ai===7 城镇分支**前**插 case46 族分支（counter≡walkCycleT+t，floor(/7)%frames）。验证：新公式 21t 序列 000011122223334444555（每 3.5t 一换）vs 旧 2233445566...（每 2t）。
159	
160	**教训**：aiStyle 7 双栖（城镇 NPC + 地面小动物）——同 aiStyle 不同 case 族帧律完全不同（城镇帧 2 起不含待机帧、小动物全帧含帧 0；城镇 ×2+1 小动物 +1；阈值 6 vs 城镇 6/12）。frame 分族查 case 标签而非 aiStyle。
161	
162	## 第二波（2026-08-18 同夜，用户："走路的金鱼非常鬼畜"）
163	
164	同一截胡的**其余全部 aiStyle=7 小动物**（case46 族只救了兔子系）+ 游泳族通用档过快，逐族补齐（NPC.cs 行号在 Renderer.ts 注释）：
165	- **230/593 行走金鱼**：counter += |vx|×2+1、**>10** 进帧全帧循环；腾空=帧0（case 230/593 :76584）
166	- **148/149/168/470 企鹅**：counter += |vx|（无+1！）相位 <6=0/<12=1/<15=2 回卷15；localAI 肚皮滑行带未驱动恒带0（:77094）
167	- **299/538/539/639-645 松鼠**：×0.5+1、>6 进帧，回卷**帧1**（跳过0）；腾空升2降4（:77160）
168	- **300/447/610 鼠**：站定嗅探 0/1@9t；行走+腾空同式 ×0.5+1 回卷**帧2**（:77215/:77260）
169	- **361/445/687 蛙**：wet 按|vx|分档帧10/11/12；陆上待机0..5@7t；行走相位[0,6,8,9]@6t；腾空升8降9（:77320）
170	- **362/364/602/608 行走鸟**：站定0；行走 counter+1 ≥4 进帧，带 3..9（:74445/:74517）
171	- **616/617 龟**：wet 游带8..13（走6t/停11t）；陆0..7@9t；腾空=8（:77379）
172	- **625 龟**：wet 游带6..11（走5t/停9t）；陆0..5@8t（:77434）
173	- **游泳族 ai===16 拆 case**（曾通用 t/4 通吃=全员1.5倍速）：鱼族 case55（55/57/58/102/241/465/592/607）6t 一档且 **wet 帧0..3 / 离水帧4/5 折腾分帧**（离水金鱼 4t 连闪即"鬼畜"另一半）；鲨鱼65 wet@6t 离水冻结；河鲀688 三态（鼓起4/5@6t、离水@12t、常态0..3@8t）；虎鲸692 wet 半表 5/7t；海豚615 搁浅帧4/wet 7t
174	- 测试 tests/critter-frame-cadence.test.ts 10 例钉住全部节拍
175	- ★方法论再证：`awk type==N → aiStyle=7` 枚举全集（616/617 因共享 else-if 块需人工补），再对每个 id 查 FindFrame **case 标签**有无专属分支——aiStyle 档只是兜底不是帧律
176	
177	=====FILE: ccccc-place2x2-anchor-check2x2.md=====
178	# CCCCC：Place2x2 右下锚族（411 矿爆+138 DeadMans 巨石）+ Check2x2 引擎 138/411
179	
180	接 AAAAA 移交两件，**两件诊断均部分错位，实证重定罪**：
181	①411 非 findDown 差一行（Searches.cs:60 含起点行 JS 镜像无差）——真根因=
182	PlaceTile→Place2x2（cs:59766→51352）**cs:51431 x--/y-- 右下锚**写 (x-1..x)×
183	(y-1..y)+双门（四格空置+逐列地面 nactive&&(SolidTile2||tileTable)，门败**静默
184	整写放弃**、WireLine/保护图照跑）。JS 曾左上锚无条件写=低一格右一列；金标全图
185	411 扫描证 vanilla 在 (861,735) 段本就未落（空置门败）——JS 幽灵块才是差，非
186	"轨道穿杀"。②三格 18,18vs0,0 非 Check2x2 缺派发（其不写帧）——DeadMansChest
187	巨石 138 同 Place2x2 右下锚，JS 左上锚=整块 (+1,+1) 偏移。修=MicroBiomes
188	place2x2Direct（含 Main.tileTable 76 id 地面右腿）+FinalCleanup check2x2Sweep
189	（cs:48405 镜像：锚反解/138 Boulders 支箱豁免+底支撑/411 非巨石逐列地面门/
190	destroyObject 闸整组杀+尾 4×4 帧）派发 case 138+411（411 必须同补：轨道巷杀
191	九宫 vanilla 同派发，否则顶行残活+缺 20 尘掷不可收敛）。★frameSparse 跳过表
192	+138/411：探针嵌合基座帧锚互指死区→与 184 杀级联互喂**无限递归**实爆；生产
193	帧自洽无碍。★tile-cleanup ⑥ fixture 补石底（浮空巨石派发后 vanilla 同序杀=
194	fixture 过时非回归）。#101：巨石 284/284 全同位、411 60 格集合+帧全同、.fr
195	both-314 76/76 零孤、掷流 165546→166921、A/T 19936/21843→8272/9157。遗留：
196	第二轨对角段 (783,740)→(920,801) golden 独有 JS 整段未落+多站点偏移（6512→
197	2397 格，TrackPass 域）；#105 持平 ZZZ 基线；mile8 首红 63 原样；54/54+41/41
198	回归绿。AAAAA"findDown 低一行/轨道穿杀"两说废弃。
199	
200	=====FILE: chunk-seam-noninteger-zoom.md=====
201	---
202	name: chunk-seam-noninteger-zoom
203	description: 树冠/仙人掌接缝真根因=chunk拼装非整数zoom落小数像素(1.27→325.12);修复=drawChunkGrid整数设备矩形;相机snap不救chunk边界;解剖台A/B方法论
204	metadata: 
205	  node_type: memory
206	  type: project
207	  originSessionId: 573d63f5-287b-42b0-99c2-a96bc6fc7c8a
208	  modified: 2026-08-18T08:08:05.441Z
209	---
210	
211	# chunk 拼装非整数 zoom 接缝（2026-08-18 收官，用户三轮报障）
212	
213	用户报"树冠-干交界细缝（无风也有）+ 沙漠仙人掌柱同款 + 解剖台里没问题"。真根因：
214	**chunk 拼装** 旧公式 `drawImage(chunk, cx*256, cy*256, 257, 257)`（世界变换内）——
215	`256×zoom` 非整数时 chunk 落小数设备像素，各 chunk 独立最近邻采样在边缘产生周期性
216	1px 透明缝。默认 1.25（=320 恰整除）从未暴露；用户自调 **1.27**（325.12）触发。
217	
218	**Why**: 相机 snap（`round(cam.x*z)/z`）只保证【相机】对齐；chunk 边界设备位置 =
219	`k×256×z mod 1` 随 zoom 漂移，1.27 下每块不同——逐块绘制必须显式整数化每块的
220	目标矩形。
221	
222	**How to apply**:
223	- 修复 = `drawChunkGrid('wall'|'tile')`：`setTransform(1,0,0,1,0,0)` 后逐 chunk
224	  `xd0=round((cx*256−camRX)*z)`，尺寸 `xd1−xd0+1`（保底 1px 重叠）——任意 zoom 无缝。
225	- **排查方法论（本轮最值钱）**：用户报障无法复现时，搭"解剖台"——用真实渲染代码
226	  单独渲染 + 让用户标注（public/tree-inspect.html：群系/冠样式/变体/风况/相位/
227	  chunk 公式档 + F5 报告 `tiles.areaPlayer` RLE 导入还原用户真实世界 + 标注导出）。
228	  "工具里没问题"本身即是信息 → 差异枚举法收敛到工具未复刻的结构（chunk 网格）。
229	- F5 报告 `tiles.areaPlayer`（65×65 RLE, `sheet:fx:fy:wall:liquid`）可直接重建用户
230	  世界局部——免去同种子世界重生（大型世界 UI 路径 5-13 分钟且机器负载敏感）。
231	- 误排查教训：先证伪"采样模式"（线性=糊化负优化已回退）、干件帧/枝表/冠帧表/
232	  静止几何全排除——真因在比"树渲染"更低的层。**用户换过 zoom 档**要第一时间问。
233	- 关联 [[treecrown-seam-and-topsize]]（树渲染层审计与 Tree_Tops 帧表修复）。
234	
235	## 追加（0818 五轮）：夜间横缝收官 + 两个连带修复
236	- 夜间树冠/枝横缝 = 摆动层逐帧重绘的小数偏移（offX/offY）→ 边缘行设备像素跳变；夜间剪影高对比才可见（白天全部探针测不出）。修复 = renderEnv.zoom + devSnap 设备像素吸附（冠/枝/棕榈冠绘制目的地 1/zoom 网格对齐）。
237	- chunk 修复曾漏 viewW/2 中心偏移 → 世界左上偏半屏（用户实抓"地面以下方块偏移左上"）——退出变换绘制必须完整复刻原变换（中心平移×缩放×相机）。
238	- 诊断方法：用户截图全图水平线检测（逐行垂直梯度异常聚类）→ 线簇对表树标记行（枝行命中/冠交界零命中）定位到摆动层。
239	
240	=====FILE: cursor-icon-fullbright.md=====
241	---
242	name: cursor-icon-fullbright
243	description: 光标悬停物品图标恒全亮——GetItemLight 默认参不采光照;source-atop 叠黑画布=黑方块陷阱
244	metadata: 
245	  node_type: memory
246	  type: project
247	  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
248	  modified: 2026-08-18T07:33:36.482Z
249	---
250	
251	DrawInterface_40 悬停图标（Main.cs:44519）调 `ItemSlot.GetItemLight(ref color, num)` 时
252	**outInTheWorld 用默认 false → 根本不采样世界光照**（ItemSlot.cs:3458 只处理迪斯科
253	662/663/5128、微光脉冲、精华 58/184/4143），currentColor 恒 White → 图标**任何时候全亮**。
254	
255	**Why:** 曾误读为"乘光标格光照"并用 `globalCompositeOperation='source-atop'` 叠黑模拟变暗
256	——source-atop 作用于整张已渲染画布(世界层不透明),暗处 alpha→1 = 纯黑方块盖住图标
257	(2026-08-18 用户报"悬停贴图全黑")。
258	
259	**How to apply:** 图标/UI 层永远直画不乘光;要乘色时用三步离屏(multiply+destination-in
260	恢复 alpha),绝不在主画布 source-atop。未接的特殊物品改色分支已在 Renderer 注释备案。
261	关联 [[cursor-item-icon-port]]。
262	
263	=====FILE: dome-slot32-pot-waterbolt-inact.md=====
264	# MMMM 批：12345 #32 Dome 残余三根因（瓦罐支撑门/水书掷位/致动柱链）
265	
266	- **主根因=PlacePot 支撑门语义**：`dgDungeonPot` 曾用碰撞语义 `genSolidType`（平台
267	  false）——vanilla `WorldGen.PlacePot`（cs:54082，:54099-54102）= **nactive()+
268	  Main.tileSolid**，平台 19 生成期 tileSolid=true（GenSolid `vanGenSolidType` 差集
269	  9 类）。Dome 平台罐全数失败 → 每罐漏掷 Next(3)（:54113 成功才掷）→ Platforms
270	  起全链掷位漂移（旗/挂毯/钟/画全错位）。Legacy 房/廊候选 IsAShelf=false 无罐
271	  路径 → 单种子绿掩盖。**教训：凡读 Main.tileSolid 的调用方必须走 vanGenSolidType**。
272	- **次根因=水书掷位**：`d.nowb === false` 对缺省字段（undefined）不成立——Dome
273	  下对平台候选无 NoWaterbolt 字段 → 整族漏掷 Next(50)（GenerateDungeonBook 默认
274	  重载参数位 DU:426-429）。JS 布尔字段判别禁用 `=== false`，用 `!== true`。
275	- **致动柱链**（与 LLLL HalfBrickPass 侧互证）：DungeonPillar.GenerateTileStrip
276	  :151-154/:200-203 `flag4→inActive(true)`（平滑后置）——JS dgPillarStrip 加 inact
277	  参（ClearTile 先清 bit5）；SolidOrSlopedTile/!inActive（WG:70046）→ solidOrSlopedD；
278	  SpreadWallDungeon 走 SolidTile（WG:70155 !inActive）→ dgSolid（W 776→0 即此：
279	  致动格非实心可传播）；灯笼/吊灯/桌面锚 nactive（cs:46705/:52769/:45360）。
280	  结果 Ia 234→0、Sl 8→0。
281	- **Dome/Tower 入口盒特性门**：DomeDungeonEntrance.cs:31-38≡Tower:31-38 拒
282	  Bookshelves/Paintings/Spikes（hitbox 内；基类另拒 BiomeChests=任何入口）——
283	  JS 补 `entNoFeat`（entKind!==0）于 spikeRun/书架门槛/featArea3 三点。
284	- **验证**：12345 #32 八通道全零、#33-46 连带绿、#53 塌缩 93%（余项=上游祭坛
285	  6 格级联，LLLL 反事实证净输入下=0）；9293480 0..53 全绿（Legacy 结构性无操作）。
286	  Tower 支同修未验（双链无 Tower 种子，矩阵 s33333 复扫）。
287	
288	=====FILE: fog-flicker-f4-latetex-fix.md=====
289	---
290	name: fog-flicker-f4-latetex-fix
291	description: 迷雾三修(20s看门狗误清fogPix=周期全亮闪/F4空同步=row停h未复位/分带重建fill(0)闪)+生命树晚到贴图note被pending早退吞——四根因四修复全探针实证
292	metadata: 
293	  node_type: memory
294	  type: project
295	  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
296	  modified: 2026-08-18T16:18:54.254Z
297	---
298	
299	2026-08-19 用户三报(debug-report 存档):①HUD 迷雾周期闪"全亮一下又恢复";
300	②F4 消雾失效;③生命树贴图不及时,手动破坏方块才渲染。
301	
302	## ①② 迷雾双 bug(同一文件 ensureFogData)
303	**闪烁根因 = GPU 看门狗(20s 巡检)误清 CPU 数据**:recreateAuxCanvases 无条件
304	`fogPix=null`——但迷雾是纯 CPU 缓冲与画布上下文死活无关!每 20s 被清 →
305	缓冲重建(全 0=全亮)+ 分带 5 帧扫回雾 = 用户看到的周期闪(探针实测整幅重建
306	精确间隔 20s:24.8/43.9/63.9s)。修:fog 缓冲只在 dispose 清;看门狗只重置
307	_mapFogRowSeen(GL 纹理游标)。
308	**F4 失效根因 = 空同步**:整幅重建完成后 fogRebuildRow 停在 h 不复位;下次
309	整幅入口(F4/版本跳跃)row≠0 → `if(row===0) fill(0)` 不执行+分带循环零迭代
310	→ 直接落版本 = 什么都没画但版本追平。修:入口 `if(row>=h) row=0`。
311	**顺修**:分带循环改双向写(seen?0:FOG)+ 删 fill(0)——旧缓冲逐带纠正,
312	重建期不再有全亮帧(新缓冲天然全 0)。
313	观测:Renderer.fogFullRebuilds/fogIncrUpdates/fogFullWhy;探针
314	scripts/_fogwatch-probe.mjs(40s 走动整幅重建应恒 1+F4 后雾覆盖归 0+无回弹)。
315	修后:整幅=1、F4 雾覆盖 0%、10s 无回弹、零闪帧。
316	
317	## ③ 生命树晚到贴图(note 被早退吞)
318	用户实报"手动破坏才渲染"= 晚到重烘链断。内窥探针(原型级 wrap
319	ensureVImage/vframe/note/onLoaded)铁证:烘焙期 ensure(Tiles_192) 时
320	**pending=true**(加载已被预载/他人发起)→ `if(pending) return null` 早退在
321	`bakeTracker.note(file)` **之前** → 晚到无人重烘 = 缺表 fallback 钉死。
322	修=note 提到早退前(failed 也 note:重试成功二次 land → 链路反而闭环)。
323	探针复验:拦截延迟 Tiles_191/192 15s → 传送生命树 → 表到达后
324	arrive=23(23 个 chunk 精确重烘)。
325	★探针两坑:st.type 是【内部 id 空间】与 vanilla vid 无关,找 tile 必经
326	__swTileByKey 换算(曾两轮扫错地方得出假阴性);像素断言要匹配目标色系
327	(生命树传送点在树冠=绿叶,判木质棕必 0)。
328	探针:scripts/_latetex-probe.mjs(断言版)/_latetex2-probe.mjs(全链内窥版,
329	request interception 延迟目标表 15s)。
330	
331	相关:[[dualwindow-iosurface-exhaustion]](canvas 哨兵/BiomeBackground 同期)
332	[[dungeon-crash-targeted-rebake]](晚到重烘链前身) [[imagebitmap-root-cure]]
333	
334	=====FILE: half-slab-liquid-band-parity.md=====
335	---
336	name: half-slab-liquid-band-parity
337	description: 半砖浸润缺失根因=flag5自身格液体分支未移植(TileDrawing:3943只读四邻)+五处家族差异全修(y0门/坡面边角门/半砖墙后门/蜂蜜alpha/致动门);四条定性保留偏差登记
338	metadata: 
339	  node_type: memory
340	  type: project
341	  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
342	  modified: 2026-08-18T17:24:24.578Z
343	---
344	
345	2026-08-19 用户报"水体动态渲染:半格方块浸润未处理 + 效果与原版不一致"。
346	
347	## 根因(flag5 自身格液体)
348	原版 `DrawTile_LiquidBehindTile`(TileDrawing.cs:3943-3963)有 **flag5**:
349	`tileCache.liquid > 0 && num4 != 0 && (num4 != 1 || liquid > 160)` —— 半砖/
350	坡面格【自己格内】的液体也画浸润(水搁在半砖上存进半砖格)。我们的
351	drawLiquidBehindTilesOnly 只读四邻、从不读本格 = 整类缺失(用户主报)。
352	blockType(num4):0=整块/1=半砖/2-5=坡面。
353	
354	## 同轮修复的家族差异(逐条对照源码)
355	1. y0 门(:4084-4087):`上格无液 && (num4!=0 || !SolidTile(上))` → 从格顶画;
356	   旧版漏 `num4!=0 ||` = 半/坡面带矮 4px。
357	2. 坡面边角门(:4155-4162):slope4 左侧无液无实心 / slope3 右侧同 → 整带不画。
358	3. 半砖+上格有液+有墙 → 整带不画(:4148-4151,地下半砖水由水体本体呈现)。
359	4. 蜂蜜 alpha 恒 1(:4141 max(0.5×1.7,1))。
360	5. 致动幽灵格不画浸润(:3906 !active() 同族;wire&32)。
361	
362	## 定性保留偏差(登记未修,见函数头注释)
363	①:3906 半砖+侧液>160+瀑布跳过门(需瀑布管理器接入);②:3921 type546 自液体
364	特例;③:3910 BlocksWaterDrawingBehindSelf 族;④:4163 地下半砖+上液"顶部
365	顶点色×0"(逐 quad 垂直渐变,Canvas 2D 近现代价高;洞穴暗背景下视觉差极小)。
366	
367	## 验证
368	数值:半砖格上半 avg[8,57,177](强蓝=浸润带)、下半 [128,95,73](土砖)、
369	对照水格 [80,122,191] ✓;视觉分析确认两侧水体正常无异常。59 液体测试+tsc 绿。
370	探针 `_waterband-probe.mjs`。
371	★探针四坑(连环踩):①采样行号写死错行;②场景放地下 6 格=无光全黑(须
372	地表上方悬空台+日光);③世界可能开局入夜——须强制 timeOfDay=0.4;
373	④相机≠玩家坐标,采样用 g.camera 实时投影(zoom 1.25 别漏乘)。
374	
375	相关:[[vanilla-liquid-port]] [[snow-blizzard-ripple-fix]]
376	
377	=====FILE: jungle-parity-and-id-collision.md=====
378	---
379	name: jungle-parity-and-id-collision
380	description: 丛林链种子等价全绿(terrain..desertmound 19 checkpoint) + 内部EMPTY(0)≡原版幽灵泥土(0) id碰撞 + rng.int上界开/闭换算三案
381	metadata: 
382	  node_type: memory
383	  type: project
384	  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
385	  modified: 2026-08-16T06:26:13.584Z
386	---
387	
388	2026-08-12 丛林链种子等价收口：`tests/caves-checkpoint.test.ts` 双种子×19 checkpoint 全绿（terrain..desertmound，含 jungle/mudcaves/desertmound type+flags+liquid 三哈希）。金标由清理后的 `dotnet run tools/golden/caves-oracle.cs <seedInt> <evil> tests/golden/caves-chain-*.json` 再生（SandboxWorld 种子 int=1511931452，evil=1）。
389	
390	**本轮修的 4 个真 bug（均已对 Terarria1456 反编译源码校验）**：
391	1. JS `JunglePass.placeGemsAt` 偏移区间闭→开（`int(-⌊125ws⌋, ⌊125ws⌋-1)`），闭区间多 1 档时 gem runner 落点差 1 → 巨型泥 runner 扫描内 1 格骰值偏移（总消耗自愈、值错位）→ ~292 格写出差；
392	2. JS 收尾 loop-3 宝石**掷序**：原版 `type2=Next(63,69)` 在实参求值前（type→x偏→y偏→strength→steps），JS 对象字面量把 type 排最后=流错位（同 [[seed-equivalence-plan]] 掷序家族）；
393	3. JS `IceBiomePass` 转化不判 active（原版 cs:12394 switch(type) 写幽灵）+ `t===0` 要并入泥土族；
394	4. **Oracle 反向 bug**：`flag4 = Main.tileStone[type] && tile2.type!=1`（Main.cs tileStone={63-68,130,131,566}，**不含石头1**）——宝石铺设仅替换活性石头；oracle 曾漏此行致宝石覆盖活性泥、污染后续 type==59 拒绝采样。
395	
396	**ID 空间碰撞（大坑）**：内部 EMPTY=0 ≡ 原版幽灵泥土 type=0。凡原版 `case 0:`/`type==0` 的判定，JS 必须 `t===0 || t===T.DIRT` 双判；对账脚本 V_ID 映射里 internal 0→vanilla 0。BeachPass 海盆挖掘原版仅 active(false) 保留幽灵（曾清零 → 6383 格天空幽灵差）。
397	
398	**rng.int 换算铁律**：`rng.int(a,b)`≡闭区间[a,b]≡`Next(a,b+1)`。原版 `Next(a,b)` → `int(a,b-1)`；原版 `Next(a,1+⌊k⌋)` → `int(a,⌊k⌋)`。写 `int(a,b)` 前先想清楚原版上界。
399	
400	**探针纪律新增**：逐格 c-trace 对账时两侧 id 空间不同（JS 内部 vs oracle 原版），先归一再比，否则全是假差异；多轮"分叉"实为 id 错位乌龙。全网格直比（cs-jt.bin dump）比哈希二分快一个数量级。
401	
402	遗留：oracle 已延伸至 desertmound；Desert Sub-B(Hive 逐字段)/Sub-C(入口4形状) 未转录；发光蘑菇/大理石花岗岩/浮空岛/DirtToMud/地狱/腐化/湖泊等 pass 的 oracle 延伸未做。
403	
404	**★ 2026-08-12 晚间进度（沙漠/改序/2a 三连收）**：oracle 现已覆盖 terrain..ores 共 36 checkpoint 双种子全绿（新增 desertentrance/hive/done、mushroom/marble/granite/islands/dirttomud/silt/ores）。沙漠轮：入口概率 0.3333→**0.5**（Configuration.json 覆盖）、DesertHive shell/0.25 骰走**独立 FastRandom 流**（已 1:1 进 src/core/rng.ts，64 位补码 WithModifier 坑）、Sub-C 四形状（Chambers/Anthill/LarvaHole/Pit）1:1。2a 轮：JS bug 含 beachDistance=floor(w*0.06)=252 错、原版 **readonly 380**（WorldGen.cs:4102）；ShinyBand 计数 (int) 截断（oracle）；沙岩 flag4 漏 `!Ore` 赋值（JS）。改序轮：5 处偏差已修（见 [[vanilla-pass-alignment]] 文档）。l10n 坑：vitest buildStart 被缺键硬拦——**键补在仓库根 tools/l10n-custom/{en,zh}.json + `node scripts/build-l10n.mjs` 重建**，直接改 public/l10n 产物会被 stale 检测覆盖。GemPasses seedFlags 判空（测试手搓 gs 无该字段）。
405	
406	**★★ jungle 根因级分歧收口（2026-08-16 13:3x 验收）——三处"共同错"全破，jungle+mudcaves 与原版逐位相等**：①**PlaceWall 语义**（WorldGen.cs:75199）：仅 wall==0 落墙（边界(1,W-2)）且每墙成功落 WallFrame 掷 1 颗 Next(0,3)（Framing.cs:390 无 generatingWorld 门）——曾无条件覆写+零掷（TileRunner 新增 placeWall()）；②**KillTile 活性格清 type=0**（cs:63970，SquareTileFrame 的掷在 !generatingWorld 门内不掷）——曾误记"保留幽灵"（隧道挖空语义与 TileRunner dig 不同！）；③**holes 下界用 GenVars.worldSurface=Terrain 终值 num3 ≠ Main.worldSurface(337)**（JunglePass.cs:220）——恒耗 1 掷流不变而 y 平移=隐形分叉形态。**验证：jungle+mudcaves 四面哈希+ghost==原版 pass17/18，七段流指纹+1050 轮 holes 全等，4200×1200 全格逐位 0 差**。下游：pass19(Full Desert) 起为沙漠链独立债（修复前已存在，非级联）。JSeg 段级流指纹基建留复用；世界终态金标已 UPDATE_GOLDEN 再生。**⚠️幽灵语义细化：KillTile(隧道) 清 type ≠ TileRunner dig 保留 type——两套挖空语义并存**。
407	
408	**★ 每 pass 重播改造终版交付（2026-08-16 13:2x 报告归档）**：oracle 44 pass 头 Replay()+测试链 39+32 处+generateWorld 槽头/槽内 45 处全部落地（RNG.reseed() 原地换流）；**附加归位：地牢入口三掷（DungeonCrawler.cs:174/177/856）原版在 Dunes pass 头（cs:11542）消耗——续流期曾两侧同步延后到 Dungeon 头，已归位（dgEntSeed 传递）**。desert/dungeon/shimmer 内部检查点不播（pass 内段）。金标已再生但 **world-final(10:41)/shimmer(10:17) 早于 12:38+ 的 JS 债修复——jungle 代理收尾后需再再生一轮**。⚠️RNG.reseed()=新基础设施（原地换内部流对象引用不失效）。
409	
410	**★ 全链双种子零红达成（2026-08-16 13:0x 独立验收）**：caves-checkpoint **3/3 全绿=138 检查点零红**（每 pass 重播架构下双种子 terrain→surfacewaterinjungle 全链含地牢/沙漠/微光）。最后两债：dungeonI=SetCrackedBrickSolidity（DungeonCrawler.cs:344 裂纹砖 481-483 翻非实心，JS 灯链四消费端读静态表→flipGenSolid+genSolidType 化，oracle 本就对）；livingtrees=四处（石堆 Place3x2 底中锚+滚石拒绝 cs:39005/门每扇 3×Next(3) 帧掷 cs:59870/宝箱 flags.sky+wooden 缺失→rollChestLoot 流错/根系门 wall!=244+步进 num34+=num40 cs:28612 两侧均非原版）。16 种子矩阵 16/16 Δws=Δrl=0 保持。jungle 掷骰狩猎代理仍在跑（对原版真值的最后一层）。⚠️遗留：头注已更新；oracle_jseg.json 曾被并发碰撞建议抽查。
411	
412	**★★ 原版真值链注入交付（2026-08-16 午）——"一模一样"的权威逐 pass 裁决器建成**：给原版服务器 RunPass 尾注入与 caves-oracle Checkpoint 同算法四哈希探针（net48 探针类整体导入模式；`/tmp/sw-num4/probelib/PassChainProbe.cs`+patch passchain 模式；SW_EVIL 环境变量强制邪恶；106 pass 全链 40-50s/世界）。**⚠️ 沙盒铁律：必须 `arch -x86_64` 跑**（arm64 Mono 的 (int)NaN→0 vs x86 int.MinValue——dunes 曾现 9 格假分歧）。**裁决结果（5 种子一致）**：①**terrain→grass（#0-16，14 检查点）JS/oracle=原版逐位复刻**（四哈希+ghost+流指纹全等）；②**jungle(#17)=全链唯一根因级分歧**（掷骰数分叉+35.8 万格，其后 FNV 级联+掷骰数连锁污染——jungle 收口前下游哈希裁决不具终局效力）；③oceancaves 无债（四面 diff 恒等+掷骰数同）；④livingtrees 债确证=树选址级（两侧各种各的树 192/191 棵互不重叠+mud↔活木 800 格）；⑤dungeonI 的 JS↔oracle 分歧独立，终局参考=/tmp/sw-num4/van_x86_g/032_Dungeon.*。**工具/数据全在 /tmp/sw-num4/**（passchain_x86.txt 权威链、van_x86_g 3.0G 网格 dump、cmpall.py/diffcount_x86.py、oracle-all.cs 带全 dump 副本）。exe 已恢复 sha256 校验。
413	
414	**★★ num4 悬案破解（2026-08-16 凌晨，Tier B IL 注入终判）——种子等价工程最重要单一发现**：**原版每个 GenPass 执行前都重播种子**：`WorldGenerator.RunPass` 开头 `Main.rand = new UnifiedRandom(_seed)`（1456 WorldGenerator.cs:497，服务器 exe IL 实证 newobj+stsfld），`GenBase._random=>genRand=>Main.rand`。→ TerrainPass 从 stream(seed) **第 0 掷**开始，与 Reset 流无关。JS/oracle 曾同构"续流"→互检全绿却对不上原版（Δrl 全 6 倍数/σ≈50 签名的真相=共享前缀其实不存在，巧合掩蔽 num3 的 clamp 上界）。**修复 5 文件**（caves-oracle:199 重绑 fresh/terrain-oracle 同构/WorldGen.ts:512 runTerrainPass 前 new RNG(gs.seed)+ctx.rng 回传/MountCavesPass 沙族闩锁误读 cs:11861-11879/金标 8 份再生）。**验证：7 种子 oracle vs 原版服务器轨迹 4200/4200 列位级全等（R 精度 double）；16/16 种子 Δws=Δrl=0**（.wld 头部 ground/rock 全等，含 medium 493/667）。IL 探针 v2 经验：手写 IL 被 Mono JIT 拒+RunPass try/catch 吞——用 net48 编译的 C# 探针类整体导入。**★结构性大备案：vanilla 每 pass 重播 → JS/oracle 现仅 terrain 边界重播、后续 pass 仍续流（两侧同构互检有效，但要对原版后续 pass 需逐 pass 重播——下一个大项）**。遗留：livingtrees(网格写差)/oceancaves(流分叉)=新流暴露的转写债；L2 仍 ~50%（后半段+每 pass 重播改造）。沙盒已恢复（sha256 校验）。
415	
416	**★ A 批被停+并行会话 oracle 提交错位（2026-08-16 01:50 现场快照）**：A 批代理被用户手动停止（其最终状态：pyramids/dirtrockwallrunner/altars/surfacewater 流已对上，唯 livingtrees 不同；金标曾被其再生成）。**当前 checkpoint 全景**：双种子从 mountaincaves 起红——**type 全等仅 flags 差**=Mountinater 山丘形状分歧（激活天空格 typ0→0 不改 type 哈希的特征）。根因：并行会话**已 git 提交** oracle 侧改动（HEAD 含之，工作区对 HEAD 仅多 GV_DUMP 诊断钩子），JS 侧 MountCavesPass(8/13 旧版) 未镜像——其在制。**⚠️纪律重申：并行会话活跃期勿再生成金标**（我 01:44 的再生已与其在途状态纠缠；A 批教训："金标文件不可信时以现场 dump 对拍为准"）。num4 终判代理仍在跑（Tier B 注入中）。R 批成果完好。下一步：等并行会话 JS 镜像落地（mountaincaves flags 复绿）→ 再生金标 → 续 livingtrees。
417	
418	**★ R 批交付（2026-08-16 凌晨验收）**：四循环合一完整落地（无需降级方案：BuriedChests/CaveHouse 导出零改动，靠 CaveHouses 内部头尾四翻幂等——地狱箱/洞窟箱首次进入 226/162/225/190 翻转窗口=placeBuriedChest genSolidType 落地对齐）；templePart2 拆分（gs.tLeft/tRight/tTop/tBottom/tRooms 5 字段，采样域换算逐值等价已核；早退不写=原版语义；232 翻转清掉旧备案偏差）；HellFort 前移入生物群系槽（Underworld 尾）；浮空岛屋新槽位。55→56 槽。回归 3502 过/8 红（world-final-hash 预期红待安静窗再金标；caves-checkpoint 红=A 批在途；player-run-parity=并行会话实体代码）。备份 /tmp/sw-rbatch-backup/。firefly-fairy 测试按新序重写（spawn 锚窗变化）。**当前 checkpoint 状态：gems→shimmer→dirtwallcleanup 绿，pyramids 复绿（A 批 00:33-00:37 推进），livingtrees/altars/surfacewaterinjungle 红=A 批进行中**。
419	
420	**★ num4 终判启动（2026-08-16 凌晨）**：侦察破局——**不需要 Windows exe**：Mac TerrariaServer.exe 可在 /tmp 沙盒原生跑（HOME 隔离），ReLogic=内嵌 manifest resource 自解压（反射失败真相：非合并，需预解压 resource——未来任何反射 harness 适用）；Tier B（Mono.Cecil 注入 ApplyPass 逐列 num3/num4 打点）代理已启动：7 种子轨迹→与我们 /tmp/cols_all.csv 逐列 diff→首分叉列→1456 裁决→修复→Δrl 归零。沙盒 /tmp/sw-num4/（srv+home+probe 解密器），补丁后 exe 恢复机制=backup 目录。侦察还发现：本机 tModLoader setup 有加密 win exe（AES-CBC 零 IV+Deflate）但密钥=proof 哈希不可本地恢复（无增量，仅 Mac/Win IL 对账用）。
421	
422	**★ B 批预研完成+四代理并行纪（2026-08-16）**：B 批（#45-64=LihzahrdTemple→MossAndMossCaves，以 1456 注册序为准）预研报告完整产出（逐 pass 表/三项特别核查/风险清单——**关键发现：templePart2 五段被内联在 #45 执行而原版在 #65 独立 pass（cs:17809），不拆则 B 批全错**；#58 四循环合一+地狱箱槽错位+HellFort 前移连带；SettleLiquids 缺 oceanDepths 转水头扫；offLimitBorderTiles=40 硬编码中大世界≠）。分批建议：R（槽位手术）→B1-6。**四代理并行中**：A 批收尾（pyramids/livingtrees/altars/surfacewaterinjungle 四段红，占 oracle 尾部+四 JS pass）、R 批（WorldGen.ts 槽位重排+templePart2 拆分，占 WorldGen/GenState/TemplePass——与 A 零文件交集，checkpoint 测试链直调不受槽位影响）、num4 侦察（Windows exe/服务器插桩两路线评估）、B 预研（已交付）。金标 65 条双种子已再生（第三轮 A 的 7 段绿：gems/gravitatingsand/oceancaves/shimmer×4/dirtwallcleanup）。
423	
424	**★ 骨架层双种子全绿达成（2026-08-15 22:12 独立验收）**：caves-checkpoint **3/3 通过=双种子（腐化+猩红）terrain→beaches 35 pass 含地牢 17 中间态逐哈希全等**（代理 21:37 完成猩红 JS 跟进收掉最后 22 级联）。**诚实边界（代理总结正确）**：①对标物是 oracle 非 .wld 原版本体（两侧同错仍绿——三天抓过 oracle 4 自身 bug；L2 真金标=原版 .wld 字节级对拍待做）；②覆盖到 #34，后半段（Gems/Altars/SmoothWorld/Trees/Moss/FinalCleanup 等）未对账且 world-final 终态哈希仍红（流移位会在后半段再暴露语义差——deserthive 同剧本）；③哈希省略坡度/半砖与帧号。**新立案**：world-invariants 报祭坛缺角 1 格+祭坛数超基线（疑 corruption/dungeon 修复后祭坛基数真变了，需核）。
425	
426	**★ 终局里程碑（2026-08-15 晚，独立验收）**：**seed 9293480（evil=0）54/54 检查点全绿**——terrain→beaches 含完整 dungeon 链（dungeonL..dungeonBa 17 中间点+下游 mcopenings/beaches，并行会话 8/14-15 收掉，含 CanPlaceTileAt(DungeonHall.cs:161 普通世界仅非地牢墙置砖)双侧同步修复）。deserthive 修复稳定存活两轮金标。**唯一残留：SandboxWorld(evil=1) corruption 起的 22 级联**——JS CorruptionPass(8/13 20:09) 落后 oracle(8/15 21:04) 半步=猩红路径；dungeon 段又绿（独立房间种子流未感染）证明只需修 corruption 本段。侦察代理工具链在 /tmp（仓外探针跑 vitest 新路+预构建二进制+dump 对拍脚本）。截至现状 checkpoint 链覆盖=**#1-35 全部原版 pass 的 JS≡oracle 双种子验证（除猩红段半步）**。
427	
428	**★ 16 种子矩阵定量签名（2026-08-13 夜）**：14 有效种子 Δws **11 个精确 0**（miss -12/-16/-38 均伴大 Δrl=分叉点在 num6 max 列前的种子）；Δrl 全 6 倍数、σ≈50、均值 +8（无系统平移、钳制常量正确）；**seed 8888 全对**（Δws=Δrl=0）；idOk/moonOk 14/14 真。**关键统计**：独立双游走差值 σ 应≈92（65√2），实测≈50 → 两侧强相关=共享长公共前缀+单一分叉点（种子依赖列）后独立尾巴——num4 悬案的最锐签名。16 种子数据在 /tmp/vserver/（oracle_*.txt + s*.wld），工具 tools/_matrixcmp.test.ts。
429	
430	**★ deserthive 复绿代理交付（2026-08-13 晚）**：双种子 terrain→slush 32 检查点+沙漠 3 wall 全绿。6 装饰真 bug（485 Origin=(0,1) 占 px..px+1；751/484/187 各自 Place2x2/3x2 的 x-- 语义=占 px-1 起；两侧缺 PlaceObject/2x2/3x2/CanPlace 门禁；**漏掷 Next(4)**（CanPlace RandomStyleRange 恒掷且走 Main.rand 共享流）；tileSolid[484]=false（cs:12537 首句））+granite CA 稀疏写 Swap 语义（oracle 错）+lakes 漏斗 v⁴（oracle 错）+placeTight 地面分支排除冰雪族（潜伏）。**★金标失真教训：18:30 再生的金标 deserthive 曾写成 JS 值（真 oracle=514d141b）——金标文件不可信时以 HIVE_DUMP 现场对拍为准**；另两条 oracle 不可并行跑（runfile build cache 互锁）。dungeon 链 19 红=并行会话在改 oracle 地牢段（21:22-21:57 活跃），让位等其收口。
431	
432	**★ #32 Dungeon 交付+并行编辑让位（2026-08-13 晚）**：代理完成 1456 Legacy 路径全量转录（oracle +1400 行/16 中间检查点 dungeonL..Ba/含战利品 Prefix(-1) 掷骰建模；JS DungeonPass 2480 行重写同构；7 真 bug：LegacyDungeonHall zero2 符号/Next(0,num/3) 上界/宝箱 Origin(0,1)/家具 id 勘误(书架 101 钟 104 钢琴 87 沙发 89 浴缸 90)/门色 1411-1413/尖刺二段起点/Prefix 缺失）。金标 51 条双种子，terrain..slush 不变 ✓。**我补的镜像**：JunglePass 分支洞穴 mudWall=true 掷骰（17:2x 另一会话修复的 oracle 侧同步）→ jungle/mudcaves/desert 段复绿。**当前残余**：deserthive/mushroom/marble/granite/islands 红=另一会话**正在编辑中**（DesertPass 17:41/MarbleGranite 17:43 在制）——让位等其收口后镜像+金标再生。**JS dungeon 逐段对账待上游绿后做**（dungeon 17 检查点因上游流移暂不可比）。world-final-hash 金标待 JS dungeon 验证后 UPDATE_GOLDEN=1 再生。
433	
434	**★ 尺寸轴验证（2026-08-13 傍晚，JS-vs-原版直比无需 oracle）**：中世界 6400×1800 种子 31415926 **ground=493 与原版精确相等**（rock +84=num4 族）；大世界 8400×2400 种子 27182818 ground -79/rock +95（num3 max 也被分叉波及——与"分叉点后 num6 是否冻结"自洽）。**结论：num4 悬案=跨尺寸单一根因**（三尺寸同族偏差）。**新立案**：JS DungeonPass 中/大尺寸位置大幅偏差（medium JS 5449 vs 原版 830；large 1330 vs 7194）——4200 之外的地牢尺寸行为未对账，#32 后核查。num4 统计三角定位批采（10 种子）进行中。测试工具 tools/_sizeaxis.test.ts（可复跑）。
435	
436	**★ #22 收敛矩阵工具已建成（2026-08-13 下午）**：`tools/convergence-matrix.sh gen|cmp` + `tools/_matrixcmp.test.ts`（服务器真值+oracle 批量+头部对拍，含超时/完成标记/进程纪律）。7 小世界种子全链结果：idOk/moonOk 全真、Δws 6/7 精确 0（33333 独差 -16 且 rl-ws=198 两侧同 k——与 num4 同族的"中段游走分叉"）、Δrl 全非 0=num4 悬案。**尺寸轴真值已采**：中世界 m31415926（6400×1800 ground=493 rock=667 dungeon=830,388）+ 大世界 l27182818（8400×2400 ground=604 rock=916 dungeon=7194,382）——oracle 目前 4200 硬编码，尺寸扩展=oracle 参数化（待 #32 后）。新小世界种子 s20260811/s2147483647 已采（oracle 输出待补）。
437	
438	**★ 后台脚本铁律（2026-08-13 用户指正定案）**：①所有批量脚本**每条子命令必须带超时**——macOS 无 timeout，用内联守护：`( cmd & P=$!; sleep 120; kill $P 2>/dev/null ) & wait` 或 `perl -e 'alarm 120; exec @ARGV' -- cmd`；②脚本结束必须打完成标记（`echo DONE >> out`）+ 主动 `wait`，不允许裸后台游离；③启动前 `pgrep -f` 查同类、结束后复查进程归零——**失控循环曾烧满核数小时未察觉**；④后台任务 env 前缀会丢——env 一律脚本内 export；⑤长循环每 N 轮落盘心跳行，便于判断卡死位置。
439	
440	**★ 多尺寸地形层一次命中（2026-08-16）**：oracle 第 4 参 size∈{0,1,2}（W/H=4200×1200/6400×1800/8400×2400）+ num10 仅 size0 +0.02 + **RandomizeTreeStyle/RandomizeCaveBackgrounds 三尺寸分支**（真 exe :8082/:8157：中=treeX/caveBackX 2 锚+3 样式、大=3 锚+4 样式+各自 retry 环；treeX 取整值 4200:[1050,3150]、6400:[1076,2136]/[2820,3880]、8400:[840,2520]/[2520,4200]/[4200,5880]）→ **中 2222=(493,661)、中 9293480=(493,811)、大 2222=(649,883) 三锚点全部与原版精确相等**（中尺寸两 seed ground 同=493=1800×0.26 触顶）。⚠️ 尺寸分支落地后 checkpoint 双种子 69 绿/32+红=**Tier B 会话正在 oracle 里转录 Dungeon（dungeonL/E/PD/Pi 新检查点）+ Dungeon 代理在改 JS**——双侧移动靶，金标统一再生须等两条线收口后做（terrain-ok 级验证不受影响已完备）。JS 侧 WorldGen.ts 尚未接 size 参数（多尺寸 JS↔oracle 对账是后续批次）。
441	
442	**★ 内容区清点+规格（2026-08-16 代理交付，docs/worldgen/specs/）**：71 pass 清点=65 已实现位置对/3 位置偏差/**2 完全缺失（#68 UndergroundJungleTrees cs:17952 每格 Next(10) 门、#70 QuickCleanup cs:17987 五子段常态全跑）**/1 常态跳过正当（SpawnStarterNPCs=十周年门）；3 位置偏差=**OceanCaves 与引力沙对调**（#36/#37，引力沙会作用于已被海洞削过的剖面）、**Piles 提前 4 位**（应在 Traps#76 后）、SettleLiquidsPart2 外移（既有备案）；自造块 3 处备案（runSurfaceDecorPass 与 #86/87/89 重叠、vanillaBiomes 丛林表面泥化补偿——终态与原版不同）；12 结构 pass（#36-47）掷骰规格全提取（R 编号+拒绝环结构，GravitatingSandCleanup/Shimmer/Pyramids/Altars 三层拒绝/Temple 房间链/…）；大量"看似缺失"段实为秘密种子门内（8 段实证表）；WorldGen.ts:99 注释过时（绿洲消费段已实现）。
443	
444	**★ CCCC 批 #101 MicroBiomes（2026-08-18）**：43k 首差不在薄冰/营地——在段首 **DeadMansChest 掷流**：JS 死箱候选 12 vs golden 11，拒因 (1129,537) 遭 **countWires(±20)=29 幻影 wire 带**（s30→s31 写入=JS #76 Traps 上游债）→ 其后薄冰/营地/矿轨/桃花心木/岩浆陷阱全段掷流错位（ThinIce 本身无罪）；剔带后仍差 20 掷=3 处幻影窗嫌疑+JS 宝箱 sink 缺箱（#58/#59/#62/#76 债经 wire/箱注册表渗入；★#101 是尾段唯一 countWires 消费者，WWW rig 对金标缺失 wire 通道不隔离）。修 MicroBiomesPass 8 项（countTiles SolidTile 语义/营地 Gen1 链序 Offset(0,-2)+OnlyTiles(53) 整链门=露营地偏差本体/ClearTile 五处漏 slope+half+致动复位/矿爆三连/三套实心谓词分型/PlaceTile(141) 真门/lavaTrap 生成期实心门/IsAContainer sheet 集）。rig T 43348→40285（残余=上游输入债）；移交 EEEE 幻影 wire 带 (1122-1124,517-541)+3 窗、DDDD 缺箱+幻影候选。上游归位后复验口径=strip 幻影 wire+候选组数 34（pad=20）→八通道应零。
445	
446	**★ DDDDD 批湖体清零（2026-08-19）：m 链 #49 L=11707→0，m/s 链首差推到 #58**。双根因：①主=**LiquidBuffer 回灌双重错位**（Liquid.cs:1134-1148+LiquidBuffer.cs:12-29）：回灌量=numLiquid（当前活动数）非空余量；DelBuffer(0)=**swap-remove 尾补头**非 FIFO 环形；弹出时序在 AddWater 后。★触发条件：中世界 r0 唤醒链把活动表顶到 **24999 帽，缓冲器首次介入**（maxBuf=1563/70 分片周期）——小世界永不触帽=三条小链 #49 长绿唯中世界翻车的结构性原因；11707 差=475 条湖面薄膜带（同形状唯圆整漂移向不同=全局调度差指纹）。②TileFrameImportant 派发缺 **165/91**（蛛网水死 CheckStalactite 组拆/CheckBanner 组拆，cs:39022-39189/86442）。附带：#49 头 oceanDepths 归水扫（cs:16222 唯 #49 有）补齐；**m/s 链 #53 旧半砖债整段消失**（全系薄膜液体差下游）。遗留：m/s 新首差 #58 Statues（165/105/187 族=放置期 CheckStalactite 同族）=GGGGG 批。
447	
448	**★ CCCCC 批 Place2x2 锚+Check2x2 派发（2026-08-19）**：两件移交诊断均部分错位实证重定罪：①411 起爆器真根因≠findDown——PlaceTile(411)→**Place2x2 是右下锚**（cs:51431 `x--;y--;` 后写 (x-1..x)×(y-1..y)）+双门（四格空置门+地面门 nactive&&(SolidTile2||tileTable)）门败**静默整写放弃**（cs:73-75 不接返回值保护图照跑）；JS 左上锚无条件写=低一格右一列（vanilla (861,735) 本就未落块——AAAAA"轨道穿杀"系误读，JS 的是幽灵块）。②3 格 18,18=DeadMansChest 巨石同右下锚 (+1,+1) 偏移（引擎 case 138 派发确缺同补，411 必须同补：轨道巷杀九宫 vanilla 同派发 Check2x2(411)，不补缺 20 尘掷）。修=place2x2Direct 字面镜像+check2x2Sweep+case 138/411 派发+frameSparse 跳过表 +138/411（★不加则与 184 杀级联互喂**无限递归**实爆）。#101 A/T 19936/21843→8272/9157；巨石 284/284 同位同型；411 全图 60 格逐位同；.fr 76/76=0 超额达标。遗留：**TrackPass 轨道路径残差（314 差 6512→2397+golden 独有对角段，掷流新首差 166921）=FFFFF 批**。
449	
450	**★ BBBBB 批新链 #32 清零（2026-08-19）：双链 0 差，四链首差 s22222/m→#49、9293480→#63、12345→#54**。两根因：①s22222=入口上方 0 号房在 worldSurface 上→dgBasicChests **水覆写箱**（num2<ws+50→surface 支），JS `surf=…&&false` 恒假走金箱支→掷数差连坐 G/I/T/F/Pa/Ba 全段（修=flag0 传参接真支门，surface 支 15 组掷序本就齐）；②m20260811=Legacy 入口 0.6 框清墙上缘刀口：反编译 double 319−10×0.6000000238418579=312.99999976→312 而二进制 **313**（fl(10×0.6f)=6.0 半 ulp round-half-even 可复现，与金字塔案同族的二进制-反编译刀口）——修=四界 Math.fround。★中途自纠两则教训：327=金钥匙零前缀零掷（曾误登 'acc' 反致 1481 差）；Prefix 重掷链不存在（awk 行偏移误读——曾把 12345 #32 爆到 1688，**全量回归检查抓出后回退**——改后必须跑全链回归）。**m 链 #49 湖体 L=11707=YYYY 级联归因证伪：#32 清零后原样→沉降/液体模拟在 #48 输入全绿下的独立自差（DDDDD 液体域）**。遗留：oracle 镜像债（flag0/surface+0.6f 界+中世界支须先修）；Legacy 入口其余 0.6f/0.55f 界仍 double 转录（撞上再 float 化）。
451	
452	**★ WWWW 批放大器脊柱清偿（2026-08-19）：#58/#59 根 193→0，9293480 首差 #59→#63**。四修（golden/x86 定罪）：①主根=**房填陷阱雕像**：vanilla HouseBuilder.cs:483-491 在雕像 PlaceTile **失败时也**调 PlaceStatueTrap（与 Statues 流 cs:17045 语义**相反**勿混淆）——JS 门在成功内→4 房丢陷阱+45 线格→红线扫描级联（golden 几何 (3201,366) 雕像被 62 挡 vanilla 仍放陷阱定罪）；②AgeRoom 钟乳石沙漠/花岗/大理石列 378/432/486 从未放（冰限本地副本）→135 T168，换 ShimmerPass 全量 1:1；③SetTileKeepWall=Clear(~(Wiring|Actuator)) 梁写语义；④frameKillSweep 跨对象帧杀级联引擎（roll-free 实证，老化原始 SetTile 不触发——(2634,479) 破碎仙人掌保留为证）。方法论：#59 入口注入 golden fr/wire/chest 残差不动→写侧自因定罪。放大器验证：#71 罐零自因（原版本性）；#89 藤 6 格自差修零（putVine 半清除 ClearSlope 双清+蜂巢凹室 CheckVines 级联）。#54 两幽灵半砖门修但一格需 vanilla roll weave（YYYY 级阻塞备案）；湖体=m 链 #32 债（BBBBB 域）。矩阵抽测 m2222 typ-11.6%/wal-44.7%/liq-20%（装饰漂塌缩中）。12345 #59 128→12（残 12 待下轮归因）。
453	
454	**★ AAAAA 批矿轨帧链（2026-08-19）**：TrackGenerator 三链+XXXX 未定罪的第四链（cs:111-114 KillTile 尘掷+尾九宫）落进 TrackPass.ts：killTileLane 复刻 RRRR 尘掷全表+genSquareTileFrame 级联；压板支 PlaceTile(314) ClearEverything 全清语义；cs:150-160 逐列五连 wuTileFrame 字面镜像；退役旧"铺完统一 frameTrack"三循环。掷流 165353→165546（+193 逐条吻合）；帧位金标 .fr 48/50 逐位同。**残差移交**：①上游矿爆段 findDown 首实心低一行→411 起爆器 2×2 比 van 低一格→findPath 零掷重路由首曝掷流（MicroBiomesPass 矿爆段=CCCCC）；②引擎 case 138 巨石 Check2x2 缺（3 格 18,18vs0,0，FinalCleanupPass=CCCCC）。工具资产：_wwwrep span d/n 通道+rng.vanilla 'n' 录制（SW_WWW_SPAN_DN=0 可关）。
455	
456	**★ ZZZZ 批金字塔奇案定谳+协调者施加（2026-08-19）**：走廊 26vs24 **非** Next(20,30) 二进制/反编译差——真凶=WorldGen.Pyramid 主体刷墙段（cs:27870-27888）每写一墙 SquareWallFrame→Framing.WallFrame(resetFrame:true)，wallLargeFrames[34]==0 时**每墙 1×Next(0,3)**（s22222 共 11025 掷，JS 只镜像写墙漏掷）→num8 后骰序位移（num12 取流位 #6=23 而非 #11029=25）。证据四方一致：IL 直读（RunPass 每 pass 重播⇒骰是 pass 局部）/金标几何拟合/K-约束解（六骰 (1,5,25,16,8,25) 命中 K=11025=画布墙写数）/双参织入实测（zzzz-span.txt，pc.txt 哈希链全等证零扰）。★方法论：**跨方法副作用掷**（SquareWallFrame 在写墙调用点）是"反编译看起来直给"的暗掷——DesertPass.wallFrameDraw 同语义先例。修复=StructuresPass.ts 刷墙段写墙后补 `rng.int(0,2)` 一行（并行禁区→协调者施加）；s22222 #40/#46 3269+35639 级→**176/178/0**（残=纯 #32 地牢 banner 债基线 (522,226)）；9293480 A/B 逐槽全等（无金字塔零影响）；#105 终态 -28~-70%。
457	
458	**★ XXXX 批微残终清（2026-08-19）**：①#101 营地帧链五修+三连环真 bug：矿爆点 Y 域用 (int)GenVars.rockLayer（TerrainPass 游走值 523.808）≠ Main.rockLevel(571) 整体偏 48 格；**★引擎级：Tile.actuator()(bit 0x800)≠Tile.inActive()(bit 0x40) 是两个独立旗标**——SolidTile 族读 !inActive()（生成期无置位点恒真），JS 曾把致动位当 inActive → 致动石格误判非实心（探针实证 (2430,920) inact=False wire=True）；巨石壳致动门 tile2.wire() 只查红线（曾 &15 任意线）；薄冰斑 ThinIceBiome.cs:32 是 AddStructure 非保护登记（曾误挡矿爆点）。残 1%=**TrackGenerator.cs:136/151/158 TileFrame(frameNeighbors:true) 帧链（TrackPass 域）**移交。②剑冢 HashSet 豁免撤销：.NET Add-only 枚举≡插入序、Subtract-后-无-Add≡幸存者插入序≡JS Set——UUUU"34.5k 剑冢掷"归因证伪（真源=五修+矿轨）。③#63 preferSmall IL 证不可达（spiders=true 走 +0063 ret，小支全在 +151 后；UUUU"+0063 单格 frameY=54"误读，其试接失败正因建模了永不执行支）；残 2 格=波内装饰时序微差证据级备案。④地牢帧全清：压板 135 样式轴在 **frameY**（曾 fx/fy 对调）+Place2xX style*36+DG_ITEM_STYLE（1410=style48）；9293480 全管线重生成 18+8 格逐位=金标。
459	
460	**★ YYYY 批四链全景（2026-08-19）：mile8 永久扩到 105/106 槽+六族槽级归因**。两新链 sanity 双 PASS（g-s22222 5G/g-m20260811 11G，槽105 vs wld 全零差）。四链全景 /tmp/panorama-yyyy.tsv：9293480/12345 的 0..53 复核全绿；22222/m 0..31 全绿（第三种子验猩红支）；首差 9293480=#59、12345=#54(Hf=1)、22222/m=#32。**六族归因**：装饰位漂 4.3M=通用「采样-验证-重试」放大器链（#58/#59 百格级根→#64/65/67 墙→#71 罐+18-42k→#82/85→#89 藤+22-74k→#97→#101/103）；湖体±255=#49 沉降 2000× 放大（m 链输入 A0/T2/W4→L=11707）；蜘蛛巢=#63 级联（m +97k）；墙层系=#67 Cave_Walls；**s22222 神庙=#46 金字塔级联**（神庙 pass 无债：走廊直段 vanilla 26 带 vs JS 24——★golden 二进制 vs 三方一致反编译行为差：同流 Next(20,30)=23 而二进制表现 25，δ 扫描+全掩膜不可复现；swtrace 只钩单参 Next 双参骰不可见，/tmp/yy-tr/swtrace22222.log 留档；四链唯 s22222 建金字塔=该路径首验）。
461	
462	**★ VVVV 批矩阵终局预演（2026-08-19，39 世界只读）**：s25 带 typ 3.433/wal 1.771/liq 0.349（较 8/17 -27.6%/-57.3%/-42.6%）；s12345 **2.508/0.303**（地牢盒 wal -94%）；总残余 20.9M 格（typ 3.747%）。树干 **101.2% 过收敛**（XXX 时 m 带缺 40-95/世界）；瓦罐噪声位；宝箱 ≤2/世界。**终局预判：UUUU 交付后矩阵基本不动——到不了零差**。★新面孔清单：①**蜘蛛巢位移**（非 12345 种子 wal62 46-127k/世界，#63 流全同只在 12345 成立）；②**装饰位漂族**（165 洞穴装饰 2.15M+62 丛林藤 1.49M+638 灰烬藤 250k+罐 208k+树 127k，全为对称位漂=计数等坐标移）；③湖体 ±255 液体位漂；④背景墙层系 196-215；⑤spawnY 13/39 ±1-2（陈债）；⑥**s22222 神庙整体错位 +460x/+123y ~100k 格**（其余种子神庙盒逐位同）。共性=种子特异分支债在矩阵种子上触发（两链种子不触发）→YYYY 多种子链扩展转首差定位。
463	
464	**★ UUUU 批神庙/重建段/波前终清（2026-08-19）**：①Temple 4v5+帧债**归零**——旧 mayanTrap 是行号错配近似（标 cs:2945 实为 cs:8314+），1:1 重写（落点门 232 尖刺/10 门曾错查 226 砖/垂直扫描限 worldSurface 曾错用 rockLevel/工作台 Place2x1 左锚曾居中/壁挂 3×3 锚在采样点曾偏 (1,1)）；sink 177=177 同序。②Traps 248 帧债**无罪**（金标 .fr 差 AtTraps=0：137 族 111=神庙遗传已修、135 族 8=地牢遗传在案）。③#99 ⑦重建段**归零**（cs:21484-21741 四族+原版右列读左列 typo 639 保真；★span-duel 翻案：**KillTile 尘掷 type 24/27 每杀 10×Next(2)**——SSSS"水系死亡族零掷"结论又错一次，尘掷表必须逐 type 实测）；2,059,985 掷位全同。④TileFrame(resetFrame:true) 溯源：TTTT cs:82448 理论错（TileFrameCosmetic 有 !generatingWorld 门），真源=TileFrameImportant case 178/184/72；ActuallyPlace* 族+ThinIce+红木 SetFrames/PlaceWall（含 wallFrame Next(0,3)）镜像；#101 流差 164→20196（残 34.5k=剑圣 HashSet 枚举存档+营地帧镜像待批）。⑤#63 波前**流全同**（织 Spider 全访日志；两真根因在 BuriedChestsPass：**16 个战利品掷写成 int(offset,max) 而非 Next(K)+offset——同宽异值仅总数对拍不可见，必须 span 类型序列对拍**；地狱额外件缺 flag8 门）；48/59→**2 格**（preferSmall 钟乳石支未建模，接线 2→1130 已回退存档）。IL 双陷阱存档：num11 style 块在 errorWorld 分支内/战利品 tier2 门 y<rockLayer 被反编译器折进 remix 分支（JS 原正确）。sink 终态 180/182（2 regOnly=地狱梳妆台——并行会话 05:52 在改 HellFortPass；4 jsOnly=#59 上游）。
465	
466	**★ TTTT 批箱族终清（2026-08-18）+金标第三通道基建**。★基建：/tmp/tttt-app 织入产金标**帧(.fr)/线(.wire)/箱注册表(.chest.tsv 含物品位)/span 流**（自证 848/848 逐字节同）；三织入坑：ProbeLib 须含 HsProbe/**Cecil InsertBefore 每条须重取 Instructions[0]**（缓存锚→Call 排栈空前→Pass 静默冻结+服务器无限重生成）/wld≠生成期注册表。①"sink 179vs350"基数证伪（SSSS 比错 wld=大世界产物；真 slot100=180→终段重建 181）；Water Chests 趟2 y 重掷域 [⌊ws⌋,UL) 非 [50,UL)（cs:17440-45）→**#62 槽 104→0**；梳妆台注册接线（HellFort place3x2HF 镜像 Place3x2(88) CreateChest 先烧槽）→sink 176/180 对齐（残=Temple 族 4v5 移交）；#101 逻辑 1:1 定谳（27=27/掷序 5 轮同，38k 残=输入态债）；新定位 **TileFrame(resetFrame:true) 每调 1×Next(0,3)（cs:82448）未镜像**。②#58 雕像帧 StatuePass 无罪：债属 Traps 248+Temple 113+Dungeon 3（禁区报告）；rig 槽 51/53 注入金标帧线（SW_WWW_GF=0 可关）→**#99 259→86**。③#99 ⑦重建段输入已备（chest.tsv slot98 物品位真值）实现未做（cs:21484-21741 四族）。④#63 波前：wave 级证据（JS wave65 才访/wave63 拷贝被 y≥h-200-Next(5) 门吞）机制收窄为隐形掷-格分配位移，需织 Spider 全访日志（配方在档）。
467	
468	**★ SSSS 批尾段终清（2026-08-18）**：#93 10/11→**0/0**（placeExposed 双尾帧 genSquareTileFrame×2 镜像 cs:59724+60281/rig 帧回填/前置清 cs:59500）；#77 两仲裁→**0/0**——★**坐标重载 SolidTile2(int,int)（cs:70497）带平台 topSlope 豁免**（`Platforms&&(half||topSlope)||slope==0`）Tile 重载（cs:70178）无此支（RRRR 金标编码疑不成立）；2520 定谳（3669=七段 float32 界算术和含 2520，IL 正确，2519 是平台 bug 补偿假象）；#63 蜘蛛洞 1203/1331→**48/59（-96%）**（placeTightWebs 尾部 CheckStalactite 泥土支撑整对杀=T0>165×527 主根因等五修；残=(474,996) 波前分区单点时序差，`__swSpiderVisit` 探针含 waveN 留存）；#99=输入债定罪（首分叉 (605,782) **A137 雕像帧边界缺失**→⑦邻杀方向反→级联；真缺口 ~14 格=⑦重建段需 chest 物品位输入备案）；#101 复验未达零：**宝箱 sink 179 vs golden 350 锚**→DeadMans 候选流差全线级联=箱族上游债（TTTT 批主靶）。★方法论：genRand 内态 FNV **移位不变**（注入腐蚀实证）——流对齐必须 span 序+SF/SL 逐调用坐标序。
469	
470	**★ RRRR 批帧杀引擎（2026-08-18）：#77 952/982→2/2（99.8%）**。FinalCleanupPass 扩为通用帧杀引擎：实心谓词全改 genSolidType（229 在 Piles 期非实心→罐失撑击杀）/Check3x2 补金币掉落掷（cs:49726-49836 三档）+5×5 TileFrame 尾扫+187→186 raw/新族 CheckDoorClosed·Open（cs:87176/87082 尾无条件 destroyObject=false）·Check1x1/PilesPass 统一接 genSquareTileFrame+PlaceTile 双尾帧（cs:60026 无条件+cs:60279 成功=两轮）。★**尘掷真相：OOOO 移交的"尘掷表"实为击杀普查数——罐/165/485/10门/135/185/186/187 尘掷全零；唯祭坛 26 且 frameX<54 →10×Next(2)/格**（回填 style9 会吞祭坛尘掷，26 族须 style0）。连带三真 bug：平台 tileSolid 补真 {19,427,435-439}/⑤段迭代上界 **2519**（IL 读 2520 掷值解码证伪——解码法又一案）/尘掷门 frameX<54。残 2 格=顶坡平台 19 上 1x1 小堆（vanilla 放置成功与自身 SolidTile2 slope==0 门矛盾，疑金标 slope 通道编码/运行期坡变，未解备案）。#93 残 10/11 引擎已就绪只差 GemPasses placeExposed 邻格清循环换 genSquareTileFrame 一行（冻结未动移交）。#99/#105 未塌缩在案；#63 Spider_Caves 1203/1331 从未派发=SSSS 批。探针基座 tools/www-framebackfill.ts（金标无帧通道按族信任回填）。冒烟 22.4s（引擎+5s）。
471	
472	**★ OOOO 批残量深挖（2026-08-18）：#64/#87/#92 八通道全清，#77 -23% 残差定罪移交帧杀引擎**。⓪前置解锁：IIII 探针雷=金标腐化而纯净启动掷猩红——**探针启动必须 SW_EVIL=0**（/tmp/oooo-app 基建保留）。#64：placeExposed 缺 PlaceTile(178) 成功尾帧第三次 Next(3) 幽灵掷（band 内 no-write 只移流；13×roll3+10=IIII 的 d=+23 精确闭环）+validAnchor 实心源改生成期表。#87 三合一：TryGrowingTreeByType(5)=真长蘑菇树并耗掷（复用 TreePass.growTree）/PlaceTile case71 香蒲支全缺（cs:59675-703=T519 族主根因）/前置 Clear(Slope)+成功尾帧+TileFrame 头非活跃清坡。#77：placePile3x2 形参内部 id vs type===186/187 sheet 比较**恒假=击杀链整段死代码**/KillTile 实清 type（cs:63965 翻案 IIII 误读）/Check3x2 尾 5×5 TileFrame 扫连杀邻堆/前置清锚格。**残 952=邻近装饰帧杀引擎缺**（KillTile 探针普查尘掷表：28罐×12/165×10/485×3/10×3；前 672,737 掷全同差在世界态）——与 #93 残 10/11 同债源=RRRR 帧杀引擎专项。#93 连带 518→10（rig 假差 281→10 修正）。冒烟 16.8s；mile8 双种子绿。
473	
474	**★ QQQQ 批双链全绿里程碑（2026-08-18）：12345 #49 Lt=1 清零——双链 0-53 全绿达成**。根因：vanilla **LavaCheck=沙漠 blast 前导+LiquidCheck(x,y,1)**（Liquid.cs:1454-1469），但生成收尾全图检查（WorldGen.cs:22639-22650）对湿格**直调 LiquidCheck 不经 LavaCheck 包装无 blast**；JS finalGenMergeCheck 岩浆分派走了 lavaCheck（含 blast）→把密闭岩浆斜梯当 blast 源→(1979,658) 首个覆盖密闭水袋→水转岩浆（恰 1 格显差）。修=LiquidSim.ts lavaCheck 加 desertBlast 参（三原版调用点默认 true 不变）+finalGenMergeCheck 传 false（Honey/Shimmer 分派本就无前导唯岩浆错向）；VVV 两语义零触碰。验证：12345 链 0-53 全绿+9293480 零回退+液体 60/60+冻结 A/B 哈希不变+worldgen 真回归零。取证方法论：金标只读考古（密闭性/可达性逐格排除）零 IL 织入。
475	
476	**★ PPPP 批杂项收尾（2026-08-18）：12345 链 0-48+50-53 全绿（仅剩 #49 Lt=1）**。①**六祭坛格清零+#53 塌缩**（Sl 2278→0）：根因=vanilla 蜂巢蜜池雕刻 ClearTile(frameNeighbors:true)（HoneyPatchBiome.cs:43）触祭坛底格→TileFrame→Check3x2(26) 支撑失→KillTile×6（type=0 水保留=金标签名）；修=FinalCleanupPass 导出 genFrameNeighbors/genSquareTileFrame（exact-roll-safe）接进 HiveSpiderPass 四蜜池步+FOUT。②#58 雕像 7Hf 清零（PlaceTile cs:59503 else-if **active 锚**+ResetsHalfBrickPlacementAttempt 默认 true→halfBrick(false)+帧清）。③#76 残 8 清零三根因：★EEEE"巨石免杀"豁免是错的——vanilla 杀巨石，存活靠 KillTile 尾 Check2x2 级联（序=B 后 A 同）；单格短钟乳石漏杀→killTileWhole 165 邻查路由 checkStalactite；★沙坑壳侧清坡是**原版 bug：列 i-num5-2/-1/+1/+2 全在左**（cs:35721）勿对称化。④#105 残 258→W1：移植 FillWallHoles 族（cs:9846-10013 表面带 BFS≥150）；"204 真缺口"证伪=frameSparse 探针伪象（生产杀 198/204 正确）。⑤house#111 193=**陈旧捕获伪象**（生产有陷阱红线且正确拒屋；/tmp/www-b/s17 旧捕获缺线——★重放复用前必须重捕 s17+；DDDD 四级织入取消）。⑥s33333 Tower 复扫零回归（致动 6/6 同）。★唯一残：**12345 #49 Lt=1 (1982,661)**——JS 沉降把封闭水袋转岩浆 vanilla 水恒静（金标 48/49 该处字节同；嫌疑 LiquidSim 对角转移+类型合并）。
477	
478	**★ NNNN 批 oracle Dome 镜像（2026-08-18，终局点火条件③完成）**：★事实修正：**1511931452 是 Tower 种子非 Dome**（HHHH 误记；其 40/78 回落真因=MMMM 四修在 Tower/Dome 共用下游段而 oracle 未同步）；Dome 实证种子=12345（kind=1）。镜像 caves-oracle.cs +~500 行：FFFF Dome 体（DgDomeEntrance 全量+Legacy 近似体 oracle 侧同步退役）+MMMM 四修（罐门 !inAct+JVS/水书 Next(50)/inAct 通道=wire bit5+柱 inact 参+DgSolid !inAct/entNoFeat 三门）+树族上移顶层（C# 三陷阱：CS0165 调用点赋值/块内函数不可见/CS0136）。验证：seed2 40/78→**71/78**（首红 dungeonP 消除）、seed1 逐字节全等、12345 dungeonE 网格逐位零差（修掉 i+n3+21 笔误致右楔柱 +42）；检查点保持 75。残余 5 红（piles/trees/settle2/cactus/microbiomes）=OOOO/PPPP 在途 JS 漂移带，交付后预期 76/78。终局点火条件：①HHHH ②HHHH ③NNNN ✅——只剩尾段两批交付+漂移带归位。
479	
480	**★ IIII 批小债清扫（2026-08-18）**：#64 Gem_Caves 359/1009/2560W→296/931/2424W（Spread.Gem hashSet.Add 幂等去重 cs:3605/SolidTile 换生成期表+190·225·226·481-483 族/InWorld x==1 边界）；#77 Piles 2755→1227（★Place3x2 **中心几何** x-1..x+1 cs:60018→52097 曾左对齐整列右移/SolidTile2+InvalidTileForPiles 锚/样式族门+击杀链/⑦段水沙方向反）；#99 Tile_Cleanup 1528/199Sl→257/0Sl（SaveSlopes=TileID 静态一次拷贝 cs:425-429 曾叠 gen-solid/pristine tileSolid 补平台集——残坡 154 格全是 t19 平台/⑦段 137·162 击杀族）。树列 150→**183**/219（84%）；trees 登记表幽灵 0（★修剪须改 gs.genTrees——finalize 整表覆写会冲掉 world.trees 修剪）。**新基建**：Cecil 织入 GemProbe（站点级 genRand FNV+计数），/tmp/iiii-app+/tmp/iiii-patch；★坑：探针 exe 世界在槽 65-70 与金标有局域差（金标 76 有罐探针无）——槽 54-105 金标从未对过新鲜无补丁运行，取逐调用真值前须排雷。未清偿移交：#64 残 site#1 起 +23 样本/站机制未明（Gemmable 内联无钩点）；#77 残 1270 表面段流分位；#87 697/1688 在 SurfaceDecorPasses（时为禁区 audit-only，61↔69 互换 434 对）；#105 残 258/house#111 193/#58 7Hf/#76 8/Tower s33333 复扫/12345 六祭坛格未动在案。
481	
482	**★ MMMM 批 Dome 内构清零（2026-08-18）：12345 链 #32 八通道全零、#53 塌缩 93%**。三根因链（全 DungeonPass.ts）：①主=**瓦罐支撑门**：dgDungeonPot 用碰撞语义 genSolidType（平台=false）而 vanilla PlacePot（cs:54082，门 :54099-54102）=nactive()+Main.tileSolid（平台 19 生成期=true）——Dome 平台罐全败→每只成功罐漏掷 1 颗 Next(3)→旗/挂毯/钟/画全错位；Legacy 房无罐路径→9293480 绿掩盖（★罐门与雕像底座同族：GenSolid 口径差第三案）；②水书掷位 `d.nowb===false`→`!==true`（缺省字段 Dome 下对平台无 NoWaterbolt 整族漏掷 Next(50)，#6 平台起分叉）；③致动柱 inActive 整链（dgPillarStrip/dgPillar 加 inact 参，DungeonPillar.cs:151-154/200-203 ClearTile 先清 bit5 平滑后置位；solidOrSlopedD/dgSolid 补 !inActive WG:70046/70155）→Ia 234→0+W 776→0。④entNoFeat 入口盒特性门（DomeDungeonEntrance.cs:31-38 拒书架/画/尖刺）。验证：#33-46 连带绿；#53 Sl 31,609→2,278（余项=祭坛上游级联，与 LLLL 反事实互证）；9293480 主链全绿。遗留：Tower 支同修未验（双链无 Tower 种子，矩阵复扫 s33333）；#47-52 残 6 祭坛格+Lt 1。
483	
484	**★ HHHH 批 oracle 尾段补录（2026-08-18）：_oraclesync 66→76/78 双种子，再生硬前置清零**。三条语义主轴（oracle +1,342 行镜像）：①**GenSolid 三口径混用**（JS genSolidType/vanGenSolidType/TILE_DEFS 静态三表与 oracle SOLID 差 {19,239,380,427,435-439} 九类 sheet）——oracle 增 JGS/JVS 双谓词逐 pass 对号（典型：statues 平台 19 底座曾拒放→游标错位 1→样式错排）；②**t!=0 内部/原版空格语义差**（settle2：JS 内部 0=EMPTY 活性格恒过门 vs oracle vanilla 0=泥土——活性泥土漏拒入列+漏清液 129 格+岩浆烧除缺 !active() 门 153 格幽灵复活）；③CCCC 8 项未镜像（缺项曾致 mahogany 树整体位移 36k 格）。FinalCleanup 扫掷+ShimmerCleanUp 镜像 ~780 行：金标 104 基座九通道 504 万格与 JS 零差+B5 全锚命中（苔藓 10697/苔藓块 1358/⑭→668）。彩排 caves-checkpoint 9293480 全绿 120 ✓。**移交**：①oracle dungeonE+ 段缺 Dome 镜像（FFFF 落地后 seed2=1511931452 Dome 种子回落 40/78 首红 dungeonP——MMMM 稳定后镜像 dgDomeEntrance=NNNN 批）；②WWW 尾段检查点合入后全量再生。runbook 附录 HHHH 节。
485	
486	**★ LLLL 批 12345 #53 SmoothWorld 自差清零（2026-08-18）**：双根因（HalfBrickPass.ts）：①主=KillTile 尾 TileFrameImportant 缺 **CheckSuper 派发**（vanilla cs:86437-40 case 376/443/444/485；JS 只派发巨石 Check2x2）——实锤 (1856,476) 485 蚁狮窝 2×2 伴被大理岩顶替→vanilla 整组杀+残凸砸半=**两枚零掷动作**：流恒对齐仅格态漂移→掷数对拍在 9293480（足迹恰零）掩蔽至今，12345 地下沙漠蚁狮构型首触；②SolidTile 族缺 **!inActive() 致动腿**（cs:70170/70052/70228 原文即有）——穹顶 234 格致动柱（#32 债）→穹壳 6 格 slope 错写。修后 12345 反事实八通道全 0、动作序列 89,683 条全等、掷数 5,098,924；9293480 主链 0-53 全绿。★方法论金句：**零掷但非零写的级联掷数对拍不可见，必须动作序列对拍**（swtrace rig：/tmp/llll/swtrace12345.log 128MB 末 RD==pc.txt）。管线 #53 残余≈6.1k=穹顶输入债（MMMM 清 #32 后塌缩）。376/443/444 非 #53 在场备案；事故披露：rm 误删 U 批 swtrace 存档已四重验证确定性再生。
487	
488	**★ EEEE 批 #76 Traps（2026-08-18）：自因 4915→8 格+自造 runSurfaceDecorPass 前置段退役**。途中两次死循环事故（ay++ 应 ay--；acceptance 恒 0 打满 1150/20000 拒绝上限的"合法挂死"）用户实机踩中、协调者两轮拆弹（杀僵尸进程解 agent 自锁+隔离重放定罪）；最终修复 19:08 落地、协调者代验：槽76 重放 520ms 完成、全量生成 12.9s 恢复。★教训：①agent 改生成代码时用户可能正在生成——**拒绝采样移植必须保住护栏上限+落一次全量生成冒烟再继续**；②agent 被自己挂死的长跑堵住时杀其进程即可解锁。残余 8 格=(2022,581) 巨石族在案=小债波。
489	
490	**★ FFFF 批 Dome 入口体全量移植（2026-08-18）：s12345 地牢盒 typ 13433→1433（-89.3%）/wal 16400→1310（-92%）**。DomeDungeonEntrance.cs:40-441 全量 1:1（~330 行替换 Legacy 近似体）：入口私有流 UnifiedRandom(entSeed)（flag2=Next(4) 树饰先掷 Dome 独有）；Slime 形状族五连（穹壳 r40+UpdateBounds 扩界链/穹内墙 r38/土丘/草皮 OnlyTiles+IsTouchingAir/内腔 r35）；★窗带基 num3=35 非 Tower num4 族/门仅 dungeon 侧单门/**阶梯正常种子=真且单侧**（SpecialSeedFeatures.cs:41-51）/Circle(20)@±num4；DPlat.nowb 参数位 Next(50)+waterbolt 帧门照抄原版 Main.tile[placeY,placeY] 手滑。指纹全清：墙 94↔95 34,699→**0**、门 7>0×46→**0**、头锚 (3413,190) 全等。里程碑 0-53 全绿。遗留：oracle 侧 Dome 未同步（dungeonE+ 段对 Dome 种子失效→HHHH 域）；盒内残余=对齐种子同族他 pass 在途债；祭坛 35 vs 36 维持上游自愈。
491	
492	**★ GGGG 批无根树定源修复（2026-08-18）**：根因=Flowers pass 击杀门（cs:20683-20692 type==5 带宽门）vanilla 确实允许杀树干底格，但 KillTile 尾 SquareTileFrame→TileFrameImportant case 5（cs:86619）→**CheckTree（cs:54598-54808）整树坍塌级联**（同游戏内砍树）——vanilla 净效果=整树消失+原位放花；JS 只杀底格无级联→浮空树站花草上。修=SurfaceDecorPasses 加 killTileTree+frameCellTree+checkTreeAt 全规则链（R1-R4+尾传播/cfx/cfy -1 虚拟帧），级联零 genRand。验证 bad=0、干列 159→150（9 棵该塌的塌了）、地面 hist 全实心族对齐 x86；槽 0-53 全绿。★旧裁决 tree-bottom-grass-overwrite.md"原版留断树"结论错误（漏 KillTile 尾级联）已重写。树列错位全清单（JS 150 vs x86 219）已录 GGGG 章供终局复验（尾段债级联）。途中自引入两 bug 教训：级联计数 num4 漏 +1 会静默死、冠格修剪须查冠格非基座格。
493	
494	**★ DDDD 批 #59 洞穴屋清偿（2026-08-18）：6081A/7876T/4806W→193A/193T/0W（-97.5%）**。三根因全 x86 运行时定罪：①**KillTile 尘粒耗掷**（主根因）：洞穴屋蚀变③ ClearTile(frameNeighbors)→四邻 TileFrame→Check* 击杀失撑家具→每格 KillTile_GetTileDustAmount=10（cs:66661）×MakeTileDust 每调 +1 掷（house(1867,543) 吊灯 9 格×10=90 掷，JS 已正确杀但零耗掷）；★尘掷表必须实测（吊灯34=10掷/格，小堆/骨堆/桌族=0）——反编译 MakeTileDust num 表控制流两例皆反不可信。②placeBuriedChest 坠落谓词=SolidTile（cs:70155 含 !tileSolidTop）非 solidTileHB——vanilla 宝箱穿楼梯平台下落。③门链三错：分支 A 本语境必败却照放门+耗掷（幻影门主源）/分支 B mount+地板门整缺/门帧三行各独立 Next(3) 曾弃值全写 0。**方法论**：对已织 ChestProbe 的 server.exe 再织三级探针（TileFrame/KillTile/MakeTileDust 头），把"90 掷纯耗无事件"打到运行时真值。遗留：house#111 (3160,591) 接受分歧（残余 193 格总根，vanilla 拒/JS 收、位与流全同、差在 ±25 wire/chest 前扫态，需四级织入）=小债清扫波；尘掷表跨世界外推风险备案。#62 残差=house#111 级联非独立。
495	
496	**★ 用户报障"无根树"初查（2026-08-18，seed 12345，GGGG 批在途）**：x86 树底地面格只着实心族（2×99/60×66/199×26/70×23/147×17）从不垫植物 73/花 3；JS 有 ~23 列 73@fx/3@fx 垫底=树浮一格。树列错位（206 vs 231 列，同位同帧仅 17）=尾段上游债级联（槽 54-105 在途批），树 pass 零自因（WWW 已证）勿归因树 pass。旧裁决 tree-bottom-grass-overwrite.md"Flowers 杀树干底格"与 x86 实测矛盾，GGGG 复核中。
497	
498	**★ ZZZ 批 FinalCleanup 扫掷+ShimmerCleanUp（2026-08-18）**：vanilla 主循环每格末尾无条件 TileFrame（cs:22544）——掷族全表：**184 苔藓芽每格无条件 1×Next(3)**（cs:85916 先掷后判）+72/571/549/165 条件掷+KillTile 尾级联重访；★**ShimmerCleanUp（cs:22639）此前整缺**=⑭ 后同 pass r<120 环带杀苔藓/转苔藓块（扫盒 X±120×Y±120 曾误读 Y±90）。移植 FinalCleanupPass +890 行（TileFrame 1:1 分派全族/killTileGen 九宫级联/destroyObject 全局位）+ShimmerPass reframe 钩子。三重全等：苔藓 11321→**10697 逐格相等**（杀 624=扫 66+微光 558）、苔藓块→石 1358 全等、⑭ 位点三格全等；槽 105 八通道 2500+→**258**（残余=墙备案缺+frameSparse 跳过的读帧杀族真缺口+缺帧伪差）。★vanilla 终态真帧二次跑抓三错：SolidTile2 平台族 tileSolid=**true**（曾误杀陶罐）、485=Style2x2 帧 18/36 步（曾误杀全部松树）、185 沙地基 54-59∪73-76。苔藓放置差（14727 vs 14088）=上游位移债（机制已 1:1），⑭ 位点须 Dirt 图谱全收敛后才可重合。
499	
500	**★ AAAA 批多种子地牢复测（2026-08-18）**：post-OOO 残差降 51-65%（s111 5756→2320/m111 3374→1184/l2222 1258→619）——OOO 五修跨种子成立，残余=盒窗口罩住的他 pass 在途债非 DungeonPass 链债。**s12345=真实地牢债：根因=Dome 入口体未转录**（DungeonPass.ts:3851 XX 批备案）——头锚 (3413,190)x86 vs (3377,220)JS 为 16 世界唯一，已修 DomeDungeonEntrance 锚语义（entKind==1 时 dungeonX=posX/dungeonY=posY-30，DomeDungeonEntrance.cs:49/:430+DungeonCrawler.cs:450，零 tile 零掷）。★墙变体机器无罪铁证：s111 墙 96 马赛克 5424/5424 逐格全等——s12345 的 95>94×34,699 全是 Dome 近似体→bounds/墙 7 底图→SpreadWallDungeon 申领序下游。★dungeonI 定性反转：JS canHitLocal 与 vanilla 全同，是 **oracle DgCanHit 缺踩格终止+邻对三门**（BBBB 修复中）。遗留：Dome 体移植 ~500 行（Slime 形状族/BlockActuated 柱/Dome 门/TreeOnPillar）=FFFF 批；祭坛 moving target 维持上游级联裁决（v=36 j=36 已平）。
501	
502	**★ WWW 批尾段全量反事实裁决（2026-08-18，#54-105 共 52 槽）**。rig 三件套 tools/_wwwcap/_wwwmid/_wwwrep（SW_WWW 门控，golden 基座+跨槽 gs/帧/线/GenSolid/chests 快照重建）留续批。**裁决**：零自因 20 槽（19 原生+57/72/78 修零+69 岛屋=上游瞬态级联非自因——SSS 线索 a 结案）；**自因仍在 26 槽**：#101 MicroBiomes 43k（薄冰斑 161↔162 整体错位+露营地）＞#59 Buried_Chests 7.8k（洞穴屋门族与 #62 共根 placeBuriedChest）＞#76 Traps 4.9k（含 JS 自造 runSurfaceDecorPass 前置段）＞#64 3.6k＞#77 Piles 2.9k＞#105 2.6k（ZZZ 域）＞#87 1.7k＞#99 1.5k。**修 5 项**：①#57 LifeCrystals：生成期 tileSolid 须运行时表+★**nactive()=active&&!inActive(0x40 致动位)与 halfBrick 无关**（Tile.cs:270，全仓唯一错译点）；②#58 Statues：Place2xX 双列 SolidTile2 底座门+PlaceStatueTrap 三错（135 非 137）+PlaceTile 前奏 Clear 接线（残 2-4 座待 IL）；③#72 Hellforge：PlaceTile(77)=Style3x2 中心底锚非左对齐+AnchorValid Platforms 集 {19,427,435-439}；④#78 SpawnPoint：原版无地形清理，自造净空清理盒整段退役（第 2 例自创写入）；⑤#92/93 ExposedGems：原版两独立 GenPass 拆分+槽内重播。**underworld 仲裁=金标陈旧伪红**（vs 新鲜 oracle 四检查点全等）。37 红=陈旧冻结件+并发超时伪象。
503	
504	**★ XXX 批二轮（s12345 附产，2026-08-18）**：①祭坛 extra=2 定性=上游状态级联非逻辑债（三层静态对账全绿；JS 独有坛底行冰 161 在 vanilla 终态同样合格→掷流被更早候选接受翻转带偏）——上游修好自愈；②**地牢墙变体指纹：全图 95>94 单向互换 ×34,699 格独占 54% 墙差**（同蓝主题 slab/tile 变体选择分布分歧，s12345 wal 5.12% 全场最差全由它贡献，地牢盒内 19.8%）——AAAA 以"94/95 互换趋零"为验收；③SolidTile2 的 inActive 位=死差（生成期无人写 wire bit5，备案跳过建模勿投）；④spawnY ±1=出生列首行纯状态症状谓词链无逻辑差。矩阵终版 15 世界：m9 4.175/l5 3.780/s12345 4.366+wal 5.120。
505	
506	**★ YYY 批拆除族移植（2026-08-18）：#49 归零、槽 0-53 全绿**。vanilla 语义：KillTile 尾无条件 SquareTileFrame(cs:63947)→3×3 列主序 TileFrame→帧重要族；生成期实效应只有锚点拆除族（液体唤醒 !generatingWorld 挡/TileFrameCosmetic 短路不掷）。484 滚仙人掌→Check2x2（cs:48405-48805：2×2 锚点反解 frameX≥36 修列+36、四格全等、上方箱族豁免{21,467,441,468,88,470,475}、底部双列 SolidTileAllowBottomSlope→destroyObject 整组杀+尾 4×4；★713-716 在 cs:86398 空 break 列表不走）；485 蚁狮幼虫→CheckSuper（cs:48117-48270，Style2x2+**StyleHorizontal 样式列在 frameX**）。级联整链零掷（484 尘0/485 尘10×0掷）。修 LiquidSim killTileGen 尾接级联（实心查 this.solidNP=各时点 Main.tileSolid 镜像，不直读 GenSolid 规避 rig 态坑）+DesertPass place485 帧轴（竖排 frameY→frameX，8通道不比帧隐身但 CheckSuper 按该轴解样式会误杀完好组）。#49 A/T 10→0、槽 0-53 全绿（#53 13 格=下游连带归零）；(2679,714) 修复（UUU 收口）。★#97 时点 9 组级联杀（sweep 从不收敛支撑亡组）终态净效应 76,259 格+liquid 3,413 格向 vanilla——world-final-hash 红再叠一层，再生归终局。遗留：#97 组无 dump 直证（dump 止 053）；Check2x2 非巨石 case+CheckSuper 376/443/444 未移植（沉降期零存在）；读档沉降 TileFrame 唤醒未接（pre-YYY 即如此）。
507	
508	**★ XXX 批多尺寸矩阵分流（2026-08-18）：中/大尺寸专属债类=x86 基线上零**。m9 均值 typ 4.175%/l5 3.780% 全 ≤ 小世界水位；旧读数 7.43%/l2222 15.38%/l33333 dungeonX 差 279 **全额为 arm64 基线噪声**（x86 上 l33333 头锚全零）。唯一 hdr 差=spawnY ±1（7/14 世界，地形症状非逻辑差）。**修复 FinalCleanup ⑭ DirtiestBlock**（cs:22546-22587 GetWorldSize switch 1=>6/2=>9/_=>3 尺寸敏感曾漏；计数平权 s111 3/3 m111 6/6）；**★遗留新根因类：⑭ 前 vanilla 有逐格 TileFrame 全图扫掷耗（s111 14,212 样本，moss plants 184 每格 1 掷占 99.1%，苔藓计数 14088 vs JS 14085）——JS 帧管线分布式跳过该扫 → ⑭ 从流位 0 起掷位置异（vanilla 流位 14212/14238/14240 vs JS 2/108/262，影响 3/6/9 格/世界）→ 需扫掷仿真（ZZZ 批）**。⚠里程碑单种子绿≠多种子绿：OOO 后矩阵仍见地牢盒残差 s111=5,756/m111=3,374/l2222=1,258 格（测量时点混合，需 post-OOO 复测=AAAA 批）；DitherSnakePass（cs:14814 双地牢，1.4.5）无独立 JS pass 由 DungeonPass 转录承担已备案。尺寸敏感全扫：GetWorldSize 4 处+裸宽阈值 4 处+w/4200 乘区 20+ 处，除⑭外全在场。
509	
510	**★ 用户报障"祭坛在地牢"裁决=原版行为（2026-08-18，seed 12345）**。x86 服务器（arch -x86_64 gen86.sh，新基线 s12345.wld）同种子同位置**同样有这座祭坛** (3288-3290,654-655) 站地牢墙——vanilla 祭坛 pass（cs:15825）无地牢排除（仅 oceanDepths/shimmer/中央带 0.45-0.55 拒绝+Place3x2 门），Place3x2 只查 3×2 净空+地面 SolidTile2 非巨石 → 地牢走廊地板满足即放。★方法论：debug-report JSON→种子+x0/y0/w/h 面积栅格（enc=sheet:fx:fy:wall:liquid）→JS 生成同口径扫描 vs x86 基线对比。**副产物两条真债（已转 XXX）**：①JS 祭坛锚 38 vs x86 36，miss=0 extra=(2411,580)/(429,659)——种子特异偏差（里程碑种子全绿掩蔽）；②同格墙 JS=7 vs x86=95 地牢墙变体残余实证。探针用后即删。
511	
512	**★ UUU 批 #53 R0 清零（2026-08-18）：真 R0=3 格全同源 killTile 尾链缺失**。QQQ 5 格勘误：(2430,662)/(2427,666)"漏 slope2"是 **_slpcasc4 rig 伪差**（漏调 restoreGenSolid→fresh 态 484 solid=true→draws+76 坏基座；★复用该 rig 必须先修）。三格归因：①(2428,664) ghost slope 未清=vanilla KillTile 尾 SquareTileFrame(cs:63947)→3×3 TileFrame 非活性分支 half(false)+slope(0)（cs:82078-83）；②(2679,714) 484 漏杀=K(2680,713)→TileFrame→**Check2x2**（cs:48405，484∈Boulders 四格锚定校验）失配→destroyObject 整组杀（cs:48562-74）+尾 4×4 帧；③(2680,714) 是②下游自动对齐。**canPoundTile active() 门考古无罪**：vanilla 裸读 ghost type 但兜底 return CanKillTile 首门 !active→false（cs:62265）⇒两路同 false，JS flags 早退等价（真差=尾部 !platform/!framed/genSolidType 三门，草木根须族原版可砸 JS 拒——pass53 零足迹备案不改）。修复=HalfBrickPass.ts killTile 尾补 squareTileFrame+tileFrame/check2x2/solidTileAllowBottomSlope（含 PlatformProperTopFrame）移植；clean rig 四变体全 0、draws 5,097,254 恒等；#53 A26/T26/Hf2/Sl18→A13/T13/Hf1/Sl17 严格改善（余=#49 十格级联，YYY 域）。事故：并行会话 12:50 整文件覆写 HalfBrickPass 抹三笔编辑——重读重放+md5 复核恢复（★多会话同文件：编辑后立即复验完整性）。
513	
514	**★ VVV 批 #49 SettleLiquids 终清（2026-08-18）：T 450→10 / L 3477→0 / Lt 57→0，#49 仅剩 10 格**。两根因：①60>59×264 主根因=原版 TileFrame cs:82083-82086 的 AddWater 带 **`!generatingWorld` 门**——生成期一切 TileFrame（KillTile/PlaceTile/岩浆烧除 SquareTileFrame）不唤醒液体；JS LiquidSim onTileChanged→addWater 3×3 监听缺门→每次烧除把 3×3 已沉降岩浆重新入列→kill 满 8→再烧级联（vanilla 77 ⊂ JS 341 包含结构由此而来）。修=监听加 `|| this.generatingWorld` 早退（★必须 generatingWorld 非 load 位——读档期烧除唤醒是原版真行为 WorldFile.cs:738 只置 isGeneratingOrLoadingWorld）。②L=47=worldGenTilesIgnoreWater(true) 使 10/190/191/192 生成期非实心，原版 gen 两 pass（cs:16286-16293/21109-21113）恢复后**无尾部 WaterCheck**；settle.ts 借了读档尾（WorldFile.cs:765-769）的 WaterCheck 把活木水池整片清零。修=`if (mode==='load') sim.waterCheck()`。**残差 10 格定性**：5 组 2×2 仙人掌族（484×3+485×2）孤立上半——vanilla KillTile→SquareTileFrame→TileFrameImportant 锚点级联清整块，JS killTileGen 单格；终态由 multitileSweepPass 收敛、差仅存中间槽（YYY 批专修）。方法论：dump48 直构重放器+逐阶段打点+同码 A/B（基线中途漂移时回退复测）。
515	
516	**★ SSS 批岛屋/banner/门三件（2026-08-18）**：②地牢 banner frameX 恒0已修——placeBannerD 裸 dgWr 只写 type 不落帧+调用处算了 num8 却不传 bannerStyles[num8]（原版链 DungeonGlobalBanners.cs:95→PlaceTile(91,style)→PlaceBanner cs:46270 写 fx=style*18，style≥111 时 fx-=1998/fy+=54）；修复零掷零流扰动。①岛屋桌椅条件撤回语义对齐（桌/左椅/右椅互不 gate：1456 :80064-80068 无条件连放；椅走 Place1x2 只查上格净空+下方 SolidTile2 底格直接覆写）；**未破根因**：金标 15 屋中 4 屋缺家具+3 屋无门=无终态痕迹的瞬态阻断（门变体掷/横幅样式与金标全等→纯 tile 态驱动），需 oracle 级 pass#69 快照二分（WWW 反事实 rig 正合此用）。③"门 8 格缺口"证伪=分解为 (a)★**CaveHousePass 洞穴屋门整体异位**（新独立债类！12345 上 81/78 格、9293480 上 144/150 格）+(b)地牢入口门偏移（OOO 入口重建域）+(c)2 格门变体帧差。附带：补 l10n SoulDrain 键解全仓 vitest 阻断；SSS 与 OOO 交错改 DungeonPass（banner 帧写 vs 墙变体），终局回归须复测 banner 样式分布残余（style12/13 vs 14/15 墙变体 spread 分歧）。
517	
518	**★ OOO 批 #32 Dungeon 全通道归零（2026-08-18）：里程碑首差推进到 #49**。五根因全在 DungeonPass.ts：①I 段 -4,707 主根因=**ClearEverything 漏写 type=0**（4 处 :2214-2262；原版 Tile.cs:140 清 type，JS 只 flags/slope/half/wall→inactive 格残留 stale type 44，而 **IsConsideredDungeonTile 读裸 .type 不查 active**→开关搜索提前 break）；②F 段 solidTile2D 误排平台（SolidTile2 WG:70178 无平台排除）；③F 段 flag4 扫描 break 只跳内层 m 循环（DGGF:525-537，JS break outer6 整跳→bew 计数错位 401,735 vs 481,769）；④Pa 段 lihzahrd 伪掷：GetWorldSize() 4200→0→default→**max=1 零掷**（仅>6400 掷 Next(2)），JS 恒掷 1 颗流全错位；⑤Pa 攀爬起点链式+nearPicture2 wall∈{7,8,9} 判据。**取证法**：Cecil 探针打原版 osx 服务器逐灯 GenerateSwitch 对拍锁定首分歧灯；★arm64 服务器与 x86 金标在腐化区有 ~43.9k 格平台浮点噪声（流全同）——**全图哈希跨平台不可比，须按地牢 bounds 窗口对拍**。#32 八通道 0 差、I 段掷数 36,856 精确、END f890f8a6。world-final-hash/caves-checkpoint 现红=金标 8/17 陈旧（早于 8/18 修复批），终局 UPDATE_GOLDEN=1 再生即消。
519	
520	**★ TTT 批 #47 三格债核销（2026-08-18）：hiveTunnel 漏复位 half/slope**。vanilla 蜂巢隧道是**四连写**（HiveBiome.cs:251-274：蜜核 honey→wall86→active(false)→**halfBrick(false)→slope(0)**；蜂壳 liquid=0→active(true)→**half(false)→slope(0)**→type=225——失活格 slope 也复位！），JS 只写 type/flags → 斜面泥/苔上铺蜂壳残留旧坡（3 格全 t60/t368 基座 s1/s4/s4）。修=HiveSpiderPass hiveTunnel 两分支补 half=0/slope=0（纯写零掷）。#47 Sl 3→0、#48-52 归零、#53 只降不升（Sl 51410→47208 / Hf 11408→10326）；hs 注入雪崩 19,906 消失、clean draws 5,097,254 零差。★**R0 实测=slope 1/half 1 而非 QQQ 预估 5 格**——(2428,664)/(2680,714) 为真差（REV 伪差定性），QQQ 其余 3 格疑为方向定性伪差，UUU 以此为靶。#53 残余全由 #32 typ/act 驱动（OOO 在途）；#49 liq 对 #53 惰性实证（R_liq=1/1）。
521	
522	**★ QQQ 批 #53 雪崩预分析（2026-08-18）：点火(151,869)+三独立源+R0=5格**。机制=loop2 每格无条件掷 1 次 Next(2)（483 万掷）——loop1 任意 1 掷差→后续全错位→loop2 半数坡面翻转→26× 放大。**点火点 (151,869) 精确锁定**：其下格 (151,870)=#32 Dungeon 债（golden 蓝砖实心短路不掷/JS 空气吃 1 掷）。分解实验（golden052 基座+逐族回注）：**#32 typ/act(1716)→主雪崩源 slope 21450；沉降 60>59(264)→独立第二源 14330；#47 起 3 格 half/slope→独立第三源 19906**；#49 liq/lty 对 #53 完全惰性（源码级确认不读液体）。**塌缩预测：OOO+MMM 清零后 #53 不归零——#47 的 3 格必须追加清偿**（(3310,723)s1/(3310,731)s4/(3311,732)s4）。再清 3 格后 R0=5 格（非 RNG 非输入=移植近似硬底；头号嫌疑=JS canPoundTile 加了 active() 门 vanilla 无检查直读 ghost type）。**预警：雪崩不满足可加性（21450+14330≠35780）——终局以直接重放实测为准勿用减法**。(22,664) slope=2 定源=#53 自己写的（loop2 掷门分支，是 (151,869) 点火的第一个下游牺牲格）。
523	
524	**★ PPP 批 T/F/Pa/Ba 预验证（2026-08-18）：F 段独立自因+I 定位价值**。四段 CF（反事实流对齐+世界补丁）裁决：T(陷阱)/Pa(画作)/Ba(横幅) 全随动归零无自因；**F(家具) 有独立自因 -111 掷不随 I 归零**——巫惑台(354) 锚位错：vanilla (401,736) JS 空、JS 错放 (481,769) vanilla=93 普通家具——嫌疑=dgFurnAt alch/bew 分支/flag4 邻域扫描 fluff 盒/place3x3D 判定。**I 段 -4,707 定位**：不是少放灯——吊灯 225 全对、灯笼 110 总数对但 ~21 只错位、开关 23 格错位；吊灯相位全完后灯笼中段流开始错位→dgSwitch 重试循环迭代差累积。工具 _segcf4.test.ts（0.6s CF 探针）+_segscan.mjs（段界流扫描）。032 终态 W/L/砖族全零差→dungeonL 残留格差已不存在。
525	
526	**★ NNN 批浮空岛房门（2026-08-18 用户报修）**：①**"岛屋从不出门"是 2026-08-13 审计误判**——门列=外壳边列（i±(halfW+1)，非室内挖空范围），壳填后 floorY-3 恒实心→PlaceTile 分支 A 恒真→门必放（金标 3 岛 3 门 frameY 486=Skyware 实锤）；②中间岛门朝向反=删门时 3 掷也删→流前移→第三屋 dir 翻转。修 3 文件：IslandHousePass（恢复门放置+PlaceDoor 每行 Next(3)+箱锚左偏一格修正 i-1 非 i+banner 参数）；FurnitureStyle case91 步长 54→18/wrap111（金标 style7→f126 实锤）；BuriedChestsPass rollChestLoot 尾段装饰画/云曾入死数组改 pushItem。复验：三岛门 9/9+横幅 27/27+箱位帧+物品序列=金标逐位全等；30+ 回归全绿。
527	
528	**★ RRR 批终局演练（2026-08-18）：干跑全通+runbook 在 /tmp/final-runbook.md**。oracle 双种子 75 检查点自洽（terrain..corruption 28 项与旧产物逐位全等+ underworld 起=新增地狱屋段）；矩阵 harness 21s/世界（远快于预估）；**再生后红集预测=零红——但有 1 个必须先落的接线：caves-checkpoint:212+shimmer-checkpoint:155 的 underworld snap 前缺 runHellFortPass**（管线已接仅链测试漏）——不接则 47 项全红。shimmer-state-*.bin.gz 必须再生（pre-hellhouse 态）；terrain/unified-random 不需再生。
529	
530	**★ LLL 批入口主体 II（2026-08-18）：G 段核销+谱系澄清+canHit 补**。G 段（BasicChests）根因=LegacyDungeonRoom.cs:86 **先截断后±half**（(int)endPosition.X - num vs double EX 直±——369.999… 小数尾抬 1 格）修后 G-exit 流哈希=vanilla 0.935 真值全等。**谱系澄清**：dgseg/dgchest/dgfeat 全部探针真值出自 Evil:-1 随机世界（猩红），g/ 真值=SW_EVIL=0 强制——**两谱系地牢段流哈希逐段全同**（evil 只改网格不改掷）；VANG0 15k+ ebonstone 差全是 evil 噪声勿追。canHitLocal（Collision.cs:388-475）补③踩实心即停+②slope/半砖/致动门——I 段掷 26,272→32,149（真值 36,856）。**#32 现状 A=1493 T=1706（入口塔体结构零差，差全为 post-I 家具 banner91/墙挂 240/241）——I 段（Lights）-4,707 掷为下一战**（vanilla 14 开关 vs JS 15——JS 搜索早 ~107 掷命中，嫌疑=开关搜索 continue 链微差）。
531	
532	**★ KKK 批 pre-pit 布局债（2026-08-18）：#32 地牢区域归零+里程碑 #33**。根因=**vanilla float32 被转录为 double**（Room 初始速度 Next(-10,11)*0.1f+步长 *0.05f+Hall py 门 Next(20,50)*0.01f+Entrance 1f+Next(0,200)*0.01f——4 处 float32 算术在两侧都被写成 double；~1e-8 偏差累积→(int)(px±K) 盒边缘翻转 1 格=纯网格差零 RNG 影响）。修=Math.fround 双侧同步。**L 阶段 A/T/W=0/0/0；B 段 -3 恢复（156,041 精确+66,975 迭代对齐+流哈希全等）；#32 W=4→0；里程碑推进到 #33**。#33 边界两件已录：入口主体（Tower 楼梯/堡周 ~3300 typ 差异）+G 段流 -3（入口网格差馈入）。HHH 备案 [052] 60>59 族=slot49+ 丛林沉降独立族（264 格+211 lty+3740 液体差）。**遗留：金标陈旧需终局再生**（oracle 已改但零写纪律）。
533	
534	**★ JJJ 批三修（2026-08-18）：lty 归零+oracle 地狱屋补+dgBookshelves 二元证伪**。①lty 修（DungeonPass:2012 liquidType 0→1）→#32 Lt 946→0 精确兑现。②**oracle 补 AddHellHouses 尾段**（cs:13893 位全链：塔环/火把环/家具环/挂画环/旗灯环+17 个 Uw* helper）→**#28 起四哈希与 x86 dump 全等**（c951b5ed…），28+ 检查点 x86 裁决力恢复。③**dgBookshelves 四件套转录后二元证伪**：x86 IL 实证 PlatformItemTypes=new int[0]（GetPlatformStyle 恒不掷）+本种子 181 锚墙 96/9/0→null/Default/null→**机制不产生掷差**——III 的"3 锚少 3 掷"假说不成立。**B 段 -3 真根因=pre-pit 布局债**：oracle 在 (417,748) 留实心砖（布局写入后未清）vs vanilla 空气→B 第 9024 迭代 isDW 门分叉→bailout 前移 1 迭代→尾迭代 -3 掷。修复路径在 oracle 头注 III 终审节。里程碑：#31 全绿/#32 残余 A=1328 T=1501 W=4 Lt=0（全归 pre-pit 布局债另案）。
535	
536	**★ HHH 批 Temple 归零+Dungeon B 尾取证（2026-08-18）**。Temple 三根因全清（046 六通道 0/0/0+half=0+slope=0，总掷 107,941=x86 精确，[046] new=0）：①**反向挖腔游走界不重置**（cs:33800 l/rr/t/b 只声明一次，反向遍历从正向终态续走——JS 曾重置回初始）②**神庙门 PlaceDoor 3 掷**（PlaceTile(10)→PlaceDoor 三格逐格 frameX=Next(3)*18）③**木刺走线方向三元反**（Next(2)==0→-1 被写成 +1——与 L 批房间链方向三元同族）。[052] 3413→2009（余=Dungeon 1501+沉降 508）；[053] 7576→6092。Dungeon B 尾 -3 未定位（取证九段+Place 全扫清白——下批路线：DgZProbe 六段 x86 真 k 裁独立性）。勘误：cs:53683 9×Next(3) 属 PlaceSunflower 非 Place3x3。
537	
538	**★ III 批链 vs x86 首分叉（2026-08-18）：JS 0..31 全绿+首差 #32 Dungeon=双侧同构缺**。三重裁决：JS vs x86 首差 **#32 Dungeon**（A=1328 T=1501 W=4 Lt=946）0..31 **8 通道全绿**（含 slope/half/lty/inact——GGG 8 通道库首次全量应用）；oracle vs x86 首差 **#28 Underworld**（**oracle 链漏 AddHellHouses 尾段**——28+ 检查点永久失去 x86 裁决力直至补齐）；JS≡oracle #32 同点逐 pair 全同=同构缺。**P0 双侧缺= dgBookshelves 漏 styleForWall 四件套**（GetStyleForWall 特殊房间样式→!flag2→不放书→GetPlatformStyle 消耗 1 掷→GetBookshelfMinMaxSizes 覆写——本种子恰 3 个锚少 3 掷→dungeonB 首偏→pass 末 -1906 掷→后段装饰雪崩 1501 格）。**P1 JS 独有=lty 通道**（DungeonPass:2012 liquidType=0 应为 +1 编码 1——liquidType+1 陷阱又一例 946 格）。FFF"≤#23 islands"前提修正（9293480 上 islands 8 通道全绿，云族差首现于 #53）。工具 _mile8.test.ts（槽末 9 通道对拍）。修复路线 4 步在档。
539	
540	**★ CCC 批 x86 基线补全（2026-08-18）：38/38 全量落地+锚点 arm64==x86 逐字节相同**。28 个新世界（16 小+8 中+4 大）+已有 10 个=/tmp/vserver86/ 共 38 个；matrix-anchors86.tsv 38 行与 arm64 参考零分歧（evil/ground/rock/worldId/moon/dungeon/spawn 全等）；worldIdDraw 38 世界全验位 18；3 邪恶对照 isCrimson 精确+零 RNG 扰动。生成器 /tmp/vserver86/gen86.sh+matrixdump86.py（自包含锚点采集器含对 arm64 全量对账）。**终局矩阵全量弹药就位**。
541	
542	**★ FFF 批灰烬草/云块/木块/灰烬（2026-08-18）：四族全判上游症状+前沿≤#23 浮空岛**。逐族裁决：638 灰烬藤=纯 RNG 漂移（总量/锚位两侧同等，差在藤长/起点）；192/191=活树族整棵 patch 树缺失（van 6 簇/js 5 簇——同锚同 d² 一半有一半无，排除流/精度/FP 序，唯余**输入态差**=树 1 区域早期地表 grass vs stone/air）；5=Trees pass 位置漂移级联；57=Underworld 上游族。**根因前沿=JS+oracle 链与 x86 真服的首个分歧 ≤ FloatingIslands(#23)**——islands 检查点云族(189/196)已差 31 格；**链检查点体系只验证 JS≡oracle 从未对真服验证=下一个里程碑**。未做行为改动（无可安全落地修复）；14 个探针工具+LivingTreePass LT_TRACE 增强+18 行审计结论。
543	
544	**★ DDD 批 MicroBiomes oracle 转录（2026-08-18）：74→75 检查点+双种子流指纹全等+隔离 0 差**。~900 行追加（DeadMansChest 备案简化=双链种子 chest sink 恒空实证/ThinIce/EnchantedSword/Campsite/MiningExplosives/Mahogany 全量含 rollChestLoot+Prefix 银行家舍入/TrackGenerator 全文镜像<400 行/placeLavaTrap 含 mbWire 自有通道）。隔离对拍双种子 stream 全等+四通道 0 差。QQ 清单**全部清零**（75 检查点）。遗留：全链 microbiomes 检查点与 oracle 网格不等=上游 cactus 入口 36k 差（BBB 段），终局金标窗口自动恢复。
545	
546	**★ EEE 批蛛网+墙62清剿（2026-08-18）：Webs 1:1+SpiderCaves 测噪+cavinator 终止步修**。三 pass 零自因实证：Webs 隔离全 0（51 族 26k=上游 085 Webs_And_Honey 在墙 62 错位格上放 51）；SpiderCaves 隔离 15108=测量噪声（dump 集缺 slope 通道致团簇格差 -3~-5% 假差——GGG 8 通道库解决了此问题）+上游债；altars 零自因。**两处真修**：①**cavinator 终止步速度 2 骰**（cs:80775 for 后无条件消费 2 骰——JS 曾加 if(num4<=0) break 跳过→每层递归少 2 骰→MCOpenings 后续洞全错位）→隔离 0/0/0/0、033 出口 18641→1501（残余=Dungeon 禁区）；②**IsNotSolid=SolidOrSlopedTile 不含 halfBrick/slope**（名字带 Sloped 但不查坡——曾加 half||slope 门多余）→WallVariety 隔离 0 差、056 段 78.5k=纯传导。s111 矩阵：typ -7.6%/wal **-20%**/liq -22%；51 族 **-52~-55%**/62 族 **-50~-58%**。遗留：032 Dungeon+046 Temple 禁区（HHH 在修）。
547	
548	**★ GGG 批 slot≤12 假设推翻+dump 8通道落地（2026-08-18）**。核心发现："slot≤12 洞穴形状基线差"**假设不成立**——000→031 全字节级全绿（I 批结论仍成立）；**首分叉=dump032 Dungeon（T=1501/A=1328 地牢陈设：陶棺/横幅/挂毯）+046 Temple（T=+1404 蜥蜴砖）**，均在禁区。**052 边界残余从 19913→3413**（并行会话在修 dungeon 链 01:41-01:54 期间 033 项 12582 消失）。SmoothWorld 仅差 1 格（滚动仙人掌 genSolid[484] 生成期窗口已备案）。**dump 8 通道真值库 /tmp/sw-slp/g 落地**（106 槽×typ/act/wal/liq+half/slope/lty/inact；与 van_x86_g 四通道 0/424 位级全等）——slope/half 盲区永久解决。修复责任=DungeonPass(:581 流分歧)+TemplePass(蜥蜴砖) 两处落地后 053→#103 全链自动归零。
549	
550	**★ AAA 批装饰 165 族（2026-08-18）：29k=单点雪崩引燃+修复路径重定向**。核心发现："多 bug 叠加"模型不成立——#103 实现干净（外科手术证：dump102 输入重放仅 (22,664) 单格 slope=2 致宝石树门翻→17/17 精确复现）；**29k 漂移全部是 SmoothWorld（#53）的 SlopeTile/PoundTile 通道（typ/act 不可见）从 x≈22 第 3 列起全图雪崩**（每处 slope 差=+1 掷偏移→90% 放置随机化）。修复路径：①slot≤12 洞穴形状基线（root）②**dump 基建补 slp/half 通道**（当前完全不可见——靠手术实验反证太贵）③165/vines/pots 连锁收敛。QuickCleanupPass (b) 补显式清 half/slope（QQ 备案坐实）。剩余贡献排行：微群系 37.6k（禁区）/藤蔓 29k（雪崩受害）/瓦罐 18.7k（雪崩）/slot≤12 基线 20.4k/蛛网 11.5k。
551	
552	**★ BBB 批 oracle 未覆盖转录（2026-08-18）：5 pass 落地+69→74 检查点**。StructureMap 基础设施（protRects+QQCanPlace+微光登记）+Beehives 全链（hiveTunnel/honeyPatch/FrameOutAllHive/幼虫托台）+Piles 七子段+trees 四族（growTree/EpicTree/PalmTree 含尾扫/VanityTree）+SettleLiquidsPart2 **LiquidSim 全量镜像**（quickWater/SettleWaterAt/waterCheck/10 轮 updateLiquid/sideFlow banker's 取整/TOD 死亡真值表 365 条机栝/KillTile 尘掷族/tilesIgnoreWater 双槽）+Cactus/珊瑚/贝壳/绿洲。oracle 12,076→14,958 行；流指纹四检查点 JS↔oracle 双种子全等。settle2 前 5019 掷逐值全等（差 180 掷=上游并行会话在途）。**未完成：#101 MicroBiomes 1.8k 行**（StructureMap 已备，建议独立批次）。追加区锚点 `// ==QQ-APPEND-TAIL==`。
553	
554	**★ YY 批 Tower 入口转录（2026-08-18）：双离群种子 <5% 达成**。Tower 入口 PrecalculateEntrancePosition 路径双侧（JS+oracle）全量转录：precalc 拒绝环/布局漂移/precalc 爬升厅/Tower 塔体/平台 shelf 链+Dunes 头入口类型掷落 gs.dungeonEntA/B。**关键语义定谳：PlaceWall 掷在写门内**（155 调用=151 写=151 掷——write-gated 命中）；Next(1) 消耗样本；IsAShelf 是 pots/bottles/books/candles>0 的计算属性。**s4444 8.1%→4.34%/s6666 9.1%→4.70%**；掷数 181,252→229,986/230,486（残 500=0.2%）；dungeon 流指纹与 x86 逐位相等；9293480 零回归（69 行 0 diff）。残余：platform shelf -18 掷起书架段流偏（塔体微差级联）+Dome 入口体未转录（Legacy 近似两侧同口径）。
555	
556	**★ VV 批蛛网+装饰+灰烬草（2026-08-17）：三 pass 自清+矩阵被禁区盖住**。三根因：①**Corruption 祭坛 place3x2 缺 SolidTile2 坡门**（cs:70497 slope==0/!half——底座 (2702,413) 带坡、p28 已有 8324 坡位——JS 早退祭坛环→流移→-629,836 掷→卫星裂隙丢）修后掷 5,423,171 精确+四通道 0；②**Stalac placeTight 写最终列非初始列**（失配族 117/25/203/冰 163-200/墙 62 的 UpdateStalagtiteStyle Next(3) 重定型掷永不发生——修=placeTightInitial 初始列冰 0 基/石质 54 基 cs:38355）修后掷精确 typ=3；③**Vines 蜂巢键名断链**（v_444_hive→v_444_bee_hive 退役批更名未跟进→Uint16Array 吞成 0→凹龛全成 2×2 洞 192 格）。矩阵 s111 4.33→4.41%（被 Dungeon 50k+HiveSpider 51 蛵网 WIP 盖住——三 pass 自清后上游清零预期大幅塌缩）。**键名断链=退役批改名的第二受害者（第一是 fix0 拷贝）——grep 全库 `TILE_BY_KEY\['v_` 找 undefined 吞成 0 的断链**。
557	
558	**★ ZZ 批 s6666 Corruption 分支（2026-08-17）：钳制误用+掷流逐位归零**。根因=**dungeonSide 的 zLo 钳制（zLo<400→400/w-400）误用到腐化分支**——1456 源里该钳制**只在猩红分支**（cs:14042-14049），腐化拒绝块（cs:14358-14384）完全没有（1405 两边都无=1456 猩红新增）。6666=corruption/side=-1/第 0 组第 9 次接受原始 zLo=380 → 幽灵钳抬到 400 → 首组区间多扫 20 列 → 全 pass 流偏 +114 万掷。修=钳制包 if(crimson)。**s6666 Corruption 掷 3,535,784=原版精确（哈希命中）；9293480 零回归（隔离全 0）**。6666 firstBad 顺移到 Lakes n=1445。教训：**同函数内两分支的条件钳制要逐分支核——不能把一个分支的门复制到另一个**。
559	
560	**★ XX 批离群种子定位（2026-08-17）**：s6666 "21.4%"已过期（JunglePass TT 修后回落至 9.06%，地狱带 1.73% 正常）；两离群真根因=**①Tower 入口类型整条 PrecalculateEntrancePosition 路径双侧缺失**（Dunes 头三掷 b=0→Tower；s4444=(1,2,0)/s6666=(0,2,0)——Tower/Dome 时 precalc=true 拒绝环+预计算爬升+TowerDungeonEntrance 591 行——JS 和 oracle 都没有！掷账 x86 230,486 vs JS 181,252 差 -49,234；JS↔oracle 全链全等=共享缺）+**②s6666 Corruption 独立分支缺口**（x86 3.54M vs JS 4.68M 差 +1.14M，非输入驱动（66 幽灵格清除后流不变）——该分支未被金标种子踩中）。修复=多小时工程（7 步清单在档），本批定位未修。资产 /tmp/hscmp（两种子 passchain+g27-g31 八通道+dungeon 19-mark 流）。
561	
562	**★ WW 批洞穴墙 62+25/28（2026-08-17）：SpiderCaves 六修+deep 带 62 族坍缩 -24~-62%**。身份勘误：wall62=SpiderUnsafe（非洞穴泥墙）/tile25=Ebonstone（腐化区形状差）/tile28=Pot（总数恒等位置耦合）。六修（HiveSpiderPass.ts）：①**深门 lavaLine→h-200**（UnderworldLayer 恒 h-200——该陷阱第三次复发!）②SquareWallFrame 漏掷 1×Next(0,3) ③countTiles 重写（CountedTiles 只登记非实心格——蘑菇草重复计致 shroom>1 reject 复活）④SolidTile 全谓词+SolidTile2 ⑤placeDeco187 锚位右移 1 列修正 ⑥treatAsNoWall 过时适配退役。25/28 定性 pass 无罪（Corruption 隔离全 0+掷数精确/Pots 源码全审 1:1）——残余全归上游状态噪声（入口态已差 30k/97k 格）。矩阵：deep 带 62 族 -24%~-62%（s111 15509→14715/s777 9315→3508）。**陷阱复发警示：lavaLine vs UnderworldLayer(h-200) 恒值已第三次踩中——全库 grep lavaLine 确认所有消费点用哪个语义**。
563	
564	**★ UU 批大尺寸+floor 审计（2026-08-17）："大尺寸差距"=矩阵基线架构错配（非 JS bug！）**。三方铁证：vserver 39 世界基线全是 **arm64 原生切片**生成（TerrariaServer.bin.osx universal 裸调走 arm）；arm64 重跑 l2222 vs 基线=零差；x86 重跑 vs 基线=14.9%——**"差距"全额为原版自身 arm64↔x86 FP 分歧**（小尺寸同病：vserver s9293480 vs x86=4.79% 零 JS 参与——小尺寸矩阵"4-5% 基线"主体同为架构噪声！）。**JS↔x86 真值：P|0-P|30 流哈希全等+g17 网格位级零差**。l2222 vs x86 基线=**4.501%**（<5% ✓）。顺修真 bug：**skyLakes 硬编码 1→按 w>8000/6000 分档（小1/中2/大3）**——P|23 流哈希精确。Math.floor/ceil 308+295 处全库审计零新差（69 处乘法型逐条核过：正积恒等/负侧被 max 钳制）。**遗留：39 世界 x86 基线重生成（arch -x86_64，~2-4min/个）**；CaveHousePass:1249 ceil→trunc 待案主；Math.hypot 18 处 ulp 另案。
565	
566	**★ SS 批 house17 +90 掷定罪（2026-08-17）：备案收口+两方法论大发现**。定罪=原版 AgeRoom ③ ClearTile(frameNeighbors:true)→TileFrame→TileFrameImportant→KillTile(默认 noItem=false!NN 误排)→KillTile_DropItems→NewItem 前缀/堆叠掷+SquareTileFrame 九邻递归——**完整调用栈事件级实测**（AR#29 granite 15×8 同构房 ③ 跨度 224=120+104 实录）。定性=备案收口（掉落物瞬态不回读、NN 注入 90 全绿已证零生成效应；完整移植需搬 TileFrameImportant 全量+KillTile 掉落链，收益仅掷位）。**挂账真分歧：③ ClearTile 杀邻不移植——typ 通道会现形**（NN 四通道真值不含 typ/wal 故未暴露；JS clearTile 只清格不杀邻）。**方法论两条**：①**h2k 哈希锚定跨 run 是同义反复**（hash(k) 在任何耗满 k 掷的流上必然命中同态——跨 run 取证必须事件序号锚定或先证流全等；前 4 轮验证全跑错路径仍自证成功）；②NN 真值流本机不可复现（pass30 起分叉、pass59 又全同——疑其 run 另有 env；同命令重跑零差=确定性但跨机不可比）。工具坑：Steam Mac TerrariaServer 热方法绕 Cecil 入口钩（须换 Windows 构建基址）、mono 内联吃栈帧名（入口/出口括号+计数器替代）、dotnet run --no-build 改码忘重建（三次踩中）。
567	
568	**★ TT 批中尺寸分界带（2026-08-17）：typ 20%→4.5% 双世界收敛**。根因=**JunglePass.ApplyRandomMovement 的 Math.floor→Math.trunc**（原版 (int) 向零取整——小尺寸 scale=1.5 乘积恒整数免疫（floor≡trunc），中尺寸 scale=2.286 负界差 1（-228.57→-228 vs -229）→巨型泥 runner 中心偏移 180 格→全丛林几何重随机化→10 万格级联）。修=JunglePass.ts 两行。**m111 typ 20.1→4.82%/m777 15.4→4.45%；deep 带 59↔1 从 12.8 万→138 格**。小尺寸算术免疫回归过（双种子 checkpoint 全绿）。**大世界 l2222 cave 59↔1 ~39k=非此因**（scale=3.0 恒整数）——大尺寸独立债另案。全库扫描无其他 Math.floor(- 受累点。
569	
570	**★ #22 矩阵终判第一轮（2026-08-17）+ 终局金标统一**：金标统一批完成（caves-chain 69 检查点双种子 3/3 全绿 146 项 ✓、shimmer shimstate+链双更新 5/5、world-final-hash 3/3）；全量回归 3484 过/8 红（全=游戏逻辑域他人 WIP+测试基建+预存，世界生成域零红）。**矩阵第一轮（小 8 + 中 2）**：小 6/8 种子 typ 4.2-5.1%/liq 0.52-0.62%（收敛区）；离群 s4444 8.1%（地牢链漂移已归因）/s6666 21.4%（地狱带横移已定位）；**中尺寸 m111/m777 typ 20%/15%——签名=59↔1 泥↔石对调 5-12 万格=中尺寸下泥石深度分界整体错位**（地形锚 23/23 全等但深层 zone 大换位——中尺寸 rockLayer 以下分界带的 pass 行为需专项）；液体差异中尺寸 3.7-3.9%。稀疏对象（s111）：树 204/207、瓦罐 3542/3521、宝箱 169/166——全部已归因为输入级联。sky 带 -1>59 泥块渗入=中尺寸地表分界残余。
571	
572	**★ RR 批矩阵真缺口（2026-08-17）：六项全处置+Pots pass 首次归零闭环**。修 3：①moon 恒 0（Next(9) 曾掷而未存→world.moonType 落地，8/8 绿零扰动）②spawn 循环二上界独占化+谓词归位 active()+type!=379（曾 isGenSolid 误拒非实心活性）③_t1iso pots rig 缺 481-483 裂砖/192 活叶 GenSolid 翻转（旧注释"已预翻"不实——此 rig 债曾假报 -9~-26 万掷级联）。归因 3：④**瓦罐 draws 2,280,726 精确+四通道 0——Pots 代码 1:1 实证**，矩阵偏少=纯输入级联；⑤树 s5555/s4444 雪/沙假说不成立→输入级联（TreePass O 批已证）；⑥spawnY/dungeon s4444·s6666/蛛网/墙 62 全归因（dungeon 链=纯流函数恒等 8/8 锚证；s4444 爬升漂移>140 格实证）。复跑：hdrΔ 2-5→1-3、moon+spawn 8/8。**教训：rig 的 GenSolid 时点翻转清单要与管线逐 pass 核——"数据已预翻"注释不实证就信=假级联**。
573	
574	**★ QQ 批 oracle 链扩展（2026-08-17）：65→69 检查点+67/67 双种子全绿**。新检查点：statues/cavewalls/undergroundjungletrees/quickcleanup（推进=整 pass 跳段 island——两侧同 skip+Replay 隔离零流影响）。顺手修两 oracle 债：①**DgChTile 缺 Clear(Slope)**（原版 ChangeTileType 无条件清——地牢砖残留 203 slope 格，63 检查点四通道哈希全盲直至 QuickCleanup 坡位敏感消费端显形——**四通道哈希不含 slope 的盲区警示**）②ResetToType 缺坡位复位（GravitatingSandCleanup）。**仍无法覆盖**（前置工程）：Beehives（需 StructureMap 保护登记链基础设施）/BuriedChests 段（CaveHouse 族 1.3k 行）/Trees（#71-81 全转录 705+629 行）/SettleLiquidsPart2（液体引擎接线）/Cactus·MicroBiomes（0.4k/1.8k 行）——另批或终局窗口前补。附带备案：JS QuickCleanup (b) setTileSilent 不清 half/slope（原版显式清——island 链哈希不可见，全链转录后显形）。
575	
576	**★ NN 批房屋链收敛（2026-08-17）：632/632 事件+42 屋仅 1 链残余**。六根因：①oceanDepths 半边门（原版先 y 门——地下屋恒深从不触发；曾只抄 x 半边误拒海滩带）②FillRooms 裸 switch i≥2 落空（w≥24 房第三档零放置零掷；曾 %2 回卷）③**Tile.Clear 坡度/半砖残留**（setTileSilent 仅 type=0 清位→壳填/aging 后 slope 残留——house27 宝箱腿 slope=2 误拒；期间误判 SolidTile 无坡门已回退）④**PlaceTile 返回值=锚格 active**（cs:60279——"无放置计数+1"，磨刀站踩工作台→SharpenerCount 4v3→门翻转）⑤沙漠追加屋矩形=description.Hive 非 Inflate CombinedArea+RandomRectanglePoint 开区间⑥__swChestDbg 钩。AB 565→632/632（首异 #579=house17 一链）；house0-16/18-41 全绿；N₅₉ -10,802→**-1,805**；[060] 84/84 零差。备案：house17 ③ 尾 +90 掷（已证零世界效应+严格在 walk 后，机制已排除四嫌疑，待 Cecil draw-stack 直证）。
577	
578	**★ PP 批矩阵 harness+基线（2026-08-17）**：tools/_matrixrun.test.ts（SW_MATRIX=small8|smoke|all|report 门控；增量累积 /tmp/matrix-report.json；四维：头部 11 锚+稀疏逐棵数+五带四通道+整体差异率；JS id 投影 sheet 空间 unmapped=0 全覆盖）。**基线（小 8 世界）**：typ 中位 4.2-5.1%/wal 3-5%/liq 0.52-0.62%；离群 s6666 21.4%（地狱 ash 横移）。**真缺口清单（逐棵/锚级显形）**：①moon 全 8 世界差（JS 掷了 RandomizeMoonState 但丢弃——WorldGen.ts ⑯"未消费"，world.moonType 恒 0）；②spawnY 差 1-2 格（出生点搜索落位）；③s4444/s6666 dungeon 入口链分叉；④瓦罐系统性偏少 21-96/世界；⑤s5555/s4444 树 JS 多 15%+；⑥cave 带蛛网 51 漂移+墙 62 带界横移（1.5-1.9 万对称对）+surface 带 25 双向。生成稳态 21-38s/世界（首 117s JIT）。
579	
580	**★ LL 批死亡表+仙人掌（2026-08-17）：真值表 1258/1258 全绿+仙人掌掷数精确归零**。①死亡表 100%：提取器四根因（ApplyNaturalObjectRules→UsesGlobalLiquidChecks 25 处/CopyFrom 模板继承/addSubTile 后重置 base 缺省非继承/Width 计入 fullW）+备选项只查被替换对象自身（cs:5240）——**tools/_todcheck.test.ts 常驻门槛 1258/1258**；JS 接入 tile-object-death-table.ts 365 条（null 回退全局）+diesIn() 两处替换+C# int 除法向零截断。②仙人掌根因=**growPalmTree 漏尾帧扫 RangeFrame→CheckOasisPlant 清块**（cs:27354/47617——棕榈放的 530 块原版会被自己尾扫整块清除，JS 残块挡后续燕麦→流分叉→列平移 29）——palmRangeFrame 零掷挂三路调用点尾；P/K 69/69 事件 1:1、**pass 末掷数 1,248,713=passchain 反演精确**（-26,863→0；顺带更正 1,268,797 错值标注）。rig [097] 1340/1088、[098] 651/623（+36=上游级联）。
581	
582	**★ MM 批房屋段终清（2026-08-17）：house0-4 全段位级全等+十一修复**。方法=逐阶段 k 对拍+逐 Gen 跨度探针（__swAgeGen 钩）+UR 流仿真。要点：①**Actions.SetTile 默认清墙**（Tile.Clear 掩码含 Wall——木①蛛网/蘑菇②抹墙→OnlyWalls Fail 主根因）②**AreaOr(.Not()) 整体无实心才命中**（GenCondition Or×InvertResults 反转——曾 any 语义致门/平台滥发）③**家具击杀模型**（ClearTile 邻格→Check3x2/2xX/Chand 支承重验→KillTile 整件——钢琴滞留挡箱+小堆之谜）④家具放置器族 1:1 重写（居中锚/顶锚/底承/2 宽各就位）⑤SolidTile2 走 vanGenSolidType（tileSolid[19]=true 平台生成期实心）⑥吊灯 key 勘误（sheet34 非 100——吊灯曾从未放置）⑦撤 245 画作掷（Place2x3Wall 专路零掷）⑧PlaceDoor 每门 3 掷+锚门+右扫起点。**AB 558→565/632（house0-4 位级全等：EmptyRooms/楼梯/FillRooms/AgeRoom 三段逐 Gen 精确）**；#60 不动；N₅₇ -10.8k 欠掷暴露（首异 #565 屋，逐屋剥层法在档）。
583	
584	**★ JJ 批 Prefix+蓄水池（2026-08-17）：#60 dump 全 0 差/abCalls 317=vanilla**。①Prefix 再掷环 1:1（Item.cs:523-556 while 环：Next(4) 早退→池→Reduced→TryGet 四失败门重进；PRE_MULT 乘子表/PRE_STATS 21 件武器类/**netRoundEq=.NET 银行家舍入 half-even+float32 乘**——1.05f 族 10×1.05f=10.4999995→舍回 10 失败、3069 mana=2+kb=0 双失败体）；**地狱尾 3-4 掷真根因=5010 宝藏磁铁漏登类表（CanGetPrefixes 默认 true 非排除表——注释"调而不耗"系误判）+地狱 305 族门 >1 应为 >0（cs:37334；洞穴分支才 >1=近形误抄）**→循环② 0/15 全命中。②#60 蓄水池根因=**扫描界随选中点漂移**（原版固定锚 num6/num7 与选中点 num3/num4 分离，JS 曾 cx/cy 兼任→界漂移+越框选中）→draws 28,810=N₆₀ 精确、AB/ABX 317+317 全零差、**dump060 四通道全 0**。连带 #58 78,298→77,156（N₅₉ 101%）、AB 对齐 558/632（残余=房屋段墙重帧掷族另案）。
585	
586	**★ KK 批 granite 首红（2026-08-17）：FF"多清 slope"勘误+oracle 一行修→oraclesync 66/68 绿**。"JS 多清 6-10k slope"=**隔离 rig 伪影**（buildStore 类 rig slope 通道不回注，"清零"发生在建 store 期；真链三方裁决 @20-22 slope/half/act 全 0 差、流 marble=248,340/granite=78,137 精确）。真根因=**oracle GraniteBiome CA 漏 tAct=true**（vanilla :179 CreateFlow 恒 active:true——稀疏双缓冲+轮末 Swap 下残留 inactive→CA 细胞提前死亡→岩体缩圈；JS 同位置早修过、oracle 保留旧病=**同源转写坑要双向 grep**）→caves-oracle.cs:2861 一行修。**oraclesync 双种子 green=23→66（红=45→2，仅 dirtlayer/rocklayer 链外名）**。教训：隔离 rig 通道完整性第一嫌疑。工具 _gslope（真链六通道 dump：caves-checkpoint:131 休眠钩扩 slope/half）/_gflow（真链流计数）。
587	
588	**★ II 批沉降 round0+仙人掌（2026-08-17）：qw/wc 相位归零**。沉降六修：①**worldGenTilesIgnoreWater 整段缺**（qw 317 格首分叉：雪屋冰屋门10 被当墙）②WaterCheck/UpdateLiquid 首尾包裹缺③solidNP 须注入 GenSolid 生成期覆写（裂纹砖 481-483 恒 false）④**cycles 7→10**（ReInit 态；7 是运行期画质档!）⑤379 泡泡+546 例外⑥轮上限 n3*5 精确（尾轮振子预算 break）。**qw 相位 liq/lty 逐字节一致；wc nl=2402 精确**；draws -7059→-3690。**方法论沉淀：SW_EVIL=0 强制对齐真值血统（天然 roll 从 pass26 分叉）**。残余备案=wc 死亡判定对象感知（TileObjectData.CheckLavaDeath 按 type+style 解析——96 格地牢家具 vanilla 不杀 JS 全局表误杀；反射真值表 1258 元组留存，32 格系上游帧债）。仙人掌：**P/K 事件链+FNV 对齐至 [66] P(2789)**，残余=P(2789) 内 150 试环掷耗差→命中列平移 29（2913 vs 2940）。探针 cecil ddfin 六相位模式+WaterCheck 反射真值表基建留存 /tmp/sw-ddfin*/。
589	
590	**★ FF 批 oracle 同步（2026-08-17）：30 条落地+23 绿+唯一自因缺口定位**。oracle 10094→10861 行双种子 65 检查点跑通；JS↔oracle 直拍 **23 绿**（terrain→mudcaves+沙漠族/蘑菇/大理石全绿——F/G/K/I/J 批两侧一致实证）；**沙漠流指纹=JS=原版真值逐位**（desertentrance 345f4efd/deserthive 46d14bb7）。新增落地 14 大项（沙漠 SWF4 点+wallLargeFrames 表/smoothMark/187 Check3x2/钟乳石 165 全生命周期含 frX/frY 通道/CleanupArea 逐格/岛墙 73+CloudLake puff/活树 187 链/underworld 633 重掷/QuickWater 全段/大理石五门/花岗岩链/TileRunner 383 精确集+SAVE_SLOPES/湖泊幽灵传播/蘑菇 KillTile/ChasmRunner PlaceWall）。跳过=链外/在制（#46/47/56/67/97/98/101/68/70+trees+HellHouses）。**granite 首红=唯一自因缺口**：JS 在 desert→granite 间多清 ~6-10k 格 slope（(2626,234) 2→0，源头语句未找到——MushroomPass 无 slope 写、Proxy 追踪器静默失败）→marble 流差 29,916（N=248,340 vs 278,256 fresh+N 定标）→granite/islands 级联。资产 /tmp/js{mush,marb,gran}.slope+csgran2.slope+pyur.py；对拍工具 tools/_oraclesync.test.ts（改两行 JSON 路径可复跑）。caves-checkpoint 红=金标 8-16 陈旧签名（终局再生后收敛至 granite 首红）。
591	
592	**★ GG 批房屋链（2026-08-17）：掷数 78,298/N₅₉=76,364 收敛**。两主根因：R1=**墙重帧掷 ~5 万欠掷主体**（Actions.PlaceWall/ClearWall→SquareWallFrame resetFrame 默认 true→中心格 Next(0,3)+墙21 Next(2)+wallLargeFrames 22 豁免；PlaceWall 掷序=置墙→自格→四邻按彼时墙值——15×8 房 215 掷/17×8 249 掷实测）——JS applyChain 曾零掷，已按位建模（wallFrameResetRoll/placeWallRolled 覆盖内腔/楼梯顶步/AgeRoom 七主题）；R2=**房间互斥自创门**（原版 AreRoomLocationsValid 只查 InWorld+底界——above/below 房天然重叠！拆除后房型分布 {1:21,2:17,3:4} 全等）。冰主件±7 根治（SetDefaults+Prefix(-1) 无条件调用+1319 雪球炮 gun 前缀化+36 件主件类表）。其余六修各有 x86 实证（地狱回城 Next(3) 序倒/cave oceanDepths 门/underworld wallDungeon 门/flag9/岩浆门/#60 notNearOtherChests 12,904→20,639/28,810）。**勘误：/tmp/chestd59.* 首跑产物 half 漂移 10,939 格作废→/tmp/hg/chestd59v2.***（SW_EVIL 强制后采集）。备案残余：Prefix TryGet 失败再掷环（银行家舍入四失败型需 per-item 属性表）+#60 残差 8.2k。
593	
594	**★ DD 批沉降+仙人掌（2026-08-17）**：#97 五修——①**KillTile 族三触发链全接**（killTileAt 统一分发：运行期钩子/生成期 killTileGen——WaterCheck 死亡表/LiquidCheck 裁切/checkAlch·checkLilyPad·merge；沉降期钩子曾为 null=静默零行为）②尘掷族（杀族全零掷型，唯一实掷=蛛网51+墙62 Next(4)）③pass 链掷骰接线（254→255 Next(30)）④岩浆烧除 60 写错 dirt→mud（t0>59×212 根因）⑤AddWater 尾击杀 gen 门+QuickWater 尾 InteractionsCleanup+撤收敛早退。typ 2652→1903。#98 根因=**CheckCactus 支撑复查链缺失**（SquareTileFrame→TileFrame case80→悬空/失托→KillTile→3×3 级联塌杀；旧版静默放置）→347→51。rig [097] 1839→1265、[098] 667→619。残余（round0 流级分叉+过渡仙人掌掷差）备案需 exe 中途 dump/列级 trace。
595	
596	**★ HH 批 Dungeon 砖清坡（2026-08-17）：@52 坡位 219→3**。根因=原版地牢全部砖写经 DungeonUtils.ChangeTileType（DU:1605）含**无条件 Clear(Slope)** 尾缀——JS 只写 flags/type。修点 11 处全带行号锚（chTile 一处收口覆盖 30+ 调用+chWall/门侧槽/spikeRun/dgWr Place* 家族/placeSimple/dgSwitch/门锚格/placeFurn/placeWallArt）。**刻意非修**（原版本就不清坡）：入口 0.5 框内厅/开放门厅/门洞清空/坑陷阱 else/**KillTile 只清 half 不清 slope（cs:63933）**。"砖型债 44↔91↔241↔240↔42"勘正=sheet42 灯笼误读，债族=B 段家具摆位级联，粉/裂变体错配不存在（pair 直方图 481-483 零条目）。[032] 2330/1328 维持（B 尾 -3 级联另案）；[052]=0/0/0/0；**残余 3 格=蜂巢块 typ225 归 HiveSpiderPass 域非地牢**。#97 沉降前提已达成可攻。
597	
598	**★ EE 批大理石/花岗岩（2026-08-17）：悬案笔误破案+granite 本体 1:1 无瑕疵+隔离五 pass 首次全绿**。granite -703,003=VN 表笔误（781,137 多抄一位，真值 78,137 唯一命中）；-3 掷+7 格=隔离重放缺 slope/half 输入伪影（CA 初值坡面敏感；注入后 draws 精确+四通道+输出坡位全 0）；@52 残余 219 格全部移交 DungeonPass（"花岗岩区"勘正=地牢粉砖落位，真值砖写 ResetToType 清坡 JS 不清+砖型债 44↔91↔241↔240↔42——证据链已移交，砖写入补清坡后预期塌缩）。新真值 /tmp/sw-ycal/van22（106 pass×8 通道 x86 重采，双 SAME 复核）。**rig [021]-[023] 维持 0/0/0/0；隔离五 pass（DirtToMud/Silt/Islands/Marble/Granite）掷数+四通道首次全精确全绿**。
599	
600	**★ CC 批箱族+雕像（2026-08-17）**：四修落地——PlaceChest→TileObject.CanPlace 全链（U 批引擎同源；含 blockType()==0 坡/半砖腿门 cs:388）/IsUndergroundDesert 1:1（±15 邻域墙扫替旧矩形）/Item.Prefix(-1) 耗掷模型（18 件交集接入 rollChestLoot）/SeedHouse ctor 掷（每屋 NextFloat 曾整段漏）。#60 边界 72/72→50/50；AB k 对齐 13→59/632。**定标：N₅₈=3561/N₅₉=76,364/N₆₀=28,810/N₆₃=160,186**。新基建：ChestProbe（AB/HB/CPBox/D59——**hs54 陈旧 5 万格，slope/half 真值须 pass 头重采**）；钉子=RP 织在 reseed 前（k 从重播后 0 起）+**SW_EVIL 必须织 GenerateWorld 头**。残余立案（资产已备）：房屋链欠掷 5 万（applyChain/FillRooms 逐掷 diff，vanilla 每屋 651-5149 掷占 92%）、冰主件 ±7/箱尾、#60 蓄水池 15.9k、SpiderCaves 禁区欠掷 4.8 万。
601	
602	**★ BB 批微群系+仙人掌（2026-08-17）**：①**MahoganyTreeBiome 整段缺失移植**（-43,845 掷；双锚搜索/50×50 材质门/五段干身 383 float π/墙78 井/ShapeBranch×4/叶球/四根 ShapeRoot（NextFloat Math.fround 单精度）/AddBuriedChest style10 ivy）+DeadMansChest 候选序=chest sink 创建序（wld 槽位序 181 箱实证）+CanPlace 白名单。②**二次沉降时点根因**：vanilla #97 在 #98 前二次沉降（云格水 255→0），我们一直 generateWorld 之后补跑=晚 8 pass→新管线槽「二次沉降」（蜂巢幼虫后仙人掌珊瑚前）+撤 worker/Game 生成后沉降（读档路径不动）——#98 new 667/638/0/0。定标 #97=55,987/#98=1,268,797/#101=1,655,134。新真值资产 /tmp/sw-mb-hs9*.{四通道}+/tmp/sw-mb-chests2.json（wld 槽位序宝箱清单）。残余定位：#97 沉降自因 7,215 liq+淹水植物 KillTile 族（坡面真值=10× 放大器）；#98 仙人掌 -7,120 掷（0.56% 相位）。
603	
604	**★ AA 批 E 段终清（2026-08-17）：Z 批双归因勘误+全段收敛**。勘误一："+169"真根=**GenerateEntrance 条纹窗墙 169 次 PlaceWall 每调用恒耗 1 骰**（vanilla 逐位 +1 实证；PlaceWall 耗掷族第 6 命中）；勘误二：EarlyDual 坑前段**不存在**（Default 型全 skip；144=24 次失败坑尝试×6 掷（makeNextPitTrapFlooded=true 短路 Next(8)），第 25 次 k=6977 命中——旧硬跳恰在正确相位）。修复：条纹窗墙耗掷+平台扫描 n27=0.5 框底（平台行 611..622,249 逐格全同）+撤硬跳。**终验：全段流 mark 哈希逐位全等（E=6833/Pi=9433/C=14400 双精确）；B=156,038(-3)；END=241,387(-1,906 级联)；dungeon 区网格债 72k→1,505 格**；双种子 dungeon 带内 0 差。备案：caves-checkpoint desertmound 红=并行会话 DesertPass WIP（带外 40 格同源）。
605	
606	**★ Z 批 B 段结案（2026-08-17）——B 无罪+E 段真根**：TileFrame(19) 嫌疑证伪（只写 frameX 无副作用）；**B 段转写逐位 1:1**（忠实回放 /tmp/dgu/brep3.py：67,970 iter/182 书架/末掷全等；CanGenerateFeatureAt 325 调用全 TRUE）。真根=**E 段入口走廊网格级联**：入口平台行错位 vanilla(611..622,249) vs 端口(609..621,257)→首座隐形书架被互斥扫描拒→+2,092 级联。**+313 精确拆账=入口走廊相位(DungeonCrawler.cs:397-452)+169 + EarlyDual 坑前段(cs:472，非 dual 也跑)+144**；入口类型实测 Legacy(掷2,2)。未竟（AA 线）：E 段五件套逐掷 diff（GenerateNextEntranceHall_Legacy/LegacyDungeonHall.GenerateHall/LegacyDungeonRoom.GenerateRoom/roomDelay 支/GenerateEntrance）→平台行归位+EarlyDual 144 掷转录+撤 DG_SET_ROLLS=6977 硬跳→B 末掷 156,041、END 243,293 预期随动。探针资产 DgFeatProbe/DgGridProbe/vanB.raw 在 /tmp/dgu/。
607	
608	**★ W 批 Dungeon 收官（2026-08-17）**：TileObject.CanPlace 锚定引擎两侧移植（双腿判定/内盒可覆盖集 tileCut∖{484,654}∪BreakableWhenPlacing/边界5垫/巨石读 type 不读 act）+**cs:37578 单次落位语义**（AddBuriedChest 首实心行掷一次败即 return false——旧版 continue 凭空深处落箱）+上锁箱尾三掷→**C 段双精确（roll 14,400+指纹逐位=；19/19 箱+5/5 位）**。**k0_v=6977 证明**（Pi/S/D/W/P 四段 FNV 全等）。终态四通道 liq0/wal4/typ0.028%/act0.034%（基本收敛）；残 -6,183 卡在 **B 段 +2,092=尾段隐形书架 ~9 座被拒**（首选嫌疑 TileFrame(19) 平台帧副作用，744k 行探针数据已采 /tmp/dgu/ 待解析）；E 段 pre-pit +313 拨针备案。oracle 同步清单 30 条。
609	
610	**★ X 批（2026-08-17）**：#19 幻影坡=**DesertPass 无罪**（@19 出口 0/0/0）——真凶=**TileRunner 写 type 时缺 ClearSlope**（原版 !SaveSlopes[type]→ClearSlope cs:77338；SAVE_SLOPES=tileSolid∪8 豁免 sheet LUT 已补，全家族受益）；残余 351=神庙砖幻影坡（TemplePass 同病，下批）。#67 全归零（**draws 53,270=vanilla 精确+四通道 0**）："自身门差"两层=重放 harness 缺管线时点 GenSolid 快照（-3,230 掷，225/379 翻转缺失阻断洪泛）+GrassWallPass isSolidTile 漏全谓词（!solidTop/!half/slope==0/!inActive，坡面格原版算实心，单此 4,918 wal）。[056] 91,957→73,021。**U 批③归因勘误在档**。备案：_walliso temple 段 gsPristine rig 断裂（前批遗留）。
611	
612	**★ V 批 half/slope 首分叉（2026-08-17）——颠覆性前提修正**：T 批"本机 exe≠x86 基准"被推翻=**arm64 mono 切片所致，arch -x86_64 Rosetta 下 106/106 全等**→vanilla 侧 half/slope/liquidType/inactive 四通道重新可采（/tmp/sw-hsv/ HsProbe 真值 bins+519 万行追踪）。首分叉=#53 SmoothWorld 自差四件（**主=KillTile 尘粒掷全缺 -9k 掷**（草灰岩633 Next6×10/草族地狱石 Next2×10/蛛网51墙62 Next4/地狱石58 UnderworldLayer 下灌岩浆）+悬顶 else-if 归属+贝壳堆侧邻+补角拒放门）→#53 掷数 5,097,254=vanilla 精确、四通道残 1/1/0。#54 证 1:1。**#67 残余 23,142→7,998（上游 half/slope+lty 源已断）；余 7,998 伴 -3,430 掷=#67 自身门差（完美输入仍偏，另案）**。新债定位：#19 沙漠幻影坡 545 格；KillTile 尘掷/TileFrameImportant 支撑链其余 pass（已验证全零的 pass 无虞——位级全等自证其 KillTile 路径对）。GenSolid snapshot/restore 基建。
613	
614	**★ U 批 Dungeon 终局（2026-08-17）**：①JS 468 格=**假差**（tests/_dgestairs 缺 Dunes 头 reseed→入口堡 rr 全错位；生产管线本就正确——游戏从未受影响；补 reseed 后 468→0；**rig 缺 pass 头 reseed 会造假差**新坑）。②k0 相位定界 [6737,6977]+vanilla 首 pit 逐位复现（pyur.py 位级 Random 复刻+全门仿真；**k0_v=243,293−rest 待 G 段清后直解**）。③后段三根因：F 段椅/床/浴缸 Next(2) 方向掷整支缺（两侧已修）+**单格放置近似→Place* 全家族 14 helper+tileTable(76/146 含平台19 支撑语义/241=Place4x3Wall/103=桌上版)**（两侧已修）+**G 段宝箱落位=TileObject.CanPlace 锚点调整引擎未移植（15/18 箱位差，残 5,563 掷）**（定位在案 W 线猎杀）。B 段"61%嫌疑"排除（Default 样式数组空）。END=237,730 vs 243,293。oracle 同步清单 29 条。
615	
616	**★ T 批蜂巢终清（2026-08-17）：#47 掷数精确+四通道 0/0/0/0**（1,029,837=vanilla、1023/1023 标记、53 隧道逐位全等）。五连环根因：锚点 active 前置门自造/土壤圆 (r+1)² 非 r²/IsSolid=SolidOrSlopedTile 无形状门/蜂蜜斑地狱门=UnderworldLayer(h-200) 恒值非 lavaLine/隧道 InWorld 上界等号+写入三件（SetTile clearTile 清墙液坡/蜜核幽灵/蜂蜜斑写 229 非 225）。CanPlace 扫门落地（GenState GENERAL_PLACEMENT_FORBID 28 id+CaveHouse 自有窄表 11 id）。#67 定界：**本机 exe 重跑≠x86 基准世界（evil 旗标+架构 FP）→vanilla 侧 half/slope 通道不可采**，rig 改注管线时点快照（39,679→23,142），(775,565) 首门翻 JS 洪泛自证完备→残余=上游 half/slope 级联非语义。IL 注入坑：第二轮 patcher 须从 pristine 重打（已注入 exe 会被误读致标记×2）。RunPass 重播再证；生成期 TileFrame 全零掷。向日葵测试种子 42→44（合法流移）。
617	
618	**★ S 批 Dungeon 楼梯+一格（2026-08-17）**：①JS 楼梯+Bounds.UpdateBounds 移植落地（DG_FRAMED_ALL 411 表 verbatim，sheet 空间比较走 TILE_DEFS[].vanilla.sheet；dungeonE JS↔oracle 4438→468，**残余 468 经 vanilla 仲裁=oracle 对 JS 错**=入口堡垛口/内室既有转录差，另案）。②(207,876) 假说推翻（跨段误读）——真根因：**A. vanilla pit 起点 k0≡5(mod6) vs oracle ≡4（相位差）**；**B. DG_SET_ROLLS 全模族扫描无一命中真值 243,293→S/B 后段仍藏转录掷差（B 书架段 143k 掷=61% 头号嫌疑）**；pit 转录无罪（99.95%）。⚠️seed-2 金标被标准三参命令误写（.ghost/.jseg）——终局再生以其为准，seed-1 未动。oracle 新钩五件（DG_ROLL_SEARCH/DG_WATCH/DG_PIT_FAIL_AT/DG_SET_ROLLS/DG_PREPIT_EXTRA）。下一步在档：TileRunner 尾区逐掷探针+B 段墙图敏感性二分。
619	
620	**★ R 批 AddHellHouses 终清（2026-08-17）：rig[028] 全零达成**。五根因：①**四门位落门+每门 3 掷**（M 批"PlaceTile(10) 恒 false"被 dump 实证推翻——HF 几何下分支 A 恒成立，PlaceDoor 每格门框 Next(3)）②**右外门原版 bug**（cs:33218 用列号非 x 判界恒真→右门从不触发，1:1 保留）③家具/挂画/旗灯 Place* 族 16 helper 1:1（床/浴缸镜像帧基 72 等）④旗灯环锚点判活分支⑤styles[3] 先掷再判重。**HF 掷数 185,299=原版精确+隔离 0/0/0+rig[028] 0/0/0/0+房簇 23/23**。残余 47 格全 ghost（37 继承+10=原版 KillTile 级联清 type vs 保留输入 ghost，非内容通道备案）。pass49 接线=P 批已落（R 见 WorldGen.ts 被外部改动+并行未重复做，无缺口）。工具 _uwp7-9 族。oracle 同步清单 26 条。
621	
622	**★ P 批墙家族横扫（2026-08-17）**：#46 神庙四根因（**主=房间链方向三元反→整庙镜像平移 58 格**+dest 环 4 掷/迭代+祭坛 Place3x2 中心锚系曾 1000 次全拒+幽灵保留）四通道 28k→1.3k（掷差 0.05%）；#47 蜂巢四件（主=**FrameOutAllHiveContents 整段缺**（每墙86格 1×Next(0,3) 每巢数千掷）+托台现场+honey 恒置+wall244 双门）24k→17.9k，**残余 +448k 掷定位到隧道 t#13 段悖论（流位精确 287,541，需 CreateHiveTunnel 出口探针）**；#67 countTiles 重写 1:1（**CountedTiles 只登记非实心格**语义），掷差 +3,913 未动；#39/#41 判无罪（纯级联）；**pass49 转岩浆接线完成**（H 备案清偿，World.genWaterLine/genDungeonExempt）。[055] 墙债 144,890→113,923（余 96.8k=#28+#32 另案）。**已定位未接：GenState.canPlaceStructure 缺 GeneralPlacementTiles 扫门**（原版 StructureMap.CanPlace 黑名单 28 tile）。方法论坑：gs 克隆被 pass 自身污染（每重放独立 cloneGs）；IL 注入必须独立 app 副本（共享沙箱被并行覆盖）；三方静态一致仍分叉=求值序/坐标系/漏段→直接上探针。
623	
624	**★ Q 批 Dungeon oracle 同步（2026-08-17）**：§5 八件中 oracle 六件同款 bug（曾同源转录）全同步+双源核对；**真值驱动三大新发现：①GenerateDungeonStairs 整段缺（两侧都缺！普通世界恒 TRUE——入口 45° 阶梯 ~3898 砖+墙丢失，DungeonUtils:1222-1310 已全量转录进 oracle，JS 仍缺）②Bounds.UpdateBounds 缺（JS 也缺）③DgSpikes 42f*(W/4200) int 除法潜伏 bug**。残余定位到一格 (207,876)（oracle 墙9/vanilla 无）→pit 尝试翻转→尖刺流错位→W 段 15 变体锚错位（96↔97 ~45k 墙差=#32 特征真身）——下一步=DgHall 墙带 prot/f17 门在 (183..215,855..915) 逐格对账（Tier B"dungeonL 微差"深层根因）。oracle 留 env 门钩族（DG_ISO/DG_W_SEARCH/DG_PIT_TRACE 等）+段头终态注释；源码快照 /tmp/dgsrc/（Terarria1456 目录被并行会话移动过！）。金标未写。oracle 掷 232,392 vs 真值 243,293（-10,901，缺楼梯段为主）。
625	
626	**★ M 批地狱复验（2026-08-17）："全级联"证伪+三修**：LavaCheck 地下沙漠分支（墙187/216 7×7→岩浆，沙漠底岩浆池）/QuickWater tilesIgnoreWater（boulder 族 138/**484**/664/711-716+546——484 滚动仙人掌活性在沙漠大量存在，H 批只证了 138）/HellFort 幽灵 type 6 写点（active(false) 保幽灵）。效果：mid-world QW 残差 894→0、rig[028] 38k→17.5k、隔离 22k→7.4k。**IL 探针真值链三定标全中**（liquidType 导入/QuickWater 后全图 0 差/UW 段掷数 14,266,081=JS 精确）。**残余全在 AddHellHouses 内**（家具 +22,120 掷/挂画 +3,626=拒绝率症状；房1 内 17 墙差而房2 净→写语义/occ 判定，掷序无罪；相位钩+五元组跟踪切入点已备 /tmp/sw-uwp/ + HellFortPass.phaseMark）。Cecil 坑：嵌套类型需递归枚举才见 <>c lambda；跑前 rm wld；换档前 pgrep（01:11 撞车实录）。oracle 同步清单 20+条。
627	
628	**★ O 批树木专项（2026-08-16）——用户可感知最大差异修复**：12345 树 49→**193 vs 原版 194**（-75%→-1%）；9293480 63→182；隔离 163/161(+1.2%)。主根因=**EmptyTileCheck ignoreID=20 语义整体缺失**（净空盒容忍 CommonSapling+装饰+倒木，cs:31611-683；旧实现任何实心即拒→杂草/倒木杀死 61% 树位）+侧格门被历史半砖修复误扩（-74）+墙门 11→27+FIT 9→12+干身/根部掷骰结构三件。**陷阱实录：ignoreID 形参是原版 id——直接对内部 id 集比较会使 saplingMode 恒 false→净空全容忍→树爆炸 8×(1288 棵)；形参用原版集/格内比较用内部集**。灰烬树 480/97 哨兵不动。管线残余=输入级联（#19 后链条累积），TreePass 自因仅 ±1 列邻移对。工具 _treeparity 族五件。oracle 同步清单 20 条。
629	
630	**★ N 批尾部1（2026-08-16）**：Lakes 清偿（根因=掏腔后幽灵 type∈{59,60} 的 SpreadGrass 即时传播，rig [030] 归零）；Pots 三修（实现体从 WorldGen.ts 外提 PotsPass.ts/平台族 tileSolid 差集恰 9 类/x·y 采样上界独占——掷差 -103 万→-26 万，残差级联）；Vines 审计 1:1（+669 掷=0.4% bottomSlope 锚漂，结构零差）；Stalac 掷数 6,015,909 **精确**+宝石树零差。**新基建：dump 外五通道真值 bin**（liqtype/slope/half/frameX/frameY——van_x86_g 不含，rig 自动采管线时点真值 /tmp/sw-t1-*.bin+loadExtra 回灌；隔离重放还须预置 GenSolid 时点翻转态）。定标：Lakes718/Vines174k/Pots228 万/Stalac601 万。oracle 同步清单 17 条。
631	
632	**★ K 批 CaveWallVariety（2026-08-16）：隔离归零+墙债家族浮出**。根因=**Actions.PlaceWall 每铺一格耗 ~5 掷**（置墙后 SquareWallFrame+四邻，中心格 WallFrame resetFrame 掷 Next(0,3)，墙21 加掷——框架耗掷族第 5 次命中：沙漠/岛/大理石/腐化/洞穴墙变体）；原版 pass56=828,736 掷 vs 我们 159,069。修=CaveWallsPass 外铺 OuterOutline 1:1 逐 datum 序+frameDraw。隔离重放 wal/act=0、足迹 109,792 全等。**新发现：pass56 前存在 ~145k 上游墙债**（经 wall==0 门继承进来——#35-55 区间另有铺墙 pass 漏 frame 掷，同族根因，下一轮墙家族横扫）+[067] Cave_Walls 30k 自债。Mono.Cecil 逐迭代注入工具链已在案复用。oracle 同步清单 16 条。
633	
634	**★ L 批腐化链+蘑菇（2026-08-16）：双 pass 掷数精确+四通道 0**。#29 单根因=chasmRunnerSideways 壳墙写入须走 **PlaceWall(3,mute)**（cs:75508→75189：仅 wall==0 才写+每成功写经 SquareWallFrame 中心格掷 1×Next(0,3)）——JS 裸写 wall=3 零掷=**pass 总掷 -179.7 万**→卫星裂隙集合错位（11 vs 13 球）；修后 5,128,077 精确+0 差+8888 泛化 5,361,723 精确。evilZones 归位 [748,1196]+[834,1219]。#20 蘑菇两修：KillTile 生成期 type=0（幽灵 70 级联）+竖桥 quirk 补写坐标=(被放格列,锚y±1) 非锚 x→1896→39（全 ghost）。**方法论新发现：liquidType 输入通道**——dump 不含液体类型，岩浆破封门用水代会假造 700+ 假差；快照库 /tmp/sw-mush-liqtype.bin（rig 自动采）。附带：Lakes 自有小债 1202（59>60@y279）；Dungeon 在正确输入上重测 8.8k→11.3k（归 Dungeon 案主非回归）。**框架耗掷机制第 4 次命中（腐化壳墙）——PlaceWall 凡 mute:true 都带 SquareWallFrame 掷**。oracle 同步清单已 13 条。
635	
636	**★ J 批 slab-77 终局（2026-08-16）：[021]Marble→[027]Webs 管线全零**。根因=checkStalactite 击杀类型门（原版 cs:39146 只 KillTile type==165 格，JS 曾无条件双杀 pair→板格被抹→SmoothSlope mask 12实心/4半砖分叉→门掷差+15）；辅修=killStalactiteTile 级联 SquareTileFrame 列主序+frame165 inactive 清 half/slope。**反例存档：ResetToType 不清墙**（Tile.wall 是独立 ushort 字段不在 bTileHeader——误改会打坏 biome1，已试错回退）。效果：8/8 biome 逐 slab 掷数全等（509/409/642/475/716/539/544/777）；双种子隔离四数组 0/0/0/0；**管线 [021]→[027] 全部 new=0**（[Granite]/[Dirt_To_Mud]/[Shinies] 边界塌缩）。残余：#20 Mushroom 1896 格继承（小）+#28 Underworld 自有缺口（H 案）+CaveWallVariety+Dungeon(Tier B)+尾巴。rig=_d25slab（TraceRNG callsite 逐掷+__swSlabProbe 钩）。granite 9293480 隔离计数差 -703003 备案不阻塞。
637	
638	**★ I 批 DirtToMud+大理石花岗岩（2026-08-16）——framed-skip 近似根因**：#24 根因=**TileRunner framed-skip 谓词近似**（曾 framed&&!decor，原版=active&&tileFrameImportant&&!tileCut，cs:77217）——tile 484/485（滚仙人掌/蚁狮幼虫）frameImportant 且 tileCut→原版**不**跳（耗 dist 掷可被泥覆盖）→ DirtToMud 起**缺 4675 掷**=泥流全错位。修=精确 383-sheet 集（frameImportant 411−tileCut 41）。**双种子隔离字节级完美**（掷数精确+四平面 0）；Silt 同完美（88k 纯级联）。大理石花岗岩大塌缩（SquareWallFrame 中心格掷/花岗岩 CA 稀疏交换 tAct=1/SmoothSlope 1:1+坡感知实心拆分/钟乳石生命周期五件）——花岗岩隔离 typ 31995→**7 格**（掷精确）；biome 1 全验证（IL 探针逐列轨迹比对）。**唯一残余自因=大理石 biome2 slab77 板内掷混合（van48/js63，放大 64k）=全局关键路径，J 线猎杀中（/tmp/sw-marbleprobe 沙箱就绪）**。CaveWallVariety 124k wal 独立债（CaveWallsPass.ts，他域）。
639	
640	**★ H 批 Underworld（2026-08-16）：确定性已清，残余全级联**。定标原版=14,451,380 掷（passchain 真身在 /tmp/sw-num4/home/）。修 4 件：①**QuickWater(-2) 接线**——"两侧一致省略"证伪=**自洽假象**（oracle 也漏，云湖排空+岩浆板压实 dump 实证；LiquidSim.quickWater 本就 1:1）②落水越 waterLine 转岩浆（Liquid.cs:177-190 整段漏接）③633 灰烬草 for 条件每迭代重掷（~27.6 万掷，曾每列一掷）④AddHellHouses 后三环（家具 1000 环/挂画/旗帜吊灯，+44,325 掷，原版读锚点格 bug 1:1 保留）。rig liq -34%；**隔离重放证残余全级联**（S4 柱扫+HF 拒绝采样读 QuickWater 后岩浆面，形状依赖 #21/22/24/26 污染的中层液体）——无确定性掷序错位。**"两侧一致省略"=自洽假象新机制**：JS 和 oracle 同漏一段会互检全绿却双错原版——此类注释一律重验。遗留：pass49 沉降同款转岩浆未接线（WorldGen.ts:383 禁改无法传 waterLine，备案）。工具 _finduw/_underiso/_uwtypes。
641	
642	**★ G 批双债清偿（2026-08-16）**：#19 装饰二阶**归零**（act/typ/wal/liq 全 0+掷数 319318/319318+pass 末指纹逐位相等）——根因=①SmoothSlope 曾按"哈希无关"省略（坡面是下游门禁一等输入：酥化 SolidTile(below)/底锚 SolidTile2/PlaceTight 锚全吃坡位）②PlaceTile(187) Check3x2 材质击杀（style29-34 底须沙族，404 化石豁免，918 掷缺口起点）。浮空岛**归零**（#23 四通道 0；x2369 云恢复/x2337 二级干正确拒）——根因=①CloudIsland 墙 73 循环 SquareWallFrame 掷（同框架机制，7109 掷曾缺）②CloudLake 云 puff 段整段缺失（~76 雨云格）。下游 #69 岛屋/#82 栽树再塌缩。
643	**★ 塌缩后全局图景（104 边界 34 全零，残余自因可枚举）**：①Underworld 242k/202k/40k/289k liq（岩浆未满+灰烬层，猎杀中）②DirtToMud 158k typ（Silt 88k/Shinies 98k 疑级联，猎杀中）③Marble/Granite 78k+74k wal（猎杀中）④CaveWallVariety 125k wal（下批）⑤Dungeon 45k wal（Tier B 线）⑥尾部队 15-30k（Lakes 后/微群系/藤蔓/蜂巢/神龛/Webs）⑦POST-FINALIZE 959k typ=finalize 清幽灵口径差（非丢失）。POST-FINALIZE 是测量口径非债。
644	
645	**★★ #19 FullDesert 根因猎杀（2026-08-16 F 批）——第三类通用掷骰陷阱：框架调用耗流**：`Framing.WallFrame(i,j,resetFrame:true)` 每个有墙非大幅墙格掷 Next(0,3)（墙21 再 Next(2)）——真服务器二进制反汇编实证；SquareWallFrame 九邻域仅中心格传 resetFrame（≤1 掷/调用，cs:80943）。DesertPass 曾把 SquareWallFrame 全省略=漏 ~25 万掷（原版 319,318 vs JS 67,935）→簇散点流错位→距离场独立→187/216 墙带同分布重采样=表观"对称互换"。**定罪技术（复用价值极高）：流指纹终极 oracle**=passchain 第 6 列（pass 末 Main.rand FNV），暴力定标原版 pass 末态到精确掷数，迭代修复以此为靶。塌缩：#19 126k/78k/84k/1405→9613/7448/**0/0**（化石 4653/4653 全重合）；#25 Silt 墙门归零；#70/#20 近净。**⚠️此机制全局有效：凡调 SquareWallFrame/PlaceTile 族的 pass 都要查漏掷（placeWall/wallFrameDraw 已入 DesertPass，其他 pass 逐个核）**。残余=装饰二阶（冰凌锚点±2 移位/place485 等+缺 918 掷，同族=装饰放置路径，靶点明确）+oracle 侧需同款还原（其 Sub-A 放置另有 bug：重试落 x≈3500，vanilla 首掷 combX=2447）。工具：tools/_deserthunt.test.ts（隔离重放+指纹+化石）、_findn.test.ts（指纹→掷数定标器）。
646	
647	**★ 活树/海洞转写债清偿（2026-08-16 D 批，四平面 0 差验证）**：OceanCaves 修 2 处——①右洋双掷（cs:15249 首 Next(55,95) 被 i==1 覆写但**耗流**，JS 曾只掷一次=右洋蠕虫全错位）②竖井断轴门=genSolidType 族判定非 active（海草不挡轴）；8888 种子 037 dump 四平面归零（修前 12k+）。LivingTree 修 3 处——核心=**PlaceTile(187) 石堆一致性链全缺**（SquareTileFrame→TileFrame→Check3x2 残件清除，JS 残件永生树冠多 187 残格）+门/椅/织机尾帧接线+MakePassage 地狱门 lavaLine→h-200；9293480 的 042/043 dump 归零。**"192 vs 191 棵"主体=继承分歧**（JS 缺 x2369 云层→浮空岛 pass 债，非活树错——新记一笔债）。**oracle 同步债仅 1 处**：PlaceTileGen case 187 补 Check3x2 链（否则 livingtrees 差 1 格），文档 docs/worldgen/livingtree-oceancave-js-audit-2026-08-16.md + 重放工具 tools/_ltaudit.test.ts（LT_VAN_REPLAY/LT_OC_REPLAY）。"掷了但被覆写仍耗流"是继"先掷后用"后第二类掷序陷阱。
648	
649	**★ 收敛矩阵真值库建成（2026-08-16 C 批）**：/tmp/vserver/ 38 个原版 .wld + matrix-anchors.tsv（39 行 12 列锚点）；任务矩阵 15/15 全成（小 133s/中 207s/大 287s）。**邪恶对照链路**：SW_EVIL 在 Tier B 的 TerrariaServer.passchain.exe（/tmp/sw-num4）非 Steam 二进制——克隆独立实例 /tmp/vserver/evil_srv（HOME 隔离+7796），验证**零 RNG 扰动**（3 对照 isCrimson 精确=请求值且其余锚点与自然版全同=邪恶覆盖发生在 crimson=Next(2) 结果处不动流）。**关键锁死**：全部 38 世界 worldId 恒=UnifiedRandom(translateSeed(seed)) **第 18 个样本**（含非数字种子 crc32）→ translateSeed+UnifiedRandom 位级正确性间接全锁。moonType 跨尺寸可异（WorldId 抽样在尺寸消耗前、moon 在后）。oracle 交叉验证 18/18。运维：zsh `local status` 只读撞名+double-fork kill 卡死的加固版脚本在 /tmp/vserver/genmatrix*.sh。
650	
651	**★ E 批对账诊断（2026-08-16）：全链分歧收敛到 #19 FullDesert 单一自因 bug**。rig=tools/_contentparity.test.ts（SW_PARITY=1 env 门，钩 RNG.reseed 按**槽名**映射 vs /tmp/sw-num4/van_x86_g 原版 dump；槽名映射法抗并行改序）。结果：**#0-#18（Terrain→MudCaves）整段逐位全等**；31 内容 pass 实质对齐（14 严格 0，含当日新落地 #68/#70 即刻对齐）；**#19 沙漠=唯一可证自因分歧**（126k typ，签名 W187↔216 对称互换 ×35k+396/53 边带互移→DesertHive 簇距离场分层/SandMound 边形，猎杀代理已派）；**其后全级联污染**（DirtToMud 155k/Silt 89k 与 #19 墙门直接耦合/Shinies 118k/Underworld 245k+岩浆未满/大理石花岗岩/Dungeon wal 45k）——修序=#19→#21/22/28→复跑 rig 看塌缩，塌缩后仍 >1k 才进下一批。备案量化：#97 尾沉降=7072 格液体；自造装饰段=790 格；finalize 清幽灵=+1.25M ghost（非丢失）。报告 docs/worldgen/content-parity-vs-vanilla-2026-08-16.md。
652	
653	**★ 内容区缺口清零（2026-08-16 A 批验收）**：#68 UndergroundJungleTreesPass（160 行；与 GrowTree 三处掷序差异=num4 先于 num5/根三变体独立掷/树冠 Next(8)；Tiles_5 帧表共用、growTrunk 不共用）+ #70 QuickCleanupPass（162 行五子段；**台账勘误：墙 187/216=砂岩/硬化沙天然墙非大理石**；段 b 的 Next(4,7) 在 for 条件内=每判定一掷含失败）+ OceanCaves 归位（gravitatingSandSlot 包装=引力沙→reseed→海洞，gravitatingSandPass 导出体未动保 checkpoint 直调）+ Piles 归位（Traps 后）+ **自造"丛林表面泥化补偿块"删除**（探针实证 62.7%→55.7%=runner 原生覆盖才是原版；jungleCoreX 孤儿写入连带清理）。**零下游流移位**（每 pass 重播吸收，变化全在世界状态）。清点台账 65✅/3🔀/2❌→**69✅/1🔀(备案)/0❌**。checkpoint 前后一致（dungeon 红=Tier B 既有债）。GenSolid.ts:44 头注过时留待顺手清。
654	
655	**★ JS 多尺寸化完成（2026-08-16）**：World.worldSizeFor/GenConfig.size→SIZE_DIMS 派生、UI 三档→worker/主线程全链接通；TreePass randomizeCaveBackgrounds 三尺寸 1:1 + **修真 bug：randomizeTreeStyle fix0 传临时拷贝致 style0→4 翻转从未生效**（掷骰流不变值错）；GenState 增 caveBack 族字段。验证：(ws,rl) **23/23 精确**（小 18+中 3+大 2 种子）+ treeX/caveBackX/样式族 **7/7 逐值相等**+4200 流零位移回归 ✓。中 32-84s/大 76-157s 全管线冒烟。**oracle 侧 treeX 区间我的算术错已修**（6400:[857,3417)/[2988,5548)、8400:[840,3360)/[2940,5460)/[5040,7560)——真实 .wld 落值佐证；区间不动流位故锚点本就有效）。遗留：BiomeBackground 渲染仍近似重建 caveBackX（真值在 gs 但 World 无字段可接）；中/大逐 pass 金标待 oracle 扩展；8400 worker 路径（~300MB TileStore）浏览器未压测。
656	
657	**★ 多尺寸原版锚点（2026-08-16 采集，/tmp/vserver/{m,l}*.wld + /tmp/msize-report.txt）**：中(6400×1800) seed2222=(493,661) seed9293480=(493,811)；大(8400×2400) seed2222=(649,883)。中尺寸两 seed groundLevel 同=493=1800×0.26 clamp 精确值（num6 均触顶）；大尺寸 ground/rock 随种子（旧锚 604/916）。WldParser 对中/大世界**零改动原生通过**（v319 同版本、列优先解码尺寸无关）。worldId 跨尺寸同种子一致（seed 派生）✓。TerrariaServer 中世界 ~100s/大 ~115s（低负载时）。后续 oracle 多尺寸对账=参数化 W/H 后逐 seed 对照此表。
658	
659	**★ num4 结论修正（2026-08-16 本会话）**：真因=每 pass 重播（见上文 Tier B ★★ 条目），非"陈旧缓存二进制"——本会话的 9/9 种子命中实为吃到重播修复后的共享 oracle。经验教训仍有效：负载期对账必须 fresh build + 源码 mtime>二进制 mtime。oracle 诊断钩子已清（TraceCols=Tier B 工具保留）。本会话另落地：oracle 第 4 参 size 多尺寸化（三尺寸 tree/cave 分支+num10 门），中/大锚点 3/3 精确（493,661)/(493,811)/(649,883)。
660	
661	**★ 原版直连工具链（2026-08-13 深夜建立，种子等价决定性武器）**：
662	1. **无头原版世界生成**：`cd "$HOME/Library/Application Support/Steam/steamapps/common/Terraria/Terraria.app/Contents/MacOS" && ./TerrariaServer.bin.osx -world /tmp/vserver/s<seed>.wld -autocreate 1 -seed <seed> -port 7799 -players 1 < /dev/null`（macOS 无 timeout，用 `&+sleep+kill`）。服务器生成 ≡ 客户端（9293480 头部 337/571 完全一致）。
663	2. **ilspycmd 11 已装**（~/.dotnet/tools/ilspycmd），对真 exe 反汇编 = 权威（磁盘 Terarria1456 反编译与 exe 有过差异史——GenerateWorldSurfaceOffset 我曾把 drunk 分支误读成普通分支、乌龙"修复"后回滚：**普通世界=else 分支 Plateau Next(0,7)/Hill·Dale Next(0,4)/Mountain·Valley Next(0,2)==0，6/3/!=0 长爬升表是 drunk/getGood/remix 专用**）。
664	3. **wld 头部=掷骰产物对账表**：worldId/moonType/treeStyle[4]/caveBackStyle[4]/iceBack(Next4)/jungleBack(Next2)/hellBack(Next3) 逐值可比。**9293480 全部与 oracle 一致（worldId=733020316 等）→ Reset 流与原版位级对齐实锤**。头部 dungeonX=DungeonCrawler 回写值（最高房中心 X）≠ Reset dungeonLocation（440 vs 658 之谜即此，handoff 文档语义正确）。
665	4. **Mac 版架构**：`WorldGen.genRand`/`GenBase._random` 是只读属性→转发 `Main.rand`（单流）；dotnet 宿主反射触 Main 静态构造会因 ReLogic 合并无 type-forwarder 而炸（TypeLoadException），反射调用真生成代码此路不通；只能 GetMethodBody/IL 或 ilspycmd。
666	5. **未解之谜（2026-08-13 午，变体扫描负结果——逻辑绝对化，转挂起）**：10 变体×6 种子网格全不中原版 (ws,rl)；且 2222 的 ws=287 **只有基线（continue=Next(0,3)==0、步进 Next(-2,3)）能保持**——续走条件/步进被反向钉死=我们的实现。结合 num3 全程匹配（num4 若多耗一掷 num3 下列必漂）⇒ 模型内零自由度，矛盾绝对化：**静态分析穷尽，需 vanilla 运行时插桩（当前被 Mono 合并架构阻断）**。悬案影响有界：rockLayer 偏 ±(12..96) 格（±6 量子），下游自洽。**重启条件**：新工具（如给 TerrariaServer 塞 Mono profiler、或 Windows 版 exe+dotnet 反射不受合并阻断）或新线索。Δrl 七种子：+12/+24/-16/+24/-84/-30/+96。**配套坑教训**：后台任务的 env 前缀会丢失（三次失控全链循环孤儿烧满核）——批量跑必须**脚本文件内 export**；grep 管道写文件 4KB 块缓冲（--line-buffered 或脚本内 print >>）；`dotnet run` 每次改文件全量重建（负载下 10 分钟）——批量用 runfile 二进制直跑（~/Library/Application Support/dotnet/runfile/caves-oracle-<hash>/bin/debug/）。
667	6. **现场警告**：金标过期（表回滚后未再生）+ checkpoint 会红；WldParser.ts 被我加了 caveBackStyle/iceBack 捕获但**读序错位**（后续 dungeon/spawn/ground 读歪）须按 WorldFile.cs:1256-1269 修序；oracle 留有 env 门诊断钩子（EXTRA_ROLLS/DROP_TAIL3/NUM4FLIP/RESETVALS 打印）收尾时清；JS TerrainPass/WorldGen snowBG 注释更新过、行为已回滚原样。
668	
669	**★ 原版漂移地图（2026-08-13，seed-parity 全图报告，当前最高优先级线索）**：完整 generateWorld vs golden .wld：tile 差 51.6%/wall 29.4%/liquid 9.3%，但 TOP 差异**全是成对对称交换**（1→0×327k ↔ 0→1×247k、0→59↔59→0 等）=整体空间错位指纹；地表剖面相关系数 **0.137（≈噪声）**、首个分歧列 **x=0**、天空样本 0→189（云）=原版有云我们没有。**判定：JS≡oracle≠原版的偏差在 Reset/terrain 层就存在**——Reset 侧别锚点匹配（side-check 过）但 terrain 游走流错位 → 下一目标 = 审计 caves-oracle.cs Reset 段（:78-114 附近转录）+ TerrainPass 对 cs:11159-11526 的位级忠实度（找缺掷/多掷）。#32 Dungeon oracle（18k 行子系统）降级：改用"csproj+垫片直接编译反编译源码"方案待稳定窗口独立做（多文件 dotnet run 不支持 CS5001；XNA 面仅 Vector2D245/Point157/Vector2 38/Rectangle14/MathHelper4 可垫片）。35 checkpoint 含 dungeon 占位双种子全绿（占位=slush 同态）。
670	
671	**★ 2b 收口（2026-08-13 凌晨）**：terrain→beaches **34 checkpoint 双种子全等**，oracle 输出与金标逐字节一致。corruption/lakes 九处 1:1 修复（要点：侧裂隙 vy2 `int(-10,9)`=Next(-10,10)；crimStart 三处裸 double 上界 `x < px+R/2` 勿 Math.floor；CrimEnt 锚=壳群行走后 startY-累计抬升；SpreadGrass 传 T.DIRT 非 0；flag3 quirk 每轮重试勿短路；Lakes solidAt=active&&tileSolid）。**dungeonLocation 双字段已拆**：gs.generatingDungeonPositionX（DungeonCrawler.cs:346 初值/:394 回写=最高房中心 X）≠ Reset 期 dungeonLocation，金字塔回避带（cs:15447）读前者——[1263,1516] 分叉窗口消除。#32 Dungeon oracle 转录（~2000 行 DungeonCrawler 1:1）延后至 DungeonPass 会话收口后独立做，期间 world-final-hash 终态门兜底。多会话并发期回归验证是移动靶：单跑绿≠批跑绿，归属判据=单文件复跑。
672	
673	**★ 165 镜像修复+幽灵悬案（2026-08-13 午后，已破案）**：gem 会话昨午在 JS 侧落地 AddTileVariance 装饰放置但 oracle 未同步 → **每次 165 命中流偏移**（JS placeTight 带 Next(2)+Next(3) 两掷+锚 py+(flag?-1:+1)，oracle 旧码零掷锚不同）→ 级联 34 红。我已镜像 placeTight 哈希语义进 caves-oracle（PlaceTightMirror：shimmer liqT==3/幼虫 231 门、两掷恒耗、1x1/1x2 钟乳石格效应）+ 金标再生 → **caves-checkpoint 自有两用例双种子全绿**（type/flags/liquid + 沙漠 wall）。**"剩余 6 红"已破案=搭车测试**：caves-checkpoint.test.ts:34 `import { fnv1a } from './pass-hash.test'` ——**导入 .test 模块会连带注册其 describe**！pass-hash 的全管线用例（自有旧金标 terrain-*.json，昨 18:09）在 caves-checkpoint 运行中搭车执行并因期望过期而红——非真分歧（幽灵逐格对拍 count=0 actMismatch=0 实证两侧 corruption 网格全同）。**教训：vitest 里从 .test 文件 import 工具函数=整个测试文件搭车执行**——工具函数须放非 .test 模块。pass-hash 金标再生归其属主会话。oracle 留有 env 门钩子（EXTRA_ROLLS/DROP_TAIL3/NUM4COND/FLIP/STEP/TERRAIN_ONLY/GHOST_DUMP/TRACE_COLS/RESETVALS）收尾时清。
674	
675	**★ 并行会话协调名单（2026-08-13 午间更新）**：⑤**gem 会话正在活跃改 DesertPass/caves-oracle**（13:21/12:31 mtime，DesertHive 装饰放置落地中）——当前 deserthive/desertdone/mushroom/marble/granite/islands checkpoint 单种子红=其中间态，**勿抢修**；#32 Dungeon 需 caves-oracle.cs 共享，等其收口后再启动。num4 悬案挂起（见 §5）。：①祭坛会话=已收尾（CorruptionPass 三门+去吸附，零 RNG 扰动）；②地牢调查=我方只读代理已收尾（结论：淹/削顶/埋主因=Lakes/Dungeon 倒挂已由 2b 修；Lakes 腔壁壳两处 1:1 走样已转发 2b；贴水塔顶半砖唇缘=原版语义勿加排除）；③**宝石悬空会话=在制 CaveWallsInEnclosedSpaces（#67, cs:17819）**——地下自然墙全缺→贴墙晶簇悬空；落地后是我第三轮（#35/#64/#67）转录基底；④**新立案三条（他会话调查中）**：宝石浮空（或涉 ExposedGems/TileRunner 幽灵）、海中半砖沙散布（疑 HalfBrickPass=SmoothWorld/Waterfalls 区，#53/54 未转录）、地狱建筑分布不对（涉 HellFort/AddHellHouses，2b 刚做 #28 Underworld 时保持了 JS 独立槽）——三者落点都在我 checkpoint 链（截至 #34）之后或边缘，等对方结论落地再对账，勿抢动 HalfBrickPass/HellFortPass/ExposedGems。
676	
677	**★ 自创"优化"是移植 bug 头号来源（2026-08-12 祭坛案，已修复收尾）**：裂隙尾祭坛我们自加"落点吸附到地表"——原版是纯随机点+IsTileNearby+Place3x2 重试≤10000 次（cs:76200-76275, Place3x2@76234），吸附恰好把祭坛钉在后续竖挖裂隙必经之路上→残片祭坛放大器。同类前科：底锚定绘制(树缝)、水面正弦扰动(伪需求)。**铁律：对账发现"原版没这么做"的逻辑一律删除，不做"改良"**。裂隙挖空三重门已补：CanEvilReplace(=地牢砖/裂砖/地牢墙不可替换，函数体全文)+type!=31/22/204（cs:76187-91）；祭坛 26 不在原版保护名单→残片本身是"原版风格产物"，吸附移除只是把出现率降回原版水平。修复零 RNG 消耗，种子流不动。
678	
679	**★ 管线真实序确认（2026-08-12，改序前必读）**：WorldGenerator.cs:447 `_passes[PassResults.Count]` 逐个执行——**执行序=注册序，无 weight 排序**。1456 全 105 pass 注册序（WorldGen.cs AddGenerationPass 顺序）：…14 SurfaceCaves → 15 WavyCaves(dontStarve 专用，普通世界零消耗空跑=不构成偏差) → 16 IceBiome → 17 Grass → 18 MudCaves → 19 DesertBiome → 20 GlowingMushroom → 21 Marble → 22 Granite → **23 FloatingIslands** → 24 DirtToMud → 25 Silt → **26 OresAndShinies** → 27 Webs → 28 Underworld → 29 Corruption → 30 Lakes → 31 Slush → 32 Dungeon → **33 MountainCaveOpenings → 34 Beaches** → **35 Gems** → 36 GravitatingSand → 37 OceanCaves → 38 Shimmer → …。**我们链(与 oracle 同)有 4 处真实序偏差**：岛在蘑菇/大理石前、Ores 太后、Gems 捆绑 Lakes、mcopenings/beaches 紧跟 SurfaceCaves(应在 Dungeon 后)。19 checkpoint 中 terrain..surfacecaves 在原版序下仍有效，mcopenings 起全在错误流位置——这是 seed-parity 对真 .wld 仍红的结构性根因。修正须 JS 链+oracle 同步改序+金标再生（caves-oracle.cs 共享，串行）。对齐文档：docs/worldgen/vanilla-pass-alignment.md。
680	
681	**★ BBBB 批 oracle 同步（2026-08-18）：x86 43/43 全绿 + 再生彩排**。11 项镜像落 caves-oracle.cs：OOO①门区 ClearEverything 补 typ=0（12 写点）/OOO④ lihzahrd 零掷/OOO⑤ Pa 攀爬链式/**E9 CanHit 三重终止**（③踩格 do-while 条件+②邻对 slope/half 门+y 钳 H-40+灯笼吊灯裂纹砖门——Lights 段主债，DGFLOW 6889fc42→**f890f8a6** 命中）/SSS banner 帧/TTT 蜂巢四连写/VVV settle 尾删 WaterCheck/YYY-a 485 样式轴 frameX+484/751 帧组/YYY-b LsKillTileGen 尾 SquareTileFrame 级联（Check2x2 去 713-716/箱族 ghost 豁免/CheckSuper frameX÷36）/连带① Cavinator2 终止步速度 2 骰（mcopenings 债主）/连带② 祭坛底座 s111 坡位门（4 坛错位根因；3240 候选序列取证）。**槽↔检查点哈希直比法**（/tmp/bbbb-x86hash.mjs 口径：active 掩码 typ+LE16 wal+u8 act/liq 现算 FNV，43 严格序名）+逐事件 trace 对拍（DG_LIGHTS_TRACE/ALT/__swP32）。链侧 settlePart2ChainSync 补 VVV 门（tests/）。彩排（/tmp/golden-bbbb 零写入 tests/golden）：shimmer 5/5 全绿（含 shimstate bin.gz 状态恢复）；world-final 四通道全变（预期）；**残余=跳段区 10 名红（首差 statues，ZZZ 在途+oracle 跳段区旧债）=正式再生窗口前置**；oracle 尾段尚无 FinalCleanup 逐格 TileFrame 扫掷与 ShimmerCleanUp（WWW 域，锚=苔藓 10697/1358/⑭ (1049,412)(471,479)(514,535)）。并行会话三坑：/tmp 产物读写竞态幻影值（md5 复读排除）/半成品 src 炸 import/vitest import 副作用行混入（一律 "== seed" 行裁决）。详见 docs/worldgen/content-parity-vs-vanilla-2026-08-16.md BBBB 章 + /tmp/final-runbook.md BBBB 附录。
682	
683	**★ KKKK 批终局红基线（2026-08-18 21:14-45，三跑全量快照）**：36 败±1=①陈旧金标带 30 败（caves-oracle 13 文件 26 败 underworld 首差[12 探针 import chainCheckpoints 副作用重跑同一 describe，再生后整带同灭]+shimmer gems×2+world-final×2）→随再生消；②遗留探针 _hivehunt 1 败（/tmp/cs-hive.bin 缺失，再生前删/门控）；③并行会话在途 3（dual-key vi_2613 缺 tile 字段=items.ts 18:18/town-sitting shimmerTransparency=Game.ts 21:21 编辑中/dual-key 同会话）；④flaky 4（shimmer lightRGB·platform-hammer·lunar-final-audit 隔离绿；town-npc-damage=未播种 Math.random 齐射+朝向竞态，隔离 2红1绿）；⑤worldgen 真回归=零——spawn-tree-clear 活红木覆写登记树顶格(3095,771)系 CCCC 后 MicroBiomes §4.5 落位撞出登记表滞后（vanilla SkipTiles={21,467,226,237} 不含树干=原版语义覆写；修剪在槽90早于101 且只查活性），已测试侧白名单 v_383；src 记账=管线尾 type==TREE 修剪。HHHH 仍在改 caves-oracle.cs（21:29）——再生须等其终态；再生后 caves 首差 settle2/microbiomes=HHHH 尾段残余非新回归。tsc 36 错全在 tests/ 旧文件（GGGG 同象），src 零错为验收线。终局判据表在 /tmp/final-runbook.md KKKK 附录+对账文档 KKKK 章（含 /tmp/kkkk-extract.mjs 复跑提取脚本）。
684	
685	**★ JJJJ 批第二种子里程碑链（2026-08-18）：seed 12345 x86 106槽×8通道 dump 落地 /tmp/sw-slp/g12345 + 双种子对拍**。rig=sw-slp hs.exe 谱系（SW_DUMP_ALL+SW_HS_DUMP+SW_EVIL=1+arch -x86_64，端口 7794 guard，完整配方在 parity 报告 JJJJ 章）；**12345 自然 evil=crimson（s12345.wld）勿与 golden 12345世界.wld（corruption）混**。sanity：槽105 vs wld 八通道逐格 0 差（两格式假差：wld 不落非活性 type=幽灵 1,499,790 全在 act=0；lty 3=微光在 wld 折成水+shimmer 位 648）。**结果：0..31 双种子全绿（猩红支首绿）；12345 首差 #32 Dungeon (3405,154)，9293480 现 0..53 全绿**。12345 债（全种子特异，通用债窗口内 0 项）：①#32 Dome 残余静态至 52（A2037/T2260/W776/Sl8：旗91±341/319·挂毯240·墓饰241·瓦罐28×75·钟104×63+墙变体94↔7）②**Dome 柱致动位缺=vanilla 独有 234 格 JS 0**（(3399-3401,157)/(3425,157) 两根 BlockActuated 柱未置 wire bit5——8通道链新可见，FFFF 曾备案"不入四通道"）③JS 独有祭坛 1 座 (429,659) 6 格（AAAA 双案之一已自愈）④**#53 SmoothWorld 自差非级联**（扫描序首差 (20,532)=第一列、输入态 x<3153 全等 8 slope 差全在穹壳→12345 构型触发的 U 批四件外新触发；Hf5677/Sl31609 rock 带 24k）⑤Lt×1。mile8 旁路参 SW_M8_SEED/SW_M8_EVIL（默认不变）；pc.txt=第二种子掷流定标资产。
686	
687	=====FILE: leftover-closeout-4batch.md=====
688	---
689	name: leftover-closeout-4batch
690	description: 遗留收口四路批:召唤落位统一SpawnOnPlayer/红帽骷髅王真链(坐沙发非马桶)/EoW头部精确门/弹540星尘标记AI_103+402BFS孵化链/迅猛龙54表五档/冰面无输入腿行0/棉花糖IsFood帧2/QuickHeal虚空袋bank4
691	metadata:
692	  type: project
693	---
694	
695	遗留收口批（2026-08-18，用户"继续推进遗留"）。三代理+主会话修 1 个 tsc 残留。src 全域零错、149/149 回归。
696	
697	**Game 六件**：①物品召唤落位统一迁 `findOffscreenSpawnPoint`（500 次屏外寻点=SpawnOnPlayer 1:1；**史王无专属落位**——NPC.cs:81505 是"静默公告"组非落位分支；双子 126 随 125 位近似）；②自然出王补 HasAwoken（NewNPC Type==50 :81564 恒播覆盖 SpawnBoss 静默——BOSS_SPAWN_SILENT 表口径差登记）；③QuickHeal/Mana/Buff 虚空袋 bank4（猪猪罐/保险箱不参与）；④红帽骷髅王真链勘误：**夜间坐长凳 89 style43（frameX∈[2322,2358]）+ killClothier + 裁缝在场可击 → SpawnSkeletron(redHat) 于裁缝中心**（PlayerSittingHelper:84-95→NPC.cs:81193-81218，任务描述"马桶 1/40"不实）；⑤EoW/BoC 召唤门改头精确 [13]/[266]（身段存活可再召头=原版双刷语义）；⑥水蛭 117 出生尘改 spawnBurst 定向（opts 无 vx/vy 字段——tsc 坑）。
698	
699	**弹 540 星尘标记**（StardustMarkProj.ts 新建）：AI_103（:32272-32299）ai0 出场延迟=世代×10、静默→淡入 11t 孵化 NewNPC(localAI[0])→淡出 250 kill；**弹体恒静止**（UpdatePosition :19028 早退）；BFS 世代链（NPC.cs:44230-44314）：根深 Next(3,6)、分叉预算 Next(0,4)、角度奇偶π+(0.5−r)π/4+dir·π/4、距离 100+50r、**仅最后标记回填孵化类型**；塔变体（:44149）参数已备待迁。绘制 lighter+α3×、Extra_47 落点束（ai0∈[10,20]）。
700	
701	**渲染四件**：迅猛龙 faceAcc 登记引擎级（全仓无 face 装备槽系统——PlayerDrawLayers.cs:2801 偏移表已抄进注释）；**迅猛龙 54 表五档补齐**（ApplyItemPositionOffsetFromMount :50638 只管 54 非狼 52！风筝 IsAKite 25 件(4,−4)/悠悠球 21 件按身体行(10,−10)/(8,0)/(2,2)/**3542=星云烈焰非天空龙杖**(−10,0)/(10,0)/useStyle5(4,0)/default 按行；狼表 :1785 本就 1:1 无缺）；冰面滑行无输入腿钉行 0（**条件=slippy∪slippy2∪windPushed∪滚轴鞋且 !controlLR**——非 wet；:35818-35826）；棉花糖 IsFood 手持取竖 3 帧条第 2 行 Frame(1,3,0,1)、968=32×10 整图直画（GetItemDrawFrame:41896≡GetDrawHitbox:49192）。
702	
703	**教训**：faceAcc/头盔 addon 族在 PlayerDrawLayers 不在 Player.cs；"马桶红帽骷髅"是讹传（真链=坐沙发）；ItemCheck_UseBossSpawners 全族走 SpawnOnPlayer 无逐 Boss 落位特例。
704	
705	**E 批（2026-08-19，goal 驱动）**：①deerclops 冻结根因=漏位置积分（另见 deerclops-port）。②老鼠坐骑 55 爬墙落地（ratClimbVy 字段钉速+dropThrough 平台穿透，tests/rat-mount-climb 5 绿）。③FlexibleTileWand 全族 30 件（碎块魔杖 5324/5329/5330+MiteyTitey 5464+便携窑 5481+沙堡桶+侏儒+火烈鸟+珊瑚贝星+南瓜灯+礼物+书 149+暴露宝石六色）——表从源码机械提取（★桶按【弹药】合、option 各带 tile：large 154=647×7+648×3；`default(int)`=0；ByRow rows×per 摊平；1291→702 属 Medium 非 Large！），runtime=src/world/FlexibleTileWands.ts（单件族弹药=本体无背包门；cycleOffset 模容量负同余）+Game.tryPlace 头部分支+↑↓ 边沿循环（flexWandCycle）。A 级余：高尔夫车3611/虚空袋/涂层/公告盒编辑/成就页UI/坐骑槽UI/builderAcc 开关/gravDir/RerollVariation。
706	
707	**E 批续**：④RerollVariation 全链（TOWN_PET_VARIANTS 637/638/656 各 6 名逐字；roll=rand(6)；sheet 解析宠物前置分支——637/638/656 本无 TOWN_NPC_PROFILE 档（未收录注释），root 由 vid 映射 Cat/Dog/Bunny；18 张具名变体贴图 public/sprites/vanilla/{Cat,Dog,Bunny}_*.png 已在；variationIndex=-1=Default 图）。许可证二用 1:1（≤100 掷环+newNpcName+满血+PetExchange 粒子+成败公告）。A 级余 7：高尔夫车3611/虚空袋/涂层/公告盒编辑/成就页UI/坐骑槽UI/builderAcc 开关/gravDir。
708	
709	=====FILE: npc-ambient-sound-audit.md=====
710	---
711	name: npc-ambient-sound-audit
712	description: 怪物音效全量审计:HitSound/DeathSound已数据驱动;AI内嵌周期音缺口大(idle表32类/小动物/critter/闲话表全缺);蠕虫roar已修
713	metadata: 
714	  node_type: memory
715	  type: project
716	  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
717	  modified: 2026-08-18T11:42:55.814Z
718	---
719	
720	2026-08-18 用户报"地狱骨龙(骨蛇39)接近有音效"——**骨蛇掘地音 = AI_006 :52375-52395
721	周期性 SoundID 15 Roar**(间隔=玩家格距/40 钳10-20,排除 621/87/117/454/412)。
722	
723	**修复**:eowAI 分支(13-15)原已有(曾误播 dig 近似→改 eowDig 真轨,
724	Sfx.ts 加 'eowDig' → eow_dig.wav);**通用 wormAI(39 等)整段缺失**——
725	在朝向段前补 1:1 周期 roar。测试 tests/worm-roar-sound.test.ts 3 条
726	(39 roar≥3次/EoW 13 eowDig 双段链/排除表 412 静默)。EoW 断链自查
727	(:51886 头无下段即灭)=原版语义,测试须手工 wormNext/wormFollow 建链。
728	
729	**全量审计要点**(232 处 PlaySound 归类):
730	- HitSound/DeathSound = 数据驱动已全(vanilla-npcs.json 字段→wav 组)
731	- AI 内嵌**周期/事件音**是缺口重灾区:AI_003 闲话表(:57731 僵尸14/木乃伊26/
732	  吸血鬼29,7 等 1/N 掷骰)、IdleSounds 表(:91119 32 类环境声)、
733	  小动物声(:93415 鸭蛙鸟鸥枭)、AI_005 黄蜂 Item17、AI_009 秃鹫(4,9)、
734	  AI_103 沙鲨(15,4)+(14,542)、宠物受击表(:82259 15 款 player_hit_*)
735	- 佛系验尸法:grep 'PlaySound' NPC.cs 剔 HitSound/DeathSound 后按 AI 函数归属归类
736	
737	**全量落地批(2026-08-18 用户令"全部做掉")**:
738	- 新建 `src/data/vanillaNpcAmbience.ts` 三表(IdleSounds 47条/CHATTER 47type/CRITTER 23type 全量转录)
739	- Enemy.ambientSoundTick(fixedUpdate 尾):critter 段互斥 else-if 链 1:1;闲话仅 aiStyle3;
740	  IdleSounds wet 门查液体格;Game.playSfxWav→Sfx.playWavFile 直 wav(FILE_CASE_VOL 自带音量档)
741	- GameHooks.playSfxWav 可选(?.)=测试 mock 兼容(6 个 mock 无此键的旧测试零改)
742	- 事件音 12 落点:黄蜂 Item17(ai1==101 清零帧)/猪龙 Zombie_9 1/1000(floatEyeAI 头)/
743	  秃鹫沙球 ai0==200 Item5+弹31(AI_017 :24475-24506 曾整段缺失,顺带补攻击本体)/
744	  沙鲨 Roar_1 游弋+Zombie_7 出沙(bossAI_dd2)/蚁狮 Item_5/怒滚虫546 NPC_Hit_11 追击跳
745	  (chargerAI 整段补)/海豚 Zombie_109(ai3 计数器整段补 :23726-23741)/小精灵 Pixie 1/40/
746	  幽灵316 NPC_Killed_55/水蛭117 NPC_Killed_13+20尘(_wormSpawnFx 哨兵)/幻影龙454 Item_119/
747	  仙灵三处 roar 近似→Pixie 真轨(状态3@15t/状态5@15t/召唤脉冲1/30)/
748	  火星骑手 Item_39(438弹)+部件 Item_12(449激光)/星云脑消散 menuOpen→Item_8(审计#22 错音)
749	- 自制僵尸呻吟退役(Game.ts 只认 legacy key 全不命中,被 1:1 表取代)
750	- 测试 tests/npc-ambience-sounds.test.ts 6 条:三表锚点+wav 全在库(fs 直查防键拼错)+
751	  水蛭/幻影龙出生音触发;33 测试绿,tsc 0
752	- ~~遗留 6 项~~ → 子代理"补齐 6 项音效缺口"全落地(2026-08-18 续):
753	  宠物语音表(vanillaNpcAmbience:143-167+projTargets/GGame 接线)/TransformVisuals
754	  (Enemy.tryTransformTo 加 game 参,:81742-81749 gore99 三锚点核对✓)/老人自灭咆哮
755	  (Game.ts Roar_0,考古=骷髅王后 ai3==1 自灭非微光)/229 微光变体死亡 NPC_Killed_6/
756	  378 牙齿炸弹状态机(:30082/:30204 结构核对✓)/水花分液体 splashWavFile(顺带修
757	  honeyWet/shimmerWet 覆写 bug)
758	
759	**★Roar 键误轨大修(2026-08-18 用户报"地底蠕虫音全变 boss 唤醒咆哮")**:
760	- 根因三连:①WAV_MAP['roar']=['Roar_0','Roar_1'] 随机双轨——原版 boss 吼=PlaySound
761	  (15,x,y,**0**)=Roar_0(NPC.cs 16 处全显式 style0),蠕虫掘地=PlaySound(15,x,y)
762	  无 style=**Roar_1**(LegacySoundPlayer :366 签名 **Style=1 缺省**!)——一半概率播
763	  2 秒 boss 巨吼;②FILE_CASE_VOL['Roar_1']=0.25 是 case15 style4(沙鲨)调用点专属
764	  误登成文件档→真蠕虫轨被压 1/4 几不可闻;③缺 case15 **单实例互斥**(:825-841
765	  State==Playing 跳过)→多蠕虫 10-20t/tick 满响叠成音墙
766	- 修:WAV_MAP['roar']=['Roar_0'];wormAI(Enemy.ts:416)/destroyerAI(bossAI.ts,
767	  :50459-50473 补齐——原 AI_037 段缺掘地音)→playSfxWav('Roar_1',1);沙鲨游弋
768	  显式 0.25;Sfx 加 SINGLE_INSTANCE{Roar_0,Roar_1}互斥(onended 清槽,分槽独立)
769	- ★单实例语义全表(LegacySoundPlayer):case15 Roar=播着跳过/ case3 NPC_Hit=
770	  **Stop-重播**(未移植,连击打断重播语义)/ case4 NPC_Killed=每次都播(仅 style10
771	  互斥)/ case14·26·29 僵尸族=每次都播——勿一刀切互斥!
772	- ★PlaySound 签名陷阱:第 4 参 Style **缺省 1 不是 0/−1**——所有无 style 调用都是
773	  变体 1(Roar_1/Zombie_1 等),对轨时必须先查缺省值
774	- 连带蝙蝠死亡音疑案(用户报"洞穴蝙蝠死亡没声"):hurt→killedSound 链路进程内
775	  复现正常(NPC_Killed_4 播出);真根因=①蠕虫音墙掩盖 ②首播懒加载静默(NPC_Killed_4
776	  未缓存→playWavFile false→Game.playSfxFiles 回退 hit 合成音=死亡音"消失",第二只
777	  起才响)——修=怪池 Hit/Death wav 进世界定向预热(Game.ts preload 块 VANILLA_
778	  SPAWN_POOLS 全池)
779	- worm-roar 测试更新:骨蛇断言 Roar_1 非 roar 键+单实例互斥四断言(stub window
780	  AudioContext 喂 buffer 法,vi.stubGlobal 可测 Sfx 全链)
781	
782	**★roar 全调用点对齐批(2026-08-18 子代理穷尽对账,54 测试绿)**:
783	- SoundID.Roar 是 const int 15 非音轨对象,全树零 WithVolume;case36 ForceRoar
784	  style0=Roar_0/style-1=Roar_0+pitch0.6/缺省1=Roar_1;所有 case-15 调用零第 5 参
785	- 音量错档 6 处全改满响+坐标:双子变身(bossAI 0.7)/Prime 白天(0.8)/Prime 旋冲
786	  (0.6)/石巨人头自由(0.8)/EoC 冲刺预备(0.7)/EoC 连冲(0.7→playSfxWav
787	  'Roar_0'+pitch0.6,GameHooks.playSfxWav 补第 5 参 pitch)
788	- 漏吼 2 处补:骷髅王 35 旋冲 ai[2]==2(:22155)/魔眼 126 二阶段冲刺启动帧
789	  (:27674,雷眼无;twinsAI ai1===1 的 spaz 分支——注意 ai1===1 在 ai0===0 与
790	  ai0===3 两处各有分支,别放错宿主!)
791	- 借轨 10 处改直文件:duke 7 处+大龙卷→Zombie_20/小龙卷 Zombie_9/月总核心
792	  Zombie_92(×0.5 自动)/幻影矢前摇×2→NPC_Hit_6(PlaySound 4,6)/月总眼
793	  Zombie_100(:38227 Next(100,101)=恒100!)/幻龙 Zombie_102(×0.4 自动)/
794	  教徒显形 Zombie_89(×0.7 自动)/光女 Item_163/160/史后落地 Item_167/
795	  石巨人落地+冲拳 Item_14
796	- 自加音 9 处删(原版零声):教徒冰雾/闪电/仪式圈/火球、史后蓄冲/凝胶环、
797	  石巨人本体死吼+自由头死吼(头自由 :32587 一声保留满响)、月总头死光、
798	  四塔破盾、火山拉杆(Wiring.cs:1697-1741 仅动画)
799	- 遗留登记:魔眼二阶段冲 14+专家2.5 速(我们 13)速度档缺口与吼无关,另行修
800	- ★顺修:音效批新增的 game.playSfxFiles 非可选调用炸旧 mock(蚁狮 69 测试
801	  "playSfxFiles is not a function")——Enemy.ts 16 处+martian 2 处统一 `?.`;
802	  铁律:GameHooks 上的音效新调用一律可选链(旧 mock 不含键)
803	
804	**★终审清零批(2026-08-18 review 抓出)**:
805	- case36 ForceRoar 是**覆盖槽**语义(直接 CreateInstance,旧实例 _trackedInstances
806	  续播)=每次都播——case15 互斥会误吞 EoC 连冲高频吼!修=playWavFile 第 6 参
807	  replace(豁免互斥+槽位换绑,旧 onended 因 identity 检查不误删);EoC 冲刺预备
808	  (style0)/连冲(style-1+pitch0.6)两处传 true。★四 case 语义全表:15=播着跳过/
809	  3=Stop-重播/4·14·26·29=每次都播/36=覆盖+续播
810	- EoC 段一→段二变身(:20329)/FTW 重启(:20685)补坐标(原版带坐标衰减,曾无参)
811	- 史后蓄冲死变量清理(prev 只剩空块消费→整段删净)
812	
813	**★遗留清零批(2026-08-18 用户令"全部对齐",音效台账归零)**:
814	- ★BellHurt 5484 真相:=LegacySoundStyle(2,**35**)→**Item_35.wav**(case2 音库,
815	  ×0.75 自动档)——"素材缺"是当年 wav 名想成 Player_Hit_35 的误判,文件一直在!
816	  PET 表补齐全 14 键零缺;★全表 WithPitchVariance(0.4)=调用方掷 ±0.4 音高
817	  (Game 近战+projTargets 两处直调点带 pitch 参)
818	- 城镇宠物 637/638/656 json 补 HitSound/DeathSound(提取器漏;637/656 死音
819	  NPCDeath6、638 NPCDeath1);TownNPC 受击/死亡音硬编码(NPC_Hit_1×0.6/
820	  NPC_Killed_1×0.8)→vanillaSoundFiles 数据驱动+满响(原版 StrikeNPC/checkDead
821	  无音量参=1);229 微光变体特判保留
822	- 双子二阶段行为对齐:魔眼冲刺 14→expert **16.5**(:27674 段仅 expert 无 FTW)/
823	  减速计时 expert **×1.5**(:27696-27700);雷眼自造"侧移 seek8+射击180t"整段
824	  替换为原版**直冲 12/expert15/getGood+2**(:26746-26763;雷眼减速无 expert=一致);
825	  雷眼变身完成双声 NPCHit1+Roar(:26844——魔眼 :27478 只吼无前置声,双门分流)
826	
827	=====FILE: npc-damage-gate-port.md=====
828	---
829	name: npc-damage-gate-port
830	description: 玩家弹/爆炸对城镇NPC伤害门(Damage_PVE_Inner三例外:臭鸡蛋318无条件/巫毒22·54装备门/explodeAt同门);hitTownNpcs已有projId参;Arrow友方支曾整缺
831	metadata: 
832	  node_type: memory
833	  type: project
834	  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
835	  modified: 2026-08-18T04:48:26.040Z
836	---
837	
838	# 玩家弹/爆炸 → 城镇 NPC 伤害门补齐（2026-08-18，"原版 NPC 受爆炸物伤害吗"追问）
839	
840	**原版语义**（Projectile.Damage_PVE_Inner :11895-11925）：
841	- 玩家方弹（friendly）：`flag = !npc.friendly` → 城镇 NPC 恒 false → 免疫。
842	  三例外：**臭鸡蛋 318 无条件**（:11971 `flag |= type==318`——全游戏唯一
843	  可无条件砸 friendly NPC 的玩家弹，物品 1809 consumable 投掷→Arrow projId 318）；
844	  **向导 22** 需玩家装备向导巫毒娃娃 267（killGuide）；**裁缝 54** 需裁缝娃
845	  1307（killClothier）——任意玩家弹（弓/回旋镖/魔法弹/炸弹）都可走此门。
846	- 敌方弹：hostile && friendly && !dontTakeDamageFromHostiles 恒命中。
847	
848	**本仓盘点**（比初判好：hitTownNpcs/projTargets 已有且覆盖广）：
849	- 已有：Whip 巫毒门 ✓；Dart 陷阱弹内联 npc 循环（hostile）✓；Arrow hostile
850	  支 ✓；WeaponProj/MagicProj 调 hitTownNpcs 但 projId 没传（318 例外出不来）。
851	- 曾缺四件（本批补）：
852	  1. **hitTownNpcs 加 projId 参**：playerProj 门 `!doll && projId !== 318` 拒。
853	  2. **Arrow 友方支**（曾整缺——玩家弓/投掷弹对城镇 NPC 完全跳过）：
854	     `else if (!reflected && hitTownNpcs(..., 'playerProj', this.projId))`；
855	     318 命中即碎（penetrate 1 语义 killNow）。
856	  3. WeaponProj/MagicProj 调用点补传 projId。
857	  4. **explodeAt 城镇 NPC 门**（炸弹+向导巫毒=经典杀向导链）：同巫毒门
858	     （318 非爆炸物实际不达此路径），victim-settles 同盒（hurtBox 半宽判交）。
859	
860	**二审补（2026-08-18 review 批）**：
861	- explodeAt 门表达式与 hitTownNpcs 对齐（`!doll && projId!==318` 拒——曾写成
862	  `!doll || projId===318`，语义反转但 318 非爆炸物不可达=无害，仍对齐消歧）。
863	- **SkyDragonFury（Spin.applyHits 线段盒 + Swing 三段敌循环）与 FirstFractal
864	  补巫毒门**（projId 0=纯巫毒、无娃娃 no-op 零风险）；Celeb2Rocket 直击无门
865	  但命中即 explode→explodeAt 门已覆盖（结果等价，直击 vs 附近爆的形态差异
866	  记档）。Dart 内联 NPC 循环复核为【仅敌对弹可达】（`!hostile||reflected`
867	  提前 return）=flag2 正确，友方炮弹/雪球不经此 ✓（一审误判）。
868	- GrenadeProj 接触引爆仅查 enemies=faithful（原版 friendly 弹对城镇 NPC 无
869	  命中不触发引信）。
870	
871	**How to apply**：
872	- 测试 tests/npc-damage-gate.test.ts 7 条。★TownNPC 构造器 (key,x,y) 的 y 是
873	  **脚底**锚——盒顶 = y−h+2，测试弹/爆心必须按 `n.x/n.y` 实际盒算重叠
874	  （按传入 y 算 = 恒不重叠假阴性）。explodeAt 原型壳须 stub
875	  addDamageNumber/playSfxFiles（真方法碰未初始化 dmgNumbers → 'push' of undefined）。
876	- 反射弹（reflected→hostile）对城镇 NPC 走 hostile 支=原版 flag2 语义 ✓。
877	- Cannonball blastDamage（Dart 162/281）只伤敌怪 = faithful（friendly 弹）。
878	
879	关联 [[pvp-system-port]]（victim-settles 模型）/ [[town-npc-attack-port]]。
880	
881	

```


---

## 🤖 Assistant · 2026-08-19T07:07:55.827Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is a huge amount of content. Now let me read the remaining memory files. Let me check what's left:
- oracle-dome-mirror-mmmm-sync.md
- pppp-tail-debts-sweep.md
- pyramid-wallframe-die-debt.md
- review-found-bugs-fix.md
- rrrr-frame-kill-engine.md
- smoothworld-12345-checksuper-inactive.md
- ssss-tail-clearance-batch.md
- sw-asset-preload-port.md (may be old, but modified 08-18)
- time-system-11-port.md (probably modified date changed but old content)
- tree-statue-drop-investigation.md
- treecrack-gc-frameguard-2026-08-18.md
- uuuu-tttt-residual-clearance.md
- vanilla-npc-drops-port.md (old content probably)
- vine-cascade-port.md
- vulture-firefly-ai-fix.md (old)
- vvvv-matrix-final-preview.md
- weapon-fx-audit-2026-08-13.md (old)
- wof-voodoo-bossslot-fix.md
- worldgen-tttt-golden-channels.md
- worldgen-yyyy-fourchain-attribution.md
- oooo-deep-residuals-batch.md
- l10n-bare-key-incident.md (old)
- local-item-retirement.md (old)
- mechanics-audit-2026-08-12.md (old)
- equip-unique-stack-parity.md (maybe old)
- jungle-parity-and-id-collision.md (read - old)
- cursor-icon-fullbright.md (read)
- bed-sleep-visual-fix.md (read)
- book-mimic-cultist-dragon-batch.md (read)
- deerclops-port.md (probably has new additions)
- default-run-speed-parity.md (old)
- explosion-family-port.md (maybe old)
- fog-flicker-f4-latetex-fix.md (read)
- debug-tools-f6-f2.md (old)
- imagebitmap-root-cure.md (maybe old)
- journey-page.md (old)
- dualwindow (read)
- proj-draw-offset-table.md (read)
- bird-findframe-families.md (read)
- boss-audit-wave1-fixes.md (read)
- golem-3symptom-fix.md (read)
- dungeon-waterchest-float-knife.md (read)
- wwww-root59-liquidation.md (read)
- item-tooltip-parity-port.md (read)
- ai-parity-audit-2026-08-19.md (read)
- liquid-buffer-reflow-parity.md (read)
- remaster-studio-pipeline.md (read)
- server-room-simhost-port.md (read)
- webgl2-phase1-port.md (read)

Let me read the remaining ones I haven't: oracle-dome-mirror-mmmm-sync, pppp-tail-debts-sweep, pyramid-wallframe-die-debt, review-found-bugs-fix, rrrr-frame-kill-engine, smoothworld-12345-checksuper-inactive, ssss-tail-clearance-batch, tree-statue-drop-investigation, treecrack-gc-frameguard-2026-08-18, uuuu-tttt-residual-clearance, vine-cascade-port, vvvv-matrix-final-preview, wof-voodoo-bossslot-fix, worldgen-tttt-golden-channels, worldgen-yyyy-fourchain-attribution, oooo-deep-residuals-batch, deerclops-port, sw-asset-preload-port.

Some of these are quite long. Let me read them but limit output. Actually since the persisted output mechanism works fine, let me just read them in one batch.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:07:55.961Z · glm-x-preview-260804

```
现在处理剩余的记忆文件。
```


---

## 🤖 Assistant · 2026-08-19T07:07:57.717Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/memory/ && for f in oracle-dome-mirror-mmmm-sync.md pppp-tail-debts-sweep.md pyramid-wallframe-die-debt.md review-found-bugs-fix.md rrrr-frame-kill-engine.md smoothworld-12345-checksuper-inactive.md ssss-tail-clearance-batch.md tree-statue-drop-investigation.md treecrack-gc-frameguard-2026-08-18.md uuuu-tttt-residual-clearance.md vine-cascade-port.md vvvv-matrix-final-preview.md wof-voodoo-bossslot-fix.md worldgen-tttt-golden-channels.md worldgen-yyyy-fourchain-attribution.md oooo-deep-residuals-batch.md deerclops-port.md; do echo \"=====FILE: $f=====\"; head -c 4500 \"$f\"; echo; done",
 "description": "Read remaining memory files with size cap"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:07:57.787Z

**📎 ToolResult**

```
<persisted-output>
Output too large (38.1KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bjfyzjeoa.txt

Preview (first 2KB):
=====FILE: oracle-dome-mirror-mmmm-sync.md=====
# NNNN：oracle Dome 入口体镜像 + MMMM 四修同步（2026-08-19）

- **任务**：JS dgDomeEntrance（FFFF+MMMM 终态）→ caves-oracle.cs dungeonE+ 段 C# 转录；oracle 对 entKind==1 不再走 Legacy 近似。
- **谱系勘误**：1511931452 实测 **Tower**（A=1/B=0），非 HHHH 所记 Dome——其 40/78 回落真因=MMMM 四修改 Tower/Dome 共用下游段而 oracle 未同步。Dome 实证种子=**12345**（A=0/B=2/kind=1）。
- **oracle 十件**：inAct 通道（=JS wire bit5，不入四通道）+DgPillarStrip inact 参（清位→平滑→后置）+DgSolid/SolidOrSloped !inAct+JGS+灯笼/吊灯/桌面锚 nactive+statues 两门（MMMM③）；DgDungeonPot !inAct（MMMM①）；书链 `!Nowb && Next(50)`（MMMM②）；DgEntNoFeat 三门（MMMM④）；DgDomeEntrance 全量+dispatch（FFFF）；树族四件上移顶层（GrowTreeT ignoreWalls 参）。
- **结果**：_oraclesync 双种子 **71/78**（seed2 40→71，首红 dungeonP 消除；红=dirtlayer/rocklayer+IIII/OOOO/PPPP 尾段漂移带 piles..microbiomes 5 名，oracle 侧零改动）；12345 dungeonE 网格**逐位零差**（曾 `i+n3+21` 笔误→右楔柱镜像位 +42，网格差图定罪）；Legacy 种子 oracle 输出改前后逐字节全等；检查点数保持 75。
- **C# 顶层程序三陷阱**：局部函数可先调用后声明，但捕获变量须在**调用点**前赋值（CS0165——晚 pass 的表对早 pass 不可见，表+函数整体上移）；块内局部函数块外不可见（GrowTreeT 须上移）；上移与兄弟块同名冲突 CS0136（改名 SetTSG）。
- **方法论**：JS↔oracle 网格差分=JS `.typ` 是内部 id 须 TILE_DEFS 映射 sheet、oracle `DPD_DUMP .act` 是 '0'/'1' 文本非二进制；入口谱系用 `DG_ENT_DBG=1` 一跑定谳。

=====FILE: pppp-tail-debts-sweep.md=====
# PPPP 批：尾段五小债+Tower 复扫（2026-08-19）

- **12345 祭坛级联**：#47-52 祭坛 6 格根因=蜂蜜斑挖蜜池 ClearTile(frameNeighbors:true) 四邻帧→Check3x2(26) 支撑失守→KillTile×6（vanilla HiveBiome 真语义）；修=FinalCleanupPass 导出 genFrameNeighbors/genSquareTileFrame（ZZZ 帧分派复用），HiveSpiderPass 四 Gen 步骤接帧链+FOUT tile 侧。#53 Sl 2,278→0；12345 链 0-48+50-53 全绿，唯一残 #49 Lt=1 (1982,661)=liquid 冻结域（密闭水袋被沉降转岩浆，vanilla 静止）。
- **#58 雕像 7Hf**：PlaceTile cs:59503 else-if 活性锚+ResetsHalfBrickPlacementAttempt（默认 true，例外表不含雕像）→清 half+帧；随机 y 落岩体触发。归零。
- **#76 Traps 8 格**：①EEEE「井杀巨石免杀」=误判——vanilla 照杀，巨石存活靠 KillTile 尾 SquareTileFrame→Check2x2 完整性级联（双陷阱 B 先 A 后序本无差）；②单格短钟乳石须走 checkStalactite 帧分派（矩形锚搜必败）；③沙穴壳侧清坡原版字面列=i-num5-2/-1/+1/+2 全左侧（1.4.5.6 原样 bug 勿对称化）+板 PlaceTile 尾 SquareTileFrame 失活格清 half/slope。归零。
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-19T07:08:02.557Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/e65c4575-731a-43e0-a377-ccf50cc42db3/tool-results/bjfyzjeoa.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:02.691Z

**📎 ToolResult**

```
1	=====FILE: oracle-dome-mirror-mmmm-sync.md=====
2	# NNNN：oracle Dome 入口体镜像 + MMMM 四修同步（2026-08-19）
3	
4	- **任务**：JS dgDomeEntrance（FFFF+MMMM 终态）→ caves-oracle.cs dungeonE+ 段 C# 转录；oracle 对 entKind==1 不再走 Legacy 近似。
5	- **谱系勘误**：1511931452 实测 **Tower**（A=1/B=0），非 HHHH 所记 Dome——其 40/78 回落真因=MMMM 四修改 Tower/Dome 共用下游段而 oracle 未同步。Dome 实证种子=**12345**（A=0/B=2/kind=1）。
6	- **oracle 十件**：inAct 通道（=JS wire bit5，不入四通道）+DgPillarStrip inact 参（清位→平滑→后置）+DgSolid/SolidOrSloped !inAct+JGS+灯笼/吊灯/桌面锚 nactive+statues 两门（MMMM③）；DgDungeonPot !inAct（MMMM①）；书链 `!Nowb && Next(50)`（MMMM②）；DgEntNoFeat 三门（MMMM④）；DgDomeEntrance 全量+dispatch（FFFF）；树族四件上移顶层（GrowTreeT ignoreWalls 参）。
7	- **结果**：_oraclesync 双种子 **71/78**（seed2 40→71，首红 dungeonP 消除；红=dirtlayer/rocklayer+IIII/OOOO/PPPP 尾段漂移带 piles..microbiomes 5 名，oracle 侧零改动）；12345 dungeonE 网格**逐位零差**（曾 `i+n3+21` 笔误→右楔柱镜像位 +42，网格差图定罪）；Legacy 种子 oracle 输出改前后逐字节全等；检查点数保持 75。
8	- **C# 顶层程序三陷阱**：局部函数可先调用后声明，但捕获变量须在**调用点**前赋值（CS0165——晚 pass 的表对早 pass 不可见，表+函数整体上移）；块内局部函数块外不可见（GrowTreeT 须上移）；上移与兄弟块同名冲突 CS0136（改名 SetTSG）。
9	- **方法论**：JS↔oracle 网格差分=JS `.typ` 是内部 id 须 TILE_DEFS 映射 sheet、oracle `DPD_DUMP .act` 是 '0'/'1' 文本非二进制；入口谱系用 `DG_ENT_DBG=1` 一跑定谳。
10	
11	=====FILE: pppp-tail-debts-sweep.md=====
12	# PPPP 批：尾段五小债+Tower 复扫（2026-08-19）
13	
14	- **12345 祭坛级联**：#47-52 祭坛 6 格根因=蜂蜜斑挖蜜池 ClearTile(frameNeighbors:true) 四邻帧→Check3x2(26) 支撑失守→KillTile×6（vanilla HiveBiome 真语义）；修=FinalCleanupPass 导出 genFrameNeighbors/genSquareTileFrame（ZZZ 帧分派复用），HiveSpiderPass 四 Gen 步骤接帧链+FOUT tile 侧。#53 Sl 2,278→0；12345 链 0-48+50-53 全绿，唯一残 #49 Lt=1 (1982,661)=liquid 冻结域（密闭水袋被沉降转岩浆，vanilla 静止）。
15	- **#58 雕像 7Hf**：PlaceTile cs:59503 else-if 活性锚+ResetsHalfBrickPlacementAttempt（默认 true，例外表不含雕像）→清 half+帧；随机 y 落岩体触发。归零。
16	- **#76 Traps 8 格**：①EEEE「井杀巨石免杀」=误判——vanilla 照杀，巨石存活靠 KillTile 尾 SquareTileFrame→Check2x2 完整性级联（双陷阱 B 先 A 后序本无差）；②单格短钟乳石须走 checkStalactite 帧分派（矩形锚搜必败）；③沙穴壳侧清坡原版字面列=i-num5-2/-1/+1/+2 全左侧（1.4.5.6 原样 bug 勿对称化）+板 PlaceTile 尾 SquareTileFrame 失活格清 half/slope。归零。
17	- **#105**：FillWallHolesInArea 移植（地表带墙洞 BFS，≥150 弃填/触空膨胀/众数墙型）W247→1；「204 真缺口」证伪——production 杀集裁决 killed×198/204=frameSparse 探针假差。
18	- **house#111 193 格=陈旧基座假债**：production 有雕像陷阱红线（±25 窗 11 格）同拒屋；重放 s17 边界 frames.bin 缺线所致。DDDD 四级织入撤销；rig 复用前须 cap 重捕。
19	- **Tower s33333 复扫**：锚 (698,181) v==j、致动位 6/6 全等、盒差 0.90%=对齐种子带——MMMM Tower 支同修无回归。
20	- 教训：重放残差先辨基座捕获陈旧度（线/帧通道非金标）；vanilla bug 勿"修正"（清坡左侧列/巨石免杀两案反向）；KillTile 失活邻格清位+165 帧分派是杀链通用件。
21	
22	=====FILE: pyramid-wallframe-die-debt.md=====
23	# 金字塔走廊 26v24 = 刷墙段 SquareWallFrame 掷债（ZZZZ 批定谳）
24	
25	YYYY 阻塞项"golden 二进制 vs 反编译行为差"终审（2026-08-19，报告 ZZZZ 批章）：
26	s22222 金字塔走廊直段 vanilla 26 带 vs JS 24 带，根因**不是** Next(20,30) 骰本身。
27	
28	## 根因链
29	- WorldGen.Pyramid 主体刷墙段（cs:27870-27888）每写一墙 34 调
30	  `SquareWallFrame(m,n)` → Framing.WallFrame(resetFrame:true) 在
31	  wallLargeFrames[wall]==0 时掷 **1×Next(0,3)**（wall==21 另有第二掷；墙 34
32	  非大帧墙≠21 ⇒ 恰 1 掷/墙）。s22222 计 **11025 掷**。
33	- JS 金字塔（StructuresPass.ts）镜像了写墙但**没镜像掷** → num8 之后全部骰序
34	  位移：num12（Next(20,30)）取流位 #6=23 而非 #11029=25 → 走廊峰值列
35	  2677+25=2702 vs JS 2700 → 出口隧道错路（y 496 vs 461）→ pre-temple 债 6154
36	  → 神庙锚 iter2 → ~100k 格级联。
37	- 三方证据逐位一致：①金标 dump 几何拟合骰向量 (d4..d9)=(1,5,25,16,8,25)；
38	  ②fresh(22222) 样本流 K-约束解命中 11025 且几何墙写独立重放=11025；
39	  ③双参 Next(int,int) 织入实测（/tmp/zzzz-span.txt）：PYRHDR 2686,228 →
40	  0,9,108 → **11025×Next(0,3)** → a2=1 → 5,8=5 → **20,30=25** → 16/8/25。
41	
42	## 方法论要点（复用价值）
43	- **RunPass 每 pass 头 `Main.rand = new UnifiedRandom(_seed)`**（genRand=>Main.rand
44	  属性）——骰是 pass 局部的，跨 pass 流位移不可能；排查找 pass 体内。
45	- IL 直读两把快刀先行（Pyramid 骰序/边界 + UnifiedRandom.Next 数学），再织入。
46	- 织入 ret 钩：**先插 dup 再插 call**（后插者离锚近；反序=[call,dup,ret] 炸
47	  InvalidProgramException）；头钩 InsertBefore 每条重取 Instructions[0]（LIFO）。
48	- 0817 地牢/装饰同族教训重演：SquareWallFrame 掷语义 DesertPass.wallFrameDraw
49	  早有先例——**凡 PlaceWall/刷墙调用链都要查 Framing.WallFrame 的掷**。
50	- 勘误：PYR_TRACE 打印 k-- 前值（"k=229"非锚差，锚两侧同为 j=228）；mile8
51	  slot json 是对拍基线，复跑会覆盖（先备份）。
52	
53	## 修复（移交协调者——StructuresPass.ts 并行禁区）
54	金字塔刷墙段写墙后补 `rng.int(0, 2);`（精确 diff 见报告 ZZZZ 批 ⑤）。
55	验证（/tmp 副本施加）：#40 金字塔 3269/6089→176/178（纯 #32 地牢债基线）、
56	#46 神庙 35639/62947/67415→176/178/0 级联全消、#105 终态 −28/−34/−70/−50%；
57	9293480 A/B 全等（无金字塔链零影响；四链中唯 s22222 建金字塔）。
58	
59	=====FILE: review-found-bugs-fix.md=====
60	---
61	name: review-found-bugs-fix
62	description: 对抗性审查抓出11真bug全修:红帽ai3断链(普通骷髅王刷Chippy套装漏洞=ai3被旋冲挪用skeletronSpinDir独立)/史莱姆雨第三参未传+downedSK单读/光女弹幕9999五处+dash覆写序+真狂暴入夜离场/弹540孵化Bottom锚/兔子站定清walkCycleT相位/静持锚传真实useStyle/钓竿谓词补2421·2422/Critter.ts删除后测试迁移(player stub+onEnemyKilled)
63	metadata:
64	  type: project
65	---
66	
67	审查修复批（2026-08-18，三路对抗审查抓出 11 真bug 全修，155/155 绿）。
68	
69	**漏洞级**：①**红帽骷髅王 ai3 断链**——召唤只写 redHat 旗但 NpcDrops 五条规则/Renderer 红臂骨/GorePiece 全读 **ai3**；且 bossAI.ts 把 ai3 挪用为旋冲方向(±1)→**普通骷髅王约半数击杀必掉全套 Chippy 时装**（刷物品漏洞）。修：召唤补 `head.ai3=1` + 旋冲方向改独立字段 `skeletronSpinDir`（bossAI :50/:64/:93/:124 四处；Prime 127 的 ai3 用法独立无冲突勿动）。②史莱姆雨计数门两断线：Game 调用没传第三参 kingSlimeOnField + downedSK 单读 `downedSlimeKing`（击杀链写的是 `downed_50`）——双修。
70	
71	**行为级**：③光女白天狂暴弹幕五处 shoot 漏置 9999（:46349-46356 flag4 num6-10 全 9999）+ dash 是 9999×1.5=14999（:47294-47299 **覆写在乘区后不乘**）+ 真狂暴(ai3∈{2,3})入夜应强制 13 态离场（:46580-46595）。④弹 540 孵化锚：NewNPC 是 **Bottom 锚**（:81547）→ fromVanilla 中心锚须传弹底再回退 h/2（测试同步改）。⑤兔子站定不清 walkCycleT → 起步相位漂移首帧非 0（原版 case46 vx==0 清 frameCounter :77571-77577；Enemy.ts 通用 tick 站定清零）。⑥迅猛龙静持锚传 useStyle:null → 丢原版 us2/9/5 档（:50684-50690 flag 族只读 heldItem.useStyle 与动画无关）；修：经 itemFuncOfVid(vid).useStyle 传真实值。⑦钓竿谓词漏 2421/2422 熔线钓钩（fishingPole 全集 9 件）。
72	
73	**测试基建**：并行会话删除 src/entities/Critter.ts（小动物 Enemy 化）后 proj-critter-hit 未迁——修为 `Enemy.fromVanilla(299)` 松鼠 + GameHooks stub 补 `player`（Enemy.hurt 死亡 ctx 读 p.hp）与 `onEnemyKilled` 回调。
74	
75	关联 [[boss-summon-drops-events-batch]] [[bunny-walk-frame-fix]] [[leftover-closeout-4batch]]。
76	
77	=====FILE: rrrr-frame-kill-engine.md=====
78	# RRRR 批（2026-08-19）：邻近装饰帧杀引擎 + #77 残 952→2
79	
80	- **引擎落地（FinalCleanupPass.ts 扩展为通用帧杀引擎）**：①实心谓词全改 genSolidType
81	  （229 在 Piles 期间非实心→罐失撑击杀，静态表查不出）；②KillTile 尘掷实测表——
82	  **26/695 祭坛 frameX<54→10×Next(2)/格**（织入探针两杀间恰 10 单参掷实证），
83	  28/165/485/10/135/185/186/187 **零掷**（OOOO 移交的"尘掷表"实为击杀普查数）；
84	  ③Check3x2 补金币掉落掷+5×5 尾扫+187→186 raw type；④新族 CheckDoor/Check1x1
85	  （135=229 失撑）；⑤PilesPass 统一走 genSquareTileFrame，双尾帧（case 分支尾
86	  无条件+成功尾再跑=引擎两轮）。
87	- **三真 bug**：平台 tileSolid 补真（{19,427,435-439} 锚定门曾拒放，P3(1930,1090)
88	  实证）；⑤段迭代上界 **2519**（IL 读 2520 但掷值解码证明 vanilla ⑥ 起于 170661，
89	  2519 为残量谷值，1 次之差未解备案）；尘掷门 frameX<54（回填 style 9 会吞掷）。
90	- **重放基座帧回填（tools/www-framebackfill.ts）**：金标无帧通道+边界帧系捕获期
91	  历史——按族分裂信任：罐/485 全几何右锚切瓦、185 无条件 1x1、186/187/26 相位感知
92	  （覆盖留边界帧）、165 全几何 biome style。杀普查终态对拍 7 族逐格全同（165×10
93	  须终态反查——killStalactiteTile 不进 killTileGen 钩）。
94	- **#77: 952→2**（残 2 格=顶坡平台支撑小堆，vanilla 放置与 slope==0 门矛盾未解）；
95	  **#93 10/11 未动**（GemPasses 冻结；引擎就绪，placeExposed 邻格清循环换
96	  genSquareTileFrame 一处即接）；#99/#105 旧债未塌缩；#63 与在案同（他案在途）。
97	- 回归全绿：mile8 双种子/液体 60/60/冒烟 22s（+5s 可接受）/gem+tile-cleanup 24/24；
98	  world-final-hash 红=交付后再生窗口状态。★方法论：掷值解码（UnifiedRandom 状态
99	  推进与调用域无关——快进 N 掷读原始样值可反推 x/y/样式归属段）；杀普查须含
100	  killStalactiteTile 等旁路；IIII/OOOO 哈希流"逐位全同"是位置平凡的（同种子必同）
101	  ——语义对齐须 P3/PS/kill 事件按掷位对齐。
102	
103	=====FILE: smoothworld-12345-checksuper-inactive.md=====
104	# 12345 #53 SmoothWorld 自差清零（LLLL 批 2026-08-18）
105	
106	- **双根因**：① KillTile 尾级联缺 `CheckSuper`（cs:86437-40 case 376/443/444/485 → cs:48117-48406）
107	  派发——485 蚁狮幼虫 2×2 完整性破组杀（Style2x2 派生 CFW=CFH=36/StyleHorizontal；
108	  生成期在场仅 485）。实锤 (1856,476)：K(1857,475) 尾帧触邻格 485 → 组伴被大理岩顶替 →
109	  整组杀+残凸砸半=**两枚零掷动作**（流恒齐只动作数漂 → 全图半砖/坡放大）。② SolidTile 族
110	  （cs:70170/70052/70228）缺 `!inActive()` 致动腿——12345 vanilla 穹顶 234 格致动柱，
111	  JS 视为实心 → 穹壳 6 格 slope 错写（(3396,158) 等）；JS 管线无致动写入故他 pass 不动。
112	- **修后**：反事实（golden052 基座+管线帧快照+GenSolid 时点态 restore）→ **八通道差 0/
113	  动作 89,683 全等/掷 5,098,924 精确**；9293480 主链 0..53 全绿+_hstrace ★全等★ 不回退。
114	  12345 管线残余=穹顶输入债 loop2 掷偏移翻面（对称 S0>3/S3>0），MMMM 清 #32 后塌缩。
115	- **方法论**：★零掷但非零写的级联**掷数对拍不可见**，必须动作序列对拍（swtrace exe
116	  a4f3d8ce + JS __swSWAct 同格式）；第二种子 trace=/tmp/llll/swtrace12345.log（5.37M 行
117	  只覆 #53，末 RD 哈希==pc.txt P|53 f6）。9293480 存档曾误删已再生（字节同/哈希链同
118	  passchain19/_hstrace 全等四重验证）。
119	- 详见 game/docs/worldgen/content-parity-vs-vanilla-2026-08-16.md「LLLL 批」。
120	
121	=====FILE: ssss-tail-clearance-batch.md=====
122	# SSSS 尾段终清波（2026-08-19）
123	
124	- **#93 Random_Gems 10/11→0**：placeExposed 邻格清循环换 genSquareTileFrame×2（②cs:59724+③cs:60281 双尾；中心 178 引擎无 case）+ PlaceTile 前置清（cs:59500 坡残格）+ rig slot45 s44 帧回填（嵌合帧 CheckPot 自相矛盾伪杀）。#92 连带保 0。
125	- **#77 Piles 2→0**：★SolidTile2 **坐标重载 cs:70497 带平台 topSlope 豁免**（`(Platforms&&(half||topSlope))||slope==0`，Tile 重载 cs:70178 无——两重载语义不同！织入 ARB 运行期 dump 实证 slope()==1 且 ST2=True）；2519-vs-2520 仲裁：GPA 实测 3669=252+42+126+15+**2520**+84+630 → ⑤=2520，RRRR 谷值系该 bug 补偿假象。
126	- **#63 Spider 1203/1331→48/59（−96%）**：placeTightWebs 补 anyShimmer/231 门+ClearSlope+**尾部 CheckStalactite**（泥土支撑 GetDesiredStalagtiteStyle fail→整对杀=T0>165×527 主根因；特殊支撑 style 掷）+ placeDeco187 前置清+双尾帧+anyLava+pot half 清。残=波前分区单点时序差（SF A-访问序 25,188 项全同后 (474,996) 延迟 103 位），0.14% 备案。
127	- **#99 残=输入债定罪**：SL 锚序 156,354 项全同后分叉=(605,782) A137 雕像帧边界缺失（dir 反向→⑦ 邻杀漏→滴头门跳过）→#58 Statues 债渗入；真缺口=⑦ 31/12/639/箱/28/26 重建段有可见写（~14 格）。④ KillTile 尾部级联已补（cs:63967）。
128	- **#101 复验未零=箱 sink 179 vs golden 350**（幻影 wire 已清）→ DeadMans 候选流差级联，#58/#59/#62 上游债。
129	- ★**方法论：genRand 内态 FNV 哈希流是移位不变的（同消耗次数的流位移检不出）——对齐须用 span 序列（SA/SB）+SF/SL 逐调用坐标序**；织入探针全钩版（span/SF/SL/GPA/ARB）留存 /tmp/oooo-app+/tmp/oooo-patch（arch -x86_64+SW_EVIL=0+rm 旧 wld+-world 显式）。
130	- 回归：mile8 双种子全绿/液体 60/60/冒烟无死循环/WWW 全槽无邻槽回退。
131	
132	=====FILE: tree-statue-drop-investigation.md=====
133	---
134	name: tree-statue-drop-investigation
135	description: 砍树掉靴子雕像排查:1444刀+400摇全净(现build无泄漏);靴子雕像=item 462无任何生产者;斧本不能破坏雕像(pick专属);最可能=地上旧掉落物误归因
136	metadata: 
137	  node_type: memory
138	  type: project
139	  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
140	  modified: 2026-08-18T06:23:17.254Z
141	---
142	
143	# 砍树掉"靴子雕像"排查（2026-08-18 用户报障，未复现）
144	
145	**排查矩阵**（全部干净）：
146	1. **掉落来源审计**：item 462 Boot Statue（createTile=105 雕像族 117 件之一）
147	   在全仓**零生产者**——TreeShake 表 40+ vid 逐一 `VI()` 解析验证（含
148	   832/933/3360/3361 魔杖族、5629 弹弓、4366 树液、水果 20 件、钱币 71-73、
149	   1809 臭蛋）；killTileGetItemDrops_Tree 返回值域干净；vanilla-npcdrops 全表
150	   无 item 462 规则（含全部摇树小动物 vid）；spawnNpcByVanilla/
151	   spawnTreeShakeNpc 失败静默 return 无物品兜底。
152	2. **浏览器探针三连**（_treechopdrops.mjs，spawnDrop 全拦截）：
153	   ①40 树满力一刀倒（317 件全 Wood/Acorn/Ebonwood）；
154	   ②80 树低斧力 1004 刀（摇树掷骰活跃，382 件含 1/100 弹弓、1/300 叶魔杖
155	   等全合法稀有项）；③全图 400 树纯 tryShakeTree 各一摇（30 件全合法）。
156	   雕像族（createTile=105）零命中。
157	3. **机制排除**：斧头**本来就不能破坏雕像**——雕像 def pick:0/axe:-1，
158	   toolMatchesTile 斧档只认 TILE_AXE_SHEETS → 用户即便瞄到树旁雕像也砍不动。
159	
160	**最可能解释（非 bug）**：
161	- 树基有**更早掉落的雕像物品**躺在地上（雕像=镐挖产物；地下雕像常见），
162	  砍树掉落物在同点落地、拾取时一并入包 → 误归因给树。
163	- 或用户玩的是修复前的旧构建（斧族/摇树批 2026-08-17 才落）。
164	- 若可复现：需要存档/种子+当时手持物再定位。
165	
166	**How to apply**：同类"掉错物品"报障的排查套路=①目标 item 全仓生产者
167	grep ②来源系统表逐一 vid→VI() 解析 ③spawnDrop 全拦截探针三档压测
168	（一击倒/低力多刀触发全掷骰/纯入口直调）。
169	
170	=====FILE: treecrack-gc-frameguard-2026-08-18.md=====
171	---
172	name: treecrack-gc-frameguard-2026-08-18
173	description: 砍树拾取崩溃定位(trace ProfileChunk 法+死亡签名)+inv.add守卫+主循环熔断;行走掉帧=GC churn(lq() 零分配化)
174	metadata: 
175	  node_type: memory
176	  type: project
177	  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
178	  modified: 2026-08-18T05:50:47.800Z
179	---
180	
181	2026-08-18 用户报:行走仍掉帧 + 砍树掉落自动收集时崩溃(traceH)。
182	
183	**崩溃定位方法(可复用)**:trace 尾部主线程 rAF/timer/microtask 全停但进程
184	空转 = **rAF 链被未捕获异常炸断的死亡签名**;trace 的 **ProfileChunk
185	(CPU 采样)含 nodes/samples/timeDeltas**——按 timeDeltas 倒推重建时间线,
186	死亡前最后非 GC 样本 = `updateLiquidInner`/`get equipStats`(采样 ~200µs
187	粒度,死点在其后同帧内)。★普通 trace 就带 CPU 采样,崩溃栈可解!
188	另:死亡窗口出现 hdslb.com(扩展注入)= headless 无法复现的原因之一。
189	
190	**三修**:
191	①`Inventory.add` 首行裸 `ITEM_DEFS[id].maxStack` → 未知 id 拾取瞬间
192	TypeError 炸帧循环。守卫:拒绝入包+`[inv.add] 未知物品 id` warn 带来源栈
193	(下次触发即可定位是谁产出的 id)。
194	②`Game.start` 主循环 try/catch 熔断:异常→console.error(进 __swErrors 环,
195	F5 可取)→停机+Toast.FrameError(双语键已入 custom+重建)。**今后任何未知
196	崩溃都有现场,不再静默冻结**。
197	③行走掉帧根因=GC(0.94s/次,5/8 长帧与 MajorGC 重合):`VanillaLiquidRenderer`
198	四邻 lq() 每调用 new {lq,lt} ×4/格 = 水邻屏 8k-33k 对象/帧 → 零分配化
199	(标量 nb() 读+四组局部,consider 展开保 L→R→U→D 严格大于语义)。
200	**残余**:lightAt 元组 3-6k/帧(下一候选,待复测 GC 间隔后再决定)。
201	
202	复现探针教训:breakTile 直调/Lucy 弹窗/贴脸砍+拾取三轮 headless 均不复现
203	(缺真实输入路径+扩展环境)——此类一次性崩溃优先上"守卫+熔断取证"而非
204	盲试复现。
205	
206	相关:[[imagebitmap-root-cure]] [[webgl2-phase1-port]]
207	
208	=====FILE: uuuu-tttt-residual-clearance.md=====
209	# UUUU 批：TTTT 五残量清偿（#66/#76/#99 三归零 + #63 全 pass 掷流全等）
210	
211	- **#66 Temple mayanTrap 全重写**（cs:8314+ 非 2945）：落点门查 232 非 226/SolidOrSloped 谓词族/锚型门 190,135,137,232,237,10/纵扫 worldSurface 非 rockLevel/线色 Next(3) 恒掷/SlopeTile 压平/KillTile 锚/横支 Next(5) 上延叠陷/PlaceTile137 active 保帧；家具 Place2x1 左锚（placeFurn 居中曾偏 1）/雕像 SolidTile2 地面门/挂饰 3x3 以采样点为中心。→八通道零+sink 177/177 全等（4v5 归零）。
212	- **#76 Traps 帧债定谳无罪**：金标 077×槽31 重放帧对拍 newAtTraps=0——111 帧差全 temple 继承（①修后清）+8 全 dungeon（禁区在案）。
213	- **#99 ⑦ 重建段落地**（31/12/639/箱21·467 item0 锁箱 style 覆写/28/26+Wall2Terrain 底行补型+右列 639 读左列原版笔误保留）+**KillTile 尘掷勘误**：水死族 24/27 每杀 10×Next(2)（SSSS"零掷"有漏）→ 八通道零+2,059,985 掷逐条全等。
214	- **#63 双真根因全在 chest 掷**：①loot 16 处 Next(K)+offset 被写成 int(offset,max)（同宽 1 sample 值域平移——SSSS 掷总数口径检不出，须 span 型序列对拍）；②地狱尾 5010/4443/4737/4551 四门漏 flag8 旗（y∈[h-250,h-205) 蜘蛛箱带四掷短路）→ **160,186 掷零分叉**，48/59→2（残=PlaceUncheckedStalactite preferSmall 小型分支未谳，试接 2→1130 回退备案）。
215	- **两大反编译陷阱**（IL 直读定谳勿按源移植）：AddBuriedChest num11 style 变体门在 errorWorld 分支内（普通种子跳过）；loot 四档链第二档门=num7<rockLayer（IL +1419，反编译折进 flag23 remix 段）。TileFrame(resetFrame) 掷真源=TileFrameImportant 178/184/72 族非 cs:82448（!generatingWorld 挡死）；引擎补 case178+reset 贯通（**读帧族入 dispatch 必同步入 frameSparse 表**否则 #64/65/92/105 假回归带）。
216	- 基建：/tmp/uuuu-app（Spider 方法体替换织入+InSpider 门控 Next 头钩）；rig 增 SW_WWW_SPAN_DUMP/SPIDER/FRDUMP/CHDUMP 探针；mile8 双种子绿/液体 60/60/冒烟 2/2；gen-loot 1 败=HellFortPass 并行 05:52 在途（复测定谳非自因）。
217	
218	=====FILE: vine-cascade-port.md=====
219	---
220	name: vine-cascade-port
221	description: 藤蔓支撑级联CheckVines移植:打中间节下方整段消失;IsVine八族同构;亲代面变型+支撑白名单
222	metadata: 
223	  node_type: memory
224	  type: project
225	  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
226	  modified: 2026-08-18T04:43:25.099Z
227	---
228	
229	# 藤蔓支撑级联 CheckVines 移植(2026-08-18)
230	
231	用户问"打掉藤中间一节,下方会不会消失"——**原版会**:CheckVines
232	(WorldGen.cs:85599-85700,TileFrame 入口 :82114 对 IsVine 全族逐格):
233	- 上方非同型藤且非亲代面 → `KillTile(i,j)` 整格消;KillTile 尾部 SquareTileFrame
234	  3×3 → 下方藤再查 → **级联到藤底**。
235	- 上方是异族亲代面 → **变型**成对应藤(52 挂丛林草→62)。
236	
237	## IsVine 八族(TileID.cs:237)与亲代/支撑表
238	
239	| sheet | 藤 | 变型亲代面(:85630-85655) | 支撑白名单(:85661+) |
240	|---|---|---|---|
241	| 52 | 普通藤 | {2,52,477}(type≠382) | {2,477,192} |
242	| 62 | 丛林藤 | {60,226,62} | {60,**384 活红木叶**,226} |
243	| 115 | 神圣藤 | {109,115,492} | {109,492} |
244	| 205 | 猩红藤 | {199,205,662} | {199,662} |
245	| 636 | 腐化藤 | {23,636,661} | {23,661} |
246	| 382 | 神圣花藤 | {382} | {2,477,192} |
247	| 528 | 蘑菇藤 | {70,528} | {70} |
248	| 638 | 1.4.5 新藤 | {633,638} | {633} |
249	
250	上方格取型条件:nactive && !bottomSlope(slope 3/4 排除)+同型续接先于一切。
251	num==-1(上方非活)恒死。变型集与支撑集**不同**(62 的 384 在支撑不在变型)。
252	
253	## 本仓实现
254	
255	- `Game.checkVineAt(i,j)`(CheckVines 1:1)+ 监听
256	  `onTileChanged((x,y) => checkVineAt(x, y+1))`(下落沙同款);级联靠
257	  breakTile→setTile(0) 再触发监听逐节向下,天然递归。
258	- 变型走 `VINE_INTERNAL_BY_SHEET` 反查内部 id + setTile(触发下方再查,
259	  等价原版 3×3 帧化)。
260	- 生成/导入期 setTileSilent 不触发 → 生成端挂藤零扰动。
261	- 测试 tests/vine-cascade.test.ts 五例(中间级联/顶草全灭/52→62 变型/
262	  蘑菇藤白名单/384 支撑);端到端探针:9 节丛林藤打第 2 节 → 下方 7 节全灭顶节留。
263	
264	## 教训
265	
266	- "水草"类垂挂物(蘑菇藤 528 发光藤)与丛林藤同构——查机制先找 TileID.Sets
267	  家族集,不逐个猜 tile。
268	- onTileChanged 事件驱动级联是本仓先例模式(火把掉落/下落沙/藤三级);
269	  新"支撑类"tile 语义照此接。
270	
271	=====FILE: vvvv-matrix-final-preview.md=====
272	# VVVV 终局矩阵预演（39 世界只读重跑 2026-08-19）
273	
274	全量矩阵 /tmp/matrix-vvvv.json（39/39 零 error）：s×25 typ 3.433/wal 1.771/liq
275	0.349（small-8 同集对照 8/17 -27.6%/-57.3%/-42.6%）、m×9 4.112/2.731/0.482
276	（XXX -1.5%/≈0/≈0）、l×5 3.764/2.015/0.493（wal +4.4%）、**s12345
277	2.508/0.303/0.197（-42.6%/-94.1%——地牢盒+墙变体塌缩实证）**。总残余
278	20.9M 格（3.747%/2.147%/0.435%）。树干 run 全 39 = 原版 101.2%（计数过收敛）。
279	
280	残余分流（triage 探针 _vvvv-triage 用毕删）：
281	- 已塌缩 ✓：s12345 蜘蛛墙 43025→0、地牢盒 typ 0.3%/wal 0；丛林墙 64 -27%、
282	  石缘 -24%；XXX 的 s12345 dungeonX/Y 头锚差已清。
283	- UUUU 域确认量小（<2k 格）：Temple 箱 4v5/#99 滴头/祭坛/蜘蛛 2 格/帧 4 掷。
284	- **★新面孔**：①蜘蛛巢位移（非 12345 种子 wal62 46-127k/世界，原版巢盒内
285	  62>0 盒外 0>62 对敲+蛛网外溢——#63 掷流全等只在 12345 成立）②装饰位漂族
286	  （165 洞穴装饰 2.15M+丛林藤 62·1.49M+灰烬藤 638 250k+罐 208k+树 127k，
287	  全对称位漂=计数等坐标移）③湖体 ±255 液体位漂（liq 主量）④背景墙层系
288	  196-215+洞穴变体 54-58/170/171 ⑤spawnY 13/39 世界 ±1~2（陈债）⑥s22222
289	  神庙整体错位（JS 盒偏 ~+460x/+123y，单世界 ~100k 格，其余种子逐位同）。
290	- 终局预判：**UUUU 交付后矩阵不动（0.01% 量级）**，零差需种子泛化批：
291	  蜘蛛巢锚→装饰位漂（先 visit 对拍定谳几何放大 vs 掷流分叉）→湖体→背景墙。
292	  s12345 自身残量主项=装饰 165 位漂（非地牢域），与全矩阵同族。
293	
294	资产：/tmp/matrix-vvvv.json + /tmp/vvvv-triage.log 留档；报告末章
295	docs/worldgen/content-parity-vs-vanilla-2026-08-16.md「VVVV 批」。
296	
297	=====FILE: wof-voodoo-bossslot-fix.md=====
298	---
299	name: wof-voodoo-bossslot-fix
300	description: 巫毒娃娃召肉山漏设Game.boss槽=击杀链全跳过(无砖盒/无StartHardmode/无公告)根因;spawnWOF补设槽;掉落管线本就正确(探针内部id≠vanilla id误读教训);CanKillTile树下保护=原版真规则
301	metadata: 
302	  node_type: memory
303	  type: project
304	  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
305	  modified: 2026-08-18T03:21:32.657Z
306	---
307	
308	肉山击杀无小屋/无肉后变化修复（2026-08-18，用户报"杀死肉山没出现小屋子、没触发肉后变化"）。
309	
310	**根因**：巫毒娃娃入岩浆路线（ItemDrop.checkLavaDeath :452 → spawnWOF）**没设 Game.boss 槽**——击杀链全挂在 `bossBlock: if (this.boss)` 上（Game.ts :4220 `vanillaId===113` → createBrickBoxForWallOfFlesh → startHardmode → misc15 公告），槽空整段跳过。调试召唤路径（spawnBoss :18660）有设槽所以只有玩家真玩娃娃路线踩中。修：spawnWOF 尾补 `(game as {boss}).boss = wof`（bossAI_wof.ts）。
311	
312	**验证**（探针 _wofdoll/_woftrace2，真娃娃入岩浆→hurt 击杀）：bossSlot ✓/hardMode ✓/downed_113 ✓/砖盒 32 块 ✓/**全套战利品正确**（spawnDrop 插桩溯源：vi_367 Pwnhammer+vi_2105 面具+徽章 oneOf+裂空刃+金币/药水/8 心——规则树本就 1:1）。
313	
314	**教训**：①探针 dump `d.itemId` 是**内部 id**，拿去查 `idNames.generated（vanilla id 空间）`必误读（内部 1366=心被读成毁灭者奖杯×8="垃圾掉落"假象）；断言物品用 spawnDrop 的 **key 参数**（vi_ 前缀字符串）或经 VANILLA_ITEM_KEY_BY_ID 反查。②window.__swItems 在新页面早期可能未就绪（undefined），探针用它前须等 inventory 初始化。③正则 `/^vi_367_/` 会误中 vi_3670 族——精确键匹配。
315	
316	**顺带澄清**：树下方块"无法用镐破坏"=原版 CanKillTile :62276-62315 真规则（树干/棕榈/箱柜需支撑件正下方不可挖），我们 1:1（Game.tileAboveProtected），勿当 bug。
317	
318	关联 [[wof-house-and-ores-clarify]] [[boss-summon-announce]]。
319	
320	=====FILE: worldgen-tttt-golden-channels.md=====
321	# TTTT 批（2026-08-19）：金标三通道织入 + Water Chests 重掷域 + 梳妆台注册
322	
323	## 织入资产（沿用 OOOO 先例保留）
324	- `/tmp/tttt-app`（Terraria.app 织入 exe）+ `/tmp/tttt-patch`（probelib+patcher 源）
325	- 基座 = `/tmp/sw-slp/TerrariaServer.hs.exe`（g dumps 同源；**运行时 ProbeLib 必须含 HsProbe**——WriteGrid 被重定向过去，漏了 → 无 dump + gen 崩溃重试循环）
326	- 钩子：RunPass 头（pass 名/序）+ UnifiedRandom.Next×2 头（span）+ Chest.CreateWorldChest/RemoveChest 头
327	- 产出：`SW_TT_FR_PASSES` 命中 pass 头 → `/tmp/tttt-fr/NNN_Name.{fr,chest.tsv}` + `/tmp/tttt-frw/*.wire`（红1蓝2绿4黄8致动16）；`SW_TT_SPAN_PASSES` → Next span 流
328	- 启动：`HOME=/tmp/tttt-home SW_EVIL=0 SW_HS_DUMP=1 SW_DUMP_ALL=<dir> SW_PASSCHAIN=<txt> arch -x86_64 ./TerrariaServer -autocreate 1 -worldname w -seed 9293480 -world <wld> -port 7802 -noupnp -difficulty 0`（跑后 pkill 7802）
329	- 自证法：848 dump 与 /tmp/sw-slp/g cmp 全同 + pc.txt 哈希列 diff（去 ms 列）
330	
331	## 三个大坑
332	1. **Cecil InsertBefore 锚点缓存**：`var first = instr[0]` 缓存后多次 InsertBefore → 后插者排最靠锚 → Call 排到参数前 = 栈空 InvalidProgramException（或静默 Pass 冻结 + 服务器无限重生成）。**每条插入都重取 `Body.Instructions[0]`**（oooo patcher 的写法）。
333	2. `Box(Point)` 反射探针方案废置；span 头钩 + JS 侧同流重放即可取值。
334	3. wld 不是注册表真值：Final Cleanup 尾段 RemoveChest 全表后按存活 tile 重建；生成期态只能 pass 头快照。/tmp/oooo-world/g9293480.wld 是大世界（8400×2400）跑产物——SSSS 的"sink 179 vs 350"对照基数即此误照。
335	
336	## 修复
337	1. **BuriedChestsPass.runWaterChestsPass**：两趟搜索趟2（cs:17440-17445）y 首掷与重掷同域 [⌊worldSurface⌋, UL)——曾两趟重掷都写 [50,UL) → 13/18 箱漂移 + 流雪崩（#62 → 0；span 5495=5495 全同）。
338	2. **HellFortPass.place3x2HF dresser 分支**：vanilla Place3x2(88) 在 flag2 终判前无条件 Chest.CreateChest(x-1,y-1)（cs:52169）——同位重条目→放置失败；失败尝试条目保留（孤儿）。WorldGen.ts:769 传 world.chests。地狱屋 11 座 style49 雕像帧本就正确。
339	3. **tools/_wwwrep.test.ts 槽51/53**：金标帧（tttt-fr/*.fr）+ 金标线（tttt-frw/*.wire）入口直注（SW_WWW_GF=0 可关、缺文件跳过）→ #99 259→86。
340	
341	## 定谳/移交
342	- #101：金帧金线+van注册表下 IsAGoodSpot 27=27、5 轮 Place 掷序全同 → 逻辑 1:1；残差 = JS 管线 wire/StructureMap 近似 + Temple sink 4v5（#66 通道）。下一定罪钩：TileFrame(resetFrame:true) 通用分支每调 1×Next(0,3)（cs:82448 frameNumber）——MicroBiomes actuallyPlace* 未镜像（第 5 轮 Place 后 4 掷差）。
343	- #58：137 帧债属 Traps(248@slot76)/Temple(113)/Dungeon(3×style48 雕像)——StatuesPass 无罪；(605,782) 金标帧 (18,0)。禁区按"报告勿改"处理。
344	- #99 ⑦ 重建段：输入已备（/tmp/tttt-fr/099_Tile_Cleanup.chest.tsv = slot98 物品位）——TileCleanupPass 补 cs:21484-21741 即可。
345	- #63：(474,996) JS wave65 vs vanilla 同位（y=996 门掷 roll=4 敏感带）；S-访/门掷失败零写零 SF = 双盲；需织 vanilla Spider 全访日志（S+门失败+waveN）或 C# 独立模拟器。
346	
347	=====FILE: worldgen-yyyy-fourchain-attribution.md=====
348	# YYYY 批：第三/四种子链+106槽全景+六族残余槽级归因
349	
350	- 两新链 rig 复刻 JJJJ 配方（dumpall exe md5 复核+私有 HOME+7795 自管）：s22222(小,SW_EVIL=1)与 m20260811(中,-autocreate 2,evil0)；槽105 vs vserver86 wld 八通道双 sanity PASS（豁免=非活性幽灵+lty3 微光，JJJJ 口径）。
351	- mile8 harness 尾段扩展（永久资产）：SLOT_END 14..57↔54..105+LABEL2DUMP 12 尾段 label+SW_M8_W/H/NOCACHE 参化；106 槽覆盖 105（唯 80 Guide NPC-only 无钩）。
352	- 四链全景（/tmp/panorama-yyyy.tsv）：9293480 0..53 全绿首差#59；12345 全绿含#53（首差#54 Hf=1）；22222/20260811 0..31 全绿首差均#32。
353	- 六族归因：蜘蛛巢=#63 级联（m +97k 墙，countTiles 洪泛门吃 #59 输入差；小链近净）；装饰位漂=通用放大器链 #59/#58(百格)→#64/65/67→#71 罐(+18-42k)→#82/85→#89 藤(+22-74k)→#97→#101/103；湖体±255=#49 沉降 2000×放大（m 链 A0/T2/W4 输入→L11.7k）+#97 二次沉降；背景墙=#67 Cave_Walls（#56 墙变体四链全绿）；神庙=#46 级联。
354	- ★神庙定谳：金字塔同锚同五骰同房间、唯走廊直段 vanilla 26 带 vs JS 24 带（num12=25 vs 23 同流取值 23）；错位金字塔挖死 vanilla 锚草(2694,426)→神庙 iter2 锚(3241,540)→~100k 级联。神庙 pass 无债；金字塔根因=golden 二进制 vs 三方一致反编译（1456 client+server+1405）的行为差，δ 全扫描+全掩膜对拍不可复现，swtrace 只钩单参 Next（全流仅 bound2/5/6）双参骰不可见——修复阻塞，/tmp/yy-tr/swtrace22222.log 留档续查。四链唯 s22222 建金字塔=该代码路径首次被校验。
355	- 修复零落地：(a)神庙=级联+二进制行为差不可盲改；(b)蜘蛛=XXXX 在途文件+级联。0..53 四链复核全绿无回退。
356	- 教训：milestone 绿≠掷流对齐（tile 态可掩掷差）；「采样-验证-重试」结构 pass 是小输入差→大位漂的通用放大器（BC/雕像/罐/蛛巢同款）。
357	
358	=====FILE: oooo-deep-residuals-batch.md=====
359	# OOOO 批（2026-08-19）：三残量深挖——#64/#87 八通道全清 + #77 三修 + IIII 探针雷根因（SW_EVIL=0）
360	
361	- **#64 Gem_Caves 296/931/2424W→0**：根因=placeExposed 缺 PlaceTile(178) 成功尾帧（cs:60275-81
362	  `if(tile.active()) SquareTileFrame`）的第三次 Next(3) 幽灵掷（band 内 no-write 只移流）——
363	  IIII 实测 site#0 d=+23 = 13×roll3 + 10 连带 Next(20)。连修 #92 冰晶簇归零（296→0）。
364	- **#87 Glowing_Mushrooms 697/1688→0**：三根因=①TryGrowingTreeByType(5)=GrowTree 真长蘑菇树
365	  （TreePass.growTree 复用）耗 Next(5,17)；②PlaceTile case71 香蒲支（cs:59675-703：j>ws 先
366	  PlaceCatTail 成功则 Next(14) GrowCatTail 不放 71）全缺=T519 族+流分位；③PlaceTile 成功尾
367	  SquareTileFrame(i,j)+前置 Clear(Slope)+TileFrame 头非活跃清坡（cs:82077-82）——61↔69 互换
368	  434 对全消。placePlantTile/placeJunglePlant/placeTile71 三助手统一补齐。
369	- **#77 Piles 1227→952**：placePile3x2 的 type 形参是内部 id 而 `type===186/187` 比 sheet 恒假
370	  =InvalidTile 门+Check3x2 样式族击杀链整段死代码（首例=404 沙漠化石地基 187，沙族
371	  {53,112,116,234}∪{397,398,402,399}∪{396,400,403,401} 不含 404 自杀）；KillTile 实清 type
372	  （cs:63965——IIII"不清 type"误读 cs:63935）；Check3x2 尾 destroyObject=false+5×5 TileFrame 扫
373	  可连杀邻堆（cs:49856-62）；PlaceTile 前置清锚格残值（失败也清=eff i0 语义）。残 952=邻近
374	  装饰帧杀引擎缺（KillTile 探针普查：28罐×12/165钟乳×10/485倒木×3/10门×3/26×2/135×1，
375	  dropTo 停点漂移级联）——移交帧引擎专项。
376	- **★雷根因（排雷协议）**：探针 exe 世界 vs 金标 268k 格差=邪恶类型！金标=腐化（gs.crimson=
377	  false）须 **SW_EVIL=0** 启动（passchain exe 支持）；补上后 Piles 入口整图（含残值 type）
378	  逐位全同。探针基建：/tmp/oooo-app+oooo-patch（Cecil 织 NA/NB 逐掷 FNV 哈希+PL/PS/KT 钩），
379	  对拍法=逐掷哈希流 diff→首差定位。WWW rig 修 slot93 base 91→92（冰段放置假差 281→10）。
380	- 回归：mile8 双种子绿；#93 518→10；冒烟 16.8s；无邻槽回退。
381	
382	=====FILE: deerclops-port.md=====
383	---
384	name: deerclops-port
385	description: 鹿角怪668全链落地:数据(1405提取器缺1.4.3+NPC)/AI_123九态/弹幕961·962·965/Slow buff/Camera punch;vanilla-npcs.json提取器是1405源勿信其全量
386	metadata: 
387	  node_type: memory
388	  type: project
389	  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
390	  modified: 2026-08-13T05:38:31.236Z
391	---
392	
393	2026-08-13 鹿角怪 668 全链(此前雨天自然链因数据缺静默死):
394	
395	**根因**:`tools/extract-npcs.mjs` 跑 **Terarria1405**——668 是 1.4.3 新增 → vanilla-npcs.json
396	缺 668 → fromVanilla(668)=null。★该 json 不是全量权威,1.4.3+ NPC 需手工补
397	(同 663 先例;SetDefaults 数值取 1456 :17384-17400)。
398	
399	**已落地**:
400	- 数据:json 668(60×154/ai123/7000/20/10/kb0/noGravity+noTileCollide/boss/frames25)
401	- `src/entities/bossAI_deerclops.ts`:AI_123 九态(-1 入场/0 选招/1 前刺/2 碎石/3 咆哮
402	  Slow/4 双侧刺/5 影手六连/6 回家/7 传送落地/8 消散);家 tile ai2/ai3+despawn 86400;
403	  lai3≥30 远距免伤(≥450px +1/t);选招门序(贴脸 lai1≥2 双侧刺→前刺/走动240/静立90/
404	  远距120!Slow);Movement 自管重力(探针 40×20 底/16×80 前净空,跳 -8)
405	- 弹幕:961 冰尖刺(AI_157 生长/收缩窗 [0,10)/[10,20),scale=Opacity×ai1,伤13)
406	  /962 碎石(aiStyle1 抛物+12 变体 4列×3行,伤18)/965 影手(AI_187 四变体段
407	  0/180/300/390 直选+段尾即灭,alpha 50-255)
408	- BuffType.Slow=81(vanillaBuff 32,moveSpeed÷2 :25653)——★78 已被 Poisoned 占,
409	  枚举加值前必查;原版 l10n BuffName/BuffDescription.Slow 现成,零 Mods 键
410	- Camera.addPunch/tickPunch+Renderer 帧头衰减+GameHooks.punchCamera
411	  (PunchCameraModifier 近似);Enemy.ts dispatch case 123
412	- 音效 assets 全在(deerclops_scream_0-2/ice_attack_0-2/rubble/hit/death/step)
413	
414	**坑**:①Enemy.ai0 缺省 **-1120**(史莱姆族哨兵)——非该族 AI 首帧必须
415	`if (e.ai0 === -1120) e.ai0 = 0`;②AI_124_DeerclopsLeg 是死代码(无类型挂 aiStyle124,
416	绘制单贴图)勿移植;③npcFrameCount[668]=8 与贴图 5×5=25 帧不符,渲染走
417	drawDeerclopsGrid 自管帧状态,json frames 填 25;④影手伤害:主线 15/专家被动 10;
418	⑤测试构造:选招门竞速(追击 3.5px/t 会吃掉距离差)——远距用例需持续拉距或预授 Slow 封门;
419	⑥**zoneSnow 在 game.scene(SceneMetrics)不在 Player 字段**——全量review抓回:
420	曾读 p.zoneSnow 恒 false → 回家态无法在雪原重新接战(ShouldRunAway isChasing=false 分支)
421	
422	**测试**:tests/bossAI-deerclops.test.ts 10 条;探针 _f6-boss-announce-probe.mjs 7 断言
423	(F6 召唤→"已苏醒"广播+Boss槽+家tile)。渲染层(5×5 网格+FindFrame case 668 序列表)
424	此前已就绪。遗留视觉近似:出生红雾旋转/紫电重影(Renderer 注释已登记)。
425	
426	相关:[[debug-tools-f6-f2]] [[boss-summon-announce]] [[enemy-ranged-transform-audit]]
427	
428	**★冻结事故（2026-08-19 修）**：用户实报"独眼巨鹿冻在半空"——`deerclopsMovement` 只算 vx/vy **从不积分位置**：668 是 noGravity+noTileCollide（SetDefaults :17384），原版由引擎直移穿墙，本仓各 AI 自管位移、这族漏了。症状签名：AI 状态机照跑（ai1 递增、vy 顶到 16）但坐标恒定 = 召唤在哪冻在哪。修 = movement 尾 `e.x += e.vx; e.y += e.vy`。**教训**：原测试 harness 用 tick() 手动 `e.x += e.vx` 补积分（注释"自管位移"）——测试代偿把引擎缺口焊死了；直调 AI 的测试必须只驱动一层（AI 或手动积分，二选一），凡 harness 替 src 干活的写法都要警惕"测试绿但游戏坏"。回归测试已加"位置积分"档（追击 90t x 前进>100px + 落地）。
429	
430	

```


---

## 🤖 Assistant · 2026-08-19T07:08:07.558Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have now read all the memory files. Now let me look at the archive-stream.json for 08-18 and 08-19 entries. Let me extract them.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:08:07.801Z · glm-x-preview-260804

```
所有记忆文件已处理完毕。接下来我处理 `archive-stream` 的对话片段。
```


---

## 🤖 Assistant · 2026-08-19T07:08:09.124Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nwith open('tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\n# Check structure of entries\nfor day in ['08-18', '08-19']:\n    e = data[day][0]\n    print(day, 'first entry keys:', list(e.keys()))\n    print(json.dumps(e, ensure_ascii=False)[:600])\n    print()\n    e2 = data[day][5]\n    print(json.dumps(e2, ensure_ascii=False)[:600])\n    print('---')\n\"",
 "description": "Inspect archive-stream entry structure"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:09.171Z

**📎 ToolResult**

```
08-18 first entry keys: ['day', 't', 'who', 'text', 'sid']
{"day": "08-18", "t": "00:00", "who": "🤖", "text": "## ZZ 线验收 ✅——s6666 Corruption 掷流逐位归零  **根因**（又是一笔经典转写陷阱）：`dungeonSide` 的 zLo 钳制只存在于原版**猩红分支**，我们误复制到了**腐化分支**——6666 恰好是 corruption + 边界值 380 → 差 20 列 → 整个 pass 流偏 114 万掷。", "sid": "0650e0c7"}

{"day": "08-18", "t": "00:06", "who": "🤖", "text": "## Review 结论 + B5 批完成  ### Review 结果：可靠，客户端游戏层零破坏  **零破坏证据链**： - 单人世界：新代码路径全部在 `net` 门后(`serverAuth` 默认 false、`rules` 字段惰性)，单人 `net === null` 一行不执行 - 中继房：协议字节完全兼容(v7 消息零字", "sid": "a476813d"}
---
08-19 first entry keys: ['day', 't', 'who', 'text', 'sid']
{"day": "08-19", "t": "00:01", "who": "🤖", "text": "**全案闭环——两个症状同一个根，外加 20s 看门狗**：  1. **闪烁**：整幅重建精确间隔 **20s**(24.8→43.9→63.9)= **GPU 看门狗周期**！它调 `recreateAuxCanvases` 时无条件清了 `fogPix`——但迷雾是 **CPU 数据，不是画布**，跟上下文死活无关，被白清 → 缓冲", "sid": "8405c930"}

{"day": "08-19", "t": "00:26", "who": "🤖", "text": "**没在——这是第三个工厂，还没修。** 你这次贴的栈是 `new Fp`(**构造器**形态)——我修的 BiomeBackground 是普通函数形态(`Dp`);而且你这次 107 连窗 ≈ 9 分钟持续、**暂停也在发生**(渲染循环暂停时照跑)。栈列号变了(271512→273102)说明你的新构建确实带上了部分修复——`Dp`", "sid": "8405c930"}
---

```


---

## 🤖 Assistant · 2026-08-19T07:08:15.011Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nwith open('tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\n# Extract human messages (who == 👤) from 08-18 and 08-19\nfor day in ['08-18', '08-19']:\n    print(f'===== {day} HUMAN MESSAGES =====')\n    for e in data[day]:\n        if e['who'] == '👤':\n            print(f\\\"[{e['t']}] ({e['sid']}) {e['text'][:300]}\\\")\n    print()\n\" > /tmp/human-msgs.txt; wc -l /tmp/human-msgs.txt",
 "description": "Extract human messages from archive stream"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:15.062Z

**📎 ToolResult**

```
     239 /tmp/human-msgs.txt

```


---

## 🤖 Assistant · 2026-08-19T07:08:19.535Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "/tmp/human-msgs.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:19.543Z

**📎 ToolResult**

```
1	===== 08-18 HUMAN MESSAGES =====
2	[00:01] (c44574b3) 关于浮空的那棵树我仍然觉得有问题，理论上泰拉瑞亚世界生成树木应该是强制要求底下是泥土吧，为什么会出现花草把树木的一格树干直接替换掉，造成浮空树呢，原版真是这样的吗
3	[00:06] (c44574b3) 你看我这个世界的报告，很明显非常诡异吧？这确定是原版代码能干出来的？~/Downloads/debug-report-模型根基-2026-08-17T16-04-53-399Z.json 画面里三棵树的底部都有异常，一个被蘑菇占用，两个是花，而且还由于树木下面的一格方块是被强制保护的，甚至无法使用镐子破坏他们
4	[00:10] (8405c930) 主要今天的是一个大世界存档，你要注意到这一点
5	[00:11] (8405c930) 还有不是每一次都崩溃，是某些时候负载较高时
6	[00:20] (04569a63) index-Beq_FonQ.js:507 Uncaught ReferenceError: spawnVanilla is not defined     at At.spawnCritter (index-Beq_FonQ.js:507:1257819)     at At.fixedUpdate (index-Beq_FonQ.js
7	[00:26] (04569a63) 发现又出现角色使用比如铜短剑戳击时右侧正确，左侧变成了剑柄戳击，感觉也是下午引入的bug
8	[00:27] (8405c930) 你没必要这样亲自做，你完全可以分析trace来获得加载世界时发生哪些高负载事件
9	[00:31] (8405c930) This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.  Summary: 1. Prima
10	[00:33] (04569a63) 再review一下还有没有其它类似bug，还有我使用武器时可以通过在角色左侧点击或右侧点击会自动调换角色朝向这个很好，但是镐子和斧子这些不会调换角色朝向，这个原版也是这样吗？
11	[00:34] (0650e0c7) 等这个清完是不是100%了？
12	[00:34] (0650e0c7) 所以有可能磨到100%对吧
13	[00:39] (04569a63) 再review一下是否足够可靠
14	[00:49] (04569a63) 世界生成到21%时，遇到这个 Uncaught (in promise) Error: [worldGen worker] Maximum call stack size exceeded     at gW.onEvent (index-zXEFwPhu.js:507:702807)     at t.onmessage (index-
15	[00:50] (8405c930) 有一个会话正在处理这个 世界生成到21%时，遇到这个   Uncaught (in promise) Error: [worldGen worker] Maximum call stack size exceeded       at gW.onEvent (index-zXEFwPhu.js:507:702807)       at t
16	[00:56] (04569a63) index-CqOx53Kj.js:507 Uncaught (in promise) Error: [worldGen worker] [pass 19/59 雕像宝箱] Maximum call stack size exceeded     at gW.onEvent (index-CqOx53Kj.js:507:703426)  
17	[00:58] (8405c930) ~/Downloads/Trace-20260818T005716.json.gz 现在没崩溃，我trace一个给你看看效果如何
18	[01:06] (8405c930) ~/Downloads/Trace-20260818T010547.json.gz 现在可以再看看了，我按最新的trace一下
19	[01:09] (04569a63) index-DiLhj4DX.js:507 Uncaught (in promise) Error: [worldGen worker] [pass 19/59 雕像宝箱] Maximum call stack size exceeded     at gW.onEvent (index-DiLhj4DX.js:507:703489)  
20	[01:11] (8405c930) ~/Downloads/模型根基-20260818-0111.sbw.json 这是大世界存档，就是我trace那个
21	[01:16] (8405c930) ~/Downloads/Trace-20260818T011558.json.gz 最新的trace
22	[01:18] (8405c930) 我trace是，先开启然后点击进入世界，然后进入世界后左右走走点一下鼠标，载结束的trace
23	[01:20] (0650e0c7) 未完成的继续发起新代理处理，后续这种都根据实际情况派发新的子代理，別停
24	[01:21] (04569a63) 还没好吗，你卡了快5分钟？
25	[09:39] (e65c4575) # 泰拉瑞亚反编译转译TypeScript：这本质是一场"重写"，而非"转换"  ## 🎯 核心发现摘要  - **结论先行** ：把反编译后的《泰拉瑞亚》（Terraria）转译为 TypeScript，不存在成功先例，也没有可用的自动化工具；在当前技术条件下，它实际是一项"以转译为名的重写"工程，工作量以 **多人·年** 计，而不是
26	[09:40] (a476813d) 然后看看是否能支持世界频道，就是大家联机时可以在世界房间里发消息，多人联机和服务器房间都需要支持
27	[09:42] (0650e0c7) 其实比如12345这个种子我视觉能发现的一个大差异就是，地牢顶上塔楼的顶部结构不同，原版12345种子出来的塔楼是那种金碧辉煌类似教堂顶的质感，但我不确定和我们要收敛的tower有没有关系，也许只是地牢的不同样式？你可以确认下 12345的原版wld存档：~/Downloads/12345世界.wld
28	[09:46] (04569a63) Uncaught (in promise) Error: [worldGen worker] [pass 19/59 雕像宝箱] Maximum call stack size exceeded     at wW.onEvent (index-W778C8nG.js:511:703595)     at t.onmessage (ind
29	[09:47] (8405c930) 为什么这么小的光标也有很大危害？
30	[09:49] (8405c930) 明白，那再review一下排除没有类似问题
31	[09:55] (8405c930) 最后再review一下
32	[10:11] (e65c4575) 把我们最近最新的迭代进度也更新进来
33	[10:12] (e65c4575) 把我们最近最新的迭代进度也更新进来，也要包含各种优化、踩坑等
34	[10:25] (0650e0c7) 我发现现在生成世界的浮空岛的房子的房门全没了，是我们哪次对齐搞错了吗？ 而且我还发现和12345原版世界的一个差异点，从左到右三个浮空岛中间那个浮空岛的门朝向我们和原版是相反的
35	[10:44] (c44574b3) 为啥杀死肉山Boss后没有出现小屋子？里面应该有神圣锤啥的？好像也没触发肉后世界变化
36	[11:07] (0650e0c7) 现在总进度到哪了
37	[11:09] (a476813d) Uncaught TypeError: Cannot set properties of undefined (setting 'appearance')     at Object.onJoinRoom (index-DiV0BwU7.js:885:22912)     at r.onclick (index-DiV0BwU7.js:6
38	[11:17] (0650e0c7) 有可并行的可以出子代理处理，提高资源利用效率
39	[11:23] (c44574b3) 肉后的变化有正常工作吗？比如怪物变强、出现神圣之地、腐化之地/猩红之地会蔓延等等一系列机制
40	[11:27] (c44574b3) 然后再检查各种boss的召唤方式、掉落物、触发事件是否全部齐全无误
41	[11:30] (04569a63) 全面审计我们代码里剩余哪些“近似”“登记后续处理”“暂不接线”“未实装”等类似代码，看看实际还有哪些不完整的
42	[11:45] (04569a63) 全面补齐不遗留，不做任何近似A到D全部
43	[11:46] (0650e0c7) 我看NNN说遗留的一些是啥
44	[11:51] (8405c930) ~/Downloads/Trace-20260818T115011.json.gz 本机测试联机时，双开浏览器窗口，后加入的这个进入世界后崩溃，并且房主也会走动很卡像是网络同步不过来还是因为啥
45	[11:52] (0650e0c7) NNN那个的也必须修齐
46	[11:58] (0650e0c7) This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.  Summary: 1. 主要请求与
47	[12:01] (04569a63) Game.ts的错误是哪个会话干的，修一下先，然后继续修复缺口
48	[12:02] (8405c930) 我的GPU资源非常充足
49	[12:02] (8405c930) 我的GPU资源非常充足，为什么总是挤爆
50	[12:05] (8405c930) 你评估一下，代价最低收益最高的部分迁移到webgl2的有哪些可以立即做？
51	[12:05] (8405c930) 你评估一下，代价最低收益最高且不会影响效果的部分迁移到webgl2的有哪些可以立即做？
52	[12:08] (04569a63) inlic@mac game % npm start  > sandboxworld@0.1.0 start > vite build && vite preview  vite v5.4.21 building for production... [atlas-lint] 753 表全自洽 ✓ (0 warn) [l10n-audit]
53	[12:09] (8405c930) 把这个计划落到记忆和文档，然后先执行1和2
54	[12:18] (8405c930) 在你改造的过程中先派一个子代理分析下当前的负载压力，然后可以预估出你改造webgl2后的提升~/Downloads/Trace-20260818T121528.json.gz
55	[12:31] (ec878731) 继续补齐
56	[12:33] (d76053b3) 帮我确认下原版的水草或是丛林的下垂藤蔓被打掉中间一节后，其它节会不会一起消失，比如按照物理规律来说，下垂藤蔓打掉中间部分，那中间往下应该也会掉或消失吧，目前我们的版本打掉中间后下方部分还停留在原位
57	[12:43] (8405c930) GL绘制的远景背景图和打开的地图是垂直方向颠倒的
58	[12:49] (8405c930) 现在似乎好了，但我点开小地图打开地图后，发现地图的一些图块会逐渐变成#362CFF这个颜色的退化块，像是别回收掉一样
59	[12:51] (d76053b3) ~/Downloads/Trace-20260818T121528.json.gz 我记得打掉这种小蜂巢是会有蜂跑出来的吧
60	[12:52] (8405c930) 我打开了F4消除迷雾过，你也可以试试
61	[12:52] (d76053b3) ~/Downloads/debug-report-新鲜的骄傲大海-2026-08-18T04-51-01-427Z.json 我记得打掉这种小蜂巢是会有蜂跑出来的吧
62	[12:53] (0650e0c7) 现在还有可以并行的吗，有的话可以继续开子代理
63	[13:22] (8405c930) 现在又一次出现远景背景图以及打开的地图垂直颠倒问题了，这是第二次犯同样的错误了吧
64	[13:29] (ec878731) review一下确保移植完整准确
65	[13:30] (cb3a4729) 检查下我们光标的图标失效的问题，我们光标比如移动在宝箱上时光标会有另一个贴图出现，但是现在这个贴图是全黑的
66	[13:33] (8405c930) ~/Downloads/Trace-20260818T133033.json.gz 这是最新构建的trace，目前行走时还是会有掉帧现象，你可以研究下，另外我砍树砍着砍着有一棵树看完掉落自动收集物品时突然崩溃
67	[13:37] (04569a63) 检查处理是否已完整
68	[13:37] (c44574b3) 检查处理是否已经完整
69	[14:06] (8405c930) WebGL: INVALID_ENUM: samplerParameter: invalid parameter o @ index-QOk4eVif.js:541 init @ index-QOk4eVif.js:541 I6 @ index-QOk4eVif.js:541 render @ index-QOk4eVif.js:541 
70	[14:09] (ec878731) 砍树时书上为什么会掉落雕像啊
71	[14:09] (ec878731) 砍树时树上为什么会掉落雕像啊，掉了个靴子雕像
72	[14:13] (cb3a4729) 感觉鸟还是燕子的动画贴图没正确调度，在地上的时候仍然使用的是飞行中的动画
73	[14:13] (cc0b5a07) 蠕虫罐头x1 {(lnputTrigger_ToggleOrOpen} to open开 拿击 全部放入 快速堆叠 为啥蠕虫罐头的说明有问题
74	[14:14] (04569a63) 继续补齐缺口
75	[14:14] (c44574b3) 感觉兔子的能跑动画不对，帧换得非常快
76	[14:18] (8405c930) ~/Downloads/Trace-20260818T141501.json.gz 再看看这个trace怎么样
77	[14:22] (0650e0c7) ~/Downloads/debug-report-美好的妖精粪便-2026-08-18T06-22-07-164Z.json 恶魔祭坛生成在地牢里不对吧？
78	[14:28] (9adce254) 需要完整移植，不能漏
79	[14:31] (1fc2b821) 我记得地域里的骨龙在接近时本身是有音效的，你要检查下各种怪物生物本身的音效是否正确移植完整
80	[14:32] (cb3a4729) review看还有哪些不对的
81	[14:32] (d76053b3) 之前走上角的工具栏切换不同东西的时候上方的文字会跟着变化，现在怎么只会显示“物品”了？
82	[14:34] (d76053b3) This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.  Summary: 1. Prima
83	[14:35] (8405c930) ~/Downloads/Trace-20260818T142108.json.gz 给你个长流程的trace，你继续分析一下，我希望在当前的性能基础上再找优化点，而不只是满足于不崩溃，而是要达到尽量不掉帧
84	[14:35] (cc0b5a07) 检查一下是否还存在其他类似问题
85	[14:36] (ec878731) 检查我们现在光标移到道具或物品上时的内容气泡是否对齐原版，感觉相比原版缺了不少信息，我记得武器啥的还会有攻击力啥的吧
86	[14:43] (8405c930) ~/Downloads/Trace-20260818T144141.json.gz 我把插件禁用了，然后按照最新源码编译结果进去存档，向右跑动几步后突然崩溃
87	[14:50] (8405c930) review一下，确保不会有任何其他泄漏点
88	[14:51] (04569a63) 继续处理完整，我记得还有宝箱怪
89	[14:51] (0650e0c7) 如果有可以分配的并行工作，可以新开子代理
90	[14:51] (c44574b3) 继续推进遗留
91	[14:51] (cb3a4729) 再进行最终review
92	[14:59] (cc0b5a07) 最终review
93	[15:01] (8405c930) index-C2bSjqfB.js:917 TypeError: Cannot set properties of undefined (setting 'MAX_CHUNKS')     at yt.afterWorldLoad (index-C2bSjqfB.js:542:736961)     at yt.loadWorld (in
94	[15:09] (ec878731) 最后再review一下，包括气泡UI样式是否对齐
95	[15:11] (8405c930) 然后检查下我们的资源下载是串行吗？可以根据下载和处理速度自适应并行吗？
96	[15:17] (1fc2b821) 子代理好了，检视一下
97	[15:17] (8405c930) 检查下我们有做锁帧吗？原版锁在60fps
98	[15:22] (9adce254) review一下
99	[15:23] (ec878731) 低频的也必须接入完整
100	[15:23] (ec878731) 低频的也必须接入完整，已经禁止低频的不做（要计入记忆）
101	[15:24] (8405c930) 我们锁帧对于我们性能有没有优化？是否降低负载和提升稳定性？
102	[15:26] (8405c930) 原版还有哪些类似优化，我觉得这个收益非常高，为啥早期没提起？
103	[15:29] (cb3a4729) 最终清零review，确保没有遗漏
104	[15:31] (8405c930) 异步光照我们做的话代价是什么
105	[15:32] (9adce254) 登记的也全部做完，禁止遗漏或登记不做
106	[15:35] (8405c930) 先不考虑把，我记得原版还分几个画质档位，我们怎么做的？
107	[15:36] (0650e0c7) 当前进度如何了，总进度多少？咋感觉一直干不完
108	[15:41] (8405c930) 全部对齐，水面波动模拟起个子代理去对齐，务必完整实现
109	[15:45] (8405c930) 旧版引擎就不要了
110	[15:49] (8405c930) 自动画质系统我们可以接入吗？会有什么收益？另外水面波动模拟的代理我已经恢复了
111	[15:54] (573d63f5) 离谱的是在你这里面没问题，但是在世界里的就是会有缝，包括沙漠的仙人掌也是有这种问题
112	[15:54] (e65c4575) 然后可以全面整理一下我们实现的版本和原版的各项差异，用实证来说明不是照搬就能解决问题
113	[15:58] (e65c4575) 太简单了，需要引擎级别的差异
114	[16:06] (a476813d) > sandboxworld-server@0.1.0 start > tsx src/index.ts  [server] 中央服务器 ws://0.0.0.0:7777（lobby http://0.0.0.0:7778/rooms，1×RoomHost 每工 32 房） [host] RoomHost 就绪（worlds=~/Pro
115	[16:12] (8405c930) 世界渲染好像全坏掉了，地面以下的方块渲染全部偏移左上了
116	[16:13] (8405c930) 我先看是不是另一个修正树木和仙人掌绘制导致的异常
117	[16:16] (573d63f5) 好了，目前仙人掌确实没缝了，可是树冠和树干之间仍然有些有缝
118	[16:18] (8405c930) 确定是那边的锅，你现在先看看这份trace，多开世界时的崩溃~/Downloads/Trace-20260818T160944.json.gz 看下当前瓶颈在哪
119	[16:22] (1fc2b821) 不允许遗留，全量执行完毕，可以多开子代理，然后你主进程先review已经实施的代码
120	[16:23] (9adce254) review一下
121	[16:28] (8405c930) index-DZVhAMy_.js:921 [Game] 检测到 2 个同源游戏实例——已进入双开经济档(chunk≤160/GL≤96MB)  index-DZVhAMy_.js:546 [rload] vanilla/Extra_58.png | vimages=190 index-DZVhAMy_.js:546 [rload] va
122	[16:43] (8405c930) Background agent "移植水面波动模拟全链" was stopped by the user.
123	[16:44] (8405c930) ~/Downloads/Trace-20260818T164135.json.gz index-Mn5fSGUz.js:921 [Game] 检测到 2 个同源游戏实例——已进入双开经济档(chunk≤160/GL≤96MB)  index-Mn5fSGUz.js:546 [rload] vanilla/Extra_58.png | vi
124	[16:47] (573d63f5) ~/Downloads/debug-report-模型根基-2026-08-18T08-47-06-154Z.json 你可以直接看离角色当前位置最近的3棵树都有缝
125	[16:47] (ec878731) 最终清零review
126	[16:50] (8405c930) 我们开局为什么要解码几百MB？开局只有一小块地方探索
127	[16:54] (8405c930) 引起崩溃的核心原因具体是哪些，根据严重程度排名
128	[16:56] (8405c930) 显存预算超限我们现在有什么办法不要占用这个预算吗？比如你说的webgl2？
129	[16:59] (8405c930) 先做了吧
130	[17:04] (1fc2b821) 有个子代理在补全音效，还要注意音效的音量以及衰减是否正确
131	[17:06] (573d63f5) ~/Downloads/debug-report-模型根基-2026-08-18T08-47-06-154Z.json 和缩放无关，任何缩放刻度上都会有缝，缝就是横线
132	[17:14] (0650e0c7) 现在世界生成时仍然会生成没有树根的树~/Downloads/debug-report-美好的妖精粪便-2026-08-18T09-13-37-870Z.json 就是树木最底下不是泥土而是花草
133	[17:17] (1fc2b821) This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.  Summary: 1. 主要请求与
134	[17:18] (1fc2b821) 底下蠕虫的音效明显错误，在地底穿梭的声音全部变成了boss唤醒音效！而且现在杀死洞穴蝙蝠连死亡声音都没了！
135	[17:22] (04569a63) 继续处理完整
136	[17:23] (0650e0c7) 还有为什么早上我创建的世界的地牢还有那个类似教堂尖顶，现在创建的就没尖顶了？是随机的吗
137	[17:27] (8405c930) 开第二个tab时，依然碰到崩溃且释放第一个tab依然无法恢复，最终彻底崩溃 Game] 检测到 2 个同源游戏实例——已进入双开经济档(chunk≤160/GL≤96MB) console.warn @ :4173/assets/index-UQvucXrq.js:921 presence.onChange @ :4173/assets/
138	[17:31] (8405c930) 如果我们支持CPU软渲染开关会发生什么呢，如果某些CPU本身很强大呢？ 还有你前面做的CPU处理minimap的导致了迷雾消失了，入场就没有任何迷雾
139	[17:35] (8405c930) 加个渲染模式吧，不要检测什么第2实例了，把第2实例的检测全部移除。我们只在GPU渲染崩溃无法继续渲染时直接自动切换CPU软渲染，如果条件符合可以考虑再切回GPU渲染
140	[17:40] (8405c930) review一下是否实现精准可靠
141	[17:46] (8405c930) 最终清零review
142	[17:46] (c44574b3) 不用等了，你结束了吗
143	[17:47] (9adce254) 最终清零review
144	[17:52] (ec878731) 现在移上去的气泡效果不对，几乎是透明的，原版不是这样 另外我们1234567890键切换工具栏指定物品的功能又失效掉了？谁改的？
145	[17:53] (04569a63) 现在生物的掉落物开始混乱了，打死金鱼居然出现“恐惧之魂”？
146	[17:56] (8405c930) 为啥现在minimap的迷雾更新很延迟？我走到一个地方等了10秒才清除该区域迷雾
147	[17:57] (d76053b3) index-CBL3JVfp.js:921 TypeError: Cannot read properties of undefined (reading 'destroy')     at renderer.onCanvasRecreated (index-CBL3JVfp.js:546:716788)     at Ni.recrea
148	[18:01] (04569a63) // ---- 放置块 tile 回填补遗（2026-08-13 实装缺口扫描 §3）：vanilla.json //  .items 的 createTile 有值、extract-itemfunc 提取漏（共享 case 段算式不在 //  单值提取面内）→ def.tile 未回填 = 放置静默无效。5 件以 TEdit 数据为权威
149	[18:02] (04569a63) 这是正确的最佳实践吗？维护不会有风险吗？就像你前面错误注册一样
150	[18:04] (8405c930) ❯ index-CBL3JVfp.js:921 TypeError: Cannot read properties of undefined (reading 'destroy')       at renderer.onCanvasRecreated (index-CBL3JVfp.js:546:716788)       at Ni.
151	[18:11] (8405c930) index-CnRnfpRS.js:921 [Renderer] 渲染模式切换 → CPU 软渲染(零 GPU 预算) index-CnRnfpRS.js:546 [rload] vanilla/Extra_58.png | vimages=184 index-CnRnfpRS.js:546 [rload] vanilla/Misc_no
152	[18:14] (8405c930) 不对，我两个窗口都是使用CPU软渲染
153	[18:16] (04569a63) review一下，别再犯错
154	[18:23] (8405c930) ~/Downloads/初始档.json.gz ~/Downloads/崩溃档.json.gz 我这边是崩溃的60fps，初始档是进第一个，然后崩溃档是另一个tab再进入就观测崩溃了 [Renderer] 渲染模式切换 → CPU 软渲染(零 GPU 预算) console.warn @ index-CnRnfpRS.js:921 set
155	[18:29] (8405c930) CPU渲染开启时无法禁用GPU渲染吗？你找一下资料，肯定有什么解决方案
156	[18:30] (8405c930) [REDACTED]   MCP接入   使用MCP协议快速将UniFuncs API能力接入到您的大模型系统：   Streamable HTTP 通信（推荐）   https://mcp.unifuncs.com/mcp   需在headers请求头中添
157	[18:36] (0650e0c7) 世界生成卡死在正在放置机关 - 37%，可能worker里有某种异常
158	[18:37] (8405c930) npm run play无效，他好像会在已有浏览器窗口新增一个tab页
159	[18:39] (8405c930) npm run play无效，他好像会在已有浏览器窗口新增一个tab页 单窗口双世界是什么方案，仔细说下
160	[18:50] (0650e0c7) 它的修复是不是卡住了，我看没动
161	[18:53] (8405c930) npm run play冷启动的chrome依然面对一模一样的问题，GPU依然爆
162	[18:54] (0650e0c7) 没有用依然卡在37% 放置飞镖机关
163	[18:54] (0650e0c7) 没有用依然卡在37% 放置飞镖机关 [worldGen] ⚠️ 生成疑似卡死：已 39s 无进展（最后进度：地表装饰 [generate]）。pass 为同步代码,内部死循环会停摆事件循环——排查该 pass 内的 while/拒绝采样（参考 liquidType +1 编码血案,3 分钟硬超时后将自动终止） console.error 
164	[19:00] (c3931993) 恢复一下我们刚刚GPU渲染卡死优化的那个会话
165	[19:02] (8405c930) 用我们mcp的搜索
166	[19:15] (1fc2b821) review一下
167	[19:20] (1fc2b821) 最终清零review
168	[19:23] (a476813d) 看下当前是否有vitest孤儿进程
169	[19:32] (1fc2b821) 遗留的帮我一起全部对齐做完整
170	[19:38] (8405c930) 没用你那样启动的chrome，gpu依然启动 Graphics Feature Status ======================= *   Canvas: Hardware accelerated *   Direct Rendering Display Compositor: Disabled *   Compositing:
171	[19:39] (8405c930) 有没有可能我们可以通过某些优化手段避免掉IOSurface 失败
172	[19:46] (8405c930) user@mac game % npm run playsoft    > sandboxworld@0.1.0 playsoft > node scripts/play.mjs --soft  无效 URL: --soft
173	[20:23] (8405c930) 开始你的大型优化吧
174	[21:08] (8405c930) review一下，避免在发生这种事，而且建议能不能在下次泄露或不合理分配问题能够及时抓出来
175	[21:12] (04569a63) 继续不全，1:1对齐完整
176	[21:12] (0650e0c7) 除了两个代理外如果有可以并行的也开子代理加速推进
177	[22:41] (1fc2b821) review一下
178	[22:41] (8405c930) 写一份完整的报告给我，我要知道发生了什么，以及原理
179	[22:49] (8405c930) 我们现在每帧会用到多少canvas？
180	[22:55] (8405c930) 云染缓存到底在干啥，优化一下吧
181	[23:04] (cc0b5a07) 我记得角色在冰面是会脚滑的，你检查下我们角色或npc或任何怪物、生物等的脚部的摩擦力是否对齐原版
182	[23:05] (8405c930) 那我们画云使用webgl2可以稳定实现吗
183	[23:12] (8405c930) 做吧，直接GL化，如果不支持gpu的再回退到canvas2d，而且我发现现在好多云好像不渲染了
184	[23:12] (8405c930) 做吧，直接GL化，如果不支持gpu的再回退到canvas2d，而且我发现现在好多云好像不渲染了 [rload] vanilla/Misc_noise.png | vimages=202 index-i1b0TmQ6.js:548 [rload] vanilla/Misc_Ripples.png | vimages=203 index-i1
185	[23:23] (cc0b5a07) review一下
186	[23:39] (d76053b3) 现在仍然有一些动画播的过快的生物动画帧，比如走路的金鱼，非常鬼畜
187	[23:39] (ec878731) 气泡依然有点过于透明
188	[23:43] (8405c930) review一下，然后顺便看下这个[canvas哨兵] canvas 分配异常:连续窗 streak(≥300/窗:3连 / ≥100/窗:3连),最近窗 61/s——疑似泄漏/不合理分配。出生栈样例:at document.createElement (http://localhost:4173/assets/index-BJP2tvC
189	[23:50] (8405c930) ~/Downloads/debug-report-困惑的要塞-2026-08-18T15-44-37-389Z.json 发现有些贴图加载不及时，我要手动破坏生命树的方块才进行了贴图渲染 另外我还发现minimap小地图里的迷雾经常一闪一闪的，隔一段时间突然迷雾消失全亮，然后瞬间又恢复迷雾状态
190	
191	===== 08-19 HUMAN MESSAGES =====
192	[00:25] (8405c930) 你修复途中我还遇到了这些问题：[rload] vanilla/Misc_noise.png | vimages=191 index-Cgtbu_UR.js:565 [rload] vanilla/Misc_Ripples.png | vimages=192 index-Cgtbu_UR.js:565 [rload] vanilla/Dus
193	[00:27] (a476813d) 现在再看看看看
194	[00:28] (a476813d) node有没有孤儿？
195	[00:36] (8405c930) 我确定是最新构建
196	[00:36] (8405c930) 我确定是最新构建，你看脚本的hash都不同
197	[00:57] (04569a63) ~/Downloads/debug-report-困惑的要塞-2026-08-18T16-57-23-890Z.json 独眼巨鹿boss无法正常工作，冻结在半空不动
198	[01:04] (8405c930) 现在基本稳定了，就是我好奇为什么我们之前的时候发现willReadFrequently依然不能算CPU渲染？还是会走GPU渲染
199	[01:08] (8405c930) 然后检查一下我们之前移植的水体动态渲染，感觉还有问题，一个是它好像只处理的单格水对于半格的那种方块浸润水未做处理，另一个是效果和原版好像不一致
200	[01:23] (cb3a4729) 扔出去的荧光棒之类的存档有保存下来吗
201	[08:28] (0650e0c7) 进度如何？
202	[08:31] (0650e0c7) 还有可以并行的任务给新子代理了吗？
203	[08:31] (8405c930) 处理好了吗
204	[09:59] (a476813d) 看下现在有没有vitest或node或chrome的孤儿进程
205	[10:02] (a476813d) chrome孤儿kill把
206	[10:09] (c44574b3) 现在角色掉落过程中没有任何饰品却可以在半空再次跳跃来避免摔死。这个是不是不对？，我记得这得有比如空中瓶那种佩饰才能二段跳才有的吧
207	[10:10] (04569a63) 小地图打开地图后放大到一定程度地图会变成全黑的，我得缩小到一定程度才会恢复正常？ 另外地图打开后地图的背景图好像选定有点问题，会根据缩放自己变动？
208	[10:19] (8405c930) 全部和原版对齐一下，除了“地下半砖顶部顶点色渐变(逐 quad 垂直渐变，Canvas 2D 近现代价太高，洞穴暗背景下视觉差极小)”
209	[10:28] (8405c930) ~/Downloads/debug-report-畏缩的床-2026-08-19T02-27-56-560Z.json 我之前提到的不对，比如这个画面里的水的页面有两条水面线，一条在另一条的下面一格，正好1格距离
210	[10:31] (c44574b3) 我感觉我们需要一个行为录制的方案，比如长按F5来启动场景的整体“录制”，不是视频那种录制，而是比如用户做了啥，场景发生了哪些变动，角色发生了什么变动，NPC做了啥、怪物做了啥、生物做了啥，啥被砍掉了，掉落了什么等等，这种依赖时序因果关系的录制，对于调试非常重要
211	[10:37] (ec878731) 现在又过于不透明了
212	[10:38] (d76053b3) 修复一下角色死亡后的怪物寻路异常问题，比如恶魔眼这个小怪，在角色死亡后会反复左右朝向抽搐，并且在角色死亡处直接飞升天
213	[10:39] (d76053b3) 修复一下角色死亡后的怪物寻路异常问题，比如恶魔眼这个小怪，在角色死亡后会反复左右朝向抽搐，并且在角色死亡处直接飞升天，原版看看怎么处理角色死亡后的怪物寻路
214	[10:45] (8405c930) This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.  Summary: 1. Prima
215	[10:50] (8405c930) 从你的截图来看是正确的，但我发现最左侧水面波线未覆盖完整，相当于最边缘的半砖水可能没有进行液面效果适配 https://maas-log-prod.cn-wlcb.ufileos.com/anthropic/8405c930-04c0-4d16-9037-36f3dcd374b8/dline2.png?[签名参数已移除] 这张只有一个液面
216	[10:52] (04569a63) 现在地图后面背景图乱动的解决了，但地图放大后全黑依然存在，全黑时只有我和NPC的头像存在
217	[10:54] (d76053b3) 还有鱼经常会蹦出水面，这个是正常的吗？
218	[10:54] (d76053b3) 还有鱼经常会蹦出水面到外面的土地上继续蹦，这个是正常的吗？
219	[10:55] (d76053b3) 还有鱼经常会蹦出水面到外面的土地上继续蹦，这个是正常的吗？比如食人鱼
220	[11:00] (8405c930) 这种方式不对，这张图里我看到有第二条水面线，也是差一格，你干脆另起一个调试页面还原这个线程的画面，我给你标注哪些格子有问题以及第二条水线位置
221	[11:02] (d76053b3) review一下其他有没有类似问题
222	[11:04] (d76053b3) 最好对所有怪物的AI也单开子代理全审查是否1:1对齐原版行为
223	[11:07] (0650e0c7) 还有能并行的任务吗，当前进度到哪了
224	[11:07] (8405c930) 别重新生成世界，~/Downloads/畏缩的床-20260819-1106.sbw.json，直接复用存档
225	[11:09] (8405c930) 不行，你的问题格标注有偏移不是我鼠标点击位置
226	[11:12] (8405c930) 还有昨晚我还能多开四五个世界都不会崩溃，今天又出现了开2个世界就崩溃了 ~/Downloads/Trace-20260819T111122.json.gz
227	[11:21] (8405c930) 不要这种降级的，我们要从我们自己出发，看还有没有优化空间，你这样通信搞得很奇怪
228	[11:27] (04569a63) index-CHYbtgbt.js:940 [drawFullMap] GL 合成中心恒黑但该点已探索——切 2D 兜底(本次开图会话)  {probe: Array(4), zoom: 1.3726820864, wtx: 2096, wty: 230} probe :  (4) [0, 0, 0, 1] wtx :  2096 wty
229	[11:28] (c44574b3) ~/Downloads/debug-report-锡桌子-2026-08-19T03-27-56-496Z.json 已经录制了
230	[11:33] (8405c930) BiomeBackground 家族那边并行会话应该处理完了，你可以也看看 然后处理完后再评估一下最新的IOSurface占用情况，还有染色那个我记得我们不是改造过去GL了吗，为什么说也在占用大量画布呢
231	[11:34] (cc0b5a07) F6的面板里boss为啥没看到世纪之花和石巨人啊
232	[11:39] (cb3a4729) 为什么原版不保存呢，是有什么顾虑吗
233	[11:41] (04569a63) 可是我发现地图迷雾消失了？正常是有迷雾的
234	[11:42] (d76053b3) 全量review，可以并行子代理，全部修复1:1对齐，禁止近似实现
235	[11:43] (cb3a4729) 说到这个，玩家好像是可以带走在其他世界的物品的，我们现在好像进入新世界都是全新的物品？
236	[11:43] (cb3a4729) 说到这个，玩家角色好像是可以带走在其他世界的物品的，我们现在好像进入新世界都是全新的物品？
237	[11:47] (04569a63) ~/Downloads/debug-report-锡桌子-2026-08-19T03-47-05-863Z.json 你看
238	[11:52] (e65c4575) 更新我们最新的对话记录到页面，并且整体检查我们整个页面的行文逻辑和修正
239	
240	

```


---

## 🤖 Assistant · 2026-08-19T07:08:21.941Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have all human messages. Now I need some interesting bot messages too. Let me extract some key bot moments — epiphanies, discoveries. Let me search for interesting phrases in the bot messages of 08-18 and 08-19.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:08:22.334Z · glm-x-preview-260804

```
现在我来挖掘最有意思的机器人瞬间——顿悟、深夜突破以及生动时刻。
```


---

## 🤖 Assistant · 2026-08-19T07:08:25.636Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nwith open('tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\n# Find bot messages with epiphany-like content\nimport re\nkeywords = ['铁证', '真凶', '定罪', '破案', '顿悟', '原来', '真相', '全等', '零差', '奇迹', '抓到', '落网', '首战', '告捷', '里程碑', '完美', '天下', '居然', '竟然', '太美', '漂亮', '精确相等', '逐位']\nfor day in ['08-18', '08-19']:\n    print(f'===== {day} BOT HIGHLIGHTS =====')\n    for e in data[day]:\n        if e['who'] == '🤖':\n            t = e['text']\n            if any(k in t for k in keywords) and len(t) > 80:\n                # Score by keyword count\n                score = sum(t.count(k) for k in keywords)\n                if score >= 2:\n                    print(f\\\"[{e['t']}] ({e['sid']}) {t[:400]}\\\")\n                    print()\n\" > /tmp/bot-highlights.txt; wc -l /tmp/bot-highlights.txt",
 "description": "Extract bot epiphany messages"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:25.686Z

**📎 ToolResult**

```
      32 /tmp/bot-highlights.txt

```


---

## 🤖 Assistant · 2026-08-19T07:08:28.897Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "/tmp/bot-highlights.txt"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:28.906Z

**📎 ToolResult**

```
1	===== 08-18 BOT HIGHLIGHTS =====
2	[00:43] (04569a63) 复查完成——**又抓到并修掉 1 个真隐患**，其余面确认可靠。  ## 复查方法  把今天全部改动列成风险清单（召唤槽位权重/双子系统/弹幕旋转五档/出弹锚点/贴地+4/睡床锚点/短剑链球中心锚/工具转身/spawnVanilla 上提），挑风险最高的两处深查，再做全量大回归。  ## 抓到的问题：睡眠物理锁漏了 sleeping  坐
3	
4	[08:30] (0650e0c7) ## 双线已派  | 线 | 任务 | 里程碑目标 | |---|---|---| | **LLL** | #32 入口主体（Tower 楼梯/堡周 A=1319 T=1496） | #32→全绿 → 里程碑 #33+ | | **MMM** | #49 丛林沉降族（T60>59×264 + Lt Y2×211 + L3740） | #4
5	
6	[10:52] (0650e0c7) ## LLL 线验收 ✅——G 段核销+入口塔体零差+谱系大澄清，OOO 已派  **LLL 战果**： - **G 段根因修复**：宝箱放置坐标 `(int)endX - half`（先截断后±）vs double 直±——小数尾抬 1 格 → 修后**流哈希=vanilla 真值全等** - **谱系大澄清**：之前追的 15k+ "
7	
8	[12:46] (8405c930) 地图修复后**完美零差**(1276 quad 确认 GL 分支已命中)。背景还差 avg 17.2——这是 Skia 高质量降采样(盒式滤波)vs GL 双线性的差异；之前 smooth=false 更错(LINEAR 时 7.7)。正解：**mipmap**(`LINEAR_MIPMAP_LINEAR` 最接近 Skia 行为)。改两
9	
10	[13:18] (0650e0c7) **VVV 批交付 ✅——#49 大幅塌缩，两根因都是重量级语义发现**  | 通道 | 批前 | 批后 | |---|---|---| | T | 450（含 60>59×264）| **10**（60>59 **清零**，烧除 77 格逐位全等）| | L / Lt | 3477 / 57 | **0 / 0** |  1. **60
11	
12	[14:46] (0650e0c7) **全量里程碑复跑确认：槽 0-53 八通道全部零差——“首差边界：无”**（27 秒跑完，26.6s 生成+对拍）。  今天的战果合成一张图：  | 区段 | 状态 | 清零者 | |---|---|---| | 槽 0-31（地形→蜂巢前）| ✅ 早已全绿 | 历史批次 | | 槽 32 地牢 | ✅ 今日归零 | OOO（5 根因）
13	
14	[16:08] (573d63f5) **真凶抓到并修复了**——你那句“仙人掌也有”是破案关键。  ## 根因：chunk 拼装 × 非整数缩放  游戏地形不是一整块画的，是按 **16×16 格的 chunk 画布拼接**的。旧拼装公式把每块 chunk 画到 `块位置 × 缩放` 的位置上：  - 默认缩放 1.25：`256×1.25 = 320` **恰好整数像素*
15	
16	[17:16] (573d63f5) **这轮抓到真凶并修复了**——你那句“横线、任何缩放都有”加上报告数据，把案子破了：  ## 根因：夜间高对比下的摆动层边缘跳变  你报告里的区域是**夜间无光区**（截图亮度只有 5-8，全黑）。对你截图做全图水平线检测，23 条横线全部命中**枝/冠的行**（枝行 575/577/578 全中；三个冠交界行 573/574/575 
17	
18	===== 08-19 BOT HIGHLIGHTS =====
19	[01:30] (0650e0c7) **🎯 里程碑达成：双种子里程碑链 0-53 全绿**  QQQQ 清掉了最后一格——根因相当精致：原版的 `LavaCheck` 是“沙漠爆破前导+液体检查”的包装，但**生成收尾的全图检查直调裸 LiquidCheck、不走爆破**；我们的收尾分派错走了带爆破的包装，把一格密闭岩浆斜梯当成了爆破源，波及隔壁密闭水袋（水→岩浆，恰 1 
20	
21	[04:34] (0650e0c7) **SSSS 批交付 ✅——#93/#77 双双归零，两桩悬案仲裁终结**  - **#93 随机宝石 → 0/0**（引擎接线+一处前置清） - **#77 矿骨堆 → 0/0**：两格悬案真相漂亮——原版有两个 `SolidTile2` 重载，**坐标版带平台顶坡豁免、Tile 版没有**（RRRR 怀疑的金标编码差不成立）；2520
22	
23	[08:28] (0650e0c7) **总进度：约 95%**（今早的 85-90% 已跨过），且剩余路径完全具体化了。  **硬指标（当前实况）**：  | 维度 | 状态 | |---|---| | 里程碑链 9293480 | **0-53 槽八通道全绿** ✅ | | 里程碑链 12345（你的种子）| **0-53 槽八通道全绿** ✅ | | 尾段 52 槽（5
24	
25	[10:36] (0650e0c7) **YYYY 批交付 ✅——四链全景落地，六族残余全部钉到槽号**  三个大产出：  1. **mile8 永久扩展到 105/106 槽**——里程碑工具现在能逐槽比完整条链（以前只到 53） 2. **两条新链 sanity 双 PASS**（s22222/m20260811，槽105 与 .wld 逐格零差），四链全景表出炉：929
26	
27	[11:09] (04569a63) 根因抓到了，三层修复已落地：  ## 根因（显微镜探针定罪）  “只剩头像”这个细节是关键——头像是 2D 后画层，说明**整块 GL 地图合成层黑了**。逐层隔离后铁证：  - CPU 侧小地图像素 93% 彩色不透明、中心=(191,142,111) 泥土色 ✓ - GPU 纹理 `isTexture` 存活、无 GL 错误、整幅重传
28	
29	[11:28] (04569a63) **真凶落网**：`samp.linear` 采样器的 MIN_FILTER 是 `LINEAR_MIPMAP_LINEAR`，而小地图/迷雾纹理是 `noMip`（无 mip 链）——**用需要 mip 的采样器采样无 mip 纹理 = 纹理不完整 → 采样恒黑 (0,0,0,1)**。全部现象吻合：z<1 走 nearest 采样器（
30	
31	[11:44] (0650e0c7) **ZZZZ 批交付 ✅ + 金字塔修复已由我施加进仓库并验证**  这桩“反编译与二进制行为不符”的奇案破了，而且破得很漂亮——**根本不存在什么行为差**：真凶是金字塔刷墙段每写一堵墙，原版都会经 SquareWallFrame 偷偷掷 1 颗骰（s22222 上共 **11,025 颗**），我们只镜像了写墙漏了掷——骰序整体位移后
32	
33	

```


---

## 🤖 Assistant · 2026-08-19T07:08:35.635Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Very good. Now let me get a few more specific vivid moments. Let me search for specific things like "深夜", "凌晨", funny things, and check some other key moments: the user's shocking discoveries, the model's late-night work. Let me look for specific moments around interesting user interactions. Let me pull complete text of some particularly good candidate entries, and look for a few more categories:
1. The "三棵树" floating tree report (00:01, 00:06)
2. "打死金鱼居然出现恐惧之魂" (17:53)
3. The pyramid case: "反编译与二进制行为不符"奇案
4. The moment at 12:46 about WebGL map perfect zero diff
5. "你那句'仙人掌也有'是破案关键" (16:08)
6. The chart of progress at 08:28 "约95%"
7. "走路的金鱼非常鬼畜" (23:39)
8. "蠕虫音墙" story
9. The story about the model at 09:39 (e65c4575) about "泰拉瑞亚反编译转译TypeScript：这本质是一场'重写'，而非'转换'"

Let me get the full text of a few of these key moments.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:08:37.587Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nwith open('tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\n# Pull full text of specific timestamps\ntargets = [('08-18','09:39','e65c4575'), ('08-19','11:44','0650e0c7'), ('08-18','16:08','573d63f5'), ('08-19','08:28','0650e0c7'), ('08-18','12:46','8405c930')]\nfor day, t, sid in targets:\n    for e in data[day]:\n        if e['t'] == t and e['sid'] == sid:\n            print(f\\\"===== [{day} {t}] ({sid}) {e['who']} =====\\\")\n            print(e['text'][:1500])\n            print()\n\"",
 "description": "Pull full text of key moments"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:37.643Z

**📎 ToolResult**

```
===== [08-18 09:39] (e65c4575) 👤 =====
# 泰拉瑞亚反编译转译TypeScript：这本质是一场"重写"，而非"转换"  ## 🎯 核心发现摘要  - **结论先行** ：把反编译后的《泰拉瑞亚》（Terraria）转译为 TypeScript，不存在成功先例，也没有可用的自动化工具；在当前技术条件下，它实际是一项"以转译为名的重写"工程，工作量以 **多人·年** 计，而不是

===== [08-19 11:44] (0650e0c7) 🤖 =====
修复已在仓库生效：s22222 的 **#40 金字塔与 #46 神庙双双落到 176/178/0**（与 ZZZZ 在 /tmp 副本的验证数字逐位一致——剩余 176/178 是纯地牢 banner 债基线，归 BBBBB）。入账+通报：

===== [08-19 11:44] (0650e0c7) 🤖 =====
**ZZZZ 批交付 ✅ + 金字塔修复已由我施加进仓库并验证**  这桩“反编译与二进制行为不符”的奇案破了，而且破得很漂亮——**根本不存在什么行为差**：真凶是金字塔刷墙段每写一堵墙，原版都会经 SquareWallFrame 偷偷掷 1 颗骰（s22222 上共 **11,025 颗**），我们只镜像了写墙漏了掷——骰序整体位移后

===== [08-18 16:08] (573d63f5) 🤖 =====
**真凶抓到并修复了**——你那句“仙人掌也有”是破案关键。  ## 根因：chunk 拼装 × 非整数缩放  游戏地形不是一整块画的，是按 **16×16 格的 chunk 画布拼接**的。旧拼装公式把每块 chunk 画到 `块位置 × 缩放` 的位置上：  - 默认缩放 1.25：`256×1.25 = 320` **恰好整数像素*

===== [08-19 08:28] (0650e0c7) 👤 =====
进度如何？

===== [08-19 08:28] (0650e0c7) 🤖 =====
**总进度：约 95%**（今早的 85-90% 已跨过），且剩余路径完全具体化了。  **硬指标（当前实况）**：  | 维度 | 状态 | |---|---| | 里程碑链 9293480 | **0-53 槽八通道全绿** ✅ | | 里程碑链 12345（你的种子）| **0-53 槽八通道全绿** ✅ | | 尾段 52 槽（5

===== [08-18 12:46] (8405c930) 🤖 =====
地图修复后**完美零差**(1276 quad 确认 GL 分支已命中)。背景还差 avg 17.2——这是 Skia 高质量降采样(盒式滤波)vs GL 双线性的差异；之前 smooth=false 更错(LINEAR 时 7.7)。正解：**mipmap**(`LINEAR_MIPMAP_LINEAR` 最接近 Skia 行为)。改两

```


---

## 🤖 Assistant · 2026-08-19T07:08:42.184Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent. Now let me look at a few more vivid moments — the user's shocked discoveries and funny bits. Let me search around key times:
- 08-18 00:06 the floating tree report
- 08-18 17:53 "打死金鱼居然出现'恐惧之魂'"
- 08-18 23:39 "走路的金鱼非常鬼畜"
- 08-18 18:37-18:54 worldgen stuck
- 08-19 00:57 deerclops frozen
- 08-19 10:31 user proposing recording feature
- Let me find bot responses to some of these for context. Also the "恐惧之魂" story response.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:08:44.639Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nwith open('tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\n# Get bot responses near key user moments\ndef show(day, t_lo, t_hi, sids=None):\n    for e in data[day]:\n        # compare time strings\n        if t_lo <= e['t'] <= t_hi and (sids is None or e['sid'] in sids):\n            print(f\\\"[{e['t']}] ({e['sid']}) {e['who']}: {e['text'][:500]}\\\")\n            print()\nprint('===== 17:53 恐惧之魂 response =====')\nshow('08-18', '17:53', '18:10', {'04569a63'})\nprint('===== 23:39 金鱼鬼畜 =====')\nshow('08-18', '23:39', '23:59', {'d76053b3'})\n\"",
 "description": "Get bot responses to key user reports"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:44.706Z

**📎 ToolResult**

```
===== 17:53 恐惧之魂 response =====
[17:53] (04569a63) 👤: 现在生物的掉落物开始混乱了，打死金鱼居然出现“恐惧之魂”？

[17:55] (04569a63) 🤖: 找到根因了——是我上一批引入的：`vi_5395` 手写条目插在了自动注册循环**之前**，而 `ITEM_DEFS` 的内部 id = 数组下标，插入点之后全部物品 id 平移 +1，按内部 id 反查 vid 的掉落链全部错位（金鱼 → 恐惧之魂）。按仓内既定的 `BLOCK_TILE_BACKFILL` 模式修复（回填而非插入，零位

[17:59] (04569a63) 🤖: 已修复。这是我在上一批引入的事故，向你道歉——定位与修复如下：  ## 根因 `ITEM_DEFS` 的内部物品 id = **数组下标**（内存里的既有铁律，我踩了）。我给屎堆 5395 补链时把 `item({ key: 'vi_5395_PoopBlock', ... })` 手写插在了 **vanilla.json 自动注册循环之

[18:01] (04569a63) 👤: // ---- 放置块 tile 回填补遗（2026-08-13 实装缺口扫描 §3）：vanilla.json //  .items 的 createTile 有值、extract-itemfunc 提取漏（共享 case 段算式不在 //  单值提取面内）→ def.tile 未回填 = 放置静默无效。5 件以 TEdit 数据为权威

[18:02] (04569a63) 👤: 这是正确的最佳实践吗？维护不会有风险吗？就像你前面错误注册一样

===== 23:39 金鱼鬼畜 =====
[23:39] (d76053b3) 👤: 现在仍然有一些动画播的过快的生物动画帧，比如走路的金鱼，非常鬼畜

[23:54] (d76053b3) 🤖: 修好了，收尾完毕。总结：  ## 走路金鱼“鬼畜”根因：两类帧档错位  **① 全部 aiStyle=7 小动物被城镇 NPC 档截胡**(和上次兔子闪帧同一根因，那是第一波，这次是剩下的全部)：  我们 `vanillaFrameIdx` 的 `ai===7` 分支是**城镇 NPC** 档(帧 2 起步、`|vx|×2+1`、阈值 6

```


---

## 🤖 Assistant · 2026-08-19T07:08:48.198Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have enough material. Let me also check the floating tree story from the beginning of 08-18, the deerclops frozen story, and a couple of other highlights. Let me quickly check the 00:06 floating tree case and the deerclops response.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:08:50.875Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nwith open('tools/journey-inputs/archive-stream.json') as f:\n    data = json.load(f)\ndef show(day, t_lo, t_hi, sids=None):\n    for e in data[day]:\n        if t_lo <= e['t'] <= t_hi and (sids is None or e['sid'] in sids):\n            print(f\\\"[{e['t']}] ({e['sid']}) {e['who']}: {e['text'][:450]}\\\")\n            print()\nprint('===== 浮空树案 =====')\nshow('08-18', '00:01', '00:30', {'c44574b3'})\nprint('===== 独眼巨鹿冻半空 =====')\nshow('08-19', '00:57', '01:05', {'04569a63'})\nprint('===== 蠕虫音墙 =====')\nshow('08-18', '17:18', '17:25', {'1fc2b821'})\nprint('===== 树冠缝(用户句仙人掌也有) =====')\nshow('08-18', '15:54', '15:56', {'573d63f5'})\n\"",
 "description": "Pull more key conversation moments"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:08:50.977Z

**📎 ToolResult**

```
===== 浮空树案 =====
[00:01] (c44574b3) 👤: 关于浮空的那棵树我仍然觉得有问题，理论上泰拉瑞亚世界生成树木应该是强制要求底下是泥土吧，为什么会出现花草把树木的一格树干直接替换掉，造成浮空树呢，原版真是这样的吗

[00:03] (c44574b3) 🤖: 这次确认了关键事实：`m` 就是循环里的**世界 x 列**（`for (int m = num2 - num3; ...)`），`Main.maxTilesX` 就是世界宽——所以这确实是**按世界坐标位置开的门**，而且 remix 种子分支（:20651）里有一模一样的门，两个分支都有。  ## 拆解你的质疑  **“树木生成应该强

[00:06] (c44574b3) 👤: 你看我这个世界的报告，很明显非常诡异吧？这确定是原版代码能干出来的？~/Downloads/debug-report-模型根基-2026-08-17T16-04-53-399Z.json 画面里三棵树的底部都有异常，一个被蘑菇占用，两个是花，而且还由于树木下面的一格方块是被强制保护的，甚至无法使用镐子破坏他们

[00:07] (c44574b3) 🤖: 原版 Mushrooms pass（常规分支 :20812-20841）**只改已存在花草的帧变蘑菇，不放置新格**——所以“蘑菇占树底”在原版最多是 Flowers 先中招再被转帧，同屏三棵绝无可能。我们的移植肯定有频率 bug。查我们的 Flowers/Mushrooms 移植：

[00:09] (c44574b3) 🤖: 挖掘“保护”查明了——那是 **CanKillTile :62276-62315 的原版真规则**（树干/棕榈/箱柜等“需支撑件”正下方的方块不可挖，我们 1:1 移植了）。真正要验证的是覆盖频率。写复现诊断（vitest 全管线重生成该种子大世界+逐树核查）：

[00:21] (c44574b3) 🤖: 全案定性，三层结论：  ## 1. 你看到的“三棵同屏”不是当前代码能干出来的  用你的原种子（1814620304）+ 原尺寸（8400×2400）+ 原邪恶（腐化）在**当前代码**上完整重生成： - 全世界 648 棵树中 75 处“底格被花草占”——**每一处都落在门允许区**（左 48% 树干条款 / 右 52% 任型条款），中

===== 独眼巨鹿冻半空 =====
[00:57] (04569a63) 👤: ~/Downloads/debug-report-困惑的要塞-2026-08-18T16-57-23-890Z.json 独眼巨鹿boss无法正常工作，冻结在半空不动

[01:04] (04569a63) 🤖: **根因找到了**：`deerclopsMovement` 只算速度、**从不积分位置**——668 在原版是 `noGravity+noTileCollide`（SetDefaults :17384 实证），由引擎直接 `position += velocity` 穿墙移动；我们的移植漏了积分这一步，AI 状态机一切正常（ai1 在涨、

[01:05] (04569a63) 🤖: 修复完成。  ## 根因（三层证据闭环）  **报告快照**：668 位于 (20426, 7179)，`vx=3.51, vy=16, onGround=false`，AI 计数照常递增（ai1=817、despawnTimer 在倒数）——状态机活着、速度满格、**坐标不动**。  **探针复现**：冰原地面 + 召唤 + 逐 tic

===== 蠕虫音墙 =====
[17:18] (1fc2b821) 🤖: transformVisuals 与原版 ：81742-81749 逐锚点核对通过（Item_8×1 + gore99×3 @ y−10/y+h/2−10/y+h−10、初速×0.3;Item_8 无专属音量档=×1 正确）。接着核对 378 牙齿炸弹：

[17:18] (1fc2b821) 👤: 底下蠕虫的音效明显错误，在地底穿梭的声音全部变成了boss唤醒音效！而且现在杀死洞穴蝙蝠连死亡声音都没了！

===== 树冠缝(用户句仙人掌也有) =====
[15:54] (573d63f5) 👤: 离谱的是在你这里面没问题，但是在世界里的就是会有缝，包括沙漠的仙人掌也是有这种问题

```


---

## 🤖 Assistant · 2026-08-19T07:10:51.457Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have plenty of material now. Let me also quickly check a couple of things:
1. The 08-19 morning fog flicker story (00:01) — got it already
2. The dualwindow IOSurface story — got it from memory
3. The "simhost" E2E 15 green tests — got it

Let me also verify a couple of dates from memory files. The memory files were all mtime >= 08-18. Some contain old content (like jungle-parity-and-id-collision is old but has appended 08-18 sections). For the "story" list I need items that are actually 08-18/08-19 work. Let me be careful to pick genuinely new work.

Key stories (achievements, non-defect):
1. **WebGL2 一期** (08-18): webgl2-phase1-port.md — GLSpriteLayer + 背景族 + 全屏地图 GL 化, 像素级对拍 地图 Δ=0, plus 六号坑显存管理, y-flip regression guard tests. Also the cloud GL 化 (CloudGL→并入 GLSpriteLayer) on 08-19.
2. **SimHost 服务器权威房全链** (08-17→08-18 B4-B6): server-room-simhost-port.md — 进程内虚拟房主, ioWorker, 刷怪链镜像, 浏览器 E2E 15/15, B6a 房间进程化 worker, 聊天系统+世界频道, 千人单房优化 (120 bots CPU 82→28.6%), 千人实测带宽推算.
3. **remaster-studio-pipeline** (08-19): 素材重制管线 — AssetCatalog + gpt-image-2 逐帧重制 + zip 素材包热补丁(类 mod). 六里程碑: catalog 20 + pack/prompt 27 + runtime 9 + 工作台 17/17 + E2E 7/7.
4. **液体 buffer-reflow 对齐** (08-19, DDDDD 批): liquid-buffer-reflow-parity.md — #49 湖体 11707→0, 475 条湖面薄膜, 大世界天然压力测试.
5. **AI 全量审计** (08-19): ai-parity-audit-2026-08-19.md — 六代理 ~200 条, 当日修 15 项 + 全量修复批 181/181 测试. 死亡=只积分不steering 共享段方法论.
6. **微残留清零 XXXX 批** (08-19): xxxx-microresidual-final-clear.md — #101 掷流 20196→165353, Tile.actuator(0x800)≠inActive(0x40), 剑冢 HashSet 豁免撤销等.
7. **物品 tooltip 全量 1:1** (08-18): item-tooltip-parity-port.md — GetLinesInfo :20488-20920 行序, 四审终清零.
8. **钻石窗口 IO Surface 耗尽修复** (08-18~08-19): dualwindow-iosurface-exhaustion.md — IOSurface 张数耗尽机制钉死, chunk atlas 页化 446→28, TintAtlas 染色图集 41 变体=1页, 八场攻防战.
9. **弹幕绘制偏移表全量** (08-18): proj-draw-offset-table.md — num143/num144 表 118 条.
10. **鸟类帧族谱系** (08-18): bird-findframe-families.md — 鸟/小动物 FindFrame 专属 case 全家族.
11. **Boss 审计第一波修复** (08-19): boss-audit-wave1-fixes.md — 全 Boss 同款四维审计 25 Boss 族, 两波 8 代理, BGM 链键 17/24 族错曲.
12. **石巨人三症状修复** (08-19): golem-3symptom-fix.md — 负血不死/无头像/帧乱闪 + 终审 13 修.
13. **地牢水宝箱浮空刀** (08-19, BBBBB): dungeon-waterchest-float-knife.md — #32 清零, 0.6f float 刀口.
14. **液体最后清算 root59** (08-19, WWWW): wwww-root59-liquidation.md — #59 193→0, 帧杀级联引擎.
15. 也可以提: **金字塔奇案 ZZZZ** (08-19): pyramid-wallframe-die-debt.md — SquareWallFrame 暗掷 11025 颗.
16. **里程碑链 0-53 全绿** (08-18→08-19): 四链全景, 总进度 95%.
17. **藤蔓级联** (08-18): vine-cascade-port.md.
18. **NPC 环境音全量** (08-18): npc-ambient-sound-audit.md.
19. **Boss 召唤/掉落/事件总审计** (08-18): boss-summon-drops-events-batch.md — 40000 次统计实证.

Pits (坑) with 现象→根因→修复 structure:
1. **y 翻转两次翻车** (08-18): 并行会话写回旧版静默丢失 → 回归守卫测试.
2. **texSubUpdate 9参重载 #362CFF** (08-18): Chrome 把画布左上角 w×h 贴进目标区 → 抠 scratch 画布走 8 参.
3. **纹理缓存键碰撞** (08-18): ImageBitmap 无 .src 键退化宽x高 → WeakMap 实例 id.
4. **mipmap 透明边缘黑化** (08-18).
5. **GLSpriteLayer dispose 漏挂 → GB 级显存打爆** (08-18 二次崩溃): contextlost 风暴 26 万次/tab 3.4GB.
6. **worker .filter 崩毁** (08-18): Set 无 filter → worker exit 全房失联.
7. **选角加入崩溃** (08-18): makeGame().player 未建.
8. **砍树掉落自动收集崩溃** (08-18): inv.add 裸 ITEM_DEFS[id].maxStack → ProfileChunk 法从 trace 重建时间线定位.
9. **金鱼掉恐惧之魂** (08-18): vi_5395 手写插在自动注册循环前 → id 平移 +1.
10. **兔子/金鱼闪帧** (08-18): aiStyle 7 城镇 NPC 档截胡.
11. **蠕虫音墙** (08-18): WAV_MAP['roar'] 双轨随机 + Style 缺省 1 陷阱.
12. **悬停贴图全黑** (08-18): source-atop 叠黑画布.
13. **tooltip 透明感三轮** (08-18): tint 循环 alpha 通道误乘红通道.
14. **chunk 接缝非整数 zoom** (08-18): 1.27→325.12.
15. **迷雾 20s 周期闪** (08-19): GPU 看门狗误清 CPU 数据 fogPix.
16. **生命树晚到贴图** (08-19): note 被早退吞.
17. **独眼巨鹿冻半空** (08-19): 从不积分位置 + 测试代偿.
18. **放大全黑** (08-19): sampler 对象覆盖 texParameteri, 需 mip 的 MIN_FILTER 采无 mip 纹理 → 恒黑. zoom 1.37 即黑.
19. **石巨人负血不死** (08-19): hurt 放行在 dead=true 之前.
20. **红帽骷髅王 ai3 断链** (08-18): 普通骷髅王必掉 Chippy 套装漏洞.
21. **床唤醒误杀** (08-17/18): wake 检查读 feet+2.
22. **半砖浸润** (08-19): flag5 自身格液体分支未移植.
23. **MaxChunks 回满档 herd 共犯** (08-19): afterWorldLoad 直回满档.
24. **数字键失效** (08-19): rAF 回调被 achAdvisor 抛错炸断.
25. **软渲染下每帧重建 GLSpriteLayer 60张/s** (08-19): diedAt=0 洞.
26. **云不渲染** (08-18 深夜): globalCloudAlpha 接了雨云浓度 (晴天恒 0).
27. **哨兵三捕 tintedSprite** (08-19): 612 张/90s → 4 张.
28. **vui 光标丢失** (08-19): healCanvas 前 onCanvasRecreated 把 keydownHandlers 清空.

Raw dialogue fragments — pick 5-8:
1. [08-18 00:06] 👤 "你看我这个世界的报告,很明显非常诡异吧?这确定是原版代码能干出来的?...画面里三棵树的底部都有异常,一个被蘑菇占用,两个是花" [c44574b3]
2. [08-18 09:39] 👤 (e65c4575) "# 泰拉瑞亚反编译转译TypeScript:这本质是一场'重写',而非'转换'...工作量以多人·年计" — this is actually a user message quoting research? It's who=👤. Interesting.
3. [08-18 12:02] 👤 "我的GPU资源非常充足,为什么总是挤爆" [8405c930]
4. [08-18 15:54] 👤 "离谱的是在你这里面没问题,但是在世界里的就是会有缝,包括沙漠的仙人掌也是有这种问题" [573d63f5] + bot response [16:08] "真凶抓到并修复了——你那句'仙人掌也有'是破案关键"
5. [08-18 17:53] 👤 "现在生物的掉落物开始混乱了,打死金鱼居然出现'恐惧之魂'?" [04569a63] + bot [17:59] "已修复。这是我在上一批引入的事故,向你道歉"
6. [08-18 23:39] 👤 "现在仍然有一些动画播的过快的生物动画帧,比如走路的金鱼,非常鬼畜" [d76053b3]
7. [08-18 16:08] 🤖 "真凶抓到并修复了——你那句'仙人掌也有'是破案关键" [573d63f5]
8. [08-19 00:01] 🤖 "全案闭环——两个症状同一个根,外加 20s 看门狗:闪烁:整幅重建精确间隔 20s(24.8→43.9→63.9)= GPU 看门狗周期!" [8405c930]
9. [08-19 11:44] 🤖 "这桩'反编译与二进制行为不符'的奇案破了,而且破得很漂亮——根本不存在什么行为差:真凶是金字塔刷墙段每写一堵墙,原版都会经 SquareWallFrame 偷偷掷 1 颗骰(s22222 上共 11,025 颗)" [0650e0c7]
10. [08-19 08:28] 🤖 "总进度:约 95%..." [0650e0c7]
11. [08-18 18:54] 👤 "没有用依然卡在37% 放置飞镖机关" [0650e0c7]
12. [08-19 11:28] 👤 "index-CHYbtgbt.js:940 [drawFullMap] GL 合成中心恒黑但该点已探索——切 2D 兜底" [04569a63]
13. [08-19 11:21] 👤 "不要这种降级的,我们要从我们自己出发,看还有没有优化空间,你这样通信搞得很奇怪" [8405c930]
14. [08-18 14:31] 👤 "我记得地域里的骨龙在接近时本身是有音效的" [1fc2b821]
15. [08-18 19:46] 👤 "npm run playsoft 无效 URL: --soft" [8405c930]
16. [08-19 10:31] 👤 "我感觉我们需要一个行为录制的方案,比如长按F5来启动场景的整体'录制'..." [c44574b3]
17. [08-19 00:36] 👤 "我确定是最新构建,你看脚本的hash都不同" [8405c930] + bot response [00:26] "没在——这是第三个工厂,还没修。"

Best 8:
1. [08-18 00:06] 👤 浮空树质疑
2. [08-18 12:02] 👤 GPU 挤爆
3. [08-18 15:54] 👤 "离谱的是在你这里面没问题..." + [16:08] 🤖 "你那句'仙人掌也有'是破案关键"
4. [08-18 17:53] 👤 金鱼恐惧之魂 + [17:59] 🤖 道歉
5. [08-18 23:39] 👤 金鱼鬼畜
6. [08-19 00:01] 🤖 迷雾 20s 看门狗
7. [08-19 00:36] 👤 "我确定是最新构建,你看脚本的hash都不同" + [00:26] 🤖 "没在——这是第三个工厂,还没修" (order: 00:26 bot came before 00:36 user. The user challenged at 00:25 with a list of issues, bot said at 00:26 "没在——这是第三个工厂", user at 00:36 "我确定是最新构建" — which "点破误判" as memory says: 用户纠正"确定是最新构建"点破误判)
8. [08-19 11:44] 🤖 金字塔奇案破了
9. [08-18 09:39] 👤 多人·年 (this is a research doc the user pasted - shows the scale of the undertaking)

Let me verify the 09:39 entry is truly from user. who=👤 yes. It looks like the user pasted a research summary about the project being a "rewrite not a conversion" — actually it might be from a subagent research task the user did in a separate session (e65c4575 is the "journey page" session sid). It says "把反编译后的《泰拉瑞亚》(Terraria)转译为 TypeScript,不存在成功先例...工作量以多人·年计". This is powerful framing for the showcase.

Now, dates: The story items should be dated. Memory files have dates in their content. Let me confirm dates:
- webgl2: 08-18 (phase 1) + 08-19 additions
- simhost: B4-B6 08-17/08-18; chat system 08-18; 千人 08-18
- remaster: 08-19
- liquid-buffer-reflow: 08-19
- ai-parity: 08-19
- xxxx-microresidual: 08-19
- tooltip: 08-18
- dualwindow: 08-18~08-19
- proj-draw-offset: 08-18 (+08-19 接线)
- bird-findframe: 08-18
- boss-audit-wave1: 08-19
- golem: 08-19
- dungeon-waterchest: 08-19
- wwww-root59: 08-19
- pyramid: 08-19

For stories list (8-12), I'll write ~14 entries but keep the target in range. Let me aim for 12 stories.

Story list:
1. WebGL2 一期:GL 化背景层与全屏地图 (08-18) — map Δ=0 perfect, 六号坑显存治理
2. SimHost 服务器权威房全链 (08-18) — 进程内虚拟房主, B4: ioWorker+刷怪镜像+E2E 15绿, B6a worker 化, 聊天+世界频道, 千人实测
3. remaster-studio-pipeline 素材重制管线 (08-19) — gpt-image-2 + zip 热补丁
4. 液体 buffer-reflow 对齐 (08-19) — #49 11707→0, 475 条湖面薄膜
5. AI 全量审计 (08-19) — 六代理 ~200 条, 181/181
6. 微残留清零 XXXX (08-19) — actuator≠inActive 两大旗标
7. tooltip 全量 1:1 (08-18) — 四审终清零
8. 钻石窗口 IO Surface 攻防 (08-18~19) — 八场, chunk atlas 446→28, TintAtlas
9. 弹幕绘制偏移表 118 条 (08-18)
10. 鸟类帧族谱系 (08-18)
11. Boss 审计波1 (08-19) — 17/24 族错曲 BGM 链
12. 石巨人三症状→终审13修 (08-19)
13. 金字塔 11025 暗掷奇案 (08-19) — ZZZZ
14. 里程碑链 0-53 全绿+总进度95% (08-19)

That's 14 — maybe merge #10 into one "小动物帧族谱系+金鱼鬼畜" and keep 12-13. The target is 8-12, "目标" so a bit over is fine but let me keep it tight at 12 by merging pyramid into the wwww/root59 story or keeping both. Actually 金字塔 is one of the most vivid stories ("反编译与二进制行为不符"的奇案). I'll keep it. 13 entries is acceptable ("目标 8-12 条" — I'll do 12 by combining).

Let me combine: 鸟类帧族谱系 + 金鱼鬼畜 = one story about critter frame families (bunny-walk-frame-fix + bird-findframe-families). And 地牢水宝箱浮空刀 + root59 are separate items in the requested direction list, so keep them separate as requested. The task explicitly lists: 地牢水宝箱浮空刀 and 液体最后清算(root59) as separate directions. OK final 12:

1. WebGL2 一期 (08-18)
2. SimHost 全链 (08-18)
3. remaster-studio-pipeline (08-19)
4. 液体 buffer-reflow (08-19)
5. AI 全量审计 (08-19)
6. 微残留清零 (08-19)
7. tooltip 全量 (08-18)
8. IO Surface 攻防 (08-18~19)
9. 弹幕偏移表 (08-18)
10. 鸟类帧族谱系+小动物帧律 (08-18)
11. Boss 审计波1+石巨人 (08-19) — hmm, these are separate directions. Actually 石巨人 is listed separately. Let me do 13 entries; the instruction says 目标 8-12, slight overflow is OK but let me try to be close. I'll do 12 by merging 石巨人 into boss-audit-wave1 story (they're directly related — golem-3symptom-fix spawned the boss audit).

Final 12:
1. WebGL2 一期
2. SimHost 全链
3. remaster-studio-pipeline
4. 液体 buffer-reflow 对齐
5. AI 全量审计
6. 微残留清零
7. tooltip 全量 1:1
8. IO Surface 八场攻防
9. 弹幕绘制偏移表
10. 鸟类帧族谱系
11. Boss 审计波1(含石巨人)
12. 金字塔 11025 暗掷 + 地牢水宝箱浮空刀 + root59 — hmm these are three separate directions requested. 

OK let me reconsider. The requested directions are 14 items. I'll produce 12-13 stories to cover them all — slightly above the 8-12 target is reasonable given they explicitly listed 14 directions. I'll do 13:
12. 地牢水宝箱浮空刀 (BBBBB) — can merge with 液体 buffer-reflow? No, they're different chains (#32 vs #49). Merge pyramid+waterchest as "二进制刀口" stories? They're different: 0.6f float 刀口 vs 11025 暗掷. Actually BBBBB includes the 0.6f float knife-edge and ZZZZ pyramid is SquareWallFrame hidden rolls — both are "反编译刀口" family. I can present them as one story "反编译刀口双案" but each deserves its own. 

Let me just go with 13 entries. It's "目标 8-12 条" — I'll trim to 12 by merging "弹幕偏移表" and "鸟类帧族谱" into one "视觉帧族谱系批" story? No — they're distinct enough and both explicitly requested. I'll merge 地牢水宝箱浮空刀 into the 液体 root59 story since both are liquid/worldgen convergence? Not really.

Decision: 13 stories, slightly over target but covering all 14 requested directions (merging golem into boss-audit wave1). Actually let me count the directions again:
- WebGL2 一期 ✓ (1)
- SimHost ✓ (2)
- remaster-studio-pipeline ✓ (3)
- 液体 buffer-reflow 对齐 ✓ (4)
- AI 全量审计 ✓ (5)
- 微残留清零 ✓ (6)
- tooltip ✓ (7)
- 钻石窗口 IO Surface ✓ (8)
- 弹幕绘制偏移表 ✓ (9)
- 鸟类帧族谱系 ✓ (10)
- Boss 审计第一波修复 ✓ (11)
- 石巨人三症状 ✓ (12)
- 地牢水宝箱浮空刀 ✓ (13)
- 液体最后清算(root59) ✓ (14)

14 directions. I'll write 14 stories — wait, target says 8-12. The directions list is what they want covered ("方向:"), so I think covering all 14 is more important. I'll write ~14 concise ones. Hmm, "目标 8-12 条" is explicit. Let me merge sensibly:
- Merge 石巨人 into Boss 审计 (golem-3symptom-fix is the origin of boss-audit) → 13
- Merge 地牢水宝箱浮空刀 + 液体root59 into... they're both worldgen-chain convergence but distinct. Or merge buffer-reflow (DDDDD #49) with root59 (WWWW #59) as "液体双清算"? The buffer-reflow is LiquidBuffer semantics, root59 is CaveHouse 域. Hmm.

Actually simpler: keep 12 by merging:
1. WebGL2 一期
2. SimHost 全链
3. remaster 管线
4. 液体双清算:buffer-reflow (#49) + root59 帧杀级联 (#59) — both are liquid/cave-house convergence in worldgen. Hmm, but they asked for "液体 buffer-reflow 对齐" and "液体最后清算(root59)" as separate. 

You know what — the user said "目标 8-12 条" and listed 14 directions. The most useful output covers all directions. I'll produce 14 entries (they'll appreciate completeness) — no wait, respect the format instruction. Let me do exactly 12 by merging the 4 worldgen ones into 2:
- 液体 buffer-reflow 对齐 (standalone, it's about LiquidBuffer)
- 世界生成终局三连清算: root59 + 地牢水宝箱 + 金字塔11025 (combine as one story? that's awkward)

Alternative: 12 entries where each direction gets its own bullet but I merge:
- 石巨人 → into Boss 审计波1 story (mention golem origin)
- 地牢水宝箱浮空刀 + 金字塔11025 → "反编译刀口奇案双破" (both are float/hidden-roll knife-edge cases in worldgen convergence, ZZZZ+BBBBB)

That gives: WebGL2, SimHost, remaster, buffer-reflow, AI审计, 微残留, tooltip, IOSurface, 弹幕偏移, 鸟类帧族, Boss审计(含石巨人), 反编译刀口双案(root59算液体清算)... 

root59 still needs a home. root59 (WWWW 批 #59 百格级根清偿 + 帧杀级联引擎) — I can fold into 微残留清零 story? They're adjacent batches (XXXX follows WWWW). Or fold root59 into buffer-reflow story as "液体两波清算" — both liquid-adjacent (#49 湖体 + #59 洞穴屋). Actually #59 root59 is CaveHouse domain (陷阱雕像/钟乳石/梁写), not liquid. The name "wwww-root59-liquidation" means "清算" (liquidation in the sense of settling debts), not liquid! Yes — "最后清算" = final settlement of debts. So it's worldgen debt settlement.

OK final plan — 12 stories:
1. WebGL2 一期 (08-18)
2. SimHost 全链 (08-18)
3. remaster-studio-pipeline (08-19)
4. 液体 buffer-reflow 对齐 (08-19)
5. AI 全量审计 (08-19)
6. 微残留清零 + 世界生成终局清算 root59 (08-19) — merge XXXX+WWWW? Hmm. 

Actually, let me just be pragmatic: I'll write 14 short entries. The instruction "目标 8-12" is a target, and covering 14 requested directions matters more. No — actually I'll write 12 and be smart about merging. Let me look at what can naturally merge:

- golem + boss-audit-wave1: natural merge (same lineage, memory says "相关:[[golem-3symptom-fix]](石巨人 13 修+BGM 链根因)")
- dungeon-waterchest + pyramid: both 08-19 worldgen knife-edge cases — natural merge as "二进制刀口双奇案"

That gives 12. root59 gets its own entry. Final:
1. WebGL2 一期 GL 化 (08-18)
2. SimHost 服务器权威房 (08-18)
3. remaster 素材重制管线 (08-19)
4. 液体 buffer-reflow (08-19)
5. AI 全量审计 (08-19)
6. 微残留清零 XXXX (08-19)
7. tooltip 全量 (08-18)
8. IO Surface 攻防 (08-18~19)
9. 弹幕偏移表 (08-18)
10. 鸟类帧族谱系 (08-18)
11. Boss 审计波1 + 石巨人 (08-19)
12. 液体最后清算 root59 (08-19)
13. 地牢水宝箱 + 金字塔刀口 (08-19)

That's 13. Fine, close enough — I'll go with 13 (covering all 14 directions with golem merged). Or make it exactly 12 by also merging root59 into... eh. 13 is fine.

Actually wait — I should reconsider merging #13. The user's direction list explicitly names "地牢水宝箱浮空刀" as its own direction. And pyramid isn't even in their direction list (they didn't mention 金字塔). So I don't need to include pyramid as a story! The directions are: WebGL2, SimHost, remaster, buffer-reflow, AI审计, 微残留, tooltip, IO Surface, 弹幕偏移表, 鸟类帧族谱系, Boss审计波1, 石巨人, 地牢水宝箱, root59. That's 14. Merging golem into boss audit gives 13. Hmm, they listed both "Boss 审计第一波修复" and "石巨人三症状修复" separately though.

OK, decision: 13 entries. One over the target, covering everything they asked. Good.

Now for pits (二), target 8-15. I'll do ~15:
1. y 翻转两次翻车 (08-18)
2. texSubUpdate 9参 #362CFF (08-18)
3. 纹理键碰撞 Background_50 (08-18)
4. GLSpriteLayer dispose 漏挂→显存打爆 (08-18)
5. worker Set.filter 崩毁 (08-18)
6. 砍树收集崩溃 + GC 掉帧 (08-18)
7. 金鱼掉恐惧之魂 (08-18)
8. 兔子/金鱼闪帧 (08-18)
9. 蠕虫音墙 (08-18)
10. 悬停图标全黑 (08-18)
11. tooltip 透明感三轮 (08-18)
12. chunk 接缝非整数 zoom (08-18)
13. 迷雾 20s 周期闪 (08-19)
14. 生命树晚到贴图 (08-19)
15. 独眼巨鹿冻半空 (08-19)
16. 地图放大全黑 sampler (08-19)
17. 石巨人负血不死 (08-19)
18. 红帽骷髅王 Chippy 漏洞 (08-18)
19. 软渲染每帧重建 GLSpriteLayer 60张/s (08-19)
20. 云不渲染 雨云浓度 (08-18)
21. 半砖浸润 (08-19)

Pick the best 15. I'll include the most vivid ones with clear 现象→根因→修复.

For dialogue fragments (三), 5-8. I'll pick 8:
1. [08-18 00:06] 👤 浮空树质疑 "这确定是原版代码能干出来的?"
2. [08-18 09:39] 👤 多人·年研究 (framing the whole project)
3. [08-18 12:02] 👤 "我的GPU资源非常充足,为什么总是挤爆"
4. [08-18 15:54] 👤 "离谱的是在你这里面没问题,但是在世界里的就是会有缝" + [08-18 16:08] 🤖 "你那句'仙人掌也有'是破案关键"
5. [08-18 17:53] 👤 金鱼恐惧之魂 + [17:59] 🤖 "这是我在上一批引入的事故,向你道歉"
6. [08-18 23:39] 👤 "走路的金鱼,非常鬼畜"
7. [08-19 00:01] 🤖 "整幅重建精确间隔 20s=GPU 看门狗周期!"
8. [08-19 11:44] 🤖 金字塔 11025 颗骰

Also strong candidates:
- [08-19 00:36] 👤 "我确定是最新构建,你看脚本的hash都不同" (user pushing back, breaking the model's misdiagnosis)
- [08-19 11:21] 👤 "不要这种降级的,我们要从我们自己出发"
- [08-18 14:31] 👤 骨龙音效
- [08-19 10:31] 👤 行为录制方案提案

Let me pick the 8 most vivid. I think: 浮空树, 多人·年, GPU挤爆, 仙人掌破案(user+bot pair), 恐惧之魂(user+bot pair), 金鱼鬼畜, 20s看门狗, 金字塔11025. That's 8 (two are pairs).

Wait, need to double check the fragment requirement: "截断80字" — truncate at 80 chars. Format: `- **[时刻]** 👤/🤖 原文片段(截断80字) [sid]`

Now let me also verify a few facts I want to cite:
- E2E 15绿 for SimHost: "_sr-e2e.mjs 15/15(真实客户端建房→访客→傀儡→召唤意图→Boss v_50 可见→msg42 打击→服务器结算→移除" ✓ (later 20/20 with chat)
- 千人实测: "60分散/120分散/60聚集=人均0.44/1.05/10.8KB/s,worker CPU 46.6/82.1/59.8%。1000CCU今日拓扑=多房分线→8vCPU/16GB/100Mbps" ✓
- WebGL2 对拍: "背景 平均Δ0.02/Δ>8 占 0.1%;地图 Δ=0 完美" ✓
- chunk atlas: "活张数 446→28(223 chunk 实测);运行期画布创建≈0(回头路二遍 9 张 vs 旧每遍 ~6000)" ✓
- TintAtlas: "实测 41 变体=1 页(旧=41 张)" ✓
- liquid buffer: "#49 L=11,707→0" and "475 条湖面薄膜" ✓
- AI audit: "~200 条" "当日修 15 项" "合并终验 181/181" ✓
- tooltip: "GetLinesInfo :20488-20920" ✓
- 偏移表: "118 条静态项(2026-08-18 脚本机械对拍 118/118 全对)" ✓
- 鸟类帧族: bird 74/297/298/442, 丛林鸟 671-675, 鸮 611/689 等 ✓
- boss audit: "全 Boss 同款审计(用户令'逐一审计'):石巨人双代理模式推广到全 25 Boss 族,两波 8 代理" "BGM 链键 flag/num3 错位...17/24 族错曲" ✓
- golem: "负血不死(最重,契约断裂)" ✓
- dungeon waterchest: "两新链 #32 Dungeon 清零(水覆写箱 loot 支 + 入口 0.6f float 刀口)" "312.99999976→312 vs 二进制 313" ✓
- root59: "#59 百格级根清偿(193→0)+帧杀级联引擎" ✓
- 微残留: "#101 掷流 20196→165353/1663744(五修)" hmm that reads like 首差后移? "残 1%=TrackGenerator" — the summary in jungle memory says "#101 掷流 20196→165353"... wait that's backwards. Let me re-read: "**#101 掷流 20196→165353/1663744**(五修)". Hmm, from the jungle-parity memory: "residual: #101 流差 164→20196". So the stream diff went from... confusing. Actually in XXXX memory: "#101 掷流 20196→165353/1663744" — I think these are firstDiff positions (stream position of first difference) moving later? No wait — moving from 20196 to 165353 means the first difference moved later (from 20196th roll to 165353th roll), which is improvement. And 1663744 might be after AAAAA. Yes: "验证:掷流 firstDiff 165353→165546" in AAAAA. So firstDiff positions: 20196 → 165353 (XXXX) → 165546 (AAAAA) → 166921 (CCCCC). OK so XXXX moved the first divergence from roll #20196 to roll #165353. Good.

Also for 剑冢: "34.5k 剑冢掷"归因证伪" and "HashSet 豁免撤销:枚举=槽分配序,Add-only≡插入序" ✓.

For the stats at the end: counts of stories (13), pits (15), fragments (8). And the 3 most striking stories in one sentence each.

Let me now also double-check a couple of small details for the pit entries:

- 迷雾 20s: "整幅重建精确间隔 20s(24.8/43.9/63.9s)" root: "GPU 看门狗(20s 巡检)误清 CPU 数据:recreateAuxCanvases 无条件 fogPix=null" fix: "fog 缓冲只在 dispose 清" ✓
- 生命树: "烘焙期 ensure(Tiles_192) 时 pending=true → if(pending) return null 早退在 bakeTracker.note(file) 之前 → 晚到无人重烘" fix "note 提到早退前" ✓
- 独眼巨鹿: "deerclopsMovement 只算 vx/vy 从不积分位置" fix "movement 尾 e.x += e.vx; e.y += e.vy" ✓
- 放大全黑: "samp.linear 的 MIN_FILTER 是 LINEAR_MIPMAP_LINEAR,而小地图/迷雾纹理是 noMip——用需要 mip 的采样器采样无 mip 纹理=纹理不完整→采样恒黑 (0,0,0,1)" fix "samp.linearNoMip,quad()/tileX() 按 e.mipped 分流" ✓
- 石巨人: "Enemy.hurt 的石巨人放行段 if (245||246||247||248) return false 在 this.dead = true 之前" fix "放行列表收窄到 246(加本体活门);245 在 hurt 内灭部件" ✓
- 红帽: "召唤只写 redHat 旗但 NpcDrops 五条规则/Renderer 红臂骨/GorePiece 全读 ai3;且 bossAI.ts 把 ai3 挪用为旋冲方向(±1)→普通骷髅王约半数击杀必掉全套 Chippy 时装" fix "召唤补 head.ai3=1 + 旋冲方向改独立字段 skeletronSpinDir" ✓
- 云: "globalCloudAlpha 曾接 max(wr.cloudAlpha, 墓园×0.92)×atmo——wr.cloudAlpha 是雨云浓度(晴天恒 0)→晴天云全透明" fix "globalCloudAlpha = atmo 直取" ✓
- GLSpriteLayer 60张/s: "WebGL2 初始化失败时 GLSpriteLayer 构造器 unavailable 且 diedAt=0 → 消费方退避判 now-0>5000 恒真 → 每帧 dispose+new GLSpriteLayer=60 张/秒" fix "构造器三处失败分支补 diedAt=now;Renderer.acquireGL() 统一获取" ✓
- 半砖浸润: "原版 DrawTile_LiquidBehindTile 有 flag5:tileCache.liquid>0...半砖/坡面格自己格内的液体也画浸润。我们的只读四邻、从不读本格=整类缺失" fix "补 flag5 本格液体分支+五处家族差异" ✓

Good. Now dates for pits — all 08-18 or 08-19.

One more check on the story about E2E for SimHost — the prompt says "E2E 15绿" which matches "_sr-e2e.mjs 15/15". Later 20/20. Good.

Also the remaster story: "六里程碑全绿:catalog 单测 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7" ✓ And "10974 张 IHDR 尺寸" for gen-remaster-index. And gpt-image-2 doesn't support transparency, min pixels 655,360.

Now write the file /tmp/latest-mining.md. Language: Chinese. Make it vivid.

For story format: `- **故事名**(日期): 2-3 句描述,要生动、有画面感 | 证据:记忆文件或实录时刻`

For pit format: `- **坑名**(日期): 现象:xxx → 根因:xxx → 修复:xxx | 记忆文件:xxx.md`

For fragment format: `- **[时刻]** 👤/🤖 原文片段(截断80字) [sid]`

Let me count characters for fragments to truncate at ~80 Chinese chars. I'll write them out.

Fragments (truncated ~80 chars):
1. **[08-18 00:06]** 👤 "你看我这个世界的报告,很明显非常诡异吧?这确定是原版代码能干出来的?…画面里三棵树的底部都有异常,一个被蘑菇占用,两个是花,而且还…无法使用镐子破坏" [c44574b3]
2. **[08-18 09:39]** 👤 "泰拉瑞亚反编译转译TypeScript:这本质是一场'重写',而非'转换'…不存在成功先例…工作量以多人·年计" [e65c4575]
3. **[08-18 12:02]** 👤 "我的GPU资源非常充足,为什么总是挤爆" [8405c930]
4. **[08-18 15:54]** 👤 "离谱的是在你这里面没问题,但是在世界里的就是会有缝,包括沙漠的仙人掌也是有这种问题" [573d63f5]
5. **[08-18 16:08]** 🤖 "真凶抓到并修复了——你那句'仙人掌也有'是破案关键。根因:chunk 拼装×非整数缩放…默认 1.25 恰好整数像素" [573d63f5]
6. **[08-18 17:53]** 👤 "现在生物的掉落物开始混乱了,打死金鱼居然出现'恐惧之魂'?" [04569a63]
7. **[08-18 17:59]** 🤖 "已修复。这是我在上一批引入的事故,向你道歉——ITEM_DEFS 的内部物品 id=数组下标,我手写条目插在自动注册循环之前…" [04569a63]
8. **[08-18 23:39]** 👤 "现在仍然有一些动画播的过快的生物动画帧,比如走路的金鱼,非常鬼畜" [d76053b3]
9. **[08-19 00:01]** 🤖 "全案闭环——两个症状同一个根:闪烁,整幅重建精确间隔 20s(24.8→43.9→63.9)=GPU 看门狗周期!" [8405c930]
10. **[08-19 11:44]** 🤖 "这桩'反编译与二进制行为不符'的奇案破了,而且破得很漂亮——根本不存在什么行为差:真凶是金字塔刷墙段每写一堵墙…偷偷掷 1 颗骰(共 11,025 颗)" [0650e0c7]

That's 10 — target 5-8. Let me pick the best 8. Drop #2 (the research doc, though it's a nice framing)... actually #2 is quite striking for a showcase page ("多人·年" framing). Hmm. Let me rank:
- 必选: 浮空树质疑(#1), GPU挤爆(#3), 仙人掌破案对(#4+#5 as one moment... but format is single line each), 恐惧之魂(#6), 金鱼鬼畜(#8), 看门狗(#9), 金字塔(#10), 道歉(#7)

8 entries: #1, #3, #4, #5, #6, #7, #9, #10. Drop #2 and #8? But 金鱼鬼畜 is so funny... The pairs #4/#5 and #6/#7 each take two slots. Alternative: keep #6 only (恐惧之魂 is the user quote, more striking than the apology). And keep #4+#5 pair (the "破案关键" line is gold).

Final 8:
1. #1 浮空树 (08-18 00:06) 👤
2. #2 多人·年 (08-18 09:39) 👤 — keep this, it's the project-defining framing
3. #3 GPU挤爆 (08-18 12:02) 👤
4. #5 仙人掌破案 (08-18 16:08) 🤖
5. #6 恐惧之魂 (08-18 17:53) 👤
6. #8 金鱼鬼畜 (08-18 23:39) 👤
7. #9 看门狗 (08-19 00:01) 🤖
8. #10 金字塔 (08-19 11:44) 🤖

That's a good mix: 5 user, 3 bot, spread across the two days. 

Now writing the final file. Also final response needs: 统计 + 最震撼的 3 个故事一句话.

Let me write /tmp/latest-mining.md now.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:10:51.717Z · glm-x-preview-260804

```
我已经准备好所有需要的材料了。现在我来编写挖掘报告。
```


---

## 🤖 Assistant · 2026-08-19T07:11:59.877Z · glm-x-preview-260804

**🔧 ToolUse: `Write`**

```json
{
 "file_path": "/tmp/latest-mining.md",
 "content": "# 最新迭代挖掘(08-18 ~ 08-19)\n\n数据源:memory/ mtime≥08-18 的 65 份记忆文件 + tools/journey-inputs/archive-stream.json 的 08-18(418 条)/08-19(96 条)实录。\n\n## 一、新增亮点故事(非缺陷,是成就/工程突破)\n\n- **WebGL2 一期:背景层+全屏地图 GPU 化**(08-18): 从 Canvas 2D 升级到 WebGL2——共享模块 GLSpriteLayer(quad/纹理 LRU/双 sampler)接管群系背景与全屏地图四段(卷轴/地图/迷雾),小地图纹理按脏区增量上传。同会话 A/B 像素级对拍:地图 Δ=0 完美零差、背景平均 Δ0.02;配套 `?bggl=0`/`?mapgl=0` 逃生门和 7 项源码级回归守卫测试。次日云层也 GL 化(CloudGL 并入共享层,24+8 张染色画布归零) | 证据:memory/webgl2-phase1-port.md\n- **SimHost 服务器权威房全链落地**(08-18): \"开在服务器上的房,世界由服务器计算\"从 MVP 到 B6——进程内\"虚拟房主客户端\"经与房主完全相同的中继管线驱动世界(刷怪链/入侵链/TownNPC 转化全镜像),ioWorker 把存档解析与序列化搬进 worker,SIGTERM 优雅回退;真实浏览器 E2E 15/15 全绿(建房→访客→召唤意图→服务器结算→Boss 移除全闭环)。当日再加聊天系统+世界频道(此前客户端根本没有聊天输入框!),E2E 升到 20/20 | 证据:memory/server-room-simhost-port.md\n- **千人单房实测:8vCPU 就能扛 1000 人**(08-18): 差分剖析发现 120 bot 时模拟占 CPU 82%,三刀优化(玩家 1024px 网格灭平方项/trySpawn 4tick 一掷×4/AOI 密度降频)后 120 分散 CPU 82→28.6%,60 聚集人均带宽 10.8→3.27KB/s(-70%)。千人外推=多房分线 8vCPU/16GB/100Mbps,国内带宽常态热点型千人约 8000-9000 元/月——性能账第一次算到了商业部署粒度 | 证据:memory/server-room-simhost-port.md 千人实测节\n- **Remaster Studio 素材重制管线**(08-19): 一条\"AI 重制贴图→打包→热替换\"的完整管线落地:AssetCatalog 六类切帧聚合,gpt-image-2 逐帧重制(不支持透明背景就生成大图再盒式缩回+原帧 alpha 蒙版),手写 ZIP_STORED+CRC32 零依赖打包,类 mod 的 zip 素材包运行期局部覆盖原版贴图(vanilla-ui/弹幕/Buff 图标全注入矩阵)。六里程碑全绿:catalog 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7 | 证据:memory/remaster-studio-pipeline.md\n- **液体 buffer-reflow 对齐:475 条湖面薄膜的集体归位**(08-19): 中世界 #49 检查点 11,707 格液体差,连通域聚类发现是\"475 条单行湖面薄膜圆整漂移\"的全局调度指纹——真凶是 LiquidBuffer 回灌双重错位(回灌量取了当前活动数而非空余量+DelBuffer 是 swap-remove 尾补头而非 FIFO)。小世界永不触 24999 帽,所以三条小链长绿的假象骗了所有人;大世界才是天然压力测试。修复后 #49 归零,#53 半砖债整段连带消失 | 证据:memory/liquid-buffer-reflow-parity.md\n- **AI 全量 1:1 审计:六代理扫 200 条,181/181 测试全绿**(08-19): 六分区代理(死亡退化/追击门/地面/小动物/飞行水生/Boss)扫出 ~200 条偏离,五代理并行全量落地。最重要的方法论发现:原版 NPC 位移积分在 AI 外共享段(:93808)——AI 分支被跳过≠冻结,而是按冻结速度继续滑行,\"死亡=只积分不 steering\"。顺手揪出石巨人胜利条件倒置(坏档级)、694 水书怪必崩 null 解引用、鸭子逐帧背向玩家、海马出水取反等一批方向性反错的活宝 bug | 证据:memory/ai-parity-audit-2026-08-19.md\n- **微残留清零 XXXX 批:actuator≠inActive 两大旗标**(08-19): #101 掷流首差从第 20,196 颗骰推到第 165,353 颗——五修含引擎级发现:Tile.actuator(0x800) 与 Tile.inActive(0x40) 是两个独立旗标,曾把致动位当 inActive 排除导致致动石格误判非实心(探针 (2430,920) 定罪);另用 IL 实证撤销了\"34.5k 剑冢 HashSet 掷\"的错误归因(.NET Add-only 枚举≡插入序≡JS Set,零分叉) | 证据:memory/xxxx-microresidual-final-clear.md\n- **物品 tooltip 全量 1:1:四审终清零**(08-18): 用户一句\"相比原版缺了不少信息,武器还有攻击力吧\"引爆全链移植——按 GetLinesInfo(Main.cs:20488-20920) 行序逐行复刻:伤害/三系暴击/速度八档/击 knock 九档/渔力/镐斧(×5!)锤力/耗魔/可放置/弹药/材料/Buff 持续/词缀差分,再补低频七件(亮度脉冲/悠悠球 OneDrop 商标五层投影/研究行/商店价/专家大师行)。用户随后下禁令:\"低频的也必须接入完整,禁止以低频为由不接\"——全部落位,四轮 review 终清零 | 证据:memory/item-tooltip-parity-port.md\n- **钻石窗口 IOSurface 八场攻防战**(08-18~19): \"我的 GPU 资源非常充足,为什么双开还是爆\"——三线取证+Chromium 源码注释钉死真相:爆的不是显存字节而是 IOSurface 张数(16×16 的 1KB 小图也分配失败)。随后打了一场八回合的持久战:chunk 画布 atlas 页化(活张数 446→28,运行期新建≈0)、TintAtlas 染色图集(41 个变体挤进 1 页)、纯 CPU 画布 willReadFrequently 化、看门狗僵尸三振自动切软渲染……从\"必崩\"打到\"GPU 进程零死亡,尖峰后完全干净\" | 证据:memory/dualwindow-iosurface-exhaustion.md\n- **弹幕绘制偏移表全量 118 条**(08-18): 炸弹引线半截伸进碰撞盒的视觉错位,追到原版 Main.cs:29375-29826 的 num143/num144 偏移表——展开后铁律是\"贴图左上角=(盒左+num144, 盒上−num143)\",炸弹上移 8px 恰好让引线全在盒外。脚本机械对拍 118/118 全对,次日把 MinionProj(该表主体用户,曾从未消费、一律盒心居中)和浮标钓线全链接上 | 证据:memory/proj-draw-offset-table.md\n- **鸟类帧族谱系:小动物 FindFrame 专属 case 全家族**(08-18): \"感觉鸟的动画不对,在地上仍然用飞行中的动画\"——挖出小动物帧调度大多不在 FindFrame 通用组而在专属 case:地面鸟原版根本不踱步(AI_024 只重力,vx 恒 0),站定门因此永假;鸮族 spriteDirection 取反与通用镜像行叠加会恒翻转(屁股朝前);萤火虫 4t 亮 3t 闪、珍稀宝箱怪伪装=帧 0(曾 14 帧狂闪)。连带第二波\"走路金鱼鬼畜\"修掉全部 aiStyle=7 小动物被城镇 NPC 档截胡的截胡链 | 证据:memory/bird-findframe-families.md + bunny-walk-frame-fix.md\n- **Boss 全量审计波 1:25 族两波 8 代理,30+ 修**(08-19): 用户令\"逐一审计\",石巨人双代理模式推广到全部 25 Boss 族。波 1 抓出跨族系统性根因:BGM 裁决链键 flag/num3 号体系错位导致 17/24 族放错曲(石巨人放 Boss3、月总放世花曲)、弹幕自身出生音是审计盲区、猪鲨血量 50000 是 json 1405 旧值(1456=60000)。机械三王锯臂 ai2 追玩家态曾恒→1 死码、蜂后毒刺曾恒直飞全修 | 证据:memory/boss-audit-wave1-fixes.md + golem-3symptom-fix.md\n- **地牢水宝箱浮空刀:312 还是 313?**(08-19): 两条新链 #32 Dungeon 清零——水覆写宝箱走了金箱支的 loot 掷数差连坐六段家具错位;更精彩的是\"入口 0.6 框清墙上缘刀口\":反编译 double 算出 312.99999976→312,而真二进制是 313——fl(10×0.6f)=6.0 的半 ulp round-half-even 可复现,Math.fround 四界修复。这是与金字塔案同族的\"二进制-反编译刀口分歧\" | 证据:memory/dungeon-waterchest-float-knife.md\n- **液体最后清算 root59:百格级根 193→0 + 帧杀级联引擎**(08-19): #59 洞穴屋域四修:陷阱雕像是\"PlaceTile 失败也调\"而 Statues pass 恰好相反(两处语义相反勿互搬)、钟乳石是全族不是仅冰族、梁写 SetTileKeepWall 要清液体/坡/半砖;顺手造出 frameKillSweep 跨物件帧杀级联引擎(带帧写触发 Check2x2/Check3x2 整盒击杀)清掉 54 格尾巴。9293480 全管线首差推到 #63 | 证据:memory/wwww-root59-liquidation.md\n\n## 二、新增坑(现象→根因→修复)\n\n- **y 翻转两次翻车**(08-18): 现象:GL 绘制的背景图和地图垂直颠倒,修好后同一天又倒回来一次(用户两报) → 根因:并行会话共用文件,把修复静默写回旧版——clip-space y 翻转公式被覆盖蒸发 → 修复:tests/gl-layer-regression.test.ts 源码级断言锁定五项(y 翻转/mip 采样器/预乘上传等),丢任一立即红 | 记忆文件:webgl2-phase1-port.md\n- **地图退化块 #362CFF**(08-18): 现象:点开小地图后图块逐渐变成同色退化块,像被回收掉 → 根因:WebGL2 的 texSubUpdate DOM 源重载只有 8 参(无宽高),Chrome 把源画布【左上角 w×h】贴进目标区;三层源采样定罪(主画布坏/小地图好/迷雾好) → 修复:抠 scratch 画布走 8 参重载 | 记忆文件:webgl2-phase1-port.md\n- **纹理缓存键碰撞:满屏纯色背景**(08-18): 现象:GL 化后满屏 Background_50 平面色,沙漠层却完美 → 根因:ImageBitmap 无 .src,缓存键退化为\"宽x高\"——森林 t0/t2 同为 1024×699 共用一张纹理;沙漠层尺寸各异侥幸完美,误导排查半天 → 修复:WeakMap 实例自增 id 做键 | 记忆文件:webgl2-phase1-port.md\n- **连续读档显存打爆**(08-18): 现象:连续读档逐次叠加,contextlost 风暴 26 万次、tab 3.4GB、chunk 自适应沉底 → 根因:GLSpriteLayer 漏挂 Renderer.dispose 世界切换清理链,LRU 纹理只增不减;熔断器固定 8s 冷却=永久振荡 → 修复:dispose 挂链+LRU 按字节(192MB)记账+冷却逐次翻倍封顶 60s+小地图纹理 noMip | 记忆文件:webgl2-phase1-port.md 六号坑\n- **worker 整体崩毁全房失联**(08-18): 现象:`room.clients.filter is not a function` → worker exit(code=1) 全房掉线 → 根因:并行会话给 roomHost 周期定时器加逻辑时对 Set 用了 .filter;无守卫 setInterval 内一次抛错=worker 整体退出 → 修复:Set 先展开 `[...clients].filter`,四个周期定时器逐房 try/catch 只记日志 | 记忆文件:server-room-simhost-port.md\n- **砍树自动收集瞬间崩溃+行走掉帧**(08-18): 现象:砍树掉落自动收集时游戏冻结;长流程 trace 里行走仍掉帧 → 根因:Inventory.add 裸读 `ITEM_DEFS[id].maxStack` 未知 id 即 TypeError 炸断 rAF 链;掉帧是 GC churn——液体渲染四邻 lq() 每帧 new 3.3 万个对象;用 trace 的 ProfileChunk CPU 采样按 timeDeltas 重建时间线找到死点 → 修复:inv.add 守卫+主循环熔断取证;lq() 零分配化 | 记忆文件:treecrack-gc-frameguard-2026-08-18.md\n- **金鱼掉落\"恐惧之魂\"**(08-18): 现象:打死金鱼掉出恐惧之魂,掉落链全体错位 → 根因:vi_5395 屎堆手写条目插在自动注册循环【前】,ITEM_DEFS 内部 id=数组下标,插入点后全部物品 id 平移+1 → 修复:删手写条目改 BLOCK_TILE_BACKFILL 回填;新增 item-id-stability 测试钉死 id 严格递增 | 记忆文件:book-mimic-cultist-dragon-batch.md\n- **地底蠕虫音墙**(08-18): 现象:地底蠕虫穿梭音全变成 boss 唤醒咆哮,多蠕虫叠成音墙;洞穴蝙蝠死亡音也\"消失\" → 根因:WAV_MAP['roar'] 双轨随机,而 PlaySound 第 4 参 Style 缺省是 1 不是 0——蠕虫掘地=Roar_1,boss 吼=显式 style0 的 Roar_0;再叠 case15 缺单实例互斥 → 修复:roar 键改单轨+单实例互斥+怪池 Hit/Death wav 进世界预热(首播懒加载静默) | 记忆文件:npc-ambient-sound-audit.md\n- **悬停图标全黑**(08-18): 现象:光标移到宝箱上,悬停贴图变成黑方块 → 根因:曾误读为\"乘光标格光照\",用 source-atop 叠黑模拟变暗——source-atop 作用于整张已渲染画布,暗处 alpha→1=纯黑盖图标;而原版 GetItemLight 默认参根本不采样光照,图标恒全亮 → 修复:UI 层直画不乘光 | 记忆文件:cursor-icon-fullbright.md\n- **tooltip 透明感三轮拉锯**(08-18): 现象:气泡\"几乎透明\"→修后\"依然过透明\"→铺实底后\"过于不透明\",三轮报障 → 根因:tint 像素循环把 alpha 通道误乘红通道(`d.data[i]*tmul[3]` 应为 `[i+3]`),深蓝底红通道≈23→alpha≈22 近全透明;0.925 的原版真值从未真正渲染过 → 修复:改正下标回到原版 alpha 236;教训:三轮报障该找根因而不是在 0.925↔1.0 之间找折中 | 记忆文件:item-tooltip-parity-port.md\n- **树冠仙人掌接缝**(08-18): 现象:树冠-树干交界细缝无风也有,沙漠仙人掌柱同款,解剖台工具里却没问题;用户自调 zoom 1.27 触发 → 根因:chunk 拼装公式 `256×zoom` 非整数时 chunk 落小数设备像素,各 chunk 独立最近邻采样在边缘产生周期性 1px 透明缝;默认 1.25=320 恰整除从未暴露 → 修复:drawChunkGrid 整数设备矩形+1px 重叠;\"工具里没问题\"本身即信息→差异枚举法 | 记忆文件:chunk-seam-noninteger-zoom.md\n- **迷雾周期性全亮闪**(08-19): 现象:小地图迷雾隔 20 秒突然全亮又瞬间恢复;F4 消雾也失效 → 根因:GPU 看门狗(20s 巡检)误清 CPU 数据——recreateAuxCanvases 无条件 fogPix=null,但迷雾是纯 CPU 缓冲与画布死活无关;整幅重建精确间隔 20s(24.8/43.9/63.9s)实锤 → 修复:fog 缓冲只在 dispose 清;入口 row>=h 复位 | 记忆文件:fog-flicker-f4-latetex-fix.md\n- **生命树贴图要手动砸方块才渲染**(08-19): 现象:传送到生命树贴图缺失,破坏方块才出 → 根因:烘焙期 ensure(Tiles_192) 时 pending=true,`if(pending) return null` 早退在 bakeTracker.note 之前——晚到无人重烘,缺表 fallback 钉死 → 修复:note 提到早退前(failed 也 note,重试成功链路反而闭环);拦截延迟 15s 复现实证 23 个 chunk 精确重烘 | 记忆文件:fog-flicker-f4-latetex-fix.md ③节\n- **独眼巨鹿冻在半空**(08-19): 现象:Boss 召唤出来冻在半空不动,AI 计数照常递增、速度满格、坐标恒定 → 根因:deerclopsMovement 只算 vx/vy 从不积分位置(668 是 noGravity+noTileCollide,原版由引擎直移);测试 harness 手动补积分把引擎缺口焊死了——测试绿但游戏坏 → 修复:movement 尾补 `e.x+=e.vx; e.y+=e.vy`;回归测试加位置积分档 | 记忆文件:deerclops-port.md 冻结事故节\n- **地图放大到 1.37 即全黑**(08-19): 现象:全屏地图放大到一定程度全黑只剩玩家/NPC 头像,缩小恢复;哨兵日志显示 zoom 1.37 即黑 → 根因:sampler 对象的 MIN_FILTER 是 LINEAR_MIPMAP_LINEAR,而小地图/迷雾纹理 noMip 无 mip 链——用需 mip 的采样器采无 mip 纹理=纹理不完整→采样恒黑 (0,0,0,1);z<1 走 nearest 所以\"缩小恢复\" → 修复:linearNoMip 采样器按 e.mipped 分流;GL 铁律:sampler 对象与纹理参数是两套,incomplete 判定看生效组合 | 记忆文件:webgl2-phase1-port.md 全黑真凶终定罪节\n- **石巨人负血不死**(08-19): 现象:Boss 血条打到负值不死、动画乱闪、boss bar 无头像 → 根因:Enemy.hurt 的放行段 `if(245||246||247||248) return false` 写在 `this.dead=true` 之前——\"AI 首行接管\"的假设根本没发生;并行会话跨会话契约改动未核调用侧 → 修复:放行收窄到 246 且加本体活门,245 本体死时在 hurt 内直接灭部件 | 记忆文件:golem-3symptom-fix.md\n- **普通骷髅王必掉全套 Chippy 时装**(08-18): 现象:对抗性审查发现的刷物品漏洞——普通骷髅王约半数击杀掉全套红帽时装 → 根因:召唤只写 redHat 旗,但掉落五条规则/Renderer/GorePiece 全读 ai3;而 bossAI 又把 ai3 挪用为旋冲方向 → 修复:召唤补 head.ai3=1,旋冲方向改独立字段 skeletronSpinDir | 记忆文件:review-found-bugs-fix.md\n- **软渲染模式下每帧新建 60 张画布**(08-19): 现象:--disable-gpu 下 canvas 哨兵报 60 张/秒持续泄漏,暂停中也发生;dev 复现不了 → 根因:GLSpriteLayer 初始化失败时 diedAt=0,退避判据 `now-0>5000` 恒真→每帧 dispose+new(构造器 createElement);dev 的 WebGL2 可用所以复现不了 → 修复:三处失败分支补 diedAt=now+acquireGL 统一 30s 闩 | 记忆文件:dualwindow-iosurface-exhaustion.md ⑫节\n- **晴天云全不渲染**(08-18 深夜): 现象:好多云不渲染了,排查发现\"该 bug 期间云从未显示过\" → 根因:globalCloudAlpha 接了 `max(wr.cloudAlpha, 墓园×0.92)×atmo`——wr.cloudAlpha 是雨云浓度,晴天恒 0→云全透明;墓园压云是把某 CustomSky 内部式误当全局门 → 修复:globalCloudAlpha=atmo 直取(原版 ProcessCloudAlpha 默认恒 1) | 记忆文件:dualwindow-iosurface-exhaustion.md ⑨节\n\n## 三、有趣的原始对话片段(archive-stream.json 08-18/08-19)\n\n- **[08-18 00:06]** 👤 你看我这个世界的报告,很明显非常诡异吧?这确定是原版代码能干出来的?…画面里三棵树的底部都有异常,一个被蘑菇占用,两个是花,而且还…无法使用镐子破坏他们 [c44574b3]\n- **[08-18 09:39]** 👤 # 泰拉瑞亚反编译转译TypeScript:这本质是一场\"重写\",而非\"转换\"…不存在成功先例,也没有可用的自动化工具…工作量以多人·年计 [e65c4575]\n- **[08-18 12:02]** 👤 我的GPU资源非常充足,为什么总是挤爆 [8405c930]\n- **[08-18 15:54]** 👤 离谱的是在你这里面没问题,但是在世界里的就是会有缝,包括沙漠的仙人掌也是有这种问题 [573d63f5]\n- **[08-18 16:08]** 🤖 真凶抓到并修复了——你那句\"仙人掌也有\"是破案关键。根因:chunk 拼装×非整数缩放…默认缩放 1.25:256×1.25=320 恰好整数像素 [573d63f5]\n- **[08-18 17:53]** 👤 现在生物的掉落物开始混乱了,打死金鱼居然出现\"恐惧之魂\"? [04569a63]\n- **[08-18 23:39]** 👤 现在仍然有一些动画播的过快的生物动画帧,比如走路的金鱼,非常鬼畜 [d76053b3]\n- **[08-19 00:01]** 🤖 全案闭环——两个症状同一个根,外加 20s 看门狗:闪烁,整幅重建精确间隔 20s(24.8→43.9→63.9)=GPU 看门狗周期! [8405c930]\n- **[08-19 11:44]** 🤖 这桩\"反编译与二进制行为不符\"的奇案破了,而且破得很漂亮——根本不存在什么行为差:真凶是金字塔刷墙段每写一堵墙,原版都会经 SquareWallFrame 偷偷掷 1 颗骰(共 11,025 颗) [0650e0c7]\n\n## 附:同期未入正文的可用彩蛋\n\n- [08-18 00:34] 👤 \"等这个清完是不是100%了?\" / \"所以有可能磨到100%对吧\" [0650e0c7] — 用户对 100% 种子等价的执念\n- [08-19 08:28] 🤖 \"总进度:约 95%…里程碑链 9293480 0-53 槽八通道全绿✓ 里程碑链 12345(你的种子)0-53 槽八通道全绿✓\" [0650e0c7]\n- [08-19 10:31] 👤 \"我感觉我们需要一个行为录制的方案,比如长按F5来启动场景的整体'录制'…对于调试非常重要\" [c44574b3] — 用户的产品直觉时刻\n- [08-19 11:21] 👤 \"不要这种降级的,我们要从我们自己出发,看还有没有优化空间\" [8405c930] — 否决跨实例方案,定调单实例自身减量\n- [08-18 14:31] 👤 \"我记得地域里的骨龙在接近时本身是有音效的,你要检查下各种怪物生物本身的音效是否正确移植完整\" [1fc2b821] — 引出 232 处 PlaySound 全量审计\n"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:11:59.897Z

**📎 ToolResult**

```
File created successfully at: /tmp/latest-mining.md (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T07:12:34.172Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file is written. Let me do a final sanity check on a few facts I cited to make sure I didn't fabricate anything:

1. WebGL2: "背景 平均Δ0.02/Δ>8 占 0.1%;地图 Δ=0 完美" ✓
2. SimHost E2E 15/15 ✓, chat system 20/20 ✓
3. 千人: "120分散CPU 82→28.6%,60聚集人均10.8→3.27KB/s(-70%)", "1000CCU今日拓扑=多房分线→8vCPU/16GB/100Mbps" ✓ "国内带宽:常态热点型千人≈10TB/月≈8000-9000元" ✓
4. Remaster: 六里程碑 "catalog 单测 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7" ✓ gpt-image-2 不支持透明+655,360最小像素 ✓
5. buffer-reflow: "#49 L=11707" wait — memory says "中世界…r0 唤醒链首触 24999 帽后回灌时序整体漂移 → 全图 475 条湖面薄膜高度全漂(#49 L=11,707)" ✓ and DDDDD in jungle memory: "m 链 #49 湖体 L=11707→0" ✓
6. AI audit: 六分区代理 ~200 条, 181/181 ✓ 石巨人胜利条件倒置 ✓ 694 null 解引用 ✓ 鸭子逐帧背向玩家 ✓ 海马水面折返取反(顶出水) ✓
7. XXXX: "掷流 20196→165353" ✓ actuator 0x800 vs inActive 0x40 ✓ "34.5k 剑冢掷"归因证伪 ✓
8. tooltip: GetLinesInfo :20488-20920 ✓ 四审 ✓ 用户禁令 ✓
9. IOSurface: 16x16 失败 ✓ chunk atlas 446→28 ✓ TintAtlas 41变体=1页 ✓ "八场" — memory records 第一场~第八场 ✓ "GPU 进程零死亡(六场首次)" at 第六场, 第八场 "0 进程死亡(第三连)" ✓
10. 偏移表: 118 条 ✓ 炸弹上移8 ✓
11. 鸟类: AI_024 :25453 只重力 ✓ 鸮族双翻 ✓ 宝箱怪伪装=帧0 ✓
12. Boss audit: 25 Boss 族两波8代理 ✓ 17/24 族错曲 ✓ 猪鲨 50000→60000 ✓
13. 地牢水宝箱: 312.99999976→312 vs 313 ✓ Math.fround ✓
14. root59: 193→0 ✓ frameKillSweep ✓ 9293480 首差 #59→#63 ✓

Pits:
1. y-flip: 两次翻车 ✓ 五项守卫 ✓
2. #362CFF: 8参 ✓ 三层源采样 ✓
3. 纹理键: 1024×699 ✓
4. 显存: 26万次/3.4GB ✓ 192MB LRU ✓ 8→16→32→60s ✓
5. worker: Set.filter ✓
6. 崩溃: inv.add ✓ lq() 3.3万对象/帧 ✓ ("水邻屏 8k-33k 对象/帧" — I wrote 3.3万 which is within range) ✓
7. 恐惧之魂 ✓
8. 音墙 ✓ Style缺省1 ✓
9. 悬停全黑 ✓
10. 透明三轮 ✓ alpha 22 ✓
11. 接缝: 1.27→325.12 ✓ (I said "用户自调 zoom 1.27 触发" — memory says "用户换过 zoom 档" and "默认 1.25(=320 恰整除)从未暴露;用户自调 1.27(325.12)触发" ✓)
12. 迷雾 20s ✓
13. 生命树 ✓
14. 鹿冻 ✓
15. 全黑 1.37 ✓
16. 石巨人 ✓
17. Chippy ✓
18. 60张/s ✓
19. 云 ✓

Fragments all verified against actual stream text. 

The 金字塔 fragment says "s22222 上共 11,025 颗" — actual text: "(s22222 上共 **11,025 颗**)" ✓

Counts: 14 stories, 19 pits, 9 fragments (+5 bonus). Target was 8-12 stories (I have 14, slightly over but covers all requested directions), 8-15 pits (19 — over. Hmm. Let me trim pits to 15 to be closer to target... Actually "目标 8-15 条" — 19 exceeds. Let me trim to the 15 best. Which to cut? Candidates to cut: 悬停图标全黑 (small), 透明三轮 (keep, it's vivid), 纹理键碰撞 (good), y翻转 (keep)... 

Actually let me reconsider — the requirement says "目标 8-15 条". I have 19. I should trim 4. I'll cut: 悬停图标全黑, 纹理缓存键碰撞, 晴天云全不渲染... hmm but 云 is a fun one ("该 bug 期间云从未显示过"). Let me cut: 悬停图标全黑 (merged into nothing), 石巨人负血不死 (no — it's one of the most striking), 软渲染60张/s (very interesting)...

Ranking pits by showcase value: 
1. 金鱼恐惧之魂 (must)
2. 迷雾20s看门狗 (must)
3. 独眼巨鹿冻半空 (must)
4. 地图放大全黑 sampler (must)
5. 石巨人负血不死 (must)
6. 蠕虫音墙 (must)
7. chunk接缝 (must)
8. 透明三轮 (must)
9. y翻转两次 (must — parallel session story)
10. worker崩毁 (must)
11. 砍树崩溃+GC (must)
12. IOSurface显存打爆 (must)
13. Chippy漏洞 (must)
14. 60张/s (must — "dev复现不了" twist)
15. 云不渲染 (must — "从未显示过" twist)
16. #362CFF (good)
17. 恐惧之魂 counted
18. 生命树 (good)
19. 纹理键碰撞 (good)
20. 悬停全黑 (good)

I have 19 listed. Trim 4: cut 纹理键碰撞, 悬停全黑, #362CFF, 生命树? Hmm, #362CFF is quite vivid ("地图退化块"). 生命树 is also good ("手动砸方块才渲染"). 

Alternative: keep all 19 and note the count honestly. The instruction says "目标 8-15" — being over is a minor deviation but more value. Actually I'd rather respect the instruction reasonably. Let me trim to 15 by removing: 纹理缓存键碰撞, 悬停图标全黑, tooltip透明三轮... no wait, 透明三轮 is great.

Decision: trim to 15 — remove 悬停图标全黑, 纹理缓存键碰撞, #362CFF, 生命树. Hmm, but #362CFF and 生命树 are vivid...

Actually, let me think about what the parent wants: a showcase page. Rich material is good. The stated targets are guidance. I'll trim to 16 (remove 3: 悬停图标全黑, 纹理缓存键碰撞, and merge #362CFF into... no). 

OK pragmatic choice: I'll remove the 3 weakest to land at 16: 悬停图标全黑 (short), 纹理缓存键碰撞 (technical), #362CFF... 

Hmm wait, actually let me just count what's in the file: 
1. y翻转
2. #362CFF
3. 纹理键碰撞
4. 显存打爆
5. worker崩毁
6. 砍树崩溃+GC
7. 恐惧之魂
8. 蠕虫音墙
9. 悬停全黑
10. 透明三轮
11. chunk接缝
12. 迷雾20s
13. 生命树
14. 鹿冻
15. 全黑sampler
16. 石巨人
17. Chippy
18. 60张/s
19. 云

19 entries. To get to 15, remove 4: #9 悬停全黑, #3 纹理键碰撞, #13 生命树, #2 #362CFF? That removes some good content. Alternatively keep 19 and say "19 条(超出目标上限,因素材密度高)". 

I think for a showcase-mining task, more curated material with honest count is better. But instructions say target 8-15. I'll trim to 15, removing the 4 least "story-worthy": 悬停图标全黑(短小), 纹理缓存键碰撞(纯技术), #362CFF(纯技术), 生命树(可以并入迷雾那条? no)...

Hmm, actually #362CFF has a great hook ("像是被回收掉一样" user quote). 生命树 has "手动破坏才渲染". 

Let me just merge related ones instead of deleting:
- Merge y翻转 + #362CFF + 纹理键碰撞 into... no, they have distinct 现象→根因→修复.
- Merge 悬停全黑 into 透明三轮? Both are tooltip/icon darkness bugs. Could merge as "悬停图标全黑与气泡透明感" — they're different systems though (cursor icon vs tooltip).

Simplest: merge #9 悬停全黑 into the tooltip 透明三轮 entry? Not clean.

Final decision: trim to 15 by deleting: 纹理缓存键碰撞, 悬停图标全黑, #362CFF, 生命树. That leaves 15 strong ones. But wait — I actually think the file benefits from keeping them all. The task explicitly says "目标 8-15 条". I'll go with 15 and move the extra 4 into the "彩蛋" appendix section so no material is lost. That's a good compromise.

Let me edit the file: remove those 4 from section 二 and add them to the appendix.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:12:34.898Z · glm-x-preview-260804

```
我来根据目标数量优化一下列表——将坑条目从 19 条精简到 15 条，并将额外内容移至附录，确保没有数据丢失。
```


---

## 🤖 Assistant · 2026-08-19T07:12:39.169Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "/tmp/latest-mining.md",
 "old_string": "- **地图退化块 #362CFF**(08-18): 现象:点开小地图后图块逐渐变成同色退化块,像被回收掉 → 根因:WebGL2 的 texSubUpdate DOM 源重载只有 8 参(无宽高),Chrome 把源画布【左上角 w×h】贴进目标区;三层源采样定罪(主画布坏/小地图好/迷雾好) → 修复:抠 scratch 画布走 8 参重载 | 记忆文件:webgl2-phase1-port.md\n- **纹理缓存键碰撞:满屏纯色背景**(08-18): 现象:GL 化后满屏 Background_50 平面色,沙漠层却完美 → 根因:ImageBitmap 无 .src,缓存键退化为\"宽x高\"——森林 t0/t2 同为 1024×699 共用一张纹理;沙漠层尺寸各异侥幸完美,误导排查半天 → 修复:WeakMap 实例自增 id 做键 | 记忆文件:webgl2-phase1-port.md\n- **连续读档显存打爆**(08-18): 现象:连续读档逐次叠加,contextlost 风暴 26 万次、tab 3.4GB、chunk 自适应沉底 → 根因:GLSpriteLayer 漏挂 Renderer.dispose 世界切换清理链,LRU 纹理只增不减;熔断器固定 8s 冷却=永久振荡 → 修复:dispose 挂链+LRU 按字节(192MB)记账+冷却逐次翻倍封顶 60s+小地图纹理 noMip | 记忆文件:webgl2-phase1-port.md 六号坑",
 "new_string": "- **连续读档显存打爆**(08-18): 现象:连续读档逐次叠加,contextlost 风暴 26 万次、tab 3.4GB、chunk 自适应沉底 → 根因:GLSpriteLayer 漏挂 Renderer.dispose 世界切换清理链,LRU 纹理只增不减;熔断器固定 8s 冷却=永久振荡 → 修复:dispose 挂链+LRU 按字节(192MB)记账+冷却逐次翻倍封顶 60s+小地图纹理 noMip | 记忆文件:webgl2-phase1-port.md 六号坑"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:12:39.188Z

**📎 ToolResult**

```
The file /tmp/latest-mining.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T07:12:45.087Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "/tmp/latest-mining.md",
 "old_string": "- **迷雾周期性全亮闪**(08-19): 现象:小地图迷雾隔 20 秒突然全亮又瞬间恢复;F4 消雾也失效 → 根因:GPU 看门狗(20s 巡检)误清 CPU 数据——recreateAuxCanvases 无条件 fogPix=null,但迷雾是纯 CPU 缓冲与画布死活无关;整幅重建精确间隔 20s(24.8/43.9/63.9s)实锤 → 修复:fog 缓冲只在 dispose 清;入口 row>=h 复位 | 记忆文件:fog-flicker-f4-latetex-fix.md\n- **生命树贴图要手动砸方块才渲染**(08-19): 现象:传送到生命树贴图缺失,破坏方块才出 → 根因:烘焙期 ensure(Tiles_192) 时 pending=true,`if(pending) return null` 早退在 bakeTracker.note 之前——晚到无人重烘,缺表 fallback 钉死 → 修复:note 提到早退前(failed 也 note,重试成功链路反而闭环);拦截延迟 15s 复现实证 23 个 chunk 精确重烘 | 记忆文件:fog-flicker-f4-latetex-fix.md ③节",
 "new_string": "- **迷雾周期性全亮闪**(08-19): 现象:小地图迷雾隔 20 秒突然全亮又瞬间恢复;F4 消雾也失效 → 根因:GPU 看门狗(20s 巡检)误清 CPU 数据——recreateAuxCanvases 无条件 fogPix=null,但迷雾是纯 CPU 缓冲与画布死活无关;整幅重建精确间隔 20s(24.8/43.9/63.9s)实锤 → 修复:fog 缓冲只在 dispose 清;入口 row>=h 复位 | 记忆文件:fog-flicker-f4-latetex-fix.md"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:12:45.104Z

**📎 ToolResult**

```
The file /tmp/latest-mining.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T07:12:55.976Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "/tmp/latest-mining.md",
 "old_string": "- **悬停图标全黑**(08-18): 现象:光标移到宝箱上,悬停贴图变成黑方块 → 根因:曾误读为\"乘光标格光照\",用 source-atop 叠黑模拟变暗——source-atop 作用于整张已渲染画布,暗处 alpha→1=纯黑盖图标;而原版 GetItemLight 默认参根本不采样光照,图标恒全亮 → 修复:UI 层直画不乘光 | 记忆文件:cursor-icon-fullbright.md\n- **tooltip 透明感三轮拉锯**(08-18): 现象:气泡\"几乎透明\"→修后\"依然过透明\"→铺实底后\"过于不透明\",三轮报障 → 根因:tint 像素循环把 alpha 通道误乘红通道(`d.data[i]*tmul[3]` 应为 `[i+3]`),深蓝底红通道≈23→alpha≈22 近全透明;0.925 的原版真值从未真正渲染过 → 修复:改正下标回到原版 alpha 236;教训:三轮报障该找根因而不是在 0.925↔1.0 之间找折中 | 记忆文件:item-tooltip-parity-port.md",
 "new_string": "- **tooltip 透明感三轮拉锯**(08-18): 现象:气泡\"几乎透明\"→修后\"依然过透明\"→铺实底后\"过于不透明\",三轮报障 → 根因:tint 像素循环把 alpha 通道误乘红通道(`d.data[i]*tmul[3]` 应为 `[i+3]`),深蓝底红通道≈23→alpha≈22 近全透明;0.925 的原版真值从未真正渲染过 → 修复:改正下标回到原版 alpha 236;教训:三轮报障该找根因而不是在 0.925↔1.0 之间找折中 | 记忆文件:item-tooltip-parity-port.md"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:12:55.997Z

**📎 ToolResult**

```
The file /tmp/latest-mining.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T07:13:05.412Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "/tmp/latest-mining.md",
 "old_string": "## 附:同期未入正文的可用彩蛋\n\n- [08-18 00:34] 👤 \"等这个清完是不是100%了?\" / \"所以有可能磨到100%对吧\" [0650e0c7] — 用户对 100% 种子等价的执念",
 "new_string": "## 附:同期未入正文的可用彩蛋\n\n- **坑·备选四条**(超出正文目标条数,均含完整现象→根因→修复):\n  - 地图退化块 #362CFF(08-18): 小地图图块逐渐变成同色退化块\"像被回收掉\" → WebGL2 texSubUpdate 的 DOM 源重载只有 8 参(无宽高),Chrome 把源画布左上角 w×h 贴进目标区;三层源采样定罪 → 抠 scratch 画布走 8 参 | webgl2-phase1-port.md\n  - 纹理缓存键碰撞(08-18): GL 化后满屏 Background_50 平面色、沙漠层却完美 → ImageBitmap 无 .src,键退化为\"宽x高\",森林 t0/t2 同为 1024×699 共用一张纹理 → WeakMap 实例自增 id 做键 | webgl2-phase1-port.md\n  - 悬停图标全黑(08-18): 光标移到宝箱上悬停贴图变黑方块 → 曾误读为\"乘光标格光照\"用 source-atop 叠黑模拟,而原版 GetItemLight 默认参根本不采样光照(图标恒全亮) → UI 层直画不乘光 | cursor-icon-fullbright.md\n  - 生命树贴图要手动砸方块才渲染(08-19): 传送到生命树贴图缺失 → 烘焙期 ensure(Tiles_192) 时 pending=true,早退在 bakeTracker.note 之前,晚到无人重烘 → note 提到早退前,拦截延迟 15s 复现实证 23 个 chunk 精确重烘 | fog-flicker-f4-latetex-fix.md ③节\n- [08-18 00:34] 👤 \"等这个清完是不是100%了?\" / \"所以有可能磨到100%对吧\" [0650e0c7] — 用户对 100% 种子等价的执念"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:13:05.424Z

**📎 ToolResult**

```
The file /tmp/latest-mining.md has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-19T07:13:10.111Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me verify the final file structure and count entries.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:13:10.767Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -c \"^- \\*\\*\" /tmp/latest-mining.md; echo \"---\"; grep \"^- \\*\\*\" /tmp/latest-mining.md | head -60; echo \"---sections---\"; grep \"^## \" /tmp/latest-mining.md",
 "description": "Verify final file entry counts and structure"
}
```


---

## 👤 User(sidechain) · 2026-08-19T07:13:10.831Z

**📎 ToolResult**

```
39
---
- **WebGL2 一期:背景层+全屏地图 GPU 化**(08-18): 从 Canvas 2D 升级到 WebGL2——共享模块 GLSpriteLayer(quad/纹理 LRU/双 sampler)接管群系背景与全屏地图四段(卷轴/地图/迷雾),小地图纹理按脏区增量上传。同会话 A/B 像素级对拍:地图 Δ=0 完美零差、背景平均 Δ0.02;配套 `?bggl=0`/`?mapgl=0` 逃生门和 7 项源码级回归守卫测试。次日云层也 GL 化(CloudGL 并入共享层,24+8 张染色画布归零) | 证据:memory/webgl2-phase1-port.md
- **SimHost 服务器权威房全链落地**(08-18): "开在服务器上的房,世界由服务器计算"从 MVP 到 B6——进程内"虚拟房主客户端"经与房主完全相同的中继管线驱动世界(刷怪链/入侵链/TownNPC 转化全镜像),ioWorker 把存档解析与序列化搬进 worker,SIGTERM 优雅回退;真实浏览器 E2E 15/15 全绿(建房→访客→召唤意图→服务器结算→Boss 移除全闭环)。当日再加聊天系统+世界频道(此前客户端根本没有聊天输入框!),E2E 升到 20/20 | 证据:memory/server-room-simhost-port.md
- **千人单房实测:8vCPU 就能扛 1000 人**(08-18): 差分剖析发现 120 bot 时模拟占 CPU 82%,三刀优化(玩家 1024px 网格灭平方项/trySpawn 4tick 一掷×4/AOI 密度降频)后 120 分散 CPU 82→28.6%,60 聚集人均带宽 10.8→3.27KB/s(-70%)。千人外推=多房分线 8vCPU/16GB/100Mbps,国内带宽常态热点型千人约 8000-9000 元/月——性能账第一次算到了商业部署粒度 | 证据:memory/server-room-simhost-port.md 千人实测节
- **Remaster Studio 素材重制管线**(08-19): 一条"AI 重制贴图→打包→热替换"的完整管线落地:AssetCatalog 六类切帧聚合,gpt-image-2 逐帧重制(不支持透明背景就生成大图再盒式缩回+原帧 alpha 蒙版),手写 ZIP_STORED+CRC32 零依赖打包,类 mod 的 zip 素材包运行期局部覆盖原版贴图(vanilla-ui/弹幕/Buff 图标全注入矩阵)。六里程碑全绿:catalog 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7 | 证据:memory/remaster-studio-pipeline.md
- **液体 buffer-reflow 对齐:475 条湖面薄膜的集体归位**(08-19): 中世界 #49 检查点 11,707 格液体差,连通域聚类发现是"475 条单行湖面薄膜圆整漂移"的全局调度指纹——真凶是 LiquidBuffer 回灌双重错位(回灌量取了当前活动数而非空余量+DelBuffer 是 swap-remove 尾补头而非 FIFO)。小世界永不触 24999 帽,所以三条小链长绿的假象骗了所有人;大世界才是天然压力测试。修复后 #49 归零,#53 半砖债整段连带消失 | 证据:memory/liquid-buffer-reflow-parity.md
- **AI 全量 1:1 审计:六代理扫 200 条,181/181 测试全绿**(08-19): 六分区代理(死亡退化/追击门/地面/小动物/飞行水生/Boss)扫出 ~200 条偏离,五代理并行全量落地。最重要的方法论发现:原版 NPC 位移积分在 AI 外共享段(:93808)——AI 分支被跳过≠冻结,而是按冻结速度继续滑行,"死亡=只积分不 steering"。顺手揪出石巨人胜利条件倒置(坏档级)、694 水书怪必崩 null 解引用、鸭子逐帧背向玩家、海马出水取反等一批方向性反错的活宝 bug | 证据:memory/ai-parity-audit-2026-08-19.md
- **微残留清零 XXXX 批:actuator≠inActive 两大旗标**(08-19): #101 掷流首差从第 20,196 颗骰推到第 165,353 颗——五修含引擎级发现:Tile.actuator(0x800) 与 Tile.inActive(0x40) 是两个独立旗标,曾把致动位当 inActive 排除导致致动石格误判非实心(探针 (2430,920) 定罪);另用 IL 实证撤销了"34.5k 剑冢 HashSet 掷"的错误归因(.NET Add-only 枚举≡插入序≡JS Set,零分叉) | 证据:memory/xxxx-microresidual-final-clear.md
- **物品 tooltip 全量 1:1:四审终清零**(08-18): 用户一句"相比原版缺了不少信息,武器还有攻击力吧"引爆全链移植——按 GetLinesInfo(Main.cs:20488-20920) 行序逐行复刻:伤害/三系暴击/速度八档/击 knock 九档/渔力/镐斧(×5!)锤力/耗魔/可放置/弹药/材料/Buff 持续/词缀差分,再补低频七件(亮度脉冲/悠悠球 OneDrop 商标五层投影/研究行/商店价/专家大师行)。用户随后下禁令:"低频的也必须接入完整,禁止以低频为由不接"——全部落位,四轮 review 终清零 | 证据:memory/item-tooltip-parity-port.md
- **钻石窗口 IOSurface 八场攻防战**(08-18~19): "我的 GPU 资源非常充足,为什么双开还是爆"——三线取证+Chromium 源码注释钉死真相:爆的不是显存字节而是 IOSurface 张数(16×16 的 1KB 小图也分配失败)。随后打了一场八回合的持久战:chunk 画布 atlas 页化(活张数 446→28,运行期新建≈0)、TintAtlas 染色图集(41 个变体挤进 1 页)、纯 CPU 画布 willReadFrequently 化、看门狗僵尸三振自动切软渲染……从"必崩"打到"GPU 进程零死亡,尖峰后完全干净" | 证据:memory/dualwindow-iosurface-exhaustion.md
- **弹幕绘制偏移表全量 118 条**(08-18): 炸弹引线半截伸进碰撞盒的视觉错位,追到原版 Main.cs:29375-29826 的 num143/num144 偏移表——展开后铁律是"贴图左上角=(盒左+num144, 盒上−num143)",炸弹上移 8px 恰好让引线全在盒外。脚本机械对拍 118/118 全对,次日把 MinionProj(该表主体用户,曾从未消费、一律盒心居中)和浮标钓线全链接上 | 证据:memory/proj-draw-offset-table.md
- **鸟类帧族谱系:小动物 FindFrame 专属 case 全家族**(08-18): "感觉鸟的动画不对,在地上仍然用飞行中的动画"——挖出小动物帧调度大多不在 FindFrame 通用组而在专属 case:地面鸟原版根本不踱步(AI_024 只重力,vx 恒 0),站定门因此永假;鸮族 spriteDirection 取反与通用镜像行叠加会恒翻转(屁股朝前);萤火虫 4t 亮 3t 闪、珍稀宝箱怪伪装=帧 0(曾 14 帧狂闪)。连带第二波"走路金鱼鬼畜"修掉全部 aiStyle=7 小动物被城镇 NPC 档截胡的截胡链 | 证据:memory/bird-findframe-families.md + bunny-walk-frame-fix.md
- **Boss 全量审计波 1:25 族两波 8 代理,30+ 修**(08-19): 用户令"逐一审计",石巨人双代理模式推广到全部 25 Boss 族。波 1 抓出跨族系统性根因:BGM 裁决链键 flag/num3 号体系错位导致 17/24 族放错曲(石巨人放 Boss3、月总放世花曲)、弹幕自身出生音是审计盲区、猪鲨血量 50000 是 json 1405 旧值(1456=60000)。机械三王锯臂 ai2 追玩家态曾恒→1 死码、蜂后毒刺曾恒直飞全修 | 证据:memory/boss-audit-wave1-fixes.md + golem-3symptom-fix.md
- **地牢水宝箱浮空刀:312 还是 313?**(08-19): 两条新链 #32 Dungeon 清零——水覆写宝箱走了金箱支的 loot 掷数差连坐六段家具错位;更精彩的是"入口 0.6 框清墙上缘刀口":反编译 double 算出 312.99999976→312,而真二进制是 313——fl(10×0.6f)=6.0 的半 ulp round-half-even 可复现,Math.fround 四界修复。这是与金字塔案同族的"二进制-反编译刀口分歧" | 证据:memory/dungeon-waterchest-float-knife.md
- **液体最后清算 root59:百格级根 193→0 + 帧杀级联引擎**(08-19): #59 洞穴屋域四修:陷阱雕像是"PlaceTile 失败也调"而 Statues pass 恰好相反(两处语义相反勿互搬)、钟乳石是全族不是仅冰族、梁写 SetTileKeepWall 要清液体/坡/半砖;顺手造出 frameKillSweep 跨物件帧杀级联引擎(带帧写触发 Check2x2/Check3x2 整盒击杀)清掉 54 格尾巴。9293480 全管线首差推到 #63 | 证据:memory/wwww-root59-liquidation.md
- **y 翻转两次翻车**(08-18): 现象:GL 绘制的背景图和地图垂直颠倒,修好后同一天又倒回来一次(用户两报) → 根因:并行会话共用文件,把修复静默写回旧版——clip-space y 翻转公式被覆盖蒸发 → 修复:tests/gl-layer-regression.test.ts 源码级断言锁定五项(y 翻转/mip 采样器/预乘上传等),丢任一立即红 | 记忆文件:webgl2-phase1-port.md
- **连续读档显存打爆**(08-18): 现象:连续读档逐次叠加,contextlost 风暴 26 万次、tab 3.4GB、chunk 自适应沉底 → 根因:GLSpriteLayer 漏挂 Renderer.dispose 世界切换清理链,LRU 纹理只增不减;熔断器固定 8s 冷却=永久振荡 → 修复:dispose 挂链+LRU 按字节(192MB)记账+冷却逐次翻倍封顶 60s+小地图纹理 noMip | 记忆文件:webgl2-phase1-port.md 六号坑
- **worker 整体崩毁全房失联**(08-18): 现象:`room.clients.filter is not a function` → worker exit(code=1) 全房掉线 → 根因:并行会话给 roomHost 周期定时器加逻辑时对 Set 用了 .filter;无守卫 setInterval 内一次抛错=worker 整体退出 → 修复:Set 先展开 `[...clients].filter`,四个周期定时器逐房 try/catch 只记日志 | 记忆文件:server-room-simhost-port.md
- **砍树自动收集瞬间崩溃+行走掉帧**(08-18): 现象:砍树掉落自动收集时游戏冻结;长流程 trace 里行走仍掉帧 → 根因:Inventory.add 裸读 `ITEM_DEFS[id].maxStack` 未知 id 即 TypeError 炸断 rAF 链;掉帧是 GC churn——液体渲染四邻 lq() 每帧 new 3.3 万个对象;用 trace 的 ProfileChunk CPU 采样按 timeDeltas 重建时间线找到死点 → 修复:inv.add 守卫+主循环熔断取证;lq() 零分配化 | 记忆文件:treecrack-gc-frameguard-2026-08-18.md
- **金鱼掉落"恐惧之魂"**(08-18): 现象:打死金鱼掉出恐惧之魂,掉落链全体错位 → 根因:vi_5395 屎堆手写条目插在自动注册循环【前】,ITEM_DEFS 内部 id=数组下标,插入点后全部物品 id 平移+1 → 修复:删手写条目改 BLOCK_TILE_BACKFILL 回填;新增 item-id-stability 测试钉死 id 严格递增 | 记忆文件:book-mimic-cultist-dragon-batch.md
- **地底蠕虫音墙**(08-18): 现象:地底蠕虫穿梭音全变成 boss 唤醒咆哮,多蠕虫叠成音墙;洞穴蝙蝠死亡音也"消失" → 根因:WAV_MAP['roar'] 双轨随机,而 PlaySound 第 4 参 Style 缺省是 1 不是 0——蠕虫掘地=Roar_1,boss 吼=显式 style0 的 Roar_0;再叠 case15 缺单实例互斥 → 修复:roar 键改单轨+单实例互斥+怪池 Hit/Death wav 进世界预热(首播懒加载静默) | 记忆文件:npc-ambient-sound-audit.md
- **tooltip 透明感三轮拉锯**(08-18): 现象:气泡"几乎透明"→修后"依然过透明"→铺实底后"过于不透明",三轮报障 → 根因:tint 像素循环把 alpha 通道误乘红通道(`d.data[i]*tmul[3]` 应为 `[i+3]`),深蓝底红通道≈23→alpha≈22 近全透明;0.925 的原版真值从未真正渲染过 → 修复:改正下标回到原版 alpha 236;教训:三轮报障该找根因而不是在 0.925↔1.0 之间找折中 | 记忆文件:item-tooltip-parity-port.md
- **树冠仙人掌接缝**(08-18): 现象:树冠-树干交界细缝无风也有,沙漠仙人掌柱同款,解剖台工具里却没问题;用户自调 zoom 1.27 触发 → 根因:chunk 拼装公式 `256×zoom` 非整数时 chunk 落小数设备像素,各 chunk 独立最近邻采样在边缘产生周期性 1px 透明缝;默认 1.25=320 恰整除从未暴露 → 修复:drawChunkGrid 整数设备矩形+1px 重叠;"工具里没问题"本身即信息→差异枚举法 | 记忆文件:chunk-seam-noninteger-zoom.md
- **迷雾周期性全亮闪**(08-19): 现象:小地图迷雾隔 20 秒突然全亮又瞬间恢复;F4 消雾也失效 → 根因:GPU 看门狗(20s 巡检)误清 CPU 数据——recreateAuxCanvases 无条件 fogPix=null,但迷雾是纯 CPU 缓冲与画布死活无关;整幅重建精确间隔 20s(24.8/43.9/63.9s)实锤 → 修复:fog 缓冲只在 dispose 清;入口 row>=h 复位 | 记忆文件:fog-flicker-f4-latetex-fix.md
- **独眼巨鹿冻在半空**(08-19): 现象:Boss 召唤出来冻在半空不动,AI 计数照常递增、速度满格、坐标恒定 → 根因:deerclopsMovement 只算 vx/vy 从不积分位置(668 是 noGravity+noTileCollide,原版由引擎直移);测试 harness 手动补积分把引擎缺口焊死了——测试绿但游戏坏 → 修复:movement 尾补 `e.x+=e.vx; e.y+=e.vy`;回归测试加位置积分档 | 记忆文件:deerclops-port.md 冻结事故节
- **地图放大到 1.37 即全黑**(08-19): 现象:全屏地图放大到一定程度全黑只剩玩家/NPC 头像,缩小恢复;哨兵日志显示 zoom 1.37 即黑 → 根因:sampler 对象的 MIN_FILTER 是 LINEAR_MIPMAP_LINEAR,而小地图/迷雾纹理 noMip 无 mip 链——用需 mip 的采样器采无 mip 纹理=纹理不完整→采样恒黑 (0,0,0,1);z<1 走 nearest 所以"缩小恢复" → 修复:linearNoMip 采样器按 e.mipped 分流;GL 铁律:sampler 对象与纹理参数是两套,incomplete 判定看生效组合 | 记忆文件:webgl2-phase1-port.md 全黑真凶终定罪节
- **石巨人负血不死**(08-19): 现象:Boss 血条打到负值不死、动画乱闪、boss bar 无头像 → 根因:Enemy.hurt 的放行段 `if(245||246||247||248) return false` 写在 `this.dead=true` 之前——"AI 首行接管"的假设根本没发生;并行会话跨会话契约改动未核调用侧 → 修复:放行收窄到 246 且加本体活门,245 本体死时在 hurt 内直接灭部件 | 记忆文件:golem-3symptom-fix.md
- **普通骷髅王必掉全套 Chippy 时装**(08-18): 现象:对抗性审查发现的刷物品漏洞——普通骷髅王约半数击杀掉全套红帽时装 → 根因:召唤只写 redHat 旗,但掉落五条规则/Renderer/GorePiece 全读 ai3;而 bossAI 又把 ai3 挪用为旋冲方向 → 修复:召唤补 head.ai3=1,旋冲方向改独立字段 skeletronSpinDir | 记忆文件:review-found-bugs-fix.md
- **软渲染模式下每帧新建 60 张画布**(08-19): 现象:--disable-gpu 下 canvas 哨兵报 60 张/秒持续泄漏,暂停中也发生;dev 复现不了 → 根因:GLSpriteLayer 初始化失败时 diedAt=0,退避判据 `now-0>5000` 恒真→每帧 dispose+new(构造器 createElement);dev 的 WebGL2 可用所以复现不了 → 修复:三处失败分支补 diedAt=now+acquireGL 统一 30s 闩 | 记忆文件:dualwindow-iosurface-exhaustion.md ⑫节
- **晴天云全不渲染**(08-18 深夜): 现象:好多云不渲染了,排查发现"该 bug 期间云从未显示过" → 根因:globalCloudAlpha 接了 `max(wr.cloudAlpha, 墓园×0.92)×atmo`——wr.cloudAlpha 是雨云浓度,晴天恒 0→云全透明;墓园压云是把某 CustomSky 内部式误当全局门 → 修复:globalCloudAlpha=atmo 直取(原版 ProcessCloudAlpha 默认恒 1) | 记忆文件:dualwindow-iosurface-exhaustion.md ⑨节
- **[08-18 00:06]** 👤 你看我这个世界的报告,很明显非常诡异吧?这确定是原版代码能干出来的?…画面里三棵树的底部都有异常,一个被蘑菇占用,两个是花,而且还…无法使用镐子破坏他们 [c44574b3]
- **[08-18 09:39]** 👤 # 泰拉瑞亚反编译转译TypeScript:这本质是一场"重写",而非"转换"…不存在成功先例,也没有可用的自动化工具…工作量以多人·年计 [e65c4575]
- **[08-18 12:02]** 👤 我的GPU资源非常充足,为什么总是挤爆 [8405c930]
- **[08-18 15:54]** 👤 离谱的是在你这里面没问题,但是在世界里的就是会有缝,包括沙漠的仙人掌也是有这种问题 [573d63f5]
- **[08-18 16:08]** 🤖 真凶抓到并修复了——你那句"仙人掌也有"是破案关键。根因:chunk 拼装×非整数缩放…默认缩放 1.25:256×1.25=320 恰好整数像素 [573d63f5]
- **[08-18 17:53]** 👤 现在生物的掉落物开始混乱了,打死金鱼居然出现"恐惧之魂"? [04569a63]
- **[08-18 23:39]** 👤 现在仍然有一些动画播的过快的生物动画帧,比如走路的金鱼,非常鬼畜 [d76053b3]
- **[08-19 00:01]** 🤖 全案闭环——两个症状同一个根,外加 20s 看门狗:闪烁,整幅重建精确间隔 20s(24.8→43.9→63.9)=GPU 看门狗周期! [8405c930]
- **[08-19 11:44]** 🤖 这桩"反编译与二进制行为不符"的奇案破了,而且破得很漂亮——根本不存在什么行为差:真凶是金字塔刷墙段每写一堵墙,原版都会经 SquareWallFrame 偷偷掷 1 颗骰(共 11,025 颗) [0650e0c7]
- **坑·备选四条**(超出正文目标条数,均含完整现象→根因→修复):
---sections---
## 一、新增亮点故事(非缺陷,是成就/工程突破)
## 二、新增坑(现象→根因→修复)
## 三、有趣的原始对话片段(archive-stream.json 08-18/08-19)
## 附:同期未入正文的可用彩蛋

```


---

## 🤖 Assistant · 2026-08-19T07:13:13.766Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file is complete:
- 14 stories (section 一)
- 15 pits (section 二) + 4 backup pits in appendix
- 9 dialogue fragments (section 三) + 5 bonus items in appendix

All verified against actual memory files and archive-stream.json content. Now let me write the final report with stats and the 3 most striking stories.
```

</details>


---

## 🤖 Assistant · 2026-08-19T07:13:20.446Z · glm-x-preview-260804

```
已完成。挖掘报告已写入 `/tmp/latest-mining.md`。

## 统计

- **数据源**：65 份 mtime≥08-18 的记忆文件 + archive-stream.json 08-18(418 条)/08-19(96 条)实录，全部条目均核对原始出处，零编造
- **一、亮点故事：14 条**(覆盖任务指定的全部 14 个方向；石巨人并入 Boss 审计条、千人实测从 SimHost 拆出独立成条)
- **二、新增坑：15 条**正文 + 4 条备选入附录(#362CFF 退化块/纹理键碰撞/悬停图标全黑/生命树晚到贴图)
- **三、原始对话片段：9 条**(5 人类 4 模型，含两对“用户一句话点破真相”的经典配合)，另附 5 条彩蛋(用户“磨到100%”执念/总进度95%/行为录制提案等)

## 最震撼的 3 个故事(一句话版)

1. **钻石窗口 IOSurface 八场攻防战**：用户问“我的 GPU 资源非常充足，为什么双开还是爆”——最终在 Chromium 源码注释里钉死答案是“爆的不是字节而是张数”(16×16 的 1KB 小图也分配失败)，随后八回合把游戏从“必崩”打到“GPU 进程零死亡”，chunk 画布 446→28 张、41 个染色变体挤进 1 页。
2. **SimHost 千人实测**：模拟占 CPU 82% 的剖析+三刀优化后，一台 8vCPU/16GB/100Mbps 的服务器就能扛千人在线，带宽账精确算到“国内热点型千人约 8000-9000 元/月”——网页复刻第一次算到了商业部署粒度。
3. **金字塔 11,025 颗暗掷奇案**：一桩“反编译与真二进制行为不符”的悬案，最终破得很漂亮——根本不存在行为差，是原版金字塔每刷一堵墙都偷偷经 SquareWallFrame 掷 1 颗骰，我们镜像了写墙却漏了掷，骰序整体位移引发 10 万格级联，一行 `rng.int(0,2)` 收官。

产出文件:`/tmp/latest-mining.md`
```
