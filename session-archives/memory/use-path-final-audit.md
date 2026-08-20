---
name: use-path-final-audit
description: 道具使用链终审:传送族/永久升级/桶/饰品装备死路径/迁移表冻结化;钩爪宠物坐骑信息饰品乐器为引擎级缺口
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-17T04:21:44.314Z
---

2026-08-13 道具接入终审(用户点名魔镜/回忆药水音效与回出生点):

- **传送族 1:1**(Player.cs:42297-42516):魔镜 50/手机 3124/冰镜 3199/贝壳手机 5358 引导 90t 半程 Spawn;回忆药水 2350 起始 **drink(SoundID.Item3)**+itemTime==20 触发 **mirror(SoundID.Item6)**+保留无敌帧+消耗;传送药水 2351 itemTime==2 随机传送;海螺 4263/5360 海洋·4819/5361 地狱(螺旋尘);5359 出生点。实现:Game.recallChannel 引导态+fireRecallTeleport+findTeleportSpot(1000 次掷点)。新 Sfx:mirror=Item_6/conch=Item_64;**drink 曾映射空数组走合成兜底——已修为 Item_3**。
- **永久升级族**(UpdatePermanentBoosters :44575-44802):恶魔之心 3335→Inventory.extraAccessory+**accSlotMax 动态饰栏**(基 5,心 +1;原实现 7 槽全开是超配);5337 神盾水晶回血爬坡×1.2/5338 神盾果防御+4/5339 奥术水晶(效果端早有)/5341 软糖虫渔力+3(Bobber)/5342 仙馔蜜酒挖掘×0.95;**存档 permanentUpgrades 段持久化**(serialize/SaveFile/applyPlayer 三处)。
- **特殊单品**:2756 性别药水(skinVariant 翻转,undefined 视作 0)、4870 回归药水(出生点近似,床 stash 缺)、678 红药水(13 buff 组)、1326 混乱之杖(chaosStateT 400t 冷却近似 debuff88+1/6 扣血)/5335 和谐之杖、5043 火把眷顾(world flags)、1133 蜂王召唤、4988 皇后水晶(困难+神圣+夜)、3601 天界印记(**接现成 tickMoonLordCountdown 体系**非自造计时器)。
- **桶族扩展**:3031 无限水桶(倒 255 不耗)/3032 超吸海绵(3×3 吸干不耗)。
- **两个死路径修复**:①vi_ 配饰一键装备(UI.swapEquipItem 只认 legacy accessory 字段→vi_ 配饰静默失效,改 statOfInternal acc 判定);②电线耗材 wire(ITEM_BY_KEY['wire'] 删除后解析 -1→铺线不耗料,改 VI_ID(530))。
- **★ 迁移表冻结化铁律**:RETIRED_KEY_TO_VID 原从 idNames.ITEM_KEY_TO_ID 派生——build-l10n 会从"当前注册表"再生成,本地键删除后即从表消失(578→419 实证断裂,v3 存档 armor remap 全灭)。已改为**冻结字面量**(与 PRIV_ITEM_STABLE 同级,永不重生成)。
- **引擎级缺口登记**(单轮无法 1:1,需新子系统):钩爪族(aiStyle7,装备链在 miscEquips[4] 无行为)/宠物+光源召唤物(miscEquips[0/1],无 PetProj)/坐骑全族(mountType,仅矿车)/信息饰品(EquipStats 无 depth/radar 字段族)/乐器演奏/虫网+瓶中小动物/5326 工匠面包·5343 商贩背包·宠物执照(商店系统深改)/5120 鹿角怪+5334 机械美杜沙召唤(boss 本体未实现)。
- 探针:`_useauditprobe.mjs`(9 项:魔镜/回忆音效+回出生点/恶魔心饰栏/双桶/混乱杖/性别/蜂王/天界印记)。

- **坠星整条贴图修复**(用户报障):Item_75.png 本体=22×208 竖 8 帧条,原版 RegisterItemAnimation(75, DrawAnimationVertical(5,8) **PingPong**)(Main.cs:3688)——物品动画(Main.InitializeItemAnimations :3685-3722 全表:3580/3581/75pingPong/547-549/520/521/575/3453-3455 各 6t×4 帧、4068-4070 NotActuallyAnimating 恒帧0、IsFood int.MaxValue 静态 3 帧、5644 水晶球 7t×9)。实现:SpriteAtlas `ITEM_ANIMATION`+`itemAnimFrame`+`sliceItemAnimFrame`;Renderer.atlasIcon 中央切片(animTick 逐帧推进,所有消费方 drawDrop/家具/held 自动修复);UI iconUrl 取帧 0(背包内原版也转——静态帧偏差已注)。坠星投射体改原版 Projectile_9.png(22×24,ensureVImage 懒载,旋转对齐速度向,程序星形降级为兜底)。**教训:物品图标矩形 ih 明显大于 iw 的都要怀疑多帧条**(TEdit Item_N 直接整图入 atlas)。

- **同类扫荡(食物族 86 项)**:全仓扫描图集纵横比异常 930 条——85+ 条是 IsFood(ItemID.cs:258 权威 86 项)竖 3 帧条,原版 `DrawAnimationVertical(int.MaxValue,3)` 恒帧 0;已批量注册 FOOD 静态切片(顶部 1/3)。剩余 850 条为合法长形图标(链锯/火枪/炸药/吹箭筒 38×8 等,原版整图直画)不处理。**其余贴图族逐一核验无同类问题**:投射体(projFrames 切帧,266 史莱姆随从先例)/月亮 8 相位/翅膀 7(6)帧/表情泡 34×28 格/旗帜(整图=用户实测校准)/链条按段切片/NPC_Head 单帧。判定口诀:异常纵横比 + 原版有动画注册表→切;原版 Frame() 整画→不切。

- **放置动作三件套补齐（2026-08-17，用户问"放置方块时原版也有动作?"）**：原版放块=①挥动动画（ItemCheck_StartActualUse :50911→ApplyItemAnimation :4255——**createTile 档 useAnimation×tileSpeed / createWall 档 ×wallSpeed** :4270-4275；动画周期独立于 itemTime,持键按 useAnimation 节拍循环,放置失败也照挥）②成功音=SoundID 0 Dig（TileObject 路 :39466 显式;legacy 路在 PlaceTile 内部——'place' 音效早已映射 Dig_1/2 无缺口）③ApplyItemTime（:39485→:4221-4230 useTime×tileSpeed 下限1,**仅成功时设置**）。本仓缺①+③（useTime 硬编码 14）。修：useSwing 加 mult 参数（SetItemAnimation :4240 语义）+三处放置分派点（墙/块左键+PlaceTileOnAltUse 右键）补 `if(!swing||swing.t<=1) useSwing(def,undefined,paintTileSpeed()/paintWallSpeed())` + tryPlace 成功尾 useTime=itemCombat.useTime×tileSpeed（泥土 10 非 14）。探针 `_placefx.mjs`：swing 循环✓首拍放置✓失败不耗冷却✓。**探针坑：目标格勿与玩家列重叠（原版禁覆盖玩家→放置静默失败）；物品 id 用 window.__swItems[key] 非 g.itemId（vi_ 键查不到返 undefined 会被 JSON 丢键）**。
