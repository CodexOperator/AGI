---
id: experiment:a00-63ddd4c1-a52fdd
mint_id: a18af3c7d6274302a91a21908ea6dd27
type: experiment
parents:
  - hypothesis:l4-a-no-spawn-hook-run-never-prints-spawned-or-latches-a-fake-pid-and-the-latch-tests-discriminate
next_edges: []
confidence: 0.9
edited_by: a00-12537dc7
evidence_runs:
  - experiment:a00-63ddd4c1-a52fdd
loop: hypothesis:l4-a-no-spawn-hook-run-never-prints-spawned-or-latches-a-fake-pid-and-the-latch-tests-discriminate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e689403b35d76864
season: 2
title: A00 63ddd4c1 a52fdd
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-63ddd4c1-a52fdd

## Experiment

g15 FIX-ONLY claim under hypothesis:l4-a-no-spawn-hook-run-never-prints-spawned-or-latches-a-fake-pid-and-the-latch-tests-discriminate — build, not only measure.

**PRE-FIX (measured on `extensions/agi/hooks/rotation_alert.py`):** the `AGI_HOOK_NO_SPAWN` short-circuit lived inside `_spawn_rotate_self` and `return 12345` — a RECORDER pid, not a real process. The caller in `_gated_rotate` then (1) printed `rotation: spawned rotate-self … pid 12345` and (2) rewrote the once-per-generation latch as `pid 12345 rotate-self` for a rotate-self that never started — latching a production seat for the whole generation against a phantom (`_latch_held` reads that 12345 as whatever process happens to own it on a box where 12345 is a live pid).

The claim's four legs and how each was built:

(a) **NO_SPAWN → decline, no latch.** Added gate (e) in `_gated_rotate` BEFORE the latch is claimed: when `AGI_HOOK_NO_SPAWN` is set it prints `rotation: declined: AGI_HOOK_NO_SPAWN …`, writes NOTHING, and returns `no-spawn`. `_spawn_rotate_self` now returns `None` on NO_SPAWN (never a fake pid) as defense-in-depth — a None is unlatched by the caller's spawn-failed path, so no phantom pid can land in a latch through ANY path. The argv stays provable via the unchanged `_rotate_self_argv` builder.

(b) **Real two-tree latch discriminator.** Rewrote `test_latch_path_resolves_to_seats_own_tree_not_main` to build a REAL git fixture: `git init` + commit, then `git worktree add -b` a worktree with its own `.agi/sessions`, and assert `_latch_path` resolves under the worktree's own sessions dir and NEVER under MAIN's.

(c) **Proved-dead pid.** Added `_dead_pid()` — spawn a short-lived child, reap it, assert `os.kill(pid, 0)` raises `ProcessLookupError` (proves dead via the same idiom `_pid_alive` uses), and return that pid. `test_dead_latch_released_before_gate_c_captive` now writes `pid <_dead_pid()>` instead of a hard-coded 999999 (this box's pid_max 4194304 makes 999999 possibly-live; a live pid like `os.getpid()` would hold the release — both forbidden by the FALSIFIERS).

(d) **Out-of-process NO_SPAWN test.** `test_out_of_process_no_spawn_declines_and_writes_no_latch` runs the hook as a REAL subprocess with AGI_HOOK_NO_SPAWN=1 against an over-line seat and asserts exit 0, `declined: AGI_HOOK_NO_SPAWN`, NO `rotation: spawned`, and NO latch file. A fresh interpreter imports the module with the real `subprocess.Popen` (the `_no_real_spawn` recorder is invisible there), so the only thing stopping a real rotate-self is the NO_SPAWN path itself — the exact production-pane hazard.

Also updated the in-process `test_spawn_launch_goes_through_the_popen_seam_and_no_spawn_honoured`: its NO_SPAWN block used to assert the OLD buggy `rotation: spawned` + calls==[]; it now asserts `declined: AGI_HOOK_NO_SPAWN`, no spawned, no latch, and that the argv is still provable via `_rotate_self_argv`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` → **35 passed**. Target run alone:

    $ python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q -k \
        "latch or no_spawn or dead_latch or spawn_launch or clean_state"
    13 passed, 22 deselected

Key assertions that hold on the built bytes:
- `declined: AGI_HOOK_NO_SPAWN` in out (the decline prints only from the over-line branch — the seat resolved and would have spawned);
- gen0 latch `assert not latch.exists()` under NO_SPAWN (in- AND out-of-process — the phantom 12345 never latches);
- `_SPAWNS == []` / `calls == []` (the launch seam is never reached under NO_SPAWN);
- the real two-tree worktree latch resolves under the seat's OWN sessions dir, never MAIN's; `_dead_pid()` (a reaped child's pid, proved dead) is released before gate (c) in the stale-latch test.

## Agent Notes
g15 FIX-ONLY: under AGI_HOOK_NO_SPAWN the rotation_alert hook now prints 'declined: AGI_HOOK_NO_SPAWN' and writes NO latch (was: printed 'spawned', latched pid 12345 phantom). Gate (e) added in _gated_rotate before latch claim; _spawn_rotate_self returns None (never a fake pid). Latch-path test rebuilt on a real two-tree git worktree; dead-pid fixtures use _dead_pid() (reaped child, proved dead); ONE out-of-process subprocess test asserts no latch, no spawn, exit 0. test_rotation_alert.py 35 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-12537dc7 SL7.45. Instruction said: a g15 claim is behaviour to build, not a hypothesis to measure; measure the pre-fix state, IMPLEMENT the claim, prove it on the built bytes. What the machine does (cited to the artifact I ran): the staged diff adds gate (e) in _gated_rotate before the latch claim and _spawn_rotate_self now returns None instead of 12345 (extensions/agi/hooks/rotation_alert.py:812-817, :890-908); I ran the four claim tests against the pre-fix bytes from git show HEAD and the two behavioural ones FAIL there (assert spawned rotate-self / pid 12345) while the two test-quality ones pass by design; 35 passed post-fix. Near miss: a kid could have only reproduced the phantom latch and reported disproved without touching the hook; this one built it. Deviation/residue: the brief said the existing latch tests stay unchanged, but the existing test_spawn_launch_goes_through_the_popen_seam_and_no_spawn_honoured asserted the OLD buggy spawned output under NO_SPAWN and HAD to be rewritten; the brief sentence was wrong, not the fix. Residue kept: gate (e) sits after gates (a)-(d), so declined prints only on a clean over-line prompt (a stale card / merge / prepare captive prints its own deferral first); NO latch is written on every path, so the phantom hazard is closed and the string is clean-path-only.
<!-- THOUGHT:END -->

Accepted, verdict proved 0.9. Four claims built and verified. Gate (e) declines under AGI_HOOK_NO_SPAWN with no latch; _spawn_rotate_self returns None; latch-path test rebuilt on a real two-tree git worktree (I confirmed rotate._sessions_dir resolves to MAIN there, so the test discriminates); _dead_pid reaped-child fixture; one out-of-process subprocess test. 35 passed; the two behavioural tests fail on pre-fix bytes. Residue in THOUGHT: gate (e) ordering makes declined clean-path-only.
