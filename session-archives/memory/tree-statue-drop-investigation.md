---
name: tree-statue-drop-investigation
description: 砍树掉靴子雕像排查:1444刀+400摇全净(现build无泄漏);靴子雕像=item 462无任何生产者;斧本不能破坏雕像(pick专属);最可能=地上旧掉落物误归因
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-18T06:23:17.254Z
---

# 砍树掉"靴子雕像"排查（2026-08-18 用户报障，未复现）

**排查矩阵**（全部干净）：
1. **掉落来源审计**：item 462 Boot Statue（createTile=105 雕像族 117 件之一）
   在全仓**零生产者**——TreeShake 表 40+ vid 逐一 `VI()` 解析验证（含
   832/933/3360/3361 魔杖族、5629 弹弓、4366 树液、水果 20 件、钱币 71-73、
   1809 臭蛋）；killTileGetItemDrops_Tree 返回值域干净；vanilla-npcdrops 全表
   无 item 462 规则（含全部摇树小动物 vid）；spawnNpcByVanilla/
   spawnTreeShakeNpc 失败静默 return 无物品兜底。
2. **浏览器探针三连**（_treechopdrops.mjs，spawnDrop 全拦截）：
   ①40 树满力一刀倒（317 件全 Wood/Acorn/Ebonwood）；
   ②80 树低斧力 1004 刀（摇树掷骰活跃，382 件含 1/100 弹弓、1/300 叶魔杖
   等全合法稀有项）；③全图 400 树纯 tryShakeTree 各一摇（30 件全合法）。
   雕像族（createTile=105）零命中。
3. **机制排除**：斧头**本来就不能破坏雕像**——雕像 def pick:0/axe:-1，
   toolMatchesTile 斧档只认 TILE_AXE_SHEETS → 用户即便瞄到树旁雕像也砍不动。

**最可能解释（非 bug）**：
- 树基有**更早掉落的雕像物品**躺在地上（雕像=镐挖产物；地下雕像常见），
  砍树掉落物在同点落地、拾取时一并入包 → 误归因给树。
- 或用户玩的是修复前的旧构建（斧族/摇树批 2026-08-17 才落）。
- 若可复现：需要存档/种子+当时手持物再定位。

**How to apply**：同类"掉错物品"报障的排查套路=①目标 item 全仓生产者
grep ②来源系统表逐一 vid→VI() 解析 ③spawnDrop 全拦截探针三档压测
（一击倒/低力多刀触发全掷骰/纯入口直调）。
