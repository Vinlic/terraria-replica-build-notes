---
name: weapon-invisible-remaster-pack
description: "武器/弹幕全隐形真根因=worldLayer离屏重构(1b369fe2)后实体仍r.canvas.getContext直取主画布;76处迁r.ctx;★我此前\"fresh全绿\"是采样误测被用户当场戳穿"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-19T15:58:02.766Z
---

# 武器全隐形事件(2026-08-19 晚)真根因与修复

用户报"所有武器贴图/弹幕/投掷物(荧光棒)全隐形但功能正常",dev 5199+PROD 4173+play2 全新 profile 全坏。

## 真根因(绘制调用级插桩定谳)
- 今晚 `1b369fe2`(19:4x)新增 **worldLayer 离屏系统**(Renderer.ts beginWorldLayer/endWorldLayer,:2321/:2663):世界段 ctx 从主画布切到离屏世界层再合成
- 但**全弹幕家族 39 文件 76 处** `r.canvas.getContext('2d')` 直取主画布(Arrow/WeaponProj/Bobber/bossAI_* 等)→ 画在主画布**裸世界坐标**上(设备坐标 (6156,3840) vs 画布 1280×800 = 屏外数千像素),世界层随后合成盖掉一切
- 症状全闭环:全弹幕隐形/武器功能正常/世界与玩家正常(它们走世界层)/全环境通吃/"下午健康→晚上全挂"(提交时间吻合)
- **修复=76 处统一改 `r.ctx`**(beginWorldLayer 已把 this.ctx 切到世界层;GrappleProj.ts:260 本就是正确先例);11 文件内联结构类型 draw 参数补 `ctx: CanvasRenderingContext2D` 字段;4 个测试桩(canvas:{getContext})同步
- 验证:drawImage 插桩记录 CTM——修前 glow 矩阵 e=6156(裸世界)→ 修后 e=474/scale1.12/落点 (464,406) 屏幕正中;4173+5199 双源绿

## 我的两轮误诊(用户"是不是误测"一针见血)
1. **第一轮误测**:像素采样窗既没对准弹幕(相机坐标公式少半屏偏移,弹幕又飞出窗外),opaquePx 计数全是世界背景噪声——`持械挥击 gain:0` 这种真信号反而被我用"noGraphic 属设计"解释掉了
2. **第二轮误诊 remaster 包**:dev 也坏其实已排除 SW 缓存,我仍把"用户浏览器 IndexedDB 有包 vs 我没有"当成根因——play2 全新 profile 也坏一测戳穿
3. **正确姿势=drawImage 原型级插桩+getTransform 矩阵普查**:记 (on main/off, dev 落点, a/e/f) 一次跑就能分辨"画了没/画在哪/什么变换"——比像素采样可靠一个量级

## 顺手落地的防线(仍有效,与本次根因无关)
- RemasterRuntime.apply 全透明 sheet 拒注(canvasHasContent+probeContent DI 第 4 构造参)+appliedFiles/rejectedBlank 进 F5 报告 remaster 段+Manager.applyInstalled 启动日志
- Arrow.projSprite TTL 重试(坏 Image 永久驻缓存真 bug);★upgradeToBitmap 在 USE_BITMAP=false 时**两个回调都不调**——onload 须先判再 land;node 同步装载替身须"当次即返"再查缓存(旧契约)

## 遗留
- HEAD 带 57 个 tests/ tsc 错误(另一会话改 TownNPC 构造 4→3 参未跑测试)→ `npm run build` 的 tsc 步卡死,只能 `npx vite build` 绕过;待修
- 16 个 caves-oracle 对账失败=另一会话工作树未提交的 worldgen 改动(CaveHousePass/QuickCleanupPass/Spread/SurfaceDecorPasses),先于本次存在
- 主画布 24×22@e=2917 每帧绘制=天空层环境鸟(屏幕坐标系合法,视差屏外裕量),非漏网
