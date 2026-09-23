---
id: hypothesis:restart-carries-the-first-spawns-full-turn-and-identity
mint_id: 2e97ab95fcc84c92af8f3837086eae73
type: hypothesis
parents:
  - goal:g15.29.18
next_edges: []
assigned: director-engine (leaf goal:g15.29.18, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: df90f2084ae32822
season: 2
testable_claim: After the fix, adapter.restart receives the first spawn's skill prompt, cli_py, role and tiers (from spawn.json / the agent record) and a non-dict spawn.json falls back to None, proved by a committed test red on the pre-fix bytes, with test_dispatch_restart_render.py, test_real_adapter_restart.py and test_dispatch.py green.
title: "A restart carries the first spawn's full turn and identity (goal:g15.29.18; assigned: director-engine)"
town: core
---
# hypothesis:restart-carries-the-first-spawns-full-turn-and-identity

# hypothesis:restart-carries-the-first-spawns-full-turn-and-identity

**Assigned: director-engine** (leaf goal:g15.29.18; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
dispatch.py:3592-3607 passes none of them though the first spawn does (:2561-2593) and claude_code_adapter.restart accepts them (:835-844); the agent record (:2827-2850) stores role but no tiers; dispatch.py:3344 catches only OSError/ValueError, so a non-dict spawn.json raises AttributeError -> 'restart unavailable' (:3608-3612)
```

## CLAIM
After the fix, adapter.restart receives the first spawn's skill prompt, cli_py, role and tiers (from spawn.json / the agent record) and a non-dict spawn.json falls back to None, proved by a committed test red on the pre-fix bytes, with test_dispatch_restart_render.py, test_real_adapter_restart.py and test_dispatch.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_dispatch_restart_render.py test_real_adapter_restart.py test_dispatch.py test_*adapter*.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
dispatch.py · the adapters' restart signatures if needed · a test file

HAZARD: the spawn path: adapter test doubles only, never a real spawn

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
