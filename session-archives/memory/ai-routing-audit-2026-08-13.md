---
name: ai-routing-audit-2026-08-13
description: AI 路由双门全量审计:594 灰史莱姆根因=主 switch 缺 case;4 命中(628 补路由/690·618 整 AI 移植/453 误报)+音效 Custom/ 前缀 404 隐患+619 json 补条
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-13T03:41:13.804Z
---

# AI 路由全量审计（2026-08-13，594 风气球"灰色吊起史莱姆"报障的同类清查）

**审计方法**（可复用）：vanilla-npcs.json 全条目 (id→aiStyle/critter/townNPC) × Enemy.ts 主 switch case 集 × critterWanderAI case 集三表对账。三类检查：A. 非 critter NPC 的 aiStyle 缺主 switch 登记（→ default zombieAI）；B. critter 的 aiStyle 缺 critterWanderAI 登记；C. critterWanderAI 登记的 aiStyle 也被非 critter 用但主 switch 缺（594 同型）。**注意 townNPC:true 要剔除 + Game.trySpawnEnemy 会把 453 转 TownNPC（spawner 注释有写）——不查生成路径会出误报**。

**命中与处置**：
- 628 蒲公英：主 switch 补 `case 119`（dandelionAI 已存在）✓
- 690 雕像宝箱怪：整条 AI_126 移植（Enemy.statueMimicAI + case 126 + fromVanilla dontTakeDamage=true[:17615] + Renderer.drawStatueMimic 用 **Tiles_105 切 2×3 片**拼雕像[Main.cs:23103，本体贴图弃用，方向+3 行镜像] + ai1=Next(83)拒绝43-49 样式[WorldGen.cs:37934] + 三音轨 statuemimic_*)
- 618 恐惧鹦鹉螺：整条 AI_117 移植（bloodNautilusAI + case 117 + reflectsProjectiles 基建已存在直接接 + CallForHelp 召唤链：SquidCloud.ts[弹 813，90t 出鱿鱼] + DART_STYLE[814] + json 补 619 血鱿鱼[frames=6，swarmerAI accel 0.1 档] + 旋转链登记 stR===117 保镜像）
- 453/588/633/663：误报（TownNPC 注册）
- 出场时序坑：618 首帧 ai2=direction（target==255 分支），退出 ai2≥50 四槽清零；脉冲在 ai1==90 当帧即发（首帧 =BLOOD_WIND 就进 fire 支）——测试循环计数易差一

**顺手挖出**：
- **WAV_MAP 'Custom/' 前缀恒 404**：copy-sfx.mjs 把 Sounds/Custom/ 展平进 public/sounds/ 根，Sfx.ts 里 dd2 四轨带前缀全部静默无声——已改平铺名。新轨（statuemimic_×5/Item_150/170/171/172）已入白名单并拷贝
- reflectProjectile 的 Item_150 已补素材（此前 tink 兜底）
- canHit 签名被并行会话从点参数改成盒参数（9 参）——Enemy 直调点要先重读签名

**遗留备案**：贴图布局扫描（json frames vs PNG 尺寸）除 594/690 外无 spawnable 命中（328 未使用占位）；蜜蜂/蜻蜓等小帧高是误报阈值。squid 619 渲染帧率（原版 1/6t 定速）走通用 walkCycle 近似，未 1:1。

相关：[[critter-ai-port]]（路由双门坑原始记录）、[[meteor-fall-port]]（双会话并行约定）
