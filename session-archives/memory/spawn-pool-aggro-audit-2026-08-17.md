---
name: spawn-pool-aggro-audit-2026-08-17
description: 出怪池+仇恨脱战双代理全量审计:9处修复(墙色档/661夜窗/蒲公英门/476十周年/RollLuck/骨堆/slimeRain/蠕虫地表脱战/吸血蝙蝠白天);脱战核心=CheckActive已1:1
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-19T03:01:30.189Z
---

# 出怪池频率+仇恨脱战审计(2026-08-17)

用户两问:①所有出怪池频率正确吗 ②离开群落/多远不被追击、仇恨是否运作。
双代理(池权重/脱战门)对 NPC.cs 全量对账,结论与修复:

## 频率层(正确性结论)

- **节拍链已 1:1**:fixedUpdate@60Hz → 每 tick `rand.Next(spawnRate)`(默认 600→白天地表
  ~10s/夜 6s/地下 4s/血月 1.8s);getSpawnRate 31 乘区(hardMode/深度带/昼夜/血月日食/
  雨雪/地牢/沙尘暴/地下沙漠/丛林城镇阶梯/恶地/陨石/神庙/神圣深层/附近怪分层/隐身镇静
  向日葵/渔夫套/战斗药水/水蜡烛/和平蜡烛/clamp/getGood/旅程滑杆/地牢守卫 10)全在。
- **敏感池全吻合**:日食 15 条/血月/地狱/丛林分层/雪原暴雪/海洋/大理石花岗岩/墓地/
  月事件波表逐条一致。
- 修复 6 数值错:地牢墙色重掷 Next(3) 非 Next(4)(蓝砖曾虚高½);661 夜窗上界 <24
  (凌晨曾误出)+RollLuck;蒲公英 628 门仅{2,477}(曾草族∪雪∪冰,注释误引:4112);
  476 十周年门;稀有元素 RollLuck(十周年?50:75);专家骨堆 449-452。
- 缺池 10 条登记 docs/spawn-parity-gaps.md(多为 critter 链/海滩支/695/696/蜻蜓/侏儒,
  依赖 FindCattailTop 等基建)。**2026-08-17 二批已全量补齐**(敌怪轮昼池 critter 链/
  内带蝎/香蒲蜻蜓/晨鸟两支/695/696/海滩边缘支/侏儒两支/友好轮 isBeach+雨天香蒲;
  新增 findCattailTop 加权 reservoir/rollDragonflyType;附加只走 pendingCritterExtras)。
  ★教训:①友好轮新支必须带 spawnFriendlyCycle 外层门(:2006 链语义),曾漏致
  敌怪轮被海鸥 602 截胡+游戏内 raining ReferenceError(裸变量作用域只到
  surfaceSpawn 块);②迷你测试世界宽 <2×beachDistance(760)全图落海岸带——
  小动物采样测试须 ≥1300 宽世界且沙带放中央带,窄带采样窗边缘轮还会被
  CheckNotSpawningOnScreen 屏检拒掉(表现=产出全 null)。
  **Review 批又修 5**（自复查):晨鸟 A 漏 <9:30 门(Main.time<18000=day 轴
  4:30+5h);瓢虫写死 1/5 应 Next(butterflyChance/2)(每日掷 1-21);海滩边缘支
  水表 9/10 空过门方向反(N(10) 是 1/10 通过,应 !N(10) 拒);自定义落位被 Game
  放置段覆写(spawnNPC 非默认坐标 → customSpawnPos 标跳过 critters 找地面/
  water 扫描;香蒲附加 extras 加 ax/ay 绝对坐标);EnemyDef.defense 可选字段
  `+=` 严格空检查报错(?? 0 合并)。★N() 方向语义=N(n)=Next(n)==0(1/n 真),
  "9/10 拒"必须写 !N(n)——新代码逐支必须对方向。

## 仇恨/脱战层(运作结论)

- **CheckActive 消散系统已 1:1**:timeLeft=activeTime 750;屏内矩形(±sWidth/2+width)
  每 tick 重置;离屏倒数归零消散(Except 白名单/boss flag2);activeRange=sSize×2.1
  只管 nearbyActiveNPCs 计数(喂 rate 分层)。
- **TargetClosest 已 1:1**:曼氏距离−aggro(潜行装收窄)+镇静+1000 罚;隐身只经 aggro。
- **"离开生物群落不会脱战"——原版语义**:普通 AI 只看距离/昼夜/事件,**不看 Zone**;
  群落只决定【出生池】。常见门:守卫/南瓜王/骷髅王头 |dx|>2000‖|dy|>2000(轴向)→
  重选仍超→离场态;AI_002/AI_003 靠白天+地表+非墓地 EncourageDespawn(10);
  法师传送落点 |dx|+|dy|>2000 曼氏放弃;骷髅手 Distance>2000‖Dot≤0 退相。
- 修复 3:AI_001 flag3 补 slimeRain(史莱姆雨白天也激愤);AI_006 地下蠕虫 flag 型
  (10/39/95/117/510)玩家升地表→EncourageDespawn(300)+vy+0.2(513 沙漠外 0.1;
  621 白天 (60)+vy+1);吸血蝙蝠 158 白天地表→dirY=-1+水平翻转上飞。
- flyAI 18 格近似门只在死键 cave_bat/servant_of_cthulhu(spawner 不产)——无实际影响。

## 教训

- 代理给的"通用 2000px fighter 门"初判有误(:21934 实为 aiStyle11 Boss 家族)——
  审计结论必须回源码核行号再动手;AI_003 本体无距离门只有白天门。
- Terraria 夜晚 Main.time 独立轴:0=19:30、16200=午夜(24:00)、32400=4:30
  (Midnight 命令实证)——`time<16200`=夜前半,非"整夜"。
- RollLuck(n)≠Next(n):luck 接入后必须换 rollLuck(stats/Luck 已有),仓内多处
  平掷 N(n) 是 luck=0 等价、负运偏差——审计时逐处辨。

## 玩家死亡后的寻路语义(2026-08-19 补,用户报"恶魔眼死后左右抽搐+原地飞升天")

- **原版铁律**:玩家死亡/全灭时 `TargetClosest()` 是【无操作】——
  TargetClosestUpgraded(:78355)跳过 dead/ghost 玩家,无有效目标时 num4 哨兵
  9999999 未动 → **直接 return,direction/directionY/target 全保持原值**
  (:78421)。AI_002(:52723)/AI_014(:22943) 等照常跑,怪沿最后方向滑行,
  消散交给 CheckActive(死亡玩家在本仓实现里不重置屏内 → 750t 倒数离开)。
  **dirY=-1 恒上飞是白天驱散分支专属**(AI_002 :52707/AI_014 158 白天 :22944),
  不是死亡行为。
- 我们两处违反(已修,floatEyeAI/batAI):①`dirX=-sign(oldVx)`=朝自己速度反方向看
  → X 反复减速过零 = **左右朝向抽搐**;②`dirY=-1` 无条件上飞 = 尸体处飞升天。
  修=死亡分支 `dirX=this.facing`(seekDirX(null) 同语义)+ `dirY=this.dirY`
  (Enemy.dirY 字段持久化,活玩家分支每 tick 写入;驱散/158 白天分支写 -1)。
- 测试 tests/float-eye-dead-player.test.ts 4 例(死亡 200t 朝向 Set.size==1/
  沿用 dirY/白天驱散不回归/蝙蝠同语义)。
- ★方法论:玩家死亡=AI 收 `p=null`(Game.fixedUpdate :1163),每个 AI 家族的
  null 分支都要对"TargetClosest 无操作"语义复核——凡 null 分支里有写朝向/写
  dirY/反向加速的都是自创近似。fighterAI(保持朝向继续走)与 wormAI
  (EncourageDespawn(300)+阻尼滑行,:51532 有原文依据)本来就对。

## AI_016 鱼类 flag22 攻击门(2026-08-19 补,用户报"鱼经常蹦出水面到岸上继续蹦")

- **离水拍打(落岸随机蹦 vy∈[-5,-2]/vx±2/重力0.3)是原版行为**(:24011-24033)——
  不正常的是"经常蹦出":我们 swimAI 曾无条件朝玩家全速追(±3/±2),岸上玩家把鱼
  vy=-2 直拖出水面 → 落岸无限拍打。
- **原版 flag22 门**(:23731-23740):55 金鱼/592/607 鳉/615 海豚/688 河鲀五族
  连 TargetClosest 都不调【永不追】;其余须玩家**湿身**(player.inWater)+视线
  才进攻击档(157 巨骨舌鱼 0.25/0.2 钳 7/4;65/102/692 鲨/琵琶/虎鲸 0.15×2 钳 5/3;
  其余 0.1×2 钳 3/2)。
- **游荡档**(:23864-24004):direction 恒存撞墙翻;vx+=dir*0.1 越界(±1,615±3)
  ×0.95 → 平衡点 **1.9 px/t**(勿当"钳1"断言!);垂直 ai[0] 慢振荡 ±0.3
  (0.01 步进;157 专属 ±0.6 随 directionY 偏移);浅水检查(头顶 liquid>128 且
  脚下 1-2 格实心 → ai0=-1 上浮);|vy|>0.4 ×0.95 阻尼(157 豁免);
  撞顶/底 vy 反弹+ai0 同步(仅 !chase)。
- 测试 tests/fish-behavior.test.ts 4 例。

关联:[[spawner-vanilla-alignment]] [[spawn-progression-audit]] [[palm-chop-tileaxe-parity]]
