---
name: gap-port-master-batch
description: 缺口全量移植批:权威台账14项10核销(buffImmune/礼袋/StatusPlayer48型/附近箱/渔夫套/隐身/冰刀/浮漂饰品/magmaStone/PortalGun)+接线纪律
metadata:
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-13T13:19:49.497Z
---

缺口全量移植批（08-13 晚，/goal「缺口和未实现系统进行全量移植」）。流程：权威核验代理产台账（27 项活体验证，wiki-mechanics-audit 文档大面积陈旧——抓钩/坐骑/旗帜/BlockSwap/CultistRitual/岩浆钓/狙击镜/回旋镖-长矛-悠悠球 1:1 均已实装）→ 3 代理+主会话分领地并行 → 接线清单纪律。**105/105 绿**。

## 已核销（10/14）
1. **buffImmune 体系**：Buffs.ts `immuneVanilla: Set<vanillaBuffId>` + apply 门（AddBuff :5052）；Player equipStats 扫描累积 IMMUNE_ACC 全表 17 件（885-893 单免/901-904 双免/1612 十项/1613 十一/1921 冰寒冰冻/3781 石化/5354）；黑曜石皮 buff→免 24；buff 103 族授予 24/323/67 依赖登记
2. **礼袋开启**（代理）：vanillaOpenBags.ts 四方法保序保链（OpenPresent 十六门兜底 0.470 实测锚定/GoodieBag 19 套/HerbBag 317≠316 顺序对调）；UI 右键门 ItemSlot:1514-1527；spawnDrop 溢出=GetOrDropItem
3. **StatusPlayer 48/48 型**（代理）：AST 提取器+vanilla-statusplayer.json+projTargets 表驱动解释器；6 新 BuffType（Darkness=**vanillaBuff 22** 即 blind 源/Cursed 23/Blackout 80/Webbed 149/Vortex 164/Withered 196）；我接线 6 处（PvP 爆炸 hostile=false/光衰减 blind×0.95+blackout 双源+**globalBrightness live binding 1.2→1.0**/Webbed 物理+下坐 :26477 三联/Withered 四系×0.5 含 summon 早退支/Cursed noItems 门/Vortex gravity0+cos 摆动）
4. **附近箱合成**（代理）：craftSourcesFor 四序（开箱→虚空袋 4131→附近 bank→600px 箱）；我接线 vanillaAvailableRecipes/vanillaCraft（每 tick 缓存活引用）；顺带修单 id 分支 need 不减 bug
5. **渔夫套**：ARMOR_SET_BONUSES 8 组合（161|286 × 169|253 × 104|241）→ spawnRate×1.3/max×0.7（NPC.cs:627-630）
6. **隐身**：BuffType.Invisibility(vanillaBuff 10)+生成环 ×1.2/×0.8（:611-615，getSpawnRate +2 参）；隐身药水 297 数据原在、buff 缺失曾静默失效
7. **冰刀+冰面**：accfx iceSkate（950/1861/1862/5000）；Player floorTileT 字段（既有沙族扫描扩展+坡面门 :23466）；slippy 集 {161,162,127,163,164,200,659} acc×0.7+无冰刀 slow×0.1；slippy2=197 acc×0.6+slow=0；冰刀 acc×3.5+maxRun×1.25
8. **浮漂饰品 5139-5146**：见 [[lighting-parity-audit]]（钓鱼链非光照批遗留转正）
9. **magmaStone**：accfx 1322/1343+applyMagmaStoneProj(1/7)+Swing(1/4/3/8/3/8)+WeaponProj/Game 挥击双挂点；**纠并行会话 PvP 侧 vid===903 误查**（应 1322/1343）
10. **Portal Gun 3384**（代理，**非 1153**——1153 是旗帜）：PortalGunBolt 601 extraUpdates=30 语义；我 B1 左键 form0/B2 右键 form1（右键挂 tile 交互后= :31070 语义，inp.rightDown 防已消费）

**projStatus 收尾批**：提取器区间门补齐（390-392/399-402/1107-1109 +10 条）+type 15（1/2 掷 24@5s，remix 分支登记）/85（默认 323@20s，ai0 门登记）手工特例+**137 Slimed 实装**（Enemy slimedT——onFire 段叠 +4HP/s :92623）；151/183 依赖魂镰 3006/星尘细胞实体登记

## 进行中
- ✅ **A6 摇树全量落地**（代理，38 测试）：src/world/TreeShake.ts（37 支掉落表 1:1+树底归位+叶爆 FX+每树每日注册表黎明清）；Game tryMine fail 路径挂钩（门 axe&&IsShakeable）。**源码纠偏三则**：①弹幕摇树原版【不存在】（CutTilesAt 无 fail 分支；抓钩 effectOnly 早退先于 ShakeTree）——加了才是偏离；②IsShakeable{5,72,323,583-589,596,616,634} ≠ tileAxe 两张表（仙人掌/倒木/假人可斧砍不摇）；③宝石/景观树 GetTreeType=None 门 → 永远零掉落（1:1 保留）；冷却=每树每日（treeShake 注册上限 500，黎明 :64846 清）非每击；注册先于封死门（死树也耗份额）；**原版无命中摆幅**（树摆全靠风，WindGrid 按玩家移动推格）——渲染查询已导出但接线即偏离；顺带修 TILE_AXE_SHEETS 漏 588 钻石树。遗留登记：NPC 爬墙族 KillTile(fail) 顺带摇树（NPC AI 批）/斧头仙灵 1050 支/Lucy 斧聊天

## 登记（依赖/决策类）
- WoF ×3/×0.3：现 Boss 全局停刷门比原版宽（原版只 WoF 特例）——收窄=行为变更留决策
- 双键清理：方案在 docs/dual-key-cleanup-plan.md（4851-4857 重复键潜在 bug），恢复条件=安静窗口
- buff 103（水行族）免疫 24/323/67：需 103 buff 跟踪
- 开包产物不 roll 词缀（与 boss 袋一致偏差）；headcovered ×0.85 未跟踪；仙女 isNearFairy 生成环（:653-656）
- 礼袋/宝藏袋右键开包（宝藏袋仍走手持左键链）
- 天空盒世界族（Skyblock 六分支）/vampireSeed：跟 NpcDrops 'SkyblockIsUp' 惯例恒 false
- Pal 联动 696：数据+素材双缺
- 城镇 NPC 微光上升态（无 ai[1] 30→90 状态机载体）

## 教训
- **接线清单纪律奏效**：代理禁碰 Game/Player 写导出+清单，主会话集中接线——105 测试零冲突落地
- 并行会话 PvP netPvpOwnerCtx 曾误查 vid 903——跨会话代码也要抽查数值
- kill premature：wiki 审计文档三处"未实装"实为已落地（getGood/幸福度/狙击镜）——台账必须活体验证不 trust 文档
- StatusPlayer 无 ai 门故零跳过全量；StatusNPC 有 ai 门故 SKIP 清单永存——两表结构不同勿套模板
- **全量确认批（08-13 深夜）**：`npx vitest run` 全仓 2788 过/16 挂；★cwd 假阳性陷阱——后台任务 shell cwd 漂到仓库父目录时 44 例相对路径（public/l10n 等）集体 ENOENT，全量必须 game/ 目录内跑。16 例分诊：4 例陈旧已修（damage() false→0 返回值改制 ×2/钱币 74=9999 1456 堆叠改制/八音盒 9999）+食人鱼靶子僵尸 81 免疫 20→**D5 派生不死不流血**合法拦 375（换活体靶 4）——138/138 绿；11 例并行领地（世界生成金标 5/caves 4/渲染源断言 2/hive+firefly 生成漂移忽绿忽红）+1 外部 oracle（/tmp/vserver）

相关：[[lighting-parity-audit]]、[[use-path-final-audit]]
