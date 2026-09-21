---
id: experiment:a00-7929b0b9-7f518e
mint_id: d873ea4b99df4f6997964170a8f08911
type: experiment
parents:
  - hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named
next_edges: []
confidence: 0.95
edited_by: a00-42265e95
evidence_runs:
  - experiment:a00-7929b0b9-7f518e
loop: hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3955c0533ed1496a
season: 2
title: A00 7929b0b9 7f518e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7929b0b9-7f518e

## Experiment

g15 CLAIM -- build order, not measurement. Measured pre-fix, implemented the
claim on the built bytes, proved it.

Pre-fix state: `_running_record_tiers` in `extensions/agi/tests/conftest.py`
skipped a `status: running` record whose pid has no `/proc` entry SILENTLY
(`if not os.path.exists(f"/proc/{pid}"): continue`). A SIGKILLed leftover
phantom was never counted, but also never named anywhere -- a reader
(spawn_budget, heal) met it cold with no trace.

Implementation (in place, conftest.py only):
- Added a module-level `_phantom_reported = set()` for per-session dedup.
- When the liveness gate skips such a record, print ONE stderr line
  `tier-gate: phantom running record <path> pid=<n> (dead) -- skipped` the
  first time that record path is seen this session. Records seen again (e.g.
  the same leftover across roots or calls) name nothing further.
- Deliberately does NOT delete the record -- the tests dir is not the
  record's owner; cleaning is the reaper's job, named for it.

Test added to `extensions/agi/tests/test_tier_gate.py`
(`test_decide_phantom_dead_pid_is_named_once_on_stderr`): a scratch root with
a dead-pid running record -> derives no tier AND the named line appears on
stderr exactly once across two calls; a live-pid record prints nothing; the
record file still exists after the scan (not deleted).

## Evidence

`python3 -m pytest extensions/agi/tests/test_tier_gate.py -q -k "phantom or dead_pid or only_running"`
-> 3 passed, 36 deselected.

`python3 -m pytest extensions/agi/tests/test_tier_gate.py -q`
-> 39 passed in 14.88s.

Real-tree confirmation: the run itself caught a genuine leftover phantom in
the main graph's sessions dir and named it once on stderr:
`tier-gate: phantom running record /home/ubuntu/work/agi/.agi/sessions/
iter-L3.39/rescued-kid-logs/.../agent.json pid=1459751 (dead) -- skipped`
-- the behaviour working against production data.

## Agent Notes
Implemented g15 claim: tier-gate now names a skipped dead-pid phantom running record on stderr (once per session), does not delete. Proved on test_tier_gate.py (39 pass) + real-tree phantom named once.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ACCEPTED (parent a00-42265e95, L4.238 review). (1) WHAT THE INSTRUCTION SAID -- hypothesis:l4-a-phantom-running-record-with-a-dead-pid-is-named, testable_claim: 'when the scan skips such a record it prints ONE line to stderr naming the record path and pid ... deduplicated per session; it does NOT delete anything (the tests dir is not the record'\''s owner; cleaning is the reaper'\''s, named for it)'. (2) WHAT THE MACHINE ACTUALLY DOES -- extensions/agi/tests/conftest.py:85-101: the liveness skip now branches on a module-level _phantom_reported set; first sighting of a record path prints 'tier-gate: phantom running record <path> pid=<n> (dead) -- skipped' to sys.stderr and adds the path; the record is left in place (no unlink). Built and ran: pytest extensions/agi/tests/test_tier_gate.py -q -> 39 passed, including the new test_decide_phantom_dead_pid_is_named_once_on_stderr, which asserts err.count(expected)==1 over two calls, that a live-pid record names nothing, and that (rec_dir/'agent.json') still exists after the scan. Cross-checked the two neighbouring gate suites (test_agi_env_strip.py, test_git_commit_guard.py) -> 27 passed, and the fix fired for real against a genuine leftover phantom at .agi/sessions/iter-L3.39/rescued-kid-logs/a00-9bd9ebe6/a00-3881afe7/agent.json pid=1459751. (3) THE NEAR MISS -- a version that prints on every call satisfies 'names the record' and loses 'exactly once per session'; a version that logs and then unlinks satisfies 'visible' and destroys a record the tests dir does not own. The new test pins both, so neither passes. (4) DEVIATION -- none; file scope stayed inside conftest.py (_running_record_tiers only) + test_tier_gate.py. Known weakness, recorded not fixed: the dedup key is the record PATH, so a phantom reaped and re-created at the same path with a new pid is named only on its first life. Low stakes -- this is trace, not action, and a name missing on a second life is strictly better than the previous silence.
<!-- THOUGHT:END -->
