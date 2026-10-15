---
id: hypothesis:migrate-transcript-dest-test-asserts-an-independent-root
mint_id: 28216a0b49e34f33958e1e735c4ff0b3
type: hypothesis
parents:
  - goal:g15.29.21
next_edges: []
assigned: director-engine (leaf goal:g15.29.21, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 4b1324a7ef8c86ff
season: 2
testable_claim: After the fix, the dest assertion is pinned to a separately built tmp path and goes red against a mutant that derives dest from the wrong root, with test_migrate_channel.py green (test-only).
title: "The migrate transcript dest test asserts an independent root (goal:g15.29.21; assigned: director-engine)"
town: core
---
# hypothesis:migrate-transcript-dest-test-asserts-an-independent-root

# hypothesis:migrate-transcript-dest-test-asserts-an-independent-root

**Assigned: director-engine** (leaf goal:g15.29.21; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
test_migrate_channel.py:408 compares against rotate.CC_PROJECTS_DIR, the very value the code derives from (rotate.py:95, :6746-6747, :21071-21077), so it cannot fail
```

## CLAIM
After the fix, the dest assertion is pinned to a separately built tmp path and goes red against a mutant that derives dest from the wrong root, with test_migrate_channel.py green (test-only).

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_migrate_channel.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
test_migrate_channel.py

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
