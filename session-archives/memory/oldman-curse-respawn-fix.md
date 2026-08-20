---
name: oldman-curse-respawn-fix
description: 老人诅咒链杀王后复活根因=downed旗标双键漏改五门；skeletronDowned()助手统一；老人AI自灭语义(NPC.cs:53743-53760)
metadata: 
  node_type: memory
  type: project
  originSessionId: 573d63f5-287b-42b0-99c2-a96bc6fc7c8a
  modified: 2026-08-17T06:39:21.196Z
---

# 老人诅咒链修复（2026-08-17 用户报障）

用户报"老人变成 Boss 后没有消失"——真根因不在诅咒瞬间（`npc.dead=true`+EntityManager
compact 清扫那条路是对的），而在**杀掉骷髅王之后**：击杀链写 `downed_${vanillaId}`
（→downed_35），五处消费门只查 `downedSkeletron`（恒 undefined）→ boss 结束块判定
"未击败" → 同帧在门口重建老人；读档两处同病复活、地牢砖挖掘门同病误锁。

**Why**: downed 旗标两套键名并存（新链 `downed_<id>` / 旧档语义驼峰），:3971/:12673
等早期消费点已是双键，五处后补的漏改——单键门在写读异键下静默恒假。

**How to apply**:
- 新消费点一律双键 `flags.downedSkeletron || flags['downed_35']` 或走
  `Game.skeletronDowned()` 助手（2026-08-17 起五门已统一）。
- 原版老人语义：SpawnSkeletron(:81243) 置 ai[3]=1 → 老人 AI 下帧 life=-1 自灭
  （:53743-53756，37/54 伴咆哮 SoundID 15）；**老人 AI 每帧查 downedBoss3 → 自灭**
  （:53754-53760）——王已败后老人绝不在场（含裁缝巫毒娃娃 eq.killClothier 途径）。
- 同族坑：boss 击杀记账在 Game.ts boss 结束块（`downed_${id}`），双子家族共写
  downed_125（:4050 twinsPart 特判）——跨 id 记账先查家族键。
- 探针 _oldman-curse-probe.mjs（真实 hurt 击杀链 11 断言）可复用为 Boss 记账
  验证模板。关联 [[overall-review-2026-08-13]]。
