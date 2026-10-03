---
id: hypothesis:g716111-aa2-tier-is-projected-depth-and-a-kid-reads-one-inherited-kid-cell
mint_id: f8587a75501c4165b49b6a1bb6c76931
type: hypothesis
parents:
  - goal:g7.16.1.11.12
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: b679c278629d8c37
season: 2
testable_claim: "(a) depth projected from the ruled cells = belam 1 · council 2 · members, SM, TM-new 3 · DG1, DT-1 4 (77 B awk), and the rows' stored `tier` cell (1 on all 12 v4 rows, stale) retires with the ladder (AA2.20); (b) `kid-of P` (327 B jq) with ONE `kid` cell on belam's row resolves `{harness: claude-code, model: claude-sonnet-5-5, max: 3}` for DG1, self-perpetuating and belam, and resolves nothing for stream-master (outside the tree: it spawns nothing) (AA2.21); (c) today every v4 row's AGI_KID_MODEL is EMPTY, so agi-kid's `--model $AGI_KID_MODEL` is empty and kids on the new engine are unconfigured: the one inherited cell fixes it (AA2.22); (d) a kid spawned by DG1 runs the inherited spec and agi-kid refuses past `kid.max` (AA2.23)."
title: "AA2.20-23: a post's tier is its DEPTH projected from the parent cells (never stored), and a kid's spawn spec is the nearest ancestor-or-self row's `engine.kid` cell (one inherited template), so a v4 kid is configured without the ladder"
town: core
---
# hypothesis:g716111-aa2-tier-is-projected-depth-and-a-kid-reads-one-inherited-kid-cell

## Measured
- doc:radically-simple-engine AA2 'LADDER OUT' (posts/self-perpetuating 1b2e62b56; belam 04:43Z [decision]): Owner 03:1xZ, verbatim (via belam 04:43Z [decision]): "Oh okay yeah well we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."
- Measured on today's cells (b6b2c33d3): the v4 engine reads 0 ladder bytes (no engine*.md names it); only the old setup reads it (19 Python files under extensions/agi/bin, dispatch.py's roles table chiefly). The ladder gave three things a tree already holds: `tiers` (-> projected depth), `roles` (-> `kid-of` over one inherited `engine.kid` cell, the owner's 'every subagent Sonnet 5.5'), `read_order` + `caps.director_kids` (-> the row's `seeds` cell, already on all 12 v4 rows, and `kid.max`).
- FOUND while measuring: no v4 row sets kid_model, so AGI_KID_MODEL is empty for every v4 post. The kid is a LEAF under its post in PHI (a P->kid->P petal while it lives, no row) and its work comes UP within lands(P).
- The `kid` cell is WRITTEN on belam's row (e56869124, 05:07Z: {harness: claude-code, model: claude-sonnet-5-5, max: 3}); the build items below remain.
- Seams: agi-kid hardcodes AGI_HARNESS=pi-free + `pi --provider openrouter`, so a claude-code spec needs a harness case (a build item); the key broker ('no dispatch from a v5 post') still gates PAID spawns; all-is-one's map retires the `tier` row cells and `caps.director_kids` into `kid.max`.
- Where it runs: inside agi-kid at spawn (EXPANSION in engine-wrap, ~+360 B: kid-of + the `max` count `ls ~/k|wc -l`), NEVER in agi-project whose bytes are BASE (the base would go to ~8,318 B). base 0 B, seed 0 B.

## CLAIM
(a) depth projected from the ruled cells = belam 1 · council 2 · members, SM, TM-new 3 · DG1, DT-1 4 (77 B awk), and the rows' stored `tier` cell (1 on all 12 v4 rows, stale) retires with the ladder (AA2.20); (b) `kid-of P` (327 B jq) with ONE `kid` cell on belam's row resolves `{harness: claude-code, model: claude-sonnet-5-5, max: 3}` for DG1, self-perpetuating and belam, and resolves nothing for stream-master (outside the tree: it spawns nothing) (AA2.21); (c) today every v4 row's AGI_KID_MODEL is EMPTY, so agi-kid's `--model $AGI_KID_MODEL` is empty and kids on the new engine are unconfigured: the one inherited cell fixes it (AA2.22); (d) a kid spawned by DG1 runs the inherited spec and agi-kid refuses past `kid.max` (AA2.23).

## Dispatch line
config-max: ONE `kid` cell on belam's row (`engine.kid` = harness / model / max; the Prime lands cells it owns) / template-max: none / code: kid-of (327 B jq) + the `max` count + a claude-code harness case in agi-kid (~+360 B, engine-wrap expansion).

## FALSIFIERS
AA2.20 depth projected from the ruled cells = 1/2/3/4 as tabled (PASS scratch) · AA2.21 kid-of with one `kid` cell on belam resolves every tree post and nothing outside the tree (PASS scratch) · AA2.22 every v4 row's AGI_KID_MODEL is empty today (PASS, measured: the gap) · AA2.23 a kid spawned by DG1 runs the inherited spec and agi-kid refuses past kid.max (build) · negative: after the cell, `AGI_KID_MODEL` is non-empty on every tree post and still empty for stream-master.

## TESTS
scratch tests over a fixture posts.md (the ruled cells): depth table, kid-of resolution (inside and outside the tree), the max refusal; one live kid spawn by DG1 after the build.

## FILE SCOPE
engine-wrap agi-kid (kid-of, max, the claude-code harness case) · the `kid` cell on belam's row (the Prime's) · tests. HORIZON behind the owner's go on the build; the paid-spawn key broker is unchanged.

## CEILING
1 parent · kids <= 2 · ~+360 B expansion, 0 B in the base or seed · regular review.
