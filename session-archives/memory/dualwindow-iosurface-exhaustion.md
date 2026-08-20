---
name: dualwindow-iosurface-exhaustion
description: "双开崩溃根因=GPU进程IOSurface张数耗尽(字节无关,16x16也失败)非显存预算;force-gpu-mem-available-mb=cc tile预算纯安慰剂;--disable-gpu全域软渲染双窗0失败"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-19T07:22:41.948Z
---

2026-08-18 用户实报"npm run play 冷启 Chrome(带 --force-gpu-mem-available-mb=16384)
双开联机依然 GPU 爆"→ 三线取证 + 三组 A/B 对照,机制钉死。

## ① 旗标是安慰剂(Chromium 源码实证)
`--force-gpu-mem-available-mb` 定义在 `third_party/blink/common/switches.cc:104`,
官方注释:**"Sets the total amount of memory that may be allocated for GPU
resources in cc"** —— cc=合成器,只管 tile 光栅资源预算。转发链
`render_process_host_impl.cc:3955`(blink::switches 转给渲染进程),与画布后备
存储/WebGL 纹理/SharedImage **零关系**。Chrome 151 二进制里
`force-gpu-mem-available-mb`/`force-gpu-mem-discardable-limit-mb` 字符串都还在
(strings 实锤,开关没删但也不管我们的故障)。**教训:开关存在≠开关管用,
必须找到消费点读注释。**

## ② 真根因=IOSurface 张数/内核资源耗尽,字节无关
双窗探针(puppeteer 系统 Chrome 同实例双 tab 大世界)stderr 铁证:
```
ERROR:ui/gfx/mac/io_surface.cc:273] Failed to allocate IOSurface of size 16x16.
ERROR:...iosurface_image_backing_factory.mm:386] CreateSharedImage: Failed...
ERROR:...command_buffer_proxy_impl.cc:488] GPU state invalid → 上下文死
```
**16x16(1KB)都分配失败**(64GB 机器!)——是按"张"计费的内核资源(mach
port/fileport 类)耗尽,非显存字节。FD 排除(lsof GPU 进程仅 36 个,系统上限
245k/进程)。每张加速画布后备=一个 IOSurface;双窗把 GPU 进程(共享)的张数
顶穿→分配失败→contextlost→恢复重分配→再失败=风暴。单窗不炸=张数在阈下。

## ③ 三组双窗 A/B(headless 同负载,scripts/_dualgpu-probe.mjs)
| 模式 | contextlost | IOSurface 失败 | 熔断 |
|---|---|---|---|
| GPU 模式+play 旗标 | 9 | 27 | 3 |
| 游戏内 renderMode=cpu | 7 | 6 | 2 |
| **--disable-gpu 全域软渲染** | **0** | **0** | **0** |
- renderMode=cpu 只减 4.5×:chunk 画布 willReadFrequently→SHM 后备,但主画布
  合成链仍产 IOSurface(印证"willReadFrequently 后备仍进 GPU 进程"旧结论)。
- 游戏自身熔断器有效:10s 内 3 丢失→冷却+chunk 上限缩 64→风暴不再升级(两轮
  GPU 模式都是"受控慢渗"而非 16k/s 真窗风暴;headless 视口小+熔断早介入)。
- `--disable-gpu` 全干净=连合成器都不产 IOSurface。已做成 `npm run play --soft`
  (SW_PLAY_SOFT=1):双开联机测试就绪档(代价帧率降,单窗别开)。

## ④ 结论/出路
- **没有任何 Chrome 旗标能救 GPU 模式双窗**(overlay 开关已从 151 移除)。
- 双开测试三选:**npm run playsoft**(最稳,见⑤)/ 第二窗 renderMode=cpu
  (可用但有残留)/ 单窗口双世界(正解,方案已给用户:同源 2×2px iframe +
  headless Game + bot,GPU 开销恒等单窗,等待用户拍板落地)。
- 游戏侧最大单点=**chunk 烘焙画布张数+churn 双料元凶**:每 chunk=墙层+tile 层
  **两张** 256² canvas(renderChunkInner 新建);稳态 35 chunk=70 张;移动期
  flushDirty 4 chunk/帧=**每帧 8 张新画布**(GPU 进程 ~480 次 IOSurface
  分配/释放/秒,双窗翻倍)。**chunk atlas 打包**(4×4 cell/1024² 页,墙/tile
  各一摞;重烘焙=原位重画 cell 零画布生命周期)→ 活张数 70→~10、churn→0,
  是 GPU 模式下同方向的正手;终局=渲染器 v2(WebGL2 纹理化)。
- 单页稳态基数:DOM canvas 3 + chunk 70(35 对) + vimages 231(CPU 位图)。

## ⑤ --disable-gpu 有头生效性验证 + npm 参数坑(2026-08-18 用户实报)
用户反馈"play --soft 启动后 chrome://gpu 仍全硬加"→ 两层原因:
1. **npm 吞参**:`npm run play --soft` 的 --soft 是 npm 自己的配置,不传给脚本!
   必须 `npm run play -- --soft` 或 env SW_PLAY_SOFT=1。已加 **`npm run
   playsoft`** 专用脚本免坑(package.json)。
2. 有头 Chrome 151 实测(puppeteer headless:false + UNMASKED_RENDERER):带
   --disable-gpu → **WebGL 上下文直接拿不到**(全禁,旗标有效);无旗标 →
   ANGLE Metal Apple M5 Pro。用户那次 = 旗标没进进程(1 的锅)。
   chrome://gpu 全绿即旗标未吃到;chrome://version 看 Command Line 可复核。
   探针 scripts/_disgpu-check.mjs。

## ⑥ 游戏侧优化落地(2026-08-18 晚,用户拍板"开始大型优化")
**三刀全落地,探针验证:**
1. **chunk atlas 页化**(ChunkCache.ts):每 chunk 2 张 256² 画布(稳态 70 张/
   满额 768 张,重烘焙=新建)→ 墙/tile 各一摞 1024² 页(4×4 cell),cell 池
   复用,重烘焙=clip+translate 原位重画。活张数 446→28(223 chunk 实测);运行
   期画布创建≈0(回头路二遍 9 张 vs 旧每遍 ~6000)。★跨格外溢绘制(墙 EXT=1/
   树 EXT=6 负坐标)必须 clip 在 cell 内;tintRegion 区域坐标要页内绝对 ox+lx*TILE;
   ChunkPair 增 sx/sy/cell,Renderer drawChunkGrid 改 9 参源矩形(4 参=整页
   误绘,类型合法的静默 bug!)。bakeChunkInto(cell<0)同函数喂独立画布=E2E
   逐字节对拍 8/8 的构造保证。dispose=唯一毁页点(setRenderMode→cbOnGpuRecover
   →dispose→按新模式重建)。
2. **cloudTint 染色画布池**(SkyRenderer.ts:1404):canvas 出生栈普查实锤的
   最大隐藏工厂——键含逐帧漂移 RGB+ImageBitmap 无 .src(恒 undefined 跨纹理
   碰撞)→ **每帧每云新建画布 ~340 张/秒**(12s 移动 4091 张,泄漏大扫除年代
   漏网:活集被 64 上限"界定"但出生率无界)。修=色键量化步进8+WeakMap 纹理id
   +LRU 淘汰画布进 free 池原位重画 → 出生归零。
3. 普查残余良性:frameHasContent 帧探测(willReadFrequently=SHM 不占 IOSurface,
   首见有界)/iconUrl/tintedSprite ≤6 张/12s。
**验证**:_chunkatlas-probe 4/4(对拍 8/8 逐字节+回头路 churn≈0+页数界);双窗
GPU 对照:IOSurface 失败 27→8(-70%),残余失败尺寸=1280×800(视口/合成器
swapchain,游戏外);contextlost 计数 7→18 属两页分布变化(B 基线全程 0 = 分配
顺序偶然),无风暴升级。**教训:①"泄漏审计"必须量出生率不只活集——池化
上限会掩盖 createElement 风暴;②canvas 出生栈普查(createElement patch+聚栈)
应成为渲染改动的常规探针;③类型合法 ≠ 语义正确(4 参 drawImage 画整页)。**
探针:_chunkatlas-probe.mjs(四项)/_canvasborn-probe.mjs(聚栈)。

## ⑦ review 三修 + canvas 哨兵(2026-08-18 深夜,用户令"review 避免再发生+建早期抓取")
**自审揪出 2 真 bug + 1 效力回退:**
1. **油漆 pass 双重偏移**:bakeChunkInto 挂 translate(ox,oy) 而 tintRegion 回写
   用页内绝对坐标 → 落 (ox+px,oy+py),ox>0 的 cell 油漆被 clip 静默吞。对拍探针
   没抓到=新世界无油漆(paint 全 0)→ **对拍必须含油漆**(探针①' 涂 202 格红漆,
   cell=5 偏移位 vs 独立目标 diff=0 锁死;修=tintRegion 读写坐标分离
   readX/readY+writeX/writeY)。★教训:对拍覆盖面必须包含"改动触碰的每个 pass",
   空数据路径的逐字节一致≠全路径一致。
2. **cloudTint 池化复用双坑**:同尺寸复用残留上一轮 destination-in(首绘变擦除)
   +旧像素透过透明区串色 → 首绘改 globalCompositeOperation='copy' 整体替换;
   free 池封顶 8(工作集收缩时 surplus 弃,防池自身无界)。
3. **软收缩效力回退**:shrinkChunks 只还 cell 不放页(每页 2×4MB 背板滞留)→
   pageUsed[] 每页计数+trimFreePages() 尾部空页回收(Game.shrinkChunks 接线);
   bakeChunkInto 拆 bakeChunkBody+try/finally restore(异常逃逸=共享页残留
   clip+translate,下次烘焙 2×错位——独立画布时代异常自含,页化后必须显式复位)。

**CanvasWatch 常驻哨兵**(src/render/CanvasWatch.ts,main.ts 装载,?cwatch=0 静默):
patch createElement 计数+聚栈,console.warn 带出生栈样例(进 __swWarns/F5);
renderLog/F5 快照新增 canvasWatch 段。★判据三轮真机标定才收敛(哨兵标定笔记):
①短窗速率(20/s×2 窗)误伤正常跑图(首见帧探测单窗 30/s);②滚动总量(2000/60s)
误伤进世界洪峰——SpriteAtlas.hardAlpha 一次性单窗 1621 张与事故 1700/窗不可区分;
③终版=【连续窗双档】:≥300 张/窗连 3 窗(急性)/≥100 张/窗连 6 窗(慢性),
一次性构建 1-2 窗即衰减天然免疫,真机零误报。哨兵自身初版还有 lastWarnAt=0
把首报挡进冷却的 bug(单测当场抓住,改 -Infinity)——★哨兵也要被测。
另:hardAlpha 进世界单窗 1621 张是合法一次性构建(表硬 alpha 处理,常驻资产),
非泄漏;真泄漏的判别特征是逐窗持续不衰减。
E2E:_chunkatlas-probe 5/5(含油漆对拍)+ _canvasborn-probe 增哨兵装/静默验证
(栈顶多一层 CanvasWatch wrapper 属预期)。

## ⑧ 云染缓存二轮:真 LRU + cap 24(2026-08-18 用户"云染缓存在干啥,优化一下")
帧扫描探针(_framescan-probe:drawImage 按帧聚去重源)实测常驻账后点名:
cloudTintCache FIFO+64 把历史冷桶全留下(cap 打满 64 张常驻画布),而真实工作集
= 同屏云色桶 ~10-16。修:命中重插 Map 尾(真 LRU,冷桶先走)+ cap 64→24
(miss 重染成本=3 次 ~200×100 drawImage,超工作集也无感)。实测 64→24,
每帧绘制源不变(静止 11/移动 ~36 张),churn 仍归零,哨兵零误报。
★帧扫描数据留档:每帧绘制源 canvas 静止 p50=11/移动 ~36(移动段含烘焙表源
混入 ~25 张);bitmap 源 7(CPU 侧不占 IOSurface);常驻账 DOM 3+chunk 页 12
+云染 24+单例 ~5。四层口径:绘制源/常驻持有/每帧新建(≈0)/bitmap。

## ⑨ 云透明根因+哨兵首战+云 GL 化(2026-08-18 深夜二)
**"好多云不渲染"根因 ≠ 渲染层**:drawCloudPass 的 globalCloudAlpha 曾接
`max(wr.cloudAlpha, 墓园×0.92)×atmo`——wr.cloudAlpha 是【雨云浓度】(晴天恒 0)
→ 晴天云全透明。原版真身(反编译实证):Main.cs:58752 `num5 =
SkyManager.ProcessCloudAlpha()×atmo`,ProcessCloudAlpha = 1×Π(激活
CustomSky.GetCloudAlpha()),默认恒 1,仅月总/四塔天空 override 1-fade
(MoonLordSky.cs:72),**墓园不压云**。修 = globalCloudAlpha = atmo 直取。
★教训:注释引用的公式要回反编译核对——"max(cloudAlpha,墓园)"是把某 CustomSky
内部式误当全局门;该 bug 期间云从未显示过,坐标/染色从未被真正检验。

**canvas 哨兵首战告捷(用户真机)**:生产构建抓到 37-63 张/秒持续 30 窗,
压缩栈 new Ap→Ni.render→rt.render。定位 = **TileFlames._tintCache**:键含
火光连续 rgb(光照驱动) + imgId 裸读 .src(ImageBitmap 恒 undefined→跨表串色,
注释声称"src 唯一"在 bitmap 时代失效) + 超 512 整表 clear(下帧全量重烘雪崩)。
修 = WeakMap 实例 id + rgb 量化步进 8 + 逐条淘汰。tintedSand 查实 v 已 8 档
量化(键有界)非凶手。

**云 GL 化落地**(用户拍板"直接 GL 化,不支持再回退 canvas2d"):
- 新 `src/render/CloudGL.ts`:WebGL2 逐精灵批绘(顶点 [x,y,u,v,r,g,b,a],
  CPU 预乘顶点色,fragment `t×vCol` = 原版 spritebatch.Draw(Color) 精确色语义);
  一张视口大小离屏画布同帧双 pass 复用(远云 sky.draw 内/近云 biomeBg 后,
  pass 间 clear);预乘上传+mipmap+LINEAR;preserveDrawingBuffer 同款合成。
- SkyRenderer.drawCloudPass 双轨:GL 主路径(quad 推送)/2D cloudTint 兜底;
  ensureCloudGL 死亡 5s 退避;Renderer.setRenderMode/�dispose 接线
  (cpuRender 关+释放);`?cloudgl=0` 逃生门;quadsLastPass 观测量。
- 验证:GL 路径截图 6 朵云正常;?cloudgl=0 兜底 3 朵云颜色正常无串色
  (copy 修复实证);哨兵静默;26 测试绿。
- 收益:GL 路径下 cloudTint 缓存归零(24+8 画布→1 张 GL 画布+纹理恒定);
  量化近似消失。

**★仪表教训(两次误报"没云")**:①"覆盖度"用边缘检测(邻域差分)——平滑
色块云对它几乎不可见,必须用"与期望渐变的偏差"或直接看图;②"取最大画布"
在面积平局时抓错(主画布与光照画布同 1280×800)——必须 renderer.canvas 直取;
③GL readPixels 的 y 原点在**底**(顶行=height-1),两次采错行。
**视觉问题的终极判据 = 看截图(Read 图像文件),指标只是导航。**

## ⑩ 哨兵二捕:BiomeBackground 昼夜染色(2026-08-19,用户再报 61/s 急档)
用户真机新构建再报:≥300/窗 3 连,61/s,栈 = 普通函数 `Dp←Wi.render←rt.render`
(上一轮 `new Ap` 是构造器形态,TileFlames 修复虽对症但非此栈真身)。真凶 =
**BiomeBackground.drawTiledTinted**:键 = `im.src`(bitmap 恒 undefined)+ 昼夜
tint `.toFixed(2)`(晨昏连续漂移→每帧新键)+ `>64 整表 clear()`(清光全重烘
=永远 miss 的雪崩)。触发条件 = 晨昏段(tint≠(1,1,1) 才走烘焙;白天直画)。
修 = texId + tint 步进 8 量化 + 逐条淘汰;黄昏强制复现(CB_DUSK=1)实证归零。
**同族清剿**:全仓扫"键内 .src"→ Portal/PortalGunBolt(帧染色)/
SkyRenderer.tintedFlareSprite(镜头光斑)/GLSpriteLayer.drawRect tag 四处同病
(碰撞型:画错图/串色)→ 统一 `src/render/texId.ts`(WeakMap 实例 id)接线。
★方法论:①哨兵的栈形态(有无 new)可区分函数/构造器;②"连续值键+整表
clear()"是最毒组合(清光=100% miss);③bitmap 时代"键内 .src"= 一类扫除
模式,已全仓清零,新代码一律 texId()。

## ⑪ 哨兵三捕:tintedSprite 敌怪/掉落物光照染色(2026-08-19,主犯落网)
用户新构建再报(107 连窗≈9 分钟 60/s,暂停中持续,栈 `new Fp` 构造器形态——
BiomeBackground 修复后真凶露脸)。慢加载拉长复现(全部 vanilla 图随机延迟
300-900ms+90s 采样+中途暂停 30s):**Renderer.tintedSprite ← drawEnemy 612 张
/90s**——键含光照染色 color(连续漂移)+ `>1024 整表 clear()` 雪崩(第四个
同族据点,敌怪每个每帧调)。修 = 色键量化步进 8(烘焙用桶内首色,闪白瞬态
不受影响)+ 整表 clear→逐条淘汰。修后 612→4 张(99.3%)。
**"光照染色类"缓存家族至此全部清剿:cloudTint(天色)/TileFlames(火光)/
BiomeBackground(昼夜)/tintedSprite(光照)——共性 = 键含连续漂移的光照
派生色 + 无量化 + 整表 clear 或无上限。新写染色缓存三件套:texId+量化步进8
+逐条淘汰;池化仅高 churn 场景需要。**
探针:scripts/_slowload-probe.mjs(慢加载+暂停 90s 聚栈——暂停中持续 = 渲染
循环类工厂的特征签名)。

## ⑫ 哨兵三捕真凶更正:GLSpriteLayer 初始化失败每帧重建(2026-08-19)
用户纠正"确定是最新构建"点破误判:tintedSprite(方法形态)修复真实但非用户
60/s 的主犯——用户栈 `new Fp` 是【构造器】形态。真凶 = **bg GL 路径的
diedAt=0 洞**:WebGL2 初始化失败(playsoft `--disable-gpu` 下必失败;或
上下文数满被浏览器拒发)时 GLSpriteLayer 构造器 unavailable 且 diedAt=0 →
消费方退避判 `now-0>5000` 恒真 → **每帧 dispose+new GLSpriteLayer(构造器
createElement)= 60 张/秒**,暂停中持续(渲染循环不停),与用户日志全吻合。
dev 复现不了(WebGL2 可用)——须 `--disable-gpu` 复现(canvasborn-probe 的
CB_ARGS)。修三层:①GLSpriteLayer 构造器三处失败分支补 `diedAt=now`;
②Renderer.acquireGL() 统一获取(死亡 5s 退避/初始化失败 30s 闩,bg+map
两处消费点接线);③setRenderMode 回切 GPU 时重置闩。修后 --disable-gpu 下
12s 移动期 ~25 张零重建。
**★教训:①栈形态(有无 new)是硬证据,方法/构造器两条排查线别混;②"复现
不了"先问测试环境与用户差在哪(playsoft!);③退避判据的初值语义(0=永不
退避)要显式审。** 附带:worldgen worker 偶发 "process is not defined"
(pass 58/59 终清理)再次出现,属已知 process.env 进 worker 坑家族,另行处理。

## ⑬ ioreg 检测法不可用
用户转来的报告提 `ioreg -n IOSurfaceRoot -w 0` 数 IOSurface——实测只输出设备
树根,不列 surface 条目(需 root 且新版结构已变),当泄漏检测不可靠,勿依赖。

探针:`scripts/_dualgpu-probe.mjs`(DGP_MODE=cpu/gpu、DGP_FLAGS、DGP_SECS;
renderMode 钉死防 auto 降级掩盖)、`scripts/_canvascount-probe.mjs`(张数普查)。
经 run-diag 跑,SW_ORIGIN 指私有 52xx 实例。

## ⑭ 双开再爆+TintAtlas 染色图集(2026-08-19)
用户实报"昨晚 4-5 开没事,今天 2 开崩"(trace 202MB:GPU 任务全 45µs 碎片=
非算力;console:熔断→冷却→再熔断环+CloudGL dispose 的 INVALID_OPERATION 刷屏)。
同日并行会话正改 worldgen/AI(vitest 32 失败全是他们的种子哈希 checkpoint 中间态,
渲染链测试绿)。

**盘点(_iosurface-inventory/_combat 探针,存档现场)**:静息态 DOM 5 张(主
+光照+探针覆盖层+2 小 UI)+ chunk 页 23-25 张 + glfx 6 纹理 17.9MB;战斗态旧
实现 tintCache 可冲 **1024 张独立 canvas**——按张计费下的头号大户。

**TintAtlas(src/render/TintAtlas.ts)**:染色变体从"每条一张 canvas"合并进
≤4 张 512² 共享页(shelf 行打包+free-list 最优适应分裂+LRU 逐出冷 16 条重试);
★bake 回调在**私有 scratch** 上作画再整块 blit——destination-in/getImageData
等全画布语义绝不能直接上共享页。tintedSprite(乘法族)/lerpSprite(逐像素族)
两族全迁,~14 消费点 drawImage 改 9 参(TintRect{c,x,y,w,h};bake null=超大
精灵/图集满 → 调用方跳过该层兜底)。实测 41 变体=1 页(旧=41 张)。
GLSpriteLayer/CloudGL dispose 补 isContextLost() 守卫(死上下文 delete 只会
刷 INVALID_OPERATION)。

**用户否决跨实例方案**:"不要这种降级的,从我们自己出发"——BroadcastChannel
互感缩预算(GpuBudget)已写完又整体回滚;方向定为**单实例自身减量**。
剩余候选:CloudGL 并入 GLSpriteLayer(省 1 个 GL 上下文+背板)、cloudTint 2D
兜底(24+8)、TileFlames、tombstone/minimap skin 小家族、MAX_CHUNKS 384
(24 页)再评估。

**"染色不是迁 GL 了吗"勘误**:GL 化的是**背景层**(BiomeBackground→BGBlit
uniform,并行会话完成;2D 兜底缓存 64 条)与**云**(CloudGL)。实体侧染色
(NPC colorRGBA pass/物品 color/gore/glow 轨道/鹿角怪/月总 twoPass/血条)必须
逐精灵交织在 Canvas2D 实体链内——GL 层每帧只合成一次,没法逐实体穿插——所以
一直是"每变体一张 canvas"形态,这次才用图集合并。

## ⑮ playtrace 取证档 + 崩溃日志铁证 + 写一次缓存恢复 bug(2026-08-19 午)
**npm run playtrace**(play.mjs --trace):不经 open 直接 spawn Chrome 二进制,
`--enable-logging=stderr --log-level=1`,stderr 落 `game/logs/gpu-stderr-<时间戳>.log`。
Chrome 行自带 `[pid:tid:MMDD/HHMMSS:severity:file(line)]`——DevTools Performance
两份 trace(20s/24.5s)都只录到"健康侧"(呈现持续到录停、无死亡事件,被录页
≠ 崩溃窗),真铁证永远在 stderr。

**崩溃日志钉死**(gpu-stderr-2026-08-19-04-26-00.log):12:26:41.613 一张
**64×128**(角色合成级小图)分配失败→CreateSharedImage 失败→`Restarting GPU
process due to unrecoverable error. Context was lost.`=GPU 进程整死;恢复中
12:26:59 又一张 64×128 再死;12:27:04-07 第三次(108×70/256×104/238×72×2
+ Invalid mailbox ×3)。全程仅 6 次分配失败——张数预算卡死时小图也过不去,
每次失败都杀整个 GPU 进程。

**"崩溃后角色贴图不恢复"根因**:写一次烘焙缓存画布(PaperDoll 角色合成等)
的后备随 GPU 进程死亡蒸发,永不重画——每帧重画的层天然自愈,写一次层全灭。
PaperDoll 的 clearPaperDollCache 早就存在且注释写着这病症,但只挂在进出世界,
**没接 contextlost**。修 = Renderer.onLost(主画布+window 双挂点)首次丢失即
统一失效扫:clearPaperDollCache/tintAtlas.dispose/sky.clearCloudTintCache/
clearAmbientTintCache(并行会话新加的 AMB_TINT_CACHE 同款风险,顺手接)/
biomeBg.clearTintCache/clearTileFlamesCache/tombstoneCache——清前 width=0
先还表面。E2E(合成 contextlost):tintAtlas 5 条/1 页→0/0 ✓。

## ⑯ 第二份崩溃日志 + 基数压缩第一批(2026-08-19 午后,用户拍板 1+3 先做/2+4 登记)
第二场(gpu-stderr-...-04-37-51):启动 34s 即触顶——首败 52×26(HUD 小图)→
**Invalid mailbox ×487 跛行 11s**→恢复分配 5 连败(1088×64/3040×448/1088×864/
32×821/32×545×2)→64×128(角色合成)终败="Restarting GPU process"。与首场差别
=先跛行后死;预算比上午更满。

**已落地**:
1. MAX_CHUNKS 384→192(-24 张/窗)。★陷阱:`Game.afterWorldLoad` 每次进世界
   **硬写回 384**(08-18"回满档"修复)——静态改 192 被静默覆盖,探针读运行时
   才暴露。修=单一事实源 `BASE_MAX_CHUNKS=192`(静态初始化+afterWorldLoad
   回满+熔断减半同源)。★改类静态常量必须 grep 全部运行时写入点。
2. HUD 防御盾 2×52×48 canvas→img+dataURL(模块级 52×48 scratch 烘焙按
   (难度列,辉光) 缓存 ≤6 条;-2 张/窗)。img 进共享合成层零专属面。
验证:tsc 清+5 测试文件 30 用例绿+运行时 maxChunks=192/has52x48=0/盾 img
loaded(debug-report.test 的 384 断言同步改 192)。

**第三场(12:54)**:起跑 21s 首败→12:55:40 五连败 GPU 进程死→恢复期再 4 败,
扛 83s 无整页死(熔断梯 192→96→64+看门狗+缓存自愈全生效)。失败尺寸含
2464×256/1536×416 等非自有宽条(cc tile/另一窗)= 全机水位问题。★揪出 herd
共犯:afterWorldLoad **直回满档**——第二窗加载/崩溃重进(预算最紧时刻)反而
重堆 12 张页。修=爬档恢复 `max(64, min(BASE, cur*2))`(64→128→192 逐世界爬,
既有恢复点又不瞬时吃满;原"永远 64"bug 依旧被解)。

**第四场(13:00,"第二 tab 永不恢复")**:GPU 进程【没死】(0 次 Restarting),
但主画布后备 **1088×864 连败 7 次**(+另一窗 1512×862)——看门狗每 20s 重建
画布元素、后备永远分不出 = 僵尸循环。auto 熔断降级(60s 内 2 次熔断)对
"进程活但后备分不出"不触发(只到第 1 次熔断)。修 = **看门狗僵尸三振**:
重建后 30s 内又死 ≥3 次 → auto 模式切 CPU 软渲染(主画布 willReadFrequently
→ SHM 后备零 IOSurface,分配必成,页面至少活着)。附带:CloudGL/GLSpriteLayer
补 **objectsStale 旗**——webglcontextrestored 后 isContextLost()=false 但旧
对象已蒸发,dispose 的 isContextLost 守卫挡不住(17 条 INVALID_OPERATION 的
真身),lost/restored 双事件置旗、dispose 见旗跳过 delete。dist 已重建
(index-xDbmOBYL,4173 旧 preview 直接服务新包,EADDRINUSE 属预期)。

**第五场(13:09,"会恢复了但光标没了")**:防护栈全生效——**0 次 GPU 进程死**
(仅 5 次小图失败:40×56×2 角色帧/40×40/28×24/16×16=恢复期重烘焙的写一次
缓存,Chrome 对这些 canvas 软回退)+10 mailbox。光标不恢复根因 = **vui
ui-canvas 层零恢复链**:画布+batch 一次性创建,contextlost 后全部 vui 绘制
静默 no-op,游戏内该层只画光标(系统光标被 #sw-cursor-style 全树 cursor:none
藏掉)→ 症状恰好只剩光标。修 = `VUI.healCanvas()`(frame 头每帧查
batch.ctx.isContextLost,死即原位换画布重建 batch;★监听闭包必须取
VUI.canvas 当前引用——换画布后旧闭包 rect 全 0 鼠标坐标恒 0)。E2E:钉死
ctx→换新✓。dist=index-BjMpQP_t。**瓶颈现状**:不再有进程级死亡,天花板
表现为边际小 canvas 失败→软回退;下一刀=#A CloudGL 并入 GLSpriteLayer。

**第六场(13:47,#A 后首战)**:★**GPU 进程零死亡**(六场首次),5 分钟仅 7 次小图
失败(16×16×2=两窗油漆 tintCanvas/32×22×2=UI 图标烘焙/18×17/640×128)+
一次 1512×862(另一窗主画布重建,旋即成功)——页面"擦伤自愈"而非崩死。
瓶颈=从不显示的纯 scratch/toDataURL 烘焙画布仍在向内核要 IOSurface。
**根治:纯 CPU 用途画布一律 willReadFrequently(→SHM 后备,零 IOSurface)**,
九处落地:ChunkCache.tintCanvas/TintAtlas.scratch/GLSpriteLayer.scratch/
PaperDoll.hairScratch/UI(防御盾+图标 32²+invBg×2+tooltipBg×2;dust 双 scratch
本就有)。
**#A CloudGL 并入 GLSpriteLayer 已落地**:CloudGL.ts 退役,SkyRenderer.cloudGlLayer
由 Renderer 每帧注入共享 glfx(bggl/cloudgl 任一门开);GLSpriteLayer QuadOpts
新增 flipX(u 镜像);quad 几何中心制→左上制。验证:weatherCounter 到期重掷后
13 张 cloud: 纹理进共享层渲染正常。**云量 0 勘误**:非 bug——游走/重掷与原版
逐条一致,存档停在干档低点,+110s 到期重掷自然回满 200(实测);"天气引起崩溃"
定性=脉冲贡献(重掷瞬间 ~13 张纹理上传),非主因。
dist:index-pFHWLwCR。

**第七场(13:58)+ 两问(2026-08-19 午后)**:零进程死亡保持,17 次失败全是
不可压缩面(Chrome 合成器帧@DPR2 3024×1724/光栅 tile/光标层 16×16 + 我方
chunk 页 1024²×2)——机器全机水位贴顶,我方已到底。★用户问"菜单资源带进
世界?"——查证:enterGame 是 newWorld/loadJson 公共漏斗,stopMenu()(menuBg
destroy+titleMenu+VUI.clear)稳定执行;菜单期仅 menuBg+vui 两张全屏,vui 画布
复用为游戏内光标层;菜单贴图=CPU 位图零 IOSurface。**无泄漏**(补 menuBg
destroy 后 width=0 即还后备)。★自愈后数字键/Enter 失效根因:onCanvasRecreated
的 `input.destroy(); new Input()` 把 Game 启动时注册一次的 keydownHandlers
(Digit0-9 切栏/聊天)与 onKeyEvent 清空——新实例两张表为空,鼠标/移动(window
级+轮询)活着而数字键死。修=重建时迁移两张表。E2E:Digit3→recreate→Digit5
仍切栏 PASS。dist:index-lHeqdQHe。

**渲染侧全量审计+压缩 #1#2(2026-08-19 傍晚,用户令"全面审计...哪些可不用 GPU 且不慢")**:
运行时盘点(1280×800 窗):DOM 画布实为 2 张(主+vui;"第三张全屏"系我 debug-line
覆盖层 offsetParent 假象)+chunk 26+lightCanvas **132×84**(1/10 分辨率,早最优,
"全屏光照"系我错误假设)+hardAlpha images 18 张 canvas+glfx 1+6+TintAtlas ≤4;
vimages/uiimages 350 张 27MP=ImageBitmap 形态**零持久面**。两形态结论:①ImageBitmap
= CPU 常驻+绘制走硬件+GPU 拷贝可驱逐(零持久面,可规模化);②SHM 只适合从不进
合成的 scratch(每帧合成源 SHM=每帧 5MB 上传,不可取)。
**#1 hardAlpha→ImageBitmap 已落地**:images.set 后 createImageBitmap 异步升格
(竞态守卫同引用才替换);消费面 AutoTiler/WallTiler/rect 全 drawImage 源,无缝。
实测 18/18 bitmap、canvas 归零。
**#2 vui 光标独占模式已落地**:setState(null)(游戏内)→ ui-canvas 从全屏缩成
80×80 跟鼠标(transform 移动);菜单态恢复全屏。★两坑:①mousemove 监听原用
vui 画布自身 rect 当原点——画布漂在鼠标下时坐标系跟着跑(越移越漂),必须
视口原点直取 e.clientX/scale;②healCanvas 重建后 curMode 复位重挂模式样式、
resize() 在光标模式不得吹回全屏。E2E:80×80+transform 跟随(632,392)+光标像素在。
审计/验证探针:scripts/_render-audit.mjs(分类型计 canvas/bitmap)。
dist:index-BpBpbwgM。剩余:chunk 96 档(#3,用户未拍板)、PaperDoll/AutoTiler
家族同法 ImageBitmap 化(#4)。

**第八场(14:44,#1#2 后首战)**:0 进程死亡(第三连),**尖峰后完全干净**——
14:45 加载尖峰 70 秒 8 次失败(16×16×5=Chrome 光标层/40×56×2=PaperDoll 重烘/
1024²×1)→14:46:15 起零失败跑 4 分钟。形态已从"持续摩擦"变"尖峰对抗后稳定"。

**#4 PaperDoll/AutoTiler 家族 ImageBitmap 化(2026-08-19 傍晚,用户拍板)**:
新 `src/render/bitmapize.ts`(bitmapize:map.set 后 createImageBitmap 异步升格,
同引用竞态守卫;freeBaked:淘汰按类型释放——canvas width=0/bitmap close())。
接线:PaperDoll cache(64 LRU)/tintCache(256)/stealthTintCache(inner 48)+
AutoTiler rotCache/filledCache;类型 `Baked = HTMLCanvasElement | ImageBitmap`
贯通(compositePaperDoll/tint/tintRGBA/eyelidFrame/dollFrame(Rows) 签名放宽,
消费面全 drawImage/.width 无感)。★rotCache/filledCache 的 return img 取
`map.get(key) ?? c`(升格后返回 bitmap 而非闭包 canvas)。E2E:首取 canvas→
900ms 后 ImageBitmap ✓ 玩家 640px 在画 ✓(d1=null 陷阱=贴图未就绪早退,
须等就绪再验)。40×56 失败类应消失。dist:index-IzPX9x1W。

**第九场(15:08,#4 后)**:0 死亡第 4 连,3.5min 仅 5 败/7 mailbox——1024²
chunk 页**首次零失败**,中段 2 分多钟全净。残余=Chrome 光标层/光栅 tile/
一次烘焙瞬态。渲染侧见底。

**★配额归属定案(2026-08-19 用户问"IOSurface 是否页面级限制?GPU/内存很闲置")**:
双实例实验(scripts/_two-instance-test.mjs):两个**独立 Chrome 实例**各载存档
世界跑 100s → **零 IOSurface 失败**(各 13 chunk 页/GL 活);对照单实例双 tab
同机基线 27 败。结论:**预算/配额挂【浏览器实例】级(=每实例一个 GPU 进程,
其全部 tab/窗共享),非全机资源也非单页**——一个世界页+UI 在额度内,两个
世界页同实例即超额;显存/内存闲置与此完全兼容(按张/记账配额,非字节)。
**双开防崩正解 = 第二世界放独立实例**:`npm run play2`(play.mjs --isolate[=名],
独立 user-data-dir 于 game/chrome-profiles/,主 Chrome 无需退出;存档独立,
世界列表导出/导入搬)。亦解释"昨晚 5 开今天 2 开崩"=当时主 Chrome 里还压着
其它 tab/窗共用同池。

**已登记(docs/webgl2-migration-plan.md 尾"待办登记")**:#B 全屏地图纹理
封顶(3040×448 级,低优先);"双开档"BASE 96 可选(收益已入个位数)。

相关:[[imagebitmap-root-cure]](第九台 contextlost 抖动环+熔断器) [[webgl2-phase1-port]]
