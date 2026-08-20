---
name: tile-passability-audit
description: 全物块通行性双向审计:tileSolid/tileSolidTop 全表提取(399条)+站台家具84类+holdsMatching踏台+致动门;tileSolidBackup还原铁律(生成期翻转全是临时);Housing房间边界=纯tileSolid
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-13T17:23:09.293Z
---

全物块通行性双向审计（2026-08-14，用户："检查各种物块的通过性和不可通过性…对齐原版"+追单"家具可站检查"）。

**真值链**：`tools/extract-tile-collision.mjs` ← Main.cs tileSolid(324)/tileSolidTop(84)/TileID.Sets.Platforms(7) 全量赋值+for/ushort 循环展开 → `src/data/vanilla-tilecollision.json`（399 条）→ `tests/tile-collision-parity.test.ts` 双向对账闸门（未注册 flagged=0 恒等）。

**★ tileSolidBackup 还原铁律（判读原版 solidity 的最高优先规则）**：
WorldGen.Reset():11128 先 `tileSolidBackup = Main.tileSolid.Clone()`，生成期一切翻转
（SmoothWorld:16510 裂砖 true / :16694 树叶 false / :16695 裂砖 false / Reset:11500 微光块 false /
FinalCleanup:22306 滚球 false / 17079 蘑菇 true…）都被 generateWorld finally:11108
RestoreTemporaryStateChanges():22678 `Array.Copy(backup→tileSolid)` 整表还原。
⇒ **运行时终态 = Main.cs 初始化值**（裂砖481-483/树叶192/蘑菇190/滚球484/微光块659 全部实心）。
并行会话曾按 :16695 临时翻转把裂砖标非实心+写测试——已按此铁律纠正（cracked-brick-solid.test.ts 重写带机制链注释）。
唯一例外=379 Bubble：DoUpdateInWorld 每帧头 false 尾 true 三明治 → 碰撞语义非实心（RUNTIME_SPECIAL 豁免）。

**碰撞层修复（src/world/TileStore.ts + src/physics/TileCollision.ts）**：
- **isPlatform 三门**：platform 旗 && frameY===0（Collision:2165/:2331 `solidTop && frameY==0` 多格家具仅顶行可站）&& !致动（nactive:2064）。
- **站台家具 84 类接入**（tiles.ts 批量 platform:true）：桌14/469、工作台18/114、铁砧16/134、钢琴87、梳妆台88、书架101、壁炉405、金属条239、种植箱380、渔笼376、全笼族(275-281…710)、队伍平台427/435-439。solid+solidTop 组合(19/239/380/427/435-439) 在本仓=solid:false+platform:true（原版 X 拦截/上顶被 !solidTop 全豁免 ⇒ 碰撞等价）。
- 漏实心补齐：树叶192/裂砖481-483 solid:true（曾被误判反向）。
- **StepUp holdsMatching**（Collision:3713-3721）：Body.stepUpHolds/stepUpNpc；玩家=controlUp（按↑行走可踏上站台面）、NPC=flag22 true+IgnoredByNpcStepUp{14,469,18,16,134}排除集（sheet 比对）。

**Housing 房间边界语义**（CheckRoom:6121 = 纯 tileSolid 无 !solidTop 豁免）：
平台/金属条/种植箱=封房（平台地板可做边界），桌/砧/笼家具=房内格可穿透。
tileSolidLike 实现从 `solid||platform` 改为 `solid || (platform && ROOM_BLOCK_SOLIDTOP.has(sheet))`
（ROOM_BLOCK_SOLIDTOP=vanilla-tilecollision.json 的 solid&&solidTop 集，JSON 派生防漂移）；
floodRoom 边界从裸 `ndef?.platform` 改 tileSolidLike——曾致工作台被当边界不再访问→hasTable 恒假→findFreeHouse 全 null（house-spawn 3 红根因）。

**其他 platform 旗消费者核查**：WaterfallRenderer `solid&&!platform`（金属条改判非墙——原版 tileSolid=true 本应挡水墙视觉，方向登记）；Game.ts 动态光洪泛 expand 含 platform（家具透光=原版 tileSolid=false 一致）；VanillaTiler 仅坡面分支触及（家具无坡零影响）。

**验证**：tile-collision-parity 3/3（含未注册=0 恒等闸门）+ tile-passability 8/8（桌顶站/腿穿/致动门/单向/holdsMatching 玩家+NPC 排除集/漏实心墙挡/Player 全链踏上）+ 探针 **15/15**（scripts/_standprobe.mjs：工作台/铁砧踏台/笼顶站笼身穿/平台站+致动下穿/开门穿关门挡）。
**探针方法论三坑**：①直赋 p.inputX 被游戏每帧注入覆写（Game.ts:3142 touchKeys 才是通道）；②世界入场 spawn 传送晚于探针赋值（需 onGround+位置稳定 settle 门）；③传送后残留 onGround=true 令 waitUntil 零迭代抢跑（赋值处清 onGround）。40×40 迷你世界 StepUp 恒被 `num3>=h-40` 世界底保护门拦截（测试世界须 ≥100 高）。

遗留（并行在途，非本批）： caves/world-hash/fishing/coin/shimmer/draw-side/map-skins(Options.set 400ms 防抖测试未 flush)。
