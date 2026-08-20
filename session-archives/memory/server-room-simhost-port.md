---
name: server-room-simhost-port
description: 服务器权威房(SimHost)B1-B3 批落地——进程内虚拟房主经 room.handle 复用中继管线;GM 规则执法;协议 v8 增量纪律
metadata: 
  node_type: memory
  type: project
  originSessionId: a476813d-a6ae-471c-84eb-8f868a94a617
  modified: 2026-08-18T08:10:11.383Z
---

# 服务器权威房 SimHost 移植(2026-08-17 B1-B3 批)

**生产修复二:worker 整体崩毁(2026-08-18,用户报障)**:`room.clients.filter is not a function` → worker exit(code=1)全房失联。根因=并行会话在 roomHost 时钟推进 interval 加"全员熟睡×5"时对 **Set 用了 .filter**(room.clients=Set 无此法)——**无守卫 setInterval 内一次抛错=worker 整体退出**(B6a 周期定时器全部裸奔)。修=①Set 先展开 `[...clients].filter`②四个周期定时器(时钟/看门狗/10s 广播/落盘)逐房 try/catch 只记日志。验证 _sr-probe 25/25+_aoi-probe 8/8。★教训:**并行会话向 worker 加周期逻辑时,无守卫 interval 是全局崩毁面——roomHost 的 interval 一律逐房 try/catch**;Set×数组方法(此前 clients.find 也实踩过)。

**生产修复:UI 选角加入崩溃(2026-08-18,用户报障)**:`Cannot set properties of undefined (setting 'appearance')` @onJoinRoom——`makeGame().player` 在联机加入流程要到 loadWorld(世界数据到达,Game.ts:2816)才创建,MultiplayerSelect onJoinRoom 提前 `g.player.appearance=selectedAppearance` 踩空(仅选了角色的真实用户触发,探针无角色路径测不出!)。修=预置 `g.pendingJoinName`(Hello 名兜底,ClientNet connect 三级链 player→pendingJoinName→'玩家'),外观本体仍由 onWorldReady 的 applyAppearance 落位。验证 `_uijoin-probe.mjs` 8/8(页面 CharacterStore.create 播种角色→真实 UI 点选→点房→进房成功+PlayerActive 帧带真名)。★方法论:**探针必须覆盖"选了角色"的真实用户路径**;其余两处 appearance 早写(更衣窗回调/applyAppearance)核过安全(player 已建)。

用户目标"开在服务器上的房,世界由服务器计算"已落地 MVP(docs/server-room-plan.md 为权威台账)。

**核心架构(最低侵入)**:SimHost(`server/src/sim/SimHost.ts`)= 进程内"虚拟房主客户端"——以上行帧格式(C→S msg23/27/21/28)构造,经 `room.handleFromSim()` 走**与房主完全相同的中继管线**(AOI 滞回/短码/背压/限流零旁路)。`room.ts` 预留注释 `this.sim ? false : c.isHost` 的实际落法更优:**serverAuth 房 Hello 永不晋升房主**→全部既有访客门(Game.ts:13351 刷怪/:4081 世界事件等 ~30 处 `!isHost` 门)自动生效,客户端改动收敛到召唤路径一处。

**关键事实**:
- `entities/types.ts:4` GameHooks 接口缝=实体层本就面向接口;`Enemy.shootDart` 经鸭子 cast 访问 `game.entities`(hooks 须公开 entities 字段);死亡掉落链全在 Enemy 内经 hooks.spawnDrop 出→SimHost 继承全部 1:1 掉落管线
- 合成 avatar:真实 `new Player(x,y,new Inventory())`(构造无 DOM,Player.ts:439);**逐实体摆到最近在线客户端**=多人最近目标语义且 Enemy.ts 零改动;掉落/弹幕更新期摆 -1e9(服务器不拾取、敌弹不命中——victim-settles 各客户端本地结算)
- Boss 召唤必须镜像 Game.summonBossAtTx:18314-18356 的 fromVanilla+链(世吞 65/70 节链/双子第二只 126/毁灭者地下落位)——`new Enemy(key,x,y)` 直放是错的!
- 液体不做逐格广播(协议无液体 op):SimHost 与各客户端跑同一份确定性 LiquidSim,输入一致收敛;进房 strip 反映服务器演化态(备案近似)
- **handleFromSim 尾部必须 flushOutbox()**——静默房无 WS 入站消息,P1.3 冲洗点只在 ws message 回调
- netId owner=255(服务器段);`255<<24` JS 位运算产生负数但 NetWriter.u32 `>>>0` 序列化回正确无符号

**协议 v8(增量纪律,不升 PROTO_VER——SpectateFocus=150 同款先例)**:RoomPolicy 尾部 u8 ruleBits(bit0 serverAuth/bit1 禁Boss/bit2 禁破坏/bit3 禁放置/bit4 禁PvP/bit5 禁爆炸物/bit6 和平);Msg.SummonIntent=202(str npcKey+f32 x,y,vx,vy,客户端算好落位,服务器只查表+规则门);`RoomRules/rulesToBits/rulesFromBits` 在 protocol.ts 双端共享。

**GM 系统**:gmToken 建房生成(POST 返回/`--server-room` 常驻房内部生成);URL `?gm=` 或聊天 `/gm <token>` 认证→isGM 规则豁免;`/rules` 回显;PATCH /rooms/<code>/rules 热更→updateRules 联动 SimHost+RoomPolicy 重播。执法门全服务器端:forbidBreak/Place 按 TileOpAction 分立(protectTiles=整包语义不变);爆炸物=单批>24 清格启发;forbidPvp 复用 pvpAllowed 墙。

**探针**:`scripts/_sr-probe.mjs` 19 断言全绿(复用 _netfake.mjs 的 spawnServer/makeTinySave/Writer)。坑:探针 TileBatch 帧必须带 SetTile 的 fx/fy 尾字段;全空气微型世界自然刷怪不保证(改用 SummonIntent 确定性验证管线);PATCH 路由正则别复用 `/rooms/(\d{6})$` 的 m。

**回归定责法(无 git 仓库!)**:vitest 8 失败(town/vanity/wing/worldgen)+_roomprobe 物品断言——全归并行会话在途物品表编辑(vanity 400≠402 是铁证;`ITEM_DEFS[4798]` undefined 崩 `.key`),本批 diff 零 `.key` 访问可证清白。中继房共享路径(房主门/双保护/AOI/观战)全绿。

**B4 批完成(同日续)**:①ioWorker(`server/src/workers/ioWorker*.ts`)——parse=worker JSON.parse 回传纯对象;stringify=主线程 buildSaveParts(SaveFile 增量抽取)廉价视图→memcpy 克隆进 worker 做 RLE+stringify;故障/超时/队满全回退同步;SIGTERM=等在途→同步兜底→ioShutdown。②刷怪链全镜像 Game.trySpawnEnemy(旗标灌注+蠕虫链/水生/贴地/净空/萤火虫附加/骷髅商+bound TownNPC 转化,TOWN_SKIP 退役)。③入侵链(tickInvasion 推进+击杀扣分+日出沿自然 roll)。④SSC 强制(serverAuth 房不依赖 --ssc)。⑤浏览器 E2E `_sr-e2e.mjs` 15/15(真实客户端建房→访客→傀儡→召唤意图→Boss v_50 可见→msg42 打击→服务器结算→移除;探针坑:msg42 dmg 是 i16 用 9999 勿用 99999 会回绕)。
**探针总账**:`_sr-probe`(Node)20/20 + `_sr-e2e`(浏览器)15/15;双绿=验收门。
**并行会话撞车实录**:worldGen worker 运行期爆栈(栈溢出)系第三方在途改动(进程内 vitest 双种子全绿可证),E2E 用 `__swFlow.loadJson` 载现成档绕开——**浏览器 E2E 不必依赖 worldgen**;探针解析 msg7 时偏移 bug 连犯三次(长度当偏移),教训:手写 Reader 累计偏移必须 `o += len`。
**review 批+ B5(2026-08-18)**:自审修 4 件(step 异常防护+连续 600 次停机/召唤 Boss 傀儡预检/聊天命令只拦已知防吞正常聊天/take 重复抑制);AOI 空间索引落地(broadcastAt 2048px 网格桶+观战线性兜底★按自身位入格会漏观战者+msg23/27 整批包围盒早退;_aoi-probe 8/8);日食 roll 内联+夜沿清(避开 Eclipse.ts 的 Lang 依赖)。三探针台账:_sr-probe 20+_sr-e2e 15+_aoi-probe 8。
**B6a 房间进程化(2026-08-18 完成)**:Room/World/SimHost/persist/SSC **零改动**整体进 worker_hosts(`server/src/roomHost.ts` K 房/工,ShimSocket 还原 ws 背压语义=未ack字节+主进程回报缓冲);主进程 index.ts=lobby 路由+WS 装配(★早到帧缓冲——connOk 往返期 Hello 不丢;★onHostEvent 里 connOk 必须在 conns 守卫之前——曾全房进房超时);`--workers N` 多工扩展+stats 合并。★worker 加载 TS 的唯一解=**mjs 入口 `register()` tsx**(execArgv --import 三式全无效,Node 原生 strip-types 见 const enum 即炸)。验证:三探针 20+8+15 零改动全过+W=2 冒烟。坑:spawnServer killGroup 的 npx 转发慢+run-diag 0.5s 强退竞态会留孤儿(W=2 测试实测),手动 kill -TERM 直杀即退。
**聊天系统+世界频道批(2026-08-18,plan §14)**:客户端此前无聊天输入(只有显示)!补全:ChatInput(Enter 开框/Tab 切频道/300ms 重开抑制/键处理挂 window capture);协议 Text 尾部 u8 channel(0房/1世界,增量);世界链=Room 上抛→main 扇出全 worker→逐房 broadcastWorldChat([世界]<名>+金色,author=255,含回显);反刷屏 10s/8条;双房型同路径。验证:_sr-probe 25/25+_sr-e2e 20/20。★headless 键盘发送跳点悬案:监听器触发+各下游环独立全绿但链路在 CDP 语境断——证据指向页面闭包/模块双载,真机手动验证即可;生产已 window 活实例双路径加固。★诊断方法论:分级取证(页内埋点/服务器收帧日志/直调对照)+**先查环境再查代码**(vite 陈旧模块图/端口残留孤儿各浪费过整轮)。

**千人单房优化批(2026-08-18 续,plan §13)**:差分剖析(relay 11.6% vs sim 82.1%@120bot=模拟占86%);三优化落地:①玩家1024px网格(avatar最近目标 O(E×P)→格查,灭平方项)②trySpawn 4tick一掷概率×4(期望不变,统计O(E)砍75%)③AOI密度降频(msg13 拥挤格>16降半>48降三,插值低频设计视觉无损)。**实测:120分散CPU 82→28.6%,60聚集人均10.8→3.27KB/s(-70%)**;千人外推=带宽24-48Mbps+CPU~1.6-2.5核→**最终形态简化为"中继线程+模拟线程"双线程(B7),无需分区并行**;SAB背衬TileStore(additive开关)为B7关键件。slot u16仍gated于worldGen worker修复(_roomprobe为门)。三探针20+8+15零回归。
**千人实测(2026-08-18,`_load-probe.mjs`)**:60分散/120分散/60聚集=人均0.44/1.05/**10.8KB/s**,worker CPU 46.6/82.1/59.8%。1000CCU今日拓扑=多房分线→8vCPU/16GB/100Mbps。国内带宽:常态热点型千人≈10TB/月≈8000-9000元(按量0.8元/GB),均匀分散型≈1.5-2.5TB。测量坑:★startBpsSampler须随迁worker(已修);★探针单位B/s误标KB/s造"洪水"假象——**双口径互证法**(bot收 vs /stats出)必用;随机端口防跨跑孤儿。相关:[[multiplayer-capacity-opt-batch]]
