# XXXX 批（2026-08-19）：UUUU 移交微残终清

## 交付四件
1. **#101 掷流 20196→165353/1663744**（五修）：营地两链帧掷族（SetTile(397,setSelfFrames)五连帧+PlaceWall五连SquareWallFrame+All(data)链 SetFrames 在 OnlyWalls 前）+矿爆点同族三处；GenVars.rockLayer≠Main.rockLayer（TerrainPass.cs:232 num4 独立字段，矿爆 Y 域用错 571→523）；**★Tile.actuator()(0x800)≠Tile.inActive()(0x40)两大旗标**——SolidTile 族读 !inActive() 生成期恒真（无置位点），致动位当 inActive 排除=致动格误判非实心（ST 探针 (2430,920) inact=False wire=True 定罪）；**薄冰斑 AddStructure 非 AddProtected**（CanPlace 不查 _structures），JS 误入保护图挡掉原版放行矿爆点。残 1%=**TrackGenerator.cs:136/151/158 WorldUtils.TileFrame(frameNeighbors) 帧链**（TrackPass 域，'a 3' 苔藓掷）移交。
2. **剑冢 HashSet 豁免撤销**：枚举=槽分配序，Add-only≡插入序；Subtract 后无 Add≡幸存者插入序≡JS Set——ShrineShape 本就逐位等价；全样本流（a/b+**d/n 双盲区通道**）剑段零分叉；"34.5k 剑冢掷"归因证伪（真源=①+矿轨）。
3. **#63 preferSmall 裁决**：spiders 语境**不可达**（IL +005C brfalse +151；+0063=spiders 两格支起点，UUUU"+0063 单格 frameY=54"误读）；残 2 格=波内装饰时序/门读微差（visit 序两侧一致），需 vanilla 分支级 SpiderProbe 收口。
4. **地牢帧归零**：压板 135 样式在 **frameY**（曾 frameX）；Place2xX（cs:39705）style*36 帧（DG_ITEM_STYLE 表接线，1410=style48）；全管线 bad=0。

## 方法论
- Cecil InsertBefore 缓存锚=后插者离锚近（再踩）；ProbeLib.dll 须随织拷入 Resources（漏=MissingMethod 静默空世界）；hs.exe 系 -autocreate 跑前必 rm HOME 下全部 wld（含异名）
- 全样本流 span（d=NextDouble/n=裸 Next）：参数流对齐不保证值层对齐（盲区掷计数差=静默移位）
- 金标 102 出口态自采配方：tttt-app 副本+SW_TT_FR_PASSES="Water Plants"（pass 头=上一 pass 末态）
- rig 槽重放的帧基座=捕获期 JS 边界（slots≤50 不注金标帧）——帧修复验证须走全管线
