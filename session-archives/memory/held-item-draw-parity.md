---
name: held-item-draw-parity
description: 手持物绘制对齐——火把/荧光棒静持已实现;火焰叠画默认α0=不可见勿误移植;荧光棒族持位微调表
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T09:31:31.570Z
---

2026-08-13 手持火把/荧光棒绘制对账(PlayerDrawLayers.cs:3146+ DrawPlayer_27_HeldItem):

**原版事实**:
- holdStyle!=0 静持持续在手部画贴图(flag2 分支):DefaultToTorch 全族(flame+noWet+holdStyle=1,Item.cs:48083)+荧光棒族 282/286/3002/3112/4776/5643(holdStyle=1,color=α0)+雨伞/蜡烛/食物等
- 持位(ApplyHoldStyle Player.cs:49532):默认 (frameW/2+2)·dir, Y=24;**荧光棒 282/286/3112/4776/5643 再 X-2·dir Y+4(3002 黏棒不在表!)**;身体帧行 3 举手(:36026)
- **火焰叠画(PlayerDrawLayers.cs:3544+)= 默认不可见**:7 层 ItemFlame_N 每 5 帧重掷抖动(LegacyPlayerRenderer.cs:495-501 X∈[-1.5,1.5]/Y∈[-3.5,0)),但颜色乘子 (100,100,100,**0**) 在 BlendState.AlphaBlend(非预乘)下 α0=隐 → 普通火把/彩色火把/3045 均无额外火苗(物品贴图自带静态火苗);仅 5322(手持蜡烛 α150)/5353(群系火把 α200)/5293(α20 微光)三款可见
- 1405 无此叠画层(1.4.4 绘制重构新增);1405 Main.cs 仅 FlameRing
- 荧光棒本体直绘 α0 不可见、靠 GetColor 二次光照染色绘制——本仓全屏光照合成 pass 已天然等效,勿手工再乘(:1890 双重相乘教训)

**本仓状态**(Renderer.drawPlayer :4589+):静持绘制/holdStyle 三源(itemfunc∪HOLD_STYLE_ITEMS∪IsFood)/noWet 水下隐/行3姿势(:4771)均已实现;本轮补荧光棒族持位微调。

**陷阱**:勿给普通火把加可见火焰叠画=破坏原版(α0 是原版行为);5293/5322/5353 三款物品本仓未登记,登记后接火焰叠画才有意义;三款 ItemFlame png 在 terraria-assets/Images/ 已有。
