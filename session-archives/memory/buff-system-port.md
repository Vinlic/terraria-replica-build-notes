---
name: buff-system-port
description: Buff 系统原版化要点——AddBuff max 合并/Honey(48) 授予链/1456 数值修正（铁皮8、恢复2HP/s、荆棘全额反伤）/蜂蜜不淹死
metadata: 
  node_type: memory
  type: project
  originSessionId: 0650e0c7-c14a-4b14-b89b-73780115946c
  modified: 2026-08-10T06:22:22.264Z
---

2026-08-10 Buff 系统按 1.4.5.6 语义重构（src/stats/Buffs.ts），蜂蜜浸入加血 buff 接通：

- **AddBuff 合并规则**（Player.cs:5138 `TryUpdatingExistingBuffTime`）：同类 buff 时间取 **max 不缩短**。BuffState.apply 即此语义——浸入类 buff（蜂蜜）可每帧无脑 apply(30s) 续期，离蜜后从 30s 自然倒计时。原版授予链三处：浸蜜 AddBuff(48,1800)（:27436）、蜂蜜史莱姆接触（:30904）、蜂窝饰品受击（:37905, 300t）。
- **Honey(48) 效果**（UpdateBuffs :18952-18956 + :9763）：lifeRegenTime+=2、lifeRegen+=2 = **1 HP/s**；lifeRegen<0（中毒等 debuff）时 +4 对冲（debuff 系统未移植暂缺）。
- **1456 数值修正**（对照 UpdateBuffs :9640-9702，推翻旧 Maples 数值）：Regeneration(2) lifeRegen+4 = 2 HP/s（旧"5 秒+10"废除）；Ironskin(5) **防御 +8**（旧 6）；Swiftness(3) moveSpeed+0.25；Thorns(14) thorns=1 → **反弹接触伤害全额**（num4×1，cap 1000，Game.damagePlayer 已接）；Campfire(87) 原版是 SceneMetrics 光环 lifeRegen++（:18990），本仓库沿用 Game 扫描续期表达。
- **蜂蜜物理**：浸蜜移速再 ×0.5（原版蜂蜜重力 0.1/落速 3，:24131-24135）。**溺水勘误(2026-08-13)**:1456 Collision.cs:1415 只排 lava/shimmer——蜂蜜同样溺水;现版 drownCollision(TouchDamage.ts:96) 只豁免 lt===2/4,与原版一致(此前备忘「蜂蜜不淹死」系误读,勿再回退)。
- **Buff 图标/文案**：Honey 进 UI buff 栏（图标 honey_bucket）；描述直接用原版 `BuffDescription.Honey`（12 语言 l10n 现成），名字走 `BuffName.Honey`。
- 测试：tests/buffs.test.ts 7 用例（max 合并/到期/Honey 速率与消退/叠加/铁皮 8）。帧积分断言要留 ±1 浮点边界。

**Why:** 蜂蜜 buff 是蜂巢闭环的最后一环（打破流蜜→浸蜜回血）；同时把旧 Maples 数值体系替换成 1456 权威值。
**How to apply:** 新 buff 一律：BUFF_DEFS 加条目（vanillaBuff id + descKey 优先用原版 BuffDescription）+ UpdateBuffs 对应 case 数值 + UI buildBuffBar/initInGameLite 两处列表。- **UI 对齐**（Main.cs DrawInterface_Resources_Buffs :42618 + DrawBuffIcon :42725）：起点 (32,76)、每行 11 个横距 38px、行距 50px、裸 32×32 图标无背景板（.sw-buff 类的 border/background 需 inline 清掉）、时长文字在图标下方（"29秒"/"1分34秒" 格式）、悬停 brightness 1.35 近似 buffAlpha 渐变、**右键取消**（TryRemovingBuff SoundID 12=menuTick）、**背包打开整栏隐藏**（refreshBuffs 每秒 + refreshAll 即时）。E2E：scripts/_buffprobe.mjs（注意 g.ui 不在 __swGame 句柄上，DOM 检查+Game 每秒 onBuffsChanged 刷新）。

关联 [[beehive-port]]。
