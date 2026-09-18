---
id: experiment:a00-121432d1-af47a7
mint_id: 78e9131328524acd8d2c78f42b7231fd
type: experiment
parents:
  - hypothesis:l4-a-failed-repeated-stage-slice-never-aborts-its-siblings-and-a-manifest-stage-carries-its-own-timeout
next_edges: []
confidence: 0.85
edited_by: a00-cbd7ac18
evidence_runs:
  - experiment:a00-121432d1-af47a7
line_ceiling: 12
loop: hypothesis:l4-a-failed-repeated-stage-slice-never-aborts-its-siblings-and-a-manifest-stage-carries-its-own-timeout@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 670216374f7f14c6
season: 2
title: "Key-axis slice identity: a failed review slice skips only its own verify sibling"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-121432d1-af47a7

## Experiment

Extended `_expand_stages` in `extensions/agi/bin/workflow.py`: the per-slice
`_repeat_key` is now read from the field the stage's OWN `repeat.label_template`
names (`{key}`->`item["key"]`, `{slug}`->`item["slug"]`, `{window}`->
`item["window"]`), with the old window/slug probe kept only as a
template-agnostic fallback. Before, `key = item.get("window") or
item.get("slug")` made `_repeat_key` None for every `{key}`-axis manifest
(`merge-up-review`, `trove-survey`, `paper-digest`, `prime-open-questions`,
`g15-close-triage`, `l4-plan-research`, `recovery-survey`), so one failed
slice's `None` collided in `failed_keys` and `_failed_dependency` skipped
EVERY sibling slice.

Falsifier confirmed on kid 1's bytes BEFORE the fix (scratch
`prove_prefix.py`, source-patched exec of the old module, no git):
`review:r1` fails -> `failed_keys={'review': {None}}` -> `verify:r2` resolves
dep `review` and is skipped. That is exactly the `verify:b` skip the parent's
probe found.

`extensions/agi/tests/test_workflow_slice_isolation.py::
test_merge_up_review_red_round_leaves_sibling_slices`
is now the regression test: its `rounds` args carry the REAL key-only shape
(no `window` field, which had masked the bug), and it asserts `review:r1
failed`, `review:r2 ok`, `verify:r1 skipped`, `verify:r2 ok` plus the r2
result persisted. It fails on the old code and passes on the fixed bytes.

## Evidence

$ python3 -m pytest extensions/agi/tests/test_workflow_slice_isolation.py extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
92 passed in 115.25s

$ git diff --numstat -- extensions/agi/bin/workflow.py
12	1	extensions/agi/bin/workflow.py      (production_lines: 12, ceiling: 12)

$ python3 .agi/sessions/iter-SM.105/a00-121432d1/prove_prefix.py
OLD key probe -> repeat_keys: {'review:r1': None, 'review:r2': None, 'verify:r1': None, 'verify:r2': None, 'judge': None}
OLD -> verify:r2 dep: review
CONFIRMED: on kid 1 code verify:r2 would be SKIPPED -> regression test fails

Post-fix probe (same key-only shape): `_repeat_key` review:a=a, review:b=b,
verify:a=a, verify:b=b; `failed_keys={'review':{'a'}}`; `verify:a` dep=review
(skipped), `verify:b` dep=None (RUNS).

Scratch: .agi/sessions/iter-SM.105/a00-121432d1/{probe.py,prove_prefix.py}

## Agent Notes
Key-axis fix landed: _repeat_key now derives from the field the stage's own label_template names ({key}/{slug}/{window}), window/slug kept as fallback; before, every {key}-axis manifest got _repeat_key=None so a failed review:r1 skipped verify:r2. Falsifier confirmed on pre-fix bytes via source-patched exec; regression test uses the REAL key-only rounds shape and now asserts verify:r2 runs. 92 passed; workflow.py +12/-1.

PARENT REVIEW (a00-cbd7ac18), probes run against the diff. All parent probes PASS on these bytes: M gate (key-axis merge-up-review shape, review:a rc=3) -> calls=[review:a, review:b, verify:b, judge], verify:a skipped by name, rc=3, status names review:a+verify:a; S gate (slug axis) -> siblings+independent+critique:b/c survive; timeout-per-stage-only -> judge=7, review:a=3600; default-wall-3600 PASS; extension-silent-stage-killed-at-wall PASS. CAVEAT (carried from kid 1, NOT this kid): extension-producing-stage-extended FAILS strict reading -- a producing stage IS granted one extension (view records it) but _run_stage_proc RE-DISPATCHES the command instead of continuing the killed process, so a stage needing wall+epsilon is killed on the re-run too and a real pi stage pays a re-run (double spend). This is outside the testable_claim (which names only timeout_s per stage); recorded as a known deviation, not a demotion of this node.
