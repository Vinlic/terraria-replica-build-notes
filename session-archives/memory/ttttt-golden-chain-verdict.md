# TTTTT 批（2026-08-20）：金标链完整性终裁 + #86 荆棘谜案翻案

## 终裁结论
- **g/ 原链无罪**：JJJJ 配方重产 `/tmp/sw-slp/g-verify/`（hs.exe md5 80e7ca0e…、
  SW_EVIL=0、独立 HOME、端口 7805 自起自 kill）→ 848/848 dump 逐字节全等 + pc.txt
  哈希列全等（仅计时列差）。无探针时代钩子残留、无环境期一次性污染。
- **exe 织入内污染也排除**（三层锚）：
  1. `/tmp/vserver86/s9293480_e0.wld`（evil_srv=**8/16 15:36** md5 593e587a… 谱系独立
     最小织入）vs g-verify/105 八通道全 0（豁免：act=0 幽灵 typ 1,475,878 + 微光 980）；
  2. s12345.wld=gen86.sh 自然支（**纯 Steam**，队列 evil 列空）=g12345/105 全 0（JJJJ ①）；
  3. **结构性**：RunPass 每 pass `Main.rand = new UnifiedRandom(_seed)`（cs:491，
     genRand=>Main.rand cs:4391）——pass 间任何织入耗掷被下次重播种抹除，
     「85 边界织入侧多耗掷」不可能。
- 顺带勘定：**9293480 自然 evil=crimson**（s9293480.wld isCrimson=true，与链差
  A=175k/W=227k）；g/ 是 SW_EVIL=0 强制 corruption 变异，勿当自然世界引用。

## #86 翻案（RRRRR 备案的"金标嫌疑"撤销，改判 JS 侧共同漏读）
- **真凶**：PlaceTile 样式支（cs:59580-59592，hs.exe 二进制 IL 逐指令同构）——
  进支后 `NfL(14元表)` **无条件先掷**，随后 `num==201→NfL(16)`、`num==637→NfL(5)`
  **二次掷覆写**（前值弃、掷已耗）。
- **漏读形态**：JS placePlantTile（SurfaceDecorPasses.ts ~2088）`先按 num 选表再单掷`
  ——637/201 样式放置每次少掷 1 次。RRRRR 的"独立模拟"按同一读法写成 → JS↔sim 逐掷
  一致（3735 掷零分歧）却双双偏离 binary——**"独立"不独立于读法即无法定谳**。
- **铁证**：tttt-app（span 织入）`SW_TT_SPAN_PASSES=Weeds` 跑 9293480 →
  /tmp/ttttt-span86.txt = binary 掷界序列 **3757 掷** vs sim 3735（净差 **+22=22 个
  637 样式放置**）；修真序后掷界 **3757/3757 逐掷全等** + 8ch vs golden86 **全零**
  （10 格荆棘翻转 100% 复现归零）。
- RRRRR 的"+3/+5 注入复现"= 分布式 +22 在 #22 邻域的**局部对齐伪影**（动态组形级联
  使多组 (p,k) 收敛同有效对齐——注入法证窗口 p=1..1405 含 k∈{1..8} 多命中）。
- **修复移交**（本批零 src 改动）：placePlantTile 样式支改真序；预期 #86 自债 10→0；
  审计项=一切 PlaceTile(201/637/110) 样式支调用点。

## 方法论沉淀
- 三方链完整性裁决法：同 exe 重产（确定性）+ **异谱系织入终态锚**（对拍 .wld 八通道，
  用 WldParser）+ 纯 Steam 自然锚（仅自然==强制种子可用）+ 重播种结构性论证。
- span 织入对拍掷界序列（NA/NB 头钩只记 bound）足以定位"漏掷/多掷"类移植差——
  比状态对拍更强的中间层证据。
- Cecil 只读 IL 审读器在 /tmp/ttttt-ildump/（net10+Cecil 0.11.6；注意 mod.Types 不含
  嵌套类型须递归、ldc.i4.s 与 ldc.i4 两 opcode）。
- 对拍中"唯一掷敏可见位=荆棘 bit"（其余全为帧）⇒ 注入法窗口多重命中是常态，
  勿以"注入可复现"反推单一注入点。

## 资产
- /tmp/sw-slp/g-verify/（验证链 5.0G 留档）；/tmp/ttttt-span86.txt（binary 掷界铁证）；
  /tmp/ttttt-sim86-bounds2.txt（修正 sim 掷界）；/tmp/ttttt-ildump/（IL 审读器）；
  报告章=content-parity-vs-vanilla-2026-08-16.md「TTTTT 批」。
