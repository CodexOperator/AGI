#!/usr/bin/env python3
"""Apply streaming-suite/season2 seat patch into config:posts (run on VPS/live box)."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
PATCH = json.loads(Path(sys.argv[2] if len(sys.argv) > 2 else 'seats_patch.json').read_text())
POSTS = ROOT / '.agi/nodes/.geometry/posts.md'
text = POSTS.read_text()
parts = text.split('---', 2)
fm, body = parts[1], parts[2]
m = re.search(r'(^posts:\n)((?:  - .+\n)+)', fm, re.M)
rows = [json.loads(l[4:]) for l in m.group(2).splitlines() if l.startswith('  - ')]
by = {r['name']: r for r in rows}
for p in PATCH:
    name = p['name']
    if name in by:
        by[name].update(p)
    else:
        rows.append(p)
        by[name] = p
orig = [json.loads(l[4:])['name'] for l in m.group(2).splitlines() if l.startswith('  - ')]
ordered = [by[n] for n in orig]
for p in PATCH:
    if p['name'] not in orig:
        ordered.append(by[p['name']])
new_block = ''.join('  - ' + json.dumps(r, ensure_ascii=False) + '\n' for r in ordered)
fm2 = fm[:m.start()] + m.group(1) + new_block + fm[m.end():]
POSTS.write_text('---' + fm2 + '---' + body)
print('applied', len(PATCH), 'seat rows ->', POSTS)
