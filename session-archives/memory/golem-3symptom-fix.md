---
name: golem-3symptom-fix
description: 石巨人三症状:负血不死=hurt放行与AI首行契约断裂(放行在dead=true前!)/boss bar头像表漏245/帧=FindFrame状态帧非循环(customFrameIdx直读)
metadata: 
  node_type: memory
  type: project
  originSessionId: 1fc2b821-952a-4ed1-9b75-6e99198205af
  modified: 2026-08-19T05:21:50.578Z
---

2026-08-19 用户报三症状(debug report 锡桌子):①动画贴图乱闪 ②负血条不死
③boss bar 无头像。

**②负血不死(最重,契约断裂)**:Enemy.hurt 的石巨人放行段
`if (245||246||247||248) return false` 在 `this.dead = true` **之前**——"转换在
AI 首行接管"的注释假设 hurt 已置 dead,实际啥也没做:本体/拳血尽后 AI 每帧重入
(hp≤0)却无人置 dead = 永不死、boss bar 负值。★铁律:**hurt 放行型特判的放行
必须挂在 dead=true 之前且只有"确有 AI 首行接管"的 id 才放行**——石巨人仅 246
(头转自由态)真有;245 本体/247/248 拳走标准死。修:放行列表收窄到 246;
245 在 hurt 内灭部件(246-249,并行会话 boss#19"部件随本体消亡"定案的
执行点从 golemAI 首行挪到 hurt——dead 实体 AI 分发已跳过,首行版永不达)。
golemAI 首行血尽段注释化;dying 演出段标注不可达保留(无置位点)。
并行会话同日写 boss#19 审计时引入此断裂——**跨会话契约改动必须核对方调用侧**。

**③boss bar 头像**:BOSS_HEAD_INDEX 只给了 246/249→5,漏本体 245(boss bar
反查的是本体实体)→补 `245: 5`(Golem 头像=Head_Boss_5,与头共用)。

**①帧乱闪**:石巨人族全是 FindFrame(NPC.cs:73581-73651)**状态帧非循环**:
- 245 本体 7 帧只用 0-4:待机按 ai1 蹲伏倒计档(-20..0 五档);跳跃 ai0==1 →
  原版 `frame.Y = 1`(1 像素笔误值≈帧0,照抄取0)
- 246 挂载头:基础=l0(张嘴)1:0;眼部阶段(ai0==1,血<半)按激光侧 l1:
  -1→+4 帧 / +1→+2 帧 / 0(正上/下)→基础帧
- 249 自由头:帧=l0(frameCounter16 循环无消费)
- 247/248 拳 1 帧无动画
修:AI 侧写 `e.customFrameIdx`(先例=水书怪694),Renderer vanillaFrameIdx
直读零改。曾走通用 animT 循环=7 帧/6 帧乱闪。

测试 tests/golem-fix.test.ts 6 条(拳标准死/本体死+部件**下一拍自灭**/246 放行
(本体活门)+零死音/存量负血自愈/帧档/头像索引)。
★二轮 review 修正(用户质询"登记不修"后推翻自己):①"246 不能 die()"不成立——
原版头血尽转自由只发生在本体活(一阶段本体无敌必先打头);本体死后原版=StrikeNPCNoInteraction 标准死。修=**hurt 246 放行加本体活门**(本体死→落回标准死)。②"视觉噪音小"是搪塞——部件终战消亡全面改原版时序:**hurt 只杀本体,部件由各 AI 锚主检测后下一 tick die() 自杀**(碎块/音效管线,原版同构);
头 AI 本体缺失分支"转自由态继续战"(并行会话写)按原版改为 die(),与其
boss#19 定案"部件随本体消亡"本就矛盾。
★顺带发现:原版 246 SetDefaults **DeathSound = null(显式无声)**——json 补
`"DeathSound": null`,DeathSound 类型放宽 string|null,fromVanilla 两处
(初始/tryTransform)显式 null → killedSound=[](无声),hurt 死亡段撤
'killed' 合成 fallback(空=显式无声语义;无其他可达场景)。
★教训:登记"不可修"前先挑战自己的理由——"X 不能用 Y"常常只是"Y 的无条件
用法不行",加门(如本体活条件)即破。

**★终审清零批(2026-08-19 双子代理全维审计:音效/AI 行为/弹幕/渲染)——13 修**:
- 数据:四条 lifeMax 是 1405 旧值(json 9000/16000/7000/11000→1456 的
  15000/25000/10000/16000);恒 SCALE=0.5 错(:17942-17962 是 getGoodAdjustments
  **FTW 专属**段!普通世界 scale=1——曾误读为 SetDefaults 尾,普通世界头/拳
  锚点全缩半=嵌错位)→改运行时 sc(e)=vanillaScale??1
- **P0 BGM 裁决链键号体系错位**(Music.ts SLOT_MUSIC_CHAIN 键写成 flag 号而
  Game 存 num3 号)→17/24 族错曲:石巨人放 Boss3、EoW/骷髅王查无键落群系曲、
  月总放世花曲;BOSS_MUSIC/bossMusicFor 是死表(测试断言死表所以一直绿)。
  修=链键逐条换 num3(非线性三处:鹿角怪 flag2→16/EoW 25→23/骷髅王 26→24)+
  测试改断言活链 resolveEventMusic
- P0 一阶段本体无敌被单发弹穿透:iframes=2→**dontTakeDamage**(hurt 的
  iframes 门有 pierce!==1 豁免,原版 :19509 是挡全通道的 dontTakeDamage)
- P0 软锁:先破头(转自由)再杀本体→无敌自由头+双拳永不退场。修=头 AI 本体
  亡分支去掉 !x.free 豁免(:31521-31525 自由头同样查 golemBoss)+拳锚删 head
  回退(原版 golemBoss 单锚,找不到即自灭)
- P1:弹 258/259 出生音 Item_20/Item_33(弹幕自身首 tick 播,发射点等效);
  夹玩家门重叠→**包含**(:19666);自由头渲染换画 NPC_249(246 变身后曾一直
  画 246 贴图);拳链 drawImage ×scale(曾原尺寸环叠压)
- P2:玩家死→本体穿墙(曾漏 player.dead);258 OnFire 50%/300-420t(活表
  vanilla-projstatus.json 整条缺,死表 vanillaProjStatusPlayer.ts 固定 300t/
  100%);变身 spin 清零;删 246→249 转换吼(对账行号 :32587 系幻影龙 266 段
  误引,原版无声)
- P3:自由头穿墙开关(flag48 noLos 穿墙/有视线嵌块走碰撞);258 恒旋 +0.3/t
  备案不修(近圆火球视觉影响极小);245 镜像备案(原版永不翻,美术近对称)
- ★方法论:死表+活链并存时测试必须断言**活链**(死表正确≠运行正确);
  引用反编译行号要核宿主函数(§ :17943 曾被误读为 SetDefaults、:32587 误引
  两次事故);审计任务卡交叉两代理(音效只查 NPC 侧漏了弹幕自身音——行为
  代理补上 Item_33)

相关:[[npc-frame-golden-gate]](静态帧数闸门管不到运行时帧选择——
此案=数据全对但选帧错,闸门盲区)
