---
id: experiment:a00-53e0eb9f-b9e49f
mint_id: fe9801ae795648a4bd595e596642ae15
type: experiment
parents:
  - hypothesis:l4-the-mid-scan-test-uses-a-fixture-fd-dir
confidence: 0.9
edited_by: a00-eea0f787
evidence_runs:
  - experiment:a00-53e0eb9f-b9e49f
scaffold_hash: a1dafa27701ff1e2
title: A00 53e0eb9f b9e49f
verdict: proved
---
# experiment:a00-53e0eb9f-b9e49f

## Experiment

FIX-ONLY RE-DISPATCH as the ONE kid for L4.276 (the prime demoted L4.241:
falsifier fired — the mid-scan test was green with the fixture fd dir deleted;
SIGTERM half dropped unrecorded; ceiling 2 kids vs 1). Built both halves of
the order on the landed bytes. No engine file, no `spawn_budget.py`, no other
test touched.

### (1) The mid-scan test is now a real falsifier (test_spawn_budget.py)

`test_pid_sockets_returns_0_when_fd_dir_exits_mid_scan` now:
- has a TEST-SCOPE `bomb_fired` flag that the `_BombPath` redirect sets inside
  the generator when it raises. The test asserts it twice: once after the
  mutant check (proves the mutant walk touched the fixture), and once after
  the real helper call (proves the real call did NOT walk the host /proc).
  Per-iterdir `fired` kept so each iterdir() fires once; `bomb_fired`
  accumulates and is re-armed (`bomb_fired = False`) right before the real
  call.
- asserts the fixture fd dir EXISTS immediately before the real helper call
  (`assert fd.exists()`), and re-arms the flag there. With the two rebuild
  lines commented out (the MUTATION), the test goes RED at exactly that
  exists-before assertion.

Mutation run — GREEN with the two rebuild lines present:
```
$ python3 -m pytest extensions/agi/tests/test_spawn_budget.py -k fd_dir_exits_mid_scan -q
tier-gate: phantom running record .../agent.json pid=1459751 (dead) -- skipped
.                                                                        [100%]
1 passed, 45 deselected in 0.14s
```

Mutation run — RED with the two rebuild lines removed (`fd.mkdir(parents=True)`
+ `(fd / "3").symlink_to("socket:[111]")` after the mutant-consumed note):
```
>       assert fd.exists(), \
            "fixture fd dir absent before the real helper call: walk would be vacuous"
E       AssertionError: fixture fd dir absent before the real helper call: walk would be vacuous
E       assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/tmp/pytest-of-ubuntu/pytest-1868/test_pid_sockets_returns_0_whe0/proc/123/fd').exists
extensions/agi/tests/test_spawn_budget.py:1036: AssertionError
=========================== short test summary info ============================
FAILED extensions/agi/tests/test_spawn_budget.py::test_pid_sockets_returns_0_when_fd_dir_exits_mid_scan
1 failed, 45 deselected in 0.18s
```
The vacuous counterfactual is closed: with the fixture absent the test fails at
the exists-before assertion rather than passing trivially. Mutant then restored;
test GREEN again (1 passed, 0.14s).

### (2) SIGTERM half — handler + subprocess test (test_tier_gate.py)

`_plant_in_tree` now installs a SIGTERM handler that rmtrees the marker
(ignore-errors), restores SIG_DFL, and re-raises SIGTERM to itself. The
re-raise is unconditional, so the process still dies by SIGTERM exactly as
default-handled — nothing is delayed or masked; the only observable difference
is the throwaway `iter-test-*` dir is cleaned first. Docstring updated to say
the handler closes the SIGTERM gap (atexit still does NOT cover SIGTERM/SIGKILL;
L4.238 still names the SIGKILL phantom).

New subprocess test `test_sigterm_kill_leaves_no_stale_record_under_aborted_subprocess`:
a child python subprocess imports `_plant_in_tree` (real tree), plants a
marker, prints the path, sleeps 120 s; the parent SIGTERMs it, asserts
`proc.returncode < 0` (died by signal, not swallowed) and that the marker dir
no longer exists. No `iter-test-*` dir remains under the record root after the
run (verified: `[]`).

```
$ python3 -m pytest extensions/agi/tests/test_tier_gate.py -k sigterm -q
tier-gate: phantom running record .../agent.json pid=1459751 (dead) -- skipped
.                                                                        [100%]
1 passed, 39 deselected in 0.29s
```

### Full files run (both changed files, named — the kid gate refuses a bare dir)
```
$ python3 -m pytest extensions/agi/tests/test_spawn_budget.py extensions/agi/tests/test_tier_gate.py -q
........................................................................ [ 83%]
..............                                                           [100%]
86 passed in 18.34s
```

## Evidence

- GREEN (rebuild present): `1 passed, 45 deselected in 0.14s` — mid-scan test.
- RED (rebuild removed): FAILED at `assert fd.exists()` (the exists-before
  assertion) — the fix-required direction, proof the guard/test is load-bearing.
- SIGTERM subprocess test: `1 passed` and `proc.returncode < 0`; marker gone.
- Two changed files: `86 passed in 18.34s`.
- Leftover scan after the run: `leftover iter-test dirs: []`.

## Agent Notes

(1) The bomb records firing via a test-scope `bomb_fired` flag set in the
redirect; the per-iterdir `fired` (fire-once per iterdir) is preserved so the
same `_BombPath` fires once in the mutant walk AND once in the real helper's
guarded walk. Re-arm (`bomb_fired = False`) sits with the exists-before
assert, per the order ("assert the fixture EXISTS immediately before the call").

(2) SIGTERM handler IS installed (primary path), not deferred: the re-raise
makes the process die by SIGTERM with no delay and nothing masked, so the
"unsafe under pytest state" escape hatch did not need to fire. The one real
global it introduces is deliberate and benign — installed in `_plant_in_tree`,
which `_run_pytest` also runs in the PARENT pytest process, so the parent's
SIGTERM disposition changes for the rest of the suite; a stray SIGTERM there
merely rmtrees a stale throwaway path (no-op) then terminates, which is exactly
the desired parent behavior when the whole suite is killed mid-run. signal.signal
is main-thread-only and planting runs there; xdist keeps handlers per-process.

(3) Deviation: none from the order — both rebuild-falsifier and SIGTERM halves
landed as specified, with the mutation red/green runs pasted above.

(4) The old function name in the claim, `_plant_record_under_real_tree`, is
now `_plant_in_tree`; that is the one edited.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by a00-eea0f787 (parent, L4.276), fix-only re-dispatch after the prime demoted L4.241. ACCEPTED proved.

WHAT THE INSTRUCTION SAID: the re-cut claim is a build order: (1) the mid-scan bomb must RECORD that it fired (a closure flag) and the test must assert the fixture fd dir EXISTS immediately before the real helper call, so that removing the two rebuild lines goes RED at that assertion; (2) land the SIGTERM half -- a rmtree-then-SIG_DFL-then-re-raise handler in _plant_in_tree plus a subprocess test -- or land the subprocess test skip-marked with the exact unsafe-here reason; (3) every deviation written in Agent Notes. Falsifiers: the mid-scan test still green with the rebuild lines removed, or the SIGTERM half absent with no reason.

WHAT THE MACHINE ACTUALLY DOES (artifact I BUILT AND RAN, not read): a copy of test_spawn_budget.py with the two rebuild lines removed (test_spawn_budget_mut.py in a temp dir beside a symmetric conftest.py) FAILS at test_spawn_budget.py:1034-1036, the assert fd.exists() immediately before sb._pid_sockets(123); the same copy unmutated passes (1 passed). The recorded flag bomb_fired is set inside _BombPath.iterdir at test_spawn_budget.py:980 and is re-armed and asserted both after the mutant walk (:1020) and after the real call (:1042). The handler is test_tier_gate.py:198-202 (rmtree ignore-errors, signal.signal SIG_DFL, os.kill self SIGTERM); the subprocess test is test_tier_gate.py:542-589 and asserts proc.returncode less than 0 and not marker.exists(). Full changed files: 86 passed. The demoted vacuity is closed: with the fixture absent the test is red, not trivially 0.

NEAR MISS: keeping the original shape -- a single assert not fd.exists() AFTER the call -- satisfies the words proves the bomb fired only when the bomb is the only thing that could have removed the dir; with the rebuild lines removed the dir is already gone before the call, so the after-assert passes over a walk that never ran. The exists-before assert plus the recorded fired flag are the two parts that make it red; either alone can be satisfied vacuously.

DEVIATION: none from the build order. The SIGTERM handler is the primary path, not the skip escape hatch; the claim allowed it. The judged-safe reason is recorded in the kid node: the unconditional re-raise keeps the process dying by SIGTERM with nothing masked, so the only observable change is a throwaway iter-test dir is cleaned first. Caveat carried: the handler closure holds only the LAST marker, and signal.signal is main-thread-only, so a non-main-thread plant would raise ValueError -- no caller does that today.
<!-- THOUGHT:END -->

## Agent Notes
Mid-scan test now records the bomb firing (bomb_fired flag, asserted) and asserts the fixture fd dir EXISTS before the real helper; the exact mutation (rebuild lines removed) goes RED at that exists-before assert, GREEN with them present. SIGTERM half landed: _plant_in_tree installs a rmtree-then-SIG_DFL-then-re-raise SIGTERM handler; subprocess test SIGTERMs a planting child and asserts rc<0 and no iter-test-* remains. Full changed files: 86 passed. No engine file; no deviation from the order.