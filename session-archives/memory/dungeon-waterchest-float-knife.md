# BBBBB 批：两新链 #32 Dungeon 清零（水覆写箱 loot 支 + 入口 0.6f float 刀口）

- **s22222（A176/T178 陈设族位漂）根因**：入口上方 0 号房在 worldSurface 之上 →
  dgBasicChests 水覆写箱（num2<ws+50 → itemType=**327/chestStyle=0**）。vanilla
  AddBuriedChest 前置 flag（WG.cs:36062 chestStyle==0）使 loot 走 **surface 支**
  （(flag23&&(flag||flag6))||flag11，:36280）；JS `surf=…&&false` 恒假走金箱支 →
  掷数差 → G 段流错位连坐 I/T/F/Pa/Ba（家具地板跑扫中心 ±1 平移画像）。修=flag0
  传参+支门接真。★327=Golden Key 非水靴（零前缀零掷）；★Prefix 重掷链不存在
  （TryGetPrefixStatMultipliersForItem switch 内零 return false——81-89 均有乘子；
  唯后置四门可 false 但对地牢箱族 item 常量恒真）。
- **m20260811（W4 入口墙洞）根因**：Legacy 入口 0.6 框清墙上缘 b0=(int)(319−10×
  0.6000000238418579)=312.99999976→312（double）vs 二进制 **313**——float 乘积
  fl(10×0.6f)=6.0（半 ulp round-half-even）可复现；与 YYYY 金字塔案同族"二进制-
  反编译刀口分歧"。修=Math.fround 四界。9293480 侧两模型同解 235（无判别力、零回退）。
- **方法**：手制链探针（▶Dungeon 前 dump031 八通道 0 差=pass 自差裁决）；
  __dgTowerTrace 空谱系=Legacy 入口判别；ENT 段级八点探针定界 0.6 框；
  12345 全量回归抓回滚错误修（勘误两则均为中途自纠）。
- **YYYY 湖体级联归因证伪**：#32 清零后 m 链 #49 L=11,707 原样残留——湖体=
  沉降/液体模拟独立自差（#48 输入全绿），非地牢级联；移交 liquid 域。
- **oracle 债**：caves-oracle.cs（禁区）须镜像 flag0/surface 支+0.6f float 界；
  且 oracle 中世界支（worldSize=1）dungeonL 起自崩（首次跑中世界即暴露）。
- 首差推进：s22222 #32→#49（0..48 绿）、m #32→#49、12345 #54 基线原样、
  9293480 #63。报告=content-parity-vs-vanilla-2026-08-16.md BBBBB 章。
