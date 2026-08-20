---
name: reference-vanilla-source-of-truth
description: "用户约定的开发原则——发现异常时必须先对照反编译源码/TEdit 校对再修,它们是正确标杆"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: af6cf2c7-84f1-4f59-9d74-9dc27cdc059e
  modified: 2026-08-09T11:05:12.169Z
---

用户明确约定(2026-08-07,树渲染对齐期间):凡用户报告视觉/逻辑异常,**必须优先**去反编译源码(1.4.5.6 见 `Terarria1456`、1.4.0.5 见 `Terarria1405`,均在 `~/Project/GLM/SandboxWorld/` 下)或 `~/Project/GLM/SandboxWorld/Terraria-Map-Editor`(TEdit)找对应实现,逐行核对差异后再修,不能凭直觉猜。

**2026-08-09 补**:本机 Steam 版已确认 1.4.5.6,全量反编译为 `Terarria1456/`(ilspycmd 10.1.1,1499 个 .cs,43M)。目录结构与 1405 不同——按命名空间分目录(`Terraria/WorldGen.cs`、`Terraria.GameContent.Drawing/TileDrawing.cs`,目录名带点号);NPC.AI 等超长方法完整不空壳,查新内容(1.4.4+ 的物品/怪物/Biome)优先查它;内嵌 `Terraria.Localization.Content.zh-Hans.*.json` 官方简中本地化,是 vui UI 移植的权威文案来源。本机工具链:brew 的 dotnet-sdk + `~/.dotnet/tools/ilspycmd`(不在默认 PATH,需 export)。

**Why**: 本项目目标是像素级复刻原版。多次凭感觉修(如树冠样式、棕榈树)都修错了方向;一旦对照源码(如 `WorldGen.GetCommonTreeFoliageData`、`TileDrawing.DrawTrees`)立刻找到根因。

**How to apply**:
- 常用源码位置:`Terarria1405/WorldGen.cs`(生成/树冠样式/GetTreeFrame)、`Terarria1405/GameContent/Drawing/TileDrawing.cs`(DrawTrees/Liquid 等绘制)、`Terarria1405/Item.cs`(SetDefaults 物品数值)、`Terarria1405/NPC.cs`(怪物数值)、`Terraria-Map-Editor/src/TEdit/View/WorldRenderXna.xaml.cs`(渲染端逐 tile 逻辑)、`Terraria-Map-Editor/src/TEdit.Terraria/Data/*.json`(tiles/items/walls 权威数据)
- **2026-08-09 补**:Terarria1405 的 `NPC.AI()`/`HitEffect()`/`Projectile.AI()`/`Recipe` 是空壳(反编译器放弃超长方法)。NPC 已用 ilspycmd 反编译本机 Steam 1.4.5.6 补全为 `Terarria1405/NPC.145.cs`(96371 行完整)。查怪物行为 AI 先查 NPC.145.cs;Projectile/Recipe 需要时同法补(`bash game/tools/decompile-npc.sh` 可改类型名重跑,-t 要全限定名如 Terraria.Projectile)
- 对照时抄关键代码段到回复里给用户看,指出我们实现与标杆的具体差异点
- 相关:[[sandboxworld-project-setup]] [[terraria-assets-pipeline]]
