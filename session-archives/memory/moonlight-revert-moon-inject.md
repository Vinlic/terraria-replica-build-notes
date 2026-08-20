---
name: moonlight-revert-moon-inject
description: "2026-08-20定案:worldLayer月光重构整体回滚(默认关,?worldlayer=1选择加入);稳定基线=下午版全屏乘光;夜月唯一修复=月盘注光;光照对原版大差距另立专案docs/lighting-parity-project.md"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-20T01:56:03.192Z
---

# 月光 worldLayer 事件收口与光照专案(2026-08-20)

**终态(同日第三次转向)**:用户定案"按原版源码设计方式落地,着色器也要反编译
实施"+"以前有移植不代表完整和准确,需要细致考究"+"不要近似,全量对齐 1:1"
→ 专案 M1-M4 当日落地:
worldLayer 分层默认开+GL 双纹理精确乘+ColorOfTheSkies 单源(天空贴图/远景/云/
环境实体)+晨昏地平线系统(src/lighting/Horizon.ts)+太阳双通道+bgTopY。
★校勘出既有移植三 bug:耀斑强度多乘 celestial/baseRot 误用 sun.y(应屏顶世界Y)/
日月轨迹漏 bgTopY。夜空 (4,4,18) 精确命中原版理论值。
终轮 review 再修四件 XNA 全通道乘语义(渐变/月亮 vis²)+云量压暗+天空贴图竖向
1:1@bgTopY+闪电改走 cots。群系变色四块全量落地(scanBiomeLightCounts 可视窗
计数→蘑菇/墓园平滑→setBackColor 四块+日月色,猩红 R 用 G 归一/蘑菇月色跨通道
快照均为原版原文;端到端 (165,115,185) 精确命中)。
**残项全清(同日"逐个收齐全部对齐"+三子代理)**:星空全量(Star.cs 状态机/
DrawStar 亮度公式/坠星尾迹/StarFall 接坠星实体)/日食 Sun3/BackgroundDrawers
13 项/AuroraSky(AuroraSky.ts,月相八分支+ModifyTileColor 0.08 进 cots;shader
噪声不可复刻已诚实登记)/sunScorch 容器+AdjustIntensity/耀斑影子项真接线
(Player.advancedShadows,%1 保号 C# 语义)/sunModY 拖拽全链/Sun2 太阳镜
(head 12=物品237)/海洋背景层(8 变体远景槽3,"forest 兜底"自造已除)。
中间态(全屏乘光+月盘注光回滚到稳定基线)已被此终态取代;月盘注光仍服务于
?worldlayer=0 逃生门。

用户定案(原话级):"下午那个月光改造前的版本已经非常稳定非常好,就只是月亮贴图
晚上不够明亮,一改全部炸掉"→ worldLayer 分层([[moonlight-worldlayer-split]]的
1b369fe2)默认关;后续再报"光照和原版差距非常大,太阳渲染差十万八千里"→
**另立专案** `game/docs/lighting-parity-project.md`(差距清单/原版锚点表/里程碑)。

## 落地终态
- 默认路径=全屏乘光(下午稳定基线);`worldLayerEnabled` 改 `get('worldlayer')==='1'` 选择加入
- **夜月修复**:SkyRenderer.moonScreen(月亮分支每帧写屏位+盘半径)→
  compositeLight 默认路径在 lightCanvas 注径向满光(盘内乘法≈恒等=原版"月亮不吃
  乘光",外圈 2.2×柔晕)。验证:月心 19→(147,253,196) 明亮白盘
- 分层路径(选择加入)合成已重写为 GLWorldLight 双纹理精确乘
  (`out.rgb=w.rgb×l.rgb, α=w.a` 预乘)——A/B 实证昼 on/off 史莱姆逐像素全等;
  2D 三步回退(copy→multiply→destination-in)
- 我 2026-08-20 的 cots 单源接线(天空贴图×cots/远景tint/云色源)已整体回滚
  ——不是因为错,是用户要先回稳定基线;代码可从本会话/git 复用进专案 M2

## ★教训(比代码更值钱)
1. **观感耦合铁律**:天空/云/远景/光照是同一条 ColorOfTheSkies 色链,换合成
   架构必须与色链单源化同批落地,分批=每批都"全变了"(本次三症状连锁的根)
2. **用户眼睛>探针绿灯**:我 A/B 数值全绿后用户仍实报夜景不对(其在真机/GPU
   环境走 2D 回退或观感差异探针测不到);两轮探针误测前科+本轮,探针只能作
   下限证明,观感验收必须用户过目
3. Canvas2D 'multiply' 数学上无法表达"乘色保α"(PDF blend (1-αd)Cs 项+α膨胀
   0.7→0.91)——精确乘只能 GL 双纹理;写 GL 两个坑:跨级共享 uniform 精度须
   一致(highp);归一化 aPos 勿再除 uCanvas(quad 缩 1px,readPixels 全零定位)
4. 原版锚点全表已固化在专案文档 §1(天空=Background_N×cots/月相地板11-19/
   GetColor 线性乘 A=255/远景层×cots/日月星从不进 tile 光照)

## 关联
[[moonlight-worldlayer-split]](被回滚的分层重构)·[[weapon-invisible-remaster-pack]]
(同文件76处r.ctx修复,保留)·专案文档 game/docs/lighting-parity-project.md
