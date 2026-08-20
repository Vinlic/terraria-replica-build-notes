---
name: hell-background-fix
description: 地狱背景三修:黑盒层序(先打底)+magmaLayer 公式(曾误用 lavaLine 低135格)+magma 3帧动画/表面条;ugSlots 槽位覆写陷阱
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T15:28:35.492Z
---

2026-08-12 用户报"地狱背景缺失+接近地狱层叠错误+背景有动画?"。对照 Main.cs :52230-52503 修三处:

1. **黑盒层序**(:52265-70):原版 SurfaceTransition→Dirt→【黑盒打底】→Rock→Magma;我们黑盒画在带层之后→盖掉岩浆=两个症状的共同根因。黑盒高度=min(viewH+200, UnderworldLayer 屏 y)(:52810-17,UnderworldLayer=h-200)。接近地狱时屏上方渐黑是原版观感(黑盒打底后仅岩层/岩浆重画)。
2. **岩浆带顶公式**(:52237):magmaLayer = ws + floor((h-330-ws)/6)*6 - 5 ≈ h-335——我们曾误用 lavaLine(h-200),整条带低 ~135 格。bgTopY=magmaLayer*16-screenY+16+600-8。
3. **动画确认有**:magmaBGFrame 每 8 tick(133.33ms)推帧 mod 3(:61657-65)。岩浆体=**槽[5]=125+hell**(160×288=3 帧×96,sourceY=frame*96,:52423);表面波纹条=**槽[6]=185+hell**(160×48 取 16px 行 sourceY=frame*16,画在 UnderworldLayer 高度 :52488-97)——表面条曾从未绘制。

**ugSlots 槽位陷阱**:原版 UpdateBackgroundStyles(:53418-26)在 switch **之后统一覆写** tempBack[5]=125+hell/tempBack[6]=185+hell 对所有 case 生效;我们的 case 0/default 分支曾漏覆写([5]/[6] 残留 5/t[6] 错位)。修法:case 0/default 也返回 t[5],t[6]。

回归:tests/hell-background.test.ts 3 例(录制式 ctx 断言层序/带顶公式/帧行取帧;注意 drawImage 9 参 dy=args[5] 非 args[1];magmaFrameT 跨调用累计=原版全局计数,mod-3 用例需新实例)。浏览器探针失败因=dev server 被并行会话 HMR 挤爆(page reload 刷屏),改确定性单测更可靠。

**★三返(同日,用户 wiki 打脸):深层"纯黑"结论错了!** wiki 地狱背景=**多图层视差远景**(岩柱/岩浆湖/熔岩瀑布岛屿/山体洞穴)——独立系统 `DrawUnderworldBackground`(Main.cs:52082-52228,非地下分层那条链):gate=屏底≥(h-220)*16;5 层 idx4→0(parallax 1/(idx*2+3) 纵横同);风格集 0:[0-4]/1:[5-9]/2:[10,11,12,13,9](WorldGen.cs:7578-7597,setBG(9,Next(3)));**2×2 四帧行动画 8fps**(贴图 1/6/7/8/13,矩形分幅 1 用 (f>>1,f%2) 其余 (f%2,f>>1));各贴图 Y 偏移(1:+175/2:+100/3:+75/6:-60/7:-400x+90y/8:+90/9:-30/10:+250n/11:+100n/12:+20n/13:+20n);贴图4细柱条 scale0.5 其余1.3;Y 锚 UnderworldLayer*16 经深度投影;**层0 底部黑补 rgb(11,3,7)**;pushUp=(zoom-1)*100。素材 `Images/Backgrounds/Underworld N.png`(空格名!)→ public/sprites/vanilla/Underworld_N.png。已实现 drawHellLayers(BiomeBackground,画在黑底后/带层前,混合区带层自然遮挡)。
**教训:清屏黑≠纯黑背景——全图 grep bg 相关方法族(DrawUnderworldBackground 与 DrawBackground 并存),wiki 条目是免费的需求清单**。
遗留:underworldBG 存档字段(WF:1376)未持久化(与其余背景风格同走 seedPick 策略,登记 save-parity 账本);pushUp 取固定 zoom 1.25;SkyManager.DrawToDepth 深度交织略(顺序绘制近似)。

相关:[[vanilla-bgm-background-port]] [[waterfall-anim-frames]](背景发丝缝 +1px 外扩同文件) [[save-parity-port]]
