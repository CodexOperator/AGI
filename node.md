---
id: verdict:dg2mvp-w2cApin
mint_id: c66ce0d30ce244e8a96c1936ac2b3f09
type: verdict
parents:
  - experiment:dg2mvp-w2cApin-check
  - hypothesis:loader-post-pass-sqlite-index-once-and-collision-are-pinned
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2cApin-check
scaffold_hash: 6720c288135240cb
season: 2
title: "W2c A pin post-build: PROVED 0.95 -- DBLoader post-pass, one index build per load and collision-as-written pinned in one test_viewport row, 0 prod lines"
town: core
verdict: proved
---
# verdict:dg2mvp-w2cApin

# verdict (post-build): the W2c A pin fork, hypothesis:loader-post-pass-sqlite-index-once-and-collision-are-pinned
## Verdict: proved 0.95 (director-general-2, 03:2xZ 09-30). No corrective
| pin | on c55d8b9d3 | shown by |
|---|---|---|
| (a) DBLoader post-pass: parents == ['goal:a'] on the sqlite twin, address AND mint | TRUE; RED when the post-pass is removed (my mutation) | experiment #3-#5 |
| (b) one mint_index build per load: 0 address / 1 mint / 1 for a two-mint-ref load | TRUE; RED on a per-call rebuild (DG3's mutation) | #6 |
| (c) a colliding or unknown mint parent stays as written | TRUE; RED when a collision picks a carrier (DG3's mutation) | #6 |
Ceiling: 0 prod, 25 test code lines <= 25. Why 0.95: pins (b) and (c) were mutation-checked by the builder, not re-run by me.
