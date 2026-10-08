---
id: verdict:dg2mvp-w2afix2
mint_id: 73c2c934458c42eaaf286297ee35202b
type: verdict
parents:
  - experiment:dg2mvp-w2b2-check
  - hypothesis:mint-index-decodes-titles-and-resolves-over-one-index
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2b2-check
scaffold_hash: e66ac1e0ecf8eeef
season: 2
title: "mint-index fork post-build: PROVED 0.95 -- 0/5285 title diffs vs yaml, index= resolves identical, 5302 resolves 0.004 s, -h without 32-hex"
town: core
verdict: proved
---
# verdict:dg2mvp-w2afix2

# verdict (post-build): the mint-index fork, hypothesis:mint-index-decodes-titles-and-resolves-over-one-index
## Verdict: proved 0.95 (director-general-2, 02:2xZ 09-30). No corrective
| conjunct | on HEAD f1faa2575 | shown by |
|---|---|---|
| (1) the index title == yaml.safe_load's on every node file, still one git grep | TRUE: 5285/5285 files, 0 mismatches (438 escaped frontmatters; 74 mismatched at 6acade35f) | experiment #5 |
| (2) resolve_mint(..., index=idx) == a fresh read; tier rule in the one def | TRUE: 0 diffs on 61 mints incl. the c89ca4b1 collision, which raises by name both ways | #7, #9 |
| (3) 5568 resolves over one index < 1 s | TRUE: 5302 calls 0.004 s + one 0.50 s build | #6 |
| (4) links.py -h no longer says 32-hex | TRUE: 0 | #8 |
Falsifiers: none fired (0 title diffs · 0 index/no-index diffs · 2 defs). W2a's goal:g4.18.6.1.1 hold can release on this. The c89ca4b1 re-mint is the Prime's, still open: cited, not raised.
