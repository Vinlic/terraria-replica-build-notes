---
name: load-perf-batch
description: 读档链路零风险优化:worker 回传收窄/fromPacket 免丢弃分配/load 免轮尾扫描/RLE 局部化;decode 150-350ms 构成实测
metadata: 
  node_type: memory
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T03:33:36.539Z
---

2026-08-13 用户问读档速度优化。子代理全链路审计(带行号)+实施四项,闸门全绿。

**实测构成(4.7MB 存档/4200×1200,vitest 环境)**:IDB ~10ms + JSON.parse 15ms + **decode 128-160ms 稳态**(b64 六段 ~47ms + RLE 六段 ~75ms + meta ~30ms;粗测曾见 300-350ms=负载/GC 抖动,勿被吓到)+ settle load(已优化<100ms)+ fromPacket 3ms。afterWorldLoad 4 次全图扫 ~60-100ms + 贴图 IO。**端到端约 300-400ms,非秒级**——用户体感慢多在贴图解码 IO。

**已实施(逐项过 loadSaveData 七数组+fromPacket fnv1a 闸门)**:
1. **worker result 收窄**(worldGen.worker.ts:60):回传 `save: data` → 只留 `{header:{difficulty}, events}`(主线程唯二消费点 mainFlow.ts:275/278)。省 4.7MB 结构化克隆+主线程瞬时双份驻留。协议向后兼容(结构仍是 SaveData 子集)。
2. **fromPacket 免丢弃分配**(World.ts:259):`new World(w,h,seed,name,skipStore=true)` 构造器参数门——跳过默认 TileStore+explored(15B/tile,75-173MB 纯垃圾),**其余字段照常初始化**(store/explored 改 definite assignment `!`)。★第一版用 Object.create 壳路径漏了 weather 等字段初始化,当场翻车(applyWeatherSave 崩)——**构造器旁路必须走参数门,不能 Object.create**。
3. **settle load 免轮尾扫描**(settle.ts:54):原版 WorldFile.cs:738-770 只有一次终态 WaterCheck;轮尾扫描是生成期 pass 49 十轮结构(:16286)的,load 单轮下与终态背靠背白跑。`if (mode === 'gen')` 门住。
4. **RLE 六段局部化**(SaveFile.ts:267-346):盒装 pos 对象→内联游标、typed array 引用提局部、tiles 段 flag/fx/fy 提 run 级常量、内层填隙 `for(;i<end;)` 替 k 计数。逐字节等价。

**实测效果**:decode 160ms 稳态→128ms;主要收益是 ①②③ 的结构性浪费(克隆/分配/空扫)而非 RLE 本身。

**明确放弃**(登记):afterWorldLoad 四扫合一(pylons/trigger/dummy/repairIndex 单遍化)——收益仅 ~50ms,却要在 Game.ts(并行会话最高频冲突文件)重构四个跨模块函数,风险收益比不足;packet 携带活动液体列表(验证成本高收益 21ms);repairIndexFrames 版本门(牵动序列化层)。

**坑**:vitest 单测环境 decode 计时跨 run 波动 128-357ms(load 抖动),单次测量不可信,以闸门哈希为准、耗时取多次分布;fromPacket 计时 0-27ms 波动同理。

相关:[[liquid-settle-perf]] [[worldgen-perf-batch]] [[save-parity-port]]
