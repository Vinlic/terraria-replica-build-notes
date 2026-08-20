# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T05:57:49.144Z

```
对 ~/Project/GLM/SandboxWorld 的多人联机层做**机制合理性与滥用面**对抗分析。你不是在找语法 bug,而是在回答:"这套机制的权威模型/信任边界/降级语义合理吗?恶意客户端或恶意房主能钻什么空子?哪些设计在极端场景下会反噬?" 搜索广度:thorough。

背景权威模型(先读代码核实,server/src/room.ts + game/src/net/ClientNet.ts + game/src/core/Game.ts net 段 + game/docs/multiplayer-design.md §8bis/§8ter):
- NPC 模拟=房主权威(msg23 只信房主,打击经 msg42 房主结算)
- 玩家 HP/位置/物品=客户端权威(HP 本地结算+msg16 中继——原版同款)
- 服务器权威:tile 应用与中继、箱子内容、时钟
- AOI:服务器按各客户端上行 msg13 位置过滤 msg13/23/27;**盲端(>5s 无 msg13)跳过实体广播**(初版全视野兜底因饱和放大循环改为跳过)
- 背压:≤1MB 正常/1-4MB 丢 prio=1 实体快照/>4MB 全丢
- 敌对弹幕伤害=访客本地结算(v5,bit7=hostile 标志由房主置位)

逐项对抗分析(每项给出:威胁模型、可行性、危害、建议——标注"必须修/建议修/记录即可"):
1. **盲端免伤滥用**:恶意客户端停止发送 msg13 → 服务器判盲 → 跳过 msg23/27 → 傀儡不创建 → netPuppetContact/netPuppetProjContact 无目标 → 免疫一切 NPC/弹幕伤害,直到 120s 看门狗踢。这是不是真实漏洞?代价收益比?缓解选项(盲端仍收 hostile 弹/盲端计时器更短/盲端期间服务器侧判定)?
2. **客户端权威 HP**:访客可任意改 hp/位置/物品——原版同款,但我们的房间制有"破坏保护/物品保护"运营属性,二者矛盾吗?protectItems 保护箱子但玩家可凭空改背包物品(再放进箱子=复制)——评估这条链。
3. **恶意房主**:房主跑全部 NPC 模拟——伪造 msg23(假 NPC 位置/hp)、伪造 msg27 kind=128(把自己的武器弹标 hostile 打访客=强制 PvP,原版有 PvP 开关我们没有)、伪造 msg21 凭空刷掉落。危害与必要性。
4. **AOI 半径合理性**:msg13 1920px(120t)/实体 1280px(80t) vs 原版屏幕(1920×1080@100%≈120×67.5t)与武器射程(弓箭~1500px+屏幕外)——边界战斗中"看得见但打不着同步"或"被打但看不见来源"是否可能?弹幕滞回外径 1280*1.6=2048px:远射程武器(狙击枪/魔法竖琴)的弹幕在飞行中段被停发再重发,访客看到的弹幕轨迹是否断裂?
5. **背压语义**:prio=1 丢弃是静默的(只计数)——实体流断流后客户端傀儡 180/300 tick 清扫重建,战斗中表现为"怪闪烁消失重现"。这个降级路径自洽吗?有没有更优(如插值外推延长/清扫阈值与丢帧联动)?
6. **持久化经济学**:chestEdits/tileOps 脏标记+空房跳过——"最后一个玩家取走箱子物品后退出"在 auto-save 周期内服务器崩溃(SIGKILL)的丢失窗口;--save-interval 300s 是否合理;多房同时落盘的 IO 尖刺。
7. **信任不对称**:访客 msg13 位置服务器全信(AOI 过滤基准+中继)——恶意访客伪造位置影响他人 AOI?伪造 SpawnTileData 拉任意区域 strip(信息泄露面)?
8. **房主单点**:房主退出→hostJoined=false→下一个带 token 的人成为房主(或无主房首进者)——新房主的世界状态是服务器档(可能滞后于旧房主本地)→ NPC/掉落回退。语义是否可接受、要不要公告?

输出:按"必须修/建议修/记录即可"三档分组的分析报告,每条带代码依据。用中文。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T05:57:49.146Z

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

## 🤖 Assistant · 2026-08-12T05:57:50.387Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is a thorough adversarial analysis task on the multiplayer layer. I need to read the code first: server/src/room.ts, game/src/net/ClientNet.ts, game/src/core/Game.ts net section, game/docs/multiplayer-design.md §8bis/§8ter.

Let me start by reading these files.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:57:51.222Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/server/src/ ~/Project/GLM/SandboxWorld/game/src/net/ 2>&1; wc -l ~/Project/GLM/SandboxWorld/server/src/room.ts ~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts ~/Project/GLM/SandboxWorld/game/src/core/Game.ts ~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md 2>&1",
 "description": "List net/server source files and sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:57:51.277Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/net/:
ClientNet.ts
entitySyncHooks.ts
LanDiscovery.ts
protocol.ts

~/Project/GLM/SandboxWorld/server/src/:
index.ts
persist.ts
room.ts
stats.ts
     853 ~/Project/GLM/SandboxWorld/server/src/room.ts
     805 ~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts
    9282 ~/Project/GLM/SandboxWorld/game/src/core/Game.ts
     438 ~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md
   11378 total

```


---

## 🤖 Assistant · 2026-08-12T05:57:52.408Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read the key files. I'll read room.ts and ClientNet.ts fully, the design doc, and the net section of Game.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:57:52.524Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/room.ts"
}
```


---

## 🤖 Assistant · 2026-08-12T05:57:52.658Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/docs/multiplayer-design.md"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:57:52.683Z

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
378	**容量验证方法与实测**（`node game/scripts/_loadprobe.mjs --clients=N --seconds=20 --density=calm|boss [--spread]`，
379	本机 macOS / tsx server；平均出带宽 = 累计字节/时长，比 1s 采样可信）：
380	
381	| 场景 | 服务器平均出带宽 | 每客户端 | 备注 |
382	|---|---|---|---|
383	| 32 人 calm 簇拥（全互见，AOI 最不利） | 1.43 MB/s | 45.9 KB/s | msg27 17.4MB / msg13 6.6MB / msg23 5.4MB（20s 累计） |
384	| 32 人 calm spread（一半 5000px 外） | 0.68 MB/s | 21.8 KB/s | **-53%**（AOI 生效，远组互不可见） |
385	| 100 人 boss 簇拥 | 18.5 MB/s | 184.6 KB/s | 物理上限：全员互见+10 发弹幕互播，带宽 O(N²) 不可约 |
386	| 100 人 boss（盲端修复前） | 25.6 MB/s | 262 KB/s | 修复前 stale 兜底形成饱和放大循环 |
387	
388	实测驱动的两个设计修正（2026-08-12）：
389	1. **盲端语义从"全视野兜底"改为"跳过"**：饱和时 msg13 处理滞后 → 判盲 → 若兜底全量灌流 → 更饱和
390	   （实测 stalePos 197 万次、带宽反升）。盲端本就在滞后，停发实体流让它先追平，msg13 恢复后自愈。
391	2. **全员全量快速路径**：簇拥场景（所有接收端都收全部条目）单帧广播零重编码，
392	   去掉逐接收端 NetWriter 重建的 O(N²) 编码 CPU（msg27 无短码差异时直接复用原帧）。
393	
394	## 9. 分阶段实施（细化版）
395	
396	| 阶段 | 交付物 | 探针验收（可执行） |
397	|---|---|---|
398	| P0 协议层 | shared Buffer/MessageID 表、server 骨架（WS+握手+空世界）、ClientNet、Hello→slot→msg7 往返 | `probe-net-handshake`：浏览器连 server 收到 msg7 且字段与加载的世界一致 |
399	| P1 世界流式 | CompressTileBlock(RLE)、CheckSection、TileSections、msg8/9/10/159 | `probe-net-section`：客户端进房后出生点 ±200×150 逐格 hash == 服务器 |
400	| P2 玩家 | msg4/5/13/14/16/42、NetPlayers、远端渲染、netOffset | `probe-net-players`：双浏览器互见，A 走 10s 后 B 侧位移误差 < 300px 平滑收敛 |
401	| P3 实体 | ServerGame 60Hz（Spawner/NPC AI/液体/电路）、msg23/27/28/29、module0/2 | `probe-net-npc`：同一 NPC 双客户端 hp/位置 tick 级一致 |
402	| P4 交互 | msg17/19/20/31-34/59/61/65、聊天 module1、物品归属 | `probe-net-tiles`：A 挖 B 消失 + 掉落归属防抢拾 |
403	| P5 LAN+UI | UDP 广播、MultiplayerSelect 面板（TitleMenu mp 占位接线）、`npm run host` | 手测双机 LAN；探针覆盖 UI 流程 |
404	| P6 加固 | 重连(§6.4 默认开)、stats、定期存档、长稳脚本、优化项逐个评估开启 | 长稳 10min + 断线注入恢复比对存档 hash |
405	
406	## 10. 风险登记（扩充）
407	
408	| 风险 | 等级 | 缓解 |
409	|---|---|---|
410	| TileSection 编码位标志复杂易错 | 高 | 黄金样本单测 + 两客户端 hash 比对探针双重兜底；codecVer 版本位 |
411	| Node 单线程 60Hz 性能 | 中 | tick 直方图监控；NPC 同步限流；液体可迁 worker_threads |
412	| 引擎 import 链在 Node 断链（data/tiles 等传递依赖） | 中 | server tsconfig paths 白名单 + `--selftest` 启动自检 + CI 冒烟 |
413	| 双客户端 tick 不同步导致实体行为分歧 | 中 | 服务器权威实体（NPC/掉落）单一模拟源；客户端仅显示——天然无分歧；玩家判定各自本地（原版同款） |
414	| packWorld transfer 误用 | 高 | 服务器不用 worldPacket（走 section 流）；单机路径保持现状 |
415	| WS 在企业代理/HTTPS 环境兼容 | 低 | wss 反代文档；游戏本身不存凭证 |
416	| 原版语义偏差回归 | 中 | 每条消息实现附原版行号注释；协议单测对照黄金样本 |
417	
418	## 附录 A. 原版常量速查（实现时直接引用）
419	
420	```
421	60Hz tick / 端口 7777 / maxConnections 256 / 玩家 slot 0..254
422	帧 [u16 len][u8 msgId] ≤65535B / 缓冲 131070B
423	section 200×150 / 活跃窗口 60t / CheckSection 3×3(fluff=1) / 出生点首包 5×3
424	msg13 420t / msg36+16+40 900t / msg7 3600t / 超时 7200t
425	netOffset 平滑半径 300px / NPC 跳过容忍 4 次 / 弹幕 netSpam 60
426	msg23 life 档位 0:sbyte 1:short 2:int / msg21 slot=400 请求分配
427	物品槽冷却 timeItemSlotCannotBeReusedFor / msg17 flag13 无掉落
428	状态机：-1 密码 / 0 连接 / 1 过版本 / 2 发WorldData / 3 发section / 10 在游戏
429	```
430	
431	## 附录 B. 源码锚点（1456）
432	
433	NetMessage.cs（SendData 82 起/CompressTileBlock 1889/SendSection 2695/SyncOnePlayer 2883）、
434	MessageBuffer.cs（GetData 123/握手 179-930/msg13 937/msg17 1127/msg27 1712/门禁 156-171）、
435	Netplay.cs（InitializeServer 243/CheckSection 驱动/UDP 广播 796-857）、
436	RemoteClient.cs（TileSections 37/CheckSection 132/SpamUpdate 76）、
437	Main.cs（Update netMode 分支 17671/UpdateServer 64004/UpdateClient 63965）、
438	NetworkInitializer.cs（模块注册顺序 12-26）。
439	

````


---

## 👤 User(sidechain) · 2026-08-12T05:57:52.702Z

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
41	  chestEdits: number;                   // 累计箱子槽位编辑数（P3.1：msg32 不经 tileOps，须独立脏标记——review S1 物品复制/丢失）
42	}
43	
44	export interface RoomClient {
45	  ws: WebSocket;
46	  parser: FrameParser;
47	  slot: number;
48	  state: number;        // 对齐原版：0 连接 / 1 过握手 / 10 在游戏
49	  name: string;
50	  appearance: string;
51	  lastSeen: number;
52	  isHost: boolean;
53	  /** URL 携带的房主令牌（路由层注入；Hello 消息内 token 为兜底） */
54	  urlToken?: string;
55	  /** 重连凭据（PlayerSlot 下发；断开后 60s 内携此 session 重连同 slot 复位） */
56	  session: string;
57	  /** 重连恢复的 slot（≥0 时 Hello 跳过分配直接复位） */
58	  resumedSlot: number;
59	  /** resumeSession 已认领凭据（Hello 成功前断线 → disconnect 释放认领） */
60	  claimedSession: boolean;
61	  sentStrips: Set<string>;
62	  /** AOI 接收端位置（由其上行 msg13 顺带更新；px 坐标，P1.1） */
63	  lastX: number; lastY: number; lastPosAt: number;
64	  /** AOI 滞回集合：netId → 最近一次出现在某快照批的时刻（P1.1） */
65	  aoiNpc: Map<number, number>;
66	  aoiProj: Map<number, number>;
67	  /** 滞回集/短码集上次过期清理时刻 */
68	  lastAoiPrune: number;
69	  /** msg23 短码已知集：codeId → 最近使用时刻（P1.2；过期清除后自动回落全量） */
70	  npcKnown: Map<number, number>;
71	  /** 发送合包暂存（P1.3；ws message 回调末尾 flushOutbox 统一拼发） */
72	  outbox: Uint8Array[];
73	  stats: ClientStats;
74	  /** 物品快照（msg5 累积；新人进场时全量下发） */
75	  items: {
76	    inv: Array<{ id: number; stack: number } | null>;
77	    armor: Array<{ id: number; stack: number } | null>;
78	    dye: Array<{ id: number; stack: number } | null>;
79	  };
80	}
81	
82	/** slot 物理上限（u8 协议槽位；逻辑上限 = opts.maxPlayers 可小于此值） */
83	const MAX_PLAYERS = 255;
84	const STRIP_W = 200;
85	const STRIP_H = 20;
86	/** 背压分级（P0.1）：≤1MB 正常；1-4MB 只丢 prio=1（实体快照类）；>4MB 全丢。全计数 */
87	const LOW_BUFFER_LIMIT = 1 << 20;
88	const SEND_BUFFER_LIMIT = 4 << 20;
89	/** 单条合包 WS 消息切片上限（防超 wss maxPayload 1MB；留余量） */
90	const FLUSH_SLICE = 512 * 1024;
91	/** 箱子 tile sheet id（TileID.Chest=21；applyTileOps 清箱检测用） */
92	const CHEST_TILE_ID = 21;
93	// ---- P1.1 实体 AOI（切比雪夫距离，px）----
94	const AOI_PLAYER = 1920;  // msg13 远端玩家：120 tiles（同屏协作+建造）
95	const AOI_ENTITY = 1280;  // msg23 NPC / msg27 弹幕：80 tiles（战斗可视）
96	const AOI_OUT_FACTOR = 1.6;   // 滞回外径 = 内径 ×1.6（边界抖动防闪烁）
97	const AOI_STALE_MS = 5000;    // 接收端位置超时：跳过实体广播（见 aoiBlind——防饱和放大循环）
98	const AOI_PRUNE_MS = 30_000;  // 滞回集/短码已知集的过期清理
99	// 不变量（改动前必读）：NPC 静止兜底间隔（客户端 2s=120 tick）必须 ≪ 傀儡清扫阈值
100	// （300 tick）——AOI 重入视野后 ≤2s 内必有全量快照补 key，傀儡不会被误清。
101	// msg21 掉落物不做 AOI：spawn 是一次性事件（无重播机制），过滤会导致走近的玩家永远看不见。
102	
103	export class Room {
104	  readonly opts: RoomOptions;
105	  clients = new Set<RoomClient>();
106	  private slotUsed = new Array<boolean>(MAX_PLAYERS).fill(false);
107	  private hostJoined = false;
108	  /** 断线 session 保留（§8.8 重连：60s 内携 session 重连同 slot 复位，不刷加入公告）。
109	   *  认领制（review 项4）：建连只标记 claimed 不消费，Hello 成功才 delete——
110	   *  握手前二次断线凭据不烧、3 次重连承诺成立；且修复旧实现"认领即删条目 →
111	   *  61s 超时回调因条目不存在而跳过释放"的 slot 永久泄漏 */
112	  private sessions = new Map<string, { slot: number; name: string; appearance: string; until: number; claimed: boolean }>();
113	  closed = false;
114	  /** --world 常驻房（P3.1）：空房回收豁免；hostToken='' 首进者为房主 */
115	  persistent = false;
116	  /** 上次持久化时的 tileOps/chestEdits 基线（P3.1：空房无修改则跳过写盘） */
117	  lastSavedTileOps = 0;
118	  lastSavedChestEdits = 0;
119	  /** 观测计数（P0.1；stats.ts 采样读取） */
120	  readonly roomStats: RoomStats = {
121	    outBytes: 0, outBps: 0, lastSampleAt: Date.now(),
122	    msgHist: new Map(), sendDrops: 0, stalePos: 0,
123	    stripHit: 0, stripMiss: 0, tileOps: 0, chestEdits: 0,
124	  };
125	  /** msg23 短码表（P1.2）：netId → codeId；放 Room 级（服务器权威模拟将来直接复用） */
126	  private npcCodes = new Map<number, number>();
127	  private npcCodeSeq = 1;
128	  /** section 编码缓存（P2.1）：条带 key → 完整帧；插入序即 LRU。
129	   *  双上限：512 条带 / 32MB（最坏全异态条带 ~52KB，纯条数上限不够——review S5） */
130	  private stripCache = new Map<string, Uint8Array>();
131	  private stripCacheBytes = 0;
132	  private static readonly STRIP_CACHE_MAX_BYTES = 32 * 1024 * 1024;
133	
134	  /** 缓存淘汰至双上限内（插入后调用；Map 插入序 = LRU 序） */
135	  private stripCacheEvict() {
136	    while (this.stripCache.size > 512 || this.stripCacheBytes > Room.STRIP_CACHE_MAX_BYTES) {
137	      const oldest = this.stripCache.keys().next().value as string | undefined;
138	      if (oldest === undefined) break;
139	      const f = this.stripCache.get(oldest)!;
140	      this.stripCache.delete(oldest);
141	      this.stripCacheBytes -= f.length;
142	    }
143	  }
144	
145	  constructor(public world: World) {
146	    this.opts = { code: '', name: world.name, publicRoom: true, protectTiles: false, protectItems: false, hostToken: '', maxPlayers: MAX_PLAYERS };
147	  }
148	
149	  get st() { return this.world.store; }
150	  get onlineCount() { let n = 0; for (const c of this.clients) if (c.state >= 10) n++; return n; }
151	
152	  private allocSlot(): number {
153	    // 逻辑上限只约束分配边界；slotUsed 数组保持 255 物理上限（重连复位可能 ≥ 逻辑上限）
154	    for (let i = 0; i < this.opts.maxPlayers; i++) if (!this.slotUsed[i]) { this.slotUsed[i] = true; return i; }
155	    return -1;
156	  }
157	
158	  /** msg23 合法来源（房主权威；P5 服务器权威模拟时改为 `this.sim ? false : c.isHost`） */
159	  private npcAuthority(c: RoomClient): boolean { return c.isHost; }
160	
161	  /** msg42 转发目标（现 = 房主单播；P5 服务器权威时 = 本 Room 结算，无转发） */
162	  private strikeTarget(): RoomClient | null {
163	    for (const c of this.clients) if (c.isHost && c.state >= 10) return c;
164	    return null;
165	  }
166	
167	  /** 入队发送（P1.3 合包：不再直接 ws.send；flushOutbox 统一拼发）。
168	   *  返回是否入队成功（背压丢弃返回 false——调用方据此决定是否标记"已下发"类状态，
169	   *  见 msg23 短码 known 标记：丢帧后必须能重发全量，否则 NPC 对该端永久隐身） */
170	  send(c: RoomClient, frame: Uint8Array, prio = 0): boolean {
171	    if (c.ws.readyState !== WebSocket.OPEN) return false;
172	    const b = c.ws.bufferedAmount;
173	    if (b > c.stats.bufferedMax) c.stats.bufferedMax = b;
174	    if (b > SEND_BUFFER_LIMIT || (b > LOW_BUFFER_LIMIT && prio >= 1)) {
175	      c.stats.sendDrops++;
176	      if (prio >= 1) c.stats.lowDrops++;
177	      this.roomStats.sendDrops++;
178	      return false;
179	    }
180	    c.stats.outBytes += frame.length;
181	    this.roomStats.outBytes += frame.length;
182	    const h = this.roomStats.msgHist.get(frame[2]);
183	    if (h) { h.n++; h.bytes += frame.length; } else this.roomStats.msgHist.set(frame[2], { n: 1, bytes: frame.length });
184	    c.outbox.push(frame);
185	    return true;
186	  }
187	
188	  /** 冲洗合包队列：每客户端拼接为尽量少的 WS 消息（FLUSH_SLICE 切片防超 maxPayload） */
189	  flushOutbox() {
190	    for (const c of this.clients) {
191	      const ob = c.outbox;
192	      if (!ob.length) continue;
193	      c.outbox = [];
194	      if (c.ws.readyState !== WebSocket.OPEN) continue;
195	      let start = 0, size = 0;
196	      for (let i = 0; i < ob.length; i++) {
197	        size += ob[i].length;
198	        if (size < FLUSH_SLICE && i < ob.length - 1) continue;
199	        const total = size;
200	        const joined = new Uint8Array(total);
201	        let off = 0;
202	        for (let k = start; k <= i; k++) { joined.set(ob[k], off); off += ob[k].length; }
203	        c.ws.send(joined);
204	        start = i + 1;
205	        size = 0;
206	      }
207	    }
208	  }
209	
210	  broadcast(frame: Uint8Array, except?: RoomClient, prio = 0) {
211	    for (const c of this.clients) {
212	      if (c === except || c.state < 10) continue;
213	      this.send(c, frame, prio);
214	    }
215	  }
216	
217	  /** 踢出：**直接 ws.send 旁路背压与合包**（饱和时 outbox 路径可能丢 Kick 帧，
218	   *  客户端只见断连不见原因——review 建议；单帧极小无放大风险），随后 close */
219	  private kick(c: RoomClient, reason: string) {
220	    try {
221	      if (c.ws.readyState === WebSocket.OPEN) c.ws.send(new NetWriter(Msg.Kick).str(reason).finish());
222	    } catch { /* 已关闭 */ }
223	    c.ws.close();
224	  }
225	
226	  /** AOI 定向广播（P1.1）：只发给距 (x,y) 切比雪夫 ≤ radius 的在局客户端。
227	   *  盲端（位置过期，见 aoiBlind）跳过并计数 stalePos。 */
228	  private broadcastAt(x: number, y: number, radius: number, frame: Uint8Array, except?: RoomClient, prio = 0) {
229	    const now = Date.now();
230	    for (const c of this.clients) {
231	      if (c === except || c.state < 10) continue;
232	      if (now - c.lastPosAt > AOI_STALE_MS) { this.roomStats.stalePos++; continue; }
233	      if (Math.abs(c.lastX - x) <= radius && Math.abs(c.lastY - y) <= radius) this.send(c, frame, prio);
234	    }
235	  }
236	
237	  /** 接收端是否"位置未知/过期"（盲端）。
238	   *  盲端语义 = **跳过实体广播**（曾用"全视野兜底"，实测在服务器饱和时形成放大循环：
239	   *  msg13 处理滞后 → 判盲 → 全量灌流 → 更饱和。盲端本就在滞后，停发实体让它先追平，
240	   *  msg13 是 prio=0 小帧必达，位置恢复后自动重新入场）。新进房客户端在首个 msg13 前
241	   *  也走此语义——实体晚一两秒出现，无害。 */
242	  private aoiBlind(c: RoomClient, now: number): boolean {
243	    return now - c.lastPosAt > AOI_STALE_MS;
244	  }
245	
246	  /** 连接建立后首消息（Hello 带 roomCode/hostToken 由路由层校验后调用） */
247	  handle(c: RoomClient, msgId: number, r: NetReader) {
248	    if (c.state < 1 && msgId !== Msg.Hello) return; // S2 状态门禁
249	    c.lastSeen = 0;
250	    switch (msgId) {
251	      case Msg.Hello: {
252	        if (c.state >= 1) { this.kick(c, '重复握手'); return; }
253	        const magic = r.str();
254	        const ver = r.u16();
255	        c.name = r.str();
256	        if (magic !== PROTO_MAGIC || ver !== PROTO_VER) {
257	          this.kick(c, `协议不匹配（期望 ${PROTO_MAGIC} v${PROTO_VER}）`);
258	          return;
259	        }
260	        // 房主判定：URL token（路由层 newClient 传入）优先；无则消息内 token 兜底。
261	        // 无主房（服务器 --world 载入，hostToken=''）：首位进房者为房主（NPC 权威源）
262	        const msgToken = (() => { try { return r.str(); } catch { return ''; } })();
263	        const token = c.urlToken || msgToken;
264	        if (!this.hostJoined && ((token && token === this.opts.hostToken) || this.opts.hostToken === '')) {
265	          c.isHost = true;
266	          this.hostJoined = true;
267	        }
268	        // v3 重连：resumedSlot ≥ 0 = 断线复位（同 slot，跳过分配）。
269	        // 认领制：Hello 成功才是凭据的真正消费点（删条目；61s 超时回调见条目已删即不再释放）
270	        let slot = -1;
271	        if (c.resumedSlot >= 0) {
272	          slot = c.resumedSlot;
273	          c.resumedSlot = -1;
274	          this.slotUsed[slot] = true;
275	          c.claimedSession = false;
276	          if (c.session) this.sessions.delete(c.session);
277	        } else {
278	          slot = this.allocSlot();
279	          if (slot < 0) { this.kick(c, '房间已满'); return; }
280	        }
281	        c.slot = slot;
282	        c.state = 1;
283	        if (!c.session) c.session = randomUUID();
284	        this.send(c, new NetWriter(Msg.PlayerSlot).u8(c.slot).str(c.session).finish());
285	        return;
286	      }
287	      case Msg.RequestWorldData: {
288	        if (c.slot < 0) return;
289	        c.state = 2;
290	        this.send(c, this.worldDataFrame());
291	        return;
292	      }
293	      case Msg.SpawnTileData: {
294	        if (c.slot < 0) return;
295	        const x = r.i32(), y = r.i32();
296	        this.sendStrips(c, x, y);
297	        this.send(c, new NetWriter(Msg.PlayerSpawn).u8(c.slot).i32(this.world.spawnX).i32(this.world.spawnY).finish());
298	        // 进场：向房间广播 + 向新客户端下发策略与在场玩家
299	        this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(true).str(c.name).finish());
300	        // 加入公告（原版 NetMessage.cs:2931 Lang.mp[19] 广播、排除本人、色 (255,240,20)）
301	        this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(true).finish());
302	        this.sendPolicy(c);
303	        for (const other of this.clients) {
304	          if (other === c || other.state < 10) continue;
305	          this.send(c, new NetWriter(Msg.PlayerActive).u8(other.slot).bool(true).str(other.name).finish());
306	          this.send(c, new NetWriter(Msg.SyncPlayer).u8(other.slot).str(other.appearance).finish());
307	          // 在场玩家物品快照全量下发（msg5；手持/盔甲/挥舞渲染依赖）
308	          const entries: Array<{ playerSlot: number; container: ItemContainer; itemSlot: number; itemId: number; stack: number }> = [];
309	          const bags = [other.items.inv, other.items.armor, other.items.dye] as const;
310	          for (let ci = 0; ci < 3; ci++) {
311	            for (let i = 0; i < bags[ci].length; i++) {
312	              const it = bags[ci][i];
313	              if (it) entries.push({ playerSlot: other.slot, container: ci as ItemContainer, itemSlot: i, itemId: it.id, stack: it.stack });
314	            }
315	          }
316	          if (entries.length) this.send(c, writePlayerItems(entries));
317	        }
318	        c.state = 10;
319	        return;
320	      }
321	      case Msg.SyncPlayer: {
322	        r.u8(); // 覆写权威 slot（防冒用）
323	        c.appearance = r.str().slice(0, 4096);
324	        this.broadcast(new NetWriter(Msg.SyncPlayer).u8(c.slot).str(c.appearance).finish(), c);
325	        return;
326	      }
327	      case Msg.SyncPlayerItem: {
328	        if (c.slot < 0) return;
329	        // msg5 物品/装备（对齐原版 SyncPlayerItem）：值域校验 + 快照累积 + 权威 slot 中继
330	        const raw = readPlayerItems(r);
331	        const valid = raw.filter((e) => {
332	          if (e.container > 2) return false;
333	          if (e.itemSlot >= INV_SYNC_SIZES[e.container]) return false;
334	          if (e.itemId >= ITEM_DEFS.length) return false; // S5 值域
335	          return true;
336	        });
337	        for (const e of valid) {
338	          const arr = e.container === ItemContainer.Slots ? c.items.inv
339	            : e.container === ItemContainer.Armor ? c.items.armor : c.items.dye;
340	          arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: Math.min(e.stack, ITEM_DEFS[e.itemId]?.maxStack ?? 9999) } : null;
341	        }
342	        if (valid.length) {
343	          this.broadcast(writePlayerItems(valid.map((e) => ({ ...e, playerSlot: c.slot }))), c);
344	        }
345	        return;
346	      }
347	      case Msg.PlayerState: {
348	        if (c.state < 10) return;
349	        // v2 布局（对齐原版 msg13）：slot(丢弃防冒用) + ctrlBits + flagBits + selectedItem
350	        // + position(左上) [+velocity 若 flagBits[2]]——原样中继，仅覆写权威 slot
351	        r.u8();
352	        const ctrl = r.u8(), flag = r.u8(), sel = r.u8();
353	        const x = r.f32(), y = r.f32();
354	        let vx = 0, vy = 0;
355	        if (flag & 4) { vx = r.f32(); vy = r.f32(); }
356	        // P1.1 AOI：顺带记录发送端位置（接收端过滤的基准），零额外解析成本
357	        c.lastX = x; c.lastY = y; c.lastPosAt = Date.now();
358	        const f = new NetWriter(Msg.PlayerState);
359	        f.u8(c.slot);
360	        f.u8(ctrl); f.u8(flag); f.u8(sel);
361	        f.f32(x); f.f32(y);
362	        if (flag & 4) { f.f32(vx); f.f32(vy); }
363	        this.broadcastAt(x, y, AOI_PLAYER, f.finish(), c);
364	        return;
365	      }
366	      case Msg.TileBatch: {
367	        if (c.state < 10) return;
368	        const ops = readTileBatch(r);
369	        // 破坏保护（服务端权威）：非房主整包拒绝——原版无此机制，属我们 v3 房间制策略
370	        if (this.opts.protectTiles && !c.isHost) {
371	          // 拒绝并回发权威快照纠正（对齐原版 SendTileSquare 纠正语义，防客户端乐观预测残留）
372	          for (const o of ops.slice(0, 8)) this.send(c, this.correctionFrame(o.x, o.y));
373	          return;
374	        }
375	        // review S4：先滤掉越界/值域非法的 op 再应用与广播——原实现 apply 跳过但
376	        // broadcast 原样转发，非法 tile id 会污染其他客户端世界（TILE_DEFS[type] undefined）
377	        const valid = ops.filter((o) =>
378	          o.x >= 0 && o.y >= 0 && o.x < this.st.w && o.y < this.st.h
379	          && !(o.a === TileOpAction.SetTile && o.v >= TILE_DEFS.length)
380	          && !(o.a === TileOpAction.SetWall && o.v > 366)
381	          && !(o.a === TileOpAction.SetSlope && o.v > 4));
382	        if (!valid.length) return;
383	        this.applyTileOps(valid);
384	        this.broadcast(writeTileBatch(valid), c);
385	        return;
386	      }
387	      case Msg.NetModules: {
388	        const moduleId = r.u16();
389	        if (moduleId === NetModule.Text) {
390	          const text = r.str();
391	          if (!text || text.length > 200) return;
392	          const f = new NetWriter(Msg.NetModules);
393	          f.u16(NetModule.Text);
394	          f.u8(c.slot);
395	          f.str(text);
396	          f.u8(255); f.u8(220); f.u8(120);
397	          this.broadcast(f.finish());
398	        }
399	        return;
400	      }
401	      case Msg.RequestChestOpen: {
402	        if (c.state < 10) return;
403	        // msg31（原版 RequestChestOpen）：按锚点找箱 → 全量下发内容（msg32）。
404	        // 访客本地 chests 为空（msg7 不传），内容唯一权威 = 服务器（存档带入）
405	        const x = r.i32(), y = r.i32();
406	        // 邻域匹配（±1 tile）：客户端点击箱体任意一格都能命中锚点（findChestNear 语义）
407	        const idx = this.world.chests.findIndex((ch) => Math.abs(ch.x - x) <= 1 && Math.abs(ch.y - y) <= 1);
408	        if (idx < 0) return;
409	        this.send(c, this.chestFrame(idx, -1));
410	        return;
411	      }
412	      case Msg.SyncChestItem: {
413	        if (c.state < 10) return;
414	        // msg32 上行（槽位编辑）：protectItems 非房主整包拒绝 + 权威内容回发纠正
415	        const chestIdx = r.u16();
416	        const cx = r.i32(), cy = r.i32();
417	        void cx; void cy;
418	        const n = r.u16();
419	        const slots: Array<{ slot: number; itemId: number; stack: number }> = [];
420	        for (let i = 0; i < n; i++) {
421	          const slot = r.u8(), itemId = r.u16(), stack = r.u16();
422	          if (slot < 10 && itemId < ITEM_DEFS.length) slots.push({ slot, itemId, stack: Math.min(stack, ITEM_DEFS[itemId]?.maxStack ?? 9999) });
423	        }
424	        const chest = this.world.chests[chestIdx];
425	        if (!chest) return;
426	        if (this.opts.protectItems && !c.isHost) {
427	          this.send(c, this.chestFrame(chestIdx, -1)); // 权威纠正
428	          return;
429	        }
430	        for (const s of slots) chest.items[s.slot] = s.itemId ? { id: s.itemId, stack: s.stack } : null;
431	        if (slots.length) {
432	          this.roomStats.chestEdits++; // P3.1 脏标记（review S1：箱子编辑不走 tileOps）
433	          this.broadcast(this.chestFrame(chestIdx, slots[0].slot, c), c);
434	        }
435	        return;
436	      }
437	      case Msg.PlayerLifeMana: {
438	        if (c.state < 10) return;
439	        // msg16（原版 PlayerLifeMana）：客户端权威 HP，服务器中继（覆写权威 slot）
440	        r.u8();
441	        const hp = r.i16(), maxHp = r.i16();
442	        this.broadcast(new NetWriter(Msg.PlayerLifeMana).u8(c.slot).i16(hp).i16(maxHp).finish(), c);
443	        return;
444	      }
445	      case Msg.SyncNPC: {
446	        // msg23：NPC 快照仅权威源（现=房主，见 npcAuthority）发出。C→S 全量格式不变；
447	        // S→C v4 短码格式（每条 1B flags：bit0=含 key 全量 / bit1=boss）+ AOI 逐接收端过滤
448	        if (c.state < 10 || !this.npcAuthority(c)) return;
449	        const n = r.u16();
450	        if (n > 64) return;
451	        type Entry = { netId: number; code: number; key: string; x: number; y: number; vx: number; vy: number; hp: number; maxHp: number; animT: number; boss: boolean };
452	        const entries: Entry[] = [];
453	        for (let i = 0; i < n; i++) {
454	          const netId = r.u32();
455	          const key = r.str();
456	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
457	          const hp = r.i16(), maxHp = r.i16(), animT = r.u16(), flags = r.u8();
458	          // P1.2 短码分配（表满 60000 清表：全房 npcKnown 一并失效，全量兜底自动重建）
459	          let code = this.npcCodes.get(netId);
460	          if (code === undefined) {
461	            if (this.npcCodes.size >= 60000) {
462	              this.npcCodes.clear();
463	              for (const cl of this.clients) cl.npcKnown.clear();
464	            }
465	            this.npcCodeSeq = (this.npcCodeSeq + 1) & 0xffff;
466	            if (this.npcCodeSeq === 0) this.npcCodeSeq = 1;
467	            code = this.npcCodeSeq;
468	            this.npcCodes.set(netId, code);
469	          }
470	          entries.push({ netId, code, key: key.slice(0, 64), x, y, vx, vy, hp, maxHp, animT, boss: !!(flags & 1) });
471	        }
472	        const now = Date.now();
473	        // 逐接收端过滤；全员全量时走快速路径（单帧广播，零重编码——簇拥场景的常态）
474	        const targets: Array<{ rc: RoomClient; picked: Entry[] }> = [];
475	        let allFull = true;
476	        for (const rc of this.clients) {
477	          if (rc === c || rc.state < 10) continue;
478	          if (now - rc.lastAoiPrune > AOI_PRUNE_MS) {
479	            rc.lastAoiPrune = now;
480	            for (const [id, t] of rc.aoiNpc) if (now - t > AOI_PRUNE_MS) rc.aoiNpc.delete(id);
481	            for (const [cd, t] of rc.npcKnown) if (now - t > AOI_PRUNE_MS) rc.npcKnown.delete(cd);
482	          }
483	          if (this.aoiBlind(rc, now)) { this.roomStats.stalePos++; continue; } // 盲端：跳过（见 aoiBlind）
484	          const picked: Entry[] = [];
485	          for (const e of entries) {
486	            const dist = Math.max(Math.abs(rc.lastX - e.x), Math.abs(rc.lastY - e.y));
487	            const wasVisible = rc.aoiNpc.has(e.netId);
488	            if (dist > AOI_ENTITY * AOI_OUT_FACTOR) {
489	              if (wasVisible) rc.aoiNpc.delete(e.netId); // 出滞回外径 → 停发（客户端 300 tick 超时清除傀儡）
490	              continue;
491	            }
492	            if (dist > AOI_ENTITY && !wasVisible) continue; // 内外径滞回带且未可见：不入视野
493	            rc.aoiNpc.set(e.netId, now);
494	            picked.push(e);
495	          }
496	          if (!picked.length) continue;
497	          if (picked.length < entries.length) allFull = false;
498	          targets.push({ rc, picked });
499	        }
500	        if (!targets.length) return;
501	        if (allFull) {
502	          // 快速路径：每个目标都收全量条目——但短码标记仍按接收端（known 与否），仅当
503	          // 全员都已知全部 code 时帧内容才一致，此时单帧广播
504	          let allKnown = true;
505	          for (const t of targets) {
506	            for (const e of t.picked) {
507	              if (!t.rc.npcKnown.has(e.code)) { allKnown = false; break; }
508	            }
509	            if (!allKnown) break;
510	          }
511	          if (allKnown) {
512	            const f = new NetWriter(Msg.SyncNPC);
513	            f.u16(entries.length);
514	            for (const e of entries) {
515	              f.u8(e.boss ? 2 : 0); f.u16(e.code);
516	              f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
517	              f.i16(e.hp); f.i16(e.maxHp); f.u16(e.animT);
518	            }
519	            const frame = f.finish();
520	            // 已知集刷新同样晚于 send（与慢路径一致；丢帧只影响 30s 过期时机，自愈）
521	            for (const t of targets) {
522	              if (this.send(t.rc, frame, 1)) {
523	                for (const e of t.picked) t.rc.npcKnown.set(e.code, now);
524	              }
525	            }
526	            return;
527	          }
528	        }
529	        for (const { rc, picked } of targets) {
530	          const out = new NetWriter(Msg.SyncNPC);
531	          out.u16(picked.length);
532	          const learned: number[] = []; // 本帧首次全量下发的 code——仅在入队成功后标记 known
533	          for (const e of picked) {
534	            const known = rc.npcKnown.has(e.code);
535	            out.u8((known ? 0 : 1) | (e.boss ? 2 : 0));
536	            if (known) out.u16(e.code);
537	            else { out.u32(e.netId); out.u16(e.code); out.str(e.key); learned.push(e.code); }
538	            out.f32(e.x); out.f32(e.y); out.f32(e.vx); out.f32(e.vy);
539	            out.i16(e.hp); out.i16(e.maxHp); out.u16(e.animT);
540	          }
541	          // review S2：known 标记必须晚于 send——prio=1 帧被背压丢弃时若已标记，
542	          // 该 NPC 之后只发短码、客户端静默丢弃 → 视野内 NPC 永久隐身。丢帧则不标记，下批重发全量
543	          if (this.send(rc, out.finish(), 1)) {
544	            for (const code of learned) rc.npcKnown.set(code, now);
545	            for (const e of picked) if (rc.npcKnown.has(e.code)) rc.npcKnown.set(e.code, now);
546	          }
547	        }
548	        return;
549	      }
550	      case Msg.SyncItem: {
551	        if (c.state < 10) return;
552	        // msg21：掉落物 spawn/take/despawn 中继（netId 已含拥有者 slot 前缀）
553	        const netId = r.u32();
554	        const op = r.u8();
555	        const f = new NetWriter(Msg.SyncItem);
556	        f.u32(netId); f.u8(op);
557	        if (op === 0) {
558	          const key = r.str();
559	          const stack = r.u16();
560	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
561	          if (!key || key.length > 64 || stack === 0) return;
562	          f.str(key); f.u16(stack);
563	          f.f32(x); f.f32(y); f.f32(vx); f.f32(vy);
564	        } else if (op > 2) return;
565	        this.broadcast(f.finish(), c);
566	        return;
567	      }
568	      case Msg.SyncProjectile: {
569	        if (c.state < 10) return;
570	        // msg27：弹幕快照双向中继（各自弹幕互播）+ P1.1 AOI 滞回过滤；kind>4 整包丢弃防脏流
571	        const n = r.u16();
572	        if (n > 64) return;
573	        type PEntry = { netId: number; kind: number; tag: string; dmg: number; aux: number; x: number; y: number; vx: number; vy: number };
574	        const entries: PEntry[] = [];
575	        for (let i = 0; i < n; i++) {
576	          const netId = r.u32();
577	          const kind = r.u8();
578	          const tag = r.str();
579	          const dmg = r.i16(), aux = r.i16();
580	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
581	          // v5：kind bit7=hostile（原版 Projectile.hostile 位）原样透传；低 3 位 >4 视为脏数据丢本条
582	          if ((kind & 0x7f) > 4) continue;
583	          entries.push({ netId, kind, tag: tag.slice(0, 32), dmg, aux, x, y, vx, vy });
584	        }
585	        const now = Date.now();
586	        // 逐接收端过滤 + 全员全量快速路径（msg27 无短码，全量时帧内容一致 → 单帧广播零重编码）
587	        const targets: Array<{ rc: RoomClient; picked: PEntry[] }> = [];
588	        let allFull = true;
589	        for (const rc of this.clients) {
590	          if (rc === c || rc.state < 10) continue;
591	          if (now - rc.lastAoiPrune > AOI_PRUNE_MS) {
592	            rc.lastAoiPrune = now;
593	            for (const [id, t] of rc.aoiProj) if (now - t > AOI_PRUNE_MS) rc.aoiProj.delete(id);
594	          }
595	          if (this.aoiBlind(rc, now)) { this.roomStats.stalePos++; continue; } // 盲端：跳过
596	          const picked: PEntry[] = [];
597	          for (const e of entries) {
598	            const dist = Math.max(Math.abs(rc.lastX - e.x), Math.abs(rc.lastY - e.y));
599	            const wasVisible = rc.aoiProj.has(e.netId);
600	            if (dist > AOI_ENTITY * AOI_OUT_FACTOR) {
601	              if (wasVisible) rc.aoiProj.delete(e.netId);
602	              continue;
603	            }
604	            if (dist > AOI_ENTITY && !wasVisible) continue;
605	            rc.aoiProj.set(e.netId, now);
606	            picked.push(e);
607	          }
608	          if (!picked.length) continue;
609	          if (picked.length < entries.length) allFull = false;
610	          targets.push({ rc, picked });
611	        }
612	        if (!targets.length) return;
613	        if (allFull) {
614	          const f = new NetWriter(Msg.SyncProjectile);
615	          f.u16(entries.length);
616	          for (const e of entries) {
617	            f.u32(e.netId); f.u8(e.kind); f.str(e.tag);
618	            f.i16(e.dmg); f.i16(e.aux);
619	            f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
620	          }
621	          const frame = f.finish();
622	          for (const t of targets) this.send(t.rc, frame, 1);
623	          return;
624	        }
625	        for (const { rc, picked } of targets) {
626	          const f = new NetWriter(Msg.SyncProjectile);
627	          f.u16(picked.length);
628	          for (const e of picked) {
629	            f.u32(e.netId); f.u8(e.kind); f.str(e.tag);
630	            f.i16(e.dmg); f.i16(e.aux);
631	            f.f32(e.x); f.f32(e.y); f.f32(e.vx); f.f32(e.vy);
632	          }
633	          this.send(rc, f.finish(), 1);
634	        }
635	        return;
636	      }
637	      case Msg.StrikeNPC: {
638	        if (c.state < 10) return;
639	        // msg42：访客打击 → 定向转发权威结算端（strikeTarget）；dmg 钳 9999 防刷
640	        const netId = r.u32();
641	        const dmg = r.i16();
642	        const kbx = r.f32(), kby = r.f32();
643	        const target = this.strikeTarget();
644	        if (target) {
645	          this.send(target, new NetWriter(Msg.StrikeNPC).u32(netId).i16(Math.max(-32768, Math.min(9999, dmg))).f32(kbx).f32(kby).finish());
646	        }
647	        return;
648	      }
649	      case Msg.Ping: {
650	        const ts = r.f64();
651	        this.send(c, new NetWriter(Msg.Ping).f64(ts).finish());
652	        return;
653	      }
654	      default:
655	        return;
656	    }
657	  }
658	
659	  /** 房间策略下发（RoomPolicy）：客户端据此门禁 UI。v4 尾部追加 u16 maxPlayers */
660	  sendPolicy(c: RoomClient) {
661	    this.send(c, new NetWriter(Msg.RoomPolicy)
662	      .str(this.opts.code)
663	      .str(this.opts.name)
664	      .bool(c.isHost)
665	      .bool(this.opts.protectTiles)
666	      .bool(this.opts.protectItems)
667	      .u16(this.opts.maxPlayers)
668	      .finish());
669	  }
670	
671	  /** 箱子内容帧（msg32）。full=-1 全量下发；否则只带变更槽（最小帧）。
672	   *  广播方向除编辑者本人——编辑者本地已生效（乐观 UI） */
673	  chestFrame(chestIdx: number, full: number, except?: RoomClient): Uint8Array {
674	    const chest = this.world.chests[chestIdx];
675	    const w = new NetWriter(Msg.SyncChestItem);
676	    w.u16(chestIdx);
677	    w.i32(chest.x); w.i32(chest.y);
678	    const from = full === -1 ? 0 : full;
679	    const to = full === -1 ? chest.items.length : from + 1;
680	    w.u16(to - from);
681	    for (let i = from; i < to; i++) {
682	      const it = chest.items[i];
683	      w.u8(i);
684	      w.u16(it?.id ?? 0);
685	      w.u16(it?.stack ?? 0);
686	    }
687	    void except;
688	    return w.finish();
689	  }
690	
691	  /** 权威 tile 快照纠正（单格） */
692	  private correctionFrame(x: number, y: number): Uint8Array {
693	    const ops: TileOp[] = [];
694	    if (x >= 0 && y >= 0 && x < this.st.w && y < this.st.h) {
695	      const i = this.st.idx(x, y);
696	      ops.push({ a: TileOpAction.SetTile, x, y, v: this.st.type[i], fx: this.st.frameX[i], fy: this.st.frameY[i] });
697	    }
698	    return writeTileBatch(ops);
699	  }
700	
701	  disconnect(c: RoomClient) {
702	    this.clients.delete(c);
703	    // 认领了 session 但没完成 Hello 就断线 → 释放认领（重试窗口内可再连；超时回调兜底释放 slot）
704	    if (c.state < 1 && c.claimedSession) {
705	      const s = this.sessions.get(c.session);
706	      if (s) s.claimed = false;
707	      c.claimedSession = false;
708	    }
709	    if (c.slot >= 0) {
710	      // v3 重连：在局玩家断开 → session 保留 60s，slot 占位防新人顶号；过期释放
711	      if (c.state >= 10 && c.session) {
712	        this.sessions.set(c.session, {
713	          slot: c.slot, name: c.name, appearance: c.appearance,
714	          until: Date.now() + 60_000, claimed: false,
715	        });
716	        const sess = c.session;
717	        const slot = c.slot;
718	        setTimeout(() => {
719	          // 已被 resumeSession 消费（重连成功）则不再动；超时未归 → 释放占位
720	          if (!this.sessions.has(sess)) return;
721	          this.sessions.delete(sess);
722	          this.slotUsed[slot] = false;
723	        }, 61_000).unref?.();
724	      } else {
725	        this.slotUsed[c.slot] = false;
726	      }
727	      this.broadcast(new NetWriter(Msg.PlayerActive).u8(c.slot).bool(false).str('').finish());
728	      // 离开公告（原版 NetMessage.cs:2950-2954：先广播 14 再 Lang.mp[20]，含强制退出/掉线）
729	      this.broadcast(new NetWriter(Msg.NetModules).u16(NetModule.JoinLeave).u8(c.slot).bool(false).finish());
730	    }
731	    if (c.isHost) this.hostJoined = false;
732	  }
733	
734	  /** 断线重连识别（index.ts 从 URL ?session= 注入）：命中 → 复位 slot/身份，Hello 跳过分配。
735	   *  认领制：只标记 claimed（防并发双认领），**不删条目**——条目在 Hello 成功时消费；
736	   *  认领后断线由 disconnect 释放认领 */
737	  resumeSession(c: RoomClient, session: string): boolean {
738	    const s = this.sessions.get(session);
739	    if (!s || s.until <= Date.now() || s.claimed) return false;
740	    s.claimed = true;
741	    c.claimedSession = true;
742	    c.resumedSlot = s.slot;
743	    c.name = s.name;
744	    c.appearance = s.appearance;
745	    c.session = session;
746	    return true;
747	  }
748	
749	  // ---- 世界数据帧（msg7）：对齐 v1 字段集 ----
750	  worldDataFrame(): Uint8Array {
751	    const w = new NetWriter(Msg.WorldData);
752	    w.f64(this.world.clock.timeOfDay);
753	    w.u32(this.world.clock.dayCount);
754	    w.u16(this.st.w); w.u16(this.st.h);
755	    w.i32(this.world.spawnX); w.i32(this.world.spawnY);
756	    w.f32(this.world.groundLevel); w.f32(this.world.rockLevel); w.f32(this.world.lavaLine);
757	    w.i32(this.world.seed);
758	    w.str(this.world.name);
759	    w.bool(this.world.crimson);
760	    w.i32(this.world.dungeonX); w.i32(this.world.dungeonY); w.i32(this.world.jungleX);
761	    const keys = Object.keys(this.world.flags);
762	    w.u16(keys.length);
763	    for (const k of keys) { w.str(k); w.bool(!!this.world.flags[k]); }
764	    return w.finish();
765	  }
766	
767	  // ---- section 流式（出生点 5×5 条带，strip 粒度兴趣管理） ----
768	  sendStrips(c: RoomClient, cx: number, cy: number) {
769	    const st = this.st;
770	    const strips: Array<{ x0: number; y0: number }> = [];
771	    const sx = Math.floor(cx / STRIP_W), sy = Math.floor(cy / STRIP_H);
772	    for (let dy = -2; dy <= 2; dy++) {
773	      for (let dx = -2; dx <= 2; dx++) {
774	        const x0 = (sx + dx) * STRIP_W, y0 = (sy + dy) * STRIP_H;
775	        if (x0 >= 0 && y0 >= 0 && x0 < st.w && y0 < st.h) strips.push({ x0, y0 });
776	      }
777	    }
778	    const fresh = strips.filter((s) => !c.sentStrips.has(`${s.x0},${s.y0}`));
779	    this.send(c, new NetWriter(Msg.StatusText).u16(fresh.length).finish());
780	    for (const s of fresh) {
781	      c.sentStrips.add(`${s.x0},${s.y0}`);
782	      // P2.1 section 编码缓存：命中直发（LRU 提到队尾）；miss 编码入缓存
783	      const key = `${s.x0},${s.y0}`;
784	      let frame = this.stripCache.get(key);
785	      if (frame) {
786	        this.stripCache.delete(key);
787	        this.stripCache.set(key, frame);
788	        this.roomStats.stripHit++;
789	      } else {
790	        frame = encodeStrip(st, { x0: s.x0, y0: s.y0, w: Math.min(STRIP_W, st.w - s.x0), h: Math.min(STRIP_H, st.h - s.y0) });
791	        this.stripCache.set(key, frame);
792	        this.stripCacheBytes += frame.length;
793	        this.stripCacheEvict();
794	        this.roomStats.stripMiss++;
795	      }
796	      this.send(c, frame);
797	    }
798	  }
799	
800	  applyTileOps(ops: TileOp[]) {
801	    const st = this.st;
802	    for (const o of ops) {
803	      if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
804	      // S5 值域校验
805	      if (o.a === TileOpAction.SetTile && o.v >= TILE_DEFS.length) continue;
806	      if (o.a === TileOpAction.SetWall && o.v > 366) continue;
807	      if (o.a === TileOpAction.SetSlope && o.v > 4) continue;
808	      // P2.1：任何落格修改都使其所在条带缓存失效（按条带原点归一化）
809	      {
810	        const sk = `${Math.floor(o.x / STRIP_W) * STRIP_W},${Math.floor(o.y / STRIP_H) * STRIP_H}`;
811	        const sf = this.stripCache.get(sk);
812	        if (sf !== undefined) { this.stripCache.delete(sk); this.stripCacheBytes -= sf.length; }
813	      }
814	      this.roomStats.tileOps++;
815	      switch (o.a) {
816	        case TileOpAction.SetTile:
817	          st.setTileSilent(o.x, o.y, o.v, o.fx, o.fy);
818	          // 箱子 tile 被清除/替换 → 同步清除权威 chests 条目（防陈旧条目被 msg31
819	          // 再次开出 = 物品复制；房主 dumpChest 的掉落已走 msg21 广播）
820	          if (o.v !== CHEST_TILE_ID) {
821	            const ci = this.world.chests.findIndex((ch) => Math.abs(ch.x - o.x) <= 1 && Math.abs(ch.y - o.y) <= 1);
822	            if (ci >= 0) this.world.chests.splice(ci, 1);
823	          }
824	          break;
825	        case TileOpAction.SetWall: st.setWallSilent(o.x, o.y, o.v); break;
826	        case TileOpAction.SetHalfBrick: st.half[st.idx(o.x, o.y)] = o.v ? 1 : 0; break;
827	        case TileOpAction.SetSlope: st.slope[st.idx(o.x, o.y)] = o.v; break;
828	        case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
829	        case TileOpAction.SetWire: st.setWireSilent(o.x, o.y, o.v); break;
830	      }
831	    }
832	  }
833	
834	  newClient(ws: WebSocket, urlToken = ''): RoomClient {
835	    const c: RoomClient = {
836	      ws, parser: new FrameParser(), slot: -1, state: 0, name: '?',
837	      appearance: '{}', lastSeen: 0, isHost: false, sentStrips: new Set(),
838	      session: '', resumedSlot: -1, claimedSession: false,
839	      lastX: -1e9, lastY: -1e9, lastPosAt: 0,
840	      aoiNpc: new Map(), aoiProj: new Map(), npcKnown: new Map(), lastAoiPrune: 0,
841	      outbox: [],
842	      stats: { inBytes: 0, outBytes: 0, bufferedMax: 0, sendDrops: 0, lowDrops: 0 },
843	      items: {
844	        inv: Array(INV_SYNC_SIZES[0]).fill(null),
845	        armor: Array(INV_SYNC_SIZES[1]).fill(null),
846	        dye: Array(INV_SYNC_SIZES[2]).fill(null),
847	      },
848	    };
849	    if (urlToken) c.urlToken = urlToken;
850	    this.clients.add(c);
851	    return c;
852	  }
853	}
854	

```


---

## 🤖 Assistant · 2026-08-12T05:57:54.358Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read ClientNet.ts and Game.ts net sections. Let me read ClientNet.ts fully and grep Game.ts for net-related sections.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:57:54.449Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/ClientNet.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:57:54.586Z

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
410	        // bit1=boss；否则仅 u16 codeId（查本端 codeId→netId/key 表）。
411	        // 未知短码：**先把本条剩余字段读完再丢弃**——continue 前不消费会让读指针错位，
412	        // 毒化整条连接（review C1）；自愈靠 ≤2s 全量兜底重发
413	        const n = r.u16();
414	        const snaps: NpcSnap[] = [];
415	        for (let i = 0; i < n; i++) {
416	          const eflags = r.u8();
417	          let netId = 0, key = '';
418	          if (eflags & 1) {
419	            netId = r.u32();
420	            const code = r.u16();
421	            key = r.str();
422	            this.npcCodes.set(code, { netId, key });
423	          } else {
424	            const code = r.u16();
425	            const e = this.npcCodes.get(code);
426	            netId = e?.netId ?? 0;
427	            key = e?.key ?? '';
428	          }
429	          const x = r.f32(), y = r.f32(), vx = r.f32(), vy = r.f32();
430	          const hp = r.i16(), maxHp = r.i16(), animT = r.u16();
431	          if (!netId) continue; // 未知短码：字段已消费，仅丢弃本条快照
432	          snaps.push({ netId, key, x, y, vx, vy, hp, maxHp, animT, flags: eflags & 2 ? 1 : 0 });
433	        }
434	        this.hooks.onNpcSnapshot?.(snaps);
435	        return;
436	      }
437	      case Msg.SyncItem: {
438	        const netId = r.u32();
439	        const op = r.u8() as 0 | 1 | 2;
440	        let key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0;
441	        if (op === 0) {
442	          key = r.str(); stack = r.u16();
443	          x = r.f32(); y = r.f32(); vx = r.f32(); vy = r.f32();
444	        }
445	        this.hooks.onItemOp?.({ op, netId, key, stack, x, y, vx, vy });
446	        return;
447	      }
448	      case Msg.SyncProjectile: {
449	        const n = r.u16();
450	        const snaps: ProjSnap[] = [];
451	        for (let i = 0; i < n; i++) {
452	          snaps.push({
453	            netId: r.u32(), kind: r.u8(), tag: r.str(),
454	            dmg: r.i16(), aux: r.i16(),
455	            x: r.f32(), y: r.f32(), vx: r.f32(), vy: r.f32(),
456	          });
457	        }
458	        this.hooks.onProjectileSync?.(snaps);
459	        return;
460	      }
461	      case Msg.StrikeNPC: {
462	        const netId = r.u32();
463	        const dmg = r.i16();
464	        const kbx = r.f32(), kby = r.f32();
465	        this.hooks.onStrike?.(netId, dmg, kbx, kby);
466	        return;
467	      }
468	      case Msg.PlayerLifeMana: {
469	        const slot = r.u8();
470	        const hp = r.i16(), maxHp = r.i16();
471	        if (slot !== this.mySlot) this.hooks.onHp?.(slot, hp, maxHp);
472	        return;
473	      }
474	      case Msg.Ping:
475	        return; // 忽略回显
476	      default:
477	        return; // 未知跳过（对齐原版）
478	    }
479	  }
480	
481	  /** Game 侧设置运行期世界引用（时间对齐用） */
482	  gameWorld: World | null = null;
483	
484	  private readWorldData(r: NetReader): World {
485	    const time = r.f64();
486	    const dayCount = r.u32();
487	    const w = r.u16(), h = r.u16();
488	    const spawnX = r.i32(), spawnY = r.i32();
489	    const groundLevel = r.f32(), rockLevel = r.f32(), lavaLine = r.f32();
490	    const seed = r.i32();
491	    const name = r.str();
492	    const crimson = r.bool();
493	    const dungeonX = r.i32(), dungeonY = r.i32(), jungleX = r.i32();
494	    const flagCount = r.u16();
495	    const flags: Record<string, boolean> = {};
496	    for (let i = 0; i < flagCount; i++) flags[r.str()] = r.bool();
497	    const world = new WorldCtor(w, h, seed, name);
498	    world.clock.timeOfDay = time;
499	    world.clock.dayCount = dayCount;
500	    world.spawnX = spawnX; world.spawnY = spawnY;
501	    world.groundLevel = groundLevel; world.rockLevel = rockLevel; world.lavaLine = lavaLine;
502	    world.crimson = crimson;
503	    world.dungeonX = dungeonX; world.dungeonY = dungeonY; world.jungleX = jungleX;
504	    Object.assign(world.flags, flags);
505	    // 请求出生点周围 section（对齐原版 msg8）
506	    this.send(new NetWriter(Msg.SpawnTileData).i32(spawnX).i32(spawnY).finish());
507	    return world;
508	  }
509	
510	  // ================= tile 上报（TileStore.netReporter → 队列 → 每 tick 冲洗） =================
511	
512	  /** TileStore.netReporter 注入点；netSuppress 期间（应用远端操作）不收集 */
513	  reportTileOp(op: TileOp) {
514	    if (!this.active) return;
515	    if (this.tileQueue.length >= 256) {
516	      // R4：超限不再静默丢（静默分叉不可恢复）——告警后仍丢但留下痕迹
517	      if (!this._overflowWarned) {
518	        this._overflowWarned = true;
519	        console.warn('[net] tile 上报队列溢出（单 tick >256 op），丢弃后续——本地与远端将分叉');
520	      }
521	      return;
522	    }
523	    this.tileQueue.push(op);
524	  }
525	  private _overflowWarned = false;
526	
527	  /** Game 每 fixedUpdate 调用：冲洗 tile 队列 + 玩家状态上报（变化驱动 + 66ms 节流） */
528	  tick() {
529	    if (!this.active) return;
530	    this.syncInventory(performance.now());
531	    this.syncHp();
532	    this.flushPending(); // P1.3 msg21 合帧冲洗
533	    if (this.tileQueue.length) {
534	      // 每包最多 64 op（防超帧）
535	      const batch = this.tileQueue.splice(0, 64);
536	      const w = new NetWriter(Msg.TileBatch);
537	      w.u16(batch.length);
538	      for (const o of batch) {
539	        w.u8(o.a);
540	        w.i32(o.x); w.i32(o.y);
541	        w.u16(o.v & 0xffff);
542	        if (o.a === TileOpAction.SetTile) { w.u16(o.fx); w.u16(o.fy); }
543	      }
544	      this.send(w.finish());
545	    }
546	    this.sendPlayerState();
547	  }
548	
549	  private sendPlayerState() {
550	    // v2 布局（对齐原版 msg13）：控制位 + position(碰撞盒左上) + velocity。
551	    // 远端据此跑本地物理 → 有移动过程；位置差由接收端 netOffset 平滑（瞬移消失）
552	    const p = this.game.player as unknown as {
553	      x: number; y: number; vx: number; vy: number; facing: number; dead: boolean;
554	      inputX: number; inputJump: boolean; inputDown: boolean; inputUp: boolean;
555	      inv: { heldItem(): { id: number } | null };
556	    };
557	    const inp = (this.game as { input?: { mouseDown: boolean; rightDown: boolean } }).input;
558	    // ctrlBits: [0]up [1]down [2]left [3]right [4]jump [5]useItem [6]direction（原版 case 13）
559	    // useItem = 左键按住（原版 controlUseItem；放置/右键交互不计）
560	    const ctrl = (p.inputUp ? 1 : 0) | (p.inputDown ? 2 : 0)
561	      | (p.inputX < 0 ? 4 : 0) | (p.inputX > 0 ? 8 : 0)
562	      | (p.inputJump ? 16 : 0)
563	      | (inp?.mouseDown && !inp.rightDown ? 32 : 0)
564	      | (p.facing > 0 ? 64 : 0);
565	    // selectedItem = 快捷栏槽位索引 0-9（原版 NetMessage.cs:471 语义；v1 误发物品 id）
566	    const sel = (p.inv as unknown as { selected: number }).selected & 0xff;
567	    // 控制位变化即时发（原版 TrySyncingInput Player.cs:6484：任一 control/selectedItem
568	    // 变化立刻 SendData(13)）——原地起跳这类"位置未动"的操作不再等静止心跳
569	    const ctrlChanged = ctrl !== this.lastSentCtrl || sel !== this.lastSentSel || p.dead !== this.lastSentDead;
570	    const now = performance.now();
571	    const moved = Math.abs(p.x - this.lastSentPos.x) > 1 || Math.abs(p.y - this.lastSentPos.y) > 1;
572	    if (!ctrlChanged) {
573	      if (!moved && now - this.lastStateSent < 1000) return; // 静止 1s 心跳（原版 %420 全量兜底的加密版）
574	      if (now - this.lastStateSent < 66) return;             // 位置驱动节流 ≥66ms（≈15Hz）
575	    }
576	    this.lastStateSent = now;
577	    this.lastSentPos = { x: p.x, y: p.y };
578	    this.lastSentCtrl = ctrl;
579	    this.lastSentSel = sel;
580	    this.lastSentDead = p.dead;
581	    // flagBits: [2]hasVelocity [6]ghost
582	    const flag = 4 | (p.dead ? 64 : 0);
583	    this.send(new NetWriter(Msg.PlayerState)
584	      .u8(this.mySlot)
585	      .u8(ctrl).u8(flag)
586	      .u8(sel)
587	      .f32(p.x).f32(p.y)
588	      .f32(p.vx).f32(p.vy)
589	      .finish());
590	  }
591	
592	  private lastSentCtrl = -1;
593	  private lastSentSel = -1;
594	  private lastSentDead = false;
595	
596	  // ================= 箱子同步（msg31/32，服务器权威） =================
597	
598	  /** 请求打开箱子（interactAt 未命中本地 chests 时——访客本地无箱数据） */
599	  requestChestOpen(x: number, y: number) {
600	    this.send(new NetWriter(Msg.RequestChestOpen).i32(x).i32(y).finish());
601	  }
602	
603	  /** 槽位编辑上报（每槽一条消息；服务器权威+广播，编辑者本地已乐观生效） */
604	  sendChestSlot(chestIdx: number, x: number, y: number, slot: number, itemId: number, stack: number) {
605	    const w = new NetWriter(Msg.SyncChestItem);
606	    w.u16(chestIdx); w.i32(x); w.i32(y);
607	    w.u16(1);
608	    w.u8(slot); w.u16(itemId); w.u16(stack);
609	    this.send(w.finish());
610	  }
611	
612	  /** 本地登记的箱子 → 同步槽位号（Game 注册；diff 轮询用） */
613	  chestIndexByPos = new Map<string, number>();
614	
615	  private applyRemoteChest(r: NetReader) {
616	    const chestIdx = r.u16();
617	    const x = r.i32(), y = r.i32();
618	    const n = r.u16();
619	    const items: Array<{ id: number; stack: number } | null> = [];
620	    for (let i = 0; i < n; i++) {
621	      const slot = r.u8(), itemId = r.u16(), stack = r.u16();
622	      items[slot] = itemId ? { id: itemId, stack } : null;
623	    }
624	    this.hooks.onChestSync?.(chestIdx, x, y, items);
625	  }
626	
627	  /** 外观变更后重发 SyncPlayer（进游戏后 applyCharacter 调用——初始两发都在外观应用前） */
628	  resendAppearance() {
629	    if (!this.active || this.mySlot < 0) return;
630	    const p = this.game.player as { appearance?: unknown } | undefined;
631	    if (p?.appearance) {
632	      this.send(new NetWriter(Msg.SyncPlayer).u8(this.mySlot).str(JSON.stringify(p.appearance)).finish());
633	    }
634	  }
635	
636	  // ================= 远端 tile 应用（回环抑制 + 事件链触发） =================
637	
638	  private applyRemote(ops: TileOp[]) {
639	    const st = this.gameWorld?.store;
640	    if (!st) return;
641	    st.netSuppress = true;
642	    try {
643	      for (const o of ops) {
644	        if (o.x < 0 || o.y < 0 || o.x >= st.w || o.y >= st.h) continue;
645	        switch (o.a) {
646	          case TileOpAction.SetTile: st.setTile(o.x, o.y, o.v, o.fx, o.fy); break;
647	          case TileOpAction.SetWall: st.setWall(o.x, o.y, o.v); break;
648	          case TileOpAction.SetHalfBrick: st.setHalfBrick(o.x, o.y, !!o.v); break;
649	          case TileOpAction.SetSlope: st.setSlope(o.x, o.y, o.v); break;
650	          case TileOpAction.SetActuated: st.setActuated(o.x, o.y, !!o.v); break;
651	          case TileOpAction.SetWire: st.setWire(o.x, o.y, o.v); break;
652	        }
653	      }
654	    } finally {
655	      st.netSuppress = false; // R5：异常安全复位（否则 suppress 永久卡死上报）
656	    }
657	  }
658	
659	  /** 聊天发送 */
660	  sendChat(text: string) {
661	    this.send(new NetWriter(Msg.NetModules).u16(NetModule.Text).str(text).finish());
662	  }
663	
664	  // ================= v3 实体同步（msg16/21/23/27/42，房主权威+服务器中继） =================
665	
666	  /** NPC 快照（msg23） */
667	  sendNpcSnapshot(snaps: NpcSnap[]) {
668	    if (!snaps.length) return;
669	    const w = new NetWriter(Msg.SyncNPC);
670	    w.u16(snaps.length);
671	    for (const s of snaps) {
672	      w.u32(s.netId); w.str(s.key);
673	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
674	      w.i16(s.hp); w.i16(s.maxHp);
675	      w.u16(s.animT & 0xffff);
676	      w.u8(s.flags);
677	    }
678	    this.send(w.finish());
679	  }
680	
681	  /** 掉落物操作（msg21）：op 0=spawn / 1=take / 2=despawn。
682	   *  P1.3 上行合帧：入 pending 攒批（netDropSweep 每 4 tick 可能逐条几十发），
683	   *  tick() 冲洗时拼为单条 WS 消息；满 64 帧立即冲防延迟 */
684	  sendItemOp(op: 0 | 1 | 2, netId: number, key = '', stack = 0, x = 0, y = 0, vx = 0, vy = 0) {
685	    const w = new NetWriter(Msg.SyncItem);
686	    w.u32(netId); w.u8(op);
687	    if (op === 0) {
688	      w.str(key); w.u16(stack);
689	      w.f32(x); w.f32(y); w.f32(vx); w.f32(vy);
690	    }
691	    this.pendingFrames.push(w.finish());
692	    if (this.pendingFrames.length >= 64) this.flushPending();
693	  }
694	
695	  /** 冲洗 pending 合帧：多帧拼接为一条 WS 消息（§1.1 允许一 WS 消息串联多帧） */
696	  private flushPending() {
697	    if (!this.pendingFrames.length || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
698	      this.pendingFrames.length = 0;
699	      return;
700	    }
701	    let total = 0;
702	    for (const f of this.pendingFrames) total += f.length;
703	    const joined = new Uint8Array(total);
704	    let off = 0;
705	    for (const f of this.pendingFrames) { joined.set(f, off); off += f.length; }
706	    this.pendingFrames.length = 0;
707	    this.ws.send(joined);
708	  }
709	
710	  /** 弹幕快照（msg27，双向：各自弹幕互播） */
711	  sendProjectileBatch(snaps: ProjSnap[]) {
712	    if (!snaps.length) return;
713	    const w = new NetWriter(Msg.SyncProjectile);
714	    w.u16(snaps.length);
715	    for (const s of snaps) {
716	      w.u32(s.netId); w.u8(s.kind); w.str(s.tag);
717	      w.i16(s.dmg); w.i16(s.aux);
718	      w.f32(s.x); w.f32(s.y); w.f32(s.vx); w.f32(s.vy);
719	    }
720	    this.send(w.finish());
721	  }
722	
723	  /** 傀儡受击上报（msg42，访客→房主；Enemy.hurt 内经 entityNet 注入调用） */
724	  sendStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
725	    this.send(new NetWriter(Msg.StrikeNPC).u32(netId).i16(rawDmg).f32(kbx).f32(kby).finish());
726	  }
727	
728	  /** HP 上报（msg16，变化驱动 + 200ms 节流；原版客户端权威） */
729	  private lastHpSent = -1;
730	  private lastHpAt = 0;
731	  syncHp() {
732	    if (this.mySlot < 0) return;
733	    const p = this.game.player as unknown as { hp: number; maxHp: number };
734	    const now = performance.now();
735	    if (p.hp === this.lastHpSent) {
736	      if (now - this.lastHpAt < 5000) return; // 满血心跳 5s
737	    } else if (now - this.lastHpAt < 200) return;
738	    this.lastHpSent = p.hp;
739	    this.lastHpAt = now;
740	    this.send(new NetWriter(Msg.PlayerLifeMana).u8(this.mySlot).i16(p.hp).i16(p.maxHp).finish());
741	  }
742	
743	  // ================= 物品/装备同步（msg5，对齐原版 SyncPlayerItem 语义） =================
744	
745	  /** 远端玩家物品快照（Game 侧拷入 proxy.inv——手持/盔甲纸娃娃/挥舞动画渲染用） */
746	  remoteItems = new Map<number, { inv: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> }>();
747	
748	  /** 本地已同步快照（差分基准；null = 尚未全量 dump） */
749	  private sentInv: Array<Array<{ id: number; stack: number } | null>> | null = null;
750	  private invDumpPending = true; // 进房首包全量
751	  private lastInvSync = 0;
752	
753	  /** 全量 dump（进房后立即 + 外部可请求） */
754	  private sendFullInventory() {
755	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
756	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
757	    for (let c = 0; c < 3; c++) {
758	      const arr = c === 0 ? p.inv.slots : c === 1 ? p.inv.armor : p.inv.dye;
759	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
760	        entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: arr[i]?.id ?? 0, stack: arr[i]?.stack ?? 0 });
761	      }
762	    }
763	    this.send(writePlayerItems(entries));
764	    this.sentInv = [p.inv.slots.map(s => s ? { ...s } : null), p.inv.armor.map(s => s ? { ...s } : null), p.inv.dye.map(s => s ? { ...s } : null)];
765	    this.invDumpPending = false;
766	  }
767	
768	  /** 差分上报（tick 内每 250ms 调一次；原版 msg5 变化驱动逐槽发送的批量等价） */
769	  private syncInventory(now: number) {
770	    if (this.mySlot < 0) return;
771	    if (this.invDumpPending || !this.sentInv) { this.sendFullInventory(); return; }
772	    if (now - this.lastInvSync < 250) return;
773	    this.lastInvSync = now;
774	    const p = this.game.player as { inv: { slots: Array<{ id: number; stack: number } | null>; armor: Array<{ id: number; stack: number } | null>; dye: Array<{ id: number; stack: number } | null> } };
775	    const cur = [p.inv.slots, p.inv.armor, p.inv.dye];
776	    const entries: Array<ItemSyncEntry & { playerSlot: number }> = [];
777	    for (let c = 0; c < 3; c++) {
778	      const arr = cur[c];
779	      const sent = this.sentInv[c];
780	      for (let i = 0; i < arr.length && i < INV_SYNC_SIZES[c]; i++) {
781	        const a = arr[i], b = sent[i];
782	        if ((a?.id ?? 0) !== (b?.id ?? 0) || (a?.stack ?? 0) !== (b?.stack ?? 0)) {
783	          entries.push({ playerSlot: this.mySlot, container: c as ItemContainer, itemSlot: i, itemId: a?.id ?? 0, stack: a?.stack ?? 0 });
784	          sent[i] = a ? { ...a } : null;
785	        }
786	      }
787	    }
788	    if (entries.length) this.send(writePlayerItems(entries));
789	  }
790	
791	  private applyRemoteItems(entries: Array<ItemSyncEntry & { playerSlot: number }>) {
792	    for (const e of entries) {
793	      if (e.container > 2 || e.itemSlot >= INV_SYNC_SIZES[e.container]) continue;
794	      let bag = this.remoteItems.get(e.playerSlot);
795	      if (!bag) {
796	        bag = {
797	          inv: Array(58).fill(null), armor: Array(20).fill(null), dye: Array(10).fill(null),
798	        };
799	        this.remoteItems.set(e.playerSlot, bag);
800	      }
801	      const arr = e.container === 0 ? bag.inv : e.container === 1 ? bag.armor : bag.dye;
802	      arr[e.itemSlot] = e.itemId ? { id: e.itemId, stack: e.stack } : null;
803	    }
804	  }
805	}
806	

```


---

## 🤖 Assistant · 2026-08-12T05:57:55.175Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"netPuppetContact\\|netPuppetProjContact\\|netMakeProj\\|netDropSweep\\|simulateRemotePlayers\\|netCanEditTile\\|netCanChestInteract\\|msg16\\|PlayerLifeMana\\|puppet\\|PUPPET\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -80",
 "description": "Locate net hooks in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:57:55.207Z

**📎 ToolResult**

```
395:  netCanEditTile(): boolean {
399:  netCanChestInteract(): boolean {
461:  // ================= v3 实体同步（房主权威 NPC + 双向掉落/弹幕；msg16/21/23/27/42） =================
549:  private netDropSweep() {
633:        const p = this.netMakeProj(s);
648:  private netMakeProj(s: ProjSnap): Entity | null {
650:    // 访客端据此对敌对弹幕傀儡本地结算 Damage_EVP（见 netPuppetProjContact）
705:  /** 访客：傀儡 NPC 接触伤害（房主 AI 只对房主结算；访客本地判 AABB，HP 客户端权威+msg16 中继）。
707:  private netPuppetContact() {
723:   *  语义与近战接触伤害同模型：玩家 HP 客户端权威 + msg16 中继（原版玩家伤害即本地
727:  private netPuppetProjContact() {
3679:    if (!this.netCanEditTile()) { this.mining = null; this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
4332:    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
4431:    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
4496:    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
4796:    const editDenied = !this.netCanEditTile() && (
5038:    if (!this.netCanChestInteract()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectItems')); return; }
9143:    if (this.net?.active) this.simulateRemotePlayers();
9151:        this.netDropSweep();
9154:      if (!this.net.policy.isHost) { this.netPuppetContact(); this.netPuppetProjContact(); }
9165:  private simulateRemotePlayers() {

```


---

## 🤖 Assistant · 2026-08-12T05:57:57.066Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read the Game.ts net section (lines ~390-780 and 9130-9260).
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:57:57.238Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "offset": 380,
 "limit": 400
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:57:57.248Z

**📎 ToolResult**

```
380	  particles: Particle[] = [];
381	  dmgNumbers: DamageNumber[] = [];
382	
383	  // 敌人生成
384	  boss: Enemy | null = null;
385	  /** 本局世界是否新生成(NPC 入驻公告只在新世界播) */
386	  private freshlyCreated = false;
387	  /** 原版 Spawner 移植实例（VanillaSpawner.ts） */
388	  vanillaSpawner: VanillaSpawner | null = null;
389	  /** 世界生成 worker 客户端（懒建；不可用时 newWorld 走主线程 fallback） */
390	  private genClient: WorldGenClient | null = null;
391	  /** 多人联机客户端（netMode==1；单机 null）。docs/multiplayer-design.md §4 */
392	  net: ClientNet | null = null;
393	  // ---- v3 房间制保护门禁（集中点，低耦合）：策略存于 net.policy，门禁只在操作入口查询 ----
394	  /** 破坏保护：单人/房主/未开启保护时放行 */
395	  netCanEditTile(): boolean {
396	    return !this.net || this.net.policy.isHost || !this.net.policy.protectTiles;
397	  }
398	  /** 物品保护：宝箱取放等受控（自动拾取不门禁——需求明确豁免） */
399	  netCanChestInteract(): boolean {
400	    return !this.net || this.net.policy.isHost || !this.net.policy.protectItems;
401	  }
402	  /** 门禁拒绝提示（2s 节流防刷屏） */
403	  private netDenyAt = 0;
404	  netDeny(msg: string) {
405	    const now = Date.now();
406	    if (now - this.netDenyAt > 2000) {
407	      this.netDenyAt = now;
408	      this.cb.onToast?.(msg);
409	    }
410	    this.input.rightDown = false;
411	  }
412	  // ---- 箱子同步（msg31/32，服务器权威） ----
413	  /** 待开箱（msg31 已发、等回包后自动开面板） */
414	  private netPendingChest: { x: number; y: number } | null = null;
415	  /** 已登记箱子差分基准（postUpdate 轮询 → msg32 槽位编辑上报） */
416	  private netChestWatch: Array<{ chest: ChestData; idx: number; last: Array<{ id: number; stack: number } | null> }> = [];
417	
418	  /** msg32 回包：登记/更新 world.chests（服务器权威），待开箱自动开面板 */
419	  private netApplyChest(chestIdx: number, x: number, y: number, items: Array<{ id: number; stack: number } | null>) {
420	    const w = this.world;
421	    let chest = w.chests.find((ch) => ch.x === x && ch.y === y);
422	    if (!chest) {
423	      chest = { x, y, items: Array(10).fill(null) };
424	      w.chests.push(chest);
425	    }
426	    for (let i = 0; i < items.length; i++) {
427	      // 稀疏数组：单槽广播只带变更槽，undefined = 未涉及（全量帧才每槽都有值）
428	      if (items[i] === undefined || i >= chest.items.length) continue;
429	      chest.items[i] = items[i] ? { ...items[i]! } : null;
430	    }
431	    this.net?.chestIndexByPos.set(`${x},${y}`, chestIdx);
432	    let watch = this.netChestWatch.find((wch) => wch.chest === chest);
433	    if (!watch) {
434	      watch = { chest, idx: chestIdx, last: chest.items.map((it) => it ? { ...it } : null) };
435	      this.netChestWatch.push(watch);
436	    } else {
437	      watch.last = chest.items.map((it) => it ? { ...it } : null);
438	    }
439	    if (this.netPendingChest && this.netPendingChest.x === x && this.netPendingChest.y === y) {
440	      this.netPendingChest = null;
441	      this.tryOpenChest(chest); // 服务器已下发内容 = 通过了 protectItems 门
442	    }
443	    this.cb.onInventoryChanged?.(); // 面板打开中时刷新槽位显示
444	  }
445	
446	  /** postUpdate 每 15 tick：箱子槽位差分上报（含他人广播回写后的再同步收敛） */
447	  private netChestPoll() {
448	    const net = this.net;
449	    if (!net?.active) return;
450	    for (const wch of this.netChestWatch) {
451	      for (let i = 0; i < wch.chest.items.length; i++) {
452	        const a = wch.chest.items[i], b = wch.last[i];
453	        if ((a?.id ?? 0) !== (b?.id ?? 0) || (a?.stack ?? 0) !== (b?.stack ?? 0)) {
454	          net.sendChestSlot(wch.idx, wch.chest.x, wch.chest.y, i, a?.id ?? 0, a?.stack ?? 0);
455	          wch.last[i] = a ? { ...a } : null;
456	        }
457	      }
458	    }
459	  }
460	
461	  // ================= v3 实体同步（房主权威 NPC + 双向掉落/弹幕；msg16/21/23/27/42） =================
462	  // 模型：房主客户端跑完整模拟（刷怪/AI/掉落，与单人同码），快照经服务器中继；
463	  // 访客渲染傀儡实体（无本地 AI），打击/拾取经上报由房主权威结算。
464	  // netId = 拥有者 slot<<24 | 本地实体 id（entitySyncHooks.makeNetId，防跨端撞号）
465	
466	  private netNpcPuppets = new Map<number, { e: Enemy; seen: number }>();
467	  private netDropPuppets = new Map<number, { d: ItemDrop; seen: number }>();
468	  private netProjPuppets = new Map<number, { p: Entity; seen: number }>();
469	  private netNpcLast = new Map<number, { x: number; y: number; hp: number; t: number }>();
470	  private netProjLast = new Map<number, { x: number; y: number; t: number }>();
471	  private netDropSeen = new Map<number, ItemDrop>();
472	
473	  /** 快照广播轮转游标（review C4：固定遍历序 + >=24 break 会让第 25 个起的实体
474	   *  永远拿不到快照（入侵/血月 >24 同屏移动怪时后段集体饿死被误清）。游标本轮
475	   *  断在哪、下轮从哪继续，公平轮转） */
476	  private netNpcCursor = 0;
477	  private netProjCursor = 0;
478	
479	  /** 房主：NPC 快照广播（15Hz，变化驱动 + 2s 兜底；对齐原版 msg23 netUpdate 思想） */
480	  private netNpcBroadcast() {
481	    const net = this.net!;
482	    const snaps: NpcSnap[] = [];
483	    const list = this.entities.enemies;
484	    const n = list.length;
485	    let examined = 0;
486	    for (; examined < n && snaps.length < 24; examined++) {
487	      const e = list[(this.netNpcCursor + examined) % n] as Enemy;
488	      if (e.netPuppet) continue;
489	      let last = this.netNpcLast.get(e.id);
490	      if (!last) {
491	        last = { x: e.x, y: e.y, hp: e.hp, t: this.tickCount };
492	        this.netNpcLast.set(e.id, last);
493	      }
494	      const moved = Math.abs(e.x - last.x) > 0.5 || Math.abs(e.y - last.y) > 0.5 || e.hp !== last.hp;
495	      if (!moved && this.tickCount - last.t < 120) continue; // 2s 全量兜底
496	      last.x = e.x; last.y = e.y; last.hp = e.hp; last.t = this.tickCount;
497	      snaps.push({
498	        netId: makeNetId(net.mySlot, e.id), key: e.key,
499	        x: e.x, y: e.y, vx: e.vx, vy: e.vy,
500	        hp: e.hp, maxHp: e.maxHp, animT: e.animT,
501	        flags: e.def.boss ? 1 : 0,
502	      });
503	    }
504	    this.netNpcCursor = (this.netNpcCursor + examined) % Math.max(1, n);
505	    // 清理已消亡敌人的差分基准（游标轮转下无条件跑——成本与主循环同阶）
506	    {
507	      const alive = new Set<number>();
508	      for (const ent of this.entities.enemies) alive.add((ent as Enemy).id);
509	      for (const id of this.netNpcLast.keys()) if (!alive.has(id)) this.netNpcLast.delete(id);
510	    }
511	    net.sendNpcSnapshot(snaps);
512	  }
513	
514	  /** 双向：本地弹幕快照（15Hz 变化驱动；kind: 0=Arrow 1=WeaponProj族 2=Dart 3=TrapShot 4=MagicProj） */
515	  private netProjBroadcast() {
516	    const net = this.net!;
517	    const snaps: ProjSnap[] = [];
518	    const list = this.entities.projectiles;
519	    const n = list.length;
520	    let examined = 0;
521	    for (; examined < n && snaps.length < 24; examined++) {
522	      const p = list[(this.netProjCursor + examined) % n] as Entity & { projId?: number; damage?: number; kind?: string; color?: string; life?: number };
523	      if (p.netPuppet || p.dead) continue;
524	      let last = this.netProjLast.get(p.id);
525	      if (!last) {
526	        last = { x: p.x, y: p.y, t: this.tickCount };
527	        this.netProjLast.set(p.id, last);
528	      }
529	      if (Math.abs(p.x - last.x) < 1 && Math.abs(p.y - last.y) < 1 && this.tickCount - last.t < 60) continue;
530	      last.x = p.x; last.y = p.y; last.t = this.tickCount;
531	      let kind = -1, tag = '', dmg = Math.max(-32768, Math.min(32767, Math.round(p.damage ?? 0))), aux = 0;
532	      if (p instanceof Arrow) {
533	        kind = 0; tag = String(p.projId ?? 1);
534	        // v5：敌对弹带 bit7（原版 Projectile.hostile）——访客端据此本地结算 Damage_EVP
535	        if (p.hostile) kind |= 0x80;
536	      }
537	      else if (p instanceof Dart) { kind = 2; tag = String(p.projId ?? 0); }
538	      else if (p.projId !== undefined) { kind = 1; tag = String(p.projId); }
539	      else if (p instanceof TrapShot) { kind = 3; tag = p.kind ?? 'dart'; }
540	      else if (p.color !== undefined) { kind = 4; tag = p.color; aux = Math.max(0, Math.min(32767, p.life ?? 600)); }
541	      if (kind < 0) continue; // 未知弹幕类不同步（渲染缺类）
542	      snaps.push({ netId: makeNetId(net.mySlot, p.id), kind, tag, dmg, aux, x: p.x, y: p.y, vx: p.vx, vy: p.vy });
543	    }
544	    this.netProjCursor = (this.netProjCursor + examined) % Math.max(1, n);
545	    net.sendProjectileBatch(snaps);
546	  }
547	
548	  /** 双向：本地真掉落诞生上报 + 消失（拾取/寿命）广播——扫描差分 */
549	  private netDropSweep() {
550	    const net = this.net!;
551	    const cur = new Map<number, ItemDrop>();
552	    for (const ent of this.entities.drops) {
553	      const d = ent as ItemDrop;
554	      if (d.netPuppet) continue;
555	      if (!d.netId) {
556	        d.netId = makeNetId(net.mySlot, d.id);
557	        net.sendItemOp(0, d.netId, ITEM_DEFS[d.itemId]?.key ?? '', d.stack, d.x, d.y, d.vx, d.vy);
558	      }
559	      cur.set(d.netId, d);
560	    }
561	    for (const netId of this.netDropSeen.keys()) {
562	      if (!cur.has(netId)) net.sendItemOp(1, netId); // 上轮在、本轮没 = 拾取/过期 → take
563	    }
564	    this.netDropSeen = cur;
565	  }
566	
567	  /** msg23 回包：NPC 傀儡 upsert（首次创建入桶；boss 置 this.boss 供血条） */
568	  private netApplyNpcSnaps(snaps: NpcSnap[]) {
569	    for (const s of snaps) {
570	      let pup = this.netNpcPuppets.get(s.netId);
571	      if (!pup || pup.e.dead) {
572	        // v_* 键走 fromVanilla（防御/伤害等权威属性——占位 def 会让 hurt 双端分叉）；
573	        // 原生键退普通构造
574	        const vm = s.key.match(/^v_(\d+)$/);
575	        const e = vm ? Enemy.fromVanilla(parseInt(vm[1], 10), s.x, s.y) : new Enemy(s.key, s.x, s.y);
576	        if (!e) continue; // review C2：未知 vanillaId（数据表缺口）只丢这一条，勿中止整批（否则同帧其余傀儡饿死被误清）
577	        e.x = s.x; e.y = s.y; // 快照坐标=左上（Enemy 构造按中心偏移，直接覆写）
578	        e.netPuppet = true;
579	        e.netId = s.netId;
580	        e.hp = s.hp; e.maxHp = s.maxHp;
581	        this.entities.add(e, 'enemies');
582	        if (e.def.boss) this.boss = e;
583	        pup = { e, seen: this.tickCount };
584	        this.netNpcPuppets.set(s.netId, pup);
585	      }
586	      const e = pup.e;
587	      e.netSnapTo(s.x, s.y); // P3.2：渲染位平滑追踪快照；逻辑位（netAx/netAy）= 最新快照
588	      e.vx = s.vx; e.vy = s.vy;
589	      e.hp = s.hp; e.maxHp = s.maxHp;
590	      e.animT = s.animT;
591	      if (Math.abs(s.vx) > 0.1) e.facing = Math.sign(s.vx);
592	      pup.seen = this.tickCount;
593	    }
594	  }
595	
596	  /** msg21 回包：掉落物傀儡 upsert / take 移除（含拥有者本地真掉落被他人拾取） */
597	  private netApplyItemOp(op: ItemOpMsg) {
598	    if (op.op === 0) {
599	      const id = ITEM_BY_KEY[op.key];
600	      if (id === undefined) return;
601	      let pup = this.netDropPuppets.get(op.netId);
602	      if (!pup) {
603	        const d = new ItemDrop(op.x, op.y, id, Math.max(1, op.stack), op.vx, op.vy);
604	        d.netPuppet = true;
605	        d.netId = op.netId;
606	        this.entities.add(d, 'drops');
607	        pup = { d, seen: this.tickCount };
608	        this.netDropPuppets.set(op.netId, pup);
609	      }
610	      pup.d.x = op.x; pup.d.y = op.y;
611	      pup.d.vx = op.vx; pup.d.vy = op.vy;
612	      pup.seen = this.tickCount;
613	    } else {
614	      const pup = this.netDropPuppets.get(op.netId);
615	      if (pup) {
616	        pup.d.dead = true;
617	        this.netDropPuppets.delete(op.netId);
618	        return;
619	      }
620	      // 拥有者的真掉落被他人拾取（访客 take 上报 → 房主在此移除真身）
621	      for (const ent of this.entities.drops) {
622	        const d = ent as ItemDrop;
623	        if (!d.netPuppet && d.netId === op.netId) { d.dead = true; break; }
624	      }
625	    }
626	  }
627	
628	  /** msg27 回包：弹幕傀儡 upsert（按 kind 重建真类，纯视觉——不跑命中） */
629	  private netApplyProjSnaps(snaps: ProjSnap[]) {
630	    for (const s of snaps) {
631	      let pup = this.netProjPuppets.get(s.netId);
632	      if (!pup || pup.p.dead) {
633	        const p = this.netMakeProj(s);
634	        if (!p) continue;
635	        p.netPuppet = true;
636	        p.netId = s.netId;
637	        p.netAx = s.x; p.netAy = s.y; p.netIt = 1; // P3.2：新建直接落位
638	        this.entities.add(p, 'projectiles');
639	        pup = { p, seen: this.tickCount };
640	        this.netProjPuppets.set(s.netId, pup);
641	      }
642	      pup.p.netSnapTo(s.x, s.y); // P3.2：插值追踪（弹幕周期短，intervalTicks 默认 4）
643	      pup.p.vx = s.vx; pup.p.vy = s.vy;
644	      pup.seen = this.tickCount;
645	    }
646	  }
647	
648	  private netMakeProj(s: ProjSnap): Entity | null {
649	    // v5：bit7 = hostile（原版 Projectile.hostile，仅 kind0/Arrow 语义有效）——
650	    // 访客端据此对敌对弹幕傀儡本地结算 Damage_EVP（见 netPuppetProjContact）
651	    const hostile = (s.kind & 0x80) !== 0;
652	    switch (s.kind & 0x7f) {
653	      case 0: return new Arrow(s.x, s.y, s.vx, s.vy, s.dmg, 0, parseInt(s.tag, 10) || 1, null, { hostile });
654	      case 1: return new Boomerang(s.x, s.y, s.vx, s.vy, s.dmg, 0, parseInt(s.tag, 10) || 1); // WeaponProj 族共用 drawProj(projId) 渲染，取代表类重建
655	      case 2: return new Dart(s.x, s.y, s.vx, s.vy, s.dmg, parseInt(s.tag, 10) || 0);
656	      case 3: return new TrapShot(s.x, s.y, s.vx, s.vy, s.dmg, (s.tag || 'dart') as TrapShotKind);
657	      case 4: return new MagicProj(s.x, s.y, s.vx, s.vy, s.dmg, Math.max(60, s.aux), s.tag || '#8090FF');
658	      default: return null;
659	    }
660	  }
661	
662	  /** msg42 回包（房主）：访客打击权威结算——按 netId 找真身应用 hurt（防御减算在此一次） */
663	  private netApplyStrike(netId: number, rawDmg: number, kbx: number, kby: number) {
664	    const localId = netIdLocal(netId);
665	    for (const ent of this.entities.enemies) {
666	      const e = ent as Enemy;
667	      if (e.netPuppet || e.id !== localId) continue;
668	      e.hurt(rawDmg, kbx, kby, this);
669	      const dealt = Math.max(1, Math.round(rawDmg - (e.def.defense ?? 0) * 0.5));
670	      this.addDamageNumber(e.cx, e.y, dealt, false, '#FF7060');
671	      return;
672	    }
673	  }
674	
675	  /** 傀儡清扫：死亡/超时无快照（掉线房主、宿主清场）→ 移除 */
676	  private netSweepPuppets() {
677	    for (const [id, pup] of this.netNpcPuppets) {
678	      if (pup.e.dead || this.tickCount - pup.seen > 300) {
679	        pup.e.dead = true;
680	        if (this.boss === pup.e) this.boss = null;
681	        this.netNpcPuppets.delete(id);
682	      }
683	    }
684	    for (const [id, pup] of this.netDropPuppets) {
685	      if (pup.d.dead) {
686	        // 傀儡消失两源：本地拾取（dead 由 ItemDrop 置位）→ 上报 take 让房主移除真身；
687	        // 寿命/远端 take → netApplyItemOp 已删映射，不会走到这
688	        this.net?.sendItemOp(1, id);
689	        this.netDropPuppets.delete(id);
690	        continue;
691	      }
692	      if (this.tickCount - pup.seen > 300) {
693	        pup.d.dead = true;
694	        this.netDropPuppets.delete(id);
695	      }
696	    }
697	    for (const [id, pup] of this.netProjPuppets) {
698	      if (pup.p.dead || this.tickCount - pup.seen > 180) {
699	        pup.p.dead = true;
700	        this.netProjPuppets.delete(id);
701	      }
702	    }
703	  }
704	
705	  /** 访客：傀儡 NPC 接触伤害（房主 AI 只对房主结算；访客本地判 AABB，HP 客户端权威+msg16 中继）。
706	   *  P3.2：判定用权威位 netAx/netAy（渲染位在插值途中，最多滞后一个快照周期 66ms） */
707	  private netPuppetContact() {
708	    const p = this.player;
709	    if (p.dead) return;
710	    for (const [, pup] of this.netNpcPuppets) {
711	      const e = pup.e;
712	      if (e.dead || e.iframes > 0) continue;
713	      const dmg = e.def.damage ?? 0;
714	      if (dmg <= 0) continue;
715	      // 手工 AABB（权威位 vs 本地玩家），不经插值渲染位
716	      if (!(e.netAx < p.x + p.w && e.netAx + e.w > p.x && e.netAy < p.y + p.h && e.netAy + e.h > p.y)) continue;
717	      this.damagePlayer(dmg, e.cx, e.cy, e);
718	      e.iframes = 8;
719	    }
720	  }
721	
722	  /** 访客：敌对弹幕傀儡本地结算（原版 Projectile.Damage_EVP，Projectile.cs:13706-13830）。
723	   *  语义与近战接触伤害同模型：玩家 HP 客户端权威 + msg16 中继（原版玩家伤害即本地
724	   *  结算——每端各自跑弹幕命中本地玩家判定）。hitPlayer 内含原版门禁链：
725	   *  hostile + dmg>0 / player.immune(iframes) / AABB 相交；命中【不消耗穿透】
726	   *  （:13811-13829 特判除外），弹体照常飞行；debuff 授予以实际伤害为准（statusPlayer）。 */
727	  private netPuppetProjContact() {
728	    for (const [, pup] of this.netProjPuppets) {
729	      const pr = pup.p as Entity & { hostile?: boolean; damage?: number; projId?: number };
730	      if (!pr.hostile || pr.dead) continue;
731	      if (hitPlayer(pr, this, pr.damage ?? 0)) statusPlayer(this, pr.projId ?? 0);
732	    }
733	  }
734	  /** 远端玩家渲染代理（net.players → drawPlayer 可用形状，net 激活时每帧同步） */
735	  private remotePlayerProxies: import('../entities/Player').Player[] = [];
736	  /** tile key → id 反查表（调试句柄/wld 导入映射用） */
737	  tileByKey = TILE_BY_KEY;
738	
739	  /** 开发者模式：全部道具入包（溢出的落在展示区上方）+ 出生点右侧摆放所有可放置图块供检验 */
740	  setupDevMode() {
741	    const p = this.player;
742	    const st = this.world.store;
743	    // ---- 1) 全道具入包 ----
744	    const overflow: Array<[string, number]> = [];
745	    for (const def of ITEM_DEFS) {
746	      const n = def.maxStack === 1 ? 1 : Math.min(def.maxStack, 99);
747	      const left = p.inv.add(ITEM_BY_KEY[def.key], n);
748	      if (left > 0) overflow.push([def.key, left]);
749	    }
750	    // ---- 2) 展示区：出生点右侧清空并逐行摆放全部可放置图块 ----
751	    const sx = this.world.spawnX, sy = this.world.spawnY;
752	    const x0 = sx + 6, x1 = sx + 70, yBot = sy - 2, yTop = sy - 40;
753	    for (let x = x0; x <= x1; x++) {
754	      for (let y = yTop; y <= yBot; y++) {
755	        st.setTile(x, y, 0);
756	        st.setLiquid(x, y, 0, 0);
757	      }
758	      st.setTile(x, yBot, T.STONE);
759	      st.setTile(x, yBot + 1, T.STONE);
760	    }
761	    // 收集可放置 tile（有物品指向，去重）
762	    const placeable: number[] = [];
763	    const seen = new Set<number>();
764	    for (const def of ITEM_DEFS) {
765	      if (!def.tile) continue;
766	      const tid = TILE_BY_KEY[def.tile];
767	      if (tid === undefined || tid === 0 || seen.has(tid)) continue;
768	      seen.add(tid);
769	      placeable.push(tid);
770	    }
771	    // 逐行摆放：行高 7（最高家具 5 格 + 间隙），每行放满换行并铺新地板
772	    let cx = x0 + 1, cy = yBot - 1;
773	    const rowH = 7;
774	    for (const tid of placeable) {
775	      const td = TILE_DEFS[tid];
776	      const w = td.vanilla?.fw ?? td.w ?? 1;
777	      const h = td.vanilla?.fh ?? td.h ?? 1;
778	      if (cx + w > x1 - 1) {
779	        cx = x0 + 1;

```


---

## 🤖 Assistant · 2026-08-12T05:57:57.465Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "offset": 9130,
 "limit": 160
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:57:57.481Z

**📎 ToolResult**

```
9130	      // R3 移动续传：跨条带（200×20）边界时向服务器请求周围 strip
9131	      if (this.tickCount % 30 === 0 && this.net.gameWorld) {
9132	        const sx = Math.floor(this.player.cx / 16 / 200);
9133	        const sy = Math.floor(this.player.cy / 16 / 20);
9134	        const key = sx + ',' + sy;
9135	        if (key !== this.lastStripReq) {
9136	          this.lastStripReq = key;
9137	          this.net.requestSection(this.player.cx, this.player.cy);
9138	        }
9139	      }
9140	    }
9141	    this.updateSwingHits();
9142	    // 远端玩家模拟（每逻辑 tick：控制位驱动物理 + netOffset 平滑，对齐原版远端玩家）
9143	    if (this.net?.active) this.simulateRemotePlayers();
9144	    // 箱子槽位差分上报（15 tick 轮询；UI/快捷堆叠等所有变更源统一捕获）
9145	    if (this.net?.active && this.tickCount % 15 === 0) this.netChestPoll();
9146	    // v3 实体同步：房主 NPC 快照 + 双向弹幕/掉落 + 傀儡清扫/接触伤害
9147	    if (this.net?.active) {
9148	      if (this.tickCount % 4 === 0) {
9149	        if (this.net.policy.isHost) this.netNpcBroadcast();
9150	        this.netProjBroadcast();
9151	        this.netDropSweep();
9152	      }
9153	      if (this.tickCount % 30 === 0) this.netSweepPuppets();
9154	      if (!this.net.policy.isHost) { this.netPuppetContact(); this.netPuppetProjContact(); }
9155	    }
9156	  }
9157	
9158	  /**
9159	   * 联机远端玩家模拟（对齐原版 MessageBuffer.cs case 13 + Player.UpdateNetOffset）：
9160	   * 远端玩家在本端用同步的控制位+速度跑移动物理（有移动过程、动画帧由速度派生）；
9161	   * 每个权威包的位置差注入 netOffset，渲染时叠加并逐 tick 收敛（<2px 归零，
9162	   * 每步 max(2, len×0.1)；超 300px=Main.multiplayerNPCSmoothingRange 直接归零）。
9163	   * 物理只取移动子集——环境伤害/液体细判等权威在各自客户端，避免双端分叉。
9164	   */
9165	  private simulateRemotePlayers() {
9166	    const net = this.net!;
9167	    const list: Player[] = [];
9168	    for (const [slot, rp] of net.players) {
9169	      if (!rp.active || slot === net.mySlot) continue;
9170	      let proxy = this.remotePlayerProxies.find((p) => (p as unknown as { __netSlot?: number }).__netSlot === slot);
9171	      if (!proxy) {
9172	        proxy = new Player(rp.x, rp.y, new Inventory()); // R11：独立空背包——不共享本地 inv
9173	        (proxy as unknown as { __netSlot?: number }).__netSlot = slot;
9174	      }
9175	      // 新权威包（原版 case 13：netOffset += 模拟位置 - 权威位置；超限归零；硬设权威 pos/vel）
9176	      if (rp.fresh) {
9177	        rp.fresh = false;
9178	        proxy.netOffX += proxy.x - rp.x;
9179	        proxy.netOffY += proxy.y - rp.y;
9180	        if (Math.hypot(proxy.netOffX, proxy.netOffY) > 300) { proxy.netOffX = 0; proxy.netOffY = 0; }
9181	        proxy.x = rp.x; proxy.y = rp.y;
9182	        proxy.vx = rp.vx; proxy.vy = rp.vy;
9183	      }
9184	      // 控制位 → 输入（原版：远端玩家以同步的 control* 跑 Player.Update）。
9185	      // P1.1 AOI 配套：>1.5s 无 msg13（超出对端视野被过滤/断流）→ 冻结输入，
9186	      // 防陈旧控制位驱动的"幽灵行走"（静止心跳 1s，正常通路不会触发）。
9187	      // review C5：useItem 一并冻结——否则断流后代理原地无限空挥
9188	      const stale = performance.now() - rp.lastFresh > 1500;
9189	      proxy.inputX = stale ? 0 : (rp.left ? -1 : 0) + (rp.right ? 1 : 0);
9190	      proxy.inputJump = !stale && rp.jump;
9191	      proxy.inputDown = !stale && rp.down;
9192	      proxy.inputUp = !stale && rp.up;
9193	      proxy.facing = rp.facing;
9194	      proxy.dead = rp.dead;
9195	      // R11'.外观合并：仅接受含 hair 的完整对象（空对象会令纸娃娃读 X.r 崩溃）。
9196	      // review C10：仅在外观串变化时解析（msg4 才变）——60TPS×每玩家 JSON.parse 纯浪费
9197	      {
9198	        const meta = proxy as unknown as { __netAppearance?: string };
9199	        if (meta.__netAppearance !== rp.appearance) {
9200	          meta.__netAppearance = rp.appearance;
9201	          try {
9202	            const parsed = JSON.parse(rp.appearance) as Record<string, unknown>;
9203	            if (parsed && typeof parsed.hair === 'number') proxy.appearance = parsed as never;
9204	          } catch { /* 保持默认外观 */ }
9205	        }
9206	      }
9207	      // 物品/装备（msg5）：拷入代理背包——手持物 holdStyle/挥舞动画/盔甲纸娃娃渲染依赖。
9208	      // 数组直接共享（代理只读不写，远端真权威在各自客户端）
9209	      const bag = net.remoteItems.get(slot);
9210	      if (bag) {
9211	        proxy.inv.slots = bag.inv;
9212	        proxy.inv.armor = bag.armor;
9213	        proxy.inv.dye = bag.dye;
9214	        proxy.inv.selected = Math.min(rp.selectedItem, 9); // 快捷栏 0-9（heldItem 依赖）
9215	      }
9216	      // useItem 位 → 远端挥舞动画（原版：远端客户端以 controlUseItem 跑 ItemCheck 设置
9217	      // itemAnimation；此处派生等价 swing——时长按本地同公式，攻速配饰差异忽略）
9218	      if (!stale && rp.useItem) {
9219	        const heldId = proxy.inv.heldItem()?.id ?? -1;
9220	        if (!proxy.swingNet || proxy.swingNet.item !== heldId || proxy.swingNet.t <= 0) {
9221	          proxy.swingNet = { t: this.remoteSwingDur(heldId), dur: this.remoteSwingDur(heldId), item: heldId };
9222	        } else proxy.swingNet.t--;
9223	      } else if (proxy.swingNet) {
9224	        proxy.swingNet.t--;
9225	        if (proxy.swingNet.t <= 0) proxy.swingNet = null;
9226	      }
9227	      this.stepRemoteProxy(proxy);
9228	      // netOffset 衰减（UpdateNetOffset :28240-28270 1:1，碰撞安全项略）
9229	      const len = Math.hypot(proxy.netOffX, proxy.netOffY);
9230	      if (len < 2) { proxy.netOffX = 0; proxy.netOffY = 0; }
9231	      else {
9232	        const k = Math.max(0, len - Math.max(2, len * 0.1)) / len;
9233	        proxy.netOffX *= k; proxy.netOffY *= k;
9234	      }
9235	      list.push(proxy);
9236	    }
9237	    this.remotePlayerProxies = list;
9238	  }
9239	
9240	  /** 远端挥舞时长（对齐本地各分支公式，Game.useItem 派生处：剑/近战 max(12,useTime)、
9241	   *  镐斧锤 max(14,speed)、其它 30；攻速配饰倍率远端不可见，取基础值） */
9242	  private remoteSwingDur(itemId: number): number {
9243	    if (itemId < 0) return 30;
9244	    const def = ITEM_DEFS[itemId];
9245	    if (!def) return 30;
9246	    const cw = combatWeapon(def);
9247	    if (def.tool?.type === 'sword' || cw?.kind === 'melee') return Math.max(12, cw?.useTime ?? def.tool?.speed ?? 42);
9248	    if (def.tool && (def.tool.type === 'pick' || def.tool.type === 'axe' || def.tool.type === 'hammer')) return Math.max(14, def.tool.speed ?? 46);
9249	    return 30;
9250	  }
9251	
9252	  /** 远端代理移动子集物理（与 Player.fixedUpdate 同参数：加速/摩擦/跳跃/重力/碰撞/动画） */
9253	  private stepRemoteProxy(p: Player) {
9254	    const st = this.world.store;
9255	    // 液体粗判（游泳减速/上浮需要；同 Player 采样：脚底上方 4px）
9256	    p.inWater = st.liquid[st.idx(Math.floor(p.cx / TILE), Math.floor((p.y + p.h - 4) / TILE))] > 100;
9257	    const ix = p.inputX;
9258	    if (ix !== 0) {
9259	      p.vx += ix * PLAYER_WALK_ACCEL * (p.inWater ? 0.6 : 1);
9260	      p.facing = ix;
9261	    } else {
9262	      p.vx *= p.onGround ? PLAYER_FRICTION : PLAYER_AIR_FRICTION;
9263	      if (Math.abs(p.vx) < 0.05) p.vx = 0;
9264	    }
9265	    const maxSpd = PLAYER_WALK_MAX * (p.inWater ? 0.55 : 1);
9266	    p.vx = Math.max(-maxSpd, Math.min(maxSpd, p.vx));
9267	    if (p.inWater) {
9268	      if (p.inputJump) p.vy = Math.max(p.vy - 0.62, -4.4);
9269	      p.vy += GRAVITY * 0.3;
9270	      p.vy = Math.max(-4.6, Math.min(3.0, p.vy));
9271	    } else {
9272	      if (p.inputJump && p.onGround) { p.vy = -PLAYER_JUMP_SPEED; p.jumpHold = PLAYER_JUMP_TICKS; }
9273	      if (p.inputJump && p.jumpHold > 0) { p.vy -= 0.22; p.jumpHold--; } else p.jumpHold = 0;
9274	      p.vy = Math.min(p.vy + GRAVITY, MAX_FALL_SPEED);
9275	    }
9276	    if (!p.inputJump && p.vy < -2) p.vy = -2;
9277	    p.dropThrough = !!p.inputDown;
9278	    moveAndCollide(p, this.world, p.vx, p.vy);
9279	    if (Math.abs(p.vx) > 0.3 && p.onGround) p.animTime += Math.abs(p.vx);
9280	    else p.animTime = 0;
9281	  }
9282	}
9283	

```


---

## 🤖 Assistant · 2026-08-12T05:58:18.245Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have most of the picture. Let me also check:
- server/src/index.ts (watchdog 120s, save-interval, persistence)
- server/src/persist.ts
- entitySyncHooks.ts (makeNetId)
- The pickup logic on visitor side (netApplyItemOp take / local pickup of puppet drops) — need to check how a visitor picks up a puppet drop and whether server validates msg21 op=1 (take). In Room.handle Msg.SyncItem: any client can send op=1 take for any netId — it just relays. Host processes take on its side. But also note that the host's own take... Also the host's drop spawn (msg21 op=0) is relayed to everyone with no validation of stack! key.length<=64, stack != 0 — but stack up to 65535, key arbitrary string. So a malicious client can spawn arbitrary items via msg21 op=0? Wait — msg21 is relayed from any client (no isHost gate). Game's netDropSweep only sends op=0 for real local drops, but a malicious client can craft frames to spawn puppet drops on everyone with arbitrary key/stack. Then pickup: when a visitor's player picks up a puppet drop (auto-pickup exempt from protectItems), the item enters their real inventory → then they can put it into a chest (if protectItems off) → item duplication/injection. Even with protectItems on... protectItems protects chests from non-host. But item injection into own inventory is possible: spawn puppet drop at own feet with key="item:PlatinumCoin" stack=999 → local auto-pickup? Need to check how puppet drops get picked up locally — pickup logic in Game for drops probably picks up netPuppet drops too (auto-pickup exemption). Let me check pickup code.

Also item pickup on visitor: when visitor picks up a puppet drop, does the visitor gain the item locally? netApplyItemOp creates real ItemDrop entities with netPuppet flag. Pickup logic likely treats them as normal drops → added to inventory. Then netSweepPuppets: if pup.d.dead (local pickup) → sendItemOp(1) take → host removes real drop. So the item flow: host's real drop → visitor picks puppet → visitor gains item. But if malicious client spawns a fake msg21 op=0 with arbitrary key/stack, everyone renders a puppet, and whoever picks it up gets real items. That's an item injection exploit — must fix (server should only relay msg21 op=0 from host, or validate). Actually wait — is msg21 op=0 from visitors legitimate? Visitors' own local real drops: netDropSweep sends op=0 for local drops of any client (双向). E.g. visitor digs a block (protectTiles off) → drop spawns locally on visitor → broadcast op=0. So visitors legitimately send op=0. So server can't gate to host-only without changing semantics. But server could validate netId owner prefix (netId = owner slot << 24 | local id) — check that netId >>> 24 === c.slot. Let me check makeNetId in entitySyncHooks.

Also msg27: any client can send projectiles with arbitrary dmg (i16), hostile bit set (bit7). Malicious visitor can set kind=0|0x80 hostile with dmg=32767 → other visitors' clients compute hitPlayer locally → forced PvP damage. Same as hostile host issue but from any visitor. Also note the server validates (kind&0x7f)>4 but passes bit7 through. So forced PvP from any client, not just host. That's a must-fix or at least建议: gate hostile bit by... hmm, hostile projectiles legitimately come from NPCs (host simulates NPC arrows). Owner check: hostile NPC arrows are created by host's simulation with netId = host slot<<24. But a hostile bit from a visitor's own weapon projectile would be from visitor slot. Server could check: hostile bit allowed only if sender is host (since NPC arrows are simulated by host). Actually wait — are enemy arrows spawned by the host with hostile=true? Hostile projectiles in Terraria are those that damage players (NPC projectiles). In our port, Arrow has hostile flag (NPC arrows). On host, NPC arrows are real entities, broadcast with kind|=0x80 if p.hostile. Player-owned arrows are not hostile. So hostile should only originate from host. So server can gate: hostile bit set → require c.isHost. That closes visitor-forced-PvP but not host-forced-PvP (host is authority for NPC sim; vanilla has PvP toggle).

Also msg27 dmg from visitor: non-hostile projectile damage only affects... hits what on other clients? netMakeProj creates puppet without running hits ("纯视觉——不跑命中") except hostile→hitPlayer. So non-hostile dmg is harmless to others. But hostile+host → forced PvP.

Also msg21 op=1 (take): any client can send take for any netId — including netIds owned by others. Effect: host removes its real drop (despawns). Mild griefing (steal-by-despawn — actually if attacker sends take for a drop near victim, the drop disappears everywhere; the attacker doesn't get the item though, since take is just relayed and the host removes the real drop; attacker gets nothing but denies others). Record-level.

msg42 strike: dmg clamped 9999, but visitor can send strikes for any netId repeatedly at any rate — no rate limit. Spam possible. And negative dmg? Math.max(-32768,...) allows negative → heal NPC? e.hurt(rawDmg...) with negative rawDmg might heal or misbehave. Minor.

Now check index.ts for watchdog & save interval, persist.ts.

Also need to check pickup: does the visitor pick up puppet drops into real inventory? Let me check the drops pickup code and whether protectItems/automáticamente. Also check "拾取" path in Game (entities.drops pickup) to confirm puppet drops are pickable.

Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:58:18.335Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/server/src/index.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:58:18.351Z

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
35	
36	// ================= 房间注册表 =================
37	
38	interface RoomEntry { room: Room; createdAt: number; /** P0.3 预算占用（w*h*11B） */ bytes: number; }
39	
40	const rooms = new Map<string, RoomEntry>(); // code → room
41	/** P0.3 已用世界内存预算 */
42	let worldBudgetUsed = 0;
43	
44	function newCode(): string {
45	  for (;;) {
46	    const code = String(Math.floor(Math.random() * 900000) + 100000); // 6 位数字
47	    if (!rooms.has(code)) return code;
48	  }
49	}
50	
51	/** 统一摘除（回收/关房共用）：释放内存预算 */
52	function removeRoom(code: string) {
53	  const entry = rooms.get(code);
54	  if (!entry) return;
55	  entry.room.closed = true;
56	  worldBudgetUsed -= entry.bytes;
57	  rooms.delete(code);
58	}
59	
60	/** 空房回收（创建满 1 分钟且一直无人满 5 分钟 → 关闭回收；--world 常驻房豁免） */
61	setInterval(() => {
62	  const now = Date.now();
63	  for (const [code, entry] of rooms) {
64	    if (entry.room.persistent) continue;
65	    const idle = now - entry.createdAt;
66	    if (entry.room.closed || (entry.room.onlineCount === 0 && idle > 60_000 && idle > 5 * 60_000)) {
67	      removeRoom(code);
68	      console.log(`[room] 回收空房 ${code}`);
69	    }
70	  }
71	}, 60_000);
72	
73	function worldFromSaveJson(json: string) {
74	  return loadSaveData(JSON.parse(json)).world;
75	}
76	
77	/** 本机全部局域网 IPv4（多网卡全列出——UI 分享用） */
78	function lanIps(): string[] {
79	  const out: string[] = [];
80	  for (const list of Object.values(node_os.networkInterfaces())) {
81	    for (const ni of list ?? []) {
82	      if (ni.family === 'IPv4' && !ni.internal) out.push(ni.address);
83	    }
84	  }
85	  return out;
86	}
87	
88	// ================= HTTP Lobby =================
89	
90	const CORS = {
91	  'Access-Control-Allow-Origin': '*',
92	  'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',
93	  'Access-Control-Allow-Headers': 'Content-Type',
94	  'Access-Control-Allow-Private-Network': 'true',
95	};
96	
97	function readBody(req: http.IncomingMessage, limit: number): Promise<Buffer> {
98	  return new Promise((resolveBody, reject) => {
99	    const chunks: Buffer[] = [];
100	    let size = 0;
101	    req.on('data', (d: Buffer) => {
102	      size += d.length;
103	      if (size > limit) { reject(new Error('上传超限')); req.destroy(); return; }
104	      chunks.push(d);
105	    });
106	    req.on('end', () => resolveBody(Buffer.concat(chunks)));
107	    req.on('error', reject);
108	  });
109	}
110	
111	const lobby = http.createServer(async (req, res) => {
112	  const url = new URL(req.url ?? '/', `http://127.0.0.1:${PORT}`);
113	  const finish = (code: number, data: unknown) => {
114	    res.writeHead(code, { 'Content-Type': 'application/json', ...CORS });
115	    res.end(JSON.stringify(data));
116	  };
117	  if (req.method === 'OPTIONS') { finish(204, {}); return; }
118	
119	  try {
120	    // GET /stats → 观测快照（P0.1；全局 + 逐房 + 逐客户端）
121	    if (req.method === 'GET' && url.pathname === '/stats') {
122	      finish(200, statsSnapshot([...rooms.values()].map((e) => e.room)));
123	      return;
124	    }
125	    // GET /rooms → 公开房间列表（非公开不展示，只能码进）
126	    if (req.method === 'GET' && url.pathname === '/rooms') {
127	      const list = [...rooms.values()]
128	        .filter((e) => e.room.opts.publicRoom && !e.room.closed)
129	        .map((e) => ({
130	          code: e.room.opts.code, name: e.room.opts.name,
131	          online: e.room.onlineCount, maxPlayers: e.room.opts.maxPlayers, w: e.room.world.w, h: e.room.world.h,
132	          protectTiles: e.room.opts.protectTiles, protectItems: e.room.opts.protectItems,
133	        }));
134	      finish(200, { ok: true, rooms: list });
135	      return;
136	    }
137	    const m = url.pathname.match(/^\/rooms\/(\d{6})$/);
138	    // GET /rooms/<code> → 房间码校验（加入前置检查，非公开房也允许码查）
139	    if (req.method === 'GET' && m) {
140	      const entry = rooms.get(m[1]);
141	      if (!entry || entry.room.closed) { finish(404, { ok: false, error: '房间不存在' }); return; }
142	      finish(200, {
143	        ok: true, code: entry.room.opts.code, name: entry.room.opts.name,
144	        online: entry.room.onlineCount,
145	        protectTiles: entry.room.opts.protectTiles, protectItems: entry.room.opts.protectItems,
146	        // 首箱锚点（调试/探针确定性用；LAN 游戏服务器无敏感性）
147	        chest: entry.room.world.chests[0] ? { x: entry.room.world.chests[0].x, y: entry.room.world.chests[0].y } : null,
148	      });
149	      return;
150	    }
151	    // POST /rooms → 创建房间（body: {name, public, protectTiles, protectItems, maxPlayers, save}）
152	    if (req.method === 'POST' && url.pathname === '/rooms') {
153	      if (rooms.size >= MAX_ROOMS) { finish(503, { ok: false, error: '服务器房间已满' }); return; }
154	      // P0.3 预检①：上传体积预拒（读 body 前按 limit 截断，防超大 body 打爆内存）
155	      const raw = await readBody(req, WORLD_UPLOAD_LIMIT).catch(() => null);
156	      if (!raw) { finish(400, { ok: false, error: `上传超限（>${Math.round(WORLD_UPLOAD_LIMIT / 1048576)}MB）` }); return; }
157	      const body = JSON.parse(raw.toString('utf8')) as {
158	        name?: string; public?: boolean; protectTiles?: boolean; protectItems?: boolean; maxPlayers?: number; save?: string;
159	      };
160	      if (!body.save) { finish(400, { ok: false, error: '缺少 save（世界存档 JSON）' }); return; }
161	      // P0.3 预检②：全服世界内存预算（15B/格 估算，见 BYTES_PER_TILE 注释）
162	      let worldW = 0, worldH = 0;
163	      try {
164	        const head = JSON.parse(body.save) as { header?: { width?: number; height?: number } };
165	        worldW = head.header?.width ?? 0;
166	        worldH = head.header?.height ?? 0;
167	      } catch { /* 走 worldFromSaveJson 的解析错误 */ }
168	      const estBytes = worldW * worldH * BYTES_PER_TILE;
169	      if (estBytes > 0 && worldBudgetUsed + estBytes > WORLD_BUDGET) {
170	        finish(503, { ok: false, error: `服务器世界内存预算不足（已用 ${(worldBudgetUsed / 1048576) | 0}MB / ${(WORLD_BUDGET / 1048576) | 0}MB）` });
171	        return;
172	      }
173	      const world = worldFromSaveJson(body.save);
174	      const room = new Room(world);
175	      room.opts.code = newCode();
176	      room.opts.maxPlayers = Math.min(255, Math.max(2, body.maxPlayers ?? DEFAULT_MAX_PLAYERS));
177	      if (body.name) world.name = body.name, room.opts.name = body.name;
178	      room.opts.publicRoom = !!body.public;
179	      room.opts.protectTiles = !!body.protectTiles;
180	      room.opts.protectItems = !!body.protectItems;
181	      room.opts.hostToken = randomUUID();
182	      worldBudgetUsed += estBytes || world.w * world.h * BYTES_PER_TILE;
183	      rooms.set(room.opts.code, { room, createdAt: Date.now(), bytes: estBytes || world.w * world.h * BYTES_PER_TILE });
184	      console.log(`[room] 创建 ${room.opts.code}（${world.name} ${world.w}×${world.h} 公开=${room.opts.publicRoom} 破坏保护=${room.opts.protectTiles} 物品保护=${room.opts.protectItems} 上限=${room.opts.maxPlayers}人 预算=${(worldBudgetUsed / 1048576) | 0}/${(WORLD_BUDGET / 1048576) | 0}MB）`);
185	      finish(200, {
186	        ok: true, code: room.opts.code, hostToken: room.opts.hostToken,
187	        name: room.opts.name, protectTiles: room.opts.protectTiles, protectItems: room.opts.protectItems,
188	      });
189	      return;
190	    }
191	    // DELETE /rooms/<code>?token= → 房主关房（--world 常驻房不可关）
192	    if (req.method === 'DELETE' && m) {
193	      const entry = rooms.get(m[1]);
194	      if (!entry) { finish(404, { ok: false, error: '房间不存在' }); return; }
195	      if (entry.room.persistent) { finish(403, { ok: false, error: '常驻房不可关闭' }); return; }
196	      if (url.searchParams.get('token') !== entry.room.opts.hostToken) {
197	        finish(403, { ok: false, error: '仅房主可关房' }); return;
198	      }
199	      removeRoom(m[1]);
200	      finish(200, { ok: true });
201	      return;
202	    }
203	    // GET /lan → 本机信息（IP 分享 + 发现端点）
204	    if (req.method === 'GET' && url.pathname === '/lan') {
205	      finish(200, { ok: true, magic: 1010, port: PORT, rooms: rooms.size, lanIps: lanIps() });
206	      return;
207	    }
208	    finish(404, { ok: false, error: 'not found' });
209	  } catch (e) {
210	    finish(400, { ok: false, error: (e as Error).message });
211	  }
212	});
213	lobby.listen(PORT + 1);
214	
215	// ================= WebSocket（URL = /<房间码>?token=<房主令牌可选>） =================
216	
217	const wss = new WebSocketServer({ port: PORT, maxPayload: 1 << 20 });
218	
219	wss.on('connection', (ws: WebSocket, req) => {
220	  ws.binaryType = 'nodebuffer';
221	  const m = (req.url ?? '').match(/^\/(\d{6})/);
222	  if (!m) { ws.close(1002, '需要房间码路径 /<6位码>'); return; }
223	  const entry = rooms.get(m[1]);
224	  if (!entry || entry.room.closed) { ws.close(1002, '房间不存在'); return; }
225	  const room = entry.room;
226	  const token = new URL(req.url ?? '/', 'http://x').searchParams.get('token') ?? '';
227	  const session = new URL(req.url ?? '/', 'http://x').searchParams.get('session') ?? '';
228	  const c = room.newClient(ws, token);
229	  if (session) room.resumeSession(c, session); // 断线重连：命中则 Hello 时同 slot 复位
230	  console.log(`[ws] 连入房间 ${room.opts.code}`);
231	
232	  ws.on('message', (data: Buffer) => {
233	    c.stats.inBytes += data.length;
234	    c.parser.append(new Uint8Array(data));
235	    try {
236	      c.parser.drain((msgId, r) => room.handle(c, msgId, r));
237	    } catch (e) {
238	      console.error(`[ws] 房间 ${room.opts.code} slot ${c.slot} 异常断开:`, (e as Error).message);
239	      try { ws.close(1002); } catch { /* 已关闭 */ }
240	    }
241	    // P1.3 合包：本条 WS 消息处理完毕，统一冲洗各客户端发送队列
242	    room.flushOutbox();
243	  });
244	  ws.on('close', () => {
245	    room.disconnect(c);
246	    room.flushOutbox();
247	    console.log(`[ws] slot ${c.slot} 离开房间 ${room.opts.code}（在线 ${room.onlineCount}）`);
248	  });
249	  ws.on('error', () => { /* close 跟上 */ });
250	});
251	
252	// 超时看门狗：逐房逐客户端（未握手 10s / 已握手 120s，对齐原版 TimeOutTimer）
253	setInterval(() => {
254	  for (const entry of rooms.values()) {
255	    for (const c of [...entry.room.clients]) {
256	      c.lastSeen += 1;
257	      if (c.lastSeen > (c.state >= 1 ? 120 : 10)) {
258	        console.log(`[ws] 房间 ${entry.room.opts.code} slot ${c.slot} 超时踢出`);
259	        c.ws.close();
260	      }
261	    }
262	  }
263	}, 1000);
264	
265	// 时间同步：服务器权威时钟推进（对齐原版 WorldGen.UpdateWorld 时钟）+ 10s 广播
266	setInterval(() => {
267	  for (const entry of rooms.values()) entry.room.world.clock.tick(1000);
268	}, 1000);
269	setInterval(() => {
270	  for (const entry of rooms.values()) {
271	    const room = entry.room;
272	    const f = new NetWriter(18).f64(room.world.clock.timeOfDay).u32(room.world.clock.dayCount).finish();
273	    for (const c of room.clients) if (c.state >= 10) room.send(c, f);
274	    room.flushOutbox();
275	  }
276	}, 10000);
277	
278	// ================= P0.1 观测：1s outBps 采样 =================
279	startBpsSampler(() => [...rooms.values()].map((e) => e.room));
280	
281	// ================= P3.1 持久化：--world 常驻房 + 定时落盘 + 信号退出 =================
282	if (WORLD_FILE) {
283	  try {
284	    const json = fs.readFileSync(WORLD_FILE, 'utf8');
285	    const world = worldFromSaveJson(json);
286	    const room = new Room(world);
287	    room.opts.code = newCode();
288	    room.opts.publicRoom = true;
289	    room.opts.hostToken = '';        // 无主房：首位进房者为房主（NPC 权威源）
290	    room.opts.maxPlayers = DEFAULT_MAX_PLAYERS;
291	    room.persistent = true;
292	    const bytes = world.w * world.h * BYTES_PER_TILE;
293	    worldBudgetUsed += bytes;
294	    rooms.set(room.opts.code, { room, createdAt: Date.now(), bytes });
295	    console.log(`[room] --world 常驻房 ${room.opts.code}（${world.name} ${world.w}×${world.h} 上限=${room.opts.maxPlayers}人）`);
296	  } catch (e) {
297	    console.error(`[server] --world ${WORLD_FILE} 载入失败:`, (e as Error).message);
298	    process.exit(1);
299	  }
300	}
301	
302	const roomList = () => [...rooms.values()].map((e) => e.room);
303	setInterval(() => {
304	  const r = saveRooms(roomList(), WORLDS_DIR);
305	  if (r.saved) console.log(`[persist] auto-save：${r.saved} 房落盘，${r.skipped} 房跳过`);
306	}, SAVE_INTERVAL * 1000).unref?.();
307	
308	let shuttingDown = false;
309	function shutdown(sig: string) {
310	  if (shuttingDown) return;
311	  shuttingDown = true;
312	  console.log(`[server] 收到 ${sig}，落盘全部房间…`);
313	  try {
314	    const r = saveRooms(roomList(), WORLDS_DIR);
315	    console.log(`[persist] 退出存档：${r.saved} 房保存，${r.skipped} 房跳过`);
316	  } catch (e) {
317	    console.error('[persist] 退出存档失败:', (e as Error).message);
318	  }
319	  process.exit(0);
320	}
321	process.on('SIGTERM', () => shutdown('SIGTERM'));
322	process.on('SIGINT', () => shutdown('SIGINT'));
323	
324	process.on('uncaughtException', (e) => {
325	  console.error('[server] uncaughtException（记录不退出）:', (e as Error).stack ?? e);
326	});
327	
328	console.log(`[server] 中央服务器 ws://0.0.0.0:${PORT}（lobby http://0.0.0.0:${PORT + 1}/rooms）`);
329	

```


---

## 🤖 Assistant · 2026-08-12T05:58:18.487Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/entitySyncHooks.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:58:18.497Z

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

## 🤖 Assistant · 2026-08-12T05:59:30.673Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important observations accumulating:

1. Watchdog bug-adjacent: `c.lastSeen += 1` every 1s, and in `handle()` `c.lastSeen = 0;` — resets on ANY message. So a malicious client that stops sending msg13 but keeps sending Ping (30s client ping timer — actually ClientNet sends ping every 30s independent) stays alive indefinitely. Ping is prio=0 and small, so the blind-end state can persist for the entire session (until client closes). So blind-end invulnerability window = unlimited, not 120s. Actually even legit clients: if a client is tabbed/backgrounded, fixedUpdate stops → msg13 stops → ping timer keeps firing (30s interval) → watchdog never kicks → blind indefinitely → no NPC updates → but that's a legit degraded state.

Also note: does ClientNet send msg13 independent of fixedUpdate? tick() is called from Game fixedUpdate. If the game loop is paused (background tab), msg13 stops but ping continues (setInterval independent). So blind state persists for legit players in background tabs. This makes blind-end a persistent state for any client that throttles.

2. Blind-end immunity claim: need to verify. If a visitor stops sending msg13, server marks blind → skips msg23/27 broadcast → no puppets created → netPuppetContact/netPuppetProjContact have no targets → immune to NPC/projectile damage. But wait — is that true? Existing puppets already created before going blind: they stop receiving snapshots; after 300 ticks (5s) they're swept (netSweepPuppets) → removed. So after ~5s the attacker has zero puppets → full immunity to hostile NPCs/projectiles. Meanwhile the attacker still receives... nothing entity-wise. But can the attacker still attack NPCs? To strike, the visitor needs a local puppet entity to hit (swingHits checks enemies including puppets). Without puppets, they can't deal damage either. But they can still: mine tiles (if protectTiles off), move around, take no damage. Also other players' projectiles... immaterial.

Cost-benefit: attacker gives up dealing damage to NPCs but becomes invincible to all PvE. For boss fights this is huge (e.g., tank boss invincibly). Also they keep receiving msg13 of others? broadcastAt for other players' msg13 — the blind check applies: broadcastAt checks aoiBlind → skip. So they don't see other players either. They do receive tile batches (broadcast, no AOI) and chest sync, chat, msg16.

Is it a real vulnerability? Yes — feasible with a trivial mod (withhold msg13, keep Ping). Detection: server counts stalePos. Mitigation: blind clients should be kicked after a shorter grace (e.g. 15s blind → kick), or blind clients still receive hostile projectile frames (but then saturation loop concern returns), or server-side damage arbitration (out of scope for P5?). Simplest: watchdog on "last msg13 age" separate from general liveness — kick if blind >10s while state>=10. Legit background-tab clients would be kicked though — but currently they're frozen anyway. Hmm, vanilla: client in background doesn't get kicked because msg13 stops? In vanilla, timeout is on any traffic; client keeps sending? Actually vanilla client sends msg13 from its game loop too. Anyway.

Rating: 必须修 (or 建议修). Given it's a full PvE invulnerability exploit with trivial cost, and this is a game where combat matters — I'd say 建议修→必须修. The question asks "是不是真实漏洞?代价收益比?" I'll analyze: yes real, cost trivial, benefit high (invincible tank), mitigations.

3. Client-authoritative HP + item injection chain. Key exploit chain found above: msg21 op=0 unvalidated relay — any client can broadcast fake drops with arbitrary key+stack; other clients create real ItemDrop puppets; auto-pickup (exempt from protectItems) puts them into inventory. Then putting into chest (protectItems off) or just keeping = item duplication/injection, defeating protectItems (which only guards chest edits by non-host, and even with protectItems ON the injection into personal inventory works; chest placement blocked but personal inventory already has infinite items; and they can use/place them in world? protectTiles would block tile placement by non-host... but weapons etc. fine).

Wait — check: does pickup of a puppet drop actually add to the picker's inventory? Let me verify the ItemDrop pickup code path in Game to be careful. Also does protectItems gate pickup? Design says auto-pickup exempt. Let me grep pickup.

Also the msg21 relay has no owner check: netId high byte should equal sender slot. Server doesn't verify netId>>>24 === c.slot. So a visitor can also forge netIds of the host's drops, spawn fake drops attributed to host, and send take for host's real drops (despawn theft/denial). And op=0 spawn has no rate limit → bandwidth amplification? It's broadcast to all clients (no AOI for msg21) — a spammer can flood. n? msg21 is single-op per frame, batched client-side up to 64 frames per WS message. Server relays each. Rate unlimited → broadcast flood (prio=0! not prio=1, so backpressure won't drop until 4MB). Actually msg21 relay uses this.broadcast(f.finish(), c) with default prio=0 → never dropped until >4MB. DoS vector + item injection. 必须修: validate netId owner + gate op=0 key to known item keys + rate limit.

Let me check ITEM validation: server has ITEM_DEFS — key validation possible via ITEM_BY_KEY equivalent server-side? Server imports ITEM_DEFS (id array). Key→id map may exist in game data. Check.

4. Malicious host: 
- Forge msg23 fake NPC positions/hp: host is NPC authority — can teleport bosses onto visitors, set hp=1 etc. But visitors' damage goes through msg42 → host settles. Host can refuse to apply damage (ignore strikes) → unkillable NPCs; or fake hp display. Impact: griefing visitors. Necessity: host-authority is a deliberate architecture (host runs full sim, zero server CPU). Acceptable tradeoff for co-op with friends; document.
- Forge msg27 kind|0x80 hostile with dmg=32767 → forced PvP on visitors. Vanilla has PvP flag server-enforced (msg13/`player.hostile` checked in Damage_EVP — vanilla checks `p.hostile` for PvP). We have no PvP flag at all, so any hostile projectile damages. From a visitor perspective, a malicious host can kill them. But since HP is client-authoritative, the visitor can just... take the damage locally (their client computes hitPlayer → damagePlayer). They could mod their client to ignore it. So forced PvP from host is mitigated by client-authoritative HP — the victim can cheat back. It's symmetric cheating; record/建议.
- Forge msg21 op=0 → item injection (same as #3 but host is trusted anyway; host owns the world).

5. AOI radii: AOI_PLAYER=1920px (120t), AOI_ENTITY=1280 (80t), hysteresis 1.6×=2048. Screen 1920×1080 @100% zoom... in this game, what's the viewport? The claim: 1920×1080 px ≈ 120×67.5 tiles. AOI_PLAYER 1920px Chebyshev: a remote player at screen edge horizontally (x offset ~960px from center) is visible; at 1920px they're outside. So for wide screens two players can see each other while >1920px apart? If both are 1000px from center on opposite sides... no — Chebyshev distance between them would be 2000px > 1920 → they wouldn't see each other though both are on... wait each sees the other only if within their own screen. If A is at x=0 and B at x=2000, A can't see B on a 1920-wide screen anyway (B is 1000px beyond right edge? screen half-width 960px). So 1920 Chebyshev vs 1920 screen width: two players exactly at mutual distance 1920 are both invisible to each other on a 1920 screen (each 960px off-center = exactly at edge). OK fine. But vertical: screen height 1080 → half 540px; Chebyshev 1920 allows vertical offset up to 1920 → way beyond vertical screen — extra is fine (conservative direction). The problem direction is entities at 1280px: entity Chebyshev radius 1280px vs screen half-width 960px. An entity 1000px away horizontally is on-screen (just) but beyond AOI_ENTITY=1280? No: 1000 < 1280 → included. Entity at 1300px: not visible on 1920 screen (beyond 960 half-width)... but visible on wider screens/zoomed out. What about weapons: bow range ~1500px+ — you can shoot beyond 1280px. Your own arrow's snapshots broadcast (owner always broadcasts own projectiles to others filtered by *receiver* AOI). For the shooter, own projectiles are local (no filtering). For the victim: hostile arrow at distance >2048 → filtered. A sniper shooting from 2000px: victim receives nothing until arrow closes within 1280 (or hysteresis). So "hit by invisible source" is possible: arrow appears mid-flight at 1280-2048px (hysteresis band: if it was never visible, it enters at ≤1280; so first seen at 1280px = 80 tiles ≈ 1.3 screens away). So victim sees arrow pop in at 1280px and has ~? arrow speed. That's mostly fine visually. But mid-flight stop/resume: an arrow that exits the 2048 hysteresis radius gets dropped, and its puppet is swept after 180 ticks (3s) client-side... actually puppet sweep is 180 tick for proj. When re-entering, a new puppet is created at the latest position — trajectory appears broken/teleporting. For long-range projectiles (sniper/harp) that travel beyond 2048px from receiver while receiver stationary... wait receiver stationary, projectile path: starts at shooter (say 2000px away, not visible), approaches — once within 2048 and never visible → hysteresis band rule: dist > AOI_ENTITY(1280) && !wasVisible → skip. So it only becomes visible at ≤1280. No mid-flight drop unless path exits >2048 after being visible. E.g. magic harp bouncing/boomerang projectiles that fly past the player and loop back: enters at 1280, exits at 2048 → dropped, re-enters at 1280 → recreated. Trajectory break + damage flicker. Verdict: 边界战斗 minor inconsistency; the bigger issue: PvP between players 1280-1920 apart: you can see the player (AOI_PLAYER 1920) but their projectiles are not relayed to you (AOI_ENTITY 1280) → "看得见人打不着弹幕" and hostile projectiles from them won't reach you either (you're immune from them, they from you). That's a real gameplay gap for ranged PvP at 80-120 tile distance. Also mob aggro: NPC at 1000px chases you but its snapshot stops at >2048 — fine.

Also asymmetric: AOI filter based on receiver's last msg13 position — a fast-moving player's stale position (up to 66ms + latency) causes filter errors at edges. Minor.

6. Backpressure semantics: prio=1 drop is silent; client puppets swept at 180/300 ticks then rebuilt when frames resume. "怪闪烁消失重现" — actually worse: NPC short-code known-marking is done correctly post-send. But note the known-set trick: if a frame is dropped, code not marked → next full resend. OK self-healing. Is degradation self-consistent? Mostly yes. Improvements: client-side extrapolation already exists (netSnapTo + velocity extrapolation "到点后纯速度外推") so during short drops puppets keep moving; sweep at 300t happens only if no snapshot for 5s. A client under sustained 1-4MB buffer would lose all prio=1 → all NPCs swept → then buffer drains → rebuilt. Flicker. Better: link sweep threshold to drop indication — e.g., server sends a "snapshot gap" marker, or client extends puppet lifetime when it knows drops occurred (stats not visible to client though). Simplest: server, when dropping prio=1 frames for a client, sends a tiny prio=0 "entity-stream-paused" flag msg so client suspends sweeping and keeps extrapolating. Suggest.

Also note: backpressure thresholds are per-client ws buffer; >4MB drops everything including prio=0 (chat, policy, tile ops relay!) — dropping tile batches at >4MB → world divergence (client misses tile changes permanently; no replay). That's worse than flicker: silent permanent divergence. Also chest frames dropped → chest desync until reopen. And msg16 dropped → HP display stale. Tile ops: no correction mechanism (unlike protectTiles correction which only fires on rejection). So at >4MB, permanent world divergence. Must-note: 建议 — on exiting overload, server could send full-strip re-sync or clients re-request strips. Record/建议修.

7. Persistence economics: saveRooms every 300s; dirty flags per room; but the dirty check: lastSavedTileOps/lastSavedChestEdits baseline — updated where? Let me check persist.ts. Also crash window: up to 300s of tile/chest edits lost on SIGKILL. Reasonableness: for an ops-facing server, 300s default is loose; consider event-count-triggered save (e.g., every 1000 tileOps) or reduce interval. Multi-room simultaneous write IO spike: saveRooms iterates all rooms synchronously in one setInterval — all worlds serialized at once → IO spike + tick blocking (Node single thread: a big JSON.stringify of a 6400×1800 world blocks the event loop → all rooms' WS stall). That's a real反噬: auto-save of many large worlds blocks the single-threaded server, causing exactly the saturation that triggers backpressure drops and blind-end kicks. Check persist.ts for atomicity (tmp+rename claimed in doc).

8. Trust asymmetry: msg13 position fully trusted — forged position affects others' AOI? The receiver filter uses *receiver's own* lastX/lastY, not sender's. A forged sender position only affects: (a) what the sender sees (they can position themselves to receive any region's entity stream — info leak: watching NPC/boss fights anywhere by teleporting their reported position); (b) broadcastAt(x,y,AOI_PLAYER) for their own msg13 relay — others see the fake player position. Forged SpawnTileData → server sends 5×5 strips around ANY coordinates — info leak: full world tile data readable by strips (a visitor can enumerate the whole map: 200×20 strips; for 6400×1800 world = 32×90 = 2880 strips ≈ each up to ~52KB → 150MB to map the whole world). sentStrips dedupes per client, but a fresh connection re-requests. So yes, entire world map exfiltration is possible for any room member (including chest *positions* from tile data? chest contents aren't in strip msg10; chest contents only via msg31 by coordinates — findChestNear needs anchor within ±1. From tile data you learn chest tile positions but not anchor exactly; you can brute-force msg31 around it — ±1 tolerance, so a few requests get contents). So chest contents (potentially the "protected" valuables) are fully readable by any visitor regardless of protectItems. protectItems protects edits, not reads. Is that a problem? The room owner uploaded the world; visitors can download everything. 建议修/记录: rate-limit SpawnTileData + document.

Also forged position: teleport in msg13 lets a cheater appear anywhere to others without moving (client-authoritative position = vanilla same). And AOI abuse: claim to be near a boss to receive its snapshots (info) — minor.

9. Host failover: hostJoined=false on host disconnect → next token-holder or first-joiner becomes host. But look: the check is in Hello handler: `if (!this.hostJoined && ((token && token === this.opts.hostToken) || this.opts.hostToken === ''))`. For a token room (POST /rooms created), if host leaves and a visitor without token is already in the room... hostJoined=false, but no new Hello happens from existing clients → room stays hostless until a new connection arrives with token, or... wait for token rooms (hostToken !== ''), a new joiner without token does NOT become host. So after host leaves a token room, no one can ever become host again unless the original host reconnects with token! NPC authority gone → no msg23 → all puppets swept after 5s → no NPCs for everyone, permanently. Also strikeTarget() returns null → visitors can't damage NPCs (their strikes dropped). And drops: visitor's own drops still work. So host departure = world becomes NPC-dead. That's a liveness problem: 建议修 (failover to longest-present member, with announcement).

For --world persistent rooms (hostToken=''): first joiner becomes host. New host's world state: client world built from server strips — tiles are server-authoritative so OK; but NPC/drops/chest? Chests are server authoritative too (msg31). NPC state: new host starts with zero NPCs (spawner starts fresh — visitors' puppets swept; new host sim starts spawning from scratch, possibly losing boss fight state, invasions). Drops: old host's real drops gone (puppets swept; new host never had them). Acceptable? Mostly yes, but boss fight reset without announcement. Also new host's spawn/AI uses its local world loaded from strips — if new host hasn't requested strips for the area... they have their own local world, fine.

But also a subtle issue: for token rooms, when host disconnects and reconnects within 60s (session resume), they become host again — good. After 60s, slot freed, they reconnect with token in URL → host again. OK.

Another failover subtlety: hostile bit gate idea (host-only) would break when a *visitor*... no, NPC arrows only from host sim. Fine.

Additional check: the 120s watchdog counts `c.lastSeen += 1` per second and resets to 0 in handle(). lastSeen init 0. State>=1 → 120s. Fine.

One more: `Msg.PlayerState` handler — no rate limit, no sanity clamp on x/y (f32 NaN/Infinity possible! A malicious client sending x=NaN → lastX=NaN → Math.abs(NaN - e.x) <= radius is false → that receiver gets nothing... NaN poisons only their own reception. But broadcast: f.f32(NaN) → all receivers NaN → their remote player proxy position NaN → possibly NaN propagation into physics/render. Also Infinity similar. Minor robustness note.

Also msg13 flooding: no rate limit server-side (design §8.6 spam check off). Each msg13 triggers a broadcastAt per receiver — O(N) relay. A flooder at max WS message rate (maxPayload 1MB!) can pack thousands of msg13 frames per WS message → server CPU amplification + broadcast flood to all clients. That's a DoS: 建议修 (rate limit msg13 to ~30/s).

Similarly msg27: n up to 64 entries per frame, frames unbounded per WS message → CPU + bandwidth amplification (server re-encodes per receiver). 建议修 rate limits.

Also `Msg.SyncNPC` n>64 return — good; msg27 n>64 return — good; but number of *frames* per second unbounded.

Chest exploit check: `Msg.SyncChestItem` — chestIdx u16 unchecked against... `const chest = this.world.chests[chestIdx]; if (!chest) return;` OK. Slots validated slot<10. But: visitor can edit chest even when protectItems is... gated. But when protectItems OFF, any visitor can set chest contents arbitrarily (stack clamped to maxStack, id validated) → chest content forgery = item creation. But that's the same trust level as client-authoritative inventory: they could just as easily edit their own inventory and deposit. So the real issue remains: client-authoritative inventory makes protectItems theater. The chain: visitor edits local inventory (mod) → syncInventory diff sends msg5 (validated only for id range/stack clamp) → server relays → others see items. Then visitor deposits into chest: msg32 (if protectItems off) → server applies to authoritative chest → persists to disk. So items are created from nothing and persisted. protectItems ON blocks chest deposit for non-host but they keep items in personal inv and can use them. So "物品保护" only protects the pre-existing chest contents from tampering, not the economy. That answers question 2: yes, contradiction — protectItems is advisory for inventory-side; it cannot enforce an economy. If运营 attribute matters, need SSC (server-side characters, §8.5) — the only real fix. Otherwise document as "保护=防误伤/防小白, not防外挂".

Let me quickly check pickup of puppet drops & protectItems exemption, persist.ts, and whether server has a key→id map for validating msg21 keys.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:59:31.244Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && cat server/src/persist.ts && grep -n \"ITEM_BY_KEY\\|ITEM_KEY\" game/src/data/items.ts | head -5 && grep -rn \"netPuppet\" game/src/entities/ItemDrop.ts game/src/core/Game.ts | grep -i \"pickup\\|collect\\|拾取\" | head",
 "description": "Read persist.ts and item key map availability"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:31.296Z

**📎 ToolResult**

```
// 服务器世界持久化（P3.1，docs/multiplayer-design.md §3.3）：
// 定时 auto-save + SIGTERM/SIGINT 落盘后退出 + --world 启动载入建常驻房。
// 语义边界：服务器档只保世界（tile/箱子/clock/flags/天气），不含玩家（无 SSC）——
// 房主物品栏权威在房主本地存档。
import fs from 'node:fs';
import path from 'node:path';
import type { Room } from './room.ts';
import { saveWorldOnly } from '../../game/src/save/SaveFile.ts';

export interface PersistResult { saved: number; skipped: number; }

/** 全部房间落盘：worlds/room-<code>.json（每房单文件覆盖写，原子 tmp+rename）。
 *  跳过条件：无人在局且自上次保存后无 tile 修改且无箱子编辑（空房不产生写放大；
 *  箱子编辑必须计入脏标记——否则"取物后离开"被跳过 → 服务器档残留物品 = 复制漏洞，review S1） */
export function saveRooms(rooms: Iterable<Room>, worldsDir: string): PersistResult {
  let saved = 0, skipped = 0;
  for (const room of rooms) {
    if (room.closed) continue;
    const rs = room.roomStats;
    if (room.onlineCount === 0 && rs.tileOps === room.lastSavedTileOps && rs.chestEdits === room.lastSavedChestEdits) {
      skipped++;
      continue;
    }
    try {
      fs.mkdirSync(worldsDir, { recursive: true });
      const file = path.join(worldsDir, `room-${room.opts.code}.json`);
      const tmp = `${file}.tmp`;
      fs.writeFileSync(tmp, saveWorldOnly(room.world), 'utf8');
      fs.renameSync(tmp, file);
      room.lastSavedTileOps = rs.tileOps;
      room.lastSavedChestEdits = rs.chestEdits;
      saved++;
    } catch (e) {
      console.error(`[persist] 房间 ${room.opts.code} 保存失败:`, (e as Error).message);
    }
  }
  return { saved, skipped };
}

/** 启动载入：--world <path> → 常驻房世界（hostToken='' = 无主房，首位进房者为房主） */
export function loadWorldFile(file: string): string {
  return fs.readFileSync(file, 'utf8');
}
72:export const ITEM_BY_KEY: Record<string, number> = byKey;
759:export const VANILLA_ITEM_KEY_BY_ID: Record<number, string> = {};
764:  VANILLA_ITEM_KEY_BY_ID[Number(idStr)] = ik; // 已注册的同样入表（wld 导入按 id 反查）
777:  VANILLA_ITEM_KEY_BY_ID[Number(mbVid)] = mbKey; // 掉落/录音链按 vid 反查
781:  const mbKey = VANILLA_ITEM_KEY_BY_ID[MUSIC_BOX_ITEM_BY_STYLE[mbStyle]];

```


---

## 🤖 Assistant · 2026-08-12T05:59:31.610Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"pickup\\|Pickup\\|拾取\" game/src/core/Game.ts | head -20",
 "description": "Find drop pickup logic in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:31.644Z

**📎 ToolResult**

```
398:  /** 物品保护：宝箱取放等受控（自动拾取不门禁——需求明确豁免） */
463:  // 访客渲染傀儡实体（无本地 AI），打击/拾取经上报由房主权威结算。
548:  /** 双向：本地真掉落诞生上报 + 消失（拾取/寿命）广播——扫描差分 */
562:      if (!cur.has(netId)) net.sendItemOp(1, netId); // 上轮在、本轮没 = 拾取/过期 → take
596:  /** msg21 回包：掉落物傀儡 upsert / take 移除（含拥有者本地真掉落被他人拾取） */
620:      // 拥有者的真掉落被他人拾取（访客 take 上报 → 房主在此移除真身）
686:        // 傀儡消失两源：本地拾取（dead 由 ItemDrop 置位）→ 上报 take 让房主移除真身；
1126:    // 战斗/挖掘/拾取等开局即用的 ~20 个小 wav；怪物专属声仍随首次受击懒加载）
1127:    this.sfx.preloadNames(['hit', 'hurt', 'killed', 'pkilled', 'pickup', 'dig', 'place',
4735:          this.sfx.play('pickup'); // SoundID 7（TryFitting :698）
4743:          this.sfx.play('pickup'); // SoundID 7（TEHatRack.cs:351）
4962:        this.sfx.play('pickup'); // SoundID 7（:41025 Grab）
4977:    this.sfx.play('pickup'); // SoundID 7（Player.cs:41040）
4983:   *  此处落在提取机顶格上方，带向上初速便于拾取） */
5692:        // 心/星雕像是 pickup 类物品（ItemID.Sets.IsAPickup）
5693:        if (d && vanillaItemId === 58) d.pickup = 'heart';
5694:        else if (d && vanillaItemId === 184) d.pickup = 'star';
6139:    /** 心 pickup（item 58 是 IsAPickup：触碰回血不进包——此处曾误当蘑菇收集物） */
6140:    const dropHeart = () => { const h = drop(58); if (h) h.pickup = 'heart'; };
6176:      // 心 pickup（WorldGen.cs:57511-57531）：1 颗 + 1/2 第二颗；

```


---

## 🤖 Assistant · 2026-08-12T05:59:32.978Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check the drop pickup code around line 4940-4990 in Game.ts to confirm puppet drops are pickable into real inventory.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:59:33.183Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 60,
 "offset": 4935
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:33.193Z

**📎 ToolResult**

```
4935	  /**
4936	   * 提取机对准使用（Player.cs:41008-41049 PlaceThing_ItemInExtractinator 1:1）。
4937	   * 优先级：642 叶绿版先查矿物兑换表（ItemTrader.ChlorophyteExtractinator，
4938	   * Player.cs:41024-41033 / ItemTrader.cs:82-108），命中则 1:1 兑换（SkipItemConsumption
4939	   * 语义——本方法自扣 stack）；否则按 ExtractinatorMode（ItemID.cs:1104）走转化表
4940	   * （:41034-41044 → ExtractinatorHelper.RollExtractinatorDrop，全表在
4941	   * world/Extractinator.ts）。原版消耗走通用 consumable 扣减（Player.cs:42602），此处等价
4942	   * 为手持格扣 1。642 使用间隔 ×0.33（:41018-41020）。
4943	   * @param viaUse true = 左键使用链（updateUse，受 useTime 冷却）；false = 右键交互
4944	   * @returns 是否成功转化/兑换（false 时调用方应回落到普通放置/使用）
4945	   */
4946	  private useExtractinator(tx: number, ty: number, viaUse: boolean): boolean {
4947	    const sheet = this.wiring?.sheetOf(tx, ty) ?? -1;
4948	    if (sheet !== 219 && sheet !== 642) return false;
4949	    const held = this.player.inv.heldItem();
4950	    if (!held) {
4951	      if (!viaUse) this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NeedExtractMaterial'));
4952	      return false;
4953	    }
4954	    const vid = slotVanillaId(held.id);
4955	    // 642 矿物兑换表优先（Player.cs:41024-41033：itemTrader.TryGetTradeOption）
4956	    if (sheet === 642) {
4957	      const give = CHLOROPHYTE_TRADES[vid];
4958	      if (give !== undefined) {
4959	        this.player.inv.removeAt(this.player.inv.selected, 1);
4960	        this.cb.onInventoryChanged();
4961	        this.dropFromExtractinator({ itemType: give, stack: 1 }, tx, ty);
4962	        this.sfx.play('pickup'); // SoundID 7（:41025 Grab）
4963	        if (viaUse) this.player.useTime = extractinatorUseTime(10, sheet);
4964	        return true;
4965	      }
4966	    }
4967	    const mode = extractinatorMode(vid);
4968	    if (mode < 0) {
4969	      // 手持不可提取物：use 链回落到放置/挥砍；interact 提示
4970	      if (!viaUse) this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NeedExtractMaterial'));
4971	      return false;
4972	    }
4973	    const drop = rollExtractinatorDrop(mode, sheet, mathRand(), this.world.flags.hardMode);
4974	    this.player.inv.removeAt(this.player.inv.selected, 1);
4975	    this.cb.onInventoryChanged();
4976	    this.dropFromExtractinator(drop, tx, ty);
4977	    this.sfx.play('pickup'); // SoundID 7（Player.cs:41040）
4978	    if (viaUse) this.player.useTime = extractinatorUseTime(10, sheet);
4979	    return true;
4980	  }
4981	
4982	  /** 转化产物掉落（Player.cs:41426-41436 DropItemFromExtractinator：鼠标世界坐标生成；
4983	   *  此处落在提取机顶格上方，带向上初速便于拾取） */
4984	  private dropFromExtractinator(drop: ExtractDrop, tx: number, ty: number): void {
4985	    if (drop.itemType <= 0) return;
4986	    const key = COIN_KEY_BY_VID[drop.itemType] ?? VANILLA_ITEM_KEY_BY_ID[drop.itemType];
4987	    if (key && ITEM_BY_KEY[key] !== undefined) {
4988	      this.spawnDrop(tx * TILE + 24, (ty - 1) * TILE, key, drop.stack, 0, -2);
4989	    }
4990	  }
4991	
4992	  /**
4993	   * 提取机通电消耗源（Wiring.cs:2572-2592）。箱子查找/箱内消耗为纯函数
4994	   * （world/Extractinator.ts，对应 TryFindChestForExtractinator :2596-2622 与

```


---

## 🤖 Assistant · 2026-08-12T05:59:34.695Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Not the pickup code. Let me grep for where drops are collected into inventory (entities.drops loop with inv.add).
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:59:35.541Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -n \"drops\" game/src/core/Game.ts | grep -vn \"netDrop\\|entities.drops)\" | sed -n '1,30p'; echo ---; grep -n \"inv.add\\|canPickup\\|vacuum\" game/src/core/Game.ts | sed -n '1,30p'",
 "description": "Locate drop collection into inventory"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:35.584Z

**📎 ToolResult**

```
1:161:import type { DropExtras } from '../drops/NpcDrops';
3:606:        this.entities.add(d, 'drops');
7:4235:    const drops: Array<[string, number]> = !this.world.flags.shadowOrbSmashed
8:4238:    for (const [key, n] of drops) {
10:7561:    this.entities.add(drop, 'drops');
11:7564:    const drops = this.entities.drops;
12:7565:    while (drops.length > 400) drops.shift();
---
747:      const left = p.inv.add(ITEM_BY_KEY[def.key], n);
1280:    this.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
1281:    this.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
1282:    this.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
4768:          const left = this.player.inv.add(taken.item.id, taken.item.stack);
7301:    if (key && ITEM_BY_KEY[key] !== undefined) this.player.inv.add(ITEM_BY_KEY[key], 1);
7468:    if (gold) inv.add(ITEM_BY_KEY['coin_gold'], gold);
7469:    if (silver) inv.add(ITEM_BY_KEY['coin_silver'], silver);
7470:    if (copper) inv.add(ITEM_BY_KEY['coin_copper'], copper);
7508:    if (plat) inv.add(ITEM_BY_KEY['coin_platinum'], plat);
7509:    if (gold) inv.add(ITEM_BY_KEY['coin_gold'], gold);
7510:    if (silver) inv.add(ITEM_BY_KEY['coin_silver'], silver);
7511:    if (copper) inv.add(ITEM_BY_KEY['coin_copper'], copper);
8578:    this.player.inv.add(ITEM_BY_KEY[r.out], r.count);
8641:    const left = this.player.inv.add(ITEM_BY_KEY[outKey], r.createStack * times);
8651:    const left = this.player.inv.add(ITEM_BY_KEY[outKey], r.createStack);

```


---

## 🤖 Assistant · 2026-08-12T05:59:36.980Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 50,
 "offset": 7530
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:36.991Z

**📎 ToolResult**

```
7530	    };
7531	  }
7532	
7533	  /** 月事件掉落上下文（NpcDrops 四个 wave-gate 条件数据源）；无事件返回 null */
7534	  moonEventCtx(): { kind: 1 | 2; wave: number } | null {
7535	    const me = this.world.moonEvent;
7536	    return me.kind === 0 ? null : { kind: me.kind, wave: me.waveNumber };
7537	  }
7538	
7539	  enemies() {
7540	    return this.entities.enemies;
7541	  }
7542	
7543	  /** 小动物列表:弹幕命中用(GameHooks.critters) */
7544	  critters() {
7545	    return this.entities.critters;
7546	  }
7547	
7548	  /** 弹幕砍 tileCut 物（Projectile.CutTiles 语义）：瓦罐→整罐碎裂，其余→breakTile */
7549	  cutTile(x: number, y: number) {
7550	    const st = this.world.store;
7551	    if (!st.inBounds(x, y)) return;
7552	    const t = st.get(x, y);
7553	    if (t === POT_TILE) this.smashPot(x, y);
7554	    else if (TILE_CUT.has(t)) this.breakTile(x, y);
7555	  }
7556	
7557	  spawnDrop(x: number, y: number, itemKey: string, count = 1, vx = 0, vy = -2): ItemDrop | null {
7558	    const id = ITEM_BY_KEY[itemKey];
7559	    if (id === undefined) return null;
7560	    const drop = new ItemDrop(x - 6, y - 6, id, count, vx, vy);
7561	    this.entities.add(drop, 'drops');
7562	    // 原版 Main.item 槽位上限 400,超出移除最旧掉落(Main.UpdateItems 空 slot 回收)——
7563	    // 此前无上限:dev 模式一次 ~500 实体/雕像农场线性堆积(2026-08 审计 #10)
7564	    const drops = this.entities.drops;
7565	    while (drops.length > 400) drops.shift();
7566	    return drop;
7567	  }
7568	
7569	  damagePlayer(dmg: number, srcX: number, srcY: number, attacker?: Enemy) {
7570	    const p = this.player;
7571	    if (p.dead) return;
7572	    if (attacker) p.lastDamageCause = { kind: 'npc', name: (attacker.vanillaId != null ? Lang.npcName(attacker.vanillaId) : null) ?? attacker.def.name };
7573	    const ok = p.damage(dmg, srcX, srcY);
7574	    if (ok) {
7575	      // 星星斗篷（Player.SpawnStar 近似）：受击召 3 颗落星砸附近敌人
7576	      if (p.equipStats.starCloak) this.spawnStarCloakStars();
7577	      // 蜂蜜斗篷/蜂巢背带（Player.SpawnBees :2147 近似）：受击放 1-3 只蜂（proj 181/183/189）
7578	      if (p.equipStats.bees) {
7579	        const n = 1 + Math.floor(Math.random() * 3);

```


---

## 🤖 Assistant · 2026-08-12T05:59:39.034Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Pickup logic — where do drops get picked up by the player? Let me search for where ItemDrop is collected (maybe in ItemDrop.update or in a Game loop "updateDrops"). Grep "pickupRange\|itemNoGrabDelay\|Grab" or entities update.
```

</details>


---

## 🤖 Assistant · 2026-08-12T05:59:39.690Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -rn \"netPuppet\" game/src/entities/*.ts game/src/entities/**/*.ts 2>/dev/null | head -20; echo ===; grep -rln \"pickup\" game/src/entities/ | head",
 "description": "Find ItemDrop pickup implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:39.729Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
game/src/entities/Arrow.ts:135:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Entity.ts:17:  netPuppet = false;
game/src/entities/Entity.ts:40:  netPuppetStep() {
game/src/entities/FallingBlock.ts:33:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Dart.ts:205:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Dart.ts:575:    ctx.globalAlpha = this.netPuppet ? 1 : Math.max(0, 1 - this.alpha / 255); // 傀儡不跑 dartStep,alpha 恒初始 → 恒可见
game/src/entities/Dart.ts:609:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Enemy.ts:414:    if (this.netPuppet) {
game/src/entities/Enemy.ts:417:      this.netPuppetStep();
game/src/entities/Enemy.ts:3963:    if (this.netPuppet) entityNet.reportStrike?.(this.netId, rawDmg, kbx, kby);
game/src/entities/Enemy.ts:3996:      if (this.vanillaId === 16 && !this.netPuppet) {
game/src/entities/Enemy.ts:4025:      if (this.vanillaId && !this.netPuppet) {
game/src/entities/MagicProj.ts:41:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/WeaponProj.ts:113:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/WeaponProj.ts:184:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/WeaponProj.ts:251:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Dart.ts:205:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Dart.ts:575:    ctx.globalAlpha = this.netPuppet ? 1 : Math.max(0, 1 - this.alpha / 255); // 傀儡不跑 dartStep,alpha 恒初始 → 恒可见
game/src/entities/Dart.ts:609:    if (this.netPuppet) { this.netPuppetStep(); return; }
game/src/entities/Arrow.ts:135:    if (this.netPuppet) { this.netPuppetStep(); return; }
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T05:59:41.483Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && grep -rln \"pickup\" game/src/entities/ 2>/dev/null | head; echo \"---\"; grep -rn \"class ItemDrop\" game/src/entities/ | head -3",
 "description": "Find ItemDrop class and pickup logic"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:41.521Z

**📎 ToolResult**

```
game/src/entities/Enemy.ts
game/src/entities/ItemDrop.ts
---
game/src/entities/ItemDrop.ts:9:export class ItemDrop extends Entity {

```


---

## 🤖 Assistant · 2026-08-12T05:59:42.862Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T05:59:42.876Z

**📎 ToolResult**

```
1	// 掉落物实体：重力、落地、磁吸拾取
2	import { Entity } from './Entity';
3	import type { GameHooks } from './types';
4	import { GRAVITY, MAX_FALL_SPEED, MAGNET_RADIUS, PICKUP_DELAY, TILE } from '../core/constants';
5	import { moveAndCollide } from '../physics/TileCollision';
6	import { ITEM_DEFS } from '../data/items';
7	import type { Player } from './Player';
8	
9	export class ItemDrop extends Entity {
10	  w = 12; h = 12;
11	  itemId: number;
12	  stack: number;
13	  age = 0;
14	  bobPhase: number;
15	  /** 原版 Item.color（凝胶等掉落继承怪物色，逐像素乘法贴轮廓渲染） */
16	  color?: number[]; // [r, g, b, a]
17	  /** 心(58)/星(184) 是 pickup 类物品（ItemID.Sets.IsAPickup, ItemID.cs:248）：
18	   *  碰触即回血 20 / 回蓝 100 并消失，永不进背包（Player.PickupItem :34610-34630） */
19	  pickup?: 'heart' | 'star';
20	
21	  constructor(x: number, y: number, itemId: number, stack = 1, vx = 0, vy = -2) {
22	    super();
23	    this.x = x; this.y = y;
24	    this.itemId = itemId;
25	    this.stack = stack;
26	    this.vx = vx;
27	    this.vy = vy;
28	    this.bobPhase = Math.random() * Math.PI * 2;
29	  }
30	
31	  fixedUpdate(dt: number, game: GameHooks) {
32	    this.age++;
33	    // 寿命（10 分钟）
34	    if (this.age > 60 * 600) { this.dead = true; return; }
35	
36	    const player = (game as unknown as { player: Player }).player;
37	    let beingGrabbed = false;
38	    if (player && !player.dead && this.age > PICKUP_DELAY) {
39	      // 原版 GrabItems(Player.cs:34461-34524):hitbox 相交=直接拾取;
40	      // 否则玩家盒 ±42px(defaultItemGrabRange :2406)扩展盒相交=拉取；
41	      // 宝藏磁石(+94)/金戒指族(+12)扩展范围（Player.grabRangeBonus 聚合）
42	      const GRAB_RANGE = 42 + ((player as { grabRangeBonus?: number }).grabRangeBonus ?? 0)
43	        // 拾心药水（lifeMagnet）：红心单独扩大拾取范围
44	        + (this.pickup === 'heart' ? ((player as { heartGrabBonus?: number }).heartGrabBonus ?? 0) : 0)
45	        // 魔力磁石（manaMagnet：星 184/1735/1868 专用吸附，Player.cs:34495 专属拉取通道）
46	        + (this.pickup === 'star' ? ((player as { manaMagnetBonus?: number }).manaMagnetBonus ?? 0) : 0);
47	      const touching =
48	        this.x < player.x + player.w && this.x + this.w > player.x &&
49	        this.y < player.y + player.h && this.y + this.h > player.y;
50	      const inGrabRange =
51	        this.x < player.x + player.w + GRAB_RANGE && this.x + this.w > player.x - GRAB_RANGE &&
52	        this.y < player.y + player.h + GRAB_RANGE && this.y + this.h > player.y - GRAB_RANGE;
53	      if (touching) {
54	        // 心/星 pickup：直接回复并消失，不进背包（原版拾取即 Heal(20)/mana+100+ClearOut）
55	        if (this.pickup) {
56	          if (this.pickup === 'heart') {
57	            player.hp = Math.min(player.maxHp, player.hp + 20);
58	            game.addDamageNumber(player.cx, player.y, 20, false, '#40E080');
59	          } else {
60	            player.mana = Math.min(player.maxMana, player.mana + 100);
61	            game.addDamageNumber(player.cx, player.y, 100, false, '#4080FF');
62	          }
63	          this.dead = true;
64	          game.playSfx('pickup', 0.75); // 原版 SoundID 7 Grab
65	          return;
66	        }
67	        const before = this.stack;
68	        const left = player.inv.add(this.itemId, this.stack);
69	        if (left === 0) {
70	          this.dead = true;
71	          game.notifyInventoryChanged();
72	          // 铜币拾取用专属音效，其余走通用拾取
73	          // 音量略低（0.75）：拾取与挖掘声同时触发时两者都可闻，不被 Grab 盖住
74	          game.playSfx(ITEM_DEFS[this.itemId]?.key === 'coin_copper' ? 'coin' : 'pickup', 0.75);
75	          const def = ITEM_DEFS[this.itemId];
76	          if (def) game.showPickupLabel(def.key);
77	          return;
78	        }
79	        if (left !== before) game.notifyInventoryChanged();
80	        this.stack = left;
81	      } else if (inGrabRange) {
82	        // PullItem_Common(:34533-34584):每轴 0.45 步进、钳 4(水平含 player.vx),
83	        // 速度反向时附加 ×0.75 反拉——被拉取帧跳过瓦片碰撞(WorldItem.cs:587-597
84	        // else 分支仅 position+=velocity),物品穿墙飞向玩家
85	        beingGrabbed = true;
86	        const SPEED = 0.45, MAXV = 4, BACK = 0.75;
87	        if (player.cx > this.cx) {
88	          if (this.vx < MAXV + player.vx) this.vx += SPEED;
89	          if (this.vx < 0) this.vx += SPEED * BACK;
90	        } else {
91	          if (this.vx > -MAXV + player.vx) this.vx -= SPEED;
92	          if (this.vx > 0) this.vx -= SPEED * BACK;
93	        }
94	        if (player.cy > this.cy) {
95	          if (this.vy < MAXV) this.vy += SPEED;
96	          if (this.vy < 0) this.vy += SPEED * BACK;
97	        } else {
98	          if (this.vy > -MAXV) this.vy -= SPEED;
99	          if (this.vy > 0) this.vy -= SPEED * BACK;
100	        }
101	      }
102	    }
103	
104	    if (beingGrabbed) {
105	      // 原版被抓取帧:无重力无碰撞,直接位移(WorldItem.cs:596 ApplyMovement)
106	      this.x += this.vx;
107	      this.y += this.vy;
108	    } else {
109	      this.vy = Math.min(this.vy + GRAVITY * 0.7, MAX_FALL_SPEED);
110	      this.vx *= 0.96;
111	      moveAndCollide(this, game.world, this.vx, this.vy);
112	    }
113	    // 入水小水花声（掉落物轻，音量小）
114	    const st = game.world.store;
115	    const li = st.liquid[st.idx(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))];
116	    const wasWater = this.inWater;
117	    this.inWater = li > 80;
118	    if (this.inWater && !wasWater && this.vy > 1.2) game.playSfx('splash', 0.35);
119	    void ITEM_DEFS;
120	  }
121	
122	  inWater = false;
123	
124	  draw() { /* Renderer 统一绘制 */ }
125	}
126	

```


---

## 🤖 Assistant · 2026-08-12T06:01:01.211Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: ItemDrop.fixedUpdate does not check netPuppet — puppet drops created via netApplyItemOp are real ItemDrop entities that get picked up into the local player's inventory (auto-pickup, exempt from protectItems by design). So the msg21 injection chain is real: a malicious client sends msg21 op=0 with arbitrary key + stack (up to 65535), server relays to all (prio=0, no AOI, no rate limit, no owner check, no key validation against ITEM_BY_KEY) → every other client creates a puppet drop → any player touching it gets the items for real. Item injection / economy destruction, works regardless of protectItems (pickup exempt) — and persists via chest deposit (if protectItems off) or by simply keeping.

Also: heart/star pickup types aren't set via msg21 (key-based), so no direct heal injection, but `pickup` field not set — fine.

Also note msg21 op=0 x/y not validated — can spawn drops inside other players (auto-pickup forced). So attacker can force items into victims' inventories (griefing: fill inventory with junk) — actually pickup requires inventory space; inv.add returns left.

Now, another important check: hostile projectile bit from visitors. Confirm Arrow hostile semantics: Arrow constructor takes opts {hostile}. In netProjBroadcast, kind |= 0x80 if p.hostile. Who creates hostile arrows? Probably NPC shooters (host sim). A visitor's own weapons create non-hostile arrows. A malicious visitor crafting frames sets bit7 themselves. Server passes through. So forced PvP from any visitor — confirmed.

Does vanilla gate PvP? Yes: Damage_EVP checks `if (p.hostile ...)` for player-owned projectiles; hostile NPCs projectiles always damage. Our model lacks the PvP flag entirely, so a visitor claiming hostile is indistinguishable from an NPC arrow. Server-side gate: hostile bit requires sender isHost (since all NPC arrows are simulated on host). That's a cheap fix.

Now also check: msg42 negative damage — Math.max(-32768, Math.min(9999, dmg)) allows negative → e.hurt(negative) might heal? Let me check Enemy.hurt briefly. Not critical; mention as hardening (clamp ≥0).

Also msg42 rate: no limit; visitor can spam strikes → host CPU. Mention.

Another thing to verify: the design doc §8bis says AOI blind "全视野兜底" initially then changed to skip — consistent with code.

Backpressure: prio semantics — msg21 broadcast prio=0, tile batch broadcast prio=0, msg23/27 prio=1. At >4MB everything drops including tiles → divergence. Confirmed by code (send: b > SEND_BUFFER_LIMIT → drop regardless of prio).

Now the strip info leak: SpawnTileData handler sends strips around any x,y with no state/rate check — also `Msg.SpawnTileData` requires c.slot >= 0 but state can be 2. Also new client before state 10. Fine. Also note: sendStrips sends fresh strips each request — client dedupe via sentStrips; a malicious client reconnects (new connection) to re-pull. Full map exfiltration possible. Also strips include chest tiles and signs? decodeStrip contents — includes tile data only (msg10 no chest list per code: encodeStrip(st, ...)). Chest contents not in strip. But msg31 brute-force ±1 of chest anchor gives contents: visitor learns chest tile positions from strips, then RequestChestOpen at nearby coords → server responds full contents. No protectItems check on read. So full world + chest content exfiltration. Rating: 建议修 (rate limit + document; if rooms are "public shared worlds" this is by-design like vanilla where clients have the whole world... in vanilla the client downloads the whole world anyway! So world exfil is vanilla-equivalent. But our room model advertises "protectItems 物品保护" — reads aren't protected. So it's a documentation/expectation gap, 记录即可~建议修).

Host failover details confirmed:
- token rooms: after host leaves, hostJoined=false; only a connection presenting the correct token becomes host. Existing visitors never re-Hello → no host → msg23 stops (host was the only source), strikeTarget null → visitors can't damage NPCs. Room continues with tiles/chests working. NPC world dead until host returns. Note: any future joiner without token ≠ host.
- Wait: what about `this.opts.hostToken === ''` (persistent rooms): next joiner becomes host. But visitors already in room don't become host (Hello-only). So persistent room: host leaves → NPC sim stops until a NEW player joins (then that newbie becomes host and their local world becomes NPC authority — their world state may be behind: their world was streamed from server strips so tiles match; NPCs fresh).
- Also, subtle: when host disconnects, visitors' puppets swept after 300 ticks (5s) → all NPCs vanish for everyone. No announcement.

Another subtle: host migration doesn't reset npcCodes/known tables — new host's netIds use new host slot prefix, fine.

One more abuse: session/resume — `resumeSession` claimed flag; reconnect URL carries session. A stolen session (it's just a UUID in URL) lets someone take over a slot. Low severity.

Also: `Msg.Hello` name — no length cap on name? `c.name = r.str()` then broadcast in PlayerActive — a 1MB name string possible → broadcast amplification to all clients (each PlayerActive broadcast includes name). Actually Hello frame limited by WS maxPayload 1MB. name unbounded → broadcast amplification N×. Minor DoS; mention with rate limits. Also appearance `r.str().slice(0, 4096)` capped good; but broadcast of 4096-byte appearance strings to everyone each SyncPlayer — fine.

Also chat: text capped 200. Good.

Now AOI question 4 more concretely: I should verify viewport assumptions — game zoom? Let me check camera/zoom to ground the analysis. Quick grep for zoom or screen scale. Let me check constants: TILE=16. Screen 1920×1080 CSS px at zoom 1 → 120×67.5 tiles. But the game may render at devicePixelRatio or a zoom factor (vanilla default zoom 1). Let me check Renderer zoom quickly.

Actually, more important for the analysis: chebyshev 1920px radius means a remote player is hidden when |dx|>1920 OR |dy|>1920. On a 1920-wide screen you can see up to 960px each side, so 1920 radius covers horizontal visibility with margin... vertical: half-screen 540 < 1920 fine. So AOI_PLAYER is adequate (conservative) for 1920×1080@100%. For larger monitors (2560×1440: half-width 1280 < 1920 OK; 3440 ultrawide: half-width 1720 < 1920 OK; 4K 3840: half-width 1920 — borderline equal). So up to 4K it's fine. Entities at 1280px: on 1920 screen half-width 960 — entities visible up to 960px; 1280 covers with margin. On 2560 screen (half 1280): exactly borderline — entity at 1290px visible on screen but not synced (first-entry at ≤1280 + hysteresis band). So on >2560-wide displays, visible-but-unsynced entities at screen edges. And vertical: 1440 screen half-height 720 < 1280 fine.

Ranged weapons: bow arrow speed? Whatever — key point: PvP/range 1280-1920 gap: you see the player (≤1920) but their projectiles (hostile or not) are not relayed beyond 1280 entry. If a hostile NPC arrow is shot at you from a turret/boss 2000px away, you won't see it until it's within 1280px → you get less reaction time than vanilla (where you'd see it from off-screen anyway... vanilla syncs all projectiles in section). Minor fairness issue, 记录/建议.

Hysteresis mid-flight drop for long-range: entry at 1280 (never-visible), exit at 2048. For a projectile passing by the player and continuing (e.g., stray arrow flying across), it'll appear at 1280, disappear at 2048 — fine. Boomerang/harp that orbit: pop in/out. Client sweep for proj puppets is 180 ticks = 3s, so a projectile re-entering within 3s finds... wait, when server stops sending (out of hysteresis), the client puppet remains until 180 tick sweep; if it re-enters within 3s, netApplyProjSnaps upserts the same puppet (found by netId) → no recreate, smooth. Only after 3s of absence is it swept; re-entry then = recreate = visible teleport. Since exit happens at 2048px and re-entry requires coming back within 1280px, time gap depends on speed: an arrow at ~10px/tick takes ~77 ticks to traverse 768px — under 180. A slow projectile (magic harp ~?) could exceed 3s outside → recreated mid-air = trajectory break. Modest.

Now the backpressure question 5: degradation self-consistency. Details:
- NPC puppets swept at 300 tick (5s) without snapshot; proj 180 (3s). Host broadcast: 15Hz change-driven + 2s full fallback. If prio=1 drops persist >5s → puppets die → on recovery, full resend (known-mark logic ensures full entries) → recreate → flicker. Self-healing yes, but visible.
- The known-set marking is correctly post-send (S2 fix) — good.
- However: on drop, `roomStats.lowDrops` counts, but client has no signal → its sweep timer keeps running. Improvement: prio=0 "pause" signal, or server-side keepalive: when a receiver is in 1-4MB zone, server could still send a periodic minimal prio=0 "entity heartbeat" listing netIds (tiny) to reset client sweep timers without full snapshots. Or client-side: extend sweep threshold dynamically when interpolation extrapolation remains plausible (velocity consistent). Suggest.

Also there's a subtle interaction: backpressure drop + AOI hysteresis maps: when a frame for receiver rc is dropped, aoiNpc/aoiProj entries are still set (they're set before send — look: `rc.aoiNpc.set(e.netId, now)` happens in the pick loop before send; on drop, entry remains, and pruning happens after 30s. Consequence: while visible-entry is remembered, re-entry within the band is allowed (dist ≤ 2048) even though the client never got frames — fine since sweep is client-side. Not a bug.

Another check: `Msg.SyncNPC` — `n > 64` return drops whole frame silently. Host sends ≤24/batch. OK.

Question 6 persistence: 
- Window: SAVE_INTERVAL=300s default, min 30. Crash (SIGKILL) loses up to 300s of tile/chest edits. Also note: lastSavedTileOps baseline only updated on successful save; on exception, next interval retries. OK.
- Dirty check skips only when room empty; occupied rooms save every interval regardless of dirt — fine.
- Multi-room IO spike: saveRooms loops rooms synchronously; saveWorldOnly JSON.stringify of large world (6400×1800 = 11.5M tiles... how big is save JSON? earlier memory notes said saveGame +1.5GB RSS; world JSON maybe tens of MB) → blocking event loop for hundreds of ms per room → all rooms' WS stalls simultaneously → saturation → backpressure → the exact failure mode from the blind-end saga. Recommend staggering per-room save jitter, or moving serialization to a worker thread. Must/建议: 建议修 (given documented SIGKILL/npx fragility, plus single-thread blocking).
- "最后一个玩家取走箱子物品后退出" scenario: room empty + chestEdits changed → next auto-save writes. If crash before → item still in server chest (rollback = item duplicated: player took it locally, server still has it). Window ≤300s. Reasonable? For an economy-ish server, 60-120s or event-driven (save on room empty transition immediately!) — that's a nice cheap fix: when onlineCount hits 0 and dirty, save immediately instead of waiting for the interval. 建议修.

Question 8 announcement: host left → all NPCs vanish 5s later with no message; new host on join with no announcement (well, JoinLeave announcement exists but not "X is now host"). 建议修: broadcast NetModules "host migrated" + consider host failover to senior member for token rooms? For token rooms the token holder is the legitimate owner; transferring host to a random visitor would give them NPC authority + protectTiles exemptions (host bypasses protections!). That's a trust issue: making a random visitor host grants them tile-edit rights even with protectTiles on. So auto-failover to visitors is dangerous in protected rooms; better to keep hostless + announce. For persistent rooms (hostToken=''), anyone can already be host so failover is fine.

Now assemble the blind-end analysis (#1) carefully:
Mechanism verified: 
- room.ts:232 `if (now - c.lastPosAt > AOI_STALE_MS) { stalePos++; continue; }` in broadcastAt (msg13 relay), and :483/:595 same for msg23/27.
- Client: puppets swept (Game.ts:676-703): NPC 300t, proj 180t, drop 300t.
- netPuppetContact (707) / netPuppetProjContact (727) iterate puppet maps → empty → no damage.
- Watchdog (index.ts:252-263): lastSeen reset on ANY message (`handle()` line 249 `c.lastSeen = 0`), and ClientNet sends Ping every 30s via setInterval independent of game loop (ClientNet.ts:150-154). So withholding msg13 while sending Ping = indefinite blind state, never kicked. Even simpler: the legit client itself goes blind when tabbed to background (fixedUpdate throttled/stopped) — meaning blind-end is not even an exotic state.

Cost: attacker loses outgoing visibility of NPCs (can't attack them either since no puppets to hit — actually can they still strike? swingHits needs a puppet Enemy entity; none → no damage dealt). They also stop receiving others' msg13 (broadcastAt blind-skips) — they don't see other players. They still see: tile edits (broadcast unfiltered), chat, chest sync, their own world.

Benefit: complete immunity to all PvE damage (NPC contact, hostile projectiles, presumably also traps? TrapShot puppets are hostile? trap shots come as kind=3 with hostile? netMakeProj case 3 doesn't set hostile — so traps don't damage visitors anyway). Also lava/environment damage is local — unaffected. So the exploit = "PvE god mode at the cost of not participating in combat". In a boss fight with a team, one player can facetank... wait, no — the boss won't even aggro them? The host simulates boss AI targeting host's player only? NPC AI runs on host and targets host's player presumably (host's sim, its own player). So visitors are only damaged via puppet contact. So a blind attacker is simply ignored by the world. Value: griefing scenarios (walk through dungeon, grab items from chests without protectItems, mine without protectTiles, never die). Combined with protectItems OFF default rooms, a blind cheater can loot the world risk-free.

Also note: the attacker also stops receiving msg21? msg21 broadcast is plain broadcast (no AOI) — they still see drops.

Rating: 必须修 (cheap: server-side blind watchdog separate from liveness — e.g., state≥10 && blind > 10-15s → kick; legit background-tab clients get kicked too, which matches vanilla-ish behavior where a frozen client is useless anyway; alternatively freeze semantics... but kicking is simplest). Combined with option "blind 期间仍收 hostile 弹" — the saturation loop concern applied to all entity traffic; hostile-only is a small subset, but that reintroduces partial flow; the loop risk was from full snapshots. Actually simplest robust: kick on blind (it's an anomalous state by design: msg13 is event-driven ≥15Hz when alive; only a dead/tabbed/modified client goes blind).

Let me also double check: is there any server-side awareness for "client in game but no msg13"? stalePos counter exists (observability) — good foundation.

Question 2 chain specifics: verified:
- msg5 (SyncPlayerItem): server validates id < ITEM_DEFS.length, stack clamped to maxStack, no plausibility check (no "does this client own such item" — impossible without SSC). Relay to others (visual only).
- msg32 chest write: gated by protectItems for non-host; when OFF, arbitrary contents accepted (within item id/stack sanity). Server authoritative chest → persisted by saveRooms → permanent economy injection.
- Inventory → chest → (save) → other players can take → multi-client propagation.
So protectItems=ON does block the chest leg for non-host but not the personal-inventory leg. And protectTiles blocks tile placement. So with both ON, a cheater still gets: any items in personal inv (weapons/armor/potions = combat power), free HP, free movement/teleport. The protections are "anti-casual-griefing", not anti-cheat. Consistent with vanilla + SSC absent. Verdict: 记录即可 for design (document the boundary), 建议修 if运营 promises are real (then SSC is the only path, plus server-side inventory delta sanity: e.g., reject stacks > maxStack (done), reject item ids not obtainable? no).

One more: since visitor can edit HP freely, "death" meaningless → PvE challenges trivial. Vanilla-same. OK.

Question 3 malicious host necessity: The architecture (host-authoritative NPC sim) exists to avoid server-side simulation cost (P5 planned server authority). Threat: host can (a) fake NPC positions/hp (grief), (b) force-PvP via hostile bit (kill visitors), (c) spawn items via msg21 (but host owns world anyway), (d) ignore strikes (unkillable NPC), (e) tile ops: host is exempt from protectTiles — by design host owns the world.危害: visitors can't trust anything; but visitors' HP is self-authoritative so forced PvP can be refused client-side (cheat-back). Necessity: acceptable for friend co-op; for public persistent rooms (—world), the host is "first joiner" = random stranger with full world edit rights even if protectTiles was intended! Wait — persistent rooms set protectTiles? Room constructor defaults protectTiles:false, and index.ts --world doesn't set it. So persistent rooms are unprotected by default; fine but note: if an operator wanted protection on a persistent room, the first random joiner bypasses it as host. Worth noting.

Recommendation: keep host-authority, add (1) hostile-bit server gate to host-only (helps visitor-vs-visitor too), (2) announce host identity, (3) long-term P5 server-authoritative NPC sim removes host trust.

Now let me also double-check the claim in Q3 about "msg27 kind=128" — kind=128 = 0x80 = bit7 set, low bits 0 (Arrow). Server check `(kind & 0x7f) > 4` → 0 OK, passes. Confirmed.

Also "伪造 msg21 凭空刷掉落" by host — yes trivially, same as any client (no gate). Highlight that the msg21 hole is client-agnostic.

Question 7 specifics: forged msg13 → (a) AOI basis is receiver's own position, so a forger only shifts *their own* view (they can "远程观战" any location: set position near a boss → receive snapshots; combined with... can they *see* tiles? No, strips come from SpawnTileData requests — they can pull any strip anyway). (b) others see the forger teleporting (vanilla-same cheat). (c) f32 NaN/Infinity not sanitized → NaN relay poisons other clients' proxies (NaN positions) — minor robustness.
SpawnTileData: unauthenticated, unthrottled, arbitrary coordinates, 25 strips (5×5) per call, sentStrips dedupe per connection only → whole-world exfil possible, and each strip re-encodes or serves from cache. Bandwidth cost to server: cache hit cheap; miss = encode. Also stripCache 32MB LRU bounded. So worst case a client pulls entire map over time: for 4200×1200 world: 21×60=1260 strips ≈ maybe 20-60MB. Feasible. Vanilla equivalent: vanilla client gets whole world file? No! Vanilla sends sections on demand too (CheckSection 3×3 around player). But vanilla trusts position too — a hacked vanilla client can also pull all sections. So vanilla-equivalent. 记录即可 + optional throttle.

One more thing for #7: forged position affects *other* clients' AOI? No — AOI filter keyed on receiver's own reported pos. So a forger cannot manipulate others' feeds. Good design property worth stating.

Also: msg13 broadcast `broadcastAt(x, y, AOI_PLAYER, ...)` uses sender's claimed x,y as the broadcast origin — so a forger teleporting relays their packet to everyone within 1920px of the *claimed* location — fine.

Now, are there issues with `Msg.PlayerState` NaN? f.f32(NaN) → serialized as NaN bytes → receivers set rp.x = NaN → proxy NaN →渲染崩溃? ClientNet handles... not sanitized. Recommend server-side Number.isFinite check on x/y/vx/vy (also for msg23/27/21 from host). Cheap hardening. 建议修.

Let me now also confirm the claim "AOI blind 初版全视野兜底" is in code history — not needed.

Also check msg23 n up to 64 but each entry key up to 64 chars; host sends ≤24. Malicious host can send 64 entries × 64B key per frame at unbounded rate → server re-encodes per receiver → CPU amplification O(N). Rate limiting needed. Also npcCodes map grows: 60000 cap then clear — fine.

DoS surface summary: no inbound rate limiting anywhere (design §8.6 says default off; §6.2 says "轻量 spam 计数默认开" — actually §6.2 says light spam counting default ON as a deviation, but the code has none!). That's a doc-vs-code gap: docs promise "挖块 >500/min 告警、>2000/min 踢" default on; code has zero inbound rate limiting. 建议修 (doc/code alignment + basic per-client msg budget).

Let me verify there's truly no rate limiting: search room.ts/index.ts for spam/rate — I saw none. Confirmed.

Also maxPayload 1<<20 = 1MB per WS message; a single WS message can contain many frames; parser handles. A flooder can send 1MB messages back-to-back → server CPU. Basic: cap frames processed per message / per second per client.

Now Q5 improvements: also consider that when >4MB (all-drop), tile frames are dropped too — client world diverges silently and permanently. There's no re-sync path except client re-requesting strips on strip-boundary crossing (R3) — which would re-pull stale-ish strips? Strips come from server's authoritative store (cache invalidated on ops) → re-request gives current data. But client only requests when crossing strip boundaries (every 30 ticks check, per lastStripReq key) — so a standing client never re-pulls → permanent divergence after overload. Mitigation: on overload recovery, server pushes affected-strip invalidation or clients re-request strips on drop signals. Or simplest: make tile batch relay prio=-1/"critical" that's never dropped (tiles are small; a flood of tile ops is bounded by mining speed ~ legit; a cheater could spam tile ops though). Better: never drop prio=0 control/world-state frames; instead close the connection when >4MB sustained (slow-client eviction) — arguably cleaner than silent divergence. 建议修.

I think I have enough. One more verify: `Msg.StrikeNPC` — does host apply strike from any visitor without validating visitor proximity/LOS? Yes — netApplyStrike just finds local enemy by netIdLocal and hurts. A visitor can strike NPCs across the map (no distance check) — vanilla checks? Vanilla msg28 has no distance check either IIRC (server trusts). Mention as record.

Also msg42: rawDmg clamp allows negative (Math.max(-32768,...)) → negative hurt → check Enemy.hurt with negative: might heal or do weird. Let me quickly check hurt's handling.
```

</details>


---

## 🤖 Assistant · 2026-08-12T06:01:01.536Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld && sed -n '3940,3990p' game/src/entities/Enemy.ts",
 "description": "Check Enemy.hurt negative damage handling"
}
```


---

## 👤 User(sidechain) · 2026-08-12T06:01:01.567Z

**📎 ToolResult**

```
      // 日耀（:41431-41443）：1080px 内且低于塔顶 700px → 塔顶直投 519（斜抛 7-12px/t）
      if (this.ai1 > 0) this.ai1--;
      if (this.ai1 <= 0 && player && !player.dead
        && distTo(player.cx, player.cy) < 1080 && player.y - this.y < 700) {
        const flare = spawnPart(game, this, 519);
        if (flare) {
          flare.x = this.x - this.w * 0.33 + Math.random() * this.w * 0.66 - flare.w / 2;
          flare.y = this.y - 20;
          const theta = (Math.random() * 2 - 1) * 0.7853981852531433;   // RotatedByRandom(0.785)
          const sp = 7 + Math.random() * 5;
          flare.vx = Math.sin(theta) * sp;      // -UnitY 旋转 θ：(sinθ, -cosθ)
          flare.vy = -Math.cos(theta) * sp;
        }
        this.ai1 = 60;
      }
    }
    // 507 星云仅环境粒子（:41287-41309），怪全靠 Zone 刷怪表——略

    // noTileCollide + noGravity：直接位移（原版速度由引擎积分）
    this.x += this.vx;
    this.y += this.vy;
    this.onGround = false;
  }

  /** 受击。返回是否死亡 */
  hurt(dmg: number, kbx: number, kby: number, game: GameHooks): boolean {
    // Critter 兼容：critters 桶的调用方按 Critter.hurt(game) 单参调用；
    // 原版小动物是 Enemy 进该桶，这里把 Game 对象重映射回 game 参、伤害取固定 5
    if (typeof dmg === 'object' && dmg !== null) {
      game = dmg as unknown as GameHooks;
      dmg = 5; kbx = 0; kby = 0;
    }
    const rawDmg = dmg; // 傀儡上报用原始值（下方 def 凘认算只做一次，双端一致）
    if (this.iframes > 0) return false;
    this.justHitT = 2; // 原版 justHit 单帧旗标（AI_023 飞行武器/陆龟受击回态消费）
    // 训练假人（NPC 488，cs:83498 localAI 赋值）：immortal 永不死，
    // 受击只记摇晃强度+方向（渲染帧端消费），掉血由 dummyAI 回满
    if (this.vanillaId === 488) {
      this.dummyShake = Math.max(20, Math.min(120, dmg));
      this.dummyHitDir = Math.sign(kbx) || this.dummyHitDir;
      this.iframes = 8;
      return true;
    }
    // 原版 Main.CalculateDamageNPCsTake：dmg - defense*0.5，下限 1
    const def = this.def.defense ?? 0;
    // ichor（灵液药剂）：NPC.checkArmorPenetration（NPC.cs:81913-81938）——
    // armorPenetration += 15，结算 (armorPenetration/2) 整除 = +7 直伤；
    // 超防钳制（def>2×dmg 时按 dmg 上限，防穿透把伤害推到全额以上）
    const pen = this.ichorT > 0 ? 7 : 0;
    const effDef = def > dmg * 2 ? dmg * 2 : def;
    dmg = Math.max(1, Math.round(dmg - effDef * 0.5 + pen));

```


---

## 🤖 Assistant · 2026-08-12T06:01:29.667Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Negative dmg: `dmg = Math.max(1, Math.round(dmg - effDef*0.5 + pen))` where effDef = def > dmg*2 ? dmg*2 : def. With dmg negative: effDef = def (since def > negative*2 usually true if def>0... def > dmg*2 → for dmg=-100, dmg*2=-200, def> -200 true → effDef=def). Then dmg = max(1, round(-100 - def/2)) = 1. So negative dmg becomes 1 damage. No heal. Fine — record only as "钳到 1,无回血风险".

Now I have everything. Let me also quickly double check msg27 `dmg` from a hostile visitor projectile — dmg i16 up to 32767 → visitor client hitPlayer(pr, this, 32767) → damagePlayer huge → death. And knockback etc. And note iframes: player.immune gating. So one forged arrow kills any visitor. Confirmed severity.

Also worth checking: does a visitor's own client send hostile for its own arrows? No (only if p.hostile). So legit visitors don't set bit7. So server-side gate (host-only for bit7) is safe for legit traffic. 

One more: on the host, NPC arrows hostile=true — the host's own client doesn't get its own broadcasts (except c), fine.

Also: what about TrapShot (kind 3) — hostile? netMakeProj case 3: TrapShot without hostile. Trap shots on visitor don't damage (they're NPC-simulated on host; host takes trap damage itself). Known gap, not in scope.

Let me also verify the doc §8ter claim about msg16 relay — code: `Msg.PlayerLifeMana` broadcasts hp/maxHp from any client, only sanity: none (i16). Negative hp? Fine.

Now also check stats.ts quickly? Not necessary.

Enough. Write the report in Chinese, grouped by 必须修/建议修/记录即可, each item with threat model, feasibility, harm, code evidence, recommendation. Include the 8 requested analysis items mapped into the three tiers, plus extra findings (msg21 injection, msg27 hostile from any visitor, no inbound rate limiting, NaN, hostless token room liveness).

Let me organize:

必须修:
1. msg21 掉落物注入(无所有者校验/无 key 校验/无速率限制/prio=0 不受背压保护) → 凭空造物链,绕过 protectItems。room.ts:550-567 + Game.ts:597-626 + ItemDrop.ts:31-80。
2. msg27 hostile 位任何客户端可置位 → 强制 PvP 秒杀。room.ts:568-583(只校验低 7 位) + Game.ts:648-660/727-733。修法:bit7 仅房主可用(NPC 弹幕只出自房主模拟);长期加 PvP 开关。
3. 盲端免伤 + 看门狗失效(Ping 保活) → 无限 PvE 无敌。room.ts:232/483/595 + index.ts:252-263 + ClientNet.ts:150-154。修法:state≥10 且盲端 >10~15s 踢(独立于 lastSeen);stats 已有 stalePos 可直接做判定。

建议修:
4. 无任何上行速率限制(设计文档 §6.2 承诺"轻量 spam 计数默认开",代码零实现)——msg13/msg27/msg23/msg21/SpawnTileData 全部可刷;单条 WS 消息 1MB 可塞数千帧 → CPU/带宽放大。doc-code gap。
5. 房主退出后 token 房永久无主(NPC 世界死亡、strikeTarget=null 访客无法输出)且无公告;常驻房新进者成房主但世界 NPC/掉落状态回退。建议:公告 + (token 房)不自动移交,常驻房移交时公告。
6. >4MB 全丢含 prio=0 tile/chest 帧 → 静默永久世界分叉(客户端站位不动不会重拉 strip)。建议:prio=0 世界状态帧不丢,持续超限直接断连;或恢复后推送条带失效。
7. 背压降级与客户端清扫阈值脱节 → 怪闪烁;建议 prio=0 微型心跳(netId 列表)或丢帧信号延长清扫。
8. auto-save 阻塞事件循环 + 多房同时落盘 IO 尖刺;空房+脏立即落盘(最后一个取箱子的人退出场景)把 300s 窗口收敛到 ~0;SAVE_INTERVAL 默认建议 120s 或事件驱动。
9. f32 NaN/Infinity 未清洗(msg13/23/27) → NaN 中继毒化他人代理。
10. SpawnTileData 任意坐标无限拉条带 = 全图泄露(+msg31 暴力探测箱子内容,protectItems 不保护读取)。建议限速+文档明示;vanilla 等价故不必须。

记录即可:
11. 客户端权威 HP/位置/物品 = vanilla 同款;protectItems/protectTiles 是"防小白/防误伤"而非反作弊;矛盾点写清楚;要运营级经济需 SSC(§8.5)。复制链评估:改背包→msg5(仅值域校验)→(protectItems off)msg32 入箱→服务器权威箱→落盘→他人取 = 持久化注入。protectItems on 时个人背包仍可无限。
12. 恶意房主:伪造 msg23/拒绝 msg42 结算/无敌 NPC;hostile 强制 PvP(但受害者 HP 自权威可拒绝);房主豁免 protectTiles。架构必要(服务器零模拟成本),记录信任边界,P5 服务器权威模拟是根治路径。
13. AOI 半径:1920/1280/2048 对 ≤4K 屏够用;1280~1920 区间 PvP"见人不见弹";首次入场 1280px 弹幕突然出现(反应时间少于原版);弹幕滞回外出 3s 后重进=轨迹断裂重建。建议记录或微调(实体内径提到 1536 或加武器射程考量)。
14. msg42 负伤钳到 1 无回血;msg42 无距离/速率校验(vanilla 亦然);msg21 op=1 take 可让他人掉落消失(拒绝拾取级 grief);msg23/27 n≤64 已限但帧率未限。
15. session UUID 在 URL,可被窃取顶号(60s 窗口)。

Also mention positive findings: known-mark-after-send (S2) correct; blind-end design rationale (saturation loop) sound but needs kick; AOI keyed on receiver's own position means a position forger cannot manipulate others' feeds (good property); chest clear-on-tile-remove prevents stale chest duplication.

For #1 mitigation options asked: 盲端仍收 hostile 弹 / 盲端计时器更短 / 服务器侧判定 — I recommend 计时器(kick) because: hostile-only flow reintroduces partial saturation path and doesn't fix "看不到 NPC" asymmetry; server-side judgment is P5-scale work.

Also note for #1: legit background-tab clients already go blind (fixedUpdate stops) — so a kick-on-blind policy needs a grace period and maybe client-side mitigation: browsers throttle setInterval too but the 30s ping survived per comment R9 ("暂停/后台 fixedUpdate 停跑也不再被服务器 120s 看门狗踢" — intentional design!). So there's a direct conflict: R9 deliberately keeps tabbed-out clients alive via ping; kicking on blind would kick every tabbed-out player. That's an important tension to call out: the R9 design decision creates the abuse window. Options: (a) kick on blind — breaks R9's intent (tabbed-out users kicked); (b) blind clients get marked "afk" and are excluded from... hmm, they already receive nothing. The exploit value comes from being able to ACT while blind: a tabbed-out client can't act, but a modded client can (it runs its own loop sending only ping). Distinguishing "idle" from "acting blind" server-side: hard without observing actions — but actions ARE observable: a blind client still sends TileBatch/ chest ops / chat / msg42... Actually a blind attacker acting in the world must send some messages (tile ops when mining, msg42 when striking). Heuristic: any activity message while blind >N seconds → kick. That's a nice targeted fix: "盲端仍在操作 = 异常"。Or simpler: blind > 60s → kick regardless (tabbed-out for a minute is a reasonable kick; vanilla would have them useless anyway... though vanilla client keeps simulating when tabbed? Browsers throttle rAF/fixedUpdate... whatever). I'll present options with tradeoffs.

Let me write the report now. Keep it structured and cite file:line. It should be in Chinese. Comprehensive but not bloated.
```

</details>


---

## 🤖 Assistant · 2026-08-12T06:02:34.998Z · glm-x-preview-260804

```
# 多人联机层对抗分析报告(机制合理性 / 滥用面)

核实基础:`server/src/room.ts`(853 行)、`server/src/index.ts`、`server/src/persist.ts`、`game/src/net/ClientNet.ts`、`game/src/net/entitySyncHooks.ts`、`game/src/core/Game.ts` net 段(380-760、9130-9282)、`game/src/entities/ItemDrop.ts`、`docs/multiplayer-design.md` §8bis/§8ter。

先给一条贯穿全篇的总体结论:**权威模型的分层本身是自洽的**(NPC=房主、玩家=客户端、tile/箱/时钟=服务器,与原版混合权威一致;AOI 以"接收端自己的 msg13 位置"为过滤基准这个设计有个很好的性质——伪造位置者只能操纵自己的视野,不能操纵他人的信息流)。但**信任边界有一处实质破洞(msg21 掉落物注入)和一处语义倒挂(msg27 hostile 位对访客开放)**,它们让 `protectItems/protectTiles` 的运营承诺在实际链路上形同虚设。其余多为降级语义与经济学问题。

---

## 一、必须修

### M1. msg21 掉落物注入:任意客户端凭空造物,直接击穿 protectItems

- **代码依据**:`room.ts:550-567`(`Msg.SyncItem` 处理)——无 `isHost` 门禁、无 netId 所有者校验(`entitySyncHooks.makeNetId` 约定高 8 位=拥有者 slot,服务器没查)、key 不做 `ITEM_BY_KEY` 反查(服务器已 import `ITEM_DEFS`/可取 `ITEM_BY_KEY`,`room.ts:13`)、stack 只查 `stack===0`(u16 上限 65535)、坐标不校验、**`this.broadcast(f.finish(), c)` 走默认 prio=0,背压分级完全不保护它**(`room.ts:86-88,174`)。
- **完整链路(已逐环核实)**:
  1. 恶意客户端手工构造 msg21 op=0,`key="coin_platinum"`(或任意物品)、`stack=9999`、坐标=某受害者脚下;
  2. 服务器原样广播给全员(`room.ts:565`);
  3. 各客户端 `Game.netApplyItemOp`(`Game.ts:597-609`)创建**真 ItemDrop 实体**(仅打 `netPuppet` 标);
  4. `ItemDrop.fixedUpdate`(`ItemDrop.ts:31-101`)**不检查 netPuppet**,命中即 `player.inv.add(itemId, stack)` 进真实背包——而"自动拾取豁免物品保护"是明确需求(`Game.ts:398`、§7.3);
  5. protectItems 关闭时入箱(`msg32`,服务器权威应用 `room.ts:430`)→ `saveRooms` 落盘(`persist.ts`)→ **凭空物品永久化并跨会话流通**。
- **威胁模型/可行性/危害**:任一房间成员、几行代码、无需房主。危害=经济彻底摧毁 + 可向他人背包强制塞垃圾(拾取不需对方同意)。`protectItems` 名义上保护的"房间物品"在读取侧(msg31)和注入侧(本条)都不设防。
- **建议**:① op=0 校验 `netId>>>24 === c.slot`(所有者一致);② key 反查 `ITEM_BY_KEY`,未知键丢帧;③ stack 钳 `maxStack`;④ 加每秒条数限;⑤ relay 提为 prio=1(它是实体流,不该比 msg23 更不可丢)。这条修完后,Q2/Q3 里的"凭空刷掉落"面同时收口。

### M2. msg27 hostile 位(bit7)对任意访客开放 = 无 PvP 开关的强制击杀

- **代码依据**:`room.ts:581-582` 只校验 `(kind & 0x7f) > 4`,bit7 原样透传;`Game.ts:534-535`(hostile 来自 `p.hostile`)、`Game.ts:648-653`(访客 `netMakeProj` 按 bit7 重建带 hostile 的 Arrow)、`Game.ts:727-733`(`netPuppetProjContact` → `hitPlayer` 本地结算)。
- **链路**:任何访客把自己的弹幕帧 kind 写成 `0x80|0`、`dmg=32767` → 服务器透传 → 其他访客客户端本地跑 `Damage_EVP` → 一箭秒杀。题目第 3 点问的是"恶意房主"能不能这么干——**能,但其实不需要房主,任何访客都能**,这比题目假设的更糟。
- **关键不对称**:原版有服务器强制的 PvP 开关(`player.hostile`),我们没有;而合法流量里 hostile 弹幕**只可能出自房主的 NPC 模拟**(NPC 射的箭才有 `p.hostile=true`,玩家自己的武器弹不会置位,见 `Game.ts:534-535`)。所以服务器有免费的判别特征:**bit7 置位 ⇒ 发送者必须是房主**,否则丢帧。这一行校验就能关闭访客→访客的强制 PvP。
- **建议**(必须):服务器侧 `if ((kind & 0x80) && !c.isHost) 丢本条`。房主→访客的强制 PvP 因 HP 客户端权威(受害者可本地拒算)而对称可反制,降级为"记录即可"(见 R3)。

### M3. 盲端免伤是真实漏洞,且 120s 看门狗对它无效——但修法要避开 R9 的设计张力

- **机制核实(全部成立)**:`room.ts:232`(broadcastAt)、`room.ts:483`、`room.ts:595` 三处盲端跳过;客户端傀儡清扫 `Game.ts:676-703`(NPC/掉落 300t、弹幕 180t);`netPuppetContact`/`netPuppetProjContact`(`Game.ts:707-733`)遍历傀儡表——盲端 5 秒后表空,**免疫一切 NPC 接触与敌对弹幕伤害**,成立。
- **看门狗失效**:`index.ts:252-263` 的看门狗按"任意入包"复位(`room.ts:249` `c.lastSeen = 0`),而 `ClientNet.ts:150-154` 用**独立 setInterval 每 30s 发 Ping**,注释明说是为了"暂停/后台 fixedUpdate 停跑也不再被 120s 看门狗踢"(R9)。结论:**只停 msg13、留 Ping,可以无限期保持盲端,永不掉线**。所以"直到 120s 被踢"的前提不成立——窗口是无限的。
- **代价收益比**:代价≈零(几行代码,还能照常挖方块/开箱/聊天/收 msg21 掉落——msg21 不走 AOI,盲端照收);收益=全 PvE 无敌 + 在 protectTiles/protectItems 关闭的默认房里无风险搜刮世界。Boss 战里表现为"世界当我透明"。**真实且高收益漏洞。**
- **缓解选项对比**:
  - a) 盲端仍收 hostile 弹:只补回伤害不补回可见性,且重新打开"饱和时给盲端灌流"的部分路径(§8ter 实测的放大循环正是这类),不推荐做主修;
  - b) **盲端计时器更短/直接踢**:与 R9 冲突——后台标签页的合法玩家 fixedUpdate 停跑、本来就会盲,**一刀切踢会把每个切出去的玩家都踢了**。可行折中:盲端 >10s 后进入"AFK 态",AFK 态下**再收到任何操作类消息(TileBatch / SyncChestItem / msg42 / msg21 / 聊天)即踢**——"盲端仍在操作"在协议上不可伪装成正常客户端,而后台挂机的合法玩家不会发这些;
  - c) 服务器侧判定:P5 工作量,不是本漏洞的合理补丁。
  - 推荐组合:b 为主 + 把 `stalePos` 已有计数(`roomStats.stalePos`)接进踢出日志。此项必须修,否则 M1/M2 修完,盲端仍是最便宜的作弊入口。

---

## 二、建议修

### S1. 上行零速率限制,且与设计文档承诺相悖

- **代码依据**:`room.ts` 全文、`index.ts:232-243` 无任何 per-client 速率/帧数限制;单条 WS 消息上限 1MB(`index.ts:217`),一条消息可塞数千个 msg13/msg27 帧,每帧触发 O(N) 中继与(部分路径)O(N) 重编码。msg23/27 单帧 n≤64 已限(`room.ts:450,571`),但**帧率**未限。
- **文档 gap**:§6.2 白纸黑字"轻量 spam 计数默认开(偏离项 §8.6):挖块 >500/min 告警、>2000/min 踢"——代码里不存在。这是文档与实现的对账缺口,也是所有放大类攻击的共同前提。
- **建议**:每客户端每秒消息预算(如 msg13 ≤30/s、msg21/27 ≤30 帧/s、TileBatch op 累计限),超限先告警后踢;`/stats` 已有 msgHist,接入即可。

### S2. token 房房主退出后永久无主:静默的"世界死亡"

- **代码依据**:房主判定只在 Hello(`room.ts:264`);`disconnect` 置 `hostJoined=false`(`room.ts:731`);`strikeTarget()` 找不到房主返回 null → 访客 msg42 直接丢弃(`room.ts:643-646`);已在线访客不会再发 Hello,**token 房(hostToken≠'')里没有任何人能成为新房主**。后果:房主掉线 5 秒后全体 NPC 傀儡清扫(`Game.ts:678`),msg23 断流,访客打击无结算端——房间变成"有 tile 同步的空壳",且**没有任何公告**。
- **常驻房**(hostToken='')语义稍好:下一位**新进房者**成房主,但其世界是服务器 strip 流拼的,NPC/掉落从零开始(旧房主本地模拟的掉落、Boss 战进度全部蒸发)。语义本身可接受(tile/箱是服务器权威,不回退;NPC/掉落本就是房主本地态),但**应当公告**("X 现在是房主 / NPC 模拟已中断")。
- **建议**:① 房主离开/新房主产生时广播一条 NetModules 公告;② token 房**不要**自动移交房主给访客——房主豁免 protectTiles(`room.ts:370`),移交等于把破坏权随机送给陌生人;③ 常驻房移交时明确提示状态回退范围。是否要把"在场最久的访客"提为 NPC 权威源是产品决策,但至少要让在场者知道发生了什么。

### S3. 背压 >4MB 全丢含 tile/箱帧:静默且**永久**的世界分叉

- **代码依据**:`room.ts:174` `b > SEND_BUFFER_LIMIT` 不分 prio 全丢;prio=0 的 TileBatch 中继(`room.ts:384`)、msg32(`room.ts:433`)、msg16、聊天都在此列。客户端侧没有任何重放机制,唯一的 strip 重拉发生在"跨条带边界"时(`Game.ts:9130-9139`,30t 轮询)——**站桩不动的客户端永远不会重拉**,丢掉的 tile 变更成为永久分叉。
- **对比**:prio=1(实体)丢弃的自愈是真实的:短码 known 标记严格晚于 send(`room.ts:541-546`,S2 修复),丢帧后自动回落全量,配 300t 清扫=闪烁但不分叉。**prio=0 世界状态帧没有这个性质**——这是降级语义里真正不自洽的一环,比"怪闪烁"严重。
- **建议**:① tile/箱/时钟类帧从"可丢"改为"不可丢",持续 >4MB 的慢客户端直接断连(对齐原版 TimeOutTimer 的"慢端淘汰"精神,总好过静默分叉);或 ② 背压恢复后对该端推送"受影响条带失效/重发"。① 更简单。

### S4. 背压降级与客户端清扫阈值脱节(题 5 的"更优")

- 现状:prio=1 丢弃只计数(`room.ts:175-177`),客户端无感知,傀儡 180/300t 照常清扫 → 战斗中"怪闪烁消失重现"。**自洽但难看**。
- 更优(按性价比排序):① 服务器在丢 prio=1 帧期间,周期性发一个极小的 prio=0 "实体心跳"(仅 netId 列表,几十字节),客户端据此暂停清扫、只做速度外推(`Entity.netSnapTo` 已支持"到点后纯速度外推",基础设施现成);② 客户端清扫阈值与"最近是否收到过任意 prio=0 帧"联动(收到心跳就延长);③ 插值外推延长本身收益有限——外推已在做,瓶颈是清扫计时器不知道发生了丢帧。
- 单做 ① 即可消除 90% 的闪烁,且不引入新语义。

### S5. 持久化经济学:300s 窗口 + 单线程同步落盘的 IO/CPU 尖刺

- **代码依据**:`index.ts:303-306` 一个 setInterval 里 `saveRooms` **同步串行**写全部房;`persist.ts` `saveWorldOnly` + `fs.writeFileSync` 全在事件循环上。多房同时落盘 = 大 JSON 序列化 + 磁盘写阻塞单线程数百 ms~秒级 → 全服 WS 停摆 → 触发 S3 的饱和路径。这与 §8ter 记录的"盲端放大循环"是同一类反噬:auto-save 本身可能制造出它想防的饱和。
- **丢失窗口**:"最后一人取走箱内物品后退出"→ 房空 + chestEdits 脏 → 但要等下一个 auto-save 才落盘,SIGKILL 则服务器档残留原物品(玩家本地已拿走)= **复制**,窗口=最多 `--save-interval`(默认 300s)。
- **建议**:① **房间人数从 >0 变 0 且脏标记为脏时立即落盘**——一行代码把题目里的场景从 300s 窗口收敛到 ~0,这是全篇性价比最高的一条;② 默认 interval 300s 偏松,建议 120s,或再加"tileOps 累计超阈值触发"的事件驱动;③ 多房落盘加随机抖动(±interval/4)削平 IO 尖刺,序列化挪 worker 是中期项。

### S6. f32 坐标未清洗:NaN/Infinity 中继毒化他人

- **代码依据**:`room.ts:353-363`(msg13)原样 f32 中继;msg23/27 同。`x=NaN` → 他人客户端 `rp.x=NaN` → `simulateRemotePlayers` 的代理位置 NaN 物理污染(`Game.ts:9165-9238`),可能一路渗进渲染/碰撞。盲端判定 `Math.abs(NaN - x) <= r` 恒 false,NaN 端自己什么都收不到,但**别人会收到它的 NaN**。
- **建议**:服务器对 msg13/23/27/21 的全部 f32 做 `Number.isFinite` 校验,非法整包丢+计数。几行,防的是最脏的崩溃类滥用。

### S7. SpawnTileData 任意坐标无限拉条 = 全图读取(含箱子内容探测)

- **代码依据**:`room.ts:293-298` 只查 `slot>=0`,坐标任意;`sendStrips` 每次回 5×5=25 条带(`room.ts:768-798`),去重仅在本连接内(`c.sentStrips`)。4200×1200 世界 ≈1260 条带,分批拉完即得全图 tile;再对图中箱体格附近发 msg31(`findChestNear` ±1 容差,`room.ts:407`)即可**读出任意箱子全部内容——protectItems 不保护读取**(它只拦 msg32 写,`room.ts:426`)。
- **定性**:原版同样按 section 拉取、同样信任客户端位置,所以这是 vanilla 等价面,不是本实现的退化。但房间制的对外承诺("物品保护")容易让人以为箱子内容不可见——这是**预期管理缺口**。建议:① msg31/msg8 每秒限次;② 文档与 RoomPolicy UI 明示"保护=防改动,不防读取";③ 若未来要真保护,得做 section 级白名单,成本高,不值得现在做。

---

## 三、记录即可

### R1. 客户端权威 HP/位置/物品 vs "双保护"运营属性:矛盾是真实的,边界要写清(题 2)

- **链路核实**:访客改背包 → `syncInventory` 差分发 msg5(`ClientNet.ts:769-789`)→ 服务器仅做 id/stack 值域校验(`room.ts:331-341`)→ 中继;protectItems 关闭时入箱 msg32 被服务器**权威应用并落盘**(`room.ts:430`, `persist.ts`)。整条链无一处能发现"这物品是凭空来的"。
- **结论**:`protectItems` 保护的是"服务器箱子的既有内容不被非房主改写",`protectTiles` 保护的是"世界不被非房主挖改"。二者都是**防误伤/防小白/防低门槛 grief**,不是反作弊。背包侧的无限复制链在 protectItems=ON 时只断"入箱"一环,武器/药水/装备照进个人背包。若运营属性是认真的,唯一根治路径是 SSC(§8.5 已列为可选项,原版也有此开关);否则应在文档和 UI 文案里明确这层边界。当前实现与原版语义一致,**记录即可**,但 M1 修完后至少"伪造 msg21 塞别人背包"这条最脏的路径没了。

### R2. 恶意房主的能力面与必要性(题 3)

- **能力**:伪造 msg23(假位置/hp,可把 Boss 瞬移到访客脸上、或显示 1hp);吞掉 msg42 不结算(造不死的 NPC);伪造 msg21 刷物(修 M1 后仍可行,但房主本就拥有世界);置 hostile 位强制 PvP(修 M2 后仅剩房主可做)。**反制对称性**:访客 HP 是客户端权威,受害者本地可拒算 hostile 伤害——房主的强制 PvP 与访客的改血是同等级的作弊权,互相抵消,不像 M2 那样是单方面碾压。
- **必要性**:房主权威让服务器零 NPC 模拟成本,是当前阶段的合理取舍(代码里已留了 P5 演进点:`npcAuthority`/`strikeTarget` 的注释,`room.ts:158-165`)。记录信任边界即可;真要面向公网的常驻房,长期走 P5 服务器权威模拟。另注:常驻房默认 `protectTiles:false` 且首位进房者为房主(`index.ts:288-291`),即"第一个陌生人获得全部世界编辑权"——常驻房运营者要知道这一点。

### R3. AOI 半径:总体合理,两处边界语义值得记录(题 4)

- **核实**:AOI_PLAYER=1920px(切比雪夫)对 1080p~4K 宽屏(半宽 ≤1920)足够;AOI_ENTITY=1280px 对 ≤2560 宽屏(半宽 1280)刚好够,**超宽屏/缩小缩放下边缘会出现"看得见但不同步"的实体**。
- **两个真实边界**:
  1. **1280~1920px 的 PvP 空洞**:你看得见对方玩家(AOI_PLAYER)但收不到他的弹幕(实体内径 1280)——弓箭射程(~1500px+)正好落在这个区间,"见人不见弹"是真实存在的;
  2. **敌弹首次入场在 1280px**:Boss/炮塔从 2000px 外射来的箭,直到 1280px 才第一次出现(滞回带 `dist>1280 && !wasVisible` 不入,`room.ts:492,604`),反应时间比原版(section 全量)短。滞回外径 2048px 出场后,弹幕在外滞留超 180t(3s)再回来会**重建而非续接**(`Game.ts:697-702`),回旋镖/竖琴类轨道弹轨迹视觉断裂。
- **定性**:都是体验级而非机制级问题,记录即可;若要修,把实体内径提至 1536px(96t)或对"射弹类弹幕"单独放宽内径,代价是带宽略增。

### R4. 其余记录项

- **msg42**:负伤害会被 `Enemy.hurt` 钳到 1(`Enemy.ts:3980` 附近 `Math.max(1,...)`),无回血风险;dmg 上限 9999 已钳(`room.ts:645`)。无距离/速率校验(原版 msg28 同样没有),配合 S1 的限流即可。
- **msg21 op=1(take)可冒名移除他人掉落**:`room.ts` 不校验 netId 所有者,可对房主真掉落发 take 让它全房消失(拒绝拾取级 grief,拿不到物品)。修 M1 的所有者校验后自动收口。
- **session UUID 走 URL**(`index.ts:227`):60s 窗口内可顶号,敏感度低,记录。
- **stats/可观测基础好**:`stalePos/sendDrops/lowDrops/msgHist/stripHit` 齐全,M3/S1 的检测可以直接挂上去,这是这套机制里最值得肯定的部分。
- **已验证为正确的关键细节**(避免后续误改):短码 known 标记严格晚于 send(丢帧自愈);`applyTileOps` 清箱 tile 同步清权威 chests 条目防复制(`room.ts:818-823`);AOI 以接收端自身位置为基准使位置伪造无法操纵他人信息流。

---

## 修复优先级排序(性价比序)

1. **M1** msg21 五连校验(所有者/key/maxStack/限速/prio)——一行行加,半天工作量,关掉最脏的注入链;
2. **M2** hostile 位限房主——一行校验,关闭任意访客强制 PvP;
3. **S5①** 空房且脏立即落盘——一行调用,复制窗口 300s→~0;
4. **M3** 盲端 AFK 态+操作即踢——依赖现有 stalePos,注意保留 R9 的后台挂机语义;
5. **S1** 上行限流(兑现 §6.2 的既有承诺)+ **S3** tile/箱帧不可丢、持续超限断连;
6. **S2** 房主迁移公告、**S6** NaN 清洗、**S4** 实体心跳、**S5②③** 落盘抖动与 interval。
```
