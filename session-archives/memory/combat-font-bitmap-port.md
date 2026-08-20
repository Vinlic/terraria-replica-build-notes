---
name: combat-font-bitmap-port
description: 飘字位图字体全对齐:ReLogic DynamicSpriteFont 私有布局逆向(本地ReLogic.dll反编译)+LZX+xnb库管线;数字页裁剪158页全量3.6MB→2KB;5层绘制影=本色调暗×0.3非黑
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-13T15:39:39.792Z
---

2026-08-13 飘字位图字体完全对齐(monospace→原版 Combat_Text/Combat_Crit):

**格式逆向三钥匙**(从此不再是黑盒):
1. `Terarria1456/Terraria.Libraries.ReLogic.ReLogic.dll` 就在本地反编译树——
   `ilspycmd -t ReLogic.Graphics.DynamicSpriteFontReader` 直接拿 Reader 源:
   **spacing f32 → lineSpacing i32 → default char(1B!非u16) → pages i32
   → 每页{texture(DXT3) + glyphs/padding List<Rectangle> + characters List<char>
   + kerning List<Vector3>}**。此前卡壳=root 字段序假设错(标准 SpriteFont 无此序)
2. LZX 压缩(flags 0x80,非 LZ4 0x40)由 xnb 库 Presser 解;嵌套读走库 ReaderResolver
3. 坑:**库 buffer 头 14B 是原压缩头残留**,解压 payload 从 14 起

**提取器 `tools/extract-combat-font.mjs`**(永久资产):两字体各 158 页/39321 字形
全 Unicode。**数字 0-9 全在 p22 一页**——裁剪后 2KB JSON+两张 64×64 png(1154B)
进 `src/data/combat-font.json` + `public/sprites/vanilla/*_p22.png`;全量产物在
terraria-assets/Fonts/(以后做原版文本 UI 按页取用)。

**渲染**(`render/CombatTextFont.ts` + Renderer 步骤 8):
- XNA SpriteFont.Draw 度量:x+=kerning.X → draw(glyph rect) → x+=kerning.Y+Z+spacing
  （spacing 每字符后都加含尾字符;measure = Σ 全部）
- **5 层绘制**(Main.cs:61805-61841):0-3=±targetScale 四向影(**本色调暗×0.3,
  非黑**;alpha 两层都=num15×alpha,影层 alpha **不**再乘 0.3),4=本体;锚=文字盒
  中心(origin=Measure/2);num15=scale/targetScale 生长系数乘进全部颜色/alpha
- ★**染色:tintedGlyph 离屏缓存**(source-atop 把色铺到字形 alpha 上;按 字体|字形|
  颜色 缓存,512 上限)——**drawImage 不受 fillStyle 影响**,首版漏染=飘字全白
  (用户抓回);XNA DrawString 的 color 乘纹理语义必须离屏实现
- dot scale 归位原版(+0.1/t 无封顶;旧 0.5/t+0.8 封顶是 monospace 时代自造)
- label 飘字(物品名)仍 sans-serif(非原版 CombatText 链,后续按需)
- 字体懒加载窗口回退 monospace

**探针断言两次假通过教训**(全白 bug 漏网的根因):
①主色调断言采样区含玩家 sprite → 假绿;②天空背景不透明像素淹没 bbox → 主色调
恒背景色。最终版断言 = **红系字形像素计数**(redPx>10 且 whitePx<redPx)——
背景无红、漏染时 redPx=0,两假阳性通道全封死。14 断言全绿。

**探针坑**:Resource Timing 缓冲 250 条被启动资源塞满→后继请求不记录=假阴性;
断言资源加载须用 puppeteer CDP `page.on('request')`。位图 vs monospace 的决定性
像素断言:近不透明(alpha>200)占比≈1.00(位图二值 alpha,抗锯齿字体仅 ~0.6)。

探针 `_combat-font-probe.mjs` 5 断言(含 solid=1.00);tests/combat-font.test.ts 5 条。

**武器对齐终审(2026-08-13 深夜,用户"枪/星怒不连发"复核)**:非 bug——
164 手枪/96 火枪原版**显式 autoReuse=false**(:3351/:2480),星怒 65 缺省 false
且 useTime40>animation20(慢节奏单发),★常见误判:早期枪械/星怒原版就要逐击,
能连发的代表=迷你鲨 98/星璇机枪 3475/银阔剑 7/村正 27。数据层审计(2612 件,
melee302/ranged171/magic72/summon42/thrown76;4 个"melee 无 damage"异常均为
原版 damage 缺省 -1 的放置物/特殊件,null≡-1 语义等价)。autoReuse 链三处门
(近战 canChain/通用 :5643/投掷)+点击沿(mouseDown 边沿,_prevMouseDown 须在
updateUse 后快照)。探针两坑:window.__swItems 是物品表暴露(非 itemByKey);
挥击计数须数 swing 引用替换(useTime<animation 截断式连挥 swing 不归空)。
10 套件 83 绿收尾。
**坠星掉落物尺寸修复(用户"星星大小不一致"抓回)**:原版 Item_75=22×208 竖条
8 帧动画(DrawAnimationVertical(5,8,PingPong),Main.cs:3688-3691)→ 单帧 22×26,
掉落物按贴图原尺寸画(Main.DrawItem texture.Frame 原大)——星星比 16px 方块还大。
旧 drawDrop 统一压 14px 宽(14×16.5)视觉偏小;已改按切片后 sw×sh 原尺寸。注:
atlasIcon 本就切帧(UI/掉落物共用),仅 drawDrop 缺尺寸门。探针白盒断言
sw=22/sh=26(_star-drop-size-probe.mjs;像素采样会被玩家/地形污染,勿走)。
相关 [[debug-report-warn-ring]]
