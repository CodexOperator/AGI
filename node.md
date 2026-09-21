---
id: experiment:a00-93b7761e-ba5b62
mint_id: 54e04bdeaf92462994e5c79d58bc43ac
type: experiment
parents:
  - hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-refused-run-key
next_edges: []
confidence: 0.88
edited_by: a00-817a765c
evidence_runs:
  - experiment:a00-93b7761e-ba5b62
loop: hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-refused-run-key@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -rn 'marker-dead-code-and-truncation|code-and-truncation|dead-code-and-truncation' extensions/ skills/ src/; read each site's ordinal; then yaml.safe_load experiment:a00-c2613ff6-31b78c and list probes[].conjunct", "expected": "every ordinal agrees with the parent's (1)-(5) list -- sub-floor marker 1, dead-code 2, tree 3, experiment numbering 4, timeout 5 -- and the node's probes read [1,1,2,3,5,5,4]", "observed": "dispatch.py:2087 (1); provisioning.py:358 (1); workflow.py:908 and 1022 (3); workflow.py:1324 (2); workflow.py:1546/1662/1698 (5); test_workflow.py:1956 header (5, unchanged), 2057 (5), 2155 header and 2163 (3); probes [1,1,2,3,5,5,4]; verdict/confidence/parents/evidence_runs unchanged", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k sub_floor_notice -- the new test drives the REAL dispatch.main() with check_runtime_key_usable -> (True,None), check_key_floor -> (True,'M'), check_account_floor -> (False,'X') on an openrouter pi graph, Popen recorded; then the same test with the notice print replaced by `pass`", "expected": "green on the built bytes (notice: M printed before ERR: X, zero spawns); RED on the pre-fix bytes with the notice print removed", "observed": "RED: 1 failed -- AssertionError 'notice: M' not in stderr (stderr carried only 'ERR: X'); GREEN: 1 passed, 121 deselected", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_workflow.py -q -k 'dry_run_refuses_an_invalid_timeout or dry_run_still_green'; the invalid shapes are manifest timeout_s=0, stage timeout_s=-1 and stage timeout_s='600' (non-numeric); RED by moving the budget-resolution block back below the dry-run return", "expected": "pre-fix --dry-run returns 0 and prints the credential, [dispatch] and [summary] lines for a manifest the live run refuses; post-fix rc 5 for all three shapes with no [dispatch]/[summary]; control timeout_s=7 still rc 0", "observed": "RED: AssertionError (0, '[run-key] review\\n[credential] ...\\n[dispatch] only ...\\n[summary] workflow=review harness=pi stages=1 ...'); GREEN: 2 passed, 73 deselected", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_workflow.py -q -k 'distinct_from_the_stage_parse_error or no_per_run_key_is_minted'; both arms DRIVEN in one test (the parse-error arm by monkeypatching workflow._resolve_lenient_return to raise, the only path into its handler); RED by putting the refusal's return back to 4; plus grep -n 'return [0-9]' workflow.py for the existing code meanings", "expected": "0/2/3/4 in use (4 = stage return-parse error), 5 unused; the refusal arm gives 5 and the parse arm 4, distinct; mint called 0 times for a refused run", "observed": "RED: AssertionError 4 == 5 (refused_rc 4 == parse_rc 4); GREEN: refused_rc 5, minted == [], both tests passed; grep found the collision exactly at `_run_stage_pi`'s `return 4, None`", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe: scoped scan of every `conjunct (N)` in extensions/agi/bin+tests whose window names hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation (abbrevs included) and NOT l4-sd06-residue; N checked against the subject the window names (check_key_floor=1, _parse_last_json=2, _preview_detail=3, a00-e9f2167d=4, timeout_s=5); then yaml-load experiment:a00-c2613ff6-31b78c probes[].conjunct", "expected": "no ordinal out of 1..5 and no single-subject disagreement; a00-c2613ff6 probes [1,1,2,3,5,5,4], verdict untouched", "observed": "bad == []; five known sites correct by file (dispatch.py 1, provisioning.py 1, workflow.py 2/3/5, no 6); probes [1,1,2,3,5,5,4]; verdict proved", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "PARENT probe, independent of the kid's test: drove the real dispatch.main() with check_runtime_key_usable->(True,None), check_key_floor->(True,'M'), check_account_floor->(False,'X'), dispatch.subprocess.Popen recorded, on a temp graph with harnesses.pi.provider=openrouter; then repeated with the notice print replaced by `pass` (source restored byte-identical)", "expected": "green on built bytes: 'notice: M' before 'ERR: X', zero spawns; RED on pre-fix bytes with the notice print removed", "observed": "green: rc 1, notice: M before ERR: X, spawned == []; RED pre-fix: AssertionError \"'notice: M' not in stderr\" (stderr carried only 'ERR: X'); dispatch.py restored byte-identical", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "PARENT probe: monkeypatched workflow._resolve_stage_timeout with a call spy, drove --dry-run on a real manifest (valid timeout_s=7), then --dry-run on timeout_s=0, stage timeout_s=-1 and stage timeout_s='600'", "expected": "the dry-run path CALLS the resolver (pre-fix it returned above the resolution loop, so the spy would see zero calls); an invalid shape refuses with no [dispatch]/[summary]", "observed": "spy calls == ['only'], rc 0 control; all three invalid shapes rc 5 with no [dispatch] and no [summary]", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "PARENT probe: drove the real run_workflow with timeout_s=0 (subprocess.run captured, seen==[] the no-stage observable) and with provisioning available + workflow.provisioning.mint patched to record calls", "expected": "rc 5 distinct from the stage return-parse-error rc 4; zero stages dispatched; zero keys minted for a manifest refused before any stage", "observed": "rc 5 (not 4), seen == [], minted == []; code grep confirms 4 is _run_stage_pi parse-error and 5 unused elsewhere", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 867e0ecbef453326
season: 2
title: A00 93b7761e ba5b62
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-93b7761e-ba5b62

## Experiment

BUILD ORDER on `hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-refused-run-key`. Four conjuncts. Every location below was re-measured on THIS worktree's bytes before editing — the brief's line numbers had drifted (belam XXIII was right), and the numbers below are the current ones. All four conjuncts were IMPLEMENTED, not merely measured.

Files touched (named in prose — no git command was run):

- `extensions/agi/bin/dispatch.py` — conjunct 1
- `extensions/agi/bin/provisioning.py` — conjunct 1
- `extensions/agi/bin/workflow.py` — conjuncts 1, 3, 4
- `extensions/agi/tests/test_dispatch.py` — conjunct 2 (new fixture test)
- `extensions/agi/tests/test_workflow.py` — conjuncts 1, 3, 4 (renumbered two comments, four new tests)
- `.agi/nodes/experiment/a00-c2613ff6-31b78c.md` — conjunct 1 (probes + thought, via `write.py` ONLY)

No file outside that scope was touched. No unexpected files were seen in the tree.

### Conjunct 1 — every ordinal agrees with the parent's (1)-(5) list

The parent hypothesis's list is: (1) `check_key_floor`'s sub-floor marker return, (2) `_parse_last_json` wired or removed, (3) `RunView._tree` previews a multi-KB blob, (4) experiment `a00-e9f2167d-babbe4`'s numbering + hermeticity probe, (5) stage-level `timeout_s=0` made reachable and defined. Every reference in the tree was shifted **+1** against it. Renumbered by hand with the edit tool (code comments) and through `write.py` (the experiment node):

| file:line | was | now |
|---|---|---|
| `extensions/agi/bin/dispatch.py:2087` | conjunct (2) | conjunct (1) |
| `extensions/agi/bin/provisioning.py:358` | conjunct (2) | conjunct (1) |
| `extensions/agi/bin/workflow.py:908` | conjunct (4) | conjunct (3) |
| `extensions/agi/bin/workflow.py:1022` | conjunct (4) | conjunct (3) |
| `extensions/agi/bin/workflow.py:1324` | conjunct (3) | conjunct (2) |
| `extensions/agi/bin/workflow.py:1546` | conjunct (6) | conjunct (5) |
| `extensions/agi/bin/workflow.py:1662` | conjunct (6) | conjunct (5) |
| `extensions/agi/bin/workflow.py:1698` | conjunct (6) | conjunct (5) |
| `extensions/agi/tests/test_workflow.py:1956` (section header) | conjunct 5 (timeout) | conjunct 5 — already correct, unchanged |
| `extensions/agi/tests/test_workflow.py:2057` | conjunct (6) | conjunct (5) |
| `extensions/agi/tests/test_workflow.py:2155` (section header) | conjunct 4 (tree) | conjunct 3 |
| `extensions/agi/tests/test_workflow.py:2163` | conjunct (4) | conjunct (3) |

Two sites the brief did not name but the falsifier covers ("any ordinal still disagrees … anywhere it appears"): the two `test_workflow.py` section headers and the timeout test docstring, which the brief's grep for the hypothesis name would have missed because they carry only the bare ordinal. Also note `workflow.py:1324` abbreviates the hypothesis as `marker-dead-code-and-truncation` on a continuation line — the brief's warning about multi-line comments is real and the grep that catches it is the abbreviation grep.

experiment `a00-c2613ff6-31b78c`'s `probes:` carried `[2,2,3,4,6,6,5]` — also +1 — and now reads `[1,1,2,3,5,5,4]`. Edited with `write.py` only, after a `--dry-run` that printed the 7-probe list; `verdict`, `confidence`, `parents`, `evidence_runs` and the body are untouched, and the `cmd`/`expected`/`observed`/`result` text is byte-identical (ordinals only, no re-measurement). Its `thought` was rewritten to say why this version differs (the previous version's thought was the SD.06 parent review, whose text is now in the grid history of that file).

### Conjunct 2 — the notice surface has a committed fixture test

Pre-fix there was **no test in `extensions/agi/tests/test_dispatch.py` that exercised the notice surface** — the parent's own in-process probe was the only thing that had ever run it. New test `test_openrouter_preflight_prints_the_sub_floor_notice_before_the_account_refusal` (`test_dispatch.py:1548-1592`) drives the REAL `dispatch.main()` on the REAL pre-flight: an `_guard_project`-shaped graph with `harnesses.pi.provider = openrouter`, `check_runtime_key_usable -> (True, None)`, `check_key_floor -> (True, 'M')`, `check_account_floor -> (False, 'X')`, `AGI_AGENT_ID`/`AGI_SEAT` cleared, and `dispatch.subprocess.Popen` recorded. It asserts `rc == 1`, `notice: M` on stderr, `ERR: X` on stderr, `notice` **before** `ERR`, and `spawned == []`.

One honest note on the fixture: the graph needed `harnesses.pi.allowed_extra` (not the legacy `allowed_models`) because the model-allowlist gate now DERIVES from ladder rows + `allowed_extra`; `allowed_models` still works but prints a legacy warning. That is a fact about the current bytes, not a defect I introduced.

### Conjunct 3 — `--dry-run` and the live run agree on `timeout_s`

The budget-resolution loop was **hoisted above the `if dry_run:` block** in `run_workflow` (`workflow.py:1637-1662`), so there is ONE resolution and ONE refusal path: `--dry-run` now refuses an invalid `timeout_s` by name with the same rc the live run gives, instead of printing the credential line, every dispatch line and `[summary]` and exiting 0. A valid budget is unchanged (the control test asserts `rc == 0` with the dispatch and summary lines). Justification for hoisting rather than duplicating: the existing credential-decision principle in this file is exactly this — one decision helper read by both the dry-run print and the live mint — so the budget joins it as a second read-only decision made once.

### Conjunct 4 — a distinct return code, and no key for a refused run

Return codes in use before this round (`grep -n 'return [0-9]'` on `workflow.py`): **0** success, **2** resolve failure, **3** a pi stage exited non-zero (`_run_stage_pi` return 3), **4** a stage's return could not be parsed (`_run_stage_pi` `return 4, None` at the `_resolve_lenient_return` handler). The timeout refusal returned **4** — the same value, so a caller could not tell "refused before any stage ran" from "a stage ran and returned unparseable output". The collision is named: `4 == stage JSON/return-parse error`. The refusal now returns **5** (`workflow.py:1660`), unused anywhere else, and the module docstring gained a `RUN exit codes` block documenting all five. The ordering half was already correct in the bytes and is now pinned by a test: the resolution loop sits ABOVE `_resolve_workflow_spawn_env` (`workflow.py:1663-1664`), so a refused manifest mints nothing.

## Evidence

### Red first, then green (conjuncts 2, 3, 4)

Each red run was produced by temporarily reverting the source edit in this same worktree (edit tool only — no git) and restoring it in a `finally`; the restore is asserted byte-identical.

Conjunct 2 — the notice print removed from `dispatch.py`:

```
>       assert "notice: M" in err, err
E       AssertionError: warn: config harnesses.pi.allowed_models is legacy; ...
E         ERR: X
E         
E       assert 'notice: M' in '...\nERR: X\n'
extensions/agi/tests/test_dispatch.py:1591: AssertionError
1 failed, 121 deselected in 0.19s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k sub_floor_notice
1 passed, 121 deselected in 0.36s
```

Conjunct 3 — the resolution block moved back below the dry-run return:

```
>       assert rc == 5, (rc, text)
E       AssertionError: (0, '[run-key] review\n[credential] inherited env (provisioning unavailable)\n[dispatch] only :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium\n[summary] workflow=review harness=pi stages=1 via dispatch.py kids\n')
E       assert 0 == 5
1 failed, 1 passed, 73 deselected in 0.19s

$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -k "dry_run_refuses_an_invalid_timeout or dry_run_still_green"
2 passed, 73 deselected in 0.30s
```

Conjunct 4 — the refusal's `return 5` put back to `return 4`:

```
E       AssertionError: 4
E       assert 4 == 5
extensions/agi/tests/test_workflow.py:2190: AssertionError
1 failed, 74 deselected in 0.18s
```

That red run also shows both arms in one output: the parse-error arm printed `workflow.py: workflow=review failed at stage only (rc=4)` and the refusal arm printed `refused: … not a positive number of seconds`. On the built bytes the two rcs are 4 and 5.

### The suite

```
$ python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_workflow.py extensions/agi/tests/test_provisioning.py -q
274 passed, 5 skipped, 2 warnings in 77.01s (0:01:17)
```

The two warnings are the pre-existing `datetime.utcnow()` DeprecationWarning in `node_writer.py:1244`, unrelated to this round.

### One thing that is a GUARD, not a red-first fix

The mint half of conjunct 4 — `test_no_per_run_key_is_minted_for_a_timeout_refused_run` — is green on the PRE-fix bytes, because the resolution loop already sat above `_resolve_workflow_spawn_env`: the live path already spent no key on a timeout-refused manifest. What was missing was the dry-run parity (conjunct 3) and any test pinning the ordering. I report it as a guard rather than dress it up as a red-first fix.

## Agent Notes
Renumbered every +1 ordinal (8 code sites + 4 test sites + experiment a00-c2613ff6-31b78c probes [2,2,3,4,6,6,5]->[1,1,2,3,5,5,4] via write.py); added the committed notice-surface fixture test driving real dispatch.main() (red-first, zero spawns); hoisted timeout_s resolution above the dry-run return so --dry-run refuses rc 5 exactly as live (red-first); gave the refusal its own rc 5 distinct from the stage parse-error rc 4 and pinned no-mint ordering; 274 passed, 5 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-817a765c) of this version, SD.08. UPHELD as proved.

WHAT THE INSTRUCTION SAID: "A kid's tests are its CLAIM, not your evidence ... Run one negative probe per claim conjunct yourself and record them as `probes:`; a kid that passes its own suite but fails your probe is lean_disproved with the probe named". And: "a timeout-refused run still consumes a key with nothing recording it, or its return code is still indistinguishable from a stage parse error" is the falsifier.

WHAT THE MACHINE ACTUALLY DOES, read off the bytes and my own probes, not the report:
- conjunct 1: dispatch.py:2087 `conjunct (1)`, provisioning.py:358 `conjunct (1)`, workflow.py:918+1034 `conjunct (3)`, workflow.py:1335 `conjunct (2)`, workflow.py:1557/1719 `conjunct (5)`; no `conjunct (6)` remains in workflow.py. experiment:a00-c2613ff6-31b78c probes read [1,1,2,3,5,5,4] with verdict/confidence/parents/evidence_runs untouched.
- conjunct 2: the committed test is at test_dispatch.py:1548+ and drives the REAL dispatch.main() with check_key_floor->(True,'M') / check_account_floor->(False,'X'), asserting err.index("notice: M") < err.index("ERR: X") and spawned == []. My independent probe drove the same path and was RED with the notice print replaced by `pass` (AssertionError "'notice: M' not in stderr", stderr carrying only "ERR: X") and green with it restored, source byte-identical.
- conjunct 3: the budget-resolution loop now sits ABOVE the `if dry_run:` block (workflow.py:1647-1660), so one resolution and one refusal path. My spy on workflow._resolve_stage_timeout saw ['only'] during --dry-run (pre-fix ordering would give zero calls), and timeout_s=0 / stage -1 / stage '600' all returned rc 5 under --dry-run with no [dispatch]/[summary].
- conjunct 4: the refusal returns 5 at workflow.py:1660, distinct from _run_stage_pi's parse-error `return 4, None` at workflow.py:1505; resolution precedes _resolve_workflow_spawn_env at workflow.py:1663. My probe with mint patched recorded minted == [] and seen == [] for a timeout_s=0 run.

NEAR MISS (the part the report glossed): the kid's conjunct-4 mint test is green on the PRE-fix bytes — the resolution loop already sat above the mint, so it is a GUARD pinning existing ordering, not a red-first fix. The kid disclosed this honestly, which is why it is a caveat and not a demotion; but a reader who takes "four conjuncts red-first" at face value would be wrong about that half. Second near miss, mine: after renumbering, `conjunct (4)` now appears in workflow.py legitimately referring to THIS SD.08 residue hypothesis, so a naive greppable falsifier ("any conjunct's ordinal still disagrees") will produce false positives unless the scan is scoped by the hypothesis id in the same window — my first probe run failed exactly that way.

CAVEAT: the falsifier's letter for conjunct 4 offers "either a tracking row or skip the mint entirely"; the round proves the skip-the-mint arm only, and the tracking-row arm is untested. That is sufficient because the bytes show the refusal precedes the mint, so the row can never be needed — but it is one half of an OR stated and not exercised.

SUITE: 274 passed, 5 skipped on test_dispatch+test_workflow+test_provisioning (the 2 warnings are the pre-existing datetime.utcnow() deprecation in node_writer.py).
<!-- THOUGHT:END -->

PARENT REVIEW a00-817a765c: upheld as proved. Four conjuncts verified on the bytes with four independent parent probes added to this node's probes list -- ordinals all agree with the parent's (1)-(5) list (probes [1,1,2,3,5,5,4]); the notice fixture drives real dispatch.main() and is RED pre-fix; the timeout resolver now runs above the dry-run return so --dry-run refuses rc 5 exactly as live; rc 5 is distinct from the stage parse-error rc 4 and a refused run mints nothing. Cautions recorded in the thought: the no-mint half is a guard (green pre-fix), and the OR's tracking-row arm is untested. Suite 274 passed / 5 skipped.
