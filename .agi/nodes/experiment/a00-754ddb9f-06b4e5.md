---
id: experiment:a00-754ddb9f-06b4e5
mint_id: 51c4c5757a1e43ad963be851845ca1e5
type: experiment
parents:
  - hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp
next_edges: []
confidence: 0.85
edited_by: a00-754ddb9f
evidence_runs:
  - experiment:a00-754ddb9f-06b4e5
line_ceiling: 50
loop: hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 31
profile: balanced
role: kid
scaffold_hash: 009959603eaec9a6
season: 2
title: suite runner passes its own private basetemp to avoid the shared-pytest prune
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-754ddb9f-06b4e5 — suite runner passes its own private basetemp

## Experiment

Item (4) of hypothesis:l4-pi-review-stages-return-...-a-private-basetemp.
Pre-fix state: `verification.py run_check` built the SUITE check argv from
`.geometry/commands.md`, appended `--durations=15`, and `subprocess.run`'d it
with NO `--basetemp`, so pytest used the SHARED `/tmp/pytest-of-<user>` root
— which a concurrent pytest prunes to 3 (SM stamp run 2: 12 stale basetemps,
deleted this runner's tree mid-run, all 5247 tests errored at setup in 47 s).

Fix (in the RUNNER, same seam already appends `--durations`):
- `run_check`: when `name == SUITE_CMD` and no `--basetemp` present, mkdir
  `<shared_sessions>/pytest-basetemp-<pid>` (rotate._sessions_dir, the ONE
  resolver the pins share) and append `--basetemp=<dir>` to the argv.
- New module helper `_cleanup_basetemp(path)`: best-effort `shutil.rmtree`,
  an OSError never fails the check. Wired via a `finally` so the owned dir is
  removed on the success and both exception return paths.
- Never the shared default; never a shell habit (no reliance on
  PYTEST_ADDOPTS). commands.md untouched; non-suite argv untouched.

Files: extensions/agi/bin/verification.py + extensions/agi/tests/test_verification.py.

## Evidence

`python3 -m pytest extensions/agi/tests/test_verification.py -q` → 48 passed.
New tests:
- test_suite_check_gets_a_private_basetemp — suite argv carries
  `--basetemp=<sessions>/pytest-basetemp-<pid>`; the dir's parent is the
  sessions dir (a unique owned child, not the shared default root); the dir
  EXISTS during the run and is GONE after it returns (finally cleanup).
- test_non_suite_check_argv_untouched — a regular "links" check argv is still
  exactly `["true"]`, no `--basetemp` injected.

Measured `git diff --numstat extensions/agi/bin/verification.py` = 31 added /
5 removed (includes comments + helper), under the 50-line ceiling.
Slope note: the initial assertion `"/tmp/pytest-of-" not in arg` was trivially
weak — tmp_path physically lives under `/tmp/pytest-of-<user>`, so the
substring is always present; replaced with the structural check
(bt_path.parent == sess + unique name) which proves the real claim.

## Agent Notes
claim (4): run_check now appends its own --basetemp=<shared_sessions>/pytest-basetemp-<pid> on the SUITE path, cleaned best-effort in a finally. 48 tests pass.
