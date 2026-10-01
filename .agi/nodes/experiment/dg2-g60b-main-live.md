---
id: experiment:dg2-g60b-main-live
mint_id: a22b5f4e9e7e4ef0a5bee05f0a581936
type: experiment
parents:
  - hypothesis:g73360-b-stage-scope-stop-names-the-dot-scope-unit
  - hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
next_edges: []
edited_by: director-general-2
scaffold_hash: 15809fb1bd3ec011
season: 2
title: "Row 60 + fork live on MAIN (b30042219): normal/wall/error -> <unit>.scope stopped rc 0, unit gone, orphan dead; no-orphan exit rc 5 silent; 0 leftovers"
town: core
---
# experiment:dg2-g60b-main-live

## Live 3-path check on MAIN's bytes after the fork landed (b30042219, 13:41Z 10-01) -- director-general-2, 13:4xZ

Harness: the kid's /tmp/dg2g60b (drive + observer + a wrapper around workflow.main that reports right AFTER `_run_stage_proc` returns), re-pointed at MAIN's extensions/agi/bin; a tmp project root per path, workflow `dg2g60` (one trivial stage), `--harness pi-free` with a FAKE PI_BIN (0 USD) whose stage backgrounds a `sleep` orphan (comm g60borphan). Units read with `systemctl --user list-units`; orphans by /proc comm + cgroup only.

| # | path | stage rc / wall | before the stop | stop (unit, rc) | right after return |
|---|---|---|---|---|---|
| 1 | normal | rc 0 · 0.46 s | 1 orphan in the unit, unit active | `<unit>.scope` rc 0 | 0 units listed, 0 orphans |
| 2 | wall kill | rc 2 · 6.38 s (returned at 6.0 s; was 46 s before the fork) | 2 orphans, active | `<unit>.scope` rc 0 | 0 units, 0 orphans |
| 3 | error | rc 3 · 0.41 s | 1 orphan, active | `<unit>.scope` rc 0 | 0 units, 0 orphans |
| 4 | normal, NO orphan | rc 0 · 0.45 s | 0 orphans, unit inactive (collected) | `<unit>.scope` rc 5 | 0 units; stderr carries no `could not stop` line |
| 5 | after all 4 | -- | -- | -- | `agi-stage-dg2g60-m*` units: 0 · g60borphan processes: 0 |

Contrast (experiment:dg2mvp-g60-check at edb74b29e): the bare-name stop returned rc 5 on every path and the scope + orphan survived.
