---
id: hypothesis:g716111-z4-phase-a-graph-only-the-town-schema-drops-the-ladder-parent
mint_id: 3a552ea7266b4dd89bb0d7c51531164e
type: hypothesis
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 0bc0042adfbbc9a0
season: 2
testable_claim: "(L1) grow-project over today's schemas is byte-identical to the live growth.tsv (149 shape rows); (L2) after A1 + A2: 149 -> 148, exactly 3 rows differ (`ladder - goal` and `town - ladder` out, `town - goal+vision` in) and 147 nids are unchanged; (L3) the 5 towns as they stand are refused by the NEW matrix until A3; (L4) after A3 they are legal (only `locked: key none`); (L5) grow-check over every live node, old matrix vs new: 5,494 nodes, 0 verdicts move; and dispatch.py resolve_role_spec for all 8 (tier, role) plus workflow.py's director-stage model are unchanged (Z4.b, G4 parity)."
title: "Z4 phase A: with the [town] schema edit, ladder.md out of the projector and the 5 towns' ladder parent dropped, grow-project goes 149 -> 148 rows, exactly 3 rows differ, and 0 of 5,494 live nodes change verdict except the 5 towns -- with no reader or spec touched"
town: core
---
# hypothesis:g716111-z4-phase-a-graph-only-the-town-schema-drops-the-ladder-parent

## Measured
- doc:rse-z4-ladder-out Z4.2 phase A and Z4.4 L1-L5 (scratch on trunk 3928fed44, schemas + nodes via git archive, 0 live bytes touched). Bytes: 3 schema lines + 1 matrix row fewer + 5 parent lines out; 0 B in the zygote.
- A is Option A: an ANCHOR-SIGNED schema edit (the schema of [town] is a signed anchor: this leaf names the edit, it does not make it).
- The first town parents today: vision:the-living-being + goal:g26.towns + ladder:ladder.

## CLAIM
(L1) grow-project over today's schemas is byte-identical to the live growth.tsv (149 shape rows); (L2) after A1 + A2: 149 -> 148, exactly 3 rows differ (`ladder - goal` and `town - ladder` out, `town - goal+vision` in) and 147 nids are unchanged; (L3) the 5 towns as they stand are refused by the NEW matrix until A3; (L4) after A3 they are legal (only `locked: key none`); (L5) grow-check over every live node, old matrix vs new: 5,494 nodes, 0 verdicts move; and dispatch.py resolve_role_spec for all 8 (tier, role) plus workflow.py's director-stage model are unchanged (Z4.b, G4 parity).

## Dispatch line
config-max: none / template-max: the [town] schema parent shape / code: none (the projector's glob only).

## FALSIFIERS
Z4.a after A on the trunk grow-check parity moves 0 verdicts except the 5 towns (L5 on the landed bytes) · Z4.b dispatch.py resolve_role_spec for all 8 and workflow.py's director-stage model are identical before and after · negative: no reader file under extensions/agi/bin changes in the A range.

## TESTS
the Z4 scratch cases L1-L5 re-run on the landed bytes; the 8-spec parity script (alive's G4) before/after.

## FILE SCOPE
[town].md (signed anchor, the Prime's) · [ladder].md renamed in place to ladder.md (unbracketed, `active: false`; the projector glob skips it; NOT moved to deprecated/) · the 5 town:* nodes' parents · growth.tsv (projected). No Python.

## CEILING
1 parent · kids <= 1 · 3 schema lines + 5 parent lines · regular review. STARTABLE (belam 05:07Z: 'Phase A may start via DG1'); the [town] schema commit needs belam's anchor signature, so it is its OWN commit.

## Residue (mur dg1z4a-c1)
Verdict accept_with_residue (verify wins; files `.agi/sessions/workflows/runs/mur-dg1z4a-c1/{review,verify}_dg1z4a-c1.json`). Four conjuncts MET; L5 UNVERIFIED (the 5.5k-node walk; the experiment names `.geometry/ladder.md` as the 6th mover). Refuted, nothing owed: C1-C3 carry no per-commit signature norm (belam re-authored them blob-equal at landing); `create.sh` / `core.md:122` stale ladder text is phase B/C scope.
- ONE later round (not owed in phase A): `extensions/agi/tests/test_town_mint_final.py:175` asserts the a00-80511a41 fence still says `--parent ladder:ladder` (fence at `experiment/a00-80511a41-c96c9f.md:69-71`; the new schema refuses that line). The round fixes the fence to the goal:g26.towns + vision lines AND deletes the substitution at `:176-177` together; the test goes loudly red if only one half moves.
- Notes, left as they are (tests stay byte-equal to 45c2a4d82): `test_illegal_parent_ladder_refused_by_name` compares list order with the sorted print (wrap in `sorted()` in that round); the numstat in `experiment:a00-ed087c41-517fc1` says 36/21 for `test_town_mint.py` where the bytes say 31/21 (text only).
