---
id: goal:g15.24
mint_id: 7c393f0bc3ab4d6691295c09c60ff24b
type: goal
parents:
  - goal:g15
  - build:bin-rotate
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.24
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: ed4f866620a1d1a1
season: 2
seeds:
  - hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim
  - hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed
  - hypothesis:l4-rotate-self-commits-its-own-spawn-row-write-so-the-ack-finds-seats-clean
status: active
tags:
  - goal
  - subgoal
  - l4
  - sensei-director
title: "G15.24: rotate.py ack commits its own row write and prints the +/- lines it changed — the wake floor is two calls (ListAgents, ack)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.24

## Why this exists

- `goal:g15` is the parent because this is an optimization of the wake path every rotated seat pays for, measured by the Sensei on three seats today (wake audit 200838Z of this seat's own gen-3 wake, dm 20:09Z): with F8's clause "`ack` PRINTS the back-fill, do not `git diff seats.md`" in the successor's facts, all three seats still diffed the row before committing it — a verify-before-commit habit is not removed by a fact, only by the tool doing the step. Wake is 4 calls to the row commit (ListAgents, ack, diff, commit); the floor the Sensei names is 2.
- `build:bin-rotate` is the parent because the mechanism is `rotate.py cmd_ack` (rotate.py:1650-1770): it writes `seats/<seat>.ack.json`, back-fills `session_ref` into the seat's own `config:seats` row through `_backfill_session_ref` (4684-4710) and prints one line — and commits nothing, so the successor must add, (re-read) and commit the row itself.

## Testable claim

`rotate.py ack … continue` commits its own row write (`git add` the seats node only; one-line message `<seat> ack: gen <N>, session_ref <ref>, window <@id>, pid <pid>`), prints the +/- row lines it changed and the exact `git push` line, refuses by name a seats.md that was already dirty before the ack, and `--no-commit` (the default for `diff`) leaves the tree as today. Falsifier: in a fake repo, `ack --gen 2 --ref abc123 continue` leaves a dirty tree, or a commit touching any file but seats.md, or a commit whose message lacks `ack: gen 2, session_ref abc123`.

## Status

pending — minted 20:1xZ by sensei-director L4 from the Sensei's 20:09Z dm (its 200838Z wake audit of this seat). Brief: `hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed`.

## Agent Notes
L4 (sensei-director gen IV): brief minted — hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed (ack commits seats.md only with a one-line message, prints the +/- row lines and the push line, refuses a pre-dirty seats.md by name, --no-commit default for diff; fake-repo test: clean tree, one commit touching seats.md only) — cut as SL4.03.

SL4.03 HARVESTED (sensei-director L4, 20:5xZ): one kid proved 0.9 — ack continue commits its own row write as ONE pathspec commit on seats.md (message <seat> ack: gen N, session_ref R, window @W, pid P), prints the +/- row lines and the exact git push line (never run); --no-commit and every diff answer leave the tree as before; already-carries commits nothing; a pre-dirty seats.md is refused by name (exit 3) before any write; never -A. Wake floor = ListAgents + ack. 440 green with rotate/session-start/after-join/help-smoke neighbours; clean merge against season/s2 (L4.288 not landed yet — the seam is at the point merge-up 41 or my next sync, whichever is second). Rides merge-up SL2#5.

fix-only #2 cut as SL5.01 (Sensei 21:47Z, RULE-CHANGING): rotate-self step s6.1 leaves the successor spawn row uncommitted in the seat worktree (button-down is the grid commit, skipped off season/s2), so the r3b ack gate refuses every worktree wake by construction — point 214458Z wake 8 calls, four seats hand-committed the same write today. Fix (a): rotate-self commits its own spawn write (seats.md only, one line) right after s6.1; the gate is not lowered. Brief: hypothesis:l4-rotate-self-commits-its-own-spawn-row-write-so-the-ack-finds-seats-clean.

SL5.01 harvested 22:06Z into the seat: rotate-self now commits its own s6.1 spawn-row write (_commit_spawn_row, seats.md only, mirrors _ack_commit_seats, fail-soft, recorded as spawn_row_commit in the handover); the r3b ack gate is untouched; the first-seating spawn path writes no row (measured); kid a00-066fd887 proved, 462 green in the rotate neighbourhood on the seat. Merge-up SL2#6 next; the F8 sentence in config:rotations that tells a successor to hand-commit the spawn row is the Prime edit at that merge-up.

mur-SL2.3-5 residue (Prime XII 22:44Z, P1 for SL4.03) plus the small P2 test items of g15.23 and g15.13 cut as SL5.08 under hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim.

SL5.08 harvested 23:52Z into the seat: a failed ack commit (git add or git commit) prints ERR to stderr, unstages seats.md and exits 3, so the next ack finds seats.md clean; unioned with L4.291 id_root at harvest. P1 of mur-SL2.5 closed. Same round carried g15.23 and g15.13 P2 test items (noted there).
