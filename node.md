---
id: hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin
mint_id: 4b1fe86932c1469d89ec66977ee91c30
type: hypothesis
parents:
  - goal:g15.29.12
next_edges: []
assigned: director-engine (leaf goal:g15.29.12, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 531f76e7f7202ff6
season: 2
testable_claim: After the fix, an unknown encoding is refused by name at check time and a ~user/... bin whose user does not exist raises the named FileNotFoundError, proved by committed tests red on the pre-fix bytes (plus a pin for the spread refusal), with test_harness_template.py and test_adapters.py green.
title: "Harness argv refuses an unknown encoding and an unresolved ~user bin (goal:g15.29.12; assigned: director-engine)"
town: core
---
# hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin

# hypothesis:harness-argv-refuses-unknown-encoding-and-unresolved-user-bin

**Assigned: director-engine** (leaf goal:g15.29.12; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
harness_template.py:160-165 checks only slot/when/spread; :206 turns any non-json encoding into str; tests :113-140 cover slot and when only · adapters/__init__.py:70-83 expanduser leaves ~nosuch/x unchanged, so path != raw is False and `return raw` runs
```

## CLAIM
After the fix, an unknown encoding is refused by name at check time and a ~user/... bin whose user does not exist raises the named FileNotFoundError, proved by committed tests red on the pre-fix bytes (plus a pin for the spread refusal), with test_harness_template.py and test_adapters.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_harness_template.py test_adapters.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
harness_template.py · adapters/__init__.py · their two test files

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
