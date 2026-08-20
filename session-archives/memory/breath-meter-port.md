---
name: breath-meter-port
description: 呼吸计全链1:1:CheckDrowning/DrownCollision(蜂蜜也淹)/10气泡UI锚点顺序坑/火焰条槽数整除语义
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-12T15:08:33.491Z
---

2026-08-12 呼吸计(气口)全链 1:1 移植完成(显示+机制):

- **数据模型**:自造 5 气泡/23.33s 废弃 → 原版 `breath: int 0..200`/`breathCD`/`breathCDMax`(7,芦苇管×2,潜水盔×6,Player.cs:3693)。breathMax=200 全源码无修改点(潜水头盔加的是 breathCDMax 非 breathMax)。
- **DrownCollision**(Collision.cs:1385):头部盒(px+w/2 居中宽10, py-2, 高12);**蜂蜜也淹**(只排岩浆/微光);液面 drop=(256-liquid)/32;顶部行(gravDir==1 取扫描首行)active+solid+非 platform 豁免;j 钳 maxTilesY-40(**测试世界需 h>80 否则扫描区为空**)。
- **直伤语义**:breath≤0 后每 breathCDMax tick `hp-=2` 直伤——不过防御/不吃无敌帧,不能走 damage();breath 减到 0 的同一 tick 即开始扣血(SoundID 23 也同 tick)。
- **显示**(Main.cs:42824,新建 render/BreathMeter.ts,UI pass):气泡数=floor(breathMax/20)=**10**;26px 间距、x-125 起点、y=32+(22-22*scale)/2;部分颗 alpha=30+225r(≥30)/scale=r/4+0.75(≥0.75);**耗尽颗照画无跳过分支**;i>10 第二行(−260,+26)。
- **锚点顺序坑**:Top →(inventory 开&&屏高<1000:世界空间+h-20)→ worldToScreen →(否则**屏幕 px** -100,不乘 zoom)→ /UIScale(恒1)。-100 是屏幕空间!
- **火焰条**:flag=lavaTime<lavaMax&&(lavaWet||breath==breathMax)→火焰条替代气泡;槽数=floor(lavaMax/floor(lavaMax/10)) 整除语义(420→10);源矩形 quirk 用 Bubble 尺寸画 Flame。
- **装备**:vanillaAccFx.ts BEHAVIOR_FX 代码层补表(生成 json 勿手改):268(armor,走 recalcEquip 盔甲三件扫描)/394/1860/1861→divingHelm,497/861/3110→merman+nightWolf(851 是绿扳手勿抄!)。9 件物品已入 items.ts+WldImport(250/4275/268/394/1860/1861/497/861/3110),vanilla-itemstats 的 hs/acc 自动接装备 UI。1861 另有 arcticDivingGear(专家雪原冷水 Chilled :27692 门已移植,environmentBuffImmunityTimer 未实装恒 0),1860 另有浸水发光(1.8/0.4/1.2 已接 Game 光照)。ftw 种子 gills 翻转已接(world.seedFlags.getGoodWorld)。溺水口部 dust 34(:23003)已接 spawnParticles 近似。
- **非偏差勘误**:远端联机玩家无气泡条是原版本地专属语义(player[myPlayer]),非偏差;gfxOffY 恒 0 与无坐骑原版一致;史莱姆鞍是坐骑系统引擎级缺口(一行 if 预留)。
- 顺带修:respawnPlayer 缺 breath=breathMax/lavaTime=lavaMax 重置(原版 :37158/:37173)。
- 探针教训:表面灌水会被液体 sim 排干 → 密封石壳水箱;截图数气泡用 pngjs 按列聚类(26px 间距验证)。
- 有意偏差:ftw 种子 gills 翻转/史莱姆鞍/gfxOffY/芦苇管 dust/远端联机玩家无气泡条(注释存档于代码)。
