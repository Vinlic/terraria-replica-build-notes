---
name: seed-equivalence-plan
description: 种子等价路线图 L0 已完成——UnifiedRandom/Crc32/TranslateSeed 位级移植+真二进制金标，L2 金标 .wld 待用户产出
metadata: 
  node_type: memory
  type: project
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
  modified: 2026-08-11T06:53:30.076Z
---

种子等价工程（2026-08-11 立项，目标：同种子复现原版 1.4.5.6 地图）。

- 路线：L0 位级基座（✅）→ L2 金标闭环（✅ 5 金标 .wld 入库 + seed-parity diff）→ **L1 进行中：TerrainPass 已位级对齐（terrain-oracle.cs C# 复刻+反射真 UnifiedRandom→逐列地表 4200/4200 全等；Reset 按 cs:11159-11472 精确顺序重写；4 缺失洞穴 pass 已补齐接入）。**洞穴链+Beaches+IceBiome+Grass+Jungle+MudCaves 已位级对齐（两种子×16 检查点，374 测试全绿）**。MudCaves 原版精确版（递归洪水+散块清除）已接回真实管线，近似 spreadGrassAll 与 CleanupPass 重复清除已删。下一步=Desert(12532)→GlowingMushroom(12581)→Marble/Granite→FloatingIslands(12976)→…→Dungeon。新坑：SpreadGrass 岩浆只 break 内层循环（后续列可翻回 flag）；反射 Main.tileSolid 会触发 FNA 静态构造不可行，oracle 用已审计 TILE_DEFS solid 表。Jungle 修 6 处（gem 偏移上界/MudWallRunner 1:1 替换自创实现/抖动 6ws/拒绝无界/UnderworldLayer h-200/y clamp H）。教训新增：⑥(int)NaN 是平台语义——x86=int.MinValue（金标实证，Mac 游戏经 Rosetta x86 跑）、ARM64 dotnet=0，oracle 在 ARM Mac 须显式模拟 x86；⑦rng.int 区间错位是高发 bug（int(a,b)=Next(a,b+1)，写代码时以注释里的 Next(a,b) 为锚逐个核）；⑧tileRunner 的 type 参数是内部 id，传 vanilla sheet 会静默错放（53=内部沙漠化石）；⑨DunesBiome 两 description 先建后放（dune2 图 pre-dune1）。洞穴链三代理审计已修复（num3 Next(4) 必掷/CavesPass 重写回 TileRunner/Caverer 掷序/Clay (int) 截断/OceanSand 中点金字塔 Next(6)/地牢主题 Next(3) 归位 Dunes 头/genWorldSurfaceHigh raw 口径/Cavinator 地牢终止）** → L3 浮点兜底。
- 关键教训：①原版 TerrainPass num3/num4 是 double 非 float——曾被误加 fround float32 腐蚀整条游走；②小世界 clamp 0.17+0.02；③FillColumn 空气边界=trunc 非 ceil；④GenVars.worldSurface(游走终值 double)≠Main.worldSurface(High+25)；⑤用户在并行写 pass（沙丘/微光/DunesPass 等其接线）——改 WorldGen.ts 前先重读。
- L0 交付：`src/core/rng.ts` UnifiedRandom 1:1（RNG 类 API 不变内核已换）、`translateSeed`（数字→Abs/非数字→Crc32，Crc32 在 ReLogic.dll=`Terarria1456/Terraria.Libraries.ReLogic.ReLogic.dll`，ilspycmd 已装 `~/.dotnet/tools`）；金标 `tools/golden/rand-golden.cs` 反射**真·Terraria.exe**（Steam 本机 `~/Library/Application Support/Steam/steamapps/common/Terraria/Terraria.app/Contents/Resources/Terraria.exe`）导出 → `tests/golden/unified-random.json` + 位级断言。
- 关键陷阱：simplex-noise createNoise2D 构造即消耗 RNG 流（已删）；C# int 溢出=|0；Next(min,max) 是 (int)(double) 截断非 floor；weather 测试边界必须按原版推导不能按流标定。
- 文档：docs/worldgen/seed-equivalence.md（权威）。关联 [[vanilla-worldgen-port-status]] [[js-bitwise-int32-traps]]。
