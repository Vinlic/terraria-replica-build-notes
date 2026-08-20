---
name: behavior-parity-batch-2026-08-17
description: 角色行为对齐总批:玩家动画帧(跳落5/6·行走7..19×13速率1.3/8·游泳·重力反转·钩爪·eocDash·useStyle8/11/12·睡床旋转)+死亡三件散飞/幽灵/PlayerEyeHelper眨眼+日曜盾球视觉+放块动画/水中跑尘(互斥带/WetCollision位移层)+城镇NPC逃离/坐姿帧/白天坐椅/三档跳+使用动作P0(吃药动画/药水病分档/autoReuse边沿);台账docs/behavior-parity-audit-2026-08-17.md
metadata: 
  node_type: memory
  type: project
  originSessionId: c44574b3-7d4d-403b-8e39-61a13d11a1c6
  modified: 2026-08-17T15:30:53.518Z
---

角色行为对齐总批（2026-08-17，用户 /goal："review 有没有其他角色行为未对齐，全量对齐"）。三路审计代理（玩家动画/使用动作/城镇NPC）+五路修复代理+主会话直修。**总台账 docs/behavior-parity-audit-2026-08-17.md**（含全部原版行号+遗留 C1'-C6 登记）。

**玩家动画帧批**（Renderer.drawPlayer 双路径）：跳/落行=5/6（原 1/4 是挥动动作行!）；行走=行7..19 共13行、速率|vx|·1.3/8（:35829-35847）；游泳三段(swimTime>20→0/>10→5/≤10→0)；gravDir=-1 整体 translate(0,-h)+scale(1,-1)+useStyle5 行2↔4；钩爪悬空行2/4/3；eocDash/沙暴跳/飞毯→6；useStyle 8割草机→0/11高尔夫三段4-3-2/12吉他→3；睡床旋转 π/2·(−dir) 绕盒心（床型偏移表登记）。**equipStats.wing 加 slot 字段**（翼22/28/45 行0 判定用）——equip-stats.test 断言同步。

**死亡表现+眨眼**（PaperDoll part 过滤/Player/Renderer）：三件散飞（初速 :38287-38293 X=Next(-20,21)·0.1+2·hitDir/翻滚 rot+=vx·0.1/immuneAlpha+2t 渐隐 2.1s/stoned 归零）；幽灵=difficulty==2 硬核 Ghost.png 4帧8t（**非中核**）；PlayerEyeHelper 优先级链（致盲>受击锁20t>床>中度伤【阈值0.25非0.75!】>醉>毒>风暴>正常240t）；眼睑 Player_0_15 三帧叠画。坑：接触死路径先直置 dead → init 门须独立标记非 !dead；?play=small 快速游玩无 appearance（探针须注入）。

**水中裸装跑尘**（用户报障"水地面走也出粒子"）：原版 Run 参数零水因子——减速全在位移层 WetCollision(:27858-27888 liqFactor 水0.5/蜜0.25/微光0.375,ignoreWater=游泳坐骑∪脚蹼药∪星旋翼26)。旧 maxRun×0.55 是自造模型→裸装水中带[1.65,3)非空误触发。修=摘速度因子+位移层选档（velocity 不动）。靴族水中照冒尘=原版行为（尘门无 wet 检查）。

**城镇NPC批**（TownNPC.ts）：危险逃离(:53884-54603, 被逼墙角冻结240t仍还击)+坐姿/攻击帧带(num58=frames−AttackFrameCount, 坐=num58−3)+白天随机坐椅(rand300 无昼夜门)+三档跳−6/−5/−4.4+净空堵转身。测试 103/103。

**使用动作批**（Game.ts）：吃药/进食动画+Item_2 咀嚼音+useTime17；药水病分档(226/227→45s/1912→40s/5→30s/3001随机/余60s)+贤者石×0.75 只缩药水病；弓枪法杖 autoReuse 边沿门(undefined=false 木弓单发)；钓竿8t；工具挥击音=Item_1+破坏音四档(KillTile_PlaySounds: 草=Grass/石矿砖=Tink/默认=Dig/蛛网=Item_27)；noUseGraphic 族表。

**探针方法论新增**：探针长跑用 g.tickCount 轮询驱动（墙钟时长在负载下 tick 不足=假阴性）；Game.playSfxFiles 包装必须 .bind(g)（this 依赖，未绑定首调用炸 rAF）；探针目标格勿与玩家列重叠（禁覆盖玩家静默失败）；vite 转换缓存会在并行会话改文件的瞬间重启时烧进半坏态（loadBitmapOnly 未定义冻结）——清 /tmp/sw-vite-5201 重启即愈。

**二轮"继续补齐"批**：帧层结构（body/legs 双通道 rows:{body,legs}——use/静持只钉身体腿独立循环；坐姿腿切片全 switch；床偏移 27 档；浮水/盾行10；人鱼三件+HIDES_HEAD{38,135,269,282,288} 脸清除【39 不在集,base 脸画在全脸甲下】；变身坐骑 PlayerIsHidden{52,54,55,56,61} 藏本体；SetMatch 全表）+NPC P1（雨回家/悬崖避让/传送矩形/游走常量/社交掷骰含 **RPS 对局表情36/37/38**/派对跳舞/**keepwalking 三路**【起步期贴 AvoidedByNPCs 25 sheet 集/挤站定友方/溺水→走程重置90t】）+提取器回填（useTurn 3504/noUseGraphic 381/UseSound 968 件）+canFloatInWater 真源修正（**仅 4404∪buff265,flipper 饰品不授予**）+入驻轮房况复核（:65088-65092 全员重跑,失效转无家+房回收）。

**三轮登记项收口批**：A 路（noUseGraphic 换 381 件数据表/QuickHeal·Mana·Buff=H·J·B 键【Mana=J 非 M 勘误】/食物饮料尘284/换档删旧/远程+1帧/望远镜=pan 非 zoom/女猎手四档省弹/棉花糖 968→969/**dryadWard 全链**【树妖=id20、授予链=施法态→弹586 渐扩光环→AddBuff(165,120)，防+8/thorns+0.5；海龟套 thorns 覆写 2 非叠加】/聊天单泡真值/幽灵 boss+600 乘加序）；B 路（**DrawPrettyStarSparkle 原语**【XNA AlphaBlend=预乘！A=0 纯加色=lighter+α摊平 255】/402 sparkle+ai2 600t【段在死亡早退前否则 ai2 冻结,570 尘暴+×6 冲刺+600 重开非自灭】/SwingArc 四型号/Empress 彩虹残影环/幽灵三拖影 shadow 0.5/0.7/0.9/游泳腿相位=miscCounter 差分【原版 counter 不随 swimTime 重置】/变身坐骑手持锚+狼表/legs140=神灯之咒 3770）。

关联 [[multijump-fx-port]]（跑尘结构门）[[use-path-final-audit]]（放块三件套）[[default-run-speed-parity]]。
