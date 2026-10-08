---
id: hypothesis:context-budget-never-floors-to-zero-and-is-pinned
mint_id: f48048e6072e427280675e767ed8d007
type: hypothesis
parents:
  - goal:g15.29.20
next_edges: []
assigned: director-engine (leaf goal:g15.29.20, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: e3337bc7c37a6024
season: 2
testable_claim: After the fix, a 0<v<1 context budget never reaches a subprocess as 0, and stage-over-manifest precedence, the bool refusal, dry-run rc 5 and zero stage dispatch on a refusal are each pinned, with the fraction test red on the pre-fix bytes and test_workflow*.py green.
title: "The context budget never floors to zero; stage, bool and dry-run pinned (goal:g15.29.20; assigned: director-engine)"
town: core
---
# hypothesis:context-budget-never-floors-to-zero-and-is-pinned

# hypothesis:context-budget-never-floors-to-zero-and-is-pinned

**Assigned: director-engine** (leaf goal:g15.29.20; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
workflow.py:2083 accepts 0<v<1 and :2086 int(raw) makes it 0 -> timeout=0 at :1550-1559; the load-scaled lines :2092/:2053 truncate too; the stage branch :2073-2075 is untested; test_workflow_review_under_load.py:189-200 covers (0, -1, '300') with dry_run=False only and its fake records only context calls (:160-170)
```

## CLAIM
After the fix, a 0<v<1 context budget never reaches a subprocess as 0, and stage-over-manifest precedence, the bool refusal, dry-run rc 5 and zero stage dispatch on a refusal are each pinned, with the fraction test red on the pre-fix bytes and test_workflow*.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_workflow*.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
workflow.py · test_workflow_review_under_load.py

HAZARD: workflow.py is the live merge-up review runner: never run a real workflow

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
