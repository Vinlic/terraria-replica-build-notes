---
name: terraria-assets-pipeline
description: Terraria 全量素材解包与 ID 对照表/素材功能表的工具链和数据位置
metadata: 
  node_type: memory
  type: project
  originSessionId: e27c53f3-6128-4e65-9d23-015afd2824a3
  modified: 2026-08-09T14:54:34.338Z
---

2026-08-05 完成泰拉瑞亚素材全量解包与功能标注(游戏版本 1.4.5.6, Steam macOS 版,游戏位于 `~/Library/Application Support/Steam/steamapps/common/Terraria/Terraria.app/Contents/Resources/Content`)。

- `terraria-assets/`: 全量解包产物(14998 PNG + 852 WAV,~146MB);`assets-table.json` 为机器可读全量功能表(15851 条,9241 条带官方简中名);`素材表/` 为 20 个分类的 Markdown 明细 + README 索引
- `tools/xnb-unpack/unpack.js`: xnb 库(lybell/xnb, npm 包名 `xnb`)批量解包脚本,含自定义 XNA SoundEffectReader(输出 16bit PCM WAV);XNA4 SoundEffect 布局 = u32 waveFormatSize(18) + WAVEFORMATEX(18B) + u32 dataSize + data + 12B尾(loopStart/loopLength/duration),跳过开头 u32 否则全字段错位;注意库的 `unpackToFiles` 在 Node 下有 bug,要用 `bufferToXnb`+`xnbDataToFiles`;Fonts 的 ReLogic DynamicSpriteFont 与 XACT 音乐(.xgs/.xwb)无法解包
- `tools/extract_l10n.py`: 用 dnfile 从 Terraria.exe 提取全部官方本地化 JSON(含 zh-Hans 的 Items/NPCs/Projectiles/Game 等, 键为内部名)到 `tools/l10n/`
- `tools/build-id-maps.mjs`: 构建 ID↔名称(内部名/英/中)对照表 → `tools/id-maps/{items,tiles,walls,npcs,projectiles,buffs}.json`;来源=官方 l10n + terraria.wiki.gg(英文站 raw wikitext/数据模块, 中文站需 `action=parse` 渲染 HTML 因原文是 `{{tr|}}` 模板);wiki 抓取需缓存+重试(连接不稳);表格解析必须按列跟踪 rowspan(每行递减)
- `tools/build-asset-table.mjs`: 由对照表+素材目录生成素材功能表

**Why:** SandboxWorld 复刻开发中需要按 ID 查素材含义(如 Tiles_2 图块表、Item_N 图标)。

Wiki 离线阅读(2026-08-06):用户下载了 Kiwix ZIM 快照 `terraria.wiki.gg_en_all_2026-07a.zim`(1.2GB, 英文站,渲染后 HTML)。**agent 首选数据源是 `terraria-wiki-md/`**(由 `tools/zim-convert.py` 转换,10455 篇文章 → 每篇一个 Markdown + `index.json` 索引 + README 标题列表,内部链接已改为可跳转的相对 .md 路径,~650MB)。检索方式: index.json 按标题/分类找文件、`grep -r` 全文搜、或按需 Read 单篇。ZIM 原始读取备用: `pip3 --user install libzim` + `tools/zim-read.py <页面名> [--html|--dump]`。ZIM 是英文站,中文站 ZIM 可从 library.kiwix.org 获取;ZIM 目录解析(纯 Python dirent 解析)见 zim-convert.py,libzim 的 Archive 不可迭代/下标访问、SearchResultSet 取不出条目,只能 get_entry_by_path。自写爬虫 `tools/wiki-mirror.mjs` 曾完整爬取中文站 wikitext(37279 页)但输出目录后被用户删除,需重跑时: wiki.gg 有 Cloudflare 限流(429/56),必须带自定义 UA+cookie jar+≥0.8s 间隔+指数退避,Node stdout 重定向会缓冲、需 fs.writeSync(2,...)。

**How to apply:** 查游戏机制/物品资料用 `tools/zim-read.py` 离线读 ZIM;查素材功能直接读 `terraria-assets/assets-table.json` 或 `素材表/` 分类 md;游戏更新后重跑解包/对照表三个脚本即可重新生成。相关 [[sandboxworld-project-setup]]。

游戏内原版贴图接入管线(2026-08-09 补): `game/scripts/vanilla-whitelist.json` 是 tile/wall/npc 白名单(注意 sheet 字段=原版 tileID 而非 Tiles_N 表号),改完跑 `cd game && node scripts/vanilla-atlas.mjs` 重新拷 PNG+生成 `public/sprites/vanilla.json`(纯增量安全);曾漏 43 绿砖/72 蘑菇树两表导致贴图隐身。`game/dist/` 是构建产物,改 public/ 后要手动同步或重新 build。相关 [[vanilla-door-frames]]。

**素材包"空贴图"真相(2026-08-09 排查,勿再当解包 bug 修)**:全包 83 张全透明 PNG,其中 **Projectile_187/188/654/290-299 等是官方占位 stub**——xnb 字节级相同跨不同弹幕(真贴图不可能)、LZX 解压后像素全零但尺寸正确、AssetInitializer/TextureAssets/LoadProjectile 无任何重映射。这批弹幕的原版视觉=隐形弹体+dust 粒子(如 188 Flames 的 AI 每帧刷 dust 6 火焰尘埃,Projectile.cs:24222)。其余空桩是 1×1 魔术像素与 id_0 占位,正常。排查方法:xnb 头 flags@5(0x81=LZX)、字节级 hash 分组、xnb 库解压后数非零像素。

## Tile 全量补齐（2026-08-12，用户令"和原版没有任何出入"）
- **权威对比法**：vite-node 直载 `TILE_DEFS` 收集 `vanilla.sheet`（**正则会漏 VAN() 简写**——先按正则算出 380 缺是错的，模块直载权威值 359 缺）vs TEdit tiles.json 全 753 条。
- **生成规则**（程序化,勿手改段）：isFramed/frameSize>1x1 → framed style(fw/fh)；isSolid 1x1 → blend auto；其余 → decor auto。mapColor=TEdit color 前6位。key=`v_${id}_${slug(name)}`（602 Emerald Bunny Cage 与既有 v_602_emerald_tree 同号不同 key 无冲突——sheet 前缀撞号没关系,key 全局唯一即可）。
- **结果**：TILE_DEFS 401→760、sheet 覆盖 753/753、key 零重复、白名单 tiles 752+119=753、atlas 管线 meta 753 全出。**追加位置=TILE_DEFS.forEach 构建行之前（id 顺序铁律）**——程序段以注释标记，后续手工 def 仍插段前。
- **坑**：119 Iridescent Brick 有 def 有 PNG 但**白名单从未收录**（meta 一直缺它）——全量核对时以"TEdit id 全集 vs vanilla.json keys"复核而非只看新加的。
- tsc 零错、vitest 315/315。新 359 个 tile 只有渲染元数据（solid/framed/mapColor），行为语义（掉落/工具/发光/动画表）按需后续逐个补。
- **整体 review 收口（2026-08-12 晚）**：①贴图缓存——753 sheet 的 PNG 全在 public/sprites/vanilla 且 meta 全出，运行时**无需打入图包**（tiles 走 ensureVImage 懒加载+onVImageLoaded 重烘焙；Item_Atlas 只打包物品图标，tile 无图集化设计）；preloadVanillaWorld 全量预载仅调试路径，正常走出生点子集 collectSheetsAround。②**发现并修复真缺口：WldImport TILE_MAP 是硬编码表**——新 359 tile 导入存档会"降级石块"！加 SHEET_FALLBACK 兜底（TILE_DEFS 首个同 sheet def,framed 者拷帧;显式 TILE_MAP 优先保 null 特判）。实测 Starter_World 271 种 tile id **零未覆盖** ✓。③并行会话在途:weather/save 测试 2-3 挂（其自己代码,单独跑也挂）。
