---
name: pets-port
description: 宠物系统（vanity/light pet 86件提取+跟随实体+装备驱动存续+移动端召唤键）；DefaultToVanitypet 参数序坑；buff 栏宠物图标未接
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T09:36:16.992Z
---

宠物系统（2026-08-13，/goal 宠物批）。

**数据**：`tools/extract-pets.mjs` ← Item.cs 双模式提取 → `src/data/vanilla-pets.json`（86 件=79 vanity+7 light，85 款投射物贴图全在管线）。
- 模式①：case 块内 `buffType=N`+`shoot=N` 且非 consumable；
- 模式②：`DefaultToVanitypet(projId, buffId)`（:47549，**参数序 projId 在前 buffId 在后**——与直觉反，实证 buff=317 ∈ Main.vanityPet 表）；
- light 分类 = Main.cs `lightPet[N]=true` 赋值表抓取。
- 唯一缺口：item 425（特例）。equip.json pet/light 分类与本表交叉全覆盖（除 425）。
- **[[achievements-port]] 成就挂钩**：PET_THE_PET 依赖宠物系统（event 21 触发点 Player.cs:32892/32941 宠物交互——本批未接，下批接）。

**运行时**：
- `src/data/vanillaPets.ts`：`petInfoOfVid(vid)` → {buff, proj, light}。
- `src/entities/PetFollower.ts`：统一跟随 AI 近似（肩后 -facing×22/-26px + 正弦浮动 ±4、钳速 6px/t、>1200px 瞬移、横排帧假设 fw=img.height、随 facing 翻转）。**逐款专属 AI（Projectile.AI 各宠物分支）未移植**——二期。
- Game：`updatePets()` 每帧（Player.UpdatePet/UpdatePetLight :17147-17187 装备驱动语义：槽0宠物/槽1光宠，装备在位+未隐藏→ensure 跟随体（同款保留/换款重生），卸装/隐藏/死亡→消散）；`togglePets()`（TogglePet/ToggleLight hideMisc 翻转 :17191-17208）。
- MobileControls 坐骑/宠物键：宠物/光宠 → togglePets 真接线（原占位 toast 废除）；坐骑（槽3）仍 toast。
- 探针 `_mobileprobe.mjs` ⑩ 段 5 断言（生成/跟随/收回/重召/卸装消散）28 项全绿。

**坑/偏差（已记录）**：
- 宠物 buff 不入 BuffState（BuffType 枚举无 62 款 pet buff）→ **buff 栏无宠物图标**；pet 状态用 petHidden/petFollower 字段。原版 buff 即宠物存在标志（FindBuffIndex 判重）。
- 光宠不发光（LightingEngine 动态光未接）。
- 桌面端无宠物切换键（原版=装备界面上点宠物槽图标 Main.cs:40684；移动端按钮已接，桌面靠卸装/装备控制）。
- 603 胡萝卜→buff40/proj111（兔子）实证锚点。

**三审补完批（2026-08-13，stop hook 追单）——审查登记的宠物行为缺口全部实施**：
- **fly 距离分档加速度**（FLY_ACCEL_TIERS 表 ：56560-56640：380/198/815/817/774/1046 近远档）+ **Y 轴交叉零点 ×2**（accelTowardY ：56666-56674 总步 3acc，X 轴仅双步）。
- **Wisp(211) 远距追击闩**（wispFar = localAI[0]，:56867-56925）：>200 置位、恒速 12 直取（<12 取位移）、脱离门 d<10 且玩家静止且着地；中段追击实测 ≈12 速、追到玩家身边 ✓。
- **960 Chester 目标偏移 70px**（:56042-56050 玩家移动取 direction、静止取方位）+ **1027 GlowPine 28px**（:56014-56018）。
- **追赶飞行 <60px 漂移**（:57557-57561 近距不重定向）+ **玩家高速动态提速**（fly num111 ：57540-57543 / ground num182 ：59145-59148 取 max(|pvx|+|pvy|)）。
- **313 Spider 翻转门**（:59361 type!=313 恒不翻——draw 内 projId 门）。
- **抚摸交互距离门**（IsProjectileInteractableAndInInteractionRange :22874-22886 = inTileRange 盒）补进 Game 抚摸判定。
- OwnerRef 加 vx?/vy?；pet-ai.test.ts 追加 6 用例（42/42 绿）。
- 测试教训：Wisp 远距追击断言要抓"中段"速度——追到底后 d<12 速度=位移自然趋小，断 sp>8 会假红。

**遗留清零批（2026-08-13 第二轮，/goal 处理遗留）**：
- ★ **PET_THE_PET 已接**：右键悬停宠物 32px → event 21（Main.cs:37404 PetAnimal 语义）+爱心尘；优先于地块交互。
- ★ **光宠已发光**：updatePets 内 addLight(1.1/1.0/0.85)（逐款色差登记二期）。
- ★ **桌面宠物眼睛开关**：杂项页槽 0/1 右上 👁 按钮（Main.cs:40682-40691 InventoryTick 语义，光标空门=heldStack）→ Game.togglePetSlot(slot)；移动端聚合键仍走 togglePets。
- **damageVar 1:1 helper**（ScaleStats.ts，Main.cs:65597-65620：±15% + luck 正/负重掷取大/小）——替换荆棘反伤与矿车撞击两处裸随机。
- **石化摔伤分支**（:25066-25075）：(格数-2)×20、无安全阈值/无翼马掌豁免、else-if 独立链 + event 8。
- 护士排除表 NurseCannotRemoveDebuff（BuffID.cs:32）与本仓 DEBUFFS 零交集（实证）——注释登记。
- buff 栏宠物图标仍缺（62 款 BuffType 扩展大）；逐款宠物 AI 仍近似。

**遗留总攻批（2026-08-13 第三轮，/goal 全部补齐+子代理）**：
- ★ **多会话撞车协调**：并行会话同步在做宠物 buff 图标（UI.ts petBuffBlocks/activePetBuff 装备槽派生方案）/坐骑引擎（src/entities/Mounts.ts MountInstance 637 行+useMountItem+ridingMount 全链）/NPC 快乐度（vanillaHappiness.ts+对话按钮+成就 event 20 PriceAdjustment≤0.82）——**我派发的 A/C/D 三个子代理已 TaskStop 防重复实现**；B（宠物 AI 家族）/E（Journey 研究+经典标题）继续（彼时无冲突）。
- **event 27 PURIFY_ENTIRE_WORLD 已接**：src/world/WorldAlignment.ts（CountTiles/AddUpAlignmentCounts :71160-71296 等价一次全扫：地表段权重×5、三阵营集 TileID.cs:325/333/343、solid 基底{2,477,1,60,53,161}+阵营、百分比 round+进位1）+ dryadWorldStatus（Lang.cs:246-288 分支表+描述行全 1:1）；树妖对话新增 'status' 按钮（NpcButtonId 双 union 加成员）→ 纯净触发 event 27。差异化登记：一次性直扫非逐列 RLE（求值等价）。
- 按钮标签教训：LegacyInterface.101="击杀数"非世界状态——硬编码'世界状态'并注释。

**review 修复（2026-08-13 宠物批二审）**：
- ★ 提取器曾混入 **24 件召唤杖假阳性**（Pygmy Staff 1157 等：buffType=随从buff+shoot=随从弹 与宠物同模式，唯一区分=宠物恒 damage=0）——提取器加 damage>0 排除门 + **buff∈vanityPet∪lightPet 强不变量校验**（exit 1）。修正表 86→62 件（55 vanity+7 light）。此前"86 件"含脏数据。
- 暗影钥匙 329 **不消耗**（Player.cs:32716 flag16=num78!=329；bank4 分支 :32750 同门）——只验持有（countVanillaItem>0），金/群系钥匙才扣。
- 矿车速比分母改 **p.maxRunSpeed 动态 getter**（PLAYER_WALK_MAX×buffs.moveSpeedMult×equipStats.moveMult——曾用常量 3，有速度配饰时伤害虚高）。
- 护士费用 1:1 重写（GetNurseHealCost :39463-39511）：(缺血+100×可移除debuff)×进度倍率链(石头人200/世花150/三王100/困难60/骷髅王|蜂后25/世吞|克脑10/EoC3)×专家2——旧 0.75×缺血近似废。BuffState 加 DEBUFFS 集+debuffCount+clearDebuffs（护士同时清 debuff）。折扣 0.8（discountAvailable）未实装登记。
- 陈旧 locked 数据旗标（导入存档脏数据，样式不在锁定集）→ 清旗标直开，防金箱帧错转木箱。
- DamageVar luck 重掷段未建模（登记，影响微小）。
