# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T15:59:53.009Z

```
在 ~/Project/GLM/SandboxWorld 仓库中,搜索广度:very thorough。我正在为多人联机容量优化做规划,需要弄清以下细节(我已读过 server/src/room.ts 和 server/src/index.ts,不用重复总结它们):

1. game/src/net/protocol.ts 的完整帧格式:NetWriter 的头部/长度前缀格式、FrameParser、encodeStrip 的编码方式(是否有 RLE/压缩)、writeTileBatch 格式、字符串编码。列出每种帧的大致字节构成。
2. game/src/net/ClientNet.ts 的接收侧:每种下行消息(msg13 PlayerState、msg23 SyncNPC、msg27 SyncProjectile、msg21 SyncItem、msg7 WorldData、msg32 SyncChestItem、条带 SpawnTileData)客户端如何处理?远程玩家的傀儡(netPuppet)是如何创建/插值的?是否有距离剔除?
3. game/src/core/Game.ts 中联机钩子的调度:netNpcBroadcast/netProjBroadcast/netDropSweep 的调用时机(哪个循环、什么 tick 频率)、tile 队列冲洗逻辑(TileStore.netReporter)、单机时如何零开销跳过。
4. 是否存在任何压缩(zlib/per-message deflate)、二进制 vs JSON 的混用情况。
5. game/src/net/LanDiscovery.ts 的机制。
6. WS 连接是否启用了 permessage-deflate(ws 库默认选项在 server/src/index.ts 里如何配置)。

返回:每项的事实清单,带 文件:行号 引用。不要给优化建议,只要事实。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T15:59:53.011Z

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

## 🤖 Assistant · 2026-08-11T15:59:58.355Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a very thorough investigation of the networking code in this repo. Let me start by reading the key files in parallel:

1. game/src/net/protocol.ts
2. game/src/net/ClientNet.ts
3. game/src/core/Game.ts (the net hooks parts)
4. game/src/net/LanDiscovery.ts
5. server/src/index.ts (ws config)

Let me first check the file structure and sizes.
```

</details>


---

## 🤖 Assistant · 2026-08-11T15:59:59.000Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/game/src/net/ ~/Project/GLM/SandboxWorld/server/src/ 2>/dev/null && wc -l ~/Project/GLM/SandboxWorld/game/src/net/*.ts ~/Project/GLM/SandboxWorld/server/src/*.ts ~/Project/GLM/SandboxWorld/game/src/core/Game.ts 2>/dev/null",
 "description": "List net and server source files with line counts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:59.032Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/net/:
total 120
drwxr-xr-x@  6 user  staff    192  8月 11 12:24 .
drwxr-xr-x@ 24 user  staff    768  8月 11 18:12 ..
-rw-r--r--@  1 user  staff  31190  8月 11 12:24 ClientNet.ts
-rw-r--r--@  1 user  staff   1135  8月 11 12:16 entitySyncHooks.ts
-rw-r--r--@  1 user  staff   4501  8月 11 09:48 LanDiscovery.ts
-rw-r--r--@  1 user  staff  15763  8月 11 12:11 protocol.ts

~/Project/GLM/SandboxWorld/server/src/:
total 72
drwxr-xr-x@ 4 user  staff    128  8月 11 12:57 .
drwxr-xr-x@ 8 user  staff    256  8月 10 22:04 ..
-rw-r--r--@ 1 user  staff   9645  8月 11 12:26 index.ts
-rw-r--r--@ 1 user  staff  21864  8月 11 12:57 room.ts
     761 ~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts
      19 ~/Project/GLM/SandboxWorld/game/src/net/entitySyncHooks.ts
     105 ~/Project/GLM/SandboxWorld/game/src/net/LanDiscovery.ts
     339 ~/Project/GLM/SandboxWorld/game/src/net/protocol.ts
     228 ~/Project/GLM/SandboxWorld/server/src/index.ts
     512 ~/Project/GLM/SandboxWorld/server/src/room.ts
    7973 ~/Project/GLM/SandboxWorld/game/src/core/Game.ts
    9937 total

```


---

## 🤖 Assistant · 2026-08-11T15:59:59.684Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"netReporter\\|netNpcBroadcast\\|netProjBroadcast\\|netDropSweep\\|netPuppet\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v \"net/\" | head -80",
 "description": "Find net hook call sites outside net dir"
}
```


---

## 👤 User(sidechain) · 2026-08-11T15:59:59.713Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:399:  private netNpcBroadcast() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:404:      if (e.netPuppet) continue;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:431:  private netProjBroadcast() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:436:      if (p.netPuppet || p.dead) continue;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:458:  private netDropSweep() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:463:      if (d.netPuppet) continue;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:487:        e.netPuppet = true;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:512:        d.netPuppet = true;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:531:        if (!d.netPuppet && d.netId === op.netId) { d.dead = true; break; }
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:543:        p.netPuppet = true;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:571:      if (e.netPuppet || e.id !== localId) continue;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:610:  private netPuppetContact() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1661:      for (const e of this.entities.npcs) if (!e.netPuppet) stepConveyor(e, cst, 1);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1662:      for (const e of this.entities.critters) if (!e.netPuppet) stepConveyor(e, cst, 1);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1663:      for (const e of this.entities.drops) if (!e.netPuppet) stepConveyor(e, cst, 1, true);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1665:        if (!e.netPuppet && conveyorCarriesEnemy(e as Enemy)) stepConveyor(e, cst, 1);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7773:          world.store.netReporter = (op) => net.reportTileOp(op);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7851:        if (this.net.policy.isHost) this.netNpcBroadcast();
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7852:        this.netProjBroadcast();
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7853:        this.netDropSweep();
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7856:      if (!this.net.policy.isHost) this.netPuppetContact();
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:118:    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetTile, x, y, v: type, fx: frameX, fy: frameY });
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:127:    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetHalfBrick, x, y, v: v ? 1 : 0, fx: 0, fy: 0 });
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:136:    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetSlope, x, y, v: s, fx: 0, fy: 0 });
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:155:      if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetWall, x, y, v: wall, fx: 0, fy: 0 });
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:170:    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetWire, x, y, v: bits & 63, fx: 0, fy: 0 });
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:184:    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetActuated, x, y, v: v ? 1 : 0, fx: 0, fy: 0 });
~/Project/GLM/SandboxWorld/game/src/entities/FallingBlock.ts:33:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:113:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:184:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/WeaponProj.ts:251:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts:41:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:341:    if (this.netPuppet) {
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3728:    if (this.netPuppet) entityNet.reportStrike?.(this.netId, rawDmg, kbx, kby);
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3750:      if (this.vanillaId === 16 && !this.netPuppet) {
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3777:      // 自己的 netDropSweep 当作本端掉落二次广播 → 幽灵物品+重复掉落）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:3779:      if (this.vanillaId && !this.netPuppet) {
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts:17:  netPuppet = false;
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts:91:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:149:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts:332:    if (this.netPuppet) { this.x += this.vx; this.y += this.vy; return; }

```


---

## 🤖 Assistant · 2026-08-11T16:00:01.949Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Plan mode is active, but I'm a read-only search agent anyway. Let me read the key files. protocol.ts (339 lines), ClientNet.ts (761 lines), LanDiscovery.ts (105), entitySyncHooks.ts (19), and Game.ts sections. Game.ts is 7973 lines, so I'll read targeted ranges.

Let me read protocol.ts, ClientNet.ts, LanDiscovery.ts fully in parallel, plus Game.ts relevant ranges.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:02.072Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/protocol.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:02.084Z

**📎 ToolResult**

```
1	// 多人联机共享协议层（客户端与 Node 服务器共用，docs/multiplayer-design.md §1-2）。
2	// 帧格式对齐原版：[u16 len][u8 msgId][payload...]，小端，包上限 65535B。
3	// 消息 ID 尽量沿用原版 MessageID 编号（Hello=1/SLOT=3/WorldData=7/TileSection=10/
4	// PlayerSpawn=12/PlayerControls=13/TileManipulation=17/SetTime=18/NetModules=82/Ping=154）；
5	// 编码字段为本仓库 v1 简化集（protoVer 门禁，protoVer=1）。
6	
7	export const PROTO_MAGIC = 'SW1';
8	/** v2：msg13 对齐原版 PlayerControls 布局（控制位+position+velocity）。
9	 *  v3：实体同步族（msg16/21/23/27/42）+ 箱子权威（msg31/32）+ sessionToken 重连 */
10	export const PROTO_VER = 3;
11	
12	/** 消息 ID（v1 实现范围；编号对齐原版 MessageID.cs） */
13	export const enum Msg {
14	  Hello = 1,          // C→S {magic, protoVer, name, hostToken 兜底}
15	  Kick = 2,           // S→C {reason}（原版 Kick/Disconnect 同号）
16	  PlayerSlot = 3,     // S→C {slot, sessionToken}（原版同号 PlayerInfo=3：名字/外观在原版
17	                      //   走此包，我们拆到 Hello+msg4——字段分布简化，ID 保留；
18	                      //   sessionToken 为重连凭据）
19	  SyncPlayer = 4,     // 双向 {slot, appearanceJson}
20	  SyncPlayerItem = 5, // C→S→广播（v2 对齐原版 msg5 SyncPlayerItem 语义，批量变体）：
21	                      //   {u8 count, entries[{u8 playerSlot(服务端覆写), u8 container,
22	                      //    u8 itemSlot, u16 itemId(0=空), u16 stack}]}
23	                      //   container: 0=slots[0..57] 1=armor[0..19] 2=dye[0..9]
24	  RequestWorldData = 6, // C→S {}
25	  WorldData = 7,      // S→C {时间/尺寸/出生点/层线/flags/seed/name}
26	  SpawnTileData = 8,  // C→S {x, y}（客户端请求出生点周围 section）
27	  StatusText = 9,     // S→C {count}（将发的 strip 数，进度条）
28	  TileSection = 10,   // S→C {x0,y0,w,h, rleBytes}（200×20 条带）
29	  PlayerSpawn = 12,   // S→C {slot, x, y}（进房落点确认）
30	  PlayerState = 13,   // C→S→广播（v2 对齐原版 msg13）：{u8 slot, u8 ctrlBits, u8 flagBits,
31	                      //   u8 selectedItem, f32 x, f32 y, [f32 vx, f32 vy 若 flagBits[2]]}
32	                      //   ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction
33	                      //   flagBits: [2]hasVelocity [6]ghost(死亡)。position=碰撞盒左上（原版语义）
34	  PlayerActive = 14,  // S→C 广播 {slot, active, name}
35	  TileBatch = 17,     // C→S→广播 {count, ops[]}（tile 操作批量，对齐 msg17 语义）
36	  SetTime = 18,       // S→C {timeOfDay, dayCount}
37	  // ---- v3 实体同步（房主权威 + 服务器中继；ID 对齐原版 MessageID.cs） ----
38	  PlayerLifeMana = 16, // 双向 {u8 slot, i16 hp, i16 maxHp}（原版同号：客户端权威 HP，服务器中继）
39	  SyncItem = 21,       // 房主→广播 {u32 netId, u8 op(0=spawn/1=take/2=despawn), str key,
40	                       //   u16 stack, f32 x,y,vx,vy}（原版同号 SyncItem）
41	  SyncNPC = 23,        // 房主→广播（批量快照，原版同号 SyncNPC）：
42	                       //   {u16 count, [u32 netId, str key, f32 x,y,vx,vy, i16 hp, i16 maxHp,
43	                       //    u16 animT, u8 flags(bit0=boss)]}
44	  SyncProjectile = 27, // 双向（各自的弹幕互播，原版同号）：
45	                       //   {u16 count, [u32 netId, str key, f32 x,y,vx,vy, f32 rot]}
46	  RequestChestOpen = 31, // C→S {i32 x, i32 y}（箱子锚点；原版同号）
47	  SyncChestItem = 32,  // S→C 下发 / C→S 槽位编辑（原版同号 SyncChestItem）：
48	                       //   {u16 chestIdx, i32 x, i32 y, u16 count, [u8 slot, u16 itemId, u16 stack]}
49	  StrikeNPC = 42,      // 访客→房主 {u32 netId, i16 dmg, u8 crit, u8 kbDir, f32 srcX, srcY}
50	                       //   （原版 42=Unknown42：旧 StrikeNPC 槽位）
51	  NetModules = 82,    // 双向 {moduleId, ...}（module1=聊天 module2=ping）
52	  Ping = 154,         // 简化独立心跳（module2 并存预留）
53	  // ---- v3 房间制扩展（docs/multiplayer-design.md §房间） ----
54	  RoomPolicy = 200,   // S→C {roomCode, roomName, isHost, protectTiles, protectItems}
55	}
56	
57	/** NetModule 表（0-2 对齐原版 NetworkInitializer.cs 注册序：Liquid/Text/Ping；
58	 *  JoinLeave=3 与原版 NetAmbienceModule 撞号——本协议双端自洽，无互操作需求） */
59	export const enum NetModule {
60	  Liquid = 0,   // 预留（v1 液体客户端本地）
61	  Text = 1,     // 聊天 {authorSlot, text, r, g, b}（author=255 无前缀，对齐原版 255=服务器）
62	  PingModule = 2, // 预留
63	  JoinLeave = 3,  // S→C 系统 {slot, joined}——加入/离开公告（原版 Lang.mp[19]/[20]，服务器广播）
64	}
65	
66	// ================= Writer（小端，定宽；字符串 = u16 长度 + UTF-8） =================
67	
68	export class NetWriter {
69	  private buf = new Uint8Array(256);
70	  private len = 0;
71	  private dv: DataView;
72	
73	  constructor(private readonly msgId: number) {
74	    // 预留 [u16 len][u8 msgId]
75	    this.len = 3;
76	    this.dv = new DataView(this.buf.buffer);
77	  }
78	
79	  private grow(need: number) {
80	    if (this.len + need <= this.buf.length) return;
81	    let cap = this.buf.length;
82	    while (cap < this.len + need) cap *= 2;
83	    const nb = new Uint8Array(cap);
84	    nb.set(this.buf.subarray(0, this.len));
85	    this.buf = nb;
86	    this.dv = new DataView(this.buf.buffer);
87	  }
88	
89	  u8(v: number): this { this.grow(1); this.buf[this.len++] = v & 255; return this; }
90	  i8(v: number): this { return this.u8(v < 0 ? v + 256 : v); }
91	  u16(v: number): this { this.grow(2); this.dv.setUint16(this.len, v, true); this.len += 2; return this; }
92	  i16(v: number): this { this.grow(2); this.dv.setInt16(this.len, v, true); this.len += 2; return this; }
93	  u32(v: number): this { this.grow(4); this.dv.setUint32(this.len, v >>> 0, true); this.len += 4; return this; }
94	  i32(v: number): this { this.grow(4); this.dv.setInt32(this.len, v, true); this.len += 4; return this; }
95	  f32(v: number): this { this.grow(4); this.dv.setFloat32(this.len, v, true); this.len += 4; return this; }
96	  f64(v: number): this { this.grow(8); this.dv.setFloat64(this.len, v, true); this.len += 8; return this; }
97	  bool(v: boolean): this { return this.u8(v ? 1 : 0); }
98	  bytes(b: Uint8Array): this { this.grow(b.length); this.buf.set(b, this.len); this.len += b.length; return this; }
99	  str(s: string): this {
100	    const b = new TextEncoder().encode(s);
101	    this.u16(b.length);
102	    return this.bytes(b);
103	  }
104	
105	  /** 回填长度前缀并返回完整帧（含 [u16 len][u8 id]）。finish 后禁止再写入（subarray 视图） */
106	  finish(): Uint8Array {
107	    // Q3 修复：守卫含头总长（此前 len-3 在 65533..65535 区间漏检 → setUint16 回绕 → 接收端脏流）
108	    if (this.len > 65535) throw new Error(`net: 包超限 ${this.len}`);
109	    this.dv.setUint16(0, this.len, true);
110	    this.buf[2] = this.msgId & 255;
111	    return this.buf.subarray(0, this.len);
112	  }
113	}
114	
115	// ================= Reader =================
116	
117	export class NetReader {
118	  private dv: DataView;
119	  private p = 0;
120	  constructor(private readonly buf: Uint8Array) {
121	    this.dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
122	  }
123	  get pos() { return this.p; }
124	  u8(): number { return this.buf[this.p++]; }
125	  i8(): number { const v = this.buf[this.p++]; return v >= 128 ? v - 256 : v; }
126	  u16(): number { const v = this.dv.getUint16(this.p, true); this.p += 2; return v; }
127	  i16(): number { const v = this.dv.getInt16(this.p, true); this.p += 2; return v; }
128	  u32(): number { const v = this.dv.getUint32(this.p, true); this.p += 4; return v; }
129	  i32(): number { const v = this.dv.getInt32(this.p, true); this.p += 4; return v; }
130	  f32(): number { const v = this.dv.getFloat32(this.p, true); this.p += 4; return v; }
131	  f64(): number { const v = this.dv.getFloat64(this.p, true); this.p += 8; return v; }
132	  bool(): boolean { return this.u8() !== 0; }
133	  bytes(n: number): Uint8Array { const b = this.buf.subarray(this.p, this.p + n); this.p += n; return b; }
134	  str(): string {
135	    const n = this.u16();
136	    return new TextDecoder().decode(this.bytes(n));
137	  }
138	}
139	
140	// ================= 帧流解析（粘包；对齐原版 CheckBytes 语义） =================
141	
142	/** 字节流帧解析器：append 后逐帧回调 {msgId, payloadReader}，自动处理半包 */
143	export class FrameParser {
144	  private chunks: Uint8Array[] = [];
145	  private total = 0;
146	
147	  append(data: Uint8Array) {
148	    // 拷贝（ws 回调数据可能被复用）
149	    this.chunks.push(new Uint8Array(data));
150	    this.total += data.length;
151	  }
152	
153	  /** 解析所有完整帧；返回 false 表示缓冲为空。
154	   *  脏流防护：len 非法时按字节重同步（此前 break 不前进 → 永久失步 + 缓冲无限增长）。
155	   *  缓冲上限 256KB：超限重置（半包攻击防御） */
156	  private static readonly MAX_BUFFER = 256 * 1024;
157	  drain(cb: (msgId: number, r: NetReader) => void): boolean {
158	    if (this.total < 3) return this.total > 0;
159	    if (this.total > FrameParser.MAX_BUFFER) { this.chunks = []; this.total = 0; return false; }
160	    // 合并缓冲
161	    let buf = new Uint8Array(this.total);
162	    let off = 0;
163	    for (const c of this.chunks) { buf.set(c, off); off += c.length; }
164	    this.chunks = [];
165	    this.total = 0;
166	    let p = 0;
167	    let any = false;
168	    const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
169	    while (p + 3 <= buf.length) {
170	      const len = dv.getUint16(p, true);
171	      if (len < 3 || len > 65535) { p += 1; continue; } // 脏字节：跳过重同步
172	      if (p + len > buf.length) break; // 半包
173	      const msgId = buf[p + 2];
174	      cb(msgId, new NetReader(buf.subarray(p + 3, p + len)));
175	      p += len;
176	      any = true;
177	    }
178	    if (p < buf.length) { this.chunks.push(buf.subarray(p)); this.total = buf.length - p; }
179	    return any || this.total > 0;
180	  }
181	}
182	
183	// ================= 玩家物品同步（msg5 SyncPlayerItem 批量变体） =================
184	
185	export const enum ItemContainer {
186	  Slots = 0,  // inv.slots[0..57]
187	  Armor = 1,  // inv.armor[0..19]（0-2 盔甲/3-9 配饰/10-12 时装/13-19 时装配饰）
188	  Dye = 2,    // inv.dye[0..9]
189	}
190	
191	export interface ItemSyncEntry {
192	  container: ItemContainer;
193	  itemSlot: number;
194	  itemId: number;   // 0 = 空
195	  stack: number;
196	}
197	
198	export const INV_SYNC_SIZES = [58, 20, 10];
199	
200	export function writePlayerItems(entries: Array<ItemSyncEntry & { playerSlot: number }>): Uint8Array {
201	  const w = new NetWriter(Msg.SyncPlayerItem);
202	  w.u16(entries.length);
203	  for (const e of entries) {
204	    w.u8(e.playerSlot);
205	    w.u8(e.container);
206	    w.u8(e.itemSlot);
207	    w.u16(e.itemId & 0xffff);
208	    w.u16(e.stack & 0xffff);
209	  }
210	  return w.finish();
211	}
212	
213	export function readPlayerItems(r: NetReader): Array<ItemSyncEntry & { playerSlot: number }> {
214	  const n = r.u16();
215	  const out: Array<ItemSyncEntry & { playerSlot: number }> = [];
216	  for (let i = 0; i < n; i++) {
217	    const playerSlot = r.u8();
218	    const container = r.u8() as ItemContainer;
219	    const itemSlot = r.u8();
220	    const itemId = r.u16();
221	    const stack = r.u16();
222	    out.push({ playerSlot, container, itemSlot, itemId, stack });
223	  }
224	  return out;
225	}
226	
227	// ================= tile 操作批量（msg17，对齐原版单点操作语义的批量变体） =================
228	
229	export const enum TileOpAction {
230	  SetTile = 0,    // v=type, fx, fy
231	  SetWall = 1,    // v=wall
232	  SetHalfBrick = 5,
233	  SetSlope = 6,
234	  SetActuated = 3,
235	  SetWire = 4,    // v=bits
236	}
237	
238	export interface TileOp {
239	  a: TileOpAction;
240	  x: number; y: number;
241	  v: number;
242	  fx: number; fy: number;
243	}
244	
245	export function writeTileBatch(ops: TileOp[]): Uint8Array {
246	  const w = new NetWriter(Msg.TileBatch);
247	  w.u16(ops.length);
248	  for (const o of ops) {
249	    w.u8(o.a);
250	    w.i32(o.x); w.i32(o.y);
251	    w.u16(o.v & 0xffff);
252	    if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
253	  }
254	  return w.finish();
255	}
256	
257	export function readTileBatch(r: NetReader): TileOp[] {
258	  const n = r.u16();
259	  const ops: TileOp[] = [];
260	  for (let i = 0; i < n; i++) {
261	    const a = r.u8() as TileOpAction;
262	    const x = r.i32(), y = r.i32(), v = r.u16();
263	    let fx = 0, fy = 0;
264	    if (a === TileOpAction.SetTile) { fx = r.u16(); fy = r.u16(); }
265	    ops.push({ a, x, y, v, fx, fy });
266	  }
267	  return ops;
268	}
269	
270	// ================= tile strip RLE 编解码（msg10，codecVer=0 裸 RLE） =================
271	// 每 tile 完整状态 = type/flags/frameX/frameY/wall/liquid/liquidType/half/slope/wire
272	// 11B 裸；RLE 按"全状态相同"连续段编码 [u16 count][11B 状态]，地下均质区压缩比极高。
273	// 条带默认 200×20（4400 格，最坏 57KB < 64KB 包上限）。
274	
275	export interface StripRect { x0: number; y0: number; w: number; h: number; }
276	
277	/** 编码一条 strip（读 store 指定矩形） */
278	export function encodeStrip(
279	  st: { w: number; h: number; type: Uint16Array; flags: Uint8Array; frameX: Uint16Array; frameY: Uint16Array;
280	        wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; half: Uint8Array; slope: Uint8Array; wire: Uint8Array },
281	  rect: StripRect,
282	): Uint8Array {
283	  const w = new NetWriter(Msg.TileSection);
284	  w.i32(rect.x0); w.i32(rect.y0); w.u16(rect.w); w.u16(rect.h);
285	  const idx = (x: number, y: number) => y * st.w + x;
286	  let run = 0;
287	  let rType = 0, rFlags = 0, rFx = 0, rFy = 0, rWall = 0, rLiq = 0, rLt = 0, rHalf = 0, rSlope = 0, rWire = 0;
288	  const flushRun = () => {
289	    if (run === 0) return;
290	    w.u16(run);
291	    w.u16(rType); w.u8(rFlags); w.u16(rFx); w.u16(rFy); w.u16(rWall);
292	    w.u8(rLiq); w.u8(rLt); w.u8(rHalf); w.u8(rSlope); w.u8(rWire);
293	    run = 0;
294	  };
295	  for (let y = rect.y0; y < rect.y0 + rect.h; y++) {
296	    for (let x = rect.x0; x < rect.x0 + rect.w; x++) {
297	      const i = idx(x, y);
298	      if (run > 0 && (
299	        st.type[i] !== rType || st.flags[i] !== rFlags || st.frameX[i] !== rFx || st.frameY[i] !== rFy
300	        || st.wall[i] !== rWall || st.liquid[i] !== rLiq || st.liquidType[i] !== rLt
301	        || st.half[i] !== rHalf || st.slope[i] !== rSlope || st.wire[i] !== rWire
302	      )) flushRun();
303	      if (run === 0) {
304	        rType = st.type[i]; rFlags = st.flags[i]; rFx = st.frameX[i]; rFy = st.frameY[i];
305	        rWall = st.wall[i]; rLiq = st.liquid[i]; rLt = st.liquidType[i];
306	        rHalf = st.half[i]; rSlope = st.slope[i]; rWire = st.wire[i];
307	      }
308	      run++;
309	    }
310	  }
311	  flushRun();
312	  return w.finish();
313	}
314	
315	/** 解码一条 strip 直写目标 store（批量路径：绕过事件，调用方负责事后整块标脏） */
316	export function decodeStrip(
317	  st: { w: number; h: number; type: Uint16Array; flags: Uint8Array; frameX: Uint16Array; frameY: Uint16Array;
318	        wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; half: Uint8Array; slope: Uint8Array; wire: Uint8Array },
319	  r: NetReader,
320	): StripRect | null {
321	  const x0 = r.i32(), y0 = r.i32(), w = r.u16(), h = r.u16();
322	  if (x0 < 0 || y0 < 0 || x0 + w > st.w || y0 + h > st.h) return null;
323	  let written = 0;
324	  while (written < w * h) {
325	    const count = r.u16();
326	    // C2 防死循环：count=0（恶意/损坏数据）或 payload 已尽（截断）→ 终止并返回已写区域
327	    if (count === 0) break;
328	    const type = r.u16(), flags = r.u8(), fx = r.u16(), fy = r.u16(), wall = r.u16();
329	    const liq = r.u8(), lt = r.u8(), half = r.u8(), slope = r.u8(), wire = r.u8();
330	    for (let k = 0; k < count && written < w * h; k++) {
331	      const x = x0 + (written % w), y = y0 + Math.floor(written / w);
332	      const i = y * st.w + x;
333	      st.type[i] = type; st.flags[i] = flags; st.frameX[i] = fx; st.frameY[i] = fy; st.wall[i] = wall;
334	      st.liquid[i] = liq; st.liquidType[i] = lt; st.half[i] = half; st.slope[i] = slope; st.wire[i] = wire;
335	      written++;
336	    }
337	  }
338	  return { x0, y0, w, h };
339	}
340	

```


---

## 🤖 Assistant · 2026-08-11T16:00:02.207Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts"
}
```


---

## 🤖 Assistant · 2026-08-11T16:00:02.323Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/LanDiscovery.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:02.333Z

**📎 ToolResult**

```
1	// 局域网自动发现（浏览器侧）：无 UDP 原生 API → WebRTC 拿本机 IP + /24 网段 HTTP 扫描。
2	// 原理：
3	//  1) RTCPeerConnection 收集 ICE host candidate——非安全上下文（朋友从 http://192.168.x.x 访问）
4	//     下 candidate 暴露真实 IPv4（secure context 会被 mDNS 混淆成 .local，但那通常是房主
5	//     自己 localhost 访问，本就不需要发现——场景恰好互补）
6	//  2) 对本机所在 /24 网段并发 fetch http://<ip>:7778/lan（服务器 CORS + PNA 头已开），
7	//     响应 magic=1010 即为我们的服务器
8	export interface LanServer {
9	  ip: string;
10	  port: number;
11	  name: string;
12	  online: number;
13	  max: number;
14	  w: number;
15	  h: number;
16	}
17	
18	/** 从 WebRTC ICE host candidate 提取本机局域网 IPv4（192.168/10/172.16-31） */
19	export async function getLocalIpv4(timeoutMs = 1500): Promise<string | null> {
20	  return new Promise((resolve) => {
21	    let done = false;
22	    const finish = (ip: string | null) => {
23	      if (done) return;
24	      done = true;
25	      clearTimeout(timer);
26	      try { pc.close(); } catch { /* 忽略 */ }
27	      resolve(ip);
28	    };
29	    const timer = setTimeout(() => finish(null), timeoutMs);
30	    let pc: RTCPeerConnection;
31	    try {
32	      pc = new RTCPeerConnection({ iceServers: [] });
33	    } catch {
34	      finish(null);
35	      return;
36	    }
37	    // data channel 触发 candidate 收集
38	    pc.createDataChannel('sw-lan');
39	    pc.onicecandidate = (e) => {
40	      if (!e.candidate) { finish(null); return; }
41	      // host candidate: "candidate:... typ host ..."，从中提取 IPv4
42	      const m = e.candidate.candidate.match(/(\d+\.\d+\.\d+\.\d+)/);
43	      if (!m) return;
44	      const ip = m[1];
45	      const a = parseInt(ip.split('.')[0], 10);
46	      const isLan = a === 10 || a === 192 || (a === 172 && parseInt(ip.split('.')[1], 10) >= 16 && parseInt(ip.split('.')[1], 10) <= 31);
47	      if (isLan) finish(ip);
48	    };
49	    void pc.createOffer().then((o) => pc.setLocalDescription(o)).catch(() => finish(null));
50	  });
51	}
52	
53	/** 扫描本机所在 /24 网段的服务器（:7778/lan）。knownIp 可跳过候选（如本机 IP），返回发现列表 */
54	export async function scanLan(localIp: string, excludeIps: string[] = [], port = 7778): Promise<LanServer[]> {
55	  const prefix = localIp.split('.').slice(0, 3).join('.');
56	  const targets: string[] = [];
57	  for (let n = 1; n <= 254; n++) {
58	    const ip = `${prefix}.${n}`;
59	    if (excludeIps.includes(ip)) continue;
60	    targets.push(ip);
61	  }
62	  const found: LanServer[] = [];
63	  const probe = async (ip: string) => {
64	    try {
65	      const ctrl = new AbortController();
66	      const t = setTimeout(() => ctrl.abort(), 400);
67	      const r = await fetch(`http://${ip}:${port}/lan`, { signal: ctrl.signal, mode: 'cors' });
68	      clearTimeout(t);
69	      if (!r.ok) return;
70	      const info = await r.json() as Partial<LanServer> & { magic?: number };
71	      if (info.magic !== 1010) return;
72	      found.push({
73	        ip, port: info.port ?? 7777, name: info.name ?? '联机世界',
74	        online: info.online ?? 0, max: info.max ?? 255, w: info.w ?? 0, h: info.h ?? 0,
75	      });
76	    } catch { /* 无服务器/超时——正常 */ }
77	  };
78	  // 分批并发（32/批）防连接数爆炸
79	  for (let i = 0; i < targets.length; i += 32) {
80	    await Promise.all(targets.slice(i, i + 32).map(probe));
81	  }
82	  return found;
83	}
84	
85	/** 一键发现：自动取本机 IP → 扫描。取不到时依次 fallback：
86	 *  1) 本机服务器的 /lan 端点（房主本机运行着 server → lanIps 即网段线索）
87	 *  2) 手动指定网段前缀（"192.168.1"）
88	 * manualPrefix 手动指定网段（"192.168.1"）时的 fallback */
89	export async function discoverServers(manualPrefix?: string): Promise<{ localIp: string | null; servers: LanServer[] }> {
90	  if (manualPrefix) {
91	    return { localIp: `${manualPrefix}.1`, servers: await scanLan(`${manualPrefix}.1`) };
92	  }
93	  let localIp = await getLocalIpv4();
94	  if (!localIp) {
95	    // secure context（localhost/https）下 WebRTC 被 mDNS 混淆 → 问本机服务器。
96	    // 房主场景本机就跑着 server，lanIps 直接给出可用网段；扫描也能命中自己（供复制 IP）
97	    try {
98	      const r = await fetch('http://127.0.0.1:7778/lan');
99	      const info = await r.json() as { lanIps?: string[] };
100	      localIp = info.lanIps?.[0] ?? null;
101	    } catch { /* 本机无服务器 */ }
102	  }
103	  if (!localIp) return { localIp: null, servers: [] };
104	  return { localIp, servers: await scanLan(localIp) };
105	}
106	

```


---

## 👤 User(sidechain) · 2026-08-11T16:00:02.467Z

**📎 ToolResult**

```
1	// 多人联机客户端（netMode==1，docs/multiplayer-design.md §4）。
2	// 握手 → 世界流式组装 → 玩家互见 + tile 操作上报/应用 + 时间对齐。
3	// v1 未同步（客户端本地）：NPC/弹幕/掉落/箱子/液体模拟结果。
4	import {
5	  PROTO_MAGIC, PROTO_VER, Msg, NetModule,
6	  NetWriter, NetReader, FrameParser, TileOp, TileOpAction, readTileBatch, decodeStrip,
7	  ItemContainer, ItemSyncEntry, INV_SYNC_SIZES, writePlayerItems, readPlayerItems,
8	} from './protocol';
9	import type { World } from '../world/World';
10	import { World as WorldCtor } from '../world/World';
11	import type { TileStore } from '../world/TileStore';
12	import { TILE } from '../core/constants';
13	import { Lang } from '../i18n/Lang';
14	
15	/** 远端玩家状态（对齐原版 msg13 同步集：控制位+位置+速度；Player 实例由 Game 持有池） */
16	export interface RemotePlayerState {
17	  slot: number;
18	  name: string;
19	  appearance: string;
20	  /** 权威位置（碰撞盒左上，原版 player.position 语义）与速度 */
21	  x: number; y: number; vx: number; vy: number;
22	  /** 控制位（原版 msg13 ctrlBits：Game 侧据此跑本地物理模拟） */
23	  up: boolean; down: boolean; left: boolean; right: boolean; jump: boolean; useItem: boolean;
24	  facing: number; selectedItem: number; dead: boolean;
25	  /** 新权威包到达标记（Game 消费注入 netOffset 后清零） */
26	  fresh: boolean;
27	  active: boolean;
28	}
29	
30	/** 房间策略（S→C RoomPolicy；客户端门禁依据——v3 房间制） */
31	export interface RoomPolicyState {
32	  roomCode: string;
33	  roomName: string;
34	  isHost: boolean;
35	  protectTiles: boolean;
36	  protectItems: boolean;
37	}
38	
39	/** NPC 快照（msg23；房主权威） */
40	export interface NpcSnap {
41	  netId: number; key: string;
42	  x: number; y: number; vx: number; vy: number;
43	  hp: number; maxHp: number; animT: number;
44	  flags: number; // bit0=boss
45	}
46	
47	/** 弹幕快照（msg27；tag = projId(arrow/weapon) / dart kind / magic color） */
48	export interface ProjSnap {
49	  netId: number; kind: number; tag: string;
50	  dmg: number; aux: number;
51	  x: number; y: number; vx: number; vy: number;
52	}
53	
54	/** 掉落物操作（msg21） */
55	export interface ItemOpMsg {
56	  op: 0 | 1 | 2; netId: number;
57	  key: string; stack: number;
58	  x: number; y: number; vx: number; vy: number;
59	}
60	
61	export interface ClientNetHooks {
62	  /** 世界组装完成（全部初始 strip 到齐 + PlayerSpawn）——Game 进 loadWorld */
63	  onWorldReady: (world: World) => void;
64	  /** 运行期晚到 strip 的落地区域（Game 负责整块标脏 chunk + 小地图） */
65	  onSectionArrived?: (rect: { x0: number; y0: number; w: number; h: number }) => void;
66	  /** 进度（label, p 0..1） */
67	  onProgress?: (label: string, p: number) => void;
68	  /** 聊天 */
69	  onChat?: (text: string, r: number, g: number, b: number) => void;
70	  /** 被踢 */
71	  onKick?: (reason: string) => void;
72	  /** 箱子内容到达/被纠正（服务器权威；Game 负责登记 world.chests 与开面板） */
73	  onChestSync?: (chestIdx: number, x: number, y: number, items: Array<{ id: number; stack: number } | null>) => void;
74	  /** NPC 快照到达（msg23；Game 维护傀儡池） */
75	  onNpcSnapshot?: (snaps: NpcSnap[]) => void;
76	  /** 掉落物操作到达（msg21；Game 维护傀儡/移除本地真掉落） */
77	  onItemOp?: (op: ItemOpMsg) => void;
78	  /** 弹幕快照到达（msg27；Game 维护傀儡池） */
79	  onProjectileSync?: (snaps: ProjSnap[]) => void;
80	  /** 打击到达（msg42；房主权威结算） */
81	  onStrike?: (netId: number, rawDmg: number, kbx: number, kby: number) => void;
82	  /** 远端玩家 HP（msg16 中继） */
83	  onHp?: (slot: number, hp: number, maxHp: number) => void;
84	  /** 房间策略到达（进场时；门禁/提示用） */
85	  onPolicy?: (policy: RoomPolicyState) => void;
86	}
87	
88	export class ClientNet {
89	  active = false;
90	  mySlot = -1;
91	  players = new Map<number, RemotePlayerState>();
92	  /** 房间策略（RoomPolicy 到达前 = 自由房默认） */
93	  policy: RoomPolicyState = { roomCode: '', roomName: '', isHost: false, protectTiles: false, protectItems: false };
94	
95	  private ws: WebSocket | null = null;
96	  private parser = new FrameParser();
97	  private hooks: ClientNetHooks;
98	  private game: { player: { appearance?: unknown; inv: { slots: Array<{ id: number; stack: number } | null> } } };
99	  private hostToken = '';
100	
101	  /** 组装中的世界（收到 msg7 建骨架，strip 到齐后交给 onWorldReady） */
102	  private pendingWorld: World | null = null;
103	  private pendingStrips = 0;
104	  private pendingStripsTotal = 0;
105	  private worldDelivered = false;
106	  /** 本地 tile 变更上报队列（TileStore.netReporter 收集） */
107	  private tileQueue: TileOp[] = [];
108	  private lastStateSent = 0;
109	  private lastSentPos = { x: 0, y: 0 };
110	
111	  constructor(
112	    game: ClientNet['game'],
113	    hooks: ClientNetHooks,
114	  ) {
115	    this.game = game;
116	    this.hooks = hooks;
117	  }
118	
119	  private pingTimer: ReturnType<typeof setInterval> | null = null;
120	
121	  connect(url: string, hostToken = '') {
122	    this.url = url;
123	    this.hostToken = hostToken;
124	    this.connect0(url);
125	  }
126	
127	  /** 底层建连（首连/重连共用） */
128	  private connect0(url: string) {
129	    this.active = true;
130	    let ws: WebSocket;
131	    try {
132	      ws = new WebSocket(url);
133	    } catch (e) {
134	      // R12 修复：非法 URL 同步抛异常 → 转为 reject 语义（onKick）而非穿透调用栈
135	      this.active = false;
136	      this.hooks.onKick?.(`地址无效：${(e as Error).message}`);
137	      return;
138	    }
139	    ws.binaryType = 'arraybuffer';
140	    this.ws = ws;
141	    // R9：独立 30s 心跳——暂停/后台（fixedUpdate 停跑）也不再被服务器 120s 看门狗踢
142	    if (!this.pingTimer) {
143	      this.pingTimer = setInterval(() => {
144	        this.send(new NetWriter(Msg.Ping).f64(performance.now()).finish());
145	      }, 30000);
146	    }
147	    ws.onopen = () => {
148	      // Hello（对齐原版 msg1：版本校验）。连接时 Game.player 可能尚未创建（joinNetGame
149	      // 先连后 loadWorld）——外观名走可选链兜底
150	      const p = this.game.player as { appearance?: { name?: string } } | undefined | null;
151	      const name = p?.appearance?.name ?? '玩家';
152	      // 房主令牌：URL 已带 ?token=（路由层 newClient 注入）——消息内再传一份兜底
153	      // （非房主/旧路径传空串，服务器 try/catch 读不到即跳过）
154	      const hello = new NetWriter(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(name).str(this.hostToken);
155	      this.send(hello.finish());
156	    };
157	    ws.onmessage = (e) => {
158	      this.parser.append(new Uint8Array(e.data as ArrayBuffer));
159	      this.parser.drain((id, r) => this.handle(id, r));
160	    };
161	    ws.onclose = () => {
162	      if (!this.active || this.userClosed) return;
163	      // v3 断线重连（§8.8）：有 session 凭据 → 2s 间隔自动重试 3 次（同 slot 复位）；
164	      // 耗尽或无凭据 → 按原语义 onKick
165	      if (this.session && this.reconnects < 3) {
166	        this.reconnects++;
167	        this.active = false;
168	        setTimeout(() => {
169	          if (this.userClosed) return;
170	          const sep = this.url.includes('?') ? '&' : '?';
171	          this.connect0(`${this.url}${sep}session=${encodeURIComponent(this.session)}`);
172	        }, 2000);
173	        return;
174	      }
175	      this.active = false;
176	      this.hooks.onKick?.('与服务器断开连接');
177	    };
178	    ws.onerror = () => { /* close 跟上 */ };
179	  }
180	
181	  private url = '';
182	  private session = '';
183	  private reconnects = 0;
184	  private userClosed = false;
185	
186	  private send(frame: Uint8Array) {
187	    if (this.ws?.readyState === WebSocket.OPEN) this.ws.send(frame);
188	  }
189	
190	  /** 请求玩家位置周围的 strip（R3 移动续传：跨条带边界时由 Game 调用） */
191	  requestSection(cx: number, cy: number) {
192	    this.send(new NetWriter(Msg.SpawnTileData).i32(Math.floor(cx)).i32(Math.floor(cy)).finish());
193	  }
194	
195	  disconnect() {
196	    this.userClosed = true;
197	    this.active = false;
198	    if (this.pingTimer) { clearInterval(this.pingTimer); this.pingTimer = null; }
199	    this.ws?.close();
200	    this.ws = null;
201	  }
202	
203	  // ================= 收包分发（对齐原版 MessageBuffer switch） =================
204	
205	  private handle(msgId: number, r: NetReader) {
206	    switch (msgId) {
207	      case Msg.Kick: {
208	        this.hooks.onKick?.(r.str());
209	        this.disconnect();
210	        return;
211	      }
212	      case Msg.PlayerSlot: {
213	        this.mySlot = r.u8();
214	        this.invDumpPending = true; // 物品全量 dump 时机：slot 分配后首 tick
215	        // v3：session 凭据（重连用）；重连场景复位 join 状态以重走世界组装
216	        const sess = (() => { try { return r.str(); } catch { return ''; } })();
217	        if (sess) {
218	          if (this.worldDelivered) {
219	            // 断线重连：世界将重新组装下发（pendingWorld 复位）
220	            this.worldDelivered = false;
221	            this.pendingWorld = null;
222	            this.pendingStrips = 0;
223	          }
224	          this.session = sess;
225	          this.reconnects = 0;
226	        }
227	        // 全量上传自身（对齐原版 msg3 后立刻 SyncPlayer + RequestWorldData）
228	        const p2 = this.game.player as { appearance?: unknown } | undefined | null;
229	        const app = JSON.stringify(p2?.appearance ?? {});
230	        this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(app).finish());
231	        this.send(new NetWriter(Msg.RequestWorldData).finish());
232	        return;
233	      }
234	      case Msg.WorldData: {
235	        this.pendingWorld = this.readWorldData(r);
236	        return;
237	      }
238	      case Msg.StatusText: {
239	        this.pendingStrips = r.u16();
240	        this.pendingStripsTotal = Math.max(1, this.pendingStrips);
241	        // 仅初始组装期上报进度：进世界后 R3 移动续传也会触发 StatusText（fresh=0），
242	        // 无条件回调会把已关闭的全屏进度遮罩重新拉起 → "永久卡在接收世界数据"
243	        if (!this.worldDelivered) this.hooks.onProgress?.('接收世界数据', 0);
244	        return;
245	      }
246	      case Msg.TileSection: {
247	        // R3 修复：初始组装期写入 pendingWorld；运行期（已进世界）晚到的 strip
248	        // 直写 gameWorld 并返回区域（调用方负责整块标脏——见 requestSection 回调）
249	        if (this.pendingWorld) {
250	          decodeStrip(this.pendingWorld.store, r);
251	          if (this.pendingStrips > 0) {
252	            this.pendingStrips--;
253	            // 进度按剩余比例推进（此前恒 0.5 不动）
254	            this.hooks.onProgress?.('接收世界数据', this.pendingStripsTotal > 0 ? 1 - this.pendingStrips / this.pendingStripsTotal : 0.5);
255	          }
256	        } else if (this.gameWorld) {
257	          const rect = decodeStrip(this.gameWorld.store, r);
258	          if (rect && this.hooks.onSectionArrived) this.hooks.onSectionArrived(rect);
259	        }
260	        return;
261	      }
262	      case Msg.PlayerSpawn: {
263	        const slot = r.u8();
264	        const sx = r.i32(), sy = r.i32();
265	        if (slot === this.mySlot && !this.worldDelivered && this.pendingWorld) {
266	          this.worldDelivered = true;
267	          this.pendingWorld.spawnX = sx;
268	          this.pendingWorld.spawnY = sy;
269	          this.hooks.onProgress?.('完成', 1);
270	          this.hooks.onWorldReady(this.pendingWorld);
271	          this.pendingWorld = null;
272	          // R2 修复：进世界后重发外观——连接时 player 可能尚未创建/外观未应用，
273	          // 此刻 Game.player 必然就绪（onWorldReady 已被 loadWorld 消费）
274	          const p3 = this.game.player as { appearance?: unknown } | undefined;
275	          if (p3?.appearance) {
276	            this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p3.appearance)).finish());
277	          }
278	        }
279	        return;
280	      }
281	      case Msg.PlayerActive: {
282	        const slot = r.u8();
283	        const active = r.bool();
284	        const name = r.str();
285	        let p = this.players.get(slot);
286	        if (active) {
287	          if (!p) {
288	            p = {
289	              slot, name, appearance: '{}', x: 0, y: 0, vx: 0, vy: 0,
290	              up: false, down: false, left: false, right: false, jump: false, useItem: false,
291	              facing: 1, selectedItem: 0, dead: false, fresh: false, active: true,
292	            };
293	            this.players.set(slot, p);
294	          }
295	          p.active = true;
296	          p.name = name || p.name;
297	        } else if (p) {
298	          p.active = false;
299	        }
300	        return;
301	      }
302	      case Msg.SyncPlayer: {
303	        const slot = r.u8();
304	        const appearance = r.str();
305	        const p = this.players.get(slot);
306	        if (p) p.appearance = appearance;
307	        return;
308	      }
309	      case Msg.SyncPlayerItem: {
310	        // 远端物品/装备（msg5）：Game 侧拷入 proxy.inv 驱动手持/盔甲/挥舞渲染
311	        const entries = readPlayerItems(r);
312	        this.applyRemoteItems(entries.filter((e) => e.playerSlot !== this.mySlot));
313	        return;
314	      }
315	      case Msg.PlayerState: {
316	        // v2 布局（对齐原版 msg13）：slot + ctrlBits + flagBits + selectedItem + pos [+vel]
317	        const slot = r.u8();
318	        const ctrl = r.u8();
319	        const flag = r.u8();
320	        const sel = r.u8();
321	        const x = r.f32(), y = r.f32();
322	        let vx = 0, vy = 0;
323	        if (flag & 4) { vx = r.f32(); vy = r.f32(); } // flagBits[2] = hasVelocity
324	        let p = this.players.get(slot);
325	        if (!p) {
326	          p = {
327	            slot, name: `玩家${slot}`, appearance: '{}',
328	            x, y, vx: 0, vy: 0,
329	            up: false, down: false, left: false, right: false, jump: false, useItem: false,
330	            facing: ctrl & 64 ? 1 : -1, selectedItem: sel, dead: !!(flag & 64),
331	            fresh: true, active: true,
332	          };
333	          this.players.set(slot, p);
334	        }
335	        p.x = x; p.y = y; p.vx = vx; p.vy = vy;
336	        p.up = !!(ctrl & 1); p.down = !!(ctrl & 2);
337	        p.left = !!(ctrl & 4); p.right = !!(ctrl & 8);
338	        p.jump = !!(ctrl & 16); p.useItem = !!(ctrl & 32);
339	        p.facing = ctrl & 64 ? 1 : -1;   // ctrlBits[6] = direction（原版）
340	        p.selectedItem = sel;
341	        p.dead = !!(flag & 64);           // flagBits[6] = ghost
342	        p.fresh = true;                   // Game 侧注入 netOffset 后清零
343	        return;
344	      }
345	      case Msg.TileBatch: {
346	        // 服务器中继的远端操作：应用 + 回环抑制
347	        const ops = readTileBatch(r);
348	        this.applyRemote(ops);
349	        return;
350	      }
351	      case Msg.SetTime: {
352	        // 时间对齐（服务器权威 clock）
353	        if (this.gameWorld) {
354	          const t = r.f64();
355	          const d = r.u32();
356	          if (Math.abs(this.gameWorld.clock.timeOfDay - t) > 0.005) {
357	            this.gameWorld.clock.timeOfDay = t;
358	          }
359	          this.gameWorld.clock.dayCount = d;
360	        }
361	        return;
362	      }
363	      case Msg.NetModules: {
364	        const moduleId = r.u16();
365	        if (moduleId === NetModule.Text) {
366	          const slot = r.u8();
367	          const text = r.str();
368	          const cr = r.u8(), cg = r.u8(), cb = r.u8();
369	          const name = this.players.get(slot)?.name ?? `玩家${slot}`;
370	          this.hooks.onChat?.(`<${name}> ${text}`, cr, cg, cb);
371	        } else if (moduleId === NetModule.JoinLeave) {
372	          // 加入/离开公告（原版服务器 Lang.mp[19]/[20] 广播，色 (255,240,20)）
373	          const slot = r.u8();
374	          const joined = r.bool();
375	          const name = this.players.get(slot)?.name ?? `玩家${slot}`;
376	          this.hooks.onChat?.(
377	            Lang.text(joined ? 'LegacyMultiplayer.19' : 'LegacyMultiplayer.20', name),
378	            255, 240, 20,
379	          );
380	        }
381	        return;
382	      }
383	      case Msg.RoomPolicy: {
384	        this.policy = {
385	          roomCode: r.str(),
386	          roomName: r.str(),
387	          isHost: r.bool(),
388	          protectTiles: r.bool(),
389	          protectItems: r.bool(),
390	        };
391	        this.hooks.onPolicy?.(this.policy);
392	        return;
393	      }
394	      case Msg.SyncChestItem: {
395	        this.applyRemoteChest(r);
396	        return;
397	      }
398	      case Msg.SyncNPC: {
399	        const n = r.u16();
400	        const snaps: NpcSnap[] = [];
401	        for (let i = 0; i < n; i++) {
402	          snaps.push({
403	            netId: r.u32(), key: r.str(),
404	            x: r.f32(), y: r.f32(), vx: r.f32(), vy: r.f32(),
405	            hp: r.i16(), maxHp: r.i16(),
406	            animT: r.u16(), flags: r.u8(),
407	          });
408	        }
409	        this.hooks.onNpcSnapshot?.(snaps);
410	        return;
411	      }
412	      case Msg.SyncItem: {
413	        const netId = r.u32();
414	        const op = r.u8() as 0 | 1 | 2;
415	        let key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0;
416	        if (op === 0) {
417	          key = r.str(); stack = r.u16();
418	          x = r.f32(); y = r.f32(); vx = r.f32(); vy = r.f32();
419	        }
420	        this.hooks.onItemOp?.({ op, netId, key, stack, x, y, vx, vy });
421	        return;
422	      }
423	      case Msg.SyncProjectile: {
424	        const n = r.u16();
425	        const snaps: ProjSnap[] = [];
426	        for (let i = 0; i < n; i++) {
427	          snaps.push({
428	            netId: r.u32(), kind: r.u8(), tag: r.str(),
429	            dmg: r.i16(), aux: r.i16(),
430	            x: r.f32(), y: r.f32(), vx: r.f32(), vy: r.f32(),
431	          });
432	        }
433	        this.hooks.onProjectileSync?.(snaps);
434	        return;
435	      }
436	      case Msg.StrikeNPC: {
437	        const netId = r.u32();
438	        const dmg = r.i16();
439	        const kbx = r.f32(), kby = r.f32();
440	        this.hooks.onStrike?.(netId, dmg, kbx, kby);
441	        return;
442	      }
443	      case Msg.PlayerLifeMana: {
444	        const slot = r.u8();
445	        const hp = r.i16(), maxHp = r.i16();
446	        if (slot !== this.mySlot) this.hooks.onHp?.(slot, hp, maxHp);
447	        return;
448	      }
449	      case Msg.Ping:
450	        return; // 忽略回显
451	      default:
452	        return; // 未知跳过（对齐原版）
453	    }
454	  }
455	
456	  /** Game 侧设置运行期世界引用（时间对齐用） */
457	  gameWorld: World | null = null;
458	
459	  private readWorldData(r: NetReader): World {
460	    const time = r.f64();
461	    const dayCount = r.u32();
462	    const w = r.u16(), h = r.u16();
463	    const spawnX = r.i32(), spawnY = r.i32();
464	    const groundLevel = r.f32(), rockLevel = r.f32(), lavaLine = r.f32();
465	    const seed = r.i32();
466	    const name = r.str();
467	    const crimson = r.bool();
468	    const dungeonX = r.i32(), dungeonY = r.i32(), jungleX = r.i32();
469	    const flagCount = r.u16();
470	    const flags: Record<string, boolean> = {};
471	    for (let i = 0; i < flagCount; i++) flags[r.str()] = r.bool();
472	    const world = new WorldCtor(w, h, seed, name);
473	    world.clock.timeOfDay = time;
474	    world.clock.dayCount = dayCount;
475	    world.spawnX = spawnX; world.spawnY = spawnY;
476	    world.groundLevel = groundLevel; world.rockLevel = rockLevel; world.lavaLine = lavaLine;
477	    world.crimson = crimson;
478	    world.dungeonX = dungeonX; world.dungeonY = dungeonY; world.jungleX = jungleX;
479	    Object.assign(world.flags, flags);
480	    // 请求出生点周围 section（对齐原版 msg8）
481	    this.send(new NetWriter(Msg.SpawnTileData).i32(spawnX).i32(spawnY).finish());
482	    return world;
483	  }
484	
485	  // ================= tile 上报（TileStore.netReporter → 队列 → 每 tick 冲洗） =================
486	
487	  /** TileStore.netReporter 注入点；netSuppress 期间（应用远端操作）不收集 */
488	  reportTileOp(op: TileOp) {
489	    if (!this.active) return;
490	    if (this.tileQueue.length >= 256) {
491	      // R4：超限不再静默丢（静默分叉不可恢复）——告警后仍丢但留下痕迹
492	      if (!this._overflowWarned) {
493	        this._overflowWarned = true;
494	        console.warn('[net] tile 上报队列溢出（单 tick >256 op），丢弃后续——本地与远端将分叉');
495	      }
496	      return;
497	    }
498	    this.tileQueue.push(op);
499	  }
500	  private _overflowWarned = false;
501	
502	  /** Game 每 fixedUpdate 调用：冲洗 tile 队列 + 玩家状态上报（变化驱动 + 66ms 节流） */
503	  tick() {
504	    if (!this.active) return;
505	    this.syncInventory(performance.now());
506	    this.syncHp();
507	    if (this.tileQueue.length) {
508	      // 每包最多 64 op（防超帧）
509	      const batch = this.tileQueue.splice(0, 64);
510	      const w = new NetWriter(Msg.TileBatch);
511	      w.u16(batch.length);
512	      for (const o of batch) {
513	        w.u8(o.a);
514	        w.i32(o.x); w.i32(o.y);
515	        w.u16(o.v & 0xffff);
516	        if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
517	      }
518	      this.send(w.finish());
519	    }
520	    this.sendPlayerState();
521	  }
522	
523	  private sendPlayerState() {
524	    // v2 布局（对齐原版 msg13）：控制位 + position(碰撞盒左上) + velocity。
525	    // 远端据此跑本地物理 → 有移动过程；位置差由接收端 netOffset 平滑（瞬移消失）
526	    const p = this.game.player as unknown as {
527	      x: number; y: number; vx: number; vy: number; facing: number; dead: boolean;
528	      inputX: number; inputJump: boolean; inputDown: boolean; inputUp: boolean;
529	      inv: { heldItem(): { id: number } | null };
530	    };
531	    const inp = (this.game as { input?: { mouseDown: boolean; rightDown: boolean } }).input;
532	    // ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction（原版 case 13）
533	    // useItem = 左键按住（原版 controlUseItem；放置/右键交互不计）
534	    const ctrl = (p.inputUp ? 1 : 0) | (p.inputDown ? 2 : 0)
535	      | (p.inputX < 0 ? 4 : 0) | (p.inputX > 0 ? 8 : 0)
536	      | (p.inputJump ? 16 : 0)
537	      | (inp?.mouseDown && !inp.rightDown ? 32 : 0)
538	      | (p.facing > 0 ? 64 : 0);
539	    // selectedItem = 快捷栏槽位索引 0-9（原版 NetMessage.cs:471 语义；v1 误发物品 id）
540	    const sel = (p.inv as unknown as { selected: number }).selected & 0xff;
541	    // 控制位变化即时发（原版 TrySyncingInput Player.cs:6484：任一 control/selectedItem
542	    // 变化立刻 SendData(13)）——原地起跳这类"位置未动"的操作不再等静止心跳
543	    const ctrlChanged = ctrl !== this.lastSentCtrl || sel !== this.lastSentSel || p.dead !== this.lastSentDead;
544	    const now = performance.now();
545	    const moved = Math.abs(p.x - this.lastSentPos.x) > 1 || Math.abs(p.y - this.lastSentPos.y) > 1;
546	    if (!ctrlChanged) {
547	      if (!moved && now - this.lastStateSent < 1000) return; // 静止 1s 心跳（原版 %420 全量兜底的加密版）
548	      if (now - this.lastStateSent < 66) return;             // 位置驱动节流 ≥66ms（≈15Hz）
549	    }
550	    this.lastStateSent = now;
551	    this.lastSentPos = { x: p.x, y: p.y };
552	    this.lastSentCtrl = ctrl;
553	    this.lastSentSel = sel;
554	    this.lastSentDead = p.dead;
555	    // flagBits: [2]hasVelocity [6]ghost
556	    const flag = 4 | (p.dead ? 64 : 0);
557	    this.send(new NetWriter(Msg.PlayerState)
558	      .u8(this.mySlot)
559	      .u8(ctrl).u8(flag)
560	      .u8(sel)
561	      .f32(p.x).f32(p.y)
562	      .f32(p.vx).f32(p.vy)
563	      .finish());
564	  }
565	
566	  private lastSentCtrl = -1;
567	  private lastSentSel = -1;
568	  private lastSentDead = false;
569	
570	  // ================= 箱子同步（msg31/32，服务器权威） =================
571	
572	  /** 请求打开箱子（interactAt 未命中本地 chests 时——访客本地无箱数据） */
573	  requestChestOpen(x: number, y: number) {
574	    this.send(new NetWriter(Msg.RequestChestOpen).i32(x).i32(y).finish());
575	  }
576	
577	  /** 槽位编辑上报（每槽一条消息；服务器权威+广播，编辑者本地已乐观生效） */
578	  sendChestSlot(chestIdx: number, x: number, y: number, slot: number, itemId: number, stack: number) {
579	    const w = new NetWriter(Msg.SyncChestItem);
580	    w.u16(chestIdx); w.i32(x); w.i32(y);
581	    w.u16(1);
582	    w.u8(slot); w.u16(itemId); w.u16(stack);
583	    this.send(w.finish());
584	  }
585	
586	  /** 本地登记的箱子 → 同步槽位号（Game 注册；diff 轮询用） */
587	  chestIndexByPos = new Map<string, number>();
588	
589	  private applyRemoteChest(r: NetReader) {
590	    const chestIdx = r.u16();
591	    const x = r.i32(), y = r.i32();
592	    const n = r.u16();
593	    const items: Array<{ id: number; stack: number } | null> = [];
594	    for (let i = 0; i < n; i++) {
595	      const slot = r.u8(), itemId = r.u16(), stack = r.u16();
596	      items[slot] = itemId ? { id: itemId, stack } : null;
597	    }
598	    this.hooks.onChestSync?.(chestIdx, x, y, items);
599	  }
600	
601	  /** 外观变更后重发 SyncPlayer（进游戏后 applyCharacter 调用——初始两发都在外观应用前） */
602	  resendAppearance() {
603	    if (!this.active || this.mySlot < 0) return;
604	    const p = this.game.player as { appearance?: unknown } | undefined;
605	    if (p?.appearance) {
606	      this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p.appearance)).finish());
607	    }
608	  }
609	
610	  // ================= 远端 tile 应用（回环抑制 + 事件链触发） =================
611	
612	  private applyRemote(ops: TileOp[]) {
613	    const st = this.gameWorld?.store;
614	    if (!st) return;
615	    st.netSuppress = true;
616	    try {
617	      for (const o of ops) {
618	        if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
619	        switch (o.a) {
620	          case TileOpAction.SetTile: st.setTile(o.x, o.y, o.v, o.fx, o.fy); break;
621	          case TileOpAction.SetWall: st.setWall(o.x, o.y, o.v); break;
622	          case TileOpAction.SetHalfBrick: st.setHalfBrick(o.x, o.y, !!o.v); break;
623	          case TileOpAction.SetSlope: st.setSlope(o.x, o.y, o.v); break;
624	          case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
625	          case TileOpAction.SetWire: st.setWire(o.x, o.y, o.v); break;
626	        }
627	      }
628	    } finally {
629	      st.netSuppress = false; // R5：异常安全复位（否则 suppress 永久卡死上报）
630	    }
631	  }
632	
633	  /** 聊天发送 */
634	  sendChat(text: string) {
635	    this.send(new NetWriter(Msg.NetModules).u16(NetModule.Text).str(text).finish());
636	  }
637	
638	  // ================= v3 实体同步（msg16/21/23/27/42，房主权威+服务器中继） =================
639	
640	  /** NPC 快照（msg23） */
641	  sendNpcSnapshot(snaps: NpcSnap[]) {
642	    if (!snaps.length) return;
643	    const w = new NetWriter(Msg.SyncNPC);
644	    w.u16(snaps.length);
645	    for (const s of snaps) {
646	      w.u32(s.netId); w.str(s.key);
647	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
648	      w.i16(s.hp); w.i16(s.maxHp);
649	      w.u16(s.animT & 0xffff);
650	      w.u8(s.flags);
651	    }
652	    this.send(w.finish());
653	  }
654	
655	  /** 掉落物操作（msg21）：op 0=spawn / 1=take / 2=despawn */
656	  sendItemOp(op: 0 | 1 | 2, netId: number, key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0) {
657	    const w = new NetWriter(Msg.SyncItem);
658	    w.u32(netId); w.u8(op);
659	    if (op === 0) {
660	      w.str(key); w.u16(stack);
661	      w.f32(x); w.f32(y); w.f32(vx); w.f32(vy);
662	    }
663	    this.send(w.finish());
664	  }
665	
666	  /** 弹幕快照（msg27，双向：各自弹幕互播） */
667	  sendProjectileBatch(snaps: ProjSnap[]) {
668	    if (!snaps.length) return;
669	    const w = new NetWriter(Msg.SyncProjectile);
670	    w.u16(snaps.length);
671	    for (const s of snaps) {
672	      w.u32(s.netId); w.u8(s.kind); w.str(s.tag);
673	      w.i16(s.dmg); w.i16(s.aux);
674	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
675	    }
676	    this.send(w.finish());
677	  }
678	
679	  /** 傀儡受击上报（msg42，访客→房主；Enemy.hurt 内经 entityNet 注入调用） */
680	  sendStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
681	    this.send(new NetWriter(Msg.StrikeNPC).u32(netId).i16(rawDmg).f32(kbx).f32(kby).finish());
682	  }
683	
684	  /** HP 上报（msg16，变化驱动 + 200ms 节流；原版客户端权威） */
685	  private lastHpSent = -1;
686	  private lastHpAt = 0;
687	  syncHp() {
688	    if (this.mySlot < 0) return;
689	    const p = this.game.player as unknown as { hp: number; maxHp: number };
690	    const now = performance.now();
691	    if (p.hp === this.lastHpSent) {
692	      if (now - this.lastHpAt < 5000) return; // 满血心跳 5s
693	    } else if (now - this.lastHpAt < 200) return;
694	    this.lastHpSent = p.hp;
695	    this.lastHpAt = now;
696	    this.send(new NetWriter(Msg.PlayerLifeMana).u8(this.mySlot).i16(p.hp).i16(p.maxHp).finish());
697	  }
698	
699	  // ================= 物品/装备同步（msg5，对齐原版 SyncPlayerItem 语义） =================
700	
701	  /** 远端玩家物品快照（Game 侧拷入 proxy.inv——手持/盔甲纸娃娃/挥舞动画渲染用） */
702	  remoteItems = new Map<number, { inv: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> }>();
703	
704	  /** 本地已同步快照（差分基准；null = 尚未全量 dump） */
705	  private sentInv: Array<Array<{ id: number; stack: number } | null>> | null = null;
706	  private invDumpPending = true; // 进房首包全量
707	  private lastInvSync = 0;
708	
709	  /** 全量 dump（进房后立即 + 外部可请求） */
710	  private sendFullInventory() {
711	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
712	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
713	    for (let c = 0; c < 3; c++) {
714	      const arr = c === 0 ? p.inv.slots : c === 1 ? p.inv.armor : p.inv.dye;
715	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
716	        entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: arr[i]?.id ?? 0, stack: arr[i]?.stack ?? 0 });
717	      }
718	    }
719	    this.send(writePlayerItems(entries));
720	    this.sentInv = [p.inv.slots.map(s => s ? { ...s } : null), p.inv.armor.map(s => s ? { ...s } : null), p.inv.dye.map(s => s ? { ...s } : null)];
721	    this.invDumpPending = false;
722	  }
723	
724	  /** 差分上报（tick 内每 250ms 调一次；原版 msg5 变化驱动逐槽发送的批量等价） */
725	  private syncInventory(now: number) {
726	    if (this.mySlot < 0) return;
727	    if (this.invDumpPending || !this.sentInv) { this.sendFullInventory(); return; }
728	    if (now - this.lastInvSync < 250) return;
729	    this.lastInvSync = now;
730	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
731	    const cur = [p.inv.slots, p.inv.armor, p.inv.dye];
732	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
733	    for (let c = 0; c < 3; c++) {
734	      const arr = cur[c];
735	      const sent = this.sentInv[c];
736	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
737	        const a = arr[i], b = sent[i];
738	        if ((a?.id ?? 0) !== (b?.id ?? 0) || (a?.stack ?? 0) !== (b?.stack ?? 0)) {
739	          entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: a?.id ?? 0, stack: a?.stack ?? 0 });
740	          sent[i] = a ? { ...a } : null;
741	        }
742	      }
743	    }
744	    if (entries.length) this.send(writePlayerItems(entries));
745	  }
746	
747	  private applyRemoteItems(entries: Array<ItemSyncEntry & { playerSlot: number }>) {
748	    for (const e of entries) {
749	      if (e.container > 2 || e.itemSlot >= INV_SYNC_SIZES[e.container]) continue;
750	      let bag = this.remoteItems.get(e.playerSlot);
751	      if (!bag) {
752	        bag = {
753	          inv: Array(58).fill(null), armor: Array(20).fill(null), dye: Array(10).fill(null),
754	        };
755	        this.remoteItems.set(e.playerSlot, bag);
756	      }
757	      const arr = e.container === 0 ? bag.inv : e.container === 1 ? bag.armor : bag.dye;
758	      arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: e.stack } : null;
759	    }
760	  }
761	}
762	

```


---

## 🤖 Assistant · 2026-08-11T16:00:02.468Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/entitySyncHooks.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:02.476Z

**📎 ToolResult**

```
1	// 实体同步注入点（沿用 TileStore.netReporter 注入模式——entities 层不反向依赖 net 层）。
2	// Game 在联机模式下注入；单机恒 null（零开销）。
3	export const entityNet = {
4	  /** 傀儡受击上报（访客→房主 StrikeNPC：原始伤害+击退，房主权威结算） */
5	  reportStrike: null as null | ((netId: number, rawDmg: number, kbx: number, kby: number) => void),
6	  /** 本地实体诞生上报（drop；房主/访客各自的掉落物互播） */
7	  reportSpawn: null as null | ((netId: number, key: string, stack: number, x: number, y: number, vx: number, vy: number) => void),
8	  /** 本地掉落物被拾取上报（take：所有客户端各自的真掉落被捡→广播移除） */
9	  reportTake: null as null | ((netId: number) => void),
10	};
11	
12	/** 实体 netId 合成：高 8 位 = 拥有者 slot（防跨客户端本地 id 撞号），低 24 位 = 本地实体 id */
13	export function makeNetId(ownerSlot: number, localId: number): number {
14	  return ((ownerSlot & 0xff) << 24) | (localId & 0xffffff);
15	}
16	
17	export function netIdLocal(netId: number): number {
18	  return netId & 0xffffff;
19	}
20	

```


---

## 🤖 Assistant · 2026-08-11T16:00:04.120Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read Game.ts sections: lines 380-680 (net hooks), 7740-7900 (scheduling), plus TileStore.ts netReporter parts. Also server/src/index.ts ws config. Let me read those in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:04.318Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 330,
 "offset": 380
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:04.327Z

**📎 ToolResult**

```
380	          wch.last[i] = a ? { ...a } : null;
381	        }
382	      }
383	    }
384	  }
385	
386	  // ================= v3 实体同步（房主权威 NPC + 双向掉落/弹幕；msg16/21/23/27/42） =================
387	  // 模型：房主客户端跑完整模拟（刷怪/AI/掉落，与单人同码），快照经服务器中继；
388	  // 访客渲染傀儡实体（无本地 AI），打击/拾取经上报由房主权威结算。
389	  // netId = 拥有者 slot<<24 | 本地实体 id（entitySyncHooks.makeNetId，防跨端撞号）
390	
391	  private netNpcPuppets = new Map<number, { e: Enemy; seen: number }>();
392	  private netDropPuppets = new Map<number, { d: ItemDrop; seen: number }>();
393	  private netProjPuppets = new Map<number, { p: Entity; seen: number }>();
394	  private netNpcLast = new Map<number, { x: number; y: number; hp: number; t: number }>();
395	  private netProjLast = new Map<number, { x: number; y: number; t: number }>();
396	  private netDropSeen = new Map<number, ItemDrop>();
397	
398	  /** 房主：NPC 快照广播（15Hz，变化驱动 + 2s 兜底；对齐原版 msg23 netUpdate 思想） */
399	  private netNpcBroadcast() {
400	    const net = this.net!;
401	    const snaps: NpcSnap[] = [];
402	    for (const ent of this.entities.enemies) {
403	      const e = ent as Enemy;
404	      if (e.netPuppet) continue;
405	      let last = this.netNpcLast.get(e.id);
406	      if (!last) {
407	        last = { x: e.x, y: e.y, hp: e.hp, t: this.tickCount };
408	        this.netNpcLast.set(e.id, last);
409	      }
410	      const moved = Math.abs(e.x - last.x) > 0.5 || Math.abs(e.y - last.y) > 0.5 || e.hp !== last.hp;
411	      if (!moved && this.tickCount - last.t < 120) continue; // 2s 全量兜底
412	      last.x = e.x; last.y = e.y; last.hp = e.hp; last.t = this.tickCount;
413	      snaps.push({
414	        netId: makeNetId(net.mySlot, e.id), key: e.key,
415	        x: e.x, y: e.y, vx: e.vx, vy: e.vy,
416	        hp: e.hp, maxHp: e.maxHp, animT: e.animT,
417	        flags: e.def.boss ? 1 : 0,
418	      });
419	      if (snaps.length >= 24) break; // 防超帧，余量下轮
420	    }
421	    // 清理已消亡敌人的差分基准
422	    if (snaps.length < 24) {
423	      const alive = new Set<number>();
424	      for (const ent of this.entities.enemies) alive.add((ent as Enemy).id);
425	      for (const id of this.netNpcLast.keys()) if (!alive.has(id)) this.netNpcLast.delete(id);
426	    }
427	    net.sendNpcSnapshot(snaps);
428	  }
429	
430	  /** 双向：本地弹幕快照（15Hz 变化驱动；kind: 0=Arrow 1=WeaponProj族 2=Dart 3=TrapShot 4=MagicProj） */
431	  private netProjBroadcast() {
432	    const net = this.net!;
433	    const snaps: ProjSnap[] = [];
434	    for (const ent of this.entities.projectiles) {
435	      const p = ent as Entity & { projId?: number; damage?: number; kind?: string; color?: string; life?: number };
436	      if (p.netPuppet || p.dead) continue;
437	      let last = this.netProjLast.get(p.id);
438	      if (!last) {
439	        last = { x: p.x, y: p.y, t: this.tickCount };
440	        this.netProjLast.set(p.id, last);
441	      }
442	      if (Math.abs(p.x - last.x) < 1 && Math.abs(p.y - last.y) < 1 && this.tickCount - last.t < 60) continue;
443	      last.x = p.x; last.y = p.y; last.t = this.tickCount;
444	      let kind = -1, tag = '', dmg = Math.max(-32768, Math.min(32767, Math.round(p.damage ?? 0))), aux = 0;
445	      if (p instanceof Arrow) { kind = 0; tag = String(p.projId ?? 1); }
446	      else if (p.projId !== undefined) { kind = 1; tag = String(p.projId); }
447	      else if (p instanceof TrapShot) { kind = 3; tag = p.kind ?? 'dart'; }
448	      else if (p instanceof Dart) { kind = 2; }
449	      else if (p.color !== undefined) { kind = 4; tag = p.color; aux = Math.max(0, Math.min(32767, p.life ?? 600)); }
450	      if (kind < 0) continue; // 未知弹幕类不同步（渲染缺类）
451	      snaps.push({ netId: makeNetId(net.mySlot, p.id), kind, tag, dmg, aux, x: p.x, y: p.y, vx: p.vx, vy: p.vy });
452	      if (snaps.length >= 24) break;
453	    }
454	    net.sendProjectileBatch(snaps);
455	  }
456	
457	  /** 双向：本地真掉落诞生上报 + 消失（拾取/寿命）广播——扫描差分 */
458	  private netDropSweep() {
459	    const net = this.net!;
460	    const cur = new Map<number, ItemDrop>();
461	    for (const ent of this.entities.drops) {
462	      const d = ent as ItemDrop;
463	      if (d.netPuppet) continue;
464	      if (!d.netId) {
465	        d.netId = makeNetId(net.mySlot, d.id);
466	        net.sendItemOp(0, d.netId, ITEM_DEFS[d.itemId]?.key ?? '', d.stack, d.x, d.y, d.vx, d.vy);
467	      }
468	      cur.set(d.netId, d);
469	    }
470	    for (const netId of this.netDropSeen.keys()) {
471	      if (!cur.has(netId)) net.sendItemOp(1, netId); // 上轮在、本轮没 = 拾取/过期 → take
472	    }
473	    this.netDropSeen = cur;
474	  }
475	
476	  /** msg23 回包：NPC 傀儡 upsert（首次创建入桶；boss 置 this.boss 供血条） */
477	  private netApplyNpcSnaps(snaps: NpcSnap[]) {
478	    for (const s of snaps) {
479	      let pup = this.netNpcPuppets.get(s.netId);
480	      if (!pup || pup.e.dead) {
481	        // v_* 键走 fromVanilla（防御/伤害等权威属性——占位 def 会让 hurt 双端分叉）；
482	        // 原生键退普通构造
483	        const vm = s.key.match(/^v_(\d+)$/);
484	        const e = vm ? Enemy.fromVanilla(parseInt(vm[1], 10), s.x, s.y) : new Enemy(s.key, s.x, s.y);
485	        if (!e) return;
486	        e.x = s.x; e.y = s.y; // 快照坐标=左上（Enemy 构造按中心偏移，直接覆写）
487	        e.netPuppet = true;
488	        e.netId = s.netId;
489	        e.hp = s.hp; e.maxHp = s.maxHp;
490	        this.entities.add(e, 'enemies');
491	        if (e.def.boss) this.boss = e;
492	        pup = { e, seen: this.tickCount };
493	        this.netNpcPuppets.set(s.netId, pup);
494	      }
495	      const e = pup.e;
496	      e.x = s.x; e.y = s.y; e.vx = s.vx; e.vy = s.vy;
497	      e.hp = s.hp; e.maxHp = s.maxHp;
498	      e.animT = s.animT;
499	      if (Math.abs(s.vx) > 0.1) e.facing = Math.sign(s.vx);
500	      pup.seen = this.tickCount;
501	    }
502	  }
503	
504	  /** msg21 回包：掉落物傀儡 upsert / take 移除（含拥有者本地真掉落被他人拾取） */
505	  private netApplyItemOp(op: ItemOpMsg) {
506	    if (op.op === 0) {
507	      const id = ITEM_BY_KEY[op.key];
508	      if (id === undefined) return;
509	      let pup = this.netDropPuppets.get(op.netId);
510	      if (!pup) {
511	        const d = new ItemDrop(op.x, op.y, id, Math.max(1, op.stack), op.vx, op.vy);
512	        d.netPuppet = true;
513	        d.netId = op.netId;
514	        this.entities.add(d, 'drops');
515	        pup = { d, seen: this.tickCount };
516	        this.netDropPuppets.set(op.netId, pup);
517	      }
518	      pup.d.x = op.x; pup.d.y = op.y;
519	      pup.d.vx = op.vx; pup.d.vy = op.vy;
520	      pup.seen = this.tickCount;
521	    } else {
522	      const pup = this.netDropPuppets.get(op.netId);
523	      if (pup) {
524	        pup.d.dead = true;
525	        this.netDropPuppets.delete(op.netId);
526	        return;
527	      }
528	      // 拥有者的真掉落被他人拾取（访客 take 上报 → 房主在此移除真身）
529	      for (const ent of this.entities.drops) {
530	        const d = ent as ItemDrop;
531	        if (!d.netPuppet && d.netId === op.netId) { d.dead = true; break; }
532	      }
533	    }
534	  }
535	
536	  /** msg27 回包：弹幕傀儡 upsert（按 kind 重建真类，纯视觉——不跑命中） */
537	  private netApplyProjSnaps(snaps: ProjSnap[]) {
538	    for (const s of snaps) {
539	      let pup = this.netProjPuppets.get(s.netId);
540	      if (!pup || pup.p.dead) {
541	        const p = this.netMakeProj(s);
542	        if (!p) continue;
543	        p.netPuppet = true;
544	        p.netId = s.netId;
545	        this.entities.add(p, 'projectiles');
546	        pup = { p, seen: this.tickCount };
547	        this.netProjPuppets.set(s.netId, pup);
548	      }
549	      pup.p.x = s.x; pup.p.y = s.y;
550	      pup.p.vx = s.vx; pup.p.vy = s.vy;
551	      pup.seen = this.tickCount;
552	    }
553	  }
554	
555	  private netMakeProj(s: ProjSnap): Entity | null {
556	    switch (s.kind) {
557	      case 0: return new Arrow(s.x, s.y, s.vx, s.vy, s.dmg, 0, parseInt(s.tag, 10) || 1);
558	      case 1: return new Boomerang(s.x, s.y, s.vx, s.vy, s.dmg, 0, parseInt(s.tag, 10) || 1); // WeaponProj 族共用 drawProj(projId) 渲染，取代表类重建
559	      case 2: return new Dart(s.x, s.y, s.vx, s.vy, s.dmg);
560	      case 3: return new TrapShot(s.x, s.y, s.vx, s.vy, s.dmg, (s.tag || 'dart') as TrapShotKind);
561	      case 4: return new MagicProj(s.x, s.y, s.vx, s.vy, s.dmg, Math.max(60, s.aux), s.tag || '#8090FF');
562	      default: return null;
563	    }
564	  }
565	
566	  /** msg42 回包（房主）：访客打击权威结算——按 netId 找真身应用 hurt（防御减算在此一次） */
567	  private netApplyStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
568	    const localId = netIdLocal(netId);
569	    for (const ent of this.entities.enemies) {
570	      const e = ent as Enemy;
571	      if (e.netPuppet || e.id !== localId) continue;
572	      e.hurt(rawDmg, kbx, kby, this);
573	      const dealt = Math.max(1, Math.round(rawDmg - (e.def.defense ?? 0) * 0.5));
574	      this.addDamageNumber(e.cx, e.y, dealt, false, '#FF7060');
575	      return;
576	    }
577	  }
578	
579	  /** 傀儡清扫：死亡/超时无快照（掉线房主、宿主清场）→ 移除 */
580	  private netSweepPuppets() {
581	    for (const [id, pup] of this.netNpcPuppets) {
582	      if (pup.e.dead || this.tickCount - pup.seen > 300) {
583	        pup.e.dead = true;
584	        if (this.boss === pup.e) this.boss = null;
585	        this.netNpcPuppets.delete(id);
586	      }
587	    }
588	    for (const [id, pup] of this.netDropPuppets) {
589	      if (pup.d.dead) {
590	        // 傀儡消失两源：本地拾取（dead 由 ItemDrop 置位）→ 上报 take 让房主移除真身；
591	        // 寿命/远端 take → netApplyItemOp 已删映射，不会走到这
592	        this.net?.sendItemOp(1, id);
593	        this.netDropPuppets.delete(id);
594	        continue;
595	      }
596	      if (this.tickCount - pup.seen > 300) {
597	        pup.d.dead = true;
598	        this.netDropPuppets.delete(id);
599	      }
600	    }
601	    for (const [id, pup] of this.netProjPuppets) {
602	      if (pup.p.dead || this.tickCount - pup.seen > 180) {
603	        pup.p.dead = true;
604	        this.netProjPuppets.delete(id);
605	      }
606	    }
607	  }
608	
609	  /** 访客：傀儡 NPC 接触伤害（房主 AI 只对房主结算；访客本地判 AABB，HP 客户端权威+msg16 中继） */
610	  private netPuppetContact() {
611	    const p = this.player;
612	    if (p.dead) return;
613	    for (const [, pup] of this.netNpcPuppets) {
614	      const e = pup.e;
615	      if (e.dead || e.iframes > 0) continue;
616	      const dmg = e.def.damage ?? 0;
617	      if (dmg <= 0 || !e.aabbOverlaps(p)) continue;
618	      this.damagePlayer(dmg, e.cx, e.cy, e);
619	      e.iframes = 8;
620	    }
621	  }
622	  /** 远端玩家渲染代理（net.players → drawPlayer 可用形状，net 激活时每帧同步） */
623	  private remotePlayerProxies: import('../entities/Player').Player[] = [];
624	  /** tile key → id 反查表（调试句柄/wld 导入映射用） */
625	  tileByKey = TILE_BY_KEY;
626	
627	  /** 开发者模式：全部道具入包（溢出的落在展示区上方）+ 出生点右侧摆放所有可放置图块供检验 */
628	  setupDevMode() {
629	    const p = this.player;
630	    const st = this.world.store;
631	    // ---- 1) 全道具入包 ----
632	    const overflow: Array<[string, number]> = [];
633	    for (const def of ITEM_DEFS) {
634	      const n = def.maxStack === 1 ? 1 : Math.min(def.maxStack, 99);
635	      const left = p.inv.add(ITEM_BY_KEY[def.key], n);
636	      if (left > 0) overflow.push([def.key, left]);
637	    }
638	    // ---- 2) 展示区：出生点右侧清空并逐行摆放全部可放置图块 ----
639	    const sx = this.world.spawnX, sy = this.world.spawnY;
640	    const x0 = sx + 6, x1 = sx + 70, yBot = sy - 2, yTop = sy - 40;
641	    for (let x = x0; x <= x1; x++) {
642	      for (let y = yTop; y <= yBot; y++) {
643	        st.setTile(x, y, 0);
644	        st.setLiquid(x, y, 0, 0);
645	      }
646	      st.setTile(x, yBot, T.STONE);
647	      st.setTile(x, yBot + 1, T.STONE);
648	    }
649	    // 收集可放置 tile（有物品指向，去重）
650	    const placeable: number[] = [];
651	    const seen = new Set<number>();
652	    for (const def of ITEM_DEFS) {
653	      if (!def.tile) continue;
654	      const tid = TILE_BY_KEY[def.tile];
655	      if (tid === undefined || tid === 0 || seen.has(tid)) continue;
656	      seen.add(tid);
657	      placeable.push(tid);
658	    }
659	    // 逐行摆放：行高 7（最高家具 5 格 + 间隙），每行放满换行并铺新地板
660	    let cx = x0 + 1, cy = yBot - 1;
661	    const rowH = 7;
662	    for (const tid of placeable) {
663	      const td = TILE_DEFS[tid];
664	      const w = td.vanilla?.fw ?? td.w ?? 1;
665	      const h = td.vanilla?.fh ?? td.h ?? 1;
666	      if (cx + w > x1 - 1) {
667	        cx = x0 + 1;
668	        cy -= rowH;
669	        for (let x = x0; x <= x1; x++) st.setTile(x, cy, T.STONE);
670	      }
671	      for (let dx = 0; dx < w; dx++) {
672	        for (let dy = 0; dy < h; dy++) {
673	          // 原版帧语义（TileObject.Place）：顶行 frameY=0，底行最大——
674	          // 此处 cy 是底部行，dy=0 是底行 → frameY = (h-1-dy)*18
675	          st.setTile(cx + dx, cy - dy, tid, td.vanilla ? dx * 18 : dx, td.vanilla ? (h - 1 - dy) * 18 : dy);
676	        }
677	      }
678	      cx += w + 1;
679	    }
680	    // ---- 3) 溢出道具以掉落物排在展示区上方（背包 40 格装不下的部分） ----
681	    let dxDrop = x0;
682	    let dyDrop = yTop + 3;
683	    for (const [key, n] of overflow) {
684	      this.spawnDrop(dxDrop * TILE + 8, dyDrop * TILE, key, n, 0, 0);
685	      dxDrop += 2;
686	      if (dxDrop > x1 - 1) { dxDrop = x0; dyDrop += 3; }
687	    }
688	    this.cb.onInventoryChanged();
689	    this.cb.onToast(`开发者模式：${overflow.length} 种道具背包装不下，已排在展示区上方；全部可放置图块在出生点右侧`);
690	  }
691	
692	  // NPC 系统
693	  private housingCheckTimer = 0;
694	  guideSpawned = false;
695	  private lastWasDay: boolean | null = null;
696	  /** 环境采样结果（SceneMetrics；BGM/群系背景共用），每 15 tick 刷新 */
697	  scene: SceneFlags = { ...EMPTY_SCENE };
698	  private musicState: MusicState = newMusicState();
699	  /** 派对态（BirthdayParty 精简核：ManualParty；派对纪念碑 455 驱动） */
700	  private partyState: PartyState = newPartyState();
701	  private lastMusic = -1;
702	  private _mapClickLatch = false;
703	  private _mapClickLatch2 = false;
704	  /** 地图内按压起点（松开时与当前位置比对 <6px 判定为点击，否则是拖动） */
705	  private _mapPressX = 0;
706	  private _mapPressY = 0;
707	  private _tpTarget: { x: number; y: number } | null = null;
708	  // 方块标注模式（F5）：点击标记问题方块，导出标注+地图给开发者定位
709	  annotateMode = false;

```


---

## 🤖 Assistant · 2026-08-11T16:00:04.523Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 160,
 "offset": 7740
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:04.542Z

**📎 ToolResult**

```
7740	        if (w.invasionType <= 0 || w.invasionSizeStart <= 0) return null;
7741	        const nameKey = w.invasionType === INVASION_PIRATE ? 86 : w.invasionType === INVASION_SNOW_LEGION ? 87 : 88;
7742	        for (const e of this.entities.enemies) {
7743	          const en = e as unknown as { x: number; y: number; vanillaId?: number | null };
7744	          if (en.vanillaId != null && INVASION_GROUP[en.vanillaId] === w.invasionType
7745	            && Math.abs(en.x - this.player.cx) < 5000 && Math.abs(en.y - this.player.cy) < 5000) {
7746	            return { name: Lang.inter(nameKey), pct: (w.invasionSizeStart - w.invasionSize) / w.invasionSizeStart };
7747	          }
7748	        }
7749	        return null;
7750	      })(),
7751	    );
7752	  }
7753	
7754	  /** 加入联机服务器（mainFlow 的加入流程调用；world 就绪回调内进 loadWorld）。
7755	   *  v3 房间制：url = ws://host:port/<房间码>[?token=<房主令牌>]，hostToken 传入时
7756	   *  Hello 内兜底再传一份（路由层已从 URL 注入） */
7757	  joinNetGame(url: string, onProgress?: (label: string, p: number) => void, hostToken = ''): Promise<void> {
7758	    return new Promise((resolve, reject) => {
7759	      let settled = false;
7760	      const fail = (reason: string) => {
7761	        if (settled) return;
7762	        settled = true;
7763	        net.disconnect();
7764	        if (this.net === net) this.net = null;
7765	        reject(new Error(reason));
7766	      };
7767	      const net = new ClientNet(this, {
7768	        onProgress: (label, p) => onProgress?.(label, p),
7769	        onWorldReady: (world) => {
7770	          this.net = net;
7771	          net.gameWorld = world;
7772	          // 进世界（settled：世界已在服务器沉降过；tileReporter 注入上报链）
7773	          world.store.netReporter = (op) => net.reportTileOp(op);
7774	          // 实体同步钩子（Enemy.hurt 傀儡分支 → StrikeNPC 上报）
7775	          entityNet.reportStrike = (netId, rawDmg, kbx, kby) => net.sendStrike(netId, rawDmg, kbx, kby);
7776	          this.loadWorld(world, (label, p) => onProgress?.(label, p), { settled: true }).then(() => {
7777	            if (settled) return;
7778	            settled = true;
7779	            resolve();
7780	          }, (e) => fail(`世界加载失败：${(e as Error).message}`));
7781	        },
7782	        onSectionArrived: (rect) => {
7783	          // R3：晚到 strip 标脏（chunk 重烘焙 + 光照；200×20 逐格 mark 低频可接受）
7784	          const st = this.world.store;
7785	          for (let y = rect.y0; y < rect.y0 + rect.h; y += 4) {
7786	            for (let x = rect.x0; x < rect.x0 + rect.w; x += 4) {
7787	              if (st.inBounds(x, y)) this.chunks.markDirtyAround(x, y);
7788	            }
7789	          }
7790	          this.lighting.dirty = true;
7791	        },
7792	        onChat: (text, r, g, b) => this.newText(text, r, g, b),
7793	        onKick: (reason) => {
7794	          this.cb.onToast?.(reason);
7795	          fail(reason);
7796	        },
7797	        onPolicy: (policy) => {
7798	          // 保护房提示：非房主告知受控范围（房主静默）
7799	          if (!policy.isHost && (policy.protectTiles || policy.protectItems)) {
7800	            const parts: string[] = [];
7801	            if (policy.protectTiles) parts.push(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles'));
7802	            if (policy.protectItems) parts.push(Lang.text('Mods.SandboxWorld.Toast.RoomProtectItems'));
7803	            this.cb.onToast?.(parts.join('；'));
7804	          }
7805	        },
7806	        onChestSync: (chestIdx, x, y, items) => this.netApplyChest(chestIdx, x, y, items),
7807	        onNpcSnapshot: (snaps) => this.netApplyNpcSnaps(snaps),
7808	        onItemOp: (op) => this.netApplyItemOp(op),
7809	        onProjectileSync: (snaps) => this.netApplyProjSnaps(snaps),
7810	        onStrike: (netId, dmg, kbx, kby) => this.netApplyStrike(netId, dmg, kbx, kby),
7811	        onHp: (slot, hp, maxHp) => {
7812	          const rp = net.players.get(slot);
7813	          if (rp) { (rp as unknown as { hp?: number }).hp = hp; (rp as unknown as { maxHp?: number }).maxHp = maxHp; }
7814	        },
7815	      });
7816	      net.connect(url, hostToken);
7817	      // R10：30s 握手超时（计时器在 settle 后清除，不再空跑）
7818	      const timer = setTimeout(() => {
7819	        if (!settled && !net.gameWorld) fail('连接超时');
7820	      }, 30000);
7821	      void timer;
7822	    });
7823	  }
7824	
7825	  private lastStripReq = '';
7826	
7827	  /** 每逻辑帧后处理挥舞命中（在 fixedUpdate 实体更新后调用） */
7828	  postUpdate() {
7829	    // 联机 pump：tile 上报冲洗 + 玩家状态节流发送（docs §4.2）
7830	    if (this.net?.active) {
7831	      this.net.tick();
7832	      // R3 移动续传：跨条带（200×20）边界时向服务器请求周围 strip
7833	      if (this.tickCount % 30 === 0 && this.net.gameWorld) {
7834	        const sx = Math.floor(this.player.cx / 16 / 200);
7835	        const sy = Math.floor(this.player.cy / 16 / 20);
7836	        const key = sx + ',' + sy;
7837	        if (key !== this.lastStripReq) {
7838	          this.lastStripReq = key;
7839	          this.net.requestSection(this.player.cx, this.player.cy);
7840	        }
7841	      }
7842	    }
7843	    this.updateSwingHits();
7844	    // 远端玩家模拟（每逻辑 tick：控制位驱动物理 + netOffset 平滑，对齐原版远端玩家）
7845	    if (this.net?.active) this.simulateRemotePlayers();
7846	    // 箱子槽位差分上报（15 tick 轮询；UI/快捷堆叠等所有变更源统一捕获）
7847	    if (this.net?.active && this.tickCount % 15 === 0) this.netChestPoll();
7848	    // v3 实体同步：房主 NPC 快照 + 双向弹幕/掉落 + 傀儡清扫/接触伤害
7849	    if (this.net?.active) {
7850	      if (this.tickCount % 4 === 0) {
7851	        if (this.net.policy.isHost) this.netNpcBroadcast();
7852	        this.netProjBroadcast();
7853	        this.netDropSweep();
7854	      }
7855	      if (this.tickCount % 30 === 0) this.netSweepPuppets();
7856	      if (!this.net.policy.isHost) this.netPuppetContact();
7857	    }
7858	  }
7859	
7860	  /**
7861	   * 联机远端玩家模拟（对齐原版 MessageBuffer.cs case 13 + Player.UpdateNetOffset）：
7862	   * 远端玩家在本端用同步的控制位+速度跑移动物理（有移动过程、动画帧由速度派生）；
7863	   * 每个权威包的位置差注入 netOffset，渲染时叠加并逐 tick 收敛（<2px 归零，
7864	   * 每步 max(2, len×0.1)；超 300px=Main.multiplayerNPCSmoothingRange 直接归零）。
7865	   * 物理只取移动子集——环境伤害/液体细判等权威在各自客户端，避免双端分叉。
7866	   */
7867	  private simulateRemotePlayers() {
7868	    const net = this.net!;
7869	    const list: Player[] = [];
7870	    for (const [slot, rp] of net.players) {
7871	      if (!rp.active || slot === net.mySlot) continue;
7872	      let proxy = this.remotePlayerProxies.find((p) => (p as unknown as { __netSlot?: number }).__netSlot === slot);
7873	      if (!proxy) {
7874	        proxy = new Player(rp.x, rp.y, new Inventory()); // R11：独立空背包——不共享本地 inv
7875	        (proxy as unknown as { __netSlot?: number }).__netSlot = slot;
7876	      }
7877	      // 新权威包（原版 case 13：netOffset += 模拟位置 - 权威位置；超限归零；硬设权威 pos/vel）
7878	      if (rp.fresh) {
7879	        rp.fresh = false;
7880	        proxy.netOffX += proxy.x - rp.x;
7881	        proxy.netOffY += proxy.y - rp.y;
7882	        if (Math.hypot(proxy.netOffX, proxy.netOffY) > 300) { proxy.netOffX = 0; proxy.netOffY = 0; }
7883	        proxy.x = rp.x; proxy.y = rp.y;
7884	        proxy.vx = rp.vx; proxy.vy = rp.vy;
7885	      }
7886	      // 控制位 → 输入（原版：远端玩家以同步的 control* 跑 Player.Update）
7887	      proxy.inputX = (rp.left ? -1 : 0) + (rp.right ? 1 : 0);
7888	      proxy.inputJump = rp.jump;
7889	      proxy.inputDown = rp.down;
7890	      proxy.inputUp = rp.up;
7891	      proxy.facing = rp.facing;
7892	      proxy.dead = rp.dead;
7893	      // R11'.外观合并：仅接受含 hair 的完整对象（空对象会令纸娃娃读 X.r 崩溃）
7894	      try {
7895	        const parsed = JSON.parse(rp.appearance) as Record<string, unknown>;
7896	        if (parsed && typeof parsed.hair === 'number') proxy.appearance = parsed as never;
7897	      } catch { /* 保持默认外观 */ }
7898	      // 物品/装备（msg5）：拷入代理背包——手持物 holdStyle/挥舞动画/盔甲纸娃娃渲染依赖。
7899	      // 数组直接共享（代理只读不写，远端真权威在各自客户端）

```


---

## 🤖 Assistant · 2026-08-11T16:00:04.635Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/index.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:04.651Z

**📎 ToolResult**

```
1	// SandboxWorld 中央服务器（Node+TS）：lobby（HTTP 房间管理）+ WS 按房间码路由到 Room 会话。
2	// docs/multiplayer-design.md §房间制：房主上传存档建房 → 6 位房间码 → 房间列表/码加入。
3	// 破坏保护服务端权威拒绝（Room.handleTileBatch 前置检查）；物品保护策略下发客户端门禁。
4	import { WebSocketServer, WebSocket } from 'ws';
5	import http from 'node:http';
6	import * as node_os from 'node:os';
7	import { randomUUID } from 'node:crypto';
8	import { loadSaveData } from '../../game/src/save/SaveFile.ts';
9	import { NetWriter } from '../../game/src/net/protocol.ts';
10	import { Room } from './room.ts';
11	
12	function arg(name: string, def?: string): string | undefined {
13	  const i = process.argv.indexOf(`--${name}`);
14	  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
15	}
16	const PORT = parseInt(arg('port', '7777')!, 10);
17	const MAX_ROOMS = parseInt(arg('max-rooms', '32')!, 10);
18	const WORLD_UPLOAD_LIMIT = 256 << 20; // 单存档上传上限 256MB
19	
20	// ================= 房间注册表 =================
21	
22	interface RoomEntry { room: Room; createdAt: number; }
23	
24	const rooms = new Map<string, RoomEntry>(); // code → room
25	
26	function newCode(): string {
27	  for (;;) {
28	    const code = String(Math.floor(Math.random() * 900000) + 100000); // 6 位数字
29	    if (!rooms.has(code)) return code;
30	  }
31	}
32	
33	/** 空房回收（创建满 1 分钟且一直无人满 5 分钟 → 关闭回收） */
34	setInterval(() => {
35	  const now = Date.now();
36	  for (const [code, entry] of rooms) {
37	    const idle = now - entry.createdAt;
38	    if (entry.room.closed || (entry.room.onlineCount === 0 && idle > 60_000 && idle > 5 * 60_000)) {
39	      entry.room.closed = true;
40	      rooms.delete(code);
41	      console.log(`[room] 回收空房 ${code}`);
42	    }
43	  }
44	}, 60_000);
45	
46	function worldFromSaveJson(json: string) {
47	  return loadSaveData(JSON.parse(json)).world;
48	}
49	
50	/** 本机全部局域网 IPv4（多网卡全列出——UI 分享用） */
51	function lanIps(): string[] {
52	  const out: string[] = [];
53	  for (const list of Object.values(node_os.networkInterfaces())) {
54	    for (const ni of list ?? []) {
55	      if (ni.family === 'IPv4' && !ni.internal) out.push(ni.address);
56	    }
57	  }
58	  return out;
59	}
60	
61	// ================= HTTP Lobby =================
62	
63	const CORS = {
64	  'Access-Control-Allow-Origin': '*',
65	  'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
66	  'Access-Control-Allow-Headers': 'Content-Type',
67	  'Access-Control-Allow-Private-Network': 'true',
68	};
69	
70	function readBody(req: http.IncomingMessage, limit: number): Promise<Buffer> {
71	  return new Promise((resolveBody, reject) => {
72	    const chunks: Buffer[] = [];
73	    let size = 0;
74	    req.on('data', (d: Buffer) => {
75	      size += d.length;
76	      if (size > limit) { reject(new Error('上传超限')); req.destroy(); return; }
77	      chunks.push(d);
78	    });
79	    req.on('end', () => resolveBody(Buffer.concat(chunks)));
80	    req.on('error', reject);
81	  });
82	}
83	
84	const lobby = http.createServer(async (req, res) => {
85	  const url = new URL(req.url ?? '/', `http://127.0.0.1:${PORT}`);
86	  const finish = (code: number, data: unknown) => {
87	    res.writeHead(code, { 'Content-Type': 'application/json', ...CORS });
88	    res.end(JSON.stringify(data));
89	  };
90	  if (req.method === 'OPTIONS') { finish(204, {}); return; }
91	
92	  try {
93	    // GET /rooms → 公开房间列表（非公开不展示，只能码进）
94	    if (req.method === 'GET' && url.pathname === '/rooms') {
95	      const list = [...rooms.values()]
96	        .filter((e) => e.room.opts.publicRoom && !e.room.closed)
97	        .map((e) => ({
98	          code: e.room.opts.code, name: e.room.opts.name,
99	          online: e.room.onlineCount, w: e.room.world.w, h: e.room.world.h,
100	          protectTiles: e.room.opts.protectTiles, protectItems: e.room.opts.protectItems,
101	        }));
102	      finish(200, { ok: true, rooms: list });
103	      return;
104	    }
105	    const m = url.pathname.match(/^\/rooms\/(\d{6})$/);
106	    // GET /rooms/<code> → 房间码校验（加入前置检查，非公开房也允许码查）
107	    if (req.method === 'GET' && m) {
108	      const entry = rooms.get(m[1]);
109	      if (!entry || entry.room.closed) { finish(404, { ok: false, error: '房间不存在' }); return; }
110	      finish(200, {
111	        ok: true, code: entry.room.opts.code, name: entry.room.opts.name,
112	        online: entry.room.onlineCount,
113	        protectTiles: entry.room.opts.protectTiles, protectItems: entry.room.opts.protectItems,
114	        // 首箱锚点（调试/探针确定性用；LAN 游戏服务器无敏感性）
115	        chest: entry.room.world.chests[0] ? { x: entry.room.world.chests[0].x, y: entry.room.world.chests[0].y } : null,
116	      });
117	      return;
118	    }
119	    // POST /rooms → 创建房间（body: {name, public, protectTiles, protectItems, save}）
120	    if (req.method === 'POST' && url.pathname === '/rooms') {
121	      if (rooms.size >= MAX_ROOMS) { finish(503, { ok: false, error: '服务器房间已满' }); return; }
122	      const body = JSON.parse((await readBody(req, WORLD_UPLOAD_LIMIT)).toString('utf8')) as {
123	        name?: string; public?: boolean; protectTiles?: boolean; protectItems?: boolean; save?: string;
124	      };
125	      if (!body.save) { finish(400, { ok: false, error: '缺少 save（世界存档 JSON）' }); return; }
126	      const world = worldFromSaveJson(body.save);
127	      const room = new Room(world);
128	      room.opts.code = newCode();
129	      if (body.name) world.name = body.name, room.opts.name = body.name;
130	      room.opts.publicRoom = !!body.public;
131	      room.opts.protectTiles = !!body.protectTiles;
132	      room.opts.protectItems = !!body.protectItems;
133	      room.opts.hostToken = randomUUID();
134	      rooms.set(room.opts.code, { room, createdAt: Date.now() });
135	      console.log(`[room] 创建 ${room.opts.code}（${world.name} ${world.w}×${world.h} 公开=${room.opts.publicRoom} 破坏保护=${room.opts.protectTiles} 物品保护=${room.opts.protectItems}）`);
136	      finish(200, {
137	        ok: true, code: room.opts.code, hostToken: room.opts.hostToken,
138	        name: room.opts.name, protectTiles: room.opts.protectTiles, protectItems: room.opts.protectItems,
139	      });
140	      return;
141	    }
142	    // DELETE /rooms/<code>?token= → 房主关房
143	    if (req.method === 'DELETE' && m) {
144	      const entry = rooms.get(m[1]);
145	      if (!entry) { finish(404, { ok: false, error: '房间不存在' }); return; }
146	      if (url.searchParams.get('token') !== entry.room.opts.hostToken) {
147	        finish(403, { ok: false, error: '仅房主可关房' }); return;
148	      }
149	      entry.room.closed = true;
150	      rooms.delete(m[1]);
151	      finish(200, { ok: true });
152	      return;
153	    }
154	    // GET /lan → 本机信息（IP 分享 + 发现端点）
155	    if (req.method === 'GET' && url.pathname === '/lan') {
156	      finish(200, { ok: true, magic: 1010, port: PORT, rooms: rooms.size, lanIps: lanIps() });
157	      return;
158	    }
159	    finish(404, { ok: false, error: 'not found' });
160	  } catch (e) {
161	    finish(400, { ok: false, error: (e as Error).message });
162	  }
163	});
164	lobby.listen(PORT + 1);
165	
166	// ================= WebSocket（URL = /<房间码>?token=<房主令牌可选>） =================
167	
168	const wss = new WebSocketServer({ port: PORT, maxPayload: 1 << 20 });
169	
170	wss.on('connection', (ws: WebSocket, req) => {
171	  ws.binaryType = 'nodebuffer';
172	  const m = (req.url ?? '').match(/^\/(\d{6})/);
173	  if (!m) { ws.close(1002, '需要房间码路径 /<6位码>'); return; }
174	  const entry = rooms.get(m[1]);
175	  if (!entry || entry.room.closed) { ws.close(1002, '房间不存在'); return; }
176	  const room = entry.room;
177	  const token = new URL(req.url ?? '/', 'http://x').searchParams.get('token') ?? '';
178	  const session = new URL(req.url ?? '/', 'http://x').searchParams.get('session') ?? '';
179	  const c = room.newClient(ws, token);
180	  if (session) room.resumeSession(c, session); // 断线重连：命中则 Hello 时同 slot 复位
181	  console.log(`[ws] 连入房间 ${room.opts.code}`);
182	
183	  ws.on('message', (data: Buffer) => {
184	    c.parser.append(new Uint8Array(data));
185	    try {
186	      c.parser.drain((msgId, r) => room.handle(c, msgId, r));
187	    } catch (e) {
188	      console.error(`[ws] 房间 ${room.opts.code} slot ${c.slot} 异常断开:`, (e as Error).message);
189	      try { ws.close(1002); } catch { /* 已关闭 */ }
190	    }
191	  });
192	  ws.on('close', () => {
193	    room.disconnect(c);
194	    console.log(`[ws] slot ${c.slot} 离开房间 ${room.opts.code}（在线 ${room.onlineCount}）`);
195	  });
196	  ws.on('error', () => { /* close 跟上 */ });
197	});
198	
199	// 超时看门狗：逐房逐客户端（未握手 10s / 已握手 120s，对齐原版 TimeOutTimer）
200	setInterval(() => {
201	  for (const entry of rooms.values()) {
202	    for (const c of [...entry.room.clients]) {
203	      c.lastSeen += 1;
204	      if (c.lastSeen > (c.state >= 1 ? 120 : 10)) {
205	        console.log(`[ws] 房间 ${entry.room.opts.code} slot ${c.slot} 超时踢出`);
206	        c.ws.close();
207	      }
208	    }
209	  }
210	}, 1000);
211	
212	// 时间同步：服务器权威时钟推进（对齐原版 WorldGen.UpdateWorld 时钟）+ 10s 广播
213	setInterval(() => {
214	  for (const entry of rooms.values()) entry.room.world.clock.tick(1000);
215	}, 1000);
216	setInterval(() => {
217	  for (const entry of rooms.values()) {
218	    const room = entry.room;
219	    const f = new NetWriter(18).f64(room.world.clock.timeOfDay).u32(room.world.clock.dayCount).finish();
220	    for (const c of room.clients) if (c.state >= 10) room.send(c, f);
221	  }
222	}, 10000);
223	
224	process.on('uncaughtException', (e) => {
225	  console.error('[server] uncaughtException（记录不退出）:', (e as Error).stack ?? e);
226	});
227	
228	console.log(`[server] 中央服务器 ws://0.0.0.0:${PORT}（lobby http://0.0.0.0:${PORT + 1}/rooms）`);
229	

```


---

## 🤖 Assistant · 2026-08-11T16:00:04.867Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "limit": 190,
 "offset": 1
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:04.882Z

**📎 ToolResult**

```
1	// SoA 多通道平面数组存储。所有热点代码只碰 TypedArray。
2	import { TILE_DEFS } from '../data/tiles';
3	import { TileOpAction } from '../net/protocol';
4	
5	export class TileStore {
6	  readonly w: number;
7	  readonly h: number;
8	  readonly type: Uint16Array;
9	  readonly flags: Uint8Array; // bit0 active bit1 framedDecor占位(预留)
10	  readonly frameX: Uint16Array;
11	  readonly frameY: Uint16Array;
12	  readonly wall: Uint16Array; // 原版 wld 墙 id（0-366）
13	  readonly liquid: Uint8Array;   // 0-255 液量
14	  readonly liquidType: Uint8Array; // 0无 1水 2岩浆 3蜂蜜 4微光(原版 liquidType 3,本仓库 +1 编码;任意液体遇微光 → Aetherium 块 659)
15	  readonly half: Uint8Array;      // halfBrick 位（原版 Tile.cs bTileHeader bit1）：下半 8px 实心
16	  readonly slope: Uint8Array;     // 坡面 0-4（原版编码；渲染暂未支持，生成期少用）
17	  readonly wire: Uint8Array;      // 电路位（原版 Tile.cs sTileHeader）：bit0红 bit1蓝 bit2绿 bit3黄 bit4致动器 bit5已致动(inActive)
18	  // wire 位掩码常量（对应原版 Tile.cs:396-459 的 wire/wire2/wire3/wire4/actuator/inActive）
19	  static readonly WIRE_RED = 1;
20	  static readonly WIRE_BLUE = 2;
21	  static readonly WIRE_GREEN = 4;
22	  static readonly WIRE_YELLOW = 8;
23	  static readonly WIRE_ACTUATOR = 16;
24	  static readonly WIRE_ACTUATED = 32;
25	  static readonly WIRE_COLORS = 15; // 四色掩码
26	
27	  // tile 变更监听（chunk 缓存 / 光照脏标记 / 液体模拟统一从这里拿事件）
28	  private listeners: Array<(x: number, y: number) => void> = [];
29	
30	  // ---- 多人联机上报钩子（ClientNet 注入；单机为 null 零开销） ----
31	  /** 本地 tile 变更上报（协议层 TileOp 收集器）。liquid 通道不报（客户端本地模拟） */
32	  netReporter: ((op: import('../net/protocol').TileOp) => void) | null = null;
33	  /** 应用远端操作期间置位：上报钩子静默（防回环） */
34	  netSuppress = false;
35	
36	  constructor(w: number, h: number, bufs?: import('../workers/protocol').TileBuffers) {
37	    this.w = w; this.h = h;
38	    // buffers 注入（worker transfer 重建路径）：直接以移交的 ArrayBuffer 包装 TypedArray，
39	    // 跳过分配与拷贝。缺省 explored 由调用方（World.fromPacket）补齐
40	    if (bufs) {
41	      this.type = new Uint16Array(bufs.type);
42	      this.flags = new Uint8Array(bufs.flags);
43	      this.frameX = new Uint16Array(bufs.frameX);
44	      this.frameY = new Uint16Array(bufs.frameY);
45	      this.wall = new Uint16Array(bufs.wall);
46	      this.liquid = new Uint8Array(bufs.liquid);
47	      this.liquidType = new Uint8Array(bufs.liquidType);
48	      this.half = new Uint8Array(bufs.half);
49	      this.slope = new Uint8Array(bufs.slope);
50	      this.wire = new Uint8Array(bufs.wire);
51	      return;
52	    }
53	    const n = w * h;
54	    this.type = new Uint16Array(n);
55	    this.flags = new Uint8Array(n);
56	    this.frameX = new Uint16Array(n);
57	    this.frameY = new Uint16Array(n);
58	    this.wall = new Uint16Array(n);
59	    this.liquid = new Uint8Array(n);
60	    this.liquidType = new Uint8Array(n);
61	    this.half = new Uint8Array(n);
62	    this.slope = new Uint8Array(n);
63	    this.wire = new Uint8Array(n);
64	  }
65	
66	  idx(x: number, y: number): number { return y * this.w + x; }
67	
68	  inBounds(x: number, y: number): boolean {
69	    return x >= 0 && y >= 0 && x < this.w && y < this.h;
70	  }
71	
72	  get(x: number, y: number): number { return this.inBounds(x, y) ? this.type[this.idx(x, y)] : 0; }
73	
74	  isActive(x: number, y: number): boolean {
75	    // 原版 nactive() = active && !inActive（Tile.cs:383-394）：已致动格视为不活跃
76	    return this.inBounds(x, y) && this.type[this.idx(x, y)] !== 0
77	      && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) === 0;
78	  }
79	
80	  /** 原版 inActive()：致动器翻转后的"缩入地下"态（有 type 但不碰撞不阻挡） */
81	  isActuated(x: number, y: number): boolean {
82	    return this.inBounds(x, y) && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) !== 0;
83	  }
84	
85	  isSolid(x: number, y: number): boolean {
86	    if (!this.inBounds(x, y)) return false; // 世界外视为空（边缘自由）
87	    if (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) return false; // 已致动不碰撞
88	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
89	    return !!d && d.solid;
90	  }
91	
92	  isPlatform(x: number, y: number): boolean {
93	    if (!this.inBounds(x, y)) return false;
94	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
95	    return !!d && d.platform;
96	  }
97	
98	  onTileChanged(fn: (x: number, y: number) => void) {
99	    this.listeners.push(fn);
100	  }
101	
102	  /** 液体变化独立通道：chunk 缓存不订阅（水不入烘焙画布，无需重建），
103	   *  只有光照订阅（水的光衰减）——避免水流时每帧冲爆 chunk 重建队列造成卡顿 */
104	  private liquidListeners: Array<(x: number, y: number) => void> = [];
105	  onLiquidChanged(fn: (x: number, y: number) => void) {
106	    this.liquidListeners.push(fn);
107	  }
108	
109	  /** 唯一的写入入口（生成/导入期可绕过用 setTileSilent） */
110	  setTile(x: number, y: number, type: number, frameX = 0, frameY = 0) {
111	    if (!this.inBounds(x, y)) return;
112	    const i = this.idx(x, y);
113	    this.type[i] = type;
114	    this.flags[i] = type !== 0 ? 1 : 0;
115	    this.frameX[i] = frameX;
116	    this.frameY[i] = frameY;
117	    if (type === 0) { this.half[i] = 0; this.slope[i] = 0; } // 挖除清半砖/坡面
118	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetTile, x, y, v: type, fx: frameX, fy: frameY });
119	    this.listeners.forEach((fn) => fn(x, y));
120	  }
121	
122	  /** 运行期改半砖/坡面位（锤子交互用；生成期直接写数组即可） */
123	  setHalfBrick(x: number, y: number, v: boolean) {
124	    if (!this.inBounds(x, y)) return;
125	    const i = this.idx(x, y);
126	    this.half[i] = v ? 1 : 0;
127	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetHalfBrick, x, y, v: v ? 1 : 0, fx: 0, fy: 0 });
128	    this.listeners.forEach((fn) => fn(x, y));
129	  }
130	
131	  setSlope(x: number, y: number, s: number) {
132	    if (!this.inBounds(x, y)) return;
133	    const i = this.idx(x, y);
134	    this.slope[i] = s;
135	    this.half[i] = 0; // 原版 SlopeTile 无条件 halfBrick(false)（WorldGen.cs:49174），slope=0 复位时同样
136	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetSlope, x, y, v: s, fx: 0, fy: 0 });
137	    this.listeners.forEach((fn) => fn(x, y));
138	  }
139	
140	  setTileSilent(x: number, y: number, type: number, frameX = 0, frameY = 0) {
141	    if (!this.inBounds(x, y)) return;
142	    const i = this.idx(x, y);
143	    this.type[i] = type;
144	    this.flags[i] = type !== 0 ? 1 : 0;
145	    this.frameX[i] = frameX;
146	    this.frameY[i] = frameY;
147	    if (type === 0) { this.half[i] = 0; this.slope[i] = 0; } // 挖除同步清位（防生成期脏残留）
148	  }
149	
150	  setWall(x: number, y: number, wall: number) {
151	    if (!this.inBounds(x, y)) return;
152	    const i = this.idx(x, y);
153	    if (this.wall[i] !== wall) {
154	      this.wall[i] = wall;
155	      if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetWall, x, y, v: wall, fx: 0, fy: 0 });
156	      this.listeners.forEach((fn) => fn(x, y));
157	    }
158	  }
159	
160	  setWallSilent(x: number, y: number, wall: number) {
161	    if (!this.inBounds(x, y)) return;
162	    this.wall[this.idx(x, y)] = wall;
163	  }
164	
165	  /** 导线/致动位写入（Wiring 系统）。不发 listeners：导线不进 chunk 烘焙画布，
166	   *  走 Renderer 动态覆盖层；致动位变化才需要标脏 chunk（调用方负责） */
167	  setWire(x: number, y: number, bits: number) {
168	    if (!this.inBounds(x, y)) return;
169	    this.wire[this.idx(x, y)] = bits & 63;
170	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetWire, x, y, v: bits & 63, fx: 0, fy: 0 });
171	  }
172	
173	  setWireSilent(x: number, y: number, bits: number) {
174	    this.setWire(x, y, bits);
175	  }
176	
177	  /** 致动器翻转 inActive 态（Wiring.DeActive/ReActive 用）：影响碰撞与渲染，须发 listeners */
178	  setActuated(x: number, y: number, v: boolean) {
179	    if (!this.inBounds(x, y)) return;
180	    const i = this.idx(x, y);
181	    const b = v ? (this.wire[i] | TileStore.WIRE_ACTUATED) : (this.wire[i] & ~TileStore.WIRE_ACTUATED);
182	    if (this.wire[i] === b) return;
183	    this.wire[i] = b;
184	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetActuated, x, y, v: v ? 1 : 0, fx: 0, fy: 0 });
185	    this.listeners.forEach((fn) => fn(x, y));
186	  }
187	
188	  setLiquid(x: number, y: number, amount: number, type: number) {
189	    if (!this.inBounds(x, y)) return;
190	    const i = this.idx(x, y);

```


---

## 🤖 Assistant · 2026-08-11T16:00:19.394Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I need a few more details:

1. Check for any compression (zlib/deflate) anywhere in game/src/net or server/src. Grep for zlib, deflate, compress.
2. Check server room.ts for how SyncNPC/SyncProjectile/SyncItem are relayed and whether there's distance culling. Actually user said they already read room.ts — no need to re-summarize. But question 4 asks about compression anywhere.
3. Check remaining part of simulateRemotePlayers (lines 7899+) and remotePlayerProxies usage/rendering — distance culling for remote players. Also check if there's any distance-based culling in the codebase for net (search for "distance" in net paths). Also strip sending in room.ts (SpawnTileData) — user read room.ts so skip.
4. Check how remotePlayerProxies are rendered (render culling by camera).
5. Check where netChestPoll is, but user didn't ask. Focus.

Also check JSON usage: appearance is JSON string inside binary frames — that's the binary vs JSON mixing. Also server uses HTTP JSON for lobby. Check for any other JSON.stringify in net paths.

Also confirm ws options: `new WebSocketServer({ port: PORT, maxPayload: 1 << 20 })` — no perMessageDeflate option. Note that ws library default: perMessageDeflate defaults to true in the ws library? Actually in ws, `perMessageDeflate` defaults to `{}` (enabled) for the server... Let me recall: In ws, the server option `perMessageDeflate` defaults to... The ws docs: "perMessageDeflate {Boolean|Object} Enable/disable permessage-deflate. Default: false." Hmm — historically ws defaulted to `false`? Let me check: ws README: "permessage-deflate ... enabled by default" — I recall the client `WebSocket` option perMessageDeflate defaults to true (offers the extension). For WebSocketServer, perMessageDeflate default is false... Actually in ws source code, for the server, `perMessageDeflate` option default: `this._perMessageDeflate = (!options.perMessageDeflate ? false : ...)` — wait let me recall the actual source:

In ws lib/WebSocketServer.js:
```js
if (this.options.perMessageDeflate === true) this.options.perMessageDeflate = {};
if (this.options.perMessageDeflate == null) ... 
```
Hmm. Actually in WebSocketServer constructor: `this.options.perMessageDeflate` — code is:
```js
    if (this.options.perMessageDeflate === true) {
      this.options.perMessageDeflate = {};
    }
    if (this.options.perMessageDeflate === false) {
      this.options.perMessageDeflate = null;
    }
```
Wait no. Let me check the real ws source. In WebSocketServer:

```js
  constructor(options, callback) {
    ...
    if (this.options.maxPayload == null) this.options.maxPayload = ...
```

Actually for WebSocketServer there's this snippet:
```js
    if (options.perMessageDeflate === true) options.perMessageDeflate = {};
    if (options.perMessageDeflate == null) options.perMessageDeflate = false;
```
Hmm, I believe in ws the server default for perMessageDeflate is `true`? Let me verify — I recall the docs: "perMessageDeflate {Boolean|Object} Enable/disable permessage-deflate. Default: false. " Hmm, but for WebSocket client the default is true.

From ws docs (WebSocketServer options):
> perMessageDeflate {Boolean|Object} Enable/disable permessage-deflate. Default: false.

Hmm, actually I think the ws docs say: "See WebSocket docs for the options". The WebSocket docs say:
> perMessageDeflate {Boolean|Object} Enable/disable permessage-deflate. Default: false.

Wait, but then how do browsers negotiate deflate with a ws server? Browsers offer permessage-deflate in their handshake. If server has it disabled, it ignores the offer. I'm fairly confident the ws server default is `false`? Hmm, no — let me think about the actual source code:

lib/websocket-server.js in ws:
```js
    if (this.options.maxPayload == null) this.options.maxPayload = 100 * 1024 * 1024;
    ...
    const opts = {
      ...
      perMessageDeflate: this.options.perMessageDeflate,
      ...
    };
```
and in websocket.js completeUpgrade / setSocket:
```js
    if (this._isServer) {
      this._perMessageDeflate = perMessageDeflate ? PerMessageDeflate : null; ...
```

Hmm, in `websocket.js`:
```js
  setSocket(socket, head, options) {
    ...
    let perMessageDeflate = options.perMessageDeflate;
    if (perMessageDeflate === true) perMessageDeflate = {};
    if (!perMessageDeflate) perMessageDeflate = false;  ...
```

Hmm, actually I recall this specific bit from ws source (websocket.js):

```js
    let perMessageDeflate = options.perMessageDeflate;
    if (perMessageDeflate === true) perMessageDeflate = {};
    if (perMessageDeflate === false || ...) 
```

Let me just check whether node_modules exists in the repo and read the ws source to give a factual answer. That's the right approach — ground it in the actual installed ws version.

Also grep for zlib/deflate usage in game/server src.
````

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:20.447Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rniE \"zlib|deflate|gzip|brotli|compress|pako\" ~/Project/GLM/SandboxWorld/game/src ~/Project/GLM/SandboxWorld/server/src 2>/dev/null; echo \"---JSON in net paths---\"; grep -rn \"JSON.stringify\\|JSON.parse\" ~/Project/GLM/SandboxWorld/game/src/net ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -in \"net\\|appear\" | head -30",
 "description": "Search for compression and JSON usage in net paths"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:20.494Z

**📎 ToolResult**

```
---JSON in net paths---
1:~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:229:        const app = JSON.stringify(p2?.appearance ?? {});
2:~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:276:            this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p3.appearance)).finish());
3:~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:606:      this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p.appearance)).finish());
4:~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7895:        const parsed = JSON.parse(rp.appearance) as Record<string, unknown>;

```


---

## 🤖 Assistant · 2026-08-11T16:00:21.159Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/server/node_modules/ws/package.json 2>/dev/null && grep '\"version\"' ~/Project/GLM/SandboxWorld/server/node_modules/ws/package.json; ls ~/Project/GLM/SandboxWorld/node_modules/ws/package.json 2>/dev/null && grep '\"version\"' ~/Project/GLM/SandboxWorld/node_modules/ws/package.json",
 "description": "Find installed ws library version"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:21.200Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/server/node_modules/ws/package.json
  "version": "8.21.3",
~/Project/GLM/SandboxWorld/node_modules/ws/package.json
  "version": "8.21.2",

```


---

## 🤖 Assistant · 2026-08-11T16:00:31.972Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No compression anywhere. Good. Now check ws 8.21.3 source for perMessageDeflate default behavior in WebSocketServer.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:32.792Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"perMessageDeflate\" ~/Project/GLM/SandboxWorld/server/node_modules/ws/lib/websocket-server.js | head -20; echo \"===websocket.js setSocket===\"; grep -n -A 25 \"setSocket(socket, head, options)\" ~/Project/GLM/SandboxWorld/server/node_modules/ws/lib/websocket.js | head -45",
 "description": "Inspect ws library perMessageDeflate default handling"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:32.828Z

**📎 ToolResult**

```
54:   * @param {(Boolean|Object)} [options.perMessageDeflate=false] Enable/disable
76:      perMessageDeflate: false,
134:    if (options.perMessageDeflate === true) options.perMessageDeflate = {};
299:      this.options.perMessageDeflate &&
302:      const perMessageDeflate = new PerMessageDeflate({
303:        ...this.options.perMessageDeflate,
312:          perMessageDeflate.accept(offers[PerMessageDeflate.extensionName]);
313:          extensions[PerMessageDeflate.extensionName] = perMessageDeflate;
===websocket.js setSocket===
213:  setSocket(socket, head, options) {
214-    const receiver = new Receiver({
215-      allowSynchronousEvents: options.allowSynchronousEvents,
216-      binaryType: this.binaryType,
217-      extensions: this._extensions,
218-      isServer: this._isServer,
219-      maxBufferedChunks: options.maxBufferedChunks,
220-      maxFragments: options.maxFragments,
221-      maxPayload: options.maxPayload,
222-      skipUTF8Validation: options.skipUTF8Validation
223-    });
224-
225-    const sender = new Sender(socket, this._extensions, options.generateMask);
226-
227-    this._receiver = receiver;
228-    this._sender = sender;
229-    this._socket = socket;
230-
231-    receiver[kWebSocket] = this;
232-    sender[kWebSocket] = this;
233-    socket[kWebSocket] = this;
234-
235-    receiver.on('conclude', receiverOnConclude);
236-    receiver.on('drain', receiverOnDrain);
237-    receiver.on('error', receiverOnError);
238-    receiver.on('message', receiverOnMessage);

```


---

## 🤖 Assistant · 2026-08-11T16:00:39.170Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: ws WebSocketServer default `perMessageDeflate: false` (websocket-server.js line 76 in default options), and server/src/index.ts passes only `{ port, maxPayload }` — so no extension offered even if the browser client offers it. Good.

Now a few remaining items:

- Remote player proxies: how rendering works, any distance culling for remote players? Check remotePlayerProxies usage in render and simulateRemotePlayers rest (lines 7899-7950). Also check if there's distance culling anywhere (e.g., "剔除" in net code, or player visibility checks). Search for "active" filtering for remote players in Game (e.g., rp.active false → remove proxy?). Let me read Game.ts 7899-7960 and grep remotePlayerProxies.
- netChestPoll — not asked explicitly but msg32 downlink handling was asked: netApplyChest in Game. Let me look at netApplyChest to describe how SyncChestItem is handled client-side.
- Also check how puppet interpolation works: Enemy.ts:341 netPuppet branch (no AI, lerp?). Let me read Enemy.ts around 341. And WeaponProj etc. netPuppet update just integrates position. Check Enemy netPuppet branch.
- Check whether msg23 handles interpolation/lerp for NPC puppets — netApplyNpcSnaps sets x,y directly. Enemy.update netPuppet branch at line 341.

Also distance culling: does the client cull puppets by distance? netSweepPuppets is time-based (300 ticks), not distance. Check server room.ts for distance culling — user read it, but question 2 asks "是否有距离剔除?" on the client side. Let me grep for distance-based culling in the client and confirm absence. Search "5000" already seen (invasion progress). Search for viewport culling of remote players in Renderer? That's render-side culling, maybe relevant. Let me grep remotePlayerProxies.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:39.632Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"remotePlayerProxies\\|netApplyChest\\|netChestPoll\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -20",
 "description": "Locate remote player proxies and chest sync handlers"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:39.664Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:344:  private netApplyChest(chestIdx: number, x: number, y: number, items: Array<{ id: number; stack: number } | null>) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:372:  private netChestPoll() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:623:  private remotePlayerProxies: import('../entities/Player').Player[] = [];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1324:    this.remotePlayerProxies = [];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7718:      this.remotePlayerProxies,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7806:        onChestSync: (chestIdx, x, y, items) => this.netApplyChest(chestIdx, x, y, items),
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7847:    if (this.net?.active && this.tickCount % 15 === 0) this.netChestPoll();
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7872:      let proxy = this.remotePlayerProxies.find((p) => (p as unknown as { __netSlot?: number }).__netSlot === slot);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7928:    this.remotePlayerProxies = list;

```


---

## 🤖 Assistant · 2026-08-11T16:00:39.851Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 40,
 "offset": 330
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:39.858Z

**📎 ToolResult**

```
330	    this.maxHp = this.def.hp;
331	    this.w = this.def.width;
332	    this.h = this.def.height;
333	    this.x = x - this.w / 2;
334	    this.y = y - this.h / 2;
335	  }
336	
337	  fixedUpdate(dt: number, game: GameHooks) {
338	    this.prevX = this.x; this.prevY = this.y;
339	    // 联机傀儡（房主权威快照驱动）：无本地 AI——位置外推 + 动画计时，
340	    // 打击/拾取等交互经 entityNet 上报房主结算
341	    if (this.netPuppet) {
342	      this.aiT++;
343	      this.animT++;
344	      this.x += this.vx;
345	      this.y += this.vy;
346	      this.onGround = Math.abs(this.vy) < 0.6;
347	      if (Math.abs(this.vx) > 0.05) this.walkCycleT += Math.abs(this.vx);
348	      if (this.iframes > 0) this.iframes--;
349	      return;
350	    }
351	    this.aiT++;
352	    if (this.iframes > 0) this.iframes--;
353	    if (this.justHitT > 0) this.justHitT--;
354	    this.lightRGB = null; // 点光由 AI 每帧重写（不残留上一帧状态）
355	    if (this.hpBarT > 0) this.hpBarT--;
356	    if (this.squash !== 0) this.squash *= 0.85;
357	    this.animT++;
358	    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
359	
360	    // EoW 族出生渐显（每 tick alpha-1;原版 AI_006）——静态半透明不受影响
361	    if (this.alphaFade) {
362	      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
363	      if (this.spawnAlpha === 0) this.alphaFade = false;
364	    }
365	
366	    const player = (game as unknown as { player: Player }).player;
367	    const hasPlayer = !!player && !player.dead;
368	
369	    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----

```


---

## 🤖 Assistant · 2026-08-11T16:00:41.824Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read Game.ts 7899-7935 (end of simulateRemotePlayers), netApplyChest 344-384, and 7700-7725 (remotePlayerProxies rendering). Also check line 1324 context (reset). And check whether remote player proxies get culled when rp.active false — read 7899-7935.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:42.002Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 40,
 "offset": 7896
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:42.008Z

**📎 ToolResult**

```
7896	        if (parsed && typeof parsed.hair === 'number') proxy.appearance = parsed as never;
7897	      } catch { /* 保持默认外观 */ }
7898	      // 物品/装备（msg5）：拷入代理背包——手持物 holdStyle/挥舞动画/盔甲纸娃娃渲染依赖。
7899	      // 数组直接共享（代理只读不写，远端真权威在各自客户端）
7900	      const bag = net.remoteItems.get(slot);
7901	      if (bag) {
7902	        proxy.inv.slots = bag.inv;
7903	        proxy.inv.armor = bag.armor;
7904	        proxy.inv.dye = bag.dye;
7905	        proxy.inv.selected = Math.min(rp.selectedItem, 9); // 快捷栏 0-9（heldItem 依赖）
7906	      }
7907	      // useItem 位 → 远端挥舞动画（原版：远端客户端以 controlUseItem 跑 ItemCheck 设置
7908	      // itemAnimation；此处派生等价 swing——时长按本地同公式，攻速配饰差异忽略）
7909	      if (rp.useItem) {
7910	        const heldId = proxy.inv.heldItem()?.id ?? -1;
7911	        if (!proxy.swingNet || proxy.swingNet.item !== heldId || proxy.swingNet.t <= 0) {
7912	          proxy.swingNet = { t: this.remoteSwingDur(heldId), dur: this.remoteSwingDur(heldId), item: heldId };
7913	        } else proxy.swingNet.t--;
7914	      } else if (proxy.swingNet) {
7915	        proxy.swingNet.t--;
7916	        if (proxy.swingNet.t <= 0) proxy.swingNet = null;
7917	      }
7918	      this.stepRemoteProxy(proxy);
7919	      // netOffset 衰减（UpdateNetOffset :28240-28270 1:1，碰撞安全项略）
7920	      const len = Math.hypot(proxy.netOffX, proxy.netOffY);
7921	      if (len < 2) { proxy.netOffX = 0; proxy.netOffY = 0; }
7922	      else {
7923	        const k = Math.max(0, len - Math.max(2, len * 0.1)) / len;
7924	        proxy.netOffX *= k; proxy.netOffY *= k;
7925	      }
7926	      list.push(proxy);
7927	    }
7928	    this.remotePlayerProxies = list;
7929	  }
7930	
7931	  /** 远端挥舞时长（对齐本地各分支公式，Game.useItem 派生处：剑/近战 max(12,useTime)、
7932	   *  镐斧锤 max(14,speed)、其它 30；攻速配饰倍率远端不可见，取基础值） */
7933	  private remoteSwingDur(itemId: number): number {
7934	    if (itemId < 0) return 30;
7935	    const def = ITEM_DEFS[itemId];

```


---

## 🤖 Assistant · 2026-08-11T16:00:42.218Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 42,
 "offset": 342
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:42.223Z

**📎 ToolResult**

```
342	
343	  /** msg32 回包：登记/更新 world.chests（服务器权威），待开箱自动开面板 */
344	  private netApplyChest(chestIdx: number, x: number, y: number, items: Array<{ id: number; stack: number } | null>) {
345	    const w = this.world;
346	    let chest = w.chests.find((ch) => ch.x === x && ch.y === y);
347	    if (!chest) {
348	      chest = { x, y, items: Array(10).fill(null) };
349	      w.chests.push(chest);
350	    }
351	    for (let i = 0; i < items.length; i++) {
352	      // 稀疏数组：单槽广播只带变更槽，undefined = 未涉及（全量帧才每槽都有值）
353	      if (items[i] === undefined || i >= chest.items.length) continue;
354	      chest.items[i] = items[i] ? { ...items[i]! } : null;
355	    }
356	    this.net?.chestIndexByPos.set(`${x},${y}`, chestIdx);
357	    let watch = this.netChestWatch.find((wch) => wch.chest === chest);
358	    if (!watch) {
359	      watch = { chest, idx: chestIdx, last: chest.items.map((it) => it ? { ...it } : null) };
360	      this.netChestWatch.push(watch);
361	    } else {
362	      watch.last = chest.items.map((it) => it ? { ...it } : null);
363	    }
364	    if (this.netPendingChest && this.netPendingChest.x === x && this.netPendingChest.y === y) {
365	      this.netPendingChest = null;
366	      this.tryOpenChest(chest); // 服务器已下发内容 = 通过了 protectItems 门
367	    }
368	    this.cb.onInventoryChanged?.(); // 面板打开中时刷新槽位显示
369	  }
370	
371	  /** postUpdate 每 15 tick：箱子槽位差分上报（含他人广播回写后的再同步收敛） */
372	  private netChestPoll() {
373	    const net = this.net;
374	    if (!net?.active) return;
375	    for (const wch of this.netChestWatch) {
376	      for (let i = 0; i < wch.chest.items.length; i++) {
377	        const a = wch.chest.items[i], b = wch.last[i];
378	        if ((a?.id ?? 0) !== (b?.id ?? 0) || (a?.stack ?? 0) !== (b?.stack ?? 0)) {
379	          net.sendChestSlot(wch.idx, wch.chest.x, wch.chest.y, i, a?.id ?? 0, a?.stack ?? 0);
380	          wch.last[i] = a ? { ...a } : null;
381	        }
382	      }
383	    }

```


---

## 🤖 Assistant · 2026-08-11T16:00:42.427Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 25,
 "offset": 7700
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:42.435Z

**📎 ToolResult**

```
7700	      const [tx, ty] = cam.tileUnder(this.input.mouseX, this.input.mouseY);
7701	      return this.world.store.inBounds(tx, ty) ? { x: tx, y: ty } : null;
7702	    })();
7703	    // 宏伟蓝图拖拽预览:锚点已按下且鼠标悬停有效格时,把 L 路径交给渲染器
7704	    this.renderer.grandPreview = this.grandAnchor && hover
7705	      ? { from: this.grandAnchor, to: [hover.x, hover.y], mode: this.wireToolMode }
7706	      : null;
7707	    this.renderer.render(
7708	      cam, this.world, this.world.clock, this.chunks,
7709	      L.r, L.g, L.b, L.rx, L.ry, L.rw, L.rh,
7710	      this.player,
7711	      this.entities.all(),
7712	      this.particles, this.dmgNumbers,
7713	      this.swing, hover,
7714	      this.boss ? { name: this.boss.vanillaId != null ? Lang.npcName(this.boss.vanillaId) ?? this.boss.def.name : this.boss.def.name, hp: this.boss.hp, maxHp: this.boss.maxHp, cx: this.boss.cx, cy: this.boss.cy } : null,
7715	      this.input.mouseX, this.input.mouseY, this.input.mouseDown,
7716	      this.mining ? Math.min(1, this.mining.progress / this.hardnessCache) : 0,
7717	      this.lighting.clock, // FlickerClock：资源条亮度/呼吸（mouseTextColor/cursorScale）
7718	      this.remotePlayerProxies,
7719	      // 入侵进度条（DrawInvasionProgress :47071；nearInvasion 显示门=屏内 ±5000px 有本组 NPC）
7720	      (() => {
7721	        const w = this.world;
7722	        // 月事件分支（CheckInvasionProgressDisplay :47006-47016：snowMoon/pumpkinMoon
7723	        // 先于常规入侵；name=LegacyInterface.83 霜月 / 84 南瓜月，pct=waveKills/lookup[wave]；
7724	        // 显示门 = 夜晚 + 玩家在地表 + 屏内 ±5000px 有本组 NPC，组号 -kind）

```


---

## 🤖 Assistant · 2026-08-11T16:00:47.743Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything I need. One more: check distance culling — is there any distance-based culling on the client for puppets or remote players? netSweepPuppets is time-based. Rendering culling is camera-based in Renderer (generic). Let me quickly grep for any distance-based skip in the net-related code — search for "cx - " near net or viewport check. Also check whether entities far away are skipped in fixedUpdate (not net). The question asks "是否有距离剔除?" for remote players — the answer: no, ClientNet processes all downlink messages unconditionally; no distance-based filter on the client. Server side (room.ts) — user already read; I could confirm whether room.ts relays to all clients with no distance culling. A quick grep to confirm there's no distance filtering in room.ts relay.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:00:48.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"send\\b\\|broadcast\\|for (const c of\" ~/Project/GLM/SandboxWorld/server/src/room.ts | head -30; echo \"===distance/cull in room===\"; grep -niE \"dist|cull|剔除|范围|range\" ~/Project/GLM/SandboxWorld/server/src/room.ts | head",
 "description": "Check room relay logic for distance filtering"
}
```


---

## 👤 User(sidechain) · 2026-08-11T16:00:48.512Z

**📎 ToolResult**

```
69:  get onlineCount() { let n = 0; for (const c of this.clients) if (c.state >= 10) n++; return n; }
76:  send(c: RoomClient, frame: Uint8Array) {
79:    c.ws.send(frame);
82:  broadcast(frame: Uint8Array, except?: RoomClient) {
83:    for (const c of this.clients) {
85:      this.send(c, frame);
95:        if (c.state >= 1) { this.send(c, new NetWriter(Msg.Kick).str('重复握手').finish()); c.ws.close(); return; }
100:          this.send(c, new NetWriter(Msg.Kick).str(`协议不匹配（期望 ${PROTO_MAGIC} v${PROTO_VER}）`).finish());
119:          if (slot < 0) { this.send(c, new NetWriter(Msg.Kick).str('房间已满').finish()); c.ws.close(); return; }
124:        this.send(c, new NetWriter(Msg.PlayerSlot).u8(c.slot).str(c.session).finish());
130:        this.send(c, this.worldDataFrame());
137:        this.send(c, new NetWriter(Msg.PlayerSpawn).u8(c.slot).i32(this.world.spawnX).i32(this.world.spawnY).finish());
139:        this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(true).str(c.name).finish());
141:        this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(true).finish());
145:          this.send(c, new NetWriter(Msg.PlayerActive).u8(other.slot).bool(true).str(other.name).finish());
146:          this.send(c, new NetWriter(Msg.SyncPlayer).u8(other.slot).str(other.appearance).finish());
156:          if (entries.length) this.send(c, writePlayerItems(entries));
164:        this.broadcast(new NetWriter(Msg.SyncPlayer).u8(c.slot).str(c.appearance).finish(), c);
183:          this.broadcast(writePlayerItems(valid.map((e) => ({ ...e, playerSlot: c.slot }))), c);
201:        this.broadcast(f.finish(), c);
210:          for (const o of ops.slice(0, 8)) this.send(c, this.correctionFrame(o.x, o.y));
214:        this.broadcast(writeTileBatch(ops), c);
227:          this.broadcast(f.finish());
239:        this.send(c, this.chestFrame(idx, -1));
257:          this.send(c, this.chestFrame(chestIdx, -1)); // 权威纠正
261:        if (slots.length) this.broadcast(this.chestFrame(chestIdx, slots[0].slot, c), c);
269:        this.broadcast(new NetWriter(Msg.PlayerLifeMana).u8(c.slot).i16(hp).i16(maxHp).finish(), c);
288:        this.broadcast(f.finish(), c);
306:        this.broadcast(f.finish(), c);
327:        this.broadcast(f.finish(), c);
===distance/cull in room===

```


---

## 🤖 Assistant · 2026-08-11T16:01:26.864Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: no distance filtering anywhere — broadcast to all connected clients (state >= 10 filter presumably).

Now compile the final report. Include:

1. protocol.ts frame format details.
2. ClientNet receive side per message.
3. Game.ts scheduling.
4. Compression / JSON mixing.
5. LanDiscovery.
6. ws permessage-deflate.

Since plan mode is active — but I'm a read-only search agent and my task is to report facts. I'll just return the report as my final message. The plan-mode reminder says answer the user's query comprehensively. I don't need to create a plan file since this is a research/report task, not an implementation task.

Let me structure it carefully with file:line refs.

Frame format:
- NetWriter (protocol.ts:68-113): initial buffer 256B, len starts at 3 (reserves [u16 len][u8 msgId]), grow doubles capacity (line 79-87). Writers: u8/i8 (89-90), u16/i16/u32/i32/f32/f64 (91-96), bool=u8 (97), bytes (98), str = u16 byte length + UTF-8 TextEncoder (99-103). finish(): guard len>65535 (line 108), backfills little-endian u16 total length at offset 0 (len includes the 3-byte header, line 109), msgId at byte 2 (line 110), returns subarray view (line 111).
- Frame = [u16 little-endian total frame length including 3-byte header][u8 msgId][payload...] — protocol.ts:2, 105-112.
- FrameParser (143-181): appends a copied Uint8Array per ws message (149), buffers until >= 3 bytes, MAX_BUFFER 256KB → reset if exceeded (156, 159), on each drain merges all chunks into one new Uint8Array (161-164), scans: read u16 len at p; if len<3 or >65535 skip 1 byte resync (171); if p+len > buf.length break (half frame, 172); msgId = buf[p+2]; callback with NetReader over payload (174). Leftover tail kept for next time (178).
- NetReader (117-138): little-endian DataView reads; str() = u16 length + TextDecoder UTF-8 (134-137).
- writeTileBatch (245-255): msg17: u16 count, then per op: u8 action, i32 x, i32 y, u16 v; if action==SetTile additionally u16 fx + u16 fy. So per op 11B or 15B + 2B count + 3B header. Non-SetTile ops carry fx/fy=0 but are NOT serialized (conditional).
- encodeStrip (278-313): msg10 TileSection: header i32 x0, i32 y0, u16 w, u16 h (12B + 3 frame header), then RLE runs: [u16 count][11B state: u16 type, u8 flags, u16 frameX, u16 frameY, u16 wall, u8 liquid, u8 liquidType, u8 half, u8 slope, u8 wire] = 13B per run. Run breaks when any of the 10 channels differ (298-302). codecVer=0 plain RLE, comment 270-273: 11B bare per tile, strips default 200×20 = 4400 tiles, worst case 57KB < 64KB.
- decodeStrip (316-339): bounds check, run loop with count==0 break and written clamp (324-337).
- writePlayerItems (200-211): msg5: u16 count + per entry u8 playerSlot, u8 container, u8 itemSlot, u16 itemId, u16 stack = 8B/entry.
- Per-message byte layouts: enumerate.

msg13 (PlayerState) layout: u8 slot, u8 ctrlBits, u8 flagBits, u8 selectedItem, f32 x, f32 y, [f32 vx, f32 vy if flag&4] = 20 or 28 bytes payload + 3 header (protocol.ts:30-33; send ClientNet.ts:557-563; parse ClientNet.ts:315-343).

msg23 SyncNPC: u16 count + per: u32 netId, str key (2+len), f32 x4 (16B), i16 hp, i16 maxHp, u16 animT, u8 flags = 27B + key len per entry (protocol.ts:41-43, ClientNet.ts:641-653/398-410).

msg27 SyncProjectile: u16 count + per: u32 netId, u8 kind, str tag, i16 dmg, i16 aux, f32 x,y,vx,vy = 19B + tag (protocol.ts:44-45, ClientNet.ts:667-677/423-435).

msg21 SyncItem: u32 netId, u8 op; if op==0: str key, u16 stack, f32 x,y,vx,vy = 6 + (2+k) + 2 + 16; op 1/2 = 8 bytes total (6+3 header) (protocol.ts:39-40, ClientNet.ts:656-664/412-421).

msg7 WorldData: f64 time, u32 dayCount, u16 w, u16 h, i32 spawnX, i32 spawnY, f32 groundLevel/rockLevel/lavaLine, i32 seed, str name, bool crimson, i32 dungeonX/dungeonY/jungleX, u16 flagCount, then [str key + bool] per flag (ClientNet.ts:459-483).

msg32 SyncChestItem: u16 chestIdx, i32 x, i32 y, u16 count, per: u8 slot, u16 itemId, u16 stack (protocol.ts:47-48, ClientNet.ts:578-584/589-599).

msg8 SpawnTileData request: i32 x, i32 y (ClientNet.ts:192, 481).

msg10 strip format above.

Other messages: Hello (msg1): str magic + u16 protoVer + str name + str hostToken (ClientNet.ts:154). msg3 PlayerSlot: u8 slot + str session (ClientNet.ts:212-216). msg4 SyncPlayer: u8 slot + str appearance JSON (229, 276, 602-608). msg9 StatusText: u16 count (239). msg12 PlayerSpawn: u8 slot, i32 x, i32 y (262-264). msg14 PlayerActive: u8 slot, bool active, str name (281-284). msg18 SetTime: f64 time, u32 dayCount (352-361). msg82 NetModules: u16 moduleId; Text module: u8 slot, str text, u8 r, u8 g, u8 b (364-380). msg200 RoomPolicy: 5× str/bool (383-392). msg16: u8 slot, i16 hp, i16 maxHp (443-448). msg42: u32 netId, i16 dmg, f32 kbx, f32 kby (436-441; protocol comment says u8 crit u8 kbDir — note discrepancy: protocol.ts:49 documents {u32 netId, i16 dmg, u8 crit, u8 kbDir, f32 srcX, srcY} but implementation sends u32+i16+f32+f32 — actual wire format diverges from the doc comment; ClientNet.ts:681 and Game relay. Worth noting as fact.)
- msg154 Ping: f64 performance.now() (143-144).

2. Client receive handling — describe each.

netPuppet creation/interpolation:
- NPC: Game.netApplyNpcSnaps (477-502) creates Enemy via fromVanilla/new Enemy, netPuppet=true, added to entities; position set directly from snapshot; Enemy.fixedUpdate netPuppet branch (Enemy.ts:341-349) = dead-reckoning x+=vx/y+=vy, animT++, no AI.
- Proj: netApplyProjSnaps 537-553 + netMakeProj 555-564 rebuild actual class; puppet update in each proj class: x += vx (Arrow.ts:91, WeaponProj.ts:113/184/251, MagicProj.ts:41, Dart.ts:149/332).
- Drop: netApplyItemOp 505-534 creates ItemDrop puppet.
- Remote players: ClientNet.players map; Game.simulateRemotePlayers (7867-7929) creates Player proxy per slot, netOffset error accumulation (7878-7885), control-bit-driven physics stepRemoteProxy, netOffset decay max(2, len*0.1), >300px reset.
- Puppet cleanup: netSweepPuppets 580-607, timeout 300 ticks NPC/drop, 180 ticks proj.
- Distance culling: none. No distance check anywhere in client net path; server broadcast() (room.ts:82-86) sends to all clients state>=10 with no spatial filter (room.ts grep shows no dist/range). Only culling is time-based puppet expiry and render-camera culling (generic renderer, remotePlayerProxies passed whole at Game.ts:7718).

3. Game scheduling:
- postUpdate (Game.ts:7828-7858) called per logic tick after fixedUpdate entity update (comment 7827). Contents:
  - net.tick() every tick when net active (7830-7831) — tile queue flush (max 64 ops/packet, ClientNet.ts:507-519), inventory diff 250ms, HP sync 200ms/5s, sendPlayerState 66ms/1s.
  - Strip request every 30 ticks (7833-7841).
  - simulateRemotePlayers every tick (7845).
  - netChestPoll every 15 ticks (7847).
  - Entity sync every 4 ticks (tickCount % 4 === 0, 7850-7854): if isHost netNpcBroadcast, then netProjBroadcast + netDropSweep always. So at 60Hz logic, every 4 ticks = 15Hz.
  - netSweepPuppets every 30 ticks (7855).
  - netPuppetContact every tick for non-host (7856).
- Single-player zero-overhead: everything gated by `this.net?.active`; net is null in singleplayer. TileStore.netReporter defaults null (TileStore.ts:32) — per-write check `if (this.netReporter && !this.netSuppress)` at lines 118, 127, 136, 155, 170, 184. entityNet hooks default null (entitySyncHooks.ts:4-10). TileStore.setTileSilent doesn't report (140-148).
- netNpcBroadcast details: change-driven (moved >0.5px or hp changed) + 120 tick (2s) full-resync fallback (410-411), cap 24 snaps/packet (419), cleans diff baseline for dead enemies (421-426).
- netProjBroadcast: change driven moved <1px and <60 ticks skip (442), cap 24 (452), kinds 0-4 (445-449), unknown kinds skipped (450).
- netDropSweep: full scan diff each call; new drops send op=0 (464-467), disappeared send op=1 (470-472). NOTE: it iterates all drops and rebuilds Map every 4 ticks — no cap on sends (unlike the 24-cap on npc/proj). Actually it sends one msg per drop spawn/take, each a separate frame.

Note: tileQueue cap 256 (ClientNet.ts:490) with overflow warning once (491-497).

4. Compression: none. grep for zlib/deflate/gzip/brotli/compress/pako across game/src and server/src → 0 hits. Only compression is the RLE in encodeStrip. JSON mixing: appearance is JSON.stringify'd inside binary frame msg4 (ClientNet.ts:229, 276, 606; parsed Game.ts:7895). HTTP lobby is JSON (server index.ts:87-89 etc.), and world upload is JSON save in POST body (index.ts:122-125). ws frames are all binary (client sends Uint8Array; server ws.binaryType='nodebuffer' index.ts:171; client binaryType='arraybuffer' ClientNet.ts:139).

5. LanDiscovery — described above.

6. ws: `new WebSocketServer({ port: PORT, maxPayload: 1 << 20 })` (server/src/index.ts:168) — no perMessageDeflate option. ws 8.21.3 default perMessageDeflate: false (node_modules/ws/lib/websocket-server.js:54 doc comment "[options.perMessageDeflate=false]" and :76 in defaults). maxPayload 1MB (server side). Client browser WebSocket: whatever the browser does; since server doesn't offer the extension, no deflate negotiated.

Also note: separate lobby HTTP server on PORT+1 (index.ts:164), WS on PORT.

Write the final report now. No emojis. Use file:line refs.
```

</details>


---

## 🤖 Assistant · 2026-08-11T16:02:13.059Z · glm-x-preview-260804

```
调查完成。以下为各事实清单(均带 文件:行号)。

## 1. 协议帧格式(game/src/net/protocol.ts)

**基础帧**:`[u16 len(小端, 含头总长)][u8 msgId][payload...]`,包上限 65535B(protocol.ts:2, 105-112)。PROTO_MAGIC='SW1',PROTO_VER=3(protocol.ts:7-10)。

**NetWriter**(protocol.ts:68-113):
- 初始 buffer 256B,`len` 初始为 3(预留头)(69-77);grow 按 2 倍扩容(79-87)
- 写入器全为定宽小端:`u8/i8/u16/i16/u32/i32/f32/f64/bool(=u8)`(89-97)、`bytes` 原样拷贝(98)
- **字符串 = `[u16 字节数][UTF-8 字节]`,TextEncoder,无终止符**(99-103)
- `finish()`:`len > 65535` 抛错(含头总长守卫,108);回填 `dv.setUint16(0, len, true)`(109);`buf[2]=msgId`(110);返回 subarray 视图,finish 后禁写(105, 111)

**FrameParser**(protocol.ts:143-181):
- `append` 对每条 ws 消息做一次**拷贝**存入 chunks 数组(149)
- `drain`:缓冲 <3B 直接返回;>256KB(MAX_BUFFER)整体重置(156-159);每次 drain **把全部 chunk 合并成一个新 Uint8Array**(161-164)
- 扫描:读 u16 len;`len<3 || len>65535` → **p+=1 按字节重同步**(脏流防护,171);`p+len > buf.length` → break 半包(172);`msgId = buf[p+2]`,payload 交给 `NetReader(buf.subarray(p+3, p+len))`(173-174);尾部残留回填 chunks(178)

**NetReader**(117-138):小端 DataView;`str()` = u16 长度 + TextDecoder(134-137)。

**encodeStrip / msg10 TileSection —— 有 RLE,无其他压缩**(protocol.ts:270-339):
- 头:`i32 x0, i32 y0, u16 w, u16 h`(12B)+ 3B 帧头(284)
- RLE 段:`[u16 count][11B 完整状态]`,状态 = `u16 type, u8 flags, u16 frameX, u16 frameY, u16 wall, u8 liquid, u8 liquidType, u8 half, u8 slope, u8 wire`(291-292)→ 每段 13B
- 触发断段的条件是 **10 个通道任一不同**(298-302);按行优先(y 外层 x 内层)扫描(295-296)
- 注释:裸 tile 11B,条带默认 200×20 = 4400 格,最坏 57KB < 64KB 上限(272-273)
- `decodeStrip`:越界返回 null(322);`count===0` 或 payload 尽时终止防死循环(326-327);按 run 展开直写 SoA 数组(324-337)

**writeTileBatch / msg17**(protocol.ts:245-255):`u16 count` + 每 op `u8 action, i32 x, i32 y, u16 v`,仅 `SetTile` 附加 `u16 fx, u16 fy`(即每 op 11B 或 15B;非 SetTile 的 fx/fy 不上线,252-253)。

**writePlayerItems / msg5**(protocol.ts:200-211):`u16 count` + 每 entry `u8 playerSlot, u8 container, u8 itemSlot, u16 itemId, u16 stack` = 8B/entry;INV_SYNC_SIZES=[58,20,10](198)。

**各消息字节构成(payload,不含 3B 头)**:
| 帧 | 构成 | 引用 |
|---|---|---|
| msg1 Hello | str magic + u16 protoVer + str name + str hostToken | ClientNet.ts:154 |
| msg3 PlayerSlot | u8 slot + str session | ClientNet.ts:212-216 |
| msg4 SyncPlayer | u8 slot + str(appearance JSON) | ClientNet.ts:230, 276, 606 |
| msg7 WorldData | f64 time, u32 dayCount, u16 w, u16 h, i32 spawnX/Y, f32 ground/rock/lava, i32 seed, str name, bool crimson, i32 dungeonX/Y, i32 jungleX, u16 flagCount, [str+bool]×N | ClientNet.ts:459-483 |
| msg8 SpawnTileData | i32 x, i32 y | ClientNet.ts:192, 481 |
| msg9 StatusText | u16 count | ClientNet.ts:239 |
| msg10 TileSection | 见上 RLE | protocol.ts:283-292 |
| msg12 PlayerSpawn | u8 slot, i32 x, i32 y | ClientNet.ts:262-264 |
| msg13 PlayerState | u8 slot, u8 ctrlBits, u8 flagBits, u8 selectedItem, f32 x, f32 y, [f32 vx, f32 vy 当 flag&4] → **20B 或 28B** | ClientNet.ts:315-321, 557-563 |
| msg14 PlayerActive | u8 slot, bool active, str name | ClientNet.ts:281-284 |
| msg16 PlayerLifeMana | u8 slot, i16 hp, i16 maxHp | ClientNet.ts:443-448, 696 |
| msg17 TileBatch | 见上 | protocol.ts:245-255 |
| msg18 SetTime | f64 time, u32 dayCount | server/src/index.ts:219;ClientNet.ts:354-355 |
| msg21 SyncItem | u32 netId, u8 op;op=0 时附加 str key, u16 stack, f32 x,y,vx,vy;op=1/2 仅 6B | ClientNet.ts:412-420, 656-664 |
| msg23 SyncNPC | u16 count + 每 [u32 netId, str key, f32 x,y,vx,vy, i16 hp, i16 maxHp, u16 animT, u8 flags] = **27B + key 长度** | ClientNet.ts:398-410, 641-653 |
| msg27 SyncProjectile | u16 count + 每 [u32 netId, u8 kind, str tag, i16 dmg, i16 aux, f32 x,y,vx,vy] = **19B + tag 长度** | ClientNet.ts:423-435, 667-677 |
| msg31 RequestChestOpen | i32 x, i32 y | ClientNet.ts:574 |
| msg32 SyncChestItem | u16 chestIdx, i32 x, i32 y, u16 count, [u8 slot, u16 itemId, u16 stack] | ClientNet.ts:578-584, 589-599 |
| msg42 StrikeNPC | 实际发送 `u32 netId, i16 dmg, f32 kbx, f32 kby`(ClientNet.ts:681、436-441)。**注意 protocol.ts:49 的注释写的是 `{u32 netId, i16 dmg, u8 crit, u8 kbDir, f32 srcX, f32 srcY}` —— 注释与实际线格式不一致** | protocol.ts:49 vs ClientNet.ts:681 |
| msg82 NetModules | u16 moduleId;Text 模块: u8 slot, str text, u8 r, u8 g, u8 b | ClientNet.ts:364-380 |
| msg154 Ping | f64 performance.now() | ClientNet.ts:143-144 |
| msg200 RoomPolicy | str roomCode, str roomName, bool isHost, bool protectTiles, bool protectItems | ClientNet.ts:383-392 |

netId 合成:`(ownerSlot & 0xff) << 24 | localId & 0xffffff`(entitySyncHooks.ts:13-15)。

## 2. ClientNet 接收侧(game/src/net/ClientNet.ts + core/Game.ts)

- 收包入口:`ws.onmessage` → `parser.append(new Uint8Array(e.data))` → `drain((id,r)=>handle)`(ClientNet.ts:157-160)。`handle` 是单 switch(205-454),未知 msgId 静默跳过(451-452)。

**各下行消息处理**:
- **msg13 PlayerState**(315-343):无 RemotePlayerState 时**就地创建**条目并放入 `players` Map(325-334);否则直接覆写 x/y/vx/vy/控制位/selectedItem/dead,并置 `fresh=true`(335-342)。不做插值,位置即权威值;平滑在 Game 侧完成。
- **msg23 SyncNPC**(398-410):解出 NpcSnap 数组 → `hooks.onNpcSnapshot` → `Game.netApplyNpcSnaps`(Game.ts:477-502):傀儡 upsert,首次创建时 `v_<id>` 键走 `Enemy.fromVanilla`、原生键走 `new Enemy`(483-484),覆写快照坐标(构造按中心偏移,486),置 `netPuppet=true`、`netId/hp/maxHp`,加入 entities,boss 置 `this.boss`(489-491)。已存在的直接写 x/y/vx/vy/hp/animT,`|vx|>0.1` 时翻 facing(496-499)。
- **msg27 SyncProjectile**(423-435):→ `Game.netApplyProjSnaps`(537-553)+ `netMakeProj`(555-564):按 kind 0=Arrow/1=Boomerang(WeaponProj 族代表)/2=Dart/3=TrapShot/4=MagicProj **重建真实类**,纯视觉不跑命中(536 注释);未知 kind 跳过(450)。
- **msg21 SyncItem**(412-421):op=0 → `netApplyItemOp`(505-520)按 key 反查 itemId,新建 ItemDrop 傀儡或更新位置/速度;op=1/2(521-533)先删傀儡映射,否则扫描本地真掉落(`!netPuppet && netId` 匹配)置 dead——覆盖"拥有者的真掉落被他人拾取"。
- **msg7 WorldData**(234-236 → 459-483):构建 `pendingWorld`(World 骨架 + clock/spawn/层线/flags),随后立即发送 msg8 请求出生点周围 section(481)。
- **msg32 SyncChestItem**(394-397 → applyRemoteChest 589-599 → `Game.netApplyChest` Game.ts:344-369):稀疏槽位数组(`items[slot] = ...`,undefined=未涉及,596),登记 `world.chests`(不存在则新建 10 槽,346-350),记录 `chestIndexByPos` 并维护 `netChestWatch` 差分基准(356-363),有 `netPendingChest` 待开箱时自动开面板(364-367)。
- **msg10 条带**(246-260):初始组装期写入 `pendingWorld.store` 并推进进度(249-255);运行期直写 `gameWorld.store`,`onSectionArrived` 由 Game 每 4 格 markDirtyAround + `lighting.dirty=true`(Game.ts:7782-7791)。
- msg17(345-349)→ `applyRemote`(612-631):`st.netSuppress=true` 包裹逐 op 调 TileStore setter(try/finally 复位,615-630),即**回环抑制靠标志位而非去重**。
- msg42(436-441)→ 房主 `netApplyStrike`(Game.ts:566-577):按 netId 找真身 `hurt()`,本地减一次防御出伤害数字。
- msg16(443-448):非本 slot 时写入 RemotePlayerState 的 hp/maxHp。

**傀儡运动模型(无快照插值,纯外推)**:
- Enemy:`fixedUpdate` 的 `netPuppet` 分支只有 `x+=vx; y+=vy; animT++; onGround 判定; walkCycleT 累加`(Enemy.ts:341-349),**不跑任何 AI**。
- 弹幕:各类的 netPuppet 分支同样只有 `x+=vx; y+=vy; return`(Arrow.ts:91、WeaponProj.ts:113/184/251、MagicProj.ts:41、Dart.ts:149/332、FallingBlock.ts:33)。
- 掉落:msg21 直接写 x/y/vx/vy(518-519)。
- 傀儡回收 `netSweepPuppets`(Game.ts:580-607):NPC/掉落 300 tick、弹幕 180 tick 无新快照即置 dead;**纯时间阈值,无距离判定**。

**远程玩家傀儡与插值**:
- 状态存于 `ClientNet.players`(Map<slot, RemotePlayerState>,ClientNet.ts:91);`fresh` 标记新权威包(26-28)。
- `Game.simulateRemotePlayers`(Game.ts:7867-7929)每逻辑 tick 跑:`remotePlayerProxies` 按 `__netSlot` 查找/新建**独立 Player + 空 Inventory**(7872-7876);`fresh` 时注入 `netOffX/Y += 模拟位置 - 权威位置`,偏移 >300px 直接归零,硬设权威 pos/vel(7878-7885);控制位→input 跑 `stepRemoteProxy` 本地物理(7887-7892, 7918);netOffset 衰减 `<2px 归零,否则每步乘 max(2, len*0.1)`(7919-7925);useItem 位派生远端挥舞 swingNet(7909-7917);msg5 物品数组直接共享进代理背包(7900-7906)。
- 代理整列表传给 Renderer 渲染(Game.ts:7718)。

**距离剔除:不存在**。客户端对下行消息无条件全量处理,无任何按玩家位置/视口的过滤;服务端 `Room.broadcast`(room.ts:82-86)也只是 `for (const c of this.clients) if (state>=10) send` —— grep `dist|cull|range|剔除` 在 room.ts 为 0 命中。唯一的"剔除"是:傀儡时间超时回收(见上)、msg23/msg27 每包 24 条上限(Game.ts:419, 452)、渲染层相机剔除(与联机无关)。

## 3. Game.ts 联机钩子调度

**总入口 `postUpdate()`(Game.ts:7828-7858,注释:fixedUpdate 实体更新后每逻辑帧调用,7827)**:
- `net.tick()` —— **每 tick**(7830-7831):内部冲洗 tile 队列(每包最多 64 op,ClientNet.ts:507-519)、库存差分 250ms(725-745)、HP 上报 200ms 节流/5s 满血心跳(687-697)、`sendPlayerState`(66ms 节流/1s 静止心跳,547-548)
- 移动续传:每 30 tick 检查条带边界,变化才 `requestSection`(7833-7841)
- `simulateRemotePlayers()` —— 每 tick(7845)
- `netChestPoll()` —— 每 15 tick 箱子槽位差分上报(7847;实现 372-384)
- **实体同步:`tickCount % 4 === 0`(≈15Hz @60TPS)**(7850-7854):`isHost` 才 `netNpcBroadcast`;`netProjBroadcast` 与 `netDropSweep` 双向全跑
- `netSweepPuppets()` —— 每 30 tick(7855)
- `netPuppetContact()` —— 非 host 每 tick(7856;傀儡 NPC 对本地玩家 AABB 接触伤害,609-621)

**三个广播函数**:
- `netNpcBroadcast`(399-428):变化驱动(`|dx|>0.5 || |dy|>0.5 || hp 变`,410)+ 120 tick(2s)全量兜底(411);每包上限 24 条,余量下轮(419);顺带清理已消亡敌人的差分基准(421-426)。
- `netProjBroadcast`(431-455):变化驱动(`<1px 且 <60 tick 跳过`,442);kind 映射 Arrow/WeaponProj 族/TrapShot/Dart/MagicProj(445-449),未知类不同步(450);每包上限 24(452)。
- `netDropSweep`(458-474):每次**全量扫描** drops,新掉落(无 netId)逐条发 op=0,消失(上轮在本轮无)逐条发 op=1;**逐条独立成帧,无条数上限**(466, 471),且每 4 tick 重建整个 `netDropSeen` Map(473)。

**tile 队列冲洗(TileStore.netReporter)**:
- 注入点:`world.store.netReporter = (op) => net.reportTileOp(op)`(Game.ts:7773),onWorldReady 时设置;同时注入 `entityNet.reportStrike`(7775)。
- 上报路径:setTile/setHalfBrick/setSlope/setWall/setWire/setActuated 内 `if (this.netReporter && !this.netSuppress) this.netReporter({...})`(TileStore.ts:118, 127, 136, 155, 170, 184);`setTileSilent` 不上报(140-148);**liquid 通道不上报**(TileStore.ts:31 注释,客户端本地模拟)。
- `reportTileOp` 入队上限 256,超限告警一次后丢弃(ClientNet.ts:488-500);`net.tick()` 每 tick splice 最多 64 打包发 msg17(507-519)。

**单机零开销**:
- 所有 postUpdate 联机块都套 `if (this.net?.active)`(7830, 7833, 7845, 7847, 7849);`this.net` 单机为 null(joinNetGame 才赋值,7770;断开时置 null,7764)。
- `TileStore.netReporter` 默认 null(TileStore.ts:32),单机写路径只剩一次 null 判断。
- `entityNet` 三个钩子默认 null(entitySyncHooks.ts:4-10),单机"恒 null(零开销)"(2 行注释)。

## 4. 压缩 / JSON 混用

- **压缩:全仓库 game/src 与 server/src 中 `zlib|deflate|gzip|brotli|compress|pako` 零命中**(仅 HTTP 层无、ws 层无、应用层无)。唯一的压缩是 encodeStrip 的**自定义 RLE**(protocol.ts:270-313, codecVer=0)。
- **二进制为主,JSON 混用点**:
  - msg4 SyncPlayer 的 `appearance` 字段是 **JSON.stringify 后塞进二进制帧的字符串字段**(ClientNet.ts:229, 276, 606;接收端 Game.ts:7895 `JSON.parse`,仅接受含 `hair` 的完整对象)。
  - HTTP lobby 全 JSON(房间创建/列表/`/lan` 探测端点,server/src/index.ts:87-89, 97-158);房间创建时 **整个世界存档以 JSON 字符串放 POST body**(上限 256MB,index.ts:18, 122-125)。
  - ws 上所有帧均为二进制:浏览器侧 `binaryType='arraybuffer'`(ClientNet.ts:139),服务端 `ws.binaryType='nodebuffer'`(index.ts:171)。

## 5. LanDiscovery(game/src/net/LanDiscovery.ts)

- 背景:浏览器无 UDP,用 **WebRTC ICE host candidate 拿本机 IP + /24 网段 HTTP 扫描**(1-7)。
- `getLocalIpv4(timeoutMs=1500)`(19-51):`new RTCPeerConnection({iceServers:[]})` + 建 data channel 触发 candidate 收集(32-38);正则提取 candidate 中的 IPv4(42);仅接受 10/192.168/172.16-31(46);secure context 下被 mDNS 混淆成 .local(注释 4-6)。
- `scanLan(localIp, excludeIps, port=7778)`(54-83):枚举 /24 的 1-254(56-61);每个 IP 并发 `fetch http://<ip>:7778/lan`,400ms AbortController 超时(66-67);响应 `magic===1010` 视为自家服务器(70-71);结果含 port(默认回填 7777)/name/online/max/w/h(72-75);**分批 32 并发防连接数爆炸**(79-81)。
- `discoverServers(manualPrefix?)`(89-105):manualPrefix 直接扫;否则 getLocalIpv4 失败时 fallback 问 `http://127.0.0.1:7778/lan` 的 `lanIps[0]`(97-101,房主本机跑服务器的场景);仍取不到返回空。
- 服务端配合:`GET /lan` 返回 `{ok, magic:1010, port, rooms, lanIps}`(server/src/index.ts:155-157),CORS `*` + `Allow-Access-Control-Private-Network`(63-68);lobby 监听 PORT+1 即 7778(index.ts:164),ws 监听 PORT=7777(index.ts:16, 168)。

## 6. WS permessage-deflate 配置

- 服务端:`new WebSocketServer({ port: PORT, maxPayload: 1 << 20 })`(server/src/index.ts:168)——**未传 `perMessageDeflate`,ws 8.21.3 服务端默认 `perMessageDeflate: false`**(server/node_modules/ws/lib/websocket-server.js:54 注释 `[options.perMessageDeflate=false]`,76 默认值)。因此即便浏览器在握手中 offer permessage-deflate,服务端也不会接受协商。
- 相关边界:服务端 `maxPayload = 1MB`(index.ts:168);帧解析器应用层缓冲上限 256KB(protocol.ts:156-159)。

补充一个与容量相关的协议事实:msg42 的文档注释(protocol.ts:49)与实际线格式(ClientNet.ts:681)不一致,任何按注释写解析/中继的代码都会错位。
```
