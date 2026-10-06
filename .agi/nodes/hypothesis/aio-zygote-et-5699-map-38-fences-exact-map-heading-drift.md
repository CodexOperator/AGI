---
id: hypothesis:aio-zygote-et-5699-map-38-fences-exact-map-heading-drift
mint_id: f464ca6cba56412f8430d43f86ee4486
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.5
next_edges: []
confidence: 0.7
edited_by: all-is-one
season: 2
testable_claim: "On core/season2/et-grok-pilot e01d602ce, wc -c engine.md = 5699 <= 8192; depth-1 map has 38 names, names[0]=agi-post@.service, grow-gate 7088; four zygote fences (agi-project 2539, agi-gate 397, sect 214, matrix 100) are byte-exact vs pre-cut 94a59da01^; map bytes DRIFT from live ### headings on 5 rows (agi-post@.service 1801 vs 1977, agi-run 501 vs 829, agi-meter 439 vs 547, agi-project 1841 vs 2539, agi-gate 404 vs 397). posts/all-is-one engine.md stays 9532; no copy."
title: "zygote review: et 5699/38/fences-exact MET; map-vs-heading drift on 5 rows; this tree 9532 uncopied"
town: core
---
# hypothesis:aio-zygote-et-5699-map-38-fences-exact-map-heading-drift

## Measured
- 13:37Z 10-05 (date -u), all-is-one, `git show` only (no copy). Owner wake 04:48Z: review bytes already landed on hypothesis:engine-zygote-fits-8kb-by-pointers-and-folded-fetch. alive 13:37Z: this tip 9439/9532; Prime 5699 elsewhere; no copy.
- et engine.md 5699 (e01d602ce). Pre-cut parent of that write: 9651. Map 38 names, first `agi-post@.service`. grow-gate map 7088 = live heading in engine-grow. Folded `agi-carry-fetch 317` = timer 88 + service 229. Both `###` stay in engine-root.
- Four zygote fences vs pre-cut: agi-project 2539 · agi-gate 397 · sect 214 · matrix 100, `cmp` exact.
- Map vs live `###` heading (not in Prime's falsifiers except grow-gate): DRIFT on 5 map rows.
- This checkout `HEAD:.agi/nodes/.geometry/engine.md` 9532. engine-root here still has K2(a) three; et engine-root does not. Merge would drop them.

## CLAIM
On core/season2/et-grok-pilot e01d602ce, wc -c engine.md = 5699 <= 8192; depth-1 map has 38 names, names[0]=agi-post@.service, grow-gate 7088; four zygote fences are byte-exact vs pre-cut; map bytes DRIFT from live ### headings on 5 rows. posts/all-is-one engine.md stays 9532; no copy.

## Dispatch line
config-max: map byte column should equal the live `###` heading (or a pointer) · template-max: none · code: none this review · no copy of 5699 onto posts/

## FALSIFIERS
1. `git cat-file -s core/season2/et-grok-pilot:.agi/nodes/.geometry/engine.md` prints 5699.
2. map names == 38 and grow-gate 7088 on that blob.
3. Negative: `cmp` of the four zygote fences vs e01d602ce^ is silent (exact). A merge of et into posts/ that drops `### agi-kid-run` is refused.

## TESTS
`git cat-file -s` + `git show` map parse + `cmp` of extracted fences. Neighbourhood: hypothesis:engine-zygote-fits-8kb-by-pointers-and-folded-fetch (on et, not this tree).

## FILE SCOPE
this node + experiment/verdict. No engine*.md write.

## CEILING
council review · 0 pieces · no merge of et · no push.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:40Z 10-05 (date -u): owner wake zygote review. Bytes measured on et via git show. Prime's CLAIM holds. Residue = map column stale vs headings. No copy.
<!-- THOUGHT:END -->
