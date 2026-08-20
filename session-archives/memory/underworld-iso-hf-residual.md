# #28 Underworld 隔离复验（L 批 2026-08-17）——"全级联"证伪+QW 字节级清零+残余收拢进 HF

- **H 批"全级联"判定证伪**：#21/22/24/26/29 归零后隔离重放残差（act 26,551/wal 40,857/liq 10,290）与管线 [028] 逐位相同→残余全自因。隔离残差=管线残差时可断自因。
- **IL 探针真值链**（/tmp/sw-uwp/）：patcher 副本模式 `uwqw`（Cecil **嵌套类型要递归枚举**才找得到 `<>c` lambda！）；UWProbe.Entry/AfterQw/HfEntry/Phase 四注入点；服务器跑前**必须 rm wld**（-autocreate 见档即读不生成）；跑完恢复 app exe（并行会话共用,他们 01:11 起的服撞我换档窗口,passchain 输出会缺——换档前 pgrep）。
- **三定标**：liquidType 导入=真值（+1 编码全等,湿格 170,107=水 114,352+岩浆 55,755）；QuickWater 后全图 **0/486,934 差**；UW 段掷数 FNV 命中 **14,266,081=JS 精确**→HF 输入流+状态双全等。
- **修三件**：①LavaCheck 沙漠分支（7×7 墙 187/216→液体类型转岩浆；沙漠底岩浆池来源）②QuickWater tilesIgnoreWater（**484 滚动仙人掌**等 boulder 族 QW 期全局非实心——H 批只证了 138 无操作漏 484！）③HellFort 室内/门洞幽灵 type 保留（原版 active(false) 不清 type）+边界 half/slope 清零。
- **效果**：mid-world QW 残差 894→0；[028] typ 38,403→17,515、liq→9,396；隔离 typ(同act)→7,377。
- **残余=HF 房间网格**（act 26,551/wal 40,857/+25,569 掷全级联自此）：相位分解 家具+22,120/挂画+3,626=拒绝率症状（JS 房墙面积偏小）；主环-938。**房1-3 x 段相同、房1 内部即 17 格墙差而房2 干净**→掷序没错,是 hellFort 写语义/occ 判定——下批做逐房 colL/colR/rowT/rowB/occ 五元组跟踪（vs dump28 墙网反推）。
- 工具：_uwp2(QW 真值直拍)/_uwp4(truth 导入+房簇)/_uwp5(房内容差)/_uwp6(HF 相位掷数,phaseMark 钩已进 HellFortPass)；报告在 docs/worldgen/content-parity-vs-vanilla-2026-08-16.md L 批节。
