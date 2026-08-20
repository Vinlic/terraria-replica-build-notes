---
name: parallel-vite-sessions
description: 并行会话打断探针的根因=共用 5199 HMR 重载;解法=SW_PORT/SW_NO_HMR/SW_CACHE 私有静默实例 + 探针 SW_ORIGIN
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-12T06:47:43.976Z
---

2026-08-12 用户报告:多个并行会话跑 puppeteer 探针时被其他会话的源码编辑触发 HMR/full-reload 反复打断(navigation 错误 retry 循环)。

**根因**:全体会话共用 5199 一个 dev server;HMR 推送(full-reload)把连接中的探针页面整个撕掉。vite 的 reload 全部走 HMR websocket——关掉 hmr 即无任何推送;watcher 仍正常失效 transform 缓存,探针每次 `page.goto` 都拿最新代码,稳定性与新鲜度兼得。

**已落地的机制**(vite.config.ts):
- `SW_PORT`(缺省 5199)/`SW_NO_HMR=1`(关 HMR)/`SW_CACHE`(独立预打包缓存,防多实例 optimizeDeps 竞争)
- `server.strictPort=true`:端口被占直接报错,不静默漂移(防 [[dev-server-duplicate-modules]] 的双实例错位复发)
- scripts/ 全部 169 个探针已扫成读 `SW_ORIGIN` 环境变量(缺省回退 http://localhost:5199)

**协作约定(每个跑探针的会话都要遵守)**:
1. 起"私有静默实例":`SW_PORT=52xx SW_NO_HMR=1 SW_CACHE=/tmp/sw-vite-52xx nohup npx vite > /tmp/vite-52xx.log 2>&1 &`(端口按会话错开:5201/5202/…)
2. 探针跑法:`SW_ORIGIN=http://localhost:52xx node tools/run-diag.mjs scripts/_xxx.mjs`
3. **任何会话不得 kill 5199**(共享实例,人工试玩 + 无探针会话用)
4. 会话收尾 kill 自己的 52xx 实例(pgrep 防孤儿,见 [[diag-script-orphan-prevention]])
5. 纯 vitest 单测不需要 server,不受影响

**残留风险**:编辑 vite.config.ts 本身会令所有运行中的实例各重启一次(一次性成本);编辑后新实例才带新配置。5199 保留 HMR 供人工试玩。

验证:_wfprobe6 打 5201 私有实例跑通(load ok + falls dump);期间另一会话继续改源码页面不再重载。

**用户指令(2026-08-12,长期有效)**:所有要跑浏览器探针的会话必须用私有静默实例;不得 kill 5199;收尾 kill 自己的实例。新会话若不知情,直接把下面这段广播给它:

```
【并行会话 vite 防打断约定——请立即遵守】

问题:我们共用 5199 一个 dev server,任一会话改源码会触发 HMR 全页重载,
把其他会话正在跑的 puppeteer 探针页面撕掉(navigation 错误反复 retry)。
机制已落地:vite.config.ts 支持 SW_PORT/SW_NO_HMR/SW_CACHE 环境变量,
全部探针脚本已支持 SW_ORIGIN。

从现在起,凡是需要跑浏览器探针(scripts/_*.mjs 经 run-diag)的会话:

1. 起自己的"私有静默实例"(端口按会话错开 5201/5202/5203…,先 pgrep 确认没被占):
   SW_PORT=5201 SW_NO_HMR=1 SW_CACHE=/tmp/sw-vite-5201 \
     nohup npx vite > /tmp/vite-5201.log 2>&1 &
2. 探针一律带自己的 origin:
   SW_ORIGIN=http://localhost:5201 node tools/run-diag.mjs scripts/_xxx.mjs
3. 禁止 kill 5199(那是共享实例,人工试玩用);也禁止动别人的 52xx 端口。
4. 会话收尾时 kill 掉自己的 52xx 实例(先 pgrep 再 kill,防孤儿进程)。
5. 纯 vitest 单测不需要 server,不受影响,照常跑。

注意:SW_NO_HMR=1 只是关闭向已连接页面的 reload 推送,watcher 和代码
新鲜度不受影响——每次 page.goto 仍加载最新源码。编辑 vite.config.ts
会让所有运行中的实例各重启一次,尽量少动它。
```
