---
id: experiment:a00-a70e522d-9b4cd6
mint_id: b5aae580c3ad4a11873ed670e88ed5dd
type: experiment
parents:
  - hypothesis:l4-the-sigterm-stale-record-test-waits-on-what-the-child-emits-never-on-wall-clock
next_edges: []
confidence: 0.75
edited_by: a00-55c9ffca
evidence_runs:
  - experiment:a00-a70e522d-9b4cd6
loop: hypothesis:l4-the-sigterm-stale-record-test-waits-on-what-the-child-emits-never-on-wall-clock@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fa6d0631508b3510
season: 2
title: A00 a70e522d 9b4cd6
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-a70e522d-9b4cd6

## Experiment

Build order (goal:g15): make `test_sigterm_kill_leaves_no_stale_record_under_aborted_subprocess`
(the SIGTERM half of the L4.276 record-cleanup falsifier) wait on what the CHILD EMITS,
never on wall clock, and land it green in `extensions/agi/tests/test_tier_gate.py`.

### Real cwd for the suite (measured, not assumed)
`commands.py show tests` prints `python3 -m pytest <worktree>/extensions/agi/tests/ -q`;
`commands.py run tests` executes it with `cwd=cmd.cwd`, and `raw_cwd = str(root)` where
`root = locations.find_project_root(...)` (`extensions/agi/bin/commands.py:164-171,241`).
Measured: `find_project_root` returns `<worktree>/.agi` — the GRAPH ROOT. Every loop below
runs from that cwd.

### Pre-fix reproduction (55 full-file loops, load 3.8-5.2)
`cd <worktree>/.agi && for i in $(seq 1 N); do python3 -m pytest
<worktree>/extensions/agi/tests/test_tier_gate.py -q; done` under four CPU burners.
Batches of 25 + 15 + 15 loops: **0 failures, `40 passed` each** (~15-23 s). The original
1-in-4997 full-suite flake was NOT reproduced in these conditions — recorded honestly.
That is not evidence the pre-fix test was sound: its readiness inference is unsound by
construction (it reads a path off the pipe and then INFERS handler readiness from it, and
waits for cleanup via `proc.wait(timeout=10)`).

### What the fix does (the four conjuncts)
1. EMITTED OBSERVABLES. The child emits `armed <marker>` only AFTER `_plant_in_tree` returns
   (handler installed), and the `_on_sigterm` handler emits `cleaned <marker>` from INSIDE
   itself AFTER the rmtree and BEFORE the re-raise. The parent does TWO blocking reads on the
   pipe (`select` + `os.read` on the raw fd, helper `_readline_within`) under ONE overall
   deadline (`time.monotonic() + 15`). No filesystem poll loop; no bare `proc.wait(timeout=)`
   standing in for the observable (wait is called only after `cleaned` is read, and is named).
2. NAMED STEPS. Every assertion carries `step=...` — `armed-emitted`, `armed-marker-name`,
   `armed-marker-present`, `cleaned-emitted`, `child-exit`, `rc-negative`, `marker-gone` — so
   a red in the one-line `-q` summary names the step.
3. BEFORE/AFTER. Pre-fix loops above; post-fix 30 full-file loops under load 5.16: 30/30
   `40 passed`, 0 failures.
4. NEVER A LONGER SLEEP. No sleep added; no timeout increased. The 5 s poll loop and the 10 s
   `proc.wait` are GONE, replaced by one 15 s deadline on emissions.

### The bug found while building it (the reason emissions must be raw writes)
`print(..., flush=True)` inside a SIGTERM handler is NOT usable here, and it fails loudly: the
parent can read the line the child just flushed while the child is still a few bytecodes short
of RETURNING from that same `print`, so the signal lands with stdout's `BufferedWriter` lock
held by the main thread. The handler's `print` then raises
`RuntimeError: reentrant call inside <_io.BufferedWriter name='stdout'>`; the child exits rc=1
WITHOUT emitting `cleaned` and the marker survives the kill it was supposed to clean.
Measured **13/20 sends** with `print`; both emissions are now `os.write(1, ...)` (a bare
syscall: no Python buffer, no lock) and 30/30 standalone + 30/30 full-file loops pass.

## Evidence

Artifact changed: `extensions/agi/tests/test_tier_gate.py` (only this file).
- top imports now include `select` and `time`
- `_on_sigterm` (inside `_plant_in_tree`): `os.write(1, f"cleaned {marker}\n".encode())` after
  `shutil.rmtree`, before `signal.signal(SIGTERM, SIG_DFL); os.kill(getpid(), SIGTERM)`
- new helper `_readline_within(proc, buffered, deadline)` (select + os.read, one deadline)
- `test_sigterm_kill_leaves_no_stale_record_under_aborted_subprocess` rewritten: child emits
  `armed` via `os.write`; parent reads armed -> SIGTERM -> reads cleaned -> wait -> asserts

Commands and counts:
- pre-fix: 25 loops -> 0 failures (`25x 40 passed`), then 15 loops at load 3.85 -> 15/15 green
- post-fix standalone: `python3 -m pytest .../test_tier_gate.py -q -k sigterm` x30 -> 30/30 `1 passed`
- post-fix full file under 4 burners (load 5.16): 30 loops -> 30/30 `40 passed`, 0 `FAIL loop`
- new test BEFORE the `os.write` fix: 13/20 failed at `step=cleaned-emitted` (the reentrancy
  measurement above); after: 0/30
Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DIRECTOR REVIEW (master-sensei gen 8, SL7.132) - the parent a00-99de32ca died on the model endpoint (output.log: "error code: 520") before harvest; credits forbid a replacement parent (remaining 7.25 - 5.00 < 3.00), so the director completed the review directly (TM.07 precedent, belam 11:2xZ). (1) INSTRUCTION, verbatim from the hypothesis: the child emits armed only after the handler is installed and cleaned from inside the handler after rmtree and before the re-raise; the parent does blocking reads on one overall deadline instead of a filesystem poll and a bare wait timeout; every assertion names its step; reproduce before and after under suite conditions. (2) MECHANISM, read from the staged diff (test_tier_gate.py +102/-21): handler emits via os.write(1, ...) - the kid measured print() re-entering the BufferedWriter lock 13/20 (RuntimeError reentrant call), a real finding, not wording; _readline_within = select + os.read on the raw fd under one 15 s deadline (= the old 5 + 10, not longer); armed/cleaned/child-exit/rc-negative/marker-gone each name their step. Whole file 3x green here after the kid 30/30. (3) NEAR MISS: print(flush=True) in the handler - satisfies the words and loses the mechanism (the line is lost 13/20 and the child dies rc=1); the kid caught it by measurement. (4) VERDICT KEPT at the kid own inconclusive_lean_proved:75: the fix is built and verified but the pre-fix reproduction never fired (55 loops green under load 3.8-5.2), so the original 1-in-4997 cause stays inferred; per the hypothesis falsifier that points at the gate sweep or at whatever runs before this test in the suite - named here, not chased in this round. NUMBERS CORRECTED (SL7.136, agent a00-55c9ffca): the staged-diff figure formerly quoted here was the `--stat` BAR width (its glyph count), never the insertion count. Command run: `git show --numstat --format= 598bb875f` -> `102 21 extensions/agi/tests/test_tier_gate.py` (and `95 0 .agi/nodes/experiment/a00-a70e522d-9b4cd6.md`); the true figure is +102/-21.
<!-- THOUGHT:END -->

## Agent Notes
SIGTERM stale-record test now waits on what the child EMITS: child os.writes 'armed <marker>' after handler install, handler os.writes 'cleaned <marker>' after rmtree before re-raise, parent does two select+os.read reads on the pipe under ONE 15s deadline (5s fs poll and 10s proc.wait deleted; no sleep added). Every assert names its step. test_tier_gate.py only. Post-fix 30/30 full-file loops green under 4 burners (load 5.16) + 30/30 standalone; pre-fix 55 full-file loops under load never reproduced the original flake, so the cause stays inferred not measured. Measured design lesson: print() in a SIGTERM handler fails 13/20 with RuntimeError reentrant call inside stdout BufferedWriter (parent reads just-flushed line while child still holds the lock -> child rc=1, cleaned lost); os.write(1,...) fixes it.
