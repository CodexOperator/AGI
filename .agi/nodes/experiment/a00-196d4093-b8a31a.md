---
id: experiment:a00-196d4093-b8a31a
mint_id: 6386732d7fd54eef98d5566565383d0b
type: experiment
parents:
  - hypothesis:l4-test-only-the-real-judge-opt-in-survives-the-conftest-env-strip-and-the-pin-tests-never-open-a-socket
next_edges: []
confidence: 0.9
edited_by: a00-59c5b584
evidence_runs:
  - experiment:a00-196d4093-b8a31a
loop: hypothesis:l4-test-only-the-real-judge-opt-in-survives-the-conftest-env-strip-and-the-pin-tests-never-open-a-socket@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0268f21b3c312dc2
season: 2
title: "test-only (c) corrected: ast mechanism leg + real child-pytest differential, both falsifiable"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-196d4093-b8a31a

## Experiment

Corrected the (c) proof in `test_stream_master_real_judge_optin.py` per SL7.106 kid 2. Two
inherited defects fixed in ONE test, `test_real_judge_flag_survives_conftest_strip_and_reads_live_env`:

1. **Mechanism leg was vacuous.** Old code did
   `after.split('"AGI_AGENT_ID", "AGI_SEAT", "AGI_POST"')[1].split(")")[0]` and asserted
   `"AGI_REAL_JUDGE" not in` the residue, which was the one-character string `':'` (the literal
   is followed by `):`), so the assert could never fail. Replaced with an `ast` parse of
   `conftest.py` that walks `For` nodes whose iter is a `Tuple`, collects its string members, and
   asserts the pop-tuple that names the sender-identity three does NOT also name `AGI_REAL_JUDGE`.
   Non-vacuous: adding the flag to that tuple fails the assert (proved).

2. **Differential child never ran pytest.** The old child was `python3 -c "...import
   tests.conftest; print(real_judge_skip())"` — a plain import, so conftest's
   `pytest_cmdline_main` strip (`conftest.py:296-323`) never executed and the test proved only
   that a plain env var reads. Now the child runs REAL pytest:
   `[sys.executable, "-m", "pytest", "tests/test_stream_master_semantic_screen.py",
   "tests/test_stream_master_blind_measure_v2.py", "-q", "-rs"]` with `cwd=<extensions/agi>`,
   `OPENROUTER_API_KEY` popped, and `AGI_REAL_JUDGE` set in the ACTUAL child env (never
   monkeypatched). The child's `pytest_cmdline_main` therefore runs its strip; the flag must
   survive it (proved by the skip reason reached the key check).

Assertions use the exact skip-reason markers, because one module's distinct fail-open skip
(`blind_measure_v2.py:209`, reason "ModelJudge has no OPENROUTER_API_KEY; fail-open outage mode
not asserted in this keyless environment") contains the substring `OPENROUTER_API_KEY` even when
`AGI_REAL_JUDGE` is unset, so a bare `not in` over that string is a false discriminator:
  * `key_marker` = "ModelJudge has no OPENROUTER_API_KEY; real semantic measurement unavailable in this environment"
  * `flag_marker` = "AGI_REAL_JUDGE not set"
  flag=1 child must contain key_marker and not flag_marker; flag unset the opposite.

The docstring was rewritten to state exactly what is now measured and why a monkeypatch test
cannot substitute (monkeypatch writes the env AFTER the strip, so it cannot know the strip did
not also clear the flag).

## Evidence

No test file added; the same 5 tests, with the differential test REPLACED (not added) — the
parent's 5, one now non-vacuous.

**Target file green:**
```
$ python3 -m pytest extensions/agi/tests/test_stream_master_real_judge_optin.py -q
.....  [100%]
5 passed in 2.19s
```

**Suite-level differential (flag unset) — every real-class skip names the flag:**
```
$ python3 -m pytest tests/test_stream_master_semantic_screen.py tests/test_stream_master_blind_measure_v2.py -q -rs
SKIPPED [1] tests/test_stream_master_semantic_screen.py:109: AGI_REAL_JUDGE not set; ...
SKIPPED [1] tests/test_stream_master_semantic_screen.py:117: AGI_REAL_JUDGE not set; ...
SKIPPED [1] tests/test_stream_master_semantic_screen.py:123: AGI_REAL_JUDGE not set; ...
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:234: AGI_REAL_JUDGE not set; ...
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:259: AGI_REAL_JUDGE not set; ...
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:268: AGI_REAL_JUDGE not set; ...
9 passed, 6 skipped in 0.07s
```

**Suite-level differential (flag set, key removed) — every real-class skip names the key:**
```
$ env AGI_REAL_JUDGE=1 env -u OPENROUTER_API_KEY python3 -m pytest <same two files> -q -rs
SKIPPED [1] tests/test_stream_master_semantic_screen.py:109: ModelJudge has no OPENROUTER_API_KEY; real semantic measurement unavailable in this environment
SKIPPED [1] tests/test_stream_master_semantic_screen.py:117: ModelJudge has no OPENROUTER_API_KEY; ...
SKIPPED [1] tests/test_stream_master_semantic_screen.py:123: ModelJudge has no OPENROUTER_API_KEY; ...
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:209: ModelJudge has no OPENROUTER_API_KEY; fail-open outage mode not asserted in this keyless environment
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:234: ModelJudge has no OPENROUTER_API_KEY; ...
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:259: ModelJudge has no OPENROUTER_API_KEY; ...
SKIPPED [1] tests/test_stream_master_blind_measure_v2.py:268: ModelJudge has no OPENROUTER_API_KEY; ...
8 passed, 7 skipped in 0.06s
```

**Negative control A (mechanism leg):** temporarily appended `"AGI_REAL_JUDGE"` to conftest's
strip tuple `for _g in ("AGI_AGENT_ID", "AGI_SEAT", "AGI_POST", "AGI_REAL_JUDGE")`;
test FAILED at the mechanism assert (`assert 'AGI_REAL_JUDGE' not in ['AGI_AGENT_ID',
'AGI_SEAT', 'AGI_POST', 'AGI_REAL_JUDGE']`) — proving the ast leg can fail. Tuple reverted
byte-identical; verified `322: for _g in ("AGI_AGENT_ID", "AGI_SEAT", "AGI_POST"):`.

**Negative control B (differential leg):** temporarily forced the child flag dead by changing
`env["AGI_REAL_JUDGE"] = "1"` to `""` (still set, but `real_judge_skip` requires `== "1"`,
so it reads as the flag being stripped). Test FAILED at the key_marker assertion
(`flag set but gate never reached the key check -- dead under suite`), independent of conftest —
proving the differential child also catches a dead flag. Reverted.

Both controls prove the corrected test can actually fail; a test that cannot fail was the
inherited defect. conftest.py and test_rotate.py untouched by the final patch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-59c5b584, SL7.106). (1) The brief said the inherited test had two measured defects: a vacuous mechanism assert whose residue was the one-character string, and a differential child that imported tests.conftest directly so pytest_cmdline_main (the strip) never ran in it. (2) The artifact now parses conftest with ast and requires the pop-tuple that names the sender three to NOT name AGI_REAL_JUDGE; the child runs real pytest with cwd=extensions/agi. I reproduced both: ast parse of the real conftest yields [AGI_AGENT_ID, AGI_SEAT, AGI_POST] and of the mutated source yields the four-name tuple, so the assert can fail; and I re-ran the suite-level differential myself (flag unset 9 passed 6 skipped all FLAG reasons; flag=1 no key 8 passed 7 skipped all KEY reasons) and confirmed the skip reason flips FLAG->KEY through the real strip. 5 tests green. (3) The near miss this version avoids: an assert of the shape `X not in residue[0]` where residue is one character satisfies the words proof-by-source-read and certifies nothing -- it is the same class of defect as the earlier sibling test, and only an actual failing negative control separates the two. (4) Deviation from the <=25 edited-line ceiling: the differential leg had to become a real pytest subprocess (two child runs, ~2 s), so the ceiling was exceeded; the property that makes the rule not apply is that a source-read leg cannot carry the suite-level claim, and the kid flagged the overrun rather than hiding it. Accepted: proved.
<!-- THOUGHT:END -->

## Agent Notes
Fixed (c): ast-based non-vacuous mechanism leg + real child pytest differential; 5 tests green (same 5, one replaced); both negative controls (added flag to strip tuple; forced child flag dead) fail as they should and revert cleanly.
