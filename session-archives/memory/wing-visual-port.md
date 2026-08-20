---
name: wing-visual-port
description: 翅膀视觉1:1(锚点三连bug根因/逐款帧状态机表/alwaysAir门)；探针抓canvas必须g.renderer.canvas非querySelector
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T15:26:05.140Z
---

翅膀飞行动画 1:1（2026-08-13，用户报"角色飞的时候背后没翅膀"）。

**根因三连（旧代码全在但全坏）**：
1. ★ Renderer.drawPlayer 已平移到脚底中心局部空间后，翅膀块又 `ctx.translate(p.cx, p.y+p.h*0.45)`——把**世界坐标当局部偏移叠加** → 翅膀画到 2× 世界坐标处（屏幕外）。这是"看不到翅膀"的主根因。
2. 内层再 `ctx.scale(facing>=0?1:-1)`——外层已 scale(facing,1)，facing=-1 时乘积=1 **永不翻转**。
3. 帧数写死 7/HOVER6 集——原版 generic 尾段 num14=**4**（PlayerDrawLayers.cs:943-1000），只有 43/44=7。

**正确锚点公式**（:662-664）：局部 (0,−21)（= h−bodyFrame.Height/2+7，bodyFrame 高恒 56 与碰撞盒无关）+ 逐款 offset (num13−9, num12+2)。镜像空间里 X 局部值 = num13−9（directions.X 的 dir²=1）。表见 `src/data/vanillaWingVisuals.ts` DRAW_TABLE（5/12/27/41/43 微调 + 22/28/34/39/45/48/51/47/49/50/40 特殊分支锚）。

**帧状态机**（WingFrame :29002-30045，Player.cs）：
- flap=flag19 门：`wings>0 && controlJump && wingTime>0 && jump==0 && vy≠0` **或** hover 档固定集 **FLAP_HOVER_SET={22,28,30,32,29,33,35,37,45}**（:26477，与 VISUAL_HOVER_SET={22,28,30,31,33,35,44,45} :28994 **是两个不同的集合，勿混**——曾用 eq.wing.hover 近似是错的）。
- generic 尾段 5t/帧（counter>rate 进帧）循环 0→1→2→3；下落帧 1；地面 0。逐款：43 rate3/max7/reset1/下落2、48 rate2/max8、32 rate3/下落3、4 循环0-2+张翼3、22 六档模式、12 [1,2,3,2]@5t、30 1+counter/2、34/39 rate4/9/6 恒循环、45 counter/3(无时5)、44 fall 2/3、51 帧2-7、47/49/50 11帧三态推进（50 转移1→3）。
- **滑翔帧覆盖段**（:26874-27010，在 WingFrame 之后执行）：!flap && controlJump && vy>0 时逐款覆盖——默认→2，48→3、40→0、44→2、43→1、12→3、26/37→2，30/34/39 恒循环；22/28/45/51/47/49/50/24 除外。
- **33/38 特殊语义**：WingFrame 分支只喷尘后 return（帧永不动），帧只由滑翔覆盖驱动 → 首次滑翔后停 2、**落地不归零**（原版如此，勿"修"）。
- 绘制门 ShouldDrawWingsThatAreAlwaysAnimated（:30271：vy≠0 && 未锚定钩爪 && 非水中漂浮 && mount.CanUseWings）：22/28/34/39/44/45/48 仅空中画；generic 地面也画（收拢帧 0）。坐骑禁翼族（:26316 wings=wingsLogic=0）→ 本仓 ridingMount 直接不画。
- 执行位关键：帧机必须**每 tick 跑**（含地面）——33/38 落地保持、generic 地面归零都靠这个位置（Player.ts 翅膀 if/else 之后）。

**偏差登记**：发光叠画（22火焰/23/27/43/44彩虹/47/50双画/28 Extra38）、40 Betsy 14帧程序化摆动（单帧近似）、逐款翅膀尘、47/49 headgear 逐行±2px、tryKeepingHover 锁存、downDash（isPerformingJump_DownDash 未建模）。

**探针教训**：截图像素差验证必须用 `g.renderer.canvas`——`document.querySelector('canvas')` 抓到的是别的 canvas，diff=0 假阴性（曾误判渲染仍坏）。装翼= `p.inv.armor[3]={id,stack:1}`（equipStats getter 每次访问重算，无需手动刷新）；按住跳注入 `g.input.touchKeys.add('Space')`（keys 是 Set 非 props）。

**验证**：tests/wing-visuals.test.ts 33 用例 + _wingprobe.mjs 17 断言（像素差 3926、flap 0→1→2→3 5t/帧、wingTime 消耗回满、34 型飞行喷尘 maxDust=11、45 历史环 len=31、47 叠画 diff=2306+队列 flush=0）。全量 vitest 其余失败均为并行会话在途（世界生成金标/钱币 maxStack/godmode/iceSkate）。

**偏差清零批（2026-08-13 二轮，/goal 不能偏差）——首批登记项全部处置**：
- ★ **叠画全接**：22 火焰簇 ItemFlame_1866×7（itemFlamePos 每 5t 重掷，:493-502）/23 Flame_8(200³,200)/27 Glow_92(255³,127)/30 Glow_181(255³,127,:1038)/38 Glow_251×undershirtColor(:1044)/43 Glow_272×2 抖动/47 Glow_366(180)/50 免疫双画/45 Projectile_250 拖尾+mainWhite/28 mainWhite+Extra_38(:705-722)/44 Extra_171 彩虹层直画/34(250³,100)/51 luna 脉冲/40 Betsy 8 片程序化摆动(:854-896)。
- ★ **主纹理分两族**：lit 族（colorArmorBody）合成前画；**全亮族（mainGlow：28/34/40/44/45/51 硬编码色）+全部叠画入 wingGlowQueue 合成后 flush**（原版 DrawData 常色不受光照——合成前画会被乘光压暗）。曾全画在合成前=暗环境整体偏暗。
- ★ **VanillaDust 引擎**（src/fx/VanillaDust.ts）：NewDust 抖动/帧映射（type≥100 X−1000·Y+30）/fadeIn=生长目标语义（0<f<100：+0.03/t 至超转衰；else −0.01/t）/261·264·182 专属段/重力+0.1/缩没 0.1 失活/GetAlpha+GetColor 消费表/双 pass 绘制（lit 前合成+全亮{6,15,59-64}后合成）/光收集推 LightingEngine。
- ★ **翅膀尘埃全量**（Player.wingFx）：WingAirVisuals 10 款（10/34/51/9/6/5/26/37/29/31）+帧内尘（4 喷射音 Item13+烟雾、30 双环 229、33 眼色 182+克隆、45 Item24+43、29 烟、47/49/50 三函数 justSwitched 尘爆）+滑翔 26/37+28 微光 addLightAt。探针 34 型飞行 maxDust=11。
- ★ **47/49 行锚**：playerBodyRow 复算+HEADGEAR_ZERO_ROWS{7,8,9,14,15,16}→Y=−22/其余−20。
- ④ tryKeeping 锁存=Click 模式专属（Player.cs:361 默认 Hold → :24985 恒清零）→ 默认设置下 controlDown 近似即原版；Click 设置项本身未移植（设置系统级）。
- ⑤ downDash=isPerformingJump_DownDash：5465 手持触发（:13978），跳跃变体未移植（跳跃系统级）→ 恒 false 与现状一致。
- 残留（源头不可得/引擎级）：44 HallowBoss HLSL 不在反编译源（Extra_171 静态直画=女皇先例）；extra38 暗环境 tint 取满档（读侧光照 API 未暴露）；49 光照门 z 恒 1；45/38 残影 A=0 是原版死画（跳过=1:1）；stealth/cWings 染色全局未建模。
- 声音：rocketJet=Item_13（妖精翅）/starboardJet=Item_24（45）入 SfxName（wav 已在 public/sounds/）。

**残留清零轮（2026-08-13 三轮，/goal 不能偏差 追单后）——上轮"源头不可得"全部处置**：
- ★ **读侧光照**：LightingEngine.lightAt 已有（:166，0-255/[0,0,0] 语域——并行会话所加，勿重复定义否则 tsc 重复方法报错）→ GameHooks.lightAt：49 Heroicis 门 z=Remap((max+min)/2/255,0.2,0.4,0,1)（:30166-30192 精确移植）；28 extra38 tint=0.5×L×armor+0.5 逐通道（renderer.lighting 直读，免疫/星璇 stealth 并入）。
- ★ **44 彩虹重上色**：Extra_171 **纯灰度掩膜实证**（PNG 解码采样 180 灰/0 彩——直画=灰翅膀=真偏差）+Extra_156=横向彩虹渐变调色板（512²）+uTime=GlobalTimeWrappedHourly（MiscShaderData.cs:91）。rainbowSlice=掩膜灰度×彩虹行（时间滚动 0.25 周/秒；采样映射/滚动率是 effect 二进制语义取近似并注明）；cWings 染料在 RT 输出后再套（:1033 同链）。探针彩色占比 0.5354。
- ★ **stealth 视觉管线**（PlayerDrawSet :1523-1660 → vanillaWingVisuals.stealthFactors 纯函数+单测）：3106 变态刀/蘑菇矿 settled=(1+s'·10)/11、armor×s'、skin×s'²；星璇 settled=s'、secondColor=Lerp(White→(0,0.12,0.16),1−s')。body doll 烘焙单层整体×s'²（armor/skin 分层不可分，登记）。叠画逐款：34/40/51×settled、43/50×settled²、23/27/30×settled、38×settled、47 A180 iff settled==1、22 火焰逐次平方累乘（:681）。Player.stealth 字段本就存在（蘑菇矿蓄能/星璇双击↓/变态刀 PvP）只是渲染层零消费——本次接入。
- ★ **cWings 染料**：tools/extract-dyes.mjs ← DyeInitializer.cs → vanilla-dyes.json **116 条数据 1:1**（13 基础色×4 变体：base/黑+12/亮+31(色×0.5+0.5)/银+44；直接 68 条渐变/亮度/活火/反射/HallowBoss 等；不变量：BindShader 计数+锚点色抽查）。消费链 Player.wingDyeVid()（armor[0..19] 最后 wingSlot>0 → dye[i%10]，vanity 胜出，:9306-9312+:9417）→ dyeEmulationOf 仿真族（solid=BT.601 灰度×色+sat 回混/bright=×色/gradient=lerp(color,secondary,lum)）→ Renderer 全部翅膀 DrawData 套染料（lit 主/全亮主/彩虹层/全部叠画/Betsy 8 片）。**注意：全部染料技术（含基础 ArmorColored）都是 effect 二进制——C# 层只有 (技术,色,饱和度) 元组，像素公式是近似**；~35 条特殊染料登记为 effect 缺口。UI 染料槽可达（拖放入槽）。
- ★ **45/38 A=0 残影石锤**：1405:535 与 1456:744 同为 `Color(70,70,70,0)`——两版一致非反编译错误，XNA A×float 归零死画，跳过即 1:1。
- **leashedEnv 解锁（并行会话在途 bug）**：afterWorldLoad（:2073 respawnAll）在 player 构造前调 leashedEnv 读 .cx → **崩所有会话的进世界链路**；最小修复=playerCx/Cy 空守卫 `this.player?.cx ?? 0`（player 存在时语义不变）。
- 验证：wing-visuals.test.ts **40/40**（+stealth 三分支/染料展开/公式/wingDyeVid vanity 胜出 4 用例组）；探针 **21/21**（⑩ 彩虹 0.5354、⑪ 染料红像素增量 816、⑨ diff=10886、⑦ 尘=13）；wing-catalog+wing-flight 46/46 共绿。探针注意：run-diag 120s 上限不够时直接 node 跑；空 headless profile 每次都要建角色+世界。

**四轮 FX 二进制真值批（2026-08-13，/goal 追单：停钩四异议全清零）——染料/HallowBoss 不再有任何近似**：
- ★ **PixelShader.cso 反汇编链**：`terraria-assets/PixelShader.cso` 是 XNA4 编译 D3DX effect（头 0xBCF00BCF；MojoShader mojoshader_effects.c :976-1076 容器解析 1:1；SM2 字节码 + CTAB + PRES preshader）。`tools/disasm-fx.mjs`（反汇编器，--json 导出）→ `src/data/fxPixelShader.json`（63 pass 全量：指令 token + preshader 预解码 + CTAB 符号）。解码铁律：comment size 字段=**数据** DWORD 数（不含自身 token）；CTAB 偏移基准=Size 字段处、CINFO=20B（u16 打包）、名字偏移 rel start；preshader 子块四字符在 comment+4、**dst=末位 operand**、PRSI tokens[7] 以 fourcc 为 [0]；**texld=opcode 0x42**（非 0x40）；CMP=0x58；REG_TYPE_SAMPLER=10（mojoshader 自有枚举）；**writemask 位序 1=.x…8=.w**（曾解反致 max/min 错乱）；replicated swizzle 无后缀打印易误读——以解释器为准。
- ★ **SM2Effect 解释器**（src/fx/SM2Effect.ts）：decodeProgram→execPixel 逐指令执行 + preshader VM（FXLC）+ uniform 注入（ArmorShaderData/MiscShaderData.Apply C# 侧）。oC0=UNORM 钳；texld ctrl 全 0（实证）；s0=被染图、s1 wrap（HallowBoss）/clamp。金标：ArmorColored 白+红(uSat **1.2** C# :29)= (1,0.9167,0.9167)、(0.2,0.2,1)→(0.9867,0.1167,0.1167)——**真实公式与直觉迥异：luma=(max+min)/2 非 BT.601、着色量=range 调制、灰像素保亮度**（旧近似公式全废）。
- ★ **44 彩虹翼真链**（PlayerRainbowWingsTextureContent.cs）：主纹理=Extra_171（86×434=Wings_44 同构）经 MISC "HallowBoss" pass **烘焙一次缓存**（s1=Extra_512?? Extra_156 wrap、uTime=进程秒%3600=Main.cs:16777）；pass 公式=ramp[fold(灰度+uTime),**0.5**]×A（y=c1.x=0.5 非 0.8）；绘制再套 cWings。染料 4778=ArmorHallowBoss pass：ramp[fold(SUM/2+t/2),0.5]×0.8+原色×0.2。resetFxCache 退出世界清（contextlost 归零）。
- ★ **stealth 分层落地**（PlayerDrawSet.cs:1523-1651 精读）：3106/蘑菇矿 armor **R/G/A×s' 且 B×settled**（:1539-1541 隐藏甲偏蓝亮怪癖！）、皮肤/发/眼/衣着 RGBA×s'²；星璇 armor RGB×Lerp(White→(0,0.12,0.16,0),1−s') A×s'、皮肤×s'²。compositePaperDoll opts.layer='skin'|'armor'|'armorNoHead'（腿甲/身甲槽在 skin 层留空=原版 else-if 替代语义）+ tintRGBA 逐通道（mul 量化 1/128 防缓存爆）。doll 双层绘制：skin×s'² 下、armor×s' 上。
- ★ Reflective uLightSource=ReflectiveArmorShaderData.Apply 1:1（4 点 lightAt 梯度→伪法线，Z×0.6；bodyRotation 未建模恒 0 登记在 Renderer 注释）。
- vanillaDyes.ts 重写：dyeApplyOf(vid)→{tech,uniforms,needsImage1}，applyDyePass=SM2 执行；EMULABLE/effectDyeIds/applyDyeEmulation 旧近似全退役。全部 116 染料有可执行 pass（测试断言）。
- 验证：fx-sm2.test.ts **10/10** 金标 + wing-visuals 64/64 + 探针 **23/23**（⑩ 0.4938、⑪ 增量 837、⑫ stealth 分层 diff=4283）。

**终轮 review 补修（2026-08-13 五轮，四缺陷全闭）**：
- ★ **t0/s0 表空间映射**（真缺陷）：渐变族按 `t0×uImageSize0−uSourceRect.xy` 取像素位（ArmorColoredGradient disasm 石锤）——子矩形烘焙时 t0 必须=全表 UV `(sx+x+0.5)/sheetW`（SpriteBatch 子矩形语义），且 **s0 采样器要做反变换** `(u·W−sx)/w`（vanilla s0=整表纹理,本仓烘焙图只有切片,派生坐标采样同样落在切片内）。runPassOnImageData 加 t0Rect 参数,三 uniform 强制同源对齐。等价金标：子矩形(6×1 表内 x=2 切 4px)≡整图,逐字节差≤2。
- stealthTintCache 补进 clearPaperDollCache（contextlost 后 stealth 态 doll 全隐形隐患）。
- stealth+发色剂层序：甲层(armorNoHead)画在前发/头甲叠层 overlay(false) 之前（原版 躯干甲→前发→头甲）；overlay 内头甲/发层的 stealth 乘数集成点留给发色剂会话（在途）。
- v 寄存器文件 8 分量（v1 安全）。
- 验证：fx-sm2 **12/12**（+t0 等价/敏感性 2 例）、wing 套件 **81/81**、探针 **25/25**（+⑬ 渐变染料 diff=17840）。
