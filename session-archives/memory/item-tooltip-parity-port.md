---
name: item-tooltip-parity-port
description: "悬停气泡1:1(GetLinesInfo :20488-20920):vi_武器伤害/暴击/速度档/击退档/渔力/镐斧锤力×5/耗魔/可放置·弹药·消耗品/材料/容器/Buff持续全量;数据坑:item.ammo在combat json非func;斧显示×5;官方中文坑:Container译'收集附近掉落物'"
metadata: 
  node_type: memory
  type: user
  originSessionId: ec878731-1c65-4b4c-9a3b-c8009ce5461a
  modified: 2026-08-18T07:08:55.243Z
---

# 物品悬停气泡 1:1（2026-08-18 用户"相比原版缺了不少信息，武器还有攻击力"触发）

**原版行链**（`MouseText_DrawItemTooltip_GetLinesInfo`，Main.cs:20488-20920，
行序严格）：名(稀有度色/×N) → 伤害[+类型后缀 LegacyTooltip 2/3/4/53/55] →
暴击%（近/远/魔三系，4 基础+装备/buff+词条） → 速度档（useAnimation 分档
≤8/20/25/30/35/45/55/∞ → tip6-13） → 击退档（0/≤1.5/3/4/6/7/9/11/∞ →
tip14-22） → 渔力+需鱼饵/鱼饵力 → 可装备 → 时装 → 防御 → 镐力/斧力(×5!)/
锤力 → 恢复生命/魔力 → 耗魔(×manaCost) → 可放置/弹药/消耗品(else-if!) →
材料 → 容器/线触发 → 自带说明(ItemTooltip.*) → Buff 持续 → 词缀差分(绿/红)。

**Why（旧实现缺口）**：只有名/词缀/legacy 工具行/防御/恢复/静态说明——
vi_ 武器**伤害行整缺**（damage 在 combat json 不在 def.tool）、暴击/速度/
击退/渔力/镐斧锤/耗魔/可放置/弹药/材料/持续全无。

**样式批（同日 review）**：底=Inventory_Back13 九宫 × (23,25,81)×0.925
（:20252-20255；与面板同贴图不同染色，tooltipBgDataUrl 按 (w,h) 烘焙缓存 +
素材未就绪 onload 一次性补刷）；文字=MouseText 字体栈+1px 字影
（DrawColorCodedStringWithShadow :20256）；名称行**不加粗**（vanilla 同字号
渲染）、堆叠格式 " (N)"（GetHoverName :420-427 非 "×N"）；定位槽右锚+视口
18px 钳制（:20241-20250）。探针 _tpstyle 四断言（九宫/阴影/字体/堆叠）。

**How to apply（src/ui/itemTooltip.ts 纯函数 + UI 消费）**：
- 数据面坑：**item.ammo（是弹药旗）在 combat json**（func json 箭族缺）；
  **斧力显示 = axe×5**（铜斧 axe=7 → 35%）；材料旗无数据 → VANILLA_RECIPES
  原料反查近似；可装备 = itemstats acc/hs/bs/ls + equipKind hook/mount/pet/
  light/cart。
- 伤害行乘区 = combat.damage × 词缀 dmg × player.damageMult(kind)；
  暴击 = 4 + player.critChance(kind)（equipStats 不含武器→与原版"playerClassCrit
  −选中武器+悬停武器"同式）+ 词条 crt×2；耗魔 × manaCostMul。
- l10n：LegacyTooltip.0-61 / CommonItemTooltip.* / GameUI.* 全在 zh 包；
  ★官方中文坑：`CommonItemTooltip.Container` 译作"接收到信号时会收集附近的
  掉落物品"（不是"容器"）——断言勿按直觉词。
- 测试 tests/item-tooltip.test.ts 10 条（tag 断言，l10n 未载回退键名）；
  探针 scripts/_tooltipprobe.mjs 10/10（真实 UI.showTooltipFor + spawnDrop
  注入法）。ITEM_DEFS 的 id=数组索引；vid 反查用 def.vid ?? 正则。
- **低频二批全接入（2026-08-18 用户令"低频也必须完整"）**：
  ①亮度脉冲=mouseTextColor 190↔255 ±1/tick（:18064-18075）→ startTooltipPulse
  rAF brightness 驱动，mouseleave cancel；②yoyo 商标位（:20845-20853 悠悠球
  11 件 3262/3282-3286/3315-3317/3291/3389）→ OneDropLogo.png 五层 drop-shadow；
  ③鞭速度档例外（:20545 `!summon || IsAWhip[shoot]`——WHIP_PROJS=aiStyle165
  全 18 枚）；④tileWand 消耗行（tip52）：表 {832→木材9,933→9,932→骨154,
  1129→蜂巢1124,3360/3361→红木620}——★Dirt Rod 114 无 tileWand（发射移土弹），
  勿想当然登表；⑤研究行（:21163-21178 旅程 difficulty==3 →
  Research.tryGetSacrificeNumbers → CreativeSacrificeNeeded 紫 JourneyMode）；
  ⑥商店价格行（:20309-20402 Game.npcShopOpen 门 → 买入 value×5；
  币名=LegacyInterface.15-18 非击退档！四档色 铂220/金224/银181/铜246）；
  ⑦专家/大师行（rare -12/-13 → GameUI.Expert/Master）。
- 鞭数据坑：combat json 鞭族是**残缺条目**（{noUseGraphic} 非 null 但无 damage）
  → `c ?? 兜底`够不着，whipsJson 存在时**无条件覆写**（spread+override）。
- 遗留极小项（视觉细节）：社交栏 tip0/61、任务品 inter65、特殊种子行
  （CursedByPlantera/DD2 未通关/misc104）——这些在原版悬停几乎不可见分支。

**review 批修（2026-08-18 三审）**：
- ★商店价语义：货架条目=买入价（expectedPrices 全链：快乐度×/折扣0.8×/
  银行家舍入，Game.shopEntryPriceOf 新增反查）；**非货架自带物在商店内=卖出价
  value÷5 min1 ×stack**（:20312 isAShopItem 分流 + :20324-20326 ÷5）——曾
  一律 value×5 买入。价格行 UI 注入 stack。
- ★暴击=武器自身 crit（combat json 缺省 4，火枪 95=6）+装备+词条×2——
  曾恒 4（高暴武器显示偏低）。原版 num2=classCrit−选中crit+悬停crit 化简。
- ★击退档含玩家加成：melee+kbGlove(力量手套)×2、kbBuff(泰坦108)×1.5
  （:20195-20210，UI 读 equipStats.kbGlove/BuffType.Titan）。
- ★伤害行×ToolTipDamageMultiplier（ItemID.cs:246 回响族 10 件 ×2 显示）。
- ★prefix 差分行序改原版链：伤害39→速度40→暴击41→魔力42→大小43→弹速44→
  击退45（曾击退排第 3）。vanillaPrefixes.prefixLines 全局改（UI 槽位行同序受益）。
- ★expert/master 行序归位：原版在 prefix 差分**之后**（:21140s），曾错排在
  统计行里 → expertMasterLines 尾部字段。

**终清零批（2026-08-18 四审）**：
- ★tileBoost 范围行（tip54 :20703-20715）：表 {509/510/511 扳手=20,
  851 多彩=20, 852 工具腰带=1, 2340/2341 矿车轨=5/2, 1305 The Axe=1}——
  itemfunc 无 tileBoost 字段（玩法侧 useWireTool 硬编码 20 已同值）。
- ★任务鱼行（inter65 :20663-20666）：ctx.anglerQuestItemId=Game.
  anglerQuestItemId()（当日任务鱼，种子^天数确定性掷）注入。
- ★套装奖励行（tip48 :21138-21143）：悬停护甲 + equipStats.setBonus.name
  → l10n ArmorSetBonus.*（67 键在 zh 包）；行序在词缀差分后。
- ★社交槽双行（tip0+tip1 :20508-20513）：where=dye/miscDye → UI 传
  socialSlot。★接口坑：并行编辑致 socialSlot 双声明 tsc 重复错——接口字段
  只留一处。
- 剩余永不达项（已核）：questItem 数据旗（本仓 angler 链走 id 表非物品旗）、
  DD2 misc104（3818+ 门 gate 未消费）、CursedByPlantera、特殊种子行——
  均为原版死码/特殊种子域。

**用户报障批（2026-08-18 气泡透明感 + 数字键失效）**：
- ★透明感根因 = 脉冲 brightness 打在**整元素**上（面板一起呼吸变暗）——原版
  :20256 逐行 `lineColors[k] *= mouseTextColor/255` 只乘【文字色】，DrawInvBG
  面板色恒定。修 = 行内容包 .sw-tooltip-lines 容器，脉冲 filter 打文字层；
  startTooltipPulse 先清整元素历史 filter。
- ★数字键"失效"= refreshAllNow 里 achAdvisor.update() 抛错把 rAF 回调整体
  炸掉 → refreshHotbar 永不执行（selected 实际已变而画面不动）。修 =
  refreshHotbar 提到最前 + advisor try/catch 自摘。★教训：rAF/事件回调里
  QoL 件异常会静默吞掉后续关键刷新——关键刷新前置。
- 探针 _ttfix.mjs 9 绿（面板 filter 空/文字层脉冲在动/Digit3→2/7→6/0→9/
  1→0/refreshAllNow 无抛）。TS cast 勿写进 .mjs 探针（as any 炸 node 解析）。

**不透明度真根因终案（2026-08-18 三轮报障）**：透明感的元凶是 tint 循环
alpha 通道误乘**红通道** `d.data[i]*tmul[3]`（应为 `d.data[i+3]*tmul[3]`）——
深蓝底红通道≈23 → alpha≈22 = 近全透明。三轮演变：①初报"几乎透明"（alpha 22
+ 亮度脉冲打整元素叠加）②修脉冲后"依然过透明"（仍 alpha 22）③铺不透明底后
"过于不透明"（alpha 255）→ 回退实底时暴露 typo。修复后回到**原版真值 0.925**
（alpha 236）——此前 0.925 从未真正渲染过。★教训：像素循环改 alpha 前先探针
采样输出（_ttopaq：dataURL 页内重绘 getImageData 采样，比截图可靠）；
三轮报障的"折中值"思维错了——该找根因而不是 0.925↔1.0 之间找点。

**用户禁令（2026-08-18）**：禁止以"低频"为由不接——所有原版行为必须移植
完整，低频项也计入台账与记忆。

关联 [[cursor-item-icon-port]]（指针图标）/ [[behavior-parity-batch-2026-08-17]]。
