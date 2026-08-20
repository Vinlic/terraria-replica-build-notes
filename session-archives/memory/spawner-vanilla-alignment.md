---
name: spawner-vanilla-alignment
description: 刷怪系统 1:1 对齐大修（2026-08-11 多代理审查）——已修清单、生成端照妖镜案例、诊断法、数据缺口
metadata: 
  node_type: memory
  type: project
  originSessionId: 372ae608-2da7-4502-87f6-cedcc2af7bb7
  modified: 2026-08-11T08:13:41.023Z
---

VanillaSpawner.ts 已全链 1:1 对齐（2026-08-11，多代理对照 Terarria1456 NPC.Spawner）：

- **选点链**：PostCheck 整帧放弃（NPC.cs:922，失败不换点）；地牢门墙取 y-1（GetProperGround :5792）；六族 Zone 全走玩家 169×123 窗口计数（SceneMetrics 阈值 evil/blood 300、hallow 125、jungle 140、snow 1500、mushroom 100，含互减与向日葵-10）；联机屏检遍历全部玩家（`VanillaSpawner.remotePlayers` 静态注入，Game.trySpawnEnemy 赋值）；isOcean 沙族集 {53,112,116,234}+x 阈值 van 缩放。
- **段链补齐**：skyMob 段(链首,hard 唯一 1/10 飞龙87)、海洋+水池完整门链(渔夫376/水面线双扫描/鲨鱼/水黾/琵琶鱼102/食人鱼58/绿水母103)、神圣 tiles 段、地狱补全(税务官534/LavaBait 653-655/Red Devil 156/151)、ZoneMeteor、尾段 hallow138/137+glowshroom+hard 池+冰 tile 判定、地表昼夜细分(僵尸 style 表/小变体同帧双出/萤火虫/血月)、地下 hard、cavernMonsterType 消费。NET_ID_MAP 僵尸变体基底 3→190-194（旧表全错）。
- **浮空岛**：原版全域 [0.1w,0.9w] 仅避中央 ±150（WorldGen.cs:13017），重掷带宽扩 ±max(150,0.05w) 与 skyMob 中央带重合；skyMob 判定改"露天高空"（兼容存量中央岛）。勿改回两侧带（那是误修）。

**Why:** spawner 修对后会**照出 gen 缺陷**：地牢腔面曾不铺砖（PostCheck 踩砖率≈0→地牢不刷怪，已被并行开发修复+裂砖随主题 41→481/43→482/44→483）；地狱曾涂 wall 1（房屋墙门全拒→地狱恒不刷，hellPass 已删该行，实测灰烬面 886/1500 出怪熔岩蝙蝠/恶魔/骨蛇/LavaBait）。
**How to apply:** 刷怪异常先分层计数定位（monkey-patch findSpawnTile/checkNotSpawningOnScreen/setFlagsForChosenTile），勿先疑 spawner——语义已对齐原版。dungeon-spawn 测试的 max≤15 断言（clamp 顺序）与 4000 次采样是原版语义勿改回；[[multiplayer-room-system]] 房主权威下 spawner 只在房主端跑。

**generateWorld 跨进程非逐位确定**（液体沉降按墙钟 yield）——逐格 hash 探针只能同进程比。

**数据缺口已补齐（2026-08-11 H1）**：473-476 BigMimic 四色/590-591 火把僵尸/594 WindyBalloon/628 蒲公英/629 IceMimic/631 RockGolem/634-635 孢子族/692 Orca(虎鲸非Sharkron)。根因=extract-npcs.mjs 读 1405+MAX_ID 586 与 `||` 离散集解析缺陷——**补新 NPC 先修提取脚本再看数据**。661/hardDungeon 门已接 `flags['downed_262']`（Game 击杀通用置位链 downed_{vanillaId}，Boss 死亡自动置位勿重复接线）。

**微光已落地（H2）**：LiquidSim 补 active 位（泄流真根因：幽灵 type 被当实心）+shimmerCheck(type4↔水/岩浆/蜜→659 Aetherium，非黑曜石)+shimmerRemoveWater；渲染 water_14 真贴图 0.75 透明度；GrowTreeWithSettings 1:1 宝石树。775→749 稳定（26 格差=原版一致行为）。

**仍缺（依赖大基建，单独立项）**：事件系统段（星璇四塔/雪月/南瓜月/日食/Gem Squirrel/Bunny——需月相事件状态机+波次入侵调度）；590/591 火把照明 AI；微光 sparkle/glitter 视效与瀑布分支；宝石树砍伐掉宝石/树苗生长；caves-checkpoint golden 分歧（既有遗留）。


## 雪原出怪专项核查（2026-08-13，用户报"冰川区没怪"）
三层验证全绿：钉格池（夜 161 冰冻僵尸 83%/昼 147 冰史莱姆 100%/地下冰 147）、真实世界全链 e2e（161×833+147×302 主导，ZoneSnow=true）、live 浏览器两轮（spawnCalls→161/147 实际入场+手动 200 roll 147×51/161×24）。**结论：雪原出怪链无缺陷**。用户体感空旷的可能因：昼间雪原原版只出基础史莱姆（速率低）、怪刷在屏外 40+ 格缓行。坑：直调 spawnAnNPC 诊断须手工设 dayTime（字段默认 true，昼池假象）+ setFlagsForChosenTile（surfaceSpawn 假会掉进地下 147 池）。回归测试 tests/snow-spawn.test.ts。