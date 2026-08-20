---
name: vanilla-solid-audit
description: tileSolid 全表对账+高门自动通行(DoorOpeningHelper)+6 个可通行修正
metadata:
  type: project
---

2026-08-10 碰撞系统性审计（用户 marks 文件驱动：Tall Gate 388 五格标注）：

- **高门机制**（DoorOpeningHelper.cs）：388 关=tileSolid true（阻挡）、389 开=非实心；
  "原版可通行"=碰撞自动门：玩家 hitbox 与门矩形(16×96)相交→ShiftTallGate 自动开
  （WorldGen.cs:51747：保帧换 type、SoundID 8、锚点回溯 frameY%90/18、5 格整体校验），
  离开外扩 1px 矩形→自动关。实现：Door.ts shiftTallGate + Game.updateTallGateAuto
  （openTallGates Map 追踪）；v_389_tall_gate_open 新注册（solid:false，wld 导入 389 已有映射）。
  E2E：贴近自动开/离开自动关/熔炉 isSolid=false 三项验证过。
- **tileSolid 全表对账**（提取 Main.cs 319 处赋值+循环段 vs 我们 363 个 v_ sheet 的 solid）：
  mismatch 仅 7 个，已修：furnace(17)/v_51 蛛网/v_205 猩红藤/v_352 荆棘/v_340 活性诅咒火/
  v_131 致动关闭石 → 非实心；v_476 高尔夫球洞 → 实心。
  自定义家具 defs（桌/椅/床等）默认 solid:false 与原版一致 ✓。
  提取脚本注意：for 循环赋值段（727-732/255-268/435-439/50x gemspark）需正则特判。
- 遗留：蛛网减速（原版 -45% 移速）、荆棘/诅咒火接触伤害未接（现在纯可穿）。

## 附：fighterAI 飞天修复（同日）
- 根因：fighterAI 四级跳缺 velocity.Y==0 前置（原版 AI_003 内 44 处跳跃全部带此门）
  → 空中贴墙每帧 vy=-8 → 沿墙飞天贴天花板，主角靠近（facing 变化）才掉。
  修：movingInto 增加 this.vy === 0。
- "NPC 倒着走"排查结论：镜像链（facing>0→scale(-1)，贴图默认朝左=原版同构）、
  facing/vx 异号率 E2E=0、extra 表=原版 ExtraFramesCount（17:9/18:9/22:10）、
  帧数=贴图高度/56 全对——未能复现，待用户提供具体场景。

## 太空步根因（用户澄清"偶发"后破案）
- TownNPC 游走掷 facing=0（站立意图）时无刹车：vx 保持 ±0.8 惯性滑行，
  渲染 facing>0 才镜像 → facing=0 显示默认朝左贴图 → 向右滑行显示朝左 = 偶发太空步。
  修：wantDir===0 时 ±0.1/tick 主动刹车（原版 NPC.cs:54096-54106 驻留减速 1:1）。
- 贴图朝向排查结论（多轮像素法均不可靠）：原版约定=NPC 表默认朝左
  （Main.cs:22985 spriteDirection==1 翻转 + AI_007 spriteDirection=direction），
  我们的镜像链与之同构，无需改。行人帧"前倾/下巴/瞳孔"等启发式在帽子/胡须/
  携物 NPC 上全部失准，勿再用于判定朝向。

## 地狱熔炉独立贴图（同日追问）
- 旧状：WldImport 76/77 都映到 'furnace'（共用 sheet 17）——76 实为狱石砖（TEdit）、
  77 实为地狱熔炉（专属表 Tiles_77，3×2，非实心+火光）。
- 修：注册 v_77_hellforge（VAN(77,3,2) + light+mapColor#EE5546）；导入映射
  76→v_76_hellstone_brick、77→v_77_hellforge(copyFrame)；白名单 tiles+=77 重建 atlas
  （TILE_NAME_ITEM_BY_SHEET[77] 自动=item 134 Hellforge → 名字链自动通）。

## 全量家具对齐（同日收尾）
- 审计两维：① TILE_MAP 全映射 sheet 一致性 → 修 61/74（都误映 tallgrass）：
  61=丛林矮草(16x20)、74=丛林高草(16x32 两格)新注册 v_61/v_74；现映射 0 不一致。
  ② 家具 fw/fh vs TEdit frameSize + solid vs tileSolid → 仅 platform（设计内单向）。
- 发光（tileLighted）：56 个缺口，从 ApplyTileLight 两段可信区（L450-950/L2600-3151；
  **L1336-2500 是透射率表会污染，勿取**）提取 26 个 sheet 色值写入 def.light。
  遗留 29 个：动态色（126 迪斯科/429 导线灯泡/209 传送门炮）需扫描器特例；
  其余在中段 case（蜡烛 173/174、火山 593/594、玻璃窑 302 等需逐个确认非透射污染）。
- 发光二轮：扩大可信区至 [344-1335]+[2600-3151] 再提 19 个（蜡烛 173/174 暖光按蜡烛族、
  火山 593/594 橙、灯柱 92 白、陨铁矿 37 暗橙、和平蜡烛 372 粉等），累计 45/56。
  剩余 11：19 平台/20 树苗（原版值疑似透射污染且视觉不发光，跳过）、
  126 迪斯科球/429 导线灯泡/209 传送门炮（动态色需扫描器特例）、
  350 火星板/109 神圣草/125 水晶球/84 药草/76 狱石砖/638 灰烬藤（中段未确认，防污染留白）。

## 遗留发光全部补齐（同日）
- 静态 +3：638 灰烬藤 [83,38,13]、125 水晶球 [0,27,54]（0.3/0.6×num≈0.35）、
  350 火星板 [26,26,26]（-cos 脉冲 0..0.2 静态近似）。累计 48 静态。
- 动态特例 TileLightScanner.specialTileLight（已导出+回归测试 tile-light-specials）：
  126 迪斯科球（frameX<36→FlickerClock.discoColor）、429 导线灯泡（frameX/18 位段
  +0.5R/G/B +0.2 致动）、209 传送门炮（234/252 紫、306/324 橙 ×0.65 近似）、
  84 开花药草（style2 闪烁暗红/5 火焰草/6 颤骨草）。
- 确认不发光 4 个：19 平台/20 树苗（值来自透射开关 L1284 区=假阳性）、
  76 狱石砖/109 神圣草（扫描器无 case）。
- **顺手修了用户 WIP 的 serialize.ts rleTiles 游程比较 bug**：raw id 与映射后稳定 id
  比较（st.type[i+run]===t）恒不等 → 游程全断，4200x1200 规则地形存档 17B→21MB，
  '存档体积可控'测试红。改为 raw 对 raw。此 bug 属 v3 稳定 id 方案引入。

## 训练假人完整移植（同日）
- 原版机制：tile 378（2x3）+ NPC 488（TETrainingDummy TileEntity 激活）。
  我们：Game.spawnAllDummies（世界就绪全图扫锚点 frameX%36==0&&frameY==0）+
  spawnDummyAt（放置钩子；dup 检查）；Enemy.dummyAI（aiStyle 92 分发：
  锚 tile 消失→dead、仅重力静止、hp 恒满=immortal）+ hurt 特例（shake=clamp(dmg,20,120)、
  记方向、不掉血不死，cs:83498）+ despawn 豁免；Renderer vanillaFrameIdx 488 分支
  （shake 驱动帧：step=dir==-1?4:6, ceil(shake/step), dir==1 +5, cs:71516）。
  白名单 npcs+=488（32x550, 11 帧@50px）。
- E2E：放置→生成、hurt(45)→shake=45/dir=-1/血恒满/不死、破坏锚 tile→消亡，全过。
  dmgNums=0 是探针直调 hurt（伤害数字由 Game 挥击路径生成，真实挥击会有）。

## 房屋内刷怪修复（同日）
- 根因：findSpawnTile 移植时注释"wallHouse 房屋墙检查我们无房屋墙数据，略"——
  L886 的 `!ignoreSafeWalls && wallHouse[tile.wall]` 弃选守卫缺失。
- 修：WALL_HOUSE 表（Main.cs wallHouse[]=true 全提取 265 项=全部可玩家放置的墙，
  自然墙 2/3/8 等不在内）→ findSpawnTile 落点拒绝 + noWorms 修正
  （原版 SetSpawnFlags L321：玩家所站格带房屋墙→不出蠕虫，之前恒 false）。
- tests/house-spawn.test.ts：木墙房 300 次零生成 vs 无墙区正常出怪。
- 遗留：SpawnAnNPC 海洋段 L1742 wallHouse（海鸥落位微调）未接（边缘场景）。

## 掉落物点光（2026-08-11）
- 原版 WorldItem.UpdateItem_VisualEffects：掉落火把(createTile==4)/蜡烛(105)发光带 !wet；
  荧光棒族 282[.7,1,.8]/286 粘性[.7,.8,1]/3002 探矿[1.05,.95,.55] **无 wet 门控（水中也亮）**；
  坠落之星 75[.8,.7,.1] / 陨石锭 183[.15,.45,.9]。全部接入 Game.render 的 addLight 循环
  （torch/candle 按 tile 判、其余按 viIdFromKey）。
- 精髓：火把类 wet 熄灭 vs 荧光棒类 wet 不灭——勿统一加 !wet。

## 黏滞 tile（2026-08-11）
- 根因：Player 移动完全无 StickyTiles 移植——蛛网(51)/蜂蜜块(229) 畅通无阻。
- 修（Collision.StickyTiles :3375 + Player.cs:22650-22740 1:1，Player.fixedUpdate
  重力后 moveAndCollide 前插入）：重叠检测（bbox±1 格；蜂蜜 pad 1px）；
  X 钳±1 后 |vx|>0.75×0.85 否则×0.6；Y（gravDir=1）钳 vy≤1/≥-5 后 上升×0.96 下落×0.3；
  fallStartY 重置（不积累摔伤）；**蛛网专属**：jumpHold=0（type!=229 才清）+ 挣扎
  stickyBreak++ 超 rand(20,100) 撕破（掉 vi_150_Cobweb via VANILLA_ITEM_KEY_BY_ID[150]）。
- 测试坑：inputJump=false 时 jumpHold 每帧自然清零——蜂蜜禁跳断言须 inputJump=true
  （期望 9=自然衰减 1），蛛网断言 0。tests/cobweb.test.ts 3 用例。
- 蛛网怪（wall creeper 等）AI 不受网减速（原版 NPC 各自 AI，暂不处理）。
- 黏滞粒子补全（同日二轮）：① 纠缠丝尘（Collision.cs:3416 dust 30：网中速度>0.7、
  1/30/tick 白色网屑）② 蜂蜜滴落（Player.cs:22747 dust 153：1/5 且垂直有速、出在
  玩家背离蜂蜜一侧）③ 撕网破坏爆散（KillTile HitEffect 近似 8 粒）。
  Player 粘滞段记录 webTx/webTy 供粒子定位。212/212 全绿。

## 方块环境粒子全量对齐（2026-08-11 二轮）
- 权威来源：TileDrawing.DrawTiles_EmitParticles L6795-7667（Explore 子代理全表提取）。
  关键行号：熔炉族 7482、吊灯 7376、灯笼 7161、路灯 7243、烛台 7286、骷髅灯 7332、
  水蜡烛 7342(1/2)、和平蜡烛 7357(1/2)、腐化族 7435-7450、祭坛 7464/暗影球 7451、
  陨石/狱石 7504-7520、蘑菇 7478、丛林植物 7521、篝火 6893、壁炉 7493、烟囱 6925、
  造雾机 565:6883、守护者熔炉 7097、药草 9780-9830、矿物闪光(通用 tileShine 分支) 7529-7646。
- 实现：src/render/TileParticles.ts 规则表（sheet→rules，帧门 pred/lightGate/偏移/上浮/横漂）+
  Game.emitTileParticles（每 3 tick 视口扫描，sheet 缓存 Int16Array）。火把保留独立 1:1 实现。
- 豁免：未注册 sheet 的规则删除（133 精金熔炉/46 银砖/47 铜砖/238 花茎球——def 未注册永不命中）。
- 高频 1/2 项概率钳 0.95（每 3 tick 最多发 1 粒）。
- Tier 3 不做：风场树叶/StarCloud 萤火虫/泡泡机 gore 层级/便便/彩虹巨石/NatureFlies/
  RubbleDust/微光闪烁/马桶。51 蛛网/229 蜂蜜原版本无环境粒子。
- 测试：tile-particles.test.ts 6 用例（sheet 注册/概率域/高频量级/帧门边界/dust 色表/药草 6 style）。
  E2E：放置熔炉点燃帧+双蜡烛+水滴石+蘑菇植物，粒子稳定 ~20-30/帧、零报错。

**世界边界钳制(2026-08-12,用户报"走出边缘直接掉落")**:原版机制=Player.BordersMovement
(Player.cs:23771-23844,碰撞积分后 :27968 调用)——世界边缘**内缩 640px(40 格=
offLimitBorderTiles×16,Main.cs:433)**硬框:左右/顶越线钳回+速度清零;顶另加 vy≥0.11
下推+gravDir 复位;**底越线=出界即死 KillMe(ByOther 21,10)——绕防御/无敌帧 hp 直归零**,
死亡结算走 fixedUpdate 尾部统一段(死因文案包暂以 default 近似)。金标 wld 验尸证实
**原版无生成期边框**(y=300 边缘是海/天空、最底行 y=1199 反而全空)——屏障纯运行时。
移植注意:①必须加最小世界门(任一边 ≤80 格豁免),否则 60×60 单测世界被框死(a-batch1
6 红教训);②cameraX/Y=0 抗抖无对应系统已略;③NPC.cs 无对应方法(原版 NPC 无边界钳制,
勿画蛇添足)。回归 tests/world-border.test.ts(6 断言含小世界门/无敌帧穿透)。
