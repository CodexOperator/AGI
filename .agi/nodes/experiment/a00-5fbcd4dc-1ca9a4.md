---
id: experiment:a00-5fbcd4dc-1ca9a4
mint_id: fb060d6e4e3244b380a600bdfb0cd3e7
type: experiment
parents:
  - hypothesis:l4-spawn-paths-export-the-reaper-knob
next_edges: []
confidence: 0.85
edited_by: a00-9dd6f7bd
evidence_runs:
  - experiment:a00-5fbcd4dc-1ca9a4
loop: hypothesis:l4-spawn-paths-export-the-reaper-knob@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e029316bce944d87
season: 2
thought: Set the knob unconditionally on dispatch spawn_env and rotated _shell_cmd; dry-run both shows it. Tests prove kid/parent/claude-code and inherited-0 override.
title: A00 5fbcd4dc 1ca9a4
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5fbcd4dc-1ca9a4

## Experiment

Hypothesis `l4-spawn-paths-export-the-reaper-knob`: every spawn path must
export `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` explicitly, set
UNCONDITIONALLY (an inherited "0" must be overridden), and shown by
`--dry-run`. Implemented on the two spawn surfaces:

1. **`extensions/agi/bin/dispatch.py`** — after `spawn_env =
   adapter.child_env(...)`, set
   `spawn_env["CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP"] = "1"`
   unconditionally for EVERY spawn (pi and claude-code harnesses, all tiers),
   not conditional on tier/harness. Mirrored the same write into the dry-run
   `env` dict and added the key to the `export_keys` display list so
   `dispatch.py --dry-run` SHOWS it.
2. **`extensions/agi/bin/rotate.py`** — the seat-launch path. Added
   `REAPER_ENV_EXPORT = "export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1"`
   and prefixed it in `_shell_cmd` (the one function all four spawn paths —
   `cmd_spawn`, `cmd_loop`, `cmd_rotate_self`, `cmd_seats_launch` — route
   through via `spawn_window`). The worktree export comes AFTER the existing
   `CLAUDE_CODE_WORKFLOWS=1` gate for ultracode roles, so the existing
   `out.startswith("export CLAUDE_CODE_WORKFLOWS=1")` test stays green. The
   reaper export rides in the launched command's OWN env (prefix in
   `_shell_cmd`), not inherited from the tmux session. The load-bearing
   quoting of the constitution head (one argv with nested quotes) is
   untouched — `shlex.quote` is still applied per argument and the export is
   simply a new `&&` link at the front.

## Evidence

Required checks, all green:

- `python3 extensions/agi/bin/dispatch.py . 999 --target
  hypothesis:l4-spawn-paths-export-the-reaper-knob --tier kid --dry-run`
  env line ends with `... GIT_CONFIG_COUNT=1
  CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`.
- `rotate.py spawn --name reaper-check --tier kid --dry-run` prints
  `export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && claude
  --remote-control ...`.
- New tests: `test_dry_run_exports_reaper_knob_for_kid_and_parent` (pi
  kid/parent + claude-code parent all show the knob, and `=0` never appears),
  `test_dry_run_reaper_knob_overrides_an_inherited_zero` (inherited "0" is
  overridden to "1"), and in test_rotate.py
  `test_spawn_launch_carries_reaper_knob_for_plain_and_ultracode` (plain kid
  launch starts with the reaper export; ultracode keeps
  `CLAUDE_CODE_WORKFLOWS=1` first then the reaper export).
- `python3 -m pytest extensions/agi/tests/test_dispatch.py
  extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_rotate.py
  extensions/agi/tests/test_real_adapter_restart.py -q` → **199 passed**.
- Traced: `cmd_rotate_self` (L2463), `cmd_loop` (L1263) and
  `cmd_seats_launch` (L1676) all call `spawn_window` → `_shell_cmd`; both
  inherit the export. Full suite not run per the hypothesis's hard ceiling
  (parallel kids hold in-flight edits in the tree).

## Agent Notes
Reaper knob exported unconditionally on dispatch spawn_env and rotate _shell_cmd; dry-run shows it; 3 new tests + 199 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9dd6f7bd, L4.55): ACCEPTED as proved. Independently verified: (1) dispatch.py L1480 sets spawn_env["CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP"]="1" unconditionally after adapter.child_env — no tier/harness condition, so an inherited "0" is overridden; (2) dry-run mirror at L756 and the key present in export_keys — dry-run prints the knob; (3) rotate.py _shell_cmd prefixes REAPER_ENV_EXPORT ahead of every launch, ultracode gate stays first, shlex quoting untouched; (4) re-ran test_dispatch.py + test_dispatch_dry_run.py + test_rotate.py: 186 passed. Caveat accepted: no live reaper-kill was reproduced; proof rests on constructed-command evidence, which is the shape the hypothesis itself specified. No demotion.
<!-- THOUGHT:END -->
