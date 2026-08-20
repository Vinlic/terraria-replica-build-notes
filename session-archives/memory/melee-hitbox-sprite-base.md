---
name: melee-hitbox-sprite-base
description: "近战判定盒基底=手持贴图帧宽高(Player.cs:44485 !dedServ分支),32×32仅服务器兜底——曾被半截读法误改恒32,长武器(村正64×64)判定缩半"
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-17T10:11:05.453Z
---

2026-08-17 村正判定近修(用户报"判定稍近,与挥砍贴图不一致"):

**原版真身**(Player.cs:44480 ItemCheck_GetMeleeHitbox):
- :44483 先 `new Rectangle(itemLocation, 32, 32)`——**这只是 dedServ 兜底**;
  :44485 `if (!Main.dedServ)` 紧跟整盒替换为 `heldItemFrame.Width/Height`
  (手持贴图帧尺寸,5094-5097 缩框特例)再 ×GetAdjustedItemScale(=item.scale,
  meleeScaleGlove 泰坦手套 ×1.1)
- **判定是不旋转的 AABB**(ItemCheck_MeleeHitNPCs 直 Intersects,无旋转);
  锚 itemLocation,方向/重力翻转;useStyle1 三段相位扩展(早段宽×2 高×1.4 /
  晚段宽×1.4 高×1.1)乘在帧尺寸上

**事故链**:曾有会话只读到 :44483 一行,把基底改成恒 32×32 并把错误读法写进
注释("与武器贴图无关,此前误用贴图帧宽高")——村正贴图 64×64 判定缩半(体感
够不着),铜剑 36×36 反而超打。**教训:①读反编译必须读完整个方法,初始化值后
常跟条件分支整段替换;②错误注释会传染后续会话(本次险些又被"再修回去")**

修复:updateSwingHits 基底 `let bw=sprW, bh=sprH`(atlasIconForKey 帧尺寸,
游戏内定位早已在取);5094-5097/泰坦手套未实装不涉及。

验证探针 `_muramasa-hitbox-probe.mjs` 4 断言:atlasIconForKey(vi_155)=64×64;
中段挥击(pAnim=0.5 无相位扩展)前缘+40 僵司命中 45→25(32 盒必 miss=64 盒
实锤)、+90 对照不中。

**2026-08-17 追记:同族排查批("数据值→常量折叠"三案)**(用户问"还有类似问题+远程射多远")
1. **PickAmmo 箭速链**(Player.cs:52707-52723):弹药 `speed += item.shootSpeed` 加法✓;
   magicQuiver ×1.1(箭/桩,**无钳**);射手 buff 仅 speed<20 时 ×1.2 且钳 20——旧实现
   `min(20, ×buff×quiver)` 整体钳,高速组合(>20)被压回 20=射程缩水。修后探针:
   Hellwing6+木箭3=9 → 射手 buff 10.8 精确通过
2. **触及盒 tileReach**:任一射程配饰=布尔门 **X+3/Y+2 分轴**(ApplyEquipFunctional
   :12619-12622)——旧两轴同 +3 竖向多 1 格;旅程远置=现值(含配饰)×2+8(:18636)
   而非基座差值;钳 20 在配饰/远置后、item.tileBoost+blockRange(TB)在钳后加
   (GetTileRegion)。★射程配饰(2215工具箱/3061造物之手/5126)仓内全未实装——
   分轴偏差是休眠真 bug;equipStats 是逐次重算 getter,探针改临时对象无效(靴族
   测试须真穿装备同款教训)
3. **已验对齐勿再查**:箭/弹 timeLeft=1200(SetDefaults :555,基底 3600);枪弹
   无重力/extraUpdates/判定盒(既往批);combat 表 37 件"有 shoot 无 shootSpeed"
   多为原版真 0(通道/持续型工具);`?? 7` fallback 仅缺数据件兜底

相关 [[use-path-final-audit]] [[combat-convergence-batch]] [[default-run-speed-parity]]
