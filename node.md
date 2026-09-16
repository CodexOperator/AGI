---
id: experiment:a00-e9f2167d-babbe4
mint_id: 3ba53d55179343b49009a95211ab97f6
type: experiment
parents:
  - hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name
next_edges: []
confidence: 0.85
edited_by: a00-c2613ff6
evidence_runs:
  - experiment:a00-e9f2167d-babbe4
loop: hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 0, "class": "wire", "cmd": "git log -1 --format='%H %s' HEAD; ls .agi/nodes/experiment | wc -l", "expected": "HEAD is the season2/main merge; experiment nodes kept", "observed": "1129d2fe4 'Merge remote-tracking branch origin/season2/main into core/season2/posts/sanctuary-director/main'; 1186 experiment nodes", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "run_workflow with _stage_context patched to raise inside the stage loop; mint patched, revoke spied", "expected": "revoke called exactly once even on the RAISED path the kid never tested", "observed": "revoked == ['hash-sk-minted-run']; RuntimeError propagated", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "run_workflow --harness claude-code (non-pi) with the revoke spy installed", "expected": "claude-code path returns before the pi try/finally, so NO phantom revoke of a key never minted", "observed": "rc 0, revoked == []", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "fake pi returns invalid JSON object FIRST then a schema-valid one; read the tracking row", "expected": "lenient contract preserved: valid candidate still wins (ok=1, unstructured=0) and NO violation is recorded for the run", "observed": "row ok=1 unstructured=0 violations={}", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "grep -n _mutation_guard extensions/agi/bin/provisioning.py; test -e .env; and the pi/lenient/unstructured/revoke subset of test_workflow.py run with OPENROUTER_API_KEY+ANTHROPIC_API_KEY cleared AND a pytest plugin refusing every socket.socket.connect / create_connection", "expected": "the mint/revoke guard is live under pytest, no .env exists in the worktree, and the pi-return tests pass with no network and no credentials", "observed": "guard present at provisioning.py:639 (def _mutation_guard), :711 (mint), :789 (revoke); `.env` absent; 20 passed, 51 deselected in 74.34s with both env vars cleared and all outbound connects raising", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "check_key_floor with (A) one sub-floor capped key, (B) cap above floor but remaining below, (C) both", "expected": "A skipped (spawn allowed) AND the skip visible in the return value; B still REFUSES by name; C still refuses", "observed": "A True/None + sub-floor stderr line (pre-fix); B False 'outstanding minted key agi-real remaining $0.50 is below the configured floor'; C False. Re-measured this round: A now returns (True, <the-stderr-sentence>) and the marker is printed as `notice:` by dispatch.py:2072's caller", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "manifest timeout_s=0; stage timeout_s=0 with manifest 600; stage timeout_s=3 with no manifest; absent timeout", "expected": "a declared value is RESOLVED by presence, never by truthiness: 0 is refused by name before any stage is dispatched, a positive stage value overrides the manifest, and an absent value keeps the 600 default", "observed": "re-measured this round on the built resolver workflow.py _resolve_stage_timeout: manifest 0 -> rc 4, 0 stages dispatched, stderr names timeout_s; stage 0 + manifest 600 -> rc 4, stderr names stage 'only' and 600 never used; stage 3 -> [3]; absent -> [600]", "result": "pass"}
  - {"conjunct": 6, "class": "wire", "cmd": "fake pi returns 4000+ chars of prose with newlines; read the tracking row and the tree render", "expected": "tracking keeps the WHOLE text; the tree shows one line per stage, a head-preview with the exact omitted size, never the blob", "observed": "re-measured this round: tracked 10990/10990 chars whole; the tree line is `└─ [?] only — <200-char head>… (+10790 chars)`, no embedded newline", "result": "pass"}
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
PREVIOUS VERSION SAID: the probes were numbered 1..6 with probe 1 = the SD.02 re-cut, probe 2 = revoke (gate) and probe 2 = revoke (wire), probe 3 = schema miss, probe 4 = sub-floor, probe 5 = timeout, probe 6 = tree/tracking -- so every probe after the re-cut was off by one against the parent hypothesis's own conjunct list (1 revoke, 2 schema violation, 3 hermeticity, 4 sub-floor, 5 timeout_s, 6 unstructured whole in tracking/compact in tree), and conjunct (3) hermeticity had NO probe at all even though the body asserted 'Hermetic: no .env, no network, no real mint/revoke'. The timeout probe also recorded 'declared 0 -> [0]' as a pass, i.e. it certified the pre-fix truthiness bug as intended behaviour.
WHY THIS VERSION DIFFERS: this round (experiment a00-c2613ff6-31b78c, hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation conjunct (4) of its residue list) was ordered to align the numbering and to give hermeticity a probe that was actually RUN. Renumbered to the parent's conjunct numbers: revoke -> 1 (both probes), schema -> 2, NEW hermeticity -> 3, sub-floor -> 4, timeout -> 5, tree/tracking -> 6. The re-cut probe is MOVED OFF the conjunct sequence to conjunct 0 with class 'wire' -- it is a precondition of the round, not one of the claim's conjuncts, and 0 makes that explicit where a renumber could not. The new conjunct 3 probe is EXECUTED, not read: grep shows _mutation_guard live at provisioning.py:639/711/789, .env is absent, and the pi/lenient/unstructured/revoke subset of test_workflow.py passes 20/20 with OPENROUTER_API_KEY and ANTHROPIC_API_KEY cleared and a pytest plugin refusing every socket.socket.connect and socket.create_connection. The timeout probe's observed and expected were rewritten because the residue round CHANGED that behaviour on purpose: 0 is now refused by name before any stage is dispatched (workflow.py _resolve_stage_timeout, definition (a)), so a probe still recording '0 reaches subprocess.run as 0' would be false on the built bytes. The tree/tracking probe was re-measured on a 4000+ char return because the residue round made the tree PREVIEW a blob rather than inline it. VERDICT, CONFIDENCE, PARENTS, EVIDENCE_RUNS and the BODY are untouched, as ordered.
<!-- THOUGHT:END -->

## Agent Notes
Built conjuncts (2),(3),(5) in extensions/agi/bin/workflow.py: minted key_hash threaded out and revoked once in a finally on success/stage-failure/raise; stage timeout resolved from manifest timeout_s with 600 default; schema violations kept and recorded on the unstructured return plus a new violations row key. Red-first: 6 fixtures failed on the old bytes, 68/68 green after; 332 passed across workflow/provisioning/adapters/dispatch/commands.

Parent review accepted, upheld `proved`. Read the staged diff (not the result file); ran 7 negative probes recorded in `probes:` — all pass. Conjunct 2 (revoke) holds even on a RAISED stage-loop path the kid never tested and calls no phantom revoke on the claude-code path. Conjunct 3 (schema miss keeps its named violation) holds and the lenient valid-after-invalid contract did not regress. Conjunct 5 holds: the manifest value reaches the child, including a declared 0. Conjuncts 1/4/6 verified already-landed and re-probed live. Caveat: fixture-proven at the monkeypatched seam, not against a live key deletion or a real timed-out child (`_mutation_guard` forbids a real revoke under pytest).
