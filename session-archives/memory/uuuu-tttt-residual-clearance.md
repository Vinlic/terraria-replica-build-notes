# UUUU 批：TTTT 五残量清偿（#66/#76/#99 三归零 + #63 全 pass 掷流全等）

- **#66 Temple mayanTrap 全重写**（cs:8314+ 非 2945）：落点门查 232 非 226/SolidOrSloped 谓词族/锚型门 190,135,137,232,237,10/纵扫 worldSurface 非 rockLevel/线色 Next(3) 恒掷/SlopeTile 压平/KillTile 锚/横支 Next(5) 上延叠陷/PlaceTile137 active 保帧；家具 Place2x1 左锚（placeFurn 居中曾偏 1）/雕像 SolidTile2 地面门/挂饰 3x3 以采样点为中心。→八通道零+sink 177/177 全等（4v5 归零）。
- **#76 Traps 帧债定谳无罪**：金标 077×槽31 重放帧对拍 newAtTraps=0——111 帧差全 temple 继承（①修后清）+8 全 dungeon（禁区在案）。
- **#99 ⑦ 重建段落地**（31/12/639/箱21·467 item0 锁箱 style 覆写/28/26+Wall2Terrain 底行补型+右列 639 读左列原版笔误保留）+**KillTile 尘掷勘误**：水死族 24/27 每杀 10×Next(2)（SSSS"零掷"有漏）→ 八通道零+2,059,985 掷逐条全等。
- **#63 双真根因全在 chest 掷**：①loot 16 处 Next(K)+offset 被写成 int(offset,max)（同宽 1 sample 值域平移——SSSS 掷总数口径检不出，须 span 型序列对拍）；②地狱尾 5010/4443/4737/4551 四门漏 flag8 旗（y∈[h-250,h-205) 蜘蛛箱带四掷短路）→ **160,186 掷零分叉**，48/59→2（残=PlaceUncheckedStalactite preferSmall 小型分支未谳，试接 2→1130 回退备案）。
- **两大反编译陷阱**（IL 直读定谳勿按源移植）：AddBuriedChest num11 style 变体门在 errorWorld 分支内（普通种子跳过）；loot 四档链第二档门=num7<rockLayer（IL +1419，反编译折进 flag23 remix 段）。TileFrame(resetFrame) 掷真源=TileFrameImportant 178/184/72 族非 cs:82448（!generatingWorld 挡死）；引擎补 case178+reset 贯通（**读帧族入 dispatch 必同步入 frameSparse 表**否则 #64/65/92/105 假回归带）。
- 基建：/tmp/uuuu-app（Spider 方法体替换织入+InSpider 门控 Next 头钩）；rig 增 SW_WWW_SPAN_DUMP/SPIDER/FRDUMP/CHDUMP 探针；mile8 双种子绿/液体 60/60/冒烟 2/2；gen-loot 1 败=HellFortPass 并行 05:52 在途（复测定谳非自因）。
