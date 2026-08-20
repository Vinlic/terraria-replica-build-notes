---
name: impl-gap-scan-2026-08-13
description: 全量功能缺口扫描6059件→真缺口40件清单在docs;4子代理发车(导弹族/食人鱼/回旋镖/液体工具);扫描器_impl-gap-scan.mjs
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T15:42:05.904Z
---

2026-08-13 全量功能实装扫描(用户要"明确列表+全面补齐"):

**扫描器** scripts/_impl-gap-scan.mjs(经 run-diag;新武器登记后续查)。方法论坑:
- 全量登记在 **vanilla.json .items**(items.ts :946 运行时合成 `'vi_'+id+key`,正则扫不到!)显式 item({}) 仅 952
- "已实装"信号三层:家族派发(combatWeapon 同构)/src 代码树 vi_ 字面(**必须排除 src/data——recipes/drops 表是可获得性≠功能实现**)/数字信号(VI_ID(N)+`mvid === N`+**逗号清单 Set**(PERMANENT_USE_VIDS :383)+def 标志派发(paintTool/wireTool)——单一信号必漏
- 6059 = 实装 2332/材料 3656/候选 71 → 甄别后真缺口 ~40

**清单落盘 docs/implementation-gap-list-2026-08-13.md**:液体工具 6(无底桶/吸收绵)/墙物品 14(**wallitems 表仅 124 条,提取漏=放置静默无效根因**)/放置块 tile 回填 5(vanilla.json createTile 有值 itemfunc 无)/乐器 2/趣味 5/发色剂 3/爆炸扩展 2/杂项 8(海盗地图/单色扳手族等)。行为 GAP 11 条(G1-G11)含可控导弹族/食人鱼/回旋镖/长矛/悠悠球/StatusNPC 复杂块/FlailProj 细节/MagicProj 无贴图/笼子渲染/敌弹 w×h 归一。

**4 子代理已发车**(并行会话纪律:Game.ts 单挂点+Edit前重读+不碰 worldgen):A=可控导弹族 aiStyle 9/20/28+老星怒65(MissileProj.ts)/B=食人鱼 AI_039 咬住/C=AI_003 回旋镖 1:1/D=液体工具 6 件。剩余 GAP(长矛/悠悠球/StatusNPC/FlailProj 细节)待下一波。

**验收/进展(2026-08-13 晚)**:
- C 回旋镖完成验收 ✓:两条要害发现亲自复核坐实(**106 光碟 45t 门=死代码**,链尾 30 门先截胡 :36794 vs :37082;**301 双门按 AI 次计数**,extraUpdates=2 :3651);weapons-entities 24/24;WeaponProj 重写;_weapons-family-probe.mjs 保留作三族回归工具(报告称已删,实际保留=记录偏差)
- **§3 放置块回填 5 件已销核**(items.ts BLOCK_TILE_BACKFILL 表+tests/block-tile-backfill.test.ts)。**坑:ITEM_BY_KEY 是 key→索引表非 def 表**(测试首版栽此)
- **W2-3 MagicProj 贴图化+笼子 验收✓**:G9=MagicProj projId 尾参+PROJ_ROT_RIGHT 旋转+帧切片(测试7/7探针8/8);主会话接线两处=netSnapProj **MagicProj 分支必须插在 projId!==undefined 门前**(否则 kind1 劫持→访客 Boomerang 重建,else-if 顺序是命门,首插插反了自纠)+spawn 第8参 shoot。G10=笼子已被并行会话实装(93 tile/33族状态机/测试49绿),代理只核验未重复造,**1.4.5.6 鱼缸无液体叠层**(水烘进贴图,勿凭旧印象造)
- 第二波 W2-1(长矛+悠悠球)/W2-2(墙链)在途;A/B/D 大文件已落仍在收尾
- **W2-1 长矛+悠悠球销核✓**:前提纠偏——GAP#2/#3"现状"已被前批重写,实为终审抓 6 真偏差(**矛绘制翻转条件写反最重**:`direction>0→FlipH+num−=π/2` Main.cs:34659,左刺曾指下 90°;**2.355f 非公式是字面量**;悠悠球旋转 0.45;射程=型号常量表+string 修正**与 shootSpeed 无关**;矛命中盒型号表 14 型失真)。自造公式双溯源:reach=包络 offset×shootSpeed(:43417)/range=YoyosMaximumRange 表。weapons-entities 34 绿/7 套 66 绿。教训:**给代理的任务描述先核对现状是否已被前批改掉**
- **W2-2 墙链销核✓**:提取器重写全写法覆盖(共享 case 算式/if 区间/DefaultToPlaceableWall/嵌套 switch/goto),wallitems 124→**292 一一双射**幂等,parity 测试 7/7(独立向上归因交叉验证),消费点纯数据零接线。**反纠我清单 8 假阳性**(2=泥土块/29=生命水晶/206·207=桶/215=坐垫/1124=tileWand/1905=圣诞树顶/2262=块)——**我扫描器名字列有错位**(names 正则取串偏移),id 为准
- **§8 电路工具族销核✓(主会话)**:items.ts 电路工具段是**空壳注释**——Game.ts 三处守卫(派发/显线/R键)全等 wireTool 表,整族(509/850/851/3612/510/849/3620/3625/3611)曾为**死路径**(手持扳手零效果)。补 WIRE_TOOL_TABLE 9 件+测试。教训:**注释规划段≠已实装**,扫描器 vi_/数字信号都探不到"只差数据表"的半成品
- **W3-1 StatusNPC+debuff 销核✓**:提取器+5 形状(ai1==i 定向 tag/setHuntressT2 门/remix 局部变量/ai 三元),表 98→110 型号 SKIP 13→3;16 字段全行号锚(lifeRegen=2×HP/s);**顺手修两真 bug**:Oiled"翻倍"系误读=**六火系单块 flat−50**(:92728,已亲核)/Slimed 补齐六系;189 单层近似+636 已入表;huntressT2 套装链贯通(SUMMON_SET→equipStats→MinionProj ctx);27 新断言+回归 144 绿
- **W3-2 FlailProj 销核✓**:前提再纠偏(特殊弹型 247/757/1058/948 已被并行会话落地,转逐字对账)——修:ChangeDir 七态(消费 player.facing,旋转锚改用其结果)/757 迟 1t 当场生成/247·1058 专属旋转式+淡入/**FlaironSpike α 方向写反**(出生全显越漂越透)/scale=ai1 误改命中盒/撞墙位移回卷+dig 单响;**case 3 死状态考古**(1456 无 ai[0]=3 入口——"飞行中再按"系旧实现自造);heldProj 手臂向=引擎级登记。948→947 原文 :41064 亲核。weapons-entities 42/42。**教训同 W2-1:任务描述先核现状**
- **W3-3 敌弹画法销核✓**:自绘 9 款失真修复——**683 原版 alpha=255 根本不绘制**(:7003 亲核,旧实现 640px² 幻影)/961 Frame(1,5) 6.25×+旋转错(:31004 亲核)/962 Frame(3,4) 网格错/456 胶片条/965 漏镜像/813 2.25×;TownShot 29 型改 TOWN_DRAW_SPEC 规格表(10 旋转档全锚/9 源帧切片/scale 接通);75 断言+回归 171 绿;_enemy-proj-draw-audit.mjs 留档。lunar-final-audit 539 概率断言=既有 flake 非新引入
- **B 食人鱼销核✓(stall 唤醒后收尾)**:Arrow opts.piranha 扩展(非新实体);AI 39 全锚——咬住 16 速逼近/清速咬定/目标死 3000 视线转咬/直飞无追踪离主>700 返回/同主<8px 排斥/补弹 3−在场;**与 PROJ_ROT_RIGHT 协同要点:咬住清速后 atan2(0,0) 会把鱼掰回正右 → AI 侧维护 pRot/pFlip,draw 按 piranha 分流(:403/:437)**——凡"速度清零的姿态类弹"都要 AI 侧记录朝向,勿靠现算 atan2。8/8 绿
- **A 导弹族销核✓(stall 唤醒后收尾)**:MissileProj 新实体,21/21 绿。**任务前提双纠偏(第三次代理纠正我的清单)**:①aiStyle 范围 {9,20,28}→**只 9**(20=手持钻头 :23837/28=风动物理,误挂会错);②族成员勘误(579=Drax/753=海龟宠物/1262=叶绿手钻,**真族=16/34/79 全 aiStyle 9**——派发键应是弹的 aiStyle 不是猜的集合)。老星怒 65 独立 melee 分支(Bottom.Y≥线 与 503 的 Center.Y>线 不同);vi_495 彩虹魔杖未注册=数据缺口。**G 系十一条全部销核,仅 D 液体工具收尾中**
- **D 液体工具销核✓(战役收官)**:无底桶倒 255 不消耗/海绵与空桶共用舀取体;**第 4 次前提纠正**:海绵无饱和变体永不消耗(:45738 原文亲核)/微光桶无额外交互;**顺带修旧桶链三偏差**(3031/3032 液体门+补 mouseDown/useTime/射程门+useTime 数据驱动)。19/19 绿
- **X2 发色剂销核✓(goal 批)**:**第 5 次前提纠正——原版无发色剂装备槽**!hairDye 是 Player byte 字段使用即赋值(:42179 原文亲核,1990 去除剂=hairDye 0 在 >=0 门内),随 .plr 存档;全族=12 染料+1 去除剂(非 3 件)。提取器 12 条 BindShader 序锚+11 款 legacy CPU 公式 1:1;渲染拆发层(后发→本体→前发→头甲,skipHair 绕纸娃娃缓存);存档往返。21 测试+探针 10/10。**顺手修并行会话隐身重构漏前发层(发色剂玩家会变秃)**。vi_495 实为批量注册已生效(A 误报)
- **goal 批(E2E 欠账清)**:武器族探针 7/7+MagicProj 8/8 真机坐实(私有 5210 已清理;leashedEnv 崩溃已随并行会话收敛消失)
- **X5 heldProj 销核✓(goal 批)**:**第 6 次前提纠正,证伪缺口本身**——链枷/悠悠球/长矛/鞭四族 noUseGraphic=true(:3321)→ 原版根本不画持物不转臂(:3192 门亲核),恒定姿势是原版行为;"手臂指向缺口"是两轮登记的误读(W3-2 与悠悠球侧登记已就地纠偏)。**唯一可见消费族=食人鱼枪 1156→190**(无 noUseGraphic,AI_Adjust :26313 调用)——AI_Adjust 公式逐字移植(:21161-21191 含 minSpeed 门/flip)+帧内账本+Renderer 三单点+合成 swing(渲染侧等价 SetDummyItemTime(5));18 测试+探针 9/9(err=0)+回归 162 绿。真结构性缺口登记:SelectedDrawnProjectile drawLayer=7 前臂前分层(纸娃娃无该插槽,不硬造)
- **X1 乐器+趣味销核✓(goal 批)**:竖琴音高量化 1:1(:45905 亲核)+Sfx pitch 通道(2^pitch);鼓槌须站鼓组 tile 486 十档音色;**5464=放置物非玩具(第 7 次前提纠正,consumable=false 不消耗,:43085 亲核,顺带修 4460 沙堡桶误耗)**;1345 彩带=纯材料定案。**引擎级三补:GorePiece.fixedUpdate 全仓从未接线=死亡碎块恒冻结+600 槽泄漏(真隐藏 bug!)/气泡 gore 族 411-430 AI/Sfx 无音高**。26 测试+回归 131+探针 23/23(5213 已清)
- **X4 引擎三小项销核✓(goal 批)**:①491 飞刀=MissileProj 内 FlyingKnifeProj(挂在 aiStyle9 族文件;**探针抓到第一版分流放近战块=死代码**——3030 是 melee+noMelee 归 kind shot,vanillaItemCombat:218)4:1 收敛/近距自锁锯齿/松手回收/穿透 10t;②189 层数模型=636 最小实装(DaybreakFlare 附着登记 daybreakStacks+Enemy DoT 100×max(1,层);上限 8 淘汰最老;探针实测叠层 1→2);③_liqtoolsprobe 11/11(封闭腔砌墙+**新根因:205 舀取 220ms 内舀起→倒回原格,改 80ms 短按**)。144/144+探针 7/7 三连稳
- **X3 销核✓(goal 批收官)**:湿/干/土制弹族整族(共享 case 算式提取漏=死路径,EXTRACT_PATCH 回填;载荷 BFS plot 门不穿墙);**第 8 次前提纠正:海盗地图 1456 无夜间门**(:63863 亲核,只查进行中+hp≥200——"夜间使用"系误传);5644=观战系统(引擎登记,无目标支 1:1);5334=Mechdusa(双门 remix&&getGoodWorld,本仓 getfixedboi 不置 remix→everything 兜底登记);1905=新 XmasTree.ts(16px 紧排修 2px 漂移+**顺手修 repairIndexFrames ×18 毁圣诞树双约定 uint16 溢出**);X3 遗留开口(引信嘶声表成员)由主会话亲核关闭({903-906,910,911} ⊂ :183,FUSE_SOUND_PROJ 补六型)
- **★GOAL 终局:15 代理全闭环,认证批 15 文件 303/303 绿**——行为 GAP 11/11+功能缺口 §1-§8 全部销核(§7 含整族);8 次前提被纠;引擎级真缺口仅存:观战镜头系统(5644)/mechQueen 联动 AI(5334)/投射物前臂前分层(drawLayer=7)/MP hairDye msg4/死敌 189 散播——全部登记在 docs/implementation-gap-list-2026-08-13.md
- **总结教训:给代理的任务清单四次被纠前提**(W2-1 长矛悠悠球/W3-2 FlailProj/A 导弹族/D 液体工具)——旧 GAP 登记册的"现状/范围"会过时,代理必须被授权"先回源核现状再定范围";stall 代理用 SendMessage 定向唤醒收尾比重发任务高效
- 环境告警:并行会话热改中 Game.leashedEnv 崩(Game.ts:7653),E2E 探针受阻属预期

**假阳性教训**:Boss 召唤物走 else 分支链(557/560 无字面);蜂蜜桶 1128 在 swap 链 :9606;笼子 7 件在 items.ts 表(放置✓渲染 GAP)。
