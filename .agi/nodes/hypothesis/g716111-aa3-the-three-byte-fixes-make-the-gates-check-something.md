---
id: hypothesis:g716111-aa3-the-three-byte-fixes-make-the-gates-check-something
mint_id: f5f9370d1ce543c296d0a9f2c58e7c89
type: hypothesis
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: c27adafa16aa71e7
season: 2
testable_claim: "After the fixes, (a) `verify-commit` on a v5 commit with the ring writing `<post>@agi` reads Good; (b) grow-gate over a range already reachable from a posts/<p> ref still checks it (lane 4: a parentless hypothesis is refused `wrong order: hypothesis (-) under [-]`), where before it passed vacuously; (c) a ring cell equals the sed-stripped signer name; total about +19 B."
title: "AA3: three byte fixes make the existing gates read what they claim -- the signer principal is `<post>@agi`, grow-gate takes its quarantine bound from AGI_NOT, and its signer sed strips `@agi`"
town: core
---
# hypothesis:g716111-aa3-the-three-byte-fixes-make-the-gates-check-something

## Measured
- doc:rse-aa3-land AA3.4 / lane 4v: today's grow-gate with posts/<p> pointing at the range returns rc 0, a VACUOUS PASS (`rev-list $n --not --all` is quarantine logic; inside the shared repo the commits are already reachable). Fix `--not ${AGI_NOT:---all}` (+12 B); the hub keeps --all.
- (1) signers piece principal `<post>` vs the unit's GIT_COMMITTER_EMAIL=%i@agi: No principal matched on EVERY v5 commit; superseded by AA2's ring; ONE form agreed `<post>@agi`. (3) the signer sed keeps `@agi` so a ring cell never equals it (+7 B).
- The author's order (all-is-one 00:0xZ): these come BEFORE agi-land.

## CLAIM
After the fixes, (a) `verify-commit` on a v5 commit with the ring writing `<post>@agi` reads Good; (b) grow-gate over a range already reachable from a posts/<p> ref still checks it (lane 4: a parentless hypothesis is refused `wrong order: hypothesis (-) under [-]`), where before it passed vacuously; (c) a ring cell equals the sed-stripped signer name; total about +19 B.

## Dispatch line
config-max: none / template-max: none / code: grow-gate `--not ${AGI_NOT:---all}` and the signer sed in the engine's gate piece; the signers piece principal.

## FALSIFIERS
AA3.4(1) verify-commit Good for `<post>@agi` · AA3.4(2) lane 4 refuses under AGI_NOT=$o and passes nothing vacuously (lane 4v flips from rc 0 to refused) · AA3.4(3) the stripped name equals the ring cell · negative: the hub's pre-receive still passes `--all` (hub keeps its quarantine semantics).

## TESTS
a gate test with the lane-4 fixture under both bounds; the gate's own neighbourhood stays green. The live witness is AA3.9 (lanes.sh in doc:rse-aa3-land): `FAIL 4v` today (10 ok + FAIL 4v on trunk faabf9b7a+) and it must read `ok 4v` after these fixes.

## FILE SCOPE
grow-gate · the signers piece (engine-post) · their tests. Never the live trunk.

## CEILING
1 parent · kids <= 1 · +19 B total · regular review. BLOCKS goal:g7.16.1.11.13's agi-land hypotheses.
