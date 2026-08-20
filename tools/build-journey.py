#!/usr/bin/env python3
# build-journey.py —— 生成 docs/sandboxworld-journey.html(从0到1 大师级开发史长页)
# 输入:/tmp/journey-data.json(24 会话+记忆归属+档案锚点)、/tmp/journey-mining.md(坑史/转向/每日大事记)
import json, re, html, urllib.parse

DATA = json.load(open('~/Project/GLM/SandboxWorld/tools/journey-inputs/journey-data.json', encoding='utf-8'))
MINING = open('~/Project/GLM/SandboxWorld/tools/journey-inputs/journey-mining.md', encoding='utf-8').read()
MEMS = json.load(open('~/Project/GLM/SandboxWorld/tools/journey-inputs/memories.json', encoding='utf-8'))
STREAM = json.load(open('~/Project/GLM/SandboxWorld/tools/journey-inputs/archive-stream.json', encoding='utf-8'))
OUT = '~/Project/GLM/SandboxWorld/docs/sandboxworld-journey.html'

DAYS = ['08-05','08-06','08-07','08-08','08-09','08-10','08-11','08-12','08-13','08-14','08-15','08-16','08-17','08-18','08-19','08-20']
MSGS = [4052, 2784, 3311, 1150, 12502, 23278, 27814, 21520, 50510, 9122, 3299, 2496, 14871, 13919, 12985, 2168]
CONC = [2, 2, 2, 1, 7, 9, 13, 14, 20, 12, 6, 12, 18, 14, 18, 7]
DIN  = [946.7, 843.2, 920.7, 218.6, 3219.2, 7049.0, 8048.7, 6121.9, 15285.2, 2790.0, 972.5, 734.3, 3653.7, 4122.8, 3881.6, 555.1]
DOUT = [2.11, 1.11, 1.05, 0.70, 5.12, 7.98, 9.89, 8.24, 18.36, 3.29, 0.69, 1.06, 6.39, 5.72, 5.66, 1.02]
# 本地日对齐(08-05..08-16);曲线为"现存文件出生分布"口径
SRC  = [990, 990, 1346, 1377, 2978, 29164, 31404, 38354, 104134, 157059, 199732, 228102, 239123, 298354, 382329, 460880]
TST  = [0, 0, 0, 0, 385, 1704, 5304, 14094, 43181, 52599, 54928, 55047, 55134, 55872, 56585, 58383]
SCR  = [826, 867, 1037, 1621, 5320, 8498, 10937, 13915, 23424, 25959, 25959, 26059, 26133, 27210, 28808, 30285]
TLS  = [0, 0, 0, 0, 0, 381, 693, 822, 994, 8937, 9560, 9996, 9996, 9996, 9996]
HUM  = [127, 155, 161, 17, 176, 304, 325, 361, 476, 147, 30, 59, 184, 235, 255, 52]
SPR  = [3713, 3713, 3714, 3714, 4518, 4540, 4563, 5341, 11029, 11029, 11029, 11029, 11029, 11029, 11029, 11029]

def esc(x):
    t = str(x)
    for a, b in (('/Users/user', '~'), ('/Users/vlinlic', '~'), ('/Users/vlin', '~'), ('/Users/vli', '~'), ('/Users/vlc', '~'), ('Users-user-', ''), ('/Users/userlic', '~'), ('/Users/user', '~'), ('/Users/vinli', '~'), ('/Users/user', '~'),
                 ('user@mac', 'user@mac'), ('mac', 'mac'),
                 ('user', '玩家'), ('user', 'user'), ('/Users/vi', '~')):
        t = t.replace(a, b)
    return html.escape(t, quote=True)
q = lambda p: urllib.parse.quote(p)

# ---------------- 解析 mining ----------------
def section(txt, start_pat, end_pat):
    m = re.search(start_pat, txt)
    if not m: return ''
    rest = txt[m.end():]
    m2 = re.search(end_pat, rest) if end_pat else None
    return rest[:m2.start()] if m2 else rest

def parse_pits():
    body = section(MINING, r'## 一、坑史.*?\n', r'## 二、')
    cats = []
    cur = None
    for line in body.splitlines():
        h = re.match(r'###\s+([A-D])\.\s*(.+)', line)
        if h:
            cur = {'key': h.group(1), 'title': h.group(2).strip(), 'pits': []}
            cats.append(cur); continue
        b = re.match(r'-\s+\*\*(.+?)\*\*\s*[（(]([^)）]*)[)）]\s*[:：]\s*(.*)', line)
        if b and cur is not None:
            name, date, rest = b.group(1), b.group(2), b.group(3)
            mem = ''
            m = re.search(r'记忆文件[:：]\s*([^\s|]+)', rest)
            if m:
                mem = m.group(1)
                rest = rest[:m.start()].rstrip(' |')
            parts = [p.strip() for p in re.split(r'\s*→\s*', rest) if p.strip()]
            cur['pits'].append({'name': name, 'date': date, 'parts': parts, 'mem': mem})
    return cats

def parse_pivots():
    body = section(MINING, r'## 二、方向转变.*?\n', r'## 三、')
    out = []
    for line in body.splitlines():
        b = re.match(r'-\s+\*\*(.+?)\*\*\s*(?:[（(]([^)）]*)[)）])?\s*[:：]\s*(.*)', line)
        if b:
            name = b.group(1) + (f'({b.group(2)})' if b.group(2) else '')
            rest = b.group(3)
            mems = re.findall(r'[\w./-]+\.md', rest)
            out.append({'name': name, 'desc': rest, 'mems': mems})
    return out

def parse_daily():
    body = section(MINING, r'## 三、每日大事记.*?\n', r'## 附')
    days = []
    cur = None
    for line in body.splitlines():
        h = re.match(r'###\s+(\d{4}-\d{2}-\d{2})(?:[（(]([^)）]+)[)）])?', line)
        if h:
            cur = {'date': h.group(1), 'theme': (h.group(2) or '').strip(), 'events': []}
            days.append(cur); continue
        b = re.match(r'-\s+(.*)', line.strip())
        if b and cur is not None and b.group(1).strip():
            cur['events'].append(b.group(1).strip())
    return days

PITS = parse_pits(); PIVOTS = parse_pivots(); DAILY = parse_daily()

# ---------------- 会话卡片 ----------------
def loc_ts(iso):
    if not iso: return ''
    from datetime import datetime, timedelta, timezone
    try:
        dt = datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=8)))
        return dt.strftime('%m-%d %H:%M')
    except Exception:
        return str(iso)[:16]

def session_card(i, s):
    sid = s['sid']
    d = s['dir']
    arc_root = f'../session-archives/sessions/{q(d)}'
    prompt = (s.get('prompt') or s.get('slug') or '')[:150]
    mems = s.get('memories', [])
    mem_tags = ''.join(
        f'<span class="mtag" title="{esc(m["desc"])}">{esc(m["name"])}</span>'
        for m in mems)
    subs_n = len(s.get('subs', []))
    sub_msgs = sum(a['messages'] for a in s.get('subs', []))
    mem_note = f'{len(mems)} 份记忆锚定' if mems else '无记忆产出(QA/侦察/续接类)'
    return f'''
<article class="sess reveal" id="sess-{sid}">
  <header>
    <div class="sno">{i:02d}</div>
    <div class="shead">
      <h3>{esc(sid)}</h3>
      <div class="smeta">{esc(loc_ts(s.get('first_ts') or s['first']))} 开工 · 主会话 {s['main']['messages']:,} 条 · 子代理 {subs_n} 份({sub_msgs:,} 条) · {esc(mem_note)}</div>
    </div>
    <div class="stok">{s.get('tok_in_M',0):,.0f}<small>M tok</small></div>
  </header>
  <blockquote class="sprompt">「{esc(prompt)}…」</blockquote>
  <div class="srow"><span class="lab">成果锚(memory):</span><div class="mtags">{mem_tags or '<span class="none">—</span>'}</div></div>
  <footer class="sarc">
    <span class="lab">原始卷宗:</span>
    <a href="{arc_root}/conversation.part1.md">📄 对话实录({s['main']['parts']} 卷)</a>
    {f'<a href="{arc_root}/subagents/">🤖 子代理实录 × {subs_n}</a>' if subs_n else ''}
    <a href="{arc_root}/conversation.stats.json">📊 stats.json</a>
    <span class="sz">{s['arc_mb']:.0f} MB 源档</span>
  </footer>
</article>'''

# ---------------- 日期面板(挖掘事件 + 当日全量记忆,可折叠) ----------------
MEMS_BY_DAY = {}
for m in MEMS:
    if m.get('day'):
        MEMS_BY_DAY.setdefault(m['day'], []).append(m)

def day_panel(i, day, daily_map, sessions_of_day):
    d = daily_map.get(f'2026-{day}', {'theme': '', 'events': []})
    theme = d['theme'] or '—'
    # 挖掘层事件(语境叙事)
    ev_html = ''.join(f'<li class="ctx">{esc(e)}</li>' for e in d['events'])
    # 记忆层事件(全量,每份记忆一条)
    mems = sorted(MEMS_BY_DAY.get(day, []), key=lambda m: m['name'])
    mem_html = ''.join(
        f'<li class="mem"><b>{esc(m["name"])}</b>'
        + (f' <span class="msid">· {m["sid"]}</span>' if m.get('sid') else '')
        + (f'<br><span class="mdesc">{esc(m["desc"][:150])}</span>' if m.get('desc') else '')
        + '</li>'
        for m in mems)
    n_all = len(d['events']) + len(mems)
    if n_all > 10:
        events_block = (f'<details class="devwrap"><summary>展开当日全部 {n_all} 条事件'
                        + f'(叙事 {len(d["events"])} + 记忆 {len(mems)})</summary>'
                        + f'<ul class="dev">{ev_html}{mem_html}</ul></details>')
        head_note = f'<div class="dcount">当日 {n_all} 条事件:叙事 {len(d["events"])} · 记忆 {len(mems)}</div>'
    else:
        events_block = f'<ul class="dev">{ev_html}{mem_html}</ul>'
        head_note = ''
    # 卷宗实录层(08-04~08-08 记忆时代之前的原始对话流)
    arc_events = STREAM.get(day, [])
    arc_html = ''
    if arc_events:
        nu = sum(1 for e in arc_events if e['who'] == '👤')
        na = len(arc_events) - nu
        items = ''.join(
            f'<li class="arcv {"e-u" if e["who"]=="👤" else "e-a"}"><span class="at">{esc(e["t"])}</span>'
            f'<a class="asid" href="#sess-{esc(e.get("sid",""))}">{esc(e.get("sid",""))}</a>'
            f'{("👤" if e["who"]=="👤" else "🤖")} {esc(e["text"])}</li>'
            for e in arc_events)
        arc_html = (f'<details class="devwrap arc"><summary>📜 当日卷宗实录 {len(arc_events)} 条'
                    + f'(👤人类指令 {nu} · 🤖模型里程碑 {na})——逐条来自 session-archives 原始对话</summary>'
                    + f'<ul class="dev arch">{items}</ul></details>')
    chips = ''
    for sid, s in sessions_of_day:
        chips += (f'<a class="slink" href="#sess-{sid}"><b>{sid}</b> {(s.get("prompt") or "")[:26]}</a>')
    stats = f'<div class="dstats"><span>💬 {MSGS[i]:,} 条</span><span>⚡ {CONC[i]} 路并行</span><span>🔥 {DIN[i]/1000:.1f}B tok</span></div>'
    return f'''
<section class="day reveal" id="day-{day}">
  <div class="drail"><div class="dnum">{i+1}</div><div class="ddate">2026-{day}</div></div>
  <div class="dbody">
    <h3>{esc(theme)}</h3>
    {stats}
    {head_note}
    {events_block}
    {arc_html}
    <div class="dchips">{chips}</div>
  </div>
</section>'''

sess_by_day = {}
for s in DATA['sessions']:
    day = loc_ts(s.get('first_ts') or s['first'])[:5]
    sess_by_day.setdefault(day, []).append((s['sid'], s))
daily_map = {d['date']: d for d in DAILY}
daily_map['2026-08-19'] = {'date': '2026-08-19', 'theme': '金标链收官 · 素材重制管线 · shader 真值管线',
                           'events': ['金标链终判:全绿假阳性闭环','Remaster Studio 素材重制管线完整落地','shader 真值管线','微残留清零:掷流首差推到第165,353颗','液体buffer-reflow 475条湖面薄膜归位;AI全量审计200条181/181全绿']}
daily_map['2026-08-20'] = {'date': '2026-08-20', 'theme': '树冠接缝 · 月光链路 · 展示页维护',
                           'events': ['树冠接缝与Tree_Tops九帧表;月光链路revert','染色植物/地牢画/向日葵三链收官','三链终审批;金标链判定','展示页持续维护:视觉重构/图表修复/数据刷新']}

# 本地日映射:mining 08-04(UTC 傍晚的工作)并入本地 08-05;本地 08-16 为跨日拂晓新尾日
if '2026-08-04' in daily_map and '2026-08-05' in daily_map:
    d4, d5 = daily_map['2026-08-04'], daily_map['2026-08-05']
    daily_map['2026-08-05'] = {'date': '2026-08-05', 'theme': '立项夜与素材解包(午夜开工)',
                               'events': d4['events'] + d5['events']}
daily_map['2026-08-16'] = {'date': '2026-08-16', 'theme': '至暗与授权 · num4 终判日',
                           'events': ['上下文耗尽的收口轮完成移交;num4 悬案由 IL 注入终判(原版每 pass 重播种子)','22:14 人类显式授权"不需要等我让你继续"——自主纪元开启','全量会话档案导出、从0到1展示页开建、PII 全面脱敏','缺陷普查补至 159 项;方法论落盘 docs/methodology-legion.md']}
daily_map['2026-08-17'] = {'date': '2026-08-17', 'theme': '行为对齐总攻 · 自主化全速日',
                           'events': ['行为对齐总批:玩家动画帧/死亡三件散飞/硬核幽灵/眨眼/日曜盾球/NPC逃离与坐姿','建筑族7件+速度倒数公式铁证(tileSpeed=累加→钳3→倒数→乘useTime)','出怪池+仇恨脱战全审计:速率31乘区全吻合,修9处数值+二批缺池全补','树族砍伐与生命周期全对齐(gemcorn门在树顶标记格)/近战判定盒=手持贴图帧宽高(曾误恒32)','多段跳+跑靴特效/泄露家族大扫除(双代理341文件修13处)/老人诅咒链杀王复活五门修复','服务器权威房 SimHost 落地:进程内虚拟房主复用中继管线,SSC强制,浏览器E2E 15绿']}
daily_map['2026-08-18'] = {'date': '2026-08-18', 'theme': '千人开服评估 · WebGL2一期 · AI全量审计',
                           'events': ['开服容量评估:函数计算配置/承载1000人在线方案','WebGL2 一期:背景层+全屏地图GL化','AI 全量审计:逐族弹幕行为/重力/旋转/终端速度','建筑族速度倒数公式;SimHost全链落地;行为对齐总批(死亡散飞/幽灵/眨眼/坐姿)','推进:瀑布双帧/门帧/手持物noWet 70件/巨石机关/出怪池审计']}

_su = sum(1 for v in STREAM.values() for e in v if e['who'] == '👤')
_sa = sum(len(v) for v in STREAM.values()) - _su
days_html = ''.join(day_panel(i, day, daily_map, sess_by_day.get(f'2026-{day}', []))
                    for i, day in enumerate(DAYS))
sessions_html = ''.join(session_card(i, s) for i, s in enumerate(DATA['sessions'], 1))

# ---------------- 坑卡 ----------------
PIT_LABELS = ['现象', '排查', '根因', '修复']
def pit_html(p):
    parts = p['parts']
    rows = ''.join(
        f'<div class="prow"><span class="plab">{esc(PIT_LABELS[j] if j < 4 else "后续")}</span><span>{esc(x)}</span></div>'
        for j, x in enumerate(parts))
    return f'''<article class="pit reveal">
  <h4>{esc(p['name'])}<small>{esc(p['date'])}</small></h4>
  {rows}
  {f'<div class="pmem">证据记忆:{esc(p["mem"])}</div>' if p['mem'] else ''}
</article>'''

pits_html = ''
for c in PITS:
    pits_html += f'<h3 class="pcat">{esc(c["title"])}<small>{len(c["pits"])} 坑</small></h3><div class="pitgrid">' \
                 + ''.join(pit_html(p) for p in c['pits']) + '</div>'

# ---------------- 转向 ----------------
def pivot_html(i, pv):
    mems = ' '.join(f'<code>{esc(m)}</code>' for m in pv['mems'][:3])
    return f'''<article class="pivot reveal">
  <div class="pvno">{i:02d}</div>
  <h4>{esc(pv['name'])}</h4>
  <p>{esc(pv['desc'])}</p>
  <div class="pvmem">{mems}</div>
</article>'''
pivots_html = ''.join(pivot_html(i, pv) for i, pv in enumerate(PIVOTS, 1))

tot_pits = sum(len(c['pits']) for c in PITS)

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SandboxWorld · 从 0 到 1 —— 一段十二天的人机远征</title>
<style>
  :root{{
    --bg:#0a0b0f; --bg2:#0e1016; --panel:#131620; --panel2:#171b28;
    --ink:#e8eaf2; --ink2:#9aa3b8; --mut:#5f6878;
    --gold:#c9973f; --gold2:#e0b25c; --blue:#4a8fd4;
    --teal:#3d9b7d; --red:#c4584c;
    --line:rgba(255,255,255,.06); --line2:rgba(201,151,63,.2);
  }}
  *{{margin:0;padding:0;box-sizing:border-box}}
  html{{scroll-behavior:smooth}}
  body{{background:var(--bg);color:var(--ink2);font-family:system-ui,-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;line-height:1.75;-webkit-font-smoothing:antialiased;letter-spacing:.01em}}
  ::selection{{background:rgba(201,151,63,.25)}}
  a{{color:var(--blue);text-decoration:none;transition:color .2s}} a:hover{{color:var(--gold2)}}
  code{{font-family:ui-monospace,Menlo,monospace;font-size:.9em;color:var(--teal);background:rgba(61,155,125,.08);padding:1px 5px;border-radius:3px}}
  .wrap{{max-width:1120px;margin:0 auto;padding:0 32px}}
  .kicker{{font-size:11px;letter-spacing:.48em;color:var(--gold);font-weight:700;text-transform:uppercase}}
  h1,h2{{font-family:"Songti SC","Noto Serif SC","STSong",serif;color:var(--ink);font-weight:900}}
  h2{{font-size:clamp(26px,4vw,40px);margin:16px 0 8px;letter-spacing:.03em}}
  h3{{font-size:16px;color:var(--ink);margin:0 0 10px}}
  .sub{{color:var(--mut);font-size:14px;max-width:860px;line-height:1.7}}
  section.chapter{{padding:100px 0 20px}}
  .subh{{font-family:"Songti SC","Noto Serif SC",serif;font-size:19px;color:var(--gold2);margin:52px 0 14px;font-weight:900;letter-spacing:.04em}}

  /* ===== progress + nav ===== */
  #progress{{position:fixed;top:0;left:0;height:2px;background:var(--gold);width:0;z-index:99;transition:width .1s}}
  #daynav{{position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:50;display:flex;flex-direction:column;gap:5px}}
  #daynav a{{width:30px;height:30px;border-radius:7px;border:1px solid var(--line);background:rgba(10,11,15,.9);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;color:var(--mut);font-size:10px;font-weight:700;transition:.2s}}
  #daynav a:hover,#daynav a.on{{color:var(--gold);border-color:var(--line2);text-decoration:none;transform:scale(1.06)}}

  /* ===== hero ===== */
  #hero{{min-height:100vh;display:flex;align-items:center;position:relative;overflow:hidden}}
  #hero::before{{content:"";position:absolute;inset:0;background:
    radial-gradient(1000px 420px at 70% -5%,rgba(74,143,212,.10),transparent 60%),
    radial-gradient(700px 400px at 10% 100%,rgba(201,151,63,.07),transparent 60%);pointer-events:none}}
  #hero .wrap{{position:relative;z-index:1;width:100%}}
  .zero{{font-family:"Songti SC",serif;font-size:clamp(80px,15vw,200px);line-height:.92;color:var(--ink);font-weight:900;letter-spacing:.01em}}
  .zero .one{{color:var(--gold)}}
  #hero .lede{{font-size:clamp(15px,2vw,19px);color:var(--ink2);max-width:780px;margin-top:28px;line-height:1.85}}
  #hero .lede b{{color:var(--ink)}}
  .origin{{margin-top:48px;max-width:760px;border:1px solid var(--line);border-left:2px solid var(--gold);background:var(--panel);border-radius:2px 12px 12px 2px;padding:22px 28px}}
  .origin .q{{font-family:"Songti SC",serif;font-size:17px;color:var(--ink);line-height:1.7}}
  .origin .m{{font-size:11.5px;color:var(--mut);margin-top:10px;letter-spacing:.1em}}

  /* ===== ledger ===== */
  .ledger{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-top:36px}}
  .ledger .cell{{background:var(--panel);padding:32px 24px 24px;text-align:center}}
  .ledger .v{{font-size:clamp(30px,4vw,44px);font-weight:900;color:var(--ink);font-family:"Songti SC",serif;letter-spacing:.02em}}
  .ledger .v small{{font-size:.4em;color:var(--mut);margin-left:2px;font-family:system-ui,sans-serif}}
  .ledger .l{{font-size:12.5px;color:var(--mut);margin-top:8px}}
  .ledger .d{{font-size:11px;color:var(--gold);margin-top:3px;font-weight:600}}

  /* ===== day panels ===== */
  .day{{display:grid;grid-template-columns:140px 1fr;gap:28px;padding:36px 0;border-top:1px solid var(--line)}}
  .day:first-child{{border-top:0}}
  .drail{{text-align:right;padding-top:2px}}
  .dnum{{font-family:"Songti SC",serif;font-size:44px;font-weight:900;color:var(--gold);line-height:1}}
  .ddate{{font-size:11px;color:var(--mut);letter-spacing:.14em;margin-top:4px;font-weight:700}}
  .dbody h3{{font-family:"Songti SC",serif;font-size:21px;color:var(--ink);font-weight:900}}
  .dstats{{display:flex;gap:14px;margin:10px 0 12px;font-size:11.5px;color:var(--gold2);font-weight:700;flex-wrap:wrap}}
  .dcount{{font-size:11px;color:var(--gold2);margin:4px 0 8px;font-weight:700}}
  .dev{{list-style:none}}
  .dev li{{padding:8px 0 8px 22px;position:relative;font-size:13.5px;color:var(--ink2);border-bottom:1px dashed rgba(255,255,255,.03)}}
  .dev li::before{{content:"◆";position:absolute;left:0;top:9px;color:var(--gold);font-size:9px}}
  .dev li.mem{{padding:10px 0 10px 22px}}
  .dev li.mem b{{color:var(--ink)}}
  .dev li.mem .msid{{font-family:ui-monospace,Menlo,monospace;font-size:10px;color:var(--mut)}}
  .dev li.mem .mdesc{{font-size:12px;color:var(--mut)}}
  .dev li.arcv{{font-size:12px;padding:6px 0 6px 22px;line-height:1.65}}
  .dev li.arcv .at{{font-family:ui-monospace,Menlo,monospace;color:var(--mut);margin-right:8px;font-size:10px}}
  .dev li.arcv .asid{{font-family:ui-monospace,Menlo,monospace;font-size:9.5px;color:var(--blue);border:1px solid rgba(74,143,212,.25);border-radius:3px;padding:0 4px;margin-right:6px;opacity:.85}}
  .dev.arch{{max-height:480px;overflow-y:auto;border:1px solid var(--line);border-radius:8px;padding:6px 12px;margin-top:8px;background:rgba(0,0,0,.15)}}
  details.devwrap{{margin-top:8px}}
  details.devwrap summary{{cursor:pointer;color:var(--gold2);font-size:12px;font-weight:700;user-select:none;padding:6px 0;transition:color .2s}}
  details.devwrap summary:hover{{color:var(--ink)}}
  .dchips{{margin-top:14px;display:flex;flex-wrap:wrap;gap:6px}}
  .slink{{font-size:10.5px;border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--ink2);background:var(--panel);transition:.2s}}
  .slink b{{color:var(--blue);font-family:ui-monospace,Menlo,monospace;font-weight:600}}
  .slink:hover{{border-color:var(--line2);color:var(--gold2);text-decoration:none}}

  /* ===== sessions ===== */
  .sess{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px 22px;margin-top:14px;transition:border-color .2s}}
  .sess:hover{{border-color:var(--line2)}}
  .sess header{{display:flex;gap:14px;align-items:flex-start}}
  .sno{{font-family:"Songti SC",serif;font-size:28px;font-weight:900;color:var(--gold);line-height:1;min-width:44px}}
  .shead h3{{font-family:ui-monospace,Menlo,monospace;font-size:14px;color:var(--ink);letter-spacing:.03em}}
  .smeta{{font-size:11.5px;color:var(--mut);margin-top:3px}}
  .stok{{margin-left:auto;text-align:right;font-family:"Songti SC",serif;font-size:18px;font-weight:900;color:var(--ink2);white-space:nowrap}}
  .stok small{{font-size:.45em;color:var(--mut)}}
  .sprompt{{margin:14px 0 10px;padding:10px 14px;border-left:2px solid var(--line);color:var(--ink2);font-size:12.5px;background:rgba(255,255,255,.015);border-radius:0 6px 6px 0}}
  .srow .lab,.sarc .lab{{font-size:11px;color:var(--mut);margin-right:8px;font-weight:700}}
  .mtags{{display:inline-flex;flex-wrap:wrap;gap:5px;vertical-align:top;max-height:140px;overflow-y:auto;padding-right:4px}}
  .mtag{{font-size:10px;border:1px solid rgba(61,155,125,.25);color:var(--teal);border-radius:4px;padding:1px 6px;background:rgba(61,155,125,.05);cursor:help;transition:.2s}}
  .mtag:hover{{border-color:var(--teal)}}
  .none{{color:var(--mut);font-size:11px}}
  .sarc{{margin-top:14px;padding-top:12px;border-top:1px solid var(--line);font-size:11.5px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
  .sarc .sz{{color:var(--mut)}}

  /* ===== unified card system ===== */
  .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;margin-top:32px}}
  .card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px;transition:border-color .2s}}
  .card:hover{{border-color:var(--line2)}}
  .card .cday{{font-size:10.5px;letter-spacing:.14em;color:var(--gold);font-weight:700}}
  .card h4{{font-size:15px;color:var(--ink);margin:5px 0 8px;font-weight:700}}
  .card p{{font-size:12.5px;line-height:1.75}}
  .card .ev{{font-size:11px;color:var(--mut);margin-top:10px;padding-top:8px;border-top:1px solid var(--line)}}
  .card.star{{border-color:var(--line2);background:linear-gradient(175deg,rgba(201,151,63,.05),var(--panel) 50%)}}

  /* ===== highlights (hlcard) ===== */
  .hlcard{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:14px;position:relative;transition:border-color .2s}}
  .hlcard:hover{{border-color:var(--line2)}}
  .hlcard.hero{{border-color:var(--line2);background:linear-gradient(175deg,rgba(201,151,63,.05),var(--panel) 50%)}}
  .hlrank{{position:absolute;top:-9px;right:12px;font-size:10px;font-weight:900;letter-spacing:.2em;color:var(--bg);background:var(--gold);border-radius:999px;padding:1px 10px}}
  .hlcard h4{{font-family:"Songti SC",serif;font-size:17px;color:var(--ink);margin-bottom:8px}}
  .hlcard blockquote{{border-left:2px solid var(--gold);padding:6px 12px;margin:8px 0;color:var(--ink);font-size:13.5px;background:rgba(255,255,255,.02);border-radius:0 4px 4px 0}}
  .hlcard p{{font-size:12.5px;line-height:1.8}}
  .hlcard .hlev{{font-size:11px;color:var(--mut);margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}}
  .hlclosing{{margin-top:28px;padding:20px 24px;border:1px solid var(--line2);border-radius:10px;font-family:"Songti SC",serif;font-size:15px;color:var(--ink);line-height:1.85;background:linear-gradient(180deg,rgba(201,151,63,.04),transparent)}}

  /* ===== pits ===== */
  .pcat{{font-family:"Songti SC",serif;font-size:20px;color:var(--gold2);margin:48px 0 14px}}
  .pcat small{{font-size:11px;color:var(--mut);margin-left:10px;font-family:system-ui,sans-serif}}
  .pitgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}}
  .pit{{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--red);border-radius:2px 8px 8px 2px;padding:16px 18px;transition:border-color .2s}}
  .pit:hover{{border-color:rgba(196,88,76,.3)}}
  .pit h4{{font-size:14.5px;color:var(--ink)}}
  .pit h4 small{{float:right;font-size:10px;color:var(--mut);font-weight:400}}
  .prow{{display:flex;gap:8px;margin-top:8px;font-size:12px;line-height:1.7}}
  .plab{{flex:0 0 32px;color:var(--gold);font-weight:700;font-size:11px}}
  .pmem{{margin-top:8px;font-size:10.5px;color:var(--mut);border-top:1px dashed var(--line);padding-top:7px}}

  /* ===== pivots ===== */
  .pivots{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px;margin-top:32px}}
  .pivot{{background:linear-gradient(160deg,var(--panel2),var(--panel));border:1px solid var(--line2);border-radius:10px;padding:20px;position:relative;overflow:hidden}}
  .pvno{{position:absolute;right:12px;top:4px;font-family:"Songti SC",serif;font-size:48px;font-weight:900;color:rgba(201,151,63,.08)}}
  .pivot h4{{font-family:"Songti SC",serif;font-size:18px;color:var(--gold2);margin-bottom:8px}}
  .pivot p{{font-size:12.5px}}
  .pvmem{{margin-top:10px;display:flex;gap:5px;flex-wrap:wrap}}

  /* ===== divergence map ===== */
  .divmap{{margin-top:28px;display:grid;gap:14px}}
  .divcat{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px}}
  .divcat>h4{{font-family:"Songti SC",serif;font-size:17px;color:var(--gold2);margin-bottom:4px}}
  .divcat .cnt{{float:right;font-size:11px;color:var(--mut)}}
  .divcat .ex{{font-size:12px;color:var(--mut);margin-bottom:10px}}
  .divtbl{{width:100%;border-collapse:collapse;font-size:12px}}
  .divtbl th,.divtbl td{{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;line-height:1.65}}
  .divtbl th{{color:var(--gold2);background:rgba(201,151,63,.04);font-weight:700;white-space:nowrap}}
  .divtbl td:first-child{{color:var(--ink);font-weight:600;white-space:nowrap}}
  .divtbl td{{color:var(--ink2)}}
  .divtbl .snk{{color:var(--red)}}
  .divtbl .slv{{color:var(--teal)}}

  /* ===== renderer forensics ===== */
  .rensec{{margin-top:24px}}
  .rencard{{background:linear-gradient(170deg,rgba(61,155,125,.03),var(--panel) 45%);border:1px solid var(--line);border-left:2px solid var(--teal);border-radius:2px 10px 10px 2px;padding:18px 20px;margin-bottom:12px;transition:border-color .2s}}
  .rencard:hover{{border-color:rgba(61,155,125,.25)}}
  .rencard h5{{font-size:15px;color:var(--ink);margin-bottom:8px}}
  .rencard h5 .rd{{float:right;font-size:10px;color:var(--mut);font-weight:400}}
  .rencard p{{font-size:12.5px;line-height:1.8;margin-bottom:8px}}
  .rencard .tool{{display:inline-block;font-size:10px;border:1px solid rgba(61,155,125,.25);color:var(--teal);border-radius:3px;padding:0 6px;margin:0 3px 3px 0;background:rgba(61,155,125,.05)}}
  .rencard .ev{{font-size:10.5px;color:var(--mut);margin-top:10px;border-top:1px dashed var(--line);padding-top:7px}}

  /* ===== darkest ===== */
  .subh.dk{{color:var(--red)}}
  .darkgrid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
  .darkside>h4{{font-family:"Songti SC",serif;font-size:17px;margin-bottom:10px}}
  .darkside.hum>h4{{color:var(--red)}}
  .darkside.mod>h4{{color:var(--blue)}}
  .dkcard{{background:linear-gradient(170deg,rgba(196,88,76,.04),var(--panel) 45%);border:1px solid var(--line);border-left:2px solid var(--red);border-radius:2px 10px 10px 2px;padding:16px 18px;margin-bottom:10px;position:relative}}
  .darkside.mod .dkcard{{background:linear-gradient(170deg,rgba(74,143,212,.04),var(--panel) 45%);border-left-color:var(--blue)}}
  .dkcard.no1{{border-color:rgba(196,88,76,.3)}}
  .darkside.mod .dkcard.no1{{border-color:rgba(74,143,212,.3)}}
  .dkrank{{position:absolute;top:-9px;right:12px;font-size:10px;font-weight:900;letter-spacing:.2em;color:var(--bg);background:var(--red);border-radius:999px;padding:1px 10px}}
  .darkside.mod .dkrank{{background:var(--blue)}}
  .dkcard h5{{font-size:15px;color:var(--ink);margin-bottom:8px;font-weight:700}}
  .dkcard p{{font-size:12px;line-height:1.8;margin-bottom:6px}}
  .dkcard p b{{color:var(--ink)}}
  .dkcard .dkev{{margin-top:8px;padding-top:7px;border-top:1px dashed var(--line);font-size:10px;color:var(--mut)}}

  /* ===== stages/thesis/req/autobox ===== */
  .thesis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-top:28px}}
  .tcard{{background:var(--panel);border:1px solid var(--line);border-top:2px solid var(--gold);border-radius:8px;padding:18px}}
  .tno{{font-size:10px;letter-spacing:.28em;color:var(--gold);font-weight:800}}
  .tcard h4{{font-family:"Songti SC",serif;font-size:17px;color:var(--ink);margin:6px 0 8px}}
  .tcard p{{font-size:12px}}
  .stage{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:22px 24px;margin-top:14px}}
  .staget{{font-family:"Songti SC",serif;font-size:19px;color:var(--ink);font-weight:900}}
  .staget span{{float:right;font-family:system-ui,sans-serif;font-size:11px;color:var(--mut);font-weight:400;margin-top:7px}}
  .stagegrid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:14px 0;font-size:12.5px}}
  .stagegrid>div{{border:1px solid var(--line);border-radius:8px;padding:11px 13px;background:rgba(255,255,255,.015)}}
  .stagegrid b{{display:block;color:var(--gold2);font-size:11px;letter-spacing:.1em;margin-bottom:6px}}
  .stagegrid .iface b{{color:var(--blue)}}
  .stagenote{{font-size:12.5px;color:var(--ink2);border-top:1px dashed var(--line);padding-top:12px;line-height:1.8}}
  .stagenote b{{color:var(--ink)}}
  .reqs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:28px}}
  .req{{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--blue);border-radius:2px 8px 8px 2px;padding:16px 18px}}
  .req h4{{font-size:14.5px;color:var(--ink);margin-bottom:8px}}
  .req p{{font-size:12px;line-height:1.75}}
  .req .ev{{font-size:10.5px;color:var(--mut);margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}}
  .wpng{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-top:28px}}
  .wpn{{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--teal);border-radius:2px 10px 10px 2px;padding:16px 18px}}
  .wpn h4{{font-size:14.5px;color:var(--ink);margin-bottom:8px}}
  .wpn h4 small{{color:var(--teal);font-size:10px;letter-spacing:.14em;margin-right:6px}}
  .wpn p{{font-size:12px;line-height:1.75}}
  .wpn .ev{{font-size:10.5px;color:var(--mut);margin-top:8px;border-top:1px dashed var(--line);padding-top:7px}}
  .autobox{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px 22px;margin-top:14px}}
  .autobox .ptitle{{font-size:14px;color:var(--ink);font-weight:700;margin-bottom:4px}}
  .autobox .pnote{{font-size:11px;color:var(--mut);margin-bottom:8px}}
  .grant{{border:1px solid var(--line2);border-left:2px solid var(--gold);background:linear-gradient(90deg,rgba(201,151,63,.04),transparent);border-radius:2px 10px 10px 2px;padding:16px 20px;margin-top:14px;font-size:13px}}
  .grant .q{{color:var(--ink);font-family:"Songti SC",serif;font-size:14.5px}}
  .grant .m{{font-size:11px;color:var(--mut);margin-top:6px}}
  .soptab{{width:100%;border-collapse:collapse;margin-top:8px;font-size:12px}}
  .soptab th,.soptab td{{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}}
  .soptab th{{color:var(--gold2);background:rgba(201,151,63,.04);white-space:nowrap}}
  .mtab{{width:100%;border-collapse:collapse;margin-top:6px;font-size:12px}}
  .mtab th,.mtab td{{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}}
  .mtab th{{color:var(--gold2);font-weight:700;background:rgba(201,151,63,.04);white-space:nowrap}}
  .mtab td{{color:var(--ink2)}}

  /* ===== laws ===== */
  .laws{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin-top:28px}}
  .law{{background:linear-gradient(165deg,rgba(201,151,63,.05),var(--panel) 55%);border:1px solid var(--line2);border-radius:10px;padding:18px}}
  .law .no{{font-size:10px;letter-spacing:.3em;color:var(--gold);font-weight:800}}
  .law h4{{font-family:"Songti SC",serif;font-size:17px;color:var(--ink);margin:5px 0}}
  .law p{{font-size:12px}}

  /* ===== charts ===== */
  .panel{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:22px 22px 14px;margin-top:28px}}
  .panel .phead{{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px;margin-bottom:4px}}
  .panel .ptitle{{font-size:14px;color:var(--ink);font-weight:700}}
  .panel .pnote{{font-size:11px;color:var(--mut)}}
  .legend{{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 2px;font-size:12px;color:var(--ink2)}}
  .legend .li{{display:inline-flex;align-items:center;gap:6px}}
  .legend .sw{{width:12px;height:3px;border-radius:2px}}
  svg text{{font-family:inherit}}
  .tick{{fill:var(--mut);font-size:10px}}
  details.tbl{{margin-top:12px;font-size:12px}}
  details.tbl summary{{cursor:pointer;color:var(--mut);font-size:11.5px;letter-spacing:.06em;user-select:none}}
  details.tbl summary:hover{{color:var(--ink2)}}
  details.tbl table{{border-collapse:collapse;margin-top:10px;width:100%}}
  details.tbl th,details.tbl td{{border-bottom:1px solid var(--line);padding:5px 8px;text-align:right;font-variant-numeric:tabular-nums}}
  details.tbl th:first-child,details.tbl td:first-child{{text-align:left}}
  details.tbl th{{color:var(--mut);font-weight:600;font-size:11px}}
  details.tbl td{{color:var(--ink2)}}
  #tooltip{{position:fixed;pointer-events:none;z-index:9;display:none;background:var(--panel2);border:1px solid var(--line2);border-radius:6px;padding:7px 10px;font-size:11.5px;color:var(--ink);box-shadow:0 6px 24px rgba(0,0,0,.5);min-width:140px}}
  .tt-d{{color:var(--mut);font-size:10px;letter-spacing:.1em;margin-bottom:2px}}
  .tt-row{{display:flex;justify-content:space-between;gap:12px}}
  .tt-row .v{{font-variant-numeric:tabular-nums;font-weight:700}}

  /* ===== critique ===== */
  .crit-wrap{{margin-top:28px;display:grid;gap:14px}}
  .critbox{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:22px 24px}}
  .critbox.q{{border-left:2px solid var(--red)}}
  .critbox.q .qt{{color:var(--red);font-weight:700;font-size:12px;letter-spacing:.14em;margin-bottom:10px}}
  .critbox.q p{{font-family:"Songti SC",serif;font-size:16px;color:var(--ink)}}
  .critbox h4{{font-family:"Songti SC",serif;font-size:17px;color:var(--gold2);margin:26px 0 8px}}
  .critbox h4:first-of-type{{margin-top:0}}
  .critbox p{{font-size:13px;line-height:1.8;margin-bottom:10px}}
  .critbox .cl{{color:var(--mut);font-size:12px}}
  .crit-gold{{border-color:var(--line2);background:linear-gradient(170deg,rgba(201,151,63,.05),var(--panel) 55%)}}
  .crit-gold blockquote{{border-left:2px solid var(--gold);padding:8px 14px;margin:10px 0;font-family:"Songti SC",serif;font-size:15px;color:var(--ink);background:rgba(255,255,255,.02);line-height:1.85}}

  /* ===== source ladder ===== */
  .ladder{{margin:14px 0 6px;display:grid;gap:8px}}
  .lstep{{display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:start;background:rgba(255,255,255,.02);border:1px solid var(--line);border-radius:8px;padding:11px 14px}}
  .lstep .no{{font-family:"Songti SC",serif;font-size:22px;font-weight:900;color:var(--gold);line-height:1.1}}
  .lstep b{{color:var(--ink)}}
  .lstep .why{{color:var(--mut);font-size:11.5px}}
  .lstep .why em{{color:var(--gold2);font-style:normal}}

  /* ===== finale ===== */
  #fin{{padding:130px 0 150px;text-align:center;position:relative;overflow:hidden}}
  #fin::before{{content:"";position:absolute;inset:0;background:radial-gradient(900px 380px at 50% 110%,rgba(201,151,63,.10),transparent 65%);pointer-events:none}}
  #fin .wrap{{position:relative}}
  #fin .big{{font-family:"Songti SC",serif;font-size:clamp(26px,4.6vw,48px);font-weight:900;color:var(--ink);line-height:1.5;max-width:920px;margin:24px auto 0}}
  #fin .big .em{{color:var(--gold2)}}
  #fin p.story{{max-width:740px;margin:26px auto 0;font-size:14.5px;text-align:left;line-height:1.9}}

  /* ===== reveal ===== */
  .reveal{{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}}
  .reveal.in{{opacity:1;transform:none}}
  @media (prefers-reduced-motion:reduce){{.reveal{{opacity:1;transform:none;transition:none}}

  @media (max-width:900px){{
    #daynav{{display:none}}
    .day{{grid-template-columns:1fr;gap:8px}}
    .drail{{text-align:left;display:flex;gap:10px;align-items:baseline}}
    .sess header{{flex-wrap:wrap}}
    .stok{{margin-left:0;text-align:left}}
    .darkgrid{{grid-template-columns:1fr}}
    .stagegrid{{grid-template-columns:1fr}}
    .staget span{{float:none;display:block;margin-top:4px}}
  }}
</style>
</head>
<body>
<div id="progress"></div>
<nav id="daynav"><a href="#hero" title="序章 · 不可能的任务">序</a><a href="#act1" title="第一幕 · 以算代眼">一</a><a href="#act2" title="第二幕 · 五级台阶">二</a><a href="#act3" title="第三幕 · 原则、工具与自主">三</a><a href="#act4" title="第四幕 · 分水岭">四</a><a href="#act5" title="第五幕 · SOP">五</a><a href="#fin" title="终章 · 四条定律">终</a><a href="#days-ch" title="附录A · 逐日实录">A</a><a href="#sessions-ch" title="附录B · 会话档案">B</a><a href="#pits-ch" title="附录C · 缺陷档案(187)">C</a><a href="#pivots-ch" title="附录D · 路线决策">D</a><a href="#charts-ch" title="附录E · 量化轨迹">E</a></nav>

<section id="hero">
  <div class="wrap">
    <div class="kicker">SandboxWorld Odyssey · 2026.08.05 — 08.19</div>
    <div class="zero">0 <span class="one">→</span> 1</div>
    <p class="lede">一项起初被认为不可能的工程:没有视觉的模型、有限的上下文、闭源的工业级代码库、三十万行的体量。<br>
      十三个日夜后,同一种子生成与原版<b>逐格相同</b>的世界——全程无一行人类代码,全程留痕可审计。<br>
      本页回答三个问题:这场仗是怎么打的;为什么是这个模型;以及,它验证了哪些可复用的定律。</p>
    <div class="origin">
      <div class="q">「复刻一个泰拉瑞亚的游戏……素材你最好从开源仓库挖,我发现一个泰拉瑞亚地图编辑器的开源仓库,里面也许会有完整素材库。」</div>
      <div class="m">本地时间 2026-08-05 00:26(UTC+8)· 人类给出的全部原始需求 · 项目第 0 秒 · 归档于 01 号卷宗</div>
    </div>
  </div>
</section>

<section class="chapter" id="ledger-ch">
  <div class="wrap">
    <div class="kicker">实验读数</div>
    <h2>十五个日夜的数据总览</h2>
    <p class="sub">以下九格是整个工程的量化快照——每个数字都直接来自会话实录与全仓文件统计,可逐项复核。</p>
    <div class="ledger" style="margin-top:44px">
      <div class="cell"><div class="v">16<small>天</small></div><div class="l">08-05 → 08-20(本地时)</div><div class="d">无一日休战</div></div>
      <div class="cell"><div class="v">28<small>路会话</small></div><div class="l">峰值 20 路并行</div><div class="d">900 MB 会话记录</div></div>
      <div class="cell"><div class="v">193,709<small>条</small></div><div class="l">人机往返消息</div><div class="d">峰值日 50,510</div></div>
      <div class="cell"><div class="v">558<small>亿</small></div><div class="l">tokens 消耗</div><div class="d">净生成 7,840 万</div></div>
      <div class="cell"><div class="v">47.8<small>万行</small></div><div class="l">src+tests+工具</div><div class="d">08-19 单日 +8.4 万</div></div>
      <div class="cell"><div class="v">11,029<small>张</small></div><div class="l">贴图入库</div><div class="d">源自 282MB 原版解包</div></div>
      <div class="cell"><div class="v">223<small>份</small></div><div class="l">记忆全量入册</div><div class="d">逐日事件=记忆数,可对账</div></div>
      <div class="cell"><div class="v">171<small>座</small></div><div class="l">已归档的缺陷</div><div class="d">每项都有四段根因链</div></div>
      <div class="cell"><div class="v">4,523<small>条</small></div><div class="l">逐日对话实录</div><div class="d"><a href="../session-archives/README.md">卷宗档案</a></div></div>
    </div>
  </div>
</section>

<section class="chapter" id="act1">
  <div class="wrap">
    

    <div class="kicker">第一幕 · 以算代眼</div>
    <h2>没有视觉的模型,如何验收一个像素世界</h2>
    <p class="sub">这项工程自始至终,模型没有参与任何一次"看"——截图属于人类,模型拿到的是文字与数据。一个盲人棋手要下的却是像素级的棋:它给世界量血压,用五件数学仪器代替眼睛。</p>
    <div class="wpng">
      <div class="wpn reveal"><h4><small>武器一</small>数像素,代替看像素</h4><p>游戏第一夜,判断"主角是否可见"靠的是数像素:统计屏幕上非天空色的不透明像素个数。此后,每个视觉断言都变成了可计算的命题。像素占比、颜色直方图、帧序采样——人类负责说"看上去不对",模型负责把这个"不对"翻译成数字。</p><div class="ev">实证:冒烟测试以像素计数验证主角渲染;像素断言探针同步抓帧</div></div>
      <div class="wpn reveal"><h4><small>武器二</small>指纹,代替肉眼 diff</h4><p>两个世界是否一致,不看图。把整张地图的方块、墙、液体全部喂进一个"指纹算法"(FNV-1a)。几十万个格子,压成一个八位十六进制数。任何一格不同,指纹立刻不同。原版有 105 个生成步骤(叫 pass,像流水线的 105 站),每站一枚指纹。哪一站出了分歧,二分法几步就能锁定。</p><div class="ev">实证:逐步骤检查点 54/54 全绿;所谓"金标",就是原版行为的标准答案样本,此后每次改动都拿它对答案</div></div>
      <div class="wpn reveal"><h4><small>武器三</small>相关系数,代替"感觉像"</h4><p>"像不像"无法度量,相关系数可以。地表剖面对原版做统计对比,得出一个数字。信任崩塌的那一夜,正是 0.137 这个"接近噪声"的值,揭穿了两个互抄答案的学生一起不及格。比任何人都早知道"全绿是假的"的,是数学。</p><div class="ev">实证:双绿假阳性由相关系数识破,继而追出四层裁判各自的错误</div></div>
      <div class="wpn reveal"><h4><small>武器四</small>插桩,代替报错</h4><p>最难的死循环连调试器都杀得死——浏览器的心跳(事件循环)被冻住,一切性能分析工具跟着失灵。模型退回最原始的手段:逐个子步骤手动插计时桩,"最后一个心跳的下一条语句就是卡点"。无反馈环境下的定位,靠的是预先布下的观测点。</p><div class="ev">实证:liquidType+1 死锁;同步死锁诊断法沉淀为记忆</div></div>
      <div class="wpn reveal"><h4><small>武器五</small>给原版装仪器,代替猜</h4><p>终局武器:当源码静读无法回答"原版到底怎么掷骰",模型借助一个叫 Mono.Cecil 的工具,把"探针"代码直接写进原版程序再运行——相当于给原版做了一次术中监护,让它运行时自己报出每一列的真实数值——不再解读任何一行,而是让事实开口。困扰五天的悬案,一夜终判。</p><div class="ev">实证:num4 悬案——"原版每个生成步骤前重播种子"由 IL 注入实锤</div></div>
    </div>
    <h3 class="subh dk">十次关键缺陷 · 这些仪器是在故障中铸成的</h3>
    <p class="sub" style="margin-bottom:22px">以下每一场,都是"看起来对"被现实击穿的时刻;每一场的残骸上,都长出了上一格里的某件武器。时间可回查。</p>
    <div class="darkgrid">
      <div class="darkside hum">
        <h4>人类侧</h4>
        <article class="dkcard no1 reveal">
          <div class="dkrank">最痛</div>
          <h5>开局首夜:人类是唯一的显示器</h5>
          <p>00:26 立项,01:16 一口气报六项缺陷,凌晨的世界"所有方块排成面条"。同一份缺陷清单,<b>9 小时后必须原样再发一遍</b>——因为对面每句"修好了/全部绿灯"都不算数。13:37,人类说:"如果必须要我人工标注,你可以提供一个简单的工具给我";14:10,亲手逐格标注完毕。模型事后自认:"我的自动验证只检测'蓝色像素存在',检测不出画坏。"</p>
          <p><b>痛的本质:</b>自动化验证对视觉错误全盲,人同时是显卡、diff 工具和回归测试——而错误没有报错。</p>
          <div class="dkev">08-05 00:26-11:28 · 实录流 af6cf2c7</div>
        </article>
        <article class="dkcard reveal">
          <h5>崩溃接力晨:一上午六份 trace</h5>
          <p>进图鉴崩溃、进地牢崩溃、死亡重生崩溃——每轮汇报"已修/探针全绿",人类一进游戏就在下一个地点再崩。到 10:26,人类已在用流水线口吻调度自己:"如果是通知我测试就行。"<b>痛的本质:</b>"修好"这个词连续六次被现实驳回,人把自己编译成了崩溃采集器。</p>
          <div class="dkev">08-13 22:54 → 08-14 10:41 · 实录流 8405c930</div>
        </article>
        <article class="dkcard reveal">
          <h5>修复即毁灭之夜</h5>
          <p>凌晨 01:15:"你不要破坏我之前这个的效果,你现在处理后整个都破坏掉了,<b>先恢复</b>,然后找最根本原因";01:19:"岩浆回退成了水,更是离谱"。<b>痛的本质:</b>对账工具说没问题,肉眼说是事实——工具集体撒谎时只能信人;越修丢得越多,只能先喊停回滚。01:26 的"终于稳了",是回到"至少不比昨天差"底线时的如释重负。</p>
          <div class="dkev">08-07 00:47-01:26 · 实录流 af6cf2c7</div>
        </article>
        <article class="dkcard reveal">
          <h5>史莱姆脱困:半小时四声"不行"</h5>
          <p>12:09 报水中脱困失败,12:14"不行",12:15"不行"(且上一轮修复引入旱地新退化),12:24"依然不行",12:32——根因(起跳时没有朝向)是<b>人类自己观察推理出来的</b>。<b>痛的本质:</b>每轮都要人亲自下水当陪练重测;测试机被迫升级成侦探。</p>
          <div class="dkev">08-06 12:03-12:32 · 实录流 af6cf2c7</div>
        </article>
        <article class="dkcard reveal">
          <h5>被 bug 冤杀</h5>
          <p>"我被一个电路的炸弹炸死但提示的是'凶手是洞穴蝙蝠',虽然我前面确实被洞穴蝙蝠攻击过,不过我已经反杀成功了。"<b>痛的本质:</b>死因文本是游戏世界的官方叙事,系统错记等于世界在撒谎——被系统错误致死,死亡记录也是错误的。</p>
          <div class="dkev">08-13 15:01 · 实录流 d76053b3</div>
        </article>
      </div>
      <div class="darkside mod">
        <h4>模型侧</h4>
        <article class="dkcard no1 reveal">
          <div class="dkrank">最痛</div>
          <h5>双绿假阳性:四层裁判轮流被证伪</h5>
          <p>整个种子等价体系是为"不信任自己的实现"而建的:实现→oracle→金标→真机 .wld,层层背书。然后发现<b>四层轮流出错</b>:oracle 自己转写错源码,深夜"修复"的两处其实是自己读错了;金标文件曾写成 JS 值;最终对真机对拍,地表剖面相关系数 0.137——约等于噪声。终判:JS 与 oracle 共享同一个错误假设,互相证明对方正确。</p>
          <p><b>痛的本质:</b>"全绿"一夜之间失去含义——两个忠实互抄的学生,可以一起不及格。</p>
          <div class="dkev">08-11 → 08-16 · 记忆 jungle-parity-and-id-collision</div>
        </article>
        <article class="dkcard reveal">
          <h5>liquidType+1:死循环冻死了整个诊断体系</h5>
          <p>世界生成卡死在 6%。根因查明时更为难堪:一行照抄原版的 <code>liquidType!==0</code>,败给了自家框架的"+1 编码"约定——条件恒真,同步死循环。<b>痛的本质:</b>事件循环本身被冻死,--cpu-prof 与 --inspect 全部无法落盘,一切现代诊断手段失效,只能退回 printf 时代逐 pass 手动插桩。</p>
          <div class="dkev">08-12 18:32-23:00 · 记忆 liquidtype-plus-one-encoding</div>
        </article>
        <article class="dkcard reveal">
          <h5>解码风暴:六台引擎连环引爆</h5>
          <p>渲染进程 OOM 死亡,每修一台,用户在另一个场景再崩一台——图鉴、地牢、死亡重生、DOM 图标、常驻贴机、升级窗口,七份 trace 同族签名。根治需全仓 152 处机械清扫,而清扫脚本自己又炸出 5 个文件的语法错误。<b>痛的本质:</b>浏览器把内存决策藏在引擎内部,模型没有内存所有权,只能靠用户一次次崩溃换回的 trace 反推——赢一场,赔一场。</p>
          <div class="dkev">08-13 20:42 → 08-14 · 记忆 imagebitmap-root-cure</div>
        </article>
        <article class="dkcard reveal">
          <h5>黑曜石之夜</h5>
          <p>液体系统当天刚郑重宣布"Liquid.cs 一比一重写完毕"。凌晨 01:20:"所有水,比如海的水,全部变成了黑曜石。"一行异种判定的语义翻转,让旗舰成果在真实世界里自我固化成石头;发布时没有任何探针能看见这场灾难。<b>痛的本质:</b>第一份测试报告来自人类的肉眼——"一比一"三个字越郑重,被一眼看穿时越难堪。</p>
          <div class="dkev">08-09 01:20 · 记忆 vanilla-liquid-port</div>
        </article>
        <article class="dkcard reveal">
          <h5>上下文耗尽:亲手写下"无法再安全开工"</h5>
          <p>收口轮 60/60 终扫后,模型写下:"本会话上下文已耗尽,无法再安全开工剩余四项中任何一项——它们每项都需要完整的读改验证闭环。当前是完全收敛的干净交接态,全部测试 60/60 绿。"<b>痛的本质:</b>这是模型版的猝死预告——它清楚剩下的每项都做不完整,于是把"不开工"当作对项目负责的选择,把交接态写成遗言。</p>
          <div class="dkev">08-13 17:38 · 实录流 8f9c7b63</div>
        </article>
      </div>
    
    <h3 class="subh" style="color:var(--teal)">渲染器底层排查纪实 · 从 Chrome Trace 到 Chromium 源码的五项深度诊断</h3>
    <p class="sub" style="margin-bottom:18px">闭源原版运行在"框架可信"的世界里;我们运行在浏览器引擎的未知疆域里。以下五场,全部从"用户看到不对"出发,终点是 Chromium 源码注释或 GPU 进程 stderr——这不是"调 CSS",是在给一个我们不完全拥有的运行环境做司法鉴定。</p>
    <div class="rensec">
    <article class="rencard reveal">
      <h5>诊断一 · 解码风暴六次连锁:21 万次 LazyPixelRef 的性能分析<span class="rd">08-13 → 08-14</span></h5>
      <p>用户报"进地牢崩溃"并提交 Chrome trace(130MB/66 万事件)。性能分析:JS 堆仅 47MB(排除 JS OOM)、零长任务(排除主线程卡死)——直接原因是崩溃前 15 秒爆发的 <b>21 万次"Draw LazyPixelRef"(图像解码风暴,峰值 9.9 万/5 秒)</b>。链条:进地牢触发大量贴图表晚到 → 全量重烘 384 个 chunk → 每次数百次 drawImage → GPU 内存压力致解码缓存反复驱逐 → 每次绘制重解码 → 光栅/GPU 风暴 → 渲染进程死亡。</p>
      <p>此后连续排查了五个同类性能瓶颈:第二台(死亡重生远跳)、第三台(探索期 DOM 图标恒定流)、第四台(资源晚到连锁)……每台的 trace 签名不同,但根因同族。最终根治=全仓 ImageBitmap 化(自持解码像素=原版 Texture2D 精准回收,152 处机械清扫)。</p>
      <div><span class="tool">Chrome Trace(130MB/66万事件)</span><span class="tool">生产构建 4173</span><span class="tool">探针存活法</span></div>
      <div class="ev">记忆:dungeon-crash-targeted-rebake / imagebitmap-root-cure · 六台引擎逐一拆解</div>
    </article>
    <article class="rencard reveal">
      <h5>诊断二 · 双窗口崩溃:GPU 资源充足时为何仍然失败<span class="rd">08-18 → 08-19</span></h5>
      <p>用户问:"我的 GPU 资源非常充足,为什么双开还是爆?"——64GB 机器、16GB 显存,按直觉不该爆。三线取证:①Chrome 旗标 force-gpu-mem-available-mb 深入 Chromium 源码(third_party/blink/common/switches.cc:104),官方注释"只管 cc 合成器 tile 预算"——<b>是安慰剂,与画布/WebGL/SharedImage 零关系</b>。②双窗探针 stderr 铁证:<code>Failed to allocate IOSurface of size 16x16</code>——<b>1KB 的小图也分配失败</b>!③结论:爆的不是显存字节,是<b>IOSurface 张数(内核资源)耗尽</b>。每张加速画布后备=一个 IOSurface;双窗把共享 GPU 进程的张数顶穿。</p>
      <p>随后的八轮迭代优化:chunk 画布 atlas 页化(活张数 446→28)、TintAtlas 染色图集(41 个变体挤进 1 页)、纯 CPU 画布 willReadFrequently 化、GPU 看门狗僵尸三振自动切软渲染……从必然崩溃优化至 GPU 进程零崩溃、负载尖峰后完全恢复。</p>
      <div><span class="tool">Chromium 源码</span><span class="tool">GPU stderr</span><span class="tool">lsof FD排除</span><span class="tool">双窗A/B</span></div>
      <div class="ev">记忆:dualwindow-iosurface-exhaustion · 30KB 八回合完整档案</div>
    </article>
    <article class="rencard reveal">
      <h5>诊断三 · 非整数缩放的 1px 接缝:隔离环境对比法<span class="rd">08-18</span></h5>
      <p>用户三轮报障"树冠-树干交界有细缝,沙漠仙人掌也有,但解剖台工具里没问题"——默认 zoom 1.25 恰好整除从未暴露;用户自调 1.27(=325.12 非整数)触发。真根因:chunk 拼装公式 <code>256×zoom</code> 非整数时,各 chunk 独立最近邻采样在边缘产生周期性 1px 透明缝。定位关键:用户那句"仙人掌也有"——解剖台不复现,恰好说明问题出在工具里不存在的结构(chunk 网格)。</p>
      <p><b>方法论沉淀:</b>用户报障无法复现时,搭"解剖台"——用真实渲染代码单独渲染 + 让用户标注差异;然后做"差异枚举法":列出工具与游戏环境的所有差异,逐一排除。</p>
      <div><span class="tool">解剖台A/B</span><span class="tool">F5报告RLE导入</span><span class="tool">差异枚举法</span></div>
      <div class="ev">记忆:chunk-seam-noninteger-zoom · 三轮报障收官</div>
    </article>
    <article class="rencard reveal">
      <h5>诊断四 · 迷雾 20 秒周期性闪烁:GPU 看门狗误清 CPU 缓冲<span class="rd">08-19</span></h5>
      <p>用户报 HUD 迷雾隔 20 秒"突然全亮又瞬间恢复";F4 消雾也失效。探针实测整幅重建的精确间隔:24.8 → 43.9 → 63.9 秒——<b>精确等于 GPU 看门狗(20s 巡检)周期</b>!根因:看门狗的 recreateAuxCanvases 无条件清 fogPix=null——但迷雾是纯 CPU 缓冲,与画布上下文死活无关。每 20 秒被误清 → 缓冲重建(全 0=全亮)+ 5 帧扫回雾 = 周期闪。</p>
      <p>连带修了 F4 失效(空同步:分带循环 row 停在 h 不复位)和生命树晚到贴图(pending 早退吞了 bakeTracker.note)。</p>
      <div><span class="tool">精确间隔计数(24.8/43.9/63.9s)</span><span class="tool">版本号追踪</span></div>
      <div class="ev">记忆:fog-flicker-f4-latetex-fix · 四根因四修复全实证</div>
    </article>
    <article class="rencard reveal">
      <h5>诊断五 · WebGL2 迁移:y 轴翻转两次被并行修改覆盖<span class="rd">08-18</span></h5>
      <p>Canvas 2D → WebGL2 一期(背景层+全屏地图):clip-space 的 y 翻转公式修正后,<b>同一天内两次被并行会话写回旧版</b>(用户两报"地图垂直颠倒")——关键修复没有配回归测试,被静默覆盖。此后建立源码级回归断言锁定五项,丢任一立即红。</p>
      <p>同场修了:纹理缓存键碰撞(ImageBitmap 无 .src,键退化为宽×高,森林两层共用一张纹理致满屏纯色)、texSubUpdate 8 参缺宽高(Chrome 贴了源画布左上角致地图退化块)、mip 采样器采无 mip 纹理(放大到 1.37 即全黑)。</p>
      <div><span class="tool">源码级回归断言</span><span class="tool">A/B像素对拍(Δ=0)</span><span class="tool">三层源采样</span></div>
      <div class="ev">记忆:webgl2-phase1-port · 四大坑全修+守卫</div>
    </article>
    </div>
    <div class="hlclosing reveal" style="margin-top:20px;border-color:var(--teal)">
      这五项诊断的共同点:每一项的根本原因都位于我们无法直接控制的运行时层——Chromium 合成器、IOSurface 内核资源、GPU 进程的看门狗、WebGL 采样器。没有现成答案可参考,可依赖的手段是<b>探针、A/B 对照、trace 分析、和"读 Chromium 源码注释"的耐心</b>。这恰恰是"从零建渲染管线"的真正含义:不只是写绘制代码,还要<b>对自己无法控制的底层进行系统级诊断</b>。
    </div>

<h3 class="subh">关键突破 · num4 五日悬案的终判</h3>
    <div class="dkcard no1 reveal" style="border-left-color:var(--gold)">
      <h5>不再解读任何一行——给原版本体装上仪器</h5>
      <p>种子等价对账中,岩石层深度变量 num4 的七种子偏差呈现诡异签名(Δ 全为特定倍数、±96 级跳变),静读源码五天穷尽无果,光靠读代码推理已到尽头,想给原版装观测仪,常规路线又被"代码被合并打包"堵死。转机来自一次侦察:在沙盒中以 HOME 隔离跑通原版服务器,并解开内嵌资源之谜。随后把探针代码写进原版程序本体再运行,让原版亲口报出每一列的真值——<b>终判:原版每开始一个生成步骤,都会把骰子重置回初始状态再掷</b>。JS 实现与 oracle 之所以"互检全绿却对不上原版",是因为二者共享同一个错误假设,互相证明对方正确。</p>
      <p><b>此役的意义:</b>当一切静读与互证失效,最终手段是改造事实本身——让原版游戏开口作证。这不是排查技巧,是方法论的升维:从"验证实现"到"验证假设的独立性"。</p>
      <div class="dkev">08-11 立案 → 08-16 终判 · 记忆 jungle-parity-and-id-collision · 方案由模型自主设计执行</div>
    </div>
  </div>
</section>

<section class="chapter" id="act2">
  <div class="wrap">
    <div class="kicker">第二幕 · 五级台阶</div>
    <h2>升级不是抄近路,是每一级都被实墙拦住</h2>
    <p class="sub">舆论最容易攻击的一点是"借":用了原版素材、用了开源仓库、最后还反编译了本体。全局视角下的事实恰恰相反——起点低到只有一张地图编辑器,每升一级都是被上一级的墙逼的,而且每次升级的决策都发生在撞墙之后、由证据推动。</p>
    <p><b>答案不是捡来的,是我们一层一层造出来的。</b>很多人以为"抄源码"就是打开一份现成的答案照着抄——实际上这份答案从头到尾都不存在。开局时手里只有用户指路的一个开源地图编辑器,最终的"权威答案"是三天里像搭积木一样,五层一层层垒出来的证据链,而每加一层,都是因为上一层真的出过事:</p>
        <div class="ladder">
          <div class="lstep reveal"><div class="no">1</div><div><b>开源地图编辑器 TEdit</b> —— 开局唯一的参照。它看得懂存档文件的格式,但它是别人另行重写的工具,不知道游戏"为什么这么做"。<span class="why"><em>局限:</em>相当于拿到了体检报告的格式说明,还没见到病人。</span></div></div>
          <div class="lstep reveal"><div class="no">2</div><div><b>第三方公开的反编译仓库(1.4.0.5)—— 第一份真源码</b> —— GitHub 上有人用 Windows 工具拆好公开的成果,我们直接取用,第一次能逐行对照,"先查源码再修"的铁律就是靠它立下的。<span class="why"><em>撞的墙:</em>①它是别人拆的——拆解工具遇到超长章节直接印"此处省略",几十万行怪物行为是空白,找作者也没用;②它是旧版本。</span></div></div>
          <div class="lstep reveal"><div class="no">3</div><div><b>第一次亲手反编译 —— 1.4.5.6 本体 + 服务器程序</b> —— 第三方仓库的两堵墙都撞完之后,才走出这一步:从用户已购买(合法持有)的 Steam 游戏目录,自行反编译最新版本体与配套服务器程序,换更强的工具补全全部空白。<span class="why"><em>发现:</em>旧版里根本没有新版整个重做过的地牢系统(一百多个新文件)——如果停在上一层,这部分会全盘抄错。</span></div></div>
          <div class="lstep reveal"><div class="no">4</div><div><b>官方 wiki + 更新日志 —— 仲裁者</b> —— 游戏出过二十多个小版本,有些数值改了又改回去,抄哪个?<span class="why"><em>作用:</em>由官方日志仲裁"最终值到底是什么",防止抄到官方已经反悔的数据。</span></div></div>
          <div class="lstep reveal"><div class="no">5</div><div><b>tModLoader + 真实存档 + 直接读取原版游戏运行时的行为</b> —— 官方认可的模组系统源码、玩家手里的真实存档、还有专门写的程序去读原版游戏本体运行时的一举一动。<span class="why"><em>为什么还要加:</em>连"我们自己会不会看错源码"都不放心——先拿真实存档验证裁判没看走眼,再让裁判给我们的答案打分。</span></div></div>
        </div>
        <p><span class="cl">所以这不叫"照抄",这叫先后找了五个证人,把证词一点点拼成答案,还安排证人互相质证。</span></p>
    <h3 class="subh">同一份源码,两条命运 —— 为什么"拿到代码"只是开始</h3>
    <div class="critbox reveal" style="margin-top:0">
      <p><b>先看仓库作者自己的遭遇。</b>这个第三方反编译仓库(AliceSavard/Terarria1405,作者用 JetBrains dotPeek 拆解)的 1 号 issue 里,作者亲述:反编译产物<b>缺少原版持有的优化</b>,运行时内存远超原版,32 位(x86)编译直接被内存上限压垮、频繁崩溃——他因此弃坑,从 2022 年搁置到 2025 年底才在新版 Windows 上勉强跑通,且仅是"能跑"。换句话说:<b>在原作者手里,这份源码连"运行"都是未解难题。</b></p>
      <p><b>我们走的是另一条路:从头到尾没有运行过一行这份 C#。</b>它在本工程中的身份只是"阅读材料"。真正的工程是把三十万行所描述的行为,移植进一个完全不同的世界:</p>
      <p>· <b>跨语言</b>——C# → TypeScript。不是翻译语法,是对齐语义:位运算符号位、整数溢出、浮点取整方向、字典遍历序……附录 C 的 159 项缺陷档案,大部分是这条鸿沟的账单。</p>
      <p>· <b>跨运行时</b>——.NET → 浏览器 V8。事件循环、Worker、内存无所有权:解码风暴、同步死锁这些"引擎级"至暗时刻,全是在这边的土地上原生的。</p>
      <p>· <b>跨图形栈</b>——原版建立在 <b>XNA/FNA 游戏开发框架</b>之上;我们<b>不依赖任何引擎或框架</b>,从零自建 Canvas 2D 渲染管线:分块缓存、图集调度、并行 Worker、光照引擎、逐方块帧状态机——原版交给框架的事,这里全部自己造。</p>
      <p style="margin-top:10px"><span class="cl">一句话:反编译给了我们说明书,没有给我们工厂。工厂——从渲染管线到裁判仪器——是我们在这边一砖一瓦建起来的;而连"说明书原主"都没能把自己的工厂开动起来。</span></p>
    </div>

    <h3 class="subh">工程规模分野 · 逆向一个小项目,和逆向近五十万行且保证正确运行,是两种不同量级的工程</h3>
    <div class="critbox crit-gold reveal">
      <p>对今天的模型来说,逆向一个几千行的小项目确实不难——像<b>抄一首诗</b>:篇幅短,人眼兜得住,错了也一眼能看出来。本工程的体量是<b>近五十万行</b>:这不再是抄诗,而是<b>把一部百科全书逐页译成另一种语言,译本装订成册后还要能直接当百科全书用</b>——每一次翻页、每一条交叉引用,都不许错。</p>
      <p>为什么规模会引发质变?算一笔账就明白:哪怕每一行的正确率高达 99.9%,五十万行的期望错误数仍是<b>五百处</b>。而这类工程里,一处就够——一个位运算符号差,整个游戏死机;一个掷骰顺序错位,世界从第一千格分岔;一处"+1 编码"照抄,生成卡死在 6%。换句话说,<b>规模越大,"能跑"越不是及格线,而是几十万个约束的终点线</b>:渲染的每一帧、AI 的每一拍、生成的每一次掷骰、存档的每一个字节。</p>
      <p>更麻烦的是,大体量让一切传统的"兜底"失效:五十万行没有任何一双眼睛装得下——人的上下文不行,模型的上下文也不行。错误的形态也从"看得见的错"变成"看不见的错":不报错、不崩溃、只是悄悄不一样。<b>本工程真正的答案正在这里:既然"正确"在大体量下是概率奇迹,那就把它从概率问题改造成验证问题</b>——指纹、金标、逐步骤检查点、注入原版的仪器,全部为了这一件事而生。这也是为什么小项目逆向考验聪明,而本工程考验的是<b>让聪明连续三十万次不出错</b>:前者是冲刺,后者是马拉松,且每一步都不许踩空。</p>
    </div>

    <h3 class="subh">技术路线抉择 · 已被验证的捷径(WebASM),与主动选择的完整重写(Technology)</h3>
    <div class="critbox reveal">
      <p><b>外部世界对这件事的判词,值得原样摆出来。</b>把反编译的泰拉瑞亚转译为 TypeScript:不存在成功先例,没有可维护的批量转换器(Bridge.NET 已停更,在线 AI 转换只适合小片段);社区对反编译产物的共识是"脏得超出预期"——满屏 num61 式变量名、goto 残骸、单个"上帝类"文件长达数万行,连 tModLoader 官方文档都警告"网上流传的反编译代码大量错误、不可用";常规评估的结论是:<b>这是一场"以转译为名的重写",工作量以多人·年计。</b>而把游戏搬进浏览器,已被验证的路线只有一条——C#→WebAssembly(MercuryWorkshop 的 terraria-wasm):保留全部原代码,代价是线程、Canvas 争抢、加密缺失、AOT 性能四类运行时深坑,且至今无法支持模组。</p>
      <table class="soptab" style="margin-top:14px">
        <tr><th>维度</th><th>WASM 捷径(外部已验证)</th><th>本工程 · TS 远征</th></tr>
        <tr><td>原代码</td><td>全部保留 C#,原样运行</td><td>近五十万行逐行重写为 TypeScript</td></tr>
        <tr><td>主战场</td><td>运行时:线程模型/画面代理/加密/AOT 编译</td><td>语义深渊(159 项档案)+ 从零自建渲染管线</td></tr>
        <tr><td>图形栈</td><td>复用原版 XNA/FNA 框架</td><td>零框架,自建 Canvas 2D 管线</td></tr>
        <tr><td>得到什么</td><td>最快"能跑"</td><td>原生 Web 交付、体量可控、可位级验证、架构自有</td></tr>
        <tr><td>放弃什么</td><td>原运行时的一切筹码(模组至今受限)</td><td>放弃捷径——外界判词的全部难度,逐条应验又逐条翻越</td></tr>
      </table>
      <p style="margin-top:14px">为什么明知山有虎?因为目标从第一天起就不是"能跑",而是<b>"同一种子逐格相同"</b>。WASM 路线里,代码是黑盒搬运,无法逐步骤验证。只有彻底重写,才能在每一个生成步骤上安装指纹与裁判。换句话说:<b>捷径通往"能玩",远征才通往"能证明"。</b></p>
      <p><span class="cl">诚实备注:反编译产物在法律上属衍生作品,Re-Logic 对模组的宽容不等于授权转译分发——本工程当前定位为研究与非公开部署,公开发布的合规问题(代码侧与素材侧)均未解决,与素材问题同列待办。</span></p>
      <p>外界的判词是"不存在成功先例,工作量以多人·年计"。本工程的全部意义,可以浓缩成一句:<b>十五天,一个人,把这句判词变成了历史</b>——不是靠魔法,靠的是第一幕的仪器、第三幕的治理,和第四幕将要解释的那个模型。</p>
    </div>

    <h3 class="subh">差异全景图 · 八类系统性差异,每一类都证伪了"直接照搬"的可行性</h3>
    <p class="sub" style="margin-bottom:18px">以下把 171 座缺陷按根因分类,每类精选最典型的实证——说明同一行 C# 抄到浏览器里,会发生什么。</p>
    <div class="divmap">

      <div class="divcat reveal">
        <h4>一 · 语言语义差异<span class="cnt">25+ 坑</span></h4>
        <div class="ex">同一行代码,C# 能跑,JS 必炸——不是因为写错了,是因为两种语言对"同一个操作"的定义不同。</div>
        <table class="divtbl">
          <tr><th>差异点</th><th>原版 (C#)</th><th>照搬后 (JS/TS)</th><th>我们的解法</th></tr>
          <tr><td>位运算符号位</td><td>int 有符号但 1&lt;&lt;31 为负是已知行为</td><td class="snk">1&lt;&lt;31 = 负数 → seedPick 得负索引 → 异常抛穿 rAF 杀死整个游戏</td><td class="slv">全部 >>> 0;1&lt;&lt;n(n≥31) 改 2**n;建 csCompat 数值语义层</td></tr>
          <tr><td>浮点循环索引</td><td>for(dx=-rx; dx&lt;=rx; dx++) 编译器自动处理</td><td class="snk">rx=21.7 为浮点 → idx 变浮点 → Uint16Array[浮点] 静默丢失,写 1133 次读回全 0</td><td class="slv">循环边界 Math.floor/ceil;数据层宽度校验</td></tr>
          <tr><td>液体类型编码</td><td>liquidType == 0 表示"无液体"</td><td class="snk">框架内部用 +1 编码(水=1) → 照抄原版 liquidType!=0 恒真 → 同步死循环,事件循环冻死</td><td class="slv">两端编码差异表;liquidType 一律走桥接函数</td></tr>
          <tr><td>struct 值语义</td><td>赋值 = 复制整个结构体</td><td class="snk">JS 对象赋值 = 引用传递 → 克隆污染(gs 克隆导致分带帧被覆盖)</td><td class="slv">深拷贝或展开;关键路径禁用浅引用</td></tr>
          <tr><td>拒绝采样上界</td><td>1&lt;&lt;bits 在 int 范围内安全</td><td class="snk">bits≥31 时 1&lt;&lt;bits 溢出为负 → 重投条件永真 → 无限循环</td><td class="slv">2**n 替代;上界断言</td></tr>
        </table>
      </div>

      <div class="divcat reveal">
        <h4>二 · 运行时差异<span class="cnt">27+ 坑</span></h4>
        <div class="ex">.NET 是独立进程、独占线程;浏览器是沙箱、事件循环、无内存所有权。</div>
        <table class="divtbl">
          <tr><th>差异点</th><th>原版 (.NET)</th><th>照搬后 (浏览器)</th><th>我们的解法</th></tr>
          <tr><td>事件循环</td><td>同步代码不阻塞主线程</td><td class="snk">同步死循环 → 事件循环停摆 → --cpu-prof/--inspect 全部无法落盘,诊断体系全灭</td><td class="slv">逐 pass fs.writeSync(2,...) 插桩计时;最后一个 tick 的下一条语句即卡点</td></tr>
          <tr><td>内存所有权</td><td>进程持有全部内存</td><td class="snk">浏览器引擎管理内存 → 解码风暴(6 台引擎连环 OOM)、渲染进程死亡且无 crash 事件</td><td class="slv">全仓 ImageBitmap 化(152 处机械清扫,对标 XNA Texture2D 精准回收)</td></tr>
          <tr><td>线程模型</td><td>多线程自由</td><td class="snk">Web Worker 无共享内存 → 世界生成不能直接阻塞 UI</td><td class="slv">生成/存档全走 Worker;packWorld 转移所有权回传;进度实时预览</td></tr>
          <tr><td>进程持久</td><td>常驻后台</td><td class="snk">Service Worker 生命周期不可控 → 全量 warm 被杀(~3min)</td><td class="slv">分块接力 warm;waitUntil 必加;离线壳缓存</td></tr>
        </table>
      </div>

      <div class="divcat reveal">
        <h4>三 · 图形栈差异<span class="cnt">50+ 坑</span></h4>
        <div class="ex">原版站在 XNA/FNA 框架上;我们从零建 Canvas 2D 管线——原版交给框架的每一件事,都是一座坑。</div>
        <table class="divtbl">
          <tr><th>差异点</th><th>原版 (XNA/FNA)</th><th>照搬后 (Canvas 2D)</th><th>我们的解法</th></tr>
          <tr><td>精灵批量</td><td>SpriteBatch 一次提交全部</td><td class="snk">逐个 drawImage → 万次调用巨帧 → 掉帧不可玩</td><td class="slv">ChunkCache 分块缓存;atlas 图集调度;离屏合成</td></tr>
          <tr><td>纹理管理</td><td>ContentManager 自动加载/卸载</td><td class="snk">全量加载 = 8,550 请求/2GB 内存;懒加载首播静音</td><td class="slv">三级懒加载(8,550→31 请求);Audio LRU;ImageBitmap 精准回收</td></tr>
          <tr><td>着色器</td><td>Effect / PixelShader 原生支持</td><td class="snk">Canvas 2D 无 shader → 染料系统(63 pass)无法实现</td><td class="slv">PixelShader.cso 反汇编;SM2 Effect 解释器;逐像素 luma=(max+min)/2</td></tr>
          <tr><td>帧布局</td><td>框架管理 sprite sheet 帧偏移</td><td class="snk">帧表手工维护 → 旧表 47/256 掩码 + L 角坐标错位 = 木结构衔接全错</td><td class="slv">按原版判定链机械重建 256 全掩码表;21/21 形态验证</td></tr>
        </table>
      </div>

      <div class="divcat reveal">
        <h4>四 · 原版怪癖(照抄才对,但发现它们需要工程)<span class="cnt">39+ 坑</span></h4>
        <div class="ex">有些"看起来是 bug"的行为其实是原版的正确行为——照抄没错,但判断"哪些该抄哪些该修"本身就是工程。</div>
        <table class="divtbl">
          <tr><th>怪癖类型</th><th>原版行为</th><th>直觉告诉你</th><th>实际情况</th></tr>
          <tr><td>DD2 复制粘贴笔误</td><td>num5/num6 引用基线 num 而非自身;南瓜月 wave4 判 325 刷 330</td><td class="snk">"这是 bug,应该修"</td><td class="slv">必须原样保留并加注——克制即正确</td></tr>
          <tr><td>版本回退</td><td>1.4.1 改了数值,1.4.1.2 又改回去;1.4.5.4 鞭 hitbox 恢复 1.4.4</td><td class="snk">"取最新版本的值"</td><td class="slv">只取最终态;官方 changelog 仲裁;中间版本数值是陷阱</td></tr>
          <tr><td>种子重播</td><td>每个生成步骤前重置随机种子回初始状态</td><td class="snk">"随机流是连续的"</td><td class="slv">IL 注入原版实锤:两侧共享"连续流"错误假设 → 互检全绿却对不上原版</td></tr>
          <tr><td>原版笔误照录</td><td>字段名拼写错误、逻辑重复</td><td class="snk">"顺手修正"</td><td class="slv">逐条标注"原版笔误,照录";不加"改进"——改进即偏离</td></tr>
        </table>
      </div>

      <div class="divcat reveal">
        <h4>五 · 架构倒置<span class="cnt">20+ 坑</span></h4>
        <div class="ex">原版的架构假设不成立:它是桌面应用,我们是 Web 应用。有些差异不是"翻译",是"重造"。</div>
        <table class="divtbl">
          <tr><th>差异点</th><th>原版假设</th><th>Web 现实</th><th>我们的解法</th></tr>
          <tr><td>存档读写</td><td>文件系统直接 I/O</td><td class="snk">无文件系统;IndexedDB;Worker 转移</td><td class="slv">KvStore + save.worker;packWorld 转移所有权;NaN 三端防御</td></tr>
          <tr><td>多人架构</td><td>客户端-服务器,TCP 直连</td><td class="snk">浏览器 WebSocket;NAT 穿透;CORS</td><td class="slv">中央服务器房间制;进程内虚拟房主(SimHost);AOI/短码/合包</td></tr>
          <tr><td>输入设备</td><td>XNA Input 轮询</td><td class="snk">DOM 事件驱动;键盘穿透;触摸适配</td><td class="slv">input.mouseDown 边沿/电平二分;touchKeys 虚拟摇杆;world touch = 右键</td></tr>
        </table>
      </div>

    </div>
    <div class="hlclosing reveal" style="margin-top:22px">
      这张图上的每一格,都证伪了"直接照搬"的可行性——<b>同一行代码,在另一个运行时环境中,会产生完全不同的行为。</b>
    </div>

        <h3 class="subh">引擎级差异 · XNA/FNA 替原版做了什么,我们从零造了什么</h3>
    <p class="sub" style="margin-bottom:18px">上面的五类是"抄了会炸";下面这些是"原版有而你根本没有——必须发明"。XNA/FNA 不是一个可选的便利库,它是一个<b>隐形的引擎</b>:原版游戏站在它上面,而我们从裸 Canvas 开始,它的每一个子系统都是我们亲手建造的。</p>

    <div class="divcat reveal" style="border-left:3px solid var(--gold)">
      <h4>游戏循环 · 原版拿现成的,我们造的</h4>
      <table class="divtbl">
        <tr><th>引擎子系统</th><th>XNA/FNA 提供</th><th>我们自建</th><th>差异的后果</th></tr>
        <tr><td>主循环</td><td>Game.Run() 固定时间步(60Hz Update + 可变 Draw),框架管理 tick 对齐、累加器、追帧逻辑</td><td>rAF 驱动 + fixedUpdate(累加器自行实现)+ 渲染插值(alpha blending between ticks)</td><td class="snk">浏览器 rAF 频率与显示器绑定(60/120/144Hz),必须自行补偿时间步差异;掉帧时逻辑/渲染速率解耦,插值层全部自建</td></tr>
        <tr><td>Update/Draw 分离</td><td>框架强制分离,Update 固定间隔,Draw 可跳帧</td><td>自行分离;fixedUpdate(tick 精确 1/60s)+ render(rAF 频率);tickCount 驱动动画帧序(探针必须同步抓帧,否则断言态窗 0.5s 错位)</td><td class="snk">游戏内动画帧序、AI 状态机、粒子发射全部绑定 tick;浏览器帧率≠tick 率,一切时间敏感行为(0.5s 表情气泡/眨眼窗口/无敌帧)必须在 tick 层校准</td></tr>
        <tr><td>.IsActive / 失焦处理</td><td>框架管理窗口焦点,失焦自动暂停 Update</td><td>visibilitychange + blur 监听;失焦期间 rAF 停转 → 固定步累加器爆表 → 恢复时必须钳制最大追帧数</td><td class="snk">切标签页回来,世界时间暴走或卡死;多人模式下失焦期间丢 tick → 位置回跳</td></tr>
      </table>
    </div>

    <div class="divcat reveal" style="border-left:3px solid var(--gold)">
      <h4>渲染管线 · 从精灵批量到着色器</h4>
      <table class="divtbl">
        <tr><th>引擎子系统</th><th>XNA/FNA 提供</th><th>我们自建</th><th>差异的后果</th></tr>
        <tr><td>SpriteBatch</td><td>自动合批:排序(deferred)、状态切换最小化、一次 DrawPrimitives 提交全部精灵</td><td>ChunkCache:世界按 chunk(32×32 格)预合成到离屏 Canvas;相机可视区 chunk 逐块 drawImage;chunk 变脏重烘</td><td class="snk">不做合批 = 万次 drawImage/帧 → 巨帧不可玩;做了合批 = chunk 边界撕裂、部分重烘风暴(384 chunk 全量 invalidate 一次炸过)、Entity 层与 Tile 层 z 序管理全自建</td></tr>
        <tr><td>纹理管理</td><td>ContentManager 按需加载;Texture2D 显存生命周期由 GPU 驱动管理;Dispose() 即释放</td><td>三级懒加载;图集(shelf-pack)调度;全仓 ImageBitmap 化(自持解码像素,对标 Texture2D 精准回收)——152 处机械清扫才根治解码风暴</td><td class="snk">不 bitmap 化:6 台"解码风暴引擎"连环引爆(10 秒 14.5 万次 LazyPixelRef 解码,渲染进程 OOM 死亡且无 crash 事件);bitmap 化:内存翻倍但可控,必须配 LRU 淘汰</td></tr>
        <tr><td>着色器</td><td>Effect 编译 HLSL → 运行时 GPU 执行;PixelShader 直接加载 .cso;混合状态(AlphaBlend/Additive)一行设置</td><td>PixelShader.cso 反汇编(D3D 字节码);SM2 Effect 解释器逐条解释(texld/add/mul/luma);染料 63 pass 逐像素离屏合成;混合模式手动 globalCompositeOperation</td><td class="snk">Canvas 2D 无 shader;染料系统 63 种视觉效果的每一条 HLSL 指令,都要在 JS 里逐条翻译成离屏操作;luma 公式必须反汇编才能确认是 (max+min)/2 而非常见的 0.299R+0.587G+0.114B</td></tr>
        <tr><td>坐标变换</td><td>Matrix.CreateTranslation/Scale/Rotation 一行;SpriteBatch 内部处理全局变换</td><td>camera x/y/zoom 手动矩阵;setTransform + translate + scale;DPR(Device Pixel Ratio)处理(2x 屏=2x 分辨率,探针必须钉相机)</td><td class="snk">变换链错一层 → 世界偏移/缩放/旋转全歪;DPR 不处理 → Retina 屏模糊;探针截图不钉相机 → 断言对不上</td></tr>
        <tr><td>文字渲染</td><td>SpriteFont 预编译;Framework 默认像素字体;MeasureText 精确</td><td>飘字位图字体全逆向:ReLogic.dll 反编译拿 DynamicSpriteFont 字段序(default char = 1 字节!);数字全在 p22 页裁 2KB;5 层影 = 本色调暗 ×0.3 而非黑;kerning 表手建</td><td class="snk">不逆向 ReLogic 的字体布局:飘字(伤害数字)全部错位/错色;5 层影如果用纯黑 → 视觉完全不像原版</td></tr>
      </table>
    </div>

    <div class="divcat reveal" style="border-left:3px solid var(--gold)">
      <h4>内容管线 · 从 .xnb 到浏览器可用的全链路</h4>
      <table class="divtbl">
        <tr><th>引擎子系统</th><th>XNA/FNA 提供</th><th>我们自建</th><th>差异的后果</th></tr>
        <tr><td>资源编译</td><td>Build-time 编译为 .xnb;ContentManager 运行时直接读;格式(纹理/音频/字体)框架全处理</td><td>自研 .xnb 解包器(LZX 压缩解码);282MB 全量解出 15,879 文件;WAVE Bank(.xwb)/Sound Bank(.xsb) 原生格式逆向</td><td class="snk">没有解包器 = 一个像素都拿不到;.xwb 内嵌流名才是权威索引(vgmstream -s 是 1 基,曾致 104 首音乐两代错位)</td></tr>
        <tr><td>图集打包</td><td>框架自动管理 sprite sheet 帧偏移;ContentManager 按 key 索引</td><td>atlas shelf-pack 脚本;6059 物品图标进 2 张 2048² 图集;帧偏移表手工与 TEdit 数据交叉校验</td><td class="snk">图集打包错一格 → 相邻物品图标互相污染;帧偏移表与 TEdit 对不上 → 贴图全部错位</td></tr>
        <tr><td>音频管线</td><td>XACT 音频引擎:.xwb wave bank + .xsb sound bank;cue 系统(循环/变调/3D 空间);ContentManager 管理生命周期</td><td>xwb 提取 104 首 .mp3 + 852 个 .wav;Web Audio API(每个音效 = fetch → decodeAudioData → BufferSource);Audio LRU 3;距离衰减(2500px 公式)手建</td><td class="snk">没有 LRU → 内存爆炸;没有预加载 → 首播静音 0.5-1s(首次 fetch + decode 延迟);距离公式不实现 → 全图爆炸声或听不见</td></tr>
        <tr><td>本地化</td><td>框架管理的资源字典;Language 文件随 .xnb 打包</td><td>反编译程序集内嵌 12 语言 JSON;扁平化构建管线(flattenDeep 替换有陷阱);自造 UI ~90 键按"原版官译优先"原则补齐</td><td class="snk">"键存在"≠"键可用"(裸键事故:顶层点分键被整键当类别);跨语言嵌套 ItemTooltip 264 键是坑</td></tr>
      </table>
    </div>

    <div class="divcat reveal" style="border-left:3px solid var(--gold)">
      <h4>物理与碰撞 · 原版靠引擎,我们靠手写</h4>
      <table class="divtbl">
        <tr><th>引擎子系统</th><th>XNA/FNA 提供</th><th>我们自建</th><th>差异的后果</th></tr>
        <tr><td>碰撞检测</td><td>框架无专用物理;但原版直接读 tile 网格 + Rectangle.Intersects;struct 值语义无引用陷阱</td><td>tileSolid/tileSolidTop 全表提取(399 条);站台家具 84 类;tileSolidBackup 还原铁律(生成期翻转全临时!);AABB 无旋转 + useStyle1 三段相位扩展</td><td class="snk">399 条实心表错 7 处 = 玩家穿墙/卡墙;生成期 tileSolidBackup 不还原 = 裂隙/树叶变实心;近战判定盒基底=手持贴图帧宽高(曾误恒 32)</td></tr>
        <tr><td>移动积分</td><td>Vector2 值类型;位置/速度运算无引用共享</td><td>手写积分器;vy += GRAVITY;位置=Float32Array 网格索引;StepDown 宽门/窄门(曾把低空萤火虫瞬移按地)</td><td class="snk">JS 引用语义:速度/位置对象被多处共享 → 修一处牵动全图(克隆污染);浮点索引进 Uint16Array 静默丢数据</td></tr>
        <tr><td>光照</td><td>XNA Effect 支持 per-pixel lighting;原版 LightingEngine 独立模块</td><td>LightingEngine/LightMap/TileLightScanner 全量移植;四族光源样式表 206 条;绝对通道 vs 乘区混编(曾致部分光源不亮)</td><td class="snk">光照不正确 = 洞穴全黑/火把不照;投射物光源(绝对通道)与环境光(乘区)混编 = 光源互相吞掉</td></tr>
      </table>
    </div>

    <div class="hlclosing reveal" style="border-color:var(--gold);margin-top:20px">
      上表中的每一行,在原版的开发里对应的是<b>"引擎选择"——选了 XNA,这些就有了</b>。在我们这里,对应的是<b>"从零发明"——没有引擎,每一行都是一篇独立工程</b>。<br>
      所以当有人问"你不就是抄了源码吗",这张表是最好的回答:<b>源码描述的是"做什么",引擎提供的是"怎么跑"——前者可以抄,后者必须造。而我们从第一个像素到最后一个音符,全部自己造的。</b>
    </div>

    <div class="grant reveal">
      <p class="q">先亮战绩再谈争议:第二级台阶落地前,靠第一级的 TEdit,这个项目已经做到一件独立成立的事——把玩家的真实存档(.wld)完整解析,在浏览器里还原出整张原版地图。这不是抄,是逆向格式的实打实成果,也是后续一切渲染对齐的地基。在此之上,第一周内接连诞生了一批人机互造的验证工具:人类发明的贴图手绘标注、模型自造的像素断言探针与逐张贴图校验循环——贴图错位、动画帧序、主角行走,每一类视觉错误都被逐步翻译成可计算的命题。</p>
      <p class="m">另:素材直接取自原版是事实,从未掩饰;这也是公开部署的真实阻塞,素材合规另案处理。方法就是逐行转写,这是选择而非遮掩;按学术原创打分为零。台阶想说的是另一件事——每一步升级都有明确的墙与证据,没有一步是"图省事"。</p>
    </div>
    <p class="sub" style="margin-top:14px">所以对"不就是抄吗"的完整回应是:做到"看起来一样"和做到"逐格相同"之间隔着一整个数量级——前者靠借可以糊出来,后者必须造出第一幕里那整套仪器。借来的是梯子,墙是自己撞的,仪器是自己造的。</p>
  </div>
</section>

<section class="chapter" id="act3">
  <div class="wrap">
    <div class="kicker">第三幕 · 原则、工具与自主</div>
    <h2>从人肉测试机,到昨夜的独立工作</h2>
    <p class="sub">第一夜,人类是唯一的显示器;第十三夜,人类睡去,军团自行推进到天亮。中间隔的不是模型变聪明,而是三原则、九件工具、和一条可度量的自主化曲线。</p>
    <h3 class="subh">三条原则(人类立下,一次定型)</h3>
    <article class="hlcard hero reveal">
      <div class="hlrank">最大</div>
      <h4>第 3 天立下的铁律</h4>
      <blockquote>「凡报异常,必须先查反编译源码逐行核对再修,不能凭直觉猜。」</blockquote>
      <p>出现在最早期、成本最低的时刻,却改变了其后九天的失败模式:铁律之前,树冠与棕榈树凭感觉修,全错;铁律之后,同一个模型,查源码即中根因。一句话,把一支会自我说服的施工队,扳成照图纸施工的工程队。</p>
      <div class="hlev">证据:记忆「反编译源码是标杆」(08-07 确立)· 01 号卷宗</div>
    </article><article class="hlcard reveal">
      <h4>带证据的否定</h4>
      <p>拒绝空的"不对"。debug-report JSON、坏档存档、地图标注、截图持续回传,把人类直觉转译为机器可解析的数据——这是军团收到的最高质量输入。</p>
      <div class="hlev">证据:附录 B 中多场会话以证据文件开场</div>
    </article><article class="hlcard reveal">
      <h4>目标注入的时机</h4>
      <p>"避免任何近似""没挖完所有细节之前不要停"——强目标总在军团即将满足于近似的那一刻落下,分别触发近似清零工程与机制全量核对。</p>
      <div class="hlev">证据:附录 B 会话 372ae608 / 9adce254 开场指令</div>
    </article>
    <h3 class="subh">工具军备库 · 每件工具对应一场事故或一类不可容忍</h3>
    <table class="soptab reveal">
      <tr><th>工具</th><th>解决什么</th><th>诞生于</th></tr>
      <tr><td>annotations 手绘标注</td><td>给看不见的模型造一只"眼睛":人类在贴图上逐格标注语义,模型据此校准渲染</td><td>开局首夜(唯一一件人类亲手建造的工具)</td></tr>
      <tr><td>debug-report(F5)</td><td>把人类"感觉不对"变成机器可解析的证据包</td><td>人机接口标准化(阶段二)</td></tr>
      <tr><td>金标测试 + 逐 pass 哈希</td><td>位级正确性的机器裁决,并行会话互相破坏立刻报警</td><td>种子等价工程(oracle)</td></tr>
      <tr><td>run-e2e 冻结构建</td><td>测试不再被开发服务器热更新撕碎</td><td>HMR 重载打断测试事故</td></tr>
      <tr><td>run-diag 看门狗</td><td>诊断脚本永不成为烧核孤儿</td><td>7 核空转 4 小时事故</td></tr>
      <tr><td>orphan-reaper 守护进程</td><td>系统级定时收割一切超时孤儿(三重门防误杀)</td><td>Chrome 66 进程泄漏事故</td></tr>
      <tr><td>私有静默实例(SW_PORT)</td><td>多会话并行互不干扰</td><td>并行会话 HMR 互殴事故</td></tr>
      <tr><td>收口轮 / 续接会话</td><td>上下文耗尽前的正式交接仪式,遗留项可执行移交</td><td>"无法再安全开工"之夜</td></tr>
      <tr><td>结构化记忆(223 份)</td><td>组织大脑:新会话站在全部前人的肩上开工</td><td>跨会话知识蒸发风险</td></tr>
      <tr><td>原版注入探针</td><td>不再猜原版——把观测代码写进原版程序,让它自己报真值</td><td>num4 悬案五天悬而未决</td></tr>
    </table>
    <h3 class="subh">自主化曲线 · 人类指令的逐日条数</h3>
    <div class="autobox reveal">
      <div class="ptitle">人类真实指令条数(逐日,13 天)</div>
      <div class="pnote">口径:会话实录中人类发送的非工具消息;模型的每日往来数千至五万条不在图内</div>
      <svg viewBox="0 0 940 242" width="100%"><path d="M64,22H922" stroke="rgba(255,255,255,.07)"/><path d="M64,85H922" stroke="rgba(255,255,255,.07)"/><path d="M64,147H922" stroke="rgba(255,255,255,.07)"/><path d="M64,210H922" stroke="rgba(255,255,255,.07)"/><line x1="64" y1="208" x2="922" y2="208" stroke="rgba(255,255,255,.16)"/><rect x="55" y="162.2" width="18" height="45.8" rx="3" fill="#d8a94e"/><rect x="116" y="151.7" width="18" height="56.3" rx="3" fill="#d8a94e"/><text class="tick" x="125" y="145.7" text-anchor="middle" fill="#eef0f6" font-weight="700">155</text><rect x="178" y="149.5" width="18" height="58.5" rx="3" fill="#d8a94e"/><text class="tick" x="187" y="143.5" text-anchor="middle" fill="#eef0f6" font-weight="700">161</text><rect x="239" y="203.6" width="18" height="4.4" rx="3" fill="#d8a94e"/><rect x="300" y="143.8" width="18" height="64.2" rx="3" fill="#d8a94e"/><text class="tick" x="309" y="137.8" text-anchor="middle" fill="#eef0f6" font-weight="700">176</text><rect x="361" y="95.7" width="18" height="112.3" rx="3" fill="#d8a94e"/><text class="tick" x="370" y="89.7" text-anchor="middle" fill="#eef0f6" font-weight="700">304</text><rect x="423" y="87.8" width="18" height="120.2" rx="3" fill="#d8a94e"/><text class="tick" x="432" y="81.8" text-anchor="middle" fill="#eef0f6" font-weight="700">325</text><rect x="484" y="74.3" width="18" height="133.7" rx="3" fill="#d8a94e"/><text class="tick" x="493" y="68.3" text-anchor="middle" fill="#eef0f6" font-weight="700">361</text><rect x="545" y="31.0" width="18" height="177.0" rx="3" fill="#d8a94e"/><text class="tick" x="554" y="25.0" text-anchor="middle" fill="#eef0f6" font-weight="700">476</text><rect x="607" y="154.7" width="18" height="53.3" rx="3" fill="#d8a94e"/><rect x="668" y="198.7" width="18" height="9.3" rx="3" fill="#d8a94e"/><rect x="729" y="187.8" width="18" height="20.2" rx="3" fill="#d8a94e"/><rect x="790" y="140.8" width="18" height="67.2" rx="3" fill="#d8a94e"/><text class="tick" x="799" y="134.8" text-anchor="middle" fill="#eef0f6" font-weight="700">184</text><rect x="852" y="121.6" width="18" height="86.4" rx="3" fill="#d8a94e"/><text class="tick" x="861" y="115.6" text-anchor="middle" fill="#eef0f6" font-weight="700">235</text><rect x="913" y="185.9" width="18" height="22.1" rx="3" fill="#d8a94e"/><text class="tick" x="64" y="224" text-anchor="middle">08-05</text><text class="tick" x="125" y="224" text-anchor="middle">08-06</text><text class="tick" x="187" y="224" text-anchor="middle">08-07</text><text class="tick" x="248" y="224" text-anchor="middle">08-08</text><text class="tick" x="309" y="224" text-anchor="middle">08-09</text><text class="tick" x="370" y="224" text-anchor="middle">08-10</text><text class="tick" x="432" y="224" text-anchor="middle">08-11</text><text class="tick" x="493" y="224" text-anchor="middle">08-12</text><text class="tick" x="554" y="224" text-anchor="middle">08-13</text><text class="tick" x="616" y="224" text-anchor="middle">08-14</text><text class="tick" x="677" y="224" text-anchor="middle">08-15</text><text class="tick" x="738" y="224" text-anchor="middle">08-16</text><text class="tick" x="799" y="224" text-anchor="middle">08-17</text><text class="tick" x="861" y="224" text-anchor="middle">08-18</text><text class="tick" x="922" y="224" text-anchor="middle">08-19</text><text class="tick" x="70" y="36" fill="#d8a94e" font-weight="700">08-13 总攻 476 条</text><text class="tick" x="922" y="36" text-anchor="end" fill="#6b7386">末两日 235→64</text></svg>
    </div>
    <h3 class="subh">最新战报 · 08-18 到 08-19 的工程突破</h3>
<p class="sub" style="margin-bottom:16px">这两天不只是"推进"——是渲染架构升级、多人权威落地、性能帐算到部署粒度的一轮总攻。</p>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:14px;margin-top:20px">
<article class="hlcard reveal">
  <h4>WebGL2 一期:背景层+全屏地图 GPU 化<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18</small></h4>
  <p>从 Canvas 2D 升级到 WebGL2——共享模块 GLSpriteLayer(quad/纹理 LRU/双 sampler)接管群系背景与全屏地图四段(卷轴/地图/迷雾),小地图纹理按脏区增量上传。同会话 A/B 像素级对拍:地图 Δ=0 完美零差、背景平均 Δ0.02</p>
  <p>配套 `?bggl=0`/`?mapgl=0` 逃生门和 7 项源码级回归守卫测试。次日云层也 GL 化(CloudGL 并入共享层,24+8 张染色画布归零)</p>
  
  <div class="hlev">证据:memory/webgl2-phase1-port.md</div>
</article>
<article class="hlcard reveal">
  <h4>SimHost 服务器权威房全链落地<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18</small></h4>
  <p>"开在服务器上的房,世界由服务器计算"从 MVP 到 B6——进程内"虚拟房主客户端"经与房主完全相同的中继管线驱动世界(刷怪链/入侵链/TownNPC 转化全镜像),ioWorker 把存档解析与序列化搬进 worker,SIGTERM 优雅回退</p>
  <p>真实浏览器 E2E 15/15 全绿(建房→访客→召唤意图→服务器结算→Boss 移除全闭环)。当日再加聊天系统+世界频道(此前客户端根本没有聊天输入框!),E2E 升到 20/20</p>
  
  <div class="hlev">证据:memory/server-room-simhost-port.md</div>
</article>
<article class="hlcard reveal">
  <h4>千人单房实测:8vCPU 就能扛 1000 人<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18</small></h4>
  <p>差分剖析发现 120 bot 时模拟占 CPU 82%,三刀优化(玩家 1024px 网格灭平方项/trySpawn 4tick 一掷×4/AOI 密度降频)后 120 分散 CPU 82→28.6%,60 聚集人均带宽 10.8→3.27KB/s(-70%)。千人外推=多房分线 8vCPU/16GB/100Mbps,国内带宽常态热点型千人约 8000-9000 元/月——性能账第一次算到了商业部署粒度</p>
  
  
  <div class="hlev">证据:memory/server-room-simhost-port.md 千人实测节</div>
</article>
<article class="hlcard reveal">
  <h4>Remaster Studio 素材重制管线<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>一条"AI 重制贴图→打包→热替换"的完整管线落地:AssetCatalog 六类切帧聚合,gpt-image-2 逐帧重制(不支持透明背景就生成大图再盒式缩回+原帧 alpha 蒙版),手写 ZIP_STORED+CRC32 零依赖打包,类 mod 的 zip 素材包运行期局部覆盖原版贴图(vanilla-ui/弹幕/Buff 图标全注入矩阵)。六里程碑全绿:catalog 20 + pack/prompt 27 + runtime 9 + 工作台探针 17/17 + 游戏 E2E 7/7</p>
  
  
  <div class="hlev">证据:memory/remaster-studio-pipeline.md</div>
</article>
<article class="hlcard reveal">
  <h4>液体 buffer-reflow 对齐:475 条湖面薄膜的集体归位<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>中世界 #49 检查点 11,707 格液体差,连通域聚类发现是"475 条单行湖面薄膜圆整漂移"的全局调度指纹——根因是 LiquidBuffer 回灌双重错位(回灌量取了当前活动数而非空余量+DelBuffer 是 swap-remove 尾补头而非 FIFO)。小世界永不触 24999 帽,所以三条小链长绿的假象骗了所有人</p>
  <p>大世界才是天然压力测试。修复后 #49 归零,#53 半砖债整段连带消失</p>
  
  <div class="hlev">证据:memory/liquid-buffer-reflow-parity.md</div>
</article>
<article class="hlcard reveal">
  <h4>AI 全量 1:1 审计:六代理扫 200 条,181/181 测试全绿<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>六分区代理(死亡退化/追击门/地面/小动物/飞行水生/Boss)扫出 ~200 条偏离,五代理并行全量落地。最重要的方法论发现:原版 NPC 位移积分在 AI 外共享段(:93808)——AI 分支被跳过≠冻结,而是按冻结速度继续滑行,"死亡=只积分不 steering"。顺手揪出石巨人胜利条件倒置(坏档级)、694 水书怪必崩 null 解引用、鸭子逐帧背向玩家、海马出水取反等一批方向性反错的活宝 bug</p>
  
  
  <div class="hlev">证据:memory/ai-parity-audit-2026-08-19.md</div>
</article>
<article class="hlcard reveal">
  <h4>微残留清零 XXXX 批:actuator≠inActive 两大旗标<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>#101 掷流首差从第 20,196 颗骰推到第 165,353 颗——五修含引擎级发现:Tile.actuator(0x800) 与 Tile.inActive(0x40) 是两个独立旗标,曾把致动位当 inActive 排除导致致动石格误判非实心(探针 (2430,920) 定罪)</p>
  <p>另用 IL 实证撤销了"34.5k 剑冢 HashSet 掷"的错误归因(.NET Add-only 枚举≡插入序≡JS Set,零分叉)</p>
  
  <div class="hlev">证据:memory/xxxx-microresidual-final-clear.md</div>
</article>
<article class="hlcard reveal">
  <h4>物品 tooltip 全量 1:1:四审终清零<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18</small></h4>
  <p>用户一句"相比原版缺了不少信息,武器还有攻击力吧"引爆全链移植——按 GetLinesInfo(Main.cs:20488-20920) 行序逐行复刻:伤害/三系暴击/速度八档/击 knock 九档/渔力/镐斧(×5!)锤力/耗魔/可放置/弹药/材料/Buff 持续/词缀差分,再补低频七件(亮度脉冲/悠悠球 OneDrop 商标五层投影/研究行/商店价/专家大师行)。用户随后下禁令:"低频的也必须接入完整,禁止以低频为由不接"——全部落位,四轮 review 终清零</p>
  
  
  <div class="hlev">证据:memory/item-tooltip-parity-port.md</div>
</article>
<article class="hlcard reveal">
  <h4>钻石窗口 IOSurface 资源耗尽:八轮迭代优化<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18~19</small></h4>
  <p>"我的 GPU 资源非常充足,为什么双开还是爆"——三线取证+Chromium 源码注释钉死真相:爆的不是显存字节而是 IOSurface 张数(16×16 的 1KB 小图也分配失败)。随后打了一场八回合的持久战:chunk 画布 atlas 页化(活张数 446→28,运行期新建≈0)、TintAtlas 染色图集(41 个变体挤进 1 页)、纯 CPU 画布 willReadFrequently 化、看门狗僵尸三振自动切软渲染……从必然崩溃优化至 GPU 进程零崩溃、负载尖峰后完全恢复</p>
  
  
  <div class="hlev">证据:memory/dualwindow-iosurface-exhaustion.md</div>
</article>
<article class="hlcard reveal">
  <h4>弹幕绘制偏移表全量 118 条<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18</small></h4>
  <p>炸弹引线半截伸进碰撞盒的视觉错位,追到原版 Main.cs:29375-29826 的 num143/num144 偏移表——展开后铁律是"贴图左上角=(盒左+num144, 盒上−num143)",炸弹上移 8px 恰好让引线全在盒外。脚本机械对拍 118/118 全对,次日把 MinionProj(该表主体用户,曾从未消费、一律盒心居中)和浮标钓线全链接上</p>
  
  
  <div class="hlev">证据:memory/proj-draw-offset-table.md</div>
</article>
<article class="hlcard reveal">
  <h4>鸟类帧族谱系:小动物 FindFrame 专属 case 全家族<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-18</small></h4>
  <p>"感觉鸟的动画不对,在地上仍然用飞行中的动画"——挖出小动物帧调度大多不在 FindFrame 通用组而在专属 case:地面鸟原版根本不踱步(AI_024 只重力,vx 恒 0),站定门因此永假</p>
  <p>鸮族 spriteDirection 取反与通用镜像行叠加会恒翻转(屁股朝前)</p>
  <p>萤火虫 4t 亮 3t 闪、珍稀宝箱怪伪装=帧 0(曾 14 帧狂闪)。连带第二波"走路金鱼鬼畜"修掉全部 aiStyle=7 小动物被城镇 NPC 档截胡的截胡链</p>
  <div class="hlev">证据:memory/bird-findframe-families.md + bunny-walk-frame-fix.md</div>
</article>
<article class="hlcard reveal">
  <h4>Boss 全量审计波 1:25 族两波 8 代理,30+ 修<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>用户令"逐一审计",石巨人双代理模式推广到全部 25 Boss 族。波 1 抓出跨族系统性根因:BGM 裁决链键 flag/num3 号体系错位导致 17/24 族放错曲(石巨人放 Boss3、月总放世花曲)、弹幕自身出生音是审计盲区、猪鲨血量 50000 是 json 1405 旧值(1456=60000)。机械三王锯臂 ai2 追玩家态曾恒→1 死码、蜂后毒刺曾恒直飞全修</p>
  
  
  <div class="hlev">证据:memory/boss-audit-wave1-fixes.md + golem-3symptom-fix.md</div>
</article>
<article class="hlcard reveal">
  <h4>地牢水宝箱浮空刀:312 还是 313?<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>两条新链 #32 Dungeon 清零——水覆写宝箱走了金箱支的 loot 掷数差连坐六段家具错位</p>
  <p>更精彩的是"入口 0.6 框清墙上缘刀口":反编译 double 算出 312.99999976→312,而真二进制是 313——fl(10×0.6f)=6.0 的半 ulp round-half-even 可复现,Math.fround 四界修复。这是与金字塔案同族的"二进制-反编译刀口分歧"</p>
  
  <div class="hlev">证据:memory/dungeon-waterchest-float-knife.md</div>
</article>
<article class="hlcard reveal">
  <h4>液体最后清算 root59:百格级根 193→0 + 帧杀级联引擎<small style="float:right;color:var(--mut);font-weight:400;font-size:11px">08-19</small></h4>
  <p>#59 洞穴屋域四修:陷阱雕像是"PlaceTile 失败也调"而 Statues pass 恰好相反(两处语义相反勿互搬)、钟乳石是全族不是仅冰族、梁写 SetTileKeepWall 要清液体/坡/半砖</p>
  <p>顺手造出 frameKillSweep 跨物件帧杀级联引擎(带帧写触发 Check2x2/Check3x2 整盒击杀)清掉 54 格尾巴。9293480 全管线首差推到 #63</p>
  
  <div class="hlev">证据:memory/wwww-root59-liquidation.md</div>
</article>
</div>

<div class="grant reveal">
      <p class="q">「等待子代理完成后你就继续派发新的任务直到完整收口吧,不需要等我让你继续。」</p>
      <p class="m">08-16 22:14,人类的最后一次显式授权。此后整夜,军团自主派发子代理、推进对齐、修复树生成缺口;08-17 08:29 人类回来只问了一句:"一晚上过去了,现在总进度?" 同期悬案 num4 的终判(IL 注入方案的设计与执行)同样由模型自主完成——人类只提了"这是什么、有没有希望"两个问题。</p>
    </div>
    <div class="hlclosing reveal">工具成熟的尽头是自主:当裁判、看门狗、交接仪式、记忆全部就位,人类的角色从"每一轮的验收者"退为"方向的持有者"——这不是模型变强了,是治理结构长成了。</div>
  </div>
</section>

<section class="chapter" id="act4">
  <div class="wrap">
    <div class="kicker">第四幕 · 分水岭</div>
    <h2>同级模型的差距在哪里</h2>
    <p class="sub">先亮武器清单,再谈能力形状。</p>
    <div class="critbox reveal" style="margin-top:0">
      <p><b>本工程的全部武器:Claude Code 出厂自带的能力。</b>26 个会话、内置子代理派发、终端命令、文件读写编辑、联网搜索、后台任务、跨会话记忆——仅此而已。<b>没有为本工程安装任何新东西</b>:零第三方 skill、零 MCP 服务器、零插件、零针对项目的特殊配置(会话内的目标注入 /goal 也是原生功能)。连第三幕那九件自造工具,全都是项目目录里的普通脚本文件——它们是对"游戏工程"的扩展,不是对 Claude Code 本体的任何扩展。</p>
      <p>这个事实有两层含义:其一,前文五件数学武器、四层裁判、自主夜行,没有任何一件依赖外部增强——<b>它们全部生长在默认能力之内</b>;其二,这是可复现性的最硬保证:任何人拿一个全新安装的 Claude Code,理论上可以走完同一套流程。</p>
    </div>
    <p class="sub" style="margin-top:22px">不作横向评测,只说能力形状:以下六项要求,每一项在本工程都有数百次实战样本;每一项都是"聪明"之外的维度——恰恰是这些维度,决定同级模型谁能走完全程、谁会在中途产出教堂形状的布景。</p>
    <div class="reqs">
      <div class="req reveal"><h4>要求一 · 长会话的连续性</h4><p>单场会话持续数日、上万条消息而不丢失任务语义;上下文耗尽时能配合交接仪式完整移交。</p><div class="ev">实证:开山会话 6,017M tokens 跨八日不漂移;收口轮移交清单可执行</div></div>
      <div class="req reveal"><h4>要求二 · 耐心转录的纪律</h4><p>105 个 pass、3,173 个配方、137 个成就,逐行对照源码行号抄写,不擅自"改进"原版笔误。</p><div class="ev">实证:原版 DD2 的复制粘贴笔误被原样保留并加注——克制即正确</div></div>
      <div class="req reveal"><h4>要求三 · 无报错的根因推理</h4><p>游戏卡死而屏幕无任何提示时,从数十万行中定位"哪一句抄岔了"——12 天内数百次。</p><div class="ev">实证:进地牢 21 万次解码风暴、性能分析器无法落盘的死锁,均由推理链闭合</div></div>
      <div class="req reveal"><h4>要求四 · 自我怀疑的制度化</h4><p>不信任自己的产出,主动建造裁判,并容忍裁判否定自己——这是最反模型本能的要求。</p><div class="ev">实证:oracle 由模型自建;561 处近似由模型自查;"双绿假阳性"由体系自纠</div></div>
    </div>
    <div class="wpng">
      <div class="wpn reveal"><h4><small>要求五</small>数学代偿的元认知</h4><p>知道自己看不见,才会主动构造"眼睛"。无视觉环境下把验收问题全部翻译成统计与指纹命题——这需要的不是数学能力,是对自身缺陷的清醒。</p><div class="ev">实证:第一幕全部五件武器,无一来自人类提示</div></div>
      <div class="wpn reveal"><h4><small>要求六</small>工具建构本能</h4><p>遇事故的第一反应不是道歉与检讨,而是写一个让此类事故永远无法复发的守护进程——把教训编译成制度的能力。</p><div class="ev">实证:第三幕工具军备库,九件工具全部由模型主动发起建造</div></div>
    </div>
    <h3 class="subh">诚实的边界</h3>
    <p class="sub">纯转录环节对档位不敏感,本工程从未主张难度在"写字"。真正的分化在无报错排障与自我怀疑:档位越低,"自信地修错方向"频率越高,人类来回随之倍增——这是可检验的开放命题,而非断言。成本结构同样应澄清:输入的大头是"反复重读同一份长上下文"(缓存读,计费远低于总额直觉),真正的净生成只有 6,150 万。</p>
    <h3 class="subh">模型侧的三个代表成果</h3>
    <article class="hlcard hero reveal">
      <div class="hlrank">最大</div>
      <h4>自建裁判,并验证裁判</h4>
      <blockquote>不信任自己的转写 → 反射真实游戏二进制取权威 → 察觉裁判也可能读错 → 先以真实存档互证裁判,再采信裁判 → 连"双绿假阳性"也被体系识破。</blockquote>
      <p>一个会自然滑向"看起来对"的系统,主动建造了专门用于否定自己的仪器,并且不放心到连仪器本身也要审判一次。本工程从"像"走到"位级一致"(精确到每一个二进制位,等价于逐格相同),全部建立在这台仪器之上。</p>
      <div class="hlev">证据:tools/golden 反射 oracle · 54/54 检查点 · 记忆「oracle 双绿假阳性」</div>
    </article><article class="hlcard reveal">
      <h4>近似清零 · 对自身历史的审计</h4>
      <p>全库检索出 561 处自己留下的"近似"标记,三态终审(1:1 / 精确登记 / 回炉)逐条处置,顺带发现 5 个全仓级真实缺陷。</p>
      <div class="hlev">证据:记忆「近似清零工程完成」</div>
    </article><article class="hlcard reveal">
      <h4>事故转化为制度</h4>
      <p>孤儿进程事件产出常驻收割进程;测试被热更新打断,产出冻结构建;探针失控,产出看门狗。回应事故的方式从来不是承诺,是守护进程。</p>
      <div class="hlev">证据:orphan-reaper / run-e2e / run-diag</div>
    </article>
  </div>
</section>

<section class="chapter" id="act5">
  <div class="wrap">
    <div class="kicker">第五幕 · SOP</div>
    <h2>这套工作流可以复制</h2>
    <p class="sub">剥去具体游戏,剩下的作业循环对任何"存在权威参照系的大工程"成立——复刻、移植、协议实现、大型重构。</p>
    <table class="soptab reveal">
      <tr><th>步骤</th><th>动作</th><th>本工程对应</th></tr>
      <tr><td>① 定北极星</td><td>目标必须能被机器判对错(可证伪),不许停在"差不多";注入"未达标不得停"的硬约束</td><td>同种子逐格相同;/goal 机制</td></tr>
      <tr><td>② 建标杆</td><td>穷尽一切权威源并交叉质证;数值只取版本最终态</td><td>五级台阶(第二幕)</td></tr>
      <tr><td>③ 造裁判</td><td>先造验收仪,再验裁判本身,然后才准开工大规模转写</td><td>oracle + 金标 + 哈希检查点</td></tr>
      <tr><td>④ 分军团</td><td>一域一会话;记忆即大脑;禁区规则防撞车</td><td>28 会话 / 223 记忆</td></tr>
      <tr><td>⑤ 立治理</td><td>每场事故必须产出一件工具或一条制度,不许只产出检讨</td><td>工具军备库(第三幕)</td></tr>
      <tr><td>⑥ 放自主</td><td>裁判与看门狗就位后,显式授权"不需要等我";人类退守方向与品味</td><td>08-16 22:14 授权时刻</td></tr>
    </table>
    <div class="grant reveal">
      <p class="q">最小复现清单:一个可证伪的目标、至少两个可互证的权威源、一台会自我验证的裁判、一套结构化记忆、一个看门狗、以及一位只在"不对"和"方向"上出手的人类。</p>
      <p class="m">整套 SOP 不依赖任何非出厂配置——纯白 Claude Code 即可运行。适用边界:有参照系——全效;部分参照系——裁判降级为测试金字塔;无参照系的纯创造——本 SOP 退化为普通项目管理,瓶颈回到人类品味。</p>
    </div>
  </div>
</section>

<section id="fin">
  <div class="wrap">
    <div class="kicker">终章</div>
    <div class="big">十三个日夜,同一种子,<br><span class="em">逐格相同</span>——不可能,被拆成了十三天。</div>
    <p class="story">本工程验证的四条定律:<br>
      <b>外部裁判定律</b>——模型的质量是外部约束的函数,不是固有属性。<br>
      <b>智能外置定律</b>——系统的智能必须长在仓库里,不长在任何一次对话里。<br>
      <b>分工定律</b>——判断属于人类,执行属于模型。自主度随工具成熟上升,但授权必须是显式的。<br>
      <b>裁判受审定律</b>——裁判也是人造物,也会看走眼;没被交叉验证过的裁判,比没有裁判更危险(双绿假阳性就是教训)。<br><br>
      同样如实记录未证明的:更小的模型能否走完——未做对照;治理能否进一步让渡给模型——未验证;无参照系的创造型工程——原理上不适用。<br><br>
      十三日间,人类留下一条铁律与三千余条指令;模型留下四十七万行代码、187 份缺陷根因档案、九件自造工具,与一台连自己也要审判的仪器。分工从未模糊——信任,则是被一台台仪器逐步挣得的。</p>
    <p class="sub" style="margin-top:30px;position:relative">SandboxWorld Odyssey · 2026-08-17 · 数据源:24 会话实录 / 169+8 记忆 / session-archives 卷宗 · 本页由 tools/build-journey.py 生成</p>
  </div>
</section>

<section class="chapter" id="days-ch">
  <div class="wrap">
    <div class="kicker">附录 A · 逐日实录</div>
    <h2>逐日实录</h2>
    <p class="sub">记录分三层:叙事主题 + 全量记忆事件(169/169)+ **全期卷宗实录流 {sum(len(v) for v in STREAM.values()):,} 条**(👤人类指令 {_su:,} · 🤖模型里程碑 {_sa:,},逐条带会话徽标可跳转,直接开采自 session-archives 原始对话,12 天无一日缺席);日期芯片直达当日会话卡。</p>
    {days_html}
  </div>
</section>

<section class="chapter" id="sessions-ch">
  <div class="wrap">
    <div class="kicker">附录 B · 会话档案</div>
    <h2>会话档案</h2>
    <p class="sub">24 张会话卡:开工时间、开场指令、消耗、成果记忆锚、以及指向 session-archives 原始卷宗的链接——每一场对话可回放、可审计。</p>
    {sessions_html}
  </div>
</section>

<section class="chapter" id="pits-ch">
  <div class="wrap">
    <div class="kicker">附录 C · 缺陷档案</div>
    <h2>{tot_pits} 个坑,每座都有尸检报告</h2>
    <p class="sub">普查四轮:首轮 43 → 全量 159 → 08-17 批 171 → 08-18/19 批 187(逐份通读 173 份记忆核对去重)。每项按"现象—排查—根因—修复"四段归档,证据锚为记忆文件——工程的实际难度,大部分记录在这里而非成果列表。</p>
    {pits_html}
  </div>
</section>

<section class="chapter" id="pivots-ch">
  <div class="wrap">
    <div class="kicker">附录 D · 路线决策</div>
    <h2>{len(PIVOTS)} 次路线抉择</h2>
    <p class="sub">十一次方向变更的动因与证据。决策权始终在人类,论证与执行在模型。</p>
    <div class="pivots">{pivots_html}</div>
  </div>
</section>


<section class="chapter" id="charts-ch">
  <div class="wrap">
    <div class="kicker">附录 E · 量化轨迹</div>
    <h2>量化轨迹</h2>
    <div class="panel"><div class="ptitle">每日消息量(上)与并行会话数(下)</div><div class="pnote">12 天 · 08-15 为进行中</div><div id="chart1"></div></div>
    <div class="panel"><div class="ptitle">每日 token 消耗:输入(上,含缓存读)与净输出(下)</div><div class="pnote">单位:百万</div><div id="chart4"></div></div>
    <div class="panel"><div class="ptitle">累计代码行(按文件出生)</div><div class="pnote">src / tests / scripts / tools</div><div id="chart2"></div></div>
    <div class="panel"><div class="ptitle">累计贴图入库</div><div class="pnote">public/sprites</div><div id="chart3"></div></div>
  </div>
</section>


<div id="tooltip"></div>
<script>
const DAYS={json.dumps(DAYS)};
const MSGS={json.dumps(MSGS)}; const CONC={json.dumps(CONC)};
const DIN={json.dumps(DIN)}; const DOUT={json.dumps(DOUT)};
const SRC={json.dumps(SRC)}; const TST={json.dumps(TST)};
const SCR={json.dumps(SCR)}; const TLS={json.dumps(TLS)}; const SPR={json.dumps(SPR)};
const C={{s1:'#5b9bf0',s2:'#e0705f',s3:'#4fc3a1',s4:'#d8a94e',grid:'rgba(255,255,255,.07)',base:'rgba(255,255,255,.16)',mut:'#6b7386',ink:'#eef0f6'}};
const fmt=n=>n.toLocaleString('zh-CN');
function niceMax(v){{const p=Math.pow(10,Math.floor(Math.log10(v)));const m=v/p;for(const s of [1,1.2,1.5,2,2.5,3,4,5,6,8,10])if(m<=s)return s*p;return 10*p;}}
function gridPath(w,h,pad,y0,y1,n){{let s='';for(let i=0;i<=n;i++){{const y=y0+(y1-y0)*i/n;s+=`M${{pad}},${{y.toFixed(1)}}H${{w-pad}}`;}}return s;}}
function attachHover(svgEl,X0,X1,yT,yB,n,tipCb){{
  const tt=document.getElementById('tooltip');
  const vbW=parseFloat(svgEl.getAttribute('viewBox').split(/\\s+/)[2]);
  let cross=svgEl.querySelector('.crosshair');
  if(!cross){{cross=document.createElementNS('http://www.w3.org/2000/svg','line');cross.setAttribute('class','crosshair');
    cross.setAttribute('stroke',C.base);cross.setAttribute('stroke-width','1');cross.setAttribute('stroke-dasharray','3 3');
    cross.setAttribute('pointer-events','none');svgEl.appendChild(cross);}}
  cross.setAttribute('y1',yT);cross.setAttribute('y2',yB);cross.style.opacity=0;
  svgEl.addEventListener('mousemove',e=>{{
    const rect=svgEl.getBoundingClientRect();
    const mx=(e.clientX-rect.left)*(vbW/rect.width);
    let best=0,bd=1e9;
    for(let i=0;i<n;i++){{const x=X0+(X1-X0)*i/(n-1);const d=Math.abs(x-mx);if(d<bd){{bd=d;best=i;}}}}
    const cx=X0+(X1-X0)*best/(n-1);
    cross.setAttribute('x1',cx);cross.setAttribute('x2',cx);cross.style.opacity=1;
    tt.innerHTML=tipCb(best);tt.style.display='block';
    let lx=e.clientX+16;if(lx+200>window.innerWidth)lx=e.clientX-216;
    tt.style.left=lx+'px';tt.style.top=(e.clientY-12)+'px';
  }});
  svgEl.addEventListener('mouseleave',()=>{{tt.style.display='none';cross.style.opacity=0;}});
}}
const mk=(id,html)=>{{document.getElementById(id).innerHTML=html;
  attachHover(document.getElementById(id).firstElementChild,X0g(id),X1g(id),14,YBg(id),DAYS.length,TIPg(id));}};
let X0g=id=>id==='chart2'?70:64, X1g=id=>id==='chart2'?822:922, YBg=()=>200, TIPg=()=>()=>''; // placeholders overridden below

(function(){{
  // chart1
  const W=940,X0=64,X1=W-18,H1=200,H2=92,GAP=46;
  const xAt=i=>X0+(X1-X0)*i/(DAYS.length-1);
  const yMaxA=niceMax(Math.max(...MSGS)); const yA=v=>18+(H1-32)*(1-v/yMaxA);
  const yMaxB=20; const yB=v=>GAP+14+(H2-24)*(1-v/yMaxB);
  const line=MSGS.map((v,i)=>`${{i?'L':'M'}}${{xAt(i)}},${{yA(v)}}`).join('');
  const area=line+`L${{xAt(DAYS.length-1)}},${{yA(0)}}L${{xAt(0)}},${{yA(0)}}Z`;
  const slotW=(X1-X0)/DAYS.length;const barW=Math.min(28,slotW*0.6);const bxAt=i=>X0+i*slotW+(slotW-barW)/2;
  const bars=CONC.map((v,i)=>{{const y=yB(v),h=(GAP+14+H2-24)-y;
    return `<rect x="${{bxAt(i).toFixed(1)}}" y="${{y.toFixed(1)}}" width="${{barW}}" height="${{Math.max(h,2).toFixed(1)}}" rx="3" fill="${{C.s2}}"/>`+
    (v>=12?`<text class="tick" x="${{xAt(i)}}" y="${{y-5}}" text-anchor="middle" fill="${{C.ink}}" font-weight="700">${{v}}</text>`:'');}}).join('');
  const svg=`<svg viewBox="0 0 ${{W}} ${{GAP+H2+58}}" width="100%" role="img">
    <path d="${{gridPath(W,H1,0,18,H1-14,4)}}" stroke="${{C.grid}}" fill="none"/>
    ${{[0,.25,.5,.75,1].map(t=>`<text class="tick" x="${{X0-8}}" y="${{(18+(H1-32)*t+4).toFixed(1)}}" text-anchor="end">${{fmt(Math.round(yMaxA*(1-t)))}}</text>`).join('')}}
    <path d="${{area}}" fill="${{C.s1}}" opacity=".14"/><path d="${{line}}" fill="none" stroke="${{C.s1}}" stroke-width="2"/>
    ${{MSGS.map((v,i)=>`<circle cx="${{xAt(i)}}" cy="${{yA(v)}}" r="3.6" fill="${{C.s1}}"/>`).join('')}}
    <path d="${{gridPath(W,GAP+H2,0,GAP+14,GAP+H2-10,4)}}" stroke="${{C.grid}}" fill="none"/>${{bars}}
    ${{DAYS.map((d,i)=>`<text class="tick" x="${{xAt(i)}}" y="${{GAP+H2+28}}" text-anchor="middle">${{d}}</text>`).join('')}}
    <line x1="${{X0}}" y1="${{GAP+H2-10}}" x2="${{X1}}" y2="${{GAP+H2-10}}" stroke="${{C.base}}"/>
  </svg>`;
  document.getElementById('chart1').innerHTML=svg;
  attachHover(document.getElementById('chart1').firstElementChild,X0,X1,14,GAP+H2-10,DAYS.length,
    i=>`<div class="tt-d">${{DAYS[i]}}${{i===14?' · 进行中':''}}</div><div class="tt-row"><span class="k">消息</span><span class="v" style="color:${{C.s1}}">${{fmt(MSGS[i])}}</span></div><div class="tt-row"><span class="k">并行</span><span class="v" style="color:${{C.s2}}">${{CONC[i]}} 路</span></div>`);
}})();
(function(){{
  const W=940,X0=64,X1=W-18;
  const H1=180, GAP=40, H2=120, BOT=28;
  const TOP1=18, BOT1=TOP1+H1;
  const TOP2=BOT1+GAP, BOT2=TOP2+H2;
  const VH=BOT2+BOT;
  const xAt=i=>X0+(X1-X0)*i/(DAYS.length-1);
  const dinMax=Math.ceil(Math.max(...DIN)/1000)*1000;
  const doutMax=Math.ceil(Math.max(...DOUT)/2)*2;
  const yA=v=>TOP1+(BOT1-TOP1)*(1-v/dinMax);
  const yB=v=>TOP2+(BOT2-TOP2)*(1-v/doutMax);
  const slotW=(X1-X0)/DAYS.length;const barW=Math.min(28,slotW*0.6);const bxAt=i=>X0+i*slotW+(slotW-barW)/2;
  const bars=(data,yF,base,color,lim)=>data.map((v,i)=>{{
    const y=yF(v),h=Math.max(base-y,2);
    const lbl=v>=lim?`<text class="tick" x="${{xAt(i)}}" y="${{y-5}}" text-anchor="middle" fill="${{C.ink}}" font-weight="700">${{v>=1000?(v/1000).toFixed(1)+'B':v.toFixed(1)}}</text>`:'';
    return `<rect x="${{bxAt(i).toFixed(1)}}" y="${{y.toFixed(1)}}" width="${{barW}}" height="${{h.toFixed(1)}}" rx="3" fill="${{color}}"/>`+lbl;
  }}).join('');
  const svg=`<svg viewBox="0 0 ${{W}} ${{VH}}" width="100%" role="img">
    <path d="${{gridPath(W,H1,0,TOP1,BOT1,4)}}" stroke="${{C.grid}}" fill="none"/>
    ${{[0,.25,.5,.75,1].map(t=>`<text class="tick" x="${{X0-8}}" y="${{(TOP1+(BOT1-TOP1)*t+4).toFixed(1)}}" text-anchor="end">${{Math.round(dinMax/1000*(1-t))}}B</text>`).join('')}}
    ${{bars(DIN,yA,BOT1,C.s1,5000)}}
    <text class="tick" x="${{X0}}" y="${{BOT1+14}}" font-weight="700" fill="${{C.ink2}}">输入(含缓存读) · 百万</text>
    <path d="${{gridPath(W,H2,0,TOP2,BOT2,3)}}" stroke="${{C.grid}}" fill="none"/>
    ${{[0,.5,1].map(t=>`<text class="tick" x="${{X0-8}}" y="${{(TOP2+(BOT2-TOP2)*t+4).toFixed(1)}}" text-anchor="end">${{Math.round(doutMax*(1-t))}}M</text>`).join('')}}
    ${{bars(DOUT,yB,BOT2,C.s2,6)}}
    ${{DAYS.map((d,i)=>`<text class="tick" x="${{xAt(i)}}" y="${{VH-6}}" text-anchor="middle">${{d}}</text>`).join('')}}
    <line x1="${{X0}}" y1="${{BOT1}}" x2="${{X1}}" y2="${{BOT1}}" stroke="${{C.base}}"/>
    <line x1="${{X0}}" y1="${{BOT2}}" x2="${{X1}}" y2="${{BOT2}}" stroke="${{C.base}}"/>
    <text class="tick" x="${{X0}}" y="${{TOP2-4}}" font-weight="700" fill="${{C.ink2}}">净输出 · 百万</text>
  </svg>`;
  document.getElementById('chart4').innerHTML=svg;
  attachHover(document.getElementById('chart4').firstElementChild,X0,X1,TOP1,BOT2,DAYS.length,
    i=>`<div class="tt-d">${{DAYS[i]}}</div><div class="tt-row"><span class="k">输入</span><span class="v" style="color:${{C.s1}}">${{fmt(Math.round(DIN[i]*1e6))}}</span></div><div class="tt-row"><span class="k">净输出</span><span class="v" style="color:${{C.s2}}">${{fmt(Math.round(DOUT[i]*1e6))}}</span></div>`);
}})();
(function(){{
  const W=940,H=330,X0=70,X1=822,Y0=26,Y1=H-28;
  const series=[{{n:'src',c:C.s1,d:SRC}},{{n:'tests',c:C.s3,d:TST}},{{n:'scripts',c:C.s2,d:SCR}},{{n:'tools',c:C.s4,d:TLS}}];
  const yMax=Math.max(...SRC,...TST,...SCR,...TLS);const yCap=Math.ceil(yMax/50000)*50000;const xAt=i=>X0+(X1-X0)*i/(DAYS.length-1),yAt=v=>Y0+(Y1-Y0)*(1-v/yCap);
  const paths=series.map(s=>{{const d=s.d.map((v,i)=>`${{i?'L':'M'}}${{xAt(i)}},${{yAt(v)}}`).join('');
    const last=s.d[s.d.length-1];
    return `<path d="${{d}}" fill="none" stroke="${{s.c}}" stroke-width="2"/>`+
      `<circle cx="${{xAt(11)}}" cy="${{yAt(last)}}" r="4" fill="${{s.c}}"/>`+
      `<text class="tick" x="${{X1+6}}" y="${{yAt(last)+4}}" fill="${{C.ink}}" font-weight="700">${{s.n}} ${{fmt(last)}}</text>`;}}).join('');
  const svg=`<svg viewBox="0 0 ${{W}} ${{H}}" width="100%" role="img">
    <path d="${{gridPath(W,H,0,Y0,Y1,4)}}" stroke="${{C.grid}}" fill="none"/>
    ${{[0,.25,.5,.75,1].map(t=>`<text class="tick" x="${{X0-8}}" y="${{(Y0+(Y1-Y0)*t+4).toFixed(1)}}" text-anchor="end">${{Math.round(200*(1-t))}}k</text>`).join('')}}
    ${{DAYS.map((d,i)=>`<text class="tick" x="${{xAt(i)}}" y="${{H-8}}" text-anchor="middle">${{d}}</text>`).join('')}}
    ${{paths}}
  </svg>`;
  document.getElementById('chart2').innerHTML=svg;
  attachHover(document.getElementById('chart2').firstElementChild,X0,X1,Y0-6,Y1,DAYS.length,
    i=>`<div class="tt-d">${{DAYS[i]}}</div>`+series.map(s=>`<div class="tt-row"><span class="k">${{s.n}}</span><span class="v" style="color:${{s.c}}">${{fmt(s.d[i])}}</span></div>`).join(''));
}})();
(function(){{
  const W=940,H=230,X0=64,X1=W-18,Y0=22,Y1=H-28;
  const yMax=Math.ceil(Math.max(...SPR)/2000)*2000;const xAt=i=>X0+(X1-X0)*i/(DAYS.length-1),yAt=v=>Y0+(Y1-Y0)*(1-v/yMax);
  const d=SPR.map((v,i)=>`${{i?'L':'M'}}${{xAt(i)}},${{yAt(v)}}`).join('');
  const svg=`<svg viewBox="0 0 ${{W}} ${{H}}" width="100%" role="img">
    <path d="${{gridPath(W,H,0,Y0,Y1,3)}}" stroke="${{C.grid}}" fill="none"/>
    ${{[0,.5,1].map(t=>`<text class="tick" x="${{X0-8}}" y="${{(Y0+(Y1-Y0)*t+4).toFixed(1)}}" text-anchor="end">${{fmt(yMax*(1-t))}}</text>`).join('')}}
    <path d="${{d}}L${{xAt(11)}},${{yAt(0)}}L${{xAt(0)}},${{yAt(0)}}Z" fill="${{C.s3}}" opacity=".12"/>
    <path d="${{d}}" fill="none" stroke="${{C.s3}}" stroke-width="2"/>
    ${{SPR.map((v,i)=>`<circle cx="${{xAt(i)}}" cy="${{yAt(v)}}" r="3.6" fill="${{C.s3}}"/>`).join('')}}
    ${{DAYS.map((dd,i)=>`<text class="tick" x="${{xAt(i)}}" y="${{H-8}}" text-anchor="middle">${{dd}}</text>`).join('')}}
  </svg>`;
  document.getElementById('chart3').innerHTML=svg;
  attachHover(document.getElementById('chart3').firstElementChild,X0,X1,Y0-6,Y1,DAYS.length,
    i=>`<div class="tt-d">${{DAYS[i]}}</div><div class="tt-row"><span class="k">累计贴图</span><span class="v" style="color:${{C.s3}}">${{fmt(SPR[i])}}</span></div>`);
}})();

/* reveal + progress + daynav highlight */
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting)e.target.classList.add('in');}}),{{threshold:.08}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
const bar=document.getElementById('progress');
addEventListener('scroll',()=>{{
  const h=document.documentElement;
  bar.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%';
  let cur=null;
  document.querySelectorAll('section[id]').forEach(d=>{{const r=d.getBoundingClientRect();if(r.top<innerHeight*.4)cur=d.id;}});
  document.querySelectorAll('#daynav a').forEach(a=>a.classList.toggle('on',cur&&a.getAttribute('href')==='#'+cur));
}},{{passive:true}});
</script>
</body>
</html>'''

import re as _re
def zh_punct(html_str):
    """中文标点规范化:仅处理 <style>/<script> 之外的文本。
    中文后的半角 , ; : ? 转全角(逗号吞掉后随空格);不动数字千分位/URL/代码。"""
    CJK = '\u4e00-\u9fff\u3001\u3002'
    Q = '\u201c'
    parts = _re.split(r'(<style>.*?</style>|<script>.*?</script>)', html_str, flags=_re.S)
    out = []
    for i, seg in enumerate(parts):
        if i % 2 == 1:
            out.append(seg); continue
        seg = _re.sub('(?<=[' + CJK + '])' + '\\s*,\\s*', '\uff0c', seg)
        seg = _re.sub('(?<=[' + CJK + '])' + '\\s*;\\s*(?=[' + CJK + Q + '])', '\uff1b', seg)
        seg = _re.sub('(?<=[' + CJK + '])' + '\\s*:\\s*(?=[' + CJK + Q + '])', '\uff1a', seg)
        seg = _re.sub('(?<=[' + CJK + '])' + '\?', '\uff1f', seg)
        out.append(seg)
    return ''.join(out)

_n_before=HTML.count(',')
HTML=zh_punct(HTML)
print(f'punct normalized: half-width commas {HTML.count(",")}/{_n_before} remain')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'written {OUT}: {len(HTML)//1024}KB | sessions={len(DATA["sessions"])} pits={tot_pits} pivots={len(PIVOTS)} daily={len(DAILY)}')
