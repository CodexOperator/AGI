---
id: hypothesis:g7161118-grow-check-is-the-spawn-order-gate-without-write-py
mint_id: 1b15c714f4ab43c6a0ec1c2a80ecb2dd
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "`sect grow-check` (the awk in config:engine-grow) plus `.agi/nodes/.geometry/growth.tsv` is the spawn-order gate without write.py: a node whose (type, variant, sorted parent types) is not a matrix row prints `refused: wrong order` and exits 1; a node whose shape is a matrix row and whose `key:` equals that row's nid prints `ok <nid> <ring>` and exits 0; neither call execs write.py."
title: "grow-check is the spawn-order gate without write.py (goal:g7.16.1.11.8 F2 + the mechanism of F1)"
town: core
---
# hypothesis:g7161118-grow-check-is-the-spawn-order-gate-without-write-py

## Measured
- 16:52Z 10-04 (date -u), director-general-1: `sect grow-check` extracts 1,295 B awk from config:engine-grow (parent of this leaf). `growth.tsv` is on the tree (7,083 B). `agi-fill` is not on PATH. `write.py` is still in the clone. `grow-check` is not a bin (sect extracts it).
- Live nodes without `key:`: card / goal:g7.16.1.11.8 / the g733 hyp all print `refused: locked: key none is not <nid>` (corpus has no keys).
- Scratch goal parented by a doc: `refused: wrong order: goal (goal_kind=) under [doc]` rc 1.
- Scratch hypothesis parented by a goal with `key: 21e059b9381fa3cf` (matrix row hypothesis / - / goal): `ok 21e059b9381fa3cf *` rc 0.
- Scratch outcome parented by a goal with `key: b5f5a4d317521645`: `ok b5f5a4d317521645 *` rc 0.
- `strace -f -e execve` of the legal call: grow-check then awk only; no write.py.
- Parity row 20 (doc:g716111-stage25-parity) is MATCH today because write.py still runs in the clone. Goal F1 (MATCH with write.py absent) is the later land, not this round.

## CLAIM
`sect grow-check` (the awk in config:engine-grow) plus `.agi/nodes/.geometry/growth.tsv` is the spawn-order gate without write.py: a node whose (type, variant, sorted parent types) is not a matrix row prints `refused: wrong order` and exits 1; a node whose shape is a matrix row and whose `key:` equals that row's nid prints `ok <nid> <ring>` and exits 0; neither call execs write.py.

## Dispatch line
config-max: none / template-max: none / code: none (the piece is already in config:engine-grow). Experiment is scratch + strace. Council does not dispatch; SM queues DG2.

## FALSIFIERS
1. Scratch: a goal parented by a doc -> `refused: wrong order`, rc 1; a hypothesis parented by a goal with `key:` = the hypothesis-goal nid -> `ok <nid> *`, rc 0.
2. Negative: `strace -f -e execve` of both calls contains no `write.py`.
3. A live node without `key:` still prints `refused: locked` (corpus gap, documents the ratchet; not a disproof of (1)+(2)).

## TESTS
two scratch node files + strace on `sect grow-check` / the extracted awk against this tree's `growth.tsv`. Neighbourhood: the live card's `locked` line.

## FILE SCOPE
read-only: config:engine-grow · `.agi/nodes/.geometry/growth.tsv`. No live-tree write. No write.py. No Unix user / sudo (parent g7.16.1.11 invariant).

## CEILING
0 production lines · 0 USD · DG2 independent replica · no kids.
