---
name: shader-truth-pipeline
description: "★shader唯一真值管线:tools/disasm-fx.mjs反汇编XNA4 effect(.cso)+src/fx/SM2Effect.ts逐指令解释器;terraria-assets/{Pixel,Screen,Tile}Shader.cso全量在仓;关键pass行号表;染料/翅膀已消费"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-20T02:05:51.564Z
---

# shader 真值管线(2026-08-20 确立)

凡"编译 effect 不可见/无法 1:1"的登记一律作废——本仓有完整反编译管线:

1. **tools/disasm-fx.mjs**(自研):XNA4 D3DX effect 容器(魔数 0xBCF00BCF+0xFEFF0901,
   MojoShader 语义)→ technique/pass 结构 + DX9 SM2 字节码逐指令反汇编。
   用法 `node tools/disasm-fx.mjs <file.cso> <out.txt> [--only Pass,...] [--json out.json]`。
   踩坑已固化在文件头(comment size/CTAB 基准/preshader/texld=0x42 等)。
2. **src/fx/SM2Effect.ts**:SM2 像素着色器逐指令解释器(运行时直接执行原始字节码,
   uniform 注入对齐 C# Apply 可读侧)——染料(vanillaDyes)/翅膀视觉(vanillaWingVisuals)
   已在消费;[[wing-visual-port]] 四轮解码坑的出处。
3. **原料**:`../terraria-assets/{PixelShader,ScreenShader,TileShader}.cso`(1.4.5.6 全量)。
   Pixel 64 pass / Screen 27 pass / Tile 45 pass。
4. **关键 pass 行号**(fxPixel.txt 等按需重生成到 job tmp):
   HorizonClouds :2914 / WaterProcessor :2476 / WaterDistortionObject :2544 /
   Aurora :3109 / LensFlare :3215;Screen 的 FilterHeatDistortion :839。
5. 绑定表:DyeInitializer.cs(染料+Misc 全表,Aurora=PixelShaderRef+"Aurora"+
   Extra_286/287 噪声图,HorizonClouds/LensFlare 同文件 :440-487)。

**教训**:"shader 不可反编译"型登记(Paint.ts applyPaintTint 自造乘色、水体扭曲
"canvas 2D 无扭曲通道不做"、Aurora 噪声缺失)全部属于未发现本管线时的误判;
遇到一律走此管线取真值。用户令:秘密种子/滤镜等"缺失系统"直接子代理补齐,
禁止只登记。
