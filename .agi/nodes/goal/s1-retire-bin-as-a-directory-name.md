---
id: goal:s1
mint_id: 7ab72d5c06424296a1c4c3456e48b0e0
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S1
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S1: Retire `bin/` as a directory name"
---
**Every engine entry point is a script, not a binary.** `extensions/agi/bin/`
holds fifteen `.py` files with shebangs, plus `driver.sh` alongside in the
parent. Nothing in it is compiled and nothing in it is a binary.

The name has a measured cost: **GitNexus excludes any directory called `bin/`
by default**, so it indexes zero symbols for all fifteen — verified after a
fresh reindex, against a working control probe on `src/`. That is the half of
the engine where every 2026-08 change landed, and it is why the engine census
had to be seeded from `git ls-files` instead of the code index.

Rename to something that describes what is there — `cmd/`, `tools/`, `scripts/`
— and take the opportunity to reconsider the layout as a whole rather than
doing a one-word rename. Fifteen flat scripts with three separate generators
among them (`snapshot-goals`, `snapshot-build-site`, `decompose-engine`,
`level3`) have a structure worth making explicit.

**Not a cheap change.** `driver.sh`, `dispatch.py`, the hooks, the skill, the
tests and every one of the 27 census nodes reference these paths; `zoom.py`'s
`--level` aliases are invoked by `dispatch.py` by path. Do it as a deliberate
pass with the census re-run afterwards, and confirm GitNexus actually picks the
directory up before committing to the churn — the exclusion is inferred from
behaviour, not from a documented setting.