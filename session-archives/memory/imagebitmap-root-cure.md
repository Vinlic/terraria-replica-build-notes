---
name: imagebitmap-root-cure
description: 解码风暴根治=atlas vimages/uiimages 全 ImageBitmap 化(自持解码像素=原版 Texture2D);清扫 152 处 complete/naturalWidth/类型放宽;三风暴探针+回归全绿
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-18T11:30:10.118Z
---

2026-08-14 用户问"有根治办法吗?原版怎么做到精准回收?"→ **ImageBitmap 化**落地。

**原版对标**(反编译源):XNA Texture2D=VRAM 归游戏所有(Dispose 自主=精准回收);
原版**不烘焙 chunk**——每帧从常驻贴图直画全部可见 tile,几何走 DynamicVertexBuffer
逐帧重建(重建便宜,贴图永不挪);资产全会话常驻无隐藏缓存。Web 等价=createImageBitmap:
自持已解码像素,drawImage(bitmap) **永不重解码**(懒解码缓存驱逐免疫),close()=Dispose。

**落地(一期)**:
1. `SpriteAtlas`:vimages/uiimages 两 Map 值类型 `ImageBitmap | HTMLImageElement`;
   `USE_BITMAP` 静态门(`?bitmap=0` 逃生门);ensureVImage/ensureUiImage/preloadFiles
   onload 后 `createImageBitmap(im).then(land, () => land(im))`——**晚到钩子
   (onVImageLoaded/bakeTracker)移入 bitmap 落地后的 land()**(时序错了会"晚到不重烘")
2. 机械清扫 152 处:`.complete`→`.width>0`(负形先替换!)/(naturalWidth|naturalHeight)
   →(width|height)/instanceof 删除/全仓类型签名 union 放宽 30 文件
3. 两个 `.src` 缓存键改 **WeakMap 实例自增 id**(PaperDoll tint/UISpriteBatch tinted)
   ——bitmap 无 src,不换则跨表键碰撞画错图

**踩坑(必记)**:
- **`.complete` 正则误伤标识符前缀**:字段名 `completed` 被 `X.complete` 前缀匹配截断
  成 `(X.width > 0)d`——5 文件语法炸;修复=正则 `\(\s*X\.width > 0\)\s*(后缀字母)`
  还原 `X.complete后缀`。机械替换后必跑 tsc 看 TS1005 语法错
- DOM `<img>`/独立 loader(仍持 Image)被全仓 union 误放宽 → 访问处
  `as HTMLImageElement` 定点断言(6 处);optional chain 要先落局部变量再判
- WorldCreation previewImgs 的 complete 守卫是独立 loader 语义,**保留**(sweep 后回补)

**验证**:tsc src 面零错(剩余 20 均并行会话遗留 tests);build ✓;三风暴探针
(地牢传送 arriveChunks=0 存活/重生 20s 存活/图鉴滚轮 40 画布)全绿;
lazyload-guards+chunk-release+asset-cache 15 测试过。**物理验证待用户**:新构建
Chrome trace 的 LazyPixelRef 应≈0(根治直接证明)。

**二期已清零(同日)**:共享助手 `upgradeToBitmap(img, onReady)`(USE_BITMAP 门内
createImageBitmap,失败保留 Image)。模式=onload 里先照旧 set(Image)再升级替换,
消费方每帧重查零契约变化。迁移 12 处:Arrow projSprite/WeaponProj chainImg/
CombatTextFont/SkyRenderer(sunTex+moonTexs+meteorTex,WeakMap UPG+onBitmap 助手)/
BiomeBackground(img/hellImg/loadBg)/MenuBackground/WeatherRenderer rainTex/
FancyResourceBars+ResourceBars(UPG 登记表替换 t 字段)/BestiaryPanel bstLoadSheet/
UI invBg/Renderer 六处懒加载字段。const 局部不能重赋→升级回调直接写持有字段。
三风暴探针+27 测试全绿。剩余渲染器 v2(WebGL2)=完全原版同构,立项另议。

**内存观察(用户报 tab 占用反而降)**:合理——①HTMLImageElement 同时持
压缩 PNG 字节+解码位图双份,ImageBitmap 只持解码单份;②解码风暴本身每次
重解码都分配瞬态缓冲(21 万次=巨量瞬态内存),根除后消失;③同周伴随修复
(ChunkCache 224/Audio LRU/PaperDell 闸/UI DOM 上限)净减更多。

相关:[[dungeon-crash-targeted-rebake]] [[bestiary-contextloss-fix]] [[asset-lazy-loading]]


## 同日 trace④:第四台引擎——DOM 图标解码恒定流(paintSlot 元素重建)
用户报"仍掉帧+靠近地牢又崩",trace:80 万次 LazyPixelRef **均匀铺满 130s**
(每帧 ~52 次,非风暴是恒定流)+rAF 占 60% 帧预算。根因链:探索期 Tiles_ 表
持续晚到→onVImageLoaded 每张置 iconUiDirty→每 30t 一次 refreshAll→
**paintSlot 删旧 `<img>` 建新**(新元素即使 dataURL 相同也要重新解码/光栅化)
×50-80 槽 = 每帧 50+ 解码任务。修两刀:
1. **paintSlot 元素复用**:img 不删,src 不变不动(`getAttribute('src')!==url`
   才赋值);cnt span 同款复用——刷新从"重建 N 元素"变"零 DOM 变更"
2. **iconUiDirty 限频 500ms 窗口合一**(探索期表风暴一窗一刷)
探针(refreshAll×20+地牢传送 8s):存活、img 元素数恒定 4、零 error。
**教训:ImageBitmap 化只治 canvas drawImage 路径;DOM `<img>` 是另一条懒
解码通道——元素复用+src 不变不动是 DOM 图标层的同族根治**。canvas 五台
引擎全记录:晚到表全量重烘/动画不筛视野/重生远跳压力/DOM 图标重建/图鉴面板。


## 同日 trace⑥:第五台——迷雾整幅重建巨帧(F4/读档触发)
新签名:孤立 **642ms 单帧**(FireAnimationFrame 全程仅 3 帧>100ms,非退化趋势)
+解码流温和(51k/19s)。根因=getFogCanvas 整幅重建分支:同步 O(世界)循环
(2100×600 块×4 探测)+createImageData 5MB+putImageData,单帧 ~640ms;
exploredVersion 无脏信息跳变触发(F4 全图点亮/读档首帧/fromPacket 版本差)。
巨帧在 GPU 压力临界时直接崩。**修=分帧行带**:fogRebuildRow 游标,每帧 120 行
(5 帧完,单帧<20ms),未完不落 fogVersion(下帧续),画布半新半旧可先用。
探针(F4 点亮):maxFrame 56ms(原 642)/p99 15.7ms。
五台引擎全集:晚到表全量重烘/动画不筛视野/重生远跳压力/DOM 图标重建/迷雾巨帧。


## 同日 trace⑦:第六次崩溃=无新引擎,是常驻集贴机器 GPU 天花板
签名:主线程全程空闲(rAF 0-3ms)/GC 正常/解码温和(尾段 220/s)/零巨帧零长任务
——"卡"在合成器/GPU 侧,崩的是 GPU 进程内存。五台引擎修完后残余=常驻工作集
(112MB chunk 画布+解码位图+地牢大表+背景)在特定机器上贴近上限。
**兜底=GPU 压力自适应**:Renderer.installGpuPressureGuard 监听主画布 contextlost
(浏览器官方压力信号)→ preventDefault + ChunkCache.MAX_CHUNKS 减半(下限64)
+ Game.shrinkChunks 立即释放超限;连续丢失连续收缩,恢复后以更小足迹续跑。
**根治出路(已多次登记)=渲染器 v2(WebGL2)**:表上传 GPU 纹理一次+每帧
实例化 quad+删 chunk 画布——常驻集从"112MB 画布"变"N 张纹理",量级下降一个
数量级,才是真正的终局。六台引擎(五修一兜)+v2 立项建议完整。


## 同日终审:渲染层残余泄露/风暴清单(13 项分级)+ 调试传送问题
终审代理扫 8 类签名,残余 Top(全部登记,本轮快修 4 件):
-【已修】传送串行门(_tpInFlight:调试快速连点地图曾并发多个 teleportWhenReady
  →反复相机跳转→chunk 集高频换血=画布分配churn 放大器)
-【已修】dustTex/emoteSheet 补 bitmap 化(二期漏网两处)
-【已修】F5 世界直方图全图循环→stride 采样(8192 样本估算,报告只看分布)
-【已修】F5 整幅截图维持(手动触发可接受)+minimap 已裁
-【登记不修,按触发频率】①尘粒逐粒子 getImageData 回读(尘暴/爆炸时~1024次/
  帧,最重一台)②Monolith sepia/retro 每帧全屏回读 2MB(方尖碑常开=恒定)③
  全屏地图整幅世界 canvas 每帧缩放(33M 采样/帧,大地图挂机=GPU 带宽风暴)④
  翅膀染色逐帧像素链⑤横幅 1×1 光照回读+O(n²)过滤⑥lightAt 元组分配(风暴 3-6k/
  帧)⑦浸润 lq() 33k 对象/帧⑧每帧全实体拷贝排序⑨ctx.filter/shadowBlur 按实体
  ⑩染色缓存 contextlost 不失效⑪雪沙无池化+雨滴 O(cap) 找槽
-【调试状态定性】用户问"快速扩图+到处传送是否致崩":**是放大器非根因**——
  六台引擎任一在场时,快速传送把每台的触发频率拉满(换群系=表晚到、跳远=chunk
  换血、F4=迷雾巨帧);修复后传送只产生有界 churn,串行门已把并发叠加掐掉。
  正常游玩同样会崩,只是更慢触发。


## 同日补:暂停态系统清点(用户问"暂停是否仍有系统累积")
Game.frame 结构:paused 只门 fixedUpdate(:2863),render 每帧照跑。逐个清点
render 路径系统:①advanceAnim 已双门(暂停冻结+视野,trace② 修)②chunk.flushDirty
在 fixedUpdate 内=暂停不烘 ✓③天气 weatherFx.update(雨滴物理/池管理/雪沙出生)
**曾无门——暂停挂着下雨=雨池持续满载+雪沙对象持续出生累积**(已修:Renderer
._worldPaused 镜像 Game.paused,update 跳过、draw 保留静态画面;原版暂停世界
全冻结=语义对齐)④monoFilters 状态机随天气门同冻结⑤clock.tick/updateWeather
在 fixedUpdate=暂停冻结 ✓⑥MenuBackground 变体轮换=菜单专用与游戏暂停无关
⑦SW warm 独立(SW 进程,不占渲染内存)⑧粒子 spawn 全在 fixedUpdate 链=冻结 ✓
⑨tintCache 族有 1024 闸 ✓。唯一遗留登记:entities.all() 每帧数组分配(暂停也
分配但量恒定,GC 吸收;终审 #9)。


## 同日补:二期迁移漏 import 事故(用户报 ReferenceError: upgradeToBitmap)
CombatTextFont.ts 用了 upgradeToBitmap 但 import 没插上(当时 python 补 import
的锚点正则在注释头文件上失配,静默失败)——构建不报(minify 后运行时才炸)。
**教训:批量脚本插 import 后必须跑"用了但无 import"全仓反向扫描**
(正则 import\s*\{[^}]*upgradeToBitmap[^}]*\}\s*from),不能只信单文件 tsc
(该文件 tsc 竟 0 错=用了未导入在 noEmit 下不报?实为插入后已通过)。
修复后运行时探针(进世界+5s 监听 console)零相关错误。


## 同日补:渲染动态加载控制台日志(用户调试工具)
三件套:①`[rload]` 每张懒加载晚到一行(Game.onVImageLoaded,含 vimages 总数)
②`[rbake]` 每 60 帧汇总烘焙吞吐(dirty/chunks/lastFlushMs×n/arrive;只在有活动
时打,防刷屏)③`window.__swRenderLog` 控制台句柄:{on/off/toggle/snap}——
snap() 返回全量状态(vimages/uiimages/chunkCached/dirty/lastFlush/arrive/
failedVImages/entities/particles)。静默开关:URL `?rlog=0`。接线在
afterWorldLoad(attachRenderLogHandle)。探针验证:传送地牢捕获 20+ 条 [rload]
+ 快照全字段。F5 报告本就有的 chunkCache/assetHealth 段是机器读版,这是人读版。


## 同日补两修:bitmap 化的次生坑
① **ReferenceError: upgradeToBitmap**(CombatTextFont 漏 import,见前)
② **TypeError: h.addEventListener is not a function**(showPause 崩):invBgImg
升级为 ImageBitmap 后,旧守卫 `!(img as HTMLImageElement).complete` 对 bitmap
恒真(undefined)→ 对 bitmap 调 addEventListener(不存在)。修=instanceof
HTMLImageElement 守卫只对 Image 阶段生效;bitmap 存在即已解码(width 判定)。
**通用铁律:凡持有"升级型"引用(Image→bitmap 替换)的字段,守卫必须 instanceof
分流,不能对联合类型直接调元素 API**。invBgDataUrl 的 width 守卫已天然兼容。
回归探针(开背包+滚合成+showPause):面板建成/零错误(首跑 179 条 404=探针
误报 AudioContext autoplay,复跑分离后 0)。


## 同日补:内存趋势哨兵(用户"感觉仍有泄漏"定位工具)
`[mem]` 每 5s 采样 usedJSHeapSize,环比涨 >8MB 打一行**增量归因**:
`JS堆 127→168MB (+40) | 贴图+0→209 chunk=42 实体=8 粒子=18`
——堆涨时同屏给出当时贴图/chunk/实体/粒子规模,嫌疑面一眼分流(贴图涨=懒载
正常;chunk 涨=LRS 换血;实体/粒子涨=逻辑泄漏;全不涨纯堆涨=数据结构)。
静默 ?mlog=0;snap() 加 jsHeapMB/chunkCapNow。强分配验证:+40MB 触发一行,
归因字段全出。45s 正常会话零触发(基线平稳)。三维内存观:JS 堆(哨兵)/
GPU 显存≈live canvas(contextlost 自适应兜)/解码位图≈vimages 数(rload 行)。


## 同日:突破 Chrome 资源限制(64GB M5 Pro 机器)
`npm run play`(= `node scripts/play.mjs`,2026-08-18 改造)= 冷启 Chrome 带
`--js-flags=--max-old-space-size=8192`(JS 堆 4→8GB)+`--ignore-gpu-blocklist`。
**旗标只对冷启进程生效**——★旧的一行 `open -na … --args` 在 Chrome 已在跑时,
URL 被 Chrome 进程单例转发给既有实例开新 tab,旗标全丢(用户实报"在已有窗口
新增 tab")。脚本流程:pgrep 检测 → TTY 询问/`SW_PLAY_QUIT=1` 自动 → osascript
优雅退出(可恢复会话)→ 等全退(20s 超时)→ 再冷启(旗标保证生效);非交互无
SW_PLAY_QUIT 一律拒绝退出(防 CI 误杀浏览器);`SW_PLAY_DRY=1` 只打印命令。
不用独立 user-data-dir——丢默认 profile 的 IndexedDB 存档。
★同日证伪:`--force-gpu-mem-available-mb=16384` 是安慰剂已从 play.mjs 移除
(详见 [[dualwindow-iosurface-exhaustion]])。MAX_CHUNKS 复原 384(自适应
兜底在,起高让压力真来了自动缩)。Chrome 三道限制:GPU 画布预算(旗标可破)/
JS 堆 4GB(旗标可破)/光栅 tile cache(不可配,ImageBitmap 化已绕开)。内存哨兵
基线读数:之前 180-210MB 锯齿;一台更久会话 260-286MB 仍锯齿无单调=无泄漏。


## 同日:警告体系精细化(用户"完善警告,详细有效避免漏抓")
1. **vui 失配二分类**:VUI_FALLBACK_SAFE 正则表(Player_\d+_\d+/Armor_Head_\d+
  =设计内回退查询)→静默入 _vuiFallbackMisses(F5 assetHealth 的 vuiFallbackMisses
  计数可审计,console 不刷屏——用户报的 Player_1_10 刷屏即此类);真失配→详细
  warn 三步自查(后缀/拼写/重建清单)+noteVuiConsumer 消费点埋点(PaperDoll
  .sheetRect 已接,失配时给"谁在查"线索)
2. **资源加载失败入警告环**:window error 捕获阶段(capture=true)拦 target.src/
  .href——img/audio/script 的 404 此前不进 console.error 也不进环,F5 全盲;
  现入 __swWarns `[资源加载失败] url`
3. 分类直测:Player_1_10(回退)静默+UI_Fake2(真失配)一条详细 warn ✓
警告面现况:errors 环(pageerror/unhandledrejection/console.error)/warns 环
(console.warn+资源404)/vui 二分类/[rload][rbake][mem][contextlost]/F5
assetHealth+chunkCache 段——漏抓面已闭合。


## trace⑨(18:36,复现崩溃)→ 第七台引擎:升级窗口期 LazyPixelRef
签名:末 10s 4.95 万次解码爆发(单桶 2.96 万/5s)+帧全程稳+零巨帧——主线程健康,
仍是 raster 侧。根因:**12 处独立 loader 的"先存 Image 再升级 bitmap"模式**——
onload 到 createImageBitmap 完成之间的窗口期,每帧 drawImage(Image) 照发
LazyPixelRef;天气粒子(dust/rain 每帧几百次绘制)+图鉴(81 格 NPC 大表)是量级
主力。修=五处重量级 loader 改"**bitmap 就绪才入缓存**"(WeatherRenderer rain/dust/
BestiaryPanel bstLoadSheet/CombatTextFont/MenuBackground,未就绪消费方跳帧——
原 ensure 契约;导出 USE_BITMAP 别名)。轻量持有字段(太阳/月相/armBone 等
单帧单绘)保留 Image-first 可接受。冒烟(下雨+地牢传送+图鉴开关):存活零错误。
**教训:Image→bitmap 升级型 loader,"先 Image 后升级"= 窗口期解码漏点;
高频绘制消费的 loader 必须 bitmap-only 入缓存**。contextlost 384→192 触发=用户
未带 npm run play 旗标运行(旗标需冷启 Chrome)。


## trace⑨ 收尾:全仓窗口期清零(用户"确认没有其他地方有此问题")
反查三模式(set-before-upgrade/field-then-upgrade/pure-Image)全仓扫描→修 8 处
重量级:BiomeBackground(img/hellImg/loadBg——2048px 背景每帧 5 层)+SkyRenderer
5 处懒单例(dramaTex/meteor/lantern/party/sunflare,字段赋值型)+dramaTexCache
类型放宽。**定性保留(低频一次性,不修)**:WorldCreation 预览/Splash/
AssetDownloadUI 面板底/像素画导入(dev-only)。复扫残余窗口期=零。
**极端压测(裸 Chrome 无旗标,比用户操作更狠)**:雨+雪+沙尘全开+连续传送 4 处
(地表四角)+图鉴开关+暂停挂 10s——40s+ 存活、零 pageerror、堆 134MB。
窗口期问题类闭合。注:headless 裸启默认 GPU 预算与用户正常窗口不同,真正
的 GPU 天花板结论仍以用户 npm run play 实测为准。


## 2026-08-17 载入花墙回退绿块(用户报,存档玩家远离出生点)
症状:读档后墙 68(花墙)整片 mapColor 绿块回退;挖一格=局部自愈;重进=全好。
F5 全绿(failedVImages 0/errors 0)=表没加载失败,是【首烘回退后晚到重烘漏达】。
根因链:preloadSceneAssets 只扫出生点 ±240;存档玩家远离出生点 → 玩家区墙表
不在预载集 → 首烘 hasTexture false 画绿块(ensureVImage 同时发起加载)→ 晚到
钩子精确打击网偶发漏达(竞态窗口)→ 停在回退。修=**载入终态保险**:afterWorldLoad
后 2.5s 单次全量标脏(有界,区别于 per-arrival 风暴)一次性对齐——表届时已就位,
重烘即正确。日志 [rbake] 载入终态保险。
**探针坑(headless)**:页面无人在看时 rAF 被节流 → tick 停、flushDirty 不跑、
dirty 卡住=假 FAIL;evaluate 内 await+rAF 录帧才可信。手动 flushDirty 验证
35→0 正常。任何"卡死"结论必须先验 tick 在推进。
## 同日:窗口期修复自身的两个真 bug(用户报贴图丢失+复扫)
①失败路径永久缺:upgradeToBitmap 失败是静默 no-op → 纹理永不入缓存(用户
"贴图丢失";F4/F8/F9 并发压力抬高触发率——不是键的错)。修=失败一律回退存 Image。
②在飞守卫缺失:bitmap-only 改造后未就绪期间每帧 new Image 重发(雨/尘每粒子
每帧=请求风暴)。修=统一 loadBitmapOnly(file,has,store)(内置守卫+失败回退),
迁移雨/尘/背景/云/事件月/灯笼/派对/Renderer 四字段/图鉴(land 闭包)/飘字字体/
MenuBackground/BiomeBackground。按 URL 计数验证:同名图恰好 1 次。
性能实测(雨雪 20s):p50 8.2ms vs 基线 8.3ms=零退化(守卫是净收益)。


## 花墙收尾:预载中心改玩家落点(用户"允许加载页停一下,全部就位再进")
2.5s 保险生效但用户等回退窗口久——正解=读档路径 preloadSceneAssets 扫描中心从
出生点改【存档玩家落点】(loadWorld opts.playerAt,mainFlow 读档两路径传存档
player.x/y;生成路径不传=出生点,行为不变)。玩家区表在加载页 await 完,首烘零
回退;2.5s 保险降级为纯保险丝。探针(存档→退出→quickLoad 重进):读档后晚到
Tiles_/Wall_ = **0 条**(此前洪峰)。坐标取值 player as {x?,y?} ?? spawn 兜底。


## 2026-08-17 主角走路静帧排查(用户报,疑并行会话破坏)
诊断链:animTime(Player.fixedUpdate :2714 + Game postUpdate :18551 双写同向)
→ playerBodyRow(useStyleBodyRow 优先→坐骑行3→**走路 6+⌊animTime/6⌋%14**)
→ dollFrame 切行。真键盘探针(按 D 2.5s):animTime 39→392 正常累计;row 序列
[6,7,11,15,19,10,14,19,10,15,19,9] 唯一 8 行正常轮转。**最新构建上链路健康**。
结论:用户看到静帧的构建不是最新(或特定装备/状态路径),非当前代码回归。
排查方法论:症状=动画数据 or 行选择 or 纹理切片三段,每段一探针定位;
headless 节流下必须真键盘+evaluate 内 rAF 采样(外层 sleep 采样假冻结)。


## 2026-08-18 大世界进世界 811/943ms 巨帧=Minimap 构造同步 redrawAll(第八台)
traceA/B(2026-08-17 23:39)同签名:**EventDispatch(type=load) 几乎全程 RunMicrotasks**
(811/943ms 里 810/942ms)+帧尾指纹(最后 1ms 突发 20+ Projectile_N 请求 =
prefetchInvProjectiles + 3 个 data: URL = iconUrl 生成)→ 判定 = **最后一个 await 的
图片 onload → 进世界续体在单个微任务里一口气跑完**。定位:
`Game.afterWorldLoad :2763 new Minimap(w)` → 构造器同步 `redrawAll()`:
**80MB 整幅画布 + 80MB createImageData + 2016 万格循环 + putImageData**
(大世界 8400×2400;中世界 46MB 才有"~50ms 级"旧实测——"只有大世界+高负载才崩"
的定量解释;进世界瞬间一次砸 160MB 直接把 GPU 预算顶穿 → contextlost →
解码位图全逐出)。
**修**:`Minimap(w, deferBuild)` + `buildStriped()` 64 行/带、带间 **MessageChannel
让路**(★setTimeout 隐藏页被节流 1s/带 = 探针/挂机读档假冻结;postMessage 宏任务
不节流)、`Game.minimapReady` 三条进世界路径(await 后才 onWorldReady,加载页多停
~1s)。fillBand 抽出共用热循环(buf 相对带顶 base=y0*world.w 偏移);LUT 抽
ensureLUT;测试构造(默认同步)零改动。单测:拆带 vs 同步全量逐像素一致(130 行
含尾带 2 行收缩)+幂等。**E2E 被并行会话 worldgen worker 栈溢出挡住**(21% 复现,
他们处理中;_mmstripe-probe.mjs 待 worldgen 修复后可复跑)。

**trace 巨帧后 12s 解码流定性**(4612 次 Draw LazyPixelRef,衰减 605/s→220→45):
p50 间隔 8.3ms = **120Hz 每帧**,4 个 pixel_ref 主导(349×1573/9257×1333/…),
仅 291 次 Decode Image = 同批图被反复作废重置而非新解码——ghost img.src 属性
比较恒不等(已修 getAttribute)+ 压力下解码位图被逐出的 DOM 同层重绘。
巨帧分析方法论沉淀:**帧窗口内嵌套事件树 + 帧尾 SendRequest 指纹**(续体发出
的请求指纹 = 定位"哪个 await 链在跑"的直接证据;巨帧前 4s 零请求 = onload
主人是缓存命中,不可能是网络路径)。


## 2026-08-18 traceC 验证 + 两残余清剿(loadUiTex/双前缀)
**拆带验证通过**(用户重测不再崩):37 个 10-33ms 任务跨 0.5s(2400 行/64 带
完美形态);rAF p99=5.7ms max=73.6;4612→3276 LazyPixelRef。
**残余①已修**:loadUiTex 曾返回 Image 且 `upgradeToBitmap` 的位图被丢弃
(只有 onUp 消费者换引用,而无人传)→ 小地图框 tex.frame **每帧 HUD 绘制
Image 阶段贴图** = 残余流主源(552xx 四张 = 皮肤 frame+3 按钮同批分配,
~500/s×4s)。修=loadUiTex 走 loadBitmapOnly 缓存(返回 null 跳帧自愈),
minimapSkinTex 槽位 null 补查。
**残余②(连带揪出真 bug)**:Renderer 四处 loadBitmapOnly 传了
`'sprites/vanilla/…'`(助手内部再拼 sprites/ → `sprites/sprites/…` 404,
onerror 出守卫 → 每帧重发 = 请求风暴)。Arm_Bone/Arm_Bone_3/PumpkingCloak/
PumpkingArm 四处已去前缀。**铁律:loadBitmapOnly 的 file 参数不带 sprites/
前缀**(BiomeBackground 的 'vanilla/…' 形态才是对的)。
**残余③登记未修**:载入期仍有 747/523/501/350ms 同步微任务块(全在加载页,
无巨分配不致命):523ms=afterWorldLoad 减去 minimap 后的剩余(尾部指纹仍
Projectile 预取爆发);747/501/350=存档解析/沉降/回包微任务链;206/239=
DevTools 开录的 CpuProfiler 启动开销(非游戏)。后续可拆:waterCheck/
spawnAllDummies 全图扫、fromPacket 分片。


## 2026-08-18 traceD 终审:canvas 链零 Image(实测)+残余定性 DOM 侧
**实测方法论**:document-start 挂 `CanvasRenderingContext2D.prototype.drawImage`
计数 wrapper(菜单 + loadJson 载入用户真实大世界存档 public/tmp-imgdraw-world.json
绕 worldgen)——**菜单态与游戏态 HTMLImageElement drawImage 均为 0**,canvas 链
(含 UISpriteBatch/VUI 光标)全 bitmap 干净。★UISpriteBatch 用普通
CanvasRenderingContext2D(非 OffscreenCanvas),prototype wrapper 全覆盖。
残余 2344 次 LazyPixelRef(p50 8.3ms=每帧,519831×1095 从 trace 起连续画到尾)
= **DOM 侧绘制记录**(层重记录时的懒引用):ghost left/top 移动触发所在层
整体重记录 → 层内 Inventory_Back CSS 背景/图标被解码逐出时反复 lazy。
已修:ghost 升独立合成层(will-change:transform + transform 移动,合成器直移
零重记录)。要精确指认剩余 DOM 元素需 invalidation-tracking trace。
**loadJson 探针大法**:`__swFlow.loadJson(await (await fetch('/tmp-xxx.json')).text())`
可绕 worldgen 进真实存档(20MB 也能跑);public/ 探针存档用完必须删(vite
build 会整拷进 dist)。


## 2026-08-18 imglog 实锤:第四站 preloadUiFiles(残余流终局)
用户 trace 流程澄清:trace 从主菜单开录→点进世界→走动点鼠标→停。据此
**`?imglog=1` 探针**(main.ts:drawImage prototype wrapper+5s TOP 报告,全
canvas 覆盖含 OffscreenCanvas 之外的普通 ctx)一跑命中:**UI_Cursor_0 ×553/5s
= 每帧画的 Image 阶段光标**——`preloadUiFiles` 是唯一漏网第四站(直接
`uiimages.set(f, im)` + decode(),无 bitmap 桥),而菜单预载清单含光标、
读档预载含 Player_ 纸娃娃全表(进世界起每帧画)——**trace 残余流两大恒定
家族(菜单起 877711/519831 + 进图起 886611/528731)的全部来源,一次修复**。
修后 imglog 复验:光标归零,仅剩加载屏一次性贴图(Sunflower×7,无害)。
**连带加固**:tryBitmapUpgrade 共享升级器(失败→console.warn `[bitmap失败]`
可见化 + 10/20/40s 退避重试,成功原地换回 bitmap——压力窗口期失败不再
永久停在 Image);upgradeToBitmap/loadBitmapOnly/ensureVImage/ensureUiImage/
preloadFiles/preloadUiFiles 六路全接。bmpFailStats 计数表可审计。
**教训:①"ImageBitmap 根治"验收必须扫全部入表路径(第四站在预载批量入口,
前面只桥了懒载单发路径);②wrapper 探针挂 prototype 比 trace 读 id 逆向快
一个数量级,先工具后推理;③headless 零 Image ≠ 真机零 Image——但这次
headless 也测到了(光标每帧 553 次),因为它是确定性漏网非压力相关**。


## 2026-08-18 同类问题全量 review(四族扫尾,修 3 处)
用户"再 review 排除类似问题"→ 四族定义:①永久 Image 入缓存/字段被高频画
②createImageBitmap 失败静默永久回退 ③loadBitmapOnly 路径参数错(双前缀族)
④DOM 每帧失效(src 重设/left-top 移动族)。全仓扫 new Image() 26 处 +
loadBitmapOnly 14 处 + src/left-top 赋值面:
**修 3 处**:①Renderer emoteSheet(Extra_48)曾完全裸 Image 无桥——表情
激活期间每帧画,接 upgradeToBitmap;②Renderer loadExtraSprite 曾裸
createImageBitmap().catch 静默——改共享 upgradeToBitmap 链(失败可见+重试);
③TitleMenu 菜单日月体 .body 曾 opacity:0——**opacity:0 的层仍每帧参与绘制**
(syncCelestial 每帧写 left/top/transform,菜单全程重记录隐形日/月大贴图),
改 visibility:hidden(跳过绘制,布局与命中热区保留)。
**判定合格**:loadBitmapOnly 14 处参数全规范;WeaponProj/Arrow/Fancy/
Resource/CombatText/SkyRenderer×2/BiomeBackground/BestiaryPanel 全走共享
升级链;UI iconUrl 6 处在 500ms 合并刷新路径可接受;Splash/WorldCreation/
Housing/NpcDialog/AssetDownload/F2 导入为一次性或低频 DOM 定性保留;
createPattern/OffscreenCanvas 通道全仓零使用。
**CSS 隐藏语义教训:opacity:0≠不绘制(仍合成仍重绘),常驻隐藏元素必须
visibility:hidden/display:none;每帧移动的 DOM 必上 transform+独立层**。


## 2026-08-18 终审:重试机制自身三处交互收口
自查"失败重试"新机制与既有钩子的交互,修三处:
①**fallback 只许首败触发一次**(fellBack 门)——否则每次重试失败都重发
  ensureVImage 的 land→onVImageLoaded→chunk 重烘(压力期 50 张×3 重试
  =200 次无谓重烘风暴);重试成功仍会再发一次 onReady(=晚到表重烘语义,故意的)。
②**preloadFiles/preloadUiFiles 的 settled 门**——进度 done++/resolve 只结算
  一次,重试成功只换表项不计进度(曾会双计数→进度条>100%)。
③**Game.minimapReady .catch 保险**——buildStriped 极端 OOM reject 会经
  await 断掉整个读档链;降级为 warn+部分构建继续进图。
④警告防刷屏:[bitmap失败] 每文件只警告一次(计数仍全量入 bmpFailStats);
  重试成功打 [bitmap重试成功](第 N 次) 便于诊断。
**教训:给带回调钩子的旧链路加"重试/再触发"语义时,必须逐调用方审计
钩子的幂等性与计数器——重试放大的是当初设计为"只跑一次"的一切**。


## 2026-08-18 联机双开崩溃:contextlost 抖动环(第九台)+熔断器
用户双开浏览器测联机,后加入窗口进世界即崩 + 房主走动卡。trace 铁证:
**最后 3s `contextlost`×17137 + `contextrestored`×20043**(每秒上万次抖动),
主线程被 6.4 万任务/1.5s 淹没=崩溃;LazyPixelRef 仅 63(bitmap 革新完全生效,
与渲染无关);进世界点击本身 891ms(EventDispatch type=click);风暴前
~1.4s 周期 150ms 纯 JS 块×7 = 读档液体运行时收敛窗(已知,自止)。
**机制**:双开窗口共用一个 Chrome GPU 进程,两个大世界联合打爆预算;
旧守卫每次 contextlost 都 preventDefault 请求恢复→恢复即重分配→再丢→
**永久抖动环**;房主卡=同一 GPU 进程被风暴拖累(不是网络同步问题)。
**修=熔断器**(installGpuPressureGuard 重写):10s 内 ≥3 次丢失→不再
preventDefault(上下文保持丢失),`gpuDegraded=true` 让 render() 整体跳过
(世界模拟照跑,画面冻结),8s 冷却期满以最小足迹重试,再抖再熔断;
单次偶发丢失仍走旧自动恢复路径。l10n 键 Toast.GpuDegraded 双语已入
custom+重建产物。**教训:preventDefault 恢复上下文=自动重分配,预算被
根本性打超时它是放大器不是救星;自愈型守卫必须有"放弃 N 次后冷却"闸**。







相关:[[dungeon-crash-targeted-rebake]] [[bestiary-contextloss-fix]] [[asset-lazy-loading]]


## 2026-08-17 走路静帧根因(用户实报,并行会话破坏)
**飞毯 carpetTime 门误伤**:2026-08-16 水体交互批把 `carpetTime=300` 写进
Player 两个 onGround 重置段(:1998/:2139,"站液面/落地回满")→ 落地恒 300;
渲染门 `carpetTime>0 → legs 钉 0(站立)` 把**地面走路腿永久钉死站立帧**
(平移+站立腿=用户症状)。修=两处门补 `!p.onGround`(原版门=飞毯滑翔中
airborne+在用,非燃料剩余>0;Renderer :6148/:6169)。验证:修后 legs
[8,11,16,8,14…] 唯一 5 行轮转,carpetTime 仍 300 但不再钉腿。
**教训:①倒计时燃料类的"渲染消费门"必须判使用中,不能判余量>0——落地回满
类重置会让门恒真;②跨会话并行改 Player 状态字段时,必须 grep 全部消费点
(渲染门在 Renderer,Player 会话看不见);③动画静帧探针必须测最终
playerFrameRows 双行(单测 playerBodyRow 会漏——它没有 carpet 门)**。


## 2026-08-18 双开二进宫:全局画布哨兵+硬释放+同源互认经济档
用户双开再崩(traceM):**16.4 万次 contextlost**(热秒 16k/s),而 JS 堆
39MB 稳/帧 p99 9ms/GC 正常——纯 GPU 配额问题,且风暴打在几百个无守卫画布
上(chunk 烘焙/GL/光照/VUI,主画布单点熔断器是聋的;单画布物理上不可能
8k 次/秒循环)。三修:①window capture 级 contextlost 哨兵(全部画布计入
熔断);②熔断即硬释放:GLSpriteLayer.MAX_BYTES 腰斩(下限 48MB)+
glfx.dispose() 立刻让出显存;③**GamePresence 同源互认**(BroadcastChannel
'sw-game-instances',announce/heartbeat 2s/goodbye/5s 超时):>1 实例双方
自动进经济档(chunk≤160/GL≤96MB+toast),双开不再互相打爆——这是双开的
工程正解(两窗口自己分蛋糕),比"记得带旗标"可靠。**教训:contextlost
守卫必须全画布覆盖,单 canvas 监听在多画布应用里形同虚设**。

**白屏事故(用户实报"第二个 tab 永久白屏")**:熔断分支对主画布丢失也不
preventDefault → 主上下文永久死亡 → 冷却期满"恢复渲染"只是往死上下文上画
= 永久白屏。修:①主画布【永远】preventDefault(熔断期 gpuDegraded 跳 render,
恢复后的空闲上下文无绘制无重分配=不再喂风暴);②冷却期满健康检查
isContextLost→recreateMainCanvas(换画布元素+Game 重绑 Input+重挂守卫);
③chunk 池死画布经 cbOnGpuRecover→chunks.dispose() 全量重烘。**铁律:熔断
可以停渲染,但可见主画布的上下文必须始终保活——"不请求恢复"只适用于
可重建的离屏资源**。

**"关掉另一窗口也不恢复"根因=GL 无自愈**(2026-08-18 三进宫):熔断释放
的 GL 池在恢复后被懒重建→新 GL 立刻再死(双开压力仍在)→GLSpriteLayer
无人监听 webglcontextlost=永远持有死上下文,背景层全空不再重试。2D 画布
丢弃后备多数自恢复,GL 不会——这是两者关键差异。修四件:①GL 层
webglcontextlost/restored 双钩→unavailable+diedAt(★restore 也要按死亡
处理:纹理/程序已蒸发,整体重建比复用干净);②bg 路径死实例 5s 退避重建;
③recreateAuxCanvases(光照/迷雾同尺寸重建);④**20s GPU 看门狗**(非熔断
期发现死上下文静默重建——熔断链终止后此前无任何机制再触发恢复)。
**双开资源战的本质(答用户)**:两标签页=两渲染进程,GPU 进程画布/纹理
后备总账共享但内容零共享(进程隔离铁律);经济档后单窗仍 ~600MB+
(小地图80/位图几百/chunk/GL/光照/迷雾),双开 1.2GB+ 超默认预算→Chrome
8200 次/秒"丢弃↔恢复"循环。出路:带旗标冷启(16GB)/单窗双世界(联机
测试正解)/经济档再深挖(治标)。

## 2026-08-18 晚:小地图+迷雾 CPU 化(GPU 预算 -100MB/窗)
用户问"开局为什么解码几百MB"——实测开局位图仅 ~72MB(树冠 7/MISC 6/NPC 1/
背景 9/纸娃娃 5/出生点 tiles 20/图标 24 后台);"几百MB"实为 GPU 画布基础设施,
其中小地图整幅 80MB+迷雾 20MB 是开局即全额分配的最大浪费。CPU 化落地:
**Minimap**:pix Uint8ClampedArray(w*h*4)+image ImageData 包装(GL 上传源,
node 环境无 ImageData 则 null);redrawAll/buildStriped/fillBand 直写 pix
(小端 ABGR 同旧);flushDirty colorFor→parse 打包直写。HUD 缩略图 mmHudBlit:
≤512² 本地画布+步长最近邻抽样(低缩放 viewTiles 可达 1220)+迷雾逐像素合成
(2×2 覆盖,FOG=0xff080505)——GPU 常驻 80MB→~1MB。全屏地图 GL:image 纹理
(开图持有/关图 dropTexture);2D 回退:开图期临时整幅画布。GLSpriteLayer 增
texSubUpdateData(ImageData 直传,不能 drawImage 进 scratch)+dropTexture。
**迷雾**:fogPix/fogP32/fogImage 同款;ensureFogData=原 getFogCanvas 的脏矩形
+分帧行带逻辑 1:1 落 CPU;HUD 走 mmHudBlit 合成;drawFog 删除。
**测试坑**:①ImageData 构造 TS5.7 泛型——new ImageData(pix,w,h) 需局部变量
非字段;buffer 视图构造 Uint8ClampedArray<ArrayBufferLike> 类型不匹配→改
ImageData(w,h)+Uint32Array.set 拷贝(脏区小,代价可忽略);②夹具 World 不设
groundLevel 时 gl=0——fillBand rock=max(surf+1,rl) 与 colorFor max(1,rl) 在
退化档分裂(真实世界恒等,历史边角非本次回归),夹具必须给 gl/rl 正常值。
浏览器验证:HUD 采样正常/pix 77MB CPU/关图即释零错误。

## 2026-08-18 终局:渲染模式三档(用户方案,多实例检测退役)
GamePresence/双开经济档整体移除(用户拍板"不检测第2实例");替换为
**渲染模式三档**:gpu(默认)/cpu(软渲染)/auto(GPU 崩→CPU,稳→GPU)。
**实现**:OptionsData.renderMode;Renderer.cpuRender + setRenderMode()(重建
主画布[willReadFrequently 条件 ctx]/光照画布/GL 池/chunk 池);ChunkCache
.CPU_RENDER 静态门(烘焙画布按模式走 willReadFrequently)。**自动降级链**:
auto 模式下 60s 内第 2 次熔断→setRenderMode(true)+toast;CPU 稳定 120s 后
尝试回 GPU(失败 5 分钟冷却);gpu/cpu 手动档不自动切。GL/bg/map 在 cpuRender
下全禁(走 2D 回退)。设置面板 modeRow 三档循环。
**CPU 软渲染原理**:willReadFrequently 强制 Skia 软件光栅化——画布后备走
CPU 内存,完全不占 Chrome GPU 进程预算;M 系列统一内存下不省物理 RAM,
但彻底移出 GPU 预算池=多开不互抢。帧率预期 30-60fps(2-5× GPU 加速耗时)。
**迷雾消失 bug 同轮修**:CPU 化遗漏 ensureFogData 在 HUD 路径的调用——
旧 drawFog 每帧推进,新 mmHudBlit 只读不建,入场全图无雾;补一行推修。
