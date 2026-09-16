---
id: experiment:a00-e9f2167d-babbe4
mint_id: 3ba53d55179343b49009a95211ab97f6
type: experiment
parents:
  - hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name
next_edges: []
confidence: 0.85
edited_by: a00-08a53ba9
evidence_runs:
  - experiment:a00-e9f2167d-babbe4
loop: hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "git log -1 --format='%H %s' HEAD; ls .agi/nodes/experiment | wc -l", "expected": "HEAD is the season2/main merge; experiment nodes kept", "observed": "1129d2fe4 'Merge remote-tracking branch origin/season2/main into core/season2/posts/sanctuary-director/main'; 1186 experiment nodes", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "run_workflow with _stage_context patched to raise inside the stage loop; mint patched, revoke spied", "expected": "revoke called exactly once even on the RAISED path the kid never tested", "observed": "revoked == ['hash-sk-minted-run']; RuntimeError propagated", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "run_workflow --harness claude-code (non-pi) with the revoke spy installed", "expected": "claude-code path returns before the pi try/finally, so NO phantom revoke of a key never minted", "observed": "rc 0, revoked == []", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "fake pi returns invalid JSON object FIRST then a schema-valid one; read the tracking row", "expected": "lenient contract preserved: valid candidate still wins (ok=1, unstructured=0) and NO violation is recorded for the run", "observed": "row ok=1 unstructured=0 violations={}", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "check_key_floor with (A) one sub-floor capped key, (B) cap above floor but remaining below, (C) both", "expected": "A skipped (spawn allowed); B still REFUSES by name; C still refuses", "observed": "A True/None + sub-floor stderr line; B False 'outstanding minted key agi-real remaining $0.50 is below the configured floor'; C False", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "stage-level timeout_s=3 with NO manifest timeout; and manifest timeout_s=0", "expected": "manifest/stage value reaches subprocess.run(timeout=...); declared value is not replaced by the 600 default", "observed": "stage-only -> [3]; declared 0 -> [0] (value threaded, not discarded)", "result": "pass"}
  - {"conjunct": 6, "class": "wire", "cmd": "fake pi returns 1120 chars of prose with newlines; read the tracking row and the tree render", "expected": "tracking keeps the WHOLE text; the tree stays one compact flattened line per stage", "observed": "tracked 1120/1120 chars; stage line has no embedded newline; 3 tree lines", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 7f416f9947a42734
season: 2
thought_session: SD.04
title: A00 e9f2167d babbe4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e9f2167d-babbe4

## Experiment

BUILD ORDER on `hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name`, executed against worktree `a00-08a53ba9` at HEAD `1129d2fe4`. Conjunct (1) (the SD.02→season2 re-cut) was already true on the tree. The code conjuncts (2), (3) and (5) were built in `extensions/agi/bin/workflow.py`; conjuncts (4) and (6) were verified already-landed, not rebuilt.

### Pre-fix state (measured on the bytes, before any edit)

- `grep -n "revoke" extensions/agi/bin/workflow.py` → zero hits; `mint` only at `_resolve_workflow_spawn_env` ~L1175, which returned a bare `dict` and DISCARDED `minted.key_hash`. `run_workflow()` had no `try/finally` and no revoke at all.
- `_run_stage_pi()` line ~L1378: `subprocess.run(cmd, ..., timeout=600)` — a bare literal; no manifest carries `timeout_s`.
- `_resolve_lenient_return()` called `validate_return()` and threw the violation strings away; a JSON-but-schema-invalid return was indistinguishable from prose and its named violation was lost.

### Red first (same three fixtures, before the fix)

```
FAILED test_pi_run_revokes_the_minted_key_once_on_success
FAILED test_pi_run_revokes_the_minted_key_once_when_a_stage_fails
FAILED test_revoke_failure_does_not_fail_the_run_but_is_named
FAILED test_manifest_timeout_s_reaches_the_stage_subprocess
FAILED test_per_stage_timeout_overrides_the_manifest
FAILED test_schema_violation_is_recorded_on_the_unstructured_return
6 failed, 3 passed, 59 deselected in 0.71s
```

(The three that passed already described intended-true behaviour: no-mint → nothing revoked, absent `timeout_s` → 600, and a later valid candidate still winning.)

### What was built

**Conjunct (2) — revoke.** `_resolve_workflow_spawn_env()` now returns `(env, key_hash | None)`, carrying `minted.key_hash` out of the mint seam. `run_workflow()` wraps the whole pi stage loop in `try/finally` and calls a new `_revoke_run_credential(key_hash, root)`, which calls `provisioning.revoke(key_hash, root=root)` exactly once on success, on a stage failure (`return rc`) and on any raised path. A fallback path (no mint) revokes nothing. Revoke failure never becomes a run failure — the run's exit code is untouched — but a `False` return or a raising seam prints ONE stderr line naming the key.

**Conjunct (5) — timeout.** `run_workflow()` resolves `stage["timeout_s"] or manifest["timeout_s"]` per stage and threads it into `_run_stage_pi(..., timeout_s=...)`; `_run_stage_pi` uses `600 if timeout_s is None else timeout_s`. A manifest with no `timeout_s` is byte-behaviour-identical to the old literal.

**Conjunct (3) — schema miss.** `_resolve_lenient_return(schema, text, violations_out=None)` appends the violation strings of every JSON candidate that failed the schema, then still returns the first candidate that validates. `_run_stage_pi` dedupes them, names the first on stderr, and returns `{"unstructured": <whole text>, "violations": [...]}`. `RunView` carries the violations per stage and `_track_run` writes them to the row under a new `violations` key, so the run's record names the violation instead of filing JSON-shaped output under the same key as prose.

**Verified already-landed, untouched:** conjunct (4) sub-floor skip (`provisioning.py:403`, `test_provisioning.py:1575`) and conjunct (6) whole-text `returns` retention (`_track_run`, `RunView._tree`).

## Evidence

Green, after the build:

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q
68 passed in 67.39s

$ python3 -m pytest extensions/agi/tests/test_workflow.py \
    extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_commands.py -q
332 passed, 5 skipped, 2 warnings in 80.18s
```

Hermetic: no `.env`, no network, no real mint/revoke — the fake-pi bin pattern and a monkeypatched `provisioning.mint`/`revoke` seam are used throughout (the project-wide `_mutation_guard` makes a real revoke impossible under pytest by design).

`git status --porcelain` on the worktree shows exactly the two owned files modified plus this node; no git command was run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-08a53ba9) of this version. The instruction said a kid's tests are its CLAIM, not my evidence, and that I must read the DIFF bytes and run one negative probe per conjunct (hypothesis:l4-the-parent-task-section-says-a-kids-tests-are-its-claim-and-hands-the-parent-the-kid-diff-not-its-result-file). What the machine actually does, cited: workflow.py:1597 `_resolve_workflow_spawn_env` now returns `(env, key_hash)` and `workflow.py:1638` wraps the pi stage loop in try/finally -> `_revoke_run_credential`; `workflow.py:1441` `timeout=(600 if timeout_s is None else timeout_s)` with the manifest lookup at `workflow.py:1612`; `workflow.py:1372` `_resolve_lenient_return(..., violations_out)` appended at `workflow.py:1460` and written to the tracking row at `workflow.py:947`. I read the staged diff (`git diff --cached`), not the result file, and ran SEVEN probes of my own (recorded in `probes:`): a RAISED stage-loop path still revokes (the kid tested success and rc>0, never a raise); the claude-code path revokes nothing (no phantom call); invalid-then-valid JSON still wins with no violation recorded (lenient contract intact); a cap-above-floor key whose REMAINING is below the floor still REFUSES while a sub-floor cap is skipped (the skip did not swallow the real refusal); a stage-level timeout with no manifest timeout reaches the child, and a declared 0 reaches it as 0 rather than being replaced by the default; and 1120 chars of prose survive whole in tracking while the tree stays one flattened line. All pass, so `proved` is upheld. NEAR MISS: fixture-proof through a monkeypatched seam is not a real key deletion and not a real timed-out child; the project-wide `_mutation_guard` makes the first impossible under pytest by design, and the second is only observed as the resolved `subprocess.run(timeout=...)` kwarg, so the claim is proved at the seam, not against live OpenRouter. DEVIATION: none from the brief; the `violations` key rides the tracking row rather than reshaping `returns`, which the kid chose to keep conjunct (6)'s already-landed `returns[label] == <whole prose>` shape intact.
<!-- THOUGHT:END -->

## Agent Notes
Built conjuncts (2),(3),(5) in extensions/agi/bin/workflow.py: minted key_hash threaded out and revoked once in a finally on success/stage-failure/raise; stage timeout resolved from manifest timeout_s with 600 default; schema violations kept and recorded on the unstructured return plus a new violations row key. Red-first: 6 fixtures failed on the old bytes, 68/68 green after; 332 passed across workflow/provisioning/adapters/dispatch/commands.

Parent review accepted, upheld `proved`. Read the staged diff (not the result file); ran 7 negative probes recorded in `probes:` — all pass. Conjunct 2 (revoke) holds even on a RAISED stage-loop path the kid never tested and calls no phantom revoke on the claude-code path. Conjunct 3 (schema miss keeps its named violation) holds and the lenient valid-after-invalid contract did not regress. Conjunct 5 holds: the manifest value reaches the child, including a declared 0. Conjuncts 1/4/6 verified already-landed and re-probed live. Caveat: fixture-proven at the monkeypatched seam, not against a live key deletion or a real timed-out child (`_mutation_guard` forbids a real revoke under pytest).
