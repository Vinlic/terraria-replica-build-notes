---
name: proj-rotation-right-art
description: 弹幕旋转两族——AI_001默认+π/2(箭/子弹朝上)vs朝右贴图ToRotation族;食人鱼190/魔法飞弹16/Flamelash34五款入表
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-13T10:45:46.554Z
---

2026-08-13 用户报"食人鱼枪的鱼角度差 90°"——Arrow generic draw 恒 `atan2+π/2` 只对"贴图朝上"族正确。

**原版两族(核实锚)**:
- **默认 +π/2**:AI_001 尾部兜底 `rotation = atan2(vy,vx)+1.57f`(Projectile.cs:54877)——箭 1/子弹 14 等贴图朝上族 ✓ 我们恒 +π/2 对这族正确
- **朝右族 `rotation = ToRotation()`**(贴图头朝右,向左运动按 spriteDirection 水平镜像):AI_001 显式分支(:54715 MIRROR 837/:54755-54780 ToRotation 408/435/459/682/709/436 等)+ 非 aiStyle1 自家 AI(190 食人鱼 :26122-26140、16 魔法飞弹 AI_009 :54039、34 Flamelash AI_020 族)

**修复**:`PROJ_ROT_RIGHT` 表(Arrow.ts,导出;tests/proj-rotation.test.ts 锁){16, 34, 190, 837, 1023};canvas 等价变换 `scale(-1,1)+rotate(π−ang)`(vx<0)≡原版 flip+atan2(−vy,−vx)。generic draw 同时按 projFrameCount 帧切片(34 是 48×384 八帧行,190 四帧/837 三帧——防胶片压扁,单帧走整图)。

**审计工具**:scripts/_projrot-audit.mjs(经 run-diag)——扫 AI_001 type 链 + 已登记武器 shoot × 原版 rotation 分类;新武器登记后重跑可续查。

**登记后接**(未实装物品):1313 骷髅头法书(837 MIRROR)/5460 发射器(1023 wiggle)/3787 天空断裂(660 ToRotation+π/4,Portal 同款需查 Portal.ts 路由)。aiStyle 9/20 可控导弹族(16/34/107/252 等)行为层仍是直飞近似(原版 channel 操控)——行为 GAP 另案。

## 剑气族第三档 +45°（2026-08-17，用户报"附魔剑光束角度偏"）
aiStyle 27 尾部（Projectile.cs:24858-24861）：rotation = atan2(vy,vx) + **0.785**——
斜向剑气贴图，区别于朝上 +π/2 与朝右 +0 两档。PROJ_ROT_DIAG={114,115,116,132,156,173}；
1.4.5.6 可达三枚：114(683 邪恶三叉戟)/116(723 光束剑)/173(989 附魔剑)；例外 157 夜波
=direction×0.4 旋转体（无武器射出，登记未移植）。旋转档位共三档：RIGHT(0)/DIAG(π/4)/UP(π/2)。

## 武器弹幕旋转全审计（2026-08-17，用户令 review 同类）——五修复+登记
方法：itemcombat 全表 shoot × projectiles aiStyle 分组 → AI_001 尾链（:54660-54870）
逐分支解析（node 脚本 else-if 切分）∩ 武器可达集。**箭矢三档之外还有两种模式**：
- **直立族**（aiStyle 29 :24994-25207 零 rotation 赋值）：宝石法杖箭 121-126（六色杖
  739-744）/521 水晶脉冲/597 琥珀箭——恒不旋转，曾对速度 +π/2 翻滚 ❌→PROJ_NO_ROT。
- **恒旋族**（rotation 逐帧累加）：312 南瓜灯 +=vx·0.02、772 晶洞 +=sign(vx)·|v|·0.05
  （PROJ_SPIN 表+spinRot 累积）；同链 248/483/532/675/921/926/937 无武器可达。
- 660 天穹碎裂 →DIAG(+45°)；485 地狱之翼（:54844-54853 vx<0 翻转+atan2(−v)）→RIGHT；
  469 蜂箭 → 默认角+vx>0 源翻转（贴图朝左）。
已等价：684/711/712（+π/2=默认）、477（平滑≈默认）、639/710（重力分支非旋转）、
1023（wiggle 近似既有收案）；登记 C 级：311 糖果玉米反弹态 spin、157 夜波旋转体
（无来源武器）。默认分支排除项 344/498 不可达。AI_002 投掷族 tumble 既有收案 ✓。
测试 proj-rotation 9 例。**审计法在档：shoot×aiStyle 分组→AI 尾链解析→∩可达集。**
