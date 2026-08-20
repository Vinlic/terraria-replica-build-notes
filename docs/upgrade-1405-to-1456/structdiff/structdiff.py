#!/usr/bin/env python3
"""Structural diff between Terarria1405 (dotPeek, 1.4.0.5) and Terarria1456 (ilspycmd, 1.4.5.6).

Compares at member level (types / methods / fields / enum members), NOT line-level,
because the two trees come from different decompilers.
"""
import os, re, sys, json
from collections import defaultdict

ROOT_1405 = "~/Project/GLM/SandboxWorld/Terarria1405"
ROOT_1456 = "~/Project/GLM/SandboxWorld/Terarria1456"

# files added manually to 1405 (not vanilla) — exclude
EXCLUDE_1405 = {"NPC.145.cs", "annotations.json"}

def norm_key_1405(path):
    rel = os.path.relpath(path, ROOT_1405)
    if rel in EXCLUDE_1405:
        return None
    d, f = os.path.split(rel)
    return "Terraria/" + (d + "/" if d else "") + f

def norm_key_1456(path):
    rel = os.path.relpath(path, ROOT_1456)
    d, f = os.path.split(rel)
    if d:
        d = d.replace(".", "/") + "/"
    return d + f

def collect(root, norm_fn):
    files = {}
    for dirpath, _, names in os.walk(root):
        for n in names:
            if not n.endswith(".cs"):
                continue
            p = os.path.join(dirpath, n)
            k = norm_fn(p)
            if k:
                files[k] = p
    return files

RE_TYPE = re.compile(r'^\s*(?:\[[^\]]*\]\s*)*(?:(?:public|internal|private|protected|static|sealed|abstract|partial|readonly|ref|unsafe)\s+)*(class|struct|enum|interface)\s+([A-Za-z_]\w*)')
RE_METHOD = re.compile(
    r'^[ \t]+(?:\[[^\]]*\][^\n]*\n[ \t]+)*'
    r'(?:(?:public|private|protected|internal|static|virtual|override|sealed|abstract|extern|unsafe|new|partial|readonly|async)\s+)+'
    r'[\w<>\[\],.?@ ]+?\s+([A-Za-z_]\w*)\s*\(')
RE_FIELD = re.compile(
    r'^\s*(?:\[[^\]]*\]\s*)*(?:(?:public|private|protected|internal|static|const|readonly|volatile|unsafe)\s+)+'
    r'[\w<>\[\],.?@ ]+?\s+([A-Za-z_]\w*)\s*(?:[=;])')
SKIP_NAMES = {"if", "for", "foreach", "while", "switch", "catch", "using", "return", "lock", "fixed", "else", "do"}

def members(path):
    types, methods, fields = set(), set(), set()
    try:
        text = open(path, encoding="utf-8-sig", errors="replace").read()
    except Exception:
        return types, methods, fields
    for line in text.splitlines():
        m = RE_TYPE.match(line)
        if m:
            types.add(m.group(2))
            continue
        m = RE_METHOD.match(line)
        if m and m.group(1) not in SKIP_NAMES:
            methods.add(m.group(1))
            continue
        m = RE_FIELD.match(line)
        if m and m.group(1) not in SKIP_NAMES:
            fields.add(m.group(1))
    return types, methods, fields

def main():
    f1405 = collect(ROOT_1405, norm_key_1405)
    f1456 = collect(ROOT_1456, norm_key_1456)
    keys1405, keys1456 = set(f1405), set(f1456)

    new_files = sorted(keys1456 - keys1405)
    gone_files = sorted(keys1405 - keys1456)

    report = {"new_files": new_files, "gone_files": gone_files, "deltas": {}}

    for k in sorted(keys1405 & keys1456):
        t1, m1, fl1 = members(f1405[k])
        t2, m2, fl2 = members(f1456[k])
        d = {
            "types_added": sorted(t2 - t1), "types_removed": sorted(t1 - t2),
            "methods_added": sorted(m2 - m1), "methods_removed": sorted(m1 - m2),
            "fields_added": sorted(fl2 - fl1), "fields_removed": sorted(fl1 - fl2),
        }
        if any(d.values()):
            report["deltas"][k] = d

    with open("/tmp/tw-changelog/structdiff.json", "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    # ---- markdown summary ----
    out = []
    out.append(f"# 源码结构 diff:1.4.0.5 (Terarria1405) → 1.4.5.6 (Terarria1456)\n")
    out.append(f"- 共同文件:{len(keys1405 & keys1456)};1456 新增文件:{len(new_files)};1405 独有(移除/更名/人工添加):{len(gone_files)}")
    out.append(f"- 有成员增删的共同文件:{len(report['deltas'])}\n")
    out.append("## 一、1456 新增文件(新系统)\n")
    for k in new_files:
        out.append(f"- {k}")
    out.append("\n## 二、1405 独有文件(可能是重命名/合并进其他文件)\n")
    for k in gone_files:
        out.append(f"- {k}")
    out.append("\n## 三、共同文件的成员增删\n")
    # sort by amount of change desc
    def weight(d):
        return sum(len(v) for v in d.values())
    for k, d in sorted(report["deltas"].items(), key=lambda kv: -weight(kv[1])):
        w = weight(d)
        out.append(f"\n### {k} (+{len(d['methods_added'])+len(d['fields_added'])+len(d['types_added'])} / -{len(d['methods_removed'])+len(d['fields_removed'])+len(d['types_removed'])})")
        note = ""
        if len(d["methods_removed"]) > 25:
            note = "  <!--注意:removed 大概率是 1405 dotPeek 反编译空壳/命名差异造成的假象-->"
        if d["types_added"]:
            out.append(f"- 新类型(+{len(d['types_added'])}): {', '.join(d['types_added'][:60])}{' …' if len(d['types_added'])>60 else ''}")
        if d["methods_added"]:
            out.append(f"- 新方法(+{len(d['methods_added'])}): {', '.join(d['methods_added'][:80])}{' …' if len(d['methods_added'])>80 else ''}{note}")
        if d["fields_added"]:
            out.append(f"- 新字段(+{len(d['fields_added'])}): {', '.join(d['fields_added'][:80])}{' …' if len(d['fields_added'])>80 else ''}")
        if d["types_removed"]:
            out.append(f"- 移除类型(-{len(d['types_removed'])}): {', '.join(d['types_removed'][:30])}")
        if d["methods_removed"]:
            out.append(f"- 移除方法(-{len(d['methods_removed'])}): {', '.join(d['methods_removed'][:30])}{' …' if len(d['methods_removed'])>30 else ''}{note}")
        if d["fields_removed"]:
            out.append(f"- 移除字段(-{len(d['fields_removed'])}): {', '.join(d['fields_removed'][:30])}")
    with open("/tmp/tw-changelog/structdiff.md", "w") as f:
        f.write("\n".join(out))
    print(f"done. deltas={len(report['deltas'])}, new={len(new_files)}, gone={len(gone_files)}")

if __name__ == "__main__":
    main()
