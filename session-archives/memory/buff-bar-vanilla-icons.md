---
name: buff-bar-vanilla-icons
description: "buff栏1:1修复=Buff_{vanillaBuff}原版贴图(388张入库)+11个/行横排步距38行距50+动态建块无白名单+buffAlpha 0.4语义"
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-12T17:06:29.853Z
---

2026-08-13 用户报"buff贴图全不对+多buff应横排"。根因全是呈现层,系统语义(AddBuff 合并等)无恙:

1. **图标错**:曾用"药水物品图标即 Buff 图标"hack。修复=terraria-assets/Images/Buff_*.png 全量 388 张拷入 public/sprites/vanilla/,refreshBuffs 按 `BUFF_DEFS[t].vanillaBuff` 取 `/sprites/vanilla/Buff_{id}.png`(onerror 兜底回物品图标)。
2. **布局**:原版 DrawInterface_Resources_Buffs(Main.cs:42618-42640)+DrawBuffIcon(:42725)硬几何:起点(32,76)、**每行 11 个横排步距 38**、行卷绕 y+=50;DOM 化=flex row wrap width 418 column-gap 6 row-gap 18。探针实测 12 buff:行1 x=32..412、行2 (32,126) ✓。
3. **白名单缺口**:曾硬编码 19 种,战斗/镇静/挖矿/建筑工/糖分冲刺等 20+ 种永不显示——改 refreshBuffs 按 buffs.active 插入序动态建块(makeBuffBlock),原版语义=按 buff 槽全量显示。
4. **buffAlpha(Main.cs:42732/42750-42777)**:基准 0.4、悬停渐亮 1.0、离开回落——alpha 通道非 brightness;inactive 槽重置 0.4(:42649)。

**How to apply**:BuffType 是内部枚举,BUFF_DEFS[t].vanillaBuff 才是原版 id(贴图/文案都走它);新增 buff 无需动 buff 栏(动态建块)。探针 scripts/_buffbar-probe.mjs(注意:?play=small 后再手动 newWorld 会 UI 双挂载 gameMounts=2,buff 刷新全哑——探针别二次生成世界;headless 需 page.bringToFront 否则 rAF 停摆)。

关联 [[buff-system-port]] [[vanilla-resource-bars-port]]
