---
name: remaster-studio-pipeline
description: 素材重制管线(Remaster Studio)全链落地:AssetCatalog 六类切帧聚合+gpt-image-2 逐帧重制+zip 素材包热补丁(类 mod 局部覆盖)
metadata: 
  node_type: memory
  type: project
  originSessionId: be9285e0-8206-48c4-a7de-b260d1c6d232
  modified: 2026-08-19T09:42:49.201Z
---

# 素材重制管线(Remaster Studio,2026-08-19 落地)

六里程碑全绿:catalog 单测 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7。

**架构三层**:`src/remaster/`(types/AssetCatalog/NpcGridLayouts/FrameOps/PackFormat 进 bundle;ImageRemaster/PromptTemplates/WorkbenchState 工作台专属)+ `public/remaster.html`(dev-only 工作台,tree-inspect 模式直接 import '/src/*.ts')+ `tools/remaster-proxy.mjs`(OpenAI 代理 :5210,npm run remaster-proxy)。

**关键坑与定谳**:
- ★`onBakeAssetArrived` 对已就位贴图替换是 **no-op**(chunkSheets 只登记烘焙期 miss,ensureVImage hit 早退在 note 前)→ 运行中热补替换 tile/wall 必须走新增的 `ChunkCache.onSheetReplaced`(查 chunkConsumed 消费登记表,500ms 去抖,★禁 invalidateAll)
- gpt-image-2 **不支持透明背景**+最小总像素 655,360(边长 16 倍数)→ 必须生成大图(computeGenLayout:帧放大到长边~1024,画布逐 16 扩边达标)后盒式缩回+原帧 alpha 蒙版(轮廓逐像素不变=特性)
- OpenAI CORS 两度移除 ACAO → 本地代理转发(node:http 原样 pipe multipart,key 走 Authorization 透传>env,300s 超时)
- 卸载/禁用 replay 的 restore 集合必须含【被删 pack 的文件】(只取现存 installed 并集 = 卸载后 vimages 停留 pack 图的根因,E2E 抓到)
- tile cols/rows 不可信(压板 135 cols=0 前科)→ AssetCatalog 按 sheet 实际尺寸+stride 步进枚举;696 不在 vanilla-npcs.json(网格兜底补建,694=693+1)
- **帧枚举≠渲染 idx**:2D 网格 NPC(npcGridFrames)按行优先网格序枚举 sheet 全格,perRow(696=9)是渲染 idx 折行语义,混入会丢帧(162→54 首版 bug)
- 独立缓存三处不经 atlas 须钩子:Arrow.spriteCache/frameCache(键 `id|idx` 无 texId)、UI.ts buff 栏直链 img.src、**UI.ts iconCache(物品id→dataURL,Plan 代理漏,验收时亲查补)**;BestiaryPanel.bstTintCache 经 sw:remaster-applied 事件清
- public html 的裸 URL import `'/public/sprites/*.json'` 走静态服务(JSON MIME)→ 模块加载失败;json 一律运行时 fetch
- upgradeToBitmap 在 USE_BITMAP=false 时两个回调都不调 → 先判 USE_BITMAP 再走

**热补丁注入矩阵**:vanilla→`vimages.set`/vanilla-ui→`uiimages.set`/Projectile 双写+setProjSpriteOverride/Buff→buffIconUrl(objectURL)。KvStore **DB v2** 加 remaster blob store( pack+帧像素;onversionchange 让路)。启动应用在 loadAssets 后零竞争(后继懒加载 has 早退)。`__swRemaster` 桥(main.ts);标题菜单「素材包」→RemasterPanel。

素材包 `sw-remaster-pack/1`:manifest(baseVersion=assetVersion 同源 fnv1a36;rect/hash 自带不依赖当前 vanilla.json)+ sheets/ 镜像原版路径混合 sheet png(仅 accepted 帧落重制像素);手写 ZIP_STORED+CRC32 零依赖。素材重打包后重跑 `node scripts/gen-remaster-index.mjs`(10974 张 IHDR 尺寸)。

**遗留**:全量回归 25 失败全为并行会话 worldgen/AI 中间态(海马 626 等,与本管线零交集);真实 gpt-image-2 效果调优(prompt 模板/风格锚 edits 多输入图)待用户实跑;PaperDoll/Background/液体/树冠/NPC 横条(594)二期。

**Review 修复批(2026-08-19 同日)**:8 项全修+复验 66 单测/17/17/7/7——①IDB v2 多标签 blocked 挂死(applyInstalled 8s 超时兜底+onblocked 告警;★onversionchange 只对同代码版本生效,生产首次部署旧页跑旧 bundle 必踩)②Item_Atlas 共享 sheet 的 manifest frames[frameIdx] 互相覆盖→键改 `${entryKey}#${idx}`(rect 自带,应用侧不依赖此键)③叠加对比语义(newcv CSS opacity 露背景格→原帧打底+临时 canvas α0.5 叠;★putImageData 不吃 globalAlpha)④algo select 缺 value(脏字符串碰巧落 box 分支)⑤PackStore 帧像素整行聚合 O(n²)→单帧单行(id=`frame:条目|帧`)⑥readPack sheet 路径白名单(zip 逃逸条目静默丢)⑦versionMismatch 实装(Manager 注入 getBaseVersion,不符警告不拒装)⑧objectUrls 冗余池删。★html 内联 script 是原生 JS——`getContext('2d')!` TS 非空断言=SyntaxError(修复时自己引入,探针即时抓住)。

**整图重制+prompt 增量批(2026-08-19 用户需求)**:62 单测+21/21+7/7——
- **整图模式**:无法逐帧切的素材(excluded:594/690/纸娃娃/液体/树冠/背景)整张 sheet 一个重制单元。★记录键哨兵 `WHOLE_FRAME_IDX=-1`(与逐帧 0 区分);excluded 条目 frames 清空→`every([])=true` 使 complete 只取决于整图记录;普通条目可主动切 whole(进度两模式独立)。布局 `computeWholeLayout`:k 只放大不缩(缩回丢像素);★全库 4577 张比例 >3:1(Acc_Back 40×1120=28:1 类)→ pad 短边修比例+交替扩较小边补面积(收敛近方形,永达不了 3840 上限)。whole 模板核心约束=逐元素原位(do not move/resize/crop——混排表任何位移破坏下游切帧)。导出:-1 记录整图 putImageData,manifest 键 `${key}#-1`。
- **prompt 增量语义**:输入框只放【用户微调】(空=纯默认模板),完整 prompt=默认组装+微调追加(composePrompt userPrompt 从整体覆盖改追加);下方"▸ 完整 prompt"实时预览;FrameRecord.prompt 恒存完整组装。

**整图批 review 修复(同日)**:①★单帧整图条目(ui/gore/glow/buff/misc ~2500 条)whole 模式与逐帧模式重制单元相同却分裂 -1/0 两键=重复重制+进度分母虚增→isSingleWholeFrameEntry() 判定共享键 0(探针断言锁定);②进度(含 prompt 全文历史)与 prompt 微调持久化全迁 **kvSetIdb/kvGetIdb**(新加的只进 IndexedDB 通道;★localStorage 5MB 全局上限迟早被无界增长的验收历史撑爆,kvSet 的 ≤2MB 快路径对此类数据不合适;INSTALLED_KEY 轻元数据仍走 kvSet);③localStorage 反序列化 try/catch 防御(损坏数据炸整页);④whole 模板补窄条居中说明(pad 画布中 40×1120 类主体仅占 6.7% 宽,防模型拉伸填白)。

**效率批(2026-08-19 二轮 review,A-F 全落地;62 单测+26/26+7/7)**:量化定谳=总重制单元 19.2 万(tile 帧占 75%),串行点击-等待 400 工作日不可行。①**A 队列+并发预取**:执行核解耦 `runUnit(entry,frameIdx)`(脱离 curEntry 语境,sheetCache LRU12 跨条目),入队即返不阻塞,人工只验收(闸门保留);R=入队/H=定稿档重出/N=下一未完成;并发数设置(默认4)②**B tile/wall 默认整图**(`wholeModeFor`:753+366 表一次生成覆盖 17.3万帧,单元 ×7 → 2.8 万;条目可手动切回)③**C 两阶段**:试拍档/定稿档分离+QUALITY_COST 计量(顶栏 API 次数/成本估算)④**D 候选 N 选 1**:framePixelsMem 改 `{list[≤4],sel}`(重试不覆盖,candPut/candSel;IDB 只存选中候选,切候选即 putFramePixels)⑤**E 动画预览**:多帧条目胶片条下方 ▶ 轮播(120ms,重制帧优先)⑥**F**:gotoNextTodo(N)+全局进度统计(顶栏)+微调条目级继承(「微调→整条目」)。★patch 教训:多轮 python replace 的锚点会被前序块重构失效(s.replace 不命中不报错)——块序依赖(块2 重构 doRemaster→runUnit 后,块3 的旧锚点失配=新函数静默未插入),大改后必须 esbuild 语法校验+探针即时报 undefined;候选/队列断言入 _remaster-smoke(26 项)。
