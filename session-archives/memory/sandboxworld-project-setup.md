---
name: sandboxworld-project-setup
description: SandboxWorld 泰拉瑞亚复刻项目的位置、运行方式与测试脚本
metadata: 
  node_type: memory
  type: project
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-11T03:00:22.695Z
---

泰拉瑞亚风格沙盒游戏（Web/TS）位于 `~/Project/GLM/SandboxWorld/game/`（2026-08 从零构建）。

- **运行**：`npx vite --port 5199 --strictPort`（5173-5175 被用户其他项目占用，必须用固定端口）
- **E2E 测试(推荐,2026-08-11 起)**:`node scripts/run-e2e.mjs <script.mjs>` 或 `npm run e2e -- <script.mjs>`——自动 `vite build` 冻结版本 → `vite preview` 静态服务(5299,无文件监听)→ 注入 `URL` 跑脚本 → 进程组收尾。**禁止再把 E2E 脚本直连 5199 dev server**:dev server 有 HMR,测试期间会话里改任何源码都会整页重载,废掉 puppeteer 页面状态/waitForSelector 上下文/__swGame 句柄(历史踩坑:_potprobe/_biomeaudio 里的"HMR 防抖"注释就是在补这个);`--skip-build` 或 `NO_BUILD=1` 复用 dist,`PORT` 改端口
- **冒烟/功能测试**(直连 dev server,仅限交互调试手动跑):`URL=http://localhost:5199 node scripts/{smoke,interact,combat,m4,boss}.mjs`;调试句柄 `window.__swGame`(mainFlow.ts:85 创建世界后才挂载,主菜单阶段是 undefined,探针勿误判)
- **单测**：`npx vitest run`（含真实 wld 导入固件 `game/Starter_World Master.wld`）
- **格式参考**：`~/Project/GLM/SandboxWorld/Terraria-Map-Editor/`（TEdit 仓库，只做 .wld 格式与数据表参考，不含游戏贴图；FileType 枚举 Map=1/World=2）

**Why:** 端口冲突曾导致冒烟测试测到别的应用；测试脚本体系已验证全部核心玩法链路。
**How to apply:** 改动后跑 vitest + 对应场景脚本验证(场景脚本一律经 run-e2e.mjs,勿直连 dev server);不要照抄 TEdit 的 C# 实现逻辑。

## 开局配置原版化（2026-08-11，用户令"只给原版默认装备"）
- 新角色 = 铜三件（copper_pickaxe/copper_axe/copper_sword——自研 def，**挖掘系统依赖 ITEM_DEFS[].tool 元数据**，vi_3506/3507/3509 无 tool 字段不能直接给），无护甲/配饰/药水/电路包（旧调试全家桶已删）。
- **调试道具入口**：背包面板"🔍 道具搜索"按钮（UI.ts openItemSearch，原版无此按钮）——按 名称/key/原版id 过滤全 ITEM_DEFS，点击入包（可堆叠给≤99组），关闭背包自动关。标签硬编码不入 l10n（生成产物 12 语言）。
