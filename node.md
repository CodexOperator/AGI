---
id: hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node
mint_id: 8b8791641f424ec2a17193ef7075506c
type: hypothesis
parents:
  - goal:g15.29.16
next_edges: []
assigned: director-engine (leaf goal:g15.29.16, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: fe4f0b0aa0d92dd2
season: 2
testable_claim: After the fix, a malformed required_any raises a SecretsError that is not a ValueError, and `anonymize.py check --root <repo root>` refuses text carrying a declared key's env value, proved by committed tests red on the pre-fix bytes, with test_envfile.py and test_anonymize_guard.py green.
title: "Secretserror is its own type and the hook reads the graph's secrets node (goal:g15.29.16; assigned: director-engine)"
town: core
---
# hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node

# hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node

**Assigned: director-engine** (leaf goal:g15.29.16; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
envfile.py:121 SecretsError(ValueError) (it subclassed Exception before 8e1ef136b1); test_envfile.py:839 asserts ValueError · anonymize.py:24 reads <root>/nodes/.geometry/secrets.md but the installed hook passes --root = the repo root (anonymize.py:100-101; locations.py:413-414) where no nodes/ exists -> the pre-commit guard checks ZERO secret values
```

## CLAIM
After the fix, a malformed required_any raises a SecretsError that is not a ValueError, and `anonymize.py check --root <repo root>` refuses text carrying a declared key's env value, proved by committed tests red on the pre-fix bytes, with test_envfile.py and test_anonymize_guard.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_envfile.py test_anonymize_guard.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
envfile.py · anonymize.py · their tests

HAZARD: a fixture hooks dir and fake values only; never print a real secret

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
