---
name: webgl2-phase1-port
description: "WebGL2 一期完成(GLSpriteLayer+背景族+全屏地图,像素级对拍);y翻转两次翻车+回归守卫测试;texSubUpdate 9参/#362CFF/纹理键碰撞三大坑全记录"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-18T05:26:21.529Z
---

2026-08-18 一期完成落地(docs/webgl2-migration-plan.md 计划表,#3/#4 待二期)。

**形态**:GL 离屏画布 + 调用方在原 2D 链同一时序 `ctx.drawImage(glfx.canvas,0,0)`
单次合成——层序/透明度零改动。共享模块 `src/render/GLSpriteLayer.ts`
(quad/纹理LRU/双sampler/fillQuad/texSubUpdate)。#1 BiomeBackground 走
BGBlit 接口(2D=CanvasBgBlit 原语义/GL=GLBgBlit),`?bggl=0`/`?mapgl=0` 逃生
门(bgGlEnabled/mapGlEnabled 可运行时切,探针 A/B 用);#2 drawFullMap 四段
(MapBG/卷轴/地图/迷雾)GL,小地图纹理按 Minimap.flushedPixelRects 脏区增量
上传,迷雾按 version:row 键换纹理;MAX_TEXTURE_SIZE 守卫(8400 超限回 2D)。

**对拍结果(同会话 A/B,真实大世界存档 loadJson)**:背景 平均Δ0.02/Δ>8 占
0.1%;地图 Δ=0 完美。方法:暂停冻结→同屏切后端→主画布网格采样(对照组
2D-vs-2D=0.1% 验证冻结有效)。

**四大坑(全修+守卫)**:
1. **clip-space y 翻转两次翻车**(canvas2D y向下 vs GL y向上):修=`gl_Position.y
   = 1.0 - screen.y/uCanvas.y*2`;曾两次被并行会话写回旧版静默丢失(用户两报
   倒置)——**守卫=tests/gl-layer-regression.test.ts 源码级断言锁定五项
   (y翻转/mip采样器/generateMipmap/预乘上传/texSub 8参),丢任一立即红**。
   ★并行会话共用文件,关键修复必须配回归测试,否则"修好了"会被静默蒸发。
2. **texSubUpdate 9 参重载**:WebGL2 的 DOM 源重载只有 8 参(无宽高)——
   Chrome 把画布【左上角 w×h】贴进目标区 = 地图脏块渐变 #362CFF 退化块
   (用户实报+三层源采样定罪:主画布坏/小地图画布好/迷雾好)。修=抠 scratch
   画布走 8 参。**WebGL2 overload 陷阱:DOM 源取子区无原生 API**。
3. **纹理缓存键碰撞**:ImageBitmap 无 .src,键退化为"宽x高"——森林 t0/t2 同
   1024×699 共用一张纹理=满屏 Background_50 平面色(沙漠层尺寸各异侥幸完美,
   误导排查半天)。修=WeakMap 实例自增 id(同 PaperDoll/UISpriteBatch 旧坑)。
4. **mipmap 透明边缘黑化**:直 Alpha 上传+mip=透明像素 RGB(黑)混进边缘;
   修=UNPACK_PREMULTIPLY_ALPHA_WEBGL=true 预乘上传(mip 平均预乘=能量正确,
   shader 公式无需变:premul×tint×uAlpha ≡ straight×tint×a)+LINEAR_MIPMAP_LINEAR
   对齐 Skia 盒式降采样。

**基线(子代理 traceG 分析)**:常规 9.5-11.3ms/帧,背景族 1.5-2.6ms/帧;
地图时段 13.48ms(+20%)、GPUTask 52.3/帧(常规 15.9)。预期 #1 后 -1.5~2.5ms
/帧、#2 地图时段与常规持平/GPUTask ≤20。**restore 族(Canvas2D 状态机)占
非 idle 34% = 下一优先级独立优化点,不依赖 GL**。

探针族:_glpar(跨会话)/_glpar2(同会话A/B)/_glctrl(对照组)/_glflip(正式
对拍)/_glrow(行扫描)/_gldeg(退化复现)/_gltex/_glband/_glstate2/_glunit
(页内单测)。loadJson 探针存档 public/tmp-*.json 用完必删(会打进 dist)。

相关:[[imagebitmap-root-cure]]

**五号坑(2026-08-18 补)**:TEXTURE_MAG_FILTER 只接受 NEAREST|LINEAR——
mip 档(LINEAR_MIPMAP_LINEAR)传给 MAG = INVALID_ENUM 警告 + MAG 落回
sampler 默认 NEAREST(放大采样错过滤,地图 zoom>1 细微画质差)。修=mkSampler
分 min/mag 两参;守卫测试同步锁 MAG 恒 LINEAR。

**六号坑(2026-08-18 二次崩溃会话)**:①GLSpriteLayer 漏挂 Renderer.dispose
世界切换清理链——连续读档逐次叠满 LRU=GB 级显存打爆(contextlost 风暴 26 万次/
tab 3.4GB/JS 堆 1GB,chunk 自适应沉到 64 底);同款病 2026-08-10 在 chunk 画布上
修过,新增资源池必须同步挂 dispose。②LRU 按条数(96)→按字节(192MB)+记账;
③熔断器固定 8s 冷却=永久振荡(期满放行→再抖→再熔),改逐次翻倍 8→16→32→60s
封顶+稳定 60s 回落;④小地图/迷雾纹理 noMip(8400×2400 每脏块全链 mip 重生成
=巨量 churn,且 MIN/mip 永不被采样);⑤迷雾纹理 version:row 换键→稳定键+行带
texSubUpdate(探索期换血烧穿预算)。守卫测试扩到 7 项。

**泄漏终审(2026-08-18 用户"确保无其他泄漏点")**:全量资源池扫一遍,
补两处——①mainFlow.enterGame 曾直接 `game = g` 替换引用:旧 Game 的 rAF
循环靠每帧自注册永生,running 唯一关断入口是 destroy()——任何不经
quitToMenu 的直达进图路径(未来新增)都会旧实例永生叠加;兜底=enterGame
先拆仍存活的旧实例。②ChunkCache.MAX_CHUNKS 自适应收缩曾【无恢复点】:
熔断沉到 64 后所有后续世界永远 64(视野烘焙跟不上);修=afterWorldLoad
回满 384(真撑不住熔断器会再自适应,冷却已升级不振荡)。
已审清白池:GLSpriteLayer scratch/WHITE_PX(单例)、BG_TEX_ID(WeakMap)、
bmpFailStats/Warned(按唯一文件名有界)、tryBitmapUpgrade 重试(≤3,≤70s
瞬态)、breaker 定时器(有界)、uiTexCache(随 Renderer 亡)、
BiomeBackground imgs(按群系样式有界,随 Renderer 亡)、minimap
flushedPixelRects(cap 128)、imglog(flag 门,dev only)。

**附带两修(2026-08-18 晚)**:①MAX_CHUNKS 恢复点曾写
`this.chunks?.constructor`——afterWorldLoad 头部 chunks 未构造,undefined
赋值即崩(用户进档即崩报);改直引 ChunkCache 类静态。**教训:静态恢复点
别经实例取,时序上实例可能未生**。②资产门槛"卡一下"真相:门槛等的是 SW
status 回包(SW 冷启动+cache.keys() 枚举万条 1-2s),期间 done=0 误显示
"正在下载 0%",trace 实证零实际下载;修=完成态落 localStorage(键含版本),
门槛先查标志秒开,SW 回包实测校准(被清理则撤销标志)。

**全屏地图两修（2026-08-19 用户报"放大到一定程度全黑+背景随缩放变动"）**：①fullMapBgIndex 旧 vy=(cy0+mapH/2)/zoom 是"地图底边屏幕坐标÷zoom"纯错位量→随缩放漂移=背景自己换根因；修=视口顶世界 tile `-cy0/zoom`（原版 screenPosition.Y 语义，:55804 深度档其余档全玩家墙/群系），tests/fullmap-bg-index 4 绿（同视口顶 6 档 zoom 恒同档）。②MapBG*+Map.png vui 懒加载首开图几百 ms 未就绪→近黑底闪（很可能被用户归因为"放大变黑"）→进世界 preloadUiPrefix(['MapBG','Map.png']) 预取。黑屏本体六路复现不中（直调/全帧/DPR2/真滚轮+缓动/±雾/探索泡 0.5→6）+截图证实 z=6 内容正常——若残留需 F5 现场报告。★教训：canvas 像素采样必须用 canvas.getBoundingClientRect 换算（曾用 viewport CSS 坐标直乘 dpr→采到底边 UI 区，"变暗曲线"全是伪影）。

**全黑终局（2026-08-19 二轮，用户确认背景修好但放大全黑仍在"只剩头像"）**：头像=2D 后画层 → 整块 GL 合成黑。显微镜探针定罪链：CPU pix 93% 彩色+纹理 isTexture+重传后仍黑，仅大 dst 黑小 dst 正常 → **GPU guard-band 裁剪**（dst 伸出画布数万 px 时部分驱动整图元丢弃）。三层落地：①`Renderer.clipMapQuadToView`（mm/fog quad src/dst 同比回裁进画布——根因修复）；②GL 合成哨兵（end 前 readPixel 中心 1px+CPU explored 对照，连续 3 黑帧→60s 内 2D 兜底——GLSpriteLayer.readPixel 公开 API）；③2D 兜底 `_fm2dDirtyAt` 脏块门重灌（曾一次性建死：建画布时条带重建未完成=永远空图）+F5 `fullMapDiag` 段（路径/探针/bg·scroll 解析/CPU 像素/centerTile）。★headless 无头环境 GL+2D 大图都渲染异常（233=MapBG 羊皮纸透出）——无头结论只可信"相对变化"，绝对正确性要真机截图；2D 兜底是 GL 化前跑了几个月的原始路径，真机可信。

**全黑真凶终定罪（同日三轮）**：用户回传哨兵日志 **zoom 1.37 即黑**（非高倍专属）→ 与 `smooth: fm.zoom>=1` 的采样器切换线完全重合 → 查 `samp.linear = mkSampler(LINEAR_MIPMAP_LINEAR, LINEAR)`，而小地图/迷雾纹理 `noMip=true` 无 mip 链——**WebGL 采样器对象覆盖 texParameteri：用需 mip 的 MIN_FILTER 采无 mip 纹理 = 纹理不完整 → 采样恒黑 (0,0,0,1)**。z<1 走 nearest 档所以"缩小恢复"；此前"小矩形正常"对照恰好 smooth:false(nearest) 把我误导去 guard-band。修 = `samp.linearNoMip(LINEAR/LINEAR)`，quad()/tileX() 按 `e.mipped` 分流采样器；探针全档 0.5→6 中心全内容色、哨兵零触发。★GL 铁律：**sampler 对象与纹理参数是两套——incomplete 判定看生效组合**；noMip 纹理必须配无 mip 的 MIN_FILTER。clipMapQuadToView/哨兵/2D 重灌保留作加固与遥测。

**迷雾消失排查（2026-08-19 四轮，未复现→遥测定案）**：用户报"迷雾消失没按 F4"。三方排查：F4(main.ts:220)/devMode(mainFlow maybeDev explored.fill(1)，报告 invNonEmpty 仅 3 格=排除)/markExplored r28 是 explored 仅三写入方。渲染侧 4200×1200 同尺寸+1.25% 覆盖率探针全档绿（远角恒雾色 5,5,8）。fullMapDiag 增 `exploredCoverage`（步 997 抽样）+`cornerTileExplored.canvasPx`（未探索角合成像素：雾色=正常/内容色=渲染丢雾/coverage≈1=数据全亮）——一份报告三分支定案。疑点存档：用户旧会话可能按过当时"失效"的 F4（修好后 fill 生效）或存档 explored 段已全 1。

**远景背景 Y 偏下（2026-08-19）**：`camTopY = cam.y - viewH/2/1`——**/1 是缩放占位符**！zoom 1.25 下屏顶世界 Y 差 viewH/2×(1-1/zoom)≈86px → num3 偏大 → bgTopY=num3×topA+topB 整体下移 ~70px（实测远山档 476.4 vs 旧 546.4）。修 = `cam.y - viewH/2/cam.zoom`（Main.screenPosition 语义，X 同式 camLeftX）；地表深度门同改屏顶；横向 bgStartX 改 vanilla 式 `-ieeeRem(camLeftX×parallax,w)-w/2-w`（比正模多退一整块，loops ceil+3）；ieeeRemOf 提为类静态。tests/surface-bg-parallax 3 绿（断言修正档 476.4/594.8 出现+旧档恒不出现）。Cam 接口加 zoom 字段。★教训：占位符 `/1` 编译不报错——写死魔法数替代真实语义时 grep 一下语义来源。
