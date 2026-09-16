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
