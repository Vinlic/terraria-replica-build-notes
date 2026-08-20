---
name: mobile-controls-port
description: 移动端适配：触摸合成(Input.touchKeys/世界触摸长按=右键)/虚拟控件层(摇杆跳跃攻击光标钩爪药水)/横屏全屏；钩爪最小引擎；探针_mobileprobe 20步
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T03:21:21.561Z
---

移动端适配（2026-08-13）。零侵入设计：**所有按键合成注入既有 Input 语义**，游戏消费链（updateUse/移动/智能光标 updateWanted）完全复用桌面路径，桌面端零渲染零影响。

**架构**：
- `Input.touchKeys`：虚拟键集，`down()` 与物理键盘同权（uiBlocking 门一致生效）。摇杆→KeyA/D/W/S、跳跃→Space、智能光标→ControlLeft（Toggle 模式 rising edge 翻转 wanted，复用 SmartCursor.updateWanted）。
- 世界触摸合成（Input 构造器内 el=renderer.canvas）：touchstart=左键按下+光标定位、touchmove=瞄准（>12px 移动取消长按）、**长按 400ms=右键交互脉冲**（rightDown，开箱/对话/门）、touchend 全清。UI 面板/控件元素 closest 跳过（原生 click）。preventDefault 阻浏览器合成鼠标。
- `src/ui/MobileControls.ts`：控件层（.sw-mobile，仅触屏设备渲染）。左侧摇杆（死区 0.35，R=46）+跳跃；右侧攻击（mouseDown 边沿+mouseHeld 电平，悠悠球 channel 语义正确）/智能光标/钩爪/药水/坐骑宠物；⛶ 全屏按钮（requestFullscreen+orientation.lock('landscape')，iOS 静默降级）+竖屏提示横幅。1s 节流刷新按钮态（药水 lit=有药+受伤；钩爪/坐骑按 miscEquips 显隐）。
- 钩爪最小引擎：`GrappleProj`（飞→锚定→写 player.grappleTarget；Player.fixedUpdate 移动积分前朝锚点恒速 13.5 覆盖 vx/vy）+`Game.useEquippedGrapple`（再按收回）。释放三条件在 proj 内终结（抵达 24px/按跳/再按）——Player 侧只清 target 不杀弹（弹活着会重写）。AI_007 全量移植后替换。
- `Game.quickDrinkPotion(kind)`：扫包首瓶 itemFunc consumable healLife/healMana 直饮（=updateUse vi_ 消耗品桥接段镜像）。
- mainFlow：enterGame 建控件层+手势内 tryFullscreenLandscape；quitToMenu destroy。

**坑**：
- Input 的 el 是 **renderer.canvas** 不是 #game-root——探针合成 TouchEvent 必须派发到 `g.renderer.canvas`（querySelector('canvas') 会抓到别的画布）。
- 合成事件同 turn 连发 touchstart/touchend 时游戏 tick 看不到电平——探针需 ≥120ms 间隔（真机按压自然满足）。
- 坐骑/宠物键为占位 toast（引擎未实装，矿车除外）；l10n 键 `Mods.SandboxWorld.Toast.MobileRideTodo`。
- index.html viewport 加 maximum-scale=1+user-scalable=no+viewport-fit=cover；#game-root/canvas 加 touch-action:none。
- 探针 `scripts/_mobileprobe.mjs`（hasTouch+isMobile 视口，TouchEvent 合成）20 步全绿。

**视觉批（2026-08-13 第二轮）**：
- `mobileUiScale()`（触屏=0.7）：小地图 drawMinimap 右锚 ctx 缩放变换整体缩（框贴图/按钮/时间面板随变换自动缩）；**两处鼠标读点须逆变换**（lmX/lmY 右锚逆式）——悬停命中 + 时间/天气面板 hit；`minimapRect` 存屏幕坐标（外部点击检测）。资源条（Fancy/Classic 两样式）Renderer 调用点右锚缩放包裹。
- VUI.drawCursor 触屏早退（原版移动端无指针精灵）。
- 控件美化缩小：玻璃拟态（backdrop-filter+径向高光+内描边+按压 scale 0.93）；摇杆 150→118（R=38）、跳跃 74→58、攻击 96→72、簇按钮 62→46/42、⛶ 38×30。
- 智能光标键改**同步脉冲**（`Game.pulseSmartCursor` 直调 updateWanted）——不依赖 tick 窗口，防 headless rAF 节流 flake（探针教训：同 turn 连发 touchstart/end 时电平不可见）。
- ★ 钩爪引擎被并行会话全量重写（AI_007 1:1：GrappleProj 三态/grappleHooks.ts 全表/Player.grappleMovement/quickMax 门/双钩交替/月钩轮换）——我的最小实现作废，useEquippedGrapple 由他们重写为 QuickGrapple_GetItemToUse 语义（**原版无收回键，释放=跳键**；再按=单钩族替换/拒发）。收回循环遍历副本防 unregister splice 跳元素。
- 探针 ⑧ 对齐原版：再按存活 ≤1（弹桶计数——挂墙钩在登记表+弹桶双出现，**勿相加双计数**）；跳键释放锚定钩。
- 私有端口教训：5201 会被并行会话掀掉——遇 ERR_CONNECTION_REFUSED 换 5202 起实例。
