---
id: goal:g7.16.1.11.46.23.1.1
mint_id: d4db0c975b794d2f81fbd6831610339c
type: goal
parents:
  - goal:g7.16.1.11.46.23.1
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.23.1.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: a4a1758ed384d094
season: 3
seeds: []
status: active
tags:
  - V8a
  - verify-land
title: "G7.16.1.11.46.23.1.1: verify-land holds an R out of .agi/nodes/ by name and reads its D diff's exit code (a failed read is D: unread, never D: 0)"
town: local-maxxing
---

# goal:g7.16.1.11.46.23.1.1

# goal:g7.16.1.11.46.23.1.1

## Why this exists
goal:g7.16.1.11.46.23.1 (verify-land's D block: a delete admitted only by path from BASE's land.deletes_admitted, renames pinned with -M, a node delete never admitted) left two readings unguarded, both queued on director-general-1's card and placed by the council 3/3 (alive [decision] 18:45:32Z 10-28, U-b, corrected 19:02:55Z; SM [note] 18:59:07Z): (1) an R whose source is under .agi/nodes/ and whose destination is outside it passes the D block (only a D under .agi/nodes/ is refused; all-is-one's sweep g16 line (2): "an R out was unchecked"); (2) the `ns=$(git diff -M --name-status B L)` read's exit code is never read, so a failed diff yields an empty set that prints `D: 0` and passes.

## Target end-state
- An R from under .agi/nodes/ to a path outside it HOLDs D, naming the move: `R out of the graph: <from> -> <to> (a node: retire into .agi/nodes/deprecated/, never move out)`. An R into .agi/nodes/deprecated/ (a retire) is not held by this line.
- The D read's exit code is read: a failed diff prints `D: unread (git diff -M --name-status rc N)`, reads no D set, and HOLDs D; never `D: 0`.

## Invariants
- Every check still runs to the verdict; these lines add a hold, never remove one.
- The D read stays `-M` pinned (goal:g7.16.1.11.46.23.1 falsifier 2: no name-status line without -M).

## Falsifier
1. extensions/agi/tests/verify-land.t.sh rows: ro1 (an R out of .agi/nodes/ HOLDs D with the named line), ro2 (an R into .agi/nodes/deprecated/ reads `D: 0` and verify-land: OK), nr1 (a PATH git shim failing only the --name-status read -> `D: unread (git diff -M --name-status rc 128)` and HOLD D); each RED under its mutant: m-ro (the R-out hold never fires -> ro1's move passes the D block) and m-nr (the rc not read -> nr1 prints `D: 0` and no D hold). The lane exits 0.
2. negative: da8 stays green: `grep name-status extensions/agi/guard/verify-land.sh | grep -vc -- '-M --name-status'` = 0.

## Out of scope
goal:g7.16.1.11.46.23.1's landed rows; the home step (goal:g7.16.1.11.46.16; the system-account home false positive was closed by L211 + L214, measured 100/0 at 2ce5624054); the R-land mode flip (the council's).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted with its build (one RULES tip, extensions/agi/guard/ + the lane): the placed leaf is ONLY these two rows, because the placed atom (the system-account home false positive) was already fixed on the trunk (DG1 [finding] 18:58Z, measured verify-land.t.sh 100/0 at 2ce5624054; SM and alive agreed). Parent = goal:g7.16.1.11.46.23.1 (complete) because both rows harden its D block; a leaf under the complete goal, not a reopen of it.
<!-- THOUGHT:END -->
