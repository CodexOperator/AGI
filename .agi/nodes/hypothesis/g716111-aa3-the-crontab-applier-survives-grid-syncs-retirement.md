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
- LIVE 10-08 05:2xZ (DG1, trunk tip 3b41d2bc6b; E2 of town:local-maxxing 'Engine rework trajectory', owner 01:4xZ 10-08 'It's already decided'; belam [rule] 05:1xZ placed AA3.10 with DG1, cut FIRST): cron:crons has NO `crons_apply` cell; `grid_sync` is `every_mins: 5, enabled: true, mirror_towns: true` and its rendered line is three `;`-chained steps (`grid.py commit --all --prefix 'cron: '`, `grid.py push-changed`, `crons.py apply --unit-dir ~/.config/systemd/user`), so disabling it alone removes the crontab self-heal. `crons.py` KNOWN_JOBS = (grid_sync, branch_push, engine_push, mail_poll, nudge_sweep); ANY other cadences key with a non-empty `cmd` is a GENERIC job (crons.py:255-262, the maint_gc / graph_metrics / memory_alarm rows are live examples), so `crons_apply` needs NO renderer row and 0 engine bytes. The cell is BOXLESS (see (g)): `crons.py apply` refuses a linked worktree, so it only ever lands in a common-root checkout's crontab, the same reach as grid_sync.
- doc:rse-aa3-land AA3.10: cron:crons `grid_sync` every 5 min ALSO runs `crons.py apply` (the crontab self-heal), so disabling grid_sync alone would silently stop the self-heal; `crons.py apply` is gated by require_common_root (refuses a linked worktree) and the live crontab is one per user.
- Interim = its own cadence; target = projection at the trunk tip.

## CLAIM
(V3) after grid_sync is disabled, a hand edit of the live crontab is undone within 5 minutes by a `crons_apply: every_mins 5` job that runs `crons.py apply` on its own (0 engine bytes: one cell); the target shape is that the crontab follows the trunk (agi-project.path already fires on the trunk ref's log), so the crontab becomes one more projection of cron:crons at the trunk tip with no polling.

## ROUND SHAPE (DG1 cut 10-08, E2a): this is the FIRST step of AA3.10 and the precondition for the rest: it lands BEFORE grid_sync is disabled, so the self-heal never has a gap.
- DG2 (lane FIRST, test-only, ONE new file, python allowed this season, no pi): a render test over a fixture cron:crons: (a) with `grid_sync: enabled: false` and NO `crons_apply` cell the rendered managed block holds no `crons.py apply` line (the witness: the self-heal is gone); (b) with the cell the block holds exactly ONE line `*/5 * * * * cd <root> && python3 <engine_root>/extensions/agi/bin/crons.py apply --unit-dir <udir> >> <log> 2>&1` and every other managed line is unchanged; (c) `apply` twice is byte-identical; (d) with a FAKE `crontab` binary first on PATH (a file-backed table), a hand-edited line is undone by one `crons.py apply` and a hand-ADDED line outside the managed markers is left alone; (e) the cell has NO `box:` key and renders on EVERY box, including with `AGI_BOX` unset and no `default_box` cell (RE5: `_on_this_box` crons.py:793-805 FAILS CLOSED on an unresolved box for any job that names a box, the render then writes only the refusal comment and `cmd_apply` REPLACES the managed block, so a box-gated self-heal erases itself on the next `crons.py apply` from an unresolved shell and, after E2b, nothing re-adds it); (f) the cell's `cmd` carries `--unit-dir`, so `crons_live: false` still stops the units (the lane puts a FAKE `systemctl` first on PATH: `_apply_systemctl` crons.py:1061-1096 calls the real one when --unit-dir is passed), and the rendered line carries the LITERAL `$HOME/.config/systemd/user` (cron expands it), so (b) matches that string, not an expanded path; (g) RE5 RULING (DG1; replaces the why_box ruling of re-cut 2, because a boxless cell makes it moot): the cell is BOXLESS, exactly the reach of the grid_sync line it replaces (grid_sync has no box key and renders on any box that runs `crons.py apply`); my earlier `box: local-town` NARROWED the self-heal and made it erasable. A mutant that restores `box: local-town` (with a why_box) makes (e)'s unresolved-box row RED; a `box` key WITHOUT `why_box` is flagged by `crons.py audit` (:1455) and a blank one raises CronsError (:220-227), two separate assertions, kept as mutants of the cell. Mutants: the cmd without `--unit-dir`; `box: local-town` restored (the unresolved-box row), `why_box` dropped from a boxed cell (audit names the job), `why_box` blank (CronsError); every_mins 5 -> 50; enabled false; the box gate dropped; the cell's cmd chained with `grid.py commit`; and, on crons.py itself, grid_sync's own `;` between its commit step and its apply step written `&&` (the one chain that exists; the single-command cell has none to break). The fixture keeps `repo_root == engine_root` (a generic cell can only say `{repo_root}`, the rendered line shows the engine path), so the lane's `<engine_root>` pattern and the cell agree by construction. The cell is boxless, so it does NOT narrow the self-heal compared with grid_sync (RE5, (g)).
- DG4 (build AFTER lane B, belam): ONE commit on the live tip adding the `crons_apply` cadence to .agi/nodes/.geometry/crons.md (the cell: `every_mins: 5`, `enabled: true`, NO `box:` key (and so no `why_box`), `cmd: python3 {repo_root}/extensions/agi/bin/crons.py apply --unit-dir $HOME/.config/systemd/user`; and the 'self-reapply property' prose updated to name it; grid_sync's own apply step STAYS until the switch round). Prime-owned cell: DG1 judges, SM lands, belam's `crons.py apply` is the host act that installs it.
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
