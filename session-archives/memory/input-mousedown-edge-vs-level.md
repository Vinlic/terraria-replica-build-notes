---
name: input-mousedown-edge-vs-level
description: "input.mouseDown 是边沿消费量(use 后清零),channel 类滞留判定必须用 mouseHeld 电平量——阳炎之怒出生 1 帧即死根因"
metadata: 
  node_type: memory
  type: project
  originSessionId: cc0b5a07-65b0-46a9-b141-4257ee7a1554
  modified: 2026-08-12T16:34:42.627Z
---

2026-08-13 修"阳炎之怒(Sunfury, item 220 → proj 35, aiStyle 15=AI_FLAIL)使用没起效":链球掷出 1 帧即死。

根因:`Input.mouseDown` 由 mousedown/mouseup 事件维护,但 Game.ts 有 16 处 use 代码用完即置 false(边沿消费语义)。`case 'yoyo'/'flail'`(Game.ts ~4303)掷出后清 mouseDown,而 YoyoProj.channel 回调又查同一个 `input.mouseDown`——真实浏览器"按住"只发一次 mousedown 事件,清掉后无事件回填,channel 恒 false → 出生 1 帧进回收分支消失。悠悠球同分支同样中招。

修法:Input 加 `mouseHeld`(mousedown→true/mouseup→false/blur 清,不被消费),channel 回调改用 mouseHeld。探针 `scripts/_sunfury-probe.mjs`(4 断言全绿)。

**Why:** 边沿量(一次性动作)与电平量(持续按住)是两种语义,共用一个字段必出"出生即死"类 bug。

**How to apply:** 新增"按住期间滞留/持续"判定一律用 `input.mouseHeld`;一次性点击门(`mouseDown && useTime===0`)继续用 mouseDown。探针模拟按住时要同时设 `mouseDown=true; mouseHeld=true` 且全程不重设。相关 [[parallel-vite-sessions]]。
