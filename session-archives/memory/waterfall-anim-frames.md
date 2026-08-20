---
name: waterfall-anim-frames
description: "下落水柱\"贴图不对\"根因=1456 双动画帧(中列 X==16 走 0.5/s 瀑布帧),1405 移植时缺;风速调制公式"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T07:49:55.579Z
---

2026-08-11 用户报"水从上方下落贴图不对"(标注 2891,835-841 = 地狱水柱坠入岩浆)。

**根因**:LiquidRenderer 双动画帧是 **1.4.4(1456)新增**,1405 无——我们按 1405 移植只有单一帧,所有液体格共用 ~6 帧/秒快帧。1456 `DrawNormalLiquids`(:636-644):
- IsSurfaceLiquid(X=16,Y=0 且 y>worldSurface-40)→ 固定 1280 表面波浪行
- **sourceRectangle.X==16(中列=下落柱/池体,FrameOffset.X=16 即无左壁)→ `_waterfallAnimationFrame`,Update :852 = 0.5 帧/秒**(慢速流纹,近乎平滑)
- 其余(边缘格)→ `_animationFrame` = windSpeed*25 ± 6 /秒,负风倒放,模 16(:845-856)

下落水柱的格全是"左右皆干边"→双壁分支 FrameOffset.X=16 → 正好命中瀑布帧。旧实现 6fps 快闪即用户所见"贴图不对"。

**修复**(VanillaLiquidRenderer.ts):`waterfallFrame = floor(nowMs/1000*0.5)%16`;帧判定用**最终 sx**(=(16-右壁*16)+fx,与原版 sourceRectangle.X 同构)而非 fx;`srcY = isSurface ? 1280 : sy + (sx===16 ? waterfallFrame : animFrame)*80`。animFrame 补风速调制(负风负速,安全模);Renderer 调用传 `world.weather.windSpeedCurrent`。

注意:WaterfallManager 长柱瀑布(halfBrick 唇缘,Waterfall_N 胶片条)帧速(水每 3 tick/岩浆蜜 7)是另一套,已在 WaterfallRenderer.ts,勿混淆。探针 scripts/_wfprobe.mjs(载用户存档传送截图)。

**Review 补齐(同轮审计,三项相邻缺口)**:
- **群系水色 waterStyle**(Main.CalculateWaterStyle :56771-56824):13 种(0纯净/2腐化/3丛林/10猩红/4神圣/5雪/6沙漠/12地下沙漠/13地狱/7地下/8洞穴/9血月夜/14微光);Renderer.updateWaterStyle 每帧算(SceneFlags zones + clock.isDay + 相机深度 rockLevel+40);液体主表/浸润 pass(Liquid_N)两处按水色取图;vanilla-atlas.mjs MISC 清单补 Misc_water_0-14/Liquid_0-14/Waterfall_0-13,25-27(已重打包落盘)。fountain 覆盖(ActiveFountainColor)无水泉系统未接
- **★长柱瀑布按群系水色换贴图,但走【通道表偏移】非恒等(2026-08-12 三返定论,以此为准;前两返皆误读!)**:WaterfallManager.Draw :1173-1227 有**十二条水样式通道** `DrawWaterfall(贴图号, liquidAlpha[水样式号])`:(0,α[0])/(3,α[2])/(4,α[3])/(5,α[4])/(6,α[5])/(7,α[6])/(8,α[7])/(9,α[8])/(10,α[9])/(13,α[10])/(23,α[12])/(24,α[13])——即腐化样式2→**Waterfall_3 紫**(实测均色 (80,55,144) ✓)/丛林3→4(teal ✓)/神圣4→5/雪5→6/沙漠6→7/蘑菇7→8/洞穴8→9/血月9→10/猩红10→13/地下沙漠12→23/地狱13→24。**错位原因**:贴图 1/2 被岩浆/迪斯科喷泉占用(:663 tile160→num12=2)。样式11蜂蜜/14微光无水通道(走液体类型14/25)。一返错=恒等映射(腐化套到灰色迪斯科 Waterfall_2);二返错=只看第一条通道断言"恒 Waterfall_0"。**教训:多通道循环要全列对,首条通道≠全部语义**。
- **liquidAlpha 交叉淡变(Main.cs:56177/:56845-56860)**:按水样式索引的权重,目标样式 +0.2/帧→1、其余 −0.2/帧→0;水体主画当前样式 + 其余样式按 α 叠画(:56870 DrawLiquid waterOnly)——**用户记忆的"水色过渡"本体**!我们水体/瀑布均为硬切+wsDelay 迟滞(30t/60t),瀑布交叉淡变未移植(登记待补);waterfallStyle 贴图已按通道表对齐。Waterfall_23/24 贴图已补(地下沙漠/地狱)。
- **微光液体**:并行会话 ShimmerPass 已生成(liquidType 4=本仓库编码,与 3=蜂蜜不冲突✓),但渲染(toVanillaType(4)→0 画成水)与 LiquidSim(ShimmerCheck 空实现注释仍说"世界未生成")未接——属他们 shimmer 端到端在途,勿抢先改
- 长柱瀑布水类型帧速已核(1456 UpdateFrame :257-277 仍是 3/7 tick,无回归)

**水色切换/水深衰减二问(2026-08-11 追问)**:
- **原版水色也是硬切**!用户记忆的"过渡"= bgDelay 迟滞(DrawBG_HandleBackgroundTransition :63508:偏好持续 30t 才提交、切后 60t 冷却不响应;森林族 60t)+ 背景层 alpha 交叉淡入(另一套 bgAlphaFrontLayer,未移植)。Renderer.updateWaterStyle 已加 wsDelay 迟滞(统一 30t 近似)
- **水深亮度衰减已有**(lightTables.ts LightMap 移植自带 RGB 分色:水 (0.88,0.96,1.015)×0.91 即水下偏蓝/蜂蜜 (0.75,0.7,0.6)×0.91)——但恒用基准表。本轮补:13 种群系衰减表(updateLightDecay/LightingEngine.cs:143-180 全表,Game 每帧调)+ **夜枭 buff**(NightOwl 12,600s,item 299;nightVision→air/solid 衰减 ×1.03 :184)。blind/blackout/headcovered 与 SceneState 调制无对应系统跳过

**长柱瀑布"贴图不对"三返结论已推翻(2026-08-12 五返修正,以此为准)**:三返称"原版主水流全部取 y=24 行、32px 整槽宽(:740/744/754-758)"——**误读**。那些行是坡面切片+依赖滞后变量的分支;真正的分派在 :823-928,且循环尾 :940-945 回填 num15=上格水平步/num16=上格竖直步/num18=上格水平向/num19=上格坡向(三返当成了死变量),构成**滞后状态机**:
- 竖直格(:823):上格也竖直 → y=24 行 32px 宽带(x-1 起 Flip);上格非竖直(水平/坡后首格) → **y=0 行左半幅 16px 竖条**(带 num11=8 撞地下沉)
- 水平格(:852 switch):非坡 → (16+slot,0,16,16) 右半幅横流条(向右 Flip);坡上横移 → 8×2px 扇形切片(:858-901)
- 坡面格 32px 主带(:801)仅上格非水平(num15==0)才画;flag2 切片(:739)门=坡向≠上格 num18;坡转竖浅流(:761)/撞地 8px 溅片(:779,画本格顶部非下一格)同为滞后门;竖转坡白带(:747)因坡面分支同步 num17=num18 恒假=死代码
- 唇缘半砖格(水平平移)只画 16px 横流条——**不画宽带、不压西邻池面格**(五返用户标注 1484,587 即旧版宽带压池面)
- 撞地后 both-open 分支沿地面水平铺展条@y+8,直到出界/100 步(原版行为)
五返修复=WaterfallRenderer.draw 逐格绘制段按上述状态机 1:1 重写;回归测试 tests/waterfall-draw.test.ts(构造 1484,587 场景 mock ctx 对拍调用序列,7 断言);确定性模拟脚本法比浏览器插桩可靠(相机漂移+镜像变换污染坐标)。插桩探针 scripts/_wfprobe7.mjs、网格 dump scripts/_wfprobe6.mjs。教训:反编译源码里"看起来死"的变量要先全文 grep 赋值点(尾部回填极易漏),head 截断 grep 输出会漏关键行。

**同类问题补齐(2026-08-11 四返——撞地溅落/转向浅流两条已被五返滞后状态机语义取代,见上)**:
- **岩浆瀑布发光**(AddLight :1069-1080):type1 每格 r≈0.22/g=r×0.3/b=r×0.1 橙光,WaterfallRenderer.litCells 收集 → Renderer.drawWaterfalls 后经 renderer.lighting(Game 创建后回填)注入;每帧清空防残留
- GetAlpha 复核:岩浆 1.0/蜂蜜 0.8 ✓、水露天 1.0/有墙或地下 0.6 ✓、末 10 格渐隐 ✓(已对齐)
- 省略项(周边系统缺失,文件头备注):StylizeColor 通道调制(岩浆 190 下限/canvas 无 per-channel tint)、TrySparkling 溅花尘、彩虹/荧光砖改写、环境音
- 贴图尺寸陷阱:Waterfall_11/12/26/27 是 18px 单行窄条(雨幕专用)非 512×40 胶片——水类型 style 永远取 0-13 的 512×40 ✓ 不冲突;雨幕分支(并行会话已加)用窄条
- l10n-audit 插件会阻断整个 vitest(并行会话新增 buff 51-55 未补键时)——协作时可代补 tools/l10n-custom 五键恢复
