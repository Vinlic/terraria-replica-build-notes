---
name: sfx-distance-attenuation
description: 音效距离衰减移植——LegacySoundPlayer 2500px 公式、监听器=相机中心、x=-1 不衰减语义、进世界巨响根因
metadata:
  type: project
---

2026-08-10 音效距离衰减移植（用户报"全世界声音无衰减出现在角色耳边"）：

- **原版公式**（Terraria.Audio/LegacySoundPlayer.cs:381-401 + :160）：世界坐标声源 `vol × (1 - dist/2500)`，**dist ≥ 2500px 直接不播**；参照点是 **Main.Camera.Center（相机中心）非玩家**；`x=-1`（不传坐标）= UI/玩家自身动作声，**不衰减**；另有立体声 pan（`dx/(MaxWorldViewSize.X*0.5)`）未移植。
- **实现**：Sfx.ATTEN=2500 + `setListener(x,y)`（Game 每帧更新 camera.x/y）+ `atten()`；`play/playWav/playWavFile/playFiles` 全部加可选 `x?, y?` 参数（原版 PlaySound 带 x/y 的调用点对齐）；GameHooks.playSfx/playSfxFiles 接口加可选坐标。
- **进世界巨响根因**：`liquid.killTile → Game.breakTile → sfx.play('chop')`——waterCheck() 激活全图液体，每个活动液体格冲毁火把/植物（WATER/LAVA_DEATH 表）都全量播 Grass.wav，同一帧几十上百次叠加。修复=breakTile 的 chop 带tile坐标衰减（≥2500px 不播）。探针：scripts/_sfxprobe.mjs（patch Sfx.prototype 记录调用；进世界后 chop 0 次 ✓）。**声音该保留**（原版液体冲毁也响），只是要衰减——用户明确说"有声音不是问题"。
- **已带坐标**：breakTile chop、怪物挥击受击声（Game.swing 3014）、怪物死亡声（Enemy.hurt 尾 roar/killedSound）、僵尸环境声。**暂未带**（都在屏内差异小，待后续）：bossAI 族 36 处、Enemy AI 内散点（roar/spawn/splash 已有自带距离衰减逻辑的可保留）。
- **探针坑**：patch Game.prototype.breakTile 无效——HMR 双实例（?t= 后缀）；patch Sfx.prototype 有效因为两个模块实例共享原型？不——Sfx patch 生效而 Game patch 失败，原因是世界创建后 evaluate 注入的模块是同一 vite 模块图，Game 类在页面已实例化走旧模块。教训：**探针 patch 要在页面加载后立即装（createFlow 之前）或 patch 已实例化对象的方法而非原型**。

**Why:** 3D 音效衰减是原版基础体验（远处战斗/液体声渐弱），缺它=全图声音满音量灌耳。
**How to apply:** 新增世界事件声一律 `playSfx(name, vol, x, y)`；UI/玩家动作声不传坐标。原版衰减权威=LegacySoundPlayer.cs（别用玩家中心，是相机中心）。关联 [[dev-server-duplicate-modules]]。

## 全量音量表对齐（2026-08-13，Sfx.ts FILE_CASE_VOL 表 185 条）
原版权威链：LegacySoundPlayer.cs `num2×case修正×volumeScale`；num2=1- dist/2500；**主音量仅乘无坐标分支**(:418)。
最大历史偏差：**per-NPC Hit_20-54/Killed_23-57 缺 ×0.5**（半数敌怪命中/死亡声 2 倍响）——Sfx.ts FILE_CASE_VOL
按 wav 名单点统一乘，per-NPC 路径自动生效。case 14 僵尸呻吟恒 ×0.4、Item 55 ×0.5625、Drip ×0.5、瀑布 ×style/50×0.2 等。
调用点传值全部归 1（表内乘一次，防双乘）。修 MinionProj 'explode' 恒静音、bossAI Zombie_1→NPC_Hit_1。
**遗留**：ambient 分轨未建（:1443 集合 30-35/39/43/44-46/67-69 应走环境滑条）；带坐标声不吃主音量(legacy)我方仍吃；
Zombie_13+/105+ 低乘无调用点未入表。
