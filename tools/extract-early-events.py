#!/usr/bin/env python3
"""卷宗实录流 v4:UTC→本地(+08:00)转换与本地日分桶。

修正历史:此前直接用 UTC 时间戳分日/显示,时刻与日期边界都偏了 8 小时
(立项消息 2026-08-04T16:26Z 实为本地 2026-08-05 00:26)。
"""
import glob, json, re
from datetime import datetime, timedelta, timezone

ARC = '~/Project/GLM/SandboxWorld/session-archives/sessions'
OUT = '~/Project/GLM/SandboxWorld/tools/journey-inputs/archive-stream.json'
TZ = timezone(timedelta(hours=8))
_RE_HOME = re.compile(r'/Users/[A-Za-z0-9_.]{2,15}/(Project|Downloads|Library|Desktop|Documents|Movies|Music|Pictures|Applications)')
KEY = re.compile(r'完成|已完成|实现|修复|新增|移植|通过|全绿|✅|PASS|落地|上线|搞定|构建成功|管线|脚手架|对齐')

events = []
for part in glob.glob(ARC + '/*/conversation.part*.md'):
    sid = re.search(r'/\d\d_[0-9]+_([0-9a-f]{8})_', part).group(1)
    txt = open(part, encoding='utf-8').read()
    for b in re.split(r'\n(?=---\n\n## )', txt):
        mh = re.search(r'## (👤|🤖) (?:User|Assistant) · (\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})', b)
        if not mh:
            continue
        who = mh.group(1)
        utc = datetime.strptime(mh.group(2) + 'T' + mh.group(3), '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
        loc = utc.astimezone(TZ)
        body = b[mh.end():]
        body = re.sub(r'<details[^>]*>.*?</details>', '', body, flags=re.S)
        m = re.search(r'\n```\n(.*?)\n```', body, re.S)
        if not m:
            continue
        t = m.group(1).strip()
        if not t or t.lstrip()[0] in '{[':
            continue
        if '📎' in b[:mh.end()+40]:
            continue
        if who == '👤':
            if t.startswith('<') or 'system-reminder' in t[:90] or 'tool_result' in t[:60] or len(t) < 4:
                continue
        else:
            if len(t) < 120 or not KEY.search(t):
                continue
        t = t.replace('/Users/user', '~').replace('user@mac', 'user@mac')
        for _v in ('userlic','user','vinli','user'):
            t = t.replace('/Users/'+_v, '~').replace(_v, 'user')
        t = t.replace('mac', 'mac').replace('user', '玩家').replace('user', 'user')
        t = _RE_HOME.sub(lambda m: '~/' + m.group(1), t)
        events.append({'day': loc.strftime('%m-%d'), 't': loc.strftime('%H:%M'),
                       'who': who, 'text': t[:170].replace('\n', ' '), 'sid': sid})

events.sort(key=lambda e: (e['day'], e['t'], e['sid']))
by_day, last = {}, None
for e in events:
    k = (e['who'], e['text'][:60])
    if k == last:
        continue
    last = k
    by_day.setdefault(e['day'], []).append(e)

json.dump(by_day, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for d in sorted(by_day):
    u = sum(1 for e in by_day[d] if e['who'] == '👤')
    print(d, f'{len(by_day[d])} 条(👤{u} / 🤖{len(by_day[d])-u})')
print('total:', sum(len(v) for v in by_day.values()))
