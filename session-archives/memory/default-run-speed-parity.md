---
name: default-run-speed-parity
description: 默认移速对账——裸装accRunSpeed基准是3非6(||6翻倍30mph根因)+越帽摩擦回落锯齿(原版无硬钳)+常量表全对;accRunSpeed=reset时maxRunSpeed裸值不随moveSpeed
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-17T03:45:10.594Z
---

# 默认（裸装）移动速度对账（2026-08-16，用户问"无加速道具默认移速是否对齐"触发）

**结论：此前不对齐（默认极速翻倍），已修 1:1。**

**常量表全对**（Player.cs:2376-2390 ↔ constants.ts）：gravity 0.4 / maxFallSpeed 10 / maxRunSpeed 3 / runAcceleration 0.08 / runSlowdown 0.2 / jumpSpeed 5.01 / jumpHeight 15。跳跃持跳模型也已是原版钉速语义（vy 每 tick 覆写 −jumpSpeed、vy==0 终止、松键不清计数——2026-08-15 并行会话审计已修，勿再引入 vy−=0.22 累加）。

**Why（两真偏差）**：
1. **裸装 accRunSpeed 基准错 6**：原版每 tick reset（:24099）`accRunSpeed = maxRunSpeed`——此时 maxRunSpeed 尚为裸值 3（moveSpeed 乘区 :25694-25695 在 reset 之后、只乘 runAcceleration/maxRunSpeed 不乘 accRunSpeed）；6/6.75 是靴族 equip 覆写（赫尔墨斯 54→6、Frostspark 1862→6.75、Terraspark 5000→6.75）。本仓 `equipStats.accRunSpeed || 6` 把"未装备"当"闪电靴"→ 裸装 3→6 慢爬坡（×0.2 档）跑到 **6 px/t = 30mph，原版 15mph 翻倍**。修：`|| 3`。
2. **越帽硬钳 ≠ 原版摩擦回落**：原版水平链（HorizontalMovement :19559-19800）**无通用硬钳**（仅 sticky :26211 钳 maxRun）——持键越帽（+0.08 过冲 3.04）落入摩擦分支（地面 −0.2/空中 −0.1）→ 2.84 → 再 +0.08……**锯齿均值 ≈2.93 = 原版"15mph"的真实纹理**。本仓曾 `vx=min(vx, max(accRun,toward))` 硬钳=恒 3.0 平线。修：去钳 + 持键越帽走同款摩擦（applyRunFriction 共用段，ix==0 与超帽两路同源）。

**How to apply**：两段模型速查——|vx|<maxRun：+0.08（反向先 ±0.2 制动，净 −0.28/t；越零后 |vx|≤0.2 无制动仅 0.08）；maxRun≤|vx|<accRun：×0.2 爬坡（需 vy==0 或翼飞，slow/burned 封）；≥accRun：摩擦回落。靴族测试**必须真穿靴**（equipStats 是逐次重算 getter，改返回对象无效）；长跑测试世界要够宽（靴族 300t≈1.5 万 px，120 格世界 ~200t 撞边界掉速）。测试 tests/player-run-parity.test.ts（4 条：逐 tick 与原版复算零差/急停/反向/靴族爬坡+6 锯齿）。

关联 [[pvp-system-port]]（msg13 远端玩家模拟同链）。

**2026-08-17 补**：裸装锯齿 3.04 越线在原版**不会**触发跑尘/脚步声——SpawnFastRunParticles 嵌在爬坡分支 B（入口 vx<accRunSpeed）内，与尘门 vx>中点互斥，裸装带 [3,3) 空。勿把锯齿越线当"原版裸装也出跑尘"的证据（详见 [[multijump-fx-port]]）。


## 二轮：地面材质链全量对齐（2026-08-18 "角色在冰面会脚滑"检查批）

用户问冰面脚滑——审查发现**玩家冰面链整条是死代码**：材质分支拿**原版 sheet id
(161/197…)** 直接对比 `floorTileT`（存**内部 tile id**,st.type——ice 内部 45/薄冰
46/神圣冰 413,全不相等）→ slippy/slippy2 永不命中=冰面不滑。★教训：**st.type
是内部 id,与原版 sheet id 对比前必须 TILE_BY_KEY 反查**（同 spawnTileType 坑）。
修：ICE_SLIP_IDS/FROZEN_SLIME_ID/ASPHALT_ID/HONEY_FLOOR_ID 四集导出,移动链+
渲染腿动画门共用。

**顺带补齐原版 else-if 真序全链**（Player.cs:26210-26255,曾只有 sand/ice 段）：
- sticky 蜂蜜块【地面】229：maxRun/acc×0.25+slow×2+钳 ±maxRun（:26210-21,与
  StickyTiles 泡块阻尼 :22650+ 是两条链）+ **跳削弱 :19343**（jumpHeight/10、
  jumpSpeed/5——站蜂蜜跳不高）。
- powerrun 沥青 198：maxRun×3.5+slow×2（跑道;:28067 还有 RollerSkate 专用
  ×2.25/×1.6,无该坐骑族略）。
- 腿动画 :35818-26：打滑面无输入 → counter=0 腿钉行 0（滑行不迈腿）——同款
  内部 id 死门一并修。
**冰刀旗也是死的**：accfx 提取器漏 `iceSkate = true;` 模式（七轮补,950/1861/
1862/5000 四件再生）——修前 eqEarly.iceSkate 恒 false。
**NPC/怪物侧核实**：原版 NPC.cs 零地面材质摩擦检查 → 敌怪/TownNPC/小动物在
冰面【不】滑（我方各 AI 亦无材质分支=已对齐,勿自作主张加）。
测试 player-run-parity +7（冰面×0.7 加速/松键×0.1 惯性/197 零摩擦/蜂蜜钳速/
沥青跑道/蜂蜜跳削弱/真穿冰刀到帽 3.75）。


## review 轮（同日）：sticky 时序纠偏 + 折叠凳全链移植

自审发现两偏差两缺口，全修：
1. **sticky 跳削弱时序**：原版 :19343 在 UpdateJumpHeight 的坐骑赋值【之后】
   （坐骑跳同样被削 /10//5）——我首版挂在 baseJump 阶段=坐骑豁免。已挪到
   mJumpSpd/Ticks 分辨后。
2. **Dazed(160) 跳削弱不移植**：全 1456 源码零施加源=死字段（accWatchTime 先例）。
3. **折叠凳（Step Stool 4341/造物之手 5126）全链新移植**：equipStats.stepStool
   （★accVid 检查必须在 `if (fx)` 块**外**——4341 无 accfx 条目,块内恒跳过；
   SetStats 在 Player.cs:14077 非 Item 字段,提取器模式扫不到）+每 tick 使用门
   （站定 vx/vy==0+按上+非坐骑+无钩爪+CanFitSpace(26) 头顶净空；原版每 tick
   Reset→条件重建=松条件即收）+命中盒 42→68 脚锚上长+跳链 +5（:19341 非坐骑支）
   +起跳离凳 y-=26 净上步（:20504 **无分支门**——湿跳同）+渲染无需改
   （VisualYOffset=26 恰补偿盒上长=贴图原地,只是头顶判定+26）。
4. 教训：**装备效果检查先看该物品在 accfx 有没有条目**——`if (fx){...}` 块内的
   vid 检查对无 accfx 物品是死代码（4341 实锤）；tsc 对此沉默（类型合法）。
测试 player-run-parity +2（凳全生命周期/顶棚 CanFitSpace 拦截）→13 例。
