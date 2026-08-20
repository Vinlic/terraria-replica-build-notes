---
name: king-slime-crown-ninja
description: 史莱姆王视觉——金冠=Extra_39叠画(Main.cs:25571另一switch，grep "type == 50"会漏)、忍者=Ninja.png叠画、母史莱姆死亡分裂Baby(-5)
metadata:
  type: project
---

2026-08-10 史莱姆王视觉对齐（**第二轮修正：第一轮结论"无冠"是错的**，用户指出 Wiki 有冠后复查破案）：

- **金冠确实存在且常态佩戴**：Main.cs:25571-25595 `case 50:` 用 **TextureAssets.Extra[39]**（Extra_39.png 82×56）叠画。**教训：它在另一个 switch(type) 里（case 50: 写法），grep "== 50" 搜不到**——DrawNPC 有多段 type 分派（22798 忍意块 + 25571 光罩/叠饰 switch）。几何：锚=KS Center 上移 `(70-num223)×scale`，num223 按帧序 [2,-6,2,10,2,0]；朝向翻转继承；无旋转。贴图部署 vanilla/Extra_39.png + VANILLA_MISC。
- **忍者**：Main.cs:22798-22818，Ninja.png 叠画在 Center，offset=(-vy,-vx*2)、rot=vx*0.05、帧 120/360/480 y 修正。两者已都移植 Renderer.drawEnemy（vanillaId===50 块）。
- **Gore 734**：专家传送时抛冠演出（NPC.cs:43550），与常态叠冠并存——"drops his current crown"。
- **KS 不召唤小怪**（AI_015 无 NewNPC）；bossAI.kingSlimeAI 落地 30% 出母史莱姆是自创。
- **母史莱姆(16)**：配色=灰剪影×alpha120×color黑50（半透明灰黑）；**死亡**分裂 1-3 Baby Slime（netID -5，wiki 权威；非受击——已实现 Enemy.hurt 死亡分支）。
- 探针坑：canvas 多层须用 g.renderer.canvas；headless 采样要 explored.fill(1)+白天+多帧 rAF；Wiki 主图/动图=Bestiary 合成（金色斑纹遍布全身≠游戏内观感，别拿 wiki 图当贴图判断依据）。

**Why:** 第一轮"贴图无金像素→无冠"推理链断了：贴图确实无金，但金冠是另一张图叠画的。**How to apply:** 查 NPC 视觉缺口必须搜全 DrawNPC 的**所有** type 分派段（`case N:` 与 `== N` 两种写法），并搜 TextureAssets.Extra[] 数组访问（Wiki Trivia 常给内部文件名线索——"Ninja and Extra_39 internally"一句直接定位了资产）。关联 [[vanilla-npc-port]]。
