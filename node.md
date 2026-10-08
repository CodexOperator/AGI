---
id: experiment:a00-a2fdcdc5-31ef26
mint_id: fca49acf52cd49a09737c3d7d7f9d914
type: experiment
parents:
  - hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order
next_edges: []
confidence: 0.85
edited_by: a00-a2fdcdc5
evidence_runs:
  - experiment:a00-a2fdcdc5-31ef26
line_ceiling: 10
loop: hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 83a12f997fb8f4b6
season: 2
title: config_max/template_max required by name in both live mur stages and a named first-answer line in the director brief
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-a2fdcdc5-31ef26

## Experiment

SM.125 third attempt (the prior two kids were demoted by the parent's own
probes). Built on this branch, from scratch:

1. `extensions/agi/workflows/merge-up-review.json` -- review AND verify stage
   schemas gain `config_max` and `template_max` as sibling top-level required
   properties, each byte-for-byte the owner's shape
   `{type: object, properties: {answer: {enum: [yes,no]}, where: {type: string}},
   required: [answer, where]}`. The review prompt gains the owner's two
   questions verbatim as step (8); the verify prompt gains a FRESH RESTATEMENT
   clause (plain prose, no `{config_max}` placeholder -- the render context
   would interpolate a dict repr).
2. `.agi/nodes/doc/unified-director-brief.md` -- via `write.py` only. The §1
   NODE bullet now ends with the named first-answer line:
   "config-max: <what moves to a cell> / template-max: <what moves to a
   template line> / code: <the trigger or resolver that does not exist>".
3. `extensions/agi/tests/test_config_max_template_max_required.py` (new, 7
   tests) -- (a) both live schemas require the fields with the yes|no enum
   asserted literally as `{"enum": ["yes", "no"]}`; (b) a return missing
   either is refused by `workflow.validate_return()` and the violation names
   the field; (c) a well-formed return validates with zero violations; (d) an
   out-of-enum `answer: "maybe"` is refused for both fields on both stages
   (the kid-2 regression); (e) exactly one brief line carries all three of
   `config-max:`, `template-max:`, `code:`.
4. `extensions/agi/tests/test_workflow_slice_isolation.py` -- the 4-line
   fixture fix: the fake review:r2 and verify:r2 returns now carry
   `config_max`/`template_max` with `{"answer": "no", "where": ""}`.

Code lines written: ZERO. `validate_return()` (workflow.py) already calls
real `jsonschema.validate()` and names a missing required field or an invalid
enum value; the round is schema DATA + brief text + tests.

## The round's own three answers

- **config-max:** no config cell. The `{answer, where}` shape, the owner's two
  questions and the yes|no enum are the rule itself, living in the workflow
  manifest and the brief -- not a value that belongs in `.agi/config.json`.
- **template-max:** yes -- the dispatch-order line belongs in a template /
  brief, which is exactly where it went (`doc:unified-director-brief` §1); the
  review wording is manifest prompt text, not code.
- **code:** the trigger/resolver already exists (`workflow.validate_return`,
  `extensions/agi/bin/workflow.py:937`); no new code line is needed.

## Evidence

`env -u TMUX -u TMUX_PANE python3 -m pytest
extensions/agi/tests/test_config_max_template_max_required.py
extensions/agi/tests/test_workflow_slice_isolation.py -q -p no:cacheprovider`
-> **17 passed in 3.13s**.

`env -u TMUX -u TMUX_PANE python3 -m pytest
extensions/agi/tests/test_workflow.py -q -p no:cacheprovider`
-> **93 passed in 124.25s** (no merge-up-review fixture broke).

Schema read back from the committed bytes:
`config_max` == `{'type': 'object', 'properties': {'answer': {'enum': ['yes',
'no']}, 'where': {'type': 'string'}}, 'required': ['answer', 'where']}` for
both review and verify; both stages list `config_max` and `template_max` in
`required` and neither is nested inside `verdicts.items`.

Production lines (`git diff --numstat` over the production paths): **0 code
lines** -- 80/-4 on the manifest (schema data + prompt text) and 2/-2 on the
brief node (the one named line). `line_ceiling` 10.

Exact done command (with `--owns` visible -- kid 1 lost its doc edit by
omitting it):

```
python3 extensions/agi/bin/cli.py done 129 a00-a2fdcdc5 \
  --verdict inconclusive_lean_proved:85 --confidence 0.85 \
  --node-id experiment:a00-a2fdcdc5-31ef26 \
  --parent hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order \
  --owns doc:unified-director-brief \
  --evidence-runs experiment:a00-a2fdcdc5-31ef26 \
  --notes "config_max/template_max required by name in both live mur stages; bad enum refused; named line in brief §1; 8+9 tests green"
```

## Agent Notes
config_max/template_max required by name in both live mur stages (answer enum asserted literally); bad enum refused for both fields both stages by validate_return; named first-answer line in brief Section 1 with THOUGHT; 7 new tests + 10 slice-isolation + 93 workflow tests green; zero production code lines
