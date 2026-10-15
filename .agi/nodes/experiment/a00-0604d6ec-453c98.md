---
id: experiment:a00-0604d6ec-453c98
mint_id: 9d5bf0c38ddd41728450bba8d1809fea
type: experiment
parents:
  - hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order
next_edges: []
confidence: 0.8
edited_by: a00-0604d6ec
evidence_runs:
  - experiment:a00-0604d6ec-453c98
line_ceiling: 10
loop: hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: dda51da8e55fc925
season: 2
title: "SM.125 kid: merge-up-review review+verify require config_max/template_max (refused by name) and the dispatch order gains the config-max/template-max/code line"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0604d6ec-453c98

## Experiment

SM.125 KID — conjuncts (1)-(3) of the parent testable_claim. Built, then
proved on the built bytes. FILE:LINE of every change:

1. `extensions/agi/workflows/merge-up-review.json`
   - review stage schema: `config_max` + `template_max` added to `properties`
     (each `{answer: yes|no, where: str}`, `required:[answer,where]`) and to
     the stage `required` list (raw lines ~63-98).
   - verify stage schema: the same two fields added as SIBLING top-level
     required properties (not nested in `verdicts` items), `required` list
     gains both (raw lines ~192-227).
   - review `prompt`: new step `(8) CONFIG-MAX / TEMPLATE-MAX ...` quoting the
     owner's own words (`.agi/config.json` / `.geometry` / schema for
     config_max; prompt/brief/order/rotation text for template_max; a yes =
     returned with the exact cell or line named).
   - verify `prompt`: appended prose requiring the refuter to restate
     config_max/template_max fresh. Branch taken: PROSE, not
     `{config_max}` placeholders — `chained_from` DOES merge the review return
     into the verify render context (workflow.py:1290-1295), but the value is a
     dict and `str(dict)` renders a Python repr into the prompt, not a clean
     answer. Prose is honest and costs zero code.

2. `.agi/nodes/doc/unified-director-brief.md` (via `write.py`, body line 16)
   — the §1 NODE dispatch-order shape gains ONE named line, answered FIRST
   before any code:
   `config-max: <what moves to a cell> / template-max: <what moves to a
   template line> / code: <the trigger or resolver that does not exist>.`
   A THOUGHT block records why (a §2 review-direction rule alone is wording;
   nothing makes a kid ANSWER before writing code).

3. `extensions/agi/tests/test_config_max_template_max_required.py` (new, 4
   tests): the two live schemas require both fields; a return missing either
   is refused by `validate_return` and the violation string NAMES the field;
   a well-formed return validates with zero violations; the brief carries all
   three sub-strings on ONE line. Reads the LIVE manifest and LIVE node, never
   a copied list.

## Evidence

Own test file:
```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_config_max_template_max_required.py -q -p no:cacheprovider
4 passed in 0.26s
```

Touched-neighbourhood run (`test_workflow.py`, `test_workflow_review_under_load.py`,
`test_workflow_result_file.py`, `test_workflow_slice_isolation.py`):
```
1 failed, 115 passed in 167.06s
FAILED .../test_workflow_slice_isolation.py::test_merge_up_review_red_round_leaves_sibling_slices
```
That failure is the claim WORKING, not breaking: the test's fake pi returns
for `review:r2` and `verify:r2` (test_workflow_slice_isolation.py:236-243) omit
the two new fields, so `validate_return` now refuses them by name —
```
workflow.py: stage review:r2 returned JSON that violates its schema (1 violation(s)):
  <root>: 'config_max' is a required property
```
The fixture must learn the resolver. Fix = add
`"config_max": {"answer": "no", "where": ""}` and
`"template_max": {"answer": "no", "where": ""}` to BOTH fake return dicts
(4 lines). That file is OUTSIDE my FILE SCOPE (my scope named only one NEW
test file, and the director brief §2 says a test-only fix <= 4 lines is the
Prime's call) — left untouched, reported here as a residue.

Measured production lines (`git diff --numstat` over the production path):
```
80  4  extensions/agi/workflows/merge-up-review.json
```
This is MANIFEST text (JSON schema + prompt strings), which the node's own
testable_claim exempts from the ceiling ("CEILING 10 production lines +
manifest/template/brief text"). CODE lines: 0 — `workflow.py:937`
`validate_return` already calls real `jsonschema.validate()` and names the
missing required property, so no new validation code was needed.

## The round answers its own named line (self-rule)

- **config-max**: none of my own diff. The schema strings and the one-line
  required-list entries ARE config/schema data and they live in the manifest,
  which is where they belong. Nothing in the diff is a value that wanted to be
  a `.agi/config.json` cell.
- **template-max**: the review prompt step (8), the verify prompt paragraph,
  and the brief §1 named line — all prompt/brief text pushed to the template
  and the brief node rather than baked into code.
- **code**: 0 production lines. The trigger (a stage return missing a required
  field) and the resolver (the existing jsonschema path) already exist; this
  round only declares the two fields required.

## Agent Notes
Built conj (1)-(3): merge-up-review.json review+verify stage schemas now REQUIRE config_max/template_max {answer:yes|no,where:str}; review prompt step (8) asks both questions in the owner's words; verify prompt restates them (prose branch -- a {config_max} placeholder would render a Python dict repr); doc:unified-director-brief body line 16 gains the ONE named dispatch-order line config-max/template-max/code via write.py plus a THOUGHT. 4 new tests pass (missing field refused by validate_return and NAMED; well-formed validates clean; brief carries all three substrings on one line). CODE LINES: 0 -- validate_return's existing jsonschema path names missing required properties, so no new validation code. RESIDUE (out of my file scope, Prime's call per brief S2): test_workflow_slice_isolation.py:236-243 fake returns for review:r2/verify:r2 omit the two fields and now fail validation -- a 4-line fixture fix; 115 passed, 1 failed in the touched-neighbourhood run.
