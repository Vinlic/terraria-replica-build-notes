---
name: explosion-family-port
description: 爆炸物族群 1:1（ExplodeTiles/CanExploteTile/半径表）+ 功能方块全量审计结论（双代理 2026-08-11）
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-11T09:16:33.782Z
---

# 爆炸物族群修复（2026-08-11，用户报"起爆炸药不破坏方块"）

**根因**：explodeAt 用 `d.pick < 0 || pick >= 200` 硬度启发式判可炸——`def()` 默认 pick:-1
导致大量 vi_ 块全被跳过；半径恒 3；无墙破坏；"不掉落"注释是错的（原版 KillTile 掉落）。

**修复**（Game.explodeAt 1:1 + devices + 手雷分支）：
- **半径表 cs:75262**（Game.EXPLODE_RADIUS）：炸弹族 28/37/516/519=4、炸药棍族 29/470/637=7、
  **放置炸药 tile141→proj108=10**；**手雷 30/地雷 164 不在 ExplodeTiles 判定表 = 不破坏地形**（纯伤害）
- **CanExploteTile cs:75764**（Game.canExplodeTile 静态纯函数）：永不可炸=tileDungeon{41,43,44,677-679}
  +BasicChest{21,467}+黑名单{26,88,121,122,150,211,226,237,248-250,346,470,475,504,685,686}+墙350；
  HM矿石{107,108,111,221-223}仅scarab弹(未引入恒false)；陨石37/狱石58肉前免疫；
  黑檀石77肉前地狱免疫(y≥lavaLine)；蜥蜴砖137石巨人前**仅神庙门行**(frameY/18∈1-4)免疫（flags['downed_245']）
- **墙破坏** ShouldWallExplode cs:75739：盘内任一格无墙→每格3×3清墙(≠350)
- 破坏走 breakTile（KillTile 全语义含掉落）；141 链爆保留（上限32）
- 手雷分支此前 fuse/dmg **双双错位**（29拿炸弹150、30拿炸药棍135；手雷拿250）：正解
  fuse 28=150/29=135/30=180、dmg 28=100/29=250/30=60（Projectile.SetDefaults）
- devices：141→explode(500,10)；210 地雷→explode(250,0,false)（原 100）
测试 tests/explosion.test.ts 5 例（374 全绿）。

# 功能方块全量审计（同日双代理）

我方已实现远超预期：**传送器235/泵142-143/逻辑门/分线盒/像素盒/全雕像表/陷阱族/巨石雕像/
大炮雪球炮/热喷泉/陷阱箱/宝石锁/感应器/测重板** 全已移植。剩余缺口分组：

**A. 光环 buff 快赢**（下批做）：瓶中星(42 frameY252-286 mana)、向日葵27(buff146 移速+墓地减半已有计数)、
和平蜡烛372(刷怪抑制)、巴斯特506(+5防)、水晶球125(预见)、附魔台354/磨刀石377/弹药箱287/战争桌464/蛋糕621
**B. 系统/交互**：提取机219/642(silt/slush转化+1.4.5通电)、传送带421/422实体输送(现仅翻向)、
烟花三件套216/335/338真实弹幕、音乐盒/喷泉/Monolith族(现toast)、物品框395/武器架334/470模特/475帽架/520食物盘、
宝石锁钥匙侧、大炮炮弹(现巨石近似)
**C. 小项**：地雷踩踏触发=原版无(仅电路,核实过)、篝火/心灯已有、马桶烟花497、广播箱425(需sign系统)
**D. Boss 召唤台**：蜥蜴祭坛237(电池召Golem)、永恒水晶座466、传送塔597

相关：[[vanilla-wiring-port]] [[enemy-ranged-transform-audit]]

## 智能光标全量移植（2026-08-11 同日晚，并行实现+收尾）

SmartCursorHelper.cs 39 策略 1:1 → src/player/SmartCursor.ts（84KB：原版 TileID.Sets 全表
+hitLine 射线+状态机 Toggle/Hold+方向锁）；Game.ts 接线（updateUse 每帧 lookup 覆盖 tx,ty——
HitTile 按格累计切目标不丢进度是能无成本换块的关键）；Renderer 黄框四象限（Main.cs:46016）；
设置 UI（Toggle/Hold+三开关，localStorage）。让位集=DisableSmartCursor 57 项原表。
**坑**：combatWeapon 联合加 'summon' 成员时必须同步 ItemCombat 接口加 summon 字段
（并行改动漏接口字段 tsc 报错）。测试 26 例（tests/smart-cursor.test.ts）。
Smart Select（Shift 换工具 Player.cs:17283）是独立系统未做。

## 教训（2026-08-12，世界树批次）

1. **子代理的"缺口报告"必须实测证伪**：上批报告称 itemstats 缺 832/4281 被 vid() 静默丢弃——
   复核发现 vid() 查的是 vanilla.json 全量表、从未丢弃；真缺陷是 523 个 vi_ 物品双键注册
   （snake 显式键+驼峰自动键）导致 rollChestLoot 主件双份入箱。**收尾报告里的"注意点/存疑"
   要当作待验证线索而非事实**。
2. **oracle 对账安全性判断法**：caves-checkpoint 自建链自持 RNG、对账终点=desertmound，
   链外任何 pass 插入零影响；新 pass 移植选原版注册序位置（下游插队尾会穿模）。
   世界树=LivingTrees(cs:15551)+Walls(:15792) 已移植，LivingTreePass.ts 独立函数便于
   将来 oracle 延链时零成本追加检查点。


## 2026-08-14 爆炸族全面 1:1 复核(用户报:雷管贴图巨大/无火焰粒子/引信不一致)
- **雷管贴图巨大根因**:drawProj 按碰撞盒宽 dw 画非方贴图——雷管 29 贴图 10×32 被拉成 14×44.8。修:drawProj 增加 drawSize=-1 原生尺寸模式(原版投射物绘制=贴图原生尺寸×scale1,与碰撞盒解耦)。
- **碰撞盒 1:1**(SetDefaults :846-869):炸弹 28=22×22/雷管 29=10×10/手雷 30=14×14——曾统一 14×14。
- **引信 timeLeft 1:1**(SetDefaults :10348-10372):**28=180/29=300/30=180**——曾误写 150/135/180(引信不一致根源;150/135 无源码出处)。
- **物理 1:1**(AI_016 :44859-44913):重力 0.2/tick(曾 0.3);旋转 rotation+=vx×0.1 滚动(曾 speed×0.03 自旋);着地摩擦 vx×0.97(雷管追加语义并入 0.96;曾 0.92 停太急)。
- **爆炸视觉按类型分档**(Kill :74881 炸弹/手雷 vs :74943 雷管 200×200 场):explodeAt 加 projId 参数——炸弹/手雷:烟 20(scale1.5 vel1.4)+火 10 对(scale2.5 noGrav vel5/scale1.5 vel3)+gore 4;雷管:烟 50+火 80 对+gore 8(scale1.5)。dust 31=烟/dust 6=火把焰(黄橙)。火粒子 grav 0+高阻尼=noGravity 语义。实测画面 4887 橙色像素。
- 手雷 30 不破坏地形(不在 ExplodeTiles 表);**手雷爆炸声也是 Item14**(74484 分支的 Item62 是死分支,28/29/30 全走 :74881 分支)。
- IsABombWithFuse 燃烧嘶声(SoundID BombFuse "fuse")素材未提取,未接。
- 探针:_bombprobe.mjs(8 项:碰撞盒/引信/粒子喷发)+ _boomvis.mjs(全画布橙色像素);GrenadeProj 构造曾漏 this.onExplode 赋值(当场崩)已修。


## 2026-08-14 三轮:死亡归因串号修复(用户:电路炸药炸死却报"凶手是洞穴蝙蝠")
- **根因**:`lastDamageCause` 是"最近一次设置者"模型——damagePlayer(带 attacker)会写,但 explodeAt/敌弹命中/祭坛锤自伤走 `p.damage()` 不写 → 死因残留上一个攻击者(已反杀的蝙蝠)。
- **修复**:爆炸族死亡归因 = **ByProjectile**(BombsHurtPlayers Projectile.cs:13974)——DeathCause 新增 `{kind:'projectile',name}` → DeathSource.Projectile「…凶手是{1}。」(Lang.cs:1031)。explodeAt 玩家伤害前设 cause(名 = Lang.projectileName(projId||108));GameHooks.projectileName 注入;Wiring devices ctx.explode 带 projId(炸药 108 Explosives/地雷 164 Landmine,来自 Wiring.cs case141/case210 的 NewProjectile 108/164);链爆=108;祭坛锤自伤=defaultWrap(ByOther 3 同族);WeaponProj 敌弹命中=弹型名。Lang.projectileName 走 PROJECTILE_NAME_BY_ID→ProjectileName 分节(108=炸药/164=地雷/28=炸弹/29=雷管/30=手榴弹)。
- 探针 _deathcauseprobe.mjs 7/7:残留蝙蝠归因被炸药覆盖/死亡公告实测「…凶手是炸药。」。
- **踩坑**:探针连环致死要先 `p.iframes=0`(前轮爆炸留的 40t 无敌帧会挡掉 99999 致死判定,死因设置了但死亡不结算)。
- 顺修并行会话两处页崩:Game.ts `scanBannerNpcs` 消费漏 import(:2386)/random-text.test 旧称 'default'→'defaultWrap'。

**火光双机制(2026-08-19 补)**:爆炸火尘必须走 VanillaDust 引擎(type 6)——①DrawDust 强制白全亮(:38406,暗处自发光)+②烟雾族链尾逐尘 AddLight(:1081-1090 尾档 num60/×0.65/×0.4 钳 0.6——火尘照亮周围)。曾用通用 spawnParticles=画在光照合成前被乘光压暗+零发光,黑暗洞穴爆炸近黑。烟 31/gore 61-64 同换原版引擎(fadeIn 老化/收缩族物理);28 族 22 盒/烟 20×1.5/火 10 对(2.5 noGrav×5 + 1.5×3)/gore×4(×0.4 对角±1),29 族 240 盒/烟 50×2/火 80 对(3+2)/gore×8(1.5 ±1.5)。探针 _explosion-light-probe(黑暗基线 0→峰 125)。
