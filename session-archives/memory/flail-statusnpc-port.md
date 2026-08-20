---
name: flail-statusnpc-port
description: 链球 AI_015 全状态机移植+链条贴图+StatusNPC 命中 debuff 表提取接线+noUseGraphic 静态图标修复;武器投射物族审计与 GAP 清单
metadata: 
  node_type: memory
  type: project
  originSessionId: cc0b5a07-65b0-46a9-b141-4257ee7a1554
  modified: 2026-08-13T17:02:00.064Z
---

2026-08-13 阳炎之怒(Sunfury 220→proj 35)专项牵引的武器投射物族大修(对照 Terarria1456):

**已修**:
- channel 电平语义:Input.mouseHeld(不被消费)替代 mouseDown(边沿消费量)——[[input-mousedown-edge-vs-level]]
- FlailProj 新实体:AI_015_Flails 状态机 1:1(0 旋转椭圆 R=37 下压 0.4/1 掷出 17px·t/2 回拉/5 撞墙坠落 0.4 反弹/6 垂地悬荡/4 回收;Projectile.cs:41051),每型号参数表 10 型;替换 YoyoProj flail 近似
- 链条贴图:DrawProj_FlailChains(Main.cs:34752)1:1,型号→ChainN 映射(35→Chain6),逐节光照着色;vanilla-atlas.mjs MISC 补 10 张
- StatusNPC(Projectile.cs:10555)提取器 tools/extract-projstatus.mjs → vanilla-projstatus.json(88 型号/97 条)→ applyProjStatus() 接 WeaponProj/Arrow/WhipProj;35=50% OnFire 300t
- noUseGraphic 族(spear/yoyo/flail/boomerang)排除 useSwing(角色旁静态图标根因)
- GetWeaponCrit=4+武器crit+装备 合并注入四实体(此前写死 4%,Sunfury 应 11%)
- 武器浸剂投射物侧 applyMeleeImbue(近战四族 meleeProj=true)

**Why**: 投射物近战族曾整体按"通用弹"近似,行为/命中/debuff/视觉四层全偏。

**How to apply**: GAP 清单在 game/docs/weapon-proj-audit-2026-08-13.md(AI_003 摩擦/AI_019 长矛/AI_099 悠悠球/Arrow 远程 crit/MinionProj 挂点/Enemy buff 字段缺口等 9 项);探针 scripts/_sunfury-probe.mjs 10 断言。1.4.5.6 投射物 id 重排(Sunfury proj=35 非 181)。

**review 二轮修正**(同类问题四连):
1. 提取器嵌套概率拍平:`if(rand){A}else{B}` 的 else 应 (K-1)/K 非 1/K——285/267/504/163 族全错已修;提取器现按两层门组合+未知形状防御跳过。
2. 链条光照 lightAt 返回 **0..255**(Renderer 同源 /255)——不除即恒满亮静默 no-op。
3. FlailProj 碰撞盒按型号(247/757=34、947/948=20、1058=26)非写死 22。
4. 弹墙计数=每次接触(localAI[0]),>4 只是音尘门——只计 >4 则缓磨墙永不触发卡死逃生。
鞭命中补浸剂(StatusNPC 门含 IsAWhip)。教训:近似值/裸常数一律对源码核量纲与语义,静默 no-op 类 bug 靠"消费侧反查取值范围"抓。

**/goal 全量武器族第三轮**:AI_003 回旋镖重写(无摩擦直线+30t 回收+返回目标速度制+穿墙+AABB 收手);AI_019 长矛重写(伸缩包络 1:1,SPEAR_PARAMS 21 型号,位移=offset×shootSpeed);AI_099 悠悠球重写(三表+双 meleeSpeed 缩放+lerp 逼近+死区+寿命终态锁);**⑩ autoReuse 边沿门时序 bug**(prev 在 updateUse 前赋值=本帧值→边沿恒 false→非 autoReuse 武器全体掷不出,挪到 updateUse 后);五分支补 mouseDown 消费;挥砍/shot/投掷暴击链补武器 crit。探针 _weapons-family-probe.mjs 7 断言。**教训:边沿检测的 prev 快照必须记录在消费之后**;⑩ 门是并行会话引入的——并行会话改动后必须全族回归。

**第四轮(/goal 续)完善**:AI_003 特例族全落地(182/866 追踪×12 目标速度制、106 光碟 45t、301 按 20t/100t 双门+channel、383/320 下垂、Phaseblade 18 型号垂落+40/3 回收)——36 型号全覆盖;aiStyle 161 细剑(AI_161 线性外伸 v×(t-1) 16t,RAPIER_PROJ 10 型号);MinionProj 6 处 StatusNPC 挂点(TigerPounce 本体攻击除外)。tests/weapons-entities.test.ts 10/10(含特例族 6 新测试)。**经验:tests/weapons-entities.test.ts 有 mock GameHooks 基建(makeHooks),实体级行为优先写 vitest 而非 puppeteer**。

**第五轮**:182/866 追踪视线门(canHit 接入);细剑 rotation/Opacity 淡入淡出;Enemy 五系新 DoT 字段(44=8/324=25/323=15/153=15 HP/s+Oiled 六火系翻倍:93728)→21 条 StatusNPC 条目自动生效;**互斥组(mut)语义**:if/else 双分支=单掷骰必中其一,独立双掷会双落空/双中——提取器标 mut id,运行时累积区间判定。proj-status-table.test.ts 5 断言。Daybreak=层数模型(636 计数)仍 GAP。

**第六轮(铜剑变投掷+冰霜引擎)**:**提取器 targetId 根治**——`match(/\d+/)` 抓到 SetDefaultsN 的方法号 N 而非模板号 M,全部委托族继承错基底(3507 继承铁镐 1→autoReuse:true/shootSpeed 缺→spd 默认 8→细剑位移 120px=丢剑观感)。修为取括号内数字,重提 diff 44/2612 全对(2778 旧继承**土墙模板**、3480 珍珠木弓旧缺 shoot/useAlee 静默失效——顺带治好)。冰霜盔甲 46 引擎落地(frostBurn→equipStats→挥砍/近战四族/远程箭三挂点→Frostburn2 5-14s)。教训:**委托/模板类提取一律打印继承链对账**;提取器改动必须 diff 审计+全族回归。探针 _shortsword-probe.mjs。

**第七轮(铜短剑视觉+收尾)**:铜短剑"抛出"第二层根因=**useSwing 门按 kind 一刀切误伤短剑族**(161 族 SetDefaults1(6) 无 noUseGraphic=必须画手持剑 useStyle 13);门细化(spear 仅排 aiStyle 19)+heldUseStyle 161→13 推断+aim。**教训:排除类逻辑必须按原版字段逐族核,不按 kind 一刀切**。剩余 GAP 清:BrokenArmor 20 防/BetsysCurse 40 防穿甲、Daybreak 单层 100HP/s(层数模型 GAP)、链球撞墙音、948 入水变形 947。SUPPORTED 15 项。全量 review:tsc 37 错全在并行会话区、测试 29/29、探针 24 断言全绿。五条教训沉淀见 docs/weapon-proj-audit-2026-08-13.md 第七轮。

**第八轮(铜短剑双贴图,纠正第七轮)**:第七轮"短剑必须画手持剑"是**错的**——noUseGraphic=true 就在 SetDefaults1 case 6 块倒数第二行,此前 awk 输出被 head 截断漏看!修正:swing.noGraphic 标志(useStyle 13 身体手臂姿势保留,物品贴图不画)+Renderer drawUseItem 门+投射物 32×32 原尺寸绘制(碰撞盒 18 解耦)。**教训:读源码块必须打印完整块(到 break/}),head 截断曾两次造成误判(第一次=铜剑数据,这次=视觉)**——判"未设置"类结论前必须 grep 全块。短剑最终视觉=手臂突刺+剑投射物从手心刺出 30px 淡出。

**第九轮(铜镐/铜斧无法挖掘,双根因)**:①剑分支 `tool?.type==='sword' || cwMelee` 没豁免工具——镐斧锤同时 melee=true,cwMelee 命中→挥砍 return→tryMine 永不被调(实锤 tryMineCalls=0);修为 `cwMelee && !tool`。②**HitTile 自创衰减**(每 2 tick 分档 -2/-5/-7/-10,错误归因"原版 Prune 语义")>铜镐 15t 冷却的 +35/击积累,净 +2/击永远凑不满 100;原版 HitTile **无周期衰减**(无 Update 方法,damage 永久保留)——衰减全删仅留 TTL 清条目。修复后 13 击砍树模型吻合。智能光标目标"漂移"=玩家下落期相机跟随的环境现象(站定后稳定,原版同敏感)。探针 _mining-probe.mjs。**教训:自创近似必须标注"非原版"且实测数值闭环;群伤类改 useUse 主链前先想"还有谁共享这条链"。**

**第十轮(巨石陷阱贴图不全/悬空)**:用户 F5 报告像素考古定位——boulder trap 两处(TrapsPass:103 巨石陷阱井 / MicroBiomes actuallyPlaceBoulderTrap)移植 `PlaceTile(cx,cy,138)` 时**只写锚定格一格**,原版按 TileObjectData Style2x2 展开**四格分片帧**(CoordinateHeights{16,18},Tiles_138 36×38 单变体帧 0/18×0/18)——孤格+style 帧引擎拼不出 2×2=渲染只剩 18×18 左上小片悬在井里。修:两处展开四格。探针 _boulder-probe.mjs(103 锚点×4=412 格零缺角)。普通洞穴 boulder 生成本就四格齐全,坏的只有 trap 两处("几个"数量级吻合)。F5 报告 warnings 的 `[VanillaTiler] img=未载` 是懒加载首帧瞬态(素材全在位,非持久问题)。**教训:移植 PlaceTile 类调用必须连带 TileObjectData 展开(fw×fh 分片帧),grep 全仓还有无同类孤格放置是后续项。**

**第十一轮(自动检查四件套,/goal 计划落地)**:A 世界不变量扫描器(src/world/audit/,R1 缺角锚点无关算法+R2 帧重复,豁免表带原版依据,集成=FRAGMENTS 白名单+计数基线——**新类型必红**;负向验收用**注入式**抠格,教训:特定种子的陷阱路径可能不可达,回退 pass 测不出);B atlas-lint(tools/atlas-lint.mjs ATL-01..07+vite 插件 build 阻断,行级正则带 ≥700 基数护栏;**4 处存量错配裁决**:树苗 fh 已修,74/590/93 豁免带依据);C 提取器 --audit(itemcombat pinned 3507/3509 deep equal+anomalies X-04 委托基数;ROOT 相对化;双层=常跑层(不依赖 C# 源)+审计层);D run-probes(--boot-server 5300-5399 私有实例自管,收编 7 探针,_usereach=共享链截胡通用捕手)。**四负向验收全过**(巨石注入/ATL-02 改 cols/3507 还原/剑分支还原)。集成首跑抓 9 类疑点(陶罐/祭坛/雕像/水晶残片=KillTile 整块清未接通二期专项;海燕麦=原版单格写入)。基线:测试 40/40、探针 36 断言全绿。

**第十二轮(Esc 暂停面板像素化+导出存档)**:原版 Esc=IngameOptions.Draw,面板=Utils.DrawInvBG(Inventory_Back13 52×52 九宫角 10px,乘色 (33,15,91)×0.685=XNA Color*float 同乘 RGB 与 A)。UI.ts invBgDataUrl 逐像素乘色+九宫合成 dataURL(模块级 img 预载+onload 回补防首次竞态);按钮=像素字体+黑描边+黄 hover(主菜单同款)。导出存档=flow.doExportSave(saveClient 同链,Blob 下载 `<名>-<日期>.sbw.json`,与 __swFlow.loadJson 闭环;注意 mainFlow 有**两个返回点**:flow return 对象 + __swFlow 桥,都得挂)。l10n 新键必须进根目录 ../tools/l10n-custom/(game/tools 下没有!)再 build-l10n。探针 _pause-export-probe(9 断言,像素采样验乘色 α=175)。

**第十三轮(可靠性四提升,全落地)**:③usereach 扩 6 族(镐/斧/短剑/弓/魔杖/荧光棒,7 断言;木弓已退役未注册→用 vi_3019_hellwing_bow+vi_40_wooden_arrow);④package.json test:audit+prebuild(build 前置 atlas-lint+extract-audit;非 git 仓无法挂 pre-commit——npm 脚本是唯一强制点);②**MultitileFragmentSweep**(FinalCleanup 后,破损可放置多格物体整体清除=原版 KillTile 语义;判定与 R1 同源 findFragments 单一事实源;祭坛/186/187/海燕麦保留)——FRAGMENTS 白名单 9→4 类,被清 5 类转**缺席断言**(清扫回归即红);①双种子默认(9293480,12345)——**抓到扫描器真 bug:maxPerRule=50 截断会在残片>50 时掩掉注入违规**,注入复查改不截断。基线:测试 41/41(含 fullgen-smoke)、8 探针全绿。**教训:run-probes 不带 SW_ORIGIN 会回退共享 5199 被并行会话打死——必须 SW_ORIGIN 或 --boot-server;探针计数器新增项记得在 runUse 里重置。**

**第十四轮(登记项清零)**:R2 悬案裁决——**全 0 帧/混合零帧=渲染扫描路径接管(VanillaTiler:808 连续延伸重建),R2 仅在"全显式非零+重复"时报**(31 处误报修复+仙人掌/织布机 2 真例原则化收口);链球三特例子弹(FlailProj.spawnProj 回调:247 Flairon 20t 自机弹 248 dmg/1.5 kb/2 速 14 距离+CanHit/757 掷出态两过渡气泡 928 vel×0.3×1.3/1058 旋转态 3-6t 轨道刺 405 朝玩家反向(4.5-6.5)±π/4 旋转态 kb×0.5);Enemy 余量 DoT 五系(Bleeding 12HP/s:92598/Hemorrhage 100:92610/骨标 3·触手刺 3·血腥屠夫 4=单层近似,层数模型 GAP 同 Daybreak;137/151/183 非 DoT 裁决不设)。**教训:python 批量注入多锚点时逐一 assert 匹配,静默失败会留下半套代码(tsc 抓重复声明);FlailProj 构造签名(x,y,dmg,kb,projId,channel,target)——测试里参数错位 projId 会静默错族。**

**第十四轮 review(3 真问题)**:①757 气泡**每帧掷**(trans757 在 case 1 顶部无条件缓存=掷出态 60 泡/s;原版仅两过渡点 :41245/:41258)——过渡点才缓存;②1058 节奏数值(原版 num28 默认 4/垂链+悬荡 6/旋转 3-5 :41417-41423,我写成"非旋转一律 6");③spawnProj 回调 sDmg×ps?.dmg **双乘前缀**(FlailProj.damage=cw.damage 已含词缀)。另清掉测试遗留 R2 调试输出。**教训:子机制移植后必须回读自己代码+对源数(本轮三个全是"写了但没回读");回调注入伤害时先问上游是否已乘过。**

**第十七轮(186/187 装饰组残片最终裁决)**:用户 debug-report(不灭的弓太空)实锤——type 186 装饰组 17 格中 11 格残片(两组仅顶行 3 格,底行 y+1 完全不存在;一组底行缺 1 格)。曾以"多带表帧语义"豁免清扫——**那是 R2 帧重复检测的理由(贴图带宽换带),不是 R1 几何缺角的理由**;186/187 放置恒 3×2,缺角=真残片。从 KEEP_KEYS/FRAGMENTS 白名单移除,清扫归零。**全量豁免审计(同日)**:751/752(掘地龟蛋)"单格存储"豁免同样错误——生成端完整 2×2 帧分片,"单格"是渲染跳画(VanillaTiler:860)非存储形态,移除后 12/12 全绿。其余 7 条豁免逐条对 TileObjectData.cs 核实全部合理(314 连接 ID/165/185/233 多 style 变尺寸/74 Height34 植物实为 1×1/590 带宽标记/93 灯笼占格+样式行双轴)。**教训:同一条豁免理由不能跨规则复用;"渲染跳画"≠"单格存储"——R1 看 tile 数据不看绘制。**

**第十五轮(子弹 1:1 全对齐+finalize 时序)**:①247/1058 **去 st!==4 门**(原版 switch(type) 特例段全态运行 :41434+);②弹型分流——248=Arrow grav 0.3(aiStyle1 箭物理,Item17 音 GAP)/928=Arrow bounce 34×34 grav0.3 life250 pierce2(aiStyle14)/405=**新实体 FlaironSpike**(aiStyle 70 全语义:ai0=-10 漂入 10t vel×0.95 α-25→650 寻敌(CanHit)转向 (v×20+dir×Next(35,75)/30)/21→追踪 (v×40+dir×12)/41;撞块前 2 弹第 3 Kill+20 火尘;scale=ai1);③**finalize 在清扫后跑会再造残片**(幽灵 type 净化清掉 flags=0 格)——finalize 后补终扫;④清扫**通用式收口**(清扫全部多格残片仅豁免祭坛/186/187/海燕麦四类)。**第十六轮:地牢门/平台样式修复(用户 debug-report 报告"地牢门是木门/平台是木平台")**——dgPlaceDoorAt 忽略 style 参数帧全不写=全部退化木门;修为 PlaceDoor 1:1(:31938 frameX=54*(style/36)+Next(3)*18, frameY=54*(style%36)+k*18);平台 chTile 不写 frameY=修为 18*tileStyle(DungeonGlobalPlatforms:158,蓝6/绿8/粉7);入口门硬编码13→1/3 themed 门(DungeonGlobalDoors:47-54)。**教训:接收参数的函数要 grep 它是否真的被用(style 收了没写帧=静默退化);"入哈希"/"不入哈希"注释不等于帧已写。**


## 覆盖审计终扫（2026-08-19"火焰弹射上去该燃烧吗"）

全实体文件机械扫(命中循环/固定 projId∩表):唯一漏网=**TrapShot 飞镖类**
(Dart.ts:427 陷阱弹命中环无 applyProjStatus)——毒飞镖 98(Poison 600t 掷中必染
:11041)/超级镖 184(900t :11045)永不染毒,已补 `if (trapProjId !== undefined)
applyProjStatus(...)`(矛 186/尖球 185/巨石 99/喷泉 654 表内无条目天然空掷)。
其余全绿:Arrow(弓/枪/镖/魔法通用弹全走它,projId=弹药 shoot——火矢 41→弹 2
33% OnFire 180t 早接)/WeaponProj(近战四族+日耀喷发 611)/MissileProj(火箭)/
WhipProj/MinionProj/暗影焰弓 495(ShadowFlame 153,走 Arrow)。★projId 归属:
投射物型号=【弹药的 shoot】非物品 id(火矢物品 41 弹 2;毒镖物品 283 弹 283)。
SolarEruptionWhip 611 手写 applyDaybreak(300t)与表值一致(层数模型专道)。
projStatus.TABLE 已 export(测试锚);探针 _projstatus-probe(3 断言:表驱动
掷骰/毒镖/实体链 Arrow 直击染火)——**探针放箭须贴敌 24px 内**(远距箭会先撞
地形死,测的是命中链不是弹道)。
