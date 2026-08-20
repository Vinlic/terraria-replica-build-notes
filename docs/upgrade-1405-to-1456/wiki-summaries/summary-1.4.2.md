# 泰拉瑞亚 1.4.2 全系版本更新日志结构化摘要(1.4.2 / 1.4.2.1 / 1.4.2.2 / 1.4.2.3)

> 来源:中文 wiki(MediaWiki API,parse.wikitext)。版本主题:1.4.2 为 Steam 创意工坊支持,1.4.2.1/1.4.2.2 为修补程序,1.4.2.3 为十周年更新(新增 Celebrationmk10 秘密种子)。

---

## 1.4.2(2021-03-29,补丁名:Steam 创意工坊支持)

### 【新增内容】
- 将 Steam 创意工坊整合进游戏,允许玩家下载和分享世界文件与资源包 (→ Terraria.Social, Terraria.Social.Steam)
- 原"纹理包"功能拓展为"资源包",新增游戏文本替换(语言包)与音乐替换功能 (→ Terraria.Social, Terraria.Localization, Main.cs)
- 为研究菜单和图鉴菜单加入可清空当前搜索内容的按钮 (→ Terraria.GameContent.UI)
- 加入用于更改角色和世界名称的选项 (→ Terraria.GameContent.UI, Terraria.IO)

### 【机制系统改动】
- 敌怪旗(Enemy Banners)现在也对敌怪弹幕(enemy projectiles)提供减伤保护——此前只对接触伤害生效 (→ Player.cs, Terraria.ID.ItemID.cs)

### 【Bug修复-仅列影响玩法逻辑的】
- 部分掉落的物块会穿过平台而不是落在其上方 (→ Item.cs)
- 纸飞机(Paper Airplanes)并不以图鉴所述的数量掉落 (→ Terraria.GameContent.ItemDropRules)
- 下落的金币无法落在其它金币上方(金币堆叠) (→ Item.cs)
- 活板门(Trap Doors)在多人游戏中不同步,导致敌怪能穿过它们 (→ Terraria.NetMessage, Terraria.IO)
- 麦酒投掷器(Ale Tosser)无法正确获得冰霜盔甲的霜燃效果 (→ Item.cs, Projectile.cs)
- 部分海洋敌怪会在玩家放置的墙前生成 (→ NPC.cs)
- 闪烁怪(Twinkle Popper)召唤的 Twinkles 不再捡起金币——它们爆炸时会永久删除携带的金币 (→ NPC.cs)
- 化石镐(Fossil Pickaxe)、树木球(Tree Globe)和世界球(World Globe)物品会穿过方块一直下落 (→ Item.cs)
- 血肉墙会下降到世界范围以外 (→ NPC.cs)
- 共振权杖(Resonance Scepter)和生命汲取(Life Drain)只能向右击退敌怪 (→ Projectile.cs)
- 高速子弹有时会命中大型目标两次(多体节敌怪仍可被多次命中,不受影响) (→ Projectile.cs)
- 鳉鱼(Pupfish)有时会生成在海洋 (→ NPC.cs, Terraria.GameContent.Biomes)
- 火花魔棒(Wand of Sparking)的弹幕错误地应用近战伤害加成而非魔法 (→ Projectile.cs, Item.cs)
- 已死亡的玩家或硬核玩家鬼魂会触发玩家逻辑感应器 (→ Main.cs, Terraria.GameContent)
- 星炮弹幕无法造成暴击,且不总是正确获得玩家装备的属性加成 (→ Projectile.cs, Item.cs)
- 星炮弹幕无法穿过平台 (→ Projectile.cs)
- 修复了一些物品复制漏洞 (→ Item.cs, Terraria.NetMessage)
- 尖刺(Spikes)在特定高度下的某些角度无法伤害玩家 (→ Player.cs)
- 世界球(World Globe)会跳过部分森林生物群落背景 (→ Projectile.cs, Main.cs)
- 蛙腿(Frog Leg)与其升级不互相叠加,但两栖靴(Amphibian Boots)的效果会和其它蛙腿变体叠加 (→ Player.cs)
- 世界种子在一次游玩过程中创建太多世界后,不总会生成同样的世界(随机种子复现性) (→ WorldGen.cs, Terraria.Utilities)
- 大理石块(Smooth Marble Blocks)会与回声块(Echo Blocks)融合渲染 (→ Terraria.GameContent.Drawing.TileDrawing.cs)
- 烟雾块(Smoke Blocks)在多次游玩间不保持锤击后状态 (→ WorldGen.cs)
- 苔藓蔓延时在服务器中不总使用正确帧 (→ WorldGen.cs)
- 流星无法生成时会导致游戏崩溃的罕见问题 (→ WorldGen.cs)
- 纯崩溃/表现类:滚动仙人掌在祭坛上生成导致崩溃、"Wasp Gun 拥有一条只写自身名字的 tooltip"、联合军士盾意外显示饰品染料、穿道服(Gi)坐下摆出跳跃姿势等一并归并。

---

## 1.4.2.1(2021-03-31,修补程序)

### 【音频】
- 修复用 MP3 文件替换音乐时音乐不循环的问题 (→ Terraria.Social, 音频引擎)
- 修复替换后的音乐比原版音乐更响的问题 (→ Terraria.Social, 音频引擎)

### 【机制系统改动】
- 修正"决定性一刻"(Striking Moment)buff 文本:实际效果为伤害增加 400%(即增至 500%),而非文本所写的增加 500%——本次只改文字,数值未动 (→ Terraria.Lang, Terraria.ID.BuffID.cs)
- 气泡块(Bubble)现在可作为玩家出生点房屋的墙壁(修复其不能作为房屋墙壁的问题) (→ WorldGen.cs)
- 门、活板门和高门开启时不再使房屋判定无效 (→ WorldGen.cs)
- 夜明矿与夜明砖被挖掘时发出矿石/金属声而非泥土声 (→ Terraria.ID.TileID.cs, 音频资源表)

### 【UI与界面】
- 世界生成菜单说明更新:现在可以重命名世界(对应 1.4.2 的更改) (→ Terraria.GameContent.UI)
- 创意工坊发布菜单中"其他"标签不再以 Debug 模式文本显示 (→ Terraria.Social)
- 修复描述沙漠与雪原生物群落生成位置的一条信息中的文字错误 (→ Terraria.Lang)
- 修复若干语法与大小写小问题 (→ Terraria.Lang)

### 【其他/可忽略项】
- Mac(可能含 Linux)上替换音乐不生效、标题信息(Title Messages)无法被资源包更改、资源包 XNB 配置文件加载问题——均为资源包/创意工坊基础设施 (→ Terraria.Social)

---

## 1.4.2.2(2021-04-21,修补程序)

### 【新增内容】
- 在表情指令(Emote Commands)菜单列表中加入 /ale 表情 (→ Terraria.GameContent.UI, Terraria.Chat)

### 【NPC与Boss与AI】
- "弹幕型 NPC"(可被玩家摧毁的敌怪弹幕)现在也受对应敌怪旗的影响 (→ NPC.cs, Player.cs)
- 咬齿炸弹(Chattering Teeth Bomb)和暗影焰幻影(Shadowflame Apparition)现在受其创建者的敌怪旗影响(分别对应小丑 Clown 与哥布林召唤师 Goblin Summoner) (→ NPC.cs, Player.cs, Terraria.ID.ProjectileID.cs)

### 【物品与数值平衡】
- 飞镖手枪(Dart Pistol)和飞镖步枪(Dart Rifle):1.4.1 中对其做出的平衡调整此前未实际应用,本次补上(wiki 此处内联了 1.4.1 的飞镖枪平衡条目,数值以 1.4.1 日志为准) (→ Item.cs)
- 修正 Pillagin Me Pixels 物品英文名中缺失的撇号 (→ Terraria.Lang, Terraria.ID.ItemID.cs)

### 【机制系统改动】
- 所有城镇 NPC 的名字现在可以用资源包更改 (→ Terraria.Localization, Terraria.Lang)
- 修复非旅途模式玩家有时可被设置为永久激活旅途模式能力的问题 (→ Player.cs)
- 修复多人模式下敌怪治疗效果的同步问题 (→ NPC.cs, Terraria.NetMessage)
- 修复弹幕击退在多人模式下不一致的问题 (→ Projectile.cs, Terraria.NetMessage)

### 【UI与界面】
- 修复非英语语言下图鉴完成度计量条达到 100% 时多出逗号的问题 (→ Terraria.GameContent.UI, Terraria.Lang)

### 【渲染与视觉特效】
- 修复 Lazure's Barrier Platform 在重力反转状态下会显示在玩家头部的问题 (→ Projectile.cs, Terraria.GameContent.Drawing)

### 【Bug修复-仅列影响玩法逻辑的】
- 修复重命名或导入世界时会把世界时间变为主菜单时间的问题 (→ Terraria.IO, WorldGen.cs)
- 修复部分 MP3 文件播放速度显著偏低的问题 (→ 音频引擎)
- 修复启动游戏时没有有效/检测到音频设备导致崩溃的问题 (→ Main.cs)
- 修复开场音乐等部分音乐被资源包替换后不循环的问题 (→ Terraria.Social, 音频引擎)

### 【其他/可忽略项】
- 创意工坊/平台类:config.json 中赛睿 RGB 设置误用罗技设置、Linux GOG 专用服务器启动异常、资源包内语言/音乐/材质优先级不一致(顶部包应最高优先级) (→ Terraria.Social, Terraria.Program)

---

## 1.4.2.3(2021-05-16,补丁名:10 周年更新)

### 【新增内容】
- 加入 Celebrationmk10 秘密世界种子(Special world seeds,十周年庆典世界) (→ WorldGen.cs, Terraria.GameContent.Biomes, Terraria.IO)

### 【物品与数值平衡】
- 冰霜盔甲(Frost armor)套装奖励减益的伤害由 20 修正为 25 DPS (→ Item.cs, Player.cs)

### 【Bug修复-仅列影响玩法逻辑的】
- 修复除普通/花朵藤蔓外,其它所有种类藤蔓生长时不传递油漆的问题 (→ WorldGen.cs, Terraria.GameContent.Drawing.TileDrawing.cs)
- 修复尖刺史莱姆(Spiked Slime)能捡起金币并随金币一起消失的问题 (→ NPC.cs)
- 修复史莱姆皇后宝袋缺失 tooltip 的问题 (→ Terraria.Lang, Terraria.GameContent.ItemDropRules)
- 纯崩溃/渲染类:基于 FNA 的 Vulkan/Metal 渲染崩溃问题一并归并;另修复"一个小疏漏"。

---

## 【本版本改动规模评估】

**规模估算**:1.4.2 全系共触及约 10 个独立系统,其中大头是"平台基础设施"而非"玩法"——Steam 创意工坊、资源包(纹理/语言/音乐替换)、音频播放器(MP3 解码、循环、音量、变速)占了全部条目的一半以上,外加约 30 条散布在弹幕、敌怪 AI、掉落、房屋判定、种子复现、渲染上的单项修复。

**对网页复刻项目(无 Steam)可以忽略的部分**:
- 全部 Steam 创意工坊条目:创意工坊整合、发布菜单、世界/资源分享(Terraria.Social 整个命名空间)
- 资源包体系:纹理包→资源包扩展、语言包、音乐替换、XNB 配置、包优先级、标题信息/城镇 NPC 名字可被资源包改写(除非项目自建 mod 管线,否则不适用)
- 音频播放器类修复:MP3 循环/音量/变速、无音频设备崩溃、开场音乐循环——这些是 XNA/MP3 解码器特有问题,Web Audio 天然不同
- 平台特定项:Linux GOG 专用服务器、赛锐/罗技 RGB 设置、Vulkan/Metal FNA 渲染崩溃

**必须跟进的核心改动(直接影响玩法逻辑/数值)**:
1. **敌怪旗减伤覆盖敌怪弹幕**(1.4.2)+ **弹幕型 NPC 与召唤物受旗影响**(1.4.2.2)——banner 计算逻辑要扩展到 projectile 层,复刻的 Player.cs 旗子逻辑必须照做。
2. **Celebrationmk10 秘密种子**(1.4.2.3)——新增一条完整的世界生成分支,若项目计划支持特殊种子则必须移植;至少要在 WorldGen 里留出 special seed 钩子。
3. **冰霜盔甲套装减益 20→25 DPS**(1.4.2.3)与 **飞镖手枪/步枪的 1.4.1 平衡实际生效**(1.4.2.2)——两处数值修正,Item.cs/Player.cs 直接改动,工作量极小但影响平衡。
4. **房屋判定修正**(1.4.2.1):门/活板门/高门开启不再使房屋无效、气泡块可作出生房屋墙——WorldGen 房屋检查逻辑的两处行为变更。
5. **弹幕/物品行为修复群**(1.4.2):星炮(暴击+平台穿透+装备加成)、高速子弹双倍命中、共振权杖/生命汲取击退方向、火花魔棒伤害类型、活板门多人同步、弹幕击退多人同步、敌怪生成位置(墙前/海洋)等——散点修复,建议在移植对应武器/弹幕时逐条对照,不必单独立项。

**总体结论**:1.4.2 是一个"平台更新 + 小修小补"版本,除 banner 机制扩展与 Celebrationmk10 种子外没有新系统、没有新 Boss/物品,复刻项目可用约 1-2 个小迭代完成全部必须跟进项。
