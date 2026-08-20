# 泰拉瑞亚 1.4.1 / 1.4.1.1 / 1.4.1.2 更新日志结构化摘要

> 来源：中文 wiki（MediaWiki API wikitext），原始文件 /tmp/tw-changelog/1.4.1.json、1.4.1.1.json、1.4.1.2.json。
> 1.4.1 代号 "Rounding Out the Journey（结束旅程）"，发布于 2020-10-13；1.4.1.1 发布于 2020-10-14；1.4.1.2 发布于 2020-11-10。
> 行尾括号内为该条大概率影响的反编译源码文件（Terraria 命名空间）。

---

## 一、版本 1.4.1（Rounding Out the Journey）

### 【新增内容】

- 新增 6 套 Vanity 竞赛获奖套装，全部可用 pre-Hardmode 材料制作：瘟疫使者套装（Plaguebringer's set）、流浪者套装（Wandering set）、时空旅者套装（Timeless Traveler's set）、小花守护者套装（Floret Protector set）、摩羯座套装（Capricorn set）、电视头套装（TV Head set，大奖得主）(→ Item.cs, Recipe.cs, Terraria.ID/ItemID.cs)
- 新增一批成就 (→ Main.cs, Terraria.GameContent.UI)
- 新增制作人员字幕（Credits）及对应音乐曲目：第一次打败 Moon Lord 后出现，主菜单也可查看；Music Box (Journey's End) 改为录下 Credits 音乐生成，普通饰品栏使用会在游戏内播放 Credits 动画，社交栏使用只放音乐 (→ Item.cs, Main.cs, Terraria/Audio)
- 新城镇 NPC 公主（Princess）及各种相关物品，外加一个新发型 (→ NPC.cs, Terraria.ID/NPCID.cs, Item.cs)
- 新早期召唤装备：Flinx Fur Coat（伶鼬皮大衣）、Flinx Staff（伶鼬法杖）(→ Item.cs, Terraria.ID/ItemID.cs, Projectile.cs)
- 新 pre-Hardmode 鞭子 Spinal Tap（脊骨鞭），地牢等级可制作 (→ Item.cs, Projectile.cs, Recipe.cs)
- 新饰品 Lavaproof Tackle Bag（熔岩防钓具袋）：Lavaproof Fishing Hook + Angler Tackle Bag 合成 (→ Item.cs, Recipe.cs)
- Bee Hive（蜂巢块）与 Antlion Eggs（蚁狮蛋）现在可制作、可放置 (→ Item.cs, Recipe.cs, Terraria.ID/TileID.cs)
- 新 vanity 饰品 Rainbow Cursor（彩虹光标）(→ Item.cs)
- Plantero's Sombrero 回归游戏（官方 I.C 节，原已移除的世纪之花造型帽）(→ Item.cs)

### 【物品与数值平衡 — 近战武器】

- Terra Blade 线整体重构：Mothron 只在 Plantera 后生成，Broken Hero Sword 因此变为 Plantera 后限定 (→ NPC.cs, WorldGen.cs, Item.cs)
- True Night's Edge：弹幕伤害 1.5 倍基础伤害；autoswing；配方改为 Night's Edge + 3 个机械 Boss 魂，不再需要 Broken Hero Sword (→ Item.cs, Projectile.cs, Recipe.cs)
- True Excalibur：伤害 66→70；autoswing；弹幕穿透 1 次最多命中 2 敌；配方改为 Excalibur + 叶绿锭，不再需要 Broken Hero Sword (→ Item.cs, Projectile.cs, Recipe.cs)
- Terra Blade：伤害 95→115，Use Time 16→14，弹幕伤害 1.25 倍→1.5 倍；配方改为两把"真"剑 + 一把 Broken Hero Sword (→ Item.cs, Projectile.cs, Recipe.cs)
- Beam Sword：缩放比例 1→1.3（剑本体变大）(→ Item.cs, Projectile.cs)
- Brand of the Inferno：缩放比例 1.15→1.3 (→ Item.cs, Projectile.cs)
- Sunfury：基础伤害 35→32（链球普通挥舞双倍伤害，预期伤害 70→64）(→ Item.cs)
- Arkhalis：伤害 20→25；忽略至多 20 点敌人防御 (→ Item.cs, Projectile.cs)
- Chain Guillotines：伤害 43→59 (→ Item.cs)
- Ghastly Glaive：免伤帧时长 36→20 (→ Projectile.cs)
- Anchor：伤害 55→70，击退 5→8 (→ Item.cs)
- Sergeant United Shield：伤害 60→80；每命中一个目标的伤害减免 30%→20% (→ Item.cs, Projectile.cs)
- Scourge of the Corruptor：伤害 64→70；小吞噬怪伤害 70%→75% 基础伤害 (→ Item.cs, Projectile.cs)
- 悠悠球：撤销 1.4 对 Chik、Amarok、Hel-Fire 的改动；不撤销 Code 2、Amazon、Kraken 的改动；Gradient 伤害 44→49；Format C 伤害 35→39 (→ Item.cs)
- Light's Bane：伤害 17→18 (→ Item.cs)
- Muramasa：伤害 21→26，击退 2.5→3 (→ Item.cs)
- Fiery Greatsword：伤害 36→40 (→ Item.cs)
- Beekeeper：撤销 1.4 对它的改动 (→ Item.cs)
- 所有 Phaseblade：伤害 21→25 (→ Item.cs)
- Night's Edge：Use Time 27→21；autoswing (→ Item.cs)
- Bananarang：Use Time 14→11；香蕉弹幕速度与返回速度均提升 (→ Item.cs, Projectile.cs)
- Thorn Chakram / Flamarang：弹幕速度与返回速度均提升，Flamarang 更快 (→ Projectile.cs)
- Sleepy Octopod：伤害 40→50；命中半径/攻击大小 +35% (→ Item.cs, Projectile.cs)
- Flying Dragon：伤害 90→180；视线无法直达的弹幕（穿墙射击）只造成一半伤害（即 90）(→ Item.cs, Projectile.cs)
- Sky Dragon's Fury：伤害 70→140；弹幕伤害 75%→50% 基础伤害（原单发 52 即 70×75%，现为 70 即 140×50%，实际提升）(→ Item.cs, Projectile.cs)
- Starlight：伤害 70→80；新增 10% 暴击率奖励 (→ Item.cs)
- Daybreak：弹幕在过期或击中墙时爆炸，爆炸额外造成 100% 武器伤害并可命中附近敌人 (→ Projectile.cs)

### 【物品与数值平衡 — 远程武器与弹药】

- Onyx Blaster：伤害 28→24，Use Time 45→48 (→ Item.cs)
- Quad-Barrel Shotgun：伤害 24→17，弹丸数 4→6，Use Time 45→55；军火商只在骷髅王后出售 (→ Item.cs, Projectile.cs, NPC.cs)
- StakeLauncher：Use Time 26→12；弹幕每穿透一敌，下一次命中受 10% 伤害惩罚 (→ Item.cs, Projectile.cs)
- Blowpipe：Use Time 45→25；种子（弹药）伤害 3→4 (→ Item.cs)
- Jack 'O Lantern Launcher：Use Time 30→25；爆炸南瓜（弹药）伤害 30→60 (→ Item.cs)
- Dart Pistol / Dart Rifle：撤销 1.4 的平衡改动，伤害分别 33→28、62→52（注：wiki 标注此条实际到 1.4.2.2 才生效）；Crystal/Curse/Ichor 弹药的改动保留 (→ Item.cs)
- Tsunami：伤害 60→53 (→ Item.cs)
- Nano Bullet：可反弹一次，附近有目标时"智能反弹"；反弹后只造成 66% 伤害 (→ Projectile.cs, Item.cs)
- Beenade：伤害 14→12；Bone Arrow：伤害 6→8；Chlorophyte Bullet：伤害 10→9 (→ Item.cs)
- Cursed Bullet：速度提升到与 Ichor Bullet 一致 (→ Item.cs)
- Meteor Shot：伤害 9→8；重做免伤时间系统，快速开火/霰弹类武器不再因免伤帧丢命中 (→ Item.cs, Projectile.cs)
- High Velocity Bullet：伤害 10→11；弹幕穿透 2 次最多命中 3 敌；每穿透一敌下一次命中受 15% 伤害惩罚；免伤时间系统与 Meteor Shot 一致 (→ Item.cs, Projectile.cs)
- Crystal Bullet：撞击时只生成 2 个碎片（原 3 个）(→ Projectile.cs)
- Jester's Arrow：每穿透一敌下一次命中受 10% 伤害惩罚；Unholy Arrow：受 5% 伤害惩罚 (→ Projectile.cs)

### 【物品与数值平衡 — 魔法武器】

- Life Drain：伤害 30→35；未命中不消耗魔力（同 Medusa Head）(→ Item.cs)
- Nightglow：魔力消耗 26→23；弹幕会反弹 (→ Item.cs, Projectile.cs)
- Shadowbeam Staff：伤害 53→60，Use Time 16→15，每目标命中伤害减免 20%→10% (→ Item.cs, Projectile.cs)
- Unholy Trident：伤害 73→88；每穿透一敌下一次命中受 10% 伤害惩罚 (→ Item.cs, Projectile.cs)
- Poison Staff 射程约 30 格→37 格；Venom Staff 射程约 45 格→58 格 (→ Item.cs, Projectile.cs)
- Medusa Head：效果射程 +25% (→ Item.cs)
- Crystal Vile Shard / Nettle Burst / Wasp Gun：忽略至多 10 点敌人防御 (→ Projectile.cs)
- Razorblade Typhoon：同等魔力消耗与 Use Time 下每次只发 1 发弹幕（原 2 发），弹幕伤害 +50%（60→90）(→ Item.cs, Projectile.cs)
- Magical Harp：伤害 32→42，击退 0→0.25，魔力消耗 4→5；每穿透一敌下一次命中受 5% 伤害惩罚 (→ Item.cs, Projectile.cs)
- Blood Thorn：伤害 29→34；单个弹幕可命中 3 次（原 2 次）；重做免伤时间系统；Use Time 21→33 (→ Item.cs, Projectile.cs)
- Magic Missile：Use Time 18→22，魔力消耗 12→14；Flamelash：伤害 36→32，魔力消耗 18→21 (→ Item.cs)
- Flower of Fire：Use Time 20→16，魔力消耗 15→12；Space Gun：伤害 19→17，魔力消耗 7→6 (→ Item.cs)
- Charged Blaster Cannon：完全光束模式下可以瞄准光束 (→ Projectile.cs)
- Betsy's Wrath：伤害 65→110 (→ Item.cs)
- Stellar Tune：伤害 75→85 (→ Item.cs)

### 【物品与数值平衡 — 召唤武器】

- 鞭子多目标伤害惩罚下调：Cool Whip 33%→30%，Durendal 30%→20%，Morning Star 25%→5%，Dark Harvest 30%→10%，Kaleidoscope 15%→10% (→ Projectile.cs, Item.cs)
- 所有鞭子（Leather Whip 除外）射程提升：早期最少（Snapthorn 约 +10%），末期最大（约 +50%）(→ Projectile.cs)
- 鞭子现在可受益于 Flask 增益 (→ Projectile.cs, Player.cs)
- Leather Whip：Zoologist 处购买所需图鉴完成度 15%→10% (→ NPC.cs)
- Finch Staff：雀鸟命中目标更可靠（故意保留少量不准）；被击退的敌人几乎总是退向远离玩家方向 (→ Projectile.cs)
- Optic Staff：修正 Retinamini 激光未使用独立免伤计时器的 bug，减少免伤帧冲突 (→ Projectile.cs)
- Sanguine Staff：血蝠攻击速度 60→66（攻击路线耗时）(→ Projectile.cs)
- Xeno Staff：开火冷却 30→33（攻速约 -10%）；Tempest Staff：开火冷却 60→50（攻速约 +20%），Sharkron 弹速 14→20，风暴自身移速 +50% (→ Projectile.cs)
- Hornet Staff：伤害 9→11；Vampire Frog Staff：伤害 11→13，整个身体都能造成伤害（原只有舌头），修正未用独立免伤计时器的 bug (→ Item.cs, Projectile.cs)
- Pygmy Staff：弹速 12→18；触发投矛范围 +40% (→ Projectile.cs)
- Desert Tiger Staff：基础伤害 33→41；特殊攻击碰撞框增大减少落空 (→ Item.cs, Projectile.cs)
- Frost Hydra Staff：弹幕穿透 2 次最多 3 敌；每穿透一敌下一次命中受 15% 伤害惩罚 (→ Projectile.cs)
- Explosive Trap Staff：爆炸大小与检测范围 +50%；爆炸冷却 110→90；Huntress 套装/red Riding 套装（Hood）冷却分别 74→60、40→30 (→ Projectile.cs, Item.cs)
- Kaleidoscope：伤害 165→180 (→ Item.cs)

### 【物品与数值平衡 — 盔甲】

- Cactus armor：移除 1 防御套装奖励；新套装奖励：造成 15 点针刺伤害（Expert/Master 下 ×2/×3 为 30/45）(→ Item.cs, Player.cs)
- Mining armor：Mining Shirt/Pants 掉落率 2.4%→12% (→ ItemDropRules, Item.cs)
- Gladiator armor：头盔护腿防御 +1、胸甲 +2；新套装奖励：全套免疫击退；掉落率 1/20→1/7（随机一件）(→ Item.cs, ItemDropRules)
- Fossil armor：头盔护腿防御 2→4、其远程暴击 3%→4%；胸甲防御 4→5、3% 远程暴击替换为 5% 远程伤害 (→ Item.cs)
- Wizard Hat：魔法伤害 15%→5%，防御 2→4；Magic Hat：魔法伤害/暴击奖励 7→6 (→ Item.cs)
- Meteor armor：每件魔法伤害 7%→9%（总量 21%→27%）(→ Item.cs)
- Jungle armor（含 Ancient Cobalt armor）：帽/裤魔法暴击 4%→6%；衬衫 4% 魔法暴击替换为 6% 魔法伤害 (→ Item.cs)
- Necro armor：套装远程暴击 15%→10%；每件防御 +1（共 +3，含 Ancient Necro Helmet）(→ Item.cs)
- Obsidian armor：整套改为以鞭子为核心的召唤师盔甲；组件只能在 Hellforge 制作（需 Shadow Scale/Tissue Sample）；Obsidian Outlaw Hat +9% 召唤伤害、Obsidian Longcoat +1 仆从位、Obsidian Greaves +9% 召唤伤害；新套装奖励：鞭子射程与速度 +50%，再 +25% 召唤伤害（全套共 43%）(→ Item.cs, Recipe.cs, Player.cs)
- Molten armor：头盔 7% 近战暴击、胸甲 7% 近战伤害、护腿 7% 近战速度；17% 近战伤害套装奖励降为 10%（7% 移入胸甲）；新套装奖励：全套不会染上 On Fire (→ Item.cs, Player.cs)
- Cobalt armor：胸甲暴击 3%→5%；护腿防御 7→8、新增 3% 伤害；近战头盔防御 11→12、移速 7%→10%、12% 近战速度改为 15% 近战伤害；远程 Mask 暴击 6%→10%；魔法 Hat 新增 10% 魔法伤害 (→ Item.cs)
- Palladium armor：治疗套装奖励效力 6→4；Melee Mask 伤害 8%→12%；Magic Headgear 伤害 7%→9% (→ Item.cs, Player.cs)
- Mythril armor：链甲伤害 5%→7%；护腿暴击 3%→10%；近战头盔暴击 5%→8%；近战套装奖励 5%→10% 暴击 (→ Item.cs)
- Orichalcum armor：Melee Mask 伤害 7%→11%、近战速度 7%→11% (→ Item.cs)
- Adamantite armor：胸甲伤害 6%→8%；护腿暴击 4%→7%；近战套装奖励 18%→20%；远程 Mask 暴击 8%→10%；魔法 Headgear 伤害 11%→12%、暴击 11%→12% (→ Item.cs)
- Titanium armor：Melee Mask 伤害/暴击/速度 8%→9% (→ Item.cs)
- Frost armor：套装奖励额外 +10% 近战/远程伤害；其 On Fire 特版改为 25 DPS（原 8）(→ Item.cs, BuffID.cs)
- Forbidden armor：Forbidden Robes +10% 召唤伤害；Forbidden Treads +10% 魔法伤害 (→ Item.cs)
- Chlorophyte armor：叶绿水晶射击冷却 50→40 (→ Item.cs, Projectile.cs)
- Spectre armor（Mask）：魔法伤害/暴击加成 5%→10%；套装爆发伤害上限 1000→1500；"恢复率" 250→400 (→ Item.cs, Player.cs)
- Spectre armor（Hood）：数值无变化；-40% 伤害惩罚从 Hood 移到套装奖励，重写 tooltip 使"以攻换疗"更清晰 (→ Item.cs, Player.cs)
- Crystal Assassin armor：头 -10% 魔力消耗、衣 -10% 弹药消耗、腿 +10% 近战速度；移除套装 15% 移速但靴子移速 10%→20%；新套装奖励：全套可冲刺（Dash）(→ Item.cs, Player.cs)
- Old One's Army 系列盔甲：Squire Greaves 近战暴击 20%→15%；Monk Pants 近战暴击 10%→15%；Huntress's Jerkin +10% 弹药减免；Apprentice Helmet +10% 魔法伤害；Valhalla Knight 头盔 +10% 近战伤害、护腿移速 30%→20%；Shinobi Infiltrator 裤移速 20%→30%、躯干 +5% 近战暴击；Red Riding 腿 +10% 远程暴击、裙 +20% 弹药减免；Dark Artist 腿 +20% 移速、袍 -15% 魔力消耗、5% 仆从/魔法伤害从袍移到帽 (→ Item.cs)

### 【物品与数值平衡 — 饰品】

- Band of Regeneration / Charm of Myths：恢复速度 0.5 生命/秒→1 生命/秒 (→ Item.cs, Player.cs)
- Band of Starpower / Panic Necklace：可在墓地区工匠作坊制作（与生命/魔力水晶互转），全世界更容易获得 (→ Recipe.cs)
- Bone Glove：完全重制为饰品；装备后攻击时每秒向光标射出交叉骨头，25 点无类型伤害并忽略至多 25 点防御；新增手部栏 vanity 外观 (→ Item.cs, Projectile.cs, Player.cs)
- Brain of Confusion：Cerebral Mindtrick 暴击奖励 20%→10%，持续时间 -1 秒 (→ Item.cs, BuffID.cs)
- Celestial Cuffs：获得组件的 +20 魔力奖励 (→ Item.cs)
- Diving Helmet 及其所有制品：呼吸容量加成 +50% (→ Item.cs, Player.cs)
- Feral Claws / Titan Glove："近战 autoswing"能力从 Titan Glove 转移到 Feral Claws；Titan Glove 新特性：合格近战武器大小 +10%（制品链继承，不叠加）(→ Item.cs, Player.cs)
- Lucky Horseshoe / Fledgling Wings：幸运马掌不再出现在空岛箱，改入地下金箱掉落表；稚翼之翼加入空岛箱与空岛匣 (→ ItemDropRules)
- Flesh Knuckles / Berserker's Glove：防御 7→8；Hero Shield：防御 7→10；Fire Gauntlet：伤害与近战速度 10%→12%，继承 Titan Glove 与 Magma Stone 新特性 (→ Item.cs)
- Honey Comb 系列（Bee Cloak、Honey Balloon、Stinger Necklace、Sweetheart Necklace）：蜜蜂基础伤害 7→13（配 Hive Pack 为 18）；Expert ×1.5、Master ×2；被击中时获得 5 秒蜂蜜增益 (→ Item.cs, Projectile.cs, BuffID.cs)
- Jellyfish Necklace 及制品：出水时散发光晕，水中大幅增亮 (→ Item.cs, Main.cs)
- Lava Charm：生成率翻倍，熔岩层箱/熔岩匣 1/20 几率 (→ ItemDropRules, WorldGen.cs)
- Magma Stone：特版 On Fire 4 DPS→15 DPS (→ Item.cs, BuffID.cs)
- Molten Quiver：木箭转火矢时正确给 +2 伤害（仅对木箭生效）(→ Item.cs, Player.cs)
- Obsidian Rose：熔岩伤害减免 30→45（适用所有制品，并纳入 Lava Waders/Hellfire Treads/Terraspark Boots）；熔岩伤害改用独立免伤计时器 (→ Item.cs, Player.cs)
- Panic Necklace / Sweetheart Necklace：Panic! 增益持续 5 秒→8 秒 (→ Item.cs, BuffID.cs)
- Pygmy Necklace：Witch Doctor 在 pre-Hardmode 即出售 (→ NPC.cs)
- Star Cloak / Bee Cloak / Star Veil / Mana Cloak：星星基础伤害 30→75，忽略至多 25 防御；Expert ×2、Master ×3；改用本地免伤帧，不干扰其他穿透弹幕 (→ Item.cs, Projectile.cs)

### 【物品与数值平衡 — 工具与坐骑】

- Reaver Shark：Use Time 18→13；Bone Pickaxe：掉落率 2%→5% (→ Item.cs, ItemDropRules)
- Chlorophyte Jackhammer：纳入钻头/链锯机制大改，速度提高、射程降低 (→ Item.cs, Projectile.cs)
- 钓鱼竿：Mechanic's Rod 钓力 30%→35%、机械师救出即售、多个月相有售；Fiberglass Fishing Pole 钓力 27%→30%、箱中几率 1/30→1/15；Scarab Fishing Rod 钓力 25%→30%；Sitting Duck's Fishing Pole 改为旅行商人只在骷髅王后出售 (→ Item.cs, NPC.cs)
- 生命法杖：Living Wood Wand / Leaf Wand 摇纯净森林树 1/300 掉落；Living Mahogany Wand / Rich Mahogany Leaf Wand 摇丛林树 1/200 掉落 (→ ItemDropRules, Player.cs)
- The Black Spot 坐骑：最高速度与加速度大幅降低（低于 UFO 坐骑）；不能靠 dash-骑乘直接达最高速 (→ Mount.cs, Item.cs)
- Scutlix 坐骑：攻击范围 500→850（性能折衷）；伤害 100→150 (→ Mount.cs, Item.cs)
- Dark Mage's Tome 坐骑：可像飞毯一样爬斜坡和 1 格高障碍 (→ Mount.cs)
- Witch's Broom 速度略增；Flamingo 坐骑最高速度 7.5→6；三种 pre-Hardmode 马鞍（Dusty Rawhide/Royal Gilded/Black Studded）最高速度 8→9 (→ Mount.cs, Item.cs)
- 光宠：Jewel of Light / Pumpkin Scented Candle 亮度约 +50%；Suspicious Looking Tentacle 亮度约 +33% (→ Item.cs, Main.cs)

### 【物品与数值平衡 — 合成与掉落】

- Blood Rain Bow / Chum Caster / Vampire Frog Staff：原为三选一各 1/8，改为各自独立 1/8 掉落（实际掉率 ×3）(→ ItemDropRules)
- Bloody Tear：标准血月怪 1/200→1/100；血月钓鱼怪 1/200→1/25；The Groom/The Bride 1/9→1/5；Dreadnautilus 1/9→1/2（Expert/Master 100%）(→ ItemDropRules)
- Sanguine Staff：Dreadnautilus 掉落 1/5→1/2（Expert/Master 100%）(→ ItemDropRules)
- Blade Staff：改由 Queen Slime 掉落（原附魔剑）(→ ItemDropRules)
- 风筝/纸飞机：Windy Balloon Slime 掉落的风筝掉率约 ×3（wiki 记 1/260→1/72）；Paper Airplanes 掉率基本不变，但改为小堆叠掉落（wiki 记堆叠 1→2–5）；Bone Serpent Kite 掉率 4%→6%（wiki 记 1/25→1/15，取整差异）(→ ItemDropRules)
- Sturdy Fossil：Tomb Crawler 有几率掉少量；Basilisk 1/3→100%、数量 1→1–3；绿洲/幻象匣可开出 (→ ItemDropRules)
- Golden Lock Box：修正 Muramasa 掉率双倍问题；现在可开出 Valor (→ ItemDropRules)
- 火把：丛林火把配方更高效；身上火把少于 20 个时打罐更易掉火把 (→ Recipe.cs)
- Mana Crystal：配方从 3 颗坠落之星增加到 5 颗 (→ Recipe.cs)
- 早期矿石装备成本全面下调（铜/锡/铁/铅/银/钨/金/铂）：镐 12→10（铜锡 8）；斧 9→8（铜锡 6）；铜锡阔剑 8→6；短剑 7→6（铜锡 5）；锤 10→8；弓不变；铜/锡盔甲 15/25/20 锭→12/20/16；铁铅与银钨 20/30/25→15/25/20；金铂 25/35/30→20/30/25 (→ Recipe.cs)
- Hardmode 矿剑：钴/秘银剑 10→8 锭；钯金/山铜剑 12→10 锭 (→ Recipe.cs)
- Adamantite Bar / Titanium Bar：5 矿→4 矿，连带所有相关装备降价 (→ Recipe.cs)
- Jester's Arrow：每颗坠落之星产 20 支→10 支；Super Star Shooter：不再由旅行商人出售，改为 Star Cannon + 神圣锭制作 (→ Recipe.cs, Item.cs)

### 【机制系统改动 — Buff/Debuff】

- Frostburn：玩家版改为与敌人版一致，8 DPS (→ BuffID.cs, Player.cs)
- Cursed Inferno：纠正 1.4 的错误解读，敌人版现在正确造成 24 DPS（玩家承受仍为 12）(→ BuffID.cs, NPC.cs)
- Venom 更名 Acid Venom：纠正后正确造成 30 DPS（玩家承受 15）；免疫大改：免疫 Poison 的敌人不再必然免疫 Acid Venom，且它通常影响不死/石头/金属/有毒敌人 (→ BuffID.cs, NPC.cs)
- Ichor：防御减免 20→15 (→ BuffID.cs, NPC.cs)
- Oiled：不再使用单独的 On Fire 类 debuff，而是目标已有其中之一时直接 +25 DPS (→ BuffID.cs, NPC.cs)
- Thorns Potion：荆棘反伤从所受伤害 1/3→100%；Dryad's Blessing：20%→50% (→ Item.cs, BuffID.cs, Player.cs)
- 敌人 debuff 免疫大改（数百项）：总体让敌人更易受以前免疫的 debuff 影响；绝大多数免疫 Venom 的敌人不再免疫；大量石头/金属敌人不再免疫 Cursed Inferno；Cursed Inferno 与 Shadowflame 免疫解耦；幽灵类敌人（Wraith、Poltergeist 等）几乎免疫所有主要 debuff（含 Ichor，鞭子 debuff 除外）；南瓜月/星旋入侵等"全免疫"敌人改为按属性免疫；Destroyer 等有意全免疫者不再免疫鞭子 debuff；绝大多数免疫困惑的敌人维持免疫 (→ NPC.cs, Terraria.ID/BuffID.cs)

### 【NPC与Boss与AI】

- Vicious Goldfish：现在在猩红水中自然生成 (→ NPC.cs, Main.cs)
- Blood Feeder：生命 20→150，伤害 30→50，防御 4→20，掉钱 350→500 (→ NPC.cs)
- Ghost：生命 70→50，伤害 18→15，防御 8→4，击退易感性 40%→50% (→ NPC.cs)
- Antlion Larva：生命 45→35，伤害 12→10 (→ NPC.cs)
- Antlion Eggs：世界生成时更少（地下沙漠危险性略降）；会随时间缓慢再生（区域低于阈值才再生）(→ WorldGen.cs, TileID.cs)
- Rolling Cactus：巨石基础伤害降低约 1/3；仙人掌刺弹幕伤害 20→30 (→ Projectile.cs, NPC.cs)
- Angry Dandelion / Rock Golem：修正弹幕伤害被放大两倍的 bug (→ NPC.cs, Projectile.cs)
- Wall of Flesh：会让屏幕褪色为黑色；附近所有玩家死亡或无玩家时消失 (→ NPC.cs, Main.cs)
- Ice Elemental：弹幕攻击可造成 Frostburn (→ NPC.cs)
- Jungle Creeper：生命 120→400，防御 14→40，伤害 50→100；移速更快；攻击造成 Venom；Expert/Master 下喷网 (→ NPC.cs)
- Lac/Cyan/Cochineal Beetle：生命体分析仪稀有度 1→2（降低优先级，不再抢在 Lost Girl 等更稀有敌人之前显示）(→ NPC.cs, Main.cs)
- Phantasm Dragon：生命 4000→10000，头部防御 10→15，身体尾部防御 20→30，头部伤害 80→100，身体尾部伤害 40→50 (→ NPC.cs)
- Hoppin' Jack：Hardmode 全年可在墓地区生成 (→ NPC.cs)
- Vortex Lightning：星旋入侵期间两种闪电伤害均提升到 100 (→ Projectile.cs)
- Town Happiness 机制（官方三处改动）：喜欢/反感/喜爱/讨厌因素加减成提升 20%；"So Much Space"（空间充裕）加成减半；不触发"拥挤"的城镇 NPC 数 3→4（拥挤惩罚起点更低、随人数增长更快）；城镇检测尺寸翻倍（1.4.1.2 会回调检测尺寸）(→ NPC.cs, Main.cs)

### 【世界生成】

- 世界生成会尝试避免 Corruption/Crimson 与 Jungle 重叠（不适用于 Hardmode 感染条带）(→ WorldGen.cs, GameContent/Biomes)
- Armed Zombie / Bone Skeleton Statue 现在任意世界难度都可能在世界生成中出现并正常工作 (→ WorldGen.cs)
- Shadow Chests 数量上限 7–10→10–15 (→ WorldGen.cs)
- Pyramid 放置几率 +50%；Enchanted Sword Shrine 生成几率翻倍（单次尝试 1/4→1/2）(→ WorldGen.cs, GameContent/Biomes)
- Sandstorm 频率：Hardmode ×2，pre-Hardmode ×1.33 (→ Main.cs)
- 修复丛林神社会阻止其东侧生成许多重要建筑（生命红木树、地下小屋等）(→ WorldGen.cs)
- 修正压力板生成在可破坏冰上漂浮、巨石陷阱嵌进神庙、罐子罕见出界、红木树不把丛林草视为丛林等问题 (→ WorldGen.cs)

### 【渲染与视觉特效 — Vanity 系统大改】

- 背部装备（背包、尾巴、翅膀、披风）不再互斥，四类各一件可同时显示（原一次只见一件）(→ Player.cs, Terraria.GameContent.Drawing/TileDrawing.cs)
- Combat Wrench 作为背部独立分类，无论其他背包如何总显示 (→ Player.cs)
- Angel Halo 像 Unicorn Horn 一样无视头部装备总可见 (→ Player.cs)
- 头部饰品细分多个子分组，可同时佩戴多个（眼睛栏 Blindfold/Spectre Goggles、花栏 Nature's Gift/Obsidian Rose、Ginger Beard 等）(→ Player.cs)
- 戴露脸帽子/头盔时可见 Blindfold；Diving Helmet 系列设为可见时覆盖头盔；Obsidian Skull 系列与露脸帽兼容并将脸替换为骷髅头；Ginger Beard 重画并兼容大多数头/脸饰品 (→ Player.cs)
- 盾/披风显示重做：盾绘制在披风"前面"，二者视觉上重新兼容；设为不可见的盾仍可染色，主动使用（克盾冲刺、狱火之刃格挡）时显示染色效果 (→ Player.cs)
- 玩家长发正确兼容翅膀/背包，显示全长不截断 (→ Player.cs)
- 各类奔跑靴（Sailfish/Flurry/Flower Boots 等）尾迹受 vanity 使用影响，可重排饰品栏或用社交栏选择 (→ Player.cs)
- 戴 Ultrabright Helmet 时可见头发；Bone Glove 手部新增视觉装饰 (→ Player.cs)
- Boss Mask 物品贴图更新；Orange/Amber Phasesaber 贴图更新 (→ Item.cs)

### 【UI与界面】

- Journey Mode 复制菜单大改：新增多个过滤器分解大类；其他选项更正确地包含不属于所有类别的物品 (→ Terraria.GameContent.UI, Main.cs)
- Bestiary 现在说明霜月/南瓜月掉落是否基于波数或特定波数后掉落 (→ Terraria.GameContent.UI)
- 连接服务器时显示加载 Tips (→ Terraria.GameContent.UI)
- 分辨率/全屏/无边框菜单设置重组为同一子菜单 (→ Terraria.GameContent.UI)
- 修正向导合成栏/哥布林重铸槽未正确链接玩家、天柱血条 Journey 难度切换时溢出、Quick Stack 不考虑已收藏钱币、Journey 滑块滑动中关闭会最大化、时间暂停时自发下雨/入侵宣告、boss 小地图图标不随方向改变等 (→ Terraria.GameContent.UI, Main.cs)

### 【音频】

- 打雷音量改用环境音效设置调整 (→ Terraria/Audio)
- Torch God 相应设置开启时播放异界版曲子；音乐音量为 0 时音乐盒不再播放 (→ Terraria/Audio)
- 修正音轨用 60% 而非 100% 质量压缩的问题（地下沙漠曲最明显）；修正火星人大量 SFX 问题 (→ Terraria/Audio)

### 【机制系统改动 — 其他】

- 墓地阈值：触发各级墓地氛围所需墓碑数量 +1 (→ Main.cs, Player.cs)
- Block Swap 与坠落块：可对最顶一块沙/坠落块换块；镐力足够（钴及以上）可自由对任何坠落块换块 (→ Player.cs, Main.cs)
- Meteorite 矿：Hardmode 后可被爆炸物破坏（原免疫）(→ Main.cs, TileID.cs)
- 常规橙色蘑菇：药水病时长 60 秒→30 秒 (→ Item.cs, Player.cs)
- 钓鱼：移除高钓力时的收益递减 (→ Projectile.cs, Player.cs)
- 晶塔（Pylons）：星旋入侵期间可用晶塔传送（Moon Lord 与其他入侵/Boss 战仍不可用）(→ Main.cs, Player.cs)
- Journey Mode 开局自带基础抓钩 (→ Player.cs)
- 摇树获取掉落物次数上限 200→500/天 (→ Player.cs)
- 特殊家具制作站：蒸汽朋克人在对应生物群落出售大多数特殊制作站（雪地=制冰机、太空=天磨等）；Bone Welder 在墓地区出售；带生命木法杖时出售 Living Loom；邪恶世界两种邪恶制作站可用暗影之魂在墓地区互转 (→ NPC.cs, Recipe.cs)
- Bestiary：有独立图鉴的 Boss 仆从在打败对应 Boss 后完全解锁；Dark Mage 和 Ogre 只需打败一次即完全解锁 (→ Terraria.GameContent.UI)
- Rock Lobster 卖价 20 银→10 银 (→ Item.cs)
- Sakura/Yellow Willow Saplings 价格 3 金→1 金 (→ Item.cs)
- Mirage Fish / Pixie Fish 稀有度 rare→uncommon，与其他任务鱼一致 (→ Item.cs, Player.cs)
- Sharpening Station（磨刀站）：Hardmode 后由 Merchant 出售 (→ NPC.cs)
- Books：Wizard 开始出售书籍，价格 3 银→15 银 (→ NPC.cs, Item.cs)
- 1/3/5 秒计时器：除合成外也由 Mechanic 出售 (→ NPC.cs)
- 平台层：SteelSeries 外设 RGB、FNA 更新、全语言本地化（复刻可忽略）

### 【多人/网络】

- 修正 Queen Bee 多人同步问题（冲锋/传送不稳）、Big Mimic 同步、多人只伤双子之一时宝藏袋不掉、Flying Dutchman 失同步/自发死亡、Moon Lord 某攻击多人中异常、水晶碎片多人放置同步错误（变明胶水晶）、木人模特/帽架多人被炸坏、世界最右边缘出生点不工作等 (→ NPC.cs, Main.cs, MessageBuffer/Netplay)
- 服务器：独立服务器生成世界不遵循名称/种子长度限制、不能用特殊种子、生成的世界偶尔损坏；最大玩家数可设超 255 或低于 1；"Liquid Spam"改为正确计数后才踢人；玩家不捡物品时服务器无限塞物品 (→ NetMessage/Netplay)

### 【Bug修复-影响玩法逻辑的】

- 纯崩溃/平台类（滚动备份删除、地图图标崩溃、坐骑动画罕见崩溃、剪贴板崩溃、云端存档同步、分辨率上限、关闭挂起、Mac 主机崩溃、Linux 截图）归并一句：修复大量崩溃与 Mac/Linux 平台问题。
- NPC/Boss：白天击杀光之女皇不掉 Terraprisma；克苏鲁之眼/双子转二阶段有几率永远旋转；拜月教邪教徒与火星飞碟目标离开/死亡不寻找新目标；Antlion Swarmer 掉 10 倍金钱笔误；Angry Nimbus 无法穿平台；打败史莱姆皇后双倍提升城镇 NPC 能力而光之女皇完全不提升；漂浮类敌人（Pixies、Wraiths 等）无法上下穿平台；地表木质 Mimic 不再自然生成；旧日军团 2 级哥布林投弹手造成 1 级伤害；史莱姆雨无视 Journey 生成滑块；Devourer 身体/尾巴击杀不计旗帜计数；挖掘中的松露虫不显示在生命体分析仪；Hemogoblin Shark 穿平台掉落；蜘蛛行走动画帧不全；Golem 部位生成外观古怪；Moon Lord 不再使用 NPC 平滑设置；Torch God 双倍计数/死亡不失去进度；腐化/猩红无效房屋只说"无效"；Angry Dandelion 多人瞄错玩家；时间暂停时旅行商人生成；海洋小动物屏幕内生成 (→ NPC.cs, Main.cs, Projectile.cs)
- 战斗/物品使用：鞭子大小词缀反向影响速度；Blood Arrow 不被视为远程（不暴击）；沙漠之虎突袭被算作魔法攻击（不触发鞭子 debuff）；高尔夫球车撞击不随仆从伤害缩放；马坐骑撞击错误随近战伤害缩放；Expert/Master 服务器幸运币掉钱；Terraprisma 传送远处返回慢；钛金远程套未公开的不耗弹药几率；Bat Scepter/Bee Gun 不瞄准猪鲨；黄蜂/小鬼/风暴/UFO/星尘细胞仆从不造成击退；沙滩球无速度上限；Life Drain 命中检测；Celestial Starboard 飞行时大幅缩短冲刺距离；雪地传送到非雪地水中染 Chilled；雪人集群碎片不造成伤害/不破坏图格；躲闪掉的攻击仍上 debuff；Magic Missile 类液体中穿墙；背包满时捕成组鱼（炸弹鱼/霜匕首鱼）删除原物品组；Journey/Expert 模式 debuff 时间未正确倍增；Dart Pistol 两个可能的 Deadly 词缀；Sanguine Staff/Terraprisma 不正确使用召唤锁定；Golden Lock Box 中 Valor 不正确掉落 (→ Item.cs, Projectile.cs, Player.cs, NPC.cs)
- 图格/方块：竹子与熟铁栅栏不允许树木生长；沙子相关欺骗行为；Block Swap 悬停 Logic Sensors 可能破坏它们；环境改造不转化恶性蘑菇；邪恶荆棘世界生成后停止生长；珊瑚/贝壳在被致动块上重新长出；恶魔祭坛可能生成在滚球仙人掌上；绳不再与平滑大理石块融合；丛林/蘑菇藤蔓地下不生长；多人移除武器架；制作抓钩会暂时允许手动使用；坠落块穿过的平台失去斜坡状态；不能在硬核玩家幽灵背后放置图格；沙子图格形式坠落时偶尔复制；蓝色传送门站上使用彩纸会发射彩纸；压力板生成在可破坏冰上；巨石陷阱嵌进神庙；无法从各种梁向外延伸建造；石平台免疫熔岩；泥土炸弹不让埋住的草死亡；晶塔 NPC 检测只查住房旗号；智能光标药草放置不一致 (→ Main.cs, WorldGen.cs, TileID.cs, Player.cs)
- 视觉/美术（择要）：Mac/Linux 能看到顶点着色器尾迹（Zenith、Terraprisma、Magic Missile）；披风与税官西装坐下时正确隐藏；沙漠之虎突袭不用召唤染料；矿车尘土用错染料槽；死亡后仍显示翅膀；反向重力身体部位位置错误；部分图格忽略光照涂料；暂停时星尘守卫停止攻击动画 (→ Terraria.GameContent.Drawing/TileDrawing.cs, Main.cs, Player.cs)

---

## 二、版本 1.4.1.1（修补程序，2020-10-14）

> 以 1.4.1 的 bug 修复为主。纯崩溃类（Mac 多人主机崩溃、手柄房屋菜单崩溃、Linux 截图失败）归并一句：修复了 Mac/Linux 多处崩溃与截图问题。

### 【机制系统改动】

- 修正 "Leading Landlord" 成就所需 NPC 快乐度获得难度高于预期的问题 (→ Terraria.GameContent.UI, NPC.cs)
- Moon Lord：眼睛闭上时，插在眼中的 Daybreak 长矛会立即爆炸并造成额外伤害 (→ Projectile.cs, NPC.cs)
- 修正 Dungeon 代码中导致同一种子每次生成世界不同的问题 (→ WorldGen.cs)
- Master 模式玩家用手柄时无法使用全部饰品栏 (→ Terraria.GameContent.UI, Player.cs)

### 【NPC与Boss与AI】

- Princess：修正不能正确检测附近 NPC 的问题（邻居簇拥她也觉得孤独）；修正关于 Santa Claus 的一条对话；变身后的 Zoologist 关于 Princess 的一条对话 (→ NPC.cs)
- Town NPC 会试图坐在 Dynasty Chair 上（应当无法坐上去）(→ NPC.cs)

### 【物品与数值平衡】

- 修正 Jungle Armor、Ancient Cobalt armor、Molten Armor 套装未拥有正确套装奖励、反而由 Band of Regeneration 等其他物品获得的问题 (→ Item.cs, Player.cs)
- Bone Glove：修正无法通过背包内右键点击装备、必须手动装备的问题 (→ Item.cs, Player.cs)

### 【渲染与视觉特效】

- 变身为 Werewolf/Merman（Celestial Shell）的玩家不再因佩戴某些饰品而拥有人脸 (→ Player.cs)
- Video Visage 显示在地图上时未给屏幕部分应用染料 (→ Terraria.GameContent.Drawing/TileDrawing.cs)
- Witch Costume 未能正确显示其下双腿 (→ Player.cs)
- 修正 Game Credits 中的疏漏 (→ Terraria.GameContent.UI)

### 【其他】

- 任意液体中钓鱼都会解锁 "Hot Reels!" 成就的 bug (→ Terraria.GameContent.UI)
- 修正汉字键会自动替换某些键位绑定的问题 (→ Terraria.GameContent.UI)
- 修正重命名箱子时玩家无法轻松关闭背包的问题 (→ Terraria.GameContent.UI)
- NPC 对话、物品 tooltip/背景文本的若干语法/拼写问题（本地化资源）

---

## 三、版本 1.4.1.2（修补程序，2020-11-10）

### 【新增内容】

- 无新增游戏内容；本地化内容补齐（1.4.1 内容全部翻译入包，并修正 1.4 中文本地化无法正确加入游戏的问题）。

### 【机制系统改动】

- 还原 Town NPC 住房/村庄检查距离：1.4.1 中曾翻倍，现回到 1.4 水平 (→ NPC.cs, Main.cs)
- NPC 快乐度：3 个 NPC 的城镇现在给予"Space（空间）"奖励（之前既无奖励也无惩罚）(→ NPC.cs)
- Skeletron Prime 的炸弹现在会在种植箱（Planter Boxes）上爆炸（类似此前对平台的改动）(→ Projectile.cs, TileID.cs)
- Queen Slime 的仆从现在以正常掉落率掉落 Slime Staff (→ ItemDropRules)
- 坐着或骑坐骑时也显示披风（此前因冲突受限）(→ Player.cs)
- Journey/图鉴菜单任意位置点击会暂停搜索 (→ Terraria.GameContent.UI)
- Timeless Traveler 套装贴图更新为正确版本；Spectre Goggles 不再完全覆盖头盔 (→ Item.cs, Player.cs)

### 【物品与数值平衡 — 对 1.4.1 的回调与二次调整】

- Brand of the Inferno：Use Time 25→20 (→ Item.cs)
- Chlorophyte Claymore：伤害 80→95；Chlorophyte Saber：伤害 48→57 (→ Item.cs)
- Christmas Tree Sword：弹幕造成 75% 基础伤害（原 50%）(→ Projectile.cs)
- Super Star Shooter：Use Time 12→18，伤害 70→60（因免伤帧机制实际总伤更一致，官方称实际为强化）(→ Item.cs, Projectile.cs)
- Betsy's Wrath：部分还原 1.4.1 强化，伤害 110→100 (→ Item.cs)
- Hornet Staff：伤害 11→12（在 1.4.1 从 9→11 基础上）；Vampire Frog Staff：还原 1.4.1 强化，伤害 13→11（AI/功能改动已足够）(→ Item.cs)
- Imp Staff：小鬼攻击的敌人免伤帧 10→6；Optic Staff：Spazmamini/Retinamini 免伤帧 16→12，Spazmamini 追敌移速提高 (→ Projectile.cs)
- Spider Staff：召唤蜘蛛改为按顺序系统性轮换种类而非随机（免伤帧机制下伤害更一致，最大潜力不变）(→ Projectile.cs)
- Obsidian armor：头盔/护腿仆从伤害 9%→8%/件；套装奖励仆从伤害 25%→15%；鞭速 50%→35% (→ Item.cs)
- Deadly Sphere Staff：攻击免伤帧 10→8 (→ Projectile.cs)
- Firecracker：爆炸伤害 3 倍仆从基础伤害→2.75 倍 (→ Projectile.cs)
- Cool Whip：命中时短时间造成 Frostburn；雪花仆从移速 +50% (→ Projectile.cs, BuffID.cs)
- Desert Tiger：目标在空中时会"反弹至"目标，维持更牢固锁定；每扩展一个仆从位的伤害缩放 33%→40% 基础伤害 (→ Projectile.cs)
- Rainbow Crystal Staff：部分还原 1.4 的伤害下调，伤害 80→130 (→ Item.cs)
- Celestial Starboard：操作手感调整，保留完整冲刺距离修正 (→ Item.cs, Player.cs)
- Star Cloak：只在受到来自敌人源的伤害时才产生星星 (→ Item.cs, Player.cs)
- Black Spot 坐骑：加速度略升，略为抵消 1.4.1 的总速度损失 (→ Mount.cs)
- Chlorophyte Bar：配方 6 矿→5 矿；Chlorophyte Bullet：每锭 70 发→60 发 (→ Recipe.cs)
- 未说明更改："Gypsy Robe" 更名为 "Mystic Robe" (→ Item.cs)

### 【NPC与Boss与AI — 敌人 debuff 免疫调整】

- Snow Flinx、Wall of Flesh：移除对 Poisoned 的免疫 (→ NPC.cs, BuffID.cs)
- Queen Bee、Mourning Wood、Twins、Martian Probe、Old One's Skeleton：新增对 Poisoned 的免疫 (→ NPC.cs)
- Granite Golem / Granite Elemental、Betsy：新增对 On Fire!/Hellfire 的免疫 (→ NPC.cs)
- Frozen Zombie：新增对 Frostburn 的免疫；Clinger：新增对 Cursed Inferno 的免疫 (→ NPC.cs)

### 【Bug修复-影响玩法逻辑的】

- 纯崩溃类（音乐音量无法提高到 0% 以上及关联启动崩溃、Credits 贴图包崩溃、Prismatic Lacewing 贴图致 Linux 严重问题、Clinger Staff 反向重力世界顶部崩溃等）归并一句。
- 快乐度值被严重向下取整，消除微小差异并使阈值更难达成；只有 1 个 NPC 时拥挤惩罚与 3 个 NPC 一样 (→ NPC.cs)
- Life Drain 在 PVP 中使用不消耗魔力 (→ Item.cs, Player.cs)
- Town NPC 夜间不传送进入过高/瘦房屋或椅子上方空间不足的房屋；Town NPC 仅当敌人可作为目标时才对其开火（不再对 Plantera Hook 之类开火）；NPC 和猫夜间可能坐在同一座位 (→ NPC.cs)
- 碎裂地牢砖同步问题（应能解决地牢中敌人传送）(→ Main.cs, TileID.cs)
- Journey 模式提高时间速率会让主菜单 Credits 跑得特别快；Credits 暂停时也滚动 (→ Terraria.GameContent.UI)
- Ronin set（Wandering set）女性角色不显示萤火虫；某些情况下（如部分光宠）玩家皮肤过亮；Reaper Hood 头部贴图一帧偏移；Robot Shirt 与手部/腰带饰品不兼容、Pumpkin Shirt 与腰带饰品不兼容 (→ Player.cs, Item.cs)
- Video Visage 屏幕反向重力时偏移；某些 vanity 耳朵坐下时背后耳朵位置错误；坐下时尾巴饰品高度不正确、某些发型"双重绘制"、骑坐骑时高帽子视觉问题 (→ Player.cs)
- Bamboo Lantern 视觉分帧；Stardust Guardian 染色后不再透明；某些小动物在水下超级跳；虚荣火箭靴尾迹优先级不一致 (→ Terraria.GameContent.Drawing/TileDrawing.cs, Projectile.cs, Player.cs)
- Bone 仍被标记为弹药；Luminite 钻头/链锯取得不该取得的词缀；Jousting Lance 不再获得近战速度词缀；Old One's Army 盔甲属性与 tooltip 不一致；Hero Shield 未带来仇恨（aggro）加成；Sky Dragon's Fury 落地无动画、二次火焰不造成 Flask debuff；瓶中魂缺动画帧；发型 6/94 与披风冲突 (→ Item.cs, Projectile.cs, Player.cs)
- 强行传送其他玩家的漏洞（多人/网络）(→ Main.cs, NetMessage)
- 成就菜单不自动暂停；手柄 Master Mode 栏位可见性切换不工作；手柄/WASD 在角色难度模式中循环滚动方向反向 (→ Terraria.GameContent.UI)
- Adamantite/Titanium 矿锭制作花费变动带来的卖出价不一致；Paper Airplane 弹幕未被视为远程、不正确并堆；Molotov Cocktail 未获得霜甲 Frostburn；Coin Gun 不优先使用钱币栏 (→ Item.cs, Projectile.cs, Player.cs)
- 某些头盔反向重力时小地图绘制错误；某些叶贴图不能正确处理油漆 (→ Terraria.GameContent.Drawing/TileDrawing.cs)
- Brain of Cthulhu 没有足够空间传送时会消失 (→ NPC.cs)
- 部分物品掉落率未正确受 luck 影响（多为 Old One's Army 掉落，对实际掉率影响不大）(→ ItemDropRules)
- 除普通沙外大多数坠落图格弹幕会穿过平台，现在除敌对沙球外全部落在平台上 (→ Projectile.cs)
- 蜂巢、兔子炮、蚁狮蛋相关漏洞/疏忽；敌对蜜蜂会攻击神秘石碑等无敌敌人 (→ Item.cs, Projectile.cs, NPC.cs)
- 大纹理物品聊天中被缩小两次 (→ Terraria.GameContent.UI)
- 某些贴图大小未更新导致外观贴图的 texture packs 无法工作 (→ Main.cs)

---

## 四、本版本改动规模评估

### 涉及独立系统数量

1.4.1 系列合计涉及约 20 个独立系统：物品数值（近战/远程/魔法/召唤四大类全覆盖）、盔甲套装（30+ 套）、饰品、合成配方、掉落表、Buff/Debuff 体系（含敌人 debuff 免疫数百项的系统性重排）、召唤/仆从 AI 与免伤帧机制、敌人与 Boss 数值/AI、坐骑、钓鱼、城镇快乐度、墓地生物群落、世界生成（结构放置率/生物群落避让）、Vanity 渲染分层（背部/头部饰品分组）、Journey 模式 UI、Credits/音频、图格与坠落块机制、多人同步、成就与图鉴。

### 复刻项目必须跟进的核心改动

1. 免伤帧（immune frame）与穿透惩罚体系：大量弹药/仆从改为"每穿透一敌下一次命中伤害惩罚 X%"并使用独立/本地免伤计时器（Meteor Shot、High Velocity Bullet、Frost Hydra、星星、蜜蜂，以及 Imp 10→6、Optic 16→12、Deadly Sphere 10→8 等具体免伤帧数字）。这是 Projectile 命中逻辑的底层机制，复刻若不做会导致召唤与穿透武器手感完全不对。(→ Terraria/Projectile.cs, Terraria/Player.cs)
2. 敌人 debuff 免疫大改 + Venom→Acid Venom 重命名：数百项 NPC 免疫标志变化、Cursed Inferno/Venom 的 DPS 纠错（24/30）、Ichor 减防 20→15、Oiled 机制重做、1.4.1.2 又加了约 10 个敌人的具体免疫调整。数据驱动 NPC 的 debuffImmune 表必须按 1.4.1.2 后版本重建。(→ Terraria/NPC.cs, Terraria.ID/BuffID.cs)
3. 物品数值全量刷新：本系列是 1.4.x 中最大的平衡性补丁，Item.SetDefaults 中几乎全部近战/远程/魔法武器、30+ 套盔甲、大量饰品数值都变了（Terra Blade 95→115/UT14、Arkhalis 20→25、Betsy's Wrath 65→110 后回调至 100 等）。若复刻目标为 1.4.5.6，直接以 1.4.1.2 后的数值表为准即可，不必逐步还原中间态。(→ Terraria/Item.cs, Terraria.ID/ItemID.cs)
4. 配方与掉落表大改：Terra Blade 合成线重构（真剑不再需要 Broken Hero Sword）、Adamantite/Titanium 锭 5→4 矿（1.4.1.2 又调叶绿锭 6→5）、早期矿装全面降价、Mana Crystal 3→5 星、Super Star Shooter/Blade Staff/Lucky Horseshoe 等来源变更、Bloody Tear/Sanguine Staff 掉率提升。(→ Terraria/Recipe.cs, Terraria.GameContent/ItemDropRules)
5. Princess NPC + 早期召唤内容：新城镇 NPC 公主（及其快乐度关系网）、Flinx Fur Coat/Flinx Staff、Spinal Tap、Lavaproof Tackle Bag。1.4.5.6 的 NPC 生成与快乐度计算依赖她。(→ Terraria/NPC.cs, Terraria.ID/NPCID.cs)
6. Vanity 渲染分组：背部四类（背包/尾巴/翅膀/披风）同时显示、头部饰品子分组、盾绘制在披风之前、坐下/骑乘时显示披风。玩家绘制管线需要对应的分层/兼容性矩阵。(→ Terraria/Player.cs, Terraria.GameContent.Drawing/TileDrawing.cs)
7. Town Happiness 参数（两连改）：1.4.1 加减成 ×1.2、拥挤阈值 3→4、检测距离翻倍；1.4.1.2 又把检测距离还原、给 3 NPC 城镇加空间奖励。快乐度公式必须按 1.4.1.2 后的最终态实现。(→ Terraria/NPC.cs, Terraria/Main.cs)
8. 世界生成参数微调：地牢种子确定性修复（1.4.1.1，WorldGen 种子消费顺序）、金字塔 +50%、附魔剑神龛 1/4→1/2、暗影箱 7-10→10-15、邪恶生物群落避让丛林、丛林神社东侧建筑 bug。105 pass 管线需按此校对。(→ Terraria/WorldGen.cs)

### 一句话总评

1.4.1 是"平衡性大补丁"：以数百项物品/敌人数值调整和 debuff 免疫体系重排为主体，附带公主 NPC、早期召唤装备等少量新内容；1.4.1.1/1.4.1.2 是纯修补程序，1.4.1.2 还对 1.4.1 的过量强化做了一轮回调（含快乐度参数两连改），复刻应以 1.4.1.2 之后的最终数值为准。

---

## 五、校验记录

已用官方 changelog.txt 反向核对，完整度约 90%，四大类武器平衡数值 100% 命中。

- 校验范围：官方 changelog.txt 第 4698–5991 行，即 Version 1.4.1.2 / 1.4.1.1 / 1.4.1 三个完整段落。
- 本次修订：更正 5 处数值/方向错误（Lac/Cyan/Cochineal Beetle 分析仪稀有度方向、Sky Dragon's Fury 新旧单发伤害、Orichalcum Mask 第二属性类型、Paper Airplanes 掉率口径、Queen Bee 多人同步误写 Queen Slime）；补漏 8 条（Plantero's Sombrero 回归、Town Happiness"So Much Space"加成减半、Rock Lobster/Saplings 降价、Mirage/Pixie Fish 稀有度、Sharpening Station/Books/Timers 出售来源）。
- 残余已知差异：官方 1.4.1 段约 182 条 bug 修复中约 30 条视觉/UI 琐碎项未逐条列出（沿用归并写法）；Basilisk Sturdy Fossil 掉率、Dart 枪绝对伤害值为 zh wiki 补充细节，官方日志无对应数字。
