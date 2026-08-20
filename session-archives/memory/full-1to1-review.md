---
name: full-1to1-review
description: 全面1:1审查+修复终态：3审查代理分区(坐骑快乐度/宠物AI研究/移动端成就)+~20处修复；坐骑hover疲劳固定类型表是审查最大鱼；遗留登记清单
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T09:21:29.514Z
---

全面 1:1 审查 + 修复终态（2026-08-13 第五轮，/goal 补齐+review）。[[systems-final-batch]] 续。

**方法**：3 个只读审查代理分区并行（坐骑+快乐度=并行会话新产出待审 / 宠物AI+研究=子代理产出待验 / 移动端+成就=主会话自审），全部对照反编译逐行。修复合计 ~20 处。

**坐骑（并行会话产出）审查发现 11 项，已修 6**：
1. ★★ hover 疲劳语义：DoesHoverIgnoresFatigue（Mount.cs:3534-3542）是**固定类型表 {7,8,12,23,44,49,56,61}**——曾实现成 fatigueMax<=0，致 UFO/钻头/猪鲨崽全飞行族误耗能坠落。已改固定表（MountInstance.HOVER_IGNORES_FATIGUE）。
2. 熔岩鲨 buff 305 进 BUFF_SWIM_FREE（Player.cs:9602-9608）。
3. R 键缺 QuickMount 召唤支：补 Game.quickMount（装备槽优先→背包扫非矿车→useMountItem；无坐骑物才 QuickMinecart，Player.cs:5728-5783/:5859-5878）。
4. 兔兔 type==1 摔伤落距清零（Player.cs:25022-25025——曾按 fallDamage 0.8 结算）。
5. 下坐三连败：FailedNoSpaceCount 计数→第 3 次强制下坐+PlayerNoSpaceTeleport（:5738-5753/:5685-5726）——Game.mountNoSpaceCount + playerNoSpaceTeleport。
6. 派对女孩 Dislike snow→underground（PersonalityDatabasePopulator.cs:137-141；曾抄串行）。
7. forest zone 补 zoneDirtLayerHeight 排除（Player.cs:3660-3683 泥土层也算 BelowSurface）。
**未修登记（中/轻）**：骑乘 hitbox 不长高（42+heightBoost，Mount.cs:6254-6265——影响天花板碰撞）；hover type48 专属段+原地悬停微推（:3363-3449）；type54 速龙条件飞行；dismountsOnItemUse；飞行坐骑摔伤豁免（:25014-17）。

**快乐度**：24/25 关系表+24/25 群系表对齐，公式全 1:1（0.94/1.06/0.88/1.12/拥挤×1.05/钳[0.75,1.5]），event 20 PriceAdjustment≤0.82 门 ✓。

**宠物 AI（子代理 B）**：提取器幂等+锚点真实+61 款 frames 0 差异+测试非恒真 ✓。修 2 提取器正则盲区：875 VoltBunny landRange=100 连写漏提（:57461-57465）、960 Chester idleRange=10 后缀条件漏提（:56039-56041）。登记未建模：Wisp 211 远距追击档、fly 距离分档加速度、Y 轴加速×2、960/1027 目标偏移、313 翻转门。

**研究（子代理 E）**：need 表 6089 全量重算 0 差异+override 12 对+幂等语义全 ✓。修 2：SacrificeAll 超扣（改 min(need-have,stack) 封顶，CreativeUI.cs:297-314）；补逐帧 checkResearchAchievement（Player.cs:25418 版本门——曾只进世界查）。

**移动端+成就自审发现，已修 5**：damageVar trunc→**round**（Main.cs:65620 是 (int)Math.Round——曾系统性偏低 0.5）；矿车撞怪补 **expert ×1.5**（:28811-28813 独立乘区）；荆棘 luck 符号**-p.luck**（:30929 0f-luck）；ResearchUI 入 Input.isUiTarget + uiBlocking 门；mainFlow 顶层 __swAchievements（首访标题屏可达 GOING_OLDSCHOOL）。登记：击退预除 knockBackResist 近似（hurt 侧无 resist 暴露）、次指 touchstart 无 preventDefault、Math.Round 银行家 vs Math.round 半值差、成就派发缺口族（prog 8/16/17/18/24/26/30-44、flag 5/17/19/22/23/25 多挂未移植子系统）。

**验证**：135/135 全绿（9 测试文件含 mounts/happiness/pet-ai/research/alignment）；我的文件 tsc 零错（余错=并行在途）。审查期间并行会话修复瞬态 2 测试（钻头光束/山羊跳——在途态勿慌）。