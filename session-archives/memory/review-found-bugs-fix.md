---
name: review-found-bugs-fix
description: 对抗性审查抓出11真bug全修:红帽ai3断链(普通骷髅王刷Chippy套装漏洞=ai3被旋冲挪用skeletronSpinDir独立)/史莱姆雨第三参未传+downedSK单读/光女弹幕9999五处+dash覆写序+真狂暴入夜离场/弹540孵化Bottom锚/兔子站定清walkCycleT相位/静持锚传真实useStyle/钓竿谓词补2421·2422/Critter.ts删除后测试迁移(player stub+onEnemyKilled)
metadata:
  type: project
---

审查修复批（2026-08-18，三路对抗审查抓出 11 真bug 全修，155/155 绿）。

**漏洞级**：①**红帽骷髅王 ai3 断链**——召唤只写 redHat 旗但 NpcDrops 五条规则/Renderer 红臂骨/GorePiece 全读 **ai3**；且 bossAI.ts 把 ai3 挪用为旋冲方向(±1)→**普通骷髅王约半数击杀必掉全套 Chippy 时装**（刷物品漏洞）。修：召唤补 `head.ai3=1` + 旋冲方向改独立字段 `skeletronSpinDir`（bossAI :50/:64/:93/:124 四处；Prime 127 的 ai3 用法独立无冲突勿动）。②史莱姆雨计数门两断线：Game 调用没传第三参 kingSlimeOnField + downedSK 单读 `downedSlimeKing`（击杀链写的是 `downed_50`）——双修。

**行为级**：③光女白天狂暴弹幕五处 shoot 漏置 9999（:46349-46356 flag4 num6-10 全 9999）+ dash 是 9999×1.5=14999（:47294-47299 **覆写在乘区后不乘**）+ 真狂暴(ai3∈{2,3})入夜应强制 13 态离场（:46580-46595）。④弹 540 孵化锚：NewNPC 是 **Bottom 锚**（:81547）→ fromVanilla 中心锚须传弹底再回退 h/2（测试同步改）。⑤兔子站定不清 walkCycleT → 起步相位漂移首帧非 0（原版 case46 vx==0 清 frameCounter :77571-77577；Enemy.ts 通用 tick 站定清零）。⑥迅猛龙静持锚传 useStyle:null → 丢原版 us2/9/5 档（:50684-50690 flag 族只读 heldItem.useStyle 与动画无关）；修：经 itemFuncOfVid(vid).useStyle 传真实值。⑦钓竿谓词漏 2421/2422 熔线钓钩（fishingPole 全集 9 件）。

**测试基建**：并行会话删除 src/entities/Critter.ts（小动物 Enemy 化）后 proj-critter-hit 未迁——修为 `Enemy.fromVanilla(299)` 松鼠 + GameHooks stub 补 `player`（Enemy.hurt 死亡 ctx 读 p.hp）与 `onEnemyKilled` 回调。

关联 [[boss-summon-drops-events-batch]] [[bunny-walk-frame-fix]] [[leftover-closeout-4batch]]。
