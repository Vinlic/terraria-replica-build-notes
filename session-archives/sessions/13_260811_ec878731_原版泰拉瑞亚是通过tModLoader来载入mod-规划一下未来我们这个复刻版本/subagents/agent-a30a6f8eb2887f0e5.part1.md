# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T04:18:39.047Z

```
对 ~/Project/GLM/SandboxWorld 做代码审查,聚焦本轮联机容量优化批的**服务器侧**改动。搜索广度:very thorough。审查目标:正确性 bug、可靠性隐患(竞态/泄漏/崩溃路径)、性能热点。

审查范围:
1. server/src/room.ts —— 重点:
   - P1.1 AOI:broadcastAt/aoiBlind、msg23 短码路径(targets/allFull/allKnown 快速路径)、msg27 路径。检查:盲端跳过语义下有没有客户端永远收不到流的死锁路径?滞回集 aoiNpc/aoiProj/npcKnown 的泄漏与清理?allKnown 快速路径里 npcKnown 的更新时机是否与慢路径一致(漏更/重复)?entries 为空时的行为?
   - P1.3 合包:send/flushOutbox(切片逻辑 512KB,`size < FLUSH_SLICE && i < ob.length - 1` 的边界)、kick() 先冲刷再 close。检查:有没有调用点绕过 outbox 直接 ws.send 导致乱序?flushOutbox 在哪些路径之后没被调到(index.ts 的所有 send 触发点)?outbox 无上限堆积(背压只查 bufferedAmount,但排队期间 outbox 本身会无限涨吗)?
   - 背压分级 prio 参数的使用是否覆盖该覆盖的消息?
   - stripCache LRU 的正确性(淘汰最旧的 keys().next().value 是否真的是最旧?Map 插入序语义)、失效是否覆盖所有修改入口(applyTileOps 之外还有修改 tile 的路径吗,如液体?liquid 不走服务器,确认)。
   - npcCodes 清表 60000 后 codeId 复用与客户端 npcKnown 的失效一致性。
   - RoomClient 新字段初始化完备性(resumeSession 恢复的 client 是否走 newClient?)。
2. server/src/index.ts —— 内存预算(预检/计入/释放路径有没有漏 removeRoom 导致预算泄漏)、--world 常驻房、SIGTERM/SIGINT 双信号、saveRooms 的 interval 与 shutdown 并发。
3. server/src/stats.ts —— startBpsSampler 的清理、topMsgs 的性能(每房 /stats 调用)。
4. server/src/persist.ts —— saveRooms 的 skip 条件、tmp+rename 原子性、错误路径。
5. 与 game/src/net/protocol.ts 的协议一致性:服务器 msg23 下行编码(eflags bit0/bit1)与客户端解码是否逐字段对齐?RoomPolicy maxPlayers 追加方向?

不要泛泛而谈。每个发现给出:文件:行号、缺陷描述、具体触发场景(什么输入/时序→什么错误结果)、严重程度(高/中/低)。也列出你检查过但确认没问题的点(简短)。用中文。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T04:18:39.055Z

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

## 🤖 Assistant · 2026-08-12T04:18:40.225Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is a code review task for server-side changes in a multiplayer capacity optimization batch. Let me start by reading the relevant files thoroughly.

Let me read the main files first.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:18:40.299Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/room.ts"
}
```


---

## 🤖 Assistant · 2026-08-12T04:18:40.486Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/index.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:40.619Z

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
14	import { saveRooms } from './persist.ts';
15	
16	function arg(name: string, def?: string): string | undefined {
17	  const i = process.argv.indexOf(`--${name}`);
18	  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
19	}
20	const PORT = parseInt(arg('port', '7777')!, 10);
21	const MAX_ROOMS = parseInt(arg('max-rooms', '32')!, 10);
22	/** 单房人数逻辑上限默认值（POST /rooms 可按房覆盖；slot 物理上限恒 255） */
23	const DEFAULT_MAX_PLAYERS = Math.min(255, Math.max(2, parseInt(arg('max-players', '255')!, 10)));
24	/** P0.3 内存护栏：全服世界内存预算（TileStore 11B/格 估算；默认 2GB）。
25	 *  注意不能用位运算默认值：2<<30 溢出 int32 成负数（js-bitwise-int32-traps） */
26	const WORLD_BUDGET = parseInt(arg('world-budget', String(2 * 1024 * 1024 * 1024))!, 10);
27	/** 单存档上传上限（默认 96MB——4200×1200 实测 3.8MB，96MB 已是 25 倍余量） */
28	const WORLD_UPLOAD_LIMIT = parseInt(arg('upload-limit', String(96 * 1024 * 1024))!, 10);
29	/** P3.1 持久化：--world <path> 启动载入建常驻房；--save-interval 秒（默认 300） */
30	const WORLD_FILE = arg('world');
31	const SAVE_INTERVAL = Math.max(30, parseInt(arg('save-interval', '300')!, 10));
32	const WORLDS_DIR = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../worlds');
33	
34	// ================= 房间注册表 =================
35	
36	interface RoomEntry { room: Room; createdAt: number; /** P0.3 预算占用（w*h*11B） */ bytes: number; }
37	
38	const rooms = new Map<string, RoomEntry>(); // code → room
39	/** P0.3 已用世界内存预算 */
40	let worldBudgetUsed = 0;
41	
42	function newCode(): string {
43	  for (;;) {
44	    const code = String(Math.floor(Math.random() * 900000) + 100000); // 6 位数字
45	    if (!rooms.has(code)) return code;
46	  }
47	}
48	
49	/** 统一摘除（回收/关房共用）：释放内存预算 */
50	function removeRoom(code: string) {
51	  const entry = rooms.get(code);
52	  if (!entry) return;
53	  entry.room.closed = true;
54	  worldBudgetUsed -= entry.bytes;
55	  rooms.delete(code);
56	}
57	
58	/** 空房回收（创建满 1 分钟且一直无人满 5 分钟 → 关闭回收；--world 常驻房豁免） */
59	setInterval(() => {
60	  const now = Date.now();
61	  for (const [code, entry] of rooms) {
62	    if (entry.room.persistent) continue;
63	    const idle = now - entry.createdAt;
64	    if (entry.room.closed || (entry.room.onlineCount === 0 && idle > 60_000 && idle > 5 * 60_000)) {
65	      removeRoom(code);
66	      console.log(`[room] 回收空房 ${code}`);
67	    }
68	  }
69	}, 60_000);
70	
71	function worldFromSaveJson(json: string) {
72	  return loadSaveData(JSON.parse(json)).world;
73	}
74	
75	/** 本机全部局域网 IPv4（多网卡全列出——UI 分享用） */
76	function lanIps(): string[] {
77	  const out: string[] = [];
78	  for (const list of Object.values(node_os.networkInterfaces())) {
79	    for (const ni of list ?? []) {
80	      if (ni.family === 'IPv4' && !ni.internal) out.push(ni.address);
81	    }
82	  }
83	  return out;
84	}
85	
86	// ================= HTTP Lobby =================
87	
88	const CORS = {
89	  'Access-Control-Allow-Origin': '*',
90	  'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
91	  'Access-Control-Allow-Headers': 'Content-Type',
92	  'Access-Control-Allow-Private-Network': 'true',
93	};
94	
95	function readBody(req: http.IncomingMessage, limit: number): Promise<Buffer> {
96	  return new Promise((resolveBody, reject) => {
97	    const chunks: Buffer[] = [];
98	    let size = 0;
99	    req.on('data', (d: Buffer) => {
100	      size += d.length;
101	      if (size > limit) { reject(new Error('上传超限')); req.destroy(); return; }
102	      chunks.push(d);
103	    });
104	    req.on('end', () => resolveBody(Buffer.concat(chunks)));
105	    req.on('error', reject);
106	  });
107	}
108	
109	const lobby = http.createServer(async (req, res) => {
110	  const url = new URL(req.url ?? '/', `http://127.0.0.1:${PORT}`);
111	  const finish = (code: number, data: unknown) => {
112	    res.writeHead(code, { 'Content-Type': 'application/json', ...CORS });
113	    res.end(JSON.stringify(data));
114	  };
115	  if (req.method === 'OPTIONS') { finish(204, {}); return; }
116	
117	  try {
118	    // GET /stats → 观测快照（P0.1；全局 + 逐房 + 逐客户端）
119	    if (req.method === 'GET' && url.pathname === '/stats') {
120	      finish(200, statsSnapshot([...rooms.values()].map((e) => e.room)));
121	      return;
122	    }
123	    // GET /rooms → 公开房间列表（非公开不展示，只能码进）
124	    if (req.method === 'GET' && url.pathname === '/rooms') {
125	      const list = [...rooms.values()]
126	        .filter((e) => e.room.opts.publicRoom && !e.room.closed)
127	        .map((e) => ({
128	          code: e.room.opts.code, name: e.room.opts.name,
129	          online: e.room.onlineCount, maxPlayers: e.room.opts.maxPlayers, w: e.room.world.w, h: e.room.world.h,
130	          protectTiles: e.room.opts.protectTiles, protectItems: e.room.opts.protectItems,
131	        }));
132	      finish(200, { ok: true, rooms: list });
133	      return;
134	    }
135	    const m = url.pathname.match(/^\/rooms\/(\d{6})$/);
136	    // GET /rooms/<code> → 房间码校验（加入前置检查，非公开房也允许码查）
137	    if (req.method === 'GET' && m) {
138	      const entry = rooms.get(m[1]);
139	      if (!entry || entry.room.closed) { finish(404, { ok: false, error: '房间不存在' }); return; }
140	      finish(200, {
141	        ok: true, code: entry.room.opts.code, name: entry.room.opts.name,
142	        online: entry.room.onlineCount,
143	        protectTiles: entry.room.opts.protectTiles, protectItems: entry.room.opts.protectItems,
144	        // 首箱锚点（调试/探针确定性用；LAN 游戏服务器无敏感性）
145	        chest: entry.room.world.chests[0] ? { x: entry.room.world.chests[0].x, y: entry.room.world.chests[0].y } : null,
146	      });
147	      return;
148	    }
149	    // POST /rooms → 创建房间（body: {name, public, protectTiles, protectItems, maxPlayers, save}）
150	    if (req.method === 'POST' && url.pathname === '/rooms') {
151	      if (rooms.size >= MAX_ROOMS) { finish(503, { ok: false, error: '服务器房间已满' }); return; }
152	      // P0.3 预检①：上传体积预拒（读 body 前按 limit 截断，防超大 body 打爆内存）
153	      const raw = await readBody(req, WORLD_UPLOAD_LIMIT).catch(() => null);
154	      if (!raw) { finish(400, { ok: false, error: `上传超限（>${Math.round(WORLD_UPLOAD_LIMIT / 1048576)}MB）` }); return; }
155	      const body = JSON.parse(raw.toString('utf8')) as {
156	        name?: string; public?: boolean; protectTiles?: boolean; protectItems?: boolean; maxPlayers?: number; save?: string;
157	      };
158	      if (!body.save) { finish(400, { ok: false, error: '缺少 save（世界存档 JSON）' }); return; }
159	      // P0.3 预检②：全服世界内存预算（TileStore 11B/格 估算）
160	      let worldW = 0, worldH = 0;
161	      try {
162	        const head = JSON.parse(body.save) as { header?: { width?: number; height?: number } };
163	        worldW = head.header?.width ?? 0;
164	        worldH = head.header?.height ?? 0;
165	      } catch { /* 走 worldFromSaveJson 的解析错误 */ }
166	      const estBytes = worldW * worldH * 11;
167	      if (estBytes > 0 && worldBudgetUsed + estBytes > WORLD_BUDGET) {
168	        finish(503, { ok: false, error: `服务器世界内存预算不足（已用 ${(worldBudgetUsed / 1048576) | 0}MB / ${(WORLD_BUDGET / 1048576) | 0}MB）` });
169	        return;
170	      }
171	      const world = worldFromSaveJson(body.save);
172	      const room = new Room(world);
173	      room.opts.code = newCode();
174	      room.opts.maxPlayers = Math.min(255, Math.max(2, body.maxPlayers ?? DEFAULT_MAX_PLAYERS));
175	      if (body.name) world.name = body.name, room.opts.name = body.name;
176	      room.opts.publicRoom = !!body.public;
177	      room.opts.protectTiles = !!body.protectTiles;
178	      room.opts.protectItems = !!body.protectItems;
179	      room.opts.hostToken = randomUUID();
180	      worldBudgetUsed += estBytes || world.w * world.h * 11;
181	      rooms.set(room.opts.code, { room, createdAt: Date.now(), bytes: estBytes || world.w * world.h * 11 });
182	      console.log(`[room] 创建 ${room.opts.code}（${world.name} ${world.w}×${world.h} 公开=${room.opts.publicRoom} 破坏保护=${room.opts.protectTiles} 物品保护=${room.opts.protectItems} 上限=${room.opts.maxPlayers}人 预算=${(worldBudgetUsed / 1048576) | 0}/${(WORLD_BUDGET / 1048576) | 0}MB）`);
183	      finish(200, {
184	        ok: true, code: room.opts.code, hostToken: room.opts.hostToken,
185	        name: room.opts.name, protectTiles: room.opts.protectTiles, protectItems: room.opts.protectItems,
186	      });
187	      return;
188	    }
189	    // DELETE /rooms/<code>?token= → 房主关房（--world 常驻房不可关）
190	    if (req.method === 'DELETE' && m) {
191	      const entry = rooms.get(m[1]);
192	      if (!entry) { finish(404, { ok: false, error: '房间不存在' }); return; }
193	      if (entry.room.persistent) { finish(403, { ok: false, error: '常驻房不可关闭' }); return; }
194	      if (url.searchParams.get('token') !== entry.room.opts.hostToken) {
195	        finish(403, { ok: false, error: '仅房主可关房' }); return;
196	      }
197	      removeRoom(m[1]);
198	      finish(200, { ok: true });
199	      return;
200	    }
201	    // GET /lan → 本机信息（IP 分享 + 发现端点）
202	    if (req.method === 'GET' && url.pathname === '/lan') {
203	      finish(200, { ok: true, magic: 1010, port: PORT, rooms: rooms.size, lanIps: lanIps() });
204	      return;
205	    }
206	    finish(404, { ok: false, error: 'not found' });
207	  } catch (e) {
208	    finish(400, { ok: false, error: (e as Error).message });
209	  }
210	});
211	lobby.listen(PORT + 1);
212	
213	// ================= WebSocket（URL = /<房间码>?token=<房主令牌可选>） =================
214	
215	const wss = new WebSocketServer({ port: PORT, maxPayload: 1 << 20 });
216	
217	wss.on('connection', (ws: WebSocket, req) => {
218	  ws.binaryType = 'nodebuffer';
219	  const m = (req.url ?? '').match(/^\/(\d{6})/);
220	  if (!m) { ws.close(1002, '需要房间码路径 /<6位码>'); return; }
221	  const entry = rooms.get(m[1]);
222	  if (!entry || entry.room.closed) { ws.close(1002, '房间不存在'); return; }
223	  const room = entry.room;
224	  const token = new URL(req.url ?? '/', 'http://x').searchParams.get('token') ?? '';
225	  const session = new URL(req.url ?? '/', 'http://x').searchParams.get('session') ?? '';
226	  const c = room.newClient(ws, token);
227	  if (session) room.resumeSession(c, session); // 断线重连：命中则 Hello 时同 slot 复位
228	  console.log(`[ws] 连入房间 ${room.opts.code}`);
229	
230	  ws.on('message', (data: Buffer) => {
231	    c.stats.inBytes += data.length;
232	    c.parser.append(new Uint8Array(data));
233	    try {
234	      c.parser.drain((msgId, r) => room.handle(c, msgId, r));
235	    } catch (e) {
236	      console.error(`[ws] 房间 ${room.opts.code} slot ${c.slot} 异常断开:`, (e as Error).message);
237	      try { ws.close(1002); } catch { /* 已关闭 */ }
238	    }
239	    // P1.3 合包：本条 WS 消息处理完毕，统一冲洗各客户端发送队列
240	    room.flushOutbox();
241	  });
242	  ws.on('close', () => {
243	    room.disconnect(c);
244	    room.flushOutbox();
245	    console.log(`[ws] slot ${c.slot} 离开房间 ${room.opts.code}（在线 ${room.onlineCount}）`);
246	  });
247	  ws.on('error', () => { /* close 跟上 */ });
248	});
249	
250	// 超时看门狗：逐房逐客户端（未握手 10s / 已握手 120s，对齐原版 TimeOutTimer）
251	setInterval(() => {
252	  for (const entry of rooms.values()) {
253	    for (const c of [...entry.room.clients]) {
254	      c.lastSeen += 1;
255	      if (c.lastSeen > (c.state >= 1 ? 120 : 10)) {
256	        console.log(`[ws] 房间 ${entry.room.opts.code} slot ${c.slot} 超时踢出`);
257	        c.ws.close();
258	      }
259	    }
260	  }
261	}, 1000);
262	
263	// 时间同步：服务器权威时钟推进（对齐原版 WorldGen.UpdateWorld 时钟）+ 10s 广播
264	setInterval(() => {
265	  for (const entry of rooms.values()) entry.room.world.clock.tick(1000);
266	}, 1000);
267	setInterval(() => {
268	  for (const entry of rooms.values()) {
269	    const room = entry.room;
270	    const f = new NetWriter(18).f64(room.world.clock.timeOfDay).u32(room.world.clock.dayCount).finish();
271	    for (const c of room.clients) if (c.state >= 10) room.send(c, f);
272	    room.flushOutbox();
273	  }
274	}, 10000);
275	
276	// ================= P0.1 观测：1s outBps 采样 =================
277	startBpsSampler(() => [...rooms.values()].map((e) => e.room));
278	
279	// ================= P3.1 持久化：--world 常驻房 + 定时落盘 + 信号退出 =================
280	if (WORLD_FILE) {
281	  try {
282	    const json = fs.readFileSync(WORLD_FILE, 'utf8');
283	    const world = worldFromSaveJson(json);
284	    const room = new Room(world);
285	    room.opts.code = newCode();
286	    room.opts.publicRoom = true;
287	    room.opts.hostToken = '';        // 无主房：首位进房者为房主（NPC 权威源）
288	    room.opts.maxPlayers = DEFAULT_MAX_PLAYERS;
289	    room.persistent = true;
290	    const bytes = world.w * world.h * 11;
291	    worldBudgetUsed += bytes;
292	    rooms.set(room.opts.code, { room, createdAt: Date.now(), bytes });
293	    console.log(`[room] --world 常驻房 ${room.opts.code}（${world.name} ${world.w}×${world.h} 上限=${room.opts.maxPlayers}人）`);
294	  } catch (e) {
295	    console.error(`[server] --world ${WORLD_FILE} 载入失败:`, (e as Error).message);
296	    process.exit(1);
297	  }
298	}
299	
300	const roomList = () => [...rooms.values()].map((e) => e.room);
301	setInterval(() => {
302	  const r = saveRooms(roomList(), WORLDS_DIR);
303	  if (r.saved) console.log(`[persist] auto-save：${r.saved} 房落盘，${r.skipped} 房跳过`);
304	}, SAVE_INTERVAL * 1000).unref?.();
305	
306	let shuttingDown = false;
307	function shutdown(sig: string) {
308	  if (shuttingDown) return;
309	  shuttingDown = true;
310	  console.log(`[server] 收到 ${sig}，落盘全部房间…`);
311	  try {
312	    const r = saveRooms(roomList(), WORLDS_DIR);
313	    console.log(`[persist] 退出存档：${r.saved} 房保存，${r.skipped} 房跳过`);
314	  } catch (e) {
315	    console.error('[persist] 退出存档失败:', (e as Error).message);
316	  }
317	  process.exit(0);
318	}
319	process.on('SIGTERM', () => shutdown('SIGTERM'));
320	process.on('SIGINT', () => shutdown('SIGINT'));
321	
322	process.on('uncaughtException', (e) => {
323	  console.error('[server] uncaughtException（记录不退出）:', (e as Error).stack ?? e);
324	});
325	
326	console.log(`[server] 中央服务器 ws://0.0.0.0:${PORT}（lobby http://0.0.0.0:${PORT + 1}/rooms）`);
327	

```


---

## 👤 User(sidechain) · 2026-08-12T04:18:40.623Z

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
13	import { ITEM_DEFS } from '../../game/src/data/items.ts';
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
26	/** 每客户端观测计数（P0.1 /stats） */
27	export interface ClientStats {
28	  inBytes: number; outBytes: number;
29	  bufferedMax: number;   // ws.bufferedAmount 高水位
30	  sendDrops: number;     // 背压丢弃总帧数
31	  lowDrops: number;      // 其中 prio=1（实体快照类）低水位先行丢弃
32	}
33	
34	/** 每房观测计数（P0.1 /stats；outBps 由 stats.ts 1s 差分采样写入） */
35	export interface RoomStats {
36	  outBytes: number; outBps: number; lastSampleAt: number;
37	  msgHist: Map<number, { n: number; bytes: number }>;
38	  sendDrops: number; stalePos: number;
39	  stripHit: number; stripMiss: number;  // P2.1 section 缓存
40	  tileOps: number;                      // 累计 tile op 数（P3.1 持久化脏标记用）
41	}
42	
43	export interface RoomClient {
44	  ws: WebSocket;
45	  parser: FrameParser;
46	  slot: number;
47	  state: number;        // 对齐原版：0 连接 / 1 过握手 / 10 在游戏
48	  name: string;
49	  appearance: string;
50	  lastSeen: number;
51	  isHost: boolean;
52	  /** URL 携带的房主令牌（路由层注入；Hello 消息内 token 为兜底） */
53	  urlToken?: string;
54	  /** 重连凭据（PlayerSlot 下发；断开后 60s 内携此 session 重连同 slot 复位） */
55	  session: string;
56	  /** 重连恢复的 slot（≥0 时 Hello 跳过分配直接复位） */
57	  resumedSlot: number;
58	  sentStrips: Set<string>;
59	  /** AOI 接收端位置（由其上行 msg13 顺带更新；px 坐标，P1.1） */
60	  lastX: number; lastY: number; lastPosAt: number;
61	  /** AOI 滞回集合：netId → 最近一次出现在某快照批的时刻（P1.1） */
62	  aoiNpc: Map<number, number>;
63	  aoiProj: Map<number, number>;
64	  /** 滞回集/短码集上次过期清理时刻 */
65	  lastAoiPrune: number;
66	  /** msg23 短码已知集：codeId → 最近使用时刻（P1.2；过期清除后自动回落全量） */
67	  npcKnown: Map<number, number>;
68	  /** 发送合包暂存（P1.3；ws message 回调末尾 flushOutbox 统一拼发） */
69	  outbox: Uint8Array[];
70	  stats: ClientStats;
71	  /** 物品快照（msg5 累积；新人进场时全量下发） */
72	  items: {
73	    inv: Array<{ id: number; stack: number } | null>;
74	    armor: Array<{ id: number; stack: number } | null>;
75	    dye: Array<{ id: number; stack: number } | null>;
76	  };
77	}
78	
79	/** slot 物理上限（u8 协议槽位；逻辑上限 = opts.maxPlayers 可小于此值） */
80	const MAX_PLAYERS = 255;
81	const STRIP_W = 200;
82	const STRIP_H = 20;
83	/** 背压分级（P0.1）：≤1MB 正常；1-4MB 只丢 prio=1（实体快照类）；>4MB 全丢。全计数 */
84	const LOW_BUFFER_LIMIT = 1 << 20;
85	const SEND_BUFFER_LIMIT = 4 << 20;
86	/** 单条合包 WS 消息切片上限（防超 wss maxPayload 1MB；留余量） */
87	const FLUSH_SLICE = 512 * 1024;
88	/** 箱子 tile sheet id（TileID.Chest=21；applyTileOps 清箱检测用） */
89	const CHEST_TILE_ID = 21;
90	// ---- P1.1 实体 AOI（切比雪夫距离，px）----
91	const AOI_PLAYER = 1920;  // msg13 远端玩家：120 tiles（同屏协作+建造）
92	const AOI_ENTITY = 1280;  // msg23 NPC / msg27 弹幕：80 tiles（战斗可视）
93	const AOI_OUT_FACTOR = 1.6;   // 滞回外径 = 内径 ×1.6（边界抖动防闪烁）
94	const AOI_STALE_MS = 5000;    // 接收端位置超时：跳过实体广播（见 aoiBlind——防饱和放大循环）
95	const AOI_PRUNE_MS = 30_000;  // 滞回集/短码已知集的过期清理
96	// 不变量（改动前必读）：NPC 静止兜底间隔（客户端 2s=120 tick）必须 ≪ 傀儡清扫阈值
97	// （300 tick）——AOI 重入视野后 ≤2s 内必有全量快照补 key，傀儡不会被误清。
98	// msg21 掉落物不做 AOI：spawn 是一次性事件（无重播机制），过滤会导致走近的玩家永远看不见。
99	
100	export class Room {
101	  readonly opts: RoomOptions;
102	  clients = new Set<RoomClient>();
103	  private slotUsed = new Array<boolean>(MAX_PLAYERS).fill(false);
104	  private hostJoined = false;
105	  /** 断线 session 保留（§8.8 重连：60s 内携 session 重连同 slot 复位，不刷加入公告） */
106	  private sessions = new Map<string, { slot: number; name: string; appearance: string; until: number }>();
107	  closed = false;
108	  /** --world 常驻房（P3.1）：空房回收豁免；hostToken='' 首进者为房主 */
109	  persistent = false;
110	  /** 上次持久化时的 tileOps 基线（P3.1：空房无修改则跳过写盘） */
111	  lastSavedTileOps = 0;
112	  /** 观测计数（P0.1；stats.ts 采样读取） */
113	  readonly roomStats: RoomStats = {
114	    outBytes: 0, outBps: 0, lastSampleAt: Date.now(),
115	    msgHist: new Map(), sendDrops: 0, stalePos: 0,
116	    stripHit: 0, stripMiss: 0, tileOps: 0,
117	  };
118	  /** msg23 短码表（P1.2）：netId → codeId；放 Room 级（服务器权威模拟将来直接复用） */
119	  private npcCodes = new Map<number, number>();
120	  private npcCodeSeq = 1;
121	  /** section 编码缓存（P2.1）：条带 key → 完整帧；插入序即 LRU，上限 512 条带 */
122	  private stripCache = new Map<string, Uint8Array>();
123	
124	  constructor(public world: World) {
125	    this.opts = { code: '', name: world.name, publicRoom: true, protectTiles: false, protectItems: false, hostToken: '', maxPlayers: MAX_PLAYERS };
126	  }
127	
128	  get st() { return this.world.store; }
129	  get onlineCount() { let n = 0; for (const c of this.clients) if (c.state >= 10) n++; return n; }
130	
131	  private allocSlot(): number {
132	    // 逻辑上限只约束分配边界；slotUsed 数组保持 255 物理上限（重连复位可能 ≥ 逻辑上限）
133	    for (let i = 0; i < this.opts.maxPlayers; i++) if (!this.slotUsed[i]) { this.slotUsed[i] = true; return i; }
134	    return -1;
135	  }
136	
137	  /** msg23 合法来源（房主权威；P5 服务器权威模拟时改为 `this.sim ? false : c.isHost`） */
138	  private npcAuthority(c: RoomClient): boolean { return c.isHost; }
139	
140	  /** msg42 转发目标（现 = 房主单播；P5 服务器权威时 = 本 Room 结算，无转发） */
141	  private strikeTarget(): RoomClient | null {
142	    for (const c of this.clients) if (c.isHost && c.state >= 10) return c;
143	    return null;
144	  }
145	
146	  /** 入队发送（P1.3 合包：不再直接 ws.send；flushOutbox 统一拼发） */
147	  send(c: RoomClient, frame: Uint8Array, prio = 0) {
148	    if (c.ws.readyState !== WebSocket.OPEN) return;
149	    const b = c.ws.bufferedAmount;
150	    if (b > c.stats.bufferedMax) c.stats.bufferedMax = b;
151	    if (b > SEND_BUFFER_LIMIT || (b > LOW_BUFFER_LIMIT && prio >= 1)) {
152	      c.stats.sendDrops++;
153	      if (prio >= 1) c.stats.lowDrops++;
154	      this.roomStats.sendDrops++;
155	      return;
156	    }
157	    c.stats.outBytes += frame.length;
158	    this.roomStats.outBytes += frame.length;
159	    const h = this.roomStats.msgHist.get(frame[2]);
160	    if (h) { h.n++; h.bytes += frame.length; } else this.roomStats.msgHist.set(frame[2], { n: 1, bytes: frame.length });
161	    c.outbox.push(frame);
162	  }
163	
164	  /** 冲洗合包队列：每客户端拼接为尽量少的 WS 消息（FLUSH_SLICE 切片防超 maxPayload） */
165	  flushOutbox() {
166	    for (const c of this.clients) {
167	      const ob = c.outbox;
168	      if (!ob.length) continue;
169	      c.outbox = [];
170	      if (c.ws.readyState !== WebSocket.OPEN) continue;
171	      let start = 0, size = 0;
172	      for (let i = 0; i < ob.length; i++) {
173	        size += ob[i].length;
174	        if (size < FLUSH_SLICE && i < ob.length - 1) continue;
175	        const total = size;
176	        const joined = new Uint8Array(total);
177	        let off = 0;
178	        for (let k = start; k <= i; k++) { joined.set(ob[k], off); off += ob[k].length; }
179	        c.ws.send(joined);
180	        start = i + 1;
181	        size = 0;
182	      }
183	    }
184	  }
185	
186	  broadcast(frame: Uint8Array, except?: RoomClient, prio = 0) {
187	    for (const c of this.clients) {
188	      if (c === except || c.state < 10) continue;
189	      this.send(c, frame, prio);
190	    }
191	  }
192	
193	  /** 踢出：入队 Kick 后**先冲刷再 close**——close 置 CLOSING 会让后续 send 静默丢弃
194	   *  （P1.3 合包后的竞态：Kick 在 outbox 里未发，close 先行 → 客户端只见断连不见原因） */
195	  private kick(c: RoomClient, reason: string) {
196	    this.send(c, new NetWriter(Msg.Kick).str(reason).finish());
197	    this.flushOutbox();
198	    c.ws.close();
199	  }
200	
201	  /** AOI 定向广播（P1.1）：只发给距 (x,y) 切比雪夫 ≤ radius 的在局客户端。
202	   *  盲端（位置过期，见 aoiBlind）跳过并计数 stalePos。 */
203	  private broadcastAt(x: number, y: number, radius: number, frame: Uint8Array, except?: RoomClient, prio = 0) {
204	    const now = Date.now();
205	    for (const c of this.clients) {
206	      if (c === except || c.state < 10) continue;
207	      if (now - c.lastPosAt > AOI_STALE_MS) { this.roomStats.stalePos++; continue; }
208	      if (Math.abs(c.lastX - x) <= radius && Math.abs(c.lastY - y) <= radius) this.send(c, frame, prio);
209	    }
210	  }
211	
212	  /** 接收端是否"位置未知/过期"（盲端）。
213	   *  盲端语义 = **跳过实体广播**（曾用"全视野兜底"，实测在服务器饱和时形成放大循环：
214	   *  msg13 处理滞后 → 判盲 → 全量灌流 → 更饱和。盲端本就在滞后，停发实体让它先追平，
215	   *  msg13 是 prio=0 小帧必达，位置恢复后自动重新入场）。新进房客户端在首个 msg13 前
216	   *  也走此语义——实体晚一两秒出现，无害。 */
217	  private aoiBlind(c: RoomClient, now: number): boolean {
218	    return now - c.lastPosAt > AOI_STALE_MS;
219	  }
220	
221	  /** 连接建立后首消息（Hello 带 roomCode/hostToken 由路由层校验后调用） */
222	  handle(c: RoomClient, msgId: number, r: NetReader) {
223	    if (c.state < 1 && msgId !== Msg.Hello) return; // S2 状态门禁
224	    c.lastSeen = 0;
225	    switch (msgId) {
226	      case Msg.Hello: {
227	        if (c.state >= 1) { this.kick(c, '重复握手'); return; }
228	        const magic = r.str();
229	        const ver = r.u16();
230	        c.name = r.str();
231	        if (magic !== PROTO_MAGIC || ver !== PROTO_VER) {
232	          this.kick(c, `协议不匹配（期望 ${PROTO_MAGIC} v${PROTO_VER}）`);
233	          return;
234	        }
235	        // 房主判定：URL token（路由层 newClient 传入）优先；无则消息内 token 兜底。
236	        // 无主房（服务器 --world 载入，hostToken=''）：首位进房者为房主（NPC 权威源）
237	        const msgToken = (() => { try { return r.str(); } catch { return ''; } })();
238	        const token = c.urlToken || msgToken;
239	        if (!this.hostJoined && ((token && token === this.opts.hostToken) || this.opts.hostToken === '')) {
240	          c.isHost = true;
241	          this.hostJoined = true;
242	        }
243	        // v3 重连：resumedSlot ≥ 0 = 断线复位（同 slot，跳过分配）
244	        let slot = -1;
245	        if (c.resumedSlot >= 0) {
246	          slot = c.resumedSlot;
247	          c.resumedSlot = -1;
248	          this.slotUsed[slot] = true;
249	        } else {
250	          slot = this.allocSlot();
251	          if (slot < 0) { this.kick(c, '房间已满'); return; }
252	        }
253	        c.slot = slot;
254	        c.state = 1;
255	        if (!c.session) c.session = randomUUID();
256	        this.send(c, new NetWriter(Msg.PlayerSlot).u8(c.slot).str(c.session).finish());
257	        return;
258	      }
259	      case Msg.RequestWorldData: {
260	        if (c.slot < 0) return;
261	        c.state = 2;
262	        this.send(c, this.worldDataFrame());
263	        return;
264	      }
265	      case Msg.SpawnTileData: {
266	        if (c.slot < 0) return;
267	        const x = r.i32(), y = r.i32();
268	        this.sendStrips(c, x, y);
269	        this.send(c, new NetWriter(Msg.PlayerSpawn).u8(c.slot).i32(this.world.spawnX).i32(this.world.spawnY).finish());
270	        // 进场：向房间广播 + 向新客户端下发策略与在场玩家
271	        this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(true).str(c.name).finish());
272	        // 加入公告（原版 NetMessage.cs:2931 Lang.mp[19] 广播、排除本人、色 (255,240,20)）
273	        this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(true).finish());
274	        this.sendPolicy(c);
275	        for (const other of this.clients) {
276	          if (other === c || other.state < 10) continue;
277	          this.send(c, new NetWriter(Msg.PlayerActive).u8(other.slot).bool(true).str(other.name).finish());
278	          this.send(c, new NetWriter(Msg.SyncPlayer).u8(other.slot).str(other.appearance).finish());
279	          // 在场玩家物品快照全量下发（msg5；手持/盔甲/挥舞渲染依赖）
280	          const entries: Array<{ playerSlot: number; container: ItemContainer; itemSlot: number; itemId: number; stack: number }> = [];
281	          const bags = [other.items.inv, other.items.armor, other.items.dye] as const;
282	          for (let ci = 0; ci < 3; ci++) {
283	            for (let i = 0; i < bags[ci].length; i++) {
284	              const it = bags[ci][i];
285	              if (it) entries.push({ playerSlot: other.slot, container: ci as ItemContainer, itemSlot: i, itemId: it.id, stack: it.stack });
286	            }
287	          }
288	          if (entries.length) this.send(c, writePlayerItems(entries));
289	        }
290	        c.state = 10;
291	        return;
292	      }
293	      case Msg.SyncPlayer: {
294	        r.u8(); // 覆写权威 slot（防冒用）
295	        c.appearance = r.str().slice(0, 4096);
296	        this.broadcast(new NetWriter(Msg.SyncPlayer).u8(c.slot).str(c.appearance).finish(), c);
297	        return;
298	      }
299	      case Msg.SyncPlayerItem: {
300	        if (c.slot < 0) return;
301	        // msg5 物品/装备（对齐原版 SyncPlayerItem）：值域校验 + 快照累积 + 权威 slot 中继
302	        const raw = readPlayerItems(r);
303	        const valid = raw.filter((e) => {
304	          if (e.container > 2) return false;
305	          if (e.itemSlot >= INV_SYNC_SIZES[e.container]) return false;
306	          if (e.itemId >= ITEM_DEFS.length) return false; // S5 值域
307	          return true;
308	        });
309	        for (const e of valid) {
310	          const arr = e.container === ItemContainer.Slots ? c.items.inv
311	            : e.container === ItemContainer.Armor ? c.items.armor : c.items.dye;
312	          arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: Math.min(e.stack, ITEM_DEFS[e.itemId]?.maxStack ?? 9999) } : null;
313	        }
314	        if (valid.length) {
315	          this.broadcast(writePlayerItems(valid.map((e) => ({ ...e, playerSlot: c.slot }))), c);
316	        }
317	        return;
318	      }
319	      case Msg.PlayerState: {
320	        if (c.state < 10) return;
321	        // v2 布局（对齐原版 msg13）：slot(丢弃防冒用) + ctrlBits + flagBits + selectedItem
322	        // + position(左上) [+velocity 若 flagBits[2]]——原样中继，仅覆写权威 slot
323	        r.u8();
324	        const ctrl = r.u8(), flag = r.u8(), sel = r.u8();
325	        const x = r.f32(), y = r.f32();
326	        let vx = 0, vy = 0;
327	        if (flag & 4) { vx = r.f32(); vy = r.f32(); }
328	        // P1.1 AOI：顺带记录发送端位置（接收端过滤的基准），零额外解析成本
329	        c.lastX = x; c.lastY = y; c.lastPosAt = Date.now();
330	        const f = new NetWriter(Msg.PlayerState);
331	        f.u8(c.slot);
332	        f.u8(ctrl); f.u8(flag); f.u8(sel);
333	        f.f32(x); f.f32(y);
334	        if (flag & 4) { f.f32(vx); f.f32(vy); }
335	        this.broadcastAt(x, y, AOI_PLAYER, f.finish(), c);
336	        return;
337	      }
338	      case Msg.TileBatch: {
339	        if (c.state < 10) return;
340	        const ops = readTileBatch(r);
341	        // 破坏保护（服务端权威）：非房主整包拒绝——原版无此机制，属我们 v3 房间制策略
342	        if (this.opts.protectTiles && !c.isHost) {
343	          // 拒绝并回发权威快照纠正（对齐原版 SendTileSquare 纠正语义，防客户端乐观预测残留）
344	          for (const o of ops.slice(0, 8)) this.send(c, this.correctionFrame(o.x, o.y));
345	          return;
346	        }
347	        this.applyTileOps(ops);
348	        this.broadcast(writeTileBatch(ops), c);
349	        return;
350	      }
351	      case Msg.NetModules: {
352	        const moduleId = r.u16();
353	        if (moduleId === NetModule.Text) {
354	          const text = r.str();
355	          if (!text || text.length > 200) return;
356	          const f = new NetWriter(Msg.NetModules);
357	          f.u16(NetModule.Text);
358	          f.u8(c.slot);
359	          f.str(text);
360	          f.u8(255); f.u8(220); f.u8(120);
361	          this.broadcast(f.finish());
362	        }
363	        return;
364	      }
365	      case Msg.RequestChestOpen: {
366	        if (c.state < 10) return;
367	        // msg31（原版 RequestChestOpen）：按锚点找箱 → 全量下发内容（msg32）。
368	        // 访客本地 chests 为空（msg7 不传），内容唯一权威 = 服务器（存档带入）
369	        const x = r.i32(), y = r.i32();
370	        // 邻域匹配（±1 tile）：客户端点击箱体任意一格都能命中锚点（findChestNear 语义）
371	        const idx = this.world.chests.findIndex((ch) => Math.abs(ch.x - x) <= 1 && Math.abs(ch.y - y) <= 1);
372	        if (idx < 0) return;
373	        this.send(c, this.chestFrame(idx, -1));
374	        return;
375	      }
376	      case Msg.SyncChestItem: {
377	        if (c.state < 10) return;
378	        // msg32 上行（槽位编辑）：protectItems 非房主整包拒绝 + 权威内容回发纠正
379	        const chestIdx = r.u16();
380	        const cx = r.i32(), cy = r.i32();
381	        void cx; void cy;
382	        const n = r.u16();
383	        const slots: Array<{ slot: number; itemId: number; stack: number }> = [];
384	        for (let i = 0; i < n; i++) {
385	          const slot = r.u8(), itemId = r.u16(), stack = r.u16();
386	          if (slot < 10 && itemId < ITEM_DEFS.length) slots.push({ slot, itemId, stack: Math.min(stack, ITEM_DEFS[itemId]?.maxStack ?? 9999) });
387	        }
388	        const chest = this.world.chests[chestIdx];
389	        if (!chest) return;
390	        if (this.opts.protectItems && !c.isHost) {
391	          this.send(c, this.chestFrame(chestIdx, -1)); // 权威纠正
392	          return;
393	        }
394	        for (const s of slots) chest.items[s.slot] = s.itemId ? { id: s.itemId, stack: s.stack } : null;
395	        if (slots.length) this.broadcast(this.chestFrame(chestIdx, slots[0].slot, c), c);
396	        return;
397	      }
398	      case Msg.PlayerLifeMana: {
399	        if (c.state < 10) return;
400	        // msg16（原版 PlayerLifeMana）：客户端权威 HP，服务器中继（覆写权威 slot）
401	        r.u8();
402	        const hp = r.i16(), maxHp = r.i16();
403	        this.broadcast(new NetWriter(Msg.PlayerLifeMana).u8(c.slot).i16(hp).i16(maxHp).finish(), c);
404	        return;
405	      }
406	      case Msg.SyncNPC: {
407	        // msg23：NPC 快照仅权威源（现=房主，见 npcAuthority）发出。C→S 全量格式不变；
408	        // S→C v4 短码格式（每条 1B flags：bit0=含 key 全量 / bit1=boss）+ AOI 逐接收端过滤
409	        if (c.state < 10 || !this.npcAuthority(c)) return;
410	        const n = r.u16();
411	        if (n > 64) return;
412	        type Entry = { netId: number; code: number; key: string; x: number; y: number; vx: number; vy: number; hp: number; maxHp: number; animT: number; boss: boolean };
413	        const entries: Entry[] = [];
414	        for (let i = 0; i < n; i++) {
415	          const netId = r.u32();
416	          const key = r.str();
417	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
418	          const hp = r.i16(), maxHp = r.i16(), animT = r.u16(), flags = r.u8();
419	          // P1.2 短码分配（表满 60000 清表：全房 npcKnown 一并失效，全量兜底自动重建）
420	          let code = this.npcCodes.get(netId);
421	          if (code === undefined) {
422	            if (this.npcCodes.size >= 60000) {
423	              this.npcCodes.clear();
424	              for (const cl of this.clients) cl.npcKnown.clear();
425	            }
426	            this.npcCodeSeq = (this.npcCodeSeq + 1) & 0xffff;
427	            if (this.npcCodeSeq === 0) this.npcCodeSeq = 1;
428	            code = this.npcCodeSeq;
429	            this.npcCodes.set(netId, code);
430	          }
431	          entries.push({ netId, code, key: key.slice(0, 64), x, y, vx, vy, hp, maxHp, animT, boss: !!(flags & 1) });
432	        }
433	        const now = Date.now();
434	        // 逐接收端过滤；全员全量时走快速路径（单帧广播，零重编码——簇拥场景的常态）
435	        const targets: Array<{ rc: RoomClient; picked: Entry[] }> = [];
436	        let allFull = true;
437	        for (const rc of this.clients) {
438	          if (rc === c || rc.state < 10) continue;
439	          if (now - rc.lastAoiPrune > AOI_PRUNE_MS) {
440	            rc.lastAoiPrune = now;
441	            for (const [id, t] of rc.aoiNpc) if (now - t > AOI_PRUNE_MS) rc.aoiNpc.delete(id);
442	            for (const [cd, t] of rc.npcKnown) if (now - t > AOI_PRUNE_MS) rc.npcKnown.delete(cd);
443	          }
444	          if (this.aoiBlind(rc, now)) { this.roomStats.stalePos++; continue; } // 盲端：跳过（见 aoiBlind）
445	          const picked: Entry[] = [];
446	          for (const e of entries) {
447	            const dist = Math.max(Math.abs(rc.lastX - e.x), Math.abs(rc.lastY - e.y));
448	            const wasVisible = rc.aoiNpc.has(e.netId);
449	            if (dist > AOI_ENTITY * AOI_OUT_FACTOR) {
450	              if (wasVisible) rc.aoiNpc.delete(e.netId); // 出滞回外径 → 停发（客户端 300 tick 超时清除傀儡）
451	              continue;
452	            }
453	            if (dist > AOI_ENTITY && !wasVisible) continue; // 内外径滞回带且未可见：不入视野
454	            rc.aoiNpc.set(e.netId, now);
455	            picked.push(e);
456	          }
457	          if (!picked.length) continue;
458	          if (picked.length < entries.length) allFull = false;
459	          targets.push({ rc, picked });
460	        }
461	        if (!targets.length) return;
462	        if (allFull) {
463	          // 快速路径：每个目标都收全量条目——但短码标记仍按接收端（known 与否），仅当
464	          // 全员都已知全部 code 时帧内容才一致，此时单帧广播
465	          let allKnown = true;
466	          for (const t of targets) {
467	            for (const e of t.picked) {
468	              if (!t.rc.npcKnown.has(e.code)) { allKnown = false; break; }
469	            }
470	            if (!allKnown) break;
471	          }
472	          if (allKnown) {
473	            const f = new NetWriter(Msg.SyncNPC);
474	            f.u16(entries.length);
475	            for (const e of entries) {
476	              const boss = e.boss ? 2 : 0;
477	              f.u8(boss); f.u16(e.code);
478	              f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
479	              f.i16(e.hp); f.i16(e.maxHp); f.u16(e.animT);
480	              for (const t of targets) t.rc.npcKnown.set(e.code, now);
481	            }
482	            for (const t of targets) this.send(t.rc, f.finish(), 1);
483	            return;
484	          }
485	        }
486	        for (const { rc, picked } of targets) {
487	          const out = new NetWriter(Msg.SyncNPC);
488	          out.u16(picked.length);
489	          for (const e of picked) {
490	            const known = rc.npcKnown.has(e.code);
491	            out.u8((known ? 0 : 1) | (e.boss ? 2 : 0));
492	            if (known) out.u16(e.code);
493	            else { out.u32(e.netId); out.u16(e.code); out.str(e.key); }
494	            rc.npcKnown.set(e.code, now);
495	            out.f32(e.x); out.f32(e.y); out.f32(e.vx); out.f32(e.vy);
496	            out.i16(e.hp); out.i16(e.maxHp); out.u16(e.animT);
497	          }
498	          this.send(rc, out.finish(), 1); // prio=1：背压 1-4MB 水位先丢
499	        }
500	        return;
501	      }
502	      case Msg.SyncItem: {
503	        if (c.state < 10) return;
504	        // msg21：掉落物 spawn/take/despawn 中继（netId 已含拥有者 slot 前缀）
505	        const netId = r.u32();
506	        const op = r.u8();
507	        const f = new NetWriter(Msg.SyncItem);
508	        f.u32(netId); f.u8(op);
509	        if (op === 0) {
510	          const key = r.str();
511	          const stack = r.u16();
512	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
513	          if (!key || key.length > 64 || stack === 0) return;
514	          f.str(key); f.u16(stack);
515	          f.f32(x); f.f32(y); f.f32(vx); f.f32(vy);
516	        } else if (op > 2) return;
517	        this.broadcast(f.finish(), c);
518	        return;
519	      }
520	      case Msg.SyncProjectile: {
521	        if (c.state < 10) return;
522	        // msg27：弹幕快照双向中继（各自弹幕互播）+ P1.1 AOI 滞回过滤；kind>4 整包丢弃防脏流
523	        const n = r.u16();
524	        if (n > 64) return;
525	        type PEntry = { netId: number; kind: number; tag: string; dmg: number; aux: number; x: number; y: number; vx: number; vy: number };
526	        const entries: PEntry[] = [];
527	        for (let i = 0; i < n; i++) {
528	          const netId = r.u32();
529	          const kind = r.u8();
530	          const tag = r.str();
531	          const dmg = r.i16(), aux = r.i16();
532	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
533	          if (kind > 4) return;
534	          entries.push({ netId, kind, tag: tag.slice(0, 32), dmg, aux, x, y, vx, vy });
535	        }
536	        const now = Date.now();
537	        // 逐接收端过滤 + 全员全量快速路径（msg27 无短码，全量时帧内容一致 → 单帧广播零重编码）
538	        const targets: Array<{ rc: RoomClient; picked: PEntry[] }> = [];
539	        let allFull = true;
540	        for (const rc of this.clients) {
541	          if (rc === c || rc.state < 10) continue;
542	          if (now - rc.lastAoiPrune > AOI_PRUNE_MS) {
543	            rc.lastAoiPrune = now;
544	            for (const [id, t] of rc.aoiProj) if (now - t > AOI_PRUNE_MS) rc.aoiProj.delete(id);
545	          }
546	          if (this.aoiBlind(rc, now)) { this.roomStats.stalePos++; continue; } // 盲端：跳过
547	          const picked: PEntry[] = [];
548	          for (const e of entries) {
549	            const dist = Math.max(Math.abs(rc.lastX - e.x), Math.abs(rc.lastY - e.y));
550	            const wasVisible = rc.aoiProj.has(e.netId);
551	            if (dist > AOI_ENTITY * AOI_OUT_FACTOR) {
552	              if (wasVisible) rc.aoiProj.delete(e.netId);
553	              continue;
554	            }
555	            if (dist > AOI_ENTITY && !wasVisible) continue;
556	            rc.aoiProj.set(e.netId, now);
557	            picked.push(e);
558	          }
559	          if (!picked.length) continue;
560	          if (picked.length < entries.length) allFull = false;
561	          targets.push({ rc, picked });
562	        }
563	        if (!targets.length) return;
564	        if (allFull) {
565	          const f = new NetWriter(Msg.SyncProjectile);
566	          f.u16(entries.length);
567	          for (const e of entries) {
568	            f.u32(e.netId); f.u8(e.kind); f.str(e.tag);
569	            f.i16(e.dmg); f.i16(e.aux);
570	            f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
571	          }
572	          const frame = f.finish();
573	          for (const t of targets) this.send(t.rc, frame, 1);
574	          return;
575	        }
576	        for (const { rc, picked } of targets) {
577	          const f = new NetWriter(Msg.SyncProjectile);
578	          f.u16(picked.length);
579	          for (const e of picked) {
580	            f.u32(e.netId); f.u8(e.kind); f.str(e.tag);
581	            f.i16(e.dmg); f.i16(e.aux);
582	            f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
583	          }
584	          this.send(rc, f.finish(), 1);
585	        }
586	        return;
587	      }
588	      case Msg.StrikeNPC: {
589	        if (c.state < 10) return;
590	        // msg42：访客打击 → 定向转发权威结算端（strikeTarget）；dmg 钳 9999 防刷
591	        const netId = r.u32();
592	        const dmg = r.i16();
593	        const kbx = r.f32(), kby = r.f32();
594	        const target = this.strikeTarget();
595	        if (target) {
596	          this.send(target, new NetWriter(Msg.StrikeNPC).u32(netId).i16(Math.max(-32768, Math.min(9999, dmg))).f32(kbx).f32(kby).finish());
597	        }
598	        return;
599	      }
600	      case Msg.Ping: {
601	        const ts = r.f64();
602	        this.send(c, new NetWriter(Msg.Ping).f64(ts).finish());
603	        return;
604	      }
605	      default:
606	        return;
607	    }
608	  }
609	
610	  /** 房间策略下发（RoomPolicy）：客户端据此门禁 UI。v4 尾部追加 u16 maxPlayers */
611	  sendPolicy(c: RoomClient) {
612	    this.send(c, new NetWriter(Msg.RoomPolicy)
613	      .str(this.opts.code)
614	      .str(this.opts.name)
615	      .bool(c.isHost)
616	      .bool(this.opts.protectTiles)
617	      .bool(this.opts.protectItems)
618	      .u16(this.opts.maxPlayers)
619	      .finish());
620	  }
621	
622	  /** 箱子内容帧（msg32）。full=-1 全量下发；否则只带变更槽（最小帧）。
623	   *  广播方向除编辑者本人——编辑者本地已生效（乐观 UI） */
624	  chestFrame(chestIdx: number, full: number, except?: RoomClient): Uint8Array {
625	    const chest = this.world.chests[chestIdx];
626	    const w = new NetWriter(Msg.SyncChestItem);
627	    w.u16(chestIdx);
628	    w.i32(chest.x); w.i32(chest.y);
629	    const from = full === -1 ? 0 : full;
630	    const to = full === -1 ? chest.items.length : from + 1;
631	    w.u16(to - from);
632	    for (let i = from; i < to; i++) {
633	      const it = chest.items[i];
634	      w.u8(i);
635	      w.u16(it?.id ?? 0);
636	      w.u16(it?.stack ?? 0);
637	    }
638	    void except;
639	    return w.finish();
640	  }
641	
642	  /** 权威 tile 快照纠正（单格） */
643	  private correctionFrame(x: number, y: number): Uint8Array {
644	    const ops: TileOp[] = [];
645	    if (x >= 0 && y >= 0 && x < this.st.w && y < this.st.h) {
646	      const i = this.st.idx(x, y);
647	      ops.push({ a: TileOpAction.SetTile, x, y, v: this.st.type[i], fx: this.st.frameX[i], fy: this.st.frameY[i] });
648	    }
649	    return writeTileBatch(ops);
650	  }
651	
652	  disconnect(c: RoomClient) {
653	    this.clients.delete(c);
654	    if (c.slot >= 0) {
655	      // v3 重连：在局玩家断开 → session 保留 60s，slot 占位防新人顶号；过期释放
656	      if (c.state >= 10 && c.session) {
657	        this.sessions.set(c.session, {
658	          slot: c.slot, name: c.name, appearance: c.appearance,
659	          until: Date.now() + 60_000,
660	        });
661	        const sess = c.session;
662	        const slot = c.slot;
663	        setTimeout(() => {
664	          // 已被 resumeSession 消费（重连成功）则不再动；超时未归 → 释放占位
665	          if (!this.sessions.has(sess)) return;
666	          this.sessions.delete(sess);
667	          this.slotUsed[slot] = false;
668	        }, 61_000).unref?.();
669	      } else {
670	        this.slotUsed[c.slot] = false;
671	      }
672	      this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(false).str('').finish());
673	      // 离开公告（原版 NetMessage.cs:2950-2954：先广播 14 再 Lang.mp[20]，含强制退出/掉线）
674	      this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(false).finish());
675	    }
676	    if (c.isHost) this.hostJoined = false;
677	  }
678	
679	  /** 断线重连识别（index.ts 从 URL ?session= 注入）：命中 → 复位 slot/身份，Hello 跳过分配 */
680	  resumeSession(c: RoomClient, session: string): boolean {
681	    const s = this.sessions.get(session);
682	    if (!s || s.until <= Date.now()) return false;
683	    this.sessions.delete(session);
684	    c.resumedSlot = s.slot;
685	    c.name = s.name;
686	    c.appearance = s.appearance;
687	    c.session = session;
688	    return true;
689	  }
690	
691	  // ---- 世界数据帧（msg7）：对齐 v1 字段集 ----
692	  worldDataFrame(): Uint8Array {
693	    const w = new NetWriter(Msg.WorldData);
694	    w.f64(this.world.clock.timeOfDay);
695	    w.u32(this.world.clock.dayCount);
696	    w.u16(this.st.w); w.u16(this.st.h);
697	    w.i32(this.world.spawnX); w.i32(this.world.spawnY);
698	    w.f32(this.world.groundLevel); w.f32(this.world.rockLevel); w.f32(this.world.lavaLine);
699	    w.i32(this.world.seed);
700	    w.str(this.world.name);
701	    w.bool(this.world.crimson);
702	    w.i32(this.world.dungeonX); w.i32(this.world.dungeonY); w.i32(this.world.jungleX);
703	    const keys = Object.keys(this.world.flags);
704	    w.u16(keys.length);
705	    for (const k of keys) { w.str(k); w.bool(!!this.world.flags[k]); }
706	    return w.finish();
707	  }
708	
709	  // ---- section 流式（出生点 5×5 条带，strip 粒度兴趣管理） ----
710	  sendStrips(c: RoomClient, cx: number, cy: number) {
711	    const st = this.st;
712	    const strips: Array<{ x0: number; y0: number }> = [];
713	    const sx = Math.floor(cx / STRIP_W), sy = Math.floor(cy / STRIP_H);
714	    for (let dy = -2; dy <= 2; dy++) {
715	      for (let dx = -2; dx <= 2; dx++) {
716	        const x0 = (sx + dx) * STRIP_W, y0 = (sy + dy) * STRIP_H;
717	        if (x0 >= 0 && y0 >= 0 && x0 < st.w && y0 < st.h) strips.push({ x0, y0 });
718	      }
719	    }
720	    const fresh = strips.filter((s) => !c.sentStrips.has(`${s.x0},${s.y0}`));
721	    this.send(c, new NetWriter(Msg.StatusText).u16(fresh.length).finish());
722	    for (const s of fresh) {
723	      c.sentStrips.add(`${s.x0},${s.y0}`);
724	      // P2.1 section 编码缓存：命中直发（LRU 提到队尾）；miss 编码入缓存
725	      const key = `${s.x0},${s.y0}`;
726	      let frame = this.stripCache.get(key);
727	      if (frame) {
728	        this.stripCache.delete(key);
729	        this.stripCache.set(key, frame);
730	        this.roomStats.stripHit++;
731	      } else {
732	        frame = encodeStrip(st, { x0: s.x0, y0: s.y0, w: Math.min(STRIP_W, st.w - s.x0), h: Math.min(STRIP_H, st.h - s.y0) });
733	        this.stripCache.set(key, frame);
734	        if (this.stripCache.size > 512) {
735	          this.stripCache.delete(this.stripCache.keys().next().value as string); // 淘汰最旧
736	        }
737	        this.roomStats.stripMiss++;
738	      }
739	      this.send(c, frame);
740	    }
741	  }
742	
743	  applyTileOps(ops: TileOp[]) {
744	    const st = this.st;
745	    for (const o of ops) {
746	      if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
747	      // S5 值域校验
748	      if (o.a === TileOpAction.SetTile && o.v >= TILE_DEFS.length) continue;
749	      if (o.a === TileOpAction.SetWall && o.v > 366) continue;
750	      if (o.a === TileOpAction.SetSlope && o.v > 4) continue;
751	      // P2.1：任何落格修改都使其所在条带缓存失效（按条带原点归一化）
752	      this.stripCache.delete(`${Math.floor(o.x / STRIP_W) * STRIP_W},${Math.floor(o.y / STRIP_H) * STRIP_H}`);
753	      this.roomStats.tileOps++;
754	      switch (o.a) {
755	        case TileOpAction.SetTile:
756	          st.setTileSilent(o.x, o.y, o.v, o.fx, o.fy);
757	          // 箱子 tile 被清除/替换 → 同步清除权威 chests 条目（防陈旧条目被 msg31
758	          // 再次开出 = 物品复制；房主 dumpChest 的掉落已走 msg21 广播）
759	          if (o.v !== CHEST_TILE_ID) {
760	            const ci = this.world.chests.findIndex((ch) => Math.abs(ch.x - o.x) <= 1 && Math.abs(ch.y - o.y) <= 1);
761	            if (ci >= 0) this.world.chests.splice(ci, 1);
762	          }
763	          break;
764	        case TileOpAction.SetWall: st.setWallSilent(o.x, o.y, o.v); break;
765	        case TileOpAction.SetHalfBrick: st.half[st.idx(o.x, o.y)] = o.v ? 1 : 0; break;
766	        case TileOpAction.SetSlope: st.slope[st.idx(o.x, o.y)] = o.v; break;
767	        case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
768	        case TileOpAction.SetWire: st.setWireSilent(o.x, o.y, o.v); break;
769	      }
770	    }
771	  }
772	
773	  newClient(ws: WebSocket, urlToken = ''): RoomClient {
774	    const c: RoomClient = {
775	      ws, parser: new FrameParser(), slot: -1, state: 0, name: '?',
776	      appearance: '{}', lastSeen: 0, isHost: false, sentStrips: new Set(),
777	      session: '', resumedSlot: -1,
778	      lastX: -1e9, lastY: -1e9, lastPosAt: 0,
779	      aoiNpc: new Map(), aoiProj: new Map(), npcKnown: new Map(), lastAoiPrune: 0,
780	      outbox: [],
781	      stats: { inBytes: 0, outBytes: 0, bufferedMax: 0, sendDrops: 0, lowDrops: 0 },
782	      items: {
783	        inv: Array(INV_SYNC_SIZES[0]).fill(null),
784	        armor: Array(INV_SYNC_SIZES[1]).fill(null),
785	        dye: Array(INV_SYNC_SIZES[2]).fill(null),
786	      },
787	    };
788	    if (urlToken) c.urlToken = urlToken;
789	    this.clients.add(c);
790	    return c;
791	  }
792	}
793	

```


---

## 🤖 Assistant · 2026-08-12T04:18:42.120Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the remaining files: stats.ts, persist.ts, and the protocol.ts (relevant sections, particularly msg23 encode/decode).
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:18:42.255Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/stats.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:42.355Z

**📎 ToolResult**

```
1	// /stats 观测聚合(P0.1):每房/每客户端计数由 Room 维护,本模块负责
2	// 1s 采样(outBps)与 GET /stats 快照序列化。设计文档 multiplayer-design.md §6.5。
3	import type { Room } from './room.ts';
4	
5	/** 全局+逐房 /stats 快照(lobby HTTP 直接 JSON.stringify) */
6	export function statsSnapshot(rooms: Iterable<Room>): Record<string, unknown> {
7	  let totalOnline = 0, totalClients = 0, totalOutBps = 0, totalSendDrops = 0;
8	  const roomList = [];
9	  for (const room of rooms) {
10	    const rs = room.roomStats;
11	    const clients = [];
12	    for (const c of room.clients) {
13	      clients.push({
14	        slot: c.slot, name: c.name, state: c.state, isHost: c.isHost,
15	        inKb: +(c.stats.inBytes / 1024).toFixed(1), outKb: +(c.stats.outBytes / 1024).toFixed(1),
16	        bufferedKb: +(c.stats.bufferedMax / 1024).toFixed(1),
17	        sendDrops: c.stats.sendDrops, lowDrops: c.stats.lowDrops,
18	      });
19	    }
20	    totalOnline += room.onlineCount;
21	    totalClients += room.clients.size;
22	    totalOutBps += rs.outBps;
23	    totalSendDrops += rs.sendDrops;
24	    roomList.push({
25	      code: room.opts.code, name: room.opts.name, public: room.opts.publicRoom,
26	      online: room.onlineCount, maxPlayers: room.opts.maxPlayers,
27	      w: room.world.w, h: room.world.h,
28	      outKbS: +(rs.outBps / 1024).toFixed(2),
29	      outBytesTotal: rs.outBytes, sendDrops: rs.sendDrops, stalePos: rs.stalePos,
30	      stripHit: rs.stripHit, stripMiss: rs.stripMiss,
31	      topMsgs: topMsgs(rs, 5),
32	      clients,
33	    });
34	  }
35	  return {
36	    ok: true, ts: Date.now(),
37	    total: { rooms: roomList.length, online: totalOnline, clients: totalClients, outKbS: +(totalOutBps / 1024).toFixed(2), sendDrops: totalSendDrops },
38	    rooms: roomList,
39	  };
40	}
41	
42	/** msgId → {n, bytes} 直方图取前 K */
43	function topMsgs(rs: Room['roomStats'], k: number): Array<{ msg: number; n: number; kb: number }> {
44	  return [...rs.msgHist.entries()]
45	    .map(([msg, v]) => ({ msg, n: v.n, kb: +(v.bytes / 1024).toFixed(2) }))
46	    .sort((a, b) => b.kb - a.kb)
47	    .slice(0, k);
48	}
49	
50	/** 1s 采样循环:差分 roomStats.outBytes → outBps。定时器 unref(不阻止进程退出)。
51	 *  传 getter 而非数组快照——启动后才建的房也要被采样 */
52	export function startBpsSampler(getRooms: () => Iterable<Room>): ReturnType<typeof setInterval> {
53	  const last = new Map<Room, number>();
54	  const timer = setInterval(() => {
55	    const now = Date.now();
56	    for (const room of getRooms()) {
57	      const rs = room.roomStats;
58	      const prev = last.get(room);
59	      if (prev === undefined) { last.set(room, rs.outBytes); continue; }
60	      rs.outBps = Math.max(0, (rs.outBytes - prev) / Math.max(0.001, (now - rs.lastSampleAt) / 1000));
61	      rs.lastSampleAt = now;
62	      last.set(room, rs.outBytes);
63	    }
64	    // 清理已摘除房间的差分基准（防 Map 泄漏）
65	    const alive = new Set(getRooms() as Iterable<Room>);
66	    for (const room of last.keys()) if (!alive.has(room)) last.delete(room);
67	  }, 1000);
68	  timer.unref?.();
69	  return timer;
70	}
71	

```


---

## 🤖 Assistant · 2026-08-12T04:18:42.380Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/persist.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:42.476Z

**📎 ToolResult**

```
1	// 服务器世界持久化（P3.1，docs/multiplayer-design.md §3.3）：
2	// 定时 auto-save + SIGTERM/SIGINT 落盘后退出 + --world 启动载入建常驻房。
3	// 语义边界：服务器档只保世界（tile/箱子/clock/flags/天气），不含玩家（无 SSC）——
4	// 房主物品栏权威在房主本地存档。
5	import fs from 'node:fs';
6	import path from 'node:path';
7	import type { Room } from './room.ts';
8	import { saveWorldOnly } from '../../game/src/save/SaveFile.ts';
9	
10	export interface PersistResult { saved: number; skipped: number; }
11	
12	/** 全部房间落盘：worlds/room-<code>.json（每房单文件覆盖写，原子 tmp+rename）。
13	 *  跳过条件：无人在局且自上次保存后无 tile 修改（空房不产生写放大）。 */
14	export function saveRooms(rooms: Iterable<Room>, worldsDir: string): PersistResult {
15	  let saved = 0, skipped = 0;
16	  for (const room of rooms) {
17	    if (room.closed) continue;
18	    if (room.onlineCount === 0 && room.roomStats.tileOps === room.lastSavedTileOps) { skipped++; continue; }
19	    try {
20	      fs.mkdirSync(worldsDir, { recursive: true });
21	      const file = path.join(worldsDir, `room-${room.opts.code}.json`);
22	      const tmp = `${file}.tmp`;
23	      fs.writeFileSync(tmp, saveWorldOnly(room.world), 'utf8');
24	      fs.renameSync(tmp, file);
25	      room.lastSavedTileOps = room.roomStats.tileOps;
26	      saved++;
27	    } catch (e) {
28	      console.error(`[persist] 房间 ${room.opts.code} 保存失败:`, (e as Error).message);
29	    }
30	  }
31	  return { saved, skipped };
32	}
33	
34	/** 启动载入：--world <path> → 常驻房世界（hostToken='' = 无主房，首位进房者为房主） */
35	export function loadWorldFile(file: string): string {
36	  return fs.readFileSync(file, 'utf8');
37	}
38	

```


---

## 🤖 Assistant · 2026-08-12T04:18:44.291Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the protocol.ts file — it's probably huge. Let me search for the relevant parts: msg23 encode/decode (SyncNPC), Msg enum, RoomPolicy, NetWriter/NetReader, FrameParser, encodeStrip, readTileBatch, writeTileBatch.

Let me grep for the specific functions.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:18:45.000Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"SyncNPC\\|RoomPolicy\\|eflags\\|case 23\\|case 27\\|case 13\\|case Msg\\.\" game/src/net/protocol.ts | head -80",
 "description": "Find msg23/RoomPolicy handling in protocol.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:45.349Z

**📎 ToolResult**

```
10: *  v4：msg23 S→C 短码格式（key 每次全量→codeId 短码+按需全量）+ RoomPolicy 尾部 u16 maxPlayers。
43:  SyncNPC = 23,        // C→S（房主上行）：{u16 count, [u32 netId, str key, f32 x,y,vx,vy,
45:                       // S→C（v4 短码+AOI 逐端过滤）：{u16 count, [u8 eflags, ...,
46:                       //    eflags.bit0=含 key 全量(u32 netId + u16 codeId + str key)
59:  RoomPolicy = 200,   // S→C {roomCode, roomName, isHost, protectTiles, protectItems, u16 maxPlayers(v4)}

```


---

## 🤖 Assistant · 2026-08-12T04:18:45.469Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && wc -l game/src/net/protocol.ts server/src/*.ts && ls server/src server/tests 2>/dev/null",
 "description": "Check file sizes and server layout"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:45.647Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
     361 game/src/net/protocol.ts
     326 server/src/index.ts
      37 server/src/persist.ts
     792 server/src/room.ts
      70 server/src/stats.ts
    1586 total
server/src:
index.ts
persist.ts
room.ts
stats.ts

```


---

## 🤖 Assistant · 2026-08-12T04:18:47.990Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
protocol.ts is only 361 lines. Let me read the whole thing. Also, the client-side decoding of msg23 might be in game/src/net/ somewhere. Let me read protocol.ts fully first, then find the client decoder.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:18:48.096Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/protocol.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:48.316Z

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
9	 *  v3：实体同步族（msg16/21/23/27/42）+ 箱子权威（msg31/32）+ sessionToken 重连
10	 *  v4：msg23 S→C 短码格式（key 每次全量→codeId 短码+按需全量）+ RoomPolicy 尾部 u16 maxPlayers。
11	 *      server 与 game 同仓库同时发布，不做 v3 向后兼容 */
12	export const PROTO_VER = 4;
13	
14	/** 消息 ID（v1 实现范围；编号对齐原版 MessageID.cs） */
15	export const enum Msg {
16	  Hello = 1,          // C→S {magic, protoVer, name, hostToken 兜底}
17	  Kick = 2,           // S→C {reason}（原版 Kick/Disconnect 同号）
18	  PlayerSlot = 3,     // S→C {slot, sessionToken}（原版同号 PlayerInfo=3：名字/外观在原版
19	                      //   走此包，我们拆到 Hello+msg4——字段分布简化，ID 保留；
20	                      //   sessionToken 为重连凭据）
21	  SyncPlayer = 4,     // 双向 {slot, appearanceJson}
22	  SyncPlayerItem = 5, // C→S→广播（v2 对齐原版 msg5 SyncPlayerItem 语义，批量变体）：
23	                      //   {u8 count, entries[{u8 playerSlot(服务端覆写), u8 container,
24	                      //    u8 itemSlot, u16 itemId(0=空), u16 stack}]}
25	                      //   container: 0=slots[0..57] 1=armor[0..19] 2=dye[0..9]
26	  RequestWorldData = 6, // C→S {}
27	  WorldData = 7,      // S→C {时间/尺寸/出生点/层线/flags/seed/name}
28	  SpawnTileData = 8,  // C→S {x, y}（客户端请求出生点周围 section）
29	  StatusText = 9,     // S→C {count}（将发的 strip 数，进度条）
30	  TileSection = 10,   // S→C {x0,y0,w,h, rleBytes}（200×20 条带）
31	  PlayerSpawn = 12,   // S→C {slot, x, y}（进房落点确认）
32	  PlayerState = 13,   // C→S→广播（v2 对齐原版 msg13）：{u8 slot, u8 ctrlBits, u8 flagBits,
33	                      //   u8 selectedItem, f32 x, f32 y, [f32 vx, f32 vy 若 flagBits[2]]}
34	                      //   ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction
35	                      //   flagBits: [2]hasVelocity [6]ghost(死亡)。position=碰撞盒左上（原版语义）
36	  PlayerActive = 14,  // S→C 广播 {slot, active, name}
37	  TileBatch = 17,     // C→S→广播 {count, ops[]}（tile 操作批量，对齐 msg17 语义）
38	  SetTime = 18,       // S→C {timeOfDay, dayCount}
39	  // ---- v3 实体同步（房主权威 + 服务器中继；ID 对齐原版 MessageID.cs） ----
40	  PlayerLifeMana = 16, // 双向 {u8 slot, i16 hp, i16 maxHp}（原版同号：客户端权威 HP，服务器中继）
41	  SyncItem = 21,       // 房主→广播 {u32 netId, u8 op(0=spawn/1=take/2=despawn), str key,
42	                       //   u16 stack, f32 x,y,vx,vy}（原版同号 SyncItem）
43	  SyncNPC = 23,        // C→S（房主上行）：{u16 count, [u32 netId, str key, f32 x,y,vx,vy,
44	                       //    i16 hp, i16 maxHp, u16 animT, u8 flags(bit0=boss)]}
45	                       // S→C（v4 短码+AOI 逐端过滤）：{u16 count, [u8 eflags, ...,
46	                       //    eflags.bit0=含 key 全量(u32 netId + u16 codeId + str key)
47	                       //             bit1=boss；否则仅 u16 codeId（客户端 codeId→netId/key 表）]}
48	  SyncProjectile = 27, // 双向（各自的弹幕互播，原版同号）：
49	                       //   {u16 count, [u32 netId, str key, f32 x,y,vx,vy, f32 rot]}
50	  RequestChestOpen = 31, // C→S {i32 x, i32 y}（箱子锚点；原版同号）
51	  SyncChestItem = 32,  // S→C 下发 / C→S 槽位编辑（原版同号 SyncChestItem）：
52	                       //   {u16 chestIdx, i32 x, i32 y, u16 count, [u8 slot, u16 itemId, u16 stack]}
53	  StrikeNPC = 42,      // 访客→房主（服务器定向转发）{u32 netId, i16 dmg, f32 kbx, f32 kby}
54	                       //   （原版 42=Unknown42：旧 StrikeNPC 槽位；注释曾误写 crit/kbDir/srcX/srcY——
55	                       //    实际线格式自 v3 起即为 dmg+击退两分量，2026-08 校正）
56	  NetModules = 82,    // 双向 {moduleId, ...}（module1=聊天 module2=ping）
57	  Ping = 154,         // 简化独立心跳（module2 并存预留）
58	  // ---- v3 房间制扩展（docs/multiplayer-design.md §房间） ----
59	  RoomPolicy = 200,   // S→C {roomCode, roomName, isHost, protectTiles, protectItems, u16 maxPlayers(v4)}
60	}
61	
62	/** NetModule 表（0-2 对齐原版 NetworkInitializer.cs 注册序：Liquid/Text/Ping；
63	 *  JoinLeave=3 与原版 NetAmbienceModule 撞号——本协议双端自洽，无互操作需求） */
64	export const enum NetModule {
65	  Liquid = 0,   // 预留（v1 液体客户端本地）
66	  Text = 1,     // 聊天 {authorSlot, text, r, g, b}（author=255 无前缀，对齐原版 255=服务器）
67	  PingModule = 2, // 预留
68	  JoinLeave = 3,  // S→C 系统 {slot, joined}——加入/离开公告（原版 Lang.mp[19]/[20]，服务器广播）
69	}
70	
71	// ================= Writer（小端，定宽；字符串 = u16 长度 + UTF-8） =================
72	
73	export class NetWriter {
74	  private buf = new Uint8Array(256);
75	  private len = 0;
76	  private dv: DataView;
77	
78	  constructor(private readonly msgId: number) {
79	    // 预留 [u16 len][u8 msgId]
80	    this.len = 3;
81	    this.dv = new DataView(this.buf.buffer);
82	  }
83	
84	  private grow(need: number) {
85	    if (this.len + need <= this.buf.length) return;
86	    let cap = this.buf.length;
87	    while (cap < this.len + need) cap *= 2;
88	    const nb = new Uint8Array(cap);
89	    nb.set(this.buf.subarray(0, this.len));
90	    this.buf = nb;
91	    this.dv = new DataView(this.buf.buffer);
92	  }
93	
94	  u8(v: number): this { this.grow(1); this.buf[this.len++] = v & 255; return this; }
95	  i8(v: number): this { return this.u8(v < 0 ? v + 256 : v); }
96	  u16(v: number): this { this.grow(2); this.dv.setUint16(this.len, v, true); this.len += 2; return this; }
97	  i16(v: number): this { this.grow(2); this.dv.setInt16(this.len, v, true); this.len += 2; return this; }
98	  u32(v: number): this { this.grow(4); this.dv.setUint32(this.len, v >>> 0, true); this.len += 4; return this; }
99	  i32(v: number): this { this.grow(4); this.dv.setInt32(this.len, v, true); this.len += 4; return this; }
100	  f32(v: number): this { this.grow(4); this.dv.setFloat32(this.len, v, true); this.len += 4; return this; }
101	  f64(v: number): this { this.grow(8); this.dv.setFloat64(this.len, v, true); this.len += 8; return this; }
102	  bool(v: boolean): this { return this.u8(v ? 1 : 0); }
103	  bytes(b: Uint8Array): this { this.grow(b.length); this.buf.set(b, this.len); this.len += b.length; return this; }
104	  str(s: string): this {
105	    const b = new TextEncoder().encode(s);
106	    this.u16(b.length);
107	    return this.bytes(b);
108	  }
109	
110	  /** 回填长度前缀并返回完整帧（含 [u16 len][u8 id]）。finish 后禁止再写入（subarray 视图） */
111	  finish(): Uint8Array {
112	    // Q3 修复：守卫含头总长（此前 len-3 在 65533..65535 区间漏检 → setUint16 回绕 → 接收端脏流）
113	    if (this.len > 65535) throw new Error(`net: 包超限 ${this.len}`);
114	    this.dv.setUint16(0, this.len, true);
115	    this.buf[2] = this.msgId & 255;
116	    return this.buf.subarray(0, this.len);
117	  }
118	}
119	
120	// ================= Reader =================
121	
122	export class NetReader {
123	  private dv: DataView;
124	  private p = 0;
125	  constructor(private readonly buf: Uint8Array) {
126	    this.dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
127	  }
128	  get pos() { return this.p; }
129	  u8(): number { return this.buf[this.p++]; }
130	  i8(): number { const v = this.buf[this.p++]; return v >= 128 ? v - 256 : v; }
131	  u16(): number { const v = this.dv.getUint16(this.p, true); this.p += 2; return v; }
132	  i16(): number { const v = this.dv.getInt16(this.p, true); this.p += 2; return v; }
133	  u32(): number { const v = this.dv.getUint32(this.p, true); this.p += 4; return v; }
134	  i32(): number { const v = this.dv.getInt32(this.p, true); this.p += 4; return v; }
135	  f32(): number { const v = this.dv.getFloat32(this.p, true); this.p += 4; return v; }
136	  f64(): number { const v = this.dv.getFloat64(this.p, true); this.p += 8; return v; }
137	  bool(): boolean { return this.u8() !== 0; }
138	  bytes(n: number): Uint8Array { const b = this.buf.subarray(this.p, this.p + n); this.p += n; return b; }
139	  str(): string {
140	    const n = this.u16();
141	    return new TextDecoder().decode(this.bytes(n));
142	  }
143	}
144	
145	// ================= 帧流解析（粘包；对齐原版 CheckBytes 语义） =================
146	
147	/** 字节流帧解析器：append 后逐帧回调 {msgId, payloadReader}，自动处理半包。
148	 *  P0.4 增量化：单一缓冲 + 读写偏移（旧版每 drain 把全部 chunk 合并成新数组——
149	 *  4 人房每秒数百次全量拷贝，纯 GC 压力）。残余半包 copyWithin 归位。 */
150	export class FrameParser {
151	  private buf = new Uint8Array(4096);
152	  private len = 0;
153	  private _draining = false;
154	
155	  append(data: Uint8Array) {
156	    if (this._draining) throw new Error('FrameParser: drain 回调内禁止 append（会破坏解析缓冲）');
157	    if (this.len + data.length > this.buf.length) {
158	      let cap = this.buf.length;
159	      while (cap < this.len + data.length) cap *= 2;
160	      const nb = new Uint8Array(cap);
161	      nb.set(this.buf.subarray(0, this.len));
162	      this.buf = nb;
163	    }
164	    // 拷贝入缓冲（ws 回调数据可能被复用）
165	    this.buf.set(data, this.len);
166	    this.len += data.length;
167	  }
168	
169	  /** 解析所有完整帧；返回 false 表示缓冲为空。
170	   *  脏流防护：len 非法时按字节重同步（此前 break 不前进 → 永久失步 + 缓冲无限增长）。
171	   *  缓冲上限：超限重置（半包攻击防御）。P1.3 合包后单条 WS 消息可达 512KB
172	   *  （服务器 FLUSH_SLICE 切片；25 条 strip 拼发），上限须高于切片粒度——
173	   *  2026-08 实踩：沿用 256KB 旧值会把进房 strip 大包整包丢弃 → 世界组装永久卡死 */
174	  private static readonly MAX_BUFFER = 4 * 1024 * 1024;
175	  drain(cb: (msgId: number, r: NetReader) => void): boolean {
176	    if (this._draining) throw new Error('FrameParser: drain 重入');
177	    if (this.len < 3) return this.len > 0;
178	    if (this.len > FrameParser.MAX_BUFFER) { this.len = 0; return false; }
179	    this._draining = true;
180	    let p = 0;
181	    let any = false;
182	    const dv = new DataView(this.buf.buffer, this.buf.byteOffset, this.buf.byteLength);
183	    try {
184	      while (p + 3 <= this.len) {
185	        const len = dv.getUint16(p, true);
186	        if (len < 3 || len > 65535) { p += 1; continue; } // 脏字节：跳过重同步
187	        if (p + len > this.len) break; // 半包
188	        const msgId = this.buf[p + 2];
189	        cb(msgId, new NetReader(this.buf.subarray(p + 3, p + len)));
190	        p += len;
191	        any = true;
192	      }
193	    } finally {
194	      this._draining = false;
195	    }
196	    // 回调同步消费完 subarray 视图后才压缩缓冲（期间禁止 append，见上）
197	    if (p > 0) {
198	      if (p < this.len) this.buf.copyWithin(0, p, this.len);
199	      this.len -= p;
200	    }
201	    return any || this.len > 0;
202	  }
203	}
204	
205	// ================= 玩家物品同步（msg5 SyncPlayerItem 批量变体） =================
206	
207	export const enum ItemContainer {
208	  Slots = 0,  // inv.slots[0..57]
209	  Armor = 1,  // inv.armor[0..19]（0-2 盔甲/3-9 配饰/10-12 时装/13-19 时装配饰）
210	  Dye = 2,    // inv.dye[0..9]
211	}
212	
213	export interface ItemSyncEntry {
214	  container: ItemContainer;
215	  itemSlot: number;
216	  itemId: number;   // 0 = 空
217	  stack: number;
218	}
219	
220	export const INV_SYNC_SIZES = [58, 20, 10];
221	
222	export function writePlayerItems(entries: Array<ItemSyncEntry & { playerSlot: number }>): Uint8Array {
223	  const w = new NetWriter(Msg.SyncPlayerItem);
224	  w.u16(entries.length);
225	  for (const e of entries) {
226	    w.u8(e.playerSlot);
227	    w.u8(e.container);
228	    w.u8(e.itemSlot);
229	    w.u16(e.itemId & 0xffff);
230	    w.u16(e.stack & 0xffff);
231	  }
232	  return w.finish();
233	}
234	
235	export function readPlayerItems(r: NetReader): Array<ItemSyncEntry & { playerSlot: number }> {
236	  const n = r.u16();
237	  const out: Array<ItemSyncEntry & { playerSlot: number }> = [];
238	  for (let i = 0; i < n; i++) {
239	    const playerSlot = r.u8();
240	    const container = r.u8() as ItemContainer;
241	    const itemSlot = r.u8();
242	    const itemId = r.u16();
243	    const stack = r.u16();
244	    out.push({ playerSlot, container, itemSlot, itemId, stack });
245	  }
246	  return out;
247	}
248	
249	// ================= tile 操作批量（msg17，对齐原版单点操作语义的批量变体） =================
250	
251	export const enum TileOpAction {
252	  SetTile = 0,    // v=type, fx, fy
253	  SetWall = 1,    // v=wall
254	  SetHalfBrick = 5,
255	  SetSlope = 6,
256	  SetActuated = 3,
257	  SetWire = 4,    // v=bits
258	}
259	
260	export interface TileOp {
261	  a: TileOpAction;
262	  x: number; y: number;
263	  v: number;
264	  fx: number; fy: number;
265	}
266	
267	export function writeTileBatch(ops: TileOp[]): Uint8Array {
268	  const w = new NetWriter(Msg.TileBatch);
269	  w.u16(ops.length);
270	  for (const o of ops) {
271	    w.u8(o.a);
272	    w.i32(o.x); w.i32(o.y);
273	    w.u16(o.v & 0xffff);
274	    if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
275	  }
276	  return w.finish();
277	}
278	
279	export function readTileBatch(r: NetReader): TileOp[] {
280	  const n = r.u16();
281	  const ops: TileOp[] = [];
282	  for (let i = 0; i < n; i++) {
283	    const a = r.u8() as TileOpAction;
284	    const x = r.i32(), y = r.i32(), v = r.u16();
285	    let fx = 0, fy = 0;
286	    if (a === TileOpAction.SetTile) { fx = r.u16(); fy = r.u16(); }
287	    ops.push({ a, x, y, v, fx, fy });
288	  }
289	  return ops;
290	}
291	
292	// ================= tile strip RLE 编解码（msg10，codecVer=0 裸 RLE） =================
293	// 每 tile 完整状态 = type/flags/frameX/frameY/wall/liquid/liquidType/half/slope/wire
294	// 11B 裸；RLE 按"全状态相同"连续段编码 [u16 count][11B 状态]，地下均质区压缩比极高。
295	// 条带默认 200×20（4400 格，最坏 57KB < 64KB 包上限）。
296	
297	export interface StripRect { x0: number; y0: number; w: number; h: number; }
298	
299	/** 编码一条 strip（读 store 指定矩形） */
300	export function encodeStrip(
301	  st: { w: number; h: number; type: Uint16Array; flags: Uint8Array; frameX: Uint16Array; frameY: Uint16Array;
302	        wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; half: Uint8Array; slope: Uint8Array; wire: Uint8Array },
303	  rect: StripRect,
304	): Uint8Array {
305	  const w = new NetWriter(Msg.TileSection);
306	  w.i32(rect.x0); w.i32(rect.y0); w.u16(rect.w); w.u16(rect.h);
307	  const idx = (x: number, y: number) => y * st.w + x;
308	  let run = 0;
309	  let rType = 0, rFlags = 0, rFx = 0, rFy = 0, rWall = 0, rLiq = 0, rLt = 0, rHalf = 0, rSlope = 0, rWire = 0;
310	  const flushRun = () => {
311	    if (run === 0) return;
312	    w.u16(run);
313	    w.u16(rType); w.u8(rFlags); w.u16(rFx); w.u16(rFy); w.u16(rWall);
314	    w.u8(rLiq); w.u8(rLt); w.u8(rHalf); w.u8(rSlope); w.u8(rWire);
315	    run = 0;
316	  };
317	  for (let y = rect.y0; y < rect.y0 + rect.h; y++) {
318	    for (let x = rect.x0; x < rect.x0 + rect.w; x++) {
319	      const i = idx(x, y);
320	      if (run > 0 && (
321	        st.type[i] !== rType || st.flags[i] !== rFlags || st.frameX[i] !== rFx || st.frameY[i] !== rFy
322	        || st.wall[i] !== rWall || st.liquid[i] !== rLiq || st.liquidType[i] !== rLt
323	        || st.half[i] !== rHalf || st.slope[i] !== rSlope || st.wire[i] !== rWire
324	      )) flushRun();
325	      if (run === 0) {
326	        rType = st.type[i]; rFlags = st.flags[i]; rFx = st.frameX[i]; rFy = st.frameY[i];
327	        rWall = st.wall[i]; rLiq = st.liquid[i]; rLt = st.liquidType[i];
328	        rHalf = st.half[i]; rSlope = st.slope[i]; rWire = st.wire[i];
329	      }
330	      run++;
331	    }
332	  }
333	  flushRun();
334	  return w.finish();
335	}
336	
337	/** 解码一条 strip 直写目标 store（批量路径：绕过事件，调用方负责事后整块标脏） */
338	export function decodeStrip(
339	  st: { w: number; h: number; type: Uint16Array; flags: Uint8Array; frameX: Uint16Array; frameY: Uint16Array;
340	        wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array; half: Uint8Array; slope: Uint8Array; wire: Uint8Array },
341	  r: NetReader,
342	): StripRect | null {
343	  const x0 = r.i32(), y0 = r.i32(), w = r.u16(), h = r.u16();
344	  if (x0 < 0 || y0 < 0 || x0 + w > st.w || y0 + h > st.h) return null;
345	  let written = 0;
346	  while (written < w * h) {
347	    const count = r.u16();
348	    // C2 防死循环：count=0（恶意/损坏数据）或 payload 已尽（截断）→ 终止并返回已写区域
349	    if (count === 0) break;
350	    const type = r.u16(), flags = r.u8(), fx = r.u16(), fy = r.u16(), wall = r.u16();
351	    const liq = r.u8(), lt = r.u8(), half = r.u8(), slope = r.u8(), wire = r.u8();
352	    for (let k = 0; k < count && written < w * h; k++) {
353	      const x = x0 + (written % w), y = y0 + Math.floor(written / w);
354	      const i = y * st.w + x;
355	      st.type[i] = type; st.flags[i] = flags; st.frameX[i] = fx; st.frameY[i] = fy; st.wall[i] = wall;
356	      st.liquid[i] = liq; st.liquidType[i] = lt; st.half[i] = half; st.slope[i] = slope; st.wire[i] = wire;
357	      written++;
358	    }
359	  }
360	  return { x0, y0, w, h };
361	}
362	

```


---

## 🤖 Assistant · 2026-08-12T04:18:48.512Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && ls game/src/net/ && grep -rn \"SyncNPC\" game/src --include=*.ts -l | head"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:48.730Z

**📎 ToolResult**

```
ClientNet.ts
entitySyncHooks.ts
LanDiscovery.ts
protocol.ts
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-12T04:18:50.080Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read ClientNet.ts to check the client-side decoding of msg23 (eflags bit0/bit1) and RoomPolicy (maxPlayers append).
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:18:50.211Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:18:50.472Z

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
84	  /** 打击到达（msg42；房主权威结算） */
85	  onStrike?: (netId: number, rawDmg: number, kbx: number, kby: number) => void;
86	  /** 远端玩家 HP（msg16 中继） */
87	  onHp?: (slot: number, hp: number, maxHp: number) => void;
88	  /** 房间策略到达（进场时；门禁/提示用） */
89	  onPolicy?: (policy: RoomPolicyState) => void;
90	}
91	
92	export class ClientNet {
93	  active = false;
94	  mySlot = -1;
95	  players = new Map<number, RemotePlayerState>();
96	  /** 房间策略（RoomPolicy 到达前 = 自由房默认） */
97	  policy: RoomPolicyState = { roomCode: '', roomName: '', isHost: false, protectTiles: false, protectItems: false, maxPlayers: 255 };
98	
99	  private ws: WebSocket | null = null;
100	  private parser = new FrameParser();
101	  private hooks: ClientNetHooks;
102	  private game: { player: { appearance?: unknown; inv: { slots: Array<{ id: number; stack: number } | null> } } };
103	  private hostToken = '';
104	
105	  /** 组装中的世界（收到 msg7 建骨架，strip 到齐后交给 onWorldReady） */
106	  private pendingWorld: World | null = null;
107	  private pendingStrips = 0;
108	  private pendingStripsTotal = 0;
109	  private worldDelivered = false;
110	  /** 本地 tile 变更上报队列（TileStore.netReporter 收集） */
111	  private tileQueue: TileOp[] = [];
112	  /** msg23 短码表（v4：codeId → {netId, key}；服务器端分配，全量条目重建） */
113	  private npcCodes = new Map<number, { netId: number; key: string }>();
114	  /** msg21 上行合帧暂存（P1.3：netDropSweep 每 4 tick 逐条发 → 攒到 tick 冲洗拼一条 WS 消息） */
115	  private pendingFrames: Uint8Array[] = [];
116	  private lastStateSent = 0;
117	  private lastSentPos = { x: 0, y: 0 };
118	
119	  constructor(
120	    game: ClientNet['game'],
121	    hooks: ClientNetHooks,
122	  ) {
123	    this.game = game;
124	    this.hooks = hooks;
125	  }
126	
127	  private pingTimer: ReturnType<typeof setInterval> | null = null;
128	
129	  connect(url: string, hostToken = '') {
130	    this.url = url;
131	    this.hostToken = hostToken;
132	    this.connect0(url);
133	  }
134	
135	  /** 底层建连（首连/重连共用） */
136	  private connect0(url: string) {
137	    this.active = true;
138	    let ws: WebSocket;
139	    try {
140	      ws = new WebSocket(url);
141	    } catch (e) {
142	      // R12 修复：非法 URL 同步抛异常 → 转为 reject 语义（onKick）而非穿透调用栈
143	      this.active = false;
144	      this.hooks.onKick?.(`地址无效：${(e as Error).message}`);
145	      return;
146	    }
147	    ws.binaryType = 'arraybuffer';
148	    this.ws = ws;
149	    // R9：独立 30s 心跳——暂停/后台（fixedUpdate 停跑）也不再被服务器 120s 看门狗踢
150	    if (!this.pingTimer) {
151	      this.pingTimer = setInterval(() => {
152	        this.send(new NetWriter(Msg.Ping).f64(performance.now()).finish());
153	      }, 30000);
154	    }
155	    ws.onopen = () => {
156	      // Hello（对齐原版 msg1：版本校验）。连接时 Game.player 可能尚未创建（joinNetGame
157	      // 先连后 loadWorld）——外观名走可选链兜底
158	      const p = this.game.player as { appearance?: { name?: string } } | undefined | null;
159	      const name = p?.appearance?.name ?? '玩家';
160	      // 房主令牌：URL 已带 ?token=（路由层 newClient 注入）——消息内再传一份兜底
161	      // （非房主/旧路径传空串，服务器 try/catch 读不到即跳过）
162	      const hello = new NetWriter(Msg.Hello).str(PROTO_MAGIC).u16(PROTO_VER).str(name).str(this.hostToken);
163	      this.send(hello.finish());
164	    };
165	    ws.onmessage = (e) => {
166	      this.parser.append(new Uint8Array(e.data as ArrayBuffer));
167	      this.parser.drain((id, r) => this.handle(id, r));
168	    };
169	    ws.onclose = () => {
170	      if (!this.active || this.userClosed) return;
171	      // v3 断线重连（§8.8）：有 session 凭据 → 2s 间隔自动重试 3 次（同 slot 复位）；
172	      // 耗尽或无凭据 → 按原语义 onKick
173	      if (this.session && this.reconnects < 3) {
174	        this.reconnects++;
175	        this.active = false;
176	        setTimeout(() => {
177	          if (this.userClosed) return;
178	          const sep = this.url.includes('?') ? '&' : '?';
179	          this.connect0(`${this.url}${sep}session=${encodeURIComponent(this.session)}`);
180	        }, 2000);
181	        return;
182	      }
183	      this.active = false;
184	      this.hooks.onKick?.('与服务器断开连接');
185	    };
186	    ws.onerror = () => { /* close 跟上 */ };
187	  }
188	
189	  private url = '';
190	  private session = '';
191	  private reconnects = 0;
192	  private userClosed = false;
193	
194	  private send(frame: Uint8Array) {
195	    if (this.ws?.readyState === WebSocket.OPEN) this.ws.send(frame);
196	  }
197	
198	  /** 请求玩家位置周围的 strip（R3 移动续传：跨条带边界时由 Game 调用） */
199	  requestSection(cx: number, cy: number) {
200	    this.send(new NetWriter(Msg.SpawnTileData).i32(Math.floor(cx)).i32(Math.floor(cy)).finish());
201	  }
202	
203	  disconnect() {
204	    this.userClosed = true;
205	    this.active = false;
206	    if (this.pingTimer) { clearInterval(this.pingTimer); this.pingTimer = null; }
207	    this.ws?.close();
208	    this.ws = null;
209	  }
210	
211	  // ================= 收包分发（对齐原版 MessageBuffer switch） =================
212	
213	  private handle(msgId: number, r: NetReader) {
214	    switch (msgId) {
215	      case Msg.Kick: {
216	        this.hooks.onKick?.(r.str());
217	        this.disconnect();
218	        return;
219	      }
220	      case Msg.PlayerSlot: {
221	        this.mySlot = r.u8();
222	        this.invDumpPending = true; // 物品全量 dump 时机：slot 分配后首 tick
223	        // v3：session 凭据（重连用）；重连场景复位 join 状态以重走世界组装
224	        const sess = (() => { try { return r.str(); } catch { return ''; } })();
225	        if (sess) {
226	          if (this.worldDelivered) {
227	            // 断线重连：世界将重新组装下发（pendingWorld 复位）
228	            this.worldDelivered = false;
229	            this.pendingWorld = null;
230	            this.pendingStrips = 0;
231	          }
232	          this.session = sess;
233	          this.reconnects = 0;
234	        }
235	        // 全量上传自身（对齐原版 msg3 后立刻 SyncPlayer + RequestWorldData）
236	        const p2 = this.game.player as { appearance?: unknown } | undefined | null;
237	        const app = JSON.stringify(p2?.appearance ?? {});
238	        this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(app).finish());
239	        this.send(new NetWriter(Msg.RequestWorldData).finish());
240	        return;
241	      }
242	      case Msg.WorldData: {
243	        this.pendingWorld = this.readWorldData(r);
244	        return;
245	      }
246	      case Msg.StatusText: {
247	        this.pendingStrips = r.u16();
248	        this.pendingStripsTotal = Math.max(1, this.pendingStrips);
249	        // 仅初始组装期上报进度：进世界后 R3 移动续传也会触发 StatusText（fresh=0），
250	        // 无条件回调会把已关闭的全屏进度遮罩重新拉起 → "永久卡在接收世界数据"
251	        if (!this.worldDelivered) this.hooks.onProgress?.('接收世界数据', 0);
252	        return;
253	      }
254	      case Msg.TileSection: {
255	        // R3 修复：初始组装期写入 pendingWorld；运行期（已进世界）晚到的 strip
256	        // 直写 gameWorld 并返回区域（调用方负责整块标脏——见 requestSection 回调）
257	        if (this.pendingWorld) {
258	          decodeStrip(this.pendingWorld.store, r);
259	          if (this.pendingStrips > 0) {
260	            this.pendingStrips--;
261	            // 进度按剩余比例推进（此前恒 0.5 不动）
262	            this.hooks.onProgress?.('接收世界数据', this.pendingStripsTotal > 0 ? 1 - this.pendingStrips / this.pendingStripsTotal : 0.5);
263	          }
264	        } else if (this.gameWorld) {
265	          const rect = decodeStrip(this.gameWorld.store, r);
266	          if (rect && this.hooks.onSectionArrived) this.hooks.onSectionArrived(rect);
267	        }
268	        return;
269	      }
270	      case Msg.PlayerSpawn: {
271	        const slot = r.u8();
272	        const sx = r.i32(), sy = r.i32();
273	        if (slot === this.mySlot && !this.worldDelivered && this.pendingWorld) {
274	          this.worldDelivered = true;
275	          this.pendingWorld.spawnX = sx;
276	          this.pendingWorld.spawnY = sy;
277	          this.hooks.onProgress?.('完成', 1);
278	          this.hooks.onWorldReady(this.pendingWorld);
279	          this.pendingWorld = null;
280	          // R2 修复：进世界后重发外观——连接时 player 可能尚未创建/外观未应用，
281	          // 此刻 Game.player 必然就绪（onWorldReady 已被 loadWorld 消费）
282	          const p3 = this.game.player as { appearance?: unknown } | undefined;
283	          if (p3?.appearance) {
284	            this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p3.appearance)).finish());
285	          }
286	        }
287	        return;
288	      }
289	      case Msg.PlayerActive: {
290	        const slot = r.u8();
291	        const active = r.bool();
292	        const name = r.str();
293	        let p = this.players.get(slot);
294	        if (active) {
295	          if (!p) {
296	            p = {
297	              slot, name, appearance: '{}', x: 0, y: 0, vx: 0, vy: 0,
298	              up: false, down: false, left: false, right: false, jump: false, useItem: false,
299	              facing: 1, selectedItem: 0, dead: false, fresh: false, active: true, lastFresh: 0,
300	            };
301	            this.players.set(slot, p);
302	          }
303	          p.active = true;
304	          p.name = name || p.name;
305	        } else if (p) {
306	          p.active = false;
307	        }
308	        return;
309	      }
310	      case Msg.SyncPlayer: {
311	        const slot = r.u8();
312	        const appearance = r.str();
313	        const p = this.players.get(slot);
314	        if (p) p.appearance = appearance;
315	        return;
316	      }
317	      case Msg.SyncPlayerItem: {
318	        // 远端物品/装备（msg5）：Game 侧拷入 proxy.inv 驱动手持/盔甲/挥舞渲染
319	        const entries = readPlayerItems(r);
320	        this.applyRemoteItems(entries.filter((e) => e.playerSlot !== this.mySlot));
321	        return;
322	      }
323	      case Msg.PlayerState: {
324	        // v2 布局（对齐原版 msg13）：slot + ctrlBits + flagBits + selectedItem + pos [+vel]
325	        const slot = r.u8();
326	        const ctrl = r.u8();
327	        const flag = r.u8();
328	        const sel = r.u8();
329	        const x = r.f32(), y = r.f32();
330	        let vx = 0, vy = 0;
331	        if (flag & 4) { vx = r.f32(); vy = r.f32(); } // flagBits[2] = hasVelocity
332	        let p = this.players.get(slot);
333	        if (!p) {
334	          p = {
335	            slot, name: `玩家${slot}`, appearance: '{}',
336	            x, y, vx: 0, vy: 0,
337	            up: false, down: false, left: false, right: false, jump: false, useItem: false,
338	            facing: ctrl & 64 ? 1 : -1, selectedItem: sel, dead: !!(flag & 64),
339	            fresh: true, active: true, lastFresh: performance.now(),
340	          };
341	          this.players.set(slot, p);
342	        }
343	        p.lastFresh = performance.now();
344	        p.x = x; p.y = y; p.vx = vx; p.vy = vy;
345	        p.up = !!(ctrl & 1); p.down = !!(ctrl & 2);
346	        p.left = !!(ctrl & 4); p.right = !!(ctrl & 8);
347	        p.jump = !!(ctrl & 16); p.useItem = !!(ctrl & 32);
348	        p.facing = ctrl & 64 ? 1 : -1;   // ctrlBits[6] = direction（原版）
349	        p.selectedItem = sel;
350	        p.dead = !!(flag & 64);           // flagBits[6] = ghost
351	        p.fresh = true;                   // Game 侧注入 netOffset 后清零
352	        return;
353	      }
354	      case Msg.TileBatch: {
355	        // 服务器中继的远端操作：应用 + 回环抑制
356	        const ops = readTileBatch(r);
357	        this.applyRemote(ops);
358	        return;
359	      }
360	      case Msg.SetTime: {
361	        // 时间对齐（服务器权威 clock）
362	        if (this.gameWorld) {
363	          const t = r.f64();
364	          const d = r.u32();
365	          if (Math.abs(this.gameWorld.clock.timeOfDay - t) > 0.005) {
366	            this.gameWorld.clock.timeOfDay = t;
367	          }
368	          this.gameWorld.clock.dayCount = d;
369	        }
370	        return;
371	      }
372	      case Msg.NetModules: {
373	        const moduleId = r.u16();
374	        if (moduleId === NetModule.Text) {
375	          const slot = r.u8();
376	          const text = r.str();
377	          const cr = r.u8(), cg = r.u8(), cb = r.u8();
378	          const name = this.players.get(slot)?.name ?? `玩家${slot}`;
379	          this.hooks.onChat?.(`<${name}> ${text}`, cr, cg, cb);
380	        } else if (moduleId === NetModule.JoinLeave) {
381	          // 加入/离开公告（原版服务器 Lang.mp[19]/[20] 广播，色 (255,240,20)）
382	          const slot = r.u8();
383	          const joined = r.bool();
384	          const name = this.players.get(slot)?.name ?? `玩家${slot}`;
385	          this.hooks.onChat?.(
386	            Lang.text(joined ? 'LegacyMultiplayer.19' : 'LegacyMultiplayer.20', name),
387	            255, 240, 20,
388	          );
389	        }
390	        return;
391	      }
392	      case Msg.RoomPolicy: {
393	        this.policy = {
394	          roomCode: r.str(),
395	          roomName: r.str(),
396	          isHost: r.bool(),
397	          protectTiles: r.bool(),
398	          protectItems: r.bool(),
399	          maxPlayers: (() => { try { return r.u16(); } catch { return 255; } })(),
400	        };
401	        this.hooks.onPolicy?.(this.policy);
402	        return;
403	      }
404	      case Msg.SyncChestItem: {
405	        this.applyRemoteChest(r);
406	        return;
407	      }
408	      case Msg.SyncNPC: {
409	        // v4 短码格式：每条 1B eflags——bit0=含 key 全量(u32 netId+u16 codeId+str key)，
410	        // bit1=boss；否则仅 u16 codeId（查本端 codeId→netId/key 表）。未知短码静默丢弃
411	        // （≤2s 全量兜底自动补；AOI 重入视野/短码表清空后的自愈路径）
412	        const n = r.u16();
413	        const snaps: NpcSnap[] = [];
414	        for (let i = 0; i < n; i++) {
415	          const eflags = r.u8();
416	          let netId = 0, key = '';
417	          if (eflags & 1) {
418	            netId = r.u32();
419	            const code = r.u16();
420	            key = r.str();
421	            this.npcCodes.set(code, { netId, key });
422	          } else {
423	            const code = r.u16();
424	            const e = this.npcCodes.get(code);
425	            if (!e) continue; // 未知短码：跳过本条
426	            netId = e.netId;
427	            key = e.key;
428	          }
429	          snaps.push({
430	            netId, key,
431	            x: r.f32(), y: r.f32(), vx: r.f32(), vy: r.f32(),
432	            hp: r.i16(), maxHp: r.i16(),
433	            animT: r.u16(), flags: eflags & 2 ? 1 : 0,
434	          });
435	        }
436	        this.hooks.onNpcSnapshot?.(snaps);
437	        return;
438	      }
439	      case Msg.SyncItem: {
440	        const netId = r.u32();
441	        const op = r.u8() as 0 | 1 | 2;
442	        let key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0;
443	        if (op === 0) {
444	          key = r.str(); stack = r.u16();
445	          x = r.f32(); y = r.f32(); vx = r.f32(); vy = r.f32();
446	        }
447	        this.hooks.onItemOp?.({ op, netId, key, stack, x, y, vx, vy });
448	        return;
449	      }
450	      case Msg.SyncProjectile: {
451	        const n = r.u16();
452	        const snaps: ProjSnap[] = [];
453	        for (let i = 0; i < n; i++) {
454	          snaps.push({
455	            netId: r.u32(), kind: r.u8(), tag: r.str(),
456	            dmg: r.i16(), aux: r.i16(),
457	            x: r.f32(), y: r.f32(), vx: r.f32(), vy: r.f32(),
458	          });
459	        }
460	        this.hooks.onProjectileSync?.(snaps);
461	        return;
462	      }
463	      case Msg.StrikeNPC: {
464	        const netId = r.u32();
465	        const dmg = r.i16();
466	        const kbx = r.f32(), kby = r.f32();
467	        this.hooks.onStrike?.(netId, dmg, kbx, kby);
468	        return;
469	      }
470	      case Msg.PlayerLifeMana: {
471	        const slot = r.u8();
472	        const hp = r.i16(), maxHp = r.i16();
473	        if (slot !== this.mySlot) this.hooks.onHp?.(slot, hp, maxHp);
474	        return;
475	      }
476	      case Msg.Ping:
477	        return; // 忽略回显
478	      default:
479	        return; // 未知跳过（对齐原版）
480	    }
481	  }
482	
483	  /** Game 侧设置运行期世界引用（时间对齐用） */
484	  gameWorld: World | null = null;
485	
486	  private readWorldData(r: NetReader): World {
487	    const time = r.f64();
488	    const dayCount = r.u32();
489	    const w = r.u16(), h = r.u16();
490	    const spawnX = r.i32(), spawnY = r.i32();
491	    const groundLevel = r.f32(), rockLevel = r.f32(), lavaLine = r.f32();
492	    const seed = r.i32();
493	    const name = r.str();
494	    const crimson = r.bool();
495	    const dungeonX = r.i32(), dungeonY = r.i32(), jungleX = r.i32();
496	    const flagCount = r.u16();
497	    const flags: Record<string, boolean> = {};
498	    for (let i = 0; i < flagCount; i++) flags[r.str()] = r.bool();
499	    const world = new WorldCtor(w, h, seed, name);
500	    world.clock.timeOfDay = time;
501	    world.clock.dayCount = dayCount;
502	    world.spawnX = spawnX; world.spawnY = spawnY;
503	    world.groundLevel = groundLevel; world.rockLevel = rockLevel; world.lavaLine = lavaLine;
504	    world.crimson = crimson;
505	    world.dungeonX = dungeonX; world.dungeonY = dungeonY; world.jungleX = jungleX;
506	    Object.assign(world.flags, flags);
507	    // 请求出生点周围 section（对齐原版 msg8）
508	    this.send(new NetWriter(Msg.SpawnTileData).i32(spawnX).i32(spawnY).finish());
509	    return world;
510	  }
511	
512	  // ================= tile 上报（TileStore.netReporter → 队列 → 每 tick 冲洗） =================
513	
514	  /** TileStore.netReporter 注入点；netSuppress 期间（应用远端操作）不收集 */
515	  reportTileOp(op: TileOp) {
516	    if (!this.active) return;
517	    if (this.tileQueue.length >= 256) {
518	      // R4：超限不再静默丢（静默分叉不可恢复）——告警后仍丢但留下痕迹
519	      if (!this._overflowWarned) {
520	        this._overflowWarned = true;
521	        console.warn('[net] tile 上报队列溢出（单 tick >256 op），丢弃后续——本地与远端将分叉');
522	      }
523	      return;
524	    }
525	    this.tileQueue.push(op);
526	  }
527	  private _overflowWarned = false;
528	
529	  /** Game 每 fixedUpdate 调用：冲洗 tile 队列 + 玩家状态上报（变化驱动 + 66ms 节流） */
530	  tick() {
531	    if (!this.active) return;
532	    this.syncInventory(performance.now());
533	    this.syncHp();
534	    this.flushPending(); // P1.3 msg21 合帧冲洗
535	    if (this.tileQueue.length) {
536	      // 每包最多 64 op（防超帧）
537	      const batch = this.tileQueue.splice(0, 64);
538	      const w = new NetWriter(Msg.TileBatch);
539	      w.u16(batch.length);
540	      for (const o of batch) {
541	        w.u8(o.a);
542	        w.i32(o.x); w.i32(o.y);
543	        w.u16(o.v & 0xffff);
544	        if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
545	      }
546	      this.send(w.finish());
547	    }
548	    this.sendPlayerState();
549	  }
550	
551	  private sendPlayerState() {
552	    // v2 布局（对齐原版 msg13）：控制位 + position(碰撞盒左上) + velocity。
553	    // 远端据此跑本地物理 → 有移动过程；位置差由接收端 netOffset 平滑（瞬移消失）
554	    const p = this.game.player as unknown as {
555	      x: number; y: number; vx: number; vy: number; facing: number; dead: boolean;
556	      inputX: number; inputJump: boolean; inputDown: boolean; inputUp: boolean;
557	      inv: { heldItem(): { id: number } | null };
558	    };
559	    const inp = (this.game as { input?: { mouseDown: boolean; rightDown: boolean } }).input;
560	    // ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction（原版 case 13）
561	    // useItem = 左键按住（原版 controlUseItem；放置/右键交互不计）
562	    const ctrl = (p.inputUp ? 1 : 0) | (p.inputDown ? 2 : 0)
563	      | (p.inputX < 0 ? 4 : 0) | (p.inputX > 0 ? 8 : 0)
564	      | (p.inputJump ? 16 : 0)
565	      | (inp?.mouseDown && !inp.rightDown ? 32 : 0)
566	      | (p.facing > 0 ? 64 : 0);
567	    // selectedItem = 快捷栏槽位索引 0-9（原版 NetMessage.cs:471 语义；v1 误发物品 id）
568	    const sel = (p.inv as unknown as { selected: number }).selected & 0xff;
569	    // 控制位变化即时发（原版 TrySyncingInput Player.cs:6484：任一 control/selectedItem
570	    // 变化立刻 SendData(13)）——原地起跳这类"位置未动"的操作不再等静止心跳
571	    const ctrlChanged = ctrl !== this.lastSentCtrl || sel !== this.lastSentSel || p.dead !== this.lastSentDead;
572	    const now = performance.now();
573	    const moved = Math.abs(p.x - this.lastSentPos.x) > 1 || Math.abs(p.y - this.lastSentPos.y) > 1;
574	    if (!ctrlChanged) {
575	      if (!moved && now - this.lastStateSent < 1000) return; // 静止 1s 心跳（原版 %420 全量兜底的加密版）
576	      if (now - this.lastStateSent < 66) return;             // 位置驱动节流 ≥66ms（≈15Hz）
577	    }
578	    this.lastStateSent = now;
579	    this.lastSentPos = { x: p.x, y: p.y };
580	    this.lastSentCtrl = ctrl;
581	    this.lastSentSel = sel;
582	    this.lastSentDead = p.dead;
583	    // flagBits: [2]hasVelocity [6]ghost
584	    const flag = 4 | (p.dead ? 64 : 0);
585	    this.send(new NetWriter(Msg.PlayerState)
586	      .u8(this.mySlot)
587	      .u8(ctrl).u8(flag)
588	      .u8(sel)
589	      .f32(p.x).f32(p.y)
590	      .f32(p.vx).f32(p.vy)
591	      .finish());
592	  }
593	
594	  private lastSentCtrl = -1;
595	  private lastSentSel = -1;
596	  private lastSentDead = false;
597	
598	  // ================= 箱子同步（msg31/32，服务器权威） =================
599	
600	  /** 请求打开箱子（interactAt 未命中本地 chests 时——访客本地无箱数据） */
601	  requestChestOpen(x: number, y: number) {
602	    this.send(new NetWriter(Msg.RequestChestOpen).i32(x).i32(y).finish());
603	  }
604	
605	  /** 槽位编辑上报（每槽一条消息；服务器权威+广播，编辑者本地已乐观生效） */
606	  sendChestSlot(chestIdx: number, x: number, y: number, slot: number, itemId: number, stack: number) {
607	    const w = new NetWriter(Msg.SyncChestItem);
608	    w.u16(chestIdx); w.i32(x); w.i32(y);
609	    w.u16(1);
610	    w.u8(slot); w.u16(itemId); w.u16(stack);
611	    this.send(w.finish());
612	  }
613	
614	  /** 本地登记的箱子 → 同步槽位号（Game 注册；diff 轮询用） */
615	  chestIndexByPos = new Map<string, number>();
616	
617	  private applyRemoteChest(r: NetReader) {
618	    const chestIdx = r.u16();
619	    const x = r.i32(), y = r.i32();
620	    const n = r.u16();
621	    const items: Array<{ id: number; stack: number } | null> = [];
622	    for (let i = 0; i < n; i++) {
623	      const slot = r.u8(), itemId = r.u16(), stack = r.u16();
624	      items[slot] = itemId ? { id: itemId, stack } : null;
625	    }
626	    this.hooks.onChestSync?.(chestIdx, x, y, items);
627	  }
628	
629	  /** 外观变更后重发 SyncPlayer（进游戏后 applyCharacter 调用——初始两发都在外观应用前） */
630	  resendAppearance() {
631	    if (!this.active || this.mySlot < 0) return;
632	    const p = this.game.player as { appearance?: unknown } | undefined;
633	    if (p?.appearance) {
634	      this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p.appearance)).finish());
635	    }
636	  }
637	
638	  // ================= 远端 tile 应用（回环抑制 + 事件链触发） =================
639	
640	  private applyRemote(ops: TileOp[]) {
641	    const st = this.gameWorld?.store;
642	    if (!st) return;
643	    st.netSuppress = true;
644	    try {
645	      for (const o of ops) {
646	        if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
647	        switch (o.a) {
648	          case TileOpAction.SetTile: st.setTile(o.x, o.y, o.v, o.fx, o.fy); break;
649	          case TileOpAction.SetWall: st.setWall(o.x, o.y, o.v); break;
650	          case TileOpAction.SetHalfBrick: st.setHalfBrick(o.x, o.y, !!o.v); break;
651	          case TileOpAction.SetSlope: st.setSlope(o.x, o.y, o.v); break;
652	          case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
653	          case TileOpAction.SetWire: st.setWire(o.x, o.y, o.v); break;
654	        }
655	      }
656	    } finally {
657	      st.netSuppress = false; // R5：异常安全复位（否则 suppress 永久卡死上报）
658	    }
659	  }
660	
661	  /** 聊天发送 */
662	  sendChat(text: string) {
663	    this.send(new NetWriter(Msg.NetModules).u16(NetModule.Text).str(text).finish());
664	  }
665	
666	  // ================= v3 实体同步（msg16/21/23/27/42，房主权威+服务器中继） =================
667	
668	  /** NPC 快照（msg23） */
669	  sendNpcSnapshot(snaps: NpcSnap[]) {
670	    if (!snaps.length) return;
671	    const w = new NetWriter(Msg.SyncNPC);
672	    w.u16(snaps.length);
673	    for (const s of snaps) {
674	      w.u32(s.netId); w.str(s.key);
675	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
676	      w.i16(s.hp); w.i16(s.maxHp);
677	      w.u16(s.animT & 0xffff);
678	      w.u8(s.flags);
679	    }
680	    this.send(w.finish());
681	  }
682	
683	  /** 掉落物操作（msg21）：op 0=spawn / 1=take / 2=despawn。
684	   *  P1.3 上行合帧：入 pending 攒批（netDropSweep 每 4 tick 可能逐条几十发），
685	   *  tick() 冲洗时拼为单条 WS 消息；满 64 帧立即冲防延迟 */
686	  sendItemOp(op: 0 | 1 | 2, netId: number, key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0) {
687	    const w = new NetWriter(Msg.SyncItem);
688	    w.u32(netId); w.u8(op);
689	    if (op === 0) {
690	      w.str(key); w.u16(stack);
691	      w.f32(x); w.f32(y); w.f32(vx); w.f32(vy);
692	    }
693	    this.pendingFrames.push(w.finish());
694	    if (this.pendingFrames.length >= 64) this.flushPending();
695	  }
696	
697	  /** 冲洗 pending 合帧：多帧拼接为一条 WS 消息（§1.1 允许一 WS 消息串联多帧） */
698	  private flushPending() {
699	    if (!this.pendingFrames.length || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
700	      this.pendingFrames.length = 0;
701	      return;
702	    }
703	    let total = 0;
704	    for (const f of this.pendingFrames) total += f.length;
705	    const joined = new Uint8Array(total);
706	    let off = 0;
707	    for (const f of this.pendingFrames) { joined.set(f, off); off += f.length; }
708	    this.pendingFrames.length = 0;
709	    this.ws.send(joined);
710	  }
711	
712	  /** 弹幕快照（msg27，双向：各自弹幕互播） */
713	  sendProjectileBatch(snaps: ProjSnap[]) {
714	    if (!snaps.length) return;
715	    const w = new NetWriter(Msg.SyncProjectile);
716	    w.u16(snaps.length);
717	    for (const s of snaps) {
718	      w.u32(s.netId); w.u8(s.kind); w.str(s.tag);
719	      w.i16(s.dmg); w.i16(s.aux);
720	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
721	    }
722	    this.send(w.finish());
723	  }
724	
725	  /** 傀儡受击上报（msg42，访客→房主；Enemy.hurt 内经 entityNet 注入调用） */
726	  sendStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
727	    this.send(new NetWriter(Msg.StrikeNPC).u32(netId).i16(rawDmg).f32(kbx).f32(kby).finish());
728	  }
729	
730	  /** HP 上报（msg16，变化驱动 + 200ms 节流；原版客户端权威） */
731	  private lastHpSent = -1;
732	  private lastHpAt = 0;
733	  syncHp() {
734	    if (this.mySlot < 0) return;
735	    const p = this.game.player as unknown as { hp: number; maxHp: number };
736	    const now = performance.now();
737	    if (p.hp === this.lastHpSent) {
738	      if (now - this.lastHpAt < 5000) return; // 满血心跳 5s
739	    } else if (now - this.lastHpAt < 200) return;
740	    this.lastHpSent = p.hp;
741	    this.lastHpAt = now;
742	    this.send(new NetWriter(Msg.PlayerLifeMana).u8(this.mySlot).i16(p.hp).i16(p.maxHp).finish());
743	  }
744	
745	  // ================= 物品/装备同步（msg5，对齐原版 SyncPlayerItem 语义） =================
746	
747	  /** 远端玩家物品快照（Game 侧拷入 proxy.inv——手持/盔甲纸娃娃/挥舞动画渲染用） */
748	  remoteItems = new Map<number, { inv: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> }>();
749	
750	  /** 本地已同步快照（差分基准；null = 尚未全量 dump） */
751	  private sentInv: Array<Array<{ id: number; stack: number } | null>> | null = null;
752	  private invDumpPending = true; // 进房首包全量
753	  private lastInvSync = 0;
754	
755	  /** 全量 dump（进房后立即 + 外部可请求） */
756	  private sendFullInventory() {
757	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
758	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
759	    for (let c = 0; c < 3; c++) {
760	      const arr = c === 0 ? p.inv.slots : c === 1 ? p.inv.armor : p.inv.dye;
761	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
762	        entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: arr[i]?.id ?? 0, stack: arr[i]?.stack ?? 0 });
763	      }
764	    }
765	    this.send(writePlayerItems(entries));
766	    this.sentInv = [p.inv.slots.map(s => s ? { ...s } : null), p.inv.armor.map(s => s ? { ...s } : null), p.inv.dye.map(s => s ? { ...s } : null)];
767	    this.invDumpPending = false;
768	  }
769	
770	  /** 差分上报（tick 内每 250ms 调一次；原版 msg5 变化驱动逐槽发送的批量等价） */
771	  private syncInventory(now: number) {
772	    if (this.mySlot < 0) return;
773	    if (this.invDumpPending || !this.sentInv) { this.sendFullInventory(); return; }
774	    if (now - this.lastInvSync < 250) return;
775	    this.lastInvSync = now;
776	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
777	    const cur = [p.inv.slots, p.inv.armor, p.inv.dye];
778	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
779	    for (let c = 0; c < 3; c++) {
780	      const arr = cur[c];
781	      const sent = this.sentInv[c];
782	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
783	        const a = arr[i], b = sent[i];
784	        if ((a?.id ?? 0) !== (b?.id ?? 0) || (a?.stack ?? 0) !== (b?.stack ?? 0)) {
785	          entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: a?.id ?? 0, stack: a?.stack ?? 0 });
786	          sent[i] = a ? { ...a } : null;
787	        }
788	      }
789	    }
790	    if (entries.length) this.send(writePlayerItems(entries));
791	  }
792	
793	  private applyRemoteItems(entries: Array<ItemSyncEntry & { playerSlot: number }>) {
794	    for (const e of entries) {
795	      if (e.container > 2 || e.itemSlot >= INV_SYNC_SIZES[e.container]) continue;
796	      let bag = this.remoteItems.get(e.playerSlot);
797	      if (!bag) {
798	        bag = {
799	          inv: Array(58).fill(null), armor: Array(20).fill(null), dye: Array(10).fill(null),
800	        };
801	        this.remoteItems.set(e.playerSlot, bag);
802	      }
803	      const arr = e.container === 0 ? bag.inv : e.container === 1 ? bag.armor : bag.dye;
804	      arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: e.stack } : null;
805	    }
806	  }
807	}
808	

```


---

## 🤖 Assistant · 2026-08-12T04:21:13.891Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have a thorough picture. Let me analyze the issues carefully.

### P1.1 AOI analysis

**msg23 path (SyncNPC):**
Server-side flow:
1. Parse entries (netId, code, key, ...).
2. For each rc (excluding sender, state<10): prune; if blind → skip; else compute picked per AOI hysteresis. If picked.length < entries.length → allFull = false.
3. If targets empty → return.
4. If allFull: check allKnown for every (t, e in t.picked). Since allFull means picked.length === entries.length for all targets, allKnown check covers all entries. If allKnown: encode single frame with all entries with flags = boss?2:0 (bit0 not set — known short-code only: f.u8(boss); f.u16(e.code)), and for each entry, for all targets set npcKnown. Then send to each target prio=1. Return.
5. Otherwise per-target encoding with eflags bit0 = full if not known.

Key bug hunt #1: **allKnown fast path writes flags as `boss ? 2 : 0` with only codeId — never the full key**. Correct given that all targets have the code in npcKnown. npcKnown is updated for all targets — consistent with the slow path which does `rc.npcKnown.set(e.code, now)` for each picked entry. In the fast path, npcKnown.set happens for all entries for all targets. In slow path, for each picked entry. Since allFull → picked == entries for all targets. OK.

But wait — the fast path is entered when `allFull` is true. allFull is initialized true, and set to false if any target's picked.length < entries.length. Fine. However there's a subtle bug: **the frame sent in the allKnown fast path is built with `entries.length`, but for all targets `picked === entries`.** OK.

But here's a real issue: the fast-path frame encodes eflags as `boss ? 2 : 0` — i.e. bit0 = 0 meaning "known short code". The client, upon decoding with eflags bit0=0, looks up `this.npcCodes.get(code)`; if missing, `continue` (skip). Client's npcCodes map is keyed by codeId and maps to netId/key. The server's npcKnown is a map keyed by codeId. The server sets npcKnown[code] when it first sends a full entry for that code. But the client's npcCodes entry is set when it receives a full entry (bit0=1) — same condition. But: **npcKnown entries are pruned after 30s of non-use, and npcCodes table cleared at 60000**. If npcKnown was cleared but the client still has the code in its npcCodes (no clearing mechanism client-side except on server's 60000 clear... wait, on server clear, the server clears all clients' npcKnown, but the CLIENT's npcCodes map is not cleared!). Hmm — the client's npcCodes is `private npcCodes = new Map()` in ClientNet, never cleared except... let me check. It's set on full entries. Never cleared. Is there any disconnect/leave clearing? Let me check if npcCodes is reset on disconnect/reconnect. I don't see it reset in disconnect() or connect0(). So on reconnect the stale entries persist — that's actually beneficial for consistency.

But consider the server-side prune: `if (now - t > AOI_PRUNE_MS) rc.npcKnown.delete(cd)` — the server forgets the code is known, so it will re-send the full entry (bit0=1). Client re-sets the same mapping. Fine — self-healing.

The dangerous direction: server thinks client knows code (npcKnown has it), but the client does not have it → client silently drops the entry (`continue`). When can this happen?

Scenario: client reconnects (resumeSession or fresh connection) — new RoomClient created by `room.newClient(ws, token)` in index.ts → new npcKnown map. OK. But what about the client reconnecting with session — index.ts calls `room.newClient` always (line 226), then resumeSession(c, session) which only sets resumedSlot/name/appearance/session. The RoomClient is fresh, so npcKnown is fresh. But the client's local npcCodes map persists across reconnects within the same ClientNet instance (reconnect0 keeps the same ClientNet object)... wait — on reconnect, does the client clear its npcCodes? No. So the client has a stale npcCodes table and the server has an empty npcKnown. Server sends full entries (bit0=1) → client re-registers. Fine.

The reverse: server npcKnown has code, client npcCodes doesn't. Client's npcCodes is only ever *set*, never deleted. So client side only grows. Server-side npcKnown can shrink (30s prune) or clear (60000). Server's npcCodes (code assignment) can also clear at 60000 — and on clear, all clients' npcKnown are cleared too. After the clear, new codes get assigned via `npcCodeSeq = (npcCodeSeq+1) & 0xffff`. **Here's a critical issue**: after clear, the seq continues from where it was (wrapped to 1 if 0). The client's npcCodes table still has the OLD mapping for those codeIds (client-side never cleared!). Consider: before clear, code 37 → netId 100 (Zombie A). Table fills to 60000, server clears. New NPC netId 200 appears, server assigns code = seq continuing, e.g. 5000 → netId 200, sends full entry bit0=1: client does `npcCodes.set(5000, {netId:200,...})` — overwrites. Fine.

But what if the server's seq wraps to a value previously used in the client's stale table and the full entry is dropped (e.g., the frame with bit0=1 is dropped due to backpressure prio=1 drop, or the client was blind at that moment)? Then the server's npcKnown has the code (set in slow path when sending full), the client doesn't have the *new* mapping but has the *old* mapping for the same codeId → **client silently applies the NPC's snapshot to the WRONG NPC (wrong netId/key)**. That's a correctness bug: ghost corruption. Trigger: code table clear at 60000 + subsequent codeId reuse + the initial full frame lost (backpressure drop of prio=1 is exactly the designed drop path!). Actually wait — when server sends the full entry, it does `rc.npcKnown.set(e.code, now)` even if the send itself is later dropped in `send()` due to backpressure. So npcKnown says known while the client never received the full. That's a generic hole: **npcKnown is updated on "queued for send", not "sent"** — any drop in send() (both the prio-based drop at >1MB, and the readyState check) leaves a stale known-entry and the client will permanently skip that NPC until npcKnown prunes after 30s... but wait, prune only happens if the entry isn't refreshed; `npcKnown.set(e.code, now)` happens on every snapshot for that entry while in view, so it will keep being refreshed and the client will never get a full key again. NPC invisible forever (client drops every short-code entry). Recovery requires the NPC to leave the client's AOI for 30s (so npcKnown entry prunes) and come back. Severity: medium-high. This is a genuine finding: "npcKnown 更新时机在 send 之前/与丢帧不一致".

Actually let me double check the order in the slow path:

```js
const known = rc.npcKnown.has(e.code);
out.u8((known ? 0 : 1) | (e.boss ? 2 : 0));
if (known) out.u16(e.code);
else { out.u32(e.netId); out.u16(e.code); out.str(e.key); }
rc.npcKnown.set(e.code, now);
```

Then `this.send(rc, out.finish(), 1)` — send can drop (bufferedAmount > 4MB, or > 1MB && prio>=1). So yes, on drop the known set has already been updated. The entry with the full key is lost → client will `continue` on every subsequent short-code entry for that code → NPC never appears for that client, indefinitely (as long as it stays in view). Confirmed defect. Severity: 高 (in saturation conditions, which is exactly when this batch runs).

Same for fast path: `for (const t of targets) t.rc.npcKnown.set(e.code, now);` inside the encode loop, then sends afterwards. Same issue.

**Deadlock/blind path question**: "盲端跳过语义下有没有客户端永远收不到流的死锁路径?" — Blind clients are skipped. Recovery: msg13 is prio=0 and sent by the client itself (its own position updates lastPosAt at the server when received). Client sends msg13 at ≥66ms when moving, 1s heartbeat when static. So blind ends recover. But what about a client that is state>=10 but has never sent msg13? lastPosAt=0, so now - 0 > 5000 → blind. It will recover after its first msg13. Clients send msg13 in tick() → sendPlayerState. Should be OK.

However — a real hazard: **client that is paused/frozen**: fixedUpdate stops, no msg13 → server marks blind → no entity traffic → fine, that's by design.

What about the NPC authority being the host: if the host is blind (e.g. host's lastPosAt stale because the host client is tabbed out — ping timer still runs though: ping keeps connection alive but no msg13). Then host's own msg23 snapshot... wait the host sends msg23 regardless; the server filters *receivers*. The host is the sender, excluded. So fine.

But here's a subtle one: **NPC AOI for the authority itself**: NPCs near the host get sent to others based on their own positions. Fine.

**A potential "never receives" issue**: AOI uses receiver's position; a receiver who is standing still and sends msg13 every 1s (heartbeat) — fine, positions current.

**aoiNpc leak**: entries are deleted when out of outer radius, or pruned after 30s of no refresh. If a netId disappears entirely (NPC dies / host stops sending it), the entry stays with an old timestamp; prune after 30s removes it. Prune runs only when `now - rc.lastAoiPrune > AOI_PRUNE_MS` — checked in the msg23 loop over receivers. If no msg23 arrives (no NPCs at all), no prune runs — but then no new entries are added either, so no leak beyond a bounded set. OK.

**npcKnown leak**: prune condition `now - t > AOI_PRUNE_MS` — timestamps are refreshed on every sent snapshot for in-view NPCs, so known entries for NPCs that stay in view persist (bounded by entries count ≤64 per batch, but NPC count could be large over time). Prune happens only in the msg23 receive loop. Same as above — bounded. However, note the prune loop runs only if `!picked.length continue` happens after prune — actually prune is before blind check. Fine.

Wait, actually there's an ordering issue: the prune block is inside `for (const rc of this.clients)` in the msg23 handler. But `continue` for blind happens after prune. OK.

**allFull flag bug with targets where picked is partial**: covered.

**Another important check — `allKnown` fast path vs targets that had entries filtered**: In the fast path we send the frame built from `entries` (all of them) to all targets. Since allFull true, every target's picked == entries. OK.

**msg27 path**: no short codes. Fine. One difference: msg27 AOI prune only handles aoiProj; npcKnown untouched — fine.

**msg27 missing: kind>4 → return entire batch**: `if (kind > 4) return;` inside the loop over entries — a single invalid entry silently discards the whole batch. That's a pre-existing pattern (also `if (n > 64) return`). Not part of the AOI batch though. Could mention as low.

Wait, actually there's an inconsistency: in msg23 there's `if (n > 64) return;` and per-entry nothing. In msg27 `if (kind > 4) return` — for a C→S message from an arbitrary client, a malformed single projectile kills the batch for everyone. Low severity.

### broadcastAt for msg13

`broadcastAt(x, y, AOI_PLAYER, f.finish(), c)` — receiver filter, excludes sender. Checks blind. OK. Note prio=0 for player state — deliberate (must-reach). OK.

**Potential issue**: msg13 broadcast — `broadcastAt` filters by receiver's distance to sender's position. But `f` is built fresh — fine.

### P1.3 send/flushOutbox

flushOutbox slices: 
```js
let start = 0, size = 0;
for (let i = 0; i < ob.length; i++) {
  size += ob[i].length;
  if (size < FLUSH_SLICE && i < ob.length - 1) continue;
  const total = size; ... send joined; start = i+1; size = 0;
}
```
This groups frames until size >= FLUSH_SLICE or last element. Note: a single frame larger than FLUSH_SLICE is sent alone (fine — max frame 65535 < 512KB anyway). Slices ≤ 512KB + last frame could push over: when size reaches >= FLUSH_SLICE it flushes at that i. The joined total = size which may exceed FLUSH_SLICE by up to one frame (65535) → max ~576KB < 1MB maxPayload. OK.

Edge: `if (size < FLUSH_SLICE && i < ob.length - 1) continue;` — for the last frame (i === ob.length-1), it always flushes even if size is small. Correct (must flush the remainder).

Edge case: **empty outbox frames**? A frame could theoretically be zero-length? No, min 3 bytes header.

**Critical ordering issue**: flushOutbox is called at the end of each WS 'message' handler in index.ts (line 240), in the close handler (line 244), and in the 10s time-sync interval (line 272). But `kick()` flushes too. Are there other paths that enqueue into outbox without a subsequent flushOutbox? Let's enumerate send() callers and their trigger context:

- All sends in `Room.handle` — called from ws 'message' drain → flush at line 240 after. But **drain processes MULTIPLE frames per message**; handle is called per frame; flush after all. Fine.
- `sendPolicy` — called in SpawnTileData handling. Flushed by message handler.
- `sendStrips` — SpawnTileData. Same.
- The 10s interval sends + flush (line 267-274). OK.
- **disconnect()** broadcasts PlayerActive and JoinLeave to remaining clients (this.send for each other client) — flush happens in the ws 'close' handler (line 244) after room.disconnect(c). OK.
- **What about sends triggered from one client's message handler targeting OTHER clients whose own sockets are idle?** flushOutbox iterates all clients, so fine.

So the outbox is always flushed. **But here's the leak**: outbox grows unboundedly? Between flushes, at most one message's worth of frames (bounded by maxPayload 1MB input → frames). Since flush happens after each message, outbox stays bounded. But wait — **the drain callback may call handle() which enqueues for many clients; then flushOutbox is called once**. Fine.

Hmm, but there's one notable thing: `c.outbox = []` — allocation of new array per flush per client, minor.

**Real bug in flushOutbox**: `if (c.ws.readyState !== WebSocket.OPEN) continue;` — but outbox was already swapped to `[]`... it sets `c.outbox = []` BEFORE the readyState check, so frames are discarded for non-OPEN sockets. That's fine (dropping for closing sockets is intended).

But subtle: **frames enqueued during flushOutbox execution?** flushOutbox → ws.send → synchronous, doesn't invoke handle. No reentrancy.

**Backpressure checks only ws.bufferedAmount** — the question: "排队期间 outbox 本身会无限涨吗?" Between message handler flushes, no. So no.

BUT: there's one path where sends happen outside message handling and outside the 10s interval: **none**? Let me double check index.ts: the only other sends... `room.send` called in the watchdog? No, watchdog just closes. HTTP lobby doesn't send. OK.

Actually wait — there IS a missing flush path: **Room.disconnect()** is called from the 'close' handler, which flushes. But if a client is removed via kick() → ws.close() → close event → disconnect → broadcast to others → flush at line 244. OK.

**kick() ordering**: send(Kick) → flushOutbox() → c.ws.close(). flushOutbox calls c.ws.send(joined) while OPEN → buffered in the socket. Then close() initiates close handshake; ws library will attempt to flush pending data before closing? Actually in `ws`, `close()` sends a close frame but queued data in the send buffer is still transmitted (the close frame is queued after). The remote receives data then close. Generally OK on TCP. But `close()` without a code... `c.ws.close()` defaults to 1005? Fine.

Hmm, but there's a subtle race: kick() → flushOutbox → but the kick frame might be *dropped* by send() if bufferedAmount > 4MB! Then flush, then close → client sees only a disconnect without a reason. Edge case at saturation. Minor.

### stripCache LRU

```js
let frame = this.stripCache.get(key);
if (frame) { delete; set; hit++; }
else {
  frame = encodeStrip(...);
  this.stripCache.set(key, frame);
  if (this.stripCache.size > 512) {
    this.stripCache.delete(this.stripCache.keys().next().value);
  }
  miss++;
}
```

Map preserves insertion order; delete+re-insert on hit moves to end (most-recent). keys().next().value = oldest = LRU. Correct.

But wait — the eviction happens BEFORE `this.roomStats.stripMiss++`? No: after set, before miss++? Order: set, evict check, stripMiss++. Fine.

**Invalidation**: `applyTileOps` deletes the strip key for each op. But is applyTileOps the ONLY path that modifies the world tiles on the server? The server world is also modified by:
- Liquid simulation? Liquid runs client-side (per NetModule.Liquid comment "预留（v1 液体客户端本地）"). The user says "liquid 不走服务器,确认" — confirmed: no liquid messages handled server-side; Msg.TileBatch ops include no liquid action (TileOpAction has no liquid). So liquid changes never reach the server. OK — but note that means clients' liquid diverges; not a server cache issue.
- `this.world.clock.tick(1000)` — clock only.
- chests spliced in applyTileOps.
- saveRooms only reads.

But wait — **TileOpAction.SetTile doesn't carry liquid**, so a client placing/removing a tile where liquid exists doesn't sync liquid. Not part of this review batch.

Hmm, one more: `st.setTileSilent` etc. — are there any other mutations e.g. world.chests from SyncChestItem (chestFrame) — chests aren't in strips. OK.

So stripCache invalidation is complete... **except** one hole: the stripCache deletion happens in applyTileOps *before* the tile is actually modified — same call, same op. Fine. But note the invalidation uses `Math.floor(o.x / STRIP_W) * STRIP_W` — matches sendStrips' key format `${x0},${y0}` with x0 = strip origin. Consistent.

**BUT there is a real cache-consistency bug**: `sendStrips` sends the cached frame to a client only for strips the client hasn't received (`fresh` filter). The cache stores encoded frames for the CURRENT world state. When a tile op invalidates a strip, the cache entry is deleted. But clients who ALREADY received that strip don't get an update... except via msg17 TileBatch broadcast, which happens for every op (broadcast writeTileBatch). So consistency maintained. OK.

Another: **the LRU eviction with a negative/undefined key**: `this.stripCache.keys().next().value as string` — fine since size>512 guarantees non-empty.

**Memory concern**: stripCache holds up to 512 strips × up to 57KB (worst case 200×20 all-distinct tiles) = ~29MB per room. Hmm, 512 × 57KB = 29MB. Realistic strips RLE compress well. But worst case: 32 rooms × 29MB ≈ 940MB — this memory is NOT counted in the worldBudgetUsed (which counts only w*h*11). Worth flagging as a memory observation (medium/low). Actually worst case is realistic for builds with lots of detail? Each strip is 4000 tiles; if fully distinct states (frames differ), the RLE produces runs of 1 → 4000 × 13B ≈ 52KB + header. Yes ~52KB. 512 strips → 26MB/room. For 32 rooms: 850MB. Not budgeted. Medium finding (reliability/memory).

### npcCodes 60000 clear + codeId reuse

As analyzed: the server clears npcCodes and all clients' npcKnown on the server side. Client's npcCodes is NOT cleared → stale codeId→netId mappings. After clear, seq continues: `npcCodeSeq = (npcCodeSeq + 1) & 0xffff`. New codes will eventually collide with old codeIds that remain in the client's table. When the server sends a FULL entry (bit0=1) for a reused code, the client overwrites — correct. But if the full entry is dropped (backpressure) or the client was blind at that moment... wait, blind clients: the server doesn't add to npcKnown for blind clients (they're skipped before the picked loop). So a blind client never gets marked known. Good.

But dropped frames → stale known → silent mis-association: client's stale npcCodes[code] = old NPC → the new NPC's snapshots get applied to the OLD NPC's netId/key. **Ghost misdirection** — visible wrong behavior. And per the earlier finding, the server won't re-send the full key while in view. So it's persistent until the AOI drop + 30s prune.

The fix direction: client should validate? Or server should include a table-generation counter. Anyway, this is a genuine correctness finding tied to the codeId-reuse question. Severity 高 (requires 60000 NPCs accumulated over room lifetime — netIds accumulate; each new spawn gets a new netId? NPC netIds from the host; with respawns over hours, could reach 60000 in a long session. Plausible in a long-running persistent room).

Actually let me reconsider: is `npcCodes.size >= 60000` reachable? netIds are host-assigned; do dead NPCs' netIds get freed and reused by the host? If the host reuses netIds (pool), the table stays small. If netIds monotonically increase, the table grows to 60000 over time. Terraria NPCs: netId increments (Main.npc index based?). Not sure. Either way, the clearing logic exists so it was deemed reachable.

Also: `if (this.npcCodeSeq === 0) this.npcCodeSeq = 1;` — skips 0. Note `npcCodeSeq` init 1, and after clear the seq is NOT reset to 1 (continues), which is actually intentional to delay reuse. Good — but reuse is still inevitable within 65535 assignments.

### resumeSession / newClient field completeness

index.ts line 226: `const c = room.newClient(ws, token);` — always called for every connection, including reconnects. resumeSession only overrides resumedSlot/name/appearance/session. All fields (aoiNpc, aoiProj, npcKnown, lastPosAt, outbox, items, stats) initialized in newClient. Complete. ✓.

But one gap: **resumed client loses its items snapshot** — c.items is a fresh empty inventory, and c.sentStrips is empty so it re-requests all strips (good, needed after reconnect since the world reassembles). Items: the reconnecting client will re-dump its full inventory on the first tick after slot assignment (invDumpPending = true set on PlayerSlot receipt). OK, self-heals.

Another reconnect gap: on reconnect, other clients are NOT re-notified... Actually SpawnTileData handler broadcasts PlayerActive(true) again for the resumed slot. Fine.

**Slot race in resume**: `this.slotUsed[slot] = true;` — the old client's disconnect scheduled a timeout to free the slot in 61s; resumeSession deletes the session entry so the timeout callback returns early. ✓. But what if the timeout already fired (freed slot) and a NEW player took that slot, then the old player reconnects with an expired session → resumeSession returns false (until check) → treated as new player → allocSlot. ✓.

What if the session resume happens while the original disconnect's timeout is pending but the slot was NOT freed — fine.

Edge: `resumeSession` deletes the session entry at resume time. If the reconnect then fails (e.g., Hello never sent, ws closes), the session entry is gone → the client cannot retry again (it has up to 3 reconnect attempts!). Look at ClientNet: on close with session and reconnects < 3 → reconnects++ and reconnects with ?session=. Second attempt: server resumeSession → sessions.get(session) → NOT FOUND (deleted on first attempt) → returns false → c.resumedSlot stays -1 → Hello allocates a NEW slot → the client gets a new slot (PlayerSlot) and continues with a new session. Meanwhile the old slot remains occupied until the 61s timeout frees it. So the client would appear as a new player; old slot leaks for 61s then frees; other clients see the old slot leave. Acceptable-ish, but the "3 reconnect attempts" promise is broken after the first attempt consumes the session even if the connection dies before the game resumes. Minor (低). Actually more precisely: resumeSession consumes the session when the WS connects, but the slot reservation is only meaningful if Hello follows. If the WS dies pre-Hello, the resumedSlot is never used and the session is burned. Medium-low.

Also: **resumeSession is called for a client whose slot may be occupied**? sessions entry holds the slot and slotUsed[slot] stays true during the 60s window (the timeout frees at 61s). If the same player reconnects within the window: slotUsed[slot] is still true (from the original allocation; disconnect didn't free it because state>=10 path). resumedSlot=slot; Hello sets slotUsed[slot]=true (already true). ✓.

But what if TWO connections resume the same session concurrently? Both get resumedSlot=slot (first deletes the session, so second fails). ✓.

### disconnect() slot freeing race

disconnect: `if (c.state >= 10 && c.session)` → keep 60s. Else free immediately. But for a client that never sent Hello (state 0, slot -1) — `if (c.slot >= 0)` guard. ✓.

**Hmm — one real bug candidate in disconnect**: the timeout `.unref?.()` — fine.

But: if the room is closed/removed while sessions pending — setTimeout references `this.slotUsed` — harmless.

### Memory budget (index.ts)

- POST /rooms: estBytes computed from header width/height. If header missing → estBytes = 0 → falls back to `world.w * world.h * 11` after parsing (line 180-181: `worldBudgetUsed += estBytes || world.w*world.h*11`). ✓.
- **预检② vs 实际计入不一致**: precheck uses estBytes (header-based); accounting uses `estBytes || world.w*world.h*11`. If the header lies (e.g. save JSON's header.width ≠ actual world w after load), the precheck could pass while accounting adds more. Minor: an adversarial body could claim a tiny header then load a huge world? loadSaveData creates the world from the save — the actual world dims come from the save data, which presumably matches the header. But a crafted save could have header.width=10 while the world data is 4200×1200? Depends on loadSaveData. If loadSaveData trusts the header too, then fine. Let me check SaveFile.loadSaveData quickly to see whether world dims can exceed header dims.

- removeRoom releases budget. Callers: the idle-reaper interval and DELETE /rooms. Any other place rooms should be removed? `room.closed = true` set in removeRoom. If a room is closed, the reaper also removes it. What about rooms created but the host never joins → reaper handles after 5min idle. ✓.

- **Budget leak via duplicate-code overwrite?** newCode() guarantees uniqueness against existing rooms. ✓.

- **--world persistent room**: added to worldBudgetUsed. Never removed (persistent) ✓. But if WORLD_FILE load succeeds, and the process also had POST /rooms rooms... fine.

- **removeRoom does NOT save the room** — closing a room discards unsaved world changes. Design choice; skip.

- What about `rooms.delete` in the reaper while iterating `rooms` Map — safe for Map iteration with delete. ✓.

- `worldBudgetUsed -= entry.bytes` — if estBytes was 0 and fallback used, entry.bytes = fallback. Consistent ✓.

Let me check loadSaveData to verify header width/height vs world dims.

### saveRooms / shutdown concurrency

- `setInterval(() => saveRooms(...), SAVE_INTERVAL*1000).unref?.()` — the interval is unref'd, fine.
- shutdown: synchronous saveRooms then process.exit(0). Since Node is single-threaded and saveRooms is sync, no interleaving with the interval callback mid-save. ✓ 双信号: shuttingDown guard. ✓.
- **Issue**: shutdown doesn't flush outboxes or close WS connections gracefully — clients just see the socket die. Minor.
- **Issue**: `process.exit(0)` in SIGINT handler — fine.
- **Issue with uncaughtException handler**: keeps running after arbitrary corruption — risky but deliberate ("记录不退出").
- **tmp+rename atomicity**: writeFileSync to `${file}.tmp` then renameSync. **Problem**: multiple rooms use distinct filenames per room, but the SAME tmp name per room. If saveRooms runs concurrently... it can't (sync). But: rename is atomic on POSIX ✓. On failure mid-write, the .tmp remains (no cleanup) — orphan tmp files accumulate on repeated failures. Low.

- **skip condition**: `room.onlineCount === 0 && room.roomStats.tileOps === room.lastSavedTileOps` → skip. Consider: a room with players online always saves (every 5 min) — fine. A room with NO players but tile changes since last save → saves. Note tileOps only increments for ops that pass validation and in-range... wait, let me check: in applyTileOps, `this.roomStats.tileOps++` occurs after the invalidation delete but BEFORE the switch, for every in-range op (even if SetTile v invalid → `continue` earlier). Hmm: the value-range check `if (o.a === TileOpAction.SetTile && o.v >= TILE_DEFS.length) continue;` skips before tileOps++. OK so tileOps counts applied ops.

  **But**: chests! `SyncChestItem` edits modify `chest.items` but do NOT bump tileOps. So an empty room where... wait, chest edits require state>=10 (a player online). Chest edits can only happen while someone is online → onlineCount > 0 at save time... but if the last player leaves right after editing chests and before the save interval, then onlineCount===0 and tileOps unchanged (if no tile edits) → **chest item changes are LOST** (skipped save). That's a real persistence bug! Trigger: single player empties a chest, leaves the room within the save interval window, room goes empty → next auto-save skips because tileOps didn't change → chest contents revert to last saved state. Also `disconnect` doesn't trigger a save. Severity: 高 for persistence correctness (item loss/dupe: actually the last player leaving with items — items taken from chest are in the player's local save... the server save would still have them → item duplication! Player takes item from chest (client local), leaves, server save skipped → chest still has the item on server → another player joins and takes it → dupe).

  Wait — but the room gets reaped 5 minutes after going empty. Between the last player leaving and reaping, autosave runs up to every 300s. If the skip condition holds, the world is never written. Yes — real dupe/loss bug. Also clock.tick changes timeOfDay every second but that's not persisted-relevant? timeOfDay IS saved (saveWorldOnly saves clock presumably). An empty room's clock keeps advancing (the 1s tick interval) but the save is skipped since tileOps unchanged. So server-side time doesn't persist either. Combined with chest changes — the skip condition is too narrow: it should also consider chest mutations and onlineCount transition. I'd rank this 高.

Let me double-check: `room.onlineCount === 0 && room.roomStats.tileOps === room.lastSavedTileOps` → skipped++. Also note `lastSavedTileOps` is only set inside the try after a successful save. ✓.

Also: a room that is empty at startup (--world) with tileOps=0 and lastSavedTileOps=0 → always skipped → never saved even though players may have come, edited chests, and left. Yes.

### stats.ts

- startBpsSampler: `last` Map cleaned by comparing against alive rooms. ✓. Timer unref'd and returned but never used/cleared in index.ts — fine for process lifetime.
- **topMsgs performance**: msgHist grows with distinct msgIds (bounded by 256 msg ids) — Map max ~200 entries. Per /stats call, topMsgs sorts ~200 entries per room — trivial. Not a hotspot. ✓. But msgHist never resets (long-running counters) — fine.
- **A subtle bug in outBps sampling**: uses `rs.lastSampleAt` as the previous sample time, initialized to Date.now() at room construction. First iteration: `prev === undefined` → sets last, continue. Then next: uses (now - rs.lastSampleAt)/1000 ≈ 1s. OK. But if /stats or anything else modifies lastSampleAt... no. Fine.
- `Math.max(0, ...)` guards negative. Fine.

### index.ts watchdog

`c.lastSeen += 1` per second, and handle() sets `c.lastSeen = 0` on EVERY message. Threshold: state>=1 → 120s, else 10s. Client pings every 30s → OK. But note: `room.handle` is invoked from drain for every frame → resets. ✓.

**Bug**: the watchdog iterates `entry.room.clients` for all rooms every second including persistent rooms — fine.

**Bug**: watchdog closes the ws but doesn't call disconnect until the close event fires — fine.

### send() prio coverage

Messages and their prio:
- msg23 NPC snapshots → prio=1 ✓ (both fast and slow paths).
- msg27 projectiles → prio=1 ✓.
- msg13 player state → prio=0 (default) — must-reach, correct.
- msg21 SyncItem → broadcast default prio=0. Hmm, drop protections: item spawn events are one-shot; if dropped due to >4MB backpressure, the item never appears for that client (spawn is a one-time event, no replay). At >4MB the whole link is dropping anyway. Acceptable, but worth noting that msg21 is prio=0 so it survives the 1-4MB band while prio=1 entity frames are dropped — that's arguably correct prioritization.
- msg17 TileBatch broadcast → prio=0 (must reach for world consistency) ✓.
- msg32 chest → 0 ✓. msg42 strike → 0 ✓ (must reach host).
- msg5 items → 0. msg16 HP → 0.

So the prio coverage seems right. One question: in `send()`, the condition `b > LOW_BUFFER_LIMIT && prio >= 1` — meaning prio=1 frames are dropped between 1MB and 4MB. prio values only 0 and 1. OK.

Hmm wait, one more thing: **prio=1 drop accounting**: `if (prio >= 1) c.stats.lowDrops++` — lowDrops counts frames dropped in the 1-4MB band. ✓.

### broadcastAt blind check and the msg13 self-heal

One more check on the "deadlock" question: a blind receiver never gets NPC/projectile/player streams. Its own msg13s still flow up (client always sends). If the client is downloading the world (SpawnTileData) — during that phase, does the client send msg13? state becomes 10 only after SpawnTileData handling. Client sends PlayerState in tick() → sendPlayerState. Does tick run before the world is ready? `if (!this.active) return;` — active is true. It would send position of a player that may not exist yet... `p.x` etc. might be undefined → f32(NaN)? Possibly sends garbage. But the server requires state>=10 to process PlayerState — server sets state=10 in SpawnTileData. The client's first msg13 comes after it's in-game. Fine.

Now, is there a scenario where a client is state>=10 but never sends msg13 and thus is permanently blind → never sees NPCs? A client that joined, got state 10, but whose tick() isn't called (paused before loadWorld?) — the client would be stuck anyway. Also ClientNet.tick is called by Game fixedUpdate. If the game is paused (menu open), does fixedUpdate still run? Probably. OK.

**One more AOI-specific risk**: `aoiBlind` uses `now - c.lastPosAt > AOI_STALE_MS`. lastPosAt is only updated by msg13. But msg13's processing requires `c.state >= 10`. ✓.

### Protocol consistency: msg23 S→C

Server fast path: `f.u8(boss)` where boss = e.boss ? 2 : 0 → eflags bit1, bit0=0 → client reads u16 code, looks up. ✓ fields after: f32 x,y,vx,vy; i16 hp,maxHp; u16 animT. Client reads exactly that order: f32,f32,f32,f32,i16,i16,u16. ✓.

Slow path: eflags bit0|bit1; if bit0 → u32 netId, u16 code, str key, then the common tail. Client: eflags&1 → u32 netId, u16 code, str key → set npcCodes. ✓ same tail. ✓.

C→S msg23: server reads u32 netId, str key, f32×4, i16,i16,u16 animT, u8 flags. Client sendNpcSnapshot writes exactly that. ✓.

Wait — one discrepancy! **In the server fast path, `f.u8(boss)` writes `e.boss ? 2 : 0`, and then `f.u16(e.code)`.** The client decodes `flags: eflags & 2 ? 1 : 0` for the boss bit → matches the original `flags & 1`. ✓.

**RoomPolicy**: server writes str code, str name, bool isHost, bool protectTiles, bool protectItems, u16 maxPlayers. Client reads the same, with a try/catch fallback of 255 for the u16. ✓ direction: S→C only. ✓.

### msg21 check

Server msg21 handler: netId u32, op u8; if op===0 reads str key, u16 stack, f32×4. else if op>2 return. Then broadcast f. Client sendItemOp writes the same. Client receive SyncItem reads u32, u8, and if op===0 the tail. ✓. But server: op===1/2 → nothing more. ✓.

### msg27 C→S vs S→C

The client sends (sendProjectileBatch): u16 n; per entry: u32 netId, u8 kind, str tag, i16 dmg, i16 aux, f32 x,y,vx,vy. Server reads the same ✓. Server relays the same shape ✓. Client receive reads the same ✓. (The protocol.ts comment for msg27 mentions f32 rot — stale comment, but the actual code is consistent.)

### Now check the msg5 count width mismatch!

Server broadcast of player items: `writePlayerItems` writes `w.u16(entries.length)`. Server's read path `readPlayerItems` reads `r.u16()`. ✓ consistent.

But the client's HostItem dump: entries count for a full inventory = 58+20+10 = 88 < 65535 ✓.

### PlayerSlot/Hello

Server Hello reads str magic, u16 ver, str name, then try str token. Client writes str magic, u16 ver, str name, str token ✓.

### SyncPlayerItem server validation

`if (e.itemId >= ITEM_DEFS.length) return false;` — itemId is u16. If a client sends count huge (u16 up to 65535) the loop allocates 65535 entries — bounded, fine. Also `n` is unbounded read from the wire: `readPlayerItems` loops n times, reading 8 bytes each. A malicious frame with n=65535 but only a few bytes → NetReader reads past the end → `this.buf[this.p++]` returns undefined for u8; DataView.getUint16 past end throws RangeError → caught by the try/catch in index.ts around drain → connection closed. Acceptable-ish.

Actually note: **reads past buffer end** in NetReader: u8 returns undefined (not a throw) for byte reads; u16 throws RangeError. Mixed behavior could produce NaN positions without a throw in some paths (e.g., PlayerState reading: r.u8() past end → undefined; f32 past end → throw). Since each frame is length-delimited and the parser gives exact payload bounds, a malformed-but-plausible frame can cause partial processing. The global try/catch closes the socket. OK for robustness; mention as low if worth it.

### readTileBatch server path

Server: `readTileBatch(r)` then `applyTileOps`. **Note**: server validates bounds and applies. But the `ops` broadcast `writeTileBatch(ops)` re-broadcasts ops that were SKIPPED by validation (out-of-range / bad v). E.g. op with v >= TILE_DEFS.length gets skipped in apply but still broadcast to other clients → clients applyRemote does `st.setTile(o.x,o.y,o.v,...)` with an out-of-range... client checks bounds but not v range. Could corrupt client tile state (invalid type index → type arrays are Uint16 so no OOB crash, but render lookup by invalid id → undefined). Hmm, severity 低-中. The op is broadcast with original values. For out-of-range x/y, the client skips them too (`if (o.x<0...) continue`). For invalid tile v, the client will set an invalid type → undefined TILE_DEFS lookups downstream. Let me flag it as a low/medium correctness gap (server should filter before broadcast). Also note that writeTileBatch re-encodes `o.v & 0xffff`.

Also `readTileBatch` n is u16, ops could be 65535 → loops, and `applyTileOps` per op does a stripCache.delete (Map op) — fine.

**Performance note in applyTileOps**: for every op, a `stripCache.delete(key)` and string template allocation — fine.

Also, `this.world.chests.findIndex` per SetTile op with v!==21 — O(chests) per op; chests can be thousands (a 4200×1200 world has hundreds of chests). With a big tile batch (64 ops) that's 64 × O(chests). Minor perf note. Pre-existing? The chest-clear logic with findIndex per op — could be O(n·m). Worth a low perf note.

### Now the msg23 allKnown fast path: "漏更/重复" question

In the fast path, npcKnown.set is called for all entries × all targets — matching the slow path. But note the fast path only sets npcKnown when allKnown was true (they were already known) — so it's a refresh, no new information. ✓ consistent.

**But there's one asymmetry**: the slow path sets npcKnown for picked entries only. If a target is blind, no update. Fine.

**And a missed update**: in the fast-path *attempt* — if `allKnown` is false, the code falls through to the slow loop which correctly handles per-target known flags. ✓.

**entries 为空时的行为**: if n===0 (host sends an empty batch), entries=[], then the targets loop: for each rc, picked=[] → `if (!picked.length) continue;` → targets empty → `if (!targets.length) return;` ✓. No frame sent. ✓. Note: this means a zero-count msg23 is a cheap no-op. ✓.

Wait — but there's an important detail: with entries empty, `allFull` stays true and targets empty → return before the fast path. ✓.

### flushOutbox boundary question (the specific expression)

`if (size < FLUSH_SLICE && i < ob.length - 1) continue;`

Suppose ob = [A(300KB), B(300KB), C(300KB)]:
- i=0: size=300K < 512K && i<2 → continue.
- i=1: size=600K ≥ 512K → flush [A,B] (600KB > 512KB but < 1MB OK), start=2, size=0.
- i=2: size=300K; i is last → flush [C]. ✓.

Worst slice = FLUSH_SLICE - 1 + 65535 ≈ 576KB < 1MB ✓.

### outbox allocation: `c.outbox = []` then later pushes during the loop? No reentrancy.

### One more index.ts issue: `flushOutbox` in the 10s SetTime interval — it iterates all clients of all rooms; each with an empty outbox → cheap.

### Time sync sends use `new NetWriter(18)` hardcoded — Msg.SetTime=18 ✓.

### Now the /stats question about topMsgs performance — fine, bounded.

### Memory: msgHist Map entries keyed by frame[2] — bounded by 256. ✓.

### Check: `send()` uses `frame[2]` as msgId — frame is the finished NetWriter subarray with header. ✓.

### rooms reaper: `entry.room.onlineCount === 0 && idle > 60_000 && idle > 5*60_000` — the `idle > 60_000` is redundant. Cosmetic.

### One more potential budget leak: **`removeRoom` is only called for rooms in `rooms`**. What if a Room's WS server outlives... no.

### HTTP: readBody on error mid-body: reject + req.destroy; the promise rejects → caught → returns 400 ✓. But if the client disconnects, 'error' fires → reject → catch → finish() on a destroyed socket → harmless.

### `JSON.parse(raw.toString('utf8'))` — a 96MB body parse per room create — memory spike 96MB×2. Acceptable given the limit.

### The watchdog: `c.lastSeen > (c.state >= 1 ? 120 : 10)` — for state 0 clients, 10s to complete Hello. Fine.

Let me now check loadSaveData for header mismatch, and also check `saveWorldOnly` writes chests. And check whether tileOps includes chest-clearing ops.

Also need to check: does anything else modify `room.world` (e.g., chest splice outside applyTileOps)? `chest.items` mutations in SyncChestItem handler — yes (not tileOps). Already covered.

Let me quickly grep SaveFile for loadSaveData/saveWorldOnly.
````

</details>


---

## 🤖 Assistant · 2026-08-12T04:21:15.523Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"export function loadSaveData\\|export function saveWorldOnly\" -A 30 game/src/save/SaveFile.ts | head -80",
 "description": "Inspect loadSaveData/saveWorldOnly"
}
```


---

## 🤖 Assistant · 2026-08-12T04:21:15.552Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -rn \"flushOutbox\\|\\.send(\" server/src/ | grep -v \"^\\s*//\" | grep -v \"ws.send\\|this.ws\" ",
 "description": "Enumerate all send/flush call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:21:15.642Z

**📎 ToolResult**

```
84:export function saveWorldOnly(world: World): string {
85-  const st = world.store;
86-  const view: SaveStoreView = {
87-    type: st.type, flags: st.flags, frameX: st.frameX, frameY: st.frameY,
88-    wall: st.wall, liquid: st.liquid, liquidType: st.liquidType, wire: st.wire,
89-    half: st.half, slope: st.slope,
90-  };
91-  const meta: SaveMeta = {
92-    name: world.name, seed: world.seed, w: st.w, h: st.h,
93-    spawnX: world.spawnX, spawnY: world.spawnY,
94-    groundLevel: world.groundLevel, rockLevel: world.rockLevel, lavaLine: world.lavaLine,
95-    treeX: world.treeX, treeStyle: world.treeStyle, treeTops: world.treeTops,
96-    crimson: world.crimson, dungeonX: world.dungeonX, dungeonY: world.dungeonY, jungleX: world.jungleX,
97-    timeOfDay: world.clock.timeOfDay, dayCount: world.clock.dayCount,
98-    chests: world.chests, signs: world.signs, flags: world.flags,
99-    weather: weatherToSave(world.weather),
100-    invasion: { type: world.invasionType, size: world.invasionSize, sizeStart: world.invasionSizeStart,
101-      x: world.invasionX, delay: world.invasionDelay },
102-    altarCount: world.altarCount,
103-    // 挂物族存放物：内部 id 直传（serializeSave 内统一过稳定 id 表，与 chests 同路径）
104-    furniture: world.furnitureItems,
105-  };
106-  const placeholderPlayer: SaveData['player'] = {
107-    hp: 0, x: world.spawnX * 16, y: world.spawnY * 16,
108-    inventory: [], selected: 0,
109-  };
110-  return serializeSave(view, meta, placeholderPlayer, 0);
111-}
112-
113-/** 直接从内存 SaveData 构建(导入 .wld 路径用——跳过 stringify→parse 双拷贝,
114- *  2026-08 审计 #3:该往返单次 20~50MB×2) */
115:export function loadSaveData(data: SaveData): { world: World; player: SaveData['player'] } {
116-  // v3 物品稳定 id → internal(箱子/背包/储物就地重写;v2 旧档直读)
117-  const v3 = (data.version ?? 1) >= 3;
118-  const mapItem = (it: { id: number; stack: number } | null) =>
119-    it && v3 ? { id: it.id === 0 ? 0 : ITEM_INTERNAL_OF_STABLE.get(it.id) ?? 0, stack: it.stack } : it;
120-  const v3Chests = v3
121-    ? data.chests.map((c) => ({ x: c.x, y: c.y, items: c.items.map(mapItem) }))
122-    : data.chests;
123-  if (v3 && data.player) {
124-    data.player = {
125-      ...data.player,
126-      inventory: data.player.inventory.map(mapItem),
127-      banks: data.player.banks?.map((b) => b.map(mapItem)),
128-    };
129-  }
130-  const world = new WorldClass(data.header.width, data.header.height, data.header.seed, data.header.name);
131-  world.spawnX = data.header.spawn[0];
132-  world.spawnY = data.header.spawn[1];
133-  world.groundLevel = data.header.groundLevel;
134-  world.rockLevel = data.header.rockLevel;
135-  // 旧档缺 lavaLine（原版 UnderworldLayer = maxTilesY-200）
136-  world.lavaLine = data.header.lavaLine ?? data.header.height - 200;
137-  if (data.header.treeX) world.treeX = data.header.treeX;
138-  if (data.header.treeStyle) world.treeStyle = data.header.treeStyle;
139-  if (data.header.treeTops?.length) world.treeTops = data.header.treeTops;
140-  if (data.header.crimson !== undefined) world.crimson = data.header.crimson;
141-  if (data.header.dungeonX !== undefined) world.dungeonX = data.header.dungeonX;
142-  // dungeonY 缺省（旧档/导入）回退地表线：CheckToSpawnDungeonEnemies 的 pY<dungeonY+40 门槛近似成立
143-  if (data.header.dungeonY !== undefined && data.header.dungeonY > 0) world.dungeonY = data.header.dungeonY;
144-  else world.dungeonY = world.groundLevel;
145-  if (data.header.jungleX !== undefined) world.jungleX = data.header.jungleX;

```


---

## 👤 User(sidechain) · 2026-08-12T04:21:15.676Z

**📎 ToolResult**

```
server/src/index.ts:240:    room.flushOutbox();
server/src/index.ts:244:    room.flushOutbox();
server/src/index.ts:271:    for (const c of room.clients) if (c.state >= 10) room.send(c, f);
server/src/index.ts:272:    room.flushOutbox();
server/src/room.ts:68:  /** 发送合包暂存（P1.3；ws message 回调末尾 flushOutbox 统一拼发） */
server/src/room.ts:165:  flushOutbox() {
server/src/room.ts:189:      this.send(c, frame, prio);
server/src/room.ts:196:    this.send(c, new NetWriter(Msg.Kick).str(reason).finish());
server/src/room.ts:197:    this.flushOutbox();
server/src/room.ts:208:      if (Math.abs(c.lastX - x) <= radius && Math.abs(c.lastY - y) <= radius) this.send(c, frame, prio);
server/src/room.ts:256:        this.send(c, new NetWriter(Msg.PlayerSlot).u8(c.slot).str(c.session).finish());
server/src/room.ts:262:        this.send(c, this.worldDataFrame());
server/src/room.ts:269:        this.send(c, new NetWriter(Msg.PlayerSpawn).u8(c.slot).i32(this.world.spawnX).i32(this.world.spawnY).finish());
server/src/room.ts:277:          this.send(c, new NetWriter(Msg.PlayerActive).u8(other.slot).bool(true).str(other.name).finish());
server/src/room.ts:278:          this.send(c, new NetWriter(Msg.SyncPlayer).u8(other.slot).str(other.appearance).finish());
server/src/room.ts:288:          if (entries.length) this.send(c, writePlayerItems(entries));
server/src/room.ts:344:          for (const o of ops.slice(0, 8)) this.send(c, this.correctionFrame(o.x, o.y));
server/src/room.ts:373:        this.send(c, this.chestFrame(idx, -1));
server/src/room.ts:391:          this.send(c, this.chestFrame(chestIdx, -1)); // 权威纠正
server/src/room.ts:482:            for (const t of targets) this.send(t.rc, f.finish(), 1);
server/src/room.ts:498:          this.send(rc, out.finish(), 1); // prio=1：背压 1-4MB 水位先丢
server/src/room.ts:573:          for (const t of targets) this.send(t.rc, frame, 1);
server/src/room.ts:584:          this.send(rc, f.finish(), 1);
server/src/room.ts:596:          this.send(target, new NetWriter(Msg.StrikeNPC).u32(netId).i16(Math.max(-32768, Math.min(9999, dmg))).f32(kbx).f32(kby).finish());
server/src/room.ts:602:        this.send(c, new NetWriter(Msg.Ping).f64(ts).finish());
server/src/room.ts:612:    this.send(c, new NetWriter(Msg.RoomPolicy)
server/src/room.ts:721:    this.send(c, new NetWriter(Msg.StatusText).u16(fresh.length).finish());
server/src/room.ts:739:      this.send(c, frame);

```


---

## 🤖 Assistant · 2026-08-12T04:21:56.067Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Good — loadSaveData creates the world from `data.header.width/height`, so the precheck header parse matches the accounting fallback (both header-derived, plus actual world dims equal header dims). So the estBytes precheck is consistent with accounting. ✓ (as long as header exists; if the header is missing, estBytes=0 → precheck passes → accounting uses world.w*world.h*11 = header-derived too; and missing header would throw in loadSaveData → caught → 400. ✓)

Now, the send callsite inventory: are all sends followed by flushOutbox?

- All sends inside `room.handle(...)` — invoked from `ws.on('message')` → flush at line 240 ✓.
- index.ts line 271 (SetTime) → flush line 272 ✓.
- kick() → own flush ✓.
- disconnect() broadcasts — called from 'close' handler → line 244 flush after ✓.

Wait — one more: the `Hello` kick path in index.ts... `ws.close(1002, ...)` directly without going through Room. That's before newClient. Fine.

BUT here's an important one: `room.disconnect(c)` is called in the 'close' handler, which broadcasts PlayerActive(false) to other clients. That flush at line 244 covers it ✓.

**Now the missing-flush case**: are there sends triggered from HTTP handlers? No.

So the ordering concern "有没有调用点绕过 outbox 直接 ws.send" — the only direct ws.send calls are in flushOutbox (line 179) and the ws.close in index.ts. ✓ All good.

One more potential ordering issue: **outbox ordering vs. directly-sent frames** — none exist. ✓

But here's a subtle issue: `flushOutbox()` is called from the message handler of *each* client's socket. Suppose client A's message handler is processing and enqueues to client B. Fine. But consider the reverse ordering issue: within one drain, handle() for frame 1 might enqueue a Kick to client A... kick flushes immediately. OK.

Another subtle one: **kick() calls flushOutbox() which flushes ALL clients' outboxes**, not just the kicked one. That's fine (just early flushing).

Now let me think about **re-entrancy in drain + flush**: `c.parser.drain(...)` → handle → send → outbox push → after drain returns, flushOutbox. If handle throws mid-drain, the catch closes the ws, and flushOutbox still runs at line 240. ✓.

Hmm, but wait: the drain catch at line 235-238 closes the socket. Then line 240 flushOutbox: the throwing client's outbox is discarded (readyState check). Others' flushed ✓.

### Now check npcKnown fast-path frame and `boss` for the allKnown path more carefully.

Fast path frame construction:
```js
f.u16(entries.length);
for (const e of entries) {
  const boss = e.boss ? 2 : 0;
  f.u8(boss); f.u16(e.code);
  ...
}
```
Note the fast path assumes ALL targets know ALL codes (checked). But here's the catch: the check iterates `t.picked` which equals entries when allFull. ✓.

BUT there's a subtle bug: **the fast path is entered only when allFull is true**, and `allKnown` verified. Then for each entry, npcKnown.set for all targets. OK.

**One asymmetry worth reporting**: in the fast path, the NPC's `key` is never re-sent, so if a client's npcCodes has a STALE entry for that codeId (e.g., after the server's 60000-table clear + seq reuse), and the server's npcKnown was also cleared at that moment... then the server would send a full entry (bit0=1) on the next batch, because npcKnown is empty. So the stale-mapping window requires the full entry to be dropped. Combined finding stands.

Actually wait — there's a sharper version of this. After the 60000 clear, the client's npcCodes still contains old codeId→netId mappings. The server reassigns codes via the continuing seq. Now suppose a new codeId value collides with an old one (guaranteed within 65535 assignments after clear). The first time the server sends that code to a client, npcKnown doesn't have it → server sends full (bit0=1) → client overwrites npcCodes[code] ✓ correct. So under lossless conditions the reuse is safe. Only frame loss creates the hazard — and frame loss is the designed behavior under backpressure. So the finding: **codeId 复用 + 丢帧 = 静默错绑**, and no table-generation/epoch to detect it. Plus npcKnown-updated-before-send amplifies it. Report as 高 (though requires a long-lived room + saturation).

Hmm, also worth checking: does the client clear npcCodes on world re-delivery (reconnect)? On reconnect, `worldDelivered=false`, pendingWorld=null... but npcCodes is NOT cleared. On reconnect the server's npcKnown is fresh so full entries come. ✓ safe.

But there's another subtle thing: **two different rooms reuse the same client object?** No.

### Another look at the msg23 receiver filter and the NPC-authority-only sender: `if (c.state < 10 || !this.npcAuthority(c)) return;` ✓.

### AOI: aoiNpc uses netId; `rc.aoiNpc.set(e.netId, now)` — refreshed for picked. Prune after 30s. ✓ no leak.

### One more potential correctness issue in the hysteresis: `if (dist > AOI_ENTITY && !wasVisible) continue;` — a NEW NPC spawning within the inner radius: wasVisible=false, dist <= AOI_ENTITY → passes ✓.

### The "永远收不到流" (deadlock) question — one more scenario: **a receiver inside the inner radius but the sender (host) is far away**: dist computed from the receiver's position to the NPC's position ✓ (not sender-relative). Good.

### broadcastAt for msg13 uses AOI_PLAYER=1920 (Chebyshev). Receiver filter only. ✓.

### Now check `sendStrips` + stripCache more carefully for a correctness issue: the cached frame is a `Uint8Array` subarray view of the NetWriter's internal buffer — shared per frame instance; each encodeStrip creates a new NetWriter ✓. The cache holds references to those buffers (subarray views keep the whole backing ArrayBuffer alive — the buffer is sized to content + slack ≤ 2× ; minor memory note: caching a subarray view pins the entire backing buffer including up to 2× slack. Not important.)

### `sentStrips` Set growth: per client, strips requested are bounded by world area (4200/200 × 1200/20 = 21×60 = 1260 strips max). ✓ no leak.

### Room.clients cleanup on kick: kick() closes the ws; the 'close' handler calls disconnect ✓.

### Now the **`Room.handle` `case Msg.SyncPlayer`** — no `c.state < 10` gate! `case Msg.SyncPlayer: r.u8(); c.appearance = ...` — a client that hasn't completed the handshake (state 1) can set appearance and broadcast to everyone. Pre-existing? Also `case Msg.Ping` has no state gate (fine). Not part of this batch; maybe mention in passing as low. Actually the gate at line 223 `if (c.state < 1 && msgId !== Msg.Hello) return;` — so state>=1 allows SyncPlayer broadcast to state>=10 clients only (broadcast checks state<10 skip). Harmless-ish. Skip or mention briefly.

### The `Hello` resumed-slot path and allocSlot bound comment ✓.

### `allocSlot` uses opts.maxPlayers; resumedSlot can be ≥ maxPlayers ✓ by design.

### One thing to verify: `this.slotUsed[slot] = true;` in the resumed path — but what if that slot is currently occupied by ANOTHER live client (e.g., the session timeout freed the slot and a new player took it, but the session entry hadn't expired... can't happen: the slot is freed only when the session entry is deleted in the same timeout callback). ✓ consistent.

Actually wait — there IS a race: the timeout frees the slot at 61s. `resumeSession` checks `s.until <= Date.now()` → until = disconnect+60s. So at 60-61s, resumeSession fails (expired) ✓. Before 60s, the session entry exists → resume works and the timeout callback sees the session deleted → returns ✓. Consistent.

### saveRooms: `room.closed` skip — after removeRoom, closed=true → skip ✓.

### **Orphan .tmp files**: writeFileSync failure → catch → tmp left behind. Also: rename across devices? tmp is in the same dir ✓.

### stats: `topMsgs` sorts the whole msgHist per room per /stats call — bounded ✓.

### startBpsSampler `last` Map — cleaned ✓. Timer returned but never stopped; unref'd ✓.

### One more: `statsSnapshot` iterates clients including state<10 — fine.

### /stats every room: `[...rooms.values()].map(...)` allocations — fine.

Now let me also double-check `flushOutbox` slicing edge: **frames are Uint8Array subarrays**; `joined.set(ob[k], off)` works with views ✓.

### Priority check on `send(c, correctionFrame)` for protectTiles rejections — prio 0 ✓ must-reach.

### `Msg.SyncItem` broadcast prio 0: one-shot spawn events; when >4MB they're dropped permanently (no replay). The code comment says msg21 deliberately has no AOI because of that. Under saturation, item spawns vanish for saturated clients. Design tradeoff; worth a low note.

Now let me also verify there's no issue with `send()` being called for a client that has state < 10 in broadcastAt/broadcast — both check state ✓.

### One more possible issue: **`this.roomStats.msgHist` keyed by `frame[2]`** — if frame is shorter than 3 bytes → undefined key. All frames are ≥3 ✓.

### index.ts: `wss = new WebSocketServer({ port: PORT, maxPayload: 1 << 20 })` — maxPayload 1MB ✓ > 576KB slice ✓.

### FrameParser.MAX_BUFFER 4MB ✓ > slice.

Now let me double check one thing about the FLUSH_SLICE and the client's FrameParser: the server sends a WS message of up to ~576KB. The client's FrameParser handles it ✓ (4MB buffer).

### Another check on `send()` stats: `c.stats.outBytes += frame.length` happens even if the frame is later dropped in flushOutbox (non-OPEN). Minor stats inaccuracy.

### Now the chest persistence bug — let me double check that `tileOps` doesn't increment for chest edits: in `case Msg.SyncChestItem`, `chest.items[s.slot] = ...` — no tileOps++ ✓. Confirmed: chest edits are invisible to the save-skip heuristic.

Also `clock.tick(1000)` runs for all rooms even when empty → timeOfDay advances; not persisted when skipped. So after a server restart, the clock resets to the last save. Combined with chest edits — the skip condition `onlineCount===0 && tileOps===lastSavedTileOps` skips the world even though the clock and chests changed. Real finding.

Also: **item dupe scenario** — need the room to later be saved. Sequence: player takes item from chest → leaves → autosave skips (no tile ops) → another player joins → server still has the item in the chest → takes it → dupe. Or the room gets reaped (unsaved) → the host's local save is the only copy. Yes, flag as 高.

Now, also check: when a player leaves (disconnect), should we force-save? The design comment says "空房不产生写放大". A cheap fix: set a dirty flag on chest edits or on any disconnect. Suggest.

### Let me also look at whether `applyTileOps` bumps tileOps even for protectTiles-rejected batches — no, rejected batches return before applyTileOps ✓.

### Check the `broadcast(writeTileBatch(ops), c)` for protectTiles rejection — rejected ops don't broadcast (return before) ✓.

But for accepted batches: ops that fail server-side validation (out-of-range, bad v) are still broadcast raw. Client applyRemote has the same bounds check for x/y but NOT the v range check (`SetTile` with v ≥ TILE_DEFS.length → `st.setTile(o.x,o.y,o.v...)` on the client — let me check TileStore.setTile for clamping. If not clamped, the client stores an invalid type id → rendering/data lookup issues, and the client's netReporter might echo it back. Let me quickly check setTile for validation.
````

</details>


---

## 🤖 Assistant · 2026-08-12T04:21:56.542Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"setTile(\\|setTileSilent(\\|setWall(\\|setWallSilent(\" game/src/world/TileStore.ts | head -20",
 "description": "Find setTile definitions in TileStore"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:21:56.622Z

**📎 ToolResult**

```
110:  setTile(x: number, y: number, type: number, frameX = 0, frameY = 0) {
140:  setTileSilent(x: number, y: number, type: number, frameX = 0, frameY = 0) {
150:  setWall(x: number, y: number, wall: number) {
160:  setWallSilent(x: number, y: number, wall: number) {

```


---

## 🤖 Assistant · 2026-08-12T04:21:57.268Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -rn \"aoiNpc\\|aoiProj\\|npcKnown\\|lastAoiPrune\\|lastPosAt\" game/src server/src --include='*.ts' | grep -v \"server/src/room.ts\" | head -20",
 "description": "Find other usages of AOI fields"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:21:57.335Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-12T04:21:58.688Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "limit": 70,
 "offset": 105
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:21:58.713Z

**📎 ToolResult**

```
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

```


---

## 🤖 Assistant · 2026-08-12T04:22:25.516Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Client's setTile does no type-range clamping — stores any u16. So a relayed op with an invalid type (v ≥ TILE_DEFS.length, rejected by the server but still broadcast) corrupts client tile state. But wait — where would an invalid v come from? Only from a malicious/buggy client. The server rejects it locally (its own world stays clean) but broadcasts it to all other clients. That's a validation gap: 中. Trigger: a client sends a TileBatch containing an op with v=TILE_DEFS.length+5 (or wall=9999, slope=9). Server: skips apply; still `this.broadcast(writeTileBatch(ops), c)` — the whole ops array including invalid ones. Other clients apply them. Also, since applyRemote wraps with netSuppress, no echo. Effects: invalid type index stored → downstream TILE_DEFS[type] undefined → likely render errors or weird tiles. Severity 中.

Also note `SetSlope` v>4 server-side check, and `SetWall` v>366 — those too are broadcast raw.

Also `SetActuated` — server checks nothing for actuated (v bool-ish). Client setActuated(!!o.v) — fine.

Now let me double check one more area from the task: "msg23 短码路径(targets/allFull/allKnown 快速路径)... npcKnown 的更新时机是否与慢路径一致(漏更/重复)". I found: fast path sets npcKnown for all targets/entries — same as slow. But one subtle inconsistency: **the fast path refreshes npcKnown even when the send is dropped** (same as slow path). And another: in the slow path, npcKnown.set happens per picked entry — including entries for NPCs at the hysteresis edge. Consistent.

Hmm, but here's a real one I should double check: **the fast-path frame is built from `entries`, but the fast path only runs when every target's picked == entries. The `allKnown` check iterates `t.picked`**. If `entries.length === 0`, targets is empty → early return. Fine.

What about **`allFull` when there is exactly ONE entry and a target picked it**? picked.length(1) < entries.length(1)? No → allFull stays true ✓.

Now the **important one I should verify: `if (picked.length < entries.length) allFull = false;`** — placed after `if (!picked.length) continue;`. So a target with an empty picked contributes nothing and doesn't clear allFull. Correct: only picked targets get frames, and each picked target got all entries.

OK. Now let me also consider the **duplicate-update question**: fast path sets npcKnown twice? No.

One more possible issue in the fast path: **`for (const t of targets) t.rc.npcKnown.set(e.code, now);` is inside the entry loop — O(entries × targets) Map sets** — trivial.

### Now, is there a correctness issue where the fast path is taken but some target's picked has entries in a DIFFERENT ORDER or subset? picked is built by iterating `entries` in order, so picked ⊆ entries in order, and equal when allFull ✓.

### Another possible finding: msg23's AOI filter uses receiver position but NPCs can be HUGE (bosses) — AOI_ENTITY=1280px is fine.

### Now, performance hotspots worth reporting:

1. **msg23/msg27 per-receiver re-encoding**: in the non-allFull path, the server re-encodes a frame per receiver per batch. With 255 players at 15Hz msg23 (host sends how often? entity sync hooks — let me not go too deep). Worst case 255 receivers × 64 entries — bounded. Acceptable, it's the designed path.

2. **`Math.abs` + Map ops per (receiver × entry)** — fine.

3. **`this.roomStats.msgHist`** — fine.

4. **applyTileOps chests.findIndex per SetTile op** — O(ops × chests). With chests in the hundreds and batches of 64 → 64×500=32K comparisons per batch. Minor. Worth a low note.

5. **flushOutbox allocates a new Uint8Array per slice and a new `[]` per client per message** — fine.

6. **`broadcastAt` and the msg13 path allocate a NetWriter per message** — fine.

7. **/stats JSON of all rooms** — fine.

8. **stripCache memory**: 512 strips × up to ~52KB = up to ~26MB per room, NOT counted in the world memory budget (P0.3). With MAX_ROOMS=32 → up to ~850MB unbudgeted. Also, these are `Uint8Array` subarray views pinning their backing buffers. Medium finding (memory budget escape).

Also **stripCache is shared per Room and never shrinks when the room is reaped** — it dies with the Room ✓.

9. **`sendStrips` re-encodes on miss**: the LRU of 512 strips vs. players roaming a 4200×1200 world (1260 strips) → thrashing: every strip request beyond the working set of 512 is a miss → full re-encode of 4000 tiles (11 fields each) ≈ tens of thousands of comparisons per strip. With a player sprinting across the map, each new strip = encode cost. That's the designed tradeoff; miss rate visible in stats. Low note.

Now let me check entitySyncHooks.ts briefly to see the msg23 send rate, to judge whether the fast path matters and whether the host sends all NPCs every tick (n up to 64 per batch, possibly multiple batches per tick). Not strictly necessary.

Let me also verify the claim about `npcKnown` prune being keyed by codeId but `aoiNpc` keyed by netId — after the 60000 clear, aoiNpc entries (keyed by netId) survive while codes are reassigned. Fine.

One more thing to check per the task: "kick() 先冲刷再 close" — done. And "outbox 无上限堆积" — verified no.

Let me also double check the `disconnect()` broadcast: it uses `this.broadcast(...)` which requires state>=10 for receivers, so a leaving player's departure isn't announced to clients still downloading (state<10) — they'll learn via the SpawnTileData loop (only state>=10 others are listed) ✓.

And: **disconnect broadcasts but doesn't flush** — the close handler flushes ✓.

Another index.ts item from the task list: "内存预算(预检/计入/释放路径有没有漏 removeRoom 导致预算泄漏)". Checked:
- POST /rooms → add ✓
- removeRoom (reaper, DELETE) → subtract ✓
- --world → add ✓
- Any room.replace? No.
- What if POST /rooms succeeds in budget accounting but `rooms.set` ... always ✓.
- What about a room whose code collides? newCode checks rooms.has ✓.

One gap: **the precheck uses estBytes from the JSON header; accounting uses `estBytes || world.w*world.h*11`.** If the header width/height are 0/missing (estBytes=0), the precheck passes and accounting uses the real dims — consistent with the actual world since loadSaveData builds from the header dims... wait, if header.width is missing, `data.header.width` would be undefined → `new WorldClass(undefined,...)` → probably NaN/garbage or throws. The try/catch returns 400. Fine.

But here's a subtle mismatch: precheck happens BEFORE `worldFromSaveJson`, accounting AFTER. Between them, no other rooms can be created (single-threaded sync) ✓ no TOCTOU.

**Another budget consideration**: the budget counts only TileStore 11B/tile, but a World also holds chests, signs, furniture, wire arrays... and the 512-strip cache (up to 26MB) and liquid arrays (already in the 11B? type/flags/frameX/frameY/wall/liquid/liquidType/half/slope/wire = 2+1+2+2+2+1+1+1+1+1 = 14B actually! Let me count: type u16=2, flags u8=1, frameX u16=2, frameY u16=2, wall u16=2, liquid u8=1, liquidType u8=1, half u8=1, slope u8=1, wire u8=1 → 14 bytes, not 11. Hmm, the comment says "TileStore 11B/格 估算". Let me verify the actual TileStore field types.

type: Uint16Array (2B), flags: Uint8Array (1B), frameX/frameY: Uint16Array (4B), wall: Uint16Array (2B), liquid/liquidType/half/slope/wire: Uint8Array (5B) → total 14B/tile. Unless wall is Uint8Array. Let me check. If the estimate is 11B but the real footprint is 14B, the budget underestimates by ~27% — a real finding for a memory-guard feature. Let me check TileStore's declarations.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:22:25.789Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && sed -n '1,60p' game/src/world/TileStore.ts",
 "description": "Read TileStore field declarations"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:22:25.866Z

**📎 ToolResult**

```
// SoA 多通道平面数组存储。所有热点代码只碰 TypedArray。
import { TILE_DEFS } from '../data/tiles';
import { TileOpAction } from '../net/protocol';

export class TileStore {
  readonly w: number;
  readonly h: number;
  readonly type: Uint16Array;
  readonly flags: Uint8Array; // bit0 active bit1 framedDecor占位(预留)
  readonly frameX: Uint16Array;
  readonly frameY: Uint16Array;
  readonly wall: Uint16Array; // 原版 wld 墙 id（0-366）
  readonly liquid: Uint8Array;   // 0-255 液量
  readonly liquidType: Uint8Array; // 0无 1水 2岩浆 3蜂蜜 4微光(原版 liquidType 3,本仓库 +1 编码;任意液体遇微光 → Aetherium 块 659)
  readonly half: Uint8Array;      // halfBrick 位（原版 Tile.cs bTileHeader bit1）：下半 8px 实心
  readonly slope: Uint8Array;     // 坡面 0-4（原版编码；渲染暂未支持，生成期少用）
  readonly wire: Uint8Array;      // 电路位（原版 Tile.cs sTileHeader）：bit0红 bit1蓝 bit2绿 bit3黄 bit4致动器 bit5已致动(inActive)
  // wire 位掩码常量（对应原版 Tile.cs:396-459 的 wire/wire2/wire3/wire4/actuator/inActive）
  static readonly WIRE_RED = 1;
  static readonly WIRE_BLUE = 2;
  static readonly WIRE_GREEN = 4;
  static readonly WIRE_YELLOW = 8;
  static readonly WIRE_ACTUATOR = 16;
  static readonly WIRE_ACTUATED = 32;
  static readonly WIRE_COLORS = 15; // 四色掩码

  // tile 变更监听（chunk 缓存 / 光照脏标记 / 液体模拟统一从这里拿事件）
  private listeners: Array<(x: number, y: number) => void> = [];

  // ---- 多人联机上报钩子（ClientNet 注入；单机为 null 零开销） ----
  /** 本地 tile 变更上报（协议层 TileOp 收集器）。liquid 通道不报（客户端本地模拟） */
  netReporter: ((op: import('../net/protocol').TileOp) => void) | null = null;
  /** 应用远端操作期间置位：上报钩子静默（防回环） */
  netSuppress = false;

  constructor(w: number, h: number, bufs?: import('../workers/protocol').TileBuffers) {
    this.w = w; this.h = h;
    // buffers 注入（worker transfer 重建路径）：直接以移交的 ArrayBuffer 包装 TypedArray，
    // 跳过分配与拷贝。缺省 explored 由调用方（World.fromPacket）补齐
    if (bufs) {
      this.type = new Uint16Array(bufs.type);
      this.flags = new Uint8Array(bufs.flags);
      this.frameX = new Uint16Array(bufs.frameX);
      this.frameY = new Uint16Array(bufs.frameY);
      this.wall = new Uint16Array(bufs.wall);
      this.liquid = new Uint8Array(bufs.liquid);
      this.liquidType = new Uint8Array(bufs.liquidType);
      this.half = new Uint8Array(bufs.half);
      this.slope = new Uint8Array(bufs.slope);
      this.wire = new Uint8Array(bufs.wire);
      return;
    }
    const n = w * h;
    this.type = new Uint16Array(n);
    this.flags = new Uint8Array(n);
    this.frameX = new Uint16Array(n);
    this.frameY = new Uint16Array(n);
    this.wall = new Uint16Array(n);
    this.liquid = new Uint8Array(n);
    this.liquidType = new Uint8Array(n);

```


---

## 🤖 Assistant · 2026-08-12T04:22:29.483Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: per-tile storage = 2+1+2+2+2+1+1+1+1+1 = 14 bytes/tile, plus `explored` possibly (let me check if there's an explored array). The estimate uses 11B/tile. So the budget underestimates by 27% (or more with `explored`). That's a genuine P0.3 finding: the WORLD_BUDGET guard under-counts. Severity 中 (budget is a guardrail, and the default 2GB vs actual usage — with a 4200×1200 world: 5.04M tiles × 14B = 70MB actual vs 55MB estimated; 32 such rooms = 2.24GB actual vs 1.77GB estimated → the guard passes at "budget full" while actually 27% over). Combined with the unbudgeted stripCache (~26MB/room) and chest/sign/furniture data, real overshoot can be ~50%+. Report as 中.

Let me quickly check if TileStore has an `explored` array too.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:22:30.117Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"explored\\|Uint8Array(n)\\|Uint16Array(n)\" game/src/world/TileStore.ts | head -20 && echo ---- && grep -rn \"sendNpcSnapshot\\|sendProjectileBatch\" game/src/net/entitySyncHooks.ts | head",
 "description": "Check explored array and entity sync rates"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:22:30.231Z

**📎 ToolResult**

```
39:    // 跳过分配与拷贝。缺省 explored 由调用方（World.fromPacket）补齐
54:    this.type = new Uint16Array(n);
55:    this.flags = new Uint8Array(n);
56:    this.frameX = new Uint16Array(n);
57:    this.frameY = new Uint16Array(n);
58:    this.wall = new Uint16Array(n);
59:    this.liquid = new Uint8Array(n);
60:    this.liquidType = new Uint8Array(n);
61:    this.half = new Uint8Array(n);
62:    this.slope = new Uint8Array(n);
63:    this.wire = new Uint8Array(n);
----

```


---

## 🤖 Assistant · 2026-08-12T04:22:33.078Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"explored\" game/src/world/TileStore.ts | head -5; echo ----; grep -rn \"sendNpcSnapshot\\|sendProjectileBatch\\|netNpcSweep\\|netProjSweep\" game/src --include='*.ts' -l | head; echo ----; grep -rn \"explored\" game/src/world/World.ts | head -3",
 "description": "Check explored array location and entity sync callers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:22:33.851Z

**📎 ToolResult**

```
39:    // 跳过分配与拷贝。缺省 explored 由调用方（World.fromPacket）补齐
----
game/src/net/ClientNet.ts
game/src/core/Game.ts
----
game/src/world/World.ts:74:  explored: Uint8Array;
game/src/world/World.ts:117:  exploredVersion = 0;
game/src/world/World.ts:122:  exploredDirty: { x0: number; y0: number; x1: number; y1: number } | null = null;

```


---

## 🤖 Assistant · 2026-08-12T04:22:35.695Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`explored: Uint8Array` is in World — another 1B/tile. So actual per-tile = 15B vs the 11B estimate → 36% under-count. Good enough for the finding.

Now let me look at how Game.ts calls sendNpcSnapshot to understand the msg23 rate (to assess the fast-path relevance and AOI save). Quick grep.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:22:36.112Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"sendNpcSnapshot\\|sendProjectileBatch\\|netNpcSweep\\|netProjSweep\\|netDropSweep\" game/src/core/Game.ts | head -12",
 "description": "Find entity sync call sites in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:22:36.200Z

**📎 ToolResult**

```
484:    net.sendNpcSnapshot(snaps);
511:    net.sendProjectileBatch(snaps);
515:  private netDropSweep() {
8888:        this.netDropSweep();

```


---

## 🤖 Assistant · 2026-08-12T04:22:39.181Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 60,
 "offset": 465
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:22:39.207Z

**📎 ToolResult**

```
465	        this.netNpcLast.set(e.id, last);
466	      }
467	      const moved = Math.abs(e.x - last.x) > 0.5 || Math.abs(e.y - last.y) > 0.5 || e.hp !== last.hp;
468	      if (!moved && this.tickCount - last.t < 120) continue; // 2s 全量兜底
469	      last.x = e.x; last.y = e.y; last.hp = e.hp; last.t = this.tickCount;
470	      snaps.push({
471	        netId: makeNetId(net.mySlot, e.id), key: e.key,
472	        x: e.x, y: e.y, vx: e.vx, vy: e.vy,
473	        hp: e.hp, maxHp: e.maxHp, animT: e.animT,
474	        flags: e.def.boss ? 1 : 0,
475	      });
476	      if (snaps.length >= 24) break; // 防超帧，余量下轮
477	    }
478	    // 清理已消亡敌人的差分基准
479	    if (snaps.length < 24) {
480	      const alive = new Set<number>();
481	      for (const ent of this.entities.enemies) alive.add((ent as Enemy).id);
482	      for (const id of this.netNpcLast.keys()) if (!alive.has(id)) this.netNpcLast.delete(id);
483	    }
484	    net.sendNpcSnapshot(snaps);
485	  }
486	
487	  /** 双向：本地弹幕快照（15Hz 变化驱动；kind: 0=Arrow 1=WeaponProj族 2=Dart 3=TrapShot 4=MagicProj） */
488	  private netProjBroadcast() {
489	    const net = this.net!;
490	    const snaps: ProjSnap[] = [];
491	    for (const ent of this.entities.projectiles) {
492	      const p = ent as Entity & { projId?: number; damage?: number; kind?: string; color?: string; life?: number };
493	      if (p.netPuppet || p.dead) continue;
494	      let last = this.netProjLast.get(p.id);
495	      if (!last) {
496	        last = { x: p.x, y: p.y, t: this.tickCount };
497	        this.netProjLast.set(p.id, last);
498	      }
499	      if (Math.abs(p.x - last.x) < 1 && Math.abs(p.y - last.y) < 1 && this.tickCount - last.t < 60) continue;
500	      last.x = p.x; last.y = p.y; last.t = this.tickCount;
501	      let kind = -1, tag = '', dmg = Math.max(-32768, Math.min(32767, Math.round(p.damage ?? 0))), aux = 0;
502	      if (p instanceof Arrow) { kind = 0; tag = String(p.projId ?? 1); }
503	      else if (p instanceof Dart) { kind = 2; tag = String(p.projId ?? 0); }
504	      else if (p.projId !== undefined) { kind = 1; tag = String(p.projId); }
505	      else if (p instanceof TrapShot) { kind = 3; tag = p.kind ?? 'dart'; }
506	      else if (p.color !== undefined) { kind = 4; tag = p.color; aux = Math.max(0, Math.min(32767, p.life ?? 600)); }
507	      if (kind < 0) continue; // 未知弹幕类不同步（渲染缺类）
508	      snaps.push({ netId: makeNetId(net.mySlot, p.id), kind, tag, dmg, aux, x: p.x, y: p.y, vx: p.vx, vy: p.vy });
509	      if (snaps.length >= 24) break;
510	    }
511	    net.sendProjectileBatch(snaps);
512	  }
513	
514	  /** 双向：本地真掉落诞生上报 + 消失（拾取/寿命）广播——扫描差分 */
515	  private netDropSweep() {
516	    const net = this.net!;
517	    const cur = new Map<number, ItemDrop>();
518	    for (const ent of this.entities.drops) {
519	      const d = ent as ItemDrop;
520	      if (d.netPuppet) continue;
521	      if (!d.netId) {
522	        d.netId = makeNetId(net.mySlot, d.id);
523	        net.sendItemOp(0, d.netId, ITEM_DEFS[d.itemId]?.key ?? '', d.stack, d.x, d.y, d.vx, d.vy);
524	      }

```


---

## 🤖 Assistant · 2026-08-12T04:23:11.297Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important observation at line 468: the NPC snapshot skips NPCs that haven't moved for <120 ticks (2s) — the "2s 全量兜底" comment. The room.ts comment says "NPC 静止兜底间隔(客户端 2s=120 tick)必须 ≪ 傀儡清扫阈值(300 tick)——AOI 重入视野后 ≤2s 内必有全量快照补 key". OK so NPCs re-entering view get a full key within 2s. That's consistent with the AOI design. ✓

Also note: `netNpcLast` cleanup — "清理已消亡敌人的差分基准" only when snaps.length < 24. Fine.

One more thing relevant to the codeId reuse question: `makeNetId(net.mySlot, e.id)` — netId includes the slot and entity id. Entity ids presumably recycle (id pools). If ids recycle, the npcCodes table stays small (bounded by live NPC count). So the 60000 clear might rarely trigger. Still, the code path exists.

Now — an important check on the AOI comment claim: "客户端 300 tick 超时清除傀儡". When an NPC leaves a receiver's AOI (hysteresis outer), the client's puppet gets no more snapshots → cleared after 300 ticks ✓. When it re-enters, within 2s a full snapshot arrives (if the client knows the code, short-code only; if not, full). ✓ Consistent.

BUT: there's an important interaction with npcKnown prune: after 30s out of view, npcKnown's entry prunes → the next entry into view gets a full key ✓.

Now, let me also verify the entity sync hook cadence: netNpcBroadcast called every tick? Let me check where it's called (tickCount cadence) — not vital.

One more: `if (snaps.length >= 24) break;` — the server allows n ≤ 64 ✓.

I think I have enough for a thorough review. Let me also spot-check `entitySyncHooks.ts` for the puppet timeout claim and whether the client-side handles a wrong-code binding gracefully. Not strictly needed.

Let me also double check one item from the task: "P1.3 ... kick() 先冲刷再 close" — done, plus the noted edge that send() may drop the Kick frame itself at >4MB.

And: "flushOutbox 在哪些路径之后没被调到(index.ts 的所有 send 触发点)" — verified all covered.

Now let me also think about a subtle **ordering bug between outbox and direct sends**: none.

But here's one more real ordering concern: **`send()` checks `c.ws.bufferedAmount` (the socket's unsent bytes) but enqueues to outbox; the outbox is only accounted on flush**. Within a single message handler processing a big inbound message (up to 1MB → could contain ~16 frames of 64KB), the backpressure check sees the pre-message bufferedAmount, so it can enqueue 1MB+ for a client already at 3.9MB, overshooting the 4MB cap. Bounded overshoot (≈1 message). Minor, not worth much.

Another one: **`send()` drops are decided per-frame, but a single flush can push a 512KB slice** — consistent granularity. Fine.

Let me now also confirm the claim in the task about "aoiNpc/aoiProj/npcKnown 的泄漏与清理": all three are pruned on a 30s cadence *but only while msg23/msg27 messages arrive* (prune runs inside those handlers). If the host stops sending msg23 (e.g., host leaves and no new host takes over — hostJoined=false; then npcAuthority(c) is false for everyone → no msg23 → no prune → the maps freeze at their last size). Bounded by the last state; no growth. ✓ No leak.

However — **a leak-ish issue: `sessions` Map** — entries removed by timeout ✓.

And **Room.clients**: removed in disconnect ✓. But what if the WS 'close' event never fires (e.g., a half-open TCP connection)? The watchdog closes after 120s of no messages... `c.ws.close()` on a half-open socket may not emit 'close' promptly; the client object stays in `room.clients` forever → a slot leak and a perpetual broadcast target. Node's ws doesn't have its own keepalive... The ping frame? The server never sends WS protocol-level pings. Half-open detection relies on TCP. Low likelihood; worth a 低 note (room.clients growth on half-open sockets; watchdog's ws.close() doesn't force-terminate). Actually the watchdog runs every second: `c.lastSeen += 1` → after 120 it calls `c.ws.close()` once, then next second lastSeen is 121 > 120 → calls close() again (idempotent). The close event will eventually fire when TCP gives up (could be hours with no traffic? TCP keepalive default off). So a dead-NAT client lingers. Low.

Now let me write up findings. Let me organize:

## 高

1. **persist.ts:18 — 空房跳过条件不含箱子编辑 → 物品复制/丢失**。
   - Trigger: player edits chest contents (msg32, no tileOps bump), leaves room; room empty; auto-save sees `onlineCount===0 && tileOps===lastSavedTileOps` → skip → chest state reverts to the last save. Item taken from a chest "reappears" server-side → dupe when another player loots it; item placed is lost.
   - Also clock.tick advances time but is skipped too (less important).

2. **room.ts:494/480 — npcKnown 在 send 之前/无论 send 是否成功都更新 → 丢帧后该 NPC 对该客户端永久隐身**。
   - Trigger: bufferedAmount in 1–4MB band (prio=1 drop is the designed behavior) exactly when the server sends the only full-key entry for a code → send() drops it → npcKnown already marked known → all subsequent snapshots are short-code only → client `continue` at ClientNet.ts:425 → NPC never renders for that client while it stays in view (npcKnown keeps refreshing each batch → the 30s prune never fires). Recovery only by leaving AOI >30s.
   - Severity 高 (it's precisely the saturation scenario this batch targets; silent and persistent).

3. **room.ts:422-427 + ClientNet.ts:421 — 60000 清表后 codeId 复用 + 客户端 npcCodes 不清 → 错绑(张冠李戴)**。
   - The server clears npcCodes and all clients' npcKnown, but the client's local `npcCodes` map is never cleared (ClientNet has no reset on table-clear or reconnect). After the clear, `npcCodeSeq` continues and will re-issue previously used codeIds. If the re-introducing full frame is dropped (see #2) or... actually even without a drop: safe. With a drop: the client resolves the short code to the OLD netId/key → snapshots of the new NPC drive the wrong puppet. Also same mechanism: any unknown-code skip is silent.
   - Mitigation direction: epoch/generation counter in msg23, or client-side clearing triggered by... simplest: include a table-generation u8 at the head, or never reuse codeIds until the client acks. Severity 高(条件较苛刻但后果是静默数据错绑; 且 #2 使其可达).

Hmm — actually I should double check whether the client's npcCodes gets cleared anywhere else, e.g. entitySyncHooks. Let me grep.

## 中

4. **room.ts:348 — 未通过服务端值域校验的 op 仍原样广播** → other clients store invalid tile types (client setTile doesn't clamp). Trigger: one malicious/buggy client sends SetTile v=TILE_DEFS.length+5 (or wall>366, slope>4) → server skips locally but broadcasts → every other client's world gets the corrupt tile. 中.

5. **index.ts:26/166/180 — 预算按 11B/格估算,实际 TileStore 14B/格 + World.explored 1B/格 = 15B** → 预算低估 ~36%; plus stripCache(≤512×~52KB≈26MB/房)完全不计入 → 32 房满载时实际 RSS 可超预算 ~50%. 中(护栏性缺陷).

6. **room.ts:122/734 — stripCache 无字节上限只有条数上限** — 同上合并进 5? I'll merge into 5 or keep separate. Keep as part of 5.

7. **room.ts:680-689 + index.ts:227 — resumeSession 在 TCP 连接建立时即消费 session,Hello 前断线则凭据作废** → ClientNet 的 3 次重连承诺在第 2 次起失效(回落为新玩家+新 slot,旧 slot 占位 61s). 低-中. I'd rank 低.

## 低

8. kick():196 — Kick 帧本身在 >4MB 时会被 send() 丢弃 → 客户端只见断连无原因. 低.

9. msg27 room.ts:533 — 单条 kind>4 整批丢弃(应 continue 跳过该条). 低.

10. index.ts watchdog — 半开连接 ws.close() 不强制终结 → room.clients 滞留. 低.

11. persist.ts:23 — 写失败留下孤儿 .tmp. 低.

12. room.ts:760 — applyTileOps 每 SetTile op 一次 chests.findIndex O(chests). 低(性能).

13. SyncPlayer 无 state>=10 门禁 (room.ts:293) — state>=1 即可广播外观. 低(非本批).

Actually let me check #3 (client npcCodes clearing) before asserting.

Also to be fair, let me verify #2's claim once more precisely — in the slow path the order is: read known → encode → `rc.npcKnown.set(e.code, now)` → after the loop `this.send(...)`. And send() drops if `b > SEND_BUFFER_LIMIT || (b > LOW_BUFFER_LIMIT && prio >= 1)` with prio=1. Yes.

And #1's severity depends on whether `disconnect` triggers a save — it doesn't. Confirmed.

Also one more check for #1: is there any other dirty signal? `roomStats.tileOps` only in applyTileOps. Yes.

Let me also double check the fast-path line numbers: 480 (`for (const t of targets) t.rc.npcKnown.set(e.code, now);`), slow path 494.

Let me grep the client for npcCodes clearing.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:23:11.677Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -rn \"npcCodes\" game/src | grep -v \"^Binary\"",
 "description": "Check all npcCodes usages on client"
}
```


---

## 👤 User(sidechain) · 2026-08-12T04:23:11.823Z

**📎 ToolResult**

```
game/src/net/ClientNet.ts:113:  private npcCodes = new Map<number, { netId: number; key: string }>();
game/src/net/ClientNet.ts:421:            this.npcCodes.set(code, { netId, key });
game/src/net/ClientNet.ts:424:            const e = this.npcCodes.get(code);

```


---

## 🤖 Assistant · 2026-08-12T04:23:46.601Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: client npcCodes is set-only, never cleared (not on disconnect, not on reconnect, not on any table-clear signal). So finding #3 holds: codeId reuse after the server's 60000 clear can silently bind to a stale mapping if the re-introducing full frame is lost, and there is no epoch to detect it.

Also worth noting for #3: even without frame loss, there is a subtle issue — the client map grows unboundedly across a long session (bounded by distinct codeIds = 65535 max → fine, ~65k entries × small objects = a few MB. Minor).

Now let me double check finding #4 (broadcast of invalid ops) line numbers: applyTileOps validation at room.ts:746-750, broadcast at room.ts:348. Yes.

Also I want to double-check the msg27 "kind>4 return" line number: room.ts:533.

And the watchdog: index.ts:251-261.

One more thing from the task: "RoomPolicy maxPlayers 追加方向" — server writes u16 maxPlayers at the tail (room.ts:618), client reads it at the tail with a try/catch fallback (ClientNet.ts:399). Direction S→C. ✓ aligned. Note the fallback to 255 on a truncated read masks errors but is fine.

And the protocol doc comment for msg27 mentions "f32 rot" (protocol.ts:49) which doesn't match the implementation — stale comment, worth a 低 note for doc consistency.

Also check: "服务器 msg23 下行编码(eflags bit0/bit1)与客户端解码是否逐字段对齐?" — verified aligned. ✓ I'll list in the "checked OK" section.

One more check on the fast path frame: `f.u8(boss)` — for the allKnown fast path, the frame never carries bit0. If a target's npcKnown was stale-but-present (i.e., the code is in npcKnown but the client's map lacks it — from a dropped earlier full), the client skips. Already covered by #2.

Now, one more possible issue I should verify: the allKnown fast-path condition only checks codes present in this batch. Fine.

Let me also think again about the question "盲端跳过语义下有没有客户端永远收不到流的死锁路径?" — I concluded no permanent deadlock because msg13 is prio=0 and self-sent. But there's one more subtle case worth mentioning: **a client whose msg13 never arrives because its own outbound is saturated**? Client sends are small. And another: **a client in state>=10 that sends msg13 but whose msg13 positions are stale because the client is in a menu** — positions still update from the last game position. Fine.

BUT here's one more genuine scenario: **the host itself being the only NPC authority, and the host's msg23 reaching the server, while a receiver's lastPosAt is current** — fine.

And one more: **`aoiBlind` on broadcastAt for msg13** — a blind receiver doesn't get other players' positions. Its own msg13s still update the server. When it unblinds, it gets streams again. But there's no snapshot/replay: the blind client missed player positions → remote players will snap when traffic resumes (the client extrapolates via physics). Not a deadlock. OK.

Also "entries 为空时的行为" — verified no-op return ✓.

Let me now also double check `flushOutbox` slicing for a pathological case: ob = [] — handled by `if (!ob.length) continue`.

And one final check on the task item: "send/flushOutbox(切片逻辑 512KB,`size < FLUSH_SLICE && i < ob.length - 1` 的边界)" — verified correct: always flushes the tail; slices can slightly exceed 512KB by up to one frame (≤65535B) but stay well under the 1MB maxPayload; FrameParser.MAX_BUFFER=4MB covers it. ✓

One more potential issue I should double check — `flushOutbox` resets `size = 0` and `start = i + 1` but what if the LAST iteration flushes at i = ob.length-1 → start = ob.length → loop ends ✓.

Alright. One more thing about stats: `startBpsSampler` returns the timer; index.ts ignores it; unref'd so no exit-blocking. ✓ cleaned via the `last` Map sweep. ✓

And `/stats` topMsgs: msgHist is bounded by msgId count; sorting ~200 entries × rooms per call — negligible. ✓ (I'll note it's fine, with a caveat that msgHist never resets so topMsgs reflects lifetime totals, not current rate — a UX nit, 低/观察值).

Also `statsSnapshot` computes `bufferedKb` from `bufferedMax` (high-water) not current — by design.

Let me also double-check the "sendDrops" bookkeeping double-count: `c.stats.sendDrops++` and `this.roomStats.sendDrops++` — both incremented per dropped frame; roomStats aggregates across clients, so summing client drops would equal room drops. Fine, no double count within one metric.

Hmm wait, one more real check on `send()`: when a frame is dropped, `c.stats.outBytes` and `roomStats.outBytes` are NOT incremented (they're after the drop return) ✓ good — outBps measures sent bytes.

Now — one more consideration on `broadcast()` default prio=0 for msg17 TileBatch: under >4MB saturation, tile ops get dropped → permanent world divergence between clients (no replay/correction mechanism except protectTiles corrections). The room comment for msg21 acknowledges one-shot semantics. For msg17, a dropped op = permanent divergence until someone re-edits that tile. Worth a 中 note? Under >4MB the link is basically dead, so recovery usually means reconnect. I'd list it as 低-中. Let me include as 低 with context.

I think I'm ready. Let me also quickly verify the strip invalidation covers all tile-mutating paths once more, since the task explicitly asks: "失效是否覆盖所有修改入口(applyTileOps 之外还有修改 tile 的路径吗,如液体?liquid 不走服务器,确认)". Server-side world mutation sites: applyTileOps (tile ops, invalidates ✓), SyncChestItem (chests only, not in strips ✓), clock.tick (not tile data ✓), chests.splice in applyTileOps ✓. Liquid: no server path (NetModule.Liquid reserved, TileBatch has no liquid action) — confirmed liquid never mutates the server world, so no invalidation gap. BUT this means client-side liquid changes are never synced at all — a pre-existing v1 limitation (documented in the protocol comment "v1 液体客户端本地"). Worth one line.

Also: `decodeStrip` is not used server-side ✓.

One more: does `setActuated` exist as silent? `st.setActuated` — used in applyTileOps; invalidation happens before the switch regardless of action ✓.

Let me write the final review now. Structure:

- 高 severity findings (3)
- 中 (2-3)
- 低 (several, brief)
- 已检查无问题的点 (bullet list)

Line numbers: let me pin them precisely.
- persist.ts:18 skip condition.
- room.ts:494 (slow path npcKnown.set) and room.ts:480 (fast path set) — and send() drop at room.ts:151-156.
- room.ts:422-427 (clear + seq).
- ClientNet.ts:113/421-427 (no clear, silent continue at 425).
- room.ts:346-349 (broadcast raw ops) vs applyTileOps validation room.ts:748-750; client TileStore.setTile no clamp (TileStore.ts:110-120).
- index.ts:26 + 166 + 180 (11B estimate) vs TileStore.ts:54-63 (14B) + World.ts:74 (explored 1B).
- room.ts:122/734 stripCache 512-entry cap ~26MB unbudgeted.
- room.ts:195-199 kick; send drop at 151.
- room.ts:533 kind>4 whole-batch drop.
- index.ts:251-261 watchdog half-open.
- persist.ts:22-24 orphan tmp.
- room.ts:759-762 chests.findIndex per op.
- room.ts:680-689 + index.ts:227 session consumed at connect.
- protocol.ts:48-49 stale msg27 comment (f32 rot).
- msg17 prio=0 dropped at >4MB → divergence (room.ts:151 + 348).

Also mention the checked-OK list:
- flushOutbox slice boundary math & maxPayload headroom; all send triggers followed by flush (message handler, close handler, 10s timer, kick); outbox bounded (one inbound message's worth) — no unbounded growth, no direct ws.send bypass.
- prio coverage: msg23/msg27 prio=1 (droppable), msg13/17/21/31/32/42/16 prio=0 (must-reach) — direction correct; msg21 one-shot note.
- stripCache LRU: Map insertion-order + delete/re-insert on hit → keys().next() is truly oldest; invalidation key normalization matches sendStrips; no other server-side tile mutation path (liquid confirmed client-local).
- allKnown fast path: npcKnown update timing matches the slow path (refresh-only when all known); entries empty → early return no frame; frame layout matches client decode.
- msg23 S→C/C→S field order & eflags bit0/bit1 aligned with ClientNet; RoomPolicy tail u16 maxPlayers S→C aligned with try/catch fallback.
- blind-end semantics: no permanent starvation — msg13 is prio=0 self-driven, blind ends auto-recover; aoiNpc/aoiProj/npcKnown pruned on 30s cadence, bounded, no leak even if the host stops sending (maps freeze but don't grow).
- newClient field completeness: reconnects go through newClient (index.ts:226) so all P1.1/P1.2 state is fresh; resumeSession only overrides slot/name/appearance/session. Items re-dump via invDumpPending.
- session slot reservation/timeout consistency (60s until vs 61s timeout, resume deletes entry first).
- memory budget add/release symmetry (POST add / removeRoom subtract / --world add; no double-count; single-threaded no TOCTOU; header-based precheck consistent with accounting since loadSaveData builds dims from the same header).
- SIGTERM/SIGINT guarded, saveRooms sync so no interval/shutdown interleaving; timer unref'd.
- stats: last-Map swept, timer unref'd, msgHist bounded (≤256 ids) so topMsgs is cheap.
- FrameParser MAX_BUFFER 4MB > 576KB worst slice — the noted trap is already handled.
- resume slot ≥ maxPlayers allowed by design.

I should also mention one thing about `readBody` — fine.

One more check I should do quickly: does the msg23 handler's prune block run for the SENDER too? No — the loop skips `rc === c`. So the sender's own aoiNpc/npcKnown never pruned. But the sender is the host; the host doesn't receive its own NPC frames. When the host changes (hostJoined=false then a new host), the old host becomes a receiver with a stale, never-pruned... wait, prune happens for receivers in the loop, so once the old host becomes a receiver it gets pruned. But until a msg23 arrives from the new host, no prune. Bounded. ✓

Also: `aoiNpc` etc. are per-client; the sender's own maps are unused. Fine.

Let me finalize. One thing — I should double check my claim about `c.lastSeen` for the watchdog and state. Fine.

Also the redundant `idle > 60_000 && idle > 5*60_000` — cosmetic, mention in passing under low.

Write the final answer in Chinese, concise but specific.
```

</details>


---

## 🤖 Assistant · 2026-08-12T04:24:16.568Z · glm-x-preview-260804

```
以下是对本轮联机容量优化批服务器侧改动的审查结果。已通读 `server/src/room.ts`、`index.ts`、`stats.ts`、`persist.ts`，并逐字段比对 `game/src/net/protocol.ts` 与 `game/src/net/ClientNet.ts` 的收发两端。

---

## 高

### 1. persist.ts:18 — 空房跳过条件不含箱子编辑 → 物品复制/丢失
`saveRooms` 的 skip 条件是 `room.onlineCount === 0 && room.roomStats.tileOps === room.lastSavedTileOps`。但 `tileOps` 只在 `applyTileOps`(room.ts:753)累加，而 **msg32 `SyncChestItem` 直接写 `chest.items`，不碰 tileOps**;`clock.tick` 每秒推进也不计入。

触发场景：玩家从箱子取走物品 → 在 auto-save 周期内退房 → 房间变空且期间无 tile 修改 → 下次 auto-save 跳过写盘 → 服务器档里箱子仍含该物品。之后另一个玩家进房取走 = **物品复制**；反向(放入物品后离开)则是丢失。`disconnect()` 也不触发落盘，没有兜底。房间 5 分钟后被回收，未保存状态彻底丢失。
建议：箱子编辑置脏标记，或 `disconnect` 使最后一个在局玩家离场时强制 save 一次。

### 2. room.ts:480 / 494 — npcKnown 在 send 之前无条件更新，丢帧后该 NPC 对该客户端永久隐身
慢路径顺序是：查 `known` → 编码 → **`rc.npcKnown.set(e.code, now)`** → 循环外才 `this.send(rc, ..., 1)`;快路径同样先 `npcKnown.set` 再 send。而 `send()`(room.ts:151)在 `bufferedAmount ∈ (1MB, 4MB]` 时会丢 prio=1 帧——这正是本批设计的背压行为。

触发场景：服务器饱和、某客户端水位在 1–4MB 区间时，恰好下发某 code 的**唯一一次全量条目**(bit0=1)→ 帧被丢 → npcKnown 已标记"已知" → 之后每批都只发短码 → 客户端在 ClientNet.ts:425 `continue` 静默丢弃。且只要该 NPC 留在视野内，每批都会刷新 `npcKnown` 的时间戳，30s 过期清理永远不会触发 → **NPC 对该客户端无限期不可见**，只有走出滞回外径 30s 以上才自愈。这恰好在“饱和”这一本批要解决的场景下必然发生，且完全静默。
建议：npcKnown 的更新移到确认入队成功之后(send 返回是否入队)，或对全量条目用 prio=0。

### 3. room.ts:422-427 + ClientNet.ts:113/421 — 60000 清表后 codeId 复用 + 客户端 npcCodes 从不清空 → 静默错绑
服务器清表时只清了 `npcCodes` 和各客户端的 `npcKnown`(room.ts:423-424),**客户端本地的 `npcCodes` 表没有任何清空路径**(grep 全库确认只有 set/get 两处，disconnect/重连/清表信号均不清)。清表后 `npcCodeSeq` 继续递增，65535 个分配内必然复用旧 codeId。

触发场景：清表后某 codeId 被重新分配给新 netId → 服务器第一次下发时带全量(bit0=1)，客户端覆盖旧映射，正常；但若该全量帧被丢(见 #2),客户端会用**旧 NPC 的 netId/key** 去驱动新 NPC 的快照 —— 张冠李戴的傀儡，且无任何告警。协议里没有表代际(epoch)字段，客户端无法检测。
建议：msg23 头部加一个表代际 u8,代际变化时客户端清空本地表；这是最小改动。

---

## 中

### 4. room.ts:348 + 748-750 — 未通过服务端值域校验的 op 仍原样广播，污染其他客户端世界
`Msg.TileBatch` 先 `readTileBatch` 拿到全量 `ops`,`applyTileOps` 里对 `v >= TILE_DEFS.length`、`wall > 366`、`slope > 4` 的 op `continue` 跳过，但随后 `this.broadcast(writeTileBatch(ops), c)` 广播的是**未过滤的原始 ops**。客户端 `applyRemote` 只查 x/y 边界，`TileStore.setTile`(TileStore.ts:110)对 type 不做钳制，直接写入 Uint16Array。
触发：任一客户端发一条含非法 v 的 TileBatch → 服务器自己的世界干净，但所有其他客户端存入非法 tile id → 下游 `TILE_DEFS[type]` 取到 undefined。建议先 filter 再 broadcast(与 protectTiles 拒绝路径对称)。

### 5. index.ts:26/166/180 — 内存预算按 11B/格估算，实际 15B/格，且 stripCache 完全不计入
`TileStore` 实际通道是 type2+flags1+frameX2+frameY2+wall2+liquid1+liquidType1+half1+slope1+wire1 = **14B/格**(TileStore.ts:54-63),另有 `World.explored: Uint8Array` 1B/格(World.ts:74)，合计 15B,估算低了 ~36%。默认 2GB 预算下 32 个 4200×1200 房可通过预检，但实际 TileStore 就要 ~2.24GB。另外 `stripCache` 上限 512 条带(room.ts:734),最坏每条 ~52KB(200×20 全异态)≈ **26MB/房**，不在预算内，32 房满载再 +850MB。护栏形同虚设的边缘。建议把估算系数改成 15,并把 stripCache 计入(或加字节上限)。

---

## 低

- **room.ts:195-199(kick)**:`send()` 在 >4MB 时连 Kick 帧本身也会丢 → 饱和时客户端只见断连不见原因。可对 Kick 用不可丢路径(直接 ws.send 或置 prio=-1 语义)。
- **room.ts:533(msg27)**:`if (kind > 4) return` 在循环体内，一条非法弹幕导致整批丢弃，应 `continue` 跳过该条。
- **index.ts:251-261(看门狗)**：半开 TCP 连接上 `ws.close()` 后 close 事件可能长期不来(无协议级 ping/keepalive)，`room.clients` 与 slot 滞留，该端持续被广播。可改 `c.ws.terminate()`。
- **persist.ts:22-24**:`writeFileSync(tmp)` 失败后 catch 只打日志，`.tmp` 孤儿残留，反复失败会堆积。
- **room.ts:759-762(applyTileOps)**:每个非箱 `SetTile` op 都做一次 `chests.findIndex`,O(ops×chests);大世界数百箱 × 64 op/批，批次多时有感。可按 strip 或坐标哈希定位。
- **index.ts:227 + room.ts:680-689**:TCP 建连即消费 session(`sessions.delete`),若 Hello 前断线，凭据已烧掉，ClientNet 承诺的 3 次重连从第 2 次起失效，回落为新玩家+新 slot(旧 slot 占位 61s)。
- **room.ts:348 + 151**:msg17 TileBatch 是 prio=0,>4MB 时被丢后**无重放/纠正机制**(protectTiles 纠正只对非房主)，客户端间世界永久分叉直到重连。
- **index.ts:64**:`idle > 60_000 && idle > 5*60_000` 前半冗余，纯冗余。
- **protocol.ts:48-49**:msg27 注释写"f32 rot"与实现(dmg/aux)不符，陈旧注释。
- **stats.ts:43(topMsgs)**:`msgHist` 键受 msgId 数量约束(≤256),每房排序 ~200 条，/stats 调用开销可忽略，无性能问题；但计数是进程生命周期累计，topMsgs 反映的是历史总量而非当前速率，读数时需注意。

---

## 已检查、确认没问题的点

- **flushOutbox 切片边界**:`size < FLUSH_SLICE && i < ob.length - 1` 逻辑正确——尾帧必发、单帧超限可独立成片；单片最坏 512KB-1+65535B ≈ 576KB,远低于 wss `maxPayload` 1MB 与 `FrameParser.MAX_BUFFER` 4MB(protocol.ts:174 注释里的旧坑已避开)。
- **outbox 无泄漏/无乱序**：全库仅 flushOutbox 内一处 `ws.send`,无绕过；index.ts 所有 send 触发点(message 回调:240、close 回调:244、10s 时钟：272、kick 内部)之后均有 flush;两次 flush 之间 outbox 至多积压一条入站消息的帧量，不会无限涨。
- **prio 覆盖**：msg23/msg27(可降级的实体快照)prio=1,msg13/17/21/31/32/42/16(必须达)prio=0,分级方向正确；msg21 不做 AOI 且 prio=0 与其一次性语义一致。
- **stripCache LRU**:`Map` 插入序 + hit 时 delete/re-set 提尾，`keys().next().value` 确为最旧；失效键归一化(`floor(x/200)*200`)与 `sendStrips` 键格式一致；**liquid 确认不进服务器**(NetModule.Liquid 预留、TileBatch 无液体动作)，applyTileOps 之外无其他服务器侧 tile 写入路径，失效覆盖完整(代价是液体本身不同步，属 v1 已知边界)。
- **msg23 allKnown 快速路径**：npcKnown 更新时机与慢路径一致(快路径仅刷新、慢路径对 picked 逐条置位，无漏更/重复);`entries` 为空时 targets 为空提前 return,零帧下行；快路径帧字段序(eflags,u16 code,f32×4,i16×2,u16)与 ClientNet 解码逐字段对齐，bit0/bit1 语义一致；C→S 全量格式与 `sendNpcSnapshot` 对齐。
- **RoomPolicy**：尾部追加 `u16 maxPlayers`,S→C 方向，客户端带 try/catch 兜底 255,对齐。
- **盲端无死锁**：盲端跳过依赖 msg13 自驱动(prio=0 必达、静止 1s 心跳)，不存在“永远收不到流”的路径；aoiNpc/aoiProj/npcKnown 30s 过期清理有界，即使房主停发也只是冻结不增长，无泄漏。
- **RoomClient 初始化完备**：重连也走 `room.newClient`(index.ts:226),所有 P1.1/P1.2 新字段(lastPosAt/aoiNpc/aoiProj/npcKnown/outbox/items/stats)均为新实例;`resumeSession` 只覆写 slot/name/appearance/session,物品靠客户端 `invDumpPending` 重 dump 自愈。
- **session/slot 一致性**：60s `until` vs 61s 超时释放、resume 先删条目使超时回调早退、重连 slot ≥ maxPlayers 按注释允许，均自洽。
- **预算进出对称**：POST /rooms 与 --world 只加、removeRoom(回收 interval + DELETE)只减，无重复计入；Node 单线程下预检与计入之间无 TOCTOU;预检用 header 尺寸与 loadSaveData 的建世来源一致(header.width/height),预检=计入。
- **关停路径**：SIGTERM/SIGINT 有 `shuttingDown` 单次守卫;`saveRooms` 同步执行，与 unref 的 auto-save interval 不会交错；`.unref()` 不阻塞退出。
- **stats 采样**:`startBpsSampler` 的 `last` Map 有摘房清扫、timer unref;`outBytes` 只在入队成功后累加，outBps 不含丢弃帧，口径正确。

**修复优先级建议**：#2(丢帧后 NPC 永久隐身)和 #1(箱子编辑不落盘)是本轮最该先修的两个——一个破坏本批要保障的饱和场景可用性，一个是经济系统漏洞。
```
