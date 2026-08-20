---
name: multiplayer-capacity-opt-batch
description: "2026-08-12 联机容量优化批 P0-P3 全量落地:AOI/短码表 v4/合包/strip缓存/持久化/插值,文件与探针索引"
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-12T04:50:16.024Z
---

**msg4 hairDye 外观同步（2026-08-14，发色剂批遗留销核）**：hairDye 并入 SyncPlayer
外观 JSON 三点——ClientNet 入房上传/resendAppearance 注入 + Game.simulateRemotePlayers
代理解析注入（Renderer.hairDyeRenderColor/派对彩纸消费位）+ Game 染料使用点调
`net?.resendAppearance()`。服务器 room.ts 对 msg4 盲存盲转（字符串透传 slice 4096）
→ 零协议改动零 PROTO_VER 升版。**两坑**：①resendAppearance 旧 `if (p?.appearance)`
守卫在裸加入流程（无角色档）静默吞掉重发——改为只看连接态（原版 msg4 本就无条件发）；
②_roomprobe 页面游戏循环不自动跑（全程手动 fixedUpdate）——读代理派生状态前须先驱动
若干 tick 且**复位位置**（重力沉降 10px 会打穿下游"坐标零错位"断言）。探针断言
wire=9/proxy=9 两绿；既有抖动集（掉落物 msg21/protectItems/物品同步/傀儡hp 收敛）
逐次运行浮动 3-6 条与本批无关。裸 WS 假客户端路线不可行：服务器 broadcast 只发
state>=10（世界组装完成）的客户端——探针必须走真浏览器页。

**观战 review 修（同日）**：键位切换路径漏 5644 持握音效——原版音效块在
HandleSpectatingControls 内（:16961-16971），键/鼠标两路都播；抽 spectateCycle(step)
共用段（SpectateNextPlayer + 197/198）。复查核毕：消费序（spectate tick 3341 在
updateUse 3703 之前=观战期使用冻结有效）；断线目标→相机同 tick 退出（controls 在
相机前跑）；Space 在 UI 打开时退出=原版 controlInv 同族退出语义非误触。

**观战系统全链（2026-08-14，占卜球 5644 引擎级缺口销核）**：Player.cs
:16931-17122 1:1——CanSpectateNet（死亡滞留窗 180t :1528）/AnyoneToSpectate/
SpectateNextPlayer（±step 环形 255 槽，单机恒 false :17044）/setSpectating +
**msg150 SpectateFocus**（服务器把该端 AOI 过滤中心从 avatar 切到目标——
broadcastAt 逐端取 spectateSlot 目标 lastX/lastY；旧 server default 忽略=优雅
降级故不升 PROTO_VER）/SpectatingCameraPosition（代理 Bottom−21+netOffset）。
**键位两半边**：keydownHandlers（Space/Escape 退、←/→ 切——Input 无 keyEdge，
事件天然边沿）+ tick 半边 handleSpectatingControls（鼠标左右切+吞输入=观战期
移动/使用冻结+目标失效自动换/退）。**条带跟随**：strip 请求轮（%30）取相机位
（=RemoteClient.CheckSection 观战段 :17118 等价）。5644 使用支：有目标→关全 UI
（新回调 onCloseAllUI→ui.closeAll）+Item197+观战；无目标→Item198+单机
SpectateSinglePlayer/联机 SpectateNoTargets（此前恒走无目标支）。**未移植登记**：
虫洞药水传送（QuickBuff+同队 :16940-16946，unity potion 链未建）、死亡自动观战
（CanDeathSpectate）、NoMoreTargets 相机推挤、观战 UI 名牌条（以聊天行
SpectateHintChangeTarget 近似）。探针 _roomprobe 七断言全绿（锁定/msg150/相机
收敛 0px/输入冻结 0px/Space 退出/回落 0px）；既有抖动集（msg5/掉落物/protectItems/
HP 中继）逐次浮动 3-6 条与本批无关。

2026-08-12 实施联机容量优化批(计划文档 ~/.claude/plans/smooth-cuddling-hamster.md),P0-P3 全量:

- **PROTO_VER 3→4(v5 见下)**(server 与 game 同仓库必须同时发布):msg23 S→C 改短码格式(1B eflags: bit0=含key全量 u32 netId+u16 codeId+str key / bit1=boss;否则仅 u16 codeId);RoomPolicy 尾部追加 u16 maxPlayers;顺手修正 protocol.ts msg42 注释(实际线格式=dmg+kbx+kby,非 crit/kbDir)。
- **AOI**(server/src/room.ts):msg13 半径 1920px/msg23+27 1280px,滞回外径×1.6(每客户端 aoiNpc/aoiProj 滞回集);接收端位置取其上行 msg13。**盲端(>5s 无 msg13)语义=跳过实体广播**(初版"全视野兜底"实测在饱和时形成放大循环:msg13 滞后→判盲→全量灌流→更饱和,百人 boss 25.6MB/s;改跳过后 18.5MB/s)。**msg21 掉落不做 AOI**(spawn 一次性无重播,过滤=永久不可见)。客户端联动:>1.5s 无 msg13 冻结远端代理输入(Game.simulateRemotePlayers)。不变量:NPC 2s 兜底(120t)≪傀儡清扫 300t。簇拥场景有"全员全量"快速路径(单帧广播零重编码)。
- **合包**:Room.send 入 outbox,ws message 回调末尾 flushOutbox 拼发(512KB 切片);上行 msg21 攒批(ClientNet.pendingFrames,tick 冲洗)。背压分级 ≤1MB 正常/1-4MB 丢 prio=1/ >4MB 全丢,/stats 全计数。**两个实测竞态**:①FrameParser MAX_BUFFER 必须>合包切片(256KB 旧值会把进房 25-strip 大包整包丢→世界组装永久卡死,已提 4MB);②Kick 须先 flushOutbox 再 ws.close()(close 置 CLOSING 后 send 静默丢,客户端只见断连不见原因,Room.kick() 助手)。
- **/stats**(server/src/stats.ts):GET lobby:7778/stats,1s outBps 差分采样(startBpsSampler 传 getter 非快照数组——后建的房也要采样)。
- **maxPlayers**:`--max-players` + POST /rooms.maxPlayers 钳[2,255];slot 数组物理上限恒 255(resumeSession 按物理上限校验)。内存护栏 `--world-budget` 默认 2GB(w×h×11B)、`--upload-limit` 默认 96MB。**坑:2<<30 溢出 int32**(见 [[js-bitwise-int32-traps]])。
- **持久化**(server/src/persist.ts):--world 常驻房(hostToken='' 首进者为房主,persistent 豁免空房回收)+ --save-interval 300s(空房无 tileOps 跳过) + SIGTERM/SIGINT 落盘退出;saveWorldOnly(SaveFile.ts,不含玩家)。修复开服.sh --world 挂账。
- **P3.2 插值**:Entity.netSnapTo/netPuppetStep(smoothstep 4tick),逻辑位 netAx/netAy(接触判定用),渲染位插值;各弹幕类傀儡分支统一 `netPuppetStep()`。
- **FrameParser 增量化**(protocol.ts):单缓冲+偏移+copyWithin,drain 回调内禁 append(_draining 断言)。
- **strip 缓存**(P2.1):Room.stripCache LRU 512,applyTileOps 按条带原点归一化失效。

探针:game/scripts/_netfake.mjs(共享线协议假客户端+makeTinySave 全空气小世界档+spawnServer),_loadprobe.mjs(压测,--clients/--density/--spread,平均带宽用累计字节自算),_roomprobe.mjs 50 断言全绿(满员Kick/AOI三态/短码表/stripHit/SIGTERM持久化/--world 重启)。实测:32人calm簇拥1.43MB/s vs spread 0.68MB/s(-53%);100人boss簇拥18.5MB/s(=带宽物理上限,全互见不可约);review 修复后复测 1.42MB/s 零回退。设计文档 game/docs/multiplayer-design.md §8bis 含实测表。**review 修复批(2026-08-12,双代理审查+逐条核实)**:①msg23 客户端未知短码必须**先读完本条字段再 continue**(否则读指针错位毒化连接);②netApplyNpcSnaps 构造失败 return→continue(未知怪致同帧其余傀儡饿死被误清);③FrameParser 缓冲压缩挪进 finally(回调异常→永久重放);④NPC/弹幕广播 >=24 break 改游标轮转(否则第25个起永久饿死);⑤stale 冻结须含 useItem(防无限空挥);⑥外观 JSON.parse 仅变化时解析(60TPS×每人纯浪费);⑦npcKnown 标记晚于 send 成功(prio=1 丢帧后可重发全量,防 NPC 永久隐身);⑧箱子编辑独立脏标记 chestEdits(否则空房跳过落盘=物品复制漏洞);⑨TileBatch 先滤非法 op 再广播;⑩内存预算 11→15B/格+stripCache 32MB 字节上限;kick 旁路背压直发;msg27 单条非法只丢本条。**v5 补齐批(2026-08-12)**:①敌对弹幕访客伤害——msg27 kind bit7=hostile(仅 kind0/Arrow),访客 netPuppetProjContact 本地结算(hitPlayer=原版 Damage_EVP 1:1,命中不耗穿透);**原版语义=玩家伤害各端本地结算**(同 netPuppetContact 模型),不走 msg42(那是 NPC 受击链);敌对弹全是 new Arrow(...,{hostile:true})(bossAI 各文件),hitPlayer/statusPlayer 在 entities/projTargets.ts;②session 认领制——建连只 claimed 不删条目,Hello 成功才消费,握手前断线释放认领(修复二次重连失效+slot 永久泄漏)。PROTO_VER 4→5,_roomprobe 53 断言全绿。**review 第二轮(对抗审查,已修)**:①Dart/TrapShot 补 hostile 字段(敌怪弹=Enemy.shootDart 咽喉+3直构处置位;TrapShot=构造时 !style.friendly;玩家弹默认 false 防 friendly fire)——否则普通射击怪远程弹访客整体免疫;②服务器剥除非房主的 msg27 bit7+dmg 钳 9999(否则任意访客伪造 hostile 弹秒杀他人=无 PvP 开关的强制击杀);③msg21 op=0 三重校验(netId 高8位=发送者 slot/key 反查 ITEM_BY_KEY/stack 钳 maxStack)——堵凭空造物直塞背包;④盲端免伤漏洞:停发 msg13→判盲→傀儡空→免疫一切伤害,且 Ping 心跳让 120s 看门狗永不触发——对策 blindAbuser(盲>15s 发操作类消息即踢,合法后台挂机不发操作);⑤session 超时回调按条目世代判等(防同键新条目被旧定时器误删)+迟到 Hello 复核条目仍在(防超时后双占 slot);⑥NaN 坐标清洗(msg13/23/27/21 Number.isFinite);⑦空房且脏即时落盘(ws close 钩子,复制窗口 300s→~0);⑧弹幕接触判定用权威位 netAx/netAy;⑨netProjLast 差分清理。**挂账清偿批(v6,2026-08-12 第三轮,PROTO_VER 5→6)**:①上行限流(每客户端每秒 per-msgId,阈值=合法峰值3-6倍,超限踢,§6.2兑现);②prio=0 帧>4MB 不丢改踢慢客户端(带原因);③房主迁移公告(Text 模块 slot=255=服务器直显,客户端无名字前缀);④AOI 实体内径 1280→1536px(消对射空洞,带宽+20%);⑤msg28 弹幕消亡上报(各端消亡批量netId→中继→即时移除傀儡,消幽灵弹窗口);⑥Boss 锚定弹体同步 kind 5-8(DukeSharknadoBolt/龙卷/MLDeathray/LunarOrb)——**访客重建真类本地跑确定性 AI**(锚=msg23傀儡按 netId 回溯,netProjMeta() 打包 tag/aux/exVx),spawn 副作用 !netPuppet 门禁(出鲨/落龙卷/线发576);⑦--ssc 服务器角色档(msg201:msg5/16/13累积→断开落盘 server/ssc/<name>.json→同名重连下发,存档型同原版 SSC 非反作弊);⑧重连清掉落 netId 重播 spawn。**判定位定论**:敌对弹幕接触判定用渲染位非权威位(权威位在差分间隔内冻结→慢速弹系统性漏判,F3 实测翻案)。**_netfake 坑**:假客户端 Msg 表缺号(SyncPlayerItem/PlayerLifeMana/ProjDespawn/SscSync 曾 undefined→帧头 msgId=0 被服务器默认丢弃,SSC 测试全空值的根因)。探针 54 断言(msg28 即时移除/hostile 伤害/msg16 中继),54/54 全绿一轮;并行会话高负载时 headless 页饿死会 flaky(47-54 波动,签名=B 收不到房主流)。剩余挂账:msg17 无重放(原版同款)、限流阈值经验值待 /stats 调优、ItemDrop 傀儡本地直接拾取(乐观模型与注释不符,已知语义偏差)、msg8/31 无限流。**终审批(第四轮,三路交叉,已修)**:①SSC 双缺陷——msg201 与 PlayerSpawn 同批+loadWorld await 让出栈→应用到旧 Player 丢失,改暂存(net.pendingSSC)loadWorld 完成后消费;世界下载期断开(state=10,msg13 未到)空背包+(-1e9)坐标覆盖好档,落盘加 lastPosAt>0 守卫+定时刷盘;②重连傀儡残表——entities.clear() 后三傀儡表持孤儿,同 netId 命中孤儿只 netSnapTo 不重新入桶→永久隐形+孤儿 NPC 摸人,onWorldReady 全清(傀儡表+差分基准+箱watch+远端代理);③限流按帧计重估(SyncItem 60→300/StrikeNPC 120→240);④空房回收改空置时长(原按创建年龄误伤 60s 重连窗);⑤凭据恢复名字以 session 为准(防 SSC 按名错位);⑥/stats 加 kicks;⑦v6 锚定 netId 合成改乘法(`<<24` slot≥128 溢出 int32——js-bitwise-int32-traps 第三犯);⑧msg28 上行分片/Bolt exVx 速度通道/Bolt+Orb 重建坐标左上→中心换算。修后 54/54 全绿×2。**死码清扫轮(第五轮,已清)**:死码 10 处(ClientNet 未用 import TileStore/TILE+零调用 sendChat(聊天 UI 未接线,收包侧保留)/protocol i8 双向+get pos/chestFrame 死参 except(调用方 broadcast except 承担)/entitySyncHooks reportSpawn+reportTake(掉落上报实际走 netDropSweep 直调,LunarOrb explode 死局部 st/探针 ''+..+'' 空拼接);注释 14 处(strip 字节账 11B→16B/run 修正——全异态 4000×16+15=64015<65535 余量仅 1.5KB 扩 strip 前必核!、R10 timer 曾 void 空转已改 fail 内 clearTimeout、Arrow/Dart 三处"伤害归拥有者结算"改双语义、hostile 覆盖 kind0/2/3、state 枚举去"3"、kicks 来源补全、探针文件头 v3→v6 等)。**环境坑**:vite preview 偶发服务空响应(404/空 body),kill 重启即好;load>15 探针必 flaky 第五次验证。清扫后 54/54 全绿。**hello 处理器改名字读取时注意:字段只能读一次**(改凭据名保护时曾引入双重 r.str() 把 token 读成名)。**近似收紧(第三轮补)**:MLDeathray 束角快照回写(exVx/exVy 消费式同步,读后清零防回拉振荡);DukeSharknadoTornado 生长态携带(tag=big,ai1,ai0+快照段盒反解 topY,确定性对齐)。剩余近似=原版同款模型代价(Orb 随机抖动双端异掷/猪鲨狂暴速度差/液体束长差),msg28 兜底有界。**环境教训:load>15(vitest 舰队/多 Chrome)时探针必 flaky,等负载回落再跑**。**已知保留**(评审确认不修):断连窗口掉落 spawn 丢失、msg17 >4MB 无重放(原版同款,靠后续包自然收敛+重连兜底)。**探针经验**:①并行编辑引发 vite 全页 reload 杀探针时,用生产构建跑(vite build + preview --port 5299,PROBE_GAME_URL 环境变量指向);页内 import('/src/...') 仅 dev 可达,须走 __swFlow 探针桥(itemByKey/spawnVanillaEnemy);②headless 后台页 rAF 停转,所有泵(fixedUpdate+postUpdate)必须在 evaluate 里显式做;③SIGTERM 必须**单播主进程**(0.5s 落盘✓),组播 TERM 与落盘并发静默死亡(机制未定,killGroup 已改直杀+5s 组杀兜底)。遗留:P2.2 增量快照(仅当 /stats 显示 msg23>40% 出带宽)、P4 permessage-deflate/msg13 自适应节流(数据驱动)、服务器权威 NPC(P5,接口已留:npcAuthority()/strikeTarget())。相关 [[multiplayer-room-system]] [[diag-script-orphan-prevention]]
