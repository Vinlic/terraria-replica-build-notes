---
name: pvp-system-port
description: PvP 全链移植完成——victim-settles 权威模型/协议 v7/StatusPvP 双表/探针抓三真 bug/备案偏差清单
metadata: 
  node_type: memory
  type: project
  originSessionId: cb3a4729-b2a0-4330-a696-da1975f3392a
  modified: 2026-08-13T10:34:12.426Z
---

PvP 系统移植完成（2026-08-13，P0-P5 全量 + 验证）。核心架构决策：**被打方本地结算**（victim-settles，与 msg16 客户端权威 HP 同构）——攻击端只广播意向，被击端过 InOpposingTeam 门禁后自行扣血，伪造包无法强制扣血，规避原版服务器门禁必要性。

**Why:** 原版是"攻击者结算+服务器校验"（MessageBuffer.cs:3864），我方没有仲裁服务器；选被打方结算更安全且与现有 HP 中继一致。

**How to apply:**
- 协议 v7（PROTO_VER=7）：msg13 flagBits[7]=hostile + 尾部 u8 team（**服务器 msg13 handler 重建帧必须透传尾部 team**——曾漏）；msg27 kind bit6=0x40=玩家 PvP 弹（bit7 仍是 NPC 敌弹）；msg44 StrikePlayer{targetSlot,dmg,kbx,kby,weaponId,flags(bit0=crit/bits1-4=meleeEnchant/bit5=圣骑士盾转移/bit6=狱火光环)}，S→C 尾部回填 fromSlot；RoomPolicy 尾部 u8 pvpAllowed
- **服务器脏值掩码坑**：msg27 kind 检查必须 `(kind&0x3f)>8`——0x7f 会把 bit6 PvP 弹整条吞掉（探针实抓）；room.ts clients 是 **Set**，不能 .find（实抓崩连接）
- 数值 1:1：PvP 实际扣血走**常规链**（难度防系数+endurance，CalculateDamagePlayersTakeInPVP 固定半防只用于 Hurt 返回值=吸血消费 :37953）；无敌帧 8t（:37769）；每弹 playerImmune 40t（傀儡单计数器近似）；近战 PvP 暴击恒 10%（:43410 不吃 meleeCrit）；PvP 死亡不掉钱/300t 无敌满血复活/跳过 Boss 延迟/numberOfDeathsPVP
- P5 完整：StatusPvP 弹型表（Projectile.cs:11092-11348）+ 近战物品表（:6251-6349）在 stats/Pvp.ts；新增 8 个玩家 debuff BuffType（Venom=85 起编——81-84 被并行会话占用！）：Confused 控制轮换含原版 Up←Right 怪癖（:24683-24690 字面）、Ichor def-15、BrokenArmor 终值减半
- 验证：tests/pvp.test.ts（22 例）+ scripts/_pvp-probe.mjs（14 断言协议层，不起浏览器，需先发 msg8 才收 RoomPolicy）+ **scripts/_pvp-e2e.mjs（21 断言双浏览器全链，ALL PASS）**：近战(挥击盒→msg44→被击端结算/8t无敌帧/msg16回报)/同队免疫/单hostile免疫/弹幕bit6傀儡命中/爆炸bit7/PvP死亡全套
- **第二轮 1:1 补齐（2026-08-13 goal 批）**：爆炸 PvP（BombsHurtPlayers :13944 跨端=bit7 意向,原版爆炸无 hostile 门、108/1002 pvp=false、服务器对 bit7 放行非 pvp 房）；近战后效（蝙蝠棒5097回1血/变态刀3106满潜行/甲虫窗口/派对彩纸）;kind1 PvP 弹视线门(CanHitWithMeleeWeapon 近似,canHitLine);damagePlayer 返回实扣值(圣骑士盾精确 25%/Hurt>0 语义);弹幕吸血(304 vampire/幽灵套 ghost,攻击端 InPVP 口径反馈)
- 探针实抓 5 真 bug：msg13 team 尾漏传/**0x7f 掩码吞 bit6（服务器墙+netMakeProj 两处,改 0x3f）**/Set.find 崩/**bit7 直调 p.damage 绕过死亡结算**（改走 damagePlayer）/HMR fork items.ts 多实例 id 错位（探针必须走 __swFlow 桥）
- **E2E 探针方法论**：headless 后台页 rAF 冻结→手动泵 fixedUpdate+postUpdate（_roomprobe 模式）;tiny 存档出生点悬空+底部击杀线(h-40 格)→先铺平台于 h-60;8t 无敌帧须 damage 包装捕获峰值;房主裸 join 可行(不需 newWorld)
- **备案偏差（更新）**：弹幕暴击不同步（近战 flags bit0 有,弹幕无通道——aux 被 MagicProj life 占/浸剂占低 4 位）;103/119/137/320 纯视觉 buff 未实装;3211 天蝎鞭/1123 蜂王剑 PvP 特效=与敌怪侧同缺（共享 PvE 缺口,非 PvP 偏差）;近战 PvP lifesteal（吸血鬼刀近战态）走攻击端反馈池与弹幕同构
- _roomprobe 3 个失败（msg5 手持/msg21 掉落/protectItems）全部卡在 `__swFlow.itemByKey` 返回 -1——并行会话数据层重构中，非 PvP 链（49 项协议断言全过）
