---
name: liquidtype-plus-one-encoding
description: "TileStore.liquidType 是原版+1编码(0无1水2岩浆),照抄原版 liquidType==0/!=0 的移植必死循环;水中箱两案"
metadata: 
  node_type: memory
  type: project
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-12T14:46:55.253Z
---

TileStore.liquidType(TileStore.ts:14)采用**原版+1 编码**:0=无 1=水 2=岩浆 3=蜂蜜 4=微光(原版 LiquidID: Water=0 Lava=1 Honey=2)。所有从 C# 照抄的 `tile.liquidType() == 0`(判水)/`!= 0` 移植必须改成 `=== 1`/`!== 1`。

**Why**: 2026-08-12 世界生成卡死"生物群系 8%"(浏览器显示 6%)根因 = BuriedChestsPass.ts runWaterChestsPass 的拒绝采样 `while (liquid<250 || liquidType!==0) 重掷` ——水格 liquidType=1 恒真→**永不命中的死循环**(pass 是同步函数,worker/主线程事件循环全停,setTimeout 看门狗与 --cpu-prof 落盘都不会执行,只有外带手段能诊断)。同类静默失效:OceanCavesPass.ts:198 `liquidType===0` 永假(海洋洞窟水中箱特性从未生成)。两处已修(===1/!==1),grep 全库确认无第三处。

**已建三层防御(2026-08-12)**:①TileStore.ts 导出 `LIQUID_TYPE` 枚举(唯一真源,移植禁裸写 0/1/2,枚举注释含血案+grep 排查式);②水中箱拒绝采样加百万掷守卫——超限 console.error 点名降级继续(不再静默死循环);③WorldGenClient 静默看门狗:生成中 >30s 无 worker 事件 → console.error 报"最后进度 X% label + 静默时长 + pass 内死循环排查指引"(原有 3 分钟硬超时 terminate 保留)。

**How to apply**:
- 新移植液体判断时一律先查 TileStore.ts:14 的编码注释;全库判水模式 = `st.liquid[i] > 250 && st.liquidType[i] === 1`(BeachPass/LakesPass 写侧同为 1)。
- 存档/联机协议侧另有各自的 liquidType 编码(serialize SaveData 注释同 TileStore;protocol strip 裸传 store 值)——三方同源,但与原版 C# 不同。
- 排查同步死循环的方法论:pass 级进度日志定位组 → 在 vanillaBiomes 内逐子 pass 插 `fs.writeSync(2,...)` 计时(ESM 无 require!)→ 最后一个 tick 的下一条语句即卡点;Node --cpu-prof/--inspect 在同步死循环下无法落盘(事件循环停摆),插桩法最可靠。诊断脚本 _worldgen-prof.mjs 已删(复刻:generateWorld + 文件日志,Node 直跑绕开 worker)。
- 相关 [[js-bitwise-int32-traps]](拒绝采样死循环家族)、[[vanilla-worldgen-port-status]]
