---
name: shimmer-decraft-pickup-fix
description: 微光分解浮出拾取链两个真bug(恒加速上浮永不减速/拉动死锁);探针7断言;自建湖必须封底防LiquidSim漏干
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T07:30:35.120Z
---

**第二轮(用户报"有时分解有时不行/产物无限横漂")两真 bug 已修(2026-08-13 下午)**：
①shimmerWet=**Collision.shimmer 盒判定**(LiquidCollision :1600-1655:包围盒擦任一 liquid>0
微光格即真,坡面格另判上格)——旧实现中心单格>30,浅液面/盒缘擦液时 Shimmering 根本
不跑="有时能分解有时不能"根因;②vx 摩擦(:927-932)是**通用段**(shimmered 也执行),
曾误放非 shimmered 分支→decraft 散射初速(n×(1+n·0.05)±:1.05/-2.2/3.45…)永不衰减
=产物无限横漂+恒>0.2 永不可拾。Shimmering 顶格采样(Center.X/16,position.Y/16−1)
与调用门(shimmerWet&&!shimmered :547-549)均与原版一致,勿"修"。浅液 liquid=40 时
液面段仅上部 ~3px((256−liq)/32×2),测试盒顶须压入该段才湿。decraft 数据层恒定
(铜镐3509 任何月相/旗标→木材12+铜矿9,数据层非"有时"的来源)。shimmer.test 23 条;
白光尘计数用例与 save/buffs 并发偶发 flaky(单跑稳定,余量 80 vs 期望 8)。

2026-08-13 端到端验证"微光湖扔物分解→浮出→自动拾取"，顺手修了**两个真 bug**（玩家可感知）：

**Bug1 上浮永不减速**（ItemDrop shimmered 分支）：我们恒 `vy-0.05 钳-4`。原版三分支（WorldItem.cs:515-536）：①shimmerWet→加速上浮；②干态但**下方 2 格内有微光**（微光柱上方）→继续上浮；③否则 `vy×0.9` 衰减悬停——速度 <0.2 才可拾。修后产物浮出湖面减速悬停 ✓。

**Bug2 拾取拉动死锁**：原版 GrabItems 顶部速度门（Player.cs:34466）同时拦**拾取+拉动**（快的 shimmered 整体忽略）；且 CanPullItem 分支先 `shimmered=false`（:34498）——拉动开始即解门，按普通物品吸走。我们此前只拦拾取不拦拉动+拉动不清旗 → 拉动加速把物品锁死 ≥0.2 永不可拾。两处已 1:1。

**已验证链**（scripts/_shimmer-drop-probe.mjs 7 断言，私有 5201 已收）：抛出公式 4×facing+vx/-2 → 浸泡 shimmerTime 爬升 → decraft（探针正测=**木剑 vid 24 → 木材×7**，与原版配方 Recipe.cs:6794 逐字吻合；曾用木墙×3→木材×30）→ 悬停 → 自动拾取入包 vi_9_Wood → 金币 73→coinLuck 9999（分支序钱币最前 ✓）。

**武器入微光的完整语义（用户问"武器也有效果?"——原版核对 2026-08-13）**：GetShimmered 无武器专属分支，效果=通用三层：①转化表命中（ItemID.cs:84 CreateIntSet——含**跨世界金属族转化对**如 135↔5365/1379↔5367 钴钯链、5295↔5519 双向对、火把族→5353 单向）；②decraft——**一切 IsCrafted 武器分解回材料**（木剑24→木7/铜弓3504→木7/金剑3520→金锭8/泰拉刃1185→英雄剑10/天顶剑5115→夜明20，引擎抽验全对）；③无配方且不在表（掉落型武器如 470 鞭炮/536）→滞留无效果。**陷阱：27 是橡实不是木锤**（查询标错名差点误报缺口）；引擎 transform 返回 0=原版 -1（无转化）语义一致。

**探针坑**：①自建微光湖必须 **S+4..S+5 封实心底+侧壁**——地下 40 格常挨天然洞穴，不封 120t 液体被 LiquidSim 漏干（液面 255→0 实测）；②玩家钉位勿跟随掉落物重钉（间隙恒定永不触）；拾取判定间隙要 <42px 或贴身；③金币阶段玩家须在币 6 格外（>42px 否则币被 pull 直接捡走不走 luck）；④新探针引导用 `/?play=small`+waitForFunction（主菜单已换 vui，旧 select 引导作废）；⑤掉落物模拟有冻结距离，钉玩家别超 ~15 格。相关 [[vanilla-shimmer-port]] [[thrown-physics-fix]]
