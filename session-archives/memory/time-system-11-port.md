---
name: time-system-11-port
description: 时间系统1:1：昼夜边界4:30/19:30常量Clock.DAWN/DUSK、全周期24min恒速tick(勿分段调速!)、起始8:15AM、time↔Main.time换算86400
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-12T06:47:22.730Z
---

时间系统 1:1 落地（2026-08-12，whip8-time-probe.mjs 全绿）：

**Clock（src/world/World.ts）**：
- `Clock.DAWN=4.5/24=0.1875`、`Clock.DUSK=19.5/24=0.8125`（原版昼 4:30AM-7:30PM）
- **全周期 dayLengthMs=24min、tick 恒速**（dt/dayLengthMs）——0.625/0.375 窗口自然得出昼 15min/夜 9min。**★勿按段调速**：首版除反（/span）导致昼夜缩水到 12.7min，探针抓回
- 起始 timeOfDay=8.25/24（8:15AM=Main.time 13500）；此前 0.3(7:12)/30min 周期/6:00-18:00 边界三处偏差全修
- time↔Main.time 换算（Game.ts:328）：恒速 86400t/周期 → 昼 (t-DAWN)×86400 / 夜 (t-DUSK mod 1)×86400

**消费者迁移**：Game 昼夜事件 crossed(0.25/0.75)→crossed(Clock.DAWN/DUSK)；WindSway/SkyRenderer 的 isDay 副本改读 ClockVal（**type-only import 取静态常量 esbuild 会剥掉——必须值导入**）；TitleMenu/Renderer 夜进度字面量 0.8125；城镇 NPC 夜对话 nf=(t-DUSK mod1)/0.375；旅行商人离场 (t-DAWN)/0.625>0.8。

**存档兼容**：hour=t×24 线性映射两侧一致（0=午夜），旧存档 timeOfDay 无需迁移。

**事件层早已 1:1**（血月 1/9/>120HP/非新月/灯笼压制、日食 1/20、月相黎明+1、哥布林海盗 roll、灯笼夜/派对/月事件/税款）。

**遗留**：床睡 5 倍速（床系统本身未实装）；MenuBackground 菜单背景用独立 150s 时钟（纯装饰从略）。

相关：[[class-stat-reconciliation]]

**锁帧(2026-08-18 补)**:渲染曾无上限跟 rAF(120/144Hz);原版锁 60fps。
修=OptionsData.frameCap(默认 60,0=不锁),Game.start 循环按档跳 rAF(提前
到档内的帧直接 re-register 跳过,-1ms 余量防 vsync 抖动漂移);逻辑 tick 恒
60Hz 不受影响(fixedUpdate 累加器下帧补步,≤5 步钳)。设置面板三档循环
60/120/不锁(modeRow)。探针实测:默认 60fps/dt 17ms;切 0 后 ~109fps/dt 8ms;
切回 60 恢复。★锁 60 同时把渲染/GPU 负载砍半——高刷屏用户不锁才有满帧体验。

**原版性能策略清单终审(2026-08-18)**:锁帧后全面对表,补 Frame Skip
(原版视频设置默认开):渲染耗时>预算×1.5 → 本帧只跑逻辑不渲染(连跳≤2 钳),
options.frameSkip+设置行。**仍未移植:①异步光照(原版 LightingEngine 后台
线程+交换缓冲,主线程用上一帧结果——我们同步跑,blurLine ~0.55ms/帧+尖峰
不平滑;移植需 worker+一帧延迟语义,收益中等,登记后续)②SpriteBatch 批
渲染(canvas restore 34% 的终局=渲染器 v2)**。已对齐:逻辑 60Hz/渲染上限/
跳帧/世界演化时间片/尘 gore 视口剔除/实体粒子上限池/声距衰减/动画分档。
**流程教训:标杆审计必须含工程策略层(帧率/跳帧/预算类),不只数值行为——
前期全在"让每帧更快",没看"让帧更少"这半边,锁帧这类零成本高收益项
被漏到用户点名**。

**画质档位终局(2026-08-18)**:①光照模式不移植——原版四档实为
White/Retro/Trippy(全走 1440 行 LegacyLighting 遗留引擎,Mode 1/2/3)+
Color(新引擎,即我们唯一已移植的);用户拍板"旧版引擎不要了",保持 Color
单引擎。②跳帧升级三态(原版 FrameSkipMode Off/On/Subtle,默认 Subtle:
落后整帧(>2×预算)才跳+连跳≤1——原版 successiveSkippedDraws<=0 语义
Main.cs:16968;On=1.5×/≤2 激进);旧布尔 frameSkip 有迁移。③**新发现:
原版 gfxQuality 自动画质系统**(Main.cs:16908-16933:fps≥30+30q 缓升/
<29+30q 每秒降 0.1,驱动动画/波浪/mapTimeMax 预算;qaStyle 1/2/3 手动钉
1/0.5/0)——未移植,登记待水面波动系统立项时一起(它正是波浪预算的调节器)。
④水面波动模拟子代理曾被派发后被用户停止,状态未落地。

**gfxQuality 自动画质已接入(2026-08-18)**:src/core/GfxQuality.ts(调速器
1:1:每秒一评,fps≥30+30q 缓升 rate+0.005/掉破 29+30q 骤降 0.1,29~30 带
滞回,q∈[0,1];计数=实际渲染帧,跳帧不计)。四消费点全接:瀑布
MAX_FALLS()=1000×q/DIST()=75q+25(WaterfallManager.cs:116-117);雨密度门
rand(100)<q×100(Rain.cs:123,每滴独立掷)+落水花同门;雪活片门
target×(q/2+0.5)+0.1×target(Main.cs:12993);小地图 flushDirty 节流
(1-q)×60ms、q≥0.8 恒 0(:16941)。F5 报告 gfxQuality 字段。qaStyle 手动
三档暂缓(等波浪代理落地后随 Options 一起,防同文件冲突)。q=1 时全部
行为与接入前逐像素一致(门的边界即 1.1×target/恒溅原状)。
