---
name: explosion-sfx-port
description: 炸弹无音效根因=按需加载首播 fetch 中+合成 switch 无 explosion 分支;爆炸族伤害盒/视觉 1:1(Kill :74882-74916)
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T04:35:50.063Z
---

2026-08-12 用户报"炸弹没有音效"。探针实证链路通(explodeCalls=2/Item_14.wav 存在/decode OK/preload 命中)。

**根因(双保险都缺)**:
1. Sfx 合成兜底 switch **无 `case 'explosion'`** → 按需加载首播(wav 还在 fetch,pending 返回 null)完全静音
2. **无预热**:afterWorldLoad preloadNames 清单没 explosion → 每次进世界第一爆必静音;第二爆起才有真声(用户单颗试=恒静音体感)

修复:Sfx.ts 补 explosion 合成分支(白噪 buffer+低通 900→120+低频 thump);Game.afterWorldLoad 预热清单加 'explosion'。
**同坑复查(2026-08-12 召唤音)**:summon(Item_44)/whipCrack(Item_152)已由并行会话接线,但漏预热+漏合成兜底 → 补齐;敌弹发射音(Item_8/11/12/17/20/28/154,playSfxFiles 直放)也入 preloadFiles。**新音效接入三件套=接线+预热+合成兜底,缺一首播即静音**。

**爆炸族 1:1 对齐(Projectile.Kill :74882-74916 炸弹族 / :74943-74951 炸药棍)**:
- **实体伤害盒与地形半径无关**!原版 Kill 里 Resize 盒+Damage() 盒交判定:炸弹/手雷族(28/30/37/75/102/164/397/516/517/519/773)Resize(**22,22**)=半宽 11px;炸药棍 29/:470/637 = **200×200**=半宽 100;102/75 额外 128×128 一轮。我们曾用 `R*TILE+16` 距离圆(炸弹 80px = 原版 7 倍)→ explodeAt 加 hurtBox 参(盒交:中心距 < hurtBox+实体半宽),手雷回调传 (29?100:11);器件爆(放置炸药/接线)按 R*TILE 兜底
- 视觉:原版 = 烟 31×20(×1.4 速慢散)+火 6×10 对(noGravity ×5/×3)+gore 61-63 四向 4 块;我们曾 26 橙粒一把抓 → 已分层重写(spawnParticles 加 size 选项)
- 已对齐无需动:地形半径表(EXPLODE_RADIUS=cs:75262)✓、免疫表 CanExploteTile ✓、墙炸 ShouldWallExplode ✓、链式引爆 ✓、引信(150/135/180)与伤害(100/250/60)✓
- 遗留(周边系统未实装):爆炸震屏(CameraModifiers)、爆炸光闪(Lighting 瞬时)
