---
name: vanilla-1456-upgrade-notes
description: "1.4.0.5→1.4.5.6 差异文档位置与升级路线——docs/upgrade-1405-to-1456/,数据源最终态一律取 Terarria1456"
metadata: 
  node_type: memory
  type: project
  originSessionId: e65c4575-731a-43e0-a377-ccf50cc42db3
  modified: 2026-08-09T11:50:32.907Z
---

2026-08-09 完成原版 1.4.0.5 → 1.4.5.6 全量差异整理,落盘 `docs/upgrade-1405-to-1456/`(相对项目根 `~/Project/GLM/SandboxWorld/`):

- `README.md` — 版本总纲、源码级差异实测、升级路线 P0~P2
- `wiki-summaries/summary-1.4.1~1.4.5.md` — 五大版本+26 子版本更新日志结构化解析(每条带 → 源码文件标注)
- `structdiff/` — 两版反编译源码成员级对比(md/json/脚本):1456 新增 564 文件、386 个共同文件有成员增删;ItemID +1164 字段、NPCID +109、TileID +191、ProjectileID +181、BuffID +126
- `raw-wiki/` — wiki wikitext 原始存档(33 页)

**已做完整性校验**(2026-08-09 查漏轮):
- 用官方 changelog.txt(Steam 自带,权威英文日志)反向核对版本清单:发现并补入唯一遗漏子版本 **1.4.4.8.1**(North Pole 伤害 73→80)
- 三份大摘要(1.4.1/1.4.4/1.4.5)经官方日志逐条校验并修订:1.4.5 补 25 条+修正 Paladin's Shield 表述、1.4.4 补 11 条(Morning Star/Celestial Sigil 60→12s 等)+修正 4 处、1.4.1 更正 5 处数值方向错误(Beetle 稀有度反、Queen Bee 误作 Queen Slime 等)+补 8 条;每份文末有【校验记录】节;1.4.2/1.4.3 人工核对无遗漏
- 官方 changelog.txt 路径:`~/Library/Application Support/Steam/steamapps/common/Terraria/changelog.txt`(1.4.0.1~1.4.5.6 全量,做数值争议时的最终仲裁源)
- 另:`Terarria1456Server/` 为 TerrariaServer.exe 反编译(1498 文件,含 Main 等;查 NetMessage/多人同步逻辑以它为准)

**关键结论**:
1. 数值/逻辑移植**直接以 Terarria1456 为最终权威**,不按版本日志逐条打补丁——1.4.1.2/1.4.3.2/1.4.4.9/1.4.5.6 都有回退性改动,中间版本数值会抄错
2. 105-pass 世界生成的**地牢 pass 必须按 1456 重写**(1.4.4 地牢生成整体重做,`Terraria.GameContent.Generation.Dungeon` 命名空间 104 个新文件,1405 完全没有)
3. 免伤帧/穿透惩罚体系在 1.4.1 与 1.4.4 两次重构,召唤/穿透武器手感的地底层,按 1456 最终态实现
4. 1.4.5 主题 Bigger and Boulder:种子可组合+Skyblock、650+ 新物品、Palworld/Dead Cells 联动、雷击/传送带/电信号;1.4.4 主题 Labor of Love:微光 Shimmer、Town Slimes、Loadouts
5. structdiff 字段增量混排"新 const ID"与"新静态数据表",逐条用时按语义区分

**Why:** 项目当前 105-pass/液体/561 NPC/UI 都以 1.4.0.5 为基准;升级到 1.4.5.6 需要这份差异清单导航,避免漏改或抄到中间版本数值。
**How to apply:** 涉及"升级到 1456"的任务先读 docs/upgrade-1405-to-1456/README.md 的 §5 路线;对照具体实现时查 Terarria1456 对应文件。
相关:[[reference-vanilla-source-of-truth]] [[vanilla-worldgen-port-status]] [[vanilla-npc-port]] [[vanilla-ui-port]]
