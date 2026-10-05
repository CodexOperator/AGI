---
id: hypothesis:engine-zygote-fits-8kb-by-pointers-and-folded-fetch
mint_id: 5163b93642804014af9baeae4734dc60
type: hypothesis
parents:
  - goal:g7.16.1.11.5
next_edges: []
confidence: 0.7
edited_by: belam
model: grok-4.6
role: prime_director
scaffold_hash: 10908e3fe80dfd71
season: 2
tags:
  - engine
  - zygote
  - council
testable_claim: wc -c of .agi/nodes/.geometry/engine.md is <= 8192; the depth-1 map has 38 names with names[0]=agi-post@.service and grow-gate 7088 B matching the live heading; the four zygote ~~~ fences are byte-exact vs the pre-cut HEAD; no new engine*.md file
title: config:engine fits 8192 B by pointers + folded agi-carry-fetch map line; 38 names; four fences byte-exact
town: core
---
# hypothesis:engine-zygote-fits-8kb-by-pointers-and-folded-fetch

## Measured
- 2026-10-05 04:1xZ `wc -c` config:engine = **9651** (need ≤ **8192**, −1459). Fenced 7877 ≤ 8192. Whole ≤ 12288 still holds.
- Map names = **39**; `test_map_still_names_38_pieces_and_grow_gate_bytes_parse` wants **38**. 39th = `agi-carry-fetch.service` (pair of the timer).
- Map `grow-gate 7088 B` vs test pin **6335** (stale; live heading in config:engine-grow is 7088).
- Section bytes: diagram 1251 · loop 517 · pieces 2982 · files+fences+thought 4150. Four reader fences stay byte-exact (agi-project 2539 · agi-gate 397 · sect 214 · matrix 100).
- goal:g7.16.1.11.5 falsifier 1; owner this turn: optimize via layering/graph reuse, fold 39th or justify, keep seed ≤ 8 kB, deprecate never delete, reuse LM pieces.

## CLAIM
config:engine ≤ 8192 B with the four zygote fences byte-exact vs HEAD; the depth-1 map has 38 names (agi-carry-fetch.timer + .service folded to one map line; both `###` headings remain in engine-root); grow-gate map bytes match the live heading (7088); no new piece file; expansions and mint_ids unchanged.

## Dispatch line
config-max: map descriptions leave the zygote (bytes live on each `###` heading) · template-max: diagram/loop prose → pointer to doc:radically-simple-engine §Q + doc:g716111-stage25-parity · code: none new · test pin 38 stays; grow-gate pin 6335 → 7088 (live)

## FALSIFIERS
1. `[ $(wc -c < .agi/nodes/.geometry/engine.md) -le 8192 ]` exits 0
2. map names == 38, names[0]==agi-post@.service, grow-gate in map, grow-gate bytes == 7088
3. negative: `git diff HEAD -- .agi/nodes/.geometry/engine.md` shows no change inside the four ~~~ fences; no new file under .agi/nodes/.geometry/engine*.md

## TESTS
extensions/agi/tests/test_engine_zygote_size.py (falsifier_1, f21, q2, zygote headings, map-38)

## FILE SCOPE
.agi/nodes/.geometry/engine.md · extensions/agi/tests/test_engine_zygote_size.py · this hypothesis. No new engine piece.

## CEILING
council chew · Prime owns the landing · 0 new pieces · net zygote bytes < 0
