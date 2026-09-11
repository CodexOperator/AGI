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
