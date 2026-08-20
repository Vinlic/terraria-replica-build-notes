---
name: proj-draw-offset-table
description: 投射物绘制偏移表 num143/num144 移植——炸弹引线出盒对齐的权威公式与已备案动态项
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-18T07:33:23.041Z
---

投射物贴图与碰撞盒对齐走原版 **num143/num144 偏移表**（Main.cs:29375-29826）+ 通用绘制公式
（Main.cs:34040）:anchor=(盒左+num145+num144, 盒上+盒高/2),origin=(num145, 盒高/2+num143),
num145=(贴图宽+盒宽)/2 → 展开后**贴图左上角=(盒左+num144, 盒上−num143)**。典型:炸弹 28
上移 8(22×30 贴图,引线 y=0-7 全在盒外,弹体恰填 22×22 盒,:29560);雷管 29 上移 11。

本仓:`WeaponProj.ts` `PROJ_DRAW_OFFSET` 118 条静态项(2026-08-18 脚本机械对拍 118/118 全对)。

**Why:** 曾按"贴图中心=盒中心"绘制,引线半截进盒(用户校准 {x:1,y:8,w:22,h:22} 指出)。

**How to apply:** 新投射物视觉错位先查该表再手调。消费端(2026-08-19 全接):①WeaponProj.
drawProj(武器弹)②**MinionProj.draw(aiStyle 26 随从族——该表主体即此族,曾从未消费,
一律盒心居中;现走 anchor=(盒左+num145+num144, 盒上+h/2) 公式,共享 projDrawOffsetFor
导出;AI_026 spriteDirection 恒−1→dirX=−1;未登记型号维持居中=备案差异,原版=盒左上对齐)**
③397 燃烧瓶经 GrenadeProj。浮标已接(2026-08-19:Bobber 走公式+bobber num143=8+钓线段链 DrawProj_FishingLine 1:1,含竿尖表/线色表/张力摆垂 lai0)。MINION_NO_FLIP 曾漏
112/959/1003/1004/1095/1096(同 AI_026 零赋值却被 facing<0 误翻)。验证法:拦截 5 参
drawImage 断言 dest 原点=(-num145, -(h/2+num143));★9 参形态是帧切片制作调用勿混淆;
浮点须容差。关联 [[melee-hitbox-sprite-base]][[summoner-full-parity-batch]]。
