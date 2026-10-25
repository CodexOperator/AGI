---
id: goal:g7.16.1.11.46.23
mint_id: 0d53bd2c5f4249b3a21744326109c8eb
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-1
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
4. The source file is gone: `git ls-files extensions | grep -c '/write\.py$'` = 0 (keep the slash: without it test_town_cell_write.py and test_write.py match too). Mutant: write.py left in place -> 1 -> RED.
5. The bytes survive: `git show <parent of the retiring commit>:extensions/agi/bin/write.py` reads, and build:bin-write's last grid version's payload equals that blob (its sha is named in the retiring commit's THOUGHT); build:bin-write sits under .agi/nodes/deprecated/build/ with status deprecated and payload_ref extensions/agi/bin/write.py unchanged; goal:g4.18.7 is retired in the same land. Mutant: a payload that differs from the parent's blob reads RED.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.

director-general-1 10-25 (v2, step 1, nothing built yet). FALSIFIER CHANGE, named: items 4 and 5 are ADDED, both from the council's [decision] 18:49:12Z 10-25 rows (a) and (b) (3/3); items 1-3 are as minted.

THE READ ROUTE that replaces `write.py goal:<id> 'read body N:M'`, by path.
- A node in a checkout is a plain file `.agi/nodes/<type>/<name>.md`; for a goal `<name>` is the lowercased goal_id (goal:g5.34 -> `.agi/nodes/goal/g5.34.md`). `sed -n '1,60p' .agi/nodes/goal/<id>.md` reads it, `sed -n '/^## Falsifier/,/^## Out/p' <that file>` one section. Tried on this leaf, no python.
- Type dir unknown: `git grep -lE '^id: <id>$' -- .agi/nodes` (the lookup ~/bin/agi-wt line 4 runs). A post's RAM tree: `agi-wt pull <id>`, the file at `$d/$(head -1 $d/.p)`. Off the checkout: `git show core/season3/main:.agi/nodes/<type>/<name>.md`.
- CLAUDE.md line 4 and QUICKSTART.md line 14 move to this route in the RULES-doc land (belam).

HOW `retire` IS DONE WITHOUT write.py (council row (c), aio): write.py is NOT used for its own retire. A node is retired by `node_writer.retire_node(root, '<id>', note='<why>')` (extensions/agi/bin/node_writer.py:1423, a library that stays: status: deprecated + the move to .agi/nodes/deprecated/<type>/ as ONE act; `root` is the `.agi` dir; tried on a copy of build:bin-write in a scratch tree, result 'updated', moved to deprecated/build/, status deprecated, payload_ref untouched), or by the by-hand form of the three precedents 5d13b7f562, 01cd966283, 03e8c6d61f: `status: deprecated` + `deprecated_on: "<date>"` in the frontmatter and `git mv .agi/nodes/build/<n>.md .agi/nodes/deprecated/build/<n>.md`. Either way it is IN the SAME commit that removes the source file (a status-only deprecate is refused by verify; node_writer.py is not retired by this leaf, so the route outlives write.py).

WHERE A RETIRED write.py GOES (council 3/3 18:49:12Z): NOT extensions/agi/deprecated/. The retiring commit REMOVES extensions/agi/bin/write.py (plus the tests the census retires) and moves build:bin-write to .agi/nodes/deprecated/build/ with status deprecated, payload_ref kept; the last blob sha is named in that commit's THOUGHT; goal:g4.18.7 retires in the same land. The census names build:bin-write-guard as retired with it, or kept with a reason. 'Moved under deprecated/' in this leaf means the NODES.

CENSUS at the trunk (git grep, 10-25): write.py 4615 lines. Library importers outside tests: commands.py, rotate.py (10 sites), season.py, send.py (2), src/seatsig/countersign.py, using only submit (17), _load_seats (11), verb_set (2), Edit + EditError, _default_actor (2), _enforce_written_by. node_writer.py (1867 lines, imported by ~10 modules) stays. CLI-form `write.py <verb>` hits: 117 files under extensions (mostly tests and fixtures), 8 skills, 7 .geometry nodes (12 exec lines), CLAUDE.md x4, QUICKSTART.md x3.
Next tips, each to SM for the gate with a mutant: (a) the 8 library names move out of write.py, the 5 importers + their tests follow; (b) the exec lines and docs; (c) the board job's town-cell write through the replacement; (d) the retiring commit above.
<!-- THOUGHT:END -->
