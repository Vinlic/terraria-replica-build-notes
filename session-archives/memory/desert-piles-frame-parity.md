---
name: desert-piles-frame-parity
description: 沙漠石堆187贴图错位三层根因:finalize净化器误杀合法换带帧(fx2808)+dgWr零帧+重建截断扫描;修复=换带豁免+整段run模数切块
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-17T09:05:51.937Z
---

沙漠石头装饰物 187 贴图错位修复批（2026-08-17，用户 debug-report"石头装饰物贴图错位"，沙漠 (2988,226) 一带连排石堆）。

## 三层根因（叠加）
1. **finalize 净化器误杀合法换带帧**（WorldGen.ts 帧越界净化）：原版 wld 语义=多带样式存**原始 fx**（Tiles_187 1890×72 两带，样式 52-54 = fx 2808，绘制端 VanillaTiler 分带换算回 (918, fy+36)）。净化器把 fx≥表宽一律清零 → PilesPass 沙地段（`below===53` → style 52-54）头骨石堆全族塌零帧。修复=按绘制端同款分带数学换算后仍在表内则豁免（WorldGen.ts:1546+）。
2. **dgWr 系地牢放置不写帧**（91 旗帜×112 组/241/240/15/93/104… 共 ~220 组零帧，见 `tests/_furn-zero-frames.test.ts` 审计）——**遗留未修**（渲染正确，见 3；写帧=改世界哈希会砸并行金标，另批处理）。
3. **渲染端零帧重建截断扫描**：旧 `ax=min(k,fw-1)` 对**相邻同型零帧物体**连排第 4 格起 ofx 恒 36 → 右列碎片重复=用户所见错位。修复=整段扫描 run 边界 + `(边界距离 % fw)*18` 模数切块（run 左/上边界必是某物体的物体边）——孤立物体行为不变，相邻物体逐格精确。

## 验证
- 单测 `tests/anim-furniture-frame.test.ts` 5 条（新增相邻零帧 3×2：ofx 序列 [0,18,36,0,18,36]，旧逻辑 [0,18,36,36,36,36]）
- 一次性 `tests/_furn-zero-frames.test.ts`：setTileSilent 探针+零帧组清点；修复后 fresh seed 12345 世界 187 零帧 46→0、fx 2808/2826/2844 原始帧存活
- 探针 `scripts/_pilesfix.mjs`：小世界自然簇+零帧化两轮，recording-ctx sx 循环 + 像素 12/12 互异

## 读档修复（旧世界愈合，2026-08-17 追加）
用户旧世界（零帧时代生成）样式数据已灭失（净化器在生成期清零）→ 渲染只能按样式 0 画长草石堆。补 `repairZeroFramePileStyles`（PilesPass.ts 导出，Game.ts 载入侧接 repairIndexFrames 后）：
- 按 PilesPass 地面→样式表推断：沙53→52-54 头骨/草2→14-16/丛林60→0-5/57·58→6-8/神庙226→18-22/396·397·404→29-34/花岗368→35-40/大理367→41-46/石+苔→23-28；掷骰区间取位置稳定散列 `(x*7+y*13)%span`；未知地面不动
- ★幂等关键：整组 6 格**全零帧**才修（样式 0 组修后左上格仍 (0,0)，只查锚点会每轮重修）
- 探针 `scripts/_pilerepair.mjs`：零帧化→修复→fx 2916(样式54)→分带采样 972-1008 ✓ 幂等 ✓
- `?play=small` 会缓存世界（跨代码版本复用旧档）——恰好可当旧世界测试样本

## ★用户定案（2026-08-17 17:00）：旧世界不做兼容，只保新开档正确
读档修复层整体撤销（repairZeroFramePileStyles/repairZeroFrameDungeonDecor 及 Game.ts 接线已删，探针同删）——旧档零帧陈设就按渲染端重建呈现（对齐正确、样式 0）。新档正确性 = 生成端写帧（终清批）+ 净化器分带豁免 + 渲染重建兜底三层。此为长期方向：**今后所有修复只考虑新开档，不做存档迁移/读档回填**。

## 全面清查批（2026-08-17 傍晚，"不要再出现第二次"）
- **样式基准提取**（Item.cs SetDefaults 逐条）：DG 家具 item→placeStyle 全表 + 原版 Place* 帧公式 raw 验证——★大头是**竖排带**族（椅 15 fy=style*40、床/浴 79/89/90 fy=36*style、烛台 93 fy=style*54、241 fy=style*54、2x2 fy=36*style）与横排族（3x2 fx=style*54、2x1 fx=36*style）**不能一刀切 objW**；4x2 镜像=fx+72(dir==1)；6x4Wall 双轴 floor(s/27)*108/(s%27)*72。勘误：2645-47=24/25/26（非全 22）、3900-02=30/31/32（28+type-3898）、2402-04=6/7/8（2397-2416 区间）。
- **骨墙=变体墙 94-105 族**（探针实锤 241 骨画 192 格全在墙 94），非 191/192。
- **读档修复扩展**：`DungeonDecorRepair.ts`（新文件避撞车）按墙主题回填——家具 14 族×[蓝7/绿8/粉9/新族94-105] 列、旗 16+variant*2+hash、画按墙族分流（240 同墙{12..23}/骨{16,17}、241 骨 0-8、242 0-16）；帧布局按 PLACE 公式逐族写。幂等=整组全零门。Game.ts 接 repairIndexFrames 后。
- **撞车实录**：DungeonPass 16:53-16:58 被并行"终清批"实时重写（helper 重构+契约注释"帧走 setTileSilent 由调用方追加"）——本会话只留下 place3x3D 写帧 + DG_ITEM_STYLE 表(:154 已共存)，其余全移交；交接文档 game/docs/dungeon-frame-handoff.md。
- 复扫基线（终清批前）：fresh seed12345 整组零帧 222 组（91×112/241×20/240×16/15×16/93×10…）；`tests/_zero-scan.test.ts` 可复跑。
- #86 扫尾结论：其他 vframeAt 消费点（Renderer 墓碑85/FallingBlock/TileFlames/WldImport copyFrame/repairIndexFrames 门）全部对合法换带帧安全，无第二处误判。

## 要点
- 用户世界=seed 12345（沙漠簇坐标 (2988,226) 在 fresh 复现中逐格一致）→ 探针可用 fresh 世界复刻用户档场景
- **存量档零迁移**：渲染端重建修复使零帧连排正确渲染
- 我方改动（净化器豁免+place3x3D 帧）会改变世界生成输出 → 并行会话的世界生成金标（world-final-hash/caves ×6）预期需要其属主随合法修复重基
- TownNPC.socialUpdate 缺失仍在（并行会话实时编辑中，勿碰）

相关：[[alchemy-table-anim-collapse-fix]]（同日同族：零帧+渲染重建）
