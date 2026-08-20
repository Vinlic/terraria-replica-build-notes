# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-04T16:35:31.665Z

```
为一个泰拉瑞亚（Terraria）复刻游戏设计详细的实现方案。项目目录 ~/Project/GLM/SandboxWorld 是空的（只有参考资料），这是一个从零开始的新项目。

## 已确定的决策（用户已确认，不要再改动）
- 技术栈：Web 前端，TypeScript + Vite，Canvas 2D 或 WebGL 渲染（你建议用哪个并说明理由，Canvas 2D 通常是合理选择）
- 素材：纯程序化生成原创像素素材（代码绘制 sprite，不用任何原版/第三方贴图，无版权问题）。TEdit 数据表中的颜色值可作调色参考
- 地图格式：支持导入真实泰拉瑞亚 .wld 地图文件（照 TEdit 的格式实现 TS 版解析器）+ 自有 JSON 存档格式。不做 .wld 写出
- 功能范围：核心 + 进阶（见下）
- 重要约束：**不得照抄任何其他开源泰拉瑞亚克隆项目的实现**，核心逻辑自己设计。TEdit 仓库只作为地图格式和数据表参考

## 参考资料（已 clone 到本地）
~/Project/GLM/SandboxWorld/Terraria-Map-Editor/ — TEdit 地图编辑器仓库。关键文件：
- src/TEdit.Terraria/World.FileV2.cs (2629行)：.wld 格式完整读写。架构：文件头(version uint32) → section pointers（10-11个section的int32偏移）→ header flags（世界属性、出生点、地层、NPC列表等）→ tiles section（RLE+位标记压缩的 tile 数组）→ chests → signs → NPCs → tile entities → footer（"wld" 魔数校验）。你需要仔细阅读 LoadSectionHeader、LoadHeaderFlags、LoadTiles（理解 tile 的 RLE 压缩编码和 bit 标志位含义）、LoadChests、LoadNPCs，总结出 .wld 格式的技术要点写进方案（供后续 TS 实现参考）
- src/TEdit.Terraria/Tile.cs：tile 数据结构（IsActive/Type/WallType/Liquid/FrameX/FrameY/检查位标志 BitsByte）
- src/TEdit.Terraria/Data/tiles.json、walls.json、items.json、npcs.json：tile/wall/item/npc 定义数据表（id、名称、地图渲染颜色、融合规则等）
- src/TEdit.Terraria/Objects/TileProperty.cs 等：属性模型

## 功能范围（核心 + 进阶）
核心：
1. 程序化世界生成（地形起伏、表土层/石层、洞穴（噪声挖空）、矿石分布（铜铁银金+对应矿物深度）、树木、地表草地、基础生物群系分层、出生点、地下小屋可选）
2. 玩家系统：物理（重力/跳跃/行走/碰撞，与 tile 网格的 AABB 碰撞）、生命值、重生
3. 挖掘/放置：镐/斧/锤工具区分，工具挖掘力与 tile 硬度，挖掘范围，放置 tile/wall，物体（树）破坏逻辑
4. 光照系统：昼夜光照变化、火把等光源、光照传播（BFS/递归）、全图光照缓存（分层渲染：墙光照+tile光照）
5. 物品系统：物品栏+快捷栏、堆叠、掉落物实体与拾取（磁吸范围）、物品 tooltip
6. 合成系统：配方表（按可用合成站过滤：徒手/工作台/熔炉/铁砧）、合成 UI
7. 昼夜循环：时间流逝、天色渐变、月亮/太阳
8. 敌人与战斗：史莱姆（AI：跳跃追击）、夜间僵尸/恶魔眼、接触伤害与击退、玩家近战武器挥舞（旋转弧线）、伤害数字、敌人生成规则（光照/距离/数量上限）
9. 掉落表：敌人掉落、tile 破坏掉落
进阶：
10. 液体：水（流动模拟、简单元胞自动机）、液体渲染
11. 宝箱：世界生成放置宝箱+战利品表、打开宝箱 UI
12. NPC 系统：向导（Guide）入驻条件（空房间判定：封闭+门+光源+家具）、快乐度简化
13. Boss：克苏鲁之眼（夜间召唤/自然生成条件、两阶段 AI：旋转冲撞+召唤小眼球、血量条）
14. 熔炼/精炼：矿石→锭（熔炉）、基础工具/武器/护甲升级链

## 需要你产出的方案内容
1. 项目结构（目录树、模块划分、依赖）——考虑用 Vite + TS，无框架或轻量框架（建议不用 React，游戏主循环+UI 混合 DOM/Canvas 自绘由你判断）
2. 游戏主循环与状态架构（fixed timestep 物理与渲染分离、场景/状态管理、实体系统设计——ECS 还是简单类继承，给出推荐）
3. 各系统设计要点：
   - 世界数据结构（tile 数组怎么存、Uint8Array 多通道还是对象数组、性能考量、大世界 4200x1200 的内存与遍历）
   - 世界生成算法（噪声库选择如 simplex-noise，分层生成管线）
   - 光照算法（推荐 BFS 光衰减 + 脏矩形重算，性能方案）
   - 渲染管线（相机、视锥剔除、只渲染可视区域、tile 变体与边缘融合贴图程序化生成方案、minimap）
   - 程序化素材生成方案（sprite 怎么用代码画：噪声+调色板+边缘处理，tile sheet 运行时生成，item 图标、角色/敌人动画帧的生成策略）
   - 物理与碰撞（分轴扫描 tile AABB）
   - .wld 导入解析器设计（TS 实现，参照 World.FileV2.cs，给出关键格式要点摘要、分步解析流程、需要处理的 version 差异、tileFrameImportant 机制）
   - 自有存档格式设计
   - UI 架构（HUD、物品栏、合成、宝箱、菜单——DOM overlay vs canvas 自绘的取舍）
4. 分阶段实施计划（里程碑：M1 世界+移动+挖掘 → M2 光照+物品+合成 → M3 敌人+战斗 → M4 液体+宝箱+NPC → M5 Boss → M6 .wld 导入），每个里程碑列出具体文件与验收标准
5. 风险与注意事项

请先阅读 TEdit 的 World.FileV2.cs（重点是 LoadTiles 的 RLE 编码）、Tile.cs、以及 Data/*.json 的结构，再写方案。方案要具体到文件名和关键函数签名级别，但不要写出完整实现代码。方案用中文写。
```

---

## 📎 Attachment · skill_listing · 2026-08-04T16:35:31.669Z

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

## 🤖 Assistant · 2026-08-04T16:35:38.951Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the TEdit repository to understand the .wld format, tile structure, and data tables. I need to read World.FileV2.cs (especially LoadTiles RLE encoding), Tile.cs, and Data/*.json structures.

Let me plan my exploration:
1. List the TEdit directory structure
2. Read World.FileV2.cs - key sections (LoadSectionHeader, LoadHeaderFlags, LoadTiles, LoadChests, LoadNPCs)
3. Read Tile.cs
4. Look at Data/*.json structure (tiles.json, walls.json, items.json, npcs.json)
5. Look at TileProperty.cs

Then write the comprehensive plan in Chinese.

Let me start.
```

</details>


---

## 🤖 Assistant · 2026-08-04T16:35:39.451Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/ && echo \"---\" && ls ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/ | head -50",
 "description": "List project root and TEdit.Terraria directory"
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:39.498Z

**📎 ToolResult**

```
Terraria-Map-Editor
---
BannerItem.cs
Bestiary.cs
BestiaryConfiguration.cs
BitsByte.cs
BrickStyle.cs
Chest.cs
ChestSignTool.cs
CreativePowers.cs
Data
DataModel
FileType.cs
GlobalUsing.cs
IO
Item.cs
ITileData.cs
JunctionBoxMode.cs
KillTally.cs
LiquidType.cs
Loaders
Map.cs
Minecart.cs
ModDataSerializer.cs
NPC.cs
Objects
Player
PressurePlate.cs
Render
Sign.cs
TEdit.Terraria.csproj
TerrariaDataStore.cs
Tile.cs
TileEntity.cs
TileEntityItem.cs
TileEntityType.cs
TileType.cs
TModLoader
TownManager.cs
TownNpcKey.cs
Vector2FloatObservable.cs
Vector2Int32Observable.cs
World.cs
World.FileV1.cs
World.FileV2.cs
World.Properties.cs
WorldConfiguration.cs
WorldHeaderInfo.cs
WorldHeaderPatcher.cs
WorldValidationStatus.cs

```


---

## 🤖 Assistant · 2026-08-04T16:35:40.304Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void LoadTiles\\|void LoadSectionHeader\\|void LoadHeaderFlags\\|LoadChests\\|LoadNPCs\\|LoadSigns\\|LoadTileEntities\\|LoadFooter\\|LoadWorldHeader\\|tileFrameImportant\\|sectionPointer\" ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/World.FileV2.cs",
 "description": "Find key method locations in World.FileV2.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:40.337Z

**📎 ToolResult**

```
33:            bool[] tileFrameImportant;
34:            int[] sectionPointers;
50:            if (!LoadSectionHeader(b, out tileFrameImportant, out sectionPointers, w))
53:            w.TileFrameImportant = tileFrameImportant;
56:            if (b.BaseStream.Position != sectionPointers[0])
60:            LoadHeaderFlags(b, w, sectionPointers[1]);
61:            if (b.BaseStream.Position != sectionPointers[1])
64:            if (w.Version >= 210 && sectionPointers.Length > 9)
67:                b.BaseStream.Position = sectionPointers[8];
69:                if (b.BaseStream.Position != sectionPointers[9])
95:            if (!LoadSectionHeader(b, out var tileFrameImportant, out var sectionPointers, w))
98:            w.TileFrameImportant = tileFrameImportant;
100:            if (b.BaseStream.Position != sectionPointers[0])
104:            LoadHeaderFlags(b, w, sectionPointers[1]);
105:            if (b.BaseStream.Position != sectionPointers[1])
126:        int[] sectionPointers = new int[world.GetSectionCount()];
132:        bool[] tileFrameImportant;
137:            tileFrameImportant = new bool[maxLen];
138:            Array.Copy(world.TileFrameImportant, tileFrameImportant, world.TileFrameImportant.Length);
141:                tileFrameImportant[i] = configFrames[i];
145:            tileFrameImportant = configFrames;
149:        sectionPointers[0] = SaveSectionHeader(world, bw, tileFrameImportant);
150:        sectionPointers[1] = SaveHeaderFlags(world, bw, (int)world.Version);
152:        sectionPointers[2] = SaveTiles(world.Tiles, (int)world.Version, world.TilesWide, world.TilesHigh, bw, tileFrameImportant, preserveAll);
155:        sectionPointers[3] = SaveChests(world.Chests, bw, (int)world.Version, preserveAll);
157:        sectionPointers[4] = SaveSigns(world.Signs, bw, (int)world.Version);
160:        sectionPointers[5] = SaveNPCs(world, bw, (int)world.Version, preserveAll);
165:            sectionPointers[6] = SaveTileEntities(world.TileEntities, bw, world.Version);
171:            sectionPointers[7] = SavePressurePlate(world.PressurePlates, bw);
177:            sectionPointers[8] = SaveTownManager(world.PlayerRooms, bw, (int)world.Version, preserveAll);
183:            sectionPointers[9] = SaveBestiary(world.Bestiary, bw);
189:            sectionPointers[10] = SaveCreativePowers(world.CreativePowers, bw);
194:        UpdateSectionPointers(world.Version, sectionPointers, bw);
198:    public static int SaveTiles(Tile[,] tiles, int version, int maxX, int maxY, BinaryWriter bw, bool[] tileFrameImportant, bool preserveAll = false, IProgress<ProgressChangedEventArgs>? progress = null)
216:                byte[] tileData = SerializeTileData(tile, version, maxTileId, maxWallId, tileFrameImportant, out dataIndex, out headerIndex);
272:        bool[] tileFrameImportant,
310:            // For tiles beyond tileFrameImportant array, assume framed (preserve UV data)
311:            if (tile.Type < tileFrameImportant.Length ? tileFrameImportant[tile.Type] : true)
727:    public static int UpdateSectionPointers(uint worldVersion, int[] sectionPointers, BinaryWriter bw)
734:        bw.Write((short)sectionPointers.Length);
736:        for (int i = 0; i < sectionPointers.Length; i++)
738:            bw.Write(sectionPointers[i]);
744:    public static int SaveSectionHeader(World world, BinaryWriter bw, bool[] tileFrameImportant)
779:        WriteBitArray(bw, tileFrameImportant);
1390:        bool[] tileFrameImportant;
1391:        int[] sectionPointers;
1398:        if (!LoadSectionHeader(b, out tileFrameImportant, out sectionPointers, w))
1401:        w.TileFrameImportant = tileFrameImportant;
1404:        if (b.BaseStream.Position != sectionPointers[0])
1408:        LoadHeaderFlags(b, w, sectionPointers[1]);
1409:        if (b.BaseStream.Position != sectionPointers[1])
1417:        if (b.BaseStream.Position != sectionPointers[2])
1418:            b.BaseStream.Position = sectionPointers[2];
1432:        if (b.BaseStream.Position != sectionPointers[3])
1446:        if (b.BaseStream.Position != sectionPointers[4])
1450:        LoadNPCsData(b, w);
1451:        if (b.BaseStream.Position != sectionPointers[5])
1464:                LoadTileEntities(b, w);
1466:            if (b.BaseStream.Position != sectionPointers[6])
1473:            if (b.BaseStream.Position != sectionPointers[7])
1479:            if (b.BaseStream.Position != sectionPointers[8])
1485:            if (b.BaseStream.Position != sectionPointers[9])
1491:            if (b.BaseStream.Position != sectionPointers[10])
1496:        LoadFooter(b, w);
1501:    public static Tile[,] LoadTileData(BinaryReader r, int maxX, int maxY, int version, bool[] tileFrameImportant, IProgress<ProgressChangedEventArgs>? progress = null)
1515:                    Tile tile = DeserializeTileData(r, tileFrameImportant, version, out rle);
1546:    public static Tile DeserializeTileData(BinaryReader r, bool[] tileFrameImportant, int version, out int rle)
1607:            // For tiles beyond tileFrameImportant array, assume framed (read UV data)
1608:            bool isFramed = tileType < tileFrameImportant.Length ? tileFrameImportant[tileType] : true;
1835:    public static void LoadNPCsData(BinaryReader r, World w)
1935:    public static void LoadFooter(BinaryReader r, World w)
1970:    public static void LoadTileEntities(BinaryReader r, World w)
1990:    public static void LoadHeaderFlags(BinaryReader r, World w, int expectedPosition)
2499:    public static bool LoadSectionHeader(BinaryReader r, out bool[] tileFrameImportant, out int[] sectionPointers, World w)
2501:        tileFrameImportant = null;
2502:        sectionPointers = null;
2538:        sectionPointers = new int[sectionCount];
2541:            sectionPointers[i] = r.ReadInt32();
2545:        tileFrameImportant = ReadBitArray(r);

```


---

## 🤖 Assistant · 2026-08-04T16:35:44.344Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read the key sections of World.FileV2.cs. I'll read LoadTileData/DeserializeTileData (lines ~1501-1650), LoadSectionHeader (2499-2560), LoadHeaderFlags (1990-2500), LoadNPCsData, LoadFooter, LoadChests.

Let me read these chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-04T16:35:44.610Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/World.FileV2.cs",
 "offset": 1501,
 "limit": 340
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:44.625Z

**📎 ToolResult**

```
1501	    public static Tile[,] LoadTileData(BinaryReader r, int maxX, int maxY, int version, bool[] tileFrameImportant, IProgress<ProgressChangedEventArgs>? progress = null)
1502	    {
1503	        var tiles = new Tile[maxX, maxY];
1504	        int rle;
1505	        for (int x = 0; x < maxX; x++)
1506	        {
1507	            progress?.Report(
1508	                 new ProgressChangedEventArgs(x.ProgressPercentage(maxX), "Loading Tiles..."));
1509	
1510	            for (int y = 0; y < maxY; y++)
1511	            {
1512	                try
1513	                {
1514	
1515	                    Tile tile = DeserializeTileData(r, tileFrameImportant, version, out rle);
1516	
1517	
1518	                    tiles[x, y] = tile;
1519	
1520	                    while (rle > 0)
1521	                    {
1522	                        y++;
1523	
1524	                        if (y >= maxY)
1525	                        {
1526	                            break;
1527	                            throw new TEditFileFormatException(
1528	                                $"Invalid Tile Data: RLE Compression outside of bounds [{x},{y}]");
1529	                        }
1530	                        tiles[x, y] = tile;
1531	                        rle--;
1532	                    }
1533	                }
1534	                catch (Exception ex)
1535	                {
1536	                    System.Diagnostics.Debug.WriteLine($"Tile data recovery: {ex.Message}");
1537	                    // default(Tile) is valid zero state for structs — no null-fill needed
1538	                    return tiles;
1539	                }
1540	            }
1541	        }
1542	
1543	        return tiles;
1544	    }
1545	
1546	    public static Tile DeserializeTileData(BinaryReader r, bool[] tileFrameImportant, int version, out int rle)
1547	    {
1548	        Tile tile = new Tile();
1549	
1550	        int tileType = -1;
1551	        byte header4 = 0;
1552	        byte header3 = 0;
1553	        byte header2 = 0;
1554	        byte header1 = r.ReadByte();
1555	
1556	        bool hasHeader2 = false;
1557	        bool hasHeader3 = false;
1558	        bool hasHeader4 = false;
1559	
1560	        // check bit[0] to see if header2 has data
1561	        if ((header1 & 0b_0000_0001) == 0b_0000_0001)
1562	        {
1563	            hasHeader2 = true;
1564	            header2 = r.ReadByte();
1565	        }
1566	
1567	        // check bit[0] to see if header3 has data
1568	        if (hasHeader2 && (header2 & 0b_0000_0001) == 0b_0000_0001)
1569	        {
1570	            hasHeader3 = true;
1571	            header3 = r.ReadByte();
1572	        }
1573	
1574	        if (version >= 269) // 1.4.4+ 
1575	        {
1576	            // check bit[0] to see if header4 has data
1577	            if (hasHeader3 && (header3 & 0b_0000_0001) == 0b_0000_0001)
1578	            {
1579	                hasHeader4 = true;
1580	                header4 = r.ReadByte();
1581	            }
1582	        }
1583	
1584	        // check bit[1] for active tile
1585	        bool isActive = (header1 & 0b_0000_0010) == 0b_0000_0010;
1586	
1587	        if (isActive)
1588	        {
1589	            tile.IsActive = isActive;
1590	            // read tile type
1591	
1592	            if ((header1 & 0b_0010_0000) != 0b_0010_0000) // check bit[5] to see if tile is byte or little endian int16
1593	            {
1594	                // tile is byte
1595	                tileType = r.ReadByte();
1596	            }
1597	            else
1598	            {
1599	                // tile is little endian int16
1600	                byte lowerByte = r.ReadByte();
1601	                tileType = r.ReadByte();
1602	                tileType = tileType << 8 | lowerByte;
1603	            }
1604	            tile.Type = (ushort)tileType; // convert type to ushort after bit operations
1605	
1606	            // read frame UV coords
1607	            // For tiles beyond tileFrameImportant array, assume framed (read UV data)
1608	            bool isFramed = tileType < tileFrameImportant.Length ? tileFrameImportant[tileType] : true;
1609	            if (!isFramed)
1610	            {
1611	                tile.U = 0;//-1;
1612	                tile.V = 0;//-1;
1613	            }
1614	            else
1615	            {
1616	                // read UV coords
1617	                tile.U = r.ReadInt16();
1618	                tile.V = r.ReadInt16();
1619	
1620	                // reset timers
1621	                if (tile.Type == (int)TileType.Timer)
1622	                {
1623	                    tile.V = 0;
1624	                }
1625	
1626	            }
1627	
1628	            // check header3 bit[3] for tile color
1629	            if ((header3 & 0b_0000_1000) == 0b_0000_1000)
1630	            {
1631	                tile.TileColor = r.ReadByte();
1632	            }
1633	        }
1634	
1635	        // Read Walls
1636	        if ((header1 & 0b_0000_0100) == 0b_0000_0100) // check bit[3] bit for active wall
1637	        {
1638	            tile.Wall = r.ReadByte();
1639	
1640	
1641	            // check bit[4] of header3 to see if there is a wall color
1642	            if ((header3 & 0b_0001_0000) == 0b_0001_0000)
1643	            {
1644	                tile.WallColor = r.ReadByte();
1645	            }
1646	        }
1647	
1648	        // check for liquids, grab the bit[3] and bit[4], shift them to the 0 and 1 bits
1649	        byte liquidType = (byte)((header1 & 0b_0001_1000) >> 3);
1650	        if (liquidType != 0)
1651	        {
1652	            tile.LiquidAmount = r.ReadByte();
1653	            tile.LiquidType = (LiquidType)liquidType; // water, lava, honey
1654	
1655	            // shimmer (v 1.4.4 +)
1656	            if (version >= 269 && (header3 & 0b_1000_0000) == 0b_1000_0000)
1657	            {
1658	                tile.LiquidType = LiquidType.Shimmer;
1659	            }
1660	
1661	        }
1662	
1663	        // check if we have data in header2 other than just telling us we have header3
1664	        if (header2 > 1)
1665	        {
1666	            // check bit[1] for red wire
1667	            if ((header2 & 0b_0000_0010) == 0b_0000_0010)
1668	            {
1669	                tile.WireRed = true;
1670	            }
1671	            // check bit[2] for blue wire
1672	            if ((header2 & 0b_0000_0100) == 0b_0000_0100)
1673	            {
1674	                tile.WireBlue = true;
1675	            }
1676	            // check bit[3] for green wire
1677	            if ((header2 & 0b_0000_1000) == 0b_0000_1000)
1678	            {
1679	                tile.WireGreen = true;
1680	            }
1681	
1682	            // grab bits[4, 5, 6] and shift 4 places to 0,1,2. This byte is our brick style
1683	            byte brickStyle = (byte)((header2 & 0b_0111_0000) >> 4);
1684	            if (brickStyle != 0)
1685	            {
1686	                // For unknown tiles (beyond TileProperties), preserve brick style data
1687	                bool hasSlopes = tile.Type >= WorldConfiguration.TileProperties.Count
1688	                    || WorldConfiguration.TileProperties[tile.Type].HasSlopes;
1689	                if (hasSlopes)
1690	                {
1691	                    tile.BrickStyle = (BrickStyle)brickStyle;
1692	                }
1693	            }
1694	        }
1695	
1696	        // check if we have data in header3 to process
1697	        if (header3 > 1)
1698	        {
1699	            // check bit[1] for actuator
1700	            if ((header3 & 0b_0000_0010) == 0b_0000_0010)
1701	            {
1702	                tile.Actuator = true;
1703	            }
1704	
1705	            // check bit[2] for inactive due to actuator
1706	            if ((header3 & 0b_0000_0100) == 0b_0000_0100)
1707	            {
1708	                tile.InActive = true;
1709	            }
1710	
1711	            if ((header3 & 0b_0010_0000) == 0b_0010_0000)
1712	            {
1713	                tile.WireYellow = true;
1714	            }
1715	
1716	            if (version >= 222)
1717	            {
1718	                if ((header3 & 0b_0100_0000) == 0b_0100_0000)
1719	                {
1720	                    tile.Wall = (ushort)(r.ReadByte() << 8 | tile.Wall);
1721	
1722	                }
1723	            }
1724	        }
1725	
1726	        if (version >= 269 && header4 > (byte)1)
1727	        {
1728	            if ((header4 & 0b_0000_0010) == 0b_0000_0010)
1729	            {
1730	                tile.InvisibleBlock = true;
1731	            }
1732	            if ((header4 & 0b_0000_0100) == 0b_0000_0100)
1733	            {
1734	                tile.InvisibleWall = true;
1735	            }
1736	            if ((header4 & 0b_0000_1000) == 0b_0000_1000)
1737	            {
1738	                tile.FullBrightBlock = true;
1739	            }
1740	            if ((header4 & 0b_0001_0000) == 0b_0001_0000)
1741	            {
1742	                tile.FullBrightWall = true;
1743	            }
1744	        }
1745	
1746	        // get bit[6,7] shift to 0,1 for RLE encoding type
1747	        // 0 = no RLE compression
1748	        // 1 = byte RLE counter
1749	        // 2 = int16 RLE counter
1750	        // 3 = not implemented, assume int16
1751	        byte rleStorageType = (byte)((header1 & 192) >> 6);
1752	
1753	        rle = rleStorageType switch
1754	        {
1755	            0 => (int)0,
1756	            1 => (int)r.ReadByte(),
1757	            _ => (int)r.ReadInt16()
1758	        };
1759	
1760	        tile.ResetCache();
1761	        return tile;
1762	    }
1763	
1764	    public static IEnumerable<Chest> LoadChestData(BinaryReader r, uint version)
1765	    {
1766	        int totalChests = r.ReadInt16();
1767	
1768	        int maxItems = 40;
1769	
1770	        if (version < 294)
1771	        {
1772	            maxItems = r.ReadInt16();
1773	        }
1774	
1775	        // read chests
1776	        for (int i = 0; i < totalChests; i++)
1777	        {
1778	            var chest = new Chest
1779	            {
1780	                X = r.ReadInt32(),
1781	                Y = r.ReadInt32(),
1782	                Name = r.ReadString()
1783	            };
1784	
1785	
1786	            if (version >= 294)
1787	            {
1788	                chest.MaxItems = r.ReadInt32();
1789	            }
1790	
1791	            // ensure Items collection has enough slots for MaxItems
1792	            while (chest.Items.Count < chest.MaxItems)
1793	            {
1794	                chest.Items.Add(new Item());
1795	            }
1796	
1797	            // read items in chest
1798	            for (int slot = 0; slot < chest.MaxItems; slot++)
1799	            {
1800	                var stackSize = r.ReadInt16();
1801	                chest.Items[slot].StackSize = stackSize;
1802	
1803	                if (stackSize > 0)
1804	                {
1805	                    int id = r.ReadInt32();
1806	                    byte prefix = r.ReadByte();
1807	
1808	                    chest.Items[slot].NetId = id;
1809	                    chest.Items[slot].StackSize = stackSize;
1810	                    chest.Items[slot].Prefix = prefix;
1811	
1812	                }
1813	            }
1814	
1815	
1816	
1817	            yield return chest;
1818	        }
1819	
1820	    }
1821	
1822	    public static IEnumerable<Sign> LoadSignData(BinaryReader r)
1823	    {
1824	        short totalSigns = r.ReadInt16();
1825	
1826	        for (int i = 0; i < totalSigns; i++)
1827	        {
1828	            string text = r.ReadString();
1829	            int x = r.ReadInt32();
1830	            int y = r.ReadInt32();
1831	            yield return new Sign(x, y, text);
1832	        }
1833	    }
1834	
1835	    public static void LoadNPCsData(BinaryReader r, World w)
1836	    {
1837	        // load shimmerd town
1838	        if (w.Version >= 268)
1839	        {
1840	            int numNpcs = r.ReadInt32();

```


---

## 🤖 Assistant · 2026-08-04T16:35:44.878Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/World.FileV2.cs",
 "offset": 2499,
 "limit": 70
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:44.895Z

**📎 ToolResult**

```
2499	    public static bool LoadSectionHeader(BinaryReader r, out bool[] tileFrameImportant, out int[] sectionPointers, World w)
2500	    {
2501	        tileFrameImportant = null;
2502	        sectionPointers = null;
2503	        uint versionNumber = r.ReadUInt32();
2504	
2505	        if (versionNumber >= 140) // 135
2506	        {
2507	            // check for chinese
2508	
2509	            w.IsChinese = (char)r.PeekChar() == 'x';
2510	
2511	            string headerFormat = new string(r.ReadChars(7));
2512	            FileType fileType = (FileType)r.ReadByte();
2513	
2514	            if (fileType != FileType.World)
2515	            {
2516	                throw new TEditFileFormatException($"Is not a supported file type: {fileType.ToString()}");
2517	            }
2518	
2519	            if (!w.IsChinese && headerFormat != WorldConfiguration.DesktopHeader)
2520	            {
2521	                throw new TEditFileFormatException("Invalid desktop world header.");
2522	            }
2523	
2524	            if (w.IsChinese && headerFormat != WorldConfiguration.ChineseHeader)
2525	            {
2526	                throw new TEditFileFormatException("Invalid chinese world header.");
2527	            }
2528	
2529	            w.FileRevision = r.ReadUInt32();
2530	
2531	            UInt64 flags = r.ReadUInt64(); // load bitflags (currently only bit 1 isFavorite is used)
2532	            w.IsFavorite = ((flags & 1uL) == 1uL);
2533	
2534	        }
2535	
2536	        // read file section stream positions
2537	        int sectionCount = r.ReadInt16();
2538	        sectionPointers = new int[sectionCount];
2539	        for (int i = 0; i < sectionCount; i++)
2540	        {
2541	            sectionPointers[i] = r.ReadInt32();
2542	        }
2543	
2544	        // Read tile frame importance from bit-packed data
2545	        tileFrameImportant = ReadBitArray(r);
2546	
2547	        return true;
2548	    }
2549	
2550	    /// <summary>
2551	    /// Read an array of booleans from a bit-packed array.
2552	    /// </summary>
2553	    /// <param name="reader">BinaryReader at start of bit array.</param>
2554	    /// <returns>Array of booleans</returns>
2555	    public static bool[] ReadBitArray(BinaryReader reader)
2556	    {
2557	        // get the number of bits
2558	        int length = reader.ReadInt16();
2559	
2560	        // read the bit data
2561	        var booleans = new bool[length];
2562	        byte data = 0;
2563	        byte bitMask = 128;
2564	        for (int i = 0; i < length; i++)
2565	        {
2566	            // If we read the last bit mask (B1000000 = 0x80 = 128), read the next byte from the stream and start the mask over.
2567	            // Otherwise, keep incrementing the mask to get the next bit.
2568	            if (bitMask != 128)

```


---

## 🤖 Assistant · 2026-08-04T16:35:49.187Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read LoadHeaderFlags (1990-2499) — this is long, let me read key parts. And LoadNPCsData continuation, LoadFooter, LoadTileEntities. Let me also check the header flags order.
```

</details>


---

## 🤖 Assistant · 2026-08-04T16:35:49.464Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/World.FileV2.cs",
 "limit": 130,
 "offset": 1835
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:49.492Z

**📎 ToolResult**

```
1835	    public static void LoadNPCsData(BinaryReader r, World w)
1836	    {
1837	        // load shimmerd town
1838	        if (w.Version >= 268)
1839	        {
1840	            int numNpcs = r.ReadInt32();
1841	            w.ShimmeredTownNPCs.Clear();
1842	
1843	            for (int i = 0; i < numNpcs; i++)
1844	            {
1845	                w.ShimmeredTownNPCs.Add(r.ReadInt32());
1846	            }
1847	        }
1848	
1849	        // load npc
1850	        int totalNpcs = 0;
1851	        for (bool i = r.ReadBoolean(); i; i = r.ReadBoolean())
1852	        {
1853	            NPC npc = new NPC();
1854	            if (w.Version >= 190)
1855	            {
1856	                npc.SpriteId = r.ReadInt32();
1857	                if (WorldConfiguration.NpcNames.ContainsKey(npc.SpriteId))
1858	                    npc.Name = WorldConfiguration.NpcNames[npc.SpriteId];
1859	            }
1860	            else
1861	            {
1862	                npc.Name = r.ReadString();
1863	                if (WorldConfiguration.NpcIds.ContainsKey(npc.Name))
1864	                    npc.SpriteId = WorldConfiguration.NpcIds[npc.Name];
1865	            }
1866	            npc.DisplayName = r.ReadString();
1867	            npc.Position = new Vector2FloatObservable(r.ReadSingle(), r.ReadSingle());
1868	            npc.IsHomeless = r.ReadBoolean();
1869	            npc.Home = new Vector2Int32Observable(r.ReadInt32(), r.ReadInt32());
1870	
1871	            if (w.Version >= 213 && ((BitsByte)r.ReadByte())[0])
1872	            {
1873	                npc.TownNpcVariationIndex = r.ReadInt32();
1874	            }
1875	
1876	            if (w.Version >= 315)
1877	            {
1878	                npc.HomelessDespawn = r.ReadBoolean();
1879	            }
1880	
1881	            w.NPCs.Add(npc);
1882	            totalNpcs++;
1883	        }
1884	
1885	        // load mobs
1886	        if (w.Version >= 140)
1887	        {
1888	            int totalMobs = 0;
1889	            bool flag = r.ReadBoolean();
1890	            while (flag)
1891	            {
1892	                NPC npc = new NPC();
1893	                if (w.Version >= 190)
1894	                {
1895	                    npc.SpriteId = r.ReadInt32();
1896	                }
1897	                else
1898	                {
1899	                    npc.Name = r.ReadString();
1900	                    if (WorldConfiguration.NpcIds.ContainsKey(npc.Name))
1901	                        npc.SpriteId = WorldConfiguration.NpcIds[npc.Name];
1902	                }
1903	                npc.Position = new Vector2FloatObservable(r.ReadSingle(), r.ReadSingle());
1904	                w.Mobs.Add(npc);
1905	                totalMobs++;
1906	                flag = r.ReadBoolean();
1907	            }
1908	        }
1909	    }
1910	    public static void LoadTownManager(BinaryReader r, World w)
1911	    {
1912	        int totalRooms = r.ReadInt32();
1913	        for (int i = 0; i < totalRooms; i++)
1914	        {
1915	            TownManager room = new TownManager();
1916	            room.NpcId = r.ReadInt32();
1917	            room.Home = new Vector2Int32Observable(r.ReadInt32(), r.ReadInt32());
1918	            w.PlayerRooms.Add(room);
1919	        }
1920	    }
1921	
1922	    public static void LoadBestiary(BinaryReader r, World w)
1923	    {
1924	        w.Bestiary = new Bestiary();
1925	        w.Bestiary.Load(r, w.Version);
1926	    }
1927	
1928	    public static void LoadCreativePowers(BinaryReader r, World w)
1929	    {
1930	        w.CreativePowers = new CreativePowers();
1931	        w.CreativePowers.Load(r, w.Version);
1932	    }
1933	
1934	
1935	    public static void LoadFooter(BinaryReader r, World w)
1936	    {
1937	        if (!r.ReadBoolean())
1938	            throw new TEditFileFormatException("Invalid Footer");
1939	
1940	        if (r.ReadString() != w.Title)
1941	            throw new TEditFileFormatException("Invalid Footer");
1942	
1943	        if (r.ReadInt32() != w.WorldId)
1944	            throw new TEditFileFormatException("Invalid Footer");
1945	    }
1946	
1947	    public static List<TileEntity> LoadTileEntityData(BinaryReader r, uint version)
1948	    {
1949	        int numEntities = r.ReadInt32();
1950	        var entities = new List<TileEntity>();
1951	        for (int i = 0; i < numEntities; i++)
1952	        {
1953	            TileEntity entity = new TileEntity();
1954	            entity.Load(r, version);
1955	            entities.Add(entity);
1956	        }
1957	        return entities;
1958	    }
1959	
1960	    public static void LoadDummies(BinaryReader r, World w)
1961	    {
1962	        // load past deprecated dummies
1963	        int count = r.ReadInt32();
1964	        for (int i = 0; i < count; i++)

```


---

## 🤖 Assistant · 2026-08-04T16:35:49.735Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/World.FileV2.cs",
 "limit": 200,
 "offset": 1990
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:49.738Z

**📎 ToolResult**

```
1990	    public static void LoadHeaderFlags(BinaryReader r, World w, int expectedPosition)
1991	    {
1992	        w.Title = r.ReadString();
1993	        if (w.Version >= 179)
1994	        {
1995	            if (w.Version == 179)
1996	                w.Seed = r.ReadInt32().ToString();
1997	            else
1998	                w.Seed = r.ReadString();
1999	            w.WorldGenVersion = r.ReadUInt64();
2000	        }
2001	        else
2002	            w.Seed = "";
2003	        if (w.Version >= 181)
2004	        {
2005	            w.WorldGUID = new Guid(r.ReadBytes(16));
2006	        }
2007	        else
2008	        {
2009	            w.WorldGUID = Guid.NewGuid();
2010	        }
2011	        w.WorldId = r.ReadInt32();
2012	        w.LeftWorld = (float)r.ReadInt32();
2013	        w.RightWorld = (float)r.ReadInt32();
2014	        w.TopWorld = (float)r.ReadInt32();
2015	        w.BottomWorld = (float)r.ReadInt32();
2016	        w.TilesHigh = r.ReadInt32();
2017	        w.TilesWide = r.ReadInt32();
2018	
2019	        if (w.Version >= 209)
2020	        {
2021	            w.GameMode = r.ReadInt32();
2022	
2023	            if (w.Version >= 222) { w.DrunkWorld = r.ReadBoolean(); }
2024	            if (w.Version >= 227) { w.GoodWorld = r.ReadBoolean(); }
2025	            if (w.Version >= 238) { w.TenthAnniversaryWorld = r.ReadBoolean(); }
2026	            if (w.Version >= 239) { w.DontStarveWorld = r.ReadBoolean(); }
2027	            if (w.Version >= 241) { w.NotTheBeesWorld = r.ReadBoolean(); }
2028	            if (w.Version >= 249) { w.RemixWorld = r.ReadBoolean(); }
2029	            if (w.Version >= 266) { w.NoTrapsWorld = r.ReadBoolean(); }
2030	            w.ZenithWorld = (w.Version < 267) ? w.RemixWorld && w.DrunkWorld : r.ReadBoolean();
2031	            if (w.Version >= 302) { w.SkyblockWorld = r.ReadBoolean(); }
2032	        }
2033	        else if (w.Version == 208)
2034	        {
2035	            w.GameMode = r.ReadBoolean() ? 2 : 0;
2036	        }
2037	        else if (w.Version >= 112)
2038	        {
2039	            w.GameMode = r.ReadBoolean() ? 1 : 0;
2040	        }
2041	        else
2042	        {
2043	            w.GameMode = 0;
2044	        }
2045	
2046	        w.CreationTime = w.Version >= 141 ? r.ReadInt64() : DateTime.Now.ToBinary();
2047	        w.LastPlayed = w.Version >= 284 ? r.ReadInt64() : DateTime.Now.ToBinary();
2048	
2049	        w.MoonType = r.ReadByte();
2050	        w.TreeX[0] = r.ReadInt32();
2051	        w.TreeX[1] = r.ReadInt32();
2052	        w.TreeX[2] = r.ReadInt32();
2053	        w.TreeX2 = w.TreeX[2];
2054	        w.TreeX1 = w.TreeX[1];
2055	        w.TreeX0 = w.TreeX[0];
2056	        w.TreeStyle0 = r.ReadInt32();
2057	        w.TreeStyle1 = r.ReadInt32();
2058	        w.TreeStyle2 = r.ReadInt32();
2059	        w.TreeStyle3 = r.ReadInt32();
2060	        w.CaveBackX[0] = r.ReadInt32();
2061	        w.CaveBackX[1] = r.ReadInt32();
2062	        w.CaveBackX[2] = r.ReadInt32();
2063	        w.CaveBackX2 = w.CaveBackX[2];
2064	        w.CaveBackX1 = w.CaveBackX[1];
2065	        w.CaveBackX0 = w.CaveBackX[0];
2066	        w.CaveBackStyle0 = r.ReadInt32();
2067	        w.CaveBackStyle1 = r.ReadInt32();
2068	        w.CaveBackStyle2 = r.ReadInt32();
2069	        w.CaveBackStyle3 = r.ReadInt32();
2070	        w.IceBackStyle = r.ReadInt32();
2071	        w.JungleBackStyle = r.ReadInt32();
2072	        w.HellBackStyle = r.ReadInt32();
2073	
2074	        w.SpawnX = r.ReadInt32();
2075	        w.SpawnY = r.ReadInt32();
2076	        w.GroundLevel = r.ReadDouble();
2077	        w.RockLevel = r.ReadDouble();
2078	        w.Time = r.ReadDouble();
2079	        w.DayTime = r.ReadBoolean();
2080	        w.MoonPhase = r.ReadInt32();
2081	        w.BloodMoon = r.ReadBoolean();
2082	        w.IsEclipse = r.ReadBoolean();
2083	        w.DungeonX = r.ReadInt32();
2084	        w.DungeonY = r.ReadInt32();
2085	
2086	        w.IsCrimson = r.ReadBoolean();
2087	
2088	        w.DownedBoss1EyeofCthulhu = r.ReadBoolean();
2089	        w.DownedBoss2EaterofWorlds = r.ReadBoolean();
2090	        w.DownedBoss3Skeletron = r.ReadBoolean();
2091	        w.DownedQueenBee = r.ReadBoolean();
2092	        w.DownedMechBoss1TheDestroyer = r.ReadBoolean();
2093	        w.DownedMechBoss2TheTwins = r.ReadBoolean();
2094	        w.DownedMechBoss3SkeletronPrime = r.ReadBoolean();
2095	        w.DownedMechBossAny = r.ReadBoolean();
2096	        w.DownedPlantBoss = r.ReadBoolean();
2097	        w.DownedGolemBoss = r.ReadBoolean();
2098	
2099	        if (w.Version >= 118) { w.DownedSlimeKingBoss = r.ReadBoolean(); }
2100	
2101	        w.SavedGoblin = r.ReadBoolean();
2102	        w.SavedWizard = r.ReadBoolean();
2103	        w.SavedMech = r.ReadBoolean();
2104	        w.DownedGoblins = r.ReadBoolean();
2105	        w.DownedClown = r.ReadBoolean();
2106	        w.DownedFrost = r.ReadBoolean();
2107	        w.DownedPirates = r.ReadBoolean();
2108	
2109	        w.ShadowOrbSmashed = r.ReadBoolean();
2110	        w.SpawnMeteor = r.ReadBoolean();
2111	        w.ShadowOrbCount = (int)r.ReadByte();
2112	        w.AltarCount = r.ReadInt32();
2113	        w.HardMode = r.ReadBoolean();
2114	        if (w.Version >= 257) { w.PartyOfDoom = r.ReadBoolean(); }
2115	        w.InvasionDelay = r.ReadInt32();
2116	        w.InvasionSize = r.ReadInt32();
2117	        w.InvasionType = r.ReadInt32();
2118	        w.InvasionX = r.ReadDouble();
2119	
2120	        if (w.Version >= 118) { w.SlimeRainTime = r.ReadDouble(); }
2121	
2122	        if (w.Version >= 113) { w.SundialCooldown = r.ReadByte(); }
2123	
2124	        w.IsRaining = r.ReadBoolean();
2125	        w.TempRainTime = r.ReadInt32();
2126	        w.TempMaxRain = r.ReadSingle();
2127	        w.SavedOreTiersCobalt = r.ReadInt32();
2128	        w.SavedOreTiersMythril = r.ReadInt32();
2129	        w.SavedOreTiersAdamantite = r.ReadInt32();
2130	        w.BgTree = r.ReadByte();
2131	        w.BgCorruption = r.ReadByte();
2132	        w.BgJungle = r.ReadByte();
2133	        w.BgSnow = r.ReadByte();
2134	        w.BgHallow = r.ReadByte();
2135	        w.BgCrimson = r.ReadByte();
2136	        w.BgDesert = r.ReadByte();
2137	        w.BgOcean = r.ReadByte();
2138	        w.CloudBgActive = (float)r.ReadInt32();
2139	        w.NumClouds = r.ReadInt16();
2140	        w.WindSpeedSet = r.ReadSingle();
2141	
2142	        if (w.Version < 95) { return; }
2143	
2144	        for (int i = r.ReadInt32(); i > 0; i--)
2145	        {
2146	            w.Anglers.Add(r.ReadString());
2147	        }
2148	
2149	        if (w.Version < 99) { return; }
2150	
2151	        w.SavedAngler = r.ReadBoolean();
2152	
2153	        if (w.Version < 101) { return; }
2154	        w.AnglerQuest = r.ReadInt32();
2155	
2156	        if (w.Version < 104) { return; }
2157	
2158	        w.SavedStylist = r.ReadBoolean();
2159	
2160	        if (w.Version >= 140)
2161	        {
2162	            w.SavedTaxCollector = r.ReadBoolean();
2163	        }
2164	
2165	        if (w.Version >= 201)
2166	        {
2167	            w.SavedGolfer = r.ReadBoolean();
2168	        }
2169	
2170	        if (w.Version >= 107)
2171	        {
2172	            w.InvasionSizeStart = r.ReadInt32();
2173	        }
2174	        w.CultistDelay = w.Version >= 108 ? r.ReadInt32() : 86400;
2175	
2176	        if (w.Version < 109) { return; }
2177	
2178	        LoadBanners(r, w);
2179	
2180	        if (w.Version < 128) { return; }
2181	
2182	        if (w.Version >= 140)
2183	        {
2184	            w.FastForwardTime = r.ReadBoolean();
2185	        }
2186	
2187	        if (w.Version < 131) { return; }
2188	
2189	        w.DownedFishron = r.ReadBoolean();

```


---

## 🤖 Assistant · 2026-08-04T16:35:55.639Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have a good understanding of the header flags (they go on with many version-gated fields). Now let me read Tile.cs and look at data JSON structures.
```

</details>


---

## 🤖 Assistant · 2026-08-04T16:35:55.779Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Tile.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:55.786Z

**📎 ToolResult**

```
1	using System;
2	using TEdit.Geometry;
3	
4	namespace TEdit.Terraria;
5	
6	public struct Tile : IEquatable<Tile>
7	{
8	    public bool IsEmpty { get => !IsActive && Wall == 0 && !HasLiquid && !HasWire && !Actuator; }
9	    public bool HasWire { get => WireBlue || WireRed || WireGreen || WireYellow; }
10	    public bool HasLiquid { get => LiquidAmount > 0 && LiquidType != LiquidType.None; }
11	    public bool HasMultipleWires
12	    {
13	        get
14	        {
15	            if (WireRed && (WireGreen || WireBlue || WireYellow)) return true;
16	            if (WireGreen && (WireBlue || WireYellow)) return true;
17	            if (WireBlue && WireYellow) return true;
18	
19	            return false;
20	        }
21	    }
22	
23	    public bool Actuator;
24	    public BrickStyle BrickStyle;
25	    public bool InActive;
26	    public bool IsActive;
27	    public bool v0_Lit;
28	    public byte LiquidAmount;
29	    public LiquidType LiquidType;
30	    public byte TileColor;
31	    public ushort Type;
32	    public Int16 U;
33	    public Int16 V;
34	    public ushort Wall;
35	    public byte WallColor;
36	    public bool WireBlue;
37	    public bool WireGreen;
38	    public bool WireRed;
39	    public bool WireYellow;
40	    public bool InvisibleBlock;
41	    public bool InvisibleWall;
42	    public bool FullBrightBlock;
43	    public bool FullBrightWall;
44	
45	    /* Heathtech */
46	    public ushort uvTileCache; //Caches the UV position of a tile, since it is costly to generate each frame
47	    /* Heathtech */
48	    public ushort uvWallCache; //Caches the UV position of a wall tile
49	    /* Heathtech */
50	    public byte lazyMergeId; //The ID here refers to a number that helps blocks know whether they are actually merged with a nearby tile
51	    /* Heathtech */
52	    public bool hasLazyChecked; //Whether the above check has taken place
53	
54	    /// <summary>
55	    /// Initializes cache fields to sentinel values.
56	    /// Note: new Tile[,] arrays use default(Tile) which skips this constructor.
57	    /// </summary>
58	    public Tile()
59	    {
60	        uvTileCache = 0xFFFF;
61	        uvWallCache = 0xFFFF;
62	        lazyMergeId = 0xFF;
63	    }
64	
65	    /// <summary>
66	    /// Resets all cache fields to their "not computed" sentinel values.
67	    /// Call after deserialization or when invalidating render caches.
68	    /// </summary>
69	    public void ResetCache()
70	    {
71	        uvTileCache = 0xFFFF;
72	        uvWallCache = 0xFFFF;
73	        lazyMergeId = 0xFF;
74	        hasLazyChecked = false;
75	    }
76	
77	    public Vector2Short GetUV() => new Vector2Short(U, V);
78	
79	    public override bool Equals(object obj)
80	    {
81	        return obj is Tile other && Equals(other);
82	    }
83	
84	    /// <summary>
85	    /// Compares serialized tile properties. Ignores cache fields.
86	    /// </summary>
87	    public bool Equals(Tile other)
88	    {
89	        return IsActive == other.IsActive &&
90	               Type == other.Type &&
91	               U == other.U &&
92	               V == other.V &&
93	               TileColor == other.TileColor &&
94	               Wall == other.Wall &&
95	               WallColor == other.WallColor &&
96	               LiquidAmount == other.LiquidAmount &&
97	               LiquidType == other.LiquidType &&
98	               WireRed == other.WireRed &&
99	               WireGreen == other.WireGreen &&
100	               WireBlue == other.WireBlue &&
101	               WireYellow == other.WireYellow &&
102	               BrickStyle == other.BrickStyle &&
103	               Actuator == other.Actuator &&
104	               InActive == other.InActive &&
105	               InvisibleBlock == other.InvisibleBlock &&
106	               InvisibleWall == other.InvisibleWall &&
107	               FullBrightBlock == other.FullBrightBlock &&
108	               FullBrightWall == other.FullBrightWall;
109	    }
110	
111	    public override int GetHashCode()
112	    {
113	        int hashCode = -1661845228;
114	        hashCode = hashCode * -1521134295 + IsActive.GetHashCode();
115	        hashCode = hashCode * -1521134295 + Type.GetHashCode();
116	        hashCode = hashCode * -1521134295 + U.GetHashCode();
117	        hashCode = hashCode * -1521134295 + V.GetHashCode();
118	        hashCode = hashCode * -1521134295 + TileColor.GetHashCode();
119	        hashCode = hashCode * -1521134295 + Wall.GetHashCode();
120	        hashCode = hashCode * -1521134295 + WallColor.GetHashCode();
121	        hashCode = hashCode * -1521134295 + LiquidAmount.GetHashCode();
122	        hashCode = hashCode * -1521134295 + LiquidType.GetHashCode();
123	        hashCode = hashCode * -1521134295 + WireRed.GetHashCode();
124	        hashCode = hashCode * -1521134295 + WireGreen.GetHashCode();
125	        hashCode = hashCode * -1521134295 + WireBlue.GetHashCode();
126	        hashCode = hashCode * -1521134295 + WireYellow.GetHashCode();
127	        hashCode = hashCode * -1521134295 + BrickStyle.GetHashCode();
128	        hashCode = hashCode * -1521134295 + Actuator.GetHashCode();
129	        hashCode = hashCode * -1521134295 + InActive.GetHashCode();
130	        hashCode = hashCode * -1521134295 + InvisibleBlock.GetHashCode();
131	        hashCode = hashCode * -1521134295 + InvisibleWall.GetHashCode();
132	        hashCode = hashCode * -1521134295 + FullBrightBlock.GetHashCode();
133	        hashCode = hashCode * -1521134295 + FullBrightWall.GetHashCode();
134	        return hashCode;
135	    }
136	
137	    public static bool operator ==(Tile left, Tile right)
138	    {
139	        return left.Equals(right);
140	    }
141	
142	    public static bool operator !=(Tile left, Tile right)
143	    {
144	        return !left.Equals(right);
145	    }
146	
147	    // Added legacy enums back
148	    public enum WallType : int
149	    {
150	        Sky = 0,
151	        StoneWall = 1,
152	        DirtWall = 2
153	    }
154	
155	    public enum TileType : int
156	    {
157	        DirtBlock = 0,
158	        StoneBlock = 1,
159	        GrassBlock = 2,
160	        AshBlock = 57
161	    }
162	
163	    /// <summary>Clears tile-only fields (Type, U, V, color, style, coatings). Preserves wall, liquid, and wire state.</summary>
164	    public void ClearTile()
165	    {
166	        IsActive = false;
167	        InActive = false;
168	        Actuator = false;
169	        Type = 0;
170	        U = 0;
171	        V = 0;
172	        TileColor = 0;
173	        BrickStyle = 0;
174	        InvisibleBlock = false;
175	        FullBrightBlock = false;
176	    }
177	
178	    public void Reset()
179	    {
180	        Actuator = false;
181	        BrickStyle = 0;
182	        InActive = false;
183	        IsActive = false;
184	        LiquidAmount = 0;
185	        LiquidType = 0;
186	        TileColor = 0;
187	        Type = 0;
188	        U = 0;
189	        V = 0;
190	        Wall = 0;
191	        WallColor = 0;
192	        WireBlue = false;
193	        WireGreen = false;
194	        WireRed = false;
195	        WireYellow = false;
196	        FullBrightBlock = false;
197	        FullBrightWall = false;
198	        InvisibleBlock = false;
199	        InvisibleWall = false;
200	    }
201	
202	    public bool IsTileEntity() => TileTypes.IsTileEntity(Type);
203	    public bool IsChest() => TileTypes.IsChest(Type);
204	    public bool IsSign() => TileTypes.IsSign(Type);
205	    public bool StopsWallsFloodFill() => TileTypes.StopsWallsFloodFill(Type);
206	}
207	

```


---

## 🤖 Assistant · 2026-08-04T16:35:56.617Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Data && ls | head -40 && echo \"=== tiles.json head ===\" && head -c 1200 tiles.json && echo \"\" && echo \"=== walls.json head ===\" && head -c 600 walls.json && echo \"\" && echo \"=== items.json head ===\" && head -c 600 items.json && echo \"\" && echo \"=== npcs.json head ===\" && head -c 600 npcs.json",
 "description": "Inspect data JSON structures"
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:35:56.669Z

**📎 ToolResult**

```
backgroundStyles.json
bestiaryNpcs.json
dyes.json
globalColors.json
items.json
Localization
morphBiomes.json
npcs.json
paints.json
prefixes.json
TileOverrides
tiles.json
versions.json
walls.json
=== tiles.json head ===
[
  {
    "id": 0,
    "isSolid": true,
    "canBlend": true,
    "textureGrid": [16, 16],
    "frameGap": [2, 2],
    "frameSize": [[1, 1]],
    "name": "Dirt Block",
    "key": "Dirt",
    "color": "#976B4BFF"
  },
  {
    "id": 1,
    "isSolid": true,
    "isStone": true,
    "canBlend": true,
    "mergeWith": 0,
    "textureGrid": [16, 16],
    "frameGap": [2, 2],
    "frameSize": [[1, 1]],
    "name": "Stone Block",
    "key": "Stone",
    "color": "#808080FF"
  },
  {
    "id": 2,
    "isSolid": true,
    "isGrass": true,
    "canBlend": true,
    "mergeWith": 0,
    "textureGrid": [16, 16],
    "frameGap": [2, 2],
    "frameSize": [[1, 1]],
    "name": "Grass Block",
    "key": "Grass",
    "color": "#1CD85EFF",
    "special": "Grass"
  },
  {
    "id": 3,
    "isFramed": true,
    "textureGrid": [16, 20],
    "frameGap": [2, 2],
    "frameSize": [[1, 1]],
    "frames": [
      { "name": "Forest Short Plants", "variety": "Grass Single Blade A", "uv": [0, 0] },
      { "name": "Forest Short Plants", "variety": "Grass Double Blade", "uv": [18, 0] },
      { "name": "Forest Short Plants", "variety": "Grass Small Y", "uv": [36, 0] 
=== walls.json head ===
[
  { "id": 0, "name": "Sky", "key": "None", "color": "#00000000" },
  {
    "id": 1,
    "name": "Stone Wall",
    "key": "Stone",
    "color": "#353535FF",
    "blendType": 48
  },
  { "id": 2, "name": "Dirt Wall (natural)", "key": "DirtUnsafe", "color": "#573C30FF" },
  {
    "id": 3,
    "name": "Ebonstone Wall (natural)",
    "key": "EbonstoneUnsafe",
    "color": "#2F2935FF",
    "blendType": 48
  },
  { "id": 4, "name": "Wood Wall", "key": "Wood", "color": "#453225FF" },
  { "id": 5, "name": "Gray Brick Wall", "key": "GrayBrick", "color": "#3B3B3BFF" },
  { "id": 6, "
=== items.json head ===
[
  {
    "id": 1,
    "scale": 1,
    "maxStackSize": 9999,
    "isRackable": true,
    "name": "Iron Pickaxe",
    "key": "IronPickaxe",
    "rack": "True"
  },
  {
    "id": 2,
    "scale": 1,
    "maxStackSize": 9999,
    "name": "Dirt Block",
    "key": "DirtBlock",
    "createTile": 0
  },
  {
    "id": 3,
    "scale": 1,
    "maxStackSize": 9999,
    "name": "Stone Block",
    "key": "StoneBlock",
    "createTile": 1
  },
  {
    "id": 4,
    "scale": 1,
    "maxStackSize": 9999,
    "isRackable": true,
    "name": "Iron Broadsword",
    "key": "IronBroad
=== npcs.json head ===
[
  {
    "id": 17,
    "name": "Merchant",
    "key": "Merchant",
    "sourceRect": [0, 0, 40, 56],
    "canShimmer": true
  },
  {
    "id": 18,
    "name": "Nurse",
    "key": "Nurse",
    "sourceRect": [0, 0, 40, 56],
    "canShimmer": true
  },
  {
    "id": 19,
    "name": "Arms Dealer",
    "key": "ArmsDealer",
    "sourceRect": [0, 0, 40, 56],
    "canShimmer": true
  },
  {
    "id": 20,
    "name": "Dryad",
    "key": "Dryad",
    "sourceRect": [0, 0, 40, 56],
    "canShimmer": true
  },
  {
    "id": 22,
    "name": "Guide",
    "key": "Guide",
    "

```


---

## 🤖 Assistant · 2026-08-04T16:36:02.912Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have a comprehensive understanding. Let me also quickly check TileProperty.cs and how ReadString works (7-bit encoded length prefix) and check the version table (versions.json). Also check the section count difference and footer. Let me quickly peek at TileProperty.cs and versions.json, and the globalColors.json.

Actually I have enough. One more useful check: how ReadString works in TEdit (it's .NET BinaryReader.ReadString = 7-bit encoded length + UTF8 bytes). Important for TS implementation.

Let me check versions.json quickly and TileProperty.cs briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-04T16:36:03.465Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria && cat Data/versions.json | head -20 && echo \"=== TileProperty.cs ===\" && cat Objects/TileProperty.cs 2>/dev/null | head -80",
 "description": "Read versions.json and TileProperty.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-04T16:36:03.514Z

**📎 ToolResult**

```
{
  "gameVersionToSaveVersion": {
    "1.0": 38,
    "1.0.1": 2,
    "1.0.2": 3,
    "1.0.3": 4,
    "1.0.4": 9,
    "1.0.5": 12,
    "1.0.6": 20,
    "1.0.6.1": 22,
    "1.1": 36,
    "1.1.1": 37,
    "1.1.2": 39,
    "1.2": 67,
    "1.2.0.1": 68,
    "1.2.0.2": 69,
    "1.2.0.3": 70,
    "1.2.0.3.1": 71,
    "1.2.1": 72,
    "1.2.1.1": 73,
=== TileProperty.cs ===
﻿#nullable enable
using System.Linq;
using TEdit.Geometry;
using TEdit.Common;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace TEdit.Terraria.Objects;

/// <summary>
/// Axis for texture UV wrapping when tile variants exceed texture dimensions.
/// </summary>
public enum TextureWrapAxis
{
    None,   // No wrapping (default)
    U,      // Wrap on U-axis (horizontal) - most common
    V       // Wrap on V-axis (vertical) - e.g., lamps
}

/// <summary>
/// Rendering pipeline for tree-type tiles that need code-driven texture assembly.
/// </summary>
public enum TreeMode
{
    None,       // Standard frame-based rendering (default)
    Forest,     // Standard trees (tile 5) — tops, branches, trunks
    Palm,       // Palm trees (tile 323) — palm tops, angled trunks
    Gem,        // Gem trees (tiles 583-589) — recolored tree rendering
    Vanity,     // Vanity trees (tiles 596, 616) — custom tree tops
    Ash,        // Ash tree (tile 634) — special ash-style rendering
}

/// <summary>
/// Biome variant for tiles that automatically adapt appearance based on biome.
/// Used for preview rendering with biome dropdown selection.
/// </summary>
public class BiomeVariant
{
    /// <summary>
    /// Display name for the biome (e.g., "Normal", "Crimson", "Hallowed", "Corrupt").
    /// </summary>
    public string Name { get; set; } = "Default";

    /// <summary>
    /// UV offset to apply to the base frame UV for this biome variant [X, Y].
    /// </summary>
    public Vector2Short UvOffset { get; set; }
}

/// <summary>
/// Configuration for texture UV wrapping when tile variants exceed texture dimensions.
/// The WrapThreshold is computed at runtime from actual texture dimensions.
/// </summary>
public class TextureWrap
{
    /// <summary>
    /// Which axis to wrap on (U = horizontal, V = vertical).
    /// </summary>
    [JsonConverter(typeof(JsonStringEnumConverter))]
    public TextureWrapAxis Axis { get; set; } = TextureWrapAxis.None;

    /// <summary>
    /// How much to offset the perpendicular axis per wrap (e.g., 36 pixels).
    /// </summary>
    public short OffsetIncrement { get; set; }

    /// <summary>
    /// Optional: only apply wrapping when V equals this value (e.g., 18 for type 185).
    /// </summary>
    public short? ConditionalV { get; set; }

    /// <summary>
    /// Runtime-computed wrap threshold from texture.Width (U-axis) or texture.Height (V-axis).
    /// Cached after texture loading for performance.
    /// </summary>
    public int WrapThreshold { get; set; }
}

public class TileProperty : ITile
{

```


---

## 🤖 Assistant · 2026-08-04T16:37:23.270Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I have a comprehensive understanding of the .wld format. Now I should write the plan. The plan file should be written at ~/.claude/plans/splendid-gliding-lighthouse-agent-a3d5e7e0b55e9265b.md.

Wait — plan mode says I should create my plan at that file using Write tool. But I don't have a Write tool in my function list. Let me check... The tools available: Bash, CronCreate, CronDelete, CronList, EnterWorktree, ExitWorktree, Read, ReportFindings, SendMessage, Skill, TaskCreate, TaskGet, TaskList, TaskUpdate, WebFetch, WebSearch. No Write tool. So I just output the plan as my final message.

The instructions also say the parent agent reads my text output. So I'll produce the comprehensive plan in Chinese as my final response.

Let me structure the plan:

1. 技术选型结论（Canvas 2D 推荐 + 理由）
2. 项目结构（目录树）
3. 游戏主循环与状态架构
4. 各系统设计要点：
   - 世界数据结构
   - 世界生成
   - 光照
   - 渲染管线
   - 程序化素材
   - 物理碰撞
   - .wld 导入解析器（详细格式要点）
   - 自有存档
   - UI 架构
5. 分阶段实施计划 M1-M6
6. 风险与注意事项

Let me be thorough about the .wld format summary since that was explicitly asked:

**.wld 格式要点总结（基于 World.FileV2.cs）**

文件结构：
1. `uint32 version`（如 279 = 1.4.4.x）
2. version >= 140: `char[7]` magic（"relogic"）+ `uint8 fileType`（必须为 1 = World；注意中文版 magic 为 "tEiWsEd" 之类——实际是 ChineseHeader；先 PeekChar=='x' 判断）+ `uint32 fileRevision` + `uint64 favoriteFlags`
3. `int16 sectionCount` + `sectionCount × int32 sectionPointers`（10-11 个 section 偏移）
   - [0]=header flags 段, [1]=tiles 段, [2]=chests, [3]=signs, [4]=NPCs, [5]=tile entities, [6]=pressure plates, [7]=town manager, [8]=bestiary, [9]=creative powers
   - sectionCount>=11 时 (version>=210) 有 tile entities 之后的段
4. tileFrameImportant 位图：`int16 len` + ceil(len/8) 字节位打包（MSB first）
5. header flags 段（version 门控字段流）
6. tiles 段（RLE）
7. chests / signs / npcs / tile entities
8. footer: `bool true` + string title + int32 worldId

Header flags 关键字段（所有 version）: title(string), seed, worldId(int32), left/right/top/bottom(int32), tilesHigh, tilesWide(int32), gameMode, creationTime(int64), moonType(byte), treeX[3], treeStyle[4], caveBackX[3], caveBackStyle[4], spawnX/Y, groundLevel(double), rockLevel(double), time(double), dayTime(bool), moonPhase, bloodMoon, isEclipse, dungeonX/Y, isCrimson, downed boss flags... 后续大量 version 门控字段。对于导入用途，只需精确读取流位置，忽略不关心的字段。

Tiles 段（LoadTiles 核心）：
- 列优先遍历（x 外层，y 内层），逐 tile 读取直到填满 maxX*maxY
- 每 tile：header1 byte
  - bit0 (0x01): 存在 header2
  - bit1 (0x02): tile active
  - bit2 (0x04): 存在 wall（wall byte 跟在后面）
  - bit3-4 (0x18)>>3: liquid type（1=water 2=lava 3=honey；1.4.4+ header3 bit7 → shimmer）
  - bit5 (0x20): tile type 为 int16 LE（否则为 byte）
  - bit6-7 (0xC0)>>6: RLE 存储类型：0=无RLE, 1=RLE 计数 byte, 2=RLE 计数 int16, 3=按 int16 处理
- header2 存在时（header2 bit0 → header3）:
  - bit1: red wire, bit2: blue wire, bit3: green wire, bit4-6: brickStyle (slope), bit7: 未用？(实际 bit7 是 'has header3' ... 不，header2 bit0=header3 存在)
- header3: bit0 → header4 (v269+), bit1: actuator, bit2: inactive (actuated off), bit3: tile color byte, bit4: wall color byte, bit5: yellow wire, bit6: wall 高字节 (v222+, wall 变为 ushort), bit7: shimmer
- header4 (v269+): bit1 invisible block, bit2 invisible wall, bit3 fullbright block, bit4 fullbright wall
- tile active 时: type（byte 或 int16 LE），若 tileFrameImportant[type]（或 type 超出数组则视为 framed）→ int16 U + int16 V；header3 bit3 → TileColor byte
- wall 存在时: wall byte；header3 bit6 → wall 高字节；header3 bit4 → WallColor byte
- liquid 存在时: liquidAmount byte
- RLE 计数 N 表示当前 tile 向下（同列 y+1..y+N）重复 N 次（额外重复次数，即该 tile 占 N+1 格）
- tileFrameImportant 机制：只有标记为 framed 的 tile 类型才在流中写 UV 坐标（多格物体如桌子、宝箱、树）；非 framed 的 1x1 方块不写 UV 节省空间。解析时必须先读位图才能正确对齐流。

字符串编码：.NET BinaryReader.ReadString → 7-bit varint 长度前缀 + UTF-8。

double 是 8 字节 LE IEEE754；float 4 字节。

Chests 段: int16 totalChests；v<294 再读 int16 maxItems；每个：int32 x, int32 y, string name, (v>=294) int32 maxItems, 然后 maxItems 个 slot：int16 stack，若 >0 再读 int32 itemId + byte prefix。

Signs: int16 total；每个 string text + int32 x + int32 y。

NPCs: v>=268 先 int32 shimmeredCount + int32 数组；然后 bool 循环直到 false：每个 town NPC：int32 spriteId (v>=190), string displayName, float x, float y, bool isHomeless, int32 homeX, int32 homeY, (v>=213) byte flag + 可能 int32 variation, (v>=315) bool homelessDespawn；之后 mobs：bool 循环：int32 spriteId, float x, float y。

Tile entities (v>=210): int32 count；每个按类型解析。

Footer: bool(true) + string title + int32 worldId。

Version 差异要点：支持 1.4.x（version ~279）为主，最低支持 ~1.4.0.5（230）。关键 version 门槛：140（section 头）、179/181（seed/GUID）、190（npc id）、209（gameMode）、210（tile entities section）、213、222（wall ushort、世界 flag booleans）、267/268/269（zenith/shimmer/header4）、294+（chest maxItems per chest）、302、315。

建议 TS 实现：主攻 1.4.4（version 279-327），对低版本用 version 门控跳过字段；或者干脆限定"仅支持 version >= 210 (1.4.0.5+)"，减少分支。

现在设计各系统。

**技术栈决定：Canvas 2D**
理由：
- 程序化生成 sprite 天然是逐像素操作 → 需要频繁 ImageData put；Canvas 2D + OffscreenCanvas + drawImage 复制足够
- Tile-based 渲染每帧 drawImage 几千次，Canvas 2D 在现代浏览器性能足够（配合 chunk 缓存：把静态 tile 区域预渲染到离屏 canvas，只 drawImage chunk）
- WebGL 优势在全屏后处理/光照贴图混合，但光照可以用一个低分辨率 canvas 放大叠加（multiply/overlay 合成），不需要 shader
- 开发效率高，避免着色器/资源管线复杂度
- 可留抽象层（Renderer 接口），后期如需可换 WebGL

关键性能设计：chunk 化静态渲染缓存（16x16 tile 一个离屏 canvas，脏标记重绘），光照低分辨率 buffer（1 tile = 1 像素，再放大 16x 用 smoothing 双线性，或 2x2 采样）。

**世界数据结构**
Uint8Array 多通道 SoA（structure of arrays），比对象数组省内存且快：
- tiles: width*height 的若干平面
  - tileType: Uint16Array（640+ 类型上限，wld 用 ushort）
  - tileFlags: Uint8Array（active、slope、actuator... 打包位）
  - frameX, frameY: Uint16Array（可为空/懒分配，因为多数 tile 非 framed——或者干脆每 tile 都有，4200*1200*2*2 = 20MB，可以接受；更省：只存 type+flags，framed tile 存 frame 在独立 Map？太复杂。推荐：frameX/frameY 用 Uint16Array 全量分配，简单且够快）
  - wallType: Uint8Array（1.4 用 ushort 但实际 <256 的常用；为兼容 wld 用 Uint16Array）
  - liquid: Uint8Array（高4位 type 低4位 amount 或分开两个）
  - light（光照缓存）: 分层 wallLight/tileLight 或合并
  - color/paint: 可省略或 Uint8Array
- 4200x1200 = 5.04M tiles
  - type u16 = 10MB, frameX/Y u16 = 20MB, wall u16 = 10MB, flags u8 = 5MB, liquid u8 = 5MB, light u8x3 = 15MB
  - 总计 ~65MB，可接受；若要省，wall 用 u8（只支持 id<256）
- 索引 idx = y * width + x（行优先，对按行扫描光照/渲染更友好）
- 碰撞/光照查询直接平面数组访问，无指针追踪
- 推荐：索引 y*width+x；TEdit 是 x 外层但那是文件遍历顺序，内存布局自由

**实体系统**：简单类继承 + 组件混合。推荐不用完整 ECS（archetype 查询的收益在本项目不明显，徒增复杂度），用：
- abstract Entity { id, pos, vel, size(aabb), update(dt), draw(ctx), type }
- 子类：Player, ItemDrop, Enemy(Slime/Zombie/DemonEye/EoC), Projectile, NPC(Town), Particle, DamageNumber
- EntityManager 数组分类桶 + 空间网格（SpatialHash，cell 16x16 tile）用于碰撞查询和敌人生成查询

**主循环**
- requestAnimationFrame；accumulator 固定步长物理 1/60（GAME_TICK=1000/60），渲染插值可选（先不做插值，直接渲染最新状态）
- Game 状态机：Boot → MainMenu → WorldGen → Playing → Paused
- 场景：world 单例 + entities；UI 状态独立

**光照**
- BFS/优先队列传播：光强 0-255（u8）
- 三层：skyLight（天空列预计算：从每列顶部向下直到第一个不透明 tile，以上为全亮；传播衰减 0）、tileLight（彩色光源，RGB 三通道或单通道+色调？推荐单通道强度 + 光源颜色单独调色：存 R,G,B 三个 Uint8Array 平面）
- 衰减：空气/非实心衰减 ~5%/格，实心 tile 衰减大（~15%），不同 tile 不透明度表
- 计算范围：只算可视区域 + 边距（如 viewport + 40 tile），玩家移动时增量重算；光源变化（放置火把）时标记局部脏矩形重算
- 实现：从光源和天空亮块做 BFS（队列，按强度降序处理——用 bucket queue 256 个桶避免排序）
- 缓存：每帧只重算 dirty 区域；光源列表缓存

**渲染管线**
- 相机 Camera { x, y (像素), zoom(固定 2x 或缩放), viewport }
- 视锥剔除：只遍历可视 tile 范围
- 静态 chunk 缓存：ChunkCache 16x16 tiles → OffscreenCanvas 256x256 px（16px tile），dirty 标记，瓦片变化时只重绘该 chunk（和相邻 chunk 若在边缘融合）
- 渲染顺序：sky background（渐变+太阳月亮+星星，视差云） → wall 层（从 chunk 分离 or 同 canvas 先画 wall 后 tile） → tile 层 → liquid → entity（按 y 排序） → 光照遮罩 → weather/particles → UI
  - chunk 离屏 canvas 内含 wall+tile；光照用独立低分辨率 canvas 叠加（globalCompositeOperation 'multiply'）
- tile 边缘融合（merge）：4-bit 邻接掩码（上下左右是否同类）→ 选 47 种变体中对应 frame；程序化生成时预生成每种 tile 类型的 merge sheet
- minimap：低分辨率，1 tile = 1px，用 tile 颜色表（TEdit tiles.json color 可参考）预渲染到离屏 canvas，定期（每 N tick）只更新变化区域

**程序化素材**
- 运行时生成 sprite sheet：AssetGen 模块
- 每种 tile：base 调色板（3-5 色）+ 值噪声抖动 + 边缘变暗/高光 → 16x16 基础贴图；再生成 merge 变体（47 blend mask）
- 洗牌：用 seeded RNG（mulberry32/xorshift），世界种子无关的固定种子保证全局一致
- 草：顶部边缘绿色覆盖层变体
- 矿石：石底 + 矿物斑点簇（几个随机 blob 用金属色）
- 树：程序画（树干段 tile + 树冠 blob），叶子用噪声剪影
- 物品图标：16x16，矿石→宝石形、锭→梯形、工具→柄+头像素画（用参数化：镐头弧线、斧刃、剑刃）——可用小型像素图模板（字符串数组像素图）+ 调色板替换，这在代码里原创且高效
- 角色/敌人动画帧：骨架化参数绘制（身体盒、头、四肢），帧=四肢相位偏移； slime = 果冻 blob squash & stretch；生成 4-6 帧行走循环
- 存储为 ImageBitmap / HTMLCanvasElement，索引访问

**物理**
- 分轴 AABB：先 x 移动 → 解析与 tile 网格碰撞（扫描 AABB 覆盖的 tile cell，实心则推回并置 vx=0），再 y 同理；落地检测 onGround
- tile 尺寸 16px，玩家 20x42 px（缩放 2x 后 40x84 屏幕像素）
- 液体：浮力简化、游泳
- 掉落物：简单重力 + 地面停留 + 磁吸

**.wld 解析器设计**（上面已总结格式）— 给出模块文件与函数签名

**自有存档 JSON**
- 格式：{ version, seed, header{...}, tiles: { RLE 编码的自定义紧凑格式 或 base64 的二进制段 } }
- 建议：JSON 外壳 + tiles 二进制段（自定义 RLE，格式：[varint count][tile struct]）转 base64，体积小、解析快；实体（宝箱、NPC、敌人生成状态）用 JSON 明文
- 或者纯 JSON 但 tile 用行 RLE 数组。给出推荐：混合式

**UI**
- DOM overlay 用于：主菜单、设置、物品栏/快捷栏、合成面板、宝箱面板、tooltip —— DOM 更好做布局、文字、hover、可访问性
- Canvas 自绘用于：HUD 内嵌元素（血条心形、小地图、buff 图标）、伤害数字、 Boss 血条
- 推荐：HUD 背板 DOM + 关键动态元素 canvas；用极简状态驱动（每个 UI 组件一个 update() 函数 + data 对象，不引入 React/Vue；手写 20 行的微型 store）

**分阶段 M1-M6** 每个里程碑列文件与验收标准。

**风险**：
- 光照性能（全图遍历）—— 用局部重算
- wld 版本碎片化 —— 限定支持 1.4.4，版本门控表
- 程序化素材观感 —— 像素模板 + 调色板，迭代成本低
- 版权：只用 TEdit 数据表中的 id/颜色/名称等事实性数据，不拷贝其代码逻辑/贴图；注意 Terraria 本身名称/数字是否可用——id、颜色值属事实数据，风险低；游戏名避免使用 "Terraria" 商标
- liquid 元胞自动机性能 —— 限制更新区域（仅可视区+活跃区）
- 浮点/固定步长在低帧率下的螺旋死亡 —— clamp accumulator

我需要给出具体的文件名与函数签名。让我认真组织目录树：

```
sandbox-world/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── public/
├── src/
│   ├── main.ts                 // 入口：启动 Game
│   ├── core/
│   │   ├── Game.ts             // class Game { loop, states }
│   │   ├── StateMachine.ts
│   │   ├── Input.ts            // class InputManager { keys, mouse, worldPos }
│   │   ├── Time.ts             // 固定步长 accumulator
│   │   ├── EventBus.ts
│   │   └── rng.ts              // mulberry32, hash2
│   ├── world/
│   │   ├── World.ts            // class World { getTile, setTile, ... }
│   │   ├── TileStore.ts        // SoA 平面数组
│   │   ├── TileDefs.ts         // 内部 tile/wall 注册表（id、属性、硬度、光照）
│   │   ├── gen/
│   │   │   ├── WorldGen.ts     // generate(seed, config): World 管线
│   │   │   ├── TerrainPass.ts  // 1D 高度图 + 分层
│   │   │   ├── CavePass.ts     // 2D 噪声阈值挖空 + 蠕虫隧道
│   │   │   ├── OrePass.ts
│   │   │   ├── SurfacePass.ts  // 草、树、装饰
│   │   │   ├── LiquidPass.ts   // 湖泊
│   │   │   └── StructurePass.ts // 小屋/宝箱
│   │   └── liquid/
│   │       └── LiquidSim.ts    // 元胞自动机
│   ├── lighting/
│   │   ├── LightingEngine.ts   // BFS 传播
│   │   ├── LightRegion.ts      // 区域管理/脏标记
│   │   └── SkyLight.ts
│   ├── physics/
│   │   ├── AABB.ts
│   │   ├── TileCollision.ts    // moveAndCollide(entity, dt)
│   │   └── SpatialHash.ts
│   ├── entities/
│   │   ├── Entity.ts
│   │   ├── EntityManager.ts
│   │   ├── Player.ts
│   │   ├── ItemDrop.ts
│   │   ├── enemies/ (Slime.ts, Zombie.ts, DemonEye.ts, EyeOfCthulhu.ts, EnemyAI.ts)
│   │   ├── TownNPC.ts
│   │   ├── Projectile.ts
│   │   └── Spawner.ts          // 敌人生成规则
│   ├── combat/
│   │   ├── Damage.ts           // 伤害计算/防御/击退
│   │   └── Drops.ts            // 掉落表
│   ├── items/
│   │   ├── ItemDefs.ts
│   │   ├── ItemStack.ts
│   │   ├── Inventory.ts
│   │   └── Crafting.ts         // 配方表 + 合成站过滤
│   ├── render/
│   │   ├── Renderer.ts         // Canvas2D 渲染器接口
│   │   ├── Camera.ts
│   │   ├── ChunkCache.ts
│   │   ├── TileRenderer.ts     // merge 掩码、变体
│   │   ├── SkyRenderer.ts      // 昼夜渐变、太阳月亮
│   │   ├── LightCompositor.ts
│   │   ├── Minimap.ts
│   │   └── ParticleSystem.ts
│   ├── assets/
│   │   ├── AssetGen.ts         // 入口：buildAll() 生成全部 sheet
│   │   ├── Palette.ts          // 调色板（参考 TEdit 颜色）
│   │   ├── TileSheet.ts
│   │   ├── ItemIcons.ts
│   │   ├── CharacterSprites.ts
│   │   └── PixelTemplate.ts    // 字符串像素图模板 + palette swap
│   ├── wld/
│   │   ├── WldReader.ts        // BinaryReader + 入口 parse(buffer)
│   │   ├── WldSections.ts      // section header/pointers/frameImportant
│   │   ├── WldHeader.ts        // header flags 流
│   │   ├── WldTiles.ts         // RLE tile 解码
│   │   ├── WldEntities.ts      // chests/signs/npcs/tile entities
│   │   ├── WldMapping.ts       // wld id → 内部 tile id 映射表
│   │   └── BinaryReaderLE.ts
│   ├── save/
│   │   ├── SaveFile.ts         // 自有 JSON 格式读写
│   │   └── TileRLE.ts          // 自定义紧凑编码
│   ├── ui/
│   │   ├── ui.css
│   │   ├── Hud.ts              // canvas HUD（血量、小地图）
│   │   ├── Hotbar.ts           // DOM
│   │   ├── InventoryPanel.ts
│   │   ├── CraftingPanel.ts
│   │   ├── ChestPanel.ts
│   │   ├── Tooltip.ts
│   │   └── MainMenu.ts
│   ├── time/
│   │   └── Clock.ts            // 昼夜循环
│   └── data/                   // 静态数据表（内部 tile/item/npc/recipe 注册）
│       ├── tiles.ts
│       ├── walls.ts
│       ├── items.ts
│       ├── npcs.ts
│       └── recipes.ts
```

依赖：vite, typescript, simplex-noise（或自实现），无其他。jest/vitest 用于 wld 解析器与 RLE 的单元测试。

现在写函数签名级别细节。

TileStore:
```ts
class TileStore {
  readonly w: number; readonly h: number;
  tileType: Uint16Array; tileFlags: Uint8Array;
  frameX: Uint16Array; frameY: Uint16Array;
  wall: Uint16Array; liquid: Uint8Array; liquidType: Uint8Array;
  constructor(w, h)
  idx(x, y): number
  get(x,y): TileView (或解构访问)
  isActive(x,y): boolean
  setTile(x, y, type, frameX?, frameY?)
  isSolid(x, y): boolean   // 查 TileDefs + slope
  cloneRegion / fillRect
}
```

flags 位定义：bit0 active, bit1-2 slope(需2位不够 → brickStyle 3位)，让我定：bit0 active, bit1 actuator, bit2 actuatedOff, bit3-5 brickStyle(3位), bit6 important/framed, bit7 reserved。或者把 brickStyle 放独立数组。简化：flags: bit0 active, bit1 actuator, bit2 inactive, bit3..5 slope。

Lighting:
```ts
class LightingEngine {
  updateRegion(world, rect: Rect, sources: LightSource[]): void   // BFS
  lightAt(x,y): [r,g,b]  // 或访问 planes
  markDirty(x, y, radius)
}
```

Physics:
```ts
function moveAndCollide(body: Body, world: World, dt: number): CollisionResult
// body: {x,y,w,h,vx,vy,onGround,...}
// 分轴：先 x += vx*dt，扫描覆盖 cells，遇 solid 推回；再 y
```

Wld:
```ts
class BinaryReaderLE {
  constructor(buf: ArrayBuffer)
  readUInt32/Int32/Int16/UInt16/Int64(as bigint)/Single/Double/Boolean/Byte
  readString7Bit(): string  // .NET BinaryReader.ReadString
  readBitArray(): Uint8Array
}
parseWld(buf: ArrayBuffer): WldWorld
// WldWorld { version, header: WldHeader, tiles: WldTilePlane, chests, signs, npcs, tileEntities }
```

RLE 解码循环伪代码描述。

验收标准每里程碑。

字数控制：这是一个大方案，用户要求非常详细。我会写长一些，但组织清晰。目标 500-700 行中文。

关于 tileFrameImportant 详细位打包：ReadBitArray: int16 length = bit 数；然后每 8 bit 一字节，MSB 在前。

还要注意 sectionPointers 数量：version >= 210 → 11 个（含 bestiary/creative? 让我确认：SaveSectionHeader 写 GetSectionCount。加载时 sectionCount 从文件读。v1.4.4 是 11? TEdit 代码 sectionPointers[8]=bestiary, [9]=creative, [10]=? 看 Load：sectionPointers[6] pressure plate? 让我看 load 流程 1450-1500：

```
LoadNPCsData (sectionPointers[4]?)
```
从 line 1446: `if (b.BaseStream.Position != sectionPointers[3]) → chest?` 让我重新看 save 顺序：
- [0] SaveHeaderFlags
- [1] SaveTiles
- [2] SaveChests
- [3] SaveSigns
- [4] SaveNPCs
- [5] SaveTileEntities
- [6] SavePressurePlate
- [7] SaveTownManager
- [8] SaveBestiary
- [9] SaveCreativePowers

等一下，save 代码里 sectionPointers[0] = SaveSectionHeader（section header 自身），[1] = SaveHeaderFlags，[2] = SaveTiles，[3] = SaveChests，[4] = SaveSigns，[5] = SaveNPCs，[6] = SaveTileEntities，[7] = SavePressurePlate，[8] = SaveTownManager，[9] = SaveBestiary，[10] = SaveCreativePowers。因为 sectionPointers[0] 是 section header 自身结束位置。

而 load 时 line 56: `if (b.BaseStream.Position != sectionPointers[0]) b.BaseStream.Position = sectionPointers[0]; LoadHeaderFlags(b, w, sectionPointers[1]);` — 即 [0]=header flags 起点（section header 之后），[1]=tiles 起点，[2]=chests, [3]=signs, [4]=npcs, [5]=tile entities, [6]=pressure plates, [7]=town manager, [8]=bestiary, [9]=creative powers。共 10 个（v<210 是 9 个：0-8 即 pressure plates 最后）。好，与我的总结一致。

另外 version >= 210 时 sectionCount > 9 → 跳到 sectionPointers[8] 读 tile entities？line 64-69:
```
if (w.Version >= 210 && sectionPointers.Length > 9) {
    b.BaseStream.Position = sectionPointers[8];
    LoadTileEntities(b, w);
    if (b.BaseStream.Position != sectionPointers[9])...
```
嗯这看起来有点奇怪（TEdit 用 [8] 作为 tile entities？）可能这是他们修复某些文件的 hack。实际标准：tiles section 之后顺序是 chests、signs、npcs、tile entities。加载顺序在 load 主流程 1417-1460 顺序读取即可（文件本身就是顺序的）。我在方案中说明按顺序读取即可，section pointers 用于校验/容错。

行，我有足够信息。还有 header flags 后半部分（2188 之后还有很多字段直到 2499），我在方案中说明"字段清单长，用版本门控的顺序读取表生成"，并给出 TS 实现策略：将 LoadHeaderFlags 的字段序列转录为描述表（field descriptor list），驱动式读取，跳过不关心字段——这样避免遗漏导致流错位。

开始写最终方案。结构：

# 泰拉瑞亚复刻（SandboxWorld）实现方案

## 0. 总体技术决策
## 1. .wld 格式技术要点（解析参考）
## 2. 项目结构
## 3. 游戏主循环与状态架构
## 4. 系统设计
  4.1 世界数据
  4.2 世界生成
  4.3 光照
  4.4 渲染管线
  4.5 程序化素材
  4.6 物理碰撞
  4.7 .wld 解析器
  4.8 自有存档
  4.9 UI
## 5. 里程碑 M1-M6
## 6. 风险
### Critical Files

Let me write it now. Also per plan mode instructions I should write the plan file... but I don't have Write. The final message serves as the plan. I'll just deliver it as text.
````

</details>


---

## 🤖 Assistant · 2026-08-04T16:39:32.690Z · glm-x-preview-260804

````
我已仔细阅读了 TEdit 的 `World.FileV2.cs`（重点 `LoadTiles`/`DeserializeTileData` 的 RLE 编码）、`Tile.cs`、`LoadSectionHeader`、`LoadHeaderFlags`、`LoadChests`、`LoadNPCsData`、`LoadFooter` 以及 `Data/*.json` 数据表结构。以下是完整实现方案。

---

# Terraria 复刻游戏（SandboxWorld）实现方案

## 0. 总体技术决策

**渲染：推荐 Canvas 2D**，理由：

1. 本项目素材全部程序化生成，生成过程是逐像素 `ImageData` 操作，产物是小尺寸 tile sheet，Canvas 2D 的 `drawImage` + 离屏 `OffscreenCanvas` 缓存完全够用；
2. 渲染主体是 tile 网格，配合 **chunk 级静态缓存**（每 chunk 16×16 tile 预渲染成离屏画布）后，每帧实际只剩几十次 `drawImage` + 实体绘制，Canvas 2D 无性能瓶颈；
3. 光照不需要 shader——用一张 **1 tile = 1 像素的低分辨率光照画布**放大 16 倍并以 `multiply` 混合叠加即可，双线性插值还免费得到光照的柔和渐变；
4. WebGL 的收益（大规模粒子、全屏后处理）不在本项目功能范围内，引入 GL 资源管线和着色器维护成本不值。

保留一层 `IRenderer` 抽象（本方案中 `render/Renderer.ts`），未来如需换 WebGL 只替换实现。

**UI：DOM overlay 为主 + Canvas 自绘 HUD 为辅**（详见 4.9）。

**依赖**：`vite`、`typescript`、`simplex-noise`（也可自实现，约 100 行）、`vitest`（仅测试 wld 解析与 RLE）。**无框架、无 React**。

---

## 1. `.wld` 格式技术要点（供 TS 解析器参考，基于 World.FileV2.cs 实测）

### 1.1 整体文件布局（顺序流 + section 偏移表）

```
uint32  version                      // 如 279 ≈ 1.4.4.x，见 Data/versions.json
-- version >= 140 时：
char[7] headerFormat                 // "relogic"（中文版为另一常量，先 PeekChar=='x' 判断）
uint8   fileType                     // 必须 == 1 (World)
uint32  fileRevision
uint64  favoriteFlags                // bit0 = isFavorite
int16   sectionCount                 // 1.4.x 为 10；v>=210 才有 tileEntities 段
int32[] sectionPointers              // [0]=headerFlags 起点 [1]=tiles [2]=chests [3]=signs
                                    // [4]=npcs [5]=tileEntities [6]=pressurePlates
                                    // [7]=townManager [8]=bestiary [9]=creativePowers
int16   frameImportantBitCount
byte[]  tileFrameImportant           // 位打包，MSB 在前，ceil(count/8) 字节
-- 之后按 sectionPointers[0] 开始顺序读 headerFlags → tiles → chests → signs → npcs → ... → footer
```

注意：sectionPointers[0] 指向的是 **header flags 段**（section header 自身结束后）；TEdit 加载时严格用 `position != sectionPointers[i]` 做容错跳转，TS 版同样应在每段开始前 `seek` 到指针位置，这样即使某版本字段读错位也能自愈。

### 1.2 header flags 段（`LoadHeaderFlags`）

按 version 门控的顺序字段流，核心字段（**全部要读，否则流错位**）：

```
string  title                        // .NET BinaryReader.ReadString：7-bit varint 长度 + UTF-8
[string seed, uint64 worldGenVersionVer]  // v>=179
[guid 16 bytes]                      // v>=181
int32   worldId
int32   leftWorld / rightWorld / topWorld / bottomWorld
int32   tilesHigh / tilesWide
int32   gameMode                     // v>=209；v208 为 bool；v112~207 为 bool
int64   creationTime                 // v>=141
byte    moonType
int32   treeX[3], treeStyle[4], caveBackX[3], caveBackStyle[4]
int32   iceBackStyle / jungleBackStyle / hellBackStyle
int32   spawnX / spawnY
double  groundLevel / rockLevel / time
bool    dayTime;  int32 moonPhase;  bool bloodMoon / isEclipse
int32   dungeonX / dungeonY;  bool isCrimson
bool    downedBoss1..downedPlantBoss, [v>=118 downedSlimeKing]
bool    savedGoblin/savedWizard/savedMech/downedGoblins/downedClown/downedFrost/downedPirates
bool    shadowOrbSmashed / spawnMeteor;  byte shadowOrbCount;  int32 altarCount;  bool hardMode
[v>=257 partyOfDoom]  int32 invasionDelay/Size/Type; double invasionX
[v>=118 double slimeRainTime] [v>=113 byte sundialCooldown]
bool    isRaining; int32 tempRainTime; float tempMaxRain
int32   savedOreTiers ×3;  byte bgTree/BgCorruption/BgJungle/BgSnow/BgHallow/BgCrimson/BgDesert/BgOcean
int32   cloudBgActive; int16 numClouds; float windSpeedSet
-- v>=95: int32 anglerCount + string[]；v>=99 起继续大量门控字段（angler/sundial/banners/
-- 全部 boss 击杀标记/时刻表/天气…直到 v>=327 附近结束）
```

字段非常多且全部 version 门控。**TS 实现策略**：不要手写一长串 if-else，而是把字段序列转录成 `HeaderFieldSpec[]` 描述表（`{ name, type, minVersion, optional }`），用驱动式读取器顺序消费。不关心的字段也必须读掉（丢弃即可）以保证流位置正确。

### 1.3 tiles 段（`LoadTiles`，本项目核心）—— RLE 编码

- 遍历顺序为**列优先**（x 外层 0..maxX，y 内层 0..maxY），逐 tile 解码直到填满 `tilesWide × tilesHigh`。
- 每个 tile 从一个 `header1` 字节开始，**位标志定义**：

| header1 位 | 含义 |
|---|---|
| bit0 (0x01) | 存在 header2 |
| bit1 (0x02) | tile active（本格有方块） |
| bit2 (0x04) | 存在 wall（后跟 wall 字节） |
| bit3-4 (0x18)>>3 | liquid 类型：1=水 2=岩浆 3=蜂蜜（1.4.4+ header3.bit7 → 微光 shimmer） |
| bit5 (0x20) | tile type 用 **int16 LE** 编码（否则为单字节） |
| bit6-7 (0xC0)>>6 | **RLE 存储类型**：0=无 RLE；1=后跟 1 字节重复计数；2=后跟 int16 计数；3=按 int16 处理 |

| header2 位（存在时） | 含义 |
|---|---|
| bit0 | 存在 header3 |
| bit1 / bit2 / bit3 | 红线 / 蓝线 / 绿线 |
| bit4-6 >>4 | BrickStyle（半砖斜坡：0=无 1=半砖 2=右斜 3=左斜 4=左下斜…） |

| header3 位（存在时） | 含义 |
|---|---|
| bit0 | 存在 header4（仅 v>=269） |
| bit1 | actuator（制动器） |
| bit2 | inactive（被制动器关掉的方块） |
| bit3 | 后跟 TileColor（油漆）字节 |
| bit4 | 后跟 WallColor 字节 |
| bit5 | 黄线 |
| bit6 | wall 需再读 1 字节作高 8 位（v>=222，wall 实为 ushort） |
| bit7 | 液体是 shimmer（v>=269） |

| header4 位（v>=269 且存在时） | bit1=invisibleBlock bit2=invisibleWall bit3=fullBrightBlock bit4=fullBrightWall |

- 字段读取顺序（在 header 链之后）：`tileType`（active 时）→ `frameU(int16)+frameV(int16)`（**仅当 tileFrameImportant[tileType]**，见 1.4）→ `tileColor`（header3.bit3）→ `wall` → `wallColor` → `liquidAmount(1 byte)` → `RLE 计数`。
- **RLE 语义**：计数 N 表示该 tile 向下（同列 y+1 … y+N）再重复 N 次，即该条目共占 N+1 格；`tiles[x, y..y+N] = tile`。注意 TEdit 源码里 RLE 计数是在**所有数据读完后**才读的（`DeserializeTileData` 末尾），TS 解码顺序必须一致。
- wires/actuator/slope 对本项目无用但必须消费；`BrickStyle` 决定斜坡碰撞，导入时可忽略斜坡（按实心处理）以简化。

### 1.4 tileFrameImportant 机制（关键对齐点）

- 该位图标记哪些 tile 类型是“多格框架物体”（桌子、门、宝箱、树、火把…）。**只有 framed 类型的 active tile 在流中写 U/V 坐标**（int16 各一，单位像素偏移）；非 framed 的 1×1 方块不写 UV。
- 因此必须**先读位图才能开始解 tiles 段**，否则流立刻错位。
- 超出位图长度的 type 按 framed 处理（TEdit: `tileType < len ? arr[tileType] : true`）。
- 树等超规格物体 U/V 可能很大且有 wrapping 规则（见 TileProperty.cs 的 `TextureWrap`/`TreeMode`），本项目导入时只保留 U/V 原值，渲染时对已知类型映射，未知类型退化为 1×1 色块。

### 1.5 chests / signs / npcs / tileEntities / footer

```
chests:  int16 total; [v<294: int16 maxItems]
         每个: int32 x, int32 y, string name, [v>=294: int32 maxItems]
               maxItems × (int16 stack; stack>0 → int32 itemId + byte prefix)
signs:   int16 total; 每个: string text, int32 x, int32 y
npcs:    [v>=268: int32 shimmeredCount + int32[count]]
         bool 循环读 town NPC 直到 false:
           int32 spriteId(v>=190，否则 string name), string displayName,
           float x, float y, bool isHomeless, int32 homeX, int32 homeY,
           [v>=213: byte flag，bit0 时 int32 variationIndex] [v>=315: bool]
         之后 bool 循环读 mobs: int32 spriteId, float x, float y
tileEntities (v>=210): int32 count; 每个按 type 分支解析（本方案只需读取并跳过/丢弃）
footer:  bool(必须 true) + string title + int32 worldId（双重校验）
```

### 1.6 基础类型与字符串

- 全部小端。`double` 8 字节、`float` 4 字节、`bool` 1 字节、`string` = 7-bit varint 长度前缀 + UTF-8 字节（.NET `BinaryReader.ReadString`）。
- **版本支持范围建议**：只支持 **version ≥ 210（1.4.0.5）**，主攻 1.4.4（279+）。低版本 header flags 门控分支过多，收益低。用 `Data/versions.json` 做版本号↔游戏版本映射显示给用户。

### 1.7 数据表参考方式（版权约束）

`tiles.json`/`walls.json`（id、name、color、canBlend、mergeWith、textureGrid、frameSize）、`items.json`（id、name、createTile、maxStackSize）、`npcs.json`（id、name）只作**事实性参考**：提取「id → 名称 → 地图色」映射到本方案自有数据表（`src/data/*.ts`）中，并重新组织字段（硬度、光照、工具归属等全部自己定义）。不复制 TEdit 的渲染/合并算法实现代码。

---

## 2. 项目结构

```
~/Project/GLM/SandboxWorld/game/
├── index.html
├── package.json / tsconfig.json / vite.config.ts
├── src/
│   ├── main.ts                      // 创建 Game 并启动
│   ├── core/
│   │   ├── Game.ts                  // 拥有 states/input/renderer/clock
│   │   ├── GameState.ts             // 状态机：Boot|Menu|WorldGen|Playing|Paused
│   │   ├── Input.ts                 // class InputManager（键盘/鼠标，含 worldPos 换算）
│   │   ├── FixedLoop.ts             // accumulator 固定步长，防螺旋死亡
│   │   ├── EventBus.ts
│   │   └── rng.ts                   // mulberry32 / hash2(x,y,seed)（世界生成确定性）
│   ├── world/
│   │   ├── World.ts                 // 门面：封装 TileStore + 尺寸 + spawn + 时间
│   │   ├── TileStore.ts             // SoA 多通道平面数组（见 4.1）
│   │   ├── TileDefs.ts              // 内部 tile 注册表（含由 wld 映射而来的条目）
│   │   ├── WallDefs.ts
│   │   ├── gen/
│   │   │   ├── WorldGen.ts          // generate(seed, GenConfig): World（管线编排）
│   │   │   ├── TerrainPass.ts       // 地表高度图 + 表土/石层分界
│   │   │   ├── CavePass.ts          // 噪声挖空 + 蠕虫隧道 + 大洞厅
│   │   │   ├── OrePass.ts           // 铜铁银金 + 深度分层
│   │   │   ├── SurfacePass.ts       // 草皮、树、灌木装饰
│   │   │   ├── LiquidPass.ts        // 地表湖 + 地下静水
│   │   │   └── StructurePass.ts     // 地下小屋（可选开关）+ 宝箱预埋
│   │   └── liquid/LiquidSim.ts      // 元胞自动机
│   ├── lighting/
│   │   ├── LightingEngine.ts        // BFS 衰减传播（三通道 RGB）
│   │   ├── SkyLightColumn.ts        // 天空光列缓存
│   │   └── LightDirtyTracker.ts     // 脏矩形
│   ├── physics/
│   │   ├── AABB.ts                  // interface Body { x,y,w,h,vx,vy,... }
│   │   ├── TileCollision.ts         // moveAndCollide(body, world, dt)
│   │   └── SpatialHash.ts           // 实体粗筛网格
│   ├── entities/
│   │   ├── Entity.ts / EntityManager.ts
│   │   ├── Player.ts
│   │   ├── ItemDrop.ts
│   │   ├── Projectile.ts
│   │   ├── TownNPC.ts               // Guide 等，含入住/搬家 AI
│   │   ├── Spawner.ts               // 敌人生成规则（光照/距离/上限/昼夜表）
│   │   └── enemies/{Enemy.ts, Slime.ts, Zombie.ts, DemonEye.ts, EyeOfCthulhu.ts}
│   ├── combat/
│   │   ├── Damage.ts                // computeDamage / 击退 / i-frame / 伤害数字
│   │   └── DropTable.ts
│   ├── items/
│   │   ├── ItemDefs.ts  ItemStack.ts  Inventory.ts
│   │   └── Crafting.ts              // 配方 + 合成站过滤 + 可合成判定
│   ├── time/Clock.ts                // 昼夜（1 游戏日 = 24 现实分钟，可调）
│   ├── render/
│   │   ├── Renderer.ts              // Canvas2D 实现 + IRenderer 抽象
│   │   ├── Camera.ts
│   │   ├── ChunkCache.ts            // 16×16 tile → OffscreenCanvas，脏标记
│   │   ├── TileRenderer.ts          // merge 掩码/变体选择，决定画哪个 frame
│   │   ├── SkyRenderer.ts           // 天空渐变、太阳/月亮/星星、云（视差）
│   │   ├── LightCompositor.ts       // 低分辨率光照画布 + multiply 叠加
│   │   ├── Minimap.ts
│   │   └── Particles.ts
│   ├── assets/
│   │   ├── AssetGen.ts              // buildAll(rng): AssetBundle（启动期一次性生成）
│   │   ├── Palette.ts               // 全局调色板（颜色参考自 TEdit 数据表）
│   │   ├── TileSheetGen.ts          // 每类 tile 基础贴图 + 47 种 merge 变体
│   │   ├── ItemIconGen.ts
│   │   ├── CharacterSheetGen.ts     // 玩家/NPC 行走帧、敌人动画帧
│   │   └── PixelTemplate.ts         // 字符串像素模板 + palette-swap 引擎
│   ├── wld/
│   │   ├── BinaryReaderLE.ts        // readU32/ I32/ I16/ F32/ F64/ Bool/ String7Bit/ BitArray
│   │   ├── WldParser.ts             // parseWld(buffer): WldWorld（编排）
│   │   ├── WldSectionHeader.ts      // version/magic/sectionPointers/frameImportant
│   │   ├── WldHeader.ts             // 驱动式 HeaderFieldSpec 表读取
│   │   ├── WldTiles.ts              // decodeTiles(reader, w, h, ver, frameImportant)
│   │   ├── WldEntities.ts           // chests/signs/npcs/tileEntities
│   │   ├── WldToInternal.ts         // wld id → 内部 id 映射 + World 组装
│   │   └── headerFieldTable.ts      // 字段描述表（数据，可单测）
│   ├── save/
│   │   ├── SaveFile.ts              // 自有 JSON 格式读写 + 版本迁移
│   │   └── TileRLE.ts               // 自有紧凑 tile 编码
│   ├── ui/
│   │   ├── ui.css / dom.ts          // 极简 DOM helper（el(), bind()）
│   │   ├── HudCanvas.ts             // Canvas 自绘：血量、Buff、Boss 条
│   │   ├── Hotbar.ts / InventoryPanel.ts / CraftingPanel.ts
│   │   ├── ChestPanel.ts / Tooltip.ts / MainMenu.ts / PauseMenu.ts
│   │   └── store.ts                 // 微型 reactive store（~40 行）
│   └── data/
│       ├── tiles.ts walls.ts items.ts npcs.ts recipes.ts enemies.ts
│       └── wldMapping.ts             // wld tileId → 内部 tileId（含忽略清单）
└── tests/                            // vitest：RLE 编解码、wld 固件测试、碰撞、合成
```

**模块依赖方向（单向，禁止回环）**：`data` ← `assets/wld/save` ← `world/physics/items/lighting` ← `entities/combat` ← `render/ui` ← `core`。

---

## 3. 游戏主循环与状态架构

```ts
// core/FixedLoop.ts
const FIXED_DT = 1 / 60;
let acc = 0;
function frame(now: number) {
  acc += Math.min((now - last) / 1000, 0.25);   // 钳制防螺旋死亡
  while (acc >= FIXED_DT) { state.fixedUpdate(FIXED_DT); acc -= FIXED_DT; }
  state.render(ctx);                            // 渲染最新状态（暂不做插值）
  requestAnimationFrame(frame);
}
```

- **物理/游戏逻辑固定 60Hz**；渲染每 rAF 一次。液体模拟、敌人生成、光照重算都在固定步内按各自频率节流（液体每 3 tick 一轮、光照每 2 tick 或脏时）。
- **状态机** `GameState`：`fixedUpdate(dt)` / `render(ctx)` / `onEnter/onExit`。`PlayingState` 持有 World、EntityManager、Camera、各系统引用；`PausedState` 只渲染不更新；`WorldGenState` 跑分帧生成（见 4.2）。
- **实体系统：推荐简单类继承 + 轻组件，不用 ECS**。理由：实体种类 <15、系统间交互紧密（玩家挥剑要同时改碰撞、动画、光照无关），ECS 的 archetype 查询收益体现不出来，反而把“史莱姆跳跃”这类行为拆散。设计：
  ```ts
  abstract class Entity {
    id: number; x = 0; y = 0; vx = 0; vy = 0; w = 0; h = 0;
    dead = false; onGround = false;
    abstract fixedUpdate(dt: number, ctx: WorldContext): void;
    abstract draw(r: IRenderer, cam: Camera): void;
    get aabb(): AABB;
  }
  ```
  `EntityManager` 按类型分桶数组（`enemies[] / drops[] / projectiles[] / npcs[] / particles[]`）+ `SpatialHash`（格子 8×8 tile）供碰撞查询与生成点筛选。行为差异用组合的小 AI 对象（`EnemyAI` 接口：`idle/chase/attack` 状态函数）。

---

## 4. 各系统设计要点

### 4.1 世界数据结构（SoA 多通道平面数组）

4200×1200 = 5.04M 格。**用多个 TypedArray 平面（Structure of Arrays），不用对象数组**：

```ts
// world/TileStore.ts
class TileStore {
  readonly w: number; readonly h: number;
  readonly tileType:  Uint16Array;   // 10 MB  内部 tile id
  readonly tileFlags: Uint8Array;    //  5 MB  bit0 active | bit1 actuator | bit2 inactive | bit3-5 slope
  readonly frameX:    Uint16Array;   // 10 MB  framed 物体像素偏移（wld 导入/树/门用）
  readonly frameY:    Uint16Array;   // 10 MB
  readonly wall:      Uint16Array;   // 10 MB  用 u16 兼容 1.4 的 wall>255
  readonly liquid:    Uint8Array;    //  5 MB  amount 0-255
  readonly liquidType:Uint8Array;    //  5 MB  0无 1水 2岩浆 3蜂蜜
  // 光照缓存（lighting 模块持有，引用同一索引规则）
  idx(x: number, y: number): number  // y * w + x（行优先，利于光照行扫描与 chunk 行拷贝）
  isActive(x, y): boolean
  isSolid(x, y): boolean             // TileDefs[type].solid && slope==0 && !actuatedOff
  setTile(x, y, type, opts?: {frameX?, frameY?}): void   // 同时通知 ChunkCache + 光照脏标记
}
```

- 合计约 55 MB，浏览器可接受；若要省内存可把 `wall` 降为 `Uint8Array`（放弃 id>255 的稀有墙）。
- `wld` 导入与自有存档都直接填充这些平面，零中间对象 → 导入 4200×1200 全图解码预计 <1.5 s（纯 typed array 循环），可在 Worker 中跑。
- **遍历性能**：所有热点（光照 BFS、chunk 重绘、碰撞扫描、minimap）都只访问视口 + 边距区域；全图遍历仅发生在生成期和导入期，且可分帧。
- `TileDefs`：`Map<number, TileDef>`，`TileDef { id, key, name, solid, blend, mergeWith, platform, lightSource?: RGB, opacity: number(光照阻挡), pickPower(镐力需求), axePower?, hammerPower?, framed?, frameSize, drops: DropEntry[] }`。硬度、光照阻挡率等数值自行设计平衡表。

### 4.2 世界生成（分层管线，分帧执行）

- **噪声库**：`simplex-noise`（MIT，纯 TS，带 seed）。地表用 1D fBm（4 个 octave），洞穴用 2D fBm。
- `WorldGen.generate(seed, cfg)` 管线，每 pass 是纯函数 `(store, rng, cfg, progressCb) => void`，`WorldGenState` 用 `requestIdleCallback`-style 分帧跑（每帧 ≤8 ms）以显示进度条：
  1. `TerrainPass`：地表高度 `surfaceY(x) = base + fbm1(x)*amp`（amp 随深度递增制造丘陵）；`surfaceY < y < surfaceY+深度的区间填土，更深填石；y > rockLevel（约 0.72h）全石。基岩边界 3-4 格不可破坏层。
  2. `CavePass`：两类——(a) 2D 噪声 `fbm2(x*f, y*f) > 0.32` 挖空（阈值随深度轻微变化，浅层少洞）；(b) 蠕虫隧道：随机游走 8-14 条，头部方向受噪声扰动，半径 2-5 变化，沿途清空形成连通大洞穴。表层 6 格内不挖防止破地。
  3. `OrePass`：按深度带（表土带/浅洞带/深洞带）撒簇：铜（浅多）、铁（中）、银（深）、金（最深），每簇 blob 生长 4-14 格；金与深洞面积挂钩。簇密度用泊松式随机点 + 拒绝重复。
  4. `LiquidPass`：地表洼地（局部高度极小值）灌水成湖；洞穴低处灌静水。
  5. `SurfacePass`：最上层实心土改草；随机撒树（间距 5-14，树 = 树干 6-12 格 + 树冠 framed tile，记录到 `TreeRegistry` 供整体砍伐逻辑）；撒花/蘑菇/石子装饰 tile。
  6. `StructurePass`（可选）：3-5 座地下小屋（木板墙 + 木墙 background + 门洞 + 火把 + 工作台/熔炉），内置宝箱（loot 表按深度分层：地表→木材/火把/绳，地下→矿石/药水/钱币）。
  7. 后处理：出生点 = 世界中心附近第一个 2×3 空气站立的列；`skyLight` 列重算。
- 生物群系分层（简化）：水平分区（雪原/森林/沙漠/丛林按 x 段）影响表层 tile 与树样式；垂直分层（天空/地表/浅洞/深洞/地狱底界）影响敌人生成表。M1 先只做森林单群系，M4 补雪原/沙漠。

### 4.3 光照系统（BFS 衰减 + 局部脏重算）

- **模型**：强度 0-255，三通道 RGB 三个 `Uint8Array`（与 TileStore 同索引）。颜色光源（火把橙、岩浆红）才有分通道必要。
- **两套光**：`skyLight`（天空直射光，无色，随昼夜缩放 0.05~1.0）与 `blockLight`（光源 BFS）。最终 `light = max(skyLight * dayFactor, blockLight)`，逐通道合成。
- **天空光**：每列从 y=0 向下，遇到第一个 `opacity > 0` 的 tile 停止，以上全亮；草/平台半透明衰减小。列缓存 `skyLightColumnTop[x]`，tile 变化时 O(高度) 更新单列。
- **传播（BFS）**：初始队列入列 = 区域内所有光源 + 天空亮格。用 **256 桶队列**（bucket queue，按强度分桶，从高到低处理，避免优先队列排序成本）。弹出格 `(x,y,lv)`，对四邻：`nlv = lv - (opaque(neighbor) ? solidCost : airCost)`（airCost≈6、solidCost≈22，每 tile 不同 opacity），`nlv > cur[neighbor]` 则更新并入队。每格最多入队常数次。
- **计算范围**：只算 `viewportTileRect 外扩 24 格`。玩家移动跨越 chunk 边界时增量平移已有 buffer（避免全量重算）；放置/破坏 tile、火把增删 → `LightDirtyTracker.markDirty(x, y, radius=16)`，本帧或下帧只重算脏矩形。
- 性能预算：可视 60×35 tile 外扩后 ~110×85 ≈ 9.4k 格，BFS 每格约 4 邻居 + typed array 访问，一次全量重算 <2 ms，只在跨 chunk 时发生，完全可承受。

### 4.4 渲染管线

每帧顺序（`Renderer.render(camera, world, entities, light, clock)`）：

1. **天空** `SkyRenderer`：按 `Clock.timeOfDay` 插值的天空渐变（几组关键色关键帧），太阳/月亮沿圆弧运动，星星（夜间淡入），2 层视差云（程序噪声生成的云剪影，循环平铺）。
2. **背景墙 + tile（chunk 缓存）** `ChunkCache`：
   - 世界切 16×16 tile chunk，每 chunk 一张 256×256 离屏 canvas，内容 = 背景墙层 + tile 层（含液体静态部分不进缓存）。
   - `markDirty(cx, cy)`（tile 变更、首次访问、邻接融合变化时）→ 该 chunk（及边缘相邻 chunk）入重绘队列，每帧最多重绘 4 个 chunk 削峰。
   - 绘制时 `drawImage(chunkCanvas, screenX, screenY)`，视口外 chunk 全部剔除。
3. **TileRenderer**（chunk 重绘时调用）：对每格先画 wall（比 tile 暗 15% 的同系色变体），再画 tile。**边缘融合**：对本格四邻 + 四角是否同类 solid 计算 8-bit 掩码 → 选对应 merge 变体 frame（贴图由 4.5 预生成）。`canBlend=false`（如矿石）直接整块贴。framed 物体按 `frameX/frameY` 从 sheet 取块。
4. **液体**：半透明色块 + 顶部表面线 + 根据 `liquid` 值的高度裁剪；水面加正弦波动画。
5. **实体**：`ItemDrop / Projectile / Enemy / TownNPC / Player` 按 y 排序绘制（前景感），玩家手持工具挥舞旋转绘制（以肩部为轴的弧线，挥动角度由攻击计时驱动）。
6. **光照合成** `LightCompositor`：一个 `viewportW×viewportH`（tile 数）的小 canvas，每像素写入合成后的光照色，`drawImage` 放大 16 倍（`imageSmoothingEnabled=true` 得到柔和过渡），`globalCompositeOperation='multiply'` 盖在世界之上；再叠一层昼夜整体色调（`'overlay'` 微弱）。
7. **粒子上层、选框**（鼠标悬停 tile 高亮 + 可挖范围圈）。
- **Camera**：`{ x, y (世界像素), zoom }`，`zoom` 默认 2（1 tile 16px → 屏 32px），跟随玩家带缓动 + 前视偏移，钳制在世界边界内。
- **Minimap**：1 tile = 1px 离屏 canvas，初始化全图扫一遍（用 TileDefs 的 mapColor，颜色参考 TEdit tiles.json/walls.json 的 color 字段但重新取整组织），运行期每 30 tick 把脏 chunk 区域重刷。视口矩形 + 玩家点 + 大 NPC 点叠加。

### 4.5 程序化素材生成

**原则：所有 sprite 启动期代码生成，一次生成常驻内存；确定性 RNG（固定种子）保证每次刷新一致。**

- `Palette.ts`：全局色板，分材质组（土/石/木/金属/草/液/皮肤…），每组 base + 2 阴影 + 2 高光。起始色值参考 TEdit 数据表 `color` 字段（如 Dirt `#976B4B`、Stone `#808080`、Grass `#1CD85E`），随后自行派生明暗档位。
- `TileSheetGen.ts`：
  1. 基础块 16×16：底色填充 → 值噪声逐像素抖动（±1 明暗档）→ 四边按外露方向加深/提亮（上边受光）→ 少量像素级杂质点。
  2. **merge 变体 sheet**：由 8-bit 邻接掩码（4 直邻 + 4 角）选取，标准 47-blob 变体。生成方式：对每个掩码画“圆角外轮廓”——对每个边缘像素判断其到块中心的象限归属决定去留，再叠加噪声；角位（同时缺两个正交邻）内缩圆角。每 tile 类型生成一张 `16×16×47` 的 sheet（或按需生成常用掩码，惰性缓存）。
  3. 草块：土基 + 顶部 3-4px 草层（边缘锯齿随机高度）；矿石：石基 + 2-4 簇矿物斑点（每簇 3-6px blob，金属高光像素）；木板：横向条纹 + 钉点；平台：半高块 + 支架。
  4. framed 物体（工作台/熔炉/铁砧/门/宝箱/火把/树）：`PixelTemplate.ts` 用字符串像素图定义（每字符映射色板索引），16×16 或 16×24，含 2-3 帧动画（火把火焰、熔炉火光）。树 = 树干段 tile（上/中/下）+ 树冠 2×2 blob（噪声剪影 + 叶色双色调）。
- `ItemIconGen.ts`：16×16 图标。方块类 = 对应 tile 贴图缩样；工具类 = 参数化绘制（柄线段 + 镐头弧/斧刃三角/锤面矩形/剑刃菱形），金属档位换色即得铜铁银金系列；锭 = 梯形 + 高光条；药水 = 瓶形模板 + 液体色换。
- `CharacterSheetGen.ts`：玩家/NPC 40×56 像素框，骨架参数绘制（头/躯干/双臂/双腿矩形），生成 idle 1 帧 + 走路 4-6 帧（四肢相位表）+ 跳跃 1 帧 + 使用物品 2 帧；敌人：史莱姆 = 圆润 blob（squash/stretch 参数直接运行时变换，不必逐帧）、僵尸 = 人形模板换绿皮、恶魔眼 = 球 + 虹膜 + 尾巴触须 3 帧、EoC = 大眼球 + 断裂虹膜（P2 用第二模板）。武器挥舞直接对武器图标做运行时旋转变换，不预生成。
- 产物统一进 `AssetBundle { tileSheets: Map<tileId, Canvas>, itemIcons, charSheets, fx }`，渲染层只查表。

### 4.6 物理与碰撞（分轴扫描 tile AABB）

```ts
// physics/TileCollision.ts
interface Body { x: number; y: number; w: number; h: number; vx: number; vy: number;
                 onGround: boolean; hitWall: boolean; headHit: boolean; }
function moveAndCollide(b: Body, world: World, dt: number): void {
  // 1) X 轴：b.x += b.vx*dt；计算 AABB 覆盖的 tile cell 范围 [x0..x1]×[y0..y1]；
  //    对每个 solid cell，按 vx 方向把 b 推回 cell 边界，vx=0，hitWall=true。
  // 2) Y 轴：b.y += b.vy*dt；同法解析；vy>0 落地置 onGround，vy<0 撞头。
  // 步进子分：单帧位移 > 8px 时拆多步，防高速穿透。
}
```

- tile = 16px。玩家 hitbox 20×42 px（碰撞盒），视觉稍大。重力 ~0.35 px/tick²、行走加速/摩擦、跳跃初速 ~6.4 px/tick、土-Speed 感调参集中放 `core/constants.ts`。
- 平台（platform tile）：只有 `vy>0 且 之前脚部在其上方 且 未按下降键` 才实心，实现单向穿越。
- 液体：玩家进入水 → 重力减半、最大速度钳制、按跳上浮（游泳）；简化浮力不做密度。
- 敌人复用同一 `moveAndCollide`；恶魔眼类飞行实体只做 tile 穿透判定（撞墙反弹/转向）。

### 4.7 `.wld` 导入解析器（TS）

- `BinaryReaderLE.ts`：`readUInt32/readInt32/readInt16/readUInt16/readSingle/readDouble/readBoolean/readByte/readString7Bit/readBitArray`（`readInt64` 用 `BigInt`，仅 creationTime 等少数字段，可读两 u32 拼 BigInt）。字符串长度用 7-bit varint。
- `WldParser.parseWld(buf, onProgress)` 流程：
  1. 读 version、magic/fileType 校验、fileRevision、flags、sectionCount、sectionPointers、tileFrameImportant 位图。
  2. seek `sectionPointers[0]`，用 `headerFieldTable` 驱动读 header（含全部版本门控字段），取 `tilesWide/tilesHigh/spawnX/spawnY/groundLevel/rockLevel/time/dayTime/isCrimson` 等。
  3. seek `sectionPointers[1]`，`WldTiles.decodeTiles`：按 1.3 的 header 位语义逐 tile 解码，列优先 + RLE 展开写入 `Uint16Array/Uint8Array` 目标平面（不解码成对象）。
  4. 顺序读 chests/signs/npcs/tileEntities（用 sectionPointers 校验位置）。
  5. footer 三重校验（bool/title/worldId）。
  6. `WldToInternal.convert(wld)`:按 `data/wldMapping.ts` 把用到的 wld tileId（土/石/草/各类矿/木/平台/火把/工作台/熔炉/铁砧/门/宝箱/树…约 60 个）映射到内部 id；未映射的 tile → 就近实心/非实心降级（实心的显示为石色杂色块，保持碰撞语义）；liquid 直接保留；chests 转为内部 Chest 对象（物品 id 同样映射，未知的丢弃并计入警告清单）。
  - 放在 **Web Worker**（`wld/worker.ts`）执行，主线程 postMessage 传回 typed array（transferable，零拷贝）。
- 单测：用一份真实 1.4.4 小地图（4200×1200 以下）做固件，断言 header 字段、若干已知坐标 tile、chests 数量；再加一个**手工构造的字节流**用例覆盖 RLE 三种计数类型、header 链、wall 高位、liquid、frameImportant 位图边界。

### 4.8 自有存档格式（JSON 外壳 + 二进制 tile 段）

```jsonc
{
  "format": "sandboxworld.save", "version": 1,
  "header": { "name", "seed", "width", "height", "spawn": [x,y], "created", "playTime",
              "groundLevel", "rockLevel" },
  "clock": { "timeOfDay", "dayCount", "moonPhase" },
  "tiles": "<base64>",          // TileRLE 自定义编码，见下
  "liquid": "<base64>",         // 与 tiles 同编码（只存非零格）
  "entities": {
    "player": { "hp", "position", "inventory": [ {id, stack} ×40 ] },
    "chests":  [ { "x", "y", "items": [...] } ],
    "townNpcs":[ { "type", "x", "y", "home": [x,y] } ]
  },
  "flags": { "downedBoss": {...} }
}
```

- `TileRLE.ts` 自定义编码：行优先扫描，每个条目 `varint 重复计数 | tile flags byte | tileType varint | frameXY varint(仅 framed) | wall varint`——比 wld 简单（无 header 链），配合每行末尾 sentinel。目标是自有存档体积 <2 MB、解析 <300 ms，同时 JSON 部分保持人可读可 diff。
- `SaveFile.save(world): string` / `load(json): World`；`version` 字段 + `migrations: ((save)=>save)[]` 支持未来升级。

### 4.9 UI 架构（DOM overlay 为主）

- **DOM overlay（推荐）**：主菜单、暂停菜单、物品栏/背包、合成面板、宝箱面板、tooltip、设置。理由：布局/文字/点击/hover/滚动是 DOM 强项，开发快、无需实现焦点与命中测试；用 `ui/dom.ts` 的极简 helper + `store.ts` 微型响应式（`createStore(state)` + `subscribe(selector, fn)`），不引框架。
- **Canvas 自绘**：血量心形/血条、Buff 图标行、Boss 血条（屏幕底部）、小地图（右上）、伤害数字、物品拾取提示。这些贴着世界/需要每帧动画，canvas 内做更顺。
- 交互流：点击快捷栏格 → DOM 更新选中态 → `Input` 屏蔽该次点击穿透到世界（用 `event.target` 判断是否 UI 命中）。
- 合成面板：左侧可用配方列表（按 `Crafting.stations(player)` = 玩家 3×3 格内检测工作台/熔炉/铁砧 + 徒手），右侧材料检查（缺料置灰显示缺口），点击合成调用 `Inventory.consume/insert`。

---

## 5. 分阶段实施计划

### M1 世界 + 移动 + 挖掘（打通最小可玩闭环）
**文件**：`core/*`、`world/TileStore.ts`、`world/World.ts`、`world/TileDefs.ts`、`gen/{WorldGen,TerrainPass,CavePass,OrePass,SurfacePass}.ts`、`physics/*`、`entities/{Entity,EntityManager,Player}.ts`、`render/{Renderer,Camera,ChunkCache,TileRenderer,SkyRenderer}.ts`、`assets/{AssetGen,Palette,TileSheetGen,PixelTemplate}.ts`、`time/Clock.ts`、`ui/Hotbar.ts`。
**要点**：AssetGen 先行（土/石/草/木/矿/树的贴图 + merge sheet）；挖掘 = 鼠标悬停高亮 + 按住按 `pickPower` 计时破坏 + `TileStore.setTile` + 粗糙掉落（M1 直接进背包）；树整体砍伐（`TreeRegistry` 找同树所有格一起清）；放置走快捷栏选中物品。
**验收**：生成 2100×600 世界 <3 s 且进度可见；60 fps 平地行走/跳跃/挖/放；挖洞后天空区域直观变亮（暂用简单天空列光）；破坏树掉木材；存档/读档往返一致。

### M2 光照 + 物品 + 合成
**文件**：`lighting/*`、`render/LightCompositor.ts`、`items/*`、`combat/DropTable.ts`、`entities/ItemDrop.ts`、`assets/ItemIconGen.ts`、`ui/{InventoryPanel,CraftingPanel,Tooltip}.ts`、`data/recipes.ts`、`save/*`。
**要点**：BFS 光照 + 火把放置为光源；掉落物实体（重力、落地、2.5 格磁吸、合并堆叠）；配方链：木→工作台→木镐/木剑/火把（凝胶+木）；石→熔炉（火把+石+木）→ 铜锭/铁锭→ 铁砧→ 金属工具/剑/护甲。
**验收**：洞穴全黑、火把照明柔和衰减正确；昼夜天空光变化平滑；满配方链从徒手到铁套可全程合成；tooltip 显示名称/伤害/工具力/堆叠。

### M3 敌人 + 战斗
**文件**：`entities/enemies/{Enemy,Slime,Zombie,DemonEye}.ts`、`entities/Spawner.ts`、`combat/Damage.ts`、`render/Particles.ts`、`assets/CharacterSheetGen.ts`、`ui/HudCanvas.ts`。
**要点**：近战挥舞（以玩家为圆心半径 ~2.6 tile 的旋转弧判定，一挥多段但每敌一挥一次）；接触伤害 + 击退 + 受击无敌帧 + 伤害数字；生成规则：地表白天史莱姆限量、夜间僵尸/恶魔眼、地下暗处生成、距玩家 25-60 格环带、总数上限 8；死亡掉落（史莱姆凝胶+钱币、僵尸铁器概率）。
**验收**：夜间地表持续有敌、白天安全；挥剑可同时命中多个且击退方向正确；玩家死亡→重生（掉一半钱币可选）→ 出生点。

### M4 液体 + 宝箱 + NPC
**文件**：`world/liquid/LiquidSim.ts`、`gen/{LiquidPass,StructurePass}.ts`、`ui/ChestPanel.ts`、`entities/TownNPC.ts`、`render/Minimap.ts`。
**要点**：液体元胞自动机（每 3 tick：本格向下→两侧均分，用变化格集合增量更新，只模拟可视区+10 格；静止格快速通道跳过）；世界生成埋宝箱 + 按深度 loot 表；宝箱 UI 双栏物品移动；空房间判定（flood-fill 封闭矩形区域 + 含门 tile + 桌椅 + 光源）→ 向导入住、死亡白天重生、夜间回家。
**验收**：挖开湖底水正确流动扩散最终静止；游泳可行；宝箱战利品可取出且关箱重开保留；建合格房间向导入住。

### M5 Boss（克苏鲁之眼）
**文件**：`entities/enemies/EyeOfCthulhu.ts`、`ui/HudCanvas.ts`（Boss 条）、`combat/Damage.ts`、`data/enemies.ts`、`items/*`（可疑眼球召唤物配方：晶球+恶魔眼下落后 lens×6 @ 恶魔祭坛简化为工作台）。
**要点**：两阶段——P1 悬浮 + 周期斜向冲撞 ×3；HP<50% 转 P2（嘴部裂开、召唤 2 只小眼球、冲撞更频更快的伺服浮动）；夜间自然生成条件（HP≥200+防御≥10 或已砸暗影球简化）与召唤物手动召唤；黎明强制飞离；击杀掉猩红矿/弱效药水/钱币。
**验收**：Boss 条显示两段血量；两阶段 AI 行为可辨；召唤→击杀→掉落→天亮消失全流程通。

### M6 `.wld` 导入
**文件**：`wld/*`、`data/wldMapping.ts`、`ui/MainMenu.ts`（导入入口）、`wld/worker.ts`。
**要点**：按 1.3/1.4 实现解码；只支持 version ≥210；导入后把未知 tile 降级；导入的世界可正常玩（挖掘/光照/液体）。
**验收**：真实 1.4.4 地图导入成功（4200×1200 <3 s，Worker 内无卡帧）；地表轮廓、洞穴、水域、宝箱位置与原版地图肉眼一致；单元测试覆盖 RLE 三型计数与 header 链边界。

---

## 6. 风险与注意事项

1. **版权红线**：TEdit 只作格式/数据事实参考。禁止复制其 C# 代码逻辑到 TS（RLE 解码语义可参照，但实现要按自己的组织方式重写并充分理解后独立表达）；不使用任何 Terraria 原版或第三方贴图/音频；游戏名、宣传语避开 "Terraria" 商标。tile/wall/item 的 id、名称、颜色属事实数据，风险低，但渲染、AI、生成、平衡数值全部原创。
2. **光照与 chunk 缓存的一致性**：tile 变化必须同时通知 `ChunkCache` 与 `LightDirtyTracker`，且相邻 chunk 因边缘融合也要标脏——统一收敛到 `World.setTile` 一个入口，禁止绕过。
3. **wld 版本碎片化**：header flags 字段极多，靠 `headerFieldTable` 数据驱动而非散落 if-else；每加一个支持版本用真实文件做固件回归，防止流错位这种静默错误。
4. **液体性能**：全图元胞自动机是大坑，必须限制在可视区 + 增量变化集合 + 静止快速通道，否则大湖会拖垮帧率。
5. **性能回归**：每里程碑用固定场景（生成种子固定）记录 fps 与单帧耗时；`ChunkCache` 命中率、光照重算次数要有临时调试面板。
6. **accumulator 螺旋死亡**：低帧率下钳制单帧累积时间；液体/生成等重逻辑放固定步内节流而非每 tick。
7. **数值平衡**（挖掘时间、敌伤、掉率）不要在代码里散落魔法数，集中 `data/*.ts` + `core/constants.ts`，便于整体调参。
8. **大世界内存**：导入 4200×1200 世界时三个 RGB 光照平面全图分配是 15 MB，但光照只需视口 buffer——光照平面按「可视区域 + 2 倍边距」的环形缓冲分配而非全图，避免浪费。

### Critical Files for Implementation
- ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/World.FileV2.cs （.wld 全格式参考，重点 `LoadSectionHeader`/`LoadHeaderFlags`/`DeserializeTileData`/`LoadChestData`/`LoadNPCsData`/`LoadFooter`）
- ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Tile.cs （tile 字段与位标志语义）
- ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Data/tiles.json （tile 定义/颜色/融合规则事实参考）
- ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Data/versions.json （版本号↔游戏版本映射）
- ~/Project/GLM/SandboxWorld/Terraria-Map-Editor/src/TEdit.Terraria/Objects/TileProperty.cs （textureGrid/frameSize/wrap 语义，辅助理解 framed tile）
````
