---
name: session-archives-export
description: "全量会话档案导出位置与再生成方法——session-archives/ 415MB,737 个 md,含 545 份子代理实录"
metadata: 
  node_type: memory
  type: project
  originSessionId: e65c4575-731a-43e0-a377-ccf50cc42db3
  modified: 2026-08-15T14:12:26.383Z
---

2026-08-15 完成全部 Claude Code 开发记录的全量导出(用户要求"完整对话+实施记录"):

- **位置**:`~/Project/GLM/SandboxWorld/session-archives/`(415 MB)
- **结构**:`sessions/<序号>_<日期>_<sid8>_<主题>/conversation.partN.md`(主会话,>25MB 分卷)+ `subagents/agent-*.md`(子代理实录)+ `images/`(124 张解码截图)+ `memory/`(162 份记忆快照)+ `index.json` + `README.md`(总索引表)
- **完整性**:消息逐字全收(thinking/工具调用完整 JSON/工具返回全文/附件注入);纯簿记行不计正文只计数量;21 个静止会话消息数与源逐条一致,活会话差额=快照后新增
- **再生成**:`python3 tools/export-session-archives.py`(约 90 秒,幂等;导出器随仓库保存)
- 源:`~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/`(1.3 GB,24 主会话 jsonl + 各会话 subagents/ + memory/)

**Why:** 用户需要把人机协作的完整过程留档;这些实录也是研究"多会话协作工程"的一手材料(编年史 docs/sandboxworld-chronicle.html 的数据源)。
**How to apply:** 用户要查"当时怎么做的/某次会话改了什么"时优先 grep session-archives/;重大节点后可重跑导出脚本刷新快照。
相关:[[sandboxworld-project-setup]]
