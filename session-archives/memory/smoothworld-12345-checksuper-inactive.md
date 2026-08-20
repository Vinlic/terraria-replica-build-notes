# 12345 #53 SmoothWorld 自差清零（LLLL 批 2026-08-18）

- **双根因**：① KillTile 尾级联缺 `CheckSuper`（cs:86437-40 case 376/443/444/485 → cs:48117-48406）
  派发——485 蚁狮幼虫 2×2 完整性破组杀（Style2x2 派生 CFW=CFH=36/StyleHorizontal；
  生成期在场仅 485）。实锤 (1856,476)：K(1857,475) 尾帧触邻格 485 → 组伴被大理岩顶替 →
  整组杀+残凸砸半=**两枚零掷动作**（流恒齐只动作数漂 → 全图半砖/坡放大）。② SolidTile 族
  （cs:70170/70052/70228）缺 `!inActive()` 致动腿——12345 vanilla 穹顶 234 格致动柱，
  JS 视为实心 → 穹壳 6 格 slope 错写（(3396,158) 等）；JS 管线无致动写入故他 pass 不动。
- **修后**：反事实（golden052 基座+管线帧快照+GenSolid 时点态 restore）→ **八通道差 0/
  动作 89,683 全等/掷 5,098,924 精确**；9293480 主链 0..53 全绿+_hstrace ★全等★ 不回退。
  12345 管线残余=穹顶输入债 loop2 掷偏移翻面（对称 S0>3/S3>0），MMMM 清 #32 后塌缩。
- **方法论**：★零掷但非零写的级联**掷数对拍不可见**，必须动作序列对拍（swtrace exe
  a4f3d8ce + JS __swSWAct 同格式）；第二种子 trace=/tmp/llll/swtrace12345.log（5.37M 行
  只覆 #53，末 RD 哈希==pc.txt P|53 f6）。9293480 存档曾误删已再生（字节同/哈希链同
  passchain19/_hstrace 全等四重验证）。
- 详见 game/docs/worldgen/content-parity-vs-vanilla-2026-08-16.md「LLLL 批」。
