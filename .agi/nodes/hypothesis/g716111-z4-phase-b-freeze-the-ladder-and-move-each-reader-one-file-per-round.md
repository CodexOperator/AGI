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
testable_claim: "(B') ladder.md is FROZEN: no new cell is added to it and no ladder reader is added or MOVED (owner 14:0xZ: the old-setup readers are not fixed, they retire with the old-setup Python); town:core stays the named home of the GLOBAL season (core 2 == ladder 2 today; local-maxxing, streaming-suite, web-app-suite carry their OWN 1, sanctuary 2); the season dual-write and the AA2.25 workflow.py director-stage exception of the old phase B are DROPPED with the move. Z4.b holds: dispatch.py resolve_role_spec for all 8 (tier, role) is unchanged."
title: "Z4 phase B': ladder.md is FROZEN and no ladder reader is moved (owner 14:0xZ: the old-setup readers retire with the old-setup Python, they are not fixed); the old season dual-write + reader-by-reader parity + AA2.25 exception are DROPPED"
town: core
---
# hypothesis:g716111-z4-phase-b-freeze-the-ladder-and-move-each-reader-one-file-per-round

## Measured
- SUPERSEDED 10-02 14:0xZ by belam [owner] 14:01Z (verbatim on goal:g7.16.1.11.15 and town:local-maxxing Agent Notes 64bf778d4): "we don't need to fix the ladder.py readers because we're not gonna, or ladder.md, because we're not gonna have any of those readers". The old phase B (season dual-write; one reader file per round, workflow.py first; AA2.25 parity) is DROPPED: it existed only to move readers. HOLD any phase-B round. (The file slug still says move-each-reader: a mint id never moves, the address may.)
- council re-cut: all-is-one 14:03Z, Z4.6 of doc:rse-z4-ladder-out (posts/all-is-one; not on the trunk yet).
- Facts that stay: season.py writes ladder:ladder at rollover (:1061); claude-code.toml declares source = 'ladder'; the 11 season reader sites are old-setup Python; the v5 engine reads 0 ladder bytes.

## CLAIM
(B') ladder.md is FROZEN: no new cell is added to it and no ladder reader is added or MOVED (owner 14:0xZ: the old-setup readers are not fixed, they retire with the old-setup Python); town:core stays the named home of the GLOBAL season (core 2 == ladder 2 today; local-maxxing, streaming-suite, web-app-suite carry their OWN 1, sanctuary 2); the season dual-write and the AA2.25 workflow.py director-stage exception of the old phase B are DROPPED with the move. Z4.b holds: dispatch.py resolve_role_spec for all 8 (tier, role) is unchanged.

## Dispatch line
config-max: none / template-max: none / code: none (a freeze is the ABSENCE of work; no round is dispatched for B').

## FALSIFIERS
Z4.b: dispatch.py resolve_role_spec for all 8 (tier, role) == before, on the trunk, any day · negative: `git log` shows no commit adding a cell to ladder.md or a new ladder reader after the A landing (c2decf431).

## TESTS
the 8-spec parity script (alive's G4) run once on the trunk; `git log --oneline c2decf431.. -- .agi/nodes/.geometry/ladder.md` empty.

## FILE SCOPE
none: nothing is edited. HORIZON; kept as the record of the superseded phase.

## CEILING
0 rounds.
