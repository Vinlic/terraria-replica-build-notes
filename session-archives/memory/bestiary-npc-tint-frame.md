---
name: bestiary-npc-tint-frame
description: "图鉴NPC头像三修:frames查母体sheetId(负id键缺→整条两帧画)+netid表color染色(绿史莱姆-3=(0,220,40,100))+原生尺寸只缩不放(原版DrawNPCDirect不放大填框,僵尸剪影34×46>绿史莱姆28×20);离屏两步混合防挖MapBG"
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-14T09:07:04.152Z
---

图鉴 NPC 头像染色/帧/尺寸三修（2026-08-14，用户："图鉴没对需要染色的怪物滤镜染色？绿史莱姆贴图灰的且显示完整两帧，僵尸正确"+"史莱姆这么大吗比僵尸大"）。

**三根因**（BestiaryPanel.drawPortrait）：
1. **frames 查负 id 键**：绿史莱姆 npcId=-3，`VANILLA_NPCS['-3']` 无条目（负 netID 变体共用母体贴图）→ frames 默认 1 → 整张两帧条当一帧画。修：查**母体 sheetId**（`npcId>=-10?1:14` 解析结果）。
2. **color 染色缺失**：负 id 变体色在 `vanilla-npcnetid.json`（NETID_OV：-3 绿史莱姆 (0,220,40,100)/-4 粉红 (250,30,90,90)/-5,-6 黑 (0,0,0,50)+alpha 120/scale 0.6~1.2），正 id 用 VANILLA_NPCS 自身 color。渲染=Renderer 同款两步混合（XNA AlphaBlend 预乘：destination-out 按 colorA 削 base + lighter 加逐像素乘色帧）——**在离屏 canvas 合成完再贴回**，destination-out 才不会挖掉主画布 MapBG 底图。缓存 bstTintCache 有界 800。
3. **放大填框假象**：曾 `s=min(size/(w·scale),size/(h·scale))` 等比**放大**填满 64px 画布→方形史莱姆被拉宽比僵尸显大。原版语义（UnlockableNPCEntryIcon :52-109 → DrawNPCDirect）：**原生帧尺寸×scale 直接画、无适配框**（巨怪靠 NPCBestiaryDrawOffset 逐 NPC 调——Leinfors 段 654 条 60 处 Scale；僵尸 3 号条目仅 Velocity，史莱姆族无条目走 netid scale）。修：`s=min(1,…)` 只缩不放。修后：僵尸剪影 34×46 > 绿史莱姆 28×20（史莱姆本体矮胖帧内剪影仅 ~20px）=原版观感。

**探针方法论**：getImageData 统计 hue 类占比（绿>rgb+25）+剪影 bbox；图鉴免门 `import('/src/data/Bestiary.ts').bestiaryGating.unlockAll=true`（vite dev 动态 import）；图鉴按钮监听 **mousedown 非 click**；背包手动开=槽最多的 .sw-panel display:block。

**紧急插曲**：并行会话在 DungeonPass.ts 加的 4 处 `process.env.SW_DGPA_TRACE` 炸 worker（浏览器无 process，页面全挂 player NOT ready）——守卫 `(typeof process !== 'undefined' && …)` 即修。并行调试注入踩 browser 兼容是共性坑。

遗留：~~NPCBestiaryDrawOffset 未移植~~ **已全量落地（2026-08-14 二批）**：`tools/extract-npcbestiaryoffset.mjs` 提取 NPCID.cs 三段合并 665 条（Scale/PortraitScale 59、Hide 216、CustomTexture 25）→ `src/data/vanilla-npcbestiaryoffset.json`；drawPortrait 接入五项：scale 链（DrawOffset.Scale 覆盖 netid scale→portrait 档 PortraitScale 再覆盖）、Position 偏移（原版 72px iconbox 口径×画布比例，portrait X/Y Override 分量覆盖，钳防移出）、Frame 静态帧（bstTintedFrame 帧参同步）、Rotation、CustomTexture 替换贴图（单图 frames=1、不染色）。Hide=GetExclusions 不建条目——我们 BESTIARY_HIDE_IDS 早有 ✓。探针：Duke(491 scale0.8+custom) 34×45、KS 60×21、克眼 41×38 全框内。

**l10n 连带坑（同日）**：并行会话 l10n 化批不断加新键 → l10n-audit 闸门挡死全仓 vitest（Startup Error 空输出）——替补 28+1 键（Craft/Reforge/Tabs/Map/Toast/Party/JourneyPowers 等，zh 大半已在=en-US 缺）+ build-l10n 重建；**重建暴露 l10n-data.test.ts 过时断言**（UI.Inventory/UI.Dropped 键已更名 InvLabel 等、src 零消费，旧产物残留假绿）→ 断言改现存键。教训：build-l10n 再生前先跑 l10n-data 测试对照。
