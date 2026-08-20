# 最新迭代挖掘(08-18 ~ 08-19)

数据源:memory/ mtime≥08-18 的 65 份记忆文件 + tools/journey-inputs/archive-stream.json 的 08-18(418 条)/08-19(96 条)实录。

## 一、新增亮点故事(非缺陷,是成就/工程突破)

- **WebGL2 一期:背景层+全屏地图 GPU 化**(08-18): 从 Canvas 2D 升级到 WebGL2——共享模块 GLSpriteLayer(quad/纹理 LRU/双 sampler)接管群系背景与全屏地图四段(卷轴/地图/迷雾),小地图纹理按脏区增量上传。同会话 A/B 像素级对拍:地图 Δ=0 完美零差、背景平均 Δ0.02;配套 `?bggl=0`/`?mapgl=0` 逃生门和 7 项源码级回归守卫测试。次日云层也 GL 化(CloudGL 并入共享层,24+8 张染色画布归零) | 证据:memory/webgl2-phase1-port.md
- **SimHost 服务器权威房全链落地**(08-18): "开在服务器上的房,世界由服务器计算"从 MVP 到 B6——进程内"虚拟房主客户端"经与房主完全相同的中继管线驱动世界(刷怪链/入侵链/TownNPC 转化全镜像),ioWorker 把存档解析与序列化搬进 worker,SIGTERM 优雅回退;真实浏览器 E2E 15/15 全绿(建房→访客→召唤意图→服务器结算→Boss 移除全闭环)。当日再加聊天系统+世界频道(此前客户端根本没有聊天输入框!),E2E 升到 20/20 | 证据:memory/server-room-simhost-port.md
- **千人单房实测:8vCPU 就能扛 1000 人**(08-18): 差分剖析发现 120 bot 时模拟占 CPU 82%,三刀优化(玩家 1024px 网格灭平方项/trySpawn 4tick 一掷×4/AOI 密度降频)后 120 分散 CPU 82→28.6%,60 聚集人均带宽 10.8→3.27KB/s(-70%)。千人外推=多房分线 8vCPU/16GB/100Mbps,国内带宽常态热点型千人约 8000-9000 元/月——性能账第一次算到了商业部署粒度 | 证据:memory/server-room-simhost-port.md 千人实测节
- **Remaster Studio 素材重制管线**(08-19): 一条"AI 重制贴图→打包→热替换"的完整管线落地:AssetCatalog 六类切帧聚合,gpt-image-2 逐帧重制(不支持透明背景就生成大图再盒式缩回+原帧 alpha 蒙版),手写 ZIP_STORED+CRC32 零依赖打包,类 mod 的 zip 素材包运行期局部覆盖原版贴图(vanilla-ui/弹幕/Buff 图标全注入矩阵)。六里程碑全绿:catalog 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7 | 证据:memory/remaster-studio-pipeline.md
- **液体 buffer-reflow 对齐:475 条湖面薄膜的集体归位**(08-19): 中世界 #49 检查点 11,707 格液体差,连通域聚类发现是"475 条单行湖面薄膜圆整漂移"的全局调度指纹——真凶是 LiquidBuffer 回灌双重错位(回灌量取了当前活动数而非空余量+DelBuffer 是 swap-remove 尾补头而非 FIFO)。小世界永不触 24999 帽,所以三条小链长绿的假象骗了所有人;大世界才是天然压力测试。修复后 #49 归零,#53 半砖债整段连带消失 | 证据:memory/liquid-buffer-reflow-parity.md
- **AI 全量 1:1 审计:六代理扫 200 条,181/181 测试全绿**(08-19): 六分区代理(死亡退化/追击门/地面/小动物/飞行水生/Boss)扫出 ~200 条偏离,五代理并行全量落地。最重要的方法论发现:原版 NPC 位移积分在 AI 外共享段(:93808)——AI 分支被跳过≠冻结,而是按冻结速度继续滑行,"死亡=只积分不 steering"。顺手揪出石巨人胜利条件倒置(坏档级)、694 水书怪必崩 null 解引用、鸭子逐帧背向玩家、海马出水取反等一批方向性反错的活宝 bug | 证据:memory/ai-parity-audit-2026-08-19.md
- **微残留清零 XXXX 批:actuator≠inActive 两大旗标**(08-19): #101 掷流首差从第 20,196 颗骰推到第 165,353 颗——五修含引擎级发现:Tile.actuator(0x800) 与 Tile.inActive(0x40) 是两个独立旗标,曾把致动位当 inActive 排除导致致动石格误判非实心(探针 (2430,920) 定罪);另用 IL 实证撤销了"34.5k 剑冢 HashSet 掷"的错误归因(.NET Add-only 枚举≡插入序≡JS Set,零分叉) | 证据:memory/xxxx-microresidual-final-clear.md
- **物品 tooltip 全量 1:1:四审终清零**(08-18): 用户一句"相比原版缺了不少信息,武器还有攻击力吧"引爆全链移植——按 GetLinesInfo(Main.cs:20488-20920) 行序逐行复刻:伤害/三系暴击/速度八档/击 knock 九档/渔力/镐斧(×5!)锤力/耗魔/可放置/弹药/材料/Buff 持续/词缀差分,再补低频七件(亮度脉冲/悠悠球 OneDrop 商标五层投影/研究行/商店价/专家大师行)。用户随后下禁令:"低频的也必须接入完整,禁止以低频为由不接"——全部落位,四轮 review 终清零 | 证据:memory/item-tooltip-parity-port.md
- **钻石窗口 IOSurface 八场攻防战**(08-18~19): "我的 GPU 资源非常充足,为什么双开还是爆"——三线取证+Chromium 源码注释钉死真相:爆的不是显存字节而是 IOSurface 张数(16×16 的 1KB 小图也分配失败)。随后打了一场八回合的持久战:chunk 画布 atlas 页化(活张数 446→28,运行期新建≈0)、TintAtlas 染色图集(41 个变体挤进 1 页)、纯 CPU 画布 willReadFrequently 化、看门狗僵尸三振自动切软渲染……从"必崩"打到"GPU 进程零死亡,尖峰后完全干净" | 证据:memory/dualwindow-iosurface-exhaustion.md
- **弹幕绘制偏移表全量 118 条**(08-18): 炸弹引线半截伸进碰撞盒的视觉错位,追到原版 Main.cs:29375-29826 的 num143/num144 偏移表——展开后铁律是"贴图左上角=(盒左+num144, 盒上−num143)",炸弹上移 8px 恰好让引线全在盒外。脚本机械对拍 118/118 全对,次日把 MinionProj(该表主体用户,曾从未消费、一律盒心居中)和浮标钓线全链接上 | 证据:memory/proj-draw-offset-table.md
- **鸟类帧族谱系:小动物 FindFrame 专属 case 全家族**(08-18): "感觉鸟的动画不对,在地上仍然用飞行中的动画"——挖出小动物帧调度大多不在 FindFrame 通用组而在专属 case:地面鸟原版根本不踱步(AI_024 只重力,vx 恒 0),站定门因此永假;鸮族 spriteDirection 取反与通用镜像行叠加会恒翻转(屁股朝前);萤火虫 4t 亮 3t 闪、珍稀宝箱怪伪装=帧 0(曾 14 帧狂闪)。连带第二波"走路金鱼鬼畜"修掉全部 aiStyle=7 小动物被城镇 NPC 档截胡的截胡链 | 证据:memory/bird-findframe-families.md + bunny-walk-frame-fix.md
- **Boss 全量审计波 1:25 族两波 8 代理,30+ 修**(08-19): 用户令"逐一审计",石巨人双代理模式推广到全部 25 Boss 族。波 1 抓出跨族系统性根因:BGM 裁决链键 flag/num3 号体系错位导致 17/24 族放错曲(石巨人放 Boss3、月总放世花曲)、弹幕自身出生音是审计盲区、猪鲨血量 50000 是 json 1405 旧值(1456=60000)。机械三王锯臂 ai2 追玩家态曾恒→1 死码、蜂后毒刺曾恒直飞全修 | 证据:memory/boss-audit-wave1-fixes.md + golem-3symptom-fix.md
- **地牢水宝箱浮空刀:312 还是 313?**(08-19): 两条新链 #32 Dungeon 清零——水覆写宝箱走了金箱支的 loot 掷数差连坐六段家具错位;更精彩的是"入口 0.6 框清墙上缘刀口":反编译 double 算出 312.99999976→312,而真二进制是 313——fl(10×0.6f)=6.0 的半 ulp round-half-even 可复现,Math.fround 四界修复。这是与金字塔案同族的"二进制-反编译刀口分歧" | 证据:memory/dungeon-waterchest-float-knife.md
- **液体最后清算 root59:百格级根 193→0 + 帧杀级联引擎**(08-19): #59 洞穴屋域四修:陷阱雕像是"PlaceTile 失败也调"而 Statues pass 恰好相反(两处语义相反勿互搬)、钟乳石是全族不是仅冰族、梁写 SetTileKeepWall 要清液体/坡/半砖;顺手造出 frameKillSweep 跨物件帧杀级联引擎(带帧写触发 Check2x2/Check3x2 整盒击杀)清掉 54 格尾巴。9293480 全管线首差推到 #63 | 证据:memory/wwww-root59-liquidation.md

## 二、新增坑(现象→根因→修复)

- **y 翻转两次翻车**(08-18): 现象:GL 绘制的背景图和地图垂直颠倒,修好后同一天又倒回来一次(用户两报) → 根因:并行会话共用文件,把修复静默写回旧版——clip-space y 翻转公式被覆盖蒸发 → 修复:tests/gl-layer-regression.test.ts 源码级断言锁定五项(y 翻转/mip 采样器/预乘上传等),丢任一立即红 | 记忆文件:webgl2-phase1-port.md
- **连续读档显存打爆**(08-18): 现象:连续读档逐次叠加,contextlost 风暴 26 万次、tab 3.4GB、chunk 自适应沉底 → 根因:GLSpriteLayer 漏挂 Renderer.dispose 世界切换清理链,LRU 纹理只增不减;熔断器固定 8s 冷却=永久振荡 → 修复:dispose 挂链+LRU 按字节(192MB)记账+冷却逐次翻倍封顶 60s+小地图纹理 noMip | 记忆文件:webgl2-phase1-port.md 六号坑
- **worker 整体崩毁全房失联**(08-18): 现象:`room.clients.filter is not a function` → worker exit(code=1) 全房掉线 → 根因:并行会话给 roomHost 周期定时器加逻辑时对 Set 用了 .filter;无守卫 setInterval 内一次抛错=worker 整体退出 → 修复:Set 先展开 `[...clients].filter`,四个周期定时器逐房 try/catch 只记日志 | 记忆文件:server-room-simhost-port.md
- **砍树自动收集瞬间崩溃+行走掉帧**(08-18): 现象:砍树掉落自动收集时游戏冻结;长流程 trace 里行走仍掉帧 → 根因:Inventory.add 裸读 `ITEM_DEFS[id].maxStack` 未知 id 即 TypeError 炸断 rAF 链;掉帧是 GC churn——液体渲染四邻 lq() 每帧 new 3.3 万个对象;用 trace 的 ProfileChunk CPU 采样按 timeDeltas 重建时间线找到死点 → 修复:inv.add 守卫+主循环熔断取证;lq() 零分配化 | 记忆文件:treecrack-gc-frameguard-2026-08-18.md
- **金鱼掉落"恐惧之魂"**(08-18): 现象:打死金鱼掉出恐惧之魂,掉落链全体错位 → 根因:vi_5395 屎堆手写条目插在自动注册循环【前】,ITEM_DEFS 内部 id=数组下标,插入点后全部物品 id 平移+1 → 修复:删手写条目改 BLOCK_TILE_BACKFILL 回填;新增 item-id-stability 测试钉死 id 严格递增 | 记忆文件:book-mimic-cultist-dragon-batch.md
- **地底蠕虫音墙**(08-18): 现象:地底蠕虫穿梭音全变成 boss 唤醒咆哮,多蠕虫叠成音墙;洞穴蝙蝠死亡音也"消失" → 根因:WAV_MAP['roar'] 双轨随机,而 PlaySound 第 4 参 Style 缺省是 1 不是 0——蠕虫掘地=Roar_1,boss 吼=显式 style0 的 Roar_0;再叠 case15 缺单实例互斥 → 修复:roar 键改单轨+单实例互斥+怪池 Hit/Death wav 进世界预热(首播懒加载静默) | 记忆文件:npc-ambient-sound-audit.md
- **悬停图标全黑**(08-18): 现象:光标移到宝箱上,悬停贴图变成黑方块 → 根因:曾误读为"乘光标格光照",用 source-atop 叠黑模拟变暗——source-atop 作用于整张已渲染画布,暗处 alpha→1=纯黑盖图标;而原版 GetItemLight 默认参根本不采样光照,图标恒全亮 → 修复:UI 层直画不乘光 | 记忆文件:cursor-icon-fullbright.md
- **tooltip 透明感三轮拉锯**(08-18): 现象:气泡"几乎透明"→修后"依然过透明"→铺实底后"过于不透明",三轮报障 → 根因:tint 像素循环把 alpha 通道误乘红通道(`d.data[i]*tmul[3]` 应为 `[i+3]`),深蓝底红通道≈23→alpha≈22 近全透明;0.925 的原版真值从未真正渲染过 → 修复:改正下标回到原版 alpha 236;教训:三轮报障该找根因而不是在 0.925↔1.0 之间找折中 | 记忆文件:item-tooltip-parity-port.md
- **树冠仙人掌接缝**(08-18): 现象:树冠-树干交界细缝无风也有,沙漠仙人掌柱同款,解剖台工具里却没问题;用户自调 zoom 1.27 触发 → 根因:chunk 拼装公式 `256×zoom` 非整数时 chunk 落小数设备像素,各 chunk 独立最近邻采样在边缘产生周期性 1px 透明缝;默认 1.25=320 恰整除从未暴露 → 修复:drawChunkGrid 整数设备矩形+1px 重叠;"工具里没问题"本身即信息→差异枚举法 | 记忆文件:chunk-seam-noninteger-zoom.md
- **迷雾周期性全亮闪**(08-19): 现象:小地图迷雾隔 20 秒突然全亮又瞬间恢复;F4 消雾也失效 → 根因:GPU 看门狗(20s 巡检)误清 CPU 数据——recreateAuxCanvases 无条件 fogPix=null,但迷雾是纯 CPU 缓冲与画布死活无关;整幅重建精确间隔 20s(24.8/43.9/63.9s)实锤 → 修复:fog 缓冲只在 dispose 清;入口 row>=h 复位 | 记忆文件:fog-flicker-f4-latetex-fix.md
- **独眼巨鹿冻在半空**(08-19): 现象:Boss 召唤出来冻在半空不动,AI 计数照常递增、速度满格、坐标恒定 → 根因:deerclopsMovement 只算 vx/vy 从不积分位置(668 是 noGravity+noTileCollide,原版由引擎直移);测试 harness 手动补积分把引擎缺口焊死了——测试绿但游戏坏 → 修复:movement 尾补 `e.x+=e.vx; e.y+=e.vy`;回归测试加位置积分档 | 记忆文件:deerclops-port.md 冻结事故节
- **地图放大到 1.37 即全黑**(08-19): 现象:全屏地图放大到一定程度全黑只剩玩家/NPC 头像,缩小恢复;哨兵日志显示 zoom 1.37 即黑 → 根因:sampler 对象的 MIN_FILTER 是 LINEAR_MIPMAP_LINEAR,而小地图/迷雾纹理 noMip 无 mip 链——用需 mip 的采样器采无 mip 纹理=纹理不完整→采样恒黑 (0,0,0,1);z<1 走 nearest 所以"缩小恢复" → 修复:linearNoMip 采样器按 e.mipped 分流;GL 铁律:sampler 对象与纹理参数是两套,incomplete 判定看生效组合 | 记忆文件:webgl2-phase1-port.md 全黑真凶终定罪节
- **石巨人负血不死**(08-19): 现象:Boss 血条打到负值不死、动画乱闪、boss bar 无头像 → 根因:Enemy.hurt 的放行段 `if(245||246||247||248) return false` 写在 `this.dead=true` 之前——"AI 首行接管"的假设根本没发生;并行会话跨会话契约改动未核调用侧 → 修复:放行收窄到 246 且加本体活门,245 本体死时在 hurt 内直接灭部件 | 记忆文件:golem-3symptom-fix.md
- **普通骷髅王必掉全套 Chippy 时装**(08-18): 现象:对抗性审查发现的刷物品漏洞——普通骷髅王约半数击杀掉全套红帽时装 → 根因:召唤只写 redHat 旗,但掉落五条规则/Renderer/GorePiece 全读 ai3;而 bossAI 又把 ai3 挪用为旋冲方向 → 修复:召唤补 head.ai3=1,旋冲方向改独立字段 skeletronSpinDir | 记忆文件:review-found-bugs-fix.md
- **软渲染模式下每帧新建 60 张画布**(08-19): 现象:--disable-gpu 下 canvas 哨兵报 60 张/秒持续泄漏,暂停中也发生;dev 复现不了 → 根因:GLSpriteLayer 初始化失败时 diedAt=0,退避判据 `now-0>5000` 恒真→每帧 dispose+new(构造器 createElement);dev 的 WebGL2 可用所以复现不了 → 修复:三处失败分支补 diedAt=now+acquireGL 统一 30s 闩 | 记忆文件:dualwindow-iosurface-exhaustion.md ⑫节
- **晴天云全不渲染**(08-18 深夜): 现象:好多云不渲染了,排查发现"该 bug 期间云从未显示过" → 根因:globalCloudAlpha 接了 `max(wr.cloudAlpha, 墓园×0.92)×atmo`——wr.cloudAlpha 是雨云浓度,晴天恒 0→云全透明;墓园压云是把某 CustomSky 内部式误当全局门 → 修复:globalCloudAlpha=atmo 直取(原版 ProcessCloudAlpha 默认恒 1) | 记忆文件:dualwindow-iosurface-exhaustion.md ⑨节

## 三、有趣的原始对话片段(archive-stream.json 08-18/08-19)

- **[08-18 00:06]** 👤 你看我这个世界的报告,很明显非常诡异吧?这确定是原版代码能干出来的?…画面里三棵树的底部都有异常,一个被蘑菇占用,两个是花,而且还…无法使用镐子破坏他们 [c44574b3]
- **[08-18 09:39]** 👤 # 泰拉瑞亚反编译转译TypeScript:这本质是一场"重写",而非"转换"…不存在成功先例,也没有可用的自动化工具…工作量以多人·年计 [e65c4575]
- **[08-18 12:02]** 👤 我的GPU资源非常充足,为什么总是挤爆 [8405c930]
- **[08-18 15:54]** 👤 离谱的是在你这里面没问题,但是在世界里的就是会有缝,包括沙漠的仙人掌也是有这种问题 [573d63f5]
- **[08-18 16:08]** 🤖 真凶抓到并修复了——你那句"仙人掌也有"是破案关键。根因:chunk 拼装×非整数缩放…默认缩放 1.25:256×1.25=320 恰好整数像素 [573d63f5]
- **[08-18 17:53]** 👤 现在生物的掉落物开始混乱了,打死金鱼居然出现"恐惧之魂"? [04569a63]
- **[08-18 23:39]** 👤 现在仍然有一些动画播的过快的生物动画帧,比如走路的金鱼,非常鬼畜 [d76053b3]
- **[08-19 00:01]** 🤖 全案闭环——两个症状同一个根,外加 20s 看门狗:闪烁,整幅重建精确间隔 20s(24.8→43.9→63.9)=GPU 看门狗周期! [8405c930]
- **[08-19 11:44]** 🤖 这桩"反编译与二进制行为不符"的奇案破了,而且破得很漂亮——根本不存在什么行为差:真凶是金字塔刷墙段每写一堵墙,原版都会经 SquareWallFrame 偷偷掷 1 颗骰(共 11,025 颗) [0650e0c7]

## 附:同期未入正文的可用彩蛋

- [08-18 00:34] 👤 "等这个清完是不是100%了?" / "所以有可能磨到100%对吧" [0650e0c7] — 用户对 100% 种子等价的执念
- [08-19 08:28] 🤖 "总进度:约 95%…里程碑链 9293480 0-53 槽八通道全绿✓ 里程碑链 12345(你的种子)0-53 槽八通道全绿✓" [0650e0c7]
- [08-19 10:31] 👤 "我感觉我们需要一个行为录制的方案,比如长按F5来启动场景的整体'录制'…对于调试非常重要" [c44574b3] — 用户的产品直觉时刻
- [08-19 11:21] 👤 "不要这种降级的,我们要从我们自己出发,看还有没有优化空间" [8405c930] — 否决跨实例方案,定调单实例自身减量
- [08-18 14:31] 👤 "我记得地域里的骨龙在接近时本身是有音效的,你要检查下各种怪物生物本身的音效是否正确移植完整" [1fc2b821] — 引出 232 处 PlaySound 全量审计
