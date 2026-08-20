---
name: held-item-nowet-parity
description: 手持物水下渲染noWet逐件化(芦苇管186水下可显根因)+NO_WET_ITEMS 70件提取法+珊瑚火把4384水火把行为+探针drawImage精确矩形匹配法(像素差分/近身过滤双双失败)
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-17T06:08:09.120Z
---

# 手持物水下渲染 noWet 逐件化（2026-08-17，用户报"芦苇呼吸管在水中无法渲染"触发）

**根因**：`Renderer.drawPlayer` 静持段被全局 `!p.inWater` 门拦死——火把的
noWet 熄灭语义被扩到所有手持物，芦苇管 186（holdStyle 2、无 noWet）在水下
（它的主场景）反而隐身。原版门是**逐件** `(!wet || !noWet)`
（Player.cs:36026/:36030）。

**Why（数据面）**：
- NO_WET_ITEMS 70 件 = Item.cs 逐 case 字面 `noWet = true`（63）∪
  DefaultToTorch **无** allowWaterPlacement 族（7：4383,4385-4388,5293,5353；
  :48086 `noWet = !allowWater`）。提取脚本法：扫 `case (\d+):` 后到下个 case
  前的 `noWet = true` / `DefaultToTorch(...)`。
- **珊瑚火把 = item 4384**（不是 523——523 是诅咒火把且手写块无 noWet＝
  vanilla 自身不一致）；4384 DefaultToTorch(17, allowWaterPlacement:true) →
  noWet=false → 水下照常显示+发光（水火把）。探针正断言此行为。
- FLAME_ITEMS ⊄ NO_WET（12/16/23/33/49 等武器火苗无 noWet）——火把族子集
  重叠即可：静持分支里 noWet 先拦，火苗叠画自然不进。

**How to apply（探针方法论——三层失败后唯一可靠法）**：
水下渲染探针**像素差分不可用**（水波/光照/气泡帧抖淹没信号）；
**近身坐标过滤也不可用**（ctx.translate 世界变换下 drawImage 的 dx 是局部
原点≈0，屏坐标过滤器全滤掉）。可靠法 = **drawImage 精确矩形匹配**：包
CanvasRenderingContext2D.prototype.drawImage 抓 9 参调用的 (sx,sy,sw,sh)，
与 `renderer.atlasIcon(held.id)` 期望矩形全等（icon 兜底路径抓 5 参
dw×dh=宽高×0.6）。前置：①物品 key 用 vanilla.json 权威 PascalKey
（vi_8_Torch 非 vi_8_torch——mkStack 错键返回 null 静默）；②`cb.onInventoryChanged()`
触发 itemIcons 懒建；③定帧须 `running=false`+手动 fixedUpdate+render+复原；
④水下场景用天然海洋水列（自挖坑 setLiquid 会被液体沉降排干——
setLiquid(x,y,**amount,type**) 参数序，amount>100 才判湿）；⑤出水对照在
cap 的 500ms 真实 rAF 期间也要钉位（setInterval pin y0，重力会回落再入水）。

探针 `scripts/_reedprobe.mjs` 五断言全绿（复跑两次稳定）。

**review 补（同日二次 review）**：①手持光源门（Game EmitHeldItemLight）也是
全局 !inWater——**WaterTorches {523 诅咒,1333 神圣,4384 珊瑚}**（ItemID.cs:1194，
`:48997 (Torches && !wet) || WaterTorches`）水下应发光；**并行会话同分钟落了
同修复**（heldRGB 前置段 WATER_TORCH_ITEMS），我方删重复声明让位、门上留指路
注释——撞车调和模式：先 grep 最新盘面再动手，双修以单源为准。②三处注释纠错：
"523/1333 无 noWet 是 vanilla 不一致"系误判——恰是 WaterTorches 有意设计；
FLAME_ITEMS ⊄ NO_WET_ITEMS（12/16/23/33/49 武器火苗等不在集，但 holdStyle=0
走挥舞路径不进静持分支，523/1333/4384 水炬有意水下带火苗）；渲染段头注同步
逐件化。**教训：全局水门是家族模式——渲染/光源两侧都要查 noWet 逐件化。**

关联 [[breath-meter-port]]（芦苇管换气功能侧）。
