---
name: snow-blizzard-ripple-fix
description: 雪原下雨无雨滴=缺snowing雪粒系统(暴风雪)/涟漪位置错=自创环系统双画退役+splash公式修正
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-14T00:07:24.471Z
---

2026-08-14 用户报"冰雪地区下雨没雨滴"+"水面涟漪位置不对"双修:

**① 雪粒系统移植**(此前整系统缺失):原版 `Main.snowing()`(Main.cs:12964-13045)与下雨独立常开——雪原晴天也飘轻雪,dust 76;**下雨时 cloudAlpha 把雪吹成暴风雪**(尝试 1+50α/t、目标 500×屏比×(1+2α)、雨时水平速度=√|wind|×sign×(α+0.5)×10、vy×0.5 再×(1+0.3α)、scale=1+0.4α、末端×(1+0.5α))。密度=(SnowTileCount/6000)^(4−3α)。雪花贴图=Dust.png 源矩形 **(760,0,10,10)**(1000×120 表,10px 格,dust id 76)。更新分支 Dust.cs:1810-1828(scale+0.009/t、玩家下落 vy lerp 0.04+Y×0.2 补偿、落地 scale×0.9/v×0.25)。实现 WeatherRenderer 自持 snow 池(同雨滴模式,光照 8 级烘焙 tintedFlake)。

**雨滴雪区削减本来就对**(Rain.NewRain :182-184 count/Threshold² 削到 0)——所以"雪原没雨"的真身=雪粒系统缺失(雨没了+雪没有=什么都没有)。

**② 涟漪位置**:实为**双涟漪系统**(双血条/双气泡同病第三案)——SkyRenderer 的"水面扩散椭圆环"是自创近似(随机列采样与雨滴落点无关=位置漂移根因),与 WeatherRenderer 的原版 splash 尘双画。**整套退役**(Weather.ripples/rippleBudget/pushRipple/RIPPLE_LIFE/CAP+SkyRenderer updateRipples/drawRipples+单测)。原版无环状涟漪——Ripples.png 是水体扭曲 shader 掩码(WaterShaderData :108),canvas 2D 无扭曲通道不做。

**splash 公式修正**(Rain.cs:120-133):尘生在 **position−velocity**(检测点入水/入地后退一步=回表面)再 X−2/Y+2;速度=−v×0.025 且 Y−2;概率=gfxQuality(0.5)。曾生在当前位置=沉水/地内 14px。粒子 vy≈−2.4/t 上飘→事后采样全是飞行位移,**验证必须包 emitSand 入口记录**(实测带[-11,0]=贴面)。

**探针** _snow-ripple-probe.mjs 8 断言:定位雪原(列直方图扫 sheet147,注意**扫描窗要对准地表带 y180-400**)/晴天轻雪/雨天暴风雪 587 片+雨滴 0/环系统退役/splash 入口带。雪原雨滴=0 是削减正确生效,splash 测试要搬非雪区。私有 vite 5203 已清。

hooks 增 `snowTileCount`(原始计数,密度指数用;snowRatio 是 /1500 的削减比,两套分母勿混)。相关 [[dungeon-furnish-parity-batch]]

**全量 review 批(2026-08-14,用户令"禁近似全 1:1")**:11 修复(gfxQuality=1 恒溅/雪门1.1×/雨条顶锚origin(0,0)/风场两掷else-if 3-8-3分布/史莱姆阈值杀王减半75/金币雨玩家±2400锚/沙色按格数EmitDust:171/沙尘发射速度密度1:1/云量=numClouds直连0-200/相机视差UpdateCloudParallax/云色=ColorOfTheSkies×(scale×α)链+atmo²)+**遗留2项同日清零**:沙尘dust268渲染池(EmitDust全链簇生j--/num9预算+Dust.cs:1854更新+DrawDust:38403双画(环境光底+GetColor叠画,帧680,20))、云三段深度通道(distant背景后sky层内/closer·closest背景前biomeBg后挂drawCloudsNear,bgTopY=num3×1200+1190,num3=(300−camTop)/(worldSurface×16))。探针_cloud-sand-parity-probe.mjs 8断言(云量饱和147/收敛30精确/三通道/视差drift−6.1/沙尘733粒)。教训:gfxQuality默认1勿当0.5;C# else-if分支是【再掷】不是单掷映射;DrawRain origin=(0,0)顶锚非中心;云淡出0.001/t=千帧慢消散是原版节奏勿误判bug;云屏锚+视差补偿≠随相机移动。
