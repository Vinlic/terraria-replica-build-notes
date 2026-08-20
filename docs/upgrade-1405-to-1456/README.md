# 原版 1.4.0.5 → 1.4.5.6 版本差异总纲(供复刻升级跟进)

> 建立日期:2026-08-09。
> 目的:本项目当前以 **1.4.0.5**(`Terarria1405` 反编译)为移植基准,本文档记录 1.4.1 ~ 1.4.5.6 五个大版本的全部差异,用于后续把复刻目标升级到 **1.4.5.6**(`Terarria1456` 反编译)。
> 原则:**所有数值/逻辑以 `Terarria1456` 源码为最终权威**,wiki 更新日志只做导航和"为什么改"的背景——因为多个版本存在后续回退(见 §3),只看中间版本日志会移植错。

## 目录内容

| 文件 | 内容 |
|---|---|
| `wiki-summaries/summary-1.4.1.md` ~ `summary-1.4.5.md` | 五个大版本(含全部 27 个子版本)更新日志的结构化解析,每条标注影响的源码文件 |
| `structdiff/structdiff.md` + `.json` | 两版反编译源码的**成员级**结构对比:564 个新文件清单 + 386 个改动文件的类型/方法/字段增删明细 |
| `structdiff/structdiff.py` | 生成上述对比的脚本(可重跑:`python3 structdiff.py`) |
| `raw-wiki/*.json` | wiki MediaWiki API 原始 wikitext 存档(33 页,溯源用) |

> 补充权威源:本地 Steam 自带 `changelog.txt`(官方英文全量日志,含 1.4.0.1~1.4.5.6 全部版本)——版本清单已用它反向核对,wiki 覆盖除 1.4.4.8.1 外无遗漏(该版已补入 summary-1.4.4.md);摘要内容也已用官方日志对三大版本(1.4.1/1.4.4/1.4.5)做完整性校验。

## 1. 版本时间线与定位

| 版本 | 主题 | 一句话定性 |
|---|---|---|
| **1.4.1**(+.1/.2) | Rounding Out the Journey | **巨型平衡补丁**:免伤帧/穿透惩罚体系重构、数百项数值调整、敌人 debuff 免疫重排、公主 NPC;1.4.1.2 对过量强化做官方回调 |
| **1.4.2**(+.1~.3) | Steam 创意工坊 | 平台更新,**可忽略大半**;玩法侧只有敌怪旗扩到弹幕、Celebrationmk10 秘密种子、房屋判定修正 |
| **1.4.3**(+.1~.6) | 以眼还眼(饥荒联动) | 新种子 The Constant + 新 Boss 鹿角怪 + 成套联动物品;1.4.3.2 联动物品数值大改、1.4.3.3 含全局规则修正;.4~.6 是平台层可忽略 |
| **1.4.4**(+.1~.9) | Labor of Love 爱的劳动 | **最大机制版本**:微光 Shimmer/Aether 生物群落、Town Slimes、无敌帧再重构、buff 上限 22→44、装备配装 Loadouts、地牢生成整体重做、4 个新特殊种子;数值以 1.4.4.9 为准 |
| **1.4.5**(+.1~.6) | Bigger and Boulder | **最新大版本**:650+ 新物品、世界种子可组合 + Skyblock 种子、全武器数值精修、召唤武器零耗蓝、雷击/传送带/电信号新机制层、合成与旗帜 UI 大重做;**存在回退性改动,必须以 1.4.5.6 最终态为准** |

## 2. 源码层面客观差异(structdiff 实测)

两版反编译源码全量成员级对比(`structdiff/structdiff.md` 有完整明细):

- **文件量**:983 → 1499 个 `.cs`;1456 新增 564 个文件;47 个文件被移除/合并;386 个共同文件有成员增删。
- **ID 表扩容**(字段级增量,含新 const ID 段 + 新静态数据表,注意混排):
  - `ItemID.cs` +1164(1.4.4 加 ~500 物品、1.4.5 再加 650+,含大量矿车/宠物/联动变体)
  - `ProjectileID.cs` +181(9 种新鞭、Shimmer 系、TerraBlade2、Palworld/Dead Cells 联动弹幕等)
  - `NPCID.cs` +109(Deerclops、TorchGod、OwlMimic、8 种 Town Slime、ShimmerSlime、Palworld 联动 NPC 等)
  - `TileID.cs` +191(Shimmer 系、各色 Ancient Brick、彩虹/发光苔藓、Boulder 全家族、Echo 系、联动装饰)
  - `BuffID.cs` +126(Hunger 三态、Whip 系 debuff、30+ 种矿车变体 buff、RollerSkates/Velociraptor/Wolf/Rat/Pixie 坐骑 buff、联动宠物 buff)
  - 另:`GoreID` +177、`ArmorIDs` +165、`SoundID` +115、`GlowMaskID` +78、`WallID` +65
- **全新子系统**(1456 新增文件的主要聚集地):
  - `Terraria.GameContent.Generation.Dungeon.*` **104 个文件**——1.4.4 地牢生成整体重做(整个命名空间 1.4.0.5 不存在)。**本项目移植的 105-pass 管线中地牢相关 pass 需按 1456 重写**。
  - `Terraria.GameContent.LeashedEntities.*` 21 个文件——1.4.4 风筝(Kite)与栓绳小动物系统。
  - `Terraria.GameContent/UI` +56 个文件——1.4.5 UI 大重做(合成窗口/旗帜菜单/种子选择等)。
  - `Terraria.GameContent/Personalities` +16——NPC 个性/快乐度持续扩容。
  - `Terraria.GameContent/ShimmerTransforms.cs`——微光转化表(1.4.4)。
  - `Terraria.DataStructures` +86、`Graphics` +24、`WorldBuilding` +19——配套数据结构与生成动作。
- **可整体忽略**:`Terraria.Social.*` +18(Steam 创意工坊)、平台/RGB/资源包基础设施。

## 3. 关键警示:后续版本回退(移植时必须取最终态)

- **1.4.1.2**:对 1.4.1 的过量强化做官方回调(快乐度参数两连改等)→ 取 1.4.1.2 后状态
- **1.4.2.2**:1.4.1 的飞镖枪平衡此时才真正生效
- **1.4.3.2**:联动物品初版数值全部作废(Bat Bat 18→31、Ham Bat 50→57 等)
- **1.4.4.8/.9**:Undertaker 回退、Night's Edge 再削、90 种武器尺寸乘数归一 → 取 1.4.4.9 后状态
- **1.4.5.4/.5/.6**:鞭 hitbox 恢复 1.4.4 一致、隐身恢复 1.4.4.9、放置范围恢复 1.4.4.9 → **取 1.4.5.6**
- 结论:**不要按版本日志逐条打补丁式移植,直接以 `Terarria1456` 全量提取目标数据**(项目已有同款管线:`tools/build-asset-table.mjs` 等可改造为从 1456 的 `SetDefaults`/静态表直接生成数据)。

## 4. 各版本核心改动索引(详情见 wiki-summaries/)

### 1.4.1 —— 平衡与免伤帧体系重构
- 免伤帧/穿透惩罚重构:大量弹药/仆从改"每穿透一敌下次伤害 -X%",独立/局部免伤计时器(→ Projectile.cs、NPC.cs、Player.cs)——**召唤与穿透武器手感的地底层**
- 敌人 debuff 免疫体系系统性重排;Venom→Acid Venom 重命名;Ichor 减防 20→15
- 物品数值全量刷新(Terra Blade 95→115、矿装降价、Mana Crystal 3→5 星等)→ Item.cs、Recipe.cs
- 公主 NPC(Flinx 系早期召唤装)→ NPC.cs、Personalities
- Vanity 渲染分层(背部四类同时显示等)→ Player.cs 绘制管线

### 1.4.2 —— 平台更新(玩法侧很薄)
- 敌怪旗减伤扩展到敌怪弹幕、弹幕型 NPC 受旗影响 → Player.cs、NPC.cs
- Celebrationmk10 秘密种子 → WorldGen.cs、Utilities
- 房屋判定:开门不失效、气泡块可作墙 → WorldGen.cs
- 其余(创意工坊/资源包/MP3)对 web 复刻可忽略

### 1.4.3 —— 饥荒联动
- The Constant 特殊种子:黑暗伤害、雨水灭火把、饥饿机制、饥荒光照 → Utilities、Player.cs、Lighting
- 新 Boss 鹿角怪 Deerclops(掉落/AI/后续三轮修复)→ NPC.cs、ItemDropRules
- 联动物品套装(Bernie/Chester/Glommer 宠物、Ham Bat、Abigail's Flower 等)
- 1.4.3.3 全局规则(不做联动也要):仆从不伤小动物、黑曜石镐力门槛、NPC 快乐度 0.85→0.9

### 1.4.4 —— Labor of Love(机制最大版本)
- **微光 Shimmer**:新液体 + Aether 生物群落 + ShimmerTransforms(物品 decraft、生物转化、Town Slime 变形)→ 新文件 GameContent/ShimmerTransforms.cs、Liquid 逻辑、WorldGen
- **无敌帧再重构**:全阔剑改局部无敌帧,数十件武器改独立/局部帧 → Item/Projectile/NPC/Player
- buff 框架:玩家上限 22→44、敌怪 debuff 5→20、死亡无敌 1→3s、火系 On Fire!→Hellfire
- 装备配装 Loadouts(F1-F3)、Void Bag 重做、涂层 Coating、堆叠 9999
- 鞭与召唤标记伤害体系(标记伤害、哨兵持续 10 分钟)
- 掉落重构:EoW/BoC 比例制掉落、宝箱物品池 12→10
- 地牢生成整体重做(Dungeon 命名空间 104 文件)+ 4 新特殊种子(Remix/No Traps/Everything/Zenith?)
- 数值数百条:近战全系加强、Terra Blade 115→85、Golem/Duke 生命调整

### 1.4.5 —— Bigger and Boulder(最新)
- 650+ 新物品:9 新鞭、22 套家具、Dead Cells + Palworld 两套联动(5 武器 + 5 宠物)、4 变身坐骑、2 新晶塔
- **世界种子系统重构**:特殊种子可组合、Skyblock 种子、新种子选择菜单 → WorldGen 入口逻辑框架级改动
- 全武器数值精修(召唤武器零耗蓝 + 召唤词缀)
- 新机制层:雷击系统(1.4.5.3 削弱至 80/160/240)、箱子/提取机接电线、传送带向上运输、火炮发射火把
- UI 大改:合成窗口重做(搜索/过滤/附近箱子)、旗帜菜单、堆叠 9999、村民头像
- AI:海盗入侵削弱、Boss 专家倍率 100%→85%、Boss 战可开晶塔、Shimmer 对 Boss 无敌失效

## 5. 对本项目的升级路线建议(按优先级)

> 现状参考记忆:105-pass 世界生成(1405 基准)、液体系统、561 种 NPC 数据、vui UI(M2 进行中)均已按 1.4.0.5 移植。

**P0 —— 框架级(影响后续所有移植的正确性)**
1. **数据源切换**:物品/NPC/弹幕/buff/方块数值表从 1405 切到 1456 全量重提取(含 1.4.5 新增的 ID 段与静态数据表),一次到位,不做逐版本补丁
2. **特殊种子框架**:WorldGen 入口支持 special seeds(1.4.3 The Constant、1.4.2 Celebrationmk10、1.4.4 Remix/No Traps/Everything、1.4.5 可组合 + Skyblock)——即使暂不实现内容,也要留钩子
3. **地牢生成重写**:105-pass 中地牢 pass 按 1456 的 Dungeon 命名空间重写(结构完全不同)
4. **免伤帧/穿透惩罚体系**:按 1456 的 Projectile/NPC/Player 实现最终态(1.4.1 与 1.4.4 两次重构的叠加结果)

**P1 —— 核心玩法机制**
5. 微光 Shimmer 液体 + Aether 生物群落 + 转化表(液体系统已移植,增量可控)
6. buff/debuff 框架扩容(上限 44、敌 debuff 20、whip 标记体系)
7. Town Slimes、公主、Deerclops、1.4.4/1.4.5 新敌怪与 Boss(AI 家族分批管线直接吃 1456 数据)
8. 装备配装 Loadouts、旗帜/banner 机制扩展(含弹幕)

**P2 —— 内容填充**
9. 1.4.4/1.4.5 新物品/武器/家具(数据驱动,批量)
10. 风筝/栓绳系统、雷击/传送带/电信号、Monolith 新成员
11. UI:合成窗口重做、旗帜菜单、种子选择菜单(vui 管线对齐 1456)

**可忽略**:Steam 创意工坊、资源包、RGB 设备、Linux/Deck 平台层、FNA 渲染崩溃、MP3 解码(Web Audio 天然不同)

## 6. 已知的数据噪音提示

- `structdiff` 的"字段新增"混排了**新 const ID** 与**新静态数据表**(如 TileID 里 `ShimmerImmunity` 这类是 Set/数组);逐条用时按名字语义区分
- 1405(dotPeek)与 1456(ilspycmd)来自不同反编译器,方法体风格不可逐行 diff;`structdiff` 只比成员签名级,大文件的"removed"侧仍有少量重命名噪音,以"added"侧为准
- 1405 中 `NPC.AI()`/`HitEffect()`/`Recipe` 等是空壳(已有 `NPC.145.cs` 补丁),对比时这些文件按"全量以 1456 为准"处理
