---
name: vanilla-bgm-background-port
description: 原版 BGM+世界背景图移植：xwb 提取(cue→wave 映射大坑)/选曲链/SceneMetrics/BiomeBackground
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-11T05:00:54.039Z
---

2026-08-10 原版 BGM + 世界背景图 1:1 移植（用户令）。

- **★ 音乐提取大坑（用户报"丛林/腐化 BGM 反了"）**：macOS 版是 XACT 三件套（`Wave Bank.xwb` 495MB ADPCM / `Sound Bank.xsb` / `TerrariaMusic.xgs`，在 Terraria.app/Contents/Resources/Content/）。**波形条目号 ≠ MusicID**——游戏按 cue 名 `Music_N`（Main.cs:10818 `LoadCue(i,"Music_"+i)`）查 xsb，**cue→wave 映射 = 名字表 @0xDCA 的 cue 顺序 与 声音表 @0xCA stride 19（签名 02 01 00 5a，wave index @+9）按位置配对**（首三条旋转 [2,1,0]，即 Music_1→wave2/2→1/3→0）。曾按"条目号=MusicID"假设提取致全表错位（Music_7 装了 Hallow 曲）。`tools/xwb-extract.mjs` 已内置 xsb 解析（vgmstream 解码 + ffmpeg libmp3lame 128k；homebrew ffmpeg 无 libvorbis）。时长锚点：OverworldDay 58s/TitleClassic 65s/Underworld 1:50.9/TitleIntro 3:32。
- **BGM 链**：`src/data/Music.ts`（MusicID 全表+`pickMusic` 按 Main.cs:12470-12913 优先级链：boss→城镇≥3NPC→地狱→太空(num5)→神庙墙→地牢→蘑菇→腐化 8/10→猩红 16/33→陨石→墓地→地下沙漠→沙漠→丛林 7/55/54→雪 14/20→地下 4/31 随机粘性→神圣 9/11→海洋 22/43→森林 1/18/3）；`Audio.ts` 重写为 BGM 池（`audios/music/Music_<id>.mp3` 懒建 audio）+ musicFade ±0.005/帧 rAF 交叉淡化（LegacyAudioSystem.cs:281/309）；title=Music_50；Maples main/title.mp3 已弃。`__swAudio` 调试桥。
- **环境判定 `src/world/SceneMetrics.ts`**：SceneMetrics.cs 精简核——玩家中心 169×124 tile 计数→阈值聚合（含神圣/邪恶/猩红互减+向日葵-10）→ Zone 标志+深度+oceanDepths(y≤(surface+rock)/2+40 且 x<beachDistance=w*0.06)。Game 每 15 tick 刷新存 `game.scene`。**World.lavaLine 新增**（GenState 落回+WldImport+SaveFile 兜底 h-200）。
- **背景 `src/render/BiomeBackground.ts`**：地表 bgStyle（GetPreferredBGStyleForPlayer :63658）+bgAlpha ±0.05/帧+群系 3 层视差（scale 1.25/1.31/1.34、parallax 0.4/0.43/0.49、topY=num3*A+B，num3=-(camTopY-300)/(surface*16)）+昼夜 tint；地下 style（PickUndergroundBackgroundStyle :53454）→7 槽贴图表（:53221 全量）→泥土/岩石/岩浆分层+地狱黑幕+ugBackTransition 0.25/帧双绘。贴图 344 张全量落盘（vanilla-atlas MISC），运行时**懒加载不进 VANILLA_MISC**。贴图集 style 由 world.seed 派生（seedPick）——**终局必须 `>>> 0`**（见 [[js-bitwise-int32-traps]]，负索引曾崩 drawSurface）。兜底+warn-once(JSON 现场)惯例。
- Renderer.render 插入点：sky.draw 后、世界变换前；`renderer.scene` 由 Game.render 每帧注入。
- 遗留：M6 完整回归（_biomeaudio.mjs 群系断言——曾因 FastRandom 死循环(另会话已修)+seedPick 崩溃阻塞）；事件曲/天气/Otherworld 不做。

关联 [[js-bitwise-int32-traps]] [[reference-vanilla-source-of-truth]] [[vanilla-ui-port]]

## 地下背景岩石带槽位语义修复（2026-08-10，用户标注 Starter_World (3488-3491,735-740) 报"深层背景下半错误贴图"）
- **与导入无关**：根因是槽位绘制语义读错原版。标注框恰好横跨泥土/岩石分界（rockTop 屏幕坐标 432 落框内）——上半泥土带(slot1)对、下半全是 slot2 平铺=错。
- **原版真实语义**（Main.cs :52532 GetRockTransitionPoint + :52669/:53143）：岩石带顶 = worldSurface*16 + ceil((rockLevel-worldSurface)*16 / slot3纹理高)*slot3纹理高 + 32（泥土带按 slot3 纹理高对齐收口）；**slot2 只是带顶上一条 16px 过渡条**（Rectangle 只取纹理第 0 行、画一次）；**slot3 才是岩石带主体**，按自身纹理高平铺至 magmaLayer*16+600。旧实现误把 slot2 当"岩石带上 1/3"平铺——深层时岩浆层远在屏外，slot3 永远轮不到，整屏是过渡条纹理反复平铺。
- 槽位→贴图表（ugSlots）本身与 :53221 逐项核对一致（含 style4=[70,71,68,72]）；该表无需动。
- 顺带：导入 wld 的 header seed 导出为 0（wld seed 字符串解析另案）；caveBackStyle 四段是我们 seedPick 近似（原版 worldgen 期随机），形态级可接受。
- 验证：tsc + 180/180。

## BGM 不随场景切换修复（2026-08-11，用户报"进不同场景不切 BGM"）
三层掩蔽 bug 叠加，均以 Main.cs:12155-12913 为准修正：
1. **天气链全局前置**（主因）：44 风日/19 雨/52 风暴被放在 pickMusic 最前 return——原版天气曲只嵌特定槽位（L12886 风日只覆盖森林白天曲与神圣地表 L12811；雨只在森林白天/夜晚/神圣地表；风暴只在丛林表层/神圣地表/非特殊地表尾槽 L12816）。重写 pickMusic 按原版主链逐槽排布。
2. **TownNPCCount 语义**：原版是距离盒计数（SceneMetrics.cs:755 `CenteredRectangle(Center, AssumedConstantScreenSize×2)`=±1920×±1080px 内 townNPC），我们传全图存活数 → ≥3 个 NPC 后 46/47 盖住一切。Game.ts 传参改距离盒。
3. **风日门窗口**：updateMusicGates 白天中段写 (0.2,0.8)，原版 time∈(10800,43200) 对应 timeOfDay (0.35,0.65)（白天 0.25-0.75 ↔ time 0-54000，Weather.ts:230 的换算表达式是对的）。修正常数。
- 另补：MusicInput 加 bloodMoon（夜晚森林/海洋/风暴槽 2 号曲）；晨雨 59 = vanillaTime<10800。
- 验证：tests/music-pick.test.ts 8 例 + probe-music.mjs（地表1→地下4→地表1）。城镇距离盒、天气槽位是"曲子不换"的两大经典根因——排查先查这两处。

## 瀑布贴图取半错误（2026-08-12 晚2，用户标注 太阳花避难所 (2178,424-430) 报"瀑布贴图错误"）
- **WaterfallRenderer 帧槽取样取错半格**：Waterfall_N.png(512×40) 每 32px 帧槽——**主水流 16px 全宽柱在右半 [16,32)**（顶部 0-23 行全宽 / 24-39 行 10px 是唇缘入池变体），左半只有 2px 细边。原版主体路径采样 `Rectangle(16+num21, 0, 16, height)`（WaterfallManager.cs L888/922/930），带水平方向才用左半(num21,0,16) 的 2px 边条（L767-776/829/842）。我们取 (32f, 0, 16) 画的全是透明残边——瀑布近乎不可见/只剩细丝。修复=frameX+16。
- **标注文件分析套路**：map-*.json 是 saveGameCompat 全量存档（tiles/liquid 均为 base64 RLE：varint(run-1)+varint(value)，tiles 多两帧参数）——自解码即可离线勘验液体分布，无需进游戏。
- 探针：出生点造半砖唇缘+侧格水 → 唇缘下空气柱 16×64 采样 1024 px 全不透明（修复前是残边）✓。hive.test.ts RNG 重复导入错误=并行会话在途。
