# 大理石 slab77 终局:CheckStalactite 击杀类型门

biome2 slab78@(990,917) van48/js63 根因:原版击杀带类型门(cs:39146/39193
`tile[x,num].type == tile[x,j].type` 才 KillTile),JS 曾无条件双杀 num/num+1 →
PlaceSlab 覆写钟乳石对偶格(165→367)时把刚放的大理石抹掉 → SmoothSlope mask
分叉 → PlaceTight 门掷差。修复=两 pair 分支加 `st.type[a]===st.type[i0]` 门
(bisect 实证仅此项即定胜负);附带 killStalactiteTile 级联改列主序(cs:80924)、
frame165 inactive 清 half/slope(cs:82082)。**反例**:ResetToType 不清墙——
Tile.cs `wall` 是独立 ushort 字段非 bTileHeader,`wall=pWall?178:0` 改法立即
打坏 biome1。效果:8/8 biome 逐 slab 掷数全等、双种子 Marble 掷数精确+四数组
0 差、管线 [021]-[027] new=0。方法:TraceRNG 栈帏 callsite(tools/_d25slab.test.ts)
+`__swSlabProbe` 快照钩子+rolltrace MX 按 biome 对拍(biome 边界=marblePlace:168)。
world-final 金标已过期待政策性再生;oracle 165 生命周期同步清单第 9 条。
