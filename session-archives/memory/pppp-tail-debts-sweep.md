# PPPP 批：尾段五小债+Tower 复扫（2026-08-19）

- **12345 祭坛级联**：#47-52 祭坛 6 格根因=蜂蜜斑挖蜜池 ClearTile(frameNeighbors:true) 四邻帧→Check3x2(26) 支撑失守→KillTile×6（vanilla HiveBiome 真语义）；修=FinalCleanupPass 导出 genFrameNeighbors/genSquareTileFrame（ZZZ 帧分派复用），HiveSpiderPass 四 Gen 步骤接帧链+FOUT tile 侧。#53 Sl 2,278→0；12345 链 0-48+50-53 全绿，唯一残 #49 Lt=1 (1982,661)=liquid 冻结域（密闭水袋被沉降转岩浆，vanilla 静止）。
- **#58 雕像 7Hf**：PlaceTile cs:59503 else-if 活性锚+ResetsHalfBrickPlacementAttempt（默认 true，例外表不含雕像）→清 half+帧；随机 y 落岩体触发。归零。
- **#76 Traps 8 格**：①EEEE「井杀巨石免杀」=误判——vanilla 照杀，巨石存活靠 KillTile 尾 SquareTileFrame→Check2x2 完整性级联（双陷阱 B 先 A 后序本无差）；②单格短钟乳石须走 checkStalactite 帧分派（矩形锚搜必败）；③沙穴壳侧清坡原版字面列=i-num5-2/-1/+1/+2 全左侧（1.4.5.6 原样 bug 勿对称化）+板 PlaceTile 尾 SquareTileFrame 失活格清 half/slope。归零。
- **#105**：FillWallHolesInArea 移植（地表带墙洞 BFS，≥150 弃填/触空膨胀/众数墙型）W247→1；「204 真缺口」证伪——production 杀集裁决 killed×198/204=frameSparse 探针假差。
- **house#111 193 格=陈旧基座假债**：production 有雕像陷阱红线（±25 窗 11 格）同拒屋；重放 s17 边界 frames.bin 缺线所致。DDDD 四级织入撤销；rig 复用前须 cap 重捕。
- **Tower s33333 复扫**：锚 (698,181) v==j、致动位 6/6 全等、盒差 0.90%=对齐种子带——MMMM Tower 支同修无回归。
- 教训：重放残差先辨基座捕获陈旧度（线/帧通道非金标）；vanilla bug 勿"修正"（清坡左侧列/巨石免杀两案反向）；KillTile 失活邻格清位+165 帧分派是杀链通用件。
