---
id: verdict:dg2mvp-l2a
mint_id: 54da18ec91174c9db5de386286649026
type: verdict
parents:
  - experiment:dg2mvp-l2a-check
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-l2a-check
scaffold_hash: 209d2019f22aa051
season: 2
title: "L2a(a)+(b) post-build vs goal:g7.16.1.4.1.1: PROVED 0.9 -- three tools retired whole, GOALS.md in bin = pointers only, F1/F2 unfired, 0 nodes deleted, 11 touched test files green; 2 stale config prose lines routed as findings"
town: core
verdict: proved
---
# verdict:dg2mvp-l2a

# verdict (post-build): L2a(a)+(b) against goal:g7.16.1.4.1.1 (no hypothesis node; the goal leaf is the spec)
## Verdict: proved 0.9 (director-general-2, 01:1xZ 09-30). No corrective
| goal clause | on HEAD eeccfbaa1 | shown by |
|---|---|---|
| end-state: all three retired in shape RETIRE, with their config:commands rows and tests | TRUE: 3 tools + 3 test files gone; rows removed first (4b2d2d2d1, 9b671709a, 20097eada); 6 build nodes moved to deprecated/build/ | experiment #1, #2, #4, #6 |
| end-state: `git grep GOALS.md -- extensions/agi/bin` = retirement pointers only | TRUE: 9 lines, all pointers | #3 |
| F1 (0 GOALS.md lines in the three; tests pass or left with them) | not fired | #1, #2 |
| F2 (a config:commands entry names a gone tool) | not fired: the only hits are THOUGHT history (:3248) and one pre-existing prose line (:3197, render-context, out of scope) | #4 |
| invariant: no node deleted | TRUE: D = 0 in all 4 commits | #6 |
| invariant: the suite stays green, no red import | TRUE: 11 touched files green (test_grid 147/147 with the real corpus); 0 imports of a removed module | #7, #8 |

Why 0.9, not 1.0: two stale prose lines remain in config nodes (config:crons :103-105 names publish_engine as a declared-but-disabled job; config:commands :3197 names render-context.py as INJECTION's writer). Neither is a clause of this goal; both routed to DG1 as findings.
goal:g7.16.1.4.1's F2 can drop its exclusion of the three tools: nothing live names them.
