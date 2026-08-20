#!/usr/bin/env python3
"""全量导出 Claude Code 会话实录为可读 Markdown 档案。

源:~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/
  - <sid>.jsonl        主会话(24 份)
  - <sid>/subagents/*  子代理实录(agent-*.jsonl + meta)
  - memory/*.md        跨会话记忆

出:~/Project/GLM/SandboxWorld/session-archives/
  - README.md                      总索引(每会话统计)
  - sessions/<NN>_<sid8>_<slug>/
      conversation.partN.md         主会话全量对话(超 25MB 分卷)
      subagents/<agent-id>.md       子代理实录(同格式)
      meta.json / *.meta.json       原样拷贝
      images/                       从消息中解码的图片
  - memory/                        记忆全量拷贝

完整性约定:用户/助手全部文本逐字保留;thinking 全收;tool_use 含完整输入 JSON;
tool_result 文本全收;图片解码为文件并链接;system/attachment 收录;
mode/permission-mode/last-prompt/queue-operation/file-history-* 为纯簿记行,
不导出正文,只在头部计数控件里报告。
"""
import base64, glob, hashlib, json, os, re, shutil, sys, time

SRC = os.path.expanduser('~/.claude/projects/-Users-user-Project-GLM-SandboxWorld')
DST = '~/Project/GLM/SandboxWorld/session-archives'
PART_LIMIT = 25 * 1024 * 1024  # 单卷上限
BOOKKEEPING = {'mode', 'permission-mode', 'last-prompt', 'queue-operation',
               'file-history-snapshot', 'file-history-delta'}


import re as _re
_RE_EMAIL=_re.compile(r'[A-Za-z0-9._%+\-]*user[A-Za-z0-9._%+\-]*@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
_RE_UCLOUD=_re.compile(r'\?UCloudPublicKey=[^"\s&]+&Expires=\d+&Signature=[^"\s&]+')
_RE_COOKIE=_re.compile(r'(?i)(set-cookie: [REDACTED]
_RE_LAN=_re.compile(r'\b(192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b')
_RE_HOME=_re.compile(r'/Users/[A-Za-z0-9_.]{2,15}/(Project|Downloads|Library|Desktop|Documents|Movies|Music|Pictures|Applications)')
def sanitize_pii(t):
    t = t.replace('user@mac','user@mac').replace('mac','mac')
    t = t.replace('/Users/user','~').replace('user','玩家').replace('user','user')
    for _v in ('userlic','user','vinli','user'): t = t.replace('/Users/'+_v,'~').replace(_v,'user')
    t = _RE_EMAIL.sub('user@***', t)
    t = _RE_UCLOUD.sub('?[签名参数已移除]', t)
    t = _RE_COOKIE.sub(lambda m: m.group(1)+' [已移除]', t)
    t = _RE_LAN.sub(lambda m: m.group(1)+'.x.x', t)
    t = _RE_HOME.sub(r'~/\1', t)
    return t

def fence(text, base='```'):
    n = max(3, len(base))
    while True:
        f = '`' * n
        if f not in text:
            return f
        n += 1


def jdump(o):
    try:
        return json.dumps(o, ensure_ascii=False, indent=1)
    except Exception:
        return repr(o)


class Writer:
    """分卷 Markdown 写出器。"""
    def __init__(self, outdir, stem):
        self.outdir = outdir
        self.stem = stem
        self.part = 0
        self.buf = []
        self.size = 0
        self.paths = []
        self._open()

    def _open(self):
        self.part += 1
        self.path = os.path.join(self.outdir, f'{self.stem}.part{self.part}.md')
        self.buf = [f'# (第 {self.part} 卷 · 自动分卷)\n']
        self.size = 0

    def w(self, text):
        self.buf.append(sanitize_pii(text))
        self.size += len(text.encode('utf-8'))
        if self.size > PART_LIMIT:
            self.flush()

    def flush(self):
        if not self.buf:
            return
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.buf))
        self.paths.append(self.path)
        if self.size > PART_LIMIT:
            self._open()


class ImageStore:
    def __init__(self, outdir):
        self.dir = os.path.join(outdir, 'images')
        os.makedirs(self.dir, exist_ok=True)
        self.count = 0

    def add(self, b64, media='image/png'):
        try:
            raw = base64.b64decode(b64)
        except Exception:
            return None
        h = hashlib.sha1(raw).hexdigest()[:10]
        ext = media.split('/')[-1].replace('jpeg', 'jpg')
        p = os.path.join(self.dir, f'img-{h}.{ext}')
        if not os.path.exists(p):
            with open(p, 'wb') as f:
                f.write(raw)
        self.count += 1
        return os.path.relpath(p, os.path.dirname(self.dir))


def render_message(msg, role_label, sid, imgs, stats):
    """把一条 message 渲染为 markdown 段。返回 list[str]。"""
    out = [f'\n---\n\n## {role_label}\n']
    content = msg.get('content')
    if isinstance(content, str):
        f = fence(content)
        out.append(f + '\n' + content + ('\n' if not content.endswith('\n') else '') + f)
        return out
    if not isinstance(content, list):
        out.append('```json\n' + jdump(msg) + '\n```')
        return out
    for b in content:
        if not isinstance(b, dict):
            out.append(str(b)); continue
        t = b.get('type')
        if t == 'text':
            txt = b.get('text', '')
            f = fence(txt)
            out.append(f + '\n' + txt + ('\n' if txt and not txt.endswith('\n') else '') + f + '\n')
            stats['text'] += 1
        elif t == 'thinking':
            txt = b.get('thinking', '')
            f = fence(txt)
            out.append('<details open>\n<summary>💭 thinking</summary>\n\n' + f + '\n' + txt + '\n' + f + '\n\n</details>\n')
            stats['thinking'] += 1
        elif t == 'tool_use':
            name = b.get('name', '?')
            inp = b.get('input', {})
            body = jdump(inp)
            f = fence(body, '`' * 3)
            out.append(f'**🔧 ToolUse: `{name}`**\n\n' + f + 'json\n' + body + '\n' + f + '\n')
            stats['tool_use'] += 1
        elif t == 'tool_result':
            cc = b.get('content')
            parts = []
            if isinstance(cc, str):
                parts.append(('text', cc))
            elif isinstance(cc, list):
                for bb in cc:
                    if isinstance(bb, dict) and bb.get('type') == 'text':
                        parts.append(('text', bb.get('text', '')))
                    elif isinstance(bb, dict) and bb.get('type') == 'image':
                        src = bb.get('source', {})
                        b64 = src.get('data') if isinstance(src, dict) else None
                        rel = imgs.add(b64, (src or {}).get('type', 'image/png').replace('image/', '', 1) if isinstance(src, dict) else 'png') if b64 else None
                        if rel:
                            parts.append(('img', rel))
                        else:
                            parts.append(('text', '[image 数据无法解码]'))
                    elif isinstance(bb, dict):
                        parts.append(('text', jdump(bb)))
            elif cc is None:
                parts.append(('text', '(无内容)'))
            else:
                parts.append(('text', jdump(cc)))
            body = []
            for kind, v in parts:
                if kind == 'img':
                    body.append(f'![导出图片]({v})\n')
                else:
                    body.append(v + '\n')
            joined = '\n'.join(body) or '(空)'
            f = fence(joined)
            err = ' ⚠️ERROR' if b.get('is_error') else ''
            out.append(f'**📎 ToolResult{err}**\n\n' + f + '\n' + joined + '\n' + f + '\n')
            stats['tool_result'] += 1
        elif t == 'image':
            src = b.get('source', {})
            b64 = src.get('data') if isinstance(src, dict) else None
            rel = imgs.add(b64, 'png') if b64 else None
            out.append(f'![消息内图片]({rel})\n' if rel else '[image 数据缺失]\n')
        else:
            out.append('```json\n' + jdump(b) + '\n```\n')
    return out


def convert_jsonl(path, outdir, stem, header_lines):
    os.makedirs(outdir, exist_ok=True)
    imgs = ImageStore(outdir)
    wr = Writer(outdir, stem)
    stats = {'text': 0, 'thinking': 0, 'tool_use': 0, 'tool_result': 0}
    book = {}
    n_msgs = 0
    for line in open(path, encoding='utf-8', errors='replace'):
        try:
            e = json.loads(line)
        except Exception:
            wr.w('\n```\n[本行 JSON 解析失败,原样保留]\n' + line.rstrip() + '\n```\n')
            continue
        t = e.get('type')
        if t in BOOKKEEPING:
            book[t] = book.get(t, 0) + 1
            continue
        if t == 'user':
            msg = e.get('message', {})
            label = '👤 User' + ('(meta)' if e.get('isMeta') else '') + ('(sidechain)' if e.get('isSidechain') else '')
            ts = e.get('timestamp', '')
            for seg in render_message(msg, f'{label} · {ts}', None, imgs, stats):
                wr.w(seg)
            n_msgs += 1
        elif t == 'assistant':
            msg = e.get('message', {})
            model = msg.get('model', '')
            ts = e.get('timestamp', '')
            for seg in render_message(msg, f'🤖 Assistant · {ts} · {model}', None, imgs, stats):
                wr.w(seg)
            n_msgs += 1
        elif t == 'system':
            content = e.get('content') or e.get('message') or jdump({k: v for k, v in e.items() if k in ('subtype', 'level', 'content')})
            if not isinstance(content, str):
                content = jdump(content)
            wr.w(f'\n---\n\n## ⚙️ System · {e.get("timestamp","")}\n\n' + content + '\n')
        elif t == 'attachment':
            a = e.get('attachment', e)
            txt = a.get('content') or a.get('text') or ''
            if not txt:
                txt = jdump({k: v for k, v in a.items() if k not in ('data',)})
            body = str(txt)[:200000]
            f = fence(body)
            wr.w(f'\n---\n\n## 📎 Attachment · {a.get("type","?")} · {e.get("timestamp","")}\n\n' + f + '\n' + body + '\n' + f + '\n')
        elif t == 'summary':
            wr.w(f'\n---\n\n## 🗒️ Summary\n\n' + str(e.get('summary', '')) + '\n')
        else:
            wr.w('\n```json\n' + jdump(e) + '\n```\n')
    wr.flush()
    with open(os.path.join(outdir, stem + '.stats.json'), 'w', encoding='utf-8') as f:
        json.dump({'messages': n_msgs, 'blocks': stats, 'bookkeeping_skipped': book,
                   'images': imgs.count, 'parts': [os.path.basename(p) for p in wr.paths],
                   'generated': time.strftime('%Y-%m-%d %H:%M:%S')}, f, ensure_ascii=False, indent=1)
    return {'messages': n_msgs, 'blocks': stats, 'images': imgs.count,
            'parts': len(wr.paths), 'bookkeeping': sum(book.values())}


def slugify(s, maxlen=40):
    s = re.sub(r'[^\w一-鿿-]+', '-', (s or '')).strip('-')
    return (s[:maxlen] or 'session')


def main():
    os.makedirs(DST, exist_ok=True)
    index = []
    files = sorted(glob.glob(os.path.join(SRC, '*.jsonl')),
                   key=lambda f: get_first_ts(f))
    for i, f in enumerate(files, 1):
        sid = os.path.basename(f).split('-')[0]
        first_ts = get_first_ts(f)
        slug = get_slug(f)
        name = f'{i:02d}_{first_ts[2:4]}{first_ts[5:7]}{first_ts[8:10]}_{sid}_{slugify(slug)}'
        outdir = os.path.join(DST, 'sessions', name)
        print(f'[{i}/{len(files)}] {name} ({os.path.getsize(f)/1e6:.0f}MB)', flush=True)
        st = convert_jsonl(f, outdir, 'conversation',
                           [f'# 会话 {sid} · {first_ts}'])
        # 子代理
        sub_dir = os.path.join(SRC, os.path.basename(f)[:-6], 'subagents')
        subs = []
        if os.path.isdir(sub_dir):
            for a in sorted(glob.glob(os.path.join(sub_dir, 'agent-*.jsonl'))):
                aid = os.path.basename(a)[6:-6]
                ast = convert_jsonl(a, os.path.join(outdir, 'subagents'), f'agent-{aid}',
                                    [f'# 子代理 {aid}'])
                subs.append({'agent': aid, **ast})
            for m in glob.glob(os.path.join(sub_dir, '*.meta.json')):
                shutil.copy2(m, os.path.join(outdir, 'subagents', os.path.basename(m)))
        # meta.json(会话级,如有)
        mp = os.path.join(SRC, os.path.basename(f)[:-6], 'meta.json')
        if os.path.exists(mp):
            shutil.copy2(mp, os.path.join(outdir, 'meta.json'))
        index.append({'dir': name, 'sid': sid, 'first': first_ts, 'slug': slug,
                      'src_mb': round(os.path.getsize(f)/1e6, 1), 'main': st, 'subagents': subs})
    with open(os.path.join(DST, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    print('ALL DONE')


def get_first_ts(f):
    with open(f, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            try:
                e = json.loads(line)
                if e.get('timestamp'):
                    return e['timestamp'][:19]
            except Exception:
                pass
    return 'unknown'


def get_slug(f):
    with open(f, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get('slug'):
                return e['slug']
            if e.get('type') == 'user' and not e.get('isMeta'):
                c = e.get('message', {}).get('content')
                txt = c if isinstance(c, str) else ''
                if isinstance(c, list):
                    txt = ' '.join(b.get('text', '') for b in c if isinstance(b, dict) and b.get('type') == 'text')
                txt = txt.strip()
                if txt and not txt.startswith('<'):
                    return txt[:60]
    return 'session'


if __name__ == '__main__':
    main()
