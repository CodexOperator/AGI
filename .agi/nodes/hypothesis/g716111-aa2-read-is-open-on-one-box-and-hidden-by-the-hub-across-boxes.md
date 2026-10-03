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
testable_claim: "On a hub with the matrix hide filter (331 B awk), DG1 sees {DG1, SM}, SM sees {council, DG1, SM}, council sees {council, SM}, and a fetch of a hidden branch by name fails (`couldn't find remote ref`) (AA2.13, PASS on a scratch hub); the one-box half is NOT here: ruling 2 (b) made it per-post object stores (a separate hypothesis)."
title: "AA2.13: across boxes the hub's upload-pack runs under `hide P lands(P)` so each post sees only itself, its parent and the children it lands from, and a hidden branch fetch by name is refused (the slug keeps the old one-box wording: ONE-box read is now per-post object stores, belam ruling 2 (b), hypothesis g716111-aa2-per-post-object-stores-make-one-box-look-like-n-boxes)"
town: core
---
# hypothesis:g716111-aa2-read-is-open-on-one-box-and-hidden-by-the-hub-across-boxes

## Measured
- doc:radically-simple-engine AA2 'READ, stated as it is': measured by alive and all-is-one 00:2xZ: objects/ and refs/ are group agi rwx + other r-x; the one-box answer is now per-post object stores (ruling 2 (b)); the hub `hide` is the across-boxes answer: ONE mechanism, the matrix, box or hub.
- SETTLED: belam accepted ruling 2 = (b) (signed [decision] 04:45Z): one box gets one git object store per post user (owner 00:34Z), see hypothesis g716111-aa2-per-post-object-stores-make-one-box-look-like-n-boxes; the council lands cell is DONE on the trunk (b6b2c33d3). This hypothesis keeps ONLY the hub-side `hide` for ACROSS boxes.
- Depends on the carrier/hub (goal:g7.16.1.11.11 AA1.3, a second box).

## CLAIM
On a hub with the matrix hide filter (331 B awk), DG1 sees {DG1, SM}, SM sees {council, DG1, SM}, council sees {council, SM}, and a fetch of a hidden branch by name fails (`couldn't find remote ref`) (AA2.13, PASS on a scratch hub); on one box read is NOT restrictable (one shared object store, packs mix every branch), so the box-local half is an owner/belam ruling, not a test.

## Dispatch line
config-max: the hub's hide hook as an installed cell / template-max: none / code: `hide` (331 B awk) on the hub side.

## FALSIFIERS
AA2.13 a hub under `hide` shows each post only itself, its parent and its lands-children, and refuses a hidden fetch by name

## TESTS
scratch hub test (PASS) re-run on the built bytes.

## FILE SCOPE
the hub-side hide hook · the doc. HORIZON: needs a hub and a second box.

## CEILING
1 parent · kids <= 1 · +331 B on the hub side only · regular review.
