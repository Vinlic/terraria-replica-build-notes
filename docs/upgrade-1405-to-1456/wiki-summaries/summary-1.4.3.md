# 泰拉瑞亚 1.4.3（含 1.4.3.1 ~ 1.4.3.6）更新日志结构化摘要

> 原始来源：中文 wiki 更新日志（本地 MediaWiki JSON）。1.4.3 主版本代号「以眼还眼」（An Eye For An Eye），2021-11-18 发布，是泰拉瑞亚 × 饥荒联机版（Don't Starve Together）联动更新。1.4.3.1/.2 为联动内容热修复，1.4.3.3~.6 为 2022 年 2-3 月的 Steam Deck 优化及收尾修复。
>
> 标注约定：行尾 `(→ 文件)` 表示该条大概率影响的反编译源码文件。

---

## 1.4.3（以眼还眼，饥荒联动）— 2021-11-18

### 【新增内容】
- 新增受饥荒启发的特殊世界种子 **The Constant**（永夜/饥荒世界），并带来一整套专属规则（→ Terraria.Utilities, Terraria/Main.cs, Terraria/Player.cs）：
  - 受饥荒启发的着色器和光照（→ Terraria/GameContent/Drawing/TileDrawing.cs, Terraria/Main.cs）。
  - 完全黑暗现在会直接损害玩家生命值（黑暗伤害）（→ Terraria/Player.cs, Terraria/Main.cs）。
  - 露天的火把和篝火不再可靠——雨水可以熄灭它们（→ Terraria/WorldGen.cs, Terraria/GameContent/Drawing/TileDrawing.cs, Terraria/Main.cs）。
  - **饥饿机制**：玩家需要进食，否则会持续饥饿并最终饿死（→ Terraria/Player.cs, Terraria.ID/BuffID.cs）。
  - 部分受饥荒启发的世界生成：如地表**大理石洞**（Marble Cave 出现在地表）和地上**蜘蛛生物群落**（Spider 群落暴露在地表）（→ Terraria/WorldGen.cs, Terraria/GameContent/Biomes, Terraria.ID/TileID.cs）。
  - 大幅提高饥荒相关物品的掉落率和可用性（→ Terraria/GameContent/ItemDropRules）。
- 新增 Boss **鹿角怪（Deerclops）**，来自饥荒世界的困难模式前中后期 Boss（→ Terraria/NPC.cs, Terraria.ID/NPCID.cs, Terraria/GameContent/ItemDropRules）。
- 新增鹿角怪 Boss 主题曲变奏，由科雷娱乐（Klei）提供（→ 音频资源）。
- 天空背景云中现在可以出现包含饥荒人物的罕见云（→ Terraria/GameContent/Drawing/TileDrawing.cs, Terraria/Main.cs）。
- 新增若干饥荒主题表情（emotes）（→ Terraria/Main.cs）。
- 世界选择菜单中，特殊种子世界拥有独特图标以便区分（→ UI, Terraria/Main.cs）。
- 主菜单新增泰拉瑞亚相关网站的链接（→ UI, Terraria/Main.cs）。
- 新增配置项 `SmartCursorHoldCanReleaseMidUse`：设为 true 后，「长按」模式的智能光标会在松开按钮时立即关闭，即使玩家正在挖矿（→ Terraria/Player.cs, 配置读写）。

### 【物品与数值平衡】
- 新增多个饥荒宇宙**宠物**：伯尼（Bernie's Button）、猪人（Monster Meat）、切斯特（Eye Bone 召唤 Chester）、小鹿角怪（Deerclops Eyeball）（→ Terraria.ID/ItemID.cs, Terraria/Item.cs, Terraria/Projectile.cs）。
- 新增一系列饥荒武器与装备，代表性物品：**火腿棒（Ham Bat）、阿比盖尔的花（Abigail's Flower）、蝙蝠棒（Bat Bat）、触手长钉（Tentacle Spike）**，另有 Pew-matic Horn、Weather Pain、Houndius Shootius、Lucy the Axe 等（→ Terraria/Item.cs, Terraria.ID/ItemID.cs, Terraria/Projectile.cs）。
- 新增虚荣套装：威尔逊（Gentleman's set）、薇洛（Firestarter's set）（→ Terraria/Item.cs）。
- 新增时装帽子与饰品：花冠（Garland）、荧光项链（Magiluminescence）（→ Terraria/Item.cs）。
- 新增两种食物：蛙腿三明治（Froggle Bunwich）、怪物千层面（Monster Lasagna）（→ Terraria/Item.cs, Terraria.ID/BuffID.cs）。
- 鹿角怪掉落全套标准 Boss 相关物品（→ Terraria/GameContent/ItemDropRules, Terraria.ID/ItemID.cs）。
- 新增 4 幅饥荒主题画作（→ Terraria.ID/ItemID.cs, Terraria/Item.cs）。

### 【NPC与Boss与AI】
- 鹿角怪（Deerclops）加入，为困难模式前中后期 Boss（详见新增内容）（→ Terraria/NPC.cs, Terraria.ID/NPCID.cs）。
- 拜月教邪教徒（Lunatic Cultist）对部分自动寻的射弹具有伤害抗性，该列表存在不准确与过时条目，本版进行了更新、添加与删减（→ Terraria/NPC.cs, Terraria.ID/ProjectileID.cs）。

### 【世界生成】
- The Constant 种子的饥荒风格世界生成（地表大理石、地上蜘蛛群落等）（→ Terraria/WorldGen.cs, Terraria/GameContent/Biomes）。
- 修复小滩蜂蜜微型生物群落无法在丛林中生成的问题（→ Terraria/WorldGen.cs, Terraria/GameContent/Biomes）。
- 修复一个罕见的世界生成卡死：尝试放置地狱熔炉（Hellforge）时游戏卡住（→ Terraria/WorldGen.cs）。

### 【渲染与视觉特效】
- The Constant 专属饥荒风格着色器与光照（→ Terraria/GameContent/Drawing/TileDrawing.cs, Terraria/Main.cs）。
- 修复反重力情况下星盘（Celestial Starboard）无法正确绘制/制造灰尘的问题（→ Terraria/Player.cs, Terraria/GameContent/Drawing/TileDrawing.cs）。
- 修复某些物品在快捷栏与物品栏中颜色不一致的微小问题（→ Terraria/Item.cs）。
- 修复部分较新篝火缺少智能光标轮廓的问题（→ Terraria/GameContent/Drawing/TileDrawing.cs）。
- 修复白色王朝墙（Dynasty Walls）在地图上显示为不准确青绿色的问题（→ 地图渲染, Terraria/Main.cs）。

### 【UI与界面】
- 主菜单新增泰拉瑞亚相关网站链接；世界选择菜单为特殊种子世界加独特图标；新增多个饥荒表情（→ Terraria/Main.cs, UI 层）。

### 【音频】
- 新增鹿角怪 Boss 主题曲变奏（Klei 提供）（→ 音频资源）。
- 修复公主（Princess）缺少与渔夫（Angler）相同的「离开」音效的问题（→ Terraria.ID/NPCID.cs, 音频触发逻辑）。
- 更改部分较新召唤武器和魔法武器的音效，使其更能代表攻击效果（→ Terraria/Item.cs, 音频触发逻辑）。

### 【机制系统改动】
- The Constant 专属机制：黑暗伤害、雨水熄灭火把/篝火、饥饿系统（→ Terraria/Player.cs, Terraria/Main.cs, Terraria/WorldGen.cs）。
- 修复猩红草墙比腐化草墙传播速度慢的问题（→ Terraria.ID/TileID.cs, Terraria/WorldGen.cs）。
- 修复穿着寒霜盔甲时，巨石（Boulder）和滚动仙人掌（Rolling Cactus）被算作远程物品并能造成冰冻减益（Frostbite）的问题（→ Terraria/Player.cs, Terraria/Projectile.cs）。
- 修复 NPC ID 高于金史莱姆（Golden Slime）的敌人会错误继承金史莱姆额外金币掉落的问题（→ Terraria/NPC.cs, Terraria/GameContent/ItemDropRules）。
- 修复 Smooth Marble Block 不能与土块、灰烬块、冰冻史莱姆块合并的问题（→ Terraria.ID/TileID.cs）。

### 【多人/网络】
- 修复部分哨兵（sentry）仆从的问题：在它们被召唤之后加入游戏的玩家会出现不同步（→ Terraria/Projectile.cs, 网络同步）。

### 【Bug修复（影响玩法逻辑）】
- 修复皮鞭（Leather Whip）部分节被切断的问题（→ Terraria/Projectile.cs）。
- 修复冰霜弓（Ice Bow）被误标为引导武器的问题（→ Terraria/Item.cs）。
- 修复飞刀（Flying Knife）屏幕范围限制不正确的问题（→ Terraria/Projectile.cs）。
- 修复部分仆从（minions）可能消失的罕见错误（→ Terraria/Projectile.cs）。
- 修复部分火箭射弹产生「无声与不那么无声」碰撞的问题（→ Terraria/Projectile.cs）。
- 修复荆棘效果以极快速度击中光之女皇（Empress of Light）时发生的错误（→ Terraria/Projectile.cs, Terraria/NPC.cs）。
- 另有：每次安装更新/补丁时部分设置被重置（全屏分辨率重置问题未修复）——配置持久化问题（→ Terraria/Main.cs, 配置读写）。其余纯崩溃/显示类修复从略。

---

## 1.4.3.1（修补程序）— 2021-11-22

### 【物品与数值平衡】
- **阿比盖尔的花（Abigail's Flower）**：生成率提升 1/3（→ Terraria/Item.cs, Terraria/WorldGen.cs）。
- **阿比盖尔**：每次攻击最多打击 3 名敌人，该上限每拥有 2 个额外仆从槽位提升 1（3 个仆从 = 4，5 个仆从 = 5，以此类推）（→ Terraria/Projectile.cs, Terraria/Player.cs）。
- **蝙蝠棒等武器无本版数值改动。**

### 【NPC与Boss与AI】
- **鹿角怪（Deerclops）**：现在免疫困惑（Confused）减益（→ Terraria/NPC.cs, Terraria.ID/BuffID.cs）。
- **鹿角怪**：接触伤害及其冰冻弹幕现在受温暖药水（Warmth Potion）影响（→ Terraria/NPC.cs, Terraria.ID/BuffID.cs）。
- **松露虫（Truffle Worms）**：不再受到敌对 NPC 或弹幕的伤害（→ Terraria/NPC.cs, Terraria/Projectile.cs）。
- 修复鹿角怪在多人模式下的「疯狂（madness）」潜在问题（→ Terraria/NPC.cs）。
- 鹿角怪现在会正确掉落金币（→ Terraria/GameContent/ItemDropRules, Terraria/NPC.cs）。

### 【世界生成】
- （本版无独立世界生成条目。）

### 【渲染与视觉特效】
- 修复玩家不正确持握水晶蛇（Crystal Serpent）的问题（→ 物品使用动画, Terraria/Player.cs）。
- 修复泥巴芽（Mud Bud / Plantero 宠物）的阔边帽在关闭「血腥与断肢」设置时变成一团云雾的问题（→ Terraria/Projectile.cs, 渲染）。
- 修复使用风暴弓（Daedalus Stormbow）时视觉上不在「向上射击」的问题（→ Terraria/Projectile.cs, 渲染）。

### 【UI与界面】
- 修复各季节兔子在怪物图鉴（Bestiary）中没有「地表」标签的问题（→ 图鉴, Terraria.ID/NPCID.cs）。
- 修复冻僵僵尸（Frozen Zombie）和狼（Wolf）在图鉴中缺少雪原生物群落分类的问题（→ 图鉴, Terraria.ID/NPCID.cs）。
- 鹿角怪和冰霜巨人（Ice Golem）现在正确在图鉴中使用「雨天」标签（→ 图鉴, Terraria.ID/NPCID.cs）。
- 修复图鉴中「地表」与「时间」标签排序不一致的问题（→ 图鉴, UI）。

### 【音频】
- 修复资源包中部分 ogg 文件无法正确循环的问题（→ 音频/资源包）。

### 【机制系统改动】
- 修复水晶塔（Pylons）从下方交互的距离与实际允许传送距离不一致的问题（→ Terraria/Player.cs, Terraria/Main.cs）。
- 修复某些情况下压力板（Pressure Plates）和逻辑感应器（Logic Sensors）被采掘时没有正确从世界中移除的问题（→ Terraria/WorldGen.cs, Terraria.ID/TileID.cs）。
- 移除花冠（Garland）意外具有的第二种合成配方（→ Terraria/Recipe.cs）。

### 【多人/网络】
- 修复阿比盖尔的花在服务器中生长时视觉不同步（使其隐形，直到玩家重新加入）（→ Terraria/Projectile.cs, 网络同步）。
- 尝试修复加入缓慢的玩家可能在加入服务器过程中死于黑暗（The Constant 黑暗伤害）的问题（→ Terraria/Player.cs, 网络同步）。
- 修复物品复制漏洞与另一个未具名漏洞（→ 物品/容器同步逻辑）。

### 【Bug修复（纯崩溃归并一句）】
- 修复丛林宝箱怪（Jungle Mimic）罕见崩溃、游玩损坏的云存档世界崩溃等问题（→ Terraria/NPC.cs, 存档系统）。

---

## 1.4.3.2（修补程序）— 2021-11-24

### 【物品与数值平衡】（全部保留具体数字）
- **阿比盖尔的花（Abigail's Flower）**：
  - 仆从基础移动速度增加 33%（由 3 增加至 4）（→ Terraria/Projectile.cs）。
  - 每个仆从的速度增加量由 1.5 降低至 1.4（在 11 个仆从时与之前数值相同）（→ Terraria/Projectile.cs）。
  - 基础加速度增加 10%（→ Terraria/Projectile.cs）。
  - 加速度增加量由 2 降低至 1.75（在相同仆从数量时达到最大）（→ Terraria/Projectile.cs）。
- **露西斧（Lucy the Axe）**：使用时间由 20 降低至 17；体积由 1 增加至 1.2（大 20%）；斧力由 125% 增加至 150%（→ Terraria/Item.cs）。
- **Weather Pain（痛苦法杖）**：弹幕持续时间增加 50%；最多穿透数由 10 增加至 12；弹幕移动速度由 7 增加至 8（→ Terraria/Projectile.cs, Terraria/Item.cs）。
- **Pew-matic Horn**：伤害提升 1；使用时间由 24 降低至 15；弹速由 11 增加至 14（→ Terraria/Item.cs, Terraria/Projectile.cs）。
- **Houndius Shootius**：弹速由 8.5 增加至 12.5（→ Terraria/Projectile.cs, Terraria/Item.cs）。
- **蝙蝠棒（Bat Bat）**：使用时间由 30 增加至 45；伤害由 18 增加至 31；体积由 1 增加至 1.15（大 15%）；现在每次挥舞击中时恢复 1 点生命值（→ Terraria/Item.cs, Terraria/Player.cs）。
- **触手长钉（Tentacle Spike）**：击中敌人会刺入一根伤害性钉刺；每根钉刺每秒造成 3 伤害，持续 9 秒；每个敌人最多被刺入 5 根钉刺（→ Terraria/Item.cs, Terraria/Projectile.cs, Terraria.ID/BuffID.cs）。
- **火腿棒（Ham Bat）**：新特性——杀死敌人会提供一小段爆发性生命再生；伤害由 50 增加至 57；体积由 1 增加至 1.2（大 20%）（→ Terraria/Item.cs, Terraria/Player.cs）。
- **炒蛙腿（Sauteed Frog Legs）**：10 分钟「很满意（Plenty Satisfied）」调整为 10 分钟「进食良好（Well Fed）」（→ Terraria/Item.cs, Terraria.ID/BuffID.cs）。
- **蛙腿三明治（Froggle Bunwich）**：8 分钟「精致增饱（Exquisitely Stuffed）」调整为 8 分钟「很满意（Plenty Satisfied）」（→ Terraria/Item.cs, Terraria.ID/BuffID.cs）。

### 【机制系统改动】
- 修复蝙蝠棒造成击杀时不会治疗的问题（→ Terraria/Item.cs, Terraria/Player.cs）。
- 修复特定弹幕会错误地重置 NPC 对其它弹幕免疫的问题（→ Terraria/Projectile.cs, Terraria/NPC.cs）。
- 修复护士（Nurse）会治愈一些正面减益的问题（→ Terraria/NPC.cs, Terraria.ID/BuffID.cs）。
- 修复 The Constant 世界中，饥饿状态更改时会删除部分增益（buff）的问题（→ Terraria/Player.cs, Terraria.ID/BuffID.cs）。
- 修复用 serverconfig.txt 生成的世界没有正确设置特殊种子数据的问题（→ Terraria.Utilities, Terraria/WorldGen.cs）。
- 修复打开房屋管理菜单「非常长」时间后游戏运行缓慢的问题（→ Terraria/Main.cs, UI）。

### 【世界生成】
- 修复 Don't Starve（The Constant）种子的黑暗会在天空中造成不正常的黑色方块，并使部分生物群落夜间过亮的问题（→ Terraria/GameContent/Drawing/TileDrawing.cs, Terraria/Main.cs）。

### 【渲染与视觉特效】
- 修复创意工坊资源包不总是正确显示创意工坊标签的问题（→ UI, 资源包系统）。

### 【UI与界面】
- 损坏的玩家存档现在会尽可能列出其来源而非损坏文本；损坏的世界存档不再使世界选择界面崩溃；损坏存档文本颜色改为灰色而非红色（→ 存档系统, UI）。

### 【音频】
- （本版无独立音频改动。）

### 【多人/网络】
- （再次）修复阿比盖尔的花在服务器中生长时视觉不同步（→ Terraria/Projectile.cs, 网络同步）。
- 修复旅途模式（Journey Mode）的敌人生成速率设置在离开服务器后重置的问题（→ Terraria/Main.cs, 网络同步）。
- 修复物品复制漏洞（→ 物品/容器同步逻辑）。

### 【Bug修复（纯崩溃归并一句）】
- 修复与标记收藏的云存档相关的罕见崩溃、损坏存档导致的界面崩溃等问题；另有修复部分情况下允许用户上传从创意工坊下载的资源包的问题（→ 存档系统, 资源包校验）。

---

## 1.4.3.3（Steam Deck 优化更新）— 2022-02-24

### 【机制系统改动】（总体）
- 召唤的仆从、哨兵及其弹幕不再伤害小动物（critters）（→ Terraria/Projectile.cs, Terraria/NPC.cs）。
- **黑曜石**现在可被镐力 55% 及以上的镐采掘（→ Terraria.ID/TileID.cs, Terraria/Player.cs）。
- **经典模式**下击败血肉墙（Wall of Flesh）时总是会掉落 1 件武器和 1 件徽章（emblem），与专家模式宝藏袋一致（→ Terraria/GameContent/ItemDropRules, Terraria/NPC.cs）。
- **黑珍珠与粉珍珠**在打开牡蛎（Oyster）时更为常见，售价按比例降低（→ Terraria/GameContent/ItemDropRules, Terraria/Item.cs）。
- **生命雕像与星星雕像**的生成几率相较于其他雕像提高到两倍（→ Terraria/WorldGen.cs, Terraria.ID/TileID.cs）。
- **蛛网投放器（Web Slinger）**射程增加 25%（→ Terraria/Item.cs, Terraria/Projectile.cs）。
- **食人鱼枪（Piranha Gun）**的食人鱼现在能更好地跟随快速移动的敌人（只要它们未传送或短暂无敌）（→ Terraria/Projectile.cs）。
- 将**仙灵之翼（Fairy Wings）**的合成配方改为仅需 99 个妖精尘（Pixie Dust），而非 100（因妖精尘最大堆叠为 99）（→ Terraria/Recipe.cs）。
- 相较于用于合成它的宝石，**彩色玻璃（Stained Glass）**售价更加合理（→ Terraria/Recipe.cs, Terraria/Item.cs）。
- **旅途模式（Journey Mode）研究数量下调**：毛皮（Flinx Fur）所需研究数量更少；所有食物（麦酒与清酒除外）研究数量更少；所有生物群落宝箱（crates）以及金锁盒、黑曜石锁盒研究数量更少（→ 旅途研究, Terraria.ID/ItemID.cs）。
- **NPC 快乐度（Happiness）系统调整**：
  - 水晶塔（Pylons）至少需要 2 个 NPC 待在一起时才会出售（→ Terraria/NPC.cs, Terraria/Main.cs）。
  - NPC 可出售水晶塔的最低快乐度要求由 0.85 放宽至 0.9（数值越低越快乐，即更容易达标）（→ Terraria/NPC.cs）。
  - 混合生物群落（如神圣沙漠）规则：若 NPC 至少喜欢其中一个群落，则可从他喜欢的群落获得快乐度加成；仅限「喜欢 + 中立/不喜欢」组合，中立不会覆盖不喜欢，也不会覆盖因邻近腐化/猩红/地牢导致的最大不快乐与住房不可用（→ Terraria/NPC.cs）。
  - 「拥挤」惩罚生效前，城镇可容纳 NPC 数量上限提升 1（→ Terraria/NPC.cs）。

### 【物品与数值平衡】（Boss 掉落相关）
- **骷髅王（Skeletron）**现在掉落治疗药水（Healing Potion）而非弱效治疗药水（Lesser Healing Potion）；**鹿角怪**同样处理；**蜂后（Queen Bee）**仍掉落瓶装蜂蜜（→ Terraria/GameContent/ItemDropRules, Terraria/NPC.cs）。
- **鹿角怪**死亡时掉落治疗药水，与骷髅王相同（→ Terraria/GameContent/ItemDropRules）。

### 【NPC与Boss与AI】（鹿角怪专项）
- 如果玩家尚未击败鹿角怪，向导（Guide）会提供一条如何寻找它的提示（→ Terraria/NPC.cs, 对话数据）。
- 鹿角怪的生命值在专家/大师模式下现在会和其他 Boss 一样按修正系数增加，因此其最大生命值在专家与大师中都会**降低**（→ Terraria/NPC.cs, Terraria.ID/NPCID.cs）。
- 上述修复同时修正了鹿角怪生命值在专家/大师多人模式下没有按玩家数量提高的问题（→ Terraria/NPC.cs, 多人同步）。
- 附近没有玩家时，鹿角怪只会在雪原生物群落停留 1 天而非 3 天（→ Terraria/NPC.cs）。
- 鹿角怪的 Boss 血条现在会在距离远到 Boss 战不激活时消失，战斗继续时重新出现（→ Boss 血条 UI, Terraria/Main.cs）。
- 修复鹿角怪具有 0 点防御的疏漏（→ Terraria/NPC.cs, Terraria.ID/NPCID.cs）。
- 击败鹿角怪后，它在适当条件下只有 25% 几率自然生成，而非之前的 100%（→ Terraria/NPC.cs, 生成逻辑）。

### 【世界生成】
- 优化了放置砂岩宝箱（Sandstone Chest，官方日志中宝箱名称有误）阶段的世界生成（→ Terraria/WorldGen.cs）。
- 修复丛林神龛（Jungle Shrine）与生命红木树（Living Mahogany Tree）重叠生成可能产生破损宝箱的问题（→ Terraria/WorldGen.cs）。

### 【渲染与视觉特效】
- 更新了气球束（Bundle of Balloons）的贴图，以更好展现用于合成它的物品（→ 贴图资源）。
- 在天然墙旁边放置墓地（Graveyard）制作的对应墙时，现在应无缝衔接、没有较大空隙（→ Terraria/GameContent/Drawing/TileDrawing.cs, Terraria.ID/TileID.cs）。
- 修复应当阻挡光的部分物块没有阻挡光的问题（→ 光照, Terraria/Main.cs, TileDrawing.cs）。
- 修复来自腐化火把的火炬之神的弹幕生成雪尘的问题（→ Terraria/Projectile.cs）。
- 修复切斯特（Chester）的智能光标边框在它处于空中时不随它旋转的问题（→ Terraria/Projectile.cs, 智能光标）。
- 修复黑曜石盔甲只具有稀有度 0 的问题（应为更高稀有度）（→ Terraria/Item.cs）。
- 修复星辰披风类饰品生成的星星在多人下不同步的问题（→ Terraria/Projectile.cs, 多人同步）。
- 修复世纪之花（Plantera）的孢子弹幕在多人下不同步的问题（→ Terraria/Projectile.cs, 多人同步）。

### 【UI与界面】
- 虚拟键盘（手柄用游戏内键盘）现在可用于 IP/密码输入及其他多人文本输入（→ UI, Terraria/Main.cs）。
- 修复「感电（Electrified）」减益具有不准确且毫无提示作用的工具提示（tooltip）的问题（→ Terraria.ID/BuffID.cs, 文本）。
- 修复部分 UI 控制文本在波兰语设置下损坏的问题（→ 本地化文本）。

### 【物品使用/合成】
- 修复蜂蜜炸弹（Honey Bomb）与干炸弹（Dry Bomb）不能放在武器架（Weapon Rack）上的问题（→ Terraria/Item.cs, Terraria.ID/TileID.cs）。
- 修复熔岩钓鱼装备会错误影响钓鱼数值的问题（→ Terraria/Player.cs, 钓鱼逻辑）。

### 【音频】
- （本版无独立音频改动。）

### 【多人/网络】
- 星辰披风星星、世纪之花孢子弹幕的多人不同步修复（见渲染与视觉特效）（→ Terraria/Projectile.cs）。
- 修复文本导致的多人崩溃（→ 网络同步）。

### 【Bug修复（影响玩法逻辑）】
- 修复行走的金鱼无法像其他金鱼一样被腐化/猩红感染的问题（→ Terraria/NPC.cs, Terraria.ID/NPCID.cs）。
- 修复沙漠虎（Desert Tiger）在旅途模式时间暂停/加速时无法正确在敌人身上弹跳的问题（→ Terraria/Projectile.cs, Terraria/Main.cs）。
- 修复露西斧在砍伐棕榈树或仙人掌时不会说话的问题（→ Terraria/Item.cs, 特殊武器对话）。
- 修复精灵熔毁（Elf Melter）每次使用消耗 2 发弹药的问题（→ Terraria/Item.cs, Terraria/Player.cs）。
- 修复连锁断头台（Chain Guillotines）的锁链在某些角度下消失的问题（→ Terraria/Projectile.cs）。
- 修复睡眠时 Eyebrella 的云位置奇怪的问题（→ Terraria/Player.cs, 渲染）。

### 【Bug修复（纯崩溃归并一句）】
- 修复特定 NPC 大量生成时的罕见崩溃等（→ Terraria/NPC.cs）。

---

## 1.4.3.4（修补程序）— 2022-02-24

- 【Bug修复】修复游戏中游戏摇杆与鼠标输入的特定组合导致 Steam Deck 上出现光标式闪烁的问题（→ 输入处理, Terraria/Main.cs）。
- 【Bug修复】修复特定的游戏摇杆 UI 操作无法正常执行的问题（→ UI/输入, Terraria/Main.cs）。

---

## 1.4.3.5（修补程序）— 2022-02-28

- 【Bug修复-机制】修复使用「跳帧：关闭」设置时，部分输入失效或表现奇怪的问题（→ Terraria/Main.cs, 输入处理）。
- 【NPC与Boss与AI】修复城镇 NPC 没有正确谈论其所在生物群落名称的问题（→ Terraria/NPC.cs, 对话数据）。
- 【NPC与Boss与AI/弹幕】修复传送门法杖（Lunar Portal）的激光在特定情况下会消失的问题（→ Terraria/Projectile.cs）。
- 【多人/网络】修复敌人在多人模式下会在破裂地牢砖（Cracked Dungeon Bricks）上滑动的问题（→ Terraria/NPC.cs, 碰撞/网络同步）。
- 【世界生成】修复砂岩宝箱的生成优化（承接 1.4.3.3 的改动）（→ Terraria/WorldGen.cs）。

---

## 1.4.3.6（修补程序）— 2022-03-01

- 【Bug修复】修复大量导致 Mac/Linux 平台在退出游戏时无限挂起的问题（→ FNA/平台层）。
- 【Bug修复】修复 Linux 上的 Steam 覆盖界面问题；更新 FNA（Mac/Linux 相关）（→ FNA/平台层）。
- 说明：本版为纯平台层修复，与游戏玩法逻辑无关，网页复刻项目无需跟进。

---

## 【本版本改动规模评估】

**改动规模**：1.4.3 全系列共涉及约 **15+ 个独立系统**：特殊种子/世界常量（The Constant）、新 Boss（鹿角怪）、饥饿与黑暗伤害机制、火把/篝火熄灭机制、新物品体系（宠物/武器/食物/虚荣/画作/饰品）、NPC 快乐度与水晶塔经济、Boss 掉落规则、仆从/哨兵与召唤物 AI、弹幕穿透与免疫机制、镐力门槛与物块合并、旅途模式研究数量、世界生成（大理石/蜘蛛群落/砂岩宝箱/微生态）、渲染与光照、Boss 血条 UI、怪物图鉴、输入与配置（含 Steam Deck 适配）。其中 1.4.3 主体是「内容型」更新（新增远多于修改），1.4.3.1~.3 是数值与规则热修，1.4.3.4~.6 几乎全是平台层修复。

**复刻项目必须跟进的核心改动**（按优先级）：
1. **The Constant 特殊种子**（种子解析、专属着色器/光照、黑暗伤害、雨水熄灭火把、地表大理石/地上蜘蛛群落的世界生成分支）——最大的机制型新增，涉及 Terraria.Utilities、WorldGen.cs、Player.cs、TileDrawing.cs，建议作为独立世界生成分支实现。
2. **饥饿机制**（Player.cs 专属状态机 + BuffID）——全新玩家生存系统，必须先于任何联动物品落地。
3. **鹿角怪 Boss**（NPCID 新增、Boss AI、专家/大师生命值系数、雪原停留与 25% 自然生成率、全套掉落与主题曲）——联动版本的标志性内容，且 1.4.3.1/.3 对其数值修了三轮，落地时要直接采用修后数值。
4. **联动物品数值**（阿比盖尔的花、Bat Bat、Tentacle Spike、Ham Bat、Lucy the Axe、Weather Pain、Pew-matic Horn、Houndius Shootius 及食物增益档位）——以 1.4.3.2 修后数值为准，1.4.3 初版数值已全部作废，不要照抄初版。
5. **全局规则修正**（仆从不再伤害小动物、黑曜石 55% 镐力、经典模式血肉墙必掉武器+徽章、NPC 快乐度 0.9 门槛与拥挤上限 +1、鹿角怪/骷髅王掉治疗药水、精灵熔毁耗弹修复、弹幕重置 NPC 免疫修复）——这些是无条件生效的全局规则，即使不做联动内容也必须同步，建议优先合入。

**可暂缓/不必跟进**：Steam Deck 输入适配（1.4.3.4）、Mac/Linux 与 FNA 层修复（1.4.3.6）、创意工坊资源包与云存档相关（复刻环境无对应基础设施）、图鉴标签排序等纯展示条目。
