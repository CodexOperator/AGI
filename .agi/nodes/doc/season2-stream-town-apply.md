---
id: doc:season2-stream-town-apply
mint_id: 0ea27ab4e401402fa0b6294a4b2cb22c
type: doc
tags:
  - doc
  - season2
  - streaming-suite
parents:
  - goal:g18.1
next_edges: []
edited_by: owner
link_ref: /tmp/agi-payloads/season2-stream-town-apply.md
location: source_root
scaffold_hash: 97bcd23380b4aa11
season: 2
spawn_gate: bypassed
status: active
thought_session: grok-bot-season2-migrate
title: Apply commands for streaming-suite/season2 seating
town: streaming-suite
---
<!-- BODY:BEGIN -->
# Apply commands — streaming-suite/season2 seating (VPS / pi)

Authority: `streaming-suite/season2/main` posts at HEAD.

## On a live box with engine + Doppler + OPENROUTER_API_KEY

```bash
cd /path/to/AGI
git fetch origin
git checkout streaming-suite/season2/main
git pull --ff-only origin streaming-suite/season2/main

# Verify seats
python3 - <<'PY'
import json,re
from pathlib import Path
t=Path('.agi/nodes/.geometry/posts.md').read_text()
m=re.search(r'^posts:\n((?:  - .+\n)+)', t, re.M)
rows=[json.loads(l[4:]) for l in m.group(1).splitlines() if l.startswith('  - ')]
for n in ['stream-prime','shael','stream-master','council-streaming-suite','director-g18.1','director-g18','director-g9','director-g10']:
    r=next(x for x in rows if x['name']==n)
    print(n, r.get('model'), r.get('settings'), r.get('owning_goal',''))
PY

# Spawn / wake (names match config:posts). Exact rotate/dispatch flags follow live box runbook:
#   python3 extensions/agi/bin/rotate.py spawn --post stream-prime
#   python3 extensions/agi/bin/rotate.py spawn --post stream-master
#   python3 extensions/agi/bin/rotate.py spawn --post council-streaming-suite
#   python3 extensions/agi/bin/rotate.py spawn --post shael
#   for d in director-g18.1 director-g18 director-g9 director-g10; do
#     python3 extensions/agi/bin/rotate.py spawn --post "$d"
#   done
# Directors then dispatch pi parents via unified workflows (OpenRouter), not Grok seats.
```

If engine cannot run: leave posts as committed; a live box applies rows at next rotate/heal pass.

## Do NOT
- Push to season2/main or core/season2/main
- Seat parents/kids on Grok
- Merge to streaming-suite/main until season rollover
