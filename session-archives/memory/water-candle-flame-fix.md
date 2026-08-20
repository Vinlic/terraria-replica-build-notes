---
name: water-candle-flame-fix
description: "水蜡烛\"蓝+红焰叠加\"=邻焰外溢盖格;蜡烛族火焰绘制尺寸曾18x18(原版16x20零外溢);tintedFlameCell缓存键须含贴图身份"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-17T10:10:36.455Z
---

2026-08-17 用户报"水蜡烛出现红色火焰,像蓝+红叠加,原版没红焰"。

**排查**(矩阵探针 scripts/_candle-matrix.mjs 保留:地板/平台/桌上×昼夜×邻位):
- 水蜡烛本体火焰**纯蓝零红**(夜间孤立 red=0;贴图 Flame_5/Tiles_49/ItemFlame_148 全蓝,与原版逐桶一致);
- 红色只出现在**邻位有暖焰源**(火把/蜡烛)时——邻居火焰外溢盖进水蜡烛格。

**根因(两处)**:
1. **火焰绘制尺寸用了图集格而非原版 tileWidth/Height**(GetTileDrawData):蜡烛族
   33/49/174/372/646 原版 **16×20**(:4887-4893, tileTop=-4)恰零外溢;我们画 18×18 →
   外溢 1px×7 份叠加;火把原版 **20×20**(:4724,上方实心 tileTop+4),我们 22×22。
   修=FLAME_DRAW_SIZE 表覆盖 r.sw/sh(同格左上取 w×h),dx=x*16-(w-16)/2 不变。
2. **tintedFlameCell 缓存键不含贴图身份**:各族源矩形同格同 tint(如 default 族都是
   (100,100,100))会跨 Flame_N 表命中——后画的族拿到先画族的颜色(潜在蓝+红叠加源)。
   修=键加 img.src。

**方法论**:像素色桶分类器会把木头/蜡体暖棕计"红"(矩阵 red=40 恒值=分类噪声);
断言红焰须夜间+孤立+黑背景。原版火焰源矩形=(tileFrameX, tileFrameY+addFrY, w, h)
——w/h 来自 GetTileDrawData 各 case,非图集元数据,两套尺寸勿混。
