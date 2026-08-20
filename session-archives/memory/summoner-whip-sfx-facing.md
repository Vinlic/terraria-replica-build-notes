---
name: summoner-whip-sfx-facing
description: 召唤师收尾批：随从朝向翻转(AI_062 :62975)+鞭响 Item_152/召唤杖声 Item_44；SfxName 联合续行不能踩行尾分号
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-12T02:54:12.951Z
---

召唤师职业收尾批（2026-08-12），三处：

1. **随从朝向翻转**（MinionProj）：原版 `AI_062` Projectile.cs:62975 `velocity.X>0 → spriteDirection=-1`。本作近似 `dirX = tgt ? sign(tgt.cx-cx) : sign(vx)`，draw 里 `facing<0 → ctx.scale(-1,1)`（随从+哨兵通用，哨兵另有 AI_130 :65386 `direction=Sign(指向)`）。探针双向验证：目标左 -1 → 右 +1。
2. **鞭 UseSound = Item_152**（`DefaultToWhip`，Item.cs:47448）→ SfxName `'whipCrack'`，WAV_MAP `['Item_152']`，Game.ts `case 'whip'` 播。**召唤杖通用 UseSound = Item_44** → `'summon'`。素材 `public/sounds/Item_152.wav`/`Item_44.wav`。
3. **Sfx.ts 联合续行坑**：`SfxName` union 里上一条目 `'portalBlue';` 行尾有分号终止了 union，后续 `| 'whipCrack'` 行 esbuild 直接炸（tsc 却能过）——续写 union 必须先摘掉前条行尾分号。

DD2 哨兵塔（AI_130/134/137/138）开火音效原版素材未提取（SoundID DD2 系无 wav），暂无声。探针脚本 `game/whip3-sfx.mjs`（stub `g.sfx.playWav` 录音 + 给手物品 `VANILLA_ITEM_KEY_BY_ID[vid]`→`ITEM_BY_KEY`）。

相关：[[explosion-sfx-port]]（首播静音=按需加载兜底）、[[vanilla-npc-port]]
