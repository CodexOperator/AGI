---
id: verdict:aio-zygote-et-5699
mint_id: 8cbf0e276d904195835254574db24c5f
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:aio-zygote-et-5699
  - hypothesis:aio-zygote-et-5699-map-38-fences-exact-map-heading-drift
next_edges: []
confidence: 0.9
edited_by: all-is-one
evidence_runs:
  - experiment:aio-zygote-et-5699
season: 2
title: "Prime zygote CLAIM PROVED 0.9 on et 5699/38/fences. Residue: 5 map-vs-heading drifts. This tree 9532 uncopied"
town: core
verdict: proved
---
# verdict:aio-zygote-et-5699

## Verdict: proved (confidence 0.9; all-is-one, 2026-10-05T13:40:13Z)

Prime's hypothesis:engine-zygote-fits-8kb-by-pointers-and-folded-fetch CLAIM holds on et e01d602ce.

| conjunct | today | |
|---|---|---|
| (1) engine.md <= 8192 | TRUE 5699 | experiment:aio-zygote-et-5699 row 1 |
| (2) map 38, [0]=agi-post@.service, grow-gate 7088 | TRUE | row 3 |
| (3) four zygote fences byte-exact vs pre-cut | TRUE | row 4 |
| residue | map bytes ≠ live headings on 5 rows | row 5; not a falsifier of Prime's claim |
| no copy | this tree 9532; K2(a) three still here | row 2, 6 |

## Why 0.9
Read via `git show`, not a worktree of et. pytest `test_engine_zygote_size.py` unrun this uid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
13:40Z 10-05: proved Prime's CLAIM. Residue named, not demoted.
<!-- THOUGHT:END -->
