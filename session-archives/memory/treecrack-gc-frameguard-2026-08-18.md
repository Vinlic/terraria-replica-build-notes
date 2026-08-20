---
name: treecrack-gc-frameguard-2026-08-18
description: 砍树拾取崩溃定位(trace ProfileChunk 法+死亡签名)+inv.add守卫+主循环熔断;行走掉帧=GC churn(lq() 零分配化)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-18T05:50:47.800Z
---

2026-08-18 用户报:行走仍掉帧 + 砍树掉落自动收集时崩溃(traceH)。

**崩溃定位方法(可复用)**:trace 尾部主线程 rAF/timer/microtask 全停但进程
空转 = **rAF 链被未捕获异常炸断的死亡签名**;trace 的 **ProfileChunk
(CPU 采样)含 nodes/samples/timeDeltas**——按 timeDeltas 倒推重建时间线,
死亡前最后非 GC 样本 = `updateLiquidInner`/`get equipStats`(采样 ~200µs
粒度,死点在其后同帧内)。★普通 trace 就带 CPU 采样,崩溃栈可解!
另:死亡窗口出现 hdslb.com(扩展注入)= headless 无法复现的原因之一。

**三修**:
①`Inventory.add` 首行裸 `ITEM_DEFS[id].maxStack` → 未知 id 拾取瞬间
TypeError 炸帧循环。守卫:拒绝入包+`[inv.add] 未知物品 id` warn 带来源栈
(下次触发即可定位是谁产出的 id)。
②`Game.start` 主循环 try/catch 熔断:异常→console.error(进 __swErrors 环,
F5 可取)→停机+Toast.FrameError(双语键已入 custom+重建)。**今后任何未知
崩溃都有现场,不再静默冻结**。
③行走掉帧根因=GC(0.94s/次,5/8 长帧与 MajorGC 重合):`VanillaLiquidRenderer`
四邻 lq() 每调用 new {lq,lt} ×4/格 = 水邻屏 8k-33k 对象/帧 → 零分配化
(标量 nb() 读+四组局部,consider 展开保 L→R→U→D 严格大于语义)。
**残余**:lightAt 元组 3-6k/帧(下一候选,待复测 GC 间隔后再决定)。

复现探针教训:breakTile 直调/Lucy 弹窗/贴脸砍+拾取三轮 headless 均不复现
(缺真实输入路径+扩展环境)——此类一次性崩溃优先上"守卫+熔断取证"而非
盲试复现。

相关:[[imagebitmap-root-cure]] [[webgl2-phase1-port]]
