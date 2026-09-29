---
id: verdict:dg2b4-w2c
mint_id: 490d1e34a02d412796f2b44f2ac92602
type: verdict
parents:
  - experiment:dg2b4-w2c-baseline
  - hypothesis:every-link-reader-resolves-mint-ids
next_edges: []
confidence: 0.55
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2c-baseline
scaffold_hash: cde818d2af453dfa
season: 2
title: "W2c: lean disproved at 55 -- 17 address-only reader modules (~40 sites, 3 families); 15/17 break on a mint-id twin; fits 80 lines only split by family"
town: core
verdict: inconclusive_lean_disproved:55
---
# verdict:dg2b4-w2c

## Verdict: inconclusive_lean_disproved:55 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w2c-baseline) | decided by |
|---|---|---|
| (1) the enumerated readers all call the resolver | FALSE today: 0 of 17 reader modules; no resolver exists (g4.18.6.1 unbuilt) | the enumeration grep (readers.md) prints only resolver-routed sites + the 3 W2c rows XPASS; the 14 other reader modules need their own rows |
| (2) a mint-id fixture = its address twin in output | FALSE today: 15 DIFF / 17 probed readers | test_viewport.py / test_links.py / test_level3.py ::test_w2c_* (strict xfail) + the twin probe re-run over all 17 |
| (3) the dual accept is marked for retirement by goal:g4.18.6.4 | FALSE today (nothing to mark) | a grep for the dual-accept marker naming goal:g4.18.6.4 in the resolver |
Lean: 17 modules / ~40 sites in 3 families under a <= 80-line, <= 60-test-line ceiling only fits if families A (one post-pass at graph_core/loader.py:90) and B/C (~13 private fm parses) are split into rounds, which the ceiling itself prescribes -- one round will not close (1)+(2).
CORRECTION: the hypothesis's reader list is wrong in two places: hierarchy.py reads no parents/next_edges (test_hierarchy.py gets no row) and level3.py is a parents WRITER (:1127) with one map reader (:929). The goal's "`links.py links` resolves 5035, 0 broken" is not a parents gate: `links` resolves link_ref/payload_ref only and stays 0 broken on a mint-id twin.
