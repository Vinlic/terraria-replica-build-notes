---
name: player-jump-vanilla-alignment
description: 起跳/下落全链对齐原版:jumpSpeed 5.01(曾6.6猛32%)/jumpHeight 15平台段恒钉-5.01(曾-0.22累加抛物线头)/松键只+0.01无跳高截断(曾vy=2狠掐)/jumpBoost→20+6.51链/水中30+6.01+g0.2+fall5;实测跳高5.84格≈原版6格;tick序=JumpMovement钉→重力+0.4→位移(-4.61与原版同)
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-15T14:38:53.631Z
---

玩家起跳/下落对齐原版（2026-08-15，用户："起跳和下落感觉和原版有很大差异"——审计证实 6 处实质偏差全修）。

**原版模型**（Player.cs）：
- 常量：`jumpSpeed=5.01`/`jumpHeight=15`（:2378-2380 static）——**jumpHeight 是平台段 tick 数不是高度**
- 起跳：vy=-jumpSpeed；`jump>0 && vy≠0` 期间 **vy 每 tick 恒钉 -jumpSpeed**（:20391 JumpMovement 内重置，非累加）→ 恒速平台段 15t；tick 尽重力接管 → 抛物线尾
- **tick 序（Update 内自上而下）**：JumpMovement 钉(:26422) → 重力 +0.4(:27033) → 位移——平台段位移速度实为 **-4.61**（钉后带重力），与原版 1:1（勿当 bug 修）
- **无跳高截断**：松键 vy+=0.01（:22446 几乎不衰减）；releaseJump 是"再跳资格门"非空中减速——原版跳高基本固定 6 格（平台 69.15px+尾 29px≈98px）
- UpdateJumpHeight(:19301-19341)：jumpBoost（云朵气球族 16 件）→ h≥20/s≥6.51；狼人 +2/+0.2；jumpSpeedBoost（蛙腿 1.6/女皇胸针 1.8）加算
- 水(:24150-24155)：h=30/s=6.01/g=0.2/maxFall=5；蜂蜜 g0.1/fall3；微光湿 g0.15/h23/s5.51；shimmering ×0.9
- 多段跳(:20521-20560)：同 -jumpSpeed 起跳，jumpHeight 梯度=沙暴×3/暴雪·海啸×1.5/屁瓶·云×1.25/云朵×1

**我们六修**：
1. constants：6.6/9 → **5.01/15**
2. 长跳模型：vy-=0.22 累加 → **vy 恒钉 -mJumpSpd**（Player.ts:1841）
3. 松键截断 vy>2→2 → **vy+=0.01 原版语义**（:2166 附近）
4. jumpBoost 链接入（曾只 1.25 乘数近似）；jumpSpd（蛙腿 1.6）加算进 base；狼人 0.2 已在 jumpSpd
5. 水中：0.3g/-4.6~3.0 钳 → **0.2g(=GRAVITY×0.5)/-6.01~5.0**，水面起跳 -6.01/h30
6. 多段跳 mult 乘速度 → **hMult 乘平台段**（沙暴 3/暴雪 1.5/Fart·Cloud 1.25）；蹬墙跳/翅膀 JS 基准对齐参数链

**验证**：浏览器探针 vy0=-4.61 恒 15t 平台 ✓、峰 93.5px=5.84 格 ≈ 原版 98px/6.13 格（采样窗差 1 tick）；mounts/grapple/cobweb 123 tests 绿（jumpHeight×2=20t 断言仍过）。

**Review 二轮 4 修**（2026-08-15 同日终审）：
1. **vy==0→jump=0 守卫**（:20386）：撞顶/落地须终止平台段——曾缺守卫撞头后继续把 vy 钉向天花板；探针敞顶 93.5px 不变+撞顶 jumpHold 即刻 0 双验证。
2. **松键不清 jump 计数**：原版松键只停钉（重力立即生效）、中途再按**恢复剩余平台段**——曾 else-clear 清零。重构为 `jumpHold>0 → vy==0?清零:inputJump?钉+递减`。`jumpHold===0` 各消费门（翅膀 :26545/坐骑飞行 :26640）与原版 `jump==0` 判定随持久化语义自动对齐。
3. **Game.ts:17829 联机代理玩家**漏改：0.22 累加/-2 截断/水 0.3g 全套旧模型——同步为钉模型+0.2g/5.0。
4. **狼人 jumpHeight+2**（:19334 只并了速度 0.2）——补 baseJumpTicks+=2。

**备案未动**（审慎偏差，非 bug）：
- 全浸没游泳 -0.62 连续加速度 vs 原版跳跃循环模型（水中 h30/s6.01 反复起跳，无脚蹼需 vy==0 顶点+松键再跳=节奏游泳；脚蹼 flag2 任意时刻可再跳）——重构水块风险大，保留近似；
- 多段跳 vy>-2 门（原版 canJumpAgain 无速度门允许上升中二段跳）——防我们无 releaseJump 模型下按住跳瞬间烧完全部段位，净等价；
- merman 游泳不耗 jump tick（:20394）/便携马桶 jumpHeight+5（:19339）——两者均未实装。

**踩坑**：探针 touchKeys.add('Space')；夯实平地需清上方 12 行。并行会话 build-l10n `--cultures=zh-Hans,en-US` 局部重建会把 index.json 缩到 2 语言（l10n-data 12 语言断言红）——跑无参全量 `node scripts/build-l10n.mjs` 恢复。

**2026-08-19 半空免费二段跳修复（行为录制首批战果）**：用户报裸装半空可再跳免摔死——空井探针不复现（平地无坡），**行为录制（behaviorTail 键沿+60t 采样）抓到 t=1053 起跳→t=1078 半空再按跳 vy 转负**；坡面地形探针（V 形谷 slope1/2）复现 vy+2.31→-2.55。双根因：①slopeCollide 地面坡抬升分支无条件置 onGround（TileCollision :331）——修为仅 vy>=0 置（原版 velocity.Y==0 落地语义）；②**jumpHold-- 只在按住时递减**（:2549）——松键冻结平台预算，半空再按恢复整段钉速=免费二段跳；修为平台计时器无条件每 tick 流逝（原版 jump-- 在 controlJump 门外，松键不清计数 :22446 但窗口照常耗尽）。教训：**平地探针测不出坡面/地形相关 bug——合成探针必须覆盖坡面**；行为录制（键沿+采样轨迹）是用户侧现象→数据证据的最短链路。
