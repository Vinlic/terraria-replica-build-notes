# 图鉴（Bestiary）数据层移植

- 数据层 `src/data/Bestiary.ts`：BestiaryTracker 三桶（杀数 Map/遇数 Set/聊天 Set，key=creditId）
  + 条目注册表（惰性 546 条，与原版总量吻合）+ UnlockState 四档 + completion()。
- 静态表 `src/data/bestiaryStatics.generated.ts`（tools/extract-bestiary.mjs 生成，源=Terarria1456）：
  BESTIARY_HIDE_IDS（216 条 GetExclusions）/ BESTIARY_CREDIT_REDIRECT（119 条 ModifyNPCIds 负 id 归并）
  / BESTIARY_KILLS_TO_FULL（68 条非默认阈值，链 NPCtoBanner→BannerToItem→KillsToBanner，默认 50）。
- 关键语义：
  - creditId = NPCID 名经 REDIRECT 归并（世吞身 14→头 13 等）；杀数按 netID 记（vanillaNetId）。
  - 解锁档：敌怪 1/full÷5/full÷2/full（quickUnlock=Boss 族杀 1 即满）；小动物=遇（首见置位）；
    城镇=聊天；金小动物另有"任一金种已见"全图门；68/35/37/534/小动物对=多来源取 max。
  - 遇数语义 = NPCWasNearPlayerTracker.ScanWorldForFinds：仅 CountsAsACritter
    （lifeMax≤5 && damage==0 && id∉{594,686}）与玩家盒（外扩 300×200，Player.cs:3165）相交，
    每 tick 扫（Game.fixedUpdate）。
- 消费点：动物学家（zoologist）入住门 = completion().percent >= 0.1（Main.cs:65375，
  原 bestiaryTenPercent 门旗已删）。杀数接 Game.onEnemyKilled（IsNPCValidForBestiaryKillCredit
  1:1：121 不计、EoW 13/14/15 需 boss 旗；GetWereThereAnyInteractions 未接——hurt 无伤害源）。
- 持久化：原版是世界侧（IPersistentPerWorldContent，WorldFile.cs:3399/3405）——World.bestiary
  + SaveData/SaveMeta.bestiary + WorldPacket.bestiary（worker 读档路径 packWorld/fromPacket 均带）。
- 偏差面：负 id 变体小动物按敌怪条目分类（vanilla-npcs.json 无负 id 段）；多人 NetBestiaryModule
  未接（房间制 host 权威，图鉴随宿主世界）；成就 TryGrantingBestiary100PercentAchievement 无成就系统未接。
- UI 二期：全屏图鉴面板（vui/ 或 DOM）未做——数据层已全，直接消费 bestiaryEntries()+tracker。
- 测试 tests/bestiary.test.ts 8 探针（档位/阈值/遇数聊天语义/金种门/注册表全量可达成/10% 门/存档往返）。
