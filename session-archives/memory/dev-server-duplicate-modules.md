---
name: dev-server-duplicate-modules
description: 长跑 vite dev server HMR 时间戳分叉导致单例模块双实例；src/*.js 是 tsc 陈旧产物
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-10T04:26:59.279Z
---

2026-08-10 排查"光标不可见"：用户长跑的 vite dev server（game/ 端口 5199）里 HMR `?t=` 时间戳
在各导入链上分叉，同一模块（VUI.ts/UITextures.ts）在一张页面里被实例化两份——main.ts 持有的
实例跑了 init/setAtlas，另一份覆盖 `window.__swVUI` 且绘图循环用的 UITextures 没 atlas →
ui-canvas 全透明零像素。症状是"改了代码但表现诡异/单例失效"，**重启 dev server 即愈**。

相关坑与已做的修复（勿回退）：
- `game/src/` 下曾有 141 个 tsc 编译产物 `.js`（`npm run build` 的 tsc 无 noEmit 时吐在源码旁），
  会以默认扩展序(.js 优先)遮蔽 `.ts`。已加 [[vite-config-ts-first]]：新建 `game/vite.config.ts`
  resolve.extensions 把 .ts 放最前；tsconfig.json 加 `"noEmit": true`（build 的 tsc 只做类型检查）。
- 陈旧 .js 当时未能批量删除（权限拦截），若再出现解析到旧代码，可手动
  `cd game && find src -name "*.js" -delete`。
- vite dev 期间还会偶发整页 reload（依赖预构建），puppeteer E2E 脚本要容忍
  "Execution context was destroyed"（轮询重试）。
