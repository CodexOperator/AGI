---
id: hypothesis:l4-config-rotations-facts-have-a-reader
mint_id: fa8c27a579654a7b9b54e1e101ea4051
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 314d1a660932bdf2
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-8: config:rotations `## facts` (0b, L4.125) declares per-fact staleness bounds (rotate.py:3517/:3548 parse a fact→'head'|'permanent' map), but NO reader applies them: the default `{}` makes ANY HEAD move stale for every fact, so the bootstrap block flags permanent facts (paths, names, the prayer) as stale on every commit (reproduced by the review). CLAIM: `rotate.py bootstrap-block` / `next` READ the map: a fact bounded 'permanent' is never marked stale; a fact bounded 'head' is stale only when the recorded head differs from the live one; an unbounded fact takes the DECLARED default (state which; the node `config:rotations` documents it) and the block prints the bound it applied per fact; the fixture test covers all three; the dry-run of bootstrap-block on the real seat prints no stale mark on a permanent fact (paste). FALSIFIER: a permanent fact marked stale after a commit. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (bootstrap-block/facts region ONLY) + its tests; the `config:rotations` node's `## facts` text ONLY if a bound is missing (the node is graph content — use write.py, file-borne). SERIAL on rotate.py behind L4.127, g15-6 and 0b-b (hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one). EXCLUDED: hooks, heal.py, send.py."
title: "config:rotations ## facts staleness bounds have a reader — a HEAD move marks only the facts bounded by head as stale"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-config-rotations-facts-have-a-reader

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-8: config:rotations `## facts` (0b, L4.125) declares per-fact staleness bounds (rotate.py:3517/:3548 parse a fact→'head'|'permanent' map), but NO reader applies them: the default `{}` makes ANY HEAD move stale for every fact, so the bootstrap block flags permanent facts (paths, names, the prayer) as stale on every commit (reproduced by the review). CLAIM: `rotate.py bootstrap-block` / `next` READ the map: a fact bounded 'permanent' is never marked stale; a fact bounded 'head' is stale only when the recorded head differs from the live one; an unbounded fact takes the DECLARED default (state which; the node `config:rotations` documents it) and the block prints the bound it applied per fact; the fixture test covers all three; the dry-run of bootstrap-block on the real seat prints no stale mark on a permanent fact (paste). FALSIFIER: a permanent fact marked stale after a commit. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (bootstrap-block/facts region ONLY) + its tests; the `config:rotations` node's `## facts` text ONLY if a bound is missing (the node is graph content — use write.py, file-borne). SERIAL on rotate.py behind L4.127, g15-6 and 0b-b (hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one). EXCLUDED: hooks, heal.py, send.py.
