---
name: altar-fragment-fix
description: 恶魔祭坛 2 格残片根因=裂隙挖空漏三重门+裂隙尾祭坛自加吸附;1:1 修复(CanEvilReplace/魔矿猩红矿保护/去吸附)
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T08:33:01.731Z
---

2026-08-12 用户报腐化区祭坛只剩左上 2 格(帧 (0,0)+(18,0))浮空。地图解码扫描实锤:5 祭坛簇 1 残片(其余完整 3×2)。生成链路:腐化祭坛**全部**来自 ChasmRunner 尾部(腐化分支不调散布 placeAltars——那只属猩红),place3x2 自身先查净空后整体落 6 格不会残缺。

**根因双重(对照 WorldGen.cs ChasmRunner :76066-76240)**:
1. **挖空门漏三重**:原版 :76187-91/:75414 = `CanEvilReplace(k,l) && type!=31(球) && type!=22(魔矿) && type!=204(猩红矿)`——我们只判 `!=ORB`。CanEvilReplace(WorldGen.cs:76182-97)=地牢砖族(tileDungeon 41/43/44/677-679,Main.cs:7941-46)+裂砖族(481-483)+地牢墙(7-9/94-99,Main.cs:10507-15)不可替换。已补(竖挖+横挖两处,纯谓词零 RNG——种子等价保持)。
2. **裂隙尾祭坛自加吸附**(偏离原版):原版 :76210-40 纯随机点直过 IsTileNearby(26,3)+Place3x2,失败重试 10000(我们注释误写"原版直接放弃");散布版(:14278,猩红)才有吸附+oceanDepths。我们给裂隙尾也加了吸附 → 祭坛钉地表 = 后续裂隙竖挖必经之路,残片概率放大。已移除(吸附不耗 RNG,种子流不变)。

**原版真相**:祭坛(26)**不在**挖空保护名单——原版同样可能出幽灵残片(active=false 渲染不画;原版 .wld 保留幽灵,我们存档幽灵净化=永久消失,表现一致)。用户档 (3518,358) 残片属原版风格产物,敲掉即可。

**验证**:同种子 914488298 重生成(掷到猩红,crimtane 584)——14 祭坛簇全部 6 格完整零残片;seed-parity 6/6 绿。工具:/tmp 脚本(altar-scan.mjs 解 SaveData RLE 找祭坛簇;altar-verify.mjs generateWorld+扫描)——祭坛簇 BFS 按 4 邻接聚簇,size≠6 即残片。

相关:[[jungle-parity-and-id-collision]] [[vanilla-worldgen-passes]] [[save-parity-port]]
