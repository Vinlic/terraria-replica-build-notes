# CCCCC：Place2x2 右下锚族（411 矿爆+138 DeadMans 巨石）+ Check2x2 引擎 138/411

接 AAAAA 移交两件，**两件诊断均部分错位，实证重定罪**：
①411 非 findDown 差一行（Searches.cs:60 含起点行 JS 镜像无差）——真根因=
PlaceTile→Place2x2（cs:59766→51352）**cs:51431 x--/y-- 右下锚**写 (x-1..x)×
(y-1..y)+双门（四格空置+逐列地面 nactive&&(SolidTile2||tileTable)，门败**静默
整写放弃**、WireLine/保护图照跑）。JS 曾左上锚无条件写=低一格右一列；金标全图
411 扫描证 vanilla 在 (861,735) 段本就未落（空置门败）——JS 幽灵块才是差，非
"轨道穿杀"。②三格 18,18vs0,0 非 Check2x2 缺派发（其不写帧）——DeadMansChest
巨石 138 同 Place2x2 右下锚，JS 左上锚=整块 (+1,+1) 偏移。修=MicroBiomes
place2x2Direct（含 Main.tileTable 76 id 地面右腿）+FinalCleanup check2x2Sweep
（cs:48405 镜像：锚反解/138 Boulders 支箱豁免+底支撑/411 非巨石逐列地面门/
destroyObject 闸整组杀+尾 4×4 帧）派发 case 138+411（411 必须同补：轨道巷杀
九宫 vanilla 同派发，否则顶行残活+缺 20 尘掷不可收敛）。★frameSparse 跳过表
+138/411：探针嵌合基座帧锚互指死区→与 184 杀级联互喂**无限递归**实爆；生产
帧自洽无碍。★tile-cleanup ⑥ fixture 补石底（浮空巨石派发后 vanilla 同序杀=
fixture 过时非回归）。#101：巨石 284/284 全同位、411 60 格集合+帧全同、.fr
both-314 76/76 零孤、掷流 165546→166921、A/T 19936/21843→8272/9157。遗留：
第二轨对角段 (783,740)→(920,801) golden 独有 JS 整段未落+多站点偏移（6512→
2397 格，TrackPass 域）；#105 持平 ZZZ 基线；mile8 首红 63 原样；54/54+41/41
回归绿。AAAAA"findDown 低一行/轨道穿杀"两说废弃。
