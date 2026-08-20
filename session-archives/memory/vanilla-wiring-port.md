---
name: vanilla-wiring-port
description: 原版电路系统 Wiring.cs 全量移植完成——核心文件/触发语义陷阱/测试与验证方式
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-09T15:21:39.270Z
---

2026-08-09 完成 Wiring.cs(1.4.0.5)全量移植,游戏内电路可用。

- **核心**:`game/src/world/Wiring.ts`(TripWire 四色 pass 红→蓝→绿→黄 / HitWire BFS 含分线盒预算与像素盒 / LogicGatePass / XferWater / UpdateMech / MassWireOperation)+ `game/src/world/wiring/devices.ts`(HitWireSingle 器件全表)。Game.ts 持有 `this.wiring`,afterWorldLoad 装配 `attachDevices(makeDeviceCtx())`。
- **数据**:TileStore.wire 位(bit0-3 四色/bit4 致动器/bit5 actuated);存档 `wire` 段(缺字段容忍,version 不升);WldParser 从 header2 提取 `(h2 & 0x3E)>>1`;WldImport 透传。
- **关键语义陷阱**:**TripWire 种子格自己会被 SkipWire——触发源及其 2×2 矩形内的器件不会被自己触发**(排测试电路时器件必须放在源矩形外)。逻辑门 Queue 必须"排空"否则下次级联被 `gatesCurrent.length!==0` 早退(已修)。BFS 邻居序 下/上/右/左;分线盒进入方向决定出口。
- **工具**:wire/red|blue|green|yellow_wrench/wire_cutter/actuator_item/actuation_rod/multicolor_wrench/grand_design(ItemDef.wireTool);R 键循环多彩/蓝图模式;宏伟蓝图=两次点击(锚点→终点)执行 L 形批量(原版两段开区间+端点)。渲染:`Renderer.drawWires`(WiresNew.png 图集,色行/连接掩码/多色淡化),F7 强制显示,手持 mech 工具自动显示;致动幽灵态在 ChunkCache(globalAlpha 0.3)。
- **触发源**:拉杆/开关/计时器右键→hitSwitch;压板 135 踩踏;测重板 428 与感应器 423 由 `scanTriggerTiles` 登记+onTileChanged 增量维护,昼夜感应挂 lastWasDay 切换。旧的直线扫描占位(fireTrapsFrom)已删除。
- **机关音效距离衰减**(2026-08-09,用户报"世界任何一处机关响都能听到"):原版 SoundEngine.PlaySound(type,x,y) 语义。`Game.sfxAt(name,x,y)`:R=视野 1.5×,超距直接 return,范围内 vol=1−d/R。接入点:DeviceCtx.sfx 签名改 `(name, x?, y?)`(devices.ts 全部 7 个调用点传器件格中心);Game 侧 shootProjectile 的 tink、explodeAt 的 roar 走 sfxAt。拉杆右键 tink 玩家贴身不衰减。E2E 当时被另一会话在途损坏(StructuresPass 缺 ITEM_BY_KEY/Enemy.tint,vite 页面卡"地狱屋")阻塞,降级用单测验证器件坐标透传(31/31)——**他会在途文件修好后建议重跑 _trapfire/_trapdmg 探针**。
- **★ 陷阱弹幕全实体伤害(2026-08-09,用户报"机关不伤怪/NPC")**:TrapShot.fixedUpdate 除玩家外加三桶命中(game.enemies()/entities.critters 单参 hurt(game) shim/ entities.npcs TownNPC.hurt)。穿透规则:boulder 恒穿透;spiky/flame 穿透(受击者 8tick 无敌帧节流);dart/superdart/geyser/spear 一碰即碎。TownNPC 新增 hp/maxHp(取 vanilla-npcs.json lifeMax 250)/iframes/hurt(防御 15 减伤 dmg-7.5、8tick 无敌、死亡移除+粒子+音效,**原版次日重生未移植**)、Renderer 受击闪白。探针 `_trapdmg.mjs`(走廊摆僵尸+兔子+商人三靶,paused 后手动步进——**勿与实时循环双跑**;靶要贴陷阱口,小动物会蹦出弹道)。
- **生成端**:TemplePass 尾部移植 templePart2+mayanTrap(压板 135 style6+陷阱 137+三色随机布线);实测小世界约 600 格线/26 压板/54 陷阱。
- **★ 地牢机关补全（2026-08-09，用户报"地牢里机关电路没有"）**:DungeonPass 第 7 步原是简化飞镖陷阱(无板无线→永不触发),已重写为 **placeTrap(x,y,0) 1:1**(WorldGen.cs:3324-3420):下扫实心格→上方压板(135,有墙恒 style2=frameX36);压板行±侧扫锚墙(实心或裂砖481/482/483,距离5..49,锚脚实心、非门10/尖刺48);挖墙格嵌飞镖(137,墙左→frameX18朝右);红线 L 路径(先x后y)连板→陷阱。探针 `_dungeondtrap.mjs` 4/4(陷阱邻线全通+BFS 板→陷阱连通;注意要按 world.dungeonX±350 过滤——TemplePass 的板/陷阱会混入全局扫描)。守卫细节:IsTileNearby(70蘑菇草,20)/墙87蜥蜴unsafe/岩浆/落点上方两行3×3全空/下方非48尖刺232木尖刺。**遗留:全局 pass 76 Traps(L8932,placeTrap 全4型+PlaceSandTrap 沙陷阱)未移植**——vanilla/ 目录无 TrapsPass.ts,洞穴巨石/火焰陷阱仍缺。
- **验证**:`node_modules/.bin/vite-node scripts/wiring-test.mts`(30 用例:BFS 去重/分线盒/像素盒/逻辑门/泵/计时器/致动器/批量铺线/存读往返/**灯光照门控**);E2E 用 `?play=small` + 页内 `__swGame.wiring` 摆电路断言(注意 vite-node 会转译 evaluate 字符串里的 `import(`,E2E 脚本用 `node --input-type=module -` stdin 跑)。
- **光照门控**(review 补):接线灯器件关帧不发光——`devices.ts` 的 `LIGHT_TOGGLE` 表(sheet→[轴,delta],on = frame%(2δ)<δ)供 `LightingEngine` 查询 `lightIsOn`。
- **开局背包**(验证用):afterWorldLoad bag 含全套电路工具(四色扳手/电线300/钢丝钳/致动器30/魔杖/多彩/蓝图)+ 常用器件放置物品(拉杆/开关/计时器/压板/陷阱/雕像/逻辑门/传送器/泵),槽位 10-36 与盔甲位(45+)不冲突。
- **已知缺口**(有意简化):音乐盒/派对/天塔柱/大炮弹药为占位(依赖音乐/派对/天象/弹药系统,非电路本身)。~~敌人触发压板/陷阱箱/442 垫板/蓝图预览~~ **已全部补齐(四轮)**:①updateEntityPlates(Collision.SwitchTiles objType 2/3 语义:critters 桶触发 135、巨石 TrapShot 触发 135+442,**勿用 instanceof 判弹幕——跨模块实例失败,用 `.kind === 'boulder'` duck-typing**);②陷阱箱 441(`v_441_fakecontainers`!)/468:interactAt 分支放宽 + tryOpenChest 内 hitSwitch+八方射镖(Player.cs:21303);③宏伟蓝图拖拽预览:Game.render 注入 renderer.grandPreview,Renderer.drawGrandPreview 画 L 路径半透明格(剪线蓝/致动器绿/铺线红,与 massWireOperation 先纵后横同构)。
- **陷阱弹幕贴图**(三轮+四轮+五轮终版):tile 137 kind ↔ projectile 终版对应(**五轮经 Item.cs placeStyle 交叉核实,纠正了 1/2 对调的老错误**):**0 飞镖机关(539)→98(10×28 有图) | 1 超级飞镖机关(1146)→184(10×18 毒镖有图) | 2 烈焰机关(1147)→187(官方空桩:隐形弹体+火焰尘埃,Projectile.cs:24222 同族 dust 驱动) | 3 尖球机关(1148)→185 | 4 长矛机关(1149)→186(10×16 有图)**。神庙 mayanTrap 横置=超钻/烈焰、竖置=尖球/长矛。**关键证据链**:187/654 等空桩 xnb 是字节级相同的占位 stub(不同弹幕共享同一文件,真贴图不可能)且解压后像素全零;AssetInitializer/LoadProjectile/TextureAssets 均无重映射——**官方 Content 本来就缺这批贴图,解包是忠实的**;全素材包共 83 张空桩(多为 1×1 魔术像素与 id_0 占位,属正常)。帧规格按解包 PNG 整图;98/184/186 内容朝上需 rotOff=+π/2;isBlankTex 检出空桩走色块回退+拖尾。PNG 需同时进 vanilla-atlas.mjs MISC(落盘)与 SpriteAtlas VANILLA_MISC(运行时)。验证探针 `_trapfire.mjs`(差分采样:弹幕在场 vs 移开)。
- **验证轮修复**(2026-08-09 二轮):①工具图标走 `VANILLA_ITEM_ICON_MAP`(wire→530/扳手→509 等,id 经 Terarria1456 Item.cs case 核实);②WiresNew/Actuator 必须加进 SpriteAtlas.ts 的**运行时** VANILLA_MISC(拷贝脚本的 MISC 只管落盘,漏加运行时清单=贴图不加载);③place_v_* 图标回退用 vframeAt(压板 135 是 16×200 窄条,cols=0 会让 vframe 判越界);④**投射物渲染**:Renderer 实体循环原本只画五类,projectiles 桶(飞镖/箭)从不绘制(历史缺口),已加 `typeof e.draw === 'function'` 回退分支,且 TrapShot/Dart.draw 改世界坐标(实体循环在世界变换内,自算屏幕坐标会双重变换);⑤v_137_traps def 原 frame:'auto'(8 向邻接取帧)导致放置贴图乱变,改 framed/'style';⑥压板触发改 AABB 扫描(Collision.SwitchTiles 语义,原脚底单格判定在 1px 陷入时偏移);⑦采样验证 8×4px 移动投射物要即时取最新坐标,隔帧采样会扑空。
- 音乐盒/派对/天塔柱/大炮弹药等无对应系统的器件为帧翻转+toast 占位(devices.ts 注释标明);Enemy.ts 的 critter 报错是 NPC 会话在途文件,与电路无关。

关联 [[vanilla-door-frames]]、[[vanilla-worldgen-port-status]]、[[terraria-assets-pipeline]]。

## 陷阱(137)朝向规则（2026-08-11，用户问"飞镖机关朝向咋调整"）
- **帧编码**：frameY/18=种类（0 飞镖/1 超级/2 烈焰/3 尖刺球/4 长矛），frameX=方向（水平系 0=左 18=右；尖刺球/长 spear 系 0-3=下/上/左/右，见 devices.fireTrap）。
- **生成侧**已 1:1：TrapsPass placeTrapDart 按"陷阱在压板哪侧"写 `dir===1?18:0`（cs:3365-3420）。
- **玩家放置侧** = **放置瞬间按玩家面朝方向固定**（Player.cs:40209 PlaceThing_Tiles_PlaceIt_SpinTraps：`createTile==137 && direction==1 → frameX+=18`）——tryPlace 补此补丁（此前恒 placeStyle*stride=0 永远朝左）。**放置后不可再调向**（锤子不旋转陷阱）。
- **触发侧** fireTrap 读 frameX 定弹向 ✓（Wiring.cs:1495-1743）。

## 雕像触发 1:1 对齐（2026-08-11，用户令"检查其他雕像是否能被电路正常触发"）
原版语义全在 Wiring.cs case 105（:2129-2483）：
- **主表 STATUE_NPC**（:2176-2267）style→npc：5:73/13:24/30:6/35:2/51:[299,538]/…/79:[616,617]/**80:[671,672]、81:673、82:[674,675]（1.4.4 新增，此前漏）**；spawn 于 (锚X+16, 底行+3)×16；flag7={64,71} 生成区(ax-2..ax+3×ay..ay+2)实心→poof 不生成。
- **DIRECT 表**（:2290-2440）各自偏移：7=(px-4,py-6)、10=(px,py)、27=(px-9,py)、16/42/4/8/9/18/23/28=py-12、50(史莱姆王)=solid 检查；28 是蛇三色随机 [74,297,298]（曾写死 74）。
- **物品雕像**：2 星 184/17 炸弹 166/37 心 58，CheckMech 600 + **心/星要过全部等价 id 的 MechSpawn**（58&1734&1867 / 184&1735&1868）。
- **MechSpawn 1:1**（NPC.cs:7399 / Item.cs:48982）：等价组互计（蛇74/297/298、骷髅46/540/303/337、鸟362-365、602/603、608/609、616/617、55+230）；NPC 阈 200px≥3/600px≥6/全图≥10；Item 300/800/全图同阈。曾是无类型"25格<6"近似。
- **63 随机传送雕像**要额外 MechSpawn(165)（曾漏）。
- **雕像产怪标**：spawnNpc 打 Enemy.spawnedFromStatue → 掉落端三连门（NPCLoot :79648-79654）：value=0 不掉钱；NoEarlymodeLootWhenSpawnedFromStatue={480,82,86,170,180,171} 肉前整单不出；StatueSpawnedDropRarity 表（85=0 永不出，多数 0.05/0.2）概率门；NotFromStatue 条件为 false。
- 心/星雕像产物走 pickup（IsAPickup）——dropItem 打 pickup 标；dropItem 同步换 VANILLA_ITEM_KEY_BY_ID（曾用 wld ITEM_MAP 窄映射）。
- 验证 probe-statue.mjs：史莱姆雕像→带标怪+凝胶掉/零钱、心雕像→pickup、mimic 雕像零掉落、新雕像 80 可触发。

**尖刺球物理修复(2026-08-12,用户报"放出后无反弹只沉降")**:185=aiStyle14,全部语义:
- 尾部(1405 :21600-21608/1456 同):vy==0 贴地叠 vx*=0.95;每帧 vx*=0.98、重力 0.3、终端 15.9
- 碰撞响应(1405 :13302-13307/1456 :18289-18297):分轴,X 阻挡→vx=-lastVx*0.9;
  Y 阻挡且 lastVy>1→vy=-lastVy*0.9,否则 vy=0 落定不微弹。旧近似 -0.4/0.7 即病根
- SetDefaults:14×14、timeLeft **900**(曾写 1800)、旋转 = vx*0.14(:21630,非 0.03)
- 生成端 1456 :1944-1976(与 1405 不同!取 1456):无视朝向固定下丢,vx∈[-1,1]、vy∈[4,5],
  位 (x*16+8, y*16+22);预算 200 按"每弹自身距离"扣(50/15/10/8/6/5/4/3/2/1 档,
  旧按数量排名扣是错的)→ Game.ctx.spikyBudgetPenalty 新接口
- 回归 tests/spiky-ball.test.ts(5 断言);TrapShot spiky 分轴链与通用积分已分流
