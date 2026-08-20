---
name: npc-extra-limb-drawing
description: NPC 附属肢体（藤蔓/链/臂骨）是 Main.cs DrawNPC 叠画分支，非贴图表；已移植清单+遗留缺口
metadata: 
  node_type: memory
  type: project
  originSessionId: d65984ee-19eb-4ecb-a23f-ae09c6e8abd8
  modified: 2026-08-11T08:25:14.653Z
---

原版 NPC 的"多出来的部件"多数不在 NPC_xxx.png 里，而是 Main.cs DrawNPCDirect(22350-26209)/DrawNPCs(22159-22301) 的叠画分支逐段程序化绘制。2026-08-11 食人怪"只有头没有藤蔓"根因；同族全量对账（两代理审计）结果：

**已移植（Renderer，均在 drawEnemy 前置钩子）**：
- AI_013 族（43/56/175/259/260）Chain4/5/14/24/25 步进链 :22433-22514 → drawPlantVine
- **101 邪恶触手是独占分支** :22391-22432（`if(type==101) else if(aiStyle==13)` 互斥！）：Chain10/11 交替、scale 0.75、步进 15px、终止 21px、尾段高 dist-40+28（绘制高恒 28 重叠）——勿走 Chain4 默认
- 双子 125↔126 互连链 Chain12 :22177-22224（1.4.5 新增，IsMechQueenUp 门）→ drawTwinsChain（125 单侧画）
- 石巨人拳 247/248 Chain21 :22593-22632 → drawGolemFistChain（master=本体，死透锚自由头=偏差）
- Prime 部件 129-131(aiStyle 33-36) Arm_Bone_2 两段 92/60 IK :22633-22675 → drawPrimeArm（master=头）
- 世花钩蔓 263/触须 264 Chain26/27 :22225-22285 → drawPlanteraVine（master=本体/锚触须）
- 骷髅王手 36 Arm_Bone :22543-22596（原有 drawSkeletronArm）、史莱姆王忍者+王冠 :22798/:25567

AI 侧部件→主体链接统一走 `e.master`（bossAI.ts primePartAI / bossAI_golem 拳 / bossAI_queenbee_plantera 钩蔓+触须均已赋值）。

**遗留缺口（未移植，按可见度排序）**：
- 月总 397 手/398 核心 Extra[13-19] 伪 IK（acos(len/340) 弯曲）:24325-24505
- 光之女皇 636 翼+双臂+彩虹克隆 :26364-26550；史莱姆皇后 657 翼 Extra[185] :22318-22348/23134
- aiStyle 20 链锤/尖球 Chain+SpikeBase :22714-22741（会写回 npc.rotation）
- 地牢史莱姆 71 金钥匙 :22819、蚁狮 69 沙堆 :22841、史莱姆体内物品 DrawNPC_SlimeItem :22845/:26709
- 大批 GlowMask 发光覆盖/残影（火人 24、南瓜王 327 披风+脸闪、火星系等）:25044-26207
- 未实装内容：南瓜月/霜月/火星/海盗事件 NPC、DD2 系列

陷阱：NPC 95 不是食人怪是 DiggerHead；食人怪=43、aiStyle=13。新增单图走 VANILLA_MISC 白名单+拷 public/dist sprites/vanilla/。链段 while 一律加 guard<200 防死循环。[[vanilla-npc-port]]

**食人怪头部旋转补 1:1（2026-08-11 五修，用户报"头不旋转只左右硬转"）**：藤蔓链已移植但
头部 rotation 漏了——原版 AI_013 尾段（NPC.cs:22778-22794）：259/260 真菌球恒
`atan2(num220,num219)+π/2`；其余（43/101/175）朝玩家伸展方向 `atan2(oy,ox)`，目标在左
（num219<0）**+π 且 spriteDirection=-1**——旋转+镜像组合保证头不倒挂。两处修复：
①Enemy.plantAI 写 visAngle/facing（ox=0 无目标时保留上帧角度，原版同语义）；
②Renderer NPC 旋转分支补 `aiStyle===13 → rotate(visAngle)`——**不可进 rotationDriven**
（本族原版翻 spriteDirection，禁镜像会"屁股朝前"）。验证：tests/plant-ai-rotation.test.ts
4 例 + scripts/_maneater-rotate-probe.mjs（锚点格须**先清空再放**，清空循环含锚点坐标会把
锚抹掉→plantAI 锚失活原地假死）。**教训：附属肢体叠画移植时，别只对齐"多出来的部件"，
同帧的 npc.rotation 写点也要对账（DrawNPC 叠画分支与 AI 内 rotation 赋值是两处独立源码）**。


## 附肢层序：master 锚排序（2026-08-19"石巨人头跑到背后"）

实体层排序是**全实体 y 升序**——石巨人挂载头(246)锚在本体上方(headY<bodyY)
→ y 排序把头画在本体【前】之前=垫到身后;原版 NPC 按 **whoAmI 槽序**遍历绘制
(NewNPC 先本体后部件)=挂件恒画本体前。修:Renderer 实体排序键 sortY(e) =
`e.master 活 ? master.y+0.01 : e.y`——挂件紧随本体之后(在前),挂件间保插入序
(=出生序,原版 247/248 拳→246 头=头最前)。**挂载头 246 此前没设 e.master**
(只有拳设了,拳链渲染用)——golemHeadAI 锚段补 `e.master=body`(非自由态)。
受益族:骷髅王臂 36/南瓜王臂 328/石巨人拳+头/机械三王臂 33-36/世花钩蔓
263/264(此前同样有"垫后"隐患,只是部件 y 常贴近本体未暴露)。探针
_golem-layer-probe(4 断言:家族齐/头 y<本体 y 实锤旧序必垫后/头拳双锚)。


## 同族全审计（2026-08-19 二轮,石巨人修复的连带排查）

**审计法**：列全 master 设置点逐族判方向——"部件由本体生成"(部件画本体前=原版
槽序) vs "坐骑由骑手生成"(坐骑画骑手前=方向反!)。三处发现：
1. **骑手族(390 Scutli骑手/416 火龙骑手)方向反**：master=坐骑是 AI 链接,
   原版槽序=坐骑后生成画骑手【前】——我的 sortY 锚把它画到了坐骑前=反。
   修:`drawBehindMaster=true` 标记(Enemy 新字段),sortY 回落自然 y
   (骑手 y<坐骑 → 先画在后) ✓原版。
2. **蠕虫链(EoW 13-15/毁灭者 134)未锚**:wormFollow 已有但排序没用——
   y 起伏时段序被打乱(物理 y 序≠生成序)。修:sortY 纳入 wormFollow
   (递归链键+帧内 memo+环保护)——段序恒=生成序(槽序)。
3. **月总(398 核心/397 双手/396 头)未锚**:头物理最高=y 排序恒垫底,原版
   槽序头最前(手扫过头区域时头盖手)。修:双手+头 master=核心,同键+稳定排序
   保插入序(手→手→头=头最前)——同锚同键的插入序依赖 **V8 sort 稳定性**。
其余 master 族(骷髅王臂/南瓜王刃/Prime 臂/世花钩蔓/DD2 船炮/火星飞碟部件/
军官盾/克脑 creepers)方向全对,无需改。WoF 113-115 走 behindTiles 特殊层。
测试 +3(骑手反转/蠕虫链起伏序/月总插入序),探针 _golem-layer 扩 4 断言。
