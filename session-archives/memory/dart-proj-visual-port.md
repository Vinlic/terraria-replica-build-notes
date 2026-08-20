---
name: dart-proj-visual-port
description: 敌怪弹幕 DART_STYLE 表:贴图/旋转语义/重力/加速/extraUpdates/渐入/火箭;射击怪→弹型全映射;XNA→canvas 旋转同号直接套
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T04:31:41.595Z
---

2026-08-12 用户报"鸟妖羽毛贴图角度不对应转 90°"。根因:全部射击怪弹幕是无旋转 8×4 色块;原版羽毛(Projectile_38)是竖版 14×24 贴图,rotation=atan2(vy,vx)+π/2(AI_001 尾 :54868)→ 竖版旋转 90° 尖朝弹向。

**Why**: 敌弹视觉+弹速此前全靠手填常数,原版每弹型的重力门/加速段/extraUpdates 才是权威。

**How to apply**:
- `Dart.ts DART_STYLE` 表(Record<projId, DartStyle>):w/h=SetDefaults 盒、rot 六模式(align90/a45/roll/spin/tilt/none)、alpha0+fade 渐入、light、grav/gravDelay/xDamp、accel{from,to,mul}、updates(extraUpdates=每 tick 完整更新次数)、noTile、life、trail、sfx(wav 直名)、rocket(303 Kill 128 盒爆)、shrink(288)、frameRand/animEvery、windSeed(836)、home(293 AI_051 vel=(vel*100+t)/101)、noTex(299 贴图 1×1 空桩纯尘埃)。
- **XNA→canvas 旋转同号直接套**(都顺时针正);swarmer 的符号反教训仅适用贴图方向翻转非 rotation。
- extraUpdates 是弹速关键:302 狙击弹 spawn 4×(7+1)次更新=32px/t;290 暗影束 updates=100 近似瞬达束。
- 射击怪→弹型映射(NPC.cs 行号在 Enemy.ts 调用点注释):哈比48→38/恶魔62,66→44(0.2 起步×1.06@ai0[30,100))/红恶魔156→115(0.2 起步×1.125@ai0<30+枪口+100px)/黄蜂→55/尖刺史莱姆184→174·204→176·535→605(重力0.15@5/0.05@15)/蚁狮69→31(g0.41 spin0.1)/爬行者101→96(spin0.3 Item20)/诅咒颅289→299(穿墙 extraUpdates2)/冰巨人243→257/岩巨人631→909(随机帧1-6)/NPC122→84/冰元素169→128/脓水268→288(32×32 g0.075 shrink)/战士族 RANGED_TABLE.proj:111,379,380→81/110,215→82/214,216,292→180/206→177/290→300(穿墙 roll)/291→302/293→303(火箭)/449-452→471(roll g0.4@20)/481→508(g0.3@61)/498-506→572/史后法师281,282→293·283,284→290·285,286→291/蒲公英628→836(风力转向+tilt vx*0.125)。
- 发射音 wav 按需拷贝自 terraria-assets/Sounds/ 到 public/sounds/(本轮补 Item_8/11/12/17/20/28);GameHooks.playSfxFiles 直放文件名。
- Game.ts:实体点光循环已含 projectiles 桶(Dart.lightRGB);netProjBroadcast Dart 分支须在通用 projId 分支**之前**(kind=2 tag=projId)。
- 联机探针注意:5199/5299 均可能是 vite preview(旧构建,类名 minified 如 'bt');起独立 dev(`npx vite --port N --strictPort`)后必须 curl /src/*.ts 验证服务的是源码。
- **静态 import node:fs 会炸整个浏览器 dev 引导**(并行会话 MushroomPass DBG 踩过)——node 侧调试写盘用环境门+`new Function('return import("node:fs")')()`。
- 验证:tests/dart-proj-styles.test.ts 12 例;_dartdrawprobe.mjs 像素级(羽毛 248px 质心偏右=尖朝弹向)。
- 遗留已入账 docs/spawn-parity-gaps.md:291 到点即爆/290 反射/44 phase1 转向/216 专家 240。
- **review 补修四件(2026-08-12)**:①299 noTex 曾漏画兜底短线→纯尘埃不画本体;②836 贴图是**横向 4 列胶片**(Frame(4,1,frame) Main.cs:33247,projFrameImg 竖切不适用→DartStyle.hFrames);③联机傀儡弹不跑 dartStep,alpha0=255 族恒透明→draw 对 netPuppet 恒 1;④尖刺族发射音 174/176 Item17、605 Item154(:52166/:52244/:52222);另 290 life=300(NPC.cs:21191 覆写非 SetDefaults 的 100)、冰巨人 257 枪口 (cx+10×dir, y+20)+vel×3。
- alpha=255 族(572/128/177/288)渐入 -50 是族标准,这四型的递减行在 AI_001 未定位到(已入账,视觉不可辨)。
- tsc 若见 GUN_SHOTGUN_VIDS/UI.ts favorited 报错=并行会话在途,非本域。

相关:[[enemy-ranged-transform-audit]] [[explosion-sfx-port]] [[dev-server-duplicate-modules]]
