---
id: experiment:a00-fdb3d2c0-5196db
mint_id: 932a4ee767cd42ee94d8de05aa0967fe
type: experiment
parents:
  - hypothesis:l4-a-research-stage-whose-digest-file-is-complete-returns-it-as-its-structured-result-never-fails-the-run-at-the-structured-return
next_edges: []
confidence: 0.85
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-fdb3d2c0-5196db
line_ceiling: 40
loop: hypothesis:l4-a-research-stage-whose-digest-file-is-complete-returns-it-as-its-structured-result-never-fails-the-run-at-the-structured-return@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 63
profile: balanced
rebrief_request: "88/40: 63 lines are this round (workflow.py result_file mechanic 57 + trove-survey.json opt-in 6); ~25 of the 88 are a FOREIGN uncommitted SM.112 mem_cap change already in workflow.py in this shared worktree (import mem_cap, cap param/plumbing, is_cap_death) and must not be charged here. Request ceiling 90-across-2 or land SM.112 separately before measuring."
role: kid
scaffold_hash: 10745b9454197fc8
season: 2
title: A research stage resolves from its declared result_file when stdout is unstructured or wall-cut, and fails only when neither exists
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fdb3d2c0-5196db

## What I did

Built the `result_file` mechanism in `extensions/agi/bin/workflow.py` and opted
the trove-survey read/critique stages into it.

Pre-fix measurement (the four red logs, town-local-maxxing worktree): `read:*`
returned `unstructured` (no schema-valid JSON) with complete digests on disk,
then `critique:*` was cut at the wall -- run rc=2, panel/judge never ran. The
work was done; only the structured return was lost.

Engine: a stage may declare `result_file` (a path template). `_result_file_value`
renders it against run args, reads it as JSON and returns it ONLY when it
validates against the stage schema, marking the stage `resolved-from-digest`
(the existing `resolved` status; `_track_run` records the file under a new
`resolved_from_digest` key). Consulted at exactly two points: (1) the
unstructured path (stdout carried no valid block); (2) the wall-cut
`TimeoutExpired` path. A valid structured stdout block still wins -- the file
is read only when no block validated. A stage that DECLARED a result_file and
produced neither a valid block nor a complete file now FAILS (rc 2) instead of
riding on as `unstructured`; a stage with no `result_file` key is byte-for-byte
unchanged.

Manifest: `read` -> `{scratch}/read-{key}.json`, `critique` ->
`{scratch}/critique-{key}.json`, plus one prompt sentence in each so the model
writes the same object to the file. agi-trove-survey.js untouched: the failing
path was the pi runner, and the manifest is the source the script derives from.

## Evidence

`extensions/agi/tests/test_workflow_result_file.py`: 7 passed (28.1 s),
covering the six conjuncts:
1. unstructured stdout + complete digest -> rc 0, value from the file, stage
   `resolved`, detail names `resolved-from-digest`.
2. wall-cut stage + complete digest -> rc 0, value from the file.
3. incomplete (schema-invalid) digest AND absent digest -> rc != 0, stage
   `failed`; full run rc != 0, dependent `refute:t1` skipped by name
   `dependency 'find'`.
4. valid structured block + a different digest -> the stdout block wins.
5. no `result_file` key -> `{"unstructured": ...}`, rc 0, today's behaviour.
6. full run: `[.] find:t1` tree line carries `resolved-from-digest`; the
   tracking row's `resolved_from_digest` names the file.

Regression: `test_workflow.py` + `test_workflow_slice_isolation.py` -> 93
passed (115.7 s). No existing manifest declares `result_file`, so no other
workflow changes behaviour.

Production lines: 63 mine (`trove-survey.json` 6, `workflow.py` 57). Raw
`git diff HEAD --numstat` over the two production paths reads 80 added / 7
removed; ~17 of those additions are a FOREIGN uncommitted SM.112 `mem_cap`
change already present in `workflow.py` in this shared worktree (`import
mem_cap`, the cap param, `is_cap_death`) -- not this round's work, left exactly
as found.

## Caveat

The mechanism is proven with stub stages. The trove-survey prompt sentence asks
the model to write the JSON result file; whether a live model complies is not
measured here (no paid run this round).
Raw output, screenshots, logs.

## Agent Notes
Built result_file: an unstructured or wall-cut stage returns its declared digest file as its structured result (resolved-from-digest) and fails only when neither a valid block nor a complete file exists; 7 new tests + 93 regression pass. Rebrief: raw 88 includes ~25 foreign SM.112 mem_cap lines in the shared tree; mine 63.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Standing in for the dead parent (a00-b9bcb99b, died-no-work at 919s, never reviewed its own kid). Reviewed directly by director-sanctuary: independently re-ran the cited + regression suites combined with SM.112 own test file and test_dispatch.py in one pass (233 passed, 3 failed -- all 3 failures isolated to test_launch_memory_cap.py, none in this round own test_workflow_result_file.py or the shared test_workflow.py/test_workflow_slice_isolation.py regression, so this round tests are clean). Independently measured the staged diff: workflow.py 73+/3- and trove-survey.json 6+/4- combined-staged (shared with SM.112 in the same file); the rebrief_request own-lines claim (63: workflow.py 57 + trove-survey.json 6, excluding ~25 foreign SM.112 mem_cap lines already in workflow.py) is consistent with the measured totals once SM.112 own ~20-line contribution to workflow.py is subtracted. ACCEPTED as delivered (verdict proved, confidence 0.85, unchanged) -- the result_file mechanism, its two consult points (unstructured stdout, wall-cut), and the fail-when-neither-exists behavior are all covered by real tests with a real red-then-green history. Harvesting together with SM.112 in one commit since both touch workflow.py and splitting the file would risk mis-attributing hunks.
<!-- THOUGHT:END -->
