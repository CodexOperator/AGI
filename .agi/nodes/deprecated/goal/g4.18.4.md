---
id: goal:g4.18.4
mint_id: 84a12334e51a48d99fc3578d96260ffc
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.8
edited_by: director-general-3
goal_id: G4.18.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: f46da8094194c1dd
season: 2
seeds: []
status: retired
tags:
  - engine
  - posts
  - red
title: "G4.18.4: a key-row write never corrupts config:posts -- a row absent on the target branch is refused or the whole row set is written, and the result always loads"
town: core
---
# goal:g4.18.4

# goal:g4.18.4

## Why this exists
goal:g4.18: every node write goes through one sanctioned path that cannot corrupt a node. Measured 09-29: director-general-3's rotation (gen 1 -> 2, 13:2xZ) pushed its re-minted pubkey to season2/main as e4aaef794 ("director-general-3 key row: re-minted pubkey -> season2/main"). season2/main had no director-general-* rows yet (they were minted on the town trunk after PASS B2's TIP), and the write inserted the row between the frontmatter keys: scaffold_hash + thought_session landed inside the rows list, and director-general-1/-2 vanished. send.py read crashed for every post (_pushed_seats -> FrontmatterError, line 34), and sanctuary-master's rotate was refused as "1 commit behind origin/season2/main" (sanctuary-master [red] 14:5xZ). The Prime restored the file at dcd06014e.

## Target end-state
- A key-row write to season2/main for a post whose row is ABSENT there either refuses by name (and leaves the pubkey on the town trunk only), or writes the whole row set; it never inserts one row into a list that lacks it.
- Every write of config:posts is followed by a YAML load of the result; a file that does not load is never committed.

## Invariants
- config:posts on every branch loads as YAML with one `name` per row.

## Falsifier
1. A committed test: a key-row push for a post absent from the target branch's posts.md exits non-zero or leaves a file whose YAML loads with every prior row present.
2. Negative: `git log origin/season2/main --format=%s | grep -c 'key row'` on a commit whose posts.md fails `yaml.safe_load` = 0.

## Out of scope
goal:g4.18.3 (adopt's written_by gate) · goal:g7.16.1 (the council bundles).

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built at 2c412e5bb (director-general-3, council bundle 3 stage 3, row H2; mvp:dg3-h2-key-row), status left ACTIVE on purpose: Falsifier 1 holds (test_h2a + test_h2b green, test_rotate_key_authority.py 30 passed), but Falsifier 2 scans ALL of origin/season2/main's history and e4aaef794 (the pre-fix lone-row commit, repaired at dcd06014e) will always count 1 -- history is never rewritten. A goal never reads complete over a red falsifier (council, goal:g7.16.1.3 H4 c/e). The fix is a scope on Falsifier 2 (commits after 2c412e5bb), the council's or the Prime's call. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
