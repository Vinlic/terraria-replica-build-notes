---
name: achievements-port
description: 成就系统全量移植（137成就1:1+引擎+钩子+UI+三项背包修复）；图标64px/66步长8列锁定X+528；GAIN_TORCH_GODS_FAVOR唯一无类别
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T05:04:33.559Z
---

成就系统全量移植（2026-08-13）。对照 `AchievementInitializer.cs`（137 成就注册原序+图标序 1:1 逐条 diff 验证）+ `AchievementsHelper.cs`。

**架构**：
- `src/data/vanillaAchievements.ts`：注册表（条件链 Create/CreateMany/CustomFlag/Int/Float 全 1:1）+ 图标序 `ACH_ICON_ORDER` + 类别四表。BENCHED 用 `WORKBENCH_ITEMS`（ItemID.cs:1200 44 项展开）。
- `src/core/Achievements.ts`：引擎（条件状态机+localStorage `sbw.achievements.v1` 持久化+HandleSpecialEvent switch+MechaMayhem 三杀窗口+钓鱼/挖掘/跑动计数器）。内部 item id→原版 id 用 `Shimmer.vanillaIdOfItem`（勿再造助手）。
- 钩子在 Game.ts：onEnemyKilled（vanillaNetId）、ItemDrop 拾取路径（仅入包部分，合成/初始装备不经此=原版语义）、craft/vanillaCraft、breakTile(byPlayer)（3 个玩家工具调用点传 true；爆炸/液体路径 false）、进世界基线 `achOnWorldEnter`（扫包+装备态）、progression events（1/5 黎明、3 黄昏日食、6 砸祭坛、7 砸珠、9 WoF、10-13 入侵胜、14/15 月事件15波、19 金钥匙开锁、22 祭坛用、23 DD2 T3）、zone-reach 15t 节流（墙86蜂蜜/墙62蜘蛛/地狱层/特殊种子/地表菇/墓地）。
- UI：`src/ui/AchievementsUI.ts`（菜单 rgba(33,43,79,0.8) 半透+4分类过滤+Advisor 提示牌）+ 背包顶栏"成就"按钮。

**关键坑**：
- 图标帧 = `Achievements.png` 64px/66px 步长/每行 8 帧；锁定态 X+528 灰阶列块（UIAchievementListItem.cs:57-60）。
- GAIN_TORCH_GODS_FAVOR 是原版唯一无类别成就（cs 无其 RegisterAchievementCategory 条目），菜单恒显示不受过滤影响。
- `sw-loadout-flash` 白闪 class 曾残留不摘 → display:none→block 使 CSS 动画重播 → 进背包全体白闪；修法=600ms 后摘除（切预设白闪本身是原版行为保留）。
- 垃圾桶空槽画 Trash.png（ItemSlot.cs:2514，brightness+alpha 0.39）——此前 L133 注释误判"原版无图标"。
- .sw-panel 半透 = UIPanel Color(63,82,151)*0.785 → rgba(38,50,90,0.78)。
- 探针 `scripts/_achprobe.mjs`（17 步）验证全链；私有 5201 实例。
- 遗留偏差：暗影箱 event 20（BIG_BOOTY）未接线（锁定箱模型统一金钥匙）；NOT_THE_BEES（蜜蜂套装+1121）未接；event 8/9/16/20/21/22/25 等 HandleSpecialEvent 深层语义（幸运/矿车撞人/偷看/摸宠物/仙女等）待对应系统接通时补。
- 137 数量教训：原版成就就是 137 个不是 94——以 C# `new Achievement(` 计数为准。

**review 修复（2026-08-13 第二轮）**：
- ★ 计数条件 load 曾写 `done: v >= 1`——中途进度（BULLDOZER 5000/10000 落盘后）重载会误判完成；改为对 def 阈值判定。
- CreateMany 的 doneIds 部分进度持久化（save 格式加 `m` 桶：{ach:{condIdx:[ids]}}）。
- MechaMayhem 双子门（CountKillForAchievements NPC.cs:80631-40）：125/126 需另一只也死才通知/计杀——门在 Game.onEnemyKilled（引擎 kill 本身不管双子）；SpawnBoss 序 = Clear(生成前扫描)→Start(生成后)，场清判定 Twins=125&&126 双眼同在（cs:495-503）；boss 击败处不加 Clear（原版无）。
- HandleRunning 门 `velocity.Y==0`（Player.cs:27925）：仅着地跑动计入 MARATHON_MEDALIST——接 player.onGround。
- HandleMining 是每次成功破坏一 tile 调一次（Player.cs:52882）——与 breakTile(byPlayer) 1:1 ✓ 原实现正确。
- 死代码清理：advisorList 删除；UI 帧数学统一走引擎 iconFrameOf。
- 持久化粒度：flush() 10s 节流落盘（Game tick%600）。
- ★ 既有缺口（非本次）：flags.hardMode 全引擎无置 true 点（仅 wld 导入带入）——WoF→InitializeHardMode 未实现；event 9 暂锚 downed_113，实现后应迁移。
- 私有 vite 清理教训：SW_PORT 是 env 不在进程 cmdline，pkill -f "port 5201" 匹配不到——用 `lsof -ti tcp:5201` 杀。

**遗留补充批（2026-08-13 第三轮）**：
- 困难模式激活：并行会话同题实现 `src/world/gen/vanilla/HardmodePass.ts`（已接线 WoF 击杀链含我的 event 9）——我删了自写 HardmodeInit.ts 防双轨；修补其两缺口：①直写 st.type/st.wall 绕过 onTileChanged → chunk 不标Dirty条带不重渲染（改 setTile/setWall）；②hive>200k 门（225 Hive/230 CrispyHoney 转换，cs:76433-76445）被误删——已补回三表。测试 tests/hardmode-init.test.ts 3 例（条带/幂等/猩红表）。
- 成就六处接线：派对 prog(25)（自然+纪念碑×2）、橡实 plantedAcorn（CONSERVATIONIST）、陷阱弹致死 event 4（hitPlayer 加 trap 参，Projectile.cs:13804 trapDebuffSource 语义=被陷阱杀死；反射弹不传）、图鉴 100% prog(29)（achCheckBestiary 挂杀/遇/聊三登记点）、9+ 随从 event 6（召唤后计数）、蜜蜂套装+蜂枪 1121 event 3（NOT_THE_BEES，武器 choke 点 critTotal 处）。
- 仍缺（系统未接）：暗影箱 event 20（锁定箱统一金钥匙）、FREQUENT_FLYER 护士付费（无护士治疗对话）、TALK_TO_NPC/PET_THE_PET/FIND_A_FAIRY/LUCKY_BREAK/VEHICULAR、Journey 研究 45/46、GOING_OLDSCHOOL。

**系统补全批（2026-08-13 第四轮，/goal 继续补全所有系统）**：
- 护士付费 → handleNurseService（FREQUENT_FLYER 10000 铜计数）——nurseHeal 本就存在，只缺成就钩子。
- 摔落幸存 → event 8（Player.cs:25085-25090：摔伤后 !dead && hp≤maxHp/10 → LUCKY_BREAK）——接 Player 落地摔伤结算段。
- **矿车撞怪系统**（新，Player.cs:27225-27296）：速度>4 扩盒命中敌怪（仅敌怪，城镇 NPC 不伤）；伤害=DamageVar(25+55×速比)（SuperCart 50+100×；hardMode ×1.5）；击退=10+40×速比；暴击=max(近远魔)；命中后 iframes 覆写 30t；击杀→event 9 VEHICULAR_MANSLAUGHTER。在 Minecart.fixedUpdate 玩家回写后。
- **锁定箱样式驱动重写**（Player.cs:32684-32724 + Chest.Unlock/IsLocked 1:1）：锁定=样式属性（帧区间）非数据旗标——tile21 style2=金钥匙327/event19、**style4(帧144-178)=暗影钥匙329**（地狱暗影箱！）、style23-27(帧828-1006)=群系钥匙1533+style-23/帧回退180/世花门/event20、style36/38/40=金钥匙无事件；tile467 style13=4714/世花门/event20。解锁=四格 frameX-偏移+手动 markDirtyArea（直写帧不触发监听）。**地狱箱从此需要暗影钥匙**（此前无旗标直接开）。
- I_AM_LOOT event 16：打开金箱（sheet21 帧∈[36,72)=style1）→ 接 tryOpenCchest 开箱完成点（Player.cs:32786-32788）。
- Main.cs:39703 澄清=event 27（Dryad 世界纯净）非经典标题；GOING_OLDSCHOOL=菜单经典模式钮（TitleMenu 无该钮）仍缺。
- 仍缺系统：坐骑（非矿车）/宠物实体、NPC happiness（TALK_TO_NPC）、Journey 研究 45/46、GOING_OLDSCHOOL、PURIFY_ENTIRE_WORLD(27)、I_AM_LOOT 已接。
