---
id: goal:g7.16.1.11.8
mint_id: 913dfa27239b46dfa8f39333e92538ad
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.8
goal_kind: subgoal
origin: owner
scaffold_hash: 9ccf9843db930b04
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.8: ROUND 7: GROWTH ORDER kept by the new engine itself -- node keys from the schemas' parent shapes, a captive fill window, row-by-row checks, local models under a schema grammar"
town: core
---
# goal:g7.16.1.11.8

## Why this exists
Parent goal:g7.16.1.11: belam measured 07:1xZ: parity row 20 (spawn gate, schemas) is MATCH only because the old write.py runs in the clone -- so this leaf gates phase 3.
## Target end-state
ROUND 7: GROWTH ORDER kept by the new engine itself -- node keys from the schemas' parent shapes, a captive fill window, row-by-row checks, local models under a schema grammar.
## Invariants
a node add out of schema order is refused by the engine, without the old Python.
## Falsifier
1. parity row 20 reads MATCH with write.py absent from the clone
2. negative: a node minted out of order: zero
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"we should make sure the engine still maintains graph growth order so posts can't just grow nodes without respecting order" (owner 07:1xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3** (placed by sanctuary-master 14:1xZ 10-14; was council).

CLOSE goal:g7.16.1.11.8 = 4a01e33063 + 1a24d1d334 + 5bd0c5cf89 (DG3: the growth gate in agi-turn, ONE shared grow.py, a new node APPROVED or REFUSED never committed unchecked) + d074826b4e (DG1: rows round 2) + falsifiers RE-RUN at c3434153a6: lane agi-turn.t.sh 142 ok / 0 FAIL (30 go*/ga* growth rows); F1: row 20 reads MATCH (.agi/nodes/doc/g716111-stage25-parity.md:71) and the lane's fixture holds NO write.py (find write.py in the fixture = 0; bin = agi-at agi-brief agi-flush agi-meter agi-notice agi-out agi-sync agi-turn agi-wt grow.py sect systemctl tick.sh); F2: out-of-order / parentless / quoted / multi-line / unknown-type new nodes REFUSED through agi-turn and agi-at (go1 go1b go4 go6 go9 go7 go10-go10e goall ga1: tip unchanged), legal control LANDS (go2, ga2, go10f), an EDIT is never gated (go3, ga4, go7b), a failing diff-index fails closed (go8, ga5); MUTANT (grow.py `if r.status!=g.APPROVED:` -> `if False:` via PIECES=): 13 rows RED (go1 go1b go4 go6 go9 go7 ga1 go10 go10b go10c go10d goall go10e), the legal and edit controls stay green; unmutated PIECES= control 142 ok / 0 FAIL. Zero out-of-order mints land.
Note: row 20's basis cell still reads "write.py runs unchanged there"; the MATCH it claims is now carried by the plain path (Write + agi-turn / agi-at -> grow.py), which is what the lane proves. Not changed here (a doc row, not this leaf's).
Not run: the full pytest (SM: no full suite needed; derived files only).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-14: COMPLETE. Placed on DG3 by SM 14:1xZ with both falsifiers un-run since the build (10-10). Re-run at c3434153a6: the agi-turn lane reads 142/0, write.py is absent from its fixture, a grow.py bypass turns 13 refusal rows RED while the legal and edit controls stay green. Delta: the leaf had no CLOSE and no THOUGHT; the build and its rows already existed.
<!-- THOUGHT:END -->

belam-s2-II 08:3xZ 10-10 LANE (Prime, write-gate class): DG2 08:25Z bytes -- on v5 the plain path (Write/Edit + agi-turn/agi-at) has NO growth-order gate (spawn_gate.check_spawn runs only inside write.py/cli.py create; an out-of-order build node was accepted). DG3 builds the check into agi-turn for NEW node files only (reuse check_spawn; edits never gated); DG2 rows (refuse / legal control / edit control). After the season-close leaves.
