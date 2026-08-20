---
name: menu-sun-layering-fix
description: 菜单"太阳跑到前景前面"根因=TitleMenu DOM 日月体恒可见垫整画布之上;修复=常态隐藏仅抓取中显示;画布太阳才是原版语义
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T10:12:19.236Z
---

2026-08-13 用户报"首页背景的太阳跑到前景层前面,点单人游戏开面板就自己好了"。

**根因(探针实证,非猜)**:标题菜单有**双太阳**——①画布太阳(MenuBackground.sky.draw,
树/山层之前画=被遮挡,原版语义正确);②TitleMenu 的 DOM 日月体(`.sw-title-celestial
.body`,GOING_OLDSCHOOL 日月拖拽批引入),z-index -1 在 TitleMenu(z15)stacking context
内=**结构性垫在整块画布之上**,盖住山/树前景,且**无可见性门控恒 opacity 1**。
"开面板就好"=开面板销毁 TitleMenu(titleMenu?.destroy())→DOM 太阳消失,与画布无关。

**修复**:`.body` 常态 `opacity:0` + `.grabbing .body{opacity:1}`(仅拖拽抓取中显示=
跟手游标下的可见反馈;画布太阳经 onSunMoonGrab→setClockT 横移同步,DOM 体补垂直跟手
modY)。探针验证:常态 0/抓取 1/释放 0/画布太阳在(拨正午像素采样 (640,160)=
(254,245,204) 暖亮——首个 warmRatio 探针假阴性是采样格 y 偏 20px)。

**排查方法论**:
- DOM 层盖 canvas 层序问题时,同画布内画序分析无解——先枚举所有 canvas/DOM 层的
  z-index 结构(TitleMenu 注释 :89 自述"必在天空画布之上"=设计者明知)
- **像素级判定**:page.evaluate 里 canvas.getContext 采样 vs 合成截图隐藏元素前后
  diff——判定"前景元素=哪个层"的决定性手段;ASCII 渲染截图(pngjs 亮度字符)可
  直接目检合成画面构成
- 采样行要对着**层几何**(variant 4/style 7 树在 y≈452+,我首测 0.45H=360 落在层间隙
  得出"前景没画"的错误结论——先用 drawLayer 的 y 公式算准带位再采样)

**遗留**:51203 私有实例清理被分类器暂不可用挡住(pid 3861/3813,SW_CACHE=/tmp/
sw-vite-5203)——下次会话 pgrep 后 kill。

相关:[[parallel-vite-sessions]] [[systems-final-batch]] [[asset-lazy-loading]]
