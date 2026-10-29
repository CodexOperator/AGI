---
id: goal:g7.16.1.11.46.28
mint_id: f76de67a9b4442eb8062d5e7efa232cc
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.28
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 49741a573cc51982
season: 3
seeds: []
status: active
tags:
  - rotate
  - push
title: "G7.16.1.11.46.28: rotate's out push skips a posts/<post> branch that is not the pushing seat's (keyed on config:posts role prime_director, never on a missing helper)"
town: local-maxxing
---

# goal:g7.16.1.11.46.28

# goal:g7.16.1.11.46.28

## Why this exists
goal:g7.16.1.11.46 (active, wave 2): sanctuary-master's rotation was blocked twice on 10-28 (11:16Z, 23:4xZ; its [red] 23:4xZ): `rotate.py rotate` on posts/sanctuary-master made its stop_commit, then `_stops_push` refused the out with 'push refused out: could not read Username for github'. Mechanism (all-is-one [view] 23:47:23Z, measured): `branches.parse` raises for posts/<post>, so `mirror_ref_for_branch` returns None and `_stops_push` falls to a head push to origin; a post uid has no github helper (only agi-belam's sudoers line has one), and goal:g15.25 forbids a post branch reaching origin as a head anyway. Placed by the council 3/3 (alive [decision] 23:50:53Z 10-28; aio [view] 23:47:23Z + [word] 23:48:52Z, sp [word] 23:48:17Z, term U): it blocks every non-belam rotation.

## Target end-state
- `rotate.py`'s out push skips the origin push for a posts/<post> branch that is NOT the pushing seat's, keyed on the SEAT: the ONE config:posts row whose role is prime_director names the branch that pushes (posts/<its name>). One line names the skip: `stops push: SKIPPED -- posts/<post> is not the pushing seat's branch (posts/<prime>, config:posts role prime_director); it stays local`; the rotation completes, rc 0.
- The skip is NEVER keyed on a missing github helper: the pushing seat's own push still runs and still refuses by name when it cannot authenticate (skills/agi-rotate: a missing helper is belam's documented, loud failure).
- (U) The pushing seat is read from the config cell (config:posts role prime_director), never a literal name. Zero or several such rows = `stops push: pushing seat unread (<why>); the head push is attempted` (today's behaviour, loud), never a quiet skip.

## Invariants
- A trunk or a branch with a mirror ref takes its path unchanged (the frozen-prime HOLD, the additive mirror); only an unrecognised posts/<post> branch is read for the skip.
- Never a force-push, never a second commit.

## Falsifier
1. (I + U) extensions/agi/tests/test_rotate_post_push_skip.py, every row under a PATH git shim that logs each push and fails it like a uid with no helper (the log is READ): (a) a non-pushing posts/<post> seat -> the exact skip line, `_stops_push` returns None (rc 0), ZERO push lines in the log; (b) posts/<prime>, helper absent -> the push IS attempted (one log line) and refuses by name ('push refused out: ...'), never the skip line; (c) posts/<prime> with a working remote -> 'stops push: OK -- posts/<prime>' and the remote ref == HEAD; (d) zero or two prime_director rows -> 'pushing seat unread (...)' and the push attempted. Mutants, each RED by name: the skip removed -> (a) attempts a push; the skip keyed on the helper (`git config --get credential.helper` rc != 0) -> (b) prints the skip line rc 0.
2. (I) The engine's branches tests stay green (test_branches*.py); the fix stays rotate-side, so a pinned row (test_pinned_branches_still_does_not_know_posts_post) reads posts/<post> still unrecognised by branches.parse, with no mirror ref.
3. (A) The skip line is the run's reading: each run term names it by its exact text and rc, in the same line as the run.

## Out of scope
goal:g15.25 (the post-branch mirror rule itself: teaching branches.parse posts/<post> is a separate change, re-read with falsifier 2's pinned row); goal:g6.47.1 (keygen's push); the github helper on post uids.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted with its build (rotate.py `_pushing_seat_branch` + the skip in `_stops_push`, the test file, two reader_census.tsv rows). Unmeasured, named (sp's U): goal:g15.25's own text. The key is the prime_director ROLE, the same cell agi-sync's upward walk reads; a literal 'belam' would break at the next rename.
<!-- THOUGHT:END -->
