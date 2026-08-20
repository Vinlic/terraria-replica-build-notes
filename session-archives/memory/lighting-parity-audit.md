---
name: lighting-parity-audit
description: 发光物全量对账三路+P0修复批+收敛批:ProjLight绝对通道/Dart双注摘除/tile光源66+动态33/掉落物全分支/水母笼态机/风格族四表
metadata:
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-13T09:46:46.789Z
---

发光物全量对账（08-13 三路代理：tile/墙光源、弹幕/NPC 光、算法+天空光+手持光）+ 收敛批全落地。测试 23/23 绿（tile-light-specials+minion-kb+nebula+explosion+sky-invariant）。

## 已修（P0 批）
1. **昼夜窗口** skySeed isDay (0.25,0.75)→(0.1875,0.8125)；2. **月相地板倒置** MOON_FLOOR [19..11..17]；3. **血月夜曲线**；4. **闪烁族收敛** FLICKER_SHEETS={405,215,592}；5. **致动块发光门**摘除；6. **宝石灯墙七条**；7. **魔矿色** [31,18,82]；8. **灯笼 default** [1,1,1]；9. **传送门炮双档色**（PortalHelper.cs:387 单人档 hsl：portal0=hsl(0.12)=橙、portal1=hsl(0.52)=青——金标测试曾断言反色已更正）；10. **微光液体光**；11. **非原版光源移除**；12. **shimmerTorchColor 公式**；13. **WALL_LIGHT 补 73/227**。

## 收敛批（08-13 下午，全部对源码核过）
- **ProjLight() 1:1 全函数转写**（Game.ts）：PROJ_LIGHT_MUL 乘区表 + **PROJ_LIGHT_ABS_CHAN 绝对通道表**（原版 `num3=1f` 等绝对赋值——44/45 B=1、488 全绝对、15 R=1、16/27/72 B=1、86 B=0.75、87 G=1、173 G=0.4、870 G=0.35）+ 动态档：79/1089=Disco 绝对、**251=light×(Disco+1)/2**（先白化再乘回）、993=light×Disco、867/1000=闪烁公式绝对、209=alpha 渐变乘区、211=light 帧序自改写(1.0/1.5/1.0)、259=getGoodWorld 零化、**870=FloodFillTile 4.5 穿墙播光**（DelegateMethods:805 内容格扩展空气格不播——BFS 助手 addProjFloodLight）
- **Dart st.light 全摘除**：44/84/96/115/180/257/302=ProjLight 标量循环重复（96 曾灰色 vs 原版绿(0.35,1,0)、257 手调蓝）；596 原版无光；**814 原版无光（红光是 819 的 :53558——审计曾错挂）**。DartStyle.light 字段删除
- **实体自报光跳过门**：标量循环遇 entity.lightRGB 跳过防双注（985 泰拉刃 :39382 绿光+光心前偏 85px lightRGBAt、502 喵刀 :22611 (0.5+Disco/255)/2——Arrow.ts:451 公式精确无需动）
- **Bobber projId**：★5139-5146 **不是钓竿是浮漂饰品**（Item.cs:41803-41840 DefaultToAccessory+glowMask 318-324——曾误当竿）——全链已实装：items.ts 八条注册+itemstats acc:1（5140-5145 提取器漏 fallthrough 已补）+Player 装备扫描（fishingSkill+10 :12552/:14121 + overrideFishingBobber=986+(vid-5139) :36244）+Game 抛竿侧覆写优先（:46551）+bobberProjIdFor 摘 5139 分支；竿映射=Item.cs:23001（2291-2296→361-366、2289→360、4325→760、4442→775）
- **bossAI_martian**：:149 SkyBlue(135,206,235)/255×0.65=(0.344,0.525,0.599)/Red×0.65；:637 造假常光摘除（aiStyle74 块无 AddLight；自爆 [0.2,0.7,1.1] :35702 保留）
- **手持光**：148 水蜡烛(0,0.5,1)无 wet 门/5322 (0.2,0.3,0.32) !wet/4952 (1,0.7,0.8)×1.3 无 wet 门（Player.cs:49179/:49274/:49430，num=1 恒定）；三动态火把=demonTorchColor/discoColor/shimmerTorchColor 精确公式（曾静态近似/六色跳变）
- **tile 光源 58 条静态 + 33 条动态**：ApplyTileLight(:344-3151) brace-aware 解析器对账（tools 脚本在 $CLAUDE_JOB_DIR/tmp）；静态补 tiles.ts def.light（火族 336-344/月亮碎片 415-418/月亮砖 500-503/仙女罐 568-570/水母块 739/gemspark 262-268 通道式/苔砖族 687-691 等）；动态进 specialTileLight+ctx（坐标/局部随机/冷却/昼夜）：**33/93/100-173/34 四族样式表（206 条 Python 生成器转录，动态样式 paint/demon/hsl/shimmer 分发）**、171 吊灯原点回查 frameY&0x3C00、26/31/695/696 祭坛双色态、83 药草双帧、125/149/129/184/215/405、316-318 水母笼（FlickerClock 新态机 jellyfishCageMode 3×25）、658/660 微光烛/火把、659/667/708 GetShimmerBaseColor、663/356 日月晷冷却门、719 传送塔 14 色轮、717/718 云族、620 hsl 彩虹、597 村庄塔×0.75
- **FlickerClock 扩展**：timeForVisualEffects(:17110 +1/帧钳 216000)、globalTimeWrappedHourly getter(真实秒%3600)、hslToRgb(Main.cs:47266)、shimmerBaseColor(LiquidRenderer:803+GetShimmerWave:761)、jellyfishCageMode 态机(Main.cs:16470-16530)
- **掉落物点光全分支**（WorldItem.cs:1286-1505 1:1）：5043/116/3191/520-575/58/184/522/1332 jitter 族、四柱魂 3456-3459 ×essScale（未跟踪取 1 近似登记）、彩凝胶 1970-1976、凝胶块 2677-2689、2701、**火把族按 placeStyle 走 TorchColor（曾全部默认火把色）**含 demon/disco/shimmer 动态档与 !wet||WaterTorches 门
- **npcs 桶接入实体光扫**（曾结构性断链）
- **tiles.ts 双注坑**：B 批补静态时 13 条 def 已有 light 生成重复 key（TS1117）——dedup 保留原值（逐条核对与原版一致）；patch 脚本换行注释后残留双逗号=对象 elision TS1136

## 进行中
- ✅ **NPC 点光 80 站点全量处置**（子代理实装+本会话复核）：29 处新实装（caster 三档/灯笼鱼/火轮/幽灵族/飞武三色/地牢骷髅四族/火星行者/沙鬼三色/彩虹史莱姆 disco/金史莱姆/微光史莱姆 TorchColor23/岩浆史莱姆(1,0.3,0.1)——审计曾误标"onFire 光"/无头骑士/饿魂II/139 探针门=非实心/光皇蝴蝶 hsl/地狱蝴蝶/仙灵三色×0.7/发光蘑菇族 254-261+634/635/不死矿工/TrailingMode4 三怪/**减益发光 7 站点**（onFire 系(1,0.3,0.1)/betsys(0.6,0.1,0.9)/frostburn(0.1,0.6,1)，与 type 光逐通道 max 合并）+ Boss（饥饿者/毁灭者 !buried 门/光女 Opacity/史后(1,0.7,0.9)）+ TownNPC/Critter（松露/电子人/金史后0.35×TorchColor23/神秘青蛙三角波））；4 处修正（哀木/常世吼漏 lightRGBAt Bottom−30、特斯拉塔 Y−10、夜爬虫 essScale 三角波 0.7↔1.0+测试上界同步）；跳过清单=SlimeCanContainItems 变体系统未移植/Pal 联动/微光上升/magic aura/电子人音乐盒/松露变体档
- **家族 case ctx 守卫放开**（33/93/100/173/34/42 去 `|| !ctx`；candleFamilyLight ctx 参数可选，shimmer 档无 ctx 退 default）——a-batch4 4 参调用形态回归（曾炸 3 例灯笼 demonTorch 测试）

## 遗留登记
- ~~essScale 未跟踪~~✅ FlickerClock.essScale 三角波 0.7-1.0（Main.cs:602/61705-61713）已接四柱魂掉落光；夜爬虫用 performance.now 折帧近似（等价）
- 彩玻墙染色应乘区（ApplySurfaceLight:3190-3242 原版 num=num4 系乘区）——现 max 近似
- def.light 逐格播撒 vs 原版帧级门控差异（大族已由 specialTileLight 动态分支覆盖）
- 竿 5139-5146 itemfunc 缺 shoot 数据
- 985/502 等实体自报光 + projId 标量双通道共存——跳过门兜底，新实体自报光时勿忘
- world-final-hash 金标 11:29 后世界数组再变（并行会话 fragment sweep 在途）+ world-invariants 'pot' 残片复现——并行会话领地，勿动

**教训**：①审计代理"原版没有"结论不可靠——814 血弹光实为 819、:351 泰拉刃绿光曾误判造假、tile 209 曾误判写反，三案全靠逐行读源码翻案；②绝对通道与乘区混编必须逐 case 抄——251 的 (Disco+1)/2 再乘 light、44 的 B=1 绝对纯乘区表表达不了；③批量生成器转录优于手抄（206 条样式表手抄漏 11 条，脚本比对抓回）

相关：[[vanilla-lighting-port]]（引擎本体基线）

## 追加（2026-08-17）：光芒药水双源并存修复
- 光照引擎 ApplyPerFrameLights = **逐通道 Vector3.Max**（LightingEngine.cs:205-220 原版；本仓 TileLightScanner:744 同）——多光源不叠加、无优先级，同格各通道取大。
- 光芒 buff11=(0.8,0.95,1.0) 中心格【无条件】发射（Player.cs:9687-9690）；手持火把在手位格（:49093-49107 dir-1→X-12/else X+6,Y-14）。曾有两错：`!heldRGB&&` 优先链吞掉药水光 + 亮度误值 1.3。现 LightingEngine.buffLights 槽与 heldLight 并存。
- 教训：**buff 类点光（光芒/狱火）永不与手持物互斥**——UpdateBuffs 链独立于 ItemCheck 链；动态点光一律走 perFrame max，不做单槽优先。

## 追加二（2026-08-17 review 追修）：手位公式与 5643
- 手持光位完整链 = idle itemLocation（:50387 X=cx−2·dir,Y=cy−frameH/2；帧高火把16/蜡烛20/3002=18/4952=40）+ case 偏移（火把族±12【对称】/其余−16/+6，右向+6 是尘位勿混）−14。
- 5643 荧光棒=Disco 连续色（discoColor() 同源）；4776 有 FloodFillTile 4.5 穿墙未接（登记）。
- 探针 _shinelight-probe.mjs：inWater 字段每帧被碰撞重算，湿门测试须注真水；buff 用 apply/set 非 add。
