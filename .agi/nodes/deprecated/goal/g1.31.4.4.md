---
id: goal:g1.31.4.4
mint_id: 8dc1817e15ca453a889323785a00652c
type: goal
parents:
  - goal:g1.31.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 3d97f9f7b2e9fb44
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - workflow
title: "G1.31.4.4: workflows config-max -- the config row reaches the .js scripts, review.json and the .js are one form, leak whitelist is path containment"
town: core
---
# goal:g1.31.4.4

## Why this exists
goal:g1.31.4: PASS B3 (trunk @578650193, re-located at HEAD ff09c6101) upheld 3 residues on the workflow runner's two-copy surface, council LANES #14 #16 #17 (DG6, workflow.py cluster):
- `l3w4-workflows-config-maxxed` — `.agi/sessions/workflows/runs/mur-pb3chunk19of20/verify_l3w4-workflows-config-maxxed.json`, 2 upheld (items 1, 3).
- `l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful` — `.agi/sessions/workflows/runs/mur-pb3chunk18of20/verify_l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful.json`, 1 upheld (leak whitelist).

```
config.json workflows.review/drafting ──X──> agi-round-review.js:88,89,91  model:'sonnet' effort literals
                                     ──X──> agi-brief-drafting.js:7-8     || 'sonnet' / || 'max'
workflow.py:2600  Workflow({name, args})   <- raw caller args, not knobs[...]
review.json:12-37 (global prompt+schema)  !=  agi-round-review.js:33-48,58-  (write_guard, 4 schema fields, RULES :9)
test_workflow.py:934-947  compares label: strings only
test_workflow.py:1474     str(wf_dir).startswith(tempfile.gettempdir())   <- no resolve(), no separator
```

## Target end-state
- `extensions/agi/workflows/agi-round-review.js:88,89,91` and `agi-brief-drafting.js:7-8` carry no model/effort literal; both read `args.model` / `args.effort`, and `workflow.py:2600` (the claude-code seam) emits the resolved `knobs[...]` from `.agi/config.json` `workflows.review` / `workflows.drafting` inside the Workflow args, so the config row reaches the claude-code path.
- `review.json` global-checks prompt + schema (:12-37) and `agi-round-review.js` `globalPrompt` / `GLOBAL_SCHEMA` (:33-48, :58) are ONE form: same checklist (incl. `write_guard.py check`), same schema fields (`guard_output`, `unexpected_files`, `suite_skipped`, `suite_failures`), same read-only RULES (:9); `test_workflow.py:934` compares prompt and schema bytes, not labels only.
- `test_workflow.py:1474` whitelists a leak by path containment (`Path(wf_dir).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())`), never a string prefix.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- The pi path keeps resolving model from `harnesses.pi.models` by role; no `model` is added to a pi-provider `workflows.*` row (hypothesis:l3-workflow-model-crosses-harness-namespace).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider` passes, and `grep -q 'write_guard.py check' extensions/agi/workflows/review.json` and `grep -q unexpected_files extensions/agi/workflows/review.json` and `grep -q 'args.effort' extensions/agi/workflows/agi-round-review.js` each exit 0.
2. Negative: `git grep -nE "model: '(sonnet|opus|haiku)'|\|\| '(sonnet|max)'" -- extensions/agi/workflows/agi-round-review.js extensions/agi/workflows/agi-brief-drafting.js` and `git grep -n 'startswith(tempfile.gettempdir())' -- extensions/agi/tests/test_workflow.py` return zero hits.

## Out of scope
goal:g1.31.4.5 (box literals + engine root) · goal:g1.31.4.6 (missing tests + lost warnings) · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
