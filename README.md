# SandboxWorld Chronicle

> 一项为期 16 个日夜的工程实验:由一名人类与 GLM-5.3 模型(通过 Claude Code 界面驱动),将闭源商业游戏《泰拉瑞亚》1.4.5.6 复刻至"同一种子生成逐格相同的世界"的程度,且全程可审计。

## 这个仓库是什么

这不是游戏源码仓库。这是一份**完整的工程过程档案**——记录了整个复刻工程是如何从一句话需求出发,经过 16 个日夜、31 路会话、205,781 条人机对话,最终达到位级一致的全过程。

| 内容 | 说明 |
|---|---|
| `index.html` | **主展示页**(从0到1 · 五幕叙事 · 可直接浏览器打开) |
| `docs/methodology-legion.md` | 方法论文档(一人军团方法论) |
| `docs/upgrade-1405-to-1456/` | 1.4.0.5 → 1.4.5.6 版本差异分析 |
| `session-archives/` | **全量对话记录**(31 会话 · 622 子代理 · 20 万+条消息) |
| `session-archives/memory/` | 跨会话结构化记忆(263 份,项目的组织大脑) |
| `tools/` | 展示页构建工具 + 数据管线 |

## 在线浏览

**[https://vinlic.github.io/terraria-replica-build-notes/](https://vinlic.github.io/terraria-replica-build-notes/)**

深度阅读(克隆仓库后):

- `session-archives/sessions/` — 全部对话记录
- `session-archives/memory/` — 跨会话结构化记忆
- `docs/methodology-legion.md` — 方法论
- `tools/` — 构建工具

## 数据规模

- **16 个日夜**(2026-08-05 → 2026-08-20)
- **31 路会话** · 峰值 20 路并行
- **205,781 条**人机往返消息
- **594 亿** tokens 消耗(净生成 7,840 万)
- **56 万行**代码(TypeScript / 测试 / 工具)
- **199 项**缺陷根因档案
- **4,895 条**逐日对话实录
- 全部可审计、可回放、可对账

## 展示页结构

| 章节 | 内容 |
|---|---|
| 序章 | 不可能的任务(四重不可能 → 十六日后逐格相同) |
| 实验读数 | 9 格数据总览(3×3 方阵) |
| 第一幕 · 以算代眼 | 五件数学武器 + 十次关键缺陷 + 渲染器五项诊断 + num4 关键突破 |
| 第二幕 · 五级台阶 | 证据链演进 + 差异全景图 + 引擎级差异 + 技术路线抉择 |
| 第三幕 · 原则、工具与自主 | 三原则 + 工具军备库 + 自主化曲线 + 最新战报 |
| 第四幕 · 分水岭 | 武器清单(纯白 Claude Code)+ 六项能力要求 |
| 第五幕 · SOP | 可复制的十步工作流(奠基→执行→深化→放手) |
| 终章 | 四条定律 |
| 附录 A-E | 逐日实录 / 会话档案 / 缺陷档案 / 路线决策 / 量化轨迹 |

## 脱敏声明

本仓库所有内容均已脱敏,包括但不限于:
- 用户名 / 主机名 / 本地路径 → `user` / `mac` / `~`
- 邮箱地址 → `user@***`
- API 密钥 / Token → `[REDACTED]`
- 带签名的 CDN URL → `?[REDACTED]`
- Cookie 值 → `[REDACTED]`
- 内网 IP 地址 → 掩码处理

## License

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) — 非商业性使用 · 相同方式共享

## 相关

- 方法论详解: `docs/methodology-legion.md`
- 版本差异: `docs/upgrade-1405-to-1456/README.md`
- 构建工具: `tools/build-journey.py`
