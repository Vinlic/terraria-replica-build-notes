# OOOOO 批：三链 #61/62 水箱/海底箱带清零（trySlope 压平+落坡 / 丛林箱回退 KillTile 化）

2026-08-20。任务接 JJJJJ 移交：清零 12345/s22222/m20260811 共同首差 #61/62。

## 根因一：AddBuriedChest 下落段 trySlope 门序错位（BuriedChestsPass.ts placeBuriedChestInner）

vanilla 逐行序（cs:35931-36004）：shimmer/幼虫 → **trySlope 门（cs:35951-68，
谓词 active && tileSolid && !tileSolidTop——不含 slope/half！）** → ±30 盒
（style17，坠落途中任意实心行含半砖行都查）+ 压平 (i-1,k)/(i,k) 顶坡 →
±2 巨石盒 → SolidTile 判定。压平后 SolidTile 即真 → **箱落在坡上**。

JS 曾把盒+压平塞在 `if (solidDrop(i,gy))` 内（solidDrop 要求 slope==0）→
(i,gy) 顶坡格穿落，箱体反撞斜坡格被 PlaceChest 拒（occ 拒因：`occ(3857,354)
t22 sheet53`）→ 海底箱/水箱坡上落位全败 + 重掷流滚雪球（12345：vanilla 第 3
趟 (3857,349) 落坡置 (3856,352)，JS 败 22 趟后置 (3858,353)）。

**金标指纹**：dump61↔62 段间 delta 的箱腿行 `sl 1/2>0` 压平格
（(3857,354)/(4013,318)/(329,501)/(282,353)）。

**修**：门按 vanilla 序提前；slopeL/slopeR 改行内变量（vanilla num2/num3
每行重置——半砖行压平的 (i-1,k) 坡不回填，旧循环外单份会落定行误回填）。

## 根因二：丛林箱失败回退裸清 ≠ vanilla KillTile（JungleShrinePass.ts）

vanilla cs:17320-23：首败 → KillTile 3×3（尾 SquareTileFrame 级联**整组杀
越框多格件**：雕像 2×3 六格全灭=框内 2 直杀+框外 4 经引擎 check2xX；心 2×2 经
CheckOrb）→ 压平 3×4 → 原地重试。JS 曾 setTileSilent(0) 裸清：框外残格存活 →
二次放置撞残件再败（丢箱）+ 心/雕像孤儿格 + 重试后掷流后移（神龛 off 位错）。

**修**：回退清场改 killTileChest（尘掷走 RRRR 表——orb/雕像族 0 掷）+ 引擎
未派发的 **CheckOrb 族 {12,31,639,696} 补件 checkOrbKF**（cs:54187 1:1：锚
反解 frameX∉{0,36}→x-1/frameY≠0→y-1、2×2 完整性、支撑门仅 12/639、
destroyObject 重入闸、生成期掉落段不跑）沿九宫补扫。只挂丛林箱域（引擎
FinalCleanupPass.ts 禁区未动，沿 JJJJJ 屋域补件先例）。

## 方法论增量

- **金标 dumpN↔N+1 段间 delta** = vanilla pass 精确动作清单（箱位/压平/连带杀）。
- **__swChestDbg 失败原因流**（occ/legL 逐格）+ __swChestEv 尝试流 + RNG 原型
  包装掷流 = 定罪三件套（探针 _ooo61 模式，用毕即删）。
- ★坑：trySlope 调用面全集=水下箱段(恒 true)+水箱环(海洋带)——其余箱族不受
  门序影响；s 链 #61 的"水箱债"归因是错的（实为丛林箱域）。

## 验证与遗留

四链 mile8：12345 #62→#73（单格 Spreading_Grass 自债）、s #61→#63（蜘蛛波
W=28.5k=HiveSpider 自债，未随本案自愈——输入 dump62 已零）、m #62→#69（岛屋
单格自债）、9293480 零回退。液体 60/60；worldgen 域红零新增。遗留：引擎
CheckOrb 派发臂仍缺（丛林域补件承载）；supportOk 平台正规顶帧例外略（备案）。
