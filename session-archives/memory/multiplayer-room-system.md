---
name: multiplayer-room-system
description: 多人联机现状——中央服务器房间制 v3（房间码/公开性/双保护），探针与端口约定
metadata: 
  node_type: memory
  type: project
  originSessionId: 372ae608-2da7-4502-87f6-cedcc2af7bb7
  modified: 2026-08-11T04:54:45.196Z
---

多人联机为**中央服务器房间制**（2026-08-11 完成，取代 v1/v2 直连+开服脚本方案）：

- 服务器 `~/Project/GLM/SandboxWorld/server/`：`src/index.ts` = HTTP lobby（:port+1，POST/GET /rooms、码校验、DELETE 关房、GET /lan）+ WS 路由（:port，URL `/<6位码>?token=<hostToken>`）；`src/room.ts` = Room 会话（世界实例+策略+双 token 房主判定）。`npm start` 启动（--port 默认 7777，lobby 7778）。
- 房主 = 建房时 POST 返回的 hostToken（randomUUID）首携者；`hostJoined` 防多主。
- 双保护：protectTiles = 服务端权威拒绝非房主 TileBatch + correctionFrame 回滚（对齐原版 SendTileSquare 纠正）；protectItems = RoomPolicy(msg200) 下发 → 客户端 `Game.netCanEditTile()/netCanChestInteract()` 集中门禁（tryMine/tryPlace/tryPlaceWall/useWireTool/interactAt/tryOpenChest 入口；自动拾取豁免）。
- 客户端：`game/src/net/ClientNet.ts`（policy 字段+hostToken）、`game/src/ui/MultiplayerSelect.ts` v3（服务器地址默认 127.0.0.1:7778，**端口约定 lobby=WS+1**）、mainFlow 探针桥 `__swFlow.createRoom/joinRoom`。
- 探针：`game/scripts/_roomprobe.mjs`（14 断言全绿：建房/列表/码进/互见/保护拒绝回滚/中继/非公开过滤）；`_landiscoveryprobe.mjs` 兼容（server 忽略旧参数）；旧 `_netprobe.mjs` 已删。
- 文案键在 `tools/l10n-custom/*.json`（RoomProtectTiles/RoomProtectItems），改后须跑 `node scripts/build-l10n.mjs`。

**Why:** 房间制架构约定（端口+1、token 双通道、保护双层：服务端权威+客户端门禁）是后续 NPC/箱子同步（v1 均未同步）扩展的基线。
**How to apply:** 改联机功能先看 docs/multiplayer-design.md §7.3；报异常先起 server 复跑 _roomprobe；勿复活直连模式。

**坑：StatusText 进度误报（2026-08-11 修复）**——进世界后 R3 移动续传首个 30-tick 触发 requestSection → 服务器回 StatusText(0)（fresh 空）→ ClientNet 曾无条件 onProgress → mainFlow ui.showProgress 把全屏进度遮罩重新拉起 = "永久卡在接收世界数据"（游戏实际在跑，被遮罩盖死）。修复：StatusText 仅 `!worldDelivered` 时上报进度。教训：joinRoom 桥的 onProgress 是 noop，测不出 UI 遮罩类回归——_roomprobe 已加真实面板点进房 + `.sw-progress` 遮罩消失断言。

**msg13 v2 远端玩家同步（2026-08-11，对齐原版 PlayerControls，PROTO_VER=2）**：
- 布局：u8 slot + u8 ctrlBits([0]up[1]down[2]left[3]right[4]jump[5]useItem[6]direction) + u8 flagBits([2]hasVelocity[6]ghost) + u8 selectedItem + f32 pos×2 + f32 vel×2。**position=碰撞盒左上**（曾发 cx/cy 中心而接收直写 x/y = 恒偏 10/21px 错位）。
- 远端模拟：`Game.simulateRemotePlayers` 每 tick 用同步控制位跑移动子集物理（stepRemoteProxy：加速/摩擦/跳/重力/moveAndCollide/动画——**不复用 Player.fixedUpdate 全量**，环境伤害权威在各端）；权威包位置差入 `Player.netOffX/Y`（原版 netOffset 语义：<2px 归零、每 tick 收敛 max(2,len×0.1)、超 300px=multiplayerNPCSmoothingRange 归零），Renderer.drawPlayer translate 叠加。
- 加入/离开公告：服务器 `NetModule.JoinLeave=3 {slot,joined}` 广播（原版 Lang.mp[19]/[20] 生命周期点、色 255,240,20、排除本人），客户端本地化为 `LegacyMultiplayer.19/20`。
- 外观：初始两发（PlayerSlot/PlayerSpawn 时刻）都在 applyAppearance 之前 → applyAppearance 后必须 `g.net.resendAppearance()`；MultiplayerSelect 有角色下拉（listCharacters/onPickCharacter，默认选第一个）。
- 探针教训：同步 fixedUpdate 循环测不出移动同步——sendPlayerState 有 66ms 墙钟节流，同步循环只发一包；移动断言必须异步间隔驱动（每步 await ~70ms）。

**v3 实体同步全家桶（2026-08-11，PROTO_VER=3，全部落地）**：
- 架构=**房主权威+服务器中继**（非原版 server-sim）：房主跑完整模拟（刷怪门 `net && !isHost` 才 return），15Hz 变化驱动快照；访客傀儡实体（`Entity.netPuppet/netId` 短路 AI/命中，位置外推）；netId=slot<<24|本地id。
- msg23 NPC：傀儡必须 `Enemy.fromVanilla`（占位 def 缺 defense → hurt 双端分叉 3 点血教训）；傀儡接触伤害 `netPuppetContact` 本地判 AABB（房主 AI 只对房主结算）；boss 置 Game.boss。
- msg42 Strike：上报点在 `Enemy.hurt` 内部（发 rawDmg，房主减算一次）——7 个命中调用点零改动；服务器定向转发房主。
- msg21 掉落：owner 侧 `netDropSweep` 扫描差分（诞生报 spawn/消失报 take）——**傀儡被跳过**，拾取上报在 `netSweepPuppets` 傀儡 dead 分支补（曾漏：访客捡了房主不掉）。
- msg27 弹幕：kind 0-4 泛化记录（Arrow/WeaponProj族/Dart/TrapShot/MagicProj），重建取 Boomerang 占位（共用 drawProj(projId)）。
- msg31/32 箱子：服务器权威（Room.world.chests 来自存档）；msg31 邻域±1 匹配锚点；protectItems 编辑拒绝+全量纠正；Game `netChestWatch` 15-tick 差分轮询统一捕获所有 UI 变更源。
- msg16 HP：客户端权威变化驱动+中继。重连：PlayerSlot 带 sessionToken、服务器 60s slot 占位、ClientNet onclose 自动重试 3 次（userClosed 区分主动断开）。
- **探针环境毛刺**：用户并行改源码 → vite 全页 reload 杀 evaluate（context destroyed）+ headless 背景 rAF 停转——探针已加：动态 import 预热（mkPage）、瞬态异常整轮自重试（ROOMPROBE_RETRY）、A 侧显式泵 fixedUpdate+postUpdate。_roomprobe 现 36 断言，单轮因毛刺可能 1-2 个断言随机挂，复跑即过——**不要当产品 bug 追**。

**msg5 物品/装备同步（2026-08-11，对齐原版 SyncPlayerItem）**：
- 批量变体 `{u16 count, [{u8 playerSlot(服务端覆写), u8 container, u8 itemSlot, u16 itemId(0=空), u16 stack}]}`；container 0=slots[58] 1=armor[20] 2=dye[10]。客户端 slot 分配后全量 dump + 250ms 差分；服务器值域校验+快照累积+中继，新人进场下发他人快照。
- **msg13 selectedItem = 快捷栏槽位索引 0-9**（NetMessage.cs:471 语义）——v1 曾误发物品 id，远端 heldItem 全错。
- useItem 位=左键按住 → Game 派生 `Player.swingNet`（时长按本地公式 remoteSwingDur：剑/近战 max(12,useTime)、镐斧锤 max(14,speed)、其它 30；攻速配饰远端不可见取基础值），Renderer 以 swing 参数消费 → 远端挥舞动画/手持物 holdStyle/盔甲纸娃娃（dollEquipFromInv 读共享 proxy.inv）全通。
- 探针间歇毛刺：vite 偶发全量 reload 清 window 状态（两页同时 __swGame/chatLog 丢失）——公告类断言要尽早做、缩短暴露窗口；不要当作产品 bug。_roomprobe 现 26 断言。
