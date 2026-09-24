---
id: experiment:a00-6d16e1db-five-routes
mint_id: 04e2d82670c6489297bf8637f53ff2f5
type: experiment
parents:
  - hypothesis:a00-6d16e1db-6d95b2
next_edges: []
confidence: 0.9
edited_by: a00-6d16e1db
evidence_runs:
  - experiment:a00-6d16e1db-five-routes
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: stealth/space-bunny-alpha
production_lines: 5
profile: balanced
role: kid
scaffold_hash: e0b6e0a97ca3e941
season: 2
title: Director cold brief exposes five routes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6d16e1db-five-routes

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

# experiment:a00-6d16e1db-five-routes

## Experiment

I identified `extensions/agi/briefs/director-belam-duties.md` as the
canonical cold director-seat custom-instruction artifact: the director duties
file is the first-line pointer carried by the post card, and it already owns
the standing route vocabulary. I made the smallest artifact change there,
expanding the existing route line into five explicit route→seam entries:

- `write` → `write.py`
- `read` → `commands.py` (with viewport for see/read)
- `send` → `send.py`
- `dispatch` → `dispatch.py` + `workflow.py` (one router)
- `rotate` → `rotate.py`

I added one focused test in `test_brief.py` that reads the shipped artifact
and requires every route and seam. No engine vocabulary or special grok route
was added.

## Evidence

`python3 -m pytest extensions/agi/tests/test_brief.py -q` → 151 passed,
1 unrelated pre-existing failure: `test_g15_rule_with_no_project_root_keeps_the_current_fallback`
(the parent brief's g15 rule was not present under this worktree's fallback
resolution). The new test passed. Production diff measurement:
`git diff --numstat` → 5 added lines in the brief, 16 test lines excluded from
production.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Targeted rerun passed: python3 -m pytest extensions/agi/tests/test_brief.py -q -k cold_seat_brief_names_all_five_unified_routes (1 passed). The full file also exposed one unrelated existing g15 fallback failure.
<!-- THOUGHT:END -->

## Agent Notes
Expanded the canonical director duties brief with all five pane-facing routes and exact existing engine seams; added an artifact-level test.
