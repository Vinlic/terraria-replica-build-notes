---
name: debug-tools-f6-f2
description: "F6召唤面板+ F2无敌无限魔力调试工具;键位让位史(F2像素导入→F1,F6快速存档→Ctrl+S);探针_f6-panel 14断言"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-13T03:50:09.880Z
---

2026-08-13 调试工具批（均为原版无的自研件）：

**F6 召唤面板**（`src/core/DebugSummonPanel.ts`，DOM 浮层不进 vui）：全量 vanilla-npcs 列表（560+，搜索 id/名字、数量 1/5/10、鼠标处/玩家处落点）。生成走 `Game.debugSpawnNpc`：`Enemy.fromVanilla` + **NewNPC 底锚 `e.y = y - e.h`**（同 VanillaSpawner.spawnNPC 约定）+ Boss 槽接管 + 世吞 13 体节链 + 城镇 NPC 走 `TownNPC` 桶（TOWN_NPC_IDS 反查）。清怪按钮直置 dead 跳过掉落并清 Boss 槽防误记账。Esc 收面板优先于暂停链（main.ts）。

**F6 事件触发行**（2026-08-13 增,`Game.debugTriggerEvent`）：血月/日食/陨石/流星雨/哥布林/海盗六钮——**全部走自然入口零破坏**：血月=黄昏 roll 命中体(bloodMoon+清晷冷却+misc[8]);日食=黎明 roll 体(eclipse+misc[20],**夜按即拦**——黄昏会被自然清除白设);陨石=仅置 meteorPending(消费仍走 HandleMeteorFall time>16200 门+落点保护,午夜前按会等到午夜——探针实证);流星雨=StartMeteorShower 计数;入侵走 **startInvasionAndAnnounce**(带 hp≥200/Boss/进行中三门)——★勿用 announceNaturalInvasion(其 hp 门在自然 roll 调用点,直通漏门,探针抓回)。联机访客拦下(房主权威)。探针 scripts/_f6-event-probe.mjs 9 断言。

**世界消息广播审计**(2026-08-13,左下角 ChatMonitor=newText):Boss 出生全链已闭环——summonBossAtTx/spawnBossOnPlayer/WoF 自带/石巨人/蜂后/暗影珠三召✓;**补:F6 召唤(debugSpawnNpc,WoF113 仅文本无咆哮)/月总倒计时 spawnMoonLordOnPlayer(398)/鹿角怪 spawnDeerclopsOnPlayer(668)**;火星探测器逃逸改走 GameHooks.startInvasionWithAnnounce(直通 startInvasion 漏 misc 逼近公告+invasionWarn)。事件广播全绿:血月 misc8/日食 misc20/陨石落点 gen59/流星雨 gen92/入侵 misc approach/南瓜霜月 wave1/OOA InvasionStart/史莱姆雨 gen74-75/WoF击杀 misc15/Boss击败 HasBeenDefeated。

**鹿角怪 668**(2026-08-13 ✅已落地,详见 [[deerclops-port]]):vanilla-npcs.json 补 668+AI_123+弹幕 961/962/965 全链;F6 召唤→"已苏醒"广播+Boss 槽+家 tile 探针 7 断言全绿。

**F2 无敌+无限魔力**（`Player.debugGod`）：damage() 首行早退 + fixedUpdate 头血蓝回满（兜 DoT/溺水/摔落直改 hp 路径）。toggle 在 `Game.toggleDebugGod`。

**键位让位史（勿再对调）**：F2 原像素画导入 → 迁 **F1**；F6 原快速存档 → 迁 **Ctrl+S**；F1/F2 在 Input.ts preventDefault。F3 碰撞盒/F4 迷雾/F5 报告/F7 导线/F8 刷怪开关/F9 全亮/F10 传送鼠标均不变。

**坑**：①面板列 473-476 等已入数据（2026-08-11 补齐批），"无数据 id"测试须动态找表外 id（622 可用）；②钩蔓/触手等部件在**首帧 AI** 才入场，探针计数前须先 `g.fixedUpdate(1/60)`；③连续 damage 断言要手动清 `p.iframes`。

验证：tests/debug-tools.test.ts 4 条 + scripts/_f6-panel.mjs 浏览器探针 14 断言全绿（私有 5201 实例已收）。相关 [[debug-report-warn-ring]] [[plantera-parity-audit]]


## F6 boss 可见性双根因（2026-08-19"世纪之花/石巨人去哪了"）

①693 条按 id 升序默认截前 240——石巨人(排位 245)/世纪之花(262)/猪鲨(370)/
拜月教主(439)/光女(636)/史莱姆皇后(657)/鹿角怪(668)全在截断线外=看不见;
②filterSummonEntries 只匹配英文物名——中文搜索零命中。修:boss 行恒置顶
(默认视图+搜索结果同) + 过滤器接 nameOf 本地化名三路匹配(id/英文/本地化)。
探针 _f6panel-probe(4 断言:全 boss 在默认 240 内/中文双搜/置顶序),测试
debug-tools +2。教训:**列表类调试工具先算"条目总数×截断窗"的可见性账**
——boss 24 只排在 693 条流里,截断窗 240 必然吃掉尾部 7 只。
