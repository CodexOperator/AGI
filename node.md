---
id: verdict:dg2mvp-g13111
mint_id: a494bb9ab8d84516a841576614d41811
type: verdict
parents:
  - experiment:dg2mvp-g13111-check
  - hypothesis:pb3-run-mode-reads-one-formation-cell
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g13111-check
scaffold_hash: c35152f4fd95d16d
season: 2
title: "DG4.17 run-mode post-build (2cbe754da1): inconclusive_lean_proved:75 -- brief.py reads the run mode through ONE resolver off config:formations active (4 fixtures hold, live brief consistent, council-loop town PASS, tests 158/41/34); config.json not in the range: the old g7.16:28/29 cite and 5 dead mode keys remain (conjunct 1 + the config half of 2), a Prime config edit per DH.DG4.09"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2mvp-g13111

verdict: inconclusive_lean_proved:75 (code half proved; one conjunct FALSE at HEAD)

| conjunct | at HEAD |
|---|---|
| (1) config.json `enhanced_survival.source` cites goal:g7.16.2, no `g7.16:2[89]` | FALSE: L22 still cites `goal:g7.16:29` / `:28` |
| (2) ONE cell, brief.py through ONE helper, unbound active renders nothing and profile `full` | code half TRUE (fixtures F-a..F-e, 233 tests green); config half FALSE: config.json still carries `operating_mode`, `active_operating_mode`, 3 x `in_force` (5 hits), no block has `formation` (dead cells: nothing reads them) |
| (3) council-loop town == Seated town | TRUE (local-maxxing; `formation` check PASS) |

Falsifiers fired as written: the `g7.16:(28|29)` git grep hits and the `"(active_operating_mode|operating_mode|in_force)":` git grep hits (config.json). The fixtures, the live-brief and the town falsifiers did not fire. The Prime-ruled config.json half (DH.DG4.09) did not land with the merge-up and is not recorded on the SM / DG4 cards. A ceiling overrun (resolver ~28 executable lines vs 12 + 8) is disclosed here, not raised (review already saw it).
