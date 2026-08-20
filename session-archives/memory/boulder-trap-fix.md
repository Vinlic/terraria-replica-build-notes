---
name: boulder-trap-fix
description: 巨石机关三根因(自造物理档/中心点碰撞恒沉/裸写tile绕过渲染失效);AI_025真档;渲染改动必走setTile入口
metadata: 
  node_type: memory
  type: project
  originSessionId: c212e38d-8db4-446d-b3da-4e20d707caf7
  modified: 2026-08-14T03:49:46.411Z
---

2026-08-14 用户报巨石机关"下落慢+落地渐沉穿墙+原位贴图残留"(类比尖刺球案):

**三根因**:
1. **自造物理档**:TRAP_SHOT_STYLE.boulder 用 grav 0.22 无终端;原版 proj 99=**31×31/aiStyle 25**,重力 **0.3**/终端 **16**(:24723/:24667),滚地加速 vy≤6 且 |vx|<7 → ±0.05(:24699,**落地的巨石不会停,持续加速滚到撞墙**),旋转 vx×0.06(:24664),落地反弹 **−lastVy×0.2 仅 lastVy>5**(:17551,软落直接落定),撞墙 HitTiles+碎裂 Kill(:17574;Kill 无专属处理,仅 FTW 才 BoulderExplosion :67401)
2. **中心点碰撞**:shotCenterSolid 14×14 盒中心检测——落地 vy=0 分支**不回退 y**,每 tick 恒沉 grav px("逐渐穿墙沉降"根因);修=分轴 AABB 前沿三点采样(boxEdgeSolid)+ 每轴阻挡即回退
3. **裸写 tile 绕过渲染失效**:Wiring 巨石清格曾 `st.type[up]=0` 直写——TileStore **listeners(渲染 chunk 失效靠它)只挂在 setTile 唯一写入入口**→原位贴图残留成双;修=st.setTile(i,j-1,0)。**铁律:运行期任何 tile 改动必走 setTile/setActuated 入口,裸写数组=渲染残影+存档漂移双雷**

tests/boulder-trap.test.ts 3 条(重力/终端/31 盒、贴地不渐沉+平地滚动不消亡、硬落 ×0.2 软落落定+撞墙碎裂);spiky/sfx-wiring/cannon 44 邻域回归绿。

**测试 mock 坑**:TrapShot 全链 mock 需 entities.{critters,npcs,projectiles} 数组+player(dead=true 远置)+critters()/npcs() 函数双份(内部两处取法不同)。

**第二回合(用户档 sbw.json 实证)**:巨石 tile 是 **2×2 多格对象**(帧 (0,0)/(18,0)/(0,18)/(18,18),锚=帧 0,0 左上)——钩子曾只清单格:①残余 3/4 贴图="左下角透明缺块";②弹 99 嵌残余实心格即刻碎裂="没有巨石落下"。修=帧偏移归一到锚→清 4 格(全走 setTile)→锚点生成 1 颗。**旧档不需要新建地图**(wire/帧数据完好);挖掘侧(镐敲巨石)同款 2×2 转换待接。原版口袋几何(DeadMansChestBiome.cs:542-610)=3 宽(左空柱 X+巨石 X+1..X+2+6×6 石壳)。

**第三回合(用户报"碎裂音原地消失不滚动")三连环修**:
1. **X 轴碰撞曾 vx=0 也查**(sign(0)||1 兜底查右缘)——出生盒 31×31 比清空 2×2 宽 14.5px 天叠陷阱壁(原版 3 宽口袋同几何,靠"velocity 轴被改写才响应"容忍)→ 首拍碎裂。修=X 轴"移动后新进入实心"才响应(before/after 双检,预叠方向放行)。
2. **Y 轴必须严格阻挡**(每拍移动→检测→回退+置 0 钉位)——若学 X 做预叠容忍:贴地巨石每 tick 沉 grav 一点,沉过 y+h-1 采样线后 before=after=true 恒放行=加速沉穿(逐 tick 轨迹探针实锤)。**分轴策略不同是本质,勿统一**。
3. **滞滞启动踢**(:24578-24661):落地态且 vx==0 → 探 ±40px 侧壁(左实→+0.5/右实→−0.5/两侧空→Center.X 格奇偶)——没有它 vx=0 命不中滚地加速 ±0.05 两分支,巨石落地即死停不动。

**第四回合(用户再报"凭空消失")**:真实陷阱几何里巨石**右列坐在未致动石上**(gen 支撑只铺左空柱+巨石左列,右列是壳石)——弹 99 出生即嵌地形 ~15px,任何自建采样都会翻车(嵌住/误碎/恒沉三连)。**终修=放弃手搓碰撞,巨石走 moveAndCollide**(玩家/敌怪同款,贴边钳制+onGround/hitWall 旗标):hitWall→碎裂,onGround→硬落反弹 ×0.2/软落落定。boxEdgeSolid 助手已删。**教训:实体碰撞永远优先复用引擎 moveAndCollide,自建采样只配做只读探测(视线/探壁),不配做位移响应**。

**终态验证**:boulder-trap(重力/终端/31 盒/不渐沉滚至挡墙碎/硬落×0.2 软落落定)+boulder-2x2(整对象清+锚点单弹)+boulder-trap-e2e(真实口袋几何:双支撑致动→下落≥3 格→滚动>2 格→60t 后才碎)5 文件 29/29 绿。**逐 tick 轨迹探针法**全程立功。
**存档审计法**:_boulder-save-audit.mjs(SaveFile.readVarint+rleTiles 通道解码镜像)可秒查任意档内陷阱态——已清理,需要时照注释 20 行重写。
