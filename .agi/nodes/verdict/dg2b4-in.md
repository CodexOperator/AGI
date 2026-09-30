---
id: verdict:dg2b4-in
mint_id: b496a6d5970b4c89bf30278b8ba50b8a
type: verdict
parents:
  - experiment:dg2b4-in-baseline
  - hypothesis:core-write-hunks-each-get-a-named-disposition
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-in-baseline
scaffold_hash: 4d0f2b29da1274b1
season: 2
title: "input: proved -- 12/12 core write.py hunks named: 9 row-by-NAME -> W1a (semantics, not the write.py resolver), 3 profile_sync -> bundle 5, 0 on trunk"
town: core
verdict: proved
---
# verdict:dg2b4-in

## Verdict: proved (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-in-baseline) | decided by |
|---|---|---|
| core made 12 write.py hunks since 8e4b4c286 | TRUE: +123/-17, 12 `@@` hunks (merge-base re-verified 8e4b4c286, core tip fca147fe1) | `git diff 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/write.py \| grep -c '^@@'` = 12 |
| every hunk carries exactly one named disposition | TRUE: 9 absorbed -> goal:g4.18.5.1 (hunks 2-7, 10-12 = a4b077aba's +108/-17 exactly), 3 rejected -> bundle 5 (hunks 1, 8, 9 = profile_sync, +15/-0); 0 already on trunk (grep = 0) | hunks.tsv, 12 rows, one disposition each |
| no disposition names a leaf that does not exist (falsifier 2) | TRUE: goal:g4.18.5.1 and goal:g7.16.1.4 (whose Out of scope names profile_sync) exist at HEAD | `git grep -l '^id: goal:g4.18.5.1$' HEAD -- .agi/nodes/goal` = 1 file |
| read-only on core | TRUE: git diff / show / ls-tree only; apply --check ran on a /tmp copy of trunk | this run |

Every bundle-4 row except W1a (goal:g4.18.5.1) consumes 0 hunks; W1a absorbs the row-by-NAME SEMANTICS, not the write.py resolver (its Falsifier 2 wants one row-index def, in node_writer). CORRECTIONS: goal:g7.16.1.4's Base bullet and Out of scope say "write.py +125": 125 is a4b077aba's changed-line total (108+17); the range is +123/-17 (140 lines). Hunk 9 is the one hunk that no longer applies on trunk (context = the unpark tail, write.py:2385-2396), so bundle 5 ports it after W1b and W3 B3.
