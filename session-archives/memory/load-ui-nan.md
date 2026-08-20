---
name: load-ui-nan
description: 读档换 UIWorldLoadState(创建世界同款 VUI 页)+NaN% 三端防御;真源疑=HMR 新旧 JS 混跑(p 语义切换期)
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T05:40:48.923Z
---

2026-08-13 用户报"进存档 UI 还是旧的 + NaN%"。

**旧 UI 根因**:读档两入口(mainFlow loadFromKey/loadFromJson)走 `ui.showProgress`(DOM 旧进度条),创建世界走 `UIWorldLoadState`(VUI 原版风加载页)——两套并存。修复:读档 worker 路径 + 主线程 fallback 共三处全部 `new UIWorldLoadState(); VUI.setState(loadState);` 接 `loadState.setProgress`;失败 catch 补 `VUI.setState(null)` 退场。进游戏清理由 enterGame→stopMenu(:128→:396 VUI.setState(null))自动完成,与创建路径同链。

**NaN% 防御(三端)**:loadProgressLabel(`Number.isFinite(rawP)?rawP:0`)、UIWorldLoadState.setProgress、ui.showProgress(width NaN% 根治)。

**真源离线推导**:settle p 现为收敛比例 `(num5-cur)/num5`(全数字链不可能 NaN)、tiles i/nAll 亦然——新代码无 NaN 面;最可能 = **HMR 半更新新旧 JS 混跑**(settle p 语义从 iter 计数切收敛比例的瞬间,worker 旧码发旧 p/主线程新码按新语义映射)或构建缓存陈旧。防御已兜底;若用户 F5 后仍现 NaN,需带现场栈再查(hook 方案在 scripts 已删,重建参考本条)。

**教训**:跨 worker 协议改 p 语义时,新旧混跑窗口的 UI 必须加 isFinite 防御——比"保证不发 NaN"便宜得多。

相关:[[load-progress-vanilla]] [[load-perf-batch]] [[dev-server-duplicate-modules]]
