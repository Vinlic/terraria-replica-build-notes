---
name: asset-zip-bundle
description: 资源 zip 分片打包+页面 worker 直给解压入 Cache API;12003 请求→8 片;SW 只做 cache-first 服务;构建增量重打包
metadata:
  type: project
---

资源下载 zip 化（2026-08-19 定稿，461MB/12003 文件 → 8 片 363MB）：

**终版架构（用户拍板三轮迭代后）**：
- `scripts/pack-assets.mjs`：五目录超集（fonts/vanilla-ui/vanilla/sounds/audios/music，l10n 排除=网络优先可变；三个 json 已进 bundle）→ 64MB/片、≤4000 文件 → 8 片；sha1 清单 mtime+size 快路径（<2s 跳过）；逐片 inputHash 复用（单文件变更只重打 1 片）；★fflate zipSync 必须 `mtime` 钉死 2000-01-01（默认内嵌当前时间→跨进程字节不确定→同内容换名）；GC 孤儿。
- **页面直给驱动**（`AssetCache.startZipWarm`）：预计算每片 missing（cache.keys 一次）→ 专用 Worker（`asset-warm.worker.ts`）循环 `fetch(片)→unzipSync(整片)→128 文件/批 postMessage(transfer)` → 页面 `cache.put`（★Cache API 仅 Window/SW 可用，worker 无）→ 进度 emit。终态 failed>0 停机等"重新下载"（force=重建 worker 重扫，have-set 只补缺）。
- **SW 零参与 warming**（只留 cache-first 服务 + init gcOldCaches）。版本 = fnv1a(旧版|manifest.contentHash)——资产内容变自动换缓存名。

**走过的死路（勿重蹈）**：
1. SW 内解压：fflate 异步 API 内部 new Worker，SW 无 Worker 构造器只能 unzipSync(filter)；更致命是嫁接旧 warm 状态机（watchdog/autoRetries 轮次）→ 坏片无限重发 + 4 轮全扫 0% 回卷（用户两次打断）。**解压/下载重活给页面 Worker，别碰 SW 生命周期。**
2. worker 内相对 fetch 解析到 /assets/（worker URL 为基）→ 必须根相对 '/assets-zip/...'。
3. showTitle 的 warmAllAssets 抢在 manifest 拉取前 → enabled=false 被吞后无人补调 → 永久 idle；initAssetCache 尾部自补一脚。
4. zip fetch 必须 `cache:'reload'` + zipBytes 长度校验：并发 build 期截断体会被 ETag 钉死成 0.1KB 垃圾体。
5. 探针口径：请求计数含 SW 缓存命中（Combat_Text 等每帧重取是既有零成本行为）——验"走没走 zip"要数 404/网络未命中。
6. files 批与 done 消息异步交错 → done 计数超 total，在 assetCacheState() 边界钳制。

**dist 形态（用户选 C）**：prune-dist.mjs 裁 sprites/vanilla+sounds+audios/music（-401MB→405MB），保留 vanilla-ui 全量（首访菜单）+l10n+fonts+audios 平铺 main/title.mp3；`PRUNE_DIST=0` 全量兜底；★?nosw 进图无散件（已接受）。npm build 链=build-l10n→pack-assets→tsc→vite build→prune-dist。

E2E `scripts/_swzip-probe.mjs` 四幕全绿（404=0/断网 3s 续传完成/缓存桶=11932 精确/断网 reload 菜单+标志）。相关 [[asset-lazy-loading]] [[sw-asset-preload-port]]。
