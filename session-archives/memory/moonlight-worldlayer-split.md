---
name: moonlight-worldlayer-split
description: 夜月不亮根因=compositeLight全屏乘光吞天空；修=世界层离屏画布+光照按层alpha成形（原版分层语义）
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-19T10:13:40.205Z
---

月亮光照分层修复（2026-08-19，用户实报"夜里的月亮怎么不会亮"+772MB Trace 全文零
Moon_/Sun_ 光栅记录）：

- **根因**：compositeLight 是**全屏 multiply**（Renderer 架构注释自认"全屏 pass"
  是唯一光照通路——实体/贴图全靠它）。天空区域光照 = 月光地板 ~21/255 → 夜空整体
  压暗到 8%：月亮 241→~20、星星、夜空渐变全黑。白天环境光满 255 → 乘白无感——
  所以只有夜里暴露（月亮/星星"不亮"、夜空纯黑而非暗蓝）。
- **修法（原版分层语义）**：原版 tile/NPC 绘入 RenderTarget 乘光、sky 直绘
  backbuffer 不进光照。本仓落地：
  - render() 世界段（世界变换块 + 屏幕空间世界 pass 到 LitNature 光晕止）切
    `this.ctx`→worldCanvas（beginWorldLayer/endWorldLayer 换层对，天空段仍直绘主画布）。
  - compositeLight 新路径：光照栅格先画进 lightMaskCanvas，`destination-in`
    worldCanvas 按层 alpha 成形（★multiply 直画会把透明区糊成光色，必须先掩膜），
    再 multiply 进世界层，最后 drawImage 叠回主画布。
  - 逃生门 `?worldlayer=0` 回旧全屏乘光；fullbright(F2) 仍叠回世界层。
  - **坑**：endWorldLayer 不能清 worldLayerActive——compositeLight 在其后读该旗选
    路径（曾清了→恒走旧路径→修完还是黑，探针 worldLayerAlpha=0 + mainMoonPx 低值抓回）。
- **验证**：夜月位 13.8→165.4/137.8（亮斑区含月面纹理明暗）；夜空角 1.4→15.9
  （暗蓝非纯黑）；昼夜地表亮度比 12× ≈ 255/21 月光地板比；FPS 121.5 vs 关层 120.5
  零回归。渲染域 11 文件 280 测 + moon/lighting 域全绿。
- **附带语义改进**：实体精灵透明像素处的天空现在不乘光（原版正确）；日光/事件
  月亮/近云全走天空层不受光照。

**Why**: 单画布"全屏乘光"是光照架构的隐蔽近似——白天乘白无感，任何 <255 的
环境（夜/洞穴上空）都会把天空层一起吞掉。用户报告"月亮不亮"时先查"哪一层在
光照通路里"。

**How to apply**: 排查天空亮度类问题用三段探针法：①逐层包 draw（sky/biomeBg/
cloudsNear）每层画完同步采样目标像素定位"哪层后消失"；②Proxy 盯贴图数组索引
访问验证分支真伪；③ImageBitmap 无 .src——drawImage 拦截器要按 width/height 或
WeakMap id 匹配，按 src 匹配全漏（本次 ImageBitmap 盲区曾误判"月亮没画"）。
相关 [[cloud-parity-fill-attempts]] [[moonlight-audit]] [[vanilla-lighting-port]]。
