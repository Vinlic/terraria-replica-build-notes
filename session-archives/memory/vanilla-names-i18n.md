---
name: vanilla-names-i18n
description: 物品/方块命名全走 l10n；方块名=放置物品（createTile 反查）；审计脚本模式
metadata: 
  node_type: memory
  type: project
  originSessionId: 04569a63-44aa-4669-98a3-b777d15e98f8
  modified: 2026-08-10T06:17:38.004Z
---

2026-08-10 命名多语言审计结论与修复（数据源=tools/l10n 1456 全量包，见 [[vanilla-random-text-death-tombstone]]）：

- **物品链路本来就健康**：Lang.itemNameByKey(key)（vi_ 前缀/ITEM_KEY_TO_ID → ItemName.<internal>），
  533 个物品 = 373 l10n 中文 + 110 自定义物品中文兜底（木镐等原版不存在的发明物），0 断链。
  唯一漏网点：Game.ts 商人购买 toast 曾直用 ITEM_DEFS[].name，已改。
- **方块曾 100% 断链**：`Tiles.*` 分节在 1.4.4+ 包里是空的（原版方块无独立显示名）！
  正解=原版语义：方块名取**放置它的物品**。build-l10n.mjs 现生成
  `TILE_NAME_ITEM_BY_SHEET`（TEdit items.json createTile 反查取最小 id 基础款；覆盖 12→item29）。
  Lang.tileName 链：① placer 物品名 ② MapObject 族名 ③ null→调用方 TILE_DEFS.name。
- 官方译名与旧硬编码的差异（已统一为官方）：落地大摆钟/长椅/烹饪锅/粘土盆/墓石/
  生命水晶/铜吊灯/挂链灯笼/骷髅头灯笼。
- 回归测试 tests/tile-names.test.ts（真实包注入 loadPackJson）。
- **审计模式**：名字覆盖审计用 node 脚本解析 items.ts/tiles.ts 的 def 正则 +
  idNames.generated 的 export 块正则 + l10n json 直接对账（/tmp/name-audit.mjs 思路，可复建）。

## 全量多语言（同日二轮）
- ITEM_KEY_ALIASES 两批共 36 条（build-l10n.mjs）：platform/door/workbench/…/8 系阔剑/
  药水/扳手等全有原版对应；533 物品 = 531 原版 12 语言译文 + 2 发明物(木镐/木斧,
  l10n-custom Mods.SandboxWorld.ItemName + itemNameByKey 第②级回退)。
- 硬编码文案迁移：Game.ts 60 条/UI/mainFlow/Renderer/RandomText 共 ~150 键全走
  Lang.text('Mods.SandboxWorld.*')（l10n-custom en+zh；其余 10 语言英文兜底）。
  EoC 召唤提示直接用原版 Lang.misc(9)。遗留未迁：UI.showMainMenu(死代码)、
  F5 标注面板/F3 调试面板(开发工具)、legacy puppeteer 垫片、buff duration 用自定义 Time 键
  (原版 LocalizedDuration 是代码级组合,包内无模板键)。
- 双向审计脚本：/tmp/key-completeness.mjs(源码键↔包键)+full-lang-audit.mjs(12 语言)。
- 三轮补全：367 个 VAN tile defs 全审（**def 正则要平衡大括号，`[^}]*` 会漏嵌套 vanilla:{}
  导致严重漏统计**）。Lang.tileName 第③级 = TILE_NAME_ZH/EN_BY_ID（id-maps tiles.json
  753/753 自带 zh+en——世界生成专属块[树/藤蔓/药草/宝石树/帕鲁蛋…]的唯一译名来源；
  原版对它们无 UI 显示名。zh 系语言取 zh 其余取 en）。
  363 唯一 sheet 全解析：297 placer + 3 MapObject + 63 id-maps。Timers→1秒计时器、Switch→开关。
  build-l10n write() 必须转义单引号（id-maps en 有 "Jack 'O Lantern"）。
  Boss/死因名字改 Lang.npcName(vanillaId) ?? def.name。
- 四轮（全量收尾）：**6000+ 物品早已动态注册**（items.ts 从 vanilla.json 注册 vi_，6059 id），
  真正的英文泄漏=place_v_* 放置物品 name 抄 tile 英文名且 itemNameByKey 无 place_v_ 分支。
  修：itemNameByKey ①.5 place_v_→tile sheet→tileName；l10n 缺译 id → ITEM_NAME_ZH/EN_BY_ID
  （id-maps 6129/6146）兜底。**墙也同构**：Lang.wallName（WALL_NAME_ITEM_BY_WALL createWall
  反查 + WALL_NAME_ZH/EN 自然墙），墙链 366+292 全覆盖。
  def.name 英文全清（tiles 674+walls+items vi_ 368+动态注册段）；Lang 兜底 ?? key 改 || key（防空串）。
  WldImport 宝箱物品：VANILLA_ITEM_KEY_BY_ID（注册时收集 id→key）兜底 ITEM_MAP → 不再跳过。
  注册总数 6059 而非 6146：其余是 vanilla.json 贴图表没有的开发者/未发布物品（无图标，不注册）。
  tests/item-coverage.test.ts（包注入顺序注意：后加载覆盖 → zh 最后）。

## 火把锚定+动效（第五轮）
- src/world/Torch.ts：torchAnchorFrame（TileObjectData tile4 锚 1:1，优先级
  底(0)→左(22)→右(44)→墙(0)；TEdit Tiles_4 framing：frameX 22px 步长，0=直立/22=左倾/44=右倾，
  +66=未点燃；frameY=样式×22）+ torchStillAnchored（直立火把底锚 OR 墙锚任一在即留——
  挖地板留墙不掉是原版行为）。
- Game.tryPlace 火把特例（液体拒绝/无锚拒绝）；onTileChanged 订阅 checkTorchDetach
  （支撑被挖→掉落+dig 声）。渲染：VanillaTiler 火把 X 偏移 +4（TileDrawing case4 +6 与
  20px 居中 -2 的净值）。火星：emitTorchSparks 已有，改为锚定感知（22→+6/44→+2/else+4，
  TileDrawing:7220-7231）+ 原版概率 1/40/帧。wld 导入火把 copyFrame 保留原帧 ✓。
- tests/torch.test.ts 7 用例；E2E scripts/_torch-probe.mjs（四锚定摆放+支撑破坏掉落）。
