---
id: goal:g1.31.5.1
mint_id: 5b1078a42fbf446b886a5360e40988d4
type: goal
parents:
  - goal:g1.31.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 9c56b41cc3312e61
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - red
  - intermediate
title: "G1.31.5.1: the 3 PASS B3 missed reds are closed -- agent-git hook fails closed, no email in nodes + email class, write.py never launders a hand edit"
town: core
---
# goal:g1.31.5.1

## Why this exists
goal:g1.31.5: 3 of the 59 REAL missed rows are red (a gate that passes when it should refuse, an anonymize leak, a guard that can be laundered). Each was re-read against HEAD d4b7ead17:
```
n    round (verify file under .agi/sessions/workflows/runs/)                                            lane  leaf
19   l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-ho (mur-pb3chunk12of20)                  DG6   .5.1.1
112  a-second-director-ran-this-graph-uninvited (mur-pb3chunk7of20)  (+ n88 engine-delta-6, residue)   DG6   .5.1.2
83   engine-delta-5 (mur-pb3chunk3of20)                                                                 DG4   .5.1.3
```

## Target end-state
- goal:g1.31.5.1.1: `extensions/agi/hooks/agent-git/pre-commit:76-77` runs its scope pipe under `pipefail`. A failed `git diff --cached` makes the kid-scope check refuse, where today it exits 0.
- goal:g1.31.5.1.2: the 4 experiment nodes are scrubbed forward through `write.py` and carry no email address. `anonymize.py` refuses an email address by class, tested on a synthetic fixture. `skills/` sits inside a committed home-path guard scope.
- goal:g1.31.5.1.3: `write.py _commit_write` (:4053) refuses to commit a path whose bytes on disk already differed from HEAD before the write, so a same-path hand edit stays visible to `write_guard.py`.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- No probe, dm, commit message, test or node ever prints the owner's address, a user name or a host name. Fixtures are synthetic.

## Falsifier
1. Every child is complete: `for g in 1 2 3; do grep -q '^status: complete' .agi/nodes/goal/g1.31.5.1.$g.md || exit 1; done`
2. Negative: `git grep -L pipefail -- extensions/agi/hooks/agent-git/pre-commit` returns zero hits (1 at HEAD).

## Out of scope
goal:g1.31.5.2 · goal:g1.31.5.3 · goal:g1.31.5.4 · goal:g1.31.5.5 · goal:g1.31.1-.4 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6** (intermediate; the leaves carry the lanes: director-general-6 · director-general-6 · director-general-4).
