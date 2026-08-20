---
name: gem-anchor-gate-port
description: 暴露晶簇178泛滥=PlaceTile锚定门缺失;琥珀循环漏空气/岩浆门;沙漠装饰放置补齐+Next(6);金标对账法
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-12T18:36:26.320Z
---

2026-08-12 用户报"四处散布的宝石"。两轮修复(全部金标 .wld 对账,seed 12345):

1. **PlaceTile(178) 锚定门缺失**(GemPasses.placeExposed):原版 num==178 分支要求四邻可贴实心格(CheckAndAdjustMultiDirectionalTile :60338,下>左>右>上,锚 tileSolid&&!solidTop,排除 Boulders+type10;坡面语义 SolidTileAllowTopSlope :60399 系),成功才放且 frameY=Next(3)*18 仅成功掷。三处 178 全走此门(地下单格 cs:20874/冰系 cs:20842/琥珀簇 cs:20901/Spread.Gem cs:3626)。修复前 4763 vs 金标 816、悬空 792→修后悬空≈0。
2. **琥珀循环漏目标格 !active+!anyLava 门**(cs:20901):实心沙岩也带 187/216 墙→命中率爆表(13×)。修后琥珀 1793→243(金标 140;腔体空气格我们 71328 vs 金标 54057 的 +32% 线性放大,腔体形态本身同形——cavity 连通域/内部率指标两边一致,勿再动 DesertPass 雕刻)。

**Why**: 探查代理双确认 DesertPass 蜂巢雕刻 1:1 无偏差(metaball 场强分层,窄缝天生),琥珀产量是 GemPasses 自己的门缺失。

**How to apply**:
- liquidType 用 LIQUID_TYPE 枚举(TileStore 导出,+1 编码水=1);新 while 必加硬上界(水中箱事故)。
- 沙漠装饰放置补齐(DesertPass AddTileVariance 第二遍):485(style×36)/751/484(2x2 底行贴 396 顶)/165(flag 地面·!flag 倒挂)/187(style 29+Next(6),横排 ×54)——金标实证锚点与帧;**187 分支的 Next(6) 两侧(JS+oracle)曾一致漏掷**,已同步补 → caves-oracle.cs 已改并再生两份金标(deserthive 起全变=预期)。
- UpdateDesertHiveBounds 补齐:GenState.desertHiveHigh/Low/Left/Right(PlaceClustersArea flag2 格收缩)→ BuriedChests 沙漠箱分层 cs:36084 用它(曾误用静态矩形±10)。
- **已验证(2026-08-12)**:oracle 同步(装饰放置+Next(6))并再生两份金标(deserthive 起全变=预期);caves-checkpoint 双种子 **terrain→underworld 全绿含 deserthive/desertdone:wall**——装饰落格与原版逐位一致。corruption 起仍红=并行会话在移植 CorruptionPass(他们的在途状态),非本批改动。手抄 JSON 会错(rocksclay 67bc7e98/dirtlayer 501f3b5d 被 diff 抓回)——金标安装一律 cp+diff 校验。
- 对账工具 tests/_gem-dist-audit.test.ts + tests/_fullgen-smoke.test.ts(防卡死冒烟,两种子全链<25s)。golden type 是原版 id,内部 id 要换算。两者及 tests/_amber-tree-struct.test.ts 均默认 SW_AUDIT 门控 skip,勿拖慢全量套件。
- **琥珀贴图投诉已闭环(2026-08-13)**:根因=悬空琥珀簇(已修);琥珀树 589 结构终验 9 棵全带干/顶/枝正确帧 + 样式映射 28 贴图色值实测吻合——按构造渲染正确。后续 Next(6) 掷骰归位后琥珀簇 160 vs 金标 140 收敛。
- 关联 [[liquidtype-plus-one-encoding]] [[ocean-sand-hellfort-parity]]
