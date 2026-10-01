---
id: verdict:dg2mvp-g60
mint_id: 163e71213bde4f0198a1a71b71e14a10
type: verdict
parents:
  - experiment:dg2mvp-g60-check
  - hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g60-check
  - experiment:dg2-g60b-main-live
scaffold_hash: a97aa1972bd97af6
season: 2
title: "Row 60 post-build LIFTED to proved 0.9: disproved at edb74b29e (bare-name stop, rc 5, scope + orphan survived); after the fork b30042219 every exit path stops <unit>.scope and leaves 0 units, 0 orphans on MAIN"
town: core
verdict: proved
---
# verdict:dg2mvp-g60

## Verdict: proved (0.9) -- LIFTED 13:4xZ 10-01 after the fork landed (b30042219)
Row 60's claim (a workflow stage stops its own scope on every exit path) now holds on MAIN: experiment:dg2-g60b-main-live -- normal / wall / error each stop `<unit>.scope` rc 0, unit gone, orphan dead right after return; a no-orphan exit answers rc 5 silently; 0 leftover units or orphans. The fix that made it true is hypothesis:g73360-b-stage-scope-stop-names-the-dot-scope-unit (verdict:dg2-g60b, proved 0.92). The live-mur half of SM's bar (no recursive grep of MAIN by a reviewer) stays bytes-only: the NEVER grep -r line is in both prompts and the .js; no mur was observed live. Not 0.95 for that reason.

## At edb74b29e (the disproof this lift supersedes)
Disproved on the live measurement, on the one conjunct that matters. Everything the review chain checked is true by bytes (CLAIM 2 and 3, F4/F5, ceilings, 6 test files green: 12+12+9+4+11+73), but CLAIM 1's point -- a stage's named scope is stopped on exit so no orphan outlives it -- does not happen on a real box. `_stop_stage_unit` runs `systemctl --user stop <unit>` with the bare unit name; `systemd-run --scope --unit=X` creates `X.scope`, and a bare name resolves to `X.service`, so every stop exits 5 ("Unit X.service not loaded"), prints the one stderr line and does nothing. Measured on all three paths (normal exit, wall kill, error): the scope and its orphan (`g60orphan`, comm + cwd checked) survived after the stage returned; stopping `X.scope` by hand killed the orphan in 1 s. The suite is blind to it because the fake systemctl accepts any name and :260 pins the bare name.

Not measurable as asked: the claude-code lane executes nothing in workflow.py (the `_run_stage_proc` seam is the pi adapter's), so pi-free was used (0 USD); the one real pi stage had no provider key in the tmp root (error path, no orphan to leave); no merge-up-review STARTED after the landing, so the live "no recursive grep" half is unobserved -- the rendered review and verify prompts do carry the line (quoted in experiment.md).

Corrective: a one-token fix (`.scope`) plus a fake systemctl that refuses a bare name like the real one (corrective.md). The wall path's 30 s bounded read worked (46 s total), so no hang.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
lifted disproved:0.92 -> proved 0.9 on SM's order (13:41Z 'lift dg2mvp-g60'): the claim it judged is now true on MAIN after the fork g73360-b landed as b30042219 (experiment:dg2-g60b-main-live, run by DG2 13:4xZ); the edb74b29e disproof stays in the body and the grid. Live-mur half still bytes-only.
<!-- THOUGHT:END -->
