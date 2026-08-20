# 墙家族横扫 L 批（#46/#47/#67 + pass49 转岩浆接线）

- **#46 Temple 四根因全修**（掷 99,452→107,888/原版107,941；四通道 28k/15.5k/19k→1.3k/1k/153）：①房间链方向三元反了（`Next(2)==0→-1`，JS 曾 `<0.5?1:-1` 颠倒=整链镜像）；②末房 dest 循环 4 掷/迭代（基础2+覆写2，JS 只掷覆写）；③祭坛 Place3x2 中心锚坐标系（占位 [i-1..i+1]×[j-1..j]、锚定行 j+1；tileSolid[237]=false 前导门恒过）；④active(false) 家族保留幽灵 type（清 0 造 ~12k RAW typ 差）。残余 -53 掷在木刺段。
- **#47 Hives 已修四件**（掷 1.65M→1.48M/原版1.03M）：①FrameOutAllHiveContents 整段缺失（每墙86格 1×Next(0,3)，每巢数千掷）主根因；②CreateStandForLarva 托台须 pass47 现场搭（BeeLarva pass 只是幂等重建+放231）；③隧道 honey(true) 恒置+wall244 双门+幽灵保留；④canPlaceStructure 缺 GeneralPlacementTiles 扫门（已定位未接：StructureMap.CanPlace 除矩形交叠还扫矩形内 active 格 type∈黑名单{225,41,481,43,482,44,483,226,203,112,25,70,151,21,31,696,467,12,665,639,138,664,711-716}即拒）。残余 +448k：隧道 t#0-12 逐位全等，t#13 段源 (3058,519)vs(3698,890) 悖论未解（单隧道步幅≤45 但段源差147；需 CreateHiveTunnel 出口探针）。
- **#67 Cave_Walls**：countTiles 曾用栈BFS+全格seen——原版递归DFS序(x-1→x+1→y-1→y+1)+CountedTiles 只登记非实心格（实心格重复访问、类型计数器重复累加、shroom>rock*0.75 门依赖）。重写后 wal 40,840→39,679，掷差+3,913 未动（残因待 pass 闭包逐迭代探针）。
- **#39/#41 无自因**（隔离掷数精确+四通道0）：管线债=上游 28/32 墙债经 Next(2) 短路门/wall==2 触发带级联。
- **pass49 转岩浆接线**：World 新字段 genWaterLine/genDungeonExempt（TerrainPass gs.waterLine；豁免盒=outer 半图矩形 [左5%-45%/右55%-95%]×[ws+10,UL-10]，wallDungeon{7,8,9,94-99}）；settle.ts gen 模式接线（load 不设=原版置 maxTilesY 豁免）；原版 pass49 首行 QuickWater(3) 才触发（SettleWaterAt 只被 QuickWater 调）。
- **方法论沉淀**：①隔离重放 gs 克隆会被 pass 自身污染（自加保护矩形挡自己=假分歧）——每重放独立 cloneGs；②共享 /tmp/sw-num4 会被并行会话覆盖部署——IL 注入探针必须复制独立 app（/tmp/sw-tm/app）；③探针三件套=流哈希定标（N 精确）+调用序列对拍+STRUCTS 倾倒（StructureMap 内部表反射）；④逐掷值模拟（fresh(seed)+K draws 后任意 Next(a,b) 值）定三元/分支方向类 bug 立竿见影；⑤"IL 与反编译与JS三方静态一致仍分叉"时必是求值序/坐标系/漏段，别再静态对拍，直接上探针。
- rig 边界：[046] new→1,302/1,015/153/0；[055] 墙债 144,890→113,923（余=#28 40.9k 另案+#32 55.9k 禁改+#47 残余）；[056] newWal 99,173→91,957。
- 工具：tools/_walliso.test.ts（五pass隔离重放）、_tcal.test.ts（SW_HASHES 批量FNV定标）、_tdraws.test.ts（流位掷值模拟）；TempleProbe.cs（Entry/Path/Hive/Tunnel/Mark/STRUCTS）。
