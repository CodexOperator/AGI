---
id: hypothesis:box-logs-dir-resolves-from-one-config-cell
mint_id: 1896599e76554d3b84559bb9297f1e07
type: hypothesis
parents:
  - goal:g6.49
  - hypothesis:cron-layer-keeps-its-disk-footprint-bounded
next_edges: []
edited_by: director-engine
scaffold_hash: 94dac3cecacc1acf
season: 2
testable_claim: crons.logs_dir(root) reads logs.dir (default {home}/logs, value unchanged); grid.py:1768 and rotate.py:6911 call it; {logs} renders from it; no engine literal names the dir
title: "The box logs dir resolves from ONE config cell (logs.dir) so moving every log is one cell edit (assigned: director-engine)"
town: core
---
# hypothesis:box-logs-dir-resolves-from-one-config-cell

## Why this exists
Prime [decision] 2026-09-27 22:2xZ, relaying the OWNER (verbatim on town:local-maxxing): a new disk is mounted for LOGS and sequential
scratch ONLY -- never worktrees or test tmp; each writer moves by a config cell/symlink WITH its writer, never by a live mv under a running
writer. The move plan is thought-master's (box/guard); "DE: the engine log-path cells are yours". This round builds the cell, not the move.

## Measured
- `extensions/agi/bin/crons.py:453-457` `logs_dir()` -- "the ONE place `enforce_log_caps` looks" -- returns the literal `Path.home() / "logs"`.
- `extensions/agi/bin/grid.py:1768` the grid-sync log bypasses it: `Path.home() / "logs" / f"grid-sync-...log"`.
- `extensions/agi/bin/rotate.py:6911` reaper-log discovery bypasses it: `expanded = Path.home() / "logs"`.
- `.agi/nodes/.geometry/crons.md:62` the crontab already renders a `{logs}` placeholder; `.agi/config.json` `logs` holds cap_mb / rotations /
  alerts_file / also_manage but NO directory cell. Box io PSI some avg60 ~61 at 22:3xZ (the TMM.306 gate needs < 50).

## CLAIM
The box logs directory resolves from ONE config cell, `logs.dir` in `.agi/config.json` (value `{home}/logs`: today's path, unchanged by this
round), read by `crons.logs_dir(root)`; grid.py:1768 and rotate.py:6911 call that resolver instead of their literals, and the crontab's `{logs}`
renders from it -- so moving every box log is ONE cell edit plus `crons.py apply`, and no engine file names the directory.

## Dispatch line
config-max: `logs.dir` cell (value `{home}/logs`) in the existing `logs` block · template-max: none (crons.md already writes `{logs}`) ·
code: the resolver reads the cell + the two call sites stop hard-coding it. NEVER change the cell's VALUE (the move is thought-master's).

## FALSIFIERS
1. `git grep -n 'home() / "logs"' -- extensions/agi/bin` still hits outside the resolver's default.
2. With `logs.dir` set to a tmp dir in a tmp graph, `crons.logs_dir`, the grid-sync log path, reaper-log discovery or the rendered `{logs}`
   crontab line names a path outside that tmp dir.
3. With the cell ABSENT, any of them differs from today's `{home}/logs` (the default must be byte-identical behaviour).

## TESTS
New `extensions/agi/tests/test_logs_dir_resolves_from_one_cell.py` (falsifiers 2 and 3, tmp graphs only) + neighbourhood
test_crons.py test_crons_log_cap_declared_scope.py test_crons_disk_footprint_bounds.py test_bin_help_smoke.py (timeout 900, --basetemp under
/tmp, env -u TMUX -u TMUX_PANE). Never a live crontab, pane, seat or real `crons.py apply`.

## FILE SCOPE
extensions/agi/bin/crons.py · extensions/agi/bin/grid.py · extensions/agi/bin/rotate.py · .agi/config.json (the ONE new cell) ·
extensions/agi/tests/test_logs_dir_resolves_from_one_cell.py · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 15 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut.
PARENT: paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit.
ANON: no user name, home or repo path value, mount path, host, IP or hardware name in any byte; patterns write <user>.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.667, first version. Prime [decision] 22:2xZ relaying the owner: "DE: the engine log-path cells are yours" (TM owns the move plan). Measured: crons.logs_dir is itself a literal and two writers bypass it, so the directory is not yet a cell; this round makes it one and leaves the value alone -- flipping it is the move, timed with the writers by TM. Queued right after DH.650, the round TMM.306 named first for the next freed slot.
<!-- THOUGHT:END -->
