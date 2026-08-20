# RRRR 批（2026-08-19）：邻近装饰帧杀引擎 + #77 残 952→2

- **引擎落地（FinalCleanupPass.ts 扩展为通用帧杀引擎）**：①实心谓词全改 genSolidType
  （229 在 Piles 期间非实心→罐失撑击杀，静态表查不出）；②KillTile 尘掷实测表——
  **26/695 祭坛 frameX<54→10×Next(2)/格**（织入探针两杀间恰 10 单参掷实证），
  28/165/485/10/135/185/186/187 **零掷**（OOOO 移交的"尘掷表"实为击杀普查数）；
  ③Check3x2 补金币掉落掷+5×5 尾扫+187→186 raw type；④新族 CheckDoor/Check1x1
  （135=229 失撑）；⑤PilesPass 统一走 genSquareTileFrame，双尾帧（case 分支尾
  无条件+成功尾再跑=引擎两轮）。
- **三真 bug**：平台 tileSolid 补真（{19,427,435-439} 锚定门曾拒放，P3(1930,1090)
  实证）；⑤段迭代上界 **2519**（IL 读 2520 但掷值解码证明 vanilla ⑥ 起于 170661，
  2519 为残量谷值，1 次之差未解备案）；尘掷门 frameX<54（回填 style 9 会吞掷）。
- **重放基座帧回填（tools/www-framebackfill.ts）**：金标无帧通道+边界帧系捕获期
  历史——按族分裂信任：罐/485 全几何右锚切瓦、185 无条件 1x1、186/187/26 相位感知
  （覆盖留边界帧）、165 全几何 biome style。杀普查终态对拍 7 族逐格全同（165×10
  须终态反查——killStalactiteTile 不进 killTileGen 钩）。
- **#77: 952→2**（残 2 格=顶坡平台支撑小堆，vanilla 放置与 slope==0 门矛盾未解）；
  **#93 10/11 未动**（GemPasses 冻结；引擎就绪，placeExposed 邻格清循环换
  genSquareTileFrame 一处即接）；#99/#105 旧债未塌缩；#63 与在案同（他案在途）。
- 回归全绿：mile8 双种子/液体 60/60/冒烟 22s（+5s 可接受）/gem+tile-cleanup 24/24；
  world-final-hash 红=交付后再生窗口状态。★方法论：掷值解码（UnifiedRandom 状态
  推进与调用域无关——快进 N 掷读原始样值可反推 x/y/样式归属段）；杀普查须含
  killStalactiteTile 等旁路；IIII/OOOO 哈希流"逐位全同"是位置平凡的（同种子必同）
  ——语义对齐须 P3/PS/kill 事件按掷位对齐。
