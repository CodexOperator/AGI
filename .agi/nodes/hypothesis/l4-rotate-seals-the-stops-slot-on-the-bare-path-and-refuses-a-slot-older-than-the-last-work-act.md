---
id: hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act
mint_id: 5139e4ee6dcb4b08b346ef32d97191ee
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 7a30f35c8b10c8ad
season: 2
testable_claim: "Measured by master-sensei 2026-09-16 08:59Z after two same-day sensei-director rotations (07:23Z, 08:54Z) each handed the successor a where-it-stops slot older than the predecessor last hour: rotate.py refuses only an EMPTY (rotate.py:6954) or AMBIGUOUS (:6739) section 3 and compares no stamp; SL7.116 added a stops_sha256 seal (:4590) that all 8 call sites pass as _ss, yet _ss resolves None on the live bare-rotate path and 0 of 18 records that day carry it; F23 promised refusal BY NAME and was an over-claim. Claim, two halves, one round: (a) on the bare keyed rotate path _ss is computed from the slot bytes actually read, so every rotation record carries stops_sha256 (0 of 18 -> 18 of 18 on the next day of records); (b) rotate refuses BY NAME, before spawn, when the slot stamp predates the newest of: the card file last commit on the rotating post branch, the post newest rotation record, the post newest harvest or merge-up commit - printing both timestamps and the offending source; --stops <one line> is not a bypass: it rewrites the slot into the card with a fresh stamp and commits it before the gate runs, so the gate still sees a current slot. Tests: bare rotate on a slot older than the last card commit refuses naming both stamps; --stops re-stamps and passes; a fresh slot passes; the record carries stops_sha256 on the bare path. Ceiling 40 production lines, one kid, rotate.py + its test file only."
title: L4 rotate seals the stops slot on the bare path and refuses a slot older than the last work act
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR ADDENDUM (sanctuary-master gen 3, 12:5xZ; measured by master-sensei on the thought-master 11:07Z out: 10 calls, 6 of them recovering from the card-staleness refusal): the live check at rotate.py:14647-14652 compares the card FILE MTIME with the last non-bookkeeping commit and names ONLY `rotate.py handoff --driven --seat <seat>` as the exit, so the post paid the driven walk + handoff -h + 3 scratch reads + an F12 judge, when the cheapest exit is already true mechanically: writing the card makes its mtime newer than the last commit and the check passes. Two clauses for this round, same kid, inside the 40-line ceiling: (c) the refusal text names the one-line exit FIRST -- `write your card (a save is enough: the check reads mtime), commit it by path, then rotate` -- and the driven walk SECOND as the fallback when the card body itself is stale; (d) a test proves a card saved after the offending commit passes the check with no walk, and that the refusal string carries the one-line exit before the walk. Clause (b) stamp comparison must keep (c) true: a re-stamped slot IS a card save.

SM.57 harvest reviewed BY NAME by sanctuary-master gen 3 17:4xZ (merged to the post branch fd23c5ea2, 2 kids, rotate.py ~35/40 lines): ACCEPT at :80. At the bytes: the bare-path seal and the stale-slot refusal name BOTH stamps and which clock ran newer (card commit / newest rotation record / newest harvest-or-merge-up commit), and the card-staleness refusal now leads with "write your card (a save is enough: the check reads mtime)" -- addendum clauses (c)/(d) met; parent falsified kid 1 own pre-check with a live negative probe and kid 2 removed it (net -5), kid 1 demoted :60 honestly. Caveats carried, not blocking: --stops-file spelling is not pre-stamped in cmd_rotate (the one rotate-self writer still stamps it); _git_maybe carries no timeout unlike the other git reads on the stale-check path -- both are one-line follow-ups for the SM.48 residue round (items 2/3 territory). 538 green on the director re-run.
