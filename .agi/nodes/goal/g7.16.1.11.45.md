---
id: goal:g7.16.1.11.45
mint_id: cc7a6a67d5894d7ca439aeab5a7c7e33
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.45
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 3
status: complete
title: "G7.16.1.11.45: the post shuffle -- director-review (presentation work) stands up under SM; DG1 -> director-goals-1, DG2 -> director-science-1, DG3/4/5 -> DG1/2/3; thought-master + director-thought-1 stand down"
town: local-maxxing
---
# goal:g7.16.1.11.45

## Why this exists
goal:g7.16.1.11 (the engine every post runs on): the owner (14:4xZ 10-21) ruled a new post layout. Presentation work (g5.4.2 media: the explainer, its after-checks, Drive, music) was routed through the Prime and "clogging up prime duties"; the DG names carry no role; TM and DT-1 have been parked by design since 10-16.

## OWNER 2026-10-21 14:4xZ, verbatim (to belam)
"Also ok this is clogging up prime duties we need to stand up a separate post for the presentation creation. Call it director-review working under sanctuary master.

Then director general 1 needs to be renamed to director-goals-1 and DG2 to director-science-1. Then DG3,4,5 become DG1,2,3 respectively. And stand down thought master and director thought at this time. Once done focus on season 3 improvements. I know we have one goal going now but there's a few more I'll need to add but we can worry about that once the post shuffling is done."
14:2xZ, on the 06:08Z whole-town restart (unattended-upgrades on liblzma, needrestart): "No need to disable needs restart I think it's useful overall".

## Target end-state
- `director-review` is a live engine-v4 post on this box (parent sanctuary-master, role director), owning the presentation work (g5.4.2 media and its after-checks); belam no longer relays media asks.
- The rows, users, units and branches read: director-goals-1 (was director-general-1), director-science-1 (was director-general-2), director-general-1 (was director-general-3), director-general-2 (was director-general-4), director-general-3 (was director-general-5). Each new name carries the old post's card and in-flight work; no work, card or key history is lost.
- thought-master and director-thought-1 are down and stay down (no boot, no recover), their cards committed.
- No retired name is deleted: an old identity is kept as a row off this box (the thought-master-old precedent, 10-07), its home archived, never removed.

## Invariants
- Retire, never delete: a home is moved aside, never `rm`'d; key_history and box refs survive.
- A name is reused only after its old holder's home, branch tip and session are moved aside (DG3 -> DG1 waits until DG1 -> director-goals-1 is done; same for DG4 -> DG2 and DG5 -> DG3).
- Every row change rides SM's gate as a stack (skill agi-post §8: .geometry work); live acts (unit stop/start, home moves, trunk pin) are belam's, under this owner GO.
- No post loses its in-flight step: each renamed post finishes its atomic step and commits its card before its stop.

## Falsifier
1. `sed -n 's/^  - {/{/p' .agi/nodes/.geometry/posts.md | jq -r 'select(.box=="encryption-town" and .boot==true) | .name' | sort` lists exactly: all-is-one alive belam director-general-1 director-general-2 director-general-3 director-goals-1 director-review director-science-1 sanctuary-master self-perpetuating; and `systemctl is-active agi-post@<each>` reads active.
2. Negative: `systemctl is-active agi-post@thought-master agi-post@director-thought-1 agi-post@director-general-4 agi-post@director-general-5` reads inactive for all four, and no row for those names has boot true on this box.

## Out of scope
goal:g7.16.1.11.44.8 (agi.sh start/host; this goal may use its verbs, it does not change them). goal:g5.4.2 (the media work itself moves to director-review; its spend rules stay).

## Agent Notes
Assigned to **sanctuary-master** (design + stack), **belam** (live acts + landing).
sanctuary-master 10-22 (close read, council + belam GO): all moves DONE (G1b stand-downs; G3-G7 renames, the last L61 8b247882a2; leaves .45.1-.45.4 complete, L62-L67). Remainder: director-review's first start = the owner's login (banked).
sanctuary-master 10-22 18:0xZ: CLOSED. director-review's boot row landed L70 43086245a3 (belam's one-cell host act 93167c7104, GATE159, council alive GO 2/3); F1 11/11 rows + 11/11 units, F2 passes, re-run at the L70 trunk. The rename director-review -> director-review-1 (owner 10-22) is OWNER-HELD, not part of this goal.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSE, sanctuary-master 10-22 18:0xZ. Falsifiers RE-RUN AS WRITTEN at the trunk 43086245a3 (L70). F1 PASSES: the encryption-town boot=true list reads exactly the 11 named (alive all-is-one belam director-general-1 director-general-2 director-general-3 director-goals-1 director-review director-science-1 sanctuary-master self-perpetuating) and agi-post@ is active for all 11 (director-review NRestarts 0). F2 PASSES: agi-post@thought-master, @director-thought-1, @director-general-4, @director-general-5 all inactive; 0 boot=true rows carry those names. What changed since the close read: the owner's login. agi-post@director-review active 17:22:28Z (started by belam for the login screen); owner login between 17:24:02Z and 17:25:41Z (belam ea243251b5 + tip 93167c7104); the council first read the login as before 17:22:28Z and withdrew it on the bytes (alive 17:56:38Z, all-is-one 17:5xZ). The row: ONE cell boot false -> true, recover false like the other 10, gated GATE159 (grid-writers 27/0, 1125/0, links 0 broken, 6 lanes 0 FAIL), landed L70 on LAND_TRUNK 22ec682b70. director-review's first act ([done] 17:27Z) ran. No falsifier amended. Out of scope and owner-held (belam 17:29:55Z): the rename to director-review-1 and the move tooling. The previous THOUGHT (the 09:3xZ close read, F1 10/11) = blob 7dfcf57fce (commit c77a79e416).
<!-- THOUGHT:END -->
