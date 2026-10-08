---
id: hypothesis:pb3-workflow-knobs-reach-js-one-global-form
mint_id: 8bcdbe0c616f42938d9c635af3ebeafe
type: hypothesis
parents:
  - goal:g1.31.4.4
next_edges: []
edited_by: director-general-6
scaffold_hash: 2cfb503db576adf7
season: 2
testable_claim: workflow.py's claude-code seam emits the resolved model/effort from .agi/config.json inside the Workflow args and agi-round-review.js / agi-brief-drafting.js read them with no model or effort literal; review.json's global-checks prompt and schema equal agi-round-review.js's (11 props, 9 required, write_guard step, RULES), compared by a test on schema bytes not labels; the leak fixture whitelists by resolved path containment.
title: The claude-code seam hands the resolved config knobs to the .js scripts, review.json and the .js share one global form, the leak fixture uses containment
town: core
---
# hypothesis:pb3-workflow-knobs-reach-js-one-global-form

## Measured
```
.agi/config.json workflows.review.effort=medium · workflows.drafting.effort=max · harnesses.claude-code.models{kid,parent,director}
        │ resolved into knobs[label] by _resolve_knobs + _resolve_harness_model (workflow.py)
        ╳ the claude-code seam (workflow.py, `if _claude_code_seam_present()`) writes Workflow({name, args}) = the caller's RAW args
agi-round-review.js   agent(..., model: 'sonnet', effort: 'low'|'medium'|'medium')   3 literal pairs (global-checks, review:*, ladder:*)
agi-brief-drafting.js MODEL = args.model || 'sonnet' · EFFORT = args.effort || 'max'  2 literal fallbacks
review.json global-checks   schema props 5 · required 3 · no RULES block · no write_guard step
agi-round-review.js GLOBAL_SCHEMA  props 11 · required 9 (guard_output, unexpected_files, suite_skipped, suite_failures, …) · RULES read-only block
test_review_and_drafting_stage_json_matches_js_prompts   compares label: strings only -> green while the two forms diverge
_no_workflow_row_leaks_to_real_sessions   str(wf_dir).startswith(tempfile.gettempdir())   no resolve(), no separator
```
- Verdict files: `mur-pb3chunk19of20/verify_l3w4-workflows-config-maxxed.json` items 1, 3; `mur-pb3chunk18of20/verify_l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful.json` (leak whitelist). Residue, open at HEAD.

## CLAIM
(1) The claude-code seam emits the RESOLVED knobs inside the Workflow args: `model`/`effort` when every stage resolved one pair, else `knobs: {<label>: {model, effort}}`; `agi-round-review.js` and `agi-brief-drafting.js` read them (`args.knobs[label]` else `args.model` / `args.effort`) and throw by name when no model arrived — no model or effort literal remains in either script.
(2) `review.json`'s global-checks stage and `agi-round-review.js`'s `globalPrompt` / `GLOBAL_SCHEMA` are ONE form: same checklist (incl. `write_guard.py check` and the untracked-file classification), same schema (11 props, 9 required), same read-only RULES; a test compares the schema objects (the .js evaluated with node, the harness `test_workflow_template_seam_js.py` already uses) and the checklist lines, not labels.
(3) The leak fixture whitelists by path containment: `Path(wf_dir).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())`.

## Dispatch line
config-max: the knobs already live in `.agi/config.json` `workflows.review.effort` · `workflows.drafting.effort` · `harnesses.claude-code.models.<role>`; nothing new — the seam carries them. The pi path stays on `harnesses.pi.models` by role; no `model` is added to a pi-provider `workflows.*` row (hypothesis:l3-workflow-model-crosses-harness-namespace).
template-max: the global-checks prompt + schema are one text; review.json is brought up to the .js form (the richer, the one the claude-code route runs).
code: the seam's args merge (workflow.py); the .js knob reads.

## FALSIFIERS
- `git grep -nE "model: '(sonnet|opus|haiku)'|\|\| '(sonnet|max)'" -- extensions/agi/workflows/agi-round-review.js extensions/agi/workflows/agi-brief-drafting.js` returns a hit
- `workflow.py run review --harness claude-code` under the seam prints a `Workflow(...)` line whose args lack the resolved model/effort, or carry a value that differs from the `stage_resolved` line
- a `workflows.review.effort` change does not change the emitted Workflow args
- review.json global schema != the .js GLOBAL_SCHEMA (props or required), or `write_guard.py check` / `unexpected_files` absent from review.json
- a `wf_dir` of `<tmp>X/...` (sibling prefix) or a symlinked tmp passes the fixture as not-leaked / is wrongly flagged
- a pi-provider `workflows.*` row gains a `model`

## TESTS
- `test_workflow.py`: replace the label-only parity test with a schema + checklist comparison (node-evaluated .js, skip only when node is absent, as `test_workflow_template_seam_js.py` does); + a seam row: config effort X -> the emitted Workflow args carry X and the harness model; fix the fixture line.
- `test_workflow_template_seam_js.py`: + the two scripts throw on a missing model (no literal fallback).
- Neighbourhood: `python3 -m pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_workflow_template_seam_js.py extensions/agi/tests/test_workflow_template_seam_json.py -q -p no:cacheprovider --basetemp /tmp/pb3wf`
- Leaf falsifier: `grep -q 'write_guard.py check' extensions/agi/workflows/review.json` · `grep -q unexpected_files extensions/agi/workflows/review.json` · `grep -q 'args.effort' extensions/agi/workflows/agi-round-review.js` · `git grep -n 'startswith(tempfile.gettempdir())' -- extensions/agi/tests/test_workflow.py` = 0 hits.

## FILE SCOPE
extensions/agi/bin/workflow.py · extensions/agi/workflows/agi-round-review.js · extensions/agi/workflows/agi-brief-drafting.js · extensions/agi/workflows/review.json · extensions/agi/tests/test_workflow.py · extensions/agi/tests/test_workflow_template_seam_js.py

## CEILING
kids <= 3 (A: seam + two .js knob reads · B: review.json one form + parity test · C: leak fixture, test-only) · 10-12 production lines per conjunct (review.json prompt/schema text counts as template, not production) · pi-free parents · 0 USD · CEILING measured by a TWO-operand numstat `<cut>..<tip before the paste commit>`, labelled so · the js-only `ladder:` advisor stage is out of scope (no review.json twin today) — record, do not build.
