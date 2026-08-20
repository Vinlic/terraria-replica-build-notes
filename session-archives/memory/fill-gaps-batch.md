---
name: fill-gaps-batch
description: 补齐清单全核销（2026-08-12）——14 项独立子系统落地、测试基线 896→1049、历次勘误汇总
metadata: 
  node_type: memory
  type: project
  originSessionId: 372ae608-2da7-4502-87f6-cedcc2af7bb7
  modified: 2026-08-12T08:38:05.313Z
---

"补齐缺失项"批次完成（2026-08-12，`/goal`）：登记子系统清单 1-14 全核销。

落地子系统：灯笼夜全系统（天气/商店/对话/夜空视觉）/ MoonLeech 145 / 490 仪式圈 / Obstructed 遮屏 / 表面装饰 8 pass（金标逐格一致）/ 幸运度全系统（Luck.ts 七来源+火炬全表+四消费点）/ XACT 17 轨（Sounds/Custom 已解包无需 xwb）/ Glow 拖尾链（仅 154 真拖尾——原登记 4 类有误）/ 图鉴数据层 546 条+DOM UI 面板 / 微光三层转化（312+114 对，coinLuck 接通）/ 弹幕反射管线 / DD2 事件本体（OldOnesArmy 状态机+23 探针）/ bound 链（净化粉 aiStyle 6+Convert case 11）/ 矿车全系统（Minecart.cs 全量+33 用例）/ 小项批 8 项（事件月亮/wave20/火把点光/seedFlags/Housing 8 向/402 自绘/幸运小项/吸血链）。

**Why:** 测试基线从 896 → 1049（全绿）；本批勘误多——坑点：①净化粉是 aiStyle 6 非 2 ②碎镜物品 5577 非 810（810 是 1405 旧弹号）③瓢虫 604/605 非 359/360（那是蜗牛）④敌怪矿车 1.4.5.6 不存在⑤bound 是独立 NPC 类型非 ai 态⑥Glow 仅 154 是拖尾。**补新功能前先核对 1456 的 id/aiStyle——1405 旧号与任务卡描述不可信**。
**How to apply:** 新登记项位置：Shimmer.ts 头注（decraft 反合成等八项）、bossAI_dd2 头注（九钩子已接）、素材批 Glow 注释、图鉴 UI 注释（稀有度/群系筛选字段缺）。联机遗留归并行会话（P2.2/P4/服务器权威）。相关：[[approx-zero-project]] [[event-system-port]]
