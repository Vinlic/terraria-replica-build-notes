---
name: sw-asset-preload-port
description: SW 资产持久缓存全链:分块接力warm(单发全量会被SW~3min击杀)/门槛弹窗像素风/scheme门/离线壳缓存;E2E双探针全PASS
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T14:53:56.236Z
---

2026-08-13 用户要求:进主菜单即按优先级**全量下载**(~540MB 贴图+音效+音乐)到浏览器
磁盘,右下角悬浮进度;单人游戏未完成则弹窗等待(实时进度条)完毕自动放行;被清理
自愈;不重复下载。决策:门槛=全部资产;dev 不启用(仅生产+?sw=1)。

**架构(四件)**:
1. `public/sw.js`:fetch 拦截——资产前缀 cache-first;**壳层(文档+vite hash JS/CSS)
   网络优先+离线回退**(真断网可玩);activate 清旧版本缓存。message 协议
   {init/warm(base 偏移)/status(附 lastWarm 统计)/warm-cancel}。**version 随每条
   消息走**(SW 被杀重启后内存版本丢失——无状态化)
2. `src/net/AssetCache.ts`:版本=fnv1a32(vanilla.json+vanilla-ui.json+CACHE_BUSTER
   手填闸);优先级清单纯函数 P0菜单→P1游戏贴图→P2其余(assets-index.json)→P3音效
   852→P4音乐(MUSIC 表,0=None 跳过)=11224 项;**分块接力**(块 500,页面发块/
   done 消息接下一块)+看门狗(当前块停滞 15s 补发,SW keys() 过滤=断点续传)+
   完成时失败自动重拉(≤3 轮,keys() 只补失败);F5 systems.assetCache 段;
   __swAssetCache 调试句柄
3. `src/ui/AssetDownloadUI.ts`:右下角徽标(steps(8) 跳变旋转=像素感)+门槛弹窗
   **像素风**(用户点名):面板=Inventory_Back13 九宫格×(33,15,91)×0.685(UI.ts 同源
   算法)、进度条=原版世界创建条 1:1(UI_WorldGen_Outer_Corrupt 框+570×16 槽#303030
   +腐化紫 packed 4283888223,UIGenProgressBar.ts 常量)、全程方角/硬边框/像素字体
4. `scripts/vanilla-atlas.mjs` 尾段产 `public/assets-index.json`(sounds/fonts/l10n/
   miscVanilla/miscUi 清单;★只改音频/字体需手动重跑或 bump CACHE_BUSTER)
挂点:main.ts initAssetCache(门=PROD&&secure&&!nosw,?sw=1 强制);mainFlow showTitle
warmAllAssets+mountAssetBadge(**注册异步晚于 showTitle→徽标订阅 enabled 翻真再挂**);
单人 handler 包 gateAssetsOrRun(仅单人,多人/设置不拦)。

**血泪坑(全部 E2E 实证)**:
- ★**单发全量 warm 必死**:Chrome ~3min 击杀 SW(并发 3/6 都死,页面堆平稳=死的是
  SW 非 OOM)→ 必须页面分块接力(块粒度远小于死亡窗口)
- ★message 处理器 **必须 e.waitUntil(warm(...))**——首版当废料删了,warm 几秒即死
- **cache.put 拒绝 chrome-extension://**(扩展注入请求也进页面 SW,用户实报
  "Request scheme unsupported")→ fetch 处理器最前加 `protocol!=='http(s)' return`
- pathname 归一:cache 条目=绝对 pathname(带/),清单=相对路径——比对前剥前导/
- 探针断言必须对着真实 DOM 类(CharSelectPanel 根类=**sw-list-panel**,
  `[class*="char"]` 猜错浪费两轮)
- 限速期 fetch 失败会卡死门槛(failed>0→assetsComplete 恒假)→ 完成时自动重拉≤3 轮
**E2E 双探针全 PASS**(build+preview 5311):主探针(注册/11224 零失败/CDP 断网 reload
菜单照常/删缓存自愈补下)+gate 探针(1.5Mbps 限速点单人→弹窗实时进度→解除限速→
64%…完成自动放行)。单测 8+lint 3。

## 同日可靠性 review(用户问"失败自动重试?多次失败给按钮?")
**四层重试链(全部实测)**:
1. SW 单文件即时重试 ×3(300/600ms 退避)——弱网瞬断就地恢复
2. 整轮自动重拉 ×3(全量跑完仍有 failed→cursor 归零重扫,keys() 只补失败,极快)
3. 门槛弹窗"重新下载"按钮(3 轮耗尽+settled 后显示)→ warmAllAssets(**force**)
4. 徽标失败终态常显"资源下载失败 N 项"(不淡出,菜单可见)
**★review 抓到的致命雷**:重试按钮原本是死的——warmAllAssets 的"已完成早退守卫"
(done>=total&&cursor>=len)在 3 轮重试耗尽后恒真,按钮点击 no-op=用户永久卡死。
修=force 参数绕过守卫+cursor/done 归零;scripts/_swretry-test.mjs 合成验证
(删 3 条缓存→warm(true)→补齐回满 complete=true)。
**另修**:register({updateViaCache:'none'})(防 sw.js 被 HTTP 缓存卡 24h 部署不
更新);status 满缓存早退(免每菜单 23 个空块×11k keys() 扫描,实测 force 全扫
一轮 ~2min——按钮路径可接受)。force 重扫会短暂把进度条打回 0%(诚实语义,保留)。

相关:[[asset-lazy-loading]] [[parallel-vite-sessions]]

**自适应并发(2026-08-18 用户"按下载/处理速度自适应并行")**:warm 曾固定
3 路;改 AIMD——单文件完成延迟 EMA(仅成功样本,重试等待不计入防污染),
每 32 文件调参:ema<30ms 升 1 路(封顶 8:HTTP/1.1 同源 6 连接,更高无意义)、
ema>150ms 路数减半(下限 2)。固定开 MAX 路 worker + 动态信号量闸(升降路
不重建池);400 文件 250ms 喘息保留(磁盘落盘缓冲)。warm-done 回包附
conc/emaMs 可观测。★SW 更新要 updateViaCache:'none'(已配),sw.js 变更
后老 SW 最长 24h 才换——dev 验证需 DevTools→Application→Service Workers
勾 Bypass/Unregister 重注册。