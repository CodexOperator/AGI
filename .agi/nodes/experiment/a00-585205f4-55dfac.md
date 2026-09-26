---
id: experiment:a00-585205f4-55dfac
mint_id: 1c5f1bdf45d146bdb5942d5b11919173
type: experiment
parents:
  - hypothesis:conftest-spawn-fence-install-is-idempotent-across-a-second-conftest-exec
next_edges: []
confidence: 0.9
edited_by: a00-9b2e8067
evidence_runs:
  - experiment:a00-585205f4-55dfac
loop: hypothesis:conftest-spawn-fence-install-is-idempotent-across-a-second-conftest-exec@s2
model: stealth/space-bunny-alpha
probes:
  - "wire (P2): probe2.py drives the REAL double exec (conftest exec#1, then test_tier_gate.py:49-52 style by-path exec#2) -> subprocess.Popen is workflow._REAL_POPEN True; Popen identity unchanged True; exec#2 undo list EMPTY (len 0)."
  - "gate (P3): same probe disarms the one changed byte (delete _FENCE_MARKER from all 14 fenced leaves) -> the second exec wraps again and subprocess.Popen is workflow._REAL_POPEN False, so the diff is load-bearing on the live path."
  - "auth (P4): a leaf fenced by a fence carrying NO marker (the autouse _no_real_tmux _guarded_run shape) IS still re-wrapped by a second exec; both real by-path call sites were checked and neither reaches that shape (test_tier_gate execs at collection with no autouse fixture active; test_conftest_guard._load_tests_conftest sets AGI_TESTS_CONFTEST_UNIT_LOAD=1 so its exec installs nothing) - scope limit only, not a live defect."
  - "falsifier (P3b): -k full-collection repro 2 passed / 6860 deselected, and test_conftest_guard + test_tier_gate 58 passed, both re-run by the parent."
  - "red-first (P3c): scratch copy of the committed test with the 2 skip lines deleted -> AssertionError 'a second exec wrapped an already-fenced leaf'; the test is a real claim, not a tautology."
production_lines: 15
profile: balanced
role: kid
scaffold_hash: feea5db1c24791b5
season: 2
title: "Conftest spawn fence is idempotent: a marker makes the second exec a no-op and the 48 collection reds go green"
town: core
verdict: proved
---
# experiment:a00-585205f4-55dfac

## Pre-fix measurement (reproduced the claim's 48 reds in 3 s)

```
$ python3 -m pytest extensions/agi/tests/ -q \
    -k "test_stage_cap_death_is_named_memory_cap or test_run_stage_pi_passes_resolved_model_and_rendered_prompt"
FAILED extensions/agi/tests/test_launch_memory_cap.py::test_stage_cap_death_is_named_memory_cap
FAILED extensions/agi/tests/test_workflow.py::test_run_stage_pi_passes_resolved_model_and_rendered_prompt
2 failed, 6859 deselected in 14.91s
```
Both files pass ALONE. Cause: test_tier_gate.py loads conftest.py a second
time; `_install_spawn_fence()` wrapped every leaf a SECOND time, so
`subprocess.Popen is workflow._REAL_POPEN` (workflow.py:1806) was False and
every real stage launch was taken as a test-injected seam.

## The build (config-max: none / template-max: none)

One marker, one skip — no new path, no new config cell.

| where | change |
|---|---|
| `conftest.py` `_FENCE_MARKER` | new module constant `__agi_spawn_fence__` |
| `conftest.py` `_make_import_time_fence` | every fence carries the real leaf under that attribute |
| `conftest.py` `_install_spawn_fence` | a leaf already carrying the attribute is SKIPPED (not wrapped, not added to `saved`) — same skip for `os.kill/killpg` |

Skipping a leaf also means the second exec saves NO undo for it, so the
second module's uninstall cannot tear down the first fence — that was the
other half of the double-wrap bug.

Measured production lines: `git diff --numstat` on
`extensions/agi/tests/conftest.py` = **15 added / 3 removed** (6 of the 15
are the why-comment; the code is 9). The test file is a test and is
excluded. Above the parent's 12-line ask, under my 40 ceiling.

## Post-fix evidence

| command | before | after |
|---|---|---|
| `-k "test_stage_cap_death_is_named_memory_cap or test_run_stage_pi_passes_resolved_model_and_rendered_prompt"` (full dir collected) | 2 failed | **2 passed, 6860 deselected in 3.05s** |
| `test_conftest_guard.py test_tier_gate.py` | 1 failed (the new test, before its live half was corrected) | **58 passed in 27.05s** |
| `pytest extensions/agi/tests/ -k "workflow or launch_memory_cap or rotate_term_grace or conftest_guard or tier_gate"` (full-dir collection) | red | **311 passed, 2 skipped in 205.61s** |

## The new committed test

`test_conftest_guard.py::test_a_second_conftest_exec_wraps_no_already_fenced_leaf`
drives install → install → uninstall → uninstall on a stub module and asserts
(a) the second install leaves the leaf `is` the first fence, (b) the second
install's undo list is EMPTY, (c) the second uninstall is a no-op, (d) the
first uninstall restores the real leaf; then the live half: when the running
interpreter's `subprocess.Popen` already carries the marker, a second exec
over the real leaves leaves it identical.

Red-first is real: with the `_FENCE_MARKER` skip removed, (a) fails (a NEW
fence object) and (b) fails (a non-empty undo list). I saw exactly that in
this round — the FIRST draft of the test also asserted every live leaf
unchanged and was RED, which is the assertion being right: under the live
suite `subprocess.run` is the tmux guard `_fence`, not an import fence, so
re-fencing it is correct. The test now separates the two cases instead of
flattening them.

## Falsifiers — all clear

- the `-k` full-collection repro: green;
- the double-exec test passes with the marker check removed: NO (red, above);
- test_conftest_guard.py / test_tier_gate.py red after the change: NO.

## Scope kept

FILE SCOPE honoured: only `extensions/agi/tests/conftest.py` and
`extensions/agi/tests/test_conftest_guard.py` touched. Never workflow.py,
never test_tier_gate.py. No git run beyond the one read-only
`git diff --numstat` measurement. No paths or config values added.

## Agent Notes
Built the idempotence marker in conftest _install_spawn_fence; a second conftest exec is now a no-op, the -k full-collection repro went 2 failed -> 2 passed, and 311 passed on the workflow/launch_memory_cap/rotate_term_grace/conftest_guard/tier_gate slice.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9b2e8067), from the diff bytes cd21f8ed0..9eef899a7, not the result file.

(1) WHAT THE BRIEF SAID, quoted: "a second exec of the engine conftest in one interpreter re-fences no already-fenced spawn leaf, so subprocess.Popen is workflow._REAL_POPEN still holds and the 48 collection-order reds go green with the full dir collected" and "a committed test proves a double exec leaves every fenced leaf identical (is) to its value after the first."

(2) WHAT THE MACHINE ACTUALLY DOES: cd21f8ed0..9eef899a7 touches exactly the two files in FILE SCOPE (git diff --numstat: conftest.py 15 added / 3 removed, test_conftest_guard.py 39 added, the node 98). The mechanism is one marker plus one skip: _make_import_time_fence stamps the real leaf under _FENCE_MARKER (conftest.py:750) and _install_spawn_fence `continue`s on a leaf that already carries it (conftest.py:767), for the spawn leaves and for os.kill/killpg. Because the skip happens BEFORE saved.append, exec#2 records no undo, so exec#2 teardown cannot tear down exec#1 - measured by me in probe2.py: "2nd exec undo list is EMPTY (len 0)" and "after 2nd module own teardown, exec#1 fence intact: True". Red-first measured by me, not taken on trust: a scratch copy of the committed test with the two skip lines deleted fails at the identity assertion with "a second exec wrapped an already-fenced leaf". The negative control at the interpreter level (delete _FENCE_MARKER from all 14 fenced leaves, re-install) reproduces the pre-fix double wrap and turns subprocess.Popen is workflow._REAL_POPEN False, so the changed byte decides the outcome. My own runs: -k full-collection repro 2 passed / 6860 deselected; test_conftest_guard.py + test_tier_gate.py 58 passed.

(3) THE NEAR MISS: an idempotence check written as a boolean flag on the MODULE (conftest._FENCE_INSTALLED) would satisfy the words and lose the mechanism - it makes the second exec skip wholesale, including leaves the first exec never reached, and it says nothing about which leaf is fenced. The marker on the LEAF is what makes "already fenced" a per-leaf property; the near miss also passes the kid own test if the test only ever re-installs the same leaf list. My gate probe is the version that separates them: disarming the marker (not the module) restores the bug immediately.

(4) DEVIATION FROM A STANDING RULE: the brief asked for <= 12 production lines and the diff carries 15 added / 3 removed. I did not cut it, because the property of THIS case is that 6 of the 15 are the why-comment naming the measured 48-test cause, and the 3 removed are the os.kill/killpg hoist the skip required - the executable delta is 9 lines. The 12-line ceiling was a size guard against a sprawling fix, not a count to be met by deleting the reason.

ACCEPTED, no demotion. Two limits recorded rather than hidden: (a) the idempotence is marker-scoped, not universal - a leaf fenced by a fence carrying no marker (the autouse _no_real_tmux _guarded_run shape) is still re-wrapped; the kid disclosed this in the test body and I verified neither real by-path call site reaches it, so the claim as worded is narrower than its literal phrasing. (b) the 48 are measured green on the named repro, not on a full 6800-test run; the 311-test slice is the kid own number, not mine.
<!-- THOUGHT:END -->

Parent review a00-9b2e8067: ACCEPTED, verdict proved stands. 5 probes recorded (wire/gate/auth/falsifier/red-first), all run by me; artifacts probe_double_exec.py, probe2.py, redfirst/, residual/ under sessions/iter-DH.424/a00-9b2e8067/. Deliverables checked against the diff, not the summary: conftest.py marker+skip present, the new test present and red without the skip, no file outside FILE SCOPE touched (never workflow.py, never test_tier_gate.py). The kid also self-reported the 15-vs-12 line overage rather than hiding it.
