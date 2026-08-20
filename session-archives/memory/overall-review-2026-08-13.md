---
name: overall-review-2026-08-13
description: 整体review四维度:管线三pass补缺+两顺序归位/BossAI十修(underworldLayer=陨石线大坑)/getGoodAdjustments整族缺失=下批首选/月事件Boss无boss位误占槽
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-13T11:02:32.846Z
---

# 整体 review（2026-08-13 午，四维度并行审查 + 主循环修复）

**方法**：四路代理（BossAI 新码/渲染新码/运行时事件+存档五路/管线槽位）对照 1456 逐行实读 → findings 按文件热度分层处置（安静 ≥70min 的直接修；热区只登记）。总账见 `game/docs/worldgen/pass-audit-2026-08.md` 末节。

## 高价值教训（防再犯）

1. **UnderworldLayer 恒 = maxTilesY-200**（Main.cs:2863 计算属性），≠ GenVars.lavaLine（岩浆线≈(rockLevel+h)/2+50..79，高约 150 格）——spawnWOF/墙扫描带误用 lavaLine 会整体上浮 150 格。与 [[plantera-parity-audit]] 的"UnderworldLayer=h-200 陷阱"同源复发，**凡地狱高度带一律 h-200**。
2. **月事件 Boss（325/327/344/345/346）与地牢守卫 68 在 1456 SetDefaults 无 boss=true**——占 Boss 槽会误播"已被击败"/误写 downed/误发 Boss 药水；原版只有波次计分+掉落。月 Boss 首杀走 SetEventFlagCleared(NPC.cs:80011-80033,带月别门) 才投灯笼夜。
3. **"注释以 A 理由跳过 B 代码"是高危模式**：wofEyeAI 曾以"无 g 分支"为由连 expert 加档块(:26236)一起跳过——expert 块是真代码。
4. **审视捆绑槽位**：实现 1:1 但执行位错误 = 仍是顺序偏差（Speleothems 捆在 20842 位/LihzahrdAltar 终保捆在 15911 位——后者对 Pots/Traps/TileCleanup 的祭坛扰动无人回滚）。
5. **沉降型 hook 时序**：FallenLogDestroyed 原版在 KillTile【尾部】（清格后）——挂在 breakTile 头部会让已毁倒木当夜仍出仙女。同类"事件响应 hook"一律核对调用点在清除前还是后。

## 已修清单（13 处代码 + 2 注释勘误）
管线：SunflowersPart2(20043,**普通种子向日葵唯一来源**——其稀有度是原版语义：w*0.002 带宽采样+2×4 净空+整砖门,种子 9293480 实测 0 株,42 号 38 株)/JunglePlantsPart2(20310,PlaceJunglePlant 233 两分支)/MudWallsInJungle(20963,墙 2/59→15 边缘掷骰)/两顺序归位。BossAI：上述 1-3 类十修。运行时：倒木延迟重扫/freeCake 优先级/anyDanger 集合/读档重掷 firefly/双派 id 死码。

## 登记未修（热区或需决策）
- **getGoodAdjustments 整族缺失**（NPC.cs:17874-18027，FTW scale+数值+**扩盒**）——下批首选，注意与专家档"只缩贴图不缩盒"语义相反。
- fireFlyFriendly/Multiple 三消费点/地下仙女链/WldParser 导入丢 cultistDelay(并行在途)/PlayerLOS 应为屏幕×1.2 矩形/渲染六小项(南瓜王披风等)/双子低血加速/毁灭者 AI_037 淡入链门 128。
- 金标 world-final 维持红（并行会话 MicroBiomes/Traps 在途），其收尾后自然消或其会话自再生。

## 追加（2026-08-13 下午）：placeBoundRescueNpcs 对齐原版（用户裁决+实证链）
- **实证三件套**：①WorldGen SpawnStarterNPCs(cs:19830-20041) 普通种子分支只 NewNPC(22) 向导(:20037-20041)无 bound；②bound NPC 唯一来源=NPC.Spawner 链(三人组 :1994-2008/造型师 :1576/高尔夫 :1600/机械师 :2563/税务员 :4777)；③Spawner.SpawnNPC(:5146)=普通 NewNPC，bound 形态即类型本体。
- 收口：生成期五只 bound 放置+入驻轮困难模式巫师补放**全移除**；蜘蛛巢 354 分支补齐(:1579-1581,曾"注释保留"跳过)/589 补 !savedGolfer+spawnBound 占位/123 补 !savedMech/trySpawnEnemy 六路转换(105/106/123/354/589/685→bound TownNPC;534 走净化粉)。回归 tests/bound-chains-vanilla.test.ts 四链全过。
- **断链复查抓到一个真断点并修**：applyPowder 的税务员分支只扫 npcs 桶 bound TownNPC——生成期放置移除后 534 以【敌怪】掷出，弹粉永远扫不到=税务员转化链断。已补敌怪桶 534→Transform(441)(:81850 换型+保血量+底边对齐+homeless) 段。**净化粉 66/67/2886 在树妖商店全在（shop 20）——旧注"未进货"过时**。六路转换抽成 `trySpawnBoundTownNpc` 方法（可测性）。
- **全链 e2e**（scripts/_boundchain-e2e.mjs，私有实例 5203）18/18 PASS：534 弹粉转化/六路转换+唯一门/解救写旗后 3000 掷链绝迹/**真弹体飞过 534 实际转化**/存档快照 bound 标往返。
- **方法论**：行为对齐前先取三段实证（生成期放什么/运行期唯一来源在哪/SpawnNPC 语义），缺一段就是凭感觉改；**移除一条兜底路径前，必须把原先只靠该兜底可达的所有消费者逐一接上原版路径并 e2e**（534 断点即此教训）。

## 追加二轮（2026-08-13 下午）：入驻条件表全量对齐
- 权威表 = Main.cs UpdateTime_SpawnTownNPCs(:65021-65570) 条件集 + num42 优先链 + WorldGen.CheckSpecialTownNPCSpawningConditions(:4919，仅 160 松露人有地表蘑菇房特判) + 五个 NPC.SpawnAllowed_*(:7046-7170)。
- 修 5 处：**santa 漏 downedFrost 门**（曾 xMas 即到——霜军团旗在入侵胜利块 flags.downedFrost）/angler 369 重生门缺失（死后再也不来）/tavernkeep 550 整链缺失（spawner :1565 醉酒酒保 579[ReadyToFindBartender=NPC.downedBoss2]→触碰 Transform(:19806)→入驻 :65283，此前不可达）/造型师优先位/史莱姆第二轮原序（铜→蓝→酷→老→紫→红→黄→彩虹）/公主门补 angler+tavernkeep 凑 24。
- 探针 _boundchain-e2e.mjs 扩到 28 断言全 PASS（含 santa 门双向/公主门缺一即关/579 链与旗闭环）。
- 登记缺口：兔 656/猫 637/狗 638（bought* 旗依赖动物学家许可证商店未实装）、松露人蘑菇房特判（既有备案）、spawner 链内 690/244 块位置序差（既有，1/80 门主导影响边缘）。

## 追加三轮（2026-08-13 傍晚"继续处理完整"）：备案缺口清四项
- **宠物三只全链落地**：★兔证=4910（4831-4837 是捕捉笼，勿混）+4830 狗证注册；使用=LicenseOrExchangePet（首用置 bought*/在场重用换皮（无变体系统备案）/缺席不消耗）；动物学家进货 4829 无门/4830 图鉴≥25%/4910 ≥45%（Chest.cs:3265-3280——shopstock 手工补条+shopCondOk bestiary25/45 门）；优先链 :65567-65574 序 兔→猫→狗；IsTownPet（NPCID.cs:4444=宠物+全城镇史莱姆）免房流浪生成；json 补 637/638/656（帧数取 Main.cs:65994 npcFrameCount 表 28/28/27——**宠物帧数权威源是这个表不是猜除法**）。
- **unlocked* 永久旗族**（WorldGen.cs:5510-5560 到访即置，九面旗）：五个 SpawnAllowed_* 首位查旗+到访写旗——修"商人到访后花光钱死亡永不回归"。
- **松露人蘑菇房特判**（:4919-4946）：地表+蘑菇 tile≥100，替代"全域找房"备案。
- **探针方法论教训**：①优先链一周期只放一人——测低优先级条目须预置全部高优先级在场；②前段断言副作用会污染后段（杀酒保关公主门→酒保重生抢先）；③复用存档世界有图鉴/残留 NPC 进度，绝对断言改恒等式或先清残留。
- 探针 33 断言全 PASS；49 项 vitest 绿；私有实例已收尾。
- 仍登记（跨批次遗留）：getGoodAdjustments 整族/fireFly 三消费点/地下仙女链/PlayerLOS 屏幕矩形/RollLuck(20)/渲染六小项/双子加速/毁灭者淡入链门/spawner 690/244 序差。

## 追加四轮（2026-08-13 傍晚"继续"）：遗留清账批二（安静区避让策略）
- **文件避让纪律落地**：开工前 ls -lt 探热度——Enemy/ScaleStats/Game 15 分钟内被并行会话改 → getGoodAdjustments/PlayerLOS 本批放弃；做安静区（VanillaSpawner 14:17/RuntimeEvents 13:10/WldParser 13:49/bossAI 13:05）。
- **四件落地**：①萤火虫成群附加（fireFlyMultiple 三消费点 :2327/:4419/:5767——spawner `pendingCritterExtras` 侧信道+Game 落位段消费，"单返回值 API 限制"备案全核销）②地下仙女链整支（fairyLog=扫倒木置位 world.fairyLog 运行时位/RollLuck(500·hardMode×1.66)/深度窗/AnyHelpfulFairies Game 喂入→583-585 ai2=2）③三人组 N(20)→rollLuck（原文就是运气缩放）④WldParser 导入丢 cultistDelay 修复（**SaveData.cultistDelay 是顶层字段非 header 内——缩进核对教训**）。
- 回归：tests/firefly-fairy.test.ts（主只+四附加/仙女命中/双门关门）+ 既有套件全绿。
- **仍登记**：getGoodAdjustments（下批首选，需 ScaleStats/Enemy 冷却）、PlayerLOS、渲染六小项、双子加速、毁灭者淡入、spawner 690/244 序差。

## 追加五轮（"继续补齐"）：双子低血加速
- 双子阶段三弹幕节奏 1:1（:26971-26990/:27598-27612 同表）：固定节拍 → 血量阶梯累积器（+1/ tick，<75/50/25% 各+1、<10% +2，满 180[雷眼]/8[魔眼]+视线清零发射）+魔眼 Item34 火焰音。**仍登记**：getGoodAdjustments（并行会话持续占用 ScaleStats/Enemy/Game——连续两批避让，下批开工前先探 mtime）、PlayerLOS、渲染六小项、毁灭者淡入、spawner 690/244。

**How to apply**：审查 findings 必须实读原版确认（本批三处勘误都出在"任务清单/旧注释"而非代码）；测试断言稀疏生成时先多种子扫描再锁种子（向日葵案例）；`rng.int(a,b)` 闭区间 = Next(a,b+1)，Next(n) 用 int(0,n-1)，短路求值序要保。

## 追加六轮（"继续吧"重勘轮，计划在 ~/.claude/plans/splendid-weaving-moth.md）
- **重勘铁律**：大量并行迭代后开工前必重新 grep + ls -lt（getGood 曾疑被并行做掉，实测零命中仍缺）。
- **690 雕像宝箱怪块归位**（vanilla :1478 = 入侵块后/酒保蜘蛛巢前，纯挪位 757B 逻辑不变）。
- **勘误重分类**：244"序差"实为**整支缺失**（微光 tile 落脚小动物链 :1490-1563 十支）+ dual-dungeon 支（:1484→82/316）缺失——登记待补。
- dungeon-spawn 失败=并行会话 DungeonPass.ts:420 `isDW` 声明序在途错误（非本批）——**第三方测试失败先读栈定位归属再动手**。
- 仍登记：getGoodAdjustments、PlayerLOS、渲染六小项、毁灭者淡入、244 微光链、dual-dungeon 支。

## 追加七轮（"不用等冷却"）：PlayerLOS 落地
- 两处 playerLOS 换原版屏幕×1.2 矩形语义（:69500-69515 点矩形∩视口矩形，camera.viewW/H÷zoom×0.6+8）——勿再当"视线"理解。
- 用户解除温度闸后热文件直写可行（Edit 精确匹配兜底+改完只对本批行号过滤 tsc）。
- 仍登记：getGoodAdjustments、渲染六小项、毁灭者淡入、244 微光链、dual-dungeon 支。

## 追加八轮（新会话"继续收尾遗留四项"）：getGoodAdjustments 整族落地
- ScaleStats.applySeedAdjustments 三私有方法 1:1（zenith:17774→getGood:17874→十周年:17795 else-if 互斥，先于 ScaleStats:17791）+ fromVanilla 接线。测试 scale-stats 第 12 节 48/48 绿。
- **易错点全踩清**：①39-41 `scale=1.1f` 是赋值非乘法+remix×1.2；②getGood else 提前 return=扩盒只对命中分支；③十周年无 else-return=扩盒无条件（未列族 s≠1 二次乘盒是原版怪癖，史莱姆王 122→152 照抄）；④扩盒两级 (int) 截断 `(int)((int)(w0×s0)×scaleNew)`——113/114 s=1.2、134-136 s=1.25 真二次乘；⑤defDamage 快照在 getGood 前→baseDamage 用未调基值；⑥渲染乘区=vanillaScale(scaleNew/s0) 自动进 Renderer:2213；⑦netID 覆写点改相乘（SetDefaultsFromNetId→WithScale 链；netID 基类型表与两列表零交集）。
- 备案四项：FTW sizeScaleOverride 膨胀 (o+o²)/2(:8362)/图鉴假人还原/canDisplayBuffs/netID 族 anniversary 二次盒。
- **教训：块注释体内 `**/` 会提前终止注释**（并行会话 VANILLA_BOSS_IDS 注释写 markdown 粗体 `**396**` → 全 Enemy 引用测试转译炸；修法=反引号强调）。
- 红灯归属法：18 失败全为并行在途（DungeonPass 17:47/VanillaSpawner 17:48 编辑窗口+物品存储玩家域批次）——按 mtime+失败域判定，勿接锅勿动。
- 仍登记：渲染六小项、毁灭者淡入、244 微光链、dual-dungeon 支。

## 追加九轮（新会话收尾轮）：四项全清（交接清单清空）
- **getGoodAdjustments 整族**（见八轮）+ **毁灭者链门淡入**（fadeNpc 头循环；134-136 保 255 不置 alphaFade）+ **渲染六小项**（327披风/328双臂/36 BoneArm3/拳链FTW+8Y/259-260强制亮彩实装；396-397与693登记）+ **244微光链+dual-dungeon**（见台账批九）全落地。
- **新坑与勘误**：①台账"244 微光 tile"实为**墙 id 244=Shimmer**（num=落脚上格墙，TileID 244 是 BubbleMachine 勿混）；②36 BoneArm3 的门 localAI[3]==1 全链=**Red Hat 彩蛋**（SpawnSkeletron redHatMode :81269 置头 ai[3]，手 :22304 镜像）——渲染按 master.ai3 直读；③十周年函数无 else-return=扩盒无条件（未列族 s≠1 二次乘盒原版怪癖）；④259/260 强制亮彩必须在 compositeLight **后**绘制（全屏乘光会压掉下限色），drawBrightVines+主pass跳过+scratch染色；⑤localAI 是**各 AI 文件独立 WeakMap**——跨文件读须导出口（moon_events 的 localAIOf）；⑥Enemy 字段叫 despawnTimer 非 timeLeft。
- dual-dungeon 前置系统顺手补齐：Player.insideUnbreakableWalls（8 向射线+5 位环移）+ DangerousDungeonCurse 双档位表（Game 比较传 spawner）；备案 wallColor≥16 分层门。
- 探针方法论增量：渲染像素验证用 page.evaluate 内 `import('/src/entities/Enemy.ts')` 直取模块 + 帧边界 rAF 后原型直调 draw 方法（零光照图硬验证）；Boss AI 会带实体离采样窗——采样前手动复位位置；0.75H 小世界即地狱层（岩浆背景自发光），黑暗腔验证须放 rockLevel+120。
- **全部测试断言对应并行红灯均按 mtime+失败域归属，零误接锅**（firefly-fairy=并行 spawner 编辑 RNG 序变化，连续三轮同象）。
