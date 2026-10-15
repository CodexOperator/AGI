---
id: experiment:a00-5573f9e5-37fe6d
mint_id: 871176f5a14f41919e0148d83c46afbf
type: experiment
parents:
  - hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn
next_edges: []
confidence: 0.88
edited_by: a00-4d1de05a
evidence_runs:
  - experiment:a00-5573f9e5-37fe6d
loop: hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-spawn@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f201ee69325405c5
season: 2
title: A00 5573f9e5 37fe6d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5573f9e5-37fe6d

Slice B of the target hypothesis — conjunct **(h) ONLY**: a pi stage return must
be parsed leniently. Slice A (the per-run minted credential, conjuncts a–f)
landed in this same tree; nothing here touches it.

## Pre-fix measurement (the defect, reproduced on these bytes)

A fake pi bin echoing seven markdown findings with one stray `{` through
`run_workflow(".agi", "review", "pi", …)` on the **built** tree before the edit:

```
workflow.py: stage global-checks did not return JSON: no JSON object `{...}` found in stage output
workflow.py: workflow=review failed at stage global-checks (rc=4)
RC: 4
[stage] global-checks failed
[stage] review pending
[summary] workflow=review stages=2 ok=0 failed=1
```

The strict `_parse_last_json` (`text[find("{") : rfind("}")+1]`) lost a valid
review, cut the chain (the `review:t1` stage never ran), and recorded the run
failed with rc 4.

## What was built (workflow.py only)

1. **Schema-guided candidate scan.** New `_balanced_brace_spans()` (depth- and
   string-aware, so one stray brace cannot swallow the output),
   `_json_candidates()` (fenced ```json blocks first, then bare balanced spans)
   and `_resolve_lenient_return()` (the FIRST candidate that `json.loads`
   parses AND passes `validate_return(stage["schema"], value)` with no
   violations; a candidate that parses but fails the schema is **skipped, not
   fatal**). `_run_stage_pi` now calls this instead of `_parse_last_json`.
2. **Prose → `unstructured`, never a failure.** When no candidate validates the
   stage is recorded `unstructured` and `_run_stage_pi` returns
   `(0, {"unstructured": <text WHOLE>})` — rc 0, so the run continues and the
   chain is not cut. Genuine pi process failures (rc != 0, could-not-start)
   are untouched (rc 2/3 `failed`).
3. **The whole text in the view + row + status.** `RunView` gains an
   `unstructured` status/glyph `[?]` and `stage_unstructured(label, text)` which
   stores the text WHOLE (the tree flattens newlines for display only; nothing
   is truncated to 120). `summary()` prints
   `[summary] workflow=<key> stages=N ok=N unstructured=M failed=K`. `_track_run`
   adds `"unstructured": M` and `"returns": {label: <whole text>}`.
   `workflow.py status` prints `ok=… unstructured=… failed=…`.
4. **The text threads to the next stage as `prior`.** An unstructured return is
   an ordinary value in `prior_by_key`, so a `chained_from` stage renders with
   `{"unstructured": <whole text>}` in its context (`_SafeDict` means an absent
   `{answer}` still renders ""). No stage is special-cased as skipped.

## Post-fix measurement (same fake bin, same manifest)

```
workflow.py: stage global-checks returned no schema-valid JSON; recorded unstructured (88 chars)
workflow.py: stage review returned no schema-valid JSON; recorded unstructured (88 chars)
RC: 0
├─ [?] global-checks — ## Findings Seven findings follow. 1. {oops a stray brace …
└─ [?] review — ## Findings Seven findings follow. 1. {oops a stray brace …
[summary] workflow=review stages=2 ok=0 unstructured=2 failed=0
```

rc 0, the second stage ran despite the first being unstructured, and the whole
text is on the view/row.

## Tests (extensions/agi/tests/test_workflow.py)

A real fake pi executable (a python script echoing a fixed stdout, selected by
the prompt it is handed and by `$FAKE_PI_MODE`; it appends every prompt it
receives to `$FAKE_PI_CAPTURE`) drives `run_workflow` on the `review` manifest
with the sessions root redirected under tmp:

- `test_pi_bare_json_stage_is_ok` — bare schema-valid JSON → `ok`, summary
  `ok=2 unstructured=0 failed=0`.
- `test_pi_fenced_json_stage_is_ok_with_prose_around_it` — the same object in a
  ```json fence with prose before and after → `ok`, same stage statuses.
- `test_pi_prose_stage_is_unstructured_not_failed` — seven findings with a
  stray `{` → `unstructured`, rc 0, the NEXT (chained, repeated) stage still
  runs, the tracking row carries the WHOLE text (asserts a tail substring a
  120/200-char stub would have cut) under `returns`, the whole text reached the
  next stage's rendered prompt, and `workflow.py status` prints `unstructured=1`.
- `test_run_stage_pi_schema_violating_json_is_unstructured` — a JSON that parses
  but fails its schema (the old rc 5 path) is now skipped → `unstructured` rc 0.

## Evidence

```
python3 -m pytest extensions/agi/tests/test_workflow.py -q      -> 58 passed
python3 -m pytest extensions/agi/tests/test_provisioning.py -q  -> 71 passed, 5 skipped
```

Files changed: `extensions/agi/bin/workflow.py`,
`extensions/agi/tests/test_workflow.py`. Both under the 590 s ceiling
(0.85 s / 0.24 s). No git command was run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
conjunct (h) only: replaced the single-slice _parse_last_json in _run_stage_pi with a schema-guided candidate scan (fenced blocks then balanced-brace spans), prose-only now records unstructured rc 0 with the whole text kept in RunView/_track_run/status and threaded as prior. Updated the one existing summary assertion and the old rc-5 schema test to the new semantics; added 3 fake-bin run_workflow tests (bare/fenced/prose) plus a schema-violating-JSON test.
<!-- THOUGHT:END -->

## Agent Notes
conjunct (h) built: schema-guided lenient parse (fenced then balanced-brace), prose-only recorded unstructured rc 0 with whole text in RunView/_track_run/status and threaded as prior; pre-fix rc 4 reproduced, post-fix rc 0; 3 fake-bin run_workflow tests + updated schema test; test_workflow 58 passed, test_provisioning 71 passed/5 skipped

PARENT REVIEW L4.368 (a00-4d1de05a): judged from the staged DIFF (workflow.py +~200, test_workflow.py +~430), not the result file. (h) core holds. FOUR parent probes against the built bytes: (gate) the mur-tm-01-2 shape (markdown findings + a stray brace pair whose interior is not JSON) returns rc 0 and `{"unstructured": <whole text>}` — not failed, text NOT truncated; (wire/gate) a schema-INVALID JSON snippet placed before the real answer is SKIPPED and the first VALIDATING object is returned; (gate) a fenced ```json block is trusted over a decoy unclosed bare `{`; (wire) `_track_run` writes the WHOLE prose into the row\x27s `returns` (>900 chars, not the 120-char view stub). Caveat one: the kid REPLACED test_run_stage_pi_rejects_schema_violating_return (rc 5) with a test asserting rc 0/unstructured — a schema-violating JSON return no longer fails the run. This matches (h)\x27s literal reading (unstructured = no schema-VALID return, and `failed` counts process failures) but it IS a semantic change worth naming. Caveat two: (h) proved on throwaway fixtures, not on the live pi binary. Neither caveat falsifies the conjunct.
