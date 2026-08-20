---
name: journey-page
description: 从0到1大师级开发史长页 docs/sandboxworld-journey.html 与其生成器 build-journey.py
metadata: 
  node_type: memory
  type: project
  originSessionId: e65c4575-731a-43e0-a377-ccf50cc42db3
  modified: 2026-08-18T02:25:23.983Z
---

2026-08-15 完成"从 0 到 1"超大型开发过程展示页(用户 /goal:细致整理每日时间线+每场对话,锚定档案文件,要有震撼感):

- **页面**:`docs/sandboxworld-journey.html`(121KB,高约 2.8 万 px,六章):Hero 0→1 → 总账 9 砖 → 长河逐日(12 日面板,每日主题/大事/当日会话芯片)→ 二十四路军团(24 会话卡:开场指令/消耗/成果记忆锚/**session-archives 卷宗链接** 70 个全可达)→ 万坑窟(43 坑四段尸检:现象→排查→根因→修复)→ 转向(11 次路线抉择)→ 心电图四图(12 天数据)→ 尾声
- **生成器**:`tools/build-journey.py`——数据驱动可重跑:输入已持久化到 `tools/journey-inputs/`(journey-data.json 会话+归属 / journey-mining.md 坑史43+转向11+每日主题 / memories.json 全量记忆含日期,重新生成法:扫 memory/*.md 取 2026-08-\\d\\d 日期+name+desc+originSessionId)
- **全量性 v4 终态**(2026-08-16 用户三轮要求后):每日面板三层=叙事主题+全量记忆(169/169)+**全期卷宗实录流 3,554 条**(👤1,627 人类指令+🤖1,927 模型里程碑,**12 天无一日缺席**,逐条带会话徽标可跳转,extract-early-events.py 从 session-archives 开采,sid 归属+时间戳排序+连续去重)。验收:页面 li.arcv==archive-stream.json 总数、逐日全对(见 08-13:807/807)。页面 924KB
- **设计**:深墨蓝+金、宋体章题;滚动进度条/右侧日导航/IntersectionObserver 渐显(尊重 prefers-reduced-motion);图表 hover 十字线复用 chronicle 的 viewBox 修正版
- **时区修正 v6**(2026-08-16 用户两轮指出):v5 已把实录流/统计/曲线全转本地(UTC+8);v6 修复至暗时刻卡残留的 UTC 时刻(05:37/06:10→**13:37/14:10**,源头是已弃用的 early-days.json UTC 旧输入,现已被本地 archive-stream 覆盖,陷阱源消灭)。验收法:抽取 part2/part3/crit 区全部 HH:MM,逐一核对存在于本地实录流时刻集(或已知常量 4:30/19:30/8:15),当前 0 可疑
- **路径脱敏 v5**:esc() 统一清洗 `/Users/user`→`~`;session-archives 中 4 个含 `Users-user-` 的目录已物理改名(index.json/journey-data.json 同步)。验收:输出 HTML 中 grep 不到 user
- **已知解析坑**(build-journey.py 已修):挖掘清单里日期注解有全角/半角括号两种,pit/pivot 正则都要 `[（(]…[)）]`;卷宗块以 `---\n\n` 开头须用 search 非 match
- **v8 全量追新**(2026-08-18):数据刷新至 08-18 上午——27 会话/192 记忆/4,096 实录/171 坑(+12 座 08-17/18 新坑:近战判定盒/多段跳/多弹头/泄露扫除/老人诅咒/树族砍伐/芦苇管/出怪池/建筑族倒数公式/SimHost msg42/行为总批/默认移速)/178,684 条消息/514 亿 tokens/39.1 万行代码(08-18 单日+5.9万);14 天数组;08-17 主题改"行为对齐总攻"、新增 08-18"千人开服评估"面板;**修复五幕重构时数字墙(ledger)整体丢失的回归**;README 索引重建;自主曲线 SVG 重生成为 14 天
- **v7 五幕剧终版**(2026-08-17 用户定向重写):结构=序章(四重不可能)→ 第一幕 以算代眼(五件数学武器:数像素/FNV指纹/相关系数/插桩/IL注入 + 十场保卫战)→ 第二幕 五级台阶(升级是被实墙逼的+两条命运+关键分野+路线分岔WASM对照)→ 第三幕 原则工具与自主(工具军备库表+**自主化曲线图 HUM 逐日人类指令**+08-16 22:14 授权时刻+num4 终夜)→ 第四幕 分水岭(武器清单宣言+六项要求)→ 第五幕 SOP(六步循环+最小复现清单)→ 终章(四条定律)→ 附录 A-E;构建含 zh_punct 中文标点规范化后处理
- **方法论已落盘**:docs/methodology-legion.md(一人军团方法论:三条第一性原理/五层体系 L0北极星-L1标杆-L2裁判-L3军团-L4治理/每日核心循环/人类操作手册/8 反模式/适用边界)——本工程全部实践的结晶,后续同类工程直接套用
- 相关:[[session-archives-export]] [[sandboxworld-project-setup]]
