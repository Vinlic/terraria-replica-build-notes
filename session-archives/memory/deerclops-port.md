---
name: deerclops-port
description: 鹿角怪668全链落地:数据(1405提取器缺1.4.3+NPC)/AI_123九态/弹幕961·962·965/Slow buff/Camera punch;vanilla-npcs.json提取器是1405源勿信其全量
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-13T05:38:31.236Z
---

2026-08-13 鹿角怪 668 全链(此前雨天自然链因数据缺静默死):

**根因**:`tools/extract-npcs.mjs` 跑 **Terarria1405**——668 是 1.4.3 新增 → vanilla-npcs.json
缺 668 → fromVanilla(668)=null。★该 json 不是全量权威,1.4.3+ NPC 需手工补
(同 663 先例;SetDefaults 数值取 1456 :17384-17400)。

**已落地**:
- 数据:json 668(60×154/ai123/7000/20/10/kb0/noGravity+noTileCollide/boss/frames25)
- `src/entities/bossAI_deerclops.ts`:AI_123 九态(-1 入场/0 选招/1 前刺/2 碎石/3 咆哮
  Slow/4 双侧刺/5 影手六连/6 回家/7 传送落地/8 消散);家 tile ai2/ai3+despawn 86400;
  lai3≥30 远距免伤(≥450px +1/t);选招门序(贴脸 lai1≥2 双侧刺→前刺/走动240/静立90/
  远距120!Slow);Movement 自管重力(探针 40×20 底/16×80 前净空,跳 -8)
- 弹幕:961 冰尖刺(AI_157 生长/收缩窗 [0,10)/[10,20),scale=Opacity×ai1,伤13)
  /962 碎石(aiStyle1 抛物+12 变体 4列×3行,伤18)/965 影手(AI_187 四变体段
  0/180/300/390 直选+段尾即灭,alpha 50-255)
- BuffType.Slow=81(vanillaBuff 32,moveSpeed÷2 :25653)——★78 已被 Poisoned 占,
  枚举加值前必查;原版 l10n BuffName/BuffDescription.Slow 现成,零 Mods 键
- Camera.addPunch/tickPunch+Renderer 帧头衰减+GameHooks.punchCamera
  (PunchCameraModifier 近似);Enemy.ts dispatch case 123
- 音效 assets 全在(deerclops_scream_0-2/ice_attack_0-2/rubble/hit/death/step)

**坑**:①Enemy.ai0 缺省 **-1120**(史莱姆族哨兵)——非该族 AI 首帧必须
`if (e.ai0 === -1120) e.ai0 = 0`;②AI_124_DeerclopsLeg 是死代码(无类型挂 aiStyle124,
绘制单贴图)勿移植;③npcFrameCount[668]=8 与贴图 5×5=25 帧不符,渲染走
drawDeerclopsGrid 自管帧状态,json frames 填 25;④影手伤害:主线 15/专家被动 10;
⑤测试构造:选招门竞速(追击 3.5px/t 会吃掉距离差)——远距用例需持续拉距或预授 Slow 封门;
⑥**zoneSnow 在 game.scene(SceneMetrics)不在 Player 字段**——全量review抓回:
曾读 p.zoneSnow 恒 false → 回家态无法在雪原重新接战(ShouldRunAway isChasing=false 分支)

**测试**:tests/bossAI-deerclops.test.ts 10 条;探针 _f6-boss-announce-probe.mjs 7 断言
(F6 召唤→"已苏醒"广播+Boss槽+家tile)。渲染层(5×5 网格+FindFrame case 668 序列表)
此前已就绪。遗留视觉近似:出生红雾旋转/紫电重影(Renderer 注释已登记)。

相关:[[debug-tools-f6-f2]] [[boss-summon-announce]] [[enemy-ranged-transform-audit]]

**★冻结事故（2026-08-19 修）**：用户实报"独眼巨鹿冻在半空"——`deerclopsMovement` 只算 vx/vy **从不积分位置**：668 是 noGravity+noTileCollide（SetDefaults :17384），原版由引擎直移穿墙，本仓各 AI 自管位移、这族漏了。症状签名：AI 状态机照跑（ai1 递增、vy 顶到 16）但坐标恒定 = 召唤在哪冻在哪。修 = movement 尾 `e.x += e.vx; e.y += e.vy`。**教训**：原测试 harness 用 tick() 手动 `e.x += e.vx` 补积分（注释"自管位移"）——测试代偿把引擎缺口焊死了；直调 AI 的测试必须只驱动一层（AI 或手动积分，二选一），凡 harness 替 src 干活的写法都要警惕"测试绿但游戏坏"。回归测试已加"位置积分"档（追击 90t x 前进>100px + 落地）。
