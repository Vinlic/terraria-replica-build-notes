---
name: chop-hit-sound-port
description: 砍树/挖掘每击击打音=原版每击KillTile(fail:true)都播KillTile_PlaySounds;工具类型门须查tileAxe原版表非本地d.axe标志
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-17T08:11:41.599Z
---

# 砍树击打音效对齐(2026-08-17)

用户问"原版砍树会有音效吗"——**有,每斧击中(无论砍没砍断)都是挖掘声**:
- 原版链:Player.cs:45148 每击 `WorldGen.KillTile(x, y, fail: true)`(:45160 未满 100
  伤害 else 支)→ KillTile_PlaySounds(WorldGen.cs:66483-66631)→ 树干 5 无特殊分支
  落 default → **PlaySound(0)=Dig**(和挖土同款"咚");砍断击 fail=false 同样一次。
  **没有专属"树倒"音效**(tail switch 13/54/326… 是模特/假人族)。
- 挥动工具另有 UseSound(斧=Item_1,ApplyItemAnimation :50935 每挥必播,本仓已接)。
- 同一语义覆盖镐:每击 KillTile(fail) → 石→sound21(Tink)/土树→sound0(Dig)/草→6。

## 本仓缺口与修复

- 曾只在**破坏完成**播(killTileBreakSound 只在 breakTile:9051 调)→ 砍树积累段
  (13 击)全程静默,fellTree 砍断也无声。
- 修:tryMine 击打点(addDamage 处)每击播 killTileBreakSound 四档近似;
  **砍断击恰好一次音**(fellTree 内不再补,防双播)。
- **toolCanBreak 拆分**:类型门 toolMatchesTile(镐=`d.pick>=0 && !TILE_AXE_SHEETS
  .has(sheet)`、斧=`TILE_AXE_SHEETS.has(sheet)`——权威是 Main.cs:7157-7172 原版
  tileAxe 表,本地 d.axe 标志混有平台/草等非 tileAxe 件曾误拒镐挖平台)+ d.pick
  镐力门槛后置到 dmg 计算(**镐力不足每击仍播声+尘不积累**=原版 num2=0 也走
  KillTile(fail:true) 播声;破坏进度 AddDamage(0) 不涨)。
- 平台 19 非 tileAxe/非 tileNoFail:镐可拆(无门槛累计)/斧不可拆——原版行为。

## 教训

- "每击 KillTile(fail:true)"是原版音效+尘(3 尘)的通用节拍器,不破坏也走;
  只对齐"破坏完成"会漏整个积累段的反馈。
- 本地 def 标志(d.axe)≠原版表(tileAxe):门语义以原版 sheet 表为准。
- Game.ts 被并行会话动过时 Edit 前必须重读(memory 教训再现,本次 edit 前有
  file-modified 提示,重 grep 后落地无冲突)。

关联:[[palm-chop-tileaxe-parity]](tileAxe 表全对齐)。
