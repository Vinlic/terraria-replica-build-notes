---
name: bed-sleep-visual-fix
description: 躺床效果三根因(1tick误杀/镜像内旋转角/床偏移双重镜像)与1:1修法;原版无冻结=锚点脚底踩床下地板;引导性视觉提问会假确认
metadata: 
  node_type: memory
  type: project
  originSessionId: 9adce254-f6c0-44ed-947b-3a226dd16828
  modified: 2026-08-17T13:24:05.342Z
---

躺床（上床睡觉）状态效果 2026-08-17 修复，对照 `PlayerSleepingHelper.cs` + `PlayerDrawSet.BoringSetup:336-356` + `TransformDrawData:4199-4230`：

**三根因**（用户报告"躺床上的效果并不对"）：
1. **唤醒误杀**：wake 检查读 `feet+2`（=床下一行地板≠床格）→ 入睡 1 tick 即被杀，效果一闪而过。原版语义 = `Bottom+(0,−2)` 处必须是床格（GetSleepingTargetInfo 可解）+ `frameX/72` 朝向档与 facing 一致 + 任一移动/跳跃输入/骑乘 → StopSleeping（UpdateState :93-117）。
2. **旋转角**：原版 `fullRotation = π/2·(−direction)`、origin=Size/2。本仓镜像 `scale(facing,1)` 在旋转**之前**：`S·R(θ)=R(α)·S ⟹ θ = −α`，两朝向化简后**恒 −π/2**（曾写 `π/2·(−facing)` → 视觉恒 −π/2：变体B床恰好对、变体A床头落在脚尾）。
3. **床偏移双重镜像**：镜像空间内 translate 又乘 facing → 世界位移 = bo（丢了 Directions 乘子），朝左床水平偏移反向（差 2·bo.x）。修法 = 局部直接传 bo 原值（外层 scale 会把 x 再乘 facing，恰得 bo×Directions）。

**Why:** 变换合成顺序（镜像/偏移/枢轴旋转）三个符号互相纠缠，单看一处"对"另一处就错——B 床(facing+1)碰巧三处全对掩盖了 A 床(facing−1)全错。
**How to apply:** 躺床变换已提取 `sleepingTransformOps`（Renderer.ts 导出纯函数）+ `tests/sleeping-bed-transform.test.ts` 逐点矩阵等价断言（头/脚/心/双肩 × 三组床型偏移 × 双朝向）；改这里必须过该测试。床贴图 Tiles_79：变体A(frameX<72)枕右→dir−1、B(≥72)枕左→dir+1。**原版无物理冻结**：锚点把脚底精确放到床下地板顶（床非 SolidTop），重力由地板接住——勿加"睡眠冻结"。SetOffsetbyBed 约 25 床型偏移表已在 Renderer.BED_VISUAL_OFFSET。

**Review 二轮补修（2026-08-17 同日，交互分支 4 处旧偏差，Player.cs:32184-32228 权威）**：
1. ★**极性反**：原版 `!IsHoveringOverABottomSideOfABed → StartSleeping`——**枕端入睡、脚端设重生点**；我们曾脚端入睡/枕端设点。bottomSide 公式本身同款（fx%72<36 XOR 变体B），只是两分支接反。
2. 距离门错式：原版 IsWithinSnappngRangeToTile(:17214) = 悬停格中心(tx·16+8,ty·16+8) vs 玩家(Center.X, **Bottom.Y−16**) ≤ 96；曾用 (tx+2)·16 角点。
3. 重生点坐标帧盲：原版 = 变体A(bedLeft+2)/B(bedLeft+1)、行=**bedTop+2**（床下地面行，本仓 spawnY=落脚格约定一致）；曾 (tx+1, ty−1)。
4. StartSleeping 前置缺：清坐姿（否则坐姿平移+躺床旋转叠画）/收钩爪/试下坐骑（失败由唤醒门拦）/gravDir=1；同床再点=下床、异床点击=换床重睡（:170-175）。
未移植登记：CanSnapToPosition 目标格畅通检查（床位放置链已保证）、RemoveSpawn 再点移除（无原始出生点存档）、pulley 唤醒（单机无链挂）。

**探针教训**：①视觉模型分析会被引导性提问带偏——两次"确认修复"实为幻觉，截图必须先做亮度/内容自检（纯黑=无光场景）；②headless 页面截图管线不可靠（rAF 不触发、合成器不出帧）——能用确定性单测（矩阵合成/录制式 ctx）就别折腾截图；③`page.evaluate` 内 boot 等待勿超 puppeteer protocolTimeout（默认 180s），launch 传 `protocolTimeout`。探针 `scripts/_sleepbedprobe.mjs`（行为断言部分有效：60/60 存活）。相关 [[behavior-parity-batch-2026-08-17]]。


**三轮全量补齐（2026-08-18，"完整移植不能漏"）——登记项全部落位**：
1. **CanSnapToPosition**（PC:32945-32981,Game.canSnapPlayerTo）：目标盒 SolidCollision + canHit 盒视线 + 四组 (w−2,0) 2px 窄条回退 + 横向 ±width 扫掠一步再试；失败=整个入睡静默不发生（隔墙/堵塞不能上床）。
2. **CheckSpawn 房间校验**（PC:53608-53666,Game.checkBedSpawn）：床必须处于合格房间（Housing.checkRoom=StartRoomCheck 1:1）；床上 3×3 净空→BedObstructed；Housing 新增 `lastRoomCheckFail` 穿透 floodRoom 五档失败原因（tooBig/tooSmall/hole/notValid/edge→Game.Bed* 五档文案,ServerMessage=(255,240,20)）；y 上界照抄原版 maxTilesX 笔误；UnsafeWalls 档并入 hole（门禁同,文案折叠,登记）。
3. **RemoveSpawn 再点移除**（:32215-32218 + Player.RemoveSpawn :53686）：World 新增 spawnX0/spawnY0 原始出生点快照（WorldGen/SaveFile(wld)/World.fromPacket/自有存档 header.spawn0 全链持久,旧档缺省回退 spawn）；再点同点回退+Game.SpawnPointRemoved 文案；设点成功文案换原版 Game.SpawnPointSet。
4. **物品使用唤醒**（SH:112-121）：itemAnimTicks>0（每帧由 swing.t 注入 Game.ts:3627——探针须造 swing 不能直写字段）且 damage>0&&!noMelee / fishingPole>0 / ForcesBreaksSleeping{1991,4821,3183}。★damage/noMelee 在 **itemfunc 表**（stats 表只有装备属性——曾查错表恒 false）。
5. **AnyActiveBossNPC**（NPC.cs:81040-81057 AnyDanger 终项）：场上任一活跃 boss→actUp 重置熟睡计时（不唤醒）。
6. **RemoveAllFishingBobbers**（:33120）：入睡前杀全部活鱼漂。
真 N/A：pulley 唤醒（本仓无绳索链挂机制——grep 仅注释）；mount 自定义尺寸子支（坐骑不改碰撞盒）；MP 双人叠床/睡姿同步（无 net 消息,网线协议勿动——曾误加读端险致流错位已回退为回退近似）。探针 `scripts/_sleepbedprobe.mjs` EXTRA 六断言全绿（双床入睡/snap 拒绝/spawn 拒绝/回退/boss 重置/挥砍唤醒）。

**Review 四轮（2026-08-18 同日）三修正**：
1. ★**原版序**:CanSnapToPosition 在 toggle 之前（SH:165-175）——堵塞态连"下床点击"都不响应（只能移动键醒）;曾 toggle 先行。
2. 鱼漂按 ownerRef()===player 过滤（联机不误杀远端漂;vanilla owner==whoAmI）。
3. itemWake 使用窗并入 useTime>0（ForcesBreaksSleeping 三件非挥砍——单查 swing.t 会漏;swing.t 每帧覆写 itemAnimTicks Game.ts:3627）。
另:tile 379 泡泡块——原版静态表 solid=true 但 DoUpdateInWorld(:17675)每帧改 false（通行性既有偏差,登记不动 defs）;CheckSpawn 期间按 solid 算两版一致,床链无影响。

**五轮"登记全清"（2026-08-18）：所有登记/N-A 项落位，无遗留**：
1. ★自查纠偏：床设点原版=StartRoomCheck**纯围合**（家具是 TownNPC RoomNeeds 独立步骤,PC:6000-6057 无家具检查）——曾用带家具 checkRoom 过严。Housing 新增 `checkRoomEnclosure`（floodRoom 选项化 requireFurniture/requireStand/extraSolid）。
2. **UnsafeWalls 档**：floodRoom 漏墙点细分——wall>0 且非房墙='unsafeWalls'（CheckRoom :6171-6176）→ Game.BedRoomHasUnsafeWalls；泛洪越界='edge'。★泥墙 wallHouse[1]=true 是原版事实（Main.cs:10295,可放置泥墙合法）——真不安全墙如地牢墙 7。
3. **tile 379 泡沫块**：defs 改 non-solid（原版静态表 true 但 DoUpdateInWorld :17675 每帧 false）；checkBedSpawn 3×3 与围合泛洪以 extraSolid={379} 补回检查期实心（翻转同构）。
4. **MP 睡眠全链**：msg13 flagBits[0]=sleeping（原版 bitsByte26[0];过服务器中继零改动）+ 变化即时发；代理 proxy.sleeping + 本地 timeSleeping 推进（原版各端跑 UpdateState 模型）；同床叠床 ≤2 人门 + 叠位序（slot 序,视觉 −4px/层 GetSleepingOffsetInfo 第二项）；服务器权威时钟按全员熟睡 ×5（roomHost 1s tick 累计 sleepMs≥2000,ghost 不计分子分母）。
5. **spawnX0 过网**：worldDataFrame 尾部追加两 i32（v8;客户端 remaining≥8 才读,旧服自动回退）。
6. **canSnap 横移精确化**：scratch Body 走 moveAndCollide 判位移完整（TileCollision(x)==x 同构;stepUp 关/dropThrough 开=fallThrough,ignorePlats 口径）。
7. **静持物随躺转**（段A 火把等手持层原版在 DrawDataCache 整组旋转）：世界空间施加 off+绕盒心 π/2·(−facing)。
8. **sleepingBedOffset 精确化**：先读 Bottom−2 床格 frameY/36（GetSleepingTargetInfo 同格），7×4 扫描退化为代理插值兜底。
真·空集（有据）:pulley 唤醒（引擎无绳索机制,grep 全库仅注释）;mount 自定义尺寸子支（坐骑不改碰撞盒,恒 20×42）。测试：bed-spawn-enclosure 4 项 + 全家桶 31/31;探针六断言全绿。

**六轮 Review（2026-08-18）两修正 + 一顺手解封**：
1. ★**canSnap 浮点等值 bug**：`body.x === p.x+num·p.w` —— moveAndCollide 按 ≤8px 分步累加，任意起点处 dx/steps×steps 有 ~1e-14 尾（node 实证 from100: 120.00000000000001）→ 横移试探几乎恒 false。改 epsilon<0.01。★分步位移的"全位移"判定永远用 epsilon,禁用 ===。
2. **checkRoomEnclosure 直锚点**：原版 StartRoomCheck 单点入栈（:6031-6034），无 ±1/dy 探测（那是房门锚定用）——曾照抄 checkRoom 探测会在床贴门洞等边角判进隔壁房间;锚格实心→notValid(StartedInASolidTile 走 default 档)。
3. 顺手解封并行会话 boot 炸点:TrapsPass.ts 裸 `process.env.SW_EEEE_DBG`(浏览器无 process)——按同族 LT_TRACE/PYR_TRACE 的 typeof 守卫模式补齐。
验证:enclosure/housing/sleeping 23/23 + 探针六断言全绿。
