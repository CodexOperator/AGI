---
id: hypothesis:g716111-aa3-the-crontab-applier-survives-grid-syncs-retirement
mint_id: f4991d0baea345ad843ed8b31c57f3ed
type: hypothesis
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: ec6a94d017e1d84f
season: 2
testable_claim: "(V3) after grid_sync is disabled, a hand edit of the live crontab is undone within 5 minutes by a `crons_apply: every_mins 5` job that runs `crons.py apply` on its own (0 engine bytes: one cell); the target shape is that the crontab follows the trunk (agi-project.path already fires on the trunk ref's log), so the crontab becomes one more projection of cron:crons at the trunk tip with no polling."
title: "AA3.10: retiring grid_sync does not lose the crontab self-heal -- the applier gets its own `crons_apply` cadence, then becomes a projection of cron:crons at the trunk tip with no polling"
town: core
---
# hypothesis:g716111-aa3-the-crontab-applier-survives-grid-syncs-retirement

## Measured
- doc:rse-aa3-land AA3.10: cron:crons `grid_sync` every 5 min ALSO runs `crons.py apply` (the crontab self-heal), so disabling grid_sync alone would silently stop the self-heal; `crons.py apply` is gated by require_common_root (refuses a linked worktree) and the live crontab is one per user.
- Interim = its own cadence; target = projection at the trunk tip.

## CLAIM
(V3) after grid_sync is disabled, a hand edit of the live crontab is undone within 5 minutes by a `crons_apply: every_mins 5` job that runs `crons.py apply` on its own (0 engine bytes: one cell); the target shape is that the crontab follows the trunk (agi-project.path already fires on the trunk ref's log), so the crontab becomes one more projection of cron:crons at the trunk tip with no polling.

## Dispatch line
config-max: a `crons_apply` cadence cell on cron:crons (every_mins 5) / template-max: none / code: none for the interim; the projection is the later step.

## FALSIFIERS
AA3.10 V3 a hand edit of the crontab is undone within 5 min after grid_sync's retirement · negative: with grid_sync disabled and no crons_apply cell, the edit is NOT undone (the witness for the cell) · `crons.py show` equals the live crontab after one cycle.

## TESTS
a render test over a fixture cron:crons with grid_sync off and the new cell on (the managed line set is unchanged); one live check on a throwaway crontab line only.

## FILE SCOPE
cron:crons (the cadence cell) · crons.py only if the cell needs a renderer row (it should not: a generic `cmd` row already exists). Never the live crontab beyond one throwaway line.

## CEILING
1 parent · kids <= 1 · 0 engine bytes · regular review. The Prime owns the cell.
