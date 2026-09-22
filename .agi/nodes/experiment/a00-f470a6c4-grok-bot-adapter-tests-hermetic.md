---
id: experiment:a00-f470a6c4-grok-bot-adapter-tests-hermetic
mint_id: 87b2e93d338a49fe8f38d2ed8d083a15
type: experiment
parents:
  - hypothesis:a00-ecc1c8f5-417666
next_edges: []
confidence: 0.9
edited_by: a00-2735efde
evidence_runs: experiment:a00-f470a6c4-grok-bot-adapter-tests-hermetic
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
season: 2
testable_claim: test_grok_bot_adapter.py reaches no real OS process, names no missing path, and the adapter argv bytes are unchanged.
title: Hermetic grok_bot_adapter tests -- no forked or spawned child, dangling probe ref removed
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f470a6c4-grok-bot-adapter-tests-hermetic

## Experiment

Closes the three residues of merge-up review `mur-g7-31-1-1-dt-69-5aa4f5af6-lean`
(`final_recommendation: accept_with_residue`) in
`extensions/agi/tests/test_grok_bot_adapter.py` only. The adapter's production
argv bytes are untouched, so the merged DT.69 `proved` verdict stands.

`production_lines: 0` -- the whole change is test-only and carries no
production diff.

## Pre-fix measurement (residues exist)

```
$ grep -nE 'os\.fork|time\.sleep\(30\)|SystemExit\(0\)' extensions/agi/tests/test_grok_bot_adapter.py
160:    pid = os.fork()
443:    argv = [sys.executable, "-c", "import time; time.sleep(30)"]
498:    argv = [sys.executable, "-c", "raise SystemExit(0)"]
$ test -f extensions/agi/tests/probes/probe_dt35.py   # MISSING
```

## Change

Residue 1 -- three tests rewritten to hermetic seams, intent preserved:

- `test_is_alive_tracks_a_live_pid_and_not_a_reaped_one`: no fork/waitpid.
  Live case `os.getpid()`; dead case `pid_max + 1` read from
  `/proc/sys/kernel/pid_max`, a pid the kernel can never hand out.
- `test_restart_spawns_a_live_process_and_is_killable` ->
  `test_restart_returns_a_live_pid_through_the_popen_seam`: fake
  `grok.subprocess.Popen` returns this interpreter's pid; asserts restart
  returns exactly Popen's pid and `is_alive` agrees. No `sleep(30)` child.
- `test_liveness_guard_goes_red_on_a_noop_argv` ->
  `test_liveness_guard_reads_a_dead_popen_pid_as_dead`: fake Popen returns a
  pid above `pid_max`; `is_alive` reads it dead. No `SystemExit(0)` child.

Residue 2 -- the `probe_dt35.py` reader instruction is gone; the `>= 25`
assertion it guarded stays, and the failure message now names the four scans
in `RECORDED_CLI_SOURCE_ENV_0_3_1`'s docstring.

Residue 3 -- the round note was written into the kid worktree but the branch
did NOT carry it: a `--branch` kid cannot commit a foreign `goal:` node
(`_round_scope_ok`, cli.py), so parent a00-c979ef9e landed it. The Agent Notes
below state the same; this sentence is aligned to them.

## Post-fix measurement

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
27 passed
$ grep -nE 'os\.fork\(|time\.sleep\(30\)|SystemExit\(0\)|probe_dt35' extensions/agi/tests/test_grok_bot_adapter.py
CLEAN
```

Hermeticity probe (scratch `hermetic_probe.py`, loaded with `-p
hermetic_probe`): `os.fork` and the real `subprocess.Popen` are replaced with
raisers; the file still passes 27/27. Negative control
(`probe_bites_test.py`, scratch) fails with `RealChildReached`, proving the
probe can go red.

## Disproof

Any `os.fork` call remaining; any test respawning through restart's unpatched
Popen; the `:334` path still missing; a test deleted or gutted instead of
rewritten; the file not green.

## Agent Notes
Parent review a00-c979ef9e DT.79. The testable_claim of this experiment is verified on the kid diff: test_grok_bot_adapter.py reaches no real OS process (27 passed with os.fork and the real subprocess.Popen replaced by raisers; the raiser bites on a negative control), names no missing path (grep for tests/probes/ exits 1), and the adapter argv bytes are unchanged. Its BODY sentence claiming residue 3 landed is not carried by the branch: git diff base..branch on .agi/nodes/goal/g7.31.1.1.md is empty and the edit is uncommitted in the kid worktree. The verdict stays proved because residue 3 is not part of this experiment testable_claim; the round hypothesis is demoted for it.
