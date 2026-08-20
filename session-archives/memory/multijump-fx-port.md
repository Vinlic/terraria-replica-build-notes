---
name: multijump-fx-port
description: "多段跳特效全链补齐:起跳帧(音Item_16/屁瓶10尘188+3gore435/航行30尘253)+持续尾迹doubleJumpVisuals五分支(沙暴3尘124/tick+gore220-223沙云随平台段缩放/暴雪三段8尘76/云屁1尘/航行1-2尘253);performingJump标记落地清;探针armor[3]塞配饰非末槽(10-19时装镜像)"
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-17T03:44:57.681Z
---

多段跳配饰特效补齐（2026-08-16，用户："沙暴瓶这种佩饰飞起时脚后应有粒子效果，没移植完整"）。此前多段跳只有速度/平台段，**起跳帧特效与持续尾迹全缺**。

**原版两段式**（Player.cs）：
- **起跳帧**（JumpMovement :20521-20620 各 flag 分支）：沙暴/暴雪/屁瓶/航行播 SoundID 16（Item_16.wav）；屁瓶=10×尘188（区域 x-34,102×32）+3×gore435-437（中/左-36/右+w+4）；航行瓶=30×尘253（奇偶 vx±(30,71)×0.1）；沙暴/暴雪仅音效。
- **持续尾迹**（DoubleJumpVisuals :21615-21745，Update :26445 每帧）：门=isPerformingJump_* 置位 + 上升中（vy×gravDir<0；航行瓶放宽 <1）——沙暴 **3×尘124/tick**（scale num4=(jump/75+1)/2 随平台段剩余涨、fadeIn1.5num4）+每 miscCounter%3 gore220-223 沙云（v=velocity×0.3num4、alpha100）；云瓶/屁瓶 1×尘16/188（脚底 w+8×4 条带、v 反速衰减）；暴雪三段 8×尘76（2 慢散±v0.03 + 3 顺速 +0.8v + 3 逆速 −0.8v，noGravity/noLight）；航行 1-2×尘253（平台段中 2 粒顺速−v/5、尽后 1 粒 scale×0.8）。

**实现**（Player.ts）：`performingJump: string|null` 标记（isPerformingJump_* 等价，**落地清除**——extraJumps 重置处）；起跳特效内联在多段跳消费段；`doubleJumpVisuals(game)` 五分支 1:1（挂 extraJumpCd 递减后）；gore 走 GorePiece.newGore。独角兽坐骑跳尾迹（尘176/177/179）未接（mountJumpPerforming 处，坐骑批领地）。

**探针坑**：塞配饰必须 `inv.armor[3]`（3-9 功能配饰槽）——`armor[armor.length-1]`=armor[19] 是时装镜像槽不进 equipStats 聚合；尘池直接 `game.vanillaDust.pool.filter(active).map(type)`。验证：沙暴二段跳尘池累积 153×尘124 ✓。

标签集实况：Cloud/Sandstorm/Blizzard/Fart/Sail（accfx json 17 件；'Tsunami' 仅代码兜底无数据件——海啸瓶原版并入 Blizzard 效果档）。

**二批：跑靴奔跑尘+脚步声**（SpawnFastRunParticles :19935-20027 + :36285 授予表，同日）——原 Completely 缺失：
- 门（:19697/:19731）：`|vx| > (accRunSpeed+maxRunSpeed)/2 && vy==0 && 无坐骑`——赫尔墨斯 6/3 → 阈值 4.5（冲满需 ~190t：3→6 慢爬坡 0.016/t，探针须跑 4s+）。
- ★**尘门是结构嵌套门非全局门（2026-08-17 用户原版实测纠偏）**：原版调用点嵌在爬坡分支 B（else-if，入口 `vx<accRunSpeed && !slow && !burned`）**内部**、加速步之后。分支入口门 vx<accRun 与尘门 vx>中点构成互斥带——**裸装 accRun==maxRun==3 → 带 [3,3) 空 → 永不触发**（原版裸装跑动零尘零脚步声，用户实测铁证）。曾误提升为 ix!==0 顶层全局判定 → 裸装锯齿 3.04 越线误触发蓝尘+脚步声。修复=调用点移入 B 分支内（Player.ts 水平链 else-if）。验证 _runfxtrace.mjs：裸装 0/0，赫尔墨斯 6s fireCount=220、顶部锯齿 [5.82,6.01]。**教训：原版 if/else-if 嵌套结构本身承载语义，平铺成"全局门+条件"会改变真值**。
- equipStats 新增 `bootFx`（按装备 vid :36285 switch）：4874 泰拉闪耀=火尘6(vy=-1.5-rand.5/fadeIn.5) / 3200·3990 航行=尘253×4 全身 / 1579 冰靴=雪尘76×2(脚底两半/scale1.2-1.4/noGravity) / 4055 沙丘=沙尘32(vy-gd×2) / 3993 仙灵=尘61·242·64·63 加权×2(k=2 再 pos+=v)；**其余跑靴(54/405/898/1862/5000…)=尘16（天蓝色十字闪光，见五批裁决）×1+脚步声**（hermesStepSound=SoundID 17→Item_17、冷却 9t :35517）。
- 探针验证：赫尔墨斯尘16×57 / 冰靴尘76×5 ✓。
- **坑**：ITEM_DEFS[].vid 字段可能 undefined——取 vid 必须 `def.vid ?? viIdFromKey(def.key)`（UI 层 vidOf 同源写法）；裸 `.vid` → -1 → bootFx 恒 null 走普通分支（二轮探针抓出）。
- ~~翅靴分支未接~~ **三批补齐（2026-08-16）**：`wings==3 || 时装槽 668`（Red's Leggings → vanityRocketBoots=6 :12667-12670）→ **尘186×2**（if 链首，优先于五靴型；色=cWings **翅膀**染料 wingDyeVid——Red's 无翅膀场景原版 cWings=0 同样无色）。
- **四批撤近似·染料全量真链**（用户令"禁止近似"）：VDust 加 `dyeVid`；Player 尘只带 vid 不带静态色；**Renderer.drawVanillaDustPass 跑 SM2 染料字节码**（applyDyePass 63-pass 全技术——彩虹 uTime 动态/凝胶相位/反射光照(reflectiveLightSource)/HallowBoss 双采样逐尘逐帧真跑；uDirection=玩家 facing）。**ArmorColored/Default 静态族**按 `dyeVid|fx|fy` 缓存染帧（256 上限，输出与 uTime 无关=无损缓存）。uSourceRect/uImageSize0 传尘帧在 Dust.png 表内坐标（翅膀链同构）。doubleJumpVisuals 尾迹尘**不带**染料（原版 :21615-21745 无 shader 赋值——勿画蛇添足）。探针：冰靴+红染料 1007 → 尘76×25 带 dyeVid=1007 渲染零错。
- **修复链教训**：Edit 注释头锚点吞方法签名（旧法重复+签名错接 doubleJump 注释）；python 段处理跨方法溢出（边界须以方法签名为界双侧核对 + tsc Duplicate/missing 双报错即结构串位）。
- **五批·尘16 真容裁决（2026-08-17，用户问"跑动出天蓝色泡泡？"）**：尘16 **不是白色烟团——是天蓝色十字/星形闪光**。贴图逐像素（canvas 解码非视觉模型）：Dust.png(160,0/10/20) 三变体 = RGB(105,155,255)/RGB(189,211,255) 蓝十字。原版裸装/普通跑靴全速踢出的就是它（else 分支 :20021 同款；Lightning/Frostspark 靸的蓝闪尾迹同源）。铁证：①原版 ChildSafety 把危险尘（血等）统一替换成 16 型（Dust.cs:191-204）=原版"无害闪光"标准粒子；②Dust.png 布局=1000×120、100 列×4 带×3 变体行，NewDust 自带换带 `while(t>=100){X-=1000;Y+=30}`（Dust.cs:176-186），`frame.Y=10*Next(3)` 三行变体都真用；③正午 lightAt=(210,210,210) 纯白，颜色全来自贴图。**教训：视觉模型读 8px 小贴图颜色不可信（曾误报"白色圆点"），须 canvas getImageData 逐像素**；裁帧必须带 fy 变体维（曾只裁 fy=0）。
