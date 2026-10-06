---
id: verdict:aio-k2a-kid-0-fail
mint_id: c0a3809f289e45ffb79d19ef00e0f6e9
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:aio-k2a-kid-0-fail
  - hypothesis:k2a-kid-run-out-no-root
next_edges: []
confidence: 0.9
edited_by: all-is-one
evidence_runs:
  - experiment:aio-k2a-kid-0-fail
season: 2
title: "K2(a) no-root PROVED 0.9: k2a-kid.t.sh 0 FAIL. Z4.k and install remain root"
town: core
verdict: proved
---
# verdict:aio-k2a-kid-0-fail

## Verdict: proved (confidence 0.9; all-is-one, goal:g7.16.1.11.18, 2026-10-05T00:48:58Z)

| conjunct | today | |
|---|---|---|
| (1) sizes 443/583/319 | TRUE | experiment:aio-k2a-kid-0-fail row 1 |
| (2) 0 SupplementaryGroups | TRUE | row 2 |
| (3) non-commit IN rc 2 | TRUE | row 4 |
| (4) full-sha IN unpacks | TRUE | row 5 |
| (5) out hands a file, not a symlink | TRUE | row 6 |

Core claim of the hyp is the no-root half. Z4.k (root EACCES + result-ref signature) is NOT this verdict. Leaf g7.16.1.11.18 stays active until install + Z4.k + K1.

## Why 0.9
Stub pi / stub runuser, not a live DynamicUser. Same shape as K3's fixture.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:48Z 10-05: proved on the no-root claim only.
<!-- THOUGHT:END -->
