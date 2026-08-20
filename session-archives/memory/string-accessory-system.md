---
name: string-accessory-system
description: 线饰品系统全链——stringColor 装备统计/共享 StringLine 段链/XNA 预乘混合三档/提取器落空 case 修复
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-19T08:09:21.999Z
---

线饰品(3293-3308/5540/5541/5547)全链(2026-08-19 子代理建成):
物品 `str` 字段(=Item.stringColor)→ `Player.equipStats.stringColor`(getter 每访问重算;
配饰槽 inv.armor[3-9] 扫描,5540/5541→29 在前、str>0 在后逐槽后写覆盖,Player.cs:36441-36449)
→ 消费:钓线色(Bobber→StringLine)+ 悠悠球线/配重球线段链(WeaponProj YoyoProj/Counterweight)。

**Why:** 曾三处近似:悠悠球线灰直线;钓线无染料;3293-3304 十二件 str 全缺(提取器
落空 case 组只记末标签——与 vanity 面具同坑,`case A: case B: 共享体` 全体标签须映射共享体)。

**How to apply:**
- 共享模块 `src/render/StringLine.ts`:`tryApplyingPlayerStringColor`(Main.cs:34912-34965
  1:1:paintColor+RGB 下限 75+特例 13/14/27/28/30+α×0.4+29 闪烁抖动)+ 段链两变体
  (钓线 :34967-35205 / 悠悠球线 :27799-27912,起点回退 12px vs ×0.1)。
- ★XNA 预乘混合(AlphaBlend=One/InverseSourceAlpha):画色 RGB=加色贡献、A=背景衰减——
  A=0→'lighter' 单笔纯加色(29 号发光线);A=255→source-over 纯替换(钓线 GetColor 重置后);
  中间档→黑形压暗+加色两笔(悠悠球线 127)。Canvas source-over 仅 A=255 时等价,勿直画。
- 线色求值次数:钓线循环外一次(29 全帧同色)/悠悠球线循环内逐段(29 逐段闪烁)——两版各自 1:1。
- 油漆色表 `src/world/Paint.ts paintColor`;Disco/mouseTextColor 时钟 `lighting/SkyColor.ts`。
- E2E 探针 `_string-e2e-probe`(8 色+卸下归零);单测 tests/string-accessory(13)。
- 遗留全部清零(2026-08-19 三子代理批):悠悠球袋族见 [[yoyo-bag-family]];绳锚几何
  (pulley 吸附+gfxOffY+RotatedRelativePoint+坐骑偏移表)已建——★钓线 gfxOffY 原版
  双计(:34982/:35111)照抄勿"修";1456 物品偏移表仅 mount 54 迅猛龙一张;绳族数据
  勘误(v_365/366 曾误标 solid)。关联 [[proj-draw-offset-table]]。
