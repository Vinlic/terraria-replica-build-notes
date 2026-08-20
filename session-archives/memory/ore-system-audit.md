---
name: ore-system-audit
description: 矿物分布/出产时机审计:Shinies+宝石+oreTiers+陨石+暗影珠链+祭坛公告全 1:1;仅剩祭坛拆除盒邻坛误拆小项
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-13T05:54:26.211Z
---

2026-08-13 矿系统审计(对照 Terarria1456):

**已 1:1 核对通过**:Shinies pass 全密度/区间/注册序(cs:13487-13657)、宝石密度配对
63↔0.3…68↔0.05(:15109,`TileID.Sapphire=63` 勿凭记忆倒序!)、双矿种 Next(2)==0→替代
(:11286)、狱石(UnderworldPass)、邪恶矿 2.25e-5 岩下。

**砸祭坛修复三偏差**(Game.ts smashAltar):①矿种改世界锁定 SavedOreTiers 语义
(每档首砸 roll 一次固定,随存档持久化 world.savedOreTiers,七点补全:
World/SaveFile×2/serialize×2/SaveClient/protocol/worldPacket——照 altarCount 模式;
此前每砸重 roll 会同世界混出钴+钯)②OreRunner 区间 Next(5,10) 恒定(旧 5..9+w/4200
系误读)③替代矿(221/222/223)×0.9 密度+钴档恒 ×1.05。**叶绿转化目标修正**:仅泥块 59
(cs:69716 严格 ==59,曾误含丛林草 60 直转)。

**遗留缺口(已全部清零 2026-08-13)**:
- ~~祭坛拆除盒~~ 已修:3×2 对象语义,frameX 含 style×54 偏移须 %3 回推列号

**暗影珠/猩红之心链**(2026-08-13 已落,smashOrbHeart = CheckOrb cs:54259-54358 1:1):
- 战利品五档:首破(!shadowOrbSmashed)固定 0 档,后 rand(5)——腐化{96火枪+凝胶100,
  64暗影珠,162堕落荆棘,115刺球,111}/猩红{800+凝胶100,1256,802,3062,1290};
  vid→key 走 VANILLA_ITEM_KEY_BY_ID(旧版给可疑眼球/银币是占位错值)
- shadowOrbCount 持久化(WF:1302/2099,照 altarCount 七点链)满 3 召 EoW(13)/
  BoC(266)(对侧变体存活则跳过)归零;1/2 颗广播 misc[10/11]
- **砸祭坛世界公告已接**:misc[12/13/14]+9 按锁定矿种选文案(l10n 键已全在,
  零新增成本);1.4 语义砸珠不触发陨石(触发=EoW/BoC 击杀,见上)
- **wld 导入三字段已接**(2026-08-13 收敛):WldParser 曾"读了就扔"(:164/165/172)→
  捕获 shadowOrbCount(WF:1302 byte)/altarCount(:1303 i32)/SavedOreTiers(:1315-1317)→
  WldImport 写 SaveData **顶层**(非 header!altarCount 槽位同侧)→ loadSaveData 回填。
  测试 wld.test 合成固件改非平凡值断言全链往返

**并行会话协同**:陨石/流星雨区域是热区——他们补了 677 远古蓝砖进保护表、
meteorShowerCount 持久化+1078 碎块化、lighting.dirty;勿重复改 MeteorFall.ts。
tsc 当前 2866(wiring 可空)/3202(st 未定义)/4653(heldDef) 均为并行进行中代码。

**陨石全链**(2026-08-13 已落,前为并行会话首版+本会话按源码纠偏):
- 触发三源已接:夜 1/50 门 downedBoss2(Main.cs:64715,灯笼夜压制)/EoW/BoC 击杀
  首杀必触后 50%(NPC.cs:80241-80259)/LanternNight ctx spawnMeteor 位
- 消费=原始 Main.time>16200(夜午夜后/昼 9AM 后——白天杀 EoW 当天落是原版行为,
  Game.ts rawTime 换算)
- 纠偏清单(旧版 vs 源码):玩家盒 ±62/±39px→±1022/±639(2044×1278,注释写了常数
  实现却差 16 倍);云打分集合 {86}→Clouds{189,196,460,717-719}+202;打分盒 31×31→
  30×30(上开);列扫描缺 tileSolid 门;阈值 600−0.5 仅低分时衰减(保护中止不衰减);
  **五层生成必须独立循环**(空腔在主体后雕刻——单遍 continue 合并会致空腔永远不生效
  =实心矿球);毁灭表 {5,32,352,583-589,596,616,634};保护块 BasicChest{21,467}+
  地牢砖{41,43,44}+{26,226,470,475,488,597};浮空 37 修剪+清液+ClearSlope
- host.npcs 须含城镇 NPC(原版 Main.npc 全量);落点后必须 chunks.markDirtyArea
  (setTileSilent 不触发 onTileChanged,否则陨石坑不渲染——纯数据文件调用方负责失效)
- 测试 tests/meteor-fall.test.ts 5 用例(空腔存在性是五层顺序的回归锚)

相关:[[vanilla-worldgen-port-status]] [[gem-anchor-gate-port]] [[save-parity-port]]
