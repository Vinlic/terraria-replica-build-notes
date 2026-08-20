---
name: system-coverage-audit
description: 全量系统缺口审计（三代理对账）+ 星星雨/陨石/派对/快乐度四子系统+四遗留全落地
metadata: 
  node_type: memory
  type: project
  originSessionId: d6caec24-1cc3-4182-bea5-29046ee459cf
  modified: 2026-08-13T02:30:02.174Z
---

# 全量系统覆盖审计+补齐（2026-08-13，/goal"检查未接入系统→补齐"→第二轮"遗留全部对齐"）

## 审计方法
三并行代理对账：①星星雨+陨石源码 ②WorldGen.UpdateWorld 周期清单 ③引擎现状 16 项。结论：**已覆盖远超预期**（世界演化/旅行商/矿车/蜂巢/图鉴/灯笼夜全有）；真缺口 4 项全落地；遗留 4 项也全落地（本轮）。

## 第一轮四子系统

**① 星星雨（FallingStar.ts）**：boost 三档（10%→3.0-5.0/余1/3→1.0-1.5）；每 tick 概率 `w×boost/3,360,000`（4200 宽满月期望 40.5 颗）；运气定向 RollLuck(15)；弹幕 720 Spawner 期 180t→12 恒速；落地掉 Item 75；白天清；boost>3 刷附魔夜行者 484。**星掉落被秒拾是正常语义——探烟查背包**。

**② 陨石坠落（MeteorFall.ts）**：触发三源（入夜 1/50 downedBoss2 / EoW-BoC 首杀必/后 50%）；**消费=夜 time>16200（午夜）——探针 timeOfDay 须 >回绕值**；打分+六重保护（玩家±1022/±639px/NPC/宝箱/地牢砖/特殊块）；五层生成 tile 37；setTileSilent 须 markDirtyArea；失败 1/3→陨石雨。

**③ 生日自然派对（party.ts）**：Party Girl 硬门+冷却+1/10→≥5人→1-3 人过生日；cooldown 持久化 events.partyCooldown。

**④ NPC 快乐度（vanillaHappiness.ts）**：ProcessMood 1:1。测试坑：**LoveSpace(×0.95) 污染基准断言——baseHappy 须 village=4**；公主孤单 1000 须村<2。

## 第二轮四遗留（全 1:1）

**⑤ NPC 互相关系（AllPersonalitiesModifier :12-506 全量 103 条）**：
- **NPCPreferenceTrait 在 1.4.5.6 是死代码**（0 实例化）——关系表已搬进 ModifyShopPrice_Relationships 的 switch 硬编码（25 owner×Like/Love/Dislike/Hate，全表在 vanillaHappiness.ts NPC_RELATIONSHIPS）。
- 倍率与群系同套 0.88/0.94/1.06/1.12 但**所有命中连乘**（群系只取最强一条）；**触发=同屋<25 目标**（村 25-120 只计拥挤/宽敞不触发）；目标过滤 37/368/453。
- 公主动态：owner=663 从同屋池随机抽 3 各 Love（不足全 Love）；他人同屋见 663 → ×0.94。Game.computeShopHappiness 组装 nearby 列表。
- 反直觉条目防"纠错"：208 派对女孩 Love 633；18 护士双 Dislike(208/20)；441 五条；588 的 Like 227 在 Love 369 前。

**⑥ 小地图皮肤（9 款全）**：皮肤=**客户端选项** config.json "MinimapFrame"（非 .wld！MinimapFrameManager.cs:11-19）；每款=**整张贴图**（非切片）+3 按钮，零代码分支差异只有 frameOffset+按钮位（Renderer.MINIMAP_SKINS 表）；l10n 键在包内 UI 类下嵌套（**查法 d['UI']['MinimapFrame_*'] 非平铺键**）；白名单+展平键 UI_Minimap_{Skin}_*；Settings modeRow 切换。

**⑦ 天幕流星修复**：仓库早有 spawnSkyMeteor 但**画在天空底色 fillRect 之前=完全不可见**（层序 bug）——移到天空色+日食压暗之后；参数 1:1：depth=rand*3+3、视差 1/Depth 水平+0.9/Depth 垂直、缩放 3/Depth、alpha 淡入淡出 5%×0.5（BrightnessLerper）。**触发在 meteorPending 块内、rawTime 用 Clock.DUSK=0.8125 换算——探针勿用 0.75 旧约定**（差 222 线就 miss）。

**⑧ 派对帽+派对贴图条（两套机制并存）**：
- **贴图条替换**：UpdateAltTexture(NPC.cs:91250) PartyIsUp 且非 441/453/633 → altTexture=1 → TownNPCs/{Name}_Default_Party 整条替换（TownNPCProfiles uniquePartyTexture 表；Guide/Dryad/ArmsDealer/PartyGirl 等原版就是不变）。资产=public/sprites/vanilla/NPC_{id}_Alt_1.png（663/682 本轮补拷+vanilla-atlas.mjs TOWN_PARTY_ALT 块持久化）。
- **帽子叠画**（Main.cs:26814-27089 Extra_72：20 列×40×36，色格 0 蓝/16 粉/17 青/18 紫/19 白）：UsesPartyHat 排除 441/37/633；配色=name.Length+name[0]+whoAmI+moonPhase±dir mod5（白天 moonPhase−1）；Y=HAT_FRAME_GROUPS[NPCFramingGroup] 帧表（8 组全表）+HatOffsetY 表；X=(2+num3+num7)*num5；origin=(W/2,H−12)；随体镜像同 save 块。

## 验证
- system-coverage.test.ts 17 条全绿（+关系 1 条）；_leftover-smoke.mjs：9 皮肤注册+贴图全载+切换持久化/Extra_72 800px/663·682 条/scene.partyUp/流星触发 depth∈(3,6)/**像素差分 1124px 证可见**/零 pageerror。
- 冒烟三坑：puppeteer 无 userDataDir=每次全新 profile（角色/世界每跑必建）；截图 buffer 不能直传 evaluate（Node 侧 Buffer→base64）；流星出生=中心−v×600 屏外高处（t=600 才过头顶）——差分前须 teleport 或等 t≥350。
- **并行会话共享源码：血肉墙 drawWoF mid-edit 会让 5207 探针同炸**（wait-to-settle 后复跑全绿）；tsc 剩余错全=用户 WIP（frostBurn/dungeonX/town-npc）。

## 终态缺口登记
- 城镇宠物帽（637/638/656 帧修正分支）、229/550 攻击/坐姿 X 修正：仓库无这些状态，略（注释标注）。
- 离线时间推进=原版无此机制，不移植。
- 世界周期系统清单已确认全有对应或纯视觉。

关联 [[moon-cycle-port]] [[vanilla-ui-port]] [[parallel-vite-sessions]]
