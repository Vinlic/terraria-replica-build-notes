---
name: meteor-fall-port
description: 陨石坠落事件 2026-08-13 1:1 移植终态:触发/消费/五层crater/流星雨/天幕流星;双会话并行时的分工与坑
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-13T00:51:17.302Z
---

陨石坠落事件(WorldGen.dropMeteor/meteor + Main.HandleMeteorFall)2026-08-13 完成 1:1。**双会话并行**:骨架(触发链/搜索/五层/公告)由并行会话铺,我方做逐行审计并补了 7 处偏差。

**全链语义**(锚点):
- 触发:①EoW(13/14/15)/克脑(266)击杀 `(!downedBoss2 || rand(2)==0)` 置 spawnMeteor(Game.ts boss 记账段,NPC.cs:80241-80259);②入夜 `rand(50)==0 && downedBoss2`(Main.cs:64713,**灯笼夜不压制**——roll 在 stopEvents 之前,曾误加 !lanternsUp 门已修)。spawnMeteor 存 world.flags 随档走(WorldFile :1301/:2098)。
- 消费:phase time>16200(夜=午夜后/昼=上午9点后,白天杀 EoW 当天落是原版行为);天幕流星 15000-16200 窗口恰一颗(SkyRenderer.spawnSkyMeteor,Background_Meteor.png 62×384=4帧,1x4 SpriteFrame,FramingSpeed 5,LifeTime 1200,rotation=vel 角+π/2;_skyMeteorShown 位入夜重置)。
- 搜索(MeteorFall.ts dropMeteor):上限 400×(w/4200) 地表以上陨石计数;X∈[150,w-150) 避出生点±8%w;自 groundLevel×0.3 下扫首个 tileSolid&&!platform;30×30 打分(实心+1/云族{189,196,460,717-719,202}-100/**else** 分支液体-1——实心格上液体不双计);阈值 600 每命中列-0.5 下限 100;保护命中整列作废换 X 不衰减。
- crater 五层:①R17-23 **非实心→失活(挖空)而非置 37**(原版 :6394-6401,曾直接 setTile(37) 生成空中浮矿已修)+ClearSlope ②R8-14 底部掏空 ③R25-35 GetsDestroyedForMeteors(TileID.cs:165:树5/荆棘32,352/宝石树583-589/596,616,634)清除+清液体+**孤立陨石四邻无实心→挖**(:6436-6445) ④R23-32 1/10 散布 ⑤R30-38 1/20 散布。保护表:BasicChest{21,467}+tileDungeon{41,43,44,**677**}(677 是 Main.cs:7944 第四成员,曾漏已补)+{26,226,470,475,488,597};玩家保护=中心 ±(1022,639)px(NPC.sWidth 1920/sHeight 1200+safeRange 62/39)。
- 流星雨(StartMeteorShower :6189):失败&&1/3 → 计数 **[650,751)×4 持续整夜**(WorldFile :1069/:177 持久化,SaveMeta.meteorShowerCount),每 tick 1/4 掷一颗 **Projectile 1078 伤害碎块**(MeteorChunk.ts:重力 0.3、50/专家40/大师35 伤、kb 5、命中玩家 OnFire(24) 300-600t、撞地无掉落)——审计修正:曾为一次性 8× FallingStar burst 且落地掉 vi_75(免费星农场,偏离原版灾害语义)。出生:随机 x[100,w-50)×16/y<5%h×16,1/2 改玩家±2400px clamp;晷快进清零。
- crater 后标脏:chunks.markDirtyArea(±40)+**lighting.dirty=true**(曾漏→夜落陨石黑块)。

**坑**:
- 陨石事件与夜间坠星(FallingStar,弹幕 12 落地掉 vi_75)是两套东西,勿混。
- 双会话并行同文件:Game.ts/MeteorFall.ts 被对方实时改写——patch 前必须重读锚点,python 断言失败=文件漂移,换 grep 定位再插。caves-checkpoint 若新分歧先查对方未提交 worldgen 改动(2026-08-13 深夜 terrain 分歧=对方在途编辑,与陨石无关)。
- 相关 [[recipe-engine-port]](同样双会话并行模式)、[[blockframes-lookup-rebuild]]
