---
id: experiment:a00-3a6ef699-e2351b
mint_id: 72903a9d7c6549c5bee2f2c5ff502e96
type: experiment
parents:
  - hypothesis:l4-real-judge-tests-run-only-under-one-explicit-opt-in-env-flag-default-off-a-key-alone-spends-nothing
next_edges: []
confidence: 0.9
edited_by: a00-f3e732b7
evidence_runs:
  - experiment:a00-3a6ef699-e2351b
  - experiment:a00-8f54f161-575f02
  - experiment:a00-4d9f6b08-dc569e
loop: hypothesis:l4-real-judge-tests-run-only-under-one-explicit-opt-in-env-flag-default-off-a-key-alone-spends-nothing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d70dcdf25e3ec7db
season: 2
title: A00 3a6ef699 e2351b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3a6ef699-e2351b

## Experiment

BUILT the opt-in gate for the two real-judge test classes (a g15 behaviour to
build, not just measure). One shared helper, `real_judge_skip()`, added to
`extensions/agi/tests/conftest.py` (`AGI_REAL_JUDGE`, default OFF). Both real-judge
modules gate their class through it; both module docstrings name the flag; a new
`tests/test_stream_master_real_judge_optin.py` (4 tests) proves the gate directly.

Files touched (this box IS keyed: OPENROUTER_API_KEY present in env):
- `tests/conftest.py` — appends `REAL_JUDGE_FLAG = "AGI_REAL_JUDGE"` and `real_judge_skip()`
  (returns a skip reason string, or None when the real run is permitted).
- `tests/test_stream_master_semantic_screen.py` — `_REAL_JUDGE_SKIP = real_judge_skip()`;
  `@skipif(_REAL_JUDGE_SKIP is not None, reason=_REAL_JUDGE_SKIP or "")` on TestRealSemanticMeasurement;
  docstring now names the flag + one-line invocation.
- `tests/test_stream_master_blind_measure_v2.py` — same gate on TestRealGeneralizationProbe; docstring updated.
- `tests/test_stream_master_real_judge_optin.py` — NEW: 3 gate-path tests (key+noflag→off,
  flag+nokey→off, flag+key→on) + 1 test grepping both module docstrings for the flag
  and both classes for `real_judge_skip`.

Design notes / deviation:
- Helper lives in tests/conftest.py (test-only infra), NOT semantic_screen.py, so
  `ModelJudge.available()`/`judge()` production bytes are untouched (a falsifier).
- `tests/` is a package (has `__init__.py`), so `from conftest import` was shadowed by the
  ROOT `extensions/agi/conftest.py`; imports are `from tests.conftest import real_judge_skip`.
- pytest 9 rejects `skipif(cond_that_is_True, reason=None)`: when flag+key enables the real run
  the skip reason is None, so reason is written `_REAL_JUDGE_SKIP or ""` (always a string).

## Evidence

Measured on the keyed box (OPENROUTER_API_KEY set):

- SCENARIO A (default, flag unset): 6 real-judge tests SKIP, all with
  "AGI_REAL_JUDGE not set; the real semantic measurement is opt-in and OFF by
  default (set AGI_REAL_JUDGE=1 to run it)". 9 passed, 6 skipped. Key alone spends nothing.
- SCENARIO B (`AGI_REAL_JUDGE=1`, key present): `--collect-only` shows all 6
  TestReal* cases COLLECTED as runnable (not skipped) — the real run is exactly reachable.
  (Not executed — that is a paid model call; collection proves the gate opens.)
- SCENARIO C (`AGI_REAL_JUDGE=1`, key absent): 6 skip with
  "ModelJudge has no OPENROUTER_API_KEY; real semantic measurement unavailable in this environment".
- Full run of the three affected modules + sibling blind_measure.py:
  `python3 -m pytest tests/test_stream_master_real_judge_optin.py tests/test_stream_master_blind_measure.py tests/test_stream_master_blind_measure_v2.py tests/test_stream_master_semantic_screen.py -q`
  → 17 passed, 6 skipped in 0.11s.
- Offline tests unchanged: HeuristicJudge plumbing, fail-OPEN (`test_model_judge_fails_OPEN_when_no_api_key`,
  keyless skip via `j.available()`, `mp.delenv`) all still pass. `report_split()` untouched.
- `ModelJudge.available()`/`judge()` in semantic_screen.py byte-unchanged.

FALSIFIER audit: (1) key alone runs nothing — defeated; (2) one spelling shared via one helper — defeated;
(3) both docstrings name `AGI_REAL_JUDGE` and are tested — satisfied; (4) offline tests unchanged — satisfied;
(5) production judge semantics unchanged — satisfied; (6) report_split intact — satisfied.
<!-- BODY:END -->

## Agent Notes
Built AGI_REAL_JUDGE opt-in gate (default OFF) in tests/conftest.py, wired both real-judge classes through it, named flag in both docstrings, added 4-gate test file; verified all falsifiers on keyed box.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-f3e732b7 (SL7.85). INSTRUCTION — the target's own
testable_claim: "both real-judge classes are collected-and-SKIPPED unless ONE
explicit opt-in env flag is set (AGI_REAL_JUDGE=1 ...), regardless of the key:
flag unset + key present → skipped with a reason naming the flag; flag set +
key absent → skipped with the existing key reason; flag set + key present →
the real run exactly as today."
WHAT THE MACHINE DOES — I ran it on this box, which has OPENROUTER_API_KEY
set. Flag unset: `17 passed, 6 skipped in 0.10s`, every skip reason naming
AGI_REAL_JUDGE. `env -u OPENROUTER_API_KEY AGI_REAL_JUDGE=1`: 7 skipped, the
real-judge reasons naming OPENROUTER_API_KEY — the pre-existing key reason,
unchanged. `AGI_REAL_JUDGE=1` with the key: `--collect-only` lists all 6
TestReal* cases as COLLECTED and runnable (0.04s, no model call). One helper,
`real_judge_skip()` in tests/conftest.py, imported by both modules as
`from tests.conftest import real_judge_skip`. `src/stream_master/
semantic_screen.py` and `relay.py` are byte-unchanged (`git diff --stat HEAD`
empty), so the judge's fail-open stands.
NEAR MISS — a per-file skipif that re-derives the condition locally satisfies
"skipped under a flag" and loses the mechanism: two files can drift to two
spellings, and a key alone still runs the class if either file checks the flag
wrong. This version defeats that with one imported helper plus a test that
greps BOTH modules for `real_judge_skip`. Second near miss: writing
`reason=None` when the gate is ON — pytest 9 rejects `skipif(True,
reason=None)`, and the node writes `_REAL_JUDGE_SKIP or ""` instead, which the
flag+key collect-only run confirms.
DEVIATION — the helper lives in tests/conftest.py rather than
semantic_screen.py; the claim allowed either ("semantic_screen.py
additive-only, or tests/conftest.py").
EVIDENCE ADDED BY REVIEW — the ~150s-of-606/693s cost baseline is from
experiment:a00-8f54f161-575f02 and experiment:a00-4d9f6b08-dc569e, now cited
alongside the build run rather than left implicit.
VERDICT: proved — every falsifier in the claim was measured here, not reported.
<!-- THOUGHT:END -->
