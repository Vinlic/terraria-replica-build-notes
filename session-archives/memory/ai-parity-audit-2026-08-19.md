---
name: ai-parity-audit-2026-08-19
description: 六代理AI全量1:1审计~200条:当日修15项(694崩溃/鸭子海马仙灵瓢虫反向/仙灵逃逸/石巨人胜利倒置/蜂群速度表/batAI双段/蚁狮/史莱姆激愤表);台账docs/ai-parity-gaps-2026-08-19;★死亡=只积分不steering(原版共享积分段:93808)
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-19T10:03:30.356Z
---

2026-08-19 六分区代理 AI 全量 1:1 审计(死亡退化+追击门×2、地面/小动物/飞行水生/Boss 全量×4),~200 条。台账=game/docs/ai-parity-gaps-2026-08-19.md(未修项+原版行号),当日修 15 项(测试 tests/ai-parity-batch-2026-08-19 + float-eye-dead-player + fish-behavior)。

**★最重要方法论**:原版 NPC 位移积分在 AI 外**共享段**(`Collision_MoveWhileDry` NPC.cs:93808 `position += velocity`)——AI 分支被跳过 ≠ 冻结,而是按冻结速度继续滑行。本仓各 AI 须自调 moveAndCollide ⇒ **死亡分支一律"只积分不 steering"**(birdAI/vultureAI/duckFlyAI 已照此修;仍有一批 `!player return` 早退冻结在台账 A 区)。另:原版 `GetTargetData()`(:6817)死亡时返回 (0,0) 默认位——部分 AI 字面上朝世界原点飞,实用语义仍取"保持最后方向"。

**当日修复要点**(细节在代码注释与台账文首):
- 694 水书宝箱怪冲刺段 `player!.cx` null 解引用=必崩(玩家死于冲刺 10t 内)
- 行为反向族:鸭子逐帧背向玩家+水陆变形死循环、海马水面折返取反(顶出水)、仙灵追人(应逃逸,引导态仅虫网释放 ai2=2)、瓢虫陆行慢 20 倍+翻转轴错、秃鹫死亡自造 cy−100 目标无限上飞
- **石巨人胜利条件倒置**(坏档级):应=本体死亡终战+自由头 249 恒无敌(:12151);曾满血续命+杀自由头终战
- AI_005 速度表(陨石怪曾 6 倍速)/batAI 第二段移动 11 类/史莱姆恒激愤表/蚁狮开火在 rooted 前/小动物站走计时互换+危险扫描每 tick+canHit+乌龟豁免

**★全量修复批(同日,五代理并行)**:A-F 区 ~190 条全部落地(台账 docs/ai-parity-gaps-2026-08-19.md 已逐区销项,含各批"已修 N 项"清单)。测试:五批新回归 critter-parity-fixes 25+ground-ai-parity-fixes 37+flyer-ai-parity-fixes 30+boss-parity-fixes-a/b 各 31=154 例+首日 8 例;合并终验 181/181、tsc src 零错。要点:
- A 区系统性:dispatch 改传原始 player(死亡对尸体坐标运转);solenian 恢复态"复位同 tick 拉满"结构 bug;projDmgMultiLerp (difficulty−1)/2
- C 区:史莱姆 per-type 跳跃梯/空中转向/金属矿强化段/204 专家分支;近身扑跳族 15 型;远程族重写(292 四连发/216 双档/火星七型+伺服飞行);471 术士六态机/482 石壳/631 连发循环;昼行表重构
- B 区:跳档 num27 语义(1 格台阶 StepUp 不跳)/wet 碰撞盒语义/家域 50 格回头/金鱼雨天形态链(fishTransformationDuringRain,Game 敌怪轮)/鸟拉屎 PoopProj(飞行鸭同款主会话补接)/蜗牛双轴贴墙重做/气球真碰撞(落地滑行不爆)
- D 区:蜂群全核(619 血鱿鱼/远距增速/朝向基座/白天驱散表——★5 号仆从白天上飞驱散是原版行为,shimmer 测试场景须钉夜)/幽灵族移动核/骷髅王手五态机/620 地精鲨陆地夜射连发
- E 区:Retinazer 侧移拓扑/双子+骷髅王专家档/史王全核/蜂后专家 11 处/月总 Lerp 0.98 命名参数陷阱/光女连段表+攻击12/月亮事件弹道物理表+noTileCollide/DD2 索敌夺标/火星真难度
- F 区存疑全部证据链定谳(世花×0.9 补 Remap/飞碟−1 两代反编译 no-op/鲨鱼龙 PlaySound 库 4=NPCKilled_19);**遗留全景在台账 G 区**(G1-G11 四类):实现层缺口 5(groundPhysics ±maxSpd 硬钳=S4/S5 跳冲量被砍,翻共享管线需独立批/S10 携物梯 20+ 档/弹-NPC whoAmI 通道消费端未提取/蜗牛 flipY 渲染通道/贴角 1.4px)+伪迹存疑 6(蚁狮仰角锥/水母 localAI 渲染消费/月总死光×2=iframes 补偿待 DPS 对拍/克脑掉落门/516 α 方向/花岗岩 dy-dx 笔误)+并入存证 4+方法论 2(测试世界≥140 高防底钳/批跑假红先单跑)
- ★全库批跑教训:新测试在全量扫描时偶发负载假红(单跑稳定),flaky 判定先单跑×3;测试世界高 <140 触发世界底钳(StepUp/WetCollision 屏蔽)是"旧测试恰好通过"的隐藏根因

**★G 区终清(同日追加两代理)**:G1-G11 全部落地——G1 groundPhysics 重做为原版共享位移段 1:1(**零速度钳零尾段摩擦**,±1 硬钳与 ×0.8/×0.98 均仓内自创一并废除;调用方按原版证据各自带帽:史莱姆无帽/蚱蜢 0.2/僵尸 0.9×scale)+贴地门 velocity.Y==0 字面;G5 贴角 1.4px 挪移+落地嵌固回退(collideY 位=分轴碰撞后坡面碰撞前,Entity/TileCollision 加位);G2 携物梯全 ~30 档(掷弹/金属/蜂巢生蜂/药草洒籽/化石/生命水晶/传送带摩擦替换段/地狱石等,跳过备案=屎/蜂蜜/语音/Skyblock);G3 whoAmI 定谳 411→537/424→573(Dart ownerNpcId 通道+537 全激光+573 蓄能齐射);G4 蜗牛 flipY 渲染通道;G6 蚁狮仰角锥字面接;G7 水母死槽备案+鱿鱼 FindFrame 重写;G8 月总死光 ×2=通用敌弹规则保留+难度缩放漏乘修复;G9/G10/G11 各定谳。新测试 slime-item-ladder-parity 24+parity-g-forensics 16;合并终验 208/208、tsc src 零错。1405 反编译 AI 主体缺失("method too long"),NPC AI 只能 1456 单版为准。

相关:[[spawn-pool-aggro-audit-2026-08-17]](死亡寻路语义+AI_016 flag22) [[bunny-walk-frame-fix]](帧速档)
