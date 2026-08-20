---
name: wof-house-and-ores-clarify
description: 肉山砖盒=死亡点13×13只填空壳格难察觉;新三矿+赐福消息=砸祭坛(SmashAltar)非肉山死亡;死亡链无头测试已实证
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T05:06:38.580Z
---

2026-08-13 用户问"肉山死后没小屋/没新三矿消息"——核对结论（防再混淆）：

1. **砖盒**（CreateBrickBoxForWallOfFlesh，NPC.cs:79837-79863，我方 HardmodePass.ts:211 1:1）：肉山**死亡位置**为中心 ±(width/2/16+1)（160px→r=6，13×13 格）；**只填原本非活动的边缘格**（140 魔金砖/猩红 347），盒内液体清零——作用是保掉落物干燥。难察觉三因：只在死亡点、地形格不覆写成残墙、魔金砖在黑暗地狱不显眼。
2. **新三矿+赐福公告与肉山死亡无关**：initializeHardMode（cs:31734-31860）只有 V 带 GERunner+洞穴墙回填；死亡链唯一公告 = misc[15] 光暗之魂。**矿脉+misc[12/13/14](+9) 赐福消息在 SmashAltar**（cs:48949，altarCount%3 选档/3+1 波次/世界锁定 savedOreTiers）——我方 Game.ts smashAltar 1:1 已接。引导：拿 Pwnhammer 砸祭坛。
3. tests/wof-hardmode-chain.test.ts 2 条无头实证（砖盒 48 格完整环+内部空+液体清零；hardMode 置位+V 带神圣/邪恶双转化>50）。**测试坑：内部 tile id 1=dirt 非 stone**（V 带不转裸土,测试地形用 TILE_BY_KEY['stone']）。相关 [[boss-audit-prehardmode-2026-08-13]] [[ore-system-audit]]
