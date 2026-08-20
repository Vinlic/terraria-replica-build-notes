# NNNN：oracle Dome 入口体镜像 + MMMM 四修同步（2026-08-19）

- **任务**：JS dgDomeEntrance（FFFF+MMMM 终态）→ caves-oracle.cs dungeonE+ 段 C# 转录；oracle 对 entKind==1 不再走 Legacy 近似。
- **谱系勘误**：1511931452 实测 **Tower**（A=1/B=0），非 HHHH 所记 Dome——其 40/78 回落真因=MMMM 四修改 Tower/Dome 共用下游段而 oracle 未同步。Dome 实证种子=**12345**（A=0/B=2/kind=1）。
- **oracle 十件**：inAct 通道（=JS wire bit5，不入四通道）+DgPillarStrip inact 参（清位→平滑→后置）+DgSolid/SolidOrSloped !inAct+JGS+灯笼/吊灯/桌面锚 nactive+statues 两门（MMMM③）；DgDungeonPot !inAct（MMMM①）；书链 `!Nowb && Next(50)`（MMMM②）；DgEntNoFeat 三门（MMMM④）；DgDomeEntrance 全量+dispatch（FFFF）；树族四件上移顶层（GrowTreeT ignoreWalls 参）。
- **结果**：_oraclesync 双种子 **71/78**（seed2 40→71，首红 dungeonP 消除；红=dirtlayer/rocklayer+IIII/OOOO/PPPP 尾段漂移带 piles..microbiomes 5 名，oracle 侧零改动）；12345 dungeonE 网格**逐位零差**（曾 `i+n3+21` 笔误→右楔柱镜像位 +42，网格差图定罪）；Legacy 种子 oracle 输出改前后逐字节全等；检查点数保持 75。
- **C# 顶层程序三陷阱**：局部函数可先调用后声明，但捕获变量须在**调用点**前赋值（CS0165——晚 pass 的表对早 pass 不可见，表+函数整体上移）；块内局部函数块外不可见（GrowTreeT 须上移）；上移与兄弟块同名冲突 CS0136（改名 SetTSG）。
- **方法论**：JS↔oracle 网格差分=JS `.typ` 是内部 id 须 TILE_DEFS 映射 sheet、oracle `DPD_DUMP .act` 是 '0'/'1' 文本非二进制；入口谱系用 `DG_ENT_DBG=1` 一跑定谳。
