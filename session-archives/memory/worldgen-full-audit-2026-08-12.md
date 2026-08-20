---
name: worldgen-full-audit-2026-08-12
description: 世界生成105 pass全量审计:21严重四类缺口模式/RNG流错位为主/CaveWalls等缺失pass补齐/金标oracle双绿至underworld
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-13T04:25:25.221Z
---

2026-08-12 世界生成全量审计(用户标注「悬空宝石」「神庙木椅」触发,选定全量 105 pass 逐行深查)。

**四类缺口模式**(21 严重的归类,新增/移植时逐类自查):
1. **RNG 流错位**(13/21):漏抄方法尾部无条件掷骰(**Reset 尾 3 掷 cs:8211-8213——terrain-oracle/caves-oracle 同漏=金标自洽假阳性,转译类审计必须质疑金标本身**)、掷序对调(Jungle/Shimmer/LifeCrystals)、条件掷写无条件(Cleanup)、上限错(Gems 拒采 64→3)、循环条件含掷骰需逐次求值(Pyramid cs:28078)、Reset 掷过的值重掷(JungleShrine hutIdx)、flag 声明在循环外(OceanCaves)
2. **id 空间混淆**:原版 tile id 直传内部表(Tunnels 53→沙漠化石/ DirtWallBg 147→熔岩滴/ Pots 367↔368)——[[id-space-collision-pot-bug]] 同族
3. **配对错位**:type↔style 旋转一位(TemplePass :34608-34630 原版 18→10/14→9/15→12;Dungeon ftype3/10/11)
4. **整段缺失**:CaveWalls(17819,悬空宝石根因=洞穴零背景墙)/CaveWallVariety(16786)/Piles 五子段/TileCleanup/Dungeon 头部 SetupDungeonData 掷骰/水下箱 treasure 段

**已落地**:Phase1(CaveWalls+CaveWallVariety 1:1 新增+GemCaves 归位 Moss 前+家具六连修,`tests/cavewalls.test.ts` 五组结构断言)+B1/B2 修复 15 条+B3 修复代理 25 条(8 严重全 RNG 类)+oracle 同步再生成(**terrain 双种子位级全绿,caves 链 27 段全绿至 underworld**;corruption 段分歧=另一会话在途区,转储 /tmp/js-crdump.txt;其 oracle 硬编码 380 而原版 oceanDepths 用随机 beachDistance 300-340 可能是分歧点)。

**How to apply:**
- 总账与遗留批清单:`game/docs/worldgen/pass-audit-2026-08.md`(2026-08-13 ABC+D 批全落地;**第十节=全仓复审**:id 空间/渲染帧表/运行时子系统三线审计 80+ findings,修复批全落地;含测试基线可信度表与横切模式)
- **全仓复审高价值发现**(防再犯):TILE_NO_FAIL 内部/sheet 口径错位(58 方块秒挖)/金币雨 item id+1(×100 通胀)/修剪草 477+492 刷怪门/SceneMetrics lavaLine≡h-200(勿用 GenVars.lavaLine)/大师宠物掉率提取器类字段盲区(重建 JSON 前先看 tools/extract-npcdrops.mjs 的 fields 表)/rng.int(0,N) 闭区间坑持续复发/remixWorld 专属条款勿无条件应用/【蜂蜜同样溺水:Collision.cs 只排 lava/shimmer,勿回退】
- 金标工作流:改 JS 链必须镜像 `tools/golden/caves-oracle.cs` 同步改,`dotnet run` 再生(dotnet 10 文件脚本直跑);全管线终态门 `UPDATE_GOLDEN=1`;**world-final-hash 是自洽变更探测器非正确性证明,oracle 逻辑半边是手抄(共同误读→双绿),唯一真值=golden/wld 真机(L2 硬断言是根治路径)**
- 深查方法论:并行只读审查代理(逐行对照 1456,RNG 掷数/顺序/常量/分支/写格语义五维)→ findings 精确到行 → 修复代理「先实读原文再改,核实不通跳过」→ 结构断言回归;**审计 finding 本身也要被核实**(三处勘误:石巨人实为蜂后/Devourer 3/4 非 4/5/239 是血爬虫)
- 修复代理并行约定:同文件互斥(Game.ts/Player.ts/WorldGen.ts 热点错峰)、每代理独立单测、编辑前重读盘上最新(并发会话)
- Chair 竖排音高 40 非 38;OuterOutline origin 差 1 行是原版原文;SlowlyDies 集=草本树苗族(TileID.cs:249)


**2026-08-13 遗留批收官(全备案项对齐)**:
- 快修 7:hurt() 负防御增伤(克眼 P2 专家)/灯笼夜 SetEventFlagCleared 首杀门(全体 Boss)/毁灭者 81 段/史莱姆 LUT(60=丛林草非泥/161=冰非雪砖/spawnDist 绿紫门)/SceneMetrics 扫描窗 -62..+61/城镇盒 1200(非 1080)/fround(0.35)
- 五代理:绿洲下游消费段(逐格扫描,勘误"每片掷骰"猜测)/刷怪余项 10 修 4 核(蘑菇支行号勘误 :3540 非 :4726)/肉山墙身平铺(45-47 条/帧=原版条数,肌腱链+舌头+gore)/A2 lows(BirthdayParty 已接/陨石双链路确认/luck 测试 5σ 重写)/**祭坛勘误:原版两处放置——cs:14241 逐组版在 Corruption pass 内(我方现状正确)+ cs:15825 全图撒坛独立 pass(此前整体缺失,已新建)**
- 蜂蜜蜜蜂测试重写:原版暖机 num3 无下界钳(前 60t 负加速飞离,120t 后追击)——测试断言改锁原版语义
- 终验:金标三门 8/8+全量 1539 过(剩 4=1 真修 3 负载抖动单独全绿)

**2026-08-13 清零批(全部解决,不留遗留或近似)**:getGoodWorld 30+ 分支(EoC 11/WoF+Hoplite/BoC×3/双子×9/摧毁者/Golem×4/邪教徒/蜂后;**清单三勘误:WoF 之眼无 g 分支·1456 无 jewelBeetleChance·lunar_misc 是十周年**)/管线结构尾 18 调用拆槽+DirtRockWallRunnerPass(:15536)+SpawnPoint 提槽/EoW 渲染 behindTiles 层+专家缩放+BGM 类别表+淡入(探针 20/20)/特性六件(绑缚三人组 105/106/685——**附带真修 setPlayerFlags downedSkeletron 无置位点→双键 downed_35**·setFireFlyChance·石碑重生 delay 86400 随存档·獾帽·派对蛋糕·仙女 583/584/585 非台账的 501-503)/快修(wofDrawArea getter 消近似·WallOfFlesh.png 白名单·growPalmTree -20 终态去重·v_484 核实正确)。
- **终验时序教训**:金标 11:28 再生→并行会话 11:46 改 MicroBiomes/Traps→world-final-hash 转红=**门按设计抓到别人在途编辑,溯源看 gen 文件 mtime 晚于 golden mtime 即定性,勿 UPDATE_GOLDEN 盖章**。
- 备案(结构性非错位):King Slime g 分支=速度基线单位未建模无代码可移植/685 绑缚渲染复用 679 帧表(Renderer 禁改)/453 出生脚底 +1 嵌格未动。**并行会话债务归并行会话**:knockbackResist 两测试红/RandomText 12:01 重构留 kind:'default' 失配/上述 world-final-hash 红。