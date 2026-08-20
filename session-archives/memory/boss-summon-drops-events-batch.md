---
name: boss-summon-drops-events-batch
description: 全Boss三维总审计+修复:召唤链(成功才扣×5件/同型门BOSS_FAMILY增补/天界印记四重门/4988仅ZoneHallow/老人诅咒去hardMode门/眼球清spawnEyePending/DD2两压制门/世花灯泡支撑破坏) + 宝袋4+2真bug(sw按臂数/default独立branch/猪鲨2623/EoW矿量+devArmor 1/16全局表) + 光女白天ai3=2 + 裁缝娃娃召唤骷髅王 + 史莱姆雨计数门 + 旗标(陨石快照序/misc32·33/灯泡首杀门/史王停雨)
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-18T05:41:24.300Z
---

全 Boss 召唤/掉落/触发事件总审计修复批（2026-08-18，用户令"检查各种boss的召唤方式、掉落物、触发事件是否全部齐全无误"）。三路审计（肉前召唤/肉后+事件/掉落旗标）发现 24 处偏离，三路修复代理全落地，src 全域 tsc 零错，Boss 回归 103/103。

**A 路 Game.ts 14 项**：召唤物"成功才扣"统一（1133/4988/机械三王/5120——原版 SummonItemCheck false 不 ApplyItemTime；范本 useSuspiciousEye）；BOSS_FAMILY 增补 eye_of_cthulhu/king_slime/queen_bee/deerclops 同型门（原版配对表 :41514）；老人诅咒删 !hardMode 门；useSuspiciousEye 尾清 spawnEyePending；**天界印记 3601 四重门**（downedGolem&&hardMode&&!anyDanger&&!anyoneNearCultists 2500×1500 矩形+startImpendingDoom 副作用清教徒）+useTime 45；**史后水晶 4988 门仅 ZoneHallow**（原版无昼夜无 hardMode 门——获取在肉后但使用无门）；DD2 压制机械 roll+月事件门（删 invasionType 项——军队不阻月事件）；机械三王 useTime 45；世花首杀 misc[33]+三旗首齐 misc[32]（用 !wasDowned 翻转语义防旧档误补发）；**EoW/BoC 陨石快照序**（boss2Already 写键前求值——曾恒 true 致首杀必坠变恒真）；三王全灭灯泡加首杀门（防超发）；史王死停史莱姆雨+成就16；珠/心音效分档（**心=Killed_1 珠=Shatter——审计任务文字写反了，以源码为准**）；世花灯泡支撑破坏路径（CheckJunglePlant 2×2 锚回推）。

**B 路 宝袋 4+2 真bug**（40000 次统计实证）：sw 掷面按袋内臂数（曾硬编码 8 面→四武器袋 50% 空手）+default 独立 branch（1313/1297/3858 撞号→共现双掉）；猪鲨袋 2623 chanceElse 撞 2609 的 1/10（90% 必掉→1/6 互斥）；史王/史后袋 dedup2 行自产两件（删冗余行，恰 2 件）；EoW/BoC 矿量 master 110-136/else 80-111 + **stackOf 优先级 bug**（stackVar 在 lo/hi 前吞区间）；EoC 袋 stackExpr 三段拆分；**devArmor=1/16 全局 Next(21) 套装表非 per-bag**（源码实证，21 组提取）。**光女白天 Enraged ai3+=2**（满血白天召出即 2；dash 重算曾覆盖 9999 白天档）→ Terraprisma 可达。骷髅王白天狂暴 Roar。

**C 路**：**裁缝巫毒娃娃 1307 夜杀裁缝召骷髅王**（TownNPC.hurt 死亡钩→spawnVanillaEnemy(35)+Center 落位+boss 槽+HasAwoken）；史莱姆雨击杀计数加 AnyNPCs(50) 门（王在场不计数）。

**审计勘误存档**：127=机械骷髅王本体（131=PrimeLaser 手臂！）——downed_134/125/127 三王判定本就正确；机械眼 544/蠕虫 556/骷髅头 557；血腥脊椎 1331 非 1329；明胶水晶 4988 非 4915；棱彩蜻蜓 661；塔→月总 3600t（12s 是天界印记专属）；猪鲨松露虫**有海洋带门**（:19213）；光女白天杀蝶**也召**（无日夜门）；蜂王浆无丛林门（原版本就无）。

**遗留登记**：物品召唤落位仍用±55列顶扫（原版 SpawnOnPlayer 500 次屏幕外——已有 1:1 spawnBossOnPlayer 待统一迁移）；拒用 Toast 自造 UX；单 Boss 槽替代 AnyNPCs 精确门（架构性）；自然出王缺 HasAwoken（Game:16764 登记）；马桶 RedHatSkeletron 备案。

关联 [[boss-summon-announce]] [[wof-voodoo-bossslot-fix]] [[boss-audit-prehardmode-2026-08-13]]。
