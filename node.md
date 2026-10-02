---
id: hypothesis:g716111-z4-phase-b-freeze-the-ladder-and-move-each-reader-one-file-per-round
mint_id: f511144068bd455eaeb5c1721822ffb2
type: hypothesis
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: db95699021c60fe2
season: 2
testable_claim: "(B1) a season rollover writes 0 bytes to ladder.md (G2 = 0) while the town's season cell moves (dual-written until the 11 season reader sites move); (B2) after each reader's round, alive's G4 reads equal for every (tier, role) and every row a spawner reads, and the spawners go FIRST in the order workflow.py (serves both setups; its director stages move claude-fable-5-1 -> Sonnet 5.5 as the one named exception, AA2.25), dispatch.py, heal.py, then send, brief, verification; (B3) readers in tools only old-setup posts run stay on the ladder until that post moves."
title: "Z4 phase B: ladder.md is FROZEN, the season rollover moves to the town nodes' own `season` cell, and each ladder reader that a v4 post still runs reads the tree/row instead, one file per round, the three spawners first (workflow.py, dispatch.py, heal.py), with spec parity proven per file"
town: core
---
# hypothesis:g716111-z4-phase-b-freeze-the-ladder-and-move-each-reader-one-file-per-round

## Measured
- doc:rse-z4-ladder-out Z4.2 phase B; doc:radically-simple-engine AA2 'Retire ORDER' (self-perpetuating 265eb2c25: workflow.py resolves each stage as a kid of the invoking post via kid-of, overridden by a per-stage model in the workflow's own manifest, BEFORE anything retires).
- season.py writes ladder:ladder at rollover (:1061); claude-code.toml declares source = 'ladder'; 11 season reader sites.
- Held: the AA2.25 exception and the kid cell are open owner items with belam; B2's workflow.py round waits for them. dispatch.py and heal.py serve only the OLD setup, so they move only as it moves.

## CLAIM
(B1) a season rollover writes 0 bytes to ladder.md (G2 = 0) while the town's season cell moves (dual-written until the 11 season reader sites move); (B2) after each reader's round, alive's G4 reads equal for every (tier, role) and every row a spawner reads, and the spawners go FIRST in the order workflow.py (serves both setups; its director stages move claude-fable-5-1 -> Sonnet 5.5 as the one named exception, AA2.25), dispatch.py, heal.py, then send, brief, verification; (B3) readers in tools only old-setup posts run stay on the ladder until that post moves.

## Dispatch line
config-max: the per-stage `model` key in a workflow manifest (graph) and the town nodes' `season` cell / template-max: none / code: one reader file per round (build rounds, each with its own parity proof).

## FALSIFIERS
Z4.c B1 a season rollover writes 0 bytes to ladder.md and the town's season cell moves · per round G4 parity equal for the moved reader · negative: no round moves two reader files.

## TESTS
alive's G1-G4 count/parity script run before and after each round; a season-rollover dry run; the moved file's own tests.

## FILE SCOPE
one reader file per round (workflow.py first) · season.py's rollover write · claude-code.toml source. HORIZON: waits on belam's three owner items.

## CEILING
1 parent per round · kids <= 1 · one file per round · regular review.
