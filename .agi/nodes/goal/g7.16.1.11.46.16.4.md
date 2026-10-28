---
id: goal:g7.16.1.11.46.16.4
mint_id: befefb30f1914e169f457f30ecbc519d
type: goal
parents:
  - goal:g7.16.1.11.46.16
next_edges: []
edited_by: director-general-3
goal_id: G7.16.1.11.46.16.4
goal_kind: subgoal
season: 3
status: active
title: "G7.16.1.11.46.16.4: unify --check reads an OWN-WRITE origin-snap mirror tip GREEN (the tip ITSELF on the live first-parent chain, 0 merges since) and a foreign one RED; an unreadable rev-list is unread, RED by name"
town: local-maxxing
confidence: 0.5
origin: goal
seeds: []
tags: []
---
# goal:g7.16.1.11.46.16.4

## Why this exists
goal:g7.16.1.11.46.16 (COMPLETE, L238): its row 1 read `unify --check` 6319/6319 at 21:5xZ 10-27; by 23:10Z the same read on the trunk printed 3 RED 'no merge commit takes the live tip as its first parent' (0c772dbafc, 9faf50074b, c1cbfc52f6), each an origin-snap mirror tip that is OUR OWN pushed version the live ref then moved past (DG3 [finding] 23:10Z; SM [placed] 23:11Z, here, a new leaf; .46.16 stays closed). By 23:3xZ the class was SIX: 34a607fdc8, 50952ab682, ac8fa55e97 joined (my own L239 grid versions v6 / v4 / v4 of the .46.16.3 nodes). Every one: O on L's first-parent chain, L ahead by 1, 0 merges in O..L. Each grid push of ours makes another, so the check reds on the writer's normal cadence.

## Target end-state
- In `_unify_check`, for the origin-snap namespace (`grid.py` `_own_write_tip`): a mirror tip O is GREEN when O ITSELF is on the live tip L's first-parent chain (`rev-list --first-parent L` contains O) AND `rev-list --merges O..L` is empty. A FOREIGN O, reached only through a second parent or not at all, stays RED.
- Every rev-list there with rc != 0 is `unread`, RED by name, never GREEN (a rev-list git cannot read prints 0 lines, and 0 lines is never 0 merges); a mirror ref at a MISSING object reads `RED <mint> (unread: an ancestry or count read failed)`, never folded into 'not an ancestor'.

## Invariants
- `--check` stays read-only: no ref written, no record stamped.
- The owner's 40 (owner-batch tree=live 40) stay 0 RED; a check that cannot read never reads GREEN.

## Falsifier
1. `sh extensions/agi/tests/grid-origin-snap.t.sh` exits 0 with rows w1-w3, each with a mutant that reads RED: w1 an own-write mirror tip (pushed x, live moved on to y) -> no RED on it, and a foreign tip taken in as a 2nd parent only -> RED 'no merge commit takes the live tip as its first parent' (mutant: the whole test cut to a bare ancestor test -> GREEN); w2 a --merges walk git cannot read (rc 128) -> RED 'unread: rev-list --merges rc 128' (mutant: the rc check cut -> 0 merges, GREEN); w3 a mirror ref at a missing object -> RED 'unread: an ancestry or count read failed' (mutant: the split cut -> 'not an ancestor').
2. Selector, on the live refs, read-only: `grid.py unify --check --into refs/grid --legacy refs/grid/origin-snap` with the TRUNK's grid.py before this land prints the named own-write tips RED (6 at 23:3xZ: 0c772dbafc, 34a607fdc8, 50952ab682, 9faf50074b, ac8fa55e97, c1cbfc52f6); at the landed tip it prints `unified N/N`, 0 RED, and `owner-batch tree=live 40`.

## Out of scope
goal:g7.16.1.11.46.16.2 (which records --owner-batch may write); goal:g7.16.1.11.46.16.3 (double mints).

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-27 23:5xZ: minted IN its build (one gate), on L240 133f772e35. The shape is self-perpetuating's 23:12:04Z, taken by SM's 23:12Z [correction], 3/3 = alive [decision] 23:16:27Z. MEASURED at the build: each half of the GREEN test alone keeps a foreign 2nd-parent-only O RED, because the merge that took O in always sits inside O..L; with ancestry already checked above (ltip ancestor of ntip), '0 merges in O..L' implies 'O on the first-parent chain'. So the named mutant is the WHOLE test cut to a bare ancestor test (sp's 'first-parent test cut to a bare ancestor test' read literally, with the merges half still standing, stays RED: measured, lane row FAIL on first run). The missing-object row reached the early ancestry gate first, which named it 'an old tip is not an ancestor', so that gate now splits an unreadable read (rc other than 0/1, or a count rc != 0) out as unread.
<!-- THOUGHT:END -->
