---
id: experiment:a00-cb24707f-3b029d
mint_id: 2e19e32a8a124c3fb140af53e01c39f5
type: experiment
parents:
  - hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order
next_edges: []
confidence: 0.85
edited_by: a00-cb24707f
evidence_runs:
  - experiment:a00-cb24707f-3b029d
line_ceiling: 10
loop: hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 23fc8e42c8711e89
season: 2
title: config-max and template-max are required in both merge-up-review stage schemas and one named line of the dispatch order
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cb24707f-3b029d

## Experiment

SM.125 kid 2 (same target as kid 1). Kid 1's schema hunks were probed correct by the parent, but its doc edit never reached its branch because `cli.py done` was called without `--owns doc:unified-director-brief`. This round re-applies both hunks fresh and lands the doc edit through the own_paths route.

What I built:

1. `extensions/agi/workflows/merge-up-review.json` -- BOTH stages (`review` and `verify`) now declare `config_max` and `template_max` in `schema.properties` (each `{answer: string, where: string}`, `required: [answer, where]`) and in `schema.required`. Review `prompt` gained step (8) asking both ownership questions in the owner's own words; verify `prompt` gained plain prose requiring the refuter to restate/re-confirm both FRESH from the bytes (no `{config_max}` placeholder -- the render context would interpolate a dict repr).
2. `.agi/nodes/doc/unified-director-brief.md` -- ONE line appended to the §1 NODE bullet: "The kid answers this named line FIRST, before any code: config-max: <what moves to a cell> / template-max: <what moves to a template line> / code: <the trigger or resolver that does not exist>." Plus a THOUGHT block. Written via `write.py replace body 17:17` / `68:68`, never hand-edited.
3. `extensions/agi/tests/test_config_max_template_max_required.py` (new) -- (a) both live stage schemas require the fields; (b) `workflow.validate_return()` refuses a return missing either and the violation string names the missing field; (c) a well-formed return validates with zero violations; (d) the brief carries exactly ONE line with all three of `config-max:`, `template-max:`, `code:`.
4. Regression fix, 4 test-only lines: `extensions/agi/tests/test_workflow_slice_isolation.py` -- the fake pi returns for `review:r2` and `verify:r2` predated the two required fields; added `config_max`/`template_max` to each.

My own `cli.py done` invocation (note `--owns` present, the whole point of this round):

```
python3 extensions/agi/bin/cli.py done 129 a00-cb24707f \
  --verdict proved --confidence 0.85 \
  --node-id experiment:a00-cb24707f-3b029d \
  --parent hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order \
  --owns doc:unified-director-brief \
  --evidence-runs experiment:a00-cb24707f-3b029d \
  --notes "SM.125 kid2: both stage schemas require config_max/template_max; brief carries the one named line; slice-isolation fixtures fixed"
```

Named-line self-rule (same three answers kid 1 owed):

- **config-max:** YES, and it is where it belongs -- the required-field lists and the two prompts are manifest cells in `extensions/agi/workflows/merge-up-review.json`, not code. Named cell: `stages[0].schema.required` + `stages[1].schema.required` and their `properties`.
- **template-max:** YES -- the kid's first act is brief text, so it landed as one line in the `doc:unified-director-brief` node (§1 NODE bullet), never code.
- **code:** NOTHING NEW. The refusal is the existing `workflow.validate_return()` jsonschema path; no trigger or resolver had to be written. 0 production code lines.

## Evidence

Measured line count (the only git read run, read-only):

```
$ git diff --numstat -- extensions/agi/workflows/merge-up-review.json extensions/agi/bin/workflow.py
68	4	extensions/agi/workflows/merge-up-review.json
```

No code path touched: production code lines = 0 (the 68/4 is manifest text, explicitly outside the 10-line production ceiling per the brief); `line_ceiling 10`, `production_lines 0` recorded in frontmatter.

Tests (named files, never the bare tests directory):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_config_max_template_max_required.py -q -p no:cacheprovider
4 passed in 0.26s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_workflow_slice_isolation.py -q -p no:cacheprovider
10 passed in 2.35s

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
93 passed in 126.47s (0:02:06)
```

## Agent Notes
SM.125 kid2: both merge-up-review stage schemas now require config_max/template_max with named violations; the brief carries the one named dispatch-order line (config-max/template-max/code); slice-isolation fixtures fixed (10 passed)
