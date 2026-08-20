# IIIII 两备案格终清：#63 蜘蛛箱预清场级联 + #54 CanKillTile 树干族腿

- 交付：9293480 首差 #63→#64（0..63 全绿）；12345 首差 #54→#59（0..58 全绿）。
- #63 真根因（XXXX"波内时序微差"证伪）：分支级 SpiderProbe 织入对拍 173,357 行
  逐行全等（掷流 160,186 本就全等）——差格是**蜘蛛网箱覆写装饰伙伴后的级联孤儿**：
  vanilla TileObject.Place(cs:79-90) 预清场对覆盖格 cut 族 KillTile+尾九宫级联
  （CheckStalactite/CheckPile 杀 (495,748)/(415,922) 孤儿）；JS placeBuriedChest
  写侧无清场。修=HiveSpiderPass CH 支事后补放（箱体四格快照→回滚→KillTile 镜像
  (51+wall62 补 Next(4))→genSquareTileFrame 级联→重写）；掷流恒零掷证明：
  巢内 165 全 fx=108+ 族 style=11==desired(GetStalagtiteStyle frameX/54==2) 永不进
  重定型掷——事后补杀与 vanilla 先杀后 loot 逐位等价（span 160,186 复验）。
- #54 真根因（WWWW"流分叉"证伪）：WFProbe 织入（RunPass 闸+PoundTile 头/返+
  Next 头/返）——掷流 3332 全等、pound 调用 773 含返回值全同，唯 (3845,1045)
  vanilla PoundTile 返 0：633=AshGrass 上格 634=TreeAsh∈IsATreeTrunk{5,72,583-589,
  596,616,634}→CanKillTile 树干族早退；JS canPoundTile 近似漏此腿。修=HalfBrickPass
  IsATreeTrunk 表+异型+三帧门字面镜像。
- ★织入坑：ret 前 [dup,call] **先插 dup 再插 call**（复踩 ZZZZ——先插 call 得
  [call,dup,ret]=InvalidProgramException，首发症状=Player 静态构造链崩）；
  TypeReference.Fields 须 .Resolve()。
- 方法论：全等轨迹+金标几何重建=把"备案级微差"收敛到写侧单点；"修复前绿 ⟹
  vanilla 腿零命中 ⟹ 镜像零命中"免四链全复跑。
- 资产：/tmp/iiiii-app+iiiii-patch（SpiderProbe 分支级+WFProbe）、/tmp/iiiii-work
  （两侧轨迹/决策流/cmp 脚本）；__swSpiderDeco/__swWfLog 常驻 env 钩+rig
  SW_WWW_SPIDER2。
