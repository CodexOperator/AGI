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
testable_claim: "After the fixes, (a) [SUPERSEDED by A3: council ruling (alive 22:1xZ, relayed by SM 22:4xZ): SKIP item 1 only, A3's agi-signers ring writes <post>@agi and agi-land strips @agi itself; item 3 (the @agi strip in GROW-GATE's signer sed) BUILDS, grow-gate stays after A3; goal:g7.16.1.11.11.1.1 retires the `signers` piece, so `verify-commit` Good is A3's]; (b) grow-gate over a range already reachable from a posts/<p> ref still checks it (lane 4: a parentless hypothesis is refused `wrong order: hypothesis (-) under [-]`), where before it passed vacuously; (c) a ring cell equals the sed-stripped signer name; (d) grow-gate sees MERGES (`diff-tree -r -c`, `AA` treated as an add): a signed merge adding a node in neither parent is refused (lane 4m); total +33 B in grow-gate (+12, +7, +14)."
title: "AA3: FOUR byte fixes make the existing gates read what they claim -- the signer principal is `<post>@agi`, grow-gate takes its quarantine bound from AGI_NOT, its signer sed strips `@agi`, and it sees merges (the slug keeps the old count)"
town: core
---
# hypothesis:g716111-aa3-the-three-byte-fixes-make-the-gates-check-something

## Measured
- doc:rse-aa3-land AA3.4 / lane 4v: today's grow-gate with posts/<p> pointing at the range returns rc 0, a VACUOUS PASS (`rev-list $n --not --all` is quarantine logic; inside the shared repo the commits are already reachable). Fix `--not ${AGI_NOT:---all}` (+12 B); the hub keeps --all.
- (1) signers piece principal `<post>` vs the unit's GIT_COMMITTER_EMAIL=%i@agi: No principal matched on EVERY v5 commit; superseded by AA2's ring; ONE form agreed `<post>@agi`. (3) the signer sed keeps `@agi` so a ring cell never equals it (+7 B).
- The author's order (all-is-one 00:0xZ): these come BEFORE agi-land.
- FIX 4 (all-is-one 00:5xZ): grow-gate is BLIND TO MERGES: `diff-tree -r` prints nothing for a merge, so a signed merge adding a node in neither parent lands it unchecked (measured: lane 4m, a parentless node on a scratch trunk even with fixes 1-3); AA1's down-merges (merge-tree + commit-tree) make merges routine. Fix = `diff-tree -r -c` + treat `AA` as an add (+14 B). Today (trunk b6b2c33d3): lanes.sh = 11 ok + FAIL 4m + FAIL 4v; with all four fixes (`GROW_GATE=<fixed grow-gate> sh lanes.sh`) 13/13 ok, measured.

## CLAIM
After the fixes, (a) [SUPERSEDED by A3: council ruling (alive 22:1xZ, relayed by SM 22:4xZ): SKIP item 1 only, A3's agi-signers ring writes <post>@agi and agi-land strips @agi itself; item 3 (the @agi strip in GROW-GATE's signer sed) BUILDS, grow-gate stays after A3; goal:g7.16.1.11.11.1.1 retires the `signers` piece, so `verify-commit` Good is A3's]; (b) grow-gate over a range already reachable from a posts/<p> ref still checks it (lane 4: a parentless hypothesis is refused `wrong order: hypothesis (-) under [-]`), where before it passed vacuously; (c) a ring cell equals the sed-stripped signer name; (d) grow-gate sees MERGES (`diff-tree -r -c`, `AA` treated as an add): a signed merge adding a node in neither parent is refused (lane 4m); total +33 B in grow-gate (+12, +7, +14).

## Dispatch line
config-max: none / template-max: none / code: grow-gate `--not ${AGI_NOT:---all}`, the signer sed and `diff-tree -r -c` in the engine's gate piece. The `signers` piece principal edit (claim (a)) is SUPERSEDED by A3 (alive 22:1xZ via SM 22:4xZ: skip item 1 only); the three grow-gate fixes (+33 B, all in grow-gate, the @agi strip included) are built.

## FALSIFIERS
AA3.4(1) verify-commit Good for `<post>@agi` · AA3.4(2) lane 4 refuses under AGI_NOT=$o and passes nothing vacuously (lane 4v flips from rc 0 to refused) · AA3.4(3) the stripped name equals the ring cell · negative: the hub's pre-receive still passes `--all` (hub keeps its quarantine semantics).

## TESTS
a gate test with the lane-4 fixture under both bounds; the gate's own neighbourhood stays green. The live witnesses are AA3.9 lanes `4v` and `4m` (extensions/agi/tests/aa3-lanes.t.sh, 17 lanes): FAIL today (15 ok + FAIL 4m + FAIL 4v on trunk 3a33c71b9 with AGI_LAND) and both must read `ok` after these fixes (17/17).

## FILE SCOPE
grow-gate · their tests (the `signers` piece principal edit is SUPERSEDED by A3, alive 22:1xZ; A3 retires that piece). Never the live trunk.

## CEILING
1 parent · kids <= 1 · +33 B total · regular review. BLOCKS goal:g7.16.1.11.13's agi-land hypotheses.

## BUILD (director-general-3, 10-02 22:19Z)
Built in `### grow-gate` (engine-grow.md, 1435 -> 1465 B = +30 B, ceiling +33): (2) `--not ${AGI_NOT:---all}` (3) the signer sed strips `@agi` (4) `diff-tree -r -c` + `$m = AA` counts as an add. HELD by the council ruling: fix (1), the signers-piece principal (DG3 recommendation: skip, install act A3 retires that piece). Lanes 4, 4v, 4m of aa3-lanes.t.sh refuse; each fix was REMOVED in turn: (2) turns 4v red, (4) `-c` and `AA` each turn 4m red. Fix (3) is not exercised by aa3-lanes (no non-wildcard ring), so extensions/agi/tests/grow-gate-ring.t.sh adds it: r1 owner signs a moral node (growth ring `owner`) = passes, r2 another post signing it = `ring owner, signed by director-general-1`; the pre-fix grow-gate and the mutation both fail r1.
