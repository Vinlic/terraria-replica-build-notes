---
name: gun-bullet-size-parity
description: 子弹过大四根因(贴图w归一/判定盒恒10/半速/下坠);绘制尺寸=贴图原生×scale与判定盒解耦;extraUpdates全量249条数据驱动
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T10:03:39.521Z
---

2026-08-13 用户报"子弹过大,枪没对齐"——Arrow 通用弹体四根因全修:

1. **过大主根因**:Arrow.draw 把弹幕贴图统一画进 `w×w·(H/W)` 盒(w 恒 10)——子弹贴图 Projectile_14.png 是 **2×20 竖条曳光**,被拉成 10×100 巨弹。修=绘制尺寸=**贴图原生×SetDefaults scale**(子弹 2×20×1.2),与判定盒 w/h 彻底解耦。箭 1 贴图 14×32 原生(此前也偏小)。
2. **判定盒**:实体 w/h 恒 10;原版按弹型(子弹 4×4/箭 10×10/回旋镖 22×22/长矛 4×4)。构造器读 vanilla-projectiles.json width/height。
3. **半速**:extraUpdates 手工表仅 1 条(83:2);原版 SetDefaults **249 款非 0**——普通子弹 14=**1**(2 子步/帧=2 倍速!)、高速弹 207=2(3 倍速)。提取器 NUM_FIELDS 加 scale+extraUpdates 重生成(1105 条零回归,diff 审计 196 scale/249 extraUpdates);Arrow 改 `opts ?? pd.extraUpdates ?? 0` 数据驱动。
4. **下坠**:枪械发射点没传 grav → 子弹吃默认 0.3 抛物线;原版 **AI_001 无通用重力**(Projectile.cs:51114-54889 内无 blanket velocity.Y+=,仅 349 等特殊款)= 子弹直线。发射点传 `projGravity(projId)`(箭 0.3 保持/子弹 0)。

**测试**:rainbow 星怒 503 期望按原版改(extraUpdates=1 → alpha 255−15×2=225 逐子步衰减)——旧测试按错误单步行为写,遇 extraUpdates 数据化全族弹速/衰减翻倍时需同步修期望。弹幕域 10 文件 63 测试绿。

**遗留**:MagicProj 仍是无贴图圆点(另案);敌人弹(bossAI_*/TownShot)有同款 w×h 归一画法未逐款对账;枪口 14px 偏移为近似。

**教训**:"弹幕过大/过慢"类视觉问题先查三处:贴图原生尺寸(sips -g)、SetDefaults scale/extraUpdates、绘制是否误归一到 hitbox 宽。
