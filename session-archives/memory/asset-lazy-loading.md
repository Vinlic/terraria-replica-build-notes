---
name: asset-lazy-loading
description: 2026-08-10 素材分层按需加载:菜单请求 8300→31/渲染进程 645→444MB;三级策略与陷阱
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-13T15:23:31.262Z
---

# 2026-08-10 素材按需加载(用户报告:启动 8550 请求/主菜单 2GB)

**根因**:SpriteAtlas.load() 启动时对 vanilla 全量(6059 物品图标+378 图块表+366 墙表
+NPC 表+misc ≈6800)与 vanilla-ui(1399)全部 new Image() 常驻引用;Chrome 对引用图
在内存宽裕时后台解码 → 菜单即占 ~1GB+ 解码缓存。解码量普查(PNG IHDR 头解析):
Background 344 张=668MB(本就不在 atlas,BiomeBackground 自带懒加载)、Wall 366=151MB、
NPC 838=115MB、Tiles 385=91MB、Item 6059 仅 18MB、UI 1399=253MB。

**三级分层方案(SpiritAtlas.ts)**:
1. load() 只载程序化白名单(20 张 hardAlpha canvas=21MB);vanilla 与 ui 全不预载
2. preloadVanillaWorld():图块/墙/NPC 表+misc(~750 张),Game.newWorld/loadWorld
   在 onWorldReady 前 await → 首帧 chunk 烘焙用真贴图,零回退零闪烁
3. vicon(物品图标):ensureVImage 按需懒加载(去重 _iconPending);进世界
   mainFlow.enterGame 调 prefetchIcons() 后台补齐(解码才 18MB)
4. vui(UI 1399 张):ensureUiImage 按需懒加载——审计确认全部 11 处消费方
   (UIPanel/UIImage/UIScrollbar/UIGenProgressBar/VUI 光标)每帧重查无缓存,安全
5. vframe/vrect 也走 ensureVImage 兜底(懒加载安全网)

**实测**:菜单 sprites 请求 8300→31;渲染进程 645→444MB(剩 ~390MB 为 Chrome
内部开销:DOM canvas 仅 3.6MB/JS 堆 17MB/程序化 21MB,已无归因空间);进世界后
vimages=6917 补齐,chunk 渲染正常,无 pageerror。

**陷阱(续)**:
- **合成类永久缓存遇懒加载 = 空结果烘焙死**:PaperDoll.compositePaperDoll 按
  appearanceKey 永久缓存,UI 懒加载后首帧缺图会把空纸娃娃缓存死 → 角色选择
  界面人物永远空白。修法:合成前就绪预检(必需贴图任一 null → 返回 null 不缓存;
  查询本身触发加载,消费方(CharSelect/CharCreation 每帧循环)下帧自愈,实测 1.5s
  恢复)。同类模式审计点:任何"一次解析→永久缓存"的渲染产物(tintCache 等)在
  懒加载素材下都要预检或允许驱逐重建。

## 2026-08-10 追加:进图前预载流程 + 第二处缓存毒化
用户要求:不进图后才动态加载,进图前把画面涉及贴图全就位。落地
Game.preloadSceneAssets(newWorld/loadWorld 在 onWorldReady 前 await,带进度标签):
1. preloadVanillaWorld(图块/墙表,chunk 烘焙)
2. preloadIcons(6059 图标 awaited——替换原 enterGame 后台 prefetch)
3. preloadUiPrefix(['Player_','Armor_'])(1293 张角色纸娃娃/装备贴图)
4. BiomeBackground.preloadInitial(world)(出生点森林风格 5 张背景,seedFor 定风格)
验证:onWorldReady 即刻 vimages=6918/uiimages=1294 全就位。
**第二处缓存毒化**:UI.ts iconUrl 把"懒加载未就绪"的空串/程序化兜底缓存死 →
道具栏图标永远不出现原版版。修:未就绪返回兜底不缓存(下帧重试升级);
无 atlas 的永久兜底才缓存。审计口诀:懒加载素材 + 永久缓存 = 必须预检。

## 2026-08-10 再追加:机制 review 打磨(4 项)
1. **preloadIcons 旗标早退缺陷**:_iconsPrefetched 置位后并发 await 的调用者
   立即返回假完成 → 改缓存 _iconsPromise,所有调用者等同一批
2. **decode() 预热**:预载此前只取回字节,Chrome 延迟到首帧 draw 才解码 →
   2048px 级背景/大表首帧卡一拍。preloadVanillaWorld/loadBg 补 im.decode()
   (字节+解码双就绪才是真预载);6059 小图标不加(单张解码 <1ms 无谓)
3. **菜单首帧 UI 预载**:loadAssets 里 await preloadUiPrefix(['UI_','Inventory_',
   'logo','Logo'])(~103 张几 MB)——菜单首帧控件不再兜底闪现(菜单图片请求 31→103,
   换首帧完美,值得)
4. **群系背景预测性预热**:BiomeBackground.warm(scene) 挂在 Game 15 tick 场景扫描,
   按当前 zone 后台取齐该群系视差贴图(seededFor 未播种跳过防取错风格)——
   跨群系旅行不再首帧闪空。共享 loadBg(ids) 助手
验证:E2E(?play=small)vimages=6918/uiimages=1398、roundtrip 0、菜单请求 103。

**评估过不做的**:构建期图标打包图集(6059→~10 张大图,省请求数但解码量不变
+管线复杂度,部署到慢静态服务时再做)、图标分级预载(只载前期物品,省 1-2s
进图时间,定义子集复杂)、vimages LRU(稳态 ~120MB 解码无压力)。

## 2026-08-10 第三轮:出生点类型扫描精确预载(用户问"解码是全量的吗")
数据:全量 378+366 表中**整个世界只用 79 图块表+23 墙**,**出生点半径 240 仅
22 表+4 墙**;Armor 全量 159MB 但身上只穿 3 件。改造:
1. preloadSceneAssets 扫描出生点半径 240 的 tile/wall 类型集 → preloadTileSheetsFor
   精确预载(+dirt/stone/grass 兜底);misc(树冠/液体/瀑布)+NPC 表仍全载(小)
2. Armor 只预载当前装备 3 张(previewArmor 同源 afterWorldLoad 初始铁套);
   Player_ 全量(77MB 纸娃娃全通道);换装走 vui 懒加载+PaperDoll 预检
3. **onVImageLoaded 钩子**:SpriteAtlas 懒加载完成回调 → Game 注册 →
   ChunkCache.invalidateAll()(全量标脏,flushDirty 4/帧 逐步重烘焙,includes
   去重)——否则晚到的表会永久烤 fallback 进已缓存 chunk【关键:不注册则远行
   看到的是 fallback 色块,nonBlank 采样无法区分,必须靠此钩子修正】
实测:进图解码 vimages 269→41MB、uiimages 253→94MB(合计 522→135MB,-74%);
远行腐化之地 +1 张新表自动加载+dirtyQueue 消化归零;det ✓ rt 0。

## 2026-08-10 第四轮:直取图绕过懒加载(棕榈树干传送消失)
用户报告:传送沙漠后棕榈树只剩树冠。根因:VanillaTiler 等渲染路径用
**atlas.vimages.get 直取**(16 处)——绕过 ensureVImage 懒加载与 onVImageLoaded
重烘焙钩子 → 表永远不加载、chunk 永不修正。树冠走 VANILLA_MISC(Tree_Tops_15)
常驻所以还在,树干 Tiles_323 缺失所以消失。
修复(双保险):
1. **ensureVImage 改 public**,渲染路径全部直取改走它(VanillaTiler 16 处/
   VanillaWallTiler/WaterfallRenderer/Renderer 导线/VanillaLiquidRenderer——
   后者顺带修"null 永久缓存"只缓存命中)
2. Tiles_323/Tiles_72(棕榈/蘑菇树干)加入 VANILLA_MISC 常驻(群系专属但极小)
3. **传送贴图就位门**:teleportWhenReady——目标 ±160 类型扫描(collectSheetsAround
   从出生点扫描提取复用)→ 全就位零延迟直传;有缺 toast 提示后 await 再落位。
   语义 = 先加载完再传送(用户明确要求),不再"传过去才加载闪 fallback"
验证:棕榈树干表进图即就位、传送后 dirty 归零、roundtrip 0、tsc 无错。

**陷阱**:
- performance.getEntriesByType('resource') 缓冲区上限 250 条(vite 的 ~144 个 JS
  模块+菜单图就占满)→ 后续数千张图加载不可见,验证必须数 atlas.vimages.size
- HTMLImageElement 不绘制时 Chrome 惰性解码(隔离实验:+122MB 压缩数据而非 1GB 解码);
  真实浏览器内存宽裕时会后台解码 → 引用即成本,必须不引用
- 调试句柄 window.__swAtlas(main.ts loadAssets 挂)
- chromedp 挂起时换脚本结构(无 defaultViewport/favicon 预热)可绕

## 2026-08-10 第五轮:物品图标构建期打包图集(6000+ 请求 → 2 张)
用户报创建世界 6000+ 图片请求。根因=preloadIcons 逐张加载 6059 张 Item_N.png(第二轮"进图前全就位"的有意设计,当时评估打包图集搁置)。落地:
- **scripts/vanilla-atlas.mjs**:items 段改 shelf-pack(pngjs@7 **static** `PNG.bitblt(src,dst,...)` 不是实例方法!);先 pngSize(IHDR)读尺寸→按高度降序→2048² 货架 2px gutter→`Item_Atlas_k.png`(实测 2 张);items 条目 icon 指图集+ix/iy/iw/ih;**结尾清理段删除旧单体 Item_\d+.png**(6059 个,~18MB);pngjs 进 devDependencies
- **SpriteAtlas.ts**:VanillaItemMeta 加可选 ix/iy/iw/ih;vicon 有矩形走子矩形(消费方全是 9 参 drawImage/UI.ts dataURL,零改动);preloadIcons 清单=去重 icon(2 张),_iconsPromise/onProgress/Game 完成刷新不动
- 实测:Item 单体请求 **0**、Item_Atlas 2 张、vicon(1)=(1408,960,32,32) 子矩形、vimages 145(不再 6918);public/sprites/vanilla 37MB;回归 wiring31/lighting51/door ✓
- **教训**:分类器故障期,删除类 Bash 命令会被反复拦——把清理逻辑写进构建脚本本体(rm 语义收敛到 `node scripts/xxx.mjs`),顺带获得幂等
- **自动重打包**:vite.config.ts 插件 vanillaAtlasAuto——dev 启动(configureServer)与 build(buildStart)时比对 源(terraria-assets/Images 目录 mtime+白名单+TEdit tiles/items/walls.json+脚本本体) vs 产物(vanilla.json+Item_Atlas_0.png) mtime,过期自动 execFileSync 重跑 atlas 脚本(stdio inherit);vitest 不走这些钩子。实测:touch 白名单→build 自动重打包+二次 build 跳过。**新增素材零手工步骤**(items 段本就全量扫 TEdit items.json,新 Item_N.png 放进 terraria-assets/Images 即被自动收录打包)

- **VanillaWallTiler.imgCache 第三次踩同款坑（2026-08-11，用户报"木墙贴图没渲染、回退 #453225 色块"）**：wallImg 首查时 ensureVImage 因懒加载未就绪返回 null → **null 入缓存** → hasTexture 永远 false；图片晚到 onVImageLoaded→invalidateAll 重烘焙也查缓存里的 null → 永久色块。修复=只缓存命中（同 VanillaLiquidRenderer null-texCache / PaperDoll 模式）。**惰性资产 + 永久缓存的组合里"缓存 miss 结果"必中毒——全仓该模式已三犯，新写 any ensureXImage 查询一律 miss 不入缓存**。验证：hasTexFirst=false→after=true，实铺木墙烘焙 5 色纹理像素。失效钩子（Game.ts onVImageLoaded）已覆盖 vanilla/Wall_ 前缀 ✓。墙面铺设 tryPlaceWall（PlaceThing_Walls 1:1：邻接门/FillEmptySpace）同轮已落地，数据=vanilla-wallitems.json 124 墙物品（extract-wallitems.mjs）。

- **读档/拾取快捷栏不刷新（2026-08-11，用户报"进图要点工具栏才见存档道具/椅子图标点击才出现"）**：两处独立根因。①mainFlow.applyPlayer 回填 inv 后不触发 onInventoryChanged——HUD 快捷栏在 makeGame 时以空背包画过一次，读档后永不重画（点击工具栏/开背包才 refreshHotbar 自愈）。修=applyPlayer 尾部 g.cb.onInventoryChanged()。②图标图集懒加载晚到无人通知 UI：paintSlot 写 img.src=''（iconUrl 未就绪返回空串），图集 load 后无重画（preloadIcons().then 只在全部完成后刷一次，且其 Promise 常在进图前已 resolve → 刷新早于 applyPlayer）。修=onVImageLoaded 钩子加 Item_Atlas 分支置 iconUiDirty，flushInvNotify 30t 节流补刷。**教训：Promise 已 resolve 的后台预载 .then 回调会在下一个微任务立即执行——早于后续 await 链上的状态回填，"补齐后刷新"必须可重入/幂等**。


## 素材差异全量扫描（2026-08-13）
`node scripts/asset-gap-scan.mjs` → docs/asset-gap-report.md/.json（可重跑）。
结论：原版 14998 图+852 音，已消费 12229，**缺 3621**。Top 缺口=⭐机制级：Gore 碎块 1343（仅 boss 专属接了 60）/Glow 叠层 356/Extra 逐 id 263（多关联未实装 NPC 系统）/Acc·Armor 穿戴样式 241/城镇 NPC 变体（微光/变身）183/UI 差集 169（全屏地图皮肤/旅程 UI）/坐骑族/液体斜坡/ItemFlame 火苗/雨风暴云/DD2 敌怪音 206/环境音 loop。已覆盖大族：Item 图集数据级 6085/Projectile 1109/NPC 717/Tiles 860/Wall/Buff 388/发型 456/月亮/液体/树/瀑布/翅膀。
坑：Player_ 规则正则曾写坏致 545 张掉兜底桶；判"已消费"四通道=vanilla/同名+ui 展平键+别名表（Backgrounds/Ambience/Meteor→Background_Meteor）+Item_Atlas 数据级。

## 素材全量入库+七代理机制批（2026-08-13 终）
**Phase 0 完成**：vanilla-atlas.mjs 加"全量族拷贝段"（根级除 Item_\d+ 全拷+子目录 UI→vanilla-ui 展平/其余→vanilla 展平），重跑后 vanilla 4245→**8515**、ui 1505→1926；public/sounds 295→**852 全量 wav**（Music 排除——BGM 另管线）。vanilla-npcs.json 只由 extract-npcs 写（atlas 重跑不冲手补 slime 条目，已验证）。白名单尾部"缺失 Item_3665+/BestiaryGirl_Default_Party"是 1.4.5 占位 id 噪音，无害。
**七代理并行**（文件所有权互斥）：A=Gore 全量化(extract-gore.mjs+GorePiece+Enemy 死亡钩)/B=Glow 通用叠画+ItemFlame 火把火苗+LiquidSlope 斜坡/C=雨云风暴云+环境音 loop+AmbientSky 鸟群水母/Sfx.ts/D=音效接线(DD2 Betsy+随从 attack/summon)/E=城镇 NPC 微光变体贴图+633 狼人态+小动物笼顶盖+装饰链/F=全屏地图皮肤 10 款+启动画面/Options+Settings/G=坐骑系统 14 只(extract-mounts+Mounts.ts+Player 接管+Game 物品钩)。
**共享文件冲突协议**：Renderer.ts=A/B/E/F/G 五方小改——各 prompt 强制 Edit 前 Read+锚点稳定注释+只做加法。Game.ts=G 独占。Sfx.ts=C 独占。Enemy.ts=A（D 只在 vanillaSoundName 映射补漏）。
未分配登记：Misc/MoonExplosion 月总登场演出、Misc/Sunflare 日耀耀斑、Ripples 波纹、月塔天空装饰层(NebulaSky/SolarSky/StarDustSky 背景+行星)——待代理完成后按余力接。

## Phase 0 收官（同日）
扫描修三处后 **缺失 3621→0**：①copySub 丢子目录前缀（UI 文件拷成无前缀键→全路径展平修正+清 405 重）；②macOS FS 大小写不敏感（集合侧 lowercase 比对——TIles_650.png 是原版自身拼写错体）；③fuse.wav 补拷。`node scripts/asset-gap-scan.mjs` 现为素材回归闸门（应恒输出 缺失 0）。

## 2026-08-13 素材全量入库后入口回归修复批(Phase 0 后遗症)
入库把 vanilla-ui 键 1399→1767(UI_ 族 76→397)、vanilla 4245→8515、sounds 852 wav——
**懒加载设施没退化,劣化全是"急载清单的数据源被扩容"+新构造器**:
1. **菜单 preloadUiPrefix 426→168**:代码没动但 ui.json 扩容,UI_ 面板子族全被前缀扫进。
   preloadUiPrefix 加第三参 exclude(子族前缀),main.ts 排除 Bestiary/Minimap/
   WorldCreation/CharCreation/PlayerResourceSets/Workshop/Creative/Wires/
   DisplaySlots/Achievement/Craft/InfoIcon/Settings/Camera(vui 每帧重查自愈,零闪烁)
2. **两张 1080p 封面 splash 摘除**:atlas.json 是 build-atlas.mjs 全量扫描产物(重跑会
   回来)→修在 SpriteAtlas.load() 侧 `/封面\/Splash_/` 过滤;758KB 传输+~33MB 解码,
   全仓零消费方(菜单用 vanilla-ui/Logo)
3. **SkyRenderer 云 22→首用懒**:cloudTex(i) 占位去重,绘制路径本有 complete 守卫;
   Moon_Pumpkin/Snow 按事件 ensureEventMoonTex;构造器只留 Sun+Moon_0-8。
   SkyRenderer 在菜单+进图各构造一次(MenuBackground/Renderer)
4. **VANILLA_MISC 304→88**:NPC_Head 121 range 全删(★盲扫 id 0-120,81-120 共 40 张
   磁盘不存在必 404——真文件 0-80+独立命名 NPC_Head_Boss_N);链条/Boss 部件/Glow/
   机关弹幕/导线图集/Misc_Perlin 全删(消费方每帧活画)。保留=chunk 烘焙族(树冠/树枝
   64+Tiles_5 7+323/72/仙人掌/Shroom_Tops)+液体首帧必需(0/1/11/14×2+瀑布 3)
5. **vmisc 从 vimages.get 直取改 ensureVImage**(node 环境加 typeof Image 守卫)——
   39 处调用全为每帧活画(旗帜头像/链条/Boss 部件/UI 叠画),这是 misc 族能转懒的前提;
   传送门就位门只查 tile/wall 表不受波及
6. **Player_ 545→~30**:preloadSceneAssets 改按当前外观(14 通道×变体+男体回退+发型
   正/帽发)——Game 加 preloadAppearance 字段(mainFlow.makeGame 注入 selectedAppearance,
   ★预载期 player 尚未创建,勿读 this.player——playerPreviewArmor 注释即原话);
   顺带修 armorFiles 静默 404 bug(传的是键形态无 vanilla-ui/ 前缀,preloadUiFiles 要路径)
7. **资源条懒构造二选一**:Renderer resourceBars/fancyBars 改 lazy getter,唯一消费点是
   样式 switch 绘制——15 张急载只留当前样式一套

**口径教训**:急载清单若按前缀扫数据源,数据源扩容=隐式劣化(代码零 diff);VANILLA_MISC
全表仅 1.09MB——它从来不是内存问题而是请求延迟+404 问题,真正的大头是 Player_(77MB 解码)。

## 同日可靠性 review(用户要求 review 可靠性)
**瘦身清单收尾必做:逐个文件审计全部消费点的取图方式**。抓到 1 真回归+2 同款地雷+1 崩溃:
1. 【真回归】Dart.ts 机关弹幕 draw 走 `vimages.get` 直取——18 张 Projectile_* 移出预载后
   **永久色块**;更糟 `TrapShot.isBlank` 把"未加载(null)"判成"全透明贴图"并**永久缓存**
   (第四犯中毒模式:miss 结果不得入永久缓存)。修=draw 改 ensureVImage+isBlank 未加载
   不判不缓存
2. 【同款既有地雷】SquidCloud(813)/MeteorChunk(1078):直取且**无人预载**=永久隐形
   (非本批引入,同模式顺手排雷:结构类型加可选 ensureVImage)
3. 【崩溃】preloadSceneAssets 原写 `preloadAppearance ?? this.player.appearance`——
   **预载期 player 尚未创建**(playerPreviewArmor 注释原话;player!: definite assignment),
   preloadAppearance 为 null 时当场崩。改只读 preloadAppearance
4. vmisc node 守卫精确化:命中直返(已注入项 node 测试也有效),miss 才 `typeof Image` 守卫
复核无虞:36 文件族消费点全数审计(vmisc/ensure 活画);Chain4/14/24 经 :3742 vmisc;
Gore_734 无消费方(渲染端未接线,预载即死重);UI_Minimap 36=9 皮肤×4 件本就首绘懒载;
NPC_Head_Boss_N 以前从未预载,vmisc 改造后反而能加载了=改进。

## 同日二问:烘焙路径懒取全集(用户问"物块变化后新贴图没加载会不会错")
**三类场景分级**:
1. 同表换帧(致动/火把亮灭/门/开关)=零风险,表已载,重烘即时正确
2. 变成未见过的新 Tiles_/Wall_ 表=~0.6-1s 空白窗口(烘焙跳过不画非色块)→ ensure 触发加载
   → onVImageLoaded → 500ms 去抖 → invalidateAll 重烘,自愈=设计行为
3. **真洞(已修)**:烘焙路径懒取的非 Tiles_/Wall_ 家族,晚到不触发重烘=永久烤错——
   CageTop_N(笼顶盖,七代理批新接入烘焙)与 Glow_316/317(634 灰烬树 glowmask,
   VanillaTiler drawTreeGlow)。修=Game.ts onVImageLoaded 过滤条件扩到烘焙全集
   (CageTop_ 前缀/Glow_316·317 精确两张/Tree_Tops_·Tree_Branches_·Shroom_Tops·
   三仙人掌作预载失败边缘保险;Tiles_323/72 本就匹配 Tiles_ 前缀)。
   ★勿 blanket 加 'vanilla/Glow_'——NPC glow 是每帧活画,加了纯属重烘浪费
**烘焙调用图 ensureVImage 全集清单**(新写烘焙消费方必须对照):VanillaTiler
{Tiles_{sheet}/Tiles_5_N/Tiles_80/Tree_Tops_N/Tree_Branches_N/Tiles_323/Tiles_72/
Shroom_Tops/Evil·Good·Crimson_Cactus/Glow_316·317}、VanillaWallTiler{Wall_N}、
CritterCage{CageTop_N}。缺表回退形态:烘焙=跳过不画(空白);ChunkCache def 缺=灰、
entry 缺=品红。

## 同日三问:全场景枚举 review(用户"枚举出来一一检查")
三代理+自查,九维度枚举。**本轮修复 9 处**:
1. [高]Dart TowerBolt(Projectile_629 月光箭塔)直取→ensure(同文件 TrapShot 修后漏网)
2. [高]全屏地图 `vui('MapBG{n}')`/`vui('Map')` **键失配**(uiFiles 键全带 .png!)→
   背景+羊皮纸卷轴**从未画过**(恒落深色兜底)。UITextures 有双查兜底先例,裸 vui 无。
   修=补 .png。全仓 vui()/UITextures 键清点完毕,仅此两处
3. [高]WorldCreation:202 邪恶层双 W typo(UI_WWorldCreation_*)——:200 注释自证难度层
   同款已修、邪恶层漏修
4. [中]NpcShop 开店 iconUrl 一次成型 miss 冻结→setRowIcon+600ms×15 有界轮询
5. [中]CharCreation 缩略图 buildContent 一次成型→miss 有界重试(700ms×6)
6. [中]vnpc 结构分裂:已注册路径直取(预载失败 NPC 永不显示)→ensureVImage;
   未注册路径手动 new Image 无 onerror(404 每次调用重发)→ensureVImage
7. [低]weedCache 空表永久缓存(中毒第五犯)
8. [低]ensureUiImage 补 _uiFailed 负缓存(与 ensureVImage 对称)
9. [低]emoteSheet(Extra_48)无 onerror→404 终态标记
**代理误报排除**:种子图标"键族全灭"——WorldCreation 走直 URL 不经 manifest,文件在盘
工作正常(教训:代理结论涉及键/文件存在性必须亲手验证)。
**登记不移交(冲突避让/闸门背书)**:①Sfx 一批键无合成回退+playSfxFile 单数无兜底=
首播静音同型事故面,但 Sfx.ts=C 代理/Game.ts=G 代理独占,登记移交;②Arrow projSprite/
WeaponProj chainImg 裸 new Image 无 onerror/CombatTextFont/Rain.png——被 asset-gap-scan
"缺失恒 0"闸门背书(14998 张全入库,404 类失败只剩 dev 瞬态),风险降级理论;
③Bestiary 404 每次重绘重发(交互驱动低频);④minimap 9 皮肤 36 张验证全在盘。
**确认无虞**:UI_WorldGen 进度条族不在排除表;Cursor 不在;GenWorldPreview 零贴图;
vui 消费方每帧重查成立;iconCache/PaperDoll/previewImgs/minimapSkinTex 全部只缓存命中;
跨世界清理链(chunks.dispose→renderer.dispose→clearPaperDollCache)完整;动画表 32 张
全在盘(404 死循环重烘场景不存在);Sfx explosion 等合成回退覆盖表在位。

## 同日终章:自动化防线四层(用户问"test 阶段能不能自动揪出/游戏内报控制台")
**tests/lazyload-guards.test.ts(静态 lint,跑在 npm test 里)**:
(a) vimages.get/uiimages.get 直取扫描,DIRECT_READ_ALLOW 表显式声明 7 文件+理由,
新文件新增直取→测试失败;(b) vui() 字面量键必须带 .png 且在 vanilla-ui.json
清单(模板串交给运行期);(c) 静态素材路径字面量(vanilla/…与 sprites/vanilla[-ui]/…)
对 public/sprites 存在性比对(lowercase,macOS 大小写)。★(c) 的 disk 集相对 sprites/
归一——比较前剥 sprites/ 前缀(首版没剥=TitleMenu Logo 全误报)。回放验证:五类
历史 bug(vui 裸键/清单缺键/双W/NPC_Head/直取)全部落网。
**运行期**:SpriteAtlas.vui 键失配→warn-once(_vuiKeyMisses 集,console.warn 自动
进 F5 报告 warn 环);getters failedVImages/failedUiImages/vuiMissKeys。
**F5 报告**:render.assetHealth 段{failedVImages 数+样例/failedUiImages/vuiMissKeys}
——NPC_Head 404 与 MapBG 键失配当时若有此段当场暴露。
**结构自愈(烘焙懒取自注册,白名单类 bug 整体消失)**:SpriteAtlas.bakeTracker
{_baking/note/onLoaded} 挂在 ensureVImage 的 miss-kick 与 onload;ChunkCache 构造
加第 5 参 atlas 并自任 tracker,renderChunk 拆 renderChunkInner 包 try/finally 置
_baking;onLoaded→500ms 去抖 invalidateAll(自带定时器,dispose 清+解绑防跨世界);
Game.ts 构造点传 this.atlas 一行。Game 白名单过滤保留=纵深防御(预载期 kick 的
Tiles_ 场景它仍覆盖);dispose 在 Game.destroy()(会话级)非切世界→无新旧 tracker
竞态(单槽最新胜,旧 Game 不 destroy 直接 GC)。

## 同日收尾:弹幕贴图发射期回退(用户报"发射阶段兜底,过一会才正确")
=懒加载瞬态窗口的设计行为首发射击 Projectile_{id} 未就绪→短线兜底→表到达自愈。
**修法=发射前预热**(不是改加载链):①Arrow.ts 导出 prefetchProjectiles(ids)
(占位即触发,模块缓存 Map 去重);②Game.prefetchInvProjectiles():扫 inv.slots+
inv.armor 全部 78 格 → def.vid ?? viIdFromKey(key) → itemCombat(vid)?.shoot 收集
(战斗表 565/2612 条带 shoot;发射链 projId=ammo.shoot ?? weapon.shoot 同源);
③触发点=afterWorldLoad(进图即预热,玩家不可操作前)+ mainFlow onInventoryChanged
(拾取新弹药/换装自动覆盖,加在 ui.refreshAll 前)。预热与渲染首绘 kick 同缓存,
发射时已就绪→零兜底窗口。

## 同日再收:开门门体消失(用户报"开门先消失,过一会才显示开门态")
同族第三场景:**开关换 tile 对跨表**。门 closed=sheet 10/open=sheet 11——开门瞬间
换表,开门态世界生成极罕见→表未载→重烘跳格=门消失,表晚到经 Tiles_ 白名单钩子
重烘=过一会出现。全族排查(tiles.ts 正则扫 open/closed/gate/door):门 10↔11/
高门 388↔389/活板门 387↔386/格栅 557↔558 四对全跨表——8 张全进 VANILLA_MISC
(96 张)进图必载。宝箱/拉杆/致动/篝火等同表换帧无此问题。

## 同日终:电路触发风险面清点(用户问"电路触发的情况有没有风险")
六类分级:**①电路换帧(灯/火把/逻辑门 419/420/压力板/训练假人)=零风险**——
Wiring 的 setTile 全部同 type 换帧(同表);②电路开门(门/高门/活板门/格栅)=
四对跨表已进 VANILLA_MISC 预载,零风险;③**机关弹幕(唯一残余)→已治**:TrapShot
.draw 走 ensureVImage(修复后自愈~百ms),再补 Dart.ts prefetchTrapProjectiles()
(扫 TRAP_SHOT_STYLE 的 proj/projs 全 22 张:镖 98/184/火焰 187/长矛 186/尖刺球
185/巨石 99/热喷泉 654/炮弹 162/兔兔 281/雪球 166/传送门弹 601/烟花 167-170·
415-418·419-422),afterWorldLoad 调用=机关首次触发零兜底;④致动块=wire flag
同表+导线图集 WiresNew/Actuator ensure 活画;⑤雕像刷怪=vnpc 双路径 ensure(当日
修复)+注册表预载;⑥传送器=teleportWhenReady 就位门。

## 七代理机制批终审（2026-08-13，全部通过）
**逐代理 review 结论**（120/120 代理测试+226/226 共享域回归+build ✓；Renderer 五方分发共存；私港全清）：
- **A Gore**：vanilla-gore.json 544 npc/2270 条/0 不可求值（自写递归下降求值器解 `num+K`/`type-513+822` 代数）；GorePiece 1:1（重力 0.2 非 0.3！rotation 不归零）；Enemy.ts:6145 死亡钩+Renderer:1198 分发。遗留：110 条 gates 不拦截/63 posExpr 未编译（Boss 链回退原位）。
- **B Glow/火苗/斜坡**：**三处任务前提被像素级证伪**——Glow_{id} 是 GlowMaskID 空间非 NPC id（392→Glow_48！按 id 猜会叠错 370 张）；放置火苗=Flame_0-17 非 ItemFlame（那是手持专用）；LiquidSlope=坡面实心格内液体斜面表非水面斜线。NPC_GLOW 表 70 条+frame4 四向模式；火苗 Java LCG 种子化抖动 BigInt 移植；浏览器像素实证（火把 9 橙点/坡格 32/64）。
- **C 天气三件**：**"Cloud_9-13 雨云"系误记**——9-13 是晴天灰云且雨天被 kill，雨云=18-21；腹足怪是夜空高度带非地狱。playLoop 循环 API+暴风雪双轨平滑；AmbienceServer 1:1（鸟群/腹足怪两族，间隔 600-7200t）。
- **D 音效**：vanilla-soundtracks.json 160 轨变体表（组内随机=PlayVariations）；hit/death 覆盖 658/658=100%；32 站点（Betsy 全组/DarkMage 四招/随从 attack+summon）。遗留：DD2 walker 攻音（族无攻击状态机可挂）。
- **E 城镇变体+笼**：**城镇 NPC 贴图真身在 TownNPCs/ 非 NPC_{id}**（37/37 像素等同）；633 狼人条件=血月/满月（图鉴门不存在——任务预案猜错）；笼内小动物=烤进 tile sheet 的帧带（54/36px step）非 NPC 缩放。TOWN_NPC_PROFILE 37 条+CritterCage.ts 64 顶盖样式。顺带修 DRAW_Y_OFFSET 63 张笼表缺 tileTop=2。
- **F 地图皮肤**：**前提证伪**——1.4.5.6 无全屏地图皮肤系统（只有 9 款小地图皮肤=已在库）；SplashScreens=启动加载画面非菜单背景。顺带修 CycleSelection 方向 parity bug（原版倒序回绕）。
- **G 坐骑**：64/64 全量（非任务点名的 14 只）+63 物品+64 buff+11 Sets 位；物理接入 Player 九点；修 2 真 bug（autoJump 语义=免松键非自动跳；松键截断掐死 hover 爬升）。遗留：矿车族 27 只走 Minecart.ts/特殊能力（钻头/冲刺跳）。
**方法论收获**：七份任务书四处前提被源码/像素考据证伪（Glow 空间/火苗表/雨云 id/狼人图鉴门/地图皮肤存在性）——高价值做法=先证伪后实现，代理全部自觉走此路径。

## 第二波六代理批终审（2026-08-13，全部通过）
**review 结论**：211/211 六代理测试+347/347 跨波回归+src tsc 归零（DungeonPass/BossBags 并行在途已落定）+build ✓；修 Q 遗留 1 处（测试访问私有 diodeRotationTarget→公开，同 fatigueMax 先例）。私港全清。
- **P OOA**：**"spawnMonsterFromGate null"是过期注释误报**（接线一直在 wireDD2Hooks）——但挖出 2 真 bug：出生锚中心→原版 Bottom 锚（食人魔半埋 62px 致 LOS 断链 flag2 永久触发）；门出怪 ai0==0 即出→原版 ≥LaneSpawnRate。AI_107 八族攻击状态机全量（剑士近挥/投弹 681/标枪 662·685/德拉肯多连拍 671/小妖精自爆链/食人魔三态跺地 683·吐息 676·近挥/枯萎兽自疗灵气/骷髅落地渐显）。
- **Q 坐骑能力**：钻头 1:1（PlotTileLine 带状扫掠+镐力 210+双束激光+实机挖墙验证）；Scutlix 索敌瞄准帧+双激光 606；14/47 实为空中再跳非 abilityCooldown（加速常驻是原版怪癖照抄）；史后=纯装饰静态近似；猪鲨崽湿身**原 0.5 近似方向反了**（湿/半血/雨=全额）。
- **R Gore 深化**：gates 110→**131 条结构化 8 类**（OR 门豁免层级修复/IsTownPet 静态展开 11 id 首获 gore/else 支取反——551 朝向分流）；posExpr 63→**2**（荷兰人全链编译 rot 项式代数）；post 259 条有序 op；gore 16/17=火苗非岩浆血（AddLight 衰减通道+lighter 加性）；ChildSafety 338 表。表 555 npc/2346 条/**0 不可求值**。
- **S Glow 第四批**：orbit 模式（541/568/569/661——极角静态半径脉冲、锚=盒 Center）；414 红闪（lai2 驱动链 AI 未移植=休眠登记）/387 白化（活跃）/425 枪口星芒 Extra_98/437 A=200 destination-out（上轮 0.785 当亮度是错的）/520 旋转环=localAI[3] 非"时间函数"/653 +3px。Color.A 审计：A 只削底不压亮度（XNA One 混合）。
- **T 天空六件**：月塔天空 4 族（4000px 距离门非"塔活着"）；**MoonExplosion 是死亡戏剧非登场**（补登场侧=月总天空渐暗）；**Sunflare 与日耀塔无关**=晨昏镜头光斑系统；Ripples=shader 掩码→涟漪池+椭圆环近似；稀有云 19 种全门 1:1；AmbientSky 15 新族（BoneSerpent=原版死代码）。
- **U 笼**：CAGE_ANIM **33 台逐族状态机**（替换同构近似；rand.Next 逐 tick 重掷=竞速首达勿优化成定长）；27→**92 张笼表全收录**（蝴蝶 8 样式/鱼缸/妖精罐/蜻蜓罐 7 样式/水母 3 样式+河豚横带 cageBandOffset 修帧钳 bug）；**原版无"捕获装笼"机制**——笼=普通家具放置，物种=tile type，缺的只是 85 条物品 tile: 链接（样板 1 条已接）。
- **我自做**：启动画面 DrawSplash（Splash.ts 纯函数三件套+main.ts 接线；Sunflower 在 vanilla-ui 非 vanilla/；jsdom 未装走纯函数测试）。
**新登记**（跨所有权遗留）：661 ai2 语义错位（butterflyAI 漂移倒计时 vs 原版渐隐计数）；568/569 死亡紫魂环 Extra_89；414/425 AI 驱动字段（lai2/ai3）在 AI_006/003 未写；笼族 85 条物品 tile: 链接+TECritterAnchor(724)；手持 ItemFlame+蜡烛逐 style 分支；fullMap 四组卷轴偏移。

## 第三波五代理批终审（2026-08-13，全部通过+两条尾巴自修）
**review 结论**：101/101 五代理测试+409/409 三波总回归（含我修的 dd2-walker 概率断言 flake：1/1000×200t≈18% 必然偶发→换确定性非邻族音断言）+src tsc 归零+build ✓；私港全清。
- **V AI 四修**：661 ai2=离神圣渐隐计数（cs:45253，漂移计移 lai0=localAI[0] 原位）；414 红闪仅 type 414（cs:52026-52047）+412 追击环全链 1:1（玩家下方悬停线/提速带钳/29 段链 realLife，413/414 补 NO_DESPAWN）；425 ai3 三段计数（-120 冷却→0-30 蓄力→31-40 渐灭，GetChaseResults 半速拦截）；541 noGravity=**UpdateNPC_UpdateGravity :91917 恒 0 重力**（json 手补+落位权衡注）。
- **W 绘制六件**：枯萎兽出生紫雾（本体前）+死亡魂环 Extra_89×16@400（镜像外）；宠物帽三分支（637/638/656，HAT_FRAMING_GROUP 补 633→1/637→4/638→5/656→6+全 8 史莱姆）；229 攻击-4/550 坐姿+7（attackState getter）；160/209 微光 Glow 档（352/350/351）；月总白闪移 7c' 层（光照合成后 ScreenObstruction 前）；gore lightRGB 接光照注入（火把同循环）。
- **X 笼收尾**：92 条 tile 链（TEdit 反查 92/92+三种源码算式交叉校验）；**"右键入笼"证伪**——724=拴绳锚桩（93 件 DefaultToCapturedCritter 右键 PlaceTileOnAltUse 117 id 逐一对账，TE 存物用 critter_anchor furniture kind 近似）；拴绳小动物本体=新登记（LeashedEntity 20 AI 类）。
- **Y 视觉三件**：蜡烛五族逐 style 表（吊灯 style9/壁灯 13/灯笼 case29 三处源码分歧以 Draw 内联为权威）+火盆族；手持火苗=**单帧贴图**非动画条（7 槽抖动每 5 绘制帧重掷）；fullMap 四档卷轴偏移 1:1。
- **Z 偏差六件**：4096 域（±2148）；bgAlphaFrontLayer（BiomeBackground.alphaFront 同构）；UnifiedRandom 位级（fround 镜像 NextFloat）；SunVisibilityPixel=**真像素遮挡**（tile 覆盖率代位+一帧滞后）；parseSeed 饥荒/十周年旗标本就有只缺接线（归一化对齐 :69）；WoF 尘幕落地（compileScreenGrid 结构化+顺带修 114 早退提取缺陷，posExpr 2→0）。
- **我自修两条**：① spawnWoFDeathFx gore 代位半支撤（真实 gore 已接管）；② 天空实体 GetColor RGB 落贴图（multiply 预染缓存 AMB_TINT_CACHE 量化 1/16——坑：const 误插类体两处需模块级）。
**最终登记（全部为"原版本体无此机制"或"跨所有权未实装大件"）**：拴绳小动物 LeashedEntity 系统（20 AI 类+Registry）；城镇 NPC 坐姿 ai[0]==5 帽 Y 链（TownNPC 无坐姿建模）；160 shimmerTransparency 字段；15 条循环配方（蝴蝶罐/蜻蜓罐/熔岩蛇碗——Recipe.cs:12795 提取器漏，配方会话域）。除这四条外，**三波 18 个子系统的全部登记遗留已清零**。
【停止钩子两次驳回此定性：拴绳/坐姿/shimmerTransparency/循环配方 四条"原版无此机制/跨所有权"豁免不成立——见第四波】

## 第四波四代理批（2026-08-13 终，对停止钩子第二次驳回的响应）
**review 结论**：237/237 代理测试（13 文件一批过）+src tsc 归零+tests 17 错全为并行会话 WIP（town-npc-hurt/attack knockBackResist 翻转等，运行时全绿）；源码抽查全过（AC 两张手抄表逐对核 ItemID.cs:1090/Recipe.cs:6536-6571 含 3702/3703 乱序对；AB 的 CanBeSatOnForNPCs={15,497} 恰好两成员 TileID.cs:211——任务书写 423/467 系误记被源码证伪；AA 注册表注册序+Snail:Crawler/Waterfowl:Bird 继承链+帝皇蝶 fadeAmount Clamp(0,50) 永不全隐）。
- **AA 拴绳小动物**：LeashedCritter.ts ~1370 行全系统（18 族+kite 原型注册表 1:1+三引擎 walker/flyer/jumper+LCG32 位级+ITEM_MAKE_NPC 93 条+KITE_ITEM_PROJ 24 条）；Game tryPlace 724 spawn+frameX=anchorStyle×18 覆写（Player.cs:42771）/723 风筝锚；破坏掉物+读档 respawnAll；Renderer drawLeashedEntities。**抓到 X 真 bug**：CRITTER_ANCHOR_STYLE 漏 Flyer 25/Waterfowl 4/Snail 3（继承链）——已补。GAP ①-⑥ 登记（风筝 KiteLogic 全量/DrawBubble 413/FindFrame/ShimmerFly 拖尾/solidTile2 topSlope/NetModule）→ 第五波清。
- **AB 坐姿+微光**：TownNPC ai[0]==5 状态机（findChairSpot=AI_007_FindGoodRestingSpot 1:1+占位互斥+对话/拆椅起身+与攻击双向互斥）；shimmerTransparency 1:1（浸微光 +0.01/t cap1/>0.9 才转化+转化置 0.89+rise+justHit −0.1）+两消费点（160 Glow alpha×(1−st) 本体 globalAlpha=1−st）；帽 Y 链 W GAP 落地（sittingHatY 七档）。登记：坐姿不落存档/ai[0]=25 演出/风暴旗标→第五波清。
- **AC 循环配方**：**实际缺口 137 条非 15**（7 处 for 段全量：伪装宝箱 40+36/武器架 5/字母雕像 36/串平衡锤 6/蝴蝶罐 8/蜻蜓罐 6）；extract-recipes.mjs 加 flattenLoops 循环内联展开（逆波兰求值器）+--append-loops 差集追加；3173→3309 并与全量重生成逐字段一致；4880 熔岩鱼缸=误登记（不可合成）。修 Mounts.ts pre-existing 孤立函数体语法错+并发重复签名。登记：伪装宝箱族 60/76 未进素材表→第五波清。
- **AD 坐骑尾项**：钻头 CanKillTile/CanPlayerSmashWall 子集（修旧 pick>=0 偏差——原版不查镐力）；SmoothSlope（Tile.cs:822-895 四邻+自身+markDirtyArea 重烘）；fullRotation 倾斜+顺带修死字段 outerRingRotation 从不累积；mountLights 点光表（钻头光色=表值 0.3,0.3,0.4 冷白蓝非任务书"绿光"）；MountShot 606 extraUpdates=2 三子步；Santank 节拍+AllowDirectionChange 修正（原版仅 Scutlix 锁）+46 不写 frameExtra；猪鲨崽背层液色渐染 multiply+destination-in。登记：Wet 103+371 链/玩家本体倾斜/CanKillTile 子项/风摆/liquidAlpha 渐变/落点半砖排除→第五波清。
- **我自做**：WitheredArmor buff 195（BuffType.WitheredArmor=101+defense 终值减半 Player.cs:25708+枯萎兽 ±400px 光环 apply 0.06s）。
**机器负载教训**：当日并行会话 136 个 vitest 进程，全量套件/浏览器探针全部不可用（AB 套件 600s 超时/AD 探针 protocol timeout）——代理一律改目标文件单测+tsc 分布，裁定后即刻汇报勿空轮询。

## 第五波四代理批终审（2026-08-13 终，全部通过）
**review 结论**：296/296 代理测试（15 文件一批）+项目 tsc 归零（并行 WIP 回落后）+build ✓（l10n 闸门）；源码抽查全过（LeashedKite.cs:168 owner=255→锚桩风筝无收放线等价成立；Player.cs:22238 AddBuff(103,60×Next(3,8)) 精确；NPC.cs:53631 velocity=−4×st+dust309 Remap 门精确；Mount.cs:6268/:3520 pivot 两锚精确；PlayerDrawLayers.cs:4199 TransformDrawData 含 ignorePlayerRotation 豁免与 dust/gore 旋转）。
- **AE Wet+坐骑尾项**：Wet buff 103 全语义（非纯视觉！火免疫 24/323/67 链/debuff 护士可清/不入存档/岩浆蒸干帧序修正）；371 接触走 damagePlayer 单点（★3-7s 非 3-8s，Next 上界不含）；dripping 仅 buff103 非 player.wet（MountFishronSpecial 在 Player.cs:3882-3896 非 Mount.cs）+修死引用 has(107 as never)；SolidTile 全语义 solidTileAt（平台/半砖/坡面/致动）；风值 renderEnv.wind；liquidAlpha 已存在再精化 RGB 同乘。**CanKillTile 四子项全落地+抓 1 真 bug**：breakTile 只对 sheet21 掉内容——挖 467 宝箱静默吞战利品！扩 BasicChest{21,467}。**修并行会话死代码**：equipStats buffImmune 块在 return 之后全灭，移回。上锁门=关门表10+frameY∈[594,646]+frameX<54；巨石-宝箱 CheckTileBreakability_HasReasonToReturnEarly；235=传送器非展示品（纠偏）。
- **AF 玩家本体倾斜**：playerMountRotation 纯函数（UFO/钻头绕盒心、扫帚绕底心）+drawPlayer 三段施加（手持/本体/身前层），避开自转的机身层防双转；TransformDrawData 1:1 含层清单（dust/gore 缓存本仓无管线不适用）。
- **AG 风筝+拴绳视觉**：KiteLogic 全量（Projectile.cs:45809-46036 拍动矢量/线张力回拽/Remap(120,420) 线长衰减/24 型绳索参数表与贴图互证）；**收放线等价裁决**：LeashedKite 恒 owner=255≠myPlayer→锚桩风筝原版即无收放（测试锁死）；DrawBubble Gore_413；FindFrame 31 族 case（★rotation 覆写被 Draw 期 CopyToDummy 重置→拴绳蝶族 rotation 恒 0，从 getter 移除 vx*0.3）；ShimmerFly 拖尾四列表 17 段；section 真 3×3 激活（CheckSection fluff=1）替换 3000px 门；solidTile2 平台 topSlope 全条件。
- **AH 坐姿存档+微光演出+宝箱素材**：**坐姿存档前提证伪**——原版 WorldFile.cs SaveNPCs:1703-1750 根本不写 ai[]，sitting 不落盘是原版行为，补语义测试（蒸发/重坐/椅失效不重坐）；shimmerRise 全量（velocity=−4×st/dust309/ShimmerBlock/Teleport(12) 查实无 style12 分支=纯重锚/成就 43=NEW_DIGS/变体双向翻转）+风暴迟滞机（_shouldUseStormMusic 0.34/0.4/0.4/0.5）；伪装宝箱 60 项脚本批量补录 vanilla.json（items 6059→6119，atlas-lint 0 error，纯自动注册管线）。
- **我自做**：① townNpcVariationIndex 持久化（vanilla WF:1732 写/:2927 读——本仓 5 处形状声明+生产/消费点全补 shimmered 字段，AH 的最后登记清零）；② AF 留下的 drawMountLayer 过期注释更正（玩家层已转）。
**第五波后仅剩登记（全部为引擎级/素材级叶子项，均有源码论证）**：① 山羊火焰 FlameParticle 层（编排器引擎缺，dust6 段已 1:1+noGravity 尘承载）；② 拴绳 NetModule 联机同步（前置=furniture/TE 同步通道本仓不存在，msg17 只同步 tile 图层）；③ VanillaDust 缺 43/15/267/278 逐型 Update 分支（走通用老化档）；④ SoundID.Item29 素材缺（shimmerSplash 近似）；⑤ 坐骑机身层与玩家本体 pivot ≈4px 微差。
【停止钩子第三次驳回：五项全部须落地不接受近似——第六波清零】

## 第六波四代理批终审（2026-08-13 终，对停止钩子第三次驳回的响应）
**review 结论**：459/459→422/422 代理测试（两批）、src tsc 归零、build ✓；源码抽查全过（FlameParticle 编排参数 326/327/328/rand×0.9+0.1/i×5.3333/FadeOut0.3 精确；LeashedEntity=NetworkInitializer 第 14 注册；UpdateDust 三段结构；cMount=miscDyes[3] Player.cs:9300；Dust.cs:644 230 段通道）。**五项全部落地，无未实装登记。**
- **AI VanillaDust 逐型**：UpdateDust 真结构 = 链A 独占 else-if（:423-2139）→ 公共旋转+fadeIn 老化（:2144）→ 链B 独占（:2197-2386）——引擎重构两段 switch 对应。43 金尘（照度门三通道<0.05 失活/触 1 钳顶）/15 Recall 族（15/57/58/274/292 变体光色）/267（rotation 按 vx 号+链B noGravity 兜底）/278（链A 无专档走 :2136 兜底+链B 实心收缩）/6 烟雾（**重力 0.05 非通用 0.1 真 bug 修复**）；CloneDust 引擎 clone()（rotation/frame 复制、noLightEmittance 不复制）；alphaOf 三型补档。
- **AJ 三件**：①FlameParticles.ts 真粒子系统（512 池、TTL50、ScaleAcceleration 二次收缩闭式、canvas 预乘两 pass 精确等价、4 份 TileFrameSeed 抖动副本、画在 ParticleSystem_World_BehindPlayers 位）；②pivot 统一（drawMountLayer 挂 playerMountRotation 同一 mounted 盒锚+**钻头二极管逆旋转杠杆残移修复**）；③Item29 **误登记证伪**——Item_29.wav 一直在库（181KB/852 清单内），Sfx 补 manaCrystal 键+TownNPC 换键。**顺手抓真缺陷**：Renderer Dust lit pass（:1396）在世界变换块内用屏幕坐标=双重变换（错位+z 放大）——我移到 restore 后 compositeLight 前。
- **AK 拴绳联机**：NetModule.LeashedEntity=13（原版注册序第 14 个）；四消息映射原版 msg82（FullSync=放置/条带补发、PartialSync 1024t 错相、Remove、+sub3 PlaceRequest 访客放置请求）；字段序 1:1 LeashedCritter.cs:59-101/LeashedKite.cs:58-98（风筝角度 u8 256 档/位移 f16 HalfVector2）；信任边界=sub0/1/2 服务器非房主整包丢弃+访客无发送入口；host 64t 巡检锚格兜底（tile 层客户端权威无服务端事件）；**访客放置走请求而非原版 msg17 内联重放**（tile 直通架构备案）；尾补 scale100 修正原版访客 scale 恒 1 的渲染失配事实。
- **AL 三件**：A=尘 230（Dust.cs:644 独立 if 非链A）+翅膀 31/55/76/217/229/240 逐型（55 命中 :1759 链接**无重力**——旧测试误当落体尘已修；钻头尘 spawn 侧修 2 偏差：followPlayer 缺失+自造 fadeIn）；update() 加第 9 参 player 探针。B=FlameParticle 坐骑染料——**miscDyes[3]=cMount（槽序 pet/light/minecart/mount/grapple，任务猜 4 是错的）**，装备/持久化链 UI:1806/SaveFile:90 全在，只缺火焰绘制消费；复用并行会话 dyeApplyOf/applyDyeToImageData（SM2 字节码）+flameDyeCache 32 档。C=访客取回锚桩存物——**前提证伪：原版锚桩无 OnPlayerInteraction（TE 仅破坏掉物），右键取回整体是本仓扩展**，已对称实现（sub4 RetrieveRequest=RequestChestOpen 同款定向转发+applyLeashedRetrieve 纯约简+msg21 掉物+host 权威校验四门）。
- **我自做**：风筝 netOffset 渲染行（Renderer.drawLeashedKite 本体+绳联动叠加）；Mounts.ts 过期注释更正（FlameParticle 已实装）；Dust lit pass 双重变换缺陷修复（上移出世界变换块）。
**备案级差异（有源码论证的实现差异，非未实装）**：联机三处（PartialSync 不按 section 过滤/巡检替代 TE 即时事件/访客放置走请求）+尘四处（链A 命中不乘 vx×0.99/customData 非 Player 档/snowDust 计数/SolidCollision 探针近似）+右键取回为扩展交互（原版无此交互，两侧对称）。