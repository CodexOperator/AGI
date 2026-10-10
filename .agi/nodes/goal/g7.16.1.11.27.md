---
id: goal:g7.16.1.11.27
mint_id: 8525c18333094556b3d77e747227afd1
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.27
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 08800ee9b06ec6a2
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - mail
  - wake
  - g7.16.1.11
title: "G7.16.1.11.27: the wake is box-only -- agi-run (engine-wrap.md:25) and cccc.ts (:42) stop typing the old send.py read route; box-wake.t.sh DUAL ROUTE s1 becomes its negative"
town: core
---
# goal:g7.16.1.11.27

## Why this exists
goal:g7.16.1.11: the owner made mail box-only ("switch everyone to box only please", relayed by belam [owner] 04:5xZ, SM placement 05:0xZ). The engine still TYPES the old route into every pane: agi-run (engine-wrap.md:25, claude harness) polls the size of `.agi/sessions/inbox/$AGI_SEAT.md` and on growth types `mail: send.py read $AGI_SEAT`, and cccc.ts (engine-wrap.md:42, the pi route) watches the same inbox file and sends `mail: send.py read <seat>`. The box wakes (engine-wrap.md:26 for agi-run, :43 for cccc.ts, which type `mail: box read`) stay. Checked on the bytes at trunk 548bb9c715. Pinned by box-wake.t.sh's DUAL ROUTE rows (:93-103): s1 (an inbox append types the send.py line), s2 (a box send types the box line and never the send.py one) and s4 (both sources grow in one window).

## Target end-state
- A pane is woken for mail only by the box route: agi-run and cccc.ts no longer watch `.agi/sessions/inbox/*.md` and never type `mail: send.py read`.
- box-wake.t.sh's s1 is rewritten to its NEGATIVE (an inbox append wakes nothing), s2 stays, s4 is rewritten to the box source alone; the implementing round names which rows moved.
- test_send.py:8278-8297 is a SECOND pin of the old route (SM 21:4xZ C1, read by me at 4fc8a1dc26): `_run_mail_poll` takes the FIRST line of engine-wrap.md that starts `case $H in` (today :25, the send.py inbox loop) and `test_g53_mail_poll_types_nothing_while_the_inbox_is_absent` asserts `mail: send.py read p` is typed on an inbox append (:8297). With :25 removed the next match is :26 (`case $H in claude*|pi*)`, the box wake), so the append types nothing and the row goes RED. The implementing round rewrites it to the box route (the helper runs the box-wake line against a stubbed `box n`; absent mail types nothing; an append to the inbox file types nothing), or retires it with its reason in the THOUGHT; it does NOT leave a red.
- engine-wrap.md:90 (the 10-07 record of the dual-route decision) stays as history; a new dated line says box-only superseded it.

## Invariants
- A box send still wakes once and not again while unread mail is unchanged (box-wake.t.sh's w-rows keep passing).
- No `.agi/sessions/inbox/*.md` write is added anywhere to keep a wake alive.
- The mail itself is untouched: this leaf changes what is TYPED into a pane, not what is delivered.

## Falsifier
The command that decides is the first backticked one (agi-frontier, engine-post.md:170-173): it exits 0 only when the work is done.
1. `test -z "$(git grep -n -E 'printf "mail: send\.py read|"mail: send\.py read "' -- .agi/nodes/.geometry/engine-wrap.md)"` (2 hits today, engine-wrap.md:25 and :42; the prose line :90 is deliberately not matched).
2. `bash extensions/agi/tests/box-wake.t.sh` exits 0 on the rewritten file, with s1's negative green: an append to `sessions/inbox/alive.md` types nothing for either harness, AND `python3 -m pytest extensions/agi/tests/test_send.py -q -k g53_mail_poll` passes on the rewritten helper (it may not select the box-wake line by accident: a row that still asserts `send.py read` is the failure this item catches).
3. Negative: a box send types `mail: box read` ONCE and `mail: send.py read` zero times, for agi-run and for cccc.ts.

## Out of scope
The OTHER places that still name the old route, found while checking and left to their own round: rotations.md:87 and :125 (the rotation's `inbox` step runs `send.py read {seat}`) and crons.md:24 (a cron command runs `send.py read --box-local --peek`) · goal:g7.16.1.11.24 (AGI_POST in the post unit; a wake needs it) · deleting send.py or the inbox files.

## RULE SM placement 05:0xZ 10-09, from belam [decision] 04:5xZ (SM's relay text; the cites in it are SM's, re-checked above)
"(A) BOX-ONLY WAKE (owner: mail = box only): the engine still types the OLD route into every pane -- agi-run engine-wrap.md:25 (claude*: watches .agi/sessions/inbox/$AGI_SEAT.md, types 'mail: send.py read $AGI_SEAT') and cccc.ts engine-wrap.md:42 (pi: the same inbox file watch); the box wake at :26 / :43 stays. Pinned by box-wake.t.sh's DUAL ROUTE rows (:93-103: s1 inbox growth wakes send.py read, s2 box types box read) -- the implementing round rewrites s1 to its negative."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 23:5xZ: RE-CUT 1 on SM's 21:4xZ return (C1). Read by me at 4fc8a1dc26: test_send.py:8278-8297 `_run_mail_poll` picks the first engine-wrap.md line starting `case $H in` and the g53 row asserts `mail: send.py read p` typed on an inbox append; removing :25 makes :26 (the box wake) the first match and the row red. A second pin the leaf did not name, added to Target and to falsifier 2. Order: .32 cites this leaf as the owner of the :25 retirement, so .32 lands with or after this one. Cites re-read at 4fc8a1dc26: engine-wrap.md :25 :26 :42 :43 :90 unchanged. Previous version: filed 10-09 06:5xZ (see git history).
<!-- THOUGHT:END -->
