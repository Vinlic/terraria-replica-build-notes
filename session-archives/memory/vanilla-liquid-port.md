---
name: vanilla-liquid-port
description: 液体系统已一比一移植原版 Liquid.cs/WaterfallManager；attemptToMoveLiquid 异种判定语义曾致全图黑曜石化
metadata: 
  node_type: memory
  type: project
  originSessionId: 372ae608-2da7-4502-87f6-cedcc2af7bb7
  modified: 2026-08-09T05:35:24.771Z
---

2026-08-09 液体系统按 Terarria1405 反编译源码一比一重写完毕：

- `game/src/world/liquid/LiquidSim.ts` 全量重写：活动列表 + checkingLiquid/skipLiquid + 分片调度（cycles=7/单机）+ kill 清扫（阈值8）+ 7/5/4/3/2 格侧向均流 + 岩浆 delay5/蜂蜜 delay10 降速 + 地狱蒸发（y>h-200 每 tick -2）+ LavaCheck/HoneyCheck（阈值 24/32 → 黑曜石 56/脆蜂蜜 230/蜂蜜块 229）。
- 读档沉降 = 原版 WorldFile 时序：QuickWater（自底向上 SettleWaterAt 直接搬运）→ WaterCheck → quickSettle 循环至 numLiquid=0 → WaterCheck。运行时不再"主角靠近才激活"。
- liquidType 编码：本仓库 1=水 2=岩浆 3=蜂蜜（原版 0/1/2），渲染层 toVanillaType 转换。
- `game/src/render/WaterfallRenderer.ts`：WaterfallManager 移植，触发适配为"倾泻点"（液量≥160 且下方空，每列连续段取最高格）——**原版触发依赖 halfBrick 半砖系统，我们引擎没有**，这是已知偏离；将来加半砖可改回原版条件。
- `VanillaLiquidRenderer.ts` P7 内角分支曾把 left/up 边标志对调（已修，对照 LiquidRenderer.cs:342-346）。
- **大坑**：attemptToMoveLiquid 的异种判定必须是"邻居的 lava 性 ≠ 落点格的 lava 性"（Liquid.cs:250 `neighbor.lava() != tileAtXYHasLava`），写成"邻居类型≠岩浆"会让水落水旁也触发 lavaCheck，水格把自己当岩浆、全图海洋互转黑曜石。回归检查在 scripts/_liquidprobe.mjs 第 0 项（海洋 maxRun>30 且水格>5万）。
- 验证脚本：`scripts/_liquidprobe.mjs`（7 项）、`scripts/_waterfallprobe.mjs`（2 项）、`scripts/_lavaprobe.mjs`（远近岩浆颜色）。
- 模拟器直写 store.liquid 数组绕过监听，Game 每 2 tick 手动置 `lighting.liquidDirty`。

- **半砖系统**（2026-08-09 第二轮，核心）：TileStore 加 half/slope 数组；`HalfBrickPass.ts` 移植 Smooth World(L7568)/Waterfalls(L7697) 生成 pass（地表凸起+水边唇缘砸半砖，每图约 4 万格）；ChunkCache 主绘制后 clearRect 上半 8px；LiquidRenderer 移植全部 IsHalfBrick 分支（P1 103/P2 121/P3 154,173/P4 209-214/draw 382-384）——**浸润=渲染层把上方水画进半砖格**，半砖格本身不存液体；TileCollision 碰撞盒=下半 8px（主角站半砖顶 ty*16+8）；WaterfallRenderer 触发已改回原版 halfBrick 唇缘条件（此前的"倾泻点"适配已删）。大坑：IsHalfBrick 预循环"上格"是 ly-1 不是 ly+1，方向写反整条链失效。
- **双 pass 水体**：`DrawWaters(true/false)`（Main.cs:40943/42837），背景 pass 不透明画在方块层前、前景 0.6 画在方块后；曾加"浸润外扩"适配后已删（半砖原版路径就位）。
- **2026-08-09 第三轮全面审计修复**（四个并行审计代理对照源码）：
  - LiquidRenderer P3 漏了原版 L178-179 的 HasVisibleLiquid 重算 → 瀑布拖尾干格不可见（已补 else 分支）；P2 类型优先级应为先上下后左右（ptr[-1]/[+1] 是上下！L129-138，已换序）；**层级修正：背景水画在墙层之前**（backWaterTarget Main.cs:46619）、前景水画在实体之后（waterTarget L46720，水盖玩家）、瀑布在 tile 层后实体前（L47460）——修正后水色从纯蓝 (9,61,191) 变为墙透 0.6 的 (41,61,133) 才是原版观感。
  - LiquidSim：7/5 格均分补上补偿 AddWater（L502-513/553-560）、LiquidBuffer 溢出缓冲+清扫回灌、lavaCheck/honeyCheck 入口用 SolidTile 语义（半砖放行，WorldGen.cs:42370）、swap-remove 只搬 x/y/kill 保留 delay、读档沉降 cycles 不改 1（Main.cs:12251 被 !gen 门限）。
  - WaterfallRenderer：唇缘格不直落先侧移 1 格（L470 的 !halfBrick 门）、偏折计数只计反转/直落清零/≥2 翻转、扫描窗口外扩 100 格（L74-81）。
  - TileCollision：Y 落地加"新底越盒顶且旧底在盒顶上"门槛（Collision.cs:1610/1631，防半砖提前吸附）；TileStore setSlope 无条件清 half（WorldGen.cs:49174）、setTileSilent 挖除清位。
  - 审计确认一致项：LiquidSim 侧向均分全部分支公式/交互阈值/沉降蛇形/异或语义、LiquidRenderer P4-P7 逐项、瀑布触发四条件、半砖凸起五模式。
- **最终 bug 猎手轮（同日第四轮）修复**：①settleWaterAt 蛇形探测越界（原版靠 C# 越界异常兜底、JS idx 会静默回绕写错行——已加 probeX 越界视为边界+落点钳制）；②TileCollision Y 落地改取整行最高面（原版 num13 机制，防左半砖右整砖嵌地）；③HalfBrickPass.solidTile 补半砖/坡面排除（PoundTile 是 toggle，不排除会把已砸半砖切回整砖）；④模式 A/B 去掉多余的 type===0 条件对齐原版 !SolidTile；⑤waterCheck 清 buffer；⑥_liquidNow 帧首采样。瀑布"停滞格重画"与原版一致（index4 有界），不改。
- **岩浆底部变水蓝**（用户报告）：P3 只处理到窗口底部 10 行外（原版同款 L152），绘制用 visTypeA 而它只在 P3 赋值 → 底带格子 visTypeA=0 被当水画。原版靠两个掩体：drawArea 底边 +5 行（Main.cs:42900-42908）使未构建带在屏外 + LiquidCache 跨帧复用残留正确类型。我们补齐两个掩体：drawLiquids ty1+5、P1 预填 visTypeA=typeA。回归探针 scripts/_lavabottom.mjs（池底贴屏幕底边的病灶位）。
- 未移植（后续）：slope 坡面渲染/碰撞（8 条 2px 竖切条 TileDrawing.cs:974-1006）、锤子交互循环（solid→half→slope1→2→3→4→solid）、水面波纹 shader（WaveFilters/_waveMask）、LiquidBuffer/panic、半砖邻居平滑（TileDrawing.cs:1009-1044）、SaveFile 半砖位持久化。

相关：[[reference-vanilla-source-of-truth]]、[[vanilla-worldgen-passes]]

## ★ 浸润 pass 移植(2026-08-11,用户报"水无法渲染到方块透明区域,隔缝隙")
**根因**:原版背景水 pass 含【两个】子系统,我们只移植了 LiquidRenderer.DrawNormalLiquids(液体主体);完全缺失 **TilesRenderer.DrawLiquidBehindTiles → DrawTile_LiquidBehindTile**(TileDrawing.cs:3859-4193)——对每个实心方块格检查四邻液体,在方块格内画一条液体带(背景层,不透明),方块贴图覆盖其上→透明圆角像素透出液体色。这就是"水体包裹方块"的全部机制。
**条带宽度规则**(:4069-4123):仅上方有水→格顶 16×4;仅下方→格底 16×4;仅左→格左 4px 竖条;仅右→格右 4px(x=12);左右都有或半砖→整格 16 宽;深度 num6=(256-maxLiquid)/32*2 从底收。
**透明度**(:4126-4146):地上(≤groundLevel)=1.0;地下=0.5 基线(被墙覆盖时不可见,无墙洞穴才透出)。
**层序**(vanilla Main.cs 渲染目标合成:61635 backWater → 62884 wall → 62768 tile):背景水(含浸润)画在墙之前、方块之前——墙会盖住浸润条带(有墙时原版同样透出墙色),**浸润效果在无墙洞穴最显著**。
**实现**:VanillaLiquidRenderer.ts 尾部追加 drawLiquidBehindTiles(),isBackground=true 时调用。液体贴图 Liquid_N.png(16×16 纯块;水 Liquid_0=306×16 多 style 取首段)。E2E 4/4(墙格右邻有水→左缘 1-2px alpha>0);vitest 202 全绿。**遗留**:坡面(slope)浸润用 LiquidSlope 贴图未做(引擎坡面渲染未实现);微光(lt=3)跳过;TileID.Sets.BlocksWaterDrawingBehindSelf 未查表。

### 浸润 pass 修复记录(2026-08-11 续)
三个实际 bug 已修:
1. **texFor null 缓存**:首帧 ensureVImage 返回 null → Map 缓存 null → 后续帧直接返回 null 不再重试 → **浸润条带永远不画**。修:只缓存命中(`if (t) texCache.set(vt, t)`)。
2. **源矩形越界**:默认 liquidRect=(0,4,16,16) 但 Liquid_N 高度仅 16px → ry+rh=20>16 → bounds 检查 false → **跳过绘制**。原版 XNA PointClamp 自动钳越界采样;Canvas 2D 需显式 `srcH=min(rh, tex.height-ry)`。
3. **fL const 赋值**:TS 编译错,改 let。
**离屏 mock 验证**:infiltration strip 在方块右缘正确 drawImage(dx=92 区域,dw≈4) ✓;对照区无条带 ✓。vitest 218 全绿(含另一会话新增测试)。
**注意**:E2E 屏幕坐标采样极易踩坑(camera transform + getImageData 不同坐标系);离屏 mock ctx 记录 drawImage 调用参数是更可靠的验证方式。

### 非沙方块浸润调查(2026-08-11 深夜)
**Bug 4(fR 未置位)**:原版 :4070-4074 "下方+任一侧有水"时把 flag 和 flag2 **都**置 true(全格宽浸润);我们只置了 fL → 池底常见场景(下+侧有水)只画左侧 4px 而不是全格宽。修:let fR + 双置位。
**Blend 帧透明度实测**:"右开放"帧(Tiles_0/1/53 的 UV(4,0-2))右缘 4px 仅 8-16/64 像素透明(2px 深、集中在角部或中部 4 行)——**这是原版贴图的本征设计**,浸润条带(4px 宽)只能透过这 2px 深的透明区可见,效果天然微妙。沙块"大部分正确"是因为池底场景(fD+fL/fR → 全格宽)命中了更多透明像素。
**三个可见性最强的场景**:①池底(下+侧有水 → 全格宽,已修) ②池顶(仅上有水 → 16×4 横条) ③T 型/十字(上+左右 → 默认 rect 全格)。池底修复后应显著改善。

### 液体浸润实验台(2026-08-11)
`scripts/liquidlab.ts` → mainFlow.ts enterGame 挂 `window.__swLiquidLab()` + `?liquidlab` URL 参数(1.5s 延迟自动触发)。
**布局**:8 种方块(石/泥/沙/木/蓝砖/粘土/雪/泥)× 5 种场景(A 左右夹水/B 上方水/C 下方水/D 右侧水/E 全包围)× 2 列(左=无墙浸润应可见,右=有墙原版对照);行首火把标记。玩家传到测试区顶部。
**用户用法**:F5 标注模式标记缝隙 → 导出 marks JSON 给开发者。
