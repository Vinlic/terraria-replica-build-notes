---
name: round6-review-fixes
description: 2026-08-09 全阶段 review(4 代理对照反编译源码)+ 偏差修复清单与遗留项
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-09T16:01:13.274Z
---

# 2026-08-09 全阶段代码 review + 修复(round 6)

4 个对照代理审查了全部 pass 与物品功能,确认偏差后逐条核验反编译源码再修。
关联:[[vanilla-worldgen-port-status]] [[vanilla-worldgen-passes]]

## 已修复(生成端)
- **TileRunner**:Main.tileStone 实为宝石 63-68/130/131/566(9 id);CanBeClearedDuringGeneration
  = 11 种不可清集合(TileID.cs:702);flag3 case 补 45 金砖/460 雪云、删粘土、沙上禁铺粘土;
  granite/marble 伴生墙 180/178(0.3R);阶梯补 900 档;**尾部全局速度抖动+±1 钳制**(cs L46659-46673);
  初始速度离散化 Next(-10,11)*0.1;L1/mudWall 抖动离散化 0.015/0.01
- **Spread**:补岩浆邻接检查(恒不转)+ NOT_CLEARABLE 检查
- **Corruption**:minCenter=500/中央200/地牢100/midFixer=50 全为固定常数;zLo<400;
  sideways 初速 vy 恒负;CrimStart 补 X 回中/隧道终点囊群(50 球 40-54)/列填充;
  入口囊群抖动 0.005、rise 离散;祭坛 y 带 worldSurface-widen/2..+100+widen
- **Dungeon**:边界三分带方向反转(0.5-0.75w→+1,0.25-0.5w→-1,推向外侧);
  竖井出口探测偏移(dxS1*0.6+dxS2 朝中心)、土丘 TileRunner;外壳刷墙;
  vy=-2 嵌套概率(1/27);门 1:1 重写(候选=房左右墙+水平走廊端点,±10 列择优扫描+门柱)
- **Temple**:整体重写 1:1——房间链重投至不相交(死循环修复)、行程 1-2 递增、中心锚点、
  全房对实心砖连线、双遍游走挖腔、templePather、outerTempled 封壳、入口隧道固定高度/间隔、
  门框五段、templeCleaner、祭坛 237;宝箱=房数×1.1
- **Hive**:隧道步数净 -2/迭代、三阈值独立抖动且基于基础半径、±10 墙87/地表截断、
  无速度钳制;扇形隧道链(每段从段起点);蜂蜜坠落块;75% 丛林验证+草≥2
- **Desert**:蜂巢重写 1:1——椭圆散点→深度2 DFS 簇→AttemptClaim 合并→**簇场强前二大**
  (修复单块近似);化石=获胜簇索引%15(确定性);隧道/外缘注岩浆;AddTileVariance 酥化
- **Cleanup**:第二遍不清蜂巢墙 86;邻列只清 2/40;沙例外 53/112/234(二遍仅 53);
  列范围 3..w-4 与 w-5..5;clump 扫描 [10,w-10)
- **Caves**:Small Holes 补位置避让(340);Caverer 数量=5×floor(w/4200)(整除截断)、
  起点 x∈[340,w-341]、y 上界 h-401;Dirt Caves 中部条件闭区间
- **Beach**:waterStart 上界开(Next(220,260))
- **HellFort**:整体重写 1:1——列左右界数组(宽 8-20)、翼走法、中央列跨度、
  列合法性(地狱层已有墙弃列)、四边实心/内部墙、列间门/层间平台/左右外门/顶层口、
  恶魔火把独立 pass(200×w/4200)
- **IslandHouse**:地板=实心上一格(无兜底)、外壳全填(仅顶行两角跳过)、
  内腔仅原墙0处、窗宽 halfW>10→±2、桌椅/横幅位置 1:1、天空宝箱战利品序(气球/星怒/马蹄铁)
- **Mushroom**:maxBiomes 50(原 13)、地下沙漠检查、尾端 x 抖动 int(-20,19)、落点无界重掷

## 已修复(功能端)
- Game:1×1 v_ 图块挖掘掉落回退 place_v_*;药草收割 style=/18(原 /36 bug)
- Player:绳索攀爬 1:1(上爬 -0.2/tick 至 -3 后 -0.02 下限 -8;下滑镜像;静止 ×0.7)
- items:木弓 4/30/6.1/0;火花法杖=ItemID 3069(14 伤/魔力2/UseTime26/射速7;暴击10 未做——缺 crit 基建)
- 水蜡烛:spawnRate×0.75(间隔×4/3)+ maxSpawns×1.5(NPC.cs:43241)
- 营火 0.5HP/s(每2秒1HP);心灯(灯笼 tile42 frameY 324-358)=1HP/s 独立判定
- Boss:EoW头 150/22/2/38×38;克脑 def14/kb0.5;EoC 100×110;史莱姆王 98×92
- Enemy.fromVanilla 补 def.boss(VANILLA_BOSS_IDS 集合)
- SaveFile:header 写入 treeTops
- talkToNearbyNpc 收紧为命中盒±8px(原 2 格半径会抢附近方块右键)

## 验证(安静窗口通过)
tsc ✓;确定性 ✓;三尺寸 5.4s/13.5s/24.8s(结构算法增重);roundtrip 0;
内容快照正常(temple 71k 砖=原版实心团块特征);feat-test/2/4/9/8b 绿。
feat-test4 补 NPC 隔离+飞镖早采样(撞墙即消失的竞态)。

## 2026-08-09 追加:地牢塔下行通道被封死(用户报告)
**根因**(插桩证实):legacy 盲爬的出口探测点在入口外厅未来位置(X±(dxS1*0.6+dxS2)≈50-66 格,
朝地图中心),落在高坡时楼梯被迫爬过整座山才触发;期间每次调用的外壳(±10-17)把上一次
挖空(±3-6.5)埋掉 + 水平漂移 → 120 格高、200+ 列宽的实心砖瘤(12618 空中砖),塔建在瘤顶。
**修复 = 1456 方案**(DungeonCrawler.cs L280-326/400-449):
1. 入口位置预计算:锚点±300 拒绝采样,从 y=10 下扫首个"有内容"格,校验无云块(±15 方框+
   上方 50 带)与头顶余量(ny-80>0,Legacy RoughHeight=40);成功则锚点迁移 ±25
2. 爬升改 Precalculated:沿直线分段(10-29 步/段)走向入口,剩余耗尽即达,确定性终止
3. 上限 100(1405 无上限会挂死);失败才回退 legacy 盲爬
4. num8/delay 语义修正(到 0 后保持,每轮 1/5 分支);外壳 X 无抖动(原版仅 Y 有)
验证:3 种子塔内厅存在+BFS(门可通行)全部连通到 ws+150 以下;确定性 ✓ roundtrip 0。
1456 dungeon 为 DungeonCrawler 全新架构(Entrances/Halls/LayoutProviders),legacy 塔=
LegacyDungeonEntrance.cs(与 1405 DungeonEnt 同源);探测公式 1405=1456 完全一致。

## 2026-08-09 追加:地牢陈设管线(用户报告"地牢内空空如也")
原 placeFurniture 是每房 8 次尝试的简化(工作台/桌/椅/蜡烛+75% 金箱)。已按 1405
L18441-19613 全量移植 placeFurnishing,顺序:
1. 墙变体(5轮×3,WallDungeon BFS 扩散,7→94/95、9→96/97、8→98/99)
2. 房口平台(dPlatforms 候选=房顶/底首个开口列;行±5 找两侧皆砖窄口,frameY 108/144/126)
3. 特殊上锁箱×5:style23-27+467(style13),战利品 piranha_gun/scourge|vampire_knives/
   rainbow_gun/frost_hydra/desert_tiger(ChestData.locked=true,Game 金钥匙开)
4. 书架平台(样式9-12 三选不重复,w/20 次)+ 书(1/50 frameX90)/蜡烛/水蜡烛
5. 房间金箱:战利品序 muramasa/cobalt_shield/aqua_scepter/blue_moon/magic_missile/
   valor/golden_key(浅于ws+50强制)/handgun
6. 灯具(w/150):吊灯(1/7,style27-29,下方15格净空)/灯笼(style0-6三选)+墙上开关136
   (±12/+3-20 嵌砖位,LOS)+红线布线(st.wire|=WIRE_RED 曼哈顿路径,2/3 关态帧18)
7. 飞镖陷阱(w/500,简化:无布线;原版 placeTrap 四类)
8. 地面家具 13 类(2000×w/4200 次):桌+椅+摆件/工作台+椅/雕像/烛台/椅/床/钢琴/梳妆台/
   长凳/浴缸/灯/烛台2/落地钟;变体墙(94-105)只允许桌/工作台/椅;优先炼金台/施法台各1+w/4200
9. 墙饰(420000/w):两次重定心+跨度判定 横向(>3×且>21)/纵向,主墙=randPicture(240样式
   12-19,23/242样式0-16,30)否则 randBone(240样式16,17/241样式0-8);nearPicture/2 距离检查
10. 旗帜(840000/w):向上找顶,4格净空,style 10-15(变体墙 12/14)
辅助:placeFurn(bottom/top 锚+flip 镜像帧)、flipFurn、placeWallArt、addChest(下扫地面)。
验证:双种子内容统计正常(旗帜~460/平台~760/书~200/墙饰~500/陷阱~80/灯具+294格布线/
锁定箱5+战利品箱12),确定性 ✓ roundtrip 0。
注意:VanillaSpawner.ts 有用户进行中的 vanillaScale/tint 类型错误(非本任务);
feat 测试脚本的 input/select/button 选择器需适配新 vui 主菜单(进行中)。

## 2026-08-09 追加:贴图帧方向审计(用户报告生命水晶上下颠倒)
**规则**:原版多格物顶行 frameY=0、向下递增(AddLifeCrystal cs:16023-16038 为基准)。
发现的同类问题与修复:
1. **生命水晶**(StructuresPass):生成端把 frameY=0 写给底行 → 上下颠倒。已按原版改回
2. **天空房家具**(IslandHousePass):桌 3×2/椅 1×2/旗 1×3 全是**单格残件**,且步长错
   (桌/旗用 *36,应 *54/*18);已改 placeFurn 完整多格放置(桌 style7 步长54、椅 style10
   左椅翻转、旗 style7-9 顶锚 3 格)
3. **剑冢**(SwordShrinePass):单格残件 + *36 步长;假剑应用 **tile186**(不是187 style15);
   placeFurn 净空/支撑校验致常年放不上(原版 PlaceTile force=true)→ 改强制覆盖 3×2 居中
   (底行锚 sy-12);真=187 style17、假=186 style15,均步长54
4. **地牢旗帜**:每格独立重摇 style → 一条旗混样式;改整条同 style
5. placeFurn 增加 support 参数(无锚装饰物跳过底座校验)
审计脚本结论:心 200 例顶行全 0 ✓、天空房桌10/椅44/旗155 全完整 0 残件 ✓、
地牢家具帧全对 ✓、剑 4 种子全有 ✓;确定性 ✓ roundtrip 0。
已核对无误的:祭坛 place3x2、暗影球、神庙祭坛 237、各宝箱(顶 0/底 18)、
Game tryPlace(dy*18 顶锚)、dev 展示区((h-1-dy)*18 底锚)、门 placeDoorClosed(竖排布局)。

## 2026-08-09 追加:宝箱样式修正 + 散布宝箱 pass(用户报告"很多同款木箱")
**关键事实**(PlaceChestDirect cs:34112 证实 + 贴图表采样验证):宝箱样式横排
frameX=36*style(不是竖排!与门相反)。样式表:0木 1金 2金(地牢) 3影(item328) 4地狱
11冰 12蛛网 13Skyware 16蜥蜴 17水 23-27锁金;tile467=群系箱(10=沙/丛林,13=desert tiger)
**修复的样式错误**:天空房 0→13(Skyware)、神庙 0→16(+每箱能量电池1293)、
金字塔 0→1(+战利品 857沙暴瓶/848法老面具/934飞毯)
**补齐缺失 pass**(BuriedChestsPass.ts,接在金字塔后):
- Buried Chests(cs L7907):洞穴 35-40 + 地狱 7-10;AddBuriedChest(-1) 语义:y≥ws+25→金1,
  冰系tile→11+冰战利品,地下沙漠→467:10+沙漠战利品(深/浅分层),y>h-205→地狱4+地狱武器序
  (dark_lance/flower_of_fire/flamelash/hellwing/treasure_magnet)
- Surface Chests(cs L8019):w*0.005 个地表木箱(泥墙2/59/244 处)
- Water Chests(cs L8058):9×w/4200 个水中箱17+战利品(鲨鱼饵/水上漂靴/芦笛/游泳圈/三叉戟/脚蹼)
- 验证:木34/金31/冰3/Skyware3/蜥蜴10/水8/锁金4/沙6,114箱50箱带专属战利品;det ✓ rt 0
**遗留**:普通金/木箱的杂项战利品大表(cs L21500+)未移植;Jungle Chests(丛林神龛 ivy10)缺
丛林神龛结构未做;Water Chests 的海洋洞穴部分(oceanCaveTreasure)未做。

## 2026-08-09 追加:怪物"穿墙"排查(用户报告噬魂怪穿墙)
**验证方法**:密闭竞技场(fromVanilla 直接生成 ai1/2/3/5/14 七种)+ 自然生成 90 秒监控
(身体≥2 行实心或中心行全实心才计)。结果:碰撞核(moveAndCollide 8px 步进)完全正常,
零真穿墙;早期嫌疑均为"站半砖"单行重叠误报。
**实修一处**:VanillaSpawner.spawnNPC 用 fromVanilla 的中心锚(y-h/2)把怪埋进落脚实心格
半格高(NPC.cs:46596 NewNPC 实为底锚 Y-height)→ 飞行怪沿地面内沿漂移、视觉=穿墙/钻地。
已改 e.y = y - e.h。Game.trySpawnEnemy 普通分支本就有规范落位(底锚+HasTileSpawnSpace
双格净空),水生/蠕虫/小动物分支锚点也正确。
**若用户在导入 wld 地图上看到穿墙**:优先怀疑导入端把某些墙体 tile 降级成非实心
(compat 报告 tilesDegraded),需具体位置+怪物种类+墙型再查。

## 遗留(未修,按影响排序)
- DungeonHalls 选向机制(四向扫描+lastDungeonHall 抑制)未移植,50% 硬币近似
- MarbleGranite 仍为大幅简化(slab 网格/岩浆压力模拟未移植)
- 腐化冰 163/200、沙岩 400/401 转换缺 tile;ChasmRunner 魔矿 22 用黑檀石近似
- 神庙尖刺陷阱 232 段未放;蜂巢 Webs And Honey 钟乳石未做
- 蜘蛛巢:洪泛蔓延条件放宽(wall 1/2)、装饰缺失;洪泛下限 100(原 500-3500)
- CloudIsland 阶段 2/4/7(雨云团/修补/顶部云团)与湖岛 CloudLake 缺失
- 金字塔仍是地表阶梯简化(原版为沙丘下埋式)
- Jungle generateHolesInMudWalls 用自写随机走近似 MudWallRunner
- 物品 crit 字段(火花法杖暴击 10%)缺伤害基建
- 种子应种 sprout(v_82)而非成熟态 v_83
- 桶:舀取需 3×3 合计>100、放置需 liquid<200(现任意/仅空格)

## 环境
- vite 在用户并行编辑时全量重载,测试须等安静窗口(30-60s)再跑
- Terarria1405 目录偶发 ENOENT(瞬态),命令加重试循环
- 用户同期在做:placeDoorClosed 门放置统一、wire 电路系统(items wireTool/SaveFile.wire/Door clearDoorAt)
