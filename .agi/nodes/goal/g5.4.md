---
id: goal:g5.4
mint_id: 6ea00939f8e14d958d59b423d41a0208
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 0.9
edited_by: sanctuary-master
goal_id: G5.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: c204fd7fe047b614
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - l4
thought_session: g1-g7-rewrite-2026-09-19
title: "G5.4: The season review and rollover, end to end"
---
<!-- BODY:BEGIN -->
**The season review and the rollover, end to end.** Brief point **B21** of the L4 mapping round (L4.20), minted so the point exists in the graph rather than only in a plan document.

**Source:** owner, A:183 — read the verbatim by pointer in `doc:l4-owner-decisions` ("L4 PLAN") and the row itself in `doc:l4-plan` §5.0-5.1, never copied here.

**What this becomes, in later rounds:** sub-goal → chain → build in `season.py`, scattering to `goal:g15`. Rounds **L4.18** and **L4.19** carry it and both are `Owner go? YES`.

**Minted by** `sanctuary-director` L4 gen I on 2026-09-09 under L4.20, whose claim is that every brief point B1-B25 exists under an EXISTING perpetual goal. No top-level goal was added; `goal:s29`'s shapes hold for any build node a later round adds.

## OWNER 2026-10-14 ~21:0xZ, verbatim (answer to SM's 20:50Z [decision] '--skip-fold core? yes / no', relayed by belam's signed [owner] box mail fa6e39d06c to SM + the council)
"Skip it. Or better yet overwrite it completely for season 3 since I don’t mind overwriting things between seasons only. Specifically during season rollover to clean up failed efforts like core which was lead by grok bot unsuccessfully"

## OWNER 2026-10-15 ~00:4xZ, verbatim (relayed by belam's signed [owner] box mail ceb6dfdada to SM + TM, for the council)
"Can we also move everyone to core/season3/main and yourself to core/main?"

## OWNER 2026-10-15 ~00:4xZ, verbatim, two follow-ups right after the line above (belam's signed relays df49da5795 and the next one, to SM + TM)
"I’m fine with keeping season3/main as well actually"
"And using it"

## OWNER 2026-10-15 ~02:2xZ (belam's stamp), verbatim (answer to SM's 01:08:15Z [decision] (A) --skip-fold sanctuary + streaming-suite / (B) overwrite their mains; relayed by belam's signed [owner] box mail 254e170a81 04:35:02Z to SM + TM)
"Let's go with B to keep everything aligned at this time"

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 44 21:0xZ 10-14: the owner's word on the season-2 -> 3 rollover, verbatim above (no THOUGHT block before; status and every earlier body line untouched; the edited_by stamp belam -> sanctuary-master). Read: (1) the rollover run carries --skip-fold core; (2) the owner's preferred form: at the rollover, core/main is OVERWRITTEN to the season-3 line (not folded, not merged), archive first; overwrites only between seasons, at a rollover. Placed (SM, council word asked): the archive of the old core/main tip to an origin archive ref, then a lease-guarded overwrite of core/main (lease = the archived sha), by belam as the Prime AFTER the --apply; never a history rewrite of the live trunk or season3/main.
sanctuary-master gen 44 00:4xZ 10-15: the owner's second rollover word, verbatim above. Read (council places, SM proposed 00:4xZ): season 3's ONE live town trunk = core/season3/main (every post's trunk cell and the landing target move there after the switch); the Prime's integration line = core/main (replaces season3/main as the PASS target) [SUPERSEDED 00:44Z: season3/main stays the PASS line; core/main is ff-fed from it, P2']. This supersedes the 23:50Z placement 'local-maxxing/season3/main is the live trunk'; local-maxxing/season3/main becomes the read-only twin.
sanctuary-master gen 44 00:4xZ 10-15: the two follow-ups above: season3/main is KEPT AND USED (not archived, not a dead twin); how core/main and season3/main relate is the council's placement (SM proposed it 00:4xZ).
sanctuary-master gen 44 04:36:17Z 10-15: the owner's (B) above: sanctuary/main and streaming-suite/main are OVERWRITTEN to the season-3 line between seasons, the core treatment. The run has no overwrite mode, so its argv still gains --skip-fold sanctuary --skip-fold streaming-suite (the judge refuses both folds: pre-season-2 schemas); the overwrite is its own act (archive ref first, explicit --force-with-lease, read back). Bytes, order and who pushes = the council's placement (SM proposes).
<!-- THOUGHT:END -->
