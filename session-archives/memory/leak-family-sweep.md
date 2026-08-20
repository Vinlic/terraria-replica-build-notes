---
name: leak-family-sweep
description: 全仓泄露家族大扫除:双代理341文件+自查,修13处(合成滚轮风暴/append-only DOM/closeAll缺口/PaperDoll无闸tint×2/强引用钉死/销毁断线×3/叠面板/滑杆IO风暴/Game残留引用);34有界缓存登记表
metadata:
  type: project
  originSessionId: 5743a3fd-9c70-4e00-93d4-6bf8bcfdffbc
  modified: 2026-08-13T15:41:03.289Z
---

2026-08-13 用户问"整体还有哪些类似的泄露问题"(承接图鉴滚轮崩溃)。双代理
(面板生命周期 16 文件 / 渲染缓存 341 文件)+ 自查,家族签名五类:无上限缓存/
自取不回写/监听器定时器不清理/事件风暴全量重建/强引用钉死。

**修复 13 处(高危 4 + 中危 8 + 低 1)**:
1. [高]UI.ts 合成列表 wheel 每事件直调 refreshAll 全量重建(60 配方行+48 槽
   +全成就扫描)=BestiaryPanel 同根因 → **refreshAll rAF 合并**(包装 refreshAllNow,
   31 调用点零改动透传)
2. [高]refreshVanillaCrafting append-only(搜索每键 +61 节点无上界)→ 先清后填
3. [高]closeAll 清理缺口 → 补:clothesPanel.close(CharCreation.close 放宽 public
   可选参)+closeNpcDialog+closeAchievementsPanel+closeResearchPanel+achWrapEl=null
   (此前孤儿 CharCreation rAF 永转/退菜单后成就弹窗永久不可见/研究面板
   uiBlocking 滞留 true)
4. [高]PaperDoll.tintCache 无上限(整图 canvas×用户可控色键,同文件 cache 有
   LRU 而它漏配)→ 256 满清空
5. stealthTintCache 外层强引用 Map 钉死已被 cache LRU 淘汰的源 canvas → **WeakMap**
6. CritterCage.slotStore resetCageAnim() 全仓零调用(键含世界格坐标跨世界残留)
   → Game.destroy 接线(静态 import 无环)
7. UISpriteBatch.tintCache(VUI 单例常驻)无闸 → 1024 满清空(对齐渲染层惯例)
8. _craftWheelBound 类字段置真永不复位+craftListEl 每次进游戏重建=第二次进游戏
   合成滚轮永久失效 → 元素级标记 __swCraftWheel
9. mainFlow openSettings/openBestiary 无已开守卫叠面板(每层 +1 window Esc+Lang
   订阅)→ querySelector 守卫(sw-set-panel/sw-bst)
10. Settings 滑杆 input 每像素 options.set→JSON.stringify 全量+IDB 写=IO 风暴 →
    Options.set 持久化 400ms 防抖(内存+emit 即时,仅落盘合并;★副作用:await
    options.set('lang')不再等落盘,可接受)
11. Game 残留引用:quitToMenu 不清 __swGame(旧 Game 整图世界 store 数十 MB 被
    window 钉到下次进游戏)+ui.game 同理 → __swGame=null+UI.detachGame(closeAll
    调;closeAll 三调用点全菜单期,游戏内面板切换不走 closeAll,安全)
12. DebugSummonPanel 挂 document.body,Game.destroy/quitToMenu 够不着,反复进
    游戏累积 → destroy 关闭+置 null(dev-only)
13. [低]BestiaryPanel 缺表 404 每次 refresh 重新 fetch → bstSheetFailed 负缓存

**登记不动**:DebugSummonPanel 搜索去抖(dev-only)/main.ts 250ms 轮询钉旧 Game
≤250ms(常驻设计)/VUI.init 无幂等闸(单调用现状安全)/trapCooldown 死代码
(并行域)/CharCreation thumbTimer 单发空转(有 isConnected 守卫)。

**34 个有界缓存登记表**(全部带 LRU/清空调/清理调用):ChunkCache LRU384/
tintCache×4(1024/512/64/96)/flameDye 32/towerShield LRU16/HitTile LRU500/
PaperDoll cache LRU64/Arrow frameCache 2048/LanguageManager LRU/最佳面板 160/
Waterfall MAX_FALLS 1000 等——详见审计原文;一次性填充表与 SpriteAtlas/Sfx/
Audio 设计内全量缓存=N/A;渲染层 22 处 createElement 逐一核对无每帧新建。

**方法论**:①refreshAll/refresh 类全局重建函数优先 rAF 合并包装(调用点零改动)
而非逐事件源加节流;②强引用 Map 的键若源自另一张有 LRU 的缓存表→必 WeakMap
否则 LRU 形同虚设;③closeAll 类"清屏"函数必须同时关闭逻辑面板(监听器/状态
不在 DOM 里);④持久化与内存值分离(set 防抖)是 IO 风暴的通解。

相关:[[bestiary-scroll-crash-fix]] [[perf-anomaly-fix-batch]] [[asset-lazy-loading]]
