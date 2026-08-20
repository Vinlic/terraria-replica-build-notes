---
name: js-bitwise-int32-traps
description: JS 位运算陷阱：^/<< 返回有符号 int32，1<<31 为负——两次事故（seedPick 负索引崩溃/FastRandom 拒绝采样死循环）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-10T02:57:09.302Z
---

JS 的 `^`、`<<` 返回**有符号 int32**（可能为负），`1 << 31 = -2147483648`。移植 C# 位运算代码时凡结果用作索引/上界，必须 `>>> 0` 归正。

**Why:** 本项目 2026-08-10 连续两起事故：
1. `BiomeBackground.seedPick` 终局 `(h ^ (h>>>16)) % n` 返回负数 → `FOREST_STYLES[-2]` → drawSurface 崩溃 → 异常抛穿 Game.frame → **rAF 循环死亡、整个游戏冻结**。
2. `lighting/FastRandom.next()` 拒绝采样用 `1 << bits` 算上界，bits=31 溢出为负 → 重投条件永真 → **死循环卡死主线程**（走远/瞬移新区块→光照采样触发）。修复对照 `Terarria1456/Terraria.Utilities/FastRandom.cs`：`nextBelow(max)` 幂快速路径 + 溢出带等价判据 `num <= 2147483647-(max-1)`。

**How to apply:**
- C# 位运算移植一律在最终结果 `>>> 0`；`1 << n`（n≥31）直接改用 `2 ** n`
- 游戏冻结类 bug 二分时注意**假阳性**：禁用某系统后不卡可能是时序巧合（本例禁用背景层一度"验证"了错误嫌疑）；主线程忙死时 puppeteer evaluate 会超时，CDP `Debugger.pause` 抓忙循环栈是一锤定音手段（未及使用，另一会话已定位）
- 崩溃防御（兜底+一次性 console.warn 带 JSON 现场）成本极低且这次直接暴露了根因数据，值得作为惯例
- **csCompat 模块（2026-08-10 世界生成对齐批 A 落地）**：`src/core/csCompat.ts` + `tests/cs-compat.test.ts`——`(int)`→`ctrunc`（向零截断，-0 已归一）、int 除法→`cdiv`、`Math.Round` 默认→`cround`（ToEven 银行家）、`(float)`→`fround`（Math.fround，随机游走每步舍 float32 防长程漂移）。已修复实例：IceBiomePass int[] 整除（Float32Array→Int32Array）、LiquidSim 7 处均分 round→floor（系统性偏多）、计数类 5 处 round→floor、TerrainPass fround 步进。`rng.int(a,b)` 闭区间 == C# `Next(a,b+1)`（601 处调用依赖）。

- **蘑菇不掉落（2026-08-11）**：breakTile 可砍植物分支在 `st.setTile(x,y,0)` **之后**才读 `st.frameX` 判蘑菇帧（144）——setTile 清格时 frameX 已归零，fx 恒 0，蘑菇/邪恶蘑菇/血腥蘑菇（sheet 3/24/201）永不掉落。修复=清格前捕获 fx。**教训：读帧判定必须发生在任何写格子操作之前（setTile(0)/setTileSilent 都会清 frame）**；挥砍/弹幕/挖掘三条清植物路径都汇到 breakTile，单点修复即可。验证 probe-mushroom.mjs：sheet3 fx144 → mushroom_item ✓、sheet24 fx144 → vi_60_VileMushroom ✓。

- **墙面铺设全量移植（2026-08-11，用户报"无法铺设墙面"）**：此前墙面只有锤拆除、无任何铺设路径。落地=①tools/extract-wallitems.mjs 从 Item.cs SetDefaults 提 `createWall`（**124 墙物品**→vanilla-wallitems.json）；items.ts 末段自动注册/补 wallId（vi_ 命名，已存在的补字段）；②Game.tryPlaceWall 1:1（Player.PlaceThing_Walls :38937）：射程 5.5 + useTime 门 + **邻接门（四邻至少一格 active 或有墙，防悬空墙）** + wall==0 才放（TileReplacement 替换未实现）+ **FillEmptySpace(:38973)：stack>1 时四邻中"空墙且其四邻全是本墙"的格自动补铺**（原版铺墙"一笔涂一片"手感核心）；sfx dig；wallSpeed=1。墙面拆除（锤 HitTile type2）已有。验证：放置消耗/悬空拒绝/补洞/124 项注册/存档段存在 全绿。

- **三连修（2026-08-11：木墙合成/木锤拆墙/桌子放置）**：①recipes.ts 原来零墙配方——补 wood_hammer(8木)+木墙/石墙(1材→4墙,工作台,原版 Recipe);②锤子本身端到端正常(直调+E2E 真实鼠标按住均拆墙成功,2击/37t 节流)——用户报障疑似瞄准格无墙或墙前有火把:修掉 `get(tx,ty)===0?wall:0` 误挡(火把/平台/门后的墙原版可锤,实心块已被半砖分支拦截语义一致);③桌子放置一直正常——先前探针把地面铺进了 3×2 占用区导致 isActive 拒绝,是探针几何错误非游戏 bug。**教训:E2E 探针摆家具时占用区(ow×oh)与支撑行(y+h)必须分开算,地面铺进占用区=必然放置失败假阳性**。回归:合成✓锤墙✓锤火把后墙✓桌子 6 格帧 0,0/0,18/18,0/18,18/36,0/36,18✓。
