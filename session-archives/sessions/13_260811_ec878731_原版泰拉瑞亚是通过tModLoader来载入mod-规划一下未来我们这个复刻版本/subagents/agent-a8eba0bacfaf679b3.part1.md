# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T08:34:03.119Z

```
对 ~/Project/GLM/SandboxWorld 的多人联机做**跨端协议矩阵与文档对账**终审。搜索广度:thorough。这是第三视角:前两路在查代码内部,你查"两端+文档+探针"四方一致性。

逐项核查:
1. **协议字段矩阵**:以 game/src/net/protocol.ts 的 Msg 注释为基准,逐消息核对服务器编码(room.ts)与客户端解码(ClientNet.ts)的字段序/类型/方向——特别是五轮改过的:msg23(S→C 短码 eflags/C→S 全量)、msg27(kind 值域 0-8+bit7,tag 各 kind 的打包格式 5-8)、msg28、msg200(maxPlayers)、msg201。列一张对齐表,标出任何不一致。
2. **PROTO_VER 使用点全量清点**:grep 全仓库所有 PROTO_VER(应只有 protocol.ts 定义+两端 import+探针 _netfake.mjs 常量)——有没有遗漏的硬编码版本号或残留 v4/v5 字样误导。
3. **探针覆盖对账**:game/scripts/_roomprobe.mjs(54 断言)与 _loadprobe.mjs——对照已落地机制清单(AOI/短码/合包/背压分级/maxPlayers/限流/盲端踢/session认领/持久化/--world/SSC/msg28/敌弹伤害/bit7门禁/慢客户端踢/房主公告),哪些有断言、哪些只靠代码审查、哪些完全没覆盖(诚实列表)。探针自身有没有随语义变化过时的断言文案。
4. **文档对账**:game/docs/multiplayer-design.md 的 §8bis/§8ter(挂账清偿/对抗补丁/近似收紧)逐条与代码现状核对——有没有写了没做/做了没写/写错的(尤其:慢客户端踢、房主公告文案、SSC 语义描述、限流阈值数字、AOI 半径 1536)。旧章节(§2 消息字典/§8.6)与 v6 现实的冲突清单。
5. **_netfake.mjs 健康度**:Msg 表与 protocol.ts 的 enum 是否同步(v6 新增 28/201);Writer 与 NetWriter 行为差异(边界:u16 溢出/str 编码)会不会在探针里埋雷。
6. **开服.sh/部署面**:与 --ssc/--max-players/--world-budget 等 CLI 的最终形态对账;文档里部署注意事项(SIGTERM 单播)是否准确。

输出:对齐表+不一致清单(文件:行号/期望vs现实/严重程度)+探针覆盖缺口列表。用中文。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T08:34:03.121Z

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

## 🤖 Assistant · 2026-08-12T08:34:04.643Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the relevant files. This is a thorough audit task covering protocol matrix, PROTO_VER usage, probe coverage, docs reconciliation, _netfake.mjs health, and deployment surface.

Let me find the files first.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:05.447Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld -type f \\( -name \"protocol.ts\" -o -name \"room.ts\" -o -name \"ClientNet.ts\" -o -name \"_roomprobe.mjs\" -o -name \"_loadprobe.mjs\" -o -name \"_netfake.mjs\" -o -name \"multiplayer-design.md\" -o -name \"开服.sh\" \\) 2>/dev/null | grep -v node_modules",
 "description": "Locate protocol, server, client, probe and doc files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:05.729Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/开服.sh
~/Project/GLM/SandboxWorld/server/src/room.ts
~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md
~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs
~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs
~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts
~/Project/GLM/SandboxWorld/game/src/workers/protocol.ts

```


---

## 🤖 Assistant · 2026-08-12T08:34:06.076Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"PROTO_VER\" ~/Project/GLM/SandboxWorld --include=\"*.ts\" --include=\"*.mjs\" --include=\"*.js\" --include=\"*.md\" -l 2>/dev/null | grep -v node_modules | grep -v \"src/.*\\.js$\"",
 "description": "Find all files referencing PROTO_VER"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:10.765Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/server/src/room.ts
~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md
~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs
~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs
~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts

```


---

## 🤖 Assistant · 2026-08-12T08:34:11.772Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/protocol.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:11.792Z

**📎 ToolResult**

```
1	// 多人联机共享协议层（客户端与 Node 服务器共用，docs/multiplayer-design.md §1-2）。
2	// 帧格式对齐原版：[u16 len][u8 msgId][payload...]，小端，包上限 65535B。
3	// 消息 ID 尽量沿用原版 MessageID 编号（Hello=1/SLOT=3/WorldData=7/TileSection=10/
4	// PlayerSpawn=12/PlayerControls=13/TileManipulation=17/SetTime=18/NetModules=82/Ping=154）；
5	// 编码字段为本仓库简化集（protoVer 门禁，当前 v5——见 PROTO_VER 注释）。
6	
7	export const PROTO_MAGIC = 'SW1';
8	/** v2：msg13 对齐原版 PlayerControls 布局（控制位+position+velocity）。
9	 *  v3：实体同步族（msg16/21/23/27/42）+ 箱子权威（msg31/32）+ sessionToken 重连
10	 *  v4：msg23 S→C 短码格式（key 每次全量→codeId 短码+按需全量）+ RoomPolicy 尾部 u16 maxPlayers
11	 *  v5：msg27 kind 高位 bit7=hostile（原版 Projectile.hostile 位——访客端据此对敌对弹幕
12	 *      傀儡本地结算 Damage_EVP；服务器剥除非房主置位）
13	 *  v6：msg27 kind 5-8（锚定 Boss 的自包含弹体：DukeSharknadoBolt/龙卷/MLDeathray/LunarOrb，
14	 *      tag 打包锚参数，访客重建真类本地跑确定性 AI）+ msg28 弹幕消亡上报（消幽灵弹窗口）+
15	 *      msg201 SSC 角色档下发（--ssc）。server 与 game 同仓库同时发布，不做向后兼容 */
16	export const PROTO_VER = 6;
17	
18	/** 消息 ID（v1 实现范围；编号对齐原版 MessageID.cs） */
19	export const enum Msg {
20	  Hello = 1,          // C→S {magic, protoVer, name, hostToken 兜底}
21	  Kick = 2,           // S→C {reason}（原版 Kick/Disconnect 同号）
22	  PlayerSlot = 3,     // S→C {slot, sessionToken}（原版同号 PlayerInfo=3：名字/外观在原版
23	                      //   走此包，我们拆到 Hello+msg4——字段分布简化，ID 保留；
24	                      //   sessionToken 为重连凭据）
25	  SyncPlayer = 4,     // 双向 {slot, appearanceJson}
26	  SyncPlayerItem = 5, // C→S→广播（v2 对齐原版 msg5 SyncPlayerItem 语义，批量变体）：
27	                      //   {u8 count, entries[{u8 playerSlot(服务端覆写), u8 container,
28	                      //    u8 itemSlot, u16 itemId(0=空), u16 stack}]}
29	                      //   container: 0=slots[0..57] 1=armor[0..19] 2=dye[0..9]
30	  RequestWorldData = 6, // C→S {}
31	  WorldData = 7,      // S→C {时间/尺寸/出生点/层线/flags/seed/name}
32	  SpawnTileData = 8,  // C→S {x, y}（客户端请求出生点周围 section）
33	  StatusText = 9,     // S→C {count}（将发的 strip 数，进度条）
34	  TileSection = 10,   // S→C {x0,y0,w,h, rleBytes}（200×20 条带）
35	  PlayerSpawn = 12,   // S→C {slot, x, y}（进房落点确认）
36	  PlayerState = 13,   // C→S→广播（v2 对齐原版 msg13）：{u8 slot, u8 ctrlBits, u8 flagBits,
37	                      //   u8 selectedItem, f32 x, f32 y, [f32 vx, f32 vy 若 flagBits[2]]}
38	                      //   ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction
39	                      //   flagBits: [2]hasVelocity [6]ghost(死亡)。position=碰撞盒左上（原版语义）
40	  PlayerActive = 14,  // S→C 广播 {slot, active, name}
41	  TileBatch = 17,     // C→S→广播 {count, ops[]}（tile 操作批量，对齐 msg17 语义）
42	  SetTime = 18,       // S→C {timeOfDay, dayCount}
43	  // ---- v3 实体同步（房主权威 + 服务器中继；ID 对齐原版 MessageID.cs） ----
44	  PlayerLifeMana = 16, // 双向 {u8 slot, i16 hp, i16 maxHp}（原版同号：客户端权威 HP，服务器中继）
45	  SyncItem = 21,       // 房主→广播 {u32 netId, u8 op(0=spawn/1=take/2=despawn), str key,
46	                       //   u16 stack, f32 x,y,vx,vy}（原版同号 SyncItem）
47	  SyncNPC = 23,        // C→S（房主上行）：{u16 count, [u32 netId, str key, f32 x,y,vx,vy,
48	                       //    i16 hp, i16 maxHp, u16 animT, u8 flags(bit0=boss)]}
49	                       // S→C（v4 短码+AOI 逐端过滤）：{u16 count, [u8 eflags, ...,
50	                       //    eflags.bit0=含 key 全量(u32 netId + u16 codeId + str key)
51	                       //             bit1=boss；否则仅 u16 codeId（客户端 codeId→netId/key 表）]}
52	  SyncProjectile = 27, // 双向（各自的弹幕互播，原版同号）：
53	                       //   {u16 count, [u32 netId, u8 kind, str tag, i16 dmg, i16 aux, f32 x,y,vx,vy]}
54	                       //   （kind 低 7 位: 0=Arrow 1=WeaponProj族 2=Dart 3=TrapShot 4=MagicProj
55	                       //    5=DukeSharknadoBolt 6=DukeSharknadoTornado 7=MLDeathray 8=LunarOrb（v6：
56	                       //    Boss 锚定弹体，tag 打包锚参数——见 Game.netProjBroadcast 各分支注释）；
57	                       //    bit7(0x80)=hostile——原版 Projectile.hostile，v5 起 kind0/2/3 携带
58	                       //    （服务器剥除非房主置位），访客端对 hostile 傀儡本地结算 Damage_EVP）
59	  ProjDespawn = 28,  // C→S→广播（v6）：{u16 count, [u32 netId]}——弹幕消亡上报，
60	                    //   各端对自己拥有的弹幕在消亡时批量上报，接收端即时移除傀儡
61	                    //   （替代纯 180t 超时清扫：消除幽灵弹窗口 + 消亡闪烁）
62	  RequestChestOpen = 31, // C→S {i32 x, i32 y}（箱子锚点；原版同号）
63	  SyncChestItem = 32,  // S→C 下发 / C→S 槽位编辑（原版同号 SyncChestItem）：
64	                       //   {u16 chestIdx, i32 x, i32 y, u16 count, [u8 slot, u16 itemId, u16 stack]}
65	  StrikeNPC = 42,      // 访客→房主（服务器定向转发）{u32 netId, i16 dmg, f32 kbx, f32 kby}
66	                       //   （原版 42=Unknown42：旧 StrikeNPC 槽位；注释曾误写 crit/kbDir/srcX/srcY——
67	                       //    实际线格式自 v3 起即为 dmg+击退两分量，2026-08 校正）
68	  NetModules = 82,    // 双向 {moduleId, ...}（module1=聊天 module2=ping）
69	  Ping = 154,         // 简化独立心跳（module2 并存预留）
70	  // ---- v3 房间制扩展（docs/multiplayer-design.md §房间） ----
71	  RoomPolicy = 200,   // S→C {roomCode, roomName, isHost, protectTiles, protectItems, u16 maxPlayers(v4)}
72	  SscSync = 201,      // S→C（v6，--ssc 启用时）{str recordJson}——服务器角色档下发。
73	                      //   record = {hp, maxHp, x, y, inv, armor, dye, savedAt}（id=内部下标，
74	                      //   同版本 registry 一致）。客户端进房应用覆盖本地角色。
75	                      //   语义=存档型 SSC（原版 ServerSideCharacter 同款信任模型，非反作弊）
76	}
77	
78	/** NetModule 表（0-2 对齐原版 NetworkInitializer.cs 注册序：Liquid/Text/Ping；
79	 *  JoinLeave=3 与原版 NetAmbienceModule 撞号——本协议双端自洽，无互操作需求） */
80	export const enum NetModule {
81	  Liquid = 0,   // 预留（v1 液体客户端本地）
82	  Text = 1,     // 聊天 {authorSlot, text, r, g, b}（author=255 无前缀，对齐原版 255=服务器）
83	  PingModule = 2, // 预留
84	  JoinLeave = 3,  // S→C 系统 {slot, joined}——加入/离开公告（原版 Lang.mp[19]/[20]，服务器广播）
85	}
86	
87	// ================= Writer（小端，定宽；字符串 = u16 长度 + UTF-8） =================
88	
89	export class NetWriter {
90	  private buf = new Uint8Array(256);
91	  private len = 0;
92	  private dv: DataView;
93	
94	  constructor(private readonly msgId: number) {
95	    // 预留 [u16 len][u8 msgId]
96	    this.len = 3;
97	    this.dv = new DataView(this.buf.buffer);
98	  }
99	
100	  private grow(need: number) {
101	    if (this.len + need <= this.buf.length) return;
102	    let cap = this.buf.length;
103	    while (cap < this.len + need) cap *= 2;
104	    const nb = new Uint8Array(cap);
105	    nb.set(this.buf.subarray(0, this.len));
106	    this.buf = nb;
107	    this.dv = new DataView(this.buf.buffer);
108	  }
109	
110	  u8(v: number): this { this.grow(1); this.buf[this.len++] = v & 255; return this; }
111	  i8(v: number): this { return this.u8(v < 0 ? v + 256 : v); }
112	  u16(v: number): this { this.grow(2); this.dv.setUint16(this.len, v, true); this.len += 2; return this; }
113	  i16(v: number): this { this.grow(2); this.dv.setInt16(this.len, v, true); this.len += 2; return this; }
114	  u32(v: number): this { this.grow(4); this.dv.setUint32(this.len, v >>> 0, true); this.len += 4; return this; }
115	  i32(v: number): this { this.grow(4); this.dv.setInt32(this.len, v, true); this.len += 4; return this; }
116	  f32(v: number): this { this.grow(4); this.dv.setFloat32(this.len, v, true); this.len += 4; return this; }
117	  f64(v: number): this { this.grow(8); this.dv.setFloat64(this.len, v, true); this.len += 8; return this; }
118	  bool(v: boolean): this { return this.u8(v ? 1 : 0); }
119	  bytes(b: Uint8Array): this { this.grow(b.length); this.buf.set(b, this.len); this.len += b.length; return this; }
120	  str(s: string): this {
121	    const b = new TextEncoder().encode(s);
122	    this.u16(b.length);
123	    return this.bytes(b);
124	  }
125	
126	  /** 回填长度前缀并返回完整帧（含 [u16 len][u8 id]）。finish 后禁止再写入（subarray 视图） */
127	  finish(): Uint8Array {
128	    // Q3 修复：守卫含头总长（此前 len-3 在 65533..65535 区间漏检 → setUint16 回绕 → 接收端脏流）
129	    if (this.len > 65535) throw new Error(`net: 包超限 ${this.len}`);
130	    this.dv.setUint16(0, this.len, true);
131	    this.buf[2] = this.msgId & 255;
132	    return this.buf.subarray(0, this.len);
133	  }
134	}
135	
136	// ================= Reader =================
137	
138	export class NetReader {
139	  private dv: DataView;
140	  private p = 0;
141	  constructor(private readonly buf: Uint8Array) {
142	    this.dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
143	  }
144	  get pos() { return this.p; }
145	  u8(): number { return this.buf[this.p++]; }
146	  i8(): number { const v = this.buf[this.p++]; return v >= 128 ? v - 256 : v; }
147	  u16(): number { const v = this.dv.getUint16(this.p, true); this.p += 2; return v; }
148	  i16(): number { const v = this.dv.getInt16(this.p, true); this.p += 2; return v; }
149	  u32(): number { const v = this.dv.getUint32(this.p, true); this.p += 4; return v; }
150	  i32(): number { const v = this.dv.getInt32(this.p, true); this.p += 4; return v; }
151	  f32(): number { const v = this.dv.getFloat32(this.p, true); this.p += 4; return v; }
152	  f64(): number { const v = this.dv.getFloat64(this.p, true); this.p += 8; return v; }
153	  bool(): boolean { return this.u8() !== 0; }
154	  bytes(n: number): Uint8Array { const b = this.buf.subarray(this.p, this.p + n); this.p += n; return b; }
155	  str(): string {
156	    const n = this.u16();
157	    return new TextDecoder().decode(this.bytes(n));
158	  }
159	}
160	
161	// ================= 帧流解析（粘包；对齐原版 CheckBytes 语义） =================
162	
163	/** 字节流帧解析器：append 后逐帧回调 {msgId, payloadReader}，自动处理半包。
164	 *  P0.4 增量化：单一缓冲 + 读写偏移（旧版每 drain 把全部 chunk 合并成新数组——
165	 *  4 人房每秒数百次全量拷贝，纯 GC 压力）。残余半包 copyWithin 归位。 */
166	export class FrameParser {
167	  private buf = new Uint8Array(4096);
168	  private len = 0;
169	  private _draining = false;
170	
171	  append(data: Uint8Array) {
172	    if (this._draining) throw new Error('FrameParser: drain 回调内禁止 append（会破坏解析缓冲）');
173	    if (this.len + data.length > this.buf.length) {
174	      let cap = this.buf.length;
175	      while (cap < this.len + data.length) cap *= 2;
176	      const nb = new Uint8Array(cap);
177	      nb.set(this.buf.subarray(0, this.len));
178	      this.buf = nb;
179	    }
180	    // 拷贝入缓冲（ws 回调数据可能被复用）
181	    this.buf.set(data, this.len);
182	    this.len += data.length;
183	  }
184	
185	  /** 解析所有完整帧；返回 false 表示缓冲为空。
186	   *  脏流防护：len 非法时按字节重同步（此前 break 不前进 → 永久失步 + 缓冲无限增长）。
187	   *  缓冲上限：超限重置（半包攻击防御）。P1.3 合包后单条 WS 消息可达 512KB
188	   *  （服务器 FLUSH_SLICE 切片；25 条 strip 拼发），上限须高于切片粒度——
189	   *  2026-08 实踩：沿用 256KB 旧值会把进房 strip 大包整包丢弃 → 世界组装永久卡死 */
190	  private static readonly MAX_BUFFER = 4 * 1024 * 1024;
191	  drain(cb: (msgId: number, r: NetReader) => void): boolean {
192	    if (this._draining) throw new Error('FrameParser: drain 重入');
193	    if (this.len < 3) return this.len > 0;
194	    if (this.len > FrameParser.MAX_BUFFER) { this.len = 0; return false; }
195	    this._draining = true;
196	    let p = 0;
197	    let any = false;
198	    const dv = new DataView(this.buf.buffer, this.buf.byteOffset, this.buf.byteLength);
199	    try {
200	      while (p + 3 <= this.len) {
201	        const len = dv.getUint16(p, true);
202	        if (len < 3 || len > 65535) { p += 1; continue; } // 脏字节：跳过重同步
203	        if (p + len > this.len) break; // 半包
204	        const msgId = this.buf[p + 2];
205	        cb(msgId, new NetReader(this.buf.subarray(p + 3, p + len)));
206	        p += len;
207	        any = true;
208	      }
209	    } finally {
210	      this._draining = false;
211	      // 压缩必须在 finally：回调抛错时 p 已前进，若不归位会从 0 重放同一批帧
212	      // → 同一异常反复抛出，连接永久毒化（review C3）
213	      if (p > 0) {
214	        if (p < this.len) this.buf.copyWithin(0, p, this.len);
215	        this.len -= p;
216	      }
217	    }
218	    return any || this.len > 0;
219	  }
220	}
221	
222	// ================= 玩家物品同步（msg5 SyncPlayerItem 批量变体） =================
223	
224	export const enum ItemContainer {
225	  Slots = 0,  // inv.slots[0..57]
226	  Armor = 1,  // inv.armor[0..19]（0-2 盔甲/3-9 配饰/10-12 时装/13-19 时装配饰）
227	  Dye = 2,    // inv.dye[0..9]
228	}
229	
230	export interface ItemSyncEntry {
231	  container: ItemContainer;
232	  itemSlot: number;
233	  itemId: number;   // 0 = 空
234	  stack: number;
235	}
236	
237	export const INV_SYNC_SIZES = [58, 20, 10];
238	
239	export function writePlayerItems(entries: Array<ItemSyncEntry & { playerSlot: number }>): Uint8Array {
240	  const w = new NetWriter(Msg.SyncPlayerItem);
241	  w.u16(entries.length);
242	  for (const e of entries) {
243	    w.u8(e.playerSlot);
244	    w.u8(e.container);
245	    w.u8(e.itemSlot);
246	    w.u16(e.itemId & 0xffff);
247	    w.u16(e.stack & 0xffff);
248	  }
249	  return w.finish();
250	}
251	
252	export function readPlayerItems(r: NetReader): Array<ItemSyncEntry & { playerSlot: number }> {
253	  const n = r.u16();
254	  const out: Array<ItemSyncEntry & { playerSlot: number }> = [];
255	  for (let i = 0; i < n; i++) {
256	    const playerSlot = r.u8();
257	    const container = r.u8() as ItemContainer;
258	    const itemSlot = r.u8();
259	    const itemId = r.u16();
260	    const stack = r.u16();
261	    out.push({ playerSlot, container, itemSlot, itemId, stack });
262	  }
263	  return out;
264	}
265	
266	// ================= tile 操作批量（msg17，对齐原版单点操作语义的批量变体） =================
267	
268	export const enum TileOpAction {
269	  SetTile = 0,    // v=type, fx, fy
270	  SetWall = 1,    // v=wall
271	  SetHalfBrick = 5,
272	  SetSlope = 6,
273	  SetActuated = 3,
274	  SetWire = 4,    // v=bits
275	}
276	
277	export interface TileOp {
278	  a: TileOpAction;
279	  x: number; y: number;
280	  v: number;
281	  fx: number; fy: number;
282	}
283	
284	export function writeTileBatch(ops: TileOp[]): Uint8Array {
285	  const w = new NetWriter(Msg.TileBatch);
286	  w.u16(ops.length);
287	  for (const o of ops) {
288	    w.u8(o.a);
289	    w.i32(o.x); w.i32(o.y);
290	    w.u16(o.v & 0xffff);
291	    if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
292	  }
293	  return w.finish();
294	}
295	
296	export function readTileBatch(r: NetReader): TileOp[] {
297	  const n = r.u16();
298	  const ops: TileOp[] = [];
299	  for (let i = 0; i < n; i++) {
300	    const a = r.u8() as TileOpAction;
301	    const x = r.i32(), y = r.i32(), v = r.u16();
302	    let fx = 0, fy = 0;
303	    if (a === TileOpAction.SetTile) { fx = r.u16(); fy = r.u16(); }
304	    ops.push({ a, x, y, v, fx, fy });
305	  }
306	  return ops;
307	}
308	
309	// ================= tile strip RLE 编解码（msg10，codecVer=0 裸 RLE） =================
310	// 每 tile 完整状态 = type/flags/frameX/frameY/wall/liquid/liquidType/half/slope/wire
311	// 11B 裸；RLE 按"全状态相同"连续段编码 [u16 count][11B 状态]，地下均质区压缩比极高。
312	// 条带默认 200×20（4400 格，最坏 57KB < 64KB 包上限）。
313	
314	export interface StripRect { x0: number; y0: number; w: number; h: number; }
315	
316	/** 编码一条 strip（读 store 指定矩形） */
317	export function encodeStrip(
318	  st: { w: number; h: number; type: Uint16Array; flags: Uint8Array; frameX: Uint16Array; frameY: Uint16Array;
319	        wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; half: Uint8Array; slope: Uint8Array; wire: Uint8Array },
320	  rect: StripRect,
321	): Uint8Array {
322	  const w = new NetWriter(Msg.TileSection);
323	  w.i32(rect.x0); w.i32(rect.y0); w.u16(rect.w); w.u16(rect.h);
324	  const idx = (x: number, y: number) => y * st.w + x;
325	  let run = 0;
326	  let rType = 0, rFlags = 0, rFx = 0, rFy = 0, rWall = 0, rLiq = 0, rLt = 0, rHalf = 0, rSlope = 0, rWire = 0;
327	  const flushRun = () => {
328	    if (run === 0) return;
329	    w.u16(run);
330	    w.u16(rType); w.u8(rFlags); w.u16(rFx); w.u16(rFy); w.u16(rWall);
331	    w.u8(rLiq); w.u8(rLt); w.u8(rHalf); w.u8(rSlope); w.u8(rWire);
332	    run = 0;
333	  };
334	  for (let y = rect.y0; y < rect.y0 + rect.h; y++) {
335	    for (let x = rect.x0; x < rect.x0 + rect.w; x++) {
336	      const i = idx(x, y);
337	      if (run > 0 && (
338	        st.type[i] !== rType || st.flags[i] !== rFlags || st.frameX[i] !== rFx || st.frameY[i] !== rFy
339	        || st.wall[i] !== rWall || st.liquid[i] !== rLiq || st.liquidType[i] !== rLt
340	        || st.half[i] !== rHalf || st.slope[i] !== rSlope || st.wire[i] !== rWire
341	      )) flushRun();
342	      if (run === 0) {
343	        rType = st.type[i]; rFlags = st.flags[i]; rFx = st.frameX[i]; rFy = st.frameY[i];
344	        rWall = st.wall[i]; rLiq = st.liquid[i]; rLt = st.liquidType[i];
345	        rHalf = st.half[i]; rSlope = st.slope[i]; rWire = st.wire[i];
346	      }
347	      run++;
348	    }
349	  }
350	  flushRun();
351	  return w.finish();
352	}
353	
354	/** 解码一条 strip 直写目标 store（批量路径：绕过事件，调用方负责事后整块标脏） */
355	export function decodeStrip(
356	  st: { w: number; h: number; type: Uint16Array; flags: Uint8Array; frameX: Uint16Array; frameY: Uint16Array;
357	        wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; half: Uint8Array; slope: Uint8Array; wire: Uint8Array },
358	  r: NetReader,
359	): StripRect | null {
360	  const x0 = r.i32(), y0 = r.i32(), w = r.u16(), h = r.u16();
361	  if (x0 < 0 || y0 < 0 || x0 + w > st.w || y0 + h > st.h) return null;
362	  let written = 0;
363	  while (written < w * h) {
364	    const count = r.u16();
365	    // C2 防死循环：count=0（恶意/损坏数据）或 payload 已尽（截断）→ 终止并返回已写区域
366	    if (count === 0) break;
367	    const type = r.u16(), flags = r.u8(), fx = r.u16(), fy = r.u16(), wall = r.u16();
368	    const liq = r.u8(), lt = r.u8(), half = r.u8(), slope = r.u8(), wire = r.u8();
369	    for (let k = 0; k < count && written < w * h; k++) {
370	      const x = x0 + (written % w), y = y0 + Math.floor(written / w);
371	      const i = y * st.w + x;
372	      st.type[i] = type; st.flags[i] = flags; st.frameX[i] = fx; st.frameY[i] = fy; st.wall[i] = wall;
373	      st.liquid[i] = liq; st.liquidType[i] = lt; st.half[i] = half; st.slope[i] = slope; st.wire[i] = wire;
374	      written++;
375	    }
376	  }
377	  return { x0, y0, w, h };
378	}
379	

```


---

## 🤖 Assistant · 2026-08-12T08:34:12.635Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/server/src/room.ts ~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs ~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs ~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs ~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md ~/Project/GLM/SandboxWorld/开服.sh ~/Project/GLM/SandboxWorld/game/src/workers/protocol.ts",
 "description": "Get line counts of all audited files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:12.797Z

**📎 ToolResult**

```
     975 ~/Project/GLM/SandboxWorld/server/src/room.ts
     836 ~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts
     760 ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs
     186 ~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs
      92 ~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs
     477 ~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md
      15 ~/Project/GLM/SandboxWorld/开服.sh
      73 ~/Project/GLM/SandboxWorld/game/src/workers/protocol.ts
    3414 total

```


---

## 🤖 Assistant · 2026-08-12T08:34:14.943Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: the task mentioned "_netfake.mjs" but the probes are `_roomprobe.mjs` (760 lines, not 54 assertions per se). Let me read all files. Note there might be multiple _netfake files. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:15.094Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/room.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:15.512Z

**📎 ToolResult**

```
1	// 房间会话（中央服务器架构）：一个 Room = 一个世界实例 + 一组客户端 + 房间策略。
2	// 与 index.ts（lobby/路由）解耦；对齐原版 RemoteClient 状态机语义（0/1/2/3/10）。
3	import { WebSocket } from 'ws';
4	import { randomUUID } from 'node:crypto';
5	import {
6	  PROTO_MAGIC, PROTO_VER, Msg, NetModule,
7	  NetWriter, NetReader, FrameParser,
8	  TileOp, TileOpAction, readTileBatch, writeTileBatch, encodeStrip,
9	  ItemContainer, INV_SYNC_SIZES, readPlayerItems, writePlayerItems,
10	} from '../../game/src/net/protocol.ts';
11	import { World } from '../../game/src/world/World.ts';
12	import { TILE_DEFS } from '../../game/src/data/tiles.ts';
13	import { ITEM_DEFS, ITEM_BY_KEY } from '../../game/src/data/items.ts';
14	
15	export interface RoomOptions {
16	  code: string;         // 6 位房间码
17	  name: string;         // 房间显示名（= 世界名）
18	  publicRoom: boolean;  // 公开（false = 仅房间码可进）
19	  protectTiles: boolean;  // 破坏保护：非房主禁止任何 tile 编辑（服务端权威拒绝）
20	  protectItems: boolean;  // 物品保护：非房主禁止箱子取放/物品放置（策略下发，客户端门禁）
21	  hostToken: string;    // 房主令牌（建房 HTTP 返回；首次携带的连接 = 房主；'' = 无主房，首进者为房主）
22	  /** 单房人数逻辑上限（钳 [2,255]；slot 数组物理上限恒 255，见 MAX_PLAYERS） */
23	  maxPlayers: number;
24	}
25	
26	/** SSC 角色档加载注入（index.ts 注入：读 server/ssc/<name>.json；null=无档/未启用） */
27	export type SscLoader = (name: string) => string | null;
28	
29	/** 每客户端观测计数（P0.1 /stats） */
30	export interface ClientStats {
31	  inBytes: number; outBytes: number;
32	  bufferedMax: number;   // ws.bufferedAmount 高水位
33	  sendDrops: number;     // 背压丢弃总帧数
34	  lowDrops: number;      // 其中 prio=1（实体快照类）低水位先行丢弃
35	}
36	
37	/** 每房观测计数（P0.1 /stats；outBps 由 stats.ts 1s 差分采样写入） */
38	export interface RoomStats {
39	  outBytes: number; outBps: number; lastSampleAt: number;
40	  msgHist: Map<number, { n: number; bytes: number }>;
41	  sendDrops: number; stalePos: number;
42	  stripHit: number; stripMiss: number;  // P2.1 section 缓存
43	  tileOps: number;                      // 累计 tile op 数（P3.1 持久化脏标记用）
44	  chestEdits: number;                   // 累计箱子槽位编辑数（P3.1：msg32 不经 tileOps，须独立脏标记——review S1 物品复制/丢失）
45	}
46	
47	export interface RoomClient {
48	  ws: WebSocket;
49	  parser: FrameParser;
50	  slot: number;
51	  state: number;        // 对齐原版：0 连接 / 1 过握手 / 10 在游戏
52	  name: string;
53	  appearance: string;
54	  lastSeen: number;
55	  isHost: boolean;
56	  /** URL 携带的房主令牌（路由层注入；Hello 消息内 token 为兜底） */
57	  urlToken?: string;
58	  /** 重连凭据（PlayerSlot 下发；断开后 60s 内携此 session 重连同 slot 复位） */
59	  session: string;
60	  /** 重连恢复的 slot（≥0 时 Hello 跳过分配直接复位） */
61	  resumedSlot: number;
62	  /** resumeSession 已认领凭据（Hello 成功前断线 → disconnect 释放认领） */
63	  claimedSession: boolean;
64	  sentStrips: Set<string>;
65	  /** AOI 接收端位置（由其上行 msg13 顺带更新；px 坐标，P1.1） */
66	  lastX: number; lastY: number; lastPosAt: number;
67	  /** AOI 滞回集合：netId → 最近一次出现在某快照批的时刻（P1.1） */
68	  aoiNpc: Map<number, number>;
69	  aoiProj: Map<number, number>;
70	  /** 滞回集/短码集上次过期清理时刻 */
71	  lastAoiPrune: number;
72	  /** msg23 短码已知集：codeId → 最近使用时刻（P1.2；过期清除后自动回落全量） */
73	  npcKnown: Map<number, number>;
74	  /** 发送合包暂存（P1.3；ws message 回调末尾 flushOutbox 统一拼发） */
75	  outbox: Uint8Array[];
76	  stats: ClientStats;
77	  /** 上行限流窗口（①：秒级 per-msgId 计数） */
78	  rateSecond: number;
79	  rateCounts: Int32Array;
80	  /** SSC 累积（v6 --ssc：msg16 顺带记录，断开/定时落盘） */
81	  hp: number;
82	  maxHp: number;
83	  /** 物品快照（msg5 累积；新人进场时全量下发） */
84	  items: {
85	    inv: Array<{ id: number; stack: number } | null>;
86	    armor: Array<{ id: number; stack: number } | null>;
87	    dye: Array<{ id: number; stack: number } | null>;
88	  };
89	}
90	
91	/** slot 物理上限（u8 协议槽位；逻辑上限 = opts.maxPlayers 可小于此值） */
92	const MAX_PLAYERS = 255;
93	const STRIP_W = 200;
94	const STRIP_H = 20;
95	/** 背压分级（P0.1）：≤1MB 正常；1-4MB 只丢 prio=1（实体快照类）；>4MB 全丢。全计数 */
96	const LOW_BUFFER_LIMIT = 1 << 20;
97	const SEND_BUFFER_LIMIT = 4 << 20;
98	/** 单条合包 WS 消息切片上限（防超 wss maxPayload 1MB；留余量） */
99	const FLUSH_SLICE = 512 * 1024;
100	/** 箱子 tile sheet id（TileID.Chest=21；applyTileOps 清箱检测用） */
101	const CHEST_TILE_ID = 21;
102	// ---- P1.1 实体 AOI（切比雪夫距离，px）----
103	const AOI_PLAYER = 1920;  // msg13 远端玩家：120 tiles（同屏协作+建造）
104	// 实体内径 1536px（96t）：≥玩家内径的 80%，消除 1280~1920px 的"见人不见弹"对射
105	// 空洞（弓箭射程 ~1500px 恰落在旧区间）——代价是实体流量带宽 +20%
106	const AOI_ENTITY = 1536;
107	const AOI_OUT_FACTOR = 1.6;   // 滞回外径 = 内径 ×1.6（边界抖动防闪烁）
108	const AOI_STALE_MS = 5000;    // 接收端位置超时：跳过实体广播（见 aoiBlind——防饱和放大循环）
109	const AOI_PRUNE_MS = 30_000;  // 滞回集/短码已知集的过期清理
110	// 不变量（改动前必读）：NPC 静止兜底间隔（客户端 2s=120 tick）必须 ≪ 傀儡清扫阈值
111	// （300 tick）——AOI 重入视野后 ≤2s 内必有全量快照补 key，傀儡不会被误清。
112	// msg21 掉落物不做 AOI：spawn 是一次性事件（无重播机制），过滤会导致走近的玩家永远看不见。
113	
114	export class Room {
115	  readonly opts: RoomOptions;
116	  clients = new Set<RoomClient>();
117	  private slotUsed = new Array<boolean>(MAX_PLAYERS).fill(false);
118	  private hostJoined = false;
119	  /** 断线 session 保留（§8.8 重连：60s 内携 session 重连同 slot 复位，不刷加入公告）。
120	   *  认领制（review 项4）：建连只标记 claimed 不消费，Hello 成功才 delete——
121	   *  握手前二次断线凭据不烧、3 次重连承诺成立；且修复旧实现"认领即删条目 →
122	   *  61s 超时回调因条目不存在而跳过释放"的 slot 永久泄漏 */
123	  private sessions = new Map<string, { slot: number; name: string; appearance: string; until: number; claimed: boolean }>();
124	  closed = false;
125	  /** --world 常驻房（P3.1）：空房回收豁免；hostToken='' 首进者为房主 */
126	  persistent = false;
127	  /** 上次持久化时的 tileOps/chestEdits 基线（P3.1：空房无修改则跳过写盘） */
128	  lastSavedTileOps = 0;
129	  lastSavedChestEdits = 0;
130	  /** 观测计数（P0.1；stats.ts 采样读取） */
131	  readonly roomStats: RoomStats = {
132	    outBytes: 0, outBps: 0, lastSampleAt: Date.now(),
133	    msgHist: new Map(), sendDrops: 0, stalePos: 0,
134	    stripHit: 0, stripMiss: 0, tileOps: 0, chestEdits: 0,
135	  };
136	  /** msg23 短码表（P1.2）：netId → codeId；放 Room 级（服务器权威模拟将来直接复用） */
137	  private npcCodes = new Map<number, number>();
138	  private npcCodeSeq = 1;
139	  /** section 编码缓存（P2.1）：条带 key → 完整帧；插入序即 LRU。
140	   *  双上限：512 条带 / 32MB（最坏全异态条带 ~52KB，纯条数上限不够——review S5） */
141	  private stripCache = new Map<string, Uint8Array>();
142	  private stripCacheBytes = 0;
143	  private static readonly STRIP_CACHE_MAX_BYTES = 32 * 1024 * 1024;
144	
145	  /** 缓存淘汰至双上限内（插入后调用；Map 插入序 = LRU 序） */
146	  private stripCacheEvict() {
147	    while (this.stripCache.size > 512 || this.stripCacheBytes > Room.STRIP_CACHE_MAX_BYTES) {
148	      const oldest = this.stripCache.keys().next().value as string | undefined;
149	      if (oldest === undefined) break;
150	      const f = this.stripCache.get(oldest)!;
151	      this.stripCache.delete(oldest);
152	      this.stripCacheBytes -= f.length;
153	    }
154	  }
155	
156	  constructor(public world: World) {
157	    this.opts = { code: '', name: world.name, publicRoom: true, protectTiles: false, protectItems: false, hostToken: '', maxPlayers: MAX_PLAYERS };
158	  }
159	
160	  /** SSC 角色档加载器（--ssc 启用时由 index.ts 注入；进场时下发 msg201） */
161	  sscLoad: SscLoader | null = null;
162	
163	  get st() { return this.world.store; }
164	  get onlineCount() { let n = 0; for (const c of this.clients) if (c.state >= 10) n++; return n; }
165	
166	  private allocSlot(): number {
167	    // 逻辑上限只约束分配边界；slotUsed 数组保持 255 物理上限（重连复位可能 ≥ 逻辑上限）
168	    for (let i = 0; i < this.opts.maxPlayers; i++) if (!this.slotUsed[i]) { this.slotUsed[i] = true; return i; }
169	    return -1;
170	  }
171	
172	  /** msg23 合法来源（房主权威；P5 服务器权威模拟时改为 `this.sim ? false : c.isHost`） */
173	  private npcAuthority(c: RoomClient): boolean { return c.isHost; }
174	
175	  /** msg42 转发目标（现 = 房主单播；P5 服务器权威时 = 本 Room 结算，无转发） */
176	  private strikeTarget(): RoomClient | null {
177	    for (const c of this.clients) if (c.isHost && c.state >= 10) return c;
178	    return null;
179	  }
180	
181	  /** 入队发送（P1.3 合包：不再直接 ws.send；flushOutbox 统一拼发）。
182	   *  返回是否入队成功（背压丢弃返回 false——调用方据此决定是否标记"已下发"类状态，
183	   *  见 msg23 短码 known 标记：丢帧后必须能重发全量，否则 NPC 对该端永久隐身） */
184	  send(c: RoomClient, frame: Uint8Array, prio = 0): boolean {
185	    if (c.ws.readyState !== WebSocket.OPEN) return false;
186	    const b = c.ws.bufferedAmount;
187	    if (b > c.stats.bufferedMax) c.stats.bufferedMax = b;
188	    if (b > SEND_BUFFER_LIMIT) {
189	      if (prio === 0) {
190	        // review ③/S3：prio=0 世界状态帧（tile/箱/时钟）不可静默丢——丢了无重放机制，
191	        // 客户端世界永久分叉。持续 >4MB = 慢端，直接带原因断连（重连全量拉条带自愈）
192	        this.kick(c, '网络拥堵（发送缓冲持续超限），请检查网络后重连');
193	        return false;
194	      }
195	      c.stats.sendDrops++;
196	      if (prio >= 1) c.stats.lowDrops++;
197	      this.roomStats.sendDrops++;
198	      return false;
199	    }
200	    if (b > LOW_BUFFER_LIMIT && prio >= 1) {
201	      c.stats.sendDrops++;
202	      c.stats.lowDrops++;
203	      this.roomStats.sendDrops++;
204	      return false;
205	    }
206	    c.stats.outBytes += frame.length;
207	    this.roomStats.outBytes += frame.length;
208	    const h = this.roomStats.msgHist.get(frame[2]);
209	    if (h) { h.n++; h.bytes += frame.length; } else this.roomStats.msgHist.set(frame[2], { n: 1, bytes: frame.length });
210	    c.outbox.push(frame);
211	    return true;
212	  }
213	
214	  /** 冲洗合包队列：每客户端拼接为尽量少的 WS 消息（FLUSH_SLICE 切片防超 maxPayload） */
215	  flushOutbox() {
216	    for (const c of this.clients) {
217	      const ob = c.outbox;
218	      if (!ob.length) continue;
219	      c.outbox = [];
220	      if (c.ws.readyState !== WebSocket.OPEN) continue;
221	      let start = 0, size = 0;
222	      for (let i = 0; i < ob.length; i++) {
223	        size += ob[i].length;
224	        if (size < FLUSH_SLICE && i < ob.length - 1) continue;
225	        const total = size;
226	        const joined = new Uint8Array(total);
227	        let off = 0;
228	        for (let k = start; k <= i; k++) { joined.set(ob[k], off); off += ob[k].length; }
229	        c.ws.send(joined);
230	        start = i + 1;
231	        size = 0;
232	      }
233	    }
234	  }
235	
236	  broadcast(frame: Uint8Array, except?: RoomClient, prio = 0) {
237	    for (const c of this.clients) {
238	      if (c === except || c.state < 10) continue;
239	      this.send(c, frame, prio);
240	    }
241	  }
242	
243	  /** 踢出：**直接 ws.send 旁路背压与合包**（饱和时 outbox 路径可能丢 Kick 帧，
244	   *  客户端只见断连不见原因——review 建议；单帧极小无放大风险），随后 close */
245	  private kick(c: RoomClient, reason: string) {
246	    try {
247	      if (c.ws.readyState === WebSocket.OPEN) c.ws.send(new NetWriter(Msg.Kick).str(reason).finish());
248	    } catch { /* 已关闭 */ }
249	    c.ws.close();
250	  }
251	
252	  /** AOI 定向广播（P1.1）：只发给距 (x,y) 切比雪夫 ≤ radius 的在局客户端。
253	   *  盲端（位置过期，见 aoiBlind）跳过并计数 stalePos。 */
254	  private broadcastAt(x: number, y: number, radius: number, frame: Uint8Array, except?: RoomClient, prio = 0) {
255	    const now = Date.now();
256	    for (const c of this.clients) {
257	      if (c === except || c.state < 10) continue;
258	      if (now - c.lastPosAt > AOI_STALE_MS) { this.roomStats.stalePos++; continue; }
259	      if (Math.abs(c.lastX - x) <= radius && Math.abs(c.lastY - y) <= radius) this.send(c, frame, prio);
260	    }
261	  }
262	
263	  /** 接收端是否"位置未知/过期"（盲端）。
264	   *  盲端语义 = **跳过实体广播**（曾用"全视野兜底"，实测在服务器饱和时形成放大循环：
265	   *  msg13 处理滞后 → 判盲 → 全量灌流 → 更饱和。盲端本就在滞后，停发实体让它先追平，
266	   *  msg13 是 prio=0 小帧必达，位置恢复后自动重新入场）。新进房客户端在首个 msg13 前
267	   *  也走此语义——实体晚一两秒出现，无害。 */
268	  private aoiBlind(c: RoomClient, now: number): boolean {
269	    return now - c.lastPosAt > AOI_STALE_MS;
270	  }
271	
272	  /** review M3 盲端免伤滥用门禁：盲端跳过实体广播 ⇒ 傀儡表空 ⇒ 免疫一切 NPC/弹幕伤害，
273	   *  而客户端的独立 Ping 心跳让 120s 看门狗永不触发——停发 msg13 即可持续免伤。
274	   *  对策：位置中断 >15s（AOI 盲阈值 +10s）仍发**操作类**消息 = 协议上不可伪装的异常
275	   *  （合法后台挂机页不发任何操作——fixedUpdate 停转），踢出。 */
276	  private blindAbuser(c: RoomClient): boolean {
277	    return c.state >= 10 && c.lastPosAt > 0 && Date.now() - c.lastPosAt > AOI_STALE_MS + 10_000;
278	  }
279	
280	  /** 上行限流阈值（①，docs §6.2 承诺兑现）：每客户端每秒 per-msgId 包数上限，
281	   *  取合法峰值的 3-6 倍——正常玩法不可能触达，触达即恶意/故障客户端 */
282	  private static readonly RATE_LIMIT: Record<number, number> = {
283	    [Msg.PlayerState]: 90,      // 合法 ≈15Hz + 控制位变化即时发
284	    [Msg.TileBatch]: 180,       // 合法 ≤60 包/s（挖掘高峰逐 tick 冲洗）
285	    [Msg.SyncNPC]: 60,          // 合法 15Hz
286	    [Msg.SyncProjectile]: 60,   // 合法 15Hz
287	    [Msg.ProjDespawn]: 60,      // 消亡批量与快照同频
288	    [Msg.SyncItem]: 60,         // 攒批后每秒个位数
289	    [Msg.SyncPlayerItem]: 30,   // 差分 250ms + 进房全量 dump
290	    [Msg.NetModules]: 30,       // 聊天
291	    [Msg.StrikeNPC]: 120,       // 多重命中瞬时峰
292	  };
293	
294	  /** 限流检查：false = 超限（调用方踢出） */
295	  private rateCheck(c: RoomClient, msgId: number): boolean {
296	    const sec = Math.floor(Date.now() / 1000);
297	    if (c.rateSecond !== sec) { c.rateSecond = sec; c.rateCounts.fill(0); }
298	    const limit = Room.RATE_LIMIT[msgId];
299	    if (limit === undefined) return true;
300	    return ++c.rateCounts[msgId] <= limit;
301	  }
302	
303	  /** 连接建立后首消息（Hello 带 roomCode/hostToken 由路由层校验后调用） */
304	  handle(c: RoomClient, msgId: number, r: NetReader) {
305	    if (c.state < 1 && msgId !== Msg.Hello) return; // S2 状态门禁
306	    if (!this.rateCheck(c, msgId)) { this.kick(c, '发送频率超限'); return; }
307	    c.lastSeen = 0;
308	    switch (msgId) {
309	      case Msg.Hello: {
310	        if (c.state >= 1) { this.kick(c, '重复握手'); return; }
311	        const magic = r.str();
312	        const ver = r.u16();
313	        c.name = r.str();
314	        if (magic !== PROTO_MAGIC || ver !== PROTO_VER) {
315	          this.kick(c, `协议不匹配（期望 ${PROTO_MAGIC} v${PROTO_VER}）`);
316	          return;
317	        }
318	        // 房主判定：URL token（路由层 newClient 传入）优先；无则消息内 token 兜底。
319	        // 无主房（服务器 --world 载入，hostToken=''）：首位进房者为房主（NPC 权威源）
320	        const msgToken = (() => { try { return r.str(); } catch { return ''; } })();
321	        const token = c.urlToken || msgToken;
322	        if (!this.hostJoined && ((token && token === this.opts.hostToken) || this.opts.hostToken === '')) {
323	          c.isHost = true;
324	          this.hostJoined = true;
325	          // 房主交接公告（review ⑥）：常驻房移交/房主重连时告知在场者 NPC 权威归位
326	          this.broadcast(this.serverNotice(`「${c.name}」已成为房主（NPC 模拟恢复）`));
327	        }
328	        // v3 重连：resumedSlot ≥ 0 = 断线复位（同 slot，跳过分配）。
329	        // 认领制：Hello 成功才是凭据的真正消费点（删条目；61s 超时回调见条目已删即不再释放）。
330	        // review S2：迟到 Hello 须复核条目仍在——认领后超时回调已删条目放 slot 的竞态下，
331	        // 无条件复位会与新玩家双占同一 slot
332	        let slot = -1;
333	        if (c.resumedSlot >= 0 && c.session && this.sessions.has(c.session)) {
334	          slot = c.resumedSlot;
335	          c.resumedSlot = -1;
336	          this.slotUsed[slot] = true;
337	          c.claimedSession = false;
338	          this.sessions.delete(c.session);
339	        } else {
340	          c.resumedSlot = -1;
341	          slot = this.allocSlot();
342	          if (slot < 0) { this.kick(c, '房间已满'); return; }
343	        }
344	        c.slot = slot;
345	        c.state = 1;
346	        if (!c.session) c.session = randomUUID();
347	        this.send(c, new NetWriter(Msg.PlayerSlot).u8(c.slot).str(c.session).finish());
348	        return;
349	      }
350	      case Msg.RequestWorldData: {
351	        if (c.slot < 0) return;
352	        c.state = 2;
353	        this.send(c, this.worldDataFrame());
354	        return;
355	      }
356	      case Msg.SpawnTileData: {
357	        if (c.slot < 0) return;
358	        const x = r.i32(), y = r.i32();
359	        this.sendStrips(c, x, y);
360	        this.send(c, new NetWriter(Msg.PlayerSpawn).u8(c.slot).i32(this.world.spawnX).i32(this.world.spawnY).finish());
361	        // 进场：向房间广播 + 向新客户端下发策略与在场玩家
362	        this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(true).str(c.name).finish());
363	        // 加入公告（原版 NetMessage.cs:2931 Lang.mp[19] 广播、排除本人、色 (255,240,20)）
364	        this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(true).finish());
365	        this.sendPolicy(c);
366	        // v6 SSC：--ssc 启用且有服务器档 → 进场即下发（客户端应用覆盖本地角色）
367	        if (this.sscLoad) {
368	          const rec = this.sscLoad(c.name);
369	          if (rec) this.send(c, new NetWriter(Msg.SscSync).str(rec).finish());
370	        }
371	        for (const other of this.clients) {
372	          if (other === c || other.state < 10) continue;
373	          this.send(c, new NetWriter(Msg.PlayerActive).u8(other.slot).bool(true).str(other.name).finish());
374	          this.send(c, new NetWriter(Msg.SyncPlayer).u8(other.slot).str(other.appearance).finish());
375	          // 在场玩家物品快照全量下发（msg5；手持/盔甲/挥舞渲染依赖）
376	          const entries: Array<{ playerSlot: number; container: ItemContainer; itemSlot: number; itemId: number; stack: number }> = [];
377	          const bags = [other.items.inv, other.items.armor, other.items.dye] as const;
378	          for (let ci = 0; ci < 3; ci++) {
379	            for (let i = 0; i < bags[ci].length; i++) {
380	              const it = bags[ci][i];
381	              if (it) entries.push({ playerSlot: other.slot, container: ci as ItemContainer, itemSlot: i, itemId: it.id, stack: it.stack });
382	            }
383	          }
384	          if (entries.length) this.send(c, writePlayerItems(entries));
385	        }
386	        c.state = 10;
387	        return;
388	      }
389	      case Msg.SyncPlayer: {
390	        r.u8(); // 覆写权威 slot（防冒用）
391	        c.appearance = r.str().slice(0, 4096);
392	        this.broadcast(new NetWriter(Msg.SyncPlayer).u8(c.slot).str(c.appearance).finish(), c);
393	        return;
394	      }
395	      case Msg.SyncPlayerItem: {
396	        if (c.slot < 0) return;
397	        // msg5 物品/装备（对齐原版 SyncPlayerItem）：值域校验 + 快照累积 + 权威 slot 中继
398	        const raw = readPlayerItems(r);
399	        const valid = raw.filter((e) => {
400	          if (e.container > 2) return false;
401	          if (e.itemSlot >= INV_SYNC_SIZES[e.container]) return false;
402	          if (e.itemId >= ITEM_DEFS.length) return false; // S5 值域
403	          return true;
404	        });
405	        for (const e of valid) {
406	          const arr = e.container === ItemContainer.Slots ? c.items.inv
407	            : e.container === ItemContainer.Armor ? c.items.armor : c.items.dye;
408	          arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: Math.min(e.stack, ITEM_DEFS[e.itemId]?.maxStack ?? 9999) } : null;
409	        }
410	        if (valid.length) {
411	          this.broadcast(writePlayerItems(valid.map((e) => ({ ...e, playerSlot: c.slot }))), c);
412	        }
413	        return;
414	      }
415	      case Msg.PlayerState: {
416	        if (c.state < 10) return;
417	        // v2 布局（对齐原版 msg13）：slot(丢弃防冒用) + ctrlBits + flagBits + selectedItem
418	        // + position(左上) [+velocity 若 flagBits[2]]——原样中继，仅覆写权威 slot
419	        r.u8();
420	        const ctrl = r.u8(), flag = r.u8(), sel = r.u8();
421	        const x = r.f32(), y = r.f32();
422	        let vx = 0, vy = 0;
423	        if (flag & 4) { vx = r.f32(); vy = r.f32(); }
424	        // S6 NaN 清洗：非法坐标中继会毒化他人客户端的代理物理
425	        if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(vx) || !Number.isFinite(vy)) return;
426	        // P1.1 AOI：顺带记录发送端位置（接收端过滤的基准），零额外解析成本
427	        c.lastX = x; c.lastY = y; c.lastPosAt = Date.now();
428	        const f = new NetWriter(Msg.PlayerState);
429	        f.u8(c.slot);
430	        f.u8(ctrl); f.u8(flag); f.u8(sel);
431	        f.f32(x); f.f32(y);
432	        if (flag & 4) { f.f32(vx); f.f32(vy); }
433	        this.broadcastAt(x, y, AOI_PLAYER, f.finish(), c);
434	        return;
435	      }
436	      case Msg.TileBatch: {
437	        if (c.state < 10) return;
438	        if (this.blindAbuser(c)) { this.kick(c, '位置同步中断'); return; } // M3
439	        const ops = readTileBatch(r);
440	        // 破坏保护（服务端权威）：非房主整包拒绝——原版无此机制，属我们 v3 房间制策略
441	        if (this.opts.protectTiles && !c.isHost) {
442	          // 拒绝并回发权威快照纠正（对齐原版 SendTileSquare 纠正语义，防客户端乐观预测残留）
443	          for (const o of ops.slice(0, 8)) this.send(c, this.correctionFrame(o.x, o.y));
444	          return;
445	        }
446	        // review S4：先滤掉越界/值域非法的 op 再应用与广播——原实现 apply 跳过但
447	        // broadcast 原样转发，非法 tile id 会污染其他客户端世界（TILE_DEFS[type] undefined）
448	        const valid = ops.filter((o) =>
449	          o.x >= 0 && o.y >= 0 && o.x < this.st.w && o.y < this.st.h
450	          && !(o.a === TileOpAction.SetTile && o.v >= TILE_DEFS.length)
451	          && !(o.a === TileOpAction.SetWall && o.v > 366)
452	          && !(o.a === TileOpAction.SetSlope && o.v > 4));
453	        if (!valid.length) return;
454	        this.applyTileOps(valid);
455	        this.broadcast(writeTileBatch(valid), c);
456	        return;
457	      }
458	      case Msg.NetModules: {
459	        const moduleId = r.u16();
460	        if (moduleId === NetModule.Text) {
461	          const text = r.str();
462	          if (!text || text.length > 200) return;
463	          const f = new NetWriter(Msg.NetModules);
464	          f.u16(NetModule.Text);
465	          f.u8(c.slot);
466	          f.str(text);
467	          f.u8(255); f.u8(220); f.u8(120);
468	          this.broadcast(f.finish());
469	        }
470	        return;
471	      }
472	      case Msg.RequestChestOpen: {
473	        if (c.state < 10) return;
474	        // msg31（原版 RequestChestOpen）：按锚点找箱 → 全量下发内容（msg32）。
475	        // 访客本地 chests 为空（msg7 不传），内容唯一权威 = 服务器（存档带入）
476	        const x = r.i32(), y = r.i32();
477	        // 邻域匹配（±1 tile）：客户端点击箱体任意一格都能命中锚点（findChestNear 语义）
478	        const idx = this.world.chests.findIndex((ch) => Math.abs(ch.x - x) <= 1 && Math.abs(ch.y - y) <= 1);
479	        if (idx < 0) return;
480	        this.send(c, this.chestFrame(idx, -1));
481	        return;
482	      }
483	      case Msg.SyncChestItem: {
484	        if (c.state < 10) return;
485	        if (this.blindAbuser(c)) { this.kick(c, '位置同步中断'); return; } // M3
486	        // msg32 上行（槽位编辑）：protectItems 非房主整包拒绝 + 权威内容回发纠正
487	        const chestIdx = r.u16();
488	        const cx = r.i32(), cy = r.i32();
489	        void cx; void cy;
490	        const n = r.u16();
491	        const slots: Array<{ slot: number; itemId: number; stack: number }> = [];
492	        for (let i = 0; i < n; i++) {
493	          const slot = r.u8(), itemId = r.u16(), stack = r.u16();
494	          if (slot < 10 && itemId < ITEM_DEFS.length) slots.push({ slot, itemId, stack: Math.min(stack, ITEM_DEFS[itemId]?.maxStack ?? 9999) });
495	        }
496	        const chest = this.world.chests[chestIdx];
497	        if (!chest) return;
498	        if (this.opts.protectItems && !c.isHost) {
499	          this.send(c, this.chestFrame(chestIdx, -1)); // 权威纠正
500	          return;
501	        }
502	        for (const s of slots) chest.items[s.slot] = s.itemId ? { id: s.itemId, stack: s.stack } : null;
503	        if (slots.length) {
504	          this.roomStats.chestEdits++; // P3.1 脏标记（review S1：箱子编辑不走 tileOps）
505	          this.broadcast(this.chestFrame(chestIdx, slots[0].slot, c), c);
506	        }
507	        return;
508	      }
509	      case Msg.PlayerLifeMana: {
510	        if (c.state < 10) return;
511	        // msg16（原版 PlayerLifeMana）：客户端权威 HP，服务器中继（覆写权威 slot）
512	        r.u8();
513	        const hp = r.i16(), maxHp = r.i16();
514	        c.hp = hp; c.maxHp = maxHp; // v6 SSC 累积
515	        this.broadcast(new NetWriter(Msg.PlayerLifeMana).u8(c.slot).i16(hp).i16(maxHp).finish(), c);
516	        return;
517	      }
518	      case Msg.SyncNPC: {
519	        // msg23：NPC 快照仅权威源（现=房主，见 npcAuthority）发出。C→S 全量格式不变；
520	        // S→C v4 短码格式（每条 1B flags：bit0=含 key 全量 / bit1=boss）+ AOI 逐接收端过滤
521	        if (c.state < 10 || !this.npcAuthority(c)) return;
522	        const n = r.u16();
523	        if (n > 64) return;
524	        type Entry = { netId: number; code: number; key: string; x: number; y: number; vx: number; vy: number; hp: number; maxHp: number; animT: number; boss: boolean };
525	        const entries: Entry[] = [];
526	        for (let i = 0; i < n; i++) {
527	          const netId = r.u32();
528	          const key = r.str();
529	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
530	          const hp = r.i16(), maxHp = r.i16(), animT = r.u16(), flags = r.u8();
531	          // P1.2 短码分配（表满 60000 清表：全房 npcKnown 一并失效，全量兜底自动重建）
532	          let code = this.npcCodes.get(netId);
533	          if (code === undefined) {
534	            if (this.npcCodes.size >= 60000) {
535	              this.npcCodes.clear();
536	              for (const cl of this.clients) cl.npcKnown.clear();
537	            }
538	            this.npcCodeSeq = (this.npcCodeSeq + 1) & 0xffff;
539	            if (this.npcCodeSeq === 0) this.npcCodeSeq = 1;
540	            code = this.npcCodeSeq;
541	            this.npcCodes.set(netId, code);
542	          }
543	          // S6 NaN 清洗（坐标非法只丢本条快照，字段已全部消费）
544	          if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(vx) || !Number.isFinite(vy)) continue;
545	          entries.push({ netId, code, key: key.slice(0, 64), x, y, vx, vy, hp, maxHp, animT, boss: !!(flags & 1) });
546	        }
547	        const now = Date.now();
548	        // 逐接收端过滤；全员全量时走快速路径（单帧广播，零重编码——簇拥场景的常态）
549	        const targets: Array<{ rc: RoomClient; picked: Entry[] }> = [];
550	        let allFull = true;
551	        for (const rc of this.clients) {
552	          if (rc === c || rc.state < 10) continue;
553	          if (now - rc.lastAoiPrune > AOI_PRUNE_MS) {
554	            rc.lastAoiPrune = now;
555	            for (const [id, t] of rc.aoiNpc) if (now - t > AOI_PRUNE_MS) rc.aoiNpc.delete(id);
556	            for (const [cd, t] of rc.npcKnown) if (now - t > AOI_PRUNE_MS) rc.npcKnown.delete(cd);
557	          }
558	          if (this.aoiBlind(rc, now)) { this.roomStats.stalePos++; continue; } // 盲端：跳过（见 aoiBlind）
559	          const picked: Entry[] = [];
560	          for (const e of entries) {
561	            const dist = Math.max(Math.abs(rc.lastX - e.x), Math.abs(rc.lastY - e.y));
562	            const wasVisible = rc.aoiNpc.has(e.netId);
563	            if (dist > AOI_ENTITY * AOI_OUT_FACTOR) {
564	              if (wasVisible) rc.aoiNpc.delete(e.netId); // 出滞回外径 → 停发（客户端 300 tick 超时清除傀儡）
565	              continue;
566	            }
567	            if (dist > AOI_ENTITY && !wasVisible) continue; // 内外径滞回带且未可见：不入视野
568	            rc.aoiNpc.set(e.netId, now);
569	            picked.push(e);
570	          }
571	          if (!picked.length) continue;
572	          if (picked.length < entries.length) allFull = false;
573	          targets.push({ rc, picked });
574	        }
575	        if (!targets.length) return;
576	        if (allFull) {
577	          // 快速路径：每个目标都收全量条目——但短码标记仍按接收端（known 与否），仅当
578	          // 全员都已知全部 code 时帧内容才一致，此时单帧广播
579	          let allKnown = true;
580	          for (const t of targets) {
581	            for (const e of t.picked) {
582	              if (!t.rc.npcKnown.has(e.code)) { allKnown = false; break; }
583	            }
584	            if (!allKnown) break;
585	          }
586	          if (allKnown) {
587	            const f = new NetWriter(Msg.SyncNPC);
588	            f.u16(entries.length);
589	            for (const e of entries) {
590	              f.u8(e.boss ? 2 : 0); f.u16(e.code);
591	              f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
592	              f.i16(e.hp); f.i16(e.maxHp); f.u16(e.animT);
593	            }
594	            const frame = f.finish();
595	            // 已知集刷新同样晚于 send（与慢路径一致；丢帧只影响 30s 过期时机，自愈）
596	            for (const t of targets) {
597	              if (this.send(t.rc, frame, 1)) {
598	                for (const e of t.picked) t.rc.npcKnown.set(e.code, now);
599	              }
600	            }
601	            return;
602	          }
603	        }
604	        for (const { rc, picked } of targets) {
605	          const out = new NetWriter(Msg.SyncNPC);
606	          out.u16(picked.length);
607	          const learned: number[] = []; // 本帧首次全量下发的 code——仅在入队成功后标记 known
608	          for (const e of picked) {
609	            const known = rc.npcKnown.has(e.code);
610	            out.u8((known ? 0 : 1) | (e.boss ? 2 : 0));
611	            if (known) out.u16(e.code);
612	            else { out.u32(e.netId); out.u16(e.code); out.str(e.key); learned.push(e.code); }
613	            out.f32(e.x); out.f32(e.y); out.f32(e.vx); out.f32(e.vy);
614	            out.i16(e.hp); out.i16(e.maxHp); out.u16(e.animT);
615	          }
616	          // review S2：known 标记必须晚于 send——prio=1 帧被背压丢弃时若已标记，
617	          // 该 NPC 之后只发短码、客户端静默丢弃 → 视野内 NPC 永久隐身。丢帧则不标记，下批重发全量
618	          if (this.send(rc, out.finish(), 1)) {
619	            for (const code of learned) rc.npcKnown.set(code, now);
620	            for (const e of picked) if (rc.npcKnown.has(e.code)) rc.npcKnown.set(e.code, now);
621	          }
622	        }
623	        return;
624	      }
625	      case Msg.SyncItem: {
626	        if (c.state < 10) return;
627	        if (this.blindAbuser(c)) { this.kick(c, '位置同步中断'); return; } // M3
628	        // msg21：掉落物 spawn/take/despawn 中继（netId 已含拥有者 slot 前缀）。
629	        // review M1 注入面收口：op=0（spawn）必须通过属主/key/stack 三重校验——
630	        // 此前任意客户端可伪造 msg21 凭空造物直塞他人背包（拾取无需同意），
631	        // protectItems 只拦 msg32 写箱拦不住这条链
632	        const netId = r.u32();
633	        const op = r.u8();
634	        const f = new NetWriter(Msg.SyncItem);
635	        f.u32(netId); f.u8(op);
636	        if (op === 0) {
637	          const key = r.str();
638	          const stackRaw = r.u16();
639	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
640	          if (!key || key.length > 64 || stackRaw === 0) return;
641	          if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(vx) || !Number.isFinite(vy)) return; // S6
642	          // 属主校验：spawn 的 netId 高 8 位必须 = 发送者 slot（伪造他人 netId = 劫持/冒名）
643	          if ((netId >>> 24) !== c.slot) return;
644	          // key 反查 + maxStack 钳位（未知 key 丢帧——客户端 netApplyItemOp 本就反查不到）
645	          const itemId = ITEM_BY_KEY[key];
646	          if (itemId === undefined) return;
647	          const stack = Math.min(stackRaw, ITEM_DEFS[itemId]?.maxStack ?? 9999);
648	          f.str(key); f.u16(stack);
649	          f.f32(x); f.f32(y); f.f32(vx); f.f32(vy);
650	        } else if (op > 2) return;
651	        this.broadcast(f.finish(), c);
652	        return;
653	      }
654	      case Msg.SyncProjectile: {
655	        if (c.state < 10) return;
656	        // msg27：弹幕快照双向中继（各自弹幕互播）+ P1.1 AOI 滞回过滤；kind>4 整包丢弃防脏流
657	        const n = r.u16();
658	        if (n > 64) return;
659	        type PEntry = { netId: number; kind: number; tag: string; dmg: number; aux: number; x: number; y: number; vx: number; vy: number };
660	        const entries: PEntry[] = [];
661	        for (let i = 0; i < n; i++) {
662	          const netId = r.u32();
663	          const kind = r.u8();
664	          const tag = r.str();
665	          const dmgRaw = r.i16(), aux = r.i16();
666	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
667	          // v5：kind bit7=hostile 原样透传；低 7 位 >8（v6 Boss 锚定弹体 kind 5-8）视为脏数据丢本条。
668	          // review F2/M2：hostile 位合法来源唯一 = 房主 NPC AI——非房主置位即剥除
669	          // （否则任意访客伪造 kind=0x80 + 超高 dmg 可秒杀其他访客 = 无 PvP 开关的强制击杀）；
670	          // dmg 复用 msg42 的 9999 钳位
671	          if ((kind & 0x7f) > 8) continue;
672	          if (!Number.isFinite(x) || !Number.isFinite(y) || !Number.isFinite(vx) || !Number.isFinite(vy)) continue; // S6 NaN 清洗
673	          const effKind = (!c.isHost && (kind & 0x80)) ? kind & 0x7f : kind;
674	          entries.push({ netId, kind: effKind, tag: tag.slice(0, 32), dmg: Math.max(-32768, Math.min(9999, dmgRaw)), aux, x, y, vx, vy });
675	        }
676	        const now = Date.now();
677	        // 逐接收端过滤 + 全员全量快速路径（msg27 无短码，全量时帧内容一致 → 单帧广播零重编码）
678	        const targets: Array<{ rc: RoomClient; picked: PEntry[] }> = [];
679	        let allFull = true;
680	        for (const rc of this.clients) {
681	          if (rc === c || rc.state < 10) continue;
682	          if (now - rc.lastAoiPrune > AOI_PRUNE_MS) {
683	            rc.lastAoiPrune = now;
684	            for (const [id, t] of rc.aoiProj) if (now - t > AOI_PRUNE_MS) rc.aoiProj.delete(id);
685	          }
686	          if (this.aoiBlind(rc, now)) { this.roomStats.stalePos++; continue; } // 盲端：跳过
687	          const picked: PEntry[] = [];
688	          for (const e of entries) {
689	            const dist = Math.max(Math.abs(rc.lastX - e.x), Math.abs(rc.lastY - e.y));
690	            const wasVisible = rc.aoiProj.has(e.netId);
691	            if (dist > AOI_ENTITY * AOI_OUT_FACTOR) {
692	              if (wasVisible) rc.aoiProj.delete(e.netId);
693	              continue;
694	            }
695	            if (dist > AOI_ENTITY && !wasVisible) continue;
696	            rc.aoiProj.set(e.netId, now);
697	            picked.push(e);
698	          }
699	          if (!picked.length) continue;
700	          if (picked.length < entries.length) allFull = false;
701	          targets.push({ rc, picked });
702	        }
703	        if (!targets.length) return;
704	        if (allFull) {
705	          const f = new NetWriter(Msg.SyncProjectile);
706	          f.u16(entries.length);
707	          for (const e of entries) {
708	            f.u32(e.netId); f.u8(e.kind); f.str(e.tag);
709	            f.i16(e.dmg); f.i16(e.aux);
710	            f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
711	          }
712	          const frame = f.finish();
713	          for (const t of targets) this.send(t.rc, frame, 1);
714	          return;
715	        }
716	        for (const { rc, picked } of targets) {
717	          const f = new NetWriter(Msg.SyncProjectile);
718	          f.u16(picked.length);
719	          for (const e of picked) {
720	            f.u32(e.netId); f.u8(e.kind); f.str(e.tag);
721	            f.i16(e.dmg); f.i16(e.aux);
722	            f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
723	          }
724	          this.send(rc, f.finish(), 1);
725	        }
726	        return;
727	      }
728	      case Msg.ProjDespawn: {
729	        // v6 msg28：弹幕消亡批量中继（全房广播——未知 netId 接收端为无主傀儡自动忽略；
730	        // 丢弃由接收端超时清扫兜底，走 prio=1）
731	        if (c.state < 10) return;
732	        const n = r.u16();
733	        if (n > 64) return;
734	        const f = new NetWriter(Msg.ProjDespawn);
735	        f.u16(n);
736	        for (let i = 0; i < n; i++) f.u32(r.u32());
737	        this.broadcast(f.finish(), c, 1);
738	        return;
739	      }
740	      case Msg.StrikeNPC: {
741	        if (c.state < 10) return;
742	        if (this.blindAbuser(c)) { this.kick(c, '位置同步中断'); return; } // M3
743	        // msg42：访客打击 → 定向转发权威结算端（strikeTarget）；dmg 钳 9999 防刷
744	        const netId = r.u32();
745	        const dmg = r.i16();
746	        const kbx = r.f32(), kby = r.f32();
747	        const target = this.strikeTarget();
748	        if (target) {
749	          this.send(target, new NetWriter(Msg.StrikeNPC).u32(netId).i16(Math.max(-32768, Math.min(9999, dmg))).f32(kbx).f32(kby).finish());
750	        }
751	        return;
752	      }
753	      case Msg.Ping: {
754	        const ts = r.f64();
755	        this.send(c, new NetWriter(Msg.Ping).f64(ts).finish());
756	        return;
757	      }
758	      default:
759	        return;
760	    }
761	  }
762	
763	  /** 房间策略下发（RoomPolicy）：客户端据此门禁 UI。v4 尾部追加 u16 maxPlayers */
764	  sendPolicy(c: RoomClient) {
765	    this.send(c, new NetWriter(Msg.RoomPolicy)
766	      .str(this.opts.code)
767	      .str(this.opts.name)
768	      .bool(c.isHost)
769	      .bool(this.opts.protectTiles)
770	      .bool(this.opts.protectItems)
771	      .u16(this.opts.maxPlayers)
772	      .finish());
773	  }
774	
775	  /** 箱子内容帧（msg32）。full=-1 全量下发；否则只带变更槽（最小帧）。
776	   *  广播方向除编辑者本人——编辑者本地已生效（乐观 UI） */
777	  chestFrame(chestIdx: number, full: number, except?: RoomClient): Uint8Array {
778	    const chest = this.world.chests[chestIdx];
779	    const w = new NetWriter(Msg.SyncChestItem);
780	    w.u16(chestIdx);
781	    w.i32(chest.x); w.i32(chest.y);
782	    const from = full === -1 ? 0 : full;
783	    const to = full === -1 ? chest.items.length : from + 1;
784	    w.u16(to - from);
785	    for (let i = from; i < to; i++) {
786	      const it = chest.items[i];
787	      w.u8(i);
788	      w.u16(it?.id ?? 0);
789	      w.u16(it?.stack ?? 0);
790	    }
791	    void except;
792	    return w.finish();
793	  }
794	
795	  /** 权威 tile 快照纠正（单格） */
796	  private correctionFrame(x: number, y: number): Uint8Array {
797	    const ops: TileOp[] = [];
798	    if (x >= 0 && y >= 0 && x < this.st.w && y < this.st.h) {
799	      const i = this.st.idx(x, y);
800	      ops.push({ a: TileOpAction.SetTile, x, y, v: this.st.type[i], fx: this.st.frameX[i], fy: this.st.frameY[i] });
801	    }
802	    return writeTileBatch(ops);
803	  }
804	
805	  /** 服务器系统公告（Text 模块 slot=255——客户端直显无名字前缀；色对齐加入/离开公告） */
806	  serverNotice(text: string): Uint8Array {
807	    const f = new NetWriter(Msg.NetModules);
808	    f.u16(NetModule.Text);
809	    f.u8(255);
810	    f.str(text);
811	    f.u8(255); f.u8(240); f.u8(20);
812	    return f.finish();
813	  }
814	
815	  disconnect(c: RoomClient) {
816	    this.clients.delete(c);
817	    // 房主离开公告（review ⑥）：NPC 模拟随之中断——此前完全静默，访客只见"怪全没了"
818	    if (c.isHost) {
819	      this.broadcast(this.serverNotice(`房主「${c.name}」已离开，NPC 模拟暂停；房主重连后恢复`));
820	    }
821	    // 认领了 session 但没完成 Hello 就断线 → 释放认领（重试窗口内可再连；超时回调兜底释放 slot）
822	    if (c.state < 1 && c.claimedSession) {
823	      const s = this.sessions.get(c.session);
824	      if (s) s.claimed = false;
825	      c.claimedSession = false;
826	    }
827	    if (c.slot >= 0) {
828	      // v3 重连：在局玩家断开 → session 保留 60s，slot 占位防新人顶号；过期释放。
829	      // review S1：超时回调按**条目世代**判等——同键新条目（断-连-再断）不能被旧定时器误删
830	      if (c.state >= 10 && c.session) {
831	        const entry = {
832	          slot: c.slot, name: c.name, appearance: c.appearance,
833	          until: Date.now() + 60_000, claimed: false,
834	        };
835	        this.sessions.set(c.session, entry);
836	        const sess = c.session;
837	        const slot = c.slot;
838	        setTimeout(() => {
839	          // 世代不符（期间已被 Hello 消费或被新断线条目替换）→ 不动新条目
840	          if (this.sessions.get(sess) !== entry) return;
841	          this.sessions.delete(sess);
842	          this.slotUsed[slot] = false;
843	        }, 61_000).unref?.();
844	      } else {
845	        this.slotUsed[c.slot] = false;
846	      }
847	      this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(false).str('').finish());
848	      // 离开公告（原版 NetMessage.cs:2950-2954：先广播 14 再 Lang.mp[20]，含强制退出/掉线）
849	      this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(false).finish());
850	    }
851	    if (c.isHost) this.hostJoined = false;
852	  }
853	
854	  /** 断线重连识别（index.ts 从 URL ?session= 注入）：命中 → 复位 slot/身份，Hello 跳过分配。
855	   *  认领制：只标记 claimed（防并发双认领），**不删条目**——条目在 Hello 成功时消费；
856	   *  认领后断线由 disconnect 释放认领 */
857	  resumeSession(c: RoomClient, session: string): boolean {
858	    const s = this.sessions.get(session);
859	    if (!s || s.until <= Date.now() || s.claimed) return false;
860	    s.claimed = true;
861	    c.claimedSession = true;
862	    c.resumedSlot = s.slot;
863	    c.name = s.name;
864	    c.appearance = s.appearance;
865	    c.session = session;
866	    return true;
867	  }
868	
869	  // ---- 世界数据帧（msg7）：对齐 v1 字段集 ----
870	  worldDataFrame(): Uint8Array {
871	    const w = new NetWriter(Msg.WorldData);
872	    w.f64(this.world.clock.timeOfDay);
873	    w.u32(this.world.clock.dayCount);
874	    w.u16(this.st.w); w.u16(this.st.h);
875	    w.i32(this.world.spawnX); w.i32(this.world.spawnY);
876	    w.f32(this.world.groundLevel); w.f32(this.world.rockLevel); w.f32(this.world.lavaLine);
877	    w.i32(this.world.seed);
878	    w.str(this.world.name);
879	    w.bool(this.world.crimson);
880	    w.i32(this.world.dungeonX); w.i32(this.world.dungeonY); w.i32(this.world.jungleX);
881	    const keys = Object.keys(this.world.flags);
882	    w.u16(keys.length);
883	    for (const k of keys) { w.str(k); w.bool(!!this.world.flags[k]); }
884	    return w.finish();
885	  }
886	
887	  // ---- section 流式（出生点 5×5 条带，strip 粒度兴趣管理） ----
888	  sendStrips(c: RoomClient, cx: number, cy: number) {
889	    const st = this.st;
890	    const strips: Array<{ x0: number; y0: number }> = [];
891	    const sx = Math.floor(cx / STRIP_W), sy = Math.floor(cy / STRIP_H);
892	    for (let dy = -2; dy <= 2; dy++) {
893	      for (let dx = -2; dx <= 2; dx++) {
894	        const x0 = (sx + dx) * STRIP_W, y0 = (sy + dy) * STRIP_H;
895	        if (x0 >= 0 && y0 >= 0 && x0 < st.w && y0 < st.h) strips.push({ x0, y0 });
896	      }
897	    }
898	    const fresh = strips.filter((s) => !c.sentStrips.has(`${s.x0},${s.y0}`));
899	    this.send(c, new NetWriter(Msg.StatusText).u16(fresh.length).finish());
900	    for (const s of fresh) {
901	      c.sentStrips.add(`${s.x0},${s.y0}`);
902	      // P2.1 section 编码缓存：命中直发（LRU 提到队尾）；miss 编码入缓存
903	      const key = `${s.x0},${s.y0}`;
904	      let frame = this.stripCache.get(key);
905	      if (frame) {
906	        this.stripCache.delete(key);
907	        this.stripCache.set(key, frame);
908	        this.roomStats.stripHit++;
909	      } else {
910	        frame = encodeStrip(st, { x0: s.x0, y0: s.y0, w: Math.min(STRIP_W, st.w - s.x0), h: Math.min(STRIP_H, st.h - s.y0) });
911	        this.stripCache.set(key, frame);
912	        this.stripCacheBytes += frame.length;
913	        this.stripCacheEvict();
914	        this.roomStats.stripMiss++;
915	      }
916	      this.send(c, frame);
917	    }
918	  }
919	
920	  applyTileOps(ops: TileOp[]) {
921	    const st = this.st;
922	    for (const o of ops) {
923	      if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
924	      // S5 值域校验
925	      if (o.a === TileOpAction.SetTile && o.v >= TILE_DEFS.length) continue;
926	      if (o.a === TileOpAction.SetWall && o.v > 366) continue;
927	      if (o.a === TileOpAction.SetSlope && o.v > 4) continue;
928	      // P2.1：任何落格修改都使其所在条带缓存失效（按条带原点归一化）
929	      {
930	        const sk = `${Math.floor(o.x / STRIP_W) * STRIP_W},${Math.floor(o.y / STRIP_H) * STRIP_H}`;
931	        const sf = this.stripCache.get(sk);
932	        if (sf !== undefined) { this.stripCache.delete(sk); this.stripCacheBytes -= sf.length; }
933	      }
934	      this.roomStats.tileOps++;
935	      switch (o.a) {
936	        case TileOpAction.SetTile:
937	          st.setTileSilent(o.x, o.y, o.v, o.fx, o.fy);
938	          // 箱子 tile 被清除/替换 → 同步清除权威 chests 条目（防陈旧条目被 msg31
939	          // 再次开出 = 物品复制；房主 dumpChest 的掉落已走 msg21 广播）
940	          if (o.v !== CHEST_TILE_ID) {
941	            const ci = this.world.chests.findIndex((ch) => Math.abs(ch.x - o.x) <= 1 && Math.abs(ch.y - o.y) <= 1);
942	            if (ci >= 0) this.world.chests.splice(ci, 1);
943	          }
944	          break;
945	        case TileOpAction.SetWall: st.setWallSilent(o.x, o.y, o.v); break;
946	        case TileOpAction.SetHalfBrick: st.half[st.idx(o.x, o.y)] = o.v ? 1 : 0; break;
947	        case TileOpAction.SetSlope: st.slope[st.idx(o.x, o.y)] = o.v; break;
948	        case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
949	        case TileOpAction.SetWire: st.setWireSilent(o.x, o.y, o.v); break;
950	      }
951	    }
952	  }
953	
954	  newClient(ws: WebSocket, urlToken = ''): RoomClient {
955	    const c: RoomClient = {
956	      ws, parser: new FrameParser(), slot: -1, state: 0, name: '?',
957	      appearance: '{}', lastSeen: 0, isHost: false, sentStrips: new Set(),
958	      session: '', resumedSlot: -1, claimedSession: false,
959	      lastX: -1e9, lastY: -1e9, lastPosAt: 0,
960	      aoiNpc: new Map(), aoiProj: new Map(), npcKnown: new Map(), lastAoiPrune: 0,
961	      outbox: [],
962	      stats: { inBytes: 0, outBytes: 0, bufferedMax: 0, sendDrops: 0, lowDrops: 0 },
963	      rateSecond: 0, rateCounts: new Int32Array(256),
964	      hp: 0, maxHp: 0,
965	      items: {
966	        inv: Array(INV_SYNC_SIZES[0]).fill(null),
967	        armor: Array(INV_SYNC_SIZES[1]).fill(null),
968	        dye: Array(INV_SYNC_SIZES[2]).fill(null),
969	      },
970	    };
971	    if (urlToken) c.urlToken = urlToken;
972	    this.clients.add(c);
973	    return c;
974	  }
975	}
976	

```


---

## 🤖 Assistant · 2026-08-12T08:34:15.836Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/scripts/ | head -50; echo ---; grep -rn \"PROTO_VER\\|protoVer\" ~/Project/GLM/SandboxWorld --include=\"*.ts\" --include=\"*.mjs\" 2>/dev/null | grep -v node_modules | grep -v \"\\.js:\"",
 "description": "List scripts and grep PROTO_VER/protoVer usage"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:16.110Z

**📎 ToolResult**

```
_alphaprobe.mjs
_ascii-frame.mjs
_audit7.mjs
_ballooncheck.mjs
_batprobe.mjs
_beach-probe.mjs
_behavior-smoke.mjs
_behavior2-smoke.mjs
_bestiary-ui.mjs
_biomeaudio.mjs
_biomeflagprobe.mts
_biomeprobe.mjs
_bloodmoon-smoke.mjs
_bootcheck.mjs
_bossprobe.mts
_bowprobe.mjs
_buffprobe.mjs
_cactus3.mjs
_calibrate.mjs
_casterprobe.mjs
_chan.mjs
_chargerprobe.mjs
_chatprobe.mjs
_chestdbg.mjs
_chestshot.mjs
_cmp-guide.mjs
_crab-face.mjs
_critter-hell-probe.mts
_cursor-probe.mjs
_dartdrawprobe.mjs
_dartprobe.mjs
_dartprobe2.mjs
_dartprobe3.mjs
_dbgalpha.mjs
_death-probe.mjs
_dgndbg.mjs
_dirt-probe.mjs
_dukemlprobe.mts
_dummy-probe.mjs
_dungeondtrap.mjs
_dungeonprobe.mjs
_eaterai.mjs
_eaterdbg.mjs
_eaterdbg2.mjs
_eaterpix.mjs
_equip-stats-smoke.mjs
_eye-detect.mjs
_eye2.mjs
_eyeprobe.mjs
_face-detect.mjs
---
~/Project/GLM/SandboxWorld/server/src/room.ts:6:  PROTO_MAGIC, PROTO_VER, Msg, NetModule,
~/Project/GLM/SandboxWorld/server/src/room.ts:314:        if (magic !== PROTO_MAGIC || ver !== PROTO_VER) {
~/Project/GLM/SandboxWorld/server/src/room.ts:315:          this.kick(c, `协议不匹配（期望 ${PROTO_MAGIC} v${PROTO_VER}）`);
~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs:11:import { WebSocket, Writer, PROTO_MAGIC, PROTO_VER, Msg, makeTinySave, spawnServer } from './_netfake.mjs';
~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs:99:        ws.on('open', () => ws.send(new Writer(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(`满员${i}`).str('').finish()));
~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs:17:import { WebSocket, Writer, PROTO_MAGIC, PROTO_VER, Msg, makeTinySave, spawnServer } from './_netfake.mjs';
~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs:86:      ws.send(new Writer(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(`压测${i}`).str('').finish());
~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs:11:export const PROTO_VER = 6;
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts:5:// 编码字段为本仓库简化集（protoVer 门禁，当前 v5——见 PROTO_VER 注释）。
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts:16:export const PROTO_VER = 6;
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts:20:  Hello = 1,          // C→S {magic, protoVer, name, hostToken 兜底}
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:5:  PROTO_MAGIC, PROTO_VER, Msg, NetModule,
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:166:      const hello = new NetWriter(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(name).str(this.hostToken);

```


---

## 🤖 Assistant · 2026-08-12T08:34:17.753Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: protocol.ts line 5 comment says "当前 v5" but PROTO_VER = 6. That's a doc inconsistency (minor, comment stale).

Now read ClientNet.ts, probes, docs, 开服.sh, _netfake.mjs.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:17.864Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts"
}
```


---

## 🤖 Assistant · 2026-08-12T08:34:17.984Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:18.013Z

**📎 ToolResult**

```
1	// 联机探针共享的线协议最小实现（与 game/src/net/protocol.ts 同构；探针专用，勿入 src/）。
2	// _roomprobe.mjs（满员 Kick 等断言）与 _loadprobe.mjs（压测）共用。
3	import { createRequire } from 'node:module';
4	import { fileURLToPath } from 'node:url';
5	
6	const require = createRequire(new URL('../../server/package.json', import.meta.url));
7	export const { WebSocket } = require('ws');
8	export const ROOT = fileURLToPath(new URL('../../', import.meta.url));
9	
10	export const PROTO_MAGIC = 'SW1';
11	export const PROTO_VER = 6;
12	export const Msg = {
13	  Hello: 1, Kick: 2, PlayerSlot: 3, SyncPlayer: 4, SyncPlayerItem: 5, RequestWorldData: 6,
14	  WorldData: 7, SpawnTileData: 8, StatusText: 9, TileSection: 10, PlayerSpawn: 12, PlayerState: 13,
15	  PlayerLifeMana: 16, SyncNPC: 23, SyncProjectile: 27, ProjDespawn: 28, Ping: 154, SscSync: 201,
16	};
17	
18	export class Writer {
19	  constructor(msgId) { this.buf = Buffer.alloc(256); this.len = 3; this.buf[2] = msgId; }
20	  need(n) {
21	    if (this.len + n <= this.buf.length) return;
22	    let cap = this.buf.length;
23	    while (cap < this.len + n) cap *= 2;
24	    const nb = Buffer.alloc(cap);
25	    this.buf.copy(nb, 0, 0, this.len);
26	    this.buf = nb;
27	  }
28	  u8(v) { this.need(1); this.buf.writeUInt8(v & 255, this.len); this.len += 1; return this; }
29	  u16(v) { this.need(2); this.buf.writeUInt16LE(v & 0xffff, this.len); this.len += 2; return this; }
30	  i16(v) { this.need(2); this.buf.writeInt16LE(v, this.len); this.len += 2; return this; }
31	  u32(v) { this.need(4); this.buf.writeUInt32LE(v >>> 0, this.len); this.len += 4; return this; }
32	  i32(v) { this.need(4); this.buf.writeInt32LE(v, this.len); this.len += 4; return this; }
33	  f32(v) { this.need(4); this.buf.writeFloatLE(v, this.len); this.len += 4; return this; }
34	  str(s) { const b = Buffer.from(s, 'utf8'); this.u16(b.length); this.need(b.length); b.copy(this.buf, this.len); this.len += b.length; return this; }
35	  finish() {
36	    if (this.len > 65535) throw new Error('frame too large');
37	    this.buf.writeUInt16LE(this.len, 0);
38	    return this.buf.subarray(0, this.len);
39	  }
40	}
41	
42	/** LEB128 varint（存档 RLE 用；对齐 save/serialize.ts） */
43	export function varint(v) {
44	  const out = [];
45	  let n = v;
46	  for (;;) {
47	    let b = n & 0x7f;
48	    n = Math.floor(n / 128);
49	    if (n > 0) b |= 0x80;
50	    out.push(b);
51	    if (n === 0) return out;
52	  }
53	}
54	
55	/** 构造全空气小世界存档（n×n）：一条 RLE run 覆盖全图 */
56	export function makeTinySave(n = 200) {
57	  const rle = Buffer.from([...varint(n * n - 1), ...varint(0)]).toString('base64');
58	  return JSON.stringify({
59	    format: 'sandboxworld.save', version: 3,
60	    header: {
61	      name: '探针世界', seed: 20260812, width: n, height: n,
62	      spawn: [Math.floor(n / 2), Math.floor(n / 2)], groundLevel: Math.floor(n * 0.3),
63	      rockLevel: Math.floor(n * 0.5), lavaLine: n - 20,
64	      created: Date.now(), playTimeMs: 0,
65	    },
66	    clock: { timeOfDay: 0.3, dayCount: 1 },
67	    tiles: rle, walls: rle, liquid: rle, liquidType: rle,
68	    chests: [], player: { hp: 100, x: 1600, y: 1600, inventory: [], selected: 0 },
69	    npcs: [], flags: {},
70	  });
71	}
72	
73	/** 起 server 子进程（detached 进程组，防"杀 npx 包装留 tsx 孤儿"——2026-08 实踩） */
74	export function spawnServer(port, extraArgs = [], serverDir = null) {
75	  const { spawn } = require('node:child_process');
76	  const path = require('node:path');
77	  const cwd = serverDir ?? path.join(ROOT, 'server');
78	  const server = spawn('npx', ['tsx', 'src/index.ts', '--port', String(port), ...extraArgs], {
79	    cwd, stdio: ['ignore', 'pipe', 'pipe'], detached: true,
80	  });
81	  /** 优雅停机：SIGTERM 直杀直子（npx 级联到 tsx node 子进程；实测组播信号与落盘
82	   *  并发会让服务器静默死亡——组内 esbuild/npx 转发升级疑似 SIGKILL,勿用组播发 TERM）。
83	   *  5s 未退 → 整组 SIGKILL 兜底（防孤儿）。 */
84	  server.killGroup = () => {
85	    try { server.kill('SIGTERM'); } catch { /* 已退 */ }
86	    setTimeout(() => {
87	      if (server.exitCode !== null) return;
88	      try { process.kill(-server.pid, 'SIGKILL'); } catch { try { server.kill('SIGKILL'); } catch { /* 已退 */ } }
89	    }, 5000).unref?.();
90	  };
91	  return server;
92	}
93	

```


---

## 👤 User(sidechain) · 2026-08-12T08:34:18.046Z

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
28	  /** 最近一次 msg13 到达时刻（P1.1 AOI 配套：超时未达 → Game 冻结代理输入防幽灵行走） */
29	  lastFresh: number;
30	}
31	
32	/** 房间策略（S→C RoomPolicy；客户端门禁依据——v3 房间制；v4 尾部 maxPlayers） */
33	export interface RoomPolicyState {
34	  roomCode: string;
35	  roomName: string;
36	  isHost: boolean;
37	  protectTiles: boolean;
38	  protectItems: boolean;
39	  /** 单房人数上限（v4；UI 显示 online/max） */
40	  maxPlayers: number;
41	}
42	
43	/** NPC 快照（msg23；房主权威） */
44	export interface NpcSnap {
45	  netId: number; key: string;
46	  x: number; y: number; vx: number; vy: number;
47	  hp: number; maxHp: number; animT: number;
48	  flags: number; // bit0=boss
49	}
50	
51	/** 弹幕快照（msg27；tag = projId(arrow/weapon) / dart kind / magic color） */
52	export interface ProjSnap {
53	  netId: number; kind: number; tag: string;
54	  dmg: number; aux: number;
55	  x: number; y: number; vx: number; vy: number;
56	}
57	
58	/** 掉落物操作（msg21） */
59	export interface ItemOpMsg {
60	  op: 0 | 1 | 2; netId: number;
61	  key: string; stack: number;
62	  x: number; y: number; vx: number; vy: number;
63	}
64	
65	export interface ClientNetHooks {
66	  /** 世界组装完成（全部初始 strip 到齐 + PlayerSpawn）——Game 进 loadWorld */
67	  onWorldReady: (world: World) => void;
68	  /** 运行期晚到 strip 的落地区域（Game 负责整块标脏 chunk + 小地图） */
69	  onSectionArrived?: (rect: { x0: number; y0: number; w: number; h: number }) => void;
70	  /** 进度（label, p 0..1） */
71	  onProgress?: (label: string, p: number) => void;
72	  /** 聊天 */
73	  onChat?: (text: string, r: number, g: number, b: number) => void;
74	  /** 被踢 */
75	  onKick?: (reason: string) => void;
76	  /** 箱子内容到达/被纠正（服务器权威；Game 负责登记 world.chests 与开面板） */
77	  onChestSync?: (chestIdx: number, x: number, y: number, items: Array<{ id: number; stack: number } | null>) => void;
78	  /** NPC 快照到达（msg23；Game 维护傀儡池） */
79	  onNpcSnapshot?: (snaps: NpcSnap[]) => void;
80	  /** 掉落物操作到达（msg21；Game 维护傀儡/移除本地真掉落） */
81	  onItemOp?: (op: ItemOpMsg) => void;
82	  /** 弹幕快照到达（msg27；Game 维护傀儡池） */
83	  onProjectileSync?: (snaps: ProjSnap[]) => void;
84	  /** 弹幕消亡到达（v6 msg28；Game 即时移除傀儡） */
85	  onProjDespawn?: (netIds: number[]) => void;
86	  /** SSC 角色档到达（v6 msg201，--ssc 启用；Game 应用覆盖本地角色） */
87	  onSSC?: (recordJson: string) => void;
88	  /** 打击到达（msg42；房主权威结算） */
89	  onStrike?: (netId: number, rawDmg: number, kbx: number, kby: number) => void;
90	  /** 远端玩家 HP（msg16 中继） */
91	  onHp?: (slot: number, hp: number, maxHp: number) => void;
92	  /** 房间策略到达（进场时；门禁/提示用） */
93	  onPolicy?: (policy: RoomPolicyState) => void;
94	}
95	
96	export class ClientNet {
97	  active = false;
98	  mySlot = -1;
99	  players = new Map<number, RemotePlayerState>();
100	  /** 房间策略（RoomPolicy 到达前 = 自由房默认） */
101	  policy: RoomPolicyState = { roomCode: '', roomName: '', isHost: false, protectTiles: false, protectItems: false, maxPlayers: 255 };
102	
103	  private ws: WebSocket | null = null;
104	  private parser = new FrameParser();
105	  private hooks: ClientNetHooks;
106	  private game: { player: { appearance?: unknown; inv: { slots: Array<{ id: number; stack: number } | null> } } };
107	  private hostToken = '';
108	
109	  /** 组装中的世界（收到 msg7 建骨架，strip 到齐后交给 onWorldReady） */
110	  private pendingWorld: World | null = null;
111	  private pendingStrips = 0;
112	  private pendingStripsTotal = 0;
113	  private worldDelivered = false;
114	  /** 本地 tile 变更上报队列（TileStore.netReporter 收集） */
115	  private tileQueue: TileOp[] = [];
116	  /** msg23 短码表（v4：codeId → {netId, key}；服务器端分配，全量条目重建） */
117	  private npcCodes = new Map<number, { netId: number; key: string }>();
118	  /** msg21 上行合帧暂存（P1.3：netDropSweep 每 4 tick 逐条发 → 攒到 tick 冲洗拼一条 WS 消息） */
119	  private pendingFrames: Uint8Array[] = [];
120	  private lastStateSent = 0;
121	  private lastSentPos = { x: 0, y: 0 };
122	
123	  constructor(
124	    game: ClientNet['game'],
125	    hooks: ClientNetHooks,
126	  ) {
127	    this.game = game;
128	    this.hooks = hooks;
129	  }
130	
131	  private pingTimer: ReturnType<typeof setInterval> | null = null;
132	
133	  connect(url: string, hostToken = '') {
134	    this.url = url;
135	    this.hostToken = hostToken;
136	    this.connect0(url);
137	  }
138	
139	  /** 底层建连（首连/重连共用） */
140	  private connect0(url: string) {
141	    this.active = true;
142	    let ws: WebSocket;
143	    try {
144	      ws = new WebSocket(url);
145	    } catch (e) {
146	      // R12 修复：非法 URL 同步抛异常 → 转为 reject 语义（onKick）而非穿透调用栈
147	      this.active = false;
148	      this.hooks.onKick?.(`地址无效：${(e as Error).message}`);
149	      return;
150	    }
151	    ws.binaryType = 'arraybuffer';
152	    this.ws = ws;
153	    // R9：独立 30s 心跳——暂停/后台（fixedUpdate 停跑）也不再被服务器 120s 看门狗踢
154	    if (!this.pingTimer) {
155	      this.pingTimer = setInterval(() => {
156	        this.send(new NetWriter(Msg.Ping).f64(performance.now()).finish());
157	      }, 30000);
158	    }
159	    ws.onopen = () => {
160	      // Hello（对齐原版 msg1：版本校验）。连接时 Game.player 可能尚未创建（joinNetGame
161	      // 先连后 loadWorld）——外观名走可选链兜底
162	      const p = this.game.player as { appearance?: { name?: string } } | undefined | null;
163	      const name = p?.appearance?.name ?? '玩家';
164	      // 房主令牌：URL 已带 ?token=（路由层 newClient 注入）——消息内再传一份兜底
165	      // （非房主/旧路径传空串，服务器 try/catch 读不到即跳过）
166	      const hello = new NetWriter(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(name).str(this.hostToken);
167	      this.send(hello.finish());
168	    };
169	    ws.onmessage = (e) => {
170	      this.parser.append(new Uint8Array(e.data as ArrayBuffer));
171	      this.parser.drain((id, r) => this.handle(id, r));
172	    };
173	    ws.onclose = () => {
174	      if (!this.active || this.userClosed) return;
175	      // v3 断线重连（§8.8）：有 session 凭据 → 2s 间隔自动重试 3 次（同 slot 复位）；
176	      // 耗尽或无凭据 → 按原语义 onKick
177	      if (this.session && this.reconnects < 3) {
178	        this.reconnects++;
179	        this.active = false;
180	        setTimeout(() => {
181	          if (this.userClosed) return;
182	          const sep = this.url.includes('?') ? '&' : '?';
183	          this.connect0(`${this.url}${sep}session=${encodeURIComponent(this.session)}`);
184	        }, 2000);
185	        return;
186	      }
187	      this.active = false;
188	      this.hooks.onKick?.('与服务器断开连接');
189	    };
190	    ws.onerror = () => { /* close 跟上 */ };
191	  }
192	
193	  private url = '';
194	  private session = '';
195	  private reconnects = 0;
196	  private userClosed = false;
197	
198	  private send(frame: Uint8Array) {
199	    if (this.ws?.readyState === WebSocket.OPEN) this.ws.send(frame);
200	  }
201	
202	  /** 请求玩家位置周围的 strip（R3 移动续传：跨条带边界时由 Game 调用） */
203	  requestSection(cx: number, cy: number) {
204	    this.send(new NetWriter(Msg.SpawnTileData).i32(Math.floor(cx)).i32(Math.floor(cy)).finish());
205	  }
206	
207	  disconnect() {
208	    this.userClosed = true;
209	    this.active = false;
210	    if (this.pingTimer) { clearInterval(this.pingTimer); this.pingTimer = null; }
211	    this.ws?.close();
212	    this.ws = null;
213	  }
214	
215	  // ================= 收包分发（对齐原版 MessageBuffer switch） =================
216	
217	  private handle(msgId: number, r: NetReader) {
218	    switch (msgId) {
219	      case Msg.Kick: {
220	        this.hooks.onKick?.(r.str());
221	        this.disconnect();
222	        return;
223	      }
224	      case Msg.PlayerSlot: {
225	        this.mySlot = r.u8();
226	        this.invDumpPending = true; // 物品全量 dump 时机：slot 分配后首 tick
227	        // v3：session 凭据（重连用）；重连场景复位 join 状态以重走世界组装
228	        const sess = (() => { try { return r.str(); } catch { return ''; } })();
229	        if (sess) {
230	          if (this.worldDelivered) {
231	            // 断线重连：世界将重新组装下发（pendingWorld 复位）
232	            this.worldDelivered = false;
233	            this.pendingWorld = null;
234	            this.pendingStrips = 0;
235	          }
236	          this.session = sess;
237	          this.reconnects = 0;
238	        }
239	        // 全量上传自身（对齐原版 msg3 后立刻 SyncPlayer + RequestWorldData）
240	        const p2 = this.game.player as { appearance?: unknown } | undefined | null;
241	        const app = JSON.stringify(p2?.appearance ?? {});
242	        this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(app).finish());
243	        this.send(new NetWriter(Msg.RequestWorldData).finish());
244	        return;
245	      }
246	      case Msg.WorldData: {
247	        this.pendingWorld = this.readWorldData(r);
248	        return;
249	      }
250	      case Msg.StatusText: {
251	        this.pendingStrips = r.u16();
252	        this.pendingStripsTotal = Math.max(1, this.pendingStrips);
253	        // 仅初始组装期上报进度：进世界后 R3 移动续传也会触发 StatusText（fresh=0），
254	        // 无条件回调会把已关闭的全屏进度遮罩重新拉起 → "永久卡在接收世界数据"
255	        if (!this.worldDelivered) this.hooks.onProgress?.('接收世界数据', 0);
256	        return;
257	      }
258	      case Msg.TileSection: {
259	        // R3 修复：初始组装期写入 pendingWorld；运行期（已进世界）晚到的 strip
260	        // 直写 gameWorld 并返回区域（调用方负责整块标脏——见 requestSection 回调）
261	        if (this.pendingWorld) {
262	          decodeStrip(this.pendingWorld.store, r);
263	          if (this.pendingStrips > 0) {
264	            this.pendingStrips--;
265	            // 进度按剩余比例推进（此前恒 0.5 不动）
266	            this.hooks.onProgress?.('接收世界数据', this.pendingStripsTotal > 0 ? 1 - this.pendingStrips / this.pendingStripsTotal : 0.5);
267	          }
268	        } else if (this.gameWorld) {
269	          const rect = decodeStrip(this.gameWorld.store, r);
270	          if (rect && this.hooks.onSectionArrived) this.hooks.onSectionArrived(rect);
271	        }
272	        return;
273	      }
274	      case Msg.PlayerSpawn: {
275	        const slot = r.u8();
276	        const sx = r.i32(), sy = r.i32();
277	        if (slot === this.mySlot && !this.worldDelivered && this.pendingWorld) {
278	          this.worldDelivered = true;
279	          this.pendingWorld.spawnX = sx;
280	          this.pendingWorld.spawnY = sy;
281	          this.hooks.onProgress?.('完成', 1);
282	          this.hooks.onWorldReady(this.pendingWorld);
283	          this.pendingWorld = null;
284	          // R2 修复：进世界后重发外观——连接时 player 可能尚未创建/外观未应用，
285	          // 此刻 Game.player 必然就绪（onWorldReady 已被 loadWorld 消费）
286	          const p3 = this.game.player as { appearance?: unknown } | undefined;
287	          if (p3?.appearance) {
288	            this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p3.appearance)).finish());
289	          }
290	        }
291	        return;
292	      }
293	      case Msg.PlayerActive: {
294	        const slot = r.u8();
295	        const active = r.bool();
296	        const name = r.str();
297	        let p = this.players.get(slot);
298	        if (active) {
299	          if (!p) {
300	            p = {
301	              slot, name, appearance: '{}', x: 0, y: 0, vx: 0, vy: 0,
302	              up: false, down: false, left: false, right: false, jump: false, useItem: false,
303	              facing: 1, selectedItem: 0, dead: false, fresh: false, active: true, lastFresh: 0,
304	            };
305	            this.players.set(slot, p);
306	          }
307	          p.active = true;
308	          p.name = name || p.name;
309	        } else if (p) {
310	          p.active = false;
311	        }
312	        return;
313	      }
314	      case Msg.SyncPlayer: {
315	        const slot = r.u8();
316	        const appearance = r.str();
317	        const p = this.players.get(slot);
318	        if (p) p.appearance = appearance;
319	        return;
320	      }
321	      case Msg.SyncPlayerItem: {
322	        // 远端物品/装备（msg5）：Game 侧拷入 proxy.inv 驱动手持/盔甲/挥舞渲染
323	        const entries = readPlayerItems(r);
324	        this.applyRemoteItems(entries.filter((e) => e.playerSlot !== this.mySlot));
325	        return;
326	      }
327	      case Msg.PlayerState: {
328	        // v2 布局（对齐原版 msg13）：slot + ctrlBits + flagBits + selectedItem + pos [+vel]
329	        const slot = r.u8();
330	        const ctrl = r.u8();
331	        const flag = r.u8();
332	        const sel = r.u8();
333	        const x = r.f32(), y = r.f32();
334	        let vx = 0, vy = 0;
335	        if (flag & 4) { vx = r.f32(); vy = r.f32(); } // flagBits[2] = hasVelocity
336	        let p = this.players.get(slot);
337	        if (!p) {
338	          p = {
339	            slot, name: `玩家${slot}`, appearance: '{}',
340	            x, y, vx: 0, vy: 0,
341	            up: false, down: false, left: false, right: false, jump: false, useItem: false,
342	            facing: ctrl & 64 ? 1 : -1, selectedItem: sel, dead: !!(flag & 64),
343	            fresh: true, active: true, lastFresh: performance.now(),
344	          };
345	          this.players.set(slot, p);
346	        }
347	        p.lastFresh = performance.now();
348	        p.x = x; p.y = y; p.vx = vx; p.vy = vy;
349	        p.up = !!(ctrl & 1); p.down = !!(ctrl & 2);
350	        p.left = !!(ctrl & 4); p.right = !!(ctrl & 8);
351	        p.jump = !!(ctrl & 16); p.useItem = !!(ctrl & 32);
352	        p.facing = ctrl & 64 ? 1 : -1;   // ctrlBits[6] = direction（原版）
353	        p.selectedItem = sel;
354	        p.dead = !!(flag & 64);           // flagBits[6] = ghost
355	        p.fresh = true;                   // Game 侧注入 netOffset 后清零
356	        return;
357	      }
358	      case Msg.TileBatch: {
359	        // 服务器中继的远端操作：应用 + 回环抑制
360	        const ops = readTileBatch(r);
361	        this.applyRemote(ops);
362	        return;
363	      }
364	      case Msg.SetTime: {
365	        // 时间对齐（服务器权威 clock）
366	        if (this.gameWorld) {
367	          const t = r.f64();
368	          const d = r.u32();
369	          if (Math.abs(this.gameWorld.clock.timeOfDay - t) > 0.005) {
370	            this.gameWorld.clock.timeOfDay = t;
371	          }
372	          this.gameWorld.clock.dayCount = d;
373	        }
374	        return;
375	      }
376	      case Msg.NetModules: {
377	        const moduleId = r.u16();
378	        if (moduleId === NetModule.Text) {
379	          const slot = r.u8();
380	          const text = r.str();
381	          const cr = r.u8(), cg = r.u8(), cb = r.u8();
382	          // slot=255 = 服务器系统公告（房主交接等）——直显无名字前缀
383	          if (slot === 255) this.hooks.onChat?.(text, cr, cg, cb);
384	          else {
385	            const name = this.players.get(slot)?.name ?? `玩家${slot}`;
386	            this.hooks.onChat?.(`<${name}> ${text}`, cr, cg, cb);
387	          }
388	        } else if (moduleId === NetModule.JoinLeave) {
389	          // 加入/离开公告（原版服务器 Lang.mp[19]/[20] 广播，色 (255,240,20)）
390	          const slot = r.u8();
391	          const joined = r.bool();
392	          const name = this.players.get(slot)?.name ?? `玩家${slot}`;
393	          this.hooks.onChat?.(
394	            Lang.text(joined ? 'LegacyMultiplayer.19' : 'LegacyMultiplayer.20', name),
395	            255, 240, 20,
396	          );
397	        }
398	        return;
399	      }
400	      case Msg.RoomPolicy: {
401	        this.policy = {
402	          roomCode: r.str(),
403	          roomName: r.str(),
404	          isHost: r.bool(),
405	          protectTiles: r.bool(),
406	          protectItems: r.bool(),
407	          maxPlayers: (() => { try { return r.u16(); } catch { return 255; } })(),
408	        };
409	        this.hooks.onPolicy?.(this.policy);
410	        return;
411	      }
412	      case Msg.SyncChestItem: {
413	        this.applyRemoteChest(r);
414	        return;
415	      }
416	      case Msg.SyncNPC: {
417	        // v4 短码格式：每条 1B eflags——bit0=含 key 全量(u32 netId+u16 codeId+str key)，
418	        // bit1=boss；否则仅 u16 codeId（查本端 codeId→netId/key 表）。
419	        // 未知短码：**先把本条剩余字段读完再丢弃**——continue 前不消费会让读指针错位，
420	        // 毒化整条连接（review C1）；自愈靠 ≤2s 全量兜底重发
421	        const n = r.u16();
422	        const snaps: NpcSnap[] = [];
423	        for (let i = 0; i < n; i++) {
424	          const eflags = r.u8();
425	          let netId = 0, key = '';
426	          if (eflags & 1) {
427	            netId = r.u32();
428	            const code = r.u16();
429	            key = r.str();
430	            this.npcCodes.set(code, { netId, key });
431	          } else {
432	            const code = r.u16();
433	            const e = this.npcCodes.get(code);
434	            netId = e?.netId ?? 0;
435	            key = e?.key ?? '';
436	          }
437	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
438	          const hp = r.i16(), maxHp = r.i16(), animT = r.u16();
439	          if (!netId) continue; // 未知短码：字段已消费，仅丢弃本条快照
440	          snaps.push({ netId, key, x, y, vx, vy, hp, maxHp, animT, flags: eflags & 2 ? 1 : 0 });
441	        }
442	        this.hooks.onNpcSnapshot?.(snaps);
443	        return;
444	      }
445	      case Msg.SyncItem: {
446	        const netId = r.u32();
447	        const op = r.u8() as 0 | 1 | 2;
448	        let key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0;
449	        if (op === 0) {
450	          key = r.str(); stack = r.u16();
451	          x = r.f32(); y = r.f32(); vx = r.f32(); vy = r.f32();
452	        }
453	        this.hooks.onItemOp?.({ op, netId, key, stack, x, y, vx, vy });
454	        return;
455	      }
456	      case Msg.SyncProjectile: {
457	        const n = r.u16();
458	        const snaps: ProjSnap[] = [];
459	        for (let i = 0; i < n; i++) {
460	          snaps.push({
461	            netId: r.u32(), kind: r.u8(), tag: r.str(),
462	            dmg: r.i16(), aux: r.i16(),
463	            x: r.f32(), y: r.f32(), vx: r.f32(), vy: r.f32(),
464	          });
465	        }
466	        this.hooks.onProjectileSync?.(snaps);
467	        return;
468	      }
469	      case Msg.StrikeNPC: {
470	        const netId = r.u32();
471	        const dmg = r.i16();
472	        const kbx = r.f32(), kby = r.f32();
473	        this.hooks.onStrike?.(netId, dmg, kbx, kby);
474	        return;
475	      }
476	      case Msg.ProjDespawn: {
477	        // v6 msg28：消亡批量——未知 netId 为无主傀儡，直接忽略
478	        const n = Math.min(r.u16(), 64);
479	        const ids: number[] = [];
480	        for (let i = 0; i < n; i++) ids.push(r.u32());
481	        if (ids.length) this.hooks.onProjDespawn?.(ids);
482	        return;
483	      }
484	      case Msg.PlayerLifeMana: {
485	        const slot = r.u8();
486	        const hp = r.i16(), maxHp = r.i16();
487	        if (slot !== this.mySlot) this.hooks.onHp?.(slot, hp, maxHp);
488	        return;
489	      }
490	      case Msg.SscSync: {
491	        // v6 msg201：服务器角色档（--ssc）——应用由 Game 侧 hook 负责
492	        this.hooks.onSSC?.(r.str());
493	        return;
494	      }
495	      case Msg.Ping:
496	        return; // 忽略回显
497	      default:
498	        return; // 未知跳过（对齐原版）
499	    }
500	  }
501	
502	  /** Game 侧设置运行期世界引用（时间对齐用） */
503	  gameWorld: World | null = null;
504	
505	  private readWorldData(r: NetReader): World {
506	    const time = r.f64();
507	    const dayCount = r.u32();
508	    const w = r.u16(), h = r.u16();
509	    const spawnX = r.i32(), spawnY = r.i32();
510	    const groundLevel = r.f32(), rockLevel = r.f32(), lavaLine = r.f32();
511	    const seed = r.i32();
512	    const name = r.str();
513	    const crimson = r.bool();
514	    const dungeonX = r.i32(), dungeonY = r.i32(), jungleX = r.i32();
515	    const flagCount = r.u16();
516	    const flags: Record<string, boolean> = {};
517	    for (let i = 0; i < flagCount; i++) flags[r.str()] = r.bool();
518	    const world = new WorldCtor(w, h, seed, name);
519	    world.clock.timeOfDay = time;
520	    world.clock.dayCount = dayCount;
521	    world.spawnX = spawnX; world.spawnY = spawnY;
522	    world.groundLevel = groundLevel; world.rockLevel = rockLevel; world.lavaLine = lavaLine;
523	    world.crimson = crimson;
524	    world.dungeonX = dungeonX; world.dungeonY = dungeonY; world.jungleX = jungleX;
525	    Object.assign(world.flags, flags);
526	    // 请求出生点周围 section（对齐原版 msg8）
527	    this.send(new NetWriter(Msg.SpawnTileData).i32(spawnX).i32(spawnY).finish());
528	    return world;
529	  }
530	
531	  // ================= tile 上报（TileStore.netReporter → 队列 → 每 tick 冲洗） =================
532	
533	  /** TileStore.netReporter 注入点；netSuppress 期间（应用远端操作）不收集 */
534	  reportTileOp(op: TileOp) {
535	    if (!this.active) return;
536	    if (this.tileQueue.length >= 256) {
537	      // R4：超限不再静默丢（静默分叉不可恢复）——告警后仍丢但留下痕迹
538	      if (!this._overflowWarned) {
539	        this._overflowWarned = true;
540	        console.warn('[net] tile 上报队列溢出（单 tick >256 op），丢弃后续——本地与远端将分叉');
541	      }
542	      return;
543	    }
544	    this.tileQueue.push(op);
545	  }
546	  private _overflowWarned = false;
547	
548	  /** Game 每 fixedUpdate 调用：冲洗 tile 队列 + 玩家状态上报（变化驱动 + 66ms 节流） */
549	  tick() {
550	    if (!this.active) return;
551	    this.syncInventory(performance.now());
552	    this.syncHp();
553	    this.flushPending(); // P1.3 msg21 合帧冲洗
554	    if (this.tileQueue.length) {
555	      // 每包最多 64 op（防超帧）
556	      const batch = this.tileQueue.splice(0, 64);
557	      const w = new NetWriter(Msg.TileBatch);
558	      w.u16(batch.length);
559	      for (const o of batch) {
560	        w.u8(o.a);
561	        w.i32(o.x); w.i32(o.y);
562	        w.u16(o.v & 0xffff);
563	        if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
564	      }
565	      this.send(w.finish());
566	    }
567	    this.sendPlayerState();
568	  }
569	
570	  private sendPlayerState() {
571	    // v2 布局（对齐原版 msg13）：控制位 + position(碰撞盒左上) + velocity。
572	    // 远端据此跑本地物理 → 有移动过程；位置差由接收端 netOffset 平滑（瞬移消失）
573	    const p = this.game.player as unknown as {
574	      x: number; y: number; vx: number; vy: number; facing: number; dead: boolean;
575	      inputX: number; inputJump: boolean; inputDown: boolean; inputUp: boolean;
576	      inv: { heldItem(): { id: number } | null };
577	    };
578	    const inp = (this.game as { input?: { mouseDown: boolean; rightDown: boolean } }).input;
579	    // ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction（原版 case 13）
580	    // useItem = 左键按住（原版 controlUseItem；放置/右键交互不计）
581	    const ctrl = (p.inputUp ? 1 : 0) | (p.inputDown ? 2 : 0)
582	      | (p.inputX < 0 ? 4 : 0) | (p.inputX > 0 ? 8 : 0)
583	      | (p.inputJump ? 16 : 0)
584	      | (inp?.mouseDown && !inp.rightDown ? 32 : 0)
585	      | (p.facing > 0 ? 64 : 0);
586	    // selectedItem = 快捷栏槽位索引 0-9（原版 NetMessage.cs:471 语义；v1 误发物品 id）
587	    const sel = (p.inv as unknown as { selected: number }).selected & 0xff;
588	    // 控制位变化即时发（原版 TrySyncingInput Player.cs:6484：任一 control/selectedItem
589	    // 变化立刻 SendData(13)）——原地起跳这类"位置未动"的操作不再等静止心跳
590	    const ctrlChanged = ctrl !== this.lastSentCtrl || sel !== this.lastSentSel || p.dead !== this.lastSentDead;
591	    const now = performance.now();
592	    const moved = Math.abs(p.x - this.lastSentPos.x) > 1 || Math.abs(p.y - this.lastSentPos.y) > 1;
593	    if (!ctrlChanged) {
594	      if (!moved && now - this.lastStateSent < 1000) return; // 静止 1s 心跳（原版 %420 全量兜底的加密版）
595	      if (now - this.lastStateSent < 66) return;             // 位置驱动节流 ≥66ms（≈15Hz）
596	    }
597	    this.lastStateSent = now;
598	    this.lastSentPos = { x: p.x, y: p.y };
599	    this.lastSentCtrl = ctrl;
600	    this.lastSentSel = sel;
601	    this.lastSentDead = p.dead;
602	    // flagBits: [2]hasVelocity [6]ghost
603	    const flag = 4 | (p.dead ? 64 : 0);
604	    this.send(new NetWriter(Msg.PlayerState)
605	      .u8(this.mySlot)
606	      .u8(ctrl).u8(flag)
607	      .u8(sel)
608	      .f32(p.x).f32(p.y)
609	      .f32(p.vx).f32(p.vy)
610	      .finish());
611	  }
612	
613	  private lastSentCtrl = -1;
614	  private lastSentSel = -1;
615	  private lastSentDead = false;
616	
617	  // ================= 箱子同步（msg31/32，服务器权威） =================
618	
619	  /** 请求打开箱子（interactAt 未命中本地 chests 时——访客本地无箱数据） */
620	  requestChestOpen(x: number, y: number) {
621	    this.send(new NetWriter(Msg.RequestChestOpen).i32(x).i32(y).finish());
622	  }
623	
624	  /** 槽位编辑上报（每槽一条消息；服务器权威+广播，编辑者本地已乐观生效） */
625	  sendChestSlot(chestIdx: number, x: number, y: number, slot: number, itemId: number, stack: number) {
626	    const w = new NetWriter(Msg.SyncChestItem);
627	    w.u16(chestIdx); w.i32(x); w.i32(y);
628	    w.u16(1);
629	    w.u8(slot); w.u16(itemId); w.u16(stack);
630	    this.send(w.finish());
631	  }
632	
633	  /** 本地登记的箱子 → 同步槽位号（Game 注册；diff 轮询用） */
634	  chestIndexByPos = new Map<string, number>();
635	
636	  private applyRemoteChest(r: NetReader) {
637	    const chestIdx = r.u16();
638	    const x = r.i32(), y = r.i32();
639	    const n = r.u16();
640	    const items: Array<{ id: number; stack: number } | null> = [];
641	    for (let i = 0; i < n; i++) {
642	      const slot = r.u8(), itemId = r.u16(), stack = r.u16();
643	      items[slot] = itemId ? { id: itemId, stack } : null;
644	    }
645	    this.hooks.onChestSync?.(chestIdx, x, y, items);
646	  }
647	
648	  /** 外观变更后重发 SyncPlayer（进游戏后 applyCharacter 调用——初始两发都在外观应用前） */
649	  resendAppearance() {
650	    if (!this.active || this.mySlot < 0) return;
651	    const p = this.game.player as { appearance?: unknown } | undefined;
652	    if (p?.appearance) {
653	      this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p.appearance)).finish());
654	    }
655	  }
656	
657	  // ================= 远端 tile 应用（回环抑制 + 事件链触发） =================
658	
659	  private applyRemote(ops: TileOp[]) {
660	    const st = this.gameWorld?.store;
661	    if (!st) return;
662	    st.netSuppress = true;
663	    try {
664	      for (const o of ops) {
665	        if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
666	        switch (o.a) {
667	          case TileOpAction.SetTile: st.setTile(o.x, o.y, o.v, o.fx, o.fy); break;
668	          case TileOpAction.SetWall: st.setWall(o.x, o.y, o.v); break;
669	          case TileOpAction.SetHalfBrick: st.setHalfBrick(o.x, o.y, !!o.v); break;
670	          case TileOpAction.SetSlope: st.setSlope(o.x, o.y, o.v); break;
671	          case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
672	          case TileOpAction.SetWire: st.setWire(o.x, o.y, o.v); break;
673	        }
674	      }
675	    } finally {
676	      st.netSuppress = false; // R5：异常安全复位（否则 suppress 永久卡死上报）
677	    }
678	  }
679	
680	  /** 聊天发送 */
681	  sendChat(text: string) {
682	    this.send(new NetWriter(Msg.NetModules).u16(NetModule.Text).str(text).finish());
683	  }
684	
685	  // ================= v3 实体同步（msg16/21/23/27/42，房主权威+服务器中继） =================
686	
687	  /** NPC 快照（msg23） */
688	  sendNpcSnapshot(snaps: NpcSnap[]) {
689	    if (!snaps.length) return;
690	    const w = new NetWriter(Msg.SyncNPC);
691	    w.u16(snaps.length);
692	    for (const s of snaps) {
693	      w.u32(s.netId); w.str(s.key);
694	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
695	      w.i16(s.hp); w.i16(s.maxHp);
696	      w.u16(s.animT & 0xffff);
697	      w.u8(s.flags);
698	    }
699	    this.send(w.finish());
700	  }
701	
702	  /** 掉落物操作（msg21）：op 0=spawn / 1=take / 2=despawn。
703	   *  P1.3 上行合帧：入 pending 攒批（netDropSweep 每 4 tick 可能逐条几十发），
704	   *  tick() 冲洗时拼为单条 WS 消息；满 64 帧立即冲防延迟 */
705	  sendItemOp(op: 0 | 1 | 2, netId: number, key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0) {
706	    const w = new NetWriter(Msg.SyncItem);
707	    w.u32(netId); w.u8(op);
708	    if (op === 0) {
709	      w.str(key); w.u16(stack);
710	      w.f32(x); w.f32(y); w.f32(vx); w.f32(vy);
711	    }
712	    this.pendingFrames.push(w.finish());
713	    if (this.pendingFrames.length >= 64) this.flushPending();
714	  }
715	
716	  /** 冲洗 pending 合帧：多帧拼接为一条 WS 消息（§1.1 允许一 WS 消息串联多帧） */
717	  private flushPending() {
718	    if (!this.pendingFrames.length || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
719	      this.pendingFrames.length = 0;
720	      return;
721	    }
722	    let total = 0;
723	    for (const f of this.pendingFrames) total += f.length;
724	    const joined = new Uint8Array(total);
725	    let off = 0;
726	    for (const f of this.pendingFrames) { joined.set(f, off); off += f.length; }
727	    this.pendingFrames.length = 0;
728	    this.ws.send(joined);
729	  }
730	
731	  /** 弹幕快照（msg27，双向：各自弹幕互播） */
732	  sendProjectileBatch(snaps: ProjSnap[]) {
733	    if (!snaps.length) return;
734	    const w = new NetWriter(Msg.SyncProjectile);
735	    w.u16(snaps.length);
736	    for (const s of snaps) {
737	      w.u32(s.netId); w.u8(s.kind); w.str(s.tag);
738	      w.i16(s.dmg); w.i16(s.aux);
739	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
740	    }
741	    this.send(w.finish());
742	  }
743	
744	  /** 弹幕消亡上报（v6 msg28，双向）：自己拥有的弹幕消亡时批量上报，
745	   *  接收端即时移除傀儡（替代纯 180t 超时清扫——消幽灵弹窗口 + 消亡闪烁） */
746	  sendProjDespawn(netIds: number[]) {
747	    if (!netIds.length) return;
748	    const w = new NetWriter(Msg.ProjDespawn);
749	    w.u16(Math.min(netIds.length, 64));
750	    for (const id of netIds.slice(0, 64)) w.u32(id);
751	    this.send(w.finish());
752	  }
753	
754	  /** 傀儡受击上报（msg42，访客→房主；Enemy.hurt 内经 entityNet 注入调用） */
755	  sendStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
756	    this.send(new NetWriter(Msg.StrikeNPC).u32(netId).i16(rawDmg).f32(kbx).f32(kby).finish());
757	  }
758	
759	  /** HP 上报（msg16，变化驱动 + 200ms 节流；原版客户端权威） */
760	  private lastHpSent = -1;
761	  private lastHpAt = 0;
762	  syncHp() {
763	    if (this.mySlot < 0) return;
764	    const p = this.game.player as unknown as { hp: number; maxHp: number };
765	    const now = performance.now();
766	    if (p.hp === this.lastHpSent) {
767	      if (now - this.lastHpAt < 5000) return; // 满血心跳 5s
768	    } else if (now - this.lastHpAt < 200) return;
769	    this.lastHpSent = p.hp;
770	    this.lastHpAt = now;
771	    this.send(new NetWriter(Msg.PlayerLifeMana).u8(this.mySlot).i16(p.hp).i16(p.maxHp).finish());
772	  }
773	
774	  // ================= 物品/装备同步（msg5，对齐原版 SyncPlayerItem 语义） =================
775	
776	  /** 远端玩家物品快照（Game 侧拷入 proxy.inv——手持/盔甲纸娃娃/挥舞动画渲染用） */
777	  remoteItems = new Map<number, { inv: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> }>();
778	
779	  /** 本地已同步快照（差分基准；null = 尚未全量 dump） */
780	  private sentInv: Array<Array<{ id: number; stack: number } | null>> | null = null;
781	  private invDumpPending = true; // 进房首包全量
782	  private lastInvSync = 0;
783	
784	  /** 全量 dump（进房后立即 + 外部可请求） */
785	  private sendFullInventory() {
786	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
787	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
788	    for (let c = 0; c < 3; c++) {
789	      const arr = c === 0 ? p.inv.slots : c === 1 ? p.inv.armor : p.inv.dye;
790	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
791	        entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: arr[i]?.id ?? 0, stack: arr[i]?.stack ?? 0 });
792	      }
793	    }
794	    this.send(writePlayerItems(entries));
795	    this.sentInv = [p.inv.slots.map(s => s ? { ...s } : null), p.inv.armor.map(s => s ? { ...s } : null), p.inv.dye.map(s => s ? { ...s } : null)];
796	    this.invDumpPending = false;
797	  }
798	
799	  /** 差分上报（tick 内每 250ms 调一次；原版 msg5 变化驱动逐槽发送的批量等价） */
800	  private syncInventory(now: number) {
801	    if (this.mySlot < 0) return;
802	    if (this.invDumpPending || !this.sentInv) { this.sendFullInventory(); return; }
803	    if (now - this.lastInvSync < 250) return;
804	    this.lastInvSync = now;
805	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
806	    const cur = [p.inv.slots, p.inv.armor, p.inv.dye];
807	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
808	    for (let c = 0; c < 3; c++) {
809	      const arr = cur[c];
810	      const sent = this.sentInv[c];
811	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
812	        const a = arr[i], b = sent[i];
813	        if ((a?.id ?? 0) !== (b?.id ?? 0) || (a?.stack ?? 0) !== (b?.stack ?? 0)) {
814	          entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: a?.id ?? 0, stack: a?.stack ?? 0 });
815	          sent[i] = a ? { ...a } : null;
816	        }
817	      }
818	    }
819	    if (entries.length) this.send(writePlayerItems(entries));
820	  }
821	
822	  private applyRemoteItems(entries: Array<ItemSyncEntry & { playerSlot: number }>) {
823	    for (const e of entries) {
824	      if (e.container > 2 || e.itemSlot >= INV_SYNC_SIZES[e.container]) continue;
825	      let bag = this.remoteItems.get(e.playerSlot);
826	      if (!bag) {
827	        bag = {
828	          inv: Array(58).fill(null), armor: Array(20).fill(null), dye: Array(10).fill(null),
829	        };
830	        this.remoteItems.set(e.playerSlot, bag);
831	      }
832	      const arr = e.container === 0 ? bag.inv : e.container === 1 ? bag.armor : bag.dye;
833	      arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: e.stack } : null;
834	    }
835	  }
836	}
837	

```


---

## 🤖 Assistant · 2026-08-12T08:34:19.389Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read _roomprobe.mjs and _loadprobe.mjs, docs, 开服.sh.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:19.507Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:19.710Z

**📎 ToolResult**

```
1	// 中央服务器房间制端到端验证（v3）：
2	// 1) 起 server（:7901 ws / :7902 lobby）
3	// 2) 页面 A 建小世界 → createRoom（公开 + 破坏保护 + 物品保护）→ 房间码
4	// 3) HTTP：公开列表含该房 / 码校验可达
5	// 4) A 以 hostToken 进房（policy.isHost=true）→ B 码加入（policy.isHost=false）
6	// 5) 双端互见
7	// 6) 破坏保护：B（非房主）tile op 被服务端拒绝 + correction 回滚；A（房主）op 中继到 B
8	// 7) 公开性过滤：非公开房不在列表、但码可查
9	// 用法：node scripts/_roomprobe.mjs
10	import puppeteer from 'puppeteer-core';
11	import { WebSocket, Writer, PROTO_MAGIC, PROTO_VER, Msg, makeTinySave, spawnServer } from './_netfake.mjs';
12	
13	const PORT = 7901; // ws
14	const LOBBY = PORT + 1; // http
15	
16	// ---- 起 server（detached 进程组：防"杀 npx 包装留 tsx 孤儿"——2026-08 实踩） ----
17	const server = spawnServer(PORT);
18	const serverLog = [];
19	server.stdout.on('data', (d) => { const s = d.toString(); serverLog.push(s); if (s.includes('[dbg]')) process.stdout.write(s); });
20	server.stderr.on('data', (d) => serverLog.push(d.toString()));
21	const waitServer = async () => {
22	  const t0 = Date.now();
23	  while (Date.now() - t0 < 180000) {
24	    if (serverLog.join('').includes(`ws://0.0.0.0:${PORT}`)) return true;
25	    await new Promise((r) => setTimeout(r, 1000));
26	  }
27	  return false;
28	};
29	if (!(await waitServer())) {
30	  console.log('FAIL: 服务器启动超时\n' + serverLog.slice(-10).join(''));
31	  server.killGroup();
32	  process.exit(1);
33	}
34	console.log('server up');
35	
36	const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
37	let pass = 0, fail = 0;
38	const check = (name, ok, extra = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}: ${name}${extra ? '  ' + extra : ''}`); ok ? pass++ : fail++; };
39	const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
40	
41	let retryFlag = false;
42	const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', defaultViewport: { width: 1280, height: 800 } });
43	const mkPage = async () => {
44	  const page = await browser.newPage();
45	  page.on('pageerror', (e) => console.log('[pageerror]', String(e.message).slice(0, 300)));
46	  page.setDefaultTimeout(300000); // 世界生成 evaluate 可能分钟级
47	  await page.goto(process.env.PROBE_GAME_URL ?? '' + (process.env.SW_ORIGIN ?? 'http://localhost:5199') + '', { waitUntil: 'domcontentloaded', timeout: 60000 });
48	  await sleep(1500);
49	  // 预热动态导入（data/items.ts 等）：触发可能的 vite 依赖再优化+全页 reload，
50	  // 必须发生在游戏状态建立之前——中后期 reload 会杀掉进行中的 evaluate（context destroyed）
51	  await page.evaluate(() => import('/src/data/items.ts').then(() => import('/src/entities/Enemy.ts')).catch(() => {})).catch(() => {});
52	  await sleep(1500);
53	  return page;
54	};
55	
56	try {
57	  // ---- A：建世界 + 建房 ----
58	  const pageA = await mkPage();
59	  await pageA.waitForFunction(() => !!window.__swFlow, { timeout: 30000 });
60	  console.log('A: 生成世界（worker，约 30-90s）…');
61	  await pageA.evaluate(() => window.__swFlow.newWorld('', 4200, 1200));
62	  await pageA.waitForFunction(() => !!window.__swGame, { timeout: 60000 });
63	  check('A 世界就绪', true);
64	
65	  const created = await pageA.evaluate(async (lobby) => {
66	    return window.__swFlow.createRoom(`127.0.0.1:${lobby}`, { public: true, protectTiles: true, protectItems: true });
67	  }, LOBBY);
68	  console.log('createRoom:', JSON.stringify(created));
69	  check('建房成功（6 位码 + hostToken）', !!created.code && /^\d{6}$/.test(created.code) && !!created.hostToken, created.error ?? `code=${created.code}`);
70	  if (!created.code) throw new Error('建房失败，终止');
71	
72	  // ---- HTTP lobby 断言 ----
73	  const listRes = await fetch(`http://127.0.0.1:${LOBBY}/rooms`).then((r) => r.json());
74	  const listed = (listRes.rooms ?? []).find((rm) => rm.code === created.code);
75	  check('公开房出现在列表（含保护标记）', !!listed && listed.protectTiles === true && listed.protectItems === true, JSON.stringify(listed ?? null));
76	  const codeRes = await fetch(`http://127.0.0.1:${LOBBY}/rooms/${created.code}`).then((r) => r.json());
77	  check('码校验可达', codeRes.ok === true && codeRes.protectTiles === true);
78	
79	  // ---- P0.1 /stats 观测端点 ----
80	  const stats0 = await fetch(`http://127.0.0.1:${LOBBY}/stats`).then((r) => r.json());
81	  check('/stats 可达（全局+逐房+字段齐）', stats0.ok === true && stats0.total && stats0.rooms
82	    && 'sendDrops' in stats0.total && 'outKbS' in stats0.rooms[0] && 'stripHit' in stats0.rooms[0],
83	    `rooms=${stats0.rooms?.length} total=${JSON.stringify(stats0.total)}`);
84	  check('公开房列表含 maxPlayers（P0.2）', !!listed && typeof listed.maxPlayers === 'number' && listed.maxPlayers >= 2,
85	    `maxPlayers=${listed?.maxPlayers}`);
86	
87	  // ---- P0.2 单房人数上限：maxPlayers=2 的房，第三个连接被 Kick('房间已满') ----
88	  {
89	    const tiny = await fetch(`http://127.0.0.1:${LOBBY}/rooms`, {
90	      method: 'POST', headers: { 'Content-Type': 'application/json' },
91	      body: JSON.stringify({ name: '满员房', public: false, maxPlayers: 2, save: makeTinySave() }),
92	    }).then((r) => r.json());
93	    check('maxPlayers=2 房创建成功', !!tiny.ok && !!tiny.code, tiny.error ?? '');
94	    if (tiny.ok) {
95	      const results = await Promise.all([0, 1, 2].map((i) => new Promise((resolve) => {
96	        const ws = new WebSocket(`ws://127.0.0.1:${PORT}/${tiny.code}`);
97	        let settled = false;
98	        const done = (v) => { if (!settled) { settled = true; try { ws.close(); } catch {} resolve(v); } };
99	        ws.on('open', () => ws.send(new Writer(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(`满员${i}`).str('').finish()));
100	        ws.on('message', (data) => {
101	          let p = 0;
102	          while (p + 3 <= data.length) {
103	            const len = data.readUInt16LE(p);
104	            if (data[p + 2] === Msg.PlayerSlot) return done({ slot: true });
105	            if (data[p + 2] === Msg.Kick) {
106	              let q = p + 3;
107	              const n = data.readUInt16LE(q); q += 2;
108	              return done({ kick: data.toString('utf8', q, q + n) });
109	            }
110	            if (len < 3) break;
111	            p += len;
112	          }
113	        });
114	        ws.on('close', () => done({ closed: true }));
115	        ws.on('error', () => done({ err: true }));
116	        setTimeout(() => done({ timeout: true }), 8000);
117	      })));
118	      const kicks = results.filter((r) => r.kick);
119	      check('第三连接被拒（房间已满）', kicks.length === 1 && kicks[0].kick.includes('房间已满'),
120	        JSON.stringify(results));
121	      // 清房（释放 slot 给后续断言无关紧要——独立房间）
122	      await fetch(`http://127.0.0.1:${LOBBY}/rooms/${tiny.code}?token=${encodeURIComponent(tiny.hostToken)}`, { method: 'DELETE' });
123	    }
124	  }
125	
126	  // ---- A 房主进房 ----
127	  const hostUrl = `ws://127.0.0.1:${PORT}/${created.code}?token=${encodeURIComponent(created.hostToken)}`;
128	  const joinA = await pageA.evaluate(async (url, token) => {
129	    try {
130	      await window.__swFlow.joinRoom(url, token);
131	    } catch (e) { return { err: String(e) }; }
132	    const g = window.__swGame;
133	    const oldWorld = g.world; // 建房用的世界已被换为服务器下发副本
134	    return {
135	      ok: !!g.net?.active,
136	      isHost: g.net?.policy?.isHost,
137	      protectTiles: g.net?.policy?.protectTiles,
138	      protectItems: g.net?.policy?.protectItems,
139	      w: g.world?.w, slot: g.net?.mySlot,
140	      canEdit: g.netCanEditTile(), canChest: g.netCanChestInteract(),
141	      worldReplaced: oldWorld !== null,
142	    };
143	  }, hostUrl, created.hostToken).catch((e) => ({ err: String(e) }));
144	  console.log('A(房主):', JSON.stringify(joinA));
145	  check('A 房主进房成功', !!joinA.ok && joinA.isHost === true, joinA.err ?? `slot=${joinA.slot}`);
146	  check('A policy 双保护生效 + 门禁放行（房主）', joinA.protectTiles === true && joinA.protectItems === true && joinA.canEdit === true && joinA.canChest === true);
147	
148	  // ---- B 码加入（无 token） ----
149	  const pageB = await mkPage();
150	  await pageB.waitForFunction(() => !!window.__swFlow, { timeout: 30000 });
151	  const joinB = await pageB.evaluate(async (url) => {
152	    try {
153	      await window.__swFlow.joinRoom(url, '');
154	    } catch (e) { return { err: String(e) }; }
155	    const g = window.__swGame;
156	    return {
157	      ok: !!g.net?.active,
158	      isHost: g.net?.policy?.isHost,
159	      protectTiles: g.net?.policy?.protectTiles,
160	      canEdit: g.netCanEditTile(), canChest: g.netCanChestInteract(),
161	      w: g.world?.w, slot: g.net?.mySlot,
162	    };
163	  }, `ws://127.0.0.1:${PORT}/${created.code}`).catch((e) => ({ err: String(e) }));
164	  console.log('B(访客):', JSON.stringify(joinB));
165	  check('B 码加入成功', !!joinB.ok, joinB.err ?? `slot=${joinB.slot}`);
166	  check('B policy 非房主 + 门禁拦截（protectTiles/Items）', joinB.isHost === false && joinB.canEdit === false && joinB.canChest === false);
167	
168	  // A 记录聊天（加入/离开公告断言用；B 尚未触发任何公告）
169	  await pageA.evaluate(() => {
170	    window.__chatLog = [];
171	    const g = window.__swGame;
172	    const orig = g.cb.onChat;
173	    g.cb.onChat = (t, r, gg, b) => { window.__chatLog.push([t, r, gg, b]); orig?.(t, r, gg, b); };
174	  });
175	
176	  if (joinA.ok && joinB.ok) {
177	    // ---- 双端互见 ----
178	    await pageA.evaluate(() => {
179	      const g = window.__swGame;
180	      for (let i = 0; i < 180; i++) {
181	        if (i % 3 === 0) g.player.x += 0.8;
182	        g.fixedUpdate(1 / 60);
183	      }
184	    });
185	    await sleep(800);
186	    const seeB = await pageA.evaluate(() => [...window.__swGame.net.players.values()].filter((p) => p.active).length);
187	    const seeA = await pageB.evaluate(() => [...window.__swGame.net.players.values()].filter((p) => p.active).length);
188	    check('双端互见', seeB >= 1 && seeA >= 1, `A侧=${seeB} B侧=${seeA}`);
189	
190	    // ---- P1.1 AOI（玩家态）：B 传送 6000px 外（>1920×1.6 滞回外径）→ A 侧代理冻结 ----
191	    const bHome = await pageB.evaluate(() => ({ x: window.__swGame.player.x, y: window.__swGame.player.y }));
192	    await pageB.evaluate(async (home) => {
193	      const g = window.__swGame;
194	      const far = home.x + 6000;
195	      for (let i = 0; i < 12; i++) {
196	        g.player.x = far; g.player.vx = 0; g.player.vy = 0;
197	        g.fixedUpdate(1 / 60); g.postUpdate();
198	        await new Promise((r) => setTimeout(r, 70)); // 让 66ms 节流放行上报新位置
199	      }
200	    }, bHome);
201	    await sleep(2500); // 越过 1.5s stale 冻结阈值
202	    const frozen = await pageA.evaluate(() => {
203	      const g = window.__swGame;
204	      const rp = g.net.players.get(1);
205	      const px = g.remotePlayerProxies.find((p) => p.__netSlot === 1);
206	      return { age: performance.now() - (rp?.lastFresh ?? 0), inputX: px?.inputX ?? null, hasProxy: !!px };
207	    });
208	    check('AOI：B 出视野 → A 侧代理冻结（防幽灵行走）', frozen.hasProxy && frozen.age > 1500 && frozen.inputX === 0,
209	      JSON.stringify(frozen));
210	    // B 回到 A 身边 → 恢复接收（末尾再泵一轮：headless 后台页 rAF 节流，静止心跳可能停发）
211	    await pageB.evaluate(async (home) => {
212	      const g = window.__swGame;
213	      for (let i = 0; i < 12; i++) {
214	        g.player.x = home.x; g.player.y = home.y; g.player.vx = 0; g.player.vy = 0;
215	        g.fixedUpdate(1 / 60); g.postUpdate();
216	        await new Promise((r) => setTimeout(r, 70));
217	      }
218	    }, bHome);
219	    await sleep(1200);
220	    // headless 后台页 rAF 停转：A 不泵 → 服务器判 A 盲（>5s 无 msg13）→ 不给 A 中继。
221	    // 先泵 A（保持非盲），再泵 B（位移 >1px 强制即时上报），然后读 A 的新鲜度
222	    await pageA.evaluate(() => {
223	      const g = window.__swGame;
224	      for (let i = 0; i < 4; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
225	    });
226	    await sleep(300);
227	    await pageB.evaluate(() => {
228	      const g = window.__swGame;
229	      g.player.x += 2;
230	      for (let i = 0; i < 4; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
231	    });
232	    const resumed = await pageA.evaluate(() => performance.now() - (window.__swGame.net.players.get(1)?.lastFresh ?? 0));
233	    check('AOI：B 回视野 → 恢复接收 msg13', resumed < 1500, `age=${resumed.toFixed(0)}ms`);
234	
235	    // ---- 破坏保护：B（非房主）tile op 被拒 + correction 回滚 ----
236	    const t0 = await pageB.evaluate(() => {
237	      const g = window.__swGame;
238	      const x = g.world.spawnX, y = g.world.spawnY + 3;
239	      return { x, y, before: g.world.store.get(x, y) };
240	    });
241	    // B 直接改 store（模拟绕过 UI 门禁的恶意/乐观写入）→ 上报 → 服务器拒绝 + 纠正
242	    await pageB.evaluate((t) => {
243	      const g = window.__swGame;
244	      g.world.store.setTile(t.x, t.y, 0);
245	      g.net.tick();
246	    }, t0);
247	    await sleep(1000);
248	    const afterB = await pageB.evaluate((t) => window.__swGame.world.store.get(t.x, t.y), t0);
249	    const afterA = await pageA.evaluate((t) => window.__swGame.world.store.get(t.x, t.y), t0);
250	    check('B 非房主 tile op 被拒（本地回滚 + 房主侧不变）', t0.before !== 0 && afterB === t0.before && afterA === t0.before,
251	      `before=${t0.before} B=${afterB} A=${afterA}`);
252	
253	    // ---- 房主 op 正常中继 ----
254	    const t1 = await pageA.evaluate(() => {
255	      const g = window.__swGame;
256	      const x = g.world.spawnX, y = g.world.spawnY + 3;
257	      const before = g.world.store.get(x, y);
258	      g.world.store.setTile(x, y, 0);
259	      g.net.tick();
260	      return { x, y, before };
261	    });
262	    await sleep(1000);
263	    const relayB = await pageB.evaluate((t) => window.__swGame.world.store.get(t.x, t.y), t1);
264	    check('房主 tile op 中继到 B', t1.before !== 0 && relayB === 0, `before=${t1.before} B=${relayB}`);
265	    // 恢复（避免影响后续）：房主写回
266	    await pageA.evaluate((t) => {
267	      const g = window.__swGame;
268	      g.world.store.setTile(t.x, t.y, t.before);
269	      g.net.tick();
270	    }, t1);
271	
272	    // ---- v2 msg13 远端模拟回归：netOffset 注入+衰减、坐标零错位 ----
273	    // A 持续位移 180px（墙钟节拍驱动——同步循环会被 66ms 发送节流压成单包）
274	    const finalA = await pageA.evaluate(async () => {
275	      const g = window.__swGame;
276	      const before = { x: g.player.x, y: g.player.y };
277	      for (let i = 0; i < 30; i++) {
278	        g.player.x += 6;
279	        g.fixedUpdate(1 / 60);
280	        await new Promise((r) => setTimeout(r, 70)); // 让 sendPlayerState 节流放行（≈15Hz）
281	      }
282	      return { before, after: { x: g.player.x, y: g.player.y } };
283	    });
284	    await sleep(1000); // netOffset 衰减窗口 + A 落定（循环末可能半空）
285	    // 注意：A 循环后可能仍在下落（x 位移可能走出台阶）——对比 A 的实时位置而非循环末快照
286	    const aNow = await pageA.evaluate(() => ({ x: window.__swGame.player.x, y: window.__swGame.player.y }));
287	    const align = await pageB.evaluate((a) => {
288	      const g = window.__swGame;
289	      const px = g.remotePlayerProxies[0];
290	      if (!px) return { err: 'no proxy' };
291	      return {
292	        proxyX: px.x, proxyY: px.y,
293	        offX: px.netOffX, offY: px.netOffY,
294	        onGround: px.onGround,
295	        dx: Math.abs(px.x + px.netOffX - a.x),
296	        dy: Math.abs(px.y + px.netOffY - a.y),
297	      };
298	    }, aNow);
299	    console.log('对齐:', JSON.stringify(align));
300	    check('远端代理存在（控制位驱动物理）', !align.err);
301	    check('netOffset 已收敛（移动过程平滑，非瞬移残留）', !align.err && Math.abs(align.offX) + Math.abs(align.offY) < 30,
302	      `off=(${align.offX?.toFixed(1)},${align.offY?.toFixed(1)})`);
303	    check('坐标零错位（左上角语义对齐，渲染位≈权威位 ±2px）', !align.err && align.dx < 2 && align.dy < 4,
304	      `dx=${align.dx?.toFixed(2)}px dy=${align.dy?.toFixed(2)}px onGround=${align.onGround}`);
305	
306	    // ---- msg5 物品/装备同步：手持物 + useItem 远端挥舞 ----
307	    const itemSync = await pageA.evaluate(async () => {
308	      const torch = window.__swFlow.itemByKey('torch'); // 探针桥（生产构建可用）
309	      const g = window.__swGame;
310	      g.player.inv.slots[2] = { id: torch, stack: 5 };
311	      g.player.inv.selected = 2;
312	      g.net.tick(); g.net.tick(); // 差分上报冲洗
313	      return { torch };
314	    });
315	    await sleep(600); // 服务器中继 + B 应用
316	    const bItems = await pageB.evaluate((t) => {
317	      const g = window.__swGame;
318	      const bag = g.net.remoteItems.get(0);
319	      const px = g.remotePlayerProxies[0];
320	      return {
321	        hasBag: !!bag,
322	        torch: bag?.inv?.[2]?.id ?? -1,
323	        held: px?.inv?.heldItem()?.id ?? -1,
324	        selected: px?.inv?.selected ?? -1,
325	      };
326	    }, itemSync.torch);
327	    check('物品同步（msg5 差分 → B 侧手持一致）', bItems.hasBag && bItems.torch === itemSync.torch
328	      && bItems.held === itemSync.torch && bItems.selected === 2,
329	      JSON.stringify({ ...bItems, expect: itemSync.torch }));
330	
331	    // useItem 位 → B 侧挥舞动画（按住期断言非空，松开后断言清除——分两段防节流竞态）
332	    await pageA.evaluate(async () => {
333	      const g = window.__swGame;
334	      g.input.mouseDown = true;
335	      for (let i = 0; i < 6; i++) {
336	        g.fixedUpdate(1 / 60);
337	        g.net.tick();
338	        await new Promise((r) => setTimeout(r, 70));
339	      }
340	    });
341	    await sleep(400); // 给 B 的 rAF 处理窗口（B 页面可能被后台节流）
342	    const bSwing = await pageB.evaluate(() => window.__swGame.remotePlayerProxies[0]?.swingNet ?? null);
343	    check('远端挥舞动画（useItem 位 → swingNet）', !!bSwing, JSON.stringify(bSwing));
344	    await pageA.evaluate(async () => {
345	      const g = window.__swGame;
346	      g.input.mouseDown = false;
347	      // 显式 flush 释放包（页面 rAF 可能被后台节流，不补这步 useItem=1 残留）
348	      for (let i = 0; i < 3; i++) {
349	        g.net.tick();
350	        await new Promise((r) => setTimeout(r, 70));
351	      }
352	    });
353	    await sleep(1500); // 松开后动画走完清除
354	    const bSwing2 = await pageB.evaluate(() => window.__swGame.remotePlayerProxies[0]?.swingNet ?? null);
355	    check('松开后挥舞结束清除', bSwing2 === null, JSON.stringify(bSwing2));
356	
357	    // ---- v3 实体同步：NPC 傀儡 + 打击上报 + 掉落物 + HP + 箱子 + 重连 ----
358	    // 房主生成一只僵尸（v_3）→ 快照广播 → B 侧傀儡
359	    const npcPos = await pageA.evaluate(async () => {
360	      const e = await window.__swFlow.spawnVanillaEnemy(3, window.__swGame.player.cx + 80, window.__swGame.player.cy); // 探针桥
361	      const g = window.__swGame;
362	      // 显式泵游戏循环（headless 背景页 rAF 可能停转——postUpdate 驱动快照广播）
363	      for (let i = 0; i < 60; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
364	      return e ? { x: e.x, y: e.y, id: e.id, hp: e.hp } : null;
365	    });
366	    // 房主 rAF 可能被后台节流——轮询等待快照到达（最多 6s）
367	    // 注意：房主自然刷怪已激活——按 netId（房主 slot=0 → netId=本地 id）精确找探针僵尸
368	    if (!npcPos) { check('NPC 快照→访客傀儡（msg23）', false, 'spawnVanillaEnemy 桥失败'); }
369	    let bNpc = null;
370	    for (let i = 0; i < 6 && !bNpc; i++) {
371	      await sleep(1000);
372	      bNpc = await pageB.evaluate((id) => {
373	        const g = window.__swGame;
374	        if (!g) return null;
375	        const pup = g.netNpcPuppets.get(id);
376	        return pup ? { netId: pup.e.netId, key: pup.e.key, puppet: pup.e.netPuppet, hp: pup.e.hp, n: g.netNpcPuppets.size } : null;
377	      }, npcPos?.id).catch(() => null);
378	    }
379	    check('NPC 快照→访客傀儡（msg23）', !!bNpc && bNpc.key === 'v_3' && bNpc.puppet === true, JSON.stringify(bNpc));
380	
381	    // P1.2 msg23 短码表（v4）：快照驱动 npcCodes 表填充（S→C 短码格式工作正常）
382	    const codes = await pageB.evaluate(() => window.__swGame.net.npcCodes.size);
383	    check('msg23 短码表填充（v4 短码格式生效）', codes >= 1, `npcCodes=${codes}`);
384	
385	    // B 打击傀儡 → msg42 → 房主权威扣血
386	    if (bNpc) {
387	      const strike = await pageB.evaluate(async (id) => {
388	        const g = window.__swGame;
389	        const pup = g.netNpcPuppets.get(id).e;
390	        const hpBefore = pup.hp;
391	        pup.hurt(30, 2, -1, g); // 触发 entityNet.reportStrike → msg42
392	        return { hpBefore, hpAfter: pup.hp };
393	      }, npcPos?.id);
394	      await sleep(1200);
395	      const hostHp = await pageA.evaluate((id) => {
396	        for (const ent of window.__swGame.entities.enemies) {
397	          if (ent.id === id) return ent.hp;
398	        }
399	        return -1;
400	      }, npcPos?.id);
401	      check('访客打击上报→房主权威扣血（msg42）', hostHp > 0 && hostHp < npcPos?.hp, `host hp=${hostHp}/${npcPos?.hp}（原 ${strike.hpBefore}）`);
402	      // B 侧傀儡 hp 经快照收敛到房主值
403	      await sleep(600);
404	      const bHp = await pageB.evaluate((id) => window.__swGame.netNpcPuppets.get(id)?.e.hp ?? -1, npcPos?.id);
405	      check('傀儡 hp 随快照收敛', bHp === hostHp, `B=${bHp} host=${hostHp}`);
406	
407	      // ---- P1.1 AOI（NPC 态）：B 远离 → msg23 停发 → 傀儡 300 tick 清扫；回来自动重建 ----
408	      const bHome2 = await pageB.evaluate(() => ({ x: window.__swGame.player.x, y: window.__swGame.player.y }));
409	      await pageB.evaluate(async (home) => {
410	        const g = window.__swGame;
411	        const far = home.x + 6000;
412	        for (let i = 0; i < 12; i++) {
413	          g.player.x = far; g.player.vx = 0; g.player.vy = 0;
414	          g.fixedUpdate(1 / 60); g.postUpdate();
415	          await new Promise((r) => setTimeout(r, 70));
416	        }
417	      }, bHome2);
418	      await sleep(6500); // 300 tick(5s) 傀儡清扫 + 余量
419	      const pupFar = await pageB.evaluate(() => window.__swGame.netNpcPuppets.size);
420	      check('AOI：B 出视野 → NPC 傀儡被清扫', pupFar === 0, `puppets=${pupFar}`);
421	      await pageB.evaluate(async (home) => {
422	        const g = window.__swGame;
423	        for (let i = 0; i < 12; i++) {
424	          g.player.x = home.x; g.player.y = home.y; g.player.vx = 0; g.player.vy = 0;
425	          g.fixedUpdate(1 / 60); g.postUpdate();
426	          await new Promise((r) => setTimeout(r, 70));
427	        }
428	      }, bHome2);
429	      // 回视野后房主 2s 兜底全量重播（AOI 重入自愈路径：短码已知集过期 → 全量带 key）。
430	      // headless rAF 停转：每轮显式泵房主 A（发 msg23）+ B（保持非盲收流）
431	      let pupBack = 0;
432	      for (let i = 0; i < 8 && pupBack < 1; i++) {
433	        await pageA.evaluate(() => {
434	          const g = window.__swGame;
435	          for (let k = 0; k < 30; k++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
436	        }).catch(() => {});
437	        await pageB.evaluate(() => {
438	          const g = window.__swGame;
439	          for (let k = 0; k < 10; k++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
440	        }).catch(() => {});
441	        await sleep(800);
442	        pupBack = await pageB.evaluate(() => window.__swGame.netNpcPuppets.size).catch(() => 0);
443	      }
444	      check('AOI：B 回视野 → NPC 傀儡重建（2s 兜底重入）', pupBack >= 1, `puppets=${pupBack}`);
445	    }
446	
447	    // 房主掉落物 → B 傀儡 → B 拾取 → take 上报 → 房主真身移除
448	    const dropPos = await pageA.evaluate(() => {
449	      const g = window.__swGame;
450	      const d = g.spawnDrop(g.player.cx + 30, g.player.cy - 20, 'torch', 3);
451	      // 泵循环让 netDropSweep 上报 spawn（rAF 停转兜底）
452	      for (let i = 0; i < 20; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
453	      return d ? { x: d.x, y: d.y, id: d.id } : null;
454	    });
455	    await sleep(1000);
456	    let bDrop = 0;
457	    for (let i = 0; i < 6 && bDrop < 1; i++) {
458	      await sleep(1000);
459	      bDrop = await pageB.evaluate(() => window.__swGame?.netDropPuppets?.size ?? 0).catch(() => 0);
460	    }
461	    check('掉落物 spawn→访客傀儡（msg21）', bDrop >= 1, `puppets=${bDrop}`);
462	    if (bDrop >= 1 && dropPos) {
463	      // B 走到掉落物上拾取（PICKUP_DELAY 后触发）
464	      await pageB.evaluate(async (dp) => {
465	        const g = window.__swGame;
466	        g.player.x = dp.x - 4; g.player.y = dp.y - 8;
467	        for (let i = 0; i < 90; i++) {
468	          g.fixedUpdate(1 / 60);
469	          g.net.tick();
470	          if (i % 10 === 0) await new Promise((r) => setTimeout(r, 30));
471	        }
472	      }, dropPos);
473	      await sleep(800); // take 上报 → 房主移除 → 快照收敛
474	      const hostDrops = await pageA.evaluate(() => window.__swGame.entities.drops.filter((d) => !d.netPuppet && !d.dead).length);
475	      bDrop = await pageB.evaluate(() => window.__swGame.netDropPuppets.size);
476	      check('访客拾取→take→房主真身移除', hostDrops === 0 && bDrop === 0, `host=${hostDrops} B傀儡=${bDrop}`);
477	      // B 背包拿到火把
478	      const bTorch = await pageB.evaluate(async () => {
479	        const torch = window.__swFlow.itemByKey('torch');
480	        return window.__swGame.player.inv.slots.some((s) => s && s.id === torch);
481	      });
482	      check('访客拾取入包（物品保护豁免拾取）', bTorch === true);
483	    }
484	
485	    // msg16 HP 中继：B 扣血 → A 侧 players 表同步
486	    await pageB.evaluate(() => {
487	      const g = window.__swGame;
488	      g.player.hp = 55;
489	      g.net.tick();
490	    });
491	    await sleep(600);
492	    const aHp = await pageA.evaluate(() => window.__swGame.net.players.get(1)?.hp ?? -1);
493	    check('HP 中继（msg16）', aHp === 55, `A侧=${aHp}`);
494	
495	    // ---- v5 敌对弹幕：房主发射 hostile 弹 → 访客傀儡带 bit7 → 本地结算 Damage_EVP ----
496	    {
497	      // B 满血归位 + 泵一轮刷新服务器侧位置（headless 节流下 >5s 无 msg13 会被判盲跳过中继）
498	      await pageB.evaluate(async () => {
499	        const g = window.__swGame;
500	        g.player.hp = 100;
501	        g.player.iframes = 0;
502	        for (let i = 0; i < 6; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); }
503	        await new Promise((r) => setTimeout(r, 100));
504	        g.net.tick();
505	      });
506	      const bPos = await pageB.evaluate(() => ({ x: window.__swGame.player.cx, y: window.__swGame.player.cy }));
507	      // 房主直接在 B 身上生成 hostile 弹（projId 9=EyeLaser，grav=0 微速漂移 vx=0.5）：
508	      // 零飞行 = 免地形干扰的确定性重叠；微速 = 每 2-4 tick 触发差分快照持续刷新傀儡
509	      const projSpawn = await pageA.evaluate(async (pos) => {
510	        const p = await window.__swFlow.spawnHostileProj(pos.x, pos.y, 0.5, 0, 15, 9, 0);
511	        const g = window.__swGame;
512	        for (let i = 0; i < 90; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); } // 广播 msg27（带 bit7）
513	        return p ? p.id : -1;
514	      }, bPos);
515	      // B 泵循环：傀儡到达 + netPuppetProjContact 本地结算
516	      await pageB.evaluate(async () => {
517	        const g = window.__swGame;
518	        for (let i = 0; i < 90; i++) {
519	          g.fixedUpdate(1 / 60);
520	          g.postUpdate();
521	          if (i % 10 === 0) await new Promise((r) => setTimeout(r, 30));
522	        }
523	      });
524	      await sleep(600); // msg16 中继窗口
525	      const projDmg = await pageB.evaluate(() => window.__swGame.player.hp);
526	      const aHp2 = await pageA.evaluate(() => window.__swGame.net.players.get(1)?.hp ?? -1);
527	      // 中间态诊断：房主真身弹体存活数 / B 端总傀儡数 / B iframes / 傀儡明细
528	      const diag = {
529	        aArrows: await pageA.evaluate(() => window.__swGame.entities.projectiles.filter((p) => !p.netPuppet && !p.dead).length),
530	        bTotal: await pageB.evaluate(() => window.__swGame.netProjPuppets.size),
531	        bIfr: await pageB.evaluate(() => window.__swGame.player.iframes),
532	        pup: await pageB.evaluate(() => {
533	          for (const [, pup] of window.__swGame.netProjPuppets) {
534	            const p = pup.p;
535	            return { hostile: !!p.hostile, dmg: p.damage ?? -1, ax: Math.round(p.netAx), ay: Math.round(p.netAy), x: Math.round(p.x), y: Math.round(p.y), px: Math.round(window.__swGame.player.x), py: Math.round(window.__swGame.player.y) };
536	          }
537	          return null;
538	        }),
539	      };
540	      check('敌对弹幕对访客伤害（v5 bit7 + Damage_EVP 本地结算）', projDmg < 100, `B hp=${projDmg}/100 ${JSON.stringify(diag)}`);
541	      check('弹幕伤害经 msg16 中继到房主', aHp2 === projDmg, `A侧=${aHp2} B侧=${projDmg}`);
542	      // 弹体命中不销毁（原版 :13811 穿透不消耗语义）——傀儡应仍存在或自然超时。
543	      // 轮询 3s：傀儡创建是纯网络事件，headless 投递时序偶发迟到（曾 flaky）
544	      let pupHostile = 0;
545	      for (let i = 0; i < 6 && pupHostile < 1; i++) {
546	        pupHostile = await pageB.evaluate(() => {
547	          let n = 0;
548	          for (const [, pup] of window.__swGame.netProjPuppets) if (pup.p.hostile) n++;
549	          return n;
550	        }).catch(() => 0);
551	        if (pupHostile < 1) await sleep(500);
552	      }
553	      check('hostile 弹幕傀儡重建（bit7 解码）', pupHostile >= 1, `hostile傀儡=${pupHostile}`);
554	      // ---- v6 msg28：房主击杀真身弹 → 消亡上报 → B 傀儡即时移除（替代 180t 超时）----
555	      if (projSpawn > 0) {
556	        await pageA.evaluate(async (pid) => {
557	          const g = window.__swGame;
558	          for (const ent of g.entities.projectiles) if (ent.id === pid) ent.dead = true;
559	          for (let i = 0; i < 30; i++) { g.fixedUpdate(1 / 60); g.postUpdate(); } // netProjLast 清理 → msg28
560	        }, projSpawn);
561	        await sleep(800); // 中继 + 事件驱动移除（无需 B 侧泵）
562	        const gone = await pageB.evaluate(() => window.__swGame.netProjPuppets.size).catch(() => -1);
563	        check('msg28 弹幕消亡即时移除傀儡', gone === 0, `puppets=${gone}`);
564	      }
565	    }
566	
567	    // 箱子同步：B 请求开箱（msg31）→ 服务器权威内容（msg32）→ protectItems 编辑被拒。
568	    // 锚点从 lobby 码校验端点拿（客户端只加载出生点条带，本地扫不到远处箱子）
569	    const chestTile = await fetch(`http://127.0.0.1:${LOBBY}/rooms/${created.code}`).then((r) => r.json()).then((d) => d.chest ?? null);
570	    if (chestTile) {
571	      // B 请求开箱
572	      await pageB.evaluate((ct) => {
573	        const g = window.__swGame;
574	        g.netPendingChest = { x: ct.x, y: ct.y };
575	        g.net.requestChestOpen(ct.x, ct.y);
576	      }, chestTile);
577	      await sleep(800);
578	      const bChest = await pageB.evaluate(() => {
579	        const g = window.__swGame;
580	        const ch = g.world.chests[0];
581	        return ch ? { x: ch.x, y: ch.y, slots: ch.items.filter(Boolean).length } : null;
582	      });
583	      check('箱子内容下发（msg31/32，服务器权威）', !!bChest && bChest.slots > 0, JSON.stringify(bChest));
584	      if (bChest?.slots > 0) {
585	        // B（非房主，protectItems）尝试放入火把 → 服务器拒绝 + 权威纠正回滚
586	        const before = await pageB.evaluate(() => {
587	          const ch = window.__swGame.world.chests[0];
588	          return { first: ch.items[0] ? { ...ch.items[0] } : null };
589	        });
590	        const hasEmpty = await pageB.evaluate(() => window.__swGame.world.chests[0].items.some((s) => !s));
591	        if (hasEmpty) {
592	          await pageB.evaluate(async () => {
593	            const g = window.__swGame;
594	            const ch = g.world.chests[0];
595	            const idx = ch.items.findIndex((s) => !s);
596	            ch.items[idx] = { id: 6, stack: 1 };
597	            for (let i = 0; i < 20; i++) { g.net.tick(); await new Promise((r) => setTimeout(r, 20)); }
598	          });
599	          await sleep(800); // 纠正回包
600	          const after = await pageB.evaluate(() => {
601	            const ch = window.__swGame.world.chests[0];
602	            return ch.items.some((s) => s && s.id === 6);
603	          });
604	          check('protectItems：非房主编辑被服务端拒绝+纠正', after === false, `torch残留=${after}`);
605	        } else {
606	          check('protectItems：非房主编辑被服务端拒绝+纠正', true, '箱满跳过（无空槽）');
607	        }
608	        void before;
609	      }
610	    } else {
611	      check('箱子内容下发（msg31/32，服务器权威）', false, '世界中未找到箱子 tile');
612	    }
613	
614	    // 断线重连：B 模拟网络断开（非用户主动）→ 自动携 session 重连 → 同 slot 复位
615	    const slotBefore = await pageB.evaluate(() => window.__swGame.net.mySlot);
616	    await pageB.evaluate(() => window.__swGame.net.ws.close()); // 绕过 userClosed = 模拟掉线
617	    await sleep(6000); // 2s 重试间隔 + 世界重组装
618	    const rc = await pageB.evaluate(() => ({
619	      active: window.__swGame?.net?.active,
620	      slot: window.__swGame?.net?.mySlot,
621	      world: !!window.__swGame?.world,
622	    })).catch((e) => ({ err: String(e) }));
623	    check('断线自动重连（session 同 slot 复位）', rc.active === true && rc.slot === slotBefore, JSON.stringify(rc));
624	    // 尽早断言（vite 偶发全量 reload 会清 window 状态——缩短暴露窗口）
625	    await pageB.evaluate(() => window.__swGame.net.disconnect());
626	    await sleep(1000);
627	    const chatA = await pageA.evaluate(() => window.__chatLog ?? []);
628	    const joinMsg = chatA.find((c) => String(c[0]).includes('已加入'));
629	    const leaveMsg = chatA.find((c) => String(c[0]).includes('已离开'));
630	    check('加入公告（"X已加入。"）', !!joinMsg, JSON.stringify(joinMsg ?? null));
631	    check('离开公告（"X已离开。"，强制断线触发）', !!leaveMsg, JSON.stringify(leaveMsg ?? null));
632	    check('公告颜色 (255,240,20)', !!joinMsg && joinMsg[1] === 255 && joinMsg[2] === 240 && joinMsg[3] === 20);
633	
634	    // ---- P2.1 section 编码缓存：重连重发出生点条带应命中缓存 ----
635	    const statsR = await fetch(`http://127.0.0.1:${LOBBY}/stats`).then((r) => r.json());
636	    const roomR = (statsR.rooms ?? []).find((rm) => rm.code === created.code);
637	    check('strip 编码缓存命中（重连场景）', !!roomR && roomR.stripHit > 0,
638	      `hit=${roomR?.stripHit} miss=${roomR?.stripMiss}`);
639	  }
640	
641	  // ---- 公开性过滤：非公开房不在列表、码可查 ----
642	  const created2 = await pageA.evaluate(async (lobby) => {
643	    return window.__swFlow.createRoom(`127.0.0.1:${lobby}`, { public: false });
644	  }, LOBBY);
645	  check('第二房（非公开）创建成功', !!created2.code, created2.error ?? '');
646	  if (created2.code) {
647	    const list2 = await fetch(`http://127.0.0.1:${LOBBY}/rooms`).then((r) => r.json());
648	    const visible = (list2.rooms ?? []).some((rm) => rm.code === created2.code);
649	    check('非公开房不出现在列表', visible === false);
650	    const direct = await fetch(`http://127.0.0.1:${LOBBY}/rooms/${created2.code}`).then((r) => r.json());
651	    check('非公开房码可查（码加入可行）', direct.ok === true);
652	  }
653	
654	  // ---- UI 面板回归：真实点击流程进房 + 断言进度遮罩消失（StatusText 误报修复） ----
655	  // 背景：R3 移动续传的 StatusText(0) 曾无条件回调 onProgress → 进世界后全屏
656	  // "接收世界数据"遮罩被重新拉起 → 视觉上永久卡死。桥路径（noop onProgress）测不出。
657	  const pageC = await mkPage();
658	  await pageC.waitForFunction(() => !!window.__swFlow, { timeout: 30000 });
659	  await pageC.click('[data-act="mp"]');
660	  await sleep(800);
661	  // 服务器地址默认 127.0.0.1:7778 → 改成探针 lobby 端口
662	  await pageC.evaluate((lobby) => {
663	    const panel = document.querySelector('.sw-panel');
664	    const input = panel?.querySelector('input');
665	    if (input) input.value = `127.0.0.1:${lobby}`;
666	  }, LOBBY);
667	  // 刷新房间列表 → 等列表出现公开房 → 点击第一条
668	  await pageC.evaluate(() => {
669	    const btns = [...document.querySelectorAll('.sw-panel button')];
670	    btns.find((b) => b.textContent.includes('刷新房间'))?.click();
671	  });
672	  await sleep(1500);
673	  let clicked = false;
674	  for (let i = 0; i < 4 && !clicked; i++) {
675	    clicked = await pageC.evaluate((code) => {
676	      for (const item of [...document.querySelectorAll('.sw-panel div')]) {
677	        if (item.textContent.includes(`[${code}]`) && item.onclick) { item.click(); return true; }
678	      }
679	      return false;
680	    }, created.code).catch(() => false);
681	    if (!clicked) {
682	      await pageC.evaluate(() => {
683	        const btns = [...document.querySelectorAll('.sw-panel button')];
684	        btns.find((b) => b.textContent.includes('刷新房间'))?.click();
685	      }).catch(() => {});
686	      await sleep(1200);
687	    }
688	  }
689	  check('UI 房间列表点击加入', clicked === true);
690	  // 等 C 进世界
691	  await pageC.waitForFunction(() => !!window.__swGame?.net?.active && !!window.__swGame?.world, { timeout: 60000 });
692	  await sleep(4000); // 放过 R3 续传首个 30-tick 窗口
693	  const overlay = await pageC.evaluate(() => {
694	    const p = document.querySelector('.sw-progress');
695	    return { visible: !!p, text: p?.textContent ?? '' };
696	  });
697	  check('进世界后进度遮罩已消失（不再卡"接收世界数据"）', overlay.visible === false, JSON.stringify(overlay));
698	  const cOk = await pageC.evaluate(() => ({ active: window.__swGame.net.active, isHost: window.__swGame.net.policy.isHost }));
699	  check('UI 进房 policy 正确（访客）', cOk.active === true && cOk.isHost === false, JSON.stringify(cOk));
700	
701	  // ---- P3.1 持久化：SIGTERM 落盘 → --world 重启 → 常驻房可查 ----
702	  {
703	    const { existsSync } = await import('node:fs');
704	    const path = await import('node:path');
705	    const { ROOT } = await import('./_netfake.mjs');
706	    const worldFile = path.join(ROOT, 'server', 'worlds', `room-${created.code}.json`);
707	    server.killGroup(); // SIGTERM → 优雅落盘退出
708	    let exited = false;
709	    for (let i = 0; i < 100 && !exited; i++) { await sleep(100); exited = server.exitCode !== null; }
710	    // npx 包装进程先死（143）是预期；tsx 子进程异步落盘——轮询等文件出现（≤20s）
711	    let saved = false;
712	    for (let i = 0; i < 100 && !saved; i++) { await sleep(200); saved = existsSync(worldFile); }
713	    check('SIGTERM 优雅退出', exited, `exitCode=${server.exitCode}`);
714	    check('SIGTERM 落盘世界档（room-<code>.json）', saved, worldFile);
715	    server.killGroup(); // 兜底：落盘后仍未退的 tsx 子进程整组击杀（防孤儿占 7901）
716	    if (existsSync(worldFile)) {
717	      const server2 = spawnServer(7905, ['--world', worldFile]);
718	      const log2 = [];
719	      server2.stdout.on('data', (d) => log2.push(d.toString()));
720	      server2.stderr.on('data', (d) => log2.push(d.toString()));
721	      let up2 = false;
722	      for (let i = 0; i < 100 && !up2; i++) { await sleep(200); up2 = log2.join('').includes('ws://0.0.0.0:7905'); }
723	      check('--world 重启成功（常驻房）', up2, log2.slice(-3).join('').slice(0, 200));
724	      if (up2) {
725	        const list3 = await fetch('http://127.0.0.1:7906/rooms').then((r) => r.json()).catch(() => null);
726	        const persisted = (list3?.rooms ?? []).length >= 1;
727	        check('常驻房出现在新服列表（世界存活）', persisted, JSON.stringify(list3?.rooms?.map((r) => r.code) ?? null));
728	        server2.killGroup();
729	      } else {
730	        server2.killGroup();
731	      }
732	    }
733	  }
734	} catch (e) {
735	  // 瞬态异常（vite HMR 全页 reload / context destroyed——开发期并行改码触发）：
736	  // 标记整轮重试（finally 清理端口后由尾部 respawn）；非瞬态如实抛出
737	  const msg = String(e?.message ?? e);
738	  const transient = /destroyed|navigation|Target closed|Cannot read properties of undefined/i.test(msg);
739	  console.log(`[probe] 异常：${msg.slice(0, 160)}（${transient ? '瞬态 → 整轮重试' : '真实失败'}）`);
740	  if (transient && !process.env.ROOMPROBE_RETRY) {
741	    retryFlag = true;
742	  } else {
743	    fail++; // 计入失败再走统一收尾
744	    throw e;
745	  }
746	} finally {
747	  server.killGroup();
748	  await browser.close();
749	}
750	console.log(`\n${pass} passed, ${fail} failed`);
751	if (retryFlag) {
752	  // 瞬态重试：本轮已清理（finally 杀 server/关 browser）→ respawn 自身
753	  const { spawn } = await import('node:child_process');
754	  const child = spawn(process.execPath, [new URL(import.meta.url).pathname], {
755	    env: { ...process.env, ROOMPROBE_RETRY: '1' }, stdio: 'inherit',
756	  });
757	  child.on('exit', (c) => process.exit(c ?? 1));
758	} else {
759	  process.exit(fail ? 1 : 0);
760	}
761	

```


---

## 🤖 Assistant · 2026-08-12T08:34:21.296Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read _loadprobe.mjs, the doc, and 开服.sh, plus server/src/index.ts for CLI options.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:21.472Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/_loadprobe.mjs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:21.506Z

**📎 ToolResult**

```
1	#!/usr/bin/env node
2	/**
3	 * 多人联机容量压测探针（P0.5）：Node 原生实现线协议（scripts/_netfake.mjs），
4	 * 起 K 个假客户端做真实握手（Hello→RequestWorldData→SpawnTileData）后按 15Hz 发
5	 * msg13 玩家状态 + msg27 弹幕快照，房主角色额外发 msg23 NPC 快照；
6	 * 结束时抓 /stats 输出带宽/背压/缓存命中对比表。
7	 *
8	 * 用法（自管生命周期，仿 _roomprobe——不经 run-diag，其 0.5s 强退不适合分钟级压测；
9	 * detached 进程组击杀 + 总时长看门狗，保证不孤儿）：
10	 *   node scripts/_loadprobe.mjs [--clients=16] [--seconds=20] [--density=calm|boss]
11	 *                               [--spread] [--port=7911] [--max-players=255]
12	 *   --spread：一半客户端放在 5000px 外（对比 AOI 收益：无 AOI 时流量应相同，有 AOI 时大幅下降）
13	 *
14	 * 输出：逐房 outKbS / 总出带宽 / sendDrops / msg 直方图 / strip 缓存命中——
15	 * 优化项落地前后各跑一次，把数字记入 docs/multiplayer-design.md §8。
16	 */
17	import { WebSocket, Writer, PROTO_MAGIC, PROTO_VER, Msg, makeTinySave, spawnServer } from './_netfake.mjs';
18	
19	// ---------- 参数 ----------
20	const argv = process.argv.slice(2);
21	const opt = (name, def) => {
22	  const hit = argv.find((a) => a.startsWith(`--${name}=`));
23	  return hit ? hit.slice(name.length + 3) : def;
24	};
25	const CLIENTS = Math.max(2, parseInt(opt('clients', '16'), 10));
26	const SECONDS = Math.max(5, parseInt(opt('seconds', '20'), 10));
27	const DENSITY = opt('density', 'calm');           // calm: 2 发弹幕/人/批  boss: 10 发/人/批
28	const SPREAD = argv.includes('--spread');
29	const PORT = parseInt(opt('port', '7911'), 10);
30	const LOBBY = PORT + 1;
31	const MAX_PLAYERS = parseInt(opt('max-players', '255'), 10);
32	
33	const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
34	
35	// ---------- 起 server（detached 进程组：防"杀 npx 包装留 tsx 孤儿"——2026-08 实踩） ----------
36	const server = spawnServer(PORT, ['--max-players', String(MAX_PLAYERS)]);
37	function killServer() {
38	  try { process.kill(-server.pid, 'SIGKILL'); } catch { try { server.kill('SIGKILL'); } catch { /* 已退 */ } }
39	}
40	
41	// ---------- 总看门狗：SECONDS+30s+人数余量 内必退（防孤儿；百人时收尾统计被事件洪峰拖慢） ----------
42	const watchdog = setTimeout(() => {
43	  console.error('[loadprobe] 总看门狗触发，强制退出（exit 2）');
44	  killServer();
45	  process.exit(2);
46	}, (SECONDS + 30 + Math.ceil(CLIENTS / 10)) * 1000);
47	watchdog.unref?.();
48	
49	let serverOut = '';
50	server.stdout.on('data', (d) => { serverOut += d.toString(); });
51	server.stderr.on('data', (d) => { serverOut += d.toString(); });
52	const waitServer = async () => {
53	  const t0 = Date.now();
54	  for (;;) {
55	    if (serverOut.includes(`ws://0.0.0.0:${PORT}`)) return;
56	    if (server.exitCode !== null) throw new Error(`server 启动失败:\n${serverOut.slice(-2000)}`);
57	    if (Date.now() - t0 > 60_000) throw new Error('server 启动超时');
58	    await sleep(200);
59	  }
60	};
61	
62	// ---------- 主流程 ----------
63	try {
64	  await waitServer();
65	  // 建房（拿 hostToken → 客户端 0 为房主 = NPC 权威源）
66	  const created = await (await fetch(`http://127.0.0.1:${LOBBY}/rooms`, {
67	    method: 'POST', headers: { 'Content-Type': 'application/json' },
68	    body: JSON.stringify({ name: '压测房', public: true, save: makeTinySave(), maxPlayers: MAX_PLAYERS }),
69	  })).json();
70	  if (!created.ok) throw new Error(`建房失败: ${created.error}`);
71	  const code = created.code, hostToken = created.hostToken;
72	  console.log(`[loadprobe] 房间 ${code}  clients=${CLIENTS} density=${DENSITY} spread=${SPREAD} seconds=${SECONDS}`);
73	
74	  const fakes = [];
75	  for (let i = 0; i < CLIENTS; i++) {
76	    const far = SPREAD && i >= Math.ceil(CLIENTS / 2);
77	    const baseX = 1600 + (i % 8) * 60;         // 近距簇：±420px 内互在视野
78	    const baseY = 1600 + Math.floor(i / 8) * 60;
79	    const x0 = far ? baseX + 5000 : baseX;      // 远距组：5000px 外（AOI 外）
80	    const y0 = baseY;
81	    const ws = new WebSocket(`ws://127.0.0.1:${PORT}/${code}${i === 0 ? `?token=${encodeURIComponent(hostToken)}` : ''}`);
82	    ws.binaryType = 'nodebuffer';
83	    const st = { ws, i, slot: -1, joined: false, x0, y0, framesIn: 0, bytesIn: 0 };
84	    ws.on('open', () => {
85	      // Hello（URL 已带 token：路由层注入 urlToken 优先——消息内兜底传空）
86	      ws.send(new Writer(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(`压测${i}`).str('').finish());
87	    });
88	    ws.on('error', () => { /* 收尾时 server 先退 → ECONNRESET 属预期 */ });
89	    ws.on('message', (data) => {
90	      st.bytesIn += data.length;
91	      st.framesIn++;
92	      if (st.joined) return; // 握手完成后不再逐帧解析（百人时下发洪峰会打满探针 CPU）
93	      let p = 0;
94	      const buf = data;
95	      while (p + 3 <= buf.length) {
96	        const len = buf.readUInt16LE(p);
97	        const msgId = buf[p + 2];
98	        if (msgId === Msg.PlayerSlot && st.slot < 0) {
99	          st.slot = buf[p + 3];
100	          // 对齐真实客户端：SyncPlayer → RequestWorldData
101	          ws.send(new Writer(Msg.SyncPlayer).u8(st.slot).str('{"hair":0}').finish());
102	          ws.send(new Writer(Msg.RequestWorldData).finish());
103	        } else if (msgId === Msg.WorldData) {
104	          ws.send(new Writer(Msg.SpawnTileData).i32(100).i32(100).finish());
105	        } else if (msgId === Msg.PlayerSpawn) {
106	          st.joined = true;
107	        }
108	        if (len < 3) break;
109	        p += len;
110	      }
111	    });
112	    fakes.push(st);
113	  }
114	  await sleep(Math.max(4000, CLIENTS * 80));
115	  const joined = fakes.filter((f) => f.joined).length;
116	  console.log(`[loadprobe] 握手完成 ${joined}/${CLIENTS}`);
117	  if (joined < CLIENTS) throw new Error('部分客户端握手失败');
118	
119	  // ---------- 负载注入：15Hz msg13（圆周走动）+ msg27（密度档）+ 房主 msg23 ----------
120	  const projPerBatch = DENSITY === 'boss' ? 10 : 2;
121	  const t1 = Date.now();
122	  while (Date.now() - t1 < SECONDS * 1000) {
123	    const t = (Date.now() - t1) / 1000;
124	    for (const f of fakes) {
125	      const ang = t * 1.2 + f.i;
126	      const x = f.x0 + Math.cos(ang) * 120;
127	      const y = f.y0 + Math.sin(ang) * 120;
128	      f.ws.send(new Writer(Msg.PlayerState)
129	        .u8(f.slot).u8(8).u8(4).u8(0)
130	        .f32(x).f32(y).f32(Math.cos(ang) * 2).f32(Math.sin(ang) * 2)
131	        .finish());
132	      // msg27：各自的弹幕互播（netId = slot<<24 | k，防撞号）
133	      const w = new Writer(Msg.SyncProjectile);
134	      w.u16(projPerBatch);
135	      for (let k = 0; k < projPerBatch; k++) {
136	        w.u32(((f.slot & 0xff) << 24) | (k & 0xffffff));
137	        w.u8(0); w.str('1');
138	        w.i16(10); w.i16(0);
139	        w.f32(x + k * 8); w.f32(y + k * 8); w.f32(3); w.f32(0);
140	      }
141	      f.ws.send(w.finish());
142	      // 房主 msg23：24 条 NPC 快照（真实房主每批上限同值）
143	      if (f.i === 0) {
144	        const w23 = new Writer(Msg.SyncNPC);
145	        w23.u16(24);
146	        for (let k = 0; k < 24; k++) {
147	          w23.u32(k + 1); w23.str(`v_${k + 100}`);
148	          w23.f32(x + k * 16); w23.f32(y + k * 16); w23.f32(1); w23.f32(0);
149	          w23.i16(100); w23.i16(100); w23.u16(0); w23.u8(0);
150	        }
151	        f.ws.send(w23.finish());
152	      }
153	    }
154	    await sleep(66); // ≈15Hz
155	  }
156	
157	  // ---------- /stats 汇总 ----------
158	  // 先断开全部假客户端止住收发洪峰（百人时事件风暴会拖死收尾），再取快照；
159	  // 平均出带宽用累计字节自算（outBps 1s 采样在饱和场景不可信）
160	  for (const f of fakes) { try { f.ws.close(); } catch { /* 已关 */ } }
161	  await sleep(1500);
162	  const stats = await (await fetch(`http://127.0.0.1:${LOBBY}/stats`)).json();
163	  const room = stats.rooms[0];
164	  const inbound = fakes.reduce((s, f) => s + f.bytesIn, 0);
165	  const outboundTotal = room.topMsgs.reduce((s, m) => s + m.kb, 0) * 1024; // Top5 已覆盖绝大部
166	  const avgOutKbS = outboundTotal / 1024 / SECONDS;
167	  console.log('\n===== /stats 汇总 =====');
168	  console.log(`平均出带宽    : ${avgOutKbS.toFixed(2)} KB/s（${(avgOutKbS / 1024).toFixed(2)} MB/s，累计自算）`);
169	  console.log(`每客户端均摊  : ${(avgOutKbS / Math.max(1, CLIENTS)).toFixed(2)} KB/s`);
170	  console.log(`客户端总入站  : ${(inbound / 1024).toFixed(1)} KB（${(inbound / SECONDS / 1024).toFixed(2)} KB/s）`);
171	  console.log(`背压丢弃      : ${stats.total.sendDrops} 帧`);
172	  console.log(`strip 缓存    : hit=${room.stripHit} miss=${room.stripMiss}`);
173	  console.log('msg 出流量Top5:', room.topMsgs.map((m) => `${m.msg}(${m.kb}KB×${m.n})`).join('  '));
174	  console.log(`stalePos 计数 : ${room.stalePos}`);
175	  const expect = SPREAD ? '（spread 模式：AOI 生效时近距簇内流量应远低于无 AOI 基线）' : '';
176	  console.log(`\n[loadprobe] 完成。把本表数字记入 docs/multiplayer-design.md §8 ${expect}`);
177	
178	  for (const f of fakes) { try { f.ws.close(); } catch { /* 已关 */ } }
179	  server.kill('SIGTERM'); // 走优雅退出（SIGTERM 落盘）；1s 未退则整组击杀
180	  setTimeout(() => killServer(), 1000).unref?.();
181	  setTimeout(() => process.exit(0), 300);
182	} catch (e) {
183	  console.error('[loadprobe] 失败:', e.message);
184	  killServer();
185	  setTimeout(() => process.exit(1), 300);
186	}
187	

```


---

## 🤖 Assistant · 2026-08-12T08:34:21.652Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/开服.sh"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:21.823Z

**📎 ToolResult**

```
1	#!/bin/bash
2	# SandboxWorld 一键开服：把本文件放到项目根目录（SandboxWorld/）下，运行: bash 开服.sh
3	# --world 载入的房间为常驻房（空房不回收），首位进房者自动成为房主；
4	# 全部房间每 300s 自动落盘 worlds/room-<码>.json，Ctrl-C 也会存档退出（P3.1）。
5	cd "$(dirname "$0")/server" 2>/dev/null || { echo "✗ 请把此脚本放到项目根目录(SandboxWorld/) 再运行"; exit 1; }
6	[ -d node_modules ] || { echo "安装依赖…"; npm install || exit 1; }
7	# 优先用 worlds/ 里最新的存档作为常驻房；没有则开空 lobby（玩家建房上传存档）
8	W=$(ls -t worlds/*.json 2>/dev/null | head -1)
9	if [ -n "$W" ]; then
10	  echo "▶ 常驻房存档: $W"
11	  exec npx tsx src/index.ts --world "$W" "$@"
12	else
13	  echo "▶ worlds/ 无存档，仅开 lobby（玩家建房时上传世界存档）"
14	  exec npx tsx src/index.ts "$@"
15	fi
16	

```


---

## 🤖 Assistant · 2026-08-12T08:34:23.226Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read the design doc and server index.ts CLI.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:23.369Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:23.401Z

**📎 ToolResult**

````
1	# 多人联机设计规范（WebSocket，对齐原版 1.4.5.6 + 选做优化）
2	
3	> 状态：**储备方案**（完成调研与设计，待启用实施）。基准源码 Terarria1456；
4	> 涉及原版行号均已核对。所有"优化"项单列 §8 并标注 `--opt` 开关名，
5	> 默认关闭（默认行为与原版 1:1），逐项独立可开。
6	
7	---
8	
9	## 0. 原版架构要点（调研结论速查）
10	
11	```
12	服务器 (netMode==2, 60Hz)                 客户端 (netMode==1)
13	├─ NPC.SpawnNPC()（仅服务器, Main.cs:17720） ├─ 本地玩家完整模拟
14	├─ npc.UpdateNPC()（服务器跑 AI）           ├─ 420t 兜底上报 msg13 + 事件驱动即时
15	├─ WorldGen.UpdateWorld()（液体/电路, :17921）├─ 远端玩家 = msg13 覆写 + netOffset 平滑(300px)
16	├─ UpdateServer()（:64004，CheckSection 驱动）└─ tile 收包应用 + 本地帧动画
17	└─ TCP 7777 / 帧=[ushort len][byte msgId][payload]
18	```
19	
20	- **混合权威**：NPC/世界/事件服务器权威；玩家位置/物品栏/伤害/owner 弹幕客户端上报、服务器中继
21	- 世界不传文件：msg7 元数据 → 出生点 5×3 section → CheckSection 3×3 按需
22	- Host&Play = 回环客户端（`myPlayer=255`；IsLocalHost() 判 host，NetMessage.cs:2874）
23	- 握手：1 Hello("Terraria319") → 3 slot → 客户端全量上传 → 6 → 7 WorldData → 8 → 10 sections → 12 Spawn → State=10 → 129
24	- 双轨消息：MessageID 0..161 + msg82 内嵌 NetModule（15 个，注册顺序即 ID）
25	- 帧上限 65535B（ushort len）；缓冲 131070B（MessageBuffer.cs:29-37）；小端
26	
27	## 1. 传输与协议规范
28	
29	### 1.1 WebSocket 层
30	
31	| 项 | 规范 | 说明 |
32	|---|---|---|
33	| 传输 | 二进制 WebSocket（ArrayBuffer） | 文本帧一律忽略并计异常 |
34	| 端口 | 7777（对齐原版 DefaultPort） | `--port` 可改 |
35	| 帧内格式 | **保留 `[u16 len][u8 msgId][payload...]`** | 一条 WS 消息可串联多个原版包（合包省帧开销）；粘包逻辑照搬 CheckBytes（NetMessage.cs:2504-2564） |
36	| 字节序 | 小端（LE） | 对齐 .NET BinaryWriter |
37	| 包上限 | 65535B（同原版，超限丢弃+告警） | 超大载荷必须走分片协议（§1.4） |
38	| WS 压缩 | **禁用 permessage-deflate** | msg10 内层已有 deflate，双层压缩纯浪费 CPU；若开则必须 `server_no_context_takeover` |
39	| Nagle | Node `ws` 底层 socket `setNoDelay(true)` | 对齐原版 TcpSocket（TcpSocket.cs:35-38），60Hz 小包不积团 |
40	
41	### 1.2 版本协商
42	
43	```
44	Hello(msg1) payload: { magic: "SW1", protoVer: u16, gameVer: string, features: u32 }
45	```
46	- `protoVer` = 本协议文档的修订号（初始 1）；不一致由服务器决定踢出（msg2）或降级（首版只踢，对齐原版版本校验语义）
47	- `features` 位图：bit0 SSC（服务器侧角色）、bit1 section 缓存、bit2 插值缓冲 …——未知 bit 忽略（前向兼容）
48	- 未知 msgId **跳过不断连**（原版 `b >= MessageID.Count` 丢弃，MessageBuffer.cs:137-139 同语义）
49	
50	### 1.3 编码惯例（照搬 .NET BinaryWriter 语义）
51	
52	| 类型 | 编码 |
53	|---|---|
54	| 数值 | LE 定宽（u8/i8/u16/i16/u32/i32/f32）——**不用 varint**（对齐原版，可对照逐字段校对） |
55	| 字符串 | u7-bit 前缀长度 + UTF-8（BinaryWriter.Write(string) 惯例：每字节高位续位） |
56	| bool | u8（0/1） |
57	| Vector2 | f32 x, f32 y |
58	| BitsByte | u8 位域（对齐原版大量 `BitsByte` 用法，位义在消息字典中定义） |
59	| 可选字段 | BitsByte 先行声明"哪些字段存在"，存在才写（对齐原版 msg13/23/27 惯例） |
60	
61	### 1.4 分片协议（超 64KB 载荷，如大型 section 压缩结果或未来 SSC 全量背包）
62	
63	原版无此机制（靠 section 200×150 本身小于上限，Deflate 后 30K 级）。我们保留：
64	- 逻辑通道：`{u8 chanId, u8 flags, u16 fragIdx, u16 totalFrags, payload}`，flags: bit0=first, bit1=last
65	- 收端按 chanId 组装，超时 10s 丢弃
66	- 仅在实测单 section 超 60KB 时启用（预留，首版不实现）
67	
68	### 1.5 NetModule 表（显式建表——原版靠注册顺序隐式编码，是移植坑）
69	
70	| moduleId | 模块 | 我们的状态 |
71	|---|---|---|
72	| 0 | Liquid（脏矩形批量，按 section 过滤） | P3 实现 |
73	| 1 | Text（聊天；命令服务器执行） | P4 实现 |
74	| 2 | Ping（RTT 样本） | P0 实现 |
75	| 3-14 | Ambience/Bestiary/Creative/Pylon/Particles/Banner/Crafting/TagEffect/Leash/UnbreakableWall | 暂缓（功能未到，占位跳过） |
76	
77	## 2. 消息字典（首期实现范围，字段对齐原版）
78	
79	> 完整语义见调研报告；此处给首期 wire format。`C→S`/`S→C`/双向。
80	
81	### P1 握手/世界
82	
83	**msg1 Hello（C→S）**：`string magic/protoVer 特性位（§1.2）`
84	**msg2 Kick（S→C）**：`u8 原因码, string 说明`
85	**msg3 PlayerSlot（S→C）**：`u8 slot, u8 特性位`（服务器从 0..254 分配空闲 slot）
86	**msg6 RequestWorldData（C→S）**：空
87	**msg7 WorldData（S→C）**：对齐 NetMessage.cs:210-393 字段集（裁剪项注释）：
88	```
89	f64 time; u8 dayTime; u8 bloodMoon; u8 eclipse; u8 moonPhase
90	u16 maxTilesX; u16 maxTilesY
91	i32 spawnX; i32 spawnY
92	f32 worldSurface; f32 rockLayer
93	i32 worldId; string worldName
94	u8 gameMode; string uniqueId(裁剪:传 worldId 字符串)
95	u8 flagsBits×N（downedBoss/hardMode/事件 → 对应 world.flags 逐位）
96	（裁剪：风/云/沙尘暴/种植背景——功能未到；预留 u16 reservedBits 保持前向兼容）
97	```
98	**msg8 SpawnTileData（C→S）**：`i32 spawnX, i32 spawnY`（客户端给出生点，服务器回 5×3 section，MessageBuffer.cs:647-860）
99	**msg9 StatusText（S→C）**：`i32 sectionCount`（进度条）
100	**msg10 TileSection（S→C）**：
101	```
102	i32 xStart; i32 yStart; i16 width(200); i16 height(行块 150)
103	[deflateRaw 后的字节]：
104	  每 tile 位标志 u8（对齐 CompressTileBlock 位义）：
105	    active/type>255/type/frameX/frameY/wall/liquid/liquidType/wire1-4/half/slope/actuator/inActive/color/wallColor
106	  + 存在通道的数据；RLE 重复计数
107	尾部：u16 chestCount + chests{u16 x,u16 y,items...}；signs 同构
108	```
109	首版实现顺序：**裸 RLE 先行（头部加 u8 codecVer=0），codecVer=1 再上 deflateRaw**——两版可共存。
110	**msg12 PlayerSpawn（双向）**：`u8 slot, i32 x, i32 y, i32 respawnTimer, u8 团队/死亡计数`
111	**msg129 FinishedConnecting（S→C）**：空
112	**msg154 / module2 Ping（双向）**：`i32 clientTs`；回传原值，客户端算 RTT
113	
114	### P2 玩家
115	
116	**msg4 SyncPlayer（双向）**：`u8 slot, string appearanceJson`（Appearance：hair/skinVariant/7×RGB/difficulty，~100B）
117	**msg5 SyncEquipment（双向）**：`u8 slot, u8 invSlot, i16 itemId, u8 prefix(裁剪), i16 stack, u8 favorited`
118	**msg13 PlayerControls（C→S→广播）**：对齐 NetMessage.cs:429-494：
119	```
120	u8 slot
121	BitsByte ctrlA（left/right/up/down/jump/使用/朝向1/朝向2）
122	BitsByte ctrlB（速度非零/坐骑/睡觉/重力翻转/潜行/盾/ghost/虚空袋）
123	u8 selectedItem; f32 x; f32 y;
124	[速度非零] f32 vx, f32 vy
125	[坐骑] u8 mountType(裁剪:仅标志位)
126	```
127	**msg14/16/42/50**：active / `u8 slot, i16 life, i16 lifeMax` / mana 同构 / buff 列表（裁剪：暂传计数+占位）
128	**msg21/22 SyncItem/ItemOwner（双向）**：掉落物（slot=400 表示"请服务器分配"，对齐原版）；归属 `u8 itemSlot, u8 playerSlot`
129	
130	### P3 实体
131	
132	**msg23 SyncNPC（S→C）**：对齐 NetMessage.cs:669-745：
133	```
134	u8 slot; f32 x,y,vx,vy; u16 target; u8 方向位
135	BitsByte aiFlags（ai[0..3] 哪些非零）+ 存在的 f32 ai[]
136	i16 netID(vanillaId); u8 life 档位(0:sbyte/1:short/2:int) + life
137	```
138	**msg27/29 SyncProjectile/Kill（双向）**：`i16 identity, f32 x,y,vx,vy, u8 owner(强制=whoAmI), i16 type, ai[0..2], i16 damage, f32 knockBack`——服务器收到强制 `owner=slot`（对齐 MessageBuffer.cs:1742）
139	**msg28 DamageNPC（C→S→广播）**：`u8 npcSlot, i16 damage, f32 knockBack, u8 hitDir+1, u8 crit`
140	**module0 NetLiquid（S→C）**：`u16 rectCount, 每 rect{u16 x,y,w,h} + 每格 u8 liquid + u8 type`（对齐按 section 过滤；节流 30t/次）
141	**module1 NetText（双向）**：聊天 `u8 authorSlot, string text, u8 r,g,b`；命令 `/kick /time …` 服务器执行（对齐 ChatHelper）
142	
143	### P4 交互
144	
145	**msg17 TileManipulation（C→S）**：`u8 action(0=挖/1=放/2=拆墙/3=放墙/…), i32 x, i16 data1, i16 data2`（action 枚举对齐原版 0..25）；服务器执行 WorldGen 等价逻辑后广播 msg17，**失败回 SendTileSquare 纠正**（MessageBuffer.cs:1253-1263 语义）
146	**msg20 SendTileSquare（S→C，必要时 C→S）**：`i16 x,y; u8 w,h; 每 tile {BitsByte×3 + 存在通道}`（对齐 NetMessage.cs:524-626），只广播 SectionRange 覆盖者
147	**msg19 门 / 31-34 箱子四条 / 59 开关 / 61 Boss 召唤 / 65 传送**：薄事件包，字段对齐原版
148	**msg90 InstancedItem**：私有掉落（`u8 playerSlot` 前缀，只发该玩家）
149	
150	## 3. 服务器架构细则（server/，Node+TypeScript）
151	
152	### 3.1 目录与构建
153	
154	```
155	server/
156	├─ package.json            # 依赖: ws, tsx; type: module; 无 DOM lib tsconfig
157	├─ tsconfig.json           # { lib:["ES2022"], paths: { "@game/*": ["../game/src/*"] } }
158	├─ src/
159	│  ├─ index.ts             # CLI(--port/--world/--public/--save-interval) + 启动
160	│  ├─ net/Buffer.ts        # 读/写缓冲（131070B 上限对齐）、CheckBytes 粘包
161	│  ├─ net/RemoteClient.ts  # slot 状态机(State -1..10)、TileSections 位图、
162	│  │                       #   SpamUpdate 限流器、TimeOutTimer、发送队列
163	│  ├─ net/dispatch.ts      # msgId → handler 分发（对应 MessageBuffer.GetData）
164	│  ├─ net/encode.ts        # 全部 S→C 编码器（对应 NetMessage.SendData）
165	│  ├─ game/ServerGame.ts   # 60Hz 主循环：NPC AI+刷怪+液体+电路+Wiring 事件
166	│  ├─ game/Sections.ts     # CompressTileBlock(RLE/deflate)、CheckSection、位图
167	│  ├─ game/NpcSync.ts      # msg23 快照调度（netUpdate 收集 + netSpam 限流 + section 过滤）
168	│  └─ world/WorldHost.ts   # 世界加载/生成/定期存档（复用 @game 引擎模块）
169	└─ tests/                  # vitest 复用根配置
170	```
171	
172	- **复用清单**（全部验证过零 DOM）：`WorldGen.generateWorld`、`settleWorldLiquids`、`LiquidSim`、`SaveFile.{saveGame,loadSaveData}`、`World/TileStore`、`VanillaSpawner`、`rng`。加载路径用相对 import + tsconfig paths，构建用 tsx 直跑（开发）与 tsc 产物（部署）双轨
173	- 唯一已知雷：`SaveFile.ts` 的 `btoa/atob`（Node 16+ 原生）✓
174	
175	### 3.2 进程模型（对齐原版线程语义）
176	
177	- Node 单线程 = 原版"IO 线程搬字节 + 主线程跑逻辑"的天然退化：WS `onmessage` 只做 `buffer.append(bytes)`；**全部解析与游戏逻辑在 60Hz `setInterval` tick 内**（对应 UpdateServerInMainThread）
178	- tick 超预算（>12ms）告警并计入直方图（§6 监控）；连续超限触发降级（NPC 同步降频）
179	- 世界加载/生成（重 CPU，可达数秒）**不得阻塞 tick**：启动期允许（无客户端），运行期再生成走子进程 `worker_threads`（预留）
180	
181	### 3.3 生命周期与存档
182	
183	| 事件 | 行为 |
184	|---|---|
185	| 启动 `--world <id>` | 加载 IndexedDB？否——服务器读**文件**：`worlds/<id>.json`（saveGame 格式）；缺省自动生成小世界 |
186	| 定期 `--save-interval`（默认 300s） | 全量 saveGame 写文件（原子写：tmp+rename）；对齐原版"退出存档"+防崩溃增强 |
187	| 最后一人离开 10min（`--empty-timeout`） | 可选停服存档（公网常驻则不启） |
188	| SIGINT/SIGTERM | 存档 + 优雅断开（msg2 原因码=server_shutdown） |
189	
190	### 3.4 广播管线与带宽预算
191	
192	- 每客户端**每 tick 发送字节预算**（默认 16KB，`--budget`）：优先级 心跳 > 玩家 > tile 事件 > NPC 快照 > 物品 > 液体；超预算顺延下 tick（对应原版 netSpam 思想的系统化）
193	- **section 压缩缓存**：`Map<sectionKey, {data, worldVersion}>`——世界 tile 静态为主，同 section 多客户端/重连复用压缩结果；任何 msg17/20 修改使相关缓存失效（优化项 §8.3）
194	- 合包：单 tick 内同客户端待发 ≤2KB 的包合并为一条 WS 消息（帧内原版包格式不变，对齐 §1.1）
195	
196	### 3.5 内存
197	
198	- 中世界 6400×1800 ≈ 46MB（TileStore）+ section 缓存（200×150 块压缩后均 ~30KB × 已压缩块数）+ 客户端缓冲 131KB×256 上限。设计余量 512MB/世界
199	- 进房**不传整图**（原版同款 section 流）→ 无 packWorld transfer 语义问题（worldPacket 仅用于服务器内部/单机）
200	
201	## 4. 客户端架构细则（game/src/net/）
202	
203	### 4.1 模块
204	
205	```
206	src/net/
207	├─ NetMode.ts        # netMode 0/1/2 + isServer/isClient 谓词（对齐原版裸比较语义）
208	├─ MessageBuffer.ts  # 收包缓冲 + CheckBytes + msgId 分发（与 server/net/Buffer.ts 同源双份或提 shared/）
209	├─ ClientNet.ts      # WebSocket 连接 + 握手状态机 + 重连(§6.4) + RTT 采样
210	├─ NetPlayers.ts     # slot→远端 Player 实例池；msg13 应用 + netOffset 平滑
211	├─ NetEntities.ts    # npcSlot/projIdentity→本地 Enemy/投射物实例 + 快照应用
212	└── applyTiles.ts    # msg10/17/20 → store.setTile/setWall/...（复用 onTileChanged 事件链，
213	                      #   禁用 *Silent 与直写数组——调研确认 7 个下游全靠事件链）
214	```
215	
216	### 4.2 Game 集成点
217	
218	| 位置 | 改动 |
219	|---|---|
220	| `fixedUpdate` 头部 | `net.pump()`（解析入包、应用快照）——1 行 |
221	| 玩家输入 `Game.ts:815-818` | 联网时额外打包 msg13（事件驱动：位置变化>1px 或按键变化；兜底 420t 对齐原版，见 §8.1 优化） |
222	| `trySpawnEnemy`/`LiquidSim.step`/`fellTree`/Boss 召唤/箱子写入 | **netMode==1 时全部短路**，改为发消息（服务器权威侧执行） |
223	| 渲染 | 远端 Player 包装成带 draw 的实体塞 entities 列表（蹭现成 y 排序），drawPlayer 循环复用 |
224	| `this.player` | 保留为"本地玩家"别名（避免 200+ 处机械改），远端玩家独立桶 |
225	| 迷雾 markExplored | 仅本地玩家驱动（天然免费，存档本就不含 explored） |
226	| Boss 血条/公告/老人重生 | 仅服务器侧触发广播（客户端收事件渲染） |
227	
228	### 4.3 插值（默认对齐原版 + 可选增强）
229	
230	- **默认（1:1）**：msg13 到达直接覆写 + `netOffset` 平滑（NPC.cs:91321-91357 同款：距离 ≤300px 累积偏移，每 tick 衰减回 0）
231	- **可选 `--opt-interp`（§8.2）**：快照缓冲 100ms + 渲染插值（Entity 渲染位置 = lerp(prev, cur, α)），逻辑位置仍是最新快照——不改判定只改视觉
232	- 本地玩家零延迟（客户端权威，原版同款）
233	
234	## 5. 同步职责矩阵（与原版逐格对齐）
235	
236	| 状态 | 服务器 | 拥有者客户端 | 其他客户端 |
237	|---|---|---|---|
238	| tile/墙/液体/电路 | 权威模拟+下发（msg10/17/20/module0） | 上报请求 | 事件链应用 |
239	| 时间/天气/事件/flags | 权威（msg7/18） | — | 应用 |
240	| NPC 生成/AI/血量 | 权威 + msg23/28 广播 | 上报伤害 | netOffset 平滑 |
241	| 玩家位置/动作 | 中继覆写广播 | 权威模拟+上报 | 覆写+平滑 |
242	| 玩家物品栏/生命 | 中继（SSC 可选时权威） | 权威 | 应用 |
243	| 弹幕 | 中继+section 过滤 | **owner 权威**（跑 AI 上报 msg27） | 播放 |
244	| 掉落物 | 分配 slot+归属+广播 | 上报生成/拾取 | 应用 |
245	| 聊天 | 命令执行+广播 | 上报 | 显示 |
246	
247	## 6. 工程最佳实践
248	
249	### 6.1 心跳与超时
250	- module2 Ping 每 3000t（50s）双向；RTT 滑动均值上报 UI（ping 显示）
251	- 7200t（120s）无任何入包 → 判超时（对齐原版 TimeOutTimer）；WS close/ping/pong 底层异常直接触发同路径
252	
253	### 6.2 背压与限流
254	- 服务器发送：§3.4 字节预算 + netSpam 限流（原版常量：弹幕 60、tile 500、液体 30 档）
255	- 服务器接收：**轻量 spam 计数默认开**（原版 `SpamCheck=false` 是已知宽松点，我们作为偏离项 §8.6 记录：挖块 >500/min 告警、>2000/min 踢）——防一人卡全场
256	- WS 缓冲水位监控：`bufferedAmount > 256KB` 的客户端标记慢速，跳过非关键广播（NPC 快照降频），避免雪崩
257	
258	### 6.3 安全
259	- slot 覆写 `index = whoAmI` 全点位强制（对齐原版）；弹幕 owner 强制、敌对弹幕拒收（MessageBuffer.cs:1743-1746）
260	- State<10 白名单门禁（MessageBuffer.cs:161-171 原样保留——防乱序与未握手发包）
261	- 未收 section 的客户端 tile 操作按原版"无掉落"处理（msg17 flag13 语义）
262	- 伤害上报信任但**记录**（可选 §8.7：单次伤害 > 理论上限 3 倍 → 踢，默认关）
263	- 密码：msg37/38 保留（`--password`）；banlist 文件（对齐 IsBanned）
264	
265	### 6.4 断线重连（**原版没有，必备增强**）
266	- 原 msg3 附 `u32 sessionToken`；断线 120s 内携 token 重连 → 服务器保留 slot/位置/物品栏，补发其 TileSections 缓存 + 周边 section + 全体玩家/NPC 快照，跳过完整握手
267	- 超时或服务器重启 → 客户端走全新握手（SSC 开启时角色从服务器档恢复，否则提示）
268	- 客户端侧：WS close 自动退避重连（0.5s/1s/2s/5s 封顶），期间本地玩家冻结 + "重连中"遮罩（不做本地预测——玩家本就客户端权威，重连后从最后位置继续，物品栏本地保留）
269	
270	### 6.5 观测性
271	- 服务器 `/stats`（HTTP :7778，只绑 localhost 或 `--stats`）：在线 slot/RTT 直方图/tick 耗时直方图/每客户端带宽与缓冲水位/NPC 数/液体活动格/section 缓存命中率
272	- 结构化日志（JSON 行）：连接/断开/踢出（含原因码）/存档/异常，探针可直接断言
273	- 每 3600t 广播 msg7 时附带校验和（world flags + time），客户端静默丢弃冲突（防御性）
274	
275	### 6.6 测试策略（沿用仓库探针范式）
276	| 层 | 手段 |
277	|---|---|
278	| 编解码 | vitest 单测：每条消息 roundtrip + 与 C# 字段布局逐字节对照的黄金样本（手工从原版抓或推导） |
279	| 协议 | Node 内回环：假客户端按握手序列发包，断言状态机转移与回包序列 |
280	| 一致性 | puppeteer 双浏览器探针：A/B 连同一 server，断言共享状态（tile hash/玩家位移/NPC hp）逐 tick 一致 |
281	| 稳定性 | 长稳脚本：随机操作流 10min + 断线注入 + 存档恢复比对 |
282	
283	## 7. 局域网与部署
284	
285	### 7.1 LAN
286	- server 启动 UDP :8888 每 1000ms 广播（载荷对齐原版 BroadcastThread：`int 魔数 1010, int port, string 世界名, string 主机名, u16 尺寸, bool 猩红, int 模式, u8 上限, u8 在线, bool 困难`）
287	- 浏览器无 UDP → 三档加入方式：
288	  1. **手动输 IP**（首版，`192.168.x.x:7777`，同原版主路径）
289	  2. 本机代理发现：server 附带 HTTP `:7778/lan`（CORS 开放），客户端页面试探常见网关段（`http://<网关>.1..254:7778/lan` 代价高——仅作为实验项）
290	  3. mDNS 广播 `sandboxworld._tcp`（`bonjour` 包；浏览器不解析 mDNS，供原生客户端/工具用）
291	- 局域网与公网**同一进程同一协议**，仅 `--public` 时关 UDP 广播、开 stats 鉴权
292	
293	### 7.2 部署
294	- 单文件 `node dist/index.js --port 7777 --world 1 --save-interval 300`；systemd/PM2 单进程
295	- 反代注意：WebSocket 需要 `nginx: proxy_set_header Upgrade/Connection`；禁用反代层压缩（内层已有）
296	
297	### 7.3 中央服务器房间制（v3，已实现）
298	
299	单进程双端口：**WS :port（默认 7777）+ HTTP lobby :port+1（默认 7778）**。一台中央服务器承载多房，每房一个世界实例。
300	
301	**HTTP lobby**（`server/src/index.ts`）：
302	
303	| 端点 | 行为 |
304	|---|---|
305	| `POST /rooms` | 建房。body `{name, public, protectTiles, protectItems, save}`（save=存档 JSON，≤256MB）→ `{code, hostToken}`。hostToken=`randomUUID()`，仅建房端持有 |
306	| `GET /rooms` | **公开**房间列表（非公开房不出现，只能码进） |
307	| `GET /rooms/<6位码>` | 码校验（加入前置检查；非公开房也可查） |
308	| `DELETE /rooms/<码>?token=` | 房主关房（token 校验） |
309	| `GET /lan` | `{magic:1010, port, rooms, lanIps}`（LAN 发现/本机 IP 分享） |
310	
311	全端点带 CORS + `Access-Control-Allow-Private-Network`（Chrome PNA）。房间码=6 位随机数字查重；上限 32 房；创建满 1 分钟且无人满 5 分钟回收。
312	
313	**WS 路由**：URL = `/<6位码>[?token=<hostToken>]` → `Room`（`server/src/room.ts`）。token 经路由层注入 `RoomClient.urlToken`；Hello 消息内 token 兜底。首携正确 token 的连接=房主（`hostJoined` 单例防多主）。
314	
315	**双保护**（用户需求："除房主外没有方块编辑毁坏能力；物品保护=不能取放房间物品，自动拾取豁免"）：
316	- **破坏保护 protectTiles**：服务端权威——非房主 `TileBatch` 整包拒绝 + 对前 8 个 op 回发权威快照 correctionFrame（对齐原版 SendTileSquare 纠正语义，清客户端乐观预测）
317	- **物品保护 protectItems**：`RoomPolicy`（msg200）下发 → 客户端集中门禁（`Game.netCanEditTile()/netCanChestInteract()`，挂在 tryMine/tryPlace/tryPlaceWall/useWireTool/interactAt/tryOpenChest 入口；自动拾取不门禁）。v1 无箱子内容同步，门禁开箱即拦截
318	- 单人（`net==null`）/房主恒放行；拒绝提示 2s 节流
319	
320	**客户端**（`game/src/net/ClientNet.ts` + `game/src/ui/MultiplayerSelect.ts` v3）：
321	- 服务器地址输入（默认 `127.0.0.1:7778`，lobby 端口约定 WS=lobby-1）→ 房间列表点击加入 / 码加入 / 建房表单（选存档+公开+双保护勾选 → POST → 显示 6 位码 → 进入房间）
322	- `Msg.RoomPolicy=200`：S→C `{roomCode, roomName, isHost, protectTiles, protectItems}`，存 `net.policy`；非房主受控时 toast 提示
323	
324	**探针**：`game/scripts/_roomprobe.mjs`（建房→列表/码校验→房主 token 进房→访客码加入→互见→非房主 op 被拒回滚→房主 op 中继→非公开房列表过滤/码可查，14 断言）。`__swFlow.createRoom/joinRoom` 为探针桥。
325	
326	## 8. 原版可优化点清单（全部默认关，`--opt-*` 独立开关）
327	
328	| # | 原版行为 | 问题 | 优化（默认关） | 代价/风险 |
329	|---|---|---|---|---|
330	| 8.1 | msg13 兜底 420t（7s！）纯事件驱动 | 网络抖动时远端玩家僵直；Web 场景 RTT 低用不满 | `--opt-posrate`：位置/速度变化驱动的节流上报（≥60ms 间隔、变化>1px 才发），目标 10-15Hz 有效率 | 带宽 ↑（每客户端 ~1KB/s×N）；与原版抓包不可比 |
331	| 8.2 | netOffset 事后平滑（300px 半径硬阈值） | 瞬移感（快照间隔不均时抖动） | `--opt-interp`：100ms 快照缓冲+渲染插值（§4.3） | 视觉延迟 +100ms；实现量中 |
332	| 8.3 | msg10 每次实时压缩 | 重连/多客户端重复压缩同一 section | `--opt-seccache`：压缩缓存（§3.4，含失效跟踪） | 内存 ↑（~30KB/块）；tile 频繁修改区命中率低 |
333	| 8.4 | NPC msg23 逐包广播、跳 4 次容忍 | 带宽浪费（同 section 多客户端重复字段） | `--opt-deltasnap`：每 NPC 每秒 1 次全量 + 期间增量（仅变化字段位图） | 协议复杂化；偏离原版包格式 |
334	| 8.5 | 玩家物品栏完全客户端权威 | 换设备/掉线丢进度（原版靠 SSC 服务器选项） | `--opt-ssc`：ServerSideCharacter 对齐原版 msg7 位（服务器存角色档） | 原 1.4 已有此开关，实为对齐而非偏离；实现量中 |
335	| 8.6 | SpamCheck 默认关 | 一人刷爆全场 | `--opt-spam`：§6.2 轻量限流默认开 | 误伤低概率（挖得快的高玩） |
336	| 8.7 | 伤害数值完全信任 | 秒杀外挂 | `--opt-dmgcheck`：伤害上限校验（默认 3 倍理论值踢） | 联动/反弹类伤害需白名单；默认关 |
337	| 8.8 | 无断线重连 | 掉线=丢进度退房 | §6.4 session token 重连（**此项建议直接默认开**，非原版但 Web 场景刚需；已在 §4.1 列为必备） | 服务器需短时保留 slot 状态 |
338	| 8.9 | TCP 队头阻塞 | 大 section 阻塞小指令包 | WS 无法多路复用；缓解=msg10 分片走低优先级通道+每 tick 预算（§3.4 已含） | — |
339	| 8.10 | 时间/事件全量靠 msg7 周期刷新 | 进程内时钟漂移 | 客户端 clock 以 msg18 事件驱动对齐（§2 P4 已含 msg18=SetTime） | 对齐原版语义，无代价 |
340	
341	> 原则：**默认路径逐字段对齐原版可抓包比对**；优化项只在明确收益点开启，且每项独立开关、可在 /stats 中看到生效状态。
342	
343	## 8bis. 2026-08 容量优化批（已实施，PROTO_VER=4）
344	
345	> 起因：容量估算发现带宽 O(N²)（无 AOI 全房广播）、无观测（静默丢帧）、无持久化（房主退房世界蒸发）。
346	> 本批落地 P0-P3，探针 `_roomprobe.mjs`（36→50+ 断言）+ 压测 `_loadprobe.mjs` 验收。
347	
348	| 项 | 内容 | 位置 | 实测/备注 |
349	|---|---|---|---|
350	| /stats 观测 | `GET /stats`：全局+逐房+逐客户端（in/out 字节、buffered 高水位、sendDrops、outBps 1s 采样、msg 直方图、stripHit/miss、stalePos） | `server/src/stats.ts`、`Room.send` 埋点 | 优化前的一切调优都是盲调——本项先行 |
351	| 分级背压 | ≤1MB 正常；1-4MB 只丢 prio=1（实体快照类）；>4MB 全丢，全计数 | `Room.send(c, frame, prio)` | 替代旧"超 4MB 静默丢" |
352	| 单房人数上限 | `--max-players` + `POST /rooms.maxPlayers`（钳 2-255）；RoomPolicy 尾部 u16 maxPlayers；UI 列表 online/max | `Room.opts.maxPlayers` | slot 物理上限恒 255（重连复位按物理上限校验） |
353	| 内存护栏 | `--world-budget`（默认 2GB，w×h×11B 估算）+ `--upload-limit`（默认 96MB） | `server/src/index.ts` | 注意 `2<<30` 溢出 int32 的坑（已踩过） |
354	| **实体 AOI** | msg13 半径 1920px / msg23+27 半径 1280px，滞回外径 ×1.6；接收端位置取其上行 msg13；>5s 无位置按全视野兜底（stalePos 计数） | `Room.broadcastAt` + `aoiBlind` | O(N²)→O(N·k)；msg21 掉落不做 AOI（spawn 一次性事件无重播，过滤会永久不可见） |
355	| AOI 客户端联动 | >1.5s 无 msg13 → 远端代理冻结输入（防幽灵行走）；NPC 傀儡 300 tick 自然清扫=原版"只收自己 section 内实体"语义 | `Game.simulateRemotePlayers` | 不变量：NPC 2s 兜底(120t) ≪ 300t 清扫阈值，勿改坏 |
356	| **msg23 短码** | S→C 每条 1B eflags：bit0=含 key 全量 / bit1=boss；平时仅 u16 codeId（服务器 netId→codeId 表，Room 级）。约 -25% msg23 流量。**PROTO_VER 3→4，server 与 game 必须同时发布** | `Room` npcCodes / `ClientNet.npcCodes` | 未知短码静默丢弃，≤2s 全量兜底自愈；表满 60000 清表重播 |
357	| 合包 | 上行 msg21 攒批 flush；服务器 `flushOutbox` 每 WS message 事件拼发（512KB 切片） | `ClientNet.pendingFrames` / `Room.flushOutbox` | `netDropSweep` 逐条成帧的几十次 send 归一 |
358	| FrameParser 增量化 | 单缓冲+读写偏移+copyWithin（旧版每 drain 全量合并拷贝） | `protocol.ts` | drain 回调内禁 append（重入断言） |
359	| section 缓存 | 条带级 LRU 512，`applyTileOps` 按条带归一化失效 | `Room.stripCache` | 高换人率/重连风暴场景的重复 RLE 归零 |
360	| **世界持久化** | `--world <file>` 常驻房（hostToken='' 首进者为房主）+ `--save-interval`（默认 300s，空房无修改跳过）+ SIGTERM/SIGINT 落盘退出；`saveWorldOnly`（不含玩家，无 SSC） | `server/src/persist.ts`、`SaveFile.saveWorldOnly` | 修复开服.sh `--world` 被忽略的挂账；存档=世界 tile/箱/clock/flags/天气。**部署注意**：SIGTERM 单播主进程实测 0.5s 落盘 ✓（systemd 默认行为）；对进程**组**发 TERM 与落盘并发会静默死亡（机制未定，疑似 npx 转发升级 SIGKILL）——生产用 systemd 直管主进程，避免 npx 包装层 |
361	| 傀儡插值 | 快照间 smoothstep 插值（4 tick 周期），到点后纯速度外推；逻辑位（netAx/netAy，接触判定）仍=最新快照 | `Entity.netSnapTo/netPuppetStep` | 渲染平滑，判定不漂 |
362	
363	**已知偏离**（有意为之，记录在案）：
364	- AOI 下视野外 Boss 无血条（看不见本体时也无血条，语义自洽）；
365	- 远端玩家离开视野后代理原地冻结（非消失），回视野自动恢复；
366	- msg23 C→S 全量 / S→C 短码的非对称线格式（服务器重编码点本来就在）。
367	
368	## 8ter. v5 补齐批（2026-08-12，review 后续）
369	
370	| 项 | 内容 | 语义依据 |
371	|---|---|---|
372	| 敌对弹幕访客伤害 | msg27 kind **bit7=hostile**（仅 kind0/Arrow 携带，host 广播置位/服务器 `(kind&0x7f)>4` 校验透传/访客 `netMakeProj` 重建带 hostile）→ 访客 `netPuppetProjContact` **本地结算**（`hitPlayer`=原版 Damage_EVP 1:1：hostile+dmg>0 门禁/player.immune iframes 门禁/AABB；命中不消耗穿透弹体照飞；`statusPlayer` debuff 以实际伤害为准） | 原版玩家伤害即各端本地结算（HP 客户端权威+msg16 中继，与近战 `netPuppetContact` 同模型）——不走 msg42（那是 NPC 受击链） |
373	| session 认领制 | 建连只标记 `claimed` 不删条目，**Hello 成功才消费**；握手前断线 `disconnect` 释放认领（60s 窗口内重试有效）；顺带修复旧实现"认领即删→61s 超时回调跳过释放"的 **slot 永久泄漏** | §8.8 三次重连承诺成立 |
374	
375	PROTO_VER 4→**5**（msg27 kind 值域扩展；server 与 game 同仓库同时发布）。探针新增 3 断言
376	（hostile 傀儡重建/本地伤害/msg16 中继），53 断言全绿。
377	
378	**对抗审查补丁轮（2026-08-12 第二轮 review，全部已修）**：
379	- **Dart/TrapShot 补 hostile**：敌怪射击弹（`Enemy.shootDart` 咽喉 + 3 处直构）与机关/陷阱弹（TrapShot 构造时 `!style.friendly`）随 bit7 下发——v5 首版只覆盖 Boss Arrow 族，普通射击怪远程弹访客整体免疫；
380	- **服务器剥除非房主 bit7 + dmg 钳 9999**：hostile 位合法来源唯一=房主 NPC AI，否则任意访客伪造 hostile 弹即可无 PvP 开关强制击杀他人；
381	- **msg21 op=0 三重校验**（netId 属主/key 反查/maxStack 钳位）：堵"伪造掉落凭空造物直塞他人背包"（拾取无需同意），protectItems 只拦写箱拦不住这条链；
382	- **盲端免伤漏洞**：停发 msg13 → 判盲 → 傀儡表空 → 免疫一切 NPC/弹幕伤害，且 Ping 心跳使看门狗永不触发——对策 `blindAbuser`（盲 >15s 仍发操作类消息即踢；合法后台挂机页不发操作，语义安全）；
383	- **session 世代判等 + 迟到 Hello 复核**：超时回调按条目对象判等防误删同键新条目；Hello 复核条目仍在防超时后双占 slot；
384	- **NaN 坐标清洗**（msg13/23/27/21）——非法坐标中继会毒化他人代理物理；
385	- **空房且脏即时落盘**（ws close 钩子）——"取物后退出"的复制窗口从 ≤300s 收敛到 ~0；
386	- 弹幕接触判定改权威位（netAx/netAy，与 NPC 接触同标准）；netProjLast 差分基准清理。
387	
388	**挂账清偿批（2026-08-12 第三轮，v6，PROTO_VER 5→6，全部落地）**：
389	
390	| 原挂账 | 处置 |
391	|---|---|
392	| 上行限流（§6.2 兑现） | 每客户端每秒 per-msgId 计数，阈值=合法峰值 3-6 倍（msg13≤90 / TileBatch≤180 / msg23/27/28/21≤60 / msg5≤30 / 聊天≤30 / msg42≤120），超限踢出 |
393	| tile/箱帧 >4MB 静默分叉 | prio=0 帧 >4MB 不再丢——**带原因踢慢客户端**（重连全量拉条带自愈）；prio=1 丢弃语义不变 |
394	| 房主迁移无公告 | 房主离开→"NPC 模拟暂停"公告；新房主产生→"已成为房主"公告（Text 模块 slot=255=服务器直显，客户端无名字前缀） |
395	| AOI"见人不见弹"空洞 | 实体内径 1280→**1536px**（96t，≈玩家内径 80%），带宽 +20% 换对射可见性 |
396	| 幽灵弹 180t 窗口 | **msg28 弹幕消亡上报**（各端弹幕消亡批量 netId→服务器中继→接收端即时移除傀儡）；超时清扫降级为兜底 |
397	| Boss 锚定弹体零同步 | msg27 kind **5-8**：DukeSharknadoBolt/龙卷/MLDeathray/LunarOrb(539/574)。**访客重建真类本地跑确定性 AI**（锚=msg23 傀儡，netId 回溯查找；激光扫描/盘旋/生长/爆炸全本地=原版各端模拟语义）；spawn 类副作用经 !netPuppet 门禁排除（出鲨/落龙卷/线发 576 防双端重复） |
398	| 双保护非反作弊 | **--ssc 服务器角色档**（v6 msg201）：msg5/16/13 累积→断开/即时落盘 server/ssc/\<name\>.json→同名重连下发应用。语义=原版 ServerSideCharacter 存档型（跨设备恢复），信任模型同原版——仍非反作弊 |
399	| 断连掉落丢失 | 重连世界就绪后清本地真掉落 netId+差分基准 → netDropSweep 重播 spawn |
400	
401	**判定位语义定论**（第三轮实测纠正 review F3）：敌对弹幕接触判定用**渲染位**（插值+外推）
402	而非权威位——原版各端本地模拟，"所见即所中"才是客户端权威语义；权威位在差分快照
403	间隔内（慢速弹最长 60t）冻结在过期位置，实测造成慢速敌弹系统性漏判。
404	
405	**近似收紧**（第三轮补）：①MLDeathray 束角**快照回写**——实时角度本就随 exVx/exVy
406	每帧在线上，傀儡消费式同步（读后清零防回拉振荡），快照间隙本地按扫速自推，后台页
407	暂停恢复后由下一快照纠偏（消除永久漂移）；②DukeSharknadoTornado **生长状态携带**
408	——tag=`${big},${ai1},${ai0}`，重建时由快照段盒反解 topY（y = topY − h(ai1)/2 的逆，
409	与房主同公式确定性对齐），中途入视野不再从零重长、列判定盒不错位。剩余近似
410	（Orb 冲刺随机抖动双端异掷、猪鲨大弹狂暴速度差、液体导致的激光束长差）为
411	原版同款模型代价，msg28 消亡兜底误差有界。
412	
413	**剩余挂账**（确认记录即可）：msg17 无重放（原版同款）、SSC 非反作弊边界、
414	上行限流阈值为首版经验值（按 /stats 观测调优）、Boss 锚定弹体的束角/爆炸为本地近似
415	（双端确定性漂移由 msg28 消亡兜底）。
416	
417	**容量验证方法与实测**（`node game/scripts/_loadprobe.mjs --clients=N --seconds=20 --density=calm|boss [--spread]`，
418	本机 macOS / tsx server；平均出带宽 = 累计字节/时长，比 1s 采样可信）：
419	
420	| 场景 | 服务器平均出带宽 | 每客户端 | 备注 |
421	|---|---|---|---|
422	| 32 人 calm 簇拥（全互见，AOI 最不利） | 1.43 MB/s | 45.9 KB/s | msg27 17.4MB / msg13 6.6MB / msg23 5.4MB（20s 累计） |
423	| 32 人 calm spread（一半 5000px 外） | 0.68 MB/s | 21.8 KB/s | **-53%**（AOI 生效，远组互不可见） |
424	| 100 人 boss 簇拥 | 18.5 MB/s | 184.6 KB/s | 物理上限：全员互见+10 发弹幕互播，带宽 O(N²) 不可约 |
425	| 100 人 boss（盲端修复前） | 25.6 MB/s | 262 KB/s | 修复前 stale 兜底形成饱和放大循环 |
426	
427	实测驱动的两个设计修正（2026-08-12）：
428	1. **盲端语义从"全视野兜底"改为"跳过"**：饱和时 msg13 处理滞后 → 判盲 → 若兜底全量灌流 → 更饱和
429	   （实测 stalePos 197 万次、带宽反升）。盲端本就在滞后，停发实体流让它先追平，msg13 恢复后自愈。
430	2. **全员全量快速路径**：簇拥场景（所有接收端都收全部条目）单帧广播零重编码，
431	   去掉逐接收端 NetWriter 重建的 O(N²) 编码 CPU（msg27 无短码差异时直接复用原帧）。
432	
433	## 9. 分阶段实施（细化版）
434	
435	| 阶段 | 交付物 | 探针验收（可执行） |
436	|---|---|---|
437	| P0 协议层 | shared Buffer/MessageID 表、server 骨架（WS+握手+空世界）、ClientNet、Hello→slot→msg7 往返 | `probe-net-handshake`：浏览器连 server 收到 msg7 且字段与加载的世界一致 |
438	| P1 世界流式 | CompressTileBlock(RLE)、CheckSection、TileSections、msg8/9/10/159 | `probe-net-section`：客户端进房后出生点 ±200×150 逐格 hash == 服务器 |
439	| P2 玩家 | msg4/5/13/14/16/42、NetPlayers、远端渲染、netOffset | `probe-net-players`：双浏览器互见，A 走 10s 后 B 侧位移误差 < 300px 平滑收敛 |
440	| P3 实体 | ServerGame 60Hz（Spawner/NPC AI/液体/电路）、msg23/27/28/29、module0/2 | `probe-net-npc`：同一 NPC 双客户端 hp/位置 tick 级一致 |
441	| P4 交互 | msg17/19/20/31-34/59/61/65、聊天 module1、物品归属 | `probe-net-tiles`：A 挖 B 消失 + 掉落归属防抢拾 |
442	| P5 LAN+UI | UDP 广播、MultiplayerSelect 面板（TitleMenu mp 占位接线）、`npm run host` | 手测双机 LAN；探针覆盖 UI 流程 |
443	| P6 加固 | 重连(§6.4 默认开)、stats、定期存档、长稳脚本、优化项逐个评估开启 | 长稳 10min + 断线注入恢复比对存档 hash |
444	
445	## 10. 风险登记（扩充）
446	
447	| 风险 | 等级 | 缓解 |
448	|---|---|---|
449	| TileSection 编码位标志复杂易错 | 高 | 黄金样本单测 + 两客户端 hash 比对探针双重兜底；codecVer 版本位 |
450	| Node 单线程 60Hz 性能 | 中 | tick 直方图监控；NPC 同步限流；液体可迁 worker_threads |
451	| 引擎 import 链在 Node 断链（data/tiles 等传递依赖） | 中 | server tsconfig paths 白名单 + `--selftest` 启动自检 + CI 冒烟 |
452	| 双客户端 tick 不同步导致实体行为分歧 | 中 | 服务器权威实体（NPC/掉落）单一模拟源；客户端仅显示——天然无分歧；玩家判定各自本地（原版同款） |
453	| packWorld transfer 误用 | 高 | 服务器不用 worldPacket（走 section 流）；单机路径保持现状 |
454	| WS 在企业代理/HTTPS 环境兼容 | 低 | wss 反代文档；游戏本身不存凭证 |
455	| 原版语义偏差回归 | 中 | 每条消息实现附原版行号注释；协议单测对照黄金样本 |
456	
457	## 附录 A. 原版常量速查（实现时直接引用）
458	
459	```
460	60Hz tick / 端口 7777 / maxConnections 256 / 玩家 slot 0..254
461	帧 [u16 len][u8 msgId] ≤65535B / 缓冲 131070B
462	section 200×150 / 活跃窗口 60t / CheckSection 3×3(fluff=1) / 出生点首包 5×3
463	msg13 420t / msg36+16+40 900t / msg7 3600t / 超时 7200t
464	netOffset 平滑半径 300px / NPC 跳过容忍 4 次 / 弹幕 netSpam 60
465	msg23 life 档位 0:sbyte 1:short 2:int / msg21 slot=400 请求分配
466	物品槽冷却 timeItemSlotCannotBeReusedFor / msg17 flag13 无掉落
467	状态机：-1 密码 / 0 连接 / 1 过版本 / 2 发WorldData / 3 发section / 10 在游戏
468	```
469	
470	## 附录 B. 源码锚点（1456）
471	
472	NetMessage.cs（SendData 82 起/CompressTileBlock 1889/SendSection 2695/SyncOnePlayer 2883）、
473	MessageBuffer.cs（GetData 123/握手 179-930/msg13 937/msg17 1127/msg27 1712/门禁 156-171）、
474	Netplay.cs（InitializeServer 243/CheckSection 驱动/UDP 广播 796-857）、
475	RemoteClient.cs（TileSections 37/CheckSection 132/SpamUpdate 76）、
476	Main.cs（Update netMode 分支 17671/UpdateServer 64004/UpdateClient 63965）、
477	NetworkInitializer.cs（模块注册顺序 12-26）。
478	

````


---

## 🤖 Assistant · 2026-08-12T08:34:23.910Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"ssc\\|max-players\\|world-budget\\|maxPlayers\\|argv\\|process.argv\\|--\" ~/Project/GLM/SandboxWorld/server/src/index.ts | head -60",
 "description": "Inspect CLI options in server index.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:24.044Z

**📎 ToolResult**

```
17:  const i = process.argv.indexOf(`--${name}`);
18:  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
23:const DEFAULT_MAX_PLAYERS = Math.min(255, Math.max(2, parseInt(arg('max-players', '255')!, 10)));
27:const WORLD_BUDGET = parseInt(arg('world-budget', String(2 * 1024 * 1024 * 1024))!, 10);
31:/** P3.1 持久化：--world <path> 启动载入建常驻房；--save-interval 秒（默认 300） */
35:/** v6 SSC（--ssc 启用）：服务器角色档目录 */
36:const SSC_ENABLED = process.argv.includes('--ssc');
37:const SSC_DIR = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../ssc');
40:function sscSaveClient(c: import('./room.ts').RoomClient) {
74:/** 空房回收（创建满 1 分钟且一直无人满 5 分钟 → 关闭回收；--world 常驻房豁免） */
145:          online: e.room.onlineCount, maxPlayers: e.room.opts.maxPlayers, w: e.room.world.w, h: e.room.world.h,
165:    // POST /rooms → 创建房间（body: {name, public, protectTiles, protectItems, maxPlayers, save}）
172:        name?: string; public?: boolean; protectTiles?: boolean; protectItems?: boolean; maxPlayers?: number; save?: string;
190:      room.opts.maxPlayers = Math.min(255, Math.max(2, body.maxPlayers ?? DEFAULT_MAX_PLAYERS));
198:      console.log(`[room] 创建 ${room.opts.code}（${world.name} ${world.w}×${world.h} 公开=${room.opts.publicRoom} 破坏保护=${room.opts.protectTiles} 物品保护=${room.opts.protectItems} 上限=${room.opts.maxPlayers}人 预算=${(worldBudgetUsed / 1048576) | 0}/${(WORLD_BUDGET / 1048576) | 0}MB）`);
205:    // DELETE /rooms/<code>?token= → 房主关房（--world 常驻房不可关）
244:  if (SSC_ENABLED) room.sscLoad = (name) => loadSscRecord(SSC_DIR, name); // v6：进场下发角色档
260:    sscSaveClient(c); // v6 SSC：断开即落盘（最后状态）
265:    // 否则"取走箱内物品后退出"要等下一个 --save-interval(默认 300s)才持久化,
309:// ================= P3.1 持久化：--world 常驻房 + 定时落盘 + 信号退出 =================
318:    room.opts.maxPlayers = DEFAULT_MAX_PLAYERS;
323:    console.log(`[room] --world 常驻房 ${room.opts.code}（${world.name} ${world.w}×${world.h} 上限=${room.opts.maxPlayers}人）`);
325:    console.error(`[server] --world ${WORLD_FILE} 载入失败:`, (e as Error).message);

```


---

## 🤖 Assistant · 2026-08-12T08:34:58.039Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have most of the picture. Let me verify a few remaining details:

1. server/src/index.ts full view of CLI options (especially --upload-limit, --port, etc.), and the tag format 5-8 in Game.netProjBroadcast. The task asks about msg27 tag 各 kind 的打包格式 5-8 — that's in game code (Game.ts netProjBroadcast). Let me grep.

2. Check msg23 C→S direction server decodes (already seen) vs client sends (ClientNet.sendNpcSnapshot: u16 count, u32 netId, str key, f32 x,y,vx,vy, i16 hp, i16 maxHp, u16 animT, u8 flags). Server reads: u32 netId, str key, f32×4, i16 hp, i16 maxHp, u16 animT, u8 flags. Match.

Protocol comment says C→S: {u16 count, [u32 netId, str key, f32 x,y,vx,vy, i16 hp, i16 maxHp, u16 animT, u8 flags(bit0=boss)]}. Match.

S→C short code: protocol comment: {u16 count, [u8 eflags, ..., eflags.bit0=含 key 全量(u32 netId + u16 codeId + str key) bit1=boss; 否则仅 u16 codeId]}. Server: writes u8 eflags, then if known u16 code else u32 netId + u16 code + str key, then f32×4, i16 hp, i16 maxHp, u16 animT. Client reads accordingly. Match.

But wait — one subtle issue in the allKnown fast path: `f.u8(e.boss ? 2 : 0)` — eflags = 0 or 2, meaning short-code only. That relies on the receiver knowing the code. The check `allKnown` verified all targets know all picked codes. OK.

Hmm, but there's a subtle bug: in fast path, targets where picked.length < entries.length were excluded (allFull false). Fine.

Another subtlety: in fast path known-set refresh only for picked codes; fine.

3. msg27: check server relay. Client sends sendProjectileBatch: u16 count, then per: u32 netId, u8 kind, str tag, i16 dmg, i16 aux, f32×4. Server reads same, validates (kind&0x7f) > 8 → drop; strips bit7 for non-host; relays with same format. Client handle Msg.SyncProjectile reads u16 count, per: u32, u8, str, i16, i16, f32×4. Match.

Now, the protocol comment for msg27 says kind 值域 0-8 + bit7, tag 各 kind 打包格式 5-8. The comment in protocol.ts doesn't detail tag format for 5-8 — it references "见 Game.netProjBroadcast 各分支注释". The task asks me to check that. Let me grep Game.netProjBroadcast.

4. msg28: server: n = u16, cap 64, relay u16 n + n×u32. Client sends u16 min(64) + u32 ids. Client receives: n = min(u16, 64), reads n u32. Match. Protocol comment matches.

One issue: server relays ProjDespawn via `this.broadcast(f.finish(), c, 1)` — broadcast skips clients with state < 10 and except c. Fine.

5. msg200 RoomPolicy: server sends str code, str name, bool isHost, bool protectTiles, bool protectItems, u16 maxPlayers. Client reads str, str, bool, bool, bool, u16 with try/catch fallback 255. Match. Protocol comment matches.

6. msg201 SscSync: server sends str(recordJson); client reads r.str(). Match.

Now check: does the server send SscSync anywhere else (e.g., on reconnect or periodic)? It only sends in SpawnTileData handler if sscLoad exists. OK.

Note: msg201 SscSync is NOT in the probe's Msg table? Wait — _netfake.mjs Msg has SscSync: 201. Yes it does. And ProjDespawn: 28. Yes. Good. But Msg table missing: RoomPolicy=200, SyncItem=21, SyncChestItem=32, RequestChestOpen=31, StrikeNPC=42, PlayerActive=14, SetTime=18, StatusText=9? Let's check the probe's message loop: it only handles PlayerSlot, Kick. So missing entries fine for probes, but the audit item asks whether Msg table synced with protocol.ts enum for v6 additions (28/201) — they are present. But RoomPolicy=200 is missing from _netfake Msg even though the roomprobe asserts maxPlayers... via HTTP /rooms list, not via WS. Fine.

Now Writer differences vs NetWriter:
- Writer.u16 uses `v & 0xffff` — wraps silently; NetWriter uses DataView.setUint16(v, true) which also wraps silently (ToUint16). Actually setUint16 also does modulo 2^16 conversion — same. Hmm, but NetWriter.u32 uses `v >>> 0` (int32 range limitation!) whereas Writer.u32 uses `v >>> 0` too. Both same limitation. Not relevant for probes.
- NetWriter.u8 uses `v & 255`; Writer uses `v & 255`. Same.
- str: NetWriter u16 length + UTF-8 bytes; Writer u16(b.length) + bytes. Same. No BOM difference.
- NetWriter.finish() guards len > 65535 throws; Writer.finish() same guard. Same.
- Writer lacks f64, i8, bool, bytes — not used in probes.
- Writer buffer: `Buffer.alloc(256)`, `need()` growth. Fine.
- One real difference: NetWriter.str() calls this.u16(b.length) which goes through grow(2) — fine. Writer.str: u16 then need. Fine.

Potential trap: Writer has no bounds check on u32 negative? writeUInt32LE(v >>> 0) handles. OK.

Another: In _roomprobe the manual frame parse loop: `const len = data.readUInt16LE(p); if (data[p+2] === Msg.PlayerSlot) return done(...)` — checks PlayerSlot/Kick before validating len. Minor: if len < 3 it breaks after checking. Fine.

Now items 2: PROTO_VER usage points. Found:
- game/src/net/protocol.ts:16 define
- server/src/room.ts import + compare
- ClientNet.ts import + send
- _netfake.mjs:11 constant (hardcoded 6)
- probes import from _netfake
- doc mentions PROTO_VER=4 in §8bis header, and §8ter mentions 4→5, 5→6.

Note: protocol.ts line 5 comment says "当前 v5" while PROTO_VER=6 — stale comment. Also there's game/src/workers/protocol.ts — different file (worker protocol, unrelated). Let me check whether it has a PROTO_VER-like thing... it was in grep -l for PROTO_VER? No, the first find listed it because of find pattern "protocol.ts". The grep -l for PROTO_VER did not include workers/protocol.ts. Good — but let me verify no other hardcoded version numbers like "v4"/"v5" strings that mislead. Grep for 'v4'/'v5' might be noisy. Let me grep for `PROTO_VER=\s*\d` patterns and also check for hard-coded "magic" strings.

Also check index.ts for CLI: --upload-limit? grep showed --world-budget, --max-players, --ssc, --save-interval, --port, --world. The doc §8bis mentions `--upload-limit`（默认 96MB）. Let me check index.ts for upload-limit. The grep didn't show it. Let me check.

Also 开服.sh doesn't mention --ssc or --max-players or --world-budget; it just passes "$@". Task asks: "开服.sh/部署面：与 --ssc/--max-players/--world-budget 等 CLI 的最终形态对账". Since 开服.sh passes "$@" through, users can add flags. But header comment only mentions --world and 300s save. Fine-ish; note that --ssc not documented in 开服.sh.

Also check server index.ts more fully for the room code, empty-room reclamation, upload limit, and SIGTERM handler (单播). Let me read index.ts.

Also need Game.netProjBroadcast for tag format of kind 5-8. Let me grep.

Also check Msg enum in protocol.ts includes RoomPolicy 200 & SscSync 201 — yes.

Also check the "54 assertions" claim: user says _roomprobe.mjs (54 断言). Counting checks in the file: let me count 'check(' occurrences.

Let me also check the doc §7.3 探针 says "14 断言" (stale) — yes line 324 says 14 断言, outdated. §8bis says 36→50+; §8ter says 53 断言全绿. Task claims 54. Need actual count.

Also docs §8.6 (§6.2 mentions 限流承诺). Old §2 message dictionary conflicts with v6: e.g., msg28 described in doc §2 P3 as "DamageNPC（C→S→广播）：u8 npcSlot, i16 damage..." but in our protocol msg28 = ProjDespawn. That's a conflict to list. Also msg2 Kick doc says "u8 原因码, string 说明" but implementation is just str(reason). msg3 PlayerSlot doc says "u8 slot, u8 特性位" but impl has slot + str session. msg9 StatusText doc i32 vs impl u16. msg12 PlayerSpawn 双向 doc has extra fields (respawnTimer, team) vs impl {slot, x, y} S→C only. msg154 ping doc i32 vs impl f64. msg5 doc "SyncEquipment u8 slot, u8 invSlot, i16 itemId, u8 prefix, i16 stack, u8 favorited" vs impl batch format with containers. msg13 doc BitsByte ctrlA/ctrlB vs impl u8 ctrlBits + u8 flagBits. msg23 doc vanilla format vs custom. msg27 doc vanilla vs custom with kind/tag/aux. msg31/32 box four messages vs two. Msg 200/201/28/17 batch not in §2 at all.

Also doc §6.2 阈值数字: "挖块 >500/min 告警、>2000/min 踢" — implementation uses per-second per-msgId counts (TileBatch 180/s = 10800/min). Doc's numbers conflict. §8ter 挂账清偿 lists actual thresholds (msg13≤90 / TileBatch≤180 / ...). So §6.2 old numbers conflict with §8ter new numbers. Note as inconsistency.

AOI 半径: doc §8bis says msg23+27 半径 1280px; §8ter says 实体内径 1280→1536px. Code: AOI_ENTITY = 1536, AOI_PLAYER = 1920. So §8bis row is stale (1280) — it's historical record though. The task explicitly asks about "AOI 半径 1536" — doc has it in §8ter. Also §8bis says ">5s 无位置按全视野兜底（stalePos 计数）" but code now skips blind clients (doc §8bis later has 实测修正 note at end of §8ter: "盲端语义从全视野兜底改为跳过"). The §8bis AOI row itself remains stale but the correction is documented at the bottom of §8ter. Flag it.

Slow-client kick: doc §8ter says "prio=0 帧 >4MB 不再丢——带原因踢慢客户端（重连全量拉条带自愈）". Code: in Room.send, if b > SEND_BUFFER_LIMIT && prio===0 → kick('网络拥堵（发送缓冲持续超限）...'). Match. Severity: note the kick reason text differs from doc? Doc doesn't quote text. OK.

房主公告文案: code: 「${c.name}」已成为房主（NPC 模拟恢复） and 房主「${c.name}」已离开，NPC 模拟暂停；房主重连后恢复. Doc says 房主离开→"NPC 模拟暂停"公告；新房主产生→"已成为房主"公告. Match.

SSC 语义描述: doc says record = {hp, maxHp, x, y, inv, armor, dye, savedAt}; check index.ts sscSaveClient/loadSscRecord to verify fields.

限流阈值数字 in doc §8ter: msg13≤90 / TileBatch≤180 / msg23/27/28/21≤60 / msg5≤30 / 聊天≤30 / msg42≤120. Code RATE_LIMIT: PlayerState 90 ✓, TileBatch 180 ✓, SyncNPC 60 ✓, SyncProjectile 60 ✓, ProjDespawn 60 ✓, SyncItem 60 ✓, SyncPlayerItem 30 ✓, NetModules 30 ✓, StrikeNPC 120 ✓. Match.

Now check index.ts in full for: ssc record fields, --upload-limit, SIGTERM handling, room code length, MAX rooms 32, save interval, kick 看门狗 120s.

Let me read index.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:34:58.150Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/index.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:58.190Z

**📎 ToolResult**

```
1	// SandboxWorld 中央服务器（Node+TS）：lobby（HTTP 房间管理）+ WS 按房间码路由到 Room 会话。
2	// docs/multiplayer-design.md §房间制：房主上传存档建房 → 6 位房间码 → 房间列表/码加入。
3	// 破坏保护服务端权威拒绝（Room.handleTileBatch 前置检查）；物品保护策略下发客户端门禁。
4	import { WebSocketServer, WebSocket } from 'ws';
5	import http from 'node:http';
6	import * as node_os from 'node:os';
7	import { randomUUID } from 'node:crypto';
8	import fs from 'node:fs';
9	import path from 'node:path';
10	import { loadSaveData } from '../../game/src/save/SaveFile.ts';
11	import { NetWriter } from '../../game/src/net/protocol.ts';
12	import { Room } from './room.ts';
13	import { statsSnapshot, startBpsSampler } from './stats.ts';
14	import { saveRooms, loadSscRecord, saveSscRecord, type SscRecord } from './persist.ts';
15	
16	function arg(name: string, def?: string): string | undefined {
17	  const i = process.argv.indexOf(`--${name}`);
18	  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
19	}
20	const PORT = parseInt(arg('port', '7777')!, 10);
21	const MAX_ROOMS = parseInt(arg('max-rooms', '32')!, 10);
22	/** 单房人数逻辑上限默认值（POST /rooms 可按房覆盖；slot 物理上限恒 255） */
23	const DEFAULT_MAX_PLAYERS = Math.min(255, Math.max(2, parseInt(arg('max-players', '255')!, 10)));
24	/** P0.3 内存护栏：全服世界内存预算（估算 15B/格——TileStore 14 通道 + World.explored 1B，
25	 *  review S5 实测修正；原 11B 低估 ~36%。默认 2GB）。
26	 *  注意不能用位运算默认值：2<<30 溢出 int32 成负数（js-bitwise-int32-traps） */
27	const WORLD_BUDGET = parseInt(arg('world-budget', String(2 * 1024 * 1024 * 1024))!, 10);
28	const BYTES_PER_TILE = 15;
29	/** 单存档上传上限（默认 96MB——4200×1200 实测 3.8MB，96MB 已是 25 倍余量） */
30	const WORLD_UPLOAD_LIMIT = parseInt(arg('upload-limit', String(96 * 1024 * 1024))!, 10);
31	/** P3.1 持久化：--world <path> 启动载入建常驻房；--save-interval 秒（默认 300） */
32	const WORLD_FILE = arg('world');
33	const SAVE_INTERVAL = Math.max(30, parseInt(arg('save-interval', '300')!, 10));
34	const WORLDS_DIR = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../worlds');
35	/** v6 SSC（--ssc 启用）：服务器角色档目录 */
36	const SSC_ENABLED = process.argv.includes('--ssc');
37	const SSC_DIR = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../ssc');
38	
39	/** 从在线客户端累积态组装 SSC 档并落盘 */
40	function sscSaveClient(c: import('./room.ts').RoomClient) {
41	  if (!SSC_ENABLED || c.state < 10 || !c.name) return;
42	  const rec: SscRecord = {
43	    hp: c.hp, maxHp: c.maxHp || 100, x: c.lastX, y: c.lastY,
44	    inv: c.items.inv, armor: c.items.armor, dye: c.items.dye,
45	    savedAt: Date.now(),
46	  };
47	  saveSscRecord(SSC_DIR, c.name, rec);
48	}
49	
50	// ================= 房间注册表 =================
51	
52	interface RoomEntry { room: Room; createdAt: number; /** P0.3 预算占用（w*h*11B） */ bytes: number; }
53	
54	const rooms = new Map<string, RoomEntry>(); // code → room
55	/** P0.3 已用世界内存预算 */
56	let worldBudgetUsed = 0;
57	
58	function newCode(): string {
59	  for (;;) {
60	    const code = String(Math.floor(Math.random() * 900000) + 100000); // 6 位数字
61	    if (!rooms.has(code)) return code;
62	  }
63	}
64	
65	/** 统一摘除（回收/关房共用）：释放内存预算 */
66	function removeRoom(code: string) {
67	  const entry = rooms.get(code);
68	  if (!entry) return;
69	  entry.room.closed = true;
70	  worldBudgetUsed -= entry.bytes;
71	  rooms.delete(code);
72	}
73	
74	/** 空房回收（创建满 1 分钟且一直无人满 5 分钟 → 关闭回收；--world 常驻房豁免） */
75	setInterval(() => {
76	  const now = Date.now();
77	  for (const [code, entry] of rooms) {
78	    if (entry.room.persistent) continue;
79	    const idle = now - entry.createdAt;
80	    if (entry.room.closed || (entry.room.onlineCount === 0 && idle > 60_000 && idle > 5 * 60_000)) {
81	      removeRoom(code);
82	      console.log(`[room] 回收空房 ${code}`);
83	    }
84	  }
85	}, 60_000);
86	
87	function worldFromSaveJson(json: string) {
88	  return loadSaveData(JSON.parse(json)).world;
89	}
90	
91	/** 本机全部局域网 IPv4（多网卡全列出——UI 分享用） */
92	function lanIps(): string[] {
93	  const out: string[] = [];
94	  for (const list of Object.values(node_os.networkInterfaces())) {
95	    for (const ni of list ?? []) {
96	      if (ni.family === 'IPv4' && !ni.internal) out.push(ni.address);
97	    }
98	  }
99	  return out;
100	}
101	
102	// ================= HTTP Lobby =================
103	
104	const CORS = {
105	  'Access-Control-Allow-Origin': '*',
106	  'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
107	  'Access-Control-Allow-Headers': 'Content-Type',
108	  'Access-Control-Allow-Private-Network': 'true',
109	};
110	
111	function readBody(req: http.IncomingMessage, limit: number): Promise<Buffer> {
112	  return new Promise((resolveBody, reject) => {
113	    const chunks: Buffer[] = [];
114	    let size = 0;
115	    req.on('data', (d: Buffer) => {
116	      size += d.length;
117	      if (size > limit) { reject(new Error('上传超限')); req.destroy(); return; }
118	      chunks.push(d);
119	    });
120	    req.on('end', () => resolveBody(Buffer.concat(chunks)));
121	    req.on('error', reject);
122	  });
123	}
124	
125	const lobby = http.createServer(async (req, res) => {
126	  const url = new URL(req.url ?? '/', `http://127.0.0.1:${PORT}`);
127	  const finish = (code: number, data: unknown) => {
128	    res.writeHead(code, { 'Content-Type': 'application/json', ...CORS });
129	    res.end(JSON.stringify(data));
130	  };
131	  if (req.method === 'OPTIONS') { finish(204, {}); return; }
132	
133	  try {
134	    // GET /stats → 观测快照（P0.1；全局 + 逐房 + 逐客户端）
135	    if (req.method === 'GET' && url.pathname === '/stats') {
136	      finish(200, statsSnapshot([...rooms.values()].map((e) => e.room)));
137	      return;
138	    }
139	    // GET /rooms → 公开房间列表（非公开不展示，只能码进）
140	    if (req.method === 'GET' && url.pathname === '/rooms') {
141	      const list = [...rooms.values()]
142	        .filter((e) => e.room.opts.publicRoom && !e.room.closed)
143	        .map((e) => ({
144	          code: e.room.opts.code, name: e.room.opts.name,
145	          online: e.room.onlineCount, maxPlayers: e.room.opts.maxPlayers, w: e.room.world.w, h: e.room.world.h,
146	          protectTiles: e.room.opts.protectTiles, protectItems: e.room.opts.protectItems,
147	        }));
148	      finish(200, { ok: true, rooms: list });
149	      return;
150	    }
151	    const m = url.pathname.match(/^\/rooms\/(\d{6})$/);
152	    // GET /rooms/<code> → 房间码校验（加入前置检查，非公开房也允许码查）
153	    if (req.method === 'GET' && m) {
154	      const entry = rooms.get(m[1]);
155	      if (!entry || entry.room.closed) { finish(404, { ok: false, error: '房间不存在' }); return; }
156	      finish(200, {
157	        ok: true, code: entry.room.opts.code, name: entry.room.opts.name,
158	        online: entry.room.onlineCount,
159	        protectTiles: entry.room.opts.protectTiles, protectItems: entry.room.opts.protectItems,
160	        // 首箱锚点（调试/探针确定性用；LAN 游戏服务器无敏感性）
161	        chest: entry.room.world.chests[0] ? { x: entry.room.world.chests[0].x, y: entry.room.world.chests[0].y } : null,
162	      });
163	      return;
164	    }
165	    // POST /rooms → 创建房间（body: {name, public, protectTiles, protectItems, maxPlayers, save}）
166	    if (req.method === 'POST' && url.pathname === '/rooms') {
167	      if (rooms.size >= MAX_ROOMS) { finish(503, { ok: false, error: '服务器房间已满' }); return; }
168	      // P0.3 预检①：上传体积预拒（读 body 前按 limit 截断，防超大 body 打爆内存）
169	      const raw = await readBody(req, WORLD_UPLOAD_LIMIT).catch(() => null);
170	      if (!raw) { finish(400, { ok: false, error: `上传超限（>${Math.round(WORLD_UPLOAD_LIMIT / 1048576)}MB）` }); return; }
171	      const body = JSON.parse(raw.toString('utf8')) as {
172	        name?: string; public?: boolean; protectTiles?: boolean; protectItems?: boolean; maxPlayers?: number; save?: string;
173	      };
174	      if (!body.save) { finish(400, { ok: false, error: '缺少 save（世界存档 JSON）' }); return; }
175	      // P0.3 预检②：全服世界内存预算（15B/格 估算，见 BYTES_PER_TILE 注释）
176	      let worldW = 0, worldH = 0;
177	      try {
178	        const head = JSON.parse(body.save) as { header?: { width?: number; height?: number } };
179	        worldW = head.header?.width ?? 0;
180	        worldH = head.header?.height ?? 0;
181	      } catch { /* 走 worldFromSaveJson 的解析错误 */ }
182	      const estBytes = worldW * worldH * BYTES_PER_TILE;
183	      if (estBytes > 0 && worldBudgetUsed + estBytes > WORLD_BUDGET) {
184	        finish(503, { ok: false, error: `服务器世界内存预算不足（已用 ${(worldBudgetUsed / 1048576) | 0}MB / ${(WORLD_BUDGET / 1048576) | 0}MB）` });
185	        return;
186	      }
187	      const world = worldFromSaveJson(body.save);
188	      const room = new Room(world);
189	      room.opts.code = newCode();
190	      room.opts.maxPlayers = Math.min(255, Math.max(2, body.maxPlayers ?? DEFAULT_MAX_PLAYERS));
191	      if (body.name) world.name = body.name, room.opts.name = body.name;
192	      room.opts.publicRoom = !!body.public;
193	      room.opts.protectTiles = !!body.protectTiles;
194	      room.opts.protectItems = !!body.protectItems;
195	      room.opts.hostToken = randomUUID();
196	      worldBudgetUsed += estBytes || world.w * world.h * BYTES_PER_TILE;
197	      rooms.set(room.opts.code, { room, createdAt: Date.now(), bytes: estBytes || world.w * world.h * BYTES_PER_TILE });
198	      console.log(`[room] 创建 ${room.opts.code}（${world.name} ${world.w}×${world.h} 公开=${room.opts.publicRoom} 破坏保护=${room.opts.protectTiles} 物品保护=${room.opts.protectItems} 上限=${room.opts.maxPlayers}人 预算=${(worldBudgetUsed / 1048576) | 0}/${(WORLD_BUDGET / 1048576) | 0}MB）`);
199	      finish(200, {
200	        ok: true, code: room.opts.code, hostToken: room.opts.hostToken,
201	        name: room.opts.name, protectTiles: room.opts.protectTiles, protectItems: room.opts.protectItems,
202	      });
203	      return;
204	    }
205	    // DELETE /rooms/<code>?token= → 房主关房（--world 常驻房不可关）
206	    if (req.method === 'DELETE' && m) {
207	      const entry = rooms.get(m[1]);
208	      if (!entry) { finish(404, { ok: false, error: '房间不存在' }); return; }
209	      if (entry.room.persistent) { finish(403, { ok: false, error: '常驻房不可关闭' }); return; }
210	      if (url.searchParams.get('token') !== entry.room.opts.hostToken) {
211	        finish(403, { ok: false, error: '仅房主可关房' }); return;
212	      }
213	      removeRoom(m[1]);
214	      finish(200, { ok: true });
215	      return;
216	    }
217	    // GET /lan → 本机信息（IP 分享 + 发现端点）
218	    if (req.method === 'GET' && url.pathname === '/lan') {
219	      finish(200, { ok: true, magic: 1010, port: PORT, rooms: rooms.size, lanIps: lanIps() });
220	      return;
221	    }
222	    finish(404, { ok: false, error: 'not found' });
223	  } catch (e) {
224	    finish(400, { ok: false, error: (e as Error).message });
225	  }
226	});
227	lobby.listen(PORT + 1);
228	
229	// ================= WebSocket（URL = /<房间码>?token=<房主令牌可选>） =================
230	
231	const wss = new WebSocketServer({ port: PORT, maxPayload: 1 << 20 });
232	
233	wss.on('connection', (ws: WebSocket, req) => {
234	  ws.binaryType = 'nodebuffer';
235	  const m = (req.url ?? '').match(/^\/(\d{6})/);
236	  if (!m) { ws.close(1002, '需要房间码路径 /<6位码>'); return; }
237	  const entry = rooms.get(m[1]);
238	  if (!entry || entry.room.closed) { ws.close(1002, '房间不存在'); return; }
239	  const room = entry.room;
240	  const token = new URL(req.url ?? '/', 'http://x').searchParams.get('token') ?? '';
241	  const session = new URL(req.url ?? '/', 'http://x').searchParams.get('session') ?? '';
242	  const c = room.newClient(ws, token);
243	  if (session) room.resumeSession(c, session); // 断线重连：命中则 Hello 时同 slot 复位
244	  if (SSC_ENABLED) room.sscLoad = (name) => loadSscRecord(SSC_DIR, name); // v6：进场下发角色档
245	  console.log(`[ws] 连入房间 ${room.opts.code}`);
246	
247	  ws.on('message', (data: Buffer) => {
248	    c.stats.inBytes += data.length;
249	    c.parser.append(new Uint8Array(data));
250	    try {
251	      c.parser.drain((msgId, r) => room.handle(c, msgId, r));
252	    } catch (e) {
253	      console.error(`[ws] 房间 ${room.opts.code} slot ${c.slot} 异常断开:`, (e as Error).message);
254	      try { ws.close(1002); } catch { /* 已关闭 */ }
255	    }
256	    // P1.3 合包：本条 WS 消息处理完毕，统一冲洗各客户端发送队列
257	    room.flushOutbox();
258	  });
259	  ws.on('close', () => {
260	    sscSaveClient(c); // v6 SSC：断开即落盘（最后状态）
261	    room.disconnect(c);
262	    room.flushOutbox();
263	    console.log(`[ws] slot ${c.slot} 离开房间 ${room.opts.code}（在线 ${room.onlineCount}）`);
264	    // review S5①：最后一人在局玩家离场且房间脏 → 立即落盘。
265	    // 否则"取走箱内物品后退出"要等下一个 --save-interval(默认 300s)才持久化,
266	    // 期间进程被 SIGKILL = 服务器档残留物品 = 复制漏洞窗口
267	    if (!room.closed && room.onlineCount === 0
268	      && (room.roomStats.tileOps !== room.lastSavedTileOps || room.roomStats.chestEdits !== room.lastSavedChestEdits)) {
269	      try {
270	        const r = saveRooms([room], WORLDS_DIR);
271	        if (r.saved) console.log(`[persist] 空房即时落盘 ${room.opts.code}`);
272	      } catch (e) {
273	        console.error(`[persist] 空房即时落盘失败 ${room.opts.code}:`, (e as Error).message);
274	      }
275	    }
276	  });
277	  ws.on('error', () => { /* close 跟上 */ });
278	});
279	
280	// 超时看门狗：逐房逐客户端（未握手 10s / 已握手 120s，对齐原版 TimeOutTimer）
281	setInterval(() => {
282	  for (const entry of rooms.values()) {
283	    for (const c of [...entry.room.clients]) {
284	      c.lastSeen += 1;
285	      if (c.lastSeen > (c.state >= 1 ? 120 : 10)) {
286	        console.log(`[ws] 房间 ${entry.room.opts.code} slot ${c.slot} 超时踢出`);
287	        c.ws.close();
288	      }
289	    }
290	  }
291	}, 1000);
292	
293	// 时间同步：服务器权威时钟推进（对齐原版 WorldGen.UpdateWorld 时钟）+ 10s 广播
294	setInterval(() => {
295	  for (const entry of rooms.values()) entry.room.world.clock.tick(1000);
296	}, 1000);
297	setInterval(() => {
298	  for (const entry of rooms.values()) {
299	    const room = entry.room;
300	    const f = new NetWriter(18).f64(room.world.clock.timeOfDay).u32(room.world.clock.dayCount).finish();
301	    for (const c of room.clients) if (c.state >= 10) room.send(c, f);
302	    room.flushOutbox();
303	  }
304	}, 10000);
305	
306	// ================= P0.1 观测：1s outBps 采样 =================
307	startBpsSampler(() => [...rooms.values()].map((e) => e.room));
308	
309	// ================= P3.1 持久化：--world 常驻房 + 定时落盘 + 信号退出 =================
310	if (WORLD_FILE) {
311	  try {
312	    const json = fs.readFileSync(WORLD_FILE, 'utf8');
313	    const world = worldFromSaveJson(json);
314	    const room = new Room(world);
315	    room.opts.code = newCode();
316	    room.opts.publicRoom = true;
317	    room.opts.hostToken = '';        // 无主房：首位进房者为房主（NPC 权威源）
318	    room.opts.maxPlayers = DEFAULT_MAX_PLAYERS;
319	    room.persistent = true;
320	    const bytes = world.w * world.h * BYTES_PER_TILE;
321	    worldBudgetUsed += bytes;
322	    rooms.set(room.opts.code, { room, createdAt: Date.now(), bytes });
323	    console.log(`[room] --world 常驻房 ${room.opts.code}（${world.name} ${world.w}×${world.h} 上限=${room.opts.maxPlayers}人）`);
324	  } catch (e) {
325	    console.error(`[server] --world ${WORLD_FILE} 载入失败:`, (e as Error).message);
326	    process.exit(1);
327	  }
328	}
329	
330	const roomList = () => [...rooms.values()].map((e) => e.room);
331	setInterval(() => {
332	  const r = saveRooms(roomList(), WORLDS_DIR);
333	  if (r.saved) console.log(`[persist] auto-save：${r.saved} 房落盘，${r.skipped} 房跳过`);
334	}, SAVE_INTERVAL * 1000).unref?.();
335	
336	let shuttingDown = false;
337	function shutdown(sig: string) {
338	  if (shuttingDown) return;
339	  shuttingDown = true;
340	  console.log(`[server] 收到 ${sig}，落盘全部房间…`);
341	  try {
342	    const r = saveRooms(roomList(), WORLDS_DIR);
343	    console.log(`[persist] 退出存档：${r.saved} 房保存，${r.skipped} 房跳过`);
344	  } catch (e) {
345	    console.error('[persist] 退出存档失败:', (e as Error).message);
346	  }
347	  process.exit(0);
348	}
349	process.on('SIGTERM', () => shutdown('SIGTERM'));
350	process.on('SIGINT', () => shutdown('SIGINT'));
351	
352	process.on('uncaughtException', (e) => {
353	  console.error('[server] uncaughtException（记录不退出）:', (e as Error).stack ?? e);
354	});
355	
356	console.log(`[server] 中央服务器 ws://0.0.0.0:${PORT}（lobby http://0.0.0.0:${PORT + 1}/rooms）`);
357	

```


---

## 🤖 Assistant · 2026-08-12T08:34:58.651Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"netProjBroadcast\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head; echo ---; grep -rn \"check(\" ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs | wc -l",
 "description": "Find netProjBroadcast and count probe assertions"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:34:58.736Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts:56:                       //    Boss 锚定弹体，tag 打包锚参数——见 Game.netProjBroadcast 各分支注释）；
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:605:  private netProjBroadcast() {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9889:        this.netProjBroadcast();
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:501:/** v6 联机弹体打包元数据（Boss 锚定弹体族共用形状，Game.netProjBroadcast 消费） */
---
      57

```


---

## 🤖 Assistant · 2026-08-12T08:35:01.097Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
57 check( occurrences — one is the function definition `const check = (...)`. So 56 assertion call sites; some conditional (e.g., inside if(bNpc), chest if). Actual pass-count assertions: let me count precisely. `grep -c "check('" gives calls.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:35:01.324Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -c \"check('\" ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs; echo ---; sed -n '595,700p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Count probe assertions and read netProjBroadcast"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:01.386Z

**📎 ToolResult**

```
57
---
    // 清理已消亡敌人的差分基准（游标轮转下无条件跑——成本与主循环同阶）
    {
      const alive = new Set<number>();
      for (const ent of this.entities.enemies) alive.add((ent as Enemy).id);
      for (const id of this.netNpcLast.keys()) if (!alive.has(id)) this.netNpcLast.delete(id);
    }
    net.sendNpcSnapshot(snaps);
  }

  /** 双向：本地弹幕快照（15Hz 变化驱动；kind: 0=Arrow 1=WeaponProj族 2=Dart 3=TrapShot 4=MagicProj） */
  private netProjBroadcast() {
    const net = this.net!;
    const snaps: ProjSnap[] = [];
    const list = this.entities.projectiles;
    const n = list.length;
    let examined = 0;
    for (; examined < n && snaps.length < 24; examined++) {
      const p = list[(this.netProjCursor + examined) % n] as Entity & { projId?: number; damage?: number; kind?: string; color?: string; life?: number };
      if (p.netPuppet || p.dead) continue;
      let last = this.netProjLast.get(p.id);
      if (!last) {
        last = { x: p.x, y: p.y, t: this.tickCount };
        this.netProjLast.set(p.id, last);
      }
      if (Math.abs(p.x - last.x) < 1 && Math.abs(p.y - last.y) < 1 && this.tickCount - last.t < 60) continue;
      last.x = p.x; last.y = p.y; last.t = this.tickCount;
      let kind = -1, tag = '', dmg = Math.max(-32768, Math.min(32767, Math.round(p.damage ?? 0))), aux = 0;
      let exVx: number | undefined, exVy: number | undefined; // v6：meta 通道的角度方向覆写
      if (p instanceof Arrow) {
        kind = 0; tag = String(p.projId ?? 1);
        // v5：敌对弹带 bit7（原版 Projectile.hostile）——访客端据此本地结算 Damage_EVP
        if (p.hostile) kind |= 0x80;
      }
      else if (p instanceof Dart) {
        kind = 2; tag = String(p.projId ?? 0);
        if (p.hostile) kind |= 0x80; // 射击怪弹（!style.friendly）——review F1：此前整族漏覆盖
      }
      else if (p.projId !== undefined) { kind = 1; tag = String(p.projId); }
      else if (p instanceof TrapShot) {
        kind = 3; tag = p.kind ?? 'dart';
        if (p.hostile) kind |= 0x80; // 机关/陷阱弹（环境危害，原版伤所有玩家）
      }
      else if (p.color !== undefined) { kind = 4; tag = p.color; aux = Math.max(0, Math.min(32767, p.life ?? 600)); }
      else if (typeof (p as { netProjMeta?: unknown }).netProjMeta === 'function') {
        // v6：Boss 锚定弹体族（DukeSharknadoBolt/龙卷/MLDeathray/LunarOrb）——
        // 访客重建真类、本地跑确定性 AI（锚=msg23 傀儡，见 netMakeProj case 5-8）
        const m = (p as unknown as { netProjMeta: () => import('../entities/bossAI_duke_moonlord').NetProjMeta }).netProjMeta();
        kind = m.kind; tag = m.tag.slice(0, 32); aux = m.aux; dmg = m.dmg;
        if (m.exVx !== undefined) { exVx = m.exVx; exVy = m.exVy ?? 0; }
      }
      if (kind < 0) continue; // 未知弹幕类不同步（渲染缺类）
      snaps.push({ netId: makeNetId(net.mySlot, p.id), kind, tag, dmg, aux, x: p.x, y: p.y, vx: exVx ?? p.vx, vy: exVy ?? p.vy });
    }
    this.netProjCursor = (this.netProjCursor + examined) % Math.max(1, n);
    // review F9：清理已消亡弹幕的差分基准（对照 NPC 侧——否则 Map 随会话无界增长）。
    // ⑤ msg28：消亡即上报——接收端即时移除傀儡（消幽灵弹 180t 窗口 + 消亡闪烁）
    {
      const alive = new Set<number>();
      for (const ent of this.entities.projectiles) alive.add(ent.id);
      const despawns: number[] = [];
      for (const id of this.netProjLast.keys()) {
        if (!alive.has(id)) {
          this.netProjLast.delete(id);
          despawns.push(makeNetId(net.mySlot, id));
        }
      }
      if (despawns.length) net.sendProjDespawn(despawns);
    }
    net.sendProjectileBatch(snaps);
  }

  /** 双向：本地真掉落诞生上报 + 消失（拾取/寿命）广播——扫描差分 */
  private netDropSweep() {
    const net = this.net!;
    const cur = new Map<number, ItemDrop>();
    for (const ent of this.entities.drops) {
      const d = ent as ItemDrop;
      if (d.netPuppet) continue;
      if (!d.netId) {
        d.netId = makeNetId(net.mySlot, d.id);
        net.sendItemOp(0, d.netId, ITEM_DEFS[d.itemId]?.key ?? '', d.stack, d.x, d.y, d.vx, d.vy);
      }
      cur.set(d.netId, d);
    }
    for (const netId of this.netDropSeen.keys()) {
      if (!cur.has(netId)) net.sendItemOp(1, netId); // 上轮在、本轮没 = 拾取/过期 → take
    }
    this.netDropSeen = cur;
  }

  /** msg23 回包：NPC 傀儡 upsert（首次创建入桶；boss 置 this.boss 供血条） */
  private netApplyNpcSnaps(snaps: NpcSnap[]) {
    for (const s of snaps) {
      let pup = this.netNpcPuppets.get(s.netId);
      if (!pup || pup.e.dead) {
        // v_* 键走 fromVanilla（防御/伤害等权威属性——占位 def 会让 hurt 双端分叉）；
        // 原生键退普通构造
        const vm = s.key.match(/^v_(\d+)$/);
        const e = vm ? Enemy.fromVanilla(parseInt(vm[1], 10), s.x, s.y) : new Enemy(s.key, s.x, s.y);
        if (!e) continue; // review C2：未知 vanillaId（数据表缺口）只丢这一条，勿中止整批（否则同帧其余傀儡饿死被误清）
        e.x = s.x; e.y = s.y; // 快照坐标=左上（Enemy 构造按中心偏移，直接覆写）
        e.netPuppet = true;
        e.netId = s.netId;
        e.hp = s.hp; e.maxHp = s.maxHp;
        this.entities.add(e, 'enemies');
        if (e.def.boss) this.boss = e;

```


---

## 🤖 Assistant · 2026-08-12T08:35:02.983Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now check the tag formats for kinds 5-8 in bossAI_duke_moonlord.ts NetProjMeta implementations, and netMakeProj case 5-8 (depacking). Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:35:03.344Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '490,620p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Read NetProjMeta definitions for kind 5-8"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:03.390Z

**📎 ToolResult**

```
function addProj(game: GameHooks, p: Entity): void {
  (game as unknown as { entities: { add: (e: Entity, b: string) => void } }).entities.add(p, 'projectiles');
}

// ---------------------------------------------------------------------------
// 龙卷水弹 385(Projectile.cs:28402-28482 AI / :70714-70778 Kill 落龙卷)
// ---------------------------------------------------------------------------
// aiStyle 65:ai1==0(状态 3 小弹)→ vy 余弦摆动斜落,撞块/入水/超时 Kill;
//  ai1>0(状态 8 克苏弹)→ 追踪玩家,速 4(+12 狂暴)+age/20,贴身 50px Kill。
//  Kill:小弹原地落 384 鲨鱼龙卷(伤 40);大弹自弹体 tile 向下扫描 100 格落 386
//  克苏龙卷(伤 80)——龙卷接触伤另按原版 hostile ×2 规则结算(Projectile.cs:13781)。
/** v6 联机弹体打包元数据（Boss 锚定弹体族共用形状，Game.netProjBroadcast 消费） */
export interface NetProjMeta {
  kind: number;        // msg27 kind（5-8）
  tag: string;         // 锚参数打包（各类自定义，≤32 字符）
  aux: number;         // i16 辅助通道
  dmg: number;         // 快照 dmg 字段
  /** 可选：以 vx/vy 通道携带的角度方向（重建端 atan2 还原） */
  exVx?: number;
  exVy?: number;
}

export class DukeSharknadoBolt extends Entity {
  w = 30; h = 30; // SetDefaults 385
  private vx0: number;
  private vy0: number;
  private big: boolean;
  private enraged: boolean;
  /** 小弹 vy 摆动相位(原版 ai[0]) */
  private phase = 0;
  private age = 0;
  life = 300; // SetDefaults timeLeft
  /** 鲨鱼生成所需的 Duke 引用(spawnPart 位置供体,实际落点由龙卷覆写) */
  private src: Enemy;
  dead = false;

  constructor(x: number, y: number, vx: number, vy: number, big: boolean, enraged: boolean, src: Enemy) {
    super();
    this.x = x - this.w / 2;
    this.y = y - this.h / 2;
    this.vx0 = vx; this.vy0 = vy;
    this.big = big; this.enraged = enraged;
    this.src = src;
  }

  fixedUpdate(_dt: number, game: GameHooks): void {
    if (--this.life <= 0) { this.kill(game); return; }
    this.age++;
    const p = game.player;
    if (this.big) {
      // :28405-28447 追踪:速 4(+12 狂暴)+localAI[0]/20,距玩家 <50px 即 Kill
      if (p && !p.dead) {
        const dx = p.cx - this.cx, dy = p.cy - this.cy;
        const d = Math.hypot(dx, dy) || 1;
        const spd = 4 + (this.enraged ? 12 : 0) + this.age / 20;
        this.vx0 = (dx / d) * spd;
        this.vy0 = (dy / d) * spd;
        if (d < 50) { this.kill(game); return; }
      }
    } else {
      // :28448-28475 vy 余弦摆动:vy += (cos(π/15·θₙ₊₁) − cos(π/15·θₙ))·4
      const f = (t: number) => (Math.cos((Math.PI / 15) * t) - 0.5) * 4;
      const d0 = f(this.phase);
      this.phase += 1;
      this.vy0 += f(this.phase) - d0;
    }
    this.x += this.vx0;
    this.y += this.vy0;
    // :28477-28481 入水上浮 16px 后 Kill
    const st = game.world.store;
    const tx = Math.floor(this.cx / TILE), ty = Math.floor(this.cy / TILE);
    if (st.inBounds(tx, ty) && st.liquid[st.idx(tx, ty)] > 0) { this.y -= 16; this.kill(game); return; }
    if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { this.kill(game); return; }
  }

  /** Kill(:70714-70778):尘环 + 落龙卷(小 384 / 大 386 向下扫描地面)。
   *  v6 联机傀儡:运动/消亡本地自算(确定性),但不落龙卷——房主的龙卷经 kind6 同步,
   *  双端各自生成会重复 */
  private kill(game: GameHooks): void {
    this.dead = true;
    game.spawnParticles(this.cx, this.cy, '#7FB8E8', 10, 2.4, { life: 24, damp: 0.94 });
    if (this.netPuppet) return;
    if (this.big) {
      // :70752-70770 自弹体 tile 向下扫 100 格,落点 = 首个实心/液体格上沿 -24px
      const st = game.world.store;
      let tx = clamp(Math.floor(this.cx / TILE), 10, st.w - 10);
      let ty = clamp(Math.floor(this.cy / TILE), 10, st.h - 110);
      let ground = ty + 15;
      for (let y = ty; y < ty + 100; y++) {
        if (st.inBounds(tx, y) && (st.isSolid(tx, y) || st.liquid[st.idx(tx, y)] !== 0)) { ground = y; break; }
      }
      addProj(game, new DukeSharknadoTornado(tx * TILE + 8, ground * TILE - 24, true, this.src));
    } else {
      // :70733-70737 原地落 384(中心反向偏移 direction*30, y-4)
      const dir = Math.sign(this.vx0) || 1;
      addProj(game, new DukeSharknadoTornado(this.cx - dir * 30, this.cy - 4, false, this.src));
    }
  }

  /** v6 联机打包：kind=5，tag=big 标记（访客重建后本地跑确定性运动，见 kill 傀儡门禁） */
  netProjMeta() {
    return { kind: 5, tag: this.big ? '1' : '0', aux: 0, dmg: 0 };
  }

  draw(r: Renderer, _cam: Camera): void {
    const ctx = r.canvas.getContext('2d');
    if (!ctx) return;
    ctx.fillStyle = '#8FD8FF';
    ctx.beginPath();
    ctx.arc(this.cx, this.cy, 6, 0, TAU);
    ctx.fill();
  }
}

// ---------------------------------------------------------------------------
// 鲨鱼龙卷 384 / 克苏龙卷 386(Projectile.cs:28287-28398,aiStyle 64)
// ---------------------------------------------------------------------------
// 原版是"父段 ai0 倒计时到 1 → 在正上方生成子段(ai0=10, ai1-1)直至 ai1=0"的投射物塔;
// 本实现以单实体模拟该塔:列顶随段生长上移,鲨鱼在"新段出现且 ai1 % 出鲨模 == 0"时
// 于列顶 NewNPC(小 384:模 4 → 3 只/塔;大 386:模 2 → 12 只/塔,ai2=幅宽 ai3=-1.5)。
// 接触伤害:小 40 / 大 80(经典 NewProjectile 值),命中按原版 hostile 弹 ×2 规则(:13781)。
export class DukeSharknadoTornado extends Entity {
  private big: boolean;
  private ai0: number;   // 段生长倒计时(父段 16,子段 10)
  private ai1: number;   // 剩余段数(小 15 / 大 24)
  private ai1Start: number;
  /** 列顶中心 y(鲨鱼生成点/绘制塔顶) */
  private topY: number;
  private segs = 0;      // 已生长段数
  private age = 0;
  private alpha = 255;   // 原版 alpha(实体内嵌 SolidCollision 逐渐显形)

```


---

## 🤖 Assistant · 2026-08-12T08:35:03.767Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"netMakeProj\\|case 5\\|case 6\\|case 7\\|case 8\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -20",
 "description": "Locate netMakeProj cases"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:03.823Z

**📎 ToolResult**

```
640:        // 访客重建真类、本地跑确定性 AI（锚=msg23 傀儡，见 netMakeProj case 5-8）
750:        const p = this.netMakeProj(s);
773:  private netMakeProj(s: ProjSnap): Entity | null {
784:      case 5: return new DukeSharknadoBolt(s.x, s.y, s.vx, s.vy, s.tag[0] === '1', false, null as unknown as Enemy);
785:      case 6: {
792:      case 7: {
799:      case 8: {
4570:    //   tile 71 发光蘑菇株 → case 71/72（WorldGen.cs:65697-65707）：
4806:    // tile 5/596/616/634（WorldGen.cs:65267），72 走 case 71/72 掷骰（:65697-65707）：
6777:      case 5: // 绳 965×20-40（仅非地狱肉前，L57683）
7813:        case 54: // 裁缝套装（:1795-1923）
7832:        case 633: { // 动物学家（:3358-3380 配对耳尾 + :3249-3252 满月夜狼人画）
8385:        // switch case 552/553/554——仅 Goblin T1/T2/T3；555+ 与 551 不登记）
8765:    // 宝石树苗 590（AttemptToGrowTreeFromSapling case 590，:72924-72960）：必须地下

```


---

## 🤖 Assistant · 2026-08-12T08:35:05.403Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '773,830p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts; echo ===; grep -n \"netProjMeta()\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Read netMakeProj cases 5-8 and list netProjMeta impls"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:05.456Z

**📎 ToolResult**

```
  private netMakeProj(s: ProjSnap): Entity | null {
    // v5：bit7 = hostile（原版 Projectile.hostile，仅 kind0/Arrow 语义有效）——
    // 访客端据此对敌对弹幕傀儡本地结算 Damage_EVP（见 netPuppetProjContact）
    const hostile = (s.kind & 0x80) !== 0;
    switch (s.kind & 0x7f) {
      case 0: return new Arrow(s.x, s.y, s.vx, s.vy, s.dmg, 0, parseInt(s.tag, 10) || 1, null, { hostile });
      case 1: return new Boomerang(s.x, s.y, s.vx, s.vy, s.dmg, 0, parseInt(s.tag, 10) || 1); // WeaponProj 族共用 drawProj(projId) 渲染，取代表类重建
      case 2: { const d = new Dart(s.x, s.y, s.vx, s.vy, s.dmg, parseInt(s.tag, 10) || 0); d.hostile = hostile; return d; }
      case 3: { const t = new TrapShot(s.x, s.y, s.vx, s.vy, s.dmg, (s.tag || 'dart') as TrapShotKind); t.hostile = hostile; return t; }
      case 4: return new MagicProj(s.x, s.y, s.vx, s.vy, s.dmg, Math.max(60, s.aux), s.tag || '#8090FF');
      // ---- v6：Boss 锚定弹体——重建真类，本地跑确定性 AI（锚=msg23 傀儡）----
      case 5: return new DukeSharknadoBolt(s.x, s.y, s.vx, s.vy, s.tag[0] === '1', false, null as unknown as Enemy);
      case 6: {
        // 近似收紧②：tag=`${big},${ai1},${ai0}`——中途入视野的龙卷按快照恢复生长态
        const [bigBit, ai1s, ai0s] = s.tag.split(',').map(Number);
        const t = new DukeSharknadoTornado(s.x, s.y, bigBit === 1, null as unknown as Enemy);
        t.netStateSync(ai1s, ai0s, s.x, s.y);
        return t;
      }
      case 7: {
        const [srcId, kindBit] = s.tag.split(',').map(Number);
        const m = new MLDeathray(this.netFindAnchor(s, srcId), kindBit === 0 ? 'head' : 'core',
          Math.atan2(s.vy, s.vx), (s.aux || 0) / 10000, s.dmg, s.x, s.y);
        m.srcNetId = ((s.netId >>> 24) << 24) | ((srcId || 0) & 0xffffff); // 锚未到也不死等（傀儡随后到即接上）
        return m;
      }
      case 8: {
        const [kind, parentId] = s.tag.split(',').map(Number);
        const o = new LunarOrb(this.netFindAnchor(s, parentId), kind === 574 ? 574 : 539, s.vx, s.vy, s.dmg, s.x, s.y);
        o.parentNetId = ((s.netId >>> 24) << 24) | ((parentId || 0) & 0xffffff);
        return o;
      }
      default: return null;
    }
  }

  /** msg42 回包（房主）：访客打击权威结算——按 netId 找真身应用 hurt（防御减算在此一次） */
  private netApplyStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
    const localId = netIdLocal(netId);
    for (const ent of this.entities.enemies) {
      const e = ent as Enemy;
      if (e.netPuppet || e.id !== localId) continue;
      e.hurt(rawDmg, kbx, kby, this);
      const dealt = Math.max(1, Math.round(rawDmg - (e.def.defense ?? 0) * 0.5));
      this.addDamageNumber(e.cx, e.y, dealt, false, '#FF7060');
      return;
    }
  }

  /** msg28 回包：弹幕消亡即时移除傀儡（v6——替代纯超时清扫的补刀路径） */
  private netRemoveProjPuppets(ids: number[]) {
    for (const id of ids) {
      const pup = this.netProjPuppets.get(id);
      if (pup) {
        pup.p.dead = true;
        this.netProjPuppets.delete(id);
      }
    }
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T08:35:07.065Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `===` echo broke zsh? "== not found" — zsh treats `===` specially. Anyway got the output.

Now grep netProjMeta in bossAI file with proper quoting.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:35:07.297Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"netProjMeta\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "List netProjMeta implementations"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:07.354Z

**📎 ToolResult**

```
590:  netProjMeta() {
708:  netProjMeta() {
1011:  netProjMeta(): NetProjMeta {

```


---

## 🤖 Assistant · 2026-08-12T08:35:09.067Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '585,600p;700,725p;1005,1025p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Read the three netProjMeta tag pack formats"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:09.145Z

**📎 ToolResult**

```
      addProj(game, new DukeSharknadoTornado(this.cx - dir * 30, this.cy - 4, false, this.src));
    }
  }

  /** v6 联机打包：kind=5，tag=big 标记（访客重建后本地跑确定性运动，见 kill 傀儡门禁） */
  netProjMeta() {
    return { kind: 5, tag: this.big ? '1' : '0', aux: 0, dmg: 0 };
  }

  draw(r: Renderer, _cam: Camera): void {
    const ctx = r.canvas.getContext('2d');
    if (!ctx) return;
    ctx.fillStyle = '#8FD8FF';
    ctx.beginPath();
    ctx.arc(this.cx, this.cy, 6, 0, TAU);
    ctx.fill();
        game.damagePlayer(this.big ? 160 : 80, this.cx, this.cy, this.src);
      }
    }
  }

  /** v6 联机打包：kind=6，tag=`${big},${剩余段数ai1},${段倒计时ai0}`。
   *  近似收紧②：携带生长状态——中途入视野的龙卷按快照段盒+段数确定性恢复
   *  （topY = 快照y + 当前段半高,与房主同公式）,不再从零重长 */
  netProjMeta() {
    return { kind: 6, tag: `${this.big ? 1 : 0},${this.ai1},${this.ai0}`, aux: 0, dmg: 0 };
  }

  /** v6 近似收紧②：访客重建时由快照段盒 + ai1/ai0 恢复生长态。
   *  topY 与 ai1 是确定性函数关系（resize: y = topY − h(ai1)/2），故由
   *  snapY 反解即可精确对齐房主当前态（含列顶位置,判定盒不再错位） */
  netStateSync(ai1: number, ai0: number, snapX: number, snapY: number): void {
    if (!Number.isFinite(ai1) || ai1 < 0 || ai1 > this.ai1Start) return; // 非法态保持新建
    this.ai1 = ai1;
    this.ai0 = Number.isFinite(ai0) ? ai0 : 10;
    this.segs = this.ai1Start - ai1;
    this.resize();
    this.x = snapX;                    // cx = snapX + w/2,resize 后 x = cx − w/2 = snapX
    this.topY = snapY + this.h / 2;    // 反解列顶（y = topY − h/2 的逆）
    this.y = snapY;
  }

    this.x = (x ?? src!.cx) - this.w / 2;
    this.y = (y ?? src!.cy) - this.h / 2;
  }

  /** v6 联机打包：kind=7，tag=`${srcId},${head|core}`，aux=扫速×10000，
   *  束角经 vx/vy 通道携带（重建端 atan2 还原后本地扫射——确定性自包含） */
  netProjMeta(): NetProjMeta {
    return {
      kind: 7,
      tag: `${this.srcId},${this.kind === 'head' ? 0 : 1}`,
      aux: Math.max(-32768, Math.min(32767, Math.round(this.sweep * 10000))),
      dmg: this.dmg,
      exVx: Math.cos(this.angle) * 1000,
      exVy: Math.sin(this.angle) * 1000,
    };
  }

  /** scale 上限:头 1.0 / 真眼 0.4(:30468-30478 num728) */
  private get maxScale(): number { return this.kind === 'head' ? 1 : 0.4; }

  fixedUpdate(_dt: number, game: GameHooks): void {

```


---

## 🤖 Assistant · 2026-08-12T08:35:12.693Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: LunarOrb netProjMeta at line 1011 is for kind 8? Wait — line 590 is DukeSharknadoBolt (kind 5), 708 is DukeSharknadoTornado (kind 6), 1011 is MLDeathray (kind 7). Where's LunarOrb kind 8? Let me grep LunarOrb. Maybe in another file (bossAI_lunar.ts?). Grep.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:35:13.273Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"class LunarOrb\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\"; grep -rn \"kind: 8\\|kind: 7\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v protocol",
 "description": "Locate LunarOrb class and kind 8 packing"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:13.376Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts:1612:export class LunarOrb extends Entity {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts:1642:    return { kind: 8, tag: `${this.kind},${this.parentId}`, aux: 0, dmg: this.dmg };
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:1013:      kind: 7,

```


---

## 🤖 Assistant · 2026-08-12T08:35:14.760Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1630,1648p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts",
 "description": "Read LunarOrb netProjMeta"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:35:14.884Z

**📎 ToolResult**

```
    this.vx = vx; this.vy = vy;
    this.dmg = dmg;
    if (kind === 539) { this.w = 18; this.h = 30; }
    // v6 傀儡重建：parent=null 时由调用方传显式坐标
    this.x = (x ?? parent!.cx) - this.w / 2;
    this.y = (y ?? parent!.cy) - this.h / 2;
  }

  /** v6 联机打包：kind=8，tag=`${539|574},${parentId}`。
   *  访客重建后本地跑盘旋/冲刺/爆炸（确定性自包含，父=傀儡）；
   *  574 的线发 576 弹经 !netPuppet 门禁排除（房主侧已发） */
  netProjMeta(): NetProjMeta {
    return { kind: 8, tag: `${this.kind},${this.parentId}`, aux: 0, dmg: this.dmg };
  }

  /** 悬浮脑瞬移同步:全场计时 -30(:41682-41691) */
  delay(t: number): void { this.ai0 -= t; }

  fixedUpdate(_dt: number, game: GameHooks): void {

```


---

## 🤖 Assistant · 2026-08-12T08:36:02.895Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the tag formats:
- kind 5: tag = '1'/'0' (big flag)
- kind 6: tag = `${big},${ai1},${ai0}`
- kind 7: tag = `${srcId},${head|core bit}`, aux = sweep*10000, exVx/exVy = angle unit vector *1000
- kind 8: tag = `${539|574},${parentId}`

Client unpack cases match these. Good.

Now let me check some remaining audit points:

1. msg27 kind 1 (WeaponProj): netProjBroadcast sets kind=1 tag=projId for p.projId!==undefined before checking TrapShot... wait ordering: Arrow check first, then Dart, then `p.projId !== undefined` → kind 1 — but TrapShot has projId? TrapShot checked after, so unreachable if TrapShot has projId property. Hmm, does TrapShot have projId? The code path: `else if (p.projId !== undefined) { kind = 1; tag = String(p.projId); }` then `else if (p instanceof TrapShot)`. If TrapShot defines projId, kind 3 branch is dead. Let me check TrapShot class. Not strictly part of the audit but worth checking field consistency. Actually the audit focuses on protocol field matrix. Skip unless quick.

2. Probe coverage list: let me enumerate mechanisms vs assertions:
- AOI: player freeze (2 assertions), NPC puppet sweep/rebuild (2)
- 短码: 1 assertion (npcCodes >= 1)
- 合包: no direct assertion (code review only; /stats msgHist indirect)
- 背压分级: no assertion (only /stats sendDrops field presence check; loadprobe prints sendDrops but no threshold assertion)
- maxPlayers: 2 assertions (list maxPlayers, 满员 Kick)
- 限流: NO assertion at all (nothing sends >90 msg13/s to trigger kick) — 完全没覆盖
- 盲端踢 (blindAbuser): NO assertion — 完全没覆盖
- session认领: partial — reconnect same slot assertion exists (1); claimed-session release path (断开未 Hello 释放) not asserted
- 持久化: SIGTERM 落盘 + --world restart assertions (3)
- SSC (--ssc / msg201): 完全没覆盖 — probe never runs server with --ssc, never asserts msg201
- msg28: 1 assertion (弹幕消亡即时移除)
- 敌弹伤害: 3 assertions
- bit7门禁 (server strips non-host bit7): NOT asserted — probe never sends forged hostile from non-host
- 慢客户端踢 (send buffer >4MB kick): NOT covered
- 房主公告: NOT asserted! Probe only asserts 加入/离开公告 ("已加入"/"已离开") and color. The host-migration announcements (已成为房主/NPC 模拟暂停) are not asserted. Doc §8ter says 探针新增 3 断言 for v5 — those are hostile ones. Let me verify no assertion on 房主公告: grep chatLog usage — only joinMsg/leaveMsg. Confirmed gap.

Also note: the probe's join/leave assertion uses '已加入'/'已离开' — these come from Lang LegacyMultiplayer.19/20 zh text "已加入。" presumably. Fine.

Also the probe has UI 回归 + 持久化 etc.

3. Assertion count: 57 check( lines, minus 1 definition = 56 calls... wait grep -c "check('" counted 57 including the definition line? The definition is `const check = (name, ok, extra = '') => ...` which doesn't contain "check('" — it contains `check = (name`. So "check('" count 57 includes `const check = (` ? That has "check = (" not "check('". So 57 actual calls? Let me recount: `grep -c "check('"` = 57. And earlier `grep -n "check(" | wc -l` = 57 too. Hmm, both 57. That means the definition line `const check = (name, ok...` matches "check(" (57 includes def) but "check('" count also 57? The def line is `const check = (name, ok, extra = '') => {...}` — does it contain "check('"? No. Unless... `console.log(\`${ok ? 'PASS'...` no. Hmm, let me just count precisely with a better grep.

Let me also check whether probe runs are current — user says "54 断言". I'll report actual count.

4. Docs checks remaining:
- §7.3 says RoomPolicy S→C {roomCode, roomName, isHost, protectTiles, protectItems} — missing maxPlayers (v4). It's listed in §8bis table though. Conflict/stale.
- §7.3 探针 "14 断言" stale.
- §8bis header "PROTO_VER=4" stale vs current 6 (it's a historical record but header may mislead).
- §8bis AOI row "msg23+27 半径 1280px" stale → now 1536 (§8ter corrects).
- §8bis AOI row ">5s 无位置按全视野兜底" stale → now skip (corrected at §8ter bottom note).
- §6.2 限流阈值 "挖块 >500/min 告警、>2000/min 踢" vs implemented per-second per-msgId (TileBatch 180/s). Mismatch (old design number).
- §6.2 "WS 缓冲水位 >256KB 标记慢速跳过非关键广播" vs implemented 1MB/4MB thresholds. Mismatch.
- §6.4 "断线 120s 内" vs implemented 60s window + 61s timer. Mismatch!
- §6.4 "客户端退避 0.5s/1s/2s/5s 封顶" vs implemented 2s fixed ×3. Mismatch.
- §6.1 "module2 Ping 每 3000t (50s)" vs implemented Ping msg154 every 30s + server watchdog 120s (lastSeen += 1 per 1s interval; hmm: c.lastSeen increments every 1s tick and reset to 0 on any message; threshold 120 for state>=1 → 120s. matches doc 7200t=120s ✓).
- §2 message dictionary old conflicts as listed.
- §1.2 Hello payload has gameVer/features — impl has only magic+ver+name+token. Mismatch.
- §1.3 "字符串 = u7-bit 前缀长度" vs impl u16 长度前缀. Mismatch (documented in protocol.ts header as 简化集).
- §1.5 NetModule table: JoinLeave=3 conflicts with doc saying 3-14 暂缓 (module3=Ambience in vanilla; ours uses 3=JoinLeave) — protocol.ts comments acknowledge the clash, doc §1.5 row "3-14 ... 暂缓（占位跳过）" doesn't mention our module3 usage. Minor conflict.
- §8.6: "SpamCheck 默认关 ... 我们作为偏离项 §8.6 记录：挖块 >500/min 告警、>2000/min 踢" — actually §6.2 contains that. §8.6 row is the opt table entry. The 挂账清偿批 says 上行限流（§6.2 兑现). So §6.2 numbers remain stale but acknowledged as replaced. List as doc conflict.
- §8ter "AOI 半径 1536" ✓ matches code AOI_ENTITY=1536, AOI_PLAYER=1920, factor 1.6, AOI_STALE_MS 5000 ✓, prune 30s.
- §8ter 慢客户端踢 ✓.
- SSC semantics: doc record = {hp, maxHp, x, y, inv, armor, dye, savedAt}. Impl sscSaveClient: {hp, maxHp, x: lastX, y: lastY, inv, armor, dye, savedAt}. ✓ match. But note "id=内部下标" per protocol comment — fine. Also x/y use c.lastX/lastY which default -1e9 if never sent msg13 — edge case; minor.
- Also SSC load: does Game apply msg201? Check onSSC hook in Game. Quick grep.

5. _netfake health:
- Msg table includes ProjDespawn 28, SscSync 201 ✓, but lacks RoomPolicy 200, SyncItem 21, PlayerActive 14, StrikeNPC 42, RequestChestOpen 31, SyncChestItem 32, SetTime 18, StatusText 9, PlayerLifeMana 16 — probes don't reference these except... _loadprobe references Msg.WorldData, Msg.PlayerSpawn, Msg.SyncPlayer, Msg.RequestWorldData, Msg.PlayerSlot, Msg.PlayerState, Msg.SyncProjectile, Msg.SyncNPC, Msg.Hello — all present. RoomPolicy missing but not used. OK.
- PROTO_VER hardcoded 6 ✓ synced. Risk: divergence when bumping to 7 — must update _netfake.mjs; no single source.
- Writer vs NetWriter: u16 wraps (& 0xffff) vs DataView.setUint16 (also modulo) — equivalent. u32: both `>>> 0` (signed int32 limitation; NetWriter same) — fine. str: both u16-length+UTF8 ✓. finish guard both >65535 ✓. Missing f64/bool/i8 — not needed. One difference: NetWriter.u8(v) = v&255; Writer same. Writer.i16 uses writeInt16LE which throws on non-int16 out of range? Buffer.writeInt16LE coerces via ToNumber and modulo? Actually Node's writeInt16LE does bounds check: value outside [-32768, 32767] throws ERR_OUT_OF_RANGE? Let me think: Node's writeInt16LE verifies `value >= -32768 && value <= 32767`? Yes, Node int writers range-check and throw on out-of-range. NetWriter.i16 uses DataView.setInt16 which wraps silently. Difference: potential throw in probe if passing out-of-range i16. Not currently used with out-of-range values. Minor latent difference.

Also note Writer growth: need() doubles; str writes u16 length then need(bytes) — but u16() already need(2). fine.

Another subtle: _roomprobe's manual frame loop `if (len < 3) break;` after checking — OK.

6. 开服.sh: passes "$@" so --ssc/--max-players/--world-budget supported indirectly. Header documents only --world semantics + 300s auto-save + Ctrl-C 存档. It does NOT document --ssc. Also note: the script picks newest worlds/*.json and loads as 常驻房 — with --ssc not enabled by default. Also note `--save-interval` min 30 in code (Math.max(30,...)) — doc §3.3 says default 300s ✓.

Deployment note accuracy: doc §8bis says "SIGTERM 单播主进程实测 0.5s 落盘 ✓；对进程组发 TERM 与落盘并发会静默死亡... 生产用 systemd 直管主进程，避免 npx 包装层". 开服.sh uses `exec npx tsx src/index.ts` — exec replaces shell with npx, so signals go to npx which spawns tsx→node. The doc warns against npx wrapper in production, yet 开服.sh uses npx. Slight tension: 开服.sh is for LAN use; SIGTERM to the npx process works per _netfake comment ("SIGTERM 直杀直子（npx 级联到 tsx node 子进程）"). Fine but worth noting.

Also _loadprobe killServer uses process.kill(-server.pid, 'SIGKILL') group kill and later `server.kill('SIGTERM')` then killServer after 1s. Note _netfake.killGroup sends SIGTERM to direct child then SIGKILL group after 5s. OK.

Also: does 开服.sh cd into server/ and check node_modules — fine.

Now remaining: check Game's onSSC hook wiring (msg201 applied), and TrapShot projId ordering issue, and whether msg27 relaying preserves tag for kinds 5-8 with the aux/exVx — server passes aux through unchanged ✓ (aux relayed as-is). dmg clamped ✓.

One protocol matrix subtlety: msg27 S→C from server includes effKind (bit7 stripped for non-host). Client decodes kind into ProjSnap.kind and netMakeProj uses bit7 for hostile. ✓.

Another: server msg27 relay drops entries with (kind & 0x7f) > 8 — matches v6 doc. But protocol.ts comment says "kind 低 7 位: 0..8" ✓.

Check msg5: server broadcasts filtered valid entries via writePlayerItems (u16 count...) and ClientNet reads via readPlayerItems ✓. But protocol.ts msg5 comment says "u8 count" in Msg.SyncPlayerItem comment line 26-28: "{u8 count, entries[...]}" while implementation writePlayerItems uses w.u16(entries.length)! MISMATCH: comment says u8 count but code uses u16. Let me verify: protocol.ts line 241: `w.u16(entries.length);` and readPlayerItems line 253 `const n = r.u16();`. Comment line 27 says "u8 count". That's a doc-in-code inconsistency (comment wrong, both ends consistent since both use shared functions). Worth flagging as low severity.

Similarly msg17 TileBatch comment: protocol.ts line 41 says "TileBatch = 17, C→S→广播 {count, ops[]}" without type; writeTileBatch uses u16 count ✓ consistent with readTileBatch.

msg10 comment: "S→C {x0,y0,w,h, rleBytes}" and impl i32 x0, i32 y0, u16 w, u16 h ✓.

msg7 WorldData: protocol comment line 31 "{时间/尺寸/出生点/层线/flags/seed/name}" — impl order: f64 time, u32 dayCount, u16 w, u16 h, i32 spawnX/Y, f32 ground/rock/lava, i32 seed, str name, bool crimson, i32 dungeonX/Y, jungleX, u16 flagCount, [str,bool]*. Client readWorldData matches exactly ✓. Note crimson read after name ✓.

msg9 StatusText: comment {count}; impl u16 ✓ client u16 ✓. Doc §2 says i32 — conflict with doc only.

msg12 PlayerSpawn: impl {u8 slot, i32 x, i32 y} S→C; comment ✓. Client reads u8+i32+i32 ✓.

msg14 PlayerActive: impl {u8 slot, bool active, str name} ✓ client matches ✓.

msg16: {u8 slot, i16 hp, i16 maxHp} ✓ both ✓. Note: protocol enum comment says "双向" and doc says mana 同构 — impl no mana. fine.

msg18 SetTime: server sends msgId 18 hardcoded (new NetWriter(18)) with f64 + u32 ✓ client Msg.SetTime reads f64,u32 ✓.

msg21: impl as described ✓ client decode: reads netId, op, then only if op===0 reads key/stack/x/y/vx/vy ✓ matches server encode (server only writes fields for op 0) ✓. Edge: if op>2 server returns; op 1/2 short frame ✓ client handles ✓.

msg31/32 ✓ both match.

msg42 ✓ matches.

msg82 NetModules: Text {u16 moduleId, u8 slot, str text, u8 r,u8 g,u8 b} server ✓ client ✓. JoinLeave {u16 moduleId, u8 slot, bool joined} server ✓ client ✓. Client chat send: `new NetWriter(Msg.NetModules).u16(NetModule.Text).str(text)` — no slot; server reads moduleId then str ✓ consistent.

msg154 Ping: f64 ts both ✓.

Hello: {str magic, u16 ver, str name, str token} client ✓ server reads magic, ver, name, then token with try/catch ✓.

Kick: str reason ✓.

PlayerSlot: {u8 slot, str session} server ✓ client reads u8 + str(try/catch) ✓.

RoomPolicy ✓. SscSync ✓. ProjDespawn ✓.

SyncNPC covered. One more nuance: server fast path writes `f.u8(e.boss ? 2 : 0)` i.e., always short code (bit0=0), even in allKnown path. But what about the non-fast path when known — same. Fine.

Potential real bug to check in msg23: the fast path is only used when allFull (every target picked all entries). But there's a case: `allFull` initially true; targets with picked.length < entries.length set false. OK.

Hmm, but one actual subtle issue: in the fast path, if allKnown, it writes short codes for entries — including entries where some target's npcKnown contains code — checked. OK.

Another subtle: NPC entries cap n>64 return; client no cap. Fine.

Now check blindAbuser semantics vs doc: doc says 盲 >15s 仍发操作类消息即踢. Code: `c.lastPosAt > 0 && Date.now() - c.lastPosAt > AOI_STALE_MS + 10_000` = 5s+10s = 15s ✓. Applied on TileBatch, SyncChestItem, SyncItem, StrikeNPC — those are "操作类" ✓. Rate-limit kick reason '发送频率超限'.

Now, an important cross-check: slow-client kick in Room.send triggers kick() which does `c.ws.send(...)` directly bypassing outbox, then close. But kick() during the iteration over outbox flush? send() is called from handle() before flushOutbox. Fine.

Now, one inconsistency worth flagging: Room.send prio=0 >4MB kick happens on ANY prio=0 frame when buffer saturated — including during initial world strip streaming (TileSection is prio=0). A slow client during join gets kicked with '网络拥堵' — intended per doc.

Now let me verify the onSSC hook exists in Game.ts and also count probe assertions precisely. Also check the _roomprobe chatLog assertion text and the Lang text. And check whether probe covers "房主公告" — no.

Let me also check TrapShot projId ordering quickly for a real field bug, and check netProjBroadcast order: `else if (p.projId !== undefined) { kind = 1 }` before TrapShot. Does TrapShot have projId? grep class TrapShot.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:36:03.551Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"check('\" ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs | awk -F\"check('\" '{print $2}' | cut -c1-40 | head -60; echo ---COUNT---; grep -o \"check('\" ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs | wc -l",
 "description": "List all probe assertion names"
}
```


---

## 🤖 Assistant · 2026-08-12T08:36:04.333Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"onSSC\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head; echo ---; grep -n \"class TrapShot\" -A 12 ~/Project/GLM/SandboxWorld/game/src/entities/Projectile.ts 2>/dev/null | head -20 || grep -rn \"class TrapShot\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\"",
 "description": "Check onSSC hook and TrapShot definition"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:36:07.262Z

**📎 ToolResult**

```
awk: syntax error in regular expression check(' at 
 input record number 1, file 
 source line number 1
---COUNT---
      57

```


---

## 👤 User(sidechain) · 2026-08-12T08:36:07.323Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:87:  onSSC?: (recordJson: string) => void;
~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts:492:        this.hooks.onSSC?.(r.str());
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9846:        onSSC: (json) => this.netApplySSC(json),
---

```


---

## 🤖 Assistant · 2026-08-12T08:36:09.354Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"check('\" ~/Project/GLM/SandboxWorld/game/scripts/_roomprobe.mjs | sed \"s/.*check('//\" | sed \"s/'.*//\" | nl",
 "description": "List probe assertion names with numbering"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:36:09.399Z

**📎 ToolResult**

```
     1	A 世界就绪
     2	建房成功（6 位码 + hostToken）
     3	公开房出现在列表（含保护标记）
     4	码校验可达
     5	/stats 可达（全局+逐房+字段齐）
     6	公开房列表含 maxPlayers（P0.2）
     7	maxPlayers=2 房创建成功
     8	第三连接被拒（房间已满）
     9	A 房主进房成功
    10	A policy 双保护生效 + 门禁放行（房主）
    11	B 码加入成功
    12	B policy 非房主 + 门禁拦截（protectTiles/Items）
    13	双端互见
    14	AOI：B 出视野 → A 侧代理冻结（防幽灵行走）
    15	AOI：B 回视野 → 恢复接收 msg13
    16	B 非房主 tile op 被拒（本地回滚 + 房主侧不变）
    17	房主 tile op 中继到 B
    18	远端代理存在（控制位驱动物理）
    19	netOffset 已收敛（移动过程平滑，非瞬移残留）
    20	坐标零错位（左上角语义对齐，渲染位≈权威位 ±2px）
    21	物品同步（msg5 差分 → B 侧手持一致）
    22	远端挥舞动画（useItem 位 → swingNet）
    23	松开后挥舞结束清除
    24	NPC 快照→访客傀儡（msg23）
    25	NPC 快照→访客傀儡（msg23）
    26	msg23 短码表填充（v4 短码格式生效）
    27	访客打击上报→房主权威扣血（msg42）
    28	傀儡 hp 随快照收敛
    29	AOI：B 出视野 → NPC 傀儡被清扫
    30	AOI：B 回视野 → NPC 傀儡重建（2s 兜底重入）
    31	掉落物 spawn→访客傀儡（msg21）
    32	访客拾取→take→房主真身移除
    33	访客拾取入包（物品保护豁免拾取）
    34	HP 中继（msg16）
    35	敌对弹幕对访客伤害（v5 bit7 + Damage_EVP 本地结算）
    36	弹幕伤害经 msg16 中继到房主
    37	hostile 弹幕傀儡重建（bit7 解码）
    38	msg28 弹幕消亡即时移除傀儡
    39	箱子内容下发（msg31/32，服务器权威）
    40	protectItems：非房主编辑被服务端拒绝+纠正
    41	protectItems：非房主编辑被服务端拒绝+纠正
    42	箱子内容下发（msg31/32，服务器权威）
    43	断线自动重连（session 同 slot 复位）
    44	加入公告（"X已加入。"）
    45	离开公告（"X已离开。"，强制断线触发）
    46	公告颜色 (255,240,20)
    47	strip 编码缓存命中（重连场景）
    48	第二房（非公开）创建成功
    49	非公开房不出现在列表
    50	非公开房码可查（码加入可行）
    51	UI 房间列表点击加入
    52	进世界后进度遮罩已消失（不再卡"接收世界数据"）
    53	UI 进房 policy 正确（访客）
    54	SIGTERM 优雅退出
    55	SIGTERM 落盘世界档（room-<code>.json）
    56	--world 重启成功（常驻房）
    57	常驻房出现在新服列表（世界存活）

```


---

## 🤖 Assistant · 2026-08-12T08:36:15.422Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
57 assertion call sites (two are duplicates/conditional variants: #24/#25 same name, #40/#41 same name, #39/#42 same name) → the "passed" counter is 57 max in a full run; user's "54 断言" slightly off (probably counted before last additions). Report: 实际 57 处 check( 调用（3 组为同断言的双分支，实际断言点约 54 个唯一断言）— that's consistent! 57 - 3 duplicates = 54 unique assertions. 

Now let me double-check a couple of remaining code items for the matrix:
1. `netApplySSC` exists ✓.
2. The msg27 hostile strip: non-host bit7 → server masks. Probe coverage gap for the strip (no assertion).
3. Also check `Game.netProjBroadcast` comment "kind: 0=Arrow 1=WeaponProj族 2=Dart 3=TrapShot 4=MagicProj" — stale comment missing 5-8 (minor). Line 605 docstring says kind list ends at 4. Flag.

Also check protocol.ts Msg.SyncProjectile comment mentions bit7 carried by kind0/2/3 ✓ matches code (Arrow, Dart, TrapShot).

Now check the worker protocol.ts file to confirm no PROTO_VER there.

Also verify no other hardcoded version strings like "v5" in room/ClientNet (protocol.ts line 5 comment "当前 v5" — stale). Also check docs for v4/v5 misleading mentions: §8bis header "PROTO_VER=4" (historical), §8ter says 4→5 then 5→6. These are historical records, fine but note the §8bis header could mislead since current is 6.

Also: grep for any place hardcoding version number in client UI or elsewhere: search for "SW1" magic.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:36:16.355Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"SW1\" ~/Project/GLM/SandboxWorld --include=\"*.ts\" --include=\"*.mjs\" 2>/dev/null | grep -v node_modules; echo ---; grep -rn \"v4\\|v5\" ~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md | head; echo ---; sed -n '1,40p' ~/Project/GLM/SandboxWorld/game/src/workers/protocol.ts",
 "description": "Audit PROTO_MAGIC duplicates and doc v4/v5 mentions"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:36:16.747Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/scripts/_netfake.mjs:10:export const PROTO_MAGIC = 'SW1';
~/Project/GLM/SandboxWorld/game/src/net/protocol.ts:7:export const PROTO_MAGIC = 'SW1';
---
~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md:368:## 8ter. v5 补齐批（2026-08-12，review 后续）
~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md:379:- **Dart/TrapShot 补 hostile**：敌怪射击弹（`Enemy.shootDart` 咽喉 + 3 处直构）与机关/陷阱弹（TrapShot 构造时 `!style.friendly`）随 bit7 下发——v5 首版只覆盖 Boss Arrow 族，普通射击怪远程弹访客整体免疫；
---
// worldGen worker ↔ 主线程协议：世界数据包（packWorld 打包 / World.fromPacket 重建）
// + 生成/读档请求与事件联合。（type-only 模块——运行时消息按此形状对齐）
import type { SaveData } from '../save/serialize';
import type { ChestData } from '../world/World';
import type { WeatherSave } from '../world/weather/Weather';
import type { BestiarySave } from '../data/Bestiary';
import type { FurnitureItemRecord } from '../world/FurnitureItems';

/** tile 存储的转移所有权 buffer 组（worker postMessage transfer 零拷贝） */
export interface TileBuffers {
  type: ArrayBuffer; flags: ArrayBuffer;
  frameX: ArrayBuffer; frameY: ArrayBuffer;
  wall: ArrayBuffer; liquid: ArrayBuffer; liquidType: ArrayBuffer;
  half: ArrayBuffer; slope: ArrayBuffer; wire: ArrayBuffer;
  /** 战争迷雾（旧包可缺省——fromPacket 以全零补齐；saveGame 不持久化 explored） */
  explored?: ArrayBuffer;
}

export interface WorldPacket {
  w: number; h: number; seed: number; name: string;
  spawnX: number; spawnY: number;
  groundLevel: number; rockLevel: number; lavaLine: number;
  crimson: boolean; dungeonX: number; dungeonY: number; jungleX: number;
  exploredVersion: number;
  /** 世界难度 = Main.GameMode（0 经典 1 专家 2 大师 3 旅程；旧包缺省 0） */
  difficulty?: number;
  clock: { timeOfDay: number; dayCount: number; bloodMoon?: boolean; eclipse?: boolean; moonPhase?: number };
  /** 月亮贴图样式（原版 header moonType；旧包缺省 0） */
  moonType?: number;
  /** 入侵五元组（生成路径恒 0；读档路径经本包回传——packWorld 曾漏传致 worker 读档丢入侵） */
  invasion?: { type: number; size: number; sizeStart: number; x: number; delay: number };
  /** 已砸祭坛数（读档路径回传;旧包缺省 0） */
  altarCount?: number;
  /** 彩蛋种子旗标（SeedEasterEggs.parseSeed；血月 1/6 十周年 / drunkWorld 黎明翻转；旧包缺省={}） */
  seedFlags?: import('../world/gen/SeedEasterEggs').SeedFlags;
  /** 天气快照（读档路径回传;旧包缺省=晴） */
  weather?: WeatherSave;
  /** 图鉴三桶（读档路径回传;旧包缺省=空） */
  bestiary?: BestiarySave;
  /** 城镇 NPC 段（读档路径回传,Game.loadWorld 消费;旧包缺省=空→新世界出生分支） */

```


---

## 🤖 Assistant · 2026-08-12T08:36:30.381Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
workers/protocol.ts is the worldGen worker protocol — unrelated, no PROTO_VER. Good.

Now let me double check the doc claims to verify precisely what's in §8bis header: "## 8bis. 2026-08 容量优化批（已实施，PROTO_VER=4）" — stale (current 6), but historical.

Also check docs mention "msg21 不做 AOI" ✓ code ✓.

One more check: doc §8ter says 限流 "msg13≤90 / TileBatch≤180 / msg23/27/28/21≤60 / msg5≤30 / 聊天≤30 / msg42≤120" ✓ matches RATE_LIMIT exactly.

Check doc statement "空房且脏即时落盘" ✓ code.

Now, the last thing: does _roomprobe check the slow-client kick? No. Does _loadprobe assert sendDrops? It prints only.

Also potential probe staleness in assertions text:
- Line 201 comment "越过 1.5s stale 冻结阈值" — Game side freeze threshold 1.5s ✓ (need not verify).
- Line 418 comment "300 tick(5s)" — 300 ticks at 60fps = 5s ✓.
- Probe header comment (line 1-9) describes only v3-era 7 steps and "14 断言" isn't in probe; §7.3 doc says 14 断言. The probe header lists items 1-7 which matches v3 scope, missing later assertions description — stale doc header but harmless.
- _loadprobe comment "docs/multiplayer-design.md §8" numbers ✓.
- _roomprobe line 5 mentions "A 以 hostToken 进房（policy.isHost=true）" ✓.

Also check probe assertion 25 text mentions '探针桥'... fine.

Potential probe landmine with Writer: none currently.

One more: _netfake makeTinySave header seed 20260812 ✓; format version 3 — check save format version current is? loadSaveData may require version 3. Fine since probes presumably run green.

Now also verify that the doc §8bis "msg23 短码 ... PROTO_VER 3→4" ✓.

Let me also verify one potential REAL protocol inconsistency: In protocol.ts msg27 comment, "tag 各 kind 的打包格式 5-8" is not spelled out in protocol.ts (points to Game). The task asked to verify tag formats — I verified: kind5 tag='0'/'1'; kind6 'big,ai1,ai0'; kind7 'srcId,headbit' + aux=sweep*10000 + vx/vy=cos/sin*1000; kind8 'kind539|574,parentId'. Pack (netProjMeta) and unpack (netMakeProj) match. One asymmetry: kind7 netMakeProj reads `s.aux/10000` as sweep and uses `Math.atan2(s.vy, s.vx)` — packer sends exVx=cos*1000, exVy=sin*1000 → atan2 fine ✓. kind5 unpack: `s.tag[0] === '1'` — packer sends '1'/'0' ✓; but note netMakeProj kind5 passes enraged=false always and src=null — approximation (documented in doc as 猪鲨大弹狂暴速度差). Also note: kind5 tag uses only first char — robust.
kind8 unpack: `kind === 574 ? 574 : 539` ✓ packer `${this.kind}` where kind is 539|574 ✓.
kind6 unpack: split(',') → 3 numbers ✓ packer 3 fields ✓ netStateSync ✓.

Also worth noting: netProjBroadcast caps snaps at 24 and ClientNet/服务器 n≤64 ✓; msg23 caps 24 in loadprobe, real Game netNpcSnapshot — n cap? Game builds snaps; server caps n>64 return (drop whole packet). OK.

One genuine cross-end issue to flag: server msg23 handler drops the entire packet if n > 64 (`if (n > 64) return;`). ClientNet.sendNpcSnapshot has no cap. If host has >64 NPCs in a snapshot, the server silently drops → puppets never appear. Is there a cap in Game side? Let me check netNpcSnapshot caller — Game builds snaps list, does it cap? Let me grep quickly. If no cap, this is a real (moderate) issue: room with >64 visible NPCs → all dropped. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:36:30.652Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '560,600p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Check NPC snapshot batch cap on Game side"
}
```


---

## 👤 User(sidechain) · 2026-08-12T08:36:30.682Z

**📎 ToolResult**

```
  private netProjLast = new Map<number, { x: number; y: number; t: number }>();
  private netDropSeen = new Map<number, ItemDrop>();

  /** 快照广播轮转游标（review C4：固定遍历序 + >=24 break 会让第 25 个起的实体
   *  永远拿不到快照（入侵/血月 >24 同屏移动怪时后段集体饿死被误清）。游标本轮
   *  断在哪、下轮从哪继续，公平轮转） */
  private netNpcCursor = 0;
  private netProjCursor = 0;

  /** 房主：NPC 快照广播（15Hz，变化驱动 + 2s 兜底；对齐原版 msg23 netUpdate 思想） */
  private netNpcBroadcast() {
    const net = this.net!;
    const snaps: NpcSnap[] = [];
    const list = this.entities.enemies;
    const n = list.length;
    let examined = 0;
    for (; examined < n && snaps.length < 24; examined++) {
      const e = list[(this.netNpcCursor + examined) % n] as Enemy;
      if (e.netPuppet) continue;
      let last = this.netNpcLast.get(e.id);
      if (!last) {
        last = { x: e.x, y: e.y, hp: e.hp, t: this.tickCount };
        this.netNpcLast.set(e.id, last);
      }
      const moved = Math.abs(e.x - last.x) > 0.5 || Math.abs(e.y - last.y) > 0.5 || e.hp !== last.hp;
      if (!moved && this.tickCount - last.t < 120) continue; // 2s 全量兜底
      last.x = e.x; last.y = e.y; last.hp = e.hp; last.t = this.tickCount;
      snaps.push({
        netId: makeNetId(net.mySlot, e.id), key: e.key,
        x: e.x, y: e.y, vx: e.vx, vy: e.vy,
        hp: e.hp, maxHp: e.maxHp, animT: e.animT,
        flags: e.def.boss ? 1 : 0,
      });
    }
    this.netNpcCursor = (this.netNpcCursor + examined) % Math.max(1, n);
    // 清理已消亡敌人的差分基准（游标轮转下无条件跑——成本与主循环同阶）
    {
      const alive = new Set<number>();
      for (const ent of this.entities.enemies) alive.add((ent as Enemy).id);
      for (const id of this.netNpcLast.keys()) if (!alive.has(id)) this.netNpcLast.delete(id);
    }

```


---

## 🤖 Assistant · 2026-08-12T08:37:13.372Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Game caps at 24 per batch, so n≤24 < 64 — the server's 64 cap is never hit by the real client. Not a bug, just a guard. Good.

Now I have everything. Let me also double-check doc claim "PROTO_VER 4→5 ... 探针新增 3 断言（hostile 傀儡重建/本地伤害/msg16 中继），53 断言全绿" — current count 57 call sites / 54 unique. The doc says 53 — close; fine, historical.

Also the user prompt says probe has "54 断言" — 54 unique assertion names (57 call sites with 3 conditional duplicates). Consistent.

One more check for item 6: 开服.sh — verify it supports being run with --ssc etc. Yes via "$@". But note the `W=$(ls -t worlds/*.json | head -1)` path picks latest; if a room save exists it's loaded as 常驻房, so any extra rooms created at runtime also get saved to worlds/ on interval — note that on next start only ONE room is loaded (the newest). Multiple rooms aren't restored. Doc doesn't claim otherwise. Fine.

Also check: does 开服.sh mention --ssc? No. Doc deployment §7.2 mentions only port/world/save-interval. SSC is documented in §8ter only. Recommend adding to 开服.sh header comment. Low severity.

Also SIGTERM 单播 accuracy: doc says "SIGTERM 单播主进程实测 0.5s 落盘 ✓（systemd 默认行为）；对进程组发 TERM 与落盘并发会静默死亡... 生产用 systemd 直管主进程，避免 npx 包装层". But 开服.sh itself uses `exec npx tsx` — the npx wrapper layer. _netfake.killGroup comment says "SIGTERM 直杀直子（npx 级联到 tsx node 子进程；实测组播信号与落盘并发会让服务器静默死亡...勿用组播发 TERM）". So SIGTERM to direct child works. systemd 直管 npx would be "direct main process" = npx process. Consistent enough. I'll note: 部署注意 accurate; 开服.sh uses npx wrapper which doc warns about for production, but killGroup-style direct SIGTERM works.

Now let me verify the doc's SSC description "msg5/16/13 累积" — code: sscSaveClient uses c.hp/c.maxHp (from msg16) and c.items (from msg5) and x/y from c.lastX/c.lastY (from msg13). ✓. "断开/即时落盘" — code: disconnect (ws close) + also "空房且脏即时落盘" for world; SSC saved on ws close ✓. Is there a periodic SSC save? Doc says "断开/即时落盘" — the "即时" refers to world save. SSC: only on disconnect. Hmm "msg5/16/13 累积→断开/即时落盘 server/ssc/<name>.json" — could be read as two paths; actual SSC落盘 only on disconnect (ws close). Server crash = SSC loss since last disconnect. Worth flagging as wording ambiguity (SSC 无定时落盘，崩溃丢档窗口=整个会话).

Let me double check there's no periodic SSC save in persist.ts... index.ts only calls sscSaveClient on ws close. persist.ts has saveSscRecord/loadSscRecord. So yes — SSC only on disconnect. Flag as minor doc ambiguity.

Also check: sscLoad only assigned if SSC_ENABLED at connection time — assigned per-room at each connection (`if (SSC_ENABLED) room.sscLoad = ...` inside wss connection). Fine.

Edge: `c.hp`/`maxHp` default 0/0 → record maxHp `c.maxHp || 100`. x/y = lastX/lastY = -1e9 if never sent msg13 — would write garbage coords if a client disconnects before any msg13 (only if state>=10; state 10 requires SpawnTileData after which client sends msg13 quickly). Minor.

Now compile the final report in Chinese with the alignment table and inconsistency list with file:line.

Key inconsistencies list:

A. 协议矩阵（代码两端 vs protocol.ts 注释）
1. protocol.ts:26-28 Msg.SyncPlayerItem 注释写 "u8 count"，实际 writePlayerItems/readPlayerItems 用 u16（protocol.ts:241/253）。两端同源一致，仅注释错。低。
2. protocol.ts:5 头注释 "当前 v5" 实际 PROTO_VER=6（protocol.ts:16）。低（误导）。
3. protocol.ts:59-61 msg28 注释 ✓；两端口径一致。
4. msg27 tag 打包在 protocol.ts 未落表（指向 Game.netProjBroadcast）——Game.ts:605 函数头注释 kind 列表止于 4，缺 5-8（stale comment）。低。
5. msg23 C→S / S→C 短码：server(room.ts:518-623) ↔ client(ClientNet.ts:416-443, 688-700) ↔ protocol.ts:47-51 三方一致 ✓。
6. msg28: room.ts:728-739 ↔ ClientNet.ts:476-482,746-752 ↔ protocol.ts:59-61 一致 ✓（服务器 n>64 整包丢弃为防脏流护栏，真实客户端每批≤24 不会触达）。
7. msg200: room.ts:764-773 ↔ ClientNet.ts:400-410 ↔ protocol.ts:71 一致 ✓（客户端对旧版缺 maxPlayers 有 try/catch 兜底 255——向后兼容残留，v6 无互操作需求，无害）。
8. msg201: room.ts:366-370（SpawnTileData 时下发）↔ ClientNet.ts:490-493 ↔ protocol.ts:72-75 一致 ✓。
9. msg27 kind 值域/bit7: room.ts:671-674（(kind&0x7f)>8 丢条、非房主剥 bit7、dmg 钳 9999）↔ Game.ts:605-657/netMakeProj:773-806 ↔ protocol.ts:54-58 一致 ✓。
   tag 5-8 打包/解包对齐：kind5 'big位'；kind6 'big,ai1,ai0'；kind7 'srcId,head|core位'+aux=扫速×10000+vx/vy=cos/sin×1000；kind8 '539|574,parentId'——bossAI_duke_moonlord.ts:590/708/1011、bossAI_lunar_misc.ts:1642 ↔ Game.ts:784-804 逐字段对上 ✓。
10. msg21/31/32/42/16/82/154/Hello/Slot/Kick/7/9/10/12/13/14/17/18 两端逐字段一致 ✓（全部同用 NetWriter/共享编解码函数，无手工错位点）。
   - 唯一手工编码点：index.ts:300 `new NetWriter(18)` 用魔法数字而非 Msg.SetTime（枚举为 const enum，可用）；风格问题，低。
11. msg13 静止心跳：注释说 1s（ClientNet.ts:594），doc §8.1 说原版 420t；无冲突。

B. PROTO_VER 清点：使用点 = protocol.ts:16 定义、room.ts:6/314/315、ClientNet.ts:5/166、_netfake.mjs:10-11（PROTO_MAGIC/PROTO_VER 硬编码 6，探针独立副本）、两个探针 import。无遗漏硬编码版本号（全仓 grep PROTO_MAGIC 只有上述两处定义）。workers/protocol.ts 是世界生成 worker 协议，与联机无关 ✓。
   风险：_netfake.mjs 是第二份 PROTO_VER/MAGIC 真源，升 v7 时需手工同步（探针会因版本不匹配被踢，属于"fail loud"，尚可）。docs §8bis 标题"PROTO_VER=4"是历史记录，§8ter 已推进到 6——标题未标注"历史"，初读易误判当前版本。

C. 探针覆盖对账（诚实列表）：
有断言：maxPlayers（满员踢+列表字段）、AOI 玩家态 2 条、AOI NPC 态 2 条、msg23 短码表、msg42 打击、msg21 掉落 3 条、msg16、敌弹 bit7+本地伤害+中继 3 条、msg28 消亡 1 条、箱子 31/32+protectItems、双保护 tile、断线重连同 slot、加入/离开公告+颜色、strip 缓存命中、持久化 SIGTERM/--world 4 条、UI 回归 3 条、非公开房过滤。
只靠代码审查（无断言）：合包（上行 pendingFrames/服务器 flushOutbox——/stats 只看字段存在）、背压分级阈值（1MB/4MB 三档，/stats sendDrops 只打印不断言）、盲端"跳过"语义（stalePos 只打印）、慢客户端踢（prio=0 >4MB kick——完全无触发路径）、限流（RATE_LIMIT 9 条阈值——完全无触发路径）、bit7 门禁（非房主伪造 hostile 被剥除——无伪造用例）、msg21 三重校验（属主/key/maxStack——无伪造用例）、NaN 清洗、msg200 maxPlayers 的 WS 线上字段（断言走 HTTP /rooms 列表，未解码 WS 帧）、session 认领释放路径（握手前断线释放 claimed）、SSC msg201 全链路（探针从未以 --ssc 起服）、kind5-8 Boss 锚定弹体（探针只造 kind0 hostile 弹）、房主交接公告（"已成为房主"/"NPC 模拟暂停"文案无断言——探针只查加入/离开）。
探针文案过时：文件头注释（1-9 行）仍写 v3 的 7 步范围，未提 v4-v6 新断言；§7.3 文档"14 断言"严重过时（现 57 处 check/54 个唯一断言）。

D. 文档对账：
写了且做了 ✓：§8ter 慢客户端踢、房主公告、AOI 1536、msg28、限流阈值数字（与 RATE_LIMIT 逐一相符）、SSC 字段集 {hp,maxHp,x,y,inv,armor,dye,savedAt} 与 sscSaveClient(index.ts:40-48) 相符、判定位语义、空房脏即落盘。
写错/过时：
- §6.2 "挖块 >500/min 告警、>2000/min 踢" 与现实（TileBatch 180 包/s）不符——已被 §8ter 取代但旧数字未删。
- §6.2 "WS 缓冲 >256KB 标记慢速" 与现实（1MB/4MB 两档）不符。
- §6.4 "断线 120s 内携 token 重连" 与现实（60s 窗口+61s 定时器，room.ts:833/843）不符；"退避 0.5/1/2/5s 封顶" 与现实（固定 2s×3 次，ClientNet.ts:177-186）不符。
- §8bis AOI 行 "msg23+27 半径 1280px" 与 ">5s 无位置按全视野兜底" 均已被 1536/跳过语义取代（§8ter 尾部有修正记录，但行内未标注）。
- §8bis 标题 "PROTO_VER=4" 过时。
- §7.3 RoomPolicy 字段表缺 u16 maxPlayers（§8bis 有，正文没补）。
- §7.3 探针 "14 断言" 过时。
- §2 消息字典为 v0 调研稿，与 v6 线格式大面积冲突：msg2（u8 原因码+str vs 实际仅 str）、msg3（u8 特性位 vs str session）、msg5（SyncEquipment 单槽 vs 批量三容器）、msg9（i32 vs u16）、msg12（双向+respawnTimer/团队 vs S→C {slot,x,y}）、msg13（BitsByte ctrlA/ctrlB vs ctrlBits+flagBits 两字节）、msg23（原版 aiFlags/life 档位 vs 自有 netId/key 快照+短码）、msg27（原版 identity/owner/ai[] vs netId/kind/tag/dmg/aux）、msg28（原版 DamageNPC vs 现 ProjDespawn **同号不同义**——最危险的一条）、msg31-34 四条 vs 实际 31/32 两条、字符串 u7-bit 前缀（§1.3）vs 实际 u16 前缀、§1.2 Hello 的 gameVer/features 字段不存在、§1.5 NetModule 表 3 号位（原版 Ambience vs 我们 JoinLeave——protocol.ts:78-85 已注明撞号，doc 未提）。
- §8ter SSC "断开/即时落盘" 表述含糊：实际 SSC 仅在 ws close 落盘（index.ts:260），无定时刷盘——服务器崩溃丢整个会话的 SSC 增量，与"即时"字面印象不符（世界档才有空房即脏即时落盘）。

E. _netfake 健康度：Msg 表含 28/201（v6 同步 ✓）；缺 200/21/14/42/31/32/18/9 但探针未用，无雷。Writer vs NetWriter 行为差异：
- u16/u8/u32 都做模运算截断，等价；
- i16：Node writeInt16LE 越界抛 ERR_OUT_OF_RANGE，DataView.setInt16 静默回绕——探针若传越界 i16 会直接抛（当前无此用例）；
- str 编码一致（u16 长度+UTF-8）；finish 守卫一致；
- Writer 无 f64/bool/bytes——msg154 ping（f64）与 msg200（bool×3）若日后入探针需补方法。
- makeTinySave version:3——需与 save 格式版本同步（隐患：存档格式升级到 4 时探针静默坏）。低。
- spawnServer 的 killGroup 注释与 doc §8bis 部署注意一致 ✓。

F. 开服.sh/部署面：
- CLI 最终形态（index.ts:16-37）：--port/--max-rooms/--max-players/--world-budget/--upload-limit/--world/--save-interval/--ssc。开服.sh 经 "$@" 透传全部支持 ✓，但脚本头注释只写 --world 语义，未提 --ssc/--max-players/--world-budget。
- doc §7.2 部署示例 "node dist/index.js" 与现实（tsx 直跑；server 无 dist 构建产物链路说明）有出入——低。
- SIGTERM 单播注意事项准确（index.ts:336-350 shutdown 落盘→exit(0)；_netfake.mjs:81-89 注明组播信号致静默死亡）✓。开服.sh 用 exec npx 包装，doc 建议生产 systemd 直管避免 npx 层——脚本本身即 npx 层，家用场景实测 SIGTERM 直杀直子可级联，可用；生产建议维持 doc 口径。
- --save-interval 代码钳下限 30s（index.ts:33），doc §3.3 只写默认 300s，未提下限——极低。

Severity assignments. Also I should double check the claim "msg3 特性位" etc. Fine.

One more verification: does §7.3 doc say RoomPolicy lacks maxPlayers? Line 322: `Msg.RoomPolicy=200：S→C {roomCode, roomName, isHost, protectTiles, protectItems}` — yes missing maxPlayers. Confirmed.

Also confirm the doc's 探针 description at line 324 "14 断言". Yes.

Also worth noting: probe file header line 1 says "中央服务器房间制端到端验证（v3）" — stale.

I think I have a complete picture. Write the final report in Chinese. Keep it structured: 1) 对齐表, 2) 不一致清单, 3) 探针覆盖缺口, 4) PROTO_VER 清点, 5) 文档对账, 6) _netfake, 7) 开服.sh. Be thorough but organized.
```

</details>


---

## 🤖 Assistant · 2026-08-12T08:37:58.017Z · glm-x-preview-260804

```
# 多人联机跨端协议矩阵与文档对账终审报告

审计范围：`game/src/net/protocol.ts`、`server/src/room.ts`、`server/src/index.ts`、`game/src/net/ClientNet.ts`、`game/src/core/Game.ts`（netProjBroadcast/netMakeProj）、`bossAI_duke_moonlord.ts`、`bossAI_lunar_misc.ts`、`_roomprobe.mjs`、`_loadprobe.mjs`、`_netfake.mjs`、`docs/multiplayer-design.md`、`开服.sh`。

---

## 1. 协议字段矩阵（protocol.ts 注释 ↔ 服务器编码 ↔ 客户端解码）

### 1.1 五轮重点消息对齐表

| 消息 | 方向/格式基准（protocol.ts） | 服务器（room.ts） | 客户端（ClientNet.ts/Game.ts） | 结论 |
|---|---|---|---|---|
| **msg23 C→S** | `{u16 count,[u32 netId,str key,f32 x,y,vx,vy,i16 hp,maxHp,u16 animT,u8 flags]}`（:47-48） | 逐字段读 :526-530，n>64 整包丢 | `sendNpcSnapshot` :688-699 同序 | ✅ 一致 |
| **msg23 S→C 短码** | `{u16 count,[u8 eflags( bit0=全量: u32 netId+u16 codeId+str key / 否则仅 u16 codeId；bit1=boss), f32×4, i16×2, u16 animT]}`（:49-51） | 慢路径 :604-622 / allKnown 快速路径 :586-601，known 标记晚于 send | `handle Msg.SyncNPC` :416-443，未知短码先消费剩余字段再丢 | ✅ 一致 |
| **msg27** | kind 低 7 位 0-8 + bit7=hostile；`{u16 count,[u32 netId,u8 kind,str tag,i16 dmg,i16 aux,f32×4]}`（:52-58） | :654-726：(kind&0x7f)>8 丢条、非房主剥 bit7、dmg 钳 9999、AOI 滞回过滤 | `sendProjectileBatch` :732-742 / 解码 :456-467 / `netMakeProj` Game.ts:773-806 | ✅ 一致 |
| **msg28** | `{u16 count,[u32 netId]}` 双向（:59-61） | :728-739 中继（n>64 丢，prio=1） | 上行 :746-752（钳 64）/ 下行 :476-482 | ✅ 一致 |
| **msg200** | `{str code,str name,bool isHost,bool protectTiles,bool protectItems,u16 maxPlayers}`（:71） | `sendPolicy` :764-773 | :400-410（maxPlayers try/catch 兜底 255——v4 前兼容残留，无害） | ✅ 一致 |
| **msg201** | `{str recordJson}`，record={hp,maxHp,x,y,inv,armor,dye,savedAt}（:72-75） | SpawnTileData 分支 :366-370 下发 | :490-493 → `netApplySSC`（Game.ts:9846） | ✅ 一致 |

msg27 tag 打包格式（kind 5-8）打/解两侧逐字段核对一致：

| kind | 打包端 | tag 格式 | 解包端 |
|---|---|---|---|
| 5 DukeSharknadoBolt | duke_moonlord.ts:590 | `'1'/'0'`（big 位） | Game.ts:784 `s.tag[0]==='1'` |
| 6 SharknadoTornado | :708 | `` `${big},${ai1},${ai0}` `` | Game.ts:785-790 split 3 段 + netStateSync 反解 topY |
| 7 MLDeathray | :1011 | `` `${srcId},${head\|core位}` `` + aux=扫速×10000 + exVx/exVy=cos/sin×1000 | Game.ts:792-797 atan2(s.vy,s.vx) + aux/10000 |
| 8 LunarOrb | lunar_misc.ts:1642 | `` `${539\|574},${parentId}` `` | Game.ts:799-803 |

其余消息（1/2/3/4/5/7/8/9/10/12/13/14/16/17/18/21/31/32/42/82/154）全部经共享 NetWriter/readTileBatch/writePlayerItems 编解码，两端无手工错位点，均一致。

### 1.2 发现的不一致（代码内）

| # | 位置 | 期望 vs 现实 | 严重程度 |
|---|---|---|---|
| P1 | `protocol.ts:27` | Msg.SyncPlayerItem 注释写 **"u8 count"**，实际 `writePlayerItems/readPlayerItems` 用 **u16 count**（:241/:253）。两端同源一致，仅注释错 | 低（注释误导，勿照注释手写解码） |
| P2 | `protocol.ts:5` | 头注释"当前 **v5**"，实际 `PROTO_VER = 6`（:16） | 低（陈旧注释） |
| P3 | `Game.ts:605` | `netProjBroadcast` 函数头注释 kind 列表止于"4=MagicProj"，缺 v6 的 5-8 | 低（陈旧注释；branch 内有完整说明） |
| P4 | `index.ts:300` | `new NetWriter(18)` 用魔法数字而非 `Msg.SetTime` | 极低（风格；const enum 下写 `Msg.SetTime` 可行） |
| P5 | `room.ts:523/657/732` | msg23/27/28 `n > 64` **整包丢弃**；真实客户端每批硬顶 24（Game.ts:574/613/625），不可达，但探针/未来实现超限会静默失联 | 低（护栏合理，建议改"截断"或至少注释标明丢弃语义） |
| P6 | `room.ts:43`（sscSaveClient 在 index.ts:40-48） | SSC 记录 x/y 取 `c.lastX/lastY`，客户端若进房后从未发 msg13 即断线会写入 **-1e9 坐标**；且 SSC **仅 ws close 落盘**，无定时刷盘——崩溃丢整个会话增量 | 中低（SSC 数据质量/丢失窗口） |

---

## 2. PROTO_VER 使用点全量清点

全仓 grep（排除 node_modules 与 tsc 陈旧产物）结果，**共 7 处，无遗漏、无残留硬编码版本号**：

| 位置 | 性质 |
|---|---|
| `game/src/net/protocol.ts:16` | 定义（=6） |
| `server/src/room.ts:6, 314, 315` | import + Hello 门禁比对 |
| `game/src/net/ClientNet.ts:5, 166` | import + Hello 发送 |
| `game/scripts/_netfake.mjs:10-11` | **探针独立副本**（PROTO_MAGIC 'SW1' + PROTO_VER 6，硬编码） |
| `_roomprobe.mjs:11,99` / `_loadprobe.mjs:17,86` | 从 _netfake import |

- 全仓 `PROTO_MAGIC` 仅两处定义（protocol.ts:7、_netfake.mjs:10），无第三份散落。
- `game/src/workers/protocol.ts` 是世界生成 worker 的 WorldPacket 协议，与联机协议无关，不含 PROTO_VER，**不是冲突源**。
- 残留误导：`docs/multiplayer-design.md:343` §8bis 标题"（已实施，**PROTO_VER=4**）"未标注"历史"，初读易误判当前版本（§8ter 已推进至 6）。升 v7 时唯一需手工同步点是 `_netfake.mjs:11`（不同步会 fail loud——探针被版本门禁踢出，尚可接受，但建议加一行注释提醒）。

---

## 3. 探针覆盖对账（诚实列表）

`_roomprobe.mjs` 实测 **57 处 check( 调用 / 54 个唯一断言**（#24/25、#39/42、#40/41 为同断言的条件双分支）——与"54 断言"口径吻合；§7.3 文档写的"14 断言"严重过时。

### 有断言 ✅
maxPlayers（满员踢+列表字段）、AOI 玩家态冻结/恢复 2 条、AOI NPC 傀儡清扫/重建 2 条、msg23 短码表填充、msg42 打击→房主扣血→快照收敛、msg21 spawn/take/拾取入包 3 条、msg16 中继、敌弹 bit7（傀儡重建/本地伤害/msg16 回传 3 条）、**msg28 消亡即时移除 1 条**、箱子 31/32+protectItems 纠正、双保护 tile 拒绝/中继、断线重连同 slot、加入/离开公告+颜色、strip 缓存命中、SIGTERM 落盘+`--world` 重启 4 条、UI 进房回归 3 条、非公开房过滤。

### 只靠代码审查（探针有接触面但无阈值断言）⚠️
- **合包**（上行 pendingFrames / 服务器 flushOutbox）——仅 /stats 字段存在性检查，无"确实拼成单条 WS 消息"断言
- **背压分级**（1MB/4MB 三档）——/stats sendDrops 只打印不判
- **盲端"跳过"语义**——stalePos 只打印
- **session 认领释放路径**（握手前断线→claimed 复位）

### 完全没覆盖 ❌
1. **上行限流**（RATE_LIMIT 9 条阈值，room.ts:282-292）——探针无任何超频注入
2. **盲端踢 blindAbuser**（盲 >15s 发操作类消息即踢，room.ts:276-278）——无触发用例
3. **慢客户端踢**（prio=0 >4MB 带原因断连，room.ts:188-194）——无触发用例
4. **bit7 门禁**（非房主伪造 hostile 被剥除，room.ts:673）——只测了房主置位的正路径
5. **msg21 三重校验**（属主/key 反查/maxStack，room.ts:636-649）——无伪造用例
6. **SSC 全链路**——探针从未以 `--ssc` 起服，msg201 零覆盖
7. **kind 5-8 Boss 锚定弹体**——探针只造 kind0 hostile 弹，龙卷/死光/月珠重建与确定性 AI 零覆盖（`_dukemlprobe.mts` 若覆盖则另计，roomprobe 内无）
8. **房主交接公告**（"已成为房主"/"NPC 模拟暂停"，room.ts:326/819）——探针只断言加入/离开公告，**房主公告文案零覆盖**
9. msg200 的 maxPlayers **WS 线上字段**（断言走 HTTP /rooms 列表，未解码帧）
10. NaN 坐标清洗

### 探针自身过时文案
- `_roomprobe.mjs:1` 文件头仍写"（v3）"+ 7 步范围，未提 v4-v6 新增断言
- `_roomprobe.mjs:220` 注释"服务器判 A 盲（**>5s** 无 msg13）"与 AOI_STALE_MS=5000 相符 ✓；:418 "300 tick(5s)" ✓——正文注释无过时

---

## 4. 文档对账（multiplayer-design.md）

### §8bis/§8ter 逐条 vs 代码现状

| 条目 | 结论 |
|---|---|
| 慢客户端踢 | ✅ §8ter "prio=0 >4MB 带原因踢" = room.ts:188-194（文案"网络拥堵（发送缓冲持续超限）…"） |
| 房主公告 | ✅ §8ter 文案与 room.ts:326/819 一致；❌ 但探针零覆盖（见上） |
| SSC 语义 | ✅ 字段集 {hp,maxHp,x,y,inv,armor,dye,savedAt} 与 index.ts:40-48 逐字段相符；⚠️ "断开/**即时**落盘"表述含糊——SSC 实际**仅 ws close 落盘，无定时刷盘**，崩溃丢整个会话增量（"即时落盘"实际指世界档的空房即脏路径） |
| 限流阈值 | ✅ §8ter "msg13≤90/TileBatch≤180/msg23·27·28·21≤60/msg5≤30/聊天≤30/msg42≤120" 与 RATE_LIMIT **逐条相符** |
| AOI 半径 | ✅ §8ter 1536px = AOI_ENTITY；外径×1.6、stale 5s、prune 30s 全对上 |
| msg28 / kind5-8 / 盲端跳过 / 空房即脏落盘 / 全员全量快速路径 | ✅ 均与代码一致 |

### 写错/过时清单（按危险度）

| # | 位置 | 期望 vs 现实 | 严重程度 |
|---|---|---|---|
| D1 | §2 P3（:139）"**msg28 DamageNPC**（C→S→广播）：u8 npcSlot,i16 damage,…" | 现实 msg28=**ProjDespawn**（u16 count+u32 netId），同号**不同义**——照 §2 实现会直接对撞 | **高**（唯一会产出错误代码的一条） |
| D2 | §6.4（:266）"断线 **120s** 内携 token 重连" | 现实 **60s 窗口 + 61s 定时器**（room.ts:833/843）；"退避 0.5/1/2/5s 封顶" vs 现实固定 2s×3 次（ClientNet.ts:177-186） | 中 |
| D3 | §6.2（:255）"挖块 **>500/min 告警、>2000/min 踢**" | 现实 per-msgId **每秒**计数（TileBatch 180/s ≈ 10800/min），已被 §8ter 取代但旧数字未删 | 中 |
| D4 | §6.2（:256）"WS 缓冲 **>256KB** 标记慢速" | 现实 **1MB/4MB 两档**（room.ts:96-97） | 中 |
| D5 | §8bis（:354）"msg23+27 半径 **1280px**" + "**>5s 无位置按全视野兜底**" | 均已改 1536px / **跳过**（§8ter 尾部有修正记录，行内未标注"已修订"） | 中 |
| D6 | §8bis 标题（:343）"PROTO_VER=**4**" | 当前 6 | 低（历史记录，未标注） |
| D7 | §7.3（:322）RoomPolicy 字段表 | 缺尾部 u16 maxPlayers（§8bis 有，正文未补） | 低 |
| D8 | §7.3（:324）探针"**14 断言**" | 现 57 处/54 唯一 | 低（但误导性最强的一条数字） |
| D9 | §2 整章（:83-148）+ §1.2/§1.3/§1.5 | v0 调研稿与 v6 线格式大面积冲突：msg2（u8 原因码+str vs 仅 str）、msg3（u8 特性位 vs str session）、msg5（SyncEquipment 单槽 vs 批量三容器）、msg9（i32 vs u16）、msg12（双向+respawnTimer/团队 vs S→C {slot,x,y}）、msg13（BitsByte ctrlA/ctrlB vs ctrlBits+flagBits）、msg23/27（原版 aiFlags/identity/owner 布局 vs 自有 netId/key/kind/tag）、msg31-34 四条 vs 实际 31/32 两条、§1.3 字符串 u7-bit 前缀 vs 实际 **u16 前缀**、§1.2 Hello 的 gameVer/features 字段不存在、§1.5 NetModule 3 号位（原版 Ambience vs 我们 JoinLeave，protocol.ts:78-85 已注明撞号，doc 未提） | 中（整章为历史调研稿，建议加"以 protocol.ts 为准"横幅） |
| D10 | §7.2（:294）"node **dist**/index.js" | 现实 tsx 直跑，server 无 dist 构建链路说明 | 低 |
| D11 | §3.3（:187）`--save-interval` | 代码钳下限 30s（index.ts:33），doc 未提 | 极低 |

---

## 5. _netfake.mjs 健康度

- **Msg 表与 protocol.ts 同步**：v6 新增的 `ProjDespawn: 28`、`SscSync: 201` **均已补**（:12-16）✅。缺 `RoomPolicy:200 / SyncItem:21 / PlayerActive:14 / StrikeNPC:42 / RequestChestOpen:31 / SyncChestItem:32 / SetTime:18 / StatusText:9 / PlayerLifeMana:16`——两个探针均未引用，当前无雷。
- **Writer vs NetWriter 行为差异**：
  - u8/u16/u32 均模运算截断，**等价**；
  - **i16 不等价**：Node `writeInt16LE` 越界抛 `ERR_OUT_OF_RANGE`，`DataView.setInt16` 静默回绕——探针日后传越界 i16（如 dmg 钳位前原值）会直接崩，当前无此用例（**埋雷点，建议 Writer.i16 改 `v|0` 后 `& 0xffff` 写 u16**）；
  - str 编码一致（u16 长度+UTF-8）、finish 的 65535 守卫一致 ✅；
  - Writer **无 f64/bool/bytes**——若日后探针要发 msg154 Ping（f64）或伪造 msg200（3×bool）需先补方法，否则 TypeError。
- `makeTinySave` 写死 `version: 3`——存档格式升 4 时探针静默坏（与 `_netfake` 双真源同类风险），低。
- `spawnServer`/`killGroup` 的 SIGTERM 单播语义注释与 doc §8bis 部署注意一致 ✅。

---

## 6. 开服.sh / 部署面

- **CLI 最终形态**（index.ts:16-37）：`--port / --max-rooms / --max-players / --world-budget（默认 2GB，15B/格） / --upload-limit（默认 96MB） / --world / --save-interval（默认 300s，钳 ≥30） / --ssc`。开服.sh 经 `"$@"` **全部透传可用** ✅。
- 缺口：开服.sh 头注释只写 `--world` 与 300s 自动落盘，**未提 `--ssc`/`--max-players`/`--world-budget`**——SSC 是 v6 卖点，建议补一行示例（低）。
- **SIGTERM 单播注意事项准确**：index.ts:336-350 shutdown 落盘→`exit(0)`；`_netfake.mjs:81-89` 注明"组播信号与落盘并发会静默死亡，勿用组播发 TERM"与 doc §8bis 表述互证 ✅。开服.sh 自身即 `exec npx tsx` 包装层——doc 建议生产 systemd 直管主进程避免 npx 层，家用实测 SIGTERM 直杀直子可级联落盘，两者不矛盾，但脚本头可加一句"生产部署见 doc §8bis"。

---

## 总评

**线协议本体（含五轮改动的 msg23/27/28/200/201）两端+注释三方对齐，无字段序/类型/方向错位**；全部硬伤集中在三处非代码面：① doc §2 的 msg28 语义撞号（唯一可能产出错误实现的条目）；② doc §6.2/§6.4/§8bis 的过时数字（重连窗口、限流口径、AOI 半径、缓冲阈值）；③ 探针对 v6 对抗性机制的覆盖缺口——限流、盲端踢、慢客户端踢、bit7 门禁、msg21 校验、SSC、kind5-8、房主公告共 8 项完全无断言。代码内仅 6 处低危项（注释陈旧、msg5 count 注释、SSC 落盘窗口），无需改动线格式。
```
