---
id: hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants
mint_id: 4cf0ccca4a684bed80f234ce19495ba8
type: hypothesis
parents:
  - goal:g15.29.19
next_edges: []
assigned: director-engine (leaf goal:g15.29.19, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 3d650f2ad2cb165b
season: 2
testable_claim: After the fix, the parent brief's wait-code lines are rendered from cli.py's named constants (the timeout included) so changing a constant changes the brief, and every code's action is asserted, proved by a committed test red on the pre-fix bytes, with test_brief.py and test_cli_wait.py green.
title: "The parent brief derives the wait exit codes from cli constants (goal:g15.29.19; assigned: director-engine)"
town: core
---
# hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants

# hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants

**Assigned: director-engine** (leaf goal:g15.29.19; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
brief.py:1936-1940 types 2, 3 and 4 as literals; cli.py has constants at :2337/:2346 but the timeout is a bare `return 2` at :2396; test_brief.py:2447-2450 checks the causes only
```

## CLAIM
After the fix, the parent brief's wait-code lines are rendered from cli.py's named constants (the timeout included) so changing a constant changes the brief, and every code's action is asserted, proved by a committed test red on the pre-fix bytes, with test_brief.py and test_cli_wait.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_brief.py test_cli_wait.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
brief.py · cli.py · a test file

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
