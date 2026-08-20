---
name: alchemy-table-anim-collapse-fix
description: 炼金台355贴图塌碎修复:dgWr零帧+ChunkCache动画偏移预加破坏零帧重建门;修复=偏移后置+place3x3D逐格帧;探针TDZ教训
metadata: 
  node_type: memory
  type: project
  originSessionId: 4a66e745-9d91-4188-8ade-1e2b7775e8b4
  modified: 2026-08-17T07:35:51.849Z
---

炼金台贴图故障修复批（2026-08-17，用户 debug-report 报"物品贴图故障"）。

## 根因（双层）
1. **生成端**：`DungeonPass.dgWr` 系放置只写 type 帧全 0（原版 `WorldGen.Place3x3` :53610-53652 **逐格写 frameX/frameY=0/18/36**）。静态家具靠渲染端"零帧重建"兜底（VanillaTiler 扫左/上同类零帧格重建 ofx/ofy）无恙。
2. **渲染端**：`ChunkCache` 把 `animYOffset`（idx×pitch）**预加**进 fy 传入 drawVanillaCell → 零帧物体重建门 `(ofx===0&&ofy===0)` 被动画偏移破坏 → 炼金台 355/巫惑台 354（Main.cs:18868-18874 `tileFrame[355]=tileFrame[354]`，8帧/pitch54/rate5）在 idx≥1 帧整物塌成 9 块重复左上角碎片，idx=0 偶发正常（忽闪）。

## 修复（三处）
- `ChunkCache.ts`：动画分支只登记重烘焙，不再预加偏移
- `VanillaTiler.ts` drawVanillaCell：style 路径在零帧重建+分带换算**之后**叠加 `animYOffset`（=原版 GetTileDrawData addFrY 语义；215 篝火除外——ChunkCache 仍预加 campfireYOffset 36px 专属语义防双加）
- `DungeonPass.place3x3D`（唯二调用方=355/354）：逐格写帧 1:1 原版

**存量存档零迁移**：渲染端后置叠加使零帧重建重新生效——用户旧世界重载页面即修复。

## 验证
- 单测 `tests/anim-furniture-frame.test.ts` 4 条（recording-ctx：framed/零帧/idx=0 源矩形 36,144/36,144/36,36）
- 一次性 `tests/_alchemy-gen-audit.test.ts` seed 12345：3 台（alch×2 bew×1）帧矩阵全对，(3168,689) 即用户世界那张
- 探针 `scripts/_alchemyfix.mjs`：小世界自然桌+零帧化两轮，9 格哈希互异+动画 ✓

## 教训
- **探针 document-start 直 import 业务模块必炸**：抢模块图首执行权触发循环依赖 TDZ（`AVOIDED_BY_NPC_SHEETS`）。正确姿势=轮询 `window.__swGame` 出现后再 import（同 URL 只取已初始化缓存）。
- **视觉采样要逐格 3×3**（ getImageData 按字节切片"列哈希"实为横带，塌碎检测会假阳）。
- 探针合成 `setTileSilent` 不触发失效——素材懒加载不点火，recording 空矩形；需 invalidate 或走自然生成物。
- 并行会话实时编辑 TownNPC.ts（socialUpdate :970 调用未定义方法，首 NPC tick 即抛且打死渲染循环）——探针侧 prototype 中性桩绕过，未动其文件。

相关：[[blockframes-lookup-rebuild]]、[[parallel-vite-sessions]]
