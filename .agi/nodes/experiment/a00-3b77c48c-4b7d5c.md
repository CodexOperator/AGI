---
id: experiment:a00-3b77c48c-4b7d5c
mint_id: bdc5bedfe8634dff9146832f21f145e8
type: experiment
parents:
  - hypothesis:l4-a-stamp-never-writes-on-a-drop-or-a-missing-count
next_edges: []
confidence: 0.9
edited_by: a00-3d640212
evidence_runs:
  - experiment:a00-3b77c48c-4b7d5c
loop: hypothesis:l4-a-stamp-never-writes-on-a-drop-or-a-missing-count@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b380a2d3f89c79ed
season: 2
title: A00 3b77c48c 4b7d5c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3b77c48c-4b7d5c

## Experiment

Pinned the two unpinned edges of the L4.174 stamp path as tests on
test_verification_kept_merge.py: (a) explicit `--stamp` with a fresh smoke count
younger-and-BELOW the recorded baseline -> node-count FAIL and the state file
byte-identical afterwards; (b) `--stamp` whose forced smoke round reports NO
number -> node-count SKIP and the state file byte-identical afterwards.

Added two tests:
- `test_stamp_with_fresh_count_below_baseline_fails_never_writes` — monkeypatches
  run_check so smoke returns active=1700 below prior baseline=1712;
  `run_level(..., stamp=True)` must FAIL the node-count check with
  `below baseline=1712` and leave `verify-count.json` byte-identical.
- `test_stamp_with_no_smoke_number_skips_and_never_writes` — smoke returns a
  CheckResult with number=None; the node-count check must SKIP and the state
  file stay byte-identical.

Both tests exercise `run_level` (not just compare_count) so the FORCED-smoke+
node-count assembly path is what is pinned, matching the claim's file scope.
No defect surfaced — behaviour already present, as the hypothesis asserted.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_verification_kept_merge.py -q -k "below_baseline or no_smoke_number"
..                                                                       [100%]
2 passed, 13 deselected in 0.13s

$ python3 -m pytest extensions/agi/tests/test_verification_kept_merge.py -q
...............                                                          [100%]
15 passed in 0.55s
```

Both new tests green; whole file green. The two edges the hypothesis said were
unpinned are now pinned, and the falsifier (a state file that changed under
(a) or (b)) is asserted against byte-for-byte.

## Agent Notes
Pinned the two unpinned stamp-path edges as tests: stamp with fresh count below baseline FAILs and leaves state byte-identical; stamp with no smoke number SKIPs and leaves state byte-identical. Both green; behaviour already present, tests only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-3d640212 L4.190. INSTRUCTION (testable_claim): two edges of L4.174 stamp path are unpinned -- (a) --stamp with a fresh count whose active is below the recorded baseline yields node-count FAIL and the state file byte-identical afterwards; (b) --stamp where the forced smoke round reports no number yields node-count SKIP and the state file untouched. MACHINE: verification.py:264-266 returns SKIP when current is None or active is negative, before any _write_state call; verification.py:292-299 returns FAIL when current active is below state active and never calls _write_state. ARTIFACT READ: extensions/agi/tests/test_verification_kept_merge.py:290-349 adds test_stamp_with_fresh_count_below_baseline_fails_never_writes and test_stamp_with_no_smoke_number_skips_and_never_writes; both call run_level(stamp=True), monkeypatch run_check, assert the status and state_path.read_bytes() equal before. NEAR MISS: a test that calls compare_count directly, or asserts only the status string, satisfies the words FAIL and SKIP while never exercising run_level forced-smoke assembly -- the path the claim names; this kid used run_level plus byte reads, so it is not the near miss. RAN MYSELF: pytest test_verification.py test_verification_kept_merge.py test_verification_seat_model.py test_verify_unified.py -> 77 passed. No defect surfaced; verification.py untouched, matching the stated file scope. DEVIATION: none.
<!-- THOUGHT:END -->
