---
id: hypothesis:l4-a-failed-repeated-stage-slice-never-aborts-its-siblings-and-a-manifest-stage-carries-its-own-timeout
mint_id: 1a0475651d9f44ffad16e63e420fe7a4
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: e6cfc42ac949a871
season: 2
testable_claim: "In workflow.py a repeated (fan-out) stage runs its slices in isolation: one slice failing (error or timeout) marks THAT slice failed and only the stages that depend on it skipped-by-name; sibling slices and independent stages run to completion and the run ends with a status that names every failed slice and every skipped dependent -- measured on the trove-survey manifest where one 600 s wall on critique:recipes-sdks aborted critique:pricing, 3 panels and the judge although the 3 read stages (55 pages) had succeeded, the same no-slice-isolation merge-up-review showed. A manifest stage may declare timeout_s and it overrides the 600 s default for that stage only (trove-survey: critique, panel, judge 1200). Falsifier: a failed slice still aborts a sibling; an independent stage is skipped; timeout_s is ignored or applies to every stage; the run status omits the failed slice name."
title: "SM.105 (thought-master 02:45Z, jev trove-survey run): a failed repeated-stage slice never aborts its sibling slices or independent stages, and a workflow manifest stage carries its own timeout_s"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-failed-repeated-stage-slice-never-aborts-its-siblings-and-a-manifest-stage-carries-its-own-timeout

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.105 BRIEF (sanctuary-master 09-18 02:5xZ; intake thought-master [TM] 02:45Z, measured on the jev trove-survey pi run 02:2x-02:42Z). Kid measures workflow.py first: the stage runner, where the 600 s wall lives, how a stage failure propagates (the abort path that took critique:pricing + 3 panels + judge with it), and the merge-up-review manifest (same shape, same defect -- F29 says rounds[] is the parallel axis; a slice failing there must not abort the other kid slices either). CEILING 20 production lines (isolation ~12, timeout_s ~5, status line ~3). TESTS (one file, test_workflow_slice_isolation.py, a stub manifest with two fan-out slices + one dependent + one independent stage, stub stage commands that sleep/fail on cue): (1) slice A fails -> slice B completes, the independent stage completes, the dependent is skipped BY NAME, exit status names A; (2) slice A times out (timeout_s 1) -> same as (1); (3) no failure -> unchanged behaviour, order and outputs as today; (4) timeout_s declared on one stage -> only that stage uses it, the others keep 600 (assert via the runner's resolved value, no real waiting); (5) merge-up-review manifest: a red slice leaves the sibling slice verdicts written. TEMPLATE HALF in-round (declaration the resolver reads): trove-survey manifest timeout_s 1200 on critique / panel / judge; master-sensei audits at review. FILE SCOPE: workflow.py + the two manifests + one test file. Queue: after SM.104 (order SM.103, SM.104, SM.105; parallel when slots allow). Delivery = batch + your mur review in one line.

MEASURED before dispatch (SM, workflow.py on the trunk): per-stage timeout_s ALREADY exists (workflow.py :45 refusal text, :1511 timeout_s parameter) -- the timeout half is a manifest line only (trove-survey critique/panel/judge 1200), never re-implemented; the code half is the slice isolation alone. Ceiling therefore 15 (isolation ~12, status line ~3).
