---
id: verdict:dg2-g60b
mint_id: e05a26d2a5fd431cb5b472717b030a31
type: verdict
parents:
  - experiment:dg2-g60b-main-live
  - hypothesis:g73360-b-stage-scope-stop-names-the-dot-scope-unit
next_edges: []
confidence: 0.92
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-g60b-main-live
scaffold_hash: fdea896718f7ccb0
season: 2
title: "DG2.G60B proved 0.92: the stage-scope stop names <unit>.scope via mem_cap.scope_unit -- live on MAIN, normal/wall/error leave 0 units and 0 orphans (b30042219)"
town: core
verdict: proved
---
# verdict:dg2-g60b

## Verdict: proved (0.92)
`_stop_stage_unit` stops `mem_cap.scope_unit(unit)` = `<unit>.scope` (the one spelling, mem_cap.py), so the stop takes effect: on MAIN's bytes after the landing (b30042219) the unit is gone and the orphan dead right after `_run_stage_proc` returns on the normal, wall and error paths (stop rc 0 each), and a stage with no orphan (scope already collected) answers rc 5 with no stderr line. CLAIM 1-3 MET; F1-F4 not fired (review: reverting the `.scope` token fails 8 rows, reverting the rc-5 branch fails F13; dispatch.py / heal.py untouched). Not 0.95: rc 5 = "not loaded" is measured on this box, not documented (the man page lists LSB 5 "not installed"); rotate.py:1846 keeps its own `.scope` literal (rotate HELD; a findings row).
