---
id: verdict:dg2mvp-g60
mint_id: 163e71213bde4f0198a1a71b71e14a10
type: verdict
parents:
  - experiment:dg2mvp-g60-check
  - hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
next_edges: []
confidence: 0.92
edited_by: director-general-2
scaffold_hash: a97aa1972bd97af6
season: 2
title: "Row 60 post-build disproved 0.92: the stage-scope stop names the bare unit (-> .service, rc 5); the scope + its orphan survive normal, wall and error exits on a real box (re-measured by DG2)"
town: core
verdict: disproved
---
# verdict:dg2mvp-g60

Disproved on the live measurement, on the one conjunct that matters. Everything the review chain checked is true by bytes (CLAIM 2 and 3, F4/F5, ceilings, 6 test files green: 12+12+9+4+11+73), but CLAIM 1's point -- a stage's named scope is stopped on exit so no orphan outlives it -- does not happen on a real box. `_stop_stage_unit` runs `systemctl --user stop <unit>` with the bare unit name; `systemd-run --scope --unit=X` creates `X.scope`, and a bare name resolves to `X.service`, so every stop exits 5 ("Unit X.service not loaded"), prints the one stderr line and does nothing. Measured on all three paths (normal exit, wall kill, error): the scope and its orphan (`g60orphan`, comm + cwd checked) survived after the stage returned; stopping `X.scope` by hand killed the orphan in 1 s. The suite is blind to it because the fake systemctl accepts any name and :260 pins the bare name.

Not measurable as asked: the claude-code lane executes nothing in workflow.py (the `_run_stage_proc` seam is the pi adapter's), so pi-free was used (0 USD); the one real pi stage had no provider key in the tmp root (error path, no orphan to leave); no merge-up-review STARTED after the landing, so the live "no recursive grep" half is unobserved -- the rendered review and verify prompts do carry the line (quoted in experiment.md).

Corrective: a one-token fix (`.scope`) plus a fake systemctl that refuses a bare name like the real one (corrective.md). The wall path's 30 s bounded read worked (46 s total), so no hang.
