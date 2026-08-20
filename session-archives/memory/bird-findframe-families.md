---
name: bird-findframe-families
description: 鸟/小动物 FindFrame 专属 case 全家族——地面鸟不踱步是站定帧前提;鸮族 spriteDirection 取反的双翻陷阱
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-18T07:33:55.658Z
---

小动物帧调度多数不在 FindFrame 通用组(NPC.cs:69230 大 case),有专属 case,落
`vanillaFrameIdx` 通用 6t 档即错(2026-08-18 批量修正,均在 Renderer.ts):
鸟 74/297/298/442(:74326 站定=帧4/飞行0-3 每4t)、丛林鸟 671-675(:74352 站0/飞1+ 每4t)、
鸮 611/689(:74379 待机8帧转头/飞8+每5t)、萤火虫 355/358/654(:73369 4t亮3t闪+非发光
lai1≤0 暗带+2)、677/蜻蜓 595-601(3t 循环)、蚯蚓 357/448/484/606(:73455 静1/爬0↔1 12t/
腾空1)、蛆 485-487、瓢虫 604/605/椿象 669(:67616 地0-3/空4-7 每2t)、水鸟 363/365/603/609
(:74470 划水1↔2 8t/站1/飞11+每4t)、珍稀宝箱怪 473-476(:71831 伪装=帧0,曾14帧狂闪)。

**Why:** ①地面鸟 AI 原版**不踱步**(AI_024 :25453 只重力,vx 恒 0——降落 :25488 显式归零),
曾自创 ±0.7 踱步 → 站定门 vx==0&&vy==0 永假 = 地面播飞行动画;②鸮族
`spriteDirection=-direction`(:74381),flip 极性=Main.cs:22985(spriteDirection==1 才翻)
→ 仅 direction==-1 翻——**必须从通用镜像行排除,否则两条叠加成恒翻转**(屁股朝前,终审抓出)。

**How to apply:** 新小动物动画错位先 grep 原版 FindFrame 找专属 case;加镜像特判必查与
通用 `facing>0` 行的叠加。鸮族 AI:出生即飞(localAI[0] 门)、夜栖城镇 NPC 屋檐、689 夜间
玩家<80px→Transform(317 魔眼)、湿态 vy×0.95−0.5 钳−4(:25596 三态通用)、飞行帽 3/丛林鸟 4。
鸟粪弹已补(2026-08-19:PoopProj 全链,★仅负幸运玩家或 IsThisCenx 四名(cenx/cblox/jade lightning/cenigit,Player.cs:18032)会被掷——RollOnlyBadLuckExtreme 幸运≥0 恒返 −1, Luck.cs:53;尘 329 已引擎化含实心格×0.8 收缩)。蚯蚓自旋/坡面已接。鸮待机/宝箱怪状态机已 1:1(WeakMap 态)。关联 [[critter-ai-port]][[vanilla-npc-port]]。
