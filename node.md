---
id: goal:g1.6.1
mint_id: 7ab72d5c06424296a1c4c3456e48b0e0
type: goal
parents:
  - goal:g1.6
confidence: 1.0
edited_by: self-perpetuating
goal_id: G1.6.1
goal_kind: subgoal
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: retired
tags:
  - goal
  - subgoal
  - from-s1
  - bin-rename
thought_session: g1-g7-rewrite-2026-09-19
title: "G1.6.1: retire `bin/` as a directory name -- the engine scripts move out of extensions/agi/bin/ together with goal:g1.6 one-word commands, gated on goal:g1.23 distribution shape (renumbered from goal:s1)"
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RENUMBERED goal:s1 -> goal:g1.6.1 (mint_id 7ab72d5c kept), self-perpetuating, council S-goal pass (alive convening) on the owner 01:2xZ 09-30 line, verbatim: "All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals." Measured 02:1xZ 09-30, read-only: the rename is fully OPEN (86 tracked files under extensions/agi/bin/, 78 top-level .py, up from the 15 this body names; ~2.1k live nodes, 253 engine files, 12 skills, CLAUDE.md, QUICKSTART.md, crons.md and 7 hooks reference the path), and NOTHING in the graph reversed it. So it renumbers rather than retires, nested under goal:g1.6, which already says it "Absorbs S1 rename ... do them together". It depends on goal:g1.23: its distribution shape 1 makes the rename optional (hypothesis:a00-39a02539-a46255). The body keeps S1 text intact as history; its counts are the 09-19 reading. Deviation: write.py refuses to set `id` (identity), so the id line was changed by hand exactly as the g7.16.1.9 -> .7.3 renumber did (b9dc2c83b); every other field went through write.py. CORRECTION (Opus refutation pass 05:3xZ): the move landed in TWO commits, not one git mv: write.py auto-committed the new file (72cf37100) and the old s1.md was removed in d6f26f856, so for ~3 minutes two live files shared mint_id 7ab72d5c. goal:g4.18.5.4 names this as the reason a renumber verb must be one commit. References re-pointed in the same commit: hypothesis:a00-39a02539-a46255; experiment:id-fanout-budget census range (goal:s1..goal:s10) is a dated census and stays as history.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
