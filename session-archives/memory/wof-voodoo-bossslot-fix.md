---
name: wof-voodoo-bossslot-fix
description: 巫毒娃娃召肉山漏设Game.boss槽=击杀链全跳过(无砖盒/无StartHardmode/无公告)根因;spawnWOF补设槽;掉落管线本就正确(探针内部id≠vanilla id误读教训);CanKillTile树下保护=原版真规则
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-18T03:21:32.657Z
---

肉山击杀无小屋/无肉后变化修复（2026-08-18，用户报"杀死肉山没出现小屋子、没触发肉后变化"）。

**根因**：巫毒娃娃入岩浆路线（ItemDrop.checkLavaDeath :452 → spawnWOF）**没设 Game.boss 槽**——击杀链全挂在 `bossBlock: if (this.boss)` 上（Game.ts :4220 `vanillaId===113` → createBrickBoxForWallOfFlesh → startHardmode → misc15 公告），槽空整段跳过。调试召唤路径（spawnBoss :18660）有设槽所以只有玩家真玩娃娃路线踩中。修：spawnWOF 尾补 `(game as {boss}).boss = wof`（bossAI_wof.ts）。

**验证**（探针 _wofdoll/_woftrace2，真娃娃入岩浆→hurt 击杀）：bossSlot ✓/hardMode ✓/downed_113 ✓/砖盒 32 块 ✓/**全套战利品正确**（spawnDrop 插桩溯源：vi_367 Pwnhammer+vi_2105 面具+徽章 oneOf+裂空刃+金币/药水/8 心——规则树本就 1:1）。

**教训**：①探针 dump `d.itemId` 是**内部 id**，拿去查 `idNames.generated（vanilla id 空间）`必误读（内部 1366=心被读成毁灭者奖杯×8="垃圾掉落"假象）；断言物品用 spawnDrop 的 **key 参数**（vi_ 前缀字符串）或经 VANILLA_ITEM_KEY_BY_ID 反查。②window.__swItems 在新页面早期可能未就绪（undefined），探针用它前须等 inventory 初始化。③正则 `/^vi_367_/` 会误中 vi_3670 族——精确键匹配。

**顺带澄清**：树下方块"无法用镐破坏"=原版 CanKillTile :62276-62315 真规则（树干/棕榈/箱柜需支撑件正下方不可挖），我们 1:1（Game.tileAboveProtected），勿当 bug。

关联 [[wof-house-and-ores-clarify]] [[boss-summon-announce]]。
