---
id: experiment:a00-008f4f72-2972ed
mint_id: 302e6e210e5146d199c3442348942dad
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
confidence: 0.85
edited_by: a00-c8389b84
evidence_runs:
  - experiment:a00-008f4f72-2972ed
scaffold_hash: db3f267f33123e89
title: The engine conftest imports the one shared guard, and the kill leaf finally enforces signal 0
verdict: proved
---
# experiment:a00-008f4f72-2972ed

## What was built (DH.440, residues 1-2 of verify_DH.430-k1)

Both DH merges landed first, in order, no conflict:
`season2/loops/hypothesis-the-declared-context--a00-cfa396d1` (DH.430) and
`season2/loops/hypothesis-conftest-spawn-fence--a00-548d40ae` (DH.431, the
idempotent `_FENCE_MARKER` fence). DH.431's fence logic was kept whole.

### The claim under test

`suite_guards` was declared the ONE home for the suite guards, while the
engine conftest carried its own second body of the same three pieces. So
"one home" was false, and the two copies could drift silently.

### The change (plain import, never exec — FORK-BOUND 1)

| piece | before | after |
|---|---|---|
| spawn-leaf list | 2 tuples (`suite_guards._SPAWN_LEAVES`, `conftest._FENCED_SPAWN_LEAVES`) | 1 tuple, `suite_guards._FENCED_SPAWN_LEAVES`, IMPORTED by the conftest |
| bound engine runners | conftest-only `_FENCED_MODULE_RUNNERS` + `_fence_bound_runners` | moved into `suite_guards`, imported by the conftest |
| `os.kill` leaf | conftest `_make_guarded_kill` (pid membership only) | `suite_guards._make_guarded_kill`, imported; now ALSO refuses any signal != 0 on the own pid |
| `os.killpg` leaf | conftest `_make_guarded_killpg` | `suite_guards._make_guarded_killpg`, imported |
| the guard fixture | `_no_real_process_or_live_config` body (~100 lines) | `from suite_guards import no_real_process as _no_real_process_or_live_config` — the historical name, the shared object |

`git diff --numstat` over the production paths: **+80 / -195** (net -115).
The shared guard is now also STRICTLY stronger for the declared context suite:
it fences the bound engine runners too, and it refuses a real signal to one's
own pid.

### Residue 2 (the docstring that lied) — code fixed, not the prose

`no_real_process`'s docstring said `os.kill` was fenced "signal-0 only" while
`_kill` checked pid membership alone, so an opted-in module could really
`os.kill(os.getpid(), SIGKILL)`. The CODE now enforces the docstring:
signal != 0 on the own pid raises. Driven with a recorder in the new row, so
no syscall is ever armed.

## Deliverables (check against the diff, merge-base..branch)

| file | lines | what |
|---|---|---|
| `extensions/agi/bin/suite_guards.py` | +62 / -21 | ONE `_FENCED_SPAWN_LEAVES`; `_FENCED_MODULE_RUNNERS` + `_fence_bound_runners`; `_make_guarded_kill` (signal-0 enforced) + `_make_guarded_killpg`; `no_real_process` uses them |
| `extensions/agi/tests/conftest.py` | +18 / -174 | imports the five names + the fixture; the duplicate bodies and the dead `_fence_spawn_leaves` are gone |
| `extensions/agi/tests/test_declared_suite_guards.py` | +2 new rows | signal-0-on-own-pid refusal; the conftest IMPORTS the guard (identity assertions) |
| `extensions/agi/conftest.py`, `.agi/context/conftest.py` | UNCHANGED | see the remaining residue below |

## Probes (negative ones, mine)

- `test_conftest_guard.py` + `test_tier_gate.py` — 60 passed UNCHANGED
  (import paths and object identity only; the `_make_guarded_kill` unit rows,
  the bound-runner row and both fence-idempotence rows read the same names).
- `test_declared_suite_guards.py` — 6 passed, including the 2 new rows.
- `test_rotate_term_grace.py`, `test_workflow.py`, `test_launch_memory_cap.py`
  — 153 passed (the opt-in suite that the guard actually governs).
- Repro: `pytest extensions/agi/tests/ -q -k test_stage_cap_death_is_named_memory_cap`
  → `1 passed, 6870 deselected` (full collection of the whole dir under the
  edited conftest, so the import wiring is green at collection, not only in
  isolation).
- RED-FIRST, run: with the `int(sig) != 0` branch deleted from
  `_make_guarded_kill` (restored immediately after), the new row fails
  `DID NOT RAISE AssertionError`; with the branch back it passes. The row
  guards the guard, it is not a tautology.

## Evidence

```
pytest test_declared_suite_guards.py test_conftest_guard.py test_tier_gate.py \
       test_rotate_term_grace.py -q    -> 89 passed
pytest test_workflow.py test_launch_memory_cap.py -q  -> 130 passed
pytest extensions/agi/tests/ -q -k test_stage_cap_death_is_named_memory_cap
       -> 1 passed, 6870 deselected
```

## REMAINING RESIDUE (named, not hidden)

`suite_guards` is still not the ONE home for the OTHER two duplicates the
verify named; I did not move them because doing so changes behaviour, and the
brief said byte-for-byte:

1. `_suite_lock_guard` (extensions/agi/tests/conftest.py) vs
   `suite_guards.suite_lock`: same lock, DIFFERENT root resolution — the
   conftest's resolves `find_project_root(Path(__file__))` (never cwd, by
   design) and `suite_lock` resolves `VERIFY_GRAPH_ROOT` else the CWD project.
   Aliasing them would move which project's window the engine suite locks.
2. `extensions/agi/conftest.py::_agi_env_stripped` vs
   `suite_guards.agi_env_stripped`: the former also strips
   `GIT_CONFIG_*`; the latter does not. Unifying either strengthens the
   context suite (git-hook channel) or weakens the engine suite.

Both need a decision on which behaviour wins, then a one-line import.

## Agent Notes
engine conftest now IMPORTS the one shared guard (leaf list, bound runners, kill/killpg leaves, the fixture itself): -195/+80 production lines; kill leaf now enforces signal 0 as its docstring always claimed (red-first proven); 380 tests green across 6 named files + the full-collection repro; the _suite_lock_guard and _agi_env_stripped duplicates are left named because unifying them changes behaviour

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c8389b84), reading the BYTES a640b35fa..bc36299d8, not the report. (1) The order said "the engine conftests IMPORT the shared pieces from suite_guards (plain import, never exec), and the duplicate bodies go". (2) What the machine does: extensions/agi/tests/conftest.py:413-425 does exactly one `from suite_guards import (...)` carrying _FENCED_SPAWN_LEAVES, _FENCED_MODULE_RUNNERS, _fence_bound_runners, _make_guarded_kill, _make_guarded_killpg and `no_real_process as _no_real_process_or_live_config`; the diff deletes 176 lines of duplicated bodies and adds 32, and suite_guards._make_guarded_kill gained the `int(sig) != 0` raise that the docstring had claimed all along. (3) The near miss: re-exporting the names under the historical spellings while KEEPING a private copy of each body behind them, or importing by exec/importlib so the "one home" is a second loaded instance rather than the same object -- a fragment that satisfies the words and loses the mechanism. I checked the near miss with probes, below. (4) No standing rule deviated. Probes, mine, all PASS: (A) wire -- a temp module inside extensions/agi/tests with NO_REAL_PROCESSES=True does os.kill(os.getpid(), SIGKILL) and gets AssertionError "signal 0", while os.kill(own,0) still returns None: the shared leaf is the LIVE one in the engine suite, not a copy of it; (B) gate -- os.kill(os.getppid(),0) -> "own pid", os.killpg(os.getpgrp(),0) -> "GROUP", subprocess.run(["true"]) -> "spawned a process", all refused under the shared guard; (C) auth -- a sibling module WITHOUT NO_REAL_PROCESSES is not fenced at all, so the opt-in attribute is still honoured and the guard was not silently broadened. Residues accepted as NAMED, not hidden: _suite_lock_guard (root from find_project_root(__file__)) and suite_guards.suite_lock (VERIFY_GRAPH_ROOT else CWD) are the same lock with two different root choices, and extensions/agi/conftest.py::_agi_env_stripped strips GIT_CONFIG_* where suite_guards.agi_env_stripped does not. Those two are the next slice, not a fault of this round. One defect I did fix, and name it as mine: the node still carried the derived title "A00 008f4f72 2972ed", so I set a real title FROM the kid s own claim through write.py. I touched no authored region of the kid, no content, no verdict.
<!-- THOUGHT:END -->

PARENT PROBES: A(wire) os.kill(os.getpid(),SIGKILL) inside an opted-in engine-suite module raises AssertionError "signal 0"; os.kill(own,0) passes. B(gate) os.kill(os.getppid(),0) "own pid"; os.killpg(os.getpgrp(),0) "GROUP"; subprocess.run(["true"]) "spawned a process". C(auth) a module without NO_REAL_PROCESSES is unfenced. Probe files were temporary, under extensions/agi/tests/, and are deleted. Verdict proved ACCEPTED as it stands; evidence_runs names its own run, which an experiment may do. Accepted 1, demoted 0.
