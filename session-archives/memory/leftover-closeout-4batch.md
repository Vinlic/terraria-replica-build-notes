---
name: leftover-closeout-4batch
description: 遗留收口四路批:召唤落位统一SpawnOnPlayer/红帽骷髅王真链(坐沙发非马桶)/EoW头部精确门/弹540星尘标记AI_103+402BFS孵化链/迅猛龙54表五档/冰面无输入腿行0/棉花糖IsFood帧2/QuickHeal虚空袋bank4
metadata:
  type: project
---

遗留收口批（2026-08-18，用户"继续推进遗留"）。三代理+主会话修 1 个 tsc 残留。src 全域零错、149/149 回归。

**Game 六件**：①物品召唤落位统一迁 `findOffscreenSpawnPoint`（500 次屏外寻点=SpawnOnPlayer 1:1；**史王无专属落位**——NPC.cs:81505 是"静默公告"组非落位分支；双子 126 随 125 位近似）；②自然出王补 HasAwoken（NewNPC Type==50 :81564 恒播覆盖 SpawnBoss 静默——BOSS_SPAWN_SILENT 表口径差登记）；③QuickHeal/Mana/Buff 虚空袋 bank4（猪猪罐/保险箱不参与）；④红帽骷髅王真链勘误：**夜间坐长凳 89 style43（frameX∈[2322,2358]）+ killClothier + 裁缝在场可击 → SpawnSkeletron(redHat) 于裁缝中心**（PlayerSittingHelper:84-95→NPC.cs:81193-81218，任务描述"马桶 1/40"不实）；⑤EoW/BoC 召唤门改头精确 [13]/[266]（身段存活可再召头=原版双刷语义）；⑥水蛭 117 出生尘改 spawnBurst 定向（opts 无 vx/vy 字段——tsc 坑）。

**弹 540 星尘标记**（StardustMarkProj.ts 新建）：AI_103（:32272-32299）ai0 出场延迟=世代×10、静默→淡入 11t 孵化 NewNPC(localAI[0])→淡出 250 kill；**弹体恒静止**（UpdatePosition :19028 早退）；BFS 世代链（NPC.cs:44230-44314）：根深 Next(3,6)、分叉预算 Next(0,4)、角度奇偶π+(0.5−r)π/4+dir·π/4、距离 100+50r、**仅最后标记回填孵化类型**；塔变体（:44149）参数已备待迁。绘制 lighter+α3×、Extra_47 落点束（ai0∈[10,20]）。

**渲染四件**：迅猛龙 faceAcc 登记引擎级（全仓无 face 装备槽系统——PlayerDrawLayers.cs:2801 偏移表已抄进注释）；**迅猛龙 54 表五档补齐**（ApplyItemPositionOffsetFromMount :50638 只管 54 非狼 52！风筝 IsAKite 25 件(4,−4)/悠悠球 21 件按身体行(10,−10)/(8,0)/(2,2)/**3542=星云烈焰非天空龙杖**(−10,0)/(10,0)/useStyle5(4,0)/default 按行；狼表 :1785 本就 1:1 无缺）；冰面滑行无输入腿钉行 0（**条件=slippy∪slippy2∪windPushed∪滚轴鞋且 !controlLR**——非 wet；:35818-35826）；棉花糖 IsFood 手持取竖 3 帧条第 2 行 Frame(1,3,0,1)、968=32×10 整图直画（GetItemDrawFrame:41896≡GetDrawHitbox:49192）。

**教训**：faceAcc/头盔 addon 族在 PlayerDrawLayers 不在 Player.cs；"马桶红帽骷髅"是讹传（真链=坐沙发）；ItemCheck_UseBossSpawners 全族走 SpawnOnPlayer 无逐 Boss 落位特例。

**E 批（2026-08-19，goal 驱动）**：①deerclops 冻结根因=漏位置积分（另见 deerclops-port）。②老鼠坐骑 55 爬墙落地（ratClimbVy 字段钉速+dropThrough 平台穿透，tests/rat-mount-climb 5 绿）。③FlexibleTileWand 全族 30 件（碎块魔杖 5324/5329/5330+MiteyTitey 5464+便携窑 5481+沙堡桶+侏儒+火烈鸟+珊瑚贝星+南瓜灯+礼物+书 149+暴露宝石六色）——表从源码机械提取（★桶按【弹药】合、option 各带 tile：large 154=647×7+648×3；`default(int)`=0；ByRow rows×per 摊平；1291→702 属 Medium 非 Large！），runtime=src/world/FlexibleTileWands.ts（单件族弹药=本体无背包门；cycleOffset 模容量负同余）+Game.tryPlace 头部分支+↑↓ 边沿循环（flexWandCycle）。A 级余：高尔夫车3611/虚空袋/涂层/公告盒编辑/成就页UI/坐骑槽UI/builderAcc 开关/gravDir/RerollVariation。

**E 批续**：④RerollVariation 全链（TOWN_PET_VARIANTS 637/638/656 各 6 名逐字；roll=rand(6)；sheet 解析宠物前置分支——637/638/656 本无 TOWN_NPC_PROFILE 档（未收录注释），root 由 vid 映射 Cat/Dog/Bunny；18 张具名变体贴图 public/sprites/vanilla/{Cat,Dog,Bunny}_*.png 已在；variationIndex=-1=Default 图）。许可证二用 1:1（≤100 掷环+newNpcName+满血+PetExchange 粒子+成败公告）。A 级余 7：高尔夫车3611/虚空袋/涂层/公告盒编辑/成就页UI/坐骑槽UI/builderAcc 开关/gravDir。
