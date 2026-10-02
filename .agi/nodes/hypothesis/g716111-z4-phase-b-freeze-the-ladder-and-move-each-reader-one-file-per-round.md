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
testable_claim: "(B1) the rollover DUAL-WRITES the GLOBAL season -- the ladder's current_season AND town:core's `season` (core = the root town: core 2 == ladder 2 today, while local-maxxing, streaming-suite and web-app-suite carry their OWN counters of 1 and sanctuary 2, so a per-town season cannot replace the global; the global needs ONE named home, town:core, and towns.py's global-vs-town compare reads core) -- until the 11 season reader sites in 6 files read town:core (spawn_gate :742 :1414 · dispatch :1457 :2349 · send :1153 · rotate :275 :885 :21902 :22240 · seat_status :191 · towns :285); the dual-write ends when those sites read 0 from the ladder, after which a rollover writes 0 bytes to ladder.md (G2 = 0); (B2) after each reader's round, alive's G4 reads equal for every (tier, role) and every row a spawner reads, and the spawners go FIRST in the order workflow.py (serves both setups; its director stages move claude-fable-5-1 -> Sonnet 5.5 as the one named exception, AA2.25), dispatch.py, heal.py, then send, brief, verification; (B3) readers in tools only old-setup posts run stay on the ladder until that post moves."
title: "Z4 phase B: ladder.md is FROZEN, the season rollover DUAL-WRITES the global season to the ladder AND town:core's `season`, and each ladder reader that a v4 post still runs reads the tree/row instead, one file per round, the three spawners first (workflow.py, dispatch.py, heal.py), with spec parity proven per file"
town: core
---
# hypothesis:g716111-z4-phase-b-freeze-the-ladder-and-move-each-reader-one-file-per-round

## Measured
- doc:rse-z4-ladder-out Z4.2 phase B; doc:radically-simple-engine AA2 'Retire ORDER' (self-perpetuating 265eb2c25: workflow.py resolves each stage as a kid of the invoking post via kid-of, overridden by a per-stage model in the workflow's own manifest, BEFORE anything retires).
- season.py writes ladder:ladder at rollover (:1061); claude-code.toml declares source = 'ladder'; 11 season reader sites (listed above). The GLOBAL season's home is town:core (all-is-one 05:xxZ, folded from the reviewed doc:rse-z4-ladder-out at the trunk version 05a5c9a6b): the other towns' own counters cannot replace it.
- RELEASED (belam 05:07Z): the AA2.25 exception is CONFIRMED and the `kid` cell is WRITTEN (e56869124), so B2's workflow.py round is startable after phase A. dispatch.py and heal.py serve only the OLD setup, so they move only as it moves.

## CLAIM
(B1) the rollover DUAL-WRITES the GLOBAL season -- the ladder's current_season AND town:core's `season` (core = the root town: core 2 == ladder 2 today, while local-maxxing, streaming-suite and web-app-suite carry their OWN counters of 1 and sanctuary 2, so a per-town season cannot replace the global; the global needs ONE named home, town:core, and towns.py's global-vs-town compare reads core) -- until the 11 season reader sites in 6 files read town:core (spawn_gate :742 :1414 · dispatch :1457 :2349 · send :1153 · rotate :275 :885 :21902 :22240 · seat_status :191 · towns :285); the dual-write ends when those sites read 0 from the ladder, after which a rollover writes 0 bytes to ladder.md (G2 = 0); (B2) after each reader's round, alive's G4 reads equal for every (tier, role) and every row a spawner reads, and the spawners go FIRST in the order workflow.py (serves both setups; its director stages move claude-fable-5-1 -> Sonnet 5.5 as the one named exception, AA2.25), dispatch.py, heal.py, then send, brief, verification; (B3) readers in tools only old-setup posts run stay on the ladder until that post moves.

## Dispatch line
config-max: the per-stage `model` key in a workflow manifest (graph) and town:core's `season` cell (the global season's one home) / template-max: none / code: one reader file per round (build rounds, each with its own parity proof).

## FALSIFIERS
Z4.c B1 after a rollover EVERY season reader (the 11 sites) returns the new season, read from town:core once moved; when they read 0 from the ladder the dual-write stops and a rollover writes 0 bytes to ladder.md (G2 = 0) · per round G4 parity equal for the moved reader · negative: no round moves two reader files.

## TESTS
alive's G1-G4 count/parity script run before and after each round; a season-rollover dry run; the moved file's own tests.

## FILE SCOPE
one reader file per round (workflow.py first) · season.py's rollover write · claude-code.toml source. HORIZON until phase A lands (belam's three owner items are ruled).

## CEILING
1 parent per round · kids <= 1 · one file per round · regular review.
