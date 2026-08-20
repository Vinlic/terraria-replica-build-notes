---
name: mining-model-port
description: 挖掘/砍伐伤害 1:1 移植——铜斧砍树 13 击（原版），伤害公式/冷却基准/tileNoFail/门槛表
metadata:
  type: project
---

2026-08-11 挖掘模型对齐原版（用户报"铜斧砍树 3 击不对"——确认我们错了，原版 13 击）：

- **伤害公式**（Player.cs:45032-45120 ActuallyUseMiningTool + :52981 GetPickaxeDamage，阈值 100/击）：
  - **tileNoFail**（Main.cs:7138-10198 表，花草/藤蔓/蘑菇/雪泥等 77 项）→ 100 直接秒挖
  - **斧族 tile**（tileAxe 表：树 5/72/80/323/488/583-589/596/616/634/704）：`int(斧力×1.2)`（仙人掌 80 ×3 再 ×1.2）；**镐不能砍树**（原版 pick 分支被 tileAxe 排除）
  - **镐族**：`pickPower`（除数表：钴钯/2、秘银山铜/3、精金钛/4、绿藻/5、蜥蜴砖/4、黑檀猩红狱岩地牢砖/2、云×2）+ **门槛归零**（绿藻200/黑檀猩红65(地下55)/陨石50/魔金猩红矿地下55/黑曜石55/狱岩65/蜥蜴砖210/地牢砖100）
  - 旧实现"斧力×5.5 hack + 泥土族×2"整体废除
- **冷却 = useTime**（原版 toolTime=ApplyItemTime(useTime)），非 useAnimation——items.ts 工具全表补 useTime 字段（铜镐15/铜斧21/铁镐13/铁斧19/银11/18/金17/18/锤23-25）
- **击数锚**（tests/mining.test.ts）：铜斧树13/铁斧10/金斧8；铜镐土·石·矿3/金镐2；花草1（tileNoFail）；银矿(门槛20)银镐3
- **黑曜石 56 无除数**（全伤）——曾误加入 /2 族，测试纠正：55力→2击
- gate 的双重位置：外层 toolCanBreak（tiles.ts d.pick 门槛）+ 伤害归零（除数表内联 gate）——同值不冲突

**Why:** 挖掘节奏是手感核心；×5.5 hack 让早期砍树快 4 倍，完全偏离原版。
**How to apply:** 改击数/手感先查 Player.cs:45032-45120（真挖掘分支）而非 PickTile（那是召唤/钻头车的）；新工具一律提取 useTime+useAnimation 两个字段。关联 [[vanilla-1456-upgrade-notes]]。

## 挥击手速对表（2026-08-11，用户报"挥砍速度蛮快"）

原版双计数分立（Player.ItemCheck）：**itemAnimationMax=useAnimation（挥击弧时长）、
itemTime=useTime（复用冷却）**——vanilla-itemcombat.json 2481 件有双字段、**1790 件两者不同**
（铁阔剑 13/20、村长短剑 10/15）。我们此前把 useTime 当动画时长 → 挥速虚快 35%+。
修复（Game.ts 挥剑分支 + vanillaItemCombat.ts melee 变体）：
- swing.dur = useAnimation/attackSpeedMult；player.useTime = useTime/attackSpeedMult
- **autoReuse 语义**：true 持按链式（useTime<useAnimation 时动画未走完即重置弧线=原版截弧）；
  false 需重新点击（prevSwingMouse 点击沿，原版非自动武器不可按住连挥）
- 原 `Math.max(12, ...)` 下限是掩盖虚快的补丁，vi 武器改 max(4)/max(2)（原生 legacy 保留 12）
遗留：镐斧锤单 speed 数（挖掘已按 useTime 验证，动画用同值）；通用物品 30 固定。
相关挥击渲染/判定锚点修复见 [[wall-creeper-ai40-port]]（同日：origin 底角钉握点 + 32×32 恒定基底 + 早/晚段扩展对调）。
