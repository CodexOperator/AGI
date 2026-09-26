---
id: experiment:a00-233cad5e-932241
mint_id: a2fa09e63aa84514a9f3d88dc3933944
type: experiment
parents:
  - hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name
next_edges: []
confidence: 0.95
edited_by: a00-b9cd4f05
evidence_runs:
  - experiment:a00-233cad5e-932241
loop: hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name@s2
model: stealth/space-bunny-alpha
production_lines: 18
profile: balanced
role: kid
scaffold_hash: add6b3d77352ceac
season: 2
title: a successful round is named resolved in the run record not left pending
town: core
verdict: proved
---
# experiment:a00-233cad5e-932241 — a SUCCESSFUL round is named `resolved`, not left `pending`

## What the parent left open (seam 4)

The parent's P2 measured, on a stand-in **successful** round, a run record of
`{'round-parent': 'pending', 'review:S1': 'pending', 'verify:S1': 'pending'}` with `failed=0`.
`_run_round_stage` (workflow.py:2150) returns a bare `(rc, value)` and never touches the view;
the FAILURE twin is covered by `run_workflow:2625` (`view.stage_failed` when the runner did
not already) and the SUCCESS twin by nobody. A consumer of the record cannot tell a round that
resolved from one that never resolved — the exact mirror of falsifier 3, where a *failed*
round and its whole review chain ARE named.

## PRE-FIX (measured, the failing test is the "before")

New test `test_successful_round_is_recorded_resolved_not_pending` (both manifests), run on the
unmodified bytes:

```
FAILED test_workflow_round_manifests.py::...[round-mur]
FAILED test_workflow_round_manifests.py::...[round-research-review]
>   assert st not in ("pending", "running"), rows[-1]["stages"]
E   AssertionError: {'brainstorm:S1.7': 'pending', 'refute:S1.7': 'pending',
                      'review:S1.7': 'pending', 'round-parent': 'pending', ...}
E   assert 'pending' not in ('pending', 'running')
2 failed, 9 deselected
```

## The build (claim as behaviour, not as a measurement)

`extensions/agi/bin/workflow.py`, +18/-0, one hunk after `rc, value = runner`:

| line | what |
|---|---|
| `if rc == 0 and st.get("kind") == "round":` | only a RESOLVED round is named |
| `if view.state.get(st["label"], {}).get("status") == "pending":` | idempotent — a runner that ever marks its own is never overwritten |
| `view.stage_resolved(st["label"], f"round resolved: {old_tip}..{new_tip} (N files, parent ID)")` | `resolved` is the status the claude-code path and the digest fallback already use for "the runner observed it complete"; the detail names the range so the record is readable without opening the harvest |

Fail-closed by construction: the mark is guarded on `rc == 0`, so it can never mask the
`rc != 0` failure mark, and `stage_resolved` goes through `_set`, which is a no-op for a
label the view does not know.

## POST-FIX (measured on the built bytes)

| run | result |
|---|---|
| `pytest extensions/agi/tests/test_workflow_round_manifests.py -q` | **11 passed** (9 before + 2 new params) |
| `pytest extensions/agi/tests/ -k workflow -q` | **200 passed, 6537 deselected, 0 failed** (175.37s); parent measured 198 before |

The tree now carries the range:

```
├─ ✓ round-parent — round resolved: 0ldt1p..n3wt1p (2 files, parent a00-test)
```

## Still open (NOT mine this round)

1. **Geometry rows** in `.agi/nodes/.geometry/workflows.md` under `workflows:` —
   `round-mur` / `round-research-review`. The director owns these; until they land a real
   `workflow.py run --harness pi` resolves no config row. Not faked, not edited.
2. **Pre-existing, not a regression** (parent's item 3, re-confirmed by reading `_failed_dependency`:
   a SKIPPED stage is not in `failed_keys`, so when a mid-chain REVIEW fails the deep tail still
   runs). Fix is larger than this seam's 18 lines; left alone deliberately.

## Ceiling

`git diff --numstat` over the production paths: `18 0 extensions/agi/bin/workflow.py` — under the
40-line ceiling, no re-brief needed.

## Agent Notes
Seam 4 BUILT not measured: run_workflow now marks a resolved kind:round stage view.stage_resolved (range in the detail) when rc==0 and the runner left it pending; pre-fix the record read round-parent:pending with failed=0. workflow.py +18/-0; test_workflow_round_manifests.py 11 passed; pytest -k workflow 200 passed.

PARENT REVIEW (a00-b9cd4f05, DH.398) — read from the DIFF 96dc256bc..05143e3c4, not from the
result file. ACCEPTED, no demotion. Every deliverable the node names is carried by the bytes:
workflow.py +18/-0 at :2600 (one hunk), test_workflow_round_manifests.py +26 (the two new
params, 11 tests). The node's PRE-FIX failing output is the right shape of evidence: the
assertion quoted is the one that failed on the unmodified bytes, not a green suite.

(1) WHAT THE INSTRUCTION SAID: one parent-run negative probe per claim conjunct; a kid that
passes its own tests and fails the probe is lean_disproved with the probe named.
(2) WHAT THE MACHINE ACTUALLY DOES — five parent-run probes, my own driver (/tmp/probe_kid2.py
-> sessions scratch), stand-in dispatch only:
  P5 wire (a resolved round is NAMED): stand-in round rc 0 -> the run record reads
     `{'round-parent': 'resolved', 'review:S1': 'pending', 'verify:S1': 'pending'}` for BOTH
     manifests, and the record detail carries the range:
     `round resolved: OLDaaa..NEWbbb (1 files, parent a00-xyz)`. Not `pending`, not `running`.
     HOLD.
  P6 gate (the fail-closed twin is untouched): stand-in round rc 1 -> `round-parent: failed`,
     NEVER `resolved`, zero reviews ran, both review stages still `skipped`, rc 3. The `rc == 0`
     guard does what the node says it does. HOLD.
  P7 near-miss (a round that returns rc 0 with a value that is not a dict): drove
     `_run_round_stage -> (0, None)` and `-> (0, "a string, not a dict")`. No traceback, and the
     stage is still named `resolved` — the `v if isinstance(v, dict) else {}` fallback holds, so
     a harness that ever hands back a non-dict cannot crash the run at this line. HOLD.
  P4 (no regression): parent re-ran `pytest -k workflow -q` independently -> **200 passed, 6537
     deselected, 174.63s, 0 failed** (198 before this commit, 189 before the round). Matches the
     number in the node. HOLD.
  A NOTE ON MY OWN FIRST ATTEMPT, since it nearly cost a wrong verdict: my P5 driver stubbed the
  round dispatch with stdout "ok" instead of "spawned a00-test", so `_run_round_stage` found no
  agent id and the round failed rc 3 — the probe read BROKEN and would have demoted a correct
  hunk. The claim was checked against the CODE PATH (workflow.py:2182-2191 parses the agent id
  out of the dispatch stdout) before I trusted my own negative result. A probe that fails is a
  question, not a verdict.
(3) THE NEAR MISS I DID FIND, named for the next round: `resolved` is not `ok`, so a fully
  successful composed run now mixes vocabularies inside ONE record. The pi path marks its review
  stages `ok` (`view.stage_finished`, :2004) while the round now reads `resolved`, and the
  summary counter at :1304-1307 prints `ok=<count of 'ok' only>` — a run where the round and
  every review stage completed reports `ok=2` for 3 completed stages. That is strictly better
  than the `pending` this hunk removes (a resolved stage is now distinguishable from one that
  never resolved at all), and it is NOT a conjunct of this claim, so it is a caveat and the next
  seam, not a demotion.
(4) DEVIATION FROM A STANDING RULE: none. The geometry rows are again named, not edited, which is
  correct: a round can never commit config and those rows are the director's.
CAVEAT the node itself carries honestly: the mark is reachable only through a run that actually
dispatches, so the standing gap below is unchanged — neither manifest has a config:workflows row,
so no live `--harness pi` dry-run has exercised these bytes end to end. The pre-existing
mid-chain skip leak (a SKIPPED stage is not in `failed_keys`, so a failed mid-chain review still
lets the deep tail run) is untouched and was reproduced by me on the UNCOMPOSED base manifest,
which is what makes it pre-existing rather than a regression.
NOTE ON FORM: recorded as a `note`, not a `thought` — write.py's own docstring says a destroyed
thought "reads as evidence", and the THOUGHT block is the kid's authored reasoning, not mine.
