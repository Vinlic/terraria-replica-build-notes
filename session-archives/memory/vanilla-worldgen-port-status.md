---
name: vanilla-worldgen-port-status
description: 原版世界生成 105 pass 完整移植的状态跟踪——分阶段计划与进度
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-10T08:06:39.989Z
---

用户选择:完整 1:1 移植原版 105 pass 世界生成管线 + 全量物品补齐(2026-08-07 确认)。

**Why**: 自建世界要与导入 wld 世界内容对齐,差距是结构性的(无腐化/丛林/沙漠等生物群系)。

**进度**(2026-08-08):
1. ✅ **基础设施** 完成:`src/world/gen/vanilla/`(GenState/TileRunner/Spread)
2. ✅ **地形重做** 完成:TerrainPass.cs 1:1(含 RetargetSurfaceHistory/num11 校正)、Reset 掷骰按 L4780-4894 顺序(oreTiers→crimson→dungeonSide→jungleX→dX拒绝采样→snowExtend×2→beachRoll×2→dungeonLocation)、Ocean Sand(pass 3)+Beaches(pass 33,TuneOceanDepth 双曲线)。固定 tile 常量按 w/4200 线性缩放(大世界=精确原版)。`lgcTerrain:false` 走旧 fbm 回退。同 seed 逐 tile 一致(Math.random 已清出 gen 管线)
3. ✅ **生物群系** 完成(2026-08-08):IceBiomePass(逐行随机走,雪147/冰161/墙40)/GrassPass/JunglePass(1:1,含巨型泥 runner+地表隧道+收尾,泥墙64)/泥→丛林草/MushroomPass(ShroomPatch 1:1,墙80)/DesertPass(简化蜂巢:4×2 腔室格阵,墙187/216,记录 undergroundDesert)/MarbleGranitePass(TileRunner 近似)/CorruptionPass(腐化 ChasmRunner/Sideways 1:1+球+祭坛;猩红 CrimStart 简化+心 style36+祭坛 style1)。祭坛 place3x2 帧=style*54+col*18。已知坑:原版祭坛循环在 y≤worldSurface 时直接放弃,小世界采样带浅会提前退出→已改为重试
4. 🔶 **结构与内容** 核心完成(2026-08-08):StructuresPass.ts——浮空岛(七阶段 CloudIsland:扁平云盘纵压3+顶面游走/土芯只嵌云内/云墙73/10%水池)/生命水晶/地狱屋(带灰烬基座)/地表装饰(丛林/雪原树、仙人掌、藤蔓挂悬空草根、花草)。**世界尺寸已改为原版三档:4200×1200/6400×1800/8400×2400**(固定 tile 常量按原设计工作,不再需要缩放;JunglePass 步数缩放保留 van 因子自动退化为 1)。

**2026-08-08 晚 群落大修(对照反编译源码逐群落校对)**:
- 地狱层:原版 Underworld 剖面(逐列随机走 h-190..h-160,界上~20格灰烬,界下清空,岩浆带 h-100..h-60,底部湖)——替换旧 0.86h sin 带
- 沙漠:SandMound 1:1(sqrt(1-t⁴) 四次超椭圆剖面+±10 双游走噪声+中心削平+**整柱纯沙**,硬化沙只来自蜂巢壳)
- 大理石/花岗岩:原版尺寸(穹顶洞 78-149 宽/墙178;花岗岩 200×200 体+蜿蜒岩浆洞+墙180+孤块清理),BiomeTileCheck 避冰雪/丛林/沙漠
- 猩红:CrimStart+**CrimVein**(5-8 条血管:核心0.2R挖空墙83/壳0.5R猩红石,曼哈顿行程100-150,终点=恶魔之心)+CrimEnt(水平入口只穿猩红石)+CrimPlaceHearts(壳→空腔→心)
- 浮空岛:七阶段(扁平云盘+土芯嵌云+云墙+水池)
- **最大根因:spreadGrassAll 第二阶段同轮扫描链式雪崩**(边扫边转在扫描方向无限传播,整条连通泥网全变草)→ 改轮初快照,远端丛林草 3032→0,丛林变泥主体+草壳(与参考一致);另加中心距离约束(丛林核心区 ±0.21w 内才转草,泥迹全图保持泥色——正是参考世界形态)
- 2026-08-09 凌晨第三轮(存档 (6),用户报地狱不对):
  - **地狱完整 Underworld pass 移植**(WorldGen.ts hellPass):①边界随机走+界上20格灰烬+界下清空 ②岩浆线随机走(h-120..h-60)灌岩浆 ③1/50 大灰烬丘陵(addTile 巨型竖直 runner 15-19×1000)+1/13 灰烬柱(5-29×1000)+横向灰烬团±1×0.3+挖掘隧道(-2 填岩浆,三档 5-14/10-29/15-29) ④w 个小挖掘 ⑤底部 h-145/144 岩浆层 ⑥地狱石 58 脉 area×0.0008(2-6×3-6)。验证:灰烬 20.7万/岩浆 9.4万/地狱石 1.1万/洞穴 19.5万(4200×1200)——不再是纯空洞
  - **DungeonPass.ts**(pass 30 简化):蓝 41/粉 44 砖二选一(缺绿砖 43),墙 7/9;地表塔(±9 宽,地表-14 到 y0)+y0=(worldSurface+rockLevel)/2±200+3-5 条走廊(4 高×30-70 长)带房间(8-14×5-8)+宝箱登记 world.chests。验证:1688 砖+15 箱
  - 2026-08-09 第四轮:金字塔(pass 38 简化:gs.pyramidSpots→沙岩砖金字塔 151+墙34+宝箱)、Wet Jungle(pass 43:丛林草起湿 digTunnel 灌水)、蜂巢(pass 45:丛林深层椭圆蜂巢 225 壳+蜂蜜 229 芯+空腔墙 86)、蜘蛛巢(岩层蛛网 51+墙 62 腔)。全部接线 vanillaBiomes。剩余:附魔剑圣地/丛林树冠样式/绿砖 43/MakeDungeon 完整版/地下小屋主题/棕榈树 + **阶段5 物品全量**(v_ 放置物品/placeStyle/掉落连线/图标,task #37)
5. ⬜ **物品全量补齐**: 每个 v_ tile 的放置物品 + placeStyle + 图标管线

注意:createNoise2D 构造时消费 512+ 次 RNG(simplex 置换表),预测掷骰结果时必须计入。4200 世界生成 ~1.1s。缺 tile: v_163(腐化冰)/v_400/v_401(腐化/猩红沙岩)转换暂跳过。

**2026-08-08 画质大修(用户报"方块散落/丛林爆炸")——根因 5 个,全部修复**:
1. ChunkCache 只查 type≠0 不查 flags → TileRunner 写在空气格的幽灵 type 全被渲染成浮空块。修复:主通道+neighborMask 加 flags 检查(原版 active() 语义)
2. TileRunner 加速阶梯速度抖动写成 ±0.5(原版 ±0.05)→ 巨型泥 runner 满图乱窜。修复:0.05
3. CavesPass 阶段-1 参数全部错误(强度 2-5 倍过大)→ 已按 L5174-5372 逐参数 1:1 重写(RocksInDirt 4-15/5-40 等、Small Holes 每轮双 runner、Surface Caves 五组含大竖井)
4. 自定义大理石挖洞 runner(30-55×150-350)单个 20 万格 = 全图 1.6 倍挖空 → 缩小;且石族 flag3 规则(石族只能替换石头)导致"先挖后填"无效 → 改"先嵌岩再穿心挖"
5. 补 Clean Up Dirt(pass 37):表层墙清理 + ScanTileColumnAndRemoveClumps(连通<20 块清除,floating 471→2);补 Dirt To Mud(23)/Silt(24)
验证基线:scripts/gen-audit.mjs(对比官方 wld 各生态 bbox/浮空/粗糙度)+ ascii-map.mjs(ASCII 全图目检)。参考 wld 是 v319(1.4.4),反编译源码是 1.4.0.5——剩余 ~8pp 洞穴密度差属版本差。

**How to apply**: 阶段 3 起每个 pass 按原版注册顺序(L4896 起的 AddGenerationPass 序列,可用 `grep -n 'AddGenerationPass("' WorldGen.cs` 列出)插入 vanillaCaves/vanillaBeaches 前后的正确槽位;测试脚本 `scripts/gen-vanilla-test.mjs`(直调 generateWorld)+ `scripts/gen-determinism.mjs`(确定性+三尺寸)。

原版 pass 注册顺序已核实与早期记忆清单不同:Reset(1)→TerrainPass→Dunes→Ocean Sand(3)→…→Rocks In Dirt(8)→…→Surface Caves(14)→Generate Ice Biome(15)→…→Beaches(33)→…

原版管线权威文档在会话 transcript(a510ad57315063c1b 代理输出),105 pass 完整清单+行号都在。

- **★ 浮空半砖修复（2026-08-10 深夜，用户报"空中很多半砖泥土块"+marks 标注文件）**：用 onWorldPartial 逐 pass 计数定位到 **pass#8 半砖平滑**（0→1336 浮空）。根因：HalfBrickPass 全部判空/判实只看 `st.type` 不看 `st.flags`（原版是 SolidTile/nactive=active 位语义）——TileRunner 留在天空的**幽灵 tile**（有 type 无 flags）被当实心，"补角"分支 `setTileSilent(i,j,belowType)` 把幽灵 type 实体化+砸半砖 → 2583 个浮空半砖（类型=石/粘土/矿/丛林草，全是 TileRunner 写的）。修复：solidTile/canPoundTile 加 flags 检查 + 24 处 `type[idx]===0` 判空改 `!flags[idx]` + 补角分支 belowType 走 solidTile 实取。修复后浮空 2583→1（腐化裂隙合法残留）。**通用教训：生成期任何判空/判实一律 flags 优先（type 是幽灵残留不可信），与 finalize 的幽灵净化配套**。地表半砖多是 by-design（slope 渲染未实现，PoundTile 代替 SlopeTile 的文档化近似）。用户标注法（marks JSON+标注工具导出坐标）对定位极有效。

- **★ VUI 看门狗内存泄漏（2026-08-10，用户报挂机后内存 10.6GB+DevTools trace）**：trace 分析法——TimerFire 6300 次/秒（rAF 仅 24fps）、TimerInstall 溯源到 `startLoop` 内的 `setInterval(singleShot:false, 1000)`。根因：`VUI.startLoop` 每次重启都**再注册一个看门狗定时器**（注释写幂等实际不幂等）；rAF 停摆（切后台/被 >1s 大任务卡住）时每个已积累看门狗每秒触发重启各 +1 → **指数累积**（2^t）；另有僵尸 rAF 风险（loopRaf 字段只记最后一个句柄，旧闭包自我续期杀不死）。修复：看门狗仅注册一次（`watchdogId` 门闩）+ **循环代际令牌**（`loopGen`，旧循环闭包发现代际不一致即 return 自杀）。验证：模拟 10 秒停摆定时器恒为 1（修复前指数增长）。**DevTools trace 泄漏分析套路：TimerInstall/TimerFire 计数+stackTrace 溯源 > 猜代码**。

- **C2 进行中（2026-08-10 深夜2）**：Slush pass 33 完成（cs:6591-6624：雪原带石→冰、泥/沙泥→雪泥224，泥转前查±3无丛林/蘑菇草族60/70/71/72；无 RNG）。**接线顺序坑：必须在 DirtToMud/Silt(25/26) 之后**——插在 Ice(16) 后时泥还没生成，转出 0 雪泥；挪后 4406 泥全部转雪泥 ✓。tiles.ts 曾被并行会话写坏（`''s Workshop'` 撇号断行），修。**蜘蛛巢调查（用户报"没生成"）**：实测用户种子下墙62=90185格+蛛网62364格、渲染链全通（图 468×180 加载+hasTexture✓）——**已生成，在 y≥(地表+岩层)/2 深处+洞内无光+小地图墙色#201C16≈黑（原版即是"黑色斑块"）**。验证坐标：种子1677588226 世界 (4536,663)。**偏差待修：巢密度超标**（32目标×洪泛上限3500沿连通洞穴网络蔓延=整洞变蛛网墙，原版是100-500格小口袋；应降洪泛上限~500）。
- **VUI 看门狗泄漏修复**（同晚，用户 trace 实证）：TimerFire 6300/秒。startLoop 每次重启+1 setInterval（不幂等）→ rAF 停摆时指数累积；另有僵尸 rAF。修复=看门狗仅注册一次+loopGen 代际令牌自杀。**DevTools trace 泄漏分析套路：TimerInstall/TimerFire 计数+stackTrace 溯源**。

相关:[[sandboxworld-project-setup]] [[reference-vanilla-source-of-truth]]

**★ 形态 1:1 对齐进行中（2026-08-10 启动，计划 ~/.claude/plans/agile-wandering-lighthouse.md）**：三路审计完成（105 pass 覆盖度/数值差异/地形算法），用户拍板**形态 1:1 不做同种子复现**（RNG mulberry32≠.NET Random）。
- **批 A 完成**：csCompat.ts（ctrunc/cdiv/cround ToEven/fround）+单测；TileRunner 补泥专用 vy 块（1456 L77484：±0.5 钳+rockLayer+100/maxTilesY-300 定向）；JunglePass 巨型泥 runner 补 noYChange:true（曾致泥柱矮 1/20）；沙漠蜂巢深度系数 (next+1)→(next*0.5+1.5)；IceBiome Int32Array 整除；LiquidSim 7 处均分 round→floor；计数类 5 处 round→floor；TerrainPass fround 步进。
- **B1 完成**：ShiniesPass.ts（pass 27 六矿三带密度+邪恶矿 22/204+pass 36 六宝石拒绝采样+浮沙拱形化），替换自研 orePass/growOreBlob；探针验证：替代矿互斥/宝石比例/邪恶矿 minY≈rockLevel/深度递增全 ✓。**确定性改用 vite-node 直跑**（浏览器版会被并行会话 HMR 重载打爆）。
- **B2 完成**：MountCavesPass.ts——pass 7 Mountinater(L48367 上漂泥土 blob=山丘)+pass 34 CaveOpenater(L48789 山侧开口)/Cavinator(L48733 递归蜿蜒)；gs.mCaveX/Y/numMCaves 新字段；探针 4/4 丘隆起 27-142 格、间距≥100 ✓。
- **B3 完成**：TreePass.ts——pass 82 全套：RandomizeTreeStyle(L2817 按世界宽三档,finalize 写回 world.treeX/Style)、GrowEpicTree(L11850 高 20-30)、AddTrees(L15642 逐列+Next(3)/Next(4) 跳列+沙滩棕榈 0.1+0.35n)、GrowTree(L14171 **全帧表**:干身 10 case×3 变体/侧枝/根部/基座/树冠标记帧——帧表从源码程序化提取勿手抄)、GrowPalmTree(L11785 sheet 323 倾斜干)。树登记经 gs.genTrees→finalize→world.trees(砍伐判定)。旧 surfacePass/StructuresPass 树段已删。**关键修复：铺草改原版语义**(每列首个实心格为泥土→草,替换 stale surface[] 列顶转换)——山坡/洞口露土修复后树 107→316 棵。**vite-node 变换缓存坑：改完源码后首次跑探针可能拿到旧结果,加 console.log 插桩或换种子破缓存**。
- **B4 完成**：浮空岛 pass 21 补全——总量 = w*0.0008 岛 + skyLakes(1+w>8000+w>6000)；CloudLake 天湖变体(L47704 纯云盘无芯无墙)；雨云凸包 rainBumps(L47484-47522 岛底 1/4 雨云 196)；间距/中心避让改固定 150/180(去掉 van 缩放)。探针 4200 世界=3 岛+1 湖 ✓。
- **B5 完成**：LakesPass.ts——pass 31 拒绝采样(避海滩 340/中心±5%/前湖±150/山丘±100/沙顶/猩红石/宝箱/±60 顶部净空/121×121 实心率 80%/非地下沙漠)+SonOfLakinater(L48516 向下蜿蜒湖腔:lerp 椭圆挖空+灌水+首步漏斗入口+腔壁泥土壳)；替换自研 liquidPass(已删)。沉降改 pass 49/97 语义(Game.settleLiquids 外层 10 轮每轮至 numLiquid=0+waterCheck,收敛早退)。探针 4 湖(Next(3,6) 范围)各 167-553 水体 ✓。
- **B6 完成**：出生点改原版 pass 78(L9471-9508 中心±5 随机扩张采样,地表下/有水则重掷,自然地表不整平)——旧"最平坦窗口+人工平台"已删。探针:偏离中心 2 格/地表上/无水 ✓。
- **C1 完成（Traps pass 76）**：TrapsPass.ts——placeTrap 全四型 1:1（cs:3324-3610）：0 飞镖(DungeonPass 同构侧扫锚墙)/1 火焰(向上找底座掏 2 宽竖井+大理石顶+137 kind2 frameY36 四段竖排+**plate style7=frameX126**)/2 炸药桶(**tile 141=Explosives 不是巨石!** 下钻4-6+5×5实心)/3 热喷泉(v_443_geyser 2×1)；type 随机 1/20→2、lavaLine+30 以下 5/6→3；w*0.05 次 placeTrap(wall==0+oceanDepths 回避)+w*0.003 次 PlaceSandTrap(cs:19962 蜂窝墙 216/187 塌沙穴,壳 396/397 中空 53)。**tile key 大坑：v_141_boulders/v_443_geysers/v_396_sandstone_block 都不存在——正确 key 是 v_141_explosives/v_443_geyser(单数)/sandstone/hardened_sand**；TILE_BY_KEY[不存在的key]! 在运行时是 undefined,写进 Uint16Array 静默变 0+flags=1=幻影活性块。探针:飞镖97+火焰21+神庙系(spear16/downFlame18/superdart255)+炸药6+喷泉34+板179/带线365。**插桩清理坑:python replace 删 console 插桩时把相邻业务行(type3 选择)一起删了致喷泉归零——清理后必须 diff 核对**。
- **B 批(A+B1-B6)全部完成**。剩 C1 余项(Pots 样式表/Statues/Hellforge/templePart2——mayanTrap 已在 wiring 移植)+C2 约 40 缺失 pass(优先级:C1 Traps76/templePart2 陷阱>C2 冰雪水域>C3 洞穴生态>C4 植被原版化(含 Spreading Grass 中段石头→草 L8697-8730)>C5 结构箱子>C6 收尾)。洞穴 12-14 digTunnel 化需对照 1456 定夺。并行会话在途错误(tsc 过滤 Game/Enemy/mainFlow/SpriteAtlas/i18n)。**liquidPass/surfacePass 旧树段/orePass 均已删,若回退需从备份找**。
- **★ Review 三代理审计修复轮（2026-08-10 晚）**：①placeTrap type1 按 **1456 权威重写为巨石陷阱**(竖井+石头壳[注意 T.STONE 是内部 id 非 sheet]+巨石 138+2×3 致动石栅 wire|WIRE_ACTUATOR+板 style7+L线；1405 反编译"130/138 火焰陷阱"是数字错乱,1456 无火焰分支,火焰只在神庙)；②**压板 style 帧轴全链路修正**(真实 wld 实测:135 的 style 在 frameY!fx恒0——TrapsPass/DungeonPass/TemplePass 六处从 (style*18,0) 改 (0,style*18))；③NOT_CLEARABLE+=135/136/137/141/443/41/43/44(修矿石覆盖地牢陷阱断线)；④出生点改选首个**实心**格(树干 solid:false 致浮空15格)；⑤热喷泉自动喷发(Game.scanTriggerTiles 登记443+上方岩浆+120tick冷却→hitSwitch)；⑥树冠 fx=0 渲染修正(VanillaTiler/ChunkCache 冠判定 fy>=198 去 fx>=22)；⑦补 def：v_163紫冰/v_200红冰/v_482绿裂砖/v_116珍珠沙/v_76狱石砖/v_55牌子(+whitelist+atlas 重跑)；CorruptionPass v_161_snow_brick→ice。⑧Traps 留 slot15(移 slot14 致拒绝采样空转 97→8)。⑨误删浮空岛函数已从 .js 阴影恢复+B4 重放(教训:清理正则 [\s\S]*? 会跨函数吞代码)。
- **★★ id 顺序炸弹两连爆（用户报"地牢变 Disco Ball"）**：**def() 调用顺序=内部 tile id=存档编码**。a)中部插入 4 def→其后全部+4→旧存档地牢砖(41/43/44 在插入点后)指向错 tile；b)挪到段末后又落在 TILE_BY_KEY 构建语句之后→注册不上(id=undefined)。**铁律：tiles.ts 新 def 一律插在"TILE_DEFS.forEach"构建行之前**。WALL 显式 id 顺序无关✓；ITEM_BY_KEY 在注册函数内构建✓但存档 item id 同为顺序依赖(根治=存档存 sheet id)。**.js 阴影 141 个仍在 src**(vitest 已实锤加载旧码——randomWorldName 报错即此),删除命令被分类器拦截,需用户手动:`node -e "const fs=require('fs'),path=require('path');(function w(d){...删 .js 且同目录有 .ts...})('src')"`。遗留:塌沙穴纯装饰(无落沙物理)、巨石 138 无 tile 重力(致动数据 1:1)、炸药 R=3、CleanupPass 1.9s 性能热点。

- **★ 蜘蛛巢/蛛网/蜂巢内饰 1:1（2026-08-10，用户对照 Starter_World Master.wld 报"布局和内饰完全不一致"）**：HiveSpiderPass.ts 三 pass 重写：
  ① **SpiderCaves(63, cs:17455)**：采样 x∈[200,w-200) y∈[(ws+rock)/2,h-230)；**countTiles 门 500≤空腔<3500**（递归洪泛计数非实心格，触界/遇墙→判满拒绝，w/2 次重试超限弃巢）——这是巢保持"口袋尺寸"的关键，旧 DFS 无门沿洞穴网络蔓延致 90k 墙62。**Spread.Spider(cs:3653) 波前 BFS**：每格双随机深度带（lavaLine-Next(5) / ws+Next(5)）；实心或非0/1/2墙→实心背面刷62止步；空格刷62+清液体+内饰：地面1/3→1/15蛛网宝箱(style15, loot vi_939_web_slinger)否则蛛网罐28 style19-20(随机3变体在fx)；天花板1/3→垂网165(fx=108+var*18)；否则覆饰187 style9-13(**3×2 底行=air格、顶行 y-1**, fx=style*54)+1/3 小堆185×2。
  ② **WebsInSpiderCaves(64, cs:20140)**：墙86蜂巢腔→液体转蜂蜜+1/3钟乳石165；墙62→清液体+空格9/10蛛网51(±2-4有实心才放)。
  ③ **Webs(58, cs:13659)**：w*h*0.0006 次天花板蛛网 TileRunner(51, addTile, ±1/-1 速, 4-10半径2-3步)；前 numMCaves 次锚山洞口。接线序：Hives(45)<Webs(58)<SpiderCaves(63)<WebsInSpiderCaves(64)。
  **★ 关键时序发现：原版 TerrainPass 不写任何墙！** 洞穴自然墙来自 CaveWalls(67, cs:17819, countTiles maxTileCount=1500 门, 只填墙0口袋遇62即拒)——所以 pass 63 时洞穴是 wall-0，countTiles 才能工作。我方 TerrainPass 预填全墙1/2→蜘蛛 pass 内 treatAsNoWall(0/1/2) 视作无墙兼容。**系统性偏差备忘：未来移植 CaveWalls/DirtRockWall 等墙 pass 或其他 countTiles 使用者时必须考虑此预填差异**。
  **帧映射实证**（sips 量素材）：Tiles_28 罐 108×1332=3变体36px横排+style在Y(36px)；Tiles_187 1890×72=单行35个3×2(style*54)；Tiles_185 1908×54(style*18, size在Y)；Tiles_165 垂网 108+var*18。
  **TrapsPass 确定性炸弹修复**：模块级 `bouldersPlaced` 跨生成累积→同种子双生成发散（vite-node 全量哈希逐 pass 二分定位到 #14 地表装饰）。pass 开头 `length=0` 重置。教训：**pass 文件里一切模块级可变状态都是同种子双生成炸弹**（_oreSet 类内容派生缓存无害）。
  验证：墙62 21k(旧90k, ~1000/巢符合500-3500门)+罐265+垂网/钟乳1194(蜂巢腔355)+覆饰187 1634+小堆338+蛛网宝箱3；确定性 PASS；vitest 166/166。**遗留：蜂巢 HiveBiome.cs 深度对照(用户点名,疑 count/入口算法有偏差)未做——round5 记"1:1"但采样/链段结构需复核**。
- **守卫老人锚点修复（2026-08-10，用户报"老人锁在塔楼里，应在门口走廊游走"）**：根因=world.dungeonX 回写的是 gs.dungeonLocation（塔锚/塔心），老人门扫描落塔内。**原版 dungeonX/Y 语义（cs L72510-72527）= 入口结构上首个可站立点（3宽×3高净空的地牢砖上方）**，不是塔心。修复：DungeonPass dungeonEnt 记录开放门厅站立点（0.5 框中心列向下找地板）→ gs.dungeonEntX/Y → WorldGen 回写 world.dungeonX/Y；Game.ts 老人首选该点（standSpot 运行时重扫 ±10 兜底门洞 1 行漂移）+ TownNPC 新增 leashHome（白天游走但离 home >10 格折返），去掉 stationary 站桩。导入 wld 的 dungeonX/Y 本就是原版站立点语义 ✓ 无需改。

- **★ 攻击/工具作用范围原版对齐（2026-08-13，用户令"武器攻击范围+工具工作范围对齐原版"）**：
  - **挖掘/放置/交互门**：原版 IsInTileInteractionRange（Player.cs:31548）+ GetTileRegion（TileReachCheckSettings.cs:53）= 玩家盒外扩 **tileRangeX=5 / tileRangeY=3**（Simple 档 ×1/上限20/+tileBoost）的**矩形**（锚 player.position 顶/底各扩）。Game.ts 加 `inTileRange(tx,ty,tb)`，替换 5 处圆形门：挖掘 4.5→矩形、放置/墙/交互 5.5→矩形(+装备 tileRange 当 tb)、电路工具 8.5→矩形 tb=20（原版多彩扳手/蓝图 tileBoost=20）。**对角被 Y 带钳制**（x+5,y+5=false）是原版矩形语义。
  - **近战 hitbox**：原版 ItemCheck_GetMeleeHitbox（Player.cs:44480）= ApplyUseStyle 三段 itemLocation（手部位置,公式同 drawUseItem）+ **物品贴图帧宽高**（vanilla heldItemFrame≈atlasIcon 尺寸）的矩形；三段缩放 早×1.4宽×1.1高下移半高/中原样/晚×2宽×1.4高上移；朝向 -1 时 X-=W。updateSwingHits 从圆形 reach（2.2-2.6格×手造数值）改为此矩形-AABB 相交；CutTiles 砍草/瓦罐同矩形；击退方向改用 e.cx-p.cx。工具表 `reach` 字段就此废弃（保留不删）。
  - 探针：inTileRange x+5✓ x+6✗ y-3带✓ 对角✗。tsc 零错、362 中仅 caves-checkpoint 2 挂=并行会话在途 Dunes pass（其自建 oracle 对账,与本次无关）。

- **★ 恶魔祭坛破坏语义 1:1（2026-08-13，用户问"祭坛不能被镐直接破坏吧"）**：
  原版三规则（Player.cs:45058 + WorldGen.cs:48949/49455）：①镐完全不可破坏（tileFrameImportant 系，pick 无效）；②锤砸需 **hammer≥80 + hardMode**——不满足则进度清零 + **玩家受 statLife/2 电击**（Hurt ByOther(4)）；③满足 → KillTile case 26 → SmashAltar：altarCount%3 选矿档（0 钴/钯、1 秘银/山铜、2 精金/钛），波次=altarCount/3+1；矿脉数 = w/4200×310−85×档，×0.85，÷波次；深度带 ws/rock/(rock×2+h)/3 随档加深；每脉 OreRunner 5..(9+w/4200)；收尾生成 1-2 只幽灵(82)；altarCount++。
  我方三处修复：def `pick: 0→-1`（镐拦）；tryMine 加祭坛分支（hammer≥80+hardMode→smashAltar / hammer 不足→电击 statLife/2 / pick 自然无效）；Game.smashAltar 移植（tileRunner addTile 撒矿+幽灵+祭坛 3×2 整体清除，gs 用 lastGenState()——传 null 会 NPE gs.worldSurface）。探针：铜镐 10 击后祭坛 6/6 完好✓、木锤电击 100→50✓、smashAltar 后 0/6+钴/钯矿 9376 格+幽灵 1✓。**遗留：圣锤 80 锤力道具未入表（砸祭坛入口暂只能靠 flags.hardMode+大锤 def）**。回归 362+2（caves-checkpoint 并行在途）。

- **★★ 条件破坏全量对齐 + 工具力道具补齐（2026-08-13 晚2，用户令"遗留物品全补+查更多条件破坏"）**：
  - **原版挖掘条件表**（Player.cs:52990-53065 else-if 链）：黑檀石25/猩红石203/珍珠石117=pick65；陨石37=50；魔矿22/猩红矿204=55(仅地下,y>ws)；黑曜石56=55(旧40错)；地狱石58=65(旧70错)；地狱熔炉77=65(仅地狱层)；神庙砖226/神庙祭坛237=**210**(Picksaw 级)；**地牢砖 tileDungeon 且 y>ws 且 x<35%/x>65% 侧=pick100**（简化无条件100）；钴/钯=100、秘银/山铜=110、精金/钛=150（旧全65错）；猩红矿旧65→55。雪泥/沙/灰烬等 num+=pickPower 加速、165网/绳系秒断(num=100)——已由 def pick0 兼容。
  - **工具力道具 31 件全补**（Item.cs SetDefaults 逐 case 提取）：镐梯度 铜35→梦魇65→死神70→熔岩100→钴110→钯130→秘银150→山铜165→精金180→钛190→Pickaxe Axe/Drax/幽灵镐200；锤梯度 木25→铜35→铁40→银45→金55→铂59→流星锤斧60→熔岩锤斧70→**圣锤80/血肉斧80**→Hammush85→叶绿战锤/千斤顶/幽灵锤斧90→The Axe/Stardust 100。items.ts 新增 vi_ 条目+**VANILLA_TOOL_POWERS overlay**（VANILLA_ITEM_KEY_BY_ID 反查→def.tool 注入;Hamaxe 双工具主类型 pick/hammer+def.axePower 副斧力,ItemDef 加 axePower? 字段）。自研木/铜/铁/银/金锤镐力与原版一致无需改。
  - E2E 探针：铜镐(35)敲黑檀石完好✓、木锤敲祭坛电击 100→50✓、困难+圣锤 tool={hammer,80}→祭坛 0/6 砸碎✓。**圣锤通过道具搜索器('Pwnhammer'/'vi_367')即可入手**。回归 367/367 全绿。

- **★ 附魔剑圣地功能全量接入（2026-08-11，用户问"石中剑是否已按原版接入"）**：
  - **生成端已有但偏差**：SwordShrinePass 原"每世界恒 1 座+恒有入口"→ 对齐原版 pass 101（cs:21858+EnchantedSwordBiome.cs）：**attempts 1-2（ScaleWith WorldWidth）× 每次 50% 放置概率 → 世界 0-2 座**；**入口 ChanceOfEntrance=1/3**（Configuration.json：ChanceOfRealSword=1/3 已对）+ 竖井壁沙→硬化沙 397（Expand(1)+OnlyTiles(53)）。分布探针 12 种子=11 座、真剑 4/11≈1/3 ✓。
  - **破坏端原本完全缺失（本次核心）**：KillTile（WorldGen.cs:49676/49838-49848）——187 style17（锚点帧 918-970）→ **1/30 泰拉魔刃(4144) 否则附魔剑(989)**；**706 TerragrimShrineEcho 恒掉 4144**；186 style15 假剑无掉落（def.drop:null 兜底）。Game.breakTile 新分支 + breakShrineSword（锚点帧须清格前捕获）。物品 vi_989_EnchantedSword/vi_4144_Terragrim 由 vanillaItemMeta 自动注册，无需加 items.ts。
  - 186/187 已在 TILE_NO_FAIL（tileNoFail 瞬破 ✓）、不在 TILE_CUT（挥砍不误删 ✓）。导入 wld copyFrame 保帧 → 破坏判定同样生效。回归 374/374。

- **★ 武器交互审计 + melee+shoot 语义修复（2026-08-11 晚，用户问"武器特效是否已按原版移植"）**：
  - **已覆盖**（数值全量取 vanilla-itemcombat.json 2612 条）：剑挥(178,useAnimation/useTime 分立+autoReuse+词缀)、回旋镖 18(ai3)、长矛 27(ai19/161)、悠悠球 21+连枷 8(ai99/15 channel)、爆炸物 12(ai16 引信+半径表)、魔法 72(mana)、直射兜底 158、弓 32+枪 49+弹药 76(PickAmmo)、投掷消耗型(ai2)。投射物贴图走原版 projSprite。
  - **本次修复**：melee+shoot 46 件(附魔剑989/波刃190/Zenith 3065)此前落入 shot 兜底=纯"光束枪"不挥砍。原版 Player.cs:42880(flag4=itemAnimation>0&&ItemTimeIsZero→ItemCheck_Shoot)=挥砍为主+useTime 节奏射弹。combatWeapon melee 分支加 shoot/shootSpeed 可选字段；Game 挥击启动块同步发射 Arrow(伤害与挥击同源)。分布 melee 140→178。
  - **遗留缺口（直射 Arrow 近似）**：魔法特效族(追踪 ai10 Magic Missile channel/弹跳 Water Bolt/蜂枪/落星 Starfury ai5/Zenith ai5 剑雨)、召唤 minion(全未实现)、鞭 ai165、特殊弹光效/拖尾。2612 条里 null 2118=材料/家具/弹药等非武器。

- **★ 神庙门悬空 2 格修复（2026-08-11 晚，用户标注 marks-违法的要塞 报"门位置应下移两格"）**：
  根因链：原版 makeTemple 尾（1456 cs:34176）`PlaceTile(sx, num81, 10, style 11)`，num81=地板F-4（while 找首个 active 后 -4）；PlaceTile case 10（:59867）条件 B（j+1/j+2 空+j+3 实心）→ **PlaceDoor(i, j+1)**（:31938 门占 j-1..j+1）→ 门顶=F-4=jy、门底=F-2、站地板 F-1。我方注释"PlaceTile 放门要 j-2"只对条件 A（天花板挂）成立，神庙走的是条件 B——`placeDoorClosed(st, i1, jy-2)` 高了 2 格。修为 jy。探针：门 3 格完整/门底下方实心/顶上 2 格实心过梁 ✓。**注意：placeDoorClosed(x,y) 锚=门顶行（Door.ts:20）；IslandHouse floorY-2 / HellFort rowB-3 等其他调用点锚点语义未逐一复核，同类悬空疑点待查**。

- **★ 生成侧门锚点全量复核（2026-08-11 晚2，神庙门修复后用户令复核其余调用点）**：
  PlaceTile case10 双条件（:59867）：A（j-1/j-2 空+j-3 实心=天花板挂）→PlaceDoor(j-1)门顶=j-2；B（j+1/j+2 空+j+3 实心=落地）→PlaceDoor(j+1)门顶=j。PlaceDoor（:31938）门占 j-1..j+1 且强制 mount(j-2 实心)+地板(j+2 实心)。**结论：四处调用点三对一错**：
  ① IslandHouse floorY-2 ✓（原版 PlaceTile(Y) 走条件 A→门顶 Y-2，cs:79964）
  ② HellFort rowB-3 ✓（原版 PlaceTile(rowB-1) 走条件 A→门顶 rowB-3，cs:33106；style=19 对）
  ③ CaveHouse exitR/exitL ✓（原版 PlaceTile(exitY,forced) 走条件 B→门顶 exitY，HouseBuilder.cs:547）
  ④ 神庙 jy-2 ✗→已修 jy（走条件 B）。
  **新增修复**：CaveHouse placeDoors 补 PlaceDoor 门禁（mount exitY-1 实心+地板 exitY+3 实心缺一不放门只留洞——forced=true 只绕过首道空格门，锚点条件仍生效）。
  全图实证探针（两种子扫全部 door_closed 顶行）：**noFloor=0 全部站地板**；noMount 各 1 例=放门时过梁实心、后续家具放置清掉（原版流程同序，非 bug）。

- **★ 开宝箱物品图标回退修复（2026-08-11 晚3，用户报"开宝箱时内部物品贴图回退"）**：
  双根因：① `SpriteAtlas.vframeAt` 不懒加载（直接 vimages.get，与 vframe/vrect 的 ensureVImage 不一致）——`place_v_*` 家具类物品图标走 atlasIconForKey→vframeAt 取图块表首帧，表未载时**连加载请求都不发**=永久回退；② Game.onVImageLoaded 只认 `Item_Atlas` 才置 iconUiDirty，Tiles_ 表晚到只 invalidateAll 不刷 UI。修复：vframeAt 改 ensureVImage；Tiles_ 晚到也置 iconUiDirty；iconUiDirty 刷 UI 从 `%30` tick 网格改冷却 30t（晚到后 ≤1t 自愈，原来最长 0.5s）。自愈链：paintSlot→iconUrl→(触发加载)→兜底不缓存→表到位→onVImageLoaded→iconUiDirty→flushInvNotify→cb.onInventoryChanged→ui.refreshAll（含宝箱槽）。

- **★★ 世界运行时演化系统全量接入（2026-08-12 凌晨，用户令"全量接入"，P0+P1+P2 一并完成）**：
  新文件 `src/world/evolution/WorldEvolution.ts`（~900 行，1456 1:1）+ Game.fixedUpdate 每 tick 调 `evolution.update()`（性能 55μs/tick）：
  - **采样骨架**（UpdateWorld cs:71507）：地表 = w×h×3e-5（雨 ×1.5）、地下 = w×h×1.5e-5 随机样本/tick；每地表样本 1/(num7×100) PlantAlch。4200 世界 = 151+76 样本/tick。
  - **P0**：GrassGrowth 全分支（普通草仅 worldSurface 上、丛林/蘑菇/灰烬草转泥灰、邪恶草互吞+转泥对 661/662）、七族藤蔓（普通 52/382、丛林 62、蘑菇 528、神圣 115、腐化 636、猩红 205、灰烬 638；**GrowMoreVines 密度门 9×17 cap60/12**）、仙人掌 GrowCactus 全段（水量门 50×25/25、分支直立）、药草 PlantAlch（深度分布+15×15 密度门<5+按地面选种）+ GrowAlch 三态（淹死规则：岩浆除火冠花、水除月光/水叶）。
  - **P1**：hardUpdateWorld——邪恶/神圣蔓延（±3 随机点 1/2 链式、向日葵 2 格挡、叶绿防御、**神圣不吞丛林 60/69**）、水晶碎块 129（CanGrowShards 族+岩层下 1/5+±6<2）、叶绿 211 生长（深处 60 草 1/300、CanChlorophyteGrow 35/85 格 40/130 上限）、邪恶矿退化 Convert 9、世花球茎 238（mechAll 1/60+150 格密度）+生命果 236（mechAny 1/30+60 格）。
  - **P2**：苔藓蔓延 MossConversion 全表+藓堆 184、钟乳石 165 再生（PlaceTight）、蛛网 51 再生（GrowWeb）、贝壳 324/珊瑚 81 沉积、染料植物 227（普通 1/3000+奇异 1/15000）、蚁狮幼虫 485/751、蜂巢 444 地下再生、墙蔓延（SpreadGrassWalls/DesertWalls→Convert 墙半区）、草→花 3→73/110→113。
  - **破坏端配套**：breakTile 新增 238/236 分支——球茎=2×2 清除+50 格内有玩家 summonBoss('plantera')；236=掉 vi_1291 生命果（KillTile cs:48013-48036）。
  - **关键结构坑**：UndergroundTile 是 else-if 链——60 走 SpreadUnderground 分支被消费，**丛林藤延长/蜂巢再生由 62 号藤 tile 驱动**（原版 num15=j for 62）；蜂巢 2×2 主体区 tileCut 藤草可 KillTile 覆写（非 tileCut 阻断）；球茎 2×2 向上悬（placeBlock(i, minJ-1)）。
  - 近似项（注释标注）：CanHitLine LOS 加权→纯计数、PlayerLOS→玩家 50 格距离、变体帧直接随机、净化 case 5/6/7/10 未移植、海藻/香蒲/睡莲/海燕麦/绿洲/竹子/南瓜（万圣节限定）未接。
  - 验证：3600 tick 行为探针（藤+95/丛林藤+24/药草芽+5/叶绿+3/花+12/61 草+37）+ 9 场景分支探针（草蔓延/藤/蜂巢/球茎/水晶/药草开花/蛛网/钟乳石/邪恶链全 PASS）+ 回归（演化零影响；挂项均并行会话 JunglePass 在途）。

- **★ 荧光棒族全量移植（2026-08-12，用户令"手持发光+投掷+粘性等同族全量"）**：
  - **手持发光**（ItemCheck_EmitHeldItemLight，Player.cs:49288-49430）：六件各自显式 RGB——282=(0.7,1,0.8)/286=(0.7,0.8,1)/3112=(1,0.6,0.85)/3002=(1.05,0.95,0.55)/4776=(0.9,0.35,1,附4.5格泛光省略)/5643=Disco 轮转；**仅 !pulley 门无湿门——水下也亮**（与火把 (Torches&&!wet) 不同）。Game 手持光块在火把 wet 门之前先判荧光棒表。
  - **投掷**：combatWeapon 新 kind 'glowstick'——门禁 = ItemID.Sets.Glowsticks 精确六件（ItemID.cs:1198，**不能按 aiStyle 14 一律归入**：ai14 还有巨石/药瓶等）；→ proj 50/53/515/473/870/1089，消耗 1 支、shootSpeed 6、useTime 15。
  - **GlowstickProj**（WeaponProj.ts）：AI_014 主体（cs:23482-23500：ai0>5 钳位/着地滚动摩擦 ×0.97/重力 +0.2/rotation+=vx×0.1）；53 粘性=tileCollide false+固体重叠 v=(0,-0.2) 抵重力冻结（cs:23245）；870 妖精=首撞全反射→AI_170（cs:42997：半径10实心排斥场+×0.95 衰减<1 归零）；反弹表（cs:18261-18333）：50=X-0.2/Y(lastV>1.5)-0.2、≥1089 彩虹=X-0.99±1保底、其余 473/515=-0.5/-0.5。寿命 timeLeft×5=9000（473 ×2=3600）到期消失无掉落。光照走既有弹幕点光通道（projectileData.light=1）。
  - 物理探针 6/6：滚动摩擦 vx3→1.32、粘性冻结、弹力 -4.3、彩虹保底速度 1.00、妖精衰减归零、寿命精确 9000/3600。贴图 Projectile_50/53/473/515/870/1089 已在白名单。回归仅剩并行会话在途挂项（Enemy 萤火虫/caves oracle）。


## 矿骨堆斜坡门修复（2026-08-12，用户标注"装饰物出现在有斜坡格的沙漠方块上"）
原版地面门 = **SolidTileAllowBottomSlope**（WorldGen.cs:70211：实心且 `!topSlope() && !halfBrick()`；topSlope=**slope 1/2**，底坡 3/4 允许），矿骨堆 185/186 放置经 PlaceTile case 186（:49284）强制此门。
- 我们的 `pilesPass`（WorldGen.ts:521）只查 solid——斜坡沙上生成装饰。修复：**骨堆跨 3 列（185 单列），3 列地面全部须 solid+非半砖+非顶坡**（只查锚点列会残留 17/1031——跨列斜坡）。MicroBiomesPass.placeLargePile（营地倒木 186）同门 3 列。
- 验证脚本 `/tmp/pile-test.mts`（vite-node 生成 4200×1200 全图扫）：修复后 deco 1011 处/斜坡上 0 处。
- pass 顺序：半砖平滑(82) 在矿骨堆(97) 之前——生成时 slope 数据已就位，门可靠。
- CaveHousePass:450 的 v_186 是人工构造屋内陈设，平地有保证，不加门。
- **★★ else-if 链饿死双 bug + 静持行冻结走路（2026-08-12，用户报"生命水晶无效/荧光棒扔不出/持物走路无动画"）**：
  ① **useItem 链饿死**（并行会话的通用消耗品分支外层仅 mouseDown&&useTime===0，内层语义门失败后 else-if 槽位仍被占用→链条后续全成死代码）：受害=生命水晶29/魔力水晶109/生命果1291/弓枪族/荧光棒投掷/cw 武器分发。修复三连：三专用分支上移到通用分支前+补 mouseDown/useTime 门；通用分支外层加 `consumableFuncGate()` 语义门（heal/buff 才认领）；item 29/109/1291/弓 gate=false、药水 gate=true 探针全对。
  ② **静持行冻结走路动画**（Renderer.drawPlayer 纸娃娃）：静持 bodyFrame 行（Player.cs:36007-36040）排在行走循环前→持 holdStyle 物（火把/荧光棒/伞/蜡烛 40 件）走路变静态帧。**原版身体/腿是分图层：静持只钉身体行（手臂持物）、腿照常走 legFrame 循环（cs:36178）**——本项目纸娃娃单层合成帧，钉行连腿一起冻。单层近似：行走循环（row 6-19）优先于静持行，静持行仅在站立时生效；legacy Maples 路径无静持行不受影响。
  **教训：往 useItem 这类长 else-if 链插分支，外层条件必须含完整语义门（命中才认领），否则空占槽位饿死后面所有分支**。

- **荧光棒投掷态两修正（2026-08-12，用户报"太小+光色变白"）**：
  ① **绘制尺寸**：原版投射物绘制=贴图原生尺寸×scale（与碰撞盒 6×6 解耦）——50/53/515/1089 贴图是 **22×6 横条**，此前 drawProj 按碰撞盒 w=6 画成 6×1.6 细丝；870 妖精 18×96 纵条 6 帧（帧进 5t，转阶段 rotation=0）；473 18×18。GlowstickProj.draw 改原生尺寸自绘。
  ② **光色**：弹幕点光此前用 light 标量发白光——原版 Projectile.ProjLight()（cs:14809）有**逐类型 RGB 乘区表**，荧光棒族（cs:15060-15091）与手持光同色：50=(0.7,1,0.8)/53=(0.7,0.8,1)/473=(1.05,0.95,0.55)/515=(1,0.6,0.85)/870=(0.9,0.35,1)/1089=Disco。Game 弹幕光通道加 PROJ_LIGHT_RGB 表（其余类型暂白光，全表待移植）。

- **静持行冻结走路·补漏（2026-08-12 晚，用户复报"未解决"）**：上次只修了纸娃娃路径（p.appearance），**legacy Maples 路径（默认角色，无捏人外观）有一组同源 staticHoldStyle 分支漏修**——用户走的是这条路径。两路径现为同序：useRow（挥砍姿势）→ 行走循环 → 静持行 → 空中 → 站立。**教训：drawPlayer 有纸娃娃/legacy/程序化三条渲染路径，修帧选择逻辑必须三路同查**。

- **★ 深水自发光修复（2026-08-12 晚2，用户报"原版水越深越黑，我们的水像自发光"）**：
  根因 = TileLightScanner 天空/地狱光播种漏了 **liquid<200 深度门**（原版 ApplySurfaceLight :3172 / ApplyHellLight :3270）——原版仅液量 <200（表面 ~4/5 格）播满天空光，深层液体【不播】，亮度靠表层逐格水衰减（DECAY_WATER≈0.80/格 系）传播 → 越深越暗。我方 exposed() 无此门 = 整个水柱每层满天光 = 自发光。修复：exportTo 天空/地狱播种前加 `st.liquid[i] < 200`。探针（40 宽海洋）：表层 255→173→108→67→42→26→16→10→6→0 海底全黑 ✓。LightMap 水衰减/blur 本就 1:1 无需动。**探针教训：单格宽水柱会被两侧种子空气横向绕射——水体探针必须宽体取中心列；groundLevel 必须在水面以上否则海底下方空气被播天光**。
  **补漏（用户二报"水底地面发光"）**：exposed() 是误植——原版 :3170 第三析取支 =「坡面|半砖 且【四邻 liquid==0】」才放行挡阳实心格；我方写成「自身 liquid>=200 才挡」→ 海底方块自身无液被放行播满天光。修正为原版语义（挡阳实心恒不放行，坡/半砖例外需四邻全干）。探针：海底 R=255→0 ✓、陆地表层仍 255 ✓。**教训：移植判据逐项核对原版布尔结构，析取支内的邻格条件不能省成自身字段**。
  **水面扰动 review 结论（用户问"表层扰动是否漏移植"）**：**未漏，1:1 已在且实证在跑**。原版 1456 水面扰动三组成分：(a) 几何波动 waveMask = **死代码**（WAVE_MASK_STRENGTH 1456 全零无写入；1405 也只 type3=255 非水——两版水类型恒 0，从未有过水面几何起伏）；(b) 纹理动画 1:1（岸边/边缘格 = windSpeed×25±6 fps 16 帧、池体中列 X==16 = 0.5fps 慢纹 1.4.4 新增、满水表层格 IsSurfaceLiquid → Y=1280 静态带）；(c) FrameOffset P1-P6 逐行核对一致。stub-ctx 无头探针实证：岸边 (0,32)→(0,272)→(0,1152) 风驱动跳动、池体 48→208 慢纹、顶行恒 1280（原版同款——湖心满水表层原版就是静态带，扰动看岸边+慢纹）。之前会话删正弦扰动正确。
  **补移植 AllowLightInWater**（TileID.cs:359：54 玻璃/541 回声/328 彩纸/459 降雪/748 水族馆/750 尖刺——水中也透天光，ApplySurfaceLight :3161 独立分支）。遗留未移植：宝石火把墙色（:3190-3242 墙 88-93/241，依赖墙上火把挂载系统）。

- **★ 火把系统全量补齐（2026-08-12 深夜，用户令"遗留+火把挂载全移植，缺啥补啥"）**：
  **先纠正**：所谓"宝石火把墙"遗留实为**彩色玻璃墙**（墙 88-93=紫/黄/蓝/绿/红/彩虹、241 橙，ApplySurfaceLight :3190-3242 满光后 RGB 乘区染色，彩虹档 Disco）——与火把无关，已直接移植进 TileLightScanner 发光墙段。
  **火把挂载系统本已完整**（Torch.ts：四锚放置底0/左22/右44/墙0、onTileChanged 锚失效掉落、ToggleTorch ±66、光照 on/off 门控、火星）——原版也无手动复燃交互（±66 写入点仅 Torch God + Wiring）。**实际缺口四项全补**：
  ① **placeStyle**：放置 frameY 恒 0 → 群系/彩色火把全放成普通火把（色光失）。Torch.ts `torchStyleOfItemKey`（427-433=id-426 彩色 1-7 + BIOME 表 523→8..5353→23）；光照侧本就按 frameY/22 取 TORCH_COLORS ✓。
  ② **水炬**（TileObjectData addSubTile 8/11/17：WaterDeath=false/WaterPlacement Allowed；物品 523 咒火/1333 灵液/4384 珊瑚）：水中可放（放置液体门豁免）+ 水冲不灭（liquid.killTile 豁免）+ 手持水下仍亮（EmitHeldItemLight WaterTorches 无 !wet 门）。
  ③ **Torch God 彩蛋**（Player.cs:17585-17770）：触发=地下+81×41 点燃火把>100+无 5043+冷却 0；每 21t 熄一根(+66)+弹幕 949（TorchGodProj：AI_184 直飞、射程耗尽后撞块、20 伤）；余 1 根且≥95 延 3s；结束批量复燃+≥95 掉 Torch God's Favor(5043)+3600 冷却。新 src/world/TorchGod.ts + WeaponProj TorchGodProj。探针：120 根→全熄+120 弹幕+掉 5043+全复燃+冷却 ✓。
  ④ **Blackout**（buff 80，事件期间每 tick 刷新）：updateLightDecay 第三参 ×0.85（补此前"未实装跳过"注释项）。

- **★ 地狱箱"木箱"修复（2026-08-13，用户报"地狱宝箱是木箱贴图"）**：
  实证定位：地狱专用 pass（runUnderworldChestsPass，采样 y∈(h-200,h-51)）全在 h-205 门内 = style 4 暗影箱 ✓ 没问题；用户看到的是 **h-250..h-205 带（灰烬带上缘）的箱子**——根因 = rollChestLoot 洞穴/地狱战利品分界用了自造的 **h-250 门**，而原版战利品 flag8 与样式 num9=4 **共用 `y > maxTilesY-205` 一道门**（cs:36162-36164 同一处设置）→ 该带箱子拿地狱战利品却配金箱(style 1)贴图。修复：洞穴分支门改 `gy <= worldH-205`。注意：**原版该深度样式本就是金箱**（样式门 h-205 全深度一致）——修复后该带=金箱+洞穴战利品（原版同款），h-205 以下全暗影箱。探针 y=980→洞穴战利品/y=1000→地狱 ✓。回归 740/740 全绿。

- **★★ 全图帧合法性审计（2026-08-13，用户令"审查其他物块类似问题"）**：
  方法：stride-aware 探针扫生成世界全部 active framed tile 的帧（步长对齐+表内范围），误报逐类甄别（meta 缺陷/非均匀行高/多格物非锚格）。**发现并修复 5 类真 bug**：
  ① **雕像 105 换行**：帧单轴 style*36，Tiles_105 每行 **55 列**——原版 PlaceTile case105（cs:39716）`frameX=(style%55)*36、frameY=floor(style/55)*54`；style≥55 全越界（STATUE_LIST 到 78）。修 StatuesPass/TemplePass。
  ② **火把 style 轴向反**（StructuresPass placeTorch）：写 (style*22, 0)，原版 case4（:59863）**frameY=22*style**——style≥6 全越界。
  ③ **187 地被 wrap**：furnitureStyleBase 缺 case → default 单轴；原版 TileObjectData :3303 **StyleWrapLimit=35** + Y 步 36（行高 16/18 非均匀）——LivingTree 叶下地被 style 47-51（cs:28695）在第二行。修 case 187 = [(s%35)*54, floor(s/35)*36]；顺补 case 15 椅子（StyleHorizontal=false 竖排 Y 步 38）。
  ④ **帧残留**：LivingTree setLeaf 等 type 直写不清帧 → 旧 framed 帧残留进 192/1 等（audit 见石头 fx=1080/火把 fx=252）。修 setLeaf 清帧 + **finalize 全图帧越界净化**（像素级粗判 frameX≥表宽||frameY≥表高 → 清 0，V_SHEET_DIM 由 vanilla.json 构建）——兜底一切残留。
  ⑤ 185 小堆 style 59-61 size1 fx=style*36=2124 超 1908 表宽——**原版自身越界**（cs:46849/28725，XNA clamp 渲染），白名单保留原版行为。
  审计收敛后剩余 3 项均误报（103 meta rows=0 / 51 蛛网 22 步长 / 石头 blend 合法帧）。回归 99/101（2 挂=并行会话在途 MushroomPass 半成品）。**审计工具沉淀 /tmp/frame-audit2.mts（stride-aware + 白名单），后续新增 pass 后建议重跑**。

- **★★ 飞行道具全量 1:1 对齐（2026-08-13，用户令"翅膀/飞行靴等检查并 1:1"）**：
  **WingStats 全表**（vanillaWingStats.ts 重写，WingStatsInitializer.cs:26-63 全 51 slot：FlyTime + AccRunSpeedOverride（空中横移上限 6.5-9）+ AccRunAccelerationMult（1-4.5）+ HasDownHoverStats/DownHover 覆盖；旧 JSON 只有 time/speed 23 条已退役）。
  **翅膀飞行**（Player.cs:21746 WingMovement 1:1）：参数表 base (0.1,0.5,1.5,0.5,0.1) + 翼型覆盖（26/37/44/45/29/32/30/31 各档）；上升帽=-jumpSpeed×num3（1.5~4.5 翼型分档，jumpSpeed 基准取本地 PLAYER_JUMP_SPEED=6.6 与跳跃尺度自洽）；wings==4 UFO hover-up 特殊分支；hover 下落无左右移 wingTime 消耗 ×0.5。飞行条件 flag19（:26500）+ hover 族 ↓+跳 分支。
  **滑翔**（:27015）：wingTime 尽后按住跳 = 重力/3 + 终端 maxFallSpeed/3（!hoverDown）——替换旧 vy>2.5→2.5 近似。
  **悬浮缓降**（:27083）：hover 族 + ↓+跳 → vy×0.9（45=0.8）+(−2,1) 归零。
  **火箭靴**（:26548-26628 脉冲模型）：7 脉冲（rocketTime），每次触发=10t 推力段（rocketDelay）+ 速度模型 0.1/0.5/1.5 档（与翅膀同构），焰间隔 rocketDelay2 30(1档)/15(2+档)；触发门 = 松跳后重按（rocketRelease，原版 :20765 松跳置位**独立于地面**——此前放 else 内导致按住跳永不触发）+ canRocket（vy>-jumpSpeed）+ 翅膀不可用时才接管。**无靴时 rocketTime 恒 0**（:26436）——此前无脑回满 7 把飞毯门挡死。
  **飞毯**（:21568）：条件收紧（无多段跳余/jumpHold 空/火箭靴未用/翅膀尽）+ 效果 = vy 钳 -(gravity+ε) 抵消重力（净缓降），删掉旧横向加速近似。
  **空中横移**（WingAirLogicTweaks :28838）：飞行中横移上限覆盖 AccRunSpeedOverride、加速 ×AccRunAccelerationMult、hover 下落态 DownHover 档。
  **翅膀渲染**：Wings_1..51.png 入素材管线（MISC 表+atlas 重跑）+ Renderer.drawPlayer 身后层（PlayerDrawLayers :695：全宽×高/7 帧、hover 族高/6、origin 宽/2 帧高/2、身体中心锚+朝向镜像）+ Player.wingFrame 状态机（flap 1→2→3→2 @6t、滑翔帧 2、地面 0）。
  探针：翅膀 wingTime 100 飞行消耗 ✓、滑翔终端 3.29≈maxFall/3 ✓、火箭靴 7→6→5→4 每 10t 脉冲 ✓、飞毯 vy≈0 缓降+300t ✓。equip-stats 断言更新 wing 全字段。回归其余挂项=并行会话在途（pixel-art/luck/caves）。
  **review 补漏（2026-08-13 晚，用户令"review 移植是否完整可靠"）——4 处偏差修正**：
  ① **翅+靴合并改原版动态语义**（:26523-26531）：地面重置 wingTime=纯 FlyTime（去掉预加 42），空中且 rocketTime>0 时剩余脉冲×6 并入 wingTime（上限 max+本次转换量）后清零——探针 100/7 → 130(142−12t 消耗) ✓；
  ② **vy==0 恢复 rocketTime**（:26540 原版含撞顶悬停等非落地场景，不限 onGround）；
  ③ 清理 wingMovement 44/45 死分支（`!inputJump===false` 优先级垃圾代码——原版 :21855 该分支在 flag19 调用门下本就不可达=死代码证实）；
  ④ 删 wingFlapping 死字段 + Renderer 翅膀层空 tint 占位；hover 横移门补 wingTime>0（:28841 flag 完整条件）。
  **已确认可靠**（无需改）：地面重置无 releaseJump 门（原版 :26169 地面块同样无条件）；滑翔 wingTime<=0 门与原版 flag19 等价；冻结态走 inputJump 清零路径 ✓；绳索/水中分支天然跳过飞行 ✓。**已知未移植（原版死代码或外围）**：tryKeepingHover 粘滞态、empressBrooch 无限翼、火箭靴尘迹视觉、wings==4 音效。

- **EoC 冲刺残影移植（2026-08-13 深夜，用户点名"boss 冲刺速度影子"）**：原版机制 = Main.cs:25469 `type==4 && ai[1]>=4 && ai[0]==3`（二阶段冲刺态）→ 沿 **npc.oldPos[1..9]** 画 9 层鬼影，每层 RGBA×0.5×(10−i)/20（越旧越暗越淡），同一帧/当前 rotation/同一镜像，底锚+halfSize。实现：Enemy 已有 hist 缓冲（histXAt/YAt/historyDepth 公共口）→ Renderer.drawEnemy EoC 分支插鬼影循环（中心锚+eocOff 23/30，近似 alpha=(10−i)/40 不做 RGB 减半）。门= dashing && phase≥2（原版 ai[1] 连冲次数≥4 档的近似）。**原版其余拖尾族已索引**（同类机制备查）：471 星云柱头（:25487 ai[3]<0 同款 oldPos 循环）、370/372/373 猪鲨（:23962 ai[0] 档 num230=7/10 层 + 蓝 tint）、402 银河织带（:23863 oldPos+oldRot 双插值 0.8 渐隐）、519/522（粉/白收缩尾）、636 光女（:23089 oldPos+oldRot 0.35×(1-n/10)）、Queen Slime 跳跃翼影（:23210 ai[0]==4 时 8 层 0.75 收敛）。

- **★ 神庙祭坛悬空 + 石巨人召唤修复（2026-08-14，用户报"祭坛半空+电池点击无效"）**：
  **悬空根因**：TemplePass 祭坛放置只查"3×2 空置"，缺原版 Place3x2 锚点门（cs:52127-52153 底行下三列 SolidTile2）+ 无 1000 失败兜底（cs:34261-34315 向下扫实心+强制铺 3 格 226）+ 无 LihzahrdAltar 终保 pass（cs:21753-21791 重放祭坛+下方强制地板）。末间采样框中心±15 下方几乎必为空气 → 必悬空。修复：锚点门+兜底+lAltarX/Y 入 GenState+终保段并入 pass 末尾+宝箱祭坛±3 回避。探针 3 种子 1 庙 1 祭坛 0 悬空 ✓。
  **召唤链路已存在且 1:1**（interactAt→useLihzahrdAltar→golemSpawnFromAltar，NPC.cs:81278 1:1，探针落位 y=(2up+down)/3 ✓）。无效的两个真原因：① 门禁静默（hasNpcId(245)/!hardMode/!downed_262 原版静默，本作补 toast：Toast.BossActive/NeedHardMode/NeedDownedPlant——**注意 BossAlreadyHere 键是"已击败"语义不可复用**）；② **右键被 findChestNear 的 ±1 格宝箱搜索截走**（神庙箱全庙散布贴祭坛；原版无 ±1 搜索）→ 光标格是 237 时跳过搜索。玩家自摆祭坛帧 OK（tryPlace furnitureStyleBase default [style*54,0]+dx*18 含顶中格 (18,0)，golemSpawnFromAltar 扫描需要它）。

- **★ 棕榈树冠消失修复（2026-08-14，用户报"有的棕榈树冠不见"附 debug-report 截图）**：
  定位法：逐 pass onWorldPartial 追踪（Surface pass 生成时 24 棕榈全带冠、管线末仍 24 → 损失在 finalize）→ 插桩锁定 **finalize 帧越界净化误杀**。根因：棕榈 323 干身/树冠的 **frameY 是有符号像素倾斜偏移**（u16 回绕 65534=-2，VanillaTiler.ts palm 分支 `fy>=32768?fy-65536` 解码绘制）——净化裸比对 `fy>=表高` 把左倾棕榈（回绕值）当越界清零 → 冠标记帧(88-132)归 (0,0)=普通干身 → WindSway 认不出冠格不画。修复：**净化对回绕区间(≥32768)一律跳过**（刻意的有符号偏移，残留脏帧只会是小正值）；RenderAudit 同步修正。验证：两种子 24/24、11/11 全带冠。**教训：帧数据里 ≥32768 的 u16 回绕值是"带符号语义"标记，任何帧校验/净化必须先排除回绕区间**（该约定此前只在渲染端 VanillaTiler 一处有注释，净化/审计两处都漏了）。
