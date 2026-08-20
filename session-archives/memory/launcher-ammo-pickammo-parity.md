---
name: launcher-ammo-pickammo-parity
description: 发射器弹药族对账——PickAmmo 弹型解析是加法非替换(火箭一型打出隐形弹根因)+Specific匹配表60对+AI_016发射支fired模式五族行为+地形闸门表
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-14T03:07:13.005Z
---

# 发射器弹药族对账（2026-08-14，重力对账延伸案）

**根因一（弹型解析）**：`projToShoot = 发射器shoot + 弹药shoot` **加法**（Player.cs:52648-52651），非替换！火箭一型 771 shoot=0 → 基弹；二/三/四型 +3/+6/+9 偏移。本仓旧链"弹药 shoot 替换"导致：**火箭一型打出 projId 0 隐形弹、二型打出手里剑（772.shoot=3=Shuriken！）三型回旋镖六型星怒**。

**根因二（弹类分派）**：火箭族全是 aiStyle 16（=GrenadeProj 领地），旧路径按 Arrow 打（无引信无爆炸）。

**落地**：
- `resolveAmmoProjId()`（data/vanillaItemCombat.ts）= 唯一权威：Specific 匹配表（AmmoID.cs 全 60 对：759/758/760/1946/3930 × 12 弹药）> 雪人算式 338+ammo−771 / MK2 算式 715+ammo−771 > 火箭加法 > 替换；弓族特例尾改写 3019→485/3052→495 在 Game 侧。
- GrenadeProj `fired` 模式（AI_016 else 发射支 :44542-44911）：**通用 ai[0]+=1 在 :44836（视觉链后物理链前）**——五族行为：火箭（:44685）|v|<15 加速 ×1.1 + 烟尾｜雪人/集束（:44570）ai0>30 搜敌 600(930:650)+视线 lerp 1/12 → dir×16｜发射榴弹（:44870）ai0>15 后 vy+0.2+落地摩擦 ×0.95（**有重力！**）｜感应雷（:44857）恒 vy+0.2+v×0.97+|v|<0.1 归零布防 alpha 200｜撞块表（:18365）：火箭族 vel=0+隐形+timeLeft=3 贴墙爆，榴弹/雷反弹 ×−0.4。
- EXPLODE_RADIUS 补 Kill :75260-75300 闸门表：**I 型（133-135/139-141/338/340）不毁地形**；136-138 r3、142-144/341 r5、796-798/809 r7、716/780-783/804/863 r3、718 r5。
- hurtBox = Kill 尘爆盒半宽（tier1/2=11、tier3-4=40）。

**Why:** 弹名表（PROJECTILE_NAME_BY_ID）与弹 id 的错位直觉（"proj 3 应该是火箭"）必须用 ProjectileID.cs 常量表钉死；PickAmmo 特例优先级链不读源码必错。

**MK2 review 修（2026-08-14 二次 review 抓真 bug）**：muzzle 构造曾把 ai[1] 初始化成 volley 间隔 → **MK2 首发迟 8t / 派对枪迟 5t**——vanilla 出生只传 ai0（:48376），ai[1]=0 → 首 tick 即发第一发（变体=⌊1/8⌋%7=0）；且**首发跳音门仅 714**（:64114 `ai[0]!=1f`），615 的 Item36 首 volley 就播（:64004 无门）。测试补"第 1 tick 必已开火"断言。**同课再证：出生 ai 参数缺省值的计时器语义必须回 NewProjectile 调用点核（缺省 0 ≠ 周期间隔）。**

**MK2 批（同日收口，Celeb2.ts）——"5×Next(0,20)"之谜三连翻案**：①弹 id 直觉又错（714/615 非 ai147 烟花弹，是 **aiStyle 75 持械 muzzle**；真烟花=715-718）②`5×Next(0,20)`（Player.cs:48376）不是变体是**出生相位偏移**——muzzle 每 8t(714)/5t(615) 一发，变体=⌊ai0/volley⌋%7 **确定循环**，子弹 715-718 的 ai0 即变体（714 段 :64072-64195）③变体档：3 速+1、5 三连±2π/80、4 附 ai1=1（AI_147 case4 蛇形相位跳 t=1 时 +45）。落地：Celeb2Muzzle（channel 持械/每 volley fireCb 由 Game 解析弹药逐发消耗/Item156·36/彩虹枪口尘 hsl(ai0/90)）+ Celeb2Rocket（AI_147 七变体弹道：0 缓坠@20u+沿途空爆、1 上抛 vy−10@10u+scale 2.5、3 追踪保速 lerp 1/8、4 蛇形⊥×cos(t·π/45)×3、5/6 延迟重力 40u/30u，E=2 终端 16，GetCeleb2Color 七色光）；Game 接线 3930/3475 → muzzle（同型在场门），派对机枪 3475（**子弹供弹** useAmmo97）每 7 轮附赠 616 彩带 +20 伤 ×1.25kb 速8。测试 celeb2-mk2 10 条。**教训：AI_075 是持械杂烩族——弹 id 先查 aiStyle 再谈行为；"反编译数值反直觉"时先找消费端（615 的 (ai0/5)%7 揭穿相位语义）。**

**Phase B 处置（同日）**：液体火箭载荷已接（BOMB_PAYLOAD 补 784-792/799-801/805-810 四族 = Kill :74051-74244 同 903-906 四分发；发射分支注入 spreadBombPayload）+ **入液即爆**（:44267 wet→timeLeft=1，GrenadeProj firedStep 头 wet 扫描——注意 fired 分派在非 fired 湿扫之前，液体火箭的湿扫必须放进 firedStep）。**查实两项免做**：集束火箭（793-798/808/809）Kill = 纯尘环视觉无次级弹（地形半径 r7 已在 EXPLODE_RADIUS）；感应雷无近爆门 = 纯接触爆（AI_016/Colliding 均无 proximity 触发）。

**How to apply:** 发射器武器解析一律走 resolveAmmoProjId 勿手写 shoot 链；新增火箭类弹药查三张表（Specific/FIRED_*/EXPLODE_RADIUS）。测试 tests/launcher-ammo-parity.test.ts（12 条）。溶液族（AmmoID.Solution=776）本仓无武器，加法分支已备未消费。关联 [[arrow-gravity-chain-parity]] [[explosion-family-port]]。
