---
name: debug-report-warn-ring
description: F5 调试报告 errors/warnings 双环架构——main.ts 钩 console.error/warn 写 globalThis 环，报告零散接线
metadata: 
  node_type: memory
  type: project
  originSessionId: 8f9c7b63-58b1-49de-a435-85fe12e156d6
  modified: 2026-08-12T08:04:10.094Z
---

F5 调试报告（src/debug/DebugReport.ts，2026-08-12 起）的横切数据源是 **globalThis 锚定的双环**：

- `__swErrors`（cap 50）：pageerror / unhandledrejection / console.error 钩子写入（main.ts）
- `__swWarns`（cap 50）：console.warn 钩子全量捕获——渲染层 warn-once（如 VanillaTiler 源矩形越界/取帧失败，见 [[id-space-collision-pot-bug]]）无需单独接线自动入环

**Why:** 与错误环分离防告警刷屏挤掉真错误；挂 globalThis 免疫 HMR 模块双实例（[[dev-server-duplicate-modules]]）——任何模块实例的 console.warn 都进同一个环。报告读环默认 `globalThis`，测试经 `DebugReportOptions.{errors,warnings}` 注入。

**How to apply:** 新子系统要进报告的告警，直接 `console.warn('[模块名] ...')` 即可（前缀便于过滤）；结构性数据走 `DebugStateProvider.debugState()` 钩子，不要往环里塞大对象。多会话并发时 DebugReport.ts/main.ts 是共享热点，改动前先看对方最新版本。
