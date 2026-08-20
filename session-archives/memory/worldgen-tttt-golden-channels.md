# TTTT 批（2026-08-19）：金标三通道织入 + Water Chests 重掷域 + 梳妆台注册

## 织入资产（沿用 OOOO 先例保留）
- `/tmp/tttt-app`（Terraria.app 织入 exe）+ `/tmp/tttt-patch`（probelib+patcher 源）
- 基座 = `/tmp/sw-slp/TerrariaServer.hs.exe`（g dumps 同源；**运行时 ProbeLib 必须含 HsProbe**——WriteGrid 被重定向过去，漏了 → 无 dump + gen 崩溃重试循环）
- 钩子：RunPass 头（pass 名/序）+ UnifiedRandom.Next×2 头（span）+ Chest.CreateWorldChest/RemoveChest 头
- 产出：`SW_TT_FR_PASSES` 命中 pass 头 → `/tmp/tttt-fr/NNN_Name.{fr,chest.tsv}` + `/tmp/tttt-frw/*.wire`（红1蓝2绿4黄8致动16）；`SW_TT_SPAN_PASSES` → Next span 流
- 启动：`HOME=/tmp/tttt-home SW_EVIL=0 SW_HS_DUMP=1 SW_DUMP_ALL=<dir> SW_PASSCHAIN=<txt> arch -x86_64 ./TerrariaServer -autocreate 1 -worldname w -seed 9293480 -world <wld> -port 7802 -noupnp -difficulty 0`（跑后 pkill 7802）
- 自证法：848 dump 与 /tmp/sw-slp/g cmp 全同 + pc.txt 哈希列 diff（去 ms 列）

## 三个大坑
1. **Cecil InsertBefore 锚点缓存**：`var first = instr[0]` 缓存后多次 InsertBefore → 后插者排最靠锚 → Call 排到参数前 = 栈空 InvalidProgramException（或静默 Pass 冻结 + 服务器无限重生成）。**每条插入都重取 `Body.Instructions[0]`**（oooo patcher 的写法）。
2. `Box(Point)` 反射探针方案废置；span 头钩 + JS 侧同流重放即可取值。
3. wld 不是注册表真值：Final Cleanup 尾段 RemoveChest 全表后按存活 tile 重建；生成期态只能 pass 头快照。/tmp/oooo-world/g9293480.wld 是大世界（8400×2400）跑产物——SSSS 的"sink 179 vs 350"对照基数即此误照。

## 修复
1. **BuriedChestsPass.runWaterChestsPass**：两趟搜索趟2（cs:17440-17445）y 首掷与重掷同域 [⌊worldSurface⌋, UL)——曾两趟重掷都写 [50,UL) → 13/18 箱漂移 + 流雪崩（#62 → 0；span 5495=5495 全同）。
2. **HellFortPass.place3x2HF dresser 分支**：vanilla Place3x2(88) 在 flag2 终判前无条件 Chest.CreateChest(x-1,y-1)（cs:52169）——同位重条目→放置失败；失败尝试条目保留（孤儿）。WorldGen.ts:769 传 world.chests。地狱屋 11 座 style49 雕像帧本就正确。
3. **tools/_wwwrep.test.ts 槽51/53**：金标帧（tttt-fr/*.fr）+ 金标线（tttt-frw/*.wire）入口直注（SW_WWW_GF=0 可关、缺文件跳过）→ #99 259→86。

## 定谳/移交
- #101：金帧金线+van注册表下 IsAGoodSpot 27=27、5 轮 Place 掷序全同 → 逻辑 1:1；残差 = JS 管线 wire/StructureMap 近似 + Temple sink 4v5（#66 通道）。下一定罪钩：TileFrame(resetFrame:true) 通用分支每调 1×Next(0,3)（cs:82448 frameNumber）——MicroBiomes actuallyPlace* 未镜像（第 5 轮 Place 后 4 掷差）。
- #58：137 帧债属 Traps(248@slot76)/Temple(113)/Dungeon(3×style48 雕像)——StatuesPass 无罪；(605,782) 金标帧 (18,0)。禁区按"报告勿改"处理。
- #99 ⑦ 重建段：输入已备（/tmp/tttt-fr/099_Tile_Cleanup.chest.tsv = slot98 物品位）——TileCleanupPass 补 cs:21484-21741 即可。
- #63：(474,996) JS wave65 vs vanilla 同位（y=996 门掷 roll=4 敏感带）；S-访/门掷失败零写零 SF = 双盲；需织 vanilla Spider 全访日志（S+门失败+waveN）或 C# 独立模拟器。
