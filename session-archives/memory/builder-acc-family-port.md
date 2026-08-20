---
name: builder-acc-family-port
description: 建筑族7件实装+tileSpeed/wallSpeed倒数公式(累加→钳3→1/x→乘useTime)裁决铁证:25622-25632;挖掘pickSpeed加法减量链;blockRange分型调用点(挖掘不带/放置带)
metadata: 
  node_type: memory
  type: project
  originSessionId: 413208b1-378e-40ae-a408-9ae931eb30dd
  modified: 2026-08-17T11:23:36.622Z
---

2026-08-17 建筑族实装批(goal"未实装必须实装+1:1对齐"):

**tileSpeed/wallSpeed 语义裁决**(曾卡半天):反编译 ApplyItemTime(:4221)
`val=useTime×multiplier` 像乘法=更慢,与 wiki(+50%更快)矛盾。铁证在
**Player.cs:25622-25632**(Update 尾部聚合段):`tileSpeed>3→3; tileSpeed=1f/tileSpeed`
——**累加(+=0.25/0.5/0.05/0.15)→ 钳 3 → 取倒数 → 消费点乘 useTime** =
useTime/raw,更大更快。wallSpeed 同款:25628-25632。pickSpeed 无倒数(纯乘法,
减=快)。三者语义统一:都是"冷却乘数",tile/wall 用倒数表达"加速",pick 用减量。

**放置速度源表**(raw=1+Σ,钳3):Builder 药水+0.25(:9842)/ambrosia+0.05(:12458)/
风筝 buff+0.15(:9616)/砌砖刀族 acc+0.5(:12604)——★tileSpeed acc 份有**手持门**
(selectedItem.createTile≥0 且非火把;TileID.Sets.Torches=CreateBoolSet(4) 仅 tile4,
所有火把同 tile 不同帧)。本仓判定 `itemDef.tile !== undefined`(火把族走 Torch
特链无该字段,天然排除)。wallSpeed acc 无手持门(:12614)。

**pickSpeed 加法减量链**(挖掘冷却=useTime×pickSpeed,Game.ts tryMine):
Mining-0.25(:9818)/ambrosia-0.05(:12457)/食物档-0.05/0.10/0.15(:11534+)/风筝-0.15
(:9614)/chiselSpeed acc(古凿4056/创造之手5126)-0.25(:12610)。无下限钳(全叠满
0.15),冷却下限兜底。旧实现三层乘法近似(mineMult×pickMult)已废。

**blockRange 分型**(Player.cs:2604,源全集仅两处++:Builder :9844/Toolbelt407
:14873):GetTileRegion 的 TB 由**调用方**传——挖掘/桶=仅 sItem.tileBoost
(IsTargetTileInItemRange :45701)、放置块/墙/刷漆/提取机=tileBoost+blockRange
(:38939/:39058/:41154/:41012)、QuickMinecart 直调 GetTileRegion 不传=0(:5798)。
本仓 tileReach(tb) tb 参数=纯 tileBoost,blockRange() 由放置族调用点显式加。
**勿把 blockRange 内联进 tileReach**(挖掘射程会多+1)。

**授予表**(ApplyEquipFunctional :14714-14746):2214砌砖刀→tileSpeed acc/2215加长
握爪→tileRange acc/2216喷漆器→autoPaint/2217水泥机→wallSpeed acc/3061发明背包
→全家桶/5126创造之手→全家桶+treasureMagnet+chiselSpeed/407工具腰带→blockRange++
(**装备生效非手持**,14873)。2214-2217 的 accessory=true 在 SetDefaults5 的
**default: 段区间判断**(Item.cs:22346-22352)——提取器 case 扫描抓不到,已在
extract-equip-prefix.mjs 手补 4 id(同手机 3124 族先例)。

**autoPaint 消费**(PlaceIt_AutoPaintAndActuate :39935):放置成功后对放置覆盖格
TryPainting(tile 通道,applyItemAnimation:false);开关 builderAccStatus[3]==0
默认开(**builder toggle UI 未实装,GAP**)。本仓接线在 tryPlace 消耗门前,
tryPainting 复用(findPaintSlot 弹药栏优先/同色不扣)。

**探针五坑**(_builder-acc-probe.mjs 13 断言全绿):
①超时=并行 vitest 满载致世界生成>120s,--timeout=420000 解;
②killTileDropBait 世界生成期 player 未构造崩引导(挂一切破坏路径)——`if (!this.player) return` 守门;
③tryMine 自带射程门(8606)——目标格须 Y±3 射程内,且**天然首格可能是 tileNoFail
族一击秒破**(节流窗测不了)——探针自造石头格;
④二分节流窗必须**每测前回滚 lastMineHitTick**(否则命中推进基准,收敛恒=hi);
⑤json 不能 `import(...,{assert})` 在 vite 页面——用 fetch。

相关 [[melee-hitbox-sprite-base]] [[use-path-final-audit]]
