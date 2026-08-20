---
name: town-banner-doors
description: 城镇 NPC 入驻旗帜渲染（DrawNPCHousesInWorld 非放置 tile）+ NPC 开关门语义
metadata:
  type: project
---

2026-08-10 城镇 NPC 入驻旗帜 + 开关门（用户报"入驻有牌子/旗子 + NPC 该会开关门"）：

- **旗帜是渲染层挂画不是放置 tile**（Main.cs:40152 DrawNPCHousesInWorld）：对每个有家非流浪城镇 NPC（bound/老人 37 除外），在家坐标 home.x 上方找第一个实心格，**挂 House_Banner_1（2×2 帧 16×20，X=单/双人旗、Y=housingCategory）+ 叠画 NPC_Head_{id} 头像（24×24 fit）**；x=home.x*16+8、y=实心格下沿+18、同房多 NPC 每面 +26 下移；锚点=帧中心。城镇 NPC housingCategory 全 0（1 是宠物族 637/656/670/678-684）。hover 显名（手柄 housing 光标）未移植。资产：House_Banner_1.png 从 Steam xnb 解包；NPC_Head_0..120 全量 121 个拷贝 + VANILLA_MISC 注册。
- **NPC 开关门**（NPC.cs:54478-54500 开 / 54243-54252 关）：撞关着的门（tile 10/388）→ **Next(10)==0** 才开门（两方向回退 OpenDoor(x,y,dir) 失败试 -dir），成功记 doorX/doorY+closeDoor、ai[1]+=80 原地等；**走过门中心 >2 格 → CloseDoor**；>4 格或垂直离开 → 放弃关门。TownNPC.npcDoorUpdate 实现（openDoor/closeDoorAt 复用 Door.ts；高门 389 ShiftTallGate 未接）。
- 旗帜画在实体层**之前**（NPC 从旗前走过）；未做光照 tint（实体层自身无 tint，视觉一致）。

**Why:** 用户记忆的"牌子"其实是挂在 NPC 头顶家坐标的旗帜画——原版不往房间里放任何 tile（Banners tile 91 是敌人击杀旗，别混淆）。
**How to apply:** 查"某装饰是 tile 还是渲染叠画"先找 Main.cs 的 Draw*InWorld 族方法。关联 [[town-npc-persistence]]（旗帜依赖 home 恢复链）。

**2026-08-11 补完善三项**：
- **高门 NPC 开关**：npcDoorUpdate 加 tall gate 分支——撞 v_388_tall_gate_closed → shiftTallGate(closing:false)（锚点回溯返回 [x,anchorY] 记 doorX/Y）；过门关门判 doorType===v_389_tall_gate_open → shiftTallGate(closing:true)。音效 door_open/door_close 带坐标。
- **旗帜光照 tint**：原版 Lighting.GetColor(homeTileX, num3)——实现为 lightCtx.getImageData（屏幕 2× 光照图上一帧数据，一帧滞后无感）→ multiply fillRect 旗区（16×24）。lightCanvas 在实体层之后合成，首帧全黑跳过。
- **hover 名条**：原版 40255+ 鼠标悬停旗帜显 NPC 名——cam.screenToWorld(_mouseX/Y) 判旗矩形 → 半透明黑底白字名条（givenName 优先）。

**2026-08-11 修 Connor/头像两 bug**：
- **头像错**：NPC_Head_{i} 的 i 是 **head 索引≠NPC id**（原版 TownNPCProfiles.GetHeadIndexSafe → NPC.TypeToDefaultHeadIndex NPC.cs:7489 全表已建 TOWN_NPC_HEAD_INDEX：22 guide→1、17 merchant→2、588 golfer→25……）。直查 NPC_Head_{vanillaId} 显示的是错头像。
- **"Connor"**：givenName 是原版个人名池随机（GuideNames 含 Connor，语义正确）；错误在**显示层裸用个人名**。原版 FullName（NPC.cs:6657）：有个人名 → `Game.NPCTitle`（zh **"{1}{0}"=类型名+个人名**"向导Connor"；en "{0} the {1}"）；无 → 类型名。旗帜 hover（Lang.cs:416 GetNPCHouseBannerText）+对话标题+聊天替换三处已统一走 Game.NPCTitle。12 语言 NPCTitle 格式串已验证齐全。

**2026-08-11 旗帜尺寸纠错（用户对照官方原版实测推翻我的判断）**：House_Banner_1.png 像素分析 = 顶部吊杆+大面积垂布的**一面完整旗帜**（32×40 ≈ 2×2.5 格"方形 4 格"），**不是 2×2 帧表**——我此前按 `Frame(2,2)` 切 16×20（1 格）画小了。已改整图绘制（锚点中心、光照/hover 矩形跟随 32×44）。教训：**贴图内容先 ASCII 验证帧结构再信源码参数**；用户实测 > 源码推理。
