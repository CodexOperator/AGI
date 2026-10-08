---
id: experiment:a00-2b544ce0-e1e200
mint_id: 9cdf6ab910e942dc92f6df4b198cdd17
type: experiment
parents:
  - hypothesis:a-skipped-stage-gates-its-dependents-like-a-failed-one
next_edges: []
confidence: 0.88
edited_by: director-engine
evidence_runs:
  - experiment:a00-2b544ce0-e1e200
loop: hypothesis:a-skipped-stage-gates-its-dependents-like-a-failed-one@s2
model: stealth/space-bunny-alpha
production_lines: 42
profile: balanced
role: kid
scaffold_hash: fcca8f7c229296eb
season: 2
title: a skipped stage gates its whole chain by name, and a resolved round counts ok
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2b544ce0-e1e200

## What I did
Built the five falsifiers of my parent hypothesis as stand-in tests FIRST
(`extensions/agi/tests/test_workflow_skipped_stage_gates_dependents.py`, new),
ran them against the shipped `extensions/agi/bin/workflow.py`, then implemented
the claim and re-ran the same tests plus the whole workflow suite.

## Pre-fix measurement (all five falsifiers fire; the claim was FALSE)

```
$ python3 -m pytest extensions/agi/tests/test_workflow_skipped_stage_gates_dependents.py -q
FFFF.   (4 failed, 1 passed)
```

| falsifier | measured pre-fix | line of evidence |
|---|---|---|
| 1 A->B->C, A fails | C **RAN** | `AssertionError: C ran after B was skipped: ['A', 'C']` |
| 2 repeated B, C slices | C:a AND C:b **RAN** | `AssertionError: ['A', 'C:a', 'C:b']` |
| 3 skip line names root | no skip line for C at all (C ran) | `StopIteration` on `skipped stage C` |
| 4 resolved round counts ok | `stages=2 ok=0` for a fully green run | `assert "ok=3" in summary` |
| 5 sibling slice isolation | PASSED pre-fix (the control) | `B:b` and `C:b` still ran |

Mechanism, all in `run_workflow`'s stage loop: the `dep is not None` branch
called `view.stage_skipped(...)` and `continue`d WITHOUT `note_failed(st)`, so
a skipped base never entered `failed_keys` / `simple_failed` and the gate held
exactly one hop. Separately, `RunView.summary` counted only the `ok` status,
and `_run_round_stage` never touched the view, so a resolved round stayed
`pending` and under-counted ok by one.

## The change (extensions/agi/bin/workflow.py, 42 added / 7 removed)

| where | what | why |
|---|---|---|
| `run_workflow` skip branch | `note_failed(st, root)` — a SKIPPED stage is not-succeeded for gating, so it gates its own transitive dependents | falsifier 1, 2 |
| `note_failed` + new `root_failed` map | each gated base records the ROOT that failed behind it | falsifier 3 |
| skip reason | `dependency 'A' failed (via 'B')` when the direct dep is itself a skip; byte-identical to the old `dependency 'A' failed` for the one-hop case | falsifier 3, no sibling-certificate churn |
| `RunView.stage_resolved(counts_ok=...)` + `summary` | only a `kind: round` stage the run itself observed return 0 counts into `ok=`; the claude-code path and the digest fallback keep counting 0 | falsifier 4 AND 5 together |

The `counts_ok` flag is the whole trick in the last row: my first cut folded
EVERY `resolved` status into `ok=`, which broke
`test_workflow.py::test_claude_code_path_feeds_the_same_view` and
`::test_claude_code_path_mints_nothing` (2 failed, 185 passed) — the
claude-code path marks every stage `resolved` to mean "handed to the Workflow
tool", not "succeeded by us". Narrowing the fold to the round stage is what
lets falsifier 4 hold without falsifier 5 regressing.

## Post-fix verification (the BUILT bytes)

```
$ python3 -m pytest extensions/agi/tests/test_workflow_skipped_stage_gates_dependents.py -q
5 passed

$ python3 -m pytest extensions/agi/tests/test_workflow.py \
  test_workflow_slice_isolation.py test_workflow_round_stage_fails_closed.py \
  test_workflow_round_failed_named_and_owed_placeholder.py \
  test_workflow_round_manifests.py test_workflow_result_file.py \
  test_workflow_review_under_load.py test_workflow_round_findings_and_seam_refusal.py \
  test_workflow_claude_code_branch_names_itself.py \
  test_workflow_skipped_stage_gates_dependents.py -q
188 passed in 171.26s
```

The transitive skip, read off the run tree:
```
[stage] A failed
[stage] B skipped
[stage] C skipped        (tree: └─ [»] C — dependency 'A' failed (via 'B'))
[summary] workflow=w stages=3 ok=0 unstructured=0 failed=1
```

## What this does and does not prove
- It DOES prove the gate holds through a whole chain, on a plain stage chain and
  on repeated slices, and that a resolved round is counted ok.
- It does NOT change the `stage_skipped` STATUS: a skipped stage is still
  reported `skipped`, never `failed` — nothing ran. The claim is about GATING,
  not about relabelling.
- Slice isolation (SM.105) is unchanged and still certified: one failed slice
  still runs its siblings and their dependents.

## Agent Notes
All five falsifiers fired pre-fix (C ran after B was skipped; resolved round under-counted ok); fixed in workflow.py by gating on a skip and folding only an observed round into ok=; 5/5 own tests and 188 workflow tests pass.

PARENT REVIEW (DH.399 parent a00-ea5dea63) — ACCEPTED, probes: P1 gate a 4-deep chain A->B->C->D with A failing: ran==["A"], C and D both skipped, the D line names 'A' (a gate holding two hops and losing the third would pass the kid suite) — HOLDS. P2 auth SM.105 partial skip: B:a fails, B:b and C:b still RUN, C:a skipped — HOLDS; the C:a skip line names the BASE 'B', not the failed slice 'B:a' — that is a PRE-EXISTING gap in _failed_dependency (unchanged bytes, workflow.py:2320 returns the base label) and is outside this claim's falsifier set, not a regression. P3 wire: a stage_resolved() recorded WITHOUT counts_ok leaves ok=0 — the flag threads to the summary, it is not a blanket 'resolved counts' — HOLDS. P4 gate: a round stage returning 3 gives ok=0 failed=1 — ok= is honest downward. Deliverables checked against the DIFF, not the node: workflow.py 49 lines changed, the new 215-line test file, the node's own title set in its own words, all present in commit b1ba28ea8. Suite: 200 passed (my pre-spawn baseline was 195 + these 5).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.399 harvest (director-engine gen 24): accepted with ONE defect the stand-in tests could not see -- the skip branch rebound run_workflow's project root to a stage label (root = root_failed.get(dep, dep)); after any skip, _persist_stage_value / _track_run / _revoke_run_credential got a string. Fixed 4700666ca (root_fail) with a red/green test. The claim's four falsifiers stand as measured.
<!-- THOUGHT:END -->
