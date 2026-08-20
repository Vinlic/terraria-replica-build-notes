---
name: lowend-perf-trace-161246
description: trace 16:12 CPU剖析=粒子碰撞42.7%冠军(逐粒子isSolid)+clientWidth/matchMedia逐帧布局读;三刀落地(SOLID_LUT+内联粒子循环+双缓存);低配机优化点清单(粒子cap/光照模糊/小地图节流)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-19T08:35:13.400Z
---

2026-08-19 用户问"极端糟糕设备还有什么可优化"(机子资源充裕但要考虑差的),
给了 112s/554MB trace(4173 preview 包,带 19411 块 CPU 采样)。

## CPU 自耗时剖析(采样聚合法:ProfileChunk.nodes+samples+timeDeltas)

| 占比 | 项 | 归属 |
|---|---|---|
| **42.7%** | 巨函数 L | **粒子碰撞循环**(Game 粒子段:每粒子每帧 2 次 solidAt,每次 floor×2+inBounds+isSolid(双重 idx 乘法+TILE_DEFS 对象查)) |
| 4.1% | drawImage | canvas 本征 |
| 1.7% | requestAnimationFrame | rAF 派发归因 |
| 1.0% | _step | WaterWaves 步进 |
| 0.8% | blurLine | **LightMap.ts:54 光照模糊** |
| **0.8%** | get clientWidth | **Renderer:2869 波模拟逐帧读 canvas.clientWidth=每帧强制布局** |
| 0.6% | mmHudBlit | 小地图 HUD blit |
| 0.6% | compositeLight | 光照合成 |
| 0.1% | matchMedia | **isTouchDevice 每帧调(VUI.drawCursor)** |
| — | GC 644 minor/9 major | 粒子对象 churn(可控) |

★minified 巨函数定位法:callFrame 的 lineNumber+columnNumber 到 dist/assets/
对应 bundle 行**按列截取上下文**(行号 0 基!547→readlines[547]);定位到
`const L=(ce,ue)=>{...isSolid...}` 在粒子循环内。

## 已落地三刀
1. **TileStore.SOLID_LUT**(Uint8Array 类型id→1/0,模块构建一次)+ isSolid
   单次 idx(旧双重乘法)。全 isSolid 调用方受益。
2. **粒子循环完全内联**:type/wire/w/h 数组局部化+单次 idx+LUT 直读,零函数
   调用/零闭包;世界外视为空语义保持。验证:300 粒 100% 停驻(grav=0)/0 穿地/
   0 NaN;2000 粒全帧均值 8.31ms。粒子三测试文件 25 用例绿。
3. **clientWidth 缓存**(_cssW,resize 刷新)+ **isTouchDevice 一次判定缓存**
   (TOUCH_cached)。消灭两处逐帧布局/媒体查询。

## 追记:自制碰撞物理整体退役(2026-08-19 用户裁定"直接对齐原版,不要自制")
原版权威:Dust.UpdateDust(Dust.cs:423)= `position += velocity`,重力/阻尼按
尘型在发射端给(重力尘 +0.05 :894 族/阻尼 0.93-0.99),**零地形碰撞**——
全文件 Collision.* 仅十余特定尘型分支。火把火星原版参数(TileDrawing.cs:7220-7236):
上窜 vy-=1.5、×0.3 阻尼、2/3 noGravity(我方发射器本就上浮 ✓)。bounce/settle
自制物理(碎屑反弹停驻)整体删除,运动律三行原版化(grav 缺省 0.05 对齐);
下落碎屑穿地=原版行为(寿命 0.7s×0.05 只落 2-3 格,视觉无差)。验证:100/100
碎屑穿地不停驻、0 NaN、2000 粒 8.34ms、粒子三测试 25 绿。★教训:自制效果
不仅吃性能,还偏离"反编译唯一标杆"纪律——自制审计时应连同其【物理】一起审,
不只审数值。TileStore.SOLID_LUT 保留(isSolid 本体仍受益:单 idx+LUT)。
dist:index-DKaaGzHW。

## equipStats 记忆化落地(2026-08-19,367s trace 的 GC churn 主源)
**PlayerEquipStats 类型别名从内联注释放别;getter = 内容哈希键缓存**
(equipStatsKey:甲/饰品/社交 20 槽+染料 10 槽 id+extraAccessory+usedGummyWorm+
panicTime>0+buffs.active 键集合;输入清单注释钉死)。computeEquipStats 原体;
返回对象 Object.freeze(+wing/jumpOpts)=硬护栏。**counterWeight 掷骰迁消费端**
(rollYoyoCounterweight,WeaponProj):原版 ResetEffects 每帧重掷=使用期随机,
getter 每访问掷会被缓存冻结;counterweightDecision 加 yoyoBag 旗分支
(vanity→直置→现场掷)。setBonus 类型改 ArmorSetBonus(原 ReturnType<嵌套函数>
随放别失效)。E2E:同引用命中/换装失效/冻结✓;yoyo-bag 四支旧行为测试重写;
六路锁 tests/equip-stats-cache 8 用例绿(★将来给 getter 加输入必须同步键+
此测试)。坑:ITEM_BY_KEY 是 vi_ 键空间('copper_helmet' 是迁移表 id 10036,
测试须 vi_89_CopperHelmet);def 数值断言依赖 statOfInternal 解析,身份断言为主。

## 记忆化 review 战果(2026-08-19,"避免引入任何意外")
**★review 抓到真漏网:prefix(重铸词缀)不在内容键**——换词缀不换 id = 键不变 =
Warding→Arcane 数值陈旧,tests/equip-stats 的词缀用例当场红。根因=审计输入时
只 grep `this.*`,prefix 挂在【槽条目对象】(s.prefix,compute:899)上被漏。
修=键改 `(s?.id ?? 0)+'p'+(s?.prefix ?? 0)`(armor+dye 两数组),补第七路锁。
**教训:枚举派生数据的输入时,this.* 之外必须扫槽条目/参数对象的字段读取
(s.prefix 类)——对象字段的读取不显形于 this 前缀。**
其余 review 全清:wing 零写手(飞行计时是 this.wingTime,从 eq.wing.time 只读
拷贝)/counterWeight 无决策外读者(无">0 当有袋"暗代理)/compute 无全局可变读/
immuneBuffs 纯甲扫描/jumpOpts 无直改/Object.assign·delete·方括号写全零/
无其它测试依赖"每次访问重掷"。免疫重建副作用时序与旧版逐位等价(唯一写者
本来就是 getter,键覆盖其全部输入)。dist:index-lB_EGiCU。

## 自制物理全仓审计(2026-08-19,"review 还有哪些自制物理")
**对齐 ✓(行号引用齐全)**:ItemDrop(液体分档重力 0.1/0.08/0.05/0.065+
wetVelocity+吸拉 PullItem+shimmer 三分支,WorldItem.cs 全引)、GorePiece
(:352-769 链/:929-1042 碰撞尾段——**落地滑移是原版游戏对象本有的**,
非自制)、Tombstone(aiStyle17 :23677-23718)、Arrow/弹幕 bounce(水书/
Molotov 火云 = 原版弹跳弹幕机制)、golfPhysics、投掷/玩家/AI 各族。
**遗留三件**:①死亡粉碎粒子过时注释(描述旧 bounce/settle)已修;②**粒子层
= 结构性近似层**(emitTorchSparks/emitTileParticles/spawnParticles/spawnBurst:
发射率/位置 1:1 引用,但运动律用 grav/damp 近似"按尘型物理"、视觉用色块
近似 Dust.png——彻底对齐 = 迁真 dust 系统,工作量大,登记);③WaterWaves
水面波位移=自制物理(原版 _waveMask 死代码零波位移;已登记取舍,退役会
明显变"静",用户拍板)。★判别口径:游戏对象(掉落物/尸块/墓碑/弹幕)的
碰撞物理是原版机制;**尘/粒表现层**原版零碰撞——自制碰撞只该出现在前者。

## 低配机优化点清单(按价值排序,未做)
- 粒子上限按 gfxQuality 分档(现有自动画质系统挂钩:低档 cap 发射率/寿命;物理已原版化,此项只剩绘制成本)
- 光照 blurLine/compositeLight(~1.4%):低档减模糊 pass 或降光照分辨率
- 小地图 HUD(mmHudBlit+drawMinimap+readPixels ~1%):低档降刷新率(2-4Hz)
- drawImage 4.1% 本征:低档已有 chunk 质量;可再评估 dirt-batch
- GC churn:粒子对象池(644 minor GC 主源之一)
- 探针:scripts/_particle-bench.mjs(停驻验证+2000 粒帧耗)

相关:[[dualwindow-iosurface-exhaustion]] [[vanilla-liquid-port]]
