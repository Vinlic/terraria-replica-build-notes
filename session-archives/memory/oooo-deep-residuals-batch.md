# OOOO 批（2026-08-19）：三残量深挖——#64/#87 八通道全清 + #77 三修 + IIII 探针雷根因（SW_EVIL=0）

- **#64 Gem_Caves 296/931/2424W→0**：根因=placeExposed 缺 PlaceTile(178) 成功尾帧（cs:60275-81
  `if(tile.active()) SquareTileFrame`）的第三次 Next(3) 幽灵掷（band 内 no-write 只移流）——
  IIII 实测 site#0 d=+23 = 13×roll3 + 10 连带 Next(20)。连修 #92 冰晶簇归零（296→0）。
- **#87 Glowing_Mushrooms 697/1688→0**：三根因=①TryGrowingTreeByType(5)=GrowTree 真长蘑菇树
  （TreePass.growTree 复用）耗 Next(5,17)；②PlaceTile case71 香蒲支（cs:59675-703：j>ws 先
  PlaceCatTail 成功则 Next(14) GrowCatTail 不放 71）全缺=T519 族+流分位；③PlaceTile 成功尾
  SquareTileFrame(i,j)+前置 Clear(Slope)+TileFrame 头非活跃清坡（cs:82077-82）——61↔69 互换
  434 对全消。placePlantTile/placeJunglePlant/placeTile71 三助手统一补齐。
- **#77 Piles 1227→952**：placePile3x2 的 type 形参是内部 id 而 `type===186/187` 比 sheet 恒假
  =InvalidTile 门+Check3x2 样式族击杀链整段死代码（首例=404 沙漠化石地基 187，沙族
  {53,112,116,234}∪{397,398,402,399}∪{396,400,403,401} 不含 404 自杀）；KillTile 实清 type
  （cs:63965——IIII"不清 type"误读 cs:63935）；Check3x2 尾 destroyObject=false+5×5 TileFrame 扫
  可连杀邻堆（cs:49856-62）；PlaceTile 前置清锚格残值（失败也清=eff i0 语义）。残 952=邻近
  装饰帧杀引擎缺（KillTile 探针普查：28罐×12/165钟乳×10/485倒木×3/10门×3/26×2/135×1，
  dropTo 停点漂移级联）——移交帧引擎专项。
- **★雷根因（排雷协议）**：探针 exe 世界 vs 金标 268k 格差=邪恶类型！金标=腐化（gs.crimson=
  false）须 **SW_EVIL=0** 启动（passchain exe 支持）；补上后 Piles 入口整图（含残值 type）
  逐位全同。探针基建：/tmp/oooo-app+oooo-patch（Cecil 织 NA/NB 逐掷 FNV 哈希+PL/PS/KT 钩），
  对拍法=逐掷哈希流 diff→首差定位。WWW rig 修 slot93 base 91→92（冰段放置假差 281→10）。
- 回归：mile8 双种子绿；#93 518→10；冒烟 16.8s；无邻槽回退。
