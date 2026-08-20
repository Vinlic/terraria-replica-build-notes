---
name: loot-new-passes
description: AddBuriedChest 四深度分支战利品 1:1 + 雕像/丛林神龛/洞穴小屋/海洋洞窟/地狱熔炉五 pass 移植要点与行号
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-11T05:15:20.835Z
---

2026-08-11 完成"全部有货"物资对齐轮(对照 Terarria1456):

**战利品(BuriedChestsPass.ts 重写)**:`rollChestLoot` 按深度四分支(cs:36283/36563/36789/37163)——地表(仅 wooden/sky 旗标门禁)/金(ws+25..rockLevel)/洞穴(rockLevel..h-250)/地狱(h-250+)。要点:
- 地狱箱主件 = 每世界乱序 [274,220,112,218,3019] 顺序轮换(cs:11262,状态在 gs.hellChestItems/hellChestIdx);**5010 宝藏磁铁是地狱箱 1/5 附加物不是主件**(旧表错把它当主件、漏了 220 狱炎鞭)
- 冰箱主件 Next(6) [670,724,950,1319,987,1579] + 1/20→997 + 1/50→669(鱼);门禁 gy≥ws+25
- 金/洞穴默认主件 [49,50,53,54,5011,975]+1/20 提炼机/信号枪;洞穴 1/20(岩浆线下)906 熔岩符
- 965=绳、279=飞刀、40=木箭、42=手里剑、28=弱效治疗、2350=回城药水、8=火把(ItemID 实证)
- 锭按 gs.oreTiers 替代档位:锡703/铅704/钨705/铂706;钨银时地狱银弹换 4915
- 旗标池:ice(974 冰火把/3199 冰镜/5120)、desert(4423 圣甲虫炸弹)、ivy(3360+3361 法杖对/2204 蜂蜜机)、water(4425/4460)、sky(5629/4429/5528)、hell(5010/4443/4737/4551)
- 天空箱:SurfaceChests pass 墙 244 → style 12(旧版强制 style0)
- opts.loot 兼容 number|string(vi_ 反解 id;HiveSpiderPass 传字符串)

**新增 pass(均按原版注册序接进 vanillaBiomes)**:
- StatuesPass:statueList 73 项精确序(cs:4395,[34]=(349,0),[43]=(105,50),追加 63-66,68-73,75,51-62,77,78,67,74,37,2);count=floor(73*2*w/4200);陷阱雕像=**列表索引**{4,7,10,18}(索引=样式因<34)→ 飞镖陷阱137+红石线 L 形
- JungleShrinePass:jungleHut 每世界五选一[119,120,158,175,45]→墙[23,24,42,45,10];地牢异侧半区+tile60 门禁+排除 225/229/226/119/120 与墙86/87;神龛中心记录→JungleChestsPass 放 style10 常春藤箱(主件序 nextJungleItem:211/212/213/964 循环+1/50海草753/1/15竿2292/1/20花靴3017)
- CaveHousePass:35-40×面积;FindRoom 15-30×8-12(左右±25/上±10 扫描);主题评分 wood=tile0+1/jungle=59+60×10/mushroom=59+70×10/ice=147+161/desert=397+396+53/granite=368/marble=367;ChestChance 全 1.0;沙漠 Bast≤2+提炼机、丛林磨刀站 2-4;门=外侧 3×3 空区凿壁
- OceanCavesPass:地牢侧海洋 1/3;蠕虫半径17-25→4 衰减(过 beachDistance-50 后 ×0.96/步);大半径段记录宝藏点(单槽覆盖→末次位)→style17 箱 loot NextFromList[863,186,277,187,4404]
- HellforgesPass:w/200,墙 13/14 门禁,向下扫 PlaceTile 77(接在地狱箱 pass 后)
- legacy structurePass(木屋+散箱空箱)已被并行会话删除;tiles.ts v_119_iridescent_brick 已补(def+白名单已有),stable-id place_v_119=10493

回归:tests/gen-loot-passes.test.ts(空箱≤1=神庙豁免、平均≥3件、雕像≥60、熔炉≥5、神龛砖/小屋墙密度、地狱主件≥3种、陶罐地表门禁)。宝箱 items 数组可>10(存档/UI 均按 length 动态)。

**第二轮修复(用户指出地表陶罐+简化项不许兜底)**:
- 陶罐地表泛滥根因:potPass 门禁误用 worldSurfaceLow(谷底线)——原版 cs:18216 是 `y < Main.worldSurface(平均线)` 时锚点须有墙;补 oceanDepths 排除(y≤(ws+rockLevel)/2+40 且海滩列)。原版门禁只查锚点**左列单格**,右半罐/上半格露头的"墙龛罐"是原版合法形态(测试断言按锚点左列逐格等价)
- CaveHousePass 全量补齐(不再简化):楼梯=CreateStairsList 对角平台链+斜坡(slope 数据)+顶步 4×1 平台;支撑梁=CreateSupportBeamList(步长 6→4 整除,梁落下一房顶/实心,顶上非平台);门=FindSideExit(Up 搜索+AreaOr(4,3) 任一非实心,双侧);平台出口=FindVerticalExit(Left+AreaOr(3,5));FillRooms=画/烛台交替(switch(i+parity%2) 仅 i∈{0,1} 落内容,i≥2 落空是原版语义)+装饰循环(小堆185/骨堆186/雕像含陷阱/家具七选:桌(沙漠 tile469 Tables2 style7)/铁砧/工作台/织布机v_86/钢琴/酒桶94/书架,主题样式全表)+画表 RandHousePicture/Desert(cs:35286/35336:240 十八选/245 九选/246 八选,沙漠 240/245/242);AgeRoom 七主题蚀变(Dither+Blotches 相干噪声):木=蛛网51 2×2×W*H/16 次+墙侵蚀(地下清墙/地表墙2)、冰=321→161→(0.8)→147+冰钟乳石165(fx=var*18,fy 0/18 大/72 小,PlaceTight 冰名单{147,161,163,164,200})+墙40、丛=158→60→59+藤蔓62(长3..H)+墙64、蘑菇=190→70+发光菇71+清墙、花岗岩/大理石→368/367+墙180/178(钟乳石名单外 no-op 是原版语义)、沙漠=396→(0.8,团簇0.2,0.5)→397+OnlyWalls(187)→墙216;宝箱=PlaceChests 四级联(底行随机10→底行扫描→顶行同两轮→±30 千次)
- StatuesPass 导出 STATUE_LIST/STATUES_WITH_TRAPS/placeStatueTrap 供小屋 FillRooms 复用;烛台原版 +54 点亮帧本引擎不建模(def 恒点亮)

