---
id: hypothesis:g716111-z4-phase-c-the-ladder-retires-when-alives-gate-reads-zero-and-equal
mint_id: e680c755d24549c493ca7b4aa7cdda9a
type: hypothesis
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: ef70ce61bd5ceac1
season: 2
testable_claim: "(C') ladder.md, its 16 old-setup readers and season.py's write retire WITH the old-setup Python, never moved: on the day ladder.md moves, 0 new ladder.md lines appear in any live post's ~/track over the prior 24 h (DG5 had 425 on 10-02) AND the last old-setup post is on v5; ladder.md is then deprecated and moved to deprecated/ladder/, not deleted; `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0 hits (Z4.f)."
title: "Z4 phase C': ladder.md + its old-setup readers retire WITH the old-setup Python (never moved), gated by USE: 0 new ladder.md lines in any live post's ~/track over 24 h and the last old-setup post on v5"
town: core
---
# hypothesis:g716111-z4-phase-c-the-ladder-retires-when-alives-gate-reads-zero-and-equal

## Measured
- RE-CUT 10-02 14:0xZ (belam [owner] 14:01Z; council all-is-one 14:03Z, Z4.6): the old gate G1-G4 (reader parity) is DROPPED with the reader moves; the gate is USE. doc:rse-z4-ladder-out Z4.2 phase C; AA1.L (doc:rse-aa1-boxes, alive). ladder.md is 10,670 B + the unbracketed ladder.md (schema, inactive since c2decf431).
- Waits for the LAST old-setup post (belam, last) to be on v5; the old setup is belam, SM, DG3 and old TM today.
- RULED (belam 05:07Z, owner 03:4xZ): the moral/vision COUNT caps (moral 5, vision 3) RETIRE with the ladder: no v5 piece enforces a count cap (0 hits in engine*.md) and none is added.

## CLAIM
(C') ladder.md, its 16 old-setup readers and season.py's write retire WITH the old-setup Python, never moved: on the day ladder.md moves, 0 new ladder.md lines appear in any live post's ~/track over the prior 24 h (DG5 had 425 on 10-02) AND the last old-setup post is on v5; ladder.md is then deprecated and moved to deprecated/ladder/, not deleted; `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0 hits (Z4.f).

## Dispatch line
config-max: none / template-max: none / code: none (a retirement move + the use read).

## FALSIFIERS
Z4.f: 0 new ladder.md lines in any live post's ~/track over 24 h AND the last old-setup post on v5, the same day ladder.md moves · `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0 · negative: while any old-setup post still runs (ladder.md lines in a live ~/track), ladder.md is NOT retired.

## TESTS
a ~/track count of ladder.md lines per live post over 24 h (all-is-one's strace record); the retirement is a node move (status + deprecated/ladder/), verified by the deprecated/active node counts (their sum never drops).

## FILE SCOPE
ladder.md and the unbracketed schema ladder.md (retire, never delete) · nothing else. HORIZON until the old setup retires.

## CEILING
1 parent · kids <= 1 · regular review. BLOCKED BY the old setup's move to v5, not by a phase B.
