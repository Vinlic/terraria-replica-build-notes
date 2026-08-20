---
name: info-accs-review-fixes
description: 信息饰品系统终审——7真问题修复(暗行/渔情粘性反转/小动物空id/速度帧序/节流16帧/灰显/字段归属)
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T09:09:43.068Z
---

2026-08-13 信息饰品(DrawInfoAccs)实现 review,回源逐条核对 Main.cs:46142-46710 后修 7 处:

1. **暗行 bug**:原版 `i > num2 && i < num2+2` 只暗悬停行**下一行**、无悬停恒不暗;旧实现 `i>=hoveredRow&&i<hoveredRow+2` 无悬停恒暗第 0 行
2. **渔情粘性反转**(最重):原版=浮标在场(含飞行)只读缓存、**无浮标**才现算刷缓存(:46296-46316);旧实现反了(浮标在液才刷→首竿后冻结)。修法=新增 `Game.playerFishingConditions()`(GetFishingConditions :41528 1:1:手持竿优先否则全包最高/饵=弹药位54-57先扫/松露虫2673提前返回/Tipsy5+漂浮5/乘区)
3. **小动物 rarity 恒空**:`critters.map(vanillaId:null)` 写死→金色生物永不上 Rare 行;改读 `def.npc`
4. **速度窗口滞后一帧**:原版右移→入[0]→再求和(含本帧);平局取先见者非最近
5. **节流 15→16 帧**:counter=15 递减到 0 才重扫;扫描按 gates 门禁(原版在行分支内)
6. **"附近无X"灰显**:原版整行 Color(100,100,100)→row.grayed+#646464
7. **字段归属教训**(用户质疑"未消费≠可删,可能是漏移植"):回源确认 accThirdEyeNumber/accCritterGuideNumber 全部消费点=DrawInfoAccs 自身→Number 恢复为计数载体;CritterGuideNumber 存的是 npc[] 槽位索引(本仓无此数组不可移植),产出名已由 Text 等效;**补漏 Player.cs:12625** `if(!accThirdEye) accThirdEyeCounter=0` 卸装重置(CritterGuide 无此重置=原版不对称)

附带:dontCountMe 全表仅 10 id(8/9/11/12/14/15/40/41/88/89,NPC.cs SetDefaults);flag2-flag12 在 1456 已死代码恒 false;IsItStorming=_shouldUseStormMusic(:2978)字面等价。

**二轮(用户追问四偏差)后落地三项**:
- 沙尘暴文字闪烁(:46247-46251):驱动=GlobalTimeWrappedHourly=**真实墙钟秒**%3600(Main.cs:16777 TotalGameTime),`%10>=5` 亮 5s 灭 5s;ctx.weather.globalTimeSec=performance.now()/1000
- 金色生物行染色(:46661-46672):OurFavoriteColor=rgb(255,231,69)(Main.cs:868);GOLD_CRITTERS 14 id{442-448,539,592,593,601,605,613,627}(Terraria.ID/NPCID.cs:4450);缓存加 accCritterGuideVid,行 gold 标记
- ignoreWater 门(:46484):整块液体修正 `!merman&&!ignoreWater`(水上行走鞋族+buff15);另水分支 `!trident`=手持三叉戟 277 免水中减速(Player.cs:12488)——经典彩蛋,勿漏

**accWatchTime 勘误**:初登记"床冻结 GAP"是错的——该字段 1456 全源码**零赋值点**(仅声明:2446+消费:46185),死字段/API 残留,`!=0` 恒 false → 原版手表恒显 Main.time,现行为已 1:1,无需移植。

**剩余登记偏差**(不修):装备页图标竖排(:46691+)、hover 滴答声 DoStatefulTickSound、byte 回绕、金色行描边×0.1 细节(保留黑描边)。

**方法论**:移除原版字段前必须 grep 全反编译确认消费点全集;"未消费"大概率=消费没移植完,不是字段多余;登记 GAP 前必须回源确认机制(猜测=错误,accWatchTime 即教训)。回归红 13 项全归并行会话(DungeonPass.ts 编辑中途截断致 7 文件传递炸;[[vanilla-worldgen-port-status]] parity 会话 WIP)。
