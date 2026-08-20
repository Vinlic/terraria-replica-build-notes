---
name: worldgen-selfinvented-audit
description: 世界生成自制机制全量审计+修复+遗留补齐完成态:oracle同构对账全绿(39/58行权威含corruption);GenSolid/StructureMap两子系统落地;dungeonL单走廊微差=唯一余项
metadata: 
  node_type: memory
  type: project
  originSessionId: d76053b3-a9fb-4d75-a43d-41f181c7cab5
  modified: 2026-08-15T15:54:09.346Z
---

# 世界生成"自制机制"审计+修复+遗留补齐(2026-08-13 终态)

四审计代理+七修复/同步代理+直修,**全部处置完毕**(约 70 条主批 + 8 条遗留批)。

## 遗留批补齐终态(目标"遗留的全面补齐")

- **P1** SwordShrinePass.ts 死代码删除(剑冢已归位 MicroBiomes)
- **P2** dgLayout 非短路(LegacyDungeonLayoutProvider.cs:61 `&`)——仓库(先掷后判,TS 禁 bool &)+oracle 双修
- **P3** 四计数骰序(cs:17081-17084 CaveHouse→Underworld→CaveChest→AdditionalDesert)——`rollHouseChestCounts`(CaveHousePass)在结构槽头预掷暂存 gs,三消费端回退兼容
- **P4 动态 tileSolid 族**:GenSolid.ts(Map 重放,严格超集 Set——TILE_DEFS 已预翻 192/481-483 且原版有中途翻回窗口);~30 翻转点全接(多处审计改判);消费端只迁"时点态一致"的,**刻意不迁**清单(potPass/Traps/FinalCleanup 等=本仓 pass 序偏差使静态正确)在 GenSolid 头注
- **P5 StructureMap**:GenState.protectedRects(存 Inflate 后矩形,半开区间)+canPlaceStructure/addProtectedStructure;9 调用点接(蜂巢±50pad5/蜂蜜斑/神龛pad1/剑冢pad10/营地pad4/炸药pad5/CaveHouse 5/8/Shimmer);**金字塔核实原版本无保护**;validTiles 内容扫描③暂不移植备案
- **P6 oracle 同构对账全绿**:oracle=JS 同构镜像(共享旧误读,如短路&&/底左锚);全批修复同步进 caves-oracle.cs→dotnet 重跑→58 行/种子拼回。**oracle 权威 39/58(terrain→slush 含 corruption 交叉验证恢复)+JS 冻结 19/58(dungeonL→beaches)**;SW_FREEZE_CAVES=1 再生工具在 tests/_freeze-caves.test.ts

## 对账揪出的 JS 真偏差(已修,方法论:双侧同构对账)

1. dgLayout 起始房前缺两颗 settings-RandomSeed(LegacyDungeonLayoutProvider.cs:37/:42)
2. 花岗岩 CA target 初值应为 source 别名拷贝(BuildMagmaMap GraniteBiome.cs:96-107,曾全 0)
3. Lakes lerp 无钳制(Utils.cs:107,steps×1.3 末步 t<0 外扩)
4. dgHall num4 缩径行 float32 算术(LegacyDungeonHall.cs:680,JS 用 Math.fround 复刻;oracle :4549 同款)

## 唯一余项(单独立项)

**dungeonL 单走廊微差**(种子 9293480,x633-711/y511-671,~170 格):~~需插桩~~ **已破**(见下方 2026-08-14 终局——首版 fround 层级错才是根因;双正号怪癖 :628-633 双侧已复刻)。

## 测试终态

caves-checkpoint 3/3 绿;pass-hash/全链冒烟双种子/dungeon 三件/gem/gen-loot/micro-biomes 全绿;地牢连通探针 4 种子 9 PASS(尖刺带可挖通口径勿改);tsc src 零错(gen 目录;Game.ts 偶发=并行会话在途)

关联:[[dungeon-entrance-plug-fix]] [[jungle-parity-and-id-collision]] [[worldgen-perf-batch]]

## 2026-08-14 终局:dungeonL 微差已破

- **根因**:dgHall num4 缩径行的 float 复刻层级错——C# `(float)num4 * (((float)r2) * 0.01f)` 是**逐二元运算**各舍入到 float32;JS 曾"double 乘完一次 fround"→trunc 边界偶发翻 1(H#30 num 6↔7 实锤)。修=`Math.fround(Math.fround(num4) * Math.fround(Math.fround(r) * Math.fround(0.01)))`。
- **方法论**:双侧同构插桩(dgHall 休眠钩子 globalThis.__dgHallTrace + oracle DG_TRACE 环境变量)+ 轨迹逐 hall/step diff(diff 脚本 /tmp/dgdiff.mjs,注意 -0 归一与 H/S 行前导裸 idx 解析)→ **81 hall 逐步全等**。
- 终态:oracle 权威段扩为 terrain→slush 全段(冻结工具 ORACLE_AUTHORITY 31 行,JS 分歧时保留 golden=留给并行会话定稿);dungeonL→beaches=修正后 JS 冻结(已被轨迹对账背书)。
- ~~当前唯一红~~:underworld→slush 4 行(并行树会话 growAshTree 在途)已随 2026-08-15 树会话定稿后 oracle 重拼**全部转绿**;现无任何 checkpoint 红。

## 2026-08-15 差异复核批
- **dungeonBa 分歧已破**:dgBanners 的 `TILE_BY_KEY['banner']`=undefined(key 实为 **v_91_banners**)→ 横幅全部静默丢弃+近旁横幅排除恒假。双侧逐样本轨迹对账(BANNER_TRACE 2454 样本流)实锤 N 426,570 typ=91。修后 129/129 逐位一致,dungeonL→beaches 双种子全绿(全 58 行 oracle 权威)。
- **猩红链 159 格差已破(2026-08-15 终局)**:**唯一根因**=placeAltars 掷域下界的 widen/2 是 C# int 整除,JS 浮点除在奇数 widen 时下界偏 1 → 祭坛骰流整体分叉(分层对账已排除其余全部段)。修=Math.trunc(widen/2);顺修列填充上界 h-1→h。oracle Place3x2Altar 巨石门 523 笔误(蜻蜓罐!)同批修为真 Boulders 集(138/484/664-665/711-716,TileID.cs:195;原版 Place3x2 :52142 type==26 门核对)。三行回归 oracle 权威,**58/58 双种子全等+第三种子 987654321(猩红)零分歧泛化验证**。
- 对账工具箱:caves-checkpoint.snap 加 __cavesGridExport 钩子(dormant,导出 typ/act 二进制)/oracle GHOST_DUMP/内部id→sheet 对照导出法(diff 必须先归一,dump 的 JS typ 是内部 id!)。
- 顺手:并行会话 HousingPanel 缺键 Mods.SandboxWorld.Housing.More 已补(l10n-audit 硬拦恢复)。

## 2026-08-16 收尾核验
- 本批成果(widen/2、横幅、Boulders 门)双种子 corruption→beaches **全段✓ 完好**;第三种子 987654321 泛化零分歧。
- 现存 checkpoint 红=并行会话(图鉴染色批)新加的 **7 段检查点**(livingtrees/livingtreewalls/altars/surfacewaterinjungle/dirtwallcleanup/pyramids+1,oracle 58→65 行+测试链/ golden 同步扩)在其会话在途——JS livingtrees=25b90cb8 vs oracle=0ced0509 属该会话未定稿,勿跨会话代修;定稿后其会话自会拼接 golden。
- 收尾清单核验:私实例 5206 已杀(5202/5207=他会话)、一次性探针(_primeframe/_skspin/_frogfix/_enttrace/_crimtrace/_crimdiff/_thirdseed/_idcheck/_idmap)全删、_dungeonconn/_freeze-caves 保留为常驻工具、双侧插桩(CRIM_TRACE/BANNER_TRACE)清零后 oracle 与 golden 逐字节一致(确定性✓)。

## 2026-08-17 食人鱼死亡碎块修复( gore 提取器 else-if 语义)
- 用户报:食人鱼(58)死亡出"血月兔子碎块"。根因=extract-gore.mjs 把 if/else-if 链的 else 兜底块摊给外层全集(不扣兄弟 if 已领走的 type):58 死亡 gore 应只 [85],曾 [85,78,79](78/79=兔肉,只归 47)。
- 修复:siblingTypesAt(depth) 累计同链 if/else-if 的 type 并集;else **与续链 else-if**(无自身 type 谓词的门分支如 RedHat)都剔除先行兄弟 type。重生成表后 35 处同类错全正:13/14(世吞 28,29 只归 15)、51/93/150/152/226(史莱姆链 82 只归 49)、35/68(骷髅王头 1401-1402/56-57 只归手 36)、132/186/189/251(人形尾 gore 3 只归未命中型)、190-194/317/318(骨 1,2 只归 2)、245/246/249(石巨人拳/头 369-371 只归其他;246 死亡=NewNPC(249) 无 gore)、362-366 各归各。
- 全 35 处逐一对照源码核验;tests/gore 两处旧值断言同步修正(13=[24,25]、红帽 35=3 块非 7)。gore+mech+boss-music 48/48 绿;浏览器探针杀 58 实证 gores=[85]。
