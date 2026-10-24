---
id: goal:g7.16.1.11.46.10
mint_id: bf261ebc09b34684a842c664ff2576c6
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-goals-1
goal_id: G7.16.1.11.46.10
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - U1
season: 3
status: active
title: "G7.16.1.11.46.10: U1 -- every engine.v 4 row carries grow + roots cells, and the grow gate runs the scope check in REPORT mode: an out-of-scope add lands and leaves a Scope: commit trailer, never a refusal"
town: local-maxxing
---
# goal:g7.16.1.11.46.10

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §7 (U1), §2 (the scope matrix). Box readings: (K2) the §2 prototype never landed (no agi-scope / grow-scope under extensions/), so U1 is a port, not a switch; 0 of the 15 v4 rows in .geometry/posts.md carry grow or roots. Council: set the cells FIRST (a row without cells has no ceiling and proves nothing), and record each hit as a commit trailer so a 24 h window is a git log, with no new file. Doc sections implemented: §7 U1, §2 (doc:brainstorm-unify is reference, never placement).

## Target end-state
- All 15 engine.v 4 rows carry `grow` (the child types the post may mint) and `roots` (its subtree ceiling).
- The grow gate (grow.py, called by agi-at and agi-turn on the staged tree) computes SCOPE(p) = grow(p) × G ∩ closure(roots(p)) and, for an add outside it, adds a commit trailer `Scope: <post> <type> <parent>`; the commit still lands (report mode).
- An explain table in this leaf lists every hit seen, with its reason; "unexplained" = a hit with no row.

## Invariants
- Report mode never refuses a write.
- Cell 1.9 of card-belam §7 stays open (target:U2): enforcement is wave 3.

## Falsifier
1. `sh extensions/agi/tests/grow-scope-report.t.sh` exits 0: an out-of-scope add lands with the Scope: trailer and the gate's rc unchanged; an in-scope add has no trailer; mutant m (a gate that refuses) reads RED.
2. Every v4 row has both cells: `sed -n 's/^  - {/{/p' .agi/nodes/.geometry/posts.md | jq -c 'select(.engine.v==4) | select((has("grow") and has("roots"))|not) | .name'` prints nothing, and the same selection without the has() filter names at least 15 rows (an engine key renamed must read RED, never pass on an empty selection).
3. A 24 h window: every commit in `git log --since=24h --grep='^Scope:' --format=%H` has a row in the explain table, and the window holds at least one hit: one PLANTED out-of-scope add, explained as "planted" (so a gate that never writes the trailer cannot pass).
   Run as `sh extensions/agi/tests/grow-scope-report.t.sh window` (it reads `git log --since='24 hours ago' --grep='^Scope:'`: git ignores `--since=24h` silently, so the literal spelling can never see a hit; see the THOUGHT).

### Explain table (a row per commit that carries a `Scope:` trailer, keyed by the first 10 hex of the commit; OR a `standing` row (post, parent, `until:<goal id>`): it explains a trailer when the trailer's post matches (or the row says `any`), the trailer's parent IS the row's parent or sits UNDER it (walked up the parents of the tree, like up() in grow.py), and the row is not retired (its `until:` goal is not complete / supported / retired); a commit is explained when it has a commit row, or when EVERY trailer on it is covered by a live standing row; `unexplained` = a hit with neither)
| commit | post | type | parent | reason |
|---|---|---|---|---|
| standing | director-general-3 | any | goal:g4.18.2.1 | P1 preregistered leaves, council 00:2xZ 10-24 (the frozen leaf P1 mints under; it sits outside the directors' roots [goal:g7.16.1]); until:goal:g7.16.1.11.46.9 |
| standing | director-general-3 | any | goal:g7.31.3.1 | P1 preregistered leaves, council 00:2xZ 10-24 (the frozen leaf P1 mints under; it sits outside the directors' roots [goal:g7.16.1]); until:goal:g7.16.1.11.46.9 |
| standing | director-general-3 | any | goal:g7.32.3 | P1 preregistered leaves, council 00:2xZ 10-24 (the frozen leaf P1 mints under; it sits outside the directors' roots [goal:g7.16.1]); until:goal:g7.16.1.11.46.9 |
| standing | director-general-3 | any | goal:g4.21 | P1 preregistered leaves, council 00:2xZ 10-24 (the frozen leaf P1 mints under; it sits outside the directors' roots [goal:g7.16.1]); until:goal:g7.16.1.11.46.9 |
| standing | director-general-3 | any | goal:g7.32.1 | P1 preregistered leaves, council 00:2xZ 10-24 (the frozen leaf P1 mints under; it sits outside the directors' roots [goal:g7.16.1]); until:goal:g7.16.1.11.46.9 |
| (none yet: the first row is the PLANTED add, written after this leaf's engine change lands and a post runs it) | | | | |

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 10-24 (F3, council 01:1xZ, sp): the standing rows matched the trailer's LITERAL parent, so a second-level P1 node (a verdict under an experiment under goal:g4.21) would read unexplained. They now match on the CLOSURE, are narrowed to director-general-3, and retire themselves when goal:g7.16.1.11.46.9 closes (`until:`); lane rows w4 (two-level explained), w4b (another post not), w4c (retired on close), w4d (unresolvable parent not), w4m (a literal-only match is RED). director-goals-1 10-24 (follow-up, council BINDING 00:5xZ): five STANDING rows pre-add P1's frozen leaves (g4.18.2.1, g7.31.3.1, g7.32.3, g4.21, g7.32.1), which sit outside the directors' roots, so P1's first merge does not red F3 on P1 instead of on scope; the lane's `window` mode honours a standing row only when EVERY trailer of a commit names a standing parent (w2b, w3b, w3c). director-goals-1 10-23 (U1 build): (1) grow.py is an engine PIECE in engine-post.md (not a file under extensions/), so the report lives there beside agi-at and agi-turn, which hand it $GROW_TRAILERS and put its lines in the commit message as a trailer block. (2) The ceiling is the post's row cells at the TIP, never the staged tree (a post cannot widen itself in the commit it uses). `*` admits all; a row without both cells, or a post with no row, admits nothing and is reported. Values: belam, the three council members, sanctuary-master and thought-master `grow *` `roots *`; every other v4 director `grow` = goal hypothesis experiment verdict idea build mvp outcome doc task, `roots` = its owning_goal (goal:g7.16.1 for all but stream-master, goal:g2.27). (3) Report mode never refuses: a failing report is `[scope-report-broken]` on stderr with the gate's rc unchanged; the lane has a refusing-gate mutant that must read RED. (4) Falsifier 3's literal `git log --since=24h` returns nothing in any repo (git ignores the unit-less spelling), so a gate that never wrote a trailer and one that did would both fail it; the lane's `window` mode uses `--since='24 hours ago'`, the one change to the falsifier's text. (5) C1 of goal:g7.16.1.11.13 is re-cut for the two changed `commit-tree` lines (TABLE row N10). (6) G (the growth matrix) is spawn_gate's APPROVE in the same gate, so SCOPE adds only the post's type mask and the parent closure.
<!-- THOUGHT:END -->
