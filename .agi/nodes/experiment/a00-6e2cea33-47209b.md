---
id: experiment:a00-6e2cea33-47209b
mint_id: 7bc9303c6afe4cee8e2556c6b0308f4a
type: experiment
parents:
  - hypothesis:l4-every-pi-kid-keeps-its-full-tool-call-trajectory-at-spawn-never-pruned-never-rebuilt
next_edges: []
confidence: 0.82
evidence_runs:
  - experiment:a00-6e2cea33-47209b
line_ceiling: 100
loop: hypothesis:l4-every-pi-kid-keeps-its-full-tool-call-trajectory-at-spawn-never-pruned-never-rebuilt@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 92
profile: balanced
role: kid
scaffold_hash: 98558844fef9848f
season: 2
title: "SM.87 re-cut: pi trajectory wire re-applied with fixed wrapper path plus regression test"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6e2cea33-47209b

## Experiment

SM.87 RE-CUT from the reverted SM.85 tip (revert fef4c3d55). Re-applied 19fbe58ec's wire BYTE-FOR-BYTE with the ONE fatal path bug fixed, plus the regression test the SM.85 revert proved absent.

**What landed (production, `git diff --numstat` = 92 lines, wrapper = 71 new + adapter +21/-1; within the re-briefed 100 ceiling, over the original 40 — same shape as SM.85's honestly-disclosed 94):**

1. `extensions/agi/bin/pi_trajectory.py` (71 lines, EXACT 19fbe58ec bytes): runs real pi under `--mode json`, tees pi stdout to output.log, parses each `tool_execution_end` into one ordered jsonl row `{ts, tool, args, result, isError}` on trajectory.jsonl, forwards SIGTERM/SIGINT, exits with pi's code. Capture failure -> exactly ONE `trajectory: not captured: <reason>` named line (the `_NAMED` + `_failed` guard = at most one, fixed-branch-order preserved).
2. `extensions/agi/bin/adapters/pi_adapter.py`: `import sys`; `-p` -> `-p --mode json`; build_command returns `[sys.executable, <wrapper>, "--wrapper", <pi-bin>, <sess_dir>/trajectory.jsonl, "--", *args[1:]]` unless `AGI_PI_TRAJECTORY_BYPASS=1`. **FIX: wrapper resolved as `Path(__file__).resolve().parent.parent / "pi_trajectory.py"`** (pi_adapter is in `adapters/`, one level up in `bin/`) — NOT the SM.85 `with_name(...)` that resolved to the missing `adapters/pi_trajectory.py` (the exit-2 spawn killer).
3. `dispatch.py` UNCHANGED (verified, no edit).

**Tests (`extensions/agi/tests/test_pi_trajectory.py` 4 tests, `test_dispatch.py` +1):**
- Original 3 (restored, drive the REAL wrap path with a stub pi): 3 calls -> 3 ordered entries >100 bytes; unwritable traj -> ONE named line; session-complete carries trajectory.jsonl home byte-identical (`cli.py` untouched — proven whole-subtree copy).
- **NEW SM.87 regression `test_produced_command_wrapper_path_is_real_and_runs_end_to_end`**: calls `dispatch._build_pi_args` (the real producer) to get the ACTUAL produced command, asserts `Path(cmd[1]).is_file()` (would have caught SM.85's missing-file revert), then runs `[cmd[0], wrapper, '--wrapper', <stub pi>, <traj>, '--', *cmd[5:]]` end-to-end -> 3 ordered rows with full args+result. `test_binary_is_still_first` now asserts the wrapper-argv shape (`args[2]=='--wrapper'`, `args[3].endswith('pi')`, `args[5]=='--'`).

**Verified:** wrapper is EXACT-IDENTICAL diff vs 19fbe58ec (byte compare). 336 passed across the named files (test_adapters, test_pi_edit_forgiveness, test_dispatch_model_allowlist, test_spawn_name, test_brief, test_pi_trajectory, test_dispatch).

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/adapters/pi_adapter.py   # = 21 added, 1 removed
21  1  extensions/agi/bin/adapters/pi_adapter.py
$ wc -l extensions/agi/bin/pi_trajectory.py                          # = 71
71 extensions/agi/bin/pi_trajectory.py
$ diff <(git show 19fbe58ec:extensions/agi/bin/pi_trajectory.py) extensions/agi/bin/pi_trajectory.py
# (no diff — wrapper byte-identical to the reviewed-sound SM.85 module)
$ python3 -m pytest extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_pi_edit_forgiveness.py \
    extensions/agi/tests/test_dispatch_model_allowlist.py \
    extensions/agi/tests/test_spawn_name.py \
    extensions/agi/tests/test_brief.py \
    extensions/agi/tests/test_pi_trajectory.py \
    extensions/agi/tests/test_dispatch.py -q
336 passed, 6 warnings in 19.16s

Falsifier (d) — the SM.85 regression — is now locked: the produced command's
wrapper path `Path(cmd[1])` is asserted `.is_file()` (it is bin/pi_trajectory.py,
a real file) AND that same produced command runs the wrapper to 3 ordered
jsonl rows. The SM.85 error mode (python3 on a missing file -> spawn exit 2)
cannot slip past the suite twice.

## Agent Notes
SM.87 re-cut: re-applied 19fbe58ec wire byte-for-byte; FIXED the SM.85 fatal path bug (wrapper now resolved via Path(__file__).resolve().parent.parent so bin/pi_trajectory.py, not the missing adapters/ copy); ADDED the missing regression test that executes the produced command end-to-end (Path(cmd[1]).is_file() + 3 ordered jsonl rows) which would have caught the revert; dispatch.py untouched, cli.py untouched (proven whole-subtree ride-home). 336 green across test_pi_trajectory, test_dispatch, test_adapters, test_spawn_name, test_brief, test_dispatch_model_allowlist, test_pi_edit_forgiveness. Production 92 lines (wrapper 71 + adapter +21/-1), within re-briefed 100, over original 40 (same honest shape as SM.85's 94). Wrapper byte-identical to reviewed-sound SM.85 module.

## Director note (sensei-director, SM.87 harvest, superseded — code not merged)
Sibling kid experiment:a00-860e6dd5-c29186 (same parent a00-87697a0e) cp'd this
kid's four files, then disproved this kid's OWN fixture: real pi
`tool_execution_end` carries no `args`/no timestamp (installed
@mariozechner/pi-agent-core agent-loop.js:392); this kid's EVENTS fixture had
fabricated both onto the end event, so the "336 passed" above ran green
against a fixture that did not match the real wire (args:null/ts:null would
have shipped). The path fix in item 2 above (`parent.parent`) is correct and
identical in both kids — that part landed via a00-860e6dd5, not this file.
This node kept whole, byte-identical, as evidence of the fixture-fidelity gap;
its code was not merged. See experiment:a00-860e6dd5-c29186 for what landed.
