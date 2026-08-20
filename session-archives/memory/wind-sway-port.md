---
name: wind-sway-port
description: 原版风摆动系统 1:1 移植（相位钟+GetWindCycle+WindGrid 扰动+七类摆动图块摘出烘焙逐帧绘制）
metadata: 
  node_type: memory
  type: project
  originSessionId: d6caec24-1cc3-4182-bea5-29046ee459cf
  modified: 2026-08-12T04:02:01.381Z
---

# 原版风摆动系统移植（2026-08-12，用户问"树木花草随风摆动怎么做到的"→令完整实现）

**机制全貌**（TileDrawing.cs）：输入=`Main.WindForVisuals=windSpeedCurrent`（天气系统现成）；四个相位钟按风速加速（树 1/240×(1+2n)/草 1/180×(1+4n)/向日葵 1/420×(1+5n)/藤 1/120×(1+0.4n)，n=lerp(0.08,1.2,|w|)）；`GetWindCycle(:7800)`=cos(钟×2π+**x*0.5+⌊y/100⌋*0.5 相位偏移**)×0.5+wind，乘 lerp(0.08,0.18,|wind|) 无风门（<0.08 恒静止），y≥worldSurface 恒 0；绘制=position+偏移+绕锚点旋转（草 dest=(px+sway,py+|sway|) pivot 底中 rot=sway*0.1；树冠 off ×2/|×2| rot 0.08；枝 offX 条件式 rot 0.06）。

**实现**（`src/render/WindSway.ts`，全部行号注释在文件头）：
- **WindGrid.cs 1:1**：Int32/Int8 三数组，移动玩家盒打格（静止不打），`GetWindTime` 返回**elapsed**（刚标记=0！）；push=三角波脉冲（前半 (total-t)*force*dir 后半 t*force）。**原版怪癖保留**：未标记格 Time=0 → 开局前 threshold 帧全图幽灵脉冲。
- **路由集合**（TileID.cs :263-275+WallID.cs :54）：SwaysInWindBasic 23 种→Basic 逐格；184→Directional 四向；MULTI_GRASS 21 种（27 高草 2×5/233 双形/519 香蒲底锚上数）；VINE_THREADS 52 族→链式下垂（每段绕上段末端 (rot+π/2) 旋转向量推进）；549 反向链；MULTI_VINE 16 种→绕顶心摆（下部摆幅大 hFrac=(j+1)/sizeY，**与草相反**；wc 含 highestWindGridPushComplex(60,1.26,3,true)；不在风口只余扰动）。**例外**：530 fx≥270 / 705 fx%486≥270 / 227 排除帧 {204,238,408,442,476} 不摆（原版走普通路径）→ swayBakeSkip 照样烘焙。
- **渲染架构**：摆动图块从 ChunkCache 烘焙摘除（main pass swayBakeSkip + pass4 只留棕榈干/蘑菇顶 72 原版不摆），Renderer 2c 后 `drawWindSwayTiles` 逐帧画（视区±8 格边距；sway=0 时直绘不带变换）。树干仍在烘焙层。**drawTreeCell 加 sway 参数**（VanillaTiler，anchor0/1/2 三套 pivot 公式注释在代码）。
- **接线**：Game.fixedUpdate（advanceAnim 旁）`windSway.update(wind, player盒, w, h)`；Options.swayInWind（默认 true，Settings 游戏页开关，原版 SettingsEnabled_TilesSwayInWind）；getWindCycle/update/scan 三处读 options。

**Review 修复六项（2026-08-12 用户令 review，全对照源码）**：①**分发顺序**对齐 PostDrawTiles :428-436——原版分家族有序调用 MultiTileVines→MultiTileGrass→Grass→Directional→**Trees**→Vines→ReverseVines（树冠盖草），行扫描单遍会草盖树冠 → 改三遍 sweep（1:吊挂+多格草 2:草+四向 3:树+藤链）；②**WindGrid 只按视区建格**（EnsureWindGridSize :7899 传 GetScreenDrawArea，取模环形寻址 tileX%width 是 WindGrid 原文）——全图建格 6400×1800≈70MB 是浪费，改视区尺寸+slot() 取模，Game 传 viewTW/viewTH；③**树冠 fx=0 顶冠变体回归**——原版 fx>=22 门是因为 fx=0 走 DrawSingleTile 普通路径，我们的 drawTreeCell 约定 fx=0 也是冠（旧 pass4 isCrown=fy>=198 画过它）→ overlay 判定改 fy>=198 任意 fx，否则 fx=0 冠全图消失；④MultiVine 698 的 offX(-10) **同时作用于 dest**（原版 dest=vector3+offSet+(0,offY)，offSet 不只是 pivot）；⑤平台判定用 def.platform+非半砖+坡0（IsBelowANonHammeredPlatform :38315）；⑥521-527 族原版 num=0 且 flag=false → **完全静态**（非"只无旋转"），rotFactor=0 早退直绘。

**验证**：tests/wind-sway.test.ts 14 条（钟加速/无风门/相位/y 段同相/三角波/幽灵值怪癖/inAPlaceWithWind 液体墙/烘焙摘除例外）；冒烟 `_windsway-smoke.mjs`：静态可见 575/576px、无风变化率 0.42 vs 高风 1.0、玩家扰动 6/8、树冠摆动 ✓、p50 8.3ms、零 pageerror。

**二轮全量补齐（2026-08-12，用户令"低可见度的也要实现，缺失子系统补齐，1:1 复刻"）**：
- **MultiTileVine 变体表全量**（:9430-9532）：34/126 的 key=fy/54+fx/108×37 与 42 的 fy/36 两个大 switch 逐 case 移植（num3 覆盖/num5 Y 系数/num2Mul 旋转缩放/flag2 pivot+16 顶行静止）；95 族=1/0；591/592 nx=0.5,ny=-2（592 的 Glow_294 alpha=0 恒不可见=原版事实）；698 nx=0.5,offX-10；91/465 默认 -4。**注意原版 num4(vector4.X) 是死代码**——draw pos 只用 Y 分量。
- **glowmask 族**：634 灰烬树冠/枝 Glow_316/317（drawTreeGlow——尺寸实证 Glow_316=Tree_Tops_13=354×98、Glow_317=Tree_Branches_13=84×126 同帧坐标直用）；基础草 656/701→Glow_329 白×mouseTextColor 脉冲、637→自身贴图 Lerp(White,油漆,0.75) 重绘；27 香蒲同贴图 fy+74 白色重绘（flag2 族）。drawCell 加 glow 回调（主贴图后同变换内执行）。
- **落叶子系统**（`NatureParticles.ts`）：GetTreeLeaf（WorldGen.cs:29540 1:1——树型直选/草型映射 910-919/中空树 917+MAP/通用 x%6 错帧 1113-1121）+ EmitTreeLeaves（排除 -1/912/913/1278、特殊叶频率减半、枝 ×3、地下 10000、分支位置偏移表）+ UpdateLeafFrequency 档位表×7 尾乘 + **Gore_UpdateLeaf 1:1**（vy 兼相位累加器走 (−sin,|cos|) 圆弧+地表风×4、碰撞 vy=-1 转滑移褪色支、液面浮叶/岩浆烧叶、SpriteFrame(32,8) 行组循环）。贴图 Gore_910-925/1113-1121/1248-1257（53 张 gore+5 glow 入 vanilla-atlas MISC）。
- **滴水子系统**：EmitLiquidDrops（冷却 rand(num*2)+区域查重矩形+水型映射 dripGoreFor：12→1147/13,14→706/>1→706+s-1/374→716/375→717/461 群系 943·1160-62/709→1383）+ **Gore IsDrip 状态机 1:1**（0-4 蓄滴随机等待+上方活性消亡→frame5 生下落子滴(9)→7-9 加速 clamp[0.5,12]→碰撞/入水转 10-14 溅落；943/1160-62 alpha 恒 0、地下 100 地表 0）。
- **药草成熟交换**：isAlchemyPlantHarvestable（WorldGen.cs:66198 1:1，style0 昼/1 夜/3 血月满月夜/4 雨或云/5 地下雨外 t>40500）→ 83 换 84 开花贴图（basic+directional 两路径）。
- **remixWorld**：getWindCycle/inAPlaceWithWind/藤段计数/药草 style5 全部翻转门（读 world.remixWorld，当前引擎未落该字段=恒 false 语义就位）。
- **LitNature 晨昏光效**（NextNatureRenderer :105-170）：SideFlags 真相=着色器输入非几何裁剪（非着色器回退=普通直绘=我们原行为）；可见性公式 1:1（昼晨窗 1200-7200·0.3/昏窗 43200-53400·0.4²、日食清零、×0.4、太阳地平线因子）+ Canvas 加性暖色光晕近似（全屏非仅植被=近似点，vis 上限 0.16 极弱）。
- 测试 26 条（变体表逐 case/药草/GetTreeLeaf 草型/错帧/水型映射/LitNature 窗口/落叶频率档位）；冒烟补 leafPeak（高风 3s 峰值 29-50 只）。全量 718/719（dungeon-spawn 失败=用户 09:53 在改 Enemy.ts，与本模块零耦合实证）。

**坑**：
- 冒烟采样区勿含玩家精灵/天空（云漂移污染 hash）——玩家停目标左 6 格、用**变化率**断言不用逐帧相等；出生点可能无草→树冠代位采样。
- HMR 双实例：并行编辑期 evaluate 内 `import('/src/render/WindSway.ts')` 与 app 实例分裂（?t= 查询串），gate 开关的浏览器级断言不可靠——语义归单测。
- **滴水溅落音（三轮接入，用户令"音效接进来缺啥补啥"）**：Gore.cs :971-984——SoundID 39=Drip（SoundID.cs:99），落地 variant rand(0,1)（Drip_0/1）入水 variant 2（Drip_2），位置 +8；**flag4 水型（716 蜂蜜/717/943/1160-62）静音**。NatureParticles.onDripSplash 钩子（Game.afterWorldLoad 注入 sfx.playFiles + preloadFiles(['Drip_0','Drip_1','Drip_2'])，destroy 摘钩+clear）；**素材坑：public/sounds 原先只有 Drip_0，Drip_1/2 从 terraria-assets/Sounds 补拷**。测试 nature-particles.test.ts 3 条（干/湿/flag4 静音——mock TileStore 注 frame9 滴 60 tick 落地）。

**四轮修复（2026-08-12，用户报"绿树掉黄/紫叶+暂停仍喷叶"→整体 review）**：
- **叶色根因×2**：①GetTreeLeaf 的 switch(t.type) **无 default 分支**——未知草型 passStyle=-1 不出叶；我错把 default 映到 1113-1121（中空树 style20 彩叶）→ 所有树掉彩叶；②grassSheet 取错了——scanTreeType 返回的是 style 序号（-1/0-13）非草 sheet，必须取 **树底地面 tile**（`st.type[idx(grassX, scan.floorY)]`，原版 t=Main.tile[grassPosX,floorY]）。修复后森林=910 绿/雪=911/沙=915·916/神圣=919；109/492 中空树取 style!=20 支（917-925，style20 支依赖 GetHollowTreeFoliageStyle 种子派生=罕见，从略）。**合法彩叶**：樱花树 596→1248 粉、黄柳 616→1257 黄、宝石树 583-589→1249-1255——看到这些是原版正确行为勿误报。
- **暂停门**：原版 EmitTreeLeaves 有 `_isActiveAndNotPaused`（=FocusHelper.AllowTileDrawingToEmitEffects）门——加 `windSway.active`（Game.frame 每帧写 !paused；粒子物理已随 fixedUpdate 的 !paused 天然冻结）。EmitLiquidDrops 原版**无**暂停门（暂停时蓄滴继续、gore 冻结）=保持。
- **fx=0 顶冠变体**：原版 DrawTrees 门是 frameX>=22（fx=0 走普通路径=静态不摆不出叶）→ isVariantTop 静态化+免喷（我们 drawTreeCell 约定仍画它）。
- **棕榈 323 冠不出叶**（DrawTrees 323 块只画不喷）——此前误喷。
- **滴水锚点 tile 永不绘制**（主循环 :694-698 `continue`）：373/374/375/461/709 = water/lava/sand/honey/shimmer drip——原版**不可见**纯喷滴源；我们烘了 0.05 透明块=视觉缺口 → `NO_DRAW_SHEETS` 并入 swayBakeSkip（minimap 不受影响，地图色表另走 MapHelper）。
- **探针坑再犯**：改 NatureParticles 触发 HMR → 探针 `import()` 双实例读到空数组——Game 加 `window.__swNatureParticles` 调试桥（EmoteBubble 同款教训第 N 次）。
- 验证：单测 30（含未知草型→-1/中空树→917-925 修正）；冒烟 leafGores=[910,1257] 全合法族 + **pauseGateOk**（paused 1.2s 零新叶）+ 零 pageerror。

**五轮终审（2026-08-12，用户令"review 完整性+可靠性"）修三处**：
- **滴水 frame4 等待**：原版 frame==5 特例(16+Next64)在 frame<=4 块内**不可达=死代码**，我误挪到 frame4（脱滴慢 ~0.3s）→ 删；frame4 用基础等待 4。
- **藤链相位/消失**：原版 CrawlToTopOfVine 爬到**藤真顶**（可在视区外）——我只从可视首格起链（长藤屏缘错拍）；且扫描门 above-not-vine 在藤顶超出 ±8 边距时**永不触发=整藤消失** → drawVineStrip 内加上爬（≤80）、反向藤加下爬、扫描门补"视区边缘格兜底"（仍整藤一次）。
- **树族覆盖审计 ✓**：TREE_SHEET_STYLES{5,596,616,634,583-589} ≡ TREE_SWAY_SHEETS−{323}，棕榈/蘑菇(72) 各自烘焙——pass4 砍除后无孤儿树冠。
- 终态：单测 30/30、冒烟全绿（叶色合法/暂停门/性能 p50 8.3ms/零 pageerror）、全量 817 中 3 失败全归用户并行 WIP（caves-oracle×2+深空树）。

**已确认偏差清单（终态）**：LitNature 光晕是 Canvas 近似（原版像素着色器，全屏 vs 仅植被）；vine 链 SideFlags=着色器输入，非着色器回退=直绘（我们等价原版回退）；651/652 锚点去重原版 overdraw（视觉等价）；落叶 landed 支液体浮叶简化锚点（无 rotation 对齐）；中空树 style20 支（1113-1121 彩叶）未接（GetHollowTreeFoliageStyle 种子派生罕见景观）；藤链行走上限 80 段（原版到 maxTilesY，>80 段超长藤截断）。

**回归归属**：wall-creeper AI_040 失败=用户并行编辑 Enemy.ts（08:46 在改）非本轮；waterfall-draw.test.ts 缺参类型（用户 01:01 WIP）已机械补类型解锁 tsc——**npm run build 仍被用户 _ghost/caves-checkpoint 草稿挡**，出 dist 用 `npx vite build`。

关联 [[vanilla-ui-port]]（renderEnv/天气）[[sandboxworld-project-setup]]
