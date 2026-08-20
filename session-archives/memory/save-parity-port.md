---
name: save-parity-port
description: 存档 1:1 对账(WorldFile/PlayerFile):npcs 三重断链+worker packet 黑洞已修;buffs/税金/血月/moonType 对齐;依赖未实装清单
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-12T06:20:50.722Z
---

2026-08-12 用户要求"原版存档保存的状态与我们存档全量对齐"。双代理对账(原版 WorldFile.cs v319 + Player.cs PL:53802-53982 ↔ SaveData),产出 docs/save-parity-gaps.md 总账。

**修掉的两大隐性断链(此前排障史都没发现)**:
1. **城镇 NPC 持久化三重断链**:serializeSave 硬编码 `npcs: []` 丢第 5 参;SaveFile.saveGame 调用处连参数都没传;loadSaveData 不读 data.npcs、pendingTownNpcs 无填充点——读档恒走"新世界出生"分支。四端打通(serialize/SaveFile/SaveClient+worker/loadSaveData)。
2. **worker 读档字段黑洞**:读档主路径 WorldGenClient→packWorld→fromPacket,而 packWorld 只传 18 个字段——loadSaveData 恢复的 invasion/altarCount/weather/bestiary **在 worker→主线程一跳全部蒸发**。WorldPacket 补 invasion/altarCount/weather/bestiary/moonType/clock 三件套/pendingTownNpcs。教训:**"loadSaveData 恢复了"≠"主线程拿到了",worker 链路字段要过 packet 白名单**。

**How to apply**:
- 新增世界持久字段 checklist:SaveData(serialize.ts)→ SaveMeta → SaveFile.saveGame meta+playerData → **SaveClient.doSave 的独立 meta/playerData(主路径!)** → loadSaveData 回填 → **WorldPacket+packWorld+fromPacket(worker 路径)** → Game 侧消费。漏任何一环=某条路径丢字段。
- 玩家 buffs 存 vanilla id 非 BuffType 枚举值(BUFF_DEFS.vanillaBuff 反查);Main.buffNoSave 名单(Main.cs:8896-8990,含 173-181 段)在 Buffs.ts BUFF_NO_SAVE 过滤——光环 buff(篝火 87 等)不入档由扫描续期。
- 事件态(party/lantern)在 Game 侧单例→eventsForSave/eventsApplySave,loadSaveData 返回值带 data;worldgen.worker result 事件带 `save: data`。
- saveGame 系列调用点 3 处(mainFlow×2/main.ts saveGameCompat)都要带 eventsForSave()。
- **python 批量改文件务必 tsc+测试紧跟**:本轮 python 替换曾把 protocol.ts 清成 0 字节(open('w') 先截断后 write(None) 炸)——从全部消费方证据重建(grep dist 不如 grep 源码消费方)。
- l10n-audit 插件缺键会阻塞全部 vitest;并行会话加 BuffType 忘键时,补 tools/l10n-custom/{zh-Hans,en-US}.json + node scripts/build-l10n.mjs 解锁(勿删其代码)。
- 桩 player 测试({hp,x,y,inv} as never)要求序列化侧防御:player.buffs?.toSave?.() ?? []。
- 遗留:hardMode 无写点/渔夫/矿石档位等 20+ 项依赖未实装,全清单在 docs/save-parity-gaps.md。
- downedSlimeKing:击败键写 downed_50(通用),天气钩子读点回退 `?? downed_50`。

**review 补修(同日)**:loadSaveData 的 `v3Chests`(v3 稳定 id→内部 id 箱子映射)是**死变量**——赋值处用了未翻译的 data.chests;被"现有物品 stable≡internal"掩盖,自定义物品进箱读档即错(已接线+locked 透传,save.test 8 例含 packet 往回归锁)。向后兼容核查全过:旧档(npcs/clock三件套/moonType/buffs/events 全有 undefined guard)、wld 导入(version=2 直读)、服务器 saveWorldOnly(新字段可选)。

**图片方块群存档保卫(同日,用户点名)**:PRIV_TILE_STABLE 出现 `pixel_block: 1028` 与 `dirt: 1028` 双派——dirt(def 早)先注册赢 1028,pixel_block 双表被丢 → 图片方块群(F2 导入,RGB 编码 frameX=(r<<8)|g/frameY=b,均在 uint16 内 RLE 帧段可存)存档写 0=**读回全变 air 丢失**。修正:dirt 改派 1029,1028 归 pixel_block 不动(**append-only 冻结表铁律:冲突时新来者改派,绝不挪老号**)。pixel-art.test 6 例(含"存档序列化往返/1028 双向注册"契约)全绿,stderr 冲突告警消失。剩余失败=luck-system(并行会话 Luck.cs 在途)。

相关:[[town-npc-persistence]] [[multiplayer-capacity-opt-batch]] [[dart-proj-visual-port]]
