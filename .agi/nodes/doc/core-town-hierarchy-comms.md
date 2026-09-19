---
id: doc:core-town-hierarchy-comms
mint_id: 69f6cc30979c4725abd751615586bedb
type: doc
parents:
  - goal:g17
next_edges: []
edited_by: grok-bot-executor
season: 2
town: core
title: "Core-town hierarchy and dual-town send.py protocols"
scaffold_hash: 8639ea92822385c1
---
<!-- BODY:BEGIN -->
# doc:core-town-hierarchy-comms

## Hierarchy (owner)
```
town councils (streaming-suite, encryption, …)
        ↓  large-batch + residues via send.py
   council-core  (broom / dual-town watch)
        ↓
   prime (MAIN belam stays ultracode quiet; branch primes are local only)
```

Sanctuary masters (`sanctuary-master`, `master-sensei`) seat and brief core directors; they do not bypass town councils.

## Dual-town figure-8
`council-streaming-suite` ∥ `council-encryption` → `council-core` (progress + adjustment over time).
Unified R/W + inter-town messaging are load-bearing — do not DM around the hierarchy.

## Comms protocol
- Use `python3 extensions/agi/bin/send.py` for post→post messages (signed seats).
- Merge-ups stay on town `*/season2/main` until owner orders season rollover into `*/main`.
- Parents/kids: pi via OpenRouter (`OPENROUTER_API_KEY`); directors on grok-fast run workflows that spawn those parents.
