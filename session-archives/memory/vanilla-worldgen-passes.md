---
name: vanilla-worldgen-passes
description: "原版 1.4.0.5 世界生成 105 pass 完整管线清单(行号索引,从 Terarria1405/WorldGen.cs 提取)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-07T15:51:01.029Z
---

源:`~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs`,驱动 `GenerateWorld`(L4652),105 pass 顺序注册后 `L11204` 顺序执行。共享 RNG(`genRand`)的调用顺序 = 种子复现契约。**pass 顺序不可调换**(后续 pass 读前序状态)。

## 阶段 A — 初始化+基础地形 (1-8)
1 Reset L4742: 掷矿石替代(每档50%)、crimson 旗标、dungeonSide/jungleX/snowOrigin/beach 宽度/dungeonLocation
2 Terrain L4896(TerrainPass.cs:40): 每列随机走 Plateau/Hill/Dale/Mountain/Valley,输出 worldSurface/rockLayer/waterLine/lavaLine
3 Dunes L4913: 1-2 沙丘+金字塔候选(40%)
4 Ocean Sand L4962: 海滩列转沙
5 Sand Patches L5043: 1.3%×宽沙 blob
6 Tunnels L5055: 垂直入口井
7 Mount Caves L5091: 地表隆起(`Mountinater` L48367)
8 Dirt Wall Backgrounds L5149

## 阶段 B — 泥石混合+洞穴 (9-15)
9 Rocks In Dirt L5174 / 10 Dirt In Rocks L5195 / 11 Clay L5205
12 Small Holes L5234 / 13 Dirt Caves L5258 / 14 Rock Caves L5279
15 Surface Caves L5295(五子步+`Caverer` L48064)

## 阶段 C — 生物群系 (16-20)
16 Ice Biome L5372: 逐列雪转换,per-row 随机走边界 snowMinX/MaxX
17 Grass L5464 / 18 Jungle L5490(JunglePass.cs:35: mud TileRunner×3+巨型 runner+隧道+洞穴)
19 Mud Caves To Grass L5499(`SpreadGrass(59,60)`)
20 Full Desert L5525(DesertBiome.Place,含地下蚁狮巢 UndergroundDesertLocation)

## 阶段 D — 天空+微生态石 (21-29)
21 Floating Islands L5552(`CloudIsland` L47397/SnowCloud L46793/DesertCloud L47095/CloudLake L47704)
22 Mushroom Patches L5634(`ShroomPatch` L48648)
23 Marble L5755 / 24 Granite L5778
25 Dirt To Mud L5809 / 26 Silt L5819
27 Shinies(矿石)L5837:**全硬编码**——Cu/Sn 6e-5+8e-5+2e-5、Fe/Pb 3e-5+8e-5+2e-4、Ag/W 2.6e-5+1.5e-4+1.7e-4、Au/Pt 1.2e-4×2,深度三带 sky→surf→rock→bottom;Demonite/Crimtane 2.25e-5@rock 以下
28 Webs L5924 / 29 Underworld L5952(ash+岩浆+狱石+`AddHellHouses` L16068)

## 阶段 E — 邪恶生物群系 (30-33)
30 Corruption L6059:**crimson 或 corrupt 二选一**。Crimson:`CrimStart` L45443 垂直裂隙+地表转换(crimsand 234/crimson stone 203/crimson grass 199)+10-15 祭坛+`CrimPlaceHearts` L45644;Corrupt:`ChasmRunner` L45779(makeOrb)+裂隙+黑檀石球+暗影之球。排除区:雪原/丛林/地牢/沙漠/中心±200。数量 0.045%×宽
31 Lakes L6448 / 32 Dungeon L6565(`MakeDungeon` L18006)/ 33 Slush L6590

## 阶段 F — 山洞+海滩+宝石 (34-39)
34 Mountain Caves L6628(`CaveOpenater`+`Cavinator`)
35 Beaches L6639(`TuneOceanDepth`,水从 x≈220-260 起)
36 Gems L6754(6 宝石 [0.3,0.1,0.25,0.45,0.5,0.05]×宽×0.2)
37 Gravitating Sand L6831 / 38 Ocean Caves L6856(`oceanCave` L46199) / 39 Clean Up Dirt L6873

## 阶段 G — 金字塔+活木树+祭坛+丛林内容 (40-48)
40 Pyramids L6943(`Pyramid` L12286)
41 Dirt Rock Wall L6974
42 Living Trees L6984(`GrowLivingTree` L12508,0-2 棵巨型+伴生)
43 Wood Tree Walls L7118
44 Altars L7141(2e-5×面积,Place3x2)
45 Wet Jungle L7169 / 46 Jungle Temple L7190(`makeTemple` L17158) / 47 Hives L7219 / 48 Jungle Chests L7264

## 阶段 H — 液体+清理 (49-56)
49 Settle Liquids L7395 / 50 Remove Water From Sand L7433 / 51 Oasis L7470(`PlaceOasis` L4428)
52 Shell Piles L7488 / 53 Smooth World L7564 / 54 Waterfalls L7696 / 55 Ice L7742 / 56 Wall Variety L7758

## 阶段 I — 箱子+水晶+雕像+微生态 (57-67)
57 Life Crystals L7828(2e-5×面积)
58 Statues L7858
59 Buried Chests L7906(洞穴箱 35-40+地狱箱 7-10+**地下小屋** 35-40 via CaveHouseBiome)
60 Surface Chests L7976 / 61 Jungle Chests Placement L8030 / 62 Water Chests L8060
63 Spider Caves L8138(`Spread.Spider`,0.5%×宽)
64 Gem Caves L8168(`gemCave` L3751) / 65 Moss L8191 / 66 Temple L8359(`templePart2`) / 67 Cave Walls L8366

## 阶段 J — 树+岛屋+罐 (68-72)
68 Jungle Trees L8450(`GrowUndergroundTree` L15153)
69 Island Houses L8463(`IslandHouse` L48185)
70 Quick Cleanup L8472
71 Pots L8554(样式按生物群系:normal 0-3/snow 4-6/jungle 7-9/dungeon 10-12/corrupt 16-18/crimson 22-24/hell 13-15/marble 31-33)
72 Hellforge L8627

## 阶段 K — 表面装饰 (73-77)
73 Spreading Grass L8668 / 74 Surface Ore L8772 / 75 Fallen Log L8826 / 76 Traps L8932 / 77 Piles L8983

## 阶段 L — 出生点+植被 (78-96)
78 Spawn L9469 / 79 Grass Wall L9509 / 80 Guide L9589 / 81 Sunflowers L9625
82 Planting Trees L9651(`GrowEpicTree`+`AddTrees` L15642/`GrowTree` L14171/`RandomizeTreeStyle` L2817)
83 Herbs L9670(`PlantAlch` L25704) / 84 Dye Plants L9679 / 85 Webs And Honey L9686
86 Weeds L9733 / 87 Glowing Mushrooms L9772 / 88 Jungle Plants L9801 / 89 Vines L9821(草/花/丛林/蘑菇/猩红) / 90 Flowers L9990 / 91 Mushrooms L10054
92 Gems In Ice L10082 / 93 Random Gems L10108 / 94 Moss Grass L10143 / 95 Mud Walls In Jungle L10171 / 96 Larva L10217

## 阶段 M — 收尾 (97-105)
97 Settle Liquids L10247 / 98 Cactus+Palm+Coral L10285(`GrowPalmTree` L11785/`PlantCactus` L31805)
99 Tile Cleanup L10421 / 100 Lihzahrd Altars L10729
101 Micro Biomes L10754: DeadMansChest 10-20 / ThinIce 3-5 / **EnchantedSword** 1-2@25% / Campsite 6-11 / MiningExplosives 14-29 / MahoganyTree 6-11 / **矿车轨道** TrackGenerator 1-2×400-1000+4-7×150-300 / lavaTrap
102 Water Plants L10894 / 103 Stalac L10940 / 104 Remove Broken Traps L11009 / 105 Final Cleanup L11025

## 关键 workhorse 方法
- `TileRunner(i,j,strength,steps,type,addTile,xDir,yDir,noYChange,overRide,wall)` L46405 — 地形/洞穴/矿石/沙/泥全用它,**移植优先级最高**
- `SpreadGrass(from,to)` / `ChasmRunner` L45779 / `CrimStart` L45443 / `CrimPlaceHearts` L45644 / `AddShadowOrb` L16035 / `CheckOrb` L31813(暗影之球整体破坏,已移植进 Game.smashOrbHeart)

相关:[[vanilla-worldgen-port-status]] [[reference-vanilla-source-of-truth]]

## 树放置半砖修复(2026-08-10,用户报"树长在半格方块上/侧根三格地只给一格")
对照 1456 WorldGen.cs:29924-29969(GrowTree 头部):基座必须 `nactive() && !halfBrick() && slope()==0` + IsTileTypeFitForTree(2/23/60/70/109/147/199/477/492/633/661/662) + 上格墙白名单 + (i±1,j)三列无液体 + **至少一侧邻格也适树**(OR 语义,单侧即合法——"三格地只给中间一格"的崖边树原版就有,根只放有地面侧);:30227-30311 侧根只在整砖+fit 的侧放置(num6: 0=双/1=右/2=左,3=无);:30313-30366 基座帧 0→88/1→0/2→66(无 case3)。**我们的 TreePass 逻辑本就 1:1,缺的是半砖/坡面检查**(runSmoothWorldPass L289 先于 runTreePass L664,半砖已存在)——growTree/growTrunk.fitSide/growEpicTree/growPalmTree 四处补 `!half && slope==0`(棕榈同款 :27280-85)。运行时 growSaplings(Game.ts)原本无任何检查,补 草族+整砖+单侧 fit。**验证方法论**:存档是 btoa 真 base64+varint RLE(Buffer.from(s,'base64') 解码,勿用 charCodeAt);全图扫描 0 悬空根/0 基座根不匹配/0 悬空树干(侧枝帧 fx66 fy0-44/fx88 fy66-110/fx44|66 fy198+ 天然悬空须排除);像素级验证 Tiles_5(1408×264):基座帧 0/66/88 完全对称无侧 bump,根帧 fx22 偏左/fx44 偏右——用户标注的两棵树(599 步台树/605 崖边树)存档层面全部合规。E2E 新世界:314 树+19 棕榈,半砖上 0、悬空根 0。

## ★ 存档 id 稳定化 v3(2026-08-10,用户报导入世界大范围贴图错乱)
**根因**:sandboxworld.save 把 tile/item 存为 TILE_DEFS/ITEM_DEFS **数组下标**(两文件全手写、v_* 段顺序=compat-report 手抄混沌序),另一会话编辑后下标漂移→旧存档"下标→def"对照失效(整列 v_616 黄柳树变 v_530 绿洲植物、帧却是树帧=指纹特征)。**新存档/新导入自洽所以没事**;墙 id 早已直用原版值(现成范本)。
**根治(方案 A,磁盘稳定 id+双收口映射,~5 文件;方案 B 运行时全面换 id 需动 ~100 文件否决)**:
- tiles.ts/items.ts 末段:`TILE_STABLE_OF_INTERNAL/INTERNAL_OF_STABLE`+item 同构;v_* def=vanilla sheet id,**PRIV 冻结表**1000+(29 条:23 无 sheet 家具/自造+借用 sheet 的 mushroom/flower/tallgrass(真身 v_3)+tree(真身 v_5_trees)+v_389 开门态+dirt(sheet 0 让位 air 哨兵));物品 vi_=key 内嵌原版 id、自造 489 条 PRIV 10000+(运行时枚举冻结,**循环模板 key(护甲/药水)静态正则会漏——必须运行时枚举**);同 vid 双注册(字面量+运行时拼写)冲突=双 def 同 stable、读档归一首个
- serialize.ts v3(version 3+idScheme:'sheet'):rleTiles 加 stableMap 参数内联映射;物品 mapItem 遍历 chests/inventory/banks;SaveFile.loadSaveData v3 分支反向映射(**save.worker/worldGen.worker import 同模块自动覆盖**)
- **tools/migrate-save.mjs**:git 历史 ref 恢复旧顺序(header.created→`git log --before` 自动选,可 --ref 指定)→旧下标→当时 key→当前 stable;PRIV 提取正则要兼容无引号 key(`empty: 1000`)
**大坑**:created 是**导出/存档**时刻,而 id 是**载入/导入**时刻的顺序——自动选 ref 会选错(Starter World 实测:created 前最后 commit 44df 是错序,真身是 6e930dc6(唯一 key[184]=v_616 的 commit,用"标注点帧语义"做指纹全历史扫描定位)。**迁移定位法:拿原始 .wld 直读标注点 vanilla id(parseWld)→ 反查哪个历史 commit 的 key[存档id]==该 vanilla 对应 key**
**验证**:idstable 11(恒等/roundtrip/值域(tree=1026/v_5_trees=5/v_530=530/dirt=1028)/air 哨兵);迁移产物 6/6(标注点 v_616+帧 22,198 与 wld 真身逐位一致,1152 万格 0 落空);vitest 190+wiring31+lighting51+door ✓。v3 后 TILE_DEFS 顺序永久自由。

## ★ 坡面渲染 + 水面波动(2026-08-11,用户报"草地方形/水面无波动")
**四层断裂全修**:
1. **渲染**(`VanillaTiler.ts`):新增 `drawSlopedFrame`(原版 TileDrawing.cs:1328-1360 切条算法 1:1)——slope 1/2(左高右低/右高左低): 8 条 2px 竖条 src(2i,0) h=14-2i dst(2i,2i+2) + 底部 16×2 补条; slope 3/4(源行偏移) + 顶部补条。blend(:516)/auto/style(:587) 三条路径接入 slope/half 判断。半砖改源矩形裁剪(源 y+8 高-8)。**原版坡面不是独立贴图帧——是同帧错位切条采样**。
2. **生成**(`HalfBrickPass.ts`):还原 `slopeTile(st,x,y,dir)`(写 slope 清 half),6 处 poundTile 改 50% slopeTile/PoundTile 随机二选一(与原版 L7598-7616 一致)。实测新世界 slopeCount=5954 格。
3. **wld 导入**(`WldParser/WldImport`):`(header2>>4)&7` 解码 half/slope(WorldFile.cs:1519),`SaveData.blocks` RLE 字段(0=整砖 1=半砖 2-5=slope1-4),save/load/worker 全链路传递。
4. **水面波动**(`VanillaLiquidRenderer.ts`):P4 中 `hasTE` 的 TopWall 加双频正弦扰动 `sin(x*0.8+t*0.004)*0.04+sin(y*1.3+t*0.003)*0.03`,幅度按 VISCOSITY 反比(水×1/岩浆×0.25/蜂蜜×0.12)。原版 `_waveMask` + `WaveFilters` 语义。
**回归**:vitest **367/367**(另一会话新增大量测试)。E2E:slope 格 chunk 像素级验证通过(topRightTrans=24)。
**待做**:①BlockStyle blend 掩码过滤(Framing.cs FindBlockStyle,半砖/坡面邻居应断开帧连接) ②锤子 slope 循环(整砖→半→坡1-4→整) ③平台(tile 19)坡面专用帧。

### 收尾(同日补)
- **BlockStyle 过滤已做**:`VanillaTiler.ts` blend 路径邻居掩码按原版双向门控(Framing.cs:92-98 blockStyleLookup + SelfFrame8Way:199-316)——half 断上;slope1 断上/右;slope2 断上/左;slope3 断下/右;slope4 断下/左;中心 own edge && 邻居 opposite edge,角落需两向同时放行。mergeMask 同步受门控。
- **关键 bug**:drawSlopedFrame 越界保护误写 `(r.img).naturalWidth || r.img.width` 挂在 || 链中间 → 恒真 → 8 条全部跳过只画补条(这就是首测 topRightTrans=24 异常根因)。修复为 `r.img.width`。HTMLImageElement/HTMLCanvasElement 均有 .width/.height。
- **ChunkCache 第三遍 clearRect 保留**(兜底 vframe(1,1) 全帧回退路径),注释已更新。
- 顺手修两处并发遗留 tsc 错误:VanillaSpawner.ts/Game.ts 的越作用域 `raining`/`w.weather` 引用 → `this.world.weather.raining`。
- **E2E 验证脚本 `scripts/_slopevis.mjs`**:chunk tile canvas 按列 solidStart 断言斜坡对角线(slope1 [0,6,8,10,16] / slope2 [14,10,8,6,2] ✓)+ 全视口双帧 diff 验证液面波动(2349px ✓)。坑:游戏每帧把相机吸回玩家,手动 set camera 无效→把玩家放进水里让其漂浮,液面留在视口内;world gen 偶发 >300s 超时重跑即可。
- 最终:vitest **369/369**,tsc 干净,dist 已重建。

### Review 逐函数对账(2026-08-11 第二轮,7 处偏差全修)
对照 1456 反编译逐函数复查发现并修复:
1. **SmoothWorld 三路分支**(16562-16591):缺 else SlopeTile(2)/(1)——**60% 概率的坡面源**!此前只 kill 1/5 / pound 0.25,坡面全丢。修复为 Next(5)==0 删 → Next(5)==0 半砖 → else slopeTile。slope 格数 2.8万→6.3万。
2. **悬顶 slope3/4 分支**(16642-1652)整体缺失,已移植(下方空+上方实+旁格 blockType==0 → slope3/4)。fullOrEmpty 辅助注意 blockType==0 要查 half+slope 双位。
3. **Loop B 清理**(16672-16685)缺失:沙族 Conversion.Sand{53,112,116,234}→Tile.SmoothSlope(822-880 已移植,按四邻位形自整半坡);slope1/2 无支撑→slopeTile(0)+PoundTile 回落半砖。
4. **类型排除表**:16518 蘑菇树 136 旁格 / 16600 补角材料 151/274 / 16602/16621 旁格 190/48/232 / Loop B 主排除 137/48/232/191/151/274/75/76 + 两侧仅 137(右侧是 (active||type!=137) 原版怪式,别"修正"它)。
5. **角连通交叉边**(Framing.cs:269-316):corner 需两个正交邻居的交叉边放行(N 邻 down|right 等)——SelfFrame8Way 里正交未连通会 Clear() 导致角失败,单查对角不够。
6. **SaveSlopes 门禁**(WorldFile.cs:2623):加载端只对 tileSolid∪{131,351,336,340,342,341,343,344} 应用 half/slope,家具类杂波 bit 丢弃。WldImport 已加门禁(按内部 def.solid||wld id 例外表)。
7. **水面正弦扰动是伪需求**:1456 的 waveMask 是死代码——WAVE_MASK_STRENGTH=new byte[5] 全零从不赋值+WaveFilters 事件全工程无订阅者(LiquidRenderer.cs:110/616)。用户看到的"波动"=16 帧纹理动画(已 1:1,:289-291)+表面静态带 y=1280(:636-644,:314-316 已 1:1)。正弦扰动已移除。
仍保留的已文档化近似:CanPoundTile 黑名单/CanBeClearedDuringGeneration/PlaceTile 495 特判。
E2E:scripts/_slopevis.mjs 已含 slope3/4 顶部锚定断言(solidEnd),6/6 过;vitest 374/374;dist 重建。

### 最终扫尾轮(第三轮,周边链路补漏)
1. **wld wire 解码是 1.3 布局的陈年 bug**:`(header2&0x3E)>>1` 会把 half(0x10)/slope(0x20) 位漏进黄线/致动器位,且真黄线(header3 0x20)/致动器(header3 0x02)/已致动(header3 0x04)全丢。1405 反编译证实 1.4.0 就是新布局(WorldFile.cs:1676-1690)。已修:红蓝绿=header2 0x02-0x08,黄/致动/已致动=header3。
2. **锤子 6 态循环已还原**(Player.cs:45625-45695):整砖→半→slope1→2→3→4→整;方向感知(右实左空先 slope2)+天花板模式(上实下空先 slope3/4)。平台锤循环(:45394)依赖楼梯绘制未移植暂缓。
3. **碰撞坡面支持**(此前完全缺失——slope 数据一旦存在就暴露):`TileCollision.ts` 三件套——①moveAxis X/Y 加 flag3 坡面放行门(:2361-2387:贴高/低侧走过不拦)+hoik 坡链放行(:2412/:2432:身后格配套坡→不拦);②slopeCollide 后处理=原版 SlopeCollision(:1796-2036)对角线贴合(沉到斜面下抬回,取最大抬升;抬升受阻守卫);③slope3/4 天花板对称推离。E2E `scripts/_slopephys.mjs`:玩家贴 slope1 对角线 ✓ 整砖回归 ✓。
4. **mask8(auto 帧路径:矿石/冰雪/沙漠/基础方块)补 BlockStyle 双向门控**——与 blend 路径同款表;角组合位 U|L=3/U|R=5/D|L=10/D|R=12(首轮写错 9/12/6 已修)。
5. 存档视图/worker/infiltration half 分支核过无遗漏。
**并发会话冲突提示**:宝石系统(GemPasses/WorldGen vanillaGems)正被另一会话重构,中间态导致 gem 测试偶发失败+WorldGen 拼写类 tsc 错误漂移——非本链路改动,17:23 全绿基线可证。

### 坡面碰撞二连修(用户实测反馈驱动)
**用户报告①"上坡卡住往后退"**:根因=我们的 X 拦截与原版语义差——原版只在【上一位置完全在格一侧】(贴面接近,:2406/:2426)时拦;我们只查"前沿列有实心且脚低于其顶",上坡中段身体已跨在坡格列上被每帧推回。修复:moveAxis X 加 face-to-face 前提(oldX 完全一侧才拦)。
**用户报告②"坡顶过渡踏空沉入"**(标注 map-违法的要塞 (2236,276)=slope1,西邻整砖):根因=lift 的 num4=左缘-坡格左边界,越过高侧缘瞬间 <0 脱钩(:1935 原版同款 num4>=0 门),脚底残留在对角线端点下方 0-3px → Y 落地门槛(上一位置须在顶上)不补救 + hoik 放行 → 重力累积整行下沉。修复:**num4 钳 ≥0**(与原版的有意偏差,函数头已注明)——贴合保持到水平重叠结束,送脚到对角线高端点(=相邻整砖顶)由常规落地接管。
**E2E `scripts/_slopephys.mjs` 五项**:贴对角线/整砖回归/上坡行走(轨迹式断言)/用户布局雕刻复现(沉入 0px×4 轮)。坑:测试选址必须查出生区净空(树干/上方块),平台要加宽+安全地板防摔死重生污染断言;并发会话改 Player.ts 落地瞬间会造成单轮漂移,重跑即净。
**后续**:vitest 404/407,3 失败皆并发会话区(caves 金标 jungle pass 分歧/world-store 排序);dist 已重建。

### 坡面碰撞第三轮(flag3 根因 + 回退/辅助落地)
**flag3 低侧门根因**:原版 :2375/:2379 地面坡放行门是 `feet-|vx| <= 格底(top+16,num7=格高)`,此前实现成 `<= 格顶`——差 16px,导致孤立坡(无 hoik 链)低侧贴地进入永远被 X 拦在坡前一格卡死。修正后低侧进入→贴合爬升全通。
**受阻回退教训**:原版 :2010-2015 的 X 补偿按 shortfall 全量推,但其"重跑校验"保证单次;分轴结构下输入每帧再加速,X 推会变**棘轮**(每帧推一点)——只取速度清零、不推 X。
**速度辅助**(:1773-1790)已移植:落点候选 slope1/2+水平朝低侧+脚沉到对角线 → dy+=|dx| 粘斜面。
**测试方法论**:坡面碰撞回归改为**确定性单元测试** `tests/slope-collision.test.ts`(逐格构造布局直接驱动 moveAndCollide,3 场景:低侧爬升/墙角挡停/用户标注坡顶过渡)——浏览器 E2E 对此受输入抖动+自然地形+并发会话 HMR 三重干扰,只作视觉层验证。原版同款墙角推演:悬垂面在坡前一格就把人拦住(:2426),lift-revert 场景其实不可达。
vitest 451/453(2 失败=caves 金标 jungle pass,并发会话区);dist 重建。

### Review 第四轮(vector3 对齐)
- **flag3 判定基准修正**:原版 flag3(:2361-2387)全部以 vector3=移动前位置判定(:2306);此前用移动后 b.x/b.y,边界差一个子步(≤8px)。slopePass 改为传 (ox,oy):X 相用 (oldX,b.y),Y 相用 (b.x,oldY)。单元 3/3 不变。
- 速度辅助注明近似:原版作用于整行落地候选格,我们取脚底中心格(单格采样)。
- E2E 键盘输入在并发会话负载下偶发掉帧→前进距离不足断言;物理真值以 tests/slope-collision.test.ts 为准。半砖台阶拦截=原版语义(需跳)。
- vitest 449/451(仅 caves 金标 jungle pass 2 项,并发会话区);dist 重建。

### 树干-草块接缝修复(用户 wld 导入报告,2026-08-11)
**根因**:原版 GetTileDrawData case 5(TileDrawing.cs:4688-4694)树干族(tile 5/583-589/596/616/634/323)精灵 **20×20**(22px 网格取 20),普通通道(:1019-1025)dest=(x*16-2, y*16+tileTop) **顶锚定**→向下溢出 4px 盖住草块顶,接缝天然消失。我们 drawTreeCell 此前按 treeFrameBottomPad 测量美术高度**底锚定**(py+16-artH),整体上移 4px → 干底停在格边界出透明缝。
**修复**:干身族+棕榈干身改顶锚定 `drawImage(img, fx, fy, 20, 20, px-2, py, 20, 20)`;treeFrameBottomPad 已删。E2E `scripts/_treeseam.mjs`:格底连续 12/12、4px 下溢带 48/48 全覆盖。回归:树基座断言+slopevis 6/6+slope 单元 3/3。
**教训**:底锚定当时是为"短帧底部透明行"自作聪明,原版从不适配——顶锚定链式绘制下一格盖上一格空行。改绘制锚定前必须先查 case 表。

### 接缝机制全面审计+补齐(2026-08-12,用户"必须移植过来补齐")
审计代理五类清单(A 尺寸≠16 / B tileTop / C 手动偏移 / D 邻接特判 / E 帧重排),已移植:
- **A 顶锚定+X 居中公式**(:1019-1025):通用路径 dy 从底锚 `py+16-sh` 改原版 `py+tileTop`、`dpx = px-(sw-16)/2`(711 豁免 DoNotAdjustDrawPositionBasedOnTileWidth)。高>16 精灵向下溢出盖住下格顶=接缝合拢的本源;旧底锚是家具/植物悬浮与树缝共同根因。火把 dxOff=-2 特判删除(公式覆盖)。
- **D1 邻居半砖衔接**(:1609-1652)全新 `drawHalfBrickSeam`:本格整砖实心+左右邻半砖 → 素材表预制衔接帧(双半砖:(126,0)/(90,0 上邻同型);单侧:num8=SMOOTH_BORDER?2:4,主体砍 num8 列+角帧(144,0)+(148/156,0) 2px 补点)替代整帧。四 Set 全量:DONT_DRAW_SLOPES/IGNORES_NEARBY_HALFBRICK/NOT_REALLY_SOLID/SMOOTH_BORDER(~150 项)。
- **D2 半砖底部暗条**(:1657-1667):半砖下方无支撑 → 底 4px 换 (144,66) 光照条。
- **坡面门控**:HAS_SLOPE_FRAMES{421,422} 整帧;DONT_DRAW_SLOPES 跳过切条走整帧。
- **B 表换血**:DRAW_Y_OFFSET 从 TileObjectData.DrawYOffset 换成 GetTileDrawData tileTop 权威(旧表只管放置虚影!16 项多余/3 值错/条件全缺)。条件型 tileTopCond:136/443/567/388/389/184(185-187 落穿)/442/178。
- **C 手动偏移** vectorOffset:726(按 slope ±6/±2)/129/723/724/751/752/136/442。
**未移植备案**:E 类 X 翻转(x%2 FlipHorizontally ~30 组,植物镜像变体)/698(36×44)/518 动态水位 tileTop/751/752 非锚点帧跳过/D3 平台坡面填充(需 BehindTiles 层)/D6 tileTop 分层(OverTiles/BehindTiles)。
回归:slopevis 6/6 + treeseam 3/3 + vitest 549/552(3 失败皆并发会话区:caves 金标 rocksclay/jungle + 萤火虫 StepUp)。dist 重建。

### 接缝补齐第二批(用户"把所有都补齐",2026-08-12)
- **仙人掌彻底 1:1**:`cactusFrameAt` 重写为原版 WorldGen.CactusFrame(:56354-56560)——基列下行搜索+臂列平移+num3 三分支帧表(fx∈{0,18,36,54,72,90,108}×fy∈{0,18,36});drawCactusCell 加 tileTop +2(case 80 :5083)。**澄清:tile 80=仙人掌(16×16/变体行 54/108/162);32×38 的 case 227 是染料植物**(TEdit 名),曾误当仙人掌。单测 tests/cactus-frame.test.ts 5 项。
- **X 镜像翻转**:FLIP_X_EVEN 41 组(全为 x%2==0)——canvas translate+scale(-1,1);杂草/藤蔓镜像变体自此与原版一致。
- **尺寸覆写+帧重排** `drawAdjust`:HEIGHT_18 组(31 sheet)、529(高 32+源行 34*生物群系变体)、698(36×44+fx 重排)、751(56×46)/752(36×38)、185-187(宽 20)、624(高 16)、711(fx>0→18×20)、561(高 20)、270/271/581(旋 6)/660(旋 5)/572(旋 4)、593/594(-18/-36)、507/508(90*counter 公式)、336/340-344/739/748(90*帧)、405/406(38/56)、617(%54/%144)、129(addFrX)、530(36*生物群系)、227(fx==204 变体列,原版原文如此)。
- **D3 平台坡面**:平台 slope 不走切条——整帧+下侧对角实心时背面填充(slope1:(198/324,fy) / slope2:(162/306,fy) 于 (0,+16),:1540-1567);BlocksStairs/隐形块条件近似略。
- tileTopCond 增 227(fx==238?-6:-20)。
**仍备案(需运行态或分层架构)**:D6 tileTop 三层分层(OverTiles/BehindTiles)、518 水位动态 tileTop、428 压板被踩、485/489/490/493 风摆帧、349/441/468 临时帧、751/752 非锚点帧跳过、405/406 高度按帧切换。
回归:cactus 5/5 + slopevis 6/6 + treeseam 3/3 + vitest 617/620(3 失败皆并发会话: caves 金标×2 + 萤火虫 StepUp);dist 重建。

### 接缝补齐第三批(终批:运行态机制+分层架构结论)
- **分层架构结论**:原版三层(OverTiles/Tiles/BehindTiles,:885-896)在我们"双画布+列主序烘焙"下行为等价——下行溢出被后画的下行格覆盖(=BehindTiles)、上行溢出自然盖住上方格(=OverTiles),treeseam 下溢断言实证。无需拆三画布(+50% 内存无收益)。
- **428 压板被踩**:Game.weightedLatch 每帧镜像到 VanillaTiler.plates428Pressed,drawAdjust 428 → sx+18(:5697-5703);12/31(水晶心/魔球)tileTop+4 补表(与 428 同 case)。
- **风摆族**:renderEnv{wind,worldSurface} 由 Renderer 每帧刷新;inAPlaceWithWind(WorldGen:87603,AllowsWind 墙集未提取→任何墙挡风保守近似);485 恒摆/489 风门2×3 16帧/490 bob+强风偏移/493 风速分档 6/12 帧带。
- **518 悬挂火盆动态 tileTop**(:4648-4675):liquid/16-3,上方整砖钳 8,无水看下方半砖(-16+max(8,液))或坡(-4)。
- **751/752 锚点帧独绘**(:1034-1048):非 (0,0) 帧整格跳过。
- **719 族(28/105/470/719)**:14 相位 (x+y+t)%14 → 288/270 双轴;405/406/452-456 各公式全量。
- **临时帧(349/441/468 GetTemporaryFrame)不可移植**:依赖原版瞬态动画触发系统,我们无对应运行态——唯一真正无法落地的项,备案。
回归:cactus 5/5 + slope-collision 3/3 + slopevis 6/6 + treeseam 3/3 + vitest 635/637(仅 caves 金标 2 项=并发会话区);dist 重建。物理浏览器 E2E 在并发会话改 StepUp 期间漂移,以单元为准。

### 594 风气球"完整逐帧贴图"修复(用户标注"史莱姆雨的史莱姆气球")
**先澄清**:用户看到的"史莱姆气球"不是史莱姆雨产物——是 1.4.4 的**风气球(594 Windy Balloon, aiStyle 113)**:大风天飘来、下面挂一只史莱姆(金-4/母-7/绿-3,ai0=-999 冻结),爆裂后史莱姆落地开打。我们 AI_113/windyBalloonAI 已移植,炸的是【渲染】。
**根因**:NPC_594.png 是 **8 列变体横条**(256×76=32×76×8),vanilla-npcs.json `frames:1`(npcFrameCount 只数动画帧不数变体列)→ vnpc 的【纵向帧条】假设 → 整条 256 宽全画 = "完整逐帧贴图"。
**修复**:Renderer.drawWindyBalloon 专属分支(Main.cs:23380-23406 + FindFrame :68652-68656 1:1):变体帧 = ai[2] 1-7 按 32px 列切;挂载史莱姆时帧 0 以 slave colorRGBA 两遍染色(气球壳随史莱姆染色,同 tintedSprite 两步法);锚点=npc.Top 顶部居中+visAngle 旋转;scale=slave.scale。vnpc 头部加 ⚠ 注释:横向变体条 NPC 必须走专属分支。
**教训**:vnpc 纵切假设对"横向变体表"NPC 是地雷;npcFrameCount ≠ 变体列数。同类风险 NPC(凡 Main.cs 里 Frame(N,1,x) 横向取帧的)逐一排查留待后续。
**验证**:浏览器 E2E 因机器负载 50+(13 并发会话跑 4200×1200 世界生成)无法完成,_ballooncheck.mjs 已备好(大风天自然生成→量精灵宽度 32 vs 256)待负载恢复跑。修复正确性由源码三处实证:Frame(8,1,ai2)/frame.Width=32/PNG 256×76。dist 已重建。
