---
name: shimmer-audit-status
description: 微光对齐全景:生成 pass 1:1(已有 C# oracle checkpoint 金标对账)/转化系统/宝石树全链/月相砖已接;生成侧遗留已闭环
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T16:33:51.765Z
---

2026-08-12 用户问"微光湖生成机制对齐了吗"→ 三层核查 + 两缺口处置。

**已 1:1(核验过,勿再怀疑)**:
- 生成:ShimmerPass.ts = WorldGen.cs:15256-15308(选位+两级重掷)+ ShimmerMakeBiome :34889-35083(双 variant 石壳/腔体/微光液 127/255/石笋柱)+ Opening :35095-35125 + PlaceTight 钟乳石帧族 :38329/38371 + aether 宝石树 500 采样;管线槽位 = 原版注册序 Lakes(14613) < Shimmer(15256) < DirtWallCleanup(15310)。
- **宝石树全链(头注曾过时称"静态种植",实际全接)**:砍伐 = Game.fellImportedTree(KillTile_GetItemDrops :65754-65802+SetGemTreeDrops:每格 1/10 宝石/9/10 石块×1-2,干基帧 frameX≥22&&frameY≥198 50% gemcorn 4851-4857);种植 = vi_4851-4857 tile v_590;再生长 = Game.growSaplings(590 地下硬门+1/5,growGemTree 自带 GemTreeGroundTest 石/苔+WallTest 洞穴墙 1:1)。
- 转化:Shimmer.ts(312 物品对/114 NPC 对,tools/extract-shimmer.mjs)+ 钱币 luck + 掉落物入湖端到端 + 玩家脱困;tests/shimmer.test.ts 12 例。

**2026-08-12 补接**:3461 月相砖动态分支(ShimmerTransforms.cs:108-125):getTransformToItem/canShimmerItem 加可选 moonPhase 参,表 LUNAR_BRICK_TRANSFORM=[5408,5401,5403,5402,5406,5407,5405,5404](MoonPhase 枚举序=Main.moonPhase 0-7,Terraaria.Enums/MoonPhase.cs);ItemDrop.updateShimmer/getShimmered 传 game.world.clock.moonPhase(我们 moonPhase 0-7 与原版同域,`%8` 自增)。
**review 补漏(同日)**:月相砖转化目标 5401-5408 中 **5402/5406/5408 三件物品未注册** → 转化到对应月相 `internalIdOfVanilla→-1` 静默丢物;补注册三件+全 8 件接 `tile:` 放置链(createTile 669-676,Item.cs case 5401-5408,tiles v_669-676 已注册)。测试升级为 8 相位全断言+目标物品存在性(`internalIdOfVanilla(LUNAR[ph])≥0`)。**教训:动态转化分支接入时必须核每个分支目标物品的注册存在性**。

**遗留闭环(2026-08-14)**:生成侧 checkpoint 金标已建——caves-oracle.cs 扩 Gems(15109)→GravitatingSand(15198)→OceanCaves(15228)→**Shimmer(15256)** 链（Checkpoints: gems/gravitatingsand/oceancaves/shimmershell/shimmerpillars/shimmeropen/shimmer + RNG 流位置指纹 "stream" 段 + shimmerX/Y/dungeonRight 头字段）;tests/shimmer-checkpoint.test.ts 双裁决通道:①全链(beaches 流分叉时让位)②**状态恢复**——oracle `SW_DUMP_SHIMMER=1` 落 pass 前完整网格+UnifiedRandom 态(gzip 进 tests/golden/shimmer-state-*.bin.gz),JS 直跑 runShimmerPass 对账,**不受上游 pass 并发 WIP 影响**(多代理并发期最稳的裁决位)。金标暴露并已修 TreePass.growTreeWithSettings 两处掷骰偏差(见 [[gem-tree-grow-draw-order]]):cs:30906 基座帧骰无条件掷(旧内嵌 if(tL||tR),以太石地恒漏掷) + cs:30595-30596 帧变体骰先于枝型骰(旧序反,枝型取错流位);oracle GrowAshTree/GrowGemTreeFn 同步修正后 caves-chain 金标需重生成(underworld 起哈希变)。L2 全图种子金标仍待用户产原版 .wld(见 [[seed-equivalence-plan]])。

相关:[[seed-equivalence-plan]] [[vanilla-worldgen-passes]] [[save-parity-port]] [[gem-tree-grow-draw-order]]
