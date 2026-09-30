---
id: goal:g4.18.5
mint_id: e28fe576bf294848890b9049b80382c5
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.7
edited_by: all-is-one
goal_id: G4.18.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 30214a9e57369dee
season: 2
seeds: []
status: active
tags:
  - engine
  - write-path
  - owner
title: "G4.18.5: a node body is addressable rows and a write is ONE commit behind the permission layer -- one verb replaces a row, one edits lines inside a block row; the commit lands on the node's own grid ref (goal:g7.16.1.6), the era one config cell"
town: core
---
# goal:g4.18.5

## OWNER 2026-09-29 17:2xZ, verbatim (Prime pane)
"Is our new unified mint/wrote working better. We could add more verbs to mint single row changes and to change specific lines inside of a row that is a block of text not just one line."
"Actually, if we have a one-row replace verb we can split all the different body sections into their own rows. But also still have a way to overwrite specific lines. Maybe something got based that piggybacks off of git commits. Maybe a write could be a commit also and just drive all the existing git machinery just with permissions layered on top."


## Why this exists
goal:g4.18: write.py is the one node writer. Measured friction on 09-29 (belam-S2-L5-XVI): no single-row verb (re-homing stream-master rewrote the whole 25-row config:posts list via write.submit); `replace body` refuses a line inside a table paragraph (the council-loop Posts table was replaced whole to add one row); `create config` has no route (spawn gate) and `adopt` skips written_by (goal:g4.18.3); a key-row write corrupted config:posts on season2/main (goal:g4.18.4).

goal:g7.16.1.6 (the write form, owner 22:4xZ-23:0xZ 09-29, verbatim there): the owner's next line re-aims this goal's commit, "we commit ONLY to the grid ref and the specific grid ref that belongs or is created for that node". So the commit target is the node's own grid ref, never the branch. Measured the night W1 landed (09-29/30): the branch-commit form was refused while PASS B3 held verify-suite.lock (5 writes across two council posts), and one write hit a busy index.lock mid-commit. Both costs vanish when a write never touches the branch, MAIN's index or the suite lock.

## Target end-state
```
A ROWS     a node body is ONE index of addressable rows (section / table row / list item), shared by write and render (goal:g4.18.7):
           one verb replaces a row (by number or by name), one verb edits lines inside a block row                  -> goal:g4.18.5.1 (.1.1 .1.2 complete)
B COMMIT   a write IS one commit behind the permission layer: written_by, self_row, actor_rows and the schema run first; a refused gate
           writes and commits nothing. The commit lands on the node's OWN grid ref (goal:g7.16.1.6 A); ONE config cell,
           write.commit_target = branch | ref, says which era the box is in: flipped once by .6's cutover, read by write.py and every falsifier
                                                                                                          -> goal:g4.18.5.2 built the branch form;
           its busy-index retry (goal:g4.18.5.2.1) is superseded by .6 A (a write never touches MAIN's index) and is not built further
C ONE ROW WRITE per config table: config:posts' 4 rotate commit paths go through the one row write              -> goal:g4.18.5.3 (goal:g7.16.1.6 C cites it)
```
- History is git's own machinery on that ref: log, diff and blame of a node are git's; there is no second versioning mechanism.
- The teaching is one config cell and the skill lines (goal:g4.18.5.2.2): a write commits itself, so "commit by exact path" for a node file leaves every skill at the .6 cutover.

## Invariants
- Every write passes the same authorship + schema gate before any byte lands; no verb returns ahead of it.
- A row edit changes only that row's bytes; every other byte of the node stays identical, and an edit whose range holds a THOUGHT marker refuses.
- ONE row index: write and render never parse rows two ways.
- Nothing durable stores a row NUMBER: links, briefs, skills, cards and findings address a row by NAME; `row <n>` is for an interactive edit only (numbers shift on the next insert; CLAUDE.md's two-identifiers rule, one level down).

## Falsifier
1. `write.py <id> 'row <n> <file>'` replaces exactly one row, and the node's newest commit is that write's commit, looked up where write.commit_target points: `git log -1 refs/grid/<mint>` for `ref`, `git log -1 -- <node>` for `branch` (the falsifier reads the cell; it never guesses the era).
2. `write.py <id> 'row name:<NAME> <file>'` replaces the one row whose first cell is NAME; 0 or more than 1 matches refuse rc 2, nothing written.
3. Negative: zero write.py verbs that change a node without producing a commit · every body-row consumer (write, render, the census) reads rows through node_writer's one index, measured by its CALLERS against the modules that address rows, never by a function name (a check narrower than its invariant passes falsely).

## Out of scope
goal:g4.18.3 · goal:g4.18.4 (bundle 3, H1-H2) · goal:g7.16.1.6 (the ref-commit mechanism and the snapshot; this goal only takes its target) · goal:g4.18.6 (links as mint ids) · goal:g4.18.7 (the render path the row index serves).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all-is-one (council) 01:3xZ 09-30, on belam's [owner-task], OWNER 00:5xZ 09-30 verbatim: "make updates to each goal's structure and wording as needed to make sure that the new owner words are reflected in the goal format" and "apply their lenses and zoomed out thinking at my words". The owner line this goal serves most (17:2xZ, above): "Maybe a write could be a commit also and just drive all the existing git machinery just with permissions layered on top"; the line that re-aims it lives on goal:g7.16.1.6 (23:0xZ: "we commit ONLY to the grid ref"), cited here, never copied. What the lens (vision:all-is-one: one tool for any act) changed in THIS version: (1) the commit TARGET is the node's own grid ref, so the write form is ONE primitive shared with goal:g7.16.1.6, not a branch commit beside it; (2) each target row points at the leaf that carries it (A -> .1, B -> .2, C -> .3), so the goal and its leaves say one thing once; (3) goal:g4.18.5.2.1 (index-lock retry) is marked superseded by .6 A, since building it would be work the cutover throws away (its status is the directors' call); (4) .6 C cites .3 for rotate's 4 posts paths, one owner per act (settled pairwise with alive); (5) the doubled `# goal:g4.18.5` H1 dropped; (6) alive's lens: the era is ONE config cell (write.commit_target = branch | ref), flipped once at .6's cutover and read by write.py and the falsifier, so a pass in the wrong era cannot pass; (7) invariants gained the row-bytes rule, ONE row index, and self-perpetuating's lens: nothing durable stores a row number (address by name); falsifier gained row-by-name and a callers-measured one-index negative (s-p: a name-grep is narrower than the invariant).
<!-- THOUGHT:END -->

## Agent Notes
Assigned to **director-engine**.
