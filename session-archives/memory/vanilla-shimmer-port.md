# 原版微光实体转化系统（补齐清单 #5）

三层转化 1:1（Terarria1456 权威）：
- **掉落物**（WorldItem.cs:806-840 Shimmering / :1781-1931 GetShimmered）：
  ItemDrop 入微光（liquidType 4，顶上一格采样）shimmerTime +0.01/t >0.9 触发：
  ① 钱币 71-74 → 面额放大（银×100/金×10000/铂钳1×1e6）→ `player.luckState.addCoinLuck`
  （Luck.ts coinLuck 数值位就此接通，<1000px 距离门）；② ShimmerTransformToItem 有表 →
  换目标物品原堆叠+`shimmered` 上浮（vy -0.05 钳 -4、速度≥0.2 不可拾 Player.cs:34466）；
  不可转化物（如坠落之星 75）正常沉底不转化。wet 判定已排除微光（Collision.cs:1418）。
- **玩家**（Player.cs:27420 触发 / :11381 buff353 / :37591 免伤 / :28377 脱困）：
  浸微光（y<lavaLine）→ shimmering：frozen 封输入 + 免摔伤 + **damage() 直接 false** +
  gravity 0.15 轻浮大跳（非微光态）；timeShimmering ≥3600 或 ≥1200 且有输入 →
  `findShimmerFreeSpot`（切比雪夫圈 1..59 步 2，勿用步 2 内环——奇偶会漏一半格子）传送
  spot+(0,-2)px + 40t 无敌帧。地狱层内不生效（:11391）。
  **不能游泳是原版机制**（buff353 封输入，等传送脱困）。**2026-08-12 修复脱困卡死**：
  原版三层兜底（玩家周围→FindSpawn 出生点→主出生点，:28442-28469）+ 落点第二判是
  "下方 100px 内有地面"（IsSpotShimmerFree :28477）——旧实现只有第一层且要求紧贴
  下方一格可站，封闭洞穴中搜索必失败 → 每 20s 重试永远失败 = 永久卡住。已补兜底+放宽。
- **NPC**（NPC.cs:92502 GetShimmered）：Enemy 浸微光 90t（shimmerTransparency 0.9）→
  雕像产怪消散 / ShimmerTransformToNPC transformTo / ShimmerTransformToItem 掉微光化
  物品后消散；TownNPC 入微光 → `shimmered=true` + 回家（ai[0]=25 净效果）。

**转化表来源**：`game/tools/extract-shimmer.mjs` 解析 ItemID.cs:84/86/88/90/1098 +
NPCID.cs:4839/4841/4843 → `game/src/data/vanilla-shimmer.json`（312 物品对 + 114 NPC 对
+ 15 NPC→物品 + 29 城镇变体 + CommonCoin/PostMoonlord）；运行时 `game/src/stats/Shimmer.ts`
（含音乐盒 createTile=139 placeStyle 动态分支 + 内部↔原版 id 互查）。

**GAP 登记**（Shimmer.ts 头注释有全清单）：decraft 反 craft（需配方引擎+RecipeSets 骷髅
王/石巨人锁）、makeNPC 放生、4986 彩虹史莱姆解锁/560 史莱姆雨、3461 月相砖、微光视觉
（shimmerTransparency 半透明/dust309）、Critter 小动物入微光、联机 145/146 同步。

**渲染 1:1 修复（2026-08-12）**：①基底层四角顶点色（SetShimmerVertexColors :745-759）
= 2×2 子块双线性 multiply（Canvas2D 无顶点色的最优可达）；②sparkle 彩虹 = hslToRgb
（Main.cs:47266）1:1 + **每 hue 一条整带**离线染色缓存（multiply+destination-in 保明暗纹理，
hue 16 档量化）——**hue-rotate 对纯白 sparkle 是 no-op（CSS 饱和度 0 不受色相旋转），
旧实现的彩虹根本没上色**；③瓦后路径原版（TileDrawing.cs:4188-4191）重置整段顶点色
= 彩色叠加必须有（旧注"省略"是错的）。

回归：`tests/shimmer.test.ts` 12 探针（表抽查/luck 接通/掉落物端到端/玩家浸入+脱困/
地狱层门）。注意 vitest 全量有并行会话 flake（luck-system 聚合与 fishing Bobber.ts 中途
态、重 worldgen 用例满载偶发），单跑均绿。
