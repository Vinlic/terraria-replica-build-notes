# EEEEE：oracle 镜像债清零 + 中世界支四根因

- **中世界 oracle 自崩真首差=marble（pass 21）非 dungeonL**（BBBBB 误报——其链探针 PRE 段 ora 列非 oracle 检查点值；裁决法=x86 dump 逐 pass 边界哈希直拍 oracle）。
- 四根因：Marble Count=WorldArea 尺度（W*H/5040000，中→Next(9,19)）/Granite=WorldWidth（W/4200，中→Next(6,13)）/skyLakes=1+(X>8000)+(X>6000)（cs:11197，中=2）/**★DBnd 钳位域硬编码 4200/1200**（vanilla DungeonBounds 世界相对 Clamp(…,10,maxTiles-10)；中世界 dgBounds.B 被 1190 截断→pit 循环 y2 掷域错→Pi 起全段流偏；修=DBnd.WMax/HMax 程序头赋值）。
- 修后中世界 17 段 DGFLOWSEC/DGSEGHASH 与 JS 逐段全等；dungeonL..dungeon 4 通道逐位同；x86 031/032 三方全等。
- 镜像六件：BBBBB flag0+0.6f float 四界（(double)(float)(s*0.6f)≡Math.fround 双层）/ZZZZ 金字塔每墙 Next(0,3)/CCCCC Place2x2 右下锚（solid2 无平台腿）/AAAAA 矿轨帧链（Fc 引擎前向引用→FC_* 表上移 FC_PLAT 后；局部变量先声明后引用铁律）/GGGGG+PPPP 雕像族（flag2 双门+else-if 半砖帧清+幻影成功+484 Check2x2 本地支）——statues..beehives 五检查点因此双种子转绿。
- _oraclesync 双种子 71/78（残=dirtlayer/rocklayer 预期+piles/settle2/cactus/microbiomes 在途带）；中世界 66/73 首差 quickcleanup=8 格 half/slope 未哈希通道隐性差（上游半砖/坡写差经 SaveSlopes 杀门暴露，中世界特异）。
- ★方法论：oracle↔x86 对拍用 dump 逐 pass 边界直拍（不经探针转述）；段级掷数/流指纹（DGFLOWSEC+DGSEGHASH vs JS rng 计数代理）是流分歧定位最快刀；链探针哈希列口径必须先验证再当裁决。
- 详见 game/docs/worldgen/content-parity-vs-vanilla-2026-08-16.md「EEEEE 批」+ /tmp/final-runbook.md EEEEE 附录。
