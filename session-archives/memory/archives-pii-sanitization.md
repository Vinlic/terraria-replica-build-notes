---
name: archives-pii-sanitization
description: "session-archives 与展示页的敏感信息审计结论与脱敏规则库(已全零,规则已烧进三个工具脚本)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e65c4575-731a-43e0-a377-ccf50cc42db3
  modified: 2026-08-15T17:19:29.392Z
---

2026-08-16 用户要求全面敏感信息审计("密码/key 啥的,不止在 html")。扫描面:两份展示页 + journey-inputs + session-archives 全部 1,860 个文件,16+ 类指纹。

**审计结论**:无任何 API key/token/私钥/数据库连接串/discord webhook/真正的密码(sudo 密码从未被回显;"password 类命中"实为环境变量 PWD 与 `password=-1` 配置)。真实 PII 与已处置项:
1. **个人邮箱 63 处**(user@v***)→ user@***
2. **CDN 带签名 URL 18 处**(截图上传回链,含 UCloudPublicKey+Signature)→ ?[签名参数已移除]
3. **Cloudflare set-cookie 值**(抓 wiki.gg 带回的 __cf_bm/_cfuvid,非凭据)→ set-cookie: [已移除]
4. **内网 IP** → 192.168.x.x 掩码
5. **用户名/主机名海量变体**:user/user/mac/**user/user/userlic/vli/vlic**(模型当年打错的各种拼法!)→ user/mac/玩家;最终用**通配规则**根治:`/Users/<任意用户名>/(Project|Downloads|Library|Desktop|Documents|…)` → `~/<目录>`

**Why:** 档案要外发共享;用户名打错变体靠枚举永远清不完,通配主目录模式一次覆盖全部拼写。
**How to apply:** 三个脚本已内置规则,重生成即自动脱敏——`export-session-archives.py`(Writer.w 出口)、`extract-early-events.py`(截断前清洗)、`build-journey.py`(esc() 兜底)。外发前复扫一次(指纹清单见本会话 08-16);新增共享面(如 docs 其他文件)也要过同套规则。
相关:[[session-archives-export]] [[journey-page]]
