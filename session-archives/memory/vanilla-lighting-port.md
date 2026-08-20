---
name: vanilla-lighting-port
description: 原版光照系统 LightingEngine/LightMap/TileLightScanner 1:1 移植完成——文件布局/关键语义/陷阱/验证
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-11T07:09:06.820Z
---

2026-08-10 完成原版 1.4.5.6 光照(LightMode.Color)1:1 移植,替换自制 BFS 引擎(备份在 `game/docs/backup/LightingEngine.legacy.bak.ts` + README 回滚说明)。

- **文件**(`game/src/lighting/`):`FastRandom.ts`(48 位 LCG)/`lightTables.ts`(全部常数+TorchID 24 色+wallLight 15 墙+发光墙表+月相地板)/`SkyColor.ts`(Main.time 映射+SetBackColor 五段曲线+tileColor+FlickerClock 三振荡器)/`TileLightScanner.ts`(mask+播种)/`LightMap.ts`(扫描 Blur)/`LightingEngine.ts`(4 状态机+公共面)。
- **核心算法**(LightMap.cs:86-254):非洪泛——2 pass × 4 向单调线扫描;每线携带 zero+三通道死标记;每格 ①cell>zero→复活 ②写/死(阈值 0.0185) ③按**当前格** mask 衰减(air 0.91/solid 0.56/cracked 0.80/water 分通道 (0.88,0.96,1.015)×0.91×逐格 FastRandom(98,100)/honey (0.75,0.7,0.6)×0.91)。空气传播 ~42 格、实心 ~7 格。输出 ×GLOBAL_BRIGHTNESS 1.2 钳 255。
- **播种顺序**(逐格 max-raise):天空(y≤groundLevel,SetBackColor 曲线+月相地板,挡太阳=solid+坡/半砖/致动例外+liquid<200,墙透光=wallLight 表)/地狱(y>lavaLine,v=0.55+sin 脉动)/发光墙/发光 tile(sheet 4 火把走 TorchID 24 色含 demon/disco/shimmer 动态+蜡烛族 localRand 闪烁;其余 def.light/255;`lightIsOn` 接线门控)/岩浆液体光(0.55+(270-mouseTextColor)/900)/addLight 动态(手持火把 ×0.5)。
- **mask**:`blocksLight = solid && !platform && opacity≥0.9`(门/平台/树不挡);**致动/坡面不挡光**(修复旧引擎穿墙 bug);水 liquid>128、岩浆 None、蜂蜜 Honey。
- **调度**:4 状态(MinimapUpdate/ExportMetrics 空槽保 4 tick 周期/Scan/Blur+Present 双缓冲交换);dirty→同 tick 快进全周期;liquidDirty→3 tick 节流;ensureRegion 视口±28(无 MOVE_THRESHOLD,原点只在重算时移动)。
- **合成端**:Renderer.compositeLight 已删 0.78 gamma LUT 与 amb=10 环境光底(原版皆无;夜晚暗是原版行为);保留 SS=2 双线性+'multiply'。
- **★ FastRandom.Next 陷阱**:原版 L68-82 拒绝采样用 **int32 溢出**判定(num-rem+(max-1)<0);JS 无溢出,`1<<31` 是负数会让自造位宽算法死循环。正确移植:`(max&-max)===max` 走快速路径,否则 `num ≤ 2^31-1-(max-1)` 才接受。水/蜡烛闪烁全依赖它。
- **Clock 边界差**:我们 6:00/18:00 vs 原版 4:30/18:00,SkyColor.toVanillaTime 做映射吸收;SkyRenderer/音频仍吃旧 World.dayFactor 不动(晨昏轻微不同步,已记录)。
- **验证**:`vite-node scripts/lighting-test.mts` 51 用例(LCG/曲线连续性/传播距离/mask 矩阵/状态机/火把动态);E2E 数值断言(白天 255/夜 16 月相地板/洞穴 0/火把 255);性能:**全周期 1.03ms、空闲 0.25ms/tick**(140×110 区域);npm test 39/39、wiring 31/31、tsc 干净。
- 未移植(有意):Legacy 三引擎/小地图光照导出/彩色玻璃墙染色/SceneState 神庙地牢衰减平滑/微光/日食血月/油漆;addLight 仅手持火把在用(弹幕/盔甲发光待接)。

关联 [[vanilla-worldgen-port-status]]、[[reference-vanilla-source-of-truth]]。
- **日月原版化(2026-08-10 补)**:SkyRenderer 弃用程序化太阳/月亮,改用 `Sun.png`(114×114)+ `Moon_0..8.png`(50×400 竖条,8 相位帧)——SkyRenderer 自建 Image 加载(同云模式,只进 vanilla-atlas.mjs MISC 不进运行时 VANILLA_MISC)。绘制数学 1:1 Main.cs:62279 DrawSunAndMoon:`x = t*(屏宽+图宽*2)-图宽` 横穿、`y = |t*2-1|²*250+180`(正午/午夜最高)、`scale = 1.2-|t*2-1|²*0.4`(太阳再 ×1.1)、`rot = t*2-7.3`;月亮相位 = `dayCount%8` 选竖条帧;moonType 字段预留(默认 0,wld header moonType 未透传)。无径向光晕(原版没有)。E2E 验证:正午太阳暖色 3458px、夜月+星 400 亮px、贴图尺寸正确;满月/新月相位差分验证因另一会话在途损坏(StructuresPass 又挂)未完成。
- **云速修正(2026-08-10,用户报"云飘特快")**:旧实现 wind=满幅正弦(±1)→云 60-240px/s。已按 Main.cs:58222-58310 一比一移植风场:target 随机游走(±0.001 步,1/4±0.025·1/2±0.05·其余±0.1/帧)+**钳 ±0.35**+7200-28800 帧重掷(多数 0/±0.2);current 以 0.0003+|diff|×0.0015/帧缓动;初值 ±0.8(L10800)。实测 20s 采样 max 0.172/avg 0.089,云速降至 ~1/6。**教训:parallax 位移公式 `wind*9*parallax` 没错,错在 wind 的取值范围——原版风多数时间在 ±0.1-0.35,不是 ±1**。
- **手持火把 wet 门 + 全亮修正(2026-08-10,用户问"持火把入水亮吗")**:原版 ItemCheck_EmitHeldItemLight(Player.cs:48997)=`(Torches[type] && !wet) || WaterTorches[type]`——普通火把入水(任何液体,含岩浆/蜂蜜)熄灭,仅水火把水下亮;颜色走 TorchID.TorchColor(style),普通=1/0.95/0.8 全亮(与放置火把同亮度)。我们两处偏差已修:①Game.ts torchOn 加 `&& !player.inWater`(Player.inWater=头部格液体>100,不分类型≈wet);②LightingEngine heldLight 0.5/0.475/0.4→1/0.95/0.8(此前的×0.5 是压暗偏差,手持会比以前亮一档=原版手感)。E2E:旱地 heldLight 生效/入水 2 帧内熄灭 ✓;lighting 51 回归 ✓。水火把(WaterTorches,珊瑚火把 5404 系)物品未实装,注释保留。
- **蘑菇组发光补 1:1(2026-08-11,用户报"蘑菇生物群系的蘑菇无掉落+问蘑菇自发光")**:TileLightScanner.cs:2938-2960 case 70/71/72/190/348/349/528/578 是独立一组——R=0、B=1、G=0.2+num11/2(num11=Next(28,42)*0.005+(270-mouseTextColor)/1000),**只抬 G**(与蜡烛族三通道 +/700 不同),349 蘑菇雕像 frameX<36 完全不发光(门控须同时压制 def.light 静态兜底,提前到播种入口判)。已加 MUSHROOM_GLOW_SHEETS(lightTables.ts)绕过静态色;tiles.ts 修正:v_190 发光色 [120,110,180]→[0,51,255](原提取错)、v_348 补漏的 light(tileLighted[348] Main.cs:9923)。**掉落同案修**:原版 KillTile_GetItemDrops case 71/72(WorldGen.cs:65697-65707)=1/40 蘑菇草种子(194,物品 key `mushroom_grass_seeds` 可放置)/否则 1/2 发光蘑菇(183,`vi_183_glowing_mushroom`)/否则无——v_71 之前 drop:null 掉不出任何东西;蘑菇树(sheet 72)不走 KillTile_GetTreeDrops(仅 5/596/616/634,:65267),fellImportedTree 曾给蘑菇树掉木头+橡实,已改逐格掷 71/72 骰。测试:tile-light-specials 补 8 用例(exportTo 种子光实测)。
