---
name: fog-flicker-f4-latetex-fix
description: 迷雾三修(20s看门狗误清fogPix=周期全亮闪/F4空同步=row停h未复位/分带重建fill(0)闪)+生命树晚到贴图note被pending早退吞——四根因四修复全探针实证
metadata: 
  node_type: memory
  type: project
  originSessionId: 8405c930-04c0-4d16-9037-36f3dcd374b8
  modified: 2026-08-18T16:18:54.254Z
---

2026-08-19 用户三报(debug-report 存档):①HUD 迷雾周期闪"全亮一下又恢复";
②F4 消雾失效;③生命树贴图不及时,手动破坏方块才渲染。

## ①② 迷雾双 bug(同一文件 ensureFogData)
**闪烁根因 = GPU 看门狗(20s 巡检)误清 CPU 数据**:recreateAuxCanvases 无条件
`fogPix=null`——但迷雾是纯 CPU 缓冲与画布上下文死活无关!每 20s 被清 →
缓冲重建(全 0=全亮)+ 分带 5 帧扫回雾 = 用户看到的周期闪(探针实测整幅重建
精确间隔 20s:24.8/43.9/63.9s)。修:fog 缓冲只在 dispose 清;看门狗只重置
_mapFogRowSeen(GL 纹理游标)。
**F4 失效根因 = 空同步**:整幅重建完成后 fogRebuildRow 停在 h 不复位;下次
整幅入口(F4/版本跳跃)row≠0 → `if(row===0) fill(0)` 不执行+分带循环零迭代
→ 直接落版本 = 什么都没画但版本追平。修:入口 `if(row>=h) row=0`。
**顺修**:分带循环改双向写(seen?0:FOG)+ 删 fill(0)——旧缓冲逐带纠正,
重建期不再有全亮帧(新缓冲天然全 0)。
观测:Renderer.fogFullRebuilds/fogIncrUpdates/fogFullWhy;探针
scripts/_fogwatch-probe.mjs(40s 走动整幅重建应恒 1+F4 后雾覆盖归 0+无回弹)。
修后:整幅=1、F4 雾覆盖 0%、10s 无回弹、零闪帧。

## ③ 生命树晚到贴图(note 被早退吞)
用户实报"手动破坏才渲染"= 晚到重烘链断。内窥探针(原型级 wrap
ensureVImage/vframe/note/onLoaded)铁证:烘焙期 ensure(Tiles_192) 时
**pending=true**(加载已被预载/他人发起)→ `if(pending) return null` 早退在
`bakeTracker.note(file)` **之前** → 晚到无人重烘 = 缺表 fallback 钉死。
修=note 提到早退前(failed 也 note:重试成功二次 land → 链路反而闭环)。
探针复验:拦截延迟 Tiles_191/192 15s → 传送生命树 → 表到达后
arrive=23(23 个 chunk 精确重烘)。
★探针两坑:st.type 是【内部 id 空间】与 vanilla vid 无关,找 tile 必经
__swTileByKey 换算(曾两轮扫错地方得出假阴性);像素断言要匹配目标色系
(生命树传送点在树冠=绿叶,判木质棕必 0)。
探针:scripts/_latetex-probe.mjs(断言版)/_latetex2-probe.mjs(全链内窥版,
request interception 延迟目标表 15s)。

相关:[[dualwindow-iosurface-exhaustion]](canvas 哨兵/BiomeBackground 同期)
[[dungeon-crash-targeted-rebake]](晚到重烘链前身) [[imagebitmap-root-cure]]
