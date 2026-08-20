---
name: moonlight-audit
description: "夜间月光=tileColor种子×月相地板(满月19/新月11);链路已1:1在跑,夜黑=原版行为;MoonPhase枚举Full=0起"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-14T09:20:53.836Z
---

2026-08-14 用户问"晚上很黑,原版有月光吗"——**有,且我们已 1:1 在跑**(全链实证):

**原版机制**(月光三件套):
1. 天空色五段昼夜曲线(SetBackColor Main.cs:62889-63362):深夜 (5,5,5)→黎明前 (25,35,35) 蓝移
2. **月相地板**(:63230-63266):bgColorToSet 每通道 max(值, minimalLight[phase]),
   血月恒 25;**MoonPhase 枚举 Full=0 起**(MoonPhase.cs:4-13:满/3/4L/半L/1/4L/新月4/1/4R/半R/3/4R)
   → 地板表=[19,17,15,13,11,13,15,17](首夜=满月!)
3. **tileColor**(:62608-62616):(R+G+B+7C)/10 逐通道 → TileLightScanner.ApplySurfaceLight(:3152)
   播种露天格(墙==0/wallLight + 非挡阳 + 液深<200)

**我们的实现位置**:src/lighting/SkyColor.ts setBackColor/tileColor/skySeed + lightTables.MOON_FLOOR
+ TileLightScanner.exportTo 播种——逐数值核对与原版一致(枚举序曾险些"修"反,查枚举后确认本表正确)。

**实证**(scripts/_moonlight-px.mjs,保留):夜半露天格引擎光=23/255(满月)/13(新月),
渲染像素 day 122→night 10(满月)/6(新月)——比值=引擎值,无双重压暗
(compositeLight 全屏乘光=原版"无 gamma 无下限"语义,Renderer.ts:7604)。

**结论**:夜间暗=原版行为(泰拉夜晚本黑,满月夜≈9% 亮度可见轮廓,新月夜≈4% 近黑;
原版玩家靠火把)。若用户觉得更黑,查月亮贴图是否显示(Moon_N 8 相位)而非光照链。
