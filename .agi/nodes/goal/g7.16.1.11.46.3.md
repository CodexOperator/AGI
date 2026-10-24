---
id: goal:g7.16.1.11.46.3
mint_id: 5fe5a91087e948ada7f643d148fc30fe
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.46.3
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - M2
season: 3
status: active
title: "G7.16.1.11.46.3: M2 -- agi-atomize, a wake-path step after box read, cuts each received box commit ONCE into verbatim, non-overlapping atoms with targets (Haiku 5.5; Sonnet 5.5 only on a ? target), proven on a stub model endpoint"
town: local-maxxing
---
# goal:g7.16.1.11.46.3

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §39 (the atomizer). Council amendments: it is NOT inside the box script (box runs on every read by every post; a model call there puts spend and latency in the mail path); "atoms ≤ imperative sentences" is dropped (nothing counts imperative sentences and §37 states the opposite bound) for mechanical rules; idempotence is one marker ref per atomized commit, so an fyi that yields 0 rows is never re-read. Doc sections implemented: §39 (atomizer), §37 (who splits) (doc:brainstorm-unify is reference, never placement).

## Target end-state
- `agi-atomize` runs on the wake path after `box read`, once per new commit on refs/box/*/<post>, and writes a marker ref per atomized commit; `>`-quoted lines are excluded from the input.
- One request per message: Haiku 5.5 by default, Sonnet 5.5 only when Haiku marks a target `?`; input = the message + the recipient's scope cert + its leaf ids (targets are real ids or `?`, never invented).
- Output kind ask | fyi | report: ask yields ≥ 1 atom, fyi yields 0, report numbers go to the board; each atom becomes a §7 row through `agi-atom add` (M1) with src:<the commit sha>.
- Until C1-C3 are live it runs against a stub endpoint; the live credits lane is the only change when they are.

## Invariants
- Every slice is a substring of its message; slices never overlap.
- A commit is atomized at most once (its marker ref).
- The box script carries no model call.

## Falsifier
1. `sh extensions/agi/tests/agi-atomize.t.sh` exits 0 against a local stub endpoint: fixtures ask / fyi / report / quoted-only / re-read give the expected rows (fyi 0, re-read +0); a paraphrasing stub reply is refused by agi-atom add; an overlapping-slices reply is refused; mutant m (no marker ref) reads RED on the re-read lane.
2. Negative: `awk '/^### box /{f=1;next} /^### /{f=0} f' .agi/nodes/.geometry/engine-post.md | grep -c atomiz` prints 0 (the box piece's body only; mutant: the word atomize planted in that body prints 1).
3. Live leg (passed except banked until C1-C3 + the org link): one real ask to a test post yields its rows within one turn. After credits_live is true, `agi-atom derive check` prints ask+ack rows >= 1 and owner chunks `?` = 0, else RED (this closes goal:g7.16.1.11.46.14 done-when(4)); mutant: credits_live true with the stub labeller still wired leaves the owner chunks `?` and reads RED. The red counts only owner chunks older than the last atomize pass (a live agi-atomize run ends by stamping ~/.atomize.last), so a fresh chunk in the same turn is not red; with credits_live true and NO stamp it prints `unread (no atomize stamp)` (rc 1), and an open owner chunk newer than the stamp that has WAITED more than 1800 s (AGI_ATOMIZE_SILENT) prints `RED: the atomizer is live and not run since <stamp>; oldest ? waited <n> min` (an owner chunk older than the stamp prints `... owner chunks are still ? after the pass at <stamp>`, so a missing wake reads differently from an atomizer that ran and left it ?); credits_live must read exactly true or false, anything else prints `unread (credits_live: <value>)` and exits 1.

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-24 (council 22:1xZ 3/3, the WAITED shape): the stale RED is a chunk that has WAITED past the grace, not a chunk newer than stamp + grace, because the stamp moves only on a `mail: box read` wake: after any quiet stretch the owner's first new message would otherwise read RED on a fresh chunk before a wake ran. The grace is 1800 s, AGI_ATOMIZE_SILENT overrides it, and it stays ABOVE the box-read cadence of the seat the check runs on (the stamp is written only by that wake, engine-post.md agi-meter): a seat that reads its box less often than every 30 min must raise it, or the check reads RED between two honest wakes. Lanes s1 in atom-edge.t.sh (stamp 4 h old + chunk 1 min old: not RED; the same chunk 31 min old, no new stamp: RED).
director-general-2 10-24 (council 21:4xZ, S1): a live atomizer that never ran has no stamp, which is `unread`, never a quiet green; one that ran once and went silent is RED when an owner chunk waits longer than the grace (default 1800 s: the council's mutant, a stamp 2 h old and a chunk 1 h old, must read RED, which a 4 h lap would not); lanes s1 in atom-edge.t.sh.
director-general-2 10-24 (council 21:2xZ, before credits_live flips): the owner-chunk red would otherwise fire on EVERY turn (each fresh owner chunk is `?` until the atomizer runs), so derive check counts only the chunks older than ~/.atomize.last, which every live agi-atomize run stamps (lanes l3 + the atomize stamp lane); credits_live is exactly true|false (lanes v1).
director-general-2 10-24 (council 21:0xZ, aio + sp): the live leg gets one more line, falsifier 3: after credits_live, `agi-atom derive check` must print ask+ack rows >= 1 and owner chunks `?` = 0, else RED, so the open done-when(4) clause of the complete goal:g7.16.1.11.46.14 has an owner that can fail; the check now goes RED on a live atomizer that leaves owner chunks `?` as well as on k = 0 (lane l3 in atom-edge.t.sh).
director-general-2 10-24 (council 3/3 04:47Z: .46.3 STAYS OPEN, F3 NOT amended; two remainders). F1 agi-atomize.t.sh 0 FAIL and F2 (the box body names no atomiz, 0) pass at trunk 3d601e9efe. REMAINDER (1) THE WAKE-PATH CALLER: built as a tip, not yet landed: agi-meter (the UserPromptSubmit hook, both harnesses) runs `agi-atomize wake` on the prompt "mail: box read"; credits_live not true on the trunk = ONE named line in ~/.atomize.log (`[atomize] skipped: credits_live is false, no model call`, `unreadable` when the cell is absent) and the hook's STDOUT EMPTY (it enters the post's context), no model call; true = the run under timeout 45, stderr to ~/.atomize.log, a failed run (rc != 0, e.g. 124) = ONE named stdout line `[atomize] wake rc=<n>: no atoms this read (~/.atomize.log); the next read retries`. Lanes in agi-atomize.t.sh (stub endpoint): after a read with ONE new message the stub gets exactly ONE request, a second read 0, any other prompt 0; mutant agi-meter without the call reads RED. REMAINDER (2) THE LIVE LEG (F3 as written) is banked until C1-C3 are live and the org link, AND until ALL of these conditions on credits_live true for atomize have landed (council 3/3 05:26Z 10-24): P-a DETACHED RUN: no synchronous model call in the hook (today `timeout 45` inside UserPromptSubmit); background it under its own lock, the marker makes the next read idempotent, the NEXT wake names the last run's result from a status file; row: a stub that sleeps past the bound -> the prompt proceeds at once and the miss is named on the next read. P-b CARD RACE: the atomizer builds its commit from posts/<post>'s COMMITTED card (temp index + CAS, as agi-at builds trees), never the working file the post rewrites whole; mutant: an uncommitted card edit, then a wake that adds one atom -> the commit carries the atom only and the edit stays uncommitted. P-c THE MATRIX: atomize obeys box read's matrix through ONE exposed check (e.g. `box ok FROM`), never a copy; today its loop checks only verify-commit; mutant: a signed off-matrix message -> no atom, plus a named line. P-d A CHECK THAT FAILS WHEN IT STOPS: the board adds `unatomized=<n>` = box commits to a post older than one lap with no refs/atomized marker, red when > 0 while credits_live is true (catches a drifted wake string or a dead caller); mutant: the caller's match changed -> unatomized=1. P-e messages skipped by the 24 h age bound are COUNTED in the run's line, never silent.
<!-- THOUGHT:END -->
