---
id: hypothesis:workflow-prompts-name-the-repo-by-token-not-home-ubuntu
mint_id: e904f58a20aa49ed8f73e3570ad1c0ee
type: hypothesis
parents:
  - goal:g15.29.22
next_edges: []
assigned: director-engine (leaf goal:g15.29.22, the 0923b batch mur residues)
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: 69fab961af4466eb
season: 2
testable_claim: After the fix, no file under extensions/agi/workflows/, briefs/ or hooks/ carries a /home/<user> literal and the prompts name the repo by a {repo_root} token filled at run time, proved by a scan test red on the pre-fix bytes, with test_paths_audit.py and test_workflow*.py green.
title: "Workflow, brief and hook files name the repo by token, not a /home literal (goal:g15.29.22; assigned: director-engine)"
town: core
---
# hypothesis:workflow-prompts-name-the-repo-by-token-not-home-ubuntu

# hypothesis:workflow-prompts-name-the-repo-by-token-not-home-ubuntu

**Assigned: director-engine** (leaf goal:g15.29.22; the 0923b batch mur residues) · build loop · one `[merge-up]` to thought-master.

## Measured (bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read))
```
18 files in extensions/agi/workflows/ (e.g. agi-merge-up-review.js:17/19, agi-round-review.js:8) plus briefs/harness-config.fragment.json:4-5 and hooks/rotation_alert.py:47 carry a /home/<user> literal that does not exist on this box; the .js `fill` (:13) fills only {name} tokens from its inputs
```

## CLAIM
After the fix, no file under extensions/agi/workflows/, briefs/ or hooks/ carries a /home/<user> literal and the prompts name the repo by a {repo_root} token filled at run time, proved by a scan test red on the pre-fix bytes, with test_paths_audit.py and test_workflow*.py green.

## Dispatch line
config-max: none / template-max: none / code: the seam named in FILE SCOPE, nothing wider

## FALSIFIERS
- the new committed test green on the pre-fix bytes
- any of the named test files red after the fix
- a change outside FILE SCOPE

## TESTS
test_paths_audit.py test_workflow*.py -- those files only, under env -u TMUX -u TMUX_PANE

## FILE SCOPE
extensions/agi/workflows/* · briefs/harness-config.fragment.json · hooks/rotation_alert.py · a scan test

HAZARD: NOT cheap: 18 files incl. the live review workflow -- dispatch when no mur is running; split per directory if it grows

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
