---
id: hypothesis:l4-town-base-honours-the-recorded-base-branch
mint_id: 692a62aa82c7438aacb74617628c25b8
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-are-one-tree-under-the-season
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 861e1cc61e71877d
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-2 (season correctness): season.py:1240-1243 resolves the merge base as `args.target or _town_base(nodes, town) or _recorded_field(record_path, 'base_branch') or _current_branch(git_root)` — `_town_base` PRECEDES the recorded `base_branch`, so a core-town round that carries a `--round`/agent.json record with `base_branch` set merges straight into season/s2, skipping its rung (regression on the l3w4 one-rung rule; reproduced by the review). CLAIM: the recorded `base_branch` wins over the town base whenever the record exists and names a branch (`args.target` still first, explicit beats recorded); `_town_base` is the fallback for a round with no record; the order is `target → recorded base_branch → town base → current branch`, and a `--dry-run`/print path names WHICH rung was chosen and WHY (source: target|record|town|current). TESTS in extensions/agi/tests/test_season*.py: a core round with a recorded base_branch = its rung merges into the rung; a town round with no record still resolves the town base; an explicit --target beats both. FALSIFIER: a recorded base_branch that is not the chosen base. VERIFY ON THE REAL TREE: run the resolver read-only (a probe that prints the chosen base for a real record under .agi/sessions/iter-L4.12x) — never a real merge. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/season.py (the base resolution region ONLY) + its tests. g15-3 (cmd_rollover) is a SEPARATE node serial behind this one on season.py. EXCLUDED: spawn_gate.py (g15-1), rotate.py, dispatch.py."
title: A core round with a recorded base_branch merges into its rung, never straight into season/s2
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-town-base-honours-the-recorded-base-branch

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 27 review by name (wf_6699487e-b72), goal:g15 newest note at 549b8f682, the prime's priority order. Line numbers on 549b8f682. g15-2 (season correctness): season.py:1240-1243 resolves the merge base as `args.target or _town_base(nodes, town) or _recorded_field(record_path, 'base_branch') or _current_branch(git_root)` — `_town_base` PRECEDES the recorded `base_branch`, so a core-town round that carries a `--round`/agent.json record with `base_branch` set merges straight into season/s2, skipping its rung (regression on the l3w4 one-rung rule; reproduced by the review). CLAIM: the recorded `base_branch` wins over the town base whenever the record exists and names a branch (`args.target` still first, explicit beats recorded); `_town_base` is the fallback for a round with no record; the order is `target → recorded base_branch → town base → current branch`, and a `--dry-run`/print path names WHICH rung was chosen and WHY (source: target|record|town|current). TESTS in extensions/agi/tests/test_season*.py: a core round with a recorded base_branch = its rung merges into the rung; a town round with no record still resolves the town base; an explicit --target beats both. FALSIFIER: a recorded base_branch that is not the chosen base. VERIFY ON THE REAL TREE: run the resolver read-only (a probe that prints the chosen base for a real record under .agi/sessions/iter-L4.12x) — never a real merge. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/season.py (the base resolution region ONLY) + its tests. g15-3 (cmd_rollover) is a SEPARATE node serial behind this one on season.py. EXCLUDED: spawn_gate.py (g15-1), rotate.py, dispatch.py.
