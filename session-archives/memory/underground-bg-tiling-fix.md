---
name: underground-bg-tiling-fix
description: 地下带状背景平铺几何 1:1——160宽贴图实际周期128(两侧16px padding)/垂直相位锁带顶/caveParallax 0.88 视差;整宽平铺=蘑菇区远景错位根因
metadata: 
  node_type: memory
  type: project
  originSessionId: 9adce254-f6c0-44ed-947b-3a226dd16828
  modified: 2026-08-17T10:10:26.626Z
---

地下带状背景（BiomeBackground.drawUnderground，2026-08-17 重写为原版几何 1:1）：

**根因（"蘑菇区远景平铺错位" debug-report）**：原版地下背景贴图（Background_62-65 等 160×96/160×16）
**有效平铺周期是 128px，不是贴图宽 160**——两侧各 16px 是 wrap padding（像素级验证：
63/65 在列 16..144 逐字节完美循环，seamAvg=0）。整张 160 宽平铺会每 160px 出一条图案断缝。
原版采样源 X = `16*k + num4 + 16`（Main.cs DrawBackground :52536/:52836 族），源窗 [16+diff, 144+diff)。

**原版几何三件套**（对照 Main.cs :52217-53517）：
1. 水平周期 P=Width-32（岩石/岩浆带硬编码 128）；`bgStartX = -IEEERemainder(P+screenX*caveParallax, P) - P/2`（caveParallax=0.88 默认，:1172）
2. `diff = round(-IEEERemainder(bgStartX+screenX,16))`（-8→8）——采样窗对齐世界 16px 网格，src/dst 同移，防视差下纹理游动
3. 深层垂直相位：`bgStartY = IEEERemainder(bgTopY,96)-96`（锁到带顶=世界锁定；屏幕顶锚定会随相机漂移）；步进 96=backgroundHeight[2]（=Texture.Height()，:58439）

**Why:** 曾以为地下背景无水平视差、可整张贴图平铺——实际上原版全部按 16px 切片绘制（含逐格光照/贴墙裁剪），切片几何合并后就是上述三件套。
**How to apply:** 动 BiomeBackground 地下层时先抄 :52523(Rock)/:52826(Dirt)/:52276(Magma)/:53137(slot0)/:53155(slot2)/:52765(slot4)的公式；slot4 画在**岩石带底行边界**（非 magmaTop-200）；slot6 在岩浆带底行边界；IEEERemainder 必须 round-half-even（JS Math.round 是 half-up，需自写）。逐 16px 切片光照未实装（整行近似，已登记）。验证探针 `scripts/_ugbgprobe.mjs`（隔离渲染+128 周期逐字节断言）、单测 `tests/underground-bg-tiling.test.ts`。相关 [[hell-background-fix]]。

**踩坑**：Node 环境跑 drawUnderground 深层相机会经 drawHellLayers→loadBitmapOnly→`new Image()` 崩——测试需把 hellImgs 0..13 置 null（未加载态跳过）；探针/测试相机必须在岩石带内且 magma 之上，否则 magma 截止把岩石带裁空（camY=500*16 无绘制是原版行为）。
