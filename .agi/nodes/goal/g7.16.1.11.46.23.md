---
id: goal:g7.16.1.11.46.23
mint_id: 0d53bd2c5f4249b3a21744326109c8eb
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.23
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V8a
season: 3
status: active
title: "G7.16.1.11.46.23: V8a -- write.py and its build node (bin-write) retired, goal:g4.18.7 retired as superseded: 0 callers in the live pieces, skills, crons, hooks and RULES docs; the read route that replaces it is named by path"
town: local-maxxing
---
# goal:g7.16.1.11.46.23

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §23, §34.6. Box reading K4: write.py is a LIBRARY as well as a CLI: 23 extensions modules import it, 15 exec lines sit in .geometry, skills and hooks, CLAUDE.md names it 4 times and QUICKSTART.md 3 times, and 1222 node files mention it as history prose (aio 4: CLAUDE.md's first instruction reads a goal with it; the hourly board commit is 'write.py: town:local-maxxing'). Independent of the grid, so it runs in parallel once its read route is named. Owner atom a1 closes HERE (council R1).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.23 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| a1 | "Retire write py for sure we don’t need it at all and need to retire that whole build node as the capsule wrapper now tags everything for us using standard read routes" | target:W2 brief 2 leaf V8a (write.py out; supersedes g4.18.7) |

## Target end-state
- The read route that replaces `write.py goal:<id> 'read body ...'` is named BY PATH in this leaf's THOUGHT before any build.
- write.py and bin-write are retired (`status: deprecated`, moved under deprecated/, never deleted); goal:g4.18.7 is retired as superseded.
- The board job's town-cell write moves to the piece that replaces it; CLAUDE.md's command table and skill agi-node-write are edited in the same land (RULES paths: they land with belam).

## Invariants
- Retire, never delete (CLAUDE.md).
- Mentions in node history are history, not callers: they stay.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. Callers = 0: `git grep -l -E '(^|[^a-z_])(import write|from write import)|write\.py +[a-z:]'` over extensions, skills, .agi/nodes/.geometry, the hooks, CLAUDE.md and QUICKSTART.md prints nothing outside the retired node and deprecated/.
2. The board's next hourly commit after the land lands through the replacement (its subject no longer reads 'write.py:').
3. `python3 -m pytest extensions/agi/tests/ -q` passes with write.py retired; mutant: one import left in a live module reads RED in the caller grep.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
