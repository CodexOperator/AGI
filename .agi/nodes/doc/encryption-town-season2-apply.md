---
id: doc:encryption-town-season2-apply
mint_id: 420b50e840bf40c1b8734c00093c7ef8
type: doc
parents:
  - goal:g15.25
next_edges: []
edited_by: grok-bot-executor
season: 2
town: encryption
title: "Apply sheet: encryption-town/season2 seating and VPS commands"
scaffold_hash: c7067e90f5ee49b0
---
<!-- BODY:BEGIN -->
# doc:encryption-town-season2-apply

## Branch
`encryption-town/season2/main` only. Do **not** merge to `encryption-town/main` until full chain buildup.

## Seats landed (names → models)
| seat | model | notes |
|---|---|---|
| encryption-prime | grok-4.6 | branch prime |
| encryption-master | grok-4.3 | owns g15.25 chain |
| council-encryption | grok-4.6 | reports to council-core |
| director-enc-sealed-box | grok-fast | sealed-box / X25519 |
| director-enc-lockdown | grok-fast | enc_scheme / lockdown under g17 |
| sanctuary-master | grok-4.3 | unquiet; seating brief |
| master-sensei | grok-4.3 | unquiet |
| council-core | grok-4.6 | dual-town watch |
| director-core-g15 / g17 | grok-fast | core under sanctuary |

## VPS / pi apply
```bash
cd /path/to/AGI
git fetch origin && git checkout encryption-town/season2/main
git pull --ff-only origin encryption-town/season2/main
# If engine live:
#   python3 extensions/agi/bin/write.py …  # prefer for further edits
# Spawn seats from config:posts (clear quiet already applied in graph).
# export OPENROUTER_API_KEY=…   # parents/kids only on pi
```

## Chain-first nodes
- `hypothesis:enc-sealed-box-comms-x25519` (parent `goal:g15.25`)
- `hypothesis:enc-scheme-lockdown-buildout` (parent `goal:g17`)
- Director brief: `doc:director-brief-enc-sealed-box`
- Sanctuary brief: `doc:sanctuary-master-seating-brief`
