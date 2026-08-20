---
name: pyramid-plate-coin-portal
description: "金字塔无压板=原版行为(Pyramid()本体+wiki三方实证,压板在全局Traps pass且wall==0门进不了金字塔);真缺口=瓦罐钱币传送门1/125已全链补齐(AI_094+potCoinMul+地狱罐hardmode门修正)"
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-14T00:47:31.733Z
---

金字塔压板调查 + 钱币传送门补齐（2026-08-14，用户："金字塔里的电子机关好像缺乏压板放置？"）。

**定性：原版金字塔本体无压板/陷阱/导线（非缺口，三方实证）**：
1. 代码：`Pyramid()`（WorldGen.cs:27816-28129）只放 AddBuriedChest(848/857/934 三选一)+
   PlaceSmallPile×1-9+PlaceTile(91 横幅)×4+PlacePot 全宽(style 25-27)——全文无 135 压板/wire 调用；
2. wiki（terraria.wiki.gg/wiki/Pyramid）全文内容物=横幅/陶罐/硬币藏匿/宝箱，无陷阱记载；
3. 我们的 pyramid()（StructuresPass.ts:685-710）同构。压板真实来源=全局 Traps pass
   （cs:18769，placeTrap 放压板135+陷阱137+导线；**probe 起点 wall==0 门→金字塔走廊墙34进不去**）
   与 PlaceSandTrap（墙187 地下沙漠）——我们 TrapsPass.ts 均已 1:1（wall===0 门+w*0.05×1150
   探针+ocean 回避逐项核对通过）。用户观感"缺压板"实为原版行为。

**顺手补齐的真缺口：瓦罐钱币传送门（WorldGen.cs:57186-57194）**：
- 触发：SpawnThingsFromPot 顶部 `range=500/((num+1)/2)`（num 为过 `(n*2+1)/3` 变换值 :57163）
  → 最近玩家 `RollLuck(range)==0` → 弹 proj 518 CoinPortal 并短路全部常规掉落。
  金字塔罐 style25-27 n=10→range=**125**（wiki"金字塔罐 1/125 全游戏最高"精确对上）；
  普通罐→500；地狱罐 hardmode n=4→250。载入期 isGeneratingOrLoadingWorld 门=player 未建跳过。
- 实现：`src/entities/CoinPortalProj.ts`（AI_094 四阶段机 1:1：1-40t 淡入 α-=5/v×0.85/==40
  掷 ai1∈{10,15,30}→41-60 悬停→61-210 每 ai1 tick 喷金 coin item73（速度=UnitY 旋随机×(3,2)
  ×(0.5..1)−(0,1)）→211-239 缩淡→240 Kill；4 帧竖排/尘 246 环形/light×0.3）；
  Game.ts `potCoinMul(style,hardMode)` 导出helper+potLoot 顶部接线。
- **顺带修正**：style 28-30 地狱罐乘子曾无条件 ×4（原版 hardMode 才 4，肉前=1）。
- 测试 `tests/coin-portal-pot.test.ts` 5/5（乘子全档/range 三档/中心定位/ai1=10→15 币/ai1=30→5 币）。

坑：并行会话同时在改 Game.ts（编辑时两次"modified on disk"警告）——大文件 Edit 前必须重新
grep 定位最新行号。全量回归 10 败均并行领地（caves/world-hash/fishing/dungeon-walls/hive/
sky-invariant=任务#15 加 pass 在途；shimmer/cracked-brick 已消）。
