---
name: thrown-physics-fix
description: 投掷武器距离偏短根因=误用箭矢物理档;原版aiStyle2默认档=20t平飞/0.4重力/0.97阻力/终端32/翻滚
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T02:27:32.588Z
---

2026-08-13 修复"投掷武器扔出距离偏短"。同批修**丢弃抛出**（UI.throwHeldToWorld）：原版 DropSelectedItem（Player.cs:4993-4997）`vy=-2、vx=4×朝向+玩家水平速度`+`noGrabDelay=100`（:4990/:4996 抛出者 100t 拾不回）；我方曾 facing×1.5 不叠速度（距离≈1/3）。ItemDrop 加 `noGrabDelay` 字段（拾取门 age>PICKUP_DELAY(25) && age>noGrabDelay）；UI 传 4×facing+p.vx。测试坑：时序断言须每 tick 钉回玩家盒（重力会把掉落物带出 42px 拾取范围）；物品 id 须走 VANILLA_ITEM_KEY_BY_ID[2]→ITEM_BY_KEY（vi_ 迁移后裸 id/旧锚表 dirt_block=10000 已失效）。

**原版权威**（Projectile.cs AI() aiStyle==2 块）：
- 出膛速度 = normalize(鼠标−手位) × item.shootSpeed，无玩家速度叠加（Player.cs:46652-46677 ItemCheck_Shoot；PickAmmo 对 useAmmo 武器 speed=武器+弹药 shootSpeed）。
- **默认档**（:21955-21977，手里剑 3/飞刀 48/毒刀 54 等）：前 **20 tick 无重力平飞** → 每 tick `vy+=0.4`、`vx*=0.97` → 终端 **32**。
- 翻滚（:21508）：全体 aiStyle 2 自出生 `rotation += (|vx|+|vy|)*0.03*dir`；**48/54/93/520/599** 平飞期姿态锁定 atan2（:21971-21972）。
- 子分支例外（勿一刀切）：type 370/371/936 = 15t 延迟 0.3/0.98；304 吸血鬼飞刀 30t 无重力渐隐；909 = 38t 0.4/0.97；type 特化各档（0.2~0.5）——泛化时须按 type 分流。

**我们曾错**：Arrow 一律"出生即 0.3 重力/无阻力/终端 16"（`projGravity()` 注释"ai2/16=0.3 实测值"是错的，0.3 只属个别子分支）→ 投掷距离显著偏短。

**修复**：Arrow 新增 opts `drag`（X×/tick，默认 1）/`maxFall`（默认 16 不变，箭矢行为零扰动）/`tumble`+`tumblePoseLock`（翻滚累积角 tumbleRot，draw 分流）；Game 投掷分支（4619 一带）传 `{grav:0.4, gravDelay:20, drag:0.97, maxFall:32, tumble:true, tumblePoseLock:48/54/93/520/599}`。

**未动（登记）**：手雷 166 走独立 GrenadeProj（aiStyle 16 弹跳引信，物理另有公式待对账）；`projGravity()` 仍返 0.3，消费方仅近战族投射（useCombatWeapon 回旋镖路径，影响面小）；弓箭 aiStyle 1 重力 0.3 与原版一致（速度=弓+弹药 shootSpeed ✓）。tests/thrown-physics.test.ts 5 条（平飞/0.4+0.97/终端32/翻滚/世纪之花种子档回归）。相关 [[flail-statusnpc-port]] [[plantera-parity-audit]]
