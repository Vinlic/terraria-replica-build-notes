---
name: cursor-icon-fullbright
description: 光标悬停物品图标恒全亮——GetItemLight 默认参不采光照;source-atop 叠黑画布=黑方块陷阱
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-18T07:33:36.482Z
---

DrawInterface_40 悬停图标（Main.cs:44519）调 `ItemSlot.GetItemLight(ref color, num)` 时
**outInTheWorld 用默认 false → 根本不采样世界光照**（ItemSlot.cs:3458 只处理迪斯科
662/663/5128、微光脉冲、精华 58/184/4143），currentColor 恒 White → 图标**任何时候全亮**。

**Why:** 曾误读为"乘光标格光照"并用 `globalCompositeOperation='source-atop'` 叠黑模拟变暗
——source-atop 作用于整张已渲染画布(世界层不透明),暗处 alpha→1 = 纯黑方块盖住图标
(2026-08-18 用户报"悬停贴图全黑")。

**How to apply:** 图标/UI 层永远直画不乘光;要乘色时用三步离屏(multiply+destination-in
恢复 alpha),绝不在主画布 source-atop。未接的特殊物品改色分支已在 Renderer 注释备案。
关联 [[cursor-item-icon-port]]。
