# SSSS 尾段终清波（2026-08-19）

- **#93 Random_Gems 10/11→0**：placeExposed 邻格清循环换 genSquareTileFrame×2（②cs:59724+③cs:60281 双尾；中心 178 引擎无 case）+ PlaceTile 前置清（cs:59500 坡残格）+ rig slot45 s44 帧回填（嵌合帧 CheckPot 自相矛盾伪杀）。#92 连带保 0。
- **#77 Piles 2→0**：★SolidTile2 **坐标重载 cs:70497 带平台 topSlope 豁免**（`(Platforms&&(half||topSlope))||slope==0`，Tile 重载 cs:70178 无——两重载语义不同！织入 ARB 运行期 dump 实证 slope()==1 且 ST2=True）；2519-vs-2520 仲裁：GPA 实测 3669=252+42+126+15+**2520**+84+630 → ⑤=2520，RRRR 谷值系该 bug 补偿假象。
- **#63 Spider 1203/1331→48/59（−96%）**：placeTightWebs 补 anyShimmer/231 门+ClearSlope+**尾部 CheckStalactite**（泥土支撑 GetDesiredStalagtiteStyle fail→整对杀=T0>165×527 主根因；特殊支撑 style 掷）+ placeDeco187 前置清+双尾帧+anyLava+pot half 清。残=波前分区单点时序差（SF A-访问序 25,188 项全同后 (474,996) 延迟 103 位），0.14% 备案。
- **#99 残=输入债定罪**：SL 锚序 156,354 项全同后分叉=(605,782) A137 雕像帧边界缺失（dir 反向→⑦ 邻杀漏→滴头门跳过）→#58 Statues 债渗入；真缺口=⑦ 31/12/639/箱/28/26 重建段有可见写（~14 格）。④ KillTile 尾部级联已补（cs:63967）。
- **#101 复验未零=箱 sink 179 vs golden 350**（幻影 wire 已清）→ DeadMans 候选流差级联，#58/#59/#62 上游债。
- ★**方法论：genRand 内态 FNV 哈希流是移位不变的（同消耗次数的流位移检不出）——对齐须用 span 序列（SA/SB）+SF/SL 逐调用坐标序**；织入探针全钩版（span/SF/SL/GPA/ARB）留存 /tmp/oooo-app+/tmp/oooo-patch（arch -x86_64+SW_EVIL=0+rm 旧 wld+-world 显式）。
- 回归：mile8 双种子全绿/液体 60/60/冒烟无死循环/WWW 全槽无邻槽回退。
