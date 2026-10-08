---
id: hypothesis:crons-render-fails-closed-by-name-on-partial-box-schema
mint_id: 38545ad22d3d4b36b1e726c114bd536f
type: hypothesis
parents:
  - goal:g15.29.17
next_edges: []
assigned: director-engine (leaf goal:g15.29.17, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: bda93a0fa9892ee7
season: 2
testable_claim: "After the fix, no rendered cron line carries an empty or unsubstituted mapped token (a missing map entry or cell refuses as `ERR: crons.py:` rc 1, never a traceback) and a project without its own [box].md falls back to the engine's schema (director's call: availability over refusal for an ABSENT schema, refusal for a PARTIAL one), proved by fixture tests red on the pre-fix bytes, with test_crons.py, test_paths_audit.py and test_box_guard.py green."
title: "Crons render fails closed by name on a partial box schema (goal:g15.29.17; assigned: director-engine)"
town: core
---
# hypothesis:crons-render-fails-closed-by-name-on-partial-box-schema

# hypothesis:crons-render-fails-closed-by-name-on-partial-box-schema

**Assigned: director-engine** (leaf goal:g15.29.17; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
crons.py:486-491 passes four hardcoded cells; boxes.py:84-85 falls back to '' so {tmux}/{user} render empty and unmapped tokens stay literal; [box].md:15-16 maps undeclared keys; a missing schema reads {} (boxes.py:33-34) -> BoxSchemaError(ValueError) (:20), uncaught by crons.main (only CronsError, crons.py:1183); test_crons.py:132-135 always writes the schema, :1428-1445 reads the live node
```

## CLAIM
After the fix, no rendered cron line carries an empty or unsubstituted mapped token (a missing map entry or cell refuses as `ERR: crons.py:` rc 1, never a traceback) and a project without its own [box].md falls back to the engine's schema (director's call: availability over refusal for an ABSENT schema, refusal for a PARTIAL one), proved by fixture tests red on the pre-fix bytes, with test_crons.py, test_paths_audit.py and test_box_guard.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_crons.py test_paths_audit.py test_box_guard.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
crons.py · boxes.py · [box].md · test_crons.py

HAZARD: HIGH blast radius: never run `crons.py apply` (it writes the real crontab; grid_sync re-applies every 5 min) -- render in fixtures only

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
