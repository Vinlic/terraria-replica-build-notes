---
name: diag-script-orphan-prevention
description: "诊断脚本必须经 tools/run-diag.mjs 运行,禁止裸跑 vite-node/npm exec,防 100% CPU 孤儿进程"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e65c4575-731a-43e0-a377-ccf50cc42db3
  modified: 2026-08-13T04:36:30.333Z
---

2026-08-10 事故:发现 7 个 `vite-node tools/_diag-gen.mjs` 孤儿进程各占满 1 核空转 4 小时(脚本文件已被删、shell 已退出、TERM 无效)。根因:诊断脚本 import 链带起不可退出的活句柄,且无任何超时兜底。用户指示杀掉并防再犯。

**Why**: 一次性诊断脚本的进程不退出不会报错,只会在后台默默烧 CPU;SIGTERM 对忙循环进程无效,必须 SIGKILL。重复跑多次就会累积成多个满核孤儿。

**How to apply**:
- **所有 `_diag-*.mjs` 一律经 `node tools/run-diag.mjs [--timeout=ms] <script.mjs>` 运行**(game/tools/run-diag.mjs,双层架构:子进程导入完成 0.5s 强制退出 + 父进程看门狗 SIGKILL,已用 4 种卡死形态实测:残留 interval/永不 resolve 的 await/同步 while(true)/退出码透传)
- **禁止**直接 `npm exec vite-node tools/_diag-*.mjs` 或裸 `node tools/_diag-*.mjs` 跑诊断(vite-node 额外带 Vite 运行时活句柄)
- 在会话里跑长任务优先用 Bash 工具的 `timeout` 参数(超时会杀命令)而非放任后台
- 删除诊断脚本文件前,先 `pgrep -fl <脚本名>` 确认无进程(孤儿进程不会因文件删除而死)
- 巡检命令:`ps -Ao pid,etime,pcpu,command | awk '/node/ && $3+0 > 50 && $2 ~ /:/'`(跑超 10 分钟且 CPU>50% 的 node 几乎必是死循环孤儿)
- 需要外部超时兜底时用 `gtimeout`(brew coreutils)
- **spawn 起子 server 的探针(2026-08-12 新增坑)**:`server.kill()` 只杀 npx 包装进程,真实 tsx/node 子进程存活占端口——第二次跑连的是旧代码服务器,症状是"改了源码但行为不变"。防法:`spawn(..., {detached:true})` + `process.kill(-pid, 'SIGTERM'|'SIGKILL')` 整组击杀(见 game/scripts/_netfake.mjs spawnServer);探针自管生命周期时(_roomprobe/_loadprobe 这类分钟级,run-diag 的 0.5s 强退不适用)必须带总时长看门狗并在所有退出路径先击杀 server 进程组
- run-diag 只适用于"导入即完成"的同步诊断脚本;异步长流程探针禁止经它跑
- **puppeteer 探针泄漏(2026-08-13 清理 66 进程/736 临时目录)**:探针被超时/权限击杀时跳过 `b.close()`,headless Chrome 成孤儿累积占内存。防法:browser 在 `try { ... } finally { await b.close() }` 里;SIGINT/SIGTERM 处理器也要 close;巡检清理 `pkill -9 -f puppeteer_dev_chrome_profile` + `rm -rf ${TMPDIR}puppeteer_dev_chrome_profile-*`(只匹配 puppeteer 特征串,不会误伤用户正常 Chrome)
- **自动收割已上线(2026-08-13)**:`tools/orphan-reaper.sh` + LaunchAgent `com.user.orphan-reaper`(每 5 分钟)。三重门:类别白名单(puppeteer Chrome/`_diag-*` 10 分钟、tsx 探针 30 分钟、C# oracle 60 分钟)+ 孤儿(ppid=1)+ 超时,Chrome 家族递归击杀;age 解析失败一律跳过(宁漏杀不误杀);日志 `~/Library/Logs/orphan-reaper.log`。手动:`tools/orphan-reaper.sh --dry-run`。已知坑:bash 对 etime 前导零按八进制解析,必须 `10#$n` 强制十进制

相关:[[sandboxworld-project-setup]] [[multiplayer-capacity-opt-batch]]
