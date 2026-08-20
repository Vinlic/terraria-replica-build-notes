---
name: approx-zero-project
description: 近似清零工程完成（2026-08-12）——127 条普查缺口全处置、5 全仓级真 bug、AI 100%、三态终审法则
metadata: 
  node_type: memory
  type: project
  originSessionId: 372ae608-2da7-4502-87f6-cedcc2af7bb7
  modified: 2026-08-12T02:29:55.445Z
---

"近似清零"工程已完成（2026-08-11~12，用户目标 `/goal`：避免任何近似的移植，全量移植+review+补齐）。

**方法学（复用价值最高）**：双 Explore 普查代理全库 grep 近似标记（115+12 条台账）→ 按文件冲突域分波次派实施代理（Enemy.ts 串行、其余并行）→ 每批探针+源码锚点注释 → 终审复跑普查三态判定（✅1:1 / 📋精确依赖登记=合规终态 / ❌漏网回炉）。

**终态**：AI 家族 100%（521 种敌对 NPC 脚本实证零 default 兜底）；世界/核心、实体/渲染、管线（掉落/物品/食物）、gen 17 条全部 0 漏网。全量 vitest 719/719 + seed-parity 5 种子 10/10 + caves-checkpoint oracle 3/3。

**期间发现修复的 5 个全仓级真 bug**：①弹药格桩恒 0（箭/子弹永远进不了 54-57 槽）②喝药水带 32×32 近战盒砍草 ③近蜜/近岩浆合成门液体编码三支全反 ④敌弹不伤玩家（全 Boss 弹幕对玩家无伤害——hitPlayer/StatusPlayer 链+6 发射出口 hostile 化）⑤月总二阶段弹幕表死代码。另修复提取器四类缺陷（npcdrops 变量链/itemfunc SetFoodDefaults/npcjson MAX_ID/贪婪正则）。

**Why:** 此后代码库的"近似"注释应只剩 📋 型（精确登记缺什么子系统/素材/着色器载体）——若 grep 到既非 1:1 又无精确登记的，是新引入的近似，违背用户约定，应回炉。
**How to apply:** 新移植功能直接 1:1（勿留近似再补）；新素材走 terraria-assets→sprites/vanilla 管线（Projectile_*.png 先例）；敌弹必须 hostile:true+statusPlayer；掉落新规则先跑提取器验证链体完整。gen pass 改 RNG 消耗前查 caves-checkpoint 覆盖链（止于 desertentrance/deserthive——其后 pass 可自由改，早期 pass 动了会哈希漂移）。并行会话常态存在：动手前重读磁盘、只加不改。相关：[[spawner-vanilla-alignment]] [[event-system-port]] [[multiplayer-room-system]]
