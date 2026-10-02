---
id: hypothesis:g716111-aa2-read-is-open-on-one-box-and-hidden-by-the-hub-across-boxes
mint_id: 8d532e4405d34f93b11f0c16fe87874d
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 4c4af5909c3165c4
season: 2
testable_claim: "On a hub with the matrix hide filter (331 B awk), DG1 sees {DG1, SM}, SM sees {council, DG1, SM}, council sees {council, SM}, and a fetch of a hidden branch by name fails (`couldn't find remote ref`) (AA2.13, PASS on a scratch hub); on one box read is NOT restrictable (one shared object store, packs mix every branch), so the box-local half is an owner/belam ruling, not a test."
title: "AA2.13: across boxes the hub's upload-pack runs under `hide P lands(P)` so each post sees only itself, its parent and the children it lands from, and a hidden branch fetch by name is refused; on ONE box read stays open (recommended, banked to belam)"
town: core
---
# hypothesis:g716111-aa2-read-is-open-on-one-box-and-hidden-by-the-hub-across-boxes

## Measured
- doc:radically-simple-engine AA2 'READ, stated as it is': measured by alive and all-is-one 00:2xZ: objects/ and refs/ are group agi rwx + other r-x; per-post object stores fed by root are the only one-box option and cost a store per post.
- TWO belam rulings pending (self-perpetuating asked 00:5xZ): read on one box (recommend open); the council lands cell is DONE on the trunk (b6b2c33d3), so hold only AA2.13's one-box half.
- Depends on the carrier/hub (goal:g7.16.1.11.11 AA1.3, a second box).

## CLAIM
On a hub with the matrix hide filter (331 B awk), DG1 sees {DG1, SM}, SM sees {council, DG1, SM}, council sees {council, SM}, and a fetch of a hidden branch by name fails (`couldn't find remote ref`) (AA2.13, PASS on a scratch hub); on one box read is NOT restrictable (one shared object store, packs mix every branch), so the box-local half is an owner/belam ruling, not a test.

## Dispatch line
config-max: the hub's hide hook as an installed cell / template-max: none / code: `hide` (331 B awk) on the hub side.

## FALSIFIERS
AA2.13 a hub under `hide` shows each post only itself, its parent and its lands-children, and refuses a hidden fetch by name · the one-box half is HELD for belam's ruling (recommended: open read on a box).

## TESTS
scratch hub test (PASS) re-run on the built bytes; the one-box half is a documented non-test.

## FILE SCOPE
the hub-side hide hook · the doc. HORIZON: needs a hub and a second box; the one-box ruling is belam's.

## CEILING
1 parent · kids <= 1 · +331 B on the hub side only · regular review.
